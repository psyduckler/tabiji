#!/usr/bin/env python3
"""Build destination hub pages for cities with enough content.

Each hub page aggregates:
- Popular picks for that city
- Compare pages featuring that city
- Alert pages if they exist
- CTA to plan a trip
- Email capture
"""

import os
import glob
import re
from collections import defaultdict

BASE_DIR = os.path.expanduser("~/tabiji")
DEST_DIR = os.path.join(BASE_DIR, "destinations")

MULTI = {
    "abu-dhabi", "buenos-aires", "cape-town", "chiang-mai", "dar-es-salaam",
    "hong-kong", "ho-chi-minh", "kuala-lumpur", "las-vegas", "los-angeles",
    "mexico-city", "new-orleans", "new-york", "playa-del-carmen", "rio-de-janeiro",
    "san-francisco", "san-sebastian", "santa-fe", "siem-reap", "sri-lanka",
    "st-petersburg", "tel-aviv", "la-paz", "el-nido", "addis-ababa",
    "koh-samui", "koh-phangan", "koh-lipe", "phu-quoc", "puerto-vallarta",
    "nusa-penida", "da-nang", "hoi-an", "port-louis", "sharm-el-sheikh",
    "mar-del-plata", "punta-cana", "costa-rica", "ras-al-khaimah", "puerto-rico",
}

def city_slug(d):
    for s in sorted(MULTI, key=lambda x: -len(x)):
        if d.startswith(s + "-") or d == s:
            return s
    return d.split("-")[0]

def slug_to_title(slug):
    special = {
        "abu-dhabi": "Abu Dhabi", "buenos-aires": "Buenos Aires",
        "cape-town": "Cape Town", "chiang-mai": "Chiang Mai",
        "hong-kong": "Hong Kong", "ho-chi-minh": "Ho Chi Minh City",
        "kuala-lumpur": "Kuala Lumpur", "las-vegas": "Las Vegas",
        "los-angeles": "Los Angeles", "mexico-city": "Mexico City",
        "new-orleans": "New Orleans", "new-york": "New York",
        "rio-de-janeiro": "Rio de Janeiro", "san-francisco": "San Francisco",
        "tel-aviv": "Tel Aviv", "da-nang": "Da Nang", "hoi-an": "Hoi An",
        "chengdu": "Chengdu", "koh-samui": "Koh Samui",
        "koh-phangan": "Koh Phangan", "phu-quoc": "Phu Quoc",
        "puerto-vallarta": "Puerto Vallarta", "addis-ababa": "Addis Ababa",
        "ras-al-khaimah": "Ras Al Khaimah", "st-petersburg": "St. Petersburg",
        "playa-del-carmen": "Playa del Carmen", "mar-del-plata": "Mar del Plata",
        "punta-cana": "Punta Cana", "nusa-penida": "Nusa Penida",
        "sharm-el-sheikh": "Sharm El Sheikh",
    }
    return special.get(slug, slug.replace("-", " ").title())

# Build indices
cities_picks = defaultdict(list)
for p in glob.glob(os.path.join(BASE_DIR, "popular-picks/*/index.html")):
    d = os.path.basename(os.path.dirname(p))
    cs = city_slug(d)
    cat = d[len(cs) + 1:] if d.startswith(cs + "-") else ""
    if cat:
        cities_picks[cs].append((d, cat))

cities_compares = defaultdict(list)
for p in glob.glob(os.path.join(BASE_DIR, "compare/*/index.html")):
    d = os.path.basename(os.path.dirname(p))
    if "-vs-" in d:
        parts = d.split("-vs-")
        for part in parts:
            cities_compares[part].append(d)

cities_alerts = defaultdict(list)
for p in glob.glob(os.path.join(BASE_DIR, "alerts/*/index.html")):
    d = os.path.basename(os.path.dirname(p))
    cs = city_slug(d)
    cities_alerts[cs].append(d)

cities_scams = defaultdict(list)
for p in glob.glob(os.path.join(BASE_DIR, "scams/*/index.html")):
    d = os.path.basename(os.path.dirname(p))
    cs = city_slug(d)
    cities_scams[cs].append(d)

# Existing destination pages
existing = set()
for d in os.listdir(DEST_DIR):
    if os.path.isdir(os.path.join(DEST_DIR, d)):
        existing.add(d)

# Build hub pages for cities with >= 5 picks
created = 0
updated = 0

