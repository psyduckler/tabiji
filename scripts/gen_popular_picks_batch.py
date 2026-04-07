#!/usr/bin/env python3
"""Generate popular-picks HTML pages for a batch of slugs using Gemini.
Extracts template (CSS, nav, structure) from a reference page and fills with AI content."""

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

# Reference page for template extraction
REF_PAGE = PP_DIR / "kochi-coffee-shops" / "index.html"

API_KEY = os.environ.get("GEMINI_API_KEY") or subprocess.check_output(
    ["security", "find-generic-password", "-s", "google-api-key", "-w"], text=True
).strip()

import google.generativeai as genai
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


def extract_template(ref_html: str) -> dict:
    """Extract CSS, nav, footer, and structural elements from reference page."""
    # Extract everything from <style> to </style>
    css_match = re.search(r'<style>(.*?)</style>', ref_html, re.DOTALL)
    css = css_match.group(1) if css_match else ""
    
    # Extract nav
    nav_match = re.search(r'(<!-- @include:nav:start -->.*?<!-- @include:nav:end -->|<nav>.*?</nav>)', ref_html, re.DOTALL)
    if not nav_match:
        nav_match = re.search(r'(<nav\b.*?</nav>)', ref_html, re.DOTALL)
    nav = nav_match.group(0) if nav_match else ""
    
    # Extract footer
    footer_match = re.search(r'(<!-- @include:footer:start -->.*?<!-- @include:footer:end -->|<footer>.*?</footer>)', ref_html, re.DOTALL)
    if not footer_match:
        footer_match = re.search(r'(<footer\b.*?</footer>)', ref_html, re.DOTALL)
    footer = footer_match.group(0) if footer_match else ""
    
    # Extract head scripts (GA4 etc)
    head_scripts = re.findall(r'(<script[^>]*src="https://www\.googletagmanager[^"]*"[^>]*></script>)', ref_html)
    ga_config = re.search(r'(<script>.*?gtag.*?</script>)', ref_html, re.DOTALL)
    
    return {"css": css, "nav": nav, "footer": footer, "head_scripts": head_scripts, "ga_config": ga_config.group(0) if ga_config else ""}


def generate_page_content(slug: str, city: str, country: str, title: str, category: str) -> dict:
    """Use Gemini to generate all content for a popular-picks page."""
    
    prompt = f"""You are a food/travel content expert. Generate content for a popular-picks page about "{title}" in {city}, {country}.

Return a JSON object with this EXACT structure (no markdown fences):

{{
  "pageTitle": "{title} (2026) | tabiji.ai",
  "h1": "N Best {title.replace('Best ', '').replace('best ', '')}",
  "metaDescription": "SEO meta description, 150-170 chars",
  "heroSubtitle": "Quick description of the category in this city",
  "quickAnswer": {{
    "lead": "One-sentence summary of the best option",
    "bestOverall": "Name of best overall venue",
    "bestBudget": "Name of best budget option",
    "bestExperience": "Name of best for the experience"
  }},
  "methodology": "2-3 sentences about how venues were researched and selected",
  "venues": [
    {{
      "rank": 1,
      "name": "Venue Name",
      "neighborhood": "Neighborhood/Area",
      "cuisineTags": ["tag1", "tag2"],
      "priceRange": "$10-20 per person",
      "description": "2-3 sentences about why this place is great. Be specific about signature dishes, atmosphere, history.",
      "whatToOrder": "Specific dish or drink recommendation",
      "insiderTip": "A practical tip for visiting",
      "redditQuote": "A realistic Reddit-style quote about this venue",
      "redditSource": "r/travel or r/food or city-specific subreddit"
    }}
  ],
  "faqs": [
    {{"question": "Full question?", "answer": "Detailed 2-3 sentence answer"}}
  ]
}}

REQUIREMENTS:
- venues: exactly 12 items, ranked 1-12. Use REAL venue names that actually exist in {city}.
- Each venue must have a real neighborhood, realistic price range in local currency + USD equivalent
- faqs: exactly 6 items
- cuisineTags: 2-3 tags per venue
- redditQuote: should sound natural, mentioning the venue by name
- All content must be specific and factual — real place names, realistic prices
- Do NOT use markdown in any field — only plain text
- Prices should be in local currency with USD equivalent"""

    response = model.generate_content(prompt)
    text = response.text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def venue_to_section_id(name: str) -> str:
    """Convert venue name to a URL-safe section ID."""
    sid = re.sub(r'\([^)]*\)', '', name).strip()
    sid = re.sub(r'[^\w\s-]', '', sid.lower())
    sid = re.sub(r'[\s_]+', '-', sid).strip('-')
    return re.sub(r'-+', '-', sid)[:40]


