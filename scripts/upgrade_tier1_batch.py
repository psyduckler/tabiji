#!/usr/bin/env python3
"""
Batch upgrade all Tier 1 popular picks pages with SEO/AEO/GEO improvements.
- Rich schema: aggregateRating, GeoCoordinates, openingHoursSpecification, image, telephone, BreadcrumbList, speakable
- Comparison table, budget tiers, occasion sections, vs comparisons, planning section
- Filter chips (client-side)
- Enriched image alt text
- Expanded FAQs (via Gemini)
"""
import json
import os
import re
import subprocess
import sys
import time
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PP_DIR = ROOT / "popular-picks"
DATA_DIR = ROOT / "popular-picks-data"
API_DIR = ROOT / "api" / "v1" / "picks"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or subprocess.check_output(
    ["security", "find-generic-password", "-s", "gemini-api-key", "-w"], text=True
).strip()

import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

_SLUG_FILE = Path(os.environ.get("SLUG_FILE", "/tmp/tier1_slugs.txt"))
TIER1_SLUGS = _SLUG_FILE.read_text().strip().split("\n")
SEMRUSH = json.loads(Path("/tmp/semrush_progress.json").read_text())

TODAY = date.today().isoformat()

# Skip already-upgraded page
SKIP = {"new-york-pizza"}

DAY_MAP = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday",
           "Thu": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"}


# ============================================================================
# DATA EXTRACTION
# ============================================================================

def load_page_data(slug):
    """Load structured data from API JSON + data JSON + HTML."""
    api_file = API_DIR / f"{slug}.json"
    data_file = DATA_DIR / f"{slug}.json"
    html_file = PP_DIR / slug / "index.html"

    if not html_file.exists() or not api_file.exists():
        return None

    api = json.loads(api_file.read_text())
    pdata = json.loads(data_file.read_text()) if data_file.exists() else {}
    html = html_file.read_text()

    places = api.get("places", [])
    # Also try picks from data JSON
    if not places and pdata:
        places = pdata.get("picks", [])

    # Extract geo from HTML data attributes
    geo_map = {}
    for m in re.finditer(r'data-map-name="(\d+)\.[^"]*"[^>]*data-map-lat="([^"]+)"[^>]*data-map-lng="([^"]+)"', html):
        try:
            geo_map[int(m.group(1))] = {"lat": float(m.group(2)), "lng": float(m.group(3))}
        except ValueError:
            pass

    # Normalize places
    normalized = []
    for i, p in enumerate(places):
        pos = p.get("position", p.get("rank", i + 1))
        np = {
            "rank": pos,
            "name": p.get("name", ""),
            "cuisineTags": p.get("cuisineTags", []),
            "googleRating": p.get("googleRating"),
            "reviewCount": p.get("reviewCount"),
            "priceRange": p.get("priceRange", p.get("priceRangeLocal", "")),
            "address": p.get("address", p.get("neighborhood", "")),
            "neighborhood": p.get("neighborhood", p.get("address", "")),
            "googleMapsUrl": p.get("googleMapsUrl", ""),
            "website": p.get("website"),
            "phone": p.get("phone"),
            "photo": p.get("photo"),
            "hoursNote": p.get("hoursNote"),
            "openingHours": p.get("openingHours"),
            "verdict": p.get("verdict", p.get("whyItMadeTheList", "")),
            "whatToOrder": p.get("whatToOrder", (p.get("comparison") or {}).get("what to order", "")),
            "redditQuotes": p.get("redditQuotes", []),
            "sectionId": p.get("sectionId", re.sub(r'[^a-z0-9]+', '-', p.get("name", "").lower()).strip('-')),
        }
        # Add geo
        geo = geo_map.get(pos)
        if geo:
            np["lat"] = geo["lat"]
            np["lng"] = geo["lng"]
        elif p.get("lat"):
            np["lat"] = p["lat"]
            np["lng"] = p.get("lng")
        normalized.append(np)

    return {
        "slug": slug,
        "title": api.get("title", pdata.get("seo", {}).get("h1", "")),
        "description": api.get("description", pdata.get("seo", {}).get("metaDescription", "")),
        "city": api.get("city", pdata.get("taxonomy", {}).get("city", "")),
        "category": api.get("category", pdata.get("taxonomy", {}).get("category", "")),
        "country": pdata.get("taxonomy", {}).get("countryCode", ""),
        "places": normalized,
        "html": html,
        "html_file": html_file,
        "keyword": SEMRUSH.get(slug, {}).get("keyword", slug.replace("-", " ")),
        "volume": SEMRUSH.get(slug, {}).get("volume", 0),
    }


