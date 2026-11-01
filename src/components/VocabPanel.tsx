import React, { useEffect, useRef, useState } from 'react';
import {
  Bookmark,
  Download,
  Copy,
  Check,
  BookMarked,
  Layers,
  Volume2,
  ExternalLink,
  BookOpen,
} from 'lucide-react';
import type { ListeningTrack, VocabItem } from '../types/listening';
import { useListeningStore } from '../store/useListeningStore';
import { speakGermanWord } from '../hooks/useAudioPlayer';

interface VocabPanelProps {
  track: ListeningTrack;
  activeSegmentIndex: number;
}

function getGenderBadge(word: string): {
  article: string | null;
  rest: string;
  colorClass: string;
} {
  if (word.startsWith('der ')) {
    return {
      article: 'der',
      rest: word.slice(4),
      colorClass: 'bg-sky-50 text-sky-700 border-sky-300/90',
    };
  }
  if (word.startsWith('die ')) {
    return {
      article: 'die',
      rest: word.slice(4),
      colorClass: 'bg-rose-50 text-rose-700 border-rose-300/90',
    };
  }
  if (word.startsWith('das ')) {
    return {
      article: 'das',
      rest: word.slice(4),
      colorClass: 'bg-emerald-50 text-emerald-700 border-emerald-300/90',
    };
  }
  return { article: null, rest: word, colorClass: '' };
}

