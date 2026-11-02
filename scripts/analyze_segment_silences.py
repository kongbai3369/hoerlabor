import subprocess
import re

FFMPEG = r"C:\Users\king\AppData\Local\Python\pythoncore-3.15-64\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

CANDIDATES = [
    # (name, file, start, end)
    ("Goethe A1 - Einkaufen", r"D:\GermanCorpus\raw\goethe\goethe_a1_hoeren.mp3", 126.4, 153.0),
    ("Goethe A1 - Bahnhof", r"D:\GermanCorpus\raw\goethe\goethe_a1_hoeren.mp3", 195.9, 222.0),
    ("Goethe A2 - Freizeit", r"D:\GermanCorpus\raw\goethe\goethe_a2_hoeren.mp3", 81.2, 104.3),
    ("Goethe A2 - Wohnung", r"D:\GermanCorpus\raw\goethe\goethe_a2_hoeren.mp3", 154.2, 176.0),
    ("Goethe B1 - Urlaub", r"D:\GermanCorpus\raw\goethe\goethe_b1_hoeren.mp3", 45.3, 73.0),
    ("Goethe B1 - Arztpraxis", r"D:\GermanCorpus\raw\goethe\goethe_b1_hoeren.mp3", 148.1, 170.2),
    ("Goethe B1 - Bewerbung", r"D:\GermanCorpus\raw\goethe\goethe_b1_hoeren.mp3", 246.7, 275.4),
    ("Goethe B2 - Ferienprogramm", r"D:\GermanCorpus\raw\goethe\goethe_b2_hoeren.mp3", 94.0, 131.7),
    ("Goethe B2 - Praktikum", r"D:\GermanCorpus\raw\goethe\goethe_b2_hoeren.mp3", 157.5, 190.5),
    ("Goethe B2 - Romane", r"D:\GermanCorpus\raw\goethe\goethe_b2_hoeren.mp3", 215.5, 245.0),
    ("Goethe C1 - Autorenlesung", r"D:\GermanCorpus\raw\goethe\goethe_c1_hoeren.mp3", 140.7, 175.0),
    ("TestDaF 01 - Musikstudium", r"D:\GermanCorpus\raw\testdaf\testdaf_modellsatz_01_hv.mp3", 104.1, 128.0),
    ("TestDaF 01 - Assessment", r"D:\GermanCorpus\raw\testdaf\testdaf_modellsatz_01_hv.mp3", 434.3, 465.0),
    ("TestDaF 02 - Radrennen", r"D:\GermanCorpus\raw\testdaf\testdaf_modellsatz_02_hv.mp3", 108.7, 132.0),
    ("TestDaF 02 - Kunstdidaktik", r"D:\GermanCorpus\raw\testdaf\testdaf_modellsatz_02_hv.mp3", 417.6, 445.0),
]

for name, fpath, start_t, end_t in CANDIDATES:
    cmd = [
        FFMPEG, "-ss", str(start_t), "-to", str(end_t), "-i", fpath,
        "-af", "silencedetect=noise=-30dB:d=0.35",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True, errors="ignore")
    dur = end_t - start_t
    print(f"\n>>> {name} (Duration: {dur:.1f}s) <<<")
    for line in res.stderr.split("\n"):
        if "silence_end:" in line:
            m = re.search(r"silence_start:\s*([\d\.]+).*silence_end:\s*([\d\.]+).*silence_duration:\s*([\d\.]+)", line)
            if m:
                print(f"  Pause at {float(m.group(1)):.2f}s - {float(m.group(2)):.2f}s (dur: {float(m.group(3)):.2f}s)")
