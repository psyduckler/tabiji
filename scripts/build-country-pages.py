#!/usr/bin/env python3
"""
build-country-pages.py — Rebuild all 210 /health/{slug}/index.html pages in
editorial-v2 from the canonical /health-data/*.json sources.

What's preserved from the previous design:
    Emergency numbers, healthcare system description, quality rating + notes,
    hospitals list with phone/neighborhood, pharmacy hours/access/tips,
    OTC list, pharmacy chains, local drug-name map, pharmacy phrases,
    restricted medications, dental care, travel insurance notes, cash prices,
    medical evacuation, vaccinations, water + food safety, mental health,
    accessibility, COVID status, sources, last-updated date.

What's new in the rebuild (closes editor-audit gaps):
    - Editorial-v2 shell (Newsreader serif hero, reviewer strip, disclaimer)
    - Prominent "Not medical advice" red disclaimer
    - Top-risks module above-the-fold (curated for ~40 destinations, derived
      from JSON for the rest)
    - Raw-data leaks fixed (`very_easy` → "Very easy"; rating int → stars+label)
    - Star rating rendered inline (★★★★☆ Very Good)
    - travel.state.gov linked in sources
    - Cross-links to /health/medications/{slug}/ tier-1 pages when the country
      restricts a tier-1 medication
    - Cross-links to /health/insurance/ carrier guides
    - Floating emergency FAB with country-specific number + tel:
    - Per-country FAQ (generated from data)
    - MedicalWebPage + BreadcrumbList + FAQPage schema graph
    - Sticky TOC sidebar + mobile dropdown
    - Copy-to-clipboard on emergency number and pharmacy phrases

Usage:
    python3 scripts/build-country-pages.py                # all 210
    python3 scripts/build-country-pages.py japan thailand # specific slugs
"""

import html
import json
import re
import sys
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from lib.editorial import REVIEW_DATE, apply_replacements, render_faq_accordion, render_faqs_schema  # noqa: E402
from lib.country_risks import top_risks_for  # noqa: E402

ROOT = SCRIPT_DIR.parent
HEALTH_DATA = ROOT / "health-data"
OUT_DIR = ROOT / "health"


# -------------------------------------------------------------------
# Shared constants
# -------------------------------------------------------------------

# Slugs where yellow fever vaccination is required for entry (imported from
# health-hub constants for consistency).
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

STRICT_MEDS_SLUGS = {
    "japan", "uae", "singapore", "saudi-arabia", "south-korea", "thailand",
    "mexico", "indonesia", "china", "russia", "egypt", "qatar", "kuwait",
    "bahrain", "oman", "iran", "malaysia",
}

# Tier-1 medication pattern → slug for cross-linking. Keep in sync with
# scripts/lib/medication_content.py.
TIER1_PATTERNS = [
    ("adderall", ["adderall", "adhd", "amphetamine", "ritalin", "methylphenidate"]),
    ("sudafed", ["sudafed", "pseudoephedrine"]),
    ("codeine", ["codeine"]),
    ("cbd", ["cbd", "cannabis", "cannabinoid"]),
    ("tramadol", ["tramadol"]),
    ("xanax", ["benzodiazepine", "xanax", "alprazolam", "diazepam", "valium", "clonazepam", "lorazepam"]),
    ("opioids", ["opioid", "narcotic", "oxycodone", "hydrocodone", "morphine", "fentanyl"]),
]

# Display names for tier-1 slugs — .title() gives "Cbd" which looks wrong
# for an acronym. Override where the default wouldn't be right.
TIER1_DISPLAY_NAMES = {
    "cbd": "CBD",
}

# Slug → travel.state.gov URL path override for countries whose State Dept
# page name doesn't match the default `slug.title().replace("-","")` pattern.
# Verified with curl sweep against live state.gov endpoints.
# `None` means no State Dept advisory exists for that destination (US / US
# territories are the home country and get no inbound advisory).
STATE_GOV_URL_OVERRIDES = {
    "united-states": None,
    "puerto-rico": None,
    "united-states-virgin-islands": None,
    "antigua-and-barbuda": "AntiguaandBarbuda",
    "bosnia-and-herzegovina": "BosniaandHerzegovina",
    "cape-verde": "CaboVerde",
    "czech-republic": "Czechia",
    "dr-congo": "DemocraticRepublicoftheCongoDRC",
    "gambia": "TheGambia",
    "guinea-bissau": "Guinea-Bissau",
    "ivory-coast": "CotedIvoire",
    "micronesia": "FederatedStatesOfMicronesia",
    "myanmar": "Burma",
    "north-korea": "KoreaDemocraticPeoplesRepublicof",
    "north-macedonia": "Macedonia",
    "republic-of-the-congo": "RepublicoftheCongo",
    "russia": "RussianFederation",
    "saint-kitts-and-nevis": "SaintKittsandNevis",
    "saint-vincent-and-the-grenadines": "SaintVincentandtheGrenadines",
    "sao-tome-and-principe": "SaoTomeandPrincipe",
    "syria": "SyrianArabRepublic",
    "timor-leste": "Timor-Leste",
    "tokelau": "NewZealand",
    "trinidad-and-tobago": "TrinidadandTobago",
    "uae": "UnitedArabEmirates",
}


def state_gov_url(slug: str):
    """Return the valid travel.state.gov URL for this country, or None if
    no State Department advisory is available (US + US territories)."""
    if slug in STATE_GOV_URL_OVERRIDES:
        path = STATE_GOV_URL_OVERRIDES[slug]
        if path is None:
            return None
    else:
        path = slug.title().replace("-", "")
    return (
        "https://travel.state.gov/content/travel/en/international-travel/"
        f"International-Travel-Country-Information-Pages/{path}.html"
    )

# Source-name → canonical URL for the Sources section. Applied when the
# source line matches by loose string containment.
SOURCE_URLS = {
    "CDC": "https://wwwnc.cdc.gov/travel",
    "CDC Travelers": "https://wwwnc.cdc.gov/travel",
    "CDC Yellow Book": "https://wwwnc.cdc.gov/travel/yellowbook",
    "WHO": "https://www.who.int/travel-advice",
    "World Health Organization": "https://www.who.int/travel-advice",
    "IATA": "https://www.iatatravelcentre.com/",
    "IAMAT": "https://www.iamat.org/",
    "NaTHNaC": "https://travelhealthpro.org.uk/",
    "Travel Health Pro": "https://travelhealthpro.org.uk/",
    "ECDC": "https://www.ecdc.europa.eu/",
}

# Healthcare system type → friendly display label
HEALTHCARE_SYSTEM_LABELS = {
    "universal": "Universal public",
    "public": "Public-dominant",
    "mixed": "Mixed public/private",
    "private": "Private-dominant",
    "limited": "Limited",
}

PHARMACY_ACCESS_LABELS = {
    "very_easy": "Very easy",
    "easy": "Easy",
    "moderate": "Moderate",
    "limited": "Limited",
    "very_limited": "Very limited",
    "difficult": "Difficult",
}

QUALITY_LABELS = {1: "Very Limited", 2: "Limited", 3: "Good", 4: "Very Good", 5: "Excellent"}

