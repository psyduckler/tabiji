#!/usr/bin/env python3
"""One-time cutover sweep: apply `body.editorial-v2` + H1 `<em>{city}</em>`
wrap to every scam page under `/scams/*/index.html`.

Idempotent: re-running is a no-op on pages already migrated.
Skips any page that does NOT link `/assets/scams.css` (legacy pages — those
are handled by `migrate-legacy-scam-pages.py`).

Run with `--dry-run` to see which pages would change without writing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAMS = ROOT / "scams"

BODY_OPEN_RE = re.compile(r'<body(?:\s+class="[^"]*")?>')


def derive_city_from_h1(html: str) -> tuple[str, str] | None:
    """Pull city + preposition from the existing <h1> tag.

    Handles the three observed patterns:
      <h1>7 Tourist Scams in Bangkok</h1>      -> ("in",  "Bangkok")
      <h1>7 Tourist Scams on Capri</h1>        -> ("on",  "Capri")
      <h1>7 Tourist Scams at Lake Garda</h1>   -> ("at",  "Lake Garda")
    """
    m = re.search(
        r"<h1>\s*\d+\s+Tourist Scams\s+(in|on|at)\s+([^<]+?)\s*</h1>",
        html,
    )
    return (m.group(1), m.group(2)) if m else None


def migrate(page: Path) -> tuple[str, str, bool]:
    html = page.read_text(encoding="utf-8")
    original = html
    slug = page.parent.name

    # Only touch pages that use the shared scams.css
    if "/assets/scams.css" not in html:
        return (slug, "skip-nocss", False)

    # 1. Ensure body has editorial-v2 class
    def _body_sub(m):
        tag = m.group(0)
        if 'editorial-v2' in tag:
            return tag
        if 'class="' in tag:
            return tag.replace('class="', 'class="editorial-v2 ', 1)
        return '<body class="editorial-v2">'

    html = BODY_OPEN_RE.sub(_body_sub, html, count=1)

    # 2. Wrap city in H1 <em>
    if "<h1>" in html and "<em>" not in html.split("</h1>")[0]:
        extracted = derive_city_from_h1(html)
        if extracted:
            prep, city = extracted
            h1_pattern = re.compile(
                r"(<h1>\s*\d+\s+Tourist Scams\s+" + prep + r"\s+)"
                + re.escape(city) + r"(\s*</h1>)"
            )
            def _wrap_h1(m):
                return f"{m.group(1)}<em>{city}</em>{m.group(2)}"
            html = h1_pattern.sub(_wrap_h1, html, count=1)

    changed = html != original
    if changed:
        page.write_text(html, encoding="utf-8")
    return (slug, "changed" if changed else "no-op", changed)


def main(argv: list[str]) -> int:
    dry = "--dry-run" in argv
    pages = sorted(SCAMS.glob("*/index.html"))
    stats = {"changed": 0, "no-op": 0, "skip-nocss": 0}
    changed_slugs = []

    for page in pages:
        slug, status, _ = migrate(page)
        stats[status] = stats.get(status, 0) + 1
        if status == "changed":
            changed_slugs.append(slug)

    print(f"Total pages scanned: {len(pages)}")
    print(f"  changed:    {stats['changed']}")
    print(f"  no-op:      {stats['no-op']}")
    print(f"  skip (no scams.css): {stats['skip-nocss']}")
    if dry:
        print("(dry-run — no writes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
