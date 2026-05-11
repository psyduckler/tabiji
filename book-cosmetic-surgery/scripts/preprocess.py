#!/usr/bin/env python3
"""
preprocess.py — Add pandoc fenced-div semantic markers to the cosmetic
surgery manuscript so the CSS in print-style.css and epub-style.css can
style scenarios, decision gates, pull quotes, and the journey-map table.

Reads manuscript-source.md, writes manuscript-processed.md.
"""

import re
from pathlib import Path

SRC = Path(__file__).parent / "manuscript-source.md"
DST = Path(__file__).parent / "manuscript-processed.md"


def wrap_with_div(text: str, pattern: str, classname: str, flags: int = re.DOTALL) -> str:
    """Wrap content matching `pattern` in a pandoc fenced div with `classname`."""
    def replacer(match: re.Match) -> str:
        return f"::: {{.{classname}}}\n{match.group(1).rstrip()}\n:::\n"
    return re.sub(pattern, replacer, text, flags=flags)


def main() -> None:
    text = SRC.read_text(encoding="utf-8")

    # ---------------------------------------------------------------
    # 1. The manuscript's pullquotes use `::: {.pullquote}` directly.
    #    CSS uses `.pull-quote` (with hyphen) for series consistency
    #    with Volume 1. Rename here.
    # ---------------------------------------------------------------
    text = text.replace("::: {.pullquote}", "::: {.pull-quote}")

    # ---------------------------------------------------------------
    # 2. Wrap in-chapter Composite Scenarios (A through K).
    #    Pattern: "### Composite Scenario X: ..." until next ###/##/#/---
    # ---------------------------------------------------------------
    text = wrap_with_div(
        text,
        r"(### Composite Scenario [A-K]:[^\n]+\n\n.+?)(?=\n### |\n## |\n# |\n---\n)",
        "scenario",
    )

    # ---------------------------------------------------------------
    # 3. Wrap the closing Composite Scenario L. In this volume L is at
    #    h2 (## Composite Scenario L — ...) with an em-dash separator
    #    rather than a colon — distinct from the dental volume.
    # ---------------------------------------------------------------
    text = wrap_with_div(
        text,
        r"(## Composite Scenario L —[^\n]+\n\n.+?)(?=\n---\n)",
        "scenario scenario-closing",
    )

    # ---------------------------------------------------------------
    # 4. Wrap Decision Gate sections that begin with a heading.
    #    Pattern: "### Decision Gate: ..." until next ###/##/#/---
    # ---------------------------------------------------------------
    text = wrap_with_div(
        text,
        r"(### Decision Gate:[^\n]+\n\n.+?)(?=\n### |\n## |\n# |\n---\n)",
        "decision-gate",
    )

    # ---------------------------------------------------------------
    # 5. Wrap inline-label Decision Gates: "**Decision Gate**" + paragraph(s).
    #    These appear at the end of clinic / surgeon / implant chapters.
    # ---------------------------------------------------------------
    text = wrap_with_div(
        text,
        r"(\*\*Decision Gate\*\*\n\n(?:(?!\n---\n|\n## |\n# ).)+)",
        "decision-gate-inline",
    )

    # ---------------------------------------------------------------
    # 6. Class the Journey at a Glance table so the CSS can style it.
    #    The cosmetic-surgery version of the journey table uses the same
    #    column structure as the dental volume.
    # ---------------------------------------------------------------
    text = re.sub(
        r"(\| Stage \| When \| Your leverage \| Worksheets that help \| Where leverage usually drops \|\n)",
        r"::: {.journey-map}\n\1",
        text,
        count=1,
    )
    text = re.sub(
        r"(\| 10\. The return home[^\n]+\|)\n\n(The chapters that follow)",
        r"\1\n\n:::\n\n\2",
        text,
        count=1,
    )

    DST.write_text(text, encoding="utf-8")
    print(f"Preprocessed manuscript written to: {DST}")
    print(f"  Source:    {len(SRC.read_text(encoding='utf-8')):,} chars")
    print(f"  Processed: {len(text):,} chars")


if __name__ == "__main__":
    main()
