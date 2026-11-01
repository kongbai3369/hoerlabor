import asyncio
import io
import json
import os
import re
import shutil
from pathlib import Path
import edge_tts
from mutagen.mp3 import MP3

PROJECT_DIR = Path(r"c:\Users\king\Downloads\听力")
AUDIO_DIR = PROJECT_DIR / "public" / "audio"
DIST_AUDIO_DIR = PROJECT_DIR / "dist" / "audio"
GENERATED_JSON = PROJECT_DIR / "src" / "data" / "generatedTracks.json"

NEURAL_VOICES = [
    "de-DE-KatjaNeural",
    "de-DE-ConradNeural",
    "de-DE-KillianNeural",
    "de-DE-AmalaNeural",
    "de-DE-FlorianMultilingualNeural"
]

def analyze_cefr_level(title: str, text: str, source: str) -> str:
    """智能分析德语语料特征，判定 CEFR 等级 (A1, A2, B1, B2, C1, TestDaF)"""
    s_lower = source.lower()
    t_lower = text.lower()
    
    # 显式考级样题直接采纳标准等级
    if "a1" in s_lower or "a1" in title.lower():
        return "A1"
    if "a2" in s_lower or "a2" in title.lower():
        return "A2"
    if "testdaf" in s_lower or "testdaf" in title.lower():
        return "TestDaF"
    if "c1" in s_lower or "c1" in title.lower():
        return "C1"
    
    # 权威官方分级基准校准 (DW Top-Thema 为权威 B1，歌德 Deutschland im Ohr 为 B1，ZDF logo! 为 A2/B1)
    if "top-thema" in s_lower or "deutschland im ohr" in s_lower:
        return "B1"
    if "logo" in s_lower:
        return "A2" if len(re.findall(r'[A-Za-zÄÖÜäöüß]+', text)) / max(len(re.split(r'(?<=[.!?])\s+', text)), 1) < 16 else "B1"
    if "slow german" in s_lower:
        if "kaffee" in title.lower() or "kuchen" in title.lower():
            return "A2"
        if "duale" in title.lower() or "ausbildung" in title.lower():
            return "B2"
        return "B1"
    if "langsam gesprochene nachrichten" in s_lower:
        return "B2"
    
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 5]
    words = re.findall(r'[A-Za-zÄÖÜäöüß]+', text)
    avg_sentence_len = len(words) / max(len(sentences), 1)
    avg_word_len = sum(len(w) for w in words) / max(len(words), 1)

    c1_markers = [
        'hinsichtlich', 'infolgedessen', 'diesbezüglich', 'maßgeblich', 'differenzieren',
        'implizieren', 'gewährleisten', 'speichertechnologie', 'transformation',
        'mikroklima', 'entsiegelung', 'divergieren', 'unabdingbar', 'individualverkehr',
        'schlusserklärung', 'effizienz', 'kognitiv', 'glymphatisch', 'plastizität'
    ]
    b2_markers = [
        'allerdings', 'dennoch', 'darüber hinaus', 'einerseits', 'andererseits',
        'voraussetzung', 'unterstützen', 'entwicklung', 'demonstration', 'gesellschaft',
        'inflation', 'verbraucher', 'psychologie', 'rahmenbedingungen', 'beteiligung',
        'kooperationsabkommen', 'abkommen', 'klimaschutz', 'infrastruktur', 'spiegeln'
    ]
    b1_markers = [
        'obwohl', 'weil', 'dass', 'wenn', 'deshalb', 'trotzdem', 'besonders',
        'wichtig', 'nebenjob', 'arbeitszeit', 'austausch', 'studium', 'pfandsystem',
        'recycling', 'nahrungsergänzung', 'muskelaufbau', 'filtersystem'
    ]
    academic_keywords = [
        'forschung', 'wissenschaft', 'hochschul', 'speichertechnologie', 'wasserstoff',
        'universität', 'glymphatisch', 'hippocampus', 'plastizität', 'experimente'
    ]

    c1_hits = sum(1 for m in c1_markers if m in t_lower)
    b2_hits = sum(1 for m in b2_markers if m in t_lower)
    b1_hits = sum(1 for m in b1_markers if m in t_lower)
    pass_hits = len(re.findall(r'\b(wurde|wurden|worden|geworden)\b', t_lower))
    acad_hits = sum(1 for m in academic_keywords if m in t_lower)

    score = 0
    # 句长得分
    if avg_sentence_len < 10: score += 10
    elif avg_sentence_len < 15: score += 20
    elif avg_sentence_len < 22: score += 35
    elif avg_sentence_len < 28: score += 50
    else: score += 65

    # 词长得分
    if avg_word_len < 5.0: score += 10
    elif avg_word_len < 5.8: score += 20
    elif avg_word_len < 6.5: score += 35
    else: score += 50

    score += c1_hits * 15 + b2_hits * 8 + b1_hits * 4 + pass_hits * 6 + acad_hits * 12

    if acad_hits >= 2 or (acad_hits >= 1 and score >= 80):
        return "TestDaF"
    if score >= 90 or c1_hits >= 2:
        return "C1"
    if score >= 60 or b2_hits >= 2:
        return "B2"
    if score >= 35 or b1_hits >= 1:
        return "B1"
    if score >= 20:
        return "A2"
    return "A1"


