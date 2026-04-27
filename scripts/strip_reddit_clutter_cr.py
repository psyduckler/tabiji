#!/usr/bin/env python3
"""Strip Reddit clutter from Costa Rica city scam pages.

Removes:
  - Parenthetical citations with u/handles: (2024, u/Foo, 117 upvotes)
  - Parenthetical thread refs: (2024, thread 1d20xai)
  - Bare upvote counts: (146 upvotes)
  - Bare u/handle attributions in various narrative positions
  - "per u/handle" / "from u/handle" / "praised by u/handle" patterns

Preserves:
  - r/<subreddit> citations
  - URLs / hrefs
  - Year-only parens like "(2024)" or "(2025)" used as date refs

Outputs a per-city diff summary so the human can verify damage before commit.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CITIES = [
    "jaco-costa-rica",
    "la-fortuna",
    "liberia-costa-rica",
    "manuel-antonio",
    "monteverde",
    "puerto-viejo-costa-rica",
    "san-jose-costa-rica",
    "tamarindo",
]

MONTH = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
HANDLE = r"u/[A-Za-z0-9_-]+"

# Order matters — most specific patterns first.
PATTERNS: list[tuple[re.Pattern, str]] = [
    # Parenthetical citations with u/handle (most common). Captures the leading
    # space so we don't leave a double-space behind.
    (re.compile(rf"\s?\(\s?{MONTH}?\s?\d{{4}},\s?{HANDLE}(?:,\s?\d+\s?upvotes?)?\s?\)"), ""),
    # Parenthetical thread refs.
    (re.compile(rf"\s?\(\s?{MONTH}?\s?\d{{4}},\s?thread\s+[A-Za-z0-9_-]+\s?\)"), ""),
    # Leading "(NN upvotes, ..." inside parens — keep the content, drop the upvotes prefix.
    (re.compile(r"\(\s?\d+\s?upvotes?,\s*"), "("),
    # Bare (u/handle) — no other content
    (re.compile(rf"\s?\(\s?{HANDLE}\s?\)"), ""),
    # Bare (u/handle, NN) — handle plus a number (like "(u/DrexellGames, 1)")
    (re.compile(rf"\s?\(\s?{HANDLE},\s?\d+\s?\)"), ""),
    # (u/handle quotation/attribution) — strip the whole parenthetical when the
    # content is just a quote or attribution, since the speaker is implied
    # by surrounding narrative anyway. Applies when content is in single quotes
    # or starts with ":" or a verb like "recommended".
    (re.compile(rf"\s?\(\s?{HANDLE}[\s,:]+'[^']*'\s?\)"), ""),
    (re.compile(rf"\s?\(\s?{HANDLE}\s*:[^)]*\)"), ""),
    # (u/handle <single word>) like "(u/ahh651 recommended)" → "(recommended)" then squash empty
    (re.compile(rf"\(\s?{HANDLE}\s+([A-Za-z][^)]*)\)"), r"(\1)"),
    # (u/handle, <text>) → "(<text>)"
    (re.compile(rf"\(\s?{HANDLE},\s*([^)]+)\)"), r"(\1)"),
    # Possessive u/handle's → "one traveler's" (preserves grammar)
    (re.compile(rf"\b{HANDLE}'s\b"), "one traveler's"),
    # "per u/handle" / "from u/handle" / "by u/handle" — drop entirely
    (re.compile(rf"\s+(?:per|from|by)\s+{HANDLE}"), ""),
    # "praised by u/handle" / "answered by u/handle" — already covered above,
    # but defensively handle "(praised|answered|recommended) by ..." which
    # often appeared inline.
    (re.compile(rf",?\s+(?:praised|answered|recommended|confirmed)\s+by\s+{HANDLE}"), ""),
    # "u/handle: 'quote'" → "One traveler: 'quote'"
    (re.compile(rf"(?<![A-Za-z]){HANDLE}\s*(:)"), r"One traveler\1"),
    # "u/handle in that thread" / "u/handle in the same thread"
    (re.compile(rf"\b{HANDLE}\s+in\s+(?:that|the\s+same)\s+thread\b"), "another traveler in the same thread"),
    # "u/handle had/was/got/saw/described/documented/...": replace with "one traveler"
    (re.compile(rf"\b{HANDLE}\b(?=\s+(?:had|has|was|were|got|saw|described|documented|noted|paid|reported|wrote|posted|warned|pushed|complained|confirmed|recounted|asked))"), "one traveler"),
    # "Top-voted reply from u/handle" or similar — handled by "from u/handle" above
    # Bare commas around handles: ", u/handle," or ", u/handle "
    (re.compile(rf",\s*{HANDLE}\s*,"), ","),
    (re.compile(rf",\s*{HANDLE}\b"), ""),
    # Trailing or floating " u/handle" still hanging around
    (re.compile(rf"\s+{HANDLE}\b"), ""),
    # Bare upvote counts left behind: " (146 upvotes)" or ", 146 upvotes"
    (re.compile(r"\s?\(\d+\s?upvotes?\)"), ""),
    (re.compile(r",\s?\d+\s?upvotes?"), ""),
]

# Cleanup pass — run after all the strips.
CLEANUP: list[tuple[re.Pattern, str]] = [
    # Common artifact: "(N upvotes)" left bare with empty parens
    (re.compile(r"\(\s*\)"), ""),
    # Empty parens with leading comma: ", )" → ")"
    (re.compile(r",\s*\)"), ")"),
    # Double spaces
    (re.compile(r" {2,}"), " "),
    # Space before punctuation: " ." → "." but not before "..."
    (re.compile(r"\s+([,;:!])"), r"\1"),
    # Period-period (no space) artifact like ".." that's not "..."
    (re.compile(r"(?<!\.)\.\.(?!\.)"), "."),
    # Stray "()." or "()"
    (re.compile(r"\(\)\.?"), ""),
    # Period directly followed by digit-period like ".5-hour" — KEEP, this is a real
    # typo we'll fix in proofread phase. Don't touch here.
    # ", and " at sentence start (artifact of stripping leading "u/handle, and ...")
    (re.compile(r"(?<=[.!?])\s*,\s+and\s+"), " "),
    # Empty leading citation in TLDRs like "<p class=\"scam-tldr\"> ." → strip leading space-period
    (re.compile(r'(<p class="scam-tldr">)\s*[.,;:]\s*'), r"\1"),
    # Same for empty leading parenthetical ". " in TLDR
    (re.compile(r'(<p class="scam-tldr">)\s+'), r"\1"),
]


def strip_city(city: str) -> dict:
    path = REPO / "scams" / city / "index.html"
    original = path.read_text()
    text = original

    handles_before = len(re.findall(HANDLE, text))
    upvotes_before = len(re.findall(r"\d+\s?upvotes?", text))

    for pattern, replacement in PATTERNS:
        text = pattern.sub(replacement, text)
    for pattern, replacement in CLEANUP:
        text = pattern.sub(replacement, text)

    handles_after = len(re.findall(HANDLE, text))
    upvotes_after = len(re.findall(r"\d+\s?upvotes?", text))
    bytes_before = len(original)
    bytes_after = len(text)

    path.write_text(text)
    return {
        "city": city,
        "handles_before": handles_before,
        "handles_after": handles_after,
        "upvotes_before": upvotes_before,
        "upvotes_after": upvotes_after,
        "bytes_before": bytes_before,
        "bytes_after": bytes_after,
        "bytes_saved": bytes_before - bytes_after,
    }


def main():
    print(f"{'city':<28} {'u/before':>9} {'u/after':>8} {'upv-bef':>8} {'upv-aft':>8} {'bytes_saved':>12}")
    print("-" * 80)
    for city in CITIES:
        r = strip_city(city)
        print(f"{r['city']:<28} {r['handles_before']:>9} {r['handles_after']:>8} "
              f"{r['upvotes_before']:>8} {r['upvotes_after']:>8} {r['bytes_saved']:>12}")


if __name__ == "__main__":
    main()
