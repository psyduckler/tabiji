#!/usr/bin/env python3
"""
Generate country hub pages for tabiji.ai — fully data-driven.

Usage:
    python3 scripts/generate_country_hubs.py

Generates:
    - /countries/{slug}/index.html  for each discovered country
    - /countries/index.html         master index of all countries

All content is auto-discovered by scanning the filesystem:
  - Destinations from api/v1/destinations/*.json
  - Scam guides from scams/research/batch*.json
  - Popular picks from api/v1/picks/*.json
  - Compare pages from compare/*/index.html
  - Itineraries from itineraries/*/index.html
  - Alerts from alerts/{slug}/index.html & api/v1/alerts/*.json
  - Health from health/{slug}/index.html
"""

import json
import os
import glob
import re
from datetime import date
from html import escape as _html_escape

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = date.today().isoformat()
YEAR = date.today().year

# ---------------------------------------------------------------------------
# Country registry: name -> (iso2, flag emoji, continent)
# ---------------------------------------------------------------------------

def _iso2_to_flag(code):
    """Convert ISO2 country code to flag emoji."""
    return ''.join(chr(ord(c) + 0x1F1A5) for c in code.upper())

def _build_country_registry():
    """Build the full country registry from api/v1/alerts/*.json files."""
    EUROPE = set('AL,AD,AT,BY,BE,BA,BG,HR,CY,CZ,DK,EE,FI,FR,DE,GR,HU,IS,IE,IT,XK,LV,LI,LT,LU,MT,MD,MC,ME,NL,MK,NO,PL,PT,RO,RS,SK,SI,ES,SE,CH,UA,GB,RU,GL'.split(','))
    ASIA = set('AF,AM,AZ,BH,BD,BT,BN,KH,CN,GE,HK,IN,ID,IR,IQ,IL,JP,JO,KZ,KW,KG,LA,LB,MO,MY,MV,MN,MM,NP,KP,OM,PK,PH,QA,SA,SG,KR,LK,SY,TW,TJ,TH,TL,TR,TM,AE,UZ,VN,YE'.split(','))
    AFRICA = set('DZ,AO,BJ,BW,BF,BI,CV,CM,CF,TD,KM,CG,CD,CI,DJ,EG,GQ,ER,SZ,ET,GA,GM,GH,GN,GW,KE,LS,LR,LY,MG,MW,ML,MR,MU,MA,MZ,NA,NE,NG,RW,ST,SN,SC,SL,SO,ZA,SS,SD,TZ,TG,TN,UG,ZM,ZW'.split(','))
    AMERICAS = set('AG,AR,BS,BB,BZ,BM,BO,BR,CA,KY,CL,CO,CR,CU,DM,DO,EC,SV,GF,GD,GT,GY,HT,HN,JM,MX,MS,NI,PA,PY,PE,PR,KN,LC,VC,SR,TT,TC,US,UY,VE,VI,AI,AW,CW,SX'.split(','))
    OCEANIA = set('AU,FJ,KI,MH,FM,NR,NZ,PW,PG,WS,SB,TO,TV,VU,NC,FP,TK'.split(','))

    def _continent(iso2):
        if iso2 in EUROPE: return 'Europe'
        if iso2 in ASIA: return 'Asia'
        if iso2 in AFRICA: return 'Africa'
        if iso2 in AMERICAS: return 'Americas'
        if iso2 in OCEANIA: return 'Oceania'
        return 'Other'

    registry = {}
    alerts_dir = os.path.join(BASE_DIR, "api", "v1", "alerts")
    if os.path.isdir(alerts_dir):
        for fn in sorted(os.listdir(alerts_dir)):
            if not fn.endswith('.json'):
                continue
            iso2 = fn[:-5].upper()
            fp = os.path.join(alerts_dir, fn)
            try:
                with open(fp) as f:
                    data = json.load(f)
                name = data.get('name', '')
                if name:
                    registry[name] = (iso2, _iso2_to_flag(iso2), _continent(iso2))
            except Exception:
                pass

    # Add entries that don't have alert JSON files but are important
    if "United States" not in registry:
        registry["United States"] = ("US", _iso2_to_flag("US"), "Americas")
    if "Puerto Rico" not in registry:
        registry["Puerto Rico"] = ("PR", _iso2_to_flag("PR"), "Americas")

    return registry

COUNTRY_REGISTRY = _build_country_registry()

# Name used in destinations.json may differ from our canonical name
DEST_COUNTRY_ALIASES = {
    "Czech Republic": "Czechia",
    "Ivory Coast": "Ivory Coast",
    "Cote d'Ivoire": "Ivory Coast",
    "Burma (Myanmar)": "Myanmar",
    "Burma": "Myanmar",
    "Democratic Republic of the Congo": "DR Congo",
    "Swaziland": "Eswatini",
    "East Timor": "Timor-Leste",
    "Sao Tome and Principe": "S\u00e3o Tom\u00e9 and Pr\u00edncipe",
    "Macedonia": "North Macedonia",
    "Curacao": "Cura\u00e7ao",
}

# Reverse: our canonical name -> name(s) that may appear in destinations.json
CANONICAL_TO_DEST_NAMES = {}
for k, v in DEST_COUNTRY_ALIASES.items():
    CANONICAL_TO_DEST_NAMES.setdefault(v, []).append(k)
# Also add identity mappings
for name in COUNTRY_REGISTRY:
    CANONICAL_TO_DEST_NAMES.setdefault(name, []).append(name)

# Slug helpers
def slugify(name):
    """Convert a country name to a URL slug."""
    import unicodedata
    s = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    s = s.lower().strip()
    s = s.replace("'", "").replace("'", "")
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')

# Build slug -> name mapping
SLUG_TO_NAME = {}
for name in COUNTRY_REGISTRY:
    SLUG_TO_NAME[slugify(name)] = name

# ---------------------------------------------------------------------------
# Quick Facts for 66 countries
# ---------------------------------------------------------------------------

