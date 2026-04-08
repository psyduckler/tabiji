#!/usr/bin/env python3
"""
build-health-page.py — Build tabiji.ai health guide pages from template + JSON data.

Usage:
    python3 scripts/build-health-page.py JP        # builds /health/japan/
    python3 scripts/build-health-page.py --all     # builds all countries
    python3 scripts/build-health-page.py --list    # show available data files
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from html import escape

SCRIPT_DIR = Path(__file__).parent.resolve()
TABIJI_ROOT = SCRIPT_DIR.parent
TEMPLATE_PATH = TABIJI_ROOT / "docs" / "health-template.html"
DATA_DIR = TABIJI_ROOT / "health-data"
SAMPLE_DIR = TABIJI_ROOT  # for health-sample-japan.json fallback
OUTPUT_ROOT = TABIJI_ROOT / "health"

# Known source URLs for hyperlinking
SOURCE_URLS = {
    "CDC Travelers' Health": "https://wwwnc.cdc.gov/travel",
    "WHO International Travel and Health": "https://www.who.int/travel-advice",
    "European Commission — EHIC": "https://ec.europa.eu/social/main.jsp?catId=559",
    "European Commission — European Health Insurance Card": "https://ec.europa.eu/social/main.jsp?catId=559",
    "US Embassy Tokyo": "https://jp.usembassy.gov/",
    "US Embassy Vienna": "https://at.usembassy.gov/",
    "US Embassy Egypt": "https://eg.usembassy.gov/",
    "US Embassy Brazil": "https://br.usembassy.gov/",
    "US Embassy Phnom Penh": "https://kh.usembassy.gov/",
    "US Embassy London": "https://uk.usembassy.gov/",
    "US Embassy Paris": "https://fr.usembassy.gov/",
    "US Embassy Berlin": "https://de.usembassy.gov/",
    "US Embassy Rome": "https://it.usembassy.gov/",
    "US Embassy Madrid": "https://es.usembassy.gov/",
    "US Embassy Bangkok": "https://th.usembassy.gov/",
    "US Embassy New Delhi": "https://in.usembassy.gov/",
    "US Embassy Mexico City": "https://mx.usembassy.gov/",
    "US Embassy Seoul": "https://kr.usembassy.gov/",
    "US Embassy Singapore": "https://sg.usembassy.gov/",
    "US Embassy Hanoi": "https://vn.usembassy.gov/",
    "US Embassy Jakarta": "https://id.usembassy.gov/",
    "US Embassy Nairobi": "https://ke.usembassy.gov/",
    "US Embassy Canberra": "https://au.usembassy.gov/",
    "US Embassy Wellington": "https://nz.usembassy.gov/",
    "US Embassy Pretoria": "https://za.usembassy.gov/",
    "US Embassy Ottawa": "https://ca.usembassy.gov/",
    "US Embassy Bern": "https://ch.usembassy.gov/",
    "US Embassy Dublin": "https://ie.usembassy.gov/",
    "US Embassy Athens": "https://gr.usembassy.gov/",
    "US Embassy The Hague": "https://nl.usembassy.gov/",
    "US Embassy Lisbon": "https://pt.usembassy.gov/",
    "US Embassy Stockholm": "https://se.usembassy.gov/",
    "US Embassy Oslo": "https://no.usembassy.gov/",
    "US Embassy Warsaw": "https://pl.usembassy.gov/",
    "US Embassy Prague": "https://cz.usembassy.gov/",
    "US Embassy Budapest": "https://hu.usembassy.gov/",
    "US Embassy Zagreb": "https://hr.usembassy.gov/",
    "US Embassy Bucharest": "https://ro.usembassy.gov/",
    "US Embassy Reykjavik": "https://is.usembassy.gov/",
    "US Embassy Brussels": "https://be.usembassy.gov/",
    "US Embassy Bogota": "https://co.usembassy.gov/",
    "US Embassy Lima": "https://pe.usembassy.gov/",
    "US Embassy Buenos Aires": "https://ar.usembassy.gov/",
    "US Embassy San Jose": "https://cr.usembassy.gov/",
    "US Embassy Colombo": "https://lk.usembassy.gov/",
    "US Embassy Rabat": "https://ma.usembassy.gov/",
    "US Embassy Kuala Lumpur": "https://my.usembassy.gov/",
    "US Embassy Manila": "https://ph.usembassy.gov/",
    "US Embassy Ankara": "https://tr.usembassy.gov/",
    "US Embassy Amman": "https://jo.usembassy.gov/",
    "US Embassy Abu Dhabi": "https://ae.usembassy.gov/",
    "US Embassy Dar es Salaam": "https://tz.usembassy.gov/",
    "US Embassy Kathmandu": "https://np.usembassy.gov/",
    "US Embassy Tel Aviv": "https://il.usembassy.gov/",
    "Japan Ministry of Health, Labour and Welfare": "https://www.mhlw.go.jp/english/",
    "Austrian Federal Ministry of Social Affairs, Health, Care and Consumer Protection": "https://www.sozialministerium.at/en.html",
    "Egypt Ministry of Health": "https://www.mohp.gov.eg/",
    "Cambodia Ministry of Health": "https://moh.gov.kh/",
    "Brazil Ministry of Health (ANVISA)": "https://www.gov.br/anvisa/en",
    "UK NHS": "https://www.nhs.uk/",
    "NHS": "https://www.nhs.uk/",
    "France Ministry of Health": "https://sante.gouv.fr/",
    "German Federal Ministry of Health": "https://www.bundesgesundheitsministerium.de/en/",
    "Italy Ministry of Health": "https://www.salute.gov.it/",
    "Spain Ministry of Health": "https://www.sanidad.gob.es/en/home.htm",
    "Thailand Ministry of Public Health": "https://eng.moph.go.th/",
    "India Ministry of Health and Family Welfare": "https://main.mohfw.gov.in/",
    "Mexico Ministry of Health (Secretaría de Salud)": "https://www.gob.mx/salud",
    "South Korea Ministry of Health and Welfare": "https://www.mohw.go.kr/eng/",
    "Singapore Ministry of Health": "https://www.moh.gov.sg/",
    "Vietnam Ministry of Health": "https://moh.gov.vn/",
    "Indonesia Ministry of Health": "https://www.kemkes.go.id/",
    "Kenya Ministry of Health": "https://www.health.go.ke/",
    "South Africa Department of Health": "https://www.health.gov.za/",
    "New Zealand Ministry of Health": "https://www.health.govt.nz/",
    "Australia Department of Health": "https://www.health.gov.au/",
    "Canada Health Canada": "https://www.canada.ca/en/health-canada.html",
    "Swiss Federal Office of Public Health": "https://www.bag.admin.ch/bag/en/home.html",
    "IATA Travel Centre": "https://www.iata.org/en/programs/safety/health/",
    "WHO": "https://www.who.int/travel-advice",
    "WHO Ethiopia": "https://www.who.int/countries/eth",
    "WHO Ghana": "https://www.who.int/countries/gha",
    "WHO Lebanon": "https://www.who.int/countries/lbn",
    "WHO Myanmar": "https://www.who.int/countries/mmr",
    "WHO Nigeria": "https://www.who.int/countries/nga",
    "WHO Rwanda": "https://www.who.int/countries/rwa",
    "WHO Uganda": "https://www.who.int/countries/uga",
    "WHO Western Pacific": "https://www.who.int/westernpacific",
    "US Embassy Beijing": "https://china.usembassy-china.org.cn/",
    "US Embassy Copenhagen": "https://dk.usembassy.gov/",
    "US Embassy Helsinki": "https://fi.usembassy.gov/",
    "US Embassy Sofia": "https://bg.usembassy.gov/",
    "US Embassy Belgrade": "https://rs.usembassy.gov/",
    "US Embassy Podgorica": "https://me.usembassy.gov/",
    "US Embassy Tirana": "https://al.usembassy.gov/",
    "US Embassy Tbilisi": "https://ge.usembassy.gov/",
    "US Embassy Riga": "https://lv.usembassy.gov/",
    "US Embassy Vilnius": "https://lt.usembassy.gov/",
    "US Embassy Tallinn": "https://ee.usembassy.gov/",
    "US Embassy Bratislava": "https://sk.usembassy.gov/",
    "US Embassy Ljubljana": "https://si.usembassy.gov/",
    "US Embassy Nicosia": "https://cy.usembassy.gov/",
    "US Embassy Valletta": "https://mt.usembassy.gov/",
    "US Embassy Luxembourg": "https://lu.usembassy.gov/",
    "US Consulate Hong Kong": "https://hk.usconsulate.gov/",
    "American Institute in Taiwan": "https://www.ait.org.tw/",
    "US Embassy Vientiane": "https://la.usembassy.gov/",
    "US Embassy Yangon": "https://mm.usembassy.gov/",
    "US Embassy Ulaanbaatar": "https://mn.usembassy.gov/",
    "US Embassy (Sri Lanka, covering Maldives)": "https://lk.usembassy.gov/",
    "US Embassy Dhaka": "https://bd.usembassy.gov/",
    "US Embassy Islamabad": "https://pk.usembassy.gov/",
    "US Embassy Riyadh": "https://sa.usembassy.gov/",
    "US Embassy Oman": "https://om.usembassy.gov/",
    "US Embassy Doha": "https://qa.usembassy.gov/",
    "US Embassy Kuwait": "https://kw.usembassy.gov/",
    "US Embassy Beirut": "https://lb.usembassy.gov/",
    "Swiss Embassy Tehran (US interests section)": "https://www.eda.admin.ch/tehran",
    "US Embassy Abuja": "https://ng.usembassy.gov/",
    "US Embassy Accra": "https://gh.usembassy.gov/",
    "US Embassy Addis Ababa": "https://et.usembassy.gov/",
    "US Embassy Kigali": "https://rw.usembassy.gov/",
    "US Embassy Kampala": "https://ug.usembassy.gov/",
    "US Embassy Dakar": "https://sn.usembassy.gov/",
    "US Embassy Santiago": "https://cl.usembassy.gov/",
    "US Embassy Quito": "https://ec.usembassy.gov/",
    "US Embassy Santo Domingo": "https://do.usembassy.gov/",
    "US Embassy Kingston": "https://jm.usembassy.gov/",
    "US Embassy Panama": "https://pa.usembassy.gov/",
    "US Embassy Guatemala City": "https://gt.usembassy.gov/",
    "US Embassy La Paz": "https://bo.usembassy.gov/",
    "US Embassy Montevideo": "https://uy.usembassy.gov/",
    "US Embassy Asunción": "https://py.usembassy.gov/",
    "US Embassy Tegucigalpa": "https://hn.usembassy.gov/",
    "US Embassy San Salvador": "https://sv.usembassy.gov/",
    "US Embassy Suva": "https://fj.usembassy.gov/",
    "US Embassy Managua": "https://ni.usembassy.gov/",
    "China National Health Commission": "https://en.nhc.gov.cn/",
    "Danish Health Authority (Sundhedsstyrelsen)": "https://www.sst.dk/en",
    "Finnish Institute for Health and Welfare (THL)": "https://thl.fi/en",
    "Hong Kong Department of Health": "https://www.dh.gov.hk/",
    "Taiwan Centers for Disease Control": "https://www.cdc.gov.tw/En",
    "Saudi Ministry of Health": "https://www.moh.gov.sa/en/Pages/default.aspx",
    "Saudi Food & Drug Authority (SFDA)": "https://www.sfda.gov.sa/en",
    "Qatar Ministry of Public Health": "https://www.moph.gov.qa/english/Pages/default.aspx",
    "Hamad Medical Corporation": "https://www.hamad.qa/EN/",
    "Nigerian Centre for Disease Control (NCDC)": "https://ncdc.gov.ng/",
    "Rwanda Biomedical Centre": "https://rbc.gov.rw/",
    "Institut Pasteur de Dakar": "https://www.pasteur.sn/",
    "Lebanese Red Cross": "https://www.redcross.org.lb/",
}

# Country slug → countries page slug mapping
COUNTRY_PAGE_SLUGS = {
    "japan": "japan", "austria": "austria", "australia": "australia",
    "brazil": "brazil", "cambodia": "cambodia", "canada": "canada",
    "switzerland": "switzerland", "colombia": "colombia", "costa-rica": "costa-rica",
    "cuba": "cuba", "czechia": "czechia", "germany": "germany",
    "egypt": "egypt", "spain": "spain", "france": "france",
    "united-kingdom": "united-kingdom", "greece": "greece", "croatia": "croatia",
    "hungary": "hungary", "indonesia-bali": "indonesia", "ireland": "ireland",
    "israel": "israel", "india": "india", "iceland": "iceland",
    "italy": "italy", "jordan": "jordan", "kenya": "kenya",
    "south-korea": "south-korea", "sri-lanka": "sri-lanka", "morocco": "morocco",
    "mexico": "mexico", "malaysia": "malaysia", "netherlands": "netherlands",
    "norway": "norway", "nepal": "nepal", "new-zealand": "new-zealand",
    "peru": "peru", "philippines": "philippines", "poland": "poland",
    "portugal": "portugal", "sweden": "sweden", "singapore": "singapore",
    "thailand": "thailand", "turkey": "turkey", "tanzania": "tanzania",
    "vietnam": "vietnam", "south-africa": "south-africa",
    "united-arab-emirates": "united-arab-emirates", "argentina": "argentina",
    "belgium": "belgium",
}


def load_template() -> str:
    if not TEMPLATE_PATH.exists():
        sys.exit(f"ERROR: Template not found at {TEMPLATE_PATH}")
    return TEMPLATE_PATH.read_text(encoding="utf-8")


def find_data_file(iso2: str) -> Path:
    iso2 = iso2.upper()
    for name in [f"{iso2}.json", f"{iso2.lower()}.json"]:
        p = DATA_DIR / name
        if p.exists():
            return p
    # Check sample file
    sample = SAMPLE_DIR / f"health-sample-{iso2.lower()}.json"
    if sample.exists():
        return sample
    available = sorted(DATA_DIR.glob("*.json"))
    names = [f"  {p.stem}" for p in available if not p.stem.startswith("_")]
    sys.exit(
        f"ERROR: No data file for '{iso2}'.\n"
        f"Available:\n" + ("\n".join(names) if names else "  (none)")
    )


def load_data(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# ── HTML generators from structured data ─────────────────────────────────

def gen_healthcare_overview(d: dict) -> str:
    system = escape(d.get("healthcareSystem", d.get("healthcare_system", "")))
    notes = escape(d.get("qualityNotes", d.get("quality_notes", "")))
    rating = d.get("qualityRating", d.get("quality_rating", 3))
    if isinstance(rating, str):
        rating_html = escape(rating)
    else:
        stars = "★" * int(rating) + "☆" * (5 - int(rating))
        rating_html = f"{stars} ({rating}/5)"

    html = f'<h2>🏥 Healthcare Overview</h2>\n'
    html += f'<p><strong>System:</strong> {system}</p>\n'
    html += f'<p><strong>Quality:</strong> {rating_html}</p>\n'
    if notes:
        html += f'<p>{notes}</p>\n'

    tourism = d.get("medicalTourismNote", d.get("medical_tourism_note", ""))
    if tourism:
        html += f'<div class="callout callout-info"><p><strong>💡 Medical Tourism</strong></p><p>{escape(tourism)}</p></div>\n'
    return html


def gen_hospitals(d: dict) -> str:
    hospitals = d.get("hospitals", [])
    html = '<h2>🏨 Hospitals &amp; Clinics Near Tourist Areas</h2>\n'
    if not hospitals:
        html += '<p>Contact your hotel or accommodation for local hospital recommendations. In an emergency, call the local emergency number.</p>\n'
        return html

    html += '<p>Recommended facilities for travelers — English-speaking staff available at most listed locations.</p>\n'
    for h in hospitals:
        name = escape(h.get("name", ""))
        area = escape(h.get("nearTouristArea", h.get("area", "")))
        phone = escape(h.get("phone", ""))
        english = h.get("englishSpeaking", True)
        notes = escape(h.get("notes", ""))
        lang_badge = '<span class="badge badge-safe">🗣️ English spoken</span>' if english else '<span class="badge badge-caution">⚠️ Limited English</span>'

        html += '<div class="callout callout-info">\n'
        html += f'  <p><strong>{name}</strong> {lang_badge}</p>\n'
        if area:
            html += f'  <p>📍 Near: {area}</p>\n'
        if phone:
            html += f'  <p>📞 {phone}</p>\n'
        if notes:
            html += f'  <p>{notes}</p>\n'
        html += '</div>\n'
    return html


def gen_pharmacy_guide(d: dict) -> str:
    access = escape(d.get("pharmacyAccess", d.get("pharmacy_access", "")))
    hours = escape(d.get("pharmacyHours", d.get("pharmacy_hours", "")))
    tips = escape(d.get("pharmacyTips", d.get("pharmacy_tips", "")))
    rules = escape(d.get("prescriptionRules", d.get("prescription_rules", "")))
    otc = d.get("commonOTC", d.get("common_otc", []))
    phrases = d.get("pharmacyPhrases", [])

    html = '<h2>💊 Pharmacy Guide</h2>\n'
    if access:
        html += f'<p><strong>Access:</strong> {access}</p>\n'
    if hours:
        html += f'<p><strong>Hours:</strong> {hours}</p>\n'
    if rules:
        html += f'<p><strong>Prescription rules:</strong> {rules}</p>\n'
    if otc:
        html += '<h3>Available Over-the-Counter</h3>\n<ul>\n'
        for item in otc:
            html += f'  <li>{escape(str(item))}</li>\n'
        html += '</ul>\n'
    if phrases:
        html += '<h3>🗣️ Useful Pharmacy Phrases</h3>\n'
        html += '<div class="callout callout-tip"><p><strong>💡 Handy phrases at the pharmacy</strong></p>\n'
        html += '<ul>\n'
        for p in phrases:
            eng = escape(p.get("english", ""))
            local = escape(p.get("local", ""))
            translit = escape(p.get("transliteration", ""))
            line = f'  <li><strong>{eng}:</strong> {local}'
            if translit:
                line += f' <em>({translit})</em>'
            line += '</li>\n'
            html += line
        html += '</ul></div>\n'
    if tips:
        html += f'<div class="callout callout-tip"><p><strong>💡 Tips</strong></p><p>{tips}</p></div>\n'

    # Tier 2 additions: pharmacy chains + drug name translation map
    html += gen_pharmacy_chains(d)
    html += gen_drug_name_map(d)
    return html


# ── Tier 2 sub-section generators ────────────────────────────────────────

UNIVERSAL_PHARMACY_MARKER_HTML = (
    "Most pharmacies in this country are independent rather than chain-branded. "
    "Look for the universal pharmacy markers: a green cross sign in most of "
    "Europe and Latin America, a red &lsquo;A&rsquo; (Apotheke) in German-speaking "
    "countries, or local-language signage like apteka, lék&aacute;rna, or farmacia."
)


def gen_pharmacy_chains(d: dict) -> str:
    """Render the pharmacy chain block. Field is `pharmacyChains` (list).
    Empty list = render the universal-marker fallback. Missing field =
    render nothing (so existing pages without the data don't get a stub)."""
    chains = d.get("pharmacyChains")
    if chains is None:
        return ""
    html = '<h3>🏪 Pharmacy Chains You&rsquo;ll See</h3>\n'
    if not chains:
        html += f'<p>{UNIVERSAL_PHARMACY_MARKER_HTML}</p>\n'
        return html
    html += '<div class="callout callout-info"><p><strong>Look for these storefronts:</strong></p>\n<ul>\n'
    for c in chains:
        if not isinstance(c, dict):
            continue
        name = escape(c.get("name", ""))
        ident = escape(c.get("identifier", ""))
        where = escape(c.get("where", ""))
        line = f'  <li><strong>{name}</strong>'
        if ident:
            line += f' &mdash; {ident}'
        if where:
            line += f'. <em>{where}</em>'
        line += '</li>\n'
        html += line
    html += '</ul></div>\n'
    return html


def gen_drug_name_map(d: dict) -> str:
    """Render the drug name translation table. Helps travelers ask for the
    right OTC medication by local brand name."""
    dm = d.get("drugNameMap")
    if not dm:
        return ""
    html = '<h3>💊 Common OTC Medications by Local Brand</h3>\n'
    html += '<p>Knowing the local brand name makes asking for common over-the-counter medications much easier.</p>\n'
    html += '<div class="callout callout-tip"><ul>\n'
    for entry in dm:
        if not isinstance(entry, dict):
            continue
        generic = escape(entry.get("generic", ""))
        local = escape(entry.get("localName", ""))
        note = escape(entry.get("note", ""))
        html += f'  <li><strong>{generic}</strong> &rarr; <em>{local}</em>'
        if note:
            html += f'<br><span style="color:var(--text-muted);font-size:0.92em;">{note}</span>'
        html += '</li>\n'
    html += '</ul></div>\n'
    return html


def gen_common_costs(d: dict) -> str:
    """Render the cost cheat-sheet table. Used inside gen_insurance."""
    costs = d.get("commonCosts")
    if not isinstance(costs, dict):
        return ""
    rows = [
        ("Doctor visit (private clinic)", costs.get("doctorVisit", "")),
        ("ER visit (no admission)", costs.get("erVisit", "")),
        ("Overnight hospital stay", costs.get("overnightStay", "")),
        ("Ambulance call-out", costs.get("ambulance", "")),
    ]
    rows = [(label, val) for label, val in rows if val]
    if not rows:
        return ""
    note = escape(costs.get("note", ""))
    currency = escape(costs.get("currency", "USD"))
    html = '<h3>💵 Typical Out-of-Pocket Costs</h3>\n'
    html += '<div class="callout callout-info"><p><strong>Estimated cash prices ({}):</strong></p>\n'.format(currency)
    html += '<ul style="list-style:none;padding-left:0;">\n'
    for label, val in rows:
        html += f'  <li><strong>{escape(label)}:</strong> {escape(val)}</li>\n'
    html += '</ul>\n'
    if note:
        html += f'<p style="font-size:0.88em;color:var(--text-muted);margin-top:0.5rem;">{note}</p>\n'
    html += '</div>\n'
    return html


def gen_medical_evacuation(d: dict) -> str:
    """Render the medical-evacuation callout. Used inside gen_insurance."""
    evac = d.get("medicalEvacuation")
    if not isinstance(evac, dict):
        return ""
    primary = escape(evac.get("primaryDestination", ""))
    secondary = escape(evac.get("secondaryDestination", ""))
    cost = escape(evac.get("typicalCost", ""))
    note = escape(evac.get("note", ""))
    providers = evac.get("providers", [])

    html = '<h3>🚁 Medical Evacuation</h3>\n'
    html += '<div class="callout callout-warn">\n'
    if note:
        html += f'  <p>{note}</p>\n'
    if primary:
        html += f'  <p><strong>Primary destination:</strong> {primary}</p>\n'
    if secondary:
        html += f'  <p><strong>Secondary destination:</strong> {secondary}</p>\n'
    if cost:
        html += f'  <p><strong>Typical cost band:</strong> {cost}</p>\n'
    if providers:
        prov_str = ", ".join(escape(str(p)) for p in providers if p)
        html += (
            f'  <p><strong>Common providers:</strong> {prov_str} '
            '— compare current quotes and policy terms before relying on any '
            'single provider.</p>\n'
        )
    html += '</div>\n'
    return html


def gen_medications(d: dict) -> str:
    restricted = d.get("restrictedMeds", d.get("restricted_meds", []))
    docs = d.get("bringDocumentation", d.get("bring_documentation", ""))

    html = '<h2>💉 Medications &amp; Restrictions</h2>\n'
    if docs:
        html += f'<p>{escape(docs)}</p>\n'
    if restricted:
        html += '<h3>Controlled / Restricted Substances</h3>\n'
        html += '<div class="callout callout-danger"><p><strong>🚫 Watch out for these</strong></p><ul>\n'
        for med in restricted:
            if isinstance(med, dict):
                name = escape(med.get("name", ""))
                status = med.get("status", "restricted")
                note = escape(med.get("note", ""))
                badge = "🚫" if status == "banned" else "⚠️"
                html += f'  <li>{badge} <strong>{name}</strong>'
                if note:
                    html += f' — {note}'
                html += '</li>\n'
            else:
                html += f'  <li>⚠️ {escape(str(med))}</li>\n'
        html += '</ul></div>\n'
    return html


def gen_dental(d: dict) -> str:
    dental = d.get("dentalCare", {})
    html = '<h2>🦷 Dental Care</h2>\n'
    if not dental:
        html += '<p>Dental services are available in major cities. Contact your hotel for recommended dental clinics.</p>\n'
        return html

    avail = escape(dental.get("availability", ""))
    cost = escape(dental.get("costRange", ""))
    notes = escape(dental.get("notes", ""))
    emergency_tip = escape(dental.get("emergencyTip", ""))

    if avail:
        html += f'<p><strong>Availability:</strong> {avail}</p>\n'
    if cost:
        html += f'<p><strong>Typical cost range:</strong> {cost}</p>\n'
    if notes:
        html += f'<p>{notes}</p>\n'
    if emergency_tip:
        html += f'<div class="callout callout-warn"><p><strong>🦷 Dental emergency?</strong></p><p>{emergency_tip}</p></div>\n'
    return html


def gen_insurance(d: dict) -> str:
    ins = d.get("travelInsurance", d.get("travel_insurance", {}))
    if isinstance(ins, str):
        return f'<h2>🛡️ Travel Insurance</h2>\n<p>{escape(ins)}</p>\n'

    recommended = ins.get("recommended", True)
    required = ins.get("required", False)
    cost = escape(ins.get("averageCost", ins.get("average_cost", "")))
    tips = escape(ins.get("tips", ""))
    req_note = escape(ins.get("requiredNote", ins.get("required_note", "")))
    claim_process = escape(d.get("insuranceClaimProcess", ""))

    html = '<h2>🛡️ Travel Insurance</h2>\n'
    if required:
        html += '<div class="callout callout-warn"><p><strong>⚠️ Required</strong></p>'
        if req_note:
            html += f'<p>{req_note}</p>'
        html += '</div>\n'
    elif recommended:
        html += '<p><span class="badge badge-caution">⚠️ Strongly recommended</span></p>\n'
    else:
        html += '<p><span class="badge badge-safe">✅ Optional</span></p>\n'

    if cost:
        html += f'<p><strong>Average cost:</strong> {cost}</p>\n'
    if tips:
        html += f'<div class="callout callout-tip"><p><strong>💡 Tip</strong></p><p>{tips}</p></div>\n'

    if claim_process:
        html += '<h3>📋 How to File an Insurance Claim</h3>\n'
        html += f'<p>{claim_process}</p>\n'
    else:
        html += '<h3>📋 How to File an Insurance Claim</h3>\n'
        html += '<ol>\n'
        html += '  <li>Contact your insurance provider immediately — most require notification within 24-48 hours</li>\n'
        html += '  <li>Keep all receipts, medical reports, and prescriptions (request English copies)</li>\n'
        html += '  <li>Get a police report if theft or accident was involved</li>\n'
        html += '  <li>Take photos of all documents before submitting</li>\n'
        html += '  <li>File your claim within the deadline stated in your policy (usually 30-90 days)</li>\n'
        html += '</ol>\n'

    # Tier 2 additions: cost cheat sheet + medical evacuation block
    html += gen_common_costs(d)
    html += gen_medical_evacuation(d)
    return html


def gen_vaccinations(d: dict) -> str:
    vacc = d.get("vaccinations", {})
    if isinstance(vacc, str):
        return f'<h2>💉 Vaccinations</h2>\n<p>{escape(vacc)}</p>\n'

    required = vacc.get("required", [])
    recommended = vacc.get("recommended", [])
    notes = escape(vacc.get("notes", ""))

    html = '<h2>💉 Vaccinations</h2>\n'
    if required:
        html += '<h3>Required</h3>\n<ul>\n'
        for v in required:
            html += f'  <li>🔴 {escape(str(v))}</li>\n'
        html += '</ul>\n'
    if recommended:
        html += '<h3>Recommended</h3>\n<ul>\n'
        for v in recommended:
            html += f'  <li>🟡 {escape(str(v))}</li>\n'
        html += '</ul>\n'
    if not required and not recommended:
        html += '<p>No specific vaccinations required or recommended beyond routine immunizations.</p>\n'
    if notes:
        html += f'<p>{notes}</p>\n'
    return html


def gen_food_water(d: dict) -> str:
    safety = d.get("waterSafety", d.get("water_safety", ""))
    notes = escape(d.get("waterNotes", d.get("water_notes", "")))
    food_tips = escape(d.get("foodSafetyTips", d.get("food_safety_tips", "")))

    badge_map = {
        "safe": '<span class="badge badge-safe">✅ Tap water is safe to drink</span>',
        "caution": '<span class="badge badge-caution">⚠️ Use caution — bottled water recommended in some areas</span>',
        "boil": '<span class="badge badge-caution">⚠️ Boil water before drinking</span>',
        "unsafe": '<span class="badge badge-danger">❌ Tap water is NOT safe — drink bottled water only</span>',
        "bottled-only": '<span class="badge badge-danger">❌ Drink bottled water only</span>',
    }
    badge = badge_map.get(safety, f'<span class="badge">{escape(str(safety))}</span>')

    html = '<h2>🚰 Water &amp; Food Safety</h2>\n'
    html += f'<p>{badge}</p>\n'
    if notes:
        html += f'<p>{notes}</p>\n'
    if food_tips:
        html += f'<h3>Food Safety Tips</h3>\n<p>{food_tips}</p>\n'
    return html


def gen_mental_health(d: dict) -> str:
    mh = d.get("mentalHealth", {})
    html = '<h2>🧠 Mental Health Resources</h2>\n'
    if not mh:
        html += '<p>If you experience a mental health crisis while traveling, contact your embassy or consulate for assistance. Many international hotels can connect you with English-speaking counselors.</p>\n'
        return html

    crisis_line = escape(mh.get("crisisLine", ""))
    intl_line = escape(mh.get("internationalLine", ""))
    notes = escape(mh.get("notes", ""))
    english_therapists = escape(mh.get("englishTherapists", ""))

    if crisis_line:
        html += f'<div class="callout callout-danger"><p><strong>🆘 Crisis Line:</strong> {crisis_line}</p></div>\n'
    if intl_line:
        html += f'<p><strong>International crisis support:</strong> {intl_line}</p>\n'
    else:
        html += '<p><strong>International crisis support:</strong> <a href="https://findahelpline.com/" style="color:var(--terracotta);text-decoration:underline;">findahelpline.com</a> — worldwide directory of crisis lines</p>\n'
    if english_therapists:
        html += f'<p><strong>English-speaking therapists:</strong> {english_therapists}</p>\n'
    if notes:
        html += f'<p>{notes}</p>\n'
    return html


def gen_accessibility(d: dict) -> str:
    acc = d.get("accessibilityInfo", {})
    html = '<h2>♿ Accessibility</h2>\n'
    if isinstance(acc, str) and acc:
        html += f'<p>{escape(acc)}</p>\n'
        return html
    if not acc:
        html += '<p>Accessibility varies. Contact your accommodation and local tourism office in advance to arrange accessible transport and confirm facility access.</p>\n'
        return html

    overview = escape(acc.get("overview", ""))
    hospitals_acc = escape(acc.get("hospitalAccess", ""))
    transport = escape(acc.get("transport", ""))
    tips = escape(acc.get("tips", ""))

    if overview:
        html += f'<p>{overview}</p>\n'
    if hospitals_acc:
        html += f'<p><strong>Hospital accessibility:</strong> {hospitals_acc}</p>\n'
    if transport:
        html += f'<p><strong>Accessible transport:</strong> {transport}</p>\n'
    if tips:
        html += f'<div class="callout callout-tip"><p><strong>💡 Accessibility tips</strong></p><p>{tips}</p></div>\n'
    return html


def gen_covid(d: dict) -> str:
    covid = d.get("covidStatus", {})
    html = '<h2>🫁 COVID &amp; Respiratory Illness</h2>\n'
    if isinstance(covid, str) and covid:
        html += f'<p>{escape(covid)}</p>\n'
        return html
    if not covid:
        html += '<p>COVID entry restrictions have been lifted in most countries. Check current requirements with your airline and destination government before travel. Masks may still be required in healthcare settings.</p>\n'
        return html

    entry_req = escape(covid.get("entryRequirements", ""))
    mask_policy = escape(covid.get("maskPolicy", ""))
    testing = escape(covid.get("testing", ""))
    notes = escape(covid.get("notes", ""))

    if entry_req:
        html += f'<p><strong>Entry requirements:</strong> {entry_req}</p>\n'
    if mask_policy:
        html += f'<p><strong>Mask policy:</strong> {mask_policy}</p>\n'
    if testing:
        html += f'<p><strong>Testing availability:</strong> {testing}</p>\n'
    if notes:
        html += f'<p>{notes}</p>\n'
    return html


def gen_emergency_contacts(d: dict) -> str:
    number = escape(d.get("emergencyNumber", d.get("emergency_number", "")))
    eu_112 = d.get("eu112", False)
    html = '<h2>🚨 Emergency Contacts</h2>\n'
    html += f'<div class="callout callout-danger"><p><strong>🆘 Emergency:</strong> {number}</p>'
    if eu_112:
        html += '<p>📞 <strong>112</strong> also works as the universal EU emergency number</p>'
    html += '</div>\n'
    return html


def gen_related_links(d: dict) -> str:
    slug = d.get("countrySlug", d.get("country_slug", ""))
    name = d.get("countryName", d.get("country_name", ""))
    flag = d.get("flag", "")
    country_slug = COUNTRY_PAGE_SLUGS.get(slug, slug)

    html = f'<h2>🔗 Related {escape(name)} Guides</h2>\n'
    html += '<div class="callout callout-info"><p><strong>Explore more about ' + escape(name) + '</strong></p>\n'
    html += '<ul>\n'
    html += f'  <li>🌍 <a href="/countries/{escape(country_slug)}/" style="color:var(--terracotta);text-decoration:underline;">{flag} {escape(name)} Country Guide</a> — visa, culture, weather &amp; travel tips</li>\n'
    html += f'  <li>🚨 <a href="/scams/" style="color:var(--terracotta);text-decoration:underline;">Tourist Scam Alerts</a> — common scams to watch for</li>\n'
    html += f'  <li>🆚 <a href="/compare/" style="color:var(--terracotta);text-decoration:underline;">Compare Destinations</a> — compare {escape(name)} with other countries</li>\n'
    html += f'  <li>🔍 <a href="/find/" style="color:var(--terracotta);text-decoration:underline;">Destination Finder</a> — find your perfect trip</li>\n'
    html += '</ul></div>\n'
    return html


def gen_sources(d: dict) -> str:
    sources = d.get("sources", [])
    if not sources:
        return '<p>Sources: <a href="https://www.who.int/travel-advice" style="color:var(--terracotta);text-decoration:underline;">WHO</a>, <a href="https://wwwnc.cdc.gov/travel" style="color:var(--terracotta);text-decoration:underline;">CDC Travelers\' Health</a></p>'
    html = '<ul class="sources-list">\n'
    for s in sources:
        s_str = str(s)
        url = SOURCE_URLS.get(s_str, "")
        if url:
            html += f'  <li><a href="{escape(url)}" target="_blank" rel="noopener">{escape(s_str)}</a></li>\n'
        else:
            html += f'  <li>{escape(s_str)}</li>\n'
    html += '</ul>\n'
    return html


def gen_faq_schema(d: dict) -> str:
    """Generate FAQPage structured data from the health guide content."""
    name = d.get("countryName", d.get("country_name", ""))
    water = d.get("waterSafety", d.get("water_safety", ""))
    emergency = d.get("emergencyNumber", d.get("emergency_number", ""))
    ins = d.get("travelInsurance", d.get("travel_insurance", {}))
    vacc = d.get("vaccinations", {})

    water_map = {
        "safe": f"Yes, tap water is safe to drink in {name}.",
        "caution": f"Use caution in {name}. Tap water is generally safe in major cities but bottled water is recommended in rural areas.",
        "boil": f"Tap water should be boiled before drinking in {name}. Bottled water is widely available.",
        "unsafe": f"No, tap water is NOT safe to drink in {name}. Always use sealed bottled water, including for brushing teeth.",
        "bottled-only": f"No, only drink bottled water in {name}. Tap water is not safe for consumption.",
    }
    water_answer = water_map.get(water, f"Check local guidance on tap water safety in {name}.")

    ins_required = ins.get("required", False) if isinstance(ins, dict) else False
    ins_cost = ins.get("averageCost", ins.get("average_cost", "")) if isinstance(ins, dict) else ""
    ins_answer = f"Travel insurance is {'required' if ins_required else 'strongly recommended'} for {name}."
    if ins_cost:
        ins_answer += f" Average cost is {ins_cost}."

    vacc_req = vacc.get("required", []) if isinstance(vacc, dict) else []
    vacc_rec = vacc.get("recommended", []) if isinstance(vacc, dict) else []
    if vacc_req:
        vacc_answer = f"Required vaccinations for {name}: {', '.join(vacc_req)}."
    elif vacc_rec:
        vacc_answer = f"No vaccinations are required for {name}, but the following are recommended: {', '.join(vacc_rec)}."
    else:
        vacc_answer = f"No specific vaccinations are required for {name}. Ensure routine immunizations are up to date."

    faqs = [
        {
            "question": f"Is tap water safe to drink in {name}?",
            "answer": water_answer
        },
        {
            "question": f"What is the emergency number in {name}?",
            "answer": f"The emergency number in {name} is {emergency}."
        },
        {
            "question": f"Do I need travel insurance for {name}?",
            "answer": ins_answer
        },
        {
            "question": f"What vaccinations do I need for {name}?",
            "answer": vacc_answer
        },
    ]

    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["answer"]
                }
            }
            for faq in faqs
        ]
    }

    return f'<script type="application/ld+json">\n    {json.dumps(schema, indent=4, ensure_ascii=False)}\n    </script>'


