#!/usr/bin/env python3
"""Three corpus-wide a11y fixes on /compare/ leaf pages:

  #11 dd-header div+onclick → add role/tabindex/onkeydown so keyboard users
      can expand collapsible deep-dive sections.
  #12 toc-mobile div+onclick → same role/tabindex/onkeydown treatment so
      keyboard users can open the mobile TOC dropdown.
  #13 <section id="main" class="hero"> + <div class="article-content"> →
      restructure to <section class="hero"> + <main id="main"> wrapping
      <div class="article-content"> so the page has a real main landmark
      (skip-link target now hits the main content, not the hero).

All three transformations are content-preserving — no styling or behavior
changes for sighted/mouse users; pure a11y win.

Usage:
  python3 scripts/fix_a11y_template.py            # apply
  python3 scripts/fix_a11y_template.py --dry-run  # report only
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COMPARE = REPO / "compare"

HUBS = {
    "asia", "australia", "bali", "cities", "colombia", "countries", "croatia",
    "culture", "egypt", "europe", "global-mixed", "greece", "hawaii", "iceland",
    "islands", "italy", "japan", "latin-america", "luxury", "maldives", "mexico",
    "middle-east-africa", "morocco", "nature", "new-zealand", "north-america",
    "oceania", "portugal", "spain", "taiwan", "thailand", "trip-style-guides",
    "vietnam",
}

# #11: dd-header collapsible-section toggles
DD_OLD = '<div class="dd-header" onclick="toggleSection(this.parentElement)">'
DD_NEW = (
    '<div class="dd-header" role="button" tabindex="0" '
    'onclick="toggleSection(this.parentElement)" '
    'onkeydown="if(event.key===\'Enter\'||event.key===\' \')'
    '{event.preventDefault();toggleSection(this.parentElement)}">'
)

# #12: toc-mobile dropdown toggle (the broken variant has id="toc-mobile" + onclick)
TOC_OLD = (
    '<div class="toc-mobile" id="toc-mobile" '
    'onclick="this.classList.toggle(\'open\')">'
)
TOC_NEW = (
    '<div class="toc-mobile" id="toc-mobile" role="button" tabindex="0" '
    'aria-label="Toggle table of contents" '
    'onclick="this.classList.toggle(\'open\')" '
    'onkeydown="if(event.key===\'Enter\'||event.key===\' \')'
    '{event.preventDefault();this.classList.toggle(\'open\')}">'
)

# #13: <section id="main" class="hero"> → <section class="hero"> + <main> wraps article
SECTION_MAIN_OLD = '<section id="main" class="hero">'
SECTION_MAIN_NEW = '<section class="hero">'
ARTICLE_OPEN_OLD = '<div class="article-content">'
ARTICLE_OPEN_NEW = '<main id="main" tabindex="-1">\n<div class="article-content">'
ARTICLE_CLOSE_OLD = '</div><!-- /article-content -->'
ARTICLE_CLOSE_NEW = '</div><!-- /article-content -->\n</main>'


def fix_leaf(path: Path, dry_run: bool) -> dict[str, int]:
    """Apply the three transformations. Returns counts per fix."""
    txt = path.read_text(errors="replace")
    orig = txt

    counts = {"dd": 0, "toc": 0, "main": 0}

    if DD_OLD in txt:
        counts["dd"] = txt.count(DD_OLD)
        txt = txt.replace(DD_OLD, DD_NEW)

    if TOC_OLD in txt:
        counts["toc"] = txt.count(TOC_OLD)
        txt = txt.replace(TOC_OLD, TOC_NEW)

    if SECTION_MAIN_OLD in txt:
        # Only do the section→main restructure if all three markers are present.
        if (
            ARTICLE_OPEN_OLD in txt and ARTICLE_CLOSE_OLD in txt
            # Sanity: only one section-main per page (verified across corpus)
            and txt.count(SECTION_MAIN_OLD) == 1
            and txt.count(ARTICLE_OPEN_OLD) == 1
            and txt.count(ARTICLE_CLOSE_OLD) == 1
        ):
            txt = txt.replace(SECTION_MAIN_OLD, SECTION_MAIN_NEW, 1)
            txt = txt.replace(ARTICLE_OPEN_OLD, ARTICLE_OPEN_NEW, 1)
            txt = txt.replace(ARTICLE_CLOSE_OLD, ARTICLE_CLOSE_NEW, 1)
            counts["main"] = 1

    if txt != orig and not dry_run:
        path.write_text(txt)

    return counts


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    leaves = sorted(
        p for p in COMPARE.glob("*/index.html") if p.parent.name not in HUBS
    )
    totals = {"dd": 0, "toc": 0, "main": 0}
    leaves_touched = 0

    for leaf in leaves:
        counts = fix_leaf(leaf, args.dry_run)
        if any(counts.values()):
            leaves_touched += 1
        for k, v in counts.items():
            totals[k] += v

    print(f"Leaves processed:    {len(leaves)}")
    print(f"Leaves touched:      {leaves_touched}")
    print(f"  #11 dd-header swaps:   {totals['dd']}")
    print(f"  #12 toc-mobile swaps:  {totals['toc']}")
    print(f"  #13 section→main:      {totals['main']}")
    if args.dry_run:
        print("\n[dry-run — no files modified]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
