#!/usr/bin/env python3
"""Generate popular-picks HTML pages for a batch of slugs using Gemini.
Extracts template (CSS, nav, footer, map JS, filter JS) from a reference page
and fills with AI content.  Output matches the detroit-pizza reference template."""

import html as html_mod
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PP_DIR = REPO / "popular-picks"
API_DIR = REPO / "api" / "v1" / "picks"

# Reference page for template extraction (latest CSS)
REF_PAGE = PP_DIR / "kochi-coffee-shops" / "index.html"

API_KEY = os.environ.get("GEMINI_API_KEY") or subprocess.check_output(
    ["security", "find-generic-password", "-s", "google-api-key", "-w"], text=True
).strip()

import google.generativeai as genai
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

VIATOR_PID = "pid=P00292930&mcid=42383&medium=link"
MAPS_API_SCRIPT = '<script async src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBP0yidMjJEECgkIiZz2lw1NLsQ7jdASYc&callback=initPopularPicksMaps"></script>'

# ---------------------------------------------------------------------------
# Template extraction
# ---------------------------------------------------------------------------

def extract_template(ref_html: str) -> dict:
    """Extract CSS, nav, footer, map JS, and filter JS from reference page."""
    # Extract everything from <style> to </style>  (take ALL style blocks)
    css_blocks = re.findall(r'<style>(.*?)</style>', ref_html, re.DOTALL)
    css = "\n".join(css_blocks) if css_blocks else ""

    # Extract nav
    nav_match = re.search(
        r'(<!-- @include:nav:start -->.*?<!-- @include:nav:end -->)', ref_html, re.DOTALL
    )
    if not nav_match:
        nav_match = re.search(r'(<nav\b.*?</nav>)', ref_html, re.DOTALL)
    nav = nav_match.group(0) if nav_match else ""

    # Extract footer
    footer_match = re.search(
        r'(<!-- @include:footer:start -->.*?<!-- @include:footer:end -->)', ref_html, re.DOTALL
    )
    if not footer_match:
        footer_match = re.search(r'(<footer\b.*?</footer>)', ref_html, re.DOTALL)
    footer = footer_match.group(0) if footer_match else ""

    # Extract map-observer JS (the big IIFE after __POPULAR_PICKS_MAP__)
    map_js_match = re.search(
        r'(<script>\s*\(function\s*\(\)\s*\{\s*var sections.*?</script>)',
        ref_html, re.DOTALL,
    )
    map_js = map_js_match.group(1) if map_js_match else ""

    # Extract filter JS
    filter_js_match = re.search(
        r"(<script>\s*document\.addEventListener\('DOMContentLoaded'.*?</script>)",
        ref_html, re.DOTALL,
    )
    filter_js = filter_js_match.group(1) if filter_js_match else ""

    # Fallback: if filter JS not found in reference, use the generic filter script
    if not filter_js:
        filter_js = """<script>
document.addEventListener('DOMContentLoaded', function() {
    const chips = document.querySelectorAll('.filter-chip');
    const sections = document.querySelectorAll('.restaurant-section');

    chips.forEach(chip => {
        chip.addEventListener('click', function() {
            const group = this.dataset.filterGroup;
            const value = this.dataset.filterValue;

            // Toggle active state within group
            if (this.classList.contains('active')) {
                this.classList.remove('active');
            } else {
                // Deactivate others in same group
                document.querySelectorAll(`.filter-chip[data-filter-group="${group}"]`).forEach(c => c.classList.remove('active'));
                this.classList.add('active');
            }

            // Get active filters
            const activeFilters = {};
            document.querySelectorAll('.filter-chip.active').forEach(c => {
                activeFilters[c.dataset.filterGroup] = c.dataset.filterValue;
            });

            // Apply filters
            sections.forEach(section => {
                let show = true;
                if (activeFilters.style) {
                    const sectionStyle = section.dataset.filterStyle || '';
                    if (sectionStyle.toLowerCase() !== activeFilters.style.toLowerCase()) show = false;
                }
                if (activeFilters.price) {
                    const sectionPrice = section.dataset.filterPrice || '';
                    if (sectionPrice !== activeFilters.price) show = false;
                }
                if (activeFilters.area) {
                    const sectionArea = section.dataset.filterArea || '';
                    if (sectionArea !== activeFilters.area) show = false;
                }
                section.classList.toggle('filtered-out', !show);
            });
        });
    });
});
</script>"""

    return {
        "css": css,
        "nav": nav,
        "footer": footer,
        "map_js": map_js,
        "filter_js": filter_js,
    }


# ---------------------------------------------------------------------------
# Gemini prompt & content generation
# ---------------------------------------------------------------------------

