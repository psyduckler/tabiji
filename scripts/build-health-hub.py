#!/usr/bin/env python3
"""
build-health-hub.py — Generate /health/index.html and /api/v1/health.json.

Pulls per-country data from /health-data/*.json and region groupings from the
current /health/index.html, then emits a fully re-designed editorial-v2 hub
plus a machine-readable API JSON for LLM consumption.

Usage:
    python3 scripts/build-health-hub.py
"""

import html
import json
import re
import sys
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from lib.editorial import (  # noqa: E402
    REVIEW_DATE,
    apply_replacements,
    render_faq_accordion,
    render_faqs_schema,
)

ROOT = SCRIPT_DIR.parent
HEALTH_DATA = ROOT / "health-data"
EXISTING_HUB = ROOT / "health" / "index.html"
OUT_HUB = ROOT / "health" / "index.html"
OUT_API = ROOT / "api" / "v1" / "health.json"

# -------------------------------------------------------------------
# Static editorial content (the 4 modules, FAQ, methodology, alerts).
# Hand-curated and dated; update when doing a monthly pass.
# -------------------------------------------------------------------

# Top destinations with a single-line critical warning the reader cannot afford
# to miss. Shown in the "Going somewhere soon?" lookup module as chips + JS.
QUICK_WARNINGS = {
    "japan": "Adderall, Vyvanse, and Sudafed are prohibited — even with a valid US prescription.",
    "thailand": "Dengue peaks April–October. Medical cannabis is legal for Thai residents only — tourists risk arrest.",
    "mexico": "Tap water is not safe anywhere. Private hospitals in tourist zones expect upfront payment.",
    "uae": "Codeine, CBD, and many common pain meds require pre-approved import permits. Customs prosecute.",
    "india": "Monsoon brings dengue and chikungunya in the south. Private hospitals in major cities only.",
    "kenya": "Yellow fever vaccination required for entry if arriving from an endemic country. Malaria risk below 2,500m.",
    "indonesia": "Rabies is endemic — don't touch dogs or monkeys. Dengue active year-round.",
    "brazil": "Yellow fever required for Amazon and Pantanal regions. Dengue epidemic since 2024.",
    "vietnam": "Foreign prescriptions are not accepted. Dengue and Japanese encephalitis risk in rural areas.",
    "philippines": "Rabies endemic, dengue year-round. Medical evacuation to Singapore or Bangkok for serious cases.",
    "egypt": "Pharmaceutical quality varies outside Cairo. Hep A/B and typhoid vaccinations recommended.",
    "morocco": "Altitude sickness risk in Atlas Mountains. Rabies risk from stray dogs in rural areas.",
    "turkey": "Private hospitals in Istanbul/Ankara are excellent. Medical tourism hub but verify credentials.",
    "south-africa": "Private healthcare is world-class; avoid public hospitals. Malaria in Kruger + northeast.",
    "peru": "Altitude sickness in Cusco/Machu Picchu (3,400m). Yellow fever for Amazon regions.",
    "singapore": "All medications with controlled ingredients require pre-approval — even melatonin. World-class care.",
    "china": "Foreign prescriptions not accepted. Air quality in northern cities can affect respiratory conditions.",
    "russia": "ADHD medications (Adderall, Ritalin) are prohibited. Foreign prescriptions not recognized.",
    "france": "EU tap water safe. Pharmacies (green cross) open Sundays in rotation. EHIC not valid for non-EU.",
    "germany": "Pharmacies (Apotheke) closed Sundays except rotating emergency shifts. Tap water safe nationwide.",
}

# Seasonal alerts — refreshed monthly. Mix of outbreak, advisory, and
# seasonal watch items grounded in real WHO/CDC/ECDC sources.
SEASONAL_ALERTS = [
    {
        "region": "Southeast Asia",
        "title": "Dengue — early surge ahead of monsoon",
        "body": "Thailand, Vietnam, Philippines, and Bali reporting above-average case counts for April. Peak season runs through October. Use DEET, cover exposed skin at dawn/dusk, and stay in screened accommodations.",
        "severity": "high",
        "source": "WHO Disease Outbreak News",
    },
    {
        "region": "Africa",
        "title": "Cholera — active outbreaks across the Horn & Southern Africa",
        "body": "Ongoing outbreaks in Ethiopia, Sudan, DRC, Zambia, and Mozambique. Stick to bottled or boiled water, avoid unpasteurized dairy, and consider the oral cholera vaccine for long stays or aid work.",
        "severity": "high",
        "source": "WHO",
    },
    {
        "region": "United Kingdom & Europe",
        "title": "Measles resurgence",
        "body": "UK, Romania, and several continental European countries reporting measles outbreaks tied to dropping MMR coverage. Check your MMR status before travel — two doses needed.",
        "severity": "medium",
        "source": "ECDC",
    },
    {
        "region": "DRC & Central Africa",
        "title": "Mpox Clade I — sustained transmission",
        "body": "Mpox clade I continues to spread in DRC and neighboring countries. CDC Level 2 advisory. Vaccination recommended for at-risk travelers.",
        "severity": "medium",
        "source": "CDC Health Alert Network",
    },
    {
        "region": "Pakistan & Afghanistan",
        "title": "Polio — vaccination required",
        "body": "Wild poliovirus transmission continues. Both countries require polio booster within 12 months of departure if staying more than 4 weeks. Keep proof of vaccination.",
        "severity": "high",
        "source": "WHO",
    },
    {
        "region": "Global",
        "title": "H5N1 avian influenza — human cases rising",
        "body": "Avoid live-poultry markets and sick or dead birds. Not a general traveler risk yet, but relevant for birders, farm tourism, and long stays in affected regions.",
        "severity": "low",
        "source": "WHO",
    },
]

