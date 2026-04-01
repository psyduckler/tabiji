#!/usr/bin/env python3
"""
Link ALL popular-picks pages to their country hub JSON + regenerate HTML.
"""

import json
import os
import glob
import re
import html
from collections import defaultdict
from pathlib import Path

TABIJI = os.path.expanduser("~/tabiji")
PP_DIR = os.path.join(TABIJI, "popular-picks")
HUB_DATA_DIR = os.path.join(TABIJI, "popular-picks-hub-data")
PICKS_API_DIR = os.path.join(TABIJI, "api/v1/picks")
DEST_API_DIR = os.path.join(TABIJI, "api/v1/destinations")

# Country code to flag emoji
COUNTRY_FLAGS = {}
# Country name to slug mapping
COUNTRY_SLUG_MAP = {
    "United States": "usa",
    "United States of America": "usa",
    "US": "usa",
    "USA": "usa",
    "United Kingdom": "united-kingdom",
    "UK": "united-kingdom",
    "South Korea": "south-korea",
    "Republic of Korea": "south-korea",
    "South Africa": "south-africa",
    "Czech Republic": "czech-republic",
    "Czechia": "czech-republic",
    "Hong Kong": "hong-kong",
    "UAE": "uae",
    "United Arab Emirates": "uae",
    "New Zealand": "new-zealand",
    "Sri Lanka": "sri-lanka",
    "Costa Rica": "costa-rica",
    "Puerto Rico": "puerto-rico",
    "Dominican Republic": "dominican-republic",
    "Saudi Arabia": "saudi-arabia",
    "Trinidad and Tobago": "trinidad-and-tobago",
}

# Country code -> flag emoji
CC_TO_FLAG = {}

def country_code_to_flag(cc):
    """Convert 2-letter country code to flag emoji."""
    if not cc or len(cc) != 2:
        return ""
    return chr(0x1F1E6 + ord(cc[0].upper()) - ord('A')) + chr(0x1F1E6 + ord(cc[1].upper()) - ord('A'))

def country_to_slug(country_name):
    """Convert country name to URL slug."""
    if country_name in COUNTRY_SLUG_MAP:
        return COUNTRY_SLUG_MAP[country_name]
    return re.sub(r'[^a-z0-9]+', '-', country_name.lower()).strip('-')

def load_destination_country_map():
    """Build city_slug -> (country_name, country_code) from destinations API."""
    city_to_country = {}
    for f in glob.glob(os.path.join(DEST_API_DIR, "*.json")):
        try:
            data = json.load(open(f))
            slug = os.path.basename(f).replace('.json', '')
            country = data.get('country', '')
            cc = data.get('countryCode', '')
            if country:
                city_to_country[slug] = (country, cc)
        except:
            pass
    return city_to_country

def extract_city_from_slug(slug):
    """Extract likely city name from a picks slug like 'tokyo-ramen' -> 'tokyo'."""
    # Try progressively longer prefixes
    parts = slug.split('-')
    candidates = []
    for i in range(1, len(parts)):
        candidates.append('-'.join(parts[:i]))
    return candidates

def get_pick_data(slug):
    """Get pick data from API JSON."""
    api_file = os.path.join(PICKS_API_DIR, f"{slug}.json")
    if os.path.exists(api_file):
        try:
            return json.load(open(api_file))
        except:
            pass
    return None

def extract_title_from_html(slug):
    """Fallback: extract title from HTML page."""
    html_file = os.path.join(PP_DIR, slug, "index.html")
    if os.path.exists(html_file):
        try:
            content = open(html_file).read(5000)
            m = re.search(r'<title>(.*?)</title>', content)
            if m:
                title = m.group(1).replace(' — tabiji.ai', '').strip()
                return title
        except:
            pass
    return slug.replace('-', ' ').title()

