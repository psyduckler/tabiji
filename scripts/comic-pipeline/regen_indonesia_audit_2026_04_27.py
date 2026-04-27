#!/usr/bin/env python3
"""Regenerate 4 Indonesia scam comics flagged by the 2026-04-27 vision audit
for mechanic-mismatched / wrong-landmark scenes. Each comic depicted a
different scam than its title described. Per the locale-fix pattern, we
prepend explicit BACKDROP REQUIREMENT and MECHANIC EMPHASIS overrides into
the scam dict before calling synthesize_prompt.

Targets:
  lombok-3        Mount Rinjani Trek — depicted Ijen blue fire + gas masks
  nusa-penida-2   Kelingking/Broken Beach Park Fee — depicted restaurant bill
  jakarta-3       Grab/Gojek Off-App — depicted airport pickup template
  ubud-4          Ubud Taxi Mafia — depicted airport pickup template
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
        "lombok", 3,
        "Mount Rinjani volcano in Lombok — visible mountain summit silhouette and "
        "Segara Anak crater lake (the iconic blue-green lake inside Rinjani's caldera, "
        "with a small secondary cone Gunung Baru Jari rising from the lake). Daylight "
        "trekking scene with porters carrying overloaded bamboo-frame packs on a "
        "savanna-and-forest trail. CRITICAL: do NOT depict any blue sulfur fire, gas "
        "masks, sulfur miners, or yellow sulfur deposits — those are Ijen, not Rinjani. "
        "No volcanic crater glow.",
        "MECHANIC EMPHASIS: the scam is an UNLICENSED OPERATOR + PORTER OVERLOAD scam "
        "— a budget operator quotes Rp 1.5M for a 2-day Rinjani trek, then on the "
        "trail it becomes clear the porters are carrying 30–40kg loads (legal limit "
        "is 25kg), the guide isn't certified, and there's no proper equipment or "
        "evacuation insurance. At least one panel must show porters with visibly "
        "overstuffed bamboo-frame packs (sleeping bags + tents + food spilling out), "
        "and another panel must show the licensed operator's hut at Senaru / Sembalun "
        "trailhead with an 'OFFICIAL RINJANI TREK GUIDE' badge. No blue fire. No "
        "gas masks.",
    ),
    (
        "nusa-penida", 2,
        "Nusa Penida island viewpoint — visible Kelingking Beach T-rex shaped cliff "
        "(the iconic dinosaur-head limestone promontory jutting into turquoise water, "
        "with a steep stairway descent), or Broken Beach (Pasih Uug) circular natural "
        "rock arch with an inland tide pool. Coastal limestone cliffs + bright "
        "tropical sun. CRITICAL: do NOT depict a restaurant interior, a printed bill, "
        "menu books, or food. This is an outdoor cliff-top scam, not a restaurant.",
        "MECHANIC EMPHASIS: the scam is a 'PARK FEE PADDING' scam at the cliff "
        "viewpoint — a self-appointed 'park officer' or pop-up ticket booth charges "
        "tourists Rp 50,000–100,000 'entrance fee' on top of (or instead of) the "
        "real Rp 5,000 park fee, often with a hand-written cardboard sign. At least "
        "one panel must show a wooden ticket booth or makeshift gate at the Kelingking "
        "viewpoint stairs with a tout demanding cash, and another panel must show a "
        "tourist comparing the inflated demand against the official Rp 5,000 park "
        "sign. No restaurant. No menu. No bill.",
    ),
    (
        "jakarta", 3,
        "Tourist seated at a Jakarta hotel lobby or café table looking at a phone, "
        "with a WhatsApp chat from a driver visible on screen ('Skip Grab app, pay "
        "cash Rp 200,000 — meet at hotel'). Second panel showing the same tourist "
        "outside on a Jakarta street next to an unmarked car (no Grab green sticker, "
        "no Gojek green helmet) handing cash to the driver. CRITICAL: do NOT depict "
        "an airport, an arrivals hall, an 'Airport Arrivals' sign, or the same "
        "speech bubbles as scam-1 ('Grab car, three hundred thousand!' / 'Plates "
        "don't match!' / 'Official pickup zone only!'). This is an off-app booking "
        "scam, NOT an airport pickup scam.",
        "MECHANIC EMPHASIS: the scam is OFF-APP GRAB/GOJEK BOOKING FRAUD — a driver "
        "(or someone posing as a driver) approaches via WhatsApp and offers 'skip "
        "the app, pay cash, cheaper rate' to evade the platform's complaint, refund, "
        "and trip-history protections. At least one panel must show the WhatsApp "
        "chat on a phone screen with a cash-only off-app pitch, another panel must "
        "show the tourist realizing they have no trip record / no recourse, and a "
        "third panel must show booking via the actual Grab app with the in-app trip "
        "log visible. No airport. No arrivals hall. No identical airport-template "
        "speech bubbles.",
    ),
    (
        "ubud", 4,
        "Jalan Raya Ubud or Monkey Forest Road in Ubud town center — narrow shop-"
        "lined street with traditional Balinese architecture (carved stone gates, "
        "frangipani trees, paving stones), a hand-painted 'NO ONLINE TAXI' or "
        "'TAKSI ONLINE DILARANG' sign on a wall or mounted at a co-op stand, with "
        "a cluster of motor-scooter and minivan taxi-co-op drivers standing at a "
        "designated taxi stand. CRITICAL: do NOT depict an airport, arrivals hall, "
        "Airport Arrivals sign, or airport-pickup-template speech bubbles. Ubud "
        "has no airport. This is a town-center taxi-cartel scam.",
        "MECHANIC EMPHASIS: the scam is the UBUD TAXI MAFIA (LOCAL CO-OP CARTEL) — "
        "Grab and Gojek rideshare drivers cannot pick up inside Ubud center because "
        "the local taxi co-op physically blocks them, sometimes with intimidation "
        "or hand-painted 'NO ONLINE TAXI' signs. Tourists end up paying 3–5× the "
        "metered rate to the co-op. At least one panel must show the 'NO ONLINE "
        "TAXI / TAKSI ONLINE DILARANG' painted sign clearly, another panel must "
        "show a co-op driver quoting Rp 250,000 for a short trip while a tourist "
        "looks at their phone with the Grab app showing 'No drivers available', "
        "and another panel must show the workaround (walk 1km outside Ubud center "
        "to summon a Grab, or use the hotel's pre-booked transfer). No airport. "
        "No arrivals hall. No airport-template speech bubbles.",
    ),
]

COUNTRY = "indonesia"
BATCH_SIZE = 4

OUT_DIR = Path("/tmp/indonesia-audit-regen-comics")
AUDIT_LOG = Path("/tmp/indonesia-audit-regen-audit.jsonl")


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