# FAQ — 20 questions with short, answerable copy. Used for FAQPage schema.
FAQS = [
    {
        "q": "What's the emergency number I should memorize before I travel?",
        "a": "112 works across the EU, most of Europe, and as a fallback on any GSM mobile phone globally. 911 covers the US, Canada, and most of Latin America. 999 is the UK. Japan splits services: 119 for ambulance/fire, 110 for police. Always check the country page for the exact number before you land.",
    },
    {
        "q": "Can I drink the tap water?",
        "a": "Safe in most of Western Europe, North America, Japan, South Korea, Singapore, Australia, and New Zealand. Unsafe or risky almost everywhere else — Mexico, most of Latin America, Africa, South Asia, and Southeast Asia. When in doubt, drink bottled or filtered water and skip ice at non-tourist venues.",
    },
    {
        "q": "Does my US health insurance cover me abroad?",
        "a": "Rarely the way you'd expect. Most US plans cover emergencies only, at out-of-network rates, and require you to pay upfront and file a claim afterwards. Kaiser, Medicaid, and most HMOs are especially limited. See our carrier-by-carrier guides for details.",
    },
    {
        "q": "Do I need travel health insurance?",
        "a": "Yes, in almost every case. A hospital visit abroad can run $5,000–50,000+; medical evacuation runs $50,000–250,000. Even if your US plan covers emergencies, supplemental travel insurance handles evacuation, repatriation, and out-of-network costs your primary plan won't.",
    },
    {
        "q": "Which medications are banned in Japan?",
        "a": "Pseudoephedrine (Sudafed), Adderall, Vyvanse, Dexedrine, and most amphetamine-based ADHD medications are prohibited — even with a valid US prescription. Codeine is controlled and requires a Yakkan Shoumei import certificate for larger quantities. CBD with any THC is illegal.",
    },
    {
        "q": "Can I bring CBD or cannabis abroad?",
        "a": "Rarely safe. CBD with any THC content is illegal in Japan, UAE, Singapore, Saudi Arabia, South Korea, China, Russia, and many others. Thailand allows medical cannabis for residents only. Even CBD isolate is treated as a controlled substance in several jurisdictions. Never assume legality.",
    },
    {
        "q": "Which countries require yellow fever vaccination?",
        "a": "Most countries in sub-Saharan Africa and parts of tropical South America either require yellow fever vaccination for entry or strongly recommend it. Some countries require it only if you're arriving from an endemic country. Check our individual country pages for exact rules.",
    },
    {
        "q": "What should I do in a medical emergency abroad?",
        "a": "Call the local emergency number first (check before you land). Ask for an English-speaking doctor or a hospital with international patients. Contact your travel insurer's 24/7 assistance line — they can coordinate payment, find accredited facilities, and arrange evacuation if needed.",
    },
    {
        "q": "How much does medical evacuation cost?",
        "a": "$15,000–60,000 for most regional transfers. $100,000–250,000 for intercontinental ICU-level evacuation. Major providers include Global Rescue, MedJet, and International SOS. This is the single biggest financial risk of serious illness abroad and the main reason to buy travel insurance.",
    },
    {
        "q": "Is it safe to eat street food?",
        "a": "Often yes — at busy stalls where food is cooked to order and turnover is high. Avoid raw or undercooked meat and seafood, salads washed in tap water, and sliced fruit. Stick to food that's served hot off the flame. The busiest stall in the neighborhood is usually the safest bet.",
    },
    {
        "q": "Should I bring my own medications or buy them locally?",
        "a": "Bring everything you take regularly, in original labeled packaging, with a doctor's letter listing generic names and indications. Local pharmacies in developed countries often stock equivalents — but in developing regions, counterfeit medications are a real risk. Bring more than you need.",
    },
    {
        "q": "What is BCBS Global Core and how does it work?",
        "a": "BCBS Global Core gives members access to a network of international doctors and hospitals in 190+ countries. Call 1-800-810-BLUE (2583) before non-emergency care; for emergencies, go to the nearest hospital and call within 48 hours. Many network hospitals can bill BCBS directly.",
    },
    {
        "q": "Is Kaiser Permanente valid internationally?",
        "a": "Kaiser covers emergency care abroad but on a reimbursement basis — you pay upfront and file a claim. No out-of-area routine or urgent care. Kaiser is the worst major US carrier for international travel. Supplemental insurance is essential if you're a Kaiser member going abroad.",
    },
    {
        "q": "How do I find an English-speaking doctor abroad?",
        "a": "Ask your travel insurer's assistance line first — they maintain vetted lists. Second option: the US embassy in-country publishes a list of English-speaking physicians. International hospitals (Bumrungrad in Bangkok, Mount Elizabeth in Singapore, American Hospital in Paris) always have English-speaking staff.",
    },
    {
        "q": "Do I need a prescription for my medication in the country I'm visiting?",
        "a": "In most countries, foreign prescriptions are not legally accepted — you'll need a local doctor to re-prescribe. Always bring your own supply with you in original packaging. Carrying controlled substances without proper documentation can result in confiscation or arrest in strict-enforcement countries.",
    },
    {
        "q": "What vaccinations does the CDC recommend for travelers?",
        "a": "Routine (MMR, Tdap, polio, flu) should be up to date for everyone. Travel-specific depends on destination: Hep A and typhoid for developing countries, Hep B for long stays or medical tourism, yellow fever for endemic regions, rabies for remote or animal-contact travel, Japanese encephalitis for rural Asia.",
    },
    {
        "q": "How do I file an insurance claim from abroad?",
        "a": "Keep every receipt, itemized bill, and medical report. Ask for English-language documentation. Pay with a credit card if possible — it creates an audit trail. File the claim with your insurer on return. Many travel insurers can direct-bill the hospital if you call their assistance line first.",
    },
    {
        "q": "What's the most common health risk for tourists?",
        "a": "Road traffic accidents. Not exotic diseases — moped crashes in Southeast Asia, pedestrian accidents in cities where traffic rules differ, and rental-car crashes are the leading cause of tourist deaths worldwide. Wear a helmet, use seatbelts, and don't drive drunk.",
    },
    {
        "q": "What if I run out of medication abroad?",
        "a": "In developed countries, an English-speaking doctor can usually re-prescribe. In developing regions, pharmacies may stock generic equivalents without requiring a prescription — but verify authenticity (counterfeit risk). The US embassy in-country can sometimes help with emergency prescriptions.",
    },
    {
        "q": "Is travel health insurance worth it for short trips?",
        "a": "Yes, even for a long weekend. Policies start at $20–40 for a week. A single ambulance ride abroad costs more than five years of travel insurance premiums. The math is unambiguous; the only question is which provider and coverage level.",
    },
]

# Curated "editor lists" module (3 browse cards). Each maps to an existing
# destination or an in-page anchor.
EDITOR_LISTS = [
    {
        "eyebrow": "Restricted medications",
        "href": "/health/medications/",
        "title": "10 countries where your <em>prescription might be illegal</em>",
        "body": "Adderall in Japan, CBD in the UAE, codeine in Qatar, pseudoephedrine almost everywhere in East Asia. The rules that get overlooked until customs.",
        "cta": "See the list →",
    },
    {
        "eyebrow": "Medical evacuation",
        "href": "#medevac-spotlight",
        "title": "Top 5 <em>medical evacuation</em> nightmares",
        "body": "Mongolia's steppe, Bolivia's altitude, Madagascar, Nepal's trekking regions, remote Pacific. Where a helicopter call-out can run six figures.",
        "cta": "Plan ahead →",
    },
    {
        "eyebrow": "US health insurance",
        "href": "/health/insurance/",
        "title": "Where US insurance <em>actually works</em> abroad",
        "body": "PPO emergencies flow through most of Europe. Kaiser and most HMOs break down the moment you leave the US. Carrier-by-carrier breakdown.",
        "cta": "Check your carrier →",
    },
]

MEDEVAC_SPOTLIGHT = [
    {
        "slug": "mongolia",
        "flag": "🇲🇳",
        "name": "Mongolia",
        "note": "Ulaanbaatar has one tier-2 hospital. Anything serious = evacuation to Seoul or Beijing. Gobi treks put you 48+ hours from any hospital.",
    },
    {
        "slug": "bolivia",
        "flag": "🇧🇴",
        "name": "Bolivia",
        "note": "La Paz is 3,640m. Altitude complicates trauma care; severe cases evacuate to Santa Cruz or Lima. High-altitude pulmonary edema needs immediate descent.",
    },
    {
        "slug": "madagascar",
        "flag": "🇲🇬",
        "name": "Madagascar",
        "note": "Limited specialist care outside Antananarivo. Evacuation to Johannesburg or Réunion is standard for anything beyond a GP visit.",
    },
    {
        "slug": "nepal",
        "flag": "🇳🇵",
        "name": "Nepal",
        "note": "Trekking regions above 3,000m have altitude-sickness helicopter rescues running $5K–20K. Kathmandu hospitals handle basics; serious cases go to Bangkok or Singapore.",
    },
    {
        "slug": "papua-new-guinea",
        "flag": "🇵🇬",
        "name": "Papua New Guinea",
        "note": "Port Moresby has one adequate private hospital. Outside the capital, evacuation to Cairns or Brisbane is the only realistic option.",
    },
]

# Countries where yellow fever vaccination is required for entry (for at least
# some travelers — either all or those arriving from endemic zones).
# Source: CDC Yellow Book 2026 + IAMAT.
YF_REQUIRED_SLUGS = {
    "angola", "argentina", "benin", "bolivia", "brazil", "burkina-faso", "burundi",
    "cameroon", "central-african-republic", "chad", "colombia", "dr-congo",
    "ivory-coast", "ecuador", "equatorial-guinea", "ethiopia", "french-guiana",
    "gabon", "gambia", "ghana", "guinea", "guinea-bissau", "guyana", "kenya",
    "liberia", "mali", "mauritania", "niger", "nigeria", "panama", "paraguay",
    "peru", "republic-of-the-congo", "rwanda", "sao-tome-and-principe", "senegal",
    "sierra-leone", "south-sudan", "sudan", "suriname", "tanzania", "togo",
    "trinidad-and-tobago", "uganda", "venezuela",
}

# Countries with strict medication-enforcement regimes where common US/EU meds
# can result in arrest or confiscation at customs. Hand-picked from known cases.
STRICT_MEDS_SLUGS = {
    "japan", "uae", "singapore", "saudi-arabia", "south-korea", "thailand",
    "mexico", "indonesia", "china", "russia", "egypt", "qatar", "kuwait",
    "bahrain", "oman", "iran", "malaysia",
}

# -------------------------------------------------------------------
# Data extraction
# -------------------------------------------------------------------

