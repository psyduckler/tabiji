#!/usr/bin/env python3
"""Regenerate 4 Brazil scam comics flagged by the 2026-04-28 vision audit.

Targets:
  florianopolis-4  WRONG SCAM — depicted pulseira/ribbon scam instead of
                   Praia Mole / Jurerê VIP-beach-bed upcharge. Hard backdrop
                   + mechanic override.
  manaus-1         Typo "MÃO ARRIVALS" (Portuguese for "hand") instead of
                   the airport code "MAO ARRIVALS". Force airport-sign text.
  recife-2         Garbled overlay text "Under sunched Recife" + stray
                   "MARCUS MISSED" label on PERIGO sign. Force clean Boa
                   Viagem shark-warning depiction.
  rio-6            Truncated character caption "Priya, 34-year." instead of
                   "Priya, 34" (or no demographic caption at all). Suppress
                   the character-intro caption.
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
        "florianopolis", 4,
        "Praia Mole or Jurerê Internacional beach club in Florianópolis — "
        "white-sand surf beach with Atlantic-coast horizon, exclusive beach "
        "club deck with white canvas-canopy daybeds (camas balinesas), "
        "polo-shirted attendant with 'VIP BED' price card. CRITICAL: do NOT "
        "depict ribbon-tying, pulseiras, bracelets, cobblestone streets, "
        "Pelourinho-style colonial baroque, or any wrist-tying gesture. "
        "This is a beach-club setting, not a colonial street.",
        "MECHANIC EMPHASIS: an attendant at a Praia Mole or Jurerê beach "
        "club approaches with 'VIP bed for you, senhora? Best ocean view!' "
        "and quotes R$800 for a daybed/cabana that costs R$80 at the "
        "regular quiosque chairs nearby. The traveler points at the "
        "regular R$80 chairs visible behind, refuses, and walks to a "
        "regular quiosque. At least one panel must show the daybed price "
        "card reading 'CAMA BALINESA R$800' and another panel must show "
        "the regular quiosque chair sign 'CADEIRA R$30'. NO ribbon, NO "
        "pulseira, NO wrist-tying anywhere.",
    ),
    (
        "manaus", 1,
        "Eduardo Gomes International Airport (MAO) arrivals hall in Manaus "
        "— modern Brazilian airport interior, baggage carousel area, "
        "tropical-Amazon murals visible. CRITICAL: the airport-arrivals "
        "header sign must read exactly 'MAO ARRIVALS' (the IATA code for "
        "Manaus is M-A-O). Do NOT write 'MÃO' (with tilde) or 'MAOS' or "
        "any Portuguese word — only the three-letter airport code MAO. "
        "Also acceptable: 'MAO — MANAUS' or 'EDUARDO GOMES MAO'.",
        "MECHANIC EMPHASIS: at MAO airport arrivals, a 'TAXI ESPECIAL' "
        "kiosk attendant quotes R$180 fixed-price to Ponta Negra; the "
        "traveler checks the Uber app showing R$65 and walks to the "
        "official APLICATIVOS rideshare pickup zone. The airport header "
        "sign in panel 1 must read 'MAO ARRIVALS' not 'MÃO ARRIVALS'.",
    ),
    (
        "recife", 2,
        "Praia de Boa Viagem in Recife — long urban beach with high-rise "
        "apartment blocks lining Avenida Boa Viagem in the background, "
        "yellow PERIGO TUBARÕES (shark-attack warning) sign with shark "
        "silhouette. CRITICAL: the warning sign must read 'PERIGO — "
        "ATAQUE DE TUBARÕES' (or 'TUBARÕES PERIGO'). Do NOT include any "
        "stray text labels like 'MARCUS', 'MARCUS MISSED', or any "
        "character name on the sign. Do NOT include any 'Under sunched' "
        "or other garbled text overlays. All visible text must be either "
        "Portuguese ('PERIGO', 'TUBARÕES', 'BOA VIAGEM') or clean English "
        "speech-bubble dialogue.",
        "MECHANIC EMPHASIS: a beach kiosk vendor on Boa Viagem tells the "
        "traveler 'It's safe to swim here, amigo!' while the official "
        "yellow PERIGO TUBARÕES (shark-attack warning) sign is visible "
        "behind them. The lifeguard waves the traveler back from the "
        "water. The official warning beats the vendor's pitch. NO stray "
        "character-name text on the warning sign — just the Portuguese "
        "shark-warning text.",
    ),
    (
        "rio-de-janeiro", 6,
        "Booking-fraud digital scene — a young Brazilian-Indian-American "
        "woman traveler at a laptop showing an Airbnb / Booking.com "
        "Carnaval listing (Rio Copacabana skyline visible through a "
        "window). Then her phone showing a 'Booking cancelled by host' "
        "message. Then a re-listed property at 5x the original price. "
        "Then her booking direct with a hotel chain. CRITICAL: do NOT "
        "include any character-introduction caption like 'Priya, 34F' "
        "or 'Priya, 34-year-old' or 'Priya, 34-year' anywhere in the "
        "comic. The character is unlabeled — only speech-bubble dialogue "
        "appears as text on the page. NO age/demographic captions of "
        "any kind.",
        None,
    ),
]

COUNTRY = "brazil"
BATCH_SIZE = 4

OUT_DIR = Path("/tmp/brazil-book-readiness-regen")
AUDIT_LOG = Path("/tmp/brazil-book-readiness-regen-audit.jsonl")


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
    print(f"[{COUNTRY}-book-readiness] regenerating {len(targets)} comics", flush=True)

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
    print(f"\n[{COUNTRY}-book-readiness] FINAL: {json.dumps(summary)}", flush=True)
    return summary


if __name__ == "__main__":
    main()
