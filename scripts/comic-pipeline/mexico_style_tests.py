#!/usr/bin/env python3
"""Generate 5 distinct Mexican-style comic test images for style-lock selection.

Holds the scene/script/character constant — only the visual STYLE block varies —
so we can compare apples-to-apples and pick the pilot for Mexico scam comics.

Test scene: Priya at Mexico City Benito Juárez Airport (AICM) being hustled
by an unofficial "taxi amarillo" driver offering a 600-peso flat fare while
the official Sitio 300 counter is right behind. Standard 4-panel cautionary
comic format matching the v2 pipeline output.

Outputs:
- Local JPGs: /tmp/mexico-style-tests/<N>-<slug>.jpg
- R2: https://img.tabiji.ai/scam-comics/mx/style-tests/<N>-<slug>.jpg
"""
from __future__ import annotations

import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import (  # noqa: E402
    T2I_EP, download_verify, poll_nbp, submit_nbp, upload_r2, _keychain,
)
from cast import CHARACTERS  # noqa: E402

CHARACTER = CHARACTERS["priya"]

SCENE_SCRIPT = """CHARACTER (appears in every panel, consistent across all four):
""" + CHARACTER + """

SCAM CONTEXT: Mexico City Benito Juárez International Airport (AICM) taxi overcharge — unofficial drivers intercept arrivals with inflated flat fares while the official authorized-taxi counter sells pre-paid tickets steps away.

PANEL 1 — Just past the AICM arrivals customs door. An unofficial driver in a yellow cap waves at Priya and gestures toward the curb. Airport signage visible in Spanish. SPEECH BUBBLE: "Taxi, señora? Six hundred pesos!"

PANEL 2 — Priya glances past him and sees a clearly-marked "SITIO 300 TAXIS AUTORIZADOS" counter inside the terminal with a posted fare board. She points at it with her phone. SPEECH BUBBLE: "The official counter is right there."

PANEL 3 — Priya at the authorized Sitio counter, a uniformed clerk hands her a pre-paid taxi voucher. The posted rate card shows a 280-peso zone fare. SPEECH BUBBLE: "Two-eighty — half the price."

PANEL 4 — Priya in the back of an official white-and-green authorized taxi with a visible meter and ID card on the dash, heading into the city. SPEECH BUBBLE: "Always the authorized counter, never the curb."
"""

