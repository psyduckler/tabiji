#!/usr/bin/env python3
"""
build-medications.py — Rebuild /health/medications/ hub + 7 tier-1 medication
pages in editorial-v2.

Pulls per-country restrictedMeds arrays from /health-data/*.json, aggregates
banned/restricted country lists per tier-1 medication, and emits:
  - /health/medications/index.html              (rebuilt hub)
  - /health/medications/{slug}/index.html       (7 tier-1 pages: adderall,
    sudafed, codeine, cbd, tramadol, xanax, opioids)

Also enriches /api/v1/health.json with a top-level `medications` array.

Usage:
    python3 scripts/build-medications.py
"""

import html
import json
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
    render_medication_book_cta,
)
from lib.medication_content import TIER1, HUB_FAQS  # noqa: E402

ROOT = SCRIPT_DIR.parent
HEALTH_DATA = ROOT / "health-data"
OUT_HUB = ROOT / "health" / "medications" / "index.html"
OUT_DIR = ROOT / "health" / "medications"
HEALTH_API = ROOT / "api" / "v1" / "health.json"


def load_country_medications():
    """Return [{slug, name, flag, iso2, meds: [{name, status, note}]}, ...]."""
    out = []
    for p in sorted(HEALTH_DATA.glob("*.json")):
        try:
            d = json.loads(p.read_text())
        except Exception:
            continue
        out.append({
            "slug": d.get("countrySlug"),
            "name": d.get("countryName"),
            "flag": d.get("flag", ""),
            "iso2": d.get("iso2"),
            "meds": d.get("restrictedMeds") or [],
        })
    return out


def match_tier1(med_name: str, patterns) -> bool:
    name = med_name.lower()
    return any(p in name for p in patterns)


def aggregate_by_tier1(countries, tier1):
    """For each tier-1 entry, produce {banned: [...], restricted: [...]}
    where each sub-list is [{slug, name, flag, note}, ...]."""
    out = {}
    for t in tier1:
        banned = []
        restricted = []
        for c in countries:
            matching = [m for m in c["meds"] if match_tier1(m.get("name", ""), t["match_patterns"])]
            if not matching:
                continue
            statuses = {(m.get("status") or "").lower() for m in matching}
            note = "; ".join(
                (m.get("note") or "").strip() for m in matching if m.get("note")
            )[:400]
            entry = {
                "slug": c["slug"],
                "name": c["name"],
                "flag": c["flag"],
                "note": note,
            }
            if "banned" in statuses:
                banned.append(entry)
            elif "restricted" in statuses or "controlled" in statuses:
                restricted.append(entry)
        banned.sort(key=lambda e: e["name"] or "")
        restricted.sort(key=lambda e: e["name"] or "")
        out[t["slug"]] = {"banned": banned, "restricted": restricted}
    return out


def render_country_chip(entry: dict) -> str:
    flag = entry["flag"]
    slug = entry["slug"]
    name = html.escape(entry["name"] or slug)
    return (
        f'      <a href="/health/{slug}/" class="country-chip">'
        f'<span class="chip-flag">{flag}</span>{name}</a>'
    )


def render_country_list(entries, empty_msg: str) -> str:
    if not entries:
        return f'    <p class="empty-list">{html.escape(empty_msg)}</p>'
    chips = "\n".join(render_country_chip(e) for e in entries)
    return f'    <div class="country-chips">\n{chips}\n    </div>'


def render_tone_callout(tone: str, title: str, body: str) -> str:
    return (
        f'<div class="med-callout med-callout-{tone}">'
        f'<strong class="med-callout-title">{html.escape(title)}</strong>'
        f'<p>{html.escape(body)}</p></div>'
    )


def render_strategy_steps(steps) -> str:
    out = []
    for s in steps:
        out.append(
            f'      <li>\n'
            f'        <strong>{html.escape(s["title"])}</strong>\n'
            f'        <p>{html.escape(s["body"])}</p>\n'
            f'      </li>'
        )
    return "\n".join(out)


def render_tier1_chips() -> str:
    chips = []
    for t in TIER1:
        chips.append(
            f'      <a href="/health/medications/{t["slug"]}/" class="tier1-chip">'
            f'<span class="chip-icon">{t["icon"]}</span>'
            f'<span class="chip-text">'
            f'<strong>{html.escape(t["canonical_name"])}</strong>'
            f'<em>{html.escape(t["what_travelers_ask"])}</em>'
            f'</span></a>'
        )
    return "\n".join(chips)


def render_hub_schema(countries_count, med_entries_count, today) -> dict:
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "MedicalWebPage",
                "name": "Medication Restrictions by Country",
                "headline": "Can you travel with your meds?",
                "description": (
                    f"Travel medication restrictions for {countries_count} countries covering "
                    f"{med_entries_count} medication entries. Deep-dive guides for Adderall, Sudafed, "
                    "codeine, CBD, tramadol, benzodiazepines, and opioids — which countries ban them, "
                    "which require import permits, and what alternatives travel legally."
                ),
                "url": "https://tabiji.ai/health/medications/",
                "inLanguage": "en",
                "specialty": "TravelMedicine",
                "about": [
                    {"@type": "Drug", "name": "Amphetamine"},
                    {"@type": "Drug", "name": "Pseudoephedrine"},
                    {"@type": "Drug", "name": "Codeine"},
                    {"@type": "Drug", "name": "Cannabidiol"},
                    {"@type": "Drug", "name": "Tramadol"},
                    {"@type": "Drug", "name": "Benzodiazepine"},
                ],
                "audience": {"@type": "PeopleAudience", "audienceType": "International travelers with prescription medications"},
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
                    "logo": {"@type": "ImageObject", "url": "https://img.tabiji.ai/tabiji-owl-logo.png"},
                },
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tabiji.ai/"},
                    {"@type": "ListItem", "position": 2, "name": "Travel Health", "item": "https://tabiji.ai/health/"},
                    {"@type": "ListItem", "position": 3, "name": "Medication Restrictions", "item": "https://tabiji.ai/health/medications/"},
                ],
            },
            {"@type": "FAQPage", "mainEntity": render_faqs_schema(HUB_FAQS)},
            {
                "@type": "ItemList",
                "name": "Tier-1 travel medication guides",
                "numberOfItems": len(TIER1),
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": i + 1,
                        "name": t["canonical_name"],
                        "url": f"https://tabiji.ai/health/medications/{t['slug']}/",
                    }
                    for i, t in enumerate(TIER1)
                ],
            },
        ],
    }