def generate_page_content(slug: str, city: str, country: str, title: str, category: str) -> dict:
    """Use Gemini to generate all content for a popular-picks page."""

    prompt = f"""You are a food/travel content expert. Generate content for a popular-picks page about "{title}" in {city}, {country}.

Return a JSON object with this EXACT structure (no markdown fences, no trailing commas):

{{
  "pageTitle": "{title} (2026) — Reddit-Backed Guide | tabiji.ai",
  "h1": "10 Best {title.replace('Best ', '').replace('best ', '')}",
  "metaDescription": "SEO meta description, 150-170 chars. Mention Reddit, local reviews, and that a map is included.",
  "heroSubtitle": "One or two sentence teaser about the food scene in {city}.",
  "intro": [
    "First paragraph — bold opening setting the scene for {category} in {city}. Make the first sentence bold-worthy.",
    "Second paragraph — history / cultural context.",
    "Third paragraph — overview of styles/variations available.",
    "Fourth paragraph — how the guide was researched (mention Reddit subreddits, cross-referencing critics)."
  ],
  "methodology": "One dense paragraph: how many Reddit posts, which subreddits, which critic sources, verification date.",
  "quickAnswer": {{
    "lead": "2-3 sentence bold summary — mention price range and number of spots.",
    "bestOverall": "Name — short reason",
    "bestBudget": "Name — short reason",
    "bestExperience": "Name — short reason",
    "priceRange": "$X – $Y per person",
    "topPick": "Name — $$ — X.X★ (N reviews)",
    "mustTry": "The signature dish/drink everyone should try"
  }},
  "topVerdicts": [
    {{"name": "Venue1 Name", "verdict": "One sentence verdict."}},
    {{"name": "Venue2 Name", "verdict": "One sentence verdict."}},
    {{"name": "Venue3 Name", "verdict": "One sentence verdict."}}
  ],
  "budgetTiers": [
    {{
      "label": "Category label 1",
      "emoji": "single emoji",
      "color": "#hex background color",
      "borderColor": "#hex border color",
      "textColor": "#hex text color",
      "items": [
        {{"name": "Venue Name", "anchor": "venue-slug", "oneLiner": "short description"}}
      ]
    }},
    {{
      "label": "Category label 2",
      "emoji": "single emoji",
      "color": "#hex",
      "borderColor": "#hex",
      "textColor": "#hex",
      "items": [
        {{"name": "Venue Name", "anchor": "venue-slug", "oneLiner": "short description"}}
      ]
    }},
    {{
      "label": "Category label 3",
      "emoji": "single emoji",
      "color": "#hex",
      "borderColor": "#hex",
      "textColor": "#hex",
      "items": [
        {{"name": "Venue Name", "anchor": "venue-slug", "oneLiner": "short description"}}
      ]
    }}
  ],
  "filterStyles": ["Style1", "Style2", "Style3"],
  "venues": [
    {{
      "rank": 1,
      "name": "Venue Name",
      "neighborhood": "Neighborhood/Area name",
      "address": "Street address",
      "cuisineStyle": "Primary style for filtering (matches one of filterStyles)",
      "cuisineTags": ["tag1", "tag2"],
      "priceTier": "budget or mid",
      "priceRange": "$X-Y per person",
      "rating": 4.5,
      "reviewCount": 1234,
      "description": "2-3 sentence verdict about why this place is great.",
      "bestFor": "One sentence — who should come here and why.",
      "strengths": "X.X★ from N Google reviews · Key strength · Another strength",
      "whatToOrder": "Specific dish recommendation with details.",
      "insiderTip": "Practical insider tip for visiting.",
      "lat": 0.0000,
      "lng": 0.0000,
      "phone": "+1XXXXXXXXXX (E.164 format)",
      "website": "https://example.com",
      "redditQuotes": [
        {{"text": "Natural Reddit-style quote mentioning the venue.", "source": "r/cityname"}},
        {{"text": "Second Reddit-style quote.", "source": "r/food"}}
      ]
    }}
  ],
  "planning": {{
    "reservations": "Paragraph about reservation policies across the venues.",
    "payment": "Paragraph about payment methods, cash-only spots.",
    "bestTimes": "Paragraph about best times to visit, avoiding crowds.",
    "route": "Recommended crawl route mentioning 4 venues by name (use their anchor IDs for links).",
    "gettingAround": "Paragraph about transportation in {city}."
  }},
  "faqs": [
    {{"question": "Full question?", "answer": "Detailed 2-3 sentence answer."}}
  ]
}}

REQUIREMENTS:
- venues: exactly 10 items, ranked 1-10. Use REAL venue names that actually exist in {city}.
- Each venue must have a real neighborhood, realistic price range, real phone number, real website URL
- Each venue MUST have accurate lat/lng coordinates (decimal degrees, e.g. 38.1157, 13.3615 for Palermo). Use the real location of the venue.
- faqs: exactly 8 items, detailed and specific
- cuisineTags: 2 tags per venue
- filterStyles: unique style values derived from venue cuisineStyle fields (no duplicates)
- budgetTiers: exactly 3 groups with 3 items each (use real venue names matching the venues array)
- budgetTiers items anchor values MUST match the slug form of the venue name (lowercase, hyphens, no special chars)
- topVerdicts: exactly 3 items for the top 3 ranked venues
- redditQuotes: exactly 2 per venue, should sound natural and mention the venue by name
- planning.route: mention 4 venues and include their anchor IDs for linking
- All content must be specific and factual — real place names, realistic prices
- Do NOT use markdown in any field — only plain text
- Phone numbers in E.164 format (e.g. +13135551234)
- Prices should be in local currency with USD equivalent where applicable"""

    response = model.generate_content(prompt)
    text = response.text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def venue_to_section_id(name: str) -> str:
    """Convert venue name to a URL-safe section ID."""
    sid = re.sub(r'\([^)]*\)', '', name).strip()
    sid = re.sub(r'[^\w\s-]', '', sid.lower())
    sid = re.sub(r'[\s_]+', '-', sid).strip('-')
    return re.sub(r'-+', '-', sid)[:40]


