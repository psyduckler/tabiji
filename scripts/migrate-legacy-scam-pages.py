#!/usr/bin/env python3
"""Migrate the 25 legacy scam pages (Australia + Thailand) onto the shared
`/assets/scams.css` + `body.editorial-v2` system.

Each legacy page currently inlines ~100 lines of <style> before its main
content. The inline styles are the pre-v2 palette and are redundant with
what `/assets/scams.css` now ships. This script:

  1. Replaces the inline <style>...</style> block with a single
     <link rel="stylesheet" href="/assets/scams.css"> line.
  2. Flags the <body> with class="editorial-v2" so the new gated CSS
     applies.
  3. Wraps the city name in the H1 with <em> for the italic-terracotta
     accent (e.g. "6 Tourist Scams in <em>Cairns</em>").

Idempotent: re-running is a no-op on already-migrated pages.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAMS = ROOT / "scams"

LEGACY = [
    "adelaide", "alice-springs", "ayutthaya", "bangkok", "brisbane",
    "byron-bay", "cairns", "canberra", "chiang-mai", "darwin",
    "gold-coast", "hobart", "hua-hin", "koh-phangan", "koh-phi-phi",
    "koh-samui", "koh-tao", "krabi", "melbourne", "pattaya",
    "perth", "phuket", "port-douglas", "sydney", "whitsundays",
]

CITY_DISPLAY = {
    "adelaide": "Adelaide", "alice-springs": "Alice Springs",
    "ayutthaya": "Ayutthaya", "bangkok": "Bangkok", "brisbane": "Brisbane",
    "byron-bay": "Byron Bay", "cairns": "Cairns", "canberra": "Canberra",
    "chiang-mai": "Chiang Mai", "darwin": "Darwin",
    "gold-coast": "Gold Coast", "hobart": "Hobart", "hua-hin": "Hua Hin",
    "koh-phangan": "Koh Phangan", "koh-phi-phi": "Koh Phi Phi",
    "koh-samui": "Koh Samui", "koh-tao": "Koh Tao", "krabi": "Krabi",
    "melbourne": "Melbourne", "pattaya": "Pattaya", "perth": "Perth",
    "phuket": "Phuket", "port-douglas": "Port Douglas", "sydney": "Sydney",
    "whitsundays": "Whitsundays",
}

STYLE_BLOCK_RE = re.compile(r"    <style>.*?</style>\n", re.DOTALL)
STYLESHEET_LINE = '    <link rel="stylesheet" href="/assets/scams.css">\n'
BODY_OPEN_RE = re.compile(r"<body>")
BODY_V2 = '<body class="editorial-v2">'


def migrate(slug: str) -> tuple[str, bool]:
    path = SCAMS / slug / "index.html"
    if not path.exists():
        return (slug, False)

    html = path.read_text(encoding="utf-8")
    original = html

    # 1. Strip inline <style>, insert stylesheet link (only if not already linked)
    if "<style>" in html and '/assets/scams.css' not in html:
        html = STYLE_BLOCK_RE.sub(STYLESHEET_LINE, html, count=1)

    # 2. Flag body
    if '<body class="editorial-v2">' not in html:
        html = BODY_OPEN_RE.sub(BODY_V2, html, count=1)

    # 3. Wrap city in H1 <em>
    city = CITY_DISPLAY[slug]
    # Match the exact H1 pattern (with or without existing whitespace quirks)
    h1_pattern = re.compile(
        r"(<h1>[^<]*?)" + re.escape(city) + r"(</h1>)"
    )

    def _wrap(m):
        before, after = m.group(1), m.group(2)
        if "<em>" in before:  # already wrapped
            return m.group(0)
        return f"{before}<em>{city}</em>{after}"

    html = h1_pattern.sub(_wrap, html, count=1)

    changed = html != original
    if changed:
        path.write_text(html, encoding="utf-8")
    return (slug, changed)


def main(argv: list[str]) -> int:
    dry = "--dry-run" in argv
    results = []
    for slug in LEGACY:
        slug_, changed = migrate(slug)
        results.append((slug_, changed))
        status = "changed" if changed else "no-op"
        print(f"  {status:7s} {slug_}")

    total = sum(1 for _, c in results if c)
    print(f"\n{total}/{len(LEGACY)} pages migrated.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
