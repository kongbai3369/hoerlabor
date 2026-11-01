import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  Volume2,
  Eye,
  EyeOff,
  RotateCcw,
  CheckCircle2,
  Sparkles,
  Keyboard,
  Star,
  Mic,
  Radio,
  ExternalLink,
  PanelLeftClose,
  PanelLeftOpen,
  PanelRightClose,
  PanelRightOpen,
} from 'lucide-react';
import type { ListeningTrack, SentenceSegment } from '../types/listening';
import { type AudioPlayerControls, speakGermanWord } from '../hooks/useAudioPlayer';
import { useListeningStore } from '../store/useListeningStore';
import { LEVEL_BADGE_STYLE } from '../types/listening';

interface TranscriptViewProps {
  track: ListeningTrack;
  player: AudioPlayerControls;
  isSidebarOpen?: boolean;
  onToggleSidebar?: () => void;
  isVocabOpen?: boolean;
  onToggleVocab?: () => void;
}

const GERMAN_CHARS = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü'];

function isGermanWordMatch(input: string, target: string): boolean {
  const cleanInput = input.trim();
  if (!cleanInput) return false;
  if (cleanInput === target) return true;

  const normalizeUmlaut = (str: string) =>
    str
      .replace(/ä/g, 'ae')
      .replace(/ö/g, 'oe')
      .replace(/ü/g, 'ue')
      .replace(/Ä/g, 'Ae')
      .replace(/Ö/g, 'Oe')
      .replace(/Ü/g, 'Ue')
      .replace(/ß/g, 'ss');

  return normalizeUmlaut(cleanInput) === normalizeUmlaut(target);
}

