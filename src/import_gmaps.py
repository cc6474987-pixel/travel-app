# Merge a Google Maps list export (idx|name|lat,lng|addr) into places.json
import json, math, re, sys, urllib.parse
src, label, url = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.load(open('places.json')); P = d['places']
def dist(a, b, c, e):
    return 6371000 * 2 * math.asin(math.sqrt(math.sin(math.radians(c - a) / 2) ** 2 + math.cos(math.radians(a)) * math.cos(math.radians(c)) * math.sin(math.radians(e - b) / 2) ** 2))
cent = {}
for p in P:
    if p.get('from'): continue
    cent.setdefault(p['area'], []).append((p['lat'], p['lng']))
cent = {k: (sum(x for x, _ in v) / len(v), sum(y for _, y in v) / len(v)) for k, v in cent.items()}
EXTRA = {'銀座': (35.6717, 139.7650), '新宿': (35.6905, 139.7020), '池袋': (35.7295, 139.7120), '原宿': (35.6702, 139.7040),
         '惠比壽・代官山': (35.6480, 139.7030), '中目黑': (35.6440, 139.6990), '日本橋': (35.6830, 139.7740), '麻布十番': (35.6550, 139.7360),
         '品川・高輪': (35.6320, 139.7400), '谷中': (35.7270, 139.7660), '晴空塔': (35.7100, 139.8110), '吉祥寺': (35.7035, 139.5790),
         '自由之丘': (35.6100, 139.6680), '江之島': (35.3000, 139.4780), '橫濱': (35.4560, 139.6320)}
cent.update(EXTRA)
def area(lat, lng):
    k, m = min(((k, dist(lat, lng, *c)) for k, c in cent.items()), key=lambda t: t[1])
    return k if m < 2500 else ('富士五湖' if lng < 139 else '神奈川' if lat < 35.55 else '東京')
def cat(n):
    s = n.lower()
    if re.search(r'curry|咖哩', s): return '咖哩'
    if re.search(r'osteria|grill|deli|brunch|bills|eggs|pancake|班戟|鬆餅', s): return '西式'
    if re.search(r'bread|bakery|boulang|pain|パン|麵包|ange|viron|bagel|truffle', s): return '麵包'
    if re.search(r'coffee|咖啡|espresso|roast|珈琲|コーヒー|喫茶|kissa|starbucks|星巴克|fuglen|tea|茶', s): return '咖啡'
    return '甜點'

added = skipped = 0
fcat = lst = ''
for line in open(src, encoding='utf-8'):
    line = line.rstrip('\n')
    if not line: continue
    if line.startswith('##'):
        fcat, lst = line[2:].split('|', 1); label = '來自 Google 地圖清單「' + lst + '」'; url = lst; continue
    _, n, ll, addr, *rest = line.split('|')
    note = (rest[0] + '。' if rest and rest[0] else '') + label
    lat, lng = map(float, ll.split(','))
    if re.match(r'^\d+-ch', n): skipped += 1; continue  # bare address pin, not a shop
    key = re.sub(r'\s+', '', n).lower()
    if any((key == re.sub(r'\s+', '', p['name']).lower() and dist(lat, lng, p['lat'], p['lng']) < 300) or (dist(lat, lng, p['lat'], p['lng']) < 25 and key[:4] in re.sub(r'\s+', '', p['name']).lower()) for p in P):
        for p in P:
            if p.get('from') and dist(lat, lng, p['lat'], p['lng']) < 300 and re.sub(r'\s+', '', p['name']).lower() == key and lst not in p['note']:
                p['note'] += '；也在「' + lst + '」'
        print('dup', n); skipped += 1; continue
    P.append({'name': n, 'jp': '', 'cat': fcat or cat(n), 'area': area(lat, lng), 'addr': addr.strip().rstrip(','), 'lat': lat, 'lng': lng,
              'note': note, 'hours': '', 'src': 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote(n) + f'&center={lat},{lng}', 'from': url})
    added += 1
json.dump(d, open('places.json', 'w'), ensure_ascii=False, indent=1)
print('added', added, 'skipped', skipped, 'total', len(P))
