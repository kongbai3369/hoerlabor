import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type {
  CefrLevel,
  DisplayMode,
  ListeningTrack,
  SourceCategory,
  VocabItem,
} from '../types/listening';
import { getSourceDisplayInfo } from '../types/listening';
import { SEED_TRACKS } from '../data/seedTracks';

const CEFR_ORDER: Record<CefrLevel, number> = {
  A1: 1,
  A2: 2,
  B1: 3,
  B2: 4,
  C1: 5,
  TestDaF: 6,
};

export interface DictationScore {
  correct: number;
  total: number;
}

export interface TrackListItem extends ListeningTrack {
  segmentCount?: number;
  isCatalogStub?: boolean;
}

export function mergeAllTracks(
  customTracks: ListeningTrack[],
  remoteTracks: TrackListItem[] = [],
  loadedDetails: Record<string, ListeningTrack> = {}
): TrackListItem[] {
  const trackMap = new Map<string, TrackListItem>();

  SEED_TRACKS.forEach((t) =>
    trackMap.set(t.id, {
      ...t,
      sourceCategory: t.sourceCategory || getSourceDisplayInfo(t).category,
      segmentCount: t.segments.length,
    })
  );

  remoteTracks.forEach((t) => {
    const detailed = loadedDetails[t.id];
    const base = detailed ? { ...detailed, segmentCount: detailed.segments.length } : t;
    trackMap.set(t.id, {
      ...base,
      sourceCategory: base.sourceCategory || getSourceDisplayInfo(base).category,
      segmentCount: base.segmentCount ?? base.segments?.length ?? 0,
    });
  });

  customTracks.forEach((t) =>
    trackMap.set(t.id, {
      ...t,
      sourceCategory: t.sourceCategory || getSourceDisplayInfo(t).category,
      segmentCount: t.segments.length,
    })
  );

  const tracks = Array.from(trackMap.values());
  return tracks.sort((a, b) => {
    const orderDiff = (CEFR_ORDER[a.level] || 99) - (CEFR_ORDER[b.level] || 99);
    if (orderDiff !== 0) return orderDiff;
    return a.id.localeCompare(b.id);
  });
}

interface ListeningState {
  selectedLevel: CefrLevel | 'ALL';
  selectedSourceCategory: SourceCategory | 'ALL';
  selectedSource: string | 'ALL';
  searchQuery: string;
  onlyUncompleted: boolean;
  currentTrackId: string;
  displayMode: DisplayMode;
  savedVocab: VocabItem[];
  customTracks: ListeningTrack[];
  starredSegmentIds: string[];
  completedTrackIds: string[];
  dictationScores: Record<string, DictationScore>;
  autoPauseSeconds: number;
  isWordLookupActive: boolean;
  dictationInputs: Record<string, string>;

  // 运行时异步目录与按需详情缓存（不写入 localStorage）
  remoteCatalog: TrackListItem[];
  loadedTrackDetails: Record<string, ListeningTrack>;
  loadingTrackId: string | null;

  setSelectedLevel: (level: CefrLevel | 'ALL') => void;
  setSelectedSourceCategory: (category: SourceCategory | 'ALL') => void;
  setSelectedSource: (source: string | 'ALL') => void;
  setSearchQuery: (q: string) => void;
  setOnlyUncompleted: (flag: boolean) => void;
  resetFilters: () => void;
  setCurrentTrackId: (id: string) => void;
  setDisplayMode: (mode: DisplayMode) => void;
  setAutoPauseSeconds: (sec: number) => void;
  setIsWordLookupActive: (active: boolean) => void;
  toggleWordLookup: () => void;
  toggleStarSegment: (segmentId: string) => void;
  markTrackCompleted: (trackId: string) => void;
  saveDictationScore: (trackId: string, correct: number, total: number) => void;
  setDictationInput: (key: string, value: string) => void;
  clearTrackDictation: (trackId: string) => void;
  toggleSaveVocab: (item: VocabItem) => void;
  addCustomTrack: (track: ListeningTrack) => void;
  deleteCustomTrack: (trackId: string) => void;
  loadRemoteCatalog: () => Promise<void>;
  ensureTrackDetail: (trackId: string) => Promise<void>;
  exportBackupJson: () => string;
  importBackupJson: (rawJson: string) => boolean;
}