def render_tier1_schema(tier1: dict, country_counts: dict, today: str) -> dict:
    howto_steps = [
        {
            "@type": "HowToStep",
            "position": i + 1,
            "name": step["title"],
            "text": step["body"],
        }
        for i, step in enumerate(tier1["travel_strategy"])
    ]
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "MedicalWebPage",
                "name": tier1["canonical_name"],
                "headline": tier1["page_title"],
                "description": tier1["meta_description"],
                "url": f"https://tabiji.ai/health/medications/{tier1['slug']}/",
                "inLanguage": "en",
                "specialty": "TravelMedicine",
                "about": {"@type": "Drug", "name": tier1["canonical_name"]},
                "audience": {"@type": "PeopleAudience", "audienceType": "International travelers with prescription medications"},
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
                    "logo": {"@type": "ImageObject", "url": "https://img.tabiji.ai/tabiji-owl-logo.png"},
                },
            },
            {
                "@type": "HowTo",
                "name": f"How to travel with {tier1['canonical_name'].lower()}",
                "description": (
                    f"Five practical steps to travel legally with {tier1['canonical_name'].lower()} "
                    "when your destination restricts it — or to travel without it."
                ),
                "totalTime": "PT30M",
                "step": howto_steps,
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tabiji.ai/"},
                    {"@type": "ListItem", "position": 2, "name": "Travel Health", "item": "https://tabiji.ai/health/"},
                    {"@type": "ListItem", "position": 3, "name": "Medications", "item": "https://tabiji.ai/health/medications/"},
                    {"@type": "ListItem", "position": 4, "name": tier1["canonical_name"], "item": f"https://tabiji.ai/health/medications/{tier1['slug']}/"},
                ],
            },
            {"@type": "FAQPage", "mainEntity": render_faqs_schema(tier1["faqs"])},
        ],
    }


def build_hub(country_data, aggregated, today):
    countries_count = len(country_data)
    med_entries_count = sum(len(c["meds"]) for c in country_data)

    schema_str = json.dumps(render_hub_schema(countries_count, med_entries_count, today), ensure_ascii=False, indent=2)

    # Prebuild the country MD JSON for the searchable UI
    md = {}
    for c in country_data:
        if not c["meds"]:
            continue
        md[c["slug"]] = {
            "n": c["name"],
            "f": c["flag"],
            "m": [
                {"n": m.get("name", ""), "s": (m.get("status") or "").lower(), "t": m.get("note", "")}
                for m in c["meds"]
            ],
        }
    md_json = json.dumps(md, ensure_ascii=False)

    # Options for the country-select
    country_options = "\n".join(
        f'        <option value="{c["slug"]}">{html.escape(c["name"])}</option>'
        for c in sorted(country_data, key=lambda x: x["name"] or "")
        if c["meds"]
    )

    replacements = {
        "__REVIEW_DATE__": REVIEW_DATE,
        "__TODAY__": today,
        "__COUNTRIES_COUNT__": str(countries_count),
        "__MED_ENTRIES_COUNT__": str(med_entries_count),
        "__TIER1_COUNT__": str(len(TIER1)),
        "__TIER1_CHIPS__": render_tier1_chips(),
        "__COUNTRY_OPTIONS__": country_options,
        "__MD_JSON__": md_json,
        "__FAQS__": render_faq_accordion(HUB_FAQS, id_prefix="meds-faq"),
        "__SHARED_STYLES__": SHARED_STYLES,
        "__SCHEMA__": schema_str,
    }
    html_out = apply_replacements(HUB_TEMPLATE, replacements)
    OUT_HUB.write_text(html_out)
    print(f"Wrote {OUT_HUB.relative_to(ROOT)} ({len(html_out):,} chars)")


def build_tier1(tier1: dict, aggregated: dict, today: str):
    banned = aggregated[tier1["slug"]]["banned"]
    restricted = aggregated[tier1["slug"]]["restricted"]
    country_counts = {"banned": len(banned), "restricted": len(restricted)}

    schema_str = json.dumps(render_tier1_schema(tier1, country_counts, today), ensure_ascii=False, indent=2)

    warnings_html = "\n    ".join(
        render_tone_callout(c["tone"], c["title"], c["body"]) for c in tier1["headline_warnings"]
    )

    replacements = {
        "__SLUG__": tier1["slug"],
        "__NAME__": html.escape(tier1["canonical_name"]),
        "__PAGE_TITLE__": html.escape(tier1["page_title"]),
        "__META_DESCRIPTION__": html.escape(tier1["meta_description"]),
        "__ICON__": tier1["icon"],
        "__SUMMARY__": html.escape(tier1["summary"]),
        "__ALSO_KNOWN_AS__": ", ".join(html.escape(n) for n in tier1["also_known_as"]),
        "__WHAT_ASKED__": html.escape(tier1["what_travelers_ask"]),
        "__WARNINGS__": warnings_html,
        "__STRATEGY_STEPS__": render_strategy_steps(tier1["travel_strategy"]),
        "__BANNED_LIST__": render_country_list(
            banned, "No countries in our database have an outright ban — but restrictions still apply; check the list below and the full country page."
        ),
        "__RESTRICTED_LIST__": render_country_list(
            restricted, "No countries in our database restrict this medication — but always verify before traveling."
        ),
        "__BANNED_COUNT__": str(len(banned)),
        "__RESTRICTED_COUNT__": str(len(restricted)),
        "__FAQS__": render_faq_accordion(tier1["faqs"], id_prefix=f"{tier1['slug']}-faq"),
        "__BOOK_CTA__": render_medication_book_cta(
            tier1["canonical_name"],
            [e["slug"] for e in banned],
            [e["slug"] for e in restricted],
        ),
        "__SHARED_STYLES__": SHARED_STYLES,
        "__SCHEMA__": schema_str,
        "__REVIEW_DATE__": REVIEW_DATE,
        "__TODAY__": today,
    }
    html_out = apply_replacements(TIER1_TEMPLATE, replacements)
    out_path = OUT_DIR / tier1["slug"] / "index.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_out)
    print(f"Wrote {out_path.relative_to(ROOT)} ({len(html_out):,} chars) — {len(banned)} banned, {len(restricted)} restricted")


