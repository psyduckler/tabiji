#!/usr/bin/env python3
"""Replace 'community forums/threads/reports' placeholders with traveler-anchored prose.

The 2025 Reddit-shard sanitizer stripped citation bodies and left dangling
placeholders of the form 'community forums', 'community threads', and
'community reports' where the original URL + quote used to live. The lint
doesn't flag them (they're grammatical), but they read as a sanitizer leak
rather than editorial prose. Auditor counted 38 in sampled pages; full-corpus
grep turned up 2.2k+ across ~330 files.

Substitutions (applied in order, case-sensitive on the first letter; the
trailing noun is lowercased uniformly):

  # Three-token compounds first — they must fire before the generic two-
  # token patterns or we'd leave an orphan 'post'/'thread'/'anchor' behind.
  "community forums post"   → "traveler report"
  "community forums thread" → "traveler thread"
  "community forums anchor" → "traveler-account anchor"

  # Two-token leak patterns
  "community forums"  → "traveler reports"  (most common)
  "community threads" → "traveler threads"
  "community reports" → "traveler reports"
  "community report"  → "traveler report"
  "community thread"  → "traveler thread"

  # Adjectival compounds the sanitizer produced
  "community-warning anchor" → "community-warning post"
  "community ethics anchor"  → "community ethics post"

Intentionally PRESERVED (community used adjectivally, which reads as
editorial language, not sanitizer leak):
  "community baseline", "community consensus", "community-vetted",
  "community-recommended"

After the targeted substitutions, one cleanup pass fixes degenerate phrases
that result from the "community forums" → "traveler reports" swap:
  "is a traveler reports"   → "is documented in traveler reports"
  "are the traveler reports" → "are traveler reports"

Targets: rendered HTML (city pages, country hubs, master hub), research
JSON batches, and API v1 scam/country/catalog JSON.

Idempotent: the substitutions remove the dangling forms, so a rerun is a
no-op.

Usage:
    python3 scripts/sweep_community_placeholders.py --dry-run
    python3 scripts/sweep_community_placeholders.py
    python3 scripts/sweep_community_placeholders.py --dry-run --limit 5
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scam_sweep_common import collect_scam_targets

REPO = Path(__file__).resolve().parents[1]


def _case_preserve(orig_first: str, replacement: str) -> str:
    """If orig_first is uppercase, capitalize first letter of replacement."""
    if orig_first.isupper():
        return replacement[0].upper() + replacement[1:]
    return replacement


# Ordered list of (compiled pattern, base replacement). The pattern's first
# capture group is the first character of the matched phrase — used to
# preserve upper/lower case through the substitution.

# Three-token compounds first (must fire before two-token patterns).
# Pattern: [cC]ommunity\s+forums?\s+post  — singular or plural "forum(s)"
_3TOK = [
    (re.compile(r"([cC])ommunity\s+forums?\s+post"), "traveler report"),
    (re.compile(r"([cC])ommunity\s+forums?\s+thread"), "traveler thread"),
    (re.compile(r"([cC])ommunity\s+forums?\s+anchor"), "traveler-account anchor"),
]

# Adjectival compounds with "anchor" — swap "anchor" → "post"
_ANCHOR_COMPOUND = [
    (re.compile(r"([cC])ommunity-warning\s+anchor"), "community-warning post"),
    (re.compile(r"([cC])ommunity\s+ethics\s+anchor"), "community ethics post"),
]

# Two-token leak patterns
_2TOK = [
    (re.compile(r"([cC])ommunity\s+forums\b"), "traveler reports"),
    (re.compile(r"([cC])ommunity\s+forum\b"), "traveler reports"),
    (re.compile(r"([cC])ommunity\s+threads\b"), "traveler threads"),
    (re.compile(r"([cC])ommunity\s+reports\b"), "traveler reports"),
    (re.compile(r"([cC])ommunity\s+report\b"), "traveler report"),
    (re.compile(r"([cC])ommunity\s+thread\b"), "traveler thread"),
]

# Cleanup pass for degenerate phrases after the swap
_CLEANUP = [
    (re.compile(r"\bis a traveler reports\b"), "is documented in traveler reports"),
    (re.compile(r"\bare the traveler reports\b"), "are traveler reports"),
    # Handle the case-preserved variants
    (re.compile(r"\bIs a traveler reports\b"), "Is documented in traveler reports"),
    (re.compile(r"\bAre the traveler reports\b"), "Are traveler reports"),
]


def _fix(text: str) -> tuple[str, int]:
    total = 0

    # Pass 1: three-token compounds
    for pat, base in _3TOK:
        def _sub(m, _b=base):
            return _case_preserve(m.group(1), _b)
        text, n = pat.subn(_sub, text)
        total += n

    # Pass 2: adjectival "anchor → post" compounds
    for pat, base in _ANCHOR_COMPOUND:
        def _sub(m, _b=base):
            return _case_preserve(m.group(1), _b)
        text, n = pat.subn(_sub, text)
        total += n

    # Pass 3: two-token leak patterns
    for pat, base in _2TOK:
        def _sub(m, _b=base):
            return _case_preserve(m.group(1), _b)
        text, n = pat.subn(_sub, text)
        total += n

    # Pass 4: cleanup
    for pat, rep in _CLEANUP:
        text, n = pat.subn(rep, text)
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
    print(f"\n{action} {total_replacements} community-placeholder leaks across {files_changed} files")


if __name__ == "__main__":
    main()
