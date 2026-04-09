#!/usr/bin/env python3
"""
Extensive Semrush keyword research on Barcelona travel-related terms.
Uses phrase_fullsearch with compound seed phrases across all travel categories,
then aggregates, deduplicates, categorizes, and buckets results.
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

OUT_DIR = "/Users/bjh/Documents/tabiji/scripts/barcelona-research"
RAW_JSON = f"{OUT_DIR}/raw_keywords.json"
CSV_OUT = f"{OUT_DIR}/keywords_categorized.csv"
SUMMARY_JSON = f"{OUT_DIR}/summary.json"

# Categories of compound seed phrases. Each seed -> phrase_fullsearch returns
# all keywords containing that exact phrase.
SEEDS = {
    "food_restaurants": [
        "barcelona restaurants", "best restaurants barcelona", "barcelona food",
        "where to eat barcelona", "barcelona dinner", "barcelona lunch",
        "barcelona brunch", "barcelona breakfast", "barcelona michelin",
        "barcelona tapas", "barcelona paella", "barcelona vegan",
        "barcelona vegetarian", "barcelona seafood", "barcelona steakhouse",
        "cheap eats barcelona", "barcelona street food", "barcelona food tour",
        "barcelona food market", "barcelona fine dining",
    ],
    "food_cafes": [
        "barcelona coffee", "barcelona cafe", "barcelona coffee shops",
        "barcelona specialty coffee", "barcelona bakery", "barcelona pastry",
        "barcelona dessert", "barcelona ice cream", "barcelona chocolate",
    ],
    "drinks_nightlife": [
        "barcelona bars", "best bars barcelona", "barcelona cocktail bar",
        "barcelona wine bar", "barcelona rooftop bar", "barcelona beach bar",
        "barcelona sports bar", "barcelona gay bar", "barcelona speakeasy",
        "barcelona nightlife", "barcelona nightclub", "barcelona clubs",
        "barcelona party", "barcelona dancing", "barcelona live music",
        "barcelona sangria",
    ],
    "lodging_hotels": [
        "barcelona hotels", "best hotels barcelona", "cheap hotels barcelona",
        "luxury hotels barcelona", "boutique hotel barcelona",
        "5 star hotels barcelona", "barcelona beach hotel",
        "barcelona family hotel", "barcelona resort", "barcelona spa hotel",
        "barcelona hotels with pool",
    ],
    "lodging_other": [
        "barcelona hostels", "best hostels barcelona", "barcelona airbnb",
        "barcelona apartments", "barcelona vacation rental",
        "barcelona short term rental", "barcelona long term rental",
        "barcelona monthly rental", "where to stay barcelona",
        "barcelona neighborhoods", "best area to stay barcelona",
    ],
    "transport": [
        "barcelona airport", "barcelona airport to city",
        "barcelona airport transfer", "barcelona metro", "barcelona taxi",
        "uber barcelona", "barcelona car rental", "barcelona transport",
        "getting around barcelona", "barcelona bus", "barcelona train",
        "barcelona to madrid", "barcelona cruise port",
    ],
    "sights_attractions": [
        "things to do barcelona", "barcelona attractions", "barcelona sights",
        "barcelona tours", "barcelona day trips", "barcelona museums",
        "barcelona beaches", "barcelona parks", "sagrada familia",
        "park guell", "casa batllo", "casa mila", "la rambla",
        "gothic quarter barcelona", "barcelona aquarium", "camp nou",
        "barcelona walking tour", "barcelona bike tour",
        "barcelona free things to do", "barcelona with kids",
    ],
    "itinerary": [
        "barcelona itinerary", "barcelona 3 days", "barcelona 5 days",
        "barcelona weekend", "barcelona one day", "barcelona 4 days",
        "barcelona 2 days", "one week barcelona",
    ],
    "practical": [
        "barcelona weather", "best time to visit barcelona",
        "barcelona currency", "barcelona language", "barcelona tipping",
        "barcelona sim card", "barcelona wifi", "barcelona dress code",
        "barcelona etiquette", "barcelona power adapter",
    ],
    "safety": [
        "barcelona safety", "is barcelona safe", "barcelona scams",
        "barcelona pickpockets", "barcelona dangerous", "barcelona crime",
        "barcelona safe areas", "barcelona safe at night",
    ],
    "visa_entry": [
        "barcelona visa", "spain visa", "barcelona digital nomad visa",
        "spain digital nomad", "spain entry requirements",
        "schengen barcelona",
    ],
    "health_insurance": [
        "barcelona travel insurance", "spain travel insurance",
        "barcelona health insurance", "spain health insurance",
        "barcelona hospital", "barcelona pharmacy", "barcelona doctor",
        "barcelona vaccinations", "spain vaccinations",
    ],
    "remote_living": [
        "barcelona digital nomad", "barcelona coworking",
        "barcelona remote work", "living in barcelona",
        "barcelona expat", "moving to barcelona", "cost of living barcelona",
    ],
    "shopping": [
        "barcelona shopping", "barcelona markets", "barcelona souvenirs",
        "barcelona boqueria", "barcelona el corte ingles",
    ],
    "general_travel": [
        "barcelona travel", "barcelona trip", "barcelona vacation",
        "barcelona guide", "visit barcelona", "barcelona holiday",
        "barcelona tourism", "barcelona city break",
    ],
}

# Noise filters: US Barcelona restaurant chain locations and FC Barcelona terms
NOISE_PATTERNS = [
    r"\bbrookline\b", r"\bstamford\b", r"\bconnecticut\b", r"\bct\b",
    r"\bwashington dc\b", r"\bdc\b", r"\bvirginia\b", r"\bva\b",
    r"\bnew york\b", r"\bbaltimore\b", r"\bri\b", r"\brhode island\b",
    r"\bma\b", r"\bbethesda\b", r"\bnoma\b", r"\barlington\b",
    r"\bgeorgetown\b", r"\bwest hartford\b", r"\bfairfield\b",
    r"\bdis fru tar\b", r"\bdisfrutar\b",
    # FC Barcelona football noise
    r"\bfc barcelona\b", r"\bbarça\b", r"\bbarca\b",
    r"\bbarcelona vs\b", r"\bvs barcelona\b", r"\bbarcelona schedule\b",
    r"\bbarcelona standings\b", r"\bbarcelona fc\b", r"\bfutbol club\b",
    r"\bpartidos\b", r"\bmessi\b", r"\bbarcelona match\b",
    r"\breal madrid vs\b", r"\bvs real madrid\b", r"\bla liga\b",
    r"\bbarcelona players\b", r"\bbarcelona jersey\b", r"\bbarcelona kit\b",
    r"\bbarcelona b\b", r"\bbarcelona u\b", r"\bbarcelona femen\b",
    # Other Barcelona namesakes
    r"\bvenezuela\b",
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
                    try:
                        vol = int(parts[1])
                    except ValueError:
                        vol = 0
                    try:
                        cpc = float(parts[2]) if len(parts) > 2 else 0.0
                    except ValueError:
                        cpc = 0.0
                    try:
                        comp = float(parts[3]) if len(parts) > 3 else 0.0
                    except ValueError:
                        comp = 0.0
                    try:
                        nr = int(parts[4]) if len(parts) > 4 else 0
                    except ValueError:
                        nr = 0
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

    all_keywords = {}  # keyword -> {data, categories: set}
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
                if "barcelona" not in kw.lower():
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

    # Save raw
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

    # CSV
    with open(CSV_OUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["keyword", "volume", "cpc", "competition", "num_results", "categories"])
        writer.writeheader()
        for r in raw_out:
            writer.writerow({**r, "categories": "|".join(r["categories"])})

    # Volume buckets
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

    # Per-category summary
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
        print(f"  {k}: {len(v)} keywords, total vol {sum(r['volume'] for r in v):,}")

if __name__ == "__main__":
    main()
