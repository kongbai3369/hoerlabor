# -*- coding: utf-8 -*-
"""
Validates integrity of lazy-loaded Phase 2.3/2.4 multi-source tracks:
  - public/data/catalog.json schema & metadata
  - public/data/tracks/{id}.json segment timings, cloze tokens, vocab structure
  - public/data/wordAudioMap.json + BUNDLED_WORD_AUDIO completeness & MP3 sizes > 1000 bytes
  - Local telc audio files existence in public/audio/tracks (and dist/audio/tracks if built)
"""

import os
import re
import json
from pathlib import Path
from mutagen.mp3 import MP3

PROJECT_ROOT = Path(r"C:\Users\king\Downloads\听力")
CATALOG_PATH = PROJECT_ROOT / "public" / "data" / "catalog.json"
TRACKS_DIR = PROJECT_ROOT / "public" / "data" / "tracks"
WORD_MAP_PATH = PROJECT_ROOT / "public" / "data" / "wordAudioMap.json"
WORDS_DIR = PROJECT_ROOT / "public" / "audio" / "words"
BUNDLED_TS = PROJECT_ROOT / "src" / "data" / "bundledWordAudio.ts"
PUBLIC_DIR = PROJECT_ROOT / "public"
DIST_DIR = PROJECT_ROOT / "dist"

TOKEN_SPLIT_REGEX = re.compile(r"[A-Za-zÄÖÜäöüß]+(?:-[A-Za-zÄÖÜäöüß]+)*")
VALID_CATS = {"exam", "news", "podcast", "authentic", "custom"}
VALID_LEVELS = {"A1", "A2", "B1", "B2", "C1", "TestDaF"}


def to_ascii_slug(s: str) -> str:
    s = s.lower().strip()
    s = s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")


def clean_word(w: str) -> str:
    w = re.sub(r"^(der|die|das|sich|den|dem|des|ein|eine)\s+", "", w, flags=re.I)
    w = re.sub(r"\s*\(.*\)", "", w)
    w = re.sub(r"[.,!?;:()„“”\"'/…]", "", w)
    return w.strip()


def main():
    assert CATALOG_PATH.exists(), f"Missing {CATALOG_PATH}"
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    assert len(catalog) >= 20, f"Expected >=20 lazy tracks, got {len(catalog)}"

    bundled_map = dict(re.findall(r'"([^"]+)":\s*"([^"]+)"', BUNDLED_TS.read_text(encoding="utf-8")))
    extra_map = json.loads(WORD_MAP_PATH.read_text(encoding="utf-8")) if WORD_MAP_PATH.exists() else {}
    merged_words = {**bundled_map, **extra_map}

    missing_word_audio = []
    errors = []

    for item in catalog:
        tid = item["id"]
        if item.get("level") not in VALID_LEVELS:
            errors.append(f"{tid}: invalid level {item.get('level')}")
        if item.get("sourceCategory") not in VALID_CATS:
            errors.append(f"{tid}: invalid sourceCategory {item.get('sourceCategory')}")
        if item.get("segments") != []:
            errors.append(f"{tid}: catalog stub should have segments=[]")

        detail_file = TRACKS_DIR / f"{tid}.json"
        if not detail_file.exists():
            errors.append(f"{tid}: missing {detail_file}")
            continue

        detail = json.loads(detail_file.read_text(encoding="utf-8"))
        segs = detail.get("segments", [])
        if len(segs) != item.get("segmentCount"):
            errors.append(f"{tid}: segmentCount {item.get('segmentCount')} != actual {len(segs)}")

        aurl = detail.get("audioUrl", "")
        if aurl.startswith("/"):
            p = PUBLIC_DIR / aurl.lstrip("/")
            if not p.exists():
                errors.append(f"{tid}: missing local audio {p}")
            else:
                dur = MP3(p).info.length
                if abs(dur - detail.get("duration", 0)) > 1.2:
                    errors.append(f"{tid}: duration mismatch audio={dur:.2f} vs json={detail.get('duration')}")
            if DIST_DIR.exists():
                dp = DIST_DIR / aurl.lstrip("/")
                if not dp.exists():
                    errors.append(f"{tid}: missing dist audio {dp}")
        elif not aurl.startswith("https://"):
            errors.append(f"{tid}: invalid audioUrl {aurl}")

        prev_end = 0.0
        for s in segs:
            st, et = s.get("startTime"), s.get("endTime")
            if st is None or et is None or st < 0 or st >= et:
                errors.append(f"{tid}/{s.get('id')}: bad timestamps {st}..{et}")
            if st < prev_end - 0.02:
                errors.append(f"{tid}/{s.get('id')}: overlapping start {st} < {prev_end}")
            prev_end = et

            tokens = [t.lower() for t in TOKEN_SPLIT_REGEX.findall(s.get("german", ""))]
            for cw in s.get("clozeWords", []):
                if cw.lower() not in tokens:
                    errors.append(f"{tid}/{s.get('id')}: clozeWord '{cw}' not exact token match")

            # Verify word audio availability
            for raw_tok in (
                [v.get("word", "") for v in s.get("vocab", [])]
                + s.get("clozeWords", [])
                + TOKEN_SPLIT_REGEX.findall(s.get("german", ""))
            ):
                c = clean_word(raw_tok)
                if len(c) <= 1:
                    continue
                low = c.lower()
                slug = to_ascii_slug(c)
                if low not in merged_words and slug not in merged_words:
                    missing_word_audio.append((tid, low))

    # Verify all mapped MP3s on disk exist and > 1000 bytes
    bad_mp3 = []
    for k, url in extra_map.items():
        p = PUBLIC_DIR / url.lstrip("/")
        if not p.exists() or p.stat().st_size <= 1000:
            bad_mp3.append((k, url))

    # Count dist size / Pages limit safety
    total_pub_bytes = sum(f.stat().st_size for f in PUBLIC_DIR.rglob("*") if f.is_file())
    total_pub_files = sum(1 for f in PUBLIC_DIR.rglob("*") if f.is_file())

    print(f"Lazy catalog tracks verified: {len(catalog)}")
    print(f"Extra Katja word mappings in wordAudioMap.json: {len(extra_map)}")
    print(f"Public directory footprint: {total_pub_bytes / (1024*1024):.2f} MB ({total_pub_files} files)")
    print(f"Missing word mappings: {len(set(missing_word_audio))} {missing_word_audio[:10]}")
    print(f"Corrupt/missing extra word MP3s: {len(bad_mp3)} {bad_mp3[:10]}")
    print(f"Structural errors: {len(errors)} {errors[:10]}")

    assert not errors, f"Catalog errors: {errors}"
    assert not bad_mp3, f"Corrupt word MP3s: {bad_mp3}"
    assert not missing_word_audio, f"Missing Katja word audio: {missing_word_audio[:20]}"
    assert total_pub_files < 18000, f"Too many files for Cloudflare Pages: {total_pub_files}"
    print("[PASS] ALL LAZY CATALOG, STREAMING/LOCAL AUDIO, CLOZE TOKEN & KATJA WORD DICTIONARY CHECKS PASSED!")


if __name__ == "__main__":
    main()