def enrich_health_api(aggregated):
    if not HEALTH_API.exists():
        return
    data = json.loads(HEALTH_API.read_text())
    data["tier1Medications"] = [
        {
            "slug": t["slug"],
            "name": t["canonical_name"],
            "url": f"https://tabiji.ai/health/medications/{t['slug']}/",
            "bannedCountries": [e["slug"] for e in aggregated[t["slug"]]["banned"]],
            "restrictedCountries": [e["slug"] for e in aggregated[t["slug"]]["restricted"]],
        }
        for t in TIER1
    ]
    data["medicationsHub"] = "https://tabiji.ai/health/medications/"
    HEALTH_API.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"Enriched {HEALTH_API.relative_to(ROOT)} with tier1Medications")


# -------------------------------------------------------------------
# Templates
# -------------------------------------------------------------------

SHARED_STYLES = r"""
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

    body.editorial-v2 .module-section {
        max-width: 1100px;
        margin: 3rem auto 0;
        padding: 0 1.5rem;
    }
    body.editorial-v2 .module-section > h2 {
        font-family: var(--font-serif);
        font-size: clamp(1.55rem, 3vw, 2rem);
        font-weight: 500;
        color: var(--indigo);
        letter-spacing: -0.01em;
        line-height: 1.2;
        margin-bottom: 0.5rem;
    }
    body.editorial-v2 .module-section > h2 em { color: var(--terracotta); font-style: italic; font-weight: 500; }
    body.editorial-v2 .module-section > p.lede {
        font-family: var(--font-serif);
        font-style: italic;
        font-size: 1.05rem;
        color: var(--text-muted);
        line-height: 1.55;
        max-width: 640px;
        margin-bottom: 1.5rem;
    }

    /* Tier-1 chips grid on hub */
    body.editorial-v2 .tier1-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 0.9rem;
        margin-top: 1rem;
    }
    body.editorial-v2 .tier1-chip {
        display: flex;
        gap: 1rem;
        align-items: flex-start;
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        padding: 1.1rem 1.3rem;
        text-decoration: none;
        color: var(--text);
        transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
    }
    body.editorial-v2 .tier1-chip:hover {
        border-color: var(--terracotta);
        box-shadow: 0 6px 22px rgba(60, 40, 25, 0.09);
        transform: translateY(-2px);
    }
    body.editorial-v2 .tier1-chip .chip-icon { font-size: 1.6rem; line-height: 1; flex-shrink: 0; }
    body.editorial-v2 .tier1-chip .chip-text { display: flex; flex-direction: column; gap: 0.2rem; }
    body.editorial-v2 .tier1-chip strong {
        font-family: var(--font-serif);
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--indigo);
        line-height: 1.2;
    }
    body.editorial-v2 .tier1-chip em {
        font-family: var(--font-serif);
        font-style: italic;
        font-size: 0.9rem;
        color: var(--earth);
    }

    /* Country chips */
    body.editorial-v2 .country-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    body.editorial-v2 .country-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: var(--white);
        border: 1px solid var(--sand);
        border-radius: var(--radius-pill);
        padding: 0.4rem 0.9rem;
        font-family: var(--font-serif);
        font-size: 0.92rem;
        color: var(--indigo);
        text-decoration: none;
        transition: border-color 0.2s, color 0.2s;
    }
    body.editorial-v2 .country-chip:hover {
        border-color: var(--terracotta);
        color: var(--terracotta);
    }
    body.editorial-v2 .country-chip .chip-flag { font-size: 1.05rem; line-height: 1; }
    body.editorial-v2 .empty-list {
        font-family: var(--font-serif);
        font-style: italic;
        color: var(--earth);
        font-size: 0.95rem;
        margin: 0.5rem 0 0;
    }

    /* Search UI on hub */
    body.editorial-v2 .med-search {
        max-width: 680px;
        margin: 1.5rem 0 0;
    }
    body.editorial-v2 .med-search-wrap {
        display: flex;
        align-items: center;
        background: var(--white);
        border: 1px solid var(--sand);
        border-radius: var(--radius-pill);
        padding: 0.15rem 0.5rem 0.15rem 1.2rem;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    body.editorial-v2 .med-search-wrap:focus-within {
        border-color: var(--terracotta);
        box-shadow: 0 2px 12px rgba(196, 112, 75, 0.12);
    }
    body.editorial-v2 .med-search-wrap .search-icon { margin-right: 0.5rem; opacity: 0.6; }
    body.editorial-v2 #med-search {
        flex: 1;
        border: none;
        outline: none;
        background: transparent;
        padding: 0.75rem 0.25rem;
        font-family: var(--font-sans);
        font-size: 0.95rem;
        color: var(--text);
        min-width: 0;
    }
    body.editorial-v2 #med-search::placeholder {
        font-family: var(--font-serif);
        font-style: italic;
        color: var(--earth);
    }
    body.editorial-v2 .search-hint {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin-top: 0.75rem;
        font-family: var(--font-sans);
        font-size: 0.82rem;
        color: var(--earth);
        align-items: center;
    }
    body.editorial-v2 .search-hint span.label { margin-right: 0.25rem; }
    body.editorial-v2 .search-hint button {
        background: var(--white);
        border: 1px solid var(--sand);
        border-radius: var(--radius-pill);
        padding: 0.3rem 0.85rem;
        font-family: var(--font-sans);
        font-size: 0.8rem;
        color: var(--indigo);
        cursor: pointer;
        transition: border-color 0.2s, color 0.2s;
    }
    body.editorial-v2 .search-hint button:hover {
        border-color: var(--terracotta);
        color: var(--terracotta);
    }
    body.editorial-v2 #results, body.editorial-v2 #country-results { margin-top: 1rem; }
    body.editorial-v2 .result-card {
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        padding: 1rem 1.25rem;
        margin-bottom: 0.6rem;
    }
    body.editorial-v2 .result-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 0.5rem;
        flex-wrap: wrap;
    }
    body.editorial-v2 .result-flag { font-size: 1.3rem; line-height: 1; }
    body.editorial-v2 .result-country {
        font-family: var(--font-serif);
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--indigo);
    }
    body.editorial-v2 .result-link {
        margin-left: auto;
        font-family: var(--font-sans);
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--terracotta);
        text-decoration: none;
        border-bottom: 1px solid transparent;
    }
    body.editorial-v2 .result-link:hover { border-bottom-color: var(--terracotta); }
    body.editorial-v2 .med-row {
        display: flex;
        gap: 0.75rem;
        padding: 0.4rem 0;
        border-top: 1px solid var(--sand);
        align-items: flex-start;
    }
    body.editorial-v2 .med-row:first-of-type { border-top: none; }
    body.editorial-v2 .med-status {
        flex-shrink: 0;
        font-family: var(--font-sans);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 0.2rem 0.6rem;
        border-radius: var(--radius-pill);
        min-width: 8ch;
        text-align: center;
    }
    body.editorial-v2 .status-banned { background: #991B1B; color: #FFFFFF; border: 1px solid #7F1D1D; }
    body.editorial-v2 .status-restricted, body.editorial-v2 .status-controlled { background: #92400E; color: #FFFFFF; border: 1px solid #78350F; }
    body.editorial-v2 .med-info .med-name { font-family: var(--font-serif); font-weight: 600; color: var(--indigo); }
    body.editorial-v2 .med-info .med-note { font-family: var(--font-serif); font-size: 0.9rem; color: var(--text-muted); line-height: 1.5; margin-top: 0.2rem; }
    body.editorial-v2 .no-results {
        padding: 1rem 1.25rem;
        background: var(--warm-cream);
        border: 1px dashed var(--sand);
        border-radius: var(--radius-md);
        font-family: var(--font-serif);
        color: var(--text-muted);
    }
    body.editorial-v2 .results-stats {
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
        margin-bottom: 0.75rem;
    }
    body.editorial-v2 .results-stats .stat-item {
        font-family: var(--font-sans);
        font-size: 0.78rem;
        background: var(--white);
        border: 1px solid var(--sand);
        border-radius: var(--radius-pill);
        padding: 0.35rem 0.85rem;
    }

    /* Status legend box (definitions) */
    body.editorial-v2 .status-legend {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    body.editorial-v2 .status-legend-tile {
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        padding: 1.1rem 1.3rem;
    }
    body.editorial-v2 .status-legend-tile.banned { border-left: 4px solid #991B1B; }
    body.editorial-v2 .status-legend-tile.restricted { border-left: 4px solid #92400E; }
    body.editorial-v2 .status-legend-tile.controlled { border-left: 4px solid var(--info); }
    body.editorial-v2 .status-legend-tile h3 {
        font-family: var(--font-serif);
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--indigo);
        margin-bottom: 0.35rem;
    }
    body.editorial-v2 .status-legend-tile p {
        font-family: var(--font-serif);
        font-size: 0.95rem;
        color: var(--text-muted);
        line-height: 1.5;
        margin: 0;
    }

    /* Callouts */
    body.editorial-v2 .med-callout {
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        padding: 1rem 1.3rem;
        margin-bottom: 0.75rem;
    }
    body.editorial-v2 .med-callout-danger { border-left: 4px solid var(--ed-high-text); }
    body.editorial-v2 .med-callout-caution { border-left: 4px solid var(--ed-med-text); }
    body.editorial-v2 .med-callout-info { border-left: 4px solid var(--info); }
    body.editorial-v2 .med-callout-title {
        font-family: var(--font-serif);
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--indigo);
        display: block;
        margin-bottom: 0.25rem;
    }
    body.editorial-v2 .med-callout p {
        font-family: var(--font-serif);
        font-size: 0.95rem;
        color: var(--text-muted);
        line-height: 1.55;
        margin: 0;
    }

    /* Strategy step list (numbered) */
    body.editorial-v2 .strategy-list {
        list-style: none;
        counter-reset: step;
        padding: 0;
        margin-top: 0.5rem;
    }
    body.editorial-v2 .strategy-list li {
        counter-increment: step;
        position: relative;
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        padding: 1rem 1.25rem 1rem 3.5rem;
        margin-bottom: 0.6rem;
    }
    body.editorial-v2 .strategy-list li::before {
        content: "0" counter(step);
        position: absolute;
        left: 1.1rem;
        top: 1rem;
        font-family: var(--font-serif);
        font-weight: 600;
        color: var(--terracotta);
        font-size: 1rem;
    }
    body.editorial-v2 .strategy-list strong {
        font-family: var(--font-serif);
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--indigo);
        display: block;
        margin-bottom: 0.25rem;
    }
    body.editorial-v2 .strategy-list p {
        font-family: var(--font-serif);
        font-size: 0.95rem;
        color: var(--text-muted);
        line-height: 1.55;
        margin: 0;
    }

    /* Tier-1 stats bar */
    body.editorial-v2 .tier1-stats {
        display: flex;
        gap: 0.8rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }
    body.editorial-v2 .tier1-stat {
        background: var(--white);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        padding: 0.8rem 1.1rem;
    }
    body.editorial-v2 .tier1-stat .num {
        font-family: var(--font-serif);
        font-size: 1.8rem;
        font-weight: 600;
        color: var(--indigo);
        line-height: 1;
    }
    body.editorial-v2 .tier1-stat.banned .num { color: #991B1B; }
    body.editorial-v2 .tier1-stat.restricted .num { color: #92400E; }
    body.editorial-v2 .tier1-stat .label {
        font-family: var(--font-sans);
        font-size: 0.72rem;
        font-weight: 700;
        color: var(--earth);
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-top: 0.35rem;
    }

    /* Destination-aware book CTA grid on tier-1 medication pages */
    body.editorial-v2 .med-books-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 0.85rem;
        margin-top: 0.75rem;
    }
    body.editorial-v2 .med-book-card {
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
        background: var(--indigo);
        color: var(--white);
        padding: 1.3rem 1.4rem;
        border-radius: var(--radius-md);
        text-decoration: none;
        transition: transform 0.15s, box-shadow 0.2s;
        position: relative;
        overflow: hidden;
    }
    body.editorial-v2 .med-book-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(45, 58, 92, 0.25);
    }
    body.editorial-v2 .med-book-card::before {
        content: "";
        position: absolute;
        top: -30px;
        right: -30px;
        width: 100px;
        height: 100px;
        background: radial-gradient(circle, rgba(196, 112, 75, 0.22) 0%, transparent 70%);
        pointer-events: none;
    }
    body.editorial-v2 .med-book-card .med-book-eyebrow {
        font-family: var(--font-sans);
        font-size: 0.7rem;
        font-weight: 700;
        color: var(--terracotta);
        letter-spacing: 0.2em;
        text-transform: uppercase;
    }
    body.editorial-v2 .med-book-card strong {
        font-family: var(--font-serif);
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--white);
        line-height: 1.1;
        margin-top: 0.25rem;
    }
    body.editorial-v2 .med-book-card .med-book-cta {
        font-family: var(--font-sans);
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--terracotta);
        margin-top: 0.6rem;
    }
"""

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
    <title>Medication Restrictions by Country — Can I Bring My Meds Abroad? | tabiji.ai</title>
    <meta name="description" content="Travel medication restrictions for __COUNTRIES_COUNT__ countries — Adderall, Sudafed, codeine, CBD, tramadol, Xanax, opioids. What's banned, what needs a permit, and how to travel safely with your prescriptions.">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="https://tabiji.ai/health/medications/">
    <meta property="og:title" content="Can I Bring My Meds Abroad? — Country-by-Country Guide | tabiji.ai">
    <meta property="og:description" content="Travel medication restrictions for __COUNTRIES_COUNT__ countries — Adderall, Sudafed, codeine, CBD, and more.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://tabiji.ai/health/medications/">
    <meta property="og:image" content="https://img.tabiji.ai/tabiji-owl-logo.png">
    <meta property="og:site_name" content="tabiji.ai">

    <script type="application/ld+json">__SCHEMA__</script>

    <link rel="stylesheet" href="/assets/scams.css">
    <style>__SHARED_STYLES__</style>
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