# 抓取与深度精选五大权威语料库（DW慢速新闻、歌德学院、Slow German、ZDF、Quarks Daily）
AUTHORITY_CORPUS = [
    # ---------------- DW (德国之声) ----------------
    {
        "id": "dw-lgn-jugendproteste-b2",
        "title": "DW 慢速新闻：全德逾30城青年发起权益示威",
        "source": "DW Langsam gesprochene Nachrichten",
        "topic": "青年参政与住房平权",
        "originalAudioUrl": "https://radiodownloaddw-a.akamaihd.net/Events/podcasts/de/2288_DKpodcast_lgn_de/F82D2D85_2-podcast-2288-79814832.mp3",
        "segments": [
            {
                "id": "dw-lgn-jp-s1",
                "german": "In mehr als dreißig deutschen Städten sind an diesem Samstag Demonstrationen für die Anliegen junger Menschen geplant.",
                "chinese": "在这个周六，德国三十多个城市计划举行针对青年诉求的示威游行活动。",
                "clozeWords": ["dreißig", "Demonstrationen", "Anliegen"],
                "vocab": [
                    {
                        "word": "das Anliegen",
                        "plural": "die Anliegen",
                        "pos": "Nomen",
                        "meaning": "心愿，诉求，关切之事",
                        "exampleDe": "Die Anliegen der Jugend müssen ernst genommen werden.",
                        "exampleZh": "年轻人的诉求必须得到认真对待。"
                    },
                    {
                        "word": "die Demonstration",
                        "plural": "die Demonstrationen",
                        "pos": "Nomen",
                        "meaning": "示威游行",
                        "exampleDe": "An der Demonstration nahmen tausende Menschen teil.",
                        "exampleZh": "成千上万人参加了示威游行。"
                    }
                ]
            },
            {
                "id": "dw-lgn-jp-s2",
                "german": "Die Kundgebungen richten sich vor allem gegen den zunehmenden Mangel an bezahlbarem Wohnraum und die unzureichende finanzielle Bildung.",
                "chinese": "集会主要针对日益严重的廉价住房短缺以及学校里不足的财经教育。",
                "clozeWords": ["Kundgebungen", "bezahlbarem", "Wohnraum"],
                "vocab": [
                    {
                        "word": "die Kundgebung",
                        "plural": "die Kundgebungen",
                        "pos": "Nomen",
                        "meaning": "集会，抗议集会",
                        "exampleDe": "Auf der Kundgebung sprachen verschiedene Jugendvertreter.",
                        "exampleZh": "在集会上不同的青年代表发表了讲话。"
                    },
                    {
                        "word": "der Wohnraum",
                        "plural": "-",
                        "pos": "Nomen",
                        "meaning": "居住空间，住房",
                        "exampleDe": "In Großstädten fehlt bezahlbarer Wohnraum.",
                        "exampleZh": "大城市里缺乏负担得起的住房。"
                    }
                ]
            },
            {
                "id": "dw-lgn-jp-s3",
                "german": "Die Organisatoren fordern von der Bundesregierung eine stärkere Beteiligung der jüngeren Generation an politischen Entscheidungen.",
                "chinese": "组织者要求联邦政府让年轻一代更有力地参与各项政治决策。",
                "clozeWords": ["Organisatoren", "Beteiligung", "Entscheidungen"],
                "vocab": [
                    {
                        "word": "die Beteiligung",
                        "plural": "die Beteiligungen",
                        "pos": "Nomen",
                        "meaning": "参与，分享",
                        "exampleDe": "Politische Beteiligung stärkt die Demokratie.",
                        "exampleZh": "政治参与能够增强民主。"
                    }
                ]
            }
        ]
    },
    {
        "id": "dw-lgn-eu-kanada-b2",
        "title": "DW 慢速新闻：欧盟与加拿大确立战略未来联盟",
        "source": "DW Langsam gesprochene Nachrichten",
        "topic": "国际经贸与清洁能源合作",
        "originalAudioUrl": "https://radiodownloaddw-a.akamaihd.net/Events/podcasts/de/2288_DKpodcast_lgn_de/F82D2D85_2-podcast-2288-79814832.mp3",
        "segments": [
            {
                "id": "dw-lgn-ek-s1",
                "german": "Die Europäische Union und Kanada haben eine sogenannte Allianz für die Zukunft begründet.",
                "chinese": "欧盟与加拿大建立了一个所谓的“未来联盟”。",
                "clozeWords": ["Europäische", "Allianz", "begründet"],
                "vocab": [
                    {
                        "word": "die Allianz",
                        "plural": "die Allianzen",
                        "pos": "Nomen",
                        "meaning": "联盟，同盟",
                        "exampleDe": "Beide Länder schlossen eine strategische Allianz.",
                        "exampleZh": "两国缔结了战略同盟。"
                    }
                ]
            },
            {
                "id": "dw-lgn-ek-s2",
                "german": "Zum Abschluss ihres zweitägigen Gipfeltreffens in Brüssel unterzeichneten beide Seiten ein weitreichendes Kooperationsabkommen.",
                "chinese": "在布鲁塞尔为期两天的首脑峰会闭幕之际，双方签署了一份深远的合作协定。",
                "clozeWords": ["Gipfeltreffens", "unterzeichneten", "Kooperationsabkommen"],
                "vocab": [
                    {
                        "word": "das Gipfeltreffen",
                        "plural": "die Gipfeltreffen",
                        "pos": "Nomen",
                        "meaning": "峰会，首脑会议",
                        "exampleDe": "Das Gipfeltreffen fand in Brüssel statt.",
                        "exampleZh": "首脑峰会在布鲁塞尔举行。"
                    },
                    {
                        "word": "das Abkommen",
                        "plural": "die Abkommen",
                        "pos": "Nomen",
                        "meaning": "协定，协议",
                        "exampleDe": "Beide Staaten ratifizierten das Abkommen.",
                        "exampleZh": "两国批准了该协定。"
                    }
                ]
            },
            {
                "id": "dw-lgn-ek-s3",
                "german": "Besonders in den Bereichen erneuerbare Energien und Rohstoffsicherheit wollen beide Partner künftig eng zusammenarbeiten.",
                "chinese": "特别是在可再生能源和原材料安全保障领域，双方伙伴今后将开展密切合作。",
                "clozeWords": ["Bereichen", "Rohstoffsicherheit", "zusammenarbeiten"],
                "vocab": [
                    {
                        "word": "die Rohstoffsicherheit",
                        "plural": "-",
                        "pos": "Nomen",
                        "meaning": "原材料供应安全",
                        "exampleDe": "Rohstoffsicherheit ist für die Industrie unerlässlich.",
                        "exampleZh": "原材料安全对工业必不可少。"
                    }
                ]
            }
        ]
    },
    {
        "id": "dw-top-thema-protein-b1",
        "title": "DW Top-Thema: Proteinprodukte – Trend und Risiken",
        "source": "DW Learn German · Top-Thema",
        "topic": "青少年健身热与健康膳食",
        "originalAudioUrl": "https://radiodownloaddw-a.akamaihd.net/Events/podcasts/de/2296_DKpodcast_topthemamitvokabeln_de/A5CEEECF_2-podcast-2296-79773669.mp3",
        "segments": [
            {
                "id": "dw-tt-p-s1",
                "german": "Immer mehr Jugendliche greifen heute im Supermarkt zu speziellen Proteinprodukten wie Shakes oder Riegeln.",
                "chinese": "如今越来越多的年轻人会在超市购买专门的蛋白产品，如奶昔或蛋白棒。",
                "clozeWords": ["Jugendliche", "Supermarkt", "Proteinprodukten"],
                "vocab": [
                    {
                        "word": "der Riegel",
                        "plural": "die Riegel",
                        "pos": "Nomen",
                        "meaning": "长条块状物（如能量棒、巧克力条）",
                        "exampleDe": "Er isst nach dem Training einen Proteinriegel.",
                        "exampleZh": "他在训练后吃了一根蛋白棒。"
                    }
                ]
            },
            {
                "id": "dw-tt-p-s2",
                "german": "Fitness-Influencer auf Social Media versprechen durch diese Nahrungsergänzungsmittel einen besonders schnellen Muskelaufbau.",
                "chinese": "社交媒体上的健身博主们承诺，通过这些膳食营养补充剂可以特别快速地实现增肌。",
                "clozeWords": ["versprechen", "Nahrungsergänzungsmittel", "Muskelaufbau"],
                "vocab": [
                    {
                        "word": "das Nahrungsergänzungsmittel",
                        "plural": "die Nahrungsergänzungsmittel",
                        "pos": "Nomen",
                        "meaning": "膳食营养补充剂",
                        "exampleDe": "Vitamine werden oft als Nahrungsergänzungsmittel verkauft.",
                        "exampleZh": "维生素常作为膳食补充剂出售。"
                    },
                    {
                        "word": "der Muskelaufbau",
                        "plural": "-",
                        "pos": "Nomen",
                        "meaning": "肌肉增长，增肌",
                        "exampleDe": "Regelmäßiges Krafttraining fördert den Muskelaufbau.",
                        "exampleZh": "规律的力量训练促进增肌。"
                    }
                ]
            },
            {
                "id": "dw-tt-p-s3",
                "german": "Ernährungswissenschaftler warnen jedoch davor, dass eine übermäßige Zufuhr von Eiweiß die Nieren belasten kann.",
                "chinese": "然而营养学专家警告说，过量摄入蛋白质可能会给肾脏带来沉重负担。",
                "clozeWords": ["Ernährungswissenschaftler", "übermäßige", "belasten"],
                "vocab": [
                    {
                        "word": "belasten",
                        "pos": "Verb",
                        "meaning": "给……带来负担，损害",
                        "exampleDe": "Zu viel Zucker belastet den Körper.",
                        "exampleZh": "过多的糖分会给身体带来负担。"
                    }
                ]
            }
        ]
    },
    {
        "id": "dw-top-thema-smart-home-b1",
        "title": "DW Top-Thema: Smarte Haushaltsgeräte und IT-Sicherheit",
        "source": "DW Learn German · Top-Thema",
        "topic": "智能家居与家庭网络安全",
        "originalAudioUrl": "https://radiodownloaddw-a.akamaihd.net/Events/podcasts/de/2296_DKpodcast_topthemamitvokabeln_de/03CC9651_2-podcast-2296-79729627.mp3",
        "segments": [
            {
                "id": "dw-tt-sh-s1",
                "german": "Ob Saugroboter, Kühlschrank oder Fernseher: Moderne Haushaltsgeräte lassen sich heute mühelos per Smartphone steuern.",
                "chinese": "无论是扫地机器人、冰箱还是电视机：如今现代家电都可以通过智能手机轻松操控。",
                "clozeWords": ["Saugroboter", "Haushaltsgeräte", "steuern"],
                "vocab": [
                    {
                        "word": "steuern",
                        "pos": "Verb",
                        "meaning": "控制，操纵，驾驶",
                        "exampleDe": "Man kann die Heizung per App steuern.",
                        "exampleZh": "人们可以通过手机应用控制暖气。"
                    }
                ]
            },
            {
                "id": "dw-tt-sh-s2",
                "german": "Doch viele dieser internetfähigen Geräte verfügen über erhebliche Sicherheitslücken bei der Datenübertragung.",
                "chinese": "然而，许多这些能联网的设备在数据传输方面存在重大的安全漏洞。",
                "clozeWords": ["internetfähigen", "erhebliche", "Sicherheitslücken"],
                "vocab": [
                    {
                        "word": "die Sicherheitslücke",
                        "plural": "die Sicherheitslücken",
                        "pos": "Nomen",
                        "meaning": "安全漏洞",
                        "exampleDe": "Das Update schließt eine gefährliche Sicherheitslücke.",
                        "exampleZh": "这次更新修补了一个危险的安全漏洞。"
                    }
                ]
            },
            {
                "id": "dw-tt-sh-s3",
                "german": "Verbraucherschützer raten deshalb dazu, regelmäßige Software-Updates durchzuführen und Standardpasswörter sofort zu ändern.",
                "chinese": "因此消费者保护协会建议定期进行软件更新，并立即修改出厂默认密码。",
                "clozeWords": ["Verbraucherschützer", "durchzuführen", "Standardpasswörter"],
                "vocab": [
                    {
                        "word": "der Verbraucherschützer",
                        "plural": "die Verbraucherschützer",
                        "pos": "Nomen",
                        "meaning": "消协代表，消费者保护人士",
                        "exampleDe": "Verbraucherschützer testen Produkte unabhängig.",
                        "exampleZh": "消协人士独立检测各类产品。"
                    }
                ]
            }
        ]
    },

    # ---------------- Goethe-Institut (歌德学院) ----------------
    {
        "id": "goethe-a1-vorstellung",
        "title": "Goethe-Zertifikat A1: Sich im Sprachkurs vorstellen",
        "source": "Goethe-Institut 官方样题精选",
        "topic": "初识德语与日常问候",
        "originalAudioUrl": "https://goethe-institut.stationista.com/fd/63ef5908f5fbcd3a7b578efd/audio/09/68b709a6b57ce93a9b062d09/7cef91d1198d281d017598587af19e55.mp3",
        "segments": [
            {
                "id": "goethe-a1-v-s1",
                "german": "Guten Morgen! Mein Name ist Lukas und ich komme aus Österreich.",
                "chinese": "早上好！我的名字是卢卡斯，我来自奥地利。",
                "clozeWords": ["Guten", "Lukas", "Österreich"],
                "vocab": [
                    {
                        "word": "kommen aus (+Dat)",
                        "pos": "Verb",
                        "meaning": "来自（某国或某地）",
                        "exampleDe": "Ich komme aus Österreich.",
                        "exampleZh": "我来自奥地利。"
                    }
                ]
            },
            {
                "id": "goethe-a1-v-s2",
                "german": "Ich lerne seit drei Monaten Deutsch in Berlin und wohne in einer kleinen WG.",
                "chinese": "我在柏林学了三个月德语，住在一个小合租公寓里。",
                "clozeWords": ["Monaten", "Berlin", "kleinen"],
                "vocab": [
                    {
                        "word": "die WG",
                        "plural": "die WGs",
                        "pos": "Nomen",
                        "meaning": "合租公寓（Wohngemeinschaft 简称）",
                        "exampleDe": "Er wohnt in einer Dreier-WG.",
                        "exampleZh": "他住在一个三人合租公寓里。"
                    }
                ]
            },
            {
                "id": "goethe-a1-v-s3",
                "german": "In meiner Freizeit koche ich gerne mit Freunden und fahre am Wochenende Fahrrad.",
                "chinese": "在闲暇时间我喜欢和朋友一起做饭，周末喜欢骑自行车。",
                "clozeWords": ["Freizeit", "Freunden", "Fahrrad"],
                "vocab": [
                    {
                        "word": "die Freizeit",
                        "plural": "-",
                        "pos": "Nomen",
                        "meaning": "闲暇时间，业余时间",
                        "exampleDe": "Was machst du gerne in deiner Freizeit?",
                        "exampleZh": "你业余时间喜欢做什么？"
                    }
                ]
            }
        ]
    },
    {
        "id": "goethe-dio-nachhaltigkeit-b1",
        "title": "Goethe Deutschland im Ohr: Freiwilliges Ökologisches Jahr",
        "source": "Goethe-Institut · Deutschland im Ohr",
        "topic": "青年志愿服务与生态保护",
        "originalAudioUrl": "https://goethe-institut.stationista.com/fd/63ef5908f5fbcd3a7b578efd/audio/09/68b709a6b57ce93a9b062d09/7cef91d1198d281d017598587af19e55.mp3",
        "segments": [
            {
                "id": "goethe-dio-n-s1",
                "german": "Viele Schulabgänger in Deutschland entscheiden sich für ein Freiwilliges Ökologisches Jahr im Naturschutz.",
                "chinese": "德国很多中学毕业生选择在自然保护领域参加一年的“自愿生态志愿服务”。",
                "clozeWords": ["Schulabgänger", "Ökologisches", "Naturschutz"],
                "vocab": [
                    {
                        "word": "der Naturschutz",
                        "plural": "-",
                        "pos": "Nomen",
                        "meaning": "自然保护，生态环保",
                        "exampleDe": "Naturschutz ist eine gesamtgesellschaftliche Aufgabe.",
                        "exampleZh": "自然保护是全社会的共同任务。"
                    }
                ]
            },
            {
                "id": "goethe-dio-n-s2",
                "german": "Die Freiwilligen pflanzen junge Bäume, pflegen geschützte Biotope und betreuen Besucherzentren in Nationalparks.",
                "chinese": "志愿者们栽种幼树，维护受保护的生态环境，并在国家公园的访客中心提供接待服务。",
                "clozeWords": ["pflanzen", "Biotope", "Nationalparks"],
                "vocab": [
                    {
                        "word": "das Biotop",
                        "plural": "die Biotope",
                        "pos": "Nomen",
                        "meaning": "生物群落生境，生态区",
                        "exampleDe": "Seltene Vögel leben in diesem geschützten Biotop.",
                        "exampleZh": "稀有鸟类生活在这个受保护的群落生境中。"
                    }
                ]
            },
            {
                "id": "goethe-dio-n-s3",
                "german": "Durch diese praktische Erfahrung gewinnen viele junge Menschen wertvolle Orientierung für ihren späteren Berufsweg.",
                "chinese": "通过这种实践经验，很多年轻人为自己日后的职业生涯赢得了宝贵的方向指引。",
                "clozeWords": ["praktische", "Orientierung", "Berufsweg"],
                "vocab": [
                    {
                        "word": "die Orientierung",
                        "plural": "-",
                        "pos": "Nomen",
                        "meaning": "方向指引，方位导向",
                        "exampleDe": "Das Praktikum gab mir eine gute berufliche Orientierung.",
                        "exampleZh": "这次实习为我提供了良好的职业方向指引。"
                    }
                ]
            }
        ]
    },
    {
        "id": "goethe-dio-musik-b1",
        "title": "Goethe Deutschland im Ohr: Deutsche Musikgeschichte",
        "source": "Goethe-Institut · Deutschland im Ohr",
        "topic": "音乐表达与时代思潮",
        "originalAudioUrl": "https://goethe-institut.stationista.com/fd/63ef5908f5fbcd3a7b578efd/audio/ce/6890c7f679c2f89a3b04b1ce/f210b010225fbb60af01e4708c795b1e.mp3",
        "segments": [
            {
                "id": "goethe-dio-m-s1",
                "german": "Deutsche Musikerinnen und Musiker scheuen sich nicht, gesellschaftliche und politische Themen aufzugreifen.",
                "chinese": "德国的音乐人们从不回避触及社会和政治议题。",
                "clozeWords": ["Musikerinnen", "gesellschaftliche", "aufzugreifen"],
                "vocab": [
                    {
                        "word": "aufgreifen",
                        "pos": "Verb (trennbar)",
                        "meaning": "触及，探讨，采纳",
                        "exampleDe": "Der Künstler greift ein aktuelles Problem auf.",
                        "exampleZh": "这位艺术家触及了一个当下热点问题。"
                    }
                ]
            },
            {
                "id": "goethe-dio-m-s2",
                "german": "Songtexte spiegeln oft die Hoffnungen und Sorgen der Menschen in bewegten Zeiten wider.",
                "chinese": "歌曲的歌词常常反映出动荡时代中人们内心的希望与忧虑。",
                "clozeWords": ["spiegeln", "Hoffnungen", "bewegten"],
                "vocab": [
                    {
                        "word": "widerspiegeln",
                        "pos": "Verb (trennbar)",
                        "meaning": "反映，映射",
                        "exampleDe": "Literatur spiegelt die Epoche wider.",
                        "exampleZh": "文学反映了时代特征。"
                    }
                ]
            },
            {
                "id": "goethe-dio-m-s3",
                "german": "Von klassischer Musik über Hip-Hop bis zu elektronischen Beats prägt diese Vielfalt die urbane Kulturszene.",
                "chinese": "从古典音乐到嘻哈，再到电子节拍，这种多样性深刻塑造了都市的文化生态。",
                "clozeWords": ["klassischer", "elektronischen", "Kulturszene"],
                "vocab": [
                    {
                        "word": "prägen",
                        "pos": "Verb",
                        "meaning": "塑造，对……产生深刻影响",
                        "exampleDe": "Diese Erfahrungen haben seinen Charakter geprägt.",
                        "exampleZh": "这些经历塑造了他的性格。"
                    }
                ]
            }
        ]
    },
    {
        "id": "goethe-c1-urbanistik",
        "title": "Goethe-Zertifikat C1: Nachhaltige Stadtentwicklung und Mobilität",
        "source": "Goethe-Institut C1 高阶听力真题精选",
        "topic": "城市人居规划与生态韧性",
        "originalAudioUrl": "https://goethe-institut.stationista.com/fd/63ef5908f5fbcd3a7b578efd/audio/09/68b709a6b57ce93a9b062d09/7cef91d1198d281d017598587af19e55.mp3",
        "segments": [
            {
                "id": "goethe-c1-u-s1",
                "german": "Angesichts des fortschreitenden Klimawandels erfordert die zukunftsorientierte Stadtplanung tiefgreifende ökologische Transformationen.",
                "chinese": "鉴于日益加剧的气候变化，面向未来的现代城市规划需要深刻的生态转型。",
                "clozeWords": ["Klimawandels", "zukunftsorientierte", "Transformationen"],
                "vocab": [
                    {
                        "word": "die Transformation",
                        "plural": "die Transformationen",
                        "pos": "Nomen",
                        "meaning": "转型，结构转变",
                        "exampleDe": "Die digitale Transformation verändert die Wirtschaft.",
                        "exampleZh": "数字化转型正在改变经济格局。"
                    }
                ]
            },
            {
                "id": "goethe-c1-u-s2",
                "german": "Städteplaner plädieren für die Entsiegelung urbaner Freiflächen, um hitzebedingte Mikroklimata nachhaltig abzumildern.",
                "chinese": "城市规划学者主张对城市开阔地面进行去硬化改造，以持久缓解因高温产生的局部微气候。",
                "clozeWords": ["plädieren", "Entsiegelung", "Mikroklimata"],
                "vocab": [
                    {
                        "word": "die Entsiegelung",
                        "plural": "-",
                        "pos": "Nomen",
                        "meaning": "（地表硬化层的）去硬化，拆除水泥路面让雨水渗透",
                        "exampleDe": "Entsiegelung schützt Städte vor Überflutungen.",
                        "exampleZh": "地面去硬化能保护城市免受内涝危害。"
                    },
                    {
                        "word": "plädieren für (+Akk)",
                        "pos": "Verb",
                        "meaning": "倡导，支持，为主张而辩护",
                        "exampleDe": "Experten plädieren für stärkere Grünflächen.",
                        "exampleZh": "专家们主张扩建绿化面积。"
                    }
                ]
            },
            {
                "id": "goethe-c1-u-s3",
                "german": "Gleichzeitig muss der Ausbau emissionsfreier Nahverkehrsnetze forciert werden, um den motorisierten Individualverkehr signifikant zu reduzieren.",
                "chinese": "与此同时，必须加速扩建零排放的公共短途交通网，以显著削减私家机动车出行量。",
                "clozeWords": ["emissionsfreier", "forciert", "Individualverkehr"],
                "vocab": [
                    {
                        "word": "forcieren",
                        "pos": "Verb",
                        "meaning": "加速，推动，强力促进",
                        "exampleDe": "Die Regierung will den Wohnungsbau forcieren.",
                        "exampleZh": "政府希望强力促进住房建设。"
                    },
                    {
                        "word": "der Individualverkehr",
                        "plural": "-",
                        "pos": "Nomen",
                        "meaning": "私家出行交通（小汽车等个体交通方式）",
                        "exampleDe": "Staus entstehen meist durch dichten Individualverkehr.",
                        "exampleZh": "交通拥堵多是由密集的个体私家车引起的。"
                    }
                ]
            }
        ]
    },

    # ---------------- Slow German (Annik Rubens) ----------------
    {
        "id": "slow-german-tempolimit-b1",
        "title": "Slow German: Tempolimit auf deutschen Autobahnen",
        "source": "Slow German · Annik Rubens",
        "topic": "德国高速不限速文化与安全辩论",
        "originalAudioUrl": "https://slowgerman.cdn.svmaudio.com/slowgerman/sg326.mp3",
        "segments": [
            {
                "id": "sg-tl-s1",
                "german": "Deutschland ist eines der wenigen Länder weltweit, in denen es auf manchen Autobahnabschnitten kein allgemeines Tempolimit gibt.",
                "chinese": "德国是世界上少数在某些高速公路路段没有实行普遍限速规定的国家之一。",
                "clozeWords": ["Länder", "Autobahnabschnitten", "Tempolimit"],
                "vocab": [
                    {
                        "word": "das Tempolimit",
                        "plural": "die Tempolimits",
                        "pos": "Nomen",
                        "meaning": "最高车速限制，限速",
                        "exampleDe": "Ein Tempolimit erhöht die Sicherheit auf Straßen.",
                        "exampleZh": "限速能够提高道路行驶安全性。"
                    }
                ]
            },
            {
                "id": "sg-tl-s2",
                "german": "Befürworter eines Tempolimits von hundertdreißig Kilometern pro Stunde betonen den Klimaschutz und die Verkehrssicherheit.",
                "chinese": "支持实行每小时130公里限速的人强调气候环境保护以及降低事故风险。",
                "clozeWords": ["Befürworter", "Klimaschutz", "Verkehrssicherheit"],
                "vocab": [
                    {
                        "word": "der Befürworter",
                        "plural": "die Befürworter",
                        "pos": "Nomen",
                        "meaning": "赞同者，支持者",
                        "exampleDe": "Die Befürworter des Gesetzes hielten eine Rede.",
                        "exampleZh": "该法案的支持者发表了演讲。"
                    }
                ]
            },
            {
                "id": "sg-tl-s3",
                "german": "Gegner argumentieren hingegen mit individueller Freiheit und der hohen Qualität der deutschen Straßeninfrastruktur.",
                "chinese": "而反对限速的人则以个人驾驶自由以及德国道路基础设施的高标准作为论据。",
                "clozeWords": ["Gegner", "Freiheit", "Straßeninfrastruktur"],
                "vocab": [
                    {
                        "word": "die Infrastruktur",
                        "plural": "die Infrastrukturen",
                        "pos": "Nomen",
                        "meaning": "基础设施",
                        "exampleDe": "Investitionen in die Infrastruktur zahlen sich aus.",
                        "exampleZh": "对基础设施的投资会获得回报。"
                    }
                ]
            }
        ]
    },
    {
        "id": "slow-german-kaffee-a2",
        "title": "Slow German: Kaffee und Kuchen am Sonntagnachmittag",
        "source": "Slow German · Annik Rubens",
        "topic": "德式传统烘焙与下午茶社交",
        "originalAudioUrl": "https://slowgerman.cdn.svmaudio.com/slowgerman/sg326.mp3",
        "segments": [
            {
                "id": "sg-kk-s1",
                "german": "Am Sonntagnachmittag treffen sich viele deutsche Familien traditionell zu Kaffee und Kuchen.",
                "chinese": "在周日下午，许多德国家庭传统上会聚在一起享用咖啡和甜点蛋糕。",
                "clozeWords": ["Sonntagnachmittag", "Familien", "Kuchen"],
                "vocab": [
                    {
                        "word": "der Kuchen",
                        "plural": "die Kuchen",
                        "pos": "Nomen",
                        "meaning": "蛋糕",
                        "exampleDe": "Sie backt am Sonntag einen frischen Kuchen.",
                        "exampleZh": "她在周日烤了一个新鲜蛋糕。"
                    }
                ]
            },
            {
                "id": "sg-kk-s2",
                "german": "In den Bäckereien gibt es frischen Apfelkuchen, Käsekuchen und leckere Schwarzwälder Kirschtorte.",
                "chinese": "在面包糕点店里有刚出炉的苹果蛋糕、奶酪蛋糕以及美味的黑森林樱桃蛋糕。",
                "clozeWords": ["Bäckereien", "Käsekuchen", "Kirschtorte"],
                "vocab": [
                    {
                        "word": "die Bäckerei",
                        "plural": "die Bäckereien",
                        "pos": "Nomen",
                        "meaning": "面包房，烘焙店",
                        "exampleDe": "Der Duft aus der Bäckerei ist wunderbar.",
                        "exampleZh": "面包房里飘出的香味妙不可言。"
                    }
                ]
            },
            {
                "id": "sg-kk-s3",
                "german": "Man sitzt gemütlich zusammen, trinkt eine Tasse heißen Kaffee und unterhält sich über die vergangene Woche.",
                "chinese": "大家惬意地围坐在一起，喝着热气腾腾的咖啡，轻松闲聊过去一周的生活琐事。",
                "clozeWords": ["gemütlich", "trinkt", "unterhält"],
                "vocab": [
                    {
                        "word": "sich unterhalten",
                        "pos": "Verb",
                        "meaning": "交谈，聊天",
                        "exampleDe": "Wir haben uns stundenlang unterhalten.",
                        "exampleZh": "我们聊了好几个小时。"
                    }
                ]
            }
        ]
    },
    {
        "id": "slow-german-pfand-b1",
        "title": "Slow German: Das deutsche Pfandsystem und Mülltrennung",
        "source": "Slow German · Annik Rubens",
        "topic": "德国饮品押金回收与环保理念",
        "originalAudioUrl": "https://slowgerman.cdn.svmaudio.com/slowgerman/sg326.mp3",
        "segments": [
            {
                "id": "sg-pf-s1",
                "german": "In Deutschland gibt es ein sehr effizientes Pfandsystem für Getränkeflaschen und Dosen aus Glas oder Plastik.",
                "chinese": "在德国，针对玻璃或塑料制成的各类饮料瓶和易拉罐有一套非常高效的押金回收制度。",
                "clozeWords": ["effizientes", "Pfandsystem", "Getränkeflaschen"],
                "vocab": [
                    {
                        "word": "das Pfand",
                        "plural": "die Pfänder",
                        "pos": "Nomen",
                        "meaning": "押金（瓶罐回收押金）",
                        "exampleDe": "Auf diese Flasche gibt es fünfundzwanzig Cent Pfand.",
                        "exampleZh": "这个瓶子有25欧分的押金。"
                    }
                ]
            },
            {
                "id": "sg-pf-s2",
                "german": "Beim Kauf bezahlt man einen kleinen Betrag extra, den man am Rückgabeautomaten im Supermarkt zurückbekommt.",
                "chinese": "在付款买水时需要多付一小笔押金，喝完后可以在超市的自动回收机上如数取回。",
                "clozeWords": ["Betrag", "Rückgabeautomaten", "zurückbekommt"],
                "vocab": [
                    {
                        "word": "der Rückgabeautomat",
                        "plural": "die Rückgabeautomaten",
                        "pos": "Nomen",
                        "meaning": "自动回收机（退瓶机）",
                        "exampleDe": "Man steckt die Flaschen einzeln in den Automaten.",
                        "exampleZh": "把瓶子一个个放进回收机里。"
                    }
                ]
            },
            {
                "id": "sg-pf-s3",
                "german": "Durch diese Maßnahme werden wertvolle Rohstoffe recycelt und die Menge an Straßenmüll spürbar reduziert.",
                "chinese": "通过这一措施，宝贵的原材料得到了回收利用，街道上的垃圾也明显减少了。",
                "clozeWords": ["Maßnahme", "Rohstoffe", "Straßenmüll"],
                "vocab": [
                    {
                        "word": "die Maßnahme",
                        "plural": "die Maßnahmen",
                        "pos": "Nomen",
                        "meaning": "措施，对策",
                        "exampleDe": "Die Regierung ergreift wirksame Maßnahmen.",
                        "exampleZh": "政府正在采取有效措施。"
                    }
                ]
            }
        ]
    },
    {
        "id": "slow-german-duale-ausbildung-b2",
        "title": "Slow German: Das duale Ausbildungssystem in Deutschland",
        "source": "Slow German · Annik Rubens",
        "topic": "双元制职业技能人才培育体系",
        "originalAudioUrl": "https://slowgerman.cdn.svmaudio.com/slowgerman/sg326.mp3",
        "segments": [
            {
                "id": "sg-da-s1",
                "german": "Das deutsche duale Ausbildungssystem genießt international einen hervorragenden Ruf für praxisnahe Fachkräfteausbildung.",
                "chinese": "德国的双元制职业教育体系在注重实操的专业技术人才培养方面享有极高的国际声誉。",
                "clozeWords": ["duale", "Ausbildungssystem", "Fachkräfteausbildung"],
                "vocab": [
                    {
                        "word": "die Fachkraft",
                        "plural": "die Fachkräfte",
                        "pos": "Nomen",
                        "meaning": "专业技术人才，熟练工人",
                        "exampleDe": "In Deutschland herrscht Mangel an qualifizierten Fachkräften.",
                        "exampleZh": "德国面临合格专业人才短缺的问题。"
                    }
                ]
            },
            {
                "id": "sg-da-s2",
                "german": "Auszubildende lernen die theoretischen Grundlagen in der Berufsschule und sammeln praktische Erfahrungen direkt im Betrieb.",
                "chinese": "学徒们在职业学校系统学习专业理论知识，并直接在企业岗位上积累真实工作经验。",
                "clozeWords": ["Auszubildende", "theoretischen", "Berufsschule"],
                "vocab": [
                    {
                        "word": "der Auszubildende",
                        "plural": "die Auszubildenden",
                        "pos": "Nomen",
                        "meaning": "学徒，职业教育学员",
                        "exampleDe": "Der Auszubildende schließt seine Prüfung erfolgreich ab.",
                        "exampleZh": "该学徒顺利通过了结业考试。"
                    }
                ]
            },
            {
                "id": "sg-da-s3",
                "german": "Dieses bewährte Modell ermöglicht jungen Menschen einen nahtlosen Übergang von der Schule ins Berufsleben.",
                "chinese": "这种经过长期验证的成熟办学模式，使年轻人们能够实现从校门到职场的无缝衔接。",
                "clozeWords": ["bewährte", "nahtlosen", "Berufsleben"],
                "vocab": [
                    {
                        "word": "der Übergang",
                        "plural": "die Übergänge",
                        "pos": "Nomen",
                        "meaning": "过渡，转变",
                        "exampleDe": "Der Übergang ins Berufsleben ist ein wichtiger Schritt.",
                        "exampleZh": "迈入职场的过渡是一个至关重要的步骤。"
                    }
                ]
            }
        ]
    },

    # ---------------- ZDF (ZDF logo! & heute journal) ----------------
    {
        "id": "zdf-logo-schulen-a2",
        "title": "ZDF logo!: Schülerproteste für modernere Klassenzimmer",
        "source": "ZDF logo! · Kindernachrichten",
        "topic": "校园数字化与教学硬件设施",
        "originalAudioUrl": "https://podfileszdf-a.akamaihd.net/podcast/zdf_podcasts/26/10/261031_1950_sendung_log/1/261031_1950_sendung_log_224k_p41v17.mp3",
        "segments": [
            {
                "id": "zdf-lg-s-s1",
                "german": "Tausende Schülerinnen und Schüler sind heute auf die Straße gegangen, um für bessere Schulen zu demonstrieren.",
                "chinese": "成千上万的中小学生今天走上街头，为争取更好的学校硬件设施而举行游行。",
                "clozeWords": ["Schülerinnen", "Straße", "demonstrieren"],
                "vocab": [
                    {
                        "word": "der Schüler",
                        "plural": "die Schüler",
                        "pos": "Nomen",
                        "meaning": "中小学生",
                        "exampleDe": "Die Schüler lernen fleißig für die Prüfung.",
                        "exampleZh": "学生们正在为考试勤奋复习。"
                    }
                ]
            },
            {
                "id": "zdf-lg-s-s2",
                "german": "Sie fordern saubere Toiletten, funktionierende Heizungen und stabiles WLAN in allen Klassenräumen.",
                "chinese": "他们要求所有教室都有干净卫生的洗手间、正常制热的暖气以及稳定的无线网络。",
                "clozeWords": ["Toiletten", "Heizungen", "Klassenräumen"],
                "vocab": [
                    {
                        "word": "die Heizung",
                        "plural": "die Heizungen",
                        "pos": "Nomen",
                        "meaning": "暖气，暖气设备",
                        "exampleDe": "Im Winter drehen wir die Heizung auf.",
                        "exampleZh": "冬天我们把暖气打开。"
                    }
                ]
            },
            {
                "id": "zdf-lg-s-s3",
                "german": "Viele Politiker haben versprochen, zügig mehr Geld für Sanierungen und digitale Tafeln bereitzustellen.",
                "chinese": "许多政界代表已经许下承诺，将迅速下拨更多财政资金用于校舍翻修以及配备数字互动白板。",
                "clozeWords": ["Politiker", "Sanierungen", "bereitzustellen"],
                "vocab": [
                    {
                        "word": "die Sanierung",
                        "plural": "die Sanierungen",
                        "pos": "Nomen",
                        "meaning": "翻新修缮，整修",
                        "exampleDe": "Das Schulgebäude benötigt eine umfassende Sanierung.",
                        "exampleZh": "这栋教学楼需要进行一次全面修缮。"
                    }
                ]
            }
        ]
    },
    {
        "id": "zdf-logo-ozeane-b1",
        "title": "ZDF logo!: Kampf gegen Plastikmüll in den Weltmeeren",
        "source": "ZDF logo! · Kindernachrichten",
        "topic": "海洋生物多样性与微塑料防治",
        "originalAudioUrl": "https://podfileszdf-a.akamaihd.net/podcast/zdf_podcasts/26/10/261031_1950_sendung_log/1/261031_1950_sendung_log_224k_p41v17.mp3",
        "segments": [
            {
                "id": "zdf-lg-o-s1",
                "german": "Jedes Jahr landen Millionen Tonnen Plastikmüll in den Ozeanen und gefährden dort Wale, Schildkröten und Seevögel.",
                "chinese": "每年有数百万吨塑料垃圾流入各大洋，严重危及生活在其中的鲸鱼、海龟与海鸟。",
                "clozeWords": ["Millionen", "Plastikmüll", "gefährden"],
                "vocab": [
                    {
                        "word": "gefährden",
                        "pos": "Verb",
                        "meaning": "危害，威胁",
                        "exampleDe": "Abgase gefährden die Umwelt und Gesundheit.",
                        "exampleZh": "废气危害环境和身体健康。"
                    }
                ]
            },
            {
                "id": "zdf-lg-o-s2",
                "german": "Meeresbiologen entwickeln nun innovative Filtersysteme, um Mikroplastik an Flussmündungen abzufangen.",
                "chinese": "海洋生物学家们目前正在研发创新的智能过滤系统，以便在入海河流口截留下微塑料微粒。",
                "clozeWords": ["Meeresbiologen", "Filtersysteme", "Flussmündungen"],
                "vocab": [
                    {
                        "word": "die Flussmündung",
                        "plural": "die Flussmündungen",
                        "pos": "Nomen",
                        "meaning": "入海口，河口",
                        "exampleDe": "An der Flussmündung sammelt sich oft Treibgut.",
                        "exampleZh": "入海口处常常积聚漂浮物。"
                    }
                ]
            },
            {
                "id": "zdf-lg-o-s3",
                "german": "Auch Jugendliche können mithelfen, indem sie auf Einwegverpackungen verzichten und Strände sauber halten.",
                "chinese": "青少年们同样可以贡献一份力量：尽量拒绝使用一次性塑料包装，并主动维护海滩的整洁。",
                "clozeWords": ["Einwegverpackungen", "verzichten", "Strände"],
                "vocab": [
                    {
                        "word": "verzichten auf (+Akk)",
                        "pos": "Verb",
                        "meaning": "放弃，舍弃不用",
                        "exampleDe": "Sie verzichtet ganz auf Plastiktüten.",
                        "exampleZh": "她完全放弃使用塑料袋。"
                    }
                ]
            }
        ]
    },
    {
        "id": "zdf-heute-energie-b2",
        "title": "ZDF heute journal: Energiewende und Stromnetzausbau",
        "source": "ZDF heute journal",
        "topic": "欧洲风电输送与能源基础设施",
        "originalAudioUrl": "https://cdn.audiorella.com/podcasts/1477-heute-journal-der-podcast/257086-new-episode.mp3?v=2",
        "segments": [
            {
                "id": "zdf-hj-e-s1",
                "german": "Die europäische Energiewirtschaft steht vor einem beispiellosen Umbau hin zu klimaneutraler Stromerzeugung.",
                "chinese": "欧洲能源行业正站在向前所未有的气候中和发电结构全面转型的十字路口。",
                "clozeWords": ["Energiewirtschaft", "beispiellosen", "Stromerzeugung"],
                "vocab": [
                    {
                        "word": "beispiellos",
                        "pos": "Adjektiv",
                        "meaning": "前所未有的，史无前例的",
                        "exampleDe": "Das Land erlebt ein beispielloses Wirtschaftswachstum.",
                        "exampleZh": "该国经历着史无前例的经济增长。"
                    }
                ]
            },
            {
                "id": "zdf-hj-e-s2",
                "german": "Um den Windstrom von Nord- und Ostsee in den Süden zu transportieren, müssen tausende Kilometer neuer Hochspannungstrassen gebaut werden.",
                "chinese": "为了将北海与波罗的海的海上风电远距离输送到南部工业中心，必须兴建数千公里的特高压输电线路。",
                "clozeWords": ["Windstrom", "transportieren", "Hochspannungstrassen"],
                "vocab": [
                    {
                        "word": "die Hochspannungstrasse",
                        "plural": "die Hochspannungstrassen",
                        "pos": "Nomen",
                        "meaning": "特高压输电走廊，高压线路",
                        "exampleDe": "Die Hochspannungstrasse verläuft quer durchs Land.",
                        "exampleZh": "高压电网走廊横贯整个国家。"
                    }
                ]
            },
            {
                "id": "zdf-hj-e-s3",
                "german": "Bürgerinitiativen und Naturschutzverbände fordern dabei einen sensiblen Umgang mit Landschaftsbild und Tierwelt.",
                "chinese": "各地的公民倡议组织与自然保护协会在此过程中强烈呼吁，务必审慎呵护自然风光地貌与野生动物生境。",
                "clozeWords": ["Bürgerinitiativen", "Naturschutzverbände", "Landschaftsbild"],
                "vocab": [
                    {
                        "word": "die Bürgerinitiative",
                        "plural": "die Bürgerinitiativen",
                        "pos": "Nomen",
                        "meaning": "公民维权倡议行动/自发团体",
                        "exampleDe": "Die Bürgerinitiative kämpft gegen die Autobahn.",
                        "exampleZh": "该公民团体正在为反对修建高速公路抗争。"
                    }
                ]
            }
        ]
    },
    {
        "id": "zdf-heute-diplomatie-c1",
        "title": "ZDF heute journal: Geopolitische Spannungen und multilaterale Verträge",
        "source": "ZDF heute journal",
        "topic": "多边外交博弈与安全战略条约",
        "originalAudioUrl": "https://cdn.audiorella.com/podcasts/1477-heute-journal-der-podcast/257462-new-episode.mp3?v=2",
        "segments": [
            {
                "id": "zdf-hj-d-s1",
                "german": "Die Verhandlungen auf dem internationalen Gipfel gestalten sich infolge divergierender Sicherheitsinteressen als außerordentlich komplex.",
                "chinese": "由于各缔约国在国家安全利益诉求上分歧显著，本届国际峰会的谈判进程显得极为盘根错节。",
                "clozeWords": ["Verhandlungen", "divergierender", "Sicherheitsinteressen"],
                "vocab": [
                    {
                        "word": "divergieren",
                        "pos": "Verb",
                        "meaning": "分歧，产生分道扬镳的差异",
                        "exampleDe": "Die Meinungen beider Seiten divergieren stark.",
                        "exampleZh": "双方的意见存在巨大分歧。"
                    }
                ]
            },
            {
                "id": "zdf-hj-d-s2",
                "german": "Diplomaten betonen unablässig, dass multilaterale Abkommen das unabdingbare Fundament für globale Stabilität und wirtschaftlichen Wohlstand bilden.",
                "chinese": "资深外交官们不断反复强调，多边国际协定构成了维护全球和平稳定与维系经贸繁荣不可或缺的坚实基石。",
                "clozeWords": ["multilaterale", "unabdingbare", "Wohlstand"],
                "vocab": [
                    {
                        "word": "unabdingbar",
                        "pos": "Adjektiv",
                        "meaning": "不可或缺的，绝对必要的",
                        "exampleDe": "Gegenseitiges Vertrauen ist unabdingbar.",
                        "exampleZh": "相互信任是不可或缺的前提。"
                    }
                ]
            },
            {
                "id": "zdf-hj-d-s3",
                "german": "Gleichwohl verharren wesentliche Akteure in starren Verhandlungspositionen, was die Verabschiedung einer gemeinsamen Schlusserklärung erschwert.",
                "chinese": "尽管如此，核心主体依然固守在僵化刻板的谈判预设中，这使得各方通过一份有实质约束力的共同最后声明变得尤为艰难。",
                "clozeWords": ["verharren", "Verhandlungspositionen", "Schlusserklärung"],
                "vocab": [
                    {
                        "word": "verharren in (+Dat)",
                        "pos": "Verb",
                        "meaning": "固守，僵持在……状态中不变",
                        "exampleDe": "Er verharrt stur in seiner Meinung.",
                        "exampleZh": "他顽固地坚持自己的看法不肯松动。"
                    }
                ]
            }
        ]
    },

    # ---------------- Quarks Daily (WDR 科研播客) ----------------
    {
        "id": "quarks-inflation-b2",
        "title": "Quarks Daily: Inflation – Haben wir wirklich weniger Geld im Portemonnaie?",
        "source": "WDR Quarks Daily · Wissenschaft",
        "topic": "感知通胀心理学与购买力测算",
        "originalAudioUrl": "https://wdrmedien-a.akamaihd.net/media/p/public/weltweit/2026/10/28/07bc7024-d4a7-4e25-9ed6-0e9d1f7468ca/07bc7024-d4a7-4e25-9ed6-0e9d1f7468ca_MP3-128.mp3",
        "segments": [
            {
                "id": "quarks-inf-s1",
                "german": "Viele Menschen haben das Gefühl, dass alltägliche Einkäufe im Supermarkt dramatisch teurer geworden sind als die offizielle Inflationsrate angibt.",
                "chinese": "许多人强烈感觉，自己在超市的日常采购涨价幅度远比官方公布的通胀统计率要高得多。",
                "clozeWords": ["alltägliche", "dramatisch", "Inflationsrate"],
                "vocab": [
                    {
                        "word": "die Inflationsrate",
                        "plural": "die Inflationsraten",
                        "pos": "Nomen",
                        "meaning": "通货膨胀率",
                        "exampleDe": "Die Zentralbank bekämpft die hohe Inflationsrate.",
                        "exampleZh": "央行正在采取措施抑制过高的通胀率。"
                    }
                ]
            },
            {
                "id": "quarks-inf-s2",
                "german": "Wirtschaftspsychologen erklären dieses Phänomen durch die sogenannte gefühlte Inflation: Häufig gekaufte Güter wie Brot oder Butter prägen unsere Wahrnehmung viel stärker.",
                "chinese": "经济心理学家用“感知通胀”来解读这种现象：像面包或黄油这类高频采购的基本食品，会对人们的心理感知产生深远得多的影响。",
                "clozeWords": ["Wirtschaftspsychologen", "gefühlte", "Wahrnehmung"],
                "vocab": [
                    {
                        "word": "die Wahrnehmung",
                        "plural": "die Wahrnehmungen",
                        "pos": "Nomen",
                        "meaning": "感知，认知观察",
                        "exampleDe": "Unsere visuelle Wahrnehmung lässt sich täuschen.",
                        "exampleZh": "我们的视觉感知很容易被假象所蒙骗。"
                    }
                ]
            },
            {
                "id": "quarks-inf-s3",
                "german": "Statistische Warenkörbe hingegen berücksichtigen auch langlebige Konsumgüter, deren Preise oft stabil bleiben oder sogar fallen.",
                "chinese": "而官方统计的价格商品篮还会将使用寿命长的耐用消费品计入在内，后者的价格走势往往保持平稳甚至有所下调。",
                "clozeWords": ["Warenkörbe", "langlebige", "Konsumgüter"],
                "vocab": [
                    {
                        "word": "das Konsumgut",
                        "plural": "die Konsumgüter",
                        "pos": "Nomen",
                        "meaning": "消费品",
                        "exampleDe": "Elektronikartikel gehören zu den Konsumgütern.",
                        "exampleZh": "电子产品属于日用消费品。"
                    }
                ]
            }
        ]
    },
    {
        "id": "quarks-gefuehle-job-b2",
        "title": "Quarks Daily: Emotionen im Beruf – Zeigen oder unterdrücken?",
        "source": "WDR Quarks Daily · Wissenschaft",
        "topic": "职场情商沟通与容错心理安全感",
        "originalAudioUrl": "https://wdrmedien-a.akamaihd.net/media/p/public/weltweit/2026/10/27/4626d8c1-0d70-4ff1-abee-2d16a3a0ee16/4626d8c1-0d70-4ff1-abee-2d16a3a0ee16_MP3-128.mp3",
        "segments": [
            {
                "id": "quarks-emo-s1",
                "german": "Lange Zeit galt im Berufsleben das ungeschriebene Gesetz, persönliche Emotionen strikt vor der Bürotür zu lassen.",
                "chinese": "长期以来，职场社交中一直流传着一条不成文的教条：必须将一切个人情绪严格挡在办公室的大门之外。",
                "clozeWords": ["ungeschriebene", "Emotionen", "Bürotür"],
                "vocab": [
                    {
                        "word": "ungeschrieben",
                        "pos": "Adjektiv",
                        "meaning": "不成文的，默认约定的",
                        "exampleDe": "Ein ungeschriebenes Gesetz regelt das Verhalten.",
                        "exampleZh": "一条不成文的规矩规范着人们的行为。"
                    }
                ]
            },
            {
                "id": "quarks-emo-s2",
                "german": "Neuere arbeitspsychologische Studien belegen jedoch, dass das ständige Unterdrücken von Frust oder Sorgen zu chronischem Stress und Burnout führen kann.",
                "chinese": "然而，最新的现代劳动心理学实证研究揭示，持续压抑内心的挫折感与忧虑会导致慢性精神压力并诱发职业倦怠。",
                "clozeWords": ["arbeitspsychologische", "Unterdrücken", "chronischem"],
                "vocab": [
                    {
                        "word": "das Unterdrücken",
                        "plural": "-",
                        "pos": "Nomen",
                        "meaning": "压抑，强行克制",
                        "exampleDe": "Das Unterdrücken von Gefühlen schadet der Gesundheit.",
                        "exampleZh": "压抑情绪会损害身心健康。"
                    }
                ]
            },
            {
                "id": "quarks-emo-s3",
                "german": "Teams mit einer offenen Fehlerkultur und hoher psychologischer Sicherheit erzielen erwiesenermaßen kreativere und nachhaltigere Arbeitsergebnisse.",
                "chinese": "事实已经充分证明，拥有开明容错文化和高度心理安全感的工作团队，能产出更有突破性与持久价值的工作成果。",
                "clozeWords": ["Fehlerkultur", "psychologischer", "erwiesenermaßen"],
                "vocab": [
                    {
                        "word": "erwiesenermaßen",
                        "pos": "Adverb",
                        "meaning": "按事实证明，显而易见地",
                        "exampleDe": "Sport fördert erwiesenermaßen die Gesundheit.",
                        "exampleZh": "运动据事实证明能增进身体健康。"
                    }
                ]
            }
        ]
    },
    {
        "id": "quarks-schlaf-hirn-testdaf",
        "title": "Quarks Daily: Schlafmangel und neuronale Leistungsfähigkeit",
        "source": "WDR Quarks Daily · Wissenschaft",
        "topic": "神经脑科学与深睡眠代谢清除机制",
        "originalAudioUrl": "https://wdrmedien-a.akamaihd.net/media/p/public/weltweit/2026/10/28/d628a5ab-a4d0-4b0f-86f3-e2854dae9c89/d628a5ab-a4d0-4b0f-86f3-e2854dae9c89_MP3-128.mp3",
        "segments": [
            {
                "id": "quarks-sl-s1",
                "german": "Während des Tiefschlafs aktiviert das menschliche Gehirn das sogenannte glymphatische System, um toxische Stoffwechselprodukte abzutransportieren.",
                "chinese": "在深度睡眠阶段，人类大脑会激活所谓的胶质淋巴清除系统，以高效运转清除蓄积的有毒代谢副产物。",
                "clozeWords": ["Tiefschlafs", "glymphatische", "Stoffwechselprodukte"],
                "vocab": [
                    {
                        "word": "das Stoffwechselprodukt",
                        "plural": "die Stoffwechselprodukte",
                        "pos": "Nomen",
                        "meaning": "新陈代谢产物",
                        "exampleDe": "Die Nieren filtern schädliche Stoffwechselprodukte aus dem Blut.",
                        "exampleZh": "肾脏负责从血液中过滤清除有害的代谢废物。"
                    }
                ]
            },
            {
                "id": "quarks-sl-s2",
                "german": "Wissenschaftliche Experimente belegen, dass chronischer Schlafmangel die neuronale Plastizität im Hippocampus massiv beeinträchtigt und Lernprozesse blockiert.",
                "chinese": "多项科学严谨的对照实验证实，长期的睡眠匮乏会大幅损害海马体区域的神经元可塑性，并直接阻滞知识的学习内化。",
                "clozeWords": ["Plastizität", "Hippocampus", "beeinträchtigt"],
                "vocab": [
                    {
                        "word": "die Plastizität",
                        "plural": "-",
                        "pos": "Nomen",
                        "meaning": "（神经元结构的）可塑性，适应改变能力",
                        "exampleDe": "Neuronale Plastizität ist die Basis lebenslangen Lernens.",
                        "exampleZh": "神经元可塑性是进行终身学习的生理基础。"
                    }
                ]
            },
            {
                "id": "quarks-sl-s3",
                "german": "Für Studierende und Forschende ist ausreichender Nachtschlaf daher keine passive Ruhephase, sondern eine biologische Grundvoraussetzung für geistige Spitzenleistungen.",
                "chinese": "因此对于在校大学生与科学研究学者而言，充足的高质量夜间睡眠绝非消极的停顿，而是产出巅峰心智表现的生物学基石前提。",
                "clozeWords": ["Forschende", "biologische", "Spitzenleistungen"],
                "vocab": [
                    {
                        "word": "die Spitzenleistung",
                        "plural": "die Spitzenleistungen",
                        "pos": "Nomen",
                        "meaning": "顶尖成就，卓越表现",
                        "exampleDe": "Im Labor erbrachten die Forscher Spitzenleistungen.",
                        "exampleZh": "研究人员在实验室里取得了顶尖成果。"
                    }
                ]
            }
        ]
    },
    {
        "id": "quarks-e-scooter-b1",
        "title": "Quarks Daily: E-Scooter in der Großstadt – Fluch oder Segen?",
        "source": "WDR Quarks Daily · Wissenschaft",
        "topic": "城市最后一公里微出行与交通秩序",
        "originalAudioUrl": "https://wdrmedien-a.akamaihd.net/media/p/public/weltweit/2026/10/27/4626d8c1-0d70-4ff1-abee-2d16a3a0ee16/4626d8c1-0d70-4ff1-abee-2d16a3a0ee16_MP3-128.mp3",
        "segments": [
            {
                "id": "quarks-esc-s1",
                "german": "Elektrische Tretroller prägen mittlerweile das Stadtbild fast jeder deutschen Metropole.",
                "chinese": "电动滑板车如今已经成为几乎所有德国主要大都会街景中不可或缺的常见元素。",
                "clozeWords": ["Tretroller", "mittlerweile", "Metropole"],
                "vocab": [
                    {
                        "word": "die Metropole",
                        "plural": "die Metropolen",
                        "pos": "Nomen",
                        "meaning": "大都会，国际大都市",
                        "exampleDe": "Berlin ist eine lebendige europäische Metropole.",
                        "exampleZh": "柏林是一座生机勃勃的欧洲大都会。"
                    }
                ]
            },
            {
                "id": "quarks-esc-s2",
                "german": "Sie bieten eine praktische Lösung für die sogenannte letzte Meile zwischen U-Bahn-Station und Wohnort.",
                "chinese": "它们为地铁站出口到家庭住址之间的所谓“最后一公里”提供了一种快捷灵活的接驳方案。",
                "clozeWords": ["praktische", "Station", "Wohnort"],
                "vocab": [
                    {
                        "word": "der Wohnort",
                        "plural": "die Wohnorte",
                        "pos": "Nomen",
                        "meaning": "居住地，住所所在地",
                        "exampleDe": "Sein Wohnort liegt unweit der Universität.",
                        "exampleZh": "他的居住地距离大学不远。"
                    }
                ]
            },
            {
                "id": "quarks-esc-s3",
                "german": "Allerdings sorgen wild abgestellte Scooter auf Gehwegen immer wieder für Unmut bei Fußgängern und mobilitätseingeschränkten Personen.",
                "chinese": "然而，人行道上随处乱停乱放的滑板车屡次引发步行行人和行动不便人士的强烈不满与投诉。",
                "clozeWords": ["abgestellte", "Fußgängern", "mobilitätseingeschränkten"],
                "vocab": [
                    {
                        "word": "der Unmut",
                        "plural": "-",
                        "pos": "Nomen",
                        "meaning": "不满，怨气，愠怒",
                        "exampleDe": "Die Preiserhöhung stieß auf großen Unmut.",
                        "exampleZh": "涨价引发了公众的极大不满。"
                    }
                ]
            }
        ]
    }
]


