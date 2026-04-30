#!/usr/bin/env python3
"""Retry the 2 gpt-image-2 stragglers with artist-name-free style blocks.

editorial-niemann-flat-vector and classic-sunday-comic-ink-wash both
silently failed at poll on gpt-image-2, twice. Both prompts named living
illustrators (Christoph Niemann, Bill Watterson, Berkeley Breathed) which
OpenAI's image policy filter likely rejects. Rewriting the style blocks
to describe the aesthetic abstractly (no artist names) so the same visual
target is communicated without the filter trip.
"""
from __future__ import annotations

import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from bakeoff_everywhere_2026_04_30_gpt import generate_one  # noqa: E402
from bakeoff_everywhere_2026_04_30 import GENERIC_SCENE  # noqa: E402
from cast import CHARACTERS  # noqa: E402
from generate import _keychain  # noqa: E402

# Same visual targets, no living-artist names.
RETRY_CANDIDATES = [
    ("editorial-niemann-flat-vector", (
        "A single illustrated comic book page in a refined modern editorial-"
        "illustration style as seen in upmarket American magazine covers — "
        "clean precise black-ink linework with restrained flat vector-style "
        "color fills, sophisticated limited palette of cream, ink-blue, "
        "terracotta, mustard, and one accent red, minimalist confident "
        "composition with clever visual storytelling, refined modern "
        "editorial-magazine sensibility, generic American domestic-scam "
        "scenes (kitchen counter, drugstore gift-card rack, retail checkout), "
        "warm afternoon light, ageless universal appeal across generations. "
        "Showing four sequential panels arranged in a 2x2 grid with small "
        "numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated "
        "by thin black panel borders with narrow white gutters. Each panel "
        "contains one clean white rounded speech bubble with a small pointer "
        "tail, holding short printed English dialogue in simple black sans-"
        "serif lettering — text must be legible, in English only, and "
        "correctly spelled. Square 1:1 composition, 2K resolution."
    )),
    ("classic-sunday-comic-ink-wash", (
        "A single illustrated comic book page in the warm classic American "
        "Sunday-newspaper-comic-strip tradition — confident expressive "
        "black-ink contour drawing with light watercolor wash fills, friendly "
        "Sunday-paper palette of cream paper, warm yellow, sky blue, soft red, "
        "sap green, and grounded earth tones, expressive cartoon figures with "
        "warm relatable faces, classic American comic-strip pacing and "
        "composition, generic American domestic-scam scenes (kitchen counter, "
        "drugstore gift-card rack, retail checkout). Universally familiar "
        "Americana that reads as friendly and trustworthy across all ages. "
        "Showing four sequential panels arranged in a 2x2 grid with small "
        "numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated "
        "by thin black panel borders with narrow cream gutters. Each panel "
        "contains one clean white rounded speech bubble with a small pointer "
        "tail, holding short printed English dialogue in simple black comic "
        "lettering — text must be legible, in English only, and correctly "
        "spelled. Square 1:1 composition, 2K resolution."
    )),
]


def build_prompt(style_block: str) -> str:
    char = CHARACTERS["margie"]
    return f"{style_block}\n\nCHARACTER: {char}\n\n{GENERIC_SCENE}"


def main():
    ws = _keychain("wavespeed-api-key")
    if not ws:
        print("ERROR: missing wavespeed-api-key", flush=True)
        sys.exit(1)
    print(f"Retrying {len(RETRY_CANDIDATES)} gpt-image-2 stragglers (no-artist-name prompts)...", flush=True)
    results: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=2) as ex:
        futs = {ex.submit(generate_one, slug, build_prompt(sb), ws): slug
                for slug, sb in RETRY_CANDIDATES}
        for fut in as_completed(futs):
            slug = futs[fut]
            try:
                _, result = fut.result()
            except Exception as e:
                result = f"FAIL: {e}"
            results[slug] = result
            print(f"  {slug}: {result}", flush=True)


if __name__ == "__main__":
    main()
