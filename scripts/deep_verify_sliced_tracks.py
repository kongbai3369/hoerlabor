# -*- coding: utf-8 -*-
"""
Deep verification of all 40 sliced audio files in public/audio/tracks.
Performs Google Speech Recognition on each sliced audio file,
and checks word overlap against the German text in src/data/generatedTracks.json.
"""

import json
import os
import re
import subprocess
import speech_recognition as sr
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
JSON_PATH = r"C:\Users\king\Downloads\听力\src\data\generatedTracks.json"
PUBLIC_DIR = r"C:\Users\king\Downloads\听力\public"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    tracks = json.load(f)

r = sr.Recognizer()
wav_tmp = "deep_verify_tmp.wav"

def normalize_words(text):
    text = re.sub(r"[^\w\säöüÄÖÜß]", " ", text)
    return set(text.lower().split())

results = []
print(f"Deep verifying all {len(tracks)} tracks directly from sliced audio in public/audio/tracks...\n")

for idx, t in enumerate(tracks, 1):
    audio_path = os.path.join(PUBLIC_DIR, t["audioUrl"].lstrip("/"))
    assert os.path.exists(audio_path), f"Audio file not found: {audio_path}"

    # Convert sliced clip to 16kHz mono wav
    subprocess.run([FFMPEG, "-y", "-i", audio_path, "-ar", "16000", "-ac", "1", wav_tmp],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with sr.AudioFile(wav_tmp) as s:
        audio_data = r.record(s)

    try:
        stt_text = r.recognize_google(audio_data, language="de-DE")
    except Exception as e:
        stt_text = f"[STT Error: {e}]"

    # Full German transcript from the 3 segments
    full_german = " ".join(seg["german"] for seg in t["segments"])

    expected_words = normalize_words(full_german)
    actual_words = normalize_words(stt_text)

    overlap = expected_words.intersection(actual_words)
    recall = len(overlap) / max(len(expected_words), 1)

    status = "OK" if recall >= 0.40 else "WARN"
    results.append((t["id"], t["level"], recall, stt_text[:80]))

    print(f"[{idx:02d}/40] {t['id']} ({t['level']}) - Word Recall: {recall*100:.1f}% [{status}]")
    print(f"       Expected: {full_german[:70]}...")
    print(f"       Heard:    {stt_text[:70]}...")

if os.path.exists(wav_tmp):
    os.remove(wav_tmp)

print("\n" + "="*60)
print(f"Summary: {len(results)} tracks verified.")
low_recall = [r for r in results if r[2] < 0.35]
if low_recall:
    print(f"Tracks with lower than 35% recall: {low_recall}")
else:
    print("All 40 tracks have verified speech correspondence!")
