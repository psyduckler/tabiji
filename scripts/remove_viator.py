#!/usr/bin/env python3
"""One-shot removal of all Viator affiliate blocks from /compare/ leaf pages.

Removes:
  1. <section class="viator-section">…</section> (and any optional `<!-- Viator -->`
     comment marker immediately preceding it) from every leaf in compare/
  2. Inline .viator-* CSS rule blocks from <style> elements (some pages have
     these duplicated 1–3 times due to past build-pipeline bugs)
  3. The .viator-* CSS rules block from assets/compare-shared.css

Safety:
  - Refuses to write a file if any "viator" reference (case-insensitive) remains
    after the substitution.
  - --dry-run prints per-file delta without modifying anything.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COMPARE = REPO / "compare"
SHARED_CSS = REPO / "assets" / "compare-shared.css"

VIATOR_HTML_BLOCK = re.compile(
    r"(?:[ \t]*<!--\s*Viator\s*-->\s*\n)?"
    r"[ \t]*<section class=\"viator-section\">.*?</section>[ \t]*\n",
    re.DOTALL,
)

VIATOR_CSS_BLOCK = re.compile(
    r"(?:"
    r"[ \t]*\.viator-[^{]+\{[^}]*\}[ \t]*\n"
    r"|"
    r"[ \t]*@media\([^{]+\{[ \t]*\.viator[^}]+\}[ \t]*\}[ \t]*\n"
    r")+"
)


def remove_from_leaf(path: Path, dry_run: bool) -> tuple[bool, str]:
    """Remove the Viator HTML block + any inline Viator CSS from one leaf."""
    txt = path.read_text(errors="replace")
    if "viator" not in txt.lower():
        return False, "no viator reference"

    new, html_n = VIATOR_HTML_BLOCK.subn("", txt)
    new, css_n = VIATOR_CSS_BLOCK.subn("", new)

    if new == txt:
        return False, "regex did not match — investigate"

    if "viator" in new.lower():
        leftover = re.findall(r".{0,40}viator.{0,40}", new, re.IGNORECASE)[:3]
        return False, f"LEFTOVER refs after removal: {leftover}"

    delta = len(txt) - len(new)
    if not dry_run:
        path.write_text(new)
    return True, f"removed {delta} bytes (html={html_n}, css={css_n})"


def remove_from_css(path: Path, dry_run: bool) -> tuple[bool, str]:
    """Remove the .viator-* rules block from compare-shared.css."""
    txt = path.read_text(errors="replace")
    if "viator" not in txt.lower():
        return False, "no viator reference"

    new = VIATOR_CSS_BLOCK.sub("", txt)
    if new == txt:
        return False, "CSS regex did not match — investigate"
    if "viator" in new.lower():
        leftover = re.findall(r".{0,40}viator.{0,40}", new, re.IGNORECASE)[:5]
        return False, f"LEFTOVER CSS refs after removal: {leftover}"

    delta = len(txt) - len(new)
    if not dry_run:
        path.write_text(new)
    return True, f"removed {delta} bytes"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="don't write, just report")
    args = ap.parse_args()

    leaves = sorted(p for p in COMPARE.glob("*/index.html") if p.parent.name not in {
        "asia", "australia", "bali", "cities", "colombia", "countries", "croatia",
        "culture", "egypt", "europe", "global-mixed", "greece", "hawaii", "iceland",
        "islands", "italy", "japan", "latin-america", "luxury", "maldives", "mexico",
        "middle-east-africa", "morocco", "nature", "new-zealand", "north-america",
        "oceania", "portugal", "spain", "taiwan", "thailand", "trip-style-guides",
        "vietnam",
    })

    changed = 0
    skipped = 0
    failed = []

    for leaf in leaves:
        ok, msg = remove_from_leaf(leaf, args.dry_run)
        if ok:
            changed += 1
        elif msg == "no viator reference":
            skipped += 1
        else:
            failed.append((leaf.parent.name, msg))

    print(f"Leaves processed: {len(leaves)}")
    print(f"  changed:  {changed}")
    print(f"  skipped:  {skipped} (no viator)")
    print(f"  failed:   {len(failed)}")
    for slug, msg in failed[:20]:
        print(f"    {slug}: {msg}")

    print()
    css_ok, css_msg = remove_from_css(SHARED_CSS, args.dry_run)
    print(f"CSS: {'CHANGED' if css_ok else 'no-op'} — {css_msg}")

    if args.dry_run:
        print("\n[dry-run — no files modified]")
        return 0
    if failed:
        print("\n[ERROR] failed pages exist — fix and rerun")
        return 1
    if not css_ok:
        print("\n[ERROR] CSS not removed cleanly — fix and rerun")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
