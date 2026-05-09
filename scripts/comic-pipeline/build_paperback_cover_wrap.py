#!/usr/bin/env python3
"""Build the KDP paperback cover wrap PDF: back + spine + front.

KDP 6×9 paperback specs (from https://kdp.amazon.com/help):
  - Trim: 6" × 9"
  - Bleed: 0.125" all 4 outside edges
  - Spine width: page_count × 0.002252 (white) or × 0.0025 (cream)
  - Cover total: (6 + 0.125)*2 + spine_width = 12.25 + spine, by 9.25" tall

This book: 507 pages, white paper → spine = 1.142", total wrap = 13.392 × 9.25 in.

At 300 DPI: 4018 × 2775 px.

Output:
  - book-atlas/build/the-big-book-of-travel-scams-cover-wrap.pdf
  - ~/Desktop/scam-atlas-final/the-big-book-of-travel-scams-cover-wrap.pdf
"""
from __future__ import annotations

import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/Users/bjh/Documents/tabiji/.claude/worktrees/eloquent-boyd-7e72e8/book-atlas")
FRONT_COVER = ROOT / "build" / "cover.png"  # 1800x2700, the locked v22
OUT_PDF = ROOT / "build" / "the-big-book-of-travel-scams-cover-wrap.pdf"
OUT_PNG = ROOT / "build" / "the-big-book-of-travel-scams-cover-wrap.png"

# KDP specs
PAGE_COUNT = 507
PAPER = "white"  # or "cream"
SPINE_FACTOR = 0.002252 if PAPER == "white" else 0.0025
DPI = 300

TRIM_W_IN = 6.0
TRIM_H_IN = 9.0
BLEED_IN = 0.125
SPINE_IN = PAGE_COUNT * SPINE_FACTOR

WRAP_W_IN = 2 * (TRIM_W_IN + BLEED_IN) + SPINE_IN
WRAP_H_IN = TRIM_H_IN + 2 * BLEED_IN

WRAP_W = round(WRAP_W_IN * DPI)
WRAP_H = round(WRAP_H_IN * DPI)
BLEED_PX = round(BLEED_IN * DPI)
TRIM_W_PX = round(TRIM_W_IN * DPI)
TRIM_H_PX = round(TRIM_H_IN * DPI)
SPINE_W_PX = round(SPINE_IN * DPI)

# Geometry
BACK_LEFT = 0
BACK_RIGHT = BLEED_PX + TRIM_W_PX
SPINE_LEFT = BACK_RIGHT
SPINE_RIGHT = SPINE_LEFT + SPINE_W_PX
FRONT_LEFT = SPINE_RIGHT
FRONT_RIGHT = WRAP_W
TRIM_TOP = BLEED_PX
TRIM_BOTTOM = BLEED_PX + TRIM_H_PX

# Colors (sampled from cover-kindle.png)
RED = (211, 3, 18)
YELLOW = (255, 211, 64)
CREAM = (245, 235, 200)
WHITE_BARCODE = (255, 255, 255)

FONTS = {
    "helvetica_neue": "/System/Library/Fonts/HelveticaNeue.ttc",
    "avenir": "/System/Library/Fonts/Avenir.ttc",
    "georgia_italic": "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
    "georgia": "/System/Library/Fonts/Supplemental/Georgia.ttf",
    "georgia_bold": "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
}


def font(key: str, size: int, idx: int = 0):
    return ImageFont.truetype(FONTS[key], size, index=idx)


def draw_centered(draw, text, fnt, y, color, region_left=0, region_right=WRAP_W,
                  letter_spacing=0):
    region_w = region_right - region_left
    if letter_spacing == 0:
        bbox = draw.textbbox((0, 0), text, font=fnt)
        w = bbox[2] - bbox[0]
        x = region_left + (region_w - w) // 2 - bbox[0]
        draw.text((x, y), text, font=fnt, fill=color)
        return
    widths, total = [], 0
    for ch in text:
        bb = draw.textbbox((0, 0), ch, font=fnt)
        cw = bb[2] - bb[0]
        widths.append(cw)
        total += cw + letter_spacing
    total -= letter_spacing
    x = region_left + (region_w - total) // 2
    for ch, cw in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=color)
        x += cw + letter_spacing


