import requests

proxies = {
    'http': 'http://127.0.0.1:12450',
    'https': 'http://127.0.0.1:12450',
}

try:
    r = requests.get('https://www1.wdr.de/radio/podcasts/quarks-daily-100.podcast', proxies=proxies, timeout=5)
    print('Proxy WDR status:', r.status_code, len(r.content))
except Exception as e:
    print('Proxy WDR error:', e)