def _esc(text: str) -> str:
    """HTML-escape text for safe embedding in attributes and content."""
    return html_mod.escape(str(text), quote=True)


def _format_phone_display(phone: str) -> str:
    """Format E.164 phone to display format.  Best-effort."""
    p = phone.strip()
    if p.startswith("+1") and len(p) == 12:
        return f"+1 ({p[2:5]}) {p[5:8]}-{p[8:]}"
    return p


def _price_tier_symbol(tier: str) -> str:
    return "$" if tier == "budget" else "$$"


# ---------------------------------------------------------------------------
# Venue section builder
# ---------------------------------------------------------------------------

def build_venue_section(venue: dict, slug: str, city: str) -> str:
    """Build HTML for a single venue section matching the detroit-pizza template."""
    section_id = venue_to_section_id(venue['name'])
    neighborhood = venue.get('neighborhood', '')
    address = venue.get('address', '')
    cuisine_style = venue.get('cuisineStyle', '')
    price_tier = venue.get('priceTier', 'mid')
    price_symbol = _price_tier_symbol(price_tier)
    price_range = venue.get('priceRange', '')
    rating = venue.get('rating', 0)
    review_count = venue.get('reviewCount', 0)
    phone = venue.get('phone', '')
    website = venue.get('website', '')
    description = venue.get('description', '')
    best_for = venue.get('bestFor', '')
    strengths = venue.get('strengths', '')
    what_to_order = venue.get('whatToOrder', '')
    insider_tip = venue.get('insiderTip', '')
    tags = venue.get('cuisineTags', [])
    reddit_quotes = venue.get('redditQuotes', [])
    rank = venue['rank']

    maps_query = f"{venue['name']}+{neighborhood}+{city}".replace(' ', '+')
    maps_url = f"https://maps.google.com/?q={maps_query}"

    # Tag list HTML
    tag_list_html = " ".join(
        f'<span class="cuisine-tag">{_esc(t)}</span>' for t in tags
    )

    # Reddit quotes HTML
    quotes_html = ""
    for q in reddit_quotes[:2]:
        quotes_html += f"""    <div class="reddit-quote">
        {_esc(q.get('text', ''))}
        <span class="source">&mdash; {_esc(q.get('source', 'r/travel'))}</span>
    </div>\n"""

    # Contact HTML
    contact_parts = []
    if phone:
        display_phone = _format_phone_display(phone)
        contact_parts.append(
            f'<span>\U0001F4DE <a href="tel:{_esc(phone)}">{_esc(display_phone)}</a></span>'
        )
    if website:
        contact_parts.append(
            f'<span>\U0001F310 <a href="{_esc(website)}" target="_blank" rel="noopener">Website</a></span>'
        )
    contact_html = "\n    ".join(contact_parts)

    # Image alt text
    img_alt = f"{_esc(venue['name'])} in {_esc(neighborhood)} — {_esc(description[:80])}"

    lat = venue.get('lat', 0)
    lng = venue.get('lng', 0)
    lat_lng_attrs = f' data-map-lat="{lat}" data-map-lng="{lng}"' if lat and lng else ''

    return f"""<section class="restaurant-section" id="{_esc(section_id)}" data-filter-style="{_esc(cuisine_style)}" data-filter-price="{_esc(price_tier)}" data-filter-area="{_esc(neighborhood)}" data-map-name="{rank}. {_esc(venue['name'])}" data-map-cta-url="{_esc(maps_url)}" data-map-query="{_esc(venue['name'])}, {_esc(neighborhood)}, {_esc(city)}"{lat_lng_attrs}>
    <div class="restaurant-header">
        <h2><span class="restaurant-number">{rank}</span>{_esc(venue['name'])}</h2>
        <span class="cuisine-tag">{_esc(cuisine_style)}</span>
        <span class="google-rating"><span class="star">&#9733;</span> {rating} &middot; {review_count:,} reviews</span>
    </div>
    <div class="restaurant-details">
        <span>\U0001F4B4 {_esc(price_symbol)}</span>
        <span>\U0001F4CD {_esc(neighborhood)}</span>
        <a href="{_esc(maps_url)}" target="_blank" rel="noopener">\U0001F4CC Google Maps &rarr;</a>
    </div>
    <div class="pick-quick-take">
      <strong>Verdict:</strong> {_esc(description)}
    </div>
    <div class="pick-tag-list">{tag_list_html}</div>

    <div class="comparison-card">
      <h3>Quick comparison</h3>
      <dl class="comparison-grid">
        <div class="comparison-row"><dt>Best for</dt><dd>{_esc(best_for)}</dd></div>
        <div class="comparison-row"><dt>Strengths</dt><dd>{_esc(strengths)}</dd></div>
        <div class="comparison-row"><dt>Price / value</dt><dd>{_esc(price_symbol)} &middot; {rating}&#9733;</dd></div>
        <div class="comparison-row"><dt>What to order</dt><dd>{_esc(what_to_order)}</dd></div>
        <div class="comparison-row"><dt>Insider tip</dt><dd>{_esc(insider_tip)}</dd></div>
      </dl>
    </div>

    <div class="shop-hours">
        <details>
            <summary>\U0001F550 Hours</summary>
            <div class="hours-grid">
            <span>Mon</span><span>11:00 AM &ndash; 9:00 PM</span><span>Tue</span><span>11:00 AM &ndash; 9:00 PM</span><span>Wed</span><span>11:00 AM &ndash; 9:00 PM</span><span>Thu</span><span>11:00 AM &ndash; 9:00 PM</span><span>Fri</span><span>11:00 AM &ndash; 10:00 PM</span><span>Sat</span><span>11:00 AM &ndash; 10:00 PM</span><span>Sun</span><span>12:00 &ndash; 9:00 PM</span>
            </div>
        </details>
    </div>
    <div class="shop-contact">{contact_html}</div>

    <img src="https://img.tabiji.ai/popular-picks/{_esc(slug)}/{_esc(section_id)}.jpg" alt="{img_alt}" style="width:100%;border-radius:12px;margin-bottom:1rem;" loading="lazy">

{quotes_html}</section>"""


