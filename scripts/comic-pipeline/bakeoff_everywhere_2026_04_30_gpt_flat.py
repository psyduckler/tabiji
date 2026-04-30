#!/usr/bin/env python3
"""Everywhere-scams flat-style bake-off — gpt-image-2.

User feedback after first gpt-image-2 round: liked the feel + text quality,
but illustrations were too detailed/painterly. This bake-off targets
explicitly-flat aesthetics, with hard anti-detail anchors in every prompt
(no painterly texture, no gradients, no photorealism, simple geometric
shapes, minimal-prop backgrounds, 5–6 color palette max).

Same Margie / gift-card-by-phone scene as the prior round so results are
directly comparable.

Artist names removed up front — gpt-image-2 silently fails on living-
illustrator references (see memory: comic_pipeline_gpt_image_2_filter).
"""
from __future__ import annotations

import sys
import urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import submit_nbp, poll_nbp, _keychain, upload_r2  # noqa: E402
from cast import CHARACTERS  # noqa: E402
from bakeoff_everywhere_2026_04_30 import GENERIC_SCENE  # noqa: E402

GPT_T2I_EP = "https://api.wavespeed.ai/api/v3/openai/gpt-image-2/text-to-image"

OUT_DIR = Path("/tmp/bakeoff-everywhere-2026-04-30-gpt-flat")
OUT_DIR.mkdir(exist_ok=True)

# Anti-detail anchor pasted into every candidate so gpt-image-2 actually
# stays flat instead of drifting back to its painterly default.
FLAT_ANCHOR = (
    "STRICT STYLE CONSTRAINTS — these override any default tendency: "
    "FLAT 2D illustration only. No painterly texture, no visible brush "
    "strokes, no realistic rendering, no photorealism, no gradient fills, "
    "no soft airbrush shading, no atmospheric perspective. Solid flat "
    "color fills only. Simplified geometric shapes. Limited palette of 5–6 "
    "named colors maximum across the entire page. Backgrounds contain ONLY "
    "essential props directly referenced in the panel description — no "
    "incidental clutter, no decorative bowls of fruit, no extra picture "
    "frames, no busy storefront set-dressing. Generous flat negative space. "
    "Universal cross-generational appeal — clean, modern, approachable."
)

CANDIDATES = [
    ("flat-modern-editorial", (
        "A single illustrated comic book page in a clean modern flat editorial-"
        "illustration style as seen in upmarket American magazine covers — "
        "single-weight black-ink outline drawing, solid flat color fills with "
        "no gradients or texture, sophisticated limited palette of cream, "
        "ink-blue, terracotta, mustard, and one accent red, simplified "
        "confident shapes, generous negative space, ageless universal appeal "
        "across generations. " + FLAT_ANCHOR + " Showing four sequential "
        "panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the "
        "upper-left corner of each panel, separated by thin black panel "
        "borders with narrow white gutters. Each panel contains one clean "
        "white rounded speech bubble with a small pointer tail, holding short "
        "printed English dialogue in simple black sans-serif lettering — "
        "text must be legible, in English only, and correctly spelled. "
        "Square 1:1 composition, 2K resolution."
    )),
    ("flat-cel-shaded", (
        "A single illustrated comic book page in a clean flat cel-shaded "
        "animation style — single-weight black outlines, solid flat color "
        "fills with at most one single tone of darker flat shadow per shape "
        "(no gradient, no airbrush), warm friendly palette of cream, sky blue, "
        "soft coral, mustard, sage green, and accent black, simplified "
        "expressive figures, animation-cel cleanliness. " + FLAT_ANCHOR + " "
        "Showing four sequential panels arranged in a 2x2 grid with small "
        "numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated "
        "by thin black panel borders with narrow white gutters. Each panel "
        "contains one clean white rounded speech bubble with a small pointer "
        "tail, holding short printed English dialogue in simple black comic "
        "lettering — text must be legible, in English only, and correctly "
        "spelled. Square 1:1 composition, 2K resolution."
    )),
    ("flat-silkscreen-poster", (
        "A single illustrated comic book page in a flat silkscreen public-"
        "service-poster style — bold flat shapes printed in 4 spot colors only "
        "(cream paper, ink navy, brick red, and warm mustard), strong simplified "
        "compositions, confident hand-drawn black outline accents, mid-century "
        "instructional-poster sensibility, generous flat negative space, "
        "universally legible at-a-glance. " + FLAT_ANCHOR + " Showing four "
        "sequential panels arranged in a 2x2 grid with small numbers 1, 2, "
        "3, 4 in the upper-left corner of each panel, separated by thin ink-"
        "navy panel borders with narrow cream gutters. Each panel contains "
        "one clean white rounded speech bubble with a small pointer tail, "
        "holding short printed English dialogue in simple black comic "
        "lettering — text must be legible, in English only, and correctly "
        "spelled. Square 1:1 composition, 2K resolution."
    )),
    ("flat-paper-cutout", (
        "A single illustrated comic book page in a flat paper-cutout collage "
        "style — figures and objects rendered as layered flat colored paper "
        "shapes on a cream paper background, with subtle paper texture only "
        "as a base material (no painterly rendering on the shapes themselves), "
        "warm collage palette of cream, warm coral, teal blue, mustard yellow, "
        "olive green, and accent black, simplified expressive figures with "
        "minimal facial features, joyful but grounded storybook tone. "
        + FLAT_ANCHOR + " Showing four sequential panels arranged in a 2x2 "
        "grid with small hand-cut numbers 1, 2, 3, 4 in the upper-left corner "
        "of each panel, separated by thin black panel borders with narrow "
        "cream gutters. Each panel contains one clean white rounded speech "
        "bubble with a small pointer tail, holding short printed English "
        "dialogue in simple black comic lettering — text must be legible, "
        "in English only, and correctly spelled. Square 1:1 composition, "
        "2K resolution."
    )),
    ("flat-geometric-modernist", (
        "A single illustrated comic book page in a flat geometric modernist-"
        "graphic style — figures and props built from simple confident "
        "geometric shapes (circles, rectangles, soft rounded forms) with "
        "single-weight black outlines, solid flat color fills with zero "
        "gradient or texture, restrained mid-century-modern palette of warm "
        "off-white, slate blue, brick red, mustard, and charcoal, generous "
        "flat negative space, calm confident composition. " + FLAT_ANCHOR + " "
        "Showing four sequential panels arranged in a 2x2 grid with small "
        "numbers 1, 2, 3, 4 in the upper-left corner of each panel, "
        "separated by thin charcoal panel borders with narrow off-white "
        "gutters. Each panel contains one clean white rounded speech bubble "
        "with a small pointer tail, holding short printed English dialogue "
        "in simple black sans-serif lettering — text must be legible, in "
        "English only, and correctly spelled. Square 1:1 composition, 2K "
        "resolution."
    )),
]


