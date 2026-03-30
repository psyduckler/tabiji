#!/usr/bin/env python3
"""
Build safety profiles for 20 priority countries.

Assembles data from existing sources — does NOT generate or scrape new data:
  - app/data/emergency-numbers.json  (192 countries)
  - app/data/advisories-us.json      (208 US State Dept advisories)
  - app/data/advisories-uk.json      (226 UK FCDO advisories)
  - health/{slug}/index.html         (BeautifulSoup extraction)
  - scams/{city}/index.html          (BeautifulSoup extraction)

JP and TH profiles already exist at app/data/safety/ and are NOT modified.

Output: app/data/safety/{iso2_lower}.json for each of the 20 countries.

Usage: python3 app/scripts/build-safety-profiles.py
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing dependency: beautifulsoup4\nInstall: pip install beautifulsoup4", file=sys.stderr)
    raise SystemExit(1)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "app" / "data"
SAFETY_DIR = DATA_DIR / "safety"
HEALTH_DIR = BASE_DIR / "health"
SCAMS_DIR = BASE_DIR / "scams"

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ── Country configuration ────────────────────────────────────────────────────

PRIORITY_COUNTRIES = {
    "JP": {"name": "Japan",          "health_slug": "japan",          "scam_cities": ["tokyo", "osaka"]},
    "TH": {"name": "Thailand",       "health_slug": "thailand",       "scam_cities": ["bangkok", "phuket"]},
    "MX": {"name": "Mexico",         "health_slug": "mexico",         "scam_cities": ["mexico-city", "cancun"]},
    "IT": {"name": "Italy",          "health_slug": "italy",          "scam_cities": ["rome", "florence"]},
    "FR": {"name": "France",         "health_slug": "france",         "scam_cities": ["paris", "nice"]},
    "ES": {"name": "Spain",          "health_slug": "spain",          "scam_cities": ["barcelona", "madrid"]},
    "PT": {"name": "Portugal",       "health_slug": "portugal",       "scam_cities": ["lisbon"]},
    "GR": {"name": "Greece",         "health_slug": "greece",         "scam_cities": ["athens", "santorini"]},
    "GB": {"name": "United Kingdom", "health_slug": "united-kingdom", "scam_cities": ["london", "edinburgh"]},
    "DE": {"name": "Germany",        "health_slug": "germany",        "scam_cities": ["berlin"]},
    "CR": {"name": "Costa Rica",     "health_slug": "costa-rica",     "scam_cities": []},
    "CO": {"name": "Colombia",       "health_slug": "colombia",       "scam_cities": ["medellin"]},
    "PE": {"name": "Peru",           "health_slug": "peru",           "scam_cities": ["lima"]},
    "VN": {"name": "Vietnam",        "health_slug": "vietnam",        "scam_cities": ["hanoi", "ho-chi-minh-city"]},
    "ID": {"name": "Indonesia",      "health_slug": "indonesia-bali", "scam_cities": []},
    "MA": {"name": "Morocco",        "health_slug": "morocco",        "scam_cities": ["marrakech"]},
    "TR": {"name": "Turkey",         "health_slug": "turkey",         "scam_cities": ["istanbul"]},
    "KR": {"name": "South Korea",    "health_slug": "south-korea",    "scam_cities": ["seoul"]},
    "AU": {"name": "Australia",      "health_slug": "australia",      "scam_cities": []},
    "NZ": {"name": "New Zealand",    "health_slug": "new-zealand",    "scam_cities": []},
}

# Quality rating: numeric → text
QUALITY_MAP = {"1": "poor", "2": "fair", "3": "moderate", "4": "good", "5": "excellent"}

# ── Data loaders ─────────────────────────────────────────────────────────────

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_emergency_numbers():
    data = load_json(DATA_DIR / "emergency-numbers.json")
    return data.get("countries", {})


def load_us_advisories():
    data = load_json(DATA_DIR / "advisories-us.json")
    return data.get("advisories", {})


def load_uk_advisories():
    data = load_json(DATA_DIR / "advisories-uk.json")
    raw = data.get("advisories", {})
    # Build two indexes: by iso2 and by slug
    by_iso2 = {}
    by_slug = {}
    for _key, entry in raw.items():
        iso2 = entry.get("iso2")
        slug = entry.get("slug")
        if iso2:
            by_iso2[iso2] = entry
        if slug:
            by_slug[slug] = entry
    return by_iso2, by_slug


def parse_date(date_str):
    """Parse 'Fri, 20 Mar 2026' or 'YYYY-MM-DD' → 'YYYY-MM-DD'. Returns original on failure."""
    if not date_str:
        return None
    if re.match(r"\d{4}-\d{2}-\d{2}", date_str):
        return date_str[:10]
    try:
        dt = datetime.strptime(date_str.strip(), "%a, %d %b %Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        pass
    return date_str

# ── HTML parsers ─────────────────────────────────────────────────────────────

def parse_health_page(iso2):
    """Extract healthcare data from health/{slug}/index.html."""
    cfg = PRIORITY_COUNTRIES[iso2]
    slug = cfg["health_slug"]
    path = HEALTH_DIR / slug / "index.html"
    if not path.exists():
        return None

    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")

    # Quick facts
    qf = {}
    for item in soup.select("#quick-facts .qf-item"):
        label_el = item.select_one(".qf-label")
        value_el = item.select_one(".qf-value")
        if label_el and value_el:
            label = label_el.get_text(strip=True)
            value = value_el.get_text(strip=True)
            qf[label] = value

    system_type = qf.get("Healthcare System", "").strip() or None
    quality_raw = qf.get("Care Quality", "").strip()
    quality_rating = QUALITY_MAP.get(quality_raw, quality_raw.lower() if quality_raw else None)
    tap_water_raw = qf.get("Tap Water", "").strip().lower()
    tap_water = tap_water_raw in ("safe", "safe to drink", "yes", "true")
    pharmacy_access_raw = qf.get("Pharmacy Access", "").strip().lower()

    # Overview section
    overview_text = ""
    overview = soup.find("section", id="overview")
    if overview:
        paras = [p.get_text(" ", strip=True) for p in overview.find_all("p")]
        overview_text = " ".join(paras).strip()

    # Vaccinations section
    vaccinations = []
    vax_section = soup.find("section", id="vaccinations")
    if vax_section:
        for li in vax_section.find_all("li"):
            text = li.get_text(strip=True)
            # Strip emoji prefix like "🟡 "
            text = re.sub(r"^[\U0001F000-\U0001FFFF\u2600-\u26FF\u2700-\u27BF\s]+", "", text).strip()
            if text:
                vaccinations.append(text)

    # Insurance section
    insurance_text = ""
    insurance = soup.find("section", id="insurance")
    if insurance:
        paras = [p.get_text(" ", strip=True) for p in insurance.find_all("p")]
        tips = insurance.select(".callout p")
        tip_texts = [t.get_text(" ", strip=True) for t in tips]
        insurance_text = " ".join(paras + tip_texts).strip()

    # Pharmacy section
    pharmacy_notes = ""
    pharmacy = soup.find("section", id="pharmacy")
    if pharmacy:
        paras = [p.get_text(" ", strip=True) for p in pharmacy.find_all("p")]
        pharmacy_notes = " ".join(paras).strip()

    # Malaria risk — look for the word in overview or vaccinations section
    page_text = soup.get_text(" ", strip=True).lower()
    malaria_risk = "malaria" in page_text and "no malaria" not in page_text and "malaria risk: none" not in page_text

    return {
        "systemType": system_type,
        "qualityRating": quality_rating,
        "walkInAccess": None,
        "costForTourists": overview_text or None,
        "pharmacyAccess": pharmacy_access_raw or None,
        "hospitalNotes": pharmacy_notes or None,
        "vaccinationsRecommended": vaccinations,
        "malariaRisk": malaria_risk,
        "insuranceAdvice": insurance_text or None,
        "tapWater": tap_water,
    }


def parse_scam_page(city_slug):
    """Extract scam entries from scams/{city}/index.html."""
    path = SCAMS_DIR / city_slug / "index.html"
    if not path.exists():
        return []

    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    scams = []

    for card in soup.select(".scam-card"):
        name_el = card.select_one(".scam-title")
        location_el = card.select_one(".scam-location")
        story_el = card.select_one(".scam-story")
        avoid_block = card.select_one(".detail-block.avoid")

        name = name_el.get_text(strip=True) if name_el else None
        if not name:
            continue

        location = ""
        if location_el:
            raw_loc = location_el.get_text(strip=True)
            # Strip leading emoji + "📍 "
            location = re.sub(r"^[^\w]*", "", raw_loc).strip()
            # Take first location before comma
            location = location.split(",")[0].strip()

        description = story_el.get_text(" ", strip=True) if story_el else ""

        avoidance_parts = []
        if avoid_block:
            for li in avoid_block.find_all("li"):
                avoidance_parts.append(li.get_text(" ", strip=True))
        avoidance = " | ".join(avoidance_parts) if avoidance_parts else ""

        scams.append({
            "name": name,
            "city": location or city_slug.replace("-", " ").title(),
            "description": description,
            "avoidance": avoidance,
        })

    return scams

# ── Profile builder ───────────────────────────────────────────────────────────

LEVEL_TEXT_MAP = {
    1: "Exercise Normal Precautions",
    2: "Exercise Increased Caution",
    3: "Reconsider Travel",
    4: "Do Not Travel",
}

US_ADV_URL_TEMPLATE = "https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories/{slug}-travel-advisory.html"


def country_slug_for_us(name):
    """Convert country name to URL slug used by State Dept."""
    return name.lower().replace(" ", "-").replace("'", "")


def build_profile(iso2, emergency_data, us_advisories, uk_by_iso2, uk_by_slug):
    cfg = PRIORITY_COUNTRIES[iso2]
    name = cfg["name"]

    # Emergency numbers
    emrg_raw = emergency_data.get(iso2, {})
    emergency = {
        "police": emrg_raw.get("police"),
        "ambulance": emrg_raw.get("ambulance"),
        "fire": emrg_raw.get("fire"),
        "universal": emrg_raw.get("universal"),
        "notes": None,
    }

    # US advisory
    us_adv = us_advisories.get(iso2)
    if us_adv:
        travel_advisory = {
            "source": "US State Department",
            "level": us_adv.get("level"),
            "levelText": us_adv.get("levelText"),
            "summary": us_adv.get("summary", "")[:500] if us_adv.get("summary") else None,
            "lastUpdated": parse_date(us_adv.get("publishedDate")),
            "url": us_adv.get("url"),
        }
    else:
        travel_advisory = {
            "source": "US State Department",
            "level": None,
            "levelText": None,
            "summary": None,
            "lastUpdated": None,
            "url": None,
        }

    # UK advisory
    uk_adv = uk_by_iso2.get(iso2) or uk_by_slug.get(cfg["health_slug"])
    if uk_adv:
        travel_advisory_uk = {
            "source": "UK FCDO",
            "summary": uk_adv.get("summary") or None,
            "lastUpdated": uk_adv.get("lastUpdated"),
            "url": uk_adv.get("url"),
        }
    else:
        travel_advisory_uk = {
            "source": "UK FCDO",
            "summary": None,
            "lastUpdated": None,
            "url": None,
        }

    # Healthcare from health page
    health_data = parse_health_page(iso2)
    if health_data:
        tap_water = health_data.pop("tapWater", None)
        healthcare = health_data
    else:
        tap_water = None
        healthcare = {
            "systemType": None,
            "qualityRating": None,
            "walkInAccess": None,
            "costForTourists": None,
            "pharmacyAccess": None,
            "hospitalNotes": None,
            "vaccinationsRecommended": [],
            "malariaRisk": None,
            "insuranceAdvice": None,
        }

    # Scams
    scams = []
    for city_slug in cfg["scam_cities"]:
        city_scams = parse_scam_page(city_slug)
        scams.extend(city_scams)

    profile = {
        "id": f"country-safety:{iso2.lower()}",
        "iso2": iso2,
        "name": name,
        "lastUpdated": TODAY,

        "emergency": emergency,

        "embassies": [],

        "travelAdvisory": travel_advisory,

        "travelAdvisoryUK": travel_advisory_uk,

        "healthcare": healthcare,

        "medications": {
            "controlledSubstances": [],
            "generalAdvice": None,
        },

        "scams": scams,

        "connectivity": {
            "simOptions": None,
            "wifiAvailability": None,
            "bestOption": None,
        },

        "cultural": {
            "tipping": None,
            "dressCode": None,
            "greetings": None,
            "taboos": [],
            "haggling": None,
        },

        "phrases": [],

        "safety": {
            "overallRisk": None,
            "violentCrime": None,
            "pettyCrime": None,
            "naturalDisasters": [],
            "lgbtSafety": None,
            "soloFemaleSafety": None,
            "notes": None,
        },

        "practical": {
            "tapWater": tap_water,
            "drivingSide": None,
            "plugType": [],
            "voltage": None,
            "dialCode": None,
            "visaFreeCountries": None,
            "timeZone": None,
            "bestTimeToVisit": None,
        },
    }

    return profile


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    SAFETY_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading data sources...")
    emergency_data = load_emergency_numbers()
    us_advisories = load_us_advisories()
    uk_by_iso2, uk_by_slug = load_uk_advisories()
    print(f"  Emergency numbers: {len(emergency_data)} countries")
    print(f"  US advisories: {len(us_advisories)} countries")
    print(f"  UK advisories: {len(uk_by_iso2)} by iso2, {len(uk_by_slug)} by slug")

    skipped = []
    built = []

    for iso2 in PRIORITY_COUNTRIES:
        out_path = SAFETY_DIR / f"{iso2.lower()}.json"

        # JP and TH already have complete profiles — do not overwrite
        if iso2 in ("JP", "TH"):
            if out_path.exists():
                print(f"  ⏭️  {iso2}: skipping (existing complete profile)")
                skipped.append(iso2)
                continue
            # If somehow missing, fall through and build

        print(f"  🔨 {iso2} ({PRIORITY_COUNTRIES[iso2]['name']})...")
        profile = build_profile(iso2, emergency_data, us_advisories, uk_by_iso2, uk_by_slug)
        out_path.write_text(json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8")
        built.append(iso2)

    print(f"\n✅ Built {len(built)} profiles: {', '.join(built)}")
    if skipped:
        print(f"⏭️  Skipped {len(skipped)} existing: {', '.join(skipped)}")
    print(f"\nOutput: {SAFETY_DIR}")


if __name__ == "__main__":
    main()
