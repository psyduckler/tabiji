#!/usr/bin/env python3
"""Fix reading-time on all 10 Morocco city scam pages.

Audit (2026-04-28) found Casablanca/Tangier/Fez stated 14/15/11 min while
actual word counts at 540 wpm (NYC canonical skim rate) yield 8/8/7. Same
pattern as Mexico fix in scripts/fix_mexico_reading_times.py.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WPM = 540
CITIES = [
    "marrakech", "casablanca", "rabat", "tangier", "fez",
    "agadir", "merzouga", "ouarzazate", "chefchaouen", "essaouira",
]


def main() -> None:
    for city in CITIES:
        path = REPO / f"scams/{city}/index.html"
        html = path.read_text()
        m = re.search(r"<main[^>]*>(.*?)</main>", html, re.DOTALL)
        if not m:
            print(f"  {city}: SKIPPED (no <main>)")
            continue
        text = re.sub(r"<[^>]+>", " ", m.group(1))
        words = len(text.split())
        new_min = max(2, round(words / WPM))
        old_match = re.search(r'(class="reading-time"[^>]*>[^<]*?)(\d+)( min read)', html)
        if not old_match:
            print(f"  {city}: NO reading-time found")
            continue
        old_min = int(old_match.group(2))
        if old_min == new_min:
            print(f"  {city}: already {new_min} min ({words} words) — skip")
            continue
        new_html = (
            html[: old_match.start(2)]
            + str(new_min)
            + html[old_match.end(2):]
        )
        path.write_text(new_html)
        print(f"  {city}: {old_min} → {new_min} min ({words} words)")


if __name__ == "__main__":
    main()
