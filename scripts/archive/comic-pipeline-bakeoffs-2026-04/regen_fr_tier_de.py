#!/usr/bin/env python3
"""Regenerate the 26 France scam comics flagged by the audit as Tier D
(generic-template misuse) and Tier E (visual duplicates).

Tier D — generic templates miscast for unrelated scams (23):
  Single-template "Priya map-distraction" and "strawberry market scale"
  scenes were stamped onto cards whose actual mechanic is different.

Tier E — visual duplicates (3):
  - st-tropez scam-5 (Gas Burglary) ≈ scam-4 (Hotel Burglary)
  - mont-saint-michel scam-10 (Tide Timing) ≈ scam-4 (Bay Crossing)
  - montpellier scam-4 (TGV Train Theft) ≈ scam-3 (Saint-Roch Theft)

Calls generate_one(force=True) for each target so OK scams in the same
cities are left untouched.
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
AUDIT_LOG = Path("/tmp/france-tier-de-audit.jsonl")

# (city_slug, scam_n) — 26 total
TARGETS = [
    # Tier D — generic template misuse (23)
    ("chamonix", 5),         # booking deposit, not map-pickpocket
    ("chamonix", 7),         # Geneva-airport ambush specifics
    ("chamonix", 11),        # cable-car cabin pickpocket, not map
    ("mont-saint-michel", 3),  # official P1 lot, not rogue attendant
    ("mont-saint-michel", 7),  # Grande Rue crush, not generic plaza
    ("montpellier", 1),      # Tram Lines 1/2 door-close grab
    ("montpellier", 2),      # Place de la Comédie pickpocketing
    ("biarritz", 6),         # bar honeypot crew, not map-pickpocket
    ("biarritz", 7),         # Les Halles market pickpockets
    ("avignon", 5),          # OFF-festival ticket-flyer fraud
    ("avignon", 7),          # Les Halles indoor charcuterie/cheese upsell
    ("strasbourg", 4),       # Tram Lines B/C door-close grab
    ("strasbourg", 12),      # Alsatian-souvenir overcharge / photographer
    ("toulouse", 4),         # Metro pickpocket
    ("toulouse", 11),        # cyclist drive-by phone-snatch at terraces
    ("st-tropez", 8),        # market/clipboard/scooter pickpocket variants
    ("st-tropez", 11),       # contactless RFID skim through wallets in crowds
    ("bordeaux", 11),        # tram/bus rush-hour bumping
    ("annecy", 1),           # lake-promenade Old-Town markets pickpocket
    ("colmar", 2),           # Christkindelsmärik (winter market) specifics
    ("lyon", 11),            # Euronet/Travelex DCC overcharging
    ("cannes", 13),          # online phantom yacht-website wire-transfer
    ("nice", 12),            # Grand Arenas tram-stop ticket-machine "help"
    # Tier E — visual duplicates (3)
    ("st-tropez", 5),         # gas-through-AC-vent burglary, distinct from hotel
    ("mont-saint-michel", 10),  # tide-schedule trap (timing), not bay crossing
    ("montpellier", 4),       # TGV in-train theft during station stops
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
