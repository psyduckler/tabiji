#!/usr/bin/env python3
"""
Discover new travel compare page opportunities using Semrush.
Uses phrase_fullsearch with travel-intent keywords and validates
against a known destinations list.
"""

import json
import csv
import time
import urllib.request
import urllib.parse
import sys
import re

API_KEY = "466c49b8794c2ba3d09ad2afd1964cd0"
DATABASE = "us"
EXISTING_SLUGS_FILE = "/Users/bjh/Documents/tabiji/scripts/all-existing-slugs.json"
OUTPUT_FILE = "/Users/bjh/Documents/tabiji/compare-keyword-opportunities.csv"

# Known travel destinations for validation
DESTINATIONS = {
    # Countries
    "italy", "spain", "france", "portugal", "greece", "croatia", "turkey",
    "thailand", "japan", "mexico", "costa rica", "colombia", "peru", "argentina",
    "morocco", "egypt", "iceland", "norway", "switzerland", "austria", "germany",
    "netherlands", "ireland", "scotland", "england", "australia", "new zealand",
    "canada", "vietnam", "south korea", "taiwan", "indonesia", "malaysia",
    "philippines", "india", "sri lanka", "nepal", "cambodia", "laos", "myanmar",
    "china", "brazil", "chile", "ecuador", "bolivia", "uruguay", "panama",
    "belize", "guatemala", "honduras", "nicaragua", "cuba", "dominican republic",
    "puerto rico", "jamaica", "barbados", "bahamas", "aruba", "curacao",
    "trinidad and tobago", "kenya", "tanzania", "south africa", "namibia",
    "botswana", "ethiopia", "ghana", "senegal", "madagascar", "mauritius",
    "seychelles", "maldives", "fiji", "samoa", "tahiti", "new caledonia",
    "jordan", "oman", "uae", "qatar", "bahrain", "israel", "lebanon",
    "georgia", "armenia", "azerbaijan", "uzbekistan", "kyrgyzstan", "mongolia",
    "sweden", "denmark", "finland", "belgium", "luxembourg", "czech republic",
    "poland", "hungary", "romania", "bulgaria", "serbia", "montenegro",
    "albania", "north macedonia", "slovenia", "slovakia", "malta", "cyprus",
    "estonia", "latvia", "lithuania", "uk", "united kingdom", "usa",
    "united states", "singapore", "hong kong", "macau",
    # US States / Regions
    "hawaii", "alaska", "california", "florida", "colorado", "texas",
    "pacific northwest", "new england",
    # Major cities
    "london", "paris", "amsterdam", "tokyo", "rome", "barcelona", "lisbon",
    "berlin", "prague", "vienna", "dubai", "bangkok", "singapore", "seoul",
    "istanbul", "new york", "los angeles", "miami", "san francisco", "chicago",
    "seattle", "boston", "washington dc", "austin", "nashville", "denver",
    "san diego", "portland", "new orleans", "honolulu", "sydney", "melbourne",
    "brisbane", "perth", "auckland", "wellington", "toronto", "vancouver",
    "montreal", "quebec city", "calgary", "bali", "phuket", "cancun",
    "cape town", "florence", "venice", "naples", "milan", "madrid", "seville",
    "porto", "nice", "monaco", "edinburgh", "dublin", "copenhagen", "stockholm",
    "oslo", "helsinki", "budapest", "krakow", "warsaw", "marrakech", "fez",
    "cairo", "luxor", "athens", "santorini", "mykonos", "crete", "rhodes",
    "corfu", "kyoto", "osaka", "hiroshima", "okinawa", "sapporo", "fukuoka",
    "hong kong", "taipei", "hanoi", "ho chi minh city", "da nang", "hoi an",
    "chiang mai", "pattaya", "krabi", "koh samui", "buenos aires",
    "rio de janeiro", "sao paulo", "mexico city", "guadalajara", "oaxaca",
    "playa del carmen", "tulum", "lima", "cusco", "bogota", "medellin",
    "cartagena", "quito", "la paz", "santiago", "valparaiso", "montevideo",
    "havana", "san juan", "punta cana", "kingston", "nassau",
    "kuala lumpur", "penang", "langkawi", "manila", "cebu", "palawan",
    "boracay", "siargao", "el nido", "jakarta", "yogyakarta", "lombok",
    "ubud", "seminyak", "canggu", "phnom penh", "siem reap",
    "luang prabang", "vientiane", "yangon", "bagan",
    "mumbai", "delhi", "goa", "jaipur", "varanasi", "kerala",
    "colombo", "kandy", "ella", "galle", "kathmandu", "pokhara",
    "beijing", "shanghai", "xi'an", "guilin", "chengdu", "lhasa",
    "dubai", "abu dhabi", "muscat", "doha", "manama",
    "amman", "petra", "tel aviv", "jerusalem",
    "tbilisi", "yerevan", "baku", "tashkent", "samarkand", "bishkek",
    "nairobi", "zanzibar", "arusha", "cape town", "johannesburg",
    "windhoek", "gaborone", "addis ababa", "accra", "dakar",
    "antananarivo", "port louis",
    "reykjavik", "bergen", "tromso",
    "zurich", "geneva", "lucerne", "interlaken", "zermatt",
    "salzburg", "innsbruck", "hallstatt",
    "munich", "hamburg", "cologne", "frankfurt", "dresden",
    "bruges", "ghent", "antwerp",
    "dubrovnik", "split", "hvar", "zadar",
    "lake como", "amalfi coast", "cinque terre", "sardinia", "sicily",
    "tuscany", "puglia", "lake garda", "dolomites", "capri", "positano",
    "malaga", "granada", "san sebastian", "ibiza", "mallorca",
    "tenerife", "gran canaria", "lanzarote",
    "algarve", "azores", "madeira", "sintra",
    "provence", "lyon", "bordeaux", "marseille", "strasbourg",
    "mont saint-michel", "french riviera", "chamonix",
    "zakynthos", "paros", "naxos", "milos", "meteora", "thessaloniki",
    "galway", "cork", "killarney", "belfast",
    "bath", "oxford", "cambridge", "york", "brighton", "liverpool",
    "manchester", "lake district", "cotswolds", "cornwall",
    "tallinn", "riga", "vilnius",
    "bucharest", "transylvania", "sofia",
    "belgrade", "kotor", "tirana", "ohrid", "bled", "bratislava",
    "valletta", "gozo", "nicosia", "paphos",
    # Islands & beach destinations
    "maui", "big island", "kauai", "oahu", "waikiki",
    "turks and caicos", "st lucia", "antigua", "bermuda",
    "bora bora", "moorea", "whitsundays", "gold coast", "byron bay",
    "cabo", "cabo san lucas", "puerto vallarta", "riviera maya",
    "punta cana", "los cabos", "costa brava", "costa del sol",
    "french polynesia", "cook islands",
    # Nature / regions
    "patagonia", "galapagos", "amazon", "yosemite", "yellowstone",
    "grand canyon", "banff", "jasper", "glacier national park",
    "scottish highlands", "norwegian fjords", "swiss alps",
    "canadian rockies", "lapland", "lofoten",
    "queenstown", "milford sound", "abel tasman", "wanaka",
    "kruger", "serengeti", "masai mara", "okavango delta",
    "kilimanjaro", "everest base camp", "annapurna",
    "torres del paine", "iguazu falls", "angel falls",
    "lake bled", "plitvice", "cinque terre",
    "lake atitlan", "lake titicaca",
}