<main>

  <div class="hero">
    <div class="hero-badge">💊 Medication Restrictions</div>
    <h1>Can you travel with <em>your meds?</em></h1>
    <p>Every year, travelers get their medications confiscated — or worse — for drugs that are routine at home and controlled abroad. Adderall, Sudafed, codeine, CBD, Xanax: the rules that catch people by surprise.</p>
    <div class="stats-bar">
      <div class="stat"><strong>__COUNTRIES_COUNT__</strong>Countries</div>
      <div class="stat"><strong>__TIER1_COUNT__</strong>Tier-1 Guides</div>
      <div class="stat"><strong>__MED_ENTRIES_COUNT__</strong>Restriction entries</div>
      <div class="stat"><strong>Monthly</strong>Editorial review</div>
    </div>
  </div>

  <div class="reviewer-strip">
    <strong>Researched by the tabiji editorial team.</strong> Cross-referenced against CDC Yellow Book 2026, country-specific health ministry databases, embassy pharmaceutical import guidelines, and US State Department travel advisories. Last full review: __REVIEW_DATE__. <a href="#methodology">How we build these guides →</a>
  </div>

  <div class="med-disclaimer">
    <strong>⚠️ Not medical or legal advice.</strong> Medication rules change and enforcement varies by airport, official, and day. Always verify with your destination country's embassy or pharmaceutical authority before flying. This page is a starting point, not a substitute for a travel medicine consult or checking with official sources at your destination.
  </div>

  <section class="module-section" id="tier1">
    <span class="section-eyebrow">Deep-dive guides</span>
    <h2>The <em>most-asked</em> medications.</h2>
    <p class="lede">Seven medications account for the majority of traveler-medication incidents at international borders. Each links to a full guide — country list, alternatives, permit process, FAQs.</p>
    <div class="tier1-grid">
