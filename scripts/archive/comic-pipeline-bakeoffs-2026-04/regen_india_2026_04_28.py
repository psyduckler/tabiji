#!/usr/bin/env python3
"""Generate Amar Chitra Katha comics for all 60 India scams across 12 cities.

Style was locked 2026-04-28 from the 5-way bake-off (mughal/madhubani/kalighat/
ravi-varma/amar-chitra-katha) — Amar Chitra Katha picked for storytelling
strength + reader-familiar comic staging + location-specific Indian signage.

Pilot anchor: scam-comics/in/style-tests/5-amar-chitra-katha-comic.jpg
R2 output:    scams/<city>/scam-<n>.jpg → https://img.tabiji.ai/scams/<city>/scam-<n>.jpg
HTML img tags will be inserted by a separate insert_india_comics.py pass.

Usage:
    python3 scripts/comic-pipeline/regen_india_2026_04_28.py            # all 60
    python3 scripts/comic-pipeline/regen_india_2026_04_28.py --force    # overwrite
    python3 scripts/comic-pipeline/regen_india_2026_04_28.py mumbai jaipur  # subset
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import generate_one, extract_scams, _keychain  # noqa: E402

COUNTRY = "india"
CITIES = [
    "agra", "bangalore", "chennai", "delhi", "goa", "hyderabad",
    "jaipur", "kolkata", "mumbai", "rishikesh", "udaipur", "varanasi",
]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("cities", nargs="*", help="subset of cities (defaults to all 12)")
    p.add_argument("--batch-size", type=int, default=4)
    p.add_argument("--force", action="store_true")
    args = p.parse_args()

    cities = args.cities or CITIES
    out_dir = Path(f"/tmp/{COUNTRY}-comics-v2")
    out_dir.mkdir(parents=True, exist_ok=True)
    audit_log = Path(f"/tmp/{COUNTRY}-audit.jsonl")
    audit_log.write_text("")
    flagged_log = Path(f"/tmp/{COUNTRY}-flagged.log")
    flagged_log.write_text("")

    ws_token = _keychain("wavespeed-api-key")
    r2_token = _keychain("cloudflare-api-token")

    targeted: list[dict] = []
    for city in cities:
        targeted.extend(extract_scams(city))

    print(f"[{COUNTRY}] {len(targeted)} scams across {len(cities)} cities "
          f"(batch size {args.batch_size})", flush=True)

    ok = retried = flagged = 0
    for i in range(0, len(targeted), args.batch_size):
        batch = targeted[i:i + args.batch_size]
        print(f"\n=== batch {i // args.batch_size + 1} ({len(batch)} items) ===", flush=True)
        with ThreadPoolExecutor(max_workers=args.batch_size) as ex:
            futures = [ex.submit(generate_one, COUNTRY, s, out_dir, ws_token, r2_token, args.force)
                       for s in batch]
            for s, f in zip(batch, futures):
                res = f.result()
                label = f"{s['city']}/scam-{s['n']}"
                line = f"{label}: {res['status']} char={res['character']} ({res['note']})"
                print(f"  {line}", flush=True)
                audit_log.open("a").write(json.dumps({
                    "city": s["city"], "n": s["n"], "title": s["title"], **res,
                }) + "\n")
                if res["status"] in ("ok", "ok-cached"):
                    ok += 1
                elif res["status"] == "ok-retried":
                    retried += 1
                    ok += 1
                else:
                    flagged += 1
                    flagged_log.open("a").write(line + "\n")

    summary = {
        "country": COUNTRY, "total": len(targeted),
        "ok": ok, "retried": retried, "flagged": flagged,
        "audit_log": str(audit_log), "flagged_log": str(flagged_log),
    }
    print(f"\n[{COUNTRY}] FINAL: {json.dumps(summary)}", flush=True)
    return 0 if flagged == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
