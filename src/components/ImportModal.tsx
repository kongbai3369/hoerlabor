import React, { useEffect, useState } from 'react';
import { X, PlusCircle, Link as LinkIcon } from 'lucide-react';
import type {
  CefrLevel,
  ListeningTrack,
  SentenceSegment,
  SourceCategory,
} from '../types/listening';
import { useListeningStore } from '../store/useListeningStore';

interface ImportModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ImportModal: React.FC<ImportModalProps> = ({ isOpen, onClose }) => {
  const { addCustomTrack } = useListeningStore();
  const [title, setTitle] = useState('');
  const [level, setLevel] = useState<CefrLevel>('B1');
  const [source, setSource] = useState('自定义德语精听');
  const [sourceCategory, setSourceCategory] = useState<SourceCategory>('custom');
  const [audioUrl, setAudioUrl] = useState('');
  const [rawGerman, setRawGerman] = useState('');
  const [rawChinese, setRawChinese] = useState('');

  useEffect(() => {
    if (!isOpen) return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !rawGerman.trim()) return;

    const rawSentences = rawGerman
      .split(/\n+|(?<=[.!?])\s+/)
      .map((s) => s.trim())
      .filter((s) => s.length > 3);

    const chineseLines = rawChinese
      .split(/\n+/)
      .map((s) => s.trim())
      .filter(Boolean);

    const cleanAudioUrl = audioUrl.trim() || null;
    const trackId = `custom-${Date.now()}`;
    const segments: SentenceSegment[] = rawSentences.map((sent, idx) => {
      const words = sent.match(/[A-Za-zÄÖÜäöüß]+(?:-[A-Za-zÄÖÜäöüß]+)*/g) || [];
      const clozeWords = Array.from(new Set(words.filter((w) => w.length >= 5))).slice(0, 3);
      return {
        id: `${trackId}-s${idx + 1}`,
        startTime: null,
        endTime: null,
        german: sent,
        chinese: chineseLines[idx] || '（自选导入语料 · 可配合盲听与听写模式练习）',
        clozeWords,
        vocab: [],
      };
    });

    const newTrack: ListeningTrack = {
      id: trackId,
      title: title.trim(),
      level,
      source: source.trim() || '自定义导入',
      sourceCategory,
      topic: '自主拓展精听',
      license: '自选导入',
      audioUrl: cleanAudioUrl,
      originalAudioUrl: cleanAudioUrl || undefined,
      duration: null,
      segments,
    };

    addCustomTrack(newTrack);
    setTitle('');
    setAudioUrl('');
    setRawGerman('');
    setRawChinese('');
    onClose();
  };

  return (
    <div
      onClick={onClose}
      className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4 animate-fade-in"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="bg-white border border-slate-200/90 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto p-6 shadow-2xl"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <PlusCircle className="w-5 h-5 text-indigo-600" />
            <span>导入自定义德语听力语料</span>
          </h3>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 cursor-pointer transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <form onSubmit={handleCreate} className="space-y-3.5">
          <div className="grid grid-cols-3 gap-3">
            <div className="col-span-2">
              <label className="block text-xs font-semibold text-slate-700 mb-1">曲目标题</label>
              <input
                type="text"
                required
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="例如：DW Top-Thema 或教材第 3 课"
                className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-300 text-sm text-slate-900 focus:bg-white focus:border-indigo-600 focus:ring-2 focus:ring-indigo-500/20 outline-none transition"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">欧标等级</label>
              <select
                value={level}
                onChange={(e) => setLevel(e.target.value as CefrLevel)}
                className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-300 text-sm text-slate-900 focus:bg-white focus:border-indigo-600 focus:ring-2 focus:ring-indigo-500/20 outline-none transition cursor-pointer"
              >
                <option value="A1">A1</option>
                <option value="A2">A2</option>
                <option value="B1">B1</option>
                <option value="B2">B2</option>
                <option value="C1">C1</option>
                <option value="TestDaF">TestDaF</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">来源名称</label>
              <input
                type="text"
                value={source}
                onChange={(e) => setSource(e.target.value)}
                placeholder="如 Slow German / Hueber"
                className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-300 text-sm text-slate-900 focus:bg-white focus:border-indigo-600 focus:ring-2 focus:ring-indigo-500/20 outline-none transition"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">分类板块</label>
              <select
                value={sourceCategory}
                onChange={(e) => setSourceCategory(e.target.value as SourceCategory)}
                className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-300 text-sm text-slate-900 focus:bg-white focus:border-indigo-600 focus:ring-2 focus:ring-indigo-500/20 outline-none transition cursor-pointer"
              >
                <option value="custom">自定义精听</option>
                <option value="news">新闻慢速</option>
                <option value="podcast">播客电台</option>
                <option value="exam">考级真题</option>
                <option value="authentic">母语口语</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1 flex items-center gap-1">
              <LinkIcon className="w-3.5 h-3.5 text-slate-400" />
              <span>外部 MP3 音频链接（可选；留空则按文本逐句朗读）</span>
            </label>
            <input
              type="url"
              value={audioUrl}
              onChange={(e) => setAudioUrl(e.target.value)}
              placeholder="https://... .mp3（支持直接填入 DW / 播客 / R2 外链）"
              className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-300 text-sm text-slate-900 focus:bg-white focus:border-indigo-600 focus:ring-2 focus:ring-indigo-500/20 outline-none transition"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              德语原文段落（按句号或换行自动拆句并生成听写挖空）
            </label>
            <textarea
              rows={4}
              required
              value={rawGerman}
              onChange={(e) => setRawGerman(e.target.value)}
              placeholder="在此粘贴德语听力原文，支持多句连段或每行一句..."
              className="w-full p-3 rounded-lg bg-slate-50 border border-slate-300 text-sm text-slate-900 focus:bg-white focus:border-indigo-600 focus:ring-2 focus:ring-indigo-500/20 outline-none leading-relaxed transition"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              中文译文对照（可选，每行对应一句）
            </label>
            <textarea
              rows={2}
              value={rawChinese}
              onChange={(e) => setRawChinese(e.target.value)}
              placeholder="可留空，或按行粘贴对应中文翻译..."
              className="w-full p-2.5 rounded-lg bg-slate-50 border border-slate-300 text-sm text-slate-900 focus:bg-white focus:border-indigo-600 focus:ring-2 focus:ring-indigo-500/20 outline-none leading-relaxed transition"
            />
          </div>

          <div className="flex justify-end gap-2 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-lg bg-slate-100 text-xs font-semibold text-slate-700 hover:bg-slate-200 cursor-pointer transition"
            >
              取消
            </button>
            <button
              type="submit"
              className="px-4 py-2 rounded-lg bg-indigo-600 text-xs font-bold text-white hover:bg-indigo-700 shadow-sm cursor-pointer transition active:scale-95"
            >
              生成精听与听写曲目
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
