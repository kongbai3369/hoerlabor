import React, { useState, useEffect, useRef } from 'react';
import {
  Play,
  Pause,
  SkipBack,
  SkipForward,
  Repeat,
  EyeOff,
  FileText,
  Languages,
  PenTool,
  Sparkles,
  Radio,
  Timer,
  ChevronUp,
  ChevronDown,
  ExternalLink,
} from 'lucide-react';
import type { DisplayMode, ListeningTrack } from '../types/listening';
import { LEVEL_BADGE_STYLE } from '../types/listening';
import type { AudioPlayerControls } from '../hooks/useAudioPlayer';
import { useListeningStore } from '../store/useListeningStore';

interface PlayerBarProps {
  track: ListeningTrack;
  player: AudioPlayerControls;
}

const SPEED_OPTIONS = [0.8, 0.9, 1.0, 1.2, 1.5];
const PAUSE_OPTIONS = [0, 2, 4];

const MODE_OPTIONS: Array<{
  mode: DisplayMode;
  label: string;
  icon: React.FC<{ className?: string }>;
}> = [
  { mode: 'blind', label: '盲听', icon: EyeOff },
  { mode: 'de_only', label: '纯德', icon: FileText },
  { mode: 'bilingual', label: '中德', icon: Languages },
  { mode: 'dictation', label: '听写', icon: PenTool },
];

