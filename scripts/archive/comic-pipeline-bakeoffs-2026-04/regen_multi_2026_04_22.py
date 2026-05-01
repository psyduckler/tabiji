#!/usr/bin/env python3
"""Regenerate 10 fallback scam comics across 2 countries via v2 pipeline.

These 10 are the comics identified in the 2026-04-22 cross-country audit
of all 41 country hubs + 1,650 comics as remaining v1 fallback artifacts.
Per-scam list in FLAGGED below. Everything else stays untouched.

Findings from the audit:
- 41 country hubs surveyed, 20 have comics deployed, 1,650 total comics
- 18 of 20 countries are clean (0 within-country phash near-dups ≤60)
- Only US and CN have remaining fallbacks:

  CN — 1 leftover cross-city exact duplicate missed in yesterday's
       (2026-04-21) China regen because the two comics have different
       scam titles but the v1 pipeline uploaded the identical JPEG to
       both R2 paths:
    - guilin/scam-4 ≡ xian/scam-7  (tea-house template, phash = 0)

  US — 8 comics where the v1 "Times Square character shakedown"
       template ("Got a minute, bro?" / "Twenty bucks helps out!" /
       "Take it back — no thanks!" / "Trust nothing pressed in your
       hand") leaked onto scams with entirely different mechanics.
       Canonical kept: new-york-city/scam-4 (the actual Times Square
       character shakedown scam). Regens:
    - new-york-city/scam-2 (Fake Statue of Liberty Tickets — should
       show fake-ticket reseller / QR-fail at Battery Park ferry)
    - maui/scam-6 (Post-Lahaina Wildfire Recovery — should show
       fake insurance adjuster at wildfire-damaged property)
    - san-antonio/scam-4 (Alamo Mission Ticket — should show fake
       ticket booth outside the Alamo, which has free admission)
    - seattle/scam-1 (Tap-to-Pay Charity Fraud — should show NFC
       phone/card skim, not street shakedown)
    - new-orleans/scam-4 (Bourbon Street Shot Girls — should show
       bar scene with shot-girls lure + bill shock)
    - new-orleans/scam-1 (Shoe Bet Hustle — should show the
       specific French Quarter "I bet I can tell you where you got
       your shoes!" bet scam)
    - charleston/scam-1 (Palmetto Rose — should show palm-frond
       weaving / forced-gift mechanic, not generic street shakedown)
    - san-francisco/scam-2 (Fake Buddhist Monk Bracelet — borderline,
       should show fake-monk figure specifically)
    - savannah/scam-2 (Savannah Monk / River Street Donation —
       borderline, should show fake-monk figure specifically)

Uses the same generate_one() from generate.py so behavior is identical
to a full-country v2 run, just scoped to these specific (country, city, n)
targets. Iterates per-country internally so each scam gets the correct
locked STYLE + PILOT anchor.

Run:
    python3 scripts/comic-pipeline/regen_multi_2026_04_22.py
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

# (country_key, city_slug, scam_n, reason)
# country_key matches STYLES/PILOTS keys in styles.py
FLAGGED = [
    ("china",         "guilin",         4, "CN-CROSS-CITY-DUP"),       # pixel-identical to xian-7
    ("united-states", "new-york-city",  2, "US-SHAKEDOWN-TEMPLATE"),   # Statue of Liberty Tickets
    ("united-states", "maui",           6, "US-SHAKEDOWN-TEMPLATE"),   # Post-Lahaina wildfire
    ("united-states", "san-antonio",    4, "US-SHAKEDOWN-TEMPLATE"),   # Alamo ticket
    ("united-states", "seattle",        1, "US-SHAKEDOWN-TEMPLATE"),   # Tap-to-Pay charity
    ("united-states", "new-orleans",    4, "US-SHAKEDOWN-TEMPLATE"),   # Bourbon Street shot girls
    ("united-states", "new-orleans",    1, "US-SHAKEDOWN-TEMPLATE"),   # Shoe bet hustle
    ("united-states", "charleston",     1, "US-SHAKEDOWN-TEMPLATE"),   # Palmetto rose
    ("united-states", "san-francisco",  2, "US-SHAKEDOWN-TEMPLATE"),   # Fake monk bracelet (borderline)
    ("united-states", "savannah",       2, "US-SHAKEDOWN-TEMPLATE"),   # Monk donation (borderline)
]

BATCH_SIZE = 3

OUT_DIR = Path("/tmp/multi-regen-2026-04-22-comics")
AUDIT_LOG = Path("/tmp/multi-regen-2026-04-22-audit.jsonl")
FLAG_LOG = Path("/tmp/multi-regen-2026-04-22-flagged.log")


def collect_targets() -> list[tuple[str, dict, str]]:
    """Returns list of (country_key, scam_dict, reason) tuples."""
    by_city: dict[str, list[tuple[int, str, str]]] = {}
    for country_key, city, n, reason in FLAGGED:
        by_city.setdefault(city, []).append((n, country_key, reason))
    out = []
    for city, wants in sorted(by_city.items()):
        scams = extract_scams(city)
        by_n = {s["n"]: s for s in scams}
        wanted_ns = {n for n, _, _ in wants}
        missing = wanted_ns - set(by_n)
        if missing:
            raise RuntimeError(f"{city}: could not extract scams {sorted(missing)} from HTML")
        for n, country_key, reason in wants:
            out.append((country_key, by_n[n], reason))
    return out


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_LOG.write_text("")
    FLAG_LOG.write_text("")

    ws_token = _keychain("wavespeed-api-key")
    r2_token = _keychain("cloudflare-api-token")

    targets = collect_targets()
    print(f"[multi] regenerating {len(targets)} flagged scams (batch={BATCH_SIZE})",
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
                ex.submit(generate_one, country_key, s, OUT_DIR, ws_token, r2_token, False)
                for country_key, s, _ in batch
            ]
            for (country_key, s, reason), f in zip(batch, futs):
                try:
                    res = f.result()
                except Exception as e:
                    res = {"status": "flagged", "note": f"unhandled err: {e}",
                           "character": "?", "prompt": None}
                label = f"{country_key}/{s['city']}/scam-{s['n']}"
                line = (f"{label}  [{reason}]: {res['status']}  "
                        f"char={res['character']}  ({res['note']})")
                print(f"  {line}", flush=True)
                AUDIT_LOG.open("a").write(json.dumps({
                    "country": country_key, "city": s["city"], "n": s["n"],
                    "title": s["title"], "reason": reason, **res,
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
        "scope": "multi-country",
        "total": len(targets),
        "ok": ok, "retried": retried, "flagged": flagged,
        "elapsed_s": int(time.time() - t0),
        "audit_log": str(AUDIT_LOG), "flagged_log": str(FLAG_LOG),
    }
    print(f"\n[multi] FINAL: {json.dumps(summary)}", flush=True)
    return summary


if __name__ == "__main__":
    main()
