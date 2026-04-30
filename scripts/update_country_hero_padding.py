#!/usr/bin/env python3
"""Set hero padding-top to 1rem across all 23 country book pages.

Targets two CSS patterns inside the inline <style> block:
  1) Multi-line:  .hero { padding: 8rem 2rem 4rem; ... }
  2) Single-line: .hero { padding: 7rem 1.25rem 3rem; }

Only modifies the FIRST `padding:` declaration inside a `.hero {…}`
rule — leaves padding inside .hero-inner / .hero-eyebrow / etc. alone.
Idempotent.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

COUNTRIES = [
    "argentina", "australia", "brazil", "canada", "china", "colombia",
    "costa-rica", "egypt", "france", "germany", "greece", "indonesia",
    "italy", "japan", "malaysia", "mexico", "morocco", "portugal",
    "spain", "thailand", "turkey", "united-kingdom", "vietnam",
]

# Match any `.hero { … padding: <top> <rest>; … }` and rewrite the top to 1rem.
# Won't touch .hero-inner / .hero-eyebrow because those have a `-` after `.hero`.
HERO_RULE = re.compile(
    r'(\.hero\s*\{[^}]*?padding:\s*)([\d.]+rem)(\s+[^;]+;)',
    re.DOTALL,
)


def update_file(path: Path) -> int:
    """Returns count of padding lines updated in this file."""
    if not path.exists():
        return -1
    html = path.read_text()

    def sub(m: re.Match) -> str:
        return m.group(1) + "1rem" + m.group(3)

    new_html, n = HERO_RULE.subn(sub, html)
    if n and new_html != html:
        path.write_text(new_html)
    return n


def main() -> None:
    total = 0
    for country in COUNTRIES:
        path = REPO / "books" / f"{country}-tourist-scams" / "index.html"
        n = update_file(path)
        if n < 0:
            print(f"  · {country:18s}  no page")
            continue
        marker = "✓" if n else "·"
        print(f"  {marker} {country:18s}  {n} hero padding rule(s) updated")
        total += n
    print(f"\nTotal: {total} hero padding rules updated across {len(COUNTRIES)} country pages")


if __name__ == "__main__":
    main()