def extract_description_from_html(slug):
    """Fallback: extract meta description from HTML page."""
    html_file = os.path.join(PP_DIR, slug, "index.html")
    if os.path.exists(html_file):
        try:
            content = open(html_file).read(5000)
            m = re.search(r'<meta\s+name="description"\s+content="(.*?)"', content)
            if m:
                return m.group(1)[:150]
        except:
            pass
    return ""

def build_card(slug, pick_data):
    """Build a card dict for the hub JSON."""
    if pick_data:
        title = pick_data.get('title', extract_title_from_html(slug))
        desc = pick_data.get('description', '')[:150]
        if desc and not desc.endswith('...'):
            desc = desc[:147] + '...'
        image = pick_data.get('heroImage', '')
        place_count = pick_data.get('placeCount', 0)
        dest_name = pick_data.get('destinationName', '')
    else:
        title = extract_title_from_html(slug)
        desc = extract_description_from_html(slug)
        image = ''
        place_count = 0
        dest_name = ''
    
    card = {
        "slug": slug,
        "href": f"/popular-picks/{slug}/",
        "title": title,
        "description": desc,
        "badge": f"📍 {dest_name}" if dest_name else "",
        "meta": [],
        "image": image,
        "imageAlt": title
    }
    
    if place_count:
        card["meta"].append(f"🍽️ {place_count} spots")
    card["meta"].append("🗺️ Interactive Map")
    
    return card

def get_existing_hub_data():
    """Load all existing hub JSONs."""
    hubs = {}
    for f in glob.glob(os.path.join(HUB_DATA_DIR, "*.json")):
        slug = os.path.basename(f).replace('.json', '')
        try:
            hubs[slug] = json.load(open(f))
        except:
            pass
    return hubs

def get_linked_slugs(hubs):
    """Get set of all slugs already linked in hubs."""
    linked = set()
    for hub in hubs.values():
        for sec in hub.get('sections', []):
            for card in sec.get('cards', []):
                linked.add(card['slug'])
    return linked

def create_new_hub_json(country_slug, country_name, country_code, sections_dict):
    """Create a new hub JSON for a country."""
    flag = country_code_to_flag(country_code) if country_code else ""
    label = f"{flag} {country_name}" if flag else country_name
    
    # Sort cities
    sorted_cities = sorted(sections_dict.keys())
    
    # Build sections
    sections = []
    for city in sorted_cities:
        cards = sections_dict[city]
        city_id = re.sub(r'[^a-z0-9]+', '-', city.lower()).strip('-')
        sections.append({
            "id": city_id,
            "title": city.title() if city == city.lower() else city,
            "cards": cards
        })
    
    # Pick hero image from first card that has one
    hero_image = ""
    for sec in sections:
        for card in sec["cards"]:
            if card.get("image"):
                hero_image = card["image"]
                break
        if hero_image:
            break
    
    # Build TOC
    toc = [{"id": sec["id"], "label": sec["title"]} for sec in sections]
    
    total_cards = sum(len(s["cards"]) for s in sections)
    
    hub = {
        "slug": country_slug,
        "pageType": "popular-picks-hub",
        "status": "published",
        "taxonomy": {
            "scope": "country-or-region-hub",
            "label": label
        },
        "seo": {
            "title": f"{label} Popular Picks",
            "h1": label,
            "metaTitle": f"{label} Popular Picks — tabiji.ai",
            "metaDescription": f"Curated lists of the best restaurants, bars, cafés, and experiences in {country_name} — researched from thousands of real Reddit reviews.",
            "canonicalPath": f"/popular-picks/{country_slug}/",
            "ogTitle": f"Popular Picks in {country_name} — tabiji.ai",
            "ogDescription": f"Reddit-backed curated lists for {country_name}. No sponsored picks, no fluff.",
            "twitterTitle": "",
            "twitterDescription": "",
            "heroImage": hero_image,
            "publishedTime": None,
            "modifiedTime": None,
            "robots": "index, follow, max-image-preview:large"
        },
        "hero": {
            "title": label,
            "dek": f"Reddit-backed guides to the best food, restaurants, and experiences across {country_name}.",
            "backLink": "/popular-picks/",
            "meta": []
        },
        "toc": toc,
        "sections": sections,
        "faq": [
            {
                "q": f"What kinds of popular picks are included in {label}?",
                "a": f"{label} groups together Reddit-backed lists for its strongest food and travel categories, with {total_cards} curated guides across {len(sections)} cities. Each card links to a deeper guide with specific places, context, and map support."
            },
            {
                "q": f"How are Tabiji's {label} picks chosen?",
                "a": f"These picks are built from real traveler discussion patterns, then organized into curated shortlists rather than paid placements or generic roundups. The goal is to surface the places and experiences people repeatedly mention when planning trips to {label}."
            },
            {
                "q": f"Should I start with the hub page or open the individual guides for {label}?",
                "a": f"Use the hub page to decide which city or category fits what you want, then open the individual guides for ranked picks, more detailed context, and map links. The hub is the shortlist; the leaf guides are where the decision-making detail lives."
            }
        ],
        "provenance": {
            "generator": "link-all-picks-to-hubs.py",
            "version": "1.0"
        },
        "publishing": {
            "lastBuilt": None
        }
    }
    return hub