QUICK_FACTS = {
    "Japan":                {"capital": "Tokyo",           "currency": "\u00a5 (JPY)",     "language": "Japanese",       "best_time": "Mar\u2013May / Oct\u2013Nov",  "budget": "$$\u2013$$$", "visa": "90-day visa-free for most"},
    "Mexico":               {"capital": "Mexico City",     "currency": "MXN ($)",          "language": "Spanish",        "best_time": "Nov\u2013Apr",                 "budget": "$\u2013$$",   "visa": "180-day visa-free for most"},
    "Italy":                {"capital": "Rome",            "currency": "\u20ac (EUR)",      "language": "Italian",        "best_time": "Apr\u2013Jun / Sep\u2013Oct",  "budget": "$$\u2013$$$", "visa": "90-day Schengen visa-free"},
    "India":                {"capital": "New Delhi",       "currency": "\u20b9 (INR)",      "language": "Hindi / English","best_time": "Oct\u2013Mar",                 "budget": "$",           "visa": "e-Visa required"},
    "United States":        {"capital": "Washington, D.C.","currency": "$ (USD)",           "language": "English",        "best_time": "Year-round",                   "budget": "$$$",         "visa": "ESTA / visa required"},
    "United Kingdom":       {"capital": "London",          "currency": "\u00a3 (GBP)",      "language": "English",        "best_time": "May\u2013Sep",                 "budget": "$$$",         "visa": "6-month visa-free for most"},
    "Turkey":               {"capital": "Ankara",          "currency": "\u20ba (TRY)",      "language": "Turkish",        "best_time": "Apr\u2013Jun / Sep\u2013Nov",  "budget": "$\u2013$$",   "visa": "e-Visa for most"},
    "Brazil":               {"capital": "Bras\u00edlia",   "currency": "R$ (BRL)",          "language": "Portuguese",     "best_time": "Apr\u2013Oct",                 "budget": "$\u2013$$",   "visa": "90-day visa-free for most"},
    "Thailand":             {"capital": "Bangkok",         "currency": "\u0e3f (THB)",      "language": "Thai",           "best_time": "Nov\u2013Mar",                 "budget": "$",           "visa": "60-day visa-free for most"},
    "Vietnam":              {"capital": "Hanoi",           "currency": "\u20ab (VND)",      "language": "Vietnamese",     "best_time": "Feb\u2013Apr / Oct\u2013Dec",  "budget": "$",           "visa": "e-Visa or 45-day visa-free"},
    "Spain":                {"capital": "Madrid",          "currency": "\u20ac (EUR)",      "language": "Spanish",        "best_time": "Apr\u2013Jun / Sep\u2013Oct",  "budget": "$$",          "visa": "90-day Schengen visa-free"},
    "France":               {"capital": "Paris",           "currency": "\u20ac (EUR)",      "language": "French",         "best_time": "May\u2013Sep",                 "budget": "$$\u2013$$$", "visa": "90-day Schengen visa-free"},
    "Germany":              {"capital": "Berlin",          "currency": "\u20ac (EUR)",      "language": "German",         "best_time": "May\u2013Sep",                 "budget": "$$",          "visa": "90-day Schengen visa-free"},
    "Colombia":             {"capital": "Bogot\u00e1",     "currency": "COP ($)",           "language": "Spanish",        "best_time": "Dec\u2013Mar / Jul\u2013Aug",  "budget": "$",           "visa": "90-day visa-free for most"},
    "Poland":               {"capital": "Warsaw",          "currency": "z\u0142 (PLN)",     "language": "Polish",         "best_time": "May\u2013Sep",                 "budget": "$\u2013$$",   "visa": "90-day Schengen visa-free"},
    "Philippines":          {"capital": "Manila",          "currency": "\u20b1 (PHP)",      "language": "Filipino / English","best_time": "Dec\u2013May",               "budget": "$",           "visa": "30-day visa-free for most"},
    "Argentina":            {"capital": "Buenos Aires",    "currency": "ARS ($)",           "language": "Spanish",        "best_time": "Oct\u2013Apr",                 "budget": "$\u2013$$",   "visa": "90-day visa-free for most"},
    "Portugal":             {"capital": "Lisbon",          "currency": "\u20ac (EUR)",      "language": "Portuguese",     "best_time": "Apr\u2013Oct",                 "budget": "$$",          "visa": "90-day Schengen visa-free"},
    "Egypt":                {"capital": "Cairo",           "currency": "E\u00a3 (EGP)",     "language": "Arabic",         "best_time": "Oct\u2013Apr",                 "budget": "$",           "visa": "Visa on arrival for most"},
    "Greece":               {"capital": "Athens",          "currency": "\u20ac (EUR)",      "language": "Greek",          "best_time": "May\u2013Oct",                 "budget": "$$",          "visa": "90-day Schengen visa-free"},
    "South Korea":          {"capital": "Seoul",           "currency": "\u20a9 (KRW)",      "language": "Korean",         "best_time": "Mar\u2013May / Sep\u2013Nov",  "budget": "$$",          "visa": "90-day visa-free for most"},
    "South Africa":         {"capital": "Pretoria",        "currency": "R (ZAR)",           "language": "English / Zulu / Afrikaans","best_time": "May\u2013Sep",       "budget": "$\u2013$$",   "visa": "90-day visa-free for most"},
    "Sri Lanka":            {"capital": "Colombo",         "currency": "Rs (LKR)",          "language": "Sinhala / Tamil","best_time": "Dec\u2013Mar",                  "budget": "$",           "visa": "ETA required"},
    "Tanzania":             {"capital": "Dodoma",          "currency": "TSh (TZS)",         "language": "Swahili / English","best_time": "Jun\u2013Oct",                "budget": "$\u2013$$",   "visa": "Visa on arrival"},
    "Netherlands":          {"capital": "Amsterdam",       "currency": "\u20ac (EUR)",      "language": "Dutch",          "best_time": "Apr\u2013Sep",                 "budget": "$$\u2013$$$", "visa": "90-day Schengen visa-free"},
    "Morocco":              {"capital": "Rabat",           "currency": "MAD (MAD)",         "language": "Arabic / French","best_time": "Mar\u2013May / Sep\u2013Nov",  "budget": "$",           "visa": "90-day visa-free for most"},
    "Nepal":                {"capital": "Kathmandu",       "currency": "Rs (NPR)",          "language": "Nepali",         "best_time": "Oct\u2013Dec / Mar\u2013May",  "budget": "$",           "visa": "Visa on arrival"},
    "Peru":                 {"capital": "Lima",            "currency": "S/ (PEN)",          "language": "Spanish",        "best_time": "May\u2013Oct",                 "budget": "$\u2013$$",   "visa": "90-day visa-free for most"},
    "Malaysia":             {"capital": "Kuala Lumpur",    "currency": "RM (MYR)",          "language": "Malay / English","best_time": "Mar\u2013Oct",                  "budget": "$\u2013$$",   "visa": "90-day visa-free for most"},
    "Canada":               {"capital": "Ottawa",          "currency": "C$ (CAD)",          "language": "English / French","best_time": "Jun\u2013Sep",                 "budget": "$$$",         "visa": "eTA or visa required"},
    "Kenya":                {"capital": "Nairobi",         "currency": "KSh (KES)",         "language": "Swahili / English","best_time": "Jun\u2013Oct",                "budget": "$\u2013$$",   "visa": "eTA required"},
    "Ireland":              {"capital": "Dublin",          "currency": "\u20ac (EUR)",      "language": "English / Irish","best_time": "May\u2013Sep",                  "budget": "$$\u2013$$$", "visa": "90-day visa-free for most"},
    "Hungary":              {"capital": "Budapest",        "currency": "Ft (HUF)",          "language": "Hungarian",      "best_time": "Apr\u2013Jun / Sep\u2013Oct",  "budget": "$\u2013$$",   "visa": "90-day Schengen visa-free"},
    "Australia":            {"capital": "Canberra",        "currency": "A$ (AUD)",          "language": "English",        "best_time": "Sep\u2013Nov / Mar\u2013May",  "budget": "$$$",         "visa": "eVisitor or ETA required"},
    "Cuba":                 {"capital": "Havana",          "currency": "CUP (\u20b1)",      "language": "Spanish",        "best_time": "Nov\u2013Apr",                 "budget": "$",           "visa": "Tourist card required"},
    "Jordan":               {"capital": "Amman",           "currency": "JOD (JD)",          "language": "Arabic",         "best_time": "Mar\u2013May / Sep\u2013Nov",  "budget": "$$",          "visa": "Visa on arrival / Jordan Pass"},
    "Croatia":              {"capital": "Zagreb",          "currency": "\u20ac (EUR)",      "language": "Croatian",       "best_time": "May\u2013Sep",                 "budget": "$$",          "visa": "90-day Schengen visa-free"},
    "Austria":              {"capital": "Vienna",          "currency": "\u20ac (EUR)",      "language": "German",         "best_time": "Apr\u2013Oct",                 "budget": "$$\u2013$$$", "visa": "90-day Schengen visa-free"},
    "Iceland":              {"capital": "Reykjav\u00edk",  "currency": "kr (ISK)",          "language": "Icelandic",      "best_time": "Jun\u2013Aug",                 "budget": "$$$",         "visa": "90-day Schengen visa-free"},
    "Belgium":              {"capital": "Brussels",        "currency": "\u20ac (EUR)",      "language": "Dutch / French / German","best_time": "May\u2013Sep",          "budget": "$$",          "visa": "90-day Schengen visa-free"},
    "Israel":               {"capital": "Jerusalem",       "currency": "\u20aa (ILS)",      "language": "Hebrew / Arabic","best_time": "Mar\u2013May / Sep\u2013Nov",  "budget": "$$$",         "visa": "90-day visa-free for most"},
    "Cambodia":             {"capital": "Phnom Penh",      "currency": "$ / \u17db (KHR)",  "language": "Khmer",          "best_time": "Nov\u2013Apr",                 "budget": "$",           "visa": "Visa on arrival / e-Visa"},
    "China":                {"capital": "Beijing",         "currency": "\u00a5 (CNY)",      "language": "Mandarin",       "best_time": "Apr\u2013May / Sep\u2013Oct",  "budget": "$\u2013$$",   "visa": "Visa required (some transit exemptions)"},
    "Indonesia":            {"capital": "Jakarta",         "currency": "Rp (IDR)",          "language": "Indonesian",     "best_time": "Apr\u2013Oct",                 "budget": "$",           "visa": "30-day visa on arrival"},
    "Sweden":               {"capital": "Stockholm",       "currency": "kr (SEK)",          "language": "Swedish",        "best_time": "Jun\u2013Aug",                 "budget": "$$$",         "visa": "90-day Schengen visa-free"},
    "Romania":              {"capital": "Bucharest",       "currency": "lei (RON)",         "language": "Romanian",       "best_time": "May\u2013Sep",                 "budget": "$",           "visa": "90-day Schengen visa-free"},
    "Chile":                {"capital": "Santiago",        "currency": "CLP ($)",           "language": "Spanish",        "best_time": "Oct\u2013Mar",                 "budget": "$$",          "visa": "90-day visa-free for most"},
    "Norway":               {"capital": "Oslo",            "currency": "kr (NOK)",          "language": "Norwegian",      "best_time": "Jun\u2013Aug",                 "budget": "$$$",         "visa": "90-day Schengen visa-free"},
    "Switzerland":          {"capital": "Bern",            "currency": "CHF (Fr.)",         "language": "German / French / Italian","best_time": "Jun\u2013Sep / Dec\u2013Mar","budget": "$$$", "visa": "90-day Schengen visa-free"},
    "Taiwan":               {"capital": "Taipei",          "currency": "NT$ (TWD)",         "language": "Mandarin",       "best_time": "Oct\u2013Apr",                 "budget": "$$",          "visa": "90-day visa-free for most"},
    "Bulgaria":             {"capital": "Sofia",           "currency": "\u043b\u0432 (BGN)","language": "Bulgarian",      "best_time": "May\u2013Sep",                 "budget": "$",           "visa": "90-day Schengen visa-free"},
    "Denmark":              {"capital": "Copenhagen",      "currency": "kr (DKK)",          "language": "Danish",         "best_time": "May\u2013Sep",                 "budget": "$$$",         "visa": "90-day Schengen visa-free"},
    "Serbia":               {"capital": "Belgrade",        "currency": "RSD (din.)",        "language": "Serbian",        "best_time": "May\u2013Sep",                 "budget": "$",           "visa": "90-day visa-free for most"},
    "Montenegro":           {"capital": "Podgorica",       "currency": "\u20ac (EUR)",      "language": "Montenegrin",    "best_time": "May\u2013Sep",                 "budget": "$\u2013$$",   "visa": "90-day visa-free for most"},
    "United Arab Emirates": {"capital": "Abu Dhabi",       "currency": "AED (Dh)",          "language": "Arabic / English","best_time": "Nov\u2013Mar",                "budget": "$$\u2013$$$", "visa": "30-day visa on arrival for most"},
    "Ghana":                {"capital": "Accra",           "currency": "GH\u20b5 (GHS)",    "language": "English",        "best_time": "Nov\u2013Mar",                 "budget": "$",           "visa": "Visa required for most"},
    "Dominican Republic":   {"capital": "Santo Domingo",   "currency": "RD$ (DOP)",         "language": "Spanish",        "best_time": "Dec\u2013Apr",                 "budget": "$\u2013$$",   "visa": "30-day tourist card on arrival"},
    "New Zealand":          {"capital": "Wellington",      "currency": "NZ$ (NZD)",         "language": "English / M\u0101ori","best_time": "Dec\u2013Feb",              "budget": "$$\u2013$$$", "visa": "NZeTA required"},
    "Laos":                 {"capital": "Vientiane",       "currency": "\u20ad (LAK)",      "language": "Lao",            "best_time": "Nov\u2013Feb",                 "budget": "$",           "visa": "Visa on arrival for most"},
    "Puerto Rico":          {"capital": "San Juan",        "currency": "$ (USD)",           "language": "Spanish / English","best_time": "Dec\u2013Apr",                "budget": "$$",          "visa": "No visa needed (U.S. territory)"},
    "Costa Rica":           {"capital": "San Jos\u00e9",   "currency": "\u20a1 (CRC)",      "language": "Spanish",        "best_time": "Dec\u2013Apr",                 "budget": "$\u2013$$",   "visa": "90-day visa-free for most"},
    "Panama":               {"capital": "Panama City",     "currency": "B/. / $ (PAB/USD)", "language": "Spanish",        "best_time": "Dec\u2013Apr",                 "budget": "$\u2013$$",   "visa": "90-day visa-free for most"},
    "Estonia":              {"capital": "Tallinn",         "currency": "\u20ac (EUR)",      "language": "Estonian",       "best_time": "Jun\u2013Aug",                 "budget": "$$",          "visa": "90-day Schengen visa-free"},
    "Honduras":             {"capital": "Tegucigalpa",     "currency": "L (HNL)",           "language": "Spanish",        "best_time": "Dec\u2013Apr",                 "budget": "$",           "visa": "90-day visa-free for most"},
    "Jamaica":              {"capital": "Kingston",        "currency": "J$ (JMD)",          "language": "English",        "best_time": "Nov\u2013Apr",                 "budget": "$$",          "visa": "90-day visa-free for most"},
    "Mauritius":            {"capital": "Port Louis",      "currency": "Rs (MUR)",          "language": "English / French / Creole","best_time": "May\u2013Dec",        "budget": "$$",          "visa": "60-day visa-free for most"},
    "El Salvador":          {"capital": "San Salvador",    "currency": "$ (USD)",           "language": "Spanish",        "best_time": "Nov\u2013Apr",                 "budget": "$",           "visa": "90-day visa-free for most"},
    # --- Additional countries (alphabetical) ---
    "Afghanistan":          {"capital": "Kabul",           "currency": "AFN (\u060b)",      "language": "Pashto / Dari",  "best_time": "Apr\u2013Jun / Sep\u2013Nov"},
    "Albania":              {"capital": "Tirana",          "currency": "ALL (Lek)",         "language": "Albanian",       "best_time": "May\u2013Sep",                 "budget": "$",           "visa": "90-day visa-free for most"},
    "Algeria":              {"capital": "Algiers",         "currency": "DZD (DA)",          "language": "Arabic / French","best_time": "Mar\u2013May / Sep\u2013Nov",  "budget": "$"},
    "Andorra":              {"capital": "Andorra la Vella","currency": "\u20ac (EUR)",      "language": "Catalan",        "best_time": "Jun\u2013Sep / Dec\u2013Mar",  "budget": "$$$",         "visa": "90-day visa-free for most"},
    "Angola":               {"capital": "Luanda",          "currency": "AOA (Kz)",          "language": "Portuguese",     "best_time": "May\u2013Oct",                 "budget": "$$"},
    "Antigua and Barbuda":  {"capital": "St. John's",      "currency": "XCD (EC$)",         "language": "English",        "best_time": "Dec\u2013Apr",                 "budget": "$$\u2013$$$"},
    "Armenia":              {"capital": "Yerevan",         "currency": "AMD (\u058f)",      "language": "Armenian",       "best_time": "May\u2013Oct",                 "budget": "$",           "visa": "180-day visa-free for most"},
    "Azerbaijan":           {"capital": "Baku",            "currency": "AZN (\u20bc)",      "language": "Azerbaijani",    "best_time": "Apr\u2013Jun / Sep\u2013Oct",  "budget": "$\u2013$$"},
    "Bahamas":              {"capital": "Nassau",          "currency": "BSD ($)",           "language": "English",        "best_time": "Dec\u2013Apr",                 "budget": "$$$"},
    "Bahrain":              {"capital": "Manama",          "currency": "BHD (BD)",          "language": "Arabic",         "best_time": "Nov\u2013Mar",                 "budget": "$$\u2013$$$"},
    "Bangladesh":           {"capital": "Dhaka",           "currency": "BDT (\u09f3)",      "language": "Bengali",        "best_time": "Nov\u2013Feb",                 "budget": "$"},
    "Barbados":             {"capital": "Bridgetown",      "currency": "BBD ($)",           "language": "English",        "best_time": "Dec\u2013Apr",                 "budget": "$$\u2013$$$"},
    "Belarus":              {"capital": "Minsk",           "currency": "BYN (Br)",          "language": "Belarusian / Russian","best_time": "May\u2013Sep",              "budget": "$"},
    "Belize":               {"capital": "Belmopan",        "currency": "BZD ($)",           "language": "English",        "best_time": "Nov\u2013Apr",                 "budget": "$\u2013$$"},
    "Benin":                {"capital": "Porto-Novo",      "currency": "XOF (CFA)",         "language": "French",         "best_time": "Nov\u2013Feb",                 "budget": "$"},
    "Bhutan":               {"capital": "Thimphu",         "currency": "BTN (Nu)",          "language": "Dzongkha",       "best_time": "Mar\u2013May / Sep\u2013Nov",  "budget": "$$$"},
    "Bolivia":              {"capital": "Sucre / La Paz",  "currency": "BOB (Bs)",          "language": "Spanish",        "best_time": "May\u2013Oct",                 "budget": "$",           "visa": "90-day visa-free for most"},
    "Bosnia and Herzegovina": {"capital": "Sarajevo",      "currency": "BAM (KM)",          "language": "Bosnian / Croatian / Serbian","best_time": "May\u2013Sep",      "budget": "$",           "visa": "90-day visa-free for most"},
    "Botswana":             {"capital": "Gaborone",        "currency": "BWP (P)",           "language": "English / Tswana","best_time": "May\u2013Oct",                 "budget": "$$\u2013$$$"},
    "Brunei":               {"capital": "Bandar Seri Begawan","currency": "BND ($)",         "language": "Malay",          "best_time": "Feb\u2013Oct",                 "budget": "$$"},
    "Burkina Faso":         {"capital": "Ouagadougou",     "currency": "XOF (CFA)",         "language": "French",         "best_time": "Nov\u2013Feb",                 "budget": "$"},
    "Burundi":              {"capital": "Gitega",          "currency": "BIF (FBu)",         "language": "Kirundi / French","best_time": "Jun\u2013Sep",                 "budget": "$"},
    "Cambodia":             {"capital": "Phnom Penh",      "currency": "$ / \u17db (KHR)",  "language": "Khmer",          "best_time": "Nov\u2013Apr",                 "budget": "$",           "visa": "Visa on arrival / e-Visa"},
    "Cameroon":             {"capital": "Yaound\u00e9",    "currency": "XAF (CFA)",         "language": "French / English","best_time": "Nov\u2013Feb",                 "budget": "$"},
    "Cape Verde":           {"capital": "Praia",           "currency": "CVE (Esc)",         "language": "Portuguese / Creole","best_time": "Nov\u2013Jun",               "budget": "$$"},
    "Central African Republic": {"capital": "Bangui",      "currency": "XAF (CFA)",         "language": "French / Sango"},
    "Chad":                 {"capital": "N'Djamena",       "currency": "XAF (CFA)",         "language": "French / Arabic"},
    "Comoros":              {"capital": "Moroni",          "currency": "KMF (CF)",          "language": "Comorian / French / Arabic","best_time": "May\u2013Nov",         "budget": "$"},
    "Republic of the Congo": {"capital": "Brazzaville",   "currency": "XAF (CFA)",         "language": "French"},
    "DR Congo":             {"capital": "Kinshasa",        "currency": "CDF (FC)",          "language": "French"},
    "Cura\u00e7ao":         {"capital": "Willemstad",      "currency": "ANG (\u0192)",      "language": "Dutch / Papiamentu","best_time": "Jan\u2013Sep",                "budget": "$$"},
    "Cyprus":               {"capital": "Nicosia",         "currency": "\u20ac (EUR)",      "language": "Greek / Turkish","best_time": "Apr\u2013Oct",                  "budget": "$$",          "visa": "90-day visa-free for most"},
    "Czechia":              {"capital": "Prague",          "currency": "CZK (K\u010d)",     "language": "Czech",          "best_time": "Apr\u2013Jun / Sep\u2013Oct",  "budget": "$\u2013$$",   "visa": "90-day Schengen visa-free"},
    "Djibouti":             {"capital": "Djibouti",        "currency": "DJF (Fdj)",         "language": "French / Arabic"},
    "Dominica":             {"capital": "Roseau",          "currency": "XCD (EC$)",         "language": "English",        "best_time": "Nov\u2013Apr",                 "budget": "$$"},
    "Ecuador":              {"capital": "Quito",           "currency": "$ (USD)",           "language": "Spanish",        "best_time": "Jun\u2013Sep",                 "budget": "$",           "visa": "90-day visa-free for most"},
    "Equatorial Guinea":    {"capital": "Malabo",          "currency": "XAF (CFA)",         "language": "Spanish / French"},
    "Eritrea":              {"capital": "Asmara",          "currency": "ERN (Nfk)",         "language": "Tigrinya / Arabic"},
    "Eswatini":             {"capital": "Mbabane",         "currency": "SZL (E / L)",       "language": "English / Swazi","best_time": "May\u2013Sep",                  "budget": "$"},
    "Ethiopia":             {"capital": "Addis Ababa",     "currency": "ETB (Br)",          "language": "Amharic",        "best_time": "Oct\u2013Mar",                 "budget": "$"},
    "Fiji":                 {"capital": "Suva",            "currency": "FJD ($)",           "language": "English / Fijian","best_time": "May\u2013Oct",                  "budget": "$$"},
    "Finland":              {"capital": "Helsinki",        "currency": "\u20ac (EUR)",      "language": "Finnish / Swedish","best_time": "Jun\u2013Aug / Dec\u2013Mar", "budget": "$$$",         "visa": "90-day Schengen visa-free"},
    "French Polynesia":     {"capital": "Papeete",         "currency": "XPF (CFP)",         "language": "French / Tahitian","best_time": "May\u2013Oct",                "budget": "$$$"},
    "Gabon":                {"capital": "Libreville",      "currency": "XAF (CFA)",         "language": "French"},
    "Gambia":               {"capital": "Banjul",          "currency": "GMD (D)",           "language": "English",        "best_time": "Nov\u2013May",                 "budget": "$"},
    "Georgia":              {"capital": "Tbilisi",         "currency": "GEL (\u20be)",      "language": "Georgian",       "best_time": "May\u2013Oct",                 "budget": "$",           "visa": "365-day visa-free for most"},
    "Greenland":            {"capital": "Nuuk",            "currency": "DKK (kr)",          "language": "Greenlandic / Danish","best_time": "Jun\u2013Sep",              "budget": "$$$"},
    "Grenada":              {"capital": "St. George's",    "currency": "XCD (EC$)",         "language": "English",        "best_time": "Dec\u2013Apr",                 "budget": "$$"},
    "Guatemala":            {"capital": "Guatemala City",  "currency": "GTQ (Q)",           "language": "Spanish",        "best_time": "Nov\u2013Apr",                 "budget": "$"},
    "Guinea":               {"capital": "Conakry",         "currency": "GNF (FG)",          "language": "French"},
    "Guinea-Bissau":        {"capital": "Bissau",          "currency": "XOF (CFA)",         "language": "Portuguese"},
    "Guyana":               {"capital": "Georgetown",      "currency": "GYD ($)",           "language": "English",        "best_time": "Feb\u2013Apr / Sep\u2013Nov"},
    "Haiti":                {"capital": "Port-au-Prince",  "currency": "HTG (G)",           "language": "Haitian Creole / French"},
    "Hong Kong":            {"capital": "Hong Kong (SAR)", "currency": "HKD ($)",           "language": "Cantonese / English","best_time": "Oct\u2013Dec",               "budget": "$$\u2013$$$", "visa": "90-day visa-free for most"},
    "Iran":                 {"capital": "Tehran",          "currency": "IRR (\ufdfc)",      "language": "Persian (Farsi)"},
    "Iraq":                 {"capital": "Baghdad",         "currency": "IQD (\u0639.\u062f)","language": "Arabic / Kurdish"},
    "Ivory Coast":          {"capital": "Yamoussoukro",    "currency": "XOF (CFA)",         "language": "French",         "best_time": "Nov\u2013Mar",                 "budget": "$"},
    "Kazakhstan":           {"capital": "Astana",          "currency": "KZT (\u20b8)",      "language": "Kazakh / Russian","best_time": "Apr\u2013Jun / Sep\u2013Oct",  "budget": "$",           "visa": "30-day visa-free for most"},
    "Kiribati":             {"capital": "Tarawa",          "currency": "AUD (A$)",          "language": "Gilbertese / English"},
    "Kosovo":               {"capital": "Pristina",        "currency": "\u20ac (EUR)",      "language": "Albanian / Serbian","best_time": "May\u2013Sep",                "budget": "$"},
    "Kuwait":               {"capital": "Kuwait City",     "currency": "KWD (KD)",          "language": "Arabic",         "best_time": "Nov\u2013Mar",                 "budget": "$$\u2013$$$"},
    "Kyrgyzstan":           {"capital": "Bishkek",         "currency": "KGS (som)",         "language": "Kyrgyz / Russian","best_time": "Jun\u2013Sep",                  "budget": "$"},
    "Latvia":               {"capital": "Riga",            "currency": "\u20ac (EUR)",      "language": "Latvian",        "best_time": "May\u2013Sep",                 "budget": "$\u2013$$",   "visa": "90-day Schengen visa-free"},
    "Lebanon":              {"capital": "Beirut",          "currency": "LBP (LL)",          "language": "Arabic / French"},
    "Lesotho":              {"capital": "Maseru",          "currency": "LSL (L / M)",       "language": "Sesotho / English"},
    "Liberia":              {"capital": "Monrovia",        "currency": "LRD ($)",           "language": "English"},
    "Libya":                {"capital": "Tripoli",         "currency": "LYD (LD)",          "language": "Arabic"},
    "Liechtenstein":        {"capital": "Vaduz",           "currency": "CHF (Fr.)",         "language": "German",         "best_time": "Jun\u2013Sep / Dec\u2013Mar",  "budget": "$$$",         "visa": "90-day Schengen visa-free"},
    "Lithuania":            {"capital": "Vilnius",         "currency": "\u20ac (EUR)",      "language": "Lithuanian",     "best_time": "May\u2013Sep",                 "budget": "$\u2013$$",   "visa": "90-day Schengen visa-free"},
    "Luxembourg":           {"capital": "Luxembourg City", "currency": "\u20ac (EUR)",      "language": "Luxembourgish / French / German","best_time": "May\u2013Sep",    "budget": "$$$",         "visa": "90-day Schengen visa-free"},
    "Macau":                {"capital": "Macau (SAR)",     "currency": "MOP ($)",           "language": "Cantonese / Portuguese","best_time": "Oct\u2013Dec",             "budget": "$$\u2013$$$"},
    "Madagascar":           {"capital": "Antananarivo",    "currency": "MGA (Ar)",          "language": "Malagasy / French","best_time": "Apr\u2013Nov",                 "budget": "$"},
    "Malawi":               {"capital": "Lilongwe",        "currency": "MWK (MK)",          "language": "English / Chewa","best_time": "May\u2013Oct",                  "budget": "$"},
    "Maldives":             {"capital": "Mal\u00e9",       "currency": "MVR (Rf)",          "language": "Dhivehi",        "best_time": "Nov\u2013Apr",                 "budget": "$$$",         "visa": "30-day visa on arrival"},
    "Mali":                 {"capital": "Bamako",          "currency": "XOF (CFA)",         "language": "French / Bambara"},
    "Malta":                {"capital": "Valletta",        "currency": "\u20ac (EUR)",      "language": "Maltese / English","best_time": "Apr\u2013Jun / Sep\u2013Nov", "budget": "$$",          "visa": "90-day Schengen visa-free"},
    "Mauritania":           {"capital": "Nouakchott",      "currency": "MRU (UM)",          "language": "Arabic / French"},
    "Micronesia":           {"capital": "Palikir",         "currency": "$ (USD)",           "language": "English"},
    "Moldova":              {"capital": "Chi\u0219in\u0103u","currency": "MDL (lei)",       "language": "Romanian",       "best_time": "May\u2013Sep",                 "budget": "$"},
    "Monaco":               {"capital": "Monaco",          "currency": "\u20ac (EUR)",      "language": "French",         "best_time": "May\u2013Sep",                 "budget": "$$$"},
    "Mongolia":             {"capital": "Ulaanbaatar",     "currency": "MNT (\u20ae)",      "language": "Mongolian",      "best_time": "Jun\u2013Sep",                 "budget": "$"},
    "Mozambique":           {"capital": "Maputo",          "currency": "MZN (MT)",          "language": "Portuguese",     "best_time": "May\u2013Nov",                 "budget": "$"},
    "Myanmar":              {"capital": "Naypyidaw",       "currency": "MMK (Ks)",          "language": "Burmese"},
    "Namibia":              {"capital": "Windhoek",        "currency": "NAD ($)",           "language": "English",        "best_time": "May\u2013Oct",                 "budget": "$\u2013$$"},
    "Nicaragua":            {"capital": "Managua",         "currency": "NIO (C$)",          "language": "Spanish",        "best_time": "Nov\u2013Apr",                 "budget": "$"},
    "Niger":                {"capital": "Niamey",          "currency": "XOF (CFA)",         "language": "French"},
    "Nigeria":              {"capital": "Abuja",           "currency": "NGN (\u20a6)",      "language": "English",        "best_time": "Nov\u2013Feb",                 "budget": "$"},
    "North Korea":          {"capital": "Pyongyang",       "currency": "KPW (\u20a9)",      "language": "Korean"},
    "North Macedonia":      {"capital": "Skopje",          "currency": "MKD (den)",         "language": "Macedonian / Albanian","best_time": "May\u2013Sep",             "budget": "$"},
    "Oman":                 {"capital": "Muscat",          "currency": "OMR (RO)",          "language": "Arabic",         "best_time": "Oct\u2013Mar",                 "budget": "$$\u2013$$$"},
    "Pakistan":             {"capital": "Islamabad",       "currency": "PKR (Rs)",          "language": "Urdu / English"},
    "Palau":                {"capital": "Ngerulmud",       "currency": "$ (USD)",           "language": "Palauan / English","best_time": "Nov\u2013Apr",                "budget": "$$\u2013$$$"},
    "Papua New Guinea":     {"capital": "Port Moresby",    "currency": "PGK (K)",           "language": "English / Tok Pisin"},
    "Paraguay":             {"capital": "Asunci\u00f3n",   "currency": "PYG (\u20b2)",      "language": "Spanish / Guaran\u00ed","best_time": "May\u2013Sep",            "budget": "$"},
    "Qatar":                {"capital": "Doha",            "currency": "QAR (QR)",          "language": "Arabic",         "best_time": "Nov\u2013Mar",                 "budget": "$$$"},
    "Russia":               {"capital": "Moscow",          "currency": "RUB (\u20bd)",      "language": "Russian"},
    "Rwanda":               {"capital": "Kigali",          "currency": "RWF (RF)",          "language": "Kinyarwanda / French / English","best_time": "Jun\u2013Sep",     "budget": "$\u2013$$"},
    "Saint Kitts and Nevis": {"capital": "Basseterre",     "currency": "XCD (EC$)",         "language": "English",        "best_time": "Dec\u2013Apr",                 "budget": "$$\u2013$$$"},
    "Saint Lucia":          {"capital": "Castries",        "currency": "XCD (EC$)",         "language": "English",        "best_time": "Dec\u2013Apr",                 "budget": "$$\u2013$$$"},
    "Saint Vincent and the Grenadines": {"capital": "Kingstown","currency": "XCD (EC$)",     "language": "English",        "best_time": "Dec\u2013May",                 "budget": "$$"},
    "Samoa":                {"capital": "Apia",            "currency": "WST (T)",           "language": "Samoan / English","best_time": "May\u2013Oct"},
    "Saudi Arabia":         {"capital": "Riyadh",          "currency": "SAR (SR)",          "language": "Arabic",         "best_time": "Nov\u2013Feb",                 "budget": "$$\u2013$$$"},
    "Senegal":              {"capital": "Dakar",           "currency": "XOF (CFA)",         "language": "French / Wolof", "best_time": "Nov\u2013May",                 "budget": "$"},
    "Seychelles":           {"capital": "Victoria",        "currency": "SCR (Rs)",          "language": "Creole / English / French","best_time": "Apr\u2013May / Oct\u2013Nov","budget": "$$$"},
    "Sierra Leone":         {"capital": "Freetown",        "currency": "SLE (Le)",          "language": "English"},
    "Singapore":            {"capital": "Singapore",       "currency": "SGD ($)",           "language": "English / Malay / Mandarin / Tamil","best_time": "Feb\u2013Apr", "budget": "$$$",         "visa": "90-day visa-free for most"},
    "Slovakia":             {"capital": "Bratislava",      "currency": "\u20ac (EUR)",      "language": "Slovak",         "best_time": "May\u2013Sep",                 "budget": "$\u2013$$",   "visa": "90-day Schengen visa-free"},
    "Slovenia":             {"capital": "Ljubljana",       "currency": "\u20ac (EUR)",      "language": "Slovenian",      "best_time": "May\u2013Sep",                 "budget": "$$",          "visa": "90-day Schengen visa-free"},
    "Solomon Islands":      {"capital": "Honiara",         "currency": "SBD ($)",           "language": "English"},
    "Somalia":              {"capital": "Mogadishu",       "currency": "SOS (Sh)",          "language": "Somali / Arabic"},
    "South Sudan":          {"capital": "Juba",            "currency": "SSP (\u00a3)",      "language": "English / Arabic"},
    "Sudan":                {"capital": "Khartoum",        "currency": "SDG (LS)",          "language": "Arabic / English"},
    "Suriname":             {"capital": "Paramaribo",      "currency": "SRD ($)",           "language": "Dutch",          "best_time": "Feb\u2013Apr / Aug\u2013Nov",  "budget": "$\u2013$$"},
    "Syria":                {"capital": "Damascus",        "currency": "SYP (\u00a3S)",     "language": "Arabic"},
    "S\u00e3o Tom\u00e9 and Pr\u00edncipe": {"capital": "S\u00e3o Tom\u00e9","currency": "STN (Db)",  "language": "Portuguese"},
    "Tajikistan":           {"capital": "Dushanbe",        "currency": "TJS (SM)",          "language": "Tajik / Russian","best_time": "Apr\u2013Jun / Sep\u2013Oct"},
    "Timor-Leste":          {"capital": "Dili",            "currency": "$ (USD)",           "language": "Tetum / Portuguese"},
    "Togo":                 {"capital": "Lom\u00e9",       "currency": "XOF (CFA)",         "language": "French",         "best_time": "Nov\u2013Feb",                 "budget": "$"},
    "Tonga":                {"capital": "Nuku\u02bbalofa", "currency": "TOP (T$)",          "language": "Tongan / English","best_time": "May\u2013Oct"},
    "Trinidad and Tobago":  {"capital": "Port of Spain",   "currency": "TTD ($)",           "language": "English",        "best_time": "Jan\u2013May",                 "budget": "$$"},
    "Tunisia":              {"capital": "Tunis",           "currency": "TND (DT)",          "language": "Arabic / French","best_time": "Mar\u2013May / Sep\u2013Nov",  "budget": "$"},
    "Turkmenistan":         {"capital": "Ashgabat",        "currency": "TMT (T)",           "language": "Turkmen"},
    "Uganda":               {"capital": "Kampala",         "currency": "UGX (USh)",         "language": "English / Swahili","best_time": "Jun\u2013Sep / Dec\u2013Feb", "budget": "$"},
    "Ukraine":              {"capital": "Kyiv",            "currency": "UAH (\u20b4)",      "language": "Ukrainian"},
    "Uruguay":              {"capital": "Montevideo",      "currency": "UYU ($U)",          "language": "Spanish",        "best_time": "Dec\u2013Mar",                 "budget": "$$"},
    "Uzbekistan":           {"capital": "Tashkent",        "currency": "UZS (so\u2018m)",   "language": "Uzbek / Russian","best_time": "Mar\u2013May / Sep\u2013Nov",  "budget": "$",           "visa": "30-day visa-free for most"},
    "Vanuatu":              {"capital": "Port Vila",       "currency": "VUV (VT)",          "language": "Bislama / English / French","best_time": "Apr\u2013Oct"},
    "Venezuela":            {"capital": "Caracas",         "currency": "VES (Bs.S)",        "language": "Spanish"},
    "Yemen":                {"capital": "Sana'a",          "currency": "YER (\ufdfc)",      "language": "Arabic"},
    "Zambia":               {"capital": "Lusaka",          "currency": "ZMW (ZK)",          "language": "English",        "best_time": "May\u2013Oct",                 "budget": "$\u2013$$"},
    "Zimbabwe":             {"capital": "Harare",          "currency": "ZiG / $ (USD)",     "language": "English / Shona / Ndebele","best_time": "May\u2013Oct",         "budget": "$\u2013$$"},
}