# ---------------------------------------------------------------------------
# Map config builder
# ---------------------------------------------------------------------------

def build_map_config(venues: list, slug: str, city: str, category: str) -> dict:
    """Build the __POPULAR_PICKS_MAP__ config for interactive Google Maps."""
    default_query = f"{category}+in+{city}".replace(' ', '+')
    picks = []
    for v in venues:
        sid = venue_to_section_id(v['name'])
        neighborhood = v.get('neighborhood', '')
        maps_query = f"{v['name']}+{neighborhood}+{city}".replace(' ', '+')
        pick = {
            "anchorId": sid,
            "rank": v["rank"],
            "name": v["name"],
            "label": f"{v['rank']}. {v['name']}",
            "ctaUrl": f"https://maps.google.com/?q={maps_query}",
            "mapQuery": f"{v['name']}, {neighborhood}, {city}",
        }
        if v.get("lat") and v.get("lng"):
            pick["lat"] = v["lat"]
            pick["lng"] = v["lng"]
        picks.append(pick)
    return {
        "enabled": True,
        "title": f"{category.title()} Map",
        "ctaLabel": "Open in Google Maps",
        "defaultCtaUrl": f"https://www.google.com/maps/search/{default_query}",
        "picks": picks,
    }


# ---------------------------------------------------------------------------
# Map sidebar / inline builder
# ---------------------------------------------------------------------------

def _build_map_panel(panel_type: str, venues: list, city: str, category: str) -> str:
    """Build map sidebar or inline section.  panel_type is 'desktop' or 'mobile'."""
    tag = "section" if panel_type == "mobile" else "section"
    css_class = "map-sidebar" if panel_type == "desktop" else "map-inline"
    first = venues[0] if venues else {}
    first_name = _esc(first.get('name', ''))
    first_maps_q = f"{first.get('name', '')}+{first.get('neighborhood', '')}+{city}".replace(' ', '+')
    first_maps_url = f"https://maps.google.com/?q={first_maps_q}"

    # Map legend links (first 6)
    legend_items = ""
    for v in venues[:6]:
        sid = venue_to_section_id(v['name'])
        legend_items += f"""      <li>
        <a href="#{sid}">{v['rank']}. {_esc(v['name'])}</a>
      </li>\n"""

    wrapper_open = ""
    wrapper_close = ""
    if panel_type == "desktop":
        wrapper_open = "    <aside>\n"
        wrapper_close = "    </aside>\n"

    return f"""{wrapper_open}    <{tag} class="{css_class}" data-map-panel="{panel_type}">
      <h2>{_esc(category.title())} Map</h2>
      <div class="map-active-pick" data-map-active-pick>1. {first_name}</div>
      <div class="popular-picks-map" data-map-canvas aria-label="{_esc(category.title())} Map"></div>
      <div class="map-legend">
        <strong>Start with:</strong>
        <ul>
{legend_items}        </ul>
        <p><a href="{_esc(first_maps_url)}" target="_blank" rel="noopener" data-map-cta>Open in Google Maps &rarr;</a></p>
      </div>
    </{tag}>
{wrapper_close}"""


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

def _build_quick_answer_section(qa: dict, verdicts: list, today: str) -> str:
    """Build the two-column quick-answer section."""
    verdicts_html = ""
    for v in verdicts[:3]:
        verdicts_html += f'            <li><strong>{_esc(v["name"])}:</strong> {_esc(v["verdict"])}</li>\n'

    return f"""        <section class="quick-answer-section">
          <div class="quick-answer-card">
            <p class="eyebrow">Quick answer</p>
            <p class="quick-answer-lead"><strong>{_esc(qa.get('lead', ''))}</strong></p>
            <dl class="quick-answer-grid">
              <div class="comparison-row"><dt>Best overall</dt><dd>{_esc(qa.get('bestOverall', ''))}</dd></div><div class="comparison-row"><dt>Price range</dt><dd>{_esc(qa.get('priceRange', ''))}</dd></div><div class="comparison-row"><dt>Top pick</dt><dd>{_esc(qa.get('topPick', ''))}</dd></div><div class="comparison-row"><dt>Must-try</dt><dd>{_esc(qa.get('mustTry', ''))}</dd></div>
            </dl>
          </div>
          <div class="quick-answer-card">
            <p class="eyebrow">Top verdicts</p>
            <ul class="top-verdicts-list">
{verdicts_html}            </ul>
          </div>
        </section>"""