def wrap_text(text: str, fnt, max_w: int, draw) -> list[str]:
    """Wrap text by pixel width. Returns list of lines."""
    words = text.split()
    lines, current = [], []
    for word in words:
        candidate = " ".join(current + [word])
        bbox = draw.textbbox((0, 0), candidate, font=fnt)
        w = bbox[2] - bbox[0]
        if w <= max_w:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
                current = [word]
            else:
                lines.append(word)
                current = []
    if current:
        lines.append(" ".join(current))
    return lines


def draw_paragraph(draw, paragraph: str, fnt, x: int, y: int, max_w: int,
                   color, line_spacing: int = 12) -> int:
    lines = wrap_text(paragraph, fnt, max_w, draw)
    bbox = draw.textbbox((0, 0), "Hg", font=fnt)
    line_h = (bbox[3] - bbox[1]) + line_spacing
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=color)
        y += line_h
    return y


# ────────────────────────────────────────────────────────────────────────────
# Build the canvas
# ────────────────────────────────────────────────────────────────────────────

def main():
    print(f"KDP cover wrap: {WRAP_W_IN:.3f} × {WRAP_H_IN:.3f} in")
    print(f"  = {WRAP_W} × {WRAP_H} px @ {DPI} DPI")
    print(f"  Spine: {SPINE_IN:.3f} in / {SPINE_W_PX} px")
    print(f"  Page count: {PAGE_COUNT}")

    canvas = Image.new("RGB", (WRAP_W, WRAP_H), RED)
    d = ImageDraw.Draw(canvas)

    # ── Front cover (right side) ──────────────────────────────────────────
    front = Image.open(FRONT_COVER).convert("RGB")
    # Front cover is 1800×2700 — same as trim 6×9 at 300 DPI.
    # Paste at (FRONT_LEFT, TRIM_TOP) so trim aligns; the right & top/bottom
    # bleed comes from the red canvas background (matches the cover's red).
    canvas.paste(front, (FRONT_LEFT, TRIM_TOP))

    # ── Spine ─────────────────────────────────────────────────────────────
    # Vertical text running bottom-to-top (rotate 90° CCW, draw, paste back)
    spine_img = Image.new("RGB", (TRIM_H_PX, SPINE_W_PX), RED)
    sd = ImageDraw.Draw(spine_img)

    # Spine text — US convention: read top-to-bottom on the shelf =
    # TITLE first, then AUTHOR, then PUBLISHER at bottom.
    # Pre-rotation, x runs along spine length; CCW rotation maps original-left
    # to wrap-bottom (= shelf-bottom = publisher) and original-right to
    # wrap-top (= shelf-top = title).
    spine_title_font = font("helvetica_neue", 88, idx=8)  # Black weight
    spine_tag_font = font("avenir", 44, idx=2)

    spine_tag_y = (SPINE_W_PX - 44) // 2
    title_y = (SPINE_W_PX - 88) // 2

    def spine_text(text, fnt, x_pos, y_pos, color):
        sd.text((x_pos, y_pos), text, font=fnt, fill=color)

    # Publisher at original LEFT (= wrap bottom = shelf bottom)
    spine_text("TABIJI", spine_tag_font, 100, spine_tag_y, CREAM)
    # Author near the middle-right
    bbox = sd.textbbox((0, 0), "BERNARD HUANG", font=spine_tag_font)
    auth_w = bbox[2] - bbox[0]
    auth_bbox = sd.textbbox((0, 0), "THE BIG BOOK OF TRAVEL SCAMS",
                             font=spine_title_font)
    title_w = auth_bbox[2] - auth_bbox[0]
    # Title at original RIGHT (= wrap top = shelf top), with author just to its left
    title_x = TRIM_H_PX - 100 - title_w
    spine_text("THE BIG BOOK OF TRAVEL SCAMS", spine_title_font,
               title_x, title_y, YELLOW)
    # Author in middle (between publisher at far left and title at right)
    auth_x = (title_x - 200 - auth_w) // 2 + 200
    spine_text("BERNARD HUANG", spine_tag_font, auth_x, spine_tag_y, CREAM)

    # Rotate 90° CCW: original-right → wrap top, original-left → wrap bottom
    spine_rotated = spine_img.rotate(90, expand=True)
    canvas.paste(spine_rotated, (SPINE_LEFT, TRIM_TOP))

    # ── Back cover (left side) ────────────────────────────────────────────
    # Back cover content area: left bleed + 6" trim, top trim + 9" trim
    back_content_left = BLEED_PX + 80  # 80px inside trim for safe margin
    back_content_top = TRIM_TOP + 80
    back_content_right = BACK_RIGHT - 80
    back_content_w = back_content_right - back_content_left

    # All back-cover font sizes are in pixels at 300 DPI; pt = px * 72/300.
    # Body text upgraded to ~14pt (60px), hook to ~26pt (108px) — print-readable.

    # Series tag at very top — ~12pt
    bd = d
    tag_fnt = font("avenir", 50, idx=2)
    draw_centered(bd, "TABIJI  ·  TRAVEL SAFETY SERIES",
                  tag_fnt, back_content_top, CREAM,
                  region_left=back_content_left,
                  region_right=back_content_right, letter_spacing=10)

    # Hook headline — ~26pt
    hook_y = back_content_top + 130
    hook_fnt = font("helvetica_neue", 108, idx=8)
    draw_centered(bd, "DON'T BE THEIR",
                  hook_fnt, hook_y, YELLOW,
                  region_left=back_content_left,
                  region_right=back_content_right)
    draw_centered(bd, "NEXT TARGET.",
                  hook_fnt, hook_y + 132, YELLOW,
                  region_left=back_content_left,
                  region_right=back_content_right)

    # Body copy — ~14pt (60px)
    body_top = hook_y + 320
    body_fnt = font("georgia", 56)

    paragraphs = [
        "On a sunny morning in Paris, a woman picks up a brass gold "
        "ring at your feet and insists you dropped it. You didn't. "
        "Twenty euros and ten minutes later, you walk away with a "
        "worthless trinket.",
        "Multiply that scene by a thousand, across 24 countries. "
        "That's the world this book maps.",
        "Inside: 30 documented scams from Paris to Bangkok, painted "
        "in each country's signature illustrated style. The Seven "
        "Universal Patterns. Four recurring travelers — Margie, Priya, "
        "Marcus, and Harry. Five red flags per chapter. Exit phrases "
        "in 11 languages. The recovery playbook for the first hour, "
        "day, and week.",
        "The scammers ran their script ten times this week. You will "
        "run it once. This book is the asymmetry made portable.",
    ]

    y = body_top
    for para in paragraphs:
        y = draw_paragraph(bd, para, body_fnt,
                           back_content_left, y,
                           back_content_w, CREAM,
                           line_spacing=18)
        y += 32  # paragraph gap

    # Pull-quote / promise (italic) — ~16pt
    promise_y = y + 50
    promise_fnt = font("georgia_italic", 64)
    draw_centered(bd, "Travel like you've already been everywhere.",
                  promise_fnt, promise_y, YELLOW,
                  region_left=back_content_left,
                  region_right=back_content_right)

    # Byline placed RIGHT BELOW the promise quote — keeps the bottom 1.5"
    # of the back cover entirely clear for KDP's auto-overlaid ISBN barcode
    # (which lands somewhere in the bottom 15%, exact placement varies).
    # The KDP previewer flagged a collision when byline was bottom-anchored;
    # promoting it above the barcode safe zone fixes it.
    byline_y = promise_y + 130
    byline_fnt = font("avenir", 50, idx=2)
    draw_centered(bd, "BERNARD HUANG, EDITOR",
                  byline_fnt, byline_y, CREAM,
                  region_left=back_content_left,
                  region_right=back_content_right, letter_spacing=8)
    edition_fnt = font("avenir", 38, idx=0)
    draw_centered(bd, "TABIJI  ·  2026 EDITION",
                  edition_fnt, byline_y + 80, CREAM,
                  region_left=back_content_left,
                  region_right=back_content_right, letter_spacing=10)

    # ISBN/barcode zone — bottom ~1.5" of the back cover left intentionally
    # blank. KDP automatically overlays the barcode + ISBN there during
    # paperback submission. No reserved white box; KDP renders the barcode
    # on a white background of its own at upload time.

    # ── Save ──────────────────────────────────────────────────────────────
    canvas.save(OUT_PNG, format="PNG", optimize=True)
    print(f"Wrote {OUT_PNG} ({OUT_PNG.stat().st_size//1024} KB)")

    # PDF: PIL's save can output PDF. Use 300 DPI in resolution for proper sizing.
    canvas.save(OUT_PDF, format="PDF", resolution=DPI)
    print(f"Wrote {OUT_PDF} ({OUT_PDF.stat().st_size//1024} KB)")

    # Copy to Desktop
    desktop = Path.home() / "Desktop/scam-atlas-final" / OUT_PDF.name
    desktop.write_bytes(OUT_PDF.read_bytes())
    print(f"Wrote {desktop}")


if __name__ == "__main__":
    main()