# Health slug overrides (when health directory slug differs from country slug)
HEALTH_SLUG_OVERRIDES = {
    "United Arab Emirates": "uae",
    "Indonesia":            "indonesia-bali",
}

# ---------------------------------------------------------------------------
# Advisory data — dynamically loaded from api/v1/alerts/*.json
# ---------------------------------------------------------------------------

def _build_advisory_data():
    """Build advisory data from alert JSON files + hardcoded overrides."""
    data = {}
    alerts_dir = os.path.join(BASE_DIR, "api", "v1", "alerts")

    # Alert slug overrides (when the alerts/ page slug differs from the country slug)
    _ALERT_SLUG_OVERRIDES = {
        "Mexico": "mexico-travel-advisory",
        "Myanmar": "burma-myanmar",
    }

    if os.path.isdir(alerts_dir):
        for fn in sorted(os.listdir(alerts_dir)):
            if not fn.endswith('.json'):
                continue
            fp = os.path.join(alerts_dir, fn)
            try:
                with open(fp) as f:
                    jdata = json.load(fp=f)
                name = jdata.get('name', '')
                us = jdata.get('us', {})
                level = us.get('level', 0)
                lt = us.get('levelText', '')
                if name and level > 0:
                    alert_slug = _ALERT_SLUG_OVERRIDES.get(name, slugify(name))
                    data[name] = {"level": level, "slug": alert_slug, "lt": lt}
            except Exception:
                pass

    # Hardcoded entries for countries without alert JSON or with special names
    _HARDCODED = {
        "United States": {"level": 1, "slug": "united-states", "lt": "Exercise Normal Precautions"},
        "Puerto Rico": {"level": 1, "slug": "puerto-rico", "lt": "Exercise Normal Precautions"},
    }
    for k, v in _HARDCODED.items():
        if k not in data:
            data[k] = v

    return data

