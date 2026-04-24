#!/usr/bin/env python3
"""Strip orphan editorial-tag phrases left behind by the Reddit-shard sanitizer.

_sanitize_reddit_shards (in scripts/clean_us_reddit_shards.py) strips the
citation body `r/<sub> '<title>' (comments/xxx, YEAR)` but sometimes misses
the trailing editorial tag ("is the community baseline", "are the 2025
anchors", "documents the named pattern"). Those orphans land in rendered
HTML across ~100 pages — visible as subject-less sentence fragments.

This script removes them with 4 targeted regex passes and collapses the
whitespace left behind. Operates on scams/<slug>/index.html; skips country
hubs and the master hub.

Usage:
    python3 scripts/strip_orphan_phrases.py --dry-run
    python3 scripts/strip_orphan_phrases.py
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCAMS = REPO / "scams"

# The signal-words that identify orphan tags. Legitimate prose can use any
# of these individually, so we only strip when the full pattern (verb +
# determiner + qualifier + signal-noun) appears at a sentence or block edge.
_VERBS = r"(?:is|are|establishes?|established|documents?|documented|captures?|captured|tracks?|tracked|gives?|gave|confirms?|confirmed)"
_DETERMINER = r"(?:the\s+|a\s+|an\s+|)"
_QUALIFIERS = r"(?:(?:CANONICAL|canonical|\d{4}|community|baseline|recurring|first[-\s]person|named|cross-post|second|original|viral|updated|NAMED|broader)\s+){0,4}"
_SIGNALS = r"(?:anchor|baseline|reference|marker|pattern|update|thread|post|warning|context|incident|report)s?"
_TAIL_CLAUSE = (
    # Optional modifier noun after signal ("anchor threads", "baseline posts")
    r"(?:\s+(?:threads?|posts?|warnings?|incidents?|reports?))?"
    # Optional: "X-ing clause" — participles/prepositions leading tail content.
    # Bounded by sentence-end chars so we don't eat across the next sentence.
    # Also bounded by `"`, `,`, `}`, `]` so we don't eat JSON structure chars.
    r"(?:\s+(?:documenting|confirming|establishing|capturing|covering|discussing|flagging|naming|describing|warning|reviewing|with|for|on|where|about|from|explaining)\s+[^.?!<>\n\"},\]]{0,200})?"
    # Optional: em-dash or colon introducing short clause. Same bounds.
    r"(?:\s*(?:[—\-]|:)\s*[^.?!<>\n\"},\]]{0,200})?"
    # Optional: parenthetical or quoted anecdote — self-bounded by brackets/quotes.
    r"(?:\s*(?:\([^)]{0,250}\)|'[^'\n<>]{0,250}'|\"[^\"\n<>]{0,250}\"))?"
)

# Pass 1: orphan after sentence boundary — most common shape
_AFTER_SENTENCE = re.compile(
    rf"""(?<=[.!?])\s+{_VERBS}\s+{_DETERMINER}{_QUALIFIERS}{_SIGNALS}{_TAIL_CLAUSE}\s*[.?!]""",
    re.VERBOSE | re.IGNORECASE,
)

# Pass 2: orphan after HTML tag boundary (> or " for JSON values) —
# picks up orphans at the start of <p>/<li>/faq-a content
_AFTER_TAG = re.compile(
    rf"""(?<=[>"])\s+{_VERBS}\s+{_DETERMINER}{_QUALIFIERS}{_SIGNALS}{_TAIL_CLAUSE}\s*[.?!]""",
    re.VERBOSE | re.IGNORECASE,
)

# Pass 3: orphan after semicolon/comma chain — ". X; is the 2025 anchor;"
_AFTER_CHAIN = re.compile(
    rf"""(?<=[;,])\s+{_VERBS}\s+{_DETERMINER}{_QUALIFIERS}{_SIGNALS}{_TAIL_CLAUSE}\s*(?=[.?!;,])""",
    re.VERBOSE | re.IGNORECASE,
)

# Pass 4: orphan concatenated directly to prior prose (sanitizer stripped citation
# mid-sentence, leaving orphan glued to previous word). Only strip when the
# orphan has ≥ 1 qualifier (tight — prevents legit "is the baseline" from firing).
_TIGHT_QUALIFIERS = r"(?:(?:CANONICAL|canonical|\d{4}|community|baseline|recurring|first[-\s]person|named|NAMED|cross-post|viral)\s+){1,4}"
_MID_STRING = re.compile(
    rf"""\s+{_VERBS}\s+{_DETERMINER}{_TIGHT_QUALIFIERS}{_SIGNALS}{_TAIL_CLAUSE}\s*(?=[.?!;,:<>]|$)""",
    re.VERBOSE | re.MULTILINE | re.IGNORECASE,
)

# Pass 4: lines that END with an orphan phrase followed by another orphan
# ("is the CANONICAL 2025 anchor. is a second 2025 first-person anchor.") —
# Pass 1 catches them iteratively if run multiple times, but one more round
# handles the chained case cleanly.
def _strip_orphans(text: str) -> tuple[str, int]:
    total_stripped = 0
    for pattern in (_AFTER_SENTENCE, _AFTER_TAG, _AFTER_CHAIN, _MID_STRING):
        for _ in range(5):  # iterate until no more matches (chained orphans)
            new_text, n = pattern.subn("", text)
            if n == 0:
                break
            text = new_text
            total_stripped += n
    # Conservative whitespace cleanup: only collapse the specific artifacts
    # that orphan removal creates (pre-punctuation space, doubled sentence
    # boundaries). Do NOT collapse general whitespace — that would destroy
    # HTML indentation.
    text = re.sub(r" +([.?!,;])", r"\1", text)        # "word . " → "word. "
    text = re.sub(r"([.?!]) +(?=[.?!])", r"\1", text)  # ". ." → "."
    return text, total_stripped


def _collect_targets() -> list[Path]:
    city_pages = [
        p / "index.html"
        for p in sorted(SCAMS.iterdir())
        if p.is_dir() and p.name != "country" and (p / "index.html").exists()
    ]
    research = sorted((SCAMS / "research").glob("*.json"))
    api_city = sorted((REPO / "api" / "v1" / "scams").glob("*.json"))
    api_country = sorted((REPO / "api" / "v1" / "countries").glob("*/scams.json"))
    api_catalog = [REPO / "api" / "v1" / "catalog" / "scams.json"]
    return city_pages + research + api_city + api_country + [p for p in api_catalog if p.exists()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, help="Stop after N files (for testing)")
    args = ap.parse_args()

    targets = _collect_targets()
    if args.limit:
        targets = targets[: args.limit]

    total_stripped = 0
    files_changed = 0
    for path in targets:
        original = path.read_text()
        fixed, n = _strip_orphans(original)
        if n > 0 and fixed != original:
            files_changed += 1
            total_stripped += n
            label = str(path.relative_to(REPO))
            print(f"  {label:55} — {n} orphans stripped")
            if not args.dry_run:
                path.write_text(fixed)

    action = "would strip" if args.dry_run else "stripped"
    print(f"\n{action} {total_stripped} orphans across {files_changed} files")


if __name__ == "__main__":
    main()
