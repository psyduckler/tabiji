#!/usr/bin/env python3
"""One-off india-wide api/v1 reconciler — bootstraps missing files,
prunes stale entries from existing files, syncs all 12 to current HTML.

Used after the 2026-04-28 12-city rewrite where sync_api_from_html.py
couldn't handle (a) the 7 cities that lacked json files and (b) the
title renames in the 5 existing files.

Preserves curated category/tags/sources from any existing entry that
still matches by (new) name; otherwise applies sensible defaults.
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup

REPO = Path(subprocess.run(
    ["git", "rev-parse", "--show-toplevel"],
    capture_output=True, text=True, check=True,
).stdout.strip())

CITIES = [
    "agra", "bangalore", "chennai", "delhi", "goa", "hyderabad",
    "jaipur", "kolkata", "mumbai", "rishikesh", "udaipur", "varanasi",
]

DANGER_TO_SEVERITY = {"high": "high", "medium": "moderate", "low": "low"}


def _slugify(name: str) -> str:
    """Convert scam name to id-friendly slug."""
    s = name.lower()
    s = re.sub(r"['‘’]", "", s)  # drop apostrophes
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def _extract_scam(card) -> dict | None:
    title_el = card.select_one(".scam-title")
    if not title_el:
        return None
    name = title_el.get_text(strip=True)

    tldr_el = card.select_one(".scam-tldr")
    body_paras = card.select(".scam-story-body")
    location_el = card.select_one(".scam-location")
    avoid_block = card.select_one(".detail-block.avoid")

    severity = None
    badge = card.select_one(".danger-badge")
    if badge:
        for cls in badge.get("class", []) or []:
            if cls.startswith("danger-"):
                severity = DANGER_TO_SEVERITY.get(cls[len("danger-"):])
                break

    location = ""
    if location_el:
        location = location_el.get_text(" ", strip=True).lstrip("📍").strip()

    avoidance = ""
    if avoid_block:
        items = [li.get_text(" ", strip=True) for li in avoid_block.select("li")]
        avoidance = " ".join(items)

    return {
        "name": name,
        "tldr": tldr_el.get_text(" ", strip=True) if tldr_el else "",
        "description": "\n\n".join(p.get_text(" ", strip=True) for p in body_paras),
        "avoidance": avoidance,
        "location": location,
        "severity": severity or "moderate",
    }


def reconcile(slug: str, city_name: str) -> dict:
    html_path = REPO / "scams" / slug / "index.html"
    api_path = REPO / "api" / "v1" / "scams" / f"{slug}.json"
    soup = BeautifulSoup(html_path.read_text(), "html.parser")

    html_scams = []
    for card in soup.select(".scam-card"):
        s = _extract_scam(card)
        if s:
            html_scams.append(s)

    existing_by_name: dict[str, dict] = {}
    base_data = None
    if api_path.exists():
        base_data = json.loads(api_path.read_text())
        for s in base_data.get("scams", []):
            existing_by_name[s["name"]] = s

    out_scams = []
    new_count = updated_count = pruned = 0
    for hs in html_scams:
        existing = existing_by_name.pop(hs["name"], None)
        if existing:
            entry = dict(existing)
            entry["name"] = hs["name"]
            entry["tldr"] = hs["tldr"]
            entry["description"] = hs["description"]
            entry["avoidance"] = hs["avoidance"]
            entry["location"] = hs["location"]
            entry["severity"] = hs["severity"]
            updated_count += 1
        else:
            entry = {
                "id": f"scam:{slug}:{_slugify(hs['name'])}",
                "name": hs["name"],
                "category": "tourist-trap",
                "severity": hs["severity"],
                "frequency": "common",
                "tldr": hs["tldr"],
                "description": hs["description"],
                "avoidance": hs["avoidance"],
                "location": hs["location"],
                "tags": [slug, "india"],
                "sources": [f"tabiji:scams/{slug}"],
            }
            new_count += 1
        out_scams.append(entry)

    pruned = len(existing_by_name)

    if base_data:
        base_data["scams"] = out_scams
        base_data["scamCount"] = len(out_scams)
        base_data["lastUpdated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        base_data = {
            "id": f"scam:{slug}",
            "slug": slug,
            "city": city_name,
            "country": "India",
            "countryCode": "IN",
            "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "scamCount": len(out_scams),
            "scams": out_scams,
            "sourceUrl": f"https://tabiji.ai/scams/{slug}/",
            "relatedAlerts": "/api/v1/alerts/in.json",
        }

    api_path.parent.mkdir(parents=True, exist_ok=True)
    api_path.write_text(json.dumps(base_data, indent=2, ensure_ascii=False) + "\n")

    return {
        "slug": slug, "html_count": len(html_scams),
        "new": new_count, "updated": updated_count, "pruned": pruned,
        "bootstrapped": existing == None and new_count == len(html_scams),
    }


CITY_NAMES = {
    "agra": "Agra", "bangalore": "Bangalore", "chennai": "Chennai",
    "delhi": "Delhi", "goa": "Goa", "hyderabad": "Hyderabad",
    "jaipur": "Jaipur", "kolkata": "Kolkata", "mumbai": "Mumbai",
    "rishikesh": "Rishikesh", "udaipur": "Udaipur", "varanasi": "Varanasi",
}


def main() -> int:
    for slug in CITIES:
        r = reconcile(slug, CITY_NAMES[slug])
        print(f"  {r['slug']}: html={r['html_count']} new={r['new']} updated={r['updated']} pruned={r['pruned']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
