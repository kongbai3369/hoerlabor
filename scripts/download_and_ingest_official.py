import os
import sys
import subprocess
import requests
import imageio_ffmpeg
from mutagen.mp3 import MP3

RAW_GOETHE_DIR = r"D:\GermanCorpus\raw\goethe"
RAW_TESTDAF_DIR = r"D:\GermanCorpus\raw\testdaf"
PROCESSED_TRACKS_DIR = r"D:\GermanCorpus\processed\tracks"

os.makedirs(RAW_GOETHE_DIR, exist_ok=True)
os.makedirs(RAW_TESTDAF_DIR, exist_ok=True)
os.makedirs(PROCESSED_TRACKS_DIR, exist_ok=True)

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
print(f"[INIT] Using FFmpeg from: {FFMPEG_EXE}")

FILES_TO_DOWNLOAD = [
    # --- TestDaF 官方真题原声 ---
    {
        "authority": "testdaf",
        "name": "testdaf_modellsatz_01_hv.mp3",
        "url": "https://www.testdaf.de/fileadmin/testdaf/downloads/Modelltests_papierbasierter_TestDaF/Modelltest_1/Hoeren/Ton_Modelltest01_HV_final.mp3",
        "type": "audio",
        "dest": os.path.join(RAW_TESTDAF_DIR, "testdaf_modellsatz_01_hv.mp3")
    },
    {
        "authority": "testdaf",
        "name": "testdaf_modellsatz_01_hv_transkription.pdf",
        "url": "https://www.testdaf.de/fileadmin/testdaf/downloads/Modelltests_papierbasierter_TestDaF/Modelltest_1/Hoeren/Modelltest_01_HV_Transkription.pdf",
        "type": "pdf",
        "dest": os.path.join(RAW_TESTDAF_DIR, "testdaf_modellsatz_01_hv_transkription.pdf")
    },
    {
        "authority": "testdaf",
        "name": "testdaf_modellsatz_02_hv.mp3",
        "url": "https://www.testdaf.de/fileadmin/testdaf/downloads/Modelltests_papierbasierter_TestDaF/Modelltest_2/Hoeren/Ton_MS02_HV_final.mp3",
        "type": "audio",
        "dest": os.path.join(RAW_TESTDAF_DIR, "testdaf_modellsatz_02_hv.mp3")
    },
    {
        "authority": "testdaf",
        "name": "testdaf_modellsatz_02_hv_transkription.pdf",
        "url": "https://www.testdaf.de/fileadmin/testdaf/downloads/Modelltests_papierbasierter_TestDaF/Modelltest_2/Hoeren/Modelltest_02_HV_Transkription.pdf",
        "type": "pdf",
        "dest": os.path.join(RAW_TESTDAF_DIR, "testdaf_modellsatz_02_hv_transkription.pdf")
    },

    # --- 歌德学院 Goethe-Institut 官方真题原声 ---
    {
        "authority": "goethe",
        "name": "goethe_a1_hoeren.mp4",
        "url": "https://goethemp4s.akamaized.net/resources/files/mp430/pruefungstraining_1_hoeren_a1_erwachsene.mp4",
        "type": "video_to_audio",
        "dest": os.path.join(RAW_GOETHE_DIR, "goethe_a1_hoeren.mp4"),
        "mp3_dest": os.path.join(RAW_GOETHE_DIR, "goethe_a1_hoeren.mp3")
    },
    {
        "authority": "goethe",
        "name": "goethe_a2_hoeren.mp4",
        "url": "https://goethemp4s.akamaized.net/resources/files/mp434/pruefungstraining_1_hoeren_a2_erwachsene.mp4",
        "type": "video_to_audio",
        "dest": os.path.join(RAW_GOETHE_DIR, "goethe_a2_hoeren.mp4"),
        "mp3_dest": os.path.join(RAW_GOETHE_DIR, "goethe_a2_hoeren.mp3")
    },
    {
        "authority": "goethe",
        "name": "goethe_b1_hoeren.mp4",
        "url": "https://goethemp4s.akamaized.net/resources/files/mp468/pruefungstraining_1_hoeren_b1_erwachsene.mp4",
        "type": "video_to_audio",
        "dest": os.path.join(RAW_GOETHE_DIR, "goethe_b1_hoeren.mp4"),
        "mp3_dest": os.path.join(RAW_GOETHE_DIR, "goethe_b1_hoeren.mp3")
    },
    {
        "authority": "goethe",
        "name": "goethe_b1_transkription.pdf",
        "url": "https://www.goethe.de/pro/relaunch/prf/materialien/B1/b1_modellsatz_erwachsene.pdf",
        "type": "pdf",
        "dest": os.path.join(RAW_GOETHE_DIR, "goethe_b1_transkription.pdf")
    },
    {
        "authority": "goethe",
        "name": "goethe_b2_hoeren.mp4",
        "url": "https://goethemp4s.akamaized.net/resources/files/mp477/b2_modellsatz_rahmen_erwachsene.mp4",
        "type": "video_to_audio",
        "dest": os.path.join(RAW_GOETHE_DIR, "goethe_b2_hoeren.mp4"),
        "mp3_dest": os.path.join(RAW_GOETHE_DIR, "goethe_b2_hoeren.mp3")
    },
    {
        "authority": "goethe",
        "name": "goethe_b2_transkription.pdf",
        "url": "https://www.goethe.de/pro/relaunch/prf/materialien/B2/b2_modellsatz_erwachsene.pdf",
        "type": "pdf",
        "dest": os.path.join(RAW_GOETHE_DIR, "goethe_b2_transkription.pdf")
    },
    {
        "authority": "goethe",
        "name": "goethe_c1_hoeren.mp3",
        "url": "https://goethemp4s.akamaized.net/resources/files/mp310/pruefungstraining_1_hoeren_c1.mp3",
        "type": "audio",
        "dest": os.path.join(RAW_GOETHE_DIR, "goethe_c1_hoeren.mp3")
    },
    {
        "authority": "goethe",
        "name": "goethe_c1_transkription.pdf",
        "url": "https://www.goethe.de/pro/relaunch/prf/materialien/C1/c1_modellsatz.pdf",
        "type": "pdf",
        "dest": os.path.join(RAW_GOETHE_DIR, "goethe_c1_transkription.pdf")
    }
]