# ============================================================================
# SCHEMA BUILDERS
# ============================================================================

def parse_time_24(token, fallback_suffix=None):
    token = token.strip()
    if not token: return None
    if token.endswith(("AM", "PM")): suffixed = token
    elif fallback_suffix: suffixed = f"{token} {fallback_suffix}"
    else: return None
    m = re.match(r"^(\d{1,2})(?::(\d{2}))?\s*(AM|PM)$", suffixed)
    if not m: return None
    hour, minute, suffix = int(m.group(1)), int(m.group(2) or "0"), m.group(3)
    if hour == 12: hour = 0
    if suffix == "PM": hour += 12
    return f"{hour:02d}:{minute:02d}"

def parse_hours(p):
    # Try hoursNote format: "Mon: 10:00 AM – 3:00 PM; Tue: ..."
    hours_note = p.get("hoursNote")
    if hours_note:
        specs = []
        for segment in hours_note.split(";"):
            segment = segment.strip()
            m = re.match(r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun):\s*(.*)", segment)
            if not m: continue
            day_short, value = m.group(1), m.group(2).strip()
            if not value or value.lower() == "closed": continue
            parts = re.split(r"\s*[–-]\s*", value)
            if len(parts) != 2: continue
            cs = re.search(r"(AM|PM)$", parts[1].strip())
            o = parse_time_24(parts[0], cs.group(1) if cs else None)
            c = parse_time_24(parts[1])
            if o and c:
                specs.append({"@type": "OpeningHoursSpecification", "dayOfWeek": DAY_MAP.get(day_short, day_short), "opens": o, "closes": c})
        return specs or None

    # Try openingHours dict format: {"Mon-Thu": "10:30 AM - 9:00 PM", ...}
    oh = p.get("openingHours")
    if oh and isinstance(oh, dict):
        specs = []
        for key, value in oh.items():
            if not value or value.lower() == "closed": continue
            parts = re.split(r"\s*[–-]\s*", value)
            if len(parts) != 2: continue
            cs = re.search(r"(AM|PM)$", parts[1].strip())
            o = parse_time_24(parts[0], cs.group(1) if cs else None)
            c = parse_time_24(parts[1])
            if not (o and c): continue
            # Expand day ranges like "Mon-Thu"
            day_range = re.match(r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s*[-–]\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun)", key)
            if day_range:
                days = list(DAY_MAP.keys())
                start_i = days.index(day_range.group(1))
                end_i = days.index(day_range.group(2))
                for di in range(start_i, end_i + 1):
                    specs.append({"@type": "OpeningHoursSpecification", "dayOfWeek": DAY_MAP[days[di]], "opens": o, "closes": c})
            else:
                for d in DAY_MAP:
                    if d in key:
                        specs.append({"@type": "OpeningHoursSpecification", "dayOfWeek": DAY_MAP[d], "opens": o, "closes": c})
        return specs or None
    return None

def infer_place_type(category, tags):
    hay = " ".join([category] + tags).lower()
    if any(k in hay for k in ["bar", "pub", "beer", "brewery", "cocktail", "wine"]):
        return "BarOrPub"
    if any(k in hay for k in ["cafe", "coffee", "brunch", "bakery"]):
        return "CafeOrCoffeeShop"
    if any(k in hay for k in ["hotel", "ryokan", "riad", "stay", "lodge"]):
        return "LodgingBusiness"
    if any(k in hay for k in ["market", "food", "restaurant", "ramen", "sushi", "pizza", "bbq", "chicken", "taco"]):
        return "Restaurant"
    if any(k in hay for k in ["tour", "museum", "art", "temple", "beach", "hike", "view"]):
        return "TouristAttraction"
    return "LocalBusiness"

