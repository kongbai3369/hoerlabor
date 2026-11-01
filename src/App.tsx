import React, { useEffect, useMemo, useState } from 'react';
import { Library, Headphones, BookMarked } from 'lucide-react';
import { mergeAllTracks, useListeningStore } from './store/useListeningStore';
import { useAudioPlayer } from './hooks/useAudioPlayer';
import { Sidebar } from './components/Sidebar';
import { TranscriptView } from './components/TranscriptView';
import { VocabPanel } from './components/VocabPanel';
import { PlayerBar } from './components/PlayerBar';

export const App: React.FC = () => {
  const { currentTrackId, customTracks } = useListeningStore();
  const [mobilePane, setMobilePane] = useState<'tracks' | 'listen' | 'vocab'>('listen');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isVocabOpen, setIsVocabOpen] = useState(true);

  const allTracks = useMemo(() => mergeAllTracks(customTracks), [customTracks]);

  const currentTrack = useMemo(() => {
    return allTracks.find((t) => t.id === currentTrackId) || allTracks[0];
  }, [allTracks, currentTrackId]);

  const player = useAudioPlayer(currentTrack);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null;
      if (
        target &&
        (target.tagName === 'INPUT' ||
          target.tagName === 'TEXTAREA' ||
          target.isContentEditable)
      ) {
        return;
      }

      if (e.code === 'Space') {
        e.preventDefault();
        player.togglePlay();
      } else if (e.code === 'ArrowLeft') {
        e.preventDefault();
        player.prevSegment();
      } else if (e.code === 'ArrowRight') {
        e.preventDefault();
        player.nextSegment();
      } else if (e.code === 'KeyL') {
        e.preventDefault();
        player.toggleLoopSentence();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [player]);

  return (
    <div className="h-screen w-screen overflow-hidden flex flex-col bg-slate-50 text-slate-900 selection:bg-indigo-100 selection:text-indigo-900 font-sans">
      {/* 移动端与平板顶部切换栏（仅在小于 lg 屏幕时显示） */}
      <div className="lg:hidden flex items-center bg-white border-b border-slate-200/90 px-3 py-2 gap-2 shrink-0 shadow-xs z-20">
        <button
          onClick={() => setMobilePane('tracks')}
          className={`flex-1 py-1.5 rounded-lg text-xs font-semibold inline-flex items-center justify-center gap-1.5 transition cursor-pointer ${
            mobilePane === 'tracks'
              ? 'bg-indigo-600 text-white shadow-xs font-bold'
              : 'bg-slate-100 text-slate-600 hover:text-slate-900 hover:bg-slate-200/80'
          }`}
        >
          <Library className="w-3.5 h-3.5" />
          <span>曲库 ({allTracks.length})</span>
        </button>
        <button
          onClick={() => setMobilePane('listen')}
          className={`flex-1 py-1.5 rounded-lg text-xs font-semibold inline-flex items-center justify-center gap-1.5 transition cursor-pointer ${
            mobilePane === 'listen'
              ? 'bg-indigo-600 text-white shadow-xs font-bold'
              : 'bg-slate-100 text-slate-600 hover:text-slate-900 hover:bg-slate-200/80'
          }`}
        >
          <Headphones className="w-3.5 h-3.5" />
          <span>精听训练</span>
        </button>
        <button
          onClick={() => setMobilePane('vocab')}
          className={`flex-1 py-1.5 rounded-lg text-xs font-semibold inline-flex items-center justify-center gap-1.5 transition cursor-pointer ${
            mobilePane === 'vocab'
              ? 'bg-indigo-600 text-white shadow-xs font-bold'
              : 'bg-slate-100 text-slate-600 hover:text-slate-900 hover:bg-slate-200/80'
          }`}
        >
          <BookMarked className="w-3.5 h-3.5" />
          <span>词汇与Anki</span>
        </button>
      </div>

      {/* 主体三栏：桌面端支持切换侧栏展开折叠，移动端按标签切换 */}
      <div className="flex-1 flex overflow-hidden relative">
        <div
          className={`${
            mobilePane === 'tracks' ? 'flex w-full' : 'hidden'
          } ${isSidebarOpen ? 'lg:flex lg:w-80' : 'lg:hidden'} h-full shrink-0`}
        >
          <Sidebar onSelectTrack={() => setMobilePane('listen')} />
        </div>

        <div
          className={`${
            mobilePane === 'listen' ? 'flex flex-1' : 'hidden'
          } lg:flex lg:flex-1 h-full min-w-0`}
        >
          <TranscriptView
            key={currentTrack.id}
            track={currentTrack}
            player={player}
            isSidebarOpen={isSidebarOpen}
            onToggleSidebar={() => setIsSidebarOpen((prev) => !prev)}
            isVocabOpen={isVocabOpen}
            onToggleVocab={() => setIsVocabOpen((prev) => !prev)}
          />
        </div>

        <div
          className={`${
            mobilePane === 'vocab' ? 'flex w-full' : 'hidden'
          } ${isVocabOpen ? 'lg:flex lg:w-80' : 'lg:hidden'} h-full shrink-0`}
        >
          <VocabPanel
            track={currentTrack}
            activeSegmentIndex={player.activeSegmentIndex}
          />
        </div>
      </div>

      <PlayerBar track={currentTrack} player={player} />
    </div>
  );
};

export default App;