def download_file(url, dest_path):
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 100000:
        print(f"[SKIP] Already exists: {os.path.basename(dest_path)} ({os.path.getsize(dest_path):,} bytes)")
        return True

    print(f"[DOWNLOADING] {os.path.basename(dest_path)} from {url}...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    with requests.get(url, headers=headers, stream=True, timeout=60) as r:
        r.raise_for_status()
        total_len = int(r.headers.get('content-length', 0))
        downloaded = 0
        with open(dest_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 512):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
        print(f"  -> Finished: {downloaded:,} bytes saved.")
    return True

def extract_audio_from_video(video_path, mp3_path):
    if os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 100000:
        print(f"[SKIP] Pure MP3 already extracted: {os.path.basename(mp3_path)}")
        return True
    
    print(f"[EXTRACTING AUDIO] Extracting pure MP3 from {os.path.basename(video_path)} -> {os.path.basename(mp3_path)}...")
    cmd = [
        FFMPEG_EXE,
        "-y",
        "-i", video_path,
        "-vn",
        "-c:a", "libmp3lame",
        "-q:a", "2",
        mp3_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        print(f"[ERROR] Failed to extract audio: {res.stderr.decode('utf-8', errors='ignore')}")
        return False
    print(f"  -> Extracted pure audio: {os.path.getsize(mp3_path):,} bytes.")
    return True

def verify_mp3(file_path):
    try:
        audio = MP3(file_path)
        print(f"[VERIFIED] {os.path.basename(file_path)}: length={audio.info.length:.2f}s, bitrate={audio.info.bitrate//1000}kbps, samplerate={audio.info.sample_rate}Hz")
        return True
    except Exception as e:
        print(f"[INVALID MP3] {file_path}: {e}")
        return False

def main():
    print("=" * 60)
    print("  HörLabor 官方真题原声采集与落盘流水线 (Goethe + TestDaF)")
    print("=" * 60)
    
    for item in FILES_TO_DOWNLOAD:
        try:
            download_file(item["url"], item["dest"])
            if item.get("type") == "video_to_audio":
                extract_audio_from_video(item["dest"], item["mp3_dest"])
                verify_mp3(item["mp3_dest"])
            elif item.get("type") == "audio":
                verify_mp3(item["dest"])
        except Exception as e:
            print(f"[FAILED] Error processing {item['name']}: {e}")

    print("\n[COMPLETE] 官方真题母卷音频与原文 PDF 已完整落盘 D:\\GermanCorpus\\raw\\")

if __name__ == "__main__":
    main()
