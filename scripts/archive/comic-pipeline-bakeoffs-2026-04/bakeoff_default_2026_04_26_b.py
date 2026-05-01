#!/usr/bin/env python3
"""Default-style bake-off, batch B — 5 more candidates, wider range.

Same generic airport-taxi scene + Priya as batch A. Each candidate intentionally
explores a meaningfully-different visual register: print-zine, pure-line
minimalism, geometric mid-century, modern-vector flat-design, traditional
hand-carved print.
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

OUT_DIR = Path("/tmp/bakeoff-default-2026-04-26-b")
OUT_DIR.mkdir(exist_ok=True)

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
    ("risograph-2color-zine", (
        "A single illustrated comic book page in a 2-color risograph zine print style — "
        "limited 2-3 ink palette of fluorescent pink, cobalt blue, and black on warm "
        "off-white paper, deliberate slight color misregistration giving each shape a "
        "subtle ghost-edge, halftone dot shading where a third tone is needed, hand-"
        "drawn ink contour with confident expressive line, contemporary indie-zine print-"
        "culture aesthetic, slightly textured paper grain, generic-international travel-"
        "scene backgrounds (taxi rank, airport curb, modest urban streetlights — no "
        "country-specific landmarks). Showing four sequential panels arranged in a 2x2 "
        "grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, "
        "separated by thin black panel borders with narrow off-white gutters. Each "
        "panel contains one clean white rounded speech bubble with a small pointer tail, "
        "holding short printed English dialogue in simple black hand-lettered text — "
        "text must be legible, in English only, and correctly spelled. Square 1:1 "
        "composition, 2K resolution."
    )),
    ("steinberg-pure-line", (
        "A single illustrated comic book page in the witty minimalist pure-line style of "
        "Saul Steinberg's New Yorker drawings — confident black-ink contour drawing on "
        "pure white background with no shading or color fill (or at most a single "
        "accent of one warm flat tone like soft buttercup yellow or pale terracotta), "
        "extremely economical linework where every line carries observation, expressive "
        "minimalist figures with whimsical wit, witty observational tone of mid-century "
        "New Yorker editorial cartooning, generic-international travel-scene backgrounds "
        "(taxi rank, airport, dusk-lit street — no country-specific landmarks), elegant "
        "white-space-rich composition. Showing four sequential panels arranged in a 2x2 "
        "grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, "
        "separated by thin clean black panel borders with generous white gutters. Each "
        "panel contains one clean white rounded speech bubble with a small pointer tail, "
        "holding short printed English dialogue in simple black sans-serif lettering — "
        "text must be legible, in English only, and correctly spelled. Square 1:1 "
        "composition, 2K resolution."
    )),
    ("charley-harper-geometric", (
        "A single illustrated comic book page in the geometric mid-century-modern flat-"
        "color illustration style of Charley Harper — precise crisp geometric "
        "simplification of figures and objects into clean shapes, restrained mid-century-"
        "modern palette of cream, terracotta, teal, mustard yellow, olive green, and "
        "accent black, perfectly flat color fills with no gradient or texture, witty "
        "graphic-design composition with sharp visual humor, mid-century-modern "
        "sensibility, generic-international travel-scene backgrounds (airport, taxi, "
        "streetlight, sedan — rendered as crisp geometric primitives, no country-"
        "specific landmarks). Showing four sequential panels arranged in a 2x2 grid "
        "with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, "
        "separated by thin black panel borders with narrow cream gutters. Each panel "
        "contains one clean white rounded speech bubble with a small pointer tail, "
        "holding short printed English dialogue in simple black sans-serif lettering — "
        "text must be legible, in English only, and correctly spelled. Square 1:1 "
        "composition, 2K resolution."
    )),
    ("vector-flat-app-illustration", (
        "A single illustrated comic book page in the modern app-illustration vector flat-"
        "design style (Mailchimp / Notion / Slack-illustration aesthetic) — clean "
        "geometric flat-color shapes with subtle dark-line outlines and gentle gradient "
        "accents, soft modern palette of pastel coral, sky blue, sage green, butter "
        "yellow, dusty lilac, and warm cream, friendly cartoon figure proportions with "
        "rounded geometric features, contemporary tech-illustration sensibility, "
        "generic-international travel-scene backgrounds (taxi, airport, urban dusk — "
        "rendered as friendly flat-vector shapes, no country-specific landmarks). "
        "Showing four sequential panels arranged in a 2x2 grid with small numbers "
        "1, 2, 3, 4 in the upper-left corner of each panel, separated by thin clean "
        "black panel borders with narrow cream gutters. Each panel contains one clean "
        "white rounded speech bubble with a small pointer tail, holding short printed "
        "English dialogue in simple black sans-serif lettering — text must be legible, "
        "in English only, and correctly spelled. Square 1:1 composition, 2K resolution."
    )),
    ("linocut-handprinted", (
        "A single illustrated comic book page in the bold tactile hand-carved linocut / "
        "woodcut print style — confident hand-carved black ink shapes with visible "
        "carving texture and slight imprint variation, single accent spot-color (warm "
        "vermillion red OR deep cobalt blue, not both), warm cream paper background "
        "with subtle grain, mid-century social-illustration print-heritage tone, "
        "expressive simplified figures with carved-block confidence, deliberate carving-"
        "tool marks visible in the linework, generic-international travel-scene "
        "backgrounds (taxi rank, airport curb, urban streetlight — rendered with "
        "carved-block boldness, no country-specific landmarks). Showing four "
        "sequential panels arranged in a 2x2 grid with small hand-carved numbers "
        "1, 2, 3, 4 in the upper-left corner of each panel, separated by thin black "
        "carved-block panel borders with narrow cream gutters. Each panel contains one "
        "clean white rounded speech bubble with a small pointer tail, holding short "
        "printed English dialogue in simple black hand-lettered text — text must be "
        "legible, in English only, and correctly spelled. Square 1:1 composition, "
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

    print(f"Submitting {len(CANDIDATES)} default-style batch-B generations...", flush=True)
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