# ── Build page ───────────────────────────────────────────────────────────

def get_val(d: dict, camel: str, snake: str, default: str = "") -> str:
    """Get value from dict trying camelCase then snake_case keys."""
    return str(d.get(camel, d.get(snake, default)))


def build_page(template: str, d: dict) -> str:
    """Replace all {{VARIABLE}} placeholders using structured data."""

    # Check if data has pre-rendered HTML (sample format) or structured data (enrichment format)
    has_html = any(k.endswith("_html") for k in d.keys())

    # Map template variables → values (escape for safe HTML insertion)
    replacements = {
        "COUNTRY_NAME": escape(get_val(d, "countryName", "country_name")),
        "COUNTRY_SLUG": escape(get_val(d, "countrySlug", "country_slug")),
        "COUNTRY_FLAG": get_val(d, "flag", "country_flag"),  # emoji, no escaping needed
        "ISO2": escape(get_val(d, "iso2", "iso2")),
        "EMERGENCY_NUMBER": escape(get_val(d, "emergencyNumber", "emergency_number")),
        "HEALTHCARE_SYSTEM": escape(get_val(d, "healthcareSystem", "healthcare_system")),
        "QUALITY_RATING": escape(get_val(d, "qualityRating", "quality_rating")),
        "PHARMACY_ACCESS": escape(get_val(d, "pharmacyAccess", "pharmacy_access")),
        "WATER_SAFETY": escape(get_val(d, "waterSafety", "water_safety")),
        "META_DESCRIPTION": escape(get_val(d, "metaDescription", "meta_description",
            f"Health & medication guide for {get_val(d, 'countryName', 'country_name')}")),
        "OG_IMAGE": escape(get_val(d, "ogImage", "og_image",
            f"https://img.tabiji.ai/health/{get_val(d, 'countrySlug', 'country_slug')}/hero.jpg")),
        "LAST_UPDATED": escape(get_val(d, "lastUpdated", "last_updated", "2026-03-30")),
        "DATE_PUBLISHED": escape(get_val(d, "datePublished", "date_published", "2026-03-15")),
    }

    # HTML sections: use pre-rendered if available, otherwise generate
    if has_html:
        replacements["HEALTHCARE_OVERVIEW_HTML"] = d.get("healthcare_overview_html", "")
        replacements["PHARMACY_GUIDE_HTML"] = d.get("pharmacy_guide_html", "")
        replacements["MEDICATIONS_HTML"] = d.get("medications_html", "")
        replacements["INSURANCE_HTML"] = d.get("insurance_html", "")
        replacements["VACCINATIONS_HTML"] = d.get("vaccinations_html", "")
        replacements["FOOD_WATER_HTML"] = d.get("food_water_html", "")
        replacements["EMERGENCY_CONTACTS_HTML"] = d.get("emergency_contacts_html", "")
        replacements["SOURCES_HTML"] = d.get("sources_html", "")
        replacements["HOSPITALS_HTML"] = d.get("hospitals_html", gen_hospitals(d))
        replacements["DENTAL_HTML"] = d.get("dental_html", gen_dental(d))
        replacements["MENTAL_HEALTH_HTML"] = d.get("mental_health_html", gen_mental_health(d))
        replacements["ACCESSIBILITY_HTML"] = d.get("accessibility_html", gen_accessibility(d))
        replacements["COVID_HTML"] = d.get("covid_html", gen_covid(d))
        replacements["RELATED_LINKS_HTML"] = d.get("related_links_html", gen_related_links(d))
        replacements["FAQ_SCHEMA"] = gen_faq_schema(d)
    else:
        replacements["HEALTHCARE_OVERVIEW_HTML"] = gen_healthcare_overview(d)
        replacements["HOSPITALS_HTML"] = gen_hospitals(d)
        replacements["PHARMACY_GUIDE_HTML"] = gen_pharmacy_guide(d)
        replacements["MEDICATIONS_HTML"] = gen_medications(d)
        replacements["DENTAL_HTML"] = gen_dental(d)
        replacements["INSURANCE_HTML"] = gen_insurance(d)
        replacements["VACCINATIONS_HTML"] = gen_vaccinations(d)
        replacements["FOOD_WATER_HTML"] = gen_food_water(d)
        replacements["MENTAL_HEALTH_HTML"] = gen_mental_health(d)
        replacements["ACCESSIBILITY_HTML"] = gen_accessibility(d)
        replacements["COVID_HTML"] = gen_covid(d)
        replacements["EMERGENCY_CONTACTS_HTML"] = gen_emergency_contacts(d)
        replacements["RELATED_LINKS_HTML"] = gen_related_links(d)
        replacements["SOURCES_HTML"] = gen_sources(d)
        replacements["FAQ_SCHEMA"] = gen_faq_schema(d)

    # Apply replacements
    result = template
    for key, value in replacements.items():
        result = result.replace("{{" + key + "}}", str(value))

    # Strip any remaining unreplaced placeholders
    result = re.sub(r"\{\{[^{}]+\}\}", "", result)
    return result