ADVISORY_DATA = _build_advisory_data()

# ---------------------------------------------------------------------------
# Data scanning — runs once, caches globally
# ---------------------------------------------------------------------------

_DESTINATIONS_BY_COUNTRY = None
_DEST_DETAILS_CACHE = None
_SCAMS_BY_COUNTRY = None
_SCAM_DIRS_SET = None
_PICKS_BY_COUNTRY = None
_COMPARE_DIRS_SET = None
_ITIN_DIRS = None
_DEST_PAGES_SET = None


def _load_destinations():
    """Load destinations.json and group by country. Also cache per-dest detail."""
    global _DESTINATIONS_BY_COUNTRY, _DEST_DETAILS_CACHE
    if _DESTINATIONS_BY_COUNTRY is not None:
        return
    _DESTINATIONS_BY_COUNTRY = {}
    _DEST_DETAILS_CACHE = {}
    fp = os.path.join(BASE_DIR, "api", "v1", "destinations.json")
    try:
        with open(fp) as f:
            data = json.load(f)
    except Exception:
        return
    for d in data.get("destinations", []):
        country = d.get("country", "")
        _DESTINATIONS_BY_COUNTRY.setdefault(country, []).append(d)
        _DEST_DETAILS_CACHE[d.get("slug", "")] = d


def _load_dest_details(slug):
    """Load individual destination JSON for photo etc."""
    fp = os.path.join(BASE_DIR, "api", "v1", "destinations", f"{slug}.json")
    try:
        with open(fp) as f:
            return json.load(f)
    except Exception:
        return None


def _load_scams():
    """Load scam data from all batch files, grouped by country."""
    global _SCAMS_BY_COUNTRY, _SCAM_DIRS_SET
    if _SCAMS_BY_COUNTRY is not None:
        return

    # Get set of actual scam directories
    scams_dir = os.path.join(BASE_DIR, "scams")
    _SCAM_DIRS_SET = set()
    if os.path.isdir(scams_dir):
        for d in os.listdir(scams_dir):
            if os.path.isdir(os.path.join(scams_dir, d)) and d != "research":
                _SCAM_DIRS_SET.add(d)

    _SCAMS_BY_COUNTRY = {}
    seen = set()  # avoid dups (city, country)

    for pattern in ["scams/research/batch*.json", "scams/research/tier_b_batch*.json", "scams/research/tier_c_batch*.json", "scams/research/tier_d_batch*.json"]:
        for fp in sorted(glob.glob(os.path.join(BASE_DIR, pattern))):
            try:
                with open(fp) as f:
                    data = json.load(f)
                if not isinstance(data, list):
                    continue
                for entry in data:
                    country = entry.get("country", "").strip()
                    city = entry.get("city", "").strip()
                    scam_count = len(entry.get("scams", []))
                    if not country or not city:
                        continue

                    # Derive slug
                    raw_slug = slugify(city)
                    # Check if slug actually exists as a scam directory
                    if raw_slug not in _SCAM_DIRS_SET:
                        continue

                    key = (raw_slug, country)
                    if key in seen:
                        continue
                    seen.add(key)

                    _SCAMS_BY_COUNTRY.setdefault(country, []).append({
                        "city": city,
                        "slug": raw_slug,
                        "count": scam_count,
                    })
            except Exception:
                pass

    # Also check batch_tier_a.json
    tier_a_path = os.path.join(BASE_DIR, "scams", "research", "batch_tier_a.json")
    if os.path.exists(tier_a_path):
        try:
            with open(tier_a_path) as f:
                data = json.load(f)
            if isinstance(data, list):
                for entry in data:
                    country = entry.get("country", "").strip()
                    city = entry.get("city", "").strip()
                    scam_count = len(entry.get("scams", []))
                    if not country or not city:
                        continue
                    raw_slug = slugify(city)
                    if raw_slug not in _SCAM_DIRS_SET:
                        continue
                    key = (raw_slug, country)
                    if key in seen:
                        continue
                    seen.add(key)
                    _SCAMS_BY_COUNTRY.setdefault(country, []).append({
                        "city": city,
                        "slug": raw_slug,
                        "count": scam_count,
                    })
        except Exception:
            pass

    # Map aliases: "Scotland" -> "United Kingdom", "China (SAR)" -> "China" etc
    scam_country_merge = {
        "Scotland": "United Kingdom",
        "China (SAR)": "China",
        "The Bahamas": "Jamaica",  # skip — different country
    }
    for alias, canonical in scam_country_merge.items():
        if alias in _SCAMS_BY_COUNTRY:
            _SCAMS_BY_COUNTRY.setdefault(canonical, []).extend(_SCAMS_BY_COUNTRY.pop(alias))


def _load_picks():
    """Load picks from api/v1/picks/*.json, grouped by country."""
    global _PICKS_BY_COUNTRY
    if _PICKS_BY_COUNTRY is not None:
        return

    _PICKS_BY_COUNTRY = {}
    picks_api_dir = os.path.join(BASE_DIR, "api", "v1", "picks")
    picks_html_dir = os.path.join(BASE_DIR, "popular-picks")

    if not os.path.isdir(picks_api_dir):
        return

    # Build set of country slugs to filter out hub/index picks
    _country_slugs = set(slugify(n) for n in COUNTRY_REGISTRY)

    for fn in sorted(os.listdir(picks_api_dir)):
        if not fn.endswith(".json"):
            continue
        slug = fn[:-5]
        # Skip hub/index picks (e.g., "japan.json" is a country hub, not a city pick)
        if slug in _country_slugs:
            continue
        # Verify the HTML page exists
        if not os.path.isdir(os.path.join(picks_html_dir, slug)):
            continue

        fp = os.path.join(picks_api_dir, fn)
        try:
            with open(fp) as f:
                data = json.load(f)
        except Exception:
            continue

        city = data.get("city", "").strip()
        title = data.get("title", "").strip()
        if not title:
            title = slug.replace("-", " ").title()

        # Determine country from places
        country = ""
        places = data.get("places", [])
        if isinstance(places, list):
            for p in places:
                if isinstance(p, dict) and p.get("country"):
                    country = p["country"]
                    break

        if not country and city:
            # Fallback: look up destination
            _load_destinations()
            city_slug = slugify(city)
            detail = _DEST_DETAILS_CACHE.get(city_slug)
            if detail:
                country = detail.get("country", "")
            else:
                # Try loading individual
                dd = _load_dest_details(city_slug)
                if dd:
                    country = dd.get("country", "")

        if country:
            _PICKS_BY_COUNTRY.setdefault(country, []).append({
                "slug": slug,
                "title": title,
            })


def _load_compare_dirs():
    """Get the set of all compare directory slugs."""
    global _COMPARE_DIRS_SET
    if _COMPARE_DIRS_SET is not None:
        return
    compare_dir = os.path.join(BASE_DIR, "compare")
    _COMPARE_DIRS_SET = set()
    if os.path.isdir(compare_dir):
        for d in os.listdir(compare_dir):
            if os.path.isdir(os.path.join(compare_dir, d)):
                _COMPARE_DIRS_SET.add(d)


def _load_itin_dirs():
    """Get all itinerary directory slugs."""
    global _ITIN_DIRS
    if _ITIN_DIRS is not None:
        return
    itin_dir = os.path.join(BASE_DIR, "itineraries")
    _ITIN_DIRS = set()
    if os.path.isdir(itin_dir):
        for d in os.listdir(itin_dir):
            if os.path.isdir(os.path.join(itin_dir, d)):
                _ITIN_DIRS.add(d)


def _load_dest_pages():
    """Get set of destination slugs that have actual HTML pages."""
    global _DEST_PAGES_SET
    if _DEST_PAGES_SET is not None:
        return
    dest_dir = os.path.join(BASE_DIR, "destinations")
    _DEST_PAGES_SET = set()
    if os.path.isdir(dest_dir):
        for d in os.listdir(dest_dir):
            if os.path.isdir(os.path.join(dest_dir, d)):
                _DEST_PAGES_SET.add(d)


# ---------------------------------------------------------------------------
# Per-country data collectors
# ---------------------------------------------------------------------------

def get_destination_count(country_name):
    """Count destinations for a country."""
    _load_destinations()
    # Check canonical name and aliases
    count = len(_DESTINATIONS_BY_COUNTRY.get(country_name, []))
    # Also check alternate names
    for alt in CANONICAL_TO_DEST_NAMES.get(country_name, []):
        if alt != country_name:
            count += len(_DESTINATIONS_BY_COUNTRY.get(alt, []))
    return count


