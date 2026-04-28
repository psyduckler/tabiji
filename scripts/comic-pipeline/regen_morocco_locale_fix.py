#!/usr/bin/env python3
"""Regenerate 4 Morocco scam comics flagged by the 2026-04-28 vision audit
for weak/generic locale signal. The HTML location field is correct; the
prior synthesis under-weighted it, so we prepend a CRITICAL backdrop
override into the scam dict before calling synthesize_prompt.

Targets:
  casablanca-2  Fake Guide and Medina Commission Hustle — generic medina
  casablanca-6  Aggressive Souvenir Shop Pressure Sales — generic shop
  rabat-4       Rue Souika Argan & Spice Pharmacy — generic medina shop
  rabat-5       Medina Restaurant Menu Switch — generic medina restaurant

After regen, bumps the ?v=1 cache-bust on the 4 affected <img> tags to ?v=2.
"""
from __future__ import annotations

import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import extract_scams, generate_one, _keychain  # noqa: E402

# (city, n, locale_override, mechanic_override)
TARGETS = [
    (
        "casablanca", 2,
        "Casablanca's Ancienne Médina near Bab Marrakech with the white minaret "
        "of the Hassan II Mosque visible in the distance and 1930s French-colonial "
        "Mauresque buildings flanking the plaza. CRITICAL: do NOT depict a "
        "Marrakech-style red-clay souk or a Fez-style tannery — this is Casablanca's "
        "distinctive whitewashed colonial-medina mix with the Hassan II Mosque's "
        "minaret clearly on the horizon.",
        None,
    ),
    (
        "casablanca", 6,
        "Quartier des Habous (the New Medina) in Casablanca — distinctive 1930s "
        "French-colonial Spanish-Moorish architecture with sand-colored arched "
        "arcades, ornate stone arches over shop fronts, and an orderly street "
        "grid. CRITICAL: this is NOT a chaotic Marrakech-style souk; Habous is a "
        "planned colonial-era shopping quarter with regular geometric arcades.",
        None,
    ),
    (
        "rabat", 4,
        "Rue Souika in the Rabat medina — narrow shop-lined street with whitewashed "
        "walls and a distinctive BLUE lower-half wash painted onto the lower 1.5 "
        "meters of the medina walls (Rabat/Salé Andalusian style). Hassan Tower "
        "(12th-century unfinished red-sandstone minaret) optionally visible in the "
        "distance. CRITICAL: do NOT depict an all-blue Chefchaouen-style street or "
        "a Marrakech-red souk — Rabat's medina is mostly white with blue trim.",
        None,
    ),
    (
        "rabat", 5,
        "Restaurant interior on Rue des Consuls in the Rabat medina — visible "
        "whitewashed-and-blue-trim Andalusian-style architecture through the door "
        "or window, with the medina's distinctive lower-blue/upper-white wall "
        "treatment. The Kasbah of the Udayas (white-and-blue stone gate) "
        "optionally visible in the background. CRITICAL: signal Rabat with the "
        "white-and-blue Andalusian palette; do NOT use generic Moroccan medina.",
        None,
    ),
]

COUNTRY = "morocco"
BATCH_SIZE = 4

OUT_DIR = Path("/tmp/morocco-locale-regen-comics")
AUDIT_LOG = Path("/tmp/morocco-locale-regen-audit.jsonl")
REPO = Path(__file__).resolve().parents[2]


def collect_targets() -> list[dict]:
    by_city: dict[str, list[int]] = {}
    for city, n, *_ in TARGETS:
        by_city.setdefault(city, []).append(n)
    out: list[dict] = []
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


def bump_cache_bust(city: str, n: int) -> None:
    """Bump ?v=N -> ?v=(N+1) on the scam-N img tag in scams/<city>/index.html."""
    path = REPO / f"scams/{city}/index.html"
    html = path.read_text()
    pat = re.compile(
        rf'(src="https://img\.tabiji\.ai/scams/{city}/scam-{n}\.jpg\?v=)(\d+)(")'
    )
    m = pat.search(html)
    if not m:
        print(f"    [cache-bump] {city}/scam-{n}: pattern not found — skip", flush=True)
        return
    new_v = int(m.group(2)) + 1
    new_html = html[: m.start(2)] + str(new_v) + html[m.end(2):]
    path.write_text(new_html)
    print(f"    [cache-bump] {city}/scam-{n}: v={m.group(2)} -> v={new_v}", flush=True)


def main() -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_LOG.write_text("")

    ws_token = _keychain("wavespeed-api-key")
    r2_token = _keychain("cloudflare-api-token")

    targets = collect_targets()
    print(f"[{COUNTRY}-locale-fix] regenerating {len(targets)} comics", flush=True)

    ok = retried = flagged = 0
    succeeded: list[tuple[str, int]] = []
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
            print(f"  {label}: {res['status']}  char={res['character']}  ({res['note']})", flush=True)
            AUDIT_LOG.open("a").write(json.dumps({
                "city": s["city"], "n": s["n"], "title": s["title"], **res,
            }) + "\n")
            if res["status"] in ("ok", "ok-cached"):
                ok += 1
                succeeded.append((s["city"], s["n"]))
            elif res["status"] == "ok-retried":
                retried += 1
                ok += 1
                succeeded.append((s["city"], s["n"]))
            else:
                flagged += 1

    print(f"\n[{COUNTRY}-locale-fix] bumping cache-bust on {len(succeeded)} HTML img tags", flush=True)
    for city, n in succeeded:
        bump_cache_bust(city, n)

    summary = {
        "country": COUNTRY, "total": len(targets),
        "ok": ok, "retried": retried, "flagged": flagged,
        "elapsed_s": int(time.time() - t0),
    }
    print(f"\n[{COUNTRY}-locale-fix] FINAL: {json.dumps(summary)}", flush=True)
    return summary


if __name__ == "__main__":
    main()