__TIER1_CHIPS__
    </div>
  </section>

  <section class="module-section" id="search">
    <span class="section-eyebrow">Search the database</span>
    <h2>Look up your <em>specific medication</em>.</h2>
    <p class="lede">Type a drug name and see which of __COUNTRIES_COUNT__ countries ban or restrict it. Works for generic names (alprazolam), brand names (Xanax), and broad classes (benzodiazepines).</p>
    <div class="med-search">
      <div class="med-search-wrap">
        <span class="search-icon">🔍</span>
        <input type="text" id="med-search" placeholder="e.g. Adderall, codeine, Sudafed, cannabis" autocomplete="off">
      </div>
      <div class="search-hint">
        <span class="label">Popular:</span>
        <button type="button" onclick="doSearch('Adderall')">Adderall</button>
        <button type="button" onclick="doSearch('codeine')">codeine</button>
        <button type="button" onclick="doSearch('Sudafed')">Sudafed</button>
        <button type="button" onclick="doSearch('cannabis')">cannabis</button>
        <button type="button" onclick="doSearch('Xanax')">Xanax</button>
        <button type="button" onclick="doSearch('tramadol')">tramadol</button>
      </div>
    </div>
    <div id="results" aria-live="polite"></div>
  </section>

  <section class="module-section" id="by-country">
    <span class="section-eyebrow">Browse by destination</span>
    <h2>Every restriction for <em>one country</em>.</h2>
    <p class="lede">Pick your destination and see every medication on our database that's banned or restricted there.</p>
    <div class="med-search">
      <select id="country-select" style="width:100%;padding:0.75rem 1rem;font-family:var(--font-sans);font-size:0.95rem;border:1px solid var(--sand);border-radius:var(--radius-md);background:var(--white);color:var(--indigo);">
        <option value="">Select a country…</option>