_REGION_PATTERN = re.compile(
    r'<(?:div|section) class="region-section" data-region="([a-z\-]+)">\s*'
    r'<h2(?:\s+class="[^"]*")?>([^<]+)</h2>\s*'
    r'<div class="country-grid(?: city-grid)?">(.*?)</div>\s*</(?:div|section)>',
    re.DOTALL,
)
_CARD_PATTERN = re.compile(
    r'<a href="/health/([a-z\-]+)/" class="country-card(?: city-card)?" '
    r'data-country="([^"]+)"([^>]*)>(.*?)</a>',
    re.DOTALL,
)
_CARD_ATTR_PATTERN = re.compile(r'data-([a-z]+)="([^"]*)"')
_FLAG_PATTERN_LEGACY = re.compile(r'flag">([^<]+)</span>')
_FLAG_PATTERN_EDITORIAL = re.compile(r'<div class="flag">([^<]+)</div>')
_LEGACY_RATING_PATTERN = re.compile(r'color:#8B7355;[^"]*">([^<]+)</div>')
_LEGACY_BADGE_PATTERN = re.compile(r'class="badge [a-z\-]+">([^<]+)</span>')
_RATING_LABEL_PATTERN = re.compile(r'<span class="rating-label">([^<]+)</span>')


def parse_regions(hub_html: str):
    """Extract ordered regions and their country slugs from the hub (supports
    both the legacy indigo-gradient layout and the current editorial-v2 one)."""
    regions = []
    for m in _REGION_PATTERN.finditer(hub_html):
        slug, heading, grid = m.group(1), html.unescape(m.group(2)), m.group(3)
        slugs = re.findall(r'href="/health/([a-z\-]+)/"', grid)
        regions.append({"slug": slug, "heading": heading, "slugs": slugs})
    return regions


def _parse_water_insurance_from_legacy_badges(body: str):
    water = "unknown"
    insurance = "recommended"
    for b in _LEGACY_BADGE_PATTERN.findall(body):
        if "Safe Water" in b:
            water = "safe"
        elif "Caution" in b and "Water" in b:
            water = "caution"
        elif "Unsafe" in b or "Don't drink" in b:
            water = "unsafe"
        if "Insurance Required" in b:
            insurance = "required"
    return water, insurance


def parse_card_metadata(hub_html: str):
    """Map slug → {name, flag, stars, rating_label, water, insurance} by
    reading the hub HTML. Prefers data-* attributes (editorial-v2), falls back
    to parsing badge text + rating div (legacy hub)."""
    meta = {}
    for m in _CARD_PATTERN.finditer(hub_html):
        slug = m.group(1)
        name = html.unescape(m.group(2))
        attrs_tail = m.group(3)
        body = m.group(4)
        attrs = dict(_CARD_ATTR_PATTERN.findall(attrs_tail))

        flag_m = _FLAG_PATTERN_EDITORIAL.search(body) or _FLAG_PATTERN_LEGACY.search(body)
        flag = flag_m.group(1) if flag_m else ""

        if "rating" in attrs:
            stars = int(attrs["rating"])
            label_m = _RATING_LABEL_PATTERN.search(body)
            rating_label = label_m.group(1) if label_m else "Unrated"
        else:
            rating_m = _LEGACY_RATING_PATTERN.search(body)
            rating_raw = html.unescape(rating_m.group(1)) if rating_m else ""
            stars = rating_raw.count("★")
            rating_label = re.sub(r"[★☆]", "", rating_raw).strip() or "Unrated"

        if "water" in attrs:
            water = attrs["water"]
            insurance = attrs.get("insurance", "recommended")
        else:
            water, insurance = _parse_water_insurance_from_legacy_badges(body)

        meta[slug] = {
            "name": name,
            "flag": flag,
            "stars": stars,
            "rating_label": rating_label,
            "water": water,
            "insurance": insurance,
        }

    for slug, m in meta.items():
        if m["water"] in (None, "unknown"):
            data = load_country_data(slug)
            if data:
                ws = (data.get("waterSafety") or "").lower()
                if ws in ("safe", "caution", "unsafe"):
                    m["water"] = ws
    return meta


_COUNTRY_DATA = None


def load_country_data(slug: str):
    """Per-country health-data/{ISO}.json, keyed by countrySlug. Parses the
    210-file directory once on first call."""
    global _COUNTRY_DATA
    if _COUNTRY_DATA is None:
        _COUNTRY_DATA = {}
        for p in HEALTH_DATA.glob("*.json"):
            try:
                data = json.loads(p.read_text())
                _COUNTRY_DATA[data.get("countrySlug")] = data
            except Exception:
                pass
    return _COUNTRY_DATA.get(slug)


# -------------------------------------------------------------------
# Templates
# -------------------------------------------------------------------

STAR_FULL = "★"
STAR_EMPTY = "☆"


def render_stars(n: int) -> str:
    return STAR_FULL * n + STAR_EMPTY * (5 - n)


def render_card(slug: str, meta: dict) -> str:
    water = meta["water"]
    insurance = meta["insurance"]
    stars = meta["stars"]
    name = html.escape(meta["name"])
    flag = meta["flag"]
    rating_label = html.escape(meta["rating_label"])

    data_yf = "1" if slug in YF_REQUIRED_SLUGS else "0"
    data_strict = "1" if slug in STRICT_MEDS_SLUGS else "0"

    tagline_bits = []
    if water == "unsafe":
        tagline_bits.append("Tap water unsafe")
    elif water == "caution":
        tagline_bits.append("Tap water — caution")
    elif water == "safe":
        tagline_bits.append("Tap water safe")
    if data_yf == "1":
        tagline_bits.append("Yellow fever risk")
    if data_strict == "1":
        tagline_bits.append("Strict medication rules")
    if insurance == "required":
        tagline_bits.append("Insurance required for entry")
    tagline = " · ".join(tagline_bits[:3]) if tagline_bits else "See the full guide for details."

    return (
        f'      <a href="/health/{slug}/" class="country-card city-card" '
        f'data-country="{name}" data-water="{water}" data-rating="{stars}" '
        f'data-insurance="{insurance}" data-yf="{data_yf}" data-strict="{data_strict}">\n'
        f'        <div class="flag">{flag}</div>\n'
        f'        <div class="city-name">{name}</div>\n'
        f'        <div class="country-rating" aria-label="{rating_label} healthcare, {stars} of 5">'
        f'<span class="stars" aria-hidden="true">{render_stars(stars)}</span>'
        f'<span class="rating-label">{rating_label}</span></div>\n'
        f'        <div class="city-tagline">{html.escape(tagline)}</div>\n'
        f'        <div class="arrow">Read the guide →</div>\n'
        f'      </a>'
    )


def render_alerts() -> str:
    items = []
    for a in SEASONAL_ALERTS:
        items.append(
            f'      <li class="alert-item alert-{a["severity"]}">'
            f'<span class="alert-region">{html.escape(a["region"])}</span>'
            f'<strong class="alert-title">{html.escape(a["title"])}</strong>'
            f'<p class="alert-body">{html.escape(a["body"])}</p>'
            f'<span class="alert-source">Source: {html.escape(a["source"])}</span>'
            f'</li>'
        )
    return "\n".join(items)


def render_editor_lists() -> str:
    items = []
    for c in EDITOR_LISTS:
        items.append(
            f'    <a href="{c["href"]}" class="browse-card">\n'
            f'      <span class="browse-eyebrow">{html.escape(c["eyebrow"])}</span>\n'
            f'      <h3 class="browse-title">{c["title"]}</h3>\n'
            f'      <p>{html.escape(c["body"])}</p>\n'
            f'      <span class="browse-arrow">{html.escape(c["cta"])}</span>\n'
            f'    </a>'
        )
    return "\n".join(items)


def render_medevac_spotlight(meta) -> str:
    items = []
    for c in MEDEVAC_SPOTLIGHT:
        slug = c["slug"]
        href = f'/health/{slug}/'
        items.append(
            f'      <a href="{href}" class="medevac-row">\n'
            f'        <span class="medevac-flag">{c["flag"]}</span>\n'
            f'        <div class="medevac-body">\n'
            f'          <strong>{html.escape(c["name"])}</strong>\n'
            f'          <p>{html.escape(c["note"])}</p>\n'
            f'        </div>\n'
            f'        <span class="medevac-arrow">→</span>\n'
            f'      </a>'
        )
    return "\n".join(items)


QUICK_LOOKUP_ORDER = [
    "japan", "thailand", "mexico", "uae", "india", "kenya", "indonesia",
    "brazil", "france", "germany", "turkey", "peru",
]