def get_top_destinations(country_name, limit=12):
    """Get top destinations with photos for a country."""
    _load_destinations()
    _load_dest_pages()
    _load_scams()
    _load_picks()
    _load_compare_dirs()
    _load_itin_dirs()

    # Build a set of "popular" city slugs — cities that appear in other content
    popular_slugs = set()
    # Cities with scam guides
    for scams in (_SCAMS_BY_COUNTRY or {}).values():
        for sc in scams:
            popular_slugs.add(sc.get("slug", ""))
    # Cities with popular picks (extract city slug from pick slug)
    for picks in (_PICKS_BY_COUNTRY or {}).values():
        for pk in picks:
            # Pick slugs often start with city name, e.g. "fukuoka-ramen"
            parts = pk.get("slug", "").split("-")
            if parts:
                popular_slugs.add(parts[0])
    # Cities in comparison slugs
    for entry in (_COMPARE_DIRS_SET or set()):
        for part in entry.split("-vs-"):
            popular_slugs.add(part)
    # Cities in itinerary slugs
    for entry in (_ITIN_DIRS or set()):
        for part in entry.split("-"):
            popular_slugs.add(part)

    # Gather all dests for this country
    dests = list(_DESTINATIONS_BY_COUNTRY.get(country_name, []))
    for alt in CANONICAL_TO_DEST_NAMES.get(country_name, []):
        if alt != country_name:
            dests.extend(_DESTINATIONS_BY_COUNTRY.get(alt, []))

    if not dests:
        return []

    results = []
    for d in dests:
        slug = d.get("slug", "")
        name = d.get("name", "")
        if not slug or not name:
            continue

        # Load individual dest JSON for photo
        detail = _load_dest_details(slug)
        photo = ""
        if detail:
            photo = detail.get("photo", "")

        has_real_photo = photo and "owl-logo" not in photo and "tabiji-owl" not in photo
        has_page = slug in _DEST_PAGES_SET
        is_popular = slug in popular_slugs

        results.append({
            "name": name,
            "slug": slug,
            "photo": photo if has_real_photo else "",
            "has_page": has_page,
            "has_photo": has_real_photo,
            "is_popular": is_popular,
        })

    # Sort: prioritize destinations with pages, popularity signals, then photos
    # Within each tier, popular destinations (referenced in other content) rank higher
    results.sort(key=lambda x: (
        -(x["has_page"] and x["has_photo"]),
        -x["is_popular"],
        -x["has_photo"],
        -x["has_page"],
        x["name"],
    ))

    return results[:limit]


def get_scam_guides(country_name):
    """Get scam guides for a country."""
    _load_scams()
    return _SCAMS_BY_COUNTRY.get(country_name, [])


def get_popular_picks(country_name):
    """Get popular picks for a country."""
    _load_picks()
    return _PICKS_BY_COUNTRY.get(country_name, [])


def get_comparisons(country_name, country_slug):
    """Find compare pages matching this country."""
    _load_compare_dirs()
    _load_destinations()

    # Build list of city slugs for this country
    dests = list(_DESTINATIONS_BY_COUNTRY.get(country_name, []))
    for alt in CANONICAL_TO_DEST_NAMES.get(country_name, []):
        if alt != country_name:
            dests.extend(_DESTINATIONS_BY_COUNTRY.get(alt, []))

    # Get a set of significant city name tokens for matching
    city_slugs = set()
    city_slugs.add(country_slug)
    for d in dests:
        s = d.get("slug", "")
        if s and len(s) > 3:
            city_slugs.add(s)

    matches = []
    seen = set()

    # Build set of country slugs to filter out hub/index pages
    _country_slugs = set(slugify(n) for n in COUNTRY_REGISTRY)

    for entry in sorted(_COMPARE_DIRS_SET):
        if entry in seen:
            continue

        # Skip hub/index pages (e.g., /compare/japan/ is a hub, not a comparison)
        if entry in _country_slugs:
            continue

        # Check vs comparisons
        parts = entry.split("-vs-")
        if len(parts) != 2:
            continue

        matched = False
        for part in parts:
            part_tokens = set(part.split("-"))
            # Match if country slug is in the part OR a significant city slug matches
            if country_slug in part.split("-"):
                matched = True
                break
            # Check city name matches (full slug match to avoid false positives)
            if part in city_slugs:
                matched = True
                break
            # Check country name as part of the slug
            if country_slug in part:
                matched = True
                break

        if matched:
            title = entry.replace("-vs-", " vs ").replace("-", " ").title()
            # Clean up common title issues
            title = title.replace(" Vs ", " vs ")
            matches.append({"slug": entry, "title": title})
            seen.add(entry)

    return matches


def get_itineraries(country_name, country_slug):
    """Find itineraries matching this country."""
    _load_itin_dirs()
    _load_destinations()

    # Build keyword set from country and major cities
    keywords = set()
    keywords.add(country_slug)
    # Add country name words
    for w in country_name.lower().split():
        if len(w) > 2:
            keywords.add(w)

    # Add top city slugs
    dests = list(_DESTINATIONS_BY_COUNTRY.get(country_name, []))
    for alt in CANONICAL_TO_DEST_NAMES.get(country_name, []):
        if alt != country_name:
            dests.extend(_DESTINATIONS_BY_COUNTRY.get(alt, []))

    # Only add well-known cities (those with scam guides or picks)
    _load_scams()
    _load_picks()
    known_cities = set()
    for sc in _SCAMS_BY_COUNTRY.get(country_name, []):
        known_cities.add(sc["slug"])
    for pk in _PICKS_BY_COUNTRY.get(country_name, []):
        # Extract city from pick slug (e.g., "tokyo-brunch" -> "tokyo")
        parts = pk["slug"].split("-")
        if parts:
            known_cities.add(parts[0])

    for city_slug in known_cities:
        if len(city_slug) > 3:
            keywords.add(city_slug)

    matches = []
    for itin_slug in sorted(_ITIN_DIRS):
        itin_lower = itin_slug.lower()
        for kw in keywords:
            if kw in itin_lower.split("-"):
                # Extract title and days from slug
                title = itin_slug.replace("-", " ").title()
                # Try to parse days
                day_match = re.match(r"(\d+)-day", itin_slug)
                days = int(day_match.group(1)) if day_match else 0
                # Shorter title: remove the country name from title if present
                display_title = title
                matches.append({"slug": itin_slug, "title": display_title, "days": days})
                break

    return matches


def has_alert_page(country_slug):
    """Check if an alert page exists for this country."""
    return os.path.exists(os.path.join(BASE_DIR, "alerts", country_slug, "index.html"))


def has_health_page(country_name, country_slug):
    """Check if a health page exists for this country. Return the slug if found."""
    health_slug = HEALTH_SLUG_OVERRIDES.get(country_name, country_slug)
    if os.path.exists(os.path.join(BASE_DIR, "health", health_slug, "index.html")):
        return health_slug
    # Fallback: try the country slug directly
    if health_slug != country_slug and os.path.exists(os.path.join(BASE_DIR, "health", country_slug, "index.html")):
        return country_slug
    return None


def get_advisory(country_name):
    """Get advisory data for a country."""
    return ADVISORY_DATA.get(country_name)


def _is_real_destination_photo(url):
    """Reject placeholder/logo URLs that destinations sometimes use as a fallback."""
    if not url:
        return False
    bad_substrings = (
        "owl-logo",
        "tabiji-owl-logo",
        "/icon-",
        "apple-touch-icon",
        "favicon",
    )
    return not any(b in url for b in bad_substrings)


def _get_country_hero_image(country_name, country_slug):
    """Best-effort hero image for a country card.

    Prefers destinations that have their own page (major cities) over random
    alphabetical ones. The popular-picks-hub-data heroImage field is
    intentionally NOT used — those point at zoomed-in food/venue photos
    that look awful as country thumbnails.
    Returns None if no good source — caller renders a gradient placeholder.
    """
    _load_dest_pages()
    dests = (_DESTINATIONS_BY_COUNTRY or {}).get(country_name) or []
    if not dests:
        for alias, canonical in DEST_COUNTRY_ALIASES.items():
            if canonical == country_name:
                dests = (_DESTINATIONS_BY_COUNTRY or {}).get(alias) or []
                if dests:
                    break

    # Try destinations with their own page first (major cities like Tokyo, Paris)
    for d in dests:
        slug = d.get("slug")
        if not slug or slug not in (_DEST_PAGES_SET or set()):
            continue
        details = (_DEST_DETAILS_CACHE or {}).get(slug) or _load_dest_details(slug)
        if not details:
            continue
        photo = details.get("photo")
        if _is_real_destination_photo(photo):
            return photo

    # Fallback: any destination with a real photo
    for d in dests:
        slug = d.get("slug")
        if not slug:
            continue
        details = (_DEST_DETAILS_CACHE or {}).get(slug) or _load_dest_details(slug)
        if not details:
            continue
        photo = details.get("photo")
        if _is_real_destination_photo(photo):
            return photo

    return None


def extract_alert_content(alert_slug):
    """Extract the full advisory detail content from an alert HTML page."""
    alert_path = os.path.join(BASE_DIR, "alerts", alert_slug, "index.html")
    if not os.path.exists(alert_path):
        return ""
    with open(alert_path) as f:
        html = f.read()

    # Extract the detail-content section
    parts = []

    # 1. Risk tags (if present)
    risk_match = re.search(r'<div class="risk-tags">(.*?)</div>', html, re.DOTALL)
    if risk_match:
        parts.append(f'<div class="risk-tags">{risk_match.group(1)}</div>')

    # 2. Main detail content (US State Dept, UK FCDO, etc.)
    detail_match = re.search(r'<div class="detail-content">(.*?)(?:<p class="updated-text">|<!-- @include:footer)', html, re.DOTALL)
    if detail_match:
        parts.append(detail_match.group(1).strip())

    # 3. Enrichment section (emergency numbers, healthcare, medication, cultural tips, scam guides)
    enrich_match = re.search(r'<div id="alert-enrichment-section">(.*?)</div>\s*<footer', html, re.DOTALL)
    if enrich_match:
        parts.append(enrich_match.group(1).strip())

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------

def h(text):
    """HTML-escape text."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def pl(n, singular, plural=None):
    """Simple pluralization."""
    if plural is None:
        plural = singular + "s"
    return f"{n} {singular}" if n == 1 else f"{n} {plural}"


def nav_html():
    # Marker comments are required so scripts/build-partials.py can keep this
    # block in sync with _includes/nav-main.html across the whole site.
    return """<!-- @include:nav:start -->
<nav>
    <a href="/" class="logo"><img class="owl-default" src="https://img.tabiji.ai/tabiji-owl-logo.png" alt="tabiji.ai" style="height:32px;" loading="lazy"><img class="owl-fly" src="https://img.tabiji.ai/tabiji-owl-logo-flying.png?v=2" alt="" style="height:32px;">tabiji<span>.ai</span></a>
    <button class="hamburger" onclick="document.querySelector('.nav-links').classList.toggle('open')" aria-label="Menu">\u2630</button>
    <div class="nav-links">
        <div class="nav-dropdown">
            <button class="nav-dropdown-toggle" onclick="this.parentElement.classList.toggle('open')">Explore</button>
            <div class="nav-dropdown-menu">
                <a href="/api/">\U0001F50C API</a>
                <a href="/compare/">\U0001F19A Compare Destinations</a>
                <a href="/credit-cards/">\U0001F4B3 Credit Card Benefits</a>
                <a href="/find/">\U0001F50D Destination Finder</a>
                <a href="/resources/">\U0001F4DA Resources</a>
                <a href="/scams/">\U0001F6A8 Tourist Scams</a>
                <a href="/health/">\U0001F3E5 Travel Health Tips</a>
            </div>
        </div>
        <a href="/popular-picks/">Popular Picks</a>
        <a href="/countries/">Country Guides</a>
        <a href="/about/">About</a>
        <a href="/plan" class="cta-nav">Get a Free Itinerary</a>
    </div>
</nav>
<!-- @include:nav:end -->"""


def footer_html():
    return f"""<!-- @include:footer:start -->
<footer>
    <p>\u00a9 {YEAR} tabiji.ai \u00b7 <a href="/terms/" style="color: inherit; text-decoration: underline;">Terms of Service</a> \u00b7 <a href="/privacy/" style="color: inherit; text-decoration: underline;">Privacy Policy</a> \u00b7 <a href="/delete-data/" style="color: inherit; text-decoration: underline;">Delete My Data</a> \u00b7 <a href="https://www.instagram.com/tabiji.ai/" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">Instagram</a> \u00b7 <a href="https://www.youtube.com/@tabijiai" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">YouTube</a> \u00b7 <a href="https://www.pinterest.com/tabijiai/" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">Pinterest</a> \u00b7 <a href="https://x.com/tabijiai" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">X</a> \u00b7 <a href="/media/" style="color: inherit; text-decoration: underline;">Media Studio</a> \u00b7 <a href="/api/" style="color: inherit; text-decoration: underline;">API</a></p>
