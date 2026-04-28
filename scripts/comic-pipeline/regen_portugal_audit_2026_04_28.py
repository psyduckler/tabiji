#!/usr/bin/env python3
"""Regenerate 12 Portugal scam comics flagged by the 2026-04-28 vision audit.

Three defect classes — each addressed via a targeted prefix injection on the
mechanic (story) field that the synthesis prompt receives:

  Text typos (3): garbled words baked into prior generations
    faro/scam-2     placard reads "PRYIA" (should be "PRIYA")
    faro/scam-7     panel caption reads "Via Verde rental car retintal transponder"
    funchal/scam-5  panel caption reads "wond 'wine cooperative'"

  Panel-number structural defects (4)
    porto/scam-4    numbers in bottom-right instead of upper-left
    sintra/scam-1   stacked 1/2/3/4 chip in central gutter
    coimbra/scam-1  panel 4 missing its number
    coimbra/scam-4  all 4 panel numbers missing

  Style/rendering inconsistencies within a comic (5)
    sintra/scam-3   "Guide:" / "Priya:" script-style bubble attributions
    funchal/scam-4  painterly skin shading in 2 panels, flat in other 2
    cascais/scam-5  parking attendant rendered with uniform red skin tones
    coimbra/scam-5  softer painterly skin shading vs flat-fill in others
    nazare/scam-2   pixel-blended face rendering vs flat-fill in others
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

# Reusable emphasis blocks that prefix the story field.
PANEL_NUMBER_FIX = (
    "STYLE EMPHASIS: each of the 4 panels MUST display its panel number "
    "(1, 2, 3, or 4) clearly in the UPPER-LEFT corner of its own panel — "
    "small printed numerals on a clean background, NOT in any other corner, "
    "NOT stacked together in a center chip or gutter, NOT omitted. Every "
    "panel individually carries its own upper-left corner number."
)
FLAT_FILL_FIX = (
    "STYLE EMPHASIS: every panel must render in identical flat-fill folk-pop "
    "modernist style — bold flat hand-painted shapes with strong black "
    "outlines and the saturated Portuguese flag red + cobalt blue + mustard "
    "yellow + white + black palette. NO painterly skin shading, NO "
    "pixel-blended rendering, NO panel-to-panel rendering variation. All "
    "four panels must look like they came from the same hand."
)
BARE_BUBBLES = (
    "STYLE EMPHASIS: speech bubbles are BARE — no 'Speaker:' or 'Name:' or "
    "'Guide:' or 'Priya:' name attributions inside or outside the bubble. "
    "Bubbles contain dialogue text only; the speaker is identified by the "
    "bubble's pointer tail."
)
NATURAL_SKIN = (
    "STYLE EMPHASIS: figure skin tones must be natural and consistent across "
    "all panels — no red-saturated, sunburn-toned, or color-anomalous skin. "
    "Use the standard flat-fill warm-tan / fair-pink palette consistent with "
    "the José de Guimarães Portugal house style."
)

# (city, n, locale_override, mechanic_override)
TARGETS = [
    # ---------------- Text typos (3) ----------------
    (
        "faro", 2, None,
        "MECHANIC EMPHASIS: any printed signage, placards, or text-on-image "
        "showing the canonical character name must be spelled exactly "
        "'PRIYA' (P-R-I-Y-A, five letters in that order). Verify all "
        "printed letters in any name placard or sign-holder card. Do NOT "
        "produce 'PRYIA', 'PRIA', 'PRIYAH', or any other variant.",
    ),
    (
        "faro", 7, None,
        "MECHANIC EMPHASIS: all narration captions and panel text must use "
        "real, correctly-spelled English words. If referring to the "
        "rental-car toll device, write simply 'transponder' or 'Via Verde "
        "transponder' — never insert garbled or fabricated modifiers like "
        "'retintal'. Double-check every printed word in the comic.",
    ),
    (
        "funchal", 5, None,
        "MECHANIC EMPHASIS: all narration captions must use real, "
        "correctly-spelled English words. To label a fake or unauthorized "
        "wine-cooperative shopping stop, write 'fake \"wine cooperative\"' "
        "or 'phony \"wine cooperative\"' — never insert garbled non-words "
        "like 'wond'. Double-check every printed word in the comic.",
    ),

    # ------------ Panel-number defects (4) ------------
    ("porto", 4, None, PANEL_NUMBER_FIX),
    ("sintra", 1, None, PANEL_NUMBER_FIX),
    ("coimbra", 1, None, PANEL_NUMBER_FIX),
    ("coimbra", 4, None, PANEL_NUMBER_FIX),

    # --------- Style/rendering inconsistencies (5) ---------
    ("sintra", 3, None, BARE_BUBBLES),
    ("funchal", 4, None, FLAT_FILL_FIX),
    ("cascais", 5, None, NATURAL_SKIN + "\n\n" + FLAT_FILL_FIX),
    ("coimbra", 5, None, FLAT_FILL_FIX),
    ("nazare", 2, None, FLAT_FILL_FIX),
]

COUNTRY = "portugal"
OUT_DIR = Path("/tmp/portugal-audit-regen-comics")
AUDIT_LOG = Path("/tmp/portugal-audit-regen.jsonl")
BATCH_SIZE = 4  # parallel — Wavespeed has been comfortable at 4 concurrent


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
            print(f"  {label}: {res['status']}  char={res['character']}  ({res['note']})",
                  flush=True)
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


if __name__ == "__main__":
    main()
