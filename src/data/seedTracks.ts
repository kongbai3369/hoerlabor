import type { ListeningTrack } from '../types/listening';
import generatedTracksJson from './generatedTracks.json';

// Authentic Official Exam Corpus from Goethe-Institut & TestDaF
export const SEED_TRACKS: ListeningTrack[] = generatedTracksJson as ListeningTrack[];
