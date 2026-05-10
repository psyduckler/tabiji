#!/usr/bin/env python3
"""
Build the paperback cover PDF for KDP.

Layout (KDP convention, single PDF):
    [BACK COVER] [SPINE] [FRONT COVER]
    + 0.125 in bleed on each outer edge

Inputs:
    assets/covers/front-titled.jpg
    assets/covers/back-titled.jpg
Output:
    build/travel-scams-for-seniors-paperback-cover.pdf

Spine width is computed from the actual page count of the interior PDF
using KDP's cream-paper formula (0.0025 in/page). Override with --spine.

Usage:
    python3 book-travel-scams-seniors/scripts/build_paperback_cover.py
    python3 book-travel-scams-seniors/scripts/build_paperback_cover.py --spine 0.9
"""
from __future__ import annotations

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader


HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
COVERS = BOOK / "assets" / "covers"
BUILD = BOOK / "build"
INTERIOR_PDF = BUILD / "travel-scams-for-seniors-paperback-interior.pdf"

DPI = 300
TRIM_W_IN = 6.0
TRIM_H_IN = 9.0
BLEED_IN = 0.125
PAGES_PER_INCH_CREAM = 1 / 0.0025  # 400 pages = 1.0 in

NAVY = (28, 38, 78)
CREAM = (250, 245, 232)


def in_to_px(inches: float) -> int:
    return int(round(inches * DPI))


def get_page_count() -> int:
    if not INTERIOR_PDF.exists():
        raise SystemExit(f"interior PDF missing at {INTERIOR_PDF}; run build_paperback_interior.py first")
    return len(PdfReader(str(INTERIOR_PDF)).pages)


def build_cover(spine_in: float) -> Path:
    front = Image.open(COVERS / "front-titled.jpg").convert("RGB")
    back = Image.open(COVERS / "back-titled.jpg").convert("RGB")

    # Total composite dimensions (inches → pixels @ 300 dpi)
    total_w_in = TRIM_W_IN * 2 + spine_in + BLEED_IN * 2
    total_h_in = TRIM_H_IN + BLEED_IN * 2

    total_w = in_to_px(total_w_in)
    total_h = in_to_px(total_h_in)

    # Each cover panel needs to fit trim + outside-edge bleed
    # Effective cover panel size when laid out:
    #   left bleed + back-trim + spine + front-trim + right bleed
    # Each panel image bleeds into the spine? No — the wrap convention is:
    #   - The artwork extends to the bleed edges.
    #   - Front and back illustrations get full trim height + bleed top/bottom.
    #   - Front fills [bleed_left + back_trim + spine] to [total_w - 0]
    #     (the +bleed is the rightmost outer edge).
    #   - Back fills [0] to [bleed_left + back_trim].
    panel_w_px = in_to_px(TRIM_W_IN + BLEED_IN)  # one panel + outer-edge bleed
    panel_h_px = total_h
    spine_w_px = in_to_px(spine_in)

    # Resize panels: bleed extends past the trim, so the artwork should fit
    # the trim area only. We place trim-sized art + a bleed strip of the
    # average edge color to extend safely. Simplest path: scale the source
    # illustration to (trim_w * dpi) x (trim_h * dpi), then mount on a cream
    # canvas of (panel_w_px x panel_h_px) with bleed area filled cream.
    trim_w_px = in_to_px(TRIM_W_IN)
    trim_h_px = in_to_px(TRIM_H_IN)

    front_trim = front.resize((trim_w_px, trim_h_px), Image.LANCZOS)
    back_trim = back.resize((trim_w_px, trim_h_px), Image.LANCZOS)

    composite = Image.new("RGB", (total_w, total_h), CREAM)

    # Place back panel at left with top-bleed + outer-bleed (left edge is bleed)
    back_x = in_to_px(BLEED_IN)  # offset from outer-left bleed
    back_y = in_to_px(BLEED_IN)
    composite.paste(back_trim, (back_x, back_y))

    # Spine fill
    spine_x = back_x + trim_w_px
    spine_top = composite.crop((spine_x, 0, spine_x + spine_w_px, total_h))
    spine_fill = Image.new("RGB", spine_top.size, NAVY)
    composite.paste(spine_fill, (spine_x, 0))

    # Spine text — title and author rotated 90°
    draw_spine_text(composite, spine_x, spine_w_px, total_h)

    # Front panel
    front_x = spine_x + spine_w_px
    composite.paste(front_trim, (front_x, in_to_px(BLEED_IN)))

    # Save as JPEG (lossy but compact); KDP accepts JPEG cover files
    cover_jpg = BUILD / "travel-scams-for-seniors-paperback-cover.jpg"
    composite.save(cover_jpg, "JPEG", quality=95, dpi=(DPI, DPI), optimize=True)

    # Also save as PDF (single-page, sized to bleed dimensions)
    cover_pdf = BUILD / "travel-scams-for-seniors-paperback-cover.pdf"
    pdf_canvas = composite.copy()
    pdf_canvas.save(cover_pdf, "PDF", resolution=DPI)

    return cover_pdf


