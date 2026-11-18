# -*- coding: utf-8 -*-
"""
Targeted fix & completion script: keeps all tracks in aligned_candidates.json with min_rec >= 0.72,
re-aligns only the 6 tracks that had boundary drift/skipped turns or transient STT drops,
and tops up Nachrichtenleicht to 6 clean verified tracks.
"""

import os
import re
import json
import time
import shutil
import subprocess
import requests
import imageio_ffmpeg
import speech_recognition as sr
from lxml import html
from mutagen.mp3 import MP3

import sys
sys.path.insert(0, os.path.dirname(__file__))
import build_aligned_candidates as bac

STAGING_FILE = r"D:\GermanCorpus\staging\aligned_candidates.json"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
REC = sr.Recognizer()


def reliable_stt_slice(audio_path: str, start: float, end: float) -> str:
    dur = end - start
    if dur <= 0.35:
        return ""
    wav = os.path.join(bac.STAGING_DIR, f"tmp_rstt_{os.getpid()}.wav")
    for attempt in range(2):
        ss = max(0.0, start - (0.15 if attempt == 1 else 0.0))
        d = dur + (0.30 if attempt == 1 else 0.0)
        subprocess.run(
            [FFMPEG, "-y", "-ss", f"{ss:.3f}", "-t", f"{d:.3f}",
             "-i", audio_path, "-ar", "16000", "-ac", "1", wav],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        try:
            with sr.AudioFile(wav) as s:
                txt = REC.recognize_google(REC.record(s), language="de-DE")
            if txt.strip():
                if os.path.exists(wav): os.remove(wav)
                return txt
        except sr.RequestError:
            time.sleep(0.8)
        except Exception:
            pass
    if os.path.exists(wav):
        os.remove(wav)
    return ""


# Monkeypatch stt_slice inside bac so align_sentences_in_range inherits retries
bac.stt_slice = reliable_stt_slice


def align_with_wider_search(audio_path: str, sentences: list[str], t_start: float, t_end: float) -> list[dict]:
    n = len(sentences)
    silences = bac.get_silences(audio_path, ss=max(0.0, t_start - 0.5), to=t_end + 0.5, noise_db=-32, min_dur=0.16)
    mids = sorted(set([round((s[0] + s[1]) / 2, 2) for s in silences if t_start + 1.0 < (s[0] + s[1]) / 2 < t_end - 1.0]))

    total_chars = sum(max(len(s), 10) for s in sentences)
    total_dur = t_end - t_start
    boundaries = [round(t_start, 2)]
    cum = 0
    for i in range(n - 1):
        cum += max(len(sentences[i]), 10)
        est = t_start + total_dur * (cum / total_chars)
        prev_b = boundaries[-1]
        min_b = prev_b + 1.4
        max_b = t_end - 1.4 * (n - 1 - i)
        valid_mids = [m for m in mids if min_b <= m <= max_b]
        if valid_mids:
            chosen = min(valid_mids, key=lambda m: abs(m - est))
            if abs(chosen - est) > 4.5:
                chosen = round(est, 2)
        else:
            chosen = round(est, 2)
        boundaries.append(round(chosen, 2))
    boundaries.append(round(t_end, 2))

    for _pass in range(3):
        improved = False
        for i in range(n - 1):
            s_a, b, s_b = boundaries[i], boundaries[i + 1], boundaries[i + 2]
            r_a = bac.word_recall(sentences[i], reliable_stt_slice(audio_path, s_a, b))
            r_b = bac.word_recall(sentences[i + 1], reliable_stt_slice(audio_path, b, s_b))
            cur_min, cur_sum = min(r_a, r_b), r_a + r_b
            if r_a >= 0.85 and r_b >= 0.85:
                continue
            cands = [m for m in mids if s_a + 1.4 <= m <= s_b - 1.4 and abs(m - b) <= 10.5 and m != b]
            cands.sort(key=lambda m: abs(m - b))
            for cand in cands[:8]:
                nr_a = bac.word_recall(sentences[i], reliable_stt_slice(audio_path, s_a, cand))
                nr_b = bac.word_recall(sentences[i + 1], reliable_stt_slice(audio_path, cand, s_b))
                n_min, n_sum = min(nr_a, nr_b), nr_a + nr_b
                if (n_min > cur_min + 0.04) or (n_min >= cur_min and n_sum > cur_sum + 0.06):
                    boundaries[i + 1] = round(cand, 2)
                    cur_min, cur_sum = n_min, n_sum
                    improved = True
                    break
        if not improved:
            break

    aligned = []
    for i, sent in enumerate(sentences):
        st, et = boundaries[i], boundaries[i + 1]
        heard = reliable_stt_slice(audio_path, st, et)
        rec = bac.word_recall(sent, heard)
        aligned.append({
            "german": sent,
            "startTime": round(st, 2),
            "endTime": round(et, 2),
            "sttHeard": heard,
            "sttRecall": round(rec, 3),
        })
    return aligned


def safe_find_t0_and_t1(audio_path: str, sentences: list[str], search_start: float, search_end: float) -> tuple[float, float]:
    dur = bac.get_audio_duration(audio_path)
    # Find EARLIEST window containing unique start tokens of sentences[0]
    sils = bac.get_silences(audio_path, ss=max(0.0, search_start - 1.0), to=min(dur, search_end + 35.0), noise_db=-32, min_dur=0.18)
    mids = sorted(set([round(search_start, 2)] + [round((a + b) / 2, 2) for a, b, _ in sils if search_start - 0.5 <= (a + b) / 2 <= search_end]))

    # Scan stepping by 8s to find where sentences[0] appears FIRST
    first_hit = search_start
    best_r = 0.0
    t = search_start
    while t < min(dur - 2.0, search_end):
        h = reliable_stt_slice(audio_path, t, min(dur, t + 18.0))
        r0 = bac.word_recall(sentences[0], h)
        if r0 > best_r:
            best_r = r0
            first_hit = t
        if r0 >= 0.72:
            first_hit = t
            break
        t += 6.0

    # Look around [first_hit - 5, first_hit + 10] and ensure [w_s, m] did NOT already speak s0
    w_s = max(search_start, first_hit - 5.0)
    cand_mids = [m for m in mids if w_s <= m <= first_hit + 10.0]
    if not cand_mids:
        cand_mids = [round(first_hit, 2)]

    s0_dur = max(10.0, min(18.0, len(sentences[0]) / 6.0 + 4.0))
    t0 = cand_mids[0]
    peak = 0.0
    for m in cand_mids:
        if m - w_s > 2.5:
            pre = reliable_stt_slice(audio_path, w_s, m)
            if bac.word_recall(sentences[0], pre) >= 0.45:
                break
        r = bac.word_recall(sentences[0], reliable_stt_slice(audio_path, m, min(dur, m + s0_dur)))
        if r >= peak:
            peak = r
        if r >= max(0.60, peak * 0.85):
            t0 = m
        elif peak >= 0.55:
            break

    # Now find t1
    est_dur = max(16.0, sum(len(s) for s in sentences) / 11.5)
    t_tail_start = max(t0 + est_dur * 0.65, t0 + 10.0)
    t_tail_end = min(dur, t0 + est_dur * 1.45 + 15.0)
    best_end_w = t_tail_start
    best_er = 0.0
    t = t_tail_start
    while t < min(dur - 2.0, t_tail_end):
        r = bac.word_recall(sentences[-1], reliable_stt_slice(audio_path, t, min(dur, t + 20.0)))
        if r > best_er:
            best_er = r
            best_end_w = t
        if r >= 0.75:
            best_end_w = t
            break
        t += 7.0

    ew_s = max(t0 + 8.0, best_end_w)
    ew_e = min(dur, best_end_w + 26.0)
    sils1 = bac.get_silences(audio_path, ss=ew_s, to=ew_e, noise_db=-32, min_dur=0.18)
    mids1 = sorted(set([round((a + b) / 2, 2) for a, b, _ in sils1 if ew_s <= (a + b) / 2 <= ew_e] + [round(ew_e, 2)]))
    sl_dur = max(10.0, min(20.0, len(sentences[-1]) / 6.0 + 4.0))
    cand_e = []
    max_er_seen = 0.0
    for m in mids1:
        r = bac.word_recall(sentences[-1], reliable_stt_slice(audio_path, max(t0, m - sl_dur), m))
        cand_e.append((m, r))
        if r > max_er_seen:
            max_er_seen = r
    t1 = mids1[-1]
    for m, r in cand_e:
        if r >= max(0.65, max_er_seen * 0.92):
            t1 = m
            break
    return round(t0, 2), round(t1, 2)


def main():
    existing = json.load(open(STAGING_FILE, encoding="utf-8"))
    kept = []
    by_id = {t["id"]: t for t in existing}

    FIX_IDS = {
        "sg-tempolimit-in-deutschland-sg-3",
        "sg-auf-wohnungssuche-in-deutschla",
        "dw-tt-79906631",
        "dw-lgn-79977343",
        "telc-b2-zugspitze-02",
        "telc-b2-kulturfestival-03",
    }

    for t in existing:
        if t["id"] not in FIX_IDS:
            kept.append(t)

    # 1. Fix sg-tempolimit (re-align cleanly across [5.0..48.5])
    if "sg-tempolimit-in-deutschland-sg-3" in by_id:
        t = by_id["sg-tempolimit-in-deutschland-sg-3"]
        sents = [s["german"] for s in t["alignedSegments"]]
        t0, t1 = safe_find_t0_and_t1(t["localAudioPath"], sents, 4.0, 25.0)
        t["alignedSegments"] = align_with_wider_search(t["localAudioPath"], sents, t0, t1)
        print("[FIX SG-Tempolimit]", t0, t1, [s["sttRecall"] for s in t["alignedSegments"]])
        kept.append(t)

    # 2. Fix sg-auf-wohnungssuche (re-align cleanly across [5.0..36.0])
    if "sg-auf-wohnungssuche-in-deutschla" in by_id:
        t = by_id["sg-auf-wohnungssuche-in-deutschla"]
        sents = [s["german"] for s in t["alignedSegments"]]
        t0, t1 = safe_find_t0_and_t1(t["localAudioPath"], sents, 4.5, 22.0)
        t["alignedSegments"] = align_with_wider_search(t["localAudioPath"], sents, t0, t1)
        print("[FIX SG-Wohnung]", t0, t1, [s["sttRecall"] for s in t["alignedSegments"]])
        kept.append(t)

    # 3. Fix dw-tt-79906631 (Holocaust: skip jingle at 0..12s, search_start=9.0)
    if "dw-tt-79906631" in by_id:
        t = by_id["dw-tt-79906631"]
        sents = [s["german"] for s in t["alignedSegments"]]
        t0, t1 = safe_find_t0_and_t1(t["localAudioPath"], sents, 9.0, 32.0)
        t["alignedSegments"] = align_with_wider_search(t["localAudioPath"], sents, t0, t1)
        print("[FIX DW-TT-Holocaust]", t0, t1, [s["sttRecall"] for s in t["alignedSegments"]])
        kept.append(t)

    # 4. Fix dw-lgn-79977343 (Alaska Senatssitz: headline starts ~13s right after clock!)
    if "dw-lgn-79977343" in by_id:
        t = by_id["dw-lgn-79977343"]
        sents = [s["german"] for s in t["alignedSegments"]]
        t0, t1 = safe_find_t0_and_t1(t["localAudioPath"], sents, 10.0, 26.0)
        t["alignedSegments"] = align_with_wider_search(t["localAudioPath"], sents, t0, t1)
        print("[FIX DW-LGN-Alaska]", t0, t1, [s["sttRecall"] for s in t["alignedSegments"]])
        kept.append(t)

    # 5. Fix telc-b2-zugspitze-02 (include skipped line "Wir haben ja unheimlich viel zu bieten...")
    telc_z_sents = [
        "Die Zugspitze sieht man zurzeit, wenn ich aus meinem Bürofenster rausschaue.",
        "Die Zugspitze ist tief verschneit, der Wettersteingrat ist auch verschneit, aber wie gesagt, weiter unten ist alles grün und es ist wirklich gut zum Anschauen.",
        "Was sagen eigentlich die Feriengäste zum schlechten Wetter in den Bergen? Maulen die eigentlich schon kräftig herum oder sagen die sich: „Na ja, wir machen was draus“?",
        "Na, das ist Gott sei Dank in Garmisch-Partenkirchen so, dass es genügend Alternativen gibt: Wir haben ja unheimlich viel zu bieten, und das schätzen die Leute.",
        "Es gibt ein Schwimmbad, es gibt ein Eisstadion, wo die Leute Schlittschuh laufen können, und es gibt 200 Kilometer Wanderwege, wo man auch bei Schlechtwetter was machen kann.",
    ]
    raw_b2 = r"D:\GermanCorpus\raw\telc\telc_b2_uebungstest1.mp3"
    ss_z, to_z = safe_find_t0_and_t1(raw_b2, telc_z_sents, 495.0, 540.0)
    pub_z = os.path.join(bac.PUB_TRACKS_DIR, "telc_b2_zugspitze_02.mp3")
    proc_z = os.path.join(bac.PROC_DIR, "telc_b2_zugspitze_02.mp3")
    subprocess.run([FFMPEG, "-y", "-ss", f"{max(0.0, ss_z - 0.15):.3f}", "-to", f"{to_z + 0.25:.3f}",
                    "-i", raw_b2, "-c:a", "libmp3lame", "-b:a", "128k", proc_z],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    shutil.copy2(proc_z, pub_z)
    dur_z = bac.get_audio_duration(pub_z)
    segs_z = align_with_wider_search(pub_z, telc_z_sents, 0.0, dur_z)
    print("[FIX TELC-Zugspitze]", ss_z, to_z, "dur=", round(dur_z, 2), [s["sttRecall"] for s in segs_z])
    tz = by_id["telc-b2-zugspitze-02"]
    tz["duration"] = round(dur_z, 2)
    tz["alignedSegments"] = segs_z
    kept.append(tz)

    # 6. Fix telc-b2-kulturfestival-03 cleanly with wider search (align_with_wider_search)
    tk = by_id["telc-b2-kulturfestival-03"]
    pub_k = tk["localAudioPath"]
    dur_k = bac.get_audio_duration(pub_k)
    sents_k = [s["german"] for s in tk["alignedSegments"]]
    tk["alignedSegments"] = align_with_wider_search(pub_k, sents_k, 0.0, dur_k)
    print("[FIX TELC-Kultur]", [s["sttRecall"] for s in tk["alignedSegments"]])
    kept.append(tk)

    # 7. Fetch 1 extra clean Nachrichtenleicht track if NL count < 6
    nl_count = sum(1 for x in kept if x["source"] == "Nachrichtenleicht")
    if nl_count < 6:
        print(f"\nCurrently have {nl_count} NL tracks, fetching 1 more verified NL article...")
        existing_ids = {x["id"] for x in kept}
        r = requests.get("https://www.nachrichtenleicht.de/", headers=bac.HEADERS, timeout=15)
        doc = html.fromstring(r.content)
        for url in [h for h in doc.xpath("//a[contains(@href, '-100.html')]/@href") if h.startswith("https://www.nachrichtenleicht.de/")]:
            try:
                ra = requests.get(url, headers=bac.HEADERS, timeout=15)
                m_mp3 = re.search(r'https://download\.deutschlandfunk\.de/[^\s"\'<>;&]+\.mp3', ra.text)
                if not m_mp3: continue
                mp3_url = m_mp3.group(0)
                adoc = html.fromstring(ra.content)
                title = re.sub(r"\s+", " ", re.sub(r"Podcast hören", "", " ".join(adoc.xpath("//h1//text()")))).strip()
                slug = bac.slugify(title, 32)
                tid = f"nl-{slug}"
                if tid in existing_ids:
                    continue
                lead = " ".join(" ".join(p.text_content().split()) for p in adoc.xpath("//p[contains(@class,'article-header-description')]"))
                body_paras = [" ".join(d.text_content().split()) for d in adoc.xpath("//div[contains(@class,'article-details-text')]") if len(d.text_content().strip()) > 20]
                if not lead or not body_paras:
                    continue
                title_line = title if title.endswith((".", "!", "?")) else f"{title}."
                sents = [title_line] + bac.split_german_sentences(lead) + bac.split_german_sentences(" ".join(body_paras))
                if len(sents) > 10:
                    merged, buf = [], ""
                    for s in sents:
                        buf = f"{buf} {s}".strip() if buf else s
                        if len(buf) >= 115:
                            merged.append(buf); buf = ""
                    if buf:
                        merged[-1] = f"{merged[-1]} {buf}" if merged else buf
                    sents = merged
                local_mp3 = os.path.join(bac.RAW_DIR, "nachrichtenleicht", f"nl_{slug}.mp3")
                bac.download_file(mp3_url, local_mp3)
                dur = bac.get_audio_duration(local_mp3)
                if dur < 15 or dur > 110:
                    continue
                sils = bac.get_silences(local_mp3, noise_db=-35, min_dur=0.25)
                t0 = max(0.0, sils[0][1] - 0.15) if sils and sils[0][0] < 0.35 else 0.0
                t1 = min(dur, sils[-1][0] + 0.15) if sils and sils[-1][1] > dur - 0.5 else dur
                segs = align_with_wider_search(local_mp3, sents, t0, t1)
                if min(s["sttRecall"] for s in segs) >= 0.78:
                    print(f"  [NL+1] {title[:45]} | min={min(s['sttRecall'] for s in segs):.2f}")
                    kept.append({
                        "id": tid,
                        "title": title,
                        "level": "A2",
                        "source": "Nachrichtenleicht",
                        "sourceCategory": "news",
                        "topic": "Gesellschaft & Politik",
                        "taskSection": "Nachrichtenleicht · 慢速德语新闻",
                        "license": "Deutschlandradio / Bildungsnutzung",
                        "audioUrl": mp3_url,
                        "originalAudioUrl": mp3_url,
                        "originalPageUrl": url,
                        "localAudioPath": local_mp3,
                        "duration": round(dur, 2),
                        "alignedSegments": segs,
                    })
                    break
            except Exception as e:
                print(f"  [NL+1 skip]: {e}")

    # Sort consistently
    with open(STAGING_FILE, "w", encoding="utf-8") as f:
        json.dump(kept, f, ensure_ascii=False, indent=2)

    print(f"\n============================================================")
    print(f"FINAL ALIGNED DATASET: {len(kept)} tracks")
    for t in kept:
        recs = [s["sttRecall"] for s in t["alignedSegments"]]
        print(f"  {t['id']:36s} | {t['level']:3s} | {t['source']:18s} | segs={len(recs)} | avg={sum(recs)/len(recs):.2f} | min={min(recs):.2f}")


if __name__ == "__main__":
    main()
