import requests

candidates = [
    "https://www.goethe.de/pro/relaunch/prf/materialien/A1/sd1_modellsatz_01.pdf",
    "https://www.goethe.de/pro/relaunch/prf/materialien/A1/a1_modellsatz_erwachsene.pdf",
    "https://www.goethe.de/pro/relaunch/prf/materialien/A1/sd1_modellsatz.pdf",
    "https://www.goethe.de/pro/relaunch/prf/materialien/A1/A1_SD1_Modellsatz.pdf",
    "https://www.goethe.de/pro/relaunch/prf/materialien/A2/a2_modellsatz_erwachsene.pdf",
    "https://www.goethe.de/pro/relaunch/prf/materialien/A2/a2_modellsatz.pdf",
    "https://www.goethe.de/pro/relaunch/prf/materialien/A2/A2_Modellsatz.pdf",
    "https://www.goethe.de/pro/relaunch/prf/materialien/A2/gz_a2_modellsatz.pdf"
]

for url in candidates:
    try:
        r = requests.head(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        print(url, r.status_code)
    except Exception as e:
        print(url, e)