for city, picks in sorted(cities_picks.items(), key=lambda x: -len(x[1])):
    if len(picks) < 5:
        continue
    
    city_name = slug_to_title(city)
    compares = cities_compares.get(city, [])[:8]
    alerts = cities_alerts.get(city, [])
    scams = cities_scams.get(city, [])
    
    # Build picks grid HTML
    picks_html = ""
    for slug, cat in sorted(picks, key=lambda x: x[1]):
        cat_title = cat.replace("-", " ").title()
        picks_html += f'      <a class="hub-card" href="/popular-picks/{slug}/"><span class="hub-card-title">{cat_title}</span></a>\n'
    
    # Build compares HTML
    compares_html = ""
    if compares:
        compares_html = '    <section class="hub-section">\n      <h2>🆚 Compare Destinations</h2>\n      <div class="hub-grid">\n'
        for comp in compares:
            comp_title = comp.replace("-", " ").replace(" vs ", " vs ").title()
            compares_html += f'        <a class="hub-card" href="/compare/{comp}/"><span class="hub-card-title">{comp_title}</span></a>\n'
        compares_html += '      </div>\n    </section>\n'
    
    # Build alerts/scams HTML
    safety_html = ""
    if alerts or scams:
        safety_html = '    <section class="hub-section">\n      <h2>⚠️ Travel Safety</h2>\n      <div class="hub-grid">\n'
        for a in alerts:
            a_title = a.replace("-", " ").title()
            safety_html += f'        <a class="hub-card" href="/alerts/{a}/"><span class="hub-card-title">{a_title}</span></a>\n'
        for s in scams:
            s_title = s.replace("-", " ").title()
            safety_html += f'        <a class="hub-card" href="/scams/{s}/"><span class="hub-card-title">{s_title}</span></a>\n'
        safety_html += '      </div>\n    </section>\n'
    
    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{city_name} Travel Guide 2026 — Best Picks, Comparisons & Tips | tabiji.ai</title>
