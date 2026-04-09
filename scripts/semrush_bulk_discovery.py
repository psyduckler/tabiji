#!/usr/bin/env python3
"""
Bulk discover travel compare page opportunities using Semrush.
Persists ALL results (not just top 100) and does expanded seed queries.
"""

import json
import csv
import time
import urllib.request
import urllib.parse
import sys
import re
import os

API_KEY = "466c49b8794c2ba3d09ad2afd1964cd0"
DATABASE = "us"
QUEUE_FILE = "/Users/bjh/Documents/tabiji/compare-queue.json"
EXISTING_SLUGS_FILE = "/Users/bjh/Documents/tabiji/scripts/all-existing-slugs.json"
ALL_OPPORTUNITIES_FILE = "/Users/bjh/Documents/tabiji/scripts/all-discovered-opportunities.json"
OUTPUT_FILE = "/Users/bjh/Documents/tabiji/compare-keyword-opportunities.csv"
PROGRESS_FILE = "/Users/bjh/Documents/tabiji/scripts/discovery-progress.json"

DESTINATIONS = {
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
    "hawaii", "alaska", "california", "florida", "colorado", "texas",
    "pacific northwest", "new england",
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
    "beijing", "shanghai", "guilin", "chengdu", "lhasa",
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
    "french riviera", "chamonix",
    "zakynthos", "paros", "naxos", "milos", "meteora", "thessaloniki",
    "galway", "cork", "killarney", "belfast",
    "bath", "oxford", "cambridge", "york", "brighton", "liverpool",
    "manchester", "lake district", "cotswolds", "cornwall",
    "tallinn", "riga", "vilnius",
    "bucharest", "transylvania", "sofia",
    "belgrade", "kotor", "tirana", "ohrid", "bled", "bratislava",
    "valletta", "gozo", "nicosia", "paphos",
    "maui", "big island", "kauai", "oahu", "waikiki",
    "turks and caicos", "st lucia", "antigua", "bermuda",
    "bora bora", "moorea", "whitsundays", "gold coast", "byron bay",
    "cabo", "cabo san lucas", "puerto vallarta", "riviera maya",
    "punta cana", "los cabos", "costa brava", "costa del sol",
    "french polynesia", "cook islands",
    "patagonia", "galapagos", "amazon", "yosemite", "yellowstone",
    "grand canyon", "banff", "jasper", "glacier national park",
    "scottish highlands", "norwegian fjords", "swiss alps",
    "canadian rockies", "lapland", "lofoten",
    "queenstown", "milford sound", "abel tasman", "wanaka",
    "kruger", "serengeti", "masai mara", "okavango delta",
    "kilimanjaro", "everest base camp", "annapurna",
    "torres del paine", "iguazu falls", "angel falls",
    "lake bled", "plitvice", "lake atitlan", "lake titicaca",
    "mallorca", "guadalajara",
    # Additional destinations for expanded search
    "doha", "muscat", "manama", "abu dhabi",
    "luang prabang", "siem reap", "phnom penh",
    "cusco", "la paz", "quito", "santiago",
    "fez", "tangier", "chefchaouen",
    "essaouira", "rabat", "casablanca",
    "luxor", "aswan", "hurghada", "sharm el sheikh",
    "jaipur", "udaipur", "agra", "rishikesh", "darjeeling",
    "ella", "sigiriya", "trincomalee",
    "nusa penida", "komodo", "raja ampat",
    "koh phi phi", "koh lanta", "koh tao",
    "hvar", "kotor", "mostar", "ohrid",
    "bruges", "ghent", "luxembourg city",
    "granada", "malaga", "san sebastian",
    "nice", "cannes", "saint tropez",
    "positano", "ravello", "sorrento", "taormina",
    "lake garda", "lake maggiore",
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
    parts = keyword.lower().split(" vs ")
    if len(parts) != 2:
        return False
    side1 = parts[0].strip()
    side2 = parts[1].strip()
    if side1 == side2:
        return False
    return side1 in DESTINATIONS and side2 in DESTINATIONS

def get_phrase_keywords(phrase):
    url = (
        f"https://api.semrush.com/"
        f"?type=phrase_fullsearch"
        f"&key={API_KEY}"
        f"&phrase={urllib.parse.quote(phrase)}"
        f"&database={DATABASE}"
        f"&export_columns=Ph,Nq"
        f"&display_limit=200"
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

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"completed_seeds": [], "discovered": {}}

def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)

