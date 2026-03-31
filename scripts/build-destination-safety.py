#!/usr/bin/env python3
"""
Inject a 'Safety & Practical Info' section into the 8 destination detail pages.
Uses BeautifulSoup to modify HTML in-place. Idempotent: removes existing
#safety-section before reinserting.

Reads from:
  api/v1/safety/{iso2}.json
  api/v1/scams/{slug}.json
  api/v1/alerts/{iso2}.json

Destination → countryCode mapping:
  bali → ID, bangkok → TH, barcelona → ES, london → GB,
  mexico-city → MX, paris → FR, rome → IT, tokyo → JP
"""

import json
import html as html_lib
import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup, Comment
except ImportError:
    print("ERROR: beautifulsoup4 not installed. Run: pip3 install beautifulsoup4")
    sys.exit(1)

ROOT = Path(__file__).parent.parent

SLUG_TO_ISO2 = {
    "bali": "id",
    "bangkok": "th",
    "barcelona": "es",
    "london": "gb",
    "mexico-city": "mx",
    "paris": "fr",
    "rome": "it",
    "tokyo": "jp",
}


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def advisory_class(level):
    return {1: "l1", 2: "l2", 3: "l3", 4: "l4"}.get(level, "l2")


def advisory_color(level):
    return {1: "#16a34a", 2: "#a16207", 3: "#ea580c", 4: "#dc2626"}.get(level, "#a16207")


def advisory_bg(level):
    return {1: "#f0fdf4", 2: "#fefce8", 3: "#fff7ed", 4: "#fef2f2"}.get(level, "#fefce8")


def severity_badge(severity):
    colors = {
        "high": ("#dc2626", "#fef2f2"),
        "moderate": ("#ea580c", "#fff7ed"),
        "low": ("#a16207", "#fefce8"),
    }
    fg, bg = colors.get((severity or "").lower(), ("#6b5d4f", "#f5f0e8"))
    return f'<span style="display:inline-flex;align-items:center;padding:2px 8px;border-radius:8px;font-size:0.7rem;font-weight:700;background:{bg};color:{fg}">{html_lib.escape((severity or "").title())}</span>'


