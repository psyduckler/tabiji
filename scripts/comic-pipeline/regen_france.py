#!/usr/bin/env python3
"""Regenerate 49 redundant France scam comics via v2 pipeline.

These 49 are the comics identified in the 2026-04-21 audit of
tabiji.ai/scams/country/fr/ as script-reuse redundancies: 14 recurring
scam types (Gold Ring, Friendship Bracelet, Fake Police, Taxi, ATM
Skimming, Restaurant Overcharging, etc.) each had a single bespoke
4-panel script from the v1 pipeline that got copy-pasted across every
French city where the scam exists, with only the landmark backdrop
swapped — identical dialogue, identical character poses.

This is structurally different from the China/Turkey/Japan fallback
problem: every France comic was visually *about* its stated scam
(no wrong-template misfires caught by the phash sweep — 0 cross-scam
near-duplicates below phash=50/256). The issue is purely intra-scam
redundancy: readers clicking through multiple French cities see the
same 4-panel joke 4-9 times with only different cityscape.

Strategy: for each cluster, keep the canonical (Paris-preferred,
else alphabetically first) comic as the reference, and regenerate all
non-canonical occurrences with v2 bespoke per-scam scripts that play
off each city's actual local pickup point — Gold Ring on the
Croisette (Cannes) vs. Place Masséna (Nice) vs. Part-Dieu (Lyon)
rather than the copy-pasted generic distraction scene.

Reason codes below encode which scam-family cluster each regen belongs
to. Canonical references kept as-is (14 comics):
  GOLD_RING        paris-1
  BRACELET         paris-2
  FAKE_POLICE      avignon-3
  TAXI             avignon-4
  ATM              avignon-8
  RESTAURANT       avignon-6
  VACATION_RENTAL  annecy-8
  WATCH            cannes-1
  CHARITY          biarritz-9
  BEACH_CLUB       cannes-7
  XMAS_MARKET      colmar-2
  PICKPOCKETING    lyon-1
  RENTAL_CAR       montpellier-9
  SHELL_GAME       lyon-5

Run:
    python3 scripts/comic-pipeline/regen_france.py
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
    ("colmar",        5, "ATM"),
    ("montpellier",  10, "ATM"),
    ("nice",         14, "ATM"),
    ("strasbourg",   10, "ATM"),
    ("toulouse",      9, "ATM"),
    ("st-tropez",     6, "BEACH_CLUB"),
    ("annecy",        6, "BRACELET"),
    ("avignon",       9, "BRACELET"),
    ("cannes",        6, "BRACELET"),
    ("lyon",          7, "BRACELET"),
    ("marseille",     1, "BRACELET"),
    ("strasbourg",    2, "BRACELET"),
    ("marseille",     4, "CHARITY"),
    ("cannes",        9, "FAKE_POLICE"),
    ("chamonix",      9, "FAKE_POLICE"),
    ("colmar",        6, "FAKE_POLICE"),
    ("lyon",          9, "FAKE_POLICE"),
    ("marseille",     9, "FAKE_POLICE"),
    ("nice",          9, "FAKE_POLICE"),
    ("annecy",        5, "GOLD_RING"),
    ("avignon",      10, "GOLD_RING"),
    ("bordeaux",      5, "GOLD_RING"),
    ("cannes",        5, "GOLD_RING"),
    ("chamonix",      8, "GOLD_RING"),
    ("lyon",          6, "GOLD_RING"),
    ("marseille",     2, "GOLD_RING"),
    ("montpellier",   6, "GOLD_RING"),
    ("nice",          4, "GOLD_RING"),
    ("strasbourg",    3, "GOLD_RING"),
    ("toulouse",      2, "GOLD_RING"),
    ("marseille",     3, "PICKPOCKETING"),
    ("nice",          8, "RENTAL_CAR"),
    ("bordeaux",      8, "RESTAURANT"),
    ("chamonix",     12, "RESTAURANT"),
    ("lyon",          4, "RESTAURANT"),
    ("marseille",     7, "RESTAURANT"),
    ("strasbourg",    9, "RESTAURANT"),
    ("toulouse",     12, "SHELL_GAME"),
    ("biarritz",      8, "TAXI"),
    ("bordeaux",      7, "TAXI"),
    ("cannes",        2, "TAXI"),
    ("lyon",         10, "TAXI"),
    ("st-tropez",     9, "TAXI"),
    ("strasbourg",    7, "TAXI"),
    ("avignon",      12, "VACATION_RENTAL"),
    ("cannes",       11, "VACATION_RENTAL"),
    ("nice",         15, "WATCH"),
    ("st-tropez",     2, "WATCH"),
    ("strasbourg",    6, "XMAS_MARKET"),
]

COUNTRY = "france"
BATCH_SIZE = 3

OUT_DIR = Path("/tmp/france-regen-comics")
AUDIT_LOG = Path("/tmp/france-regen-audit.jsonl")
FLAG_LOG = Path("/tmp/france-regen-flagged.log")


def collect_targets() -> list[dict]:
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
    print(f"[{COUNTRY}] regenerating {len(targets)} redundant scams (batch={BATCH_SIZE})",
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