def render_quick_lookup_chips(meta_by_slug: dict) -> str:
    chips = []
    for slug in QUICK_LOOKUP_ORDER:
        m = meta_by_slug.get(slug)
        name = html.escape(m["name"]) if m else slug.title()
        flag = m["flag"] if m else "🌍"
        chips.append(
            f'      <button class="lookup-chip" type="button" data-slug="{slug}">'
            f'<span class="lookup-chip-flag">{flag}</span>{name}</button>'
        )
    return "\n".join(chips)


# -------------------------------------------------------------------
# Main generators
# -------------------------------------------------------------------

def build_hub(regions, meta):
    total_countries = sum(len(r["slugs"]) for r in regions)

    region_sections = []
    for region in regions:
        cards = []
        for slug in region["slugs"]:
            m = meta.get(slug)
            if not m:
                continue
            cards.append(render_card(slug, m))
        region_sections.append(
            f'  <section class="region-section" data-region="{region["slug"]}">\n'
            f'    <h2 class="region-heading">{html.escape(region["heading"])}</h2>\n'
            f'    <div class="country-grid city-grid">\n'
            + "\n".join(cards) + "\n"
            f'    </div>\n'
            f'  </section>'
        )
    regions_html = "\n".join(region_sections)

    alerts_html = render_alerts()
    editor_lists_html = render_editor_lists()
    medevac_html = render_medevac_spotlight(meta)
    faqs_html = render_faq_accordion(FAQS, id_prefix="faq")
    lookup_chips_html = render_quick_lookup_chips(meta)
    quick_warnings_js = json.dumps(QUICK_WARNINGS, ensure_ascii=False)

    today = date.today().isoformat()

    # Schema.org graph: MedicalWebPage + BreadcrumbList + FAQPage + ItemList
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "MedicalWebPage",
                "name": "Travel Health & Medication Guides",
                "headline": "Travel health, country by country.",
                "description": (
                    f"Travel health guides for {total_countries} countries — emergency "
                    "numbers, pharmacy access, restricted medications, vaccinations, "
                    "water safety, and US health-insurance reality-checks for international travelers."
                ),
                "url": "https://tabiji.ai/health/",
                "inLanguage": "en",
                "about": [
                    {"@type": "MedicalCondition", "name": "Travelers' diarrhea"},
                    {"@type": "MedicalCondition", "name": "Dengue fever"},
                    {"@type": "MedicalCondition", "name": "Yellow fever"},
                    {"@type": "MedicalCondition", "name": "Altitude sickness"},
                    {"@type": "MedicalCondition", "name": "Rabies"},
                ],
                "audience": {"@type": "PeopleAudience", "audienceType": "International travelers"},
                "reviewedBy": {
                    "@type": "Organization",
                    "name": "tabiji editorial team",
                    "url": "https://tabiji.ai/about/",
                },
                "datePublished": "2026-03-01",
                "dateModified": today,
                "lastReviewed": today,
                "publisher": {
                    "@type": "Organization",
                    "name": "tabiji.ai",
                    "url": "https://tabiji.ai",
                    "logo": {
                        "@type": "ImageObject",
                        "url": "https://img.tabiji.ai/tabiji-owl-logo.png",
                    },
                },
                "specialty": "TravelMedicine",
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tabiji.ai/"},
                    {"@type": "ListItem", "position": 2, "name": "Travel Health", "item": "https://tabiji.ai/health/"},
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": render_faqs_schema(FAQS),
            },
            {
                "@type": "ItemList",
                "name": f"Travel Health Guides for {total_countries} Countries",
                "numberOfItems": total_countries,
                "itemListOrder": "https://schema.org/ItemListOrderAlphabetical",
            },
        ],
    }
    schema_str = json.dumps(schema, ensure_ascii=False, indent=2)

    replacements = {
        "__TOTAL_COUNTRIES__": str(total_countries),
        "__REVIEW_DATE__": REVIEW_DATE,
        "__TODAY__": today,
        "__SCHEMA__": schema_str,
        "__LOOKUP_CHIPS__": lookup_chips_html,
        "__ALERTS__": alerts_html,
        "__EDITOR_LISTS__": editor_lists_html,
        "__MEDEVAC__": medevac_html,
        "__REGIONS__": regions_html,
        "__FAQS__": faqs_html,
        "__QUICK_WARNINGS_JS__": quick_warnings_js,
    }
    html_out = apply_replacements(HUB_TEMPLATE, replacements)
    OUT_HUB.write_text(html_out)
    print(f"Wrote {OUT_HUB} ({len(html_out):,} chars, {total_countries} countries)")


def build_api(regions, meta):
    """Emit /api/v1/health.json — structured data for LLMs and agents."""
    countries = []
    for region in regions:
        for slug in region["slugs"]:
            m = meta.get(slug)
            if not m:
                continue
            data = load_country_data(slug)
            record = {
                "slug": slug,
                "name": m["name"],
                "flag": m["flag"],
                "region": region["slug"],
                "url": f"https://tabiji.ai/health/{slug}/",
                "healthcareQuality": m["stars"],
                "healthcareQualityLabel": m["rating_label"],
                "waterSafety": m["water"],
                "insuranceRequired": m["insurance"] == "required",
                "yellowFeverRequired": slug in YF_REQUIRED_SLUGS,
                "strictMedications": slug in STRICT_MEDS_SLUGS,
            }
            if data:
                record["iso2"] = data.get("iso2")
                record["emergencyNumber"] = data.get("emergencyNumber")
                record["healthcareSystem"] = data.get("healthcareSystem")
                record["pharmacyAccess"] = data.get("pharmacyAccess")
                # Summarize restricted medications for quick LLM ingest
                banned = [r for r in data.get("restrictedMeds") or [] if r.get("status") == "banned"]
                restricted = [r for r in data.get("restrictedMeds") or [] if r.get("status") == "restricted"]
                record["bannedMedications"] = [r.get("name") for r in banned][:10]
                record["restrictedMedications"] = [r.get("name") for r in restricted][:10]
                record["lastUpdated"] = data.get("lastUpdated")
            countries.append(record)

    carriers = [
        {"slug": "aetna", "name": "Aetna"},
        {"slug": "anthem", "name": "Anthem"},
        {"slug": "blue-cross-blue-shield", "name": "Blue Cross Blue Shield"},
        {"slug": "carefirst", "name": "CareFirst"},
        {"slug": "centene", "name": "Centene"},
        {"slug": "cigna", "name": "Cigna"},
        {"slug": "hcsc", "name": "HCSC"},
        {"slug": "highmark", "name": "Highmark"},
        {"slug": "humana", "name": "Humana"},
        {"slug": "independence-blue-cross", "name": "Independence Blue Cross"},
        {"slug": "kaiser-permanente", "name": "Kaiser Permanente"},
        {"slug": "molina-healthcare", "name": "Molina Healthcare"},
        {"slug": "premera-blue-cross", "name": "Premera Blue Cross"},
        {"slug": "regence", "name": "Regence"},
        {"slug": "unitedhealthcare", "name": "UnitedHealthcare"},
    ]
    for c in carriers:
        c["url"] = f"https://tabiji.ai/health/insurance/{c['slug']}/"

    api = {
        "$schema": "https://tabiji.ai/api/v1/health.schema.json",
        "version": "1.0",
        "generatedAt": date.today().isoformat(),
        "reviewedBy": "tabiji editorial team",
        "sources": [
            "CDC Travelers' Health",
            "WHO International Travel and Health",
            "IATA Travel Centre",
            "US Department of State — travel.state.gov",
            "National health-ministry sources per country",
        ],
        "totalCountries": len(countries),
        "totalCarriers": len(carriers),
        "countries": countries,
        "insuranceCarriers": carriers,
        "medicationsHub": "https://tabiji.ai/health/medications/",
        "insuranceHub": "https://tabiji.ai/health/insurance/",
    }

    OUT_API.parent.mkdir(parents=True, exist_ok=True)
    OUT_API.write_text(json.dumps(api, ensure_ascii=False, indent=2))
    print(f"Wrote {OUT_API} ({len(countries)} countries, {len(carriers)} carriers)")


# -------------------------------------------------------------------
# HTML template
# -------------------------------------------------------------------

