#!/usr/bin/env python3
"""Regenerate 7 Mexico scam comics flagged in the 2026-04-28 audit for
weak/generic landmark backdrops. Pattern follows regen_mexico_audit_2026_04_28.py
and regen_japan_locale_fix.py — prepend BACKDROP REQUIREMENT to scam dict's
location field before calling synthesize_prompt.

Targets:
  acapulco-1        Cartel-zone DM trap — generic urban skyline (need Bay + Sierra de Guerrero contrast)
  holbox-1          Chiquilá ferry — boat shaped like cruise ship (need flat passenger ferry)
  isla-mujeres-6    Avenida Hidalgo — generic streetscape, no Hidalgo St signage
  mexico-city-3     Zócalo phone-snatch — Catedral indistinct
  tulum-1           Ruins conservation fee — generic pyramid, missing clifftop-over-Caribbean
  puerto-vallarta-5 Los Muertos photographer — generic pier, missing spiral seahorse arch
  puerto-escondido-6 Carrizalillo henna — desert/cactus backdrop wrong for tropical Pacific
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
        "acapulco", 1,
        "Acapulco Bay's iconic crescent — at least one panel must show the "
        "distinctive curved crescent of high-rise hotels along Costera Miguel "
        "Alemán wrapping a turquoise bay (the unmistakable visual identity of "
        "Acapulco). A separate panel can show the contrast: rural Sierra de "
        "Guerrero — unpaved mountain back-road, scrubby pine forest, an "
        "unmarked SUV pulled over with masked figures (NO weapons depicted "
        "in the comic, just hooded figures so the threat is implied). "
        "CRITICAL: do NOT depict generic Mexican urban skyline — Acapulco's "
        "crescent bay is non-negotiable.",
        None,
    ),
    (
        "holbox", 1,
        "Chiquilá mainland ferry pier — a flat single-deck passenger ferry "
        "boat (NOT a cruise ship, NOT a yacht), with 'HOLBOX EXPRESS' or "
        "'9 HERMANOS' branding on the side, blue-and-white livery. Ferry "
        "is open at the back with rows of bench seating, suitable for "
        "20-minute crossing. Dusty mainland parking strip with disorganized "
        "cars and 'parking attendants' in fluorescent vests waving cars in. "
        "Mangrove vegetation, turquoise shallow water in the background. "
        "CRITICAL: do NOT depict a multi-deck cruise ship, do NOT depict a "
        "yacht — this is a flat passenger ferry.",
        None,
    ),
    (
        "isla-mujeres", 6,
        "Avenida Hidalgo, Isla Mujeres' main pedestrian tourist strip — "
        "narrow car-free cobblestone street lined with brightly painted "
        "two-story buildings (Caribbean turquoise, coral pink, marigold "
        "yellow), hand-painted shop signs, tropical foliage, palm trees. "
        "At least one panel must show 'AV. HIDALGO' or 'AVENIDA HIDALGO' "
        "street signage clearly. White domed Iglesia de la Inmaculada "
        "Concepción visible in one panel. Golf carts (no cars on Isla "
        "Mujeres) in the periphery. Souvenir shops with hammocks and "
        "sarapes hung outside. CRITICAL: do NOT depict a generic narrow "
        "Mexican alley — Avenida Hidalgo's pedestrian Caribbean-painted "
        "identity is the visual anchor.",
        None,
    ),
    (
        "mexico-city", 3,
        "Zócalo, Mexico City — the massive central plaza with the "
        "Catedral Metropolitana DOMINANTLY visible: a pink-stone Spanish "
        "baroque cathedral with TWIN BELL TOWERS (one slightly taller "
        "than the other) and a central dome, on the NORTH side of the "
        "plaza. The giant Mexican flag (red-white-green tricolor) on a "
        "tall white flagpole at the center of Zócalo. Cobblestone plaza "
        "ground, sparse pedestrians. CRITICAL: the Catedral must be "
        "RECOGNIZABLE in at least 2 panels — pink stone, twin towers, "
        "central dome — not a vague distant building.",
        None,
    ),
    (
        "tulum", 1,
        "Tulum Archaeological Zone — the iconic El Castillo Mayan pyramid "
        "perched on a CLIFF EDGE above the turquoise Caribbean Sea, with "
        "white sandy beach visible far below the cliff. This clifftop-over-"
        "Caribbean position is Tulum's unique visual identity, distinct "
        "from inland Mayan sites. Wooden 'ZONA ARQUEOLÓGICA DE TULUM' or "
        "'INAH' gate sign at the entrance. Tour-guide tout in white shirt "
        "at the gate area. Stone walls of the perimeter. CRITICAL: the "
        "pyramid MUST be on a coastal cliff with sea visible — generic "
        "jungle pyramids do NOT capture Tulum.",
        None,
    ),
    (
        "puerto-vallarta", 5,
        "Playa Los Muertos and the Muelle de Los Muertos — Puerto Vallarta's "
        "iconic public beach with the distinctive curving METAL SCULPTURE "
        "PIER (Muelle de Los Muertos): a long sand-colored concrete pier "
        "extending into Banderas Bay, with a tall curling metal sail-like "
        "sculpture at the seaward end (resembles a crashing wave or seahorse "
        "spiral). Banderas Bay mountains visible in the distance, palm trees, "
        "pelicans. Sand beach with vendors and tourist umbrellas. A 'friendly "
        "photographer' with a DSLR camera approaching the family. CRITICAL: "
        "the spiral/wave-shaped pier sculpture is the unmistakable visual "
        "identity of Los Muertos pier — must be in at least 2 panels.",
        None,
    ),
    (
        "puerto-escondido", 6,
        "Playa Carrizalillo, Puerto Escondido — small cove beach surrounded "
        "by tall palm-tree-topped cliffs on both sides, white sand, "
        "TROPICAL Pacific turquoise water with surfers paddling offshore, "
        "long stairway descending the cliff to the beach. Beach palapas "
        "(thatched-roof shelters), surfboards stuck in the sand. A henna-"
        "tattoo vendor with a small folding table and ink bottles "
        "approaching a tourist. CRITICAL: do NOT depict desert, do NOT "
        "depict cactus, do NOT depict arid landscape — Puerto Escondido is "
        "a tropical Pacific surf town with lush palm cliffs.",
        None,
    ),
]

COUNTRY = "mexico"
BATCH_SIZE = 7

OUT_DIR = Path("/tmp/mexico-landmarks-regen-2026-04-28")
AUDIT_LOG = Path("/tmp/mexico-landmarks-regen-2026-04-28.jsonl")


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
    print(f"[{COUNTRY}-landmarks] regenerating {len(targets)} comics", flush=True)

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
    print(f"\n[{COUNTRY}-landmarks] FINAL: {json.dumps(summary)}", flush=True)
    return summary


if __name__ == "__main__":
    main()