def _build_intro_section(paragraphs: list) -> str:
    """Build the intro section with 3-4 paragraphs."""
    if not paragraphs:
        return ""
    # Make first paragraph bold
    parts = []
    for i, p in enumerate(paragraphs):
        if i == 0:
            parts.append(f"<p><strong>{_esc(p)}</strong></p>")
        else:
            parts.append(f"<p>{_esc(p)}</p>")
    return f"""      <section class="intro-section">
        {"".join(parts)}
      </section>"""


def _build_methodology_section(text: str) -> str:
    """Build methodology section."""
    return f"""        <section class="methodology-section">
          <h2>How we built this list</h2>
          <p>{_esc(text)}</p>
        </section>"""


def _build_comparison_table(venues: list) -> str:
    """Build the 'All N Spots at a Glance' comparison table."""
    rows = ""
    for v in venues:
        sid = venue_to_section_id(v['name'])
        rows += f"""<tr>
<td><strong>#{v['rank']}</strong></td>
<td><a href="#{sid}">{_esc(v['name'])}</a></td>
<td>{_esc(v.get('cuisineStyle', ''))}</td>
<td>{_esc(_price_tier_symbol(v.get('priceTier', 'mid')))}</td>
<td>{v.get('rating', '')}&#9733;</td>
<td>{_esc(v.get('neighborhood', ''))}</td>
</tr>\n"""

    return f"""<div class="comparison-table-section" style="margin-bottom:1.4rem;background:white;border:1px solid var(--sand);border-radius:18px;padding:1.35rem 1.4rem;overflow-x:auto;">
<h2 style="color:var(--indigo);margin:0 0 1rem;font-size:1.15rem;">All {len(venues)} Spots at a Glance</h2>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;min-width:600px;">
<thead>
<tr style="border-bottom:2px solid var(--sand);text-align:left;">
<th style="padding:.5rem .4rem;color:var(--earth);font-size:.8rem;">#</th>
<th style="padding:.5rem .4rem;color:var(--earth);font-size:.8rem;">Name</th>
<th style="padding:.5rem .4rem;color:var(--earth);font-size:.8rem;">Style</th>
<th style="padding:.5rem .4rem;color:var(--earth);font-size:.8rem;">Price</th>
<th style="padding:.5rem .4rem;color:var(--earth);font-size:.8rem;">Rating</th>
<th style="padding:.5rem .4rem;color:var(--earth);font-size:.8rem;">Area</th>
</tr>
</thead>
<tbody>
{rows}</tbody>
</table>
</div>"""


def _build_budget_tiers(tiers: list) -> str:
    """Build the Quick Picks by Style / budget tiers cards."""
    cards = ""
    for tier in tiers:
        items_html = ""
        for item in tier.get('items', []):
            anchor = item.get('anchor', '')
            items_html += f'<div><strong><a href="#{_esc(anchor)}">{_esc(item["name"])}</a></strong> &mdash; {_esc(item.get("oneLiner", ""))}</div>\n'
        cards += f"""<div style="background:{_esc(tier.get('color', '#FFF3E0'))};border:1px solid {_esc(tier.get('borderColor', '#FFE0B2'))};border-radius:12px;padding:1rem;">
<div style="font-weight:700;color:{_esc(tier.get('textColor', '#E65100'))};margin-bottom:.4rem;">{_esc(tier.get('emoji', ''))} {_esc(tier.get('label', ''))}</div>
{items_html}</div>\n"""

    return f"""<div class="budget-tiers-section" style="margin-bottom:1.4rem;background:white;border:1px solid var(--sand);border-radius:18px;padding:1.35rem 1.4rem;">
<h2 style="color:var(--indigo);margin:0 0 1rem;font-size:1.15rem;">Quick Picks by Style</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(200px, 1fr));gap:1rem;">
{cards}</div>
</div>"""


def _build_filter_bar(filter_styles: list) -> str:
    """Build the filter bar with style + price chips."""
    style_chips = ""
    for style in filter_styles:
        style_chips += f'<span class="filter-chip" data-filter-group="style" data-filter-value="{_esc(style)}">{_esc(style)}</span>'

    return f"""<div class="filter-bar">
<span class="filter-label">Style:</span> {style_chips}
<span style="width:1px;height:20px;background:var(--sand);margin:0 .3rem;"></span>
<span class="filter-label">Price:</span> <span class="filter-chip" data-filter-group="price" data-filter-value="budget">Budget ($)</span><span class="filter-chip" data-filter-group="price" data-filter-value="mid">Mid-Range ($$)</span>
</div>"""


