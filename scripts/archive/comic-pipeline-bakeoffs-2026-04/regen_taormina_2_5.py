#!/usr/bin/env python3
"""Regenerate taormina/scam-2 and taormina/scam-5 — the wrong comics were inserted.

The 2026-04-27 audit found the alt-text (which describes the comic content)
matches a different scam than the displayed scam title:

  scam-2 title: "The Teatro Antico 'Skip-the-Line' Ticket Markup"
  scam-2 alt:   "Mount Etna Unlicensed Guide & Summit-Access Scam"

  scam-5 title: "The Corso Umberto 'Pesce al Etto' Restaurant Trap"
  scam-5 alt:   "Mazzarò & Spisone Lido Minimum-Spend Ambush"

Inject MECHANIC + BACKDROP overrides so the regen depicts the right scam.
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

TARGETS = [
    (
        "taormina", 2,
        "Teatro Antico (Greek-Roman amphitheater) on Via Teatro Greco — visible "
        "ancient theater stones, Mount Etna in the distance behind the stage. The "
        "scammer is at a Corso Umberto ticket-booth / Piazza IX Aprile kiosk pitching "
        "'Skip the Line' tickets at €25 versus the official €14 ticketing window.",
        "MECHANIC: Tourist offered 'skip the line' Teatro Antico ticket at €25 by a "
        "tout-kiosk on Corso Umberto / Piazza IX Aprile. They pay, walk to the theater, "
        "and discover (a) there's no real queue and (b) the official price is €14 "
        "(half what they paid). At least one panel must show the official ticket window "
        "with the €14 'intero' price visible; another must show the tourist holding the "
        "€25 third-party resale ticket realizing the markup.",
    ),
    (
        "taormina", 5,
        "Corso Umberto pedestrian strip in Taormina at outdoor terrace tables — "
        "umbrellas, Piazza IX Aprile or Piazza Vittorio Emanuele backdrop. NOT a "
        "beach lido; NOT Mazzarò bay. This is the 800-metre Corso Umberto pedestrian "
        "shopping street.",
        "MECHANIC: Tourist orders fish at a Corso Umberto restaurant. Menu lists fish "
        "as 'pesce al etto' (price per 100g) but the server brings a whole large fish "
        "without quoting weight. Bill arrives with a triple-digit fish price plus "
        "€3-4/person coperto plus 'service charge' — totals far above the menu list. "
        "At least one panel must show the menu reading '€8 al etto' (or similar small "
        "per-100g number); another panel must show the bill with a much larger total "
        "(e.g., €120+ for the fish alone) and the tourist visibly shocked.",
    ),
]

COUNTRY = "italy"
OUT_DIR = Path("/tmp/taormina-regen-comics")
AUDIT_LOG = Path("/tmp/taormina-regen-audit.jsonl")


def collect_targets() -> list[dict]:
    by_city = {}
    for city, n, *_ in TARGETS:
        by_city.setdefault(city, []).append(n)
    overrides = {(c, n): (loc, mech) for c, n, loc, mech in TARGETS}
    out = []
    for city, wanted_ns in by_city.items():
        scams = extract_scams(city)
        for s in scams:
            if s["n"] not in wanted_ns:
                continue
            loc_o, mech_o = overrides[(city, s["n"])]
            s["location"] = f"{s['location']}. BACKDROP REQUIREMENT: {loc_o}"
            s["story"] = f"{mech_o}\n\n{s['story']}"
            out.append(s)
    return out


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_LOG.write_text("")

    ws_token = _keychain("wavespeed-api-key")
    r2_token = _keychain("cloudflare-api-token")

    targets = collect_targets()
    print(f"[{COUNTRY}] regenerating {len(targets)} flagged scams", flush=True)

    ok = retried = flagged = 0
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=2) as ex:
        futs = [ex.submit(generate_one, COUNTRY, s, OUT_DIR, ws_token, r2_token, True)
                for s in targets]
        for s, f in zip(targets, futs):
            try:
                res = f.result()
            except Exception as e:
                res = {"status": "flagged", "note": f"unhandled err: {e}",
                       "character": "?", "prompt": None}
            label = f"{s['city']}/scam-{s['n']}"
            print(f"  {label}: {res['status']}  char={res['character']}  ({res['note']})",
                  flush=True)
            AUDIT_LOG.open("a").write(json.dumps({
                "city": s["city"], "n": s["n"], "title": s["title"], **res,
            }) + "\n")
            if res["status"] in ("ok", "ok-cached"):
                ok += 1
            elif res["status"] == "ok-retried":
                retried += 1; ok += 1
            else:
                flagged += 1

    summary = {
        "country": COUNTRY, "total": len(targets),
        "ok": ok, "retried": retried, "flagged": flagged,
        "elapsed_s": int(time.time() - t0),
    }
    print(f"\n[{COUNTRY}] FINAL: {json.dumps(summary)}", flush=True)


if __name__ == "__main__":
    main()