def main():
    with open(EXISTING_SLUGS_FILE) as f:
        existing = set(json.load(f))

    # Also include current queue slugs
    with open(QUEUE_FILE) as f:
        queue = json.load(f)
    for item in queue:
        slug = item["slug"]
        existing.add(slug)
        existing.add(reverse_slug(slug))

    print(f"Loaded {len(existing)} existing slugs (including reverses)")

    # Expanded seed list - cities, countries, regions, islands
    seeds = sorted(set([
        # Major cities (tier 1)
        "london vs", "paris vs", "amsterdam vs", "tokyo vs", "rome vs",
        "barcelona vs", "lisbon vs", "berlin vs", "prague vs", "vienna vs",
        "dubai vs", "bangkok vs", "seoul vs", "istanbul vs",
        "new york vs", "los angeles vs", "miami vs", "san francisco vs",
        "sydney vs", "melbourne vs", "toronto vs", "vancouver vs",
        "singapore vs", "hong kong vs", "taipei vs",
        # Cities tier 2
        "florence vs", "venice vs", "naples vs", "milan vs",
        "madrid vs", "seville vs", "porto vs", "nice vs", "monaco vs",
        "edinburgh vs", "dublin vs", "copenhagen vs", "stockholm vs",
        "oslo vs", "helsinki vs", "budapest vs", "krakow vs",
        "marrakech vs", "cairo vs", "athens vs",
        "kyoto vs", "osaka vs", "hanoi vs", "ho chi minh city vs",
        "chiang mai vs", "da nang vs",
        "buenos aires vs", "rio de janeiro vs", "mexico city vs",
        "lima vs", "bogota vs", "medellin vs", "cartagena vs",
        "dubrovnik vs", "split vs", "zurich vs", "salzburg vs", "munich vs",
        # Cities tier 3
        "chicago vs", "seattle vs", "boston vs", "austin vs", "denver vs",
        "san diego vs", "portland vs", "new orleans vs",
        "brisbane vs", "perth vs", "auckland vs", "wellington vs",
        "montreal vs", "quebec city vs", "calgary vs",
        "kuala lumpur vs", "penang vs", "manila vs", "cebu vs",
        "jakarta vs", "yogyakarta vs",
        "mumbai vs", "delhi vs", "goa vs", "jaipur vs",
        "colombo vs", "kathmandu vs",
        "tbilisi vs", "yerevan vs",
        "nairobi vs", "cape town vs",
        "tel aviv vs", "amman vs",
        "tallinn vs", "riga vs", "vilnius vs",
        "bucharest vs", "sofia vs", "belgrade vs",
        "tirana vs", "bratislava vs",
        "lyon vs", "bordeaux vs", "marseille vs",
        "malaga vs", "granada vs", "san sebastian vs",
        "hamburg vs", "cologne vs", "frankfurt vs",
        "bruges vs", "ghent vs", "antwerp vs",
        "thessaloniki vs", "rhodes vs",
        # Islands & beach
        "santorini vs", "mykonos vs", "crete vs", "corfu vs",
        "bali vs", "phuket vs", "cancun vs",
        "maui vs", "oahu vs", "kauai vs", "big island vs",
        "tulum vs", "playa del carmen vs", "cabo vs", "puerto vallarta vs",
        "punta cana vs", "jamaica vs", "barbados vs", "bahamas vs",
        "aruba vs", "curacao vs", "st lucia vs", "antigua vs", "bermuda vs",
        "turks and caicos vs",
        "maldives vs", "fiji vs", "bora bora vs",
        "sardinia vs", "sicily vs", "mallorca vs", "ibiza vs",
        "tenerife vs", "gran canaria vs", "lanzarote vs",
        "zakynthos vs", "paros vs", "naxos vs", "milos vs",
        "koh samui vs", "krabi vs",
        "boracay vs", "siargao vs", "el nido vs", "palawan vs",
        "zanzibar vs", "mauritius vs", "seychelles vs",
        "lombok vs",
        # Regions & nature
        "amalfi coast vs", "cinque terre vs", "lake como vs",
        "tuscany vs", "puglia vs", "dolomites vs",
        "algarve vs", "azores vs", "madeira vs",
        "provence vs", "french riviera vs", "chamonix vs",
        "scottish highlands vs", "lake district vs", "cotswolds vs", "cornwall vs",
        "patagonia vs", "galapagos vs",
        "banff vs", "jasper vs",
        "norwegian fjords vs", "lofoten vs", "lapland vs",
        "swiss alps vs", "interlaken vs", "zermatt vs",
        "queenstown vs", "wanaka vs",
        # Countries
        "italy vs", "spain vs", "france vs", "portugal vs", "greece vs",
        "croatia vs", "turkey vs", "thailand vs", "japan vs", "mexico vs",
        "costa rica vs", "colombia vs", "peru vs", "argentina vs",
        "morocco vs", "egypt vs", "iceland vs", "norway vs",
        "switzerland vs", "austria vs", "germany vs", "netherlands vs",
        "ireland vs", "scotland vs", "england vs",
        "australia vs", "new zealand vs", "canada vs",
        "vietnam vs", "south korea vs", "taiwan vs",
        "indonesia vs", "malaysia vs", "philippines vs",
        "india vs", "sri lanka vs", "nepal vs",
        "cambodia vs", "laos vs",
        "belize vs", "panama vs", "guatemala vs", "honduras vs", "nicaragua vs",
        "dominican republic vs", "jamaica vs", "cuba vs",
        "brazil vs", "chile vs", "ecuador vs", "bolivia vs", "uruguay vs",
        "kenya vs", "tanzania vs", "south africa vs", "namibia vs",
        "botswana vs", "ethiopia vs", "ghana vs",
        "jordan vs", "oman vs", "uae vs", "qatar vs", "bahrain vs",
        "israel vs", "lebanon vs",
        "georgia vs", "armenia vs", "azerbaijan vs",
        "uzbekistan vs", "kyrgyzstan vs", "mongolia vs",
        "sweden vs", "denmark vs", "finland vs", "belgium vs",
        "luxembourg vs", "czech republic vs",
        "poland vs", "hungary vs", "romania vs", "bulgaria vs",
        "serbia vs", "montenegro vs", "albania vs",
        "slovenia vs", "slovakia vs", "malta vs", "cyprus vs",
        "estonia vs", "latvia vs", "lithuania vs",
        "hawaii vs", "fiji vs", "maldives vs", "samoa vs",
        "puerto rico vs",
    ]))

    progress = load_progress()
    discovered = progress.get("discovered", {})
    completed_seeds = set(progress.get("completed_seeds", []))

    remaining_seeds = [s for s in seeds if s not in completed_seeds]
    print(f"Total seeds: {len(seeds)}, already done: {len(completed_seeds)}, remaining: {len(remaining_seeds)}")
    print(f"Previously discovered: {len(discovered)}")

    for i, seed in enumerate(remaining_seeds):
        print(f"[{i+1}/{len(remaining_seeds)}] '{seed}'...", end=" ", flush=True)

        results = get_phrase_keywords(seed)
        time.sleep(0.2)

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

        completed_seeds.add(seed)
        print(f"{len(results)} raw, {new_count} new travel")

        if (i + 1) % 25 == 0:
            progress["completed_seeds"] = list(completed_seeds)
            progress["discovered"] = discovered
            save_progress(progress)
            print(f"  [Progress saved, {len(discovered)} total discoveries]")

    # Final save of discovery phase
    progress["completed_seeds"] = list(completed_seeds)
    progress["discovered"] = discovered
    save_progress(progress)

    print(f"\n{'='*60}")
    print(f"Total unique new travel opportunities: {len(discovered)}")

    # Now verify volumes for ALL discoveries (both directions)
    all_items = sorted(discovered.values(), key=lambda x: x["volume"], reverse=True)
    print(f"Verifying reverse volumes for {len(all_items)} items...")

    results = []
    for i, item in enumerate(all_items):
        slug = item["slug"]
        parts = slug.split("-vs-")
        if len(parts) != 2:
            continue

        dest1 = parts[0].replace("-", " ")
        dest2 = parts[1].replace("-", " ")
        kw1 = f"{dest1} vs {dest2}"
        kw2 = f"{dest2} vs {dest1}"

        if (i + 1) % 50 == 0:
            print(f"  [{i+1}/{len(all_items)}] {slug}...")

        vol1 = get_single_volume(kw1)
        time.sleep(0.12)
        vol2 = get_single_volume(kw2)
        time.sleep(0.12)

        total = vol1 + vol2
        best_kw = kw1 if vol1 >= vol2 else kw2
        best_vol = max(vol1, vol2)

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

    # Sort by total volume
    results.sort(key=lambda r: r["total_vol"], reverse=True)
    with_volume = [r for r in results if r["total_vol"] > 0]

    # Write ALL to CSV
    fieldnames = ["slug", "url", "keyword_1", "vol_1", "keyword_2", "vol_2", "best_keyword", "best_vol", "total_vol"]
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(with_volume)

    # Also save as JSON for easy loading
    with open(ALL_OPPORTUNITIES_FILE, "w") as f:
        json.dump(with_volume, f, indent=2)

    print(f"\n{'='*60}")
    print(f"Total with search volume > 0: {len(with_volume)}")
    print(f"CSV written to {OUTPUT_FILE}")
    print(f"JSON written to {ALL_OPPORTUNITIES_FILE}")

    print(f"\nTop 25:")
    for r in with_volume[:25]:
        print(f"  {r['slug']}: {r['total_vol']:,} ({r['best_keyword']} = {r['best_vol']:,})")

if __name__ == "__main__":
    main()
