#!/usr/bin/env python3
"""
build-insurance-hub.py — Generate /health/insurance/index.html in editorial-v2.

Also re-emits /api/v1/health.json with enriched carrier metadata (supplemental
tier, coverage mechanism, icon). Reads the 15 carriers from the current hub,
adds hand-curated editorial fields, and produces the new hub + API.

Usage:
    python3 scripts/build-insurance-hub.py
"""

import html
import json
import sys
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from lib.editorial import (  # noqa: E402
    CARRIERS,
    REVIEW_DATE,
    TIERS,
    apply_replacements,
    render_faq_accordion,
    render_faqs_schema,
    tier_slug,
)

ROOT = SCRIPT_DIR.parent
OUT_HUB = ROOT / "health" / "insurance" / "index.html"
HEALTH_API = ROOT / "api" / "v1" / "health.json"

# FAQ — 18 insurance-specific Q/A used for FAQPage schema + on-page accordion
FAQS = [
    {
        "q": "Does my US health insurance cover me when I travel abroad?",
        "a": "Rarely the way you'd expect. Most US plans cover only emergencies, at out-of-network rates, and require you to pay upfront and file a claim afterwards. Kaiser Permanente, most HMOs, Medicaid plans, and Medicare generally offer very limited or zero international coverage. PPO plans from BCBS, UHC, Aetna, and Cigna are the strongest performers but still leave big gaps.",
    },
    {
        "q": "What's the difference between PPO, HMO, and HDHP for international travel?",
        "a": "PPO plans offer the best international coverage — emergency and sometimes urgent care abroad is covered at out-of-network rates. HMO plans typically restrict coverage to in-network providers, meaning international care may only be covered in true emergencies. HDHP/HSA plans follow the same rules as their PPO or HMO base, but you pay the full deductible first.",
    },
    {
        "q": "Does Medicare cover me abroad?",
        "a": "Original Medicare (Parts A and B) does not cover care outside the US in almost all cases. A handful of narrow exceptions exist — care in Canada or Mexico en route to Alaska, or emergencies within the US that a foreign hospital happens to be closest to. Medicare Advantage plans may offer limited emergency coverage abroad with lifetime caps. Medigap plans F, G, and N include a foreign-travel emergency benefit (80% after deductible, $50,000 lifetime max).",
    },
    {
        "q": "Does Medicaid cover me abroad?",
        "a": "No. Medicaid covers care within the US only, with extremely narrow exceptions for emergencies on the US border. If you have Medicaid and are traveling internationally, supplemental travel medical insurance is essential — plan on out-of-pocket payment for anything that happens overseas.",
    },
    {
        "q": "How much does medical evacuation cost?",
        "a": "$15,000–60,000 for most regional transfers. $100,000–250,000 for intercontinental ICU-level evacuation. Medical evacuation is the single biggest financial risk of serious illness abroad — it's the main reason even people with strong primary coverage buy supplemental travel insurance.",
    },
    {
        "q": "What is BCBS Global Core and how does it work?",
        "a": "BCBS Global Core gives BCBS members access to a network of international doctors and hospitals in 190+ countries. Call 1-800-810-BLUE (2583) before non-emergency care; for emergencies, go to the nearest hospital and call within 48 hours. Many network hospitals can bill BCBS directly, reducing your upfront out-of-pocket.",
    },
    {
        "q": "Is Kaiser Permanente valid internationally?",
        "a": "Barely. Kaiser covers emergency care abroad on a reimbursement basis only — you pay upfront and file a claim. There's no out-of-area routine or urgent care, no international network, and no direct-billing partnerships. Kaiser is the worst major US carrier for international travel; supplemental insurance is essential.",
    },
    {
        "q": "What should I do in a medical emergency abroad?",
        "a": "Call the local emergency number first. Ask for an English-speaking doctor or a hospital with international patient services. Then call your travel insurer's 24/7 assistance line — they can coordinate payment, find accredited facilities, and arrange evacuation if your condition exceeds local capacity. Keep receipts and itemized bills for claims.",
    },
    {
        "q": "How do I file an insurance claim from abroad?",
        "a": "Keep every receipt, itemized bill, and medical report. Ask for English-language documentation — most international hospitals will provide it on request. Pay with a credit card where possible (better audit trail). File the claim with your insurer on return. Travel insurers with 24/7 assistance lines can often direct-bill the hospital if you call first.",
    },
    {
        "q": "How much does travel health insurance cost?",
        "a": "$30–80 for a week, $60–200 for a month, depending on age, coverage limits, and trip type. Comprehensive plans with evacuation coverage ($250K+) typically run $40–150 for a two-week trip. Expats and long-stay travelers need dedicated international plans that run $150–400+ per month.",
    },
    {
        "q": "Which supplemental travel insurance providers should I look at?",
        "a": "Popular options include World Nomads (good for adventure travel), GeoBlue (BCBS affiliate, strong for frequent travelers), IMG Global (long-stay and expat), Allianz Travel (broad coverage, large company), and Travel Guard (AIG-backed). Compare coverage limits, medical evacuation caps, pre-existing condition rules, and adventure-activity exclusions before buying.",
    },
    {
        "q": "Do I need supplemental travel insurance if I have a strong PPO?",
        "a": "Yes, in most cases. Even strong PPO coverage typically doesn't include medical evacuation (the largest financial risk), trip cancellation, or non-emergency care. A supplemental travel policy fills these gaps for $30–80 a week. Above age 65 or for trips longer than two weeks, supplemental coverage is effectively mandatory.",
    },
    {
        "q": "Are pre-existing conditions covered?",
        "a": "Most supplemental travel insurance policies exclude pre-existing conditions unless you purchase a waiver (usually requires buying the policy within 10–21 days of your initial trip deposit). Primary US plans don't apply pre-existing exclusions, but their international coverage is limited in other ways.",
    },
    {
        "q": "What's the difference between travel medical and trip cancellation insurance?",
        "a": "Travel medical insurance covers healthcare costs, medical evacuation, and repatriation if something happens while you're traveling. Trip cancellation insurance reimburses prepaid costs if you can't go or have to cut the trip short. They're often sold together as 'travel insurance' — check carefully what you're getting. For health safety, medical coverage is the essential piece.",
    },
    {
        "q": "Does my credit card provide travel medical coverage?",
        "a": "Most premium travel credit cards (Amex Platinum, Chase Sapphire Reserve, etc.) include some travel medical coverage, but limits are typically low ($2,500–25,000) and medical evacuation is rarely included at useful levels. Treat credit-card coverage as a supplement to, not a replacement for, dedicated travel medical insurance.",
    },
    {
        "q": "I'm visiting the US from abroad — does my home country's insurance cover me?",
        "a": "Varies widely. European EHIC/GHIC is not valid in the US. Many countries' public health plans cover emergencies only in the US, with low limits. If you're visiting the US, a dedicated travel medical policy is essential — US healthcare costs are the highest in the world and a single ER visit can exceed most national health systems' international coverage caps.",
    },
    {
        "q": "What questions should I ask my carrier before I travel?",
        "a": "Ask: (1) Is international emergency care covered at in-network or out-of-network rates? (2) Is medical evacuation included? (3) Do I need pre-authorization for non-emergency care abroad? (4) What's my out-of-network deductible and coinsurance? (5) Is there a per-incident or annual cap on international coverage? Get answers in writing — verbal confirmations don't hold up at claim time.",
    },
    {
        "q": "Does tabiji earn commission on insurance recommendations?",
        "a": "No. We don't have affiliate relationships with any US health insurance carrier or travel insurance provider. Our rankings reflect our editorial view of coverage quality based on published plan documents and consumer reports. If that ever changes, we'll disclose it prominently — we'd rather tell you the truth than sell you a policy.",
    },
]