def save_page(output_path: Path, html: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"  ✅ {output_path.relative_to(TABIJI_ROOT)}")


def list_countries() -> None:
    files = sorted(DATA_DIR.glob("*.json"))
    files = [f for f in files if not f.stem.startswith("_")]
    if not files:
        print(f"No country data files found in {DATA_DIR}")
    else:
        print(f"Available ({len(files)} countries):")
        for p in files:
            print(f"  {p.stem}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build tabiji health guide pages.")
    parser.add_argument("iso2", nargs="?", help="ISO2 country code (e.g. JP, TH)")
    parser.add_argument("--list", action="store_true", help="List available data files")
    parser.add_argument("--all", action="store_true", help="Build all available countries")
    args = parser.parse_args()

    if args.list:
        list_countries()
        return

    template = load_template()

    if args.all:
        print("Building all health guide pages …")
        files = sorted(DATA_DIR.glob("*.json"))
        files = [f for f in files if not f.stem.startswith("_")]
        if not files:
            sys.exit(f"No .json files found in {DATA_DIR}")
        count = 0
        for path in files:
            d = load_data(path)
            slug = get_val(d, "countrySlug", "country_slug", path.stem.lower())
            output = OUTPUT_ROOT / slug / "index.html"
            page = build_page(template, d)
            save_page(output, page)
            count += 1
        print(f"\nDone — {count} pages built.")
        return

    if not args.iso2:
        parser.print_help()
        return

    iso2 = args.iso2.upper()
    print(f"Building health guide for {iso2} …")
    path = find_data_file(iso2)
    d = load_data(path)
    slug = get_val(d, "countrySlug", "country_slug", iso2.lower())
    page = build_page(template, d)
    output = OUTPUT_ROOT / slug / "index.html"
    save_page(output, page)
    print(f"\n📄 https://tabiji.ai/health/{slug}/\n")


if __name__ == "__main__":
    main()
