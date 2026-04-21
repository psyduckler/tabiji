#!/usr/bin/env python3
"""Insert <img class="scam-comic"> tags into Mexico scam pages for the first time.

After the v2 pipeline generates comics for all 10 Mexican cities and uploads
them to R2, this script edits each city's index.html to add an <img> tag
directly below the <div class="scam-location"> in every scam-card.

Matches the house convention (see user memory: "scam-comic placement").

Idempotent: skips any scam-card that already has an img.scam-comic tag.
Safe to re-run after adding a new city — it only inserts where missing.

Usage:
    python3 scripts/comic-pipeline/insert_mexico_comics.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

REPO = _HERE.parent.parent
AUDIT_LOG = Path("/tmp/mexico-audit.jsonl")

CITIES = [
    "mexico-city", "cancun", "tulum", "oaxaca", "merida",
    "playa-del-carmen", "puebla", "puerto-escondido",
    "puerto-vallarta", "guadalajara",
]

IMG_TAG_TEMPLATE = (
    '<img class="scam-comic" src="https://img.tabiji.ai/scams/{city}/scam-{n}.jpg" '
    'alt="{title} — comic illustration" loading="lazy" '
    'style="width:100%;height:auto;border-radius:12px;margin:1rem 0 1.25rem;display:block;">'
)


def _load_flagged() -> set[tuple[str, int]]:
    flagged: set[tuple[str, int]] = set()
    if not AUDIT_LOG.exists():
        print(f"WARN: {AUDIT_LOG} not found — treating all scams as successfully regenerated")
        return flagged
    for line in AUDIT_LOG.read_text().splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("status") == "flagged":
            flagged.add((rec["city"], rec["n"]))
    return flagged


def insert_for_city(city: str, flagged: set[tuple[str, int]]) -> tuple[int, list[str]]:
    path = REPO / f"scams/{city}/index.html"
    html = path.read_text()
    changes: list[str] = []
    inserted = 0

    # walk each scam-card in order, grab title + n from the HTML itself so we
    # don't have to import the pipeline's extract_scams (keeps this standalone)
    cards = list(re.finditer(
        r'<div class="scam-card"[^>]*id="(scam-(\d+))"[^>]*>(.*?)(?=<div class="scam-card"|<section|</section|$)',
        html, re.DOTALL,
    ))
    if not cards:
        return 0, [f"  {city}: NO scam-card divs found"]

    # process in reverse so span offsets stay valid as we rewrite
    for cm in reversed(cards):
        sid = cm.group(1)
        n = int(cm.group(2))
        body = cm.group(3)
        if (city, n) in flagged:
            changes.append(f"  {city}/{sid}: SKIP (regen flagged)")
            continue
        # already has a comic? skip
        if 'class="scam-comic"' in body:
            changes.append(f"  {city}/{sid}: already has img.scam-comic")
            continue
        tm = re.search(r'<div class="scam-title">([^<]+)</div>', body)
        if not tm:
            changes.append(f"  {city}/{sid}: NO scam-title (skip)")
            continue
        title = tm.group(1).strip().replace('"', '&quot;')

        # locate the <div class="scam-location">...</div> within this card's body
        # and inject the img tag right after its closing </div>
        card_start = cm.start()
        card_body_start = cm.start(3)
        loc_m = re.search(r'<div class="scam-location">[^<]*</div>', body)
        if not loc_m:
            changes.append(f"  {city}/{sid}: NO scam-location (skip)")
            continue
        # absolute end-offset of </div> inside the whole html
        loc_end = card_body_start + loc_m.end()
        # preserve the indentation of the scam-location line
        # (walk back from card_start up to the first newline, then find the
        # scam-location line's indent by looking ahead into body)
        indent_m = re.search(r'\n(\s*)<div class="scam-location"', html[card_start:card_body_start + loc_m.start() + 1])
        indent = indent_m.group(1) if indent_m else "        "
        img = IMG_TAG_TEMPLATE.format(city=city, n=n, title=title)
        html = html[:loc_end] + "\n" + indent + img + html[loc_end:]
        inserted += 1
        changes.append(f"  {city}/{sid}: inserted")

    path.write_text(html)
    return inserted, changes


def main() -> int:
    flagged = _load_flagged()
    if flagged:
        print(f"[flagged regen: {len(flagged)} scams skipped] {sorted(flagged)}")
    total = 0
    for city in CITIES:
        n, changes = insert_for_city(city, flagged)
        total += n
        print(f"[{city}] inserted {n} img tags")
        for line in changes:
            print(line)
    print(f"\nDONE: {total} scam-comic img tags inserted across {len(CITIES)} cities")
    return 0 if total > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