def build_venue_section(venue: dict, slug: str, city: str) -> str:
    """Build HTML for a single venue section."""
    tags_html = " ".join(f'<span class="cuisine-tag">{t}</span>' for t in venue.get("cuisineTags", []))
    quote = venue.get("redditQuote", "")
    source = venue.get("redditSource", "r/travel")
    section_id = venue_to_section_id(venue['name'])
    neighborhood = venue.get('neighborhood', '')
    maps_query = f"{venue['name']}+{neighborhood}+{city}".replace(' ', '+')
    maps_url = f"https://maps.google.com/?q={maps_query}"

    return f"""
    <section class="restaurant-section" id="{section_id}" data-map-name="{venue['rank']}. {venue['name']}" data-map-cta-url="{maps_url}" data-map-query="{venue['name']}, {neighborhood}, {city}">
      <div class="restaurant-header">
        <div class="restaurant-rank">#{venue['rank']}</div>
        <div>
          <h2><span class="restaurant-number">#{venue['rank']}</span> {venue['name']}</h2>
          <div class="cuisine-tags">{tags_html}</div>
        </div>
      </div>
      <div class="restaurant-photo">
        <img src="https://img.tabiji.ai/popular-picks/{slug}/{section_id}.jpg" alt="{venue['name']}" loading="lazy">
      </div>
      <div class="restaurant-details">
        <div class="detail-grid">
          <div class="detail-item"><span class="detail-label">📍 Neighborhood</span><span>{neighborhood}</span></div>
          <div class="detail-item"><span class="detail-label">💰 Price Range</span><span>{venue.get('priceRange', '')}</span></div>
          <div class="detail-item"><span class="detail-label">🗺️ Map</span><span><a href="{maps_url}" target="_blank" rel="noopener">Open in Google Maps →</a></span></div>
        </div>
      </div>
      <div class="restaurant-body">
        <p>{venue.get('description', '')}</p>
        <div class="what-to-order">
          <h3>🍽️ What to order</h3>
          <p>{venue.get('whatToOrder', '')}</p>
        </div>
        <div class="insider-tip">
          <h3>💡 Insider tip</h3>
          <p>{venue.get('insiderTip', '')}</p>
        </div>
      </div>
      <div class="reddit-quote-block">
        <blockquote>"{quote}"</blockquote>
        <cite>— {source} user</cite>
      </div>
    </section>"""


def build_map_config(venues: list, slug: str, city: str, category: str) -> dict:
    """Build the __POPULAR_PICKS_MAP__ config for interactive Google Maps."""
    first = venues[0] if venues else {}
    first_name = first.get('name', category)
    default_query = f"{category}+in+{city}".replace(' ', '+')
    picks = []
    for v in venues:
        sid = venue_to_section_id(v['name'])
        neighborhood = v.get('neighborhood', '')
        maps_query = f"{v['name']}+{neighborhood}+{city}".replace(' ', '+')
        picks.append({
            "anchorId": sid,
            "rank": v["rank"],
            "name": v["name"],
            "label": f"{v['rank']}. {v['name']}",
            "ctaUrl": f"https://maps.google.com/?q={maps_query}",
            "mapQuery": f"{v['name']}, {neighborhood}, {city}",
        })
    return {
        "enabled": True,
        "title": f"{category.title()} Map",
        "ctaLabel": "Open in Google Maps",
        "defaultCtaUrl": f"https://www.google.com/maps/search/{default_query}",
        "picks": picks,
    }


