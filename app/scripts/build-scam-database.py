#!/usr/bin/env python3
"""
Build app/data/scams/{slug}.json for each of the 52 scam cities.

Strategy:
- Parse the HTML page at scams/{slug}/index.html for rich structured data
  (scam name, severity badge, location, story, red flags, avoidance tips)
- If HTML parsing yields 0 scams, fall back to safety profile data
  (app/data/safety/{iso2}.json scams array filtered by city name)

Usage: python3 app/scripts/build-scam-database.py
"""

import json
import re
import sys
from pathlib import Path
from datetime import timezone, datetime

try:
    from bs4 import BeautifulSoup
except ImportError:
    print(
        "Missing dependency: beautifulsoup4\n"
        "Install with: python3 -m pip install beautifulsoup4",
        file=sys.stderr,
    )
    raise SystemExit(1)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SCAMS_HTML_DIR = BASE_DIR / "scams"
SAFETY_DIR = BASE_DIR / "app" / "data" / "safety"
OUTPUT_DIR = BASE_DIR / "app" / "data" / "scams"

LAST_UPDATED = "2026-03-30T00:00:00Z"

SCAM_CITY_MAP = {
    "amsterdam": ("NL", "Netherlands"),
    "athens": ("GR", "Greece"),
    "bangkok": ("TH", "Thailand"),
    "barcelona": ("ES", "Spain"),
    "berlin": ("DE", "Germany"),
    "bruges": ("BE", "Belgium"),
    "budapest": ("HU", "Hungary"),
    "buenos-aires": ("AR", "Argentina"),
    "cairo": ("EG", "Egypt"),
    "cancun": ("MX", "Mexico"),
    "copenhagen": ("DK", "Denmark"),
    "dubai": ("AE", "UAE"),
    "dublin": ("IE", "Ireland"),
    "dubrovnik": ("HR", "Croatia"),
    "edinburgh": ("GB", "United Kingdom"),
    "florence": ("IT", "Italy"),
    "hanoi": ("VN", "Vietnam"),
    "havana": ("CU", "Cuba"),
    "ho-chi-minh-city": ("VN", "Vietnam"),
    "hong-kong": ("HK", "Hong Kong"),
    "istanbul": ("TR", "Turkey"),
    "jerusalem": ("IL", "Israel"),
    "krakow": ("PL", "Poland"),
    "kuala-lumpur": ("MY", "Malaysia"),
    "lima": ("PE", "Peru"),
    "lisbon": ("PT", "Portugal"),
    "london": ("GB", "United Kingdom"),
    "madrid": ("ES", "Spain"),
    "manila": ("PH", "Philippines"),
    "marrakech": ("MA", "Morocco"),
    "medellin": ("CO", "Colombia"),
    "mexico-city": ("MX", "Mexico"),
    "new-york-city": ("US", "United States"),
    "nice": ("FR", "France"),
    "osaka": ("JP", "Japan"),
    "paris": ("FR", "France"),
    "petra": ("JO", "Jordan"),
    "phnom-penh": ("KH", "Cambodia"),
    "phuket": ("TH", "Thailand"),
    "prague": ("CZ", "Czech Republic"),
    "reykjavik": ("IS", "Iceland"),
    "rio-de-janeiro": ("BR", "Brazil"),
    "rome": ("IT", "Italy"),
    "san-juan": ("PR", "Puerto Rico"),
    "santorini": ("GR", "Greece"),
    "seoul": ("KR", "South Korea"),
    "siem-reap": ("KH", "Cambodia"),
    "singapore": ("SG", "Singapore"),
    "split": ("HR", "Croatia"),
    "tokyo": ("JP", "Japan"),
    "vancouver": ("CA", "Canada"),
    "vienna": ("AT", "Austria"),
}


def slugify_scam(name):
    name = name.lower()
    name = re.sub(r"[^a-z0-9\s-]", "", name)
    name = re.sub(r"\s+", "-", name)
    return re.sub(r"-+", "-", name).strip("-")[:50]


