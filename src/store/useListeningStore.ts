import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { CefrLevel, DisplayMode, ListeningTrack, VocabItem } from '../types/listening';
import { SEED_TRACKS } from '../data/seedTracks';
import generatedTracksJson from '../data/generatedTracks.json';

const GENERATED_TRACKS = generatedTracksJson as ListeningTrack[];

const CEFR_ORDER: Record<CefrLevel, number> = {
  A1: 1,
  A2: 2,
  B1: 3,
  B2: 4,
  C1: 5,
  TestDaF: 6,
};

export function mergeAllTracks(customTracks: ListeningTrack[]): ListeningTrack[] {
  const trackMap = new Map<string, ListeningTrack>();
  SEED_TRACKS.forEach((t) => trackMap.set(t.id, t));
  GENERATED_TRACKS.forEach((t) => trackMap.set(t.id, t));
  customTracks.forEach((t) => trackMap.set(t.id, t));
  const tracks = Array.from(trackMap.values());
  return tracks.sort((a, b) => {
    const orderDiff = (CEFR_ORDER[a.level] || 99) - (CEFR_ORDER[b.level] || 99);
    if (orderDiff !== 0) return orderDiff;
    return a.id.localeCompare(b.id);
  });
}

interface ListeningState {
  selectedLevel: CefrLevel | 'ALL';
  currentTrackId: string;
  displayMode: DisplayMode;
  savedVocab: VocabItem[];
  customTracks: ListeningTrack[];
  starredSegmentIds: string[];
  autoPauseSeconds: number;
  isWordLookupActive: boolean;
  dictationInputs: Record<string, string>;
  setSelectedLevel: (level: CefrLevel | 'ALL') => void;
  setCurrentTrackId: (id: string) => void;
  setDisplayMode: (mode: DisplayMode) => void;
  setAutoPauseSeconds: (sec: number) => void;
  setIsWordLookupActive: (active: boolean) => void;
  toggleWordLookup: () => void;
  toggleStarSegment: (segmentId: string) => void;
  setDictationInput: (key: string, value: string) => void;
  clearTrackDictation: (trackId: string) => void;
  toggleSaveVocab: (item: VocabItem) => void;
  addCustomTrack: (track: ListeningTrack) => void;
  exportBackupJson: () => string;
  importBackupJson: (rawJson: string) => boolean;
}

export const useListeningStore = create<ListeningState>()(
  persist(
    (set, get) => ({
      selectedLevel: 'ALL',
      currentTrackId: SEED_TRACKS[0].id,
      displayMode: 'bilingual',
      savedVocab: [],
      customTracks: [],
      starredSegmentIds: [],
      autoPauseSeconds: 0,
      isWordLookupActive: false,
      dictationInputs: {},

      setSelectedLevel: (level) => set({ selectedLevel: level }),
      setCurrentTrackId: (id) => set({ currentTrackId: id }),
      setDisplayMode: (mode) => set({ displayMode: mode }),
      setAutoPauseSeconds: (sec) => set({ autoPauseSeconds: sec }),
      setIsWordLookupActive: (active) => set({ isWordLookupActive: active }),
      toggleWordLookup: () => set((state) => ({ isWordLookupActive: !state.isWordLookupActive })),

      toggleStarSegment: (segmentId) =>
        set((state) => {
          const exists = state.starredSegmentIds.includes(segmentId);
          return {
            starredSegmentIds: exists
              ? state.starredSegmentIds.filter((id) => id !== segmentId)
              : [...state.starredSegmentIds, segmentId],
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

      exportBackupJson: () => {
        const state = get();
        return JSON.stringify(
          {
            savedVocab: state.savedVocab,
            customTracks: state.customTracks,
            starredSegmentIds: state.starredSegmentIds,
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
      name: 'de-listening-storage-v1',
    }
  )
);
