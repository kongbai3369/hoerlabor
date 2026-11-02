import asyncio
import hashlib
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request
import edge_tts

PROJECT_DIR = Path(r"c:\Users\king\Downloads\听力")
OUT_DIR = PROJECT_DIR / "public" / "audio" / "words"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Collect all words from generatedTracks and seedTracks
all_sentences = []
seed_path = PROJECT_DIR / "src" / "data" / "seedTracks.ts"
seed_text = seed_path.read_text(encoding="utf-8")
for m in re.finditer(r"german:\s*'([^']+)'", seed_text):
    all_sentences.append(m.group(1))

gen_path = PROJECT_DIR / "src" / "data" / "generatedTracks.json"
gen_tracks = json.loads(gen_path.read_text(encoding="utf-8"))
for t in gen_tracks:
    for s in t.get("segments", []):
        if s.get("german"):
            all_sentences.append(s["german"])
        for v in s.get("vocab", []):
            if v.get("word"):
                all_sentences.append(v["word"])

words = set()
for sent in all_sentences:
    clean_sent = re.sub(r"^(der|die|das|sich|den|dem|des|ein|eine)\s+", "", sent, flags=re.I)
    clean_sent = re.sub(r"\s*\(\+.*\)", "", clean_sent)
    tokens = re.split(r"[^A-Za-zÄÖÜäöüß]+", clean_sent)
    for tok in tokens:
        if tok and re.match(r"^[A-Za-zÄÖÜäöüß]+$", tok):
            words.add(tok)

print(f"Total unique raw tokens collected: {len(words)}", flush=True)

canonical_map = {}
for w in sorted(words):
    lower = w.lower()
    if lower not in canonical_map:
        canonical_map[lower] = w
    else:
        existing = canonical_map[lower]
        if w[0].isupper() and not existing[0].isupper():
            canonical_map[lower] = w

print(f"Total unique lowercase words: {len(canonical_map)}", flush=True)

def to_ascii_slug(word: str) -> str:
    s = word.lower()
    s = s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    s = re.sub(r"[^a-z0-9]", "_", s)
    return s

def get_wikimedia_mp3_url(filename: str) -> str:
    title_for_hash = filename.replace(" ", "_")
    h = hashlib.md5(title_for_hash.encode("utf-8")).hexdigest()
    h1 = h[0]
    h2 = h[:2]
    return f"https://upload.wikimedia.org/wikipedia/commons/transcoded/{h1}/{h2}/{urllib.parse.quote(title_for_hash)}/{urllib.parse.quote(title_for_hash)}.mp3"

def try_download_wikimedia(url: str, timeout: float = 3.5) -> bytes | None:
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 HoerLabor/2.0"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                data = resp.read()
                if len(data) > 1000:
                    return data
    except Exception:
        pass
    return None

async def generate_edge_tts(text: str) -> bytes:
    voices = ["de-DE-KatjaNeural", "de-DE-KillianNeural", "de-DE-ConradNeural"]
    for attempt in range(3):
        voice = voices[attempt % len(voices)]
        try:
            communicate = edge_tts.Communicate(text, voice)
            audio_chunks = []
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_chunks.append(chunk["data"])
            data = b"".join(audio_chunks)
            if len(data) > 500:
                return data
        except Exception:
            await asyncio.sleep(0.3 * (attempt + 1))
    raise RuntimeError(f"Edge TTS completely failed for: {text}")

