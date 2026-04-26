#!/usr/bin/env python3
"""Regenerate 4 flagged Turkey scam comics — audit #2 (2026-04-26).

These 4 are the comics identified in the 2026-04-26 visual audit of all 78
Turkey scam comics that the earlier 2026-04-21 audit (regen_turkey.py) missed.
Three share a faulty "premium lunch add-on" template that defaulted to a
restaurant scene whenever the scam title contained "Bundle"; the fourth
applied the friendly-stranger clip-joint lure to an in-club extortion title.

Reason codes:
  BUNDLE-LUNCH-MISAPPLIED — recycled lunch/buffet upsell template
                            ("Premium lunch add-on — 600!" / "Just a basic
                            buffet!") applied to multi-stop or multi-site
                            day-tour bundle scams whose real mechanic is
                            mandatory carpet/jewelry shopping stops or
                            combined-ruins-tour overcharge, not lunch upsell
  CLIPJOINT-MISAPPLIED    — recycled friendly-stranger "let's have a drink"
                            lure template applied to a nightclub bouncer
                            bill-extortion scam whose real mechanic happens
                            inside the club, not from a harbor invitation

Uses the same generate_one() from generate.py so behavior is identical to a
full-country v2 run, just scoped to these specific (city, n) pairs.

Run:
    python3 scripts/comic-pipeline/regen_turkey_audit2.py
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
    ("konya",       5, "BUNDLE-LUNCH-MISAPPLIED"),  # Cappadocia-Konya Day Tour Bundle Reseller Markup
    ("pamukkale",   2, "BUNDLE-LUNCH-MISAPPLIED"),  # Pamukkale Day-Trip Tour Bundled Shopping Stops
    ("side-turkey", 5, "BUNDLE-LUNCH-MISAPPLIED"),  # Aspendos & Perge 'Combined Day Tour' Bundle Overcharge
    ("bodrum",      1, "CLIPJOINT-MISAPPLIED"),     # Nightclub Bar Bill Extortion
]

COUNTRY = "turkey"
BATCH_SIZE = 3

OUT_DIR = Path("/tmp/turkey-regen-audit2-comics")
AUDIT_LOG = Path("/tmp/turkey-regen-audit2.jsonl")
FLAG_LOG = Path("/tmp/turkey-regen-audit2-flagged.log")


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
