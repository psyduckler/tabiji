#!/usr/bin/env python3
"""Insert <img class="scam-comic"> tags into every /scams/everywhere/ scam-card.

Reads results.json from generate_everywhere_comics.py and edits each
target page's scam-card by inserting the <img> directly below the
matching <div class="scam-location">. Idempotent: existing scam-comic
imgs in a card are replaced rather than duplicated.

Pattern (memory: scam_comic_placement.md):
  <div class="scam-location">…</div>
  <img class="scam-comic" src="…" alt="… — comic illustration" …>
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RESULTS_PATH = Path("/tmp/everywhere-comics-2026-04-30/results.json")


def img_tag(url: str, alt: str) -> str:
    return (
        f'<img class="scam-comic" src="{url}?v=1" '
        f'alt="{alt} — comic illustration" loading="lazy" '
        f'style="width:100%;height:auto;border-radius:12px;'
        f'margin:1rem 0 1.25rem;display:block;" '
        f'width="1024" height="1024" decoding="async">'
    )


def insert_or_replace_in_card(html: str, card_id: str, alt: str, url: str) -> tuple[str, str]:
    """Insert/replace the scam-comic <img> in the card whose div has id=card_id.

    Returns (new_html, status) where status is INSERTED, REPLACED, or NOT_FOUND.
    """
    # Find the card block
    card_open = re.search(rf'<div class="scam-card"[^>]*id="{re.escape(card_id)}"[^>]*>',
                          html)
    if not card_open:
        return html, "NOT_FOUND_CARD"
    card_start = card_open.end()
    # Find the scam-location closing within this card
    loc_close = re.search(r'</div>\s*\n', html[card_start:])
    # ... but we want the close tag of the scam-location specifically.
    # Find the FIRST scam-location div inside the card.
    loc_match = re.search(r'<div class="scam-location">', html[card_start:])
    if not loc_match:
        return html, "NOT_FOUND_LOCATION"
    loc_div_start = card_start + loc_match.start()
    # Find the matching </div> for that scam-location
    # scam-location is single-line so </div> is the next </div>
    after_loc = card_start + loc_match.end()
    next_close = html.find("</div>", after_loc)
    if next_close == -1:
        return html, "NOT_FOUND_LOCATION_CLOSE"
    insert_point = next_close + len("</div>")
    # Look at next non-whitespace content; if it's an existing scam-comic img,
    # replace it. Otherwise insert a new one.
    after = html[insert_point:]
    existing_img = re.match(r'\s*<img class="scam-comic"[^>]*>', after)
    new_img = img_tag(url, alt)
    if existing_img:
        replaced = html[:insert_point] + "\n        " + new_img + after[existing_img.end():]
        return replaced, "REPLACED"
    inserted = html[:insert_point] + "\n        " + new_img + after
    return inserted, "INSERTED"


def get_alt_from_card(html: str, card_id: str) -> str:
    """Extract the scam-title text from the card with id=card_id."""
    m = re.search(
        rf'<div class="scam-card"[^>]*id="{re.escape(card_id)}"[^>]*>'
        r'.*?<div class="scam-title">([^<]+)</div>',
        html, flags=re.DOTALL)
    if not m:
        return f"scam variant {card_id}"
    title = m.group(1).strip()
    # HTML-decode quotes/escape anything weird
    title = title.replace("&quot;", '"').replace("&amp;", "&")
    # Strip from alt attribute — replace " with '
    return title.replace('"', "'")


def main():
    if not RESULTS_PATH.exists():
        print(f"ERROR: {RESULTS_PATH} not found — run generator first", file=sys.stderr)
        sys.exit(1)
    results = json.loads(RESULTS_PATH.read_text())

    # Group by page
    by_page: dict[str, list[dict]] = {}
    for r in results:
        if r["status"] != "OK":
            continue
        by_page.setdefault(r["page"], []).append(r)

    total_inserted = 0
    total_replaced = 0
    total_missing = 0

    for page_slug, entries in sorted(by_page.items()):
        page_path = REPO / "scams" / "everywhere" / page_slug / "index.html"
        if not page_path.exists():
            print(f"WARN: {page_path} not found", flush=True)
            continue
        html = page_path.read_text()
        for entry in entries:
            card_id = entry["card"]
            url = entry["url"]
            alt = get_alt_from_card(html, card_id)
            html, status = insert_or_replace_in_card(html, card_id, alt, url)
            if status == "INSERTED":
                total_inserted += 1
            elif status == "REPLACED":
                total_replaced += 1
            else:
                total_missing += 1
                print(f"  WARN {page_slug}/{card_id}: {status}", flush=True)
        page_path.write_text(html)
        print(f"  {page_slug}: {len(entries)} variants processed", flush=True)

    print(f"\n=== INSERTION SUMMARY ===")
    print(f"  inserted: {total_inserted}")
    print(f"  replaced: {total_replaced}")
    print(f"  missing:  {total_missing}")


if __name__ == "__main__":
    main()