def render_safety_section(slug, safety, alert, scams_data):
    iso2 = SLUG_TO_ISO2.get(slug, "").upper()
    city_name = slug.replace("-", " ").title()

    # === SAFETY CARD ===
    advisory_level = None
    advisory_text = "Unknown"
    emergency = {}
    overall_risk = None
    solo_female = None
    healthcare_quality = None
    medications = []

    if safety:
        ta = safety.get("travelAdvisory") or {}
        advisory_level = ta.get("level")
        advisory_text = ta.get("levelText", "")
        emergency = safety.get("emergency") or {}
        s = safety.get("safety") or {}
        overall_risk = s.get("overallRisk")
        solo_female = s.get("soloFemaleSafety")
        hc = safety.get("healthcare") or {}
        healthcare_quality = hc.get("qualityRating")
        meds = safety.get("medications") or {}
        for m in (meds.get("controlledSubstances") or []):
            if m.get("status") in ("banned", "restricted"):
                medications.append(m)

    elif alert:
        us = alert.get("us") or {}
        advisory_level = us.get("level")
        advisory_text = us.get("levelText", "")

    lvl = advisory_level or 2
    badge_bg = advisory_bg(lvl)
    badge_fg = advisory_color(lvl)

    # Emergency numbers
    em_html = ""
    if emergency:
        police = emergency.get("police", "—")
        ambulance = emergency.get("ambulance", "—")
        fire = emergency.get("fire", "—")
        em_html = f"""<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:12px 0;text-align:center">
  <div style="background:#f8f8f8;border-radius:10px;padding:10px 8px">
    <div style="font-size:1.2rem">🚔</div>
    <div style="font-weight:700;font-size:1rem;color:#2D3A5C">{html_lib.escape(police)}</div>
    <div style="font-size:0.72rem;color:#6B5D4F">Police</div>
  </div>
  <div style="background:#f8f8f8;border-radius:10px;padding:10px 8px">
    <div style="font-size:1.2rem">🚑</div>
    <div style="font-weight:700;font-size:1rem;color:#2D3A5C">{html_lib.escape(ambulance)}</div>
    <div style="font-size:0.72rem;color:#6B5D4F">Ambulance</div>
  </div>
  <div style="background:#f8f8f8;border-radius:10px;padding:10px 8px">
    <div style="font-size:1.2rem">🚒</div>
    <div style="font-weight:700;font-size:1rem;color:#2D3A5C">{html_lib.escape(fire)}</div>
    <div style="font-size:0.72rem;color:#6B5D4F">Fire</div>
  </div>
</div>"""
        if emergency.get("notes"):
            em_html += f'<p style="font-size:0.82rem;color:#6B5D4F;margin-top:4px">ℹ️ {html_lib.escape(emergency["notes"])}</p>'

    # Safety stats
    stats_html = ""
    stats_items = []
    if overall_risk:
        stats_items.append(("Overall Risk", overall_risk.replace("-", " ").title()))
    if solo_female:
        stats_items.append(("Solo Female", solo_female.replace("-", " ").title()))
    if healthcare_quality:
        stats_items.append(("Healthcare", healthcare_quality.title()))
    if stats_items:
        inner = "".join(
            f'<div style="flex:1;min-width:100px;text-align:center;padding:10px 8px;background:#f8f8f8;border-radius:10px">'
            f'<div style="font-weight:700;color:#2D3A5C;font-size:0.95rem">{html_lib.escape(v)}</div>'
            f'<div style="font-size:0.7rem;color:#6B5D4F;text-transform:uppercase;letter-spacing:0.04em;margin-top:2px">{html_lib.escape(k)}</div>'
            f'</div>'
            for k, v in stats_items
        )
        stats_html = f'<div style="display:flex;gap:8px;flex-wrap:wrap;margin:12px 0">{inner}</div>'

    # Medication warnings
    meds_html = ""
    if medications:
        med_items = "".join(
            f'<li style="margin-bottom:6px"><strong>{html_lib.escape(m["drug"])}</strong> — '
            f'<span style="color:{"#dc2626" if m["status"]=="banned" else "#ea580c"}">{html_lib.escape(m["status"].upper())}</span>. '
            f'{html_lib.escape(m.get("note",""))}</li>'
            for m in medications[:4]
        )
        meds_html = f"""<div style="margin-top:14px;padding:12px 14px;background:#fef9c3;border-radius:10px;border-left:3px solid #eab308">
  <div style="font-weight:600;font-size:0.85rem;color:#92400e;margin-bottom:6px">⚠️ Medication Restrictions</div>
  <ul style="font-size:0.82rem;color:#6B5D4F;padding-left:16px">{med_items}</ul>
</div>"""

    safety_card = f"""<div style="background:#fff;border-radius:14px;padding:20px;box-shadow:0 2px 12px rgba(0,0,0,.07);margin-bottom:20px">
  <h3 style="font-family:'Playfair Display',serif;font-size:1.2rem;color:#2D3A5C;margin-bottom:14px;display:flex;align-items:center;gap:8px">
    🛡️ Safety Overview
    <span style="margin-left:auto;font-family:inherit;font-size:0.8rem;font-weight:700;padding:4px 12px;border-radius:8px;background:{badge_bg};color:{badge_fg}">Level {lvl}: {html_lib.escape(advisory_text)}</span>
  </h3>
  {em_html}
  {stats_html}
  {meds_html}
  <div style="margin-top:10px;font-size:0.78rem;color:#6B5D4F">
    <a href="/alerts/{iso2.lower()}/" style="color:#C4704B;text-decoration:none">View full {html_lib.escape(city_name)} travel advisory →</a>
  </div>
</div>"""

    # === SCAMS CARD ===
    scams_html = ""
    if scams_data and scams_data.get("scams"):
        scam_items = scams_data["scams"][:5]
        items_html = ""
        for scam in scam_items:
            name = scam.get("name", "")
            severity = scam.get("severity", "")
            description = scam.get("description", "")
            avoidance = scam.get("avoidance", "")
            badge = severity_badge(severity)
            items_html += f"""<details style="border:1px solid #E8DFD0;border-radius:10px;margin-bottom:8px;overflow:hidden">
  <summary style="padding:12px 14px;cursor:pointer;display:flex;align-items:center;gap:8px;background:#FEFCF9;font-size:0.9rem;font-weight:600;color:#2D3A5C;list-style:none">
    <span style="flex:1">{html_lib.escape(name)}</span>
    {badge}
    <span style="font-size:0.7rem;color:#6B5D4F;flex-shrink:0">tap to expand</span>
  </summary>
  <div style="padding:12px 14px;background:#fff;border-top:1px solid #E8DFD0">
    <p style="font-size:0.85rem;color:#2C2419;line-height:1.6;margin-bottom:10px">{html_lib.escape(description)}</p>
    <div style="background:#f0fdf4;border-radius:8px;padding:10px 12px;font-size:0.82rem;color:#16a34a">
      <strong>How to avoid:</strong> {html_lib.escape(avoidance)}
    </div>
  </div>
</details>"""

        scam_link = ""
        if slug in {"bali", "bangkok", "barcelona", "london", "mexico-city", "paris", "rome", "tokyo"}:
            scam_link = f'<div style="margin-top:10px;font-size:0.78rem"><a href="/scams/{slug}/" style="color:#C4704B;text-decoration:none">View full {html_lib.escape(city_name)} scam guide →</a></div>'

        scams_html = f"""<div style="background:#fff;border-radius:14px;padding:20px;box-shadow:0 2px 12px rgba(0,0,0,.07)">
  <h3 style="font-family:'Playfair Display',serif;font-size:1.2rem;color:#2D3A5C;margin-bottom:14px">
    🎭 Common Scams
  </h3>
  {items_html}
  {scam_link}
</div>"""

    section_html = f"""<section id="safety-section" style="max-width:900px;margin:3rem auto;padding:0 2rem">
  <h2 style="font-family:'Playfair Display',serif;font-size:1.6rem;color:#2D3A5C;margin-bottom:20px;padding-bottom:12px;border-bottom:2px solid #E8DFD0">
    🌍 Safety &amp; Practical Info
  </h2>
  <div style="display:grid;grid-template-columns:1fr;gap:20px">
    {safety_card}
    {scams_html}
  </div>
</section>"""

    return section_html


