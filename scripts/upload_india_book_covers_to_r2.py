#!/usr/bin/env python3
"""Upload the India book covers to R2.

Three uploads:
  - book-india/assets/cover.jpg → books/india-tourist-scams/cover.jpg
    (the URL city-page CTAs reference, e.g. img.tabiji.ai/books/india-tourist-scams/cover.jpg)
  - book-india/assets/cover.jpg → books/india-tourist-scams/covers/front-designed.jpg
    (canonical path per books/_covers-manifest.json; used in the book lander hero)
  - book-india/assets/svg/back.jpg → books/india-tourist-scams/covers/back-designed.jpg
    (used as the background of the back-cover SVG on the lander)
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parents[1]
BOOK_ASSETS = REPO / "book-india" / "assets"
R2_ACCOUNT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"

UPLOADS = [
    (BOOK_ASSETS / "cover.jpg",       "books/india-tourist-scams/cover.jpg"),
    (BOOK_ASSETS / "cover.jpg",       "books/india-tourist-scams/covers/front-designed.jpg"),
    (BOOK_ASSETS / "svg" / "back.jpg", "books/india-tourist-scams/covers/back-designed.jpg"),
]


def get_token() -> str:
    return subprocess.check_output(
        ["security", "find-generic-password", "-s", "cloudflare-api-token", "-w"],
        text=True,
    ).strip()


def upload(local: Path, key: str, token: str) -> None:
    if not local.exists():
        sys.exit(f"missing local file: {local}")
    url = f"https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{key}"
    print(f"PUT {key}")
    print(f"  source: {local} ({local.stat().st_size / 1024:.0f} KB)")
    r = requests.put(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "image/jpeg"},
        data=local.read_bytes(),
        timeout=120,
    )
    body = r.json() if r.text else {}
    if not body.get("success"):
        sys.exit(f"R2 upload failed for {key}: HTTP {r.status_code} {r.text[:400]}")
    print("  ✓ R2 upload OK")
    public = f"https://img.tabiji.ai/{key}"
    h = requests.head(public, timeout=30)
    print(f"  HEAD {public} → HTTP {h.status_code}, "
          f"{h.headers.get('content-length')} bytes, {h.headers.get('content-type')}")


def main() -> None:
    token = get_token()
    for local, key in UPLOADS:
        upload(local, key, token)
        print()


if __name__ == "__main__":
    main()
