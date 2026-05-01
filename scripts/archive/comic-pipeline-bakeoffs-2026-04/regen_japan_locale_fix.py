#!/usr/bin/env python3
"""Regenerate 4 Japan scam comics flagged by the 2026-04-27 vision audit
for location-mismatched backdrops. The HTML location field is correct;
the prior synthesis under-weighted it, so we prepend a CRITICAL backdrop
override into the scam dict before calling synthesize_prompt.

Targets:
  hiroshima-1   Nagarekawa-Shintenchi tout — backdrop was Miyajima torii + deer
  yokohama-3    Yokohama Station West Exit tout — backdrop was Chinatown gate
  yokohama-2    Chinatown all-you-can-eat 6-order limit — depicted leftover only
  fukuoka-3     Hakata Station Tsukushi-guchi tout — generic backdrop, no station cue
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
        "hiroshima", 1,
        "Nagarekawa and Shintenchi entertainment district in Naka-ku, Hiroshima — "
        "narrow neon-lit nightlife alley with vertical Japanese cabaret/snack-bar signs "
        "in magenta, cyan, and warm amber, wet pavement reflecting neon. CRITICAL: "
        "do NOT depict the Itsukushima torii, Miyajima island, or any deer.",
        None,
    ),
    (
        "yokohama", 3,
        "Yokohama Station West Exit area (Minami-Saiwai-bashi, Nishi-ku) — visible "
        "Don Quijote (yellow penguin signage) or Bibre frontage and the JR station "
        "concourse exit. Modern station-side commercial street, evening neon. CRITICAL: "
        "do NOT depict the Yokohama Chinatown paifang/gate or red Chinese arches.",
        None,
    ),
    (
        "yokohama", 2,
        "Yokohama Chinatown (Yamashita-cho, Naka-ku) — red-and-gold Chinese restaurant "
        "interior with a cheongsam-clad tout out front pitching '¥2,500 / 90 min'.",
        "MECHANIC EMPHASIS: the distinctive scam mechanic is a hidden '6-item order limit' "
        "rule that only appears after seating, plus a separate '¥15,000 leftover surcharge'. "
        "At least one panel must show a printed RULES placard with 'MAX 6 ITEMS PER ORDER' "
        "and another panel must show the ¥15,000 leftover surcharge being added to the bill.",
    ),
    (
        "fukuoka", 3,
        "JR Hakata Station Tsukushi-guchi (east exit) — modern Japanese train station "
        "concourse with clearly legible 'Hakata' (博多) signage on the building or signs, "
        "evening commuter foot traffic, dark-suited touts approaching tourists. CRITICAL: "
        "do NOT depict Tokyo's Kabukicho, Roppongi, or Shinjuku — this is Hakata, Fukuoka.",
        None,
    ),
]

COUNTRY = "japan"
BATCH_SIZE = 4  # all 4 in parallel — they're independent

OUT_DIR = Path("/tmp/japan-locale-regen-comics")
AUDIT_LOG = Path("/tmp/japan-locale-regen-audit.jsonl")


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
        # force=True so the cache doesn't short-circuit our re-shoot
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
