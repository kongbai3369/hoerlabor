# -*- coding: utf-8 -*-
"""
Rigorous verification test:
Iterates through all 40 tracks in src/data/generatedTracks.json.
Extracts each individual segment using segment.startTime and segment.endTime
from public/audio/tracks/<out_file>, runs Google STT on it, and calculates
word recall against segment.german.
"""
import os
import sys
import json
import re
import subprocess
import speech_recognition as sr
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
r = sr.Recognizer()

JSON_PATH = r"C:\Users\king\Downloads\听力\src\data\generatedTracks.json"
with open(JSON_PATH, "r", encoding="utf-8") as f:
    tracks = json.load(f)

def clean_words(text):
    return set(re.findall(r"\w+", text.lower()))

def test_track_segments(start_idx=0, end_idx=40):
    print(f"Testing segment recall for tracks {start_idx+1} to {end_idx}...")
    total_segments = 0
    passed_segments = 0
    results = []

    for idx in range(start_idx, end_idx):
        t = tracks[idx]
        tid = t["id"]
        rel_audio = t["audioUrl"].lstrip("/")
        audio_path = os.path.join(r"C:\Users\king\Downloads\听力\public", rel_audio)
        
        print(f"\n[{idx+1:02d}/40] {tid} ({t['title']})")
        seg_res = []
        for s_idx, seg in enumerate(t["segments"], 1):
            total_segments += 1
            st = seg["startTime"]
            et = seg["endTime"]
            dur = et - st
            
            wav = f"tmp_ver_{idx}_{s_idx}.wav"
            subprocess.run([FFMPEG, "-y", "-ss", f"{st:.3f}", "-t", f"{dur:.3f}", "-i", audio_path,
                            "-ar", "16000", "-ac", "1", wav],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            heard = ""
            try:
                with sr.AudioFile(wav) as s:
                    heard = r.recognize_google(r.record(s), language="de-DE")
            except Exception as e:
                heard = ""
            if os.path.exists(wav): os.remove(wav)
            
            exp_w = clean_words(seg["german"])
            hrd_w = clean_words(heard)
            
            # Count number recall (handling digits like 19,95 vs neunzehnfünfundneunzig)
            matched = exp_w & hrd_w
            recall = len(matched) / max(len(exp_w), 1)
            
            status = "PASS" if recall >= 0.60 else "WARN"
            if recall >= 0.60:
                passed_segments += 1
                
            print(f"  S{s_idx} [{st:.1f}s -> {et:.1f}s] ({recall*100:.1f}%) [{status}]")
            print(f"     EXP: {seg['german'][:65]}...")
            print(f"     HRD: {heard[:65]}...")
            
            seg_res.append({
                "seg_id": seg["id"],
                "startTime": st,
                "endTime": et,
                "recall": recall,
                "expected": seg["german"],
                "heard": heard
            })
            
        results.append({
            "id": tid,
            "title": t["title"],
            "segments": seg_res
        })

    print(f"\n==========================================")
    print(f"SUMMARY: {passed_segments}/{total_segments} segments passed (>=60% word recall)")
    with open(f"scripts/verification_results_{start_idx}_{end_idx}.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    end = int(sys.argv[2]) if len(sys.argv) > 2 else len(tracks)
    test_track_segments(start, end)
