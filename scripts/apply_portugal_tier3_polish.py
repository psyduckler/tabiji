#!/usr/bin/env python3
"""Tier 3 polish for Portugal scam pages — denuncia → denúncia + i-pronoun fixes.

Two surgical substitutions applied across all 10 Portugal cities (HTML + JSON):

1. denuncia → denúncia (Portuguese word for police report; the diacritic is
   the canonical Portuguese spelling). Word-boundary case-sensitive: also
   handles "Denuncia" → "Denúncia" if any sentence-start instances exist.

2. (i didn't order, i don't pay) → (I didn't order, I don't pay) — the
   English gloss for "não pedi, não pago" had lowercase "i" pronouns in
   3 paragraphs (sintra/funchal/albufeira), while the same paragraphs'
   bolded summaries already used "I". Fixes the within-paragraph mismatch.

Both substitutions are unambiguous in any context — denuncia has no other
plausible meaning in English, and the parenthetical English gloss only
appears in the não-pedi-não-pago context.

Usage:
    python3 scripts/apply_portugal_tier3_polish.py --dry-run    # preview
    python3 scripts/apply_portugal_tier3_polish.py              # apply
"""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


def repo_root() -> Path:
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return Path(out)


REPO = repo_root()
CITIES = [
    "lisbon", "porto", "faro", "sintra", "funchal",
    "albufeira", "lagos-portugal", "cascais", "coimbra", "nazare",
]

SUBSTITUTIONS = [
    # (pattern, replacement, description)
    (r'\bdenuncia\b', 'denúncia', 'denuncia → denúncia'),
    (r'\bDenuncia\b', 'Denúncia', 'Denuncia → Denúncia'),
    (
        r"\(i didn't order, i don't pay\)",
        "(I didn't order, I don't pay)",
        "(i didn't order, i don't pay) → (I didn't order, I don't pay)",
    ),
]


def process_file(path: Path, apply: bool) -> dict[str, int]:
    """Returns dict of substitution_description -> count."""
    if not path.exists():
        return {}
    content = path.read_text()
    new_content = content
    counts: dict[str, int] = {}
    for pattern, replacement, desc in SUBSTITUTIONS:
        new_content, n = re.subn(pattern, replacement, new_content)
        if n > 0:
            counts[desc] = n
    if counts and apply:
        path.write_text(new_content)
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    grand_total = 0
    print("== HTML files ==")
    for city in CITIES:
        path = REPO / "scams" / city / "index.html"
        counts = process_file(path, apply=not args.dry_run)
        if counts:
            total = sum(counts.values())
            grand_total += total
            label = "DRY-RUN" if args.dry_run else "APPLIED"
            print(f"  {label}: scams/{city}/index.html: {total} substitutions")
            for desc, n in counts.items():
                print(f"    {desc}: {n}x")

    print()
    print("== api/v1 JSON files ==")
    for city in CITIES:
        path = REPO / "api" / "v1" / "scams" / f"{city}.json"
        counts = process_file(path, apply=not args.dry_run)
        if counts:
            total = sum(counts.values())
            grand_total += total
            label = "DRY-RUN" if args.dry_run else "APPLIED"
            print(f"  {label}: api/v1/scams/{city}.json: {total} substitutions")
            for desc, n in counts.items():
                print(f"    {desc}: {n}x")

    print()
    print(f"GRAND TOTAL: {grand_total} substitutions across {len(CITIES)} cities (HTML + JSON)")


if __name__ == "__main__":
    main()