__COUNTRY_OPTIONS__
      </select>
    </div>
    <div id="country-results" aria-live="polite"></div>
  </section>

  <section class="module-section" id="statuses">
    <span class="section-eyebrow">Status vocabulary</span>
    <h2>What <em>banned, restricted, and controlled</em> actually mean.</h2>
    <p class="lede">These labels get used loosely online. The legal and practical distinctions matter when you're deciding whether to pack a medication.</p>
    <div class="status-legend">
      <div class="status-legend-tile banned">
        <h3>Banned</h3>
        <p>Prohibited entry. No permit, no exception — bringing it in is illegal regardless of prescription. Japan's rule on Adderall is the archetype. Confiscation, detention, or criminal charges.</p>
      </div>
      <div class="status-legend-tile restricted">
        <h3>Restricted</h3>
        <p>Requires advance authorization — usually a pre-travel import permit from the country's health ministry, obtained 2–6 weeks before travel. Legal with the permit, illegal without.</p>
      </div>
      <div class="status-legend-tile controlled">
        <h3>Controlled</h3>
        <p>Classified as a scheduled substance under the country's drug laws. Typically requires declaration at customs, original packaging, prescription, and a doctor's letter — but not a specific import permit. Expect scrutiny; provide documentation.</p>
      </div>
    </div>
  </section>

  <section class="module-section" id="faq">
    <span class="section-eyebrow">Frequently asked</span>
    <h2>Medication travel, <em>answered</em>.</h2>
    <div class="faq-section">
