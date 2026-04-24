#!/usr/bin/env python3
"""Reconcile hero 'N scams documented' count with actual .scam-card count
and remove any empty .scam-tldr paragraphs left behind by earlier sweeps.

Runs across all scams/<slug>/index.html. Idempotent.

Usage:
    python3 scripts/sweep_count_and_empty_tldr.py --dry-run
    python3 scripts/sweep_count_and_empty_tldr.py
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scam_sweep_common import collect_scam_targets

REPO = Path(__file__).resolve().parents[1]

_HERO_COUNT_RE = re.compile(r"💬\s*(\d+)\s+scams\s+documented", re.IGNORECASE)


def _fix_page(path: Path) -> tuple[str, int, int, int]:
    """Compute the fixed HTML. Returns (new_src, hero_fixed, empty_removed, n_cards).

    Returns new_src == original src when nothing changed so callers can cheap-skip.
    """
    src = path.read_text()
    soup = BeautifulSoup(src, "html.parser")
    n_cards = len(soup.select(".scam-card"))
    if n_cards == 0:
        return src, 0, 0, 0

    hero_fixed = 0

    def _hero_replace(m: re.Match) -> str:
        nonlocal hero_fixed
        if int(m.group(1)) != n_cards:
            hero_fixed = 1
        return f"💬 {n_cards} scams documented"

    new_src = _HERO_COUNT_RE.sub(_hero_replace, src)

    # Remove empty .scam-tldr paragraphs from the same parse tree we used for
    # the card count — one BS4 parse per file, not three.
    empty = 0
    for t in soup.select(".scam-tldr"):
        if not t.get_text(strip=True):
            t.decompose()
            empty += 1
    if empty:
        # BS4's re-serialize normalizes whitespace, but it's the only way to
        # delete an element. Accept the reflow on pages that actually have
        # empty TLDRs (rare); the hero-only fast path above uses regex.
        new_src = str(soup)
        # Re-apply hero fix since str(soup) came from the pre-regex source.
        new_src = _HERO_COUNT_RE.sub(f"💬 {n_cards} scams documented", new_src)

    return new_src, hero_fixed, empty, n_cards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()

    targets = collect_scam_targets(city_pages=True)
    if args.limit:
        targets = targets[: args.limit]

    total_hero = 0
    total_empty = 0
    files_touched = 0
    for path in targets:
        new_src, hero, empty, cards = _fix_page(path)
        if hero == 0 and empty == 0:
            continue
        files_touched += 1
        total_hero += hero
        total_empty += empty
        label = str(path.relative_to(REPO))
        print(f"  {label:55} — hero={hero} empty_tldr={empty} cards={cards}")
        if not args.dry_run:
            path.write_text(new_src)

    action = "would fix" if args.dry_run else "fixed"
    print(f"\n{action} hero-count in {total_hero} pages, removed {total_empty} empty tldrs ({files_touched} files touched)")


if __name__ == "__main__":
    main()
