#!/usr/bin/env python3
"""
Re-filter Kyoto raw keywords. Strip US "Kyoto Sushi/Steak" chain noise,
Hawaii Byodo-In replica, Kyoto Protocol, Kyoto Animation, etc.
"""
import json
import re
import csv
from collections import defaultdict

OUT_DIR = "/Users/bjh/Documents/tabiji/scripts/kyoto-research"
RAW = f"{OUT_DIR}/raw_keywords.json"
CLEAN_JSON = f"{OUT_DIR}/clean_keywords.json"
CLEAN_CSV = f"{OUT_DIR}/clean_keywords.csv"
CLEAN_SUMMARY = f"{OUT_DIR}/clean_summary.json"

NOISE_PATTERNS = [
    # === Kyoto restaurant chain pollution (US locations) ===
    # State + city name patterns
    r"\bks\b", r"\bnj\b", r"\bwi\b", r"\bnv\b", r"\bca\b", r"\btx\b",
    r"\bnc\b", r"\bsc\b", r"\bfl\b", r"\bga\b", r"\bal\b", r"\bok\b",
    r"\bpa\b", r"\bma\b", r"\bmd\b", r"\bva\b", r"\bmn\b", r"\bil\b",
    r"\bin\b", r"\boh\b", r"\bky\b", r"\btn\b", r"\bar\b",
    r"\boverland park\b", r"\bcedar grove\b", r"\broseville\b", r"\beagan\b",
    r"\bunion nj\b", r"\bcrystal lake\b", r"\bsalt lake city\b",
    r"\bgreenfield\b", r"\bnorthbrook\b", r"\bcolumbia\b",
    r"\bhowell\b", r"\bcortez\b", r"\bnew bern\b", r"\bcleveland\b",
    r"\bbradenton\b", r"\bsuwanee\b", r"\bdes peres\b", r"\bdes plaines\b",
    r"\bnorth aurora\b", r"\bnorth wales\b", r"\bnorthridge\b",
    r"\bnorth charleston\b", r"\bsouth bend\b", r"\bnorth canton\b",
    r"\borland park\b", r"\bmount pleasant\b", r"\bmount kisco\b",
    r"\bmillbrae\b", r"\bedgewater\b", r"\bmaple grove\b", r"\bjamestown\b",
    r"\bsavannah\b", r"\bbrainerd\b",
    # Restaurant chain identifiers
    r"\bsushi & steak\b", r"\bsushi and steak\b", r"\bsushi & grill\b",
    r"\bsushi and grill\b", r"\bsushi and ramen\b", r"\bjapanese restaurant menu\b",
    r"\bnear me\b", r"\bsteakhouse\b", r"\bhibachi\b", r"\bbenihana\b",
    r"\bcoupon\b", r"\bbuffet\b", r"\bdelivery\b", r"\bdoordash\b",
    r"\bgrubhub\b", r"\bubereats\b", r"\byelp\b",
    # Generic "Kyoto restaurant" without "in/of Kyoto/Japan" context — too noisy to keep
    # We'll handle this by requiring japan/japanese context

    # === Byodo-In Hawaii replica ===
    r"\bhawaii byodo\b", r"\bbyodo.in.*hawaii\b", r"\bbyodo.in.*oahu\b",
    r"\bbyodo.in.*kahekili\b", r"\bbyodo.in.*kaneohe\b",
    r"\bbyodo.in temple oahu\b",

    # === Kyoto Protocol (climate change) ===
    r"\bkyoto protocol\b", r"\bkyoto agreement\b", r"\bclimate change kyoto\b",
    r"\bgreenhouse gas\b", r"\bunfccc\b", r"\bcarbon kyoto\b",

    # === Kyoto Animation (anime studio) ===
    r"\bkyoto animation\b", r"\bkyoani\b", r"\bkyoto arson\b",

    # === Kyoto University ===
    r"\bkyoto university\b", r"\bkyodai\b", r"\bnobel kyoto\b",

    # === Music / pop culture ===
    r"\bphoebe bridgers kyoto\b", r"\bkyoto song\b", r"\bkyoto lyric\b",
    r"\bskrillex kyoto\b", r"\bkyoto chords\b",

    # === Other namesakes ===
    r"\bkyoto japanese gardens .*ks\b",
    r"\bkyoto pa\b", r"\bkyoto fl\b",
    r"\bkyoto in pa\b", r"\bkyoto pennsylvania\b",
    r"\bnorth dakota\b",

    # === Pokemon / video games ===
    r"\bpokemon\b",

    # === Generic spam / non-travel ===
    r"\bcrypto\b", r"\bnft\b", r"\bdownload\b", r"\bfont\b",
]

