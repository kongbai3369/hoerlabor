import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

PROJECT_DIR = Path(r"c:\Users\king\Downloads\听力")
GENERATED_JSON = PROJECT_DIR / "src" / "data" / "generatedTracks.json"
LOCAL_PROXY = "http://127.0.0.1:12450"

# 精选 DW (德国之声) 与 Goethe-Institut (歌德学院) 全等级权威语料库
CURATED_DW_GOETHE_TRACKS = [
    {
        "id": "dw-nicos-weg-a1",
        "title": "DW Nicos Weg: Ankunft am Flughafen",
        "level": "A1",
        "source": "DW Learn German · Nicos Weg",
        "topic": "机场抵达与问路",
        "audioUrl": None,
        "duration": None,
        "segments": [
            {
                "id": "dw-a1-s1",
                "startTime": None,
                "endTime": None,
                "german": "Entschuldigung, ich suche meine Tasche. Sie ist schwarz und ziemlich groß.",
                "chinese": "打扰一下，我在找我的包。它是黑色的，而且相当大。",
                "clozeWords": ["Entschuldigung", "suche", "Tasche"],
                "vocab": [
                    {
                        "word": "die Tasche",
                        "plural": "die Taschen",
                        "pos": "Nomen",
                        "meaning": "手提包，袋子",
                        "exampleDe": "Ich suche meine schwarze Tasche.",
                        "exampleZh": "我在找我的黑色手提包。"
                    }
                ]
            },
            {
                "id": "dw-a1-s2",
                "startTime": None,
                "endTime": None,
                "german": "Wie komme ich am besten mit dem Bus ins Stadtzentrum?",
                "chinese": "我坐公交车怎么去市中心最方便？",
                "clozeWords": ["komme", "besten", "Stadtzentrum"],
                "vocab": [
                    {
                        "word": "das Stadtzentrum",
                        "plural": "die Stadtzentren",
                        "pos": "Nomen",
                        "meaning": "市中心",
                        "exampleDe": "Der Bus fährt direkt ins Stadtzentrum.",
                        "exampleZh": "这辆公交车直达市中心。"
                    }
                ]
            },
            {
                "id": "dw-a1-s3",
                "startTime": None,
                "endTime": None,
                "german": "Nehmen Sie die Linie achtundzwanzig, die Haltestelle ist direkt vor dem Ausgang.",
                "chinese": "请您乘坐28路车，车站就在出口正前方。",
                "clozeWords": ["Nehmen", "Haltestelle", "Ausgang"],
                "vocab": [
                    {
                        "word": "die Haltestelle",
                        "plural": "die Haltestellen",
                        "pos": "Nomen",
                        "meaning": "（公交或电车）车站",
                        "exampleDe": "Die Haltestelle ist direkt vor dem Ausgang.",
                        "exampleZh": "车站就在出口正前方。"
                    },
                    {
                        "word": "der Ausgang",
                        "plural": "die Ausgänge",
                        "pos": "Nomen",
                        "meaning": "出口",
                        "exampleDe": "Wir treffen uns am Ausgang.",
                        "exampleZh": "我们在出口碰面。"
                    }
                ]
            }
        ]
    },
    {
        "id": "goethe-a2-modellsatz",
        "title": "Goethe-Zertifikat A2: Termin beim Arzt vereinbaren",
        "level": "A2",
        "source": "Goethe-Institut 官方样题精选",
        "topic": "看病预约与健康咨询",
        "audioUrl": None,
        "duration": None,
        "segments": [
            {
                "id": "goethe-a2-s1",
                "startTime": None,
                "endTime": None,
                "german": "Guten Tag, Praxis Doktor Müller. Was kann ich für Sie tun?",
                "chinese": "您好，这里是穆勒医生诊所。请问有什么可以帮您？",
                "clozeWords": ["Praxis", "Doktor", "für"],
                "vocab": [
                    {
                        "word": "die Praxis",
                        "plural": "die Praxen",
                        "pos": "Nomen",
                        "meaning": "诊所，事务所",
                        "exampleDe": "Die Praxis ist heute bis achtzehn Uhr geöffnet.",
                        "exampleZh": "诊所今天营业到18点。"
                    }
                ]
            },
            {
                "id": "goethe-a2-s2",
                "startTime": None,
                "endTime": None,
                "german": "Ich habe seit gestern starke Halsschmerzen und leichtes Fieber.",
                "chinese": "我从昨天开始嗓子剧痛，还有点低烧。",
                "clozeWords": ["gestern", "Halsschmerzen", "Fieber"],
                "vocab": [
                    {
                        "word": "das Fieber",
                        "plural": "-",
                        "pos": "Nomen",
                        "meaning": "发烧，体温过高",
                        "exampleDe": "Er hat leichtes Fieber und muss im Bett bleiben.",
                        "exampleZh": "他有点低烧，必须卧床休息。"
                    }
                ]
            },
            {
                "id": "goethe-a2-s3",
                "startTime": None,
                "endTime": None,
                "german": "Kommen Sie bitte heute Nachmittag um fünfzehn Uhr dreißig vorbei und bringen Sie Ihre Versichertenkarte mit.",
                "chinese": "请您今天下午15点30分过来一趟，并带上您的医保卡。",
                "clozeWords": ["Nachmittag", "vorbei", "Versichertenkarte"],
                "vocab": [
                    {
                        "word": "die Versichertenkarte",
                        "plural": "die Versichertenkarten",
                        "pos": "Nomen",
                        "meaning": "医疗保险卡",
                        "exampleDe": "Vergessen Sie Ihre Versichertenkarte bitte nicht.",
                        "exampleZh": "请不要忘记带您的医保卡。"
                    }
                ]
            }
        ]
    },
    {
        "id": "dw-top-thema-b1",
        "title": "DW Top-Thema: Warum immer mehr Studierende im Homeoffice arbeiten",
        "level": "B1",
        "source": "DW Learn German · Top-Thema",
        "topic": "大学生兼职与远程办公",
        "audioUrl": None,
        "duration": None,
        "segments": [
            {
                "id": "dw-b1-s1",
                "startTime": None,
                "endTime": None,
                "german": "Viele Studierende in Deutschland finanzieren ihr Studium durch einen Nebenjob.",
                "chinese": "许多在德国的大学生通过兼职工作来负担自己的学业。",
                "clozeWords": ["finanzieren", "Studium", "Nebenjob"],
                "vocab": [
                    {
                        "word": "der Nebenjob",
                        "plural": "die Nebenjobs",
                        "pos": "Nomen",
                        "meaning": "兼职工作，副业",
                        "exampleDe": "Sie sucht einen flexiblen Nebenjob an der Universität.",
                        "exampleZh": "她正在大学里找一份时间灵活的兼职。"
                    }
                ]
            },
            {
                "id": "dw-b1-s2",
                "startTime": None,
                "endTime": None,
                "german": "Durch flexible Arbeitszeiten lassen sich Vorlesungen und Berufstätigkeit viel besser miteinander verbinden.",
                "chinese": "通过灵活的工作时间，大学课程与职业工作可以更好地结合在一起。",
                "clozeWords": ["Arbeitszeiten", "Vorlesungen", "verbinden"],
                "vocab": [
                    {
                        "word": "die Arbeitszeit",
                        "plural": "die Arbeitszeiten",
                        "pos": "Nomen",
                        "meaning": "工作时间，工时",
                        "exampleDe": "Flexible Arbeitszeiten sind für Studierende sehr wichtig.",
                        "exampleZh": "灵活的工作时间对大学生非常重要。"
                    }
                ]
            },
            {
                "id": "dw-b1-s3",
                "startTime": None,
                "endTime": None,
                "german": "Allerdings fehlt manchen jungen Leuten zu Hause der direkte Austausch mit den Kolleginnen und Kollegen.",
                "chinese": "不过，一些年轻人在家里缺少与同事们的直接交流。",
                "clozeWords": ["Allerdings", "Austausch", "Kollegen"],
                "vocab": [
                    {
                        "word": "der Austausch",
                        "plural": "-",
                        "pos": "Nomen",
                        "meaning": "交流，交换",
                        "exampleDe": "Der persönliche Austausch im Team ist unersetzlich.",
                        "exampleZh": "团队中面对面的交流是不可替代的。"
                    }
                ]
            }
        ]
    },
    {
        "id": "goethe-b2-vortrag",
        "title": "Goethe-Zertifikat B2: Künstliche Intelligenz im Alltag",
        "level": "B2",
        "source": "Goethe-Institut B2 听力真题训练",
        "topic": "人工智能与社会伦理",
        "audioUrl": None,
        "duration": None,
        "segments": [
            {
                "id": "goethe-b2-s1",
                "startTime": None,
                "endTime": None,
                "german": "Künstliche Intelligenz unterstützt uns heute bereits bei der medizinischen Diagnose und in der industriellen Fertigung.",
                "chinese": "如今人工智能已经在医疗诊断和工业制造中为我们提供支持。",
                "clozeWords": ["Intelligenz", "unterstützt", "Fertigung"],
                "vocab": [
                    {
                        "word": "die Fertigung",
                        "plural": "die Fertigungen",
                        "pos": "Nomen",
                        "meaning": "制造，生产",
                        "exampleDe": "In der modernen Fertigung arbeiten viele Roboter.",
                        "exampleZh": "在现代制造业中有许多机器人在工作。"
                    }
                ]
            },
            {
                "id": "goethe-b2-s2",
                "startTime": None,
                "endTime": None,
                "german": "Experten fordern jedoch klare gesetzliche Rahmenbedingungen, um den Datenschutz der Bürger zu gewährleisten.",
                "chinese": "然而专家们呼吁制定明确的法律框架条件，以保障公民的数据隐私。",
                "clozeWords": ["fordern", "Rahmenbedingungen", "gewährleisten"],
                "vocab": [
                    {
                        "word": "der Datenschutz",
                        "plural": "-",
                        "pos": "Nomen",
                        "meaning": "数据保护，隐私保护",
                        "exampleDe": "Der Datenschutz spielt in Europa eine zentrale Rolle.",
                        "exampleZh": "数据保护在欧洲扮演着核心角色。"
                    },
                    {
                        "word": "gewährleisten",
                        "pos": "Verb",
                        "meaning": "保障，确保",
                        "exampleDe": "Die Sicherheit der Daten muss gewährleistet sein.",
                        "exampleZh": "数据的安全性必须得到保障。"
                    }
                ]
            }
        ]
    },
    {
        "id": "testdaf-hv3-energie",
        "title": "TestDaF Hörverstehen 3: Erneuerbare Energien und Speichertechnologien",
        "level": "TestDaF",
        "source": "TestDaF 德福满分16+ 专家访谈模拟",
        "topic": "可再生能源与储能科技",
        "audioUrl": None,
        "duration": None,
        "segments": [
            {
                "id": "td-s1",
                "startTime": None,
                "endTime": None,
                "german": "Der Ausbau von Windkraft und Solarenergie schreitet voran, doch die schwankende Stromerzeugung stellt das Netz vor große Herausforderungen.",
                "chinese": "风能和太阳能的扩建正在推进，但波动的发电量使电网面临巨大挑战。",
                "clozeWords": ["Ausbau", "schwankende", "Herausforderungen"],
                "vocab": [
                    {
                        "word": "der Ausbau",
                        "plural": "-",
                        "pos": "Nomen",
                        "meaning": "扩建，扩展，发展",
                        "exampleDe": "Der Ausbau erneuerbarer Energien ist entscheidend.",
                        "exampleZh": "可再生能源的扩建至关重要。"
                    },
                    {
                        "word": "die Herausforderung",
                        "plural": "die Herausforderungen",
                        "pos": "Nomen",
                        "meaning": "挑战",
                        "exampleDe": "Das stellt die Forscher vor eine große Herausforderung.",
                        "exampleZh": "这使研究人员面临巨大挑战。"
                    }
                ]
            },
            {
                "id": "td-s2",
                "startTime": None,
                "endTime": None,
                "german": "Deshalb erforschen Wissenschaftler derzeit leistungsfähige Wasserstoffspeicher, mit denen sich überschüssige Energie langfristig sichern lässt.",
                "chinese": "因此科学家们目前正在研究高效氢能储存器，借此可以将过剩的能源长期保存下来。",
                "clozeWords": ["erforschen", "leistungsfähige", "überschüssige"],
                "vocab": [
                    {
                        "word": "erforschen",
                        "pos": "Verb",
                        "meaning": "研究，探索，勘探",
                        "exampleDe": "Wissenschaftler erforschen neue Speichertechnologien.",
                        "exampleZh": "科学家们正在研究新的储能技术。"
                    }
                ]
            }
        ]
    }
]


