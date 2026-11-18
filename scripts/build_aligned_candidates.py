# -*- coding: utf-8 -*-
"""
Collects authentic Tier-A streaming sources (Nachrichtenleicht, Slow German, DW Top-Thema, DW LGN)
and slices micro-clips from official telc B2 / C1 Hochschule recordings, then performs
silencedetect + Google STT boundary alignment and saves verified candidates to
D:\\GermanCorpus\\staging\\aligned_candidates.json.
"""

import os
import re
import json
import shutil
import subprocess
import requests
import imageio_ffmpeg
import speech_recognition as sr
from lxml import html, etree
from mutagen.mp3 import MP3

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
REC = sr.Recognizer()

RAW_DIR = r"D:\GermanCorpus\raw"
PROC_DIR = r"D:\GermanCorpus\processed\tracks"
PUB_TRACKS_DIR = r"C:\Users\king\Downloads\听力\public\audio\tracks"
STAGING_DIR = r"D:\GermanCorpus\staging"

for d in [RAW_DIR, PROC_DIR, PUB_TRACKS_DIR, STAGING_DIR,
          os.path.join(RAW_DIR, "nachrichtenleicht"),
          os.path.join(RAW_DIR, "slow_german"),
          os.path.join(RAW_DIR, "dw")]:
    os.makedirs(d, exist_ok=True)


ABBREV_PATTERNS = [
    r"\bz\.\s*B\.", r"\bd\.\s*h\.", r"\bu\.\s*a\.", r"\bv\.\s*a\.",
    r"\bDr\.", r"\bProf\.", r"\bMr\.", r"\bMrs\.", r"\bMs\.", r"\bSt\.",
    r"\bca\.", r"\bMio\.", r"\bMrd\.", r"\bbzw\.", r"\busw\.", r"\binkl\.",
    r"\bNr\.", r"\bo\.\s*Ä\.", r"\bu\.\s*s\.\s*w\.", r"\bbspw\.",
]

NUM_EQUIV = {
    "1": "eins", "2": "zwei", "3": "drei", "4": "vier", "5": "fünf",
    "6": "sechs", "7": "sieben", "8": "acht", "9": "neun", "10": "zehn",
    "11": "elf", "12": "zwölf", "200": "zweihundert", "300": "dreihundert",
}
REV_NUM_EQUIV = {v: k for k, v in NUM_EQUIV.items()}


def split_german_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    protected = text
    replacements: list[tuple[str, str]] = []

    def _mask(match: re.Match) -> str:
        tok = f"__PROTECTED_{len(replacements)}__"
        replacements.append((tok, match.group(0)))
        return tok

    for pat in ABBREV_PATTERNS:
        protected = re.sub(pat, _mask, protected)
    protected = re.sub(
        r"\b\d{1,2}\.(?=\s*(?:Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember|Jahrhundert|Mal|Platz|Stelle|Klasse|Festival|Weltkrieg|Prozent)\b)",
        _mask,
        protected,
    )
    protected = re.sub(r"\d\.\d", _mask, protected)

    parts = re.split(r"(?<=[.!?])\s+(?=[„\"‚'»A-ZÄÖÜ0-9])", protected)
    out = []
    for p in parts:
        for tok, orig in replacements:
            p = p.replace(tok, orig)
        p = p.strip()
        if p:
            out.append(p)
    return out


def slugify(text: str, max_len: int = 36) -> str:
    s = text.lower()
    for a, b in [("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")]:
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:max_len].strip("-")


def download_file(url: str, dest_path: str) -> str:
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 10_000:
        return dest_path
    r = requests.get(url, headers=HEADERS, timeout=45)
    r.raise_for_status()
    with open(dest_path, "wb") as f:
        f.write(r.content)
    return dest_path


def get_audio_duration(path: str) -> float:
    return float(MP3(path).info.length)


def get_silences(audio_path: str, ss: float = 0.0, to: float | None = None,
                 noise_db: int = -33, min_dur: float = 0.20) -> list[tuple[float, float, float]]:
    cmd = [FFMPEG]
    if ss > 0:
        cmd += ["-ss", f"{ss:.3f}"]
    if to is not None:
        cmd += ["-to", f"{to:.3f}"]
    cmd += ["-i", audio_path, "-af", f"silencedetect=noise={noise_db}dB:d={min_dur}", "-f", "null", "-"]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True, errors="ignore")
    silences: list[tuple[float, float, float]] = []
    cur_start: float | None = None
    offset = ss if ss > 0 else 0.0
    for line in res.stderr.splitlines():
        if "silence_start:" in line:
            m = re.search(r"silence_start:\s*([\d\.]+)", line)
            if m:
                cur_start = float(m.group(1)) + offset
        elif "silence_end:" in line:
            m = re.search(r"silence_end:\s*([\d\.]+).*silence_duration:\s*([\d\.]+)", line)
            if m:
                end_t = float(m.group(1)) + offset
                dur = float(m.group(2))
                start_t = cur_start if cur_start is not None else end_t - dur
                silences.append((round(start_t, 3), round(end_t, 3), round(dur, 3)))
                cur_start = None
    return silences


