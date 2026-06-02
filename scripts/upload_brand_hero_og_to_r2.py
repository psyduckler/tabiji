#!/usr/bin/env python3
"""Publish the default brand-hero OG share card to R2 (img.tabiji.ai).

This is the image that renders when a tabiji.ai link is pasted into iMessage,
Slack, X/Twitter, Facebook, LinkedIn, etc. — the site-wide default `og:image`
for every page that doesn't have a more specific card (scam pages keep their
own scam art; compare pages keep compare-default-og.jpg).

The 1200x630 PNG is a binary asset, so (per .gitignore) it is NOT committed —
it lives only on R2. Render it from the design source, drop it at the path
below, and run this script to publish.

    Render:  open the brand-hero design (design_handoff_brand_hero/brand-hero-og.html)
             at 1200x630 and export to assets/og/brand-hero-og.png
    Publish: python3 scripts/upload_brand_hero_og_to_r2.py [path-to-png] [--dry-run]

Served at: https://img.tabiji.ai/brand-hero-og.png
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parents[1]
R2_ACCOUNT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"
PUBLIC_BASE = "https://img.tabiji.ai"
R2_KEY = "brand-hero-og.png"
DEFAULT_LOCAL = REPO / "assets" / "og" / "brand-hero-og.png"


def get_token() -> str:
    env = os.environ.get("CLOUDFLARE_API_TOKEN")
    if env:
        return env.strip()
    return subprocess.check_output(
        ["security", "find-generic-password", "-s", "cloudflare-api-token", "-w"],
        text=True,
    ).strip()


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    dry = "--dry-run" in sys.argv
    local = Path(args[0]) if args else DEFAULT_LOCAL

    if not local.is_file():
        sys.exit(f"PNG not found: {local}\nRender it first (see module docstring).")

    size_kb = local.stat().st_size / 1024
    print(f"{local} → {PUBLIC_BASE}/{R2_KEY}  ({size_kb:.1f} KB)" + (" (dry-run)" if dry else ""))
    if dry:
        return

    token = get_token()
    url = f"https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{R2_KEY}"
    r = requests.put(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "image/png"},
        data=local.read_bytes(),
        timeout=120,
    )
    body = r.json() if r.text else {}
    if not body.get("success"):
        sys.exit(f"✗ upload failed  HTTP {r.status_code}  {r.text[:300]}")
    print(f"✓ uploaded  HTTP {r.status_code}")

    h = requests.head(f"{PUBLIC_BASE}/{R2_KEY}", timeout=20)
    print(f"  HEAD /{R2_KEY} → HTTP {h.status_code}  "
          f"({h.headers.get('content-length','?')} bytes, {h.headers.get('content-type','?')})")


if __name__ == "__main__":
    main()
