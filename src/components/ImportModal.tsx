import React, { useEffect, useState } from 'react';
import { X, PlusCircle } from 'lucide-react';
import type { CefrLevel, ListeningTrack, SentenceSegment } from '../types/listening';
import { useListeningStore } from '../store/useListeningStore';

interface ImportModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ImportModal: React.FC<ImportModalProps> = ({ isOpen, onClose }) => {
  const { addCustomTrack } = useListeningStore();
  const [title, setTitle] = useState('');
  const [level, setLevel] = useState<CefrLevel>('B1');
  const [source, setSource] = useState('Audio Lingua 自选导入');
  const [rawGerman, setRawGerman] = useState('');

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
      .split(/(?<=[.!?])\s+/)
      .map((s) => s.trim())
      .filter((s) => s.length > 3);

    const trackId = `custom-${Date.now()}`;
    const segments: SentenceSegment[] = rawSentences.map((sent, idx) => {
      const words = sent.match(/[A-Za-zÄÖÜäöüß]{5,}/g) || [];
      const clozeWords = Array.from(new Set(words)).slice(0, 2);
      return {
        id: `${trackId}-s${idx + 1}`,
        startTime: null,
        endTime: null,
        german: sent,
        chinese: '（自选导入语料 · 可配合盲听与听写模式练习）',
        clozeWords,
        vocab: [],
      };
    });

    const newTrack: ListeningTrack = {
      id: trackId,
      title: title.trim(),
      level,
      source: source.trim() || '自定义导入',
      topic: '自主拓展精听',
      audioUrl: null,
      duration: null,
      segments,
    };

    addCustomTrack(newTrack);
    setTitle('');
    setRawGerman('');
    onClose();
  };

  return (
    <div
      onClick={onClose}
      className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4 animate-fade-in"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="bg-white border border-slate-200/90 rounded-2xl w-full max-w-lg p-6 shadow-2xl"
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

        <form onSubmit={handleCreate} className="space-y-4">
          <div className="grid grid-cols-3 gap-3">
            <div className="col-span-2">
              <label className="block text-xs font-semibold text-slate-700 mb-1">曲目标题</label>
              <input
                type="text"
                required
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="例如：Audio Lingua - Studium in München"
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

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">来源标识</label>
            <input
              type="text"
              value={source}
              onChange={(e) => setSource(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-300 text-sm text-slate-900 focus:bg-white focus:border-indigo-600 focus:ring-2 focus:ring-indigo-500/20 outline-none transition"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              德语原文段落（系统将自动切分句子并生成听写挖空）
            </label>
            <textarea
              rows={5}
              required
              value={rawGerman}
              onChange={(e) => setRawGerman(e.target.value)}
              placeholder="在此粘贴德语听力原文，支持多句连段..."
              className="w-full p-3 rounded-lg bg-slate-50 border border-slate-300 text-sm text-slate-900 focus:bg-white focus:border-indigo-600 focus:ring-2 focus:ring-indigo-500/20 outline-none leading-relaxed transition"
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
