#!/usr/bin/env python3
"""Default-style bake-off — fallback used when a country has no specific lock.

5 candidates anchored on a deliberately-generic airport-taxi scam scene
(no country-specific landmarks/signage), so the chosen default reads as
universal rather than tied to any locked country.
"""
from __future__ import annotations

import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import (  # noqa: E402
    submit_nbp, poll_nbp, download_verify, upload_r2, _keychain, T2I_EP,
)
from cast import CHARACTERS  # noqa: E402

OUT_DIR = Path("/tmp/bakeoff-default-2026-04-26")
OUT_DIR.mkdir(exist_ok=True)

# Generic scene — no country-specific landmarks. Could be anywhere.
GENERIC_SCENE = (
    "SCENE:\n"
    "Panel 1: Priya stands at a generic international airport taxi rank in late afternoon "
    "light, her hiking backpack at her feet, as a taxi driver loads her rolling suitcase "
    "into the trunk of a beige sedan. A modest 'TAXI' sign is visible. Speech bubble "
    "(driver): \"To your hotel — meter is broken.\"\n"
    "Panel 2: Inside the taxi, Priya looks at her smartphone showing a generic rideshare "
    "app with a small fare estimate, while the driver gestures dismissively at the meter. "
    "Speech bubble (driver): \"Fixed price one fifty — meter no good!\"\n"
    "Panel 3: The taxi is parked under streetlights at dusk; Priya holds her phone up "
    "showing the rideshare app's map and price clearly. Speech bubble (Priya): \"App "
    "says forty.\"\n"
    "Panel 4: Priya climbs into a clearly-marked rideshare car (a clean white sedan with "
    "a generic rideshare-logo on the door), calmly waving off the first taxi. Speech "
    "bubble (Priya): \"Always use the app — never broken meters.\""
)

CANDIDATES = [
    ("warm-watercolor-storybook", (
        "A single illustrated comic book page in a warm soft watercolor-and-ink storybook "
        "style — confident fine black-ink contour drawing with light hand-painted "
        "watercolor washes, neutral universal palette of cream, sky blue, warm ochre, "
        "sage green, dusty rose, and pale terracotta, friendly cartoon character figures "
        "with simple expressive faces, generic-international travel-scene backgrounds "
        "(taxi rank, airport curb, modest sedan, streetlight, generic urban context — no "
        "country-specific landmarks), warm afternoon light, gentle storybook tone "
        "appropriate to global cautionary travel-warnings. Showing four sequential panels "
        "arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner "
        "of each panel, separated by thin black panel borders with narrow cream gutters. "
        "Each panel contains one clean white rounded speech bubble with a small pointer "
        "tail, holding short printed English dialogue in simple black comic lettering — "
        "text must be legible, in English only, and correctly spelled. Square 1:1 "
        "composition, 2K resolution."
    )),
    ("editorial-niemann-sophisticated", (
        "A single illustrated comic book page in a refined editorial-illustration style "
        "reminiscent of Christoph Niemann and modern New Yorker travel-essay visuals — "
        "clean precise black-ink linework with restrained flat-color fills, sophisticated "
        "limited palette of cream, ink-blue, terracotta, mustard, and one accent red, "
        "minimalist confident composition with clever visual storytelling, refined "
        "editorial-illustration tone, generic-international travel-scene backgrounds "
        "without country-specific landmarks, modern thoughtful travel-magazine aesthetic. "
        "Showing four sequential panels arranged in a 2x2 grid with small numbers "
        "1, 2, 3, 4 in the upper-left corner of each panel, separated by thin black panel "
        "borders with narrow white gutters. Each panel contains one clean white rounded "
        "speech bubble with a small pointer tail, holding short printed English dialogue "
        "in simple black sans-serif lettering — text must be legible, in English only, "
        "and correctly spelled. Square 1:1 composition, 2K resolution."
    )),
    ("contemporary-graphic-novel", (
        "A single illustrated comic book page in a confident contemporary graphic-novel "
        "style — bold black-ink outlines with rich painterly gouache fills, balanced "
        "saturated palette of warm sand, deep teal, brick red, mustard yellow, slate "
        "navy, and cream, realistic figure proportions and expressive faces, modern "
        "indie-comic narrative pacing, visible painterly texture, generic-international "
        "travel-scene backgrounds (airport curb, taxi rank, urban dusk-lit street, "
        "rideshare vehicle — no country-specific landmarks), contemporary American/"
        "European graphic-novel sensibility appropriate to cautionary scam-warning "
        "narrative. Showing four sequential panels arranged in a 2x2 grid with small "
        "numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin "
        "clean black panel borders with narrow white gutters. Each panel contains one "
        "clean white rounded speech bubble with a small pointer tail, holding short "
        "printed English dialogue in simple black comic lettering — text must be "
        "legible, in English only, and correctly spelled. Square 1:1 composition, "
        "2K resolution."
    )),
    ("travel-journal-sketch", (
        "A single illustrated comic book page in a loose hand-drawn travel-journal sketch "
        "style — confident pencil-and-pen contour drawing with quick observational "
        "linework, light watercolor washes with visible bleed and grain, off-white "
        "sketchbook-paper background with subtle texture, restrained palette of warm "
        "umber, cream, sky blue, sap green, and dusty rose, casual journaling-on-the-road "
        "aesthetic with handwritten margin annotations, friendly observed figures with "
        "everyday realism, generic-international travel-scene backgrounds (taxi rank, "
        "airport, dusk-lit streets — no country-specific landmarks). Showing four "
        "sequential panels arranged in a 2x2 grid with small hand-drawn numbers 1, 2, 3, 4 "
        "in the upper-left corner of each panel, separated by hand-drawn pen panel "
        "borders with narrow off-white gutters. Each panel contains one clean white "
        "rounded speech bubble with a small pointer tail, holding short printed English "
        "dialogue in simple black hand-lettering — text must be legible, in English "
        "only, and correctly spelled. Square 1:1 composition, 2K resolution."
    )),
    ("midcentury-childrens-book", (
        "A single illustrated comic book page in the warm mid-century children's-book "
        "illustration style of artists like Mary Blair, Miroslav Šašek, or Eric Carle — "
        "bold flat hand-painted shapes with confident dark-ink outline accents, warm "
        "mid-century palette of cream paper, warm coral, teal blue, mustard yellow, "
        "olive green, and accent black, slightly textured paper-and-paint feel as if "
        "rendered with cut-paper or gouache, simplified flattened figures with friendly "
        "expressive faces, joyful storybook tone, generic-international travel-scene "
        "backgrounds (taxi rank, airport, modest urban scene — no country-specific "
        "landmarks). Showing four sequential panels arranged in a 2x2 grid with small "
        "hand-painted numbers 1, 2, 3, 4 in the upper-left corner of each panel, "
        "separated by thin black panel borders with narrow cream gutters. Each panel "
        "contains one clean white rounded speech bubble with a small pointer tail, "
        "holding short printed English dialogue in simple black comic lettering — text "
        "must be legible, in English only, and correctly spelled. Square 1:1 composition, "
        "2K resolution."
    )),
]


