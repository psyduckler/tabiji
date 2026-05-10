#!/usr/bin/env python3
"""
Generate a Kindle ebook cover at Amazon's recommended dimensions.

Amazon KDP recommends 2560 px on the longest side for ebook covers, 2:3 aspect
(1600×2560 portrait). Our front-titled.jpg is 1696×2528, so we resize/crop to
match. JPEG quality 95.

Usage:
    python3 book-travel-scams-seniors/scripts/build_kindle_cover.py
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image


HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
SRC = BOOK / "assets" / "covers" / "front-titled.jpg"
DEST = BOOK / "build" / "travel-scams-for-seniors-kindle-cover.jpg"

KDP_W, KDP_H = 1600, 2560  # Amazon recommended ebook cover


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing {SRC}")
    img = Image.open(SRC).convert("RGB")
    src_w, src_h = img.size

    # Scale by height to match 2560, then center-crop or letterbox if needed.
    target_aspect = KDP_W / KDP_H
    src_aspect = src_w / src_h
    if abs(src_aspect - target_aspect) < 0.01:
        # Same aspect — straight resize.
        out = img.resize((KDP_W, KDP_H), Image.LANCZOS)
    elif src_aspect > target_aspect:
        # Source wider than target — scale by height, crop horizontally.
        scale = KDP_H / src_h
        new_w = int(src_w * scale)
        scaled = img.resize((new_w, KDP_H), Image.LANCZOS)
        left = (new_w - KDP_W) // 2
        out = scaled.crop((left, 0, left + KDP_W, KDP_H))
    else:
        # Source taller than target — scale by width, crop vertically.
        scale = KDP_W / src_w
        new_h = int(src_h * scale)
        scaled = img.resize((KDP_W, new_h), Image.LANCZOS)
        top = (new_h - KDP_H) // 2
        out = scaled.crop((0, top, KDP_W, top + KDP_H))

    DEST.parent.mkdir(parents=True, exist_ok=True)
    out.save(DEST, "JPEG", quality=95, progressive=True, optimize=True)
    print(f"[kindle-cover] {DEST.name}: {out.size[0]}×{out.size[1]}")


if __name__ == "__main__":
    main()