def infer_category(name, description):
    text = (name + " " + description).lower()
    if any(w in text for w in ["bar ", "drink", "nightlife", "club", "bottle", "hostess", "tout"]):
        return "nightlife"
    if any(w in text for w in ["taxi", "cab", "driver", "tuk-tuk", "tuk tuk", "transport", "rickshaw"]):
        return "transport"
    if any(w in text for w in ["pickpocket", "theft", "stolen", "steal", "pocket"]):
        return "pickpocket"
    if any(w in text for w in ["overcharge", "overpriced", "bill", "menu price", "price"]):
        return "overcharging"
    if any(w in text for w in ["fake", "counterfeit", "knock", "replica", "forged"]):
        return "counterfeit"
    if any(w in text for w in ["distraction", "friendship", "tea house", "art student", "friend"]):
        return "distraction"
    if any(w in text for w in ["tour", "guide", "excursion", "ticket"]):
        return "tourist-trap"
    if any(w in text for w in ["atm", "card", "money change", "currency", "exchange"]):
        return "money"
    return "tourist-trap"


def infer_severity_from_text(text):
    text = text.lower()
    if any(w in text for w in ["violent", "assault", "robbery", "weapon", "thousands", "¥100,000", "$1,000"]):
        return "high"
    if any(w in text for w in ["hundreds", "serious", "dangerous", "arrest"]):
        return "high"
    return "moderate"


def extract_tags(name, description, location):
    text = (name + " " + description + " " + (location or "")).lower()
    tags = []
    if any(w in text for w in ["bar", "nightlife", "club", "drink", "alcohol"]):
        tags.append("nightlife")
    if any(w in text for w in ["taxi", "transport", "cab"]):
        tags.append("transport")
    if any(w in text for w in ["money", "atm", "cash", "currency"]):
        tags.append("money")
    if any(w in text for w in ["tourist", "sightseeing", "temple", "museum"]):
        tags.append("sightseeing")
    if any(w in text for w in ["restaurant", "food", "eat", "dining"]):
        tags.append("food")
    if any(w in text for w in ["market", "shop", "souvenir", "vendor"]):
        tags.append("shopping")
    if any(w in text for w in ["pickpocket", "theft", "steal"]):
        tags.append("theft")
    return tags if tags else ["general"]


def parse_scams_from_html(html_path, slug):
    """Parse scam cards from HTML page. Returns (city_name, scam_count_from_title, scams_list)."""
    scams = []
    city_name = None
    title_count = None

    try:
        html = html_path.read_text(encoding="utf-8")
        soup = BeautifulSoup(html, "html.parser")

        # Extract city name and count from title
        title_el = soup.find("title")
        if title_el and title_el.string:
            title_str = title_el.string
            m = re.search(r"(\d+)\s+Tourist Scams in ([^(|]+)", title_str)
            if m:
                title_count = int(m.group(1))
                city_name = m.group(2).strip()

        cards = soup.find_all("div", class_="scam-card")
        for card in cards:
            # Name
            title_div = card.find(class_="scam-title")
            name = title_div.get_text(strip=True) if title_div else ""
            if not name:
                continue
            # Strip leading number (e.g., "1. The Foo")
            name = re.sub(r"^\d+[\.\)]\s*", "", name)

            # Severity from badge class
            badge = card.find(class_="danger-badge")
            severity = "moderate"
            if badge:
                classes = badge.get("class", [])
                if "danger-high" in classes:
                    severity = "high"
                elif "danger-low" in classes:
                    severity = "low"
                else:
                    severity = "moderate"

            # Location
            loc_el = card.find(class_="scam-location")
            location = None
            if loc_el:
                location = loc_el.get_text(strip=True)
                location = re.sub(r"^📍\s*", "", location).strip()
                if not location:
                    location = None

            # Description (story paragraph)
            story_el = card.find(class_="scam-story")
            description = story_el.get_text(strip=True) if story_el else ""

            # Avoidance tips
            avoid_block = card.find("div", class_="avoid")
            avoidance = ""
            if avoid_block:
                items = [li.get_text(strip=True) for li in avoid_block.find_all("li") if li.get_text(strip=True)]
                avoidance = " ".join(items)

            if not description and not avoidance:
                continue

            scam_slug = slugify_scam(name)
            category = infer_category(name, description)
            tags = extract_tags(name, description, location)

            scams.append({
                "id": f"scam:{slug}:{scam_slug}",
                "name": name,
                "category": category,
                "severity": severity,
                "frequency": "common",
                "description": description,
                "avoidance": avoidance,
                "location": location,
                "tags": tags,
                "sources": [f"tabiji:scams/{slug}"],
            })

    except Exception as e:
        print(f"  ⚠️  Error parsing {html_path}: {e}")

    return city_name, title_count, scams


