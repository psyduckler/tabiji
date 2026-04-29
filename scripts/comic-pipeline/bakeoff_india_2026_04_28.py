#!/usr/bin/env python3
"""India style bake-off — 5 candidates anchored on the Delhi 'Fake Government
Tourist Office' scene with Margie. Identical scene across all 5 so visual
variance is purely stylistic. Mirrors the Costa Rica bake-off pattern.
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

OUT_DIR = Path("/tmp/bakeoff-india-2026-04-28")
OUT_DIR.mkdir(exist_ok=True)

SCENE = (
    "SCENE:\n"
    "Panel 1: Margie has just stepped off the overnight train at New Delhi "
    "Railway Station and stands on the crowded platform under an arched "
    "train-shed roof, pulling a small wheeled suitcase, looking slightly "
    "lost. A friendly Indian man in a navy polo shirt with a clipboard and "
    "a lanyard approaches her from the side. Speech bubble (tout): \"Need "
    "help? Free Tourism office!\"\n"
    "Panel 2: The tout walks Margie down a narrow Paharganj lane lined "
    "with hanging shop boards, leading her toward a small storefront with "
    "a red 'INDIA TOURISM' sign above the door. Margie looks faintly "
    "uncertain. Speech bubble (Margie): \"Are you sure it's official?\"\n"
    "Panel 3: Inside the small office — an Indian man in a tan suit sits "
    "behind a wooden desk covered in tour brochures, with a wall map of "
    "India behind him. Margie stands in front of the desk holding a "
    "printed hotel confirmation; the suited man gestures at a glossy "
    "brochure. Speech bubble (suited man): \"Hotel canceled — package "
    "$400!\"\n"
    "Panel 4: Margie walks calmly away from the storefront down the "
    "Paharganj lane, holding up her phone which clearly displays a Google "
    "Maps screen with a red pin labeled '88 Janpath'. The fake office "
    "sign shrinks behind her in the background. Speech bubble (Margie): "
    "\"Real office is 88 Janpath.\""
)

CANDIDATES = [
    ("1-mughal-miniature", (
        "A single illustrated comic book page in classical Mughal miniature "
        "painting style of the Akbar-Jahangir-Shah Jahan imperial court "
        "ateliers c. 1560-1700 — flat picture plane with no Western "
        "perspective, figures stacked vertically through the panel as if "
        "seen from a slightly elevated viewpoint, opaque gouache fills "
        "with fine black contour lines and no cross-hatching, jewel-tone "
        "palette of vermilion, lapis blue, malachite green, saffron "
        "yellow, ivory cream, and burnished gold-leaf accents, faces in "
        "delicate three-quarter profile with almond-shaped eyes and "
        "refined Mughal-court features, decorative architectural framing "
        "with arched niches and floral cartouches, courtly attention to "
        "fabric pattern detail (paisley, brocade, fine stripe), "
        "location-accurate stylized Delhi setting (sandstone Mughal-arched "
        "facade for the NDLS train shed, narrow Paharganj lane with "
        "chai-stall and hanging shop boards, fake India Tourism office "
        "rendered with court-painting elegance, modern travel clothing "
        "and suit-and-tie costuming preserved). Showing four sequential "
        "panels arranged in a 2x2 grid with small gold-painted "
        "Indo-Persian numerals 1, 2, 3, 4 in the upper-left corner of "
        "each panel, separated by ornate floral-cartouche dividers with "
        "narrow ivory gutters. Each panel contains one clean white "
        "rounded speech bubble with a small pointer tail, holding short "
        "printed English dialogue in simple black comic lettering — text "
        "must be legible, in English only, and correctly spelled. Do "
        "NOT add any footer or caption banner outside the four panels — "
        "the comic must be exactly the 2x2 grid with no additional text, "
        "tagline, or banner below. Square 1:1 composition, 2K resolution."
    )),
    ("2-madhubani-mithila-folk", (
        "A single illustrated comic book page in traditional Madhubani / "
        "Mithila folk-painting style of Bihar — heavy confident black "
        "outline brushwork with no shading and no cross-hatching, "
        "all-over decorative pattern fill (fish-scale, lattice, lotus "
        "rosette, sun-rays, paisley) leaving no negative space, earthy "
        "mineral palette of lampblack, vermilion red, indigo blue, "
        "turmeric ochre, leaf green, and natural cream paper ground, "
        "stylized doe-eyed figures shown frontal or in strict profile "
        "with simplified geometric proportions, decorative double-line "
        "panel borders with repeating Mithila folk motifs, "
        "location-accurate stylized Delhi setting (NDLS train station "
        "rendered in Madhubani architectural geometry, Paharganj lane "
        "stalls flattened into folk-pattern shapes, fake India Tourism "
        "office reduced to symbolic desk and wall map, modern travel "
        "clothing simplified into Mithila figure conventions while "
        "preserving the protagonist's recognizable hat, glasses, and "
        "scarf). Showing four sequential panels arranged in a 2x2 grid "
        "with small hand-brushed numbers 1, 2, 3, 4 in the upper-left "
        "corner of each panel, separated by traditional double-line "
        "Madhubani borders with narrow cream gutters. Each panel "
        "contains one clean white rounded speech bubble with a small "
        "pointer tail, holding short printed English dialogue in simple "
        "black hand-lettering — text must be legible, in English only, "
        "and correctly spelled. Do NOT add any footer or caption banner "
        "outside the four panels — the comic must be exactly the 2x2 "
        "grid with no additional text, tagline, or banner below. Square "
        "1:1 composition, 2K resolution."
    )),
    ("3-kalighat-bazaar-watercolor", (
        "A single illustrated comic book page in late-19th-century "
        "Calcutta Kalighat bazaar-painting style — fast confident broad "
        "black brush outline laid over flat watercolor wash, loose "
        "gestural brushwork in the tradition of bazaar-stall paintings "
        "sold cheap to pilgrims around Kalighat temple, limited bazaar "
        "palette of red lake, indigo, yellow ochre, leaf green, "
        "lampblack, and warm cream paper ground, two- and three-figure "
        "compositions with mild satirical caricature built into the line "
        "(the tout's smirk, the mark's startled posture), stylized "
        "expressive faces with slightly enlarged eyes and fluid drapery, "
        "sparse uncluttered backgrounds with only essential setting "
        "elements suggested in a single wash, location-accurate Delhi "
        "backdrop (NDLS arched portico suggested in three brushstrokes, "
        "Paharganj shop-board signage in Devanagari and Latin script, "
        "fake India Tourism office interior shown with one desk and one "
        "wall map). Showing four sequential panels arranged in a 2x2 "
        "grid with small hand-brushed numbers 1, 2, 3, 4 in the "
        "upper-left corner of each panel, separated by thin black brush "
        "borders with narrow cream gutters. Each panel contains one "
        "clean white rounded speech bubble with a small pointer tail, "
        "holding short printed English dialogue in simple black "
        "hand-lettering — text must be legible, in English only, and "
        "correctly spelled. Do NOT add any footer or caption banner "
        "outside the four panels — the comic must be exactly the 2x2 "
        "grid with no additional text, tagline, or banner below. Square "
        "1:1 composition, 2K resolution."
    )),
    ("4-ravi-varma-oleograph", (
        "A single illustrated comic book page in late-19th-century Raja "
        "Ravi Varma chromolithograph oleograph calendar-art style — "
        "Indian academic-realist subject matter rendered with European "
        "oil-painting technique, soft tonal modeling with subtle "
        "chiaroscuro on faces and fabric, theatrical staging with "
        "characters posed slightly toward the viewer as on a shallow "
        "proscenium stage, saturated oleograph palette of warm sepia "
        "background washes, ivory-cream skin tones, deep crimson and "
        "saffron textiles, emerald green, royal blue, and burnished "
        "bronze, emotive faces with expressive eyes and graceful "
        "gesturing hands, shallow Renaissance-style architectural "
        "perspective with arched stone backdrops, location-accurate "
        "Delhi setting (NDLS sandstone facade rendered with academic "
        "realism, Paharganj lane in 19th-century chromolithograph "
        "composition, fake India Tourism office interior with painted "
        "wall map of India and a brochure rack). Showing four "
        "sequential panels arranged in a 2x2 grid with small ornamented "
        "numerals 1, 2, 3, 4 in the upper-left corner of each panel, "
        "separated by thin gold-buff borders with narrow cream gutters. "
        "Each panel contains one clean white rounded speech bubble with "
        "a small pointer tail, holding short printed English dialogue in "
        "simple black serif lettering — text must be legible, in English "
        "only, and correctly spelled. Do NOT add any footer or caption "
        "banner outside the four panels — the comic must be exactly the "
        "2x2 grid with no additional text, tagline, or banner below. "
        "Square 1:1 composition, 2K resolution."
    )),
    ("5-amar-chitra-katha-comic", (
        "A single illustrated comic book page in the iconic Amar Chitra "
        "Katha Indian comic-book style of the Anant Pai 1970s-80s "
        "tradition — bold confident black ink linework with "
        "decisive brush-tapered contours, flat primary-color cel-shaded "
        "fills with minimal halftone or gradient, saturated four-color "
        "newsprint palette of saffron orange, peacock blue, vermilion "
        "red, leaf green, sunflower yellow, and ivory cream, cinematic "
        "three-quarter staging with dynamic close-ups and dramatic "
        "low-and-high angles, ethnographically specific costuming (cream "
        "linen for the tourist, polo and chinos for the tout, "
        "shirt-and-tie suit for the desk-man, Delhi train-station "
        "passengers and Paharganj street-vendors in the background), "
        "subtle 1970s-print color-separation feel, location-accurate "
        "Delhi backdrop (NDLS station portico with platform-board "
        "signage in English and Hindi, narrow Paharganj lane with "
        "hanging shop boards, fake India Tourism office interior with "
        "wooden desk, wall map of India, and brochure rack). Showing "
        "four sequential panels arranged in a 2x2 grid with small bold "
        "numbers 1, 2, 3, 4 in the upper-left corner of each panel, "
        "separated by thin black panel borders with narrow cream "
        "gutters. Each panel contains one clean white rounded speech "
        "bubble with a small pointer tail, holding short printed English "
        "dialogue in classic Amar Chitra Katha comic lettering — text "
        "must be legible, in English only, and correctly spelled. Do "
        "NOT add any footer or caption banner outside the four panels — "
        "the comic must be exactly the 2x2 grid with no additional "
        "text, tagline, or banner below. Square 1:1 composition, 2K "
        "resolution."
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
    out = OUT_DIR / f"in-{slug}.jpg"
    ok, note = download_verify(raw_url, out)
    if not ok:
        return slug, f"FAIL: dl {note}"
    r2_key = f"scam-comics/in/style-tests/{slug}.jpg"
    if not upload_r2(out, r2_key, r2):
        return slug, "FAIL: r2"
    return slug, f"https://img.tabiji.ai/{r2_key}"


def main():
    ws = _keychain("wavespeed-api-key")
    r2 = _keychain("cloudflare-api-token")
    if not ws or not r2:
        print("ERROR: missing creds", flush=True)
        sys.exit(1)

    print(f"Submitting {len(CANDIDATES)} India style bake-off generations...", flush=True)
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
