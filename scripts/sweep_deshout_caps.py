#!/usr/bin/env python3
"""De-shout ALL-CAPS shouting words in rendered scam-page prose.

Editorial lint rule 8 limits ALL-CAPS tokens in `story` fields, but the rule
is only enforced on research JSON. Rendered HTML still carries a long tail of
shouted bullets ("NEVER leave passport as deposit", "IGNORE every Grab
sign-holder", "the legitimate MDAC is absolutely FREE", "it is 100% a scam",
"Do NOT stop") that escaped editing at source.

This sweep rewrites a short whitelist of shouting words to title-case, only
when the token is (a) fully uppercase, (b) a word we've explicitly listed,
and (c) outside `<script>`, `<style>`, and `<title>` blocks (JSON-LD and
page metadata).

Substitutions (applied in order; case-sensitive match on the shouted form):
  1. "DO NOT" → "Don't"  (two-word; handled first to avoid orphan "NOT")
  2. "NEVER"  → "Don't"  if followed by a lowercase verb token
             → "Never" otherwise
  3. "ALWAYS" → "Always"
  4. "IGNORE" → "Ignore"
  5. "REFUSE" → "Refuse"
  6. "AVOID"  → "Avoid"
  7. "STOP"   → "Stop"
  8. "WARNING"→ "Warning"
  9. "FREE"   → "free"  (plain adjective; not in lint's ALLCAPS_ALLOWLIST)

The allowlist from scripts/lint_scam_content.py (MDAC, KLIA, LRT, USD, etc.)
isn't replicated here on purpose — we only rewrite the nine explicit English
word-forms above, which never overlap with that allowlist's acronyms.

Numeric emphasis ("100%") is left as-is.

Idempotent: a rerun on an already-swept file produces zero changes.

Usage:
    python3 scripts/sweep_deshout_caps.py --dry-run
    python3 scripts/sweep_deshout_caps.py
    python3 scripts/sweep_deshout_caps.py --dry-run --limit 5
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scam_sweep_common import collect_scam_targets

REPO = Path(__file__).resolve().parents[1]

# Regions we NEVER touch. Captures the entire tag including content.
_SKIP_REGION = re.compile(
    r"<(script|style|title)\b[^>]*>.*?</\1>",
    re.DOTALL | re.IGNORECASE,
)


# ---- Substitution patterns ----

# "DO NOT" → "Don't" — handled first to avoid leaving an orphan "NOT".
_DO_NOT = re.compile(r"\bDO\s+NOT\b")

# "NEVER" followed by whitespace + lowercase verb → "Don't <verb>"
_NEVER_VERB = re.compile(r"\bNEVER(?=\s+[a-z]{2,})")

# Single-word substitutions. Word-boundary anchored; case-sensitive (uppercase
# tokens only). Each one is a plain English word, not a potential acronym.
_SINGLE_WORD = [
    (re.compile(r"\bNEVER\b"), "Never"),
    (re.compile(r"\bALWAYS\b"), "Always"),
    (re.compile(r"\bIGNORE\b"), "Ignore"),
    (re.compile(r"\bREFUSE\b"), "Refuse"),
    (re.compile(r"\bAVOID\b"), "Avoid"),
    (re.compile(r"\bSTOP\b"), "Stop"),
    (re.compile(r"\bWARNING\b"), "Warning"),
    (re.compile(r"\bFREE\b"), "free"),
]


def _deshout_segment(text: str) -> tuple[str, int]:
    """Apply substitutions to a prose segment (no script/style/title tags)."""
    total = 0
    text, n = _DO_NOT.subn("Don't", text)
    total += n
    text, n = _NEVER_VERB.subn("Don't", text)
    total += n
    for pat, rep in _SINGLE_WORD:
        text, n = pat.subn(rep, text)
        total += n
    return text, total


def _fix_html(text: str) -> tuple[str, int]:
    """De-shout in every region outside <script>/<style>/<title>.

    Splits the source on skip-region boundaries, runs the substitution on
    each non-skip chunk, and reassembles. Preserves source formatting
    byte-for-byte outside the substitution sites.
    """
    parts: list[str] = []
    total = 0
    pos = 0
    for m in _SKIP_REGION.finditer(text):
        # Prose before the skip region
        prose = text[pos : m.start()]
        new_prose, n = _deshout_segment(prose)
        parts.append(new_prose)
        total += n
        # The skip region itself: verbatim
        parts.append(m.group(0))
        pos = m.end()
    # Tail after the last skip region
    tail = text[pos:]
    new_tail, n = _deshout_segment(tail)
    parts.append(new_tail)
    total += n
    return "".join(parts), total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, help="Stop after N files (for testing)")
    args = ap.parse_args()

    targets = collect_scam_targets(
        city_pages=True,
        country_hubs=True,
        master_hub=True,
    )
    if args.limit:
        targets = targets[: args.limit]

    total_replacements = 0
    files_changed = 0
    for path in targets:
        if not path.exists():
            continue
        original = path.read_text()
        fixed, n = _fix_html(original)
        if n > 0 and fixed != original:
            files_changed += 1
            total_replacements += n
            label = str(path.relative_to(REPO))
            print(f"  {label:60} — {n} replacements")
            if not args.dry_run:
                path.write_text(fixed)

    action = "would replace" if args.dry_run else "replaced"
    print(f"\n{action} {total_replacements} shouting tokens across {files_changed} files")


if __name__ == "__main__":
    main()
