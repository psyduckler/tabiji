"""
Shared editorial constants and render helpers for the health / insurance /
carrier hub generators (scripts/build-health-hub.py, build-insurance-hub.py,
and the forthcoming carrier-page builder).

Single source of truth for:
  - The 15 US health-insurance carriers (CARRIERS)
  - Supplemental-tier constants and slug mapping (TIERS, tier_slug)
  - The current editorial review month (REVIEW_DATE)
  - FAQ HTML accordion + FAQPage schema rendering
  - Placeholder-based template substitution (apply_replacements)
"""

from __future__ import annotations

import html as html_mod
import json
from typing import Iterable


# -------------------------------------------------------------------
# Editorial cadence
# -------------------------------------------------------------------

REVIEW_DATE = "April 2026"


# -------------------------------------------------------------------
# Supplemental-insurance tier vocabulary
# -------------------------------------------------------------------

class TIERS:
    ESSENTIAL = "Essential"
    STRONGLY_RECOMMENDED = "Strongly Recommended"
    RECOMMENDED = "Recommended"


def tier_slug(tier: str) -> str:
    """Normalize a tier label to its CSS-class slug (`Strongly Recommended` →
    `strongly-recommended`)."""
    return tier.lower().replace(" ", "-")


# -------------------------------------------------------------------
# Canonical carrier catalog
# -------------------------------------------------------------------
# The 15 US health-insurance carriers covered across /health/insurance/.
# Extended fields (supplemental tier, mechanism, plan types, etc.) are used by
# build-insurance-hub.py; build-health-hub.py exposes the subset in its
# /api/v1/health.json. Adding a carrier = edit this list, nothing else.

