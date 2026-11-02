# -*- coding: utf-8 -*-
import os

RAW_GOETHE = r"D:\GermanCorpus\raw\goethe"
GOETHE_A1_FILE = os.path.join(RAW_GOETHE, "goethe_a1_hoeren.mp3")
GOETHE_A2_FILE = os.path.join(RAW_GOETHE, "goethe_a2_hoeren.mp3")

TRACKS_A1_A2 = [
    # =========================================================================
    # Goethe A1 (6 tracks)
    # =========================================================================
    {
        "id": "goethe-a1-pullover-01",
        "title": "Im Kaufhaus: Beratung beim Pulloverkauf",
        "level": "A1",
        "source": "Goethe-Institut",
        "topic": "Alltag & Einkaufen",
        "taskSection": "歌德 A1 · Teil 1 商场购物",
        "raw_file": GOETHE_A1_FILE,
        "ss": "127.3",
        "to": "147.2",
        "out_file": "goethe_a1_pullover.mp3",
        "segments": [
            {
                "id": "goethe-a1-pullover-01-s1",
                "startTime": 0.0,
                "endTime": 11.5,
                "german": "Entschuldigung, was kostet dieser Pullover jetzt? Da steht 30 Prozent billiger.",
                "chinese": "打扰一下，请问这件毛衣现在多少钱？上面写着便宜30%（打七折）。",
                "clozeWords": ["Entschuldigung", "kostet", "Pullover", "billiger"],
                "vocab": [
                    {"word": "die Entschuldigung", "pos": "Nomen", "meaning": "抱歉，打扰", "exampleDe": "Entschuldigung, darf ich kurz stören?", "exampleZh": "不好意思，我可以打扰一下吗？"},
                    {"word": "kosten", "pos": "Verb", "meaning": "花费，价值", "exampleDe": "Was kostet das Bahnticket?", "exampleZh": "这张火车票多少钱？"},
                    {"word": "der Pullover", "plural": "die Pullover", "pos": "Nomen", "meaning": "毛衣，套头衫", "exampleDe": "Dieser Pullover ist aus reiner Wolle.", "exampleZh": "这件毛衣是纯羊毛的。"},
                    {"word": "billig", "pos": "Adjektiv", "meaning": "便宜的", "exampleDe": "Im Ausverkauf sind die Kleider billiger.", "exampleZh": "大减价时衣服更便宜。"}
                ]
            },
            {
                "id": "goethe-a1-pullover-01-s2",
                "startTime": 11.5,
                "endTime": 16.5,
                "german": "Einen Moment bitte … neunzehnfünfundneunzig.",
                "chinese": "请稍等一下……十九块九毛五。",
                "clozeWords": ["Moment", "neunzehnfünfundneunzig"],
                "vocab": [
                    {"word": "der Moment", "plural": "die Momente", "pos": "Nomen", "meaning": "片刻，稍候", "exampleDe": "Warten Sie bitte einen kleinen Moment.", "exampleZh": "请稍等片刻。"}
                ]
            },
            {
                "id": "goethe-a1-pullover-01-s3",
                "startTime": 16.5,
                "endTime": 19.9,
                "german": "19,95 Euro? – Ja, Euro natürlich. – Hm, … ok, den nehme ich.",
                "chinese": "19.95欧元？——是的，当然是欧元。——嗯，……好的，我买了。",
                "clozeWords": ["Euro", "natürlich", "nehme"],
                "vocab": [
                    {"word": "der Euro", "pos": "Nomen", "meaning": "欧元", "exampleDe": "Das Buch kostet fünfzehn Euro.", "exampleZh": "这本书十五欧元。"},
                    {"word": "nehmen", "pos": "Verb", "meaning": "拿，买下", "exampleDe": "Ich nehme den blauen Mantel.", "exampleZh": "我买这件蓝色大衣。"}
                ]
            }
        ]
    },
    {
        "id": "goethe-a1-buero-02",
        "title": "Wegbeschreibung im Betriebsrat",
        "level": "A1",
        "source": "Goethe-Institut",
        "topic": "Alltag & Büro",
        "taskSection": "歌德 A1 · Teil 1 办公问路",
        "raw_file": GOETHE_A1_FILE,
        "ss": "50.4",
        "to": "74.5",
        "out_file": "goethe_a1_buero.mp3",
        "segments": [
            {
                "id": "goethe-a1-buero-02-s1",
                "startTime": 0.0,
                "endTime": 6.8,
                "german": "Ach, Verzeihung, wo finde ich Herrn Schneider vom Betriebsrat?",
                "chinese": "啊，不好意思，请问企业职工委员会的施耐德先生在哪里？",
                "clozeWords": ["Verzeihung", "finde", "Betriebsrat"],
                "vocab": [
                    {"word": "die Verzeihung", "pos": "Nomen", "meaning": "原谅，抱歉", "exampleDe": "Verzeihung, ich habe Sie nicht gesehen.", "exampleZh": "对不起，我没看见您。"},
                    {"word": "finden", "pos": "Verb", "meaning": "找到，寻得", "exampleDe": "Wo finde ich das Sekretariat?", "exampleZh": "请问秘书处在哪里？"},
                    {"word": "der Betriebsrat", "plural": "die Betriebsräte", "pos": "Nomen", "meaning": "企业工会，职工委员会", "exampleDe": "Der Betriebsrat hilft bei Problemen.", "exampleZh": "职工委员会在遇到问题时提供帮助。"}
                ]
            },
            {
                "id": "goethe-a1-buero-02-s2",
                "startTime": 6.8,
                "endTime": 12.8,
                "german": "Schneider. Warten Sie mal. Ich glaube, der ist in Zimmer Nummer 254.",
                "chinese": "施耐德。等一下。我想他是在254号房间。",
                "clozeWords": ["warten", "glaube", "Zimmer"],
                "vocab": [
                    {"word": "warten", "pos": "Verb", "meaning": "等待", "exampleDe": "Warten Sie bitte einen Augenblick.", "exampleZh": "请稍候片刻。"},
                    {"word": "glauben", "pos": "Verb", "meaning": "认为，相信", "exampleDe": "Ich glaube, der Zug kommt pünktlich.", "exampleZh": "我认为火车会准点到。"},
                    {"word": "das Zimmer", "plural": "die Zimmer", "pos": "Nomen", "meaning": "房间", "exampleDe": "Das Zimmer liegt im zweiten Stock.", "exampleZh": "房间在二楼。"}
                ]
            },
            {
                "id": "goethe-a1-buero-02-s3",
                "startTime": 12.8,
                "endTime": 24.1,
                "german": "Ja, stimmt, Zimmer 254. Das ist im zweiten Stock. Da können Sie den Aufzug hier nehmen. – Zweiter Stock, Zimmer 254. Okay, vielen Dank.",
                "chinese": "对，没错，254房间。在二楼。您可以坐这里的电梯。——二楼，254房间。好的，多谢。",
                "clozeWords": ["stimmt", "Stock", "Aufzug", "Dank"],
                "vocab": [
                    {"word": "stimmen", "pos": "Verb", "meaning": "正确，相符", "exampleDe": "Das stimmt genau.", "exampleZh": "完全正确。"},
                    {"word": "der Stock", "plural": "die Stockwerke", "pos": "Nomen", "meaning": "楼层", "exampleDe": "Mein Büro ist im ersten Stock.", "exampleZh": "我的办公室在一楼。"},
                    {"word": "der Aufzug", "plural": "die Aufzüge", "pos": "Nomen", "meaning": "电梯", "exampleDe": "Wir nehmen den Aufzug nach oben.", "exampleZh": "我们乘电梯上去。"}
                ]
            }
        ]
    },
    {
        "id": "goethe-a1-restaurant-03",
        "title": "Bestellung im Restaurant: Tagesgericht",
        "level": "A1",
        "source": "Goethe-Institut",
        "topic": "Alltag & Gastronomie",
        "taskSection": "歌德 A1 · Teil 1 餐厅点餐",
        "raw_file": GOETHE_A1_FILE,
        "ss": "250.2",
        "to": "276.0",
        "out_file": "goethe_a1_restaurant.mp3",
        "segments": [
            {
                "id": "goethe-a1-restaurant-03-s1",
                "startTime": 0.0,
                "endTime": 7.1,
                "german": "Was wünschen Sie bitte? – Ich hätte gern die Salatplatte und ein ...",
                "chinese": "请问您需要点什么？——我想点一份沙拉拼盘和一杯……",
                "clozeWords": ["wünschen", "Salatplatte"],
                "vocab": [
                    {"word": "wünschen", "pos": "Verb", "meaning": "希望，想要", "exampleDe": "Was wünschen Sie zu trinken?", "exampleZh": "您想喝点什么？"},
                    {"word": "die Salatplatte", "plural": "die Salatplatten", "pos": "Nomen", "meaning": "沙拉大拼盘", "exampleDe": "Die Salatplatte ist frisch zubereitet.", "exampleZh": "沙拉大拼盘是新鲜制作的。"}
                ]
            },
            {
                "id": "goethe-a1-restaurant-03-s2",
                "startTime": 7.1,
                "endTime": 13.5,
                "german": "Entschuldigung, die Salatplatte ist leider aus, aber die Bratwurst kann ich Ihnen empfehlen … ganz frisch heute.",
                "chinese": "不好意思，沙拉拼盘卖完了，不过我向您推荐烤香肠……今天非常新鲜。",
                "clozeWords": ["leider", "Bratwurst", "empfehlen", "frisch"],
                "vocab": [
                    {"word": "leider", "pos": "Adverb", "meaning": "遗憾地，可惜", "exampleDe": "Ich habe heute leider keine Zeit.", "exampleZh": "我很遗憾今天没有时间。"},
                    {"word": "die Bratwurst", "plural": "die Bratwürste", "pos": "Nomen", "meaning": "煎香肠，烤香肠", "exampleDe": "In Nürnberg isst man kleine Bratwürste.", "exampleZh": "在纽伦堡人们吃小烤肠。"},
                    {"word": "empfehlen", "pos": "Verb", "meaning": "推荐", "exampleDe": "Was können Sie uns empfehlen?", "exampleZh": "您能向我们推荐点什么？"}
                ]
            },
            {
                "id": "goethe-a1-restaurant-03-s3",
                "startTime": 13.5,
                "endTime": 25.8,
                "german": "Nein danke ... ich esse kein Fleisch. Gibt es etwas ohne Fleisch? – Ja ... nicht mehr viel: Fisch oder ... Pommes. – Fisch ... hm ... Tja, dann wohl die Pommes.",
                "chinese": "不，谢谢……我不吃肉。有不带肉的吗？——有……不多了：鱼或者……薯条。——鱼……嗯……好吧，那就要薯条。",
                "clozeWords": ["Fleisch", "Fisch", "Pommes"],
                "vocab": [
                    {"word": "das Fleisch", "pos": "Nomen", "meaning": "肉类", "exampleDe": "Er isst schon seit Jahren kein Fleisch mehr.", "exampleZh": "他已经好几年不吃肉了。"},
                    {"word": "die Pommes", "pos": "Nomen", "meaning": "炸薯条", "exampleDe": "Kinder essen besonders gerne Pommes.", "exampleZh": "小孩子们特别喜欢吃薯条。"}
                ]
            }
        ]
    },
    {
        "id": "goethe-a1-treppe-04",
        "title": "Im Kaufhaus: Weg zum Aufzug",
        "level": "A1",
        "source": "Goethe-Institut",
        "topic": "Alltag & Orientierung",
        "taskSection": "歌德 A1 · Teil 1 商场设施",
        "raw_file": GOETHE_A1_FILE,
        "ss": "382.5",
        "to": "399.5",
        "out_file": "goethe_a1_treppe.mp3",
        "segments": [
            {
                "id": "goethe-a1-treppe-04-s1",
                "startTime": 0.0,
                "endTime": 7.5,
                "german": "Ach, entschuldigen Sie, wie komme ich denn hier in den zweiten Stock?",
                "chinese": "啊，请问一下，我该怎么去这里的二楼呢？",
                "clozeWords": ["entschuldigen", "zweiten", "Stock"],
                "vocab": [
                    {"word": "entschuldigen", "pos": "Verb", "meaning": "原谅，抱歉", "exampleDe": "Entschuldigen Sie bitte die Verspätung.", "exampleZh": "抱歉迟到了。"},
                    {"word": "der Stock", "pos": "Nomen", "meaning": "楼层", "exampleDe": "Die Abteilung liegt im dritten Stock.", "exampleZh": "该部门位于三楼。"}
                ]
            },
            {
                "id": "goethe-a1-treppe-04-s2",
                "startTime": 7.5,
                "endTime": 10.3,
                "german": "Die Rolltreppe da vorn ist kaputt.",
                "chinese": "前面的自动扶梯坏了。",
                "clozeWords": ["Rolltreppe", "kaputt"],
                "vocab": [
                    {"word": "die Rolltreppe", "plural": "die Rolltreppen", "pos": "Nomen", "meaning": "自动扶梯", "exampleDe": "Die Rolltreppe fährt nach unten.", "exampleZh": "自动扶梯往下走。"},
                    {"word": "kaputt", "pos": "Adjektiv", "meaning": "损坏的，坏了", "exampleDe": "Mein Fahrrad ist leider kaputt.", "exampleZh": "我的自行车可惜坏了。"}
                ]
            },
            {
                "id": "goethe-a1-treppe-04-s3",
                "startTime": 10.3,
                "endTime": 17.0,
                "german": "Da gehen Sie hier rechts um die Ecke und nehmen den Aufzug. – Um die Ecke rechts. Danke.",
                "chinese": "您从这里往右转拐角走，坐电梯上去。——拐角右转，谢谢。",
                "clozeWords": ["rechts", "Ecke", "Aufzug", "Danke"],
                "vocab": [
                    {"word": "rechts", "pos": "Adverb", "meaning": "向右，右边", "exampleDe": "Biegen Sie nach der Kreuzung rechts ab.", "exampleZh": "在十字路口后向右拐。"},
                    {"word": "die Ecke", "plural": "die Ecken", "pos": "Nomen", "meaning": "拐角，角落", "exampleDe": "Die Apotheke liegt direkt um die Ecke.", "exampleZh": "药房就在拐角处。"}
                ]
            }
        ]
    },
    {
        "id": "goethe-a1-reisebus-05",
        "title": "Durchsage im Reisebus: Raststätte",
        "level": "A1",
        "source": "Goethe-Institut",
        "topic": "Reisen & Verkehr",
        "taskSection": "歌德 A1 · Teil 2 旅途广播",
        "raw_file": GOETHE_A1_FILE,
        "ss": "600.4",
        "to": "617.5",
        "out_file": "goethe_a1_reisebus.mp3",
        "segments": [
            {
                "id": "goethe-a1-reisebus-05-s1",
                "startTime": 0.0,
                "endTime": 4.5,
                "german": "Liebe Fahrgäste. Wir sind kurz vor Würzburg.",
                "chinese": "各位乘客，我们快到维尔茨堡了。",
                "clozeWords": ["Fahrgäste", "kurz"],
                "vocab": [
                    {"word": "der Fahrgast", "plural": "die Fahrgäste", "pos": "Nomen", "meaning": "乘客，旅客", "exampleDe": "Alle Fahrgäste müssen ein Ticket haben.", "exampleZh": "所有乘客都必须持有车票。"},
                    {"word": "kurz vor", "pos": "Phrase", "meaning": "就在……之前/临近", "exampleDe": "Wir sind kurz vor dem Ziel.", "exampleZh": "我们离目的地不远了。"}
                ]
            },
            {
                "id": "goethe-a1-reisebus-05-s2",
                "startTime": 4.5,
                "endTime": 10.5,
                "german": "Sicherlich haben Sie schon Hunger. An der nächsten Raststätte halten wir für eine Stunde.",
                "chinese": "大家想必已经饿了。我们在下一个高速服务区停靠一小时。",
                "clozeWords": ["Hunger", "Raststätte", "halten", "Stunde"],
                "vocab": [
                    {"word": "der Hunger", "pos": "Nomen", "meaning": "饥饿", "exampleDe": "Ich habe großen Hunger nach der Reise.", "exampleZh": "旅行后我感到非常饿。"},
                    {"word": "die Raststätte", "plural": "die Raststätten", "pos": "Nomen", "meaning": "高速公路服务区", "exampleDe": "An der Raststätte kann man tanken und essen.", "exampleZh": "在服务区可以加油和用餐。"},
                    {"word": "halten", "pos": "Verb", "meaning": "停靠，停止", "exampleDe": "Der Bus hält hier für zehn Minuten.", "exampleZh": "大巴在这里停靠十分钟。"}
                ]
            },
            {
                "id": "goethe-a1-reisebus-05-s3",
                "startTime": 10.5,
                "endTime": 17.1,
                "german": "Wir treffen uns wieder um halb eins am Bus, aber bitte pünktlich sein.",
                "chinese": "我们十二点半在旅游大巴集合，请大家务必准时。",
                "clozeWords": ["treffen", "halb", "Bus", "pünktlich"],
                "vocab": [
                    {"word": "treffen", "pos": "Verb", "meaning": "相聚，碰面", "exampleDe": "Wir treffen uns morgen am Hauptbahnhof.", "exampleZh": "我们明天在中央火车站碰面。"},
                    {"word": "pünktlich", "pos": "Adjektiv", "meaning": "准时的", "exampleDe": "Bitte kommen Sie ganz pünktlich zum Treffpunkt.", "exampleZh": "请务必准时到达集合地点。"}
                ]
            }
        ]
    },
    {
        "id": "goethe-a1-flughafen-06",
        "title": "Flughafendurchsage: Flug nach Warschau",
        "level": "A1",
        "source": "Goethe-Institut",
        "topic": "Reisen & Flughafen",
        "taskSection": "歌德 A1 · Teil 2 机场广播",
        "raw_file": GOETHE_A1_FILE,
        "ss": "683.8",
        "to": "700.0",
        "out_file": "goethe_a1_flughafen.mp3",
        "segments": [
            {
                "id": "goethe-a1-flughafen-06-s1",
                "startTime": 0.0,
                "endTime": 8.1,
                "german": "Herr Stefan Janda, gebucht auf dem Flug LH 737 nach Warschau, wird zum Schalter F7 gebeten.",
                "chinese": "乘坐汉莎航空LH 737航班飞往华沙的斯特凡·扬达先生，请前往F7柜台。",
                "clozeWords": ["gebucht", "Flug", "Schalter"],
                "vocab": [
                    {"word": "gebucht", "pos": "Partizip", "meaning": "已订票的", "exampleDe": "Ich bin auf dem Abendflug gebucht.", "exampleZh": "我订了晚班飞机。"},
                    {"word": "der Flug", "plural": "die Flüge", "pos": "Nomen", "meaning": "航班，飞行", "exampleDe": "Unser Flug hat leider Verspätung.", "exampleZh": "我们的航班遗憾延误了。"},
                    {"word": "der Schalter", "plural": "die Schalter", "pos": "Nomen", "meaning": "柜台，窗口", "exampleDe": "Geben Sie das Gepäck am Schalter ab.", "exampleZh": "请在柜台托运行李。"}
                ]
            },
            {
                "id": "goethe-a1-flughafen-06-s2",
                "startTime": 8.1,
                "endTime": 11.5,
                "german": "Der Flug wird in ein paar Minuten geschlossen.",
                "chinese": "该航班登机口将在几分钟内关闭。",
                "clozeWords": ["Minuten", "geschlossen"],
                "vocab": [
                    {"word": "die Minute", "plural": "die Minuten", "pos": "Nomen", "meaning": "分钟", "exampleDe": "Der Vortrag beginnt in fünf Minuten.", "exampleZh": "讲座五分钟后开始。"},
                    {"word": "schließen", "pos": "Verb", "meaning": "关闭", "exampleDe": "Das Gate wird pünktlich geschlossen.", "exampleZh": "登机口准时关闭。"}
                ]
            },
            {
                "id": "goethe-a1-flughafen-06-s3",
                "startTime": 11.5,
                "endTime": 16.2,
                "german": "Herr Janda, gebucht nach Warschau, bitte nach F7.",
                "chinese": "扬达先生，前往华沙的旅客，请立刻到F7柜台。",
                "clozeWords": ["Warschau", "bitte"],
                "vocab": [
                    {"word": "bitten", "pos": "Verb", "meaning": "请求", "exampleDe": "Darf ich Sie um Hilfe bitten?", "exampleZh": "我可以请您帮个忙吗？"}
                ]
            }
        ]
    },

    # =========================================================================
    # Goethe A2 (6 tracks)
    # =========================================================================
    {
        "id": "goethe-a2-olympia-01",
        "title": "Verkehrsinformation zur Olympiahalle",
        "level": "A2",
        "source": "Goethe-Institut",
        "topic": "Verkehr & Veranstaltungen",
        "taskSection": "歌德 A2 · Teil 1 场馆交通",
        "raw_file": GOETHE_A2_FILE,
        "ss": "80.2",
        "to": "96.5",
        "out_file": "goethe_a2_olympia.mp3",
        "segments": [
            {
                "id": "goethe-a2-olympia-01-s1",
                "startTime": 0.0,
                "endTime": 5.5,
                "german": "Eine Information für die Besucher des Basketballspiels heute in der Olympia-Halle:",
                "chinese": "一条给今天在奥林匹亚大厅观看篮球比赛的观众的通知：",
                "clozeWords": ["Information", "Besucher", "Basketballspiels"],
                "vocab": [
                    {"word": "die Information", "plural": "die Informationen", "pos": "Nomen", "meaning": "信息，通知", "exampleDe": "Haben Sie eine Information für Touristen?", "exampleZh": "您有给游客的信息吗？"},
                    {"word": "der Besucher", "plural": "die Besucher", "pos": "Nomen", "meaning": "参观者，观众", "exampleDe": "Tausende Besucher strömten ins Stadion.", "exampleZh": "成千上万的观众涌入体育场。"}
                ]
            },
            {
                "id": "goethe-a2-olympia-01-s2",
                "startTime": 5.5,
                "endTime": 10.6,
                "german": "Die Parkplätze in der Nähe sind schon besetzt.",
                "chinese": "附近的停车场已经满了。",
                "clozeWords": ["Parkplätze", "Nähe", "besetzt"],
                "vocab": [
                    {"word": "der Parkplatz", "plural": "die Parkplätze", "pos": "Nomen", "meaning": "停车位，停车场", "exampleDe": "Am Wochenende sind alle Parkplätze voll.", "exampleZh": "周末所有的停车位都满了。"},
                    {"word": "besetzt", "pos": "Adjektiv", "meaning": "被占用的，客满的", "exampleDe": "Ist dieser Sitzplatz noch frei oder besetzt?", "exampleZh": "这个座位是空的还是有人了？"}
                ]
            },
            {
                "id": "goethe-a2-olympia-01-s3",
                "startTime": 10.6,
                "endTime": 16.3,
                "german": "Im Parkhaus am Einkaufszentrum gibt es noch freie Plätze.",
                "chinese": "购物中心的停车库里还有空位。",
                "clozeWords": ["Parkhaus", "Einkaufszentrum", "freie", "Plätze"],
                "vocab": [
                    {"word": "das Parkhaus", "plural": "die Parkhäuser", "pos": "Nomen", "meaning": "停车楼，停车库", "exampleDe": "Im Parkhaus finden Sie sichere Stellplätze.", "exampleZh": "在停车楼里您可以找到安全的车位。"},
                    {"word": "das Einkaufszentrum", "plural": "die Einkaufszentren", "pos": "Nomen", "meaning": "购物中心", "exampleDe": "Das neue Einkaufszentrum hat viele Geschäfte.", "exampleZh": "新购物中心有许多商铺。"}
                ]
            }
        ]
    },
    {
        "id": "goethe-a2-bus-02",
        "title": "Kostenlose Busverbindung am Hauptbahnhof",
        "level": "A2",
        "source": "Goethe-Institut",
        "topic": "Verkehr & Mobilität",
        "taskSection": "歌德 A2 · Teil 1 接驳乘车",
        "raw_file": GOETHE_A2_FILE,
        "ss": "96.5",
        "to": "107.0",
        "out_file": "goethe_a2_bus.mp3",
        "segments": [
            {
                "id": "goethe-a2-bus-02-s1",
                "startTime": 0.0,
                "endTime": 3.2,
                "german": "Besucher von außerhalb sollten nicht mit dem Auto kommen.",
                "chinese": "外地来的访客请勿开车前往。",
                "clozeWords": ["Besucher", "außerhalb", "Auto"],
                "vocab": [
                    {"word": "außerhalb", "pos": "Präposition / Adverb", "meaning": "在……之外，外地", "exampleDe": "Er wohnt etwas außerhalb der Stadt.", "exampleZh": "他住在城市稍外围的地方。"}
                ]
            },
            {
                "id": "goethe-a2-bus-02-s2",
                "startTime": 3.2,
                "endTime": 5.0,
                "german": "Nehmen Sie die Bahn!",
                "chinese": "请乘坐轨道交通！",
                "clozeWords": ["Nehmen", "Bahn"],
                "vocab": [
                    {"word": "die Bahn", "plural": "die Bahnen", "pos": "Nomen", "meaning": "铁路，火车", "exampleDe": "Wir reisen am liebsten mit der Bahn.", "exampleZh": "我们最喜欢乘火车出行。"}
                ]
            },
            {
                "id": "goethe-a2-bus-02-s3",
                "startTime": 5.0,
                "endTime": 10.5,
                "german": "Vom Hauptbahnhof gibt es kostenlose Busse zur Olympia-Halle.",
                "chinese": "中央火车站提供前往奥林匹亚大厅的免费接驳大巴。",
                "clozeWords": ["Hauptbahnhof", "kostenlose", "Busse"],
                "vocab": [
                    {"word": "der Hauptbahnhof", "plural": "die Hauptbahnhöfe", "pos": "Nomen", "meaning": "中央火车站", "exampleDe": "Treffen wir uns am Hauptbahnhof?", "exampleZh": "我们在中央火车站碰头吗？"},
                    {"word": "kostenlos", "pos": "Adjektiv", "meaning": "免费的", "exampleDe": "WLAN ist im ganzen Hotel kostenlos.", "exampleZh": "整个酒店的无线网络都是免费的。"}
                ]
            }
        ]
    },
    {
        "id": "goethe-a2-anzug-03",
        "title": "Vorbereitung auf die Hochzeitsfeier",
        "level": "A2",
        "source": "Goethe-Institut",
        "topic": "Alltag & Feste",
        "taskSection": "歌德 A2 · Teil 1 日常待办",
        "raw_file": GOETHE_A2_FILE,
        "ss": "150.2",
        "to": "172.5",
        "out_file": "goethe_a2_anzug.mp3",
        "segments": [
            {
                "id": "goethe-a2-anzug-03-s1",
                "startTime": 0.0,
                "endTime": 6.0,
                "german": "Hallo Sabine. Denk bitte an meinen dunklen Anzug.",
                "chinese": "喂，萨宾娜。请别忘了我那套深色西装。",
                "clozeWords": ["Denk", "dunklen", "Anzug"],
                "vocab": [
                    {"word": "denken an", "pos": "Verb", "meaning": "想到，记得", "exampleDe": "Denk bitte an den Hausschlüssel!", "exampleZh": "请记着带房门钥匙！"},
                    {"word": "der Anzug", "plural": "die Anzüge", "pos": "Nomen", "meaning": "西装，套装", "exampleDe": "Zu feierlichen Anlässen trägt er einen Anzug.", "exampleZh": "隆重场合他总是穿西装。"}
                ]
            },
            {
                "id": "goethe-a2-anzug-03-s2",
                "startTime": 6.0,
                "endTime": 14.5,
                "german": "Du wolltest ihn doch aus der Reinigung abholen. Sonst weiß ich nicht, was ich bei Helenas Hochzeit morgen anziehen soll.",
                "chinese": "你之前说要去干洗店取的。否则明天海伦娜的婚礼我都不知道穿什么好。",
                "clozeWords": ["Reinigung", "abholen", "Hochzeit", "anziehen"],
                "vocab": [
                    {"word": "die Reinigung", "plural": "die Reinigungen", "pos": "Nomen", "meaning": "干洗店，清洁", "exampleDe": "Ich bringe das Hemd in die Reinigung.", "exampleZh": "我把衬衫送去干洗店。"},
                    {"word": "die Hochzeit", "plural": "die Hochzeiten", "pos": "Nomen", "meaning": "婚礼", "exampleDe": "Wir sind zu einer großen Hochzeit eingeladen.", "exampleZh": "我们受邀参加一场盛大的婚礼。"},
                    {"word": "anziehen", "pos": "Verb", "meaning": "穿上", "exampleDe": "Zieh dir eine warme Jacke an!", "exampleZh": "穿件暖和的外套！"}
                ]
            },
            {
                "id": "goethe-a2-anzug-03-s3",
                "startTime": 14.5,
                "endTime": 22.3,
                "german": "Das Geschenk hab‘ ich heute in der Mittagspause schon gekauft. Die Blumen holen wir ja erst morgen früh. Dank dir.",
                "chinese": "礼物我今天午休时已经买好了。花我们明天一早再去拿。谢谢你啦。",
                "clozeWords": ["Geschenk", "Mittagspause", "Blumen", "früh"],
                "vocab": [
                    {"word": "das Geschenk", "plural": "die Geschenke", "pos": "Nomen", "meaning": "礼物", "exampleDe": "Vielen Dank für das schöne Geschenk!", "exampleZh": "非常感谢这份精美的礼物！"},
                    {"word": "die Mittagspause", "plural": "die Mittagspausen", "pos": "Nomen", "meaning": "午休时间", "exampleDe": "In der Mittagspause gehe ich kurz spazieren.", "exampleZh": "午休时我去散一会儿步。"}
                ]
            }
        ]
    },
    {
        "id": "goethe-a2-wetter-04",
        "title": "Wetterbericht für Nord- und Süddeutschland",
        "level": "A2",
        "source": "Goethe-Institut",
        "topic": "Wetter & Natur",
        "taskSection": "歌德 A2 · Teil 1 天气预报",
        "raw_file": GOETHE_A2_FILE,
        "ss": "296.8",
        "to": "323.5",
        "out_file": "goethe_a2_wetter.mp3",
        "segments": [
            {
                "id": "goethe-a2-wetter-04-s1",
                "startTime": 0.0,
                "endTime": 7.0,
                "german": "Nun zum Wetter. Am Wochenende ist es im Norden windig und bewölkt.",
                "chinese": "现在播报天气。周末北部多风且多云。",
                "clozeWords": ["Wetter", "Wochenende", "Norden", "windig", "bewölkt"],
                "vocab": [
                    {"word": "das Wetter", "pos": "Nomen", "meaning": "天气", "exampleDe": "Wie wird das Wetter am Wochenende?", "exampleZh": "周末天气如何？"},
                    {"word": "windig", "pos": "Adjektiv", "meaning": "有风的，风大的", "exampleDe": "An der Nordsee ist es oft sehr windig.", "exampleZh": "在北海常常风很大。"},
                    {"word": "bewölkt", "pos": "Adjektiv", "meaning": "多云的，阴天的", "exampleDe": "Der Himmel ist heute stark bewölkt.", "exampleZh": "今天天空云层很厚。"}
                ]
            },
            {
                "id": "goethe-a2-wetter-04-s2",
                "startTime": 7.0,
                "endTime": 15.6,
                "german": "Es regnet bei maximal 17 Grad. Im Süden am Samstag sonnig und warm bis 25 Grad.",
                "chinese": "伴有降雨，最高气温17度。南部周六晴朗温暖，气温可达25度。",
                "clozeWords": ["regnet", "maximal", "Süden", "sonnig", "warm"],
                "vocab": [
                    {"word": "regnen", "pos": "Verb", "meaning": "下雨", "exampleDe": "Morgen soll es den ganzen Tag regnen.", "exampleZh": "明天据说会下一整天雨。"},
                    {"word": "sonnig", "pos": "Adjektiv", "meaning": "晴朗的，充满阳光的", "exampleDe": "Wir hatten eine wunderschöne sonnige Woche.", "exampleZh": "我们度过了非常美好晴朗的一周。"}
                ]
            },
            {
                "id": "goethe-a2-wetter-04-s3",
                "startTime": 15.6,
                "endTime": 26.7,
                "german": "Am Sonntag kommt das kalte Regenwetter dann auch nach Süddeutschland. Die Temperaturen fallen auch hier auf unter 15 Grad.",
                "chinese": "周日寒冷阴雨天气也将蔓延至德国南部。这里的气温也会降至15度以下。",
                "clozeWords": ["Regenwetter", "Süddeutschland", "Temperaturen", "fallen"],
                "vocab": [
                    {"word": "die Temperatur", "plural": "die Temperaturen", "pos": "Nomen", "meaning": "气温，温度", "exampleDe": "Die Temperaturen steigen am Nachmittag.", "exampleZh": "下午气温上升。"},
                    {"word": "fallen", "pos": "Verb", "meaning": "下降，跌落", "exampleDe": "Im Herbst fallen die Temperaturen rasch.", "exampleZh": "秋季气温迅速下降。"}
                ]
            }
        ]
    },
    {
        "id": "goethe-a2-reparatur-05",
        "title": "Mängelmeldung: Heizung defekt",
        "level": "A2",
        "source": "Goethe-Institut",
        "topic": "Wohnen & Reparaturen",
        "taskSection": "歌德 A2 · Teil 3 物业报修",
        "raw_file": GOETHE_A2_FILE,
        "ss": "818.5",
        "to": "842.5",
        "out_file": "goethe_a2_reparatur.mp3",
        "segments": [
            {
                "id": "goethe-a2-reparatur-05-s1",
                "startTime": 0.0,
                "endTime": 7.5,
                "german": "Hallo Herr Talas. Hier Miguel Alba aus Haus Nr. 9. Wir haben gestern schon wegen der Reparaturen telefoniert.",
                "chinese": "您好塔拉斯先生。我是9号楼的米格尔·阿尔巴。我们昨天为了维修的事通过电话。",
                "clozeWords": ["Reparaturen", "telefoniert"],
                "vocab": [
                    {"word": "die Reparatur", "plural": "die Reparaturen", "pos": "Nomen", "meaning": "修理，维修", "exampleDe": "Die Reparatur der Heizung dauerte zwei Stunden.", "exampleZh": "维修暖气花了两个小时。"},
                    {"word": "telefonieren", "pos": "Verb", "meaning": "通电话", "exampleDe": "Wir haben ausführlich über das Thema telefoniert.", "exampleZh": "我们通过电话详细探讨了该话题。"}
                ]
            },
            {
                "id": "goethe-a2-reparatur-05-s2",
                "startTime": 7.5,
                "endTime": 15.0,
                "german": "Ja. Der Mechaniker hat den Aufzug in Ihrem Haus gestern Abend noch repariert. Und die Lampe am Eingang geht auch wieder.",
                "chinese": "是的。机修工昨晚已经修好了你们楼的电梯。门口的灯也修好了。",
                "clozeWords": ["Mechaniker", "Aufzug", "repariert", "Lampe", "Eingang"],
                "vocab": [
                    {"word": "der Mechaniker", "plural": "die Mechaniker", "pos": "Nomen", "meaning": "机修工，技工", "exampleDe": "Der Mechaniker prüft alle Bauteile.", "exampleZh": "机修工检查了所有零部件。"},
                    {"word": "der Eingang", "plural": "die Eingänge", "pos": "Nomen", "meaning": "入口，大门口", "exampleDe": "Bitte warten Sie am Haupteingang.", "exampleZh": "请在正门入口处等候。"}
                ]
            },
            {
                "id": "goethe-a2-reparatur-05-s3",
                "startTime": 15.0,
                "endTime": 24.0,
                "german": "Ja, ja. Aber jetzt wird die Heizung in meiner Wohnung nicht mehr warm. Können Sie vorbeikommen und sich das mal ansehen?",
                "chinese": "对对。但我公寓里的暖气现在不热了。您能过来看看吗？",
                "clozeWords": ["Heizung", "Wohnung", "warm", "vorbeikommen"],
                "vocab": [
                    {"word": "die Heizung", "plural": "die Heizungen", "pos": "Nomen", "meaning": "暖气，暖气设备", "exampleDe": "Im Winter läuft die Heizung ununterbrochen.", "exampleZh": "冬天暖气一直开着。"},
                    {"word": "vorbeikommen", "pos": "Verb", "meaning": "顺道过来，拜访", "exampleDe": "Können Sie heute Nachmittag kurz vorbeikommen?", "exampleZh": "您今天下午能顺道过来一下吗？"}
                ]
            }
        ]
    },
    {
        "id": "goethe-a2-praxis-06",
        "title": "Terminvereinbarung Krankengymnastik",
        "level": "A2",
        "source": "Goethe-Institut",
        "topic": "Gesundheit & Termine",
        "taskSection": "歌德 A2 · Teil 3 诊所预约",
        "raw_file": GOETHE_A2_FILE,
        "ss": "862.0",
        "to": "895.0",
        "out_file": "goethe_a2_praxis.mp3",
        "segments": [
            {
                "id": "goethe-a2-praxis-06-s1",
                "startTime": 0.0,
                "endTime": 5.5,
                "german": "Guten Tag, hier ist Messner von der Arztpraxis Vollmer. – Ja? Guten Tag.",
                "chinese": "您好，我是福尔默诊所的梅斯纳。——在的，您好。",
                "clozeWords": ["Arztpraxis", "Guten", "Tag"],
                "vocab": [
                    {"word": "die Arztpraxis", "plural": "die Arztpraxen", "pos": "Nomen", "meaning": "医生诊所", "exampleDe": "Die Arztpraxis hat donnerstags geschlossen.", "exampleZh": "诊所周四不营业。"}
                ]
            },
            {
                "id": "goethe-a2-praxis-06-s2",
                "startTime": 5.5,
                "endTime": 15.0,
                "german": "Ich rufe an wegen Ihrer Krankengymnastik. Sie können nächste Woche Montag und Donnerstag um 16 Uhr kommen. – Ja, das passt.",
                "chinese": "我打电话是关于您的理疗康复训练。下周一和周四下午4点您可以过来。——好的，时间合适。",
                "clozeWords": ["Krankengymnastik", "Donnerstag", "passt"],
                "vocab": [
                    {"word": "die Krankengymnastik", "pos": "Nomen", "meaning": "理疗体操，康复运动", "exampleDe": "Nach der Knieoperation braucht er Krankengymnastik.", "exampleZh": "膝盖手术后他需要做物理理疗康复。"},
                    {"word": "passen", "pos": "Verb", "meaning": "合适，方便", "exampleDe": "Passt Ihnen der Termin am Mittwoch?", "exampleZh": "周三的预约时间对您合适吗？"}
                ]
            },
            {
                "id": "goethe-a2-praxis-06-s3",
                "startTime": 15.0,
                "endTime": 33.0,
                "german": "Sie müssen nicht an der Information warten. Gehen Sie direkt in den Sportraum. Und bitte vergessen Sie das Rezept vom Arzt und Ihre Sportkleidung nicht.",
                "chinese": "您不需要在服务台等待。直接去体操房即可。请不要忘记带医生的处方和您的运动服。",
                "clozeWords": ["Information", "Sportraum", "vergessen", "Rezept", "Sportkleidung"],
                "vocab": [
                    {"word": "das Rezept", "plural": "die Rezepte", "pos": "Nomen", "meaning": "处方，药方", "exampleDe": "Der Arzt stellte ein Rezept für die Therapie aus.", "exampleZh": "医生为理疗开具了处方。"},
                    {"word": "die Sportkleidung", "pos": "Nomen", "meaning": "运动服", "exampleDe": "Bringen Sie bitte bequeme Sportkleidung mit.", "exampleZh": "请携带舒适的运动服。"}
                ]
            }
        ]
    }
]