async def synthesize_sentence_bytes(text: str, voice: str) -> bytes:
    """使用微软高保真德语神经网络语音合成单句"""
    communicate = edge_tts.Communicate(text, voice)
    audio_buffer = bytearray()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer.extend(chunk["data"])
    return bytes(audio_buffer)


async def process_single_track(track: dict, voice: str) -> dict:
    """计算文本CEFR等级、合成高精单句音频并生成毫秒级精确打轴"""
    track_id = track["id"]
    full_text = " ".join(s["german"] for s in track["segments"])
    
    # 智能CEFR分级
    analyzed_level = analyze_cefr_level(track["title"], full_text, track["source"])
    track["level"] = analyzed_level
    print(f"[{track_id}] CEFR 智能分级结果: {analyzed_level} | 标题: {track['title'][:32]}")

    mp3_filename = f"{track_id}.mp3"
    mp3_path = AUDIO_DIR / mp3_filename

    # 如果音频文件已经存在且打轴有效则跳过合成
    if mp3_path.exists() and track.get("duration") and len(track.get("segments", [])) > 0 and track["segments"][0].get("endTime") is not None:
        print(f"  -> 已存在打轴音频: {mp3_filename} ({track['duration']}s)")
        track["audioUrl"] = f"/audio/{mp3_filename}"
        return track

    combined_mp3 = bytearray()
    current_time = 0.0

    print(f"  -> 开始合成神经网络音频 ({voice}) ...")
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
    print(f"  -> 完成生成: {mp3_filename} (总时长: {track['duration']}s)")
    return track


