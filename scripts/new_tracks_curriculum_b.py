# -*- coding: utf-8 -*-
"""
Curated Chinese translations, clozeWords, vocab items, and normalized topics
for Tracks 12-24 (4 DW Top-Thema B1 + 3 DW LGN B2 + 6 telc B2/C1).
"""

def v(word, pos, meaning, ex_de, ex_zh, plural=None):
    item = {
        "word": word,
        "pos": pos,
        "meaning": meaning,
        "exampleDe": ex_de,
        "exampleZh": ex_zh,
    }
    if plural:
        item["plural"] = plural
    return item


CURRICULUM_B = {
    "dw-tt-79969942": {
        "topic": "Kultur & Geschichte",
        "segments": [
            {
                "chinese": "腊肠犬（Dackel）不仅仅是一种体型独特的犬种。",
                "clozeWords": ["Dackel", "besonderen", "Form"],
                "vocab": [
                    v("der Dackel", "Nomen", "腊肠犬（德国典型猎犬品种）", "Der Dackel hat kurze Beine und einen langen Rücken.", "腊肠犬腿短而身长。", plural="die Dackel"),
                ],
            },
            {
                "chinese": "它在艺术领域是备受喜爱的形象，同时也与德国的历史和政治有着紧密联系——无论在积极方面还是消极方面皆是如此。",
                "clozeWords": ["beliebte", "Verbindung", "Geschichte", "Politik"],
                "vocab": [
                    v("sowohl ... als auch", "Ausdruck", "既……又……，不仅……而且……", "Die Ausstellung bietet sowohl Kunst als auch Geschichte.", "该展览既展示艺术也呈现历史。"),
                ],
            },
            {
                "chinese": "长而圆润的身体让它看起来宛如一根香肠：腊肠犬极具辨识度，并常常成为艺术创作的题材。",
                "clozeWords": ["unverwechselbar", "Gegenstand", "Kunst"],
                "vocab": [
                    v("unverwechselbar", "Adjektiv", "独一无二的，极具辨识度的，不会混淆的", "Seine tiefe Stimme ist einfach unverwechselbar.", "他低沉的嗓音让人一听就能认出来。"),
                    v("der Gegenstand", "Nomen", "题材，主题，物品", "Alte Fotografien wurden zum Gegenstand ihrer Forschung.", "老照片成了她研究的对象。", plural="die Gegenstände"),
                ],
            },
            {
                "chinese": "“这确实是一种外形极具标志性的犬类，因此让它在众多领域都备受欢迎。”目前正在不来梅举办的一场腊肠犬主题展览策展人安内特·雷克特解释道。",
                "clozeWords": ["ikonischen", "aktuellen", "Ausstellung"],
                "vocab": [
                    v("ikonisch", "Adjektiv", "标志性的，经典象征性的", "Das Bauhaus-Design gilt bis heute als ikonisch.", "包豪斯设计至今仍被视为经典标志。"),
                    v("die Ausstellung", "Nomen", "展览，陈列", "Am Wochenende eröffnete eine neue Ausstellung im Museum.", "周末博物馆举办了一场新展览。", plural="die Ausstellungen"),
                ],
            },
            {
                "chinese": "然而，不仅奥托·迪克斯、安迪·沃霍尔或巴勃罗·毕加索等世界级大师画过这种狗，它本身也讲述了一段文化史，与德国密不可分。",
                "clozeWords": ["weltberühmten", "Kulturgeschichte", "verbunden"],
                "vocab": [
                    v("die Kulturgeschichte", "Nomen", "文化史", "Kaffeehäuser spielen eine wichtige Rolle in der Kulturgeschichte.", "咖啡馆在文化史上扮演重要角色。"),
                    v("verbunden sein mit", "Ausdruck", "与……紧密相连", "Viel Arbeit ist mit diesem Projekt verbunden.", "这个项目与大量工作密切相关。"),
                ],
            },
        ],
    },
    "dw-tt-79928392": {
        "topic": "Umwelt & Energie",
        "segments": [
            {
                "chinese": "芬兰成为世界上第一个批准建造核废料最终处置库的国家。",
                "clozeWords": ["Endlager", "Atommüll", "genehmigt"],
                "vocab": [
                    v("das Endlager", "Nomen", "（核废料等的）地下永久处置库", "Für radioaktive Abfälle wird ein sicheres Endlager benötigt.", "放射性废料需要安全的永久处置库。", plural="die Endlager"),
                    v("der Atommüll", "Nomen", "核废料，放射性废物", "Wie soll der Atommüll langfristig gelagert werden?", "核废料应如何长期储存？"),
                    v("genehmigen", "Verb", "批准，核准", "Die Behörde hat den Bauantrag gestern genehmigt.", "主管部门昨天批准了建造申请。"),
                ],
            },
            {
                "chinese": "德国仍在继续寻找安全可靠的选址地点。",
                "clozeWords": ["sucht", "sicheren", "Ort"],
                "vocab": [
                    v("sicher", "Adjektiv", "安全的，可靠的，稳妥的", "Geologen prüfen, welche Gesteinsschichten besonders sicher sind.", "地质学家检测哪些岩层尤为安全。"),
                ],
            },
            {
                "chinese": "这不仅是一项艰巨复杂的任务，同时也需要耗费巨额资金。",
                "clozeWords": ["schwierige", "Aufgabe", "gleichzeitig"],
                "vocab": [
                    v("die Aufgabe", "Nomen", "任务，作业，课题", "Die Suche nach einer Lösung ist eine nationale Aufgabe.", "寻找解决方案是一项全国性的任务。", plural="die Aufgaben"),
                ],
            },
            {
                "chinese": "试问谁能预言十万年之后的世界将会发生什么呢？",
                "clozeWords": ["sagen", "geschehen"],
                "vocab": [
                    v("geschehen", "Verb", "发生，出现", "Niemand weiß, was in so ferner Zukunft geschehen wird.", "没有人知道在那样遥远的未来会发生什么。"),
                ],
            },
            {
                "chinese": "届时地球又会是一副怎样的面貌呢？",
                "clozeWords": ["Erde", "aussehen"],
                "vocab": [
                    v("aussehen", "Verb", "看起来，呈现出……外貌", "Nach dem Umbau wird das Stadtzentrum völlig anders aussehen.", "改造后市中心将呈现截然不同的面貌。"),
                ],
            },
        ],
    },
    "dw-tt-79906631": {
        "topic": "Kultur & Geschichte",
        "segments": [
            {
                "chinese": "集中营纪念馆内出现的失礼不敬行为以及对德国历史记忆文化的批评，令专家学者感到担忧。",
                "clozeWords": ["Respekt", "Erinnerungskultur", "Sorgen"],
                "vocab": [
                    v("der Respekt", "Nomen", "尊重，敬重", "Man sollte historischen Orten mit Respekt begegnen.", "人们应当以敬重之心对待历史纪念场所。"),
                    v("die Erinnerungskultur", "Nomen", "历史记忆文化，反思文化", "Die Erinnerungskultur ist ein fester Teil der deutschen Demokratie.", "历史反思与记忆文化是德国民主的重要组成部分。"),
                ],
            },
            {
                "chinese": "与此同时，能够亲口讲述大屠杀经历的历史亲历者与见证人正变得越来越少。",
                "clozeWords": ["weniger", "Zeitzeugen", "berichten"],
                "vocab": [
                    v("der Zeitzeuge", "Nomen", "历史见证人，亲历者", "Zeitzeugen berichten oft vor Schulklassen über ihr Leben.", "历史亲历者常常在学校班级讲述自身经历。", plural="die Zeitzeugen"),
                ],
            },
            {
                "chinese": "在布痕瓦尔德集中营纪念馆，有些青少年会拍自拍照：拍照时他们不仅嘻笑，甚至还行纳粹礼。",
                "clozeWords": ["manche", "lachen", "Hitlergruß"],
                "vocab": [
                    v("der Hitlergruß", "Nomen", "纳粹敬礼（在德国属违法行为）", "Das Zeigen des Hitlergrußes ist in Deutschland strafbar.", "在德国行纳粹敬礼属于违法犯罪行为。", plural="die Hitlergrüße"),
                ],
            },
            {
                "chinese": "随后他们还会把这些照片上传发布到社交媒体上。",
                "clozeWords": ["stellen", "später", "sozialen", "Medien"],
                "vocab": [
                    v("ins Netz stellen", "Ausdruck", "上传，发布到网上", "Ohne Überlegung stellen manche Fotos in soziale Medien.", "有人不假思索地把照片发到社交媒体上。"),
                ],
            },
            {
                "chinese": "据布痕瓦尔德及米特尔鲍-多拉纪念馆基金会主任延斯-克里斯蒂安·瓦格纳透露，此类事件近几年正变得越来越频繁。",
                "clozeWords": ["Direktor", "Stiftung", "häufiger"],
                "vocab": [
                    v("die Stiftung", "Nomen", "基金会", "Die Stiftung fördert Bildungsprojekte für Jugendliche.", "该基金会资助面向青少年的教育项目。", plural="die Stiftungen"),
                ],
            },
        ],
    },
    "dw-tt-79865235": {
        "topic": "Wirtschaft & Digitales",
        "segments": [
            {
                "chinese": "节省开支、更加快速且高效地工作：许多企业对人工智能寄予厚望。",
                "clozeWords": ["sparen", "effizienter", "Erwartungen", "Intelligenz"],
                "vocab": [
                    v("effizient", "Adjektiv", "高效的，有成效的", "Mit guten Werkzeugen arbeitet das Team deutlich effizienter.", "借助优秀工具，团队工作明显更加高效。"),
                    v("die Erwartung", "Nomen", "期待，期望", "Das neue System hat alle Erwartungen übertroffen.", "新系统超出了所有期待。", plural="die Erwartungen"),
                ],
            },
            {
                "chinese": "然而如今它们开始质疑：这种投入产出比（成本效益账）真的划算吗？",
                "clozeWords": ["mittlerweile", "Kosten-Nutzen-Rechnung", "aufgeht"],
                "vocab": [
                    v("die Kosten-Nutzen-Rechnung", "Nomen", "成本效益核算，性价比盘算", "Vor einer Investition prüft man die Kosten-Nutzen-Rechnung.", "投资前会先核算成本效益比。", plural="die Kosten-Nutzen-Rechnungen"),
                    v("aufgehen", "Verb", "（账目/计划）算得过来，成功奏效", "Diese Berechnung geht am Ende leider nicht auf.", "这笔账算下来最终并不划算。"),
                ],
            },
            {
                "chinese": "“有了人工智能，一切都将变得更便宜、更简单、更优质”：许多企业长久以来都是这么想的。",
                "clozeWords": ["billiger", "einfacher", "gedacht"],
                "vocab": [
                    v("der Einsatz", "Nomen", "使用，投入，部署", "Der sinnvolle Einsatz neuer Technik spart Zeit.", "合理运用新技术能节省时间。", plural="die Einsätze"),
                ],
            },
            {
                "chinese": "但这种认知如今正在发生转变。",
                "clozeWords": ["ändert", "gerade"],
                "vocab": [
                    v("sich ändern", "Verb", "改变，发生变化", "Die Arbeitswelt wird sich in den nächsten Jahren stark ändern.", "未来几年职场环境将发生巨大变化。"),
                ],
            },
            {
                "chinese": "“几年前，各类AI应用还相对便宜，因为当时人们支付的‘货币’是数据。”慕尼黑大学数字工作学教授安妮-索菲·迈尔解释说。",
                "clozeWords": ["Anwendungen", "relativ", "Währung", "Daten"],
                "vocab": [
                    v("die Anwendung", "Nomen", "应用软件，应用，运用", "Viele Anwendungen laufen direkt im Browser.", "许多应用直接在浏览器中运行。", plural="die Anwendungen"),
                    v("die Währung", "Nomen", "货币，通行交换媒介", "Im digitalen Zeitalter gelten persönliche Daten oft als Währung.", "在数字时代，个人数据往往被视作交易货币。", plural="die Währungen"),
                ],
            },
        ],
    },
    "dw-lgn-79977343": {
        "topic": "Politik & Weltgeschehen",
        "segments": [
            {
                "chinese": "美国民主党赢下阿拉斯加州最后一个悬而未决的参议院席位。",
                "clozeWords": ["gewinnen", "offenen", "Senatssitz"],
                "vocab": [
                    v("der Senatssitz", "Nomen", "参议院席位", "Um diesen Senatssitz wurde monatelang gerungen.", "人们为争夺这一参议院席位激战数月。", plural="die Senatssitze"),
                ],
            },
            {
                "chinese": "在美国国会选举结束两周后，民主党也赢得了最后一个仍未定局的参议员席位。",
                "clozeWords": ["Wochen", "Demokraten", "gewonnen"],
                "vocab": [
                    v("die Kongresswahl", "Nomen", "国会选举", "Bei den Kongresswahlen waren viele Sitze hart umkämpft.", "在国会选举中许多席位竞争激烈。", plural="die Kongresswahlen"),
                ],
            },
            {
                "chinese": "在阿拉斯加州，玛丽·佩尔托拉击败了共和党籍现任参议员丹·沙利文。",
                "clozeWords": ["setzte", "republikanischen", "Amtsinhaber"],
                "vocab": [
                    v("sich durchsetzen", "Verb", "胜出，坚持并取得胜利（gegen + A）", "Die Kandidatin setzte sich knapp gegen ihren Konkurrenten durch.", "这位女候选人微弱优势击败竞争对手。"),
                    v("der Amtsinhaber", "Nomen", "现任公职人员，在任者", "Der Amtsinhaber verteidigte sein Mandat über mehrere Jahre.", "现任者多年来一直保住自己的席位。", plural="die Amtsinhaber"),
                ],
            },
            {
                "chinese": "根据初步统计结果，她获得了50.1%的选票，沙利文的得票率为45.8%。",
                "clozeWords": ["vorläufigem", "Ergebnis", "Stimmen"],
                "vocab": [
                    v("vorläufig", "Adjektiv", "临时的，初步的，暂定的", "Laut vorläufigem Ergebnis liegt die Beteiligung bei 68 Prozent.", "根据初步结果，投票率为68%。"),
                ],
            },
            {
                "chinese": "佩尔托拉由此成为来自阿拉斯加州的第一位原住民女性联邦参议员。",
                "clozeWords": ["damit", "indigene", "Senatorin"],
                "vocab": [
                    v("indigen", "Adjektiv", "原住民的，土著的", "Indigene Gemeinschaften setzen sich stark für Naturschutz ein.", "原住民社区大力倡导自然保护。"),
                ],
            },
        ],
    },
    "dw-lgn-79966293": {
        "topic": "Politik & Weltgeschehen",
        "segments": [
            {
                "chinese": "因俄罗斯军机接近，日本紧急起飞战斗机拦截警戒。",
                "clozeWords": ["Kampfjets", "Flugzeuge", "aufsteigen"],
                "vocab": [
                    v("aufsteigen", "Verb", "起飞升空；攀登", "Bei Annäherung fremder Flugzeuge steigen Abfangjäger auf.", "当不明飞机接近时，拦截机紧急升空。"),
                ],
            },
            {
                "chinese": "日本方面指责俄罗斯侵犯了其领空。",
                "clozeWords": ["Verletzung", "Luftraums", "vorgeworfen"],
                "vocab": [
                    v("die Verletzung", "Nomen", "侵犯，违反；受伤", "Eine Verletzung des Luftraums führt oft zu diplomatischen Krisen.", "侵犯领空往往引发外交危机。", plural="die Verletzungen"),
                    v("vorwerfen", "Verb", "指责，责备（+ 第三格人 + 第四格事）", "Die Regierung warf der Gegenseite einen Vertragsbruch vor.", "政府指责对方违约。"),
                ],
            },
            {
                "chinese": "日本政府发言人木原稔通报称，当天上午两架疑似俄罗斯飞机在西南部的冲之岛附近闯入了日本领空。",
                "clozeWords": ["mutmaßlich", "südwestlichen", "eingedrungen"],
                "vocab": [
                    v("mutmaßlich", "Adjektiv", "据推测的，疑似的", "Die Polizei fasste den mutmaßlichen Täter am Abend.", "警方当晚抓获了疑似嫌疑人。"),
                    v("eindringen", "Verb", "闯入，入侵，渗入", "Feuchtigkeit darf nicht in die Wände eindringen.", "潮气不能渗入墙壁内部。"),
                ],
            },
            {
                "chinese": "他表示，日本战斗机随后升空，向这两架军机发出警告。",
                "clozeWords": ["aufgestiegen", "Maschinen", "warnen"],
                "vocab": [
                    v("warnen", "Verb", "警告，提醒警惕", "Der Wetterdienst warnte vor starkem Sturm an der Küste.", "气象部门警告沿海将有强风暴。"),
                ],
            },
            {
                "chinese": "东京方面称此举是对日本主权的严重侵犯，并向莫斯科提出了严正抗议。",
                "clozeWords": ["schwerwiegenden", "Souveränität", "Protest"],
                "vocab": [
                    v("schwerwiegend", "Adjektiv", "严重的，后果重大的", "Der Bericht deckte schwerwiegende Sicherheitsmängel auf.", "报告揭示了严重的安全隐患。"),
                    v("die Souveränität", "Nomen", "主权，独立自主权", "Jeder Staat pocht auf die Wahrung seiner Souveränität.", "每个国家都强调维护自身主权。"),
                ],
            },
        ],
    },
    "dw-lgn-79956504": {
        "topic": "Umwelt & Energie",
        "segments": [
            {
                "chinese": "在土耳其举行的世界气候大会进入最后冲刺阶段。",
                "clozeWords": ["Weltklimakonferenz", "finale", "Phase"],
                "vocab": [
                    v("final", "Adjektiv", "最终的，最后阶段的", "In der finalen Phase werden die Kompromisse ausgehandelt.", "在最后阶段将就折中方案展开磋商。"),
                ],
            },
            {
                "chinese": "在土耳其安塔利亚举行的联合国气候大会本周一开启决定性的第二周议程。",
                "clozeWords": ["beginnt", "entscheidende", "Woche"],
                "vocab": [
                    v("entscheidend", "Adjektiv", "决定性的，关键的", "Die nächsten Verhandlungstage sind entscheidend für den Vertrag.", "接下来的谈判日对协议能否达成至关重要。"),
                ],
            },
            {
                "chinese": "德国联邦环境部长卡斯滕·施奈德也介入了相关谈判。",
                "clozeWords": ["Bundesumweltminister", "Verhandlungen"],
                "vocab": [
                    v("sich einschalten", "Verb", "介入，插手参与", "Spitzenpolitiker schalten sich oft spät in schwierige Gespräche ein.", "高层政治人物常在棘手会谈后期介入协调。"),
                ],
            },
            {
                "chinese": "他不仅代表德国联邦政府出席COP31峰会，而且受土耳其主席国委托，与印度同行布彭德拉·亚达夫共同担任“减排议题”的谈判协调人。",
                "clozeWords": ["vertritt", "Vermittler", "Emissionsminderung"],
                "vocab": [
                    v("der Vermittler", "Nomen", "调解人，协调人，中间人", "Ein erfahrener Vermittler half beiden Gruppen zur Einigung.", "一位经验丰富的调解人促成双方达成一致。", plural="die Vermittler"),
                    v("die Emissionsminderung", "Nomen", "减少排放，减排", "Strenge Ziele zur Emissionsminderung sind im Klimaschutz zentral.", "严格的减排目标是气候保护的核心。", plural="die Emissionsminderungen"),
                ],
            },
            {
                "chinese": "关于气候融资的谈判进展尤为艰难，因为今年工业发达国家向发展中国家做出让步的意愿格外低。",
                "clozeWords": ["Klimafinanzierung", "Bereitschaft", "Zugeständnissen"],
                "vocab": [
                    v("sich zäh gestalten", "Ausdruck", "进展艰难，拉锯胶着", "Die Gespräche über neue Steuern gestalteten sich sehr zäh.", "关于新税制的谈判推进得十分胶着。"),
                    v("das Zugeständnis", "Nomen", "让步，妥协", "Ohne gegenseitige Zugeständnisse gibt es keinen Kompromiss.", "没有相互让步就无法达成妥协。", plural="die Zugeständnisse"),
                ],
            },
        ],
    },
    "telc-b2-mietrecht-01": {
        "topic": "Wohnen & Lebensstile",
        "segments": [
            {
                "chinese": "今后租客将能够比以往更快地解除自己的住房租赁合同。",
                "clozeWords": ["Mieter", "Mietvertrag", "kündigen"],
                "vocab": [
                    v("der Mietvertrag", "Nomen", "租房合同，租赁契约", "Lesen Sie den Mietvertrag vor der Unterschrift sorgfältig.", "签字前请仔细阅读租房合同。", plural="die Mietverträge"),
                    v("kündigen", "Verb", "解除（合同），辞职", "Man muss die Wohnung drei Monate im Voraus kündigen.", "退租需要提前三个月通知解约。"),
                ],
            },
            {
                "chinese": "《星期日图片报》对此进行了报道。",
                "clozeWords": ["berichtet"],
                "vocab": [
                    v("berichten", "Verb", "报道，汇报", "Zahlreiche Zeitungen berichteten über das neue Gesetz.", "多家报纸报道了这项新法案。"),
                ],
            },
            {
                "chinese": "报道称，德国联邦政府正计划把长期租客的法定最长解约通知期也从12个月缩短至6个月。",
                "clozeWords": ["Kündigungsfrist", "langjährige", "herabzusetzen"],
                "vocab": [
                    v("die Kündigungsfrist", "Nomen", "解约期限，提前通知解约期", "Die gesetzliche Kündigungsfrist beträgt für Mieter meistens drei Monate.", "租客的法定解约通知期通常为三个月。", plural="die Kündigungsfristen"),
                    v("herabsetzen", "Verb", "降低，缩减（标准/期限/税率）", "Das Parlament will die Altersgrenze herabsetzen.", "议会打算降低年龄限制。"),
                ],
            },
            {
                "chinese": "而对于房东来说则没有任何变化，租期满10年后房东仍须遵守长达一年的解约通知期。",
                "clozeWords": ["Vermieter", "weiterhin", "einhalten"],
                "vocab": [
                    v("einhalten", "Verb", "遵守，履行（规定/期限）", "Alle Vertragsparteien müssen die Fristen genau einhalten.", "合同各方都必须严格遵守期限。"),
                ],
            },
        ],
    },
    "telc-b2-zugspitze-02": {
        "topic": "Wetter & Reisen",
        "segments": [
            {
                "chinese": "我现在从办公室窗户往外看就能看到楚格峰。",
                "clozeWords": ["zurzeit", "Bürofenster", "rausschaue"],
                "vocab": [
                    v("rausschauen", "Verb", "朝外看，望向窗外（口语 = herausschauen）", "Wenn ich morgens rausschaue, sehe ich sofort die Berge.", "我早上朝外看时立刻就能看到群山。"),
                ],
            },
            {
                "chinese": "楚格峰现在积雪很深，韦特施泰因山脊也覆盖着白雪；不过话说回来，山脚往下一片翠绿，景色其实非常赏心悦目。",
                "clozeWords": ["verschneit", "weiter", "Anschauen"],
                "vocab": [
                    v("verschneit", "Adjektiv", "被大雪覆盖的，白雪皑皑的", "Im Winter bieten verschneite Gipfel ein herrliches Panorama.", "冬天白雪覆盖的山峰呈现壮丽全景。"),
                ],
            },
            {
                "chinese": "度假游客对山区糟糕的天气作何反应？大家已经在激烈抱怨了，还是抱着“哎呀，我们照样自得其乐吧”的心态？",
                "clozeWords": ["Feriengäste", "herum", "draus"],
                "vocab": [
                    v("maulen", "Verb", "抱怨，嘟囔发牢骚（口语）", "Einige Gäste maulten zuerst über den Dauerregen.", "一开始有几位客人抱怨阴雨连绵。"),
                ],
            },
            {
                "chinese": "这个嘛，幸好在加米施-帕滕基兴总有足够多的替代活动选择：我们这里能提供的项目实在非常丰富，游客们也很看重这一点。这里有游泳馆，还有可以滑冰的冰上运动场。眼下大家也很喜欢乘车上去上阿默高观看耶稣受难剧。",
                "clozeWords": ["genügend", "Alternativen", "schätzen"],
                "vocab": [
                    v("die Alternative", "Nomen", "替代方案，备选方案", "Bei Regen braucht man gute Alternativen für Ausflüge.", "下雨天郊游需要充足的室内备选方案。", plural="die Alternativen"),
                    v("schätzen", "Verb", "珍视，赞赏；估算", "Urlauber schätzen das vielfältige Kulturprogramm.", "度假者很欣赏丰富多彩的文化活动安排。"),
                ],
            },
            {
                "chinese": "此外这里还有200公里长的徒步步道——所以即使遇上坏天气也有足够多可做的事；每天还举办三次温泉疗养音乐会之类活动，客人们绝对不会觉得无聊，这非常重要。",
                "clozeWords": ["Wanderwege", "Schlechtwetter", "langweilig"],
                "vocab": [
                    v("das Schlechtwetter", "Nomen", "恶劣天气，坏天气", "Auch bei Schlechtwetter bleiben die Museen gut besucht.", "即便遇到恶劣天气，博物馆也依然游人如织。"),
                ],
            },
        ],
    },
    "telc-b2-kulturfestival-03": {
        "topic": "Kultur & Freizeit",
        "segments": [
            {
                "chinese": "接下来为您送上我们的周末出行贴士：这次我们邀请您前往法兰克福博物馆岸节。它究竟是一场多元文化的交融聚会，还是全城最长的炸薯条美食街呢？",
                "clozeWords": ["Wochenendtipp", "Kulturen"],
                "vocab": [
                    v("das Treffen", "Nomen", "聚会，会晤，聚首", "Das jährliche Treffen lockt Besucher aus aller Welt an.", "一年一度的盛会吸引了世界各地的游客。", plural="die Treffen"),
                ],
            },
            {
                "chinese": "一如既往，完全取决于您自己，看您如何从这样琳琅满目的文化、电影和美食菜单中挑选享受。",
                "clozeWords": ["reichhaltigen", "Angebot", "Gastronomie"],
                "vocab": [
                    v("reichhaltig", "Adjektiv", "丰富多样的，丰盛的", "Das Programm bietet ein reichhaltiges Angebot für Familien.", "活动菜单为家庭游客提供了极其丰富的选择。"),
                    v("ankommen auf", "Verb", "取决于（auf + A）", "Am Ende kommt es ganz auf den eigenen Geschmack an.", "最终完全取决于个人品味偏好。"),
                ],
            },
            {
                "chinese": "今年有超过300场文化活动同场竞技吸引目光，其中许多围绕“日本”这一主题——如同一根红线贯穿在各项演出之中。",
                "clozeWords": ["Veranstaltungen", "konkurrieren", "Aufmerksamkeit", "Faden"],
                "vocab": [
                    v("konkurrieren", "Verb", "竞争，角逐（um + A）", "Zahlreiche Bühnen konkurrieren gleichzeitig um das Publikum.", "多个舞台同时竞争观众的注意力。"),
                    v("sich wie ein roter Faden durch etwas ziehen", "Ausdruck", "像一条红线般贯穿始终", "Dieses Motiv zieht sich wie ein roter Faden durch den gesamten Roman.", "这一主题如同一条红线贯穿整部小说。"),
                ],
            },
            {
                "chinese": "另外两大亮点是位于民族学博物馆公园内的“世界花园”——在这里可以欣赏到来自全球各地的音乐，既有现场演奏也有黑胶DJ打碟。",
                "clozeWords": ["Höhepunkte", "Völkerkunde", "Plattenteller"],
                "vocab": [
                    v("der Höhepunkt", "Nomen", "亮点，高潮，顶点", "Das Abendkonzert bildete den Höhepunkt des Festivals.", "晚间音乐会构成了文化节的高潮亮点。", plural="die Höhepunkte"),
                ],
            },
            {
                "chinese": "市属艺术影院里还将不间断放映经典动画角色“线条先生（La Linea）”的动画全集——除此之外，尽情随心漫步感受节日氛围就好。",
                "clozeWords": ["Zeichentrickprogramm", "Kultfigur", "treiben"],
                "vocab": [
                    v("sich treiben lassen", "Ausdruck", "随心漫步，随遇而安地享受时光", "Auf dem Straßenfest lässt man sich am besten einfach treiben.", "逛街头节日时，最惬意的就是随意走走停停。"),
                ],
            },
        ],
    },
    "telc-c1-wg-studium-01": {
        "topic": "Studium & Wohnen",
        "segments": [
            {
                "chinese": "我上大学一开始在找房子、找房间这件事上还相当天真幼稚。",
                "clozeWords": ["Beginn", "Studiums", "ziemlich", "betrifft"],
                "vocab": [
                    v("betreffen", "Verb", "涉及，关乎（常用固定结构：was ... betrifft）", "Was die Pünktlichkeit betrifft, ist die Bahn leider unzuverlässig.", "就准点率而言，铁路确实不太可靠。"),
                ],
            },
            {
                "chinese": "临近开学前不久我才开始找房子——当时我一心只想一个人独居。",
                "clozeWords": ["Semesterbeginn", "unbedingt", "alleine"],
                "vocab": [
                    v("der Semesterbeginn", "Nomen", "学期伊始，开学", "Kurz vor Semesterbeginn steigt die Nachfrage nach Zimmern stark an.", "每逢临近开学，学生租房需求便会激增。"),
                ],
            },
            {
                "chinese": "然而我对科隆的房租水平完全抱有不切实际的幻想，很快便不得不认清一个事实：我根本负担不起。",
                "clozeWords": ["Vorstellungen", "Höhe", "Mieten", "feststellen"],
                "vocab": [
                    v("sich etwas leisten können", "Ausdruck", "在经济上负担得起某物", "Eine Wohnung in der Innenstadt können sich nur wenige Studierende leisten.", "几乎没有多少学生负担得起市中心的公寓。"),
                ],
            },
            {
                "chinese": "等我去大学的住房中介处求助时，工作人员也完全没有给我很快能分到房间的希望。",
                "clozeWords": ["Zimmervermittlung", "Mitarbeiterin", "Hoffnung"],
                "vocab": [
                    v("die Zimmervermittlung", "Nomen", "（大学等的）宿舍与租房中介服务", "Die Zimmervermittlung hilft Erstsemestern bei der Suche.", "高校租房中介处帮助新生寻找住处。", plural="die Zimmervermittlungen"),
                ],
            },
            {
                "chinese": "于是我算是迫不得已搬进了一间合租公寓（WG）；当时我对合租简直毫无好感——但如今我必须承认，我再也无法想象自己一个人住了。",
                "clozeWords": ["notgedrungen", "Wohngemeinschaft", "überzeugt", "vorstellen"],
                "vocab": [
                    v("notgedrungen", "Adverb", "迫不得已地，无奈地", "Weil die Preise stiegen, musste er notgedrungen umziehen.", "由于房租上涨，他迫不得已只能搬家。"),
                    v("die Wohngemeinschaft", "Nomen", "合租公寓（简称 WG）", "In einer Wohngemeinschaft teilt man sich Küche und Bad.", "合租公寓里大家共用厨房和卫生间。", plural="die Wohngemeinschaften"),
                ],
            },
            {
                "chinese": "合租实在太有意思了，而且当然也比独居便宜得多；这么看来我当年反而算因祸得福，因为如果是自愿选择，我大概绝不会去尝试合租。",
                "clozeWords": ["natürlich", "günstiger", "freiwillig", "ausprobiert"],
                "vocab": [
                    v("so gesehen", "Ausdruck", "从这个角度来看，这么说来", "So gesehen war der Umweg eigentlich ein großer Vorteil.", "这么说来，当初的弯路反而成了一大优势。"),
                    v("freiwillig", "Adjektiv", "自愿的，主动的", "Sie übernahm diese Aufgabe völlig freiwillig.", "她完全是自愿承担这项任务的。"),
                ],
            },
        ],
    },
    "telc-c1-mathe-interview-02": {
        "topic": "Wissenschaft & Forschung",
        "segments": [
            {
                "chinese": "这样的幸福瞬间我每天都能体验到，我在许多其他人身上也观察到了同样现象。",
                "clozeWords": ["Glücksmomente", "täglich", "beobachte"],
                "vocab": [
                    v("der Glücksmoment", "Nomen", "幸福瞬间，欣喜时刻", "Kleine Erfolge im Alltag bescheren echte Glücksmomente.", "日常生活中的小小成功会带来真正的幸福感。", plural="die Glücksmomente"),
                ],
            },
            {
                "chinese": "每当人们想在数学中探究出点名堂——无论是脑筋急转弯、拼图游戏，还是真正的前沿科研课题——起初往往根本不知道该从何下手。",
                "clozeWords": ["herauskriegen", "Knobelaufgabe", "Forschungsthemen", "zunächst"],
                "vocab": [
                    v("herauskriegen", "Verb", "弄明白，解开，查出（口语）", "Nach langem Nachdenken habe ich das Rätsel herausgekriegt.", "苦思冥想之后，我终于解开了这道谜题。"),
                    v("die Knobelaufgabe", "Nomen", "益智思考题，烧脑难题", "Mathematiker lieben knifflige Knobelaufgaben zum Nachdenken.", "数学家喜欢动脑筋的烧脑谜题。", plural="die Knobelaufgaben"),
                ],
            },
            {
                "chinese": "常常需要很长时间才能显现出成果，然后突然间出人意料地，那个让你豁然开朗、发现其实一切竟如此简单的瞬间就降临了。",
                "clozeWords": ["Erfolg", "plötzlich", "unerwartet", "letztlich"],
                "vocab": [
                    v("unerwartet", "Adjektiv", "出乎意料的，突然的", "Die Lösung erschien völlig unerwartet nach Wochen der Arbeit.", "历经数周研究后，解法出人意料地浮现出来。"),
                    v("letztlich", "Adverb", "归根结底，最终", "Letztlich zählt die Klarheit des mathematischen Beweises.", "归根结底，数学证明的清晰严谨才是最重要的。"),
                ],
            },
            {
                "chinese": "而这种脑袋里“叮”一声顿悟的瞬间——正是幸福所在，因为人类生来如此：只要哪怕理解了世界运转机制的微末一角，就会感到满足和快乐。",
                "clozeWords": ["zufrieden", "glücklich", "verstehen", "funktioniert"],
                "vocab": [
                    v("es macht klick", "Ausdruck", "突然“咔哒”顿悟，豁然开朗", "Als das Prinzip erklärt wurde, machte es plötzlich klick.", "当原理一被讲明，我脑子里突然灵光一闪顿悟了。"),
                ],
            },
        ],
    },
    "telc-c1-literatur-daf-03": {
        "topic": "Bildung & Literatur",
        "segments": [
            {
                "chinese": "阅读是社会生活中的头号核心素养能力——尤其是在这样一个高度媒介化的世界里。",
                "clozeWords": ["Schlüsselqualifikation", "medial", "vermittelten"],
                "vocab": [
                    v("die Schlüsselqualifikation", "Nomen", "核心素质能力，关键技能", "Teamfähigkeit gilt im Beruf als wichtige Schlüsselqualifikation.", "团队协作能力在职场上被视为重要核心素养。", plural="die Schlüsselqualifikationen"),
                    v("medial vermittelt", "Ausdruck", "通过媒介中介传达的", "Unsere Realität wird heute stark medial vermittelt.", "我们如今感知的现实在很大程度上经由媒介传播。"),
                ],
            },
            {
                "chinese": "阅读不仅培养理解各类文本、利用信息及反思思考的能力；阅读能力更是实现个人与职业目标的重要辅助工具。",
                "clozeWords": ["Fähigkeit", "reflektieren", "Lesekompetenz", "Hilfsmittel"],
                "vocab": [
                    v("reflektieren", "Verb", "反思，深思熟虑；反射", "Studierende lernen, Quellen kritisch zu reflektieren.", "大学生学习批判性地反思信息来源。"),
                    v("die Lesekompetenz", "Nomen", "阅读理解素养，阅读能力", "Gezielte Förderung stärkt die Lesekompetenz schon im Grundschulalter.", "有针对性的培养从小学阶段就能夯实阅读能力。"),
                ],
            },
            {
                "chinese": "“国际小学阅读素养调查”（简称IGLU）表明，德国小学的阅读教学中依然由传统方法占据主导地位。",
                "clozeWords": ["Leseunterricht", "herkömmliche", "Methoden", "dominieren"],
                "vocab": [
                    v("herkömmlich", "Adjektiv", "传统的，一贯常用的", "Herkömmliche Lehrmethoden reichen allein oft nicht mehr aus.", "传统教学方法单靠自身往往已经不够用。"),
                    v("dominieren", "Verb", "占主导地位，支配", "Frontalunterricht darf moderne Seminare nicht länger dominieren.", "单向讲授式教学不应再主导现代研讨课。"),
                ],
            },
            {
                "chinese": "而富有启发性的教学形式——譬如让学生亲自撰写文本或对所读内容进行创意加工——却依然十分罕见。",
                "clozeWords": ["Anregende", "Verfassen", "kreative", "hingegen"],
                "vocab": [
                    v("anregend", "Adjektiv", "富有启发性的，引人思考的", "Die Diskussion lieferte viele anregende Impulse für den Unterricht.", "这场讨论为教学带来了众多富有启发的灵感。"),
                    v("verfassen", "Verb", "撰写，编写（文本/报告）", "Im Kurs verfassen die Teilnehmenden kurze eigene Essays.", "课程上学员们自己动手撰写短篇随笔。"),
                ],
            },
            {
                "chinese": "然而如今人们恰恰必须运用富有创造力的方法，去激发学生对阅读的热爱，并将他们的真实生活经验融入到课堂教学之中。",
                "clozeWords": ["einsetzen", "begeistern", "Lebenserfahrung", "einzubinden"],
                "vocab": [
                    v("einbinden", "Verb", "融入，纳入其中", "Die Lernenden sollen aktiv in das Projekt eingebunden werden.", "应当让学生们积极参与融入到项目中。"),
                    v("begeistern", "Verb", "使着迷，激起……的热情（für + A）", "Mit kreativen Ideen kann man Kinder wieder fürs Lesen begeistern.", "凭借创意点子就能重新激发孩子们对阅读的热情。"),
                ],
            },
        ],
    },
}
