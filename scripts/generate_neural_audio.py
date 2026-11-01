import asyncio
import io
import json
from pathlib import Path
import edge_tts
from mutagen.mp3 import MP3

PROJECT_DIR = Path(r"c:\Users\king\Downloads\听力")
AUDIO_DIR = PROJECT_DIR / "public" / "audio"
GENERATED_JSON = PROJECT_DIR / "src" / "data" / "generatedTracks.json"

VOICES = ["de-DE-KatjaNeural", "de-DE-ConradNeural"]

BASE_TRACKS = [
    {
        "id": "a1-wohnung-01",
        "title": "Meine neue Wohnung und der Balkon",
        "level": "A1",
        "source": "水木德语 A1 同步精听",
        "topic": "租房与日常起居",
        "segments": [
            {
                "id": "a1-s1",
                "german": "Hallo! Heute zeige ich dir meine neue Wohnung in Berlin.",
                "chinese": "你好！今天我带你看看我在柏林的新公寓。",
                "clozeWords": ["zeige", "Wohnung"],
                "vocab": [
                    {
                        "word": "die Wohnung",
                        "plural": "die Wohnungen",
                        "pos": "Nomen",
                        "meaning": "公寓，住宅",
                        "exampleDe": "Heute zeige ich dir meine neue Wohnung.",
                        "exampleZh": "今天我带你看看我的新公寓。"
                    }
                ]
            },
            {
                "id": "a1-s2",
                "german": "Das Zimmer ist nicht groß, aber der Balkon ist sehr sonnig und ruhig.",
                "chinese": "房间不大，但阳台非常阳光充足且安静。",
                "clozeWords": ["Zimmer", "Balkon", "sonnig"],
                "vocab": [
                    {
                        "word": "der Balkon",
                        "plural": "die Balkone",
                        "pos": "Nomen",
                        "meaning": "阳台",
                        "exampleDe": "Der Balkon ist sehr sonnig und ruhig.",
                        "exampleZh": "阳台非常阳光充足且安静。"
                    }
                ]
            },
            {
                "id": "a1-s3",
                "german": "Jeden Morgen trinke ich hier einen Kaffee und lerne eine Stunde Deutsch.",
                "chinese": "每天早上我在这里喝一杯咖啡，并学习一小时德语。",
                "clozeWords": ["trinke", "einen", "Stunde"],
                "vocab": [
                    {
                        "word": "die Stunde",
                        "plural": "die Stunden",
                        "pos": "Nomen",
                        "meaning": "小时，课时",
                        "exampleDe": "Ich lerne eine Stunde Deutsch.",
                        "exampleZh": "我学习一小时德语。"
                    }
                ]
            }
        ]
    },
    {
        "id": "b2-uni-testdaf-01",
        "title": "Digitalisierung in der Hochschulbildung",
        "level": "B2",
        "source": "TestDaF 德福校园科研专项",
        "topic": "高等教育与数字化",
        "segments": [
            {
                "id": "b2-s1",
                "german": "In den letzten Jahren hat sich das Studium an deutschen Universitäten stark verändert.",
                "chinese": "近年来，德国大学的学习方式发生了巨大变化。",
                "clozeWords": ["Studium", "Universitäten", "verändert"],
                "vocab": [
                    {
                        "word": "sich verändern",
                        "pos": "Verb",
                        "meaning": "改变，变化",
                        "exampleDe": "Das Studium hat sich stark verändert.",
                        "exampleZh": "大学学习发生了很大变化。"
                    }
                ]
            },
            {
                "id": "b2-s2",
                "german": "Viele Vorlesungen werden online aufgezeichnet, sodass Studierende jederzeit darauf zugreifen können.",
                "chinese": "许多大课都被在线录制下来，以便学生随时可以访问。",
                "clozeWords": ["Vorlesungen", "aufgezeichnet", "zugreifen"],
                "vocab": [
                    {
                        "word": "die Vorlesung",
                        "plural": "die Vorlesungen",
                        "pos": "Nomen",
                        "meaning": "（大学）讲座，大课",
                        "exampleDe": "Viele Vorlesungen werden online aufgezeichnet.",
                        "exampleZh": "许多大学讲座都被在线录制。"
                    },
                    {
                        "word": "zugreifen auf (+Akk)",
                        "pos": "Verb",
                        "meaning": "访问，调取，获取",
                        "exampleDe": "Studierende können jederzeit darauf zugreifen.",
                        "exampleZh": "学生可以随时访问它们。"
                    }
                ]
            }
        ]
    }
]


async def synthesize_sentence_bytes(text: str, voice: str) -> bytes:
    communicate = edge_tts.Communicate(text, voice)
    audio_buffer = bytearray()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer.extend(chunk["data"])
    return bytes(audio_buffer)


async def build_track_audio(track: dict, voice: str) -> dict:
    track_id = track["id"]
    mp3_filename = f"{track_id}.mp3"
    mp3_path = AUDIO_DIR / mp3_filename

    combined_mp3 = bytearray()
    current_time = 0.0

    print(f"正在合成高精度打轴音频: {track['title']} ({voice}) ...")
    for seg in track["segments"]:
        raw_bytes = await synthesize_sentence_bytes(seg["german"], voice)
        mp3_info = MP3(io.BytesIO(raw_bytes)).info
        seg_duration = round(mp3_info.length, 3)

        seg["startTime"] = round(current_time, 3)
        seg["endTime"] = round(current_time + seg_duration, 3)
        current_time += seg_duration
        combined_mp3.extend(raw_bytes)

    mp3_path.write_bytes(bytes(combined_mp3))
    track["audioUrl"] = f"/audio/{mp3_filename}"
    track["duration"] = round(current_time, 3)
    print(f"  -> 已生成 {mp3_path.name} (总时长: {track['duration']}s)")
    return track


async def main():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    existing_generated = []
    if GENERATED_JSON.exists():
        try:
            existing_generated = json.loads(GENERATED_JSON.read_text(encoding="utf-8"))
        except Exception:
            existing_generated = []

    track_map = {t["id"]: t for t in BASE_TRACKS}
    for t in existing_generated:
        track_map[t["id"]] = t

    target_tracks = list(track_map.values())
    completed_tracks = []

    for idx, track in enumerate(target_tracks):
        mp3_file = AUDIO_DIR / f"{track['id']}.mp3"
        if track.get("audioUrl") and mp3_file.exists() and len(track.get("segments", [])) > 0 and track["segments"][0].get("endTime"):
            print(f"[已存在跳过] {track['title']} ({mp3_file.name})")
            completed_tracks.append(track)
            continue

        voice = VOICES[idx % len(VOICES)]
        try:
            updated = await build_track_audio(track, voice)
            completed_tracks.append(updated)
        except Exception as exc:
            print(f"  [警告] {track['id']} 音频合成失败，保留 TTS 模式: {exc}")
            completed_tracks.append(track)

    GENERATED_JSON.write_text(
        json.dumps(completed_tracks, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"\n[全部完成] 共 {len(completed_tracks)} 篇高精度打轴曲目已就绪！")


if __name__ == "__main__":
    asyncio.run(main())
