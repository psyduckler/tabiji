#!/usr/bin/env python3
"""Generate the 6 missing Japan scam comics via v2 pipeline.

These are scams 7-9 of Tokyo, 8 of Kyoto, and 7-8 of Osaka that exist
in the scam JSON data but had no comic on tabiji.ai at the time of the
book refresh. They were also absent from the scams/<city>/index.html
web pages (extract_scams() reads from HTML, not JSON, so a
straight-forward call misses them).

This script:
  1. Reads the 6 missing scams directly from api/v1/scams/<city>.json
  2. Builds extract_scams-compatible dicts (n, title, location, story, city)
  3. Calls generate_one() for each — identical behavior to a full-country v2 run
  4. On success, each JPEG is uploaded to R2 at scams/<city>/scam-N.jpg

Run:
    python3 scripts/comic-pipeline/generate_japan_new.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import generate_one, _keychain  # noqa: E402

REPO = _HERE.parent.parent  # tabiji repo root

MISSING = [
    ("tokyo", 7),
    ("tokyo", 8),
    ("tokyo", 9),
    ("kyoto", 8),
    ("osaka", 7),
    ("osaka", 8),
]

COUNTRY = "japan"
BATCH_SIZE = 3

OUT_DIR = Path("/tmp/japan-new-comics")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def scam_from_json(city: str, n: int) -> dict | None:
    """Load (city, n) from api/v1/scams/<city>.json, return an
    extract_scams-compatible dict (keys: n, title, location, story, city)."""
    path = REPO / "api" / "v1" / "scams" / f"{city}.json"
    data = json.loads(path.read_text())
    scams = data.get("scams", [])
    if n > len(scams):
        return None
    s = scams[n - 1]
    return {
        "n": n,
        "title": s.get("name", ""),
        "location": s.get("location", ""),
        # Keep story short so synthesize_prompt has a clear handle — 1200-char cap
        "story": s.get("description", "")[:1200],
        "city": city,
    }


def main() -> None:
    ws_token = _keychain("wavespeed-api-key")
    r2_token = _keychain("cloudflare-api-token")

    queue: list[dict] = []
    for city, n in MISSING:
        scam = scam_from_json(city, n)
        if not scam:
            print(f"⚠️ {city}/{n} not found in api/v1/scams/{city}.json — skipping")
            continue
        queue.append(scam)
        print(f"  queued: {city}/{n}  {scam['title'][:60]}")

    print(f"\nGenerating {len(queue)} missing comics with batch={BATCH_SIZE}…")
    results: list[dict] = []
    started = time.time()

    with ThreadPoolExecutor(max_workers=BATCH_SIZE) as ex:
        futures = {
            ex.submit(generate_one, COUNTRY, scam, OUT_DIR, ws_token, r2_token):
                scam for scam in queue
        }
        for fut in futures:
            scam = futures[fut]
            city = scam["city"]; n = scam["n"]; name = scam["title"][:60]
            try:
                r = fut.result()
                results.append({**r, "city": city, "n": n, "name": name})
                print(f"  {r['status']:14s} {city}/{n}  {name}  [{r['character']}]")
            except Exception as e:
                print(f"  exc            {city}/{n}  {name}  — {e}")
                results.append({"status": "exception", "note": str(e),
                               "city": city, "n": n, "name": name})

    elapsed = time.time() - started
    n_ok = sum(1 for r in results if r["status"] in ("ok", "ok-retried", "ok-cached"))
    n_flagged = sum(1 for r in results if r["status"] == "flagged")
    print(f"\n{n_ok}/{len(results)} ok, {n_flagged} flagged, {elapsed:.1f}s")

    log_path = OUT_DIR / "japan-new-comics-log.json"
    log_path.write_text(json.dumps({
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "elapsed_s": round(elapsed, 1),
        "results": results,
    }, indent=2, ensure_ascii=False))
    print(f"Log: {log_path}")


if __name__ == "__main__":
    main()
