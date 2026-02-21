#!/usr/bin/env python3
"""Fetch top 5 Google Images candidates for each restaurant via SerpAPI."""
import subprocess, json, urllib.request, urllib.parse, os, time

SERPAPI_KEY = subprocess.check_output(['security', 'find-generic-password', '-s', 'serpapi-key', '-w']).decode().strip()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
os.makedirs('candidates', exist_ok=True)

RESTAURANTS = [
    ("kamo-to-negi", "Kamo to Negi 鴨to葱 Shibuya ramen"),
    ("fuunji", "Fuunji 風雲児 tsukemen Tokyo"),
    ("oreryu-shio-ramen", "Oreryu Shio Ramen 俺流塩らーめん Shibuya"),
    ("ramen-tatsunoya", "Ramen Tatsunoya 龍の家 Shibuya"),
    ("afuri-shibuya", "AFURI ramen Shibuya yuzu shio"),
    ("menya-musashi", "Menya Musashi 麺屋武蔵 Shibuya ramen"),
    ("tsuta", "Tsuta 蔦 ramen Yoyogi-Uehara"),
    ("mammoth", "Mammoth マンモス tsukemen Shibuya"),
    ("hayashi", "Hayashi はやし ramen Shibuya"),
    ("tonari", "Tonari 東南 tanmen Shibuya ramen"),
    ("ramen-nagi", "Ramen Nagi ラーメン凪 Shibuya niboshi"),
    ("sakurazaka", "Sakurazaka 桜坂 ramen Shibuya tonkotsu"),
    ("jikasei-mensho", "Jikasei Mensho 自家製麺 ramen Shibuya"),
    ("ichiran-shibuya", "Ichiran 一蘭 Shibuya ramen"),
    ("soranoiro", "Soranoiro ソラノイロ ramen vegan Tokyo"),
    ("kiraku", "Kiraku 喜楽 ramen Shibuya"),
    ("ippudo-shibuya", "Ippudo 一風堂 Shibuya ramen"),
    ("junteuchi-men-to-mirai", "Junteuchi Men to Mirai 純手打ち 麺と未来 Shimokitazawa ramen"),
]

for slug, query in RESTAURANTS:
    final = f"{slug}.jpg"
    if os.path.exists(final) and os.path.getsize(final) > 1024:
        print(f"SKIP {slug} — already has photo")
        continue

    cdir = f"candidates/{slug}"
    os.makedirs(cdir, exist_ok=True)

    print(f"SEARCH: {slug}")
    url = f"https://serpapi.com/search.json?engine=google_images&q={urllib.parse.quote(query)}&api_key={SERPAPI_KEY}&num=8"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"  ERROR searching: {e}")
        continue

    results = data.get('images_results', [])[:5]
    downloaded = 0
    for i, r in enumerate(results):
        img_url = r.get('original', '')
        if not img_url:
            continue
        outpath = f"{cdir}/photo_{i+1}.jpg"
        try:
            req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data_bytes = resp.read()
            if len(data_bytes) < 10000:
                print(f"  photo_{i+1}: too small ({len(data_bytes)} bytes)")
                continue
            with open(outpath, 'wb') as f:
                f.write(data_bytes)
            print(f"  photo_{i+1}: {len(data_bytes)} bytes OK")
            downloaded += 1
        except Exception as e:
            print(f"  photo_{i+1}: download failed — {e}")

    print(f"  → {downloaded} candidates downloaded")
    time.sleep(0.5)

print("\nDONE fetching all candidates")