HUB_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://img.tabiji.ai">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-D7QHNRXLHJ"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-D7QHNRXLHJ');</script>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="https://img.tabiji.ai/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="192x192" href="https://img.tabiji.ai/icon-192.png">
    <title>Travel Health, Country by Country — Emergency Numbers, Meds, Insurance | tabiji.ai</title>
    <meta name="description" content="Travel health guides for __TOTAL_COUNTRIES__ countries. Emergency numbers, pharmacy language, restricted medications, vaccinations, water safety, and US health-insurance reality-checks — researched and kept current by the tabiji editorial team.">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="https://tabiji.ai/health/">
    <meta property="og:title" content="Travel Health, Country by Country — tabiji.ai">
    <meta property="og:description" content="Emergency numbers, pharmacy language, restricted medications, vaccinations, water safety, and US health-insurance reality-checks for __TOTAL_COUNTRIES__ countries.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://tabiji.ai/health/">
    <meta property="og:image" content="https://img.tabiji.ai/tabiji-owl-logo.png">
    <meta property="og:site_name" content="tabiji.ai">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Travel Health, Country by Country — tabiji.ai">
    <meta name="twitter:description" content="Emergency numbers, meds, vaccinations, water safety, and US insurance reality-checks for __TOTAL_COUNTRIES__ countries.">

    <script type="application/ld+json">__SCHEMA__</script>

    <link rel="stylesheet" href="/assets/scams.css">
    <style>
    /* Health-hub-specific additions layered on top of editorial-v2 (scams.css) */
    body.editorial-v2 .reviewer-strip {
        max-width: 860px;
        margin: 1rem auto 0;
        padding: 1rem 1.5rem;
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-left: 4px solid var(--sage);
        border-radius: var(--radius-md);
        font-family: var(--font-serif);
        font-style: italic;
        font-size: 0.95rem;
        color: var(--text-muted);
        line-height: 1.5;
        text-align: left;
    }
    body.editorial-v2 .reviewer-strip strong { font-style: normal; color: var(--indigo); }
    body.editorial-v2 .reviewer-strip a {
        color: var(--terracotta);
        text-decoration: none;
        border-bottom: 1px solid transparent;
        transition: border-color 0.2s;
        font-style: normal;
        font-weight: 600;
    }
    body.editorial-v2 .reviewer-strip a:hover { border-bottom-color: var(--terracotta); }

    body.editorial-v2 .module-section {
        max-width: 1100px;
        margin: 3.5rem auto 0;
        padding: 0 1.5rem;
    }
    body.editorial-v2 .module-section > h2 {
        font-family: var(--font-serif);
        font-size: clamp(1.6rem, 3vw, 2rem);
        font-weight: 500;
        color: var(--indigo);
        letter-spacing: -0.01em;
        line-height: 1.2;
        margin-bottom: 0.5rem;
        max-width: 720px;
    }
    body.editorial-v2 .module-section > h2 em { color: var(--terracotta); font-style: italic; font-weight: 500; }
    body.editorial-v2 .module-section > p.lede {
        font-family: var(--font-serif);
        font-style: italic;
        font-size: 1.05rem;
        color: var(--text-muted);
        line-height: 1.55;
        max-width: 620px;
        margin-bottom: 1.75rem;
    }

    /* Module 1 — Quick lookup */
    body.editorial-v2 .quick-lookup-wrap { max-width: 680px; }
    body.editorial-v2 .lookup-chip-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-top: 1rem;
    }
    body.editorial-v2 .lookup-chip {
        background: var(--white);
        border: 1px solid var(--sand);
        border-radius: var(--radius-pill);
        padding: 0.45rem 0.95rem;
        font-family: var(--font-sans);
        font-size: 0.82rem;
        font-weight: 500;
        color: var(--indigo);
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        transition: border-color 0.2s, color 0.2s, transform 0.15s;
    }
    body.editorial-v2 .lookup-chip:hover {
        border-color: var(--terracotta);
        color: var(--terracotta);
        transform: translateY(-1px);
    }
    body.editorial-v2 .lookup-chip-flag { font-size: 1rem; line-height: 1; }
    body.editorial-v2 .quick-result {
        margin-top: 1.25rem;
        padding: 1.25rem 1.5rem;
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-left: 4px solid var(--terracotta);
        border-radius: var(--radius-md);
        font-family: var(--font-serif);
        line-height: 1.55;
    }
    body.editorial-v2 .quick-result .quick-result-label {
        font-family: var(--font-sans);
        font-size: 0.7rem;
        font-weight: 700;
        color: var(--terracotta);
        letter-spacing: 0.22em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
        display: block;
    }
    body.editorial-v2 .quick-result .quick-result-country {
        font-family: var(--font-serif);
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--indigo);
        margin-bottom: 0.35rem;
        display: block;
    }
    body.editorial-v2 .quick-result .quick-result-body {
        font-size: 1rem;
        color: var(--text);
        margin-bottom: 0.6rem;
    }
    body.editorial-v2 .quick-result a {
        font-family: var(--font-sans);
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--terracotta);
        text-decoration: none;
        border-bottom: 1px solid transparent;
    }
    body.editorial-v2 .quick-result a:hover { border-bottom-color: var(--terracotta); }

    /* Module 2 — Seasonal alerts */
    body.editorial-v2 .alerts-list {
        list-style: none;
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 1rem;
        padding: 0;
        margin: 0;
    }
    body.editorial-v2 .alert-item {
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        padding: 1.15rem 1.35rem 1.1rem;
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
        border-left: 4px solid var(--earth-light);
    }
    body.editorial-v2 .alert-item.alert-high { border-left-color: var(--ed-high-text); }
    body.editorial-v2 .alert-item.alert-medium { border-left-color: var(--ed-med-text); }
    body.editorial-v2 .alert-item.alert-low { border-left-color: var(--ed-low-text); }
    body.editorial-v2 .alert-region {
        font-family: var(--font-sans);
        font-size: 0.7rem;
        font-weight: 700;
        color: var(--terracotta);
        letter-spacing: 0.22em;
        text-transform: uppercase;
    }
    body.editorial-v2 .alert-title {
        font-family: var(--font-serif);
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--indigo);
        line-height: 1.25;
        letter-spacing: -0.005em;
    }
    body.editorial-v2 .alert-body {
        font-size: 0.92rem;
        color: var(--text-muted);
        line-height: 1.55;
        margin: 0;
    }
    body.editorial-v2 .alert-source {
        font-family: var(--font-serif);
        font-style: italic;
        font-size: 0.82rem;
        color: var(--earth);
        margin-top: 0.25rem;
    }

    /* Module 3 uses .browse-grid / .browse-card from editorial-v2 directly */

    /* Medevac spotlight list */
    body.editorial-v2 .medevac-list {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    body.editorial-v2 .medevac-row {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        padding: 1rem 1.25rem;
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        text-decoration: none;
        color: var(--text);
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    body.editorial-v2 .medevac-row:hover {
        border-color: var(--terracotta);
        box-shadow: 0 4px 14px rgba(45, 58, 92, 0.08);
    }
    body.editorial-v2 .medevac-flag { font-size: 1.6rem; line-height: 1; flex-shrink: 0; }
    body.editorial-v2 .medevac-body { flex: 1; }
    body.editorial-v2 .medevac-body strong {
        font-family: var(--font-serif);
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--indigo);
        display: block;
        margin-bottom: 0.2rem;
    }
    body.editorial-v2 .medevac-body p {
        font-size: 0.92rem;
        color: var(--text-muted);
        line-height: 1.5;
        margin: 0;
    }
    body.editorial-v2 .medevac-arrow {
        color: var(--terracotta);
        font-family: var(--font-sans);
        font-weight: 600;
        align-self: center;
        flex-shrink: 0;
    }

    /* Module 4 — Risk matrix filters */
    body.editorial-v2 .filter-matrix {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        margin-top: 0.5rem;
    }
    body.editorial-v2 .filter-row {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.55rem;
    }
    body.editorial-v2 .filter-row-label {
        font-family: var(--font-sans);
        font-size: 0.72rem;
        font-weight: 700;
        color: var(--earth);
        letter-spacing: 0.14em;
        text-transform: uppercase;
        min-width: 110px;
    }
    body.editorial-v2 .filter-reset {
        background: transparent;
        border: 1px dashed var(--sand);
        color: var(--text-muted);
        padding: 0.4rem 0.9rem;
        border-radius: var(--radius-pill);
        font-family: var(--font-sans);
        font-size: 0.8rem;
        cursor: pointer;
        margin-top: 0.35rem;
        transition: border-color 0.2s, color 0.2s;
    }
    body.editorial-v2 .filter-reset:hover { border-color: var(--terracotta); color: var(--terracotta); }

    /* Directory — star rating legend + re-styled cards */
    body.editorial-v2 .rating-legend {
        max-width: 1100px;
        margin: 1.75rem auto 0.75rem;
        padding: 0.9rem 1.25rem;
        background: var(--warm-cream-soft);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        font-family: var(--font-serif);
        font-size: 0.88rem;
        color: var(--text-muted);
        line-height: 1.55;
    }
    body.editorial-v2 .rating-legend strong {
        font-family: var(--font-sans);
        font-size: 0.72rem;
        font-weight: 700;
        color: var(--terracotta);
        letter-spacing: 0.2em;
        text-transform: uppercase;
        display: block;
        margin-bottom: 0.35rem;
    }
    body.editorial-v2 .rating-legend .legend-star { color: var(--terracotta); font-weight: 600; }

    body.editorial-v2 .region-section {
        max-width: 1100px;
        margin: 2rem auto 0;
        padding: 0 1.5rem;
    }
    body.editorial-v2 .region-heading {
        font-family: var(--font-serif);
        font-size: clamp(1.3rem, 2.5vw, 1.6rem);
        font-weight: 500;
        color: var(--indigo);
        letter-spacing: -0.005em;
        margin: 2rem 0 1.1rem;
        padding-bottom: 0.55rem;
        border-bottom: 1px solid var(--sand);
    }
    body.editorial-v2 .country-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
        gap: 1rem;
    }
    body.editorial-v2 .country-card {
        /* Uses .city-card base from scams.css — these are overrides */
        background: var(--warm-cream);
    }
    body.editorial-v2 .country-card .country-rating {
        font-family: var(--font-sans);
        font-size: 0.78rem;
        color: var(--earth);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 0.1rem;
    }
    body.editorial-v2 .country-card .stars {
        color: var(--terracotta);
        letter-spacing: 0.08em;
        font-size: 0.9rem;
    }
    body.editorial-v2 .country-card .rating-label {
        font-family: var(--font-serif);
        font-style: italic;
        color: var(--text-muted);
    }
    body.editorial-v2 .country-card.filter-hidden { display: none !important; }
    body.editorial-v2 .region-section.filter-hidden { display: none !important; }

    /* FAQ uses .faq-section / .faq-item from scams.css directly */

    /* Methodology */
    body.editorial-v2 .methodology-block {
        max-width: 760px;
        margin: 0 auto;
        padding: 0 1.5rem;
    }
    body.editorial-v2 .methodology-block ol {
        list-style: none;
        counter-reset: step;
        padding: 0;
        display: flex;
        flex-direction: column;
        gap: 0.9rem;
        margin-top: 1rem;
    }
    body.editorial-v2 .methodology-block ol li {
        counter-increment: step;
        position: relative;
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        padding: 1rem 1.25rem 1rem 3.5rem;
    }
    body.editorial-v2 .methodology-block ol li::before {
        content: "0" counter(step);
        position: absolute;
        left: 1.1rem;
        top: 1rem;
        font-family: var(--font-serif);
        font-size: 1rem;
        font-weight: 600;
        color: var(--terracotta);
        letter-spacing: 0.05em;
    }
    body.editorial-v2 .methodology-block ol li strong {
        font-family: var(--font-serif);
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--indigo);
        display: block;
        margin-bottom: 0.2rem;
    }
    body.editorial-v2 .methodology-block ol li p {
        font-size: 0.92rem;
        color: var(--text-muted);
        line-height: 1.5;
        margin: 0;
    }

    /* Floating emergency panel */
    .emergency-fab {
        position: fixed;
        right: 1.25rem;
        bottom: 1.25rem;
        z-index: 100;
        background: var(--terracotta);
        color: white;
        border: none;
        width: 54px;
        height: 54px;
        border-radius: 50%;
        font-size: 1.5rem;
        cursor: pointer;
        box-shadow: 0 6px 20px rgba(196, 112, 75, 0.35);
        transition: transform 0.2s, background 0.2s;
    }
    .emergency-fab:hover { background: var(--terracotta-deep); transform: scale(1.05); }
    .emergency-panel {
        position: fixed;
        right: 1.25rem;
        bottom: 5.5rem;
        z-index: 100;
        max-width: 340px;
        width: calc(100vw - 2.5rem);
        background: var(--white);
        border: 1px solid var(--sand);
        border-radius: var(--radius-lg);
        box-shadow: 0 10px 40px rgba(45, 58, 92, 0.18);
        padding: 1.25rem 1.35rem 1rem;
    }
    .emergency-panel[hidden] { display: none; }
    .emergency-panel h3 {
        font-family: var(--font-serif);
        font-size: 1.15rem;
        font-weight: 600;
        color: var(--indigo);
        margin: 0 0 0.75rem;
    }
    .emergency-panel dl { margin: 0; }
    .emergency-panel dt {
        font-family: var(--font-sans);
        font-size: 0.7rem;
        font-weight: 700;
        color: var(--earth);
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-top: 0.6rem;
    }
    .emergency-panel dt:first-child { margin-top: 0; }
    .emergency-panel dd {
        margin: 0.1rem 0 0;
        font-family: var(--font-serif);
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--indigo);
    }
    .emergency-panel .panel-note {
        font-family: var(--font-serif);
        font-style: italic;
        font-size: 0.85rem;
        color: var(--text-muted);
        line-height: 1.5;
        margin-top: 0.9rem;
        padding-top: 0.75rem;
        border-top: 1px solid var(--sand);
    }
    .emergency-panel .panel-note a { color: var(--terracotta); font-style: normal; font-weight: 600; text-decoration: none; }
    .emergency-panel .panel-close {
        position: absolute;
        top: 0.5rem;
        right: 0.6rem;
        background: none;
        border: none;
        font-size: 1.25rem;
        color: var(--text-muted);
        cursor: pointer;
        line-height: 1;
        padding: 0.25rem;
    }

    @media (max-width: 768px) {
        body.editorial-v2 .filter-row-label { min-width: 0; width: 100%; margin-bottom: 0.15rem; }
        body.editorial-v2 .country-grid { grid-template-columns: 1fr; }
        .emergency-fab { right: 1rem; bottom: 1rem; }
        .emergency-panel { right: 1rem; bottom: 4.75rem; max-width: calc(100vw - 2rem); }
    }
    </style>