NOISE_RE = re.compile("|".join(NOISE_PATTERNS), re.IGNORECASE)

# Special filter: bare "kyoto sushi" head term is the chain
SPECIFIC_BLACKLIST = {
    "kyoto sushi", "kyoto sushi ii", "kyoto sushi iii", "kyoto sushi menu",
    "kyoto restaurant", "kyoto restaurants",  # the head term — noisy chain
}

# Categorization rules — first match wins
CATEGORY_RULES = [
    # === Lodging ===
    ("lodging_ryokan", [r"\bryokan", r"\bmachiya", r"\bonsen ryokan"]),
    ("lodging_hostels", [r"\bhostel", r"\bcapsule hotel"]),
    ("lodging_apartments", [r"\bairbnb", r"\bapartment", r"\bvacation rental", r"\bshort term", r"\bmonthly rental", r"\brental"]),
    ("lodging_neighborhoods", [r"\bwhere to stay", r"\bbest area", r"\bneighborhood", r"\bdistrict"]),
    ("lodging_hotels", [r"\bhotel", r"\bresort", r"\bb&b"]),

    # === Food ===
    ("food_michelin", [r"\bmichelin"]),
    ("food_kaiseki", [r"\bkaiseki", r"\bshojin ryori", r"\btemple cuisine", r"\bshojin"]),
    ("food_ramen", [r"\bramen"]),
    ("food_sushi", [r"\bsushi"]),
    ("food_tempura_yakitori", [r"\btempura", r"\byakitori", r"\bokonomiyaki", r"\btonkatsu", r"\bsukiyaki", r"\bshabu", r"\bteppanyaki"]),
    ("food_udon_soba", [r"\budon", r"\bsoba\b"]),
    ("food_izakaya", [r"\bizakaya"]),
    ("food_obanzai_local", [r"\bobanzai", r"\bkyo-ryori", r"\bkyoryori"]),
    ("food_matcha_tea", [r"\bmatcha", r"\bgreen tea", r"\bgyokuro", r"\btea ceremony", r"\bsencha"]),
    ("food_wagashi_sweets", [r"\bwagashi", r"\bmochi", r"\bdango", r"\bdorayaki", r"\bsweet", r"\bdessert", r"\bice cream", r"\bparfait"]),
    ("food_cafes_coffee", [r"\bcoffee", r"\bcafe", r"\bcafé", r"\b% arabica", r"\barabica\b"]),
    ("food_market_tour", [r"\bnishiki market", r"\bnishiki", r"\bfood market", r"\bfood tour", r"\bfood walk"]),
    ("food_street_food", [r"\bstreet food", r"\bstreet eats"]),
    ("food_dietary", [r"\bvegan", r"\bvegetarian", r"\bgluten free", r"\bgluten-free", r"\bhalal", r"\bkosher"]),
    ("food_specific_meal", [r"\bbreakfast", r"\bbrunch", r"\blunch\b", r"\bdinner"]),
    ("food_restaurants", [r"\brestaurant", r"\bbest place to eat", r"\bwhere to eat", r"\bfine dining", r"\bcuisine", r"\bfood in kyoto", r"\bkyoto food", r"\bbest food"]),

    # === Drinks ===
    ("drinks_sake", [r"\bsake\b", r"\bsake brewery", r"\bsake tasting", r"\bsake bar"]),
    ("drinks_whisky", [r"\bwhisky", r"\bwhiskey"]),
    ("drinks_bars", [r"\bcocktail", r"\bspeakeasy", r"\brooftop bar", r"\bbest bar", r"\bbar in kyoto", r"\bkyoto bar", r"\bbar kyoto", r"\bgion bar", r"\bpontocho"]),
    ("drinks_nightlife", [r"\bnightlife", r"\bnightclub", r"\bclub\b", r"\blive music"]),

    # === Transport ===
    ("transport_jr_pass", [r"\bjr pass", r"\bjapan rail pass", r"\bicoca", r"\bsuica", r"\bpasmo"]),
    ("transport_shinkansen", [r"\bshinkansen", r"\bbullet train"]),
    ("transport_intercity", [r"\bkyoto to (osaka|tokyo|nara|hiroshima|nagoya|hakone|takayama|kanazawa|himeji|kobe)", r"(osaka|tokyo|nara|hiroshima|nagoya|hakone|takayama|kanazawa|himeji|kobe) to kyoto", r"\btrain to kyoto", r"\btrain from kyoto"]),
    ("transport_airport", [r"\bairport", r"\bkix\b", r"\bitami", r"\bkansai international"]),
    ("transport_local", [r"\bsubway", r"\bkyoto bus", r"\btaxi", r"\buber", r"\bgetting around", r"\btransport", r"\bkyoto station", r"\bcity bus"]),

    # === Sights — Temples (each major temple is a sub-niche) ===
    ("sights_fushimi_inari", [r"\bfushimi inari", r"\bfushimi-inari"]),
    ("sights_kinkakuji", [r"\bkinkaku", r"\bgolden pavilion", r"\bgolden temple kyoto"]),
    ("sights_kiyomizu", [r"\bkiyomizu"]),
    ("sights_ginkakuji", [r"\bginkaku", r"\bsilver pavilion"]),
    ("sights_ryoanji", [r"\bryoan", r"\bryoanji"]),
    ("sights_tofukuji", [r"\btofuku"]),
    ("sights_tenryuji", [r"\btenryu"]),
    ("sights_byodoin_real", [r"\bbyodo.in.*uji", r"\buji.*byodo", r"\bbyodo.in temple kyoto"]),
    ("sights_other_temples", [r"\btemple", r"\bshrine", r"\bjingu", r"\btaisha", r"\b-ji\b", r"\b-in\b", r"\b-do\b", r"\bdaitoku", r"\bnanzen", r"\bsanjusangen", r"\beikan", r"\bhonen", r"\bshoren", r"\bchion", r"\btoji\b", r"\bto-ji"]),

    # === Sights — Areas / Landmarks ===
    ("sights_arashiyama", [r"\barashiyama", r"\bbamboo grove", r"\bbamboo forest", r"\btogetsukyo", r"\bmonkey park"]),
    ("sights_gion_geisha", [r"\bgion\b", r"\bgeisha", r"\bmaiko", r"\bhanamachi"]),
    ("sights_castle_palace", [r"\bnijo", r"\bimperial palace", r"\bkatsura villa", r"\bshugakuin", r"\bgosho"]),
    ("sights_higashiyama", [r"\bhigashiyama", r"\bphilosophers? path", r"\bphilosopher.s walk", r"\bsannenzaka", r"\bninenzaka"]),
    ("sights_gardens", [r"\bzen garden", r"\bjapanese garden", r"\brock garden", r"\bmoss garden"]),
    ("sights_attractions", [r"\bthings to do", r"\battraction", r"\bsights", r"\bsightseeing", r"\bsee in kyoto"]),
    ("sights_tours", [r"\btour\b", r"\bwalking tour", r"\bbike tour", r"\bday trip", r"\bguided tour"]),
    ("sights_museums", [r"\bmuseum"]),
    ("sights_parks_nature", [r"\bpark\b", r"\bgarden\b"]),

    # === Itinerary ===
    ("itinerary", [r"\bitinerary", r"\b\d days? in kyoto", r"\bkyoto \d days?", r"\bweekend in kyoto", r"\bkyoto weekend", r"\bone day in kyoto", r"\bone week", r"\b48 hours", r"\b72 hours"]),

    # === Cultural experiences ===
    ("cultural_experiences", [r"\bkimono rental", r"\bkimono experience", r"\btea ceremony", r"\bcalligraphy", r"\bzen meditation", r"\bsamurai experience", r"\btraditional experience", r"\bkyudo", r"\bbamboo craft"]),

    # === Practical ===
    ("practical_weather", [r"\bweather", r"\btemperature", r"\bclimate", r"\brain"]),
    ("practical_when_to_visit", [r"\bbest time", r"\bwhen to visit", r"\bbest month"]),
    ("practical_seasonal", [r"\bcherry blossom", r"\bsakura", r"\bkoyo", r"\bautumn leaves", r"\bfall colors", r"\bfall foliage", r"\bautumn foliage", r"\bspring kyoto", r"\bautumn kyoto"]),
    ("practical_money", [r"\bcurrency", r"\byen\b", r"\batm", r"\bcash", r"\btipping", r"\bcost"]),
    ("practical_language", [r"\blanguage", r"\bjapanese phrases"]),
    ("practical_connectivity", [r"\bsim card", r"\besim", r"\bwifi", r"\bpocket wifi", r"\binternet"]),
    ("practical_misc", [r"\bdress code", r"\betiquette", r"\bpower adapter", r"\bplug type"]),

    # === Safety ===
    ("safety", [r"\bsafe", r"\bsafety", r"\bdangerous", r"\bcrime", r"\bscam"]),

    # === Visa / Health / Living ===
    ("visa_entry", [r"\bvisa", r"\bentry requirement", r"\bpassport"]),
    ("health_insurance", [r"\binsurance", r"\bvaccin", r"\bhospital", r"\bpharmacy", r"\bclinic", r"\bhealth"]),
    ("remote_living", [r"\bdigital nomad", r"\bcoworking", r"\bremote work", r"\bliving in", r"\bexpat", r"\bmoving to", r"\bcost of living", r"\bteach english"]),

    # === Shopping ===
    ("shopping", [r"\bshopping", r"\bsouvenir", r"\bantique", r"\bflea market", r"\bteramachi", r"\bnishiki market"]),

    # === General ===
    ("planning_general", [r"\btravel", r"\btrip", r"\bvacation", r"\bguide", r"\bholiday", r"\btourism", r"\bcity break"]),
]

