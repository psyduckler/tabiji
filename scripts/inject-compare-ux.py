#!/usr/bin/env python3
"""
Inject compare-ux.css and compare-ux.js into all compare pages.
Only adds 2 lines to <head>. Does NOT modify any existing content.

Usage:
    python3 scripts/inject-compare-ux.py           # all pages
    python3 scripts/inject-compare-ux.py <slug>    # one page
"""
import sys, os, re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
COMPARE_DIR = REPO / "compare"

INJECT_CSS = '<link rel="stylesheet" href="/assets/compare-ux.css">'
INJECT_JS = '<script defer src="/assets/compare-ux.js"></script>'
MARKER = 'compare-ux.css'  # skip pages that already have it


def inject_page(slug: str) -> bool:
    path = COMPARE_DIR / slug / "index.html"
    if not path.exists():
        return False

    html = path.read_text("utf-8")

    # Skip if already injected
    if MARKER in html:
        return False

    # Skip if not a compare page (no deep-dive sections)
    if 'class="deep-dive"' not in html:
        return False

    # Inject before </head>
    if '</head>' not in html:
        return False

    html = html.replace(
        '</head>',
        f'{INJECT_CSS}\n{INJECT_JS}\n</head>'
    )

    path.write_text(html, "utf-8")
    return True


def main():
    if len(sys.argv) > 1 and sys.argv[1] != '--all':
        slug = sys.argv[1]
        if inject_page(slug):
            print(f"OK   {slug}")
        else:
            print(f"SKIP {slug}")
        return

    # All compare pages
    slugs = sorted([
        d for d in os.listdir(COMPARE_DIR)
        if '-vs-' in d and (COMPARE_DIR / d / "index.html").is_file()
    ])

    injected = 0
    skipped = 0
    for i, slug in enumerate(slugs):
        if inject_page(slug):
            injected += 1
            if (injected % 100 == 0):
                print(f"  ...{injected} injected so far")
        else:
            skipped += 1

    print(f"Done: {injected} injected, {skipped} skipped (already had it or no deep-dives)")


if __name__ == "__main__":
    main()