REGION_BY_ISO = None  # populated lazily from the existing hub


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def friendly_pharmacy_access(value: str) -> str:
    return PHARMACY_ACCESS_LABELS.get((value or "").lower(), (value or "").replace("_", " ").title())


def friendly_healthcare_system(value: str) -> str:
    return HEALTHCARE_SYSTEM_LABELS.get((value or "").lower(), (value or "").replace("_", " ").title())


def star_rating(n: int) -> str:
    n = int(n) if n is not None else 3
    return "★" * n + "☆" * (5 - n)


def friendly_quality(n: int) -> str:
    return QUALITY_LABELS.get(int(n or 3), "Unrated")


def friendly_water(value: str) -> str:
    return {
        "safe": "Safe to drink",
        "caution": "Use caution",
        "unsafe": "Not safe — bottled only",
    }.get((value or "").lower(), (value or "Unknown").title())


def water_tone(value: str) -> str:
    return {"safe": "safe", "caution": "caution", "unsafe": "danger"}.get((value or "").lower(), "info")


def first_emergency_number(phone: str):
    """Extract the first bare emergency number from a descriptive string like
    '1669 (ambulance/fire), 191 (police), 1155 (Tourist Police — English-speaking)'.
    Strips parenthetical explanations first so '112 (EU emergency...)' doesn't get
    skipped for the later '116 117 (medical on-call)' number."""
    if not phone:
        return None
    cleaned = re.sub(r'\([^)]*\)', '', phone)
    m = re.search(r'\b(\+?\d{3,5}(?:[\s\-]\d{3,4})?)\b', cleaned)
    return m.group(1).strip() if m else None


def tel_uri(phone: str):
    """Return a tel: URI for the first emergency number in a descriptive string,
    or None."""
    num = first_emergency_number(phone)
    if not num:
        return None
    digits = re.sub(r'[^\d+]', '', num)
    return f"tel:{digits}" if len(digits) >= 3 else None


def linkify_source(name: str):
    """Return the URL for a known source name, or None."""
    n = name.lower()
    for key, url in SOURCE_URLS.items():
        if key.lower() in n:
            return url
    return None


def matching_tier1_meds(restricted_meds):
    """Return list of tier-1 slugs the country's restrictedMeds matches."""
    out = []
    for slug, patterns in TIER1_PATTERNS:
        for m in restricted_meds:
            name = (m.get("name") or "").lower()
            if any(p in name for p in patterns):
                out.append(slug)
                break
    return out


# -------------------------------------------------------------------
# Renderers — one per section
# -------------------------------------------------------------------

def render_quick_facts(d: dict) -> str:
    emergency = d.get("emergencyNumber", "")
    water = (d.get("waterSafety") or "").lower()
    rating = d.get("qualityRating", 3)
    pharmacy_access = d.get("pharmacyAccess", "")
    sys_type = d.get("healthcareSystemType", "")

    tel = tel_uri(emergency)
    emergency_html = html.escape(emergency)
    if tel:
        emergency_html = f'<a href="{tel}" class="emergency-link">{emergency_html}</a>'

    return (
        '  <div class="quick-facts">\n'
        f'    <div class="qf-tile"><div class="qf-label">Emergency</div>'
        f'<div class="qf-value qf-emergency">{emergency_html}</div></div>\n'
        f'    <div class="qf-tile qf-water qf-water-{water_tone(water)}"><div class="qf-label">Tap water</div>'
        f'<div class="qf-value">{html.escape(friendly_water(water))}</div></div>\n'
        f'    <div class="qf-tile"><div class="qf-label">Healthcare quality</div>'
        f'<div class="qf-value"><span class="stars">{star_rating(rating)}</span> '
        f'<span class="rating-label">{html.escape(friendly_quality(rating))}</span></div></div>\n'
        f'    <div class="qf-tile"><div class="qf-label">Pharmacy access</div>'
        f'<div class="qf-value">{html.escape(friendly_pharmacy_access(pharmacy_access))}</div></div>\n'
        f'    <div class="qf-tile"><div class="qf-label">System</div>'
        f'<div class="qf-value qf-value-small">{html.escape(friendly_healthcare_system(sys_type))}</div></div>\n'
        '  </div>'
    )


def render_top_risks(risks) -> str:
    out = []
    for r in risks:
        tone = r["tone"]
        title = html.escape(r["title"])
        body = html.escape(r["body"])
        out.append(
            f'    <div class="risk-card risk-{tone}">'
            f'<strong class="risk-title">{title}</strong>'
            f'<p>{body}</p></div>'
        )
    return "\n".join(out)


def render_hospitals(hospitals) -> str:
    if not hospitals:
        return "<p>No specific hospital recommendations on file for this destination. Ask your travel insurer for a vetted list on arrival.</p>"
    out = []
    for h in hospitals:
        name = html.escape(h.get("name", ""))
        area = html.escape(h.get("nearTouristArea", ""))
        phone = h.get("phone", "").strip()
        tel = tel_uri(phone)
        phone_html = f'<a href="{tel}">{html.escape(phone)}</a>' if tel else html.escape(phone)
        english = '<span class="badge-english">🗣️ English-speaking</span>' if h.get("englishSpeaking") else ""
        notes = html.escape(h.get("notes", ""))
        out.append(
            '      <div class="hospital-card">\n'
            f'        <div class="hospital-head"><strong>{name}</strong> {english}</div>\n'
            f'        <div class="hospital-meta">📍 {area} · 📞 {phone_html}</div>\n'
            f'        <p>{notes}</p>\n'
            '      </div>'
        )
    return "\n".join(out)


def render_otc_list(otc) -> str:
    if not otc:
        return ""
    items = "\n".join(f'        <li>{html.escape(x)}</li>' for x in otc)
    return f'      <ul class="otc-list">\n{items}\n      </ul>'


def render_pharmacy_phrases(phrases) -> str:
    if not phrases:
        return ""
    out = []
    for entry in phrases[:8]:
        meaning = (entry.get("meaning") or "").strip()
        phrase = (entry.get("phrase") or "").strip()
        local = (entry.get("local") or "").strip()
        if meaning and phrase and meaning != phrase:
            english, native = meaning, phrase
        elif phrase and local and phrase != local:
            english, native = phrase, local
        else:
            english, native = meaning or phrase or local or "", phrase or local or ""
        m = re.match(r'^(.*?)\s*\(([^)]+)\)\s*$', (native or "").strip(), re.DOTALL)
        pron = None
        if m:
            native, pron = m.group(1).strip(), m.group(2).strip()
        if native and native != english:
            pron_html = f' <em>({html.escape(pron)})</em>' if pron else ""
            out.append(f'        <li><strong>{html.escape(english)}:</strong> {html.escape(native)}{pron_html}</li>')
        else:
            pron_html = f' <em>({html.escape(pron)})</em>' if pron else ""
            out.append(f'        <li><strong>{html.escape(english or native)}</strong>{pron_html}</li>')
    return f'      <ul class="pharmacy-phrases">\n' + "\n".join(out) + "\n      </ul>"


def render_pharmacy_chains(chains) -> str:
    if not chains:
        return ""
    out = []
    for c in chains:
        name = html.escape(c.get("name", ""))
        where = html.escape(c.get("where", ""))
        identifier = html.escape(c.get("identifier", ""))
        out.append(
            f'        <li><strong>{name}</strong> — {identifier} <em>({where})</em></li>'
        )
    return f'      <ul class="chain-list">\n' + "\n".join(out) + "\n      </ul>"


