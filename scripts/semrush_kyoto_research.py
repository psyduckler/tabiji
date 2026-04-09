#!/usr/bin/env python3
"""
Kyoto travel keyword research — mirrors the Barcelona script structure
with Japan-specific categories (ryokan, JR pass, temples, gion, kaiseki).
"""

import json
import csv
import time
import urllib.request
import urllib.parse
import sys
import re
from collections import defaultdict

API_KEY = "466c49b8794c2ba3d09ad2afd1964cd0"
DATABASE = "us"
DISPLAY_LIMIT = 500

OUT_DIR = "/Users/bjh/Documents/tabiji/scripts/kyoto-research"
RAW_JSON = f"{OUT_DIR}/raw_keywords.json"
CSV_OUT = f"{OUT_DIR}/keywords_categorized.csv"
SUMMARY_JSON = f"{OUT_DIR}/summary.json"

SEEDS = {
    "food_restaurants": [
        "kyoto restaurants", "best restaurants kyoto", "kyoto food",
        "where to eat kyoto", "kyoto dinner", "kyoto lunch",
        "kyoto breakfast", "kyoto michelin", "kyoto cuisine",
        "kaiseki kyoto", "kyoto kaiseki", "kyoto fine dining",
        "cheap eats kyoto", "kyoto food tour", "nishiki market",
    ],
    "food_japanese_specialty": [
        "kyoto ramen", "kyoto sushi", "kyoto tempura", "kyoto tonkatsu",
        "kyoto udon", "kyoto soba", "kyoto izakaya", "kyoto yakitori",
        "kyoto okonomiyaki", "kyoto tofu", "kyoto wagyu", "kyoto sukiyaki",
        "kyoto shojin ryori", "kyoto obanzai",
    ],
    "food_matcha_sweets": [
        "kyoto matcha", "kyoto wagashi", "kyoto sweets", "kyoto desserts",
        "kyoto tea ceremony", "matcha cafe kyoto", "kyoto green tea",
        "kyoto mochi", "kyoto ice cream",
    ],
    "food_cafes": [
        "kyoto coffee", "kyoto cafe", "kyoto coffee shops",
        "kyoto specialty coffee", "kyoto bakery",
    ],
    "food_dietary": [
        "vegan kyoto", "vegetarian kyoto", "gluten free kyoto",
        "halal kyoto", "kosher kyoto",
    ],
    "drinks_nightlife": [
        "kyoto bars", "best bars kyoto", "kyoto cocktail bar",
        "kyoto whisky bar", "kyoto sake bar", "kyoto rooftop bar",
        "kyoto nightlife", "kyoto nightclub", "kyoto clubs",
        "kyoto live music", "kyoto sake brewery", "kyoto sake tasting",
        "gion bars", "pontocho bars",
    ],
    "lodging_hotels": [
        "kyoto hotels", "best hotels kyoto", "cheap hotels kyoto",
        "luxury hotels kyoto", "boutique hotel kyoto",
        "5 star hotels kyoto", "kyoto family hotel",
        "kyoto hotels with onsen", "kyoto hotel with view",
    ],
    "lodging_ryokan": [
        "kyoto ryokan", "best ryokan kyoto", "luxury ryokan kyoto",
        "ryokan in kyoto", "traditional ryokan kyoto",
        "kyoto ryokan with onsen", "cheap ryokan kyoto",
        "kyoto machiya", "machiya rental kyoto",
    ],
    "lodging_other": [
        "kyoto hostels", "best hostels kyoto", "kyoto airbnb",
        "kyoto apartments", "kyoto vacation rental",
        "where to stay kyoto", "kyoto neighborhoods",
        "best area to stay kyoto", "gion accommodation",
        "kyoto capsule hotel",
    ],
    "transport": [
        "kyoto airport", "kansai airport to kyoto",
        "osaka airport to kyoto", "kyoto station",
        "kyoto subway", "kyoto bus", "kyoto taxi",
        "kyoto car rental", "kyoto transport",
        "getting around kyoto", "tokyo to kyoto",
        "osaka to kyoto", "kyoto to osaka", "kyoto to tokyo",
        "shinkansen kyoto", "bullet train kyoto",
        "jr pass kyoto", "icoca card kyoto",
    ],
    "sights_temples": [
        "kyoto temples", "best temples kyoto", "kyoto shrines",
        "fushimi inari", "fushimi inari shrine",
        "kinkaku-ji", "kinkakuji", "golden pavilion kyoto",
        "kiyomizu-dera", "kiyomizu temple",
        "ginkaku-ji", "silver pavilion kyoto",
        "ryoan-ji", "ryoanji zen garden",
        "tofuku-ji", "nanzen-ji", "tenryu-ji",
        "byodo-in", "to-ji", "sanjusangen-do",
        "honen-in", "eikan-do", "daitoku-ji",
        "shoren-in", "chion-in",
    ],
    "sights_arashiyama": [
        "arashiyama", "arashiyama bamboo grove",
        "arashiyama monkey park", "arashiyama kyoto",
        "bamboo forest kyoto", "tenryuji temple arashiyama",
        "togetsukyo bridge",
    ],
    "sights_gion_geisha": [
        "gion kyoto", "gion district", "kyoto geisha",
        "geisha district kyoto", "maiko kyoto",
        "geisha experience kyoto", "geisha show kyoto",
        "gion matsuri",
    ],
    "sights_castle_palace": [
        "nijo castle", "nijo-jo", "kyoto imperial palace",
        "kyoto gosho", "katsura imperial villa",
        "shugakuin imperial villa",
    ],
    "sights_attractions": [
        "things to do kyoto", "kyoto attractions", "kyoto sights",
        "kyoto tours", "kyoto day trips", "kyoto museums",
        "kyoto parks", "kyoto gardens", "philosophers path",
        "philosopher's walk kyoto", "kyoto walking tour",
        "kyoto bike tour", "kyoto free things to do",
        "kyoto with kids",
    ],
    "itinerary": [
        "kyoto itinerary", "kyoto 3 days", "kyoto 5 days",
        "kyoto weekend", "kyoto one day", "kyoto 4 days",
        "kyoto 2 days", "one week kyoto",
    ],
    "cultural_experiences": [
        "tea ceremony kyoto", "kyoto kimono rental",
        "kimono experience kyoto", "kyoto traditional experience",
        "calligraphy kyoto", "zen meditation kyoto",
        "samurai experience kyoto", "kyoto cooking class",
    ],
    "practical": [
        "kyoto weather", "best time to visit kyoto",
        "kyoto cherry blossom", "kyoto autumn leaves",
        "kyoto fall colors", "sakura kyoto",
        "kyoto in spring", "kyoto in autumn",
        "kyoto sim card", "kyoto wifi", "kyoto power adapter",
        "kyoto language", "kyoto currency",
    ],
    "safety": [
        "kyoto safety", "is kyoto safe", "kyoto scams",
        "kyoto dangerous", "kyoto crime",
        "kyoto safe at night",
    ],
    "visa_entry": [
        "kyoto visa", "japan visa", "japan entry requirements",
        "japan tourist visa", "japan digital nomad",
    ],
    "health_insurance": [
        "kyoto travel insurance", "japan travel insurance",
        "kyoto hospital", "kyoto pharmacy", "kyoto vaccinations",
        "japan vaccinations",
    ],
    "remote_living": [
        "kyoto digital nomad", "kyoto coworking",
        "kyoto remote work", "living in kyoto",
        "kyoto expat", "moving to kyoto", "cost of living kyoto",
        "teach english kyoto",
    ],
    "shopping": [
        "kyoto shopping", "kyoto markets", "kyoto souvenirs",
        "nishiki market kyoto", "teramachi shopping",
        "kyoto antique market", "kyoto flea market",
    ],
    "general_travel": [
        "kyoto travel", "kyoto trip", "kyoto vacation",
        "kyoto guide", "visit kyoto", "kyoto tourism",
        "kyoto city break",
    ],
}