def categorize(kw):
    kwl = kw.lower()
    for cat, patterns in CATEGORY_RULES:
        for p in patterns:
            if re.search(p, kwl):
                return cat
    return "other"

def is_noise(kw):
    if kw.lower().strip() in SPECIFIC_BLACKLIST:
        return True
    return bool(NOISE_RE.search(kw))

def main():
    raw = json.load(open(RAW))
    print(f"Loaded {len(raw)} raw keywords")

    clean = []
    for r in raw:
        kw = r["keyword"]
        if is_noise(kw):
            continue
        # Must contain kyoto or a known kyoto landmark
        kwl = kw.lower()
        keep = "kyoto" in kwl or any(t in kwl for t in [
            "fushimi inari", "kinkaku", "kiyomizu", "arashiyama", "ginkaku",
            "ryoanji", "ryoan-ji", "tofuku-ji", "tenryu-ji", "nanzen-ji",
            "philosopher", "nijo castle", "nijo-jo", "gion ", "byodo in temple uji",
            "byodo-in temple uji",
        ])
        if not keep:
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
        }

    summary = {
        "total_keywords": len(clean),
        "total_volume": sum(r["volume"] for r in clean),
        "buckets": {
            k: {"count": len(v), "total_volume": sum(r["volume"] for r in v), "top_10": v[:10]}
            for k, v in buckets.items()
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

    print(f"\nWrote: {CLEAN_JSON}")
    print("\nVolume buckets:")
    for k, v in buckets.items():
        print(f"  {k:>20}: {len(v):>5} kws, vol {sum(r['volume'] for r in v):>10,}")

    print("\nCategories by total volume:")
    for cat, data in summary["categories"].items():
        print(f"  {cat:>25}: {data['total_keywords']:>5} kws, vol {data['total_volume']:>9,}, cpc ${data['avg_cpc']}")

if __name__ == "__main__":
    main()