<!-- @include:shared-head:start -->
<link rel="stylesheet" href="/assets/shared-shell.css">
<meta name="theme-color" content="#2D3A5C">
<script defer src="/assets/shared-shell.js"></script>
<!-- @include:shared-head:end -->
</head>
<body class="editorial-v2">

<!-- @include:nav:start -->
<nav>
    <a href="/" class="logo"><img class="owl-default" src="https://img.tabiji.ai/tabiji-owl-logo.png" alt="tabiji.ai" style="height:32px;" loading="lazy"><img class="owl-fly" src="https://img.tabiji.ai/tabiji-owl-logo-flying.png?v=2" alt="" style="height:32px;">tabiji<span>.ai</span></a>
    <button class="hamburger" onclick="document.querySelector('.nav-links').classList.toggle('open')" aria-label="Menu">☰</button>
    <div class="nav-links">
        <div class="nav-dropdown">
            <button class="nav-dropdown-toggle" onclick="this.parentElement.classList.toggle('open')">Explore</button>
            <div class="nav-dropdown-menu">
                <a href="/countries/">🗺 Country Guides</a>
                <a href="/compare/">🆚 Compare Destinations</a>
                <a href="/find/">🔍 Destination Finder</a>
                <a href="/health/">🏥 Travel Health Tips</a>
                <a href="/api/">🔌 API</a>
            </div>
        </div>
        <a href="/trip-planner/">Trip Planner</a>
        <a href="/scams/">Tourist Scams</a>
        <a href="/about/">About</a>
        <a href="/books/" class="cta-nav">Get Travel Safety Books</a>
    </div>
</nav>
<!-- @include:nav:end -->

<div class="breadcrumb"><a href="/">Home</a><span>›</span>Travel Health</div>