function formatSeconds(sec: number): string {
  if (!Number.isFinite(sec) || sec < 0) return '00:00';
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

export const PlayerBar: React.FC<PlayerBarProps> = ({ track, player }) => {
  const { displayMode, setDisplayMode, autoPauseSeconds, setAutoPauseSeconds } =
    useListeningStore();
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const totalSegments = track.segments.length;

  const cycleAutoPause = () => {
    const nextIdx = (PAUSE_OPTIONS.indexOf(autoPauseSeconds) + 1) % PAUSE_OPTIONS.length;
    setAutoPauseSeconds(PAUSE_OPTIONS[nextIdx]);
  };

  const progressPercent =
    player.duration > 0
      ? Math.min(100, Math.max(0, (player.currentTime / player.duration) * 100))
      : ((player.activeSegmentIndex + 1) / totalSegments) * 100;

  const touchStartY = useRef<number | null>(null);

  const handleTouchStart = (e: React.TouchEvent) => {
    touchStartY.current = e.touches[0].clientY;
  };

  const handleTouchEnd = (e: React.TouchEvent) => {
    if (touchStartY.current === null) return;
    const deltaY = e.changedTouches[0].clientY - touchStartY.current;
    if (deltaY > 60) {
      setIsDrawerOpen(false);
    }
    touchStartY.current = null;
  };

  useEffect(() => {
    if (!isDrawerOpen) return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setIsDrawerOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isDrawerOpen]);

  return (
    <>
      {/* ============================================================ */}
      {/* 桌面端精美悬浮胶囊播放器 (仅在 lg 及以上屏幕显示) */}
      {/* ============================================================ */}
      <footer className="hidden lg:flex fixed bottom-5 left-1/2 -translate-x-1/2 w-[94%] max-w-5xl bg-white/95 backdrop-blur-md shadow-[0_12px_40px_-8px_rgba(15,23,42,0.15),0_4px_12px_-2px_rgba(15,23,42,0.06)] rounded-2xl border border-slate-200/90 z-40 px-6 py-3 select-none items-center justify-between gap-4">
        {/* 左侧进度区 */}
        <div className="w-64 lg:w-72 flex flex-col justify-center gap-1.5 shrink-0">
          <div className="flex items-center justify-between text-xs">
            <span className="inline-flex items-center gap-1.5 font-medium text-slate-700 truncate">
              {player.engineMode === 'tts' ? (
                <>
                  <Sparkles className="w-3.5 h-3.5 text-amber-500 shrink-0" />
                  <span className="font-semibold text-slate-800">TTS 逐句驱动</span>
                </>
              ) : (
                <>
                  <Radio className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                  <span className="font-semibold text-slate-800">MP3 60fps 原声</span>
                  {track.originalAudioUrl && (
                    <a
                      href={track.originalAudioUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center text-[10px] text-emerald-700 hover:text-emerald-800 underline decoration-dotted ml-1 font-medium"
                      title="收听官方原版完整音频"
                    >
                      广播直链
                    </a>
                  )}
                </>
              )}
            </span>

            {player.engineMode === 'tts' ? (
              <span className="text-indigo-600 font-bold text-xs shrink-0">
                第 {player.activeSegmentIndex + 1} / {totalSegments} 句
              </span>
            ) : (
              <span className="text-slate-600 font-mono font-semibold text-xs shrink-0">
                {formatSeconds(player.currentTime)} / {formatSeconds(player.duration)}
              </span>
            )}
          </div>

          {player.engineMode === 'tts' ? (
            <div className="flex items-center gap-1 sm:gap-1.5 py-0.5">
              {track.segments.map((seg, idx) => {
                const isCurrent = idx === player.activeSegmentIndex;
                const isPassed = idx < player.activeSegmentIndex;
                return (
                  <button
                    key={seg.id}
                    onClick={() => player.seekToSegment(idx, true)}
                    title={`跳至第 ${idx + 1} 句`}
                    className={`h-2 flex-1 rounded-full transition-all cursor-pointer ${
                      isCurrent
                        ? 'bg-indigo-600 ring-2 ring-indigo-400/50 shadow-xs'
                        : isPassed
                        ? 'bg-indigo-200 hover:bg-indigo-300'
                        : 'bg-slate-200 hover:bg-slate-300'
                    }`}
                  />
                );
              })}
            </div>
          ) : (
            <input
              type="range"
              min={0}
              max={player.duration || 100}
              step={0.05}
              value={player.currentTime}
              onChange={(e) => player.seekToTime(parseFloat(e.target.value))}
              className="w-full h-1.5 rounded-lg cursor-pointer"
            />
          )}
        </div>

        {/* 中部播放与复读控制 */}
        <div className="flex items-center gap-2">
          <button
            onClick={player.prevSegment}
            disabled={player.activeSegmentIndex <= 0}
            title="上一句 (←)"
            className="p-2 rounded-xl bg-slate-100 text-slate-700 hover:bg-slate-200 hover:text-slate-900 disabled:opacity-35 transition cursor-pointer border border-slate-200/60 shadow-2xs active:scale-95"
          >
            <SkipBack className="w-4 h-4" />
          </button>

          <button
            onClick={player.togglePlay}
            title="播放 / 暂停 (Space)"
            className="w-11 h-11 rounded-full bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-500 hover:to-indigo-600 text-white flex items-center justify-center shadow-lg shadow-indigo-600/30 transition-all cursor-pointer active:scale-95"
          >
            {player.isPlaying ? (
              <Pause className="w-5 h-5" />
            ) : (
              <Play className="w-5 h-5 ml-0.5" />
            )}
          </button>

          <button
            onClick={player.nextSegment}
            disabled={player.activeSegmentIndex >= totalSegments - 1}
            title="下一句 (→)"
            className="p-2 rounded-xl bg-slate-100 text-slate-700 hover:bg-slate-200 hover:text-slate-900 disabled:opacity-35 transition cursor-pointer border border-slate-200/60 shadow-2xs active:scale-95"
          >
            <SkipForward className="w-4 h-4" />
          </button>

          <button
            onClick={player.toggleLoopSentence}
            title="单句无限循环 (快捷键: L)"
            className={`px-2.5 py-1.5 rounded-xl text-xs font-medium inline-flex items-center gap-1 border transition cursor-pointer shadow-2xs active:scale-95 ${
              player.isLoopingSentence
                ? 'bg-amber-50 border-amber-300 text-amber-800 shadow-xs font-bold'
                : 'bg-slate-100 border-slate-200 text-slate-600 hover:bg-slate-200 hover:text-slate-900'
            }`}
          >
            <Repeat className="w-3.5 h-3.5" />
            <span>单句循环</span>
          </button>

          <button
            onClick={cycleAutoPause}
            title="切换句间留白停顿秒数（0s / 2s / 4s）"
            className={`px-2.5 py-1.5 rounded-xl text-xs font-medium inline-flex items-center gap-1 border transition cursor-pointer shadow-2xs active:scale-95 ${
              autoPauseSeconds > 0
                ? 'bg-emerald-50 border-emerald-300 text-emerald-800 shadow-xs font-bold'
                : 'bg-slate-100 border-slate-200 text-slate-600 hover:bg-slate-200 hover:text-slate-900'
            }`}
          >
            <Timer className="w-3.5 h-3.5" />
            <span>{autoPauseSeconds > 0 ? `跟读停 ${autoPauseSeconds}s` : '连播无停顿'}</span>
          </button>
        </div>

        {/* 右侧倍速与四态模式 */}
        <div className="flex items-center gap-2 flex-wrap justify-end">
          <div className="flex items-center bg-slate-100/90 p-1 rounded-xl border border-slate-200/80 shadow-2xs">
            {SPEED_OPTIONS.map((rate) => {
              const active = Math.abs(player.playbackRate - rate) < 0.01;
              return (
                <button
                  key={rate}
                  onClick={() => player.setPlaybackRate(rate)}
                  className={`px-2 py-1 rounded-lg text-xs font-mono transition cursor-pointer ${
                    active
                      ? 'bg-indigo-600 text-white font-bold shadow-xs'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
                  }`}
                >
                  {rate}x
                </button>
              );
            })}
          </div>

          <div className="flex items-center bg-slate-100/90 p-1 rounded-xl border border-slate-200/80 shadow-2xs">
            {MODE_OPTIONS.map(({ mode, label, icon: Icon }) => {
              const active = displayMode === mode;
              return (
                <button
                  key={mode}
                  onClick={() => setDisplayMode(mode)}
                  className={`px-2.5 py-1 rounded-lg text-xs font-medium inline-flex items-center gap-1 transition cursor-pointer ${
                    active
                      ? 'bg-indigo-600 text-white shadow-xs font-bold'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </footer>

      {/* ============================================================ */}
      {/* 移动端紧凑型 56px 迷你播放条 (粘附于移动端底部导航栏上方) */}
      {/* ============================================================ */}
      <div className="lg:hidden fixed bottom-[calc(3.5rem+env(safe-area-inset-bottom,0px))] left-0 right-0 h-14 bg-white/95 backdrop-blur-md border-t border-slate-200/90 shadow-[0_-2px_12px_rgba(15,23,42,0.06)] z-30 select-none">
        {/* 顶部超细进度线 */}
        <div className="absolute top-0 left-0 right-0 h-[2.5px] bg-slate-100 overflow-hidden">
          <div
            className="h-full bg-indigo-600 transition-[width] duration-75 ease-linear"
            style={{ width: `${progressPercent}%` }}
          />
        </div>

        {/* 主内容区域 */}
        <div className="h-full px-3 flex items-center justify-between gap-2">
          {/* 点击左中信息区弹出抽屉面板 */}
          <button
            onClick={() => setIsDrawerOpen(true)}
            className="flex-1 flex items-center gap-2.5 min-w-0 text-left cursor-pointer group py-1"
          >
            <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-indigo-50 text-indigo-700 border border-indigo-200/70 shrink-0">
              {player.activeSegmentIndex + 1}/{totalSegments}
            </span>

            <div className="min-w-0 flex-1">
              <p className="text-xs font-bold text-slate-800 truncate leading-tight">
                {track.title}
              </p>
              <p className="text-[10px] text-slate-500 font-medium truncate flex items-center gap-1 mt-0.5">
                <span className="text-indigo-600 font-semibold">{track.level}</span>
                <span>·</span>
                <span>
                  {player.engineMode === 'audio'
                    ? `${formatSeconds(player.currentTime)} / ${formatSeconds(player.duration)}`
                    : `第 ${player.activeSegmentIndex + 1} 句`}
                </span>
                {player.isLoopingSentence && (
                  <span className="text-amber-600 font-bold">· 循环</span>
                )}
                {autoPauseSeconds > 0 && (
                  <span className="text-emerald-600 font-bold">· 停{autoPauseSeconds}s</span>
                )}
              </p>
            </div>

            <ChevronUp className="w-4 h-4 text-slate-400 group-hover:text-indigo-600 shrink-0 transition" />
          </button>

          {/* 右侧快捷播放控制 */}
          <div className="flex items-center gap-1 shrink-0">
            <button
              onClick={player.prevSegment}
              disabled={player.activeSegmentIndex <= 0}
              aria-label="上一句"
              className="p-1.5 rounded-lg text-slate-600 hover:text-slate-900 disabled:opacity-30 active:scale-95 transition cursor-pointer"
            >
              <SkipBack className="w-4 h-4" />
            </button>

            <button
              onClick={player.togglePlay}
              aria-label={player.isPlaying ? '暂停' : '播放'}
              className="w-9 h-9 rounded-full bg-gradient-to-r from-indigo-600 to-indigo-700 text-white flex items-center justify-center shadow-sm shadow-indigo-600/30 active:scale-95 transition cursor-pointer"
            >
              {player.isPlaying ? (
                <Pause className="w-4 h-4" />
              ) : (
                <Play className="w-4 h-4 ml-0.5" />
              )}
            </button>

            <button
              onClick={player.nextSegment}
              disabled={player.activeSegmentIndex >= totalSegments - 1}
              aria-label="下一句"
              className="p-1.5 rounded-lg text-slate-600 hover:text-slate-900 disabled:opacity-30 active:scale-95 transition cursor-pointer"
            >
              <SkipForward className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* ============================================================ */}
      {/* 移动端 iOS 风格上滑控制抽屉 (Bottom Sheet Drawer) */}
      {/* ============================================================ */}
      {isDrawerOpen && (
        <>
          {/* 半透明遮罩层 */}
          <div
            className="lg:hidden fixed inset-0 bg-slate-900/60 backdrop-blur-xs z-50 transition-opacity animate-fade-in"
            onClick={() => setIsDrawerOpen(false)}
          />

          {/* 上滑抽屉面板 */}
          <div
            onTouchStart={handleTouchStart}
            onTouchEnd={handleTouchEnd}
            className="lg:hidden fixed inset-x-0 bottom-0 max-h-[85vh] bg-white rounded-t-3xl shadow-2xl z-50 border-t border-slate-200/90 flex flex-col p-5 pb-[calc(2rem+env(safe-area-inset-bottom,0px))] overflow-y-auto animate-slide-up select-none"
          >
            {/* 顶部居中下推把手条 */}
            <div
              className="w-12 h-1.5 bg-slate-300 hover:bg-slate-400 rounded-full mx-auto mb-4 cursor-pointer transition"
              onClick={() => setIsDrawerOpen(false)}
            />

            {/* 曲目头部信息 */}
            <div className="flex items-start justify-between gap-3 mb-4 pb-3 border-b border-slate-100">
              <div className="min-w-0">
                <div className="flex items-center gap-2 mb-1 flex-wrap">
                  <span
                    className={`px-2 py-0.5 text-[11px] font-bold rounded-md border ${
                      LEVEL_BADGE_STYLE[track.level]
                    }`}
                  >
                    {track.level}
                  </span>
                  <span className="text-xs text-slate-500 font-medium truncate">
                    {track.source}
                  </span>
                  <span className="text-slate-300">·</span>
                  <span className="text-xs text-indigo-600 font-semibold">{track.topic}</span>
                  {track.originalAudioUrl && (
                    <a
                      href={track.originalAudioUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-[10px] text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full font-medium"
                    >
                      <Radio className="w-3 h-3 text-emerald-600" />
                      <span>官方原声</span>
                      <ExternalLink className="w-2.5 h-2.5" />
                    </a>
                  )}
                </div>
                <h3 className="text-base font-bold text-slate-900 leading-snug">
                  {track.title}
                </h3>
              </div>

              <button
                onClick={() => setIsDrawerOpen(false)}
                className="p-1.5 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-500 hover:text-slate-800 transition cursor-pointer shrink-0"
              >
                <ChevronDown className="w-5 h-5" />
              </button>
            </div>

            {/* 播放进度拖动条 */}
            <div className="mb-5 space-y-1.5">
              <div className="flex items-center justify-between text-xs">
                <span className="text-indigo-600 font-bold">
                  第 {player.activeSegmentIndex + 1} / {totalSegments} 句
                </span>
                {player.engineMode === 'audio' ? (
                  <span className="text-slate-500 font-mono font-semibold">
                    {formatSeconds(player.currentTime)} / {formatSeconds(player.duration)}
                  </span>
                ) : (
                  <span className="text-slate-500 font-semibold text-xs">TTS 逐句</span>
                )}
              </div>

              {player.engineMode === 'tts' ? (
                <div className="flex items-center gap-1 py-1">
                  {track.segments.map((seg, idx) => (
                    <button
                      key={seg.id}
                      onClick={() => player.seekToSegment(idx, true)}
                      className={`h-2.5 flex-1 rounded-full transition-all cursor-pointer ${
                        idx === player.activeSegmentIndex
                          ? 'bg-indigo-600 ring-2 ring-indigo-400/50'
                          : idx < player.activeSegmentIndex
                          ? 'bg-indigo-200'
                          : 'bg-slate-200'
                      }`}
                    />
                  ))}
                </div>
              ) : (
                <input
                  type="range"
                  min={0}
                  max={player.duration || 100}
                  step={0.05}
                  value={player.currentTime}
                  onChange={(e) => player.seekToTime(parseFloat(e.target.value))}
                  className="w-full h-2 rounded-lg cursor-pointer"
                />
              )}
            </div>

            {/* 大尺寸核心播放控制区 */}
            <div className="flex items-center justify-center gap-5 mb-5">
              <button
                onClick={player.prevSegment}
                disabled={player.activeSegmentIndex <= 0}
                className="p-3.5 rounded-2xl bg-slate-100 text-slate-700 hover:bg-slate-200 disabled:opacity-30 active:scale-95 transition cursor-pointer border border-slate-200/60 shadow-2xs"
              >
                <SkipBack className="w-6 h-6" />
              </button>

              <button
                onClick={player.togglePlay}
                className="w-16 h-16 rounded-full bg-gradient-to-r from-indigo-600 to-indigo-700 text-white flex items-center justify-center shadow-lg shadow-indigo-600/30 active:scale-95 transition cursor-pointer"
              >
                {player.isPlaying ? (
                  <Pause className="w-7 h-7" />
                ) : (
                  <Play className="w-7 h-7 ml-1" />
                )}
              </button>

              <button
                onClick={player.nextSegment}
                disabled={player.activeSegmentIndex >= totalSegments - 1}
                className="p-3.5 rounded-2xl bg-slate-100 text-slate-700 hover:bg-slate-200 disabled:opacity-30 active:scale-95 transition cursor-pointer border border-slate-200/60 shadow-2xs"
              >
                <SkipForward className="w-6 h-6" />
              </button>
            </div>

            {/* 辅助循环与跟读停顿 */}
            <div className="grid grid-cols-2 gap-2.5 mb-5">
              <button
                onClick={player.toggleLoopSentence}
                className={`py-2.5 px-3 rounded-xl text-xs font-semibold inline-flex items-center justify-center gap-1.5 border transition cursor-pointer shadow-2xs active:scale-95 ${
                  player.isLoopingSentence
                    ? 'bg-amber-50 border-amber-300 text-amber-800 font-bold shadow-xs'
                    : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
                }`}
              >
                <Repeat className="w-4 h-4" />
                <span>{player.isLoopingSentence ? '单句循环: 开' : '单句循环: 关'}</span>
              </button>

              <button
                onClick={cycleAutoPause}
                className={`py-2.5 px-3 rounded-xl text-xs font-semibold inline-flex items-center justify-center gap-1.5 border transition cursor-pointer shadow-2xs active:scale-95 ${
                  autoPauseSeconds > 0
                    ? 'bg-emerald-50 border-emerald-300 text-emerald-800 font-bold shadow-xs'
                    : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
                }`}
              >
                <Timer className="w-4 h-4" />
                <span>
                  {autoPauseSeconds > 0 ? `跟读停顿: ${autoPauseSeconds}s` : '跟读停顿: 关'}
                </span>
              </button>
            </div>

            {/* 播放倍速分段切换 */}
            <div className="mb-5">
              <label className="text-xs font-bold text-slate-500 mb-1.5 block">
                播放倍速
              </label>
              <div className="grid grid-cols-5 gap-1.5 bg-slate-100 p-1 rounded-xl">
                {SPEED_OPTIONS.map((rate) => {
                  const active = Math.abs(player.playbackRate - rate) < 0.01;
                  return (
                    <button
                      key={rate}
                      onClick={() => player.setPlaybackRate(rate)}
                      className={`py-1.5 rounded-lg text-xs font-mono font-semibold transition cursor-pointer ${
                        active
                          ? 'bg-indigo-600 text-white shadow-xs font-bold'
                          : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
                      }`}
                    >
                      {rate}x
                    </button>
                  );
                })}
              </div>
            </div>

            {/* 字幕与训练模式切换 */}
            <div>
              <label className="text-xs font-bold text-slate-500 mb-1.5 block">
                字幕与训练模式
              </label>
              <div className="grid grid-cols-4 gap-1.5 bg-slate-100 p-1 rounded-xl">
                {MODE_OPTIONS.map(({ mode, label, icon: Icon }) => {
                  const active = displayMode === mode;
                  return (
                    <button
                      key={mode}
                      onClick={() => setDisplayMode(mode)}
                      className={`py-1.5 px-1 rounded-lg text-xs font-semibold inline-flex items-center justify-center gap-1 transition cursor-pointer ${
                        active
                          ? 'bg-indigo-600 text-white shadow-xs font-bold'
                          : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
                      }`}
                    >
                      <Icon className="w-3.5 h-3.5" />
                      <span>{label}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        </>
      )}
    </>
  );
};