# Noise filters specific to Kyoto
NOISE_PATTERNS = [
    # Kyoto Protocol (climate change)
    r"\bkyoto protocol\b", r"\bkyoto agreement\b", r"\bclimate kyoto\b",
    r"\bgreenhouse gas\b", r"\bemissions kyoto\b", r"\bunfccc\b",
    # Kyoto Animation (anime studio - tragedy + studio name)
    r"\bkyoto animation\b", r"\bkyoani\b", r"\banime kyoto\b",
    r"\bkyoto animation fire\b", r"\bkyoto arson\b",
    # Kyoto University (academic, not travel)
    r"\bkyoto university\b", r"\bkyodai\b", r"\bnobel kyoto\b",
    r"\bkyoto research\b", r"\bkyoto u\b",
    # Kyoto Steakhouse / Hibachi (US restaurant chain "Kyoto")
    r"\bsteakhouse\b", r"\bhibachi\b", r"\bkyoto japanese restaurant\b",
    r"\bkyoto sushi (bar|restaurant)\b",
    r"\bkyoto restaurant (orlando|tampa|denver|chicago|atlanta|houston|dallas|phoenix|miami|nyc|new york|boston|charlotte|austin|texas|florida|ohio|indiana|virginia|maryland|nj|pa|al|fl|ga|ca|tx|nc|sc|tn)\b",
    r"\bkyoto buffet\b",
    # Pokemon / video games
    r"\bpokemon\b", r"\bkyoto game\b",
    # Songs / movies / books
    r"\bkyoto song\b", r"\bphoebe bridgers kyoto\b",
    r"\bmemoirs of a geisha\b",  # ambiguous but mostly movie searches
    # Toyota / cars (Kyoto is a car name)
    r"\bkyoto sedan\b", r"\bkyoto coupe\b",
    # MIT MOOC, online courses
    r"\bkyoto course\b", r"\bkyoto online\b", r"\bmit kyoto\b",
    # Other
    r"\bkyoto pa\b", r"\bkyoto ny\b",
]

