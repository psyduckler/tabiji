#!/usr/bin/env python3
"""Regenerate 8 flagged Turkey scam comics via v2 pipeline.

These 8 are the comics identified in the 2026-04-21 audit of
tabiji.ai/scams/country/tr/ as v1 keyword-template fallbacks that don't
match their scam narrative. Per-scam list in FLAGGED below. Everything
else stays untouched.

Reason codes:
  TAXI-INCITY-MISAPPLIED — recycled in-city taxi-meter template
                           ("Straight to hotel — meter!" / "Use BiTaksi")
                           applied to airport or inter-town taxi scams
                           whose real mechanic is flat-rate / pirate-pickup,
                           not meter manipulation
  RESTAURANT-MISAPPLIED  — recycled restaurant-tourist-menu template
                           ("Our tourist specials!" / "No prices on menu!")
                           applied to bar/drink-spiking scams
  CONCIERGE-MISAPPLIED   — recycled hotel-concierge-transfer template
                           ("Private transfer 2000 lira!" / "App says 500
                           lira!") applied to excursion-reseller scams

Uses the same generate_one() from generate.py so behavior is identical
to a full-country v2 run, just scoped to these specific (city, n) pairs.

Run:
    python3 scripts/comic-pipeline/regen_turkey.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import extract_scams, generate_one, _keychain  # noqa: E402

FLAGGED = [
    ("istanbul",    8, "TAXI-INCITY-MISAPPLIED"),    # Airport Taxi Meter Trick
    ("izmir",       1, "TAXI-INCITY-MISAPPLIED"),    # Adnan Menderes Airport Taxi Overcharge
    ("ephesus",     6, "TAXI-INCITY-MISAPPLIED"),    # Selçuk-to-Ephesus Taxi Overcharge (inter-town)
    ("pamukkale",   6, "TAXI-INCITY-MISAPPLIED"),    # Denizli Otogar to Pamukkale Taxi Overcharge (inter-town)
    ("antalya",     6, "RESTAURANT-MISAPPLIED"),     # Bar Drink Spiking and Bill Inflation
    ("marmaris",    2, "RESTAURANT-MISAPPLIED"),     # Bar Street Bill Inflation and Drink Spiking
    ("alanya",      5, "CONCIERGE-MISAPPLIED"),      # All-Inclusive Resort Excursion Reseller & Hotel Tour Markups
    ("kusadasi",    6, "CONCIERGE-MISAPPLIED"),      # Off-Brand Independent Excursion Reseller Fraud
]

COUNTRY = "turkey"
BATCH_SIZE = 3  # matches Germany/Spain/Indonesia/China v2 production runs

OUT_DIR = Path("/tmp/turkey-regen-comics")
AUDIT_LOG = Path("/tmp/turkey-regen-audit.jsonl")
FLAG_LOG = Path("/tmp/turkey-regen-flagged.log")


def collect_targets() -> list[dict]:
    """Build the list of 8 scam dicts by extracting from each city's HTML."""
    by_city: dict[str, list[int]] = {}
    for city, n, _ in FLAGGED:
        by_city.setdefault(city, []).append(n)
    out = []
    for city, wanted_ns in sorted(by_city.items()):
        scams = extract_scams(city)
        want = set(wanted_ns)
        found_ns = {s["n"] for s in scams}
        missing = want - found_ns
        if missing:
            raise RuntimeError(f"{city}: could not extract scams {sorted(missing)} from HTML")
        for s in scams:
            if s["n"] in want:
                out.append(s)
    return out


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_LOG.write_text("")
    FLAG_LOG.write_text("")

    ws_token = _keychain("wavespeed-api-key")
    r2_token = _keychain("cloudflare-api-token")

    targets = collect_targets()
    reason_by_key = {(c, n): r for c, n, r in FLAGGED}
    print(f"[{COUNTRY}] regenerating {len(targets)} flagged scams (batch={BATCH_SIZE})",
          flush=True)

    ok = retried = flagged = 0
    t0 = time.time()
    for i in range(0, len(targets), BATCH_SIZE):
        batch = targets[i:i + BATCH_SIZE]
        elapsed = int(time.time() - t0)
        print(f"\n=== batch {i // BATCH_SIZE + 1}  t={elapsed}s  ({len(batch)} items) ===",
              flush=True)
        with ThreadPoolExecutor(max_workers=BATCH_SIZE) as ex:
            futs = [
                ex.submit(generate_one, COUNTRY, s, OUT_DIR, ws_token, r2_token, False)
                for s in batch
            ]
            for s, f in zip(batch, futs):
                try:
                    res = f.result()
                except Exception as e:
                    res = {"status": "flagged", "note": f"unhandled err: {e}",
                           "character": "?", "prompt": None}
                key = (s["city"], s["n"])
                label = f"{s['city']}/scam-{s['n']}"
                line = (f"{label}  [{reason_by_key[key]}]: {res['status']}  "
                        f"char={res['character']}  ({res['note']})")
                print(f"  {line}", flush=True)
                AUDIT_LOG.open("a").write(json.dumps({
                    "city": s["city"], "n": s["n"], "title": s["title"],
                    "reason": reason_by_key[key], **res,
                }) + "\n")
                if res["status"] in ("ok", "ok-cached"):
                    ok += 1
                elif res["status"] == "ok-retried":
                    retried += 1
                    ok += 1
                else:
                    flagged += 1
                    FLAG_LOG.open("a").write(line + "\n")

    summary = {
        "country": COUNTRY, "total": len(targets),
        "ok": ok, "retried": retried, "flagged": flagged,
        "elapsed_s": int(time.time() - t0),
        "audit_log": str(AUDIT_LOG), "flagged_log": str(FLAG_LOG),
    }
    print(f"\n[{COUNTRY}] FINAL: {json.dumps(summary)}", flush=True)
    return summary


if __name__ == "__main__":
    main()
