# -*- coding: utf-8 -*-
"""
Precise calibrator for HörLabor tracks.
For a given track definition, it finds:
1. Exact speech start (ss) and end (to) in raw audio
2. Exact sentence boundaries (T1, T2) within the sliced clip
3. Verifies each of the 3 segments with Google Speech-to-Text
"""

import sys
import os
import re
import json
import subprocess
import speech_recognition as sr
import imageio_ffmpeg

sys.stdout.reconfigure(line_buffering=True)
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
r = sr.Recognizer()

def get_silences(audio_path, noise_db=-30, min_dur=0.2):
    cmd = [
        FFMPEG, "-i", audio_path,
        "-af", f"silencedetect=noise={noise_db}dB:d={min_dur}",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True, errors="ignore")
    silences = []
    # silence_start: X ... silence_end: Y ... silence_duration: Z
    cur_start = None
    for line in res.stderr.splitlines():
        if "silence_start:" in line:
            m = re.search(r"silence_start:\s*([\d\.]+)", line)
            if m: cur_start = float(m.group(1))
        if "silence_end:" in line:
            m = re.search(r"silence_end:\s*([\d\.]+).*silence_duration:\s*([\d\.]+)", line)
            if m:
                end_t = float(m.group(1))
                dur = float(m.group(2))
                start_t = cur_start if cur_start is not None else end_t - dur
                silences.append((start_t, end_t, dur))
                cur_start = None
    return silences

def stt_slice(audio_path, start, end):
    dur = end - start
    if dur <= 0.3:
        return ""
    wav = f"tmp_stt_{os.getpid()}.wav"
    subprocess.run([FFMPEG, "-y", "-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-i", audio_path,
                    "-ar", "16000", "-ac", "1", wav],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    txt = ""
    try:
        with sr.AudioFile(wav) as s:
            txt = r.recognize_google(r.record(s), language="de-DE")
    except Exception:
        txt = ""
    if os.path.exists(wav): os.remove(wav)
    return txt

def clean_words(text):
    return set(re.findall(r"\w+", text.lower()))

def score_match(expected_text, heard_text):
    exp = clean_words(expected_text)
    hrd = clean_words(heard_text)
    if not exp: return 1.0
    return len(exp & hrd) / len(exp)

if __name__ == "__main__":
    print("Calibrator module loaded.")
