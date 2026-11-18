# -*- coding: utf-8 -*-
"""
Exports all 24 aligned & curated Phase 2.3/2.4 tracks into lazy-loaded static JSON files:
  - public/data/catalog.json
  - public/data/tracks/{id}.json
Generates missing de-DE-KatjaNeural word MP3s into public/audio/words/
and writes new key mappings into public/data/wordAudioMap.json.
"""

import os
import sys
import re
import json
import time
import asyncio
import edge_tts

sys.path.insert(0, os.path.dirname(__file__))
from new_tracks_curriculum_a import CURRICULUM_A
from new_tracks_curriculum_b import CURRICULUM_B

STAGING_ALIGNED = r"D:\GermanCorpus\staging\aligned_candidates.json"
PROJECT_ROOT = r"C:\Users\king\Downloads\听力"
DATA_DIR = os.path.join(PROJECT_ROOT, "public", "data")
TRACKS_DATA_DIR = os.path.join(DATA_DIR, "tracks")
WORDS_DIR = os.path.join(PROJECT_ROOT, "public", "audio", "words")
BUNDLED_TS = os.path.join(PROJECT_ROOT, "src", "data", "bundledWordAudio.ts")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TRACKS_DATA_DIR, exist_ok=True)
os.makedirs(WORDS_DIR, exist_ok=True)

VOICE = "de-DE-KatjaNeural"
TOKEN_SPLIT_REGEX = re.compile(r"[A-Za-zÄÖÜäöüß]+(?:-[A-Za-zÄÖÜäöüß]+)*")
LEVEL_ORDER = {"A1": 0, "A2": 1, "B1": 2, "B2": 3, "C1": 4, "TestDaF": 5}


def to_ascii_slug(s: str) -> str:
    s = s.lower().strip()
    s = s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")


def clean_word_for_lookup(w: str) -> str:
    w = re.sub(r"^(der|die|das|sich|den|dem|des|ein|eine)\s+", "", w, flags=re.I)
    w = re.sub(r"\s*\(.*\)", "", w)
    w = re.sub(r"[.,!?;:()„“”\"'/…]", "", w)
    return w.strip()


def to_speak_text(w: str) -> str:
    """Normalizes Nachrichtenleicht reading hyphens (Arbeits-Platz -> Arbeitsplatz) for fluent Katja TTS."""
    if "-" in w:
        parts = w.split("-")
        # Keep genuine hyphenated phrases/abbreviations separated with space or intact (KZ-Gedenkstätte -> KZ Gedenkstätte)
        if any(len(p) <= 2 or p.isupper() for p in parts) or len(parts) >= 3:
            return " ".join(parts)
        return "".join(parts)
    return w


def build_tracks() -> list[dict]:
    aligned_list = json.load(open(STAGING_ALIGNED, encoding="utf-8"))
    curated = {**CURRICULUM_A, **CURRICULUM_B}

    missing_cur = [t["id"] for t in aligned_list if t["id"] not in curated]
    assert not missing_cur, f"Missing curated data for: {missing_cur}"

    final_tracks = []
    for raw in aligned_list:
        tid = raw["id"]
        spec = curated[tid]
        segs_raw = list(raw["alignedSegments"])

        # Handle optional adjacent merges (e.g., sg-tempolimit short 2s sentence)
        for idx_a, idx_b in reversed(spec.get("mergePairs", [])):
            a, b = segs_raw[idx_a], segs_raw[idx_b]
            segs_raw[idx_a : idx_b + 1] = [{
                "german": f"{a['german']} {b['german']}",
                "startTime": a["startTime"],
                "endTime": b["endTime"],
            }]

        assert len(segs_raw) == len(spec["segments"]), (
            f"Segment mismatch on {tid}: aligned={len(segs_raw)} vs curated={len(spec['segments'])}"
        )

        merged_segs = []
        for si, (seg_a, seg_c) in enumerate(zip(segs_raw, spec["segments"]), 1):
            st = round(float(seg_a["startTime"]), 2)
            et = round(float(seg_a["endTime"]), 2)
            assert 0 <= st < et, f"Invalid timing on {tid} s{si}: {st}..{et}"

            de_text = seg_a["german"].strip()
            tokens = TOKEN_SPLIT_REGEX.findall(de_text)
            token_lower_set = {tok.lower() for tok in tokens}
            cloze = seg_c["clozeWords"]
            for cw in cloze:
                assert cw.lower() in token_lower_set, (
                    f"Cloze word '{cw}' not an exact regex token in {tid} s{si}: '{de_text}'"
                )

            merged_segs.append({
                "id": f"{tid}-s{si}",
                "startTime": st,
                "endTime": et,
                "german": de_text,
                "chinese": seg_c["chinese"],
                "clozeWords": cloze,
                "vocab": seg_c["vocab"],
            })

        # Sort check
        for i in range(1, len(merged_segs)):
            assert merged_segs[i]["startTime"] >= merged_segs[i - 1]["startTime"], f"Unsorted start in {tid}"

        final_tracks.append({
            "id": tid,
            "title": raw["title"],
            "level": raw["level"],
            "source": raw["source"],
            "sourceCategory": raw["sourceCategory"],
            "topic": spec["topic"],
            "taskSection": raw["taskSection"],
            "license": raw.get("license"),
            "audioUrl": raw["audioUrl"],
            "originalAudioUrl": raw.get("originalAudioUrl", raw["audioUrl"]),
            "originalPageUrl": raw.get("originalPageUrl"),
            "duration": round(float(raw["duration"]), 2),
            "segments": merged_segs,
        })

    final_tracks.sort(key=lambda t: (LEVEL_ORDER.get(t["level"], 99), t["source"], t["id"]))
    return final_tracks


