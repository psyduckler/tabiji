#!/usr/bin/env python3
"""Regenerate 5 Mexico scam comics flagged by the 2026-04-28 audit.

Targets:
  isla-mujeres-5   Tier 1 — depicts whale shark instead of MUSA underwater museum
  mexico-city-6    Tier 2 — TAPO bus terminal missing; comic shows generic taxi booth
  oaxaca-2         Tier 2 — Monte Albán/Mitla ruins missing; comic shows craft markets only
  mazatlan-2       Tier 2 — pulmonía depicted as generic golf cart
  playa-del-carmen-1  Tier 2 — Quinta Avenida pedestrian-strip identity missing

Pattern follows regen_japan_locale_fix.py: prepend BACKDROP REQUIREMENT to
the scam dict's location field before calling synthesize_prompt.
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
        "isla-mujeres", 5,
        "Isla Mujeres MUSA underwater sculpture museum — translucent turquoise "
        "Caribbean water with submerged life-size human-figure sculptures (Jason "
        "deCaires Taylor's 'The Silent Evolution') visible from a small open snorkel "
        "boat above. CRITICAL: do NOT depict whale sharks, do NOT depict large "
        "spotted fish — this is the underwater statue museum, not the whale-shark "
        "tour. Show snorkelers in masks looking down at concrete sculptures arranged "
        "on a sandy seabed.",
        "MECHANIC EMPHASIS: the scam is an unlicensed boat operator on Playa Norte "
        "claiming to take tourists to MUSA without proper permits. At least one panel "
        "must show statues underwater (not fish). One panel must show the cooperativa "
        "kiosk with 'PERMISO MUSA' or 'COOPERATIVA AUTORIZADA' signage as the safe "
        "alternative.",
    ),
    (
        "mexico-city", 6,
        "TAPO (Terminal de Autobuses de Pasajeros de Oriente) — the iconic round "
        "modernist bus terminal in Venustiano Carranza, CDMX, with curved domed roof, "
        "ADO bus livery (red/white) and visible 'TAPO' or 'AUTOBUSES DEL ORIENTE' "
        "signage. Inter-city long-distance bus terminal interior with rows of ticket "
        "counters and waiting passengers with luggage. CRITICAL: do NOT depict an "
        "airport, do NOT depict the Benito Juárez Aeropuerto.",
        None,
    ),
    (
        "oaxaca", 2,
        "Monte Albán archaeological zone — the iconic flat-topped Zapotec pyramid "
        "complex on a hilltop overlooking the Oaxaca valley, with the Gran Plaza "
        "platform visible and a hand-lettered 'INAH MONTE ALBÁN' wooden gate sign. "
        "At least two panels must show the pyramid silhouette in the background. "
        "One panel can show a Mitla/Teotitlán craft-market commission stop.",
        "MECHANIC EMPHASIS: the scam is a combined Monte Albán + Mitla day tour "
        "where the operator pads the price with mandatory commission-kickback craft "
        "stops in Teotitlán del Valle weavers' co-ops. The pyramid must visually "
        "anchor the scam in Oaxaca, not generic Mexico.",
    ),
    (
        "mazatlan", 2,
        "Mazatlán cruise port and Malecón — must show a *pulmonía*, the iconic "
        "Mazatlán open-air taxi: small white VW-Beetle-derived chassis with a "
        "striped white-and-red canvas top, no doors, two bench seats, often with "
        "a tassel fringe along the canopy edge. The cruise ship in the harbor "
        "background and Mazatlán's Cerro de la Nevería or Cerro del Crestón "
        "lighthouse hill visible. CRITICAL: do NOT depict a generic golf cart, "
        "do NOT depict an enclosed taxi — this is the open-canopy *pulmonía* and "
        "it's the visual identity of Mazatlán.",
        None,
    ),
    (
        "playa-del-carmen", 1,
        "Quinta Avenida (5th Avenue) pedestrian shopping strip in Playa del Carmen "
        "— car-free cobblestone street lined with thatched-palapa-roof bars and "
        "open-air restaurants, hand-painted signs, tropical greenery, sidewalk "
        "menu boards. Iconic 5a-Avenida lamp posts. The 'Quinta Av' or '5a Av' "
        "street sign visible in at least one panel. Pedestrians strolling, no cars. "
        "CRITICAL: this is a wide pedestrian promenade, not a narrow alley.",
        "MECHANIC EMPHASIS: the scam is a 'tourist menu' restaurant on Quinta "
        "Avenida that shows low prices on the street menu and swaps in a higher-"
        "priced indoor menu after seating, plus auto-applied 18% gratuity.",
    ),
]

COUNTRY = "mexico"
BATCH_SIZE = 5

OUT_DIR = Path("/tmp/mexico-audit-regen-2026-04-28")
AUDIT_LOG = Path("/tmp/mexico-audit-regen-2026-04-28.jsonl")


def collect_targets() -> list[dict]:
    by_city: dict[str, list[int]] = {}
    for city, n, *_ in TARGETS:
        by_city.setdefault(city, []).append(n)
    overrides = {(c, n): (loc, mech) for c, n, loc, mech in TARGETS}
    out = []
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
    print(f"[{COUNTRY}-audit] regenerating {len(targets)} comics", flush=True)

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
            print(f"  {label}: {res['status']}  char={res.get('character', '?')}  "
                  f"({res.get('note', '')})", flush=True)
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
    print(f"\n[{COUNTRY}-audit] FINAL: {json.dumps(summary)}", flush=True)
    return summary


if __name__ == "__main__":
    main()
