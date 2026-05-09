#!/usr/bin/env python3
"""v22 FINAL — locked book cover design.

User-requested adjustments from v21b:
  1. Suitcase photo shifted up (image_y 900 → 760)
  2. Subtitle shifted up (closer to suitcase, sb+50 gap)
  3. Subtitle on ONE line: "DON'T BE THEIR NEXT TARGET"

Output: ~/Desktop/scam-atlas-review/covers/cover-v22-final.png
        + book-atlas/build/cover.png (for ePub render)
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SRC = Path.home() / "Desktop/scam-atlas-review/covers/cover-v19-beartrap-red-cash.png"
OUT_PATH = Path.home() / "Desktop/scam-atlas-review/covers/cover-v22-final.png"

YELLOW = (255, 211, 64)
CREAM = (245, 235, 200)

TARGET_W = 1800
TARGET_H = 2700

FONTS = {
    "helvetica_neue": "/System/Library/Fonts/HelveticaNeue.ttc",
    "avenir": "/System/Library/Fonts/Avenir.ttc",
    "georgia_italic": "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
}


def font(key, size, idx=0):
    return ImageFont.truetype(FONTS[key], size, index=idx)


def sample_bg(src):
    pixels = []
    for x in range(20, 200, 10):
        for y in range(20, 200, 10):
            pixels.append(src.getpixel((x, y))[:3])
    return tuple(sum(p[i] for p in pixels) // len(pixels) for i in range(3))


def build_canvas(src, bg, image_scale, image_y):
    src_w, src_h = src.size
    crop_top = int(src_h * 0.18)
    cropped = src.crop((0, crop_top, src_w, src_h))
    cw, ch = cropped.size
    target_w = int(TARGET_W * image_scale)
    scale = target_w / cw
    new_w = target_w
    new_h = int(ch * scale)
    scaled = cropped.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGB", (TARGET_W, TARGET_H), bg)
    x_paste = (TARGET_W - new_w) // 2
    canvas.paste(scaled, (x_paste, image_y))
    return canvas, image_y + new_h


def draw_centered(draw, text, fnt, y, color, ls=0):
    if ls == 0:
        bbox = draw.textbbox((0, 0), text, font=fnt)
        w = bbox[2] - bbox[0]
        x = (TARGET_W - w) // 2 - bbox[0]
        draw.text((x, y), text, font=fnt, fill=color)
        return
    widths, total = [], 0
    for ch in text:
        bb = draw.textbbox((0, 0), ch, font=fnt)
        cw = bb[2] - bb[0]
        widths.append(cw)
        total += cw + ls
    total -= ls
    x = (TARGET_W - total) // 2
    for ch, cw in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=color)
        x += cw + ls


def render_final(src, bg):
    # Image: full-width, shifted up from y=900 → y=760
    canvas, sb = build_canvas(src, bg, image_scale=1.0, image_y=760)
    d = ImageDraw.Draw(canvas)

    # Top tag (slight bump up)
    d_tag = font("avenir", 32, idx=2)
    draw_centered(d, "TRAVEL SAFETY  ·  2026 EDITION",
                  d_tag, 70, CREAM, ls=8)

    # Italic prefix
    d_pre = font("georgia_italic", 80)
    draw_centered(d, "The Big Book of", d_pre, 145, CREAM)

    # Massive title
    d_title = font("helvetica_neue", 280, idx=8)
    draw_centered(d, "TRAVEL", d_title, 280, YELLOW)
    draw_centered(d, "SCAMS", d_title, 565, YELLOW)
    # Title block ends ~y=845; image at 760 means slight overlap area is empty
    # (the cropped suitcase has empty red space at its top so it's clean)

    # SUBTITLE — single line, shifted up to be close to suitcase bottom
    sub_y = sb + 50
    d_sub = font("helvetica_neue", 92, idx=1)
    draw_centered(d, "DON'T BE THEIR NEXT TARGET",
                  d_sub, sub_y, YELLOW)

    # Byline
    d_byline = font("avenir", 42, idx=2)
    draw_centered(d, "BERNARD HUANG  ·  TABIJI",
                  d_byline, TARGET_H - 105, CREAM, ls=8)

    return canvas


def main():
    src = Image.open(SRC).convert("RGB")
    bg = sample_bg(src)
    print(f"Source: {src.size}, bg RGB{bg}")
    out = render_final(src, bg)
    out.save(OUT_PATH, format="PNG", optimize=True)
    print(f"Wrote {OUT_PATH}")

    # Also drop a copy for the ePub build
    epub_cover = Path(
        "/Users/bjh/Documents/tabiji/.claude/worktrees/eloquent-boyd-7e72e8/"
        "book-atlas/build/cover.png"
    )
    epub_cover.parent.mkdir(parents=True, exist_ok=True)
    out.save(epub_cover, format="PNG", optimize=True)
    print(f"Wrote {epub_cover}")


if __name__ == "__main__":
    main()
