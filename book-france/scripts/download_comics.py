#!/usr/bin/env python3
"""Download France scam comics from R2 into book-france/assets/images/<slug>/NN.jpg."""
from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
REPO = BOOK.parent
DATA_DIR = REPO / "api" / "v1" / "scams"
OUT_DIR = BOOK / "assets" / "images"

CITIES = [
    "paris", "nice", "cannes", "st-tropez", "marseille", "avignon",
    "montpellier", "toulouse", "lyon", "chamonix", "annecy", "bordeaux",
    "biarritz", "strasbourg", "colmar", "mont-saint-michel",
]


def fetch(slug: str, idx: int) -> tuple[str, int, str]:
    url = f"https://img.tabiji.ai/scams/{slug}/scam-{idx}.jpg"
    dest_dir = OUT_DIR / slug
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{idx:02d}.jpg"
    if dest.exists() and dest.stat().st_size > 5_000:
        return (slug, idx, "skip")
    r = requests.get(url, timeout=60)
    if r.status_code != 200:
        return (slug, idx, f"fail-{r.status_code}")
    dest.write_bytes(r.content)
    return (slug, idx, f"ok-{len(r.content)//1024}KB")


def main() -> None:
    tasks = []
    for slug in CITIES:
        data_path = DATA_DIR / f"{slug}.json"
        data = json.loads(data_path.read_text())
        n = len(data["scams"])
        for i in range(1, n + 1):
            tasks.append((slug, i))

    print(f"Downloading {len(tasks)} comics across {len(CITIES)} cities...")
    ok = fail = skip = 0
    with ThreadPoolExecutor(max_workers=12) as pool:
        futs = [pool.submit(fetch, s, i) for s, i in tasks]
        for fut in as_completed(futs):
            slug, idx, status = fut.result()
            if status.startswith("ok"):
                ok += 1
            elif status == "skip":
                skip += 1
            else:
                fail += 1
                print(f"  ✗ {slug}/scam-{idx}.jpg → {status}")
    print(f"Done. ok={ok} skip={skip} fail={fail}")


if __name__ == "__main__":
    main()