def try_fetch_dw_rss() -> list[dict]:
    """尝试通过本地代理拉取 DW 最新慢速德语/新闻 RSS 条目"""
    rss_url = "https://rss.dw.com/xml/DKpodcast_lgn_de"
    tracks = []
    try:
        proxy_handler = urllib.request.ProxyHandler({
            "http": LOCAL_PROXY,
            "https": LOCAL_PROXY
        })
        opener = urllib.request.build_opener(proxy_handler)
        req = urllib.request.Request(rss_url, headers={"User-Agent": "Mozilla/5.0"})
        with opener.open(req, timeout=5) as resp:
            xml_bytes = resp.read()

        root = ET.fromstring(xml_bytes)
        items = root.findall(".//item")[:2]
        for idx, item in enumerate(items, start=1):
            title = (item.findtext("title") or f"DW Nachrichten #{idx}").strip()
            desc = (item.findtext("description") or "").strip()
            clean_desc = re.sub(r"<[^>]+>", " ", desc)
            sentences = [
                s.strip() for s in re.split(r"(?<=[.!?])\s+", clean_desc)
                if len(s.strip()) > 25
            ][:4]

            if len(sentences) < 2:
                continue

            track_id = f"dw-live-b2-{idx:02d}"
            segments = []
            for s_idx, sent in enumerate(sentences, start=1):
                words = re.findall(r"[A-Za-zÄÖÜäöüß]{5,}", sent)
                cloze = list(dict.fromkeys(words))[:3]
                segments.append({
                    "id": f"{track_id}-s{s_idx}",
                    "startTime": None,
                    "endTime": None,
                    "german": sent,
                    "chinese": "（DW 德国之声慢速新闻实时抓取语料）",
                    "clozeWords": cloze,
                    "vocab": []
                })

            tracks.append({
                "id": track_id,
                "title": f"DW 慢速德语新闻: {title[:36]}",
                "level": "B2",
                "source": "DW Langsam gesprochene Nachrichten",
                "topic": "德国之声时事精听",
                "audioUrl": None,
                "duration": None,
                "segments": segments
            })
        print(f"[DW RSS] 成功通过代理拉取 {len(tracks)} 篇最新 DW 慢速新闻语料！")
    except Exception as exc:
        print(f"[DW RSS 提示] 实时 RSS 跳过 ({exc})，直接启用内置 DW 与歌德权威语料包。")

    return tracks


def main():
    existing = []
    if GENERATED_JSON.exists():
        try:
            existing = json.loads(GENERATED_JSON.read_text(encoding="utf-8"))
        except Exception:
            existing = []

    track_map = {t["id"]: t for t in existing}

    for t in CURATED_DW_GOETHE_TRACKS:
        if t["id"] not in track_map:
            track_map[t["id"]] = t

    for t in try_fetch_dw_rss():
        if t["id"] not in track_map:
            track_map[t["id"]] = t

    merged = list(track_map.values())
    GENERATED_JSON.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"[完成] 曲库已合并更新，当前 generatedTracks.json 共包含 {len(merged)} 篇精听曲目！")


if __name__ == "__main__":
    main()