</footer>
<!-- @include:footer:end -->"""


# ---------------------------------------------------------------------------
# Country page generator
# ---------------------------------------------------------------------------

def generate_country_page(name, slug, iso2, flag, continent):
    """Generate the full HTML for a country hub page."""

    # Gather all data
    dest_count = get_destination_count(name)
    scams = get_scam_guides(name)
    picks = get_popular_picks(name)
    comparisons = get_comparisons(name, slug)
    itineraries = get_itineraries(name, slug)
    top_dests = get_top_destinations(name, limit=12)
    advisory = get_advisory(name)
    health_slug = has_health_page(name, slug)
    facts = QUICK_FACTS.get(name)
    has_alert = has_alert_page(slug)

    scam_count = len(scams)
    compare_count = len(comparisons)
    itin_count = len(itineraries)
    picks_count = len(picks)

    # Build subtitle
    subtitle_parts = []
    if dest_count:
        subtitle_parts.append(pl(dest_count, "destination"))
    if scam_count:
        subtitle_parts.append(pl(scam_count, "scam guide"))
    if compare_count:
        subtitle_parts.append(pl(compare_count, "comparison"))
    if itin_count:
        subtitle_parts.append(pl(itin_count, "itinerary", "itineraries"))
    if picks_count:
        subtitle_parts.append(pl(picks_count, "popular pick"))
    subtitle = " &middot; ".join(subtitle_parts)
    if not subtitle:
        subtitle = continent

    # Build meta description dynamically based on available content
    meta_parts = []
    if dest_count:
        meta_parts.append(f"{dest_count} destinations")
    if scam_count:
        meta_parts.append("scam alerts")
    if health_slug:
        meta_parts.append("health tips")
    if itin_count:
        meta_parts.append("itineraries")
    if picks_count:
        meta_parts.append("curated local picks")
    if advisory:
        meta_parts.append("travel advisory")
    if meta_parts:
        meta_detail = ", ".join(meta_parts)
        meta_desc = (
            f"Your complete {name} travel guide for {YEAR}. "
            f"Explore {meta_detail} \u2014 all backed by real traveler data."
        )
    else:
        meta_desc = (
            f"{name} travel guide for {YEAR}. "
            f"Travel advisory, entry requirements, and safety information."
        )

    # og:image — use a country-specific destination photo for better social sharing
    _load_destinations()
    hero_photo = _get_country_hero_image(name, slug)
    og_image = hero_photo or "https://img.tabiji.ai/tabiji-owl-logo.png"
    twitter_card = "summary_large_image" if hero_photo else "summary"

    # JSON-LD
    breadcrumb_json = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tabiji.ai/"},
                    {"@type": "ListItem", "position": 2, "name": "Countries", "item": "https://tabiji.ai/countries/"},
                    {"@type": "ListItem", "position": 3, "name": name, "item": f"https://tabiji.ai/countries/{slug}/"},
                ],
            },
            {
                "@type": "TouristDestination",
                "name": name,
                "description": meta_desc,
                "url": f"https://tabiji.ai/countries/{slug}/",
                "touristType": "International travelers",
                "containedInPlace": {
                    "@type": "Country",
                    "name": name,
                },
            },
        ]
    }, indent=4)

    # --- Quick Facts ---
    quick_facts_html = ""
    if facts:
        fact_items = ""
        for fkey, flabel in [("capital", "Capital"), ("currency", "Currency"), ("language", "Language"),
                              ("best_time", "Best Time to Visit"), ("budget", "Budget Level"), ("visa", "Visa")]:
            if fkey in facts:
                fact_items += f"""
            <div class="fact-item">
                <div class="fact-label">{flabel}</div>
                <div class="fact-value">{h(facts[fkey])}</div>
            </div>"""
        if fact_items:
            quick_facts_html = f"""
    <section class="section">
        <h2 class="section-title">Quick Facts</h2>
        <div class="facts-grid">{fact_items}
        </div>
    </section>"""

    # --- Travel Advisory ---
    advisory_html = ""
    if advisory:
        alert_slug = advisory.get("slug", slug)
        level = advisory["level"]
        level_colors = {
            1: ("#16A34A", "#F0FDF4"),
            2: ("#F59E0B", "#FFFBEB"),
            3: ("#F97316", "#FFF7ED"),
            4: ("#EF4444", "#FEF2F2"),
        }
        color, bg = level_colors.get(level, ("#16A34A", "#F0FDF4"))
        label = f"Level {level} \u2014 {advisory['lt']}"

        # Try to embed full alert content if the HTML page exists
        alert_exists = has_alert_page(alert_slug) or has_alert
        full_alert = ""
        if alert_exists:
            full_alert = extract_alert_content(alert_slug)
            if not full_alert:
                full_alert = extract_alert_content(slug)

        if full_alert:
            advisory_html = f"""
    <section class="section advisory-full">
        <h2 class="section-title">Travel Advisory</h2>
        <div class="advisory-badge-inline" style="background: {bg}; color: {color};">
            {h(label)}
        </div>
        <div class="alert-detail-content">
            {full_alert}
        </div>
    </section>"""
        else:
            # Always show the advisory badge card even without the full alert page
            advisory_html = f"""
    <section class="section">
        <h2 class="section-title">Travel Advisory</h2>
        <div class="advisory-card" style="border-left: 4px solid {color};">
            <div class="advisory-badge" style="background: {bg}; color: {color};">
                {h(label)}
            </div>
            <p class="advisory-desc">U.S. Department of State advisory level for {name}. Check official sources for the latest entry requirements and safety updates.</p>
        </div>
    </section>"""

    # --- Health ---
    health_html = ""
    if health_slug:
        health_html = f"""
    <section class="section">
        <h2 class="section-title">Health &amp; Safety</h2>
        <div class="health-card">
            <p style="font-size:0.92rem; color:var(--text-muted); line-height:1.55;">
                View vaccination recommendations, tap water safety, and healthcare tips for {name}.
            </p>
            <a href="/health/{health_slug}/" class="section-link">Full health guide for {name} &rarr;</a>
        </div>
    </section>"""

    # --- Scam Guides ---
    scam_html = ""
    if scams:
        scam_cards = ""
        for sc in scams:
            scam_cards += f"""
            <a href="/scams/{sc['slug']}/" class="card">
                <div class="card-body">
                    <h3 class="card-title">{h(sc['city'])}</h3>
                    <p class="card-meta">{sc['count']} scams documented</p>
                </div>
            </a>"""
        scam_html = f"""
    <section class="section">
        <h2 class="section-title">Scam Guides</h2>
        <p class="section-desc">Real tourist scams reported by Reddit travelers. Know what to watch for before you arrive.</p>
        <div class="card-grid">{scam_cards}
        </div>
    </section>"""

    # --- Popular Picks ---
    picks_html = ""
    if picks:
        picks_top = picks[:12]
        picks_cards = ""
        for pk in picks_top:
            picks_cards += f"""
            <a href="/popular-picks/{pk['slug']}/" class="card">
                <div class="card-body">
                    <h3 class="card-title">{h(pk['title'])}</h3>
                </div>
            </a>"""
        picks_view_all = ""
        if picks_count > 12:
            # Link to country-specific picks hub if it exists, otherwise global
            picks_hub = f"/popular-picks/{slug}/"
            if not os.path.isdir(os.path.join(BASE_DIR, "popular-picks", slug)):
                picks_hub = "/popular-picks/"
            picks_view_all = f'\n        <div class="view-all-wrap"><a href="{picks_hub}" class="view-all-link">View all {picks_count} popular picks &rarr;</a></div>'
        picks_html = f"""
    <section class="section">
        <h2 class="section-title">Popular Picks</h2>
        <p class="section-desc">Curated lists of the best restaurants, bars, and experiences \u2014 backed by real reviews.</p>
        <div class="card-grid">{picks_cards}
        </div>{picks_view_all}
    </section>"""

    # --- Compare ---
    compare_html = ""
    if comparisons:
        compare_top = comparisons[:12]
        compare_cards = ""
        for cp in compare_top:
            compare_cards += f"""
            <a href="/compare/{cp['slug']}/" class="card">
                <div class="card-body">
                    <h3 class="card-title">{h(cp['title'])}</h3>
                </div>
            </a>"""
        compare_view_all = ""
        if compare_count > 12:
            # Link to country-specific compare hub if it exists, otherwise global
            compare_hub = f"/compare/{slug}/"
            if not os.path.isdir(os.path.join(BASE_DIR, "compare", slug)):
                compare_hub = "/compare/"
            compare_view_all = f'\n        <div class="view-all-wrap"><a href="{compare_hub}" class="view-all-link">View all {compare_count} comparisons &rarr;</a></div>'
        compare_html = f"""
    <section class="section">
        <h2 class="section-title">Destination Comparisons</h2>
        <p class="section-desc">Side-by-side breakdowns to help you choose the right destination.</p>
        <div class="card-grid">{compare_cards}
        </div>{compare_view_all}
    </section>"""

    # --- Itineraries ---
    itin_html = ""
    if itineraries:
        itin_cards = ""
        for it in itineraries:
            days_meta = f'<p class="card-meta">{it["days"]} days</p>' if it["days"] else ""
            itin_cards += f"""
            <a href="/itineraries/{it['slug']}/" class="card">
                <div class="card-body">
                    <h3 class="card-title">{h(it['title'])}</h3>
                    {days_meta}
                </div>
            </a>"""
        itin_html = f"""
    <section class="section">
        <h2 class="section-title">Sample Itineraries</h2>
        <p class="section-desc">Day-by-day itineraries built from thousands of real traveler recommendations.</p>
        <div class="card-grid">{itin_cards}
        </div>
    </section>"""

    # --- Top Destinations ---
    dest_html = ""
    if top_dests:
        dest_cards = ""
        for td in top_dests:
            photo = td["photo"] if td["has_photo"] else f"https://img.tabiji.ai/find/img/{td['slug']}.webp"
            if td["has_page"]:
                href = f"/destinations/{td['slug']}/"
            else:
                href = f"/plan/?destination={h(td['name'])}"
            dest_cards += f"""
            <a href="{href}" class="dest-card">
                <img src="{h(photo)}" alt="{h(td['name'])}" loading="lazy" width="400" height="260">
                <div class="dest-overlay">
                    <h3>{h(td['name'])}</h3>
                </div>
            </a>"""
        dest_html = f"""
    <section class="section">
        <h2 class="section-title">Top Destinations</h2>
        <div class="dest-grid">{dest_cards}
        </div>
        <div class="view-all-wrap"><a href="/find/" class="view-all-link">Explore all {name} destinations &rarr;</a></div>
    </section>"""

    # --- CTA ---
    cta_html = f"""
    <section class="cta-box">
        <h2>Ready to plan your {name} trip?</h2>
        <p>Get a personalized, day-by-day itinerary built from real traveler recommendations.</p>
        <a href="/plan/?destination={h(name)}" class="cta-btn">Plan My {name} Trip &rarr;</a>
    </section>"""

    # --- Robots: noindex thin pages to protect crawl budget ---
    content_score = scam_count + picks_count + compare_count + itin_count
    robots_content = "index, follow"
    if content_score < 3 and dest_count < 20:
        robots_content = "noindex, follow"

    # --- Full page ---
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://img.tabiji.ai">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-D7QHNRXLHJ"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-D7QHNRXLHJ');
    </script>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="https://img.tabiji.ai/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="192x192" href="https://img.tabiji.ai/icon-192.png">
    <title>{h(name)} Travel Guide {YEAR} | tabiji.ai</title>
    <meta name="description" content="{h(meta_desc)}">
    <meta property="og:title" content="{h(name)} Travel Guide {YEAR} | tabiji.ai">
    <meta property="og:description" content="{h(meta_desc)}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://tabiji.ai/countries/{slug}/">
    <meta property="og:site_name" content="tabiji.ai">
    <meta property="og:image" content="{og_image}">
    <meta name="twitter:card" content="{twitter_card}">
    <meta name="twitter:title" content="{h(name)} Travel Guide {YEAR} | tabiji.ai">
    <meta name="twitter:description" content="{h(meta_desc)}">
    <meta name="robots" content="{robots_content}">
    <link rel="canonical" href="https://tabiji.ai/countries/{slug}/">
    <link rel="stylesheet" href="/assets/countries.css">
<!-- @include:shared-head:start -->
<link rel="stylesheet" href="/assets/shared-shell.css">
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#2D3A5C">
<script defer src="/assets/shared-shell.js"></script>
<script defer src="/assets/offline-download.js"></script>
<!-- @include:shared-head:end -->

    <script type="application/ld+json">
{breadcrumb_json}
    </script>
</head>
<body>

{nav_html()}

<main>
    <div class="breadcrumb">
        <a href="/">Home</a> <span class="sep">/</span>
        <a href="/countries/">Countries</a> <span class="sep">/</span>
        <span>{h(name)}</span>
    </div>

    <section class="hero">
        <div class="hero-inner">
            <span class="hero-flag">{flag}</span>
            <h1>{h(name)} Travel Guide</h1>
            <p class="hero-subtitle">{subtitle}</p>
        </div>
    </section>
{quick_facts_html}
{advisory_html}
{health_html}
{scam_html}
{picks_html}
{compare_html}
{itin_html}
{dest_html}
{cta_html}
</main>

{footer_html()}

</body>
</html>"""

    return html, {
        "dest_count": dest_count,
        "scam_count": scam_count,
        "compare_count": compare_count,
        "itin_count": itin_count,
        "picks_count": picks_count,
    }


# ---------------------------------------------------------------------------
# Index page generator
# ---------------------------------------------------------------------------

