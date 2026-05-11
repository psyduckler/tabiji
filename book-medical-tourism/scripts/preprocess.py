#!/usr/bin/env python3
"""
preprocess.py — Add pandoc fenced-div semantic markers to the Medical
Tourism Field Guide manuscript so the CSS in print-style.css and
epub-style.css can style scenarios, decision gates, pull quotes, and
the journey-map table.

V3 differences from V2's preprocess.py:
- Composite scenario headings use em-dash separators (e.g. "### Composite
  Scenario A — Marcus at Week 2"), not colons. The regex matches both
  initial scenes ("Composite Scenario A — Marcus") and continuation
  scenes ("Composite Scenario A continued — Marcus at 8 months").
- Composite Scenario L is at h2 (## Composite Scenario L — ...) with an
  em-dash separator, same as V2.
- Pull-quote and Bernard-note divs are already written with hyphenated
  class names in the V3 manuscript; no rename step is needed.
- Journey-map table is already inside its `::: {.journey-map}` fence;
  no auto-wrap step needed.

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
    # 1. Wrap in-chapter Composite Scenarios (A through K, including
    #    continuations). V3 uses em-dash separators, not colons.
    #    Pattern: "### Composite Scenario X — ..." or
    #             "### Composite Scenario X continued — ..."
    #    until next ###/##/#/---
    # ---------------------------------------------------------------
    text = wrap_with_div(
        text,
        r"(### Composite Scenario [A-K](?: continued)? —[^\n]+\n\n.+?)(?=\n### |\n## |\n# |\n---\n)",
        "scenario",
    )

    # ---------------------------------------------------------------
    # 2. Wrap the closing Composite Scenario L (h2). Stop before the
    #    trailing `---` so the fenced-div close tag doesn't collide
    #    with pandoc's YAML parser.
    # ---------------------------------------------------------------
    text = wrap_with_div(
        text,
        r"(## Composite Scenario L —[^\n]+\n\n.+?)(?=\n---\n)",
        "scenario scenario-closing",
    )

    # ---------------------------------------------------------------
    # 3. The V3 manuscript already uses `::: {.decision-gate}` and
    #    `::: {.bernard-note}` and `::: {.pull-quote}` directly. No
    #    rename or auto-wrap is needed for these.
    # ---------------------------------------------------------------

    # ---------------------------------------------------------------
    # 4. The Journey at a Glance table at Chapter introduction is
    #    already inside its `::: {.journey-map}` fence. No auto-wrap.
    # ---------------------------------------------------------------

    DST.write_text(text, encoding="utf-8")
    print(f"Preprocessed manuscript written to: {DST}")
    print(f"  Source:    {len(SRC.read_text(encoding='utf-8')):,} chars")
    print(f"  Processed: {len(text):,} chars")


if __name__ == "__main__":
    main()
