#!/usr/bin/env python3
"""Generate India book front + back hero illustrations via Wavespeed.

Output (local + R2):
- book-india/assets/svg/front.jpg
- book-india/assets/svg/back.jpg
- R2: scam-comics/in/book/front.jpg + back.jpg (audit copy)

Style: Amar Chitra Katha 1970s-80s — same as the 60 comics.
Aspect ratio: 2:3 (closest standard portrait to book 5:8). The SVG
uses preserveAspectRatio="xMidYMid slice" to fit either way.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent.parent / "scripts" / "comic-pipeline"))

from generate import (  # noqa: E402
    submit_nbp, poll_nbp, download_verify, upload_r2, _keychain, T2I_EP,
)
from cast import CHARACTERS  # noqa: E402

OUT_DIR = _HERE.parent / "assets" / "svg"
OUT_DIR.mkdir(parents=True, exist_ok=True)

STYLE_BLOCK = (
    "A single illustrated book-cover image in the iconic Amar Chitra Katha "
    "Indian comic-book style of the Anant Pai 1970s-80s tradition — bold "
    "confident black ink linework with decisive brush-tapered contours, flat "
    "primary-color cel-shaded fills with minimal halftone, saturated four-color "
    "newsprint palette of saffron orange, peacock blue, vermilion red, leaf "
    "green, sunflower yellow, and ivory cream, cinematic three-quarter staging, "
    "ethnographically specific Indian costuming and detail, subtle 1970s-print "
    "color-separation feel. Single hero scene with NO panel grid, NO panel "
    "numbers, NO speech bubbles, NO text or caption banner anywhere — this is "
    "a single full-bleed illustration intended to be a book cover background. "
    "Tall vertical composition with sky-heavy upper third (room for title "
    "overlay later), middle third for the main scene, lower third for "
    "foreground detail. 2K resolution."
)

FRONT_SCENE = (
    f"{STYLE_BLOCK}\n\n"
    f"CHARACTER: {CHARACTERS['margie']}\n\n"
    "SCENE: Margie at the east-gate approach to the Taj Mahal at golden-hour "
    "dawn, framed three-quarter from behind-and-side so her hat and silver "
    "hair are visible. She is holding her wheeled suitcase and looking down "
    "toward an Indian autorickshaw driver in a faded button-down shirt who "
    "stands beside his green-and-yellow autorickshaw at the foreground curb, "
    "smiling broadly with one hand gesturing toward the rickshaw in a 'free "
    "tour' invitation. Mid-ground and central focal element: the iconic white "
    "marble Taj Mahal in radiant golden-dawn light, with its main dome and "
    "four minarets reflected in the long water channel of the Charbagh "
    "garden in front. Background: a warm saffron sky fading to peacock blue "
    "with thin pink wisps of cloud. The framing leaves the upper third of "
    "the canvas mostly sky, the middle third dominated by the Taj, and the "
    "lower third holding Margie and the autorickshaw driver. Tall vertical "
    "(book-cover aspect)."
)

BACK_SCENE = (
    f"{STYLE_BLOCK}\n\n"
    f"CHARACTER: {CHARACTERS['priya']}\n\n"
    "SCENE: Priya standing on a narrow Jaipur lane in front of the iconic "
    "pink-sandstone Hawa Mahal facade in vivid afternoon sun. She is in "
    "three-quarter view, looking skeptically at an Indian autorickshaw "
    "driver leaning out of his green-and-yellow auto-rickshaw at the curb "
    "who is pitching her with a wide grin and gesturing down the lane "
    "toward an unseen 'cousin's silk emporium.' Mid-ground and central "
    "focal element: the Hawa Mahal's distinctive five-story pink-sandstone "
    "honeycomb facade — hundreds of small jharokha windows in stacked rows, "
    "ornamental arches, the dome-finials at the top — catching warm "
    "late-afternoon Jaipur light. Background: a dusty saffron-and-rose sky "
    "with a hint of haze. The framing leaves the upper third mostly sky, "
    "the middle third dominated by the Hawa Mahal facade, and the lower "
    "third holding Priya and the rickshaw driver. The composition reads "
    "as quieter and more reflective than the front cover. Tall vertical "
    "(book-cover aspect)."
)


def generate(slug: str, prompt: str, ws: str, r2: str) -> str:
    body = {"prompt": prompt, "aspect_ratio": "2:3", "resolution": "2k", "output_format": "jpeg"}
    tid = submit_nbp(body, T2I_EP, ws)
    if not tid:
        return f"FAIL submit {slug}"
    raw_url = poll_nbp(tid, ws, timeout=600)
    if not raw_url:
        return f"FAIL poll {slug}"
    out = OUT_DIR / f"{slug}.jpg"
    ok, note = download_verify(raw_url, out)
    if not ok:
        return f"FAIL dl {slug}: {note}"
    r2_key = f"scam-comics/in/book/{slug}.jpg"
    if not upload_r2(out, r2_key, r2):
        return f"FAIL r2 {slug}"
    return f"ok {slug} ({note}) → https://img.tabiji.ai/{r2_key}"


def main() -> int:
    ws = _keychain("wavespeed-api-key")
    r2 = _keychain("cloudflare-api-token")
    if not ws or not r2:
        print("missing creds")
        return 1
    print(generate("front", FRONT_SCENE, ws, r2))
    print(generate("back", BACK_SCENE, ws, r2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
