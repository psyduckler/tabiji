#!/usr/bin/env python3
"""Insert <img class="scam-comic"> tags into Morocco city HTML pages.

Per project memory rule (scam_comic_placement), the comic image goes directly
below the <div class="scam-location"> line in every scam-card. The 9 Morocco
cities rebuilt without comic slots need them inserted; Agadir's 4 already-
broken refs need a cache-bust bump (?v=1 → ?v=2) so browsers re-fetch the
freshly-uploaded JPEGs.

Idempotent — running twice does not duplicate img tags. Skips any scam that
already has an <img class="scam-comic"> in its card.

Usage:
    python3 scripts/comic-pipeline/insert_morocco_comics.py
    python3 scripts/comic-pipeline/insert_morocco_comics.py --dry-run
    python3 scripts/comic-pipeline/insert_morocco_comics.py rabat marrakech
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

# Cities that need <img> tags inserted below each <div class="scam-location">
INSERT_CITIES = [
    "marrakech", "casablanca", "tangier", "rabat", "fez",
    "merzouga", "ouarzazate", "chefchaouen", "essaouira",
]
# Cities where <img> already exists but URLs are 404 — bump cache version
BUMP_CITIES = ["agadir"]

IMG_TEMPLATE = (
    '<img class="scam-comic" src="https://img.tabiji.ai/scams/{city}/scam-{n}.jpg?v=1" '
    'alt="{alt} — comic illustration" loading="lazy" '
    'style="width:100%;height:auto;border-radius:12px;margin:1rem 0 1.25rem;display:block;" '
    'width="1200" height="675" decoding="async">'
)


def _scam_card_pattern() -> re.Pattern:
    """Match each <div class="scam-card" id="scam-N">…</div> block.
    The closing </div> is hard to match unambiguously without a stack, so
    we anchor on the next <div class="scam-card" or end-of-content marker."""
    return re.compile(
        r'(<div class="scam-card"[^>]*id="scam-(\d+)"[^>]*>)(.*?)(?=<div class="scam-card"|<!-- What to do|<!-- @book-cta:start)',
        re.DOTALL,
    )


def _has_comic(card_body: str) -> bool:
    return 'class="scam-comic"' in card_body


def _scam_title(card_body: str) -> str:
    m = re.search(r'<div class="scam-title">([^<]+)</div>', card_body)
    return m.group(1).strip() if m else "scam"


def insert_into_city(city: str, dry_run: bool) -> tuple[int, int]:
    """Insert <img> below <div class="scam-location"> in each scam-card.
    Returns (inserted, already_present)."""
    path = REPO / "scams" / city / "index.html"
    if not path.exists():
        print(f"  [{city}] SKIP — no index.html")
        return 0, 0
    html = path.read_text()
    original = html

    inserted = already = 0
    pattern = _scam_card_pattern()

    def replace_card(m: re.Match) -> str:
        nonlocal inserted, already
        opener, n_str, body = m.group(1), m.group(2), m.group(3)
        n = int(n_str)
        if _has_comic(body):
            already += 1
            return m.group(0)
        # Find the <div class="scam-location">…</div> line, insert <img> right after.
        loc_pattern = re.compile(r'(<div class="scam-location">📍[^<]+</div>)(\s*)')
        loc_match = loc_pattern.search(body)
        if not loc_match:
            return m.group(0)  # no location div; bail
        title = _scam_title(body)
        img = IMG_TEMPLATE.format(city=city, n=n, alt=title)
        # Match the indentation of the location div for cleaner output
        new_body = (
            body[: loc_match.end()]
            + img + "\n"
            + body[loc_match.end():]
        )
        inserted += 1
        return opener + new_body

    html = pattern.sub(replace_card, html)

    if html != original and not dry_run:
        path.write_text(html)
    return inserted, already


def bump_into_city(city: str, dry_run: bool) -> int:
    """Bump ?v=1 → ?v=2 on existing scam-comic <img> tags."""
    path = REPO / "scams" / city / "index.html"
    if not path.exists():
        return 0
    html = path.read_text()
    original = html
    # Match scam-comic src URLs and bump version
    new_html = re.sub(
        r'(class="scam-comic"[^>]*src="[^"]+/scams/' + re.escape(city) + r'/scam-\d+\.jpg)\?v=1"',
        r'\1?v=2"',
        html,
    )
    bumped = new_html.count("?v=2") - html.count("?v=2")
    if new_html != original and not dry_run:
        path.write_text(new_html)
    return bumped


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("cities", nargs="*", help="subset (default: all 10)")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    requested = set(args.cities) if args.cities else None

    print("=== INSERT phase ===")
    total_inserted = total_already = 0
    for city in INSERT_CITIES:
        if requested and city not in requested:
            continue
        ins, already = insert_into_city(city, args.dry_run)
        total_inserted += ins
        total_already += already
        print(f"  [{city}] inserted={ins} already_present={already}")

    print("\n=== BUMP phase (cache-busting v=1 → v=2) ===")
    total_bumped = 0
    for city in BUMP_CITIES:
        if requested and city not in requested:
            continue
        bumped = bump_into_city(city, args.dry_run)
        total_bumped += bumped
        print(f"  [{city}] bumped={bumped}")

    print(f"\nTOTAL: inserted={total_inserted} already={total_already} bumped={total_bumped}"
          f"{' (DRY RUN — no files written)' if args.dry_run else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
