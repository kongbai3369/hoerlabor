import os
import json
import re
import asyncio
import edge_tts

WORDS_DIR = r"C:\Users\king\Downloads\听力\public\audio\words"
TRACKS_JSON = r"C:\Users\king\Downloads\听力\src\data\generatedTracks.json"
BUNDLED_TS = r"C:\Users\king\Downloads\听力\src\data\bundledWordAudio.ts"
os.makedirs(WORDS_DIR, exist_ok=True)

VOICE = "de-DE-KatjaNeural"

def to_ascii_slug(s):
    s = s.lower().strip()
    s = s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")

def clean_word(w):
    w = re.sub(r"^(der|die|das|sich|den|dem|des|ein|eine)\s+", "", w, flags=re.I)
    w = re.sub(r"\s*\(.*\)", "", w)
    w = re.sub(r"[.,!?;:()„“”\"'/]", "", w)
    return w.strip()

async def generate_word(word_to_speak, filename):
    out_path = os.path.join(WORDS_DIR, filename)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        return
    try:
        communicate = edge_tts.Communicate(word_to_speak, VOICE)
        await communicate.save(out_path)
        print(f"  [Katja TTS] Generated {filename} for '{word_to_speak}' ({os.path.getsize(out_path):,} bytes)")
    except Exception as e:
        print(f"  [Error] Failed to generate {filename}: {e}")

async def main():
    with open(TRACKS_JSON, "r", encoding="utf-8") as f:
        tracks = json.load(f)

    words_to_generate = set()

    for track in tracks:
        for seg in track.get("segments", []):
            # 1. Vocab items
            for v in seg.get("vocab", []):
                raw = v.get("word", "")
                cleaned = clean_word(raw)
                if cleaned:
                    words_to_generate.add((cleaned, raw))
            # 2. Cloze words
            for c in seg.get("clozeWords", []):
                cleaned = clean_word(c)
                if cleaned:
                    words_to_generate.add((cleaned, cleaned))
            # 3. Individual transcript words
            for tok in re.findall(r"[a-zA-ZäöüÄÖÜß]+", seg.get("german", "")):
                cleaned = clean_word(tok)
                if len(cleaned) > 1:
                    words_to_generate.add((cleaned, cleaned))

    print(f"Total unique words to verify for Katja Edge-TTS: {len(words_to_generate)}")

    tasks = []
    for word_clean, speak_text in words_to_generate:
        slug = to_ascii_slug(word_clean)
        if not slug:
            continue
        fname = f"{slug}.mp3"
        fpath = os.path.join(WORDS_DIR, fname)
        if not os.path.exists(fpath) or os.path.getsize(fpath) < 1000:
            tasks.append(generate_word(speak_text, fname))

    if tasks:
        print(f"Generating {len(tasks)} missing word audios via Edge-TTS ({VOICE})...")
        # Run in batches of 10 to avoid overwhelming connection
        for i in range(0, len(tasks), 10):
            batch = tasks[i:i+10]
            await asyncio.gather(*batch)
    else:
        print("All word audios already exist!")

    # Now re-generate bundledWordAudio.ts
    all_files = [f for f in os.listdir(WORDS_DIR) if f.endswith(".mp3") and os.path.getsize(os.path.join(WORDS_DIR, f)) > 1000]
    all_files.sort()
    print(f"\nBuilding bundledWordAudio.ts with {len(all_files)} audio files...")

    entries = []
    for f in all_files:
        slug = f[:-4]
        entries.append(f'  "{slug}": "/audio/words/{f}",')

    # Also map the un-slugified words deterministically
    sorted_words = sorted(list(words_to_generate), key=lambda x: (x[0].lower(), x[0]))
    for word_clean, _ in sorted_words:
        slug = to_ascii_slug(word_clean)
        lower = word_clean.lower()
        if f"{slug}.mp3" in all_files:
            entries.append(f'  "{lower}": "/audio/words/{slug}.mp3",')

    # Deduplicate entries while preserving order
    seen = set()
    deduped = []
    for line in entries:
        k = line.split(":")[0].strip()
        if k not in seen:
            seen.add(k)
            deduped.append(line)

    ts_content = """// Auto-generated native German pronunciation audio registry (Katja Edge-TTS)
// Covers all vocabulary and transcript tokens in Hoerlabor listening tracks.

export const BUNDLED_WORD_AUDIO: Record<string, string> = {
""" + "\n".join(deduped) + "\n};\n"

    with open(BUNDLED_TS, "w", encoding="utf-8") as f:
        f.write(ts_content)
    print(f"[SUCCESS] Updated {BUNDLED_TS} with {len(deduped)} entries!")

if __name__ == "__main__":
    asyncio.run(main())
