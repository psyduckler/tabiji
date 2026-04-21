#!/usr/bin/env python3
"""Upload pre-generated US scam comics from tmp/ to R2.

Reads all *-new.jpg files from tmp/, parses city and scam number from filename,
uploads to R2 at scams/<city>/scam-<N>.jpg.

Usage:
    python3 scripts/upload_us_comics_to_r2.py [--dry-run]
"""
from __future__ import annotations

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import re

import requests

REPO = Path(__file__).resolve().parents[1]
TMP = REPO / "tmp"
R2_ACCOUNT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"


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


def parse_filename(name: str) -> tuple[str, int] | None:
    # Patterns: "anaheim-scam-2-new.jpg", "vegas-scam-3-new.jpg", "la-scam3-new.jpg"
    m = re.match(r"^(.+)-scam-?(\d+)-new\.jpg$", name)
    if not m:
        return None
    city = m.group(1)
    scam_n = int(m.group(2))
    # Normalize city slugs
    if city == "vegas":
        city = "las-vegas"
    elif city == "la":
        city = "los-angeles"
    return city, scam_n


def main():
    dry_run = "--dry-run" in sys.argv

    files = list(TMP.glob("*-new.jpg"))
    if not files:
        print("No *-new.jpg files found in tmp/")
        return

    jobs = []
    for f in sorted(files):
        parsed = parse_filename(f.name)
        if not parsed:
            print(f"⚠ Skipping unrecognized: {f.name}")
            continue
        city, scam_n = parsed
        r2_key = f"scams/{city}/scam-{scam_n}.jpg"
        jobs.append((f, city, scam_n, r2_key))

    print(f"Found {len(jobs)} comics to upload")

    if dry_run:
        for f, city, scam_n, r2_key in jobs:
            print(f"  {f.name} → {r2_key}")
        print("\n[dry-run] No uploads performed")
        return

    cf_token = get_key("cloudflare-api-token")
    success = 0
    failed = []

    def do_upload(job):
        f, city, scam_n, r2_key = job
        try:
            upload(f, r2_key, cf_token)
            return f"✓ {f.name} → {r2_key}"
        except Exception as e:
            return f"✗ {f.name}: {e}"

    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = {ex.submit(do_upload, j): j for j in jobs}
        for fut in as_completed(futures):
            result = fut.result()
            print(result)
            if result.startswith("✓"):
                success += 1
            else:
                failed.append(result)

    print(f"\nUploaded {success}/{len(jobs)} comics")
    if failed:
        print(f"Failed: {len(failed)}")


if __name__ == "__main__":
    main()
