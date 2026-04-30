#!/usr/bin/env python3
"""Restructure book-card footer so the rating sits beneath the Buy CTA.

Before:
    <div class="book-card-footer">
        <div class="book-card-price">…</div>
        <a class="book-card-cta">Buy on Amazon →</a>
    </div>
    <div class="book-card-rating">★ 5.0 · 4 reviews</div>

After:
    <div class="book-card-footer">
        <div class="book-card-price">…</div>
        <div class="book-card-buy">
            <a class="book-card-cta">Buy on Amazon →</a>
            <div class="book-card-rating">★ 5.0 · 4 reviews</div>
        </div>
    </div>

Idempotent: skips cards that already have .book-card-buy.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HUB = REPO / "books" / "index.html"


def main() -> None:
    html = HUB.read_text()
    if 'class="book-card-buy"' in html:
        existing = html.count('class="book-card-buy"')
        # could be partially applied; carry on but report
    pattern = re.compile(
        r'(<a[^>]*class="book-card-cta"[^>]*>[^<]*</a>)\s*'   # \1 = CTA
        r'</div>\s*'                                           # closing of book-card-footer
        r'(<div class="book-card-rating"[^>]*>.*?</div>)',     # \2 = rating block
        re.DOTALL,
    )
    new_html, n = pattern.subn(
        r'<div class="book-card-buy">\1\2</div></div>',
        html,
    )
    if n == 0:
        print("no cards to restructure (already done?)")
        return
    HUB.write_text(new_html)
    print(f"restructured {n} cards")


if __name__ == "__main__":
    main()
