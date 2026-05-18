#!/usr/bin/env python3
"""
Remove the redundant inline `<nav class="breadcrumb">` / `<div class="breadcrumb">`
block from every page where it duplicates the JS-injected `.page-breadcrumbs`
nav (rendered client-side by assets/shared-shell.js from BreadcrumbList JSON-LD).

Why: shared-shell.js always injects a `<nav class="page-breadcrumbs">` from the
schema. The inline copy was added by PR #1558 (compare) and earlier templates
(scams/health/countries) before the JS-injection was the canonical path. This
produced two breadcrumbs in the DOM on ~1,977 pages — most visibly on compare,
where the inline `<ol>` rendered as a numbered list because compare pages don't
load compare-shared.css.

Usage:
    python3 scripts/remove_inline_breadcrumb.py [--dry-run] [--only SECTION]

Sections: compare, scams, health, countries (default: all 4).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Matches exactly one outer <nav class="breadcrumb">...</nav> OR
# <div class="breadcrumb">...</div> wrapper. Non-greedy so it stops at the
# first matching closing tag. We anchor on `class="breadcrumb"` (literal,
# closing-quote-bounded) so `class="breadcrumb-current"` etc. won't match.
INLINE_BREADCRUMB_RE = re.compile(
    r'<(nav|div)\b[^>]*\bclass="breadcrumb"[^>]*>.*?</\1>\s*\n?',
    re.DOTALL,
)

SECTIONS = ("compare", "scams", "health", "countries")


def strip_one(html: str) -> tuple[str, int]:
    """Strip up to one inline breadcrumb wrapper. Returns (new_html, n_removed)."""
    matches = INLINE_BREADCRUMB_RE.findall(html)
    if not matches:
        return html, 0
    if len(matches) > 1:
        raise RuntimeError(
            f"refusing to edit: found {len(matches)} inline .breadcrumb wrappers "
            "(pre-edit audit asserted there is at most one per page)"
        )
    return INLINE_BREADCRUMB_RE.sub("", html, count=1), 1


def process(sections: list[str], dry_run: bool) -> int:
    total_changed = 0
    total_skipped = 0
    for section in sections:
        root = REPO_ROOT / section
        if not root.is_dir():
            print(f"skip: {section}/ does not exist", file=sys.stderr)
            continue
        changed = 0
        skipped = 0
        for path in sorted(root.rglob("index.html")):
            try:
                html = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                print(f"warn: cannot decode {path}", file=sys.stderr)
                continue
            new_html, n = strip_one(html)
            if n == 0:
                skipped += 1
                continue
            if not dry_run:
                path.write_text(new_html, encoding="utf-8")
            changed += 1
        verb = "would strip" if dry_run else "stripped"
        print(f"{section}/: {verb} {changed} pages, {skipped} had no inline breadcrumb")
        total_changed += changed
        total_skipped += skipped
    print(f"\nTOTAL: {total_changed} pages changed, {total_skipped} skipped (no inline breadcrumb)")
    return total_changed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="report only, do not write")
    ap.add_argument("--only", choices=SECTIONS, help="restrict to one section")
    args = ap.parse_args()
    sections = [args.only] if args.only else list(SECTIONS)
    process(sections, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
