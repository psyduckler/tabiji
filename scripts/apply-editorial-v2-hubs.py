#!/usr/bin/env python3
"""One-shot cutover for the 59 country hubs at /scams/country/*/index.html.

Applies the editorial-v2 system to existing hub HTML without requiring a
full generator regeneration (the next generator run will emit the same
markup natively — see the template update in `scams/generate_pages.py`).

Per page:
  1. Strip the inline <style>…</style> block.
  2. Insert `<link rel="stylesheet" href="/assets/scams.css">` in its place.
  3. Add `class="editorial-v2"` to <body>.
  4. Wrap the country name in the H1 with <em> (e.g.
     `Scams to watch for in <em>United States</em>`).

Idempotent. Run with `--dry-run` to preview.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COUNTRY_DIR = ROOT / "scams" / "country"

STYLE_BLOCK_RE = re.compile(r"    <style>.*?</style>\n", re.DOTALL)
STYLESHEET_LINE = '    <link rel="stylesheet" href="/assets/scams.css">\n'
BODY_OPEN_RE = re.compile(r'<body(?:\s+class="[^"]*")?>')

# H1 shape on country hubs:
#   <h1><span class="page-hero-flag">🇺🇸</span>Scams to watch for in United States</h1>
H1_RE = re.compile(
    r'(<h1>(?:<span[^>]*class="page-hero-flag"[^>]*>[^<]*</span>)?'
    r'Scams to watch for in )([^<]+?)(</h1>)'
)


def migrate(page: Path) -> tuple[str, bool]:
    cc = page.parent.name
    if not page.exists():
        return (cc, False)

    html = page.read_text(encoding="utf-8")
    original = html

    # 1. Replace inline <style> with stylesheet link
    if "<style>" in html and "/assets/scams.css" not in html:
        html = STYLE_BLOCK_RE.sub(STYLESHEET_LINE, html, count=1)

    # 2. Flag body
    def _body_sub(m):
        tag = m.group(0)
        if "editorial-v2" in tag:
            return tag
        if 'class="' in tag:
            return tag.replace('class="', 'class="editorial-v2 ', 1)
        return '<body class="editorial-v2">'

    html = BODY_OPEN_RE.sub(_body_sub, html, count=1)

    # 3. Wrap country name in H1 <em>
    def _h1_wrap(m):
        prefix, country, suffix = m.group(1), m.group(2), m.group(3)
        if "<em>" in prefix:
            return m.group(0)  # already wrapped
        return f"{prefix}<em>{country}</em>{suffix}"

    html = H1_RE.sub(_h1_wrap, html, count=1)

    changed = html != original
    if changed:
        page.write_text(html, encoding="utf-8")
    return (cc, changed)


def main(argv: list[str]) -> int:
    dry = "--dry-run" in argv
    pages = sorted((p / "index.html") for p in COUNTRY_DIR.iterdir()
                   if p.is_dir() and p.name != "__pycache__")
    stats = {"changed": 0, "no-op": 0}
    for page in pages:
        cc, changed = migrate(page)
        status = "changed" if changed else "no-op"
        stats[status] += 1
        print(f"  {status:7s} {cc}")
    print(f"\n{stats['changed']}/{len(pages)} hubs migrated")
    if dry:
        print("(dry-run — no writes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