def render_drug_name_map(dmap) -> str:
    if not dmap:
        return ""
    rows = []
    for d in dmap:
        generic = html.escape(d.get("generic", ""))
        local = html.escape(d.get("localName", ""))
        note = html.escape(d.get("note", ""))
        rows.append(
            f'        <li><strong>{generic}</strong> → <em>{local}</em>'
            + (f'<br><span class="drug-note">{note}</span>' if note else "")
            + "</li>"
        )
    return f'      <ul class="drug-map">\n' + "\n".join(rows) + "\n      </ul>"


def render_restricted_meds(meds, tier1_slugs) -> str:
    if not meds:
        return "<p>No notable medication restrictions on file. Always verify your specific prescriptions with the destination's embassy before flying.</p>"
    tier1_links = ""
    if tier1_slugs:
        links = " · ".join(
            f'<a href="/health/medications/{s}/">{TIER1_DISPLAY_NAMES.get(s, s.replace("-", " ").title())}</a>'
            for s in tier1_slugs
        )
        tier1_links = (
            f'      <p class="tier1-crosslinks">'
            f'<strong>Deep-dive guides for this country\'s restrictions:</strong> {links}</p>\n'
        )
    rows = []
    for m in meds:
        name = html.escape(m.get("name", ""))
        status = (m.get("status") or "").lower()
        note = html.escape(m.get("note", ""))
        rows.append(
            f'        <div class="med-row">'
            f'<span class="med-status status-{status}">{status.title() if status else ""}</span>'
            f'<div class="med-info"><strong>{name}</strong>'
            + (f'<p>{note}</p>' if note else "")
            + "</div></div>"
        )
    return tier1_links + '      <div class="med-list">\n' + "\n".join(rows) + "\n      </div>"


def render_vaccinations(vax) -> str:
    if not vax:
        return ""
    required = vax.get("required") or []
    recommended = vax.get("recommended") or []
    notes = vax.get("notes", "")
    out = []
    if required:
        out.append('      <h3>Required</h3>\n      <ul>\n' + "\n".join(f'        <li>{html.escape(v)}</li>' for v in required) + '\n      </ul>')
    if recommended:
        out.append('      <h3>Recommended</h3>\n      <ul>\n' + "\n".join(f'        <li>{html.escape(v)}</li>' for v in recommended) + '\n      </ul>')
    if notes:
        out.append(f'      <p class="vax-notes">{html.escape(notes)}</p>')
    if not out:
        out.append("<p>No mandatory vaccinations on file. Ensure routine vaccinations are up to date.</p>")
    return "\n".join(out)


def render_travel_insurance(ti, claim_process) -> str:
    if not ti:
        return ""
    avg_cost = ti.get("averageCost", "")
    tips = ti.get("tips", "")
    required = ti.get("required")
    required_note = ti.get("requiredNote", "")
    badge = ""
    if required:
        badge = '<span class="ins-badge ins-required">🛡️ Required for entry</span>'
    elif ti.get("recommended"):
        badge = '<span class="ins-badge ins-recommended">🛡️ Recommended</span>'
    out = []
    out.append(f'      <p>{badge}' + (f' {html.escape(required_note)}' if required and required_note else "") + "</p>")
    if avg_cost:
        out.append(f'      <p><strong>Average cost:</strong> {html.escape(avg_cost)}</p>')
    if tips:
        out.append(f'      <p class="ins-tip">{html.escape(tips)}</p>')
    if claim_process:
        out.append(f'      <h3>Filing a claim</h3>\n      <p>{html.escape(claim_process)}</p>')
    out.append('      <p class="ins-crosslink"><a href="/health/insurance/">→ See our carrier-by-carrier guide for 15 US insurers</a></p>')
    return "\n".join(out)


def render_common_costs(cc) -> str:
    if not cc:
        return ""
    rows = [
        ("Doctor visit (private)", cc.get("doctorVisit")),
        ("ER visit", cc.get("erVisit")),
        ("Overnight hospital stay", cc.get("overnightStay")),
        ("Ambulance", cc.get("ambulance")),
    ]
    items = "\n".join(
        f'        <tr><td>{html.escape(label)}</td><td>{html.escape(val)}</td></tr>'
        for label, val in rows if val
    )
    note = cc.get("note", "")
    return (
        '      <table class="cost-table">\n'
        '        <thead><tr><th>Service</th><th>Cost</th></tr></thead>\n'
        '        <tbody>\n' + items + '\n        </tbody>\n      </table>\n'
        + (f'      <p class="cost-note">{html.escape(note)}</p>' if note else "")
    )


def render_medevac(me) -> str:
    if not me:
        return ""
    rows = []
    for label, key in [
        ("Primary destination", "primaryDestination"),
        ("Secondary destination", "secondaryDestination"),
        ("Typical cost band", "typicalCost"),
    ]:
        val = me.get(key)
        if val:
            rows.append(f'      <p><strong>{label}:</strong> {html.escape(val)}</p>')
    providers = me.get("providers") or []
    if providers:
        rows.append(f'      <p><strong>Common providers:</strong> {html.escape(", ".join(providers))}</p>')
    note = me.get("note", "")
    if note:
        rows.append(f'      <p class="medevac-note">{html.escape(note)}</p>')
    return "\n".join(rows)


def render_dental(dc) -> str:
    if not dc:
        return ""
    out = []
    for label, key in [
        ("Availability", "availability"),
        ("Cost range", "costRange"),
    ]:
        v = dc.get(key)
        if v:
            out.append(f'      <p><strong>{label}:</strong> {html.escape(v)}</p>')
    if dc.get("notes"):
        out.append(f'      <p>{html.escape(dc["notes"])}</p>')
    if dc.get("emergencyTip"):
        out.append(f'      <div class="dental-emergency"><strong>🦷 Dental emergency:</strong> {html.escape(dc["emergencyTip"])}</div>')
    return "\n".join(out)


def render_mental_health(mh) -> str:
    if not mh:
        return ""
    out = []
    if mh.get("crisisLine"):
        out.append(f'      <div class="crisis-line"><strong>🆘 Local crisis line:</strong> {html.escape(mh["crisisLine"])}</div>')
    if mh.get("internationalLine"):
        out.append(f'      <p><strong>English / international line:</strong> {html.escape(mh["internationalLine"])}</p>')
    if mh.get("englishTherapists"):
        out.append(f'      <p><strong>English-speaking therapists:</strong> {html.escape(mh["englishTherapists"])}</p>')
    if mh.get("notes"):
        out.append(f'      <p>{html.escape(mh["notes"])}</p>')
    out.append('      <p class="mh-findahelpline">International crisis support: <a href="https://findahelpline.com/" target="_blank" rel="noopener">findahelpline.com</a> — crisis lines in 130+ countries.</p>')
    return "\n".join(out)


