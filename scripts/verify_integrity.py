import json
import re
from pathlib import Path
from mutagen.mp3 import MP3

PROJECT_DIR = Path(r"c:\Users\king\Downloads\听力")
pub_dir = PROJECT_DIR / "public" / "audio"
dist_dir = PROJECT_DIR / "dist" / "audio"
gen_file = PROJECT_DIR / "src" / "data" / "generatedTracks.json"
seed_file = PROJECT_DIR / "src" / "data" / "seedTracks.ts"

tracks = json.load(open(gen_file, encoding='utf-8'))

# Parse seedTracks.ts to verify seed tracks too
seed_text = seed_file.read_text(encoding='utf-8')
seed_ids = re.findall(r"\{\s*id:\s*['\"]([a-z0-9\-]+-01)['\"]", seed_text)

print(f"Loaded {len(tracks)} tracks from generatedTracks.json")
print(f"Found {len(seed_ids)} seed track definitions in seedTracks.ts: {seed_ids}")

# Simulate mergeAllTracks
track_map = {}
for sid in seed_ids:
    track_map[sid] = {"id": sid}

for t in tracks:
    track_map[t['id']] = t

CEFR_ORDER = {
    'A1': 1,
    'A2': 2,
    'B1': 3,
    'B2': 4,
    'C1': 5,
    'TestDaF': 6,
}

merged_tracks = sorted(
    track_map.values(),
    key=lambda t: (CEFR_ORDER.get(t.get('level', 'B1'), 99), t.get('id', ''))
)

missing_pub = []
missing_dist = []
invalid_segments = []
audio_errors = []
missing_audiourl = []
sort_errors = []

prev_order = 0
for idx, t in enumerate(merged_tracks):
    tid = t.get('id')
    audio_url = t.get('audioUrl')
    if not audio_url:
        missing_audiourl.append(tid)

    curr_order = CEFR_ORDER.get(t.get('level'), 99)
    if curr_order < prev_order:
        sort_errors.append(f"Track {tid} (order {curr_order}) appeared after order {prev_order}")
    prev_order = curr_order

    mp3_name = tid + '.mp3'
    pub_file = pub_dir / mp3_name
    dist_file = dist_dir / mp3_name

    if not pub_file.exists():
        missing_pub.append(mp3_name)
    else:
        try:
            audio = MP3(pub_file)
            dur = audio.info.length
            if dur <= 0:
                audio_errors.append(f"{mp3_name}: duration <= 0")
        except Exception as e:
            audio_errors.append(f"{mp3_name}: {e}")

    if not dist_file.exists():
        missing_dist.append(mp3_name)

    segments = t.get('segments', [])
    if not segments:
        invalid_segments.append((tid, "NO_SEGMENTS"))

    for s in segments:
        st = s.get('startTime')
        et = s.get('endTime')
        if st is None or et is None or st < 0 or st >= et or not s.get('german') or not s.get('chinese'):
            invalid_segments.append((tid, s.get('id')))

print(f'\nTotal merged tracks: {len(merged_tracks)}')
print(f'Missing audioUrl property: {len(missing_audiourl)}')
print(f'Missing public MP3s: {len(missing_pub)}')
print(f'Missing dist MP3s: {len(missing_dist)}')
print(f'Audio decode errors: {len(audio_errors)}')
print(f'Invalid segments: {len(invalid_segments)}')
print(f'CEFR sorting errors: {len(sort_errors)}')

level_counts = {}
source_counts = {}
for t in merged_tracks:
    lvl = t['level']
    src = t['source'].split('·')[0].strip()
    level_counts[lvl] = level_counts.get(lvl, 0) + 1
    source_counts[src] = source_counts.get(src, 0) + 1

print('\nCEFR Level distribution:')
for lvl in ['A1', 'A2', 'B1', 'B2', 'C1', 'TestDaF']:
    print(f'  {lvl}: {level_counts.get(lvl, 0)}')

print('\nSource distribution:')
for src, count in sorted(source_counts.items(), key=lambda x: -x[1]):
    print(f'  {src}: {count}')

assert len(missing_audiourl) == 0, f'Missing audioUrl: {missing_audiourl}'
assert len(missing_pub) == 0, f'Missing public MP3s: {missing_pub}'
assert len(missing_dist) == 0, f'Missing dist MP3s: {missing_dist}'
assert len(audio_errors) == 0, f'Audio errors: {audio_errors}'
assert len(invalid_segments) == 0, f'Invalid segments found: {invalid_segments}'
assert len(sort_errors) == 0, f'Sorting errors found: {sort_errors}'

print('\n=============================================')
print('ALL 34 MERGED TRACKS & AUDIO INTEGRITY CHECKS PASSED!')
print('=============================================')
