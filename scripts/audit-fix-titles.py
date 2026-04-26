#!/usr/bin/env python3
"""Title hygiene for popular-picks leaves.

Two fixes, applied to <title>, og:title content, and twitter:title content:

  A. bare 2026 → (2026)
     "18 Best Ceviche Spots in Lima 2026 — ..." → "18 Best Ceviche Spots in Lima (2026) — ..."

  B. missing N prefix (title starts with "Best ", no leading count)
     Pulls N from JSON-LD `numberOfItems`. Skipped if numberOfItems is absent.
     "Best Breakfast in Dallas (2026) — ..." (numberOfItems: 9)
        → "9 Best Breakfast in Dallas (2026) — ..."

The JSON-LD `headline` / ItemList `name` already carry the N prefix and no
year, so they're left alone.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAVES_DIR = ROOT / "popular-picks"

BARE_2026 = re.compile(r'(?<!\()\b2026\b(?!\))')
STARTS_WITH_BEST = re.compile(r'^Best [A-Z]')
NUMBER_OF_ITEMS = re.compile(r'"numberOfItems":\s*(\d+)')

TITLE_TAG = re.compile(r'<title>([^<]*)</title>')
OG_TITLE = re.compile(r'(<meta property="og:title" content=")([^"]*)(")')
TWITTER_TITLE = re.compile(r'(<meta name="twitter:title" content=")([^"]*)(")')


def fix_title(title: str, n_items: int | None) -> tuple[str, list[str]]:
    changes: list[str] = []
    new = title
    if BARE_2026.search(new):
        new = BARE_2026.sub("(2026)", new)
        changes.append("parens")
    if n_items is not None and STARTS_WITH_BEST.match(new):
        new = f"{n_items} " + new
        changes.append("n_prefix")
    return new, changes


def process(path: Path) -> tuple[bool, list[str]]:
    text = path.read_text()
    n_match = NUMBER_OF_ITEMS.search(text)
    n_items = int(n_match.group(1)) if n_match else None

    all_changes: list[str] = []

    def repl_title(m: re.Match) -> str:
        new, changes = fix_title(m.group(1), n_items)
        all_changes.extend(changes)
        return f"<title>{new}</title>"

    new_text = TITLE_TAG.sub(repl_title, text, count=1)

    def repl_meta(m: re.Match) -> str:
        new, changes = fix_title(m.group(2), n_items)
        all_changes.extend(changes)
        return f"{m.group(1)}{new}{m.group(3)}"

    new_text = OG_TITLE.sub(repl_meta, new_text, count=1)
    new_text = TWITTER_TITLE.sub(repl_meta, new_text, count=1)

    if new_text == text:
        return False, []
    path.write_text(new_text)
    return True, all_changes


def main() -> None:
    files_changed = 0
    parens_count = 0
    nprefix_count = 0
    for leaf_dir in sorted(LEAVES_DIR.iterdir()):
        if not leaf_dir.is_dir():
            continue
        index = leaf_dir / "index.html"
        if not index.exists():
            continue
        changed, changes = process(index)
        if changed:
            files_changed += 1
            parens_count += changes.count("parens")
            nprefix_count += changes.count("n_prefix")
    # Each file has up to 3 title locations; counts are per-location.
    print(
        f"updated {files_changed} files — "
        f"{parens_count} parens fixes, {nprefix_count} n-prefix fixes (across title/og/twitter)"
    )


if __name__ == "__main__":
    main()