def render_accessibility(ai) -> str:
    if not ai:
        return ""
    out = []
    if ai.get("overview"):
        out.append(f'      <p>{html.escape(ai["overview"])}</p>')
    for label, key in [
        ("Hospital accessibility", "hospitalAccess"),
        ("Accessible transport", "transport"),
    ]:
        v = ai.get(key)
        if v:
            out.append(f'      <p><strong>{label}:</strong> {html.escape(v)}</p>')
    if ai.get("tips"):
        out.append(f'      <p class="a11y-tip">{html.escape(ai["tips"])}</p>')
    return "\n".join(out)


def render_covid(cs) -> str:
    if not cs:
        return ""
    out = []
    for label, key in [
        ("Entry requirements", "entryRequirements"),
        ("Mask policy", "maskPolicy"),
        ("Testing availability", "testing"),
    ]:
        v = cs.get(key)
        if v:
            out.append(f'      <p><strong>{label}:</strong> {html.escape(v)}</p>')
    if cs.get("notes"):
        out.append(f'      <p>{html.escape(cs["notes"])}</p>')
    return "\n".join(out)


def render_sources(sources, country_slug) -> str:
    out = []
    # Include travel.state.gov as the first entry when a valid advisory URL
    # exists for this country (skipped for US + US territories).
    sg_url = state_gov_url(country_slug)
    if sg_url:
        out.append(
            f'        <li><a href="{sg_url}" target="_blank" rel="noopener">'
            f'US Department of State — travel advisory for this country</a></li>'
        )
    if not sources:
        out.append('        <li>CDC Yellow Book 2026</li>')
        out.append('        <li>WHO International Travel and Health</li>')
    else:
        for s in sources:
            url = linkify_source(s)
            if url:
                out.append(f'        <li><a href="{url}" target="_blank" rel="noopener">{html.escape(s)}</a></li>')
            else:
                out.append(f'        <li>{html.escape(s)}</li>')
    return "\n".join(out)


def build_faqs(d: dict) -> list:
    slug = d.get("countrySlug")
    name = d.get("countryName", "").rstrip(".")
    emergency = d.get("emergencyNumber", "")
    water = (d.get("waterSafety") or "").lower()
    quality = d.get("qualityRating", 3)
    vax = d.get("vaccinations") or {}
    meds = d.get("restrictedMeds") or []

    faqs = []
    # Strip trailing period from the raw emergency string so we don't end up with
    # "...many areas.. For..." when the source already ends the clause with a period.
    emergency_clean = (emergency or "").rstrip(". ")
    faqs.append({
        "q": f"What's the emergency number in {name}?",
        "a": f"{emergency_clean}. For non-emergency travel medical assistance, your travel insurance provider's 24/7 assistance line can locate an English-speaking doctor and arrange direct billing where possible.",
    })
    if water == "unsafe":
        faqs.append({
            "q": f"Can I drink the tap water in {name}?",
            "a": f"No. Tap water in {name} is not safe for drinking. Use bottled or properly filtered water, skip ice at budget venues, and brush your teeth with bottled water if the local supply is questionable.",
        })
    elif water == "caution":
        faqs.append({
            "q": f"Is the tap water safe in {name}?",
            "a": f"Tap water safety varies regionally in {name}. Major cities typically treat water adequately, but rural areas and older infrastructure can be unreliable. When in doubt, bottled water is a cheap insurance policy.",
        })
    elif water == "safe":
        faqs.append({
            "q": f"Is the tap water safe in {name}?",
            "a": f"Yes. Tap water in {name} is safe for drinking and brushing teeth. Public fountains in major cities are also typically potable.",
        })
    if meds:
        faqs.append({
            "q": f"What medications are restricted in {name}?",
            "a": "Several common prescription and OTC medications face restrictions — see the Medications section on this page for the full list. Always carry prescriptions in original packaging with a doctor's letter.",
        })
    if quality <= 2:
        faqs.append({
            "q": f"Should I get travel insurance for {name}?",
            "a": "Yes — essential. Healthcare infrastructure is limited, and serious cases typically require medical evacuation to a regional hub. Insurance with $250K+ evacuation coverage is the baseline.",
        })
    elif quality <= 3:
        faqs.append({
            "q": f"Should I get travel insurance for {name}?",
            "a": "Recommended. Private hospitals handle routine care well; complex cases may need evacuation. Insurance with solid evacuation coverage is worth the premium.",
        })
    if vax.get("required"):
        faqs.append({
            "q": f"Do I need vaccinations for {name}?",
            "a": f"{name} has mandatory vaccination requirements — see the Vaccinations section on this page. Required vaccines must typically be administered 10+ days before travel and documented on an International Certificate of Vaccination (yellow card).",
        })
    faqs.append({
        "q": f"How do I find an English-speaking doctor in {name}?",
        "a": "Start with your travel insurer's 24/7 assistance line — most maintain vetted provider lists. The US embassy in-country also publishes lists of English-speaking physicians. International-focused hospitals (listed in the Hospitals section above) always have English-speaking staff.",
    })
    return faqs


# -------------------------------------------------------------------
# Schema
# -------------------------------------------------------------------

def build_schema(d: dict, faqs: list, today: str) -> dict:
    slug = d.get("countrySlug")
    name = d.get("countryName", "")
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "MedicalWebPage",
                "name": f"Travel Health Guide for {name}",
                "headline": f"Travel health, meds, and insurance for {name}",
                "description": d.get("metaDescription") or (
                    f"Travel health guide for {name} — emergency numbers, hospitals, pharmacy access, "
                    "restricted medications, vaccinations, water safety, medical evacuation, and US "
                    "health-insurance reality-checks."
                ),
                "url": f"https://tabiji.ai/health/{slug}/",
                "inLanguage": "en",
                "about": {"@type": "MedicalCondition", "name": "Travel medicine"},
                "specialty": "TravelMedicine",
                "audience": {"@type": "PeopleAudience", "audienceType": "International travelers"},
                "reviewedBy": {
                    "@type": "Organization",
                    "name": "tabiji editorial team",
                    "url": "https://tabiji.ai/about/",
                },
                "datePublished": d.get("datePublished") or "2026-03-01",
                "dateModified": d.get("lastUpdated") or today,
                "lastReviewed": today,
                "publisher": {
                    "@type": "Organization",
                    "name": "tabiji.ai",
                    "url": "https://tabiji.ai",
                    "logo": {"@type": "ImageObject", "url": "https://img.tabiji.ai/tabiji-owl-logo.png"},
                },
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tabiji.ai/"},
                    {"@type": "ListItem", "position": 2, "name": "Travel Health", "item": "https://tabiji.ai/health/"},
                    {"@type": "ListItem", "position": 3, "name": name, "item": f"https://tabiji.ai/health/{slug}/"},
                ],
            },
            {"@type": "FAQPage", "mainEntity": render_faqs_schema(faqs)},
        ],
    }


# -------------------------------------------------------------------
# Main render
# -------------------------------------------------------------------