export const TranscriptView: React.FC<TranscriptViewProps> = ({
  track,
  player,
  isSidebarOpen = true,
  onToggleSidebar,
  isVocabOpen = true,
  onToggleVocab,
}) => {
  const {
    displayMode,
    dictationInputs,
    starredSegmentIds,
    toggleStarSegment,
    setDictationInput,
    clearTrackDictation,
  } = useListeningStore();

  const [peekedSegments, setPeekedSegments] = useState<Record<string, boolean>>({});
  const [showAnswerHints, setShowAnswerHints] = useState(false);
  const [onlyStarred, setOnlyStarred] = useState(false);
  const [focusedInputKey, setFocusedInputKey] = useState<string | null>(null);

  const segmentRefs = useRef<Record<number, HTMLDivElement | null>>({});
  const inputRefs = useRef<Record<string, HTMLInputElement | null>>({});

  useEffect(() => {
    const activeEl = segmentRefs.current[player.activeSegmentIndex];
    if (activeEl) {
      activeEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, [player.activeSegmentIndex, track.id]);

  const togglePeekSegment = (segId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setPeekedSegments((prev) => ({ ...prev, [segId]: !prev[segId] }));
  };

  const handleInsertGermanChar = (char: string) => {
    if (!focusedInputKey) return;
    const currentVal = dictationInputs[focusedInputKey] || '';
    setDictationInput(focusedInputKey, currentVal + char);
    const inputEl = inputRefs.current[focusedInputKey];
    if (inputEl) inputEl.focus();
  };

  const allBlankKeys = useMemo(() => {
    const keys: string[] = [];
    track.segments.forEach((seg) => {
      const tokens = seg.german.split(/([A-Za-zÄÖÜäöüß]+)/g);
      tokens.forEach((token, tokenIdx) => {
        if (seg.clozeWords.includes(token)) {
          keys.push(`${track.id}:${seg.id}:${tokenIdx}`);
        }
      });
    });
    return keys;
  }, [track]);

  const handleKeyDownCloze = (
    currentKey: string,
    e: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      const currIndex = allBlankKeys.indexOf(currentKey);
      if (currIndex !== -1 && currIndex + 1 < allBlankKeys.length) {
        const nextKey = allBlankKeys[currIndex + 1];
        inputRefs.current[nextKey]?.focus();
      }
    }
  };

  const calculateDictationStats = () => {
    let totalBlanks = 0;
    let correctBlanks = 0;

    track.segments.forEach((seg) => {
      const tokens = seg.german.split(/([A-Za-zÄÖÜäöüß]+)/g);
      tokens.forEach((token, tokenIdx) => {
        if (seg.clozeWords.includes(token)) {
          totalBlanks += 1;
          const key = `${track.id}:${seg.id}:${tokenIdx}`;
          const val = dictationInputs[key] || '';
          if (isGermanWordMatch(val, token)) {
            correctBlanks += 1;
          }
        }
      });
    });

    return { totalBlanks, correctBlanks };
  };

  const { totalBlanks, correctBlanks } = calculateDictationStats();
  const trackStarredCount = track.segments.filter((s) =>
    starredSegmentIds.includes(s.id)
  ).length;

  const renderGermanSentence = (seg: SentenceSegment, isActive: boolean) => {
    const tokens = seg.german.split(/([A-Za-zÄÖÜäöüß]+)/g);

    if (displayMode !== 'dictation') {
      return (
        <p
          className={`text-xl font-medium leading-[1.8] tracking-normal transition-colors ${
            isActive ? 'text-slate-900 font-semibold' : 'text-slate-700'
          }`}
        >
          {tokens.map((token, idx) => {
            const isWord = /^[A-Za-zÄÖÜäöüß]+$/.test(token);
            const isKeyword = seg.clozeWords.includes(token);

            if (!isWord) {
              return <React.Fragment key={idx}>{token}</React.Fragment>;
            }

            return (
              <span
                key={idx}
                onClick={(e) => {
                  e.stopPropagation();
                  speakGermanWord(token);
                }}
                title={`点击单独听维基母语真人发音 (Wiktionary): ${token}`}
                className={`rounded-md px-1 py-0.5 transition-all hover:bg-indigo-100/90 hover:text-indigo-900 cursor-pointer ${
                  isKeyword
                    ? 'underline decoration-indigo-400 decoration-2 underline-offset-4 text-indigo-950 font-bold'
                    : ''
                }`}
              >
                {token}
              </span>
            );
          })}
        </p>
      );
    }

    return (
      <div className="text-xl font-medium leading-loose text-slate-800 flex flex-wrap items-baseline gap-y-2">
        {tokens.map((token, tokenIdx) => {
          if (!seg.clozeWords.includes(token)) {
            return (
              <span key={tokenIdx} className="whitespace-pre-wrap">
                {token}
              </span>
            );
          }

          const inputKey = `${track.id}:${seg.id}:${tokenIdx}`;
          const userVal = dictationInputs[inputKey] || '';
          const isCorrect = isGermanWordMatch(userVal, token);
          const widthCh = Math.max(token.length + 3, 8);

          return (
            <span
              key={tokenIdx}
              onClick={(e) => e.stopPropagation()}
              className="inline-flex flex-col items-center mx-1 align-baseline"
            >
              <span className="relative inline-flex items-center">
                <input
                  ref={(el) => {
                    inputRefs.current[inputKey] = el;
                  }}
                  type="text"
                  value={userVal}
                  onFocus={() => setFocusedInputKey(inputKey)}
                  onChange={(e) => setDictationInput(inputKey, e.target.value)}
                  onKeyDown={(e) => handleKeyDownCloze(inputKey, e)}
                  placeholder={'_'.repeat(token.length)}
                  style={{ width: `${widthCh}ch` }}
                  className={`px-2.5 py-1 text-base font-mono rounded-lg border outline-none transition-all text-center shadow-xs ${
                    isCorrect
                      ? 'bg-emerald-50 border-emerald-500 text-emerald-800 font-bold ring-1 ring-emerald-500/20'
                      : userVal.length > 0
                      ? 'bg-amber-50 border-amber-400 text-amber-900 font-medium'
                      : 'bg-white border-slate-300 text-slate-900 focus:border-indigo-600 focus:ring-2 focus:ring-indigo-500/20'
                  }`}
                />
                {isCorrect && (
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 ml-1 shrink-0" />
                )}
              </span>
              {showAnswerHints && !isCorrect && (
                <span className="text-xs text-amber-700 font-mono mt-1 font-semibold">
                  答案: {token}
                </span>
              )}
            </span>
          );
        })}
      </div>
    );
  };

  return (
    <main className="flex-1 flex flex-col h-full bg-slate-50/50 overflow-hidden relative">
      <header className="px-5 py-3.5 border-b border-slate-200/80 bg-white/95 backdrop-blur-md flex flex-wrap items-center justify-between gap-3 shrink-0 shadow-xs z-10">
        <div className="flex items-center gap-3">
          {onToggleSidebar && (
            <button
              onClick={onToggleSidebar}
              title={isSidebarOpen ? '收起曲库侧栏' : '展开曲库侧栏'}
              className="hidden lg:flex p-1.5 rounded-lg text-slate-500 hover:text-slate-800 hover:bg-slate-100 border border-slate-200/70 transition cursor-pointer shadow-2xs"
            >
              {isSidebarOpen ? (
                <PanelLeftClose className="w-4 h-4" />
              ) : (
                <PanelLeftOpen className="w-4 h-4" />
              )}
            </button>
          )}

          <div>
            <div className="flex items-center gap-2 mb-1 flex-wrap">
              <span
                className={`px-2.5 py-0.5 text-xs font-bold rounded-md border shadow-2xs ${
                  LEVEL_BADGE_STYLE[track.level]
                }`}
              >
                {track.level}
              </span>
              <span className="text-xs text-slate-500 font-medium">{track.source}</span>
              <span className="text-slate-300">·</span>
              <span className="text-xs text-indigo-600 font-semibold">{track.topic}</span>
              {track.originalAudioUrl && (
                <>
                  <span className="text-slate-300">·</span>
                  <a
                    href={track.originalAudioUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-[11px] text-emerald-700 hover:text-emerald-800 bg-emerald-50 border border-emerald-200 px-2.5 py-0.5 rounded-full transition font-medium shadow-2xs"
                    title="在新窗口直接打开/收听官方原版完整音频"
                  >
                    <Radio className="w-3 h-3 text-emerald-600" />
                    <span>官方原声广播直链</span>
                    <ExternalLink className="w-2.5 h-2.5 opacity-70" />
                  </a>
                </>
              )}
            </div>
            <h2 className="text-base md:text-lg font-bold text-slate-900 tracking-tight">
              {track.title}
            </h2>
          </div>
        </div>

        <div className="flex items-center gap-2.5 flex-wrap">
          {/* 星标难句筛选按钮 */}
          <button
            onClick={() => setOnlyStarred((prev) => !prev)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium inline-flex items-center gap-1.5 border transition cursor-pointer ${
              onlyStarred
                ? 'bg-amber-50 border-amber-300 text-amber-800 shadow-xs font-semibold'
                : 'bg-white border-slate-200 text-slate-600 hover:text-slate-900 hover:bg-slate-50 shadow-2xs'
            }`}
          >
            <Star
              className="w-3.5 h-3.5 text-amber-500"
              fill={onlyStarred ? 'currentColor' : 'none'}
            />
            <span>难句本 ({trackStarredCount})</span>
          </button>

          {displayMode === 'dictation' && (
            <div className="flex items-center gap-2 bg-slate-100/90 border border-slate-200 px-3 py-1.5 rounded-xl shadow-2xs">
              <div className="flex items-center gap-1 border-r border-slate-200/80 pr-2">
                <Keyboard className="w-3.5 h-3.5 text-slate-400 mr-1 hidden sm:inline" />
                {GERMAN_CHARS.map((ch) => (
                  <button
                    key={ch}
                    type="button"
                    onMouseDown={(e) => {
                      e.preventDefault();
                      handleInsertGermanChar(ch);
                    }}
                    className="w-6 h-6 rounded bg-white hover:bg-indigo-600 hover:text-white border border-slate-200 text-slate-700 text-xs font-mono font-semibold transition cursor-pointer shadow-2xs active:scale-95"
                  >
                    {ch}
                  </button>
                ))}
              </div>

              <div className="text-xs text-slate-600 font-medium">
                <span className="font-bold text-emerald-600">
                  {correctBlanks}/{totalBlanks}
                </span>
              </div>

              <button
                onClick={() => setShowAnswerHints((prev) => !prev)}
                className="px-2 py-0.5 rounded bg-white border border-slate-200 hover:bg-slate-50 text-xs text-amber-700 font-semibold transition cursor-pointer shadow-2xs"
              >
                {showAnswerHints ? '隐藏' : '答案'}
              </button>

              <button
                onClick={() => clearTrackDictation(track.id)}
                title="清空本篇听写记录"
                className="p-1 rounded bg-white border border-slate-200 hover:bg-rose-50 hover:text-rose-600 hover:border-rose-200 text-slate-500 transition cursor-pointer shadow-2xs"
              >
                <RotateCcw className="w-3.5 h-3.5" />
              </button>
            </div>
          )}

          {onToggleVocab && (
            <button
              onClick={onToggleVocab}
              title={isVocabOpen ? '收起生词抽屉' : '展开生词抽屉'}
              className="hidden lg:flex p-1.5 rounded-lg text-slate-500 hover:text-slate-800 hover:bg-slate-100 border border-slate-200/70 transition cursor-pointer shadow-2xs"
            >
              {isVocabOpen ? (
                <PanelRightClose className="w-4 h-4" />
              ) : (
                <PanelRightOpen className="w-4 h-4" />
              )}
            </button>
          )}
        </div>
      </header>

      {/* 句子卡片流：留足 pb-36 md:pb-40 确保末句绝不被悬浮播放胶囊遮挡 */}
      <div className="flex-1 overflow-y-auto px-4 md:px-8 py-6 pb-36 md:pb-40 space-y-4">
        {track.segments.map((seg, idx) => {
          const isStarred = starredSegmentIds.includes(seg.id);
          if (onlyStarred && !isStarred) return null;

          const isActive = idx === player.activeSegmentIndex;
          const isBlind = displayMode === 'blind' && !peekedSegments[seg.id];

          return (
            <div
              key={seg.id}
              ref={(el) => {
                segmentRefs.current[idx] = el;
              }}
              onClick={() => player.seekToSegment(idx, true)}
              className={`group relative rounded-2xl p-5 md:p-6 transition-all duration-200 cursor-pointer overflow-hidden ${
                isActive
                  ? 'bg-white border border-indigo-200/90 shadow-[0_8px_24px_-4px_rgba(79,70,229,0.12),0_2px_6px_-1px_rgba(79,70,229,0.08)] ring-1 ring-indigo-500/15'
                  : 'bg-white/85 hover:bg-white border border-slate-200/80 hover:border-indigo-200/70 shadow-[0_1px_3px_rgba(0,0,0,0.02)] hover:shadow-sm'
              }`}
            >
              {/* 激活句专有圆润普鲁士蓝垂直导轨 */}
              {isActive && (
                <div className="absolute left-0 top-3 bottom-3 w-1.5 bg-gradient-to-b from-indigo-500 to-indigo-700 rounded-r-full shadow-sm shadow-indigo-500/30" />
              )}

              <div className="flex items-center justify-between mb-2.5">
                <div className="flex items-center gap-2.5">
                  <span
                    className={`w-6 h-6 rounded-full text-xs font-bold flex items-center justify-center transition-colors ${
                      isActive
                        ? 'bg-indigo-600 text-white shadow-xs ring-2 ring-indigo-100'
                        : 'bg-slate-100 text-slate-500 group-hover:bg-slate-200 group-hover:text-slate-700'
                    }`}
                  >
                    {idx + 1}
                  </span>

                  {isActive && !player.isShadowingPause && (
                    <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-indigo-700 bg-indigo-50/90 px-2.5 py-0.5 rounded-full border border-indigo-200/70 shadow-2xs">
                      <Volume2 className="w-3.5 h-3.5 animate-pulse text-indigo-600" />
                      <span>
                        {player.isLoopingSentence ? '单句循环精听中' : '当前朗读句 · 点击单词可单读'}
                      </span>
                    </span>
                  )}

                  {isActive && player.isShadowingPause && (
                    <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200 shadow-2xs">
                      <Mic className="w-3.5 h-3.5 animate-bounce text-emerald-600" />
                      <span>请开口跟读复述...</span>
                    </span>
                  )}
                </div>

                <div className="flex items-center gap-2">
                  {displayMode === 'blind' && (
                    <button
                      onClick={(e) => togglePeekSegment(seg.id, e)}
                      className="inline-flex items-center gap-1 text-xs px-2.5 py-1 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200 font-medium transition cursor-pointer shadow-2xs"
                    >
                      {peekedSegments[seg.id] ? (
                        <>
                          <EyeOff className="w-3.5 h-3.5 text-slate-600" />
                          <span>遮罩</span>
                        </>
                      ) : (
                        <>
                          <Eye className="w-3.5 h-3.5 text-slate-600" />
                          <span>核对</span>
                        </>
                      )}
                    </button>
                  )}

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      toggleStarSegment(seg.id);
                    }}
                    title={isStarred ? '取消难句星标' : '标记为重点难句'}
                    className={`p-1.5 rounded-lg transition cursor-pointer ${
                      isStarred
                        ? 'text-amber-500 bg-amber-50 hover:bg-amber-100 shadow-2xs'
                        : 'text-slate-400 hover:text-amber-500 hover:bg-slate-100'
                    }`}
                  >
                    <Star
                      className="w-4 h-4"
                      fill={isStarred ? 'currentColor' : 'none'}
                    />
                  </button>
                </div>
              </div>

              <div
                className={`transition-all duration-200 ${
                  isBlind ? 'blur-md select-none opacity-50' : ''
                }`}
              >
                {renderGermanSentence(seg, isActive)}

                {(displayMode === 'bilingual' ||
                  (displayMode === 'blind' && peekedSegments[seg.id]) ||
                  displayMode === 'dictation') && (
                  <p className="mt-3 text-sm text-slate-600 leading-relaxed font-normal">
                    {seg.chinese}
                  </p>
                )}
              </div>

              {isBlind && (
                <div className="mt-3 inline-flex items-center justify-between gap-3 text-xs text-amber-800 bg-amber-50/90 px-3 py-1.5 rounded-xl border border-amber-200/80 font-medium w-full sm:w-auto shadow-2xs">
                  <div className="flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-amber-600 shrink-0" />
                    <span>盲听训练中：点击卡片可重新听句</span>
                  </div>
                  <button
                    onClick={(e) => togglePeekSegment(seg.id, e)}
                    className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-white hover:bg-amber-100 text-amber-900 border border-amber-300 font-semibold transition cursor-pointer text-[11px] shadow-2xs"
                  >
                    <Eye className="w-3 h-3 text-amber-700" />
                    <span>核对原文</span>
                  </button>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </main>
  );
};