<main>

  <div class="hero">
    <div class="hero-badge">🏥 Travel Health Research</div>
    <h1>Travel health, country by country. <em>The meds, the numbers, the reality-check.</em></h1>
    <p>Emergency numbers, pharmacy language, restricted medications, vaccinations, water safety, and US health-insurance reality-checks — for __TOTAL_COUNTRIES__ countries.</p>
    <div class="stats-bar">
      <div class="stat"><strong>__TOTAL_COUNTRIES__</strong>Countries</div>
      <div class="stat"><strong>15</strong>US Insurance Carriers</div>
      <div class="stat"><strong>Monthly</strong>Editorial Review</div>
      <div class="stat"><strong>Free</strong>Always</div>
    </div>
  </div>

  <div class="reviewer-strip">
    <strong>Researched by the tabiji editorial team.</strong> Cross-referenced against CDC Travelers' Health, WHO International Travel and Health, IATA Travel Centre, US State Department, and national health-ministry sources. Last full review: __REVIEW_DATE__. This is not personal medical advice — confirm anything safety-critical with a travel-medicine clinician before you go. <a href="#methodology">How we build these guides →</a>
  </div>

  <!-- MODULE 1 — Going somewhere soon? -->
  <section class="module-section quick-lookup-wrap" id="quick-lookup">
    <span class="section-eyebrow">Going somewhere soon?</span>
    <h2>One-line <em>reality check</em> by destination.</h2>
    <p class="lede">Start with the single thing most travelers land not knowing. Tap a chip, or jump to the full country guide.</p>
    <div class="lookup-chip-row">
__LOOKUP_CHIPS__
    </div>
    <div class="quick-result" id="quick-result" hidden>
      <span class="quick-result-label" id="quick-result-label">Heads up</span>
      <span class="quick-result-country" id="quick-result-country"></span>
      <p class="quick-result-body" id="quick-result-body"></p>
      <a id="quick-result-link" href="#">Read the full health guide →</a>
    </div>
  </section>

  <!-- MODULE 2 — Seasonal alerts -->
  <section class="module-section" id="alerts">
    <span class="section-eyebrow">Current alerts · __REVIEW_DATE__</span>
    <h2>What's <em>actually circulating</em> right now.</h2>
    <p class="lede">Refreshed monthly from WHO Disease Outbreak News, CDC Health Alert Network, ECDC, and regional press. Not every advisory will affect your trip — skim for your destination.</p>
    <ul class="alerts-list">
__ALERTS__
    </ul>
  </section>

  <!-- MODULE 3 — Editor lists -->
  <section class="module-section" id="editor-lists">
    <span class="section-eyebrow">Editor's lists</span>
    <h2>The <em>non-obvious</em> stuff.</h2>
    <p class="lede">Three things that catch travelers off guard more than anything else. Start here if you haven't traveled internationally in a while.</p>
    <div class="browse-grid">
__EDITOR_LISTS__
    </div>
  </section>

  <!-- Medevac spotlight (target of editor-list card 2) -->
  <section class="module-section" id="medevac-spotlight">
    <span class="section-eyebrow">Medevac spotlight</span>
    <h2>5 countries where a <em>helicopter call-out</em> could run six figures.</h2>
    <p class="lede">These destinations have a pattern in common: limited specialist care, no nearby regional hub, and terrain that turns a hospital run into an air evacuation. Buy insurance that covers the full medevac cost band ($50K–250K) — not a $10K ceiling that won't move you.</p>
    <div class="medevac-list">
__MEDEVAC__
    </div>
  </section>

  <!-- MODULE 4 — Risk matrix filters -->
  <section class="module-section" id="risk-matrix">
    <span class="section-eyebrow">Filter the directory</span>
    <h2>Find countries by <em>specific risk</em>.</h2>
    <p class="lede">Narrow __TOTAL_COUNTRIES__ countries to the ones that match your trip. Filters combine — pick tap-water caution + yellow-fever required to see the overlap.</p>
    <div class="filter-matrix">
      <div class="filter-row">
        <span class="filter-row-label">Tap water</span>
        <button class="filter-pill" data-filter="water" data-value="safe" type="button">✅ Safe</button>
        <button class="filter-pill" data-filter="water" data-value="caution" type="button">⚠️ Caution</button>
        <button class="filter-pill" data-filter="water" data-value="unsafe" type="button">❌ Unsafe</button>
      </div>
      <div class="filter-row">
        <span class="filter-row-label">Healthcare</span>
        <button class="filter-pill" data-filter="rating" data-value="top" type="button">★★★★+ Top tier</button>
        <button class="filter-pill" data-filter="rating" data-value="mid" type="button">★★★ Adequate</button>
        <button class="filter-pill" data-filter="rating" data-value="low" type="button">★★ or less · medevac country</button>
      </div>
      <div class="filter-row">
        <span class="filter-row-label">Vaccinations</span>
        <button class="filter-pill" data-filter="yf" data-value="1" type="button">💉 Yellow fever required</button>
      </div>
      <div class="filter-row">
        <span class="filter-row-label">Medications</span>
        <button class="filter-pill" data-filter="strict" data-value="1" type="button">🚫 Strict enforcement at customs</button>
      </div>
      <div class="filter-row">
        <span class="filter-row-label">Insurance</span>
        <button class="filter-pill" data-filter="insurance" data-value="required" type="button">🛡️ Required for entry</button>
      </div>
      <button class="filter-reset" id="filter-reset" type="button">Clear all filters</button>
    </div>
  </section>

  <!-- Directory -->
  <section class="module-section" id="directory">
    <span class="section-eyebrow">All __TOTAL_COUNTRIES__ countries</span>
    <h2>Browse by <em>region</em>.</h2>
    <p class="lede">Every country links to a full health guide — emergency numbers, hospitals, pharmacy phrases, medication restrictions, cash-price estimates, and medevac guidance.</p>
    <div class="search-section" style="margin:0 0 1rem;padding:0;max-width:680px;">
      <div class="search-wrap">
        <span class="search-icon">🔍</span>
        <input type="text" id="country-search" placeholder="Search countries… Japan, Thailand, Mexico" autocomplete="off">
      </div>
    </div>
    <div class="rating-legend">
      <strong>How we rate healthcare quality</strong>
      <span class="legend-star">★★★★★</span> Excellent — tier-1 hospitals, English-speaking, direct billing ·
      <span class="legend-star">★★★★</span> Very good — private hospitals strong, some language friction ·
      <span class="legend-star">★★★</span> Good — private care adequate, public system variable ·
      <span class="legend-star">★★</span> Limited — private clinics OK, complex care needs evacuation ·
      <span class="legend-star">★</span> Minimal — emergency-only, medevac essential for anything serious.
    </div>
  </section>

__REGIONS__

  <!-- FAQ -->
  <section class="module-section" id="faq">
    <span class="section-eyebrow">Frequently asked</span>
    <h2>Travel health, <em>answered</em>.</h2>
    <p class="lede">Twenty questions we get most often. Jump to the full country or carrier guide for the specifics.</p>
    <div class="faq-section">
__FAQS__
    </div>
  </section>

  <!-- Methodology -->
  <section class="module-section methodology-block" id="methodology">
    <span class="section-eyebrow">Methodology</span>
    <h2>How we build these <em>guides</em>.</h2>
    <p class="lede">The short version: multiple official sources per country, cross-referenced, dated, and reviewed on a monthly editorial cycle. Not a replacement for a travel-medicine consult — a starting point that saves you two hours of research.</p>
    <ol>
      <li><strong>Pull the official sources first.</strong><p>CDC Travelers' Health, WHO International Travel and Health, IATA Travel Centre, US State Department advisories, and the destination country's health ministry when English-language publications exist.</p></li>
      <li><strong>Cross-reference the volatile facts.</strong><p>Emergency numbers, entry vaccination rules, and restricted-medication lists change. Every data point is checked against at least two independent sources before it ships.</p></li>
      <li><strong>Rate healthcare quality conservatively.</strong><p>Five-star = tier-1 international hospitals with English-speaking staff and direct-billing relationships. One-star = emergency-only, medevac essential. We err toward the lower rating where evidence is mixed.</p></li>
      <li><strong>Review monthly; correct on demand.</strong><p>Full editorial pass every four weeks. Reader corrections at hello@tabiji.ai usually ship within 48 hours. Every page carries its last-updated date.</p></li>
      <li><strong>Disclose what we are and aren't.</strong><p>We are a travel-safety research team. We are not physicians. These guides save you time and flag risks — they do not replace a travel-medicine consult, and they are not a substitute for reading your own insurance plan's Summary of Benefits and Coverage.</p></li>
    </ol>
  </section>

  <!-- Correction CTA -->
  <div class="report-cta">
    <h3>Spot something <em>out of date?</em></h3>
    <p>Emergency numbers change. Medication rules change. Outbreaks come and go. Every correction gets read and usually shipped within 48 hours.</p>
    <a href="mailto:hello@tabiji.ai?subject=Health%20hub%20correction" class="report-cta-btn">Send a correction</a>
  </div>

