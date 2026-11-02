# -*- coding: utf-8 -*-
"""
Master calibrator and audio slicer for all 40 HörLabor tracks.
Applies decisecond-accurate start/end boundaries, intra-track sentence timestamps,
and verbatim transcript corrections. Re-slices all 40 MP3s with ffmpeg libmp3lame.
"""
import os
import sys
import json
import shutil
import subprocess
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

PUBLIC_TRACKS_DIR = r"C:\Users\king\Downloads\听力\public\audio\tracks"
PROCESSED_TRACKS_DIR = r"D:\GermanCorpus\processed\tracks"
GENERATED_TRACKS_JSON = r"C:\Users\king\Downloads\听力\src\data\generatedTracks.json"

os.makedirs(PUBLIC_TRACKS_DIR, exist_ok=True)
os.makedirs(PROCESSED_TRACKS_DIR, exist_ok=True)

sys.path.insert(0, os.path.dirname(__file__))
from data_a1_a2 import TRACKS_A1_A2
from data_b1_b2 import TRACKS_B1_B2
from data_c1_td import TRACKS_C1_TD

# 40 Track calibration definitions
CALIBRATIONS = {
    # Goethe A1
    "goethe-a1-pullover-01": {"ss": "127.3", "to": "147.2", "t1": 6.8, "t2": 11.4},
    "goethe-a1-buero-02": {"ss": "50.4", "to": "75.8", "t1": 4.6, "t2": 11.2},
    "goethe-a1-restaurant-03": {"ss": "248.8", "to": "275.2", "t1": 6.2, "t2": 12.5},
    "goethe-a1-treppe-04": {"ss": "383.0", "to": "396.5", "t1": 5.0, "t2": 7.1},
    "goethe-a1-reisebus-05": {"ss": "600.2", "to": "616.2", "t1": 5.2, "t2": 10.6},
    "goethe-a1-flughafen-06": {"ss": "683.0", "to": "698.0", "t1": 9.0, "t2": 11.4},

    # Goethe A2
    "goethe-a2-olympia-01": {"ss": "84.5", "to": "96.8", "t1": 6.5, "t2": 9.1},
    "goethe-a2-bus-02": {"ss": "96.8", "to": "105.5", "t1": 3.0, "t2": 4.2},
    "goethe-a2-anzug-03": {"ss": "155.8", "to": "177.0", "t1": 6.6, "t2": 13.8},
    "goethe-a2-wetter-04": {"ss": "306.0", "to": "329.5", "t1": 6.8, "t2": 15.0},
    "goethe-a2-reparatur-05": {"ss": "818.0", "to": "842.0", "t1": 7.8, "t2": 15.5},
    "goethe-a2-praxis-06": {"ss": "868.0", "to": "892.0", "t1": 5.0, "t2": 15.0},

    # Goethe B1
    "goethe-b1-urlaub-01": {"ss": "46.2", "to": "75.5", "t1": 6.1, "t2": 15.3},
    "goethe-b1-praxis-02": {"ss": "144.8", "to": "177.0", "t1": 6.9, "t2": 22.0},
    "goethe-b1-bewerbung-03": {"ss": "247.3", "to": "275.5", "t1": 5.2, "t2": 12.9},
    "goethe-b1-verkehr-04": {"ss": "332.4", "to": "368.0", "t1": 11.5, "t2": 16.2},
    "goethe-b1-bahnhof-05": {"ss": "480.2", "to": "522.0", "t1": 23.1, "t2": 32.8},
    "goethe-b1-wetter-06": {"ss": "547.0", "to": "585.0", "t1": 12.95, "t2": 22.7},
    "goethe-b1-museum-07": {"ss": "744.2", "to": "771.0", "t1": 8.5, "t2": 16.5},
    "goethe-b1-krippe-08": {
        "ss": "1370.2", "to": "1403.0", "t1": 2.25, "t2": 15.9,
        "seg3_german": "Das soziale Miteinander lernen die Kinder sowieso später. Mein fünfjähriger Sohn geht seit einem Jahr in den Kindergarten und lernt jetzt, wie er mit anderen Kindern zusammen spielen kann. Unter drei Jahren brauchen Kinder keine gleichaltrigen Kinder, sondern vor allem ihre Bezugsperson.",
        "seg3_chinese": "孩子们无论如何以后都会学会人际交往。我五岁的儿子上一年前进幼儿园，现在正在学习如何与其他孩子一起玩耍。三岁以下的孩子不需要同龄玩伴，而是首先需要他们的固定监护人。",
        "seg3_cloze": ["Miteinander", "später", "fünfjähriger", "Kindergarten", "spielen", "Bezugsperson"]
    },

    # Goethe B2
    "goethe-b2-ferien-01": {"ss": "93.5", "to": "131.3", "t1": 17.5, "t2": 29.0},
    "goethe-b2-praktikum-02": {"ss": "283.5", "to": "322.0", "t1": 17.1, "t2": 26.0},
    "goethe-b2-lesen-03": {"ss": "157.5", "to": "190.7", "t1": 12.2, "t2": 23.8},
    "goethe-b2-radfahrer-04": {"ss": "353.5", "to": "391.7", "t1": 13.0, "t2": 22.8},
    "goethe-b2-ernaehrung-05": {"ss": "808.5", "to": "838.2", "t1": 9.8, "t2": 18.6},
    "goethe-b2-insekten-06": {"ss": "663.0", "to": "696.5", "t1": 12.2, "t2": 23.2},
    "goethe-b2-studium-07": {"ss": "1152.5", "to": "1174.9", "t1": 4.8, "t2": 12.0},
    "goethe-b2-arbeit-08": {
        "ss": "1664.8", "to": "1693.5", "t1": 9.8, "t2": 15.0,
        "seg1_german": "Zusammenfassend kann ich nur sagen: Es ist wichtig, Ablenkungen als solche zu erkennen und wenn möglich gar nicht erst entstehen zu lassen.",
        "seg1_chinese": "总而言之我只能说：认清这些干扰因素的本质，并且尽可能不让它们产生，这一点至关重要。",
        "seg1_cloze": ["Zusammenfassend", "wichtig", "Ablenkungen", "erkennen", "entstehen"],
        "seg2_german": "Es geht nicht darum, in Zukunft nicht mehr auf äußere Einflüsse zu reagieren.",
        "seg2_chinese": "这并不是说将来对任何外界影响都完全置之不理。",
        "seg2_cloze": ["Zukunft", "äußere", "Einflüsse", "reagieren"],
        "seg3_german": "Meiner Meinung nach reicht es beispielsweise, die E-Mails alle zwei bis drei Stunden anzusehen und dazwischen voll konzentriert zu arbeiten. Herzlichen Dank für Ihre Aufmerksamkeit, meine Damen und Herren.",
        "seg3_chinese": "依我拙见，比如每两到三小时集中查看一次电子邮件，而在两次查看之间全神贯注地投入工作就足够了。女士们先生们，非常感谢各位的聆听。",
        "seg3_cloze": ["Meinung", "E-Mails", "Stunden", "konzentriert", "Aufmerksamkeit"]
    },

    # Goethe C1
    "goethe-c1-literatur-01": {"ss": "139.5", "to": "177.5", "t1": 15.1, "t2": 29.1},
    "goethe-c1-kochschule-02": {"ss": "234.0", "to": "278.5", "t1": 14.85, "t2": 28.14},
    "goethe-c1-leselust-03": {"ss": "309.5", "to": "347.5", "t1": 7.22, "t2": 16.95},
    "goethe-c1-fantasie-04": {"ss": "557.0", "to": "580.0", "t1": 3.68, "t2": 16.42},
    "goethe-c1-kinderbuch-05": {"ss": "580.8", "to": "607.0", "t1": 7.4, "t2": 15.3},
    "goethe-c1-urbanistik-06": {
        "ss": "1096.0", "to": "1124.8", "t1": 10.3, "t2": 19.8,
        "seg1_german": "Willkommen zu unserer Sendung „Unsere Zukunft neu gedacht“. Wir widmen uns heute der Frage, wie wir in Zukunft wohnen wollen.",
        "seg1_chinese": "欢迎收听《重新构想未来》节目。今天我们聚焦于一个命题：未来我们究竟想要怎样的居住模式。",
        "seg1_cloze": ["Sendung", "Zukunft", "widmen", "wohnen"],
        "seg2_german": "Eingeladen haben wir Frau Dr. Kuhn, Soziologin an der Universität Leipzig und Herrn Hoffmann, Architekt und Städteplaner aus Köln. Guten Tag, hallo.",
        "seg2_chinese": "今天我们邀请到了莱比锡大学社会学学者库恩博士，以及来自科隆的建筑师兼城市规划专家霍夫曼先生。二位好！",
        "seg2_cloze": ["Soziologin", "Universität", "Architekt", "Städteplaner"],
        "seg3_german": "Frau Dr. Kuhn, in Ihrer jüngsten Publikation fordern Sie neue Leitbilder für das Wohnen. Können Sie das näher erläutern?",
        "seg3_chinese": "库恩博士，在您最新的著述中，您呼吁树立全新的人居导向理念。您能就此展开说明一下吗？",
        "seg3_cloze": ["Publikation", "fordern", "Leitbilder", "Wohnen", "erläutern"]
    },

    # TestDaF
    "testdaf-musikstudium-01": {"ss": "104.0", "to": "140.0", "t1": 10.44, "t2": 18.0},
    "testdaf-assessment-02": {"ss": "434.0", "to": "465.0", "t1": 10.04, "t2": 20.58},
    "testdaf-campusleben-05": {
        "ss": "165.0", "to": "198.8", "t1": 6.29, "t2": 17.74,
        "seg3_german": "Und wie kommt es, dass du hier studierst? – Die Atmosphäre an der Hochschule ist einfach etwas Besonderes... Ich habe mal ein Konzert hier besucht, das Studierende der Hochschule organisiert hatten – danach habe ich mich direkt zum nächsten Semester beworben.",
        "seg3_chinese": "那你是怎么来这里读大学的呢？——学院里的氛围非常特别……我曾经在这里听过一场由在校学生组织的音乐会——之后我就直接报名申请了下一个学期。",
        "seg3_cloze": ["Atmosphäre", "Hochschule", "Konzert", "Studierende", "Semester", "beworben"]
    },
    "testdaf-radrennen-03": {"ss": "108.0", "to": "137.7", "t1": 11.31, "t2": 19.83},
    "testdaf-kunstdidaktik-04": {"ss": "417.0", "to": "461.0", "t1": 9.76, "t2": 23.03},
    "testdaf-virus-06": {"ss": "1250.0", "to": "1280.6", "t1": 9.06, "t2": 19.84}
}

