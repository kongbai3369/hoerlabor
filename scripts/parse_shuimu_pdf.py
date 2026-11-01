import json
import re
from pathlib import Path
from pypdf import PdfReader

DOWNLOADS_DIR = Path(r"c:\Users\king\Downloads")
PROJECT_DIR = Path(r"c:\Users\king\Downloads\听力")
OUTPUT_JSON = PROJECT_DIR / "src" / "data" / "generatedTracks.json"

PDF_FILES = [
    ("A1", DOWNLOADS_DIR / "水木德语 A1讲义.pdf"),
    ("A2", DOWNLOADS_DIR / "水木德语 A2讲义.pdf"),
    ("B1", DOWNLOADS_DIR / "水木德语 B1讲义.pdf"),
    ("B2", DOWNLOADS_DIR / "水木德语 B2讲义.pdf"),
]

# 匹配包含典型德语词汇/变音字符的完整句子
GERMAN_SENTENCE_RE = re.compile(
    r"([A-ZÄÖÜ][a-zäöüßA-ZÄÖÜ0-9\s,\-–—]{15,120}[.!?])"
)
# 匹配中文翻译行
CHINESE_RE = re.compile(r"([\u4e00-\u9fa5][\u4e00-\u9fa5，。！？；：、（）a-zA-Z0-9\s]{4,80})")
# 匹配带定冠词的德语名词条目，例如 der Balkon / die Wohnung / das Zimmer
NOUN_VOCAB_RE = re.compile(
    r"\b(der|die|das)\s+([A-ZÄÖÜ][a-zäöüß]{2,20})\b"
)

STOP_WORDS = {
    "und", "oder", "aber", "nicht", "ich", "du", "er", "sie", "es", "wir",
    "ihr", "Sie", "ist", "sind", "war", "hat", "haben", "in", "im", "an",
    "auf", "mit", "von", "zu", "zum", "zur", "für", "ein", "eine", "der",
    "die", "das", "den", "dem", "des", "auch", "noch", "schon", "sehr"
}


def pick_cloze_words(sentence: str) -> list[str]:
    words = re.findall(r"[A-Za-zÄÖÜäöüß]+", sentence)
    candidates = [
        w for w in words
        if len(w) >= 4 and w.lower() not in STOP_WORDS
    ]
    # 优先选首字母大写的名词或较长的实词，最多挖空 3 个词
    candidates.sort(key=lambda w: (w[0].isupper(), len(w)), reverse=True)
    selected = []
    for w in candidates:
        if w not in selected:
            selected.append(w)
        if len(selected) >= 3:
            break
    return selected


def inspect_and_extract_pdf(level: str, pdf_path: Path) -> list[dict]:
    if not pdf_path.exists():
        print(f"[跳过] 未找到文件: {pdf_path}")
        return []

    reader = PdfReader(str(pdf_path))
    total_pages = len(reader.pages)
    print(f"\n=== 正在解析 {pdf_path.name} (共 {total_pages} 页) ===")

    extracted_pairs = []
    sample_logged = False

    # 扫描前 40 页提取高质量德中对照例句
    scan_limit = min(total_pages, 40)
    for page_idx in range(scan_limit):
        raw_text = reader.pages[page_idx].extract_text() or ""
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

        if not sample_logged and len(lines) > 5:
            print(f"  [第 {page_idx + 1} 页文本探针预览]: {lines[:4]}")
            sample_logged = True

        for i, line in enumerate(lines):
            de_match = GERMAN_SENTENCE_RE.search(line)
            if not de_match:
                continue

            de_sent = de_match.group(1).strip()
            # 过滤目录或过短无效行
            if ".." in de_sent or len(de_sent.split()) < 5:
                continue

            # 在当前行或相邻下一行寻找中文释义
            zh_sent = ""
            zh_in_same = CHINESE_RE.search(line)
            if zh_in_same:
                zh_sent = zh_in_same.group(1).strip()
            elif i + 1 < len(lines):
                zh_in_next = CHINESE_RE.search(lines[i + 1])
                if zh_in_next:
                    zh_sent = zh_in_next.group(1).strip()

            if not zh_sent:
                continue

            # 提取句中带 der/die/das 的名词作为词汇卡
            vocab_list = []
            for art, noun in NOUN_VOCAB_RE.findall(de_sent):
                full_word = f"{art} {noun}"
                if not any(v["word"] == full_word for v in vocab_list):
                    vocab_list.append({
                        "word": full_word,
                        "pos": "Nomen",
                        "meaning": f"源自《水木德语 {level}》讲义例句",
                        "exampleDe": de_sent,
                        "exampleZh": zh_sent,
                    })

            cloze = pick_cloze_words(de_sent)
            if cloze:
                extracted_pairs.append({
                    "german": de_sent,
                    "chinese": zh_sent,
                    "clozeWords": cloze,
                    "vocab": vocab_list[:2],
                })

    print(f"  -> 从 {pdf_path.name} 提取到 {len(extracted_pairs)} 条有效德中双语语料")

    # 每 5 句组装为一篇精听训练曲目，每个等级最多生成 2 篇精选
    tracks = []
    chunk_size = 5
    for idx in range(0, min(len(extracted_pairs), 10), chunk_size):
        chunk = extracted_pairs[idx:idx + chunk_size]
        if len(chunk) < 2:
            continue
        unit_num = (idx // chunk_size) + 1
        track_id = f"shuimu-{level.lower()}-{unit_num:02d}"
        segments = []
        for s_idx, item in enumerate(chunk, start=1):
            segments.append({
                "id": f"{track_id}-s{s_idx}",
                "startTime": None,
                "endTime": None,
                "german": item["german"],
                "chinese": item["chinese"],
                "clozeWords": item["clozeWords"],
                "vocab": item["vocab"],
            })

        tracks.append({
            "id": track_id,
            "title": f"水木德语 {level} 核心句型精听 #{unit_num}",
            "level": level,
            "source": f"水木德语 {level} 讲义提取",
            "topic": "讲义同步语法与听说",
            "audioUrl": None,
            "duration": None,
            "segments": segments,
        })

    return tracks


def main():
    all_generated_tracks = []
    for level, pdf_path in PDF_FILES:
        tracks = inspect_and_extract_pdf(level, pdf_path)
        all_generated_tracks.extend(tracks)

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_generated_tracks, f, ensure_ascii=False, indent=2)

    print(f"\n[完成] 共生成 {len(all_generated_tracks)} 篇讲义精听曲目 -> {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
