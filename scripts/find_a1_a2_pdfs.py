import requests
import re
from urllib.parse import urljoin

for lvl, u in [('A1', 'https://www.goethe.de/de/spr/prf/ueb/sd1.html'), ('A2', 'https://www.goethe.de/de/spr/prf/ueb/pa2.html')]:
    try:
        r = requests.get(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}, timeout=10)
        print(f"=== {lvl} ===")
        for link in set(re.findall(r'href=["\']([^"\']+\.pdf)["\']', r.text, re.IGNORECASE)):
            print(urljoin(u, link))
    except Exception as e:
        print(f"Error {lvl}: {e}")
