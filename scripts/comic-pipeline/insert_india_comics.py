#!/usr/bin/env python3
"""Insert <img class="scam-comic"> tags into all 60 India scam-cards.

Run after regen_india_2026_04_28.py finishes (60/60 ok at R2 paths
scams/<city>/scam-<n>.jpg). Inserts the img tag between each scam-card's
scam-location div and scam-tldr paragraph, matching the NYC reference pattern.

Idempotent: if a scam-comic img already exists in the card, skip.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO = Path(subprocess.run(
    ["git", "rev-parse", "--show-toplevel"],
    capture_output=True, text=True, check=True,
).stdout.strip())

CITIES = [
    "agra", "bangalore", "chennai", "delhi", "goa", "hyderabad",
    "jaipur", "kolkata", "mumbai", "rishikesh", "udaipur", "varanasi",
]

# Match each scam-card block from id="scam-N" up to the next .scam-card or section.
SCAM_CARD_RE = re.compile(
    r'(<div class="scam-card"[^>]*id="(scam-\d+)"[^>]*>)(.*?)(?=<div class="scam-card"|<section|<!-- (?:Scam|What|FAQ))',
    re.DOTALL,
)
TITLE_RE = re.compile(r'<div class="scam-title">([^<]+)</div>')
LOCATION_RE = re.compile(r'(<div class="scam-location">[^<]*</div>)')
TLDR_RE = re.compile(r'<p class="scam-tldr">')
EXISTING_COMIC_RE = re.compile(r'class="scam-comic"')


def img_tag(city: str, n: int, title: str) -> str:
    safe_title = title.replace('"', "&quot;")
    return (
        f'<img alt="{safe_title} — comic illustration" '
        f'class="scam-comic" loading="lazy" '
        f'src="https://img.tabiji.ai/scams/{city}/scam-{n}.jpg" '
        f'style="width:100%;height:auto;border-radius:12px;margin:1rem 0 1.25rem;display:block;" '
        f'width="1200" height="1200" decoding="async"/>'
    )


def insert_for_city(city: str) -> tuple[int, int]:
    """Return (inserted, skipped)."""
    path = REPO / "scams" / city / "index.html"
    html = path.read_text()

    inserted = skipped = 0

    def replace_card(m: re.Match) -> str:
        nonlocal inserted, skipped
        opening = m.group(1)
        scam_id = m.group(2)
        body = m.group(3)
        n = int(scam_id.split("-")[1])

        if EXISTING_COMIC_RE.search(body):
            skipped += 1
            return m.group(0)

        title_m = TITLE_RE.search(body)
        if not title_m:
            return m.group(0)
        title = title_m.group(1).strip()

        loc_m = LOCATION_RE.search(body)
        tldr_m = TLDR_RE.search(body)
        tag = img_tag(city, n, title)

        if loc_m:
            insert_at = loc_m.end()
            new_body = body[:insert_at] + "\n" + tag + body[insert_at:]
        elif tldr_m:
            insert_at = tldr_m.start()
            new_body = body[:insert_at] + tag + "\n" + body[insert_at:]
        else:
            return m.group(0)

        inserted += 1
        return opening + new_body

    new_html = SCAM_CARD_RE.sub(replace_card, html)
    if new_html != html:
        path.write_text(new_html)

    return inserted, skipped


def main() -> int:
    total_inserted = total_skipped = 0
    for city in CITIES:
        inserted, skipped = insert_for_city(city)
        print(f"  {city}: inserted={inserted} skipped(already had)={skipped}")
        total_inserted += inserted
        total_skipped += skipped
    print(f"\nTOTAL inserted={total_inserted} skipped={total_skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
