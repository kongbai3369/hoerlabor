import os
import json
import re
import asyncio
import edge_tts

WORDS_DIR = r"C:\Users\king\Downloads\听力\public\audio\words"
TRACKS_JSON = r"C:\Users\king\Downloads\听力\src\data\generatedTracks.json"
BUNDLED_TS = r"C:\Users\king\Downloads\听力\src\data\bundledWordAudio.ts"
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

async def main():
    with open(TRACKS_JSON, "r", encoding="utf-8") as f:
        tracks = json.load(f)

    existing = set(os.listdir(WORDS_DIR))
    to_gen = {}

    for track in tracks:
        for seg in track.get("segments", []):
            for v in seg.get("vocab", []):
                raw = v.get("word", "")
                cw = clean_word(raw)
                slug = to_ascii_slug(cw)
                if slug and f"{slug}.mp3" not in existing:
                    to_gen[slug] = (cw, raw)
            for c in seg.get("clozeWords", []):
                cw = clean_word(c)
                slug = to_ascii_slug(cw)
                if slug and f"{slug}.mp3" not in existing:
                    to_gen[slug] = (cw, c)
            for tok in re.findall(r"[a-zA-ZäöüÄÖÜß]+", seg.get("german", "")):
                cw = clean_word(tok)
                slug = to_ascii_slug(cw)
                if len(cw) > 1 and slug and f"{slug}.mp3" not in existing:
                    to_gen[slug] = (cw, cw)

    print(f"Total unique missing slugs to generate: {len(to_gen)}")

    for slug, (cw, raw) in to_gen.items():
        out_f = os.path.join(WORDS_DIR, f"{slug}.mp3")
        try:
            print(f"Generating '{raw}' -> {slug}.mp3 ...")
            comm = edge_tts.Communicate(raw, VOICE)
            await comm.save(out_f)
            await asyncio.sleep(0.15) # gentle pacing
        except Exception as e:
            print(f"  [ERROR] {slug}: {e}")

    # Now update bundledWordAudio.ts
    all_files = [f for f in os.listdir(WORDS_DIR) if f.endswith(".mp3")]
    all_files.sort()
    entries = []
    for f in all_files:
        s = f[:-4]
        entries.append(f'  "{s}": "/audio/words/{f}",')

    ts_content = """// Auto-generated Katja Neural audio registry for desktop & mobile
export const BUNDLED_WORD_AUDIO: Record<string, string> = {
""" + "\n".join(entries) + "\n};\n"

    with open(BUNDLED_TS, "w", encoding="utf-8") as f:
        f.write(ts_content)
    print(f"[DONE] bundledWordAudio.ts updated with {len(entries)} Katja words!")

if __name__ == "__main__":
    asyncio.run(main())
