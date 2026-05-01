#!/usr/bin/env python3
"""Costa Rica style bake-off — 5 candidates, anchored on the iconic Manuel Antonio
fake-park-ranger scam scene with Margie. Run via the v2 pipeline's T2I endpoint
so each style stands on its own without an anchor image biasing the result.
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

OUT_DIR = Path("/tmp/bakeoff-cr-2026-04-27")
OUT_DIR.mkdir(exist_ok=True)

# Manuel Antonio fake-park-ranger scene — the single most documented Costa Rica
# tourist scam (US Embassy San José Security Alert, 2025-11-25). Same scene for
# all 5 styles so differences are purely stylistic.
SCENE = (
    "SCENE:\n"
    "Panel 1: Margie at the wheel of a small white rental SUV on a jungle-flanked "
    "two-lane road approaching Manuel Antonio National Park, distant blue Pacific "
    "visible past the palms. A man in a fake khaki 'park ranger' uniform with a "
    "cardboard sign that reads 'PARK FULL' steps into the road and waves her "
    "down. Speech bubble (fake ranger): \"Park full — park here!\"\n"
    "Panel 2: The fake ranger leans into Margie's driver window holding a fake "
    "ticket scanner; Margie holds up her phone showing an official SINAC ticket "
    "with a green QR code. Speech bubble (Margie): \"I booked online already.\"\n"
    "Panel 3: The fake ranger looks angry; two more khaki-clad accomplices "
    "appear behind him in the road. Margie's expression turns wary. Speech "
    "bubble (fake ranger): \"Then I cancel your ticket!\"\n"
    "Panel 4: Margie drives slowly past the scammers toward the real SINAC "
    "turnstile gate visible ahead at the end of the road; the fake rangers "
    "shrink in her side mirror. Speech bubble (Margie): \"Real gate's past "
    "the scammers.\""
)

CANDIDATES = [
    ("1-sarchi-carreta-folk-painting", (
        "A single illustrated comic book page in the traditional Costa Rican "
        "Sarchí oxcart (carreta) folk-painting style — UNESCO-recognized "
        "hand-painted decorative tradition of brightly-colored geometric "
        "mandalas and concentric-circle 'rosetones' on cream wood, vivid "
        "saturated primary palette of fire-engine red, royal blue, "
        "marigold yellow, leaf green, and cream, confident black outline "
        "brushwork around every shape, decorative repeating geometric "
        "motifs (concentric circles, points, stars, scalloped petal "
        "borders) framing each panel as if painted on the wooden side of a "
        "carreta, naive-folk figure proportions with simple expressive "
        "faces, stylized location-accurate Costa Rican rainforest backdrop "
        "(palm silhouettes, distant volcanic cone, blue Pacific horizon). "
        "Showing four sequential panels arranged in a 2x2 grid with small "
        "hand-painted numbers 1, 2, 3, 4 in the upper-left corner of each "
        "panel, separated by decorative carreta-style geometric borders "
        "with narrow cream gutters. Each panel contains one clean white "
        "rounded speech bubble with a small pointer tail, holding short "
        "printed English dialogue in simple black comic lettering — text "
        "must be legible, in English only, and correctly spelled. Square "
        "1:1 composition, 2K resolution."
    )),
    ("2-1950s-pan-am-tropical-deco", (
        "A single illustrated comic book page in the vivid 1950s tropical "
        "art-deco travel-poster style used by Pan American Airways for "
        "Central America routes — bold flat simplified graphic shapes "
        "with crisp black outlines, streamlined modernist composition, "
        "sun-drenched tropical palette of deep turquoise Pacific, emerald "
        "jungle, volcano red-orange, banana yellow, tropical magenta, and "
        "cream, stylized 1950s travelers and location-accurate Costa "
        "Rican scenery (Arenal volcano cone, Manuel Antonio beach coves, "
        "palm silhouettes, SINAC ranger stations, carreta oxcart wheels, "
        "toucans and sloths — whichever fits the scam's actual location), "
        "confident hand-stenciled travel-poster typography, cheerful "
        "mid-century advertising optimism, clean legible layout. Showing "
        "four sequential panels arranged in a 2x2 grid with small numbers "
        "1, 2, 3, 4 in the upper-left corner of each panel, separated by "
        "thin black panel borders with narrow cream gutters. Each panel "
        "contains one clean white rounded speech bubble with a small "
        "pointer tail, holding short printed English dialogue in art-deco "
        "stencil-style black lettering — text must be legible, in English "
        "only, and correctly spelled. Do NOT add any footer or caption "
        "banner outside the four panels — the comic must be exactly the "
        "2x2 grid with no additional text, tagline, or banner below. "
        "Square 1:1 composition, 2K resolution."
    )),
    ("3-pre-columbian-diquis-boruca-textile", (
        "A single illustrated comic book page rendered in a stylized "
        "pre-Columbian Costa Rican indigenous heritage style fusing "
        "Diquís stone-sphere carved-line aesthetics with Boruca textile "
        "weaving motifs — flat earthy palette of terracotta clay, deep "
        "ochre, jet black, cream linen, jade green, and a single accent "
        "of carved-jade turquoise; figures rendered as flattened "
        "silhouettes with carved-stone geometric simplification, framed "
        "by woven Boruca textile pattern borders showing repeating "
        "stylized jaguar, spider, and harpy-eagle motifs, decorative "
        "concentric carved-stone circles in panel corners evoking the "
        "Diquís spheres, sparse minimalist composition with each "
        "important shape carved as if into stone, ancient indigenous "
        "Costa Rican manuscript-meets-textile feel, tropical jungle and "
        "Pacific coastline rendered as flat woven shapes. Showing four "
        "sequential panels arranged in a 2x2 grid with small carved "
        "numerals 1, 2, 3, 4 in the upper-left corner of each panel, "
        "separated by thin woven-textile borders with narrow cream "
        "gutters. Each panel contains one clean white rounded speech "
        "bubble with a small pointer tail, holding short printed English "
        "dialogue in simple black lettering — text must be legible, in "
        "English only, and correctly spelled. Square 1:1 composition, "
        "2K resolution."
    )),
    ("4-tico-naif-tropical-primitivist", (
        "A single illustrated comic book page in the lush Costa Rican "
        "naïf primitivist painting tradition — saturated tropical rainforest "
        "alive with biodiversity, bold flat hand-painted shapes with confident "
        "black outline, layered green canopy of emerald, lime, sage, and "
        "jungle-shadow teal, accents of macaw scarlet, toucan yellow, hibiscus "
        "pink, and Pacific cobalt, decorative heart-of-palm fronds and "
        "bromeliads at panel edges, hidden sloths, frogs, and toucans "
        "tucked into the foliage as joyful Easter eggs, naive-folk figure "
        "proportions with friendly oversized eyes and simple expressive "
        "faces, dense joyful 'pura vida' tico storybook composition with "
        "every surface filled with hand-painted biodiversity, warm "
        "equatorial sunlight. Showing four sequential panels arranged in "
        "a 2x2 grid with small hand-painted numbers 1, 2, 3, 4 in the "
        "upper-left corner of each panel, separated by thin black panel "
        "borders with narrow cream gutters. Each panel contains one "
        "clean white rounded speech bubble with a small pointer tail, "
        "holding short printed English dialogue in simple black comic "
        "lettering — text must be legible, in English only, and "
        "correctly spelled. Square 1:1 composition, 2K resolution."
    )),
    ("5-botanical-pen-and-watercolor-journal", (
        "A single illustrated comic book page in a contemporary botanical "
        "pen-and-watercolor travel-journal style — confident fine "
        "black-ink contour drawing with delicate cross-hatching, "
        "transparent watercolor washes with visible bleed and paper grain, "
        "off-white sketchbook background with subtle cream texture, "
        "warm Costa Rican palette of cream, leaf green, sky blue, "
        "terracotta, soft mustard, and macaw scarlet, friendly observed "
        "characters with everyday realism, location-accurate Costa Rican "
        "scenery (jungle-flanked road to Manuel Antonio, palm canopy, "
        "distant Pacific, SINAC ranger station, volcanic silhouette, "
        "small biodiversity vignettes — sloth on a branch, hummingbird, "
        "passion-flower — drawn at panel edges as journal margin "
        "annotations), modern accessible naturalist-illustration "
        "sensibility with the warm sketchbook feel of a contemporary "
        "Costa Rican travel-journal artist. Showing four sequential "
        "panels arranged in a 2x2 grid with small hand-drawn numbers "
        "1, 2, 3, 4 in the upper-left corner of each panel, separated "
        "by hand-drawn pen panel borders with narrow off-white gutters. "
        "Each panel contains one clean white rounded speech bubble with "
        "a small pointer tail, holding short printed English dialogue in "
        "simple black hand-lettering — text must be legible, in English "
        "only, and correctly spelled. Square 1:1 composition, 2K resolution."
    )),
]


def build_prompt(style_block: str) -> str:
    char = CHARACTERS["margie"]
    return f"{style_block}\n\nCHARACTER: {char}\n\n{SCENE}"


def generate_one(slug: str, prompt: str, ws: str, r2: str) -> tuple[str, str]:
    body = {"prompt": prompt, "aspect_ratio": "1:1", "resolution": "2k", "output_format": "jpeg"}
    tid = submit_nbp(body, T2I_EP, ws)
    if not tid:
        return slug, "FAIL: submit"
    raw_url = poll_nbp(tid, ws, timeout=600)
    if not raw_url:
        return slug, "FAIL: poll"
    out = OUT_DIR / f"cr-{slug}.jpg"
    ok, note = download_verify(raw_url, out)
    if not ok:
        return slug, f"FAIL: dl {note}"
    r2_key = f"scam-comics/cr/style-tests/{slug}.jpg"
    if not upload_r2(out, r2_key, r2):
        return slug, "FAIL: r2"
    return slug, f"https://img.tabiji.ai/{r2_key}"


def main():
    ws = _keychain("wavespeed-api-key")
    r2 = _keychain("cloudflare-api-token")
    if not ws or not r2:
        print("ERROR: missing creds", flush=True)
        sys.exit(1)

    print(f"Submitting {len(CANDIDATES)} Costa Rica style bake-off generations...", flush=True)
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