def _build_planning_section(planning: dict, city: str) -> str:
    """Build the planning section with 5 h3 subsections."""
    return f"""      <div class="planning-section" style="margin-bottom:1.4rem;background:white;border:1px solid var(--sand);border-radius:18px;padding:1.35rem 1.4rem;">
<h2 style="color:var(--indigo);margin:0 0 1rem;font-size:1.15rem;">Planning Your {_esc(city)} Food Crawl</h2>

<h3 style="color:var(--indigo);font-size:1rem;margin:.8rem 0 .4rem;">Reservations</h3>
<p style="color:var(--text-muted);margin:0 0 .8rem;">{planning.get('reservations', '')}</p>

<h3 style="color:var(--indigo);font-size:1rem;margin:.8rem 0 .4rem;">Payment &amp; Cash-Only Spots</h3>
<p style="color:var(--text-muted);margin:0 0 .8rem;">{planning.get('payment', '')}</p>

<h3 style="color:var(--indigo);font-size:1rem;margin:.8rem 0 .4rem;">Best Times to Avoid Lines</h3>
<p style="color:var(--text-muted);margin:0 0 .8rem;">{planning.get('bestTimes', '')}</p>

<h3 style="color:var(--indigo);font-size:1rem;margin:.8rem 0 .4rem;">Recommended Crawl Route</h3>
<p style="color:var(--text-muted);margin:0 0 .8rem;">{planning.get('route', '')}</p>

<h3 style="color:var(--indigo);font-size:1rem;margin:.8rem 0 .4rem;">Getting Around</h3>
<p style="color:var(--text-muted);margin:0 0 .8rem;">{planning.get('gettingAround', '')}</p>
</div>"""


def _build_faq_section(faqs: list) -> str:
    """Build the FAQ section."""
    items = ""
    for faq in faqs:
        items += f'<div class="faq-item"><h3>{_esc(faq["question"])}</h3><p>{_esc(faq["answer"])}</p></div>'
    return f"""<section class="faq-section">
        <h2>Frequently Asked Questions</h2>
        {items}
      </section>"""


def _build_viator_section(city: str) -> str:
    """Build the Viator affiliate section with 4 cards."""
    city_q = city.replace(' ', '+')
    cards = [
        ("Food Tour", f"{city} Food Tours", f"https://www.viator.com/search/{city_q}+food+tour?{VIATOR_PID}"),
        ("Day Trip", f"{city} Day Trips", f"https://www.viator.com/search/{city_q}+day+trips?{VIATOR_PID}"),
        ("Cultural Tour", f"{city} Cultural Tours", f"https://www.viator.com/search/{city_q}+cultural+tour?{VIATOR_PID}"),
        ("Explore More", f"All {city} Tours & Activities &rarr;", f"https://www.viator.com/search/{city_q}+tours?{VIATOR_PID}"),
    ]
    cards_html = ""
    for tour_type, tour_name, url in cards:
        cards_html += f"""      <a class="viator-card" href="{_esc(url)}" target="_blank" rel="noopener sponsored">
        <span class="tour-type">{_esc(tour_type)}</span>
        <span class="tour-name">{tour_name}</span>
      </a>\n"""

    return f"""      <section class="viator-section">
        <h2>\U0001F3AB Book {_esc(city)} Experiences</h2>
        <p class="viator-subtitle">Tours and activities hand-picked for this guide &mdash; book with free cancellation</p>
        <div class="viator-cards">
{cards_html}        </div>
        <p class="viator-powered">Experiences via Viator &mdash; free cancellation on most tours</p>
      </section>"""


def _build_cta_section(city: str) -> str:
    """Build the CTA section."""
    return f"""      <section class="cta-section">
          <h2>Plan your {_esc(city)} trip</h2>
          <p>Get a free custom itinerary for {_esc(city)} &mdash; built from real traveler insights.</p>
          <a href="/plan" class="cta-btn">Get a Free Itinerary &rarr;</a>
        </section>"""


# ---------------------------------------------------------------------------
# JSON-LD schema builders
# ---------------------------------------------------------------------------

def _build_article_schema(content: dict, slug: str, og_image: str, today: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": content["h1"],
        "description": content["metaDescription"],
        "author": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai"},
        "publisher": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai"},
        "datePublished": today,
        "dateModified": today,
        "mainEntityOfPage": f"https://tabiji.ai/popular-picks/{slug}/",
        "image": og_image,
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": [
                ".hero h1",
                ".hero .subtitle",
                ".quick-answer-section",
                ".budget-tiers-section",
                ".faq-section",
            ],
        },
    }