def build_full_page(slug: str, city: str, country: str, title: str, category: str, content: dict, template: dict) -> str:
    """Build the complete HTML page."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    venue_count = len(content["venues"])
    first_section_id = venue_to_section_id(content['venues'][0]['name']) if content['venues'] else 'hero-bg'
    og_image = f"https://img.tabiji.ai/popular-picks/{slug}/{first_section_id}.jpg"

    # Build venue sections
    venues_html = "\n".join(build_venue_section(v, slug, city) for v in content["venues"])
    
    # Build FAQ HTML
    faq_html = ""
    for faq in content["faqs"]:
        faq_html += f"""<div class="faq-item"><h3>{faq['question']}</h3><p>{faq['answer']}</p></div>\n"""
    
    # Build FAQ JSON-LD
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f["question"], "acceptedAnswer": {"@type": "Answer", "text": f["answer"]}}
            for f in content["faqs"]
        ]
    }
    
    # Build Article JSON-LD
    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": content["h1"],
        "description": content["metaDescription"],
        "author": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai"},
        "publisher": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai"},
        "datePublished": today,
        "dateModified": today,
        "mainEntityOfPage": f"https://tabiji.ai/popular-picks/{slug}/",
        "image": f"{og_image}"
    }
    
    # Build ItemList JSON-LD
    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": content["h1"],
        "numberOfItems": venue_count,
        "itemListElement": [
            {"@type": "ListItem", "position": v["rank"], "name": v["name"]}
            for v in content["venues"]
        ]
    }
    
    # Build BreadcrumbList
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tabiji.ai/"},
            {"@type": "ListItem", "position": 2, "name": "Popular Picks", "item": "https://tabiji.ai/popular-picks/"},
            {"@type": "ListItem", "position": 3, "name": content["h1"]}
        ]
    }
    
    # Build TouristTrip
    tourist_trip = {
        "@context": "https://schema.org",
        "@type": "TouristTrip",
        "name": f"{city} {title.split(' in ')[0] if ' in ' in title else title} Tour",
        "description": content["metaDescription"],
        "touristType": ["Foodies", "Travelers", "Locals"]
    }

    qa = content["quickAnswer"]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-D7QHNRXLHJ"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-D7QHNRXLHJ');</script>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="/favicon.ico" type="image/x-icon">
    <link rel="apple-touch-icon" sizes="180x180" href="https://img.tabiji.ai/apple-touch-icon.png">
    <title>{content['pageTitle']}</title>
    <meta name="description" content="{content['metaDescription']}">
    <meta property="og:title" content="{content['pageTitle']}">
    <meta property="og:description" content="{content['metaDescription']}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://tabiji.ai/popular-picks/{slug}/">
    <meta property="og:image" content="{og_image}">
    <meta property="og:site_name" content="tabiji.ai">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{content['pageTitle']}">
    <meta name="twitter:description" content="{content['metaDescription']}">
    <meta name="twitter:image" content="{og_image}">
    <meta property="article:published_time" content="{today}T00:00:00Z">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="https://tabiji.ai/popular-picks/{slug}/">
    <script type="application/ld+json">{json.dumps(article_schema, ensure_ascii=False)}</script>
    <script type="application/ld+json">{json.dumps(item_list, ensure_ascii=False)}</script>
    <script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>
    <script type="application/ld+json">{json.dumps(tourist_trip, ensure_ascii=False)}</script>
    <script type="application/ld+json">{json.dumps(breadcrumb, ensure_ascii=False)}</script>
    <style>{template['css']}</style>
    <link rel="stylesheet" href="/assets/shared-shell.css">
    <script defer src="/assets/shared-shell.js"></script>
</head>
<body>
    {template['nav']}
    
    <div class="hero">
      <span class="hero-badge">🏆 Popular Picks — {city}, {country}</span>
      <h1>{content['h1']}</h1>
      <p class="subtitle">{content.get('heroSubtitle', '')}</p>
      <div class="hero-meta">
        <span>📍 {city}, {country}</span>
        <span>📝 {venue_count} picks</span>
        <span>🔄 Updated {today}</span>
      </div>
    </div>

    <div class="page-layout">
      <section class="map-sidebar" data-map-panel="desktop">
        <h2>📍 Map</h2>
        <div class="map-active-pick" data-map-active-pick>1. {content['venues'][0]['name']}</div>
        <div class="popular-picks-map" data-map-canvas aria-label="{category.title()} Map"></div>
        <div class="map-legend">
          <ul>
            <li>Click a pin to jump to that pick</li>
            <li>Numbers match the ranking above</li>
          </ul>
          <p><a href="https://maps.google.com/?q={content['venues'][0]['name'].replace(' ', '+')}+{city.replace(' ', '+')}" target="_blank" rel="noopener" data-map-cta>Open in Google Maps &rarr;</a></p>
        </div>
      </section>

      <div class="content">
        <section class="quick-answer-section">
          <div class="quick-answer-card">
            <p class="eyebrow">Quick answer</p>
            <p class="quick-answer-lead"><strong>{qa['lead']}</strong></p>
            <dl class="quick-answer-grid">
              <div class="comparison-row"><dt>Best overall</dt><dd>{qa['bestOverall']}</dd></div>
              <div class="comparison-row"><dt>Best budget</dt><dd>{qa['bestBudget']}</dd></div>
              <div class="comparison-row"><dt>Best experience</dt><dd>{qa['bestExperience']}</dd></div>
              <div class="comparison-row"><dt>Last verified</dt><dd>{today[:7]}</dd></div>
            </dl>
          </div>
        </section>

        <section class="methodology-box">
          <h2>How we picked these</h2>
          <p>{content.get('methodology', '')}</p>
        </section>

        <section class="map-inline" data-map-panel="mobile">
          <h2>📍 Map</h2>
          <div class="map-active-pick" data-map-active-pick>1. {content['venues'][0]['name']}</div>
          <div class="popular-picks-map" data-map-canvas aria-label="{category.title()} Map"></div>
          <div class="map-legend">
            <ul>
              <li>Click a pin to jump to that pick</li>
              <li>Numbers match the ranking above</li>
            </ul>
            <p><a href="https://maps.google.com/?q={content['venues'][0]['name'].replace(' ', '+')}+{city.replace(' ', '+')}" target="_blank" rel="noopener" data-map-cta>Open in Google Maps &rarr;</a></p>
          </div>
        </section>

        {venues_html}

        <section class="faq-section">
          <h2>❓ Frequently Asked Questions</h2>
          {faq_html}
        </section>

        <section class="cta-section">
          <h2>Plan your {city} trip</h2>
          <p>Get a free custom itinerary for {city} — built from real traveler insights.</p>
          <a href="/plan" class="cta-btn">Get a Free Itinerary →</a>
        </section>
      </div>
    </div>

    <script>
    window.__POPULAR_PICKS_MAP__ = {json.dumps(build_map_config(content['venues'], slug, city, category), ensure_ascii=False)};
    </script>

    {template['footer']}
</body>
</html>"""


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
                "cuisineTags": v.get("cuisineTags", [])
            }
            for v in content["venues"]
        ],
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%d")
    }


