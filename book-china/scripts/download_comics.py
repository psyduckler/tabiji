#!/usr/bin/env python3
"""Download every China scam comic from R2 into book-china/assets/images/<slug>/NN.jpg."""
from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
import yaml

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
ROOT = BOOK.parent
CONFIG = yaml.safe_load((BOOK / "config.yaml").read_text())
DATA_DIR = (BOOK / CONFIG["scam_data_dir"]).resolve()
OUT_BASE = BOOK / "assets" / "images"


def scam_count(slug: str) -> int:
    data = json.loads((DATA_DIR / f"{slug}.json").read_text())
    scams = data.get("scams") or data.get("items") or data.get("entries") or []
    return len(scams)


def download(slug: str, n: int) -> tuple[str, int, str]:
    out_dir = OUT_BASE / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{n:02d}.jpg"
    url = f"https://img.tabiji.ai/scams/{slug}/scam-{n}.jpg"
    try:
        r = requests.get(url, timeout=30)
        if r.status_code != 200:
            return (slug, n, f"HTTP {r.status_code}")
        out_path.write_bytes(r.content)
        return (slug, n, f"OK {len(r.content)//1024}KB")
    except Exception as e:
        return (slug, n, f"ERR {e}")


def main():
    cities = CONFIG["cities"]
    tasks = []
    for slug in cities:
        for n in range(1, scam_count(slug) + 1):
            tasks.append((slug, n))

    print(f"Downloading {len(tasks)} comics across {len(cities)} cities...", flush=True)
    ok = 0
    bad = 0
    with ThreadPoolExecutor(max_workers=12) as pool:
        futs = [pool.submit(download, s, n) for s, n in tasks]
        for f in as_completed(futs):
            slug, n, status = f.result()
            if status.startswith("OK"):
                ok += 1
            else:
                bad += 1
                print(f"  FAIL {slug}/{n:02d}: {status}", flush=True)
    print(f"DONE: {ok} ok, {bad} failed", flush=True)
    sys.exit(0 if bad == 0 else 1)


if __name__ == "__main__":
    main()
