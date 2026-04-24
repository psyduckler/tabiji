#!/usr/bin/env python3
"""
build-insurance-carriers.py — Generate the 15 /health/insurance/{slug}/index.html
carrier pages in editorial-v2.

Pulls catalog data (name, icon, tier, mechanism, phone, plan types) from
scripts.lib.editorial.CARRIERS and per-carrier editorial content (overview,
covered/not-covered, scenarios, FAQs, sources) from scripts.lib.carrier_content.

Each carrier page includes:
- Editorial hero with serif headline
- Reviewer strip + affiliate disclosure
- Quick-facts banner (carrier / coverage / phone / supplemental)
- 10 content sections (overview, PPO-HMO, covered, not covered, what you need
  to know, check your plan, claim walkthrough, real-world scenario, supplemental
  verdict, destinations, FAQ, sources, methodology)
- Sticky TOC sidebar (desktop) + mobile dropdown
- FAQ accordion with per-carrier Q/As
- Article + BreadcrumbList + FAQPage schema

Usage:
    python3 scripts/build-insurance-carriers.py            # all 15
    python3 scripts/build-insurance-carriers.py kaiser-permanente cigna  # specific
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
    CARRIERS,
    REVIEW_DATE,
    apply_replacements,
    render_faq_accordion,
    render_faqs_schema,
    tier_slug,
)
from lib.carrier_content import CARRIER_CONTENT, SHARED_CLAIM_STEPS  # noqa: E402

ROOT = SCRIPT_DIR.parent
INSURANCE_DIR = ROOT / "health" / "insurance"


def render_tone_callout(tone: str, title: str, body: str) -> str:
    return (
        f'<div class="need-callout need-callout-{tone}">'
        f'<strong class="need-callout-title">{html.escape(title)}</strong>'
        f'<p>{html.escape(body)}</p></div>'
    )


def render_list(items) -> str:
    return "\n".join(f'          <li>{html.escape(x)}</li>' for x in items)


def render_ordered_questions(questions) -> str:
    return "\n".join(f'          <li>{html.escape(q)}</li>' for q in questions)


def render_claim_steps(steps) -> str:
    out = []
    for s in steps:
        out.append(
            f'        <li>\n'
            f'          <strong>{html.escape(s["title"])}</strong>\n'
            f'          <p>{html.escape(s["body"])}</p>\n'
            f'        </li>'
        )
    return "\n".join(out)


_VANITY = {"BLUE": "2583"}


def tel_href(phone: str):
    """Extract a tel: URI from an assistance-phone string, or None if the
    string is a descriptive placeholder like 'Member services on your card'.
    Vanity-number words (e.g. BLUE → 2583) are resolved first."""
    if not phone:
        return None
    resolved = phone
    for word, digits in _VANITY.items():
        resolved = re.sub(word, digits, resolved, flags=re.IGNORECASE)
    digits = re.sub(r'[^\d]', '', resolved.split("(")[0])
    if len(digits) < 10:
        return None
    return f"tel:+{digits}" if digits.startswith("1") else f"tel:+1{digits}"


def render_sources(sources) -> str:
    out = []
    for s in sources:
        name = html.escape(s["name"])
        url = s.get("url")
        if url:
            out.append(f'          <li><a href="{url}" target="_blank" rel="noopener">{name}</a></li>')
        else:
            out.append(f'          <li>{name}</li>')
    return "\n".join(out)


def render_carrier_page(carrier: dict, content: dict) -> str:
    slug = carrier["slug"]
    name = carrier["name"]
    icon = carrier["icon"]
    tier = carrier["supp_tier"]
    tslug = tier_slug(tier)
    today = date.today().isoformat()

    product_id = f"https://tabiji.ai/health/insurance/{slug}/#product"
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "FinancialProduct",
                "@id": product_id,
                "name": f"{name} — international travel coverage",
                "category": "HealthInsurance",
                "description": content.get("short") or carrier["coverage_headline"],
                "provider": {
                    "@type": "Organization",
                    "name": name,
                },
                "serviceType": "Health insurance — international travel coverage",
                "feesAndCommissionsSpecification": content["supplemental_verdict"],
                "audience": {
                    "@type": "PeopleAudience",
                    "audienceType": "US residents traveling internationally",
                },
            },
            {
                "@type": "Article",
                "headline": f"{name} — International Travel Coverage Guide",
                "description": (
                    f"Does {name} cover you abroad? Carrier-specific international travel health insurance "
                    "guide — what's covered, what's not, PPO vs HMO differences, filing claims, a real-world "
                    "cost scenario, and whether you need supplemental travel insurance."
                ),
                "url": f"https://tabiji.ai/health/insurance/{slug}/",
                "inLanguage": "en",
                "datePublished": "2026-03-01",
                "dateModified": today,
                "lastReviewed": today,
                "about": {"@id": product_id},
                "author": {"@type": "Organization", "name": "tabiji editorial team", "url": "https://tabiji.ai/about/"},
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
                    {"@type": "ListItem", "position": 3, "name": "Insurance by Carrier", "item": "https://tabiji.ai/health/insurance/"},
                    {"@type": "ListItem", "position": 4, "name": name, "item": f"https://tabiji.ai/health/insurance/{slug}/"},
                ],
            },
            {"@type": "FAQPage", "mainEntity": render_faqs_schema(content["faqs"])},
        ],
    }
    schema_str = json.dumps(schema, ensure_ascii=False, indent=2)

    need_to_know_html = "\n    ".join(
        render_tone_callout(c["tone"], c["title"], c["body"]) for c in content["need_to_know"]
    )

    phone = carrier["assistance_phone"]
    tel_uri = tel_href(phone)
    if tel_uri:
        fab_html = (
            f'<a class="call-carrier-fab" href="{tel_uri}" aria-label="Call {html.escape(name)}">'
            f'📞 Call your carrier</a>'
        )
    else:
        fab_html = ""

    replacements = {
        "__SLUG__": slug,
        "__NAME__": html.escape(name),
        "__ICON__": icon,
        "__TIER__": html.escape(tier),
        "__TIER_SLUG__": tslug,
        "__MECHANISM__": html.escape(carrier["coverage_headline"]),
        "__PHONE__": html.escape(phone),
        "__CALL_FAB__": fab_html,
        "__PLAN_TYPES__": html.escape(carrier["plan_types"]),
        "__OVERVIEW__": html.escape(content["overview"]),
        "__PPO_HMO_NOTE__": html.escape(content["ppo_hmo_note"]),
        "__COVERED_LIST__": render_list(content["covered"]),
        "__NOT_COVERED_LIST__": render_list(content["not_covered"]),
        "__NEED_TO_KNOW__": need_to_know_html,
        "__ASK_QUESTIONS__": render_ordered_questions(content["ask_questions"]),
        "__CLAIM_STEPS__": render_claim_steps(SHARED_CLAIM_STEPS),
        "__SCENARIO_DESTINATION__": html.escape(content["scenario"]["destination"]),
        "__SCENARIO_TOTAL__": html.escape(content["scenario"]["total"]),
        "__SCENARIO_REIMBURSED__": html.escape(content["scenario"]["reimbursed"]),
        "__SCENARIO_YOUR_COST__": html.escape(content["scenario"]["your_cost"]),
        "__SCENARIO_BODY__": html.escape(content["scenario"]["body"]),
        "__SUPPLEMENTAL_VERDICT__": html.escape(content["supplemental_verdict"]),
        "__FAQS__": render_faq_accordion(content["faqs"], id_prefix=f"{slug}-faq"),
        "__SOURCES__": render_sources(content["sources"]),
        "__SCHEMA__": schema_str,
        "__REVIEW_DATE__": REVIEW_DATE,
        "__TODAY__": today,
    }
    return apply_replacements(CARRIER_TEMPLATE, replacements)


def build(slugs=None):
    if slugs:
        targets = [c for c in CARRIERS if c["slug"] in slugs]
        missing = set(slugs) - {c["slug"] for c in targets}
        if missing:
            print(f"Unknown carrier slug(s): {', '.join(sorted(missing))}", file=sys.stderr)
            sys.exit(1)
    else:
        targets = CARRIERS

    for carrier in targets:
        slug = carrier["slug"]
        content = CARRIER_CONTENT[slug]
        html_out = render_carrier_page(carrier, content)
        out_path = INSURANCE_DIR / slug / "index.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html_out)
        print(f"Wrote {out_path.relative_to(ROOT)} ({len(html_out):,} chars)")


# -------------------------------------------------------------------
# HTML template
# -------------------------------------------------------------------

CARRIER_TEMPLATE = r"""<!DOCTYPE html>
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
    <title>__NAME__ International Travel Coverage — Does Your Plan Cover You Abroad? | tabiji.ai</title>
    <meta name="description" content="Does __NAME__ cover you abroad? Carrier-specific international travel health insurance guide — what's covered, what's not, PPO vs HMO, filing claims, a real cost scenario, and whether you need supplemental travel insurance.">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="https://tabiji.ai/health/insurance/__SLUG__/">
    <meta property="og:title" content="__NAME__ Abroad — Coverage, Claims, and Cost Scenarios | tabiji.ai">
    <meta property="og:description" content="Carrier-specific international travel insurance guide for __NAME__ members.">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://tabiji.ai/health/insurance/__SLUG__/">
    <meta property="og:image" content="https://img.tabiji.ai/tabiji-owl-logo.png">
    <meta property="og:site_name" content="tabiji.ai">

    <script type="application/ld+json">__SCHEMA__</script>

    <link rel="stylesheet" href="/assets/scams.css">
    <style>
    /* Carrier-page-specific additions on top of editorial-v2 (scams.css) */

    body.editorial-v2 .breadcrumb a:hover { color: var(--terracotta); }

    body.editorial-v2 .reviewer-strip,
    body.editorial-v2 .affiliate-disclosure {
        max-width: 860px;
        margin: 0 auto;
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
    body.editorial-v2 .reviewer-strip { border-left: 4px solid var(--sage); margin-top: 1rem; }
    body.editorial-v2 .reviewer-strip strong { font-style: normal; color: var(--indigo); }
    body.editorial-v2 .reviewer-strip a { color: var(--terracotta); text-decoration: none; font-style: normal; font-weight: 600; border-bottom: 1px solid transparent; }
    body.editorial-v2 .reviewer-strip a:hover { border-bottom-color: var(--terracotta); }
    body.editorial-v2 .affiliate-disclosure {
        margin-top: 0.75rem;
        background: var(--warm-cream-soft);
        border: 1px dashed var(--sand);
        font-size: 0.9rem;
        color: var(--earth);
    }
    body.editorial-v2 .affiliate-disclosure strong { font-style: normal; color: var(--indigo); }

    body.editorial-v2 .quick-facts {
        max-width: 1100px;
        margin: 2rem auto 0;
        padding: 0 1.5rem;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
    }
    body.editorial-v2 .qf-tile {
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        padding: 1rem 1.2rem;
    }
    body.editorial-v2 .qf-label {
        font-family: var(--font-sans);
        font-size: 0.7rem;
        font-weight: 700;
        color: var(--earth);
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }
    body.editorial-v2 .qf-value {
        font-family: var(--font-serif);
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--indigo);
        line-height: 1.3;
    }
    body.editorial-v2 .qf-value-small {
        font-family: var(--font-sans);
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--indigo);
    }

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
        padding: 0.35rem 0.75rem;
        color: var(--text-muted);
        font-family: var(--font-serif);
        font-size: 0.92rem;
        text-decoration: none;
        transition: color 0.2s, border-color 0.2s;
    }
    body.editorial-v2 aside.toc a:hover,
    body.editorial-v2 aside.toc a.active {
        color: var(--terracotta);
    }
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
        padding: 0.75rem 1rem;
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
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 40px; height: 2px;
        background: var(--terracotta);
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
    body.editorial-v2 article.main-col h2 em {
        font-style: italic;
        color: var(--terracotta);
    }
    body.editorial-v2 article.main-col p {
        font-family: var(--font-serif);
        font-size: 1rem;
        color: var(--text);
        line-height: 1.65;
        margin-bottom: 0.9rem;
    }

    body.editorial-v2 .covered-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.25rem;
        margin-top: 0.5rem;
    }
    body.editorial-v2 .covered-block {
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        padding: 1.1rem 1.3rem;
    }
    body.editorial-v2 .covered-block.yes { border-left: 4px solid var(--low); }
    body.editorial-v2 .covered-block.no { border-left: 4px solid var(--ed-high-text); }
    body.editorial-v2 .covered-block h3 {
        font-family: var(--font-sans);
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }
    body.editorial-v2 .covered-block.yes h3 { color: var(--low); }
    body.editorial-v2 .covered-block.no h3 { color: var(--ed-high-text); }
    body.editorial-v2 .covered-block ul {
        list-style: none;
        padding: 0;
        margin: 0;
        font-family: var(--font-serif);
        font-size: 0.95rem;
        color: var(--text-muted);
        line-height: 1.55;
    }
    body.editorial-v2 .covered-block li { padding-left: 1.25rem; position: relative; margin-bottom: 0.35rem; }
    body.editorial-v2 .covered-block.yes li::before { content: "✓"; position: absolute; left: 0; color: var(--low); font-weight: 700; }
    body.editorial-v2 .covered-block.no li::before { content: "✕"; position: absolute; left: 0; color: var(--ed-high-text); font-weight: 700; }

    body.editorial-v2 .need-callout {
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        padding: 1rem 1.25rem;
        margin-bottom: 0.85rem;
    }
    body.editorial-v2 .need-callout-danger { border-left: 4px solid var(--ed-high-text); }
    body.editorial-v2 .need-callout-caution { border-left: 4px solid var(--ed-med-text); }
    body.editorial-v2 .need-callout-info { border-left: 4px solid var(--info); }
    body.editorial-v2 .need-callout-title {
        font-family: var(--font-serif);
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--indigo);
        display: block;
        margin-bottom: 0.25rem;
    }
    body.editorial-v2 .need-callout p {
        font-family: var(--font-serif);
        font-size: 0.95rem;
        color: var(--text-muted);
        line-height: 1.55;
        margin: 0;
    }

    body.editorial-v2 .ask-list {
        counter-reset: ask;
        list-style: none;
        padding: 0;
        margin-top: 0.5rem;
    }
    body.editorial-v2 .ask-list li {
        counter-increment: ask;
        position: relative;
        padding: 0.75rem 1rem 0.75rem 3rem;
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        margin-bottom: 0.5rem;
        font-family: var(--font-serif);
        font-size: 0.95rem;
        color: var(--text);
        line-height: 1.5;
    }
    body.editorial-v2 .ask-list li::before {
        content: counter(ask, decimal-leading-zero);
        position: absolute;
        left: 0.9rem;
        top: 0.75rem;
        font-family: var(--font-serif);
        font-weight: 600;
        color: var(--terracotta);
        font-size: 1rem;
    }

    body.editorial-v2 .claim-steps {
        counter-reset: step;
        list-style: none;
        padding: 0;
        margin-top: 0.5rem;
    }
    body.editorial-v2 .claim-steps li {
        counter-increment: step;
        position: relative;
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
        padding: 1rem 1.25rem 1rem 3.5rem;
        margin-bottom: 0.6rem;
    }
    body.editorial-v2 .claim-steps li::before {
        content: "0" counter(step);
        position: absolute;
        left: 1.1rem;
        top: 1rem;
        font-family: var(--font-serif);
        font-weight: 600;
        color: var(--terracotta);
        font-size: 1rem;
    }
    body.editorial-v2 .claim-steps strong {
        font-family: var(--font-serif);
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--indigo);
        display: block;
        margin-bottom: 0.25rem;
    }
    body.editorial-v2 .claim-steps p {
        font-family: var(--font-serif);
        font-size: 0.95rem;
        color: var(--text-muted);
        line-height: 1.55;
        margin: 0;
    }

    body.editorial-v2 .scenario-card {
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-left: 4px solid var(--terracotta);
        border-radius: var(--radius-md);
        padding: 1.4rem 1.6rem;
        margin-top: 0.5rem;
    }
    body.editorial-v2 .scenario-header {
        font-family: var(--font-serif);
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--indigo);
        margin-bottom: 0.85rem;
    }
    body.editorial-v2 .scenario-numbers {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 0.9rem;
    }
    body.editorial-v2 .scenario-num {
        text-align: center;
        padding: 0.65rem;
        background: var(--white);
        border: 1px solid var(--sand);
        border-radius: var(--radius-md);
    }
    body.editorial-v2 .scenario-num .scen-label {
        font-family: var(--font-sans);
        font-size: 0.62rem;
        font-weight: 700;
        color: var(--earth);
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 0.2rem;
        display: block;
    }
    body.editorial-v2 .scenario-num .scen-amount {
        font-family: var(--font-serif);
        font-size: 1.4rem;
        font-weight: 600;
        color: var(--indigo);
    }
    body.editorial-v2 .scenario-num.your-cost .scen-amount { color: var(--ed-high-text); }
    body.editorial-v2 .scenario-card p {
        font-family: var(--font-serif);
        font-size: 0.95rem;
        color: var(--text-muted);
        line-height: 1.55;
        margin: 0;
    }

    body.editorial-v2 .supp-verdict-card {
        background: var(--warm-cream);
        border: 1px solid var(--sand);
        border-left: 4px solid var(--terracotta);
        border-radius: var(--radius-md);
        padding: 1.4rem 1.6rem;
        margin-top: 0.5rem;
    }
    body.editorial-v2 .supp-verdict-card .verdict-label {
        font-family: var(--font-sans);
        font-size: 0.7rem;
        font-weight: 700;
        color: var(--terracotta);
        letter-spacing: 0.22em;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
        display: block;
    }
    body.editorial-v2 .supp-verdict-card .verdict-tier {
        font-family: var(--font-serif);
        font-size: 1.4rem;
        font-weight: 600;
        color: var(--indigo);
        margin-bottom: 0.5rem;
    }
    body.editorial-v2 .supp-verdict-card p {
        font-family: var(--font-serif);
        font-size: 1rem;
        color: var(--text);
        line-height: 1.6;
        margin: 0;
    }

    body.editorial-v2 .destinations-cta {
        background: var(--warm-cream-soft);
        border: 1px dashed var(--sand);
        border-radius: var(--radius-md);
        padding: 1.25rem 1.5rem;
        margin-top: 0.5rem;
        text-align: center;
    }
    body.editorial-v2 .destinations-cta a {
        font-family: var(--font-sans);
        font-size: 0.95rem;
        font-weight: 600;
        color: var(--terracotta);
        text-decoration: none;
        border-bottom: 1px solid transparent;
    }
    body.editorial-v2 .destinations-cta a:hover { border-bottom-color: var(--terracotta); }

    body.editorial-v2 .sources-list {
        list-style: none;
        padding: 0;
        margin-top: 0.5rem;
    }
    body.editorial-v2 .sources-list li {
        padding: 0.55rem 0;
        border-bottom: 1px solid var(--sand);
        font-family: var(--font-serif);
        font-size: 0.95rem;
        color: var(--text-muted);
    }
    body.editorial-v2 .sources-list li:last-child { border-bottom: none; }
    body.editorial-v2 .sources-list a {
        color: var(--terracotta);
        text-decoration: none;
        border-bottom: 1px solid transparent;
    }
    body.editorial-v2 .sources-list a:hover { border-bottom-color: var(--terracotta); }

    /* Sticky call-your-carrier CTA (mobile-friendly floating) */
    .call-carrier-fab {
        position: fixed;
        right: 1.25rem;
        bottom: 1.25rem;
        z-index: 100;
        background: var(--terracotta);
        color: white;
        border-radius: var(--radius-pill);
        padding: 0.85rem 1.35rem;
        font-family: var(--font-sans);
        font-weight: 600;
        font-size: 0.9rem;
        text-decoration: none;
        box-shadow: 0 6px 20px rgba(196, 112, 75, 0.35);
        transition: background 0.2s, transform 0.15s;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    .call-carrier-fab:hover { background: var(--terracotta-deep); transform: translateY(-1px); }

    @media (max-width: 900px) {
        body.editorial-v2 .layout { grid-template-columns: 1fr; gap: 1.5rem; }
        body.editorial-v2 aside.toc { display: none; }
        body.editorial-v2 .toc-mobile { display: block; }
        body.editorial-v2 .covered-grid { grid-template-columns: 1fr; }
        body.editorial-v2 .scenario-numbers { grid-template-columns: 1fr; }
    }

    @media print {
        nav, footer, .call-carrier-fab, .toc-mobile, aside.toc { display: none !important; }
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
    <a href="/">Home</a><span>›</span><a href="/health/">Travel Health</a><span>›</span><a href="/health/insurance/">Insurance</a><span>›</span>__NAME__
</div>

<main>

  <div class="hero">
    <div class="hero-badge">__ICON__ __NAME__</div>
    <h1>Does <em>__NAME__</em> cover you abroad?</h1>
    <p>International travel coverage, claim process, real-world cost scenario, and whether you need supplemental insurance.</p>
    <div class="hero-meta">
      <span>🕐 Last reviewed __REVIEW_DATE__</span>
    </div>
  </div>

  <div class="reviewer-strip">
    <strong>Researched by the tabiji editorial team.</strong> Cross-referenced against __NAME__'s published plan documents, Summary of Benefits and Coverage filings, NAIC filings, and independent consumer reports. Last full review: __REVIEW_DATE__. This is general carrier-level information and not insurance advice — always verify with your specific plan before traveling. This page is not affiliated with or endorsed by __NAME__.
  </div>

  <div class="affiliate-disclosure">
    <strong>No affiliate commissions.</strong> We don't earn anything from __NAME__ or any supplemental travel insurance provider named on this page. Rankings reflect our editorial view of coverage quality only.
  </div>

  <div class="quick-facts">
    <div class="qf-tile">
      <div class="qf-label">Carrier</div>
      <div class="qf-value">__NAME__</div>
    </div>
    <div class="qf-tile">
      <div class="qf-label">Coverage mechanism</div>
      <div class="qf-value qf-value-small">__MECHANISM__</div>
    </div>
    <div class="qf-tile">
      <div class="qf-label">Assistance phone</div>
      <div class="qf-value qf-value-small">__PHONE__</div>
    </div>
    <div class="qf-tile">
      <div class="qf-label">Supplemental</div>
      <div class="qf-value">__TIER__</div>
    </div>
  </div>

  <div class="toc-mobile">
    <details>
      <summary>Jump to section</summary>
      <ul>
        <li><a href="#overview">Overview</a></li>
        <li><a href="#ppo-hmo">PPO vs HMO vs HDHP</a></li>
        <li><a href="#coverage">What's covered / not covered</a></li>
        <li><a href="#need-to-know">What you need to know</a></li>
        <li><a href="#check-plan">Check your plan</a></li>
        <li><a href="#filing-claim">Filing a claim abroad</a></li>
        <li><a href="#scenario">Real-world cost scenario</a></li>
        <li><a href="#supplemental">Supplemental verdict</a></li>
        <li><a href="#destinations">Destination guides</a></li>
        <li><a href="#faq">FAQ</a></li>
        <li><a href="#sources">Sources</a></li>
      </ul>
    </details>
  </div>

  <div class="layout">

    <aside class="toc">
      <h2>On this page</h2>
      <ul>
        <li><a href="#overview">Overview</a></li>
        <li><a href="#ppo-hmo">PPO vs HMO vs HDHP</a></li>
        <li><a href="#coverage">What's covered / not</a></li>
        <li><a href="#need-to-know">What you need to know</a></li>
        <li><a href="#check-plan">Check your plan</a></li>
        <li><a href="#filing-claim">Filing a claim</a></li>
        <li><a href="#scenario">Cost scenario</a></li>
        <li><a href="#supplemental">Supplemental verdict</a></li>
        <li><a href="#destinations">Destination guides</a></li>
        <li><a href="#faq">FAQ</a></li>
        <li><a href="#sources">Sources</a></li>
      </ul>
    </aside>

    <article class="main-col">

      <section id="overview">
        <span class="section-eyebrow">Overview</span>
        <h2>International coverage at a <em>glance</em>.</h2>
        <p>__OVERVIEW__</p>
      </section>

      <section id="ppo-hmo">
        <span class="section-eyebrow">Plan types</span>
        <h2>PPO vs HMO vs <em>HDHP</em>.</h2>
        <p>__PPO_HMO_NOTE__</p>
      </section>

      <section id="coverage">
        <span class="section-eyebrow">Coverage</span>
        <h2>What's covered, what <em>isn't</em>.</h2>
        <div class="covered-grid">
          <div class="covered-block yes">
            <h3>Typically covered</h3>
            <ul>
__COVERED_LIST__
            </ul>
          </div>
          <div class="covered-block no">
            <h3>Not covered</h3>
            <ul>
__NOT_COVERED_LIST__
            </ul>
          </div>
        </div>
      </section>

      <section id="need-to-know">
        <span class="section-eyebrow">What you need to know</span>
        <h2>The three things that <em>actually matter</em>.</h2>
    __NEED_TO_KNOW__
      </section>

      <section id="check-plan">
        <span class="section-eyebrow">Check your plan</span>
        <h2>Six questions to <em>ask your carrier</em>.</h2>
        <p>Call <strong>__PHONE__</strong> and ask these directly. Get the answers in writing — verbal confirmation doesn't hold up at claim time.</p>
        <ol class="ask-list">
__ASK_QUESTIONS__
        </ol>
      </section>

      <section id="filing-claim">
        <span class="section-eyebrow">Filing a claim abroad</span>
        <h2>The <em>five steps</em> that actually work.</h2>
        <p>Most international claims fail because of missing documentation or delayed filing. Do these five things and you'll maximize what you get back.</p>
        <ol class="claim-steps">
__CLAIM_STEPS__
        </ol>
      </section>

      <section id="scenario">
        <span class="section-eyebrow">Real-world scenario</span>
        <h2>What a <em>typical claim</em> looks like.</h2>
        <div class="scenario-card">
          <div class="scenario-header">__SCENARIO_DESTINATION__</div>
          <div class="scenario-numbers">
            <div class="scenario-num">
              <span class="scen-label">Total bill</span>
              <div class="scen-amount">__SCENARIO_TOTAL__</div>
            </div>
            <div class="scenario-num">
              <span class="scen-label">Reimbursed</span>
              <div class="scen-amount">__SCENARIO_REIMBURSED__</div>
            </div>
            <div class="scenario-num your-cost">
              <span class="scen-label">Your cost</span>
              <div class="scen-amount">__SCENARIO_YOUR_COST__</div>
            </div>
          </div>
          <p>__SCENARIO_BODY__</p>
        </div>
      </section>

      <section id="supplemental">
        <span class="section-eyebrow">Supplemental insurance</span>
        <h2>Do you <em>need</em> supplemental?</h2>
        <div class="supp-verdict-card">
          <span class="verdict-label">Our recommendation for __NAME__ members</span>
          <div class="verdict-tier">__TIER__</div>
          <p>__SUPPLEMENTAL_VERDICT__</p>
        </div>
        <p style="margin-top:1rem;">Popular supplemental providers: <strong>World Nomads</strong>, <strong>GeoBlue</strong> (BCBS affiliated), <strong>IMG Global</strong>, <strong>Allianz Travel</strong>, <strong>Travel Guard</strong>. Expect $30–80 for a weeklong trip, $60–200 for a month, with higher rates for adventure activities or pre-existing condition waivers.</p>
      </section>

      <section id="destinations">
        <span class="section-eyebrow">Destination guides</span>
        <h2>Where you're <em>going</em>.</h2>
        <p>Every country has its own healthcare reality. Our country-specific guides cover emergency numbers, pharmacy access, medication restrictions, vaccinations, and water safety.</p>
        <div class="destinations-cta">
          <a href="/health/">→ Browse all 210 country health guides</a>
        </div>
      </section>

      <section id="faq">
        <span class="section-eyebrow">Frequently asked</span>
        <h2>__NAME__ <em>abroad</em>, answered.</h2>
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
        <p style="margin-top:1rem;font-size:0.9rem;color:var(--earth);font-style:italic;">⚠️ This guide provides general carrier-level information and does not constitute insurance or medical advice. Coverage varies by plan, employer, state, and year. Always verify your specific coverage with your insurance carrier before traveling. This page is not affiliated with or endorsed by __NAME__.</p>
      </section>

    </article>

  </div>

  <div class="report-cta">
    <h3>Spot something <em>out of date?</em></h3>
    <p>Plan details change. Rates change. Every correction gets read and usually ships within 48 hours.</p>
    <a href="mailto:hello@tabiji.ai?subject=__NAME__%20carrier%20guide%20correction" class="report-cta-btn">Send a correction</a>
  </div>

</main>

__CALL_FAB__

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

  /* FAQ accordion */
  document.querySelectorAll('.faq-q').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var item = btn.parentElement;
      var open = item.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  /* TOC active-section highlighting */
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


if __name__ == "__main__":
    slugs = sys.argv[1:] if len(sys.argv) > 1 else None
    build(slugs)