def keyword_to_slug(keyword):
    slug = keyword.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug

def reverse_slug(slug):
    parts = slug.split("-vs-")
    if len(parts) == 2:
        return f"{parts[1]}-vs-{parts[0]}"
    return slug

def is_valid_travel_compare(keyword):
    """Check if both sides of the comparison are known destinations."""
    parts = keyword.lower().split(" vs ")
    if len(parts) != 2:
        return False

    side1 = parts[0].strip()
    side2 = parts[1].strip()

    # Both sides must be known destinations
    return side1 in DESTINATIONS and side2 in DESTINATIONS

def get_phrase_keywords(phrase, search_type="phrase_fullsearch"):
    """Get keywords from Semrush."""
    url = (
        f"https://api.semrush.com/"
        f"?type={search_type}"
        f"&key={API_KEY}"
        f"&phrase={urllib.parse.quote(phrase)}"
        f"&database={DATABASE}"
        f"&export_columns=Ph,Nq"
        f"&display_limit=100"
    )
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8").strip()
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
                    if " vs " in kw and vol > 0:
                        results.append((kw, vol))
            return results
    except Exception as e:
        print(f"  Error: {e}", file=sys.stderr)
        return []

def get_single_volume(keyword):
    url = (
        f"https://api.semrush.com/"
        f"?type=phrase_this"
        f"&key={API_KEY}"
        f"&phrase={urllib.parse.quote(keyword)}"
        f"&database={DATABASE}"
        f"&export_columns=Ph,Nq"
    )
    try:
        with urllib.request.urlopen(urllib.request.Request(url), timeout=15) as resp:
            body = resp.read().decode("utf-8").strip()
            lines = body.split("\n")
            if len(lines) >= 2:
                p = lines[1].split(";")
                if len(p) >= 2:
                    return int(p[1])
        return 0
    except:
        return 0

