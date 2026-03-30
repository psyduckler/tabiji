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
TEMPLATE_PATH = TABIJI_ROOT / "health-template.html"
DATA_DIR = TABIJI_ROOT / "health-data"
SAMPLE_DIR = TABIJI_ROOT  # for health-sample-japan.json fallback
OUTPUT_ROOT = TABIJI_ROOT / "health"


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


def gen_pharmacy_guide(d: dict) -> str:
    access = escape(d.get("pharmacyAccess", d.get("pharmacy_access", "")))
    hours = escape(d.get("pharmacyHours", d.get("pharmacy_hours", "")))
    tips = escape(d.get("pharmacyTips", d.get("pharmacy_tips", "")))
    rules = escape(d.get("prescriptionRules", d.get("prescription_rules", "")))
    otc = d.get("commonOTC", d.get("common_otc", []))

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
    if tips:
        html += f'<div class="callout callout-tip"><p><strong>💡 Tips</strong></p><p>{tips}</p></div>\n'
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


def gen_insurance(d: dict) -> str:
    ins = d.get("travelInsurance", d.get("travel_insurance", {}))
    if isinstance(ins, str):
        return f'<h2>🛡️ Travel Insurance</h2>\n<p>{escape(ins)}</p>\n'

    recommended = ins.get("recommended", True)
    required = ins.get("required", False)
    cost = escape(ins.get("averageCost", ins.get("average_cost", "")))
    tips = escape(ins.get("tips", ""))
    req_note = escape(ins.get("requiredNote", ins.get("required_note", "")))

    html = '<h2>🛡️ Travel Insurance</h2>\n'
    if required:
        html += '<div class="callout callout-warn"><p><strong>⚠️ Required</strong></p>'
        if req_note:
            html += f'<p>{req_note}</p>'
        html += '</div>\n'
    elif recommended:
        html += '<p><span class="badge badge-warn">⚠️ Strongly recommended</span></p>\n'
    else:
        html += '<p><span class="badge badge-safe">✅ Optional</span></p>\n'

    if cost:
        html += f'<p><strong>Average cost:</strong> {cost}</p>\n'
    if tips:
        html += f'<div class="callout callout-tip"><p><strong>💡 Tip</strong></p><p>{tips}</p></div>\n'
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
        "boil": '<span class="badge badge-warn">⚠️ Boil water before drinking</span>',
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


def gen_emergency_contacts(d: dict) -> str:
    number = escape(d.get("emergencyNumber", d.get("emergency_number", "")))
    html = '<h2>🚨 Emergency Contacts</h2>\n'
    html += f'<div class="callout callout-danger"><p><strong>🆘 Emergency:</strong> {number}</p></div>\n'
    return html


def gen_sources(d: dict) -> str:
    sources = d.get("sources", [])
    if not sources:
        return '<p>Sources: WHO, CDC Travelers Health</p>'
    html = '<ul class="sources-list">\n'
    for s in sources:
        html += f'  <li>{escape(str(s))}</li>\n'
    html += '</ul>\n'
    return html


# ── Build page ───────────────────────────────────────────────────────────

def get_val(d: dict, camel: str, snake: str, default: str = "") -> str:
    """Get value from dict trying camelCase then snake_case keys."""
    return str(d.get(camel, d.get(snake, default)))


def build_page(template: str, d: dict) -> str:
    """Replace all {{VARIABLE}} placeholders using structured data."""

    # Check if data has pre-rendered HTML (sample format) or structured data (enrichment format)
    has_html = any(k.endswith("_html") for k in d.keys())

    # Map template variables → values
    replacements = {
        "COUNTRY_NAME": get_val(d, "countryName", "country_name"),
        "COUNTRY_SLUG": get_val(d, "countrySlug", "country_slug"),
        "COUNTRY_FLAG": get_val(d, "flag", "country_flag"),
        "ISO2": get_val(d, "iso2", "iso2"),
        "EMERGENCY_NUMBER": get_val(d, "emergencyNumber", "emergency_number"),
        "HEALTHCARE_SYSTEM": get_val(d, "healthcareSystem", "healthcare_system"),
        "QUALITY_RATING": get_val(d, "qualityRating", "quality_rating"),
        "PHARMACY_ACCESS": get_val(d, "pharmacyAccess", "pharmacy_access"),
        "WATER_SAFETY": get_val(d, "waterSafety", "water_safety"),
        "META_DESCRIPTION": get_val(d, "metaDescription", "meta_description",
            f"Health & medication guide for {get_val(d, 'countryName', 'country_name')}"),
        "OG_IMAGE": get_val(d, "ogImage", "og_image",
            f"https://img.tabiji.ai/health/{get_val(d, 'countrySlug', 'country_slug')}/hero.jpg"),
        "LAST_UPDATED": get_val(d, "lastUpdated", "last_updated", "2026-03-30"),
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
    else:
        replacements["HEALTHCARE_OVERVIEW_HTML"] = gen_healthcare_overview(d)
        replacements["PHARMACY_GUIDE_HTML"] = gen_pharmacy_guide(d)
        replacements["MEDICATIONS_HTML"] = gen_medications(d)
        replacements["INSURANCE_HTML"] = gen_insurance(d)
        replacements["VACCINATIONS_HTML"] = gen_vaccinations(d)
        replacements["FOOD_WATER_HTML"] = gen_food_water(d)
        replacements["EMERGENCY_CONTACTS_HTML"] = gen_emergency_contacts(d)
        replacements["SOURCES_HTML"] = gen_sources(d)

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
