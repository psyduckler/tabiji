#!/usr/bin/env python3
"""Regenerate 16 partial-quality Turkey scam comics — audit #3 (2026-04-26).

These 16 are the comics flagged as PARTIAL in the 2026-04-26 visual audit:
the comic is in the right thematic family but is missing the specific scam
mechanic the title calls out (e.g., "Card-Skimming Bar Scam" rendered in a
souvenir-shop setting instead of a bar; "Manavgat Waterfall & Boat Trip"
rendered as a generic boat tour with no waterfall).

Re-running through the v2 Gemini synthesizer should produce a more faithful
4-panel script for each, since the synthesizer reads the full title and
first story paragraph.

Reason codes:
  PARTIAL-SETTING        — right scam type but wrong setting/venue
  PARTIAL-MECHANIC       — right setting but missing the specific mechanic
  PARTIAL-LANDMARK       — title names a specific landmark not depicted
  PARTIAL-MULTI-ELEMENT  — title combines two elements but only one shown

Uses the same generate_one() from generate.py.

Run:
    python3 scripts/comic-pipeline/regen_turkey_audit3.py
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
    ("alanya",      1, "PARTIAL-SETTING"),       # Card-Skimming Bar Scam — souvenir shop, not bar
    ("alanya",      2, "PARTIAL-MULTI-ELEMENT"), # Cleopatra Beach Taxi & Boat — only boat, no taxi
    ("antalya",     6, "PARTIAL-MECHANIC"),      # Bar Drink Spiking — no spiking visual
    ("cappadocia",  1, "PARTIAL-LANDMARK"),      # Pottery Showroom Heist — no Avanos pottery wheel
    ("cappadocia",  4, "PARTIAL-MECHANIC"),      # Carpet Hospitality Trap — no tea/friendship hook
    ("ephesus",     1, "PARTIAL-MECHANIC"),      # Skip-the-Line Reseller SITES — depicts physical tout
    ("ephesus",     2, "PARTIAL-SETTING"),       # Mandatory Carpet on Tours — no tour bus framing
    ("ephesus",     5, "PARTIAL-LANDMARK"),      # Virgin Mary Tour Bundle — no religious site
    ("fethiye",     5, "PARTIAL-SETTING"),       # Dalaman Airport Transfer — no airport signage
    ("istanbul",    8, "PARTIAL-SETTING"),       # Airport Taxi Meter — weak airport context
    ("izmir",       2, "PARTIAL-MULTI-ELEMENT"), # Counterfeit + Carpet — no counterfeit element
    ("izmir",       5, "PARTIAL-SETTING"),       # Nightlife Bar Card-Skimming — bazaar, not bar
    ("konya",       4, "PARTIAL-LANDMARK"),      # YHT Station Taxi — sign says airport, not train station
    ("kusadasi",    2, "PARTIAL-SETTING"),       # Cruise-Excursion Carpet — no cruise/tour-bus framing
    ("marmaris",    2, "PARTIAL-MECHANIC"),      # Bar Bill + Drink Spiking — no spiking visual
    ("side-turkey", 3, "PARTIAL-LANDMARK"),      # Manavgat Waterfall & Boat — no waterfall depicted
]

COUNTRY = "turkey"
BATCH_SIZE = 4

OUT_DIR = Path("/tmp/turkey-regen-audit3-comics")
AUDIT_LOG = Path("/tmp/turkey-regen-audit3.jsonl")
FLAG_LOG = Path("/tmp/turkey-regen-audit3-flagged.log")


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
