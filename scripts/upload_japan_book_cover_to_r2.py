#!/usr/bin/env python3
"""Upload the Japan book Ghibli cover to R2.

Replaces img.tabiji.ai/books/japan-tourist-scams/cover.jpg with the new
composed Kindle cover (1600x2560) from book-japan/assets/cover.jpg.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parents[1]
LOCAL = REPO / "book-japan" / "assets" / "cover.jpg"
R2_ACCOUNT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"
R2_KEY = "books/japan-tourist-scams/cover.jpg"


def main() -> None:
    if not LOCAL.exists():
        sys.exit(f"missing local cover: {LOCAL}")
    token = subprocess.check_output(
        ["security", "find-generic-password", "-s", "cloudflare-api-token", "-w"],
        text=True,
    ).strip()
    url = f"https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{R2_KEY}"
    print(f"PUT {url}")
    print(f"  source: {LOCAL} ({LOCAL.stat().st_size / 1024:.0f} KB)")
    r = requests.put(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "image/jpeg"},
        data=LOCAL.read_bytes(),
        timeout=120,
    )
    body = r.json() if r.text else {}
    if not body.get("success"):
        sys.exit(f"R2 upload failed: HTTP {r.status_code} {r.text[:400]}")
    print("✓ R2 upload OK")
    # Verify the upload by HEAD-ing the public URL
    public = f"https://img.tabiji.ai/{R2_KEY}"
    h = requests.head(public, timeout=30)
    print(f"  HEAD {public} → HTTP {h.status_code}, {h.headers.get('content-length')} bytes, {h.headers.get('content-type')}")


if __name__ == "__main__":
    main()
