#!/usr/bin/env python3
"""Inject <img class="scam-comic"> tags into city scam pages where missing.

For each scam-card on the given city pages, if the card has a
<div class="scam-location"> but no <img class="scam-comic">, inserts the
canonical img tag immediately after the scam-location div.

Used after running scripts/comic-pipeline/generate.py against cities that
have never had comics generated (Tier 1 in the audit), so the new R2 images
become visible on the live page.

Usage:
    python3 scripts/comic-pipeline/inject_html.py seattle houston savannah
    python3 scripts/comic-pipeline/inject_html.py <city> --dry-run
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
IMG_BASE = "https://img.tabiji.ai/scams"
ALT_MAX = 70

IMG_TEMPLATE = (
    '<img alt="{alt}" class="scam-comic" loading="lazy" '
    'src="{src}" style="width:100%;height:auto;border-radius:12px;'
    'margin:1rem 0 1.25rem;display:block;" width="1200" height="675" '
    'decoding="async"/>'
)

CARD_RE = re.compile(
    r'(<div class="scam-card"[^>]*id="(scam-\d+)"[^>]*>)(.*?)(?=<div class="scam-card"|<section|</section|\Z)',
    re.DOTALL,
)
TITLE_RE = re.compile(r'<div class="scam-title">([^<]+)</div>')
LOC_RE = re.compile(r'(<div class="scam-location">[^<]+</div>)')
HAS_COMIC_RE = re.compile(r'class="scam-comic"')


def truncate_alt(title: str) -> str:
    title = re.sub(r"\([^)]+\)", "", title).strip()
    if len(title) > ALT_MAX:
        title = title[:ALT_MAX].rstrip()
    return f"{title} — comic illustration"


def inject(city: str, dry_run: bool = False) -> int:
    path = REPO / f"scams/{city}/index.html"
    if not path.exists():
        print(f"  [{city}] HTML not found at {path}")
        return 0

    html = path.read_text()
    counter = [0]

    def replace_card(m):
        card_open, sid, body = m.group(1), m.group(2), m.group(3)
        n = int(sid.split("-")[1])
        if HAS_COMIC_RE.search(body):
            return m.group(0)
        tm = TITLE_RE.search(body)
        lm = LOC_RE.search(body)
        if not tm or not lm:
            print(f"  [{city}/{sid}] skipping — no title or location div")
            return m.group(0)
        alt = truncate_alt(tm.group(1).strip()).replace('"', "&quot;")
        src = f"{IMG_BASE}/{city}/scam-{n}.jpg"
        img_tag = IMG_TEMPLATE.format(alt=alt, src=src)
        new_body = body.replace(lm.group(1), f"{lm.group(1)}\n{img_tag}", 1)
        print(f"  [{city}/{sid}] inject: {alt[:65]}")
        counter[0] += 1
        return f"{card_open}{new_body}"

    new_html = CARD_RE.sub(replace_card, html)
    if counter[0] > 0 and not dry_run:
        path.write_text(new_html)
    return counter[0]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("cities", nargs="+")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    total = 0
    for city in args.cities:
        print(f"\n→ {city}")
        total += inject(city, dry_run=args.dry_run)
    label = "[dry-run] would inject" if args.dry_run else "injected"
    print(f"\n{label} {total} tag(s) across {len(args.cities)} cities")


if __name__ == "__main__":
    main()