<meta name="description" content="Your complete {city_name} travel hub: {len(picks)} curated guides, destination comparisons, travel alerts, and free custom itineraries. Built from real traveler insights.">
<link rel="canonical" href="https://tabiji.ai/destinations/{city}/">
<meta property="og:title" content="{city_name} Travel Guide 2026 | tabiji.ai">
<meta property="og:description" content="Your complete {city_name} travel hub: {len(picks)} curated guides, comparisons, and free itineraries.">
<meta property="og:url" content="https://tabiji.ai/destinations/{city}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="tabiji.ai">
<script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "TouristDestination",
  "name": "{city_name}",
  "description": "Complete {city_name} travel guide with {len(picks)} curated popular picks, destination comparisons, and free custom itineraries.",
  "url": "https://tabiji.ai/destinations/{city}/",
  "touristType": ["Adventure travelers", "Culture enthusiasts", "Food lovers", "Budget travelers"]
}}</script>
<!-- @include:shared-head:start -->
<link rel="stylesheet" href="/assets/shared-shell.css">
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#2D3A5C">
<script defer src="/assets/shared-shell.js"></script>
<!-- @include:shared-head:end -->
<style>
:root {{ --indigo: #2D3A5C; --terracotta: #C4704B; --warm-cream: #faf7f2; --sand: #e0d6c8; --text: #2a2520; --text-muted: #7a6f63; }}
body {{ font-family: 'Inter', system-ui, sans-serif; background: var(--warm-cream); color: var(--text); margin: 0; }}
.hub-hero {{ background: linear-gradient(135deg, var(--indigo) 0%, #3d4d70 100%); color: white; padding: 3.5rem 1.5rem 2.5rem; text-align: center; }}
.hub-hero h1 {{ font-size: 2.2rem; margin: 0 0 .5rem; }}
.hub-hero p {{ font-size: 1.05rem; opacity: .85; margin: 0; max-width: 600px; margin: 0 auto; }}
.hub-stats {{ display: flex; gap: 1.5rem; justify-content: center; margin-top: 1.2rem; }}
.hub-stat {{ font-size: .85rem; opacity: .7; }}
.hub-stat strong {{ display: block; font-size: 1.4rem; opacity: 1; }}
.hub-container {{ max-width: 1100px; margin: 0 auto; padding: 2rem 1.5rem; }}
.hub-section {{ margin-bottom: 2rem; }}
.hub-section h2 {{ color: var(--indigo); font-size: 1.3rem; margin: 0 0 1rem; }}
.hub-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: .7rem; }}
.hub-card {{ display: block; background: white; border: 1px solid var(--sand); border-radius: 14px; padding: 1rem 1.2rem; text-decoration: none; color: var(--text); transition: border-color .2s, transform .15s; }}
.hub-card:hover {{ border-color: var(--terracotta); transform: translateY(-2px); }}
.hub-card-title {{ font-weight: 600; font-size: .92rem; }}
.hub-cta {{ background: linear-gradient(135deg, var(--terracotta) 0%, #b5613e 100%); border-radius: 18px; padding: 2rem; text-align: center; color: white; margin: 2rem 0; }}
.hub-cta h2 {{ color: white; margin: 0 0 .5rem; font-size: 1.3rem; }}
.hub-cta p {{ margin: 0 0 1rem; opacity: .9; }}
.hub-cta a {{ display: inline-block; background: white; color: var(--terracotta); padding: .75rem 2rem; border-radius: 12px; font-weight: 700; text-decoration: none; transition: transform .15s; }}
.hub-cta a:hover {{ transform: translateY(-2px); }}
.hub-discovery {{ display: flex; gap: .8rem; justify-content: center; margin-top: 1.5rem; flex-wrap: wrap; }}
.hub-discovery a {{ background: rgba(255,255,255,.12); color: white; padding: .5rem 1.2rem; border-radius: 10px; text-decoration: none; font-size: .88rem; border: 1px solid rgba(255,255,255,.15); }}
.hub-discovery a:hover {{ background: rgba(255,255,255,.2); }}
</style>
</head>
<body>
<!-- @include:nav:start -->
<!-- @include:nav:end -->
  <div class="hub-hero">
    <h1>{city_name} Travel Guide</h1>
    <p>Everything you need to plan your {city_name} trip — curated from real traveler experiences.</p>
    <div class="hub-stats">
      <div class="hub-stat"><strong>{len(picks)}</strong> guides</div>
      <div class="hub-stat"><strong>{len(compares)}</strong> comparisons</div>
      <div class="hub-stat"><strong>{len(alerts) + len(scams)}</strong> safety tips</div>
    </div>
  </div>

  <div class="hub-container">
    <section class="hub-section">
      <h2>📍 Popular Picks in {city_name}</h2>
      <div class="hub-grid">
{picks_html}      </div>
    </section>

{compares_html}{safety_html}
    <div class="hub-cta">
      <h2>Plan your {city_name} trip</h2>
      <p>Get a free custom itinerary built from real traveler insights — not generic templates.</p>
      <a href="/plan">Get a Free Itinerary →</a>
    </div>

    <div class="hub-discovery">
      <a href="/quiz/">🎯 Take the Quiz</a>
      <a href="/find/">🔍 Destination Finder</a>
    </div>
  </div>

<!-- @include:footer:start -->
<footer>
    <p>© 2026 tabiji.ai · <a href="/terms/" style="color: inherit; text-decoration: underline;">Terms of Service</a> · <a href="/privacy/" style="color: inherit; text-decoration: underline;">Privacy Policy</a> · <a href="/delete-data/" style="color: inherit; text-decoration: underline;">Delete My Data</a> · <a href="https://www.instagram.com/tabiji.ai/" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">Instagram</a> · <a href="https://www.youtube.com/@tabijiai" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">YouTube</a> · <a href="https://www.pinterest.com/tabijiai/" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">Pinterest</a> · <a href="https://x.com/tabijiai" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">X</a> · <a href="/media/" style="color: inherit; text-decoration: underline;">Media Studio</a> · <a href="/api/" style="color: inherit; text-decoration: underline;">API</a></p>
</footer>
<!-- @include:footer:end -->
</body>
</html>"""
    
    dest_path = os.path.join(DEST_DIR, city)
    os.makedirs(dest_path, exist_ok=True)
    
    filepath = os.path.join(dest_path, "index.html")
    is_new = not os.path.exists(filepath)
    
    # Don't overwrite existing hand-crafted pages
    if city in existing:
        continue
    
    with open(filepath, "w") as f:
        f.write(page_html)
    
    if is_new:
        created += 1
    else:
        updated += 1

print(f"Created {created} new destination hub pages, updated {updated}")