def generate_index_page(all_countries_data):
    """Generate the /countries/index.html listing all countries."""
    count = len(all_countries_data)
    total_dests = sum(c["dest_count"] for c in all_countries_data)
    total_scams = sum(c["scam_count"] for c in all_countries_data)
    total_compares = sum(c["compare_count"] for c in all_countries_data)
    total_picks = sum(c["picks_count"] for c in all_countries_data)
    total_itins = sum(c["itin_count"] for c in all_countries_data)

    meta_desc = (
        f"Browse {count} country travel guides — {total_dests:,} destinations, "
        f"{total_picks:,} popular picks, {total_compares:,} comparisons, and "
        f"{total_scams:,} scam alerts. Backed by real Reddit reviews and traveler intel."
    )

    breadcrumb_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tabiji.ai/"},
            {"@type": "ListItem", "position": 2, "name": "Countries", "item": "https://tabiji.ai/countries/"},
        ],
    }, indent=4)

    # Sort countries by total content count desc (default view), with name as tiebreaker.
    # Empty-stats countries fall to the bottom naturally because their total = 0.
    def total_content(c):
        return (
            c["dest_count"] + c["scam_count"] + c["compare_count"]
            + c["itin_count"] + c["picks_count"]
        )

    sorted_countries = sorted(
        all_countries_data,
        key=lambda c: (-total_content(c), c["name"].lower()),
    )

    # Build country cards
    LEVEL_COLORS = {1: "#22c55e", 2: "#eab308", 3: "#f97316", 4: "#ef4444", 0: "#d1d5db"}

    def render_card(c, eager=False):
        total = total_content(c)
        is_empty = total == 0
        level = c.get("advisory_level") or 0
        adv_color = LEVEL_COLORS.get(level, "#d1d5db")
        adv_label = c.get("advisory_label") or ("No data" if level == 0 else f"Level {level}")
        hero = c.get("hero_image") or ""
        continent = c.get("continent") or "Other"

        # Stats icons row — pl() handles singular/plural
        stat_pills = []
        if c["dest_count"]:
            stat_pills.append(
                f'<span class="stat-pill" title="{pl(c["dest_count"], "destination guide")}">🏙️ {c["dest_count"]}</span>'
            )
        if c["picks_count"]:
            stat_pills.append(
                f'<span class="stat-pill" title="{pl(c["picks_count"], "popular pick")}">📍 {c["picks_count"]}</span>'
            )
        if c["compare_count"]:
            stat_pills.append(
                f'<span class="stat-pill" title="{pl(c["compare_count"], "side-by-side comparison")}">🆚 {c["compare_count"]}</span>'
            )
        if c["scam_count"]:
            stat_pills.append(
                f'<span class="stat-pill" title="{pl(c["scam_count"], "scam alert guide")}">🛡️ {c["scam_count"]}</span>'
            )
        if c["itin_count"]:
            stat_pills.append(
                f'<span class="stat-pill" title="{pl(c["itin_count"], "itinerary", "itineraries")}">🗺️ {c["itin_count"]}</span>'
            )
        stat_pills_html = "".join(stat_pills) if stat_pills else (
            '<span class="stat-pill stat-empty">No content yet</span>'
        )

        if hero:
            img_attrs = (
                'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
            )
            img_html = f'<img class="country-card-img" src="{h(hero)}" alt="" {img_attrs}>'
        else:
            img_html = '<div class="country-card-img country-card-img-fallback"></div>'

        data_attrs = (
            f'data-name="{h(c["name"]).lower()}"'
            f' data-total="{total}"'
            f' data-empty="{"1" if is_empty else "0"}"'
            f' data-has-picks="{"1" if c["picks_count"] else "0"}"'
            f' data-has-scams="{"1" if c["scam_count"] else "0"}"'
            f' data-has-compares="{"1" if c["compare_count"] else "0"}"'
            f' data-has-itins="{"1" if c["itin_count"] else "0"}"'
            f' data-advisory="{level}"'
            f' data-continent="{h(continent)}"'
            f' data-iso2="{h(c.get("iso2") or "")}"'
        )

        empty_class = " is-empty" if is_empty else ""

        return f"""
            <a href="/countries/{c['slug']}/" class="country-card{empty_class}" {data_attrs} style="border-left-color: {adv_color};">
                {img_html}
                <div class="country-card-body">
                    <div class="country-card-header">
                        <span class="country-flag">{c['flag']}</span>
                        <h2 class="country-name">{h(c['name'])}</h2>
                    </div>
                    <div class="country-card-stats">{stat_pills_html}</div>
                    <div class="country-card-advisory" title="{h(adv_label)}">
                        <span class="advisory-dot" style="background:{adv_color};"></span>
                        <span class="advisory-text">{h(adv_label) if level else "Advisory: no data"}</span>
                    </div>
                </div>
            </a>"""

    # First row (4 cards on widescreen) gets eager loading for LCP.
    country_cards = "".join(
        render_card(c, eager=(i < 4)) for i, c in enumerate(sorted_countries)
    )

    # Build hubCountries JS object
    hub_js_entries = []
    for c in all_countries_data:
        hub_js_entries.append(f'"{_js_escape(c["name"])}":"{c["slug"]}"')
    hub_js = "{" + ",".join(hub_js_entries) + "}"

    # Advisory data JS (keep full set from original)
    advisory_js_entries = []
    for name, info in sorted(ADVISORY_DATA.items()):
        advisory_js_entries.append(
            f'"{_js_escape(name)}":{{"level":{info["level"]},"slug":"{_js_escape(info["slug"])}","lt":"{_js_escape(info["lt"])}"}}'
        )
    advisory_js = "{" + ",".join(advisory_js_entries) + "}"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-D7QHNRXLHJ"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-D7QHNRXLHJ');
    </script>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="https://img.tabiji.ai/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="192x192" href="https://img.tabiji.ai/icon-192.png">
    <title>Travel Guides by Country | tabiji.ai</title>
    <meta name="description" content="{h(meta_desc)}">
    <meta property="og:title" content="Travel Guides by Country | tabiji.ai">
    <meta property="og:description" content="{h(meta_desc)}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://tabiji.ai/countries/">
    <meta property="og:site_name" content="tabiji.ai">
    <meta property="og:image" content="https://img.tabiji.ai/tabiji-owl-logo.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Travel Guides by Country | tabiji.ai">
    <meta name="twitter:description" content="{h(meta_desc)}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://tabiji.ai/countries/">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        :root {{
            --indigo:#2D3A5C; --warm-cream:#F5F0E8; --sand:#E8DFD0;
            --earth:#8B7355; --terracotta:#C4704B; --white:#FEFCF9;
            --text:#2C2419; --text-muted:#6B5D4F;
        }}
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            color: var(--text);
            background: var(--white);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }}
        a {{ color: inherit; text-decoration: none; }}

        /* hero with stats pill */
        .hero {{ padding:6rem 2rem 2.5rem; max-width:980px; margin:0 auto; text-align:center; }}
        .hero-inner h1 {{ font-size:clamp(2rem,4.5vw,2.8rem); color:var(--indigo); font-weight:800; letter-spacing:-0.02em; margin-bottom:.5rem; }}
        .hero-subtitle {{ color:var(--text-muted); font-size:1.05rem; max-width:640px; margin:0 auto 1.4rem; }}
        .hero-stats {{ display:flex; flex-wrap:wrap; gap:.6rem .8rem; justify-content:center; }}
        .hero-stats span {{ background:var(--warm-cream); border:1px solid var(--sand); color:var(--indigo); padding:.45rem 1rem; border-radius:999px; font-size:.88rem; font-weight:600; }}

        /* full-width content container */
        .layout {{ max-width:1320px; margin:0 auto; padding:0 2rem 4rem; }}

        /* map banner (full width above the grid) */
        .map-wrap {{ margin-bottom:2rem; }}
        #countryMap {{ width:100%; height:340px; border-radius:14px; border:1px solid var(--sand); z-index:1; background:#f4eedf; }}
        @media(max-width:760px) {{ #countryMap {{ height:260px; }} }}
        .map-legend {{ display:flex; flex-wrap:wrap; gap:.4rem; margin-top:.75rem; justify-content:center; }}
        .legend-chip {{ display:inline-flex; align-items:center; gap:.4rem; padding:.35rem .7rem; border:1px solid var(--sand); border-radius:999px; background:var(--white); cursor:pointer; font-size:.78rem; color:var(--text-muted); transition:all .15s; user-select:none; }}
        .legend-chip:hover {{ border-color:var(--terracotta); }}
        .legend-chip.active {{ border-color:var(--terracotta); background:#fff5ef; color:var(--indigo); font-weight:600; }}
        .legend-dot {{ width:10px; height:10px; border-radius:3px; flex-shrink:0; }}
        .map-tooltip {{ font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif; font-size:.85rem; padding:.5rem .75rem; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,.15); border:none; }}
        .map-tooltip .tt-country {{ font-weight:700; font-size:.95rem; }}
        .map-tooltip .tt-level {{ margin-top:.2rem; }}

        /* controls bar */
        .controls {{ display:flex; flex-wrap:wrap; gap:.6rem; align-items:center; margin-bottom:1.25rem; }}
        .search-input {{ flex:1; min-width:200px; padding:.65rem 1rem; border:1px solid var(--sand); border-radius:10px; font-size:.95rem; background:var(--white); color:var(--text); font-family:inherit; }}
        .search-input:focus {{ outline:none; border-color:var(--terracotta); }}
        .filter-chips {{ display:flex; flex-wrap:wrap; gap:.4rem; margin-bottom:1.5rem; }}
        .filter-chip {{ background:var(--white); border:1px solid var(--sand); color:var(--text-muted); padding:.4rem .85rem; border-radius:999px; cursor:pointer; font-size:.83rem; font-weight:500; transition:all .15s; user-select:none; font-family:inherit; }}
        .filter-chip:hover {{ border-color:var(--terracotta); color:var(--indigo); }}
        .filter-chip.active {{ background:var(--terracotta); border-color:var(--terracotta); color:#fff; font-weight:600; }}
        .filter-chip-spacer {{ flex:1; min-width:1rem; }}
        .sort-select {{ padding:.4rem .8rem; border:1px solid var(--sand); border-radius:999px; background:var(--white); color:var(--indigo); font-size:.83rem; font-weight:600; cursor:pointer; font-family:inherit; }}

        /* country grid — full width, 4 cols on widescreen */
        .country-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:1.25rem; }}
        @media(max-width:1180px) {{ .country-grid {{ grid-template-columns:repeat(3,1fr); }} }}
        @media(max-width:880px)  {{ .country-grid {{ grid-template-columns:repeat(2,1fr); }} }}
        @media(max-width:520px)  {{ .country-grid {{ grid-template-columns:1fr; }} }}

        /* group headings (region grouping mode) */
        .group-heading {{ grid-column:1/-1; font-size:.78rem; font-weight:700; text-transform:uppercase; letter-spacing:.08em; color:var(--earth); border-bottom:1px solid var(--sand); padding:1.5rem 0 .5rem; margin-top:.5rem; }}
        .group-heading:first-child {{ margin-top:0; padding-top:0; }}

        /* country card */
        .country-card {{
            background:var(--white);
            border:1px solid var(--sand);
            border-left:4px solid #d1d5db;
            border-radius:14px;
            overflow:hidden;
            display:flex;
            flex-direction:column;
            text-decoration:none;
            color:inherit;
            transition:transform .18s ease, box-shadow .18s ease, border-color .18s ease;
        }}
        .country-card:hover {{
            transform:translateY(-3px);
            box-shadow:0 8px 24px rgba(0,0,0,.08);
            border-color:var(--terracotta) !important;
        }}
        .country-card.is-empty {{ opacity:.55; }}
        .country-card.is-highlighted {{
            box-shadow:0 0 0 3px var(--terracotta), 0 8px 24px rgba(196,112,75,.2);
            border-color:var(--terracotta) !important;
        }}
        .country-card-img {{
            width:100%;
            aspect-ratio: 16 / 9;
            object-fit:cover;
            display:block;
            background:linear-gradient(135deg, var(--warm-cream), var(--sand));
        }}
        .country-card-img-fallback {{ display:block; }}
        .country-card-body {{ padding:1rem 1.1rem 1.1rem; display:flex; flex-direction:column; gap:.5rem; }}
        .country-card-header {{ display:flex; align-items:center; gap:.55rem; }}
        .country-flag {{ font-size:1.4rem; line-height:1; }}
        .country-name {{ font-size:1.05rem; font-weight:700; color:var(--indigo); margin:0; line-height:1.25; }}
        .country-card-stats {{ display:flex; flex-wrap:wrap; gap:.35rem; }}
        .stat-pill {{ display:inline-flex; align-items:center; gap:.25rem; background:var(--warm-cream); color:var(--text-muted); padding:.2rem .55rem; border-radius:999px; font-size:.75rem; font-weight:600; }}
        .stat-pill.stat-empty {{ font-style:italic; font-weight:500; opacity:.7; }}
        .country-card-advisory {{ display:flex; align-items:center; gap:.4rem; font-size:.75rem; color:var(--text-muted); }}
        .advisory-dot {{ width:8px; height:8px; border-radius:2px; flex-shrink:0; }}
        .advisory-text {{ overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}

        /* Empty results state */
        .empty-state {{ text-align:center; padding:3rem 2rem; color:var(--text-muted); grid-column:1/-1; }}
        .empty-state h3 {{ color:var(--indigo); margin-bottom:.5rem; }}
        .empty-state button {{ margin-top:1rem; background:var(--terracotta); color:#fff; border:none; padding:.6rem 1.4rem; border-radius:10px; font-weight:600; cursor:pointer; font-family:inherit; }}
    </style>
<!-- @include:shared-head:start -->
<link rel="stylesheet" href="/assets/shared-shell.css">
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#2D3A5C">
<script defer src="/assets/shared-shell.js"></script>
<script defer src="/assets/offline-download.js"></script>
<!-- @include:shared-head:end -->

    <script type="application/ld+json">
{breadcrumb_json}
    </script>
</head>
<body>

{nav_html()}

<main>
    <section class="hero">
        <div class="hero-inner">
            <h1>Travel Guides by Country</h1>
            <p class="hero-subtitle">{count} countries, backed by real Reddit reviews and traveler intel — not generic AI filler.</p>
            <div class="hero-stats">
                <span>🌍 {count} countries</span>
                <span>🏙️ {total_dests:,} destinations</span>
                <span>📍 {total_picks:,} popular picks</span>
                <span>🆚 {total_compares:,} comparisons</span>
                <span>🛡️ {total_scams:,} scam guides</span>
            </div>
        </div>
    </section>

    <div class="layout">
        <div class="map-wrap">
            <div id="countryMap"></div>
            <div class="map-legend">
                <button type="button" class="legend-chip" data-level="1"><span class="legend-dot" style="background:#22c55e;"></span> Level 1</button>
                <button type="button" class="legend-chip" data-level="2"><span class="legend-dot" style="background:#eab308;"></span> Level 2</button>
                <button type="button" class="legend-chip" data-level="3"><span class="legend-dot" style="background:#f97316;"></span> Level 3</button>
                <button type="button" class="legend-chip" data-level="4"><span class="legend-dot" style="background:#ef4444;"></span> Level 4</button>
                <button type="button" class="legend-chip" data-level="0"><span class="legend-dot" style="background:#d1d5db;"></span> No data</button>
            </div>
        </div>

        <div class="controls">
            <input type="text" class="search-input" placeholder="Search countries\u2026" id="countrySearch" oninput="applyFilters()">
            <select class="sort-select" id="sortSelect" onchange="applyFilters()">
                <option value="content-desc">Sort: Most content</option>
                <option value="name-asc">Sort: A → Z</option>
                <option value="name-desc">Sort: Z → A</option>
                <option value="advisory-asc">Sort: Safest first</option>
                <option value="region">Group by region</option>
            </select>
        </div>
        <div class="filter-chips" id="filterChips">
            <button type="button" class="filter-chip" data-filter="picks">📍 Has popular picks</button>
            <button type="button" class="filter-chip" data-filter="compares">🆚 Has comparisons</button>
            <button type="button" class="filter-chip" data-filter="scams">🛡️ Has scam guides</button>
            <button type="button" class="filter-chip" data-filter="itins">🗺️ Has itineraries</button>
            <button type="button" class="filter-chip" data-filter="hide-empty">Hide empty</button>
        </div>
        <div class="country-grid" id="countriesList">{country_cards}
        </div>
    </div>
</main>

{footer_html()}

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
// Countries with full hub pages
const hubCountries = {hub_js};

// Full advisory data (from US State Dept)
const advisoryData = {advisory_js};

const geoNameMap = {{
    "United States of America":"United States","Russian Federation":"Russia",
    "Republic of Korea":"South Korea","Dem. Rep. Korea":"North Korea",
    "Dem. Rep. Congo":"Democratic Republic of the Congo","Congo":"Republic of the Congo",
    "Czechia":"Czech Republic","Bosnia and Herz.":"Bosnia and Herzegovina",
    "Dominican Rep.":"Dominican Republic","Central African Rep.":"Central African Republic",
    "Eq. Guinea":"Equatorial Guinea","eSwatini":"Eswatini","S. Sudan":"South Sudan",
    "Solomon Is.":"Solomon Islands","Lao PDR":"Laos","Myanmar":"Burma (Myanmar)",
    "Macedonia":"North Macedonia","N. Macedonia":"North Macedonia",
    "Timor-Leste":"East Timor","Turkiye":"Turkey","T\\u00fcrkiye":"Turkey",
    "C\\u00f4te d'Ivoire":"Cote d Ivoire","Ivory Coast":"Cote d Ivoire",
    "Kyrgyzstan":"The Kyrgyz Republic","Brunei Darussalam":"Brunei",
    "Taiwan":"Taiwan","Palestine":"Palestinian Territories",
    "Somaliland":"Somalia","N. Cyprus":"Cyprus","Kosovo":"Kosovo",
}};

function getAdvisory(name) {{
    if (advisoryData[name]) return advisoryData[name];
    const mapped = geoNameMap[name];
    if (mapped && advisoryData[mapped]) return advisoryData[mapped];
    const lower = name.toLowerCase();
    for (const [k, v] of Object.entries(advisoryData)) {{
        if (k.toLowerCase() === lower) return v;
    }}
    return null;
}}

const levelColors = {{1:'#22c55e', 2:'#eab308', 3:'#f97316', 4:'#ef4444'}};

const map = L.map('countryMap', {{
    center:[25,10], zoom:1.5, minZoom:1.5, maxZoom:6,
    zoomControl:true, attributionControl:false, worldCopyJump:false,
    maxBounds:[[-85,-200],[85,200]], maxBoundsViscosity:0.8,
}});

L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_nolabels/{{z}}/{{x}}/{{y}}@2x.png',{{
    subdomains:'abcd', maxZoom:19
}}).addTo(map);

// hold layer references by canonical country name so we can highlight from list hover
const countryLayers = {{}};

fetch('https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson')
    .then(r=>r.json())
    .then(geojson=>{{
        L.geoJSON(geojson,{{
            style: function(feature){{
                const name = feature.properties.NAME || feature.properties.NAME_EN || '';
                const info = getAdvisory(name);
                const level = info ? info.level : 0;
                const color = levelColors[level] || '#d1d5db';
                return {{
                    fillColor: color,
                    fillOpacity: level === 4 ? 0.7 : level === 3 ? 0.55 : level ? 0.4 : 0.15,
                    weight: 0.8, color: '#fff', opacity: 0.8
                }};
            }},
            onEachFeature: function(feature, layer){{
                const name = feature.properties.NAME_EN || feature.properties.NAME || '';
                const info = getAdvisory(name);
                const hubSlug = hubCountries[name];
                // Save layer ref under the canonical (advisory/hub) name where possible
                const canonical = (info && Object.keys(advisoryData).find(k=>k===name)) || geoNameMap[name] || name;
                countryLayers[canonical.toLowerCase()] = {{layer, level: info ? info.level : 0}};

                if (info) {{
                    const level = info.level;
                    const color = levelColors[level] || '#94a3b8';
                    const label = info.lt || 'No advisory';
                    const hubBadge = hubSlug ? ' \\u00b7 <span style="color:#2D3A5C;font-weight:700;">Guide available</span>' : '';
                    layer.bindTooltip(
                        '<div class="map-tooltip"><div class="tt-country">' + name + '</div>' +
                        '<div class="tt-level" style="color:' + color + ';">Level ' + level + ': ' + label + '</div>' +
                        hubBadge + '</div>',
                        {{sticky:true, className:'map-tooltip'}}
                    );
                    layer.on('click', function(){{
                        if (hubSlug) {{
                            // scroll to and highlight the matching card in the list
                            const card = document.querySelector('.country-card[data-name="' + (canonical || name).toLowerCase().replace(/"/g,'\\\\"') + '"]');
                            if (card) {{
                                card.scrollIntoView({{behavior:'smooth', block:'center'}});
                                document.querySelectorAll('.country-card.is-highlighted').forEach(c=>c.classList.remove('is-highlighted'));
                                card.classList.add('is-highlighted');
                                setTimeout(()=>card.classList.remove('is-highlighted'), 2400);
                            }} else {{
                                window.location.href = '/countries/' + hubSlug + '/';
                            }}
                        }}
                    }});
                    layer.on('mouseover', function(e){{
                        e.target.setStyle({{weight:2, color:'#2D3A5C', fillOpacity:0.8}});
                        this._path.style.cursor = 'pointer';
                    }});
                    layer.on('mouseout', function(e){{
                        const l = info.level;
                        e.target.setStyle({{weight:0.8, color:'#fff', fillOpacity: l===4?0.7:l===3?0.55:l?0.4:0.15}});
                    }});
                }} else {{
                    layer.bindTooltip(
                        '<div class="map-tooltip"><div class="tt-country">' + name + '</div>' +
                        '<div class="tt-level" style="color:#94a3b8;">No data</div></div>',
                        {{sticky:true, className:'map-tooltip'}}
                    );
                }}
            }}
        }}).addTo(map);
    }});

// ---------- filter / sort / group state ----------
const state = {{
    query: '',
    filters: new Set(),         // 'picks' | 'compares' | 'scams' | 'itins' | 'hide-empty'
    levelFilter: null,          // null | 0..4
    sort: 'content-desc',       // 'content-desc' | 'name-asc' | 'name-desc' | 'advisory-asc' | 'region'
}};

const REGIONS = ['Africa','Americas','Asia','Europe','Oceania','Other'];

function applyFilters() {{
    state.query = (document.getElementById('countrySearch').value || '').toLowerCase().trim();
    state.sort = document.getElementById('sortSelect').value;
    const list = document.getElementById('countriesList');
    const cards = Array.from(list.querySelectorAll('.country-card'));

    // Pass 1: filter (visible vs hidden)
    cards.forEach(card => {{
        const name = card.dataset.name;
        const empty = card.dataset.empty === '1';
        const adv = parseInt(card.dataset.advisory, 10) || 0;
        const matches = (
            (!state.query || name.includes(state.query))
            && (!state.filters.has('picks') || card.dataset.hasPicks === '1')
            && (!state.filters.has('compares') || card.dataset.hasCompares === '1')
            && (!state.filters.has('scams') || card.dataset.hasScams === '1')
            && (!state.filters.has('itins') || card.dataset.hasItins === '1')
            && (!state.filters.has('hide-empty') || !empty)
            && (state.levelFilter === null || adv === state.levelFilter)
        );
        card.style.display = matches ? '' : 'none';
        card.classList.toggle('filtered-out', !matches);
    }});

    // Remove any prior group headings (so re-runs are clean)
    list.querySelectorAll('.group-heading').forEach(h => h.remove());

    // Pass 2: sort visible cards
    const visible = cards.filter(c => c.style.display !== 'none');
    const cmp = {{
        'content-desc': (a, b) => (parseInt(b.dataset.total,10) - parseInt(a.dataset.total,10)) || a.dataset.name.localeCompare(b.dataset.name),
        'name-asc':     (a, b) => a.dataset.name.localeCompare(b.dataset.name),
        'name-desc':    (a, b) => b.dataset.name.localeCompare(a.dataset.name),
        'advisory-asc': (a, b) => {{
            const la = parseInt(a.dataset.advisory,10) || 99;
            const lb = parseInt(b.dataset.advisory,10) || 99;
            return la - lb || a.dataset.name.localeCompare(b.dataset.name);
        }},
        'region': (a, b) => {{
            const ra = REGIONS.indexOf(a.dataset.continent || 'Other');
            const rb = REGIONS.indexOf(b.dataset.continent || 'Other');
            return (ra - rb) || ((parseInt(b.dataset.total,10)) - parseInt(a.dataset.total,10)) || a.dataset.name.localeCompare(b.dataset.name);
        }},
    }}[state.sort] || ((a,b)=>0);
    visible.sort(cmp);

    // Pass 3: re-attach in order, inserting group headings if region mode
    const frag = document.createDocumentFragment();
    let lastRegion = null;
    visible.forEach(card => {{
        if (state.sort === 'region') {{
            const r = card.dataset.continent || 'Other';
            if (r !== lastRegion) {{
                const h = document.createElement('h3');
                h.className = 'group-heading';
                h.textContent = r;
                frag.appendChild(h);
                lastRegion = r;
            }}
        }}
        frag.appendChild(card);
    }});
    // Hidden cards stay in DOM but at the end (style display:none)
    cards.filter(c => c.style.display === 'none').forEach(c => frag.appendChild(c));

    // Empty state
    list.querySelectorAll('.empty-state').forEach(e => e.remove());
    if (visible.length === 0) {{
        const empty = document.createElement('div');
        empty.className = 'empty-state';
        empty.innerHTML = '<h3>No countries match those filters</h3><p>Try removing a filter or clearing the search.</p><button type="button" onclick="clearFilters()">Clear filters</button>';
        frag.appendChild(empty);
    }}

    list.replaceChildren(frag);
}}

function clearFilters() {{
    state.query = '';
    state.filters.clear();
    state.levelFilter = null;
    document.getElementById('countrySearch').value = '';
    document.getElementById('sortSelect').value = 'content-desc';
    document.querySelectorAll('.filter-chip.active').forEach(c => c.classList.remove('active'));
    document.querySelectorAll('.legend-chip.active').forEach(c => c.classList.remove('active'));
    applyFilters();
}}

// Wire up filter chips
document.querySelectorAll('.filter-chip').forEach(chip => {{
    chip.addEventListener('click', () => {{
        const f = chip.dataset.filter;
        if (state.filters.has(f)) {{ state.filters.delete(f); chip.classList.remove('active'); }}
        else {{ state.filters.add(f); chip.classList.add('active'); }}
        applyFilters();
    }});
}});

// Wire up legend chips (advisory level filter)
document.querySelectorAll('.legend-chip').forEach(chip => {{
    chip.addEventListener('click', () => {{
        const lvl = parseInt(chip.dataset.level, 10);
        if (state.levelFilter === lvl) {{
            state.levelFilter = null;
            chip.classList.remove('active');
        }} else {{
            state.levelFilter = lvl;
            document.querySelectorAll('.legend-chip').forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
        }}
        applyFilters();
    }});
}});

// Hover a card → highlight on map
document.querySelectorAll('.country-card').forEach(card => {{
    card.addEventListener('mouseenter', () => {{
        const name = card.dataset.name;
        const entry = countryLayers[name];
        if (entry && entry.layer && entry.layer.setStyle) {{
            entry.layer.setStyle({{weight:2, color:'#2D3A5C', fillOpacity:0.9}});
        }}
    }});
    card.addEventListener('mouseleave', () => {{
        const name = card.dataset.name;
        const entry = countryLayers[name];
        if (entry && entry.layer && entry.layer.setStyle) {{
            const l = entry.level;
            entry.layer.setStyle({{weight:0.8, color:'#fff', fillOpacity: l===4?0.7:l===3?0.55:l?0.4:0.15}});
        }}
    }});
}});

// Initial sort/filter pass
applyFilters();
</script>
</body>
</html>"""

    return html


def _js_escape(s):
    """Escape a string for use inside a JS string literal (single/double quotes)."""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("'", "\\'").replace("\n", "\\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Generating country hub pages...")
    print(f"Base directory: {BASE_DIR}")

    # Pre-load all data caches
    print("  Loading destinations...")
    _load_destinations()
    print("  Loading scams...")
    _load_scams()
    print("  Loading picks...")
    _load_picks()
    print("  Loading compare dirs...")
    _load_compare_dirs()
    print("  Loading itinerary dirs...")
    _load_itin_dirs()
    print("  Loading destination pages...")
    _load_dest_pages()

    # Generate each country page
    all_countries_data = []
    generated = 0

    for name, (iso2, flag, continent) in sorted(COUNTRY_REGISTRY.items()):
        slug = slugify(name)
        out_dir = os.path.join(BASE_DIR, "countries", slug)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "index.html")

        html, stats = generate_country_page(name, slug, iso2, flag, continent)
        with open(out_path, "w") as f:
            f.write(html)

        generated += 1
        adv = ADVISORY_DATA.get(name) or {}
        all_countries_data.append({
            "name": name,
            "slug": slug,
            "flag": flag,
            "iso2": iso2,
            "continent": continent,
            "advisory_level": adv.get("level", 0),
            "advisory_label": adv.get("lt", ""),
            "hero_image": _get_country_hero_image(name, slug),
            **stats,
        })

        print(
            f"  {name:25s} -> countries/{slug}/"
            f"  ({stats['dest_count']} dests, {stats['scam_count']} scams, "
            f"{stats['compare_count']} compares, {stats['itin_count']} itins, "
            f"{stats['picks_count']} picks)"
        )

    # Sort countries for the index by name
    all_countries_data.sort(key=lambda c: c["name"])

    # Generate index page
    index_path = os.path.join(BASE_DIR, "countries", "index.html")
    html = generate_index_page(all_countries_data)
    with open(index_path, "w") as f:
        f.write(html)
    print(f"  Index  -> countries/index.html ({len(all_countries_data)} countries)")

    print(f"\nDone. Generated {generated} country pages + 1 index page.")


if __name__ == "__main__":
    main()
