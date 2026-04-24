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
# Tabiji travel-safety Kindle books
# -------------------------------------------------------------------
# Country-slug → book URL. Only countries with published + live Kindle books
# (verified via /books/{slug}-tourist-scams/ returning 200). Adding a country
# to this list causes the matching /health/{slug}/ page to show a book-CTA.
BOOKS_BY_SLUG = {
    "argentina":       "/books/argentina-tourist-scams/",
    "brazil":          "/books/brazil-tourist-scams/",
    "canada":          "/books/canada-tourist-scams/",
    "china":           "/books/china-tourist-scams/",
    "colombia":        "/books/colombia-tourist-scams/",
    "france":          "/books/france-tourist-scams/",
    "germany":         "/books/germany-tourist-scams/",
    "greece":          "/books/greece-tourist-scams/",
    "indonesia":       "/books/indonesia-tourist-scams/",
    "italy":           "/books/italy-tourist-scams/",
    "japan":           "/books/japan-tourist-scams/",
    "portugal":        "/books/portugal-tourist-scams/",
    "spain":           "/books/spain-tourist-scams/",
    "thailand":        "/books/thailand-tourist-scams/",
    "turkey":          "/books/turkey-tourist-scams/",
    "united-kingdom":  "/books/united-kingdom-tourist-scams/",
    "vietnam":         "/books/vietnam-tourist-scams/",
}


def book_url_for(slug: str):
    """Return the canonical book URL for a country slug, or None if no book."""
    return BOOKS_BY_SLUG.get(slug)


def render_country_book_cta(slug: str, name: str) -> str:
    """Render the editorial-v2 book-CTA card for a country page.
    Returns empty string if no book exists for that country."""
    url = book_url_for(slug)
    if not url:
        return ""
    import html as html_mod
    name_esc = html_mod.escape(name)
    return (
        f'  <section class="book-cta-section">\n'
        f'    <div class="book-cta">\n'
        f'      <span class="book-cta-eyebrow">📕 Travel safety book</span>\n'
        f'      <h3 class="book-cta-heading">The full <em>{name_esc}</em> safety guide.</h3>\n'
        f'      <p class="book-cta-body">Every scam pattern, customs trap, and emergency protocol '
        f'we have documented for {name_esc} — packaged into a single Kindle book. '
        f'Searchable offline, sized for your phone.</p>\n'
        f'      <a href="{url}" class="book-cta-btn">Get the {name_esc} safety book →</a>\n'
        f'      <p class="book-cta-format"><em>Kindle · instant download · offline-ready</em></p>\n'
        f'    </div>\n'
        f'  </section>'
    )


def render_medication_book_cta(tier1_name: str, banned_country_slugs: list, restricted_country_slugs: list) -> str:
    """Render a destination-aware book-CTA for a tier-1 medication page.
    Picks up to 3 countries from the banned/restricted lists that have books,
    prioritizing banned countries first."""
    import html as html_mod
    candidates = []
    for s in banned_country_slugs + restricted_country_slugs:
        if s in BOOKS_BY_SLUG and s not in [c["slug"] for c in candidates]:
            candidates.append({"slug": s, "url": BOOKS_BY_SLUG[s]})
        if len(candidates) >= 3:
            break
    if not candidates:
        return ""
    # Map slug to display name (for the CTA card labels)
    display = {
        "argentina": "Argentina", "brazil": "Brazil", "canada": "Canada",
        "china": "China", "colombia": "Colombia", "france": "France",
        "germany": "Germany", "greece": "Greece", "indonesia": "Indonesia",
        "italy": "Italy", "japan": "Japan", "portugal": "Portugal",
        "spain": "Spain", "thailand": "Thailand", "turkey": "Turkey",
        "united-kingdom": "United Kingdom", "vietnam": "Vietnam",
    }
    cards = []
    for c in candidates:
        country = display.get(c["slug"], c["slug"].replace("-", " ").title())
        cards.append(
            f'      <a href="{c["url"]}" class="med-book-card">\n'
            f'        <span class="med-book-eyebrow">📕 Safety book</span>\n'
            f'        <strong>{html_mod.escape(country)}</strong>\n'
            f'        <span class="med-book-cta">Get the guide →</span>\n'
            f'      </a>'
        )
    return (
        f'  <section class="module-section" id="book-cta">\n'
        f'    <span class="section-eyebrow">Going deeper</span>\n'
        f'    <h2>Full safety guides for <em>{html_mod.escape(tier1_name)}-restricted</em> destinations.</h2>\n'
        f'    <p class="lede">If you are heading somewhere that restricts {html_mod.escape(tier1_name.lower())}, '
        f'our country-specific Kindle books cover every scam, customs trap, and emergency protocol we have '
        f'documented — in a single searchable offline volume.</p>\n'
        f'    <div class="med-books-grid">\n'
        + "\n".join(cards) + "\n"
        f'    </div>\n'
        f'  </section>'
    )


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
        "assistance_phone": "1-951-268-3900 (Away From Home Travel Line)",
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