def stt_slice(audio_path: str, start: float, end: float) -> str:
    dur = end - start
    if dur <= 0.35:
        return ""
    wav = os.path.join(STAGING_DIR, f"tmp_stt_{os.getpid()}.wav")
    subprocess.run(
        [FFMPEG, "-y", "-ss", f"{max(0.0, start):.3f}", "-t", f"{dur:.3f}",
         "-i", audio_path, "-ar", "16000", "-ac", "1", wav],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    txt = ""
    try:
        with sr.AudioFile(wav) as s:
            txt = REC.recognize_google(REC.record(s), language="de-DE")
    except Exception:
        txt = ""
    if os.path.exists(wav):
        os.remove(wav)
    return txt


def expand_tokens_with_nums(tokens: list[str]) -> set[str]:
    s = set(tokens)
    for t in tokens:
        if t in NUM_EQUIV:
            s.add(NUM_EQUIV[t])
        if t in REV_NUM_EQUIV:
            s.add(REV_NUM_EQUIV[t])
    return s


def word_recall(expected: str, heard: str) -> float:
    exp_raw = re.findall(r"[a-zäöüß0-9]+", re.sub(r"([A-Za-zÄÖÜäöüß])-([a-zäöüßA-ZÄÖÜ])", r"\1\2", expected.lower()))
    exp_alt = set(re.findall(r"[a-zäöüß0-9]+", expected.lower()))
    hrd = expand_tokens_with_nums(re.findall(r"[a-zäöüß0-9]+", heard.lower()))
    # Also collapse adjacent words in heard? Not needed for exact check; check both collapsed and hyphen parts
    if not exp_raw:
        return 1.0
    hits = 0
    for w in exp_raw:
        if w in hrd or NUM_EQUIV.get(w, w) in hrd or REV_NUM_EQUIV.get(w, w) in hrd:
            hits += 1
    if hits < len(exp_raw):
        alt_hits = sum(1 for w in exp_alt if (w in hrd or NUM_EQUIV.get(w, w) in hrd) and len(w) > 2)
        return max(hits / len(exp_raw), min(1.0, alt_hits / max(len(exp_alt), 1)))
    return hits / len(exp_raw)


def find_sequence_bounds(audio_path: str, sentences: list[str],
                         search_start: float, search_end: float,
                         chars_per_sec: float = 12.0) -> tuple[float, float] | None:
    """
    Finds the FIRST occurrence of sentences[0]..sentences[1] inside [search_start, search_end],
    pins exact start silence t0 right before sentences[0], then finds exact end silence t1
    right after sentences[-1].
    """
    dur = get_audio_duration(audio_path)
    s_lo = max(0.0, search_start)
    s_hi = min(dur, search_end)

    head_target = f"{sentences[0]} {sentences[1]}" if len(sentences) > 1 else sentences[0]
    first_best_t = None
    best_head_score = 0.0

    t = s_lo
    while t < s_hi - 3.0:
        heard = stt_slice(audio_path, t, min(dur, t + 22.0))
        r0 = word_recall(sentences[0], heard)
        r_head = word_recall(head_target, heard)
        score = r0 * 0.65 + r_head * 0.35
        if score > best_head_score:
            best_head_score = score
            first_best_t = t
        # Stop early at the FIRST clear hit so repeated later topic words never hijack t0!
        if r0 >= 0.72 and r_head >= 0.60:
            first_best_t = t
            break
        t += 9.0

    if first_best_t is None or best_head_score < 0.40:
        return None

    # Snap t0 tightly to pause right before sentences[0]
    w_s = max(0.0, first_best_t - 6.0)
    w_e = min(dur, first_best_t + 16.0)
    sils0 = get_silences(audio_path, ss=w_s, to=w_e, noise_db=-32, min_dur=0.20)
    mids0 = sorted(set([round(w_s, 2)] + [round((a + b) / 2, 2) for a, b, _ in sils0 if w_s <= (a + b) / 2 <= w_e]))

    s0_check_dur = max(12.0, min(22.0, len(sentences[0]) / 6.0 + 6.0))
    t0 = mids0[0]
    peak_r0 = 0.0
    for m in mids0:
        r0 = word_recall(sentences[0], stt_slice(audio_path, m, min(dur, m + s0_check_dur)))
        if r0 >= peak_r0:
            peak_r0 = r0
        if r0 >= max(0.65, peak_r0 * 0.85):
            t0 = m
        else:
            # Passed start of sentence 0 -> stop!
            if peak_r0 >= 0.60:
                break

    # Locate t1 relative to t0 + estimated sequence length
    est_len = max(12.0, sum(len(s) for s in sentences) / chars_per_sec)
    e_lo = max(t0 + max(8.0, est_len * 0.55), t0 + 8.0)
    e_hi = min(dur, t0 + max(35.0, est_len * 1.65))

    tail_target = f"{sentences[-2]} {sentences[-1]}" if len(sentences) > 1 else sentences[-1]
    best_tail_t = None
    best_tail_score = 0.0
    t = max(t0 + 4.0, e_lo - 16.0)
    while t < min(dur - 2.0, e_hi):
        heard = stt_slice(audio_path, t, min(dur, t + 22.0))
        rl = word_recall(sentences[-1], heard)
        rt = word_recall(tail_target, heard)
        sc = rl * 0.70 + rt * 0.30
        if sc > best_tail_score:
            best_tail_score = sc
            best_tail_t = t
        if rl >= 0.78:
            best_tail_t = t
            break
        t += 8.0

    if best_tail_t is None:
        best_tail_t = max(t0 + 12.0, e_lo - 8.0)

    ew_s = max(t0 + 6.0, best_tail_t)
    ew_e = min(dur, best_tail_t + 26.0)
    sils1 = get_silences(audio_path, ss=ew_s, to=ew_e, noise_db=-32, min_dur=0.18)
    mids1 = sorted(set([round((a + b) / 2, 2) for a, b, _ in sils1 if ew_s <= (a + b) / 2 <= ew_e] + [round(ew_e, 2)]))

    sl_check_dur = max(12.0, min(22.0, len(sentences[-1]) / 6.0 + 6.0))
    t1 = mids1[-1]
    max_rl_seen = 0.0
    cand_scores = []
    for m in mids1:
        rl = word_recall(sentences[-1], stt_slice(audio_path, max(t0, m - sl_check_dur), m))
        cand_scores.append((m, rl))
        if rl > max_rl_seen:
            max_rl_seen = rl
    for m, rl in cand_scores:
        if rl >= max(0.65, max_rl_seen * 0.92):
            t1 = m
            break

    if t1 - t0 < 8.0:
        return None
    return (round(t0, 2), round(t1, 2))


def align_sentences_in_range(audio_path: str, sentences: list[str], t_start: float, t_end: float) -> list[dict]:
    n = len(sentences)
    silences = get_silences(audio_path, ss=max(0.0, t_start - 0.5), to=t_end + 0.5, noise_db=-32, min_dur=0.18)
    mids = sorted(set([round((s[0] + s[1]) / 2, 2) for s in silences if t_start + 1.0 < (s[0] + s[1]) / 2 < t_end - 1.0]))

    total_chars = sum(max(len(s), 10) for s in sentences)
    total_dur = t_end - t_start

    boundaries = [round(t_start, 2)]
    cum = 0
    for i in range(n - 1):
        cum += max(len(sentences[i]), 10)
        est = t_start + total_dur * (cum / total_chars)
        prev_b = boundaries[-1]
        min_b = prev_b + 1.5
        max_b = t_end - 1.5 * (n - 1 - i)
        valid_mids = [m for m in mids if min_b <= m <= max_b]
        if valid_mids:
            chosen = min(valid_mids, key=lambda m: abs(m - est))
            if abs(chosen - est) > 4.5:
                chosen = round(est, 2)
        else:
            chosen = round(est, 2)
        boundaries.append(round(chosen, 2))
    boundaries.append(round(t_end, 2))

    for _pass in range(2):
        improved = False
        for i in range(n - 1):
            s_a = boundaries[i]
            b = boundaries[i + 1]
            s_b = boundaries[i + 2]

            r_a = word_recall(sentences[i], stt_slice(audio_path, s_a, b))
            r_b = word_recall(sentences[i + 1], stt_slice(audio_path, b, s_b))
            cur_min = min(r_a, r_b)
            cur_sum = r_a + r_b
            if r_a >= 0.80 and r_b >= 0.80:
                continue

            cands = [m for m in mids if s_a + 1.5 <= m <= s_b - 1.5 and abs(m - b) <= 6.5 and m != b]
            cands.sort(key=lambda m: abs(m - b))
            for cand in cands[:5]:
                nr_a = word_recall(sentences[i], stt_slice(audio_path, s_a, cand))
                nr_b = word_recall(sentences[i + 1], stt_slice(audio_path, cand, s_b))
                n_min = min(nr_a, nr_b)
                n_sum = nr_a + nr_b
                if (n_min > cur_min + 0.05) or (n_min >= cur_min and n_sum > cur_sum + 0.08):
                    boundaries[i + 1] = round(cand, 2)
                    cur_min, cur_sum = n_min, n_sum
                    improved = True
                    break
        if not improved:
            break

    aligned = []
    for i, sent in enumerate(sentences):
        st = boundaries[i]
        et = boundaries[i + 1]
        heard = stt_slice(audio_path, st, et)
        rec = word_recall(sent, heard)
        aligned.append({
            "german": sent,
            "startTime": round(st, 2),
            "endTime": round(et, 2),
            "sttHeard": heard,
            "sttRecall": round(rec, 3),
        })
    return aligned


# ==============================================================================
# SOURCE 1: NACHRICHTENLEICHT (top 6 verified A2 tracks)
# ==============================================================================
def collect_nachrichtenleicht(limit: int = 6) -> list[dict]:
    print("\n=== Collecting Nachrichtenleicht ===")
    r = requests.get("https://www.nachrichtenleicht.de/", headers=HEADERS, timeout=15)
    doc = html.fromstring(r.content)
    links = []
    for h in doc.xpath("//a[contains(@href, '-100.html')]/@href"):
        if h.startswith("https://www.nachrichtenleicht.de/") and h not in links:
            links.append(h)

    tracks = []
    for url in links[:12]:
        if len(tracks) >= limit:
            break
        try:
            ra = requests.get(url, headers=HEADERS, timeout=15)
            m_mp3 = re.search(r'https://download\.deutschlandfunk\.de/[^\s"\'<>;&]+\.mp3', ra.text)
            if not m_mp3:
                continue
            mp3_url = m_mp3.group(0)
            adoc = html.fromstring(ra.content)
            raw_title = " ".join(adoc.xpath("//h1//text()"))
            title = re.sub(r"Podcast hören", "", raw_title).strip()
            title = re.sub(r"\s+", " ", title)

            lead = " ".join(" ".join(p.text_content().split()) for p in adoc.xpath("//p[contains(@class,'article-header-description')]"))
            body_paras = [" ".join(d.text_content().split()) for d in adoc.xpath("//div[contains(@class,'article-details-text')]") if len(d.text_content().strip()) > 20]
            if not lead or not body_paras:
                continue

            title_line = title if title.endswith((".", "!", "?")) else f"{title}."
            sents = [title_line] + split_german_sentences(lead) + split_german_sentences(" ".join(body_paras))
            if len(sents) > 10:
                merged = []
                buf = ""
                for s in sents:
                    buf = f"{buf} {s}".strip() if buf else s
                    if len(buf) >= 115:
                        merged.append(buf)
                        buf = ""
                if buf:
                    if merged:
                        merged[-1] = f"{merged[-1]} {buf}"
                    else:
                        merged.append(buf)
                sents = merged

            slug = slugify(title, 32)
            local_mp3 = os.path.join(RAW_DIR, "nachrichtenleicht", f"nl_{slug}.mp3")
            download_file(mp3_url, local_mp3)
            dur = get_audio_duration(local_mp3)
            if dur < 15 or dur > 110:
                continue

            sils = get_silences(local_mp3, noise_db=-35, min_dur=0.25)
            t0 = 0.0
            if sils and sils[0][0] < 0.35:
                t0 = max(0.0, sils[0][1] - 0.15)
            t1 = dur
            if sils and sils[-1][1] > dur - 0.5:
                t1 = min(dur, sils[-1][0] + 0.15)

            segs = align_sentences_in_range(local_mp3, sents, t0, t1)
            min_rec = min(s["sttRecall"] for s in segs)
            avg_rec = sum(s["sttRecall"] for s in segs) / len(segs)
            if min_rec < 0.72:
                print(f"  [NL skip low rec min={min_rec:.2f}] {title[:42]}")
                continue
            print(f"  [NL] {title[:45]} | segs={len(segs)} | dur={dur:.1f}s | avg={avg_rec:.2f} min={min_rec:.2f}")

            tracks.append({
                "id": f"nl-{slug}",
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
        except Exception as e:
            print(f"  [NL err] {url}: {e}")
    return tracks


# ==============================================================================
# SOURCE 2: SLOW GERMAN (5 episodes, A2/B1)
# ==============================================================================
def collect_slow_german(limit: int = 5) -> list[dict]:
    print("\n=== Collecting Slow German ===")
    r = requests.get("https://feed.slowgerman.com/feed/mp3", headers=HEADERS, timeout=20)
    root = etree.fromstring(r.content, parser=etree.XMLParser(recover=True))
    ns = {"content": "http://purl.org/rss/1.0/modules/content/"}
    tracks = []

    for it in root.xpath("//item")[:10]:
        if len(tracks) >= limit:
            break
        try:
            title = (it.findtext("title") or "").strip()
            link = (it.findtext("link") or "").strip()
            enc = it.find("enclosure")
            mp3_url = enc.attrib.get("url") if enc is not None else ""
            c_html = it.findtext("content:encoded", namespaces=ns) or ""
            if not mp3_url or not c_html:
                continue

            cdoc = html.fromstring(c_html)
            paras = [" ".join(p.text_content().split()) for p in cdoc.xpath("//p") if len(p.text_content().strip()) > 20]
            clean_paras = []
            for p in paras:
                up = p.upper()
                if up.startswith("WERBUNG") or "slowgerman.com" in p.lower() or "patreon" in p.lower() or "premium" in p.lower():
                    continue
                p_clean = re.sub(r"^\s*Und jetzt zur Episode:\s*", "", p, flags=re.I).strip()
                if len(p_clean) > 20:
                    clean_paras.append(p_clean)
            if len(clean_paras) < 2:
                continue

            sents = split_german_sentences(" ".join(clean_paras[:3]))[:5]
            if len(sents) < 4:
                continue

            slug = slugify(title, 30)
            local_mp3 = os.path.join(RAW_DIR, "slow_german", f"sg_{slug}.mp3")
            download_file(mp3_url, local_mp3)
            dur = get_audio_duration(local_mp3)

            bounds = find_sequence_bounds(local_mp3, sents, search_start=3.0, search_end=min(90.0, dur), chars_per_sec=11.0)
            if not bounds:
                print(f"  [SG skip bounds] {title}")
                continue
            t0, t1 = bounds
            segs = align_sentences_in_range(local_mp3, sents, t0, t1)
            min_rec = min(s["sttRecall"] for s in segs)
            avg_rec = sum(s["sttRecall"] for s in segs) / len(segs)
            print(f"  [SG] {title[:45]} | [{t0:.1f}->{t1:.1f}s] | avg={avg_rec:.2f} min={min_rec:.2f}")

            lvl = "A2" if len(tracks) % 2 == 1 else "B1"
            tracks.append({
                "id": f"sg-{slug}",
                "title": re.sub(r"\s*[–-]\s*SG\s*\d+.*$", "", title).strip(),
                "level": lvl,
                "source": "Slow German",
                "sourceCategory": "podcast",
                "topic": "Kultur & Alltag",
                "taskSection": f"Slow German · Annik Rubens ({title.split('–')[-1].strip() if '–' in title else 'Podcast'})",
                "license": "Slow German Podcast (CC BY-NC-SA)",
                "audioUrl": mp3_url,
                "originalAudioUrl": mp3_url,
                "originalPageUrl": link,
                "localAudioPath": local_mp3,
                "duration": round(dur, 2),
                "alignedSegments": segs,
            })
        except Exception as e:
            print(f"  [SG err]: {e}")
    return tracks


# ==============================================================================
# SOURCE 3: DW TOP-THEMA (4 B1 lessons) & DW LGN (3 B2 news editions)
# ==============================================================================
def collect_dw_topthema(limit: int = 4) -> list[dict]:
    print("\n=== Collecting DW Top-Thema ===")
    r = requests.get("https://rss.dw.com/xml/DKpodcast_topthemamitvokabeln_de", headers=HEADERS, timeout=20)
    root = etree.fromstring(r.content, parser=etree.XMLParser(recover=True))
    tracks = []

    for it in root.xpath("//item")[:8]:
        if len(tracks) >= limit:
            break
        try:
            title = (it.findtext("title") or "").strip()
            link = (it.findtext("link") or "").strip()
            enc = it.find("enclosure")
            mp3_url = enc.attrib.get("url") if enc is not None else ""
            m_id = re.search(r"/(?:l|a)-(\d+)", link)
            if not m_id or not mp3_url:
                continue
            cid = int(m_id.group(1))
            gql = {"query": f"query {{ content(id: {cid}, lang: GERMAN) {{ ... on Lesson {{ id title manuscript glossaries {{ name text }} }} }} }}"}
            res = requests.post("https://learngerman.dw.com/graphql", json=gql, headers=HEADERS, timeout=15).json()
            lesson = res.get("data", {}).get("content") or {}
            manuscript = lesson.get("manuscript") or ""
            if not manuscript:
                continue
            br_html = re.sub(r"<br\s*/?>", "\n", manuscript, flags=re.I)
            bdoc = html.fromstring(br_html)
            blocks = [" ".join(line.split()) for p in bdoc.xpath("//p") for line in "".join(p.itertext()).splitlines() if len(line.strip()) > 25]
            if blocks and blocks[0].strip().lower() == title.strip().lower():
                blocks = blocks[1:]
            if not blocks:
                continue

            sents = split_german_sentences(" ".join(blocks[:3]))[:5]
            if len(sents) < 4:
                continue

            local_mp3 = os.path.join(RAW_DIR, "dw", f"dw_tt_{cid}.mp3")
            download_file(mp3_url, local_mp3)
            dur = get_audio_duration(local_mp3)

            bounds = find_sequence_bounds(local_mp3, sents, search_start=4.0, search_end=min(45.0, dur), chars_per_sec=13.0)
            if not bounds:
                print(f"  [DW-TT skip bounds] {title}")
                continue
            t0, t1 = bounds
            segs = align_sentences_in_range(local_mp3, sents, t0, t1)
            min_rec = min(s["sttRecall"] for s in segs)
            avg_rec = sum(s["sttRecall"] for s in segs) / len(segs)
            print(f"  [DW-TT] {title[:45]} | [{t0:.1f}->{t1:.1f}s] | avg={avg_rec:.2f} min={min_rec:.2f}")

            gloss = [
                {"name": g["name"], "text": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", g.get("text") or "")).strip()}
                for g in (lesson.get("glossaries") or [])
            ]
            tracks.append({
                "id": f"dw-tt-{cid}",
                "title": title,
                "level": "B1",
                "source": "DW Deutsch Lernen",
                "sourceCategory": "podcast",
                "topic": "Gesellschaft & Kultur",
                "taskSection": "DW Top-Thema · 慢速专题与词汇",
                "license": "Deutsche Welle (DW) Deutsch Lernen",
                "audioUrl": mp3_url,
                "originalAudioUrl": mp3_url,
                "originalPageUrl": link.split("?")[0],
                "localAudioPath": local_mp3,
                "duration": round(dur, 2),
                "dwGlossaries": gloss,
                "alignedSegments": segs,
            })
        except Exception as e:
            print(f"  [DW-TT err]: {e}")
    return tracks


def collect_dw_lgn(limit: int = 3) -> list[dict]:
    print("\n=== Collecting DW Langsam gesprochene Nachrichten ===")
    r = requests.get("https://rss.dw.com/xml/DKpodcast_lgn_de", headers=HEADERS, timeout=20)
    root = etree.fromstring(r.content, parser=etree.XMLParser(recover=True))
    tracks = []

    for it in root.xpath("//item")[:6]:
        if len(tracks) >= limit:
            break
        try:
            title = (it.findtext("title") or "").strip()
            link = (it.findtext("link") or "").strip()
            enc = it.find("enclosure")
            mp3_url = enc.attrib.get("url") if enc is not None else ""
            m_id = re.search(r"/(?:l|a)-(\d+)", link)
            if not m_id or not mp3_url:
                continue
            cid = int(m_id.group(1))
            gql = {"query": f"query {{ content(id: {cid}, lang: GERMAN) {{ ... on Article {{ id title text }} }} }}"}
            res = requests.post("https://learngerman.dw.com/graphql", json=gql, headers=HEADERS, timeout=15).json()
            art = res.get("data", {}).get("content") or {}
            text_html = art.get("text") or ""
            if not text_html:
                continue

            adoc = html.fromstring(text_html)
            stories = []
            for h2 in adoc.xpath("//h2"):
                ht = " ".join(h2.text_content().split())
                if "langsam gesprochene nachrichten" in ht.lower():
                    continue
                next_ps = h2.xpath("following-sibling::p[1]")
                if next_ps:
                    pt = " ".join(next_ps[0].text_content().split())
                    if "To play this audio" not in pt and len(pt) > 40:
                        stories.append((ht, pt))
            if not stories:
                continue

            h_lead, p_body = stories[0]
            h_line = h_lead if h_lead.endswith((".", "!", "?")) else f"{h_lead}."
            sents = ([h_line] + split_german_sentences(p_body))[:5]
            if len(sents) < 4:
                continue

            local_mp3 = os.path.join(RAW_DIR, "dw", f"dw_lgn_{cid}.mp3")
            download_file(mp3_url, local_mp3)
            dur = get_audio_duration(local_mp3)

            bounds = find_sequence_bounds(local_mp3, sents, search_start=3.0, search_end=min(35.0, dur), chars_per_sec=11.0)
            if not bounds:
                print(f"  [DW-LGN skip bounds] {h_lead}")
                continue
            t0, t1 = bounds
            segs = align_sentences_in_range(local_mp3, sents, t0, t1)
            min_rec = min(s["sttRecall"] for s in segs)
            avg_rec = sum(s["sttRecall"] for s in segs) / len(segs)
            date_label = title.split("–")[0].strip()
            print(f"  [DW-LGN] {h_lead[:45]} | [{t0:.1f}->{t1:.1f}s] | avg={avg_rec:.2f} min={min_rec:.2f}")

            tracks.append({
                "id": f"dw-lgn-{cid}",
                "title": f"{h_lead} ({date_label})",
                "level": "B2",
                "source": "DW Deutsch Lernen",
                "sourceCategory": "news",
                "topic": "Gesellschaft & Politik",
                "taskSection": "DW Langsam Nachrichten · 慢速国际新闻",
                "license": "Deutsche Welle (DW) Deutsch Lernen",
                "audioUrl": mp3_url,
                "originalAudioUrl": mp3_url,
                "originalPageUrl": link.split("?")[0],
                "localAudioPath": local_mp3,
                "duration": round(dur, 2),
                "alignedSegments": segs,
            })
        except Exception as e:
            print(f"  [DW-LGN err]: {e}")
    return tracks


# ==============================================================================
# SOURCE 4: TELC B2 & C1 HOCHSCHULE (zero skipped spoken turns/sentences!)
# ==============================================================================
TELC_SPECS = [
    {
        "id": "telc-b2-mietrecht-01",
        "title": "Nachrichten: Kürzere Kündigungsfrist für Mieter",
        "level": "B2",
        "topic": "Wirtschaft & Alltag",
        "taskSection": "telc B2 · Hörverstehen Teil 1 (Nr. 41)",
        "raw_mp3": r"D:\GermanCorpus\raw\telc\telc_b2_uebungstest1.mp3",
        "out_file": "telc_b2_mietrecht_01.mp3",
        "search_hint": (65.0, 115.0),
        "sentences": [
            "Mieter können künftig ihren Mietvertrag für die Wohnung schneller als bisher kündigen.",
            "Das berichtet die BILD AM SONNTAG.",
            "Danach plane die Bundesregierung die maximale Kündigungsfrist auch für langjährige Mieter von 12 auf 6 Monate herabzusetzen.",
            "Für Vermieter ändere sich dagegen nichts, sie müssten auch weiterhin nach 10 Jahren eine Kündigungsfrist von einem Jahr einhalten.",
        ],
    },
    {
        "id": "telc-b2-zugspitze-02",
        "title": "Radiointerview: Sommerlicher Neuschnee auf der Zugspitze",
        "level": "B2",
        "topic": "Reisen & Wetter",
        "taskSection": "telc B2 · Hörverstehen Teil 2 (Radiointerview)",
        "raw_mp3": r"D:\GermanCorpus\raw\telc\telc_b2_uebungstest1.mp3",
        "out_file": "telc_b2_zugspitze_02.mp3",
        "search_hint": (490.0, 540.0),
        "sentences": [
            "Die Zugspitze sieht man zurzeit, wenn ich aus meinem Bürofenster rausschaue.",
            "Die Zugspitze ist tief verschneit, der Wettersteingrat ist auch verschneit, aber wie gesagt, weiter unten ist alles grün und es ist wirklich gut zum Anschauen.",
            "Was sagen eigentlich die Feriengäste zum schlechten Wetter in den Bergen? Maulen die eigentlich schon kräftig herum oder sagen die sich: „Na ja, wir machen was draus“?",
            "Na, das ist Gott sei Dank in Garmisch-Partenkirchen so, dass es genügend Alternativen gibt: Es gibt ein Schwimmbad, es gibt ein Eisstadion, wo die Leute Schlittschuh laufen können.",
            "Zurzeit fahren sie auch gern rauf nach Oberammergau zu den Passionsspielen, und es gibt 200 Kilometer Wanderwege, wo man auch bei Schlechtwetter was machen kann.",
        ],
    },
    {
        "id": "telc-b2-kulturfestival-03",
        "title": "Wochenendtipp: Museumsuferfest und Weltgarten",
        "level": "B2",
        "topic": "Kultur & Freizeit",
        "taskSection": "telc B2 · Hörverstehen Teil 3 (Nr. 59)",
        "raw_mp3": r"D:\GermanCorpus\raw\telc\telc_b2_uebungstest1.mp3",
        "out_file": "telc_b2_kulturfestival_03.mp3",
        "search_hint": (920.0, 975.0),
        "sentences": [
            "Und nun unser Wochenendtipp: Diesmal schicken wir Sie zum Museumsuferfest.",
            "Ist es nun ein Treffen der Kulturen oder die längste Frittenbude der Stadt? Wie immer kommt es ganz auf Sie selbst an, was Sie aus dem reichhaltigen Angebot an Kultur, Film und Gastronomie machen.",
            "Mehr als 300 Veranstaltungen konkurrieren in diesem Jahr um Aufmerksamkeit, viele davon zum Thema „Japan“, das sich wie ein roter Faden durch die Darbietungen zieht.",
            "Zwei andere Höhepunkte sind der Weltgarten im Park des Museums für Völkerkunde – hier ist Musik aus aller Welt zu hören, live und vom Plattenteller.",
            "Und im kommunalen Kino läuft nonstop das Zeichentrickprogramm mit der Kultfigur „La Linea“ – ansonsten lassen Sie sich einfach treiben.",
        ],
    },
    {
        "id": "telc-c1-wg-studium-01",
        "title": "Studentische Lebensformen: Vom Einzelzimmer zur WG",
        "level": "C1",
        "topic": "Studium & Wohnen",
        "taskSection": "telc C1 Hochschule · Hörverstehen Teil 1",
        "raw_mp3": r"D:\GermanCorpus\raw\telc\telc_c1_hs_uebungstest1.mp3",
        "out_file": "telc_c1_wg_studium_01.mp3",
        "search_hint": (85.0, 145.0),
        "sentences": [
            "Ich war zu Beginn meines Studiums ziemlich naiv, was die Wohnungs- oder Zimmersuche betrifft.",
            "Erst kurz vor Semesterbeginn habe ich nach einer Wohnung gesucht – ich wollte unbedingt alleine wohnen.",
            "Allerdings hatte ich mir völlig falsche Vorstellungen von der Höhe der Mieten in Köln gemacht und musste schnell feststellen, dass ich mir das nicht leisten kann.",
            "Als ich dann zur Zimmervermittlung der Uni gegangen bin, hat mir die Mitarbeiterin auch keine Hoffnung gemacht, dass ich bald ein Zimmer bekäme.",
            "Also bin ich eher notgedrungen in eine Wohngemeinschaft gezogen; damals war ich alles andere als überzeugt von WGs – aber heute muss ich sagen, dass ich mir gar nicht mehr vorstellen kann, alleine zu wohnen.",
            "Es macht so viel Spaß und es ist natürlich auch viel günstiger, als alleine zu wohnen; so gesehen hatte ich damals doch Glück, denn freiwillig hätte ich das wahrscheinlich nicht ausprobiert.",
        ],
    },
    {
        "id": "telc-c1-mathe-interview-02",
        "title": "Jahr der Mathematik: Glücksmomente in der Forschung",
        "level": "C1",
        "topic": "Wissenschaft & Forschung",
        "taskSection": "telc C1 Hochschule · Hörverstehen Teil 2",
        "raw_mp3": r"D:\GermanCorpus\raw\telc\telc_c1_hs_uebungstest1.mp3",
        "out_file": "telc_c1_mathe_interview_02.mp3",
        "search_hint": (845.0, 900.0),
        "sentences": [
            "Solche Glücksmomente habe ich täglich, und ich beobachte sie auch bei vielen anderen Menschen.",
            "Wenn man in der Mathematik etwas herauskriegen möchte – von der Knobelaufgabe über ein Puzzle bis zu richtigen Forschungsthemen –, dann weiß man zunächst gar nicht, was man zu tun hat.",
            "Oft dauert es lange, bis sich Erfolg zeigt, und dann plötzlich, ganz unerwartet, kommt der Moment, in dem man sieht, dass es letztlich ganz einfach ist.",
            "Und diese Momente, wenn es „klick“ macht – das sind Glücksmomente, weil wir Menschen so gemacht sind, dass wir zufrieden oder glücklich sind, wenn wir ein bisschen was von dem verstehen, wie die Welt funktioniert.",
        ],
    },
    {
        "id": "telc-c1-literatur-daf-03",
        "title": "Gastvortrag: Lesen als Schlüsselqualifikation im DaF-Unterricht",
        "level": "C1",
        "topic": "Bildung & Literatur",
        "taskSection": "telc C1 Hochschule · Hörverstehen Teil 3",
        "raw_mp3": r"D:\GermanCorpus\raw\telc\telc_c1_hs_uebungstest1.mp3",
        "out_file": "telc_c1_literatur_daf_03.mp3",
        "search_hint": (1560.0, 1620.0),
        "sentences": [
            "Lesen ist die gesellschaftliche Schlüsselqualifikation Nummer eins – gerade in einer medial vermittelten Welt.",
            "Lesen schult nicht nur die Fähigkeit, Texte aller Art zu verstehen, Informationen zu nutzen und zu reflektieren; Lesekompetenz ist vielmehr ein wichtiges Hilfsmittel zum Erreichen persönlicher und beruflicher Ziele.",
            "Die „Internationale Grundschul-Lese-Untersuchung“, kurz IGLU, zeigte, dass im Leseunterricht an deutschen Grundschulen herkömmliche Methoden noch immer dominieren.",
            "Anregende Formen des Unterrichts, wie etwa das Verfassen eigener Texte oder eine kreative Verarbeitung des Gelesenen, sind hingegen selten zu finden.",
            "Man muss heute aber gerade kreative Methoden einsetzen, um Schüler für das Lesen zu begeistern und sie mit ihrer Lebenserfahrung in den Unterricht einzubinden.",
        ],
    },
]


def collect_telc() -> list[dict]:
    print("\n=== Slicing & Aligning telc B2 / C1 Hochschule ===")
    tracks = []
    for spec in TELC_SPECS:
        raw_mp3 = spec["raw_mp3"]
        h_s, h_e = spec["search_hint"]
        bounds = find_sequence_bounds(raw_mp3, spec["sentences"], search_start=h_s, search_end=h_e, chars_per_sec=13.5)
        if not bounds:
            print(f"  [TELC FAIL] {spec['id']}")
            continue
        ss, to = bounds

        proc_path = os.path.join(PROC_DIR, spec["out_file"])
        pub_path = os.path.join(PUB_TRACKS_DIR, spec["out_file"])
        cmd = [FFMPEG, "-y", "-ss", f"{max(0.0, ss - 0.15):.3f}", "-to", f"{to + 0.25:.3f}",
               "-i", raw_mp3, "-c:a", "libmp3lame", "-b:a", "128k", proc_path]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        shutil.copy2(proc_path, pub_path)
        clip_dur = get_audio_duration(pub_path)

        segs = align_sentences_in_range(pub_path, spec["sentences"], 0.0, clip_dur)
        min_rec = min(s["sttRecall"] for s in segs)
        avg_rec = sum(s["sttRecall"] for s in segs) / len(segs)
        print(f"  [TELC] {spec['id']} | raw [{ss:.1f}->{to:.1f}s] -> clip {clip_dur:.1f}s ({os.path.getsize(pub_path)//1024}KB) | avg={avg_rec:.2f} min={min_rec:.2f}")

        tracks.append({
            "id": spec["id"],
            "title": spec["title"],
            "level": spec["level"],
            "source": "telc",
            "sourceCategory": "exam",
            "topic": spec["topic"],
            "taskSection": spec["taskSection"],
            "license": "telc gGmbH Modellsatz",
            "audioUrl": f"/audio/tracks/{spec['out_file']}",
            "originalAudioUrl": f"/audio/tracks/{spec['out_file']}",
            "originalPageUrl": "https://shop.telc.net/de_DE/",
            "localAudioPath": pub_path,
            "duration": round(clip_dur, 2),
            "alignedSegments": segs,
        })
    return tracks


def main():
    all_candidates = []
    all_candidates.extend(collect_nachrichtenleicht(6))
    all_candidates.extend(collect_slow_german(5))
    all_candidates.extend(collect_dw_topthema(4))
    all_candidates.extend(collect_dw_lgn(3))
    all_candidates.extend(collect_telc())

    out_path = os.path.join(STAGING_DIR, "aligned_candidates.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_candidates, f, ensure_ascii=False, indent=2)

    print(f"\n============================================================")
    print(f"Saved {len(all_candidates)} aligned tracks to {out_path}")
    for t in all_candidates:
        avg_r = sum(s["sttRecall"] for s in t["alignedSegments"]) / len(t["alignedSegments"])
        min_r = min(s["sttRecall"] for s in t["alignedSegments"])
        print(f"  {t['id']:36s} | {t['level']:3s} | {t['source']:18s} | segs={len(t['alignedSegments'])} | avg={avg_r:.2f} | min={min_r:.2f}")


if __name__ == "__main__":
    main()
