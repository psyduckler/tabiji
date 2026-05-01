#!/usr/bin/env python3
"""Malaysia style bake-off — 5 candidates, Margie at the Petronas Twin Towers
Skybridge fake-ticket tout scene. Modeled on bakeoff_costa_rica_2026_04_27.py.

Single shared scene + canonical Margie cast block; only the STYLE block varies
between candidates so differences are purely stylistic.
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

OUT_DIR = Path("/tmp/bakeoff-my-2026-04-28")
OUT_DIR.mkdir(exist_ok=True)

# Petronas Twin Towers Skybridge fake-ticket tout scene — KL's most iconic
# landmark, strong architectural test, two-character interaction with signage.
SCENE = (
    "SCENE:\n"
    "Panel 1: Margie in the underground concourse beneath Suria KLCC, the two "
    "glittering Petronas Twin Towers visible through the glass behind her. A "
    "tout in a cheap orange polo shirt holding a stack of laminated 'VIP "
    "SKYBRIDGE — TODAY' cards intercepts her path. Speech bubble (tout): "
    "\"Tickets sold out today! I have, RM 250!\"\n"
    "Panel 2: Margie holds up her phone showing the official "
    "petronastwintowers.com.my booking page with 'RM 98 — Available' slots; "
    "she points past him at the official 'PETRONAS TWIN TOWERS — TICKET "
    "COUNTER' sign across the concourse. Speech bubble (Margie): "
    "\"I'll buy at the counter — thanks.\"\n"
    "Panel 3: At the real Petronas ticket counter, a uniformed Petronas "
    "attendant in a navy uniform hands Margie a printed RM 98 Skybridge "
    "ticket. The Twin Towers visible through the floor-to-ceiling glass. "
    "Speech bubble (attendant): \"Skybridge at 11 — enjoy!\"\n"
    "Panel 4: Margie on the actual Skybridge between the Twin Towers, "
    "looking out at the Kuala Lumpur skyline through the slatted glass; "
    "her phone films a short video. Speech bubble (Margie): \"RM 98 "
    "official — never RM 250 from a stranger.\""
)

CANDIDATES = [
    ("1-lat-kampung-pen-and-ink", (
        "A single illustrated comic book page in the warm hand-drawn "
        "newspaper-cartoon style of Mohamad Nor Khalid (Datuk Lat), "
        "Malaysia's beloved national cartoonist behind 'Kampung Boy' and "
        "five decades of Berita Harian and New Straits Times daily strips "
        "— confident hand-drawn black-ink linework with rich crosshatched "
        "shading, gentle observational humor, soft round-faced characters "
        "with big expressive eyes, generous noses, and small smiles, "
        "everyday Malaysian street-life sensibility, warm off-white "
        "newsprint paper background with subtle grain, occasional muted "
        "watercolor wash in pale lemon, soft chili red, and faded banana "
        "yellow only when needed for emphasis, location-accurate Kuala "
        "Lumpur architecture (Petronas Twin Towers, Suria KLCC concourse, "
        "ticket counter signage) drawn with affectionate observed detail. "
        "Showing four sequential panels arranged in a 2x2 grid with small "
        "hand-drawn numbers 1, 2, 3, 4 in the upper-left corner of each "
        "panel, separated by thin hand-drawn black panel borders with "
        "narrow cream gutters. Each panel contains one clean white "
        "rounded speech bubble with a small pointer tail, holding short "
        "printed English dialogue in simple black hand-lettering — text "
        "must be legible, in English only, and correctly spelled. Square "
        "1:1 composition, 2K resolution."
    )),
    ("2-chuah-thean-teng-batik-painting", (
        "A single illustrated comic book page in the bold batik-painting "
        "style pioneered by Chuah Thean Teng, the Penang master who "
        "elevated wax-resist batik into Malaysian fine art — flat saturated "
        "hand-painted color shapes with confident black wax-line outlines, "
        "deep dye palette of indigo, terracotta, ochre, jade green, "
        "turmeric gold, crimson, and cream, signature wax-crackle "
        "fracture texture across every painted surface (the cracked "
        "veining you get when wax breaks before dye), stylized rounded "
        "human figures with simple expressive faces and elongated graceful "
        "limbs, decorative tropical foliage borders (palm fronds, hibiscus, "
        "banana leaves) framing each panel, location-accurate Kuala Lumpur "
        "architecture (Petronas Twin Towers, Suria KLCC, ticket counter) "
        "rendered as bold flat dyed-fabric shapes. Showing four sequential "
        "panels arranged in a 2x2 grid with small hand-painted numbers "
        "1, 2, 3, 4 in the upper-left corner of each panel, separated by "
        "thin black wax-line borders with narrow cream gutters. Each "
        "panel contains one clean white rounded speech bubble with a "
        "small pointer tail, holding short printed English dialogue in "
        "simple black comic lettering — text must be legible, in English "
        "only, and correctly spelled. Square 1:1 composition, 2K "
        "resolution."
    )),
    ("3-wayang-kulit-shadow-puppet", (
        "A single illustrated comic book page rendered as traditional "
        "Kelantanese wayang kulit shadow-puppet theatre — figures rendered "
        "as silhouetted dalang-carved buffalo-leather puppets in deep "
        "sepia-black and burnt umber against a warm amber-and-ochre "
        "backlit parchment screen, with intricate fretwork-carved figure "
        "edges showing lacy filigree perforations, decorative Kelantanese "
        "flourishes along puppet bodies, side-profile staging in the "
        "classical wayang manner, stylized tropical vegetation silhouettes "
        "(palm fronds, banana leaves, kampung roof-lines) layered in the "
        "foreground, the silhouetted Petronas Twin Towers standing in the "
        "background as recognizable Kuala Lumpur landmarks, subtle "
        "flickering oil-lamp warmth across the screen, classical "
        "shadow-play aesthetic merged with modern sequential-comic layout. "
        "Showing four sequential panels arranged in a 2x2 grid with small "
        "hand-painted numbers 1, 2, 3, 4 in the upper-left corner of each "
        "panel, separated by thin dark-brown panel borders with narrow "
        "amber gutters. Each panel contains one clean white rounded speech "
        "bubble with a small pointer tail, holding short printed English "
        "dialogue in simple black comic lettering — text must be legible, "
        "in English only, and correctly spelled. Square 1:1 composition, "
        "2K resolution."
    )),
    ("4-zacharevic-penang-mural", (
        "A single illustrated comic book page in the iconic photo-real "
        "street-mural style of Ernest Zacharevic, the Lithuanian-Malaysian "
        "muralist whose George Town pieces ('Little Children on a "
        "Bicycle', 'Boy on Motorbike') made Penang's heritage walls "
        "world-famous — hyper-realistic painted human figures with "
        "lifelike skin and clothing rendered in loose confident brushwork, "
        "minimal painted environment that lets the subject breathe, "
        "muted urban palette of weathered sepia, mustard yellow, faded "
        "teal, brick rust, dusty cream, and shadow charcoal, occasional "
        "pop of red or saffron for accent, characters often interacting "
        "with real-world props (a bicycle leaning against the wall, a "
        "doorway, a sign), visible wall texture and brick or peeling "
        "plaster behind, location-accurate Kuala Lumpur architecture "
        "(Petronas Twin Towers visible through windows, Suria KLCC ticket "
        "counter, official signage) rendered with painterly observed "
        "detail, contemporary Malaysian street-art sensibility. Showing "
        "four sequential panels arranged in a 2x2 grid with small numbers "
        "1, 2, 3, 4 in the upper-left corner of each panel, separated by "
        "thin black panel borders with narrow off-white gutters. Each "
        "panel contains one clean white rounded speech bubble with a "
        "small pointer tail, holding short printed English dialogue in "
        "simple black comic lettering — text must be legible, in English "
        "only, and correctly spelled. Square 1:1 composition, 2K "
        "resolution."
    )),
    ("5-peranakan-nyonya-pastel", (
        "A single illustrated comic book page in a warm Peranakan / "
        "Nyonya heritage illustration style drawn from the Straits-"
        "Chinese aesthetic of Penang and Melaka shophouses — soft pastel "
        "palette of porcelain pink, mint green, butter yellow, sky blue, "
        "powder lavender, with cream backgrounds and delicate gilt "
        "accents, decorative Peranakan tile and batik motif borders "
        "around each panel (phoenix, peony, butterfly, geometric chevron, "
        "and lotus patterns rendered as flat dyed shapes), gentle fine "
        "black ink line drawing with transparent watercolor wash interior, "
        "rounded friendly characters with soft expressive faces, "
        "location-accurate Kuala Lumpur architecture (Petronas Twin "
        "Towers visible through ornate windows, Suria KLCC ticket "
        "counter) rendered alongside heritage-shophouse-inspired interior "
        "framing, gentle Peranakan storybook composition with visible "
        "watercolor texture. Showing four sequential panels arranged in "
        "a 2x2 grid with small hand-painted numbers 1, 2, 3, 4 in the "
        "upper-left corner of each panel, separated by thin gilt panel "
        "borders inside the Peranakan tile rim with narrow cream gutters. "
        "Each panel contains one clean white rounded speech bubble with "
        "a small pointer tail, holding short printed English dialogue in "
        "simple black comic lettering — text must be legible, in English "
        "only, and correctly spelled. Square 1:1 composition, 2K "
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
    out = OUT_DIR / f"my-{slug}.jpg"
    ok, note = download_verify(raw_url, out)
    if not ok:
        return slug, f"FAIL: dl {note}"
    r2_key = f"scam-comics/my/style-tests/{slug}.jpg"
    if not upload_r2(out, r2_key, r2):
        return slug, "FAIL: r2"
    return slug, f"https://img.tabiji.ai/{r2_key}"


def main():
    ws = _keychain("wavespeed-api-key")
    r2 = _keychain("cloudflare-api-token")
    if not ws or not r2:
        print("ERROR: missing creds", flush=True)
        sys.exit(1)

    print(f"Submitting {len(CANDIDATES)} Malaysia style bake-off generations...", flush=True)
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
