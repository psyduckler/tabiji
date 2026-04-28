#!/usr/bin/env python3
"""Inject a city-specific subreddit citation into each Mexico city page.

NYC canonical cites r/AskNYC and r/nyc inline within scam-story-body
paragraphs ("r/AskNYC threads document..."). All 19 Mexico cities had
ZERO specific subreddit citations — a credibility gap.

This script appends a sentence with the city's dominant subreddit to the
LAST scam-story-body paragraph of scam-1 on each city's page. One
citation per city is enough to anchor the page's evidentiary claim
without bloating the body with redundant mentions.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# Curated dominant subreddit per city (from synth-agent recommendations
# in /tmp/mexico-title-rewrite.txt, with manual disambiguation).
CITY_SUB = {
    "acapulco": ("r/acapulco", "r/MexicoTravel"),
    "cabo-san-lucas": ("r/CaboSanLucas", "r/MexicoTravel"),
    "cancun": ("r/cancun", "r/MexicoTravel"),
    "cozumel": ("r/cozumel", "r/cruise"),
    "guadalajara": ("r/guadalajara", "r/MexicoTravel"),
    "guanajuato": ("r/MexicoTravel", "r/expats"),
    "holbox": ("r/cancun", "r/MexicoTravel"),
    "isla-mujeres": ("r/cancun", "r/MexicoTravel"),
    "mazatlan": ("r/mazatlan", "r/cruise"),
    "merida": ("r/merida", "r/expats"),
    "mexico-city": ("r/mexicocity", "r/MexicoTravel"),
    "oaxaca": ("r/oaxaca", "r/MexicoTravel"),
    "playa-del-carmen": ("r/playadelcarmen", "r/cancun"),
    "puebla": ("r/MexicoTravel", "r/mexicocity"),
    "puerto-escondido": ("r/oaxaca", "r/digitalnomad"),
    "puerto-vallarta": ("r/PuertoVallarta", "r/MexicoTravel"),
    "san-cristobal-de-las-casas": ("r/chiapas", "r/MexicoTravel"),
    "san-miguel-de-allende": ("r/SanMigueldeAllende", "r/expats"),
    "tulum": ("r/Tulum", "r/cancun"),
}


def inject(city: str, primary: str, secondary: str) -> bool:
    """Append a citation sentence to the last scam-story-body inside scam-1."""
    path = REPO / f"scams/{city}/index.html"
    html = path.read_text()

    # Locate scam-1 card body.
    m = re.search(
        r'(<div class="scam-card"[^>]*id="scam-1"[^>]*>)(.*?)(<div class="scam-details">)',
        html,
        re.DOTALL,
    )
    if not m:
        return False

    head, card_body, tail_marker = m.group(1), m.group(2), m.group(3)

    # Find the LAST <p class="scam-story-body">…</p> in the card body.
    body_paragraphs = list(
        re.finditer(
            r'(<p class="scam-story-body">)(.*?)(</p>)',
            card_body,
            re.DOTALL,
        )
    )
    if not body_paragraphs:
        return False

    last = body_paragraphs[-1]
    last_text = last.group(2)

    citation = (
        f' Threads on <a href="https://www.reddit.com/{primary}/" '
        f'rel="nofollow noopener" target="_blank">{primary}</a> and '
        f'<a href="https://www.reddit.com/{secondary}/" '
        f'rel="nofollow noopener" target="_blank">{secondary}</a> '
        f"document the same pattern across multiple seasons."
    )

    if primary in last_text or secondary in last_text:
        # Already cited
        return False

    # Insert citation just before the closing </p>, after a space if needed.
    new_text = last_text.rstrip()
    if not new_text.endswith((".", "!", "?", '."', '!"', '?"', ".)", "!)", "?)")):
        new_text = new_text + "."
    new_text = new_text + citation
    new_card_body = (
        card_body[: last.start(2)]
        + new_text
        + card_body[last.end(2):]
    )
    new_html = (
        html[: m.start()]
        + head
        + new_card_body
        + tail_marker
        + html[m.end():]
    )
    path.write_text(new_html)
    return True


def main():
    ok = skipped = 0
    for slug, (primary, secondary) in sorted(CITY_SUB.items()):
        if inject(slug, primary, secondary):
            print(f"  {slug}: injected {primary} + {secondary}")
            ok += 1
        else:
            print(f"  {slug}: SKIPPED (already cited or no body found)")
            skipped += 1
    print(f"\nTotal: {ok} injected, {skipped} skipped")


if __name__ == "__main__":
    main()
