#!/usr/bin/env python3
"""Regenerate lagos-portugal/scam-5 — flagged by the 2026-04-28 Portugal audit.

The prior comic landed with empty solid red/yellow backdrops, no Portuguese
architectural cues (azulejo, calçada, terracotta), and a figure-rendering
style closer to Christoph Niemann than the locked José de Guimarães folk-pop
modernist Portugal style.

Inject a strong BACKDROP REQUIREMENT anchored to Lagos Old Town visual cues
plus a MECHANIC override that pins the bar-strip overcharge specifics.
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
        "lagos-portugal", 5,
        "Rua 25 de Abril nightlife strip in Lagos Algarve Old Town — "
        "narrow pedestrian cobblestone street paved in calçada portuguesa "
        "(black-and-white Portuguese wave-pattern stones), whitewashed "
        "Algarve Old Town buildings with terracotta-tiled roofs and "
        "blue-and-white azulejo tile panels on the lower walls, traditional "
        "Portuguese wrought-iron balconies above bar fronts. Visible signage "
        "in Portuguese (e.g. 'Cerveja', 'Vinho do Porto', 'Aberto'). Warm "
        "summer-evening light. CRITICAL: do NOT depict empty flat-color walls; "
        "every panel must include at least one Portuguese architectural cue "
        "(azulejo tiles, calçada cobbles, terracotta roof, or whitewashed "
        "Algarve facade with blue trim).",
        "MECHANIC: A tourist couple is approached by a tout outside a Rua 25 "
        "de Abril bar offering 'Happy Hour 2-for-1 cocktails — €8'. They sit "
        "down. The bartender pours, then runs a 'free welcome shot' onto the "
        "tab. The bill arrives at €32 for the same drinks because the second "
        "round was upcharged to a 'premium spirit' tier. At least one panel "
        "must show a chalkboard/menu reading 'HAPPY HOUR 2-for-1 €8' next to "
        "the tout pitch; another panel must show the bill totalling €32 with "
        "the tourist visibly shocked. Every panel must show clear José de "
        "Guimarães folk-pop modernist styling — bold flat hand-painted shapes "
        "with strong black outline, saturated Portuguese flag red + cobalt "
        "blue + mustard yellow + white + black palette only.",
    ),
]

COUNTRY = "portugal"
OUT_DIR = Path("/tmp/lagos-regen-comics")
AUDIT_LOG = Path("/tmp/lagos-regen-audit.jsonl")


def collect_targets() -> list[dict]:
    by_city: dict[str, list[int]] = {}
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
    print(f"[{COUNTRY}-lagos-5] regenerating {len(targets)} comics", flush=True)

    ok = retried = flagged = 0
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=1) as ex:
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
    print(f"\n[{COUNTRY}-lagos-5] FINAL: {json.dumps(summary)}", flush=True)


if __name__ == "__main__":
    main()