def draw_spine_text(img: Image.Image, spine_x: int, spine_w_px: int, total_h: int) -> None:
    """Draw 'TRAVEL SCAMS FOR SENIORS · BERNARD HUANG' rotated 90° on spine."""
    title = "TRAVEL SCAMS FOR SENIORS"
    author = "BERNARD HUANG"
    # Big Caslon for the title; Optima for the author
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/BigCaslon.ttf", size=int(spine_w_px * 0.42))
        author_font = ImageFont.truetype("/System/Library/Fonts/Optima.ttc", size=int(spine_w_px * 0.30), index=1)
    except OSError:
        # Fallback fonts
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size=int(spine_w_px * 0.40))
        author_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size=int(spine_w_px * 0.28))

    # Render text on a separate canvas sized to the spine length (vertical),
    # then rotate -90° and paste. The "horizontal" canvas is total_h wide.
    spine_canvas = Image.new("RGB", (total_h, spine_w_px), NAVY)
    spine_draw = ImageDraw.Draw(spine_canvas)
    cream = CREAM

    # Title centered horizontally on the spine canvas
    bbox = spine_draw.textbbox((0, 0), title, font=title_font)
    title_w = bbox[2] - bbox[0]
    title_h = bbox[3] - bbox[1]
    spine_draw.text(
        ((total_h - title_w) // 2, (spine_w_px - title_h) // 2 - int(spine_w_px * 0.18)),
        title, font=title_font, fill=cream,
    )

    # Author at the bottom of the spine (will be at the foot when rotated)
    abbox = spine_draw.textbbox((0, 0), author, font=author_font)
    author_w = abbox[2] - abbox[0]
    author_h = abbox[3] - abbox[1]
    # Position author near one end of the horizontal canvas (becomes near top when rotated)
    spine_draw.text(
        (total_h - author_w - int(0.4 * DPI), (spine_w_px - author_h) // 2),
        author, font=author_font, fill=cream,
    )

    rotated = spine_canvas.rotate(-90, expand=True, resample=Image.BICUBIC)
    img.paste(rotated, (spine_x, 0))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spine", type=float, default=None,
                    help="Spine width in inches. If omitted, computed from interior page count.")
    args = ap.parse_args()

    if args.spine is None:
        pages = get_page_count()
        spine_in = pages / PAGES_PER_INCH_CREAM
        print(f"[paperback-cover] interior page count: {pages}; spine: {spine_in:.4f} in (cream paper)")
    else:
        spine_in = args.spine
        print(f"[paperback-cover] spine override: {spine_in:.4f} in")

    cover_pdf = build_cover(spine_in)
    print(f"[paperback-cover] DONE → {cover_pdf}")


if __name__ == "__main__":
    main()