def _build_itemlist_schema(content: dict, slug: str, city: str, today: str) -> dict:
    items = []
    for v in content["venues"]:
        sid = venue_to_section_id(v['name'])
        neighborhood = v.get('neighborhood', '')
        maps_query = f"{v['name']}+{neighborhood}+{city}".replace(' ', '+')
        maps_url = f"https://maps.google.com/?q={maps_query}"
        price_symbol = _price_tier_symbol(v.get('priceTier', 'mid'))

        item = {
            "@type": "ListItem",
            "position": v["rank"],
            "url": f"https://tabiji.ai/popular-picks/{slug}/#{sid}",
            "item": {
                "@type": "Restaurant",
                "name": v["name"],
                "servesCuisine": v.get("cuisineStyle", ""),
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": v.get("address", ""),
                    "addressLocality": neighborhood,
                    "addressCountry": "US",
                },
                "priceRange": price_symbol,
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": v.get("rating", 0),
                    "reviewCount": v.get("reviewCount", 0),
                    "bestRating": 5,
                },
                "geo": {
                    "@type": "GeoCoordinates",
                    "latitude": 0.0,
                    "longitude": 0.0,
                },
                "telephone": v.get("phone", ""),
                "image": f"https://img.tabiji.ai/popular-picks/{slug}/{sid}.jpg",
                "url": v.get("website", ""),
                "hasMap": maps_url,
                "sameAs": [u for u in [v.get("website", ""), maps_url] if u],
            },
        }
        items.append(item)

    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": content["h1"],
        "description": content["metaDescription"],
        "url": f"https://tabiji.ai/popular-picks/{slug}/",
        "numberOfItems": len(content["venues"]),
        "itemListOrder": "https://schema.org/ItemListOrderAscending",
        "itemListElement": items,
    }


def _build_faq_schema(faqs: list) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f["question"],
                "acceptedAnswer": {"@type": "Answer", "text": f["answer"]},
            }
            for f in faqs
        ],
    }


def _build_tourist_trip_schema(content: dict, slug: str, city: str, today: str) -> dict:
    qa = content.get("quickAnswer", {})
    return {
        "@context": "https://schema.org",
        "@type": "TouristTrip",
        "name": content["h1"],
        "description": f"in Popular Picks — {city}, verified {today[:7]}.",
        "url": f"https://tabiji.ai/popular-picks/{slug}/",
        "additionalProperty": [
            {"@type": "PropertyValue", "name": "totalOptions", "value": str(len(content["venues"]))},
            {"@type": "PropertyValue", "name": "bestOverall", "value": qa.get("topPick", "")},
            {"@type": "PropertyValue", "name": "topPick", "value": qa.get("bestOverall", "")},
            {"@type": "PropertyValue", "name": "lastVerified", "value": today[:7]},
        ],
    }


def _build_breadcrumb_schema(content: dict, slug: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tabiji.ai/"},
            {"@type": "ListItem", "position": 2, "name": "Popular Picks", "item": "https://tabiji.ai/popular-picks/"},
            {"@type": "ListItem", "position": 3, "name": content["h1"]},
        ],
    }


# ---------------------------------------------------------------------------
# Full page builder
# ---------------------------------------------------------------------------

def build_full_page(slug: str, city: str, country: str, title: str, category: str,
                    content: dict, template: dict) -> str:
    """Build the complete HTML page matching the detroit-pizza reference."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    venue_count = len(content["venues"])
    first_section_id = venue_to_section_id(content['venues'][0]['name']) if content['venues'] else 'hero-bg'
    og_image = f"https://img.tabiji.ai/popular-picks/{slug}/{first_section_id}.jpg"

    # JSON-LD schemas
    article_schema = _build_article_schema(content, slug, og_image, today)
    itemlist_schema = _build_itemlist_schema(content, slug, city, today)
    faq_schema = _build_faq_schema(content.get("faqs", []))
    tourist_trip = _build_tourist_trip_schema(content, slug, city, today)
    breadcrumb = _build_breadcrumb_schema(content, slug)

    # Build sections
    qa = content.get("quickAnswer", {})
    top_verdicts = content.get("topVerdicts", [])
    quick_answer_html = _build_quick_answer_section(qa, top_verdicts, today)
    intro_html = _build_intro_section(content.get("intro", []))
    methodology_html = _build_methodology_section(content.get("methodology", ""))
    comparison_table_html = _build_comparison_table(content["venues"])
    budget_tiers_html = _build_budget_tiers(content.get("budgetTiers", []))
    filter_bar_html = _build_filter_bar(content.get("filterStyles", []))

    # Venue sections
    venues_html = "\n".join(build_venue_section(v, slug, city) for v in content["venues"])

    # Post-venue sections
    planning_html = _build_planning_section(content.get("planning", {}), city)
    faq_html = _build_faq_section(content.get("faqs", []))
    viator_html = _build_viator_section(city)
    cta_html = _build_cta_section(city)

    # Map panels
    map_sidebar_html = _build_map_panel("desktop", content["venues"], city, category)
    map_inline_html = _build_map_panel("mobile", content["venues"], city, category)

    # Map config JSON
    map_config = build_map_config(content['venues'], slug, city, category)
    map_config_json = json.dumps(map_config, ensure_ascii=False)

    def _schema_tag(obj: dict) -> str:
        return f'    <script type="application/ld+json">{json.dumps(obj, indent=2, ensure_ascii=False)}</script>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-D7QHNRXLHJ"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-D7QHNRXLHJ');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="https://img.tabiji.ai/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="192x192" href="https://img.tabiji.ai/icon-192.png">
    <title>{_esc(content['pageTitle'])}</title>
    <meta name="description" content="{_esc(content['metaDescription'])}">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="https://tabiji.ai/popular-picks/{slug}/">
    <meta property="og:title" content="{_esc(content['pageTitle'])}">
    <meta property="og:description" content="{_esc(content['metaDescription'])}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://tabiji.ai/popular-picks/{slug}/">
    <meta property="og:image" content="{og_image}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="675">
    <meta property="og:site_name" content="tabiji.ai">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{_esc(content['h1'])}">
    <meta name="twitter:description" content="{_esc(content['metaDescription'])}">
    <meta name="twitter:image" content="{og_image}">
    <meta property="article:published_time" content="{today}T00:00:00Z">
    <meta property="article:modified_time" content="{today}T00:00:00Z">
{_schema_tag(article_schema)}
{_schema_tag(itemlist_schema)}
{_schema_tag(faq_schema)}
{_schema_tag(tourist_trip)}
    <style>
{template['css']}
    </style>
{_schema_tag(breadcrumb)}
<link rel="stylesheet" href="/assets/shared-shell.css">
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#2D3A5C">
<script defer src="/assets/shared-shell.js"></script>
</head>
<body>
  {template['nav']}


    <section class="hero">
      <div class="hero-badge">\U0001F3C6 Popular Picks &mdash; {_esc(city)}, {_esc(country)}</div>
      <h1>{_esc(content['h1'])}</h1>
      <p class="subtitle">{_esc(content.get('heroSubtitle', ''))}</p>
      <div class="hero-meta">

      </div>
    </section>

  <div class="page-layout">
{map_sidebar_html}
    <main class="content">

{quick_answer_html}

{intro_html}


{map_inline_html}

{methodology_html}

      <section class="pick-list">

{comparison_table_html}
{budget_tiers_html}
{filter_bar_html}
{venues_html}
      </section>

{planning_html}
{faq_html}


{viator_html}


{cta_html}
    </main>
  </div>

  {template['footer']}
  <script>
    window.__POPULAR_PICKS_MAP__ = {map_config_json};
  </script>
  {template['map_js']}
  {MAPS_API_SCRIPT}

{template['filter_js']}
</body>
</html>"""