CARRIERS = [
    {
        "slug": "blue-cross-blue-shield", "name": "Blue Cross Blue Shield", "icon": "🛡️",
        "supp_tier": TIERS.STRONGLY_RECOMMENDED,
        "badge_tone": "info",
        "coverage_headline": "Global Core network in 190+ countries",
        "mechanism": "Global Core",
        "assistance_phone": "1-800-810-BLUE (2583)",
        "plan_types": "PPO best · HMO emergency-only",
        "short": "34 independent licensees; coverage varies by state. PPO plans carry international emergency + some urgent care.",
    },
    {
        "slug": "unitedhealthcare", "name": "UnitedHealthcare", "icon": "🏥",
        "supp_tier": TIERS.RECOMMENDED,
        "badge_tone": "info",
        "coverage_headline": "UHC Global supports reimbursement in most countries",
        "mechanism": "UHC Global",
        "assistance_phone": "Member services on your card",
        "plan_types": "PPO best · HMO emergency-only",
        "short": "Emergency care covered worldwide at out-of-network rates. Direct billing at select international hospitals.",
    },
    {
        "slug": "aetna", "name": "Aetna", "icon": "💼",
        "supp_tier": TIERS.RECOMMENDED,
        "badge_tone": "info",
        "coverage_headline": "International plans (Aetna International) for long stays",
        "mechanism": "Aetna International",
        "assistance_phone": "Member services on your card",
        "plan_types": "PPO best · separate expat plans available",
        "short": "Domestic plans cover emergencies only. Aetna International is a separate product for expats and frequent travelers.",
    },
    {
        "slug": "cigna", "name": "Cigna", "icon": "🌐",
        "supp_tier": TIERS.RECOMMENDED,
        "badge_tone": "safe",
        "coverage_headline": "Strong international network; Cigna Global available separately",
        "mechanism": "Cigna Global",
        "assistance_phone": "Member services on your card",
        "plan_types": "PPO solid · Cigna Global for expats",
        "short": "One of the better US carriers for international coverage. Cigna Global is a dedicated expat product with broad worldwide access.",
    },
    {
        "slug": "humana", "name": "Humana", "icon": "❤️",
        "supp_tier": TIERS.ESSENTIAL,
        "badge_tone": "caution",
        "coverage_headline": "Emergency-only, mostly Medicare Advantage",
        "mechanism": "Limited — Medicare Advantage rules",
        "assistance_phone": "Member services on your card",
        "plan_types": "Medicare Advantage · commercial",
        "short": "Largely a Medicare Advantage carrier. International emergency coverage exists but with strict lifetime caps and no routine care.",
    },
    {
        "slug": "kaiser-permanente", "name": "Kaiser Permanente", "icon": "🏛️",
        "supp_tier": TIERS.ESSENTIAL,
        "badge_tone": "danger",
        "coverage_headline": "Emergency reimbursement only — no in-network abroad",
        "mechanism": "Pay upfront, claim back",
        "assistance_phone": "Member services on your card",
        "plan_types": "HMO only — worst international profile",
        "short": "The worst major US carrier for international travel. Emergency reimbursement only, no network abroad, upfront payment required everywhere.",
    },
    {
        "slug": "anthem", "name": "Anthem", "icon": "🔵",
        "supp_tier": TIERS.RECOMMENDED,
        "badge_tone": "info",
        "coverage_headline": "BlueCard / Global Core in 190+ countries",
        "mechanism": "BCBS Global Core",
        "assistance_phone": "1-800-810-BLUE (2583)",
        "plan_types": "PPO best · HMO emergency-only",
        "short": "BCBS licensee for 14 states. Global Core access; standard Blue emergency-only-abroad rules.",
    },
    {
        "slug": "centene", "name": "Centene", "icon": "🏢",
        "supp_tier": TIERS.ESSENTIAL,
        "badge_tone": "caution",
        "coverage_headline": "Varies dramatically by subsidiary (Ambetter, WellCare, etc.)",
        "mechanism": "Subsidiary-dependent",
        "assistance_phone": "Subsidiary member services",
        "plan_types": "Medicaid · Marketplace · Medicare Advantage",
        "short": "Largest US Medicaid carrier. International coverage is almost nonexistent across its Medicaid and Marketplace products.",
    },
    {
        "slug": "molina-healthcare", "name": "Molina Healthcare", "icon": "🏥",
        "supp_tier": TIERS.ESSENTIAL,
        "badge_tone": "caution",
        "coverage_headline": "Near-zero international coverage",
        "mechanism": "Medicaid / Marketplace limits",
        "assistance_phone": "Member services on your card",
        "plan_types": "Medicaid-focused",
        "short": "Medicaid-focused carrier with minimal international scope. Supplemental travel insurance is essential for any trip abroad.",
    },
    {
        "slug": "hcsc", "name": "Health Care Service Corporation", "icon": "🔷",
        "supp_tier": TIERS.RECOMMENDED,
        "badge_tone": "info",
        "coverage_headline": "BCBS plans across 5 states (IL/TX/NM/OK/MT)",
        "mechanism": "BCBS Global Core",
        "assistance_phone": "1-800-810-BLUE (2583)",
        "plan_types": "PPO best · HMO emergency-only",
        "short": "BCBS licensee covering Illinois, Texas, New Mexico, Oklahoma, and Montana. Global Core access with standard Blue rules.",
    },
    {
        "slug": "highmark", "name": "Highmark", "icon": "💠",
        "supp_tier": TIERS.RECOMMENDED,
        "badge_tone": "info",
        "coverage_headline": "BCBS plans across PA / WV / DE / NY",
        "mechanism": "BCBS Global Core",
        "assistance_phone": "1-800-810-BLUE (2583)",
        "plan_types": "PPO best · HMO emergency-only",
        "short": "BCBS licensee covering Pennsylvania, West Virginia, Delaware, and parts of New York. Standard Blue international rules.",
    },
    {
        "slug": "independence-blue-cross", "name": "Independence Blue Cross", "icon": "🔹",
        "supp_tier": TIERS.RECOMMENDED,
        "badge_tone": "info",
        "coverage_headline": "Global Core + GeoBlue (a BCBS affiliate)",
        "mechanism": "BCBS Global Core + GeoBlue",
        "assistance_phone": "1-800-810-BLUE (2583)",
        "plan_types": "PPO best · GeoBlue supplements available",
        "short": "Southeastern Pennsylvania's BCBS licensee. Global Core access plus easy GeoBlue supplement for extended stays.",
    },
    {
        "slug": "carefirst", "name": "CareFirst", "icon": "💙",
        "supp_tier": TIERS.RECOMMENDED,
        "badge_tone": "info",
        "coverage_headline": "BCBS plans in MD / DC / VA",
        "mechanism": "BCBS Global Core",
        "assistance_phone": "1-800-810-BLUE (2583)",
        "plan_types": "PPO best · HMO emergency-only",
        "short": "BCBS licensee for Maryland, DC, and northern Virginia. Standard Blue international emergency coverage.",
    },
    {
        "slug": "premera-blue-cross", "name": "Premera Blue Cross", "icon": "🏔️",
        "supp_tier": TIERS.RECOMMENDED,
        "badge_tone": "info",
        "coverage_headline": "BCBS plans in WA / AK",
        "mechanism": "BCBS Global Core",
        "assistance_phone": "1-800-810-BLUE (2583)",
        "plan_types": "PPO best · HMO emergency-only",
        "short": "BCBS licensee for Washington and Alaska. Alaska residents need evacuation coverage given geography.",
    },
    {
        "slug": "regence", "name": "Regence", "icon": "⛰️",
        "supp_tier": TIERS.RECOMMENDED,
        "badge_tone": "info",
        "coverage_headline": "BlueCard / Global Core in WA / OR / ID / UT",
        "mechanism": "BCBS Global Core",
        "assistance_phone": "1-800-810-BLUE (2583)",
        "plan_types": "PPO best · HMO emergency-only",
        "short": "Pacific Northwest BCBS licensee. Emergency coverage abroad via Global Core; supplemental recommended for non-emergency needs.",
    },
]


# -------------------------------------------------------------------
# Render helpers
# -------------------------------------------------------------------

def render_faq_accordion(faqs: Iterable[dict], id_prefix: str = "faq") -> str:
    """Render a FAQ list as accordion items using the editorial-v2 .faq-item /
    .faq-q / .faq-a pattern from assets/scams.css."""
    out = []
    for i, f in enumerate(faqs):
        out.append(
            f'      <div class="faq-item">\n'
            f'        <button class="faq-q" type="button" aria-expanded="false" '
            f'aria-controls="{id_prefix}-a-{i}">'
            f'{html_mod.escape(f["q"])}<span class="faq-arrow">▾</span></button>\n'
            f'        <div class="faq-a" id="{id_prefix}-a-{i}">{html_mod.escape(f["a"])}</div>\n'
            f'      </div>'
        )
    return "\n".join(out)


def render_faqs_schema(faqs: Iterable[dict]) -> list:
    """Return a list of Question entities suitable for schema.org FAQPage's
    mainEntity field."""
    return [
        {
            "@type": "Question",
            "name": f["q"],
            "acceptedAnswer": {"@type": "Answer", "text": f["a"]},
        }
        for f in faqs
    ]


def apply_replacements(template: str, replacements: dict) -> str:
    """Substitute all `__KEY__` placeholders in template. Order-independent;
    each key replaced globally."""
    out = template
    for k, v in replacements.items():
        out = out.replace(k, v)
    return out