async def synth_one_with_retry(speak_text: str, out_path: str) -> bool:
    for attempt in range(3):
        try:
            communicate = edge_tts.Communicate(speak_text, VOICE)
            await communicate.save(out_path)
            if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
                return True
        except Exception as e:
            if attempt == 2:
                print(f"  [Katja ERR] '{speak_text}' -> {e}")
            await asyncio.sleep(0.5 * (attempt + 1))
    return False


async def generate_katja_extension(tracks: list[dict]) -> None:
    # Load existing bundled keys so wordAudioMap.json only adds net-new entries
    bundled_text = open(BUNDLED_TS, encoding="utf-8").read()
    bundled_map = dict(re.findall(r'"([^"]+)":\s*"([^"]+)"', bundled_text))

    # word_clean_lower -> (speak_text, slug)
    candidates: dict[str, tuple[str, str]] = {}

    def register(raw_token: str, speak_override: str | None = None):
        cleaned = clean_word_for_lookup(raw_token)
        if not cleaned or len(cleaned) <= 1:
            return
        slug = to_ascii_slug(cleaned)
        if not slug:
            return
        speak = speak_override or to_speak_text(cleaned)
        candidates[cleaned.lower()] = (speak, slug)
        # For hyphenated words, also register their non-hyphenated collapsed form and sub-tokens >=2 chars
        if "-" in cleaned:
            collapsed = cleaned.replace("-", "")
            c_slug = to_ascii_slug(collapsed)
            if c_slug:
                candidates.setdefault(collapsed.lower(), (speak, c_slug))
            for sub in cleaned.split("-"):
                if len(sub) > 1:
                    s_slug = to_ascii_slug(sub)
                    if s_slug:
                        candidates.setdefault(sub.lower(), (sub, s_slug))

    for t in tracks:
        for seg in t["segments"]:
            for v_item in seg.get("vocab", []):
                w = v_item["word"]
                # Speak full phrase/noun with article when vocab has article or space
                register(w, speak_override=w if len(w.split()) > 1 else None)
            for cw in seg.get("clozeWords", []):
                register(cw)
            for tok in TOKEN_SPLIT_REGEX.findall(seg["german"]):
                register(tok)

    # Identify which slug MP3 files don't exist yet on disk
    needed_by_slug: dict[str, str] = {}
    for lower_k, (speak, slug) in candidates.items():
        mp3_path = os.path.join(WORDS_DIR, f"{slug}.mp3")
        if not os.path.exists(mp3_path) or os.path.getsize(mp3_path) <= 1000:
            needed_by_slug.setdefault(slug, speak)

    print(f"\nUnique word keys across 24 new tracks: {len(candidates)}")
    print(f"Missing Katja MP3 files to generate sequentially: {len(needed_by_slug)}")

    ok_count = 0
    for idx, (slug, speak) in enumerate(sorted(needed_by_slug.items()), 1):
        out_path = os.path.join(WORDS_DIR, f"{slug}.mp3")
        ok = await synth_one_with_retry(speak, out_path)
        if ok:
            ok_count += 1
        if idx % 40 == 0 or idx == len(needed_by_slug):
            print(f"  [Katja] {idx}/{len(needed_by_slug)} processed (ok={ok_count})")
        await asyncio.sleep(0.14)

    # Build public/data/wordAudioMap.json for all new keys/slugs not already identically in BUNDLED_WORD_AUDIO
    ext_map: dict[str, str] = {}
    for lower_k, (_speak, slug) in sorted(candidates.items()):
        mp3_path = os.path.join(WORDS_DIR, f"{slug}.mp3")
        if os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 1000:
            rel_url = f"/audio/words/{slug}.mp3"
            if bundled_map.get(slug) != rel_url:
                ext_map[slug] = rel_url
            if bundled_map.get(lower_k) != rel_url:
                ext_map[lower_k] = rel_url

    map_path = os.path.join(DATA_DIR, "wordAudioMap.json")
    with open(map_path, "w", encoding="utf-8") as f:
        json.dump(ext_map, f, ensure_ascii=False, indent=2)
    print(f"[SUCCESS] Wrote {map_path} with {len(ext_map)} net-new Katja word mappings.")


def main():
    tracks = build_tracks()

    catalog = []
    for t in tracks:
        detail_path = os.path.join(TRACKS_DATA_DIR, f"{t['id']}.json")
        with open(detail_path, "w", encoding="utf-8") as f:
            json.dump(t, f, ensure_ascii=False, indent=2)

        stub = {k: v for k, v in t.items() if k != "segments"}
        stub["segments"] = []
        stub["segmentCount"] = len(t["segments"])
        catalog.append(stub)

    catalog_path = os.path.join(DATA_DIR, "catalog.json")
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

    print(f"[SUCCESS] Exported {len(catalog)} tracks to {catalog_path} and {TRACKS_DATA_DIR}")
    asyncio.run(generate_katja_extension(tracks))


if __name__ == "__main__":
    main()
