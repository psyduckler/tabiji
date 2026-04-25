#!/usr/bin/env python3
"""Regenerate the 12 France scam comics flagged by the audit as Tier A/B/C —
critical content errors, wrong-scam-mechanic, and style drift.

Tier A (5) — wrong-city signage / production artifacts:
  - lyon scam-3 (stray "Harry, 64" character label visible in panel)
  - lyon scam-12 (UK police call box in a Lyon scene)
  - cannes scam-3, marseille scam-7, chamonix scam-12 (Eiffel Tower in non-Paris cities)

Tier B (5) — wrong scam mechanic:
  - nice scam-3 (taxi shown for tram ticket scam)
  - nice scam-7 (driver-snatch shown for passenger-door grab)
  - nice scam-11 (fake inspectors shown for real-inspector validation fines)
  - chamonix scam-2 (ski instructor shown for mountaineering guide)
  - chamonix scam-4 (car rental shown for ski equipment theft)

Tier C (2) — style drift away from Hergé ligne-claire:
  - nice scam-14, scam-16 (photoreal/painterly + extra panels)

Calls generate_one() with force=True for each target so OK scams in the
same cities are left untouched.
"""
from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import extract_scams, generate_one, _keychain  # noqa: E402

COUNTRY = "france"
OUT_DIR = Path("/tmp/france-comics-v2")
BATCH_SIZE = 3
AUDIT_LOG = Path("/tmp/france-tier-abc-audit.jsonl")

# (city_slug, scam_n) — 12 total
TARGETS = [
    # Tier A — critical content errors
    ("lyon", 3),       # character-name label artifact
    ("lyon", 12),      # London police call box
    ("cannes", 3),     # Eiffel in Cannes
    ("marseille", 7),  # Eiffel in Marseille
    ("chamonix", 12),  # Eiffel in Chamonix
    # Tier B — wrong scam mechanic
    ("nice", 3),       # tram ticket, not taxi
    ("nice", 7),       # passenger-door grab, not driver phone
    ("nice", 11),      # real inspectors fining unvalidated, not fake
    ("chamonix", 2),   # mountaineering guide, not ski instructor
    ("chamonix", 4),   # ski equipment theft from racks, not car rental
    # Tier C — style drift
    ("nice", 14),      # ATM, restore Hergé
    ("nice", 16),      # vacation rental, restore Hergé
]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_LOG.write_text("")
    ws_token = _keychain("wavespeed-api-key")
    r2_token = _keychain("cloudflare-api-token")

    by_city: dict[str, dict[int, dict]] = {}
    for city in sorted({t[0] for t in TARGETS}):
        by_city[city] = {s["n"]: s for s in extract_scams(city)}

    flat: list[tuple[str, dict]] = []
    for city, n in TARGETS:
        if n not in by_city.get(city, {}):
            print(f"  ⚠ {city}/scam-{n}: not found, skipping")
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

    print(f"\nFINAL: {ok}/{len(flat)} ok ({retried} retried), {len(flagged)} flagged")
    if flagged:
        print("\nFlagged (need manual attention):")
        for line in flagged:
            print(f"  {line}")


if __name__ == "__main__":
    main()
