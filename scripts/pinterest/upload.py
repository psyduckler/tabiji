#!/usr/bin/env python3
"""Upload rendered Pinterest pin JPGs to R2 (img.tabiji.ai/pinterest/<slug>/<format>.jpg)."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parents[2]
TMP = REPO / "tmp" / "pinterest"

R2_ACCOUNT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"
PUBLIC_BASE = "https://img.tabiji.ai"
FORMATS = ("stacked", "hook", "lesson")


def get_key(name: str) -> str:
    return subprocess.check_output(
        ["security", "find-generic-password", "-s", name, "-w"],
        text=True,
    ).strip()


def upload(local: Path, r2_key: str, token: str) -> str:
    url = f"https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{r2_key}"
    r = requests.put(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "image/jpeg"},
        data=local.read_bytes(),
        timeout=120,
    )
    body = r.json() if r.text else {}
    if not body.get("success"):
        raise RuntimeError(f"R2 upload failed ({r.status_code}): {r.text[:400]}")
    return f"{PUBLIC_BASE}/{r2_key}"


def upload_slug(slug: str) -> dict[str, str]:
    src_dir = TMP / slug
    if not src_dir.exists():
        sys.exit(f"no rendered files at {src_dir} — run render.py first")

    token = get_key("cloudflare-api-token")
    urls = {}
    for fmt in FORMATS:
        local = src_dir / f"{fmt}.jpg"
        if not local.exists():
            print(f"  ⚠ missing {local}, skipping")
            continue
        r2_key = f"pinterest/{slug}/{fmt}.jpg"
        public_url = upload(local, r2_key, token)
        urls[fmt] = public_url
        print(f"  {fmt} -> {public_url}")
    return urls


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--slug", required=True)
    args = p.parse_args()
    upload_slug(args.slug)


if __name__ == "__main__":
    main()
