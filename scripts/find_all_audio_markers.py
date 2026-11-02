import subprocess
import re
import os

FFMPEG = r"C:\Users\king\AppData\Local\Python\pythoncore-3.15-64\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

FILES = [
    ("Goethe A1", r"D:\GermanCorpus\raw\goethe\goethe_a1_hoeren.mp3", 400),
    ("Goethe A2", r"D:\GermanCorpus\raw\goethe\goethe_a2_hoeren.mp3", 400),
    ("Goethe B1", r"D:\GermanCorpus\raw\goethe\goethe_b1_hoeren.mp3", 400),
    ("Goethe B2", r"D:\GermanCorpus\raw\goethe\goethe_b2_hoeren.mp3", 400),
    ("Goethe C1", r"D:\GermanCorpus\raw\goethe\goethe_c1_hoeren.mp3", 400),
    ("TestDaF 01", r"D:\GermanCorpus\raw\testdaf\testdaf_modellsatz_01_hv.mp3", 600),
    ("TestDaF 02", r"D:\GermanCorpus\raw\testdaf\testdaf_modellsatz_02_hv.mp3", 600),
]

def analyze_audio(name, path, duration_sec):
    print(f"\n=================== {name} ({duration_sec}s) ===================")
    cmd = [
        FFMPEG, "-t", str(duration_sec), "-i", path,
        "-af", "silencedetect=noise=-30dB:d=0.9",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True, errors="ignore")
    
    silences = []
    for line in res.stderr.split("\n"):
        if "silence_start:" in line:
            m = re.search(r"silence_start:\s*([\d\.]+)", line)
            if m:
                s_start = float(m.group(1))
        elif "silence_end:" in line:
            m = re.search(r"silence_end:\s*([\d\.]+)\s*\|\s*silence_duration:\s*([\d\.]+)", line)
            if m:
                s_end = float(m.group(1))
                s_dur = float(m.group(2))
                silences.append((s_start, s_end, s_dur))
    
    # Identify speech blocks between silences
    print(f"Total silence events: {len(silences)}")
    long_pauses = [s for s in silences if s[2] >= 3.0]
    print(f"Long pauses (>=3s, e.g. task transitions / reading pauses): {len(long_pauses)}")
    for s in long_pauses:
        print(f"  Pause: {s[0]:.2f}s -> {s[1]:.2f}s (duration: {s[2]:.2f}s)")

if __name__ == "__main__":
    for name, path, dur in FILES:
        analyze_audio(name, path, dur)
