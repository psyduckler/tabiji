#!/usr/bin/env python3
"""
Pull the 66 Argentine scam comics from R2 into book-argentina/assets/images/<slug>/NN.jpg.
The scam-pages already have these comics injected; we just download them.

Usage: python3 book-argentina/scripts/pull_comics.py
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
ROOT = BOOK.parent
API_DIR = ROOT / "api" / "v1" / "scams"
IMAGES_DIR = BOOK / "assets" / "images"

CITIES = [
    "buenos-aires", "cordoba-argentina", "rosario", "mendoza", "salta",
    "bariloche", "el-calafate", "el-chalten", "ushuaia", "puerto-iguazu", "tigre",
]


def download(url: str, dest: Path) -> int:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return len(data)


def main() -> None:
    total_ok = 0
    total_skip = 0
    total_fail = 0
    for slug in CITIES:
        api_path = API_DIR / f"{slug}.json"
        if not api_path.exists():
            print(f"✗ {slug}: API JSON not found at {api_path}", file=sys.stderr)
            total_fail += 1
            continue
        data = json.loads(api_path.read_text())
        scams = data.get("scams", [])
        for idx, scam in enumerate(scams, start=1):
            dest = IMAGES_DIR / slug / f"{idx:02d}.jpg"
            if dest.exists() and dest.stat().st_size > 100_000:
                total_skip += 1
                continue
            url = f"https://img.tabiji.ai/scams/{slug}/scam-{idx}.jpg"
            try:
                size = download(url, dest)
                total_ok += 1
                print(f"  ✓ {slug}/scam-{idx} → {dest.relative_to(BOOK)} ({size // 1024} KB)")
            except Exception as e:
                print(f"  ✗ {slug}/scam-{idx}: {e}", file=sys.stderr)
                total_fail += 1
    print(f"\nDone: downloaded {total_ok}, skipped (cached) {total_skip}, failed {total_fail}")


if __name__ == "__main__":
    main()
