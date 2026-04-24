#!/usr/bin/env python3
"""Sweep American English drift across shipped scam pages.

The 2026-04 style guide locked en-US as default, but BrE spellings still slip
into prose (colourful, centre, travellers, organised, programme, etc.). This
script replaces lowercase BrE forms with AmE equivalents in rendered HTML
across scams/<slug>/index.html.

**Lowercase only** — Title-case occurrences are assumed proper nouns (Jane
Austen Centre, Centre Pompidou, Theatre District, etc.) and left alone.

Usage:
    python3 scripts/sweep_ame_drift.py --dry-run
    python3 scripts/sweep_ame_drift.py
    python3 scripts/sweep_ame_drift.py --city bath
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scam_sweep_common import collect_scam_targets

REPO = Path(__file__).resolve().parents[1]
SCAMS = REPO / "scams"

# (BrE, AmE) — longer stems listed first so "travellers" matches before "traveller".
REPLACEMENTS: list[tuple[str, str]] = [
    ("travellers", "travelers"), ("traveller", "traveler"),
    ("favourites", "favorites"), ("favourite", "favorite"),
    ("favoured", "favored"), ("favours", "favors"), ("favour", "favor"),
    ("colourful", "colorful"), ("coloured", "colored"),
    ("colours", "colors"), ("colour", "color"),
    ("centred", "centered"), ("centres", "centers"), ("centre", "center"),
    ("neighbourhoods", "neighborhoods"), ("neighbourhood", "neighborhood"),
    ("neighbours", "neighbors"), ("neighbour", "neighbor"),
    ("organising", "organizing"), ("organisation", "organization"),
    ("organised", "organized"), ("organise", "organize"),
    ("authorising", "authorizing"), ("authorised", "authorized"), ("authorise", "authorize"),
    ("recognising", "recognizing"), ("recognised", "recognized"), ("recognise", "recognize"),
    ("analysing", "analyzing"), ("analysed", "analyzed"), ("analyse", "analyze"),
    ("realising", "realizing"), ("realised", "realized"), ("realise", "realize"),
    ("emphasising", "emphasizing"), ("emphasised", "emphasized"), ("emphasise", "emphasize"),
    ("apologising", "apologizing"), ("apologised", "apologized"), ("apologise", "apologize"),
    ("summarising", "summarizing"), ("summarised", "summarized"), ("summarise", "summarize"),
    ("theatres", "theaters"), ("theatre", "theater"),
    ("jewellery", "jewelry"),
    ("defence", "defense"),
    ("licence", "license"),
    ("aluminium", "aluminum"),
    ("behaviour", "behavior"),
    ("programmes", "programs"), ("programme", "program"),
    ("holidaymakers", "tourists"), ("holidaymaker", "tourist"),
    ("whilst", "while"),
    ("amongst", "among"),
]


def _sub_lowercase_only(bre: str, ame: str):
    """Return a sub function that replaces only when the match is lowercase."""
    pattern = re.compile(rf"\b{re.escape(bre)}\b", re.IGNORECASE)

    def _fn(text: str) -> tuple[str, int]:
        count = 0

        def _replace(m: re.Match) -> str:
            nonlocal count
            matched = m.group(0)
            if matched[0].isupper():
                return matched  # proper noun — keep
            count += 1
            return ame

        return pattern.sub(_replace, text), count

    return _fn


_SUBSTITUTIONS = [(bre, _sub_lowercase_only(bre, ame)) for bre, ame in REPLACEMENTS]


def replace_drift(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    for bre, sub in _SUBSTITUTIONS:
        text, n = sub(text)
        if n > 0:
            counts[bre] = n
    return text, counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--city", help="Only sweep scams/<city>/index.html")
    args = ap.parse_args()

    if args.city:
        targets = [SCAMS / args.city / "index.html"]
    else:
        targets = collect_scam_targets(
            city_pages=True,
            research_json=True,
            api_json=True,
        )

    total_replacements = 0
    files_changed = 0
    for path in targets:
        if not path.exists():
            continue
        original = path.read_text()
        fixed, counts = replace_drift(original)
        if counts and fixed != original:
            files_changed += 1
            n = sum(counts.values())
            total_replacements += n
            summary = ", ".join(f"{k}={v}" for k, v in sorted(counts.items(), key=lambda x: -x[1])[:5])
            label = str(path.relative_to(REPO))
            print(f"  {label:55} — {n} replaced ({summary})")
            if not args.dry_run:
                path.write_text(fixed)

    action = "would replace" if args.dry_run else "replaced"
    print(f"\n{action} {total_replacements} BrE forms across {files_changed} files")


if __name__ == "__main__":
    main()
