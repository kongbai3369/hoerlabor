import os
import subprocess
import imageio_ffmpeg
from mutagen.mp3 import MP3

RAW_GOETHE_DIR = r"D:\GermanCorpus\raw\goethe"
RAW_TESTDAF_DIR = r"D:\GermanCorpus\raw\testdaf"
os.makedirs(RAW_GOETHE_DIR, exist_ok=True)
os.makedirs(RAW_TESTDAF_DIR, exist_ok=True)

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

ITEMS = [
    # TestDaF PDFs & MP3s
    {
        "url": "https://www.testdaf.de/fileadmin/testdaf/downloads/Modelltests_papierbasierter_TestDaF/Modelltest_1/Hoeren/Modelltest_01_HV_Transkription.pdf",
        "dest": os.path.join(RAW_TESTDAF_DIR, "testdaf_modellsatz_01_hv_transkription.pdf")
    },
    {
        "url": "https://www.testdaf.de/fileadmin/testdaf/downloads/Modelltests_papierbasierter_TestDaF/Modelltest_2/Hoeren/Ton_MS02_HV_final.mp3",
        "dest": os.path.join(RAW_TESTDAF_DIR, "testdaf_modellsatz_02_hv.mp3")
    },
    {
        "url": "https://www.testdaf.de/fileadmin/testdaf/downloads/Modelltests_papierbasierter_TestDaF/Modelltest_2/Hoeren/Modelltest_02_HV_Transkription.pdf",
        "dest": os.path.join(RAW_TESTDAF_DIR, "testdaf_modellsatz_02_hv_transkription.pdf")
    },

    # Goethe PDFs & MP4s / MP3s
    {
        "url": "https://goethemp4s.akamaized.net/resources/files/mp430/pruefungstraining_1_hoeren_a1_erwachsene.mp4",
        "dest": os.path.join(RAW_GOETHE_DIR, "goethe_a1_hoeren.mp4"),
        "mp3": os.path.join(RAW_GOETHE_DIR, "goethe_a1_hoeren.mp3")
    },
    {
        "url": "https://goethemp4s.akamaized.net/resources/files/mp434/pruefungstraining_1_hoeren_a2_erwachsene.mp4",
        "dest": os.path.join(RAW_GOETHE_DIR, "goethe_a2_hoeren.mp4"),
        "mp3": os.path.join(RAW_GOETHE_DIR, "goethe_a2_hoeren.mp3")
    },
    {
        "url": "https://goethemp4s.akamaized.net/resources/files/mp468/pruefungstraining_1_hoeren_b1_erwachsene.mp4",
        "dest": os.path.join(RAW_GOETHE_DIR, "goethe_b1_hoeren.mp4"),
        "mp3": os.path.join(RAW_GOETHE_DIR, "goethe_b1_hoeren.mp3")
    },
    {
        "url": "https://www.goethe.de/pro/relaunch/prf/materialien/B1/b1_modellsatz_erwachsene.pdf",
        "dest": os.path.join(RAW_GOETHE_DIR, "goethe_b1_transkription.pdf")
    },
    {
        "url": "https://goethemp4s.akamaized.net/resources/files/mp477/b2_modellsatz_rahmen_erwachsene.mp4",
        "dest": os.path.join(RAW_GOETHE_DIR, "goethe_b2_hoeren.mp4"),
        "mp3": os.path.join(RAW_GOETHE_DIR, "goethe_b2_hoeren.mp3")
    },
    {
        "url": "https://www.goethe.de/pro/relaunch/prf/materialien/B2/b2_modellsatz_erwachsene.pdf",
        "dest": os.path.join(RAW_GOETHE_DIR, "goethe_b2_transkription.pdf")
    },
    {
        "url": "https://goethemp4s.akamaized.net/resources/files/mp310/pruefungstraining_1_hoeren_c1.mp3",
        "dest": os.path.join(RAW_GOETHE_DIR, "goethe_c1_hoeren.mp3")
    },
    {
        "url": "https://www.goethe.de/pro/relaunch/prf/materialien/C1/c1_modellsatz.pdf",
        "dest": os.path.join(RAW_GOETHE_DIR, "goethe_c1_transkription.pdf")
    }
]

def run():
    for item in ITEMS:
        dest = item["dest"]
        url = item["url"]
        name = os.path.basename(dest)
        if os.path.exists(dest) and os.path.getsize(dest) > 10000:
            print(f"[EXISTS] {name} ({os.path.getsize(dest):,} bytes)")
        else:
            print(f"[DOWNLOADING] {name} from {url}...")
            cmd = ["curl.exe", "-L", "-k", "-s", "-S", "--connect-timeout", "15", "-o", dest, url]
            ret = subprocess.run(cmd)
            if ret.returncode == 0 and os.path.exists(dest):
                print(f"  -> Downloaded: {os.path.getsize(dest):,} bytes.")
            else:
                print(f"  -> [ERROR] Failed to download {name}")

        # If it needs MP3 extraction
        if "mp3" in item:
            mp3_dest = item["mp3"]
            mp3_name = os.path.basename(mp3_dest)
            if os.path.exists(mp3_dest) and os.path.getsize(mp3_dest) > 10000:
                print(f"[AUDIO READY] {mp3_name} ({os.path.getsize(mp3_dest):,} bytes)")
            elif os.path.exists(dest) and os.path.getsize(dest) > 10000:
                print(f"[CONVERTING] Extracting audio: {name} -> {mp3_name}...")
                ffmpeg_cmd = [
                    FFMPEG_EXE, "-y", "-i", dest,
                    "-vn", "-c:a", "libmp3lame", "-q:a", "2",
                    mp3_dest
                ]
                conv = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if conv.returncode == 0:
                    print(f"  -> Converted MP3: {os.path.getsize(mp3_dest):,} bytes.")
                else:
                    print(f"  -> [CONVERSION ERROR]: {conv.stderr.decode('utf-8', errors='ignore')}")

if __name__ == "__main__":
    run()
