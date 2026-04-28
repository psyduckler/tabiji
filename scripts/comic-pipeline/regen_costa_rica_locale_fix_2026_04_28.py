#!/usr/bin/env python3
"""Regenerate 6 Costa Rica scam comics flagged by the 2026-04-28 vision audit.

Targets:
  monteverde-1..5  ecosystem mismatch — current comics use lowland tropical
                   jungle (palms, macaws, toucans, bright sun) but Monteverde
                   is a 1,400m cool misty cloud forest. Override backdrop.
  tortuguero-2     panel 2 incorrectly shows a graveyard with crosses;
                   should be a moonlit beach turtle-walk scene.

Pattern adapted from regen_japan_locale_fix.py — inject CRITICAL backdrop
override into scam.location before synthesize_prompt is called.
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

CLOUD_FOREST = (
    "Monteverde Cloud Forest, Santa Elena, Puntarenas — high-elevation "
    "(~1,400m) cloud forest with cool misty air and low-hanging fog "
    "drifting between gnarled moss-covered oak and Cecropia trees, dense "
    "epiphytes and bromeliads on every branch, soft diffuse silver-green "
    "light, cooler subdued palette of mossy emerald, slate, fog white, and "
    "muted teal, occasional resplendent quetzal or bellbird as discreet "
    "wildlife. CRITICAL: do NOT depict palm trees, macaws, toucans, sloths, "
    "bright equatorial sun, or any lowland-tropical beach foliage — this is "
    "cloud forest at altitude, not the Pacific or Caribbean coast."
)

# (city, n, locale_override, mechanic_override)
TARGETS = [
    (
        "monteverde", 1,
        f"Cloud Forest Reserve gate (entrance kiosk on the road from Santa "
        f"Elena village). {CLOUD_FOREST}",
        None,
    ),
    (
        "monteverde", 2,
        f"Winding mountain road from Santa Elena down toward La Fortuna or "
        f"the Pan-American Highway, hairpin turns through cloud forest. "
        f"{CLOUD_FOREST}",
        None,
    ),
    (
        "monteverde", 3,
        f"Hostel front desk inside a small Santa Elena village hostel — "
        f"wooden cabin interior with a tour-booking corkboard, view of misty "
        f"cloud forest visible through the window. {CLOUD_FOREST}",
        None,
    ),
    (
        "monteverde", 4,
        f"Pickup zone in Santa Elena village at dusk for a Jeep-Boat-Jeep "
        f"shuttle to La Fortuna — small mountain town main street, cool "
        f"evening mist. {CLOUD_FOREST}",
        None,
    ),
    (
        "monteverde", 5,
        f"Tourist booking a Monteverde tour on a laptop from a small "
        f"Santa Elena village cafe — interior scene with cloud forest mist "
        f"visible through window. {CLOUD_FOREST}",
        None,
    ),
    (
        "tortuguero", 2,
        "Tortuguero National Park beach at night, moonlit black-sand "
        "Caribbean beach with the surf line visible, palm-fringed jungle "
        "set back from the beach, an unlicensed 'guide' in dark clothing "
        "leading a tourist toward the surf where a sea turtle is laying "
        "eggs in the sand. CRITICAL: do NOT depict any graveyard, "
        "tombstones, crosses, or cemetery imagery — this is a sea-turtle "
        "nesting beach scene, the scam mechanic is unlicensed turtle-walk "
        "guides flouting the park's licensed-guide rule.",
        "MECHANIC EMPHASIS: scene must show an unlicensed guide approaching "
        "tourists on the moonlit beach with sea turtles visibly nesting in "
        "the sand. No graveyards, no tombstones — only beach, ocean, and "
        "turtles.",
    ),
]

COUNTRY = "costa-rica"
BATCH_SIZE = 6  # all 6 in parallel — independent

OUT_DIR = Path("/tmp/costa-rica-locale-regen-comics")
AUDIT_LOG = Path("/tmp/costa-rica-locale-regen-audit.jsonl")


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
            line = f"{label}: {res['status']}  char={res['character']}  ({res['note']})"
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
