#!/usr/bin/env python3
"""Regenerate 4 Spain scam comics flagged by the 2026-04-27 vision audit
for mechanic-mismatched scenes. Each comic depicted a different scam than
its title described. Per the locale-fix pattern, we prepend explicit
BACKDROP REQUIREMENT and MECHANIC EMPHASIS overrides into the scam dict
before calling synthesize_prompt.

Targets:
  gran-canaria-1   Las Palmas/Maspalomas Taxi Transfer — depicted restaurant overcharge
  granada-spain-7  Sacromonte Flamenco Cave Tout — depicted three-card monte
  madrid-5         Fake Prado/Palacio Skip-the-Line Websites — depicted pickpocket
  seville-7        Tapas Bar Bill Padding — depicted pickpocket
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
        "gran-canaria", 1,
        "Las Palmas de Gran Canaria Airport (LPA) taxi rank exterior — visible "
        "'TAXI' rank sign and metered taxis lined at the curb under modern Spanish "
        "airport canopy with palm trees, daylight Canary-island setting. CRITICAL: "
        "do NOT depict any restaurant interior, menu boards, or food.",
        "MECHANIC EMPHASIS: the scam is a TAXI TRANSFER OVERCHARGE — driver quotes "
        "€60–€90 for the LPA → Maspalomas / Playa del Inglés ride that should be "
        "€38–€45 metered. At least one panel must show the meter being switched off "
        "or covered, or the driver quoting an inflated fixed price (e.g. '€80 fixed, "
        "no meter') with the tourist's confused face. No restaurant, no food, no menu.",
    ),
    (
        "granada-spain", 7,
        "Sacromonte hillside in Granada — whitewashed cave-house entrance with the "
        "Alhambra fortress visible on the opposite hillside in background, traditional "
        "Andalusian flamenco-cave (cueva) sign in Spanish, evening warm-tone light. "
        "CRITICAL: do NOT depict any card game, three-card monte, gambling table, "
        "or street-game cups.",
        "MECHANIC EMPHASIS: the scam is a FLAMENCO CAVE TOUR HUSTLE — a street tout "
        "near Granada Cathedral or Sacromonte approaches the tourist with 'authentic "
        "flamenco show, €60' pitch holding flyers, then leads them to an inferior "
        "cueva venue. At least one panel must show the tout with flyers/business cards "
        "approaching tourists with a flamenco-show pitch, and another panel inside a "
        "dim cueva venue with disappointed tourists watching a low-quality flamenco "
        "performance. No card games, no gambling.",
    ),
    (
        "madrid", 5,
        "Madrid hotel-room desk or café table with a laptop screen prominently "
        "displaying a fake 'Prado Museum — Skip-the-Line Tickets' booking website "
        "(visible URL and a big 'BUY NOW €45' button), credit card on the table next "
        "to the laptop. Second panel exterior at the Prado Museum entrance (visible "
        "'MUSEO DEL PRADO' signage) with a security guard scanning a printed QR-code "
        "voucher that shows 'INVALID' on the scanner. CRITICAL: do NOT depict a metro, "
        "subway, map, or pickpocket.",
        "MECHANIC EMPHASIS: the scam is a FAKE TICKET WEBSITE — tourist books a "
        "'skip-the-line' Prado/Royal Palace ticket on a lookalike website, pays "
        "€45–€60 (real price is €15), then the QR code scans as INVALID at the gate. "
        "Panels must show: (1) the laptop with the fake website + 'BUY NOW' button, "
        "(2) the gate scanner showing INVALID and the disappointed tourist holding the "
        "printed voucher. No pickpockets, no metro, no map.",
    ),
    (
        "seville", 7,
        "Seville tapas bar interior in Santa Cruz / El Arenal — wooden-beamed ceiling, "
        "tile-fronted bar with hanging jamón, small plates of olives and croquetas on "
        "a wooden table, evening warm interior light, terracotta and ochre walls. "
        "CRITICAL: do NOT depict a metro, subway, map, street, or pickpocket.",
        "MECHANIC EMPHASIS: the scam is TAPAS BAR BILL PADDING — the bill arrives "
        "with phantom items the tourists never ordered, no posted prices, and a "
        "'tourist menu' surcharge. At least one panel must show a paper bill being "
        "presented at the table with shocked-tourist reaction, with line items like "
        "'pan €6', 'cubierto €4', 'tapa especial €18' visible, and another panel "
        "showing the bar without posted prices on the menu board. No pickpockets, no "
        "metro, no street scene.",
    ),
]

COUNTRY = "spain"
BATCH_SIZE = 4

OUT_DIR = Path("/tmp/spain-audit-regen-comics")
AUDIT_LOG = Path("/tmp/spain-audit-regen-audit.jsonl")


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
    print(f"[{COUNTRY}-audit-fix] regenerating {len(targets)} comics", flush=True)

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
    print(f"\n[{COUNTRY}-audit-fix] FINAL: {json.dumps(summary)}", flush=True)
    return summary


if __name__ == "__main__":
    main()
