#!/usr/bin/env python3
"""
Re-filter the raw Barcelona keyword set to remove FC Barcelona football noise
and US Barcelona Wine Bar chain pollution. Re-bucket and re-categorize.
"""
import json
import re
import csv
from collections import defaultdict

OUT_DIR = "/Users/bjh/Documents/tabiji/scripts/barcelona-research"
RAW = f"{OUT_DIR}/raw_keywords.json"
CLEAN_JSON = f"{OUT_DIR}/clean_keywords.json"
CLEAN_CSV = f"{OUT_DIR}/clean_keywords.csv"
CLEAN_SUMMARY = f"{OUT_DIR}/clean_summary.json"

# Aggressive noise filters
NOISE_PATTERNS = [
    # Football / soccer
    r"\bfútbol\b", r"\bfutbol\b", r"\bfc barcelona\b", r"\bbarcelona fc\b",
    r"\bbarça\b", r"\bbarca\b", r"\balineaciones\b", r"\bestadísticas\b",
    r"\bestadisticas\b", r"\bposiciones\b", r"\bjugadores\b", r"\bpartidos\b",
    r"\bcronología\b", r"\bcronologia\b", r"\bclub brujas\b", r"\bbrujas\b",
    r"\bsporting club\b", r"\bfootball club\b", r"\bfootball\b",
    r"\bsoccer\b", r"\bla liga\b", r"\breal madrid vs\b", r"\bvs real madrid\b",
    r"\bbarcelona vs\b", r"\bvs barcelona\b", r"\bbarcelona match\b",
    r"\bbarcelona schedule\b", r"\bbarcelona standings\b", r"\bbarcelona fixtures\b",
    r"\bmessi\b", r"\bbarcelona players\b", r"\bbarcelona jersey\b",
    r"\bbarcelona kit\b", r"\bbarcelona shirt\b", r"\bbarcelona b\b",
    r"\bbarcelona u\b", r"\bbarcelona femen\b", r"\bbarcelona news\b",
    r"\bbarcelona club news\b", r"\bbarcelona club\b", r"\bclub website\b",
    r"\bcamp nou\b",  # ambiguous; we already had it as a sights seed but most queries are football
    r"\bbarcelona transfer\b", r"\bbarcelona signing\b", r"\bbarcelona coach\b",
    r"\bbarcelona manager\b", r"\bbarcelona squad\b", r"\bbarcelona lineup\b",
    r"\bbarcelona goal\b", r"\bbarcelona score\b", r"\bbarcelona result\b",
    r"\bbarcelona la liga\b", r"\bbarcelona champions\b",
    r"fútbol_club_barcelona", r"\bnou camp\b", r"\bcamp nou\b",
    r"\bxavi\b", r"\bxavi hernandez\b", r"\bgavi\b", r"\bpedri\b",
    r"\blewandowski\b", r"\bter stegen\b",
    r"\bvissel kobe\b", r"\bfc seoul\b", r"\blevante\b", r"\bathletic club\b",
    r"\bcomo 1907\b", r"\bmallorca\b", r"\brcd\b", r"\br\.c\.d\b",

    # US Barcelona Wine Bar chain locations
    r"\bbarcelona wine bar\b",
    r"\bbrookline\b", r"\bstamford\b", r"\bconnecticut\b", r"\bct\b",
    r"\bwashington dc\b", r"\bbethesda\b", r"\bnoma\b", r"\barlington va\b",
    r"\bgeorgetown\b", r"\bwest hartford\b", r"\bfairfield\b",
    r"\btampa\b", r"\bboston\b", r"\bclarendon\b", r"\bmosaic\b",
    r"\breston\b", r"\batlanta\b", r"\bbuckhead\b", r"\bcleveland park\b",
    r"\bnashville\b", r"\bcharlotte\b", r"\borlando\b",
    r"\bedgewater\b", r"\bbirmingham\b", r"\bnew haven\b",
    r"\bcape coral\b",

    # Disfrutar restaurant noise (one specific result)
    r"\bdis fru tar\b", r"\bdisfrutar barcelona\b",  # actually disfrutar is a real Michelin restaurant, but the "dis fru tar" is broken

    # Other Barcelonas
    r"\bvenezuela\b", r"\banzoategui\b",

    # Generic non-travel
    r"\bbarcelona ny\b", r"\bbarcelona new york\b",
]

NOISE_RE = re.compile("|".join(NOISE_PATTERNS), re.IGNORECASE)

