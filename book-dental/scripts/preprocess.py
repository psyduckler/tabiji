#!/usr/bin/env python3
"""
preprocess.py — Add pandoc fenced-div semantic markers to the manuscript.

Reads manuscript-source.md, identifies recurring structural elements
(composite scenarios, decision gates, color-coded flag sections, pull quotes),
and wraps them in pandoc fenced-div syntax so they can be styled by CSS in
the EPUB and the print PDF.

Output: manuscript-processed.md (in same directory)

Run:
    python3 preprocess.py
"""

import re
from pathlib import Path

SRC = Path(__file__).parent / "manuscript-source.md"
DST = Path(__file__).parent / "manuscript-processed.md"

# The five marked pull quotes (must match exactly the text in manuscript-source.md)
PULL_QUOTES = [
    "Hope is important. It is not enough to sign consent.",
    "The moment you feel rescued is the moment to ask better questions.",
    "A lifetime warranty with no written terms is not a warranty; it is a slogan.",
    "A patient who can be pressured in chat can be pressured in the chair.",
    "Cheaper dental work is only cheaper when you can finish it well.",
]


def wrap_with_div(text: str, pattern: str, classname: str, flags: int = re.DOTALL) -> str:
    """Wrap content matching `pattern` in a pandoc fenced div with `classname`."""
    def replacer(match: re.Match) -> str:
        return f"::: {{.{classname}}}\n{match.group(1).rstrip()}\n:::\n"
    return re.sub(pattern, replacer, text, flags=flags)


def main() -> None:
    text = SRC.read_text(encoding="utf-8")

    # ---------------------------------------------------------------
    # 1. Wrap in-chapter Composite Scenarios (A through K).
    #    Pattern: "### Composite Scenario X: ..." until next ###/##/#/---
    # ---------------------------------------------------------------
    text = wrap_with_div(
        text,
        r"(### Composite Scenario [A-K]:[^\n]+\n\n.+?)(?=\n### |\n## |\n# |\n---\n)",
        "scenario",
    )

    # ---------------------------------------------------------------
    # 2. Wrap the closing Composite Scenario L (top-level H1).
    #    Stop the capture BEFORE the trailing `---` separator so the
    #    fenced-div close tag does not collide with pandoc's YAML parser.
    # ---------------------------------------------------------------
    text = wrap_with_div(
        text,
        r"(# Composite Scenario L —[^\n]+\n\n.+?)(?=\n---\n)",
        "scenario scenario-closing",
    )

    # ---------------------------------------------------------------
    # 3. Wrap Decision Gate sections that begin with a heading.
    #    Pattern: "### Decision Gate: ..." until next ###/##/#/---
    # ---------------------------------------------------------------
    text = wrap_with_div(
        text,
        r"(### Decision Gate:[^\n]+\n\n.+?)(?=\n### |\n## |\n# |\n---\n)",
        "decision-gate",
    )

    # ---------------------------------------------------------------
    # 4. Wrap inline-label Decision Gates: "**Decision Gate**" + paragraph(s).
    #    These appear at the end of worksheet sections in Parts III–IV.
    #    Pattern captures up to (but not including) the next blank-line
    #    section break marker.
    # ---------------------------------------------------------------
    text = wrap_with_div(
        text,
        r"(\*\*Decision Gate\*\*\n\n(?:(?!\n---\n|\n## |\n# ).)+)",
        "decision-gate-inline",
    )

    # ---------------------------------------------------------------
    # 5. Wrap full Green/Yellow/Red Flag triplet sections.
    #    Pattern: "### Green, Yellow, and Red Flags: ..." until next ###/##/#/---
    # ---------------------------------------------------------------
    text = wrap_with_div(
        text,
        r"(### Green, Yellow, and Red Flags:[^\n]+\n\n.+?)(?=\n### |\n## |\n# |\n---\n)",
        "flags-section",
    )

    # ---------------------------------------------------------------
    # 6. Convert **Green flags** / **Yellow flags** / **Red flags** sub-labels
    #    into headed divs so they get color treatment.
    # ---------------------------------------------------------------
    # Each pattern wraps the bold label + the bullet list that follows
    text = re.sub(
        r"\*\*Green flags\*\*\n\n((?:- [^\n]+\n)+)",
        r"::: {.green-flags}\n**Green flags**\n\n\1:::\n\n",
        text,
    )
    text = re.sub(
        r"\*\*Yellow flags\*\*\n\n((?:- [^\n]+\n)+)",
        r"::: {.yellow-flags}\n**Yellow flags**\n\n\1:::\n\n",
        text,
    )
    text = re.sub(
        r"\*\*Red flags\*\*\n\n((?:- [^\n]+\n)+)",
        r"::: {.red-flags}\n**Red flags**\n\n\1:::\n\n",
        text,
    )

    # ---------------------------------------------------------------
    # 7. Wrap the five marked pull quotes as standalone divs.
    #    First, detach any pull quote that's embedded mid-paragraph
    #    by splitting it onto its own line. Then wrap each one.
    # ---------------------------------------------------------------
    for quote in PULL_QUOTES:
        # First, split the pull quote off its preceding sentence(s) on the same line.
        # Match: "<preceding text>. <pull quote>$" → "<preceding text>.\n\n<pull quote>$"
        embedded_pattern = re.compile(
            rf"^([^\n]+?\.) {re.escape(quote)}$",
            re.MULTILINE,
        )
        text = embedded_pattern.sub(rf"\1\n\n{quote}", text)

        # Then wrap the now-standalone quote.
        pattern = re.compile(rf"^{re.escape(quote)}$", re.MULTILINE)
        replacement = f"::: {{.pull-quote}}\n{quote}\n:::"
        new_text, count = pattern.subn(replacement, text)
        if count == 0:
            print(f"WARNING: pull quote not found: {quote[:40]}…")
        else:
            text = new_text

    # ---------------------------------------------------------------
    # 8. Class up the Journey Map table so it can be styled distinctively.
    # ---------------------------------------------------------------
    text = re.sub(
        r"(### The Journey at a Glance\n\n[^\n]+\n\n)(\| Stage \| When \|)",
        r"\1::: {.journey-map}\n\2",
        text,
    )
    # Close the journey-map div after the table (look for the line right after
    # the table data - matches blank line + paragraph starting with "The chapters")
    text = re.sub(
        r"(\| 10\. The return home[^\n]+\|)\n\n(The chapters that follow)",
        r"\1\n\n:::\n\n\2",
        text,
    )

    DST.write_text(text, encoding="utf-8")
    print(f"Preprocessed manuscript written to: {DST}")
    print(f"  Source:    {len(SRC.read_text(encoding='utf-8')):,} chars")
    print(f"  Processed: {len(text):,} chars")


if __name__ == "__main__":
    main()
