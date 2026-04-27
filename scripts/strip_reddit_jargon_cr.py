#!/usr/bin/env python3
"""Second-pass scrub of Reddit jargon (OP, U/handle, (N pts)) across all 8 CR pages.

The first strip pass (strip_reddit_clutter_cr.py) caught u/handles and upvote
counts but left behind: bare "OP", possessive "OP's", capital-U "U/handle"
sentence-starters, and "(N pts)" / "(N points)" comment-rank fragments.
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

PATTERNS: list[tuple[re.Pattern, str]] = [
    # "U/Handle" sentence-start (capitalized) — replace with "One traveler"
    (re.compile(r"\bU/[A-Za-z0-9_-]+"), "One traveler"),
    # "(N pts)" / "(N points)" — strip
    (re.compile(r"\s?\(\d+\s?(?:pts?|points?)\)\s?:?\s?"), " "),
    # Possessive "OP's" → "the traveler's"
    (re.compile(r"\bOP's\b"), "the traveler's"),
    # "the OP" → "the traveler"
    (re.compile(r"\bthe\s+OP\b"), "the traveler"),
    # "OP" at sentence-start (after period+space, paragraph open, em-dash, etc.) → "One traveler"
    # Use a lookbehind for sentence-start positions
    (re.compile(r"(?<=[.!?:>—]\s)OP\b"), "One traveler"),
    (re.compile(r"(?<=<p class=\"scam-story-body\">)OP\b"), "One traveler"),
    # Bare "OP " mid-sentence → "the traveler"
    (re.compile(r"\bOP\b(?=\s)"), "the traveler"),
]

# Cleanup pass.
CLEANUP: list[tuple[re.Pattern, str]] = [
    (re.compile(r" {2,}"), " "),
    (re.compile(r"\s+([,;:])"), r"\1"),
]


def scrub(city: str) -> dict:
    path = REPO / "scams" / city / "index.html"
    original = path.read_text()
    text = original
    for pattern, replacement in PATTERNS:
        text = pattern.sub(replacement, text)
    for pattern, replacement in CLEANUP:
        text = pattern.sub(replacement, text)
    path.write_text(text)
    op_after = len(re.findall(r"\bOP\b", text))
    u_after = len(re.findall(r"U/[A-Za-z]", text))
    pts_after = len(re.findall(r"\(\d+\s?(?:pts?|points?)\)", text))
    return {
        "city": city,
        "OP_after": op_after,
        "U_after": u_after,
        "pts_after": pts_after,
        "bytes_saved": len(original) - len(text),
    }


def main():
    print(f"{'city':<28} {'OP':>6} {'U/':>6} {'pts':>6} {'saved':>7}")
    print("-" * 60)
    for city in CITIES:
        r = scrub(city)
        print(f"{r['city']:<28} {r['OP_after']:>6} {r['U_after']:>6} "
              f"{r['pts_after']:>6} {r['bytes_saved']:>7}")


if __name__ == "__main__":
    main()
