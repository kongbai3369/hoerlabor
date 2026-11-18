import { useState, useEffect, useRef, useCallback } from 'react';
import type { ListeningTrack, EngineMode } from '../types/listening';
import { useListeningStore } from '../store/useListeningStore';
import { resolveAudioUrl } from '../utils/audioUrl';

export type PlaybackMode = 'single' | 'continuous';

export interface AudioPlayerControls {
  engineMode: EngineMode;
  isPlaying: boolean;
  isShadowingPause: boolean;
  activeSegmentIndex: number;
  currentTime: number;
  duration: number;
  playbackRate: number;
  isLoopingSentence: boolean;
  playbackMode: PlaybackMode;
  setPlaybackMode: (mode: PlaybackMode) => void;
  togglePlaybackMode: () => void;
  playSegment: (index: number, mode?: PlaybackMode) => void;
  togglePlay: () => void;
  pause: () => void;
  seekToSegment: (index: number, autoPlay?: boolean, mode?: PlaybackMode) => void;
  seekToTime: (time: number) => void;
  nextSegment: () => void;
  prevSegment: () => void;
  setPlaybackRate: (rate: number) => void;
  toggleLoopSentence: () => void;
}

import { BUNDLED_WORD_AUDIO } from '../data/bundledWordAudio';

// 德语母语发音缓存与单例并发音频控制 (全端统一使用 Edge-TTS Katja 高保真发音)
const wordAudioCache = new Map<string, string>();
let extraWordAudioMap: Record<string, string> | null = null;
let extraWordMapPromise: Promise<void> | null = null;
let sharedWordAudio: HTMLAudioElement | null = null;

function ensureExtraWordMapLoaded(): Promise<void> {
  if (extraWordAudioMap !== null) return Promise.resolve();
  if (extraWordMapPromise) return extraWordMapPromise;
  extraWordMapPromise = fetch('/data/wordAudioMap.json')
    .then((res) => (res.ok ? res.json() : {}))
    .then((data: unknown) => {
      extraWordAudioMap =
        data && typeof data === 'object' && !Array.isArray(data)
          ? (data as Record<string, string>)
          : {};
    })
    .catch(() => {
      extraWordAudioMap = {};
    });
  return extraWordMapPromise;
}

function getSharedWordAudio(): HTMLAudioElement {
  if (!sharedWordAudio && typeof Audio !== 'undefined') {
    sharedWordAudio = new Audio();
    sharedWordAudio.preload = 'auto';
  }
  return sharedWordAudio!;
}

// 移动端 Safari / WebKit 触控预热解锁（消除手势激活延迟与 Autoplay 拦截）
if (typeof window !== 'undefined') {
  const primeWordAudio = () => {
    try {
      const audio = getSharedWordAudio();
      if (audio && audio.paused && !audio.src) {
        audio.src = 'data:audio/wav;base64,UklGRigAAABXQVZFZm10IBIAAAABAAEARKwAAIhYAQACABAAAABkYXRhAgAAAAEA';
        audio.load();
      }
      void ensureExtraWordMapLoaded();
    } catch {
      // ignore
    }
  };
  window.addEventListener('touchstart', primeWordAudio, { passive: true, once: true });
  window.addEventListener('pointerdown', primeWordAudio, { passive: true, once: true });
}

function toAsciiSlug(word: string): string {
  return word
    .toLowerCase()
    .replace(/ä/g, 'ae')
    .replace(/ö/g, 'oe')
    .replace(/ü/g, 'ue')
    .replace(/ß/g, 'ss')
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '');
}

/**
 * 德语单词/核心词即点即读（全端统一使用微软 Edge-TTS Katja 高保真音色）：
 * 1. 优先从 BUNDLED_WORD_AUDIO 与异步 wordAudioMap 获取
 * 2. 尝试本地静态 /audio/words/{slug}.mp3 及外链 CDN 解析地址
 * 3. 若词库尚未收录，返回 'missing' 供界面友好提示，绝不静默误导或回退到机械合成音
 */
