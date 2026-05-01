#!/usr/bin/env python3
"""Regenerate 33 flagged Indonesia scam comics via v2 pipeline.

These 33 are the comics identified in the 2026-04-20 audit as recycled
template fallbacks that don't match their scam narrative. Per-scam list
in FLAGGED below. Everything else stays untouched.

Uses the same generate_one() from generate.py so behavior is identical
to a full-country v2 run, just scoped to these specific (city, n) pairs.

Run:
    python3 scripts/comic-pipeline/regen_indonesia.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import extract_scams, generate_one, _keychain  # noqa: E402

# 33 scams flagged in the Indonesia comic redundancy audit (2026-04-20)
# Reason codes:
#   GRAB  — recycled "fake-Grab taxi" template (doesn't match scam)
#   BROMO — recycled "Bromo sunrise jeep" template (only bromo_1 was legit)
#   BOAT  — recycled "Komodo harbor day-tour" template in labuan-bajo
#   IJEN  — recycled "gas-mask hiker at crater" within-city duplicate
FLAGGED = [
    ("bali",          6, "GRAB"),
    ("bali",          7, "GRAB"),
    ("batam",         5, "GRAB"),
    ("gili-islands",  1, "GRAB"),
    ("gili-islands",  3, "GRAB"),
    ("gili-islands",  4, "GRAB"),
    ("ijen-crater",   4, "IJEN"),
    ("ijen-crater",   6, "IJEN"),
    ("jakarta",       2, "GRAB"),
    ("jakarta",       5, "GRAB"),
    ("jakarta",       6, "GRAB"),
    ("labuan-bajo",   1, "BOAT"),
    ("labuan-bajo",   2, "BOAT"),
    ("labuan-bajo",   4, "BOAT"),
    ("lombok",        1, "GRAB"),
    ("lombok",        2, "GRAB"),
    ("mount-bromo",   2, "BROMO"),
    ("mount-bromo",   3, "BROMO"),
    ("mount-bromo",   4, "BROMO"),
    ("mount-bromo",   5, "BROMO"),
    ("mount-bromo",   6, "BROMO"),
    ("nusa-penida",   1, "GRAB"),
    ("nusa-penida",   4, "GRAB"),
    ("seminyak",      2, "GRAB"),
    ("seminyak",      3, "GRAB"),
    ("seminyak",      4, "GRAB"),
    ("seminyak",      5, "GRAB"),
    ("ubud",          1, "GRAB"),
    ("ubud",          2, "GRAB"),
    ("ubud",          3, "GRAB"),
    ("yogyakarta",    1, "GRAB"),
    ("yogyakarta",    3, "GRAB"),
    ("yogyakarta",    6, "GRAB"),
]

COUNTRY = "indonesia"
BATCH_SIZE = 3  # matches Germany/Spain v2 production runs

OUT_DIR = Path("/tmp/indonesia-regen-comics")
AUDIT_LOG = Path("/tmp/indonesia-regen-audit.jsonl")
FLAG_LOG = Path("/tmp/indonesia-regen-flagged.log")


def collect_targets() -> list[dict]:
    """Build the list of 33 scam dicts by extracting from each city's HTML."""
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
                ex.submit(generate_one, COUNTRY, s, OUT_DIR, ws_token, r2_token, True)
                for s in batch
            ]
            for s, f in zip(batch, futs):
                res = f.result()
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
                    retried += 1; ok += 1
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
