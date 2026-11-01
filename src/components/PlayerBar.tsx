import React from 'react';
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
} from 'lucide-react';
import type { DisplayMode, ListeningTrack } from '../types/listening';
import type { AudioPlayerControls } from '../hooks/useAudioPlayer';
import { useListeningStore } from '../store/useListeningStore';

interface PlayerBarProps {
  track: ListeningTrack;
  player: AudioPlayerControls;
}

const SPEED_OPTIONS = [0.75, 0.9, 1.0, 1.2, 1.5];
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
  const totalSegments = track.segments.length;

  const cycleAutoPause = () => {
    const nextIdx = (PAUSE_OPTIONS.indexOf(autoPauseSeconds) + 1) % PAUSE_OPTIONS.length;
    setAutoPauseSeconds(PAUSE_OPTIONS[nextIdx]);
  };

  return (
    <footer className="fixed bottom-4 sm:bottom-5 left-1/2 -translate-x-1/2 w-[94%] max-w-5xl bg-white/95 backdrop-blur-md shadow-[0_12px_40px_-8px_rgba(15,23,42,0.15),0_4px_12px_-2px_rgba(15,23,42,0.06)] rounded-2xl border border-slate-200/90 z-40 px-4 sm:px-6 py-2.5 sm:py-3 select-none flex flex-wrap items-center justify-between gap-3 sm:gap-4">
      {/* 左侧进度区 */}
      <div className="w-full md:w-64 lg:w-72 flex flex-col justify-center gap-1.5 shrink-0">
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
                    className="hidden sm:inline-flex items-center text-[10px] text-emerald-700 hover:text-emerald-800 underline decoration-dotted ml-1 font-medium"
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
      <div className="flex items-center gap-1.5 sm:gap-2.5 mx-auto md:mx-0">
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
          className={`px-2.5 py-1.5 sm:py-2 rounded-xl text-xs font-medium inline-flex items-center gap-1 border transition cursor-pointer shadow-2xs active:scale-95 ${
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
          className={`px-2.5 py-1.5 sm:py-2 rounded-xl text-xs font-medium inline-flex items-center gap-1 border transition cursor-pointer shadow-2xs active:scale-95 ${
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
                className={`px-1.5 sm:px-2 py-1 rounded-lg text-xs font-mono transition cursor-pointer ${
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
                className={`px-2 sm:px-2.5 py-1 rounded-lg text-xs font-medium inline-flex items-center gap-1 transition cursor-pointer ${
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
  );
};