# Decision tree pieces for the interactive "Not sure what you need?" widget
DEST_TIERS = {
    "high-cost": {
        "label": "High-cost healthcare (Japan, Switzerland, Australia, Singapore, Nordic)",
        "examples": "japan, switzerland, australia, singapore, norway, iceland",
        "note": "Supplemental is a must. A single ER visit in Tokyo or Zurich can run $15K+ upfront.",
    },
    "medium-cost": {
        "label": "Standard developed market (Western Europe, Canada, South Korea)",
        "examples": "france, germany, italy, spain, canada",
        "note": "Supplemental strongly recommended. Quality care but out-of-pocket can still hit five figures.",
    },
    "low-cost": {
        "label": "Low-cost healthcare (Southeast Asia, Mexico, most of Latin America)",
        "examples": "thailand, mexico, vietnam, costa rica",
        "note": "Supplemental still worth it for medical evacuation coverage alone.",
    },
    "high-risk": {
        "label": "Remote / high medevac risk (Himalayas, Andes, Mongolia, Pacific islands)",
        "examples": "nepal, bolivia, mongolia, papua new guinea, madagascar",
        "note": "Medical evacuation coverage is the #1 reason to buy insurance here. Aim for $250K+ evac limit.",
    },
}

# -------------------------------------------------------------------
# Templates
# -------------------------------------------------------------------

def _evac_status(c: dict) -> str:
    """Medevac-coverage cell text for the comparison matrix."""
    if c["slug"] in ("kaiser-permanente", "humana", "centene", "molina-healthcare"):
        return "Rarely"
    if "BCBS" in c["mechanism"] or "Global Core" in c["mechanism"]:
        return "Varies"
    return "Check plan"


def render_carrier_cards() -> str:
    out = []
    for c in CARRIERS:
        tslug = tier_slug(c["supp_tier"])
        out.append(
            f'      <a href="/health/insurance/{c["slug"]}/" class="carrier-card" '
            f'data-tier="{tslug}" data-mechanism="{html.escape(c["mechanism"])}">\n'
            f'        <div class="carrier-icon">{c["icon"]}</div>\n'
            f'        <div class="carrier-body">\n'
            f'          <h3 class="carrier-name">{html.escape(c["name"])}</h3>\n'
            f'          <p class="carrier-headline">{html.escape(c["coverage_headline"])}</p>\n'
            f'          <p class="carrier-short">{html.escape(c["short"])}</p>\n'
            f'          <div class="carrier-meta">\n'
            f'            <span class="supp-tier supp-{tslug}">'
            f'Supplemental: <strong>{html.escape(c["supp_tier"])}</strong></span>\n'
            f'            <span class="plan-types">{html.escape(c["plan_types"])}</span>\n'
            f'          </div>\n'
            f'        </div>\n'
            f'        <span class="carrier-arrow">Read the guide →</span>\n'
            f'      </a>'
        )
    return "\n".join(out)


