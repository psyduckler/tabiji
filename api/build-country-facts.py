#!/usr/bin/env python3
"""
Build country facts API endpoint from restcountries.com data.

Outputs:
  - api/v1/countries.json        (catalog)
  - api/v1/countries/{iso2}.json (individual files)

Usage:
  python3 api/build-country-facts.py [--cache /path/to/cached.json]
"""

import json
import os
import sys
import urllib.request

API_BASE = "https://restcountries.com/v3.1/all"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "v1", "countries")
CATALOG_PATH = os.path.join(SCRIPT_DIR, "v1", "countries.json")


def fetch_batch(fields):
    """Fetch a batch of fields from restcountries (max 10 per request)."""
    url = f"{API_BASE}?fields={','.join(fields)}"
    req = urllib.request.Request(url, headers={"User-Agent": "tabiji-api-builder/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def fetch_all():
    """Fetch all country data in batches (API limits to 10 fields per request)."""
    print("Fetching batch 1/3 (core identity)...")
    batch1 = fetch_batch([
        "name", "cca2", "cca3", "capital", "population",
        "area", "region", "subregion", "borders", "landlocked"
    ])

    print("Fetching batch 2/3 (cultural/practical)...")
    batch2 = fetch_batch([
        "cca2", "demonyms", "startOfWeek", "maps", "currencies",
        "languages", "timezones", "flag", "flags", "car"
    ])

    print("Fetching batch 3/3 (tld/idd)...")
    batch3 = fetch_batch(["cca2", "tld", "idd"])

    # Index batches 2 and 3 by cca2 for merging
    b2_idx = {c["cca2"]: c for c in batch2}
    b3_idx = {c["cca2"]: c for c in batch3}

    merged = []
    for country in batch1:
        iso2 = country.get("cca2", "")
        if not iso2:
            continue
        b2 = b2_idx.get(iso2, {})
        b3 = b3_idx.get(iso2, {})
        country.update(b2)
        country.update(b3)
        merged.append(country)

    return merged


def transform_country(raw):
    """Transform raw restcountries data into our API format."""
    iso2 = raw.get("cca2", "").upper()
    iso3 = raw.get("cca3", "").upper()

    # Dial code from idd
    idd = raw.get("idd", {})
    root = idd.get("root", "")
    suffixes = idd.get("suffixes", [])
    dial_code = f"{root}{suffixes[0]}" if root and suffixes else root or None

    # Demonyms (English only)
    demonyms_raw = raw.get("demonyms", {})
    demonyms_eng = demonyms_raw.get("eng", {})
    demonyms = None
    if demonyms_eng:
        demonyms = {
            "male": demonyms_eng.get("m", ""),
            "female": demonyms_eng.get("f", "")
        }

    # Currencies
    currencies = {}
    for code, info in raw.get("currencies", {}).items():
        currencies[code] = {
            "name": info.get("name", ""),
            "symbol": info.get("symbol", "")
        }

    return {
        "id": f"country:{iso2.lower()}",
        "name": raw.get("name", {}).get("common", ""),
        "officialName": raw.get("name", {}).get("official", ""),
        "iso2": iso2,
        "iso3": iso3,
        "capital": raw.get("capital", []),
        "population": raw.get("population"),
        "area": raw.get("area"),
        "region": raw.get("region", ""),
        "subregion": raw.get("subregion", ""),
        "borders": raw.get("borders", []),
        "landlocked": raw.get("landlocked", False),
        "demonyms": demonyms,
        "startOfWeek": raw.get("startOfWeek", ""),
        "maps": raw.get("maps", {}),
        "currencies": currencies if currencies else None,
        "languages": raw.get("languages", {}),
        "timezones": raw.get("timezones", []),
        "flag": raw.get("flag", ""),
        "flagSvg": raw.get("flags", {}).get("svg", ""),
        "flagPng": raw.get("flags", {}).get("png", ""),
        "drivingSide": raw.get("car", {}).get("side", ""),
        "dialCode": dial_code,
        "tld": raw.get("tld", []),
        "type": "country"
    }


def build():
    """Main build function."""
    # Check for cached raw data
    cache_path = "/tmp/restcountries-raw-merged.json"
    if "--cache" in sys.argv:
        idx = sys.argv.index("--cache")
        if idx + 1 < len(sys.argv):
            cache_path = sys.argv[idx + 1]

    # Fetch or load cached
    if os.path.exists(cache_path) and "--no-cache" not in sys.argv:
        print(f"Loading cached data from {cache_path}")
        with open(cache_path) as f:
            raw_countries = json.load(f)
    else:
        raw_countries = fetch_all()
        # Cache for re-runs
        with open(cache_path, "w") as f:
            json.dump(raw_countries, f)
        print(f"Cached raw data to {cache_path}")

    print(f"Processing {len(raw_countries)} countries...")

    # Transform
    countries = []
    for raw in raw_countries:
        try:
            country = transform_country(raw)
            countries.append(country)
        except Exception as e:
            name = raw.get("name", {}).get("common", "unknown")
            print(f"  Warning: skipping {name}: {e}")

    # Sort by name
    countries.sort(key=lambda c: c["name"])

    # Ensure output dir exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Write individual files
    for country in countries:
        iso2 = country["iso2"].lower()
        path = os.path.join(OUTPUT_DIR, f"{iso2}.json")
        with open(path, "w") as f:
            json.dump(country, f, indent=2, ensure_ascii=False)

    # Write catalog
    catalog = {
        "count": len(countries),
        "countries": countries
    }
    with open(CATALOG_PATH, "w") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Built {len(countries)} country files")
    print(f"   Catalog: {CATALOG_PATH}")
    print(f"   Individual: {OUTPUT_DIR}/")

    # Verify a few
    for test in ["jp", "fr", "us", "sg"]:
        path = os.path.join(OUTPUT_DIR, f"{test}.json")
        if os.path.exists(path):
            with open(path) as f:
                d = json.load(f)
            print(f"   ✓ {test}.json — {d['name']}, pop {d['population']:,}, capital: {d['capital']}")


if __name__ == "__main__":
    build()
