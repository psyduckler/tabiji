#!/usr/bin/env python3
"""Targeted regen for the 53 broken/partial Canada scam comics.

Selects only the specific (city, scam_n) pairs identified in the 2026-04-21
audit of https://tabiji.ai/scams/country/ca/ where the v1 fallback prompt fired
and produced generic pickpocket/polar-bear/card-swap boilerplate instead of the
named scam. Leaves the 22 good comics untouched.

Usage:
    python3 scripts/comic-pipeline/regen_canada.py
    python3 scripts/comic-pipeline/regen_canada.py --force  # re-try even if local cache exists
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import extract_scams, generate_one, _keychain  # noqa: E402

COUNTRY = "canada"

TARGETS: dict[str, list[int]] = {
    "vancouver":     [1, 2, 4, 5, 6, 7],
    "montreal":      [1, 3, 4, 6, 7, 8],
    "toronto":       [3, 5, 6, 7],
    "quebec-city":   [2, 3, 4, 5],
    "banff":         [1, 2, 3, 6],
    "jasper":        [2, 4, 5],
    "whistler":      [1, 4, 5, 6],
    "victoria-bc":   [1, 2, 3, 4, 5, 6],
    "halifax":       [1, 2, 4, 6],
    "calgary":       [2, 3, 6],
    "ottawa":        [1, 2, 3, 5],
    "niagara-falls": [1, 2, 3, 4, 5],
}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--batch-size", type=int, default=3)
    p.add_argument("--force", action="store_true")
    args = p.parse_args()

    out_dir = Path(f"/tmp/{COUNTRY}-comics-v2")
    out_dir.mkdir(parents=True, exist_ok=True)
    audit_log = Path(f"/tmp/{COUNTRY}-audit.jsonl")
    audit_log.write_text("")
    flagged_log = Path(f"/tmp/{COUNTRY}-flagged.log")
    flagged_log.write_text("")

    ws_token = _keychain("wavespeed-api-key")
    r2_token = _keychain("cloudflare-api-token")

    targeted = []
    total_expected = sum(len(v) for v in TARGETS.values())
    for city, wanted in TARGETS.items():
        city_scams = {s["n"]: s for s in extract_scams(city)}
        for n in wanted:
            if n not in city_scams:
                print(f"WARN {city}/scam-{n}: not found in index.html", flush=True)
                continue
            targeted.append(city_scams[n])

    print(f"[{COUNTRY}] targeted {len(targeted)}/{total_expected} scams "
          f"across {len(TARGETS)} cities (batch size {args.batch_size})", flush=True)

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
