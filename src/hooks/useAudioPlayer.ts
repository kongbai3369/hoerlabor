import { useState, useEffect, useRef, useCallback } from 'react';
import type { ListeningTrack, EngineMode } from '../types/listening';
import { useListeningStore } from '../store/useListeningStore';

export interface AudioPlayerControls {
  engineMode: EngineMode;
  isPlaying: boolean;
  isShadowingPause: boolean;
  activeSegmentIndex: number;
  currentTime: number;
  duration: number;
  playbackRate: number;
  isLoopingSentence: boolean;
  togglePlay: () => void;
  pause: () => void;
  seekToSegment: (index: number, autoPlay?: boolean) => void;
  seekToTime: (time: number) => void;
  nextSegment: () => void;
  prevSegment: () => void;
  setPlaybackRate: (rate: number) => void;
  toggleLoopSentence: () => void;
}

// Wiktionary 真实母语发音缓存与并发音频控制
const wiktionaryAudioCache = new Map<string, string>();
let currentWordAudio: HTMLAudioElement | null = null;

/**
 * 独立单词/词组即点即读：优先使用 Wiktionary (维基词典) 真实母语者原声录音，
 * 若未收录则自动无缝兜底至浏览器原生德语发音引擎。
 */
export async function speakGermanWord(wordText: string): Promise<'wiktionary' | 'tts'> {
  if (currentWordAudio) {
    currentWordAudio.pause();
    currentWordAudio = null;
  }
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }

  // 提取核心词形（去除冠词 der/die/das/sich 及标点、语法注解）
  const clean = wordText
    .replace(/^(der|die|das|sich|den|dem|des|ein|eine)\s+/i, '')
    .replace(/\s*\(\+.*\)/g, '')
    .replace(/[.,!?;:()„“”"']/g, '')
    .trim();

  if (!clean) return 'tts';

  const capitalized = clean.charAt(0).toUpperCase() + clean.slice(1);
  const lower = clean.toLowerCase();
  const candidates = Array.from(new Set([clean, capitalized, lower]));

  // 优先命中内存缓存
  const cachedUrl = wiktionaryAudioCache.get(clean) || wiktionaryAudioCache.get(capitalized);
  if (cachedUrl) {
    try {
      const audio = new Audio(cachedUrl);
      currentWordAudio = audio;
      await audio.play();
      return 'wiktionary';
    } catch {
      // 缓存失效继续重试
    }
  }

  // 探测 Wiktionary Commons 真实德语母语者音频
  const tryLoadAudio = (wordVariant: string): Promise<string | null> => {
    return new Promise((resolve) => {
      const url = `https://commons.wikimedia.org/wiki/Special:FilePath/De-${encodeURIComponent(wordVariant)}.ogg`;
      const audio = new Audio(url);
      let resolved = false;

      const timer = window.setTimeout(() => {
        if (!resolved) {
          resolved = true;
          audio.src = '';
          resolve(null);
        }
      }, 1500);

      audio.oncanplaythrough = () => {
        if (!resolved) {
          resolved = true;
          window.clearTimeout(timer);
          resolve(url);
        }
      };

      audio.onerror = () => {
        if (!resolved) {
          resolved = true;
          window.clearTimeout(timer);
          resolve(null);
        }
      };
    });
  };

  for (const cand of candidates) {
    const verifiedUrl = await tryLoadAudio(cand);
    if (verifiedUrl) {
      wiktionaryAudioCache.set(clean, verifiedUrl);
      wiktionaryAudioCache.set(cand, verifiedUrl);
      try {
        const audio = new Audio(verifiedUrl);
        currentWordAudio = audio;
        await audio.play();
        return 'wiktionary';
      } catch {
        break;
      }
    }
  }

  // 若维基词典未收录该变形词，自动兜底至 Web Speech API
  if ('speechSynthesis' in window) {
    const utter = new SpeechSynthesisUtterance(clean);
    utter.lang = 'de-DE';
    utter.rate = 0.95;
    const voices = window.speechSynthesis.getVoices();
    const deVoice =
      voices.find((v) => v.lang === 'de-DE' && v.name.includes('Natural')) ||
      voices.find((v) => v.lang === 'de-DE') ||
      voices.find((v) => v.lang.startsWith('de'));
    if (deVoice) utter.voice = deVoice;
    window.speechSynthesis.speak(utter);
  }
  return 'tts';
}

export function useAudioPlayer(track: ListeningTrack): AudioPlayerControls {
  const engineMode: EngineMode = track.audioUrl ? 'audio' : 'tts';
  const { autoPauseSeconds } = useListeningStore();

  const [isPlaying, setIsPlaying] = useState(false);
  const [isShadowingPause, setIsShadowingPause] = useState(false);
  const [activeSegmentIndex, setActiveSegmentIndex] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState<number>(track.duration ?? 0);
  const [playbackRate, setPlaybackRateState] = useState(1.0);
  const [isLoopingSentence, setIsLoopingSentence] = useState(false);
  const [prevTrackId, setPrevTrackId] = useState(track.id);

  if (prevTrackId !== track.id) {
    setPrevTrackId(track.id);
    setIsPlaying(false);
    setIsShadowingPause(false);
    setActiveSegmentIndex(0);
    setCurrentTime(0);
  }

  const audioRef = useRef<HTMLAudioElement | null>(null);
  const rafIdRef = useRef<number | null>(null);
  const activeIndexRef = useRef(0);
  const isLoopingRef = useRef(false);
  const playbackRateRef = useRef(1.0);
  const isPlayingRef = useRef(false);
  const autoPauseRef = useRef(autoPauseSeconds);
  const pauseTimerRef = useRef<number | null>(null);

  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);
  const ttsSessionIdRef = useRef(0);
  const ttsLoopTimerRef = useRef<number | null>(null);

  const startRafLoopRef = useRef<() => void>(() => {});
  const speakSegmentByIndexRef = useRef<(index: number) => void>(() => {});

  useEffect(() => {
    autoPauseRef.current = autoPauseSeconds;
  }, [autoPauseSeconds]);

  const syncActiveIndex = useCallback((index: number) => {
    activeIndexRef.current = index;
    setActiveSegmentIndex(index);
  }, []);

  const clearShadowingTimer = useCallback(() => {
    if (pauseTimerRef.current !== null) {
      window.clearTimeout(pauseTimerRef.current);
      pauseTimerRef.current = null;
    }
    setIsShadowingPause(false);
  }, []);

  const stopRaf = useCallback(() => {
    if (rafIdRef.current !== null) {
      cancelAnimationFrame(rafIdRef.current);
      rafIdRef.current = null;
    }
  }, []);

  const stopTts = useCallback(() => {
    ttsSessionIdRef.current += 1;
    if (ttsLoopTimerRef.current !== null) {
      window.clearTimeout(ttsLoopTimerRef.current);
      ttsLoopTimerRef.current = null;
    }
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    utteranceRef.current = null;
  }, []);

  const startRafLoop = useCallback(() => {
    stopRaf();

    const tick = () => {
      const audio = audioRef.current;
      if (!audio || audio.paused) return;

      const now = audio.currentTime;
      setCurrentTime(now);

      const segments = track.segments;
      const currentSeg = segments[activeIndexRef.current];

      if (
        isLoopingRef.current &&
        currentSeg &&
        currentSeg.startTime !== null &&
        currentSeg.endTime !== null
      ) {
        if (now >= currentSeg.endTime - 0.015) {
          audio.currentTime = currentSeg.startTime;
        }
      } else if (
        autoPauseRef.current > 0 &&
        currentSeg &&
        currentSeg.endTime !== null &&
        now >= currentSeg.endTime - 0.02
      ) {
        // 触发句间跟读留白停顿
        const nextIdx = activeIndexRef.current + 1;
        if (nextIdx < segments.length) {
          audio.pause();
          stopRaf();
          setIsShadowingPause(true);
          pauseTimerRef.current = window.setTimeout(() => {
            setIsShadowingPause(false);
            if (!isPlayingRef.current || !audioRef.current) return;
            syncActiveIndex(nextIdx);
            const nextSeg = segments[nextIdx];
            if (nextSeg && nextSeg.startTime !== null) {
              audioRef.current.currentTime = nextSeg.startTime;
              setCurrentTime(nextSeg.startTime);
            }
            audioRef.current.play().then(() => startRafLoopRef.current()).catch(() => {});
          }, autoPauseRef.current * 1000);
          return;
        }
      } else {
        const matchedIdx = segments.findIndex(
          (seg) =>
            seg.startTime !== null &&
            seg.endTime !== null &&
            now >= seg.startTime &&
            now < seg.endTime
        );
        if (matchedIdx !== -1 && matchedIdx !== activeIndexRef.current) {
          syncActiveIndex(matchedIdx);
        }
      }

      rafIdRef.current = requestAnimationFrame(tick);
    };

    rafIdRef.current = requestAnimationFrame(tick);
  }, [stopRaf, syncActiveIndex, track.segments]);

  const speakSegmentByIndex = useCallback(
    (index: number) => {
      if (!('speechSynthesis' in window)) return;
      const targetSeg = track.segments[index];
      if (!targetSeg) {
        setIsPlaying(false);
        isPlayingRef.current = false;
        return;
      }

      stopTts();
      const currentSessionId = ttsSessionIdRef.current;

      const utterance = new SpeechSynthesisUtterance(targetSeg.german);
      utterance.lang = 'de-DE';
      utterance.rate = playbackRateRef.current;

      const voices = window.speechSynthesis.getVoices();
      const deVoice =
        voices.find((v) => v.lang === 'de-DE' && v.name.includes('Natural')) ||
        voices.find((v) => v.lang === 'de-DE') ||
        voices.find((v) => v.lang.startsWith('de'));
      if (deVoice) utterance.voice = deVoice;

      utterance.onend = () => {
        if (currentSessionId !== ttsSessionIdRef.current || !isPlayingRef.current) {
          return;
        }

        const delayMs = isLoopingRef.current
          ? 300
          : autoPauseRef.current > 0
          ? autoPauseRef.current * 1000
          : 150;

        if (autoPauseRef.current > 0 && !isLoopingRef.current) {
          setIsShadowingPause(true);
        }

        ttsLoopTimerRef.current = window.setTimeout(() => {
          setIsShadowingPause(false);
          if (currentSessionId !== ttsSessionIdRef.current || !isPlayingRef.current) return;

          if (isLoopingRef.current) {
            speakSegmentByIndexRef.current(index);
          } else {
            const nextIdx = index + 1;
            if (nextIdx < track.segments.length) {
              syncActiveIndex(nextIdx);
              speakSegmentByIndexRef.current(nextIdx);
            } else {
              setIsPlaying(false);
              isPlayingRef.current = false;
            }
          }
        }, delayMs);
      };

      utterance.onerror = () => {
        if (currentSessionId !== ttsSessionIdRef.current) return;
        setIsPlaying(false);
        isPlayingRef.current = false;
      };

      utteranceRef.current = utterance;
      window.speechSynthesis.speak(utterance);
    },
    [stopTts, syncActiveIndex, track.segments]
  );

  useEffect(() => {
    startRafLoopRef.current = startRafLoop;
    speakSegmentByIndexRef.current = speakSegmentByIndex;
  });

  useEffect(() => {
    stopRaf();
    stopTts();
    if (pauseTimerRef.current !== null) {
      window.clearTimeout(pauseTimerRef.current);
      pauseTimerRef.current = null;
    }
    isPlayingRef.current = false;
    activeIndexRef.current = 0;

    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.src = '';
      audioRef.current = null;
    }

    if (track.audioUrl) {
      const audio = new Audio(track.audioUrl);
      audio.preservesPitch = true;
      audio.playbackRate = playbackRateRef.current;

      const handleLoadedMetadata = () => {
        setDuration(audio.duration || track.duration || 0);
      };

      const handleEnded = () => {
        stopRaf();
        setIsPlaying(false);
        isPlayingRef.current = false;
      };

      audio.addEventListener('loadedmetadata', handleLoadedMetadata);
      audio.addEventListener('ended', handleEnded);
      audioRef.current = audio;

      return () => {
        stopRaf();
        clearShadowingTimer();
        audio.removeEventListener('loadedmetadata', handleLoadedMetadata);
        audio.removeEventListener('ended', handleEnded);
        audio.pause();
      };
    } else {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.getVoices();
      }
      return () => {
        stopTts();
        clearShadowingTimer();
      };
    }
  }, [clearShadowingTimer, stopRaf, stopTts, syncActiveIndex, track]);

  const pause = useCallback(() => {
    clearShadowingTimer();
    setIsPlaying(false);
    isPlayingRef.current = false;
    if (engineMode === 'audio') {
      audioRef.current?.pause();
      stopRaf();
    } else {
      stopTts();
    }
  }, [clearShadowingTimer, engineMode, stopRaf, stopTts]);

  const seekToSegment = useCallback(
    (index: number, autoPlay = true) => {
      clearShadowingTimer();
      const safeIndex = Math.max(0, Math.min(index, track.segments.length - 1));
      syncActiveIndex(safeIndex);

      if (engineMode === 'audio') {
        const audio = audioRef.current;
        const targetSeg = track.segments[safeIndex];
        if (audio && targetSeg && targetSeg.startTime !== null) {
          audio.currentTime = targetSeg.startTime;
          setCurrentTime(targetSeg.startTime);
          if (autoPlay) {
            setIsPlaying(true);
            isPlayingRef.current = true;
            audio.play().then(startRafLoop).catch(() => {
              setIsPlaying(false);
              isPlayingRef.current = false;
            });
          }
        }
      } else {
        if (autoPlay) {
          setIsPlaying(true);
          isPlayingRef.current = true;
          speakSegmentByIndex(safeIndex);
        } else {
          stopTts();
          setIsPlaying(false);
          isPlayingRef.current = false;
        }
      }
    },
    [clearShadowingTimer, engineMode, speakSegmentByIndex, startRafLoop, stopTts, syncActiveIndex, track.segments]
  );

  const togglePlay = useCallback(() => {
    if (isPlayingRef.current) {
      pause();
    } else {
      setIsPlaying(true);
      isPlayingRef.current = true;
      if (engineMode === 'audio') {
        const audio = audioRef.current;
        if (audio) {
          audio.play().then(startRafLoop).catch(() => {
            setIsPlaying(false);
            isPlayingRef.current = false;
          });
        }
      } else {
        speakSegmentByIndex(activeIndexRef.current);
      }
    }
  }, [engineMode, pause, speakSegmentByIndex, startRafLoop]);

  const seekToTime = useCallback(
    (time: number) => {
      clearShadowingTimer();
      if (engineMode !== 'audio' || !audioRef.current) return;
      audioRef.current.currentTime = time;
      setCurrentTime(time);

      const matchedIdx = track.segments.findIndex(
        (seg) =>
          seg.startTime !== null &&
          seg.endTime !== null &&
          time >= seg.startTime &&
          time < seg.endTime
      );
      if (matchedIdx !== -1) {
        syncActiveIndex(matchedIdx);
      }
    },
    [clearShadowingTimer, engineMode, syncActiveIndex, track.segments]
  );

  const nextSegment = useCallback(() => {
    if (activeIndexRef.current + 1 < track.segments.length) {
      seekToSegment(activeIndexRef.current + 1, isPlayingRef.current);
    }
  }, [seekToSegment, track.segments.length]);

  const prevSegment = useCallback(() => {
    if (activeIndexRef.current - 1 >= 0) {
      seekToSegment(activeIndexRef.current - 1, isPlayingRef.current);
    }
  }, [seekToSegment]);

  const setPlaybackRate = useCallback(
    (rate: number) => {
      playbackRateRef.current = rate;
      setPlaybackRateState(rate);

      if (engineMode === 'audio' && audioRef.current) {
        audioRef.current.playbackRate = rate;
      } else if (engineMode === 'tts' && isPlayingRef.current) {
        speakSegmentByIndex(activeIndexRef.current);
      }
    },
    [engineMode, speakSegmentByIndex]
  );

  const toggleLoopSentence = useCallback(() => {
    setIsLoopingSentence((prev) => {
      const next = !prev;
      isLoopingRef.current = next;
      return next;
    });
  }, []);

  return {
    engineMode,
    isPlaying,
    isShadowingPause,
    activeSegmentIndex,
    currentTime,
    duration,
    playbackRate,
    isLoopingSentence,
    togglePlay,
    pause,
    seekToSegment,
    seekToTime,
    nextSegment,
    prevSegment,
    setPlaybackRate,
    toggleLoopSentence,
  };
}