def inject_safety(slug, iso2):
    page_path = ROOT / "destinations" / slug / "index.html"
    if not page_path.exists():
        print(f"  SKIP {slug}: page not found")
        return

    safety = load_json(ROOT / "api/v1/safety" / f"{iso2}.json")
    alert = load_json(ROOT / "api/v1/alerts" / f"{iso2}.json")
    scams_data = load_json(ROOT / "api/v1/scams" / f"{slug}.json")

    if not safety and not alert:
        print(f"  SKIP {slug}: no safety or alert data for {iso2}")
        return

    html_content = page_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove existing safety section (idempotent)
    existing = soup.find(id="safety-section")
    if existing:
        existing.decompose()

    # Generate new section
    section_html = render_safety_section(slug, safety, alert, scams_data)
    new_section = BeautifulSoup(section_html, "html.parser")

    # Insert before footer, or before closing </main>, or before closing </body>
    footer = soup.find("footer")
    if footer:
        footer.insert_before(new_section)
    else:
        body = soup.find("body")
        if body:
            body.append(new_section)
        else:
            print(f"  WARN {slug}: no footer or body found, appending to end")
            html_content += section_html
            page_path.write_text(html_content, encoding="utf-8")
            return

    page_path.write_text(str(soup), encoding="utf-8")
    has_safety = "✓ safety" if safety else ""
    has_scams = "✓ scams" if scams_data else ""
    has_alert = "✓ alert" if alert else ""
    print(f"  ✓ destinations/{slug}/  {has_safety} {has_scams} {has_alert}")


def main():
    print("Injecting safety sections into destination detail pages…")
    for slug, iso2 in SLUG_TO_ISO2.items():
        inject_safety(slug, iso2)
    print("Done.")


if __name__ == "__main__":
    main()
