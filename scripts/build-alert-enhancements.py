#!/usr/bin/env python3
"""
Enrich alert pages at alerts/{country}/index.html with data from:
  api/v1/safety/{iso2}.json   — emergency numbers, healthcare, medications, cultural tips
  api/v1/scams/*.json         — scam pages for that country

Idempotent: removes existing #alert-enrichment-section before reinserting.
Only enriches pages where a safety profile exists (20 countries).
"""

import json
import html as html_lib
import sys
import os
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: beautifulsoup4 not installed. Run: pip3 install beautifulsoup4")
    sys.exit(1)

ROOT = Path(__file__).parent.parent
ALERTS_DIR = ROOT / "alerts"
SAFETY_DIR = ROOT / "api/v1/safety"
SCAMS_DIR = ROOT / "api/v1/scams"
COUNTRIES_JSON = ROOT / "api/v1/countries.json"

# Manual overrides for slugs that don't map cleanly
SLUG_OVERRIDES = {
    "usa": "US",
    "burma-myanmar": "MM",
    "east-timor": "TL",
    "czech-republic": "CZ",
    "the-kyrgyz-republic": "KG",
    "guinea-bissau": "GW",
    "democratic-republic-of-the-congo": "CD",
    "federated-states-of-micronesia": "FM",
    "cote-d-ivoire": "CI",
    "curaao": "CW",
    "sao-tome-and-principe": "ST",
    "kingdom-of-denmark": "DK",
    "french-west-indies": "MQ",  # Martinique (representative)
    "mainland-china-hong-kong-macau-see-summaries": "CN",
    "so-tom-and-prncipe": "ST",
}

# Skip these (not country directories)
SKIP_SLUGS = {"level-1", "level-2", "level-3", "level-4", "index.html", "americas"}


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def build_name_to_iso2(countries_data):
    mapping = {}
    for c in countries_data:
        mapping[c["name"].lower()] = c["iso2"]
        # Also add iso2 as key for direct lookup
        if c.get("iso2"):
            mapping[c["iso2"].lower()] = c["iso2"]
    return mapping


def slug_to_iso2(slug, name_map):
    if slug in SLUG_OVERRIDES:
        return SLUG_OVERRIDES[slug].lower()
    candidate = slug.replace("-", " ")
    iso2 = name_map.get(candidate)
    if iso2:
        return iso2.lower()
    return None


def find_scam_files_for_iso2(iso2):
    """Find scam JSON files that match the given iso2 country code."""
    matches = []
    for f in SCAMS_DIR.glob("*.json"):
        data = load_json(f)
        if data and (data.get("countryCode") or "").upper() == iso2.upper():
            matches.append(data)
    return matches