def build_rich_itemlist(page):
    items = []
    for p in page["places"]:
        place_type = infer_place_type(page["category"], p.get("cuisineTags", []))
        obj = {"@type": place_type, "name": p["name"]}
        cuisine = p.get("cuisineTags", [])
        if cuisine and place_type in {"Restaurant", "CafeOrCoffeeShop", "BarOrPub"}:
            obj["servesCuisine"] = ", ".join(cuisine)
        addr = p.get("address") or p.get("neighborhood", "")
        if addr:
            obj["address"] = {"@type": "PostalAddress", "addressLocality": addr}
            if page.get("country"):
                obj["address"]["addressCountry"] = page["country"]
        if p.get("priceRange"):
            obj["priceRange"] = p["priceRange"]
        if p.get("googleRating") and p.get("reviewCount"):
            obj["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": p["googleRating"], "reviewCount": p["reviewCount"], "bestRating": 5}
        if p.get("lat") and p.get("lng"):
            obj["geo"] = {"@type": "GeoCoordinates", "latitude": p["lat"], "longitude": p["lng"]}
        hours = parse_hours(p)
        if hours:
            obj["openingHoursSpecification"] = hours
        if p.get("phone"): obj["telephone"] = p["phone"]
        if p.get("photo"): obj["image"] = p["photo"]
        if p.get("website"): obj["url"] = p["website"]
        if p.get("googleMapsUrl"): obj["hasMap"] = p["googleMapsUrl"]
        same_as = [u for u in [p.get("website"), p.get("googleMapsUrl")] if u]
        if same_as: obj["sameAs"] = same_as
        items.append({"@type": "ListItem", "position": p["rank"],
                       "url": f"https://tabiji.ai/popular-picks/{page['slug']}/#{p['sectionId']}", "item": obj})
    return {
        "@context": "https://schema.org", "@type": "ItemList",
        "name": page["title"], "description": page["description"],
        "url": f"https://tabiji.ai/popular-picks/{page['slug']}/",
        "numberOfItems": len(page["places"]),
        "itemListOrder": "https://schema.org/ItemListOrderAscending",
        "itemListElement": items
    }

def build_breadcrumb(page):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tabiji.ai/"},
                {"@type": "ListItem", "position": 2, "name": "Popular Picks", "item": "https://tabiji.ai/popular-picks/"},
                {"@type": "ListItem", "position": 3, "name": page["title"]}
            ]}


# ============================================================================
# CONTENT GENERATORS (programmatic)
# ============================================================================

def build_comparison_table(page):
    rows = ""
    for p in page["places"]:
        tags = ", ".join(p.get("cuisineTags", []))
        rating = f'{p.get("googleRating", "—")}★' if p.get("googleRating") else "—"
        area = (p.get("neighborhood") or p.get("address", "")).split(",")[0].strip()
        rows += f'<tr><td><strong>#{p["rank"]}</strong></td><td><a href="#{p["sectionId"]}">{escape(p["name"])}</a></td><td>{escape(tags)}</td><td>{escape(p.get("priceRange", "—"))}</td><td>{rating}</td><td>{escape(area)}</td></tr>\n'
    count = len(page["places"])
    return f'''<div class="comparison-table-section" style="margin-bottom:1.4rem;background:white;border:1px solid var(--sand);border-radius:18px;padding:1.35rem 1.4rem;overflow-x:auto;">
<h2 style="color:var(--indigo);margin:0 0 1rem;font-size:1.15rem;">All {count} Spots at a Glance</h2>
<table style="width:100%;border-collapse:collapse;font-size:.9rem;min-width:600px;">
<thead><tr style="border-bottom:2px solid var(--sand);text-align:left;">
<th style="padding:.5rem .4rem;color:var(--earth);font-size:.8rem;">#</th>
<th style="padding:.5rem .4rem;color:var(--earth);font-size:.8rem;">Name</th>
<th style="padding:.5rem .4rem;color:var(--earth);font-size:.8rem;">Style</th>
<th style="padding:.5rem .4rem;color:var(--earth);font-size:.8rem;">Price</th>
<th style="padding:.5rem .4rem;color:var(--earth);font-size:.8rem;">Rating</th>
<th style="padding:.5rem .4rem;color:var(--earth);font-size:.8rem;">Area</th>
</tr></thead><tbody>{rows}</tbody></table></div>'''

