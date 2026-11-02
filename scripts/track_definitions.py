# -*- coding: utf-8 -*-
"""
Central definition module for all 40 authentic listening comprehension tracks.
Exports:
- TRACK_DEFINITIONS: list of 40 track dictionaries
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from data_a1_a2 import TRACKS_A1_A2
from data_b1_b2 import TRACKS_B1_B2
from data_c1_td import TRACKS_C1_TD

TRACK_DEFINITIONS = TRACKS_A1_A2 + TRACKS_B1_B2 + TRACKS_C1_TD

if __name__ == "__main__":
    print(f"Total track definitions loaded: {len(TRACK_DEFINITIONS)}")
    for i, t in enumerate(TRACK_DEFINITIONS, 1):
        print(f"[{i:02d}/40] {t['id']} ({t['level']}) - {t['title']} ({t['ss']}s -> {t['to']}s)")
