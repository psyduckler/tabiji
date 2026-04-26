#!/usr/bin/env python3
"""Backfill api/v1/scams/<slug>.json from rendered scams/<slug>/index.html.

Run once to reconcile api/v1/scams.json catalog with on-disk JSON files:
  - For every catalog slug missing a JSON file, parse the HTML page and emit JSON
  - For every JSON file missing from the catalog, add a {slug, url} entry
  - Rewrite api/v1/scams.json with the unioned, sorted catalog

Idempotent: re-running on a clean tree is a no-op.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup

REPO = Path(__file__).resolve().parent.parent
SCAMS_HTML_DIR = REPO / "scams"
SCAMS_API_DIR = REPO / "api" / "v1" / "scams"
SCAMS_CATALOG = REPO / "api" / "v1" / "scams.json"
COUNTRIES_API_DIR = REPO / "api" / "v1" / "countries"
SITE_URL = "https://tabiji.ai"


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


_country_name_cache: dict[str, str] = {}


def country_name(iso2: str) -> str:
    if not iso2:
        return ""
    iso2 = iso2.lower()
    if iso2 in _country_name_cache:
        return _country_name_cache[iso2]
    path = COUNTRIES_API_DIR / f"{iso2}.json"
    name = ""
    if path.exists():
        try:
            name = json.load(open(path)).get("name", "")
        except Exception:
            pass
    _country_name_cache[iso2] = name
    return name


def parse_html_page(slug: str, html_path: Path) -> dict:
    soup = BeautifulSoup(html_path.read_text(), "html.parser")

    city = ""
    iso2 = ""
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            graph = json.loads(s.string or "{}").get("@graph", [])
        except Exception:
            continue
        for node in graph:
            if node.get("@type") == "Place":
                city = node.get("name") or city
                iso2 = (node.get("address", {}) or {}).get("addressCountry", "") or iso2
        if city and iso2:
            break

    if not city:
        h1 = soup.find("h1")
        if h1:
            text = h1.get_text(strip=True)
            m = re.search(r"in\s+(.+?)$", text)
            if m:
                city = m.group(1).strip()
    if not city:
        city = slug.replace("-", " ").title()

    iso2 = (iso2 or "").lower()
    country = country_name(iso2)
    iso2_upper = iso2.upper()

    scams_out = []
    for card in soup.find_all(class_="scam-card"):
        title_el = card.find(class_="scam-title")
        name = title_el.get_text(" ", strip=True) if title_el else ""
        if not name:
            continue

        badge = card.find(class_="danger-badge")
        severity = "medium"
        if badge:
            for cls in badge.get("class", []):
                if cls.startswith("danger-") and cls != "danger-badge":
                    severity = cls.replace("danger-", "")
                    break

        location_el = card.find(class_="scam-location")
        location = ""
        if location_el:
            location = location_el.get_text(" ", strip=True)
            location = re.sub(r"^[^\w]+", "", location).strip()

        story_el = card.find(class_="scam-story-body")
        description = story_el.get_text(" ", strip=True) if story_el else ""

        avoidance = ""
        details = card.find(class_="scam-details")
        if details:
            for block in details.find_all(class_="detail-block"):
                heading = block.find(["strong", "b", "h3", "h4"])
                heading_text = (heading.get_text(" ", strip=True) if heading else "").lower()
                if "avoid" in heading_text:
                    if heading:
                        heading.extract()
                    avoidance = block.get_text(" ", strip=True)
                    break

        tldr = ""
        if description:
            sentence = re.split(r"(?<=[.!?])\s+", description, maxsplit=1)[0]
            tldr = sentence[:400]

        tags = [t for t in [city.lower(), country.lower()] if t]

        scams_out.append({
            "id": f"scam:{slug}:{slugify(name)}",
            "name": name,
            "category": "tourist-trap",
            "severity": severity,
            "frequency": "common",
            "tldr": tldr,
            "description": description,
            "avoidance": avoidance,
            "location": location,
            "tags": tags,
            "sources": [f"tabiji:scams/{slug}"],
        })

    payload = {
        "id": f"scam:{slug}",
        "slug": slug,
        "city": city,
        "country": country,
        "countryCode": iso2_upper,
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scamCount": len(scams_out),
        "scams": scams_out,
        "sourceUrl": f"{SITE_URL}/scams/{slug}/",
    }
    if iso2:
        payload["relatedAlerts"] = f"/api/v1/alerts/{iso2}.json"
        payload["relatedSafety"] = f"/api/v1/safety/{iso2}.json"
    return payload


def reindex_catalog() -> dict:
    on_disk = sorted(
        f.stem for f in SCAMS_API_DIR.glob("*.json")
    )
    items = [
        {"slug": slug, "url": f"{SITE_URL}/scams/{slug}/"}
        for slug in on_disk
    ]
    return {
        "count": len(items),
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "items": items,
    }


def find_research_city(slug: str) -> dict | None:
    """Search scams/research/*_batch*.json for a city whose slug matches.

    Returns the city dict (with city/country/country_code/scams keys) or None.
    Slug match: slugify(city['city']) == slug.
    """
    research_dir = REPO / "scams" / "research"
    for fpath in sorted(research_dir.glob("*_batch*.json")):
        try:
            data = json.load(open(fpath))
        except (json.JSONDecodeError, OSError):
            continue
        cities = data if isinstance(data, list) else [data]
        for city in cities:
            if not isinstance(city, dict):
                continue
            if slugify(city.get("city", "")) == slug:
                return city
    return None


def build_payload_from_research(slug: str, city_data: dict) -> dict:
    """Build the rich API-JSON payload from a research-JSON city entry.

    Uses the full structured data (category, danger_level, story paragraphs,
    how_to_avoid array, reddit_sources) — much richer than what
    parse_html_page can recover from the rendered HTML.
    """
    city = city_data.get("city", "")
    country = city_data.get("country", "")
    iso2 = (city_data.get("country_code") or "").upper()

    scams_out = []
    for s in city_data.get("scams", []):
        story = s.get("story", "")
        # First sentence of the story is the load-bearing TLDR per the style guide
        tldr_parts = re.split(r"(?<=[.!?])\s+", story.strip(), maxsplit=1)
        tldr = (tldr_parts[0] if tldr_parts else "")[:400]
        avoidance = " ".join(s.get("how_to_avoid", []))
        category = s.get("category", "")

        scams_out.append({
            "id": f"scam:{slug}:{slugify(s.get('scam_name', ''))}",
            "name": s.get("scam_name", ""),
            "category": category,
            "severity": s.get("danger_level", "medium"),
            "frequency": "common",
            "tldr": tldr,
            "description": story,
            "avoidance": avoidance,
            "location": s.get("location", ""),
            "tags": [category] if category else [],
            "sources": list(s.get("reddit_sources", [])),
        })

    payload = {
        "id": f"scam:{slug}",
        "slug": slug,
        "city": city,
        "country": country,
        "countryCode": iso2,
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scamCount": len(scams_out),
        "scams": scams_out,
        "sourceUrl": f"{SITE_URL}/scams/{slug}/",
    }
    if iso2:
        payload["relatedAlerts"] = f"/api/v1/alerts/{iso2.lower()}.json"
        payload["relatedSafety"] = f"/api/v1/safety/{iso2.lower()}.json"
    return payload


def regenerate_one(slug: str) -> int:
    """Force-regenerate api/v1/scams/<slug>.json after a city rebuild.

    Prefers the research JSON (rich category, full story, real reddit_sources).
    Falls back to parsing the rendered HTML if no research entry exists for
    this slug — same low-fidelity output as the original missing-only backfill.

    Returns 0 on success, 1 if neither research nor HTML is available.
    """
    city_data = find_research_city(slug)
    if city_data is not None:
        payload = build_payload_from_research(slug, city_data)
        source = "research JSON"
    else:
        html = SCAMS_HTML_DIR / slug / "index.html"
        if not html.exists():
            print(f"❌ no research entry and no HTML page for {slug}", file=sys.stderr)
            return 1
        payload = parse_html_page(slug, html)
        source = "rendered HTML (fallback — no research entry)"

    out = SCAMS_API_DIR / f"{slug}.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(f"WROTE api/v1/scams/{slug}.json  ({payload['scamCount']} scams, from {source})")
    new_catalog = reindex_catalog()
    SCAMS_CATALOG.write_text(json.dumps(new_catalog, indent=2, ensure_ascii=False) + "\n")
    print(f"REINDEXED {SCAMS_CATALOG.relative_to(REPO)}: {new_catalog['count']} entries")
    return 0


def main() -> int:
    # CLI: `--slug <slug>` regenerates ONE city's JSON unconditionally
    # (use after a rebuild). With no args, runs the original catalog-vs-disk
    # backfill that only writes missing JSONs.
    if len(sys.argv) >= 3 and sys.argv[1] == "--slug":
        return regenerate_one(sys.argv[2])

    catalog = json.load(open(SCAMS_CATALOG))
    listed = {x["slug"] for x in catalog["items"]}
    on_disk = {f.stem for f in SCAMS_API_DIR.glob("*.json")}

    missing = sorted(listed - on_disk)
    extras = sorted(on_disk - listed)

    print(f"Catalog: {len(listed)}  On-disk JSON: {len(on_disk)}")
    print(f"Missing JSON (will backfill from HTML): {len(missing)}")
    print(f"Extras on-disk (will reindex into catalog): {len(extras)}")

    written = 0
    skipped_no_html = []
    for slug in missing:
        html = SCAMS_HTML_DIR / slug / "index.html"
        if not html.exists():
            skipped_no_html.append(slug)
            continue
        payload = parse_html_page(slug, html)
        out = SCAMS_API_DIR / f"{slug}.json"
        out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
        written += 1
        print(f"  WROTE  api/v1/scams/{slug}.json  ({payload['scamCount']} scams)")

    if skipped_no_html:
        print(f"\n⚠️  Skipped {len(skipped_no_html)} catalog slugs with no HTML page:")
        for s in skipped_no_html:
            print(f"     - {s}")

    new_catalog = reindex_catalog()
    SCAMS_CATALOG.write_text(json.dumps(new_catalog, indent=2, ensure_ascii=False) + "\n")
    print(f"\nRewrote {SCAMS_CATALOG.relative_to(REPO)}: {new_catalog['count']} entries")
    print(f"Backfilled JSONs: {written}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
