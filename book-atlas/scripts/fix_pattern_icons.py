#!/usr/bin/env python3
"""Fix the pattern-icon insertions in 05-patterns.md.

The original integrate_comics.py script used a regex that didn't account
for the "The" prefix in heading text (e.g. "## 1. The Captive-Position
Lever"). Only Pattern 7 (Manufactured Reciprocity, no "The") matched.

This script:
  1. Reverts the previously-inserted icon (will be re-inserted correctly)
  2. Re-inserts all 7 icons matching the actual heading format
"""
from __future__ import annotations

import re
from pathlib import Path

MS = Path("/Users/bjh/Documents/tabiji/.claude/worktrees/eloquent-boyd-7e72e8/book-atlas/manuscript")
PATTERNS_FILE = MS / "05-patterns.md"

PATTERN_ICONS = {
    "Captive-Position Lever": "icon-captive-position-lever",
    "Authority Costume": "icon-authority-costume",
    "Sub-Market Quote": "icon-sub-market-quote",
    "Commission Detour": "icon-commission-detour",
    "Made-Up Closure": "icon-made-up-closure",
    "Brand-Mimicry Storefront": "icon-brand-mimicry-storefront",
    "Manufactured Reciprocity": "icon-manufactured-reciprocity",
}

INSERT_MARKER = "<!-- comic-insert -->"


def main():
    content = PATTERNS_FILE.read_text(encoding="utf-8")

    # 1. Strip any existing inserted icons (idempotent reset)
    # Pattern: blank line + INSERT_MARKER line + image line
    cleaned = re.sub(
        r"\n+" + re.escape(INSERT_MARKER) + r"\n!\[.*?\]\(\.\./build/images/icon-[^)]+\)\{[^}]*\}",
        "",
        content,
    )

    # 2. Insert icon after each "## N. ..." heading
    lines = cleaned.split("\n")
    new_lines: list[str] = []
    inserted = 0
    for line in lines:
        new_lines.append(line)
        # Match: "## 1. The Captive-Position Lever" or "## 7. Manufactured Reciprocity"
        m = re.match(r"^## \d+\.\s+(.+?)\s*$", line)
        if not m:
            continue
        name = m.group(1).strip()
        # Strip leading "The " for matching
        key = name[4:] if name.lower().startswith("the ") else name
        if key not in PATTERN_ICONS:
            continue
        slug = PATTERN_ICONS[key]
        rel_path = f"../build/images/{slug}.jpg"
        new_lines.append("")
        new_lines.append(f"{INSERT_MARKER}")
        new_lines.append(
            f"![{key} pattern icon]({rel_path}){{ width=40% }}"
        )
        inserted += 1

    PATTERNS_FILE.write_text("\n".join(new_lines), encoding="utf-8")
    print(f"Inserted {inserted} pattern icons in {PATTERNS_FILE.name}")


if __name__ == "__main__":
    main()
