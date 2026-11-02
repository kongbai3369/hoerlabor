import os
import subprocess
import json
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

RAW_GOETHE = r"D:\GermanCorpus\raw\goethe"
RAW_TESTDAF = r"D:\GermanCorpus\raw\testdaf"
OUT_DIR = r"D:\GermanCorpus\processed\tracks"
os.makedirs(OUT_DIR, exist_ok=True)

TRACK_DEFINITIONS = [
    # 1. Goethe A1 Pullover
    {
        "id": "goethe-a1-pullover-01",
        "title": "Im Kaufhaus: Beratung beim Pulloverkauf",
        "level": "A1",
        "source": "Goethe-Institut",
        "topic": "Alltag & Einkaufen",
        "raw_file": os.path.join(RAW_GOETHE, "goethe_a1_hoeren.mp3"),
        "ss": "195.9",
        "to": "218.0",
        "out_file": "goethe_a1_pullover.mp3",
        "segments": [
            {
                "id": "goethe-a1-pullover-01-s1",
                "startTime": 0.0,
                "endTime": 7.2,
                "german": "Entschuldigung, was kostet dieser Pullover jetzt?",
                "chinese": "打扰一下，请问这件毛衣现在多少钱？",
                "clozeWords": ["Entschuldigung", "kostet", "Pullover"],
                "vocab": [
                    {"word": "die Entschuldigung", "pos": "Nomen", "meaning": "抱歉，打扰", "exampleDe": "Entschuldigung, darf ich kurz stören?", "exampleZh": "不好意思，我可以打扰一下吗？"},
                    {"word": "kosten", "pos": "Verb", "meaning": "花费，价值", "exampleDe": "Was kostet das Bahnticket?", "exampleZh": "这张火车票多少钱？"},
                    {"word": "der Pullover", "plural": "die Pullover", "pos": "Nomen", "meaning": "毛衣，套头衫", "exampleDe": "Dieser Pullover ist aus reiner Wolle.", "exampleZh": "这件毛衣是纯羊毛的。"}
                ]
            },
            {
                "id": "goethe-a1-pullover-01-s2",
                "startTime": 7.2,
                "endTime": 13.5,
                "german": "Da steht 30 Prozent billiger.",
                "chinese": "上面写着打七折（降价30%）。",
                "clozeWords": ["Prozent", "billiger"],
                "vocab": [
                    {"word": "das Prozent", "plural": "die Prozente", "pos": "Nomen", "meaning": "百分比", "exampleDe": "Heute gibt es zwanzig Prozent Rabatt.", "exampleZh": "今天有八折优惠。"},
                    {"word": "billig", "pos": "Adjektiv", "meaning": "便宜的", "exampleDe": "Im Supermarkt sind die Äpfel billiger.", "exampleZh": "超市里的苹果更便宜。"}
                ]
            },
            {
                "id": "goethe-a1-pullover-01-s3",
                "startTime": 13.5,
                "endTime": 22.1,
                "german": "Einen Moment bitte, neunzehnfünfundneunzig Euro natürlich.",
                "chinese": "请稍候，自然是19.95欧元。",
                "clozeWords": ["Moment", "neunzehn", "Euro"],
                "vocab": [
                    {"word": "der Moment", "plural": "die Momente", "pos": "Nomen", "meaning": "片刻，稍候", "exampleDe": "Warten Sie bitte einen kleinen Moment.", "exampleZh": "请稍等片刻。"},
                    {"word": "der Euro", "pos": "Nomen", "meaning": "欧元", "exampleDe": "Das Buch kostet fünfzehn Euro.", "exampleZh": "这本书十五欧元。"}
                ]
            }
        ]
    },

    # 2. Goethe A1 Buero
    {
        "id": "goethe-a1-buero-02",
        "title": "Wegbeschreibung im Betriebsrat",
        "level": "A1",
        "source": "Goethe-Institut",
        "topic": "Alltag & Büro",
        "raw_file": os.path.join(RAW_GOETHE, "goethe_a1_hoeren.mp3"),
        "ss": "126.4",
        "to": "151.0",
        "out_file": "goethe_a1_buero.mp3",
        "segments": [
            {
                "id": "goethe-a1-buero-02-s1",
                "startTime": 0.0,
                "endTime": 7.5,
                "german": "Ach, Verzeihung, wo finde ich Herrn Schneider vom Betriebsrat?",
                "chinese": "啊，对不起，请问企业职工委员会的施耐德先生在哪里？",
                "clozeWords": ["Verzeihung", "finde", "Betriebsrat"],
                "vocab": [
                    {"word": "die Verzeihung", "pos": "Nomen", "meaning": "原谅，对不起", "exampleDe": "Verzeihung, ich habe Sie nicht verstanden.", "exampleZh": "对不起，我没听懂您的话。"},
                    {"word": "finden", "pos": "Verb", "meaning": "找到，发现", "exampleDe": "Ich kann meinen Schlüssel nicht finden.", "exampleZh": "我找不到我的钥匙了。"},
                    {"word": "der Betriebsrat", "plural": "die Betriebsräte", "pos": "Nomen", "meaning": "企业工会，职工委员会", "exampleDe": "Der Betriebsrat vertritt die Interessen der Angestellten.", "exampleZh": "职工委员会代表雇员的利益。"}
                ]
            },
            {
                "id": "goethe-a1-buero-02-s2",
                "startTime": 7.5,
                "endTime": 16.8,
                "german": "Schneider, warten Sie mal, ich glaube, der ist in Zimmer 254 im zweiten Stock.",
                "chinese": "施耐德，等一下，我想他是在二楼254房间。",
                "clozeWords": ["warten", "glaube", "Zimmer", "Stock"],
                "vocab": [
                    {"word": "warten", "pos": "Verb", "meaning": "等待", "exampleDe": "Wir warten vor dem Bahnhof auf dich.", "exampleZh": "我们在火车站前等你。"},
                    {"word": "das Zimmer", "plural": "die Zimmer", "pos": "Nomen", "meaning": "房间", "exampleDe": "Das Zimmer liegt im ruhigen Innenhof.", "exampleZh": "这个房间朝向安静的内院。"},
                    {"word": "der Stock", "plural": "die Stockwerke", "pos": "Nomen", "meaning": "楼层", "exampleDe": "Mein Büro befindet sich im dritten Stock.", "exampleZh": "我的办公室在三楼。"}
                ]
            },
            {
                "id": "goethe-a1-buero-02-s3",
                "startTime": 16.8,
                "endTime": 24.6,
                "german": "Da können Sie direkt den Aufzug hier nehmen.",
                "chinese": "您可以直接乘这里的电梯上去。",
                "clozeWords": ["direkt", "Aufzug", "nehmen"],
                "vocab": [
                    {"word": "direkt", "pos": "Adjektiv", "meaning": "直接的", "exampleDe": "Gibt es einen direkten Flug nach Frankfurt?", "exampleZh": "有直飞法兰克福的航班吗？"},
                    {"word": "der Aufzug", "plural": "die Aufzüge", "pos": "Nomen", "meaning": "电梯", "exampleDe": "Nehmen Sie bitte den Aufzug nach oben.", "exampleZh": "请乘电梯上楼。"},
                    {"word": "nehmen", "pos": "Verb", "meaning": "乘坐，拿取", "exampleDe": "Wir nehmen jeden Morgen die U-Bahn.", "exampleZh": "我们每天早晨坐地铁。"}
                ]
            }
        ]
    },

    # 3. Goethe A2 Olympia
    {
        "id": "goethe-a2-olympia-01",
        "title": "Verkehrsinformation zur Olympiahalle",
        "level": "A2",
        "source": "Goethe-Institut",
        "topic": "Reise & Verkehr",
        "raw_file": os.path.join(RAW_GOETHE, "goethe_a2_hoeren.mp3"),
        "ss": "81.2",
        "to": "104.3",
        "out_file": "goethe_a2_olympia.mp3",
        "segments": [
            {
                "id": "goethe-a2-olympia-01-s1",
                "startTime": 0.0,
                "endTime": 6.8,
                "german": "Eine Information für die Besucher des Basketballspiels heute in der Olympiahalle.",
                "chinese": "为今天在奥林匹克体育馆观看篮球比赛的观众播报一条通知。",
                "clozeWords": ["Information", "Besucher", "Olympiahalle"],
                "vocab": [
                    {"word": "die Information", "plural": "die Informationen", "pos": "Nomen", "meaning": "信息，通知", "exampleDe": "Weitere Informationen finden Sie online.", "exampleZh": "更多信息请在线查阅。"},
                    {"word": "der Besucher", "plural": "die Besucher", "pos": "Nomen", "meaning": "访问者，观众", "exampleDe": "Viele Besucher kamen zur Ausstellung.", "exampleZh": "许多观众来看展览。"},
                    {"word": "die Halle", "plural": "die Hallen", "pos": "Nomen", "meaning": "大厅，场馆", "exampleDe": "Die Sporthalle öffnet um acht Uhr.", "exampleZh": "体育馆早上八点开门。"}
                ]
            },
            {
                "id": "goethe-a2-olympia-01-s2",
                "startTime": 6.8,
                "endTime": 14.5,
                "german": "Die Parkplätze in der Nähe sind schon besetzt, aber im Parkhaus gibt es noch freie Plätze.",
                "chinese": "附近的停车位已经停满，但在购物中心的室内停车场仍有空位。",
                "clozeWords": ["Parkplätze", "besetzt", "Parkhaus", "freie"],
                "vocab": [
                    {"word": "der Parkplatz", "plural": "die Parkplätze", "pos": "Nomen", "meaning": "停车位", "exampleDe": "Auf dem Parkplatz war kein Platz mehr frei.", "exampleZh": "停车场已经没有空位了。"},
                    {"word": "besetzt", "pos": "Adjektiv", "meaning": "占用的，已满的", "exampleDe": "Dieser Platz im Zug ist leider schon besetzt.", "exampleZh": "火车上的这个座位已经有人坐了。"},
                    {"word": "das Parkhaus", "plural": "die Parkhäuser", "pos": "Nomen", "meaning": "室内停车场", "exampleDe": "Das Parkhaus ist rund um die Uhr geöffnet.", "exampleZh": "该室内停车场全天24小时开放。"}
                ]
            },
            {
                "id": "goethe-a2-olympia-01-s3",
                "startTime": 14.5,
                "endTime": 23.1,
                "german": "Besucher von außerhalb sollten nicht mit dem Auto kommen, sondern die Bahn nehmen.",
                "chinese": "外地来的观众请尽量不要开车前来，请乘坐火车/城铁。",
                "clozeWords": ["außerhalb", "Auto", "Bahn"],
                "vocab": [
                    {"word": "außerhalb", "pos": "Präposition", "meaning": "在……之外", "exampleDe": "Das Hotel liegt etwas außerhalb des Stadtzentrums.", "exampleZh": "这家酒店位于市中心外围一点。"},
                    {"word": "das Auto", "plural": "die Autos", "pos": "Nomen", "meaning": "汽车", "exampleDe": "Er fährt jeden Tag mit dem Auto zur Arbeit.", "exampleZh": "他每天开车去上班。"},
                    {"word": "die Bahn", "plural": "die Bahnen", "pos": "Nomen", "meaning": "铁路，火车", "exampleDe": "Die Deutsche Bahn bietet günstige Spartickets an.", "exampleZh": "德国铁路提供优惠的特价票。"}
                ]
            }
        ]
    },

    # 4. Goethe A2 Bus
    {
        "id": "goethe-a2-bus-02",
        "title": "Kostenlose Busverbindung am Hauptbahnhof",
        "level": "A2",
        "source": "Goethe-Institut",
        "topic": "Alltag & Unterwegs",
        "raw_file": os.path.join(RAW_GOETHE, "goethe_a2_hoeren.mp3"),
        "ss": "107.4",
        "to": "131.0",
        "out_file": "goethe_a2_bus.mp3",
        "segments": [
            {
                "id": "goethe-a2-bus-02-s1",
                "startTime": 0.0,
                "endTime": 7.8,
                "german": "Vom Hauptbahnhof gibt es heute zusätzliche Pendelbusse für Sportfans.",
                "chinese": "今天从中央火车站开行专门面向体育迷的增开穿梭巴士。",
                "clozeWords": ["Hauptbahnhof", "zusätzliche", "Pendelbusse"],
                "vocab": [
                    {"word": "der Hauptbahnhof", "plural": "die Hauptbahnhöfe", "pos": "Nomen", "meaning": "中央火车站", "exampleDe": "Der Zug kommt pünktlich am Hauptbahnhof an.", "exampleZh": "火车准点到达中央火车站。"},
                    {"word": "zusätzlich", "pos": "Adjektiv", "meaning": "额外的，附加的", "exampleDe": "Für den Gepäcktransport fallen keine zusätzlichen Kosten an.", "exampleZh": "行李托运不产生额外费用。"},
                    {"word": "der Bus", "plural": "die Busse", "pos": "Nomen", "meaning": "公交车，大巴", "exampleDe": "Der Bus fährt alle zehn Minuten ab.", "exampleZh": "公共汽车每十分钟发出一班。"}
                ]
            },
            {
                "id": "goethe-a2-bus-02-s2",
                "startTime": 7.8,
                "endTime": 15.2,
                "german": "Diese Busse bringen Sie direkt und ohne Zwischenstopp zur Arena.",
                "chinese": "这些巴士将直接、中途不停站地将您送抵比赛场馆。",
                "clozeWords": ["bringen", "Zwischenstopp", "Arena"],
                "vocab": [
                    {"word": "bringen", "pos": "Verb", "meaning": "运送，带来", "exampleDe": "Können Sie mich zum Flughafen bringen?", "exampleZh": "您能送我去机场吗？"},
                    {"word": "der Zwischenstopp", "plural": "die Zwischenstopps", "pos": "Nomen", "meaning": "中途停留，中转站", "exampleDe": "Der Expresszug fährt ohne Zwischenstopp nach Berlin.", "exampleZh": "这趟特快列车中途不停直达柏林。"}
                ]
            },
            {
                "id": "goethe-a2-bus-02-s3",
                "startTime": 15.2,
                "endTime": 23.6,
                "german": "Bitte halten Sie Ihre Eintrittskarte beim Einsteigen bereit.",
                "chinese": "上车时请提前准备好您的入场门票。",
                "clozeWords": ["Eintrittskarte", "Einsteigen", "bereit"],
                "vocab": [
                    {"word": "die Eintrittskarte", "plural": "die Eintrittskarten", "pos": "Nomen", "meaning": "门票，入场券", "exampleDe": "Die Eintrittskarten sind bereits ausverkauft.", "exampleZh": "门票已经售罄。"},
                    {"word": "einsteigen", "pos": "Verb", "meaning": "上车", "exampleDe": "Bitte zügig einsteigen, die Türen schließen automatisch.", "exampleZh": "请迅速上车，车门自动关闭。"},
                    {"word": "bereit", "pos": "Adjektiv", "meaning": "准备就绪的", "exampleDe": "Wir sind bereit für die Abreise.", "exampleZh": "我们已经准备好出发了。"}
                ]
            }
        ]
    },

    # 5. Goethe B1 Urlaub
    {
        "id": "goethe-b1-urlaub-01",
        "title": "Urlaubsplanung und günstige Flüge nach Sizilien",
        "level": "B1",
        "source": "Goethe-Institut",
        "topic": "Reise & Freizeit",
        "raw_file": os.path.join(RAW_GOETHE, "goethe_b1_hoeren.mp3"),
        "ss": "45.3",
        "to": "73.5",
        "out_file": "goethe_b1_urlaub.mp3",
        "segments": [
            {
                "id": "goethe-b1-urlaub-01-s1",
                "startTime": 0.0,
                "endTime": 8.5,
                "german": "Hallo Jan, hier ist Frank, wir wollten doch im Sommer eine Woche ans Meer fahren.",
                "chinese": "你好扬，我是弗兰克，咱们之前不是说好夏天去海边度一周假吗？",
                "clozeWords": ["Sommer", "Woche", "Meer", "fahren"],
                "vocab": [
                    {"word": "der Sommer", "plural": "die Sommer", "pos": "Nomen", "meaning": "夏天", "exampleDe": "Im Sommer reisen viele Touristen an die Ostsee.", "exampleZh": "夏天许多游客去波罗的海旅行。"},
                    {"word": "das Meer", "plural": "die Meere", "pos": "Nomen", "meaning": "大海", "exampleDe": "Wir haben ein schönes Zimmer mit Blick aufs Meer.", "exampleZh": "我们订了一间带海景的漂亮房间。"},
                    {"word": "fahren", "pos": "Verb", "meaning": "行驶，出行", "exampleDe": "Am Wochenende fahren wir zu meinen Großeltern.", "exampleZh": "周末我们开车去看望我的祖父母。"}
                ]
            },
            {
                "id": "goethe-b1-urlaub-01-s2",
                "startTime": 8.5,
                "endTime": 17.2,
                "german": "Ich bin gerade im Internet: im Juni gibt es noch günstige Flüge nach Sizilien.",
                "chinese": "我正在上网看：6月份去西西里岛还有特价机票。",
                "clozeWords": ["Internet", "Juni", "günstige", "Flüge"],
                "vocab": [
                    {"word": "das Internet", "pos": "Nomen", "meaning": "互联网", "exampleDe": "Ich habe die Reiseunterlagen im Internet gebucht.", "exampleZh": "我在网上预订了旅行资料。"},
                    {"word": "günstig", "pos": "Adjektiv", "meaning": "实惠的，价格划算的", "exampleDe": "Das Hotel bietet sehr günstige Übernachtungspreise.", "exampleZh": "这家酒店提供非常实惠的住宿价格。"},
                    {"word": "der Flug", "plural": "die Flüge", "pos": "Nomen", "meaning": "航班", "exampleDe": "Der Flug nach Rom dauert zwei Stunden.", "exampleZh": "飞往罗马的航班飞行两小时。"}
                ]
            },
            {
                "id": "goethe-b1-urlaub-01-s3",
                "startTime": 17.2,
                "endTime": 28.2,
                "german": "Die Übernachtung müssen wir noch klären, meine Tante wohnt dort oder wir gehen campen.",
                "chinese": "住宿问题咱们还得商量一下，我姑姑住在那里，或者咱们去露营也行。",
                "clozeWords": ["Übernachtung", "klären", "Tante", "campen"],
                "vocab": [
                    {"word": "die Übernachtung", "plural": "die Übernachtungen", "pos": "Nomen", "meaning": "过夜，住宿", "exampleDe": "Die Übernachtung im Hotel beinhaltet Frühstück.", "exampleZh": "酒店住宿包含早餐。"},
                    {"word": "klären", "pos": "Verb", "meaning": "澄清，解决，商定", "exampleDe": "Wir müssen diese dringende Frage bald klären.", "exampleZh": "我们必须尽快商定这个紧迫的问题。"},
                    {"word": "campen", "pos": "Verb", "meaning": "露营，露宿野外", "exampleDe": "Im Nationalpark darf man nur an ausgewiesenen Plätzen campen.", "exampleZh": "在国家公园里只能在指定地点露营。"}
                ]
            }
        ]
    },

    # 6. Goethe B1 Praxis
    {
        "id": "goethe-b1-praxis-02",
        "title": "Terminvereinbarung in der Arztpraxis",
        "level": "B1",
        "source": "Goethe-Institut",
        "topic": "Gesundheit & Alltag",
        "raw_file": os.path.join(RAW_GOETHE, "goethe_b1_hoeren.mp3"),
        "ss": "148.1",
        "to": "170.2",
        "out_file": "goethe_b1_praxis.mp3",
        "segments": [
            {
                "id": "goethe-b1-praxis-02-s1",
                "startTime": 0.0,
                "endTime": 7.0,
                "german": "Hallo Frau Stein, hier ist die Praxis Dr. Becker, es geht um Ihre Grippe-Impfung.",
                "chinese": "您好施泰因女士，这里是贝克尔医生诊所，想跟您沟通流感疫苗接种的事情。",
                "clozeWords": ["Praxis", "Grippe-Impfung"],
                "vocab": [
                    {"word": "die Praxis", "plural": "die Praxen", "pos": "Nomen", "meaning": "诊所", "exampleDe": "Die Praxis bleibt am Mittwochnachmittag geschlossen.", "exampleZh": "诊所周三下午关闭。"},
                    {"word": "die Impfung", "plural": "die Impfungen", "pos": "Nomen", "meaning": "疫苗接种", "exampleDe": "Der Arzt empfiehlt eine jährliche Grippe-Impfung.", "exampleZh": "医生建议每年接种一次流感疫苗。"}
                ]
            },
            {
                "id": "goethe-b1-praxis-02-s2",
                "startTime": 7.0,
                "endTime": 15.0,
                "german": "Frau Dr. Becker muss zu einer Operation, könnten Sie vielleicht am Freitag um 14 Uhr kommen?",
                "chinese": "贝克尔医生需要去做一台手术，您看能不能改在周五下午14点过来？",
                "clozeWords": ["Operation", "Freitag", "kommen"],
                "vocab": [
                    {"word": "die Operation", "plural": "die Operationen", "pos": "Nomen", "meaning": "手术", "exampleDe": "Die Operation verlief ohne Komplikationen.", "exampleZh": "手术进行顺利，没有并发症。"},
                    {"word": "der Freitag", "pos": "Nomen", "meaning": "星期五", "exampleDe": "Am Freitag treffen wir uns im Labor.", "exampleZh": "星期五我们在实验室碰头。"}
                ]
            },
            {
                "id": "goethe-b1-praxis-02-s3",
                "startTime": 15.0,
                "endTime": 22.1,
                "german": "Ach, und Ihre Krankenversichertenkarte ist bei uns, die haben Sie letztes Mal vergessen.",
                "chinese": "啊，还有您的医保卡在我们这里，您上次落在这儿了。",
                "clozeWords": ["Krankenversichertenkarte", "letztes", "vergessen"],
                "vocab": [
                    {"word": "die Karte", "plural": "die Karten", "pos": "Nomen", "meaning": "卡片，医保卡", "exampleDe": "Bitte legen Sie beim Empfang Ihre Versichertenkarte vor.", "exampleZh": "在前台请出示您的医保卡。"},
                    {"word": "vergessen", "pos": "Verb", "meaning": "忘记，遗忘", "exampleDe": "Ich habe meinen Regenschirm im Bus vergessen.", "exampleZh": "我把雨伞忘在公交车上了。"}
                ]
            }
        ]
    },

    # 7. Goethe B1 Bewerbung
    {
        "id": "goethe-b1-bewerbung-03",
        "title": "Bewerbungsunterlagen bei der Versicherung",
        "level": "B1",
        "source": "Goethe-Institut",
        "topic": "Beruf & Karriere",
        "raw_file": os.path.join(RAW_GOETHE, "goethe_b1_hoeren.mp3"),
        "ss": "246.7",
        "to": "275.4",
        "out_file": "goethe_b1_bewerbung.mp3",
        "segments": [
            {
                "id": "goethe-b1-bewerbung-03-s1",
                "startTime": 0.0,
                "endTime": 9.2,
                "german": "Hallo Frau Brahms, Ulf Thomas hier von der HGB-Versicherung bezüglich Ihrer Bewerbung.",
                "chinese": "您好布拉姆斯女士，我是HGB保险公司的乌尔夫·托马斯，关于您的求职申请打来的。",
                "clozeWords": ["Versicherung", "bezüglich", "Bewerbung"],
                "vocab": [
                    {"word": "die Versicherung", "plural": "die Versicherungen", "pos": "Nomen", "meaning": "保险，保险公司", "exampleDe": "Haben Sie eine private Haftpflichtversicherung?", "exampleZh": "您有私人第三方责任险吗？"},
                    {"word": "die Bewerbung", "plural": "die Bewerbungen", "pos": "Nomen", "meaning": "求职申请", "exampleDe": "Ihre Bewerbung hat uns sofort überzeugt.", "exampleZh": "您的求职信立刻打动了我们。"}
                ]
            },
            {
                "id": "goethe-b1-bewerbung-03-s2",
                "startTime": 9.2,
                "endTime": 18.5,
                "german": "Sie haben sich als Verkaufsleiterin beworben, doch leider fehlen in Ihren Unterlagen zwei Zeugnisse.",
                "chinese": "您应聘的是销售主管一职，遗憾的是您的资料中还缺少两份证明材料。",
                "clozeWords": ["Verkaufsleiterin", "fehlen", "Unterlagen", "Zeugnisse"],
                "vocab": [
                    {"word": "fehlen", "pos": "Verb", "meaning": "缺少，缺席", "exampleDe": "Uns fehlen noch wichtige Dokumente für den Vertrag.", "exampleZh": "我们签署合同还缺少几份关键文件。"},
                    {"word": "die Unterlagen", "pos": "Nomen", "meaning": "证明材料，档案", "exampleDe": "Reichen Sie bitte alle Unterlagen fristgerecht ein.", "exampleZh": "请按时提交所有申请材料。"},
                    {"word": "das Zeugnis", "plural": "die Zeugnisse", "pos": "Nomen", "meaning": "证书，成绩单", "exampleDe": "Das Arbeitszeugnis bescheinigt hervorragende Leistungen.", "exampleZh": "工作鉴定证明了出色的工作业绩。"}
                ]
            },
            {
                "id": "goethe-b1-bewerbung-03-s3",
                "startTime": 18.5,
                "endTime": 28.7,
                "german": "Es geht um die Zertifikate für die besuchten Computer- und Englischkurse.",
                "chinese": "涉及的是您所参加的计算机培训课程与英语研修课程的结业证书。",
                "clozeWords": ["Zertifikate", "besuchten", "Kurse"],
                "vocab": [
                    {"word": "das Zertifikat", "plural": "die Zertifikate", "pos": "Nomen", "meaning": "证书，资格证明", "exampleDe": "Das Sprachzertifikat ist international anerkannt.", "exampleZh": "该语言证书在全球范围内获得认可。"},
                    {"word": "der Kurs", "plural": "die Kurse", "pos": "Nomen", "meaning": "课程，培训班", "exampleDe": "Sie belegt einen Fortgeschrittenenkurs für Datenanalyse.", "exampleZh": "她报名参加了一个高级数据分析课程。"}
                ]
            }
        ]
    },

    # 8. Goethe B2 Ferienprogramm
    {
        "id": "goethe-b2-ferien-01",
        "title": "Anmeldung zum städtischen Ferienprogramm",
        "level": "B2",
        "source": "Goethe-Institut",
        "topic": "Kultur & Gesellschaft",
        "raw_file": os.path.join(RAW_GOETHE, "goethe_b2_hoeren.mp3"),
        "ss": "94.0",
        "to": "128.0",
        "out_file": "goethe_b2_ferien.mp3",
        "segments": [
            {
                "id": "goethe-b2-ferien-01-s1",
                "startTime": 0.0,
                "endTime": 10.5,
                "german": "Ich wollte mich nach dem Ferienprogramm erkundigen, ab wann kann man sich denn anmelden?",
                "chinese": "我想咨询一下假期特色活动项目，请问从什么时候开始可以报名？",
                "clozeWords": ["Ferienprogramm", "erkundigen", "anmelden"],
                "vocab": [
                    {"word": "das Ferienprogramm", "plural": "die Ferienprogramme", "pos": "Nomen", "meaning": "假期活动项目", "exampleDe": "Die Stadt bietet ein spannendes Ferienprogramm für Jugendliche.", "exampleZh": "市政府为青少年提供了丰富的假期活动。"},
                    {"word": "sich erkundigen", "pos": "Verb", "meaning": "打听，咨询", "exampleDe": "Ich möchte mich nach den freien Stellen erkundigen.", "exampleZh": "我想打听一下空缺职位的情况。"},
                    {"word": "sich anmelden", "pos": "Verb", "meaning": "报名，登记", "exampleDe": "Sie müssen sich bis Freitag für die Prüfung anmelden.", "exampleZh": "您必须在周五之前报名参加考试。"}
                ]
            },
            {
                "id": "goethe-b2-ferien-01-s2",
                "startTime": 10.5,
                "endTime": 21.8,
                "german": "Wie immer ab dem ersten Juni, das gesamte Programm steht ab nächster Woche im Internet.",
                "chinese": "同往常一样从六月一日起开始，全部项目内容下周起公布在官网上。",
                "clozeWords": ["gesamte", "Programm", "nächster", "Woche"],
                "vocab": [
                    {"word": "gesamt", "pos": "Adjektiv", "meaning": "整个的，全部的", "exampleDe": "Der gesamte Plan wurde vom Ausschuss genehmigt.", "exampleZh": "整个方案已获得委员会的批准。"},
                    {"word": "das Programm", "plural": "die Programme", "pos": "Nomen", "meaning": "程序，日程，项目", "exampleDe": "Das Programm der Konferenz ist sehr abwechslungsreich.", "exampleZh": "会议日程非常丰富多样。"}
                ]
            },
            {
                "id": "goethe-b2-ferien-01-s3",
                "startTime": 21.8,
                "endTime": 34.0,
                "german": "Für die kostenlosen Angebote genügt das Internet, für kostenpflichtige Kurse müssen Sie sich persönlich anmelden.",
                "chinese": "免费项目在网上即可办理，而收费课程则必须由本人亲自前来前台登记。",
                "clozeWords": ["kostenlosen", "genügt", "kostenpflichtige", "persönlich"],
                "vocab": [
                    {"word": "kostenlos", "pos": "Adjektiv", "meaning": "免费的", "exampleDe": "Die Teilnahme am Workshop ist kostenlos.", "exampleZh": "参加工作坊是免费的。"},
                    {"word": "genügen", "pos": "Verb", "meaning": "足够，满足", "exampleDe": "Für den Antrag genügt eine einfache Kopie.", "exampleZh": "申请只需提供普通复印件即可。"},
                    {"word": "kostenpflichtig", "pos": "Adjektiv", "meaning": "收费的，需付费的", "exampleDe": "Der Download der Fachartikel ist kostenpflichtig.", "exampleZh": "下载这些专业文章是收费的。"},
                    {"word": "persönlich", "pos": "Adjektiv", "meaning": "亲身，本人的", "exampleDe": "Eine persönliche Unterschrift ist zwingend erforderlich.", "exampleZh": "必须本人亲笔签名。"}
                ]
            }
        ]
    },

    # 9. Goethe B2 Praktikum
    {
        "id": "goethe-b2-praktikum-02",
        "title": "Erfahrungsbericht: Praktikum in einer Anwaltskanzlei",
        "level": "B2",
        "source": "Goethe-Institut",
        "topic": "Beruf & Karriere",
        "raw_file": os.path.join(RAW_GOETHE, "goethe_b2_hoeren.mp3"),
        "ss": "157.5",
        "to": "189.5",
        "out_file": "goethe_b2_praktikum.mp3",
        "segments": [
            {
                "id": "goethe-b2-praktikum-02-s1",
                "startTime": 0.0,
                "endTime": 10.2,
                "german": "Mein Praktikum in der Anwaltskanzlei war echt toll, ich habe einen hervorragenden Einblick bekommen.",
                "chinese": "我在律师事务所的实习真的棒极了，我对这一行的实际业务有了极佳的深入了解。",
                "clozeWords": ["Praktikum", "Anwaltskanzlei", "hervorragenden", "Einblick"],
                "vocab": [
                    {"word": "das Praktikum", "plural": "die Praktika", "pos": "Nomen", "meaning": "实习", "exampleDe": "Das Praktikum vermittelt wertvolle Praxiserfahrung.", "exampleZh": "实习提供了宝贵的实践经验。"},
                    {"word": "die Kanzlei", "plural": "die Kanzleien", "pos": "Nomen", "meaning": "律师事务所，办事处", "exampleDe": "Die Kanzlei hat sich auf Wirtschaftsrecht spezialisiert.", "exampleZh": "该律师事务所专攻经济法领域。"},
                    {"word": "der Einblick", "plural": "die Einblicke", "pos": "Nomen", "meaning": "见识，洞察，了解", "exampleDe": "Wir erhielten einen Einblick in die Produktion.", "exampleZh": "我们实地观摩了解了生产流程。"}
                ]
            },
            {
                "id": "goethe-b2-praktikum-02-s2",
                "startTime": 10.2,
                "endTime": 20.8,
                "german": "Ich konnte sogar zu ein paar wichtigen Verhandlungsterminen beim Gericht mitgehen.",
                "chinese": "我甚至还能跟随带教律师一同出席法庭的几场重要庭审听证会。",
                "clozeWords": ["Verhandlungsterminen", "Gericht", "mitgehen"],
                "vocab": [
                    {"word": "die Verhandlung", "plural": "die Verhandlungen", "pos": "Nomen", "meaning": "谈判，庭审", "exampleDe": "Die mündliche Verhandlung beginnt morgen.", "exampleZh": "口头审理将于明日开庭。"},
                    {"word": "das Gericht", "plural": "die Gerichte", "pos": "Nomen", "meaning": "法院，法庭", "exampleDe": "Der Fall wird vor dem Landgericht verhandelt.", "exampleZh": "该案件将由地方法院审理。"}
                ]
            },
            {
                "id": "goethe-b2-praktikum-02-s3",
                "startTime": 20.8,
                "endTime": 32.0,
                "german": "Außerdem konnte ich mich in konkrete Rechtsfälle einlesen, was für mein Universitätsseminar sehr nützlich ist.",
                "chinese": "此外我还能深入研读具体的法律卷宗判例，这对我的大学研讨课非常有益。",
                "clozeWords": ["konkrete", "Rechtsfälle", "einlesen", "Seminar"],
                "vocab": [
                    {"word": "konkret", "pos": "Adjektiv", "meaning": "具体的", "exampleDe": "Können Sie uns ein konkretes Beispiel nennen?", "exampleZh": "您能给我们举一个具体的例子吗？"},
                    {"word": "der Fall", "plural": "die Fälle", "pos": "Nomen", "meaning": "案件，情况", "exampleDe": "In diesem konkreten Fall gelten besondere Regeln.", "exampleZh": "在此具体情形下适用特殊规定。"},
                    {"word": "das Seminar", "plural": "die Seminare", "pos": "Nomen", "meaning": "大学研讨课", "exampleDe": "Das juristische Seminar findet jeden Montag statt.", "exampleZh": "法学研讨课在每周一举行。"}
                ]
            }
        ]
    },

    # 10. Goethe C1 Paul Maar
    {
        "id": "goethe-c1-literatur-01",
        "title": "Autorenlesung und Lesekompetenz bei Kindern",
        "level": "C1",
        "source": "Goethe-Institut",
        "topic": "Wissenschaft & Kultur",
        "raw_file": os.path.join(RAW_GOETHE, "goethe_c1_hoeren.mp3"),
        "ss": "140.7",
        "to": "174.5",
        "out_file": "goethe_c1_literatur.mp3",
        "segments": [
            {
                "id": "goethe-c1-literatur-01-s1",
                "startTime": 0.0,
                "endTime": 10.8,
                "german": "Der Kinderbuch-Klassiker wurde millionenfach gekauft, gelesen, vorgelesen und gemalt.",
                "chinese": "这套经典儿童文学名著已被数以百万计的读者购买、研读、亲子朗读和绘制插画。",
                "clozeWords": ["Klassiker", "millionenfach", "vorgelesen"],
                "vocab": [
                    {"word": "der Klassiker", "plural": "die Klassiker", "pos": "Nomen", "meaning": "经典作品", "exampleDe": "Faust gehört zu den bekanntesten Klassikern der deutschen Literatur.", "exampleZh": "《浮士德》是德国文学最著名的经典作品之一。"},
                    {"word": "vorlesen", "pos": "Verb", "meaning": "朗读，读给别人听", "exampleDe": "Der Vater liest den Kindern jeden Abend eine Gutenachtgeschichte vor.", "exampleZh": "父亲每天晚上都给孩子们朗读睡前故事。"}
                ]
            },
            {
                "id": "goethe-c1-literatur-01-s2",
                "startTime": 10.8,
                "endTime": 22.5,
                "german": "An Paul Maar kann es also nicht liegen, dass laut Pisa-Studie 25 Prozent der Schulabsolventen schlecht lesen können.",
                "chinese": "因此绝不能归咎于保罗·马尔，导致比萨测试显示25%的中学毕业生阅读能力低下。",
                "clozeWords": ["liegen", "Studie", "Schulabsolventen", "lesen"],
                "vocab": [
                    {"word": "liegen an", "pos": "Verb", "meaning": "原因在于，归咎于", "exampleDe": "Der Misserfolg lag an der mangelnden Vorbereitung.", "exampleZh": "失败的原因在于准备不足。"},
                    {"word": "die Studie", "plural": "die Studien", "pos": "Nomen", "meaning": "科学研究，调研报告", "exampleDe": "Die neue empirische Studie belegt diesen Trend eindrucksvoll.", "exampleZh": "这项新的实证研究令人信服地证实了该趋势。"},
                    {"word": "der Absolvent", "plural": "die Absolventen", "pos": "Nomen", "meaning": "毕业生", "exampleDe": "Viele Absolventen streben eine universitäre Laufbahn an.", "exampleZh": "许多大学毕业生致力于走学术科研道路。"}
                ]
            },
            {
                "id": "goethe-c1-literatur-01-s3",
                "startTime": 22.5,
                "endTime": 33.8,
                "german": "Beim fünften Literaturfestival liest er heute Nachmittag vor hunderten aufmerksamen Zuhörern.",
                "chinese": "在第五届文学节上，他今天下午将面对数百名聚精会神的现场听众进行专场朗读。",
                "clozeWords": ["Literaturfestival", "aufmerksamen", "Zuhörern"],
                "vocab": [
                    {"word": "das Festival", "plural": "die Festivals", "pos": "Nomen", "meaning": "艺术节，盛会", "exampleDe": "Das internationale Festival zieht Künstler aus aller Welt an.", "exampleZh": "这一国际盛会吸引了来自世界各地的艺术家。"},
                    {"word": "aufmerksam", "pos": "Adjektiv", "meaning": "专心的，专注的", "exampleDe": "Die Zuhörer lauschten der Rede mit aufmerksamem Schweigen.", "exampleZh": "听众专注沉静地聆听了整场演讲。"},
                    {"word": "der Zuhörer", "plural": "die Zuhörer", "pos": "Nomen", "meaning": "听众", "exampleDe": "Der Vortrag begeisterte alle anwesenden Zuhörer.", "exampleZh": "这场报告让在场的所有听众赞叹不已。"}
                ]
            }
        ]
    },

    # 11. TestDaF 01 Musikstudium
    {
        "id": "testdaf-musikstudium-01",
        "title": "Das Musikstudium und die Aufnahmeprüfung",
        "level": "TestDaF",
        "source": "TestDaF",
        "topic": "Campus & Studium",
        "raw_file": os.path.join(RAW_TESTDAF, "testdaf_modellsatz_01_hv.mp3"),
        "ss": "104.1",
        "to": "128.0",
        "out_file": "testdaf_01_musik.mp3",
        "segments": [
            {
                "id": "testdaf-musikstudium-01-s1",
                "startTime": 0.0,
                "endTime": 7.5,
                "german": "Hallo Frau Weller, ich bin's Michael, Sie waren doch meine Musiklehrerin am Gymnasium.",
                "chinese": "您好韦勒老师，我是迈克尔，您当年曾是我们在中学的音乐老师呀。",
                "clozeWords": ["Musiklehrerin", "Gymnasium"],
                "vocab": [
                    {"word": "die Lehrerin", "plural": "die Lehrerinnen", "pos": "Nomen", "meaning": "女教师", "exampleDe": "Unsere engagierte Lehrerin förderte musikalische Talente.", "exampleZh": "我们充满热情的老师鼓励音乐才华的发展。"},
                    {"word": "das Gymnasium", "plural": "die Gymnasien", "pos": "Nomen", "meaning": "高级文理中学", "exampleDe": "Nach dem Gymnasium absolvierte er ein Hochschulstudium.", "exampleZh": "文理中学毕业后他完成了大学学业。"}
                ]
            },
            {
                "id": "testdaf-musikstudium-01-s2",
                "startTime": 7.5,
                "endTime": 15.5,
                "german": "Ich studiere jetzt tatsächlich an der Musikhochschule und möchte später selbst Musiklehrer werden.",
                "chinese": "我现在真正在音乐学院深造，将来也想成为一名专业音乐老师。",
                "clozeWords": ["Musikhochschule", "später", "Musiklehrer"],
                "vocab": [
                    {"word": "die Hochschule", "plural": "die Hochschulen", "pos": "Nomen", "meaning": "高等院校，大学", "exampleDe": "Die Hochschule für Musik genießt weltweit einen exzellenten Ruf.", "exampleZh": "这所音乐高等学府在世界范围内享有崇高声誉。"},
                    {"word": "werden", "pos": "Verb", "meaning": "成为，变成", "exampleDe": "Er möchte nach dem Staatsexamen Richter werden.", "exampleZh": "通过国家司法考试后他希望成为一名法官。"}
                ]
            },
            {
                "id": "testdaf-musikstudium-01-s3",
                "startTime": 15.5,
                "endTime": 23.9,
                "german": "Als mir das klar wurde, musste ich vor der Aufnahmeprüfung noch intensiv Klavier spielen lernen.",
                "chinese": "当我真正想清楚这一志愿时，在参加入学专业测试之前我还必须强化突击练好钢琴。",
                "clozeWords": ["Aufnahmeprüfung", "intensiv", "Klavier"],
                "vocab": [
                    {"word": "die Aufnahmeprüfung", "plural": "die Aufnahmeprüfungen", "pos": "Nomen", "meaning": "入学专业考试", "exampleDe": "Die anspruchsvolle Aufnahmeprüfung verlangt theoretische und praktische Kenntnisse.", "exampleZh": "严苛的入学考试要求兼具扎实的理论与实践功底。"},
                    {"word": "intensiv", "pos": "Adjektiv", "meaning": "强化的高密度的", "exampleDe": "Er bereitete sich durch einen intensiven Sprachkurs vor.", "exampleZh": "他通过高密度的强化语言班进行积极备战。"},
                    {"word": "das Klavier", "plural": "die Klaviere", "pos": "Nomen", "meaning": "钢琴", "exampleDe": "Sie übt täglich zwei Stunden am Klavier.", "exampleZh": "她每天在钢琴前坚持练琴两小时。"}
                ]
            }
        ]
    },

    # 12. TestDaF 01 Assessment
    {
        "id": "testdaf-assessment-02",
        "title": "Assessment-Center in der Personalauswahl",
        "level": "TestDaF",
        "source": "TestDaF",
        "topic": "Beruf & Karriere",
        "raw_file": os.path.join(RAW_TESTDAF, "testdaf_modellsatz_01_hv.mp3"),
        "ss": "434.3",
        "to": "465.0",
        "out_file": "testdaf_01_assessment.mp3",
        "segments": [
            {
                "id": "testdaf-assessment-02-s1",
                "startTime": 0.0,
                "endTime": 10.0,
                "german": "In unserem heutigen Gespräch geht es um eine besondere Form der Personalauswahl, das sogenannte Assessment-Center.",
                "chinese": "在我们今天的专家访谈中，聚焦的是一种新颖的人员录用选拔形式——即所谓的评价中心（Assessment-Center）。",
                "clozeWords": ["Gespräch", "Personalauswahl", "sogenannte"],
                "vocab": [
                    {"word": "das Gespräch", "plural": "die Gespräche", "pos": "Nomen", "meaning": "谈话，访谈", "exampleDe": "Das vertrauliche Gespräch verlief in konstruktiver Atmosphäre.", "exampleZh": "这场机密交谈在富有建设性的氛围中进行。"},
                    {"word": "die Personalauswahl", "pos": "Nomen", "meaning": "人员选拔，招聘评选", "exampleDe": "Moderne Personalauswahl basiert auf wissenschaftlich fundierten Tests.", "exampleZh": "现代人事招聘立足于严谨的科学测评手段。"}
                ]
            },
            {
                "id": "testdaf-assessment-02-s2",
                "startTime": 10.0,
                "endTime": 20.8,
                "german": "Neben der fachlichen Qualifikation spielen soziale Kompetenzen eine immer größere Rolle bei der Einstellung neuer Mitarbeiter.",
                "chinese": "在招录新员工时，除专业学科资质外，人际沟通与团队协作等软性社交能力扮演着日益重要的角色。",
                "clozeWords": ["Qualifikation", "soziale", "Kompetenzen", "Einstellung"],
                "vocab": [
                    {"word": "die Qualifikation", "plural": "die Qualifikationen", "pos": "Nomen", "meaning": "资质，任职资格", "exampleDe": "Seine fachliche Qualifikation entspricht exakt dem Anforderungsprofil.", "exampleZh": "他的专业资质完全契合岗位任职要求。"},
                    {"word": "die Kompetenz", "plural": "die Kompetenzen", "pos": "Nomen", "meaning": "能力，素养，权责", "exampleDe": "Methodische Kompetenz ist im Hochschulalltag unverzichtbar.", "exampleZh": "掌握科学的方法素养在大学日常学习中不可或缺。"},
                    {"word": "die Einstellung", "plural": "die Einstellungen", "pos": "Nomen", "meaning": "聘用，录用", "exampleDe": "Die Kriterien für die Einstellung wurden transparent offengelegt.", "exampleZh": "录用人员的审核标准均予以透明公开。"}
                ]
            },
            {
                "id": "testdaf-assessment-02-s3",
                "startTime": 20.8,
                "endTime": 30.7,
                "german": "Große Konzerne und Banken verzichten daher häufig auf das klassische Vorstellungsgespräch.",
                "chinese": "因此，大型跨国集团与金融银行机构往往不再单一依赖传统的求职面试。",
                "clozeWords": ["Konzerne", "verzichten", "Vorstellungsgespräch"],
                "vocab": [
                    {"word": "der Konzern", "plural": "die Konzerne", "pos": "Nomen", "meaning": "大型企业集团", "exampleDe": "Der Konzern investiert massiv in erneuerbare Energietechnologien.", "exampleZh": "该企业集团正重金投资于可再生能源技术领域。"},
                    {"word": "verzichten", "pos": "Verb", "meaning": "放弃，舍弃", "exampleDe": "Wir verzichten bewusst auf Plastikverpackungen.", "exampleZh": "我们自觉放弃使用塑料包装。"},
                    {"word": "das Vorstellungsgespräch", "plural": "die Vorstellungsgespräche", "pos": "Nomen", "meaning": "求职面试", "exampleDe": "Sie bereitete sich akribisch auf das anstehende Vorstellungsgespräch vor.", "exampleZh": "她为即将到来的求职面试做了细致周密的准备。"}
                ]
            }
        ]
    },

    # 13. TestDaF 02 Radrennen
    {
        "id": "testdaf-radrennen-03",
        "title": "Hochschulsport und Vorbereitung auf das Radrennen",
        "level": "TestDaF",
        "source": "TestDaF",
        "topic": "Campus & Alltag",
        "raw_file": os.path.join(RAW_TESTDAF, "testdaf_modellsatz_02_hv.mp3"),
        "ss": "108.7",
        "to": "132.0",
        "out_file": "testdaf_02_radrennen.mp3",
        "segments": [
            {
                "id": "testdaf-radrennen-03-s1",
                "startTime": 0.0,
                "endTime": 8.0,
                "german": "Wir fahren heute Nachmittag mit dem Zug nach Münster, um an den Deutschen Hochschulmeisterschaften teilzunehmen.",
                "chinese": "我们今天下午乘火车奔赴明斯特，去参加德国大学生锦标赛。",
                "clozeWords": ["Nachmittag", "Meisterschaften", "teilzunehmen"],
                "vocab": [
                    {"word": "die Meisterschaft", "plural": "die Meisterschaften", "pos": "Nomen", "meaning": "锦标赛，冠军争夺赛", "exampleDe": "Unsere Unimannschaft qualifizierte sich für die nationale Meisterschaft.", "exampleZh": "我们的大学校队获得了参加全国锦标赛的资格。"},
                    {"word": "teilnehmen", "pos": "Verb", "meaning": "参与，参加", "exampleDe": "Alle Studierenden dürfen an dem Wettbewerb teilnehmen.", "exampleZh": "所有在读学生均可报名参与该竞赛。"}
                ]
            },
            {
                "id": "testdaf-radrennen-03-s2",
                "startTime": 8.0,
                "endTime": 15.5,
                "german": "Wir trainieren mindestens jeden zweiten Tag und schaffen inzwischen 100 Kilometer in zweieinhalb Stunden.",
                "chinese": "我们至少隔天集训一次，目前已经能达到两个半小时骑行100公里的水准。",
                "clozeWords": ["trainieren", "mindestens", "Kilometer", "Stunden"],
                "vocab": [
                    {"word": "trainieren", "pos": "Verb", "meaning": "训练，锻炼", "exampleDe": "Die Athleten trainieren hart für den bevorstehenden Wettkampf.", "exampleZh": "运动员们为即将到来的比赛刻苦训练。"},
                    {"word": "mindestens", "pos": "Adverb", "meaning": "至少，起码", "exampleDe": "Für das Projekt benötigen wir mindestens drei Wochen Zeit.", "exampleZh": "该项目我们至少需要三周的时间。"},
                    {"word": "der Kilometer", "plural": "die Kilometer", "pos": "Nomen", "meaning": "千米，公里", "exampleDe": "Die Distanz beträgt exakt fünfzehn Kilometer.", "exampleZh": "两地间距整整十五公里。"}
                ]
            },
            {
                "id": "testdaf-radrennen-03-s3",
                "startTime": 15.5,
                "endTime": 23.3,
                "german": "Da die Fahrkarten heute billiger waren, übernachten wir günstig mit dem Schlafsack in der Universitätsturnhalle.",
                "chinese": "因为今天的火车票更便宜，所以我们带上睡袋低成本借宿在大学的体育馆里。",
                "clozeWords": ["Fahrkarten", "übernachten", "Schlafsack", "Sporthalle"],
                "vocab": [
                    {"word": "die Fahrkarte", "plural": "die Fahrkarten", "pos": "Nomen", "meaning": "乘车票，火车票", "exampleDe": "Vergessen Sie nicht, Ihre Fahrkarte am Automaten zu entwerten.", "exampleZh": "切记在自动打票机上为你所持车票盖印检票。"},
                    {"word": "übernachten", "pos": "Verb", "meaning": "过夜，借宿", "exampleDe": "Während der Tagung übernachten die Gäste im Campus-Gästehaus.", "exampleZh": "会议期间与会代表下榻在校区专家招待所。"},
                    {"word": "der Schlafsack", "plural": "die Schlafsäcke", "pos": "Nomen", "meaning": "睡袋", "exampleDe": "Beim Zelten in den Bergen braucht man einen warmen Schlafsack.", "exampleZh": "在高原野外宿营必须备有一款保暖睡袋。"}
                ]
            }
        ]
    },

    # 14. TestDaF 02 Kunstdidaktik
    {
        "id": "testdaf-kunstdidaktik-04",
        "title": "Akademische Kunstdidaktik an der Universität",
        "level": "TestDaF",
        "source": "TestDaF",
        "topic": "Wissenschaft & Forschung",
        "raw_file": os.path.join(RAW_TESTDAF, "testdaf_modellsatz_02_hv.mp3"),
        "ss": "417.6",
        "to": "445.0",
        "out_file": "testdaf_02_kunstdidaktik.mp3",
        "segments": [
            {
                "id": "testdaf-kunstdidaktik-04-s1",
                "startTime": 0.0,
                "endTime": 8.5,
                "german": "Seit zehn Jahren wird an der Universität Dortmund das interdisziplinäre Fach Kunstdidaktik gelehrt.",
                "chinese": "十年来，多特蒙德大学一直开设着美术教学法这一跨学科交叉专业门类。",
                "clozeWords": ["Universität", "interdisziplinäre", "Fach", "gelehrt"],
                "vocab": [
                    {"word": "die Universität", "plural": "die Universitäten", "pos": "Nomen", "meaning": "大学，综合性大学", "exampleDe": "Die Universität fördert den internationalen wissenschaftlichen Austausch.", "exampleZh": "大学大力扶持国际学术交流与合作。"},
                    {"word": "das Fach", "plural": "die Fächer", "pos": "Nomen", "meaning": "专业，科目", "exampleDe": "Er belegt Kunstdidaktik als akademisches Hauptfach.", "exampleZh": "他选择美术教育学作为大学主修专业。"},
                    {"word": "lehren", "pos": "Verb", "meaning": "讲授，任教", "exampleDe": "Die renommierte Dozentin lehrt seit vielen Jahren Kunstgeschichte.", "exampleZh": "这位资深讲师已执教美术史多年。"}
                ]
            },
            {
                "id": "testdaf-kunstdidaktik-04-s2",
                "startTime": 8.5,
                "endTime": 17.5,
                "german": "Über die wissenschaftliche Methodik und didaktische Konzepte möchten wir heute mit Frau Professor Weber sprechen.",
                "chinese": "今天我们将就其严谨的科研方法论与教学法设计理念，与韦伯教授展开深度访谈。",
                "clozeWords": ["wissenschaftliche", "Methodik", "didaktische", "Konzepte"],
                "vocab": [
                    {"word": "wissenschaftlich", "pos": "Adjektiv", "meaning": "学术的，科学的", "exampleDe": "Die Studie erfüllt alle Kriterien für wissenschaftliches Arbeiten.", "exampleZh": "该项研究完全符合严谨学术规范的所有准则。"},
                    {"word": "die Methodik", "pos": "Nomen", "meaning": "方法论，方法体系", "exampleDe": "Eine solide qualitative Methodik bildet das Fundament der Dissertation.", "exampleZh": "扎实优质的质性方法体系构成了博士论文的坚实根基。"},
                    {"word": "das Konzept", "plural": "die Konzepte", "pos": "Nomen", "meaning": "概念，方案，设想", "exampleDe": "Das didaktische Konzept verbindet Theorie und Unterrichtspraxis.", "exampleZh": "该教学方案将抽象理论与具体课堂实践紧密结合。"}
                ]
            },
            {
                "id": "testdaf-kunstdidaktik-04-s3",
                "startTime": 17.5,
                "endTime": 27.4,
                "german": "Dabei geht es um die Verbindung von ästhetischer Praxis und zeitgemäßen kunstpädagogischen Theorien.",
                "chinese": "其中的核心在于探索审美艺术实践同当代前沿美术教育学理论的有机融合。",
                "clozeWords": ["Verbindung", "ästhetischer", "Praxis", "Theorien"],
                "vocab": [
                    {"word": "die Verbindung", "plural": "die Verbindungen", "pos": "Nomen", "meaning": "连结，纽带，结合", "exampleDe": "Die Verbindung von Theorie und Praxis steht im Zentrum des Lehrplans.", "exampleZh": "理论与实践的相辅相成是整个教学大纲的核心。"},
                    {"word": "ästhetisch", "pos": "Adjektiv", "meaning": "审美的，美学的", "exampleDe": "Das Werk besticht durch seine hohe ästhetische Qualität.", "exampleZh": "该作品凭借其高超的美学造诣令人叹为观止。"},
                    {"word": "die Theorie", "plural": "die Theorien", "pos": "Nomen", "meaning": "理论，学说", "exampleDe": "Moderne pädagogische Theorien betonen aktives Handeln der Lernenden.", "exampleZh": "现代教育理论高度强调并倡导学习者的能动实践。"}
                ]
            }
        ]
    },

    # 15. TestDaF 01 Campusleben
    {
        "id": "testdaf-campusleben-05",
        "title": "Atmosphäre an der Hochschule und Studienstart",
        "level": "TestDaF",
        "source": "TestDaF",
        "topic": "Campus & Studium",
        "raw_file": os.path.join(RAW_TESTDAF, "testdaf_modellsatz_01_hv.mp3"),
        "ss": "180.0",
        "to": "208.5",
        "out_file": "testdaf_01_campusleben.mp3",
        "segments": [
            {
                "id": "testdaf-campusleben-05-s1",
                "startTime": 0.0,
                "endTime": 9.2,
                "german": "Die persönliche Atmosphäre an der Hochschule ist für angehende Studierende einfach etwas ganz Besonderes.",
                "chinese": "高校充满人情味的校园学术氛围，对于准大一新生而言确实是非同凡响的独特体验。",
                "clozeWords": ["Atmosphäre", "angehende", "Studierende", "Besonderes"],
                "vocab": [
                    {"word": "die Atmosphäre", "plural": "die Atmosphären", "pos": "Nomen", "meaning": "氛围，环境氛围", "exampleDe": "Am Universitätscampus herrscht eine weltoffene Atmosphäre.", "exampleZh": "大学校园弥漫着包容开放的世界性学术氛围。"},
                    {"word": "der Studierende", "plural": "die Studierenden", "pos": "Nomen", "meaning": "大学生，高校在读学生", "exampleDe": "Für internationale Studierende werden Begrüßungsveranstaltungen organisiert.", "exampleZh": "专门面向国际留学生策划举办了一系列迎新交流活动。"}
                ]
            },
            {
                "id": "testdaf-campusleben-05-s2",
                "startTime": 9.2,
                "endTime": 18.0,
                "german": "Am Tag der Prüfung gibt es immer ein gemeinsames Frühstück für alle Bewerberinnen und Bewerber.",
                "chinese": "在考核日当天，院系总会面向全体应试考生贴心备好齐聚一堂的迎考交流早餐。",
                "clozeWords": ["Prüfung", "gemeinsames", "Frühstück", "Bewerber"],
                "vocab": [
                    {"word": "die Prüfung", "plural": "die Prüfungen", "pos": "Nomen", "meaning": "考核，考试", "exampleDe": "Die mündliche Prüfung wird von zwei Hochschulprüfern abgenommen.", "exampleZh": "口试由两位高校主考官联合主持测评。"},
                    {"word": "das Frühstück", "plural": "die Frühstücke", "pos": "Nomen", "meaning": "早餐", "exampleDe": "Ein gesundes Frühstück liefert Energie für den Lerntag.", "exampleZh": "一顿营养早餐为一整天的用功研修提供充沛精力。"},
                    {"word": "der Bewerber", "plural": "die Bewerber", "pos": "Nomen", "meaning": "申请者，应试者", "exampleDe": "Auf die Studienplätze bewarben sich zahlreiche qualifizierte Bewerber.", "exampleZh": "众多具备优异资历的申请人角逐这些大学录取名额。"}
                ]
            },
            {
                "id": "testdaf-campusleben-05-s3",
                "startTime": 18.0,
                "endTime": 28.5,
                "german": "Wer möchte, kann so vor dem eigentlichen Beginn schon erste Kontakte zu Kommilitonen aus höheren Semestern knüpfen.",
                "chinese": "有意的同学便可借此在正式开考前，与高年级的学长学姐提前建立联系并交流取经。",
                "clozeWords": ["Beginn", "Kontakte", "Kommilitonen", "knüpfen"],
                "vocab": [
                    {"word": "der Kontakt", "plural": "die Kontakte", "pos": "Nomen", "meaning": "联系，交往", "exampleDe": "Auf Karrieremessen lassen sich wertvolle Kontakte zu Arbeitgebern knüpfen.", "exampleZh": "在职业招聘会上能与优质用人单位建立宝贵联系。"},
                    {"word": "der Kommilitone", "plural": "die Kommilitonen", "pos": "Nomen", "meaning": "大学同学，校友", "exampleDe": "Ich lerne in der Universitätsbibliothek oft gemeinsam mit meinen Kommilitonen.", "exampleZh": "我经常与我的大学同学们在校图书馆共同自修。"},
                    {"word": "knüpfen", "pos": "Verb", "meaning": "建立（联系），结识", "exampleDe": "Internationale Studierende knüpfen bei Orientierungstagen schnell Freundschaften.", "exampleZh": "外国留学生在新生迎新日期间很快结下了深厚友谊。"}
                ]
            }
        ]
    }
]