def build_page(d: dict, today: str) -> str:
    slug = d["countrySlug"]
    name = d["countryName"]
    flag = d.get("flag", "")
    meta_desc = d.get("metaDescription") or (
        f"Travel health guide for {name} — emergency numbers, hospitals, pharmacy access, restricted medications, vaccinations, water safety, medical evacuation, and US health-insurance tips."
    )

    meds = d.get("restrictedMeds") or []
    tier1 = matching_tier1_meds(meds)
    yf_required = slug in YF_REQUIRED_SLUGS
    strict_meds = slug in STRICT_MEDS_SLUGS

    risks = top_risks_for(slug, d, yf_required, strict_meds)
    faqs = build_faqs(d)
    schema_str = json.dumps(build_schema(d, faqs, today), ensure_ascii=False, indent=2)

    emergency_number = d.get("emergencyNumber", "")
    emergency_tel = tel_uri(emergency_number)
    fab_short = first_emergency_number(emergency_number) or "—"
    fab_html = (
        f'<a class="emergency-fab" href="{emergency_tel}" '
        f'aria-label="Call emergency services in {html.escape(name)}">'
        f'🚨 Call {html.escape(fab_short)}</a>'
        if emergency_tel
        else ""
    )

    replacements = {
        "__SLUG__": slug,
        "__NAME__": html.escape(name),
        "__FLAG__": flag,
        "__META_DESC__": html.escape(meta_desc),
        "__SCHEMA__": schema_str,
        "__REVIEW_DATE__": REVIEW_DATE,
        "__TODAY__": today,
        "__LAST_UPDATED__": html.escape(d.get("lastUpdated") or today),
        "__QUICK_FACTS__": render_quick_facts(d),
        "__TOP_RISKS__": render_top_risks(risks),
        "__OVERVIEW_SYSTEM__": html.escape(d.get("healthcareSystem", "")),
        "__QUALITY_STARS__": star_rating(d.get("qualityRating", 3)),
        "__QUALITY_LABEL__": html.escape(friendly_quality(d.get("qualityRating", 3))),
        "__QUALITY_NOTES__": html.escape(d.get("qualityNotes", "")),
        "__MEDICAL_TOURISM__": html.escape(d.get("medicalTourismNote", "")),
        "__HOSPITALS__": render_hospitals(d.get("hospitals") or []),
        "__PHARMACY_ACCESS__": html.escape(friendly_pharmacy_access(d.get("pharmacyAccess", ""))),
        "__PHARMACY_HOURS__": html.escape(d.get("pharmacyHours", "")),
        "__PRESCRIPTION_RULES__": html.escape(d.get("prescriptionRules", "")),
        "__PHARMACY_TIPS__": html.escape(d.get("pharmacyTips", "")),
        "__OTC_LIST__": render_otc_list(d.get("commonOTC") or []),
        "__PHARMACY_PHRASES__": render_pharmacy_phrases(d.get("pharmacyPhrases") or []),
        "__PHARMACY_CHAINS__": render_pharmacy_chains(d.get("pharmacyChains") or []),
        "__DRUG_NAME_MAP__": render_drug_name_map(d.get("drugNameMap") or []),
        "__BRING_DOCS__": html.escape(d.get("bringDocumentation", "")),
        "__RESTRICTED_MEDS__": render_restricted_meds(meds, tier1),
        "__DENTAL__": render_dental(d.get("dentalCare") or {}),
        "__TRAVEL_INSURANCE__": render_travel_insurance(d.get("travelInsurance") or {}, d.get("insuranceClaimProcess", "")),
        "__COMMON_COSTS__": render_common_costs(d.get("commonCosts") or {}),
        "__MEDEVAC__": render_medevac(d.get("medicalEvacuation") or {}),
        "__VACCINATIONS__": render_vaccinations(d.get("vaccinations") or {}),
        "__WATER_SAFETY_BADGE__": html.escape(friendly_water(d.get("waterSafety", ""))),
        "__WATER_NOTES__": html.escape(d.get("waterNotes", "")),
        "__FOOD_SAFETY__": html.escape(d.get("foodSafetyTips", "")),
        "__MENTAL_HEALTH__": render_mental_health(d.get("mentalHealth") or {}),
        "__ACCESSIBILITY__": render_accessibility(d.get("accessibilityInfo") or {}),
        "__COVID__": render_covid(d.get("covidStatus") or {}),
        "__SOURCES__": render_sources(d.get("sources") or [], slug),
        "__FAQS__": render_faq_accordion(faqs, id_prefix=f"{slug}-faq"),
        "__EMERGENCY_FAB__": fab_html,
    }

    return apply_replacements(PAGE_TEMPLATE, replacements)


# -------------------------------------------------------------------
# Template — kept at module bottom for readability
# -------------------------------------------------------------------

