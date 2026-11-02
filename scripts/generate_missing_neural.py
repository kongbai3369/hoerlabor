import asyncio
import json
from pathlib import Path
import edge_tts

PROJECT_DIR = Path(r"c:\Users\king\Downloads\听力")
OUT_DIR = PROJECT_DIR / "public" / "audio" / "words"
JSON_FILE = PROJECT_DIR / "scripts" / "missing_neural.json"

async def gen_word(cased: str, out_path: Path):
    voices = ["de-DE-KatjaNeural", "de-DE-KillianNeural", "de-DE-ConradNeural"]
    for attempt in range(4):
        voice = voices[attempt % len(voices)]
        try:
            communicate = edge_tts.Communicate(cased, voice)
            audio_chunks = []
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_chunks.append(chunk["data"])
            data = b"".join(audio_chunks)
            if len(data) > 500:
                out_path.write_bytes(data)
                return True
        except Exception as e:
            await asyncio.sleep(0.5 * (attempt + 1))
    return False

async def main():
    if not JSON_FILE.exists():
        print("missing_neural.json does not exist yet.")
        return

    items = json.loads(JSON_FILE.read_text(encoding="utf-8"))
    print(f"Generating Edge Neural German voice for {len(items)} missing words...")

    success = 0
    failed = 0
    for idx, item in enumerate(items):
        slug = item["slug"]
        cased = item["cased"]
        out_path = OUT_DIR / f"{slug}.mp3"
        ok = await gen_word(cased, out_path)
        if ok:
            success += 1
        else:
            failed += 1
            print(f"[FAIL] {cased} ({slug})")

        if (idx + 1) % 25 == 0 or (idx + 1) == len(items):
            print(f"[{idx + 1}/{len(items)}] Generated: {success}, Failed: {failed}")

        await asyncio.sleep(0.05)

    print(f"Done generating neural audio! Success: {success}, Failed: {failed}.")

if __name__ == "__main__":
    asyncio.run(main())