def render_matrix_rows() -> str:
    rows = []
    for c in CARRIERS:
        tslug = tier_slug(c["supp_tier"])
        rows.append(
            f'      <tr>\n'
            f'        <td class="matrix-carrier">'
            f'<a href="/health/insurance/{c["slug"]}/">{c["icon"]} {html.escape(c["name"])}</a></td>\n'
            f'        <td class="matrix-mechanism">{html.escape(c["mechanism"])}</td>\n'
            f'        <td class="matrix-tier supp-{tslug}">{html.escape(c["supp_tier"])}</td>\n'
            f'        <td class="matrix-evac">{_evac_status(c)}</td>\n'
            f'      </tr>'
        )
    return "\n".join(rows)


def render_carrier_select_options() -> str:
    opts = ['      <option value="">— Your carrier —</option>']
    for c in CARRIERS:
        opts.append(f'      <option value="{c["slug"]}">{html.escape(c["name"])}</option>')
    return "\n".join(opts)


def render_carrier_decision_data_js() -> str:
    data = {
        c["slug"]: {"tier": c["supp_tier"], "mechanism": c["mechanism"], "note": c["short"]}
        for c in CARRIERS
    }
    return json.dumps(data, ensure_ascii=False)


def render_dest_tiers_js() -> str:
    return json.dumps(DEST_TIERS, ensure_ascii=False)


# -------------------------------------------------------------------
# Main generators
# -------------------------------------------------------------------

def build_hub():
    today = date.today().isoformat()

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "FinancialProduct",
                "name": "US health insurance — international travel coverage guides",
                "description": (
                    "Carrier-by-carrier breakdown of international travel coverage for the top 15 US "
                    "health insurance companies — BCBS, UnitedHealthcare, Aetna, Cigna, Kaiser, Humana, "
                    "Anthem, Centene, HCSC, Highmark, Molina, Premera, Regence, CareFirst, "
                    "Independence Blue Cross."
                ),
                "category": "HealthInsurance",
                "url": "https://tabiji.ai/health/insurance/",
            },
            {
                "@type": "CollectionPage",
                "name": "Travel Health Insurance by Carrier",
                "headline": "Does your US health plan cover you abroad?",
                "description": (
                    "Carrier-by-carrier international travel coverage guides for BCBS, UnitedHealthcare, "
                    "Aetna, Cigna, Kaiser, Humana, Anthem, Centene, HCSC, Highmark, Molina, Premera, "
                    "Regence, CareFirst, and Independence Blue Cross. What's covered, what's not, PPO vs "
                    "HMO differences, medical-evacuation reality-checks, and whether you need "
                    "supplemental travel insurance."
                ),
                "url": "https://tabiji.ai/health/insurance/",
                "inLanguage": "en",
                "datePublished": "2026-03-01",
                "dateModified": today,
                "lastReviewed": today,
                "reviewedBy": {
                    "@type": "Organization",
                    "name": "tabiji editorial team",
                    "url": "https://tabiji.ai/about/",
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "tabiji.ai",
                    "url": "https://tabiji.ai",
                    "logo": {"@type": "ImageObject", "url": "https://img.tabiji.ai/tabiji-owl-logo.png"},
                },
                "audience": {"@type": "PeopleAudience", "audienceType": "US residents traveling internationally"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tabiji.ai/"},
                    {"@type": "ListItem", "position": 2, "name": "Travel Health", "item": "https://tabiji.ai/health/"},
                    {"@type": "ListItem", "position": 3, "name": "Insurance by Carrier", "item": "https://tabiji.ai/health/insurance/"},
                ],
            },
            {"@type": "FAQPage", "mainEntity": render_faqs_schema(FAQS)},
            {
                "@type": "ItemList",
                "name": "US Health Insurance Carriers",
                "numberOfItems": len(CARRIERS),
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": i + 1,
                        "name": c["name"],
                        "url": f"https://tabiji.ai/health/insurance/{c['slug']}/",
                    }
                    for i, c in enumerate(CARRIERS)
                ],
            },
        ],
    }
    schema_str = json.dumps(schema, ensure_ascii=False, indent=2)

    replacements = {
        "__REVIEW_DATE__": REVIEW_DATE,
        "__TODAY__": today,
        "__SCHEMA__": schema_str,
        "__CARRIER_COUNT__": str(len(CARRIERS)),
        "__CARRIER_SELECT_OPTIONS__": render_carrier_select_options(),
        "__MATRIX_ROWS__": render_matrix_rows(),
        "__CARRIER_CARDS__": render_carrier_cards(),
        "__FAQS__": render_faq_accordion(FAQS, id_prefix="ifaq"),
        "__CARRIER_DECISION_DATA__": render_carrier_decision_data_js(),
        "__DEST_TIERS__": render_dest_tiers_js(),
    }
    html_out = apply_replacements(HUB_TEMPLATE, replacements)
    OUT_HUB.write_text(html_out)
    print(f"Wrote {OUT_HUB} ({len(html_out):,} chars, {len(CARRIERS)} carriers)")


