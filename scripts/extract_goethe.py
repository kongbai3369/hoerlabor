import requests
import re
from urllib.parse import urljoin

urls = [
    ('B1', 'https://www.goethe.de/de/spr/prf/ueb/pb1.html'),
    ('B2', 'https://www.goethe.de/de/spr/prf/ueb/pb2.html'),
    ('A2', 'https://www.goethe.de/de/spr/prf/ueb/pa2.html'),
    ('A1', 'https://www.goethe.de/de/spr/prf/ueb/sd1.html'),
    ('C1', 'https://www.goethe.de/de/spr/prf/ueb/pc1.html'),
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for lvl, u in urls:
    try:
        r = requests.get(u, headers=headers, timeout=10)
        print(f'=== {lvl}: {u} -> Status {r.status_code} ===')
        links = re.findall(r'href=["\']([^"\']+)["\']', r.text)
        media = [urljoin(u, l) for l in links if any(k in l.lower() for k in ['.mp3', '.mp4', '.pdf', 'pross', 'm4a', 'download'])]
        for m in sorted(set(media))[:10]:
            print('  ', m)
    except Exception as e:
        print(f'Error {lvl}: {e}')
