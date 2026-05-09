#!/usr/bin/env python3
"""
Assemble the Scam Atlas manuscript into a single book-ready .md file.

Output: ../the-scam-atlas-FULL.md

Order:
  - Title page (generated)
  - Copyright (01)
  - Introduction (02)
  - PART I divider
  - How to Use (03)
  - Scams That Aren't (04)
  - The Seven Patterns (05)
  - Pre-Trip Checklist (06)
  - First 24 Hours (07)
  - PART II divider
  - atlas-* chapters (30, alphabetical)
  - PART III divider
  - Appendices A-I (90-98)
  - About (99)
  - Final Note (100)

Page breaks use \\newpage (pandoc raw LaTeX → PDF page break;
ePub renders as section break).
"""

import os
import sys
from pathlib import Path

MANUSCRIPT_DIR = Path(__file__).parent.parent / "manuscript"
OUTPUT_PATH = Path(__file__).parent.parent / "the-big-book-of-travel-scams-FULL.md"

# Pandoc renders the title page from YAML metadata in both ePub and
# xelatex-PDF paths. We add a small Markdown block beneath for the
# series line + edition text that the YAML metadata does not cover.
TITLE_PAGE = """---
title: "The Big Book of Travel Scams"
subtitle: "Thirty Scripts, Seven Patterns, and the Defense for Each"
author:
- "Bernard Huang, Editor"
- "Tabiji"
date: "2026"
publisher: "Tabiji"
rights: "© 2026 Tabiji Inc. All rights reserved."
language: "en-US"
toc: true
toc-depth: 1
---

\\begin{center}
\\vspace*{2cm}
{\\large 2026 Edition} \\\\[1em]
{\\itshape The Travel Safety Series}
\\end{center}

\\newpage

"""

PART_I_DIVIDER = """\\newpage

# Part I: How to Read This Book

The seven universal patterns that underlie almost every scam in
this book, plus the practical checklists for the pre-trip evening
and the first twenty-four hours of any trip. Read this part before
the atlas. If you read no further than Part I, you will spot
eighty percent of the scripts in Part II the moment they begin
running on you.

\\newpage

"""

PART_II_DIVIDER = """\\newpage

# Part II: The Thirty Scams

Thirty chapters, alphabetical by scam name, each one a single
scam. Every chapter follows the same structure: a scene, the
trick, the mechanics, the geography, the red flags, the exit
phrases, and the recovery sequence. Read by destination, not
exhaustively. The catastrophic-tier chapters (express kidnapping,
fake drug-search police sting, drink spiking, gem and jewelry shop
pressure, phone snatch motorcycle, tea house invitation) are worth
the cover-to-cover read regardless of where you are traveling.

The thirty are alphabetical, with the letters most-documented
worldwide carrying multiple chapters and other letters appearing
in the broader Tabiji web atlas at tabiji.ai/scams/atlas.

\\newpage

"""

PART_III_DIVIDER = """\\newpage

# Part III: Appendices

The eleven-language exit-phrase index. The post-scam recovery
playbook. Emergency contacts for twenty-four countries. Reading
lists by traveler type and by severity. The glossary of cultural
terms. The scope clarifier. The thirty-day aftermath chapter. The
sources-and-methodology essay.

\\newpage

"""

# Order of files
FRONT_MATTER = [
    "01-copyright.md",
    "02-introduction.md",
]

PART_I_FILES = [
    "03-how-to-use.md",
    "04-scams-that-arent.md",
    "05-patterns.md",
    "06-pre-trip-checklist.md",
    "07-first-24-hours.md",
]

# Atlas chapters: alphabetical
PART_II_FILES = sorted([f.name for f in MANUSCRIPT_DIR.glob("atlas-*.md")])

PART_III_FILES = [
    "90-appendix-phrases.md",
    "91-appendix-recovery.md",
    "92-appendix-contacts.md",
    "93-appendix-traveler-types.md",
    "94-appendix-severity.md",
    "95-appendix-glossary.md",
    "96-appendix-scope-clarifier.md",
    "97-appendix-aftermath.md",
    "98-appendix-methodology.md",
]

BACK_MATTER = [
    "99-about.md",
    "100-cta.md",
]


def read_file(name: str) -> str:
    path = MANUSCRIPT_DIR / name
    if not path.exists():
        sys.exit(f"Missing: {path}")
    return path.read_text()


def section(name: str) -> str:
    """Return file contents preceded by a page-break."""
    return f"\\newpage\n\n{read_file(name).rstrip()}\n"


def main() -> None:
    parts: list[str] = []

    # Title page
    parts.append(TITLE_PAGE)

    # Front matter (copyright + introduction)
    for f in FRONT_MATTER:
        parts.append(section(f))

    # Part I
    parts.append(PART_I_DIVIDER)
    for f in PART_I_FILES:
        parts.append(section(f))

    # Part II (atlas)
    parts.append(PART_II_DIVIDER)
    for f in PART_II_FILES:
        parts.append(section(f))

    # Part III (appendices)
    parts.append(PART_III_DIVIDER)
    for f in PART_III_FILES:
        parts.append(section(f))

    # Back matter (about + CTA)
    for f in BACK_MATTER:
        parts.append(section(f))

    full = "\n\n".join(parts)
    OUTPUT_PATH.write_text(full)

    word_count = len(full.split())
    print(f"Wrote {OUTPUT_PATH}")
    print(f"Word count: {word_count:,}")
    print(
        f"Files included: "
        f"{len(FRONT_MATTER) + len(PART_I_FILES) + len(PART_II_FILES) + len(PART_III_FILES) + len(BACK_MATTER)}"
    )
    print(f"  Front matter: {len(FRONT_MATTER)}")
    print(f"  Part I: {len(PART_I_FILES)}")
    print(f"  Part II atlas: {len(PART_II_FILES)}")
    print(f"  Part III appendices: {len(PART_III_FILES)}")
    print(f"  Back matter: {len(BACK_MATTER)}")


if __name__ == "__main__":
    main()
