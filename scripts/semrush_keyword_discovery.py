#!/usr/bin/env python3
"""
Discover new compare page opportunities using Semrush keyword research.
Queries "X vs" for popular cities/countries and finds high-volume keywords
we don't already have.
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

# Seed queries - popular travel cities and countries
SEED_QUERIES = [
    # Major cities
    "london vs", "paris vs", "amsterdam vs", "tokyo vs", "rome vs",
    "barcelona vs", "lisbon vs", "berlin vs", "prague vs", "vienna vs",
    "dubai vs", "bangkok vs", "singapore vs", "seoul vs", "istanbul vs",
    "new york vs", "los angeles vs", "miami vs", "san francisco vs",
    "sydney vs", "melbourne vs", "toronto vs", "vancouver vs",
    "bali vs", "phuket vs", "cancun vs", "cape town vs",
    "florence vs", "venice vs", "naples vs", "milan vs",
    "madrid vs", "seville vs", "porto vs", "nice vs", "monaco vs",
    "edinburgh vs", "dublin vs", "copenhagen vs", "stockholm vs",
    "oslo vs", "helsinki vs", "budapest vs", "krakow vs",
    "marrakech vs", "cairo vs", "athens vs", "santorini vs",
    "kyoto vs", "osaka vs", "hong kong vs", "taipei vs",
    "hanoi vs", "ho chi minh city vs", "chiang mai vs",
    "buenos aires vs", "rio de janeiro vs", "mexico city vs",
    "lima vs", "bogota vs", "medellin vs", "cartagena vs",
    # Countries
    "italy vs", "spain vs", "france vs", "portugal vs", "greece vs",
    "croatia vs", "turkey vs", "thailand vs", "japan vs", "mexico vs",
    "costa rica vs", "colombia vs", "peru vs", "argentina vs",
    "morocco vs", "egypt vs", "iceland vs", "norway vs",
    "switzerland vs", "austria vs", "germany vs", "netherlands vs",
    "ireland vs", "scotland vs", "england vs",
    "australia vs", "new zealand vs", "canada vs",
    "vietnam vs", "south korea vs", "taiwan vs",
    "belize vs", "panama vs", "dominican republic vs",
    "hawaii vs", "maui vs", "fiji vs", "maldives vs",
]

def keyword_to_slug(keyword):
    """Convert 'paris vs london' to 'paris-vs-london'."""
    slug = keyword.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug

def reverse_slug(slug):
    parts = slug.split("-vs-")
    if len(parts) == 2:
        return f"{parts[1]}-vs-{parts[0]}"
    return slug

def get_related_keywords(phrase):
    """Get phrase match keywords from Semrush."""
    url = (
        f"https://api.semrush.com/"
        f"?type=phrase_related"
        f"&key={API_KEY}"
        f"&phrase={urllib.parse.quote(phrase)}"
        f"&database={DATABASE}"
        f"&export_columns=Ph,Nq"
        f"&display_limit=50"
        f"&display_filter=%2B%7CPh%7CCo%7Cvs"
    )
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8").strip()
            lines = body.split("\n")
            results = []
            for line in lines[1:]:  # skip header
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
        print(f"  Error for '{phrase}': {e}", file=sys.stderr)
        return []

def get_phrase_match(phrase):
    """Get phrase match keywords from Semrush."""
    url = (
        f"https://api.semrush.com/"
        f"?type=phrase_fullsearch"
        f"&key={API_KEY}"
        f"&phrase={urllib.parse.quote(phrase)}"
        f"&database={DATABASE}"
        f"&export_columns=Ph,Nq"
        f"&display_limit=50"
        f"&display_filter=%2B%7CPh%7CCo%7Cvs"
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
        print(f"  Error for phrase_match '{phrase}': {e}", file=sys.stderr)
        return []


def is_travel_compare(keyword):
    """Filter for travel-relevant comparisons (destinations, not sports/games)."""
    # Exclude obvious non-travel patterns
    exclude_patterns = [
        r'\b(nfl|nba|mlb|nhl|ufc|fifa|premier league|champions league)\b',
        r'\b(game|match|score|playoff|championship|tournament|season|draft)\b',
        r'\b(iphone|samsung|pixel|laptop|cpu|gpu|nvidia|amd|intel|ps5|xbox)\b',
        r'\b(recipe|calories|nutrition|diet|vitamin)\b',
        r'\b(salary|stock|price|cost of living)\b',
        r'\b(university|college|school)\b',
        r'\b(language|population|gdp|economy|military|army|navy)\b',
        r'\b(airline|flight time|time zone|time difference|distance)\b',
        r'\b(visa|passport|currency)\b',
    ]
    kw_lower = keyword.lower()
    for pattern in exclude_patterns:
        if re.search(pattern, kw_lower):
            return False

    # Must have exactly one " vs " splitting two parts
    parts = kw_lower.split(" vs ")
    if len(parts) != 2:
        return False

    # Each side should be reasonable length (1-4 words typically for destinations)
    for part in parts:
        words = part.strip().split()
        if len(words) > 5 or len(words) == 0:
            return False

    return True


def main():
    # Load existing slugs
    with open(EXISTING_SLUGS_FILE) as f:
        existing = set(json.load(f))
    print(f"Loaded {len(existing)} existing slugs (including reverses)")

    # Collect all discovered keywords
    # key: normalized slug, value: {keyword, volume, source}
    discovered = {}

    for i, seed in enumerate(SEED_QUERIES):
        print(f"[{i+1}/{len(SEED_QUERIES)}] Querying '{seed}'...", end=" ", flush=True)

        # Get both related and phrase match results
        related = get_related_keywords(seed)
        time.sleep(0.2)
        phrase = get_phrase_match(seed)
        time.sleep(0.2)

        combined = {}
        for kw, vol in related + phrase:
            if kw in combined:
                combined[kw] = max(combined[kw], vol)
            else:
                combined[kw] = vol

        new_count = 0
        for kw, vol in combined.items():
            if not is_travel_compare(kw):
                continue

            slug = keyword_to_slug(kw)
            rev = reverse_slug(slug)

            # Skip if we already have this (either direction)
            if slug in existing or rev in existing:
                continue

            # Use canonical slug (alphabetical order of the two sides)
            canonical = min(slug, rev)

            if canonical not in discovered or vol > discovered[canonical]["volume"]:
                discovered[canonical] = {
                    "keyword": kw,
                    "slug": canonical,
                    "volume": vol,
                    "source": seed.strip(),
                }
                new_count += 1

        print(f"found {len(combined)} keywords, {new_count} new travel opportunities")

    # Now for top discoveries, get the reverse keyword volume too
    print(f"\nTotal unique new opportunities: {len(discovered)}")
    print("Fetching reverse volumes for top candidates...")

    # Sort by volume and take top 200 to check reverses
    top_candidates = sorted(discovered.values(), key=lambda x: x["volume"], reverse=True)[:200]

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

        # We already have one direction's volume, get the other
        print(f"  [{i+1}/200] Checking reverse for '{slug}'...", end=" ", flush=True)

        # Query both to be precise
        from urllib.request import urlopen, Request

        def get_vol(keyword):
            url = (
                f"https://api.semrush.com/"
                f"?type=phrase_this"
                f"&key={API_KEY}"
                f"&phrase={urllib.parse.quote(keyword)}"
                f"&database={DATABASE}"
                f"&export_columns=Ph,Nq"
            )
            try:
                with urlopen(Request(url), timeout=15) as resp:
                    body = resp.read().decode("utf-8").strip()
                    lines = body.split("\n")
                    if len(lines) >= 2:
                        p = lines[1].split(";")
                        if len(p) >= 2:
                            return int(p[1])
                return 0
            except:
                return 0

        vol1 = get_vol(kw1)
        time.sleep(0.15)
        vol2 = get_vol(kw2)
        time.sleep(0.15)

        total = vol1 + vol2
        best_kw = kw1 if vol1 >= vol2 else kw2
        best_vol = max(vol1, vol2)

        print(f"vol1={vol1}, vol2={vol2}, total={total}")

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

    # Write top 100
    top100 = results[:100]

    fieldnames = ["slug", "url", "keyword_1", "vol_1", "keyword_2", "vol_2", "best_keyword", "best_vol", "total_vol"]
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(top100)

    print(f"\nTop 100 new opportunities written to {OUTPUT_FILE}")
    print(f"Top 10:")
    for r in top100[:10]:
        print(f"  {r['slug']}: {r['total_vol']:,} total ({r['best_keyword']} = {r['best_vol']:,})")

if __name__ == "__main__":
    main()
