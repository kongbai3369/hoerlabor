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
    # Remove articles der/die/das/sich at start of vocab phrases
    clean_sent = re.sub(r"^(der|die|das|sich|den|dem|des|ein|eine)\s+", "", sent, flags=re.I)
    clean_sent = re.sub(r"\s*\(\+.*\)", "", clean_sent)
    tokens = re.split(r"[^A-Za-zÄÖÜäöüß]+", clean_sent)
    for tok in tokens:
        if tok and re.match(r"^[A-Za-zÄÖÜäöüß]+$", tok):
            words.add(tok)

print(f"Total unique raw tokens collected: {len(words)}")

# Canonical casing map: lowercase -> best casing (prefer Capitalized for nouns)
canonical_map = {}
for w in sorted(words):
    lower = w.lower()
    if lower not in canonical_map:
        canonical_map[lower] = w
    else:
        existing = canonical_map[lower]
        if w[0].isupper() and not existing[0].isupper():
            canonical_map[lower] = w

print(f"Total unique lowercase words: {len(canonical_map)}")

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

def try_download_wikimedia(url: str, timeout: float = 3.0) -> bytes | None:
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) HoerLabor/2.0"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                data = resp.read()
                if len(data) > 1000:
                    return data
    except Exception:
        pass
    return None

def fetch_wiktionary_image_names(word: str) -> list[str]:
    api_url = f"https://de.wiktionary.org/w/api.php?action=parse&page={urllib.parse.quote(word)}&prop=images&format=json"
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0 HoerLabor/2.0"})
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                images = data.get("parse", {}).get("images", [])
                audio_images = [
                    img for img in images
                    if (img.endswith(".ogg") or img.endswith(".oga") or img.endswith(".mp3"))
                    and (img.startswith("De-") or img.startswith("CPIDL_"))
                ]
                return audio_images
    except Exception:
        pass
    return []

async def fetch_human_or_neural(cased_word: str) -> tuple[str, bytes]:
    cap = cased_word[0].upper() + cased_word[1:]
    low = cased_word.lower()
    cands = [cap, low] if cap != low else [cased_word]

    # Step 1: Direct Wikimedia common patterns (.ogg first)
    for w in cands:
        data = await asyncio.to_thread(try_download_wikimedia, get_wikimedia_mp3_url(f"De-{w}.ogg"), 1.8)
        if data:
            return ("wikimedia", data)

    # Step 2: Try .oga (e.g. Zimmer)
    for w in cands:
        data = await asyncio.to_thread(try_download_wikimedia, get_wikimedia_mp3_url(f"De-{w}.oga"), 1.8)
        if data:
            return ("wikimedia", data)

    # Step 3: High-fidelity Edge Neural German native voice (Microsoft Azure Neural)
    # Never use robotic Google TTS! KatjaNeural provides broadcast-quality German native voice
    communicate = edge_tts.Communicate(cased_word, "de-DE-KatjaNeural")
    audio_chunks = []
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_chunks.append(chunk["data"])
    neural_data = b"".join(audio_chunks)
    return ("edge-neural", neural_data)

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

    wiki_count = 0
    edge_count = 0
    lock = asyncio.Lock()
    sem = asyncio.Semaphore(5)

    print(f"Starting processing for {len(slug_items)} unique audio slugs with concurrency of 5...", flush=True)

    async def process_slug(idx: int, slug: str, cased: str):
        nonlocal wiki_count, edge_count
        file_path = OUT_DIR / f"{slug}.mp3"

        async with sem:
            source, data = await fetch_human_or_neural(cased)
            
            # Write to temporary file then replace to avoid partial writes or locks
            tmp_path = OUT_DIR / f"{slug}.tmp.mp3"
            tmp_path.write_bytes(data)
            tmp_path.replace(file_path)

            async with lock:
                if source == "wikimedia":
                    wiki_count += 1
                else:
                    edge_count += 1

                total_done = wiki_count + edge_count
                if total_done % 50 == 0 or total_done == len(slug_items):
                    print(f"[{total_done}/{len(slug_items)}] {cased} -> {source} (Wikimedia: {wiki_count}, EdgeNeural: {edge_count})", flush=True)

            await asyncio.sleep(0.04)

    tasks = [process_slug(i, slug, cased) for i, (slug, cased) in enumerate(slug_items)]
    await asyncio.gather(*tasks)

    print(f"Completed! Total files: {len(slug_items)}. Wikimedia human: {wiki_count}, Edge Neural human: {edge_count}.", flush=True)

    # Generate bundledWordAudio.ts
    ts_content = f"""// Auto-generated native German pronunciation audio registry
// Covers all vocabulary and transcript tokens in Hoerlabor listening tracks.
// All audio files are either 100% native human recordings (Wikimedia Commons / Wiktionary)
// or high-fidelity Microsoft Edge Neural native German audio (de-DE-KatjaNeural).

export const BUNDLED_WORD_AUDIO: Record<string, string> = {json.dumps(manifest, ensure_ascii=False, indent=2)};
"""
    bundled_file = PROJECT_DIR / "src" / "data" / "bundledWordAudio.ts"
    bundled_file.write_text(ts_content, encoding="utf-8")
    print(f"Wrote {bundled_file} with {len(manifest)} entries.")

if __name__ == "__main__":
    asyncio.run(main())