STYLES: list[dict[str, str]] = [
    {
        "slug": "1-posada-calavera-engraving",
        "label": "José Guadalupe Posada calavera engraving",
        "prompt": (
            "A single illustrated comic book page in the turn-of-the-20th-century Mexican "
            "engraving style of José Guadalupe Posada — bold confident black-ink relief-print "
            "linework with fine parallel hatching for shadow, a slightly-folk woodcut feeling, "
            "warm newsprint cream paper background with visible paper grain, occasional solid "
            "black spot areas, figures rendered with expressive faces and the characteristic "
            "Calavera-broadsheet editorial-cartoon energy, subtle hand-aged border ornament, "
            "turn-of-the-century Mexico City popular-press aesthetic. Showing four sequential "
            "panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left "
            "corner of each panel, separated by thin black panel borders with narrow cream "
            "gutters. Each panel contains one clean white rounded speech bubble with a small "
            "pointer tail, holding short printed English dialogue in simple black comic "
            "lettering — text must be legible, in English only, and correctly spelled. Square "
            "1:1 composition, 2K resolution."
        ),
    },
    {
        "slug": "2-diego-rivera-muralism",
        "label": "Diego Rivera / Orozco mural-fresco",
        "prompt": (
            "A single illustrated comic book page in the bold Mexican-muralist style of Diego "
            "Rivera and José Clemente Orozco — simplified rounded figures with strong "
            "geometric volume, warm earth-tone fresco palette of terracotta red, burnt sienna, "
            "dusty cobalt blue, mustard ochre, and deep olive green with soft cream "
            "highlights, confident dark outline, subtle painterly plaster texture as if "
            "painted on a wall, social-realist Mexican-1920s dignity in the figures, "
            "considered architectural backdrops with strong horizontal composition. Showing "
            "four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in "
            "the upper-left corner of each panel, separated by thin dark-terracotta panel "
            "borders with narrow cream-plaster gutters. Each panel contains one clean white "
            "rounded speech bubble with a small pointer tail, holding short printed English "
            "dialogue in simple black comic lettering — text must be legible, in English "
            "only, and correctly spelled. Square 1:1 composition, 2K resolution."
        ),
    },
    {
        "slug": "3-loteria-card-tarjeta",
        "label": "Lotería card (Don Clemente tarjeta)",
        "prompt": (
            "A single illustrated comic book page rendered in the iconic Mexican Lotería card "
            "(Don Clemente tarjeta) style — flat bright saturated colors (chili red, marigold "
            "yellow, sky blue, cactus green, and ivory white) with bold clean black outline, "
            "naive-folk figure proportions, centered iconic compositions on each panel, "
            "decorative thin black ornamental frame around every panel evoking the classic "
            "Lotería deck, each panel reading like a small cautionary Lotería tarjeta, warm "
            "cream paper background with a subtle printing-grain texture. Showing four "
            "sequential panels arranged in a 2x2 grid with small Lotería-style card numbers "
            "1, 2, 3, 4 in the upper-left corner of each panel, separated by narrow cream "
            "gutters. Each panel contains one clean white rounded speech bubble with a small "
            "pointer tail, holding short printed English dialogue in simple black lettering "
            "— text must be legible, in English only, and correctly spelled. Square 1:1 "
            "composition, 2K resolution."
        ),
    },
    {
        "slug": "4-ex-voto-retablo-folk",
        "label": "Ex-voto retablo folk devotional",
        "prompt": (
            "A single illustrated comic book page rendered as a traditional Mexican ex-voto "
            "retablo painting — small folk-devotional narrative scenes painted as if on aged "
            "tin-metal plaques, bright saturated folk-palette of marigold, cobalt, cochineal "
            "red, turquoise, and cream with deliberate naive perspective and charmingly "
            "imperfect proportions, visible hammered-tin surface texture and gentle metallic "
            "sheen, faint aged varnish patina, hand-painted border lines, characteristic "
            "ex-voto narrative storytelling tone where ordinary people recount close calls. "
            "Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, "
            "3, 4 in the upper-left corner of each panel, separated by thin dark-brown panel "
            "borders with narrow cream gutters. Each panel contains one clean white rounded "
            "speech bubble with a small pointer tail, holding short printed English dialogue "
            "in simple black lettering — text must be legible, in English only, and "
            "correctly spelled. Square 1:1 composition, 2K resolution."
        ),
    },
    {
        "slug": "5-oaxacan-alebrije-folk-pop",
        "label": "Oaxacan alebrije folk-pop patterning",
        "prompt": (
            "A single illustrated comic book page in a vibrant Oaxacan-folk-art style "
            "inspired by alebrije carvings — confident black ink outlines with flat "
            "saturated pop colors (hot pink, turquoise, marigold, emerald, violet), richly "
            "patterned clothing and backgrounds with intricate dot-and-line decoration "
            "reminiscent of copal-wood alebrije painting, naive folk figure proportions, "
            "decorative repeating motifs of zigzag, scallop, and spiral ornament, cream "
            "paper background with subtle grain, cheerful contemporary Oaxacan-handicraft "
            "tone. Showing four sequential panels arranged in a 2x2 grid with small numbers "
            "1, 2, 3, 4 in the upper-left corner of each panel, separated by thin black "
            "panel borders with narrow cream gutters. Each panel contains one clean white "
            "rounded speech bubble with a small pointer tail, holding short printed English "
            "dialogue in simple black comic lettering — text must be legible, in English "
            "only, and correctly spelled. Square 1:1 composition, 2K resolution."
        ),
    },
]


def generate_one(style: dict, ws_token: str, r2_token: str) -> dict:
    slug = style["slug"]
    out_path = Path(f"/tmp/mexico-style-tests/{slug}.jpg")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    full_prompt = (
        "STYLE:\n" + style["prompt"] + "\n\n"
        + "SCENE:\n" + SCENE_SCRIPT
    )
    body = {"prompt": full_prompt, "resolution": "2k"}

    tid = submit_nbp(body, T2I_EP, ws_token)
    if not tid:
        return {"slug": slug, "status": "submit_failed"}
    url = poll_nbp(tid, ws_token, timeout=600)
    if not url:
        return {"slug": slug, "status": "poll_failed"}
    ok, note = download_verify(url, out_path)
    if not ok:
        return {"slug": slug, "status": f"verify_failed: {note}", "url": url}
    r2_key = f"scam-comics/mx/style-tests/{slug}.jpg"
    if not upload_r2(out_path, r2_key, r2_token):
        return {"slug": slug, "status": "r2_upload_failed"}
    return {
        "slug": slug,
        "status": "ok",
        "bytes": out_path.stat().st_size,
        "r2": f"https://img.tabiji.ai/{r2_key}",
    }


def main() -> int:
    ws_token = _keychain("wavespeed-api-key")
    r2_token = _keychain("cloudflare-api-token")

    t0 = time.time()
    print(f"generating {len(STYLES)} mexico style tests (parallel)", flush=True)
    with ThreadPoolExecutor(max_workers=len(STYLES)) as ex:
        results = list(ex.map(lambda s: generate_one(s, ws_token, r2_token), STYLES))

    print(f"\ndone in {time.time()-t0:.0f}s\n", flush=True)
    for r in results:
        print(json.dumps(r), flush=True)

    bad = [r for r in results if r["status"] != "ok"]
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
