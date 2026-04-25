#!/usr/bin/env python3
"""Regenerate the 33 Tier-2 US scam comics flagged by the audit as
mismatched/generic — comics that drifted to the "Got a minute, boss?"
template instead of depicting the specific scam mechanic.

Calls generate_one() with force=True for each target so OK scams in the
same cities are left untouched. Writes per-batch progress to stdout and
a JSONL audit log at /tmp/united-states-tier2-audit.jsonl.
"""
from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import extract_scams, generate_one, _keychain  # noqa: E402

COUNTRY = "united-states"
OUT_DIR = Path("/tmp/united-states-comics-v2")
BATCH_SIZE = 3
AUDIT_LOG = Path("/tmp/united-states-tier2-audit.jsonl")

# (city_slug, scam_n) pairs — 33 total: 20 multi-bad + 13 single-bad
TARGETS = [
    # multi-bad cities
    ("new-orleans", 2), ("new-orleans", 3), ("new-orleans", 7),
    ("chicago", 1), ("chicago", 5), ("chicago", 7),
    ("los-angeles", 1), ("los-angeles", 5),
    ("las-vegas", 1), ("las-vegas", 5),
    ("washington-dc", 2), ("washington-dc", 5),
    ("orlando", 1), ("orlando", 4),
    ("key-west", 2), ("key-west", 4),
    ("nashville", 3), ("nashville", 5),
    ("san-diego", 4), ("san-diego", 6),
    # single-bad cities
    ("miami", 6),
    ("honolulu", 6),
    ("portland", 6),
    ("san-francisco", 4),
    ("atlanta", 4),
    ("galveston", 6),
    ("anaheim", 1),
    ("memphis", 5),
    ("myrtle-beach", 3),
    ("boston", 4),
    ("denver", 4),
    ("sedona", 4),
    ("asheville", 3),
]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_LOG.write_text("")
    ws_token = _keychain("wavespeed-api-key")
    r2_token = _keychain("cloudflare-api-token")

    # Group targets by city, extract scams per-city once
    by_city: dict[str, dict[int, dict]] = {}
    for city in sorted({t[0] for t in TARGETS}):
        scams = extract_scams(city)
        by_city[city] = {s["n"]: s for s in scams}

    flat: list[tuple[str, dict]] = []
    for city, n in TARGETS:
        if n not in by_city.get(city, {}):
            print(f"  ⚠ {city}/scam-{n}: not found in city HTML, skipping")
            continue
        flat.append((city, by_city[city][n]))

    print(f"Processing {len(flat)} scams across {len({c for c, _ in TARGETS})} cities (batch={BATCH_SIZE})")

    ok = retried = 0
    flagged: list[str] = []

    for i in range(0, len(flat), BATCH_SIZE):
        batch = flat[i:i + BATCH_SIZE]
        print(f"\n=== batch {i // BATCH_SIZE + 1}/{(len(flat) + BATCH_SIZE - 1) // BATCH_SIZE} ({len(batch)} items) ===")
        with ThreadPoolExecutor(max_workers=BATCH_SIZE) as ex:
            futs = [ex.submit(generate_one, COUNTRY, s, OUT_DIR, ws_token, r2_token, True)
                    for _, s in batch]
            for (city, s), f in zip(batch, futs):
                res = f.result()
                line = f"{city}/scam-{s['n']}: {res['status']} char={res['character']} ({res['note']})"
                print(f"  {line}")
                AUDIT_LOG.open("a").write(json.dumps({
                    "city": city, "n": s["n"], "title": s["title"], **res,
                }) + "\n")
                if res["status"] in ("ok", "ok-cached"):
                    ok += 1
                elif res["status"] == "ok-retried":
                    ok += 1
                    retried += 1
                else:
                    flagged.append(line)

    print(f"\nFINAL: {ok}/{len(flat)} ok ({retried} retried via /text-to-image), {len(flagged)} flagged")
    if flagged:
        print("\nFlagged (need manual attention):")
        for line in flagged:
            print(f"  {line}")


if __name__ == "__main__":
    main()