# Re-categorization rules — assign each keyword to one PRIMARY category
# Order matters: first match wins
CATEGORY_RULES = [
    # Lodging
    ("lodging_hotels", [r"\bhotel", r"\bresort", r"\bspa hotel", r"\bb&b\b", r"\bbed and breakfast"]),
    ("lodging_hostels", [r"\bhostel"]),
    ("lodging_apartments", [r"\bairbnb", r"\bapartment", r"\bvacation rental", r"\bshort term", r"\blong term", r"\bmonthly rental", r"\brental"]),
    ("lodging_neighborhoods", [r"\bwhere to stay", r"\bbest area", r"\bneighborhood", r"\bbarrio", r"\bdistrict"]),

    # Food & drink
    ("food_michelin", [r"\bmichelin"]),
    ("food_tapas_paella", [r"\btapas", r"\bpaella"]),
    ("food_specific_meal", [r"\bbreakfast", r"\bbrunch", r"\blunch\b", r"\bdinner"]),
    ("food_dietary", [r"\bvegan", r"\bvegetarian", r"\bgluten"]),
    ("food_market_tour", [r"\bfood market", r"\bfood tour", r"\bboqueria", r"\bla boqueria"]),
    ("food_restaurants", [r"\brestaurant", r"\bbest place to eat", r"\bwhere to eat", r"\bfine dining", r"\bsteakhouse", r"\bseafood", r"\bbarcelona food", r"\bbarcelona eat", r"\bbarcelona dish", r"\bbarcelona cuisine", r"\bfood in barcelona", r"\bfood barcelona", r"\bfood around"]),
    ("food_cafes_coffee", [r"\bcoffee", r"\bcafe", r"\bcafé", r"\bespresso"]),
    ("food_bakery_dessert", [r"\bbakery", r"\bpastry", r"\bdessert", r"\bice cream", r"\bgelato", r"\bchocolate", r"\bchurros"]),

    ("drinks_bars", [r"\bcocktail", r"\bspeakeasy", r"\brooftop bar", r"\bwine bar", r"\bbeach bar", r"\bsports bar", r"\bgay bar", r"\bbest bar", r"\bbar in barcelona", r"\bbars in barcelona", r"\bbarcelona bar", r"\bbar barcelona", r"^bar ", r" bar barcelona", r"bar mut", r"bar canete", r"bar brutal", r"mont bar", r"shoko bar", r"dow jones bar", r"barcelona bistro bar"]),
    ("drinks_nightlife", [r"\bnightlife", r"\bnightclub", r"\bclub", r"\bparty", r"\bdancing", r"\blive music", r"\bdj"]),
    ("drinks_sangria", [r"\bsangria", r"\bvermouth", r"\bcava"]),

    # Transport
    ("transport_airport", [r"\bairport", r"\bbcn\b", r"\bel prat"]),
    ("transport_local", [r"\bmetro\b", r"\btaxi", r"\buber\b", r"\bcabify", r"\bcar rental", r"\brent a car", r"\bbus\b", r"\bgetting around", r"\btransport", r"\bpublic transit"]),
    ("transport_intercity", [r"\bbarcelona to madrid", r"\bmadrid to barcelona", r"\bbarcelona to ", r" to barcelona", r"\bave\b", r"\brenfe", r"\btrain"]),
    ("transport_cruise", [r"\bcruise port", r"\bcruise terminal", r"\bcruise"]),

    # Sights
    ("sights_sagrada", [r"\bsagrada familia", r"\bsagrada de familia"]),
    ("sights_gaudi", [r"\bgaudi", r"\bcasa batll", r"\bcasa mil", r"\bla pedrera", r"\bpark guell", r"\bparc guell", r"\bpark güell"]),
    ("sights_picasso", [r"\bpicasso"]),
    ("sights_gothic", [r"\bgothic quarter", r"\bbarri gotic", r"\bbarri gòtic"]),
    ("sights_beaches", [r"\bbeach", r"\bplaya", r"\bbarceloneta"]),
    ("sights_parks", [r"\bpark\b", r"\bmontjuic", r"\btibidabo"]),
    ("sights_museums", [r"\bmuseum", r"\bmuseo"]),
    ("sights_tours", [r"\btour\b", r"\btours\b", r"\bwalking tour", r"\bbike tour", r"\bday trip", r"\bexcursion"]),
    ("sights_attractions", [r"\bthings to do", r"\bthings do to", r"\battraction", r"\bsights", r"\bsightseeing", r"\bvisit", r"\bsee in barcelona", r"\baquarium", r"\bla rambla", r"\bramblas\b"]),

    # Itinerary
    ("itinerary", [r"\bitinerary", r"\b\d days? in barcelona", r"\bbarcelona \d days?", r"\b\d days barcelona", r"\bweekend in barcelona", r"\bbarcelona weekend", r"\bone day in barcelona", r"\bone week", r"\bbarcelona in \d", r"\b48 hours", r"\b72 hours"]),

    # Practical
    ("practical_weather", [r"\bweather", r"\btemperature", r"\bclimate", r"\brain", r"\bsunshine", r"\bhumidity"]),
    ("practical_when_to_visit", [r"\bbest time to visit", r"\bwhen to visit", r"\bbest month", r"\boff season", r"\bpeak season"]),
    ("practical_money", [r"\bcurrency", r"\beuro\b", r"\batm\b", r"\bcash", r"\btipping", r"\bcost"]),
    ("practical_language", [r"\blanguage", r"\bcatalan", r"\bspanish phrases", r"\bspeak english"]),
    ("practical_connectivity", [r"\bsim card", r"\besim", r"\bwifi", r"\binternet"]),
    ("practical_misc", [r"\bdress code", r"\betiquette", r"\bpower adapter", r"\bplug type", r"\bvoltage"]),

    # Safety
    ("safety", [r"\bsafe", r"\bsafety", r"\bdangerous", r"\bcrime", r"\bpickpocket", r"\bscam", r"\btheft", r"\brobbery", r"\bsketchy", r"\bavoid"]),

    # Visa / entry
    ("visa_entry", [r"\bvisa", r"\bentry requirement", r"\bschengen", r"\bpassport", r"\bcustoms"]),

    # Health / insurance
    ("health_insurance", [r"\binsurance", r"\bvaccin", r"\bhospital", r"\bpharmacy", r"\bdoctor", r"\bclinic", r"\bhealth", r"\bemergency"]),

    # Remote / living
    ("remote_living", [r"\bdigital nomad", r"\bcoworking", r"\bremote work", r"\bliving in", r"\bexpat", r"\bmoving to", r"\bcost of living", r"\brelocation"]),

    # Shopping
    ("shopping", [r"\bshopping", r"\bmarket\b", r"\bmarkets", r"\bsouvenir", r"\bel corte ingl", r"\bboutique", r"\bmall\b", r"\bbarcelona shop", r"\bshop in barcelona"]),

    # Trip planning generic
    ("planning_general", [r"\btravel", r"\btrip", r"\bvacation", r"\bguide", r"\bholiday", r"\btourism", r"\bcity break", r"\bplan"]),
]

