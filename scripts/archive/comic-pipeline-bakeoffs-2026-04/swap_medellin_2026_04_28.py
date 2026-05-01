#!/usr/bin/env python3
"""3-way rotation of Medellin scam comics flagged by 2026-04-28 vision audit.

Vision-verified mismatches (current state):
  scam-2.jpg depicts paseo millonario (taxi+ATM) -> belongs at scam-3 slot
  scam-3.jpg depicts motorcycle phone snatch    -> belongs at scam-5 slot
  scam-5.jpg depicts Tinder honeytrap           -> belongs at scam-2 slot

Source files were pre-downloaded by the audit to /tmp/co-comics-verify/.

Usage:
    python3 scripts/comic-pipeline/swap_medellin_2026_04_28.py [--dry-run]
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import requests

R2_ACCOUNT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"

# (source local file, destination R2 key)
SWAPS = [
    ("/tmp/co-comics-verify/medellin-scam-2.jpg", "scams/medellin/scam-3.jpg"),  # taxi -> Paseo slot
    ("/tmp/co-comics-verify/medellin-scam-3.jpg", "scams/medellin/scam-5.jpg"),  # motorcycle -> Motorcycle slot
    ("/tmp/co-comics-verify/medellin-scam-5.jpg", "scams/medellin/scam-2.jpg"),  # Tinder -> Tinder slot
]


def get_key(name: str) -> str:
    return subprocess.check_output(
        ["security", "find-generic-password", "-s", name, "-w"],
        text=True,
    ).strip()


def upload(local: Path, r2_key: str, token: str) -> None:
    url = f"https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{r2_key}"
    r = requests.put(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "image/jpeg"},
        data=local.read_bytes(),
        timeout=120,
    )
    body = r.json() if r.text else {}
    if not body.get("success"):
        raise RuntimeError(f"R2 upload failed: {r.status_code} {r.text[:400]}")


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    token = get_key("cloudflare-api-token")
    for src, dest in SWAPS:
        src_path = Path(src)
        if not src_path.exists():
            raise SystemExit(f"missing source: {src}")
        size = src_path.stat().st_size
        action = "DRY-RUN" if dry_run else "UPLOAD"
        print(f"{action} {src} ({size} bytes) -> r2://{R2_BUCKET}/{dest}")
        if dry_run:
            continue
        upload(src_path, dest, token)
        print(f"  ok")


if __name__ == "__main__":
    main()
