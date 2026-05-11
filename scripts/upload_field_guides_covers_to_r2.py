#!/usr/bin/env python3
"""Upload the three Tabiji Field Guides book covers to R2.

Targets:
  img.tabiji.ai/books/dental-tourism-field-guide/covers/front.jpg
  img.tabiji.ai/books/cosmetic-surgery-field-guide/covers/front.jpg
  img.tabiji.ai/books/medical-tourism-field-guide/covers/front.jpg

Source files (built locally during Phase 4 packaging):
  /tmp/v3-covers-upload/dental-tourism-field-guide/covers/front.jpg
  /tmp/v3-covers-upload/cosmetic-surgery-field-guide/covers/front.jpg
  /tmp/v3-covers-upload/medical-tourism-field-guide/covers/front.jpg
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import requests

R2_ACCOUNT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"

UPLOADS = [
    ("dental-tourism-field-guide",
     "/tmp/v3-covers-upload/dental-tourism-field-guide/covers/front.jpg"),
    ("cosmetic-surgery-field-guide",
     "/tmp/v3-covers-upload/cosmetic-surgery-field-guide/covers/front.jpg"),
    ("medical-tourism-field-guide",
     "/tmp/v3-covers-upload/medical-tourism-field-guide/covers/front.jpg"),
]


def main() -> None:
    token = subprocess.check_output(
        ["security", "find-generic-password", "-s", "cloudflare-api-token", "-w"],
        text=True,
    ).strip()

    for slug, local_path in UPLOADS:
        local = Path(local_path)
        if not local.exists():
            print(f"SKIP {slug}: missing {local}", file=sys.stderr)
            continue
        r2_key = f"books/{slug}/covers/front.jpg"
        url = f"https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{r2_key}"
        print(f"PUT {url}")
        print(f"  source: {local} ({local.stat().st_size / 1024:.0f} KB)")
        r = requests.put(
            url,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "image/jpeg"},
            data=local.read_bytes(),
            timeout=120,
        )
        body = r.json() if r.text else {}
        if not body.get("success"):
            print(f"FAIL {slug}: HTTP {r.status_code} {r.text[:400]}", file=sys.stderr)
            continue
        public = f"https://img.tabiji.ai/{r2_key}"
        h = requests.head(public, timeout=30)
        print(f"  ✓ uploaded; HEAD {public} → HTTP {h.status_code}, "
              f"{h.headers.get('content-length')} bytes, "
              f"{h.headers.get('content-type')}")


if __name__ == "__main__":
    main()