NOISE_RE = re.compile("|".join(NOISE_PATTERNS), re.IGNORECASE)

def is_noise(keyword):
    return bool(NOISE_RE.search(keyword))

def fullsearch(phrase):
    url = (
        f"https://api.semrush.com/"
        f"?type=phrase_fullsearch"
        f"&key={API_KEY}"
        f"&phrase={urllib.parse.quote(phrase)}"
        f"&database={DATABASE}"
        f"&export_columns=Ph,Nq,Cp,Co,Nr"
        f"&display_limit={DISPLAY_LIMIT}"
    )
    try:
        with urllib.request.urlopen(urllib.request.Request(url), timeout=30) as resp:
            body = resp.read().decode("utf-8").strip()
            if not body or "ERROR" in body[:30].upper():
                return []
            lines = body.split("\n")
            results = []
            for line in lines[1:]:
                parts = line.split(";")
                if len(parts) >= 2:
                    kw = parts[0].strip()
                    try: vol = int(parts[1])
                    except ValueError: vol = 0
                    try: cpc = float(parts[2]) if len(parts) > 2 else 0.0
                    except ValueError: cpc = 0.0
                    try: comp = float(parts[3]) if len(parts) > 3 else 0.0
                    except ValueError: comp = 0.0
                    try: nr = int(parts[4]) if len(parts) > 4 else 0
                    except ValueError: nr = 0
                    results.append({
                        "keyword": kw, "volume": vol, "cpc": cpc,
                        "competition": comp, "num_results": nr,
                    })
            return results
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        return []

