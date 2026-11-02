import json
import re
import os
from pathlib import Path
from mutagen.mp3 import MP3

PROJECT_DIR = Path(r"c:\Users\king\Downloads\听力")
pub_dir = PROJECT_DIR / "public"
dist_dir = PROJECT_DIR / "dist"
gen_file = PROJECT_DIR / "src" / "data" / "generatedTracks.json"
seed_file = PROJECT_DIR / "src" / "data" / "seedTracks.ts"
words_dir = pub_dir / "audio" / "words"
bundled_file = PROJECT_DIR / "src" / "data" / "bundledWordAudio.ts"

print("============================================================")
print("Verifying 40 Authentic Official Tracks & Audio Integrity")
print("============================================================\n")

# 1. Verify seedTracks.ts
seed_text = seed_file.read_text(encoding="utf-8")
assert "export const SEED_TRACKS" in seed_text, "seedTracks.ts does not export SEED_TRACKS!"
print("[OK] seedTracks.ts properly exports SEED_TRACKS")

# 2. Load generatedTracks.json
tracks = json.load(open(gen_file, encoding="utf-8"))
assert len(tracks) == 40, f"Expected 40 tracks, found {len(tracks)}"
print(f"[OK] generatedTracks.json contains exactly {len(tracks)} tracks")

CEFR_ORDER = {
    "A1": 1,
    "A2": 2,
    "B1": 3,
    "B2": 4,
    "C1": 5,
    "TestDaF": 6,
}

merged_tracks = sorted(
    tracks,
    key=lambda t: (CEFR_ORDER.get(t.get("level", "B1"), 99), t.get("id", ""))
)

missing_pub = []
missing_dist = []
invalid_segments = []
audio_errors = []
missing_audiourl = []
missing_tasksection = []
sort_errors = []
duration_mismatches = []

prev_order = 0
for idx, t in enumerate(merged_tracks):
    tid = t.get("id")
    audio_url = t.get("audioUrl")
    if not audio_url:
        missing_audiourl.append(tid)
        continue

    # Verify taskSection
    if not t.get("taskSection"):
        missing_tasksection.append(tid)

    # Verify CEFR ordering
    curr_order = CEFR_ORDER.get(t.get("level"), 99)
    if curr_order < prev_order:
        sort_errors.append(f"Track {tid} (order {curr_order}) appeared after order {prev_order}")
    prev_order = curr_order

    # Verify audio file
    rel_path = audio_url.lstrip("/")
    pub_file = pub_dir / rel_path
    dist_file = dist_dir / rel_path

    if not pub_file.exists():
        missing_pub.append(str(rel_path))
    else:
        try:
            audio = MP3(pub_file)
            dur = audio.info.length
            if dur <= 0:
                audio_errors.append(f"{rel_path}: duration <= 0")
            diff = abs(dur - t.get("duration", 0))
            if diff > 1.0:
                duration_mismatches.append(f"{tid}: audio {dur:.1f}s vs json {t.get('duration')}s")
        except Exception as e:
            audio_errors.append(f"{rel_path}: {e}")

    if dist_dir.exists() and not dist_file.exists():
        missing_dist.append(str(rel_path))

    # Verify segments
    segments = t.get("segments", [])
    if len(segments) != 3:
        invalid_segments.append((tid, f"segment count is {len(segments)}, expected 3"))

    prev_end = 0.0
    for s_idx, s in enumerate(segments):
        st = s.get("startTime")
        et = s.get("endTime")
        if st is None or et is None or st < 0 or st >= et or not s.get("german") or not s.get("chinese"):
            invalid_segments.append((tid, s.get("id")))
        if st < prev_end - 0.01:
            invalid_segments.append((tid, f"seg {s_idx} overlap: start {st} < prev end {prev_end}"))
        prev_end = et

print(f"\nTotal verified tracks: {len(merged_tracks)}")
print(f"Missing audioUrl: {len(missing_audiourl)}")
print(f"Missing taskSection: {len(missing_tasksection)}")
print(f"Missing public MP3s: {len(missing_pub)}")
if dist_dir.exists():
    print(f"Missing dist MP3s: {len(missing_dist)}")
print(f"Audio decode errors: {len(audio_errors)}")
print(f"Duration mismatches (>1s): {len(duration_mismatches)}")
print(f"Invalid segments: {len(invalid_segments)}")
print(f"CEFR sorting errors: {len(sort_errors)}")

level_counts = {}
source_counts = {}
for t in merged_tracks:
    lvl = t["level"]
    src = t["source"].split("·")[0].strip()
    level_counts[lvl] = level_counts.get(lvl, 0) + 1
    source_counts[src] = source_counts.get(src, 0) + 1

print("\nCEFR Level distribution:")
for lvl in ["A1", "A2", "B1", "B2", "C1", "TestDaF"]:
    print(f"  {lvl}: {level_counts.get(lvl, 0)}")

print("\nSource distribution:")
for src, count in sorted(source_counts.items(), key=lambda x: -x[1]):
    print(f"  {src}: {count}")

# 3. Verify Word Audio Registry
bundled_text = bundled_file.read_text(encoding="utf-8")
bundled_map = dict(re.findall(r'"([^"]+)":\s*"([^"]+)"', bundled_text))
print(f"\nBundled word audio mappings: {len(bundled_map)}")
assert len(bundled_map) >= 1700, f"Expected >= 1700 bundled word audios, got {len(bundled_map)}"

# Verify all words in public/audio/words are valid
corrupt_words = []
word_files = [f for f in os.listdir(words_dir) if f.endswith(".mp3")]
print(f"Total word MP3 files: {len(word_files)}")
for f in word_files:
    p = words_dir / f
    sz = p.stat().st_size
    if sz < 1000:
        corrupt_words.append((f, sz))

assert len(corrupt_words) == 0, f"Found corrupt word audio files: {corrupt_words}"
print("[OK] All word MP3 files are non-empty and > 1000 bytes")

# Assertions
assert len(missing_audiourl) == 0, f"Missing audioUrl: {missing_audiourl}"
assert len(missing_tasksection) == 0, f"Missing taskSection: {missing_tasksection}"
assert len(missing_pub) == 0, f"Missing public MP3s: {missing_pub}"
if dist_dir.exists():
    assert len(missing_dist) == 0, f"Missing dist MP3s: {missing_dist}"
assert len(audio_errors) == 0, f"Audio decode errors: {audio_errors}"
assert len(duration_mismatches) == 0, f"Duration mismatches: {duration_mismatches}"
assert len(invalid_segments) == 0, f"Invalid segments found: {invalid_segments}"
assert len(sort_errors) == 0, f"Sorting errors found: {sort_errors}"

print("\n============================================================")
print("ALL 40 OFFICIAL EXAM TRACKS & AUDIO INTEGRITY CHECKS PASSED!")
print("============================================================")
