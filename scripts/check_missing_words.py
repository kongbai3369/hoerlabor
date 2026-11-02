import os
import json
import re

WORDS_DIR = r"C:\Users\king\Downloads\听力\public\audio\words"
TRACKS_JSON = r"C:\Users\king\Downloads\听力\src\data\generatedTracks.json"

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

with open(TRACKS_JSON, "r", encoding="utf-8") as f:
    tracks = json.load(f)

existing = set(os.listdir(WORDS_DIR))

missing = []
for track in tracks:
    for seg in track.get("segments", []):
        for v in seg.get("vocab", []):
            raw = v.get("word", "")
            cw = clean_word(raw)
            slug = to_ascii_slug(cw)
            if slug and f"{slug}.mp3" not in existing:
                missing.append((raw, cw, slug))
        for c in seg.get("clozeWords", []):
            cw = clean_word(c)
            slug = to_ascii_slug(cw)
            if slug and f"{slug}.mp3" not in existing:
                missing.append((c, cw, slug))

print(f"Total missing vocabulary/cloze words: {len(missing)}")
for r, c, s in missing[:25]:
    print(f"  Missing: {r} -> {s}.mp3")