export const VocabPanel: React.FC<VocabPanelProps> = ({
  track,
  activeSegmentIndex,
}) => {
  const { savedVocab, toggleSaveVocab } = useListeningStore();
  const [activeTab, setActiveTab] = useState<'track' | 'saved'>('track');
  const [copied, setCopied] = useState(false);
  const activeItemRef = useRef<HTMLDivElement | null>(null);

  const trackVocabList: Array<{ item: VocabItem; isCurrentSentence: boolean }> = [];
  track.segments.forEach((seg, idx) => {
    seg.vocab?.forEach((v) => {
      trackVocabList.push({
        item: v,
        isCurrentSentence: idx === activeSegmentIndex,
      });
    });
  });

  const displayList: Array<{ item: VocabItem; isCurrentSentence: boolean }> =
    activeTab === 'track'
      ? trackVocabList
      : savedVocab.map((item) => ({ item, isCurrentSentence: false }));

  useEffect(() => {
    if (activeTab === 'track' && activeItemRef.current) {
      activeItemRef.current.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }, [activeSegmentIndex, activeTab]);

  const buildAnkiTsv = () => {
    const sourceItems =
      activeTab === 'saved' && savedVocab.length > 0
        ? savedVocab
        : trackVocabList.map((x) => x.item);

    return sourceItems
      .map((v) => {
        const pluralInfo = v.plural ? ` (Pl. ${v.plural})` : '';
        const front = `<b>${v.word}</b>${pluralInfo}<br><span style="color:#475569">${v.exampleDe}</span>`;
        const back = `[${v.pos}] <b>${v.meaning}</b><br><span style="color:#64748b">${v.exampleZh}</span>`;
        return `${front}\t${back}`;
      })
      .join('\n');
  };

  const handleCopyAnkiTsv = async () => {
    const tsv = buildAnkiTsv();
    if (!tsv) return;
    await navigator.clipboard.writeText(tsv);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadAnkiTsv = () => {
    const tsv = buildAnkiTsv();
    if (!tsv) return;
    const blob = new Blob([tsv], { type: 'text/tab-separated-values;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `anki-deutsch-${track.level}-${track.id}.tsv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <aside className="w-full lg:w-80 bg-white border-l border-slate-200/80 flex flex-col h-full shrink-0 shadow-xs select-none">
      {/* 顶部词汇标签 */}
      <div className="p-3 border-b border-slate-200/80 flex gap-2 bg-white">
        <button
          onClick={() => setActiveTab('track')}
          className={`flex-1 py-2 px-3 rounded-lg text-xs font-semibold inline-flex items-center justify-center gap-1.5 transition cursor-pointer ${
            activeTab === 'track'
              ? 'bg-indigo-600 text-white shadow-xs font-bold'
              : 'bg-slate-100 text-slate-600 hover:text-slate-900 hover:bg-slate-200/80'
          }`}
        >
          <Layers className="w-3.5 h-3.5" />
          <span>本篇核心词 ({trackVocabList.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('saved')}
          className={`flex-1 py-2 px-3 rounded-lg text-xs font-semibold inline-flex items-center justify-center gap-1.5 transition cursor-pointer ${
            activeTab === 'saved'
              ? 'bg-indigo-600 text-white shadow-xs font-bold'
              : 'bg-slate-100 text-slate-600 hover:text-slate-900 hover:bg-slate-200/80'
          }`}
        >
          <BookMarked className="w-3.5 h-3.5" />
          <span>生词本 ({savedVocab.length})</span>
        </button>
      </div>

      {/* 词性与德语三性提示 */}
      <div className="px-4 py-2 bg-slate-50/80 border-b border-slate-200/80 flex items-center justify-between text-[11px] text-slate-500 font-medium">
        <span>真人音源：Wiktionary 维基母语</span>
        <div className="flex items-center gap-2">
          <span className="text-sky-700 font-bold">der 阳</span>
          <span className="text-rose-700 font-bold">die 阴</span>
          <span className="text-emerald-700 font-bold">das 中</span>
        </div>
      </div>

      {/* 词汇列表 */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2.5">
        {displayList.length === 0 ? (
          <div className="text-center py-12 text-slate-400 text-xs leading-relaxed px-4">
            {activeTab === 'saved'
              ? '生词本为空，点击卡片右上角书签即可收藏并随时导出至 Anki'
              : '本篇暂无挂载核心词'}
          </div>
        ) : (
          displayList.map(({ item, isCurrentSentence }, itemIdx) => {
            const isSaved = savedVocab.some((v) => v.word === item.word);
            const { article, rest, colorClass } = getGenderBadge(item.word);
            const pureLookupWord = rest.replace(/\s*\(\+.*\)/g, '').trim();
            const forvoUrl = `https://de.forvo.com/word/${encodeURIComponent(pureLookupWord)}/#de`;

            return (
              <div
                key={`${item.word}-${itemIdx}`}
                ref={isCurrentSentence ? activeItemRef : null}
                className={`p-3.5 rounded-xl border transition-all ${
                  isCurrentSentence
                    ? 'bg-indigo-50/80 border-indigo-200 shadow-xs ring-1 ring-indigo-500/20'
                    : 'bg-white border-slate-200/80 hover:bg-slate-50/80 hover:border-slate-300 shadow-2xs'
                }`}
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="flex items-center flex-wrap gap-1.5">
                    {article && (
                      <span
                        className={`text-xs font-bold px-1.5 py-0.5 rounded border shadow-2xs ${colorClass}`}
                      >
                        {article}
                      </span>
                    )}
                    <span className="text-sm font-bold text-slate-900">{rest}</span>
                    {item.plural && (
                      <span className="text-[11px] text-slate-500 font-mono">
                        (Pl. {item.plural})
                      </span>
                    )}
                  </div>

                  <div className="flex items-center gap-1 shrink-0">
                    <button
                      onClick={() => speakGermanWord(item.word)}
                      title="播放维基词典真人母语发音 (Wiktionary)"
                      className="p-1 rounded text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 transition cursor-pointer"
                    >
                      <Volume2 className="w-3.5 h-3.5" />
                    </button>

                    <a
                      href={`https://de.wiktionary.org/wiki/${encodeURIComponent(pureLookupWord)}`}
                      target="_blank"
                      rel="noreferrer"
                      title="在德语维基词典查看词条变位与释义"
                      className="p-1 rounded text-slate-400 hover:text-sky-600 hover:bg-sky-50 transition"
                    >
                      <BookOpen className="w-3.5 h-3.5" />
                    </a>

                    <a
                      href={forvoUrl}
                      target="_blank"
                      rel="noreferrer"
                      title="在 Forvo 中听更多母语者发音"
                      className="p-1 rounded text-slate-400 hover:text-amber-600 hover:bg-amber-50 transition"
                    >
                      <ExternalLink className="w-3.5 h-3.5" />
                    </a>

                    <button
                      onClick={() => toggleSaveVocab(item)}
                      title={isSaved ? '从生词本移除' : '加入生词本'}
                      className={`p-1 rounded transition cursor-pointer ${
                        isSaved
                          ? 'text-amber-500 hover:text-amber-600'
                          : 'text-slate-400 hover:text-slate-600 hover:bg-slate-100'
                      }`}
                    >
                      <Bookmark
                        className="w-4 h-4"
                        fill={isSaved ? 'currentColor' : 'none'}
                      />
                    </button>
                  </div>
                </div>

                <div className="mt-1.5 flex items-center gap-2">
                  <span className="text-[11px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-600 font-medium">
                    {item.pos}
                  </span>
                  <span className="text-xs font-semibold text-indigo-700">
                    {item.meaning}
                  </span>
                </div>

                <div className="mt-2.5 pt-2 border-t border-slate-200/60 text-xs space-y-1">
                  <p className="text-slate-700 italic">{item.exampleDe}</p>
                  <p className="text-slate-500">{item.exampleZh}</p>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* 底部 Anki 导出区（保持 pb-28 确保在所有屏幕下均绝不被底部悬浮胶囊覆盖） */}
      <div className="p-3 border-t border-slate-200/80 bg-slate-50/95 space-y-2 pb-28 select-none">
        <div className="text-[11px] text-slate-500 flex items-center justify-between font-medium">
          <span>Anki 制表符格式导出 (FSRS 兼容)</span>
          <span className="text-indigo-600 font-semibold">
            {activeTab === 'saved' && savedVocab.length > 0 ? '导出生词' : '导出本篇'}
          </span>
        </div>
        <div className="grid grid-cols-2 gap-2">
          <button
            onClick={handleCopyAnkiTsv}
            disabled={displayList.length === 0}
            className="py-2 px-3 rounded-lg bg-white hover:bg-slate-100 border border-slate-200 disabled:opacity-40 text-xs font-medium text-slate-700 inline-flex items-center justify-center gap-1.5 transition cursor-pointer shadow-2xs hover:shadow-xs active:scale-95"
          >
            {copied ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-600" />
                <span className="text-emerald-600 font-semibold">已复制 TSV</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5" />
                <span>复制 TSV</span>
              </>
            )}
          </button>

          <button
            onClick={handleDownloadAnkiTsv}
            disabled={displayList.length === 0}
            className="py-2 px-3 rounded-lg bg-indigo-600 hover:bg-indigo-700 disabled:opacity-40 text-xs font-semibold text-white inline-flex items-center justify-center gap-1.5 transition cursor-pointer shadow-xs hover:shadow-sm active:scale-95"
          >
            <Download className="w-3.5 h-3.5" />
            <span>下载 .tsv</span>
          </button>
        </div>
      </div>
    </aside>
  );
};