async def fetch_word_audio(cased_word: str) -> tuple[str, bytes]:
    cap = cased_word[0].upper() + cased_word[1:]
    low = cased_word.lower()
    variants = [cased_word, cap, low]
    cands = []
    for v in variants:
        if v not in cands:
            cands.append(v)

    # 1. Try Wikimedia Commons .ogg & .oga & .ogg2 & De-at in parallel
    patterns = []
    for w in cands:
        patterns.append(f"De-{w}.ogg")
        patterns.append(f"De-{w}2.ogg")
        patterns.append(f"De-{w}.oga")
        patterns.append(f"De-at-{w}.ogg")

    async def check_wikimedia(fn: str):
        url = get_wikimedia_mp3_url(fn)
        return await asyncio.to_thread(try_download_wikimedia, url, 2.8)

    results = await asyncio.gather(*[check_wikimedia(fn) for fn in patterns])
    for r in results:
        if r:
            return ("wikimedia", r)

    # 2. Natural native Microsoft Edge Neural German voice
    # Guaranteed natural human-like voice, zero robot artifacts
    data = await generate_edge_tts(cased_word)
    return ("edge-neural", data)

async def main():
    slug_to_cased = {}
    for lower, cased in canonical_map.items():
        slug = to_ascii_slug(lower)
        if slug not in slug_to_cased:
            slug_to_cased[slug] = cased
        elif cased[0].isupper() and not slug_to_cased[slug][0].isupper():
            slug_to_cased[slug] = cased

    slug_items = sorted(slug_to_cased.items())
    manifest = {}
    for lower in canonical_map.keys():
        manifest[lower] = f"/audio/words/{to_ascii_slug(lower)}.mp3"

    print(f"Total unique slugs to process: {len(slug_items)}", flush=True)

    wiki_count = 0
    edge_count = 0
    skipped_count = 0
    lock = asyncio.Lock()
    sem = asyncio.Semaphore(4)

    async def process_item(idx: int, slug: str, cased: str):
        nonlocal wiki_count, edge_count, skipped_count
        file_path = OUT_DIR / f"{slug}.mp3"

        # Check if already verified Wikimedia file
        if file_path.exists() and file_path.stat().st_size > 1000:
            header = file_path.read_bytes()[:3]
            if header == b"ID3":
                async with lock:
                    wiki_count += 1
                    skipped_count += 1
                    total = wiki_count + edge_count
                    if total % 50 == 0 or total == len(slug_items):
                        print(f"[{total}/{len(slug_items)}] {cased} -> reused ID3 (Wiki: {wiki_count}, Edge: {edge_count})", flush=True)
                return

        async with sem:
            source, data = await fetch_word_audio(cased)
            tmp_path = OUT_DIR / f"{slug}.tmp.mp3"
            tmp_path.write_bytes(data)
            tmp_path.replace(file_path)

            async with lock:
                if source == "wikimedia":
                    wiki_count += 1
                else:
                    edge_count += 1

                total = wiki_count + edge_count
                if total % 25 == 0 or total == len(slug_items):
                    print(f"[{total}/{len(slug_items)}] {cased} -> {source} (Wiki: {wiki_count}, Edge: {edge_count}, SkippedID3: {skipped_count})", flush=True)

            await asyncio.sleep(0.05)

    tasks = [process_item(i, slug, cased) for i, (slug, cased) in enumerate(slug_items)]
    await asyncio.gather(*tasks)

    print(f"Done! {len(slug_items)} words saved. Wikimedia: {wiki_count}, EdgeNeural: {edge_count}.", flush=True)

    ts_content = f"""// Auto-generated native German pronunciation audio registry
// Covers all vocabulary and transcript tokens in Hoerlabor listening tracks.
// All audio files are either authentic native German speaker recordings (Wikimedia Commons)
// or high-fidelity Microsoft Edge Neural native German audio (de-DE-KatjaNeural).

export const BUNDLED_WORD_AUDIO: Record<string, string> = {json.dumps(manifest, ensure_ascii=False, indent=2)};
"""
    bundled_file = PROJECT_DIR / "src" / "data" / "bundledWordAudio.ts"
    bundled_file.write_text(ts_content, encoding="utf-8")
    print(f"Wrote {bundled_file} with {len(manifest)} entries.", flush=True)

if __name__ == "__main__":
    asyncio.run(main())

