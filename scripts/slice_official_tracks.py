import os
import sys
import shutil
import subprocess
import json
import imageio_ffmpeg

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))
from track_definitions import TRACK_DEFINITIONS

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

PROCESSED_DIR = r"D:\GermanCorpus\processed\tracks"
PUBLIC_DIR = r"C:\Users\king\Downloads\听力\public\audio\tracks"
JSON_PATH = r"C:\Users\king\Downloads\听力\src\data\generatedTracks.json"

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(PUBLIC_DIR, exist_ok=True)

def main():
    print(f"============================================================")
    print(f"Slicing all {len(TRACK_DEFINITIONS)} authentic tracks from D:\\GermanCorpus\\raw")
    print(f"Destination 1: {PROCESSED_DIR}")
    print(f"Destination 2: {PUBLIC_DIR}")
    print(f"Metadata file: {JSON_PATH}")
    print(f"============================================================\n")

    tracks_json = []

    for idx, item in enumerate(TRACK_DEFINITIONS, 1):
        out_name = item["out_file"]
        proc_path = os.path.join(PROCESSED_DIR, out_name)
        pub_path = os.path.join(PUBLIC_DIR, out_name)

        dur = float(item["to"]) - float(item["ss"])
        print(f"[{idx:02d}/{len(TRACK_DEFINITIONS)}] Slicing '{item['id']}' ({item['level']} - {item['taskSection']})...")
        print(f"       From: {os.path.basename(item['raw_file'])} [{item['ss']}s -> {item['to']}s] (dur: {dur:.1f}s)")

        # Run ffmpeg slicing
        cmd = [
            FFMPEG, "-y",
            "-ss", str(item["ss"]),
            "-to", str(item["to"]),
            "-i", item["raw_file"],
            "-c:a", "libmp3lame",
            "-b:a", "128k",
            proc_path
        ]
        ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if ret.returncode != 0:
            err_msg = ret.stderr.decode('utf-8', errors='ignore')
            print(f"  [ERROR] Slicing failed for {item['id']}: {err_msg[:300]}")
            continue

        # Copy to public/audio/tracks
        shutil.copy2(proc_path, pub_path)
        size = os.path.getsize(pub_path)
        print(f"       -> Sliced & copied: {out_name} ({size:,} bytes)")

        # Prepare ListeningTrack object
        track_obj = {
            "id": item["id"],
            "title": item["title"],
            "level": item["level"],
            "source": item["source"],
            "topic": item["topic"],
            "taskSection": item["taskSection"],
            "audioUrl": f"/audio/tracks/{out_name}",
            "duration": round(dur, 2),
            "segments": item["segments"]
        }
        tracks_json.append(track_obj)

    # Save to src/data/generatedTracks.json
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(tracks_json, f, ensure_ascii=False, indent=2)

    print(f"\n[COMPLETED] Successfully processed and saved all {len(tracks_json)} tracks to {JSON_PATH}!")

if __name__ == "__main__":
    main()
