#!/usr/bin/env python3
"""
One-shot script: refresh api/v1/scams/<city>.json for the 10 Morocco cities
from the live site (https://tabiji.ai/scams/<city>/) as source of truth.

For each city:
- Scrape v2 HTML structure (scam-card divs)
- Combine tldr + story-body paragraphs into legacy `description`
- Combine howToAvoid bullets into legacy `avoidance`
- Carry over category/frequency/id/sources/tags from existing JSON if present
- Synthesize category/frequency for cities without an existing JSON

Run from repo root:
  python3 scripts/refresh-morocco-scams.py
"""
import json
import re
import sys
import time
import urllib.request
from html import unescape
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup

REPO = Path(__file__).resolve().parent.parent
SCAMS_DIR = REPO / "api" / "v1" / "scams"

CITIES = [
    ("agadir",      "Agadir"),
    ("casablanca",  "Casablanca"),
    ("chefchaouen", "Chefchaouen"),
    ("essaouira",   "Essaouira"),
    ("fez",         "Fez"),
    ("marrakech",   "Marrakech"),
    ("merzouga",    "Merzouga"),
    ("ouarzazate",  "Ouarzazate"),
    ("rabat",       "Rabat"),
    ("tangier",     "Tangier"),
]

# Defaults for synthesized JSON entries when no existing legacy data is present.
# Pick category/frequency from live-site visible signals where possible;
# otherwise use sensible defaults that build.py will render correctly.
DEFAULT_CATEGORY = "tourist-trap"
DEFAULT_FREQUENCY = "common"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (book-generator)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s


def severity_from_badge(badge_classes) -> str:
    """Map danger-{high|medium|low} → severity string used in legacy JSON."""
    for c in badge_classes:
        if c in ("danger-high", "danger-medium", "danger-low"):
            return c.replace("danger-", "")
    return "medium"


def parse_scam_card(card) -> dict:
    title_el = card.select_one(".scam-title")
    title = title_el.get_text(strip=True) if title_el else ""

    badge = card.select_one(".danger-badge")
    severity = severity_from_badge(badge.get("class", [])) if badge else "medium"

    loc_el = card.select_one(".scam-location")
    location = ""
    if loc_el:
        location = loc_el.get_text(strip=True)
        # strip leading 📍 + whitespace
        location = re.sub(r"^[\U0001F4CD  \s]+", "", location)

    tldr_el = card.select_one("p.scam-tldr")
    tldr = tldr_el.get_text(" ", strip=True) if tldr_el else ""

    story_paragraphs = [p.get_text(" ", strip=True) for p in card.select("p.scam-story-body")]

    # description = tldr + story body, joined as one block (legacy schema)
    desc_parts = []
    if tldr:
        desc_parts.append(tldr)
    desc_parts.extend(story_paragraphs)
    description = "\n\n".join(p for p in desc_parts if p)

    # how to avoid
    avoid_block = card.select_one(".detail-block.avoid")
    avoidance_lines = []
    if avoid_block:
        for li in avoid_block.select("li"):
            avoidance_lines.append(li.get_text(" ", strip=True))
    # legacy avoidance is one string; rejoin with double-spaced sentence boundaries
    avoidance = " ".join(avoidance_lines)

    # red flags (kept on the v2 side; build.py ignores but we'll preserve)
    rf_block = card.select_one(".detail-block.red-flags")
    red_flags = [li.get_text(" ", strip=True) for li in rf_block.select("li")] if rf_block else []

    # how-to-avoid bullets preserved as v2 list too
    how_to_avoid = list(avoidance_lines)

    return {
        "title": title,
        "severity": severity,
        "location": location,
        "tldr": tldr,
        "description": description,
        "avoidance": avoidance,
        "redFlags": red_flags,
        "howToAvoid": how_to_avoid,
    }


def load_existing(slug: str) -> Optional[dict]:
    p = SCAMS_DIR / f"{slug}.json"
    if not p.exists():
        return None
    return json.loads(p.read_text())


def existing_scam_meta(existing: Optional[dict], scam_title: str) -> dict:
    """Lookup category/frequency/sources/tags/id from a previous scam entry by name match."""
    if not existing:
        return {}
    for s in existing.get("scams", []):
        if (s.get("name") or "").strip().lower() == scam_title.strip().lower():
            return {
                "id": s.get("id"),
                "category": s.get("category"),
                "frequency": s.get("frequency"),
                "tags": s.get("tags") or [],
                "sources": s.get("sources") or [f"tabiji:scams/{existing.get('slug')}"]
            }
    return {}


def build_city_json(slug: str, display: str) -> dict:
    url = f"https://tabiji.ai/scams/{slug}/"
    html = fetch(url)
    soup = BeautifulSoup(html, "lxml")
    cards = soup.select("div.scam-card")
    if not cards:
        raise RuntimeError(f"no scam-card divs found on {url}")

    existing = load_existing(slug)
    scams_out = []

    for idx, card in enumerate(cards, start=1):
        parsed = parse_scam_card(card)
        title = parsed["title"]
        if not title:
            print(f"  WARN: scam #{idx} has no title", file=sys.stderr)

        meta = existing_scam_meta(existing, title)
        scam_id = meta.get("id") or f"scam:{slug}:{slugify(title)}"
        category = meta.get("category") or DEFAULT_CATEGORY
        frequency = meta.get("frequency") or DEFAULT_FREQUENCY
        tags = meta.get("tags") or [slug, "morocco"]
        sources = meta.get("sources") or [f"tabiji:scams/{slug}"]

        scams_out.append({
            "id": scam_id,
            "name": title,
            "category": category,
            "severity": parsed["severity"],
            "frequency": frequency,
            "tldr": parsed["tldr"],
            "description": parsed["description"],
            "avoidance": parsed["avoidance"],
            "location": parsed["location"],
            "redFlags": parsed["redFlags"],
            "howToAvoid": parsed["howToAvoid"],
            "tags": tags,
            "sources": sources,
        })

    # preserve existing top-level metadata where reasonable
    base = existing or {}
    out = {
        "id": base.get("id") or f"scam:{slug}",
        "slug": slug,
        "city": display,
        "country": "Morocco",
        "countryCode": "MA",
        "lastUpdated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "scamCount": len(scams_out),
        "scams": scams_out,
    }
    return out


def main():
    SCAMS_DIR.mkdir(parents=True, exist_ok=True)
    summary = []
    for slug, display in CITIES:
        print(f"→ {slug}")
        data = build_city_json(slug, display)
        path = SCAMS_DIR / f"{slug}.json"
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        summary.append((slug, len(data["scams"])))
        print(f"  wrote {path.relative_to(REPO)} ({len(data['scams'])} scams)")
    total = sum(n for _, n in summary)
    print()
    print("=== summary ===")
    for s, n in summary:
        print(f"  {s:15s} {n:3d}")
    print(f"  TOTAL: {len(summary)} cities, {total} scams")


if __name__ == "__main__":
    main()
