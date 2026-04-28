#!/usr/bin/env python3
"""Regenerate 3 Brazil scam comics with minor visual mismatches flagged
in the 2026-04-28 vision audit:

  sao-paulo-2  Title says "Paulista Avenue 'Clowns' Distraction Pickpocket"
               but comic showed a generic distraction (no clowns). Force
               a clown costume in the depicted distractor.
  buzios-5     Title says "The Búzios Pousada Bait-and-Switch" (cancel-and-
               relist + bait-switch), but comic showed only on-arrival bait-
               switch. Force a cancel-and-relist beat (booking confirmed,
               then cancelled email, then relist at higher price).
  fortaleza-2  Caption says "Never let a stranger handle your card," but
               only the phone is depicted. Add a credit-card swipe at the
               metro turnstile so the warning matches the visual.
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import extract_scams, generate_one, _keychain  # noqa: E402

TARGETS = [
    (
        "sao-paulo", 2,
        "Avenida Paulista at the MASP underpass / Trianon-MASP block in São "
        "Paulo — busy avenue with the iconic red MASP concrete-pylon museum "
        "building visible in the background, weekday office-lunch crowds, "
        "Paulista's wide pedestrian-and-traffic mix. CRITICAL: at least one "
        "of the distractor figures must wear a red clown nose, oversized "
        "clown shoes, or a clown wig — the scam is locally called the "
        "'palhaços' (clowns) distraction-pickpocket ring and the comic must "
        "depict that specifically. Do NOT depict a generic 'something fell' "
        "distraction without any clown element.",
        "MECHANIC EMPHASIS: a costumed clown (red nose, painted face, or "
        "rainbow wig) approaches the older male traveler on Avenida Paulista "
        "with an exaggerated stumbling-fall act ('Cuidado! Caiu!') while a "
        "second partner in plain clothes lifts the wallet from behind. The "
        "clown is the distraction; the partner is the lift. At least one "
        "panel must show the clown costume clearly visible, and another "
        "must show the partner's hand on the wallet from behind.",
    ),
    (
        "buzios", 5,
        "Búzios pousada booking-fraud digital scene — a young Indian-American "
        "woman traveler at her laptop showing a Booking.com Búzios pousada "
        "confirmation for Carnaval, then a 'host cancelled' email forty-five "
        "days before the trip, then the same property re-listed at three "
        "times the price under a slightly different name, then her booking "
        "an established hotel chain with platform protection. Búzios "
        "atmosphere: cobblestone Rua das Pedras / palm-and-sea backdrop in "
        "panel transitions. CRITICAL: the comic depicts a CANCEL-AND-RELIST "
        "fraud, not an on-arrival bait-and-switch. Panel 2 must show a "
        "cancellation email or notification; panel 3 must show the same "
        "property re-listed at a higher price (3-5x).",
        "MECHANIC EMPHASIS: the comic must show the cancel-and-relist fraud "
        "arc — confirmed booking → host cancellation 30-60 days before "
        "Carnaval → same unit relisted at 3-5x the price. Panel 1: traveler "
        "happily booking. Panel 2: cancellation email/notification on "
        "screen. Panel 3: same unit relisted at 'R$1,800/night' or similar "
        "tripled price. Panel 4: traveler booking a Booking.com hotel chain "
        "instead. NO on-arrival check-in scenes.",
    ),
    (
        "fortaleza", 2,
        "Terminal da Parangaba metro station walkway in Fortaleza — modern "
        "Brazilian metro turnstile gate area with green-arrow ticket-readers, "
        "a 'helpful' stranger pretending to assist with the ticket card. "
        "CRITICAL: at least one panel must clearly show the traveler's "
        "credit card or transit card being handled by the stranger at the "
        "turnstile reader — the warning caption is 'Never let a stranger "
        "handle your card,' so the card must be visible in the visual.",
        "MECHANIC EMPHASIS: a 'helpful' stranger at the Terminal da Parangaba "
        "turnstile offers to help the traveler tap her credit card or transit "
        "card on the reader 'because the gate is tricky' — uses the moment "
        "to skim card details with a hidden reader OR swap the card. Panel 1: "
        "stranger offering 'let me help.' Panel 2: traveler handing card "
        "(card visible in shot). Panel 3: traveler walking through gate, "
        "stranger lingering. Panel 4: traveler later realizing card has "
        "been skimmed/swapped (shown as suspicious charges or a 'card "
        "blocked' notification). The CARD must be the visual focus, not "
        "just the phone.",
    ),
]

COUNTRY = "brazil"
BATCH_SIZE = 3
OUT_DIR = Path("/tmp/brazil-minor-regen")
AUDIT_LOG = Path("/tmp/brazil-minor-regen-audit.jsonl")


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
    print(f"[{COUNTRY}-minor-fix] regenerating {len(targets)} comics", flush=True)
    ok = retried = flagged = 0
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=BATCH_SIZE) as ex:
        futs = [ex.submit(generate_one, COUNTRY, s, OUT_DIR, ws_token, r2_token, True) for s in targets]
        for s, f in zip(targets, futs):
            try:
                res = f.result()
            except Exception as e:
                res = {"status": "flagged", "note": f"err: {e}", "character": "?", "prompt": None}
            label = f"{s['city']}/scam-{s['n']}"
            print(f"  {label}: {res['status']}  char={res['character']}  ({res['note']})", flush=True)
            AUDIT_LOG.open("a").write(json.dumps({"city": s["city"], "n": s["n"], "title": s["title"], **res}) + "\n")
            if res["status"] in ("ok", "ok-cached"):
                ok += 1
            elif res["status"] == "ok-retried":
                retried += 1; ok += 1
            else:
                flagged += 1
    print(f"\n[{COUNTRY}-minor-fix] FINAL: ok={ok} retried={retried} flagged={flagged} elapsed={int(time.time()-t0)}s", flush=True)


if __name__ == "__main__":
    main()