export async function speakGermanWord(wordText: string): Promise<'katja' | 'missing'> {
  await ensureExtraWordMapLoaded();

  const audio = getSharedWordAudio();
  if (audio) {
    try {
      audio.pause();
      audio.currentTime = 0;
    } catch {
      // ignore
    }
  }

  // 提取核心词形（去除冠词 der/die/das/sich 及标点、语法注解）
  const clean = wordText
    .replace(/^(der|die|das|sich|den|dem|des|ein|eine)\s+/i, '')
    .replace(/\s*\(\+.*\)/g, '')
    .replace(/[.,!?;:()„“”"'/]/g, '')
    .trim();

  if (!clean) return 'missing';

  const lower = clean.toLowerCase();
  const cached = wordAudioCache.get(lower);
  if (cached) {
    try {
      audio.src = cached;
      await audio.play();
      return 'katja';
    } catch {
      wordAudioCache.delete(lower);
    }
  }

  const slug = toAsciiSlug(lower);
  const headword = clean.split(/\s+/)[0];
  const headwordLower = headword.toLowerCase();
  const headwordSlug = toAsciiSlug(headwordLower);

  const mergedDict = extraWordAudioMap || {};
  const dictUrl =
    mergedDict[lower] ||
    mergedDict[slug] ||
    BUNDLED_WORD_AUDIO[lower] ||
    BUNDLED_WORD_AUDIO[clean] ||
    BUNDLED_WORD_AUDIO[headwordLower] ||
    BUNDLED_WORD_AUDIO[headword] ||
    BUNDLED_WORD_AUDIO[slug] ||
    BUNDLED_WORD_AUDIO[headwordSlug];

  const rawCandidates = [
    dictUrl,
    `/audio/words/${slug}.mp3`,
    `/audio/words/${headwordSlug}.mp3`,
  ].filter(Boolean) as string[];

  const candidateUrls: string[] = [];
  rawCandidates.forEach((raw) => {
    if (!candidateUrls.includes(raw)) candidateUrls.push(raw);
    const resolved = resolveAudioUrl(raw);
    if (resolved && !candidateUrls.includes(resolved)) candidateUrls.push(resolved);
  });

  for (const url of candidateUrls) {
    try {
      audio.src = url;
      const playPromise = audio.play();
      if (playPromise !== undefined) {
        await playPromise;
        wordAudioCache.set(lower, url);
        return 'katja';
      }
    } catch {
      // try next
    }
  }

  return 'missing';
}

export function useAudioPlayer(track: ListeningTrack): AudioPlayerControls {
  const engineMode: EngineMode = track.audioUrl ? 'audio' : 'tts';
  const { autoPauseSeconds, markTrackCompleted } = useListeningStore();

  const [isPlaying, setIsPlaying] = useState(false);
  const [isShadowingPause, setIsShadowingPause] = useState(false);
  const [activeSegmentIndex, setActiveSegmentIndex] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState<number>(track.duration ?? 0);
  const [playbackRate, setPlaybackRateState] = useState(1.0);
  const [isLoopingSentence, setIsLoopingSentence] = useState(false);
  const [playbackMode, setPlaybackMode] = useState<PlaybackMode>('single');
  const [prevTrackId, setPrevTrackId] = useState(track.id);

  const playbackModeRef = useRef<PlaybackMode>('single');
  const oneShotSingleRef = useRef(false);
  const isSeekingRef = useRef(false);

  useEffect(() => {
    playbackModeRef.current = playbackMode;
  }, [playbackMode]);

  const togglePlaybackMode = useCallback(() => {
    oneShotSingleRef.current = false;
    setPlaybackMode((prev) => (prev === 'single' ? 'continuous' : 'single'));
  }, []);

  if (prevTrackId !== track.id) {
    setPrevTrackId(track.id);
    setIsPlaying(false);
    setIsShadowingPause(false);
    setActiveSegmentIndex(0);
    setCurrentTime(0);
    setDuration(track.duration ?? 0);
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
      if (!audio || audio.paused || isSeekingRef.current) return;

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
        (playbackModeRef.current === 'single' || oneShotSingleRef.current) &&
        currentSeg &&
        currentSeg.endTime !== null &&
        now >= currentSeg.endTime - 0.02
      ) {
        // 单句精听或「播此句」单次点播：句尾立即硬暂停并复位至句首，不破坏用户的全局连播开关
        oneShotSingleRef.current = false;
        audio.pause();
        stopRaf();
        if (currentSeg.startTime !== null) {
          audio.currentTime = currentSeg.startTime;
          setCurrentTime(currentSeg.startTime);
        }
        if (activeIndexRef.current >= segments.length - 1) {
          markTrackCompleted(track.id);
        }
        setIsPlaying(false);
        isPlayingRef.current = false;
        return;
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
  }, [markTrackCompleted, stopRaf, syncActiveIndex, track.id, track.segments]);

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

        if (
          (playbackModeRef.current === 'single' || oneShotSingleRef.current) &&
          !isLoopingRef.current
        ) {
          oneShotSingleRef.current = false;
          if (index >= track.segments.length - 1) {
            markTrackCompleted(track.id);
          }
          setIsPlaying(false);
          isPlayingRef.current = false;
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
              markTrackCompleted(track.id);
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
    [markTrackCompleted, stopTts, syncActiveIndex, track.id, track.segments]
  );

  useEffect(() => {
    startRafLoopRef.current = startRafLoop;
    speakSegmentByIndexRef.current = speakSegmentByIndex;
  });

  useEffect(() => {
    stopRaf();
    stopTts();
    oneShotSingleRef.current = false;
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
      const finalUrl = resolveAudioUrl(track.audioUrl);
      const audio = new Audio(finalUrl);
      audio.preload = 'auto';
      // 移动端 WebKit 允许原生行内播放，避免全屏或被静音拦截
      // @ts-expect-error - playsInline is WebKit standard on iOS Safari
      audio.playsInline = true;
      audio.setAttribute('playsinline', 'true');
      audio.setAttribute('webkit-playsinline', 'true');
      audio.preservesPitch = true;
      audio.playbackRate = playbackRateRef.current;

      try {
        audio.load();
      } catch {
        // 部分测试环境可能没有 load 方法
      }

      const handleLoadedMetadata = () => {
        setDuration(audio.duration || track.duration || 0);
      };

      const handleEnded = () => {
        stopRaf();
        setIsPlaying(false);
        isPlayingRef.current = false;
        markTrackCompleted(track.id);
      };

      // 针对移动端 WebKit / iOS Safari 的首次触控预热解锁
      const unlockAudio = () => {
        if (audio.paused && audio.readyState === 0) {
          try {
            audio.load();
          } catch {}
        }
      };

      window.addEventListener('touchstart', unlockAudio, { passive: true, once: true });
      window.addEventListener('pointerdown', unlockAudio, { passive: true, once: true });

      audio.addEventListener('loadedmetadata', handleLoadedMetadata);
      audio.addEventListener('ended', handleEnded);
      audioRef.current = audio;

      return () => {
        stopRaf();
        clearShadowingTimer();
        window.removeEventListener('touchstart', unlockAudio);
        window.removeEventListener('pointerdown', unlockAudio);
        audio.removeEventListener('loadedmetadata', handleLoadedMetadata);
        audio.removeEventListener('ended', handleEnded);
        audio.pause();
      };
    } else {
      if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
        window.speechSynthesis.getVoices();
      }
      return () => {
        stopTts();
        clearShadowingTimer();
      };
    }
  }, [clearShadowingTimer, markTrackCompleted, stopRaf, stopTts, syncActiveIndex, track]);

  const pause = useCallback(() => {
    clearShadowingTimer();
    oneShotSingleRef.current = false;
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
    (index: number, autoPlay = true, mode?: PlaybackMode) => {
      if (track.segments.length === 0) return;
      oneShotSingleRef.current = mode === 'single';
      clearShadowingTimer();
      const safeIndex = Math.max(0, Math.min(index, track.segments.length - 1));
      syncActiveIndex(safeIndex);

      if (engineMode === 'audio') {
        const audio = audioRef.current;
        const targetSeg = track.segments[safeIndex];
        if (audio && targetSeg) {
          const targetTime = targetSeg.startTime ?? 0;
          isSeekingRef.current = true;
          stopRaf();

          const onSeekComplete = () => {
            isSeekingRef.current = false;
            audio.removeEventListener('seeked', onSeekComplete);
            if (isPlayingRef.current) {
              startRafLoop();
            }
          };
          audio.addEventListener('seeked', onSeekComplete, { once: true });
          // 兜底超时解锁
          window.setTimeout(() => {
            if (isSeekingRef.current) {
              isSeekingRef.current = false;
              if (isPlayingRef.current) startRafLoop();
            }
          }, 350);

          if (audio.readyState >= 1) {
            try {
              audio.currentTime = targetTime;
              setCurrentTime(targetTime);
            } catch {
              // 保护
            }
          } else {
            const onMetadata = () => {
              audio.removeEventListener('loadedmetadata', onMetadata);
              try {
                audio.currentTime = targetTime;
                setCurrentTime(targetTime);
              } catch {}
            };
            audio.addEventListener('loadedmetadata', onMetadata);
          }

          if (autoPlay) {
            setIsPlaying(true);
            isPlayingRef.current = true;
            const playPromise = audio.play();
            if (playPromise !== undefined) {
              playPromise.then(startRafLoop).catch((err) => {
                console.warn('Audio playback prevented on mobile gesture:', err);
                setIsPlaying(false);
                isPlayingRef.current = false;
              });
            }
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
    [clearShadowingTimer, engineMode, speakSegmentByIndex, startRafLoop, stopRaf, stopTts, syncActiveIndex, track.segments]
  );

  const playSegment = useCallback(
    (index: number, mode: PlaybackMode = 'single') => {
      seekToSegment(index, true, mode);
    },
    [seekToSegment]
  );

  const togglePlay = useCallback(() => {
    if (track.segments.length === 0) return;
    if (isPlayingRef.current) {
      pause();
    } else {
      oneShotSingleRef.current = false;
      setIsPlaying(true);
      isPlayingRef.current = true;
      if (engineMode === 'audio') {
        const audio = audioRef.current;
        if (audio) {
          const currentSeg = track.segments[activeIndexRef.current];
          if (
            currentSeg &&
            currentSeg.startTime !== null &&
            (audio.currentTime < currentSeg.startTime ||
              (currentSeg.endTime !== null && audio.currentTime >= currentSeg.endTime))
          ) {
            try {
              audio.currentTime = currentSeg.startTime;
              setCurrentTime(currentSeg.startTime);
            } catch {}
          }
          const playPromise = audio.play();
          if (playPromise !== undefined) {
            playPromise.then(startRafLoop).catch((err) => {
              console.warn('Audio playback prevented on mobile gesture:', err);
              setIsPlaying(false);
              isPlayingRef.current = false;
            });
          }
        }
      } else {
        speakSegmentByIndex(activeIndexRef.current);
      }
    }
  }, [engineMode, pause, speakSegmentByIndex, startRafLoop, track.segments]);

  const seekToTime = useCallback(
    (time: number) => {
      clearShadowingTimer();
      oneShotSingleRef.current = false;
      if (engineMode !== 'audio' || !audioRef.current) return;
      try {
        audioRef.current.currentTime = time;
        setCurrentTime(time);
      } catch {}

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

  // 注册系统级 Media Session 控制（支持手机锁屏界面与蓝牙耳机按键切句）
  useEffect(() => {
    if (typeof navigator === 'undefined' || !('mediaSession' in navigator)) return;
    try {
      navigator.mediaSession.metadata = new MediaMetadata({
        title: `${track.title} (第 ${activeSegmentIndex + 1}/${Math.max(track.segments.length, 1)} 句)`,
        artist: track.source,
        album: `${track.level} · ${track.topic}`,
      });
      navigator.mediaSession.playbackState = isPlaying ? 'playing' : 'paused';
      navigator.mediaSession.setActionHandler('play', () => {
        if (!isPlayingRef.current) togglePlay();
      });
      navigator.mediaSession.setActionHandler('pause', () => {
        if (isPlayingRef.current) pause();
      });
      navigator.mediaSession.setActionHandler('previoustrack', prevSegment);
      navigator.mediaSession.setActionHandler('nexttrack', nextSegment);
    } catch {
      // ignore unsupported handlers
    }
  }, [
    activeSegmentIndex,
    isPlaying,
    nextSegment,
    pause,
    prevSegment,
    togglePlay,
    track.level,
    track.segments.length,
    track.source,
    track.title,
    track.topic,
  ]);

  return {
    engineMode,
    isPlaying,
    isShadowingPause,
    activeSegmentIndex,
    currentTime,
    duration,
    playbackRate,
    isLoopingSentence,
    playbackMode,
    setPlaybackMode,
    togglePlaybackMode,
    playSegment,
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
