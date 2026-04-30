#!/usr/bin/env python3
"""Undo the .book-card-buy wrapper introduced in #1336.

Returns the footer to single-row (price + CTA, like France) and moves
the rating block back to a standalone right-aligned row between
footer and readmore.

Before:
    <div class="book-card-footer">
      <div class="book-card-price">...</div>
      <div class="book-card-buy">
        <a class="book-card-cta">Buy →</a>
        <div class="book-card-rating">★ 5.0 · 4 reviews</div>
      </div>
    </div>

After:
    <div class="book-card-footer">
      <div class="book-card-price">...</div>
      <a class="book-card-cta">Buy →</a>
    </div>
    <div class="book-card-rating">★ 5.0 · 4 reviews</div>
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HUB = REPO / "books" / "index.html"


def main() -> None:
    html = HUB.read_text()
    # Match: <div class="book-card-buy">CTA + rating</div></div>
    # Capture: CTA group (\1), rating group (\2)
    pattern = re.compile(
        r'<div class="book-card-buy">'
        r'(<a[^>]*class="book-card-cta"[^>]*>[^<]*</a>)'    # \1 CTA
        r'(<div class="book-card-rating"[^>]*>.*?</div>)'    # \2 rating
        r'</div></div>',                                     # close buy + close footer
        re.DOTALL,
    )
    new_html, n = pattern.subn(
        r'\1</div>\n            \2',
        html,
    )
    HUB.write_text(new_html)
    print(f"unwrapped {n} cards")


if __name__ == "__main__":
    main()
