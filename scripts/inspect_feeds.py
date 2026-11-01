import requests
from lxml import etree

r = requests.get('https://www1.wdr.de/radio/podcasts/quarks-daily-100.podcast', timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
parser = etree.XMLParser(recover=True, encoding='utf-8')
root = etree.fromstring(r.content, parser=parser)
items = root.xpath('//item')
print('Quarks real items count:', len(items))
for item in items[:10]:
    t = item.findtext('title')
    enc = item.find('enclosure')
    u = enc.attrib.get('url') if enc is not None else None
    desc = item.findtext('description')
    print('Title:', t)
    print('Audio:', u)
    print('Desc:', desc[:150] if desc else 'No desc')
    print('-'*40)
