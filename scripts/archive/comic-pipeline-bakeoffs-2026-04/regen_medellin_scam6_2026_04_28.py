#!/usr/bin/env python3
"""Regenerate Medellin scam-6 — José María Córdova Airport Taxi & Uber Overcharge.

The 2026-04-28 vision audit found scam-6.jpg depicts a day-tour bait-and-switch
("Escobar tour? $80 USD") with no airport, no taxi, no card-charge mechanic.
The actual scam is an English-speaking driver overcharging on the MDE→El Poblado
run, then adding a zero on the card receipt.

This script overrides the location and mechanic to force a depiction of:
  - José María Córdova International (MDE) arrivals concourse
  - Friendly English-speaking driver intercepting before official taxi line
  - Card terminal showing 2,850,000 COP (zero added) vs 285,000 COP agreed
  - Defensive lesson: take regulated white airport taxi at posted 110,000 COP

Usage:
    python3 scripts/comic-pipeline/regen_medellin_scam6_2026_04_28.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import extract_scams, generate_one, _keychain  # noqa: E402

COUNTRY = "colombia"
CITY = "medellin"
SCAM_N = 6

LOCATION_OVERRIDE = (
    "José María Córdova International Airport (MDE) in Rionegro outside Medellín — "
    "modern airport arrivals hall with luggage carousels visible, an English-speaking "
    "driver in a polo shirt intercepting tourists at the curb past the official "
    "white-taxi rank, a posted 110,000 COP rate sign visible behind. CRITICAL: "
    "do NOT depict a walking-tour pitch, a tour bus, an Escobar tour, or any street "
    "tout outside an airport context. The setting must be MDE airport curbside / "
    "card-terminal scene only."
)
MECHANIC_OVERRIDE = (
    "MECHANIC EMPHASIS: the scam is a card-charge bait-and-switch. The driver agrees "
    "verbally to ~285,000 COP, then enters 2,850,000 COP into the card terminal at "
    "drop-off (extra zero). At least one panel must show the card terminal screen "
    "clearly displaying '$2,850,000 COP' with a tourist's shocked expression beside "
    "it. The defensive panel must show the regulated WHITE airport taxi line with "
    "'110,000 COP TARIFA OFICIAL' on a posted sign."
)

OUT_DIR = Path("/tmp/medellin-scam6-regen")
AUDIT_LOG = Path("/tmp/medellin-scam6-regen-audit.jsonl")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_LOG.write_text("")

    ws_token = _keychain("wavespeed-api-key")
    r2_token = _keychain("cloudflare-api-token")

    scams = extract_scams(CITY)
    target = next((s for s in scams if s["n"] == SCAM_N), None)
    if target is None:
        raise SystemExit(f"could not find {CITY}/scam-{SCAM_N}")

    target["location"] = f"{target['location']}. BACKDROP REQUIREMENT: {LOCATION_OVERRIDE}"
    target["story"] = f"{MECHANIC_OVERRIDE}\n\n{target['story']}"

    print(f"[medellin-6 regen] regenerating {target['title']!r}", flush=True)
    t0 = time.time()
    try:
        res = generate_one(COUNTRY, target, OUT_DIR, ws_token, r2_token, True)
    except Exception as e:
        res = {"status": "flagged", "note": f"unhandled err: {e}",
               "character": "?", "prompt": None}

    AUDIT_LOG.open("a").write(json.dumps({
        "city": CITY, "n": SCAM_N, "title": target["title"], **res,
    }) + "\n")
    print(f"  result: {res['status']}  ({res['note']})  elapsed={int(time.time() - t0)}s", flush=True)
    return 0 if res["status"].startswith("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
