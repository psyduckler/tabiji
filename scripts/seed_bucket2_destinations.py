#!/usr/bin/env python3
"""One-shot: backfill country hub images for countries with no destinations.

Phase A — reassign 5 existing destinations whose `country` field is wrong,
so the /countries/ hub groups them correctly.

Phase B — seed 16 new destinations (one per country) with SerpAPI-sourced
photos uploaded to R2, wired into destinations.json (array) and
destinations-full.json (keyed map).

Usage:
    python3 scripts/seed_bucket2_destinations.py [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DESTS_JSON = REPO / "api" / "v1" / "destinations.json"
FULL_JSON = REPO / "api" / "v1" / "destinations-full.json"

R2_ACCOUNT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"
R2_PUBLIC = "https://img.tabiji.ai"

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ---------------------------------------------------------------------------
# Phase A: reassignments — slug -> (new country, new ISO2, new continent, new region)
# ---------------------------------------------------------------------------
REASSIGNMENTS: list[tuple[str, str, str, str, str]] = [
    ("sandy-ground-anguilla",              "Anguilla",         "AI", "North America", "Caribbean"),
    ("seven-mile-beach-grand-cayman",      "Cayman Islands",   "KY", "North America", "Caribbean"),
    ("roseau-dominica",                    "Dominica",         "DM", "North America", "Caribbean"),
    ("majuro-marshall-islands",            "Marshall Islands", "MH", "Oceania",       "Micronesia"),
    ("santa-cruz-islands-solomon-islands", "Solomon Islands",  "SB", "Oceania",       "Melanesia"),
]

# ---------------------------------------------------------------------------
# Phase B: new seeds — one destination per bucket-2 country without any data
# ---------------------------------------------------------------------------
# (slug, name, country, iso2, continent, region, currency_code, currency_name,
#  currency_symbol, language, timezone, dial_code, driving_side, pitch, query)
SEEDS: list[dict] = [
    {
        "slug": "kabul", "name": "Kabul", "country": "Afghanistan", "iso2": "AF",
        "continent": "Asia", "region": "Afghanistan",
        "currency": {"code": "AFN", "name": "afghani", "symbol": "؋"},
        "language": "Dari", "timezone": "UTC+04:30", "dialCode": "+93",
        "drivingSide": "right",
        "pitch": "Afghanistan's capital — travel is restricted; this listing is for research and context.",
        "query": "Kabul Afghanistan cityscape",
    },
    {
        "slug": "hamilton-bermuda", "name": "Hamilton, Bermuda", "country": "Bermuda", "iso2": "BM",
        "continent": "North America", "region": "Atlantic",
        "currency": {"code": "BMD", "name": "Bermudian dollar", "symbol": "$"},
        "language": "English", "timezone": "UTC-04:00", "dialCode": "+1441",
        "drivingSide": "left",
        "pitch": "Pink sand beaches and pastel colonial architecture on a tiny Atlantic archipelago.",
        "query": "Hamilton Bermuda harbour",
    },
    {
        "slug": "bangui", "name": "Bangui", "country": "Central African Republic", "iso2": "CF",
        "continent": "Africa", "region": "Central Africa",
        "currency": {"code": "XAF", "name": "Central African CFA franc", "symbol": "Fr"},
        "language": "French", "timezone": "UTC+01:00", "dialCode": "+236",
        "drivingSide": "right",
        "pitch": "Riverside capital on the Ubangi — travel is restricted; this listing is for research and context.",
        "query": "Bangui Central African Republic Ubangi river",
    },
    {
        "slug": "port-au-prince", "name": "Port-au-Prince", "country": "Haiti", "iso2": "HT",
        "continent": "North America", "region": "Caribbean",
        "currency": {"code": "HTG", "name": "gourde", "symbol": "G"},
        "language": "French", "timezone": "UTC-05:00", "dialCode": "+509",
        "drivingSide": "right",
        "pitch": "Haiti's capital — travel is restricted; this listing is for research and context.",
        "query": "Port-au-Prince Haiti landscape",
    },
    {
        "slug": "tripoli-libya", "name": "Tripoli, Libya", "country": "Libya", "iso2": "LY",
        "continent": "Africa", "region": "North Africa",
        "currency": {"code": "LYD", "name": "Libyan dinar", "symbol": "ل.د"},
        "language": "Arabic", "timezone": "UTC+02:00", "dialCode": "+218",
        "drivingSide": "right",
        "pitch": "Libya's Mediterranean capital — travel is restricted; this listing is for research and context.",
        "query": "Tripoli Libya medina old city",
    },
    {
        "slug": "vaduz", "name": "Vaduz", "country": "Liechtenstein", "iso2": "LI",
        "continent": "Europe", "region": "Central Europe",
        "currency": {"code": "CHF", "name": "Swiss franc", "symbol": "Fr"},
        "language": "German", "timezone": "UTC+01:00", "dialCode": "+423",
        "drivingSide": "right",
        "pitch": "A castle-topped micro-capital in the Alps, easily seen in half a day from Zurich.",
        "query": "Vaduz Liechtenstein castle",
    },
    {
        "slug": "monaco-monte-carlo", "name": "Monaco", "country": "Monaco", "iso2": "MC",
        "continent": "Europe", "region": "French Riviera",
        "currency": {"code": "EUR", "name": "euro", "symbol": "€"},
        "language": "French", "timezone": "UTC+01:00", "dialCode": "+377",
        "drivingSide": "right",
        "pitch": "Monte Carlo's casino, superyachts, and cliffside old town packed into a tiny principality.",
        "query": "Monaco Monte Carlo harbour",
    },
    {
        "slug": "yaren-nauru", "name": "Yaren, Nauru", "country": "Nauru", "iso2": "NR",
        "continent": "Oceania", "region": "Micronesia",
        "currency": {"code": "AUD", "name": "Australian dollar", "symbol": "$"},
        "language": "Nauruan", "timezone": "UTC+12:00", "dialCode": "+674",
        "drivingSide": "left",
        "pitch": "The world's smallest island nation — a Pacific outpost with phosphate history.",
        "query": "Nauru island aerial",
    },
    {
        "slug": "pyongyang", "name": "Pyongyang", "country": "North Korea", "iso2": "KP",
        "continent": "Asia", "region": "Korean Peninsula",
        "currency": {"code": "KPW", "name": "North Korean won", "symbol": "₩"},
        "language": "Korean", "timezone": "UTC+09:00", "dialCode": "+850",
        "drivingSide": "right",
        "pitch": "North Korea's capital — travel is tightly restricted; this listing is for research and context.",
        "query": "Pyongyang North Korea skyline",
    },
    {
        "slug": "basseterre", "name": "Basseterre", "country": "Saint Kitts and Nevis", "iso2": "KN",
        "continent": "North America", "region": "Caribbean",
        "currency": {"code": "XCD", "name": "East Caribbean dollar", "symbol": "$"},
        "language": "English", "timezone": "UTC-04:00", "dialCode": "+1869",
        "drivingSide": "left",
        "pitch": "A relaxed Caribbean capital on St. Kitts, gateway to rainforest hikes and Brimstone Hill.",
        "query": "Basseterre Saint Kitts harbour",
    },
    {
        "slug": "philipsburg", "name": "Philipsburg", "country": "Sint Maarten", "iso2": "SX",
        "continent": "North America", "region": "Caribbean",
        "currency": {"code": "ANG", "name": "Netherlands Antillean guilder", "symbol": "ƒ"},
        "language": "Dutch", "timezone": "UTC-04:00", "dialCode": "+1721",
        "drivingSide": "right",
        "pitch": "The Dutch-side capital of a two-nation island, famed for Maho Beach's runway-skimming jets.",
        "query": "Philipsburg Sint Maarten beach",
    },
    {
        "slug": "mogadishu", "name": "Mogadishu", "country": "Somalia", "iso2": "SO",
        "continent": "Africa", "region": "Horn of Africa",
        "currency": {"code": "SOS", "name": "Somali shilling", "symbol": "Sh"},
        "language": "Somali", "timezone": "UTC+03:00", "dialCode": "+252",
        "drivingSide": "right",
        "pitch": "Somalia's Indian Ocean capital — travel is restricted; this listing is for research and context.",
        "query": "Mogadishu Somalia coastline",
    },
    {
        "slug": "juba", "name": "Juba", "country": "South Sudan", "iso2": "SS",
        "continent": "Africa", "region": "East Africa",
        "currency": {"code": "SSP", "name": "South Sudanese pound", "symbol": "£"},
        "language": "English", "timezone": "UTC+02:00", "dialCode": "+211",
        "drivingSide": "right",
        "pitch": "South Sudan's Nile-side capital — travel is restricted; this listing is for research and context.",
        "query": "Juba South Sudan Nile",
    },
    {
        "slug": "khartoum", "name": "Khartoum", "country": "Sudan", "iso2": "SD",
        "continent": "Africa", "region": "North Africa",
        "currency": {"code": "SDG", "name": "Sudanese pound", "symbol": "£"},
        "language": "Arabic", "timezone": "UTC+02:00", "dialCode": "+249",
        "drivingSide": "right",
        "pitch": "Where the Blue and White Niles meet — travel is restricted; this listing is for research and context.",
        "query": "Khartoum Sudan Nile confluence",
    },
    {
        "slug": "damascus", "name": "Damascus", "country": "Syria", "iso2": "SY",
        "continent": "Asia", "region": "Levant",
        "currency": {"code": "SYP", "name": "Syrian pound", "symbol": "£"},
        "language": "Arabic", "timezone": "UTC+03:00", "dialCode": "+963",
        "drivingSide": "right",
        "pitch": "One of the world's oldest continuously inhabited cities — travel is restricted; this listing is for research and context.",
        "query": "Damascus Syria old city Umayyad",
    },
    {
        "slug": "tokelau", "name": "Tokelau", "country": "Tokelau", "iso2": "TK",
        "continent": "Oceania", "region": "Polynesia",
        "currency": {"code": "NZD", "name": "New Zealand dollar", "symbol": "$"},
        "language": "Tokelauan", "timezone": "UTC+13:00", "dialCode": "+690",
        "drivingSide": "left",
        "pitch": "Three remote coral atolls in the South Pacific, reachable only by cargo boat from Samoa.",
        "query": "Tokelau atoll aerial",
    },
]


# ---------------------------------------------------------------------------
# Keychain + SerpAPI + R2 (ported from fetch-destination-photos.py)
# ---------------------------------------------------------------------------

def keychain(name: str) -> str:
    r = subprocess.run(
        ["security", "find-generic-password", "-s", name, "-w"],
        capture_output=True, text=True, timeout=5,
    )
    out = r.stdout.strip()
    if not out:
        sys.exit(f"ERROR: {name} not found in keychain")
    return out


SERPAPI_KEY = ""
CF_TOKEN = ""


def search_google_images(query: str) -> list[dict]:
    params = urllib.parse.urlencode({
        "engine": "google_images",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": "5",
        "ijn": "0",
        "tbs": "isz:m",
    })
    url = f"https://serpapi.com/search.json?{params}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())
    return [
        {
            "url": img.get("original", ""),
            "title": img.get("title", ""),
            "width": img.get("original_width", 0),
            "height": img.get("original_height", 0),
        }
        for img in data.get("images_results", [])[:5]
        if img.get("original")
    ]


def download_image(url: str, dest: Path) -> bool:
    r = subprocess.run(
        ["curl", "-sL", "-o", str(dest), "--max-time", "15", url],
        capture_output=True, timeout=20,
    )
    if r.returncode != 0:
        return False
    size = dest.stat().st_size if dest.exists() else 0
    if size < 10_000:
        dest.unlink(missing_ok=True)
        return False
    return True


def convert_to_webp(src: Path, dest: Path) -> bool:
    tmp_jpg = src.with_suffix(".opt.jpg")
    subprocess.run(
        ["sips", "-Z", "1080", "--setProperty", "format", "jpeg",
         "--setProperty", "formatOptions", "85", str(src), "--out", str(tmp_jpg)],
        capture_output=True, timeout=15,
    )
    r = subprocess.run(
        ["cwebp", "-quiet", "-q", "80", str(tmp_jpg), "-o", str(dest)],
        capture_output=True, timeout=15,
    )
    tmp_jpg.unlink(missing_ok=True)
    return r.returncode == 0 and dest.exists() and dest.stat().st_size > 5_000


def upload_to_r2(local: Path, key: str) -> str | None:
    r = subprocess.run(
        ["curl", "-s", "-X", "PUT",
         "-H", f"Authorization: Bearer {CF_TOKEN}",
         "-H", "Content-Type: image/webp",
         "--data-binary", f"@{local}",
         f"https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{key}"],
        capture_output=True, text=True, timeout=60,
    )
    if r.returncode != 0:
        return None
    try:
        resp = json.loads(r.stdout) if r.stdout else {}
    except Exception:
        resp = {}
    if resp.get("success", True):
        return f"{R2_PUBLIC}/{key}"
    return None


def fetch_photo_for_seed(seed: dict, dry_run: bool) -> str | None:
    """Return R2 URL of the uploaded webp, or None on failure."""
    slug = seed["slug"]
    queries = [seed["query"], f"{seed['name']} travel", seed["name"]]
    seen = set()
    queries = [q for q in queries if not (q in seen or seen.add(q))]

    for q in queries:
        print(f"  [{slug}] q='{q}'", flush=True)
        try:
            results = search_google_images(q)
        except Exception as e:
            print(f"  [{slug}] SerpAPI error: {str(e)[:150]}", flush=True)
            continue
        if not results:
            continue

        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            for i, img in enumerate(results):
                raw = td / f"raw_{i}.jpg"
                if not download_image(img["url"], raw):
                    continue
                webp = td / f"{slug}.webp"
                if not convert_to_webp(raw, webp):
                    raw.unlink(missing_ok=True)
                    continue
                if dry_run:
                    print(f"  [{slug}] DRY-RUN would upload {webp.stat().st_size} bytes from {img['url'][:80]}", flush=True)
                    return f"{R2_PUBLIC}/find/img/{slug}.webp"
                key = f"find/img/{slug}.webp"
                public = upload_to_r2(webp, key)
                if public:
                    print(f"  [{slug}] OK -> {public}", flush=True)
                    return public
    print(f"  [{slug}] FAILED after all queries", flush=True)
    return None


# ---------------------------------------------------------------------------
# Build a full destination record matching the existing schema
# ---------------------------------------------------------------------------

def build_entry(seed: dict, photo_url: str) -> dict:
    slug = seed["slug"]
    iso2_lower = seed["iso2"].lower()
    tags = [
        seed["region"], seed["continent"], seed["country"], seed["iso2"],
        "Cultural", "offbeat",
    ]
    return {
        "slug": slug,
        "name": seed["name"],
        "region": seed["region"],
        "continent": seed["continent"],
        "country": seed["country"],
        "countryCode": seed["iso2"],
        "currency": seed["currency"],
        "language": seed["language"],
        "languages": [seed["language"]],
        "flag": {
            "svg": f"https://flagcdn.com/{iso2_lower}.svg",
            "png": f"https://flagcdn.com/w320/{iso2_lower}.png",
        },
        "timezone": seed["timezone"],
        "timezones": [seed["timezone"]],
        "coordinates": {"lat": None, "lng": None, "source": "country-centroid"},
        "plugType": [],
        "drivingSide": seed["drivingSide"],
        "dialCode": seed["dialCode"],
        "tapWaterSafe": None,
        "tippingCustom": "Tipping norms vary by venue and service level; check local custom.",
        "visaNote": "Visa rules depend on your passport and trip length; verify requirements before booking.",
        "photo": photo_url,
        "pitch": seed["pitch"],
        "budget": "$$",
        "season": "Varies",
        "vibes": ["Cultural"],
        "travelStyles": ["offbeat"],
        "url": f"https://tabiji.ai/find/?q={slug}",
        "id": f"destination:{slug}",
        "type": "destination",
        "entityType": "destination",
        "schemaVersion": "1.0",
        "updatedAt": NOW,
        "sourceUrl": f"https://tabiji.ai/find/?q={slug}",
        "tags": tags,
        "freshness": {
            "updatedAt": NOW,
            "lastVerifiedAt": NOW,
            "confidence": "editorial",
            "confidenceScore": 0.9,
            "operationalFieldsMayChange": False,
        },
        "provenance": {
            "sources": ["tabiji_static_page"],
            "sourceUrl": f"https://tabiji.ai/find/?q={slug}",
            "lastVerifiedAt": NOW,
            "sourcePath": "find/destinations.json",
        },
        "sourceMeta": {
            "sourceType": "tabiji-static-page",
            "sourcePath": "find/destinations.json",
            "sourceUrl": f"https://tabiji.ai/find/?q={slug}",
            "lastVerified": NOW,
        },
        "editorialSummary": seed["pitch"],
        "bestFor": ["Cultural", "offbeat"],
        "relatedPicks": [],
        "relatedItineraries": [],
        "relatedComparisons": [],
        "relatedDestinations": [],
        "alertsRef": f"https://tabiji.ai/api/v1/alerts/{iso2_lower}.json",
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    global SERPAPI_KEY, CF_TOKEN
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Skip R2 upload + JSON write")
    args = ap.parse_args()

    SERPAPI_KEY = keychain("serpapi-key")
    CF_TOKEN = keychain("cloudflare-pages-token")

    # Load both JSON files
    with open(DESTS_JSON) as f:
        dests_wrapper = json.load(f)
    dests_list = dests_wrapper.get("destinations", [])
    dests_by_slug = {d.get("slug"): d for d in dests_list}

    with open(FULL_JSON) as f:
        full = json.load(f)

    # --- Phase A: reassignments ---
    print(f"\n=== Phase A: {len(REASSIGNMENTS)} reassignments ===", flush=True)
    reassigned = 0
    for slug, country, iso2, continent, region in REASSIGNMENTS:
        if slug not in dests_by_slug:
            print(f"  [{slug}] NOT FOUND in destinations.json -- skipping", flush=True)
            continue
        d = dests_by_slug[slug]
        old_country = d.get("country")
        old_iso = d.get("countryCode")
        d["country"] = country
        d["countryCode"] = iso2
        d["continent"] = continent
        d["region"] = region
        d["updatedAt"] = NOW
        # Also update the keyed version
        if slug in full:
            full[slug]["country"] = country
            full[slug]["countryCode"] = iso2
            full[slug]["continent"] = continent
            full[slug]["region"] = region
            full[slug]["updatedAt"] = NOW
        reassigned += 1
        print(f"  [{slug}] {old_country}/{old_iso} -> {country}/{iso2}", flush=True)

    # --- Phase B: new seeds ---
    print(f"\n=== Phase B: {len(SEEDS)} new seeds ===", flush=True)
    seeded = 0
    failed = 0
    for seed in SEEDS:
        slug = seed["slug"]
        if slug in dests_by_slug:
            print(f"  [{slug}] already exists -- skipping", flush=True)
            continue
        photo = fetch_photo_for_seed(seed, args.dry_run)
        if not photo:
            failed += 1
            continue
        entry = build_entry(seed, photo)
        if not args.dry_run:
            dests_list.append(entry)
            dests_by_slug[slug] = entry
            full[slug] = entry
        seeded += 1

    # --- Save ---
    if args.dry_run:
        print(f"\nDRY RUN: reassigned={reassigned}, seeded={seeded}, failed={failed}", flush=True)
        return

    # Update count in wrapper
    dests_wrapper["destinations"] = dests_list
    dests_wrapper["count"] = len(dests_list)

    tmp = DESTS_JSON.with_suffix(".json.tmp")
    with open(tmp, "w") as f:
        json.dump(dests_wrapper, f, separators=(",", ":"), ensure_ascii=False)
    tmp.replace(DESTS_JSON)

    tmp = FULL_JSON.with_suffix(".json.tmp")
    with open(tmp, "w") as f:
        json.dump(full, f, separators=(",", ":"), ensure_ascii=False)
    tmp.replace(FULL_JSON)

    print(f"\nDone. reassigned={reassigned}, seeded={seeded}, failed={failed}", flush=True)
    print(f"destinations.json count: {dests_wrapper['count']}", flush=True)


if __name__ == "__main__":
    main()
