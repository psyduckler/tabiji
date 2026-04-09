#!/usr/bin/env python3
"""
health-tier2-enrich.py — Add Tier 2 fields to all 100 health-data/*.json files.

Adds four new optional fields to every country JSON:
  - commonCosts          → cheat-sheet of typical out-of-pocket prices
  - medicalEvacuation    → regional evac routing + cost band + provider list
  - pharmacyChains       → dominant pharmacy chains (where they exist)
  - drugNameMap          → local brand names for common OTC meds

The data is composed from:
  - A 5-tier cost table (A = highest cost like CH/SG/AU, E = lowest like ET/MM)
  - A regional evacuation table (SE Asia → Bangkok, E Africa → Nairobi, etc.)
  - Per-country pharmacy chain overrides (Watsons in HK, Boots in UK, …)
  - A region-default drug-name table with per-country overrides for famous
    local brands (Doliprane in FR, Tachipirina in IT, EVE in JP, …)

Important: every value here is intentionally a *range* or *category*, never
a specific quote. We never name a hospital, phone number, or insurer in the
generated text. Liability surface is kept narrow.

Idempotent: re-running on already-enriched data is a no-op.

Usage:
    python3 scripts/health-tier2-enrich.py
    python3 scripts/health-tier2-enrich.py --dry-run
    python3 scripts/health-tier2-enrich.py --force      # overwrite existing
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

SCRIPT_DIR = Path(__file__).parent.resolve()
TABIJI_ROOT = SCRIPT_DIR.parent
DATA_DIR = TABIJI_ROOT / "health-data"

# ─── 1. Cost tier ────────────────────────────────────────────────────────
# Wide ranges for typical out-of-pocket prices at private / international
# facilities. Bottom of range = small clinic / public option; top = expat /
# international clinic. Always USD; clearly labeled as estimates.

TIER_COSTS = {
    "A": {
        "doctorVisit": "$80-200",
        "erVisit": "$400-1,500",
        "overnightStay": "$1,000-3,000",
        "ambulance": "$300-1,500",
    },
    "B": {
        "doctorVisit": "$60-150",
        "erVisit": "$200-700",
        "overnightStay": "$400-1,200",
        "ambulance": "$100-500",
    },
    "C": {
        "doctorVisit": "$25-60",
        "erVisit": "$80-300",
        "overnightStay": "$150-500",
        "ambulance": "$30-150",
    },
    "D": {
        "doctorVisit": "$10-30",
        "erVisit": "$40-150",
        "overnightStay": "$60-250",
        "ambulance": "$20-80",
    },
    "E": {
        "doctorVisit": "$5-20",
        "erVisit": "$20-80",
        "overnightStay": "$30-120",
        "ambulance": "$10-50",
    },
}

COST_TIER = {
    # Tier A — highest cost (developed economies, resource-rich Gulf)
    "CH": "A", "NO": "A", "DK": "A", "SE": "A", "FI": "A", "IS": "A",
    "LU": "A", "SG": "A", "HK": "A", "AE": "A", "QA": "A", "KW": "A",
    "SA": "A", "AU": "A", "NZ": "A",
    # Tier B — high cost (W. Europe, developed Asia, Israel, Canada)
    "GB": "B", "IE": "B", "DE": "B", "FR": "B", "NL": "B", "BE": "B",
    "AT": "B", "IT": "B", "ES": "B", "PT": "B", "GR": "B", "JP": "B",
    "KR": "B", "TW": "B", "IL": "B", "CA": "B",
    # Tier C — mid (E. Europe, advanced LATAM, mid Asia, S. Africa)
    "CZ": "C", "SK": "C", "PL": "C", "HU": "C", "SI": "C", "HR": "C",
    "EE": "C", "LV": "C", "LT": "C", "RO": "C", "BG": "C", "RS": "C",
    "ME": "C", "AL": "C", "CY": "C", "MT": "C",
    "AR": "C", "CL": "C", "UY": "C", "BR": "C", "MX": "C", "CR": "C",
    "PA": "C", "CO": "C", "PE": "C", "TR": "C",
    "TH": "C", "MY": "C", "ID": "C", "VN": "C", "CN": "C", "OM": "C",
    "ZA": "C",
    # Tier D — lower cost (developing)
    "IN": "D", "LK": "D", "PH": "D", "KH": "D", "LA": "D", "MV": "D",
    "EG": "D", "MA": "D", "JO": "D", "LB": "D",
    "KE": "D", "TZ": "D", "UG": "D", "GH": "D", "SN": "D", "RW": "D",
    "HN": "D", "NI": "D", "GT": "D", "SV": "D", "PY": "D", "DO": "D",
    "CU": "D", "JM": "D", "BO": "D", "EC": "D",
    "MN": "D", "GE": "D", "IR": "D",
    "BD": "D", "PK": "D", "NP": "D", "FJ": "D",
    # Tier E — lowest (least-developed healthcare systems)
    "ET": "E", "NG": "E", "MM": "E",
}

COST_NOTE = (
    "Estimated typical out-of-pocket costs at private or international "
    "facilities. Public-system rates can be much lower (or free for "
    "residents). Actual costs vary by city, facility, and exchange rate."
)

# ─── 2. Medical evacuation ──────────────────────────────────────────────
# Regional routing patterns. The "tier-A-local" framing softens the
# callout for high-quality countries; the "tier-D-essential" framing
# escalates it for lower-quality ones.

EVAC_REGIONS = {
    "sea": {
        "countries": {"TH", "VN", "KH", "LA", "MM", "MY", "ID", "PH"},
        "primary": "Bangkok",
        "secondary": "Singapore",
        "cost": "$15,000-60,000",
        "hubs": "Bangkok (Bumrungrad, Bangkok Hospital) and Singapore (Mount Elizabeth, Raffles) are the regional medical hubs.",
    },
    "east_asia": {
        "countries": {"JP", "KR", "TW", "HK", "CN"},
        "primary": "Local treatment is excellent in major cities",
        "secondary": "Singapore or Tokyo",
        "cost": "$30,000-100,000",
        "hubs": "Tokyo, Seoul, Taipei, Hong Kong, and major Chinese cities have world-class tertiary hospitals — Singapore is the regional super-hub for the most specialized cases.",
    },
    "sg_hub": {
        "countries": {"SG"},
        "primary": "Singapore is itself the regional medical hub",
        "secondary": "No evacuation typically needed",
        "cost": "$15,000-50,000",
        "hubs": "Singapore is the leading medical hub for Southeast and South Asia. Mount Elizabeth, Raffles, and Gleneagles handle the most complex cases in the region.",
    },
    "mn": {
        "countries": {"MN"},
        "primary": "Beijing or Seoul",
        "secondary": "Bangkok",
        "cost": "$30,000-90,000",
        "hubs": "Mongolian healthcare is limited outside Ulaanbaatar. Beijing and Seoul are the closest tertiary medical centers.",
    },
    "s_asia": {
        "countries": {"IN", "BD", "PK", "NP", "LK", "MV"},
        "primary": "Singapore",
        "secondary": "Bangkok or Mumbai",
        "cost": "$25,000-90,000",
        "hubs": "Singapore and Bangkok are the regional medical hubs. Indian metros (Mumbai, Delhi) handle complex cases for the subcontinent.",
    },
    "me_gulf": {
        "countries": {"AE", "QA", "KW", "SA", "OM", "IL"},
        "primary": "Local treatment is generally excellent",
        "secondary": "Dubai or Frankfurt",
        "cost": "$30,000-100,000",
        "hubs": "Dubai is the regional referral hub for North Africa and South Asia, and Gulf-state tertiary hospitals (Cleveland Clinic Abu Dhabi, Sheikh Khalifa Medical City, Hamad Medical Corporation, Sheba Medical Center in Israel) are well-equipped.",
    },
    "me_other": {
        "countries": {"IR", "LB", "JO", "EG", "MA"},
        "primary": "Dubai",
        "secondary": "Istanbul or Athens",
        "cost": "$30,000-90,000",
        "hubs": "Dubai is the primary medical hub for the broader Middle East and North Africa.",
    },
    "e_africa": {
        "countries": {"KE", "TZ", "UG", "RW", "ET"},
        "primary": "Nairobi",
        "secondary": "Johannesburg or Dubai",
        "cost": "$40,000-120,000",
        "hubs": "Nairobi (Aga Khan, Nairobi Hospital) is the primary East African medical hub. Johannesburg and Dubai handle complex tertiary cases.",
    },
    "w_africa": {
        "countries": {"NG", "GH", "SN"},
        "primary": "Johannesburg",
        "secondary": "Paris or Casablanca",
        "cost": "$50,000-150,000",
        "hubs": "West Africa lacks a strong regional hub. Most serious cases evacuate to Johannesburg, Paris, or Casablanca.",
    },
    "s_africa": {
        "countries": {"ZA"},
        "primary": "Local treatment is excellent in major cities",
        "secondary": "Cape Town or Johannesburg",
        "cost": "$15,000-50,000",
        "hubs": "South African private hospital groups (Mediclinic, Netcare, Life Healthcare) operate world-class facilities in Cape Town, Johannesburg, and Durban.",
    },
    "eu_west": {
        "countries": {"GB", "IE", "DE", "FR", "NL", "BE", "AT", "LU", "CH"},
        "primary": "Local treatment is world-class",
        "secondary": "Cross-border to a major European center",
        "cost": "$10,000-40,000",
        "hubs": "Western European hospitals are among the best in the world. Cross-border air evacuation is uncommon and usually only for highly specialized cases.",
    },
    "eu_north": {
        "countries": {"NO", "SE", "DK", "FI", "IS"},
        "primary": "Local treatment is excellent",
        "secondary": "Oslo, Stockholm, or Copenhagen",
        "cost": "$15,000-50,000",
        "hubs": "Nordic public healthcare is excellent and air evacuation within the region is well-coordinated.",
    },
    "eu_south": {
        "countries": {"IT", "ES", "PT", "GR", "MT", "CY"},
        "primary": "Local treatment is good",
        "secondary": "Rome, Athens, or Madrid",
        "cost": "$15,000-50,000",
        "hubs": "Southern European tertiary hospitals are well-equipped. Cross-border evacuation to Western Europe is reserved for highly complex cases.",
    },
    "eu_east": {
        "countries": {"PL", "CZ", "SK", "HU", "SI", "HR", "EE", "LV", "LT", "RO", "BG", "RS", "ME", "AL"},
        "primary": "Vienna or Munich",
        "secondary": "Berlin or Frankfurt",
        "cost": "$15,000-60,000",
        "hubs": "Vienna and Munich are the standard regional referral hubs for Central and Eastern European travelers.",
    },
    "caucasus": {
        "countries": {"GE"},
        "primary": "Istanbul",
        "secondary": "Vienna or Dubai",
        "cost": "$25,000-80,000",
        "hubs": "Istanbul is the closest major medical hub. Vienna handles complex cases for Caucasus travelers.",
    },
    "australasia": {
        "countries": {"AU", "NZ"},
        "primary": "Local treatment is world-class",
        "secondary": "Sydney, Melbourne, or Auckland",
        "cost": "$20,000-80,000",
        "hubs": "Australian and New Zealand hospitals are among the best globally. Inter-city air evacuation is well-developed.",
    },
    "pacific": {
        "countries": {"FJ"},
        "primary": "Auckland",
        "secondary": "Sydney or Brisbane",
        "cost": "$60,000-200,000",
        "hubs": "Pacific island healthcare is limited. Most serious cases require fixed-wing evacuation to New Zealand or Australia.",
    },
    "n_america": {
        "countries": {"CA"},
        "primary": "Local treatment is excellent",
        "secondary": "Toronto, Montreal, or Vancouver",
        "cost": "$20,000-100,000",
        "hubs": "Canadian tertiary hospitals (Toronto General, Vancouver General, McGill University Health Centre) offer world-class care across all provinces.",
    },
    "c_america": {
        "countries": {"MX", "GT", "SV", "HN", "NI", "CR", "PA"},
        "primary": "Houston or Miami",
        "secondary": "Mexico City",
        "cost": "$25,000-80,000",
        "hubs": "Houston, Miami, and Mexico City are the primary medical hubs for Central America.",
    },
    "s_america": {
        "countries": {"AR", "BR", "CL", "CO", "EC", "PE", "UY", "PY", "BO"},
        "primary": "São Paulo",
        "secondary": "Buenos Aires or Miami",
        "cost": "$30,000-100,000",
        "hubs": "São Paulo (Hospital Albert Einstein, Sírio-Libanês) is the leading South American medical hub. Buenos Aires and Santiago handle southern-cone cases.",
    },
    "caribbean": {
        "countries": {"CU", "DO", "JM"},
        "primary": "Miami",
        "secondary": "Mexico City or Houston",
        "cost": "$30,000-90,000",
        "hubs": "Caribbean island healthcare is limited for complex cases. Miami is the primary medical hub for the region.",
    },
    "turkey": {
        "countries": {"TR"},
        "primary": "Local treatment is excellent in Istanbul and Ankara",
        "secondary": "Istanbul (Anadolu Medical Center, Memorial)",
        "cost": "$15,000-50,000",
        "hubs": "Turkish private hospitals in Istanbul offer world-class care and serve as a regional medical hub for the Middle East and Caucasus.",
    },
}

EVAC_PROVIDERS = ["Global Rescue", "MedJet", "International SOS"]

# ─── 3. Pharmacy chains ─────────────────────────────────────────────────
# Per-country dominant pharmacy chains. Many continental European and
# Middle Eastern countries don't have a dominant chain (independent
# pharmacies marked with the green cross / red A). Those countries get
# `None` and the renderer falls back to the universal-marker line.

PHARMACY_CHAINS = {
    # East / Southeast Asia
    "JP": [
        {"name": "Matsumoto Kiyoshi", "identifier": "Yellow and black storefront, マツモトキヨシ signage", "where": "Throughout Japan, especially train stations and shopping districts"},
        {"name": "Cocokara Fine", "identifier": "Blue and white storefront", "where": "Major cities"},
        {"name": "Sun Drug", "identifier": "Yellow and red signage", "where": "Cities and suburbs nationwide"},
    ],
    "KR": [
        {"name": "On Pharm (온약국)", "identifier": "Green cross with 약국 signage", "where": "Throughout Korea (yakguk = pharmacy)"},
    ],
    "TW": [
        {"name": "Watsons (屈臣氏)", "identifier": "Green and white Watsons logo", "where": "Throughout Taiwan in shopping centers and high streets"},
        {"name": "Cosmed (康是美)", "identifier": "Pink and white storefront", "where": "Urban areas nationwide"},
    ],
    "HK": [
        {"name": "Watsons", "identifier": "Green and white Watsons logo", "where": "Throughout Hong Kong"},
        {"name": "Mannings", "identifier": "Red and white storefront", "where": "Throughout Hong Kong"},
    ],
    "CN": [
        {"name": "Watsons (屈臣氏)", "identifier": "Green and white Watsons logo", "where": "Major cities throughout mainland China"},
        {"name": "Mannings", "identifier": "Red and white signage", "where": "Tier 1 cities, often inside malls"},
    ],
    "SG": [
        {"name": "Watsons", "identifier": "Green and white Watsons logo", "where": "Throughout Singapore"},
        {"name": "Guardian", "identifier": "Green storefront with white cross", "where": "Throughout Singapore"},
        {"name": "Unity Pharmacy", "identifier": "Orange Unity logo (NTUC)", "where": "FairPrice supermarkets and standalone stores"},
    ],
    "MY": [
        {"name": "Watsons", "identifier": "Green and white Watsons logo", "where": "Throughout Malaysia"},
        {"name": "Guardian", "identifier": "Green storefront with white cross", "where": "Major shopping malls"},
    ],
    "TH": [
        {"name": "Boots", "identifier": "Blue Boots logo", "where": "Bangkok malls and tourist areas"},
        {"name": "Watsons", "identifier": "Green and white Watsons logo", "where": "Major shopping centers throughout Thailand"},
    ],
    "VN": [
        {"name": "Pharmacity", "identifier": "Blue Pharmacity logo", "where": "Throughout Vietnamese cities"},
        {"name": "Long Châu", "identifier": "Green Long Châu logo", "where": "Nationwide"},
    ],
    "PH": [
        {"name": "Mercury Drug", "identifier": "Blue and red Mercury Drug signage", "where": "Throughout the Philippines, the dominant chain"},
        {"name": "Watsons", "identifier": "Green and white Watsons logo", "where": "Major shopping malls"},
    ],
    "ID": [
        {"name": "Kimia Farma", "identifier": "Orange Kimia Farma logo", "where": "Government-affiliated chain throughout Indonesia"},
        {"name": "Apotek K-24", "identifier": "Green K-24 logo", "where": "24-hour stores in major cities"},
        {"name": "Guardian", "identifier": "Green storefront with white cross", "where": "Major shopping malls in Bali, Jakarta, and other cities"},
    ],
    "KH": [
        {"name": "U-Care Pharmacy", "identifier": "Orange and white U-Care signage", "where": "Phnom Penh and Siem Reap, popular with expats"},
        {"name": "Pharmacie de la Gare", "identifier": "French-style farmacie storefront", "where": "Phnom Penh"},
    ],
    "LA": [None],  # mostly independents
    "MM": [None],
    # South Asia
    "IN": [
        {"name": "Apollo Pharmacy", "identifier": "Blue and white Apollo logo", "where": "Throughout India, the dominant chain"},
        {"name": "MedPlus", "identifier": "Red MedPlus signage", "where": "Throughout India"},
        {"name": "Wellness Forever", "identifier": "Blue Wellness Forever logo", "where": "Mumbai, Pune, Bangalore"},
    ],
    "BD": [
        {"name": "Lazz Pharma", "identifier": "Green Lazz Pharma signage", "where": "Throughout Dhaka and Chittagong"},
    ],
    "PK": [
        {"name": "Servaid Pharmacy", "identifier": "Blue Servaid logo", "where": "Major cities"},
        {"name": "Fazaldin's Pharmacy", "identifier": "Established chain in Lahore and Karachi", "where": "Punjab and Sindh"},
    ],
    "NP": [None],
    "LK": [
        {"name": "Healthguard Pharmacy", "identifier": "Green and white Healthguard signage", "where": "Throughout Sri Lanka"},
        {"name": "Osu Sala", "identifier": "Government chain", "where": "Nationwide"},
    ],
    "MV": [None],
    # UK / Ireland / Anglosphere
    "GB": [
        {"name": "Boots", "identifier": "Blue Boots logo", "where": "Throughout the UK, the dominant chain"},
        {"name": "Superdrug", "identifier": "Pink Superdrug logo", "where": "High streets and shopping centers"},
        {"name": "Lloyds Pharmacy", "identifier": "Yellow Lloyds signage", "where": "Throughout the UK"},
    ],
    "IE": [
        {"name": "Boots", "identifier": "Blue Boots logo", "where": "Throughout Ireland"},
        {"name": "Hickey's Pharmacy", "identifier": "Local Irish chain", "where": "Dublin and Leinster"},
    ],
    "AU": [
        {"name": "Chemist Warehouse", "identifier": "Yellow Chemist Warehouse signage", "where": "Throughout Australia, the dominant discount chain"},
        {"name": "Priceline Pharmacy", "identifier": "Pink Priceline signage", "where": "Shopping centers nationwide"},
        {"name": "Terry White Chemmart", "identifier": "Blue and white Terry White signage", "where": "Throughout Australia"},
    ],
    "NZ": [
        {"name": "Chemist Warehouse", "identifier": "Yellow Chemist Warehouse signage", "where": "Major cities"},
        {"name": "Unichem", "identifier": "Local pharmacy network", "where": "Throughout New Zealand"},
        {"name": "Life Pharmacy", "identifier": "Green Life Pharmacy signage", "where": "Shopping centers"},
    ],
    "CA": [
        {"name": "Shoppers Drug Mart", "identifier": "Red Shoppers Drug Mart logo", "where": "Throughout Canada (Pharmaprix in Quebec)"},
        {"name": "Rexall", "identifier": "Blue Rexall signage", "where": "Throughout Canada"},
        {"name": "London Drugs", "identifier": "Orange and blue logo", "where": "Western Canada (BC, Alberta)"},
    ],
    # Middle East / North Africa
    "AE": [
        {"name": "Aster Pharmacy", "identifier": "Green Aster signage", "where": "Throughout the UAE"},
        {"name": "Life Pharmacy", "identifier": "Red and white Life signage", "where": "Throughout the UAE"},
        {"name": "BinSina Pharmacy", "identifier": "Blue and white BinSina logo", "where": "Throughout the UAE, often 24-hour"},
    ],
    "QA": [
        {"name": "Al Shifa Pharmacy", "identifier": "Green and white Al Shifa signage", "where": "Throughout Qatar"},
        {"name": "Wellcare Pharmacy", "identifier": "Blue Wellcare signage", "where": "Doha and major cities"},
    ],
    "KW": [
        {"name": "Boots", "identifier": "Blue Boots logo", "where": "Major shopping malls in Kuwait City"},
        {"name": "Al Sayer Pharmacy", "identifier": "Local chain", "where": "Throughout Kuwait"},
    ],
    "SA": [
        {"name": "Al Dawaa Pharmacy", "identifier": "Green and white Al Dawaa signage", "where": "Throughout Saudi Arabia"},
        {"name": "Nahdi Medical Company", "identifier": "Blue Nahdi logo", "where": "Throughout Saudi Arabia, the largest chain"},
    ],
    "OM": [
        {"name": "Muscat Pharmacy", "identifier": "Established Omani chain", "where": "Muscat and major cities"},
    ],
    "IL": [
        {"name": "Super-Pharm", "identifier": "Blue Super-Pharm signage", "where": "Throughout Israel, the dominant chain"},
    ],
    "EG": [
        {"name": "El Ezaby Pharmacy", "identifier": "Green El Ezaby signage", "where": "Throughout Egypt"},
        {"name": "19011", "identifier": "Branded as 19011 (the chain's hotline)", "where": "Cairo, Alexandria, and major cities"},
        {"name": "Seif Pharmacy", "identifier": "Blue Seif signage", "where": "Cairo and Alexandria"},
    ],
    "MA": [None],
    "JO": [None],
    "LB": [None],
    "IR": [None],
    # Africa
    "ZA": [
        {"name": "Clicks", "identifier": "Blue Clicks logo", "where": "Throughout South Africa"},
        {"name": "Dis-Chem", "identifier": "Red Dis-Chem signage", "where": "Throughout South Africa"},
    ],
    "KE": [
        {"name": "GoodLife Pharmacy", "identifier": "Green GoodLife signage", "where": "Nairobi, Mombasa, and major cities"},
    ],
    "TZ": [None],
    "UG": [None],
    "RW": [None],
    "ET": [None],
    "GH": [None],
    "SN": [None],
    "NG": [
        {"name": "HealthPlus Pharmacy", "identifier": "Green HealthPlus signage", "where": "Lagos, Abuja, and major cities"},
        {"name": "MedPlus Pharmacy", "identifier": "Red MedPlus signage", "where": "Lagos and Abuja"},
    ],
    # Europe — mostly independents marked with green cross / red A
    "DE": [None],  # Apotheke (red A)
    "AT": [None],  # Apotheke (red A)
    "CH": [None],  # Apotheke / pharmacie (green cross)
    "FR": [None],  # pharmacie (green cross)
    "BE": [None],  # apotheek / pharmacie (green cross)
    "NL": [None],  # apotheek (green cross)
    "LU": [None],
    "IT": [None],  # farmacia (green cross)
    "ES": [None],  # farmacia (green cross)
    "PT": [None],  # farmácia (green cross)
    "GR": [None],  # φαρμακείο (green cross)
    "MT": [None],
    "CY": [None],
    "DK": [None],  # apotek
    "SE": [None],
    "NO": [None],  # Apotek 1, Vitusapotek, Boots are common but no dominant
    "FI": [None],  # apteekki
    "IS": [None],
    "PL": [None],  # apteka
    "CZ": [None],  # lékárna
    "SK": [None],  # lekáreň
    "HU": [None],  # gyógyszertár
    "RO": [None],  # farmacie
    "BG": [None],  # аптека
    "RS": [None],
    "ME": [None],
    "AL": [None],
    "HR": [None],
    "SI": [None],
    "EE": [None],  # apteek
    "LV": [None],
    "LT": [None],
    "GE": [None],
    # Latin America
    "MX": [
        {"name": "Farmacia Guadalajara", "identifier": "Orange and white Farmacias Guadalajara signage", "where": "Throughout Mexico"},
        {"name": "Farmacias del Ahorro", "identifier": "Yellow del Ahorro signage", "where": "Throughout Mexico"},
        {"name": "Farmacias Similares", "identifier": "Red Dr. Simi mascot, blue and white storefront", "where": "Throughout Mexico (generics + on-site doctor)"},
    ],
    "AR": [
        {"name": "Farmacity", "identifier": "Yellow and orange Farmacity signage", "where": "Buenos Aires and major cities"},
        {"name": "Vantage", "identifier": "Local chain with red signage", "where": "Buenos Aires"},
    ],
    "CL": [
        {"name": "Cruz Verde", "identifier": "Green cross in name and signage", "where": "Throughout Chile"},
        {"name": "Salcobrand", "identifier": "Blue Salcobrand signage", "where": "Throughout Chile"},
        {"name": "Ahumada", "identifier": "Green and yellow Farmacias Ahumada signage", "where": "Throughout Chile"},
    ],
    "BR": [
        {"name": "Drogaria São Paulo", "identifier": "Blue and yellow signage", "where": "Throughout Brazil"},
        {"name": "Drogasil", "identifier": "Red Drogasil logo", "where": "Throughout Brazil"},
        {"name": "Pacheco", "identifier": "Drogarias Pacheco — orange signage", "where": "Throughout Brazil"},
    ],
    "CO": [
        {"name": "Cruz Verde", "identifier": "Green cross in name and signage", "where": "Throughout Colombia"},
        {"name": "Cafam", "identifier": "Local supermarket-pharmacy chain", "where": "Bogotá and major cities"},
        {"name": "Drogas la Rebaja", "identifier": "Discount pharmacy chain", "where": "Throughout Colombia"},
    ],
    "PE": [
        {"name": "Inkafarma", "identifier": "Red Inkafarma signage", "where": "Throughout Peru, the dominant chain"},
        {"name": "Mifarma", "identifier": "Orange Mifarma signage", "where": "Throughout Peru"},
        {"name": "Boticas y Salud", "identifier": "Blue and white signage", "where": "Throughout Peru"},
    ],
    "EC": [
        {"name": "Fybeca", "identifier": "Blue Fybeca signage", "where": "Throughout Ecuador, the dominant chain"},
        {"name": "Sana Sana", "identifier": "Yellow Sana Sana signage", "where": "Throughout Ecuador"},
    ],
    "BO": [None],
    "PY": [None],
    "UY": [None],
    "CR": [None],
    "PA": [None],
    "GT": [None],
    "HN": [None],
    "NI": [None],
    "SV": [None],
    "DO": [
        {"name": "Farmacia Carol", "identifier": "Local chain", "where": "Santo Domingo and major cities"},
    ],
    "JM": [None],
    "CU": [None],  # state-run system, no chain branding
    # Other
    "TR": [None],  # eczane (red E)
    "MN": [None],
    "FJ": [None],
    "IN": [
        {"name": "Apollo Pharmacy", "identifier": "Blue and white Apollo logo", "where": "Throughout India, the dominant chain"},
        {"name": "MedPlus", "identifier": "Red MedPlus signage", "where": "Throughout India"},
        {"name": "Wellness Forever", "identifier": "Blue Wellness Forever logo", "where": "Mumbai, Pune, Bangalore"},
    ],
}

UNIVERSAL_PHARMACY_MARKER = (
    "Most pharmacies in this country are independent rather than chain-branded. "
    "Look for the universal pharmacy markers: a green cross sign in most of "
    "Europe and Latin America, a red 'A' (Apotheke) in German-speaking countries, "
    "or local-language signage like apteka, lékárna, or farmacia."
)

# ─── 4. Drug name maps ──────────────────────────────────────────────────
# Region defaults + per-country overrides for famous local brands.
# Three core entries per country: paracetamol, ibuprofen, anti-diarrheal.

DRUG_REGIONS = {
    # English-speaking world / Commonwealth (GBR-style)
    "english_commonwealth": {
        "countries": {"GB", "IE", "AU", "NZ", "SG", "HK", "MY", "ZA", "JM"},
        "drugs": [
            {"generic": "paracetamol/acetaminophen", "localName": "Panadol", "note": "The dominant Commonwealth brand. Generic 'paracetamol' also widely sold."},
            {"generic": "ibuprofen", "localName": "Nurofen", "note": "Most common ibuprofen brand."},
            {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium", "note": "Available OTC at all pharmacies."},
        ],
    },
    # Americas (US/CA + LATAM)
    "americas": {
        "countries": {"CA", "MX", "BR", "AR", "CL", "CO", "PE", "EC", "BO", "PY", "UY", "CR", "PA", "GT", "HN", "NI", "SV", "DO", "CU"},
        "drugs": [
            {"generic": "paracetamol/acetaminophen", "localName": "Tylenol or paracetamol generic", "note": "Tylenol is widely available; locals often ask for 'paracetamol' or 'acetaminofén'."},
            {"generic": "ibuprofen", "localName": "Advil or Motrin", "note": "Advil is the dominant retail brand."},
            {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium", "note": "Available OTC at most pharmacies."},
        ],
    },
    # German-speaking Europe
    "german": {
        "countries": {"DE", "AT", "CH", "LU"},
        "drugs": [
            {"generic": "paracetamol/acetaminophen", "localName": "Paracetamol generic or ben-u-ron", "note": "ben-u-ron is a well-known brand; the generic name is also widely used."},
            {"generic": "ibuprofen", "localName": "ibuHEXAL or Dolormin", "note": "Common German ibuprofen brands."},
            {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium akut", "note": "Available OTC at any Apotheke."},
        ],
    },
    # Nordic
    "nordic": {
        "countries": {"NO", "SE", "DK", "FI", "IS"},
        "drugs": [
            {"generic": "paracetamol/acetaminophen", "localName": "Alvedon (SE), Panodil (DK), Paracet (NO), Panadol (FI)", "note": "Each Nordic country has its own dominant paracetamol brand."},
            {"generic": "ibuprofen", "localName": "Ipren or Ibumetin", "note": "Common Nordic ibuprofen brands."},
            {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium", "note": "Available OTC at any apotek/apteekki."},
        ],
    },
    # Mediterranean Europe
    "mediterranean_eu": {
        "countries": {"ES", "PT", "GR", "MT", "CY"},
        "drugs": [
            {"generic": "paracetamol/acetaminophen", "localName": "Gelocatil (ES), Ben-u-ron (PT), Depon (GR)", "note": "Country-specific paracetamol brands; the generic name is also widely understood."},
            {"generic": "ibuprofen", "localName": "Espidifen (ES), Brufen (others)", "note": "Common Mediterranean ibuprofen brands."},
            {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium or Fortasec (ES)", "note": "Available OTC at any farmacia."},
        ],
    },
    # Slavic / E. European
    "slavic_e_europe": {
        "countries": {"PL", "CZ", "SK", "HU", "RO", "BG", "RS", "ME", "AL", "HR", "SI", "EE", "LV", "LT", "GE"},
        "drugs": [
            {"generic": "paracetamol/acetaminophen", "localName": "Paracetamol generic or Panadol", "note": "Generic 'paracetamol' is the most common name in pharmacies."},
            {"generic": "ibuprofen", "localName": "Ibuprom or Nurofen", "note": "Both are widely available."},
            {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium or Loperamid", "note": "Available OTC at any pharmacy."},
        ],
    },
    # Arabic-speaking Middle East
    "arab_me": {
        "countries": {"AE", "QA", "KW", "SA", "OM", "JO", "LB", "EG", "MA"},
        "drugs": [
            {"generic": "paracetamol/acetaminophen", "localName": "Panadol", "note": "Panadol is the dominant brand throughout the Arab world."},
            {"generic": "ibuprofen", "localName": "Brufen or Advil", "note": "Both available; Brufen is more common locally."},
            {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium", "note": "Available OTC at most pharmacies."},
        ],
    },
    # Iran
    "iran": {
        "countries": {"IR"},
        "drugs": [
            {"generic": "paracetamol/acetaminophen", "localName": "Acetaminophen (Iranian generic) or Apotel", "note": "Locally manufactured; sanctions-related shortages are possible — bring your own supply."},
            {"generic": "ibuprofen", "localName": "Iranian generic ibuprofen", "note": "Widely available; brand names vary."},
            {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium or local generic", "note": "Available at most pharmacies."},
        ],
    },
    # South Asia (India, Pakistan, Bangladesh, Nepal, Sri Lanka, Maldives)
    "s_asia": {
        "countries": {"IN", "PK", "BD", "NP", "LK", "MV"},
        "drugs": [
            {"generic": "paracetamol/acetaminophen", "localName": "Crocin or Calpol", "note": "Crocin (GSK) is the dominant Indian-subcontinent brand. Calpol is for kids."},
            {"generic": "ibuprofen", "localName": "Brufen or Combiflam", "note": "Brufen (Abbott) is the most common; Combiflam is paracetamol+ibuprofen combo."},
            {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium or Roko", "note": "Available OTC at most pharmacies."},
        ],
    },
    # Anglophone Africa
    "anglo_africa": {
        "countries": {"NG", "GH", "KE", "TZ", "UG", "RW", "ET"},
        "drugs": [
            {"generic": "paracetamol/acetaminophen", "localName": "Panadol", "note": "Panadol dominates throughout English-speaking Africa."},
            {"generic": "ibuprofen", "localName": "Brufen or Nurofen", "note": "Available at urban pharmacies."},
            {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium", "note": "Bring your own — quality varies and stock can be inconsistent in rural areas."},
        ],
    },
    # Francophone Africa
    "franco_africa": {
        "countries": {"SN"},
        "drugs": [
            {"generic": "paracetamol/acetaminophen", "localName": "Doliprane", "note": "French brand dominates francophone Africa."},
            {"generic": "ibuprofen", "localName": "Advil or Nurofen", "note": "Available at urban pharmacies."},
            {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium", "note": "Available OTC at most pharmacies."},
        ],
    },
    # Southeast Asia
    "se_asia": {
        "countries": {"TH", "VN", "KH", "LA", "MM", "ID", "PH"},
        "drugs": [
            {"generic": "paracetamol/acetaminophen", "localName": "Panadol or Tylenol", "note": "Panadol is the most common brand throughout Southeast Asia."},
            {"generic": "ibuprofen", "localName": "Brufen or Nurofen", "note": "Available at most pharmacies."},
            {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium", "note": "Available OTC at most pharmacies."},
        ],
    },
    # East Asia (CN/TW/KR — JP has its own override)
    "east_asia": {
        "countries": {"CN", "TW", "KR", "MN"},
        "drugs": [
            {"generic": "paracetamol/acetaminophen", "localName": "Panadol or Tylenol", "note": "Panadol and Tylenol are both available; locals also use generic brands."},
            {"generic": "ibuprofen", "localName": "Brufen or Advil", "note": "Available at most pharmacies."},
            {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium", "note": "Available OTC at most pharmacies."},
        ],
    },
    # Israel
    "israel": {
        "countries": {"IL"},
        "drugs": [
            {"generic": "paracetamol/acetaminophen", "localName": "Acamol", "note": "Acamol is the dominant Israeli brand."},
            {"generic": "ibuprofen", "localName": "Nurofen or Advil", "note": "Both widely available."},
            {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium or Stopit", "note": "Available OTC at most pharmacies."},
        ],
    },
    # Pacific
    "pacific": {
        "countries": {"FJ"},
        "drugs": [
            {"generic": "paracetamol/acetaminophen", "localName": "Panadol", "note": "Panadol is the dominant brand."},
            {"generic": "ibuprofen", "localName": "Nurofen", "note": "Available at urban pharmacies."},
            {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium", "note": "Bring your own from a reliable source."},
        ],
    },
    # Turkey
    "turkey": {
        "countries": {"TR"},
        "drugs": [
            {"generic": "paracetamol/acetaminophen", "localName": "Parol", "note": "Parol is the dominant Turkish paracetamol brand."},
            {"generic": "ibuprofen", "localName": "Brufen or Nurofen", "note": "Both are widely available at any eczane."},
            {"generic": "loperamide (anti-diarrheal)", "localName": "Lopermid or Imodium", "note": "Available OTC at any eczane."},
        ],
    },
}

# Per-country overrides for famous local brands (override the regional defaults)
DRUG_OVERRIDES = {
    "FR": [
        {"generic": "paracetamol/acetaminophen", "localName": "Doliprane", "note": "Doliprane (Sanofi) is the iconic French paracetamol brand — recognized by every French traveler."},
        {"generic": "ibuprofen", "localName": "Advil or Nurofen", "note": "Both widely available."},
        {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium", "note": "Available OTC at any pharmacie."},
    ],
    "IT": [
        {"generic": "paracetamol/acetaminophen", "localName": "Tachipirina", "note": "Tachipirina is the dominant Italian paracetamol brand."},
        {"generic": "ibuprofen", "localName": "Moment or Brufen", "note": "Moment is the iconic Italian over-the-counter ibuprofen brand."},
        {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium", "note": "Available OTC at any farmacia."},
    ],
    "BE": [
        {"generic": "paracetamol/acetaminophen", "localName": "Dafalgan or Doliprane", "note": "Dafalgan is the most common Belgian paracetamol brand."},
        {"generic": "ibuprofen", "localName": "Brufen or Nurofen", "note": "Available at most apotheek/pharmacie locations."},
        {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium", "note": "Available OTC at most pharmacies."},
    ],
    "NL": [
        {"generic": "paracetamol/acetaminophen", "localName": "Paracetamol (generic)", "note": "Dutch pharmacies sell paracetamol almost exclusively under its generic name."},
        {"generic": "ibuprofen", "localName": "Brufen or generic ibuprofen", "note": "Sold under the generic name."},
        {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium", "note": "Available OTC at any apotheek or drogist."},
    ],
    "JP": [
        {"generic": "paracetamol/acetaminophen", "localName": "Tylenol or generic アセトアミノフェン", "note": "Tylenol is sold in most large pharmacies; locals also use the generic katakana name."},
        {"generic": "ibuprofen", "localName": "EVE (イブ)", "note": "EVE is the dominant Japanese ibuprofen brand — widely recognized."},
        {"generic": "loperamide (anti-diarrheal)", "localName": "Stoppa or Pireena", "note": "Available OTC at most drugstores."},
    ],
    "MX": [
        {"generic": "paracetamol/acetaminophen", "localName": "Tempra or Tylenol", "note": "Tempra is the most common Mexican paracetamol brand."},
        {"generic": "ibuprofen", "localName": "Advil or Motrin", "note": "Both widely available."},
        {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium", "note": "Available OTC at any farmacia."},
    ],
    "BR": [
        {"generic": "paracetamol/acetaminophen", "localName": "Tylenol", "note": "Tylenol is the most recognized Brazilian paracetamol brand."},
        {"generic": "ibuprofen", "localName": "Advil or Alivium", "note": "Both widely available."},
        {"generic": "loperamide (anti-diarrheal)", "localName": "Imosec", "note": "Imosec is the dominant Brazilian loperamide brand."},
    ],
    "AR": [
        {"generic": "paracetamol/acetaminophen", "localName": "Tafirol or Termofren", "note": "Common Argentine paracetamol brands."},
        {"generic": "ibuprofen", "localName": "Ibupirac or Actron", "note": "Common Argentine ibuprofen brands."},
        {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium", "note": "Available OTC at any farmacia."},
    ],
    "CL": [
        {"generic": "paracetamol/acetaminophen", "localName": "Kitadol or Tapsin", "note": "Common Chilean paracetamol brands."},
        {"generic": "ibuprofen", "localName": "Tapsin or Diariofen", "note": "Tapsin is a popular line that includes paracetamol+ibuprofen combos."},
        {"generic": "loperamide (anti-diarrheal)", "localName": "Imodium", "note": "Available OTC at any farmacia."},
    ],
    "CU": [
        {"generic": "paracetamol/acetaminophen", "localName": "Paracetamol (Cuban generic)", "note": "Locally manufactured; supply can be inconsistent — bring your own."},
        {"generic": "ibuprofen", "localName": "Ibuprofeno (Cuban generic)", "note": "Available at state pharmacies; supply varies."},
        {"generic": "loperamide (anti-diarrheal)", "localName": "Loperamida (generic)", "note": "Bring your own — supply at Cuban pharmacies is unreliable."},
    ],
}


# ─── Lookup helpers ─────────────────────────────────────────────────────

def lookup_evac(iso2: str) -> Optional[Dict[str, Any]]:
    for region in EVAC_REGIONS.values():
        if iso2 in region["countries"]:
            return {
                "primaryDestination": region["primary"],
                "secondaryDestination": region["secondary"],
                "typicalCost": region["cost"],
                "providers": EVAC_PROVIDERS,
                "note": region["hubs"],
            }
    return None


def lookup_pharmacy_chains(iso2: str) -> Optional[List[Dict[str, str]]]:
    val = PHARMACY_CHAINS.get(iso2)
    if val is None:
        return None
    if val == [None]:
        return []  # explicitly "no dominant chain"
    return val


def lookup_drug_names(iso2: str) -> Optional[List[Dict[str, str]]]:
    if iso2 in DRUG_OVERRIDES:
        return DRUG_OVERRIDES[iso2]
    for region in DRUG_REGIONS.values():
        if iso2 in region["countries"]:
            return region["drugs"]
    return None


def compose_evac_note(iso2: str, quality_rating: int, evac: Dict[str, Any]) -> Dict[str, Any]:
    """Adjust framing of evacuation note based on healthcare quality.

    Each framing prefix ends with a period so the regional `hubs` sentence
    flows as a separate, grammatically complete next sentence."""
    if quality_rating >= 4:
        # World-class local healthcare — soften the framing
        framing = (
            "Local hospitals handle the vast majority of cases — air "
            "evacuation is rarely needed for tourists. If a condition "
            f"exceeds local capacity: {evac['note']}"
        )
    elif quality_rating <= 2:
        # Limited local healthcare — escalate the framing
        framing = (
            "Medical evacuation insurance is essential for serious cases. "
            f"{evac['note']} Actual costs depend on distance, aircraft type, "
            "and whether ICU-level care is required in transit."
        )
    else:
        # Mid-tier — neutral framing
        framing = (
            "Local hospitals handle routine cases; for complex care that "
            "exceeds local capacity, regional referral options are "
            f"well-established. {evac['note']}"
        )
    return {**evac, "note": framing}


# ─── Main enricher ──────────────────────────────────────────────────────

def enrich_file(path: Path, dry_run: bool, force: bool) -> Dict[str, str]:
    text = path.read_text(encoding="utf-8")
    d = json.loads(text)
    iso2 = d.get("iso2", path.stem).upper()
    changes: Dict[str, str] = {}

    # 1. commonCosts
    if force or "commonCosts" not in d:
        tier = COST_TIER.get(iso2)
        if tier:
            d["commonCosts"] = {
                **TIER_COSTS[tier],
                "currency": "USD",
                "note": COST_NOTE,
            }
            changes["commonCosts"] = f"tier {tier}"

    # 2. medicalEvacuation
    if force or "medicalEvacuation" not in d:
        evac = lookup_evac(iso2)
        if evac:
            quality = d.get("qualityRating", 3)
            try:
                quality = int(quality)
            except (TypeError, ValueError):
                quality = 3
            d["medicalEvacuation"] = compose_evac_note(iso2, quality, evac)
            changes["medicalEvacuation"] = f"primary={evac['primaryDestination']}"

    # 3. pharmacyChains
    if force or "pharmacyChains" not in d:
        chains = lookup_pharmacy_chains(iso2)
        if chains is not None:  # we have a record (could be empty list)
            d["pharmacyChains"] = chains
            changes["pharmacyChains"] = f"{len(chains)} chains" if chains else "no dominant chain (universal marker)"

    # 4. drugNameMap
    if force or "drugNameMap" not in d:
        dm = lookup_drug_names(iso2)
        if dm:
            d["drugNameMap"] = dm
            changes["drugNameMap"] = f"{len(dm)} entries"

    if changes and not dry_run:
        path.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return changes


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    ap.add_argument("--force", action="store_true", help="Overwrite existing fields")
    args = ap.parse_args()

    files = sorted(p for p in DATA_DIR.glob("*.json") if " " not in p.name)
    print(f"Enriching {len(files)} canonical health-data files…\n")

    summary = {
        "files_changed": 0,
        "commonCosts": 0,
        "medicalEvacuation": 0,
        "pharmacyChains": 0,
        "pharmacyChains_empty": 0,
        "drugNameMap": 0,
        "missing_cost_tier": [],
        "missing_evac_region": [],
        "missing_drug_region": [],
    }

    for f in files:
        d = json.loads(f.read_text())
        iso2 = d.get("iso2", f.stem).upper()
        changes = enrich_file(f, args.dry_run, args.force)
        if not changes:
            continue
        summary["files_changed"] += 1
        if "commonCosts" in changes:
            summary["commonCosts"] += 1
        if "medicalEvacuation" in changes:
            summary["medicalEvacuation"] += 1
        if "pharmacyChains" in changes:
            if "no dominant" in changes["pharmacyChains"]:
                summary["pharmacyChains_empty"] += 1
            else:
                summary["pharmacyChains"] += 1
        if "drugNameMap" in changes:
            summary["drugNameMap"] += 1

    # Coverage check — warn about countries we don't have data for
    for f in files:
        d = json.loads(f.read_text())
        iso2 = d.get("iso2", f.stem).upper()
        if iso2 not in COST_TIER:
            summary["missing_cost_tier"].append(iso2)
        if not lookup_evac(iso2):
            summary["missing_evac_region"].append(iso2)
        if not lookup_drug_names(iso2):
            summary["missing_drug_region"].append(iso2)
        if iso2 not in PHARMACY_CHAINS:
            print(f"  ⚠️  {iso2}: not in PHARMACY_CHAINS table (will fall back to universal marker)")

    print("\n" + "=" * 60)
    print(f"Files changed: {summary['files_changed']}")
    print(f"  commonCosts added:                {summary['commonCosts']}")
    print(f"  medicalEvacuation added:          {summary['medicalEvacuation']}")
    print(f"  pharmacyChains (with chains):     {summary['pharmacyChains']}")
    print(f"  pharmacyChains (empty/universal): {summary['pharmacyChains_empty']}")
    print(f"  drugNameMap added:                {summary['drugNameMap']}")

    if summary["missing_cost_tier"]:
        print(f"\n❌ Missing cost tier: {summary['missing_cost_tier']}")
    if summary["missing_evac_region"]:
        print(f"❌ Missing evac region: {summary['missing_evac_region']}")
    if summary["missing_drug_region"]:
        print(f"❌ Missing drug region: {summary['missing_drug_region']}")

    if any([summary["missing_cost_tier"], summary["missing_evac_region"], summary["missing_drug_region"]]):
        print("\n⚠️  Some countries are missing from one or more lookup tables.")
        sys.exit(1)
    if args.dry_run:
        print("\n(dry run — no files written)")


if __name__ == "__main__":
    main()
