#!/usr/bin/env python3
"""Sweep currency-space violations across the scam-page corpus.

Editorial lint rule 3 forbids a space between a currency symbol/code and the
number that follows it ("$ 45", "£ 20", "RM 50"). Violations are widespread
across shipped city pages, country hubs, the master hub, research JSON, and
the API v1 scam/country/catalog JSON.

Two in-scope substitutions (applied in order):
  1. Currency symbol + whitespace + digit  →  symbol + digit
     Symbols: $ £ € ¥ R$ NT$ US$ HK$ S$
  2. 3-letter currency code + whitespace + digit  →  code + digit
     Codes: RM THB JPY EUR USD NTD ARS BRL INR

No exclusion for <script>/<style>/JSON-LD: the style guide's intent is that a
currency-space is ALWAYS wrong, even inside structured data. The substitutions
are narrow enough (symbol/code immediately before a digit) that they do not
trigger inside attribute values or URLs.

Usage:
    python3 scripts/sweep_currency_spaces.py --dry-run
    python3 scripts/sweep_currency_spaces.py
    python3 scripts/sweep_currency_spaces.py --dry-run --limit 5
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scam_sweep_common import collect_scam_targets

REPO = Path(__file__).resolve().parents[1]

# Pass 1: symbol + whitespace + (?=digit).  Longer prefixes (R$, NT$, US$, HK$,
# S$) are matched implicitly because they end with $ — the $ alone is enough to
# anchor the substitution; the prefix letters stay where they are.
_SYMBOL_SPACE = re.compile(r"(\$|£|€|¥)\s+(?=\d)")

# Pass 2: 3-letter currency code + whitespace + (?=digit).
_CODE_SPACE = re.compile(r"\b(RM|THB|JPY|EUR|USD|NTD|ARS|BRL|INR)\s+(?=\d)")


def _fix(text: str) -> tuple[str, int]:
    total = 0
    text, n = _SYMBOL_SPACE.subn(lambda m: m.group(1), text)
    total += n
    text, n = _CODE_SPACE.subn(lambda m: m.group(1), text)
    total += n
    return text, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, help="Stop after N files (for testing)")
    args = ap.parse_args()

    targets = collect_scam_targets(
        city_pages=True,
        country_hubs=True,
        master_hub=True,
        research_json=True,
        api_json=True,
    )
    if args.limit:
        targets = targets[: args.limit]

    total_replacements = 0
    files_changed = 0
    for path in targets:
        if not path.exists():
            continue
        original = path.read_text()
        fixed, n = _fix(original)
        if n > 0 and fixed != original:
            files_changed += 1
            total_replacements += n
            label = str(path.relative_to(REPO))
            print(f"  {label:60} — {n} replacements")
            if not args.dry_run:
                path.write_text(fixed)

    action = "would replace" if args.dry_run else "replaced"
    print(f"\n{action} {total_replacements} currency-space violations across {files_changed} files")


if __name__ == "__main__":
    main()