def enrich_health_api():
    """Re-emit /api/v1/health.json with enriched carrier fields."""
    if not HEALTH_API.exists():
        print(f"Skipping health API enrichment — {HEALTH_API} does not exist yet.")
        return
    data = json.loads(HEALTH_API.read_text())
    enriched = []
    for c in CARRIERS:
        enriched.append({
            "slug": c["slug"],
            "name": c["name"],
            "url": f"https://tabiji.ai/health/insurance/{c['slug']}/",
            "supplementalTier": c["supp_tier"],
            "coverageMechanism": c["mechanism"],
            "coverageHeadline": c["coverage_headline"],
            "planTypes": c["plan_types"],
            "assistancePhone": c["assistance_phone"],
        })
    data["insuranceCarriers"] = enriched
    data["totalCarriers"] = len(enriched)
    HEALTH_API.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"Enriched {HEALTH_API} with carrier fields")


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
    <title>Does Your US Health Plan Cover You Abroad? — Carrier-by-Carrier Guides | tabiji.ai</title>
    <meta name="description" content="Travel health insurance guides for the top 15 US carriers — BCBS, UnitedHealthcare, Aetna, Cigna, Kaiser, Humana, and more. What's covered, what's not, PPO vs HMO, evacuation, and whether you need supplemental travel insurance.">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="https://tabiji.ai/health/insurance/">
    <meta property="og:title" content="US Health Insurance Abroad — Carrier-by-Carrier Reality-Check | tabiji.ai">
    <meta property="og:description" content="Does your US health insurance cover you abroad? Carrier-by-carrier guides for 15 top insurers.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://tabiji.ai/health/insurance/">
    <meta property="og:image" content="https://img.tabiji.ai/tabiji-owl-logo.png">
    <meta property="og:site_name" content="tabiji.ai">
    <meta name="twitter:card" content="summary_large_image">

    <script type="application/ld+json">__SCHEMA__</script>

    <link rel="stylesheet" href="/assets/scams.css">
    <style>
    /* Insurance-hub-specific additions on top of editorial-v2 */

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
    }
    body.editorial-v2 .reviewer-strip strong { font-style: normal; color: var(--indigo); }
    body.editorial-v2 .reviewer-strip a {
        color: var(--terracotta);
        text-decoration: none;
        border-bottom: 1px solid transparent;
        font-style: normal;
        font-weight: 600;
    }
    body.editorial-v2 .reviewer-strip a:hover { border-bottom-color: var(--terracotta); }

    body.editorial-v2 .affiliate-disclosure {
        max-width: 860px;
        margin: 0.75rem auto 0;
        padding: 0.75rem 1.25rem;
        background: var(--warm-cream-soft);
        border: 1px dashed var(--sand);
        border-radius: var(--radius-md);
        font-family: var(--font-serif);
        font-style: italic;
        font-size: 0.9rem;
        color: var(--earth);
        line-height: 1.5;
    }
    body.editorial-v2 .affiliate-disclosure strong { color: var(--indigo); font-style: normal; }

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
        max-width: 640px;
        margin-bottom: 1.75rem;
    }

    /* Why-this-matters cost callouts */
    body.editorial-v2 .cost-callouts {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
        margin-top: 1.5rem;
    }
    body.editorial-v2 .cost-callout {
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-left: 4px solid var(--terracotta);
        border-radius: var(--radius-md);
        padding: 1.1rem 1.3rem;
    }
    body.editorial-v2 .cost-callout .cost-label {
        font-family: var(--font-sans);
        font-size: 0.7rem;
        font-weight: 700;
        color: var(--terracotta);
        letter-spacing: 0.22em;
        text-transform: uppercase;
        display: block;
        margin-bottom: 0.25rem;
    }
    body.editorial-v2 .cost-callout .cost-amount {
        font-family: var(--font-serif);
        font-size: 1.6rem;
        font-weight: 600;
        color: var(--indigo);
        line-height: 1.1;
        margin-bottom: 0.2rem;
    }
    body.editorial-v2 .cost-callout p {
        font-family: var(--font-serif);
        font-style: italic;
        font-size: 0.9rem;
        color: var(--text-muted);
        line-height: 1.5;
        margin: 0;
    }

    /* Decision tree */
    body.editorial-v2 .decision-panel {
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-radius: var(--radius-lg);
        padding: 1.75rem 2rem;
        margin-top: 1rem;
    }
    body.editorial-v2 .decision-step {
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
        margin-bottom: 1.25rem;
    }
    body.editorial-v2 .decision-step:last-of-type { margin-bottom: 0; }
    body.editorial-v2 .decision-step label {
        font-family: var(--font-sans);
        font-size: 0.72rem;
        font-weight: 700;
        color: var(--earth);
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }
    body.editorial-v2 .decision-step select {
        background: var(--white);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        padding: 0.6rem 0.85rem;
        font-family: var(--font-sans);
        font-size: 0.95rem;
        color: var(--indigo);
        max-width: 400px;
    }
    body.editorial-v2 .decision-step select:focus {
        outline: 2px solid var(--terracotta);
        outline-offset: 1px;
    }
    body.editorial-v2 .decision-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
    }
    body.editorial-v2 .decision-pill {
        background: var(--white);
        border: 1px solid var(--sand);
        border-radius: var(--radius-pill);
        padding: 0.45rem 0.95rem;
        font-family: var(--font-sans);
        font-size: 0.82rem;
        font-weight: 500;
        color: var(--indigo);
        cursor: pointer;
        transition: border-color 0.2s, color 0.2s, background 0.2s;
    }
    body.editorial-v2 .decision-pill:hover { border-color: var(--terracotta); color: var(--terracotta); }
    body.editorial-v2 .decision-pill.active {
        background: var(--terracotta);
        border-color: var(--terracotta);
        color: var(--white);
    }
    body.editorial-v2 .decision-result {
        margin-top: 1.5rem;
        padding: 1.25rem 1.5rem;
        background: var(--white);
        border: 1px solid var(--sand);
        border-left: 4px solid var(--terracotta);
        border-radius: var(--radius-md);
        font-family: var(--font-serif);
        line-height: 1.55;
    }
    body.editorial-v2 .decision-result[hidden] { display: none; }
    body.editorial-v2 .decision-result .decision-verdict {
        font-family: var(--font-serif);
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--indigo);
        display: block;
        margin-bottom: 0.35rem;
    }
    body.editorial-v2 .decision-result .decision-verdict em {
        font-style: italic;
        color: var(--terracotta);
    }
    body.editorial-v2 .decision-result p {
        margin: 0 0 0.5rem;
        color: var(--text);
    }
    body.editorial-v2 .decision-result .decision-note {
        font-family: var(--font-serif);
        font-style: italic;
        font-size: 0.92rem;
        color: var(--text-muted);
    }
    body.editorial-v2 .decision-result a {
        font-family: var(--font-sans);
        font-weight: 600;
        font-size: 0.9rem;
        color: var(--terracotta);
        text-decoration: none;
        border-bottom: 1px solid transparent;
    }
    body.editorial-v2 .decision-result a:hover { border-bottom-color: var(--terracotta); }

    /* Comparison matrix */
    body.editorial-v2 .matrix-wrap {
        max-width: 1100px;
        margin-top: 1rem;
        overflow-x: auto;
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        background: var(--white);
    }
    body.editorial-v2 table.matrix {
        border-collapse: collapse;
        width: 100%;
        font-family: var(--font-sans);
        font-size: 0.9rem;
    }
    body.editorial-v2 table.matrix th {
        background: var(--warm-cream);
        font-family: var(--font-sans);
        font-size: 0.72rem;
        font-weight: 700;
        color: var(--earth);
        letter-spacing: 0.14em;
        text-transform: uppercase;
        text-align: left;
        padding: 0.85rem 1rem;
        border-bottom: 1px solid var(--sand);
    }
    body.editorial-v2 table.matrix td {
        padding: 0.85rem 1rem;
        border-bottom: 1px solid var(--sand);
        vertical-align: top;
    }
    body.editorial-v2 table.matrix tr:last-child td { border-bottom: none; }
    body.editorial-v2 table.matrix tr:hover td { background: var(--warm-cream-soft); }
    body.editorial-v2 table.matrix .matrix-carrier a {
        font-family: var(--font-serif);
        font-size: 1rem;
        font-weight: 600;
        color: var(--indigo);
        text-decoration: none;
    }
    body.editorial-v2 table.matrix .matrix-carrier a:hover { color: var(--terracotta); }
    body.editorial-v2 table.matrix .matrix-tier {
        font-weight: 600;
    }
    body.editorial-v2 .matrix-tier.supp-essential { color: var(--ed-high-text); }
    body.editorial-v2 .matrix-tier.supp-strongly-recommended { color: var(--ed-med-text); }
    body.editorial-v2 .matrix-tier.supp-recommended { color: var(--ed-low-text); }

    /* Medicare / Medicaid callouts */
    body.editorial-v2 .gov-callouts {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.25rem;
        margin-top: 1rem;
    }
    body.editorial-v2 .gov-callout {
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-left: 4px solid var(--ed-high-text);
        border-radius: var(--radius-md);
        padding: 1.25rem 1.4rem;
    }
    body.editorial-v2 .gov-callout h3 {
        font-family: var(--font-serif);
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--indigo);
        margin-bottom: 0.5rem;
        letter-spacing: -0.005em;
    }
    body.editorial-v2 .gov-callout h3 em {
        font-style: italic;
        color: var(--ed-high-text);
        font-weight: 500;
    }
    body.editorial-v2 .gov-callout p {
        font-size: 0.92rem;
        color: var(--text-muted);
        line-height: 1.55;
        margin: 0 0 0.5rem;
    }
    body.editorial-v2 .gov-callout p:last-child { margin-bottom: 0; }
    body.editorial-v2 .gov-callout .gov-exception {
        font-family: var(--font-serif);
        font-style: italic;
        font-size: 0.88rem;
        color: var(--earth);
    }

    /* Non-US visitors callout */
    body.editorial-v2 .visitors-callout {
        background: var(--warm-cream-soft);
        border: 1px solid var(--sand);
        border-left: 4px solid var(--sage);
        border-radius: var(--radius-md);
        padding: 1.25rem 1.5rem;
        margin-top: 1rem;
    }
    body.editorial-v2 .visitors-callout h3 {
        font-family: var(--font-serif);
        font-size: 1.15rem;
        font-weight: 600;
        color: var(--indigo);
        margin-bottom: 0.5rem;
    }
    body.editorial-v2 .visitors-callout p {
        font-size: 0.95rem;
        color: var(--text-muted);
        line-height: 1.6;
        margin: 0 0 0.6rem;
    }

    /* Carrier directory cards */
    body.editorial-v2 .carrier-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    body.editorial-v2 .carrier-card {
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        padding: 1.35rem 1.4rem 1.25rem;
        text-decoration: none;
        color: var(--text);
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
    }
    body.editorial-v2 .carrier-card:hover {
        border-color: var(--terracotta);
        box-shadow: 0 6px 22px rgba(60, 40, 25, 0.09);
        transform: translateY(-2px);
    }
    body.editorial-v2 .carrier-card .carrier-icon {
        font-size: 1.8rem;
        line-height: 1;
    }
    body.editorial-v2 .carrier-card .carrier-body {
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
    }
    body.editorial-v2 .carrier-card .carrier-name {
        font-family: var(--font-serif);
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--indigo);
        margin: 0;
        letter-spacing: -0.005em;
    }
    body.editorial-v2 .carrier-card .carrier-headline {
        font-family: var(--font-serif);
        font-style: italic;
        font-size: 0.92rem;
        color: var(--earth);
        margin: 0;
        line-height: 1.45;
    }
    body.editorial-v2 .carrier-card .carrier-short {
        font-size: 0.88rem;
        color: var(--text-muted);
        margin: 0.2rem 0 0;
        line-height: 1.5;
    }
    body.editorial-v2 .carrier-card .carrier-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem 1rem;
        align-items: center;
        margin-top: 0.4rem;
        padding-top: 0.55rem;
        border-top: 1px solid var(--sand);
    }
    body.editorial-v2 .carrier-card .supp-tier {
        font-family: var(--font-sans);
        font-size: 0.78rem;
        color: var(--indigo);
        font-weight: 500;
    }
    body.editorial-v2 .carrier-card .supp-tier strong {
        font-weight: 700;
    }
    body.editorial-v2 .supp-essential strong { color: var(--ed-high-text); }
    body.editorial-v2 .supp-strongly-recommended strong { color: var(--ed-med-text); }
    body.editorial-v2 .supp-recommended strong { color: var(--ed-low-text); }
    body.editorial-v2 .carrier-card .plan-types {
        font-family: var(--font-serif);
        font-style: italic;
        font-size: 0.82rem;
        color: var(--earth);
    }
    body.editorial-v2 .carrier-card .carrier-arrow {
        font-family: var(--font-sans);
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--terracotta);
        margin-top: 0.2rem;
        opacity: 0.85;
        transition: opacity 0.2s, transform 0.2s;
    }
    body.editorial-v2 .carrier-card:hover .carrier-arrow { opacity: 1; transform: translateX(3px); }

    /* Methodology block */
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

    @media (max-width: 768px) {
        body.editorial-v2 .carrier-grid { grid-template-columns: 1fr; }
        body.editorial-v2 .decision-panel { padding: 1.25rem 1.25rem; }
        body.editorial-v2 table.matrix th, body.editorial-v2 table.matrix td { padding: 0.7rem 0.75rem; font-size: 0.85rem; }
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

<div class="breadcrumb"><a href="/">Home</a><span>›</span><a href="/health/">Travel Health</a><span>›</span>Insurance by Carrier</div>

<main>

  <div class="hero">
    <div class="hero-badge">🛡️ Insurance Research</div>
    <h1>Does your US health plan <em>cover you abroad?</em></h1>
    <p>Carrier-by-carrier international coverage for the top 15 US insurers. What's covered, what's not, and whether you need supplemental travel insurance.</p>
    <div class="stats-bar">
      <div class="stat"><strong>__CARRIER_COUNT__</strong>US Carriers</div>
      <div class="stat"><strong>210</strong>Country Guides</div>
      <div class="stat"><strong>Monthly</strong>Editorial Review</div>
      <div class="stat"><strong>Free</strong>Always</div>
    </div>
  </div>

  <div class="reviewer-strip">
    <strong>Researched by the tabiji editorial team.</strong> Cross-referenced against carrier plan documents, Summary of Benefits and Coverage filings, the NAIC (National Association of Insurance Commissioners), the US Department of State's travel insurance guidance, and independent consumer reports. Last full review: __REVIEW_DATE__. This is not insurance advice — always verify coverage with your specific plan before you travel.
  </div>

  <div class="affiliate-disclosure">
    <strong>No affiliate commissions.</strong> We don't earn anything from any US health insurance carrier or supplemental travel insurance provider named on these pages. Rankings reflect our editorial view of coverage quality only. If that ever changes, we'll disclose it prominently.
  </div>

  <!-- Module 1 — Why this matters, made concrete -->
  <section class="module-section" id="why">
    <span class="section-eyebrow">Why this matters</span>
    <h2>Three numbers that <em>change the math</em>.</h2>
    <p class="lede">Most Americans assume their plan travels with them. It doesn't. Coverage varies wildly by carrier, plan type, and even specific employer group — and the costs when you're wrong are very real.</p>
    <div class="cost-callouts">
      <div class="cost-callout">
        <span class="cost-label">ER visit abroad</span>
        <div class="cost-amount">$5K–50K+</div>
        <p>Paid upfront at most international hospitals, then claimed back. Japan, Switzerland, Australia skew to the high end.</p>
      </div>
      <div class="cost-callout">
        <span class="cost-label">Medical evacuation</span>
        <div class="cost-amount">$50K–250K</div>
        <p>ICU-level intercontinental transfers. Rarely included in primary US plans. The #1 reason to buy supplemental insurance.</p>
      </div>
      <div class="cost-callout">
        <span class="cost-label">Supplemental policy</span>
        <div class="cost-amount">$30–80 / week</div>
        <p>The cost of fixing all of the above. Less than an airport meal. Do the math.</p>
      </div>
    </div>
  </section>

  <!-- Module 2 — Decision tree -->
  <section class="module-section" id="decide">
    <span class="section-eyebrow">Not sure what you need?</span>
    <h2>Three questions, <em>one recommendation</em>.</h2>
    <p class="lede">Pick your carrier, destination type, and trip length. We'll translate that into a supplemental-insurance recommendation with rough cost guidance.</p>
    <div class="decision-panel">
      <div class="decision-step">
        <label for="decide-carrier">Your US health insurance carrier</label>
        <select id="decide-carrier">
__CARRIER_SELECT_OPTIONS__
          <option value="other">Other / not listed</option>
          <option value="medicare">Medicare (original)</option>
          <option value="medicaid">Medicaid</option>
        </select>
      </div>
      <div class="decision-step">
        <label>Destination type</label>
        <div class="decision-pills" data-group="dest">
          <button type="button" class="decision-pill" data-value="high-cost">High-cost healthcare (Japan, Switzerland, Australia)</button>
          <button type="button" class="decision-pill" data-value="medium-cost">Western Europe / Canada / South Korea</button>
          <button type="button" class="decision-pill" data-value="low-cost">Thailand, Mexico, Latin America, SE Asia</button>
          <button type="button" class="decision-pill" data-value="high-risk">Remote / high medevac risk (Himalayas, Andes, Pacific)</button>
        </div>
      </div>
      <div class="decision-step">
        <label>Trip length</label>
        <div class="decision-pills" data-group="length">
          <button type="button" class="decision-pill" data-value="weekend">Long weekend</button>
          <button type="button" class="decision-pill" data-value="week">1–2 weeks</button>
          <button type="button" class="decision-pill" data-value="month">3–4 weeks</button>
          <button type="button" class="decision-pill" data-value="extended">Month+ / expat</button>
        </div>
      </div>
      <div class="decision-result" id="decide-result" hidden>
        <span class="decision-verdict" id="decide-verdict"></span>
        <p id="decide-body"></p>
        <p class="decision-note" id="decide-note"></p>
        <a id="decide-link" href="#">Read the full carrier guide →</a>
      </div>
    </div>
  </section>

  <!-- Module 3 — Comparison matrix -->
  <section class="module-section" id="matrix">
    <span class="section-eyebrow">Comparison matrix</span>
    <h2>All 15 carriers, <em>side by side</em>.</h2>
    <p class="lede">Same four columns for every carrier. Skim to find yours, then click through for the full breakdown.</p>
    <div class="matrix-wrap">
      <table class="matrix">
        <thead>
          <tr>
            <th>Carrier</th>
            <th>Coverage mechanism abroad</th>
            <th>Supplemental</th>
            <th>Medical evacuation</th>
          </tr>
        </thead>
        <tbody>
__MATRIX_ROWS__
        </tbody>
      </table>
    </div>
  </section>

  <!-- Module 4 — Medicare & Medicaid reality -->
  <section class="module-section" id="medicare-medicaid">
    <span class="section-eyebrow">Medicare & Medicaid reality</span>
    <h2>The two plans that <em>don't follow you</em> overseas.</h2>
    <p class="lede">If you have original Medicare or any Medicaid plan, your international coverage is close to zero. Here's exactly what that means and what to do about it.</p>
    <div class="gov-callouts">
      <div class="gov-callout">
        <h3>🏥 Medicare <em>rarely travels</em>.</h3>
        <p>Original Medicare (Parts A and B) does not cover care outside the US in almost all cases. Medicare Advantage plans occasionally include emergency coverage with lifetime caps of $25K–50K. Medigap plans F, G, and N include a foreign-travel emergency benefit: 80% after deductible, $50,000 lifetime maximum.</p>
        <p class="gov-exception">Exceptions: care in Canada or Mexico en route to Alaska, and the rare case of a foreign hospital being the closest facility to a US emergency.</p>
      </div>
      <div class="gov-callout">
        <h3>🏥 Medicaid <em>doesn't either</em>.</h3>
        <p>Medicaid covers care within the US only, with extremely narrow exceptions for emergencies near the US border. Every major Medicaid carrier — Centene, Molina, and the state Medicaid plans — treats international care as effectively out of pocket.</p>
        <p class="gov-exception">If you have Medicaid and are traveling internationally, a supplemental travel medical policy is essential. Budget $30–80 per week of travel.</p>
      </div>
    </div>
  </section>

  <!-- Module 5 — Non-US visitors -->
  <section class="module-section" id="visiting-us">
    <span class="section-eyebrow">Visiting the US?</span>
    <h2>Your home plan <em>probably doesn't cover US costs</em>.</h2>
    <div class="visitors-callout">
      <h3>The gotcha list.</h3>
      <p><strong>EHIC / GHIC (European).</strong> Not valid in the US. Period.</p>
      <p><strong>Most national health systems.</strong> Cover emergencies abroad with low caps (often €30K–100K). US healthcare costs can exceed these limits with a single ICU stay.</p>
      <p><strong>Private international plans from home.</strong> Some cover the US but often at limited rates. Verify before you fly; don't assume.</p>
      <p>Plan on a dedicated travel medical policy if you're visiting the US. US healthcare is the most expensive in the world — a seven-figure hospital bill is a real outcome for a serious accident.</p>
    </div>
  </section>

  <!-- Directory — 15 carrier cards -->
  <section class="module-section" id="directory">
    <span class="section-eyebrow">All __CARRIER_COUNT__ carriers</span>
    <h2>Pick <em>your carrier</em>.</h2>
    <p class="lede">Click for the full international coverage breakdown — what's covered, what's not, how to check your specific plan, and whether you need supplemental travel insurance.</p>
    <div class="carrier-grid">
__CARRIER_CARDS__
    </div>
  </section>

  <!-- FAQ -->
  <section class="module-section" id="faq">
    <span class="section-eyebrow">Frequently asked</span>
    <h2>Insurance abroad, <em>answered</em>.</h2>
    <p class="lede">Eighteen questions we get most often about US health insurance and international travel.</p>
    <div class="faq-section">
__FAQS__
    </div>
  </section>

  <!-- Methodology -->
  <section class="module-section methodology-block" id="methodology">
    <span class="section-eyebrow">Methodology</span>
    <h2>How we build these <em>carrier guides</em>.</h2>
    <p class="lede">Carrier-level coverage is compiled from official plan documents, NAIC filings, carrier websites, and consumer reports. Always verify against your specific plan's Summary of Benefits and Coverage (SBC).</p>
    <ol>
      <li><strong>Start with the carrier's published plan documents.</strong><p>Summary of Benefits and Coverage filings, carrier websites, and state Department of Insurance rate filings are the primary source. Anything that conflicts gets flagged and researched.</p></li>
      <li><strong>Cross-check with independent consumer sources.</strong><p>NAIC complaint indexes, JD Power member satisfaction data, and consumer-reports reviews provide the real-world experience layer on top of marketing copy.</p></li>
      <li><strong>Classify supplemental tier conservatively.</strong><p>"Essential" means the primary plan is inadequate for international travel on its own. "Strongly Recommended" means the plan covers emergencies but leaves major gaps (routine care, medevac, extended stays). "Recommended" means the plan is competent but supplemental adds value for specific scenarios.</p></li>
      <li><strong>Review monthly; correct on reader reports.</strong><p>Plan details change annually in January; rates change mid-year. Full editorial pass every four weeks. Reader corrections at hello@tabiji.ai usually ship within 48 hours.</p></li>
      <li><strong>Disclose limits and relationships.</strong><p>We're a travel safety research team, not licensed insurance brokers. We don't sell policies. We don't earn commission from any carrier or supplemental provider. If that ever changes, we'll disclose it prominently.</p></li>
    </ol>
  </section>

  <!-- Correction CTA -->
  <div class="report-cta">
    <h3>Spot something <em>out of date?</em></h3>
    <p>Plan details change. Coverage changes. Rates change. Every correction gets read and usually ships within 48 hours.</p>
    <a href="mailto:hello@tabiji.ai?subject=Insurance%20hub%20correction" class="report-cta-btn">Send a correction</a>
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

  var CARRIER_DATA = __CARRIER_DECISION_DATA__;
  var DEST_TIERS = __DEST_TIERS__;

  var state = { carrier: "", dest: "", length: "" };

  /* Pill selection — single-select per group */
  document.querySelectorAll('.decision-pills').forEach(function(group) {
    var key = group.getAttribute('data-group');
    group.querySelectorAll('.decision-pill').forEach(function(pill) {
      pill.addEventListener('click', function() {
        group.querySelectorAll('.decision-pill').forEach(function(p) { p.classList.remove('active'); });
        pill.classList.add('active');
        state[key] = pill.getAttribute('data-value');
        update();
      });
    });
  });

  var select = document.getElementById('decide-carrier');
  select.addEventListener('change', function() { state.carrier = select.value; update(); });

  function update() {
    if (!state.carrier || !state.dest || !state.length) return;
    var result = document.getElementById('decide-result');
    var verdict = document.getElementById('decide-verdict');
    var body = document.getElementById('decide-body');
    var note = document.getElementById('decide-note');
    var link = document.getElementById('decide-link');

    var c = CARRIER_DATA[state.carrier];
    var destNote = (DEST_TIERS[state.dest] || {}).note || '';
    var lengthNote = {
      'weekend': 'For a weekend, basic travel medical is cheap insurance.',
      'week': '1–2 weeks is the sweet spot for standard travel medical policies.',
      'month': 'At 3–4 weeks, look for higher coverage limits and check pre-existing condition waiver windows.',
      'extended': 'Extended stays need a true expat policy (Cigna Global, GeoBlue, IMG Global, Aetna International) rather than short-trip travel medical.'
    }[state.length];

    if (!c) {
      // medicare / medicaid / other path
      if (state.carrier === 'medicare') {
        verdict.innerHTML = 'Medicare + supplemental = <em>essential</em>.';
        body.textContent = 'Medicare does not travel. You need a supplemental travel medical policy. Medigap F, G, or N adds $50K lifetime foreign-emergency coverage, but medevac is typically not included and a dedicated travel policy is still recommended.';
      } else if (state.carrier === 'medicaid') {
        verdict.innerHTML = 'Medicaid + supplemental = <em>essential</em>.';
        body.textContent = 'Medicaid does not cover international care. A supplemental travel medical policy is mandatory for anything beyond the US border.';
      } else {
        verdict.innerHTML = 'Carrier not listed — treat as <em>essential supplemental</em>.';
        body.textContent = 'Assume emergency-only abroad at best. Buy supplemental travel medical with evacuation coverage and verify your primary plan\'s international benefits in writing before you go.';
      }
      link.setAttribute('href', '#directory');
      link.textContent = 'See all carrier guides →';
    } else {
      verdict.innerHTML = 'Supplemental: <em>' + c.tier + '</em>.';
      body.textContent = c.note;
      link.setAttribute('href', '/health/insurance/' + state.carrier + '/');
      link.textContent = 'Read the full ' + (select.options[select.selectedIndex].text) + ' guide →';
    }
    note.textContent = destNote + (destNote ? ' ' : '') + (lengthNote || '');
    result.hidden = false;
  }

  /* FAQ accordion */
  document.querySelectorAll('.faq-q').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var item = btn.parentElement;
      var open = item.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
})();
</script>

</body>
</html>
"""


if __name__ == "__main__":
    build_hub()
    enrich_health_api()
