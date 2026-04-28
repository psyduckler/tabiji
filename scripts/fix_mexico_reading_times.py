#!/usr/bin/env python3
"""Fix reading-time on all 19 Mexico city scam pages.

Audit found every Mexico page lists 12-14 min while the actual word count
yields 6-7 min at 540 wpm (the canonical NYC skim rate). This script:

1. Counts words inside <main> for each page
2. Computes max(2, round(words/540))
3. Replaces the 'X min read' literal in the .reading-time div
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WPM = 540
CITIES = [
    "acapulco", "cabo-san-lucas", "cancun", "cozumel", "guadalajara",
    "guanajuato", "holbox", "isla-mujeres", "mazatlan", "merida",
    "mexico-city", "oaxaca", "playa-del-carmen", "puebla", "puerto-escondido",
    "puerto-vallarta", "san-cristobal-de-las-casas", "san-miguel-de-allende",
    "tulum",
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
            print(f"  {city}: already {new_min} min — skip")
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
