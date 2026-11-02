# -*- coding: utf-8 -*-
"""
Updates data_a1_a2.py, data_b1_b2.py, data_c1_td.py with the calibrated tracks
from apply_all_calibrations.py
"""
import os
import sys
import json
import pprint

sys.path.insert(0, os.path.dirname(__file__))
from apply_all_calibrations import CALIBRATIONS
from data_a1_a2 import TRACKS_A1_A2
from data_b1_b2 import TRACKS_B1_B2
from data_c1_td import TRACKS_C1_TD

def update_tracks(track_list):
    for t in track_list:
        tid = t["id"]
        c = CALIBRATIONS.get(tid)
        if not c:
            continue
        ss = float(c["ss"])
        to = float(c["to"])
        dur = round(to - ss, 2)
        t1 = c["t1"]
        t2 = c["t2"]
        
        t["ss"] = str(ss)
        t["to"] = str(to)
        
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
            
        t["segments"][0]["startTime"] = 0.0
        t["segments"][0]["endTime"] = t1
        t["segments"][1]["startTime"] = t1
        t["segments"][1]["endTime"] = t2
        t["segments"][2]["startTime"] = t2
        t["segments"][2]["endTime"] = dur

def format_file(var_name, tracks, header):
    content = header.strip() + f"\n\n{var_name} = "
    formatted = pprint.pformat(tracks, indent=4, width=120, sort_dicts=False)
    # Replace raw path strings with variables for clean readability
    formatted = formatted.replace(r"'D:\\GermanCorpus\\raw\\goethe\\goethe_a1_hoeren.mp3'", "GOETHE_A1_FILE")
    formatted = formatted.replace(r"'D:\\GermanCorpus\\raw\\goethe\\goethe_a2_hoeren.mp3'", "GOETHE_A2_FILE")
    formatted = formatted.replace(r"'D:\\GermanCorpus\\raw\\goethe\\goethe_b1_hoeren.mp3'", "GOETHE_B1_FILE")
    formatted = formatted.replace(r"'D:\\GermanCorpus\\raw\\goethe\\goethe_b2_hoeren.mp3'", "GOETHE_B2_FILE")
    formatted = formatted.replace(r"'D:\\GermanCorpus\\raw\\goethe\\goethe_c1_hoeren.mp3'", "GOETHE_C1_FILE")
    formatted = formatted.replace(r"'D:\\GermanCorpus\\raw\\testdaf\\testdaf_modellsatz_01_hv.mp3'", "TESTDAF_01_FILE")
    formatted = formatted.replace(r"'D:\\GermanCorpus\\raw\\testdaf\\testdaf_modellsatz_02_hv.mp3'", "TESTDAF_02_FILE")
    return content + formatted + "\n"

# Update A1/A2
update_tracks(TRACKS_A1_A2)
a1_a2_header = """# -*- coding: utf-8 -*-
import os

RAW_GOETHE = r"D:\\GermanCorpus\\raw\\goethe"
GOETHE_A1_FILE = os.path.join(RAW_GOETHE, "goethe_a1_hoeren.mp3")
GOETHE_A2_FILE = os.path.join(RAW_GOETHE, "goethe_a2_hoeren.mp3")
"""
with open("scripts/data_a1_a2.py", "w", encoding="utf-8") as f:
    f.write(format_file("TRACKS_A1_A2", TRACKS_A1_A2, a1_a2_header))

# Update B1/B2
update_tracks(TRACKS_B1_B2)
b1_b2_header = """# -*- coding: utf-8 -*-
import os

RAW_GOETHE = r"D:\\GermanCorpus\\raw\\goethe"
GOETHE_B1_FILE = os.path.join(RAW_GOETHE, "goethe_b1_hoeren.mp3")
GOETHE_B2_FILE = os.path.join(RAW_GOETHE, "goethe_b2_hoeren.mp3")
"""
with open("scripts/data_b1_b2.py", "w", encoding="utf-8") as f:
    f.write(format_file("TRACKS_B1_B2", TRACKS_B1_B2, b1_b2_header))

# Update C1/TD
update_tracks(TRACKS_C1_TD)
c1_td_header = """# -*- coding: utf-8 -*-
import os

RAW_GOETHE = r"D:\\GermanCorpus\\raw\\goethe"
RAW_TESTDAF = r"D:\\GermanCorpus\\raw\\testdaf"

GOETHE_C1_FILE = os.path.join(RAW_GOETHE, "goethe_c1_hoeren.mp3")
TESTDAF_01_FILE = os.path.join(RAW_TESTDAF, "testdaf_modellsatz_01_hv.mp3")
TESTDAF_02_FILE = os.path.join(RAW_TESTDAF, "testdaf_modellsatz_02_hv.mp3")
"""
with open("scripts/data_c1_td.py", "w", encoding="utf-8") as f:
    f.write(format_file("TRACKS_C1_TD", TRACKS_C1_TD, c1_td_header))

print("Successfully updated data_a1_a2.py, data_b1_b2.py, and data_c1_td.py!")
