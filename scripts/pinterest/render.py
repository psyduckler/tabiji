#!/usr/bin/env python3
"""Render a scam comic into 3 Pinterest pin variants (1000x1500, 2:3).

Variants:
  stacked — full 4-panel comic + headline + brand strip (cream bg)
  hook    — panel 1 only with bold hook text overlay (dark bg)
  lesson  — panel 4 only with takeaway text below (cream bg)
"""
from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[2]
TMP = REPO / "tmp" / "pinterest"

W, H = 1000, 1500
SRC_SIZE = 1024
PANEL_SIZE = 512

FONT_HEAVY = ("/System/Library/Fonts/Avenir Next.ttc", 8)
FONT_REGULAR = ("/System/Library/Fonts/Avenir Next.ttc", 7)
FONT_CONDENSED_BLACK = ("/System/Library/Fonts/HelveticaNeue.ttc", 9)

ACCENT = "#C8553D"
CREAM = "#FAF6F0"
DARK = "#141414"
TEXT = "#1a1a1a"


def load_font(size: int, weight: str = "heavy") -> ImageFont.FreeTypeFont:
    spec = {
        "heavy": FONT_HEAVY,
        "regular": FONT_REGULAR,
        "condensed_black": FONT_CONDENSED_BLACK,
    }[weight]
    return ImageFont.truetype(spec[0], size, index=spec[1])


def fetch_source(url_or_path: str) -> Image.Image:
    if url_or_path.startswith(("http://", "https://")):
        r = requests.get(url_or_path, timeout=30)
        r.raise_for_status()
        return Image.open(io.BytesIO(r.content)).convert("RGB")
    return Image.open(url_or_path).convert("RGB")


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, current = [], []
    for word in words:
        test = " ".join(current + [word])
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def draw_text_block(draw, text, font, x, y, max_width, fill=TEXT, line_spacing=1.05):
    lines = wrap_text(draw, text, font, max_width)
    bbox = draw.textbbox((0, 0), "Ag", font=font)
    line_h = int((bbox[3] - bbox[1]) * line_spacing)
    for i, line in enumerate(lines):
        draw.text((x, y + i * line_h), line, font=font, fill=fill)


def crop_panel(img: Image.Image, n: int) -> Image.Image:
    w, h = img.size
    half_w, half_h = w // 2, h // 2
    coords = {
        1: (0, 0, half_w, half_h),
        2: (half_w, 0, w, half_h),
        3: (0, half_h, half_w, h),
        4: (half_w, half_h, w, h),
    }
    return img.crop(coords[n])


def render_stacked(src: Image.Image, copy: dict, out: Path) -> None:
    canvas = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(canvas)

    eyebrow_font = load_font(28, "heavy")
    headline_font = load_font(78, "condensed_black")
    brand_font = load_font(34, "heavy")
    sub_font = load_font(24, "regular")

    draw.text((60, 60), copy["eyebrow"], font=eyebrow_font, fill=ACCENT)
    draw_text_block(draw, copy["headline"], headline_font, 60, 115, W - 120)

    comic = src.resize((1000, 1000), Image.LANCZOS)
    canvas.paste(comic, (0, 360))

    draw.text((60, 1390), "tabiji.ai", font=brand_font, fill=TEXT)
    sub = copy.get("brand_sub", "Real scams from real travelers")
    draw.text((60, 1440), sub, font=sub_font, fill="#555555")
    draw.ellipse((W - 100, 1410, W - 60, 1450), fill=ACCENT)

    canvas.save(out, "JPEG", quality=92)


def render_hook(src: Image.Image, copy: dict, out: Path) -> None:
    canvas = Image.new("RGB", (W, H), DARK)
    draw = ImageDraw.Draw(canvas)

    panel = crop_panel(src, 1).resize((1000, 1000), Image.LANCZOS)
    canvas.paste(panel, (0, 460))

    eyebrow_font = load_font(28, "heavy")
    hook_font = load_font(86, "condensed_black")
    foot_font = load_font(22, "regular")

    draw.text((60, 70), copy["eyebrow"], font=eyebrow_font, fill="#FFB199")
    draw_text_block(draw, copy["hook"], hook_font, 60, 130, W - 120, fill="#ffffff")

    foot = copy.get("foot", "tabiji.ai")
    draw.text((60, H - 30), foot, font=foot_font, fill="#cccccc")

    canvas.save(out, "JPEG", quality=92)


def render_lesson(src: Image.Image, copy: dict, out: Path) -> None:
    canvas = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(canvas)

    panel = crop_panel(src, 4).resize((1000, 1000), Image.LANCZOS)
    canvas.paste(panel, (0, 0))

    eyebrow_font = load_font(28, "heavy")
    lesson_font = load_font(86, "condensed_black")
    foot_font = load_font(24, "regular")

    draw.rectangle((60, 1020, 140, 1028), fill=ACCENT)
    draw.text((60, 1050), copy["eyebrow"], font=eyebrow_font, fill=ACCENT)
    draw_text_block(draw, copy["lesson"], lesson_font, 60, 1095, W - 120)

    foot = copy.get("foot", "tabiji.ai  ·  Real scams from real travelers")
    draw.text((60, H - 50), foot, font=foot_font, fill="#666666")

    canvas.save(out, "JPEG", quality=92)


RENDERERS = {
    "stacked": render_stacked,
    "hook": render_hook,
    "lesson": render_lesson,
}


def render_all(entry: dict, out_dir: Path) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    src = fetch_source(entry["source_image"])
    paths = {}
    for fmt, copy in entry["formats"].items():
        if fmt not in RENDERERS:
            continue
        out = out_dir / f"{fmt}.jpg"
        RENDERERS[fmt](src, copy, out)
        paths[fmt] = out
    return paths


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", default=str(Path(__file__).parent / "manifest.json"))
    p.add_argument("--slug", required=True)
    args = p.parse_args()

    manifest = json.loads(Path(args.manifest).read_text())
    entries = {e["slug"]: e for e in manifest["scams"]}
    if args.slug not in entries:
        sys.exit(f"slug not found in manifest: {args.slug}")

    out_dir = TMP / args.slug
    paths = render_all(entries[args.slug], out_dir)
    for fmt, path in paths.items():
        print(f"  {fmt} -> {path}")


if __name__ == "__main__":
    main()