__FAQS__
    </div>
  </section>

  <section class="module-section" id="methodology">
    <span class="section-eyebrow">Methodology</span>
    <h2>How we build these <em>guides</em>.</h2>
    <p class="lede">Per-country medication restrictions are compiled from official pharmaceutical-authority databases, embassy publications, and verified traveler reports. Tier-1 deep-dives add editorial synthesis on top.</p>
    <ol style="list-style:none;counter-reset:step;padding:0;margin-top:1rem;display:flex;flex-direction:column;gap:0.9rem;">
      <li style="counter-increment:step;position:relative;background:var(--warm-cream);border:1px solid var(--sand);border-radius:var(--radius-md);padding:1rem 1.25rem 1rem 3.5rem;">
        <span style="position:absolute;left:1.1rem;top:1rem;font-family:var(--font-serif);font-weight:600;color:var(--terracotta);">01</span>
        <strong style="display:block;font-family:var(--font-serif);font-size:1.05rem;font-weight:600;color:var(--indigo);margin-bottom:0.2rem;">Source from each country's pharmaceutical authority first.</strong>
        <p style="font-family:var(--font-serif);font-size:0.95rem;color:var(--text-muted);line-height:1.55;margin:0;">Japan's PMDA, UAE's Ministry of Health and Prevention, Singapore's Health Sciences Authority, etc. Official lists supersede all other sources.</p>
      </li>
      <li style="counter-increment:step;position:relative;background:var(--warm-cream);border:1px solid var(--sand);border-radius:var(--radius-md);padding:1rem 1.25rem 1rem 3.5rem;">
        <span style="position:absolute;left:1.1rem;top:1rem;font-family:var(--font-serif);font-weight:600;color:var(--terracotta);">02</span>
        <strong style="display:block;font-family:var(--font-serif);font-size:1.05rem;font-weight:600;color:var(--indigo);margin-bottom:0.2rem;">Cross-reference with CDC Yellow Book + embassy publications.</strong>
        <p style="font-family:var(--font-serif);font-size:0.95rem;color:var(--text-muted);line-height:1.55;margin:0;">US embassy abroad pages and CDC's annual Yellow Book catch ambiguities in the primary sources. Conflicts get researched.</p>
      </li>
      <li style="counter-increment:step;position:relative;background:var(--warm-cream);border:1px solid var(--sand);border-radius:var(--radius-md);padding:1rem 1.25rem 1rem 3.5rem;">
        <span style="position:absolute;left:1.1rem;top:1rem;font-family:var(--font-serif);font-weight:600;color:var(--terracotta);">03</span>
        <strong style="display:block;font-family:var(--font-serif);font-size:1.05rem;font-weight:600;color:var(--indigo);margin-bottom:0.2rem;">Err toward stricter status when evidence is mixed.</strong>
        <p style="font-family:var(--font-serif);font-size:0.95rem;color:var(--text-muted);line-height:1.55;margin:0;">When sources disagree, we mark the stricter status (restricted vs controlled) and flag the uncertainty. A traveler over-prepared is safer than under-prepared.</p>
      </li>
      <li style="counter-increment:step;position:relative;background:var(--warm-cream);border:1px solid var(--sand);border-radius:var(--radius-md);padding:1rem 1.25rem 1rem 3.5rem;">
        <span style="position:absolute;left:1.1rem;top:1rem;font-family:var(--font-serif);font-weight:600;color:var(--terracotta);">04</span>
        <strong style="display:block;font-family:var(--font-serif);font-size:1.05rem;font-weight:600;color:var(--indigo);margin-bottom:0.2rem;">Review monthly; correct on reader reports.</strong>
        <p style="font-family:var(--font-serif);font-size:0.95rem;color:var(--text-muted);line-height:1.55;margin:0;">Full editorial pass every four weeks. Reader corrections at hello@tabiji.ai usually ship within 48 hours. Pharmaceutical regulations change more often than most editorial categories.</p>
      </li>
      <li style="counter-increment:step;position:relative;background:var(--warm-cream);border:1px solid var(--sand);border-radius:var(--radius-md);padding:1rem 1.25rem 1rem 3.5rem;">
        <span style="position:absolute;left:1.1rem;top:1rem;font-family:var(--font-serif);font-weight:600;color:var(--terracotta);">05</span>
        <strong style="display:block;font-family:var(--font-serif);font-size:1.05rem;font-weight:600;color:var(--indigo);margin-bottom:0.2rem;">Disclose limits — we are not physicians or pharmacists.</strong>
        <p style="font-family:var(--font-serif);font-size:0.95rem;color:var(--text-muted);line-height:1.55;margin:0;">A travel-safety editorial team, not a clinical one. Our guides save you research time and flag risks — they do not replace a travel-medicine consult, a call to your destination's embassy, or checking with your prescriber about alternatives.</p>
      </li>
    </ol>
  </section>

  <div class="report-cta">
    <h3>Spot an <em>outdated rule?</em></h3>
    <p>Pharmaceutical regulations change. Every correction gets read and usually ships within 48 hours.</p>
    <a href="mailto:hello@tabiji.ai?subject=Medications%20hub%20correction" class="report-cta-btn">Send a correction</a>
  </div>

</main>

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
  var MD = __MD_JSON__;

  function escHtml(s) {
    return String(s).replace(/[&<>"']/g, function(c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function renderResults(matches, banned, restricted) {
    if (!matches.length) return '<div class="no-results">No countries in our database have specific restrictions for this medication. This does not guarantee it is allowed everywhere — always verify with local authorities.</div>';
    var s = '<div class="results-stats">' +
      '<span class="stat-item"><strong>' + matches.length + '</strong> countries</span>' +
      '<span class="stat-item"><strong>' + banned + '</strong> bans</span>' +
      '<span class="stat-item"><strong>' + restricted + '</strong> restrictions</span>' +
      '</div>';
    matches.forEach(function(m) {
      s += '<div class="result-card"><div class="result-header">' +
        '<span class="result-flag">' + m.flag + '</span>' +
        '<span class="result-country">' + escHtml(m.name) + '</span>' +
        '<a href="/health/' + m.slug + '/" class="result-link">Full country guide →</a>' +
        '</div>';
      m.meds.forEach(function(med) {
        s += '<div class="med-row">' +
          '<span class="med-status status-' + med.s + '">' +
          (med.s === 'banned' ? '❌ Banned' : (med.s === 'restricted' ? '⚠️ Restricted' : '📋 Controlled')) +
          '</span>' +
          '<div class="med-info">' +
          '<div class="med-name">' + escHtml(med.n) + '</div>' +
          (med.t ? '<div class="med-note">' + escHtml(med.t) + '</div>' : '') +
          '</div></div>';
      });
      s += '</div>';
    });
    return s;
  }

  function searchMeds(q) {
    q = q.toLowerCase().trim();
    var res = document.getElementById('results');
    if (!q) { res.innerHTML = ''; return; }
    var banned = 0, restricted = 0, matches = [];
    Object.keys(MD).forEach(function(slug) {
      var c = MD[slug];
      var found = c.m.filter(function(m) { return m.n.toLowerCase().indexOf(q) !== -1; });
      if (found.length) {
        matches.push({ slug: slug, name: c.n, flag: c.f, meds: found });
        found.forEach(function(m) { if (m.s === 'banned') banned++; else restricted++; });
      }
    });
    matches.sort(function(a, b) {
      var aB = a.meds.some(function(m) { return m.s === 'banned'; });
      var bB = b.meds.some(function(m) { return m.s === 'banned'; });
      if (aB && !bB) return -1;
      if (!aB && bB) return 1;
      return (a.name || '').localeCompare(b.name || '');
    });
    res.innerHTML = renderResults(matches, banned, restricted);
  }

  window.doSearch = function(q) {
    document.getElementById('med-search').value = q;
    searchMeds(q);
  };

  var medInput = document.getElementById('med-search');
  if (medInput) medInput.addEventListener('input', function(e) { searchMeds(e.target.value); });

  var select = document.getElementById('country-select');
  if (select) {
    select.addEventListener('change', function(e) {
      var slug = e.target.value;
      var cr = document.getElementById('country-results');
      if (!slug) { cr.innerHTML = ''; return; }
      var c = MD[slug];
      if (!c) { cr.innerHTML = ''; return; }
      var banned = 0, restricted = 0;
      c.m.forEach(function(m) { if (m.s === 'banned') banned++; else restricted++; });
      cr.innerHTML = renderResults([{ slug: slug, name: c.n, flag: c.f, meds: c.m }], banned, restricted);
    });
  }

  document.querySelectorAll('.faq-q').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var item = btn.parentElement;
      var open = item.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  var params = new URLSearchParams(window.location.search);
  if (params.get('q') && medInput) window.doSearch(params.get('q'));
  if (params.get('country') && select) {
    select.value = params.get('country');
    select.dispatchEvent(new Event('change'));
  }
})();
</script>