def categorize(kw):
    kwl = kw.lower()
    for cat, patterns in CATEGORY_RULES:
        for p in patterns:
            if re.search(p, kwl):
                return cat
    return "other"

def is_noise(kw):
    return bool(NOISE_RE.search(kw))

def main():
    raw = json.load(open(RAW))
    print(f"Loaded {len(raw)} raw keywords")

    clean = []
    for r in raw:
        kw = r["keyword"]
        if is_noise(kw):
            continue
        # Must contain barcelona explicitly
        if "barcelona" not in kw.lower():
            continue
        cat = categorize(kw)
        clean.append({
            "keyword": kw,
            "volume": r["volume"],
            "cpc": r["cpc"],
            "competition": r["competition"],
            "num_results": r["num_results"],
            "category": cat,
        })

    clean.sort(key=lambda r: r["volume"], reverse=True)
    print(f"After filter: {len(clean)} keywords (removed {len(raw) - len(clean)})")

    # Volume buckets
    buckets = {
        "head_10k+": [], "high_5k_10k": [], "mid_1k_5k": [],
        "low_500_1k": [], "longtail_100_500": [], "tail_lt_100": [],
    }
    for r in clean:
        v = r["volume"]
        if v >= 10000: buckets["head_10k+"].append(r)
        elif v >= 5000: buckets["high_5k_10k"].append(r)
        elif v >= 1000: buckets["mid_1k_5k"].append(r)
        elif v >= 500: buckets["low_500_1k"].append(r)
        elif v >= 100: buckets["longtail_100_500"].append(r)
        else: buckets["tail_lt_100"].append(r)

    # Per-category summary with bucket breakdown
    cats = defaultdict(list)
    for r in clean:
        cats[r["category"]].append(r)

    cat_summary = {}
    for cat, items in cats.items():
        items.sort(key=lambda r: r["volume"], reverse=True)
        cat_summary[cat] = {
            "total_keywords": len(items),
            "total_volume": sum(r["volume"] for r in items),
            "avg_cpc": round(sum(r["cpc"] for r in items) / len(items), 2),
            "top_15": items[:15],
            "head_count": sum(1 for r in items if r["volume"] >= 5000),
            "mid_count": sum(1 for r in items if 1000 <= r["volume"] < 5000),
            "long_tail_count": sum(1 for r in items if r["volume"] < 1000),
        }

    summary = {
        "total_keywords": len(clean),
        "total_volume": sum(r["volume"] for r in clean),
        "buckets": {
            k: {
                "count": len(v),
                "total_volume": sum(r["volume"] for r in v),
                "top_10": v[:10],
            } for k, v in buckets.items()
        },
        "categories": dict(sorted(cat_summary.items(), key=lambda x: -x[1]["total_volume"])),
    }

    with open(CLEAN_JSON, "w") as f:
        json.dump(clean, f, indent=2)
    with open(CLEAN_SUMMARY, "w") as f:
        json.dump(summary, f, indent=2)
    with open(CLEAN_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["keyword", "volume", "cpc", "competition", "num_results", "category"])
        writer.writeheader()
        for r in clean:
            writer.writerow(r)

    print(f"\nWrote: {CLEAN_JSON}, {CLEAN_CSV}, {CLEAN_SUMMARY}")
    print("\nVolume buckets:")
    for k, v in buckets.items():
        print(f"  {k:>20}: {len(v):>5} kws, vol {sum(r['volume'] for r in v):>10,}")

    print("\nCategories by total volume:")
    for cat, data in summary["categories"].items():
        print(f"  {cat:>25}: {data['total_keywords']:>5} kws, vol {data['total_volume']:>9,}, avg cpc ${data['avg_cpc']}")

if __name__ == "__main__":
    main()
