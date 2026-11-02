# -*- coding: utf-8 -*-
import os
import json
import re

JSON_PATH = r"C:\Users\king\Downloads\听力\src\data\generatedTracks.json"
PUBLIC_TRACKS_DIR = r"C:\Users\king\Downloads\听力\public\audio\tracks"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    tracks = json.load(f)

print(f"Loaded {len(tracks)} tracks from {JSON_PATH}")
assert len(tracks) == 40, f"Expected 40 tracks, found {len(tracks)}"

errors = []
for idx, t in enumerate(tracks, 1):
    tid = t["id"]
    # 1. Audio file existence
    rel_audio = t["audioUrl"].lstrip("/")
    abs_audio = os.path.join(r"C:\Users\king\Downloads\听力\public", rel_audio)
    if not os.path.exists(abs_audio):
        errors.append(f"[{tid}] Audio file does not exist: {abs_audio}")
    else:
        sz = os.path.getsize(abs_audio)
        if sz < 10000:
            errors.append(f"[{tid}] Audio file unexpectedly small: {sz} bytes")

    # 2. Check duration
    dur = t["duration"]
    if dur is None or dur <= 0:
        errors.append(f"[{tid}] Invalid duration: {dur}")

    # 3. Check segments
    segs = t.get("segments", [])
    if len(segs) != 3:
        errors.append(f"[{tid}] Expected 3 segments, found {len(segs)}")

    for s_idx, seg in enumerate(segs, 1):
        sid = seg["id"]
        st = seg["startTime"]
        et = seg["endTime"]
        if st is None or et is None or st >= et or et > (dur + 1.0):
            errors.append(f"[{sid}] Invalid times: st={st}, et={et}, dur={dur}")

        ger = seg["german"].strip()
        zh = seg["chinese"].strip()
        if not ger or not zh:
            errors.append(f"[{sid}] Missing text or translation")

        # Check clozeWords
        cloze = seg.get("clozeWords", [])
        if not cloze:
            errors.append(f"[{sid}] Missing clozeWords")
        for cw in cloze:
            # Check if cw appears in ger (strip punctuation)
            clean_ger = re.sub(r"[^\w\säöüÄÖÜß]", " ", ger).lower()
            clean_cw = re.sub(r"[^\w\säöüÄÖÜß]", " ", cw).lower().strip()
            if clean_cw not in clean_ger:
                errors.append(f"[{sid}] clozeWord '{cw}' not found in german: '{ger}'")

        # Check vocab
        vocab = seg.get("vocab", [])
        for v in vocab:
            if not v.get("word") or not v.get("meaning") or not v.get("pos"):
                errors.append(f"[{sid}] Incomplete vocab: {v}")

if errors:
    print(f"\n[FAILED] Found {len(errors)} validation errors:")
    for e in errors:
        print("  -", e)
    exit(1)
else:
    print("\n[SUCCESS] All 40 tracks passed data validation! 0 errors found.")
