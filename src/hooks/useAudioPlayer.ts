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

import { md5 } from '../utils/md5';
import { BUNDLED_WORD_AUDIO } from '../data/bundledWordAudio';

// 德语母语发音缓存与并发音频控制
const wordAudioCache = new Map<string, string>();
let currentWordAudio: HTMLAudioElement | null = null;

const supportsOgg =
  typeof window !== 'undefined' &&
  typeof Audio !== 'undefined' &&
  Boolean(new Audio().canPlayType('audio/ogg'));

/**
 * 根据 MediaWiki / Wikimedia Commons 规范，利用 MD5 计算 OGG 原始发音文件的 MP3 转码衍生 URL。
 * 全面兼容 iOS Safari、iPadOS 及各类不支持原生 OGG 容器的移动端浏览器。
 */
function getWikimediaMp3Url(filename: string): string {
  const titleForHash = filename.replace(/ /g, '_');
  const hash = md5(titleForHash);
  const h1 = hash[0];
  const h2 = hash.substring(0, 2);
  return `https://upload.wikimedia.org/wikipedia/commons/transcoded/${h1}/${h2}/${encodeURIComponent(titleForHash)}/${encodeURIComponent(titleForHash)}.mp3`;
}

/**
 * 尝试在 Audio 实例中加载并播放指定音频地址
 */
function tryPlayAudioUrl(url: string, timeoutMs = 2500): Promise<boolean> {
  return new Promise((resolve) => {
    const audio = new Audio();
    currentWordAudio = audio;
    let finished = false;

    const cleanup = () => {
      audio.oncanplay = null;
      audio.onerror = null;
    };

    const timer = window.setTimeout(() => {
      if (!finished) {
        finished = true;
        cleanup();
        try {
          audio.pause();
          audio.src = '';
        } catch {
          // ignore
        }
        resolve(false);
      }
    }, timeoutMs);

    audio.oncanplay = async () => {
      if (!finished) {
        finished = true;
        window.clearTimeout(timer);
        cleanup();
        try {
          await audio.play();
          resolve(true);
        } catch {
          resolve(false);
        }
      }
    };

    audio.onerror = () => {
      if (!finished) {
        finished = true;
        window.clearTimeout(timer);
        cleanup();
        resolve(false);
      }
    };

    audio.src = url;
    audio.load();
  });
}

/**
 * 独立单词/词组即点即读：
 * 1. 优先使用本地同源预置的 800+ 核心词汇母语 MP3（零网络延时、iOS Safari 100% 畅播）
 * 2. 动态探测 Wiktionary / Wikimedia Commons 维基德语母语者 MP3 转码源（突破 iOS .ogg 限制）
 * 3. 动态备选高质量德语神经网络自然原声 MP3 接口（杜绝机械生硬的系统 TTS）
 * 4. 离线/全平台极端情况优雅降级至浏览器本地德语语音合成
 */
export async function speakGermanWord(wordText: string): Promise<'wiktionary' | 'tts'> {
  if (currentWordAudio) {
    try {
      currentWordAudio.pause();
      currentWordAudio.src = '';
    } catch {
      // ignore
    }
    currentWordAudio = null;
  }
  if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }

  // 提取核心词形（去除冠词 der/die/das/sich 及标点、语法注解）
  const clean = wordText
    .replace(/^(der|die|das|sich|den|dem|des|ein|eine)\s+/i, '')
    .replace(/\s*\(\+.*\)/g, '')
    .replace(/[.,!?;:()„“”"'/]/g, '')
    .trim();

  if (!clean) return 'tts';

  const lower = clean.toLowerCase();
  const capitalized = clean.charAt(0).toUpperCase() + clean.slice(1);
  const headword = clean.split(/\s+/)[0];
  const headwordLower = headword.toLowerCase();
  const headwordCapitalized = headword.charAt(0).toUpperCase() + headword.slice(1);

  // 1. 第一优先级：命中本地静态预置的 800+ 课程与核心生词 MP3（解决手机端网络延时及 WebKit 交互限制）
  const bundledUrl =
    BUNDLED_WORD_AUDIO[lower] ||
    BUNDLED_WORD_AUDIO[headwordLower] ||
    BUNDLED_WORD_AUDIO[clean] ||
    BUNDLED_WORD_AUDIO[headword];

  if (bundledUrl) {
    try {
      const audio = new Audio(bundledUrl);
      currentWordAudio = audio;
      await audio.play();
      return 'wiktionary';
    } catch {
      // 本地音频被浏览器拦截或异常时继续后备流程
    }
  }

  // 2. 第二优先级：命中运行时内存缓存
  const cachedUrl = wordAudioCache.get(lower) || wordAudioCache.get(clean);
  if (cachedUrl) {
    try {
      const audio = new Audio(cachedUrl);
      currentWordAudio = audio;
      await audio.play();
      return 'wiktionary';
    } catch {
      wordAudioCache.delete(lower);
      wordAudioCache.delete(clean);
    }
  }

  // 3. 第三优先级：动态构建母语原声候选地址序列（MP3 优先，确保 iOS Safari 与移动 Chrome 纯正原声）
  const candidateUrls: string[] = [];

  const wordVariants = Array.from(
    new Set([clean, capitalized, lower, headword, headwordCapitalized, headwordLower])
  ).filter(Boolean);

  // 3.1 维基共享资源 (Wikimedia Commons) 母语原声 MP3 转码流
  for (const variant of wordVariants) {
    candidateUrls.push(getWikimediaMp3Url(`De-${variant}.ogg`));
  }

  // 3.2 原生支持 OGG 的平台（如桌面端、Android Chrome）同时尝试原始 OGG
  if (supportsOgg) {
    for (const variant of wordVariants) {
      candidateUrls.push(
        `https://commons.wikimedia.org/wiki/Special:FilePath/De-${encodeURIComponent(variant)}.ogg`
      );
    }
  }

  // 3.3 高品质自然母语神经网络德语 MP3 流（用于罕见变形词/未收录短语，彻底消除机械发音）
  candidateUrls.push(
    `https://translate.google.com/translate_tts?ie=UTF-8&tl=de&client=tw-ob&q=${encodeURIComponent(clean)}`
  );
  if (headword !== clean) {
    candidateUrls.push(
      `https://translate.google.com/translate_tts?ie=UTF-8&tl=de&client=tw-ob&q=${encodeURIComponent(headword)}`
    );
  }

  for (const url of candidateUrls) {
    const ok = await tryPlayAudioUrl(url);
    if (ok) {
      wordAudioCache.set(lower, url);
      wordAudioCache.set(clean, url);
      return 'wiktionary';
    }
  }

  // 4. 第四优先级：极端无网离线降级至浏览器系统语音
  if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
    const utter = new SpeechSynthesisUtterance(clean);
    utter.lang = 'de-DE';
    utter.rate = 0.95;
    const voices = window.speechSynthesis.getVoices();
    const deVoice =
      voices.find(
        (v) =>
          v.lang.startsWith('de') &&
          (v.name.includes('Natural') ||
            v.name.includes('Online') ||
            v.name.includes('Google') ||
            v.name.includes('Premium') ||
            v.name.includes('Enhanced') ||
            v.name.includes('Siri') ||
            v.name.includes('Anna') ||
            v.name.includes('Helena'))
      ) ||
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
        if (audio && targetSeg) {
          const targetTime = targetSeg.startTime ?? 0;

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

          // 核心修复：audio.play() 必须直接在用户点击手势的同步调用栈中立即触发，
          // 切勿包裹在异步 loadedmetadata 回调内部，否则 iOS Safari 会判定手势失效并拒绝播放！
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
