#!/usr/bin/env python3
"""Regenerate 2 Egypt scam comics flagged by the 2026-04-28 vision audit
for location-mismatched backdrops (Cairo/Giza imagery leaking into non-Cairo
cities). Same pattern as regen_japan_locale_fix.py — prepend a CRITICAL
backdrop override into the scam dict before calling synthesize_prompt.

Targets:
  luxor-2            Fake Temple Guide — panel 4 had pyramids + Sphinx
  sharm-el-sheikh-6  Romance Scam (Bezness) — panel 4 had pyramids + Sphinx
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

# (city, n, locale_override, mechanic_override)
TARGETS = [
    (
        "luxor", 2,
        "Inside a painted-hieroglyph tomb chamber on Luxor's West Bank (Valley of the "
        "Kings) or an inner chamber of Karnak Temple — narrow stone passage with "
        "polychrome wall reliefs of Egyptian deities, low warm tomb lighting from a "
        "single bulb, and the final outdoor panel set against the Theban limestone "
        "cliffs of the West Bank or the towering hypostyle columns of Karnak. CRITICAL: "
        "do NOT depict the Pyramids of Giza, the Sphinx, Cairo, or any pyramid silhouette.",
        None,
    ),
    (
        "sharm-el-sheikh", 6,
        "Naama Bay, Sharm El Sheikh — palm-lined Red Sea hotel pool deck and beachfront "
        "promenade, turquoise water visible behind, white-stucco resort architecture, "
        "the final panel set against the Naama Bay marina or a Red Sea coastline with "
        "diving boats moored. CRITICAL: do NOT depict the Pyramids of Giza, the Sphinx, "
        "Cairo, the Nile, or any pyramid silhouette — Sharm El Sheikh is on the Red Sea "
        "Sinai coast and has none of these.",
        None,
    ),
]

COUNTRY = "egypt"
BATCH_SIZE = 2  # both in parallel — they're independent

OUT_DIR = Path("/tmp/egypt-locale-regen-comics")
AUDIT_LOG = Path("/tmp/egypt-locale-regen-audit.jsonl")


def collect_targets() -> list[dict]:
    by_city: dict[str, list[int]] = {}
    for city, n, *_ in TARGETS:
        by_city.setdefault(city, []).append(n)
    out = []
    overrides = {(c, n): (loc, mech) for c, n, loc, mech in TARGETS}
    for city, wanted_ns in sorted(by_city.items()):
        scams = extract_scams(city)
        for s in scams:
            if s["n"] not in wanted_ns:
                continue
            loc_o, mech_o = overrides[(city, s["n"])]
            if loc_o:
                s["location"] = f"{s['location']}. BACKDROP REQUIREMENT: {loc_o}"
            if mech_o:
                s["story"] = f"{mech_o}\n\n{s['story']}"
            out.append(s)
    return out


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_LOG.write_text("")

    ws_token = _keychain("wavespeed-api-key")
    r2_token = _keychain("cloudflare-api-token")

    targets = collect_targets()
    print(f"[{COUNTRY}-locale-fix] regenerating {len(targets)} comics", flush=True)

    ok = retried = flagged = 0
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=BATCH_SIZE) as ex:
        futs = [
            ex.submit(generate_one, COUNTRY, s, OUT_DIR, ws_token, r2_token, True)
            for s in targets
        ]
        for s, f in zip(targets, futs):
            try:
                res = f.result()
            except Exception as e:
                res = {"status": "flagged", "note": f"unhandled err: {e}",
                       "character": "?", "prompt": None}
            label = f"{s['city']}/scam-{s['n']}"
            line = (f"{label}: {res['status']}  char={res['character']}  ({res['note']})")
            print(f"  {line}", flush=True)
            AUDIT_LOG.open("a").write(json.dumps({
                "city": s["city"], "n": s["n"], "title": s["title"], **res,
            }) + "\n")
            if res["status"] in ("ok", "ok-cached"):
                ok += 1
            elif res["status"] == "ok-retried":
                retried += 1
                ok += 1
            else:
                flagged += 1

    summary = {
        "country": COUNTRY, "total": len(targets),
        "ok": ok, "retried": retried, "flagged": flagged,
        "elapsed_s": int(time.time() - t0),
    }
    print(f"\n[{COUNTRY}-locale-fix] FINAL: {json.dumps(summary)}", flush=True)
    return summary


if __name__ == "__main__":
    main()
