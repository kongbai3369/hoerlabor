import React, { useState, useMemo } from 'react';
import {
  Headphones,
  Radio,
  Plus,
  Tag,
  Search,
  X,
  CheckCircle2,
  RotateCcw,
  Sparkles,
} from 'lucide-react';
import type { CefrLevel, SourceCategory } from '../types/listening';
import {
  LEVEL_BADGE_STYLE,
  SOURCE_CATEGORY_META,
  getSourceDisplayInfo,
} from '../types/listening';
import { useListeningStore, mergeAllTracks } from '../store/useListeningStore';
import { ImportModal } from './ImportModal';
import { SourceBadge } from './SourceBadge';

const LEVELS: Array<CefrLevel | 'ALL'> = ['ALL', 'A1', 'A2', 'B1', 'B2', 'C1', 'TestDaF'];
const CATEGORY_ORDER: SourceCategory[] = ['exam', 'news', 'podcast', 'authentic', 'custom'];

interface SidebarProps {
  onSelectTrack?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ onSelectTrack }) => {
  const {
    selectedLevel,
    setSelectedLevel,
    selectedSourceCategory,
    setSelectedSourceCategory,
    selectedSource,
    setSelectedSource,
    searchQuery,
    setSearchQuery,
    onlyUncompleted,
    setOnlyUncompleted,
    resetFilters,
    currentTrackId,
    setCurrentTrackId,
    customTracks,
    remoteCatalog,
    loadedTrackDetails,
    completedTrackIds,
    dictationScores,
  } = useListeningStore();

  const [isImportOpen, setIsImportOpen] = useState(false);
  const [selectedTopic, setSelectedTopic] = useState<string>('ALL');

  const allTracks = useMemo(
    () => mergeAllTracks(customTracks, remoteCatalog, loadedTrackDetails),
    [customTracks, remoteCatalog, loadedTrackDetails]
  );

  // 动态统计各分类曲目数（仅展示存在语料的分类）
  const categoryCounts = useMemo(() => {
    const counts: Record<SourceCategory, number> = {
      exam: 0,
      news: 0,
      podcast: 0,
      authentic: 0,
      custom: 0,
    };
    allTracks.forEach((t) => {
      const cat = t.sourceCategory || getSourceDisplayInfo(t).category;
      counts[cat] = (counts[cat] || 0) + 1;
    });
    return counts;
  }, [allTracks]);

  const activeCategories = useMemo(
    () => CATEGORY_ORDER.filter((cat) => categoryCounts[cat] > 0),
    [categoryCounts]
  );

  // 动态提取当前分类下的具体来源机构/站点列表
  const availableSources = useMemo(() => {
    const map = new Map<string, number>();
    allTracks.forEach((t) => {
      const cat = t.sourceCategory || getSourceDisplayInfo(t).category;
      if (selectedSourceCategory !== 'ALL' && cat !== selectedSourceCategory) return;
      map.set(t.source, (map.get(t.source) || 0) + 1);
    });
    return Array.from(map.entries());
  }, [allTracks, selectedSourceCategory]);

  // 动态提取话题列表
  const topics = useMemo(() => {
    const set = new Set<string>();
    allTracks.forEach((t) => {
      if (t.topic) set.add(t.topic);
    });
    return Array.from(set);
  }, [allTracks]);

  // 多维联合筛选
  const filteredTracks = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();
    return allTracks.filter((track) => {
      const cat = track.sourceCategory || getSourceDisplayInfo(track).category;
      const matchCategory = selectedSourceCategory === 'ALL' || cat === selectedSourceCategory;
      const matchSource = selectedSource === 'ALL' || track.source === selectedSource;
      const matchLevel = selectedLevel === 'ALL' || track.level === selectedLevel;
      const matchTopic = selectedTopic === 'ALL' || track.topic === selectedTopic;
      const matchUncompleted = !onlyUncompleted || !completedTrackIds.includes(track.id);
      const matchQuery =
        !q ||
        track.title.toLowerCase().includes(q) ||
        track.topic.toLowerCase().includes(q) ||
        track.source.toLowerCase().includes(q) ||
        (track.taskSection || '').toLowerCase().includes(q);
      return (
        matchCategory &&
        matchSource &&
        matchLevel &&
        matchTopic &&
        matchUncompleted &&
        matchQuery
      );
    });
  }, [
    allTracks,
    selectedSourceCategory,
    selectedSource,
    selectedLevel,
    selectedTopic,
    onlyUncompleted,
    completedTrackIds,
    searchQuery,
  ]);

  const handleResetAll = () => {
    resetFilters();
    setSelectedTopic('ALL');
  };

  return (
    <aside className="w-full lg:w-88 bg-white border-r border-slate-200/80 flex flex-col h-full select-none shrink-0 shadow-xs">
      {/* 顶部品牌区与自定义导入入口 */}
      <div className="p-3.5 border-b border-slate-200/80 flex items-center justify-between gap-3 bg-white">
        <div className="flex items-center gap-2.5 min-w-0">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-600 to-indigo-800 flex items-center justify-center text-white shadow-md shadow-indigo-600/25 shrink-0">
            <Headphones className="w-5 h-5" />
          </div>
          <div className="min-w-0">
            <h1 className="text-sm sm:text-base font-bold text-slate-900 tracking-tight flex items-center gap-1.5 flex-wrap">
              <span className="truncate">HörLabor 德语精听室</span>
              <span className="text-[10px] font-semibold px-1.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300 shrink-0">
                {completedTrackIds.length}/{allTracks.length} 已练
              </span>
            </h1>
            <p className="text-[11px] text-slate-500 font-medium truncate">
              真题 · 慢速新闻 · 播客 · 母语原声库
            </p>
          </div>
        </div>

        <button
          onClick={() => setIsImportOpen(true)}
          title="导入自定义德语语料"
          className="p-2 rounded-lg bg-indigo-50 hover:bg-indigo-100 text-indigo-600 border border-indigo-200/80 transition cursor-pointer shadow-2xs hover:shadow-xs active:scale-95 shrink-0"
        >
          <Plus className="w-4 h-4" />
        </button>
      </div>

      {/* 关键词搜索 + 未学筛选栏 */}
      <div className="px-2.5 pt-2.5 pb-1.5 border-b border-slate-100 bg-white flex items-center gap-1.5">
        <div className="relative flex-1">
          <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="搜标题、考点、来源…"
            className="w-full pl-7 pr-6 py-1.5 rounded-lg bg-slate-50 border border-slate-200/80 text-xs text-slate-800 placeholder:text-slate-400 focus:bg-white focus:border-indigo-400 focus:outline-none transition"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery('')}
              aria-label="清空搜索"
              className="absolute right-1.5 top-1/2 -translate-y-1/2 p-0.5 text-slate-400 hover:text-slate-700 cursor-pointer"
            >
              <X className="w-3 h-3" />
            </button>
          )}
        </div>

        <button
          onClick={() => setOnlyUncompleted(!onlyUncompleted)}
          title="仅显示尚未听完练习的篇目"
          className={`px-2 py-1.5 rounded-lg text-[11px] font-semibold border transition cursor-pointer whitespace-nowrap ${
            onlyUncompleted
              ? 'bg-emerald-50 border-emerald-300 text-emerald-800 shadow-2xs'
              : 'bg-slate-50 border-slate-200/80 text-slate-600 hover:bg-slate-100'
          }`}
        >
          只看未学
        </button>
      </div>

      {/* 动态内容分类筛选 (考级 / 新闻 / 播客 / 口语 / 自定义) */}
      <div className="p-2 border-b border-slate-200/70 bg-slate-50/60 space-y-1.5">
        <div className="flex items-center gap-1 overflow-x-auto pb-0.5 scrollbar-none">
          <button
            onClick={() => setSelectedSourceCategory('ALL')}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition cursor-pointer whitespace-nowrap ${
              selectedSourceCategory === 'ALL'
                ? 'bg-indigo-600 text-white shadow-xs font-bold'
                : 'bg-white text-slate-600 hover:text-slate-900 border border-slate-200/80'
            }`}
          >
            全部 ({allTracks.length})
          </button>
          {activeCategories.map((cat) => {
            const meta = SOURCE_CATEGORY_META[cat];
            const active = selectedSourceCategory === cat;
            return (
              <button
                key={cat}
                onClick={() => setSelectedSourceCategory(cat)}
                className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition cursor-pointer whitespace-nowrap inline-flex items-center gap-1 ${
                  active
                    ? 'bg-indigo-600 text-white shadow-xs font-bold'
                    : 'bg-white text-slate-600 hover:text-slate-900 border border-slate-200/80'
                }`}
              >
                <span>{meta.emoji}</span>
                <span>{meta.label}</span>
                <span className={`text-[10px] ${active ? 'text-white/80' : 'text-slate-400'}`}>
                  {categoryCounts[cat]}
                </span>
              </button>
            );
          })}
        </div>

        {/* 当存在多个具体来源站点时，展示二级具体站点过滤胶囊 */}
        {availableSources.length > 1 && (
          <div className="flex items-center gap-1 overflow-x-auto pb-0.5 scrollbar-none">
            <button
              onClick={() => setSelectedSource('ALL')}
              className={`px-2 py-0.5 rounded-md text-[11px] font-medium transition cursor-pointer whitespace-nowrap ${
                selectedSource === 'ALL'
                  ? 'bg-slate-800 text-white font-semibold'
                  : 'bg-slate-200/70 text-slate-600 hover:bg-slate-200'
              }`}
            >
              全站点
            </button>
            {availableSources.map(([srcName, cnt]) => {
              const info = getSourceDisplayInfo({ source: srcName });
              const active = selectedSource === srcName;
              return (
                <button
                  key={srcName}
                  onClick={() => setSelectedSource(srcName)}
                  className={`px-2 py-0.5 rounded-md text-[11px] font-medium transition cursor-pointer whitespace-nowrap inline-flex items-center gap-1 ${
                    active
                      ? 'bg-indigo-100 text-indigo-900 border border-indigo-300 font-semibold'
                      : 'bg-white text-slate-600 border border-slate-200/80 hover:bg-slate-100'
                  }`}
                >
                  <span>{info.shortLabel}</span>
                  <span className="text-[10px] opacity-70">{cnt}</span>
                </button>
              );
            })}
          </div>
        )}
      </div>

      {/* 欧标等级筛选栏（4列对称布局） */}
      <div className="p-2.5 border-b border-slate-200/80 bg-slate-50/70">
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
                className={`py-1 px-1.5 rounded-lg text-xs font-semibold transition-all text-center cursor-pointer flex items-center justify-center gap-1 ${
                  isTestDaf ? 'col-span-2' : 'col-span-1'
                } ${
                  active
                    ? 'bg-indigo-600 text-white shadow-xs font-bold'
                    : 'bg-white text-slate-600 hover:text-slate-900 hover:bg-slate-100/80 border border-slate-200/80 shadow-2xs'
                }`}
              >
                <span>{lvl === 'ALL' ? '全部等级' : lvl}</span>
                <span
                  className={`text-[10px] px-1 rounded-full font-normal ${
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
      <div className="px-2.5 py-2 border-b border-slate-200/80 bg-white">
        <div className="flex items-center gap-1.5 overflow-x-auto pb-0.5 scrollbar-none text-xs">
          <Tag className="w-3.5 h-3.5 text-slate-400 shrink-0" />
          <button
            onClick={() => setSelectedTopic('ALL')}
            className={`px-2.5 py-0.5 rounded-full text-[11px] font-medium whitespace-nowrap transition cursor-pointer ${
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
              className={`px-2.5 py-0.5 rounded-full text-[11px] font-medium whitespace-nowrap transition cursor-pointer ${
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
          <div className="text-center py-10 px-4 space-y-3">
            <p className="text-slate-400 text-sm">当前筛选条件下暂无匹配曲目</p>
            <button
              onClick={handleResetAll}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-50 text-indigo-700 hover:bg-indigo-100 border border-indigo-200 text-xs font-semibold cursor-pointer transition"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>重置所有筛选</span>
            </button>
          </div>
        ) : (
          filteredTracks.map((track) => {
            const isSelected = track.id === currentTrackId;
            const isCompleted = completedTrackIds.includes(track.id);
            const score = dictationScores[track.id];
            const segCount = track.segmentCount ?? track.segments?.length ?? 0;

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

                {/* 顶栏：分级 + 动态来源 + 主题 */}
                <div className="flex items-center justify-between gap-1.5 mb-1.5 flex-wrap">
                  <div className="flex items-center gap-1.5 min-w-0">
                    <span
                      className={`text-[11px] font-bold px-2 py-0.5 rounded-md border shrink-0 ${
                        LEVEL_BADGE_STYLE[track.level]
                      }`}
                    >
                      {track.level}
                    </span>
                    <SourceBadge track={track} compact />
                  </div>

                  <span className="text-[10px] text-slate-500 font-medium bg-slate-100 px-1.5 py-0.5 rounded border border-slate-200/60 truncate max-w-[110px]">
                    {track.topic}
                  </span>
                </div>

                {/* 标题 + 完成打卡与听写分标 */}
                <div className="flex items-start justify-between gap-1.5 mb-1.5">
                  <h3
                    className={`text-sm font-semibold line-clamp-1 ${
                      isSelected ? 'text-indigo-950 font-bold' : 'text-slate-800'
                    }`}
                  >
                    {track.title}
                  </h3>
                  {isCompleted && (
                    <span title="已完成精听" className="shrink-0 mt-0.5">
                      <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                    </span>
                  )}
                </div>

                {/* 考点 / 栏目副标签 */}
                {track.taskSection && (
                  <div className="mb-1.5 flex items-center gap-1.5 flex-wrap">
                    <span
                      title={track.taskSection}
                      className="inline-flex items-center text-[10px] font-medium px-1.5 py-0.5 rounded bg-violet-50 text-violet-700 border border-violet-200/70 truncate max-w-full"
                    >
                      🎯 {track.taskSection}
                    </span>
                    {score && score.total > 0 && (
                      <span className="text-[10px] font-mono font-semibold px-1.5 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200">
                        听写 {score.correct}/{score.total}
                      </span>
                    )}
                  </div>
                )}

                {/* 底栏：音频模式 + 句数 + 时长 */}
                <div className="flex items-center justify-between text-xs text-slate-500 pt-1.5 border-t border-slate-100">
                  {track.audioUrl ? (
                    <span className="inline-flex items-center gap-1 text-[11px] text-emerald-700 font-medium">
                      <Radio className="w-3 h-3 text-emerald-600" />
                      <span>
                        原声音频 ({track.duration ? `${Math.round(track.duration)}s` : 'MP3'})
                      </span>
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 text-[11px] text-amber-700 font-medium">
                      <Sparkles className="w-3 h-3 text-amber-500" />
                      <span>TTS 文本驱动</span>
                    </span>
                  )}
                  <span className="shrink-0 text-slate-400 font-medium text-[11px]">
                    {segCount} 句精听
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
            <kbd className="px-1.5 py-0.5 bg-white border border-slate-200 rounded text-slate-700 font-mono text-[10px] shadow-2xs">
              1~9
            </kbd>
            <span className="text-slate-400">/</span>
            <kbd className="px-1.5 py-0.5 bg-white border border-slate-200 rounded text-slate-700 font-mono text-[10px] shadow-2xs">
              ← / →
            </kbd>
          </div>
        </div>
        <div className="flex justify-between items-center">
          <span>播放 / 暂停</span>
          <kbd className="px-1.5 py-0.5 bg-white border border-slate-200 rounded text-slate-700 font-mono text-[10px] shadow-2xs">
            Space
          </kbd>
        </div>
        <div className="flex justify-between items-center">
          <span>单句循环开关</span>
          <kbd className="px-1.5 py-0.5 bg-white border border-slate-200 rounded text-slate-700 font-mono text-[10px] shadow-2xs">
            L
          </kbd>
        </div>
      </div>

      <ImportModal isOpen={isImportOpen} onClose={() => setIsImportOpen(false)} />
    </aside>
  );
};