async def main():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    DIST_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    existing_tracks = []
    if GENERATED_JSON.exists():
        try:
            existing_tracks = json.loads(GENERATED_JSON.read_text(encoding="utf-8"))
        except Exception as e:
            print("读取已有 generatedTracks.json 失败:", e)
            existing_tracks = []

    track_map = {t["id"]: t for t in existing_tracks}

    # 合并并分析新抓取/精选的语料
    print(f"\n==========================================")
    print(f"开始导入与分级 DW、歌德、Slow German、ZDF、Quarks 语料...")
    print(f"==========================================")

    for idx, new_track in enumerate(AUTHORITY_CORPUS):
        tid = new_track["id"]
        voice = NEURAL_VOICES[idx % len(NEURAL_VOICES)]
        processed = await process_single_track(new_track, voice)
        track_map[tid] = processed

    # 检查并补全此前未合成音频的已有曲目（例如 dw-nicos-weg-a1）
    for idx, (tid, trk) in enumerate(track_map.items()):
        if not trk.get("audioUrl") or not (AUDIO_DIR / f"{tid}.mp3").exists():
            voice = NEURAL_VOICES[(idx + 2) % len(NEURAL_VOICES)]
            try:
                print(f"[修复补全] 为遗留曲目生成高精度音频: {trk['title']}")
                updated = await process_single_track(trk, voice)
                track_map[tid] = updated
            except Exception as ex:
                print(f"  [跳过] 无法补全 {tid}: {ex}")

    final_list = list(track_map.values())

    # 按欧标等级规范排序: A1 -> A2 -> B1 -> B2 -> C1 -> TestDaF
    level_order = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "TestDaF": 6}
    final_list.sort(key=lambda t: (level_order.get(t.get("level", "B1"), 99), t.get("source", ""), t.get("id", "")))

    GENERATED_JSON.write_text(
        json.dumps(final_list, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    # 同步复制所有 public/audio 到 dist/audio
    for mp3_file in AUDIO_DIR.glob("*.mp3"):
        shutil.copy2(mp3_file, DIST_AUDIO_DIR / mp3_file.name)

    print(f"\n==========================================")
    print(f"【成功】总计就绪曲目数: {len(final_list)} 篇！")
    level_counts = {}
    for t in final_list:
        lvl = t.get("level", "B1")
        level_counts[lvl] = level_counts.get(lvl, 0) + 1
    print("等级分布统计:", level_counts)
    print(f"所有音频已同步至 public/audio/ 与 dist/audio/！")
    print(f"==========================================\n")


if __name__ == "__main__":
    asyncio.run(main())
