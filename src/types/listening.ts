export type CefrLevel = 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'TestDaF';

export type DifficultyLevel = CefrLevel;

export type DisplayMode = 'blind' | 'de_only' | 'bilingual' | 'dictation';

export type EngineMode = 'audio' | 'tts';

export const LEVEL_BADGE_STYLE: Record<CefrLevel, string> = {
  A1: 'bg-emerald-50 text-emerald-700 border-emerald-300/80',
  A2: 'bg-teal-50 text-teal-700 border-teal-300/80',
  B1: 'bg-sky-50 text-sky-700 border-sky-300/80',
  B2: 'bg-indigo-50 text-indigo-700 border-indigo-300/80',
  C1: 'bg-purple-50 text-purple-700 border-purple-300/80',
  TestDaF: 'bg-amber-50 text-amber-800 border-amber-300/80',
};

export interface VocabItem {
  word: string;          // 原形，名词带冠词如 "der Balkon"
  plural?: string;       // 名词复数形式，如 "die Balkone"
  pos: string;           // 词性：Nomen, Verb, Adjektiv 等
  meaning: string;       // 中文释义
  exampleDe: string;     // 原句例句
  exampleZh: string;     // 例句翻译
}

export interface SentenceSegment {
  id: string;
  startTime: number | null; // 纯 TTS 模式下为 null；MP3 模式下为秒数（如 0.0）
  endTime: number | null;   // 纯 TTS 模式下为 null；MP3 模式下为秒数（如 4.5）
  german: string;           // 德语原句
  chinese: string;          // 中文对照翻译
  clozeWords: string[];     // 听写模式下挖空的核心词（区分大小写）
  vocab?: VocabItem[];      // 该句包含的重点词汇
}

export interface ListeningTrack {
  id: string;
  title: string;
  level: CefrLevel;
  source: string;           // 来源标识，如 "DW", "Goethe-Institut", "Slow German", "ZDF", "Quarks Daily"
  topic: string;            // 话题分类
  audioUrl: string | null;  // 为 null 时路由至 TTS 引擎；非空时路由至 HTML5 Audio 引擎
  originalAudioUrl?: string; // 官方原版播客/广播完整流媒体音频链接
  duration: number | null;  // 纯 TTS 模式下为 null；MP3 模式下为总时长（秒）
  segments: SentenceSegment[];
}
