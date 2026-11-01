import React, { useEffect, useMemo, useState } from 'react';
import { Library, Headphones, BookMarked } from 'lucide-react';
import { mergeAllTracks, useListeningStore } from './store/useListeningStore';
import { useAudioPlayer } from './hooks/useAudioPlayer';
import { Sidebar } from './components/Sidebar';
import { TranscriptView } from './components/TranscriptView';
import { VocabPanel } from './components/VocabPanel';
import { PlayerBar } from './components/PlayerBar';

export const App: React.FC = () => {
  const { currentTrackId, customTracks, savedVocab } = useListeningStore();
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

      {/* 底部播放条：桌面端为居中悬浮胶囊，移动端为 56px 迷你条 */}
      <PlayerBar track={currentTrack} player={player} />

      {/* 移动端原生 iOS 风格底部导航栏 (Bottom Tab Bar) */}
      <nav className="lg:hidden fixed bottom-0 left-0 right-0 h-[calc(3.5rem+env(safe-area-inset-bottom,0px))] pb-[env(safe-area-inset-bottom,0px)] bg-white/95 backdrop-blur-md border-t border-slate-200/90 z-40 select-none flex items-center justify-around px-3 shadow-[0_-2px_12px_rgba(15,23,42,0.04)]">
        <button
          onClick={() => setMobilePane('tracks')}
          className={`flex-1 flex flex-col items-center justify-center gap-1 py-1 transition cursor-pointer ${
            mobilePane === 'tracks'
              ? 'text-indigo-600 font-bold'
              : 'text-slate-400 hover:text-slate-600 font-medium'
          }`}
        >
          <div className="relative">
            <Library className="w-5 h-5" />
            <span className="absolute -top-1 -right-2 bg-slate-100 text-slate-500 text-[9px] font-bold px-1 rounded-full border border-slate-200">
              {allTracks.length}
            </span>
          </div>
          <span className="text-[10px] leading-none">曲库</span>
        </button>

        <button
          onClick={() => setMobilePane('listen')}
          className={`flex-1 flex flex-col items-center justify-center gap-1 py-1 transition cursor-pointer ${
            mobilePane === 'listen'
              ? 'text-indigo-600 font-bold'
              : 'text-slate-400 hover:text-slate-600 font-medium'
          }`}
        >
          <Headphones className="w-5 h-5" />
          <span className="text-[10px] leading-none">精听</span>
        </button>

        <button
          onClick={() => setMobilePane('vocab')}
          className={`flex-1 flex flex-col items-center justify-center gap-1 py-1 transition cursor-pointer ${
            mobilePane === 'vocab'
              ? 'text-indigo-600 font-bold'
              : 'text-slate-400 hover:text-slate-600 font-medium'
          }`}
        >
          <div className="relative">
            <BookMarked className="w-5 h-5" />
            {savedVocab.length > 0 && (
              <span className="absolute -top-1 -right-2 bg-amber-500 text-white text-[9px] font-bold px-1 rounded-full">
                {savedVocab.length}
              </span>
            )}
          </div>
          <span className="text-[10px] leading-none">核心词</span>
        </button>
      </nav>
    </div>
  );
};

export default App;