def main():
    import os
    os.makedirs(OUT_DIR, exist_ok=True)

    all_keywords = {}
    seeds_by_keyword = defaultdict(list)

    total_seeds = sum(len(v) for v in SEEDS.values())
    seed_idx = 0

    for category, seed_list in SEEDS.items():
        print(f"\n=== {category} ===")
        for seed in seed_list:
            seed_idx += 1
            print(f"[{seed_idx}/{total_seeds}] '{seed}'...", end=" ", flush=True)
            results = fullsearch(seed)
            time.sleep(0.2)
            kept = 0
            for row in results:
                kw = row["keyword"]
                if "kyoto" not in kw.lower() and "fushimi inari" not in kw.lower() and "kinkaku" not in kw.lower() and "kiyomizu" not in kw.lower() and "arashiyama" not in kw.lower() and "ginkaku" not in kw.lower() and "ryoanji" not in kw.lower() and "ryoan-ji" not in kw.lower() and "nijo" not in kw.lower() and "byodo" not in kw.lower() and "tenryu" not in kw.lower() and "tofuku" not in kw.lower() and "nanzen" not in kw.lower() and "ginkaku-ji" not in kw.lower() and "philosopher" not in kw.lower():
                    continue
                if is_noise(kw):
                    continue
                if kw not in all_keywords:
                    all_keywords[kw] = {**row, "categories": set()}
                all_keywords[kw]["categories"].add(category)
                seeds_by_keyword[kw].append(seed)
                kept += 1
            print(f"{len(results)} raw, {kept} kept")

    print(f"\nTotal unique keywords: {len(all_keywords)}")

    raw_out = []
    for kw, data in all_keywords.items():
        raw_out.append({
            "keyword": kw,
            "volume": data["volume"],
            "cpc": data["cpc"],
            "competition": data["competition"],
            "num_results": data["num_results"],
            "categories": sorted(data["categories"]),
        })
    raw_out.sort(key=lambda r: r["volume"], reverse=True)
    with open(RAW_JSON, "w") as f:
        json.dump(raw_out, f, indent=2)
    with open(CSV_OUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["keyword", "volume", "cpc", "competition", "num_results", "categories"])
        writer.writeheader()
        for r in raw_out:
            writer.writerow({**r, "categories": "|".join(r["categories"])})

    buckets = {
        "head_10k+": [], "high_5k_10k": [], "mid_1k_5k": [],
        "low_500_1k": [], "longtail_100_500": [], "tail_lt_100": [],
    }
    for r in raw_out:
        v = r["volume"]
        if v >= 10000: buckets["head_10k+"].append(r)
        elif v >= 5000: buckets["high_5k_10k"].append(r)
        elif v >= 1000: buckets["mid_1k_5k"].append(r)
        elif v >= 500: buckets["low_500_1k"].append(r)
        elif v >= 100: buckets["longtail_100_500"].append(r)
        else: buckets["tail_lt_100"].append(r)

    cat_summary = {}
    for cat in SEEDS.keys():
        cat_kws = [r for r in raw_out if cat in r["categories"]]
        cat_kws.sort(key=lambda r: r["volume"], reverse=True)
        cat_summary[cat] = {
            "total_keywords": len(cat_kws),
            "total_volume": sum(r["volume"] for r in cat_kws),
            "top_20": cat_kws[:20],
        }

    summary = {
        "total_keywords": len(raw_out),
        "total_volume": sum(r["volume"] for r in raw_out),
        "buckets": {k: {"count": len(v), "total_volume": sum(r["volume"] for r in v)} for k, v in buckets.items()},
        "categories": cat_summary,
        "top_50_overall": raw_out[:50],
    }
    with open(SUMMARY_JSON, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nWrote:\n  {RAW_JSON}\n  {CSV_OUT}\n  {SUMMARY_JSON}")
    print("\nVolume buckets:")
    for k, v in buckets.items():
        print(f"  {k}: {len(v)} kws, vol {sum(r['volume'] for r in v):,}")

if __name__ == "__main__":
    main()