def render_hub_html(hub_data):
    """Render hub JSON to HTML page."""
    d = hub_data
    seo = d["seo"]
    hero = d["hero"]
    label = d["taxonomy"]["label"]
    country_slug = d["slug"]
    
    # Escape for HTML attributes
    def esc(s):
        return html.escape(str(s), quote=True) if s else ""
    
    # Build TOC HTML
    toc_items = ""
    for t in d.get("toc", []):
        toc_items += f'<li><a href="#{esc(t["id"])}">{esc(t["label"])}</a></li>'
    
    first_toc_label = d["toc"][0]["label"] if d.get("toc") else "Sections"
    
    # Build sections HTML
    sections_html = ""
    for sec in d.get("sections", []):
        cards_html = ""
        for card in sec.get("cards", []):
            img_html = ""
            if card.get("image"):
                img_html = f'<img src="{esc(card["image"])}" alt="{esc(card["imageAlt"])}" loading="lazy">'
            
            badge_html = ""
            if card.get("badge"):
                badge_html = f'<span class="card-badge">{esc(card["badge"])}</span>'
            
            meta_html = ""
            for m in card.get("meta", []):
                meta_html += f"<span>{esc(m)}</span>"
            
            cards_html += f'''
<a href="{esc(card["href"])}" class="pick-card">
  {img_html}
  <div class="pick-card-body">
    {badge_html}
    <h3>{esc(card["title"])}</h3>
    <p>{esc(card.get("description", ""))}</p>
    <div class="card-meta">{meta_html}</div>
  </div>
</a>'''
        
        sections_html += f'''
<section class="city-section" id="{esc(sec["id"])}">
  <h2>{esc(sec["title"])}</h2>
  <div class="picks-grid">
    {cards_html}
  </div>
</section>'''
    
    # Build FAQ HTML
    faq_html = ""
    faq_schema_items = []
    for faq in d.get("faq", []):
        q = faq.get("q", "")
        a = faq.get("a", "")
        faq_html += f'<details class="faq-item"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
        faq_schema_items.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    
    # Schema JSON-LD
    article_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": label,
        "description": seo.get("metaDescription", ""),
        "author": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai"},
        "publisher": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai"},
        "mainEntityOfPage": f"https://tabiji.ai/popular-picks/{country_slug}/",
        "image": seo.get("heroImage", "")
    }, indent=2)
    
    breadcrumb_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tabiji.ai/"},
            {"@type": "ListItem", "position": 2, "name": "Popular Picks", "item": "https://tabiji.ai/popular-picks/"},
            {"@type": "ListItem", "position": 3, "name": label, "item": f"https://tabiji.ai/popular-picks/{country_slug}/"}
        ]
    }, indent=2)
    
    faq_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_schema_items
    }, indent=2)
    
    hero_img = seo.get("heroImage", "")
    hero_img_tag = f'<figure class="hero-figure"><img src="{esc(hero_img)}" alt="{esc(label)}" loading="eager"></figure>' if hero_img else ""
    
    page_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-D7QHNRXLHJ"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}} gtag('js', new Date()); gtag('config', 'G-D7QHNRXLHJ');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="https://img.tabiji.ai/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="192x192" href="https://img.tabiji.ai/icon-192.png">
    <title>{esc(seo.get("metaTitle", ""))}</title>
    <meta name="description" content="{esc(seo.get("metaDescription", ""))}">
    <meta name="robots" content="{esc(seo.get("robots", "index, follow, max-image-preview:large"))}">
    <link rel="canonical" href="https://tabiji.ai/popular-picks/{country_slug}/">
    <meta property="og:title" content="{esc(seo.get("ogTitle", ""))}">
    <meta property="og:description" content="{esc(seo.get("ogDescription", ""))}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://tabiji.ai/popular-picks/{country_slug}/">
    <meta property="og:image" content="{esc(hero_img)}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="675">
    <meta property="og:site_name" content="tabiji.ai">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{esc(seo.get("metaTitle", ""))}">
    <meta name="twitter:description" content="{esc(seo.get("ogDescription", ""))}">
    <meta name="twitter:image" content="{esc(hero_img)}">
    <script type="application/ld+json">{article_schema}</script>
    <script type="application/ld+json">{breadcrumb_schema}</script>
    <script type="application/ld+json">{faq_schema}</script>
    <style>
      :root {{ --indigo:#2D3A5C; --warm-cream:#F5F0E8; --sand:#E8DFD0; --earth:#8B7355; --terracotta:#C4704B; --white:#FEFCF9; --text:#2C2419; --text-muted:#6B5D4F; }}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      body {{ font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif; color:var(--text); background:var(--white); line-height:1.6; }}
      a {{ color:inherit; text-decoration:none; }}
      nav {{ position:sticky; top:0; z-index:100; background:rgba(254,252,249,.92); backdrop-filter:blur(20px); border-bottom:1px solid var(--sand); padding:1rem 1.5rem; display:flex; justify-content:space-between; align-items:center; }}
      .logo {{ font-size:1.3rem; font-weight:700; color:var(--indigo); }}
      .cta-nav {{ background:var(--terracotta); color:white; padding:.55rem 1rem; border-radius:8px; }}
      .hero {{ padding:7rem 1.5rem 2rem; max-width:1080px; margin:0 auto; }}
      .back-link {{ display:inline-block; margin-bottom:1rem; color:var(--earth); }}
      .hero h1 {{ font-size:clamp(2rem,4.7vw,3rem); line-height:1.12; color:var(--indigo); margin-bottom:1rem; }}
      .hero p {{ color:var(--text-muted); max-width:780px; }}
      .hero-meta {{ display:flex; gap:1rem 1.5rem; flex-wrap:wrap; margin-top:1rem; color:var(--earth); font-size:.95rem; }}
      .hero-figure {{ margin-top:1.5rem; border:1px solid var(--sand); border-radius:18px; overflow:hidden; background:var(--warm-cream); }}
      .hero-figure img {{ width:100%; height:min(46vw,420px); min-height:220px; object-fit:cover; display:block; }}
      .hero-caption {{ padding:.85rem 1rem; color:var(--text-muted); font-size:.92rem; border-top:1px solid var(--sand); background:rgba(245,240,232,.65); }}
      .toc-sidebar {{ position:sticky; top:90px; align-self:start; width:220px; border-right:1px solid var(--sand); padding-right:1rem; }}
      .toc-sidebar h2 {{ font-size:1rem; margin-bottom:.8rem; color:var(--indigo); }}
      .toc-sidebar ul {{ list-style:none; }}
      .toc-sidebar li {{ margin-bottom:.4rem; }}
      .toc-sidebar a {{ color:var(--text-muted); }}
      .toc-sidebar a:hover, .toc-sidebar a.active {{ color:var(--terracotta); font-weight:600; }}
      .toc-mobile-sticky {{ display:none; position:sticky; top:73px; z-index:90; background:var(--white); border-bottom:1px solid var(--sand); padding:.75rem 1rem; }}
      .toc-mobile-toggle {{ width:100%; background:var(--warm-cream); border:1px solid var(--sand); border-radius:10px; padding:.85rem 1rem; display:flex; justify-content:space-between; align-items:center; font-size:1rem; }}
      .toc-mobile-dropdown {{ max-height:0; overflow:hidden; transition:max-height .2s ease; }}
      .toc-mobile-sticky.open .toc-mobile-dropdown {{ max-height:60vh; overflow-y:auto; }}
      .toc-mobile-dropdown ul {{ list-style:none; padding-top:.6rem; }}
      .toc-mobile-dropdown li {{ margin-bottom:.3rem; }}
      .content-wrapper {{ max-width:1200px; margin:0 auto; display:grid; grid-template-columns:220px minmax(0,1fr); gap:2rem; padding:0 1.5rem 4rem; }}
      .main-content {{ min-width:0; }}
      .city-section {{ margin-bottom:3rem; }}
      .city-section h2 {{ font-size:1.75rem; color:var(--indigo); margin-bottom:1rem; }}
      .picks-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:1.25rem; }}
      @media (max-width:900px) {{ .picks-grid {{ grid-template-columns:repeat(2,1fr); }} }}
      @media (max-width:560px) {{ .picks-grid {{ grid-template-columns:1fr; }} }}
      .pick-card {{ background:#FEFCF9; border:1px solid var(--sand); border-radius:14px; overflow:hidden; display:block; transition:transform .15s, box-shadow .15s; }}
      .pick-card:hover {{ transform:translateY(-3px); box-shadow:0 8px 30px rgba(0,0,0,.08); }}
      .pick-card img {{ width:100%; height:180px; object-fit:cover; display:block; }}
      .pick-card-body {{ padding:1rem; }}
      .card-badge {{ display:inline-block; font-size:.82rem; color:var(--earth); margin-bottom:.55rem; }}
      .pick-card h3 {{ font-size:1.12rem; color:var(--indigo); margin-bottom:.5rem; }}
      .pick-card p {{ font-size:.95rem; color:var(--text-muted); margin-bottom:.8rem; }}
      .card-meta {{ display:flex; gap:.75rem; flex-wrap:wrap; color:var(--earth); font-size:.86rem; }}
      .faq-section {{ max-width:1200px; margin:0 auto; padding:0 1.5rem 4rem; }}
      .faq-section h2 {{ color:var(--indigo); margin-bottom:1rem; }}
      .faq-item {{ border-top:1px solid var(--sand); padding:.9rem 0; }}
      .faq-item summary {{ cursor:pointer; font-weight:700; color:var(--indigo); }}
      footer {{ max-width:1200px; margin:0 auto; padding:0 1.5rem 3rem; color:var(--text-muted); }}
      @media (max-width: 900px) {{
        .toc-sidebar {{ display:none; }}
        .toc-mobile-sticky {{ display:block; }}
        .content-wrapper {{ grid-template-columns:1fr; }}
      }}
    </style>
</head>
<body>
  <nav>
    <a class="logo" href="/">tabiji.ai</a>
    <a class="cta-nav" href="/plan">Get a Free Itinerary</a>
  </nav>

  <section class="hero">
    <a href="/popular-picks/" class="back-link">← All Popular Picks</a>
    <h1>{esc(label)}</h1>
    <p>{esc(hero.get("dek", ""))}</p>
    
    {hero_img_tag}
  </section>

  
<div class="toc-mobile-sticky" id="toc-mobile">
  <button class="toc-mobile-toggle" onclick="this.parentElement.classList.toggle('open')">
    <span class="toc-active-label" id="toc-active-label">{esc(first_toc_label)}</span>
    <span class="toc-chevron">▼</span>
  </button>
  <div class="toc-mobile-dropdown"><ul>{toc_items}</ul></div>
</div>

<div class="content-wrapper">
  <aside class="toc-sidebar">
    <h2>Sections</h2>
    <ul>{toc_items}</ul>
  </aside>
    <div class="main-content">
      {sections_html}
    </div>
  </div>

  
<section class="faq-section">
  <h2>Frequently Asked Questions</h2>
  {faq_html}
</section>

  <footer>Generated from structured hub source data.</footer>

  <script>
  const sections = document.querySelectorAll('.city-section');
  const tocLinks = document.querySelectorAll('.toc-sidebar a, .toc-mobile-dropdown a');
  const mobileLabel = document.getElementById('toc-active-label');
  const observer = new IntersectionObserver(entries => {{
    entries.forEach(entry => {{
      if (entry.isIntersecting) {{
        const id = entry.target.id;
        tocLinks.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + id));
        if (mobileLabel) mobileLabel.textContent = entry.target.querySelector('h2')?.textContent || 'Sections';
      }}
    }});
  }}, {{ rootMargin: '-80px 0px -60% 0px', threshold: 0 }});
  sections.forEach(s => observer.observe(s));
  document.querySelectorAll('.toc-mobile-dropdown a').forEach(a => {{
    a.addEventListener('click', () => document.getElementById('toc-mobile').classList.remove('open'));
  }});
  </script>
