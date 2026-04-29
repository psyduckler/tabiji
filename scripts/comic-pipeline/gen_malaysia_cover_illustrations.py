#!/usr/bin/env python3
"""Generate the Malaysia book cover illustrations (front + back) in the locked
Peranakan/Nyonya pastel heritage style.

Outputs:
  book-malaysia/assets/svg/front.jpg — KL/Petronas hero scene
  book-malaysia/assets/svg/back.jpg  — Penang/Melaka heritage scene

Run: python3 scripts/comic-pipeline/gen_malaysia_cover_illustrations.py
"""
from __future__ import annotations

import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import (  # noqa: E402
    submit_nbp, poll_nbp, download_verify, _keychain, T2I_EP,
)

REPO = _HERE.parent.parent
OUT_DIR = REPO / "book-malaysia" / "assets" / "svg"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PERANAKAN_BASE = (
    "A vertical book-cover illustration in the Peranakan / Nyonya heritage "
    "style of Penang and Melaka — soft pastel palette of porcelain pink, "
    "mint green, butter yellow, sky blue, powder lavender, with cream "
    "backgrounds and delicate gilt accents. Decorative Peranakan tile and "
    "batik motif borders along the edges (phoenix, peony, butterfly, "
    "geometric chevron, and lotus patterns rendered as flat dyed shapes). "
    "Gentle fine black ink line drawing with transparent watercolor wash "
    "interior. Single scene, NO panel borders, NO speech bubbles, NO text, "
    "NO people in the foreground. Vertical portrait orientation. Lots of "
    "clean negative space in the upper third for a title overlay; richer "
    "architectural detail in the lower two-thirds. 1:1 square composition, "
    "2K resolution."
)

FRONT_PROMPT = PERANAKAN_BASE + (
    "\n\nSCENE: Kuala Lumpur at golden hour. The iconic Petronas Twin "
    "Towers stand tall in the center against a soft pastel-pink and "
    "sky-blue sunset sky with gentle lavender clouds. The KL skyline "
    "fills the middle ground — Menara KL tower silhouette to one side, "
    "Suria KLCC mall rooftops, and distant Genting Highlands mountains "
    "as a pale blue silhouette. Tropical palm fronds curve in from both "
    "lower corners, a single saturated hibiscus blossom in the "
    "lower-left for accent. The air is warm and still. Decorative "
    "Peranakan phoenix-and-peony tile border frames the entire scene."
)

BACK_PROMPT = PERANAKAN_BASE + (
    "\n\nSCENE: George Town, Penang at dusk. A row of pastel Peranakan "
    "heritage shophouses with louvered shutters and hanging paper "
    "lanterns line a quiet narrow lane (Armenian Street). The shophouses "
    "are in soft mint, butter, and powder-pink with cream pillars and "
    "delicate gilt trim. A traditional Penang trishaw with floral "
    "decorations is parked along the lane. A bougainvillea bush in pink "
    "spills over a doorway. Soft sunset glow on cream walls. Decorative "
    "Peranakan butterfly-and-lotus tile border frames the entire scene."
)


def generate_one(slug: str, prompt: str, ws: str) -> tuple[str, str]:
    body = {"prompt": prompt, "aspect_ratio": "1:1", "resolution": "2k", "output_format": "jpeg"}
    tid = submit_nbp(body, T2I_EP, ws)
    if not tid:
        return slug, "FAIL: submit"
    raw_url = poll_nbp(tid, ws, timeout=600)
    if not raw_url:
        return slug, "FAIL: poll"
    out = OUT_DIR / f"{slug}.jpg"
    ok, note = download_verify(raw_url, out)
    if not ok:
        return slug, f"FAIL: dl {note}"
    return slug, str(out)


def main():
    ws = _keychain("wavespeed-api-key")
    if not ws:
        print("ERROR: missing wavespeed creds", flush=True)
        sys.exit(1)

    jobs = [
        ("front", FRONT_PROMPT),
        ("back", BACK_PROMPT),
    ]
    print(f"Generating {len(jobs)} Malaysia cover illustrations...", flush=True)
    with ThreadPoolExecutor(max_workers=2) as ex:
        futs = {ex.submit(generate_one, slug, prompt, ws): slug for slug, prompt in jobs}
        for fut in as_completed(futs):
            slug = futs[fut]
            try:
                _, result = fut.result()
            except Exception as e:
                result = f"FAIL: {e}"
            print(f"  {slug}: {result}", flush=True)


if __name__ == "__main__":
    main()