def main():
    with open(EXISTING_SLUGS_FILE) as f:
        existing = set(json.load(f))
    print(f"Loaded {len(existing)} existing slugs")

    # Seed queries - city-specific "X vs" searches
    seeds = [
        # Top cities
        "london vs", "paris vs", "amsterdam vs", "tokyo vs", "rome vs",
        "barcelona vs", "lisbon vs", "berlin vs", "prague vs", "vienna vs",
        "dubai vs", "bangkok vs", "seoul vs", "istanbul vs",
        "new york vs", "los angeles vs", "miami vs", "san francisco vs",
        "sydney vs", "melbourne vs", "toronto vs", "vancouver vs",
        "bali vs", "phuket vs", "cancun vs", "cape town vs",
        "florence vs", "venice vs", "naples vs", "milan vs",
        "madrid vs", "seville vs", "porto vs", "nice vs",
        "edinburgh vs", "dublin vs", "copenhagen vs", "stockholm vs",
        "budapest vs", "krakow vs", "marrakech vs", "athens vs",
        "santorini vs", "mykonos vs", "crete vs",
        "kyoto vs", "osaka vs", "hong kong vs", "taipei vs",
        "hanoi vs", "chiang mai vs", "da nang vs",
        "buenos aires vs", "rio de janeiro vs", "mexico city vs",
        "lima vs", "bogota vs", "medellin vs", "cartagena vs",
        "dubrovnik vs", "split vs", "zurich vs", "salzburg vs",
        "munich vs", "maui vs", "oahu vs", "kauai vs",
        "tulum vs", "playa del carmen vs", "cabo vs",
        "amalfi coast vs", "cinque terre vs", "lake como vs",
        "sicily vs", "sardinia vs", "tuscany vs",
        "algarve vs", "azores vs",
        "reykjavik vs", "tromso vs",
        # Countries
        "italy vs", "spain vs", "france vs", "portugal vs", "greece vs",
        "croatia vs", "turkey vs", "thailand vs", "japan vs", "mexico vs",
        "costa rica vs", "colombia vs", "peru vs", "argentina vs",
        "morocco vs", "egypt vs", "iceland vs", "norway vs",
        "switzerland vs", "austria vs", "germany vs",
        "ireland vs", "australia vs", "new zealand vs",
        "vietnam vs", "south korea vs", "taiwan vs",
        "hawaii vs", "maldives vs", "fiji vs",
        "dominican republic vs", "jamaica vs", "cuba vs",
        "belize vs", "panama vs", "guatemala vs",
        "sri lanka vs", "nepal vs", "india vs",
        "kenya vs", "tanzania vs", "south africa vs",
    ]

    discovered = {}

    for i, seed in enumerate(seeds):
        print(f"[{i+1}/{len(seeds)}] '{seed}'...", end=" ", flush=True)

        results = get_phrase_keywords(seed)
        time.sleep(0.25)

        new_count = 0
        for kw, vol in results:
            if not is_valid_travel_compare(kw):
                continue

            slug = keyword_to_slug(kw)
            rev = reverse_slug(slug)

            if slug in existing or rev in existing:
                continue

            canonical = min(slug, rev)
            if canonical not in discovered or vol > discovered[canonical]["volume"]:
                discovered[canonical] = {"keyword": kw, "slug": canonical, "volume": vol}
                new_count += 1

        print(f"{len(results)} raw, {new_count} new travel")

    print(f"\nTotal unique new travel opportunities: {len(discovered)}")

    # Get precise volumes for top candidates (both directions)
    top_candidates = sorted(discovered.values(), key=lambda x: x["volume"], reverse=True)[:150]
    print(f"Checking reverse volumes for top {len(top_candidates)}...")

    results = []
    for i, item in enumerate(top_candidates):
        slug = item["slug"]
        parts = slug.split("-vs-")
        if len(parts) != 2:
            continue

        dest1 = parts[0].replace("-", " ")
        dest2 = parts[1].replace("-", " ")
        kw1 = f"{dest1} vs {dest2}"
        kw2 = f"{dest2} vs {dest1}"

        print(f"  [{i+1}/{len(top_candidates)}] {slug}...", end=" ", flush=True)

        vol1 = get_single_volume(kw1)
        time.sleep(0.15)
        vol2 = get_single_volume(kw2)
        time.sleep(0.15)

        total = vol1 + vol2
        best_kw = kw1 if vol1 >= vol2 else kw2
        best_vol = max(vol1, vol2)

        print(f"{vol1} + {vol2} = {total}")

        results.append({
            "slug": slug,
            "url": f"https://tabiji.ai/compare/{slug}/",
            "keyword_1": kw1,
            "vol_1": vol1,
            "keyword_2": kw2,
            "vol_2": vol2,
            "best_keyword": best_kw,
            "best_vol": best_vol,
            "total_vol": total,
        })

    results.sort(key=lambda r: r["total_vol"], reverse=True)
    top100 = [r for r in results if r["total_vol"] > 0][:100]

    fieldnames = ["slug", "url", "keyword_1", "vol_1", "keyword_2", "vol_2", "best_keyword", "best_vol", "total_vol"]
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(top100)

    print(f"\nTop 100 new travel opportunities written to {OUTPUT_FILE}")
    print(f"\nTop 20:")
    for r in top100[:20]:
        print(f"  {r['slug']}: {r['total_vol']:,} ({r['best_keyword']} = {r['best_vol']:,})")

if __name__ == "__main__":
    main()
