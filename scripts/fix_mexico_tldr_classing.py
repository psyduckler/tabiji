#!/usr/bin/env python3
"""Re-class missing TLDRs across Mexico city scam pages.

NYC canonical pattern: each scam-card has 1 <p class="scam-tldr"> followed
by 3 <p class="scam-story-body">. 9 Mexico cities are missing some TLDRs —
the first body paragraph is acting as a TLDR but lacks the right class.

This script: for every scam-card with no scam-tldr, re-class the first
<p class="scam-story-body"> to <p class="scam-tldr">.

Acapulco special case: 4 cards have 4 story-body paragraphs (not 3 + 1
TLDR). Same fix — re-class the first to scam-tldr — leaves the canonical
3 body paragraphs.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CITIES = [
    "acapulco", "cabo-san-lucas", "cozumel", "guanajuato", "holbox",
    "isla-mujeres", "mazatlan", "san-cristobal-de-las-casas",
    "san-miguel-de-allende",
]

CARD_RE = re.compile(
    r'(<div class="scam-card"[^>]*id="scam-\d+"[^>]*>)(.*?)'
    r'(?=<div class="scam-card"|<div class="mid-cta"|<!-- What to do)',
    re.DOTALL,
)


def fix_card(body: str) -> str:
    if 'class="scam-tldr"' in body:
        return body
    return re.sub(
        r'<p class="scam-story-body">',
        r'<p class="scam-tldr">',
        body,
        count=1,
    )


def main() -> None:
    for city in CITIES:
        path = REPO / f"scams/{city}/index.html"
        html = path.read_text()
        before_tldr = html.count('class="scam-tldr"')
        before_body = html.count('class="scam-story-body"')

        new_html = CARD_RE.sub(
            lambda m: m.group(1) + fix_card(m.group(2)),
            html,
        )
        after_tldr = new_html.count('class="scam-tldr"')
        after_body = new_html.count('class="scam-story-body"')

        path.write_text(new_html)
        print(
            f"  {city}: tldr {before_tldr}→{after_tldr}, "
            f"story-body {before_body}→{after_body}"
        )


if __name__ == "__main__":
    main()