# ---------------------------------------------------------------------------
# API JSON builder
# ---------------------------------------------------------------------------

def build_api_json(slug: str, city: str, country: str, content: dict) -> dict:
    """Build API JSON for a popular-picks page."""
    return {
        "slug": slug,
        "city": city,
        "country": country,
        "title": content["h1"],
        "venueCount": len(content["venues"]),
        "venues": [
            {
                "rank": v["rank"],
                "name": v["name"],
                "neighborhood": v.get("neighborhood", ""),
                "priceRange": v.get("priceRange", ""),
                "cuisineTags": v.get("cuisineTags", []),
                "cuisineStyle": v.get("cuisineStyle", ""),
                "priceTier": v.get("priceTier", ""),
                "rating": v.get("rating", 0),
                "reviewCount": v.get("reviewCount", 0),
            }
            for v in content["venues"]
        ],
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }


# ---------------------------------------------------------------------------
# Process & main
# ---------------------------------------------------------------------------

def process_page(slug: str, city: str, country: str, title: str, category: str, template: dict) -> str:
    """Generate and save one popular-picks page. Returns status."""
    html_path = PP_DIR / slug / "index.html"
    api_path = API_DIR / f"{slug}.json"

    if html_path.exists():
        return f"  \u23ED\uFE0F  {slug}: already exists, skipping"

    try:
        content = generate_page_content(slug, city, country, title, category)
        html = build_full_page(slug, city, country, title, category, content, template)

        html_path.parent.mkdir(parents=True, exist_ok=True)
        html_path.write_text(html)

        api_json = build_api_json(slug, city, country, content)
        api_path.parent.mkdir(parents=True, exist_ok=True)
        api_path.write_text(json.dumps(api_json, indent=2, ensure_ascii=False) + "\n")

        return f"  \u2705 {slug}: {len(content['venues'])} venues, {len(html)} bytes"
    except Exception as e:
        return f"  \u274C {slug}: {e}"


def main():
    if len(sys.argv) < 2:
        print("Usage: gen_popular_picks_batch.py <slug:city:country:title:category> ...")
        print("  Each arg format: slug|city|country|title|category (pipe-separated)")
        sys.exit(1)

    # Parse args
    pages = []
    for arg in sys.argv[1:]:
        parts = arg.split("|")
        if len(parts) != 5:
            print(f"Bad format: {arg} (need slug|city|country|title|category)")
            continue
        pages.append({"slug": parts[0], "city": parts[1], "country": parts[2], "title": parts[3], "category": parts[4]})

    print(f"Processing {len(pages)} popular-picks pages...")

    # Extract template from reference page
    ref_html = REF_PAGE.read_text()
    template = extract_template(ref_html)
    print(f"Template extracted: CSS={len(template['css'])}chars, nav={len(template['nav'])}chars, map_js={len(template['map_js'])}chars, filter_js={len(template['filter_js'])}chars")

    results = []
    for i, page in enumerate(pages, 1):
        print(f"[{i}/{len(pages)}] {page['slug']}")
        result = process_page(page["slug"], page["city"], page["country"], page["title"], page["category"], template)
        print(result)
        results.append(result)
        if i < len(pages):
            time.sleep(1)

    success = sum(1 for r in results if "\u2705" in r)
    skip = sum(1 for r in results if "\u23ED" in r)
    fail = sum(1 for r in results if "\u274C" in r)
    print(f"\nDone: {success} built, {skip} skipped, {fail} failed")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