PAGE_TEMPLATE = r"""<!DOCTYPE html>
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
    <title>__NAME__ Travel Health Guide — Meds, Hospitals, Insurance | tabiji.ai</title>
    <meta name="description" content="__META_DESC__">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="https://tabiji.ai/health/__SLUG__/">
    <meta property="og:title" content="__NAME__ Travel Health Guide — tabiji.ai">
    <meta property="og:description" content="__META_DESC__">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://tabiji.ai/health/__SLUG__/">
    <meta property="og:image" content="https://img.tabiji.ai/tabiji-owl-logo.png">
    <meta property="og:site_name" content="tabiji.ai">

    <script type="application/ld+json">__SCHEMA__</script>

    <link rel="stylesheet" href="/assets/scams.css">
    <style>
    body.editorial-v2 .reviewer-strip,
    body.editorial-v2 .med-disclaimer {
        max-width: 860px;
        margin: 1rem auto 0;
        padding: 1rem 1.5rem;
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        font-family: var(--font-serif);
        font-style: italic;
        font-size: 0.95rem;
        color: var(--text-muted);
        line-height: 1.5;
    }
    body.editorial-v2 .reviewer-strip { border-left: 4px solid var(--sage); }
    body.editorial-v2 .reviewer-strip strong { font-style: normal; color: var(--indigo); }
    body.editorial-v2 .reviewer-strip a { color: var(--terracotta); text-decoration: none; font-style: normal; font-weight: 600; border-bottom: 1px solid transparent; }
    body.editorial-v2 .reviewer-strip a:hover { border-bottom-color: var(--terracotta); }
    body.editorial-v2 .med-disclaimer {
        background: #FEF2F2;
        border: 1px solid #FCA5A5;
        border-left: 4px solid var(--ed-high-text);
        color: #7F1D1D;
        font-style: normal;
    }
    body.editorial-v2 .med-disclaimer strong { color: #7F1D1D; }

    body.editorial-v2 .quick-facts {
        max-width: 1100px;
        margin: 2rem auto 0;
        padding: 0 1.5rem;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 0.85rem;
    }
    body.editorial-v2 .qf-tile {
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        padding: 0.85rem 1rem;
    }
    body.editorial-v2 .qf-water.qf-water-safe { border-left: 4px solid var(--low); }
    body.editorial-v2 .qf-water.qf-water-caution { border-left: 4px solid var(--ed-med-text); }
    body.editorial-v2 .qf-water.qf-water-danger { border-left: 4px solid var(--ed-high-text); }
    body.editorial-v2 .qf-label {
        font-family: var(--font-sans);
        font-size: 0.7rem;
        font-weight: 700;
        color: var(--earth);
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 0.2rem;
    }
    body.editorial-v2 .qf-value {
        font-family: var(--font-serif);
        font-size: 1rem;
        font-weight: 600;
        color: var(--indigo);
        line-height: 1.3;
    }
    body.editorial-v2 .qf-value-small { font-size: 0.9rem; }
    body.editorial-v2 .qf-value .stars { color: var(--terracotta); letter-spacing: 0.05em; margin-right: 0.25rem; }
    body.editorial-v2 .qf-value .rating-label { font-style: italic; color: var(--text-muted); font-weight: 500; }
    body.editorial-v2 .qf-emergency { font-variant-numeric: tabular-nums; }
    body.editorial-v2 .qf-emergency a { color: var(--indigo); text-decoration: none; border-bottom: 1px solid var(--terracotta); }

    body.editorial-v2 .layout {
        max-width: 1100px;
        margin: 2.5rem auto 0;
        padding: 0 1.5rem 4rem;
        display: grid;
        grid-template-columns: 220px 1fr;
        gap: 2.5rem;
        align-items: start;
    }
    body.editorial-v2 aside.toc {
        position: sticky;
        top: 90px;
    }
    body.editorial-v2 aside.toc h2 {
        font-family: var(--font-sans);
        font-size: 0.72rem;
        font-weight: 700;
        color: var(--earth);
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
    }
    body.editorial-v2 aside.toc ul { list-style: none; padding: 0; margin: 0; }
    body.editorial-v2 aside.toc li { border-left: 2px solid var(--sand); }
    body.editorial-v2 aside.toc a {
        display: block;
        padding: 0.3rem 0.7rem;
        color: var(--text-muted);
        font-family: var(--font-serif);
        font-size: 0.9rem;
        text-decoration: none;
    }
    body.editorial-v2 aside.toc a.active,
    body.editorial-v2 aside.toc a:hover { color: var(--terracotta); }
    body.editorial-v2 aside.toc li.active { border-left-color: var(--terracotta); }
    body.editorial-v2 .toc-mobile {
        display: none;
        max-width: 1100px;
        margin: 1.5rem auto 0;
        padding: 0 1.5rem;
    }
    body.editorial-v2 .toc-mobile details {
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
    }
    body.editorial-v2 .toc-mobile summary {
        padding: 0.7rem 1rem;
        cursor: pointer;
        font-family: var(--font-sans);
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--indigo);
        list-style: none;
    }
    body.editorial-v2 .toc-mobile summary::after { content: " ▾"; color: var(--earth); }
    body.editorial-v2 .toc-mobile details[open] summary::after { content: " ▴"; }
    body.editorial-v2 .toc-mobile ul {
        list-style: none;
        padding: 0 1rem 0.75rem;
        margin: 0;
    }
    body.editorial-v2 .toc-mobile a {
        display: block;
        padding: 0.35rem 0;
        color: var(--text-muted);
        font-family: var(--font-serif);
        font-size: 0.92rem;
        text-decoration: none;
    }

    body.editorial-v2 article.main-col { min-width: 0; }
    body.editorial-v2 article.main-col section {
        margin-bottom: 2.5rem;
        padding-bottom: 2.25rem;
        border-bottom: 1px solid var(--sand);
    }
    body.editorial-v2 article.main-col section:last-of-type { border-bottom: none; }
    body.editorial-v2 article.main-col .section-eyebrow {
        display: inline-block;
        font-family: var(--font-sans);
        font-size: 0.72rem;
        font-weight: 700;
        color: var(--terracotta);
        letter-spacing: 0.22em;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
        position: relative;
        padding-top: 1.25rem;
    }
    body.editorial-v2 article.main-col .section-eyebrow::before {
        content: ''; position: absolute; top: 0; left: 0;
        width: 40px; height: 2px; background: var(--terracotta);
    }
    body.editorial-v2 article.main-col h2 {
        font-family: var(--font-serif);
        font-size: clamp(1.45rem, 2.5vw, 1.85rem);
        font-weight: 500;
        color: var(--indigo);
        letter-spacing: -0.01em;
        line-height: 1.2;
        margin-bottom: 0.9rem;
    }
    body.editorial-v2 article.main-col h2 em { font-style: italic; color: var(--terracotta); }
    body.editorial-v2 article.main-col h3 {
        font-family: var(--font-serif);
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--indigo);
        margin: 1.2rem 0 0.4rem;
    }
    body.editorial-v2 article.main-col p {
        font-family: var(--font-serif);
        font-size: 1rem;
        color: var(--text);
        line-height: 1.65;
        margin-bottom: 0.9rem;
    }
    body.editorial-v2 article.main-col ul { margin: 0 0 0.9rem 1.25rem; font-family: var(--font-serif); }
    body.editorial-v2 article.main-col li { margin-bottom: 0.35rem; line-height: 1.6; }

    /* Top-risks module */
    body.editorial-v2 .risk-card {
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        padding: 1rem 1.25rem;
        margin-bottom: 0.7rem;
    }
    body.editorial-v2 .risk-danger { border-left: 4px solid var(--ed-high-text); }
    body.editorial-v2 .risk-caution { border-left: 4px solid var(--ed-med-text); }
    body.editorial-v2 .risk-info { border-left: 4px solid var(--info); }
    body.editorial-v2 .risk-title {
        font-family: var(--font-serif);
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--indigo);
        display: block;
        margin-bottom: 0.3rem;
    }
    body.editorial-v2 .risk-card p {
        font-family: var(--font-serif);
        font-size: 0.95rem;
        color: var(--text-muted);
        line-height: 1.55;
        margin: 0;
    }

    /* Hospitals */
    body.editorial-v2 .hospital-card {
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        padding: 1rem 1.25rem;
        margin-bottom: 0.7rem;
    }
    body.editorial-v2 .hospital-head {
        font-family: var(--font-serif);
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--indigo);
        margin-bottom: 0.25rem;
        display: flex;
        gap: 0.5rem;
        align-items: center;
        flex-wrap: wrap;
    }
    body.editorial-v2 .badge-english {
        font-family: var(--font-sans);
        font-size: 0.72rem;
        font-weight: 600;
        background: var(--low-bg);
        color: var(--low);
        border-radius: var(--radius-pill);
        padding: 0.15rem 0.55rem;
    }
    body.editorial-v2 .hospital-meta {
        font-family: var(--font-serif);
        font-size: 0.88rem;
        color: var(--earth);
        margin-bottom: 0.4rem;
    }
    body.editorial-v2 .hospital-meta a { color: var(--terracotta); text-decoration: none; }

    /* Pharmacy */
    body.editorial-v2 .pharmacy-phrases li {
        line-height: 1.65;
    }
    body.editorial-v2 .pharmacy-phrases em {
        font-style: italic;
        color: var(--earth);
        font-size: 0.9em;
    }
    body.editorial-v2 .drug-map .drug-note {
        font-family: var(--font-serif);
        font-style: italic;
        color: var(--text-muted);
        font-size: 0.9em;
    }

    /* Restricted meds */
    body.editorial-v2 .tier1-crosslinks {
        background: var(--warm-cream-soft);
        border: 1px dashed var(--sand);
        border-radius: var(--radius-md);
        padding: 0.65rem 0.9rem;
        font-family: var(--font-serif);
        font-size: 0.92rem;
        color: var(--text-muted);
    }
    body.editorial-v2 .tier1-crosslinks a {
        color: var(--terracotta);
        text-decoration: none;
        font-weight: 600;
    }
    body.editorial-v2 .tier1-crosslinks a:hover { border-bottom: 1px solid var(--terracotta); }
    body.editorial-v2 .med-row {
        display: flex;
        gap: 0.75rem;
        padding: 0.5rem 0;
        border-top: 1px solid var(--sand);
        align-items: flex-start;
    }
    body.editorial-v2 .med-row:first-of-type { border-top: none; }
    body.editorial-v2 .med-status {
        flex-shrink: 0;
        font-family: var(--font-sans);
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 0.2rem 0.55rem;
        border-radius: var(--radius-pill);
        min-width: 7ch;
        text-align: center;
    }
    body.editorial-v2 .status-banned { background: #FEE2E2; color: #991B1B; }
    body.editorial-v2 .status-restricted, body.editorial-v2 .status-controlled { background: #FEF3D8; color: #92400E; }
    body.editorial-v2 .med-info strong {
        font-family: var(--font-serif);
        color: var(--indigo);
    }
    body.editorial-v2 .med-info p {
        font-size: 0.92rem;
        color: var(--text-muted);
        margin: 0.2rem 0 0;
    }

    /* Cost table */
    body.editorial-v2 .cost-table {
        width: 100%;
        border-collapse: collapse;
        margin: 0.5rem 0;
        font-family: var(--font-sans);
        font-size: 0.92rem;
    }
    body.editorial-v2 .cost-table th {
        background: var(--warm-cream);
        color: var(--earth);
        font-size: 0.72rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        text-align: left;
        padding: 0.6rem 0.85rem;
        border-bottom: 1px solid var(--sand);
    }
    body.editorial-v2 .cost-table td {
        padding: 0.55rem 0.85rem;
        border-bottom: 1px solid var(--sand);
    }
    body.editorial-v2 .cost-table td:last-child {
        font-family: var(--font-serif);
        color: var(--indigo);
        font-weight: 600;
    }
    body.editorial-v2 .cost-note {
        font-size: 0.85rem;
        color: var(--earth);
        font-style: italic;
        margin-top: 0.4rem;
    }

    /* Insurance */
    body.editorial-v2 .ins-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        font-family: var(--font-sans);
        font-size: 0.78rem;
        font-weight: 600;
        padding: 0.3rem 0.75rem;
        border-radius: var(--radius-pill);
    }
    body.editorial-v2 .ins-required { background: var(--ed-high-bg); color: var(--ed-high-text); }
    body.editorial-v2 .ins-recommended { background: var(--info-bg); color: var(--info); }
    body.editorial-v2 .ins-crosslink a {
        color: var(--terracotta);
        text-decoration: none;
        font-family: var(--font-sans);
        font-weight: 600;
    }

    /* Dental, crisis line, etc. */
    body.editorial-v2 .dental-emergency,
    body.editorial-v2 .crisis-line {
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-left: 4px solid var(--terracotta);
        border-radius: var(--radius-md);
        padding: 0.75rem 1rem;
        margin: 0.7rem 0;
        font-family: var(--font-serif);
    }

    /* Sources */
    body.editorial-v2 .sources-list {
        list-style: none;
        padding: 0;
        margin: 0.5rem 0 0;
    }
    body.editorial-v2 .sources-list li {
        padding: 0.45rem 0;
        border-bottom: 1px solid var(--sand);
        font-family: var(--font-serif);
        font-size: 0.95rem;
        color: var(--text-muted);
    }
    body.editorial-v2 .sources-list li:last-child { border-bottom: none; }
    body.editorial-v2 .sources-list a { color: var(--terracotta); text-decoration: none; border-bottom: 1px solid transparent; }
    body.editorial-v2 .sources-list a:hover { border-bottom-color: var(--terracotta); }

    /* Emergency FAB */
    .emergency-fab {
        position: fixed;
        right: 1.25rem;
        bottom: 1.25rem;
        z-index: 100;
        background: var(--ed-high-text);
        color: white;
        border-radius: var(--radius-pill);
        padding: 0.85rem 1.35rem;
        font-family: var(--font-sans);
        font-weight: 700;
        font-size: 0.85rem;
        text-decoration: none;
        box-shadow: 0 6px 20px rgba(143, 58, 42, 0.35);
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        max-width: calc(100vw - 2.5rem);
    }
    .emergency-fab:hover { background: #7f2f22; }

    @media (max-width: 900px) {
        body.editorial-v2 .layout { grid-template-columns: 1fr; gap: 1.5rem; }
        body.editorial-v2 aside.toc { display: none; }
        body.editorial-v2 .toc-mobile { display: block; }
    }
    @media print {
        nav, footer, .emergency-fab, .toc-mobile, aside.toc { display: none !important; }
        body { font-size: 11pt; }
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
                <a href="/popular-picks/">⭐ Popular Picks</a>
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

<div class="breadcrumb">
    <a href="/">Home</a><span>›</span><a href="/health/">Travel Health</a><span>›</span>__NAME__
</div>

<main>

  <div class="hero">
    <div class="hero-badge">__FLAG__ __NAME__ · Travel Health</div>
    <h1>Travel health for <em>__NAME__</em>.</h1>
    <p>Emergency numbers, hospital contacts, pharmacy language, restricted medications, vaccinations, water safety, and insurance realities — everything you need to know before you land.</p>
    <div class="hero-meta">
      <span>🕐 Last updated __LAST_UPDATED__</span>
    </div>
  </div>

  <div class="reviewer-strip">
    <strong>Researched by the tabiji editorial team.</strong> Cross-referenced against CDC Travelers' Health, CDC Yellow Book 2026, WHO International Travel and Health, IATA Travel Centre, US State Department travel advisories, and the destination's national health-ministry publications. Last full review: __REVIEW_DATE__. <a href="/health/#methodology">How we build these guides →</a>
  </div>

  <div class="med-disclaimer">
    <strong>⚠️ Not medical or legal advice.</strong> Travel health and medication rules change; enforcement varies. Always verify safety-critical information with a travel-medicine clinician and your destination's embassy or pharmaceutical authority before flying. This page is a starting point, not a substitute for a professional consult.
  </div>

__QUICK_FACTS__

  <div class="toc-mobile">
    <details>
      <summary>Jump to section</summary>
      <ul>
        <li><a href="#top-risks">Biggest risks for tourists</a></li>
        <li><a href="#healthcare">Healthcare overview</a></li>
        <li><a href="#hospitals">Hospitals &amp; clinics</a></li>
        <li><a href="#pharmacy">Pharmacy guide</a></li>
        <li><a href="#medications">Medication restrictions</a></li>
        <li><a href="#dental">Dental care</a></li>
        <li><a href="#insurance">Travel insurance</a></li>
        <li><a href="#costs">Cash prices</a></li>
        <li><a href="#medevac">Medical evacuation</a></li>
        <li><a href="#vaccinations">Vaccinations</a></li>
        <li><a href="#water-food">Water &amp; food safety</a></li>
        <li><a href="#mental-health">Mental health</a></li>
        <li><a href="#accessibility">Accessibility</a></li>
        <li><a href="#covid">COVID &amp; respiratory</a></li>
        <li><a href="#faq">FAQ</a></li>
        <li><a href="#sources">Sources</a></li>
      </ul>
    </details>
  </div>

  <div class="layout">

    <aside class="toc">
      <h2>On this page</h2>
      <ul>
        <li><a href="#top-risks">Top risks</a></li>
        <li><a href="#healthcare">Healthcare</a></li>
        <li><a href="#hospitals">Hospitals</a></li>
        <li><a href="#pharmacy">Pharmacy</a></li>
        <li><a href="#medications">Medications</a></li>
        <li><a href="#dental">Dental</a></li>
        <li><a href="#insurance">Insurance</a></li>
        <li><a href="#costs">Cash prices</a></li>
        <li><a href="#medevac">Medevac</a></li>
        <li><a href="#vaccinations">Vaccinations</a></li>
        <li><a href="#water-food">Water &amp; food</a></li>
        <li><a href="#mental-health">Mental health</a></li>
        <li><a href="#accessibility">Accessibility</a></li>
        <li><a href="#covid">COVID</a></li>
        <li><a href="#faq">FAQ</a></li>
        <li><a href="#sources">Sources</a></li>
      </ul>
    </aside>

    <article class="main-col">

      <section id="top-risks">
        <span class="section-eyebrow">Biggest risks for tourists</span>
        <h2>What <em>actually</em> happens to travelers here.</h2>
__TOP_RISKS__
      </section>

      <section id="healthcare">
        <span class="section-eyebrow">Healthcare overview</span>
        <h2>The <em>system</em>.</h2>
        <p><strong>System:</strong> __OVERVIEW_SYSTEM__</p>
        <p><strong>Quality:</strong> <span style="color:var(--terracotta);">__QUALITY_STARS__</span> <em>__QUALITY_LABEL__</em></p>
        <p>__QUALITY_NOTES__</p>
        <p><em>__MEDICAL_TOURISM__</em></p>
      </section>

      <section id="hospitals">
        <span class="section-eyebrow">Hospitals &amp; clinics</span>
        <h2>Where to <em>actually go</em>.</h2>
__HOSPITALS__
      </section>

      <section id="pharmacy">
        <span class="section-eyebrow">Pharmacy guide</span>
        <h2>Finding what you <em>need</em>.</h2>
        <p><strong>Access:</strong> __PHARMACY_ACCESS__</p>
        <p><strong>Hours:</strong> __PHARMACY_HOURS__</p>
        <p><strong>Prescription rules:</strong> __PRESCRIPTION_RULES__</p>
        <p>__PHARMACY_TIPS__</p>
        <h3>Available over the counter</h3>
__OTC_LIST__
        <h3>Useful pharmacy phrases</h3>
__PHARMACY_PHRASES__
        <h3>Chains you'll see</h3>
__PHARMACY_CHAINS__
        <h3>Common OTC medications by local brand</h3>
__DRUG_NAME_MAP__
      </section>

      <section id="medications">
        <span class="section-eyebrow">Medication restrictions</span>
        <h2>What you <em>can't</em> bring in.</h2>
        <p>__BRING_DOCS__</p>
__RESTRICTED_MEDS__
      </section>

      <section id="dental">
        <span class="section-eyebrow">Dental care</span>
        <h2>If something <em>breaks</em>.</h2>
__DENTAL__
      </section>

      <section id="insurance">
        <span class="section-eyebrow">Travel insurance</span>
        <h2>What you <em>actually need</em>.</h2>
__TRAVEL_INSURANCE__
      </section>

      <section id="costs">
        <span class="section-eyebrow">Cash prices</span>
        <h2>What it <em>costs</em> out of pocket.</h2>
__COMMON_COSTS__
      </section>

      <section id="medevac">
        <span class="section-eyebrow">Medical evacuation</span>
        <h2>When local <em>won't cut it</em>.</h2>
__MEDEVAC__
      </section>

      <section id="vaccinations">
        <span class="section-eyebrow">Vaccinations</span>
        <h2>What to <em>get done</em> before you fly.</h2>
__VACCINATIONS__
      </section>

      <section id="water-food">
        <span class="section-eyebrow">Water &amp; food safety</span>
        <h2>The <em>Bali belly</em> prevention guide.</h2>
        <p><strong>Tap water:</strong> __WATER_SAFETY_BADGE__ — __WATER_NOTES__</p>
        <h3>Food safety</h3>
        <p>__FOOD_SAFETY__</p>
      </section>

      <section id="mental-health">
        <span class="section-eyebrow">Mental health</span>
        <h2>In <em>crisis</em> abroad.</h2>
__MENTAL_HEALTH__
      </section>

      <section id="accessibility">
        <span class="section-eyebrow">Accessibility</span>
        <h2>Getting around with <em>mobility needs</em>.</h2>
__ACCESSIBILITY__
      </section>

      <section id="covid">
        <span class="section-eyebrow">COVID &amp; respiratory</span>
        <h2>Entry rules + <em>local status</em>.</h2>
__COVID__
      </section>

      <section id="faq">
        <span class="section-eyebrow">Frequently asked</span>
        <h2>__NAME__ travel health, <em>answered</em>.</h2>
        <div class="faq-section">
__FAQS__
        </div>
      </section>

      <section id="sources">
        <span class="section-eyebrow">Sources &amp; references</span>
        <h2>What we <em>checked</em>.</h2>
        <ul class="sources-list">
__SOURCES__
        </ul>
      </section>

    </article>

  </div>

  <div class="report-cta">
    <h3>Spot something <em>out of date?</em></h3>
    <p>Every correction gets read and usually ships within 48 hours.</p>
    <a href="mailto:hello@tabiji.ai?subject=__NAME__%20health%20correction" class="report-cta-btn">Send a correction</a>
  </div>

</main>

__EMERGENCY_FAB__

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
          <li><a href="/popular-picks/">Popular Picks</a></li>
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
  document.querySelectorAll('.faq-q').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var item = btn.parentElement;
      var open = item.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  var sections = document.querySelectorAll('article.main-col section');
  var tocLinks = document.querySelectorAll('aside.toc a, .toc-mobile a');
  if (sections.length && 'IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          var id = entry.target.id;
          tocLinks.forEach(function(l) {
            var match = l.getAttribute('href') === '#' + id;
            l.classList.toggle('active', match);
            if (l.parentElement) l.parentElement.classList.toggle('active', match);
          });
        }
      });
    }, { rootMargin: '-80px 0px -60% 0px', threshold: 0 });
    sections.forEach(function(s) { observer.observe(s); });
  }
})();
</script>

</body>
</html>
"""


# -------------------------------------------------------------------
# Driver
# -------------------------------------------------------------------

def main(slugs=None):
    today = date.today().isoformat()
    targets = []
    for p in sorted(HEALTH_DATA.glob("*.json")):
        try:
            d = json.loads(p.read_text())
        except Exception:
            continue
        if slugs and d.get("countrySlug") not in slugs:
            continue
        targets.append(d)

    if slugs:
        missing = set(slugs) - {d["countrySlug"] for d in targets}
        if missing:
            print(f"Unknown slugs: {', '.join(sorted(missing))}", file=sys.stderr)

    for d in targets:
        slug = d["countrySlug"]
        html_out = build_page(d, today)
        out_path = OUT_DIR / slug / "index.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html_out)
    print(f"Built {len(targets)} country pages.")


if __name__ == "__main__":
    args = sys.argv[1:]
    main(slugs=set(args) if args else None)
