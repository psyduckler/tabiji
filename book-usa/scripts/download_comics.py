#!/usr/bin/env python3
"""
Download all 114 scam comic illustrations from R2 into the book-mexico
asset tree (used by build.py and build_paperback_interior.py).

Source: https://img.tabiji.ai/scams/<slug>/scam-<N>.jpg
Dest:   book-mexico/assets/images/<slug>/<NN>.jpg

Usage:
    python3 book-mexico/scripts/download_comics.py
"""
from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin

import requests
import yaml


HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
REPO = BOOK.parent
DATA_DIR = REPO / "api" / "v1" / "scams"
OUT_BASE = BOOK / "assets" / "images"
OUT_BASE.mkdir(parents=True, exist_ok=True)

CONFIG = yaml.safe_load((BOOK / "config.yaml").read_text())
CITIES = CONFIG["cities"]


def comic_jobs() -> list[tuple[str, int, str, Path]]:
    """Return list of (slug, idx, url, dest) tuples for every scam comic."""
    jobs = []
    for slug in CITIES:
        path = DATA_DIR / f"{slug}.json"
        if not path.exists():
            print(f"! {slug}: data file missing", file=sys.stderr)
            continue
        data = json.loads(path.read_text())
        out_dir = OUT_BASE / slug
        out_dir.mkdir(exist_ok=True)
        for idx, _scam in enumerate(data["scams"], start=1):
            url = f"https://img.tabiji.ai/scams/{slug}/scam-{idx}.jpg"
            dest = out_dir / f"{idx:02d}.jpg"
            jobs.append((slug, idx, url, dest))
    return jobs


def fetch_one(slug: str, idx: int, url: str, dest: Path) -> tuple[bool, str]:
    if dest.exists() and dest.stat().st_size > 1024:
        return True, f"· {slug}/{idx:02d}: cached"
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        dest.write_bytes(r.content)
        return True, f"✓ {slug}/{idx:02d}: {dest.stat().st_size / 1024:.0f} KB"
    except Exception as e:
        return False, f"✗ {slug}/{idx:02d}: {e}"


def main() -> None:
    jobs = comic_jobs()
    print(f"→ Downloading {len(jobs)} comics ({len(CITIES)} cities)…")

    fails: list[str] = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {
            pool.submit(fetch_one, slug, idx, url, dest): (slug, idx)
            for slug, idx, url, dest in jobs
        }
        for f in as_completed(futures):
            ok, msg = f.result()
            print(msg)
            if not ok:
                fails.append(msg)

    print(f"\nDone. {len(jobs) - len(fails)} / {len(jobs)} succeeded.")
    if fails:
        print("\nFailures:")
        for m in fails:
            print(f"  {m}")
        sys.exit(1)


if __name__ == "__main__":
    main()