def build_filter_chips(page):
    """Build filter bar + CSS + JS for any page."""
    styles = sorted(set(t for p in page["places"] for t in p.get("cuisineTags", [])))
    if len(styles) < 2:
        return "", "", ""  # Not enough variety to filter

    style_chips = "".join(f'<span class="filter-chip" data-filter-group="style" data-filter-value="{escape(s)}">{escape(s)}</span>' for s in styles)

    bar_html = f'''<div class="filter-bar">
<span class="filter-label">Filter:</span> {style_chips}
</div>'''

    css = """
    .filter-bar { display:flex; flex-wrap:wrap; gap:.5rem; margin-bottom:1.4rem; padding:1rem; background:white; border:1px solid var(--sand); border-radius:18px; align-items:center; }
    .filter-bar .filter-label { font-weight:700; color:var(--indigo); font-size:.85rem; margin-right:.5rem; }
    .filter-chip { display:inline-flex; align-items:center; padding:.35rem .8rem; border-radius:999px; border:1px solid var(--sand); background:white; color:var(--text-muted); font-size:.82rem; cursor:pointer; transition:all .15s; user-select:none; }
    .filter-chip:hover { border-color:var(--terracotta); color:var(--terracotta); }
    .filter-chip.active { background:var(--terracotta); color:white; border-color:var(--terracotta); }
    .restaurant-section.filtered-out { display:none !important; }
"""

    js = '''<script>
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.filter-chip').forEach(function(chip) {
        chip.addEventListener('click', function() {
            var group = this.dataset.filterGroup, value = this.dataset.filterValue;
            if (this.classList.contains('active')) { this.classList.remove('active'); }
            else { document.querySelectorAll('.filter-chip[data-filter-group="'+group+'"]').forEach(function(c){c.classList.remove('active')}); this.classList.add('active'); }
            var active = {}; document.querySelectorAll('.filter-chip.active').forEach(function(c){ active[c.dataset.filterGroup] = c.dataset.filterValue; });
            document.querySelectorAll('.restaurant-section').forEach(function(s) {
                var show = true;
                if (active.style && (s.dataset.filterStyle||'').toLowerCase() !== active.style.toLowerCase()) show = false;
                s.classList.toggle('filtered-out', !show);
            });
        });
    });
});
</script>'''
    return bar_html, css, js


# ============================================================================
# GEMINI CONTENT GENERATION
# ============================================================================

