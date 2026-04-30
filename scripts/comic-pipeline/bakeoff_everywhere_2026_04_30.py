#!/usr/bin/env python3
"""Everywhere-scams style bake-off — picking the locked house style for
/scams/everywhere/ comics (one-per-variant).

Different from the travel-scam default (bakeoff_default_2026_04_26): the
test scene here is a domestic gift-card-by-phone scam, since everywhere
content lives in kitchens / phones / drugstores rather than airports
or taxi ranks. The chosen style must read as universal across age and
class — these articles target Gen Z marketplace buyers and 60+
gift-card-scam targets in the same series.

5 candidates, all distinct, all universal-domestic.
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

OUT_DIR = Path("/tmp/bakeoff-everywhere-2026-04-30")
OUT_DIR.mkdir(exist_ok=True)

# Generic everywhere-scam scene — gift-card-by-phone. The most universal
# everywhere-scam channel (phone-call impersonation covers gift-card,
# Medicare, IRS, boss-BEC, AI-voice-clone, tech-support, bank-impersonation).
GENERIC_SCENE = (
    "SCENE:\n"
    "Panel 1: Margie stands at her kitchen counter in late afternoon light, "
    "holding a cordless phone to her ear with a worried expression, a half-"
    "made cup of tea on the counter. Speech bubble (voice from phone): "
    "\"This is your bank — your account is being drained right now.\"\n"
    "Panel 2: Margie at a drugstore gift-card rack with the phone still "
    "pressed to her ear, hand reaching toward a stack of $500 retail gift "
    "cards on the rack. Speech bubble (voice from phone): \"Buy gift cards "
    "and read me the codes — that's how we secure your funds.\"\n"
    "Panel 3: Margie at the drugstore checkout, $2,000 of gift cards on "
    "the counter, a young cashier looking concerned and gesturing at the "
    "cards. Speech bubble (cashier): \"Ma'am — is someone on the phone "
    "telling you to buy these?\"\n"
    "Panel 4: Margie back at her kitchen counter, phone face-down on the "
    "counter, talking calmly to a younger family member at the kitchen "
    "table. Speech bubble (Margie): \"No bank ever asks for gift cards.\""
)

CANDIDATES = [
    ("editorial-niemann-flat-vector", (
        "A single illustrated comic book page in a refined editorial-illustration "
        "style reminiscent of Christoph Niemann and modern New Yorker covers — "
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
    ("risograph-zine-duotone", (
        "A single illustrated comic book page in a contemporary risograph-print "
        "zine style — bold confident hand-drawn linework printed in a saturated "
        "risograph duotone-plus-accent palette of fluorescent coral red, deep "
        "ink blue, and warm cream paper with visible grain and slight off-"
        "register print misalignment for authentic riso character, halftone-dot "
        "shading textures, modern indie-zine aesthetic, friendly observational "
        "figures with simple clear features, generic American domestic-scam "
        "scenes (kitchen counter, drugstore gift-card rack, retail checkout). "
        "Contemporary, humane, universally readable across age and class. "
        "Showing four sequential panels arranged in a 2x2 grid with small "
        "numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated "
        "by thin ink-blue panel borders with narrow cream gutters. Each panel "
        "contains one clean white rounded speech bubble with a small pointer "
        "tail, holding short printed English dialogue in simple black comic "
        "lettering — text must be legible, in English only, and correctly "
        "spelled. Square 1:1 composition, 2K resolution."
    )),
    ("midcentury-storybook-poster", (
        "A single illustrated comic book page in the warm mid-century "
        "American children's-book and travel-poster style of Mary Blair, "
        "Miroslav Šašek, and Charley Harper — bold flat hand-painted gouache "
        "shapes with confident dark-ink outline accents, mid-century palette "
        "of cream paper, warm coral, teal blue, mustard yellow, olive green, "
        "and accent black, slightly textured paper-and-paint feel, simplified "
        "stylized figures with friendly expressive faces, joyful but grounded "
        "storybook tone, generic American domestic-scam scenes (kitchen "
        "counter, drugstore gift-card rack, retail checkout). Nostalgic-"
        "American without being dated; universally beloved across "
        "generations. Showing four sequential panels arranged in a 2x2 grid "
        "with small hand-painted numbers 1, 2, 3, 4 in the upper-left corner "
        "of each panel, separated by thin black panel borders with narrow "
        "cream gutters. Each panel contains one clean white rounded speech "
        "bubble with a small pointer tail, holding short printed English "
        "dialogue in simple black comic lettering — text must be legible, "
        "in English only, and correctly spelled. Square 1:1 composition, "
        "2K resolution."
    )),
    ("contemporary-painterly-gouache", (
        "A single illustrated comic book page in a sophisticated contemporary "
        "painterly editorial-illustration style reminiscent of New York Times "
        "Magazine and modern long-form journalism illustration — confident "
        "loose gouache and ink work with visible brush texture, sophisticated "
        "muted palette of bone, slate navy, brick red, ochre, sage, and warm "
        "shadow grays, expressive realistic figures with thoughtful body "
        "language, modern editorial-illustration tone appropriate to serious "
        "consumer-protection journalism, generic American domestic-scam "
        "scenes (kitchen counter, drugstore gift-card rack, retail checkout). "
        "Quiet, dignified, universally readable as serious-but-warm. "
        "Showing four sequential panels arranged in a 2x2 grid with small "
        "numbers 1, 2, 3, 4 in the upper-left corner of each panel, "
        "separated by thin black panel borders with narrow off-white gutters. "
        "Each panel contains one clean white rounded speech bubble with a "
        "small pointer tail, holding short printed English dialogue in simple "
        "black comic lettering — text must be legible, in English only, and "
        "correctly spelled. Square 1:1 composition, 2K resolution."
    )),
    ("classic-sunday-comic-ink-wash", (
        "A single illustrated comic book page in the warm classic American "
        "Sunday-newspaper-comic style of Bill Watterson and Berkeley Breathed "
        "— confident expressive black-ink contour drawing with light watercolor "
        "wash fills, friendly Sunday-paper palette of cream paper, warm "
        "yellow, sky blue, soft red, sap green, and grounded earth tones, "
        "expressive cartoon figures with warm relatable faces, classic "
        "American comic-strip pacing and composition, generic American "
        "domestic-scam scenes (kitchen counter, drugstore gift-card rack, "
        "retail checkout). Universally familiar Americana that reads as "
        "friendly and trustworthy across all ages. Showing four sequential "
        "panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the "
        "upper-left corner of each panel, separated by thin black panel "
        "borders with narrow cream gutters. Each panel contains one clean "
        "white rounded speech bubble with a small pointer tail, holding short "
        "printed English dialogue in simple black comic lettering — text "
        "must be legible, in English only, and correctly spelled. Square 1:1 "
        "composition, 2K resolution."
    )),
]


def build_prompt(style_block: str) -> str:
    char = CHARACTERS["margie"]
    return f"{style_block}\n\nCHARACTER: {char}\n\n{GENERIC_SCENE}"


def generate_one(slug: str, prompt: str, ws: str, r2: str) -> tuple[str, str]:
    body = {"prompt": prompt, "aspect_ratio": "1:1", "resolution": "2k", "output_format": "jpeg"}
    tid = submit_nbp(body, T2I_EP, ws)
    if not tid:
        return slug, "FAIL: submit"
    raw_url = poll_nbp(tid, ws, timeout=600)
    if not raw_url:
        return slug, "FAIL: poll"
    out = OUT_DIR / f"everywhere-{slug}.jpg"
    ok, note = download_verify(raw_url, out)
    if not ok:
        return slug, f"FAIL: dl {note}"
    r2_key = f"scam-comics/_everywhere/style-tests/{slug}.jpg"
    if not upload_r2(out, r2_key, r2):
        return slug, "FAIL: r2"
    return slug, f"https://img.tabiji.ai/{r2_key}"


def main():
    ws = _keychain("wavespeed-api-key")
    r2 = _keychain("cloudflare-api-token")
    if not ws or not r2:
        print("ERROR: missing creds", flush=True)
        sys.exit(1)

    print(f"Submitting {len(CANDIDATES)} everywhere-style bake-off generations...", flush=True)
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
