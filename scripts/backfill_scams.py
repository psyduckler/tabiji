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

# Subdirs of /scams/ that are NOT individual city scam pages and must be skipped
# when looking for HTML→JSON backfill candidates. country/ holds country hubs,
# research/ holds raw Reddit JSON, everywhere/ is the master non-tourist scam
# index, atlas/ uses a different schema (per scripts/_scam_sweep_common.py).
_NON_CITY_SCAM_DIRS = {"country", "research", "everywhere", "atlas"}


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


def _city_html_slugs() -> set[str]:
    """Slugs in /scams/ that look like city pages (have index.html, not a hub dir)."""
    if not SCAMS_HTML_DIR.is_dir():
        return set()
    out: set[str] = set()
    for p in SCAMS_HTML_DIR.iterdir():
        if not p.is_dir():
            continue
        if p.name in _NON_CITY_SCAM_DIRS:
            continue
        if (p / "index.html").exists():
            out.add(p.name)
    return out


def main() -> int:
    catalog = json.load(open(SCAMS_CATALOG))
    listed = {x["slug"] for x in catalog["items"]}
    on_disk = {f.stem for f in SCAMS_API_DIR.glob("*.json")}
    html_slugs = _city_html_slugs()

    # Three classes of drift to repair:
    #   A) catalog lists slug, JSON file missing  → parse HTML, write JSON
    #   B) HTML page exists but no JSON file       → parse HTML, write JSON (covers C4)
    #   C) JSON file exists but catalog lacks slug → reindex catalog from on-disk
    missing_json_for_listed = sorted(listed - on_disk)
    missing_json_for_html = sorted((html_slugs - on_disk) - set(missing_json_for_listed))
    extras = sorted(on_disk - listed)

    print(f"Catalog listed:        {len(listed)}")
    print(f"On-disk JSON:          {len(on_disk)}")
    print(f"City HTML pages:       {len(html_slugs)}")
    print(f"  A) listed-no-JSON   (backfill HTML→JSON): {len(missing_json_for_listed)}")
    print(f"  B) HTML-no-JSON     (backfill HTML→JSON): {len(missing_json_for_html)}")
    print(f"  C) JSON-not-listed  (reindex catalog):    {len(extras)}")

    written = 0
    skipped_no_html: list[str] = []
    skipped_parse_failed: list[str] = []

    for slug in [*missing_json_for_listed, *missing_json_for_html]:
        html = SCAMS_HTML_DIR / slug / "index.html"
        if not html.exists():
            skipped_no_html.append(slug)
            continue
        try:
            payload = parse_html_page(slug, html)
        except Exception as exc:  # noqa: BLE001 — we want to keep going on a single broken page
            skipped_parse_failed.append(f"{slug} ({exc})")
            continue
        if payload["scamCount"] == 0:
            # A city page that parses to zero scam-cards is almost always a hub or
            # template stub — emitting an empty {scams: []} JSON would publish a
            # misleading "we have no scams here" record. Skip and surface.
            skipped_parse_failed.append(f"{slug} (zero scam-cards parsed)")
            continue
        out = SCAMS_API_DIR / f"{slug}.json"
        out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
        written += 1
        print(f"  WROTE  api/v1/scams/{slug}.json  ({payload['scamCount']} scams)")

    if skipped_no_html:
        print(f"\n⚠️  Skipped {len(skipped_no_html)} catalog slugs with no HTML page:")
        for s in skipped_no_html:
            print(f"     - {s}")

    if skipped_parse_failed:
        print(f"\n⚠️  Skipped {len(skipped_parse_failed)} HTML pages that did not yield a city scam record:")
        for s in skipped_parse_failed:
            print(f"     - {s}")

    new_catalog = reindex_catalog()
    SCAMS_CATALOG.write_text(json.dumps(new_catalog, indent=2, ensure_ascii=False) + "\n")
    print(f"\nRewrote {SCAMS_CATALOG.relative_to(REPO)}: {new_catalog['count']} entries")
    print(f"Backfilled JSONs: {written}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
