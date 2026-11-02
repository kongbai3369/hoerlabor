import requests
import re
from urllib.parse import urljoin

url = 'https://www.testdaf.de/de/teilnehmende/der-papierbasierte-testdaf/vorbereitung-auf-den-papierbasierten-testdaf/modelltests/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
r = requests.get(url, headers=headers)
print('Status:', r.status_code)

links = re.findall(r'href=["\']([^"\']+)["\']', r.text)
for l in links:
    if any(k in l.lower() for k in ['h%c3%b6r', 'hoer', 'transkription', 'audiodatei', '.mp3', '.pdf']):
        full = urljoin(url, l)
        print(full)
