# -*- coding: utf-8 -*-
"""
Curated Chinese translations, clozeWords, vocab items, and normalized topics
for Tracks 01-11 (6 Nachrichtenleicht + 5 Slow German).
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


CURRICULUM_A = {
    "nl-die-ukraine-hat-eine-wichtige-kr": {
        "topic": "Politik & Weltgeschehen",
        "segments": [
            {
                "chinese": "乌克兰摧毁了俄罗斯通往克里米亚的一座重要大桥。乌克兰正在经历战争，多年来一直在抵抗俄罗斯。",
                "clozeWords": ["wichtige", "Krieg", "verteidigt"],
                "vocab": [
                    v("kaputt machen", "Ausdruck", "损坏，摧毁（口语/浅易表达）", "Der Sturm hat viele Dächer kaputt gemacht.", "暴风雨损坏了许多屋顶。"),
                    v("der Krieg", "Nomen", "战争", "Seit Jahren leidet das Land unter dem Krieg.", "这个国家多年来一直饱受战争之苦。", plural="die Kriege"),
                    v("sich verteidigen", "Verb", "自卫，防御，保卫自己", "Die Stadt konnte sich erfolgreich verteidigen.", "这座城市成功地保卫了自己。"),
                ],
            },
            {
                "chinese": "如今乌克兰用导弹击中了一座重要的桥梁。这座桥从俄罗斯通向克里米亚半岛。",
                "clozeWords": ["Raketen", "getroffen", "führt"],
                "vocab": [
                    v("die Rakete", "Nomen", "导弹，火箭", "Die Rakete flog über das Meer.", "导弹飞越大海。", plural="die Raketen"),
                    v("treffen", "Verb", "击中，遇见", "Der Ball hat genau das Tor getroffen.", "球正好击中了球门。"),
                    v("die Halbinsel", "Nomen", "半岛", "Die Krim liegt auf einer Halbinsel am Schwarzen Meer.", "克里米亚位于黑海的一座半岛上。", plural="die Halbinseln"),
                ],
            },
            {
                "chinese": "克里米亚属于乌克兰。然而俄罗斯在2014年向克里米亚派遣了士兵并占领了该地区，因此乌克兰也对克里米亚发动袭击。",
                "clozeWords": ["gehört", "Soldaten", "besetzt"],
                "vocab": [
                    v("gehören", "Verb", "属于（+ 第三格）", "Diese Tasche gehört meiner Schwester.", "这个包是我妹妹的。"),
                    v("besetzen", "Verb", "占领，占据", "Fremde Truppen haben die Region besetzt.", "外国军队占领了该地区。"),
                    v("angreifen", "Verb", "进攻，袭击", "Im Morgengrauen griffen die Truppen an.", "部队在黎明时分发动了进攻。"),
                ],
            },
            {
                "chinese": "长期以来，克里米亚与俄罗斯本土之间没有陆路连接。2018年俄罗斯修建了这座通往克里米亚的大桥。",
                "clozeWords": ["Verbindung", "gebaut"],
                "vocab": [
                    v("das Festland", "Nomen", "大陆，本土", "Vom Festland fährt eine Fähre zur Insel.", "从本土有一班渡轮开往海岛。"),
                    v("die Verbindung", "Nomen", "连接，交通线路，联系", "Es gibt eine schnelle Zugverbindung zwischen beiden Städten.", "这两座城市之间有高速列车连接。", plural="die Verbindungen"),
                ],
            },
            {
                "chinese": "许多人表示，这座桥对俄罗斯来说是一个重要象征，旨在表明“克里米亚属于俄罗斯”。",
                "clozeWords": ["wichtiges", "Symbol", "zeigen"],
                "vocab": [
                    v("das Symbol", "Nomen", "象征，符号", "Die Taube gilt weltweit als Symbol des Friedens.", "鸽子在世界各地被视为和平的象征。", plural="die Symbole"),
                ],
            },
            {
                "chinese": "现在乌克兰破坏了桥面道路。俄军原本通过这座桥向克里米亚和乌克兰南部的士兵运送武器及其他物资。乌克兰方面希望：那里的俄军此后或许将难以再有效防守。",
                "clozeWords": ["Militär", "Waffen", "hofft"],
                "vocab": [
                    v("das Militär", "Nomen", "军队，军方", "Das Militär sicherte die Straßen ab.", "军方封锁并守卫了道路。"),
                    v("die Waffe", "Nomen", "武器", "Schwere Waffen dürfen nicht transportiert werden.", "禁止运输重型武器。", plural="die Waffen"),
                    v("hoffen", "Verb", "希望，期盼", "Wir hoffen auf eine baldige Einigung.", "我们希望尽快达成协议。"),
                ],
            },
        ],
    },
    "nl-viele-menschen-mit-psychischen-e": {
        "topic": "Psychologie & Arbeit",
        "segments": [
            {
                "chinese": "许多患有精神疾病的人在工作场所遭到歧视。",
                "clozeWords": ["psychischen", "diskriminiert"],
                "vocab": [
                    v("psychisch", "Adjektiv", "心理的，精神的", "Psychische Gesundheit ist genauso wichtig wie körperliche.", "心理健康与身体健康同样重要。"),
                    v("diskriminieren", "Verb", "歧视，不公正对待", "Niemand darf wegen seines Alters diskriminiert werden.", "任何人都不得因年龄而受到歧视。"),
                ],
            },
            {
                "chinese": "许多有心理或精神疾病的人曾在工作岗位上受到过歧视。",
                "clozeWords": ["Erkrankung", "Arbeits-Platz"],
                "vocab": [
                    v("die Erkrankung", "Nomen", "疾病，患病", "Bei einer schweren Erkrankung sollte man einen Arzt aufsuchen.", "如果患上重病应当就医。", plural="die Erkrankungen"),
                    v("der Arbeitsplatz", "Nomen", "工作岗位，工作场所", "Ein ruhiger Arbeitsplatz fördert die Konzentration.", "安静的工作环境有助于集中注意力。", plural="die Arbeitsplätze"),
                ],
            },
            {
                "chinese": "这是德国联邦反歧视局调查发现的结果。",
                "clozeWords": ["herausgefunden"],
                "vocab": [
                    v("herausfinden", "Verb", "查明，调查发现", "Die Forscher konnten die Ursache schnell herausfinden.", "研究人员很快查明了原因。"),
                ],
            },
            {
                "chinese": "该机构对数千名患有精神疾病的人士进行了问卷访问。",
                "clozeWords": ["tausende", "befragt"],
                "vocab": [
                    v("befragen", "Verb", "询问，做调查访问", "Für die Studie wurden über tausend Bürger befragt.", "该研究调查了一千多名市民。"),
                ],
            },
            {
                "chinese": "精神疾病包括抑郁症、焦虑症或成瘾症等。",
                "clozeWords": ["Depression", "Angst-Störung", "Sucht"],
                "vocab": [
                    v("die Depression", "Nomen", "抑郁症", "Eine Depression lässt sich heute oft gut behandeln.", "如今抑郁症通常可以得到良好治疗。", plural="die Depressionen"),
                    v("die Angststörung", "Nomen", "焦虑症，焦虑障碍", "Therapien helfen Menschen mit einer Angststörung.", "心理治疗有助于焦虑症患者。", plural="die Angststörungen"),
                    v("die Sucht", "Nomen", "成瘾，嗜好", "Hilfsangebote unterstützen Menschen im Kampf gegen die Sucht.", "援助项目支持人们对抗成瘾问题。", plural="die Süchte"),
                ],
            },
            {
                "chinese": "近半数受访的精神疾病患者表示：我曾因自己的病情在工作中遭到歧视。",
                "clozeWords": ["Hälfte", "Befragten", "Krankheit"],
                "vocab": [
                    v("die Hälfte", "Nomen", "一半，半数", "Fast die Hälfte des Teams arbeitet im Homeoffice.", "团队近一半人在居家办公。", plural="die Hälften"),
                ],
            },
            {
                "chinese": "比如曾有人对这些患者说：你因为生病而工作干不好。",
                "clozeWords": ["Arbeit", "wegen"],
                "vocab": [
                    v("wegen", "Ausdruck", "因为，由于（介词，常接第二格）", "Wegen des Regens blieb das Museum länger offen.", "由于下雨，博物馆延长了开放时间。"),
                ],
            },
            {
                "chinese": "有时甚至还会拿这些人开玩笑嘲讽。",
                "clozeWords": ["Witze", "gemacht"],
                "vocab": [
                    v("der Witz", "Nomen", "笑话，玩笑", "Über ernste Themen sollte man keine schlechten Witze machen.", "对严肃话题不该开恶劣的玩笑。", plural="die Witze"),
                ],
            },
            {
                "chinese": "因此，许多人宁愿隐瞒自己的病情。",
                "clozeWords": ["verstecken", "deshalb", "lieber"],
                "vocab": [
                    v("verstecken", "Verb", "隐藏，隐瞒", "Viele verstecken ihre Gefühle hinter einem Lächeln.", "许多人把情绪藏在微笑背后。"),
                ],
            },
            {
                "chinese": "然而，这样做有时反而会让病情变得更加严重。",
                "clozeWords": ["dadurch", "schlimmer"],
                "vocab": [
                    v("schlimm", "Adjektiv", "严重的，糟糕的", "Ohne Behandlung können die Schmerzen schlimmer werden.", "如果不经治疗，疼痛可能会加重。"),
                ],
            },
        ],
    },
    "nl-der-schauspieler-robert-pattinso": {
        "topic": "Kultur & Medien",
        "segments": [
            {
                "chinese": "演员罗伯特·帕丁森将成为新一任“詹姆斯·邦德”。詹姆斯·邦德是一位家喻户晓的电影角色，这位秘密特工此前已由多位演员扮演过。",
                "clozeWords": ["Schauspieler", "bekannte", "gespielt"],
                "vocab": [
                    v("der Schauspieler", "Nomen", "男演员", "Der Schauspieler erhielt großen Applaus für seine Rolle.", "这位演员因其饰演的角色赢得了热烈掌声。", plural="die Schauspieler"),
                    v("der Geheimagent", "Nomen", "秘密特工，间谍", "In dem Film arbeitet die Hauptfigur als Geheimagent.", "电影的主角是一名秘密特工。", plural="die Geheimagenten"),
                ],
            },
            {
                "chinese": "如今新任詹姆斯·邦德的人选已经敲定：正是演员罗伯特·帕丁森。帕丁森来自英国。",
                "clozeWords": ["entschieden", "kommt"],
                "vocab": [
                    v("entscheiden", "Verb", "决定，裁决", "Die Jury hat über den besten Film entschieden.", "评委会选出了最佳影片。"),
                ],
            },
            {
                "chinese": "他今年40岁，最初凭借《暮光之城》系列电影中的吸血鬼一角成名。他近期还参演了《奥德赛》和《蝙蝠侠》等影片。",
                "clozeWords": ["Rolle", "bekannt", "mitgespielt"],
                "vocab": [
                    v("die Rolle", "Nomen", "角色", "Sie spielt eine wichtige Rolle im neuen Theaterstück.", "她在这部新戏剧中担任重要角色。", plural="die Rollen"),
                    v("mitspielen", "Verb", "参演，参与（游戏/比赛）", "In diesem Film spielen viele bekannte Stars mit.", "这部电影有很多知名明星参演。"),
                ],
            },
            {
                "chinese": "电影专家表示：帕丁森常常会赋予角色某种独特的气质，詹姆斯·邦德这一角色也可能会这样。过去詹姆斯·邦德一直被塑造成一位主要只对女性和汽车感兴趣的冷酷男人。",
                "clozeWords": ["Besonderes", "bisher", "interessiert"],
                "vocab": [
                    v("der Experte", "Nomen", "专家，行家", "Laut Experten wird der Film ein großer Erfolg.", "据专家称，这部电影将会大获成功。", plural="die Experten"),
                    v("sich interessieren", "Verb", "对……感兴趣（für + A）", "Er interessiert sich sehr für europäische Filmgeschichte.", "他对欧洲电影史很感兴趣。"),
                ],
            },
            {
                "chinese": "很多人认为这种形象带有性别歧视色彩。部分影迷相信，帕丁森或许会塑造一个更加敏感脆弱的詹姆斯·邦德。由罗伯特·帕丁森主演的第一部邦德电影预计将于2028年制作完成。",
                "clozeWords": ["sexistisch", "verletzlicheren", "wahrscheinlich"],
                "vocab": [
                    v("sexistisch", "Adjektiv", "性别歧视的", "Alte Werbespots wirken heute oft sexistisch.", "一些老式广告在今天看来往往带有性别歧视。"),
                    v("verletzlich", "Adjektiv", "脆弱的，易受伤害的", "Im Gespräch zeigte er auch seine verletzliche Seite.", "交谈中他也展现出了自己脆弱的一面。"),
                ],
            },
        ],
    },
    "nl-britischer-regierungs-chef-burnh": {
        "topic": "Politik & Weltgeschehen",
        "segments": [
            {
                "chinese": "英国首相伯纳姆表示：退出欧盟并不成功。英国已在六年前正式退出了欧盟。",
                "clozeWords": ["Regierungs-Chef", "Erfolg", "ausgetreten"],
                "vocab": [
                    v("der Regierungschef", "Nomen", "政府首脑，首相/总理", "Der Regierungschef hielt eine Rede im Parlament.", "政府首脑在议会发表了演讲。", plural="die Regierungschefs"),
                    v("austreten", "Verb", "退出（组织等）", "Nach langen Debatten trat das Land aus dem Bündnis aus.", "经过漫长辩论，该国退出了联盟。"),
                ],
            },
            {
                "chinese": "这就是所谓的“英国脱欧”。长久以来人们一直在追问：这对英国有益吗？新任首相安迪·伯纳姆认为：脱欧是一次失败。",
                "clozeWords": ["immer", "meint", "Misserfolg"],
                "vocab": [
                    v("der Misserfolg", "Nomen", "失败，挫折", "Trotz großer Mühe endete das Projekt als Misserfolg.", "尽管付出了很大努力，项目还是以失败告终。", plural="die Misserfolge"),
                ],
            },
            {
                "chinese": "伯纳姆表示：英国失去的比得到的更多。我们并没有对进入英国的移民获得更强的控制权。",
                "clozeWords": ["verloren", "gewonnen", "Kontrolle", "einwandert"],
                "vocab": [
                    v("die Kontrolle", "Nomen", "控制，管制，检查", "An der Grenze gibt es strengere Kontrollen.", "边境实行更严格的检查。", plural="die Kontrollen"),
                    v("einwandern", "Verb", "移入，移民入境", "Viele Fachkräfte möchten nach Europa einwandern.", "许多专业人才希望移民到欧洲。"),
                ],
            },
            {
                "chinese": "脱欧也损害了英国经济。因此伯纳姆希望再次与欧盟展开谈判。",
                "clozeWords": ["Wirtschaft", "geschadet", "verhandeln"],
                "vocab": [
                    v("schaden", "Verb", "损害，危害（+ 第三格）", "Hohe Zölle können der Wirtschaft stark schaden.", "高关税可能会严重损害经济。"),
                    v("verhandeln", "Verb", "谈判，协商", "Beide Seiten verhandeln über neue Regeln.", "双方正在就新规则进行谈判。"),
                ],
            },
            {
                "chinese": "例如他希望让英国与欧盟之间的贸易再次变得更加便利。此外，应当让年轻人在欧盟与英国之间求学和工作重新变得更容易。",
                "clozeWords": ["Handel", "einfacher", "studieren"],
                "vocab": [
                    v("der Handel", "Nomen", "贸易，商业", "Der internationale Handel schafft viele Arbeitsplätze.", "国际贸易创造了大量就业岗位。"),
                ],
            },
        ],
    },
    "nl-sexuelle-uebergriffe-franzoesisc": {
        "topic": "Gesellschaft & Recht",
        "segments": [
            {
                "chinese": "性侵害指控：法国演员热拉尔·德帕迪约请求原谅。热拉尔·德帕迪约是一位来自法国的著名演员。",
                "clozeWords": ["Übergriffe", "Entschuldigung", "berühmter"],
                "vocab": [
                    v("der Übergriff", "Nomen", "侵犯，侵害，袭击行为", "Solche Übergriffe werden konsequent angezeigt.", "此类侵害行为会依法遭到举报。", plural="die Übergriffe"),
                    v("um Entschuldigung bitten", "Ausdruck", "请求原谅，道歉", "Er hat öffentlich um Entschuldigung gebeten.", "他已经公开道歉。"),
                ],
            },
            {
                "chinese": "多名女性称：德帕迪约曾对我们实施性骚扰。如今德帕迪约首次请求谅解。",
                "clozeWords": ["Mehrere", "belästigt", "gebeten"],
                "vocab": [
                    v("belästigen", "Verb", "骚扰，纠缠", "Niemand darf am Arbeitsplatz belästigt werden.", "任何人在工作场所都不得受到骚扰。"),
                ],
            },
            {
                "chinese": "不过一名受害女性表示：我不知道德帕迪约的道歉是否真诚，因为他并没有亲自当面道歉。",
                "clozeWords": ["betroffene", "ernst", "persönlich"],
                "vocab": [
                    v("betroffen", "Adjektiv", "受影响的，涉事的，感到震惊的", "Die betroffenen Personen erhielten rechtliche Beratung.", "涉事人员获得了法律咨询帮助。"),
                    v("etwas ernst meinen", "Ausdruck", "认真对待某事，不是开玩笑", "Meinst du dieses Angebot wirklich ernst?", "你提出这个建议是认真的吗？"),
                ],
            },
            {
                "chinese": "是由他人代他在庭上宣读了这份道歉声明。这一幕发生在因性骚扰而审理的一起司法诉讼程序中。",
                "clozeWords": ["vorgelesen", "Gerichts-Verfahren"],
                "vocab": [
                    v("vorlesen", "Verb", "大声朗读，宣读", "Die Anwältin las den Brief im Saal vor.", "女律师在法庭内宣读了这封信。"),
                    v("das Gerichtsverfahren", "Nomen", "司法程序，诉讼程序", "Das Gerichtsverfahren dauerte mehrere Monate.", "这起诉讼持续了几个月。", plural="die Gerichtsverfahren"),
                ],
            },
            {
                "chinese": "两名女性表示：2021年拍摄工作期间，德帕迪约曾触碰我们的胸部和臀部。德帕迪约回应称：我本意并不想伤害这两位女性。",
                "clozeWords": ["Dreh-Arbeiten", "angefasst", "verletzen"],
                "vocab": [
                    v("die Dreharbeiten", "Nomen", "电影/电视拍摄工作（常用复数）", "Die Dreharbeiten finden in Paris statt.", "拍摄工作正在巴黎进行。"),
                    v("anfassen", "Verb", "触摸，触碰", "Bitte die empfindlichen Kunstwerke nicht anfassen!", "请勿触摸脆弱的艺术品！"),
                ],
            },
            {
                "chinese": "“但她们感到了受伤。这一点我理解，因此我接受判决。” 法院判处的刑罚是18个月缓刑监禁。",
                "clozeWords": ["verstanden", "Strafe", "Bewährung"],
                "vocab": [
                    v("die Strafe", "Nomen", "惩罚，刑罚，罚款", "Für das Vergehen droht eine hohe Geldstrafe.", "这一违法行为可能面临高额罚款。", plural="die Strafen"),
                    v("die Haft auf Bewährung", "Ausdruck", "缓刑监禁", "Das Gericht verhängte eine Haftstrafe auf Bewährung.", "法院判处了缓刑。"),
                ],
            },
        ],
    },
    "nl-mecklenburg-vorpommern-manuela-s": {
        "topic": "Politik & Gesellschaft",
        "segments": [
            {
                "chinese": "梅克伦堡-前波美拉尼亚州：来自社民党（SPD）的曼努埃拉·施韦西希再次当选州长。曼努埃拉·施韦西希将继续担任梅前州州长。",
                "clozeWords": ["wiedergewählt", "Minister-Präsidentin", "Bundes-Land"],
                "vocab": [
                    v("der Ministerpräsident", "Nomen", "（德国联邦州的）州长", "Die Ministerpräsidentin leitete die Kabinettssitzung.", "女州长主持了内阁会议。", plural="die Ministerpräsidenten"),
                    v("das Bundesland", "Nomen", "联邦州", "Deutschland besteht aus sechzehn Bundesländern.", "德国由十六个联邦州组成。", plural="die Bundesländer"),
                ],
            },
            {
                "chinese": "州议会再次选举施韦西希连任。施韦西希隶属于德国社会民主党，社民党计划与左翼党及绿党共同联合执政。",
                "clozeWords": ["Landtag", "Partei", "regieren"],
                "vocab": [
                    v("der Landtag", "Nomen", "州议会", "Im Landtag werden neue Landesgesetze beschlossen.", "新州法将在州议会表决通过。", plural="die Landtage"),
                    v("regieren", "Verb", "执政，治理", "Drei Parteien wollen das Land gemeinsam regieren.", "三个政党计划共同组阁执政。"),
                ],
            },
            {
                "chinese": "当选后施韦西希进行了宣誓就职。这意味着：她郑重承诺将尽最大努力履行政府首脑的职责。",
                "clozeWords": ["vereidigt", "bedeutet", "versprochen"],
                "vocab": [
                    v("vereidigen", "Verb", "使宣誓就职", "Die neue Ministerin wurde am Vormittag vereidigt.", "新任部长于上午宣誓就职。"),
                    v("versprechen", "Verb", "承诺，答应", "Sie hat schnelle Verbesserungen versprochen.", "她承诺尽快推进改善。"),
                ],
            },
            {
                "chinese": "各位部长也一同宣誓就职。其中5位来自社民党，2位来自左翼党，还有1位女部长来自绿党。",
                "clozeWords": ["Ministerinnen", "kommen"],
                "vocab": [
                    v("der Minister", "Nomen", "部长，大臣", "Der Minister präsentierte den neuen Haushaltsplan.", "部长提交了新的预算案。", plural="die Minister"),
                ],
            },
            {
                "chinese": "州议会中唯一的反对党是德国选择党（AfD）。该党在9月的州选举中获得了最多选票，但没有任何其他政党愿意与选择党合作执政。",
                "clozeWords": ["Oppositions-Partei", "Stimmen", "zusammen"],
                "vocab": [
                    v("die Opposition", "Nomen", "反对派，在野党", "Die Opposition kritisierte den Vorschlag scharf.", "在野党严厉批评了这一提案。", plural="die Oppositionen"),
                    v("die Stimme", "Nomen", "选票，声音", "Jede einzelne Stimme zählt bei dieser Wahl.", "在这次选举中每一张选票都很关键。", plural="die Stimmen"),
                ],
            },
        ],
    },
    "sg-expats-in-deutschland-sg-327": {
        "topic": "Arbeit & Gesellschaft",
        "segments": [
            {
                "chinese": "诚然，“Expat”（外派人员/外籍专才）并不是一个德语词。",
                "clozeWords": ["Zugegeben", "deutsches", "Wort"],
                "vocab": [
                    v("zugegeben", "Adverb", "诚然，不得不承认", "Zugegeben, das Thema ist am Anfang nicht leicht.", "诚然，这个话题一开始并不简单。"),
                ],
            },
            {
                "chinese": "它对应的德语表达或许可以是“外来技术工人”。",
                "clozeWords": ["vielleicht", "zugewanderte", "Facharbeiter"],
                "vocab": [
                    v("der Facharbeiter", "Nomen", "技术工人，专业技工", "Viele Firmen suchen dringend qualifizierte Facharbeiter.", "许多企业急需高素质技术工人。", plural="die Facharbeiter"),
                ],
            },
            {
                "chinese": "不过这个词太复杂绕口了，对吧？",
                "clozeWords": ["kompliziert"],
                "vocab": [
                    v("kompliziert", "Adjektiv", "复杂的，棘手的", "Bitte erklären Sie die Regel weniger kompliziert.", "请把规则解释得不要这么复杂。"),
                ],
            },
            {
                "chinese": "那我们还是沿用“Expat”这个词吧。",
                "clozeWords": ["Bleiben"],
                "vocab": [
                    v("bei etwas bleiben", "Ausdruck", "坚持，继续沿用某事物", "Bleiben wir bei unserem ursprünglichen Plan.", "我们还是按原计划推进吧。"),
                ],
            },
            {
                "chinese": "在德国当我们谈起“Expats”时，通常指那些为了工作而移居到另一个国家生活的人。",
                "clozeWords": ["sprechen", "meinen", "Arbeit", "ziehen"],
                "vocab": [
                    v("ziehen", "Verb", "迁居，搬家；拉", "Nächsten Monat zieht die Familie nach Hamburg.", "下个月这家人将搬到汉堡。"),
                ],
            },
        ],
    },
    "sg-wiedereinfuehrung-der-wehrpfli": {
        "topic": "Politik & Gesellschaft",
        "segments": [
            {
                "chinese": "德国很快又要恢复普遍义务兵役制了吗？",
                "clozeWords": ["bald", "Wehrpflicht", "Deutschland"],
                "vocab": [
                    v("die Wehrpflicht", "Nomen", "义务兵役制", "In einigen Ländern gilt weiterhin eine Wehrpflicht.", "在一些国家至今仍实行义务兵役制。"),
                ],
            },
            {
                "chinese": "我今年刚刚年满50岁。",
                "clozeWords": ["dieses", "Jahr", "geworden"],
                "vocab": [
                    v("werden", "Verb", "成为，变为（年龄增长）", "Im Oktober wird mein Bruder dreißig Jahre alt.", "今年十月我哥哥就满三十岁了。"),
                ],
            },
            {
                "chinese": "在我还是一名刚步入社会的年轻人时，男性“入伍服役”或从事社会替代役（民役）是再正常不过的事。",
                "clozeWords": ["Erwachsene", "normal", "Zivildienst"],
                "vocab": [
                    v("der Zivildienst", "Nomen", "社会替代役，民役", "Früher leisteten viele junge Männer statt des Militärs Zivildienst.", "过去许多年轻男子选择用社会民役代替兵役。"),
                ],
            },
            {
                "chinese": "这意味着，我那一代的年轻男性必须履行大约一年的兵役义务。",
                "clozeWords": ["bedeutet", "Generation", "ungefähr", "Militärdienst"],
                "vocab": [
                    v("die Generation", "Nomen", "一代人", "Jede Generation erlebt den technischen Wandel anders.", "每一代人对技术变革的体验各不相同。", plural="die Generationen"),
                    v("einen Dienst leisten", "Ausdruck", "履行义务，服役", "Er hat ein freiwilliges soziales Jahr geleistet.", "他参加了一年的志愿社会服务。"),
                ],
            },
            {
                "chinese": "在那段时间里，他们就是军人。",
                "clozeWords": ["dieser", "Zeit", "Soldaten"],
                "vocab": [
                    v("der Soldat", "Nomen", "士兵，军人", "Die Soldaten halfen beim Hochwasserschutz.", "士兵们协助开展了防洪救灾。", plural="die Soldaten"),
                ],
            },
        ],
    },
    "sg-social-media-fuer-jugendliche": {
        "topic": "Digitales & Medien",
        "segments": [
            {
                "chinese": "要为青少年出台社交媒体禁令吗？",
                "clozeWords": ["Jugendliche"],
                "vocab": [
                    v("das Verbot", "Nomen", "禁令，禁止", "Über ein solches Verbot wird intensiv diskutiert.", "各方正在就此类禁令展开激烈讨论。", plural="die Verbote"),
                ],
            },
            {
                "chinese": "核心问题在于：儿童和青少年到底应不应该被允许使用社交媒体？",
                "clozeWords": ["große", "Frage", "überhaupt", "nutzen"],
                "vocab": [
                    v("überhaupt", "Adverb", "究竟，到底；根本", "Hast du heute überhaupt Zeit für eine Pause?", "你今天到底有时间休息一下吗？"),
                    v("nutzen", "Verb", "利用，使用", "Viele Lernende nutzen digitale Plattformen täglich.", "许多学习者每天都使用数字平台。"),
                ],
            },
            {
                "chinese": "这场讨论并不新鲜——我自己也常常琢磨这个问题。",
                "clozeWords": ["Diskussion", "immer", "wieder"],
                "vocab": [
                    v("die Diskussion", "Nomen", "讨论，辩论", "Die Diskussion über den Datenschutz bleibt aktuell.", "关于数据保护的讨论依然极具现实意义。", plural="die Diskussionen"),
                ],
            },
            {
                "chinese": "但在最近几个月里，这个话题变得格外紧迫和受到关注。",
                "clozeWords": ["letzten", "Monaten", "aktuell"],
                "vocab": [
                    v("aktuell", "Adjektiv", "当前的，热门的，时下的", "Das Thema ist zurzeit sehr aktuell in den Medien.", "这个话题目前在媒体上非常热门。"),
                ],
            },
            {
                "chinese": "尤其是因为澳大利亚成为了全球第一个采取立法行动的国家。",
                "clozeWords": ["Besonders", "erstes", "gehandelt"],
                "vocab": [
                    v("handeln", "Verb", "行动，处理；涉及", "Die Regierung musste wegen der Krise schnell handeln.", "面对危机，政府必须迅速采取行动。"),
                ],
            },
        ],
    },
    "sg-tempolimit-in-deutschland-sg-3": {
        "topic": "Verkehr & Mobilität",
        "mergePairs": [(1, 2)],  # Combine 2s short sentence s2 with s3 cleanly!
        "segments": [
            {
                "chinese": "我还记得，我来自美国的表妹曾经来我家做客，当时她一心想亲眼看看著名的德国高速公路。",
                "clozeWords": ["Cousine", "Besuch", "unbedingt", "Autobahn"],
                "vocab": [
                    v("die Autobahn", "Nomen", "高速公路", "Auf deutschen Autobahnen gibt es viel Fernverkehr.", "德国高速公路上的长途车流量很大。", plural="die Autobahnen"),
                    v("unbedingt", "Adverb", "一定，务必", "Du solltest diese Ausstellung unbedingt besuchen.", "你一定要去看看这个展览。"),
                ],
            },
            {
                "chinese": "结果她有些失望。她来自洛杉矶，那里动辄有十条车道的超级公路，一切都大得惊人。",
                "clozeWords": ["enttäuscht", "Straßen", "riesig"],
                "vocab": [
                    v("enttäuscht", "Adjektiv", "失望的，沮丧的", "Nach der Absage war er sehr enttäuscht.", "被拒绝后他感到非常失望。"),
                    v("riesig", "Adjektiv", "巨大的，庞大的", "Vor dem Gebäude steht ein riesiger Baum.", "大楼前矗立着一棵参天大树。"),
                ],
            },
            {
                "chinese": "而我带她看的那段高速公路只有双向两车道，看起来相当平淡无奇。",
                "clozeWords": ["gezeigt", "Spuren", "langweilig"],
                "vocab": [
                    v("die Spur", "Nomen", "车道，痕迹", "Bitte bleiben Sie im Stau auf Ihrer Spur.", "堵车时请保持在自己的车道内行驶。", plural="die Spuren"),
                ],
            },
            {
                "chinese": "但真正让人惊讶的事实是：在德国许多路段上并没有统一的最高限速。",
                "clozeWords": ["Strecken", "allgemeines", "Tempolimit"],
                "vocab": [
                    v("das Tempolimit", "Nomen", "最高限速", "Auf dieser Landstraße gilt ein Tempolimit von 80.", "这条乡村公路限速80公里每小时。", plural="die Tempolimits"),
                    v("die Strecke", "Nomen", "路段，距离，路程", "Die Strecke zwischen Berlin und Hamburg ist gut ausgebaut.", "柏林至汉堡之间的线路建设得很完善。", plural="die Strecken"),
                ],
            },
        ],
    },
    "sg-auf-wohnungssuche-in-deutschla": {
        "topic": "Wohnen & Lebensstile",
        "segments": [
            {
                "chinese": "柏林刚刚举行了地方选举。",
                "clozeWords": ["Berlin", "gerade", "gewählt"],
                "vocab": [
                    v("wählen", "Verb", "选举，投票；选择", "Alle Bürger dürfen ab achtzehn Jahren wählen.", "所有年满十八岁的公民均可投票。"),
                ],
            },
            {
                "chinese": "在这次选举中，“左翼党”的表现尤为强劲。",
                "clozeWords": ["stark", "Partei"],
                "vocab": [
                    v("die Partei", "Nomen", "政党", "Mehrere Parteien stellen ein neues Wahlprogramm vor.", "多个政党推出了新的竞选纲领。", plural="die Parteien"),
                ],
            },
            {
                "chinese": "他们在竞选中的核心议题是让民众负担得起的平价住房。",
                "clozeWords": ["Hauptthema", "Wahlkampf", "bezahlbares", "Wohnen"],
                "vocab": [
                    v("bezahlbar", "Adjektiv", "价格适中的，负担得起的", "Bezahlbarer Wohnraum fehlt in fast allen Großstädten.", "几乎所有大城市都缺少价格适中的住房。"),
                    v("der Wahlkampf", "Nomen", "竞选活动", "Im Wahlkampf versprechen Politiker oft niedrigere Mieten.", "在竞选期间，政客们常常承诺降低房租。", plural="die Wahlkämpfe"),
                ],
            },
            {
                "chinese": "左翼党希望将大型房地产企业手中的住房“公有化/社会化”。",
                "clozeWords": ["Wohnungen", "Konzernen", "vergesellschaften"],
                "vocab": [
                    v("der Konzern", "Nomen", "大型企业集团，康采恩", "Der Konzern besitzt tausende Mietwohnungen im Land.", "该集团在全国拥有数千套出租公寓。", plural="die Konzerne"),
                    v("vergesellschaften", "Verb", "使公有化，社会化", "Der Vorschlag sieht vor, große Wohnungsbestände zu vergesellschaften.", "该提议主张将大规模住房存量公有化。"),
                ],
            },
            {
                "chinese": "这意味着，相当于由柏林市政府出钱把这些公寓从企业集团手中买下来。",
                "clozeWords": ["bedeutet", "sozusagen", "abkaufen"],
                "vocab": [
                    v("sozusagen", "Adverb", "可以说，好比，相当于", "Das Café ist sozusagen mein zweites Wohnzimmer.", "这家咖啡馆可以说是我第二个客厅。"),
                    v("abkaufen", "Verb", "从……手中买下", "Er hat seinem Nachbarn das alte Fahrrad abgekauft.", "他从邻居手里买下了那辆旧自行车。"),
                ],
            },
        ],
    },
}