</body>
</html>'''
    
    return page_html

def main():
    print("=== Link All Popular Picks to Country Hubs ===\n")
    
    # Step 1: Load destination -> country mapping
    print("Loading destination->country map...")
    city_to_country = load_destination_country_map()
    print(f"  {len(city_to_country)} destinations with country info")
    
    # Step 2: Get all popular-picks slugs
    all_slugs = sorted([d for d in os.listdir(PP_DIR) 
                       if os.path.isdir(os.path.join(PP_DIR, d)) 
                       and os.path.exists(os.path.join(PP_DIR, d, "index.html"))
                       and d not in ('japan', 'usa', 'france', 'italy', 'spain', 'germany', 
                                     'thailand', 'vietnam', 'mexico', 'india', 'south-korea',
                                     'united-kingdom', 'greece', 'turkey', 'portugal',
                                     'indonesia', 'morocco', 'peru', 'colombia', 'argentina',
                                     'egypt', 'kenya', 'tanzania', 'south-africa', 'ghana',
                                     'ethiopia', 'rwanda', 'senegal', 'madagascar', 'namibia',
                                     'botswana', 'mauritius', 'jamaica', 'cambodia', 'laos',
                                     'myanmar', 'malaysia', 'singapore', 'philippines', 'taiwan',
                                     'hong-kong', 'israel', 'jordan', 'croatia', 'hungary',
                                     'czech-republic', 'austria', 'belgium', 'netherlands',
                                     'sweden', 'denmark')])
    
    # Actually, let's just exclude directories that ARE country hub pages
    # A country hub page has no picks data — check if the dir is a country slug
    existing_hubs = get_existing_hub_data()
    hub_slugs = set(existing_hubs.keys())
    
    # Get ALL dirs including potential country dirs, but filter out country hub dirs
    all_dirs = sorted([d for d in os.listdir(PP_DIR) 
                      if os.path.isdir(os.path.join(PP_DIR, d))
                      and os.path.exists(os.path.join(PP_DIR, d, "index.html"))])
    
    # Separate: country hub pages vs actual picks pages
    # A picks page has a corresponding API JSON or its slug contains a city name
    picks_slugs = []
    country_hub_dirs = []
    for d in all_dirs:
        if d in hub_slugs:
            country_hub_dirs.append(d)
        else:
            picks_slugs.append(d)
    
    print(f"  {len(all_dirs)} total dirs, {len(country_hub_dirs)} are country hub dirs, {len(picks_slugs)} are picks pages")
    
    # Step 3: Get currently linked slugs
    linked_slugs = get_linked_slugs(existing_hubs)
    print(f"  {len(linked_slugs)} picks already linked in hubs")
    
    unlinked = [s for s in picks_slugs if s not in linked_slugs]
    print(f"  {len(unlinked)} picks NOT yet linked\n")
    
    # Step 4: Map each unlinked slug to a country
    slug_to_country = {}  # slug -> (country_name, country_code, city_name)
    unmapped = []
    
    for slug in picks_slugs:
        # Try to find country via API JSON destinationSlug -> destinations API
        pick_data = get_pick_data(slug)
        dest_slug = pick_data.get('destinationSlug', '') if pick_data else ''
        dest_name = pick_data.get('destinationName', '') if pick_data else ''
        
        country_found = False
        
        if dest_slug and dest_slug in city_to_country:
            country_name, cc = city_to_country[dest_slug]
            slug_to_country[slug] = (country_name, cc, dest_name or dest_slug)
            country_found = True
        
        if not country_found:
            # Try extracting city from slug
            candidates = extract_city_from_slug(slug)
            for c in reversed(candidates):  # try longest first
                if c in city_to_country:
                    country_name, cc = city_to_country[c]
                    slug_to_country[slug] = (country_name, cc, c)
                    country_found = True
                    break
        
        if not country_found:
            unmapped.append(slug)
    
    print(f"  Mapped {len(slug_to_country)} picks to countries")
    if unmapped:
        print(f"  ⚠️  {len(unmapped)} picks could not be mapped to a country:")
        for s in unmapped[:20]:
            print(f"      {s}")
        if len(unmapped) > 20:
            print(f"      ... and {len(unmapped) - 20} more")
    
    # Step 5: Group unlinked picks by country
    country_additions = defaultdict(lambda: defaultdict(list))  # country_slug -> city_name -> [cards]
    
    for slug in unlinked:
        if slug not in slug_to_country:
            continue
        country_name, cc, city_name = slug_to_country[slug]
        country_slug = country_to_slug(country_name)
        pick_data = get_pick_data(slug)
        card = build_card(slug, pick_data)
        
        # Use the city_name for the section title
        display_city = city_name.replace('-', ' ').title() if city_name == city_name.lower() else city_name
        # Fix the badge
        card["badge"] = f"📍 {display_city}"
        
        country_additions[country_slug][display_city].append(card)
    
    print(f"\n  Countries needing updates: {len(country_additions)}")
    
    # Step 6: Update existing hubs and create new ones
    created_hubs = 0
    updated_hubs = 0
    total_added = 0
    
    # Also need to include already-linked picks for context when building
    # Group ALL picks by country (not just unlinked)
    all_by_country = defaultdict(lambda: defaultdict(list))
    for slug in picks_slugs:
        if slug not in slug_to_country:
            continue
        country_name, cc, city_name = slug_to_country[slug]
        cs = country_to_slug(country_name)
        display_city = city_name.replace('-', ' ').title() if city_name == city_name.lower() else city_name
        all_by_country[cs][display_city].append(slug)
    
    for country_slug, city_cards in country_additions.items():
        added_count = sum(len(cards) for cards in city_cards.values())
        
        if country_slug in existing_hubs:
            # Update existing hub
            hub = existing_hubs[country_slug]
            existing_section_ids = {sec["id"]: sec for sec in hub["sections"]}
            
            for city_name, cards in city_cards.items():
                city_id = re.sub(r'[^a-z0-9]+', '-', city_name.lower()).strip('-')
                
                if city_id in existing_section_ids:
                    # Add cards to existing section
                    existing_slugs_in_section = {c["slug"] for c in existing_section_ids[city_id]["cards"]}
                    for card in cards:
                        if card["slug"] not in existing_slugs_in_section:
                            existing_section_ids[city_id]["cards"].append(card)
                else:
                    # New city section
                    new_section = {
                        "id": city_id,
                        "title": city_name,
                        "cards": cards
                    }
                    hub["sections"].append(new_section)
                    hub["toc"].append({"id": city_id, "label": city_name})
            
            # Sort sections alphabetically
            hub["sections"].sort(key=lambda s: s["id"])
            hub["toc"].sort(key=lambda t: t["id"])
            
            # Update FAQ with new count
            total_cards = sum(len(s["cards"]) for s in hub["sections"])
            total_sections = len(hub["sections"])
            label = hub["taxonomy"]["label"]
            hub["faq"] = [
                {
                    "q": f"What kinds of popular picks are included in {label}?",
                    "a": f"{label} groups together Reddit-backed lists for its strongest food and travel categories, with {total_cards} curated guides across {total_sections} cities. Each card links to a deeper guide with specific places, context, and map support."
                },
                {
                    "q": f"How are Tabiji's {label} picks chosen?",
                    "a": f"These picks are built from real traveler discussion patterns, then organized into curated shortlists rather than paid placements or generic roundups. The goal is to surface the places and experiences people repeatedly mention when planning trips to {label}."
                },
                {
                    "q": f"Should I start with the hub page or open the individual guides for {label}?",
                    "a": f"Use the hub page to decide which city or category fits what you want, then open the individual guides for ranked picks, more detailed context, and map links. The hub is the shortlist; the leaf guides are where the decision-making detail lives."
                }
            ]
            
            updated_hubs += 1
        else:
            # Create new hub
            # Find the country info
            sample_slug = list(city_cards.values())[0][0]["slug"]
            if sample_slug in slug_to_country:
                country_name, cc, _ = slug_to_country[sample_slug]
            else:
                country_name = country_slug.replace('-', ' ').title()
                cc = ""
            
            hub = create_new_hub_json(country_slug, country_name, cc, city_cards)
            existing_hubs[country_slug] = hub
            created_hubs += 1
        
        total_added += added_count
        
        # Save hub JSON
        hub_file = os.path.join(HUB_DATA_DIR, f"{country_slug}.json")
        with open(hub_file, 'w') as f:
            json.dump(existing_hubs[country_slug], f, indent=2, ensure_ascii=False)
    
    print(f"\n  Updated {updated_hubs} existing hubs")
    print(f"  Created {created_hubs} new hubs")
    print(f"  Added {total_added} new pick links total")
    
    # Step 7: Regenerate ALL hub HTML pages (including unchanged ones for consistency)
    print(f"\nRegenerating HTML for all {len(existing_hubs)} hubs...")
    for country_slug, hub_data in existing_hubs.items():
        html_dir = os.path.join(PP_DIR, country_slug)
        os.makedirs(html_dir, exist_ok=True)
        html_file = os.path.join(html_dir, "index.html")
        page_html = render_hub_html(hub_data)
        with open(html_file, 'w') as f:
            f.write(page_html)
    print("  Done!")
    
    # Print summary of new country hubs
    if created_hubs > 0:
        new_hubs = [cs for cs in country_additions if cs not in hub_slugs]
        print(f"\n  New country hubs created:")
        for cs in sorted(new_hubs):
            card_count = sum(len(cards) for cards in country_additions[cs].values())
            print(f"    {cs}: {card_count} picks")
    
    # Print unmapped summary
    if unmapped:
        print(f"\n  ⚠️  {len(unmapped)} picks remain unmapped (no country found)")
    
    print(f"\n=== SUMMARY ===")
    print(f"Total picks pages: {len(picks_slugs)}")
    print(f"Previously linked: {len(linked_slugs)}")
    print(f"Newly linked: {total_added}")
    print(f"Still unmapped: {len(unmapped)}")
    print(f"Hubs updated: {updated_hubs}")
    print(f"Hubs created: {created_hubs}")
    print(f"Total hubs: {len(existing_hubs)}")

if __name__ == "__main__":
    main()