def build_prompt(style_block: str) -> str:
    char = CHARACTERS["margie"]
    return f"{style_block}\n\nCHARACTER: {char}\n\n{GENERIC_SCENE}"


def _download_any(url: str, base: Path) -> tuple[bool, str, Path | None]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
    except Exception as e:
        return False, f"download err: {e}", None
    if len(data) < 50_000:
        return False, f"too small ({len(data)}B)", None
    if data[:3] == b"\xff\xd8\xff":
        ext = "jpg"
    elif data[:8] == b"\x89PNG\r\n\x1a\n":
        ext = "png"
    elif data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        ext = "webp"
    else:
        return False, f"unknown format (head={data[:8]!r})", None
    final = base.with_suffix(f".{ext}")
    final.write_bytes(data)
    return True, f"ok ({ext}, {len(data)}B)", final


def generate_one(slug: str, prompt: str, ws: str) -> tuple[str, str]:
    body = {
        "prompt": prompt,
        "aspect_ratio": "1:1",
        "resolution": "2k",
        "quality": "medium",
    }
    tid = submit_nbp(body, GPT_T2I_EP, ws)
    if not tid:
        return slug, "FAIL: submit"
    raw_url = poll_nbp(tid, ws, timeout=1500)
    if not raw_url:
        return slug, "FAIL: poll"
    base = OUT_DIR / f"everywhere-gpt-flat-{slug}"
    ok, note, final = _download_any(raw_url, base)
    if not ok:
        return slug, f"FAIL: dl {note}"
    # Upload to R2 immediately so URLs are ready when bakeoff completes.
    ext = final.suffix.lstrip(".")
    r2_key = f"scam-comics/_everywhere/style-tests-gpt-flat/{slug}.{ext}"
    if not upload_r2(final, r2_key, ""):
        return slug, f"OK_LOCAL: {final} (R2 upload failed)"
    return slug, f"OK: https://img.tabiji.ai/{r2_key} ({note})"


def main():
    ws = _keychain("wavespeed-api-key")
    if not ws:
        print("ERROR: missing wavespeed-api-key", flush=True)
        sys.exit(1)
    print(f"Submitting {len(CANDIDATES)} flat-style gpt-image-2 generations...", flush=True)
    results: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(generate_one, slug, build_prompt(sb), ws): slug
                for slug, sb in CANDIDATES}
        for fut in as_completed(futs):
            slug = futs[fut]
            try:
                _, result = fut.result()
            except Exception as e:
                result = f"FAIL: {e}"
            results[slug] = result
            print(f"  {slug}: {result}", flush=True)
    print("\n=== RESULTS (gpt-image-2 flat) ===", flush=True)
    for slug, _ in CANDIDATES:
        print(f"  {slug}: {results.get(slug, 'missing')}", flush=True)


if __name__ == "__main__":
    main()
