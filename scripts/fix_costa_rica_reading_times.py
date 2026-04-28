#!/usr/bin/env python3
"""Fix reading-time on all 11 Costa Rica city scam pages.

Audit (2026-04-28) found every CR page used a 300 wpm divisor while
the canonical NYC formula is max(2, round(words/540)). Same logic as
fix_mexico_reading_times.py.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WPM = 540
CITIES = [
    "jaco-costa-rica", "la-fortuna", "liberia-costa-rica", "manuel-antonio",
    "monteverde", "puerto-viejo-costa-rica", "quepos", "san-jose-costa-rica",
    "santa-teresa", "tamarindo", "tortuguero",
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
