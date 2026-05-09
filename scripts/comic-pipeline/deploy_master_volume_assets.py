#!/usr/bin/env python3
"""Deploy The Big Book of Travel Scams master-volume assets to R2.

Uploads to canonical paths matching the country-book convention:
  - books/the-big-book-of-travel-scams/covers/front.png  (1800x2700 PNG)
  - books/the-big-book-of-travel-scams/covers/front.jpg  (1600x2560 JPG, KDP)
  - books/the-big-book-of-travel-scams/covers/cover-wrap.pdf (paperback wrap)

Future cover updates: re-run this script after rebuilding cover.png /
cover-kindle.jpg / cover-wrap.pdf.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import upload_r2  # noqa: E402

BOOK_ROOT = Path(
    "/Users/bjh/Documents/tabiji/.claude/worktrees/eloquent-boyd-7e72e8/book-atlas"
)
DESKTOP = Path.home() / "Desktop/scam-atlas-final"

ASSETS = [
    # (local_path, r2_key, friendly_name)
    (BOOK_ROOT / "build" / "cover.png",
     "books/the-big-book-of-travel-scams/covers/front.png",
     "Hi-res cover PNG (1800x2700, used in ePub title page)"),
    (DESKTOP / "cover-kindle.jpg",
     "books/the-big-book-of-travel-scams/covers/front.jpg",
     "Kindle cover JPG (1600x2560, KDP listing thumbnail)"),
    (BOOK_ROOT / "build" / "the-big-book-of-travel-scams-cover-wrap.pdf",
     "books/the-big-book-of-travel-scams/covers/cover-wrap.pdf",
     "Paperback wraparound PDF (front + spine + back, 13.39x9.25 in)"),
]


def main():
    print(f"Deploying {len(ASSETS)} assets to R2 (img.tabiji.ai)...")
    for local, key, label in ASSETS:
        if not local.exists():
            print(f"  SKIP {key} — local file missing: {local}")
            continue
        size_kb = local.stat().st_size // 1024
        print(f"  Uploading {label}")
        print(f"    local: {local}")
        print(f"    r2:    {key}")
        print(f"    size:  {size_kb} KB")
        ok = upload_r2(local, key, "")
        if ok:
            print(f"    ✓ https://img.tabiji.ai/{key}")
        else:
            print(f"    ✗ upload failed")
        print()


if __name__ == "__main__":
    main()
