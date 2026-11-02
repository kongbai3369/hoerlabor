import React, { useState, useMemo } from 'react';
import { Headphones, Radio, Plus, Award, GraduationCap, Tag } from 'lucide-react';
import type { CefrLevel } from '../types/listening';
import { LEVEL_BADGE_STYLE } from '../types/listening';
import { useListeningStore, mergeAllTracks } from '../store/useListeningStore';
import { ImportModal } from './ImportModal';

const LEVELS: Array<CefrLevel | 'ALL'> = ['ALL', 'A1', 'A2', 'B1', 'B2', 'C1', 'TestDaF'];

type AuthorityFilter = 'ALL' | 'Goethe-Institut' | 'TestDaF';

interface SidebarProps {
  onSelectTrack?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ onSelectTrack }) => {
  const { selectedLevel, setSelectedLevel, currentTrackId, setCurrentTrackId, customTracks } =
    useListeningStore();
  const [isImportOpen, setIsImportOpen] = useState(false);
  const [selectedAuthority, setSelectedAuthority] = useState<AuthorityFilter>('ALL');
  const [selectedTopic, setSelectedTopic] = useState<string>('ALL');

  const allTracks = useMemo(() => mergeAllTracks(customTracks), [customTracks]);

  // Extract distinct topics
  const topics = useMemo(() => {
    const set = new Set<string>();
    allTracks.forEach((t) => {
      if (t.topic) set.add(t.topic);
    });
    return Array.from(set);
  }, [allTracks]);

  // Filter tracks by Authority, Level, and Topic
  const filteredTracks = useMemo(() => {
    return allTracks.filter((track) => {
      const matchLevel = selectedLevel === 'ALL' || track.level === selectedLevel;
      const matchAuthority = selectedAuthority === 'ALL' || track.source === selectedAuthority;
      const matchTopic = selectedTopic === 'ALL' || track.topic === selectedTopic;
      return matchLevel && matchAuthority && matchTopic;
    });
  }, [allTracks, selectedLevel, selectedAuthority, selectedTopic]);

  const goetheCount = useMemo(
    () => allTracks.filter((t) => t.source === 'Goethe-Institut').length,
    [allTracks]
  );
  const testdafCount = useMemo(
    () => allTracks.filter((t) => t.source === 'TestDaF').length,
    [allTracks]
  );

  return (
    <aside className="w-full lg:w-88 bg-white border-r border-slate-200/80 flex flex-col h-full select-none shrink-0 shadow-xs">
      {/* 顶部品牌区与官方真题标识 */}
      <div className="p-4 border-b border-slate-200/80 flex items-center justify-between gap-3 bg-white">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-600 to-indigo-800 flex items-center justify-center text-white shadow-md shadow-indigo-600/25 shrink-0">
            <Headphones className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold text-slate-900 tracking-tight flex items-center gap-1.5">
              <span>HörLabor 德语精听室</span>
              <span className="text-[10px] font-semibold px-1.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300">
                100% 官方真题
              </span>
            </h1>
            <p className="text-[11px] text-slate-500 font-medium">歌德学院官网 · 德福官网官方原声语料</p>
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

      {/* 来源与考试机构筛选 (歌德 vs 德福) */}
      <div className="p-2.5 border-b border-slate-200/70 bg-slate-50/50">
        <div className="flex items-center gap-1.5 p-1 bg-slate-200/70 rounded-xl">
          <button
            onClick={() => setSelectedAuthority('ALL')}
            className={`flex-1 py-1.5 px-2 rounded-lg text-xs font-semibold transition cursor-pointer text-center ${
              selectedAuthority === 'ALL'
                ? 'bg-white text-indigo-700 shadow-xs font-bold'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            全部官方来源 ({allTracks.length})
          </button>
          <button
            onClick={() => setSelectedAuthority('Goethe-Institut')}
            className={`flex-1 py-1.5 px-2 rounded-lg text-xs font-semibold transition cursor-pointer flex items-center justify-center gap-1 ${
              selectedAuthority === 'Goethe-Institut'
                ? 'bg-white text-emerald-800 shadow-xs font-bold'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Award className="w-3.5 h-3.5 text-emerald-600" />
            <span>歌德 ({goetheCount})</span>
          </button>
          <button
            onClick={() => setSelectedAuthority('TestDaF')}
            className={`flex-1 py-1.5 px-2 rounded-lg text-xs font-semibold transition cursor-pointer flex items-center justify-center gap-1 ${
              selectedAuthority === 'TestDaF'
                ? 'bg-white text-amber-800 shadow-xs font-bold'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <GraduationCap className="w-3.5 h-3.5 text-amber-600" />
            <span>德福 ({testdafCount})</span>
          </button>
        </div>
      </div>

      {/* 欧标等级筛选栏（4列对称布局） */}
      <div className="p-2.5 border-b border-slate-200/80 bg-slate-50/70">
        <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1.5 px-0.5">
          语料分级 (Level)
        </div>
        <div className="grid grid-cols-4 gap-1.5">
          {LEVELS.map((lvl) => {
            const active = selectedLevel === lvl;
            const isTestDaf = lvl === 'TestDaF';
            const count =
              lvl === 'ALL'
                ? allTracks.length
                : allTracks.filter((t) => t.level === lvl).length;
            return (
              <button
                key={lvl}
                onClick={() => setSelectedLevel(lvl)}
                className={`py-1.5 px-1.5 rounded-lg text-xs font-semibold transition-all text-center cursor-pointer flex items-center justify-center gap-1 ${
                  isTestDaf ? 'col-span-2' : 'col-span-1'
                } ${
                  active
                    ? 'bg-indigo-600 text-white shadow-xs font-bold'
                    : 'bg-white text-slate-600 hover:text-slate-900 hover:bg-slate-100/80 border border-slate-200/80 shadow-2xs'
                }`}
              >
                <span>{lvl === 'ALL' ? '全部' : lvl}</span>
                <span
                  className={`text-[10px] px-1 py-0.2 rounded-full font-normal ${
                    active ? 'bg-white/20 text-white' : 'text-slate-400'
                  }`}
                >
                  {count}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* 主题标签分类栏 (Topics) */}
      <div className="p-2.5 border-b border-slate-200/80 bg-white">
        <div className="flex items-center gap-1 text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1.5 px-0.5">
          <Tag className="w-3 h-3 text-slate-400" />
          <span>核心主题 (Themen)</span>
        </div>
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none text-xs">
          <button
            onClick={() => setSelectedTopic('ALL')}
            className={`px-2.5 py-1 rounded-full text-xs font-medium whitespace-nowrap transition cursor-pointer ${
              selectedTopic === 'ALL'
                ? 'bg-slate-800 text-white font-semibold shadow-2xs'
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            全部主题
          </button>
          {topics.map((t) => (
            <button
              key={t}
              onClick={() => setSelectedTopic(t)}
              className={`px-2.5 py-1 rounded-full text-xs font-medium whitespace-nowrap transition cursor-pointer ${
                selectedTopic === t
                  ? 'bg-indigo-600 text-white font-semibold shadow-2xs'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {/* 曲目列表 */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2.5 pb-[calc(9rem+env(safe-area-inset-bottom,0px))] lg:pb-3">
        {filteredTracks.length === 0 ? (
          <div className="text-center py-12 text-slate-400 text-sm">
            当前筛选条件下暂无听力专题
          </div>
        ) : (
          filteredTracks.map((track) => {
            const isSelected = track.id === currentTrackId;
            const isGoethe = track.source === 'Goethe-Institut';

            return (
              <button
                key={track.id}
                onClick={() => {
                  setCurrentTrackId(track.id);
                  onSelectTrack?.();
                }}
                className={`w-full text-left p-3 rounded-xl border transition-all cursor-pointer relative overflow-hidden ${
                  isSelected
                    ? 'bg-indigo-50/80 border-indigo-300 ring-1 ring-indigo-500/25 shadow-xs'
                    : 'bg-white border-slate-200/80 hover:bg-slate-50/80 hover:border-slate-300 shadow-2xs'
                }`}
              >
                {isSelected && (
                  <div className="absolute left-0 top-2 bottom-2 w-1 bg-indigo-600 rounded-r-full" />
                )}

                {/* 顶栏：分级 + 来源 + 主题 */}
                <div className="flex items-center justify-between gap-1.5 mb-1.5 flex-wrap">
                  <div className="flex items-center gap-1.5">
                    <span
                      className={`text-[11px] font-bold px-2 py-0.5 rounded-md border ${
                        LEVEL_BADGE_STYLE[track.level]
                      }`}
                    >
                      {track.level}
                    </span>
                    <span
                      className={`inline-flex items-center gap-0.5 text-[10px] px-1.5 py-0.5 rounded font-medium border ${
                        isGoethe
                          ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                          : 'bg-amber-50 text-amber-800 border-amber-200'
                      }`}
                    >
                      {isGoethe ? <Award className="w-3 h-3" /> : <GraduationCap className="w-3 h-3" />}
                      <span>{isGoethe ? '歌德真题' : '德福真题'}</span>
                    </span>
                  </div>

                  <span className="text-[10px] text-slate-500 font-medium bg-slate-100 px-1.5 py-0.5 rounded border border-slate-200/60 truncate max-w-[120px]">
                    {track.topic}
                  </span>
                </div>

                {/* 标题 */}
                <h3
                  className={`text-sm font-semibold line-clamp-1 mb-1.5 ${
                    isSelected ? 'text-indigo-950 font-bold' : 'text-slate-800'
                  }`}
                >
                  {track.title}
                </h3>

                {/* 题型考点标签 */}
                {track.taskSection && (
                  <div className="mb-1.5 flex items-center">
                    <span className="inline-flex items-center text-[10px] font-medium px-1.5 py-0.5 rounded bg-violet-50 text-violet-700 border border-violet-200/70 truncate max-w-full">
                      🎯 {track.taskSection}
                    </span>
                  </div>
                )}

                {/* 底栏：原声MP3标记 + 3句精听 + 时长 */}
                <div className="flex items-center justify-between text-xs text-slate-500 pt-1.5 border-t border-slate-100">
                  <span className="inline-flex items-center gap-1 text-[11px] text-emerald-700 font-medium">
                    <Radio className="w-3 h-3 text-emerald-600" />
                    <span>真题原声 ({track.duration ? `${track.duration}s` : 'MP3'})</span>
                  </span>
                  <span className="shrink-0 text-slate-400 font-medium text-[11px]">
                    {track.segments.length} 句精听
                  </span>
                </div>
              </button>
            );
          })
        )}
      </div>

      {/* 底部快捷键提示 */}
      <div className="hidden lg:block p-3 border-t border-slate-200/80 bg-slate-50/90 text-[11px] text-slate-500 space-y-1.5 pb-28 select-none">
        <div className="flex justify-between items-center">
          <span>单句自由点播</span>
          <div className="flex items-center gap-1">
            <kbd className="px-1.5 py-0.5 bg-white border border-slate-200 rounded text-slate-700 font-mono text-[10px] shadow-2xs">1</kbd>
            <kbd className="px-1.5 py-0.5 bg-white border border-slate-200 rounded text-slate-700 font-mono text-[10px] shadow-2xs">2</kbd>
            <kbd className="px-1.5 py-0.5 bg-white border border-slate-200 rounded text-slate-700 font-mono text-[10px] shadow-2xs">3</kbd>
          </div>
        </div>
        <div className="flex justify-between items-center">
          <span>播放 / 暂停</span>
          <kbd className="px-1.5 py-0.5 bg-white border border-slate-200 rounded text-slate-700 font-mono text-[10px] shadow-2xs">Space</kbd>
        </div>
        <div className="flex justify-between items-center">
          <span>单句精听 / 连续连播</span>
          <kbd className="px-1.5 py-0.5 bg-white border border-slate-200 rounded text-slate-700 font-mono text-[10px] shadow-2xs">L</kbd>
        </div>
      </div>

      <ImportModal isOpen={isImportOpen} onClose={() => setIsImportOpen(false)} />
    </aside>
  );
};
