import json
import re

seed_tracks = [
    {"id": "a1-wohnung-01", "level": "A1"},
    {"id": "a2-alltag-01", "level": "A2"},
    {"id": "b1-audiolingua-01", "level": "B1"},
    {"id": "b2-uni-testdaf-01", "level": "B2"}
]

gen_tracks = json.load(open('src/data/generatedTracks.json', encoding='utf-8'))
gen_map = {t['id']: t for t in gen_tracks}

print("=== SEED TRACKS IN GENERATED ===")
for st in seed_tracks:
    sid = st['id']
    if sid in gen_map:
        gt = gen_map[sid]
        print(f"  {sid}: PRESENT, audioUrl={gt.get('audioUrl')}, duration={gt.get('duration')}")
    else:
        print(f"  {sid}: MISSING in generatedTracks.json! audioUrl=None")

# Simulate mergeAllTracks([])
merged_map = {}
for st in seed_tracks:
    merged_map[st['id']] = st
for gt in gen_tracks:
    merged_map[gt['id']] = gt

print(f"\nTotal merged tracks: {len(merged_map)}")
print("First 8 track IDs in merged order:")
for i, (tid, trk) in enumerate(list(merged_map.items())[:8]):
    print(f"  {i+1}. {tid} [{trk.get('level')}] (audio: {trk.get('audioUrl') is not None})")