def scams_from_safety_profile(iso2, city_name, slug):
    """Fall back: get scams from safety profile for a given city."""
    profile_path = SAFETY_DIR / f"{iso2.lower()}.json"
    if not profile_path.exists():
        return []

    try:
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
    except Exception:
        return []

    raw_scams = profile.get("scams", [])
    if not raw_scams:
        return []

    # Filter by city name if possible
    city_lower = city_name.lower()
    city_scams = [s for s in raw_scams if s.get("city", "").lower() == city_lower]
    if not city_scams:
        city_scams = raw_scams  # use all if city filter yields nothing

    result = []
    for s in city_scams:
        name = s.get("name", "")
        if not name:
            continue
        description = s.get("description", "")
        avoidance = s.get("avoidance", "")
        scam_slug = slugify_scam(name)
        category = infer_category(name, description)
        tags = extract_tags(name, description, city_name)
        result.append({
            "id": f"scam:{slug}:{scam_slug}",
            "name": name,
            "category": category,
            "severity": infer_severity_from_text(description),
            "frequency": "common",
            "description": description,
            "avoidance": avoidance,
            "location": s.get("city"),
            "tags": tags,
            "sources": [f"tabiji:scams/{slug}"],
        })
    return result


def slug_to_display_name(slug):
    return " ".join(p.capitalize() for p in slug.split("-"))


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    processed = 0
    errors = 0

    for slug, (iso2, country) in sorted(SCAM_CITY_MAP.items()):
        html_path = SCAMS_HTML_DIR / slug / "index.html"
        if not html_path.exists():
            print(f"  ⚠️  No HTML at scams/{slug}/index.html — skipping")
            errors += 1
            continue

        # Parse HTML (primary source)
        city_name, title_count, scams = parse_scams_from_html(html_path, slug)

        # Fall back to safety profile if HTML gave nothing
        if not scams:
            display_city = city_name or slug_to_display_name(slug)
            scams = scams_from_safety_profile(iso2, display_city, slug)

        # Use title-extracted city name, or derive from slug
        if not city_name:
            city_name = slug_to_display_name(slug)

        scam_count = title_count if title_count is not None else len(scams)
        iso2_lower = iso2.lower()

        record = {
            "id": f"scam:{slug}",
            "slug": slug,
            "city": city_name,
            "country": country,
            "countryCode": iso2,
            "lastUpdated": LAST_UPDATED,
            "scamCount": scam_count,
            "scams": scams,
            "sourceUrl": f"https://tabiji.ai/scams/{slug}/",
            "relatedAlerts": f"/api/v1/alerts/{iso2_lower}.json",
            "relatedSafety": f"/api/v1/safety/{iso2_lower}.json",
        }

        out = OUTPUT_DIR / f"{slug}.json"
        out.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
        processed += 1
        print(f"  ✅ {slug}: {city_name} ({len(scams)} scams extracted, {scam_count} documented)")

    print(f"\n✅ Done: {processed} cities processed, {errors} skipped")


if __name__ == "__main__":
    main()