def build_prompt(style_block: str) -> str:
    char = CHARACTERS["priya"]
    return f"{style_block}\n\nCHARACTER: {char}\n\n{GENERIC_SCENE}"


def generate_one(slug: str, prompt: str, ws: str, r2: str) -> tuple[str, str]:
    body = {"prompt": prompt, "aspect_ratio": "1:1", "resolution": "2k", "output_format": "jpeg"}
    tid = submit_nbp(body, T2I_EP, ws)
    if not tid:
        return slug, "FAIL: submit"
    raw_url = poll_nbp(tid, ws, timeout=600)
    if not raw_url:
        return slug, "FAIL: poll"
    out = OUT_DIR / f"default-{slug}.jpg"
    ok, note = download_verify(raw_url, out)
    if not ok:
        return slug, f"FAIL: dl {note}"
    r2_key = f"scam-comics/_default/style-tests/{slug}.jpg"
    if not upload_r2(out, r2_key, r2):
        return slug, "FAIL: r2"
    return slug, f"https://img.tabiji.ai/{r2_key}"


def main():
    ws = _keychain("wavespeed-api-key")
    r2 = _keychain("cloudflare-api-token")
    if not ws or not r2:
        print("ERROR: missing creds", flush=True)
        sys.exit(1)

    print(f"Submitting {len(CANDIDATES)} default-style bake-off generations...", flush=True)
    results: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(generate_one, slug, build_prompt(sb), ws, r2): slug
                for slug, sb in CANDIDATES}
        for fut in as_completed(futs):
            slug = futs[fut]
            try:
                _, result = fut.result()
            except Exception as e:
                result = f"FAIL: {e}"
            results[slug] = result
            print(f"  {slug}: {result}", flush=True)

    print("\n=== RESULTS ===", flush=True)
    for slug, _ in CANDIDATES:
        print(f"  {slug}: {results.get(slug, 'missing')}", flush=True)


if __name__ == "__main__":
    main()
