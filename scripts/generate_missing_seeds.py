import asyncio
import io
import json
import os
import shutil
from pathlib import Path
import edge_tts
from mutagen.mp3 import MP3

os.environ["HTTP_PROXY"] = "http://127.0.0.1:12450"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:12450"

PROJECT_DIR = Path(r"c:\Users\king\Downloads\听力")
AUDIO_DIR = PROJECT_DIR / "public" / "audio"
DIST_AUDIO_DIR = PROJECT_DIR / "dist" / "audio"
GENERATED_JSON = PROJECT_DIR / "src" / "data" / "generatedTracks.json"

MISSING_TRACKS = [
    {
        "id": "a2-alltag-01",
        "title": "Tagesablauf und Einkaufen am Wochenende",
        "level": "A2",
        "source": "水木德语 A2 同步精听",
        "topic": "周末采购与日常作息",
        "segments": [
            {
                "id": "a2-s1",
                "german": "Am Samstagmorgen stehe ich meistens erst um neun Uhr auf.",
                "chinese": "周六早上我通常直到九点才起床。",
                "clozeWords": ["Samstagmorgen", "stehe", "auf"],
                "vocab": [
                    {
                        "word": "aufstehen",
                        "pos": "Verb (trennbar)",
                        "meaning": "起床（可分动词）",
                        "exampleDe": "Ich stehe meistens um neun Uhr auf.",
                        "exampleZh": "我通常九点起床。"
                    }
                ]
            },
            {
                "id": "a2-s2",
                "german": "Nach dem Frühstück gehe ich auf den Markt, weil das Gemüse dort besonders frisch ist.",
                "chinese": "早饭后我去集市，因为那里的蔬菜特别新鲜。",
                "clozeWords": ["Frühstück", "Markt", "Gemüse"],
                "vocab": [
                    {
                        "word": "das Gemüse",
                        "plural": "-",
                        "pos": "Nomen",
                        "meaning": "蔬菜（集合名词，通常无复数）",
                        "exampleDe": "Das Gemüse auf dem Markt ist frisch.",
                        "exampleZh": "集市上的蔬菜很新鲜。"
                    }
                ]
            }
        ]
    },
    {
        "id": "b1-audiolingua-01",
        "title": "Mit dem Fahrrad durch die Stadt",
        "level": "B1",
        "source": "Audio Lingua 原声话题精选",
        "topic": "城市绿色出行",
        "originalAudioUrl": "https://www.audio-lingua.eu/spip.php?rubrique2",
        "segments": [
            {
                "id": "b1-s1",
                "german": "Obwohl es im Herbst oft regnet, fahre ich fast jeden Tag mit dem Fahrrad zur Universität.",
                "chinese": "尽管秋天经常下雨，我几乎每天还是骑自行车去大学。",
                "clozeWords": ["Obwohl", "regnet", "Fahrrad"],
                "vocab": [
                    {
                        "word": "das Fahrrad",
                        "plural": "die Fahrräder",
                        "pos": "Nomen",
                        "meaning": "自行车",
                        "exampleDe": "Ich fahre mit dem Fahrrad zur Universität.",
                        "exampleZh": "我骑自行车去大学。"
                    }
                ]
            },
            {
                "id": "b1-s2",
                "german": "Man steht nie im Stau und tut gleichzeitig etwas Gutes für die Umwelt.",
                "chinese": "人们绝不会堵在路上，同时还能为环境做点好事。",
                "clozeWords": ["Stau", "gleichzeitig", "Umwelt"],
                "vocab": [
                    {
                        "word": "der Stau",
                        "plural": "die Staus",
                        "pos": "Nomen",
                        "meaning": "交通拥堵，堵车",
                        "exampleDe": "Mit dem Fahrrad steht man nie im Stau.",
                        "exampleZh": "骑车绝不会堵车。"
                    }
                ]
            }
        ]
    }
]


async def synthesize_sentence_bytes(text: str, voice: str) -> bytes:
    comm = edge_tts.Communicate(text, voice)
    stream = bytearray()
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            stream.extend(chunk["data"])
    return bytes(stream)


async def process_track(track: dict, voice: str) -> dict:
    mp3_filename = f"{track['id']}.mp3"
    mp3_path = AUDIO_DIR / mp3_filename
    dist_path = DIST_AUDIO_DIR / mp3_filename

    combined_mp3 = bytearray()
    current_time = 0.0

    print(f"Synthesizing {track['id']} ({voice})...")
    for seg in track["segments"]:
        raw_bytes = await synthesize_sentence_bytes(seg["german"], voice)
        mp3_info = MP3(io.BytesIO(raw_bytes)).info
        seg_duration = round(mp3_info.length, 3)

        seg["startTime"] = round(current_time, 3)
        seg["endTime"] = round(current_time + seg_duration, 3)
        current_time += seg_duration
        combined_mp3.extend(raw_bytes)

    mp3_path.write_bytes(bytes(combined_mp3))
    shutil.copy2(mp3_path, dist_path)

    track["audioUrl"] = f"/audio/{mp3_filename}"
    track["duration"] = round(current_time, 3)
    print(f"Done {mp3_filename}: duration {track['duration']}s")
    return track


async def main():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    DIST_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    tracks = json.loads(GENERATED_JSON.read_text(encoding="utf-8"))
    track_map = {t["id"]: t for t in tracks}

    # Also fix dw-nicos-weg-a1 level
    if "dw-nicos-weg-a1" in track_map:
        track_map["dw-nicos-weg-a1"]["level"] = "A1"
        print("Fixed dw-nicos-weg-a1 level to A1")

    voices = ["de-DE-ConradNeural", "de-DE-AmalaNeural"]
    for idx, t in enumerate(MISSING_TRACKS):
        voice = voices[idx % len(voices)]
        processed = await process_track(t, voice)
        track_map[processed["id"]] = processed

    final_list = list(track_map.values())
    level_order = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "TestDaF": 6}
    final_list.sort(key=lambda t: (level_order.get(t.get("level", "B1"), 99), t.get("source", ""), t.get("id", "")))

    GENERATED_JSON.write_text(
        json.dumps(final_list, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"Updated generatedTracks.json: now {len(final_list)} tracks total.")


if __name__ == "__main__":
    asyncio.run(main())
