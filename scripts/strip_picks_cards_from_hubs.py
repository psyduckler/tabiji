#!/usr/bin/env python3
"""
Strip <a class="pick-card" href="/popular-picks/{drop}/">...</a> anchors from all
popular-picks HTML hub pages, plus remove the dropped slugs from
popular-picks-hub-data/*.json so future rebuilds don't re-add them.

Run after apply_picks_drops.py.
"""

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PICKS_DIR = ROOT / "popular-picks"
HUB_DATA_DIR = ROOT / "popular-picks-hub-data"
TIERS_CSV = ROOT / "scripts" / "compare-analysis" / "picks-tiers.csv"


def load_drops():
    with open(TIERS_CSV) as f:
        return {
            r["slug"] for r in csv.DictReader(f)
            if r["page_type"] == "topic" and int(r["volume"]) == 0
        }


def strip_card(html, slug):
    # Match <a ... href="/popular-picks/{slug}/" ... class="pick-card" ...> ... </a>
    # Cards may have class before or after href — use two patterns
    patterns = [
        re.compile(
            rf'<a\s+href="/popular-picks/{re.escape(slug)}/"\s+class="pick-card"[^>]*>.*?</a>',
            re.DOTALL,
        ),
        re.compile(
            rf'<a\s+class="pick-card"\s+href="/popular-picks/{re.escape(slug)}/"[^>]*>.*?</a>',
            re.DOTALL,
        ),
    ]
    total_removed = 0
    for p in patterns:
        new, n = p.subn("", html)
        if n:
            html = new
            total_removed += n
    return html, total_removed


def strip_hub_html(drops):
    """Patch all HTML hubs + the main popular-picks/index.html."""
    touched = 0
    for hub_html in PICKS_DIR.glob("*/index.html"):
        # Only hub pages (not leaf pages that we've already deleted — those are gone)
        # Heuristic: country hub pages are at /popular-picks/{country}/ — 109 of them
        content = hub_html.read_text(encoding="utf-8")
        total = 0
        for slug in drops:
            if f'/popular-picks/{slug}/' not in content:
                continue
            content, n = strip_card(content, slug)
            total += n
        if total:
            hub_html.write_text(content, encoding="utf-8")
            touched += 1
            print(f"  {hub_html.relative_to(ROOT)}: removed {total} cards")
    # Also patch /popular-picks/index.html
    root_html = PICKS_DIR / "index.html"
    content = root_html.read_text(encoding="utf-8")
    total = 0
    for slug in drops:
        if f'/popular-picks/{slug}/' not in content:
            continue
        content, n = strip_card(content, slug)
        total += n
    if total:
        root_html.write_text(content, encoding="utf-8")
        touched += 1
        print(f"  popular-picks/index.html: removed {total} cards")
    return touched


def strip_hub_data(drops):
    """Remove dropped slugs from popular-picks-hub-data/*.json sections[].cards[]."""
    touched = 0
    for path in sorted(HUB_DATA_DIR.glob("*.json")):
        if " 2.json" in path.name:
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        removed = 0
        for section in data.get("sections", []):
            cards = section.get("cards", [])
            kept = []
            for c in cards:
                slug = c.get("slug") or c.get("href", "").strip("/").split("/")[-1]
                if slug in drops:
                    removed += 1
                else:
                    kept.append(c)
            if len(kept) != len(cards):
                section["cards"] = kept
        if removed:
            path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            touched += 1
            print(f"  {path.relative_to(ROOT)}: removed {removed} cards")
    return touched


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slugs-file", help="Newline-delimited slug file (overrides default zero-vol selection)")
    args = ap.parse_args()
    if args.slugs_file:
        with open(args.slugs_file) as f:
            drops = {l.strip() for l in f if l.strip()}
    else:
        drops = load_drops()
    print(f"Drop count: {len(drops)}")
    print("\nStripping HTML hub pages:")
    html_touched = strip_hub_html(drops)
    print(f"HTML files touched: {html_touched}")
    print("\nStripping hub-data JSONs:")
    json_touched = strip_hub_data(drops)
    print(f"JSON files touched: {json_touched}")


if __name__ == "__main__":
    main()