</body>
</html>
"""

TIER1_TEMPLATE = r"""<!DOCTYPE html>
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
    <title>__PAGE_TITLE__ | tabiji.ai</title>
    <meta name="description" content="__META_DESCRIPTION__">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="https://tabiji.ai/health/medications/__SLUG__/">
    <meta property="og:title" content="__PAGE_TITLE__ | tabiji.ai">
    <meta property="og:description" content="__META_DESCRIPTION__">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://tabiji.ai/health/medications/__SLUG__/">
    <meta property="og:image" content="https://img.tabiji.ai/tabiji-owl-logo.png">
    <meta property="og:site_name" content="tabiji.ai">

    <script type="application/ld+json">__SCHEMA__</script>

    <link rel="stylesheet" href="/assets/scams.css">
    <style>__SHARED_STYLES__</style>
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

<main>

  <div class="hero">
    <div class="hero-badge">__ICON__ __NAME__</div>
    <h1>__WHAT_ASKED__</h1>
    <p>__META_DESCRIPTION__</p>
    <div class="hero-meta">
      <span>🕐 Last reviewed __REVIEW_DATE__</span>
    </div>
  </div>

  <div class="reviewer-strip">
    <strong>Researched by the tabiji editorial team.</strong> Cross-referenced against each destination country's pharmaceutical authority, CDC Yellow Book 2026, US State Department guidance, and embassy publications. Last full review: __REVIEW_DATE__. This is not medical or legal advice — always verify with your destination's embassy or pharmaceutical authority before flying, and consult your prescriber about alternatives.
  </div>

  <div class="med-disclaimer">
    <strong>⚠️ Not medical or legal advice.</strong> Medication rules change and enforcement varies. Verify at the official source for your destination before flying. This page is a starting point, not a substitute for a travel-medicine consult.
  </div>

  <section class="module-section" id="summary">
    <span class="section-eyebrow">About</span>
    <h2>What you're <em>dealing with</em>.</h2>
    <p class="lede">__SUMMARY__</p>
    <p style="font-family:var(--font-serif);font-size:0.92rem;color:var(--earth);font-style:italic;"><strong style="font-style:normal;color:var(--indigo);">Also known as:</strong> __ALSO_KNOWN_AS__.</p>
    <div class="tier1-stats">
      <div class="tier1-stat banned"><div class="num">__BANNED_COUNT__</div><div class="label">Countries that ban</div></div>
      <div class="tier1-stat restricted"><div class="num">__RESTRICTED_COUNT__</div><div class="label">Countries that restrict</div></div>
    </div>
  </section>

  <section class="module-section" id="warnings">
    <span class="section-eyebrow">What you need to know</span>
    <h2>The <em>hot spots</em>.</h2>
    __WARNINGS__
  </section>

  <section class="module-section" id="banned">
    <span class="section-eyebrow">Banned countries</span>
    <h2><em>__BANNED_COUNT__ countries</em> where it's prohibited.</h2>
    <p class="lede">These destinations prohibit this medication outright — no permit, no exception. Tap a country for the full health guide.</p>
__BANNED_LIST__
  </section>

  <section class="module-section" id="restricted">
    <span class="section-eyebrow">Restricted countries</span>
    <h2><em>__RESTRICTED_COUNT__ countries</em> where it's controlled.</h2>
    <p class="lede">These destinations allow this medication but require advance paperwork — import permit, declaration, and original packaging. Tap a country for the specifics.</p>
__RESTRICTED_LIST__
  </section>

  <section class="module-section" id="strategy">
    <span class="section-eyebrow">Travel strategy</span>
    <h2>If your <em>destination restricts it</em>.</h2>
    <p class="lede">Five practical steps to travel with this medication legally — or to avoid needing to carry it at all.</p>
    <ol class="strategy-list">
__STRATEGY_STEPS__
    </ol>
  </section>

  <section class="module-section" id="faq">
    <span class="section-eyebrow">Frequently asked</span>
    <h2>__NAME__ <em>abroad</em>, answered.</h2>
    <div class="faq-section">
__FAQS__
    </div>
  </section>

__BOOK_CTA__

  <div class="report-cta">
    <h3>Spot an <em>outdated rule?</em></h3>
    <p>Every correction gets read and usually ships within 48 hours.</p>
    <a href="mailto:hello@tabiji.ai?subject=__NAME__%20correction" class="report-cta-btn">Send a correction</a>
  </div>

</main>

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
document.querySelectorAll('.faq-q').forEach(function(btn) {
  btn.addEventListener('click', function() {
    var item = btn.parentElement;
    var open = item.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
});
</script>

</body>
</html>
"""


if __name__ == "__main__":
    today = date.today().isoformat()
    countries = load_country_medications()
    aggregated = aggregate_by_tier1(countries, TIER1)
    build_hub(countries, aggregated, today)
    for tier1 in TIER1:
        build_tier1(tier1, aggregated, today)
    enrich_health_api(aggregated)