def render_enrichment(safety, scam_files, slug, iso2):
    country_name = safety.get("name", slug.replace("-", " ").title())

    # Emergency numbers
    emergency = safety.get("emergency") or {}
    police = emergency.get("police", "—")
    ambulance = emergency.get("ambulance", "—")
    fire = emergency.get("fire", "—")
    em_notes = emergency.get("notes", "")

    em_html = f"""<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:12px 0;text-align:center">
  <div style="background:var(--warm-cream);border-radius:10px;padding:12px 8px">
    <div style="font-size:1.4rem">🚔</div>
    <div style="font-weight:700;font-size:1.1rem;color:var(--indigo)">{html_lib.escape(police)}</div>
    <div style="font-size:0.72rem;color:var(--text-muted);margin-top:2px">Police</div>
  </div>
  <div style="background:var(--warm-cream);border-radius:10px;padding:12px 8px">
    <div style="font-size:1.4rem">🚑</div>
    <div style="font-weight:700;font-size:1.1rem;color:var(--indigo)">{html_lib.escape(ambulance)}</div>
    <div style="font-size:0.72rem;color:var(--text-muted);margin-top:2px">Ambulance</div>
  </div>
  <div style="background:var(--warm-cream);border-radius:10px;padding:12px 8px">
    <div style="font-size:1.4rem">🚒</div>
    <div style="font-weight:700;font-size:1.1rem;color:var(--indigo)">{html_lib.escape(fire)}</div>
    <div style="font-size:0.72rem;color:var(--text-muted);margin-top:2px">Fire</div>
  </div>
</div>"""
    if em_notes:
        em_html += f'<p style="font-size:0.82rem;color:var(--text-muted);margin-bottom:0">ℹ️ {html_lib.escape(em_notes)}</p>'

    # Healthcare summary
    hc = safety.get("healthcare") or {}
    hc_quality = hc.get("qualityRating", "")
    hc_notes = hc.get("hospitalNotes", "") or hc.get("costForTourists", "")
    insurance_advice = hc.get("insuranceAdvice", "")
    hc_html = ""
    if hc_quality or hc_notes:
        quality_str = hc_quality.title() if hc_quality else ""
        quality_color = {"excellent": "#16a34a", "good": "#a16207", "fair": "#ea580c"}.get(
            hc_quality, "#6B5D4F"
        )
        hc_html = f"""<div class="alert-section" style="margin-top:1.5rem">
  <h2>🏥 Healthcare Summary</h2>
  {'<div style="display:inline-flex;background:#f0fdf4;color:' + quality_color + ';padding:3px 10px;border-radius:8px;font-size:0.8rem;font-weight:700;margin-bottom:10px">' + html_lib.escape(quality_str) + ' quality</div>' if quality_str else ''}
  {'<p>' + html_lib.escape(hc_notes) + '</p>' if hc_notes else ''}
  {'<p style="margin-top:8px;font-size:0.85rem;color:var(--text-muted)"><strong>Insurance:</strong> ' + html_lib.escape(insurance_advice) + '</p>' if insurance_advice else ''}
</div>"""

    # Medication warnings
    meds = safety.get("medications") or {}
    controlled = meds.get("controlledSubstances") or []
    general_advice = meds.get("generalAdvice", "")
    meds_html = ""
    if controlled or general_advice:
        items_html = ""
        for m in controlled[:5]:
            status = m.get("status", "")
            color = "#dc2626" if status == "banned" else "#ea580c"
            items_html += (
                f'<li style="margin-bottom:6px"><strong>{html_lib.escape(m.get("drug",""))}</strong>'
                f' — <span style="color:{color};font-weight:600">{html_lib.escape(status.upper())}</span>'
                f'{": " + html_lib.escape(m.get("note","")) if m.get("note") else ""}</li>'
            )
        meds_html = f"""<div class="alert-section" style="margin-top:1.5rem">
  <h2>💊 Medication Restrictions</h2>
  {'<p style="font-size:0.9rem;margin-bottom:10px">' + html_lib.escape(general_advice) + '</p>' if general_advice else ''}
  {'<ul style="padding-left:18px;font-size:0.85rem;color:var(--text-muted)">' + items_html + '</ul>' if items_html else ''}
</div>"""

    # Cultural tips
    cultural = safety.get("cultural") or {}
    tipping = cultural.get("tipping", "")
    taboos = cultural.get("taboos") or []
    cultural_html = ""
    if tipping or taboos:
        taboos_html = ""
        if taboos:
            t_items = "".join(f"<li>{html_lib.escape(t)}</li>" for t in taboos[:5])
            taboos_html = f'<ul style="padding-left:18px;font-size:0.85rem;color:var(--text-muted);margin-top:6px">{t_items}</ul>'
        cultural_html = f"""<div class="alert-section" style="margin-top:1.5rem">
  <h2>🙏 Cultural Tips</h2>
  {'<p style="margin-bottom:8px"><strong>Tipping:</strong> ' + html_lib.escape(tipping) + '</p>' if tipping else ''}
  {'<p style="margin-bottom:4px"><strong>Cultural taboos to avoid:</strong></p>' + taboos_html if taboos else ''}
</div>"""

    # Scam page links
    scam_links_html = ""
    if scam_files:
        links = ""
        for sf in scam_files:
            city = sf.get("city", "")
            scam_slug = sf.get("slug", "")
            count = sf.get("scamCount", len(sf.get("scams", [])))
            if city and scam_slug:
                links += (
                    f'<a href="/scams/{html_lib.escape(scam_slug)}/" class="tabiji-link">'
                    f'🎭 {html_lib.escape(city)} Scam Guide ({count} scams)</a>'
                )
        if links:
            scam_links_html = f"""<div class="alert-section" style="margin-top:1.5rem">
  <h2>🎭 Tourist Scam Guides</h2>
  <p style="margin-bottom:10px">Common scams to watch out for in {html_lib.escape(country_name)}:</p>
  <div class="tabiji-links">{links}</div>
</div>"""

    section = f"""<div id="alert-enrichment-section">
<div class="alert-section" style="margin-top:1.5rem">
  <h2>🚨 Emergency Numbers</h2>
  {em_html}
</div>
{hc_html}
{meds_html}
{cultural_html}
{scam_links_html}
</div>"""

    return section


def enrich_alert_page(slug, iso2):
    page_path = ALERTS_DIR / slug / "index.html"
    if not page_path.exists():
        return False

    safety = load_json(SAFETY_DIR / f"{iso2}.json")
    if not safety:
        return False  # Only enrich pages with safety profiles

    scam_files = find_scam_files_for_iso2(iso2)

    html_content = page_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove existing enrichment section (idempotent)
    existing = soup.find(id="alert-enrichment-section")
    if existing:
        existing.decompose()

    enrichment_html = render_enrichment(safety, scam_files, slug, iso2)
    new_section = BeautifulSoup(enrichment_html, "html.parser")

    # Insert before footer or at end of .detail-content, or before </body>
    detail_content = soup.find(class_="detail-content")
    footer = soup.find("footer")

    if footer:
        footer.insert_before(new_section)
    elif detail_content:
        detail_content.append(new_section)
    else:
        body = soup.find("body")
        if body:
            body.append(new_section)
        else:
            return False

    page_path.write_text(str(soup), encoding="utf-8")
    return True


def main():
    print("Loading countries data…")
    countries_data = load_json(COUNTRIES_JSON)
    countries_list = countries_data.get("countries", []) if isinstance(countries_data, dict) else []
    name_map = build_name_to_iso2(countries_list)

    alert_slugs = [
        d for d in os.listdir(ALERTS_DIR)
        if (ALERTS_DIR / d).is_dir() and d not in SKIP_SLUGS
    ]
    alert_slugs.sort()
    print(f"Alert pages: {len(alert_slugs)}")

    enriched = 0
    skipped_no_safety = 0
    skipped_no_mapping = 0

    for slug in alert_slugs:
        iso2 = slug_to_iso2(slug, name_map)
        if not iso2:
            skipped_no_mapping += 1
            continue

        result = enrich_alert_page(slug, iso2)
        if result:
            enriched += 1
            scam_count = len(find_scam_files_for_iso2(iso2))
            scam_note = f" + {scam_count} scam guide(s)" if scam_count else ""
            print(f"  ✓ alerts/{slug}/ [{iso2.upper()}]{scam_note}")
        else:
            skipped_no_safety += 1

    print(f"\nEnriched: {enriched} pages")
    print(f"Skipped (no safety profile): {skipped_no_safety}")
    print(f"Skipped (no country mapping): {skipped_no_mapping}")
    print("Done.")


if __name__ == "__main__":
    main()