def apply_and_slice():
    all_raw_tracks = TRACKS_A1_A2 + TRACKS_B1_B2 + TRACKS_C1_TD
    print(f"Total input tracks: {len(all_raw_tracks)}")
    
    calibrated_tracks = []
    
    for idx, t in enumerate(all_raw_tracks):
        tid = t["id"]
        c = CALIBRATIONS.get(tid)
        if not c:
            print(f"[WARN] No calibration for {tid}")
            calibrated_tracks.append(t)
            continue
            
        ss = float(c["ss"])
        to = float(c["to"])
        dur = round(to - ss, 2)
        t1 = c["t1"]
        t2 = c["t2"]
        
        t["ss"] = str(ss)
        t["to"] = str(to)
        
        # Apply transcript adjustments if any
        if "seg1_german" in c:
            t["segments"][0]["german"] = c["seg1_german"]
            t["segments"][0]["chinese"] = c["seg1_chinese"]
            t["segments"][0]["clozeWords"] = c["seg1_cloze"]
        if "seg2_german" in c:
            t["segments"][1]["german"] = c["seg2_german"]
            t["segments"][1]["chinese"] = c["seg2_chinese"]
            t["segments"][1]["clozeWords"] = c["seg2_cloze"]
        if "seg3_german" in c:
            t["segments"][2]["german"] = c["seg3_german"]
            t["segments"][2]["chinese"] = c["seg3_chinese"]
            t["segments"][2]["clozeWords"] = c["seg3_cloze"]
            
        # Update segment timestamps
        t["segments"][0]["startTime"] = 0.0
        t["segments"][0]["endTime"] = t1
        t["segments"][1]["startTime"] = t1
        t["segments"][1]["endTime"] = t2
        t["segments"][2]["startTime"] = t2
        t["segments"][2]["endTime"] = dur
        
        # Audio slicing
        out_name = t["out_file"]
        proc_path = os.path.join(PROCESSED_TRACKS_DIR, out_name)
        pub_path = os.path.join(PUBLIC_TRACKS_DIR, out_name)
        
        raw_source = t["raw_file"]
        print(f"[{idx+1:02d}/40] Slicing {tid} ({ss}s -> {to}s, dur={dur}s) -> {out_name}...")
        
        cmd = [
            FFMPEG, "-y",
            "-ss", str(ss),
            "-to", str(to),
            "-i", raw_source,
            "-c:a", "libmp3lame",
            "-b:a", "128k",
            proc_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        def safe_copy(src, dst):
            try:
                if os.path.exists(dst):
                    os.remove(dst)
            except Exception:
                pass
            try:
                shutil.copy2(src, dst)
            except Exception:
                with open(src, "rb") as fs, open(dst, "wb") as fd:
                    fd.write(fs.read())

        if res.returncode != 0:
            print(f"  [ERROR] ffmpeg slice failed for {tid}")
        else:
            safe_copy(proc_path, pub_path)
            
        # Prepare track entry for generatedTracks.json
        # Format matching src/data/generatedTracks.json
        json_track = {
            "id": t["id"],
            "title": t["title"],
            "level": t["level"],
            "source": t["source"],
            "topic": t["topic"],
            "taskSection": t.get("taskSection", f"{t['level']} · {t['title']}"),
            "audioUrl": f"/audio/tracks/{out_name}",
            "duration": round(dur, 2),
            "segments": t["segments"]
        }
        calibrated_tracks.append(json_track)

    # Save to src/data/generatedTracks.json
    with open(GENERATED_TRACKS_JSON, "w", encoding="utf-8") as f:
        json.dump(calibrated_tracks, f, ensure_ascii=False, indent=2)
    print(f"\n[SUCCESS] Successfully written 40 calibrated tracks to {GENERATED_TRACKS_JSON}")

if __name__ == "__main__":
    apply_and_slice()
