#!/usr/bin/env python3
"""Add aria-label + scope="col" to all 1,903 comparison-tables on /compare/
leaf pages. Closes audit P1 #36 / #37 (WCAG H39 + H63).

Five table patterns in the corpus, all need both fixes:
  1. <table class="comparison-table">  — 823 (side-by-side destination)
  2. <table class="cost-table">         — 433 (cost breakdown)
  3. <table style=...font-size:.9rem;>  — 382 (cost-breakdown variant)
  4. <table style=...min-width:520px;>  — 227 (weather/monthly)
  5. <table>                            — 38  (bare comparison)

Transformations:
  - Wrap with aria-label derived from header content. We sniff the first
    <th> text to pick a label:
      "Category"/"Aspect" → "Destination comparison"
      "Expense"           → "Daily costs by category"
      "Month"             → "Monthly weather and seasonality"
      else                → "Comparison data"
  - Add scope="col" to every <th> in <thead><tr>.

Idempotent: re-running on a fixed file is a no-op.

Usage:
  python3 scripts/fix_table_a11y.py            # apply
  python3 scripts/fix_table_a11y.py --dry-run  # report only
"""
from __future__ import annotations

import argparse
import re
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


def label_for_table(table_html: str) -> str:
    """Pick an aria-label based on the first <th> text."""
    m = re.search(r"<th[^>]*>([^<]+?)</th>", table_html)
    if not m:
        return "Comparison data"
    first_th = m.group(1).strip().lower()
    if first_th in {"category", "aspect"}:
        return "Destination comparison"
    if first_th == "expense":
        return "Daily costs by category"
    if first_th == "month":
        return "Monthly weather and seasonality"
    return "Comparison data"


# Match a complete <table>…</table>. Greedy-ish: stop at first </table>.
TABLE_RE = re.compile(r"<table\b([^>]*)>(.*?)</table>", re.DOTALL)
# Match a <th> inside <thead> (we only add scope="col" to thead headers).
THEAD_TH_RE = re.compile(
    r"(<thead[^>]*>.*?</thead>)", re.DOTALL
)


def add_scope_to_thead(thead_html: str) -> str:
    """Add scope="col" to every <th> inside <thead> that lacks it."""
    def add(m: re.Match) -> str:
        attrs = m.group(1)
        if "scope=" in attrs:
            return m.group(0)
        return f"<th{attrs} scope=\"col\">"
    return re.sub(r"<th(\s[^>]*|)>", add, thead_html)


def fix_table(table_match: re.Match) -> str:
    full_open_attrs = table_match.group(1)
    body = table_match.group(2)

    # Skip if aria-label or aria-labelledby or caption already present
    has_aria = "aria-label" in full_open_attrs or "<caption" in body
    has_scope = "scope=" in body

    if has_aria and has_scope:
        return table_match.group(0)

    new_open_attrs = full_open_attrs
    if not has_aria:
        label = label_for_table(table_match.group(0))
        new_open_attrs = f'{full_open_attrs} aria-label="{label}"'

    new_body = body
    if not has_scope:
        new_body = THEAD_TH_RE.sub(lambda m: add_scope_to_thead(m.group(1)), body)

    return f"<table{new_open_attrs}>{new_body}</table>"


def fix_leaf(path: Path, dry_run: bool) -> tuple[int, int]:
    """Fix tables in one leaf. Returns (tables_processed, tables_changed)."""
    txt = path.read_text(errors="replace")
    if "<table" not in txt:
        return 0, 0

    processed = 0
    changed = 0

    def replace(m: re.Match) -> str:
        nonlocal processed, changed
        processed += 1
        new = fix_table(m)
        if new != m.group(0):
            changed += 1
        return new

    new_txt = TABLE_RE.sub(replace, txt)
    if new_txt != txt and not dry_run:
        path.write_text(new_txt)
    return processed, changed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    leaves = [p for p in COMPARE.glob("*/index.html") if p.parent.name not in HUBS]
    total_processed = 0
    total_changed = 0
    leaves_touched = 0

    for leaf in sorted(leaves):
        processed, changed = fix_leaf(leaf, args.dry_run)
        total_processed += processed
        total_changed += changed
        if changed:
            leaves_touched += 1

    print(f"Leaves processed:        {len(leaves)}")
    print(f"Leaves touched:          {leaves_touched}")
    print(f"Tables processed:        {total_processed}")
    print(f"Tables changed:          {total_changed}")
    if args.dry_run:
        print("\n[dry-run — no files modified]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
