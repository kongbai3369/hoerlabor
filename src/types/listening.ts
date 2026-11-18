export type CefrLevel = 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'TestDaF';

export type DifficultyLevel = CefrLevel;

export type DisplayMode = 'blind' | 'de_only' | 'bilingual' | 'dictation';

export type EngineMode = 'audio' | 'tts';

export type SourceCategory = 'exam' | 'news' | 'podcast' | 'authentic' | 'custom';

export const LEVEL_BADGE_STYLE: Record<CefrLevel, string> = {
  A1: 'bg-emerald-50 text-emerald-700 border-emerald-300/80',
  A2: 'bg-teal-50 text-teal-700 border-teal-300/80',
  B1: 'bg-sky-50 text-sky-700 border-sky-300/80',
  B2: 'bg-indigo-50 text-indigo-700 border-indigo-300/80',
  C1: 'bg-purple-50 text-purple-700 border-purple-300/80',
  TestDaF: 'bg-amber-50 text-amber-800 border-amber-300/80',
};

export const SOURCE_CATEGORY_META: Record<
  SourceCategory,
  { label: string; emoji: string }
> = {
  exam: { label: '考级真题', emoji: '🏛️' },
  news: { label: '慢速新闻', emoji: '📰' },
  podcast: { label: '播客电台', emoji: '🎙️' },
  authentic: { label: '母语口语', emoji: '🗣️' },
  custom: { label: '自定义', emoji: '✍️' },
};

export interface SourceDisplayInfo {
  label: string;
  shortLabel: string;
  category: SourceCategory;
  badgeClass: string;
  iconKey: 'award' | 'graduation' | 'newspaper' | 'radio' | 'mic' | 'podcast' | 'user';
}

export function getSourceDisplayInfo(
  trackOrSource: Pick<ListeningTrack, 'source' | 'sourceCategory'>
): SourceDisplayInfo {
  const src = (trackOrSource.source || '').trim();
  const sLower = src.toLowerCase();

  if (src === 'Goethe-Institut' || sLower.includes('goethe')) {
    return {
      label: '歌德学院官网真题',
      shortLabel: '歌德真题',
      category: trackOrSource.sourceCategory || 'exam',
      badgeClass: 'bg-emerald-50 text-emerald-800 border-emerald-300',
      iconKey: 'award',
    };
  }
  if (src === 'TestDaF' || sLower.includes('testdaf')) {
    return {
      label: '德福官网官方真题',
      shortLabel: '德福真题',
      category: trackOrSource.sourceCategory || 'exam',
      badgeClass: 'bg-amber-50 text-amber-900 border-amber-300',
      iconKey: 'graduation',
    };
  }
  if (sLower.includes('telc')) {
    return {
      label: 'telc 官方真题',
      shortLabel: 'telc 真题',
      category: trackOrSource.sourceCategory || 'exam',
      badgeClass: 'bg-cyan-50 text-cyan-800 border-cyan-300',
      iconKey: 'award',
    };
  }
  if (sLower.includes('ösd') || sLower.includes('osd')) {
    return {
      label: 'ÖSD 奥地利真题',
      shortLabel: 'ÖSD 真题',
      category: trackOrSource.sourceCategory || 'exam',
      badgeClass: 'bg-rose-50 text-rose-800 border-rose-300',
      iconKey: 'award',
    };
  }
  if (sLower.includes('dsh')) {
    return {
      label: 'DSH 高校入学真题',
      shortLabel: 'DSH 真题',
      category: trackOrSource.sourceCategory || 'exam',
      badgeClass: 'bg-orange-50 text-orange-800 border-orange-300',
      iconKey: 'graduation',
    };
  }
  if (sLower.includes('nachrichtenleicht')) {
    return {
      label: 'Nachrichtenleicht 简明新闻',
      shortLabel: '简明新闻',
      category: trackOrSource.sourceCategory || 'news',
      badgeClass: 'bg-sky-50 text-sky-800 border-sky-300',
      iconKey: 'newspaper',
    };
  }
  if (src === 'DW' || sLower.includes('dw ') || sLower.includes('deutsche welle')) {
    return {
      label: src.length > 3 ? src : 'DW 德国之声',
      shortLabel: sLower.includes('langsam') ? 'DW 慢速新闻' : 'DW 德国之声',
      category: trackOrSource.sourceCategory || 'news',
      badgeClass: 'bg-blue-50 text-blue-800 border-blue-300',
      iconKey: 'radio',
    };
  }
  if (sLower.includes('tagesschau')) {
    return {
      label: 'Tagesschau 简明新闻',
      shortLabel: 'Tagesschau',
      category: trackOrSource.sourceCategory || 'news',
      badgeClass: 'bg-indigo-50 text-indigo-800 border-indigo-300',
      iconKey: 'newspaper',
    };
  }
  if (sLower.includes('slow german')) {
    return {
      label: 'Slow German 慢速播客',
      shortLabel: 'Slow German',
      category: trackOrSource.sourceCategory || 'podcast',
      badgeClass: 'bg-purple-50 text-purple-800 border-purple-300',
      iconKey: 'podcast',
    };
  }
  if (sLower.includes('deutschlandfunk') || sLower === 'dlf') {
    return {
      label: 'Deutschlandfunk 电台',
      shortLabel: 'DLF 广播',
      category: trackOrSource.sourceCategory || 'podcast',
      badgeClass: 'bg-slate-100 text-slate-800 border-slate-300',
      iconKey: 'radio',
    };
  }
  if (sLower.includes('audio-lingua') || sLower.includes('audio lingua')) {
    return {
      label: 'Audio-Lingua 母语口语',
      shortLabel: 'Audio-Lingua',
      category: trackOrSource.sourceCategory || 'authentic',
      badgeClass: 'bg-teal-50 text-teal-800 border-teal-300',
      iconKey: 'mic',
    };
  }

  return {
    label: src || '自定义语料',
    shortLabel: src || '自定义',
    category: trackOrSource.sourceCategory || 'custom',
    badgeClass: 'bg-slate-100 text-slate-700 border-slate-300',
    iconKey: 'user',
  };
}

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
  source: string;              // 来源标识，如 "Goethe-Institut", "TestDaF", "Nachrichtenleicht", "Slow German", "DW Deutsch Lernen", "Audio-Lingua"
  sourceCategory?: SourceCategory;
  topic: string;               // 话题分类
  taskSection?: string;        // 考点/题型/栏目副标签，如 "歌德 B1 · Teil 1" 或 "SG 327 · Alltag"
  license?: string;            // 许可信息，如 "官方样题", "CC BY-NC", "公开广播"
  sourceExam?: string;         // 备用考试名称字段
  audioUrl: string | null;     // 为 null 时路由至 TTS 引擎；非空时路由至 HTML5 Audio 引擎
  originalAudioUrl?: string;   // 官方原版完整音频外链
  originalPageUrl?: string;    // 原始出处文章页链接
  duration: number | null;     // 纯 TTS 模式下为 null；MP3 模式下为总时长（秒）
  segments: SentenceSegment[];
}
