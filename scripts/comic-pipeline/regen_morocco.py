#!/usr/bin/env python3
"""Generate comics for all 61 Morocco scams from the rebuilt city HTML pages.

Style is locked (PR #796) — Matisse 1912 Tangier watercolor — and the anchor
image lives at scam-comics/ma/style-tests/matisse-tangier-watercolor.jpg
in styles.PILOTS.

Unlike Malaysia (which had to read from api/v1/scams JSON because the HTML
was being rebuilt in parallel), Morocco's 10 city HTMLs were just shipped
to main and are stable — so we can use generate.extract_scams() directly.

R2 output paths match the convention so the existing/inserted img tags work:
  https://img.tabiji.ai/scams/<city>/scam-<n>.jpg

Usage:
    python3 scripts/comic-pipeline/regen_morocco.py            # all 61 scams
    python3 scripts/comic-pipeline/regen_morocco.py --force    # overwrite cache
    python3 scripts/comic-pipeline/regen_morocco.py marrakech rabat  # subset
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

COUNTRY = "morocco"
CITIES = [
    "marrakech", "casablanca", "tangier", "rabat", "fez",
    "agadir", "merzouga", "ouarzazate", "chefchaouen", "essaouira",
]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("cities", nargs="*", help="subset of cities (defaults to all 10)")
    p.add_argument("--batch-size", type=int, default=3)
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