def generate_content_sections(page):
    """Use Gemini to generate budget tiers, occasion sections, vs comparisons, planning section, extra FAQs."""
    places_summary = []
    for p in page["places"]:
        places_summary.append(f"#{p['rank']} {p['name']} — {', '.join(p.get('cuisineTags',[]))} — {p.get('priceRange','?')} — {p.get('neighborhood','?')} — {p.get('googleRating','?')}★ ({p.get('reviewCount','?')} reviews) — Verdict: {p.get('verdict','')[:100]}")
    places_text = "\n".join(places_summary)

    prompt = f"""You are a travel/food content expert. Generate content sections for a popular-picks page about "{page['title']}" in {page['city']}.

Here are the venues on this page:
{places_text}

Return a JSON object with this EXACT structure (no markdown fences, no explanation):

{{
  "budgetTiers": {{
    "tiers": [
      {{"label": "Budget", "emoji": "💰", "color": "#f0fdf4", "border": "#bbf7d0", "textColor": "#166534", "picks": [{{"name": "Venue Name", "sectionId": "venue-id", "note": "Brief note"}}]}},
      {{"label": "Mid-Range", "emoji": "🍽️", "color": "#eff6ff", "border": "#bfdbfe", "textColor": "#1e40af", "picks": [...]}},
      {{"label": "Splurge", "emoji": "✨", "color": "#fef3c7", "border": "#fde68a", "textColor": "#92400e", "picks": [...]}}
    ]
  }},
  "occasions": [
    {{"title": "Best for [Occasion]", "text": "2-3 sentences recommending 2-3 specific venues with anchor links. Use <a href=\\"#section-id\\"><strong>Venue Name</strong></a> format."}},
    ... (4-5 occasions)
  ],
  "vsComparisons": [
    {{"title": "Venue A vs Venue B", "text": "3-4 sentences comparing the top 2 venues head-to-head on price, quality, experience, vibe."}},
    ... (2-3 comparisons)
  ],
  "planningSection": {{
    "title": "Planning Your {page['city']} {page['category'].title()} Visit",
    "subsections": [
      {{"title": "Subsection Title", "text": "2-3 practical sentences about reservations, timing, payments, etiquette, etc."}}
    ]
  }},
  "extraFaqs": [
    {{"question": "Full question about {page['city']} {page['category']}?", "answer": "Detailed 2-3 sentence answer mentioning specific venues."}},
    ... (4-6 extra FAQs targeting AI engine queries)
  ]
}}

REQUIREMENTS:
- sectionId values must be kebab-case derived from venue names (e.g., "joes-pizza" for "Joe's Pizza")
- Budget tiers should have 2-3 picks each, using actual venues from the list
- Occasions should be specific to this city and category (e.g., "Best for a Date Night", "Best for Families", "Best Late Night")
- VS comparisons should compare the top 2-3 pairs that people would naturally compare
- Planning section should have 3-5 practical subsections relevant to this category in this city
- Extra FAQs should target queries people ask AI chatbots about this topic
- All venue references must use <a href="#sectionId"><strong>Name</strong></a> format
- Do NOT use markdown — only HTML inline tags (a, strong, em)
- Every pick in budgetTiers must reference a real venue from the list above
"""

    for attempt in range(3):
        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            # Strip markdown fences if present
            text = re.sub(r'^```json\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
            return json.loads(text)
        except Exception as e:
            print(f"    Gemini attempt {attempt+1} failed: {e}")
            time.sleep(2)
    return None


# ============================================================================
# HTML INJECTION
# ============================================================================

def render_budget_tiers(data):
    if not data or not data.get("tiers"): return ""
    tiers_html = ""
    for tier in data["tiers"]:
        picks_html = ""
        for pick in tier.get("picks", []):
            picks_html += f'<div><strong><a href="#{pick["sectionId"]}">{escape(pick["name"])}</a></strong> — {escape(pick.get("note",""))}</div>\n'
        tiers_html += f'''<div style="background:{tier.get("color","#f5f5f5")};border:1px solid {tier.get("border","#ddd")};border-radius:12px;padding:1rem;">
<div style="font-weight:700;color:{tier.get("textColor","#333")};margin-bottom:.4rem;">{tier.get("emoji","")} {escape(tier["label"])}</div>
{picks_html}</div>\n'''
    return f'''<div class="budget-tiers-section" style="margin-bottom:1.4rem;background:white;border:1px solid var(--sand);border-radius:18px;padding:1.35rem 1.4rem;">
<h2 style="color:var(--indigo);margin:0 0 1rem;font-size:1.15rem;">Quick Picks by Budget</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(200px, 1fr));gap:1rem;">{tiers_html}</div></div>'''

def render_occasions(occasions):
    if not occasions: return ""
    items = ""
    for occ in occasions:
        items += f'''<h3 style="color:var(--indigo);font-size:1rem;margin:1rem 0 .4rem;">{occ["title"]}</h3>
<p style="color:var(--text-muted);margin:0 0 .8rem;">{occ["text"]}</p>\n'''
    return f'''<div class="occasion-sections" style="margin-bottom:1.4rem;background:white;border:1px solid var(--sand);border-radius:18px;padding:1.35rem 1.4rem;">
<h2 style="color:var(--indigo);margin:0 0 1rem;font-size:1.15rem;">Best Picks by Occasion</h2>
{items}</div>'''

def render_vs_comparisons(comps):
    if not comps: return ""
    items = ""
    for c in comps:
        items += f'''<h3 style="color:var(--indigo);font-size:1rem;margin:1rem 0 .4rem;">{c["title"]}</h3>
<p style="color:var(--text-muted);margin:0 0 .8rem;">{c["text"]}</p>\n'''
    return f'''<div class="vs-comparisons" style="margin-bottom:1.4rem;background:white;border:1px solid var(--sand);border-radius:18px;padding:1.35rem 1.4rem;">
<h2 style="color:var(--indigo);margin:0 0 1rem;font-size:1.15rem;">Head-to-Head Comparisons</h2>
{items}</div>'''

def render_planning(planning):
    if not planning: return ""
    subs = ""
    for s in planning.get("subsections", []):
        subs += f'''<h3 style="color:var(--indigo);font-size:1rem;margin:.8rem 0 .4rem;">{escape(s["title"])}</h3>
<p style="color:var(--text-muted);margin:0 0 .8rem;">{s["text"]}</p>\n'''
    return f'''<div class="planning-section" style="margin-bottom:1.4rem;background:white;border:1px solid var(--sand);border-radius:18px;padding:1.35rem 1.4rem;">
<h2 style="color:var(--indigo);margin:0 0 1rem;font-size:1.15rem;">{escape(planning.get("title", "Planning Your Visit"))}</h2>
{subs}</div>'''

def render_extra_faqs_html(faqs):
    if not faqs: return ""
    items = ""
    for f in faqs:
        items += f'''<div class="faq-item"><h3>{escape(f["question"])}</h3><p>{f["answer"]}</p></div>\n'''
    return items


# ============================================================================
# MAIN UPGRADE FUNCTION
# ============================================================================

def upgrade_page(slug):
    page = load_page_data(slug)
    if not page:
        print(f"  SKIP {slug}: no data")
        return False

    html = page["html"]

    # --- 1. Replace ItemList schema ---
    new_itemlist = build_rich_itemlist(page)
    def replace_itemlist(m):
        try:
            d = json.loads(m.group(1))
            if d.get("@type") == "ItemList":
                return f'<script type="application/ld+json">{json.dumps(new_itemlist, indent=2, ensure_ascii=False)}</script>'
        except: pass
        return m.group(0)
    html = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL).sub(replace_itemlist, html)

    # --- 2. Add speakable to Article ---
    if '"speakable"' not in html:
        def add_speak(m):
            try:
                d = json.loads(m.group(1))
                if d.get("@type") == "Article":
                    d["speakable"] = {"@type": "SpeakableSpecification", "cssSelector": [".hero h1", ".hero .subtitle", ".quick-answer-section", ".budget-tiers-section", ".faq-section"]}
                    return f'<script type="application/ld+json">{json.dumps(d, indent=2, ensure_ascii=False)}</script>'
            except: pass
            return m.group(0)
        html = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL).sub(add_speak, html)

    # --- 3. Add BreadcrumbList ---
    if "BreadcrumbList" not in html:
        bc_json = json.dumps(build_breadcrumb(page), indent=2, ensure_ascii=False)
        html = html.replace("</head>", f'    <script type="application/ld+json">{bc_json}</script>\n</head>')

    # --- 4. Generate content via Gemini ---
    content = generate_content_sections(page)
    if not content:
        print(f"  WARNING {slug}: Gemini generation failed, applying schema-only upgrades")

    # --- 5. Build comparison table ---
    table_html = build_comparison_table(page)

    # --- 6. Build filter chips ---
    filter_bar, filter_css, filter_js = build_filter_chips(page)

    # --- 7. Build content section HTMLs ---
    budget_html = render_budget_tiers(content.get("budgetTiers")) if content else ""
    occasion_html = render_occasions(content.get("occasions")) if content else ""
    vs_html = render_vs_comparisons(content.get("vsComparisons")) if content else ""
    planning_html = render_planning(content.get("planningSection")) if content else ""
    extra_faq_html = render_extra_faqs_html(content.get("extraFaqs")) if content else ""

    # --- 8. Add extra FAQs to FAQPage schema ---
    if content and content.get("extraFaqs"):
        def add_faqs(m):
            try:
                d = json.loads(m.group(1))
                if d.get("@type") == "FAQPage":
                    for f in content["extraFaqs"]:
                        d["mainEntity"].append({"@type": "Question", "name": f["question"], "acceptedAnswer": {"@type": "Answer", "text": f["answer"]}})
                    return f'<script type="application/ld+json">{json.dumps(d, indent=2, ensure_ascii=False)}</script>'
            except: pass
            return m.group(0)
        html = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL).sub(add_faqs, html)

    # --- 9. Add filter CSS ---
    if filter_css and "filter-bar" not in html:
        html = html.replace("</style>", filter_css + "\n    </style>")

    # --- 10. Add filter data attributes to sections ---
    for p in page["places"]:
        style = p.get("cuisineTags", [""])[0] if p.get("cuisineTags") else ""
        sid = p["sectionId"]
        old = f'class="restaurant-section" id="{sid}"'
        if old in html and f'data-filter-style' not in html[html.find(old):html.find(old)+200]:
            new = f'class="restaurant-section" id="{sid}" data-filter-style="{escape(style)}"'
            html = html.replace(old, new, 1)

    # --- 11. Insert new content sections before first restaurant-section ---
    new_sections = table_html + "\n" + budget_html + "\n" + occasion_html + "\n" + vs_html
    if filter_bar:
        new_sections += "\n" + filter_bar
    first_section = re.search(r'(<section class="restaurant-section")', html)
    if first_section and "comparison-table-section" not in html:
        pos = first_section.start()
        html = html[:pos] + new_sections + "\n" + html[pos:]

    # --- 12. Insert planning section before FAQ ---
    if planning_html and "planning-section" not in html:
        faq_match = re.search(r'(<(?:div|section) class="faq-section")', html)
        if faq_match:
            html = html[:faq_match.start()] + planning_html + "\n" + html[faq_match.start():]

    # --- 13. Insert extra FAQs into HTML ---
    if extra_faq_html:
        faq_items = list(re.finditer(r'<div class="faq-item">', html))
        if faq_items:
            # Find the end of the last existing faq-item
            last_pos = faq_items[-1].start()
            # Find the next closing that ends the faq-item
            remaining = html[last_pos:]
            # Find </div></div> pattern that closes the faq-item
            close = re.search(r'</p>\s*</div>', remaining)
            if close:
                insert_at = last_pos + close.end()
                html = html[:insert_at] + "\n" + extra_faq_html + html[insert_at:]

    # --- 14. Enrich image alt text ---
    for p in page["places"]:
        if not p.get("photo"): continue
        old_alt = f'alt="{escape(p["name"])} in {escape(p.get("neighborhood", p.get("address", "")))}"'
        cuisine = ", ".join(p.get("cuisineTags", []))
        area = (p.get("neighborhood") or p.get("address", "")).split(",")[0].strip()
        new_alt_text = f'{cuisine} at {p["name"]}, {area}, {page["city"]} — {p.get("priceRange", "")}'
        new_alt = f'alt="{escape(new_alt_text)}"'
        if old_alt in html:
            html = html.replace(old_alt, new_alt)

    # --- 15. Add filter JS before </body> ---
    if filter_js and "filter-chip" in html and "filterGroup" not in html:
        html = html.replace("</body>", filter_js + "\n</body>")

    # --- 16. Update dateModified ---
    html = re.sub(r'"dateModified":\s*"[^"]*"', f'"dateModified": "{TODAY}"', html)

    # Validate before writing
    has_table = "comparison-table-section" in html
    has_rating = "aggregateRating" in html
    has_geo = "GeoCoordinates" in html
    orig_len = len(page["html"])
    new_len = len(html)
    print(f"    table={has_table} rating={has_rating} geo={has_geo} delta={new_len - orig_len}")

    if new_len <= orig_len:
        print(f"    WARNING: no content added (len unchanged), skipping write")
        return False

    # Write
    page["html_file"].write_text(html)
    return True


# ============================================================================
# MAIN
# ============================================================================

def main():
    start_idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 20

    slugs = [s for s in TIER1_SLUGS if s not in SKIP]
    batch = slugs[start_idx:start_idx + batch_size]

    print(f"=== Upgrading Tier 1 pages {start_idx}-{start_idx + len(batch)} of {len(slugs)} ===")
    success = 0
    failed = []

    for i, slug in enumerate(batch):
        vol = SEMRUSH.get(slug, {}).get("volume", 0)
        print(f"[{start_idx + i + 1}/{len(slugs)}] {slug} (vol={vol:,})")
        try:
            if upgrade_page(slug):
                success += 1
                print(f"  ✓ upgraded")
            else:
                failed.append(slug)
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed.append(slug)
        time.sleep(1)  # Rate limit Gemini

    print(f"\n=== DONE: {success} upgraded, {len(failed)} failed ===")
    if failed:
        print(f"Failed: {failed}")


if __name__ == "__main__":
    main()
