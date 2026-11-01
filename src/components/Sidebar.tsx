import React, { useState } from 'react';
import { Headphones, Sparkles, BookOpen, Radio, Plus } from 'lucide-react';
import type { CefrLevel } from '../types/listening';
import { LEVEL_BADGE_STYLE } from '../types/listening';
import { useListeningStore, mergeAllTracks } from '../store/useListeningStore';
import { ImportModal } from './ImportModal';

const LEVELS: Array<CefrLevel | 'ALL'> = ['ALL', 'A1', 'A2', 'B1', 'B2', 'C1', 'TestDaF'];

interface SidebarProps {
  onSelectTrack?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ onSelectTrack }) => {
  const { selectedLevel, setSelectedLevel, currentTrackId, setCurrentTrackId, customTracks } =
    useListeningStore();
  const [isImportOpen, setIsImportOpen] = useState(false);

  const allTracks = mergeAllTracks(customTracks);
  const filteredTracks =
    selectedLevel === 'ALL'
      ? allTracks
      : allTracks.filter((t) => t.level === selectedLevel);

  return (
    <aside className="w-full lg:w-80 bg-white border-r border-slate-200/80 flex flex-col h-full select-none shrink-0 shadow-xs">
      {/* 顶部品牌区与导入入口 */}
      <div className="p-4 border-b border-slate-200/80 flex items-center justify-between gap-3 bg-white">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-600 to-indigo-800 flex items-center justify-center text-white shadow-md shadow-indigo-600/25 shrink-0">
            <Headphones className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold text-slate-900 tracking-tight">
              HörLabor 德语精听室
            </h1>
            <p className="text-[11px] text-slate-500 font-medium">DW · 歌德 · SlowGerman · ZDF · Quarks</p>
          </div>
        </div>

        <button
          onClick={() => setIsImportOpen(true)}
          title="导入自定义德语语料"
          className="p-2 rounded-lg bg-indigo-50 hover:bg-indigo-100 text-indigo-600 border border-indigo-200/80 transition cursor-pointer shadow-2xs hover:shadow-xs active:scale-95"
        >
          <Plus className="w-4 h-4" />
        </button>
      </div>

      {/* 欧标等级筛选栏（4列对称无缺口布局：TestDaF独占2列） */}
      <div className="p-3 border-b border-slate-200/80 bg-slate-50/70">
        <div className="grid grid-cols-4 gap-1.5">
          {LEVELS.map((lvl) => {
            const active = selectedLevel === lvl;
            const isTestDaf = lvl === 'TestDaF';
            return (
              <button
                key={lvl}
                onClick={() => setSelectedLevel(lvl)}
                className={`py-1.5 px-2 rounded-lg text-xs font-semibold transition-all text-center cursor-pointer ${
                  isTestDaf ? 'col-span-2' : 'col-span-1'
                } ${
                  active
                    ? 'bg-indigo-600 text-white shadow-xs font-bold'
                    : 'bg-white text-slate-600 hover:text-slate-900 hover:bg-slate-100/80 border border-slate-200/80 shadow-2xs'
                }`}
              >
                {lvl === 'ALL' ? '全部' : lvl}
              </button>
            );
          })}
        </div>
      </div>

      {/* 曲目列表 */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {filteredTracks.length === 0 ? (
          <div className="text-center py-12 text-slate-400 text-sm">
            该等级暂无曲目数据
          </div>
        ) : (
          filteredTracks.map((track) => {
            const isSelected = track.id === currentTrackId;
            const isTts = !track.audioUrl;

            return (
              <button
                key={track.id}
                onClick={() => {
                  setCurrentTrackId(track.id);
                  onSelectTrack?.();
                }}
                className={`w-full text-left p-3.5 rounded-xl border transition-all cursor-pointer relative overflow-hidden ${
                  isSelected
                    ? 'bg-indigo-50/80 border-indigo-300 ring-1 ring-indigo-500/25 shadow-xs'
                    : 'bg-white border-slate-200/80 hover:bg-slate-50/80 hover:border-slate-300 shadow-2xs'
                }`}
              >
                {isSelected && (
                  <div className="absolute left-0 top-2 bottom-2 w-1 bg-indigo-600 rounded-r-full" />
                )}

                <div className="flex items-center justify-between gap-2 mb-1.5">
                  <span
                    className={`text-[11px] font-semibold px-2 py-0.5 rounded-md border ${
                      LEVEL_BADGE_STYLE[track.level]
                    }`}
                  >
                    {track.level}
                  </span>
                  <span className="inline-flex items-center gap-1 text-[11px] px-2 py-0.5 rounded-full font-medium">
                    {isTts ? (
                      <span className="inline-flex items-center gap-1 text-amber-700 bg-amber-50 border border-amber-200/70 px-2 py-0.5 rounded-full">
                        <Sparkles className="w-3 h-3 text-amber-500" />
                        TTS 句驱
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 text-emerald-700 bg-emerald-50 border border-emerald-200/70 px-2 py-0.5 rounded-full">
                        <Radio className="w-3 h-3 text-emerald-600" />
                        MP3 精听
                      </span>
                    )}
                  </span>
                </div>

                <h3
                  className={`text-sm font-semibold line-clamp-1 mb-1 ${
                    isSelected ? 'text-indigo-950 font-bold' : 'text-slate-800'
                  }`}
                >
                  {track.title}
                </h3>

                <div className="flex items-center justify-between text-xs text-slate-500 mt-2 pt-2 border-t border-slate-100">
                  <span className="inline-flex items-center gap-1 truncate font-medium">
                    <BookOpen className="w-3 h-3 text-slate-400 shrink-0" />
                    <span className="truncate">{track.source}</span>
                  </span>
                  <span className="shrink-0 text-slate-400 font-medium">
                    {track.segments.length} 句
                  </span>
                </div>
              </button>
            );
          })
        )}
      </div>

      {/* 底部快捷键提示（留出 pb-28 确保绝不被悬浮播放胶囊遮挡） */}
      <div className="p-3 border-t border-slate-200/80 bg-slate-50/90 text-[11px] text-slate-500 space-y-1.5 pb-28 select-none">
        <div className="flex justify-between items-center">
          <span>播放 / 暂停</span>
          <kbd className="px-1.5 py-0.5 bg-white border border-slate-200 rounded text-slate-700 font-mono text-[10px] shadow-2xs">Space</kbd>
        </div>
        <div className="flex justify-between items-center">
          <span>上一句 / 下一句</span>
          <kbd className="px-1.5 py-0.5 bg-white border border-slate-200 rounded text-slate-700 font-mono text-[10px] shadow-2xs">← / →</kbd>
        </div>
        <div className="flex justify-between items-center">
          <span>单句循环开关</span>
          <kbd className="px-1.5 py-0.5 bg-white border border-slate-200 rounded text-slate-700 font-mono text-[10px] shadow-2xs">L</kbd>
        </div>
      </div>

      <ImportModal isOpen={isImportOpen} onClose={() => setIsImportOpen(false)} />
    </aside>
  );
};