</main>

<!-- Floating emergency reference -->
<button class="emergency-fab" id="emergency-fab" type="button" aria-label="Quick emergency reference" aria-expanded="false">🚨</button>
<div class="emergency-panel" id="emergency-panel" role="dialog" aria-label="Emergency numbers" hidden>
  <button class="panel-close" id="panel-close" type="button" aria-label="Close">×</button>
  <h3>🚨 Emergency — fast reference</h3>
  <dl>
    <dt>European Union &amp; most of Europe</dt><dd>112</dd>
    <dt>United States &amp; Canada</dt><dd>911</dd>
    <dt>United Kingdom</dt><dd>999 or 112</dd>
    <dt>Australia</dt><dd>000 or 112</dd>
    <dt>Japan</dt><dd>119 ambulance · 110 police</dd>
    <dt>Mobile fallback anywhere on GSM</dt><dd>112</dd>
  </dl>
  <p class="panel-note">Your destination isn't listed? Use the search above to jump to the country page — every guide opens with its exact emergency numbers. Mental-health crisis? <a href="https://findahelpline.com/" target="_blank" rel="noopener">findahelpline.com</a> lists crisis lines in 130+ countries.</p>
</div>

<!-- @include:footer:start -->
<footer>
  <div class="footer-inner">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="/" class="footer-logo">tabiji<span>.ai</span></a>
        <p class="footer-tagline">Travel safety, country by country.</p>
      </div>
      <div class="footer-col">
        <h4>Explore</h4>
        <ul>
          <li><a href="/books/">Travel Safety Books</a></li>
          <li><a href="/scams/">Tourist Scams</a></li>
          <li><a href="/countries/">Country Guides</a></li>
          <li><a href="/trip-planner/">Trip Planner</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Follow</h4>
        <ul>
          <li><a href="https://www.instagram.com/tabiji.ai/" target="_blank" rel="noopener">Instagram</a></li>
          <li><a href="https://www.youtube.com/@tabijiai" target="_blank" rel="noopener">YouTube</a></li>
          <li><a href="https://www.pinterest.com/tabijiai/" target="_blank" rel="noopener">Pinterest</a></li>
          <li><a href="https://x.com/tabijiai" target="_blank" rel="noopener">X</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <ul>
          <li><a href="/about/">About</a></li>
          <li><a href="/media/">Media Studio</a></li>
          <li><a href="/api/">API</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-legal">
      <p class="footer-copyright">© 2026 tabiji.ai</p>
      <div class="footer-legal-links">
        <a href="/terms/">Terms of Service</a><span class="footer-sep" aria-hidden="true">·</span><a href="/privacy/">Privacy Policy</a><span class="footer-sep" aria-hidden="true">·</span><a href="/delete-data/">Delete My Data</a>
      </div>
    </div>
  </div>
</footer>
<!-- @include:footer:end -->

<script>
(function() {
  "use strict";

  /* ---------- Quick lookup (Module 1) ---------- */
  var QUICK_WARNINGS = __QUICK_WARNINGS_JS__;
  var COUNTRY_NAMES = {};
  document.querySelectorAll('.country-card[data-country]').forEach(function(card) {
    var slug = card.getAttribute('href').replace(/\/health\/|\//g, '');
    COUNTRY_NAMES[slug] = card.getAttribute('data-country');
  });

  function showQuickLookup(slug) {
    var warn = QUICK_WARNINGS[slug];
    if (!warn) return;
    var resultBox = document.getElementById('quick-result');
    document.getElementById('quick-result-country').textContent = COUNTRY_NAMES[slug] || slug;
    document.getElementById('quick-result-body').textContent = warn;
    document.getElementById('quick-result-link').setAttribute('href', '/health/' + slug + '/');
    resultBox.hidden = false;
  }
  document.querySelectorAll('.lookup-chip').forEach(function(btn) {
    btn.addEventListener('click', function() { showQuickLookup(btn.getAttribute('data-slug')); });
  });

  /* ---------- Country search (directory) ---------- */
  var searchInput = document.getElementById('country-search');
  if (searchInput) {
    searchInput.addEventListener('input', function(e) {
      var q = e.target.value.toLowerCase().trim();
      document.querySelectorAll('.country-card').forEach(function(card) {
        var name = (card.getAttribute('data-country') || '').toLowerCase();
        card.classList.toggle('filter-hidden', q.length > 0 && !name.includes(q));
      });
      updateRegionVisibility();
    });
  }

  /* ---------- Risk matrix filters (Module 4) ---------- */
  var activeFilters = {};  // { 'water': Set(['safe']), ... }

  function ratingBucket(stars) {
    stars = parseInt(stars, 10) || 0;
    if (stars >= 4) return 'top';
    if (stars === 3) return 'mid';
    return 'low';
  }

  function applyFilters() {
    document.querySelectorAll('.country-card').forEach(function(card) {
      var show = true;
      Object.keys(activeFilters).forEach(function(key) {
        var vals = activeFilters[key];
        if (!vals || vals.size === 0) return;
        var cardVal;
        if (key === 'rating') cardVal = ratingBucket(card.getAttribute('data-rating'));
        else if (key === 'water') cardVal = card.getAttribute('data-water');
        else if (key === 'insurance') cardVal = card.getAttribute('data-insurance');
        else if (key === 'yf') cardVal = card.getAttribute('data-yf');
        else if (key === 'strict') cardVal = card.getAttribute('data-strict');
        if (!vals.has(cardVal)) show = false;
      });
      card.classList.toggle('filter-hidden', !show);
    });
    updateRegionVisibility();
  }

  function updateRegionVisibility() {
    document.querySelectorAll('.region-section').forEach(function(section) {
      var visible = section.querySelectorAll('.country-card:not(.filter-hidden)').length;
      section.classList.toggle('filter-hidden', visible === 0);
    });
  }

  document.querySelectorAll('.filter-pill[data-filter]').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var key = btn.getAttribute('data-filter');
      var val = btn.getAttribute('data-value');
      if (!activeFilters[key]) activeFilters[key] = new Set();
      if (activeFilters[key].has(val)) {
        activeFilters[key].delete(val);
        btn.classList.remove('active');
      } else {
        activeFilters[key].add(val);
        btn.classList.add('active');
      }
      applyFilters();
      // Scroll to directory after first filter use
      document.getElementById('directory').scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  var resetBtn = document.getElementById('filter-reset');
  if (resetBtn) {
    resetBtn.addEventListener('click', function() {
      activeFilters = {};
      document.querySelectorAll('.filter-pill.active').forEach(function(b) { b.classList.remove('active'); });
      if (searchInput) searchInput.value = '';
      document.querySelectorAll('.country-card.filter-hidden, .region-section.filter-hidden').forEach(function(el) { el.classList.remove('filter-hidden'); });
    });
  }

  /* ---------- FAQ accordion ---------- */
  document.querySelectorAll('.faq-q').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var item = btn.parentElement;
      var open = item.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  /* ---------- Emergency floating panel ---------- */
  var fab = document.getElementById('emergency-fab');
  var panel = document.getElementById('emergency-panel');
  var panelClose = document.getElementById('panel-close');
  function togglePanel(open) {
    if (open === undefined) open = panel.hidden;
    panel.hidden = !open;
    fab.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  if (fab) fab.addEventListener('click', function() { togglePanel(); });
  if (panelClose) panelClose.addEventListener('click', function() { togglePanel(false); });
  document.addEventListener('keydown', function(e) { if (e.key === 'Escape' && !panel.hidden) togglePanel(false); });
})();
</script>

</body>
</html>
"""


def main():
    hub_html = EXISTING_HUB.read_text()
    regions = parse_regions(hub_html)
    meta = parse_card_metadata(hub_html)
    build_api(regions, meta)
    build_hub(regions, meta)


if __name__ == "__main__":
    main()