export const useListeningStore = create<ListeningState>()(
  persist(
    (set, get) => ({
      selectedLevel: 'ALL',
      selectedSourceCategory: 'ALL',
      selectedSource: 'ALL',
      searchQuery: '',
      onlyUncompleted: false,
      currentTrackId: SEED_TRACKS[0]?.id || '',
      displayMode: 'bilingual',
      savedVocab: [],
      customTracks: [],
      starredSegmentIds: [],
      completedTrackIds: [],
      dictationScores: {},
      autoPauseSeconds: 0,
      isWordLookupActive: false,
      dictationInputs: {},

      remoteCatalog: [],
      loadedTrackDetails: {},
      loadingTrackId: null,

      setSelectedLevel: (level) => set({ selectedLevel: level }),
      setSelectedSourceCategory: (category) =>
        set({ selectedSourceCategory: category, selectedSource: 'ALL' }),
      setSelectedSource: (source) => set({ selectedSource: source }),
      setSearchQuery: (searchQuery) => set({ searchQuery }),
      setOnlyUncompleted: (onlyUncompleted) => set({ onlyUncompleted }),
      resetFilters: () =>
        set({
          selectedLevel: 'ALL',
          selectedSourceCategory: 'ALL',
          selectedSource: 'ALL',
          searchQuery: '',
          onlyUncompleted: false,
        }),
      setCurrentTrackId: (id) => set({ currentTrackId: id }),
      setDisplayMode: (mode) => set({ displayMode: mode }),
      setAutoPauseSeconds: (sec) => set({ autoPauseSeconds: sec }),
      setIsWordLookupActive: (active) => set({ isWordLookupActive: active }),
      toggleWordLookup: () =>
        set((state) => ({ isWordLookupActive: !state.isWordLookupActive })),

      toggleStarSegment: (segmentId) =>
        set((state) => {
          const exists = state.starredSegmentIds.includes(segmentId);
          return {
            starredSegmentIds: exists
              ? state.starredSegmentIds.filter((id) => id !== segmentId)
              : [...state.starredSegmentIds, segmentId],
          };
        }),

      markTrackCompleted: (trackId) =>
        set((state) => {
          if (!trackId || state.completedTrackIds.includes(trackId)) return state;
          return {
            completedTrackIds: [...state.completedTrackIds, trackId],
          };
        }),

      saveDictationScore: (trackId, correct, total) =>
        set((state) => {
          const prev = state.dictationScores[trackId];
          if (prev && prev.correct === correct && prev.total === total) return state;
          return {
            dictationScores: {
              ...state.dictationScores,
              [trackId]: { correct, total },
            },
          };
        }),

      setDictationInput: (key, value) =>
        set((state) => ({
          dictationInputs: {
            ...state.dictationInputs,
            [key]: value,
          },
        })),

      clearTrackDictation: (trackId) =>
        set((state) => {
          const next = { ...state.dictationInputs };
          Object.keys(next).forEach((k) => {
            if (k.startsWith(`${trackId}:`)) {
              delete next[k];
            }
          });
          return { dictationInputs: next };
        }),

      toggleSaveVocab: (item) =>
        set((state) => {
          const exists = state.savedVocab.some((v) => v.word === item.word);
          return {
            savedVocab: exists
              ? state.savedVocab.filter((v) => v.word !== item.word)
              : [...state.savedVocab, item],
          };
        }),

      addCustomTrack: (track) =>
        set((state) => ({
          customTracks: [track, ...state.customTracks],
          currentTrackId: track.id,
        })),

      deleteCustomTrack: (trackId) =>
        set((state) => ({
          customTracks: state.customTracks.filter((t) => t.id !== trackId),
        })),

      loadRemoteCatalog: async () => {
        try {
          const res = await fetch('/data/catalog.json', { cache: 'no-cache' });
          if (!res.ok) return;
          const items = (await res.json()) as TrackListItem[];
          if (Array.isArray(items)) {
            set({
              remoteCatalog: items.map((item) => ({
                ...item,
                segments: item.segments || [],
                isCatalogStub: !item.segments || item.segments.length === 0,
              })),
            });
          }
        } catch {
          // 离线或无扩展目录时静默降级至内嵌语料
        }
      },

      ensureTrackDetail: async (trackId) => {
        const state = get();
        if (!trackId) return;
        if (state.loadedTrackDetails[trackId]) return;
        const inSeed = SEED_TRACKS.some((t) => t.id === trackId);
        const inCustom = state.customTracks.some((t) => t.id === trackId);
        if (inSeed || inCustom) return;

        const stub = state.remoteCatalog.find((t) => t.id === trackId);
        if (stub && stub.segments && stub.segments.length > 0) {
          set((s) => ({
            loadedTrackDetails: { ...s.loadedTrackDetails, [trackId]: stub },
          }));
          return;
        }

        set({ loadingTrackId: trackId });
        try {
          const res = await fetch(`/data/tracks/${encodeURIComponent(trackId)}.json`);
          if (res.ok) {
            const detail = (await res.json()) as ListeningTrack;
            set((s) => ({
              loadedTrackDetails: { ...s.loadedTrackDetails, [trackId]: detail },
              loadingTrackId: s.loadingTrackId === trackId ? null : s.loadingTrackId,
            }));
            return;
          }
        } catch {
          // ignore
        }
        set((s) => ({
          loadingTrackId: s.loadingTrackId === trackId ? null : s.loadingTrackId,
        }));
      },

      exportBackupJson: () => {
        const state = get();
        return JSON.stringify(
          {
            savedVocab: state.savedVocab,
            customTracks: state.customTracks,
            starredSegmentIds: state.starredSegmentIds,
            completedTrackIds: state.completedTrackIds,
            dictationScores: state.dictationScores,
            dictationInputs: state.dictationInputs,
          },
          null,
          2
        );
      },

      importBackupJson: (rawJson) => {
        try {
          const data = JSON.parse(rawJson);
          set((state) => ({
            savedVocab: Array.isArray(data.savedVocab) ? data.savedVocab : state.savedVocab,
            customTracks: Array.isArray(data.customTracks) ? data.customTracks : state.customTracks,
            starredSegmentIds: Array.isArray(data.starredSegmentIds)
              ? data.starredSegmentIds
              : state.starredSegmentIds,
            completedTrackIds: Array.isArray(data.completedTrackIds)
              ? data.completedTrackIds
              : state.completedTrackIds,
            dictationScores:
              data.dictationScores && typeof data.dictationScores === 'object'
                ? data.dictationScores
                : state.dictationScores,
            dictationInputs:
              data.dictationInputs && typeof data.dictationInputs === 'object'
                ? data.dictationInputs
                : state.dictationInputs,
          }));
          return true;
        } catch {
          return false;
        }
      },
    }),
    {
      name: 'de-listening-storage-v3',
      partialize: (state) => ({
        selectedLevel: state.selectedLevel,
        selectedSourceCategory: state.selectedSourceCategory,
        selectedSource: state.selectedSource,
        currentTrackId: state.currentTrackId,
        displayMode: state.displayMode,
        savedVocab: state.savedVocab,
        customTracks: state.customTracks,
        starredSegmentIds: state.starredSegmentIds,
        completedTrackIds: state.completedTrackIds,
        dictationScores: state.dictationScores,
        autoPauseSeconds: state.autoPauseSeconds,
        isWordLookupActive: state.isWordLookupActive,
        dictationInputs: state.dictationInputs,
      }),
    }
  )
);
