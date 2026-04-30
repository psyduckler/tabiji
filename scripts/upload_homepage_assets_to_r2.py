#!/usr/bin/env python3
"""Upload homepage logos + book covers to R2.

Logos: assets/logos/*.png  →  homepage/logos/<name>.png
Covers: assets/covers/*.jpg →  homepage/covers/<country>.jpg

Usage:
    python3 scripts/upload_homepage_assets_to_r2.py [--dry-run]
"""
from __future__ import annotations

import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parents[1]
R2_ACCOUNT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"
PUBLIC_BASE = "https://img.tabiji.ai"


def get_token() -> str:
    env = os.environ.get("CLOUDFLARE_API_TOKEN")
    if env:
        return env.strip()
    return subprocess.check_output(
        ["security", "find-generic-password", "-s", "cloudflare-api-token", "-w"],
        text=True,
    ).strip()


def upload_one(local: Path, r2_key: str, content_type: str, token: str) -> tuple[str, int, str]:
    url = f"https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{r2_key}"
    r = requests.put(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": content_type},
        data=local.read_bytes(),
        timeout=120,
    )
    body = r.json() if r.text else {}
    if not body.get("success"):
        return (r2_key, r.status_code, r.text[:200])
    return (r2_key, 200, "ok")


def main() -> None:
    dry = "--dry-run" in sys.argv
    jobs: list[tuple[Path, str, str]] = []

    for png in sorted((REPO / "assets" / "logos").glob("*.png")):
        jobs.append((png, f"homepage/logos/{png.name}", "image/png"))

    for jpg in sorted((REPO / "assets" / "covers").glob("*.jpg")):
        jobs.append((jpg, f"homepage/covers/{jpg.name}", "image/jpeg"))

    print(f"{len(jobs)} files to upload" + (" (dry-run)" if dry else ""))
    for local, key, ct in jobs:
        size_kb = local.stat().st_size / 1024
        print(f"  {local.name:40s} → {key}  ({size_kb:.1f} KB, {ct})")

    if dry:
        return

    token = get_token()
    failures: list[tuple[str, int, str]] = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(upload_one, l, k, c, token): k for l, k, c in jobs}
        for fut in as_completed(futures):
            key, status, msg = fut.result()
            mark = "✓" if status == 200 else "✗"
            print(f"  {mark} {key}  HTTP {status}  {msg}")
            if status != 200:
                failures.append((key, status, msg))

    if failures:
        sys.exit(f"\n{len(failures)} upload(s) failed")

    # Verify a sample by HEAD
    sample_keys = [j[1] for j in jobs[:3]] + [j[1] for j in jobs[-3:]]
    print("\nVerifying via public CDN:")
    for key in sample_keys:
        h = requests.head(f"{PUBLIC_BASE}/{key}", timeout=20)
        cl = h.headers.get("content-length", "?")
        print(f"  HEAD /{key}  → HTTP {h.status_code}  ({cl} bytes)")


if __name__ == "__main__":
    main()
