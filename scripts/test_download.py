import requests

url = 'https://slowgerman.cdn.svmaudio.com/slowgerman/sg326.mp3'
try:
    r = requests.get(url, stream=True, timeout=10)
    print('Slow German stream status:', r.status_code)
    chunk = next(r.iter_content(chunk_size=4096))
    print('Received chunk bytes:', len(chunk))
except Exception as e:
    print('Download error:', e)
