#!/usr/bin/env python3
"""Regenerate 13 Canada scam comics flagged by the 2026-04-27 vision audit
for template reuse. Two clusters share verbatim 4-panel speech bubbles:

  Vacation rental fraud (7 cities): banff/5, calgary/5, halifax/5, jasper/6,
    ottawa/6, toronto/4, whistler/2 — all share "This doesn't match the
    photos!" / "Host not answering!" / "Stolen photos — classic scam!" /
    "Only book verified listings!"

  Restaurant pricing (6 cities): banff/4, halifax/3, jasper/3, montreal/2,
    quebec-city/1, whistler/3 — all share "Our house specials, madam!" /
    "No prices on the menu!" / "One hundred eighty for lunch?!" / "Always
    check posted prices!"

Each override below specifies city-specific dialogue, mechanic variant, and
backdrop so the regenerated comics produce visually + textually distinct
results, not just backdrop swaps.
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
    # ============ VACATION RENTAL FRAUD ============
    (
        "banff", 5,
        "Banff townsite alpine cabin / mountain-view condo, Cascade Mountain "
        "or Mount Rundle silhouette in background through a window or in panel "
        "exterior. Wood-frame chalet exterior with a 'NO SHORT-TERM RENTAL "
        "PERMIT' notice taped to the door. Daylight, snowy peaks visible.",
        "MECHANIC EMPHASIS: Banff alpine-cabin rental fraud via PHOTO-STOLEN "
        "LISTING + E-TRANSFER DEPOSIT. Speech bubbles MUST be DIFFERENT from "
        "any other Canada rental fraud comic. Use these panels:\n"
        "Panel 1: tourist at laptop with Airbnb-style listing showing a Banff "
        "log cabin, host says 'Save the Airbnb fee — Interac e-Transfer me $2,400 "
        "directly!'\n"
        "Panel 2: tourist arriving at the address, suitcase in hand, looking at "
        "an empty lot or wrong building, saying 'No cabin at 412 Bear Street?!'\n"
        "Panel 3: tourist's phone showing a Google reverse-image-search result, "
        "saying 'These photos are from a Whistler listing!'\n"
        "Panel 4: tourist at the Banff Visitor Centre information desk, with the "
        "ranger saying 'Always book through Airbnb directly — never e-Transfer.'",
    ),
    (
        "calgary", 5,
        "Calgary apartment building exterior with Stampede grandstand / chuckwagon "
        "signage banners in mid-distance, July daylight. Calgary Tower skyline "
        "(short tower with UFO-style top, NOT CN Tower's lattice needle) visible "
        "in one panel. Stampede-week visible cues: cowboy hats, wagon banner.",
        "MECHANIC EMPHASIS: Calgary STAMPEDE-WEEK surge-pricing rental fraud via "
        "FACEBOOK MARKETPLACE listings. Speech bubbles MUST be city-specific:\n"
        "Panel 1: tourist on Facebook Marketplace seeing 'STAMPEDE WEEK SPECIAL: "
        "$450/night, e-Transfer only. No platform fees!' with a cowboy emoji.\n"
        "Panel 2: tourist at a downtown apartment building with the doorman saying "
        "'Sorry, that unit isn't a short-term rental — owner's away on vacation.'\n"
        "Panel 3: tourist's phone showing Calgary's STR registry website with "
        "'Address NOT REGISTERED' in red, saying 'No license = no real listing.'\n"
        "Panel 4: tourist at a verified Stampede-week hotel front desk, clerk "
        "saying 'For Stampede week, book licensed hotels or Airbnb-verified hosts.'",
    ),
    (
        "halifax", 5,
        "Halifax-style colorful waterfront row house exteriors (the famous painted "
        "wood facades on Granville/Argyle), Citadel Hill or Halifax Harbour visible "
        "in one panel, daylight Atlantic-coast setting.",
        "MECHANIC EMPHASIS: Halifax LONG-STAY (>30 day) lease fraud targeting "
        "students, contract workers, and military families on posting. Speech "
        "bubbles MUST be city-specific:\n"
        "Panel 1: tourist on a laptop seeing a Kijiji listing 'Halifax 1BR near "
        "Dalhousie, $1,800/month — e-Transfer first AND last to secure!'\n"
        "Panel 2: tourist at the building manager's office, manager says 'There's "
        "no Suite 4B — and we don't lease through Kijiji.'\n"
        "Panel 3: tourist on phone with Property Management Association NS, saying "
        "'PMANS has no record of this landlord.'\n"
        "Panel 4: tourist at the Halifax housing-resource centre, with a poster "
        "behind reading 'NEVER e-Transfer first-and-last — sign a lease in person.'",
    ),
    (
        "jasper", 6,
        "Jasper townsite EXTERIOR after the 2024 wildfire — partially-rebuilt wood "
        "facades visible, some scaffolding, a 'JASPER REBUILDS' banner on a "
        "construction fence, mountain backdrop with autumn larches. CRITICAL: "
        "do NOT depict the same alpine cabin as banff/scam-5; this is a "
        "townsite-rebuild context, NOT a wilderness chalet.",
        "MECHANIC EMPHASIS: Jasper POST-WILDFIRE RECOVERY rental fraud — preys "
        "on disaster sympathy, fake 'wildfire-displaced housing' or 'rebuild "
        "project rental' listings. Speech bubbles MUST be city-specific:\n"
        "Panel 1: tourist seeing a Facebook 'Jasper Rebuild Support' post: "
        "'Wildfire-recovery rental: $90/night, helps the community!'\n"
        "Panel 2: tourist arriving at an address still inside the evacuation "
        "zone, with a 'NO ENTRY — RECONSTRUCTION ZONE' Parks Canada sign, saying "
        "'This property is still on the evac list!'\n"
        "Panel 3: tourist on phone with a Parks Canada officer in uniform, "
        "officer says 'No reopened rentals at that address yet.'\n"
        "Panel 4: tourist at the Jasper Information Centre with a community "
        "bulletin saying 'For Jasper rentals: book only through Tourism Jasper's "
        "verified-rebuild list at tourismjasper.com.'",
    ),
    (
        "ottawa", 6,
        "Ottawa downtown brick walk-up apartment building (typical Sandy Hill / "
        "Centretown style with stone steps and small balconies), Parliament's "
        "Peace Tower visible distantly in one panel.",
        "MECHANIC EMPHASIS: Ottawa GOVERNMENT-CONTRACTOR housing fraud — targets "
        "federal contractors, parliamentary interns, on-secondment workers. "
        "Speech bubbles MUST be city-specific:\n"
        "Panel 1: tourist on a 'Government Contractor Housing Ottawa' Facebook "
        "group seeing 'Furnished apartment for federal contractors — $2,800/month, "
        "send a CERTIFIED CHEQUE to lock it in!'\n"
        "Panel 2: tourist on the phone with PWGSC (Public Works) housing services, "
        "officer says 'PWGSC has no record of that address as government housing.'\n"
        "Panel 3: tourist looking at a downtown brick apartment with a regular "
        "tenant in the doorway saying 'Nobody by that landlord name lives here.'\n"
        "Panel 4: tourist at the Ottawa Housing Resource Centre, sign reads "
        "'Verify all government-contractor housing through CFHA (canadianforces "
        "housing.gc.ca) or PWGSC directly.'",
    ),
    (
        "toronto", 4,
        "Toronto downtown street with CN Tower visible in the background through "
        "a condo balcony view in one panel. King West / Liberty Village condo "
        "lobby aesthetic. Modern glass-and-steel skyline. CRITICAL: do NOT use "
        "the same generic-suburban-door composition as the other rental-fraud "
        "comics.",
        "MECHANIC EMPHASIS: Toronto STR-PERMIT-HIJACKING fraud — listing claims a "
        "real Toronto STR permit number that's stolen from another property; "
        "tourist arrives to find the building's bylaw forbids short-term rentals. "
        "Speech bubbles MUST be city-specific:\n"
        "Panel 1: tourist on Airbnb seeing a Toronto condo listing with badge "
        "'TORONTO STR PERMIT #STR-12345 ✓', booking it.\n"
        "Panel 2: tourist at the condo lobby, security guard says 'This building's "
        "bylaw forbids short-term rentals — and that permit number isn't ours.'\n"
        "Panel 3: tourist's phone showing the City of Toronto STR licence search "
        "page with the message 'Permit STR-12345 is registered to a different "
        "address.'\n"
        "Panel 4: tourist at City of Toronto's STR Information desk, the "
        "officer says 'Verify every Toronto STR permit at toronto.ca/STR-search "
        "before booking.'",
    ),
    (
        "whistler", 2,
        "Whistler Village pedestrian plaza in winter — visible Whistler-Blackcomb "
        "gondola cars overhead, snowy peaks, après-ski crowd. Wood-and-stone "
        "ski-resort architecture. CRITICAL: do NOT depict an alpine cabin door "
        "(too similar to banff/scam-5 and jasper/scam-6).",
        "MECHANIC EMPHASIS: Whistler SKI-WEEK chalet fraud via WIRE TRANSFER to "
        "OVERSEAS account. Speech bubbles MUST be city-specific:\n"
        "Panel 1: tourist on a 'Whistler Ski Chalets' website seeing 'Ski-week "
        "chalet 8 guests $1,200/night — wire transfer to our European account "
        "for the discount!'\n"
        "Panel 2: tourist at a Whistler Village address with a regular family at "
        "the door saying 'We live here. We've never rented this place out.'\n"
        "Panel 3: tourist looking at a wire-transfer receipt to a Lithuanian bank "
        "with 'Total wired: $7,200 CAD', saying 'They're already gone.'\n"
        "Panel 4: tourist at the Tourism Whistler office, with a sign reading "
        "'Book only through Tourism Whistler's licensed-operator directory at "
        "whistler.com — never wire transfer overseas.'",
    ),
    # ============ RESTAURANT PRICING ============
    (
        "banff", 4,
        "Banff Avenue restaurant interior with floor-to-ceiling mountain views "
        "(Cascade Mountain or Mount Rundle visible through the window), wood-"
        "beam ceiling, antler chandelier, log-cabin upscale-dining feel.",
        "MECHANIC EMPHASIS: Banff Avenue 'specials board' restaurant where the "
        "specials are VERBALLY pitched and never written, then arrive at $52 each. "
        "MUST use city-specific dialogue + bill total — DIFFERENT from any other "
        "Canada restaurant comic:\n"
        "Panel 1: server at the table holding a small chalkboard, saying 'Tonight's "
        "specials: elk tenderloin, market price... and a Cascade Mountain Cabernet, "
        "ask me about the vintage!'\n"
        "Panel 2: tourist looking at the printed menu, only appetizers + soup "
        "listed, saying 'No mains on the printed menu — just specials?'\n"
        "Panel 3: bill close-up: 'Elk tenderloin $68, Cab Sauv $42, total $147', "
        "with tourist's hand recoiling, saying 'A hundred and forty-seven dollars "
        "for one main?!'\n"
        "Panel 4: tourist at a different restaurant on Banff Ave (Caribou Bistro / "
        "Park Distillery sign visible), printed menu in hand showing entrées at "
        "$24-32, saying 'Ask for the printed menu before sitting.'",
    ),
    (
        "halifax", 3,
        "Halifax Harbour-front restaurant patio with the Halifax Harbour, Theodore "
        "Tugboat, or Maritime Museum of the Atlantic visible behind. Wooden boardwalk "
        "patio, fishing boats nearby, lobster-trap décor.",
        "MECHANIC EMPHASIS: Halifax HARBOUR-FRONT lobster-roll tourist trap where "
        "'market price' lobster bill arrives at $89/roll. MUST be DIFFERENT from "
        "any other Canada restaurant comic:\n"
        "Panel 1: server pointing at a chalkboard 'TODAY'S CATCH: Atlantic lobster "
        "roll, market price' on a harbour-front restaurant patio.\n"
        "Panel 2: tourist asking 'What's the market price today?' — server "
        "shrugging 'It depends on the boats coming in!'\n"
        "Panel 3: bill arriving with 'Lobster roll $89, mussels $34, total $185' "
        "— tourist saying '$89 for one lobster roll?!'\n"
        "Panel 4: tourist at a casual harbour-front lobster-pound (Boondock's, "
        "Hall's Harbour, or similar) with a posted price board reading 'Lobster "
        "roll: $24', saying 'Always check posted prices on the chalkboard first.'",
    ),
    (
        "jasper", 3,
        "Jasper Town main-street restaurant (post-wildfire restored facade), "
        "Pyramid Mountain or The Whistlers in the distance. CRITICAL: do NOT use "
        "the same composition as banff/scam-4 — different camera angle, different "
        "interior, no antler chandelier, no specials chalkboard.",
        "MECHANIC EMPHASIS: Jasper Town COMBINED hotel-parking + restaurant pricing "
        "trap — restaurant adds an automatic 'parking validation fee' on top of "
        "inflated entrée prices. MUST be DIFFERENT from any other Canada restaurant "
        "comic:\n"
        "Panel 1: tourist parking, hotel sign reads 'PARK FREE WITH RESTAURANT "
        "VALIDATION ✓' — tourist thinking 'Parking is free if I eat here!'\n"
        "Panel 2: server bringing a thick leather menu with no prices on the "
        "specials section, saying 'The chef recommends the Alberta beef tasting "
        "tonight.'\n"
        "Panel 3: bill arriving showing 'Beef tasting $58, Parking validation "
        "fee $12, total with tip suggestion $94' — tourist saying 'A parking "
        "validation FEE?!'\n"
        "Panel 4: tourist at the Jasper Information Centre with a tip-sheet "
        "reading 'Verify parking-validation policies BEFORE ordering, and ask if "
        "specials are written or only spoken.'",
    ),
    (
        "montreal", 2,
        "Old Montreal cobblestone street restaurant patio — Notre-Dame Basilica "
        "spire visible in one panel, exposed-stone walls, French bistro chairs. "
        "Bilingual French / English signage on chalkboards is appropriate and "
        "expected.",
        "MECHANIC EMPHASIS: Old Montreal Place Jacques-Cartier 'tourist menu' "
        "trap where the French menu has lower prices than the English-translated "
        "one handed to tourists. MUST be DIFFERENT from any other Canada "
        "restaurant comic:\n"
        "Panel 1: server in front of an Old Montreal restaurant, holding two menu "
        "booklets — saying 'English menu, madame?'\n"
        "Panel 2: tourist looking at the English menu showing 'Bavette steak $42'; "
        "next-table local has a French menu showing 'Bavette $26', tourist "
        "thinking 'Same dish, different price!'\n"
        "Panel 3: bill arriving showing 'Bavette $42, vin maison $14, total $74' "
        "— tourist comparing with the French menu, saying 'C'est seize dollars "
        "de plus pour le menu anglais.'\n"
        "Panel 4: tourist at a Plateau-area BYO bistro (Le Pied de Cochon or "
        "L'Express style), saying 'Ask for the menu en français — same food, "
        "real price.'",
    ),
    (
        "quebec-city", 1,
        "Old Quebec Rue Saint-Louis or Place Royale stone-walled bistro interior, "
        "Château Frontenac visible through the window in one panel. 17th-century "
        "stone arches, traditional Quebec décor (snowshoes on wall, tin ceiling). "
        "Wintertime — snow on the cobblestones outside.",
        "MECHANIC EMPHASIS: Old Quebec 'Québécois experience bundle' trap — "
        "restaurant sells a $95/person tourist set-menu (3 courses + maple syrup "
        "tasting) where the same dishes à la carte total $48. MUST be DIFFERENT "
        "from any other Canada restaurant comic:\n"
        "Panel 1: server at a Rue Saint-Louis stone-bistro, presenting a leather "
        "folio: 'Le Forfait Québécois — soupe à l'oignon, tourtière, pouding chômeur, "
        "dégustation de sirop d'érable... only $95 per person!'\n"
        "Panel 2: tourist looking at the regular à la carte menu, doing math, "
        "saying 'Soupe $9, tourtière $22, pouding $11... that's $42 not $95!'\n"
        "Panel 3: bill arriving with '2 × Forfait Québécois = $190 + 18% gratuity "
        "auto-added = $224' — tourist saying 'The bundle is double the real price.'\n"
        "Panel 4: tourist at Buffet de l'Antiquaire (Limoilou) or Chez Ashton (St-"
        "Roch) ordering tourtière à la carte for $22, saying 'Walk five minutes "
        "off the tourist strip for residential pricing.'",
    ),
    (
        "whistler", 3,
        "Whistler Village après-ski pub interior — wood-paneled walls, ski "
        "memorabilia, fireplace, bar with beer taps. Whistler Mountain visible "
        "through a window.",
        "MECHANIC EMPHASIS: Whistler après-ski pub SUBTLE BILL-PADDING — adds "
        "automatic 18% gratuity AND a 'resort fee' AND upcharges house wine to "
        "premium without asking. MUST be DIFFERENT from any other Canada restaurant "
        "comic:\n"
        "Panel 1: tourist at the bar after skiing, server saying 'Two glasses of "
        "the house red?' — tourist nodding 'Yes, two of the house.'\n"
        "Panel 2: bill arriving — close-up showing 'Premium Cabernet $24, Premium "
        "Cabernet $24, Resort fee $8, Auto-gratuity 18% $11.52, TOTAL $67.52' — "
        "tourist saying 'I asked for the HOUSE wine!'\n"
        "Panel 3: server returning, dismissive: 'Our house pour IS the premium — "
        "and the resort fee and auto-grat are non-negotiable.'\n"
        "Panel 4: tourist on phone reading the receipt to a friend, saying "
        "'Always read the bill line-by-line in Whistler — confirm wine pours, "
        "refuse undisclosed resort fees.'",
    ),
]

COUNTRY = "canada"
BATCH_SIZE = 6  # 13 targets — tune to avoid Wavespeed 429s

OUT_DIR = Path("/tmp/canada-audit-regen-comics")
AUDIT_LOG = Path("/tmp/canada-audit-regen-audit.jsonl")


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