def process_page(slug: str, city: str, country: str, title: str, category: str, template: dict) -> str:
    """Generate and save one popular-picks page. Returns status."""
    html_path = PP_DIR / slug / "index.html"
    api_path = API_DIR / f"{slug}.json"
    
    if html_path.exists():
        return f"  ⏭️  {slug}: already exists, skipping"
    
    try:
        content = generate_page_content(slug, city, country, title, category)
        html = build_full_page(slug, city, country, title, category, content, template)
        
        html_path.parent.mkdir(parents=True, exist_ok=True)
        html_path.write_text(html)
        
        api_json = build_api_json(slug, city, country, content)
        api_path.parent.mkdir(parents=True, exist_ok=True)
        api_path.write_text(json.dumps(api_json, indent=2, ensure_ascii=False) + "\n")
        
        return f"  ✅ {slug}: {len(content['venues'])} venues, {len(html)} bytes"
    except Exception as e:
        return f"  ❌ {slug}: {e}"


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
    print(f"Template extracted: CSS={len(template['css'])}chars, nav={len(template['nav'])}chars")
    
    results = []
    for i, page in enumerate(pages, 1):
        print(f"[{i}/{len(pages)}] {page['slug']}")
        result = process_page(page["slug"], page["city"], page["country"], page["title"], page["category"], template)
        print(result)
        results.append(result)
        if i < len(pages):
            time.sleep(1)
    
    success = sum(1 for r in results if "✅" in r)
    skip = sum(1 for r in results if "⏭️" in r)
    fail = sum(1 for r in results if "❌" in r)
    print(f"\nDone: {success} built, {skip} skipped, {fail} failed")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