def main():
    tracks_json = []
    for item in TRACK_DEFINITIONS:
        out_path = os.path.join(OUT_DIR, item["out_file"])
        print(f"[SLICING] {item['id']} -> {item['out_file']} ({item['ss']}s to {item['to']}s)...")
        cmd = [
            FFMPEG, "-y", "-ss", item["ss"], "-to", item["to"],
            "-i", item["raw_file"],
            "-c:a", "libmp3lame", "-b:a", "128k",
            out_path
        ]
        ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if ret.returncode != 0:
            print(f"Error slicing {item['id']}: {ret.stderr.decode('utf-8', errors='ignore')}")
            continue

        size = os.path.getsize(out_path)
        dur = float(item["to"]) - float(item["ss"])
        print(f"  -> Generated {item['out_file']}: {size:,} bytes (~{dur:.1f}s)")

        # Prepare ListeningTrack object
        track_obj = {
            "id": item["id"],
            "title": item["title"],
            "level": item["level"],
            "source": item["source"],
            "topic": item["topic"],
            "audioUrl": f"/audio/tracks/{item['out_file']}",
            "duration": round(dur, 2),
            "segments": item["segments"]
        }
        tracks_json.append(track_obj)

    # Save to generatedTracks.json
    json_path = r"C:\Users\king\Downloads\听力\src\data\generatedTracks.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(tracks_json, f, ensure_ascii=False, indent=2)
    print(f"\n[DONE] Successfully saved {len(tracks_json)} authentic tracks to {json_path}!")

if __name__ == "__main__":
    main()
