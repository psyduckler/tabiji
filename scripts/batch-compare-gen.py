#!/usr/bin/env python3
"""
Batch compare page generator for tabiji.ai
Generates compare-data JSON, HTML pages, API JSON, and updates inventory + sitemap.

Usage:
  python3 batch-compare-gen.py generate <slug>   # Generate one compare page JSON + HTML
  python3 batch-compare-gen.py batch <slugs.json> # Process a batch of slugs from JSON file
  python3 batch-compare-gen.py finalize           # Update inventory, sitemap, API index after all pages built
"""

import json
import os
import re
import subprocess
import sys
import html as html_module
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parents[1]
COMPARE_DIR = REPO_ROOT / "compare"
DATA_DIR = REPO_ROOT / "compare-data"
API_COMPARE_DIR = REPO_ROOT / "api" / "v1" / "compare"
INVENTORY_PATH = COMPARE_DIR / "inventory.json"
SITEMAP_PATH = REPO_ROOT / "sitemap.xml"
QUEUE_PATH = REPO_ROOT / "compare-queue.json"
SHELL_TEMPLATE_PATH = Path(__file__).resolve().parent / "compare-shell-template.json"

# Load shell template
def get_shell():
    return json.loads(SHELL_TEMPLATE_PATH.read_text())

def slug_to_names(slug):
    """Convert 'tokyo-vs-kyoto' to ('Tokyo', 'Kyoto')"""
    parts = slug.split('-vs-')
    if len(parts) != 2:
        raise ValueError(f"Invalid slug format: {slug}")
    def titleize(s):
        # Handle special cases
        specials = {
            'st-lucia': 'St. Lucia',
            'el-calafate': 'El Calafate',
            'la-paz': 'La Paz',
            'la-union': 'La Union',
            'ho-chi-minh': 'Ho Chi Minh City',
            'san-miguel-de-allende': 'San Miguel de Allende',
            'pacific-coast-highway': 'Pacific Coast Highway',
            'playa-del-carmen': 'Playa del Carmen',
            'bocas-del-toro': 'Bocas del Toro',
            'leon-nicaragua': 'León (Nicaragua)',
            'san-blas': 'San Blas Islands',
            'sacred-valley': 'Sacred Valley',
            'colca-canyon': 'Colca Canyon',
            'douro-valley': 'Douro Valley',
            'costa-brava': 'Costa Brava',
            'cinque-terre': 'Cinque Terre',
            'death-valley': 'Death Valley',
            'big-sur': 'Big Sur',
            'trinidad-cuba': 'Trinidad (Cuba)',
            'turks-and-caicos': 'Turks and Caicos',
            'san-juan': 'San Juan',
            'lake-atitlan': 'Lake Atitlán',
            'amazon-ecuador': 'Amazon (Ecuador)',
            'napa-valley': 'Napa Valley',
            'santa-fe': 'Santa Fe',
            'sharm-el-sheikh': 'Sharm El Sheikh',
            'saint-louis': 'Saint-Louis',
            'garden-route': 'Garden Route',
            'ras-al-khaimah': 'Ras Al Khaimah',
            'stone-town': 'Stone Town',
            'wadi-rum': 'Wadi Rum',
            'dead-sea': 'Dead Sea',
            'red-sea': 'Red Sea',
            'masai-mara': 'Masai Mara',
            'okavango-delta': 'Okavango Delta',
            'victoria-falls': 'Victoria Falls',
            'iguazu-falls': 'Iguazu Falls',
            'fish-river-canyon': 'Fish River Canyon',
            'simien-mountains': 'Simien Mountains',
            'al-ula': 'Al Ula',
            'great-barrier-reef': 'Great Barrier Reef',
            'ningaloo-reef': 'Ningaloo Reef',
            'south-island': 'South Island (NZ)',
            'abel-tasman': 'Abel Tasman',
            'milford-sound': 'Milford Sound',
            'byron-bay': 'Byron Bay',
            'gold-coast': 'Gold Coast',
            'margaret-river': 'Margaret River',
            'barossa-valley': 'Barossa Valley',
            'blue-mountains': 'Blue Mountains',
            'hunter-valley': 'Hunter Valley',
            'sunshine-coast': 'Sunshine Coast',
            'bay-of-islands': 'Bay of Islands',
            'new-caledonia': 'New Caledonia',
            'kangaroo-island': 'Kangaroo Island',
            'phillip-island': 'Phillip Island',
            'da-nang': 'Da Nang',
            'chiang-mai': 'Chiang Mai',
            'buenos-aires': 'Buenos Aires',
            'mexico-city': 'Mexico City',
            'mont-blanc': 'Mont Blanc',
            'rio-de-janeiro': 'Rio de Janeiro',
            'lake-bled': 'Lake Bled',
            'hoi-an': 'Hoi An',
            'torres-del-paine': 'Torres del Paine',
            'bora-bora': 'Bora Bora',
            'cape-town': 'Cape Town',
            'faroe-islands': 'Faroe Islands',
            'abu-dhabi': 'Abu Dhabi',
            'addis-ababa': 'Addis Ababa',
        }
        if s in specials:
            return specials[s]
        return ' '.join(word.capitalize() for word in s.split('-'))
    return titleize(parts[0]), titleize(parts[1])


def generate_compare_content(slug, dest1, dest2):
    """Use Gemini to generate compare page content."""
    api_key = subprocess.run(
        ['security', 'find-generic-password', '-s', 'gemini-api-key', '-w'],
        capture_output=True, text=True
    ).stdout.strip()
    
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    today_display = datetime.now(timezone.utc).strftime("%B %Y")
    
    prompt = f"""You are creating a travel comparison page for tabiji.ai comparing {dest1} vs {dest2}.

Generate a comprehensive, opinionated comparison with REAL travel data. Be specific with costs, distances, flight times.
Write like a well-traveled friend giving honest advice — not generic AI filler.

BANNED WORDS AND PHRASES — do NOT use any of these:
- "vibrant", "bustling", "unforgettable", "hidden gem", "rich tapestry"
- "unique blend", "something for everyone", "whether you're", "no matter what"
- "a feast for the senses", "steeped in history", "melting pot", "picture-perfect"
- "world-class", "must-visit", "breathtaking", "stunning", "enchanting"
- "seamlessly blends", "offers something", "it depends on your preferences"
Instead: use specific, concrete language. Say what IS there, not how it FEELS.

Output ONLY valid JSON (no markdown fences). The JSON structure must be EXACTLY:

{{
  "heroSubtitle": "One compelling sentence about this comparison — what makes it interesting",
  "heroBadge": "🆚 Comparison — [Region/Country]",
  "heroSources": "Relevant subreddits (e.g. r/travel, r/solotravel, r/[country]Travel)",
  "heroDataTypes": "Real traveler costs, flight routes, local insights",
  "metaDescription": "Write a unique, specific meta description for this comparison (max 155 chars). Include at least one specific number (budget, flight time, or price). Example: 'Paris vs New York compared: $80-150/day vs $120-200/day, 7h direct flights, café culture vs skyscraper energy. Honest picks.'",
  "verdictSummary": "2-3 sentences: who should pick which, with a rough daily budget range. Be opinionated — pick a side for most travelers.",
  "verdictTakeaways": [
    {{"choose": "{dest1}", "reason": "Who and why — be specific about traveler type"}},
    {{"choose": "{dest2}", "reason": "Who and why — be specific about traveler type"}},
    {{"choose": "Both", "reason": "When/why to do both and how long"}}
  ],
  "comparisonCategories": [
    {{
      "name": "Category Name",
      "emoji": "🏖️",
      "id": "kebab-case-id",
      "dest1Summary": "Key points for {dest1}",
      "dest2Summary": "Key points for {dest2}",
      "winner": "{dest1}" or "{dest2}" or "Tie",
      "deepDive": "Two paragraphs joined by \\n\\n. Para 1: dest1 specifics (places, prices, tips). Para 2: dest2 specifics. End with tabiji verdict: one opinionated sentence. Total 1000-1800 chars. CRITICAL: use \\n\\n between paragraphs, never literal newlines. Avoid apostrophes and special quotes.",
      "winnerWhy": "One sentence on why this destination wins this category",
      "winnerWhoMatters": "Who this matters most for"
    }}
  ],
  "decisionFramework": {{
    "dest1Reasons": ["7-9 specific, concrete reasons to choose {dest1} — e.g. 'You want $2 street tacos at 2am'"],
    "dest2Reasons": ["7-9 specific, concrete reasons to choose {dest2} — e.g. 'You want temples and 6am monks' alms ceremonies'"]
  }},
  "faqItems": [
    {{
      "question": "Natural question travelers ask about {dest1} vs {dest2}",
      "answer": "Detailed, helpful answer (2-4 sentences) with specific numbers"
    }}
  ],
  "ctaText": "Ready to plan your [region] trip?",
  "ctaDescription": "Get a free custom itinerary for {dest1}, {dest2}, or both — built from real traveler insights.",
  "ctaButton1": "Plan Your {dest1} Trip →",
  "ctaButton2": "Plan Your {dest2} Trip →",
  "methodologyPoints": [
    "Reviewed X+ Reddit threads from r/travel, r/solotravel, etc.",
    "Verified costs and logistics against current booking platforms",
    "Cross-referenced seasonal patterns and weather data"
  ]
}}

Requirements:
- EXACTLY 10 comparison categories (pick the most relevant from: beaches, food, nightlife, culture, costs, getting there, getting around, accommodation, day trips, weather/seasons, safety, nature, shopping, families, digital nomads, solo travel, etc.)
- EXACTLY 8 FAQ items
- Each deepDive must be 1000-1800 chars (two paragraphs + verdict) with specific place names, prices in local currency AND USD. Use \\n\\n between paragraphs in the JSON string.
- Be opinionated — pick real winners, don't hedge everything as "Tie"
- Include specific restaurant/hotel/attraction names where relevant
- decisionFramework: 7-9 bullet points per destination, each concrete and specific
- metaDescription: max 155 chars, include at least one number
- ZERO banned words/phrases — every single one will be flagged and rejected
"""

    import urllib.request
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.9,
            "maxOutputTokens": 8192,
            "responseMimeType": "application/json"
        }
    })
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, data=body.encode(), headers={"Content-Type": "application/json"})
            resp = urllib.request.urlopen(req, timeout=120)
            result = json.loads(resp.read())
            text = result['candidates'][0]['content']['parts'][0]['text']
            # Clean any markdown fences
            text = re.sub(r'^```json\s*', '', text.strip())
            text = re.sub(r'\s*```$', '', text.strip())
            # Try to fix common JSON issues
            # Replace literal newlines in strings
            # First try direct parse
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                # Try fixing escaped quotes and newlines in strings
                fixed = text.replace('\n', '\\n')
                # That's too aggressive — instead try a more targeted fix
                # Remove control characters
                fixed = re.sub(r'[\x00-\x1f](?!["\\bfnrt/])', ' ', text)
                try:
                    return json.loads(fixed)
                except json.JSONDecodeError:
                    raise
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  Retry {attempt+1} for {slug}: {e}")
                time.sleep(2 + attempt * 2)
            else:
                raise


def generate_rich_content(slug, dest1, dest2, base_content):
    """Second Gemini call for rich structured data: cost table, weather, itineraries, quick answers, scorecard."""
    api_key = subprocess.run(
        ['security', 'find-generic-password', '-s', 'gemini-api-key', '-w'],
        capture_output=True, text=True
    ).stdout.strip()

    # Extract category winners for scorecard
    categories_info = ""
    for cat in base_content.get('comparisonCategories', []):
        categories_info += f"- {cat['name']}: winner={cat['winner']}\n"

    prompt = f"""You are generating structured travel data for a {dest1} vs {dest2} comparison page on tabiji.ai.

Based on these comparison categories and winners:
{categories_info}

Generate ALL of the following as valid JSON. Be specific with real prices, temperatures, and place names.

BANNED: "vibrant", "bustling", "unforgettable", "hidden gem", "rich tapestry", "unique blend", "something for everyone", "world-class", "must-visit", "breathtaking"

{{
  "quickAnswers": [
    {{
      "question": "Which is cheaper?",
      "answer": "Short specific answer with numbers (1-2 sentences)",
      "winner": "{dest1}" or "{dest2}" or "Tie",
      "linkId": "kebab-case-section-id"
    }}
  ],
  "costTable": {{
    "items": [
      {{"label": "🛏️ Hostel dorm", "dest1Price": "$X–Y", "dest2Price": "$X–Y"}},
      {{"label": "🏨 Budget hotel", "dest1Price": "$X–Y", "dest2Price": "$X–Y"}},
      {{"label": "🍽️ Meal (mid-range)", "dest1Price": "$X–Y", "dest2Price": "$X–Y"}},
      {{"label": "🍺 Beer/drink", "dest1Price": "$X–Y", "dest2Price": "$X–Y"}},
      {{"label": "🚇 Local transport", "dest1Price": "$X–Y", "dest2Price": "$X–Y"}},
      {{"label": "☕ Coffee", "dest1Price": "$X–Y", "dest2Price": "$X–Y"}},
      {{"label": "📊 Daily total (mid-range)", "dest1Price": "$X–Y", "dest2Price": "$X–Y"}}
    ],
    "savingsSummary": "Which city saves how much per day and over a 5-day trip"
  }},
  "weatherData": [
    {{"month": "Jan", "dest1Temp": "X°", "dest2Temp": "Y°", "flag": ""}},
    {{"month": "Feb", "dest1Temp": "X°", "dest2Temp": "Y°", "flag": ""}},
    {{"month": "Mar", "dest1Temp": "X°", "dest2Temp": "Y°", "flag": ""}},
    {{"month": "Apr", "dest1Temp": "X°", "dest2Temp": "Y°", "flag": ""}},
    {{"month": "May", "dest1Temp": "X°", "dest2Temp": "Y°", "flag": "best"}},
    {{"month": "Jun", "dest1Temp": "X°", "dest2Temp": "Y°", "flag": ""}},
    {{"month": "Jul", "dest1Temp": "X°", "dest2Temp": "Y°", "flag": ""}},
    {{"month": "Aug", "dest1Temp": "X°", "dest2Temp": "Y°", "flag": "avoid"}},
    {{"month": "Sep", "dest1Temp": "X°", "dest2Temp": "Y°", "flag": "best"}},
    {{"month": "Oct", "dest1Temp": "X°", "dest2Temp": "Y°", "flag": "best"}},
    {{"month": "Nov", "dest1Temp": "X°", "dest2Temp": "Y°", "flag": ""}},
    {{"month": "Dec", "dest1Temp": "X°", "dest2Temp": "Y°", "flag": ""}}
  ],
  "itineraries": [
    {{
      "tabLabel": "3 Days in {dest1}",
      "title": "Weekend in {dest1} (3 Days)",
      "days": [
        {{"dayNum": "Day 1", "desc": "Specific activities with costs and tips (2-3 sentences)"}},
        {{"dayNum": "Day 2", "desc": "Specific activities with costs and tips (2-3 sentences)"}},
        {{"dayNum": "Day 3", "desc": "Specific activities with costs and tips (2-3 sentences)"}}
      ],
      "tip": "One insider tip with a specific cost or time-saving hack"
    }},
    {{
      "tabLabel": "3 Days in {dest2}",
      "title": "Weekend in {dest2} (3 Days)",
      "days": [
        {{"dayNum": "Day 1", "desc": "..."}},
        {{"dayNum": "Day 2", "desc": "..."}},
        {{"dayNum": "Day 3", "desc": "..."}}
      ],
      "tip": "..."
    }},
    {{
      "tabLabel": "7 Days in {dest1}",
      "title": "One Week in {dest1} (7 Days)",
      "days": [
        {{"dayNum": "Days 1–2", "desc": "..."}},
        {{"dayNum": "Days 3–4", "desc": "..."}},
        {{"dayNum": "Days 5–6", "desc": "..."}},
        {{"dayNum": "Day 7", "desc": "..."}}
      ],
      "tip": "..."
    }},
    {{
      "tabLabel": "7 Days in {dest2}",
      "title": "One Week in {dest2} (7 Days)",
      "days": [
        {{"dayNum": "Days 1–2", "desc": "..."}},
        {{"dayNum": "Days 3–4", "desc": "..."}},
        {{"dayNum": "Days 5–6", "desc": "..."}},
        {{"dayNum": "Day 7", "desc": "..."}}
      ],
      "tip": "..."
    }}
  ],
  "scorecardRows": [
    {{"emoji": "💰", "label": "Budget", "dest1Pct": 80, "dest2Pct": 60, "winner": "{dest1}" or "{dest2}" or "Tie"}}
  ],
  "dest1Score": 0,
  "dest2Score": 0,
  "tieCount": 0,
  "personalizeRecommendations": {{
    "solo_backpacker_food": "For a <strong>solo backpacker into food</strong>, pick <strong>[winner]</strong>. [1 sentence with specific place and price].",
    "solo_midrange_culture": "...",
    "solo_midrange_beaches": "...",
    "couple_midrange_food": "...",
    "couple_midrange_culture": "...",
    "couple_midrange_beaches": "...",
    "couple_luxury_food": "...",
    "family_midrange_food": "...",
    "family_midrange_beaches": "...",
    "friends_midrange_nightlife": "...",
    "friends_midrange_food": "...",
    "friends_backpacker_nightlife": "..."
  }},
  "relatedComparisons": [
    {{
      "slug": "similar-comparison-slug",
      "title": "City A vs City B",
      "desc": "One sentence description"
    }}
  ],
  "sectionPhotoQueries": [
    {{"sectionIndex": 0, "dest1Query": "[dest1] [topic] travel photo", "dest2Query": "[dest2] [topic] travel photo"}}
  ]
}}

Requirements:
- quickAnswers: exactly 6 items covering cost, food, safety, culture, weather, and one unique category
- costTable: 7 items including daily total. Use USD prices. Be realistic.
- weatherData: 12 months. Use average high temps in °C. Mark 2-3 months as "best", 1-2 as "avoid"
- itineraries: 4 total (3-day + 7-day for each destination). Each day description should mention specific places, costs, and tips.
- scorecardRows: One row per comparison category from the base content. dest1Pct/dest2Pct are 0-100 showing relative strength (winner gets 70-90, loser gets 40-60, ties get similar numbers)
- dest1Score/dest2Score/tieCount: count of category wins for each destination
- relatedComparisons: 3 items with slugs of real travel comparisons that would interest the same audience
- personalizeRecommendations: 12 entries covering key combos. Each 1 sentence with a specific place/price. Use <strong> tags. Always pick a winner.
- sectionPhotoQueries: One entry per comparison category. dest1Query and dest2Query should be specific Google Images search queries for each destination's version of that category topic (e.g., "Madrid tapas bar food" and "Barcelona paella restaurant food").
- All prices in USD
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 8192,
            "responseMimeType": "application/json"
        }
    })

    max_retries = 3
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, data=body.encode(), headers={"Content-Type": "application/json"})
            resp = urllib.request.urlopen(req, timeout=120)
            result = json.loads(resp.read())
            text = result['candidates'][0]['content']['parts'][0]['text']
            text = re.sub(r'^```json\s*', '', text.strip())
            text = re.sub(r'\s*```$', '', text.strip())
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                fixed = re.sub(r'[\x00-\x1f](?!["\\bfnrt/])', ' ', text)
                return json.loads(fixed)
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  Rich content retry {attempt+1} for {slug}: {e}")
                time.sleep(2 + attempt * 2)
            else:
                print(f"  ⚠️ Rich content generation failed (non-fatal): {e}")
                return None


def build_compare_json(slug, content_data):
    """Build the full compare-data JSON from generated content."""
    dest1, dest2 = slug_to_names(slug)
    shell = get_shell()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    today_iso = f"{today}T00:00:00Z"
    today_display = datetime.now(timezone.utc).strftime("%B %Y")
    
    d = content_data
    
    # Build title
    title = f"{dest1} vs {dest2}: Which Should You Visit? (2026 Comparison) | tabiji.ai"
    short_title = f"{dest1} vs {dest2}: Which Should You Visit?"
    meta_desc = d.get('metaDescription', f"{dest1} vs {dest2} — a data-backed comparison based on Reddit discussions, real costs, and traveler preferences. Honest verdicts for your next trip.")
    
    canonical = f"https://tabiji.ai/compare/{slug}/"
    og_image = f"https://img.tabiji.ai/compare/{slug}/hero.jpg"
    
    # Build TOC items from categories
    toc_items = [
        {"href": "#the-tl-dr-verdict", "label": "⚡ The TL;DR Verdict"},
        {"href": "#how-we-built-this-comparison", "label": "📊 Methodology"},
        {"href": "#quick-comparison", "label": "📋 Quick Comparison"},
    ]
    for cat in d['comparisonCategories']:
        toc_items.append({"href": f"#{cat['id']}", "label": f"{cat['emoji']} {cat['name']}"})
    toc_items.append({"href": "#the-decision-framework", "label": "🎯 Decision Framework"})
    toc_items.append({"href": "#faq", "label": "❓ FAQ"})

    # Build TOC mobile HTML
    toc_links = "\n".join(f'<a href="{t["href"]}">{t["label"]}</a>' for t in toc_items)
    toc_mobile_html = f'''<div class="toc-mobile" id="toc-mobile" onclick="this.classList.toggle('open')">
<span class="toc-active-label">⚡ The TL;DR Verdict</span>
<div class="toc-mobile-dropdown">
{toc_links}
</div>
</div>'''
    
    # Build TOC sidebar HTML
    toc_sidebar_links = "\n".join(f'<a href="{t["href"]}">{t["label"]}</a>' for t in toc_items)
    toc_sidebar_html = f'''<aside class="toc-sidebar">
<div class="toc-title">On this page</div>
{toc_sidebar_links}
</aside>'''
    
    # Hero HTML
    hero_html = f'''<section class="hero">
<div class="hero-badge">{html_module.escape(d.get('heroBadge', f'🆚 Destination Comparison'))}</div>
<h1>{dest1} vs {dest2}: <em>Which Should You Visit?</em></h1>
<p>{html_module.escape(d.get('heroSubtitle', f'A data-backed comparison to help you decide between {dest1} and {dest2}.'))}</p>
<div class="hero-meta">
<div><strong>Updated:</strong> {today_display}</div>
<div><strong>Sources:</strong> {html_module.escape(d.get('heroSources', 'r/travel, r/solotravel'))}</div>
<div><strong>Data:</strong> {html_module.escape(d.get('heroDataTypes', 'Real traveler costs, flight routes, local insights'))}</div>
</div>
</section>'''
    
    # Methodology HTML
    method_points = "\n".join(f"<li>{html_module.escape(p)}</li>" for p in d.get('methodologyPoints', [
        "Reviewed multiple Reddit threads from r/travel and r/solotravel.",
        "Verified costs against current booking platforms.",
        "Cross-referenced seasonal patterns and weather data."
    ]))
    methodology_html = f'''<div class="methodology-box"><h2 id="how-we-built-this-comparison">How we built this comparison</h2><p>This page combines traveler discussion patterns, published price ranges, flight schedules, and seasonal data to help you decide between {dest1} and {dest2}.</p><ul class="methodology-points">{method_points}</ul></div>'''
    
    # Photo grid (placeholder — no actual images needed)
    photo_grid_html = f'''<div class="photo-grid">
<div>
<img alt="{dest1} travel destination" loading="lazy" src="https://img.tabiji.ai/compare/{slug}/dest1.jpg">
<div class="caption">{dest1}</div>
</img></div>
<div>
<img alt="{dest2} travel destination" loading="lazy" src="https://img.tabiji.ai/compare/{slug}/dest2.jpg">
<div class="caption">{dest2}</div>
</img></div>
</div>'''
    
    # Verdict HTML
    takeaways = "\n".join(
        f'<li><strong>Choose {html_module.escape(t["choose"])}:</strong> {html_module.escape(t["reason"])}</li>'
        for t in d.get('verdictTakeaways', [])
    )
    verdict_html = f'''<div class="verdict-box"><h2 id="the-tl-dr-verdict">⚡ The TL;DR Verdict</h2><p class="verdict-summary"><strong>{html_module.escape(d.get("verdictSummary", ""))}</strong></p><ul class="verdict-takeaways">{takeaways}</ul></div>'''
    
    # Comparison table HTML
    rows = "\n".join(f'''<tr>
<td>{html_module.escape(cat["name"])}</td>
<td>{html_module.escape(cat["dest1Summary"])}</td>
<td>{html_module.escape(cat["dest2Summary"])}</td>
<td><span class="edge-{cat['winner'].lower().replace(' ', '-')}">{html_module.escape(cat["winner"])}</span></td>
</tr>''' for cat in d['comparisonCategories'])
    
    comparison_html = f'''<div class="comparison-section">
<h2 id="quick-comparison">Quick Comparison</h2>
<table class="comparison-table">
<thead>
<tr>
<th>Category</th>
<th>{dest1}</th>
<th>{dest2}</th>
<th>Winner</th>
</tr>
</thead>
<tbody>
{rows}
</tbody>
</table>
</div>'''
    
    # Deep dive sections
    deep_dive_html = []
    for cat in d['comparisonCategories']:
        # Parse deepDive text into paragraphs, extract Reddit quotes
        dive_text = cat.get('deepDive', '')
        # Split into paragraphs
        paragraphs = [p.strip() for p in dive_text.split('\n\n') if p.strip()]
        if not paragraphs:
            paragraphs = [dive_text]
        
        body_parts = []
        for p in paragraphs:
            # Check if it looks like a Reddit quote
            if p.startswith('"') or p.startswith('"') or p.startswith("'"):
                quote_text = p.strip('"').strip('"').strip("'").strip('"')
                body_parts.append(f'''<div class="reddit-quote">
            "{html_module.escape(quote_text)}"
            <span class="source">— <a href="https://www.reddit.com/r/travel/">r/travel user</a></span>
</div>''')
            else:
                body_parts.append(f'<p>{p}</p>')
        
        winner_section = f'''<div class="section-winner"><h3>Winner takeaway</h3><ul><li><strong>Winner:</strong> {html_module.escape(cat["winner"])}</li><li><strong>Why:</strong> {html_module.escape(cat.get("winnerWhy", ""))}</li><li><strong>Who this matters for:</strong> {html_module.escape(cat.get("winnerWhoMatters", ""))}</li></ul></div>'''
        
        section = f'''<section class="deep-dive">
<h2 id="{cat['id']}">{cat['emoji']} {html_module.escape(cat['name'])}</h2>
{''.join(body_parts)}
{winner_section}
</section>'''
        deep_dive_html.append(section)
    
    # Decision Framework HTML
    df = d.get('decisionFramework', {})
    dest1_reasons = df.get('dest1Reasons', [f"You want the {dest1} experience"])
    dest2_reasons = df.get('dest2Reasons', [f"You want the {dest2} experience"])
    dest1_li = "\n".join(f"<li>{html_module.escape(r)}</li>" for r in dest1_reasons)
    dest2_li = "\n".join(f"<li>{html_module.escape(r)}</li>" for r in dest2_reasons)
    decision_framework_html = f'''<section class="deep-dive">
<h2 id="the-decision-framework">🎯 The Decision Framework</h2>
<div class="decision-grid">
<div class="decision-card dest1-card">
<h3>Choose {dest1} If…</h3>
<ul>
{dest1_li}
</ul>
</div>
<div class="decision-card dest2-card">
<h3>Choose {dest2} If…</h3>
<ul>
{dest2_li}
</ul>
</div>
</div>
</section>'''
    deep_dive_html.append(decision_framework_html)

    # FAQ HTML
    faq_items_html = "\n".join(f'''<div class="faq-item" itemscope="" itemprop="mainEntity" itemtype="https://schema.org/Question">
<h3 itemprop="name">{html_module.escape(faq["question"])}</h3>
<div itemscope="" itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
<div itemprop="text"><p>{html_module.escape(faq["answer"])}</p></div>
</div>
</div>''' for faq in d['faqItems'])
    
    faq_html = f'''<div class="faq-section" id="faq" itemscope="" itemtype="https://schema.org/FAQPage">
<h2>❓ Frequently Asked Questions</h2>
{faq_items_html}
</div>'''
    
    # CTA HTML
    cta_html = f'''<div class="cta-section">
<h2>{html_module.escape(d.get("ctaText", f"Ready to plan your trip?"))}</h2>
<p>{html_module.escape(d.get("ctaDescription", f"Get a free custom itinerary for {dest1}, {dest2}, or both."))}</p>
<div class="cta-buttons">
<a class="cta-btn-primary" href="/plan">{html_module.escape(d.get("ctaButton1", f"Plan Your {dest1} Trip →"))}</a>
<a class="cta-btn-secondary" href="/plan">{html_module.escape(d.get("ctaButton2", f"Plan Your {dest2} Trip →"))}</a>
</div>
</div>'''
    
    # Build schema
    faq_schema = [
        {
            "@type": "Question",
            "name": faq["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["answer"]
            }
        }
        for faq in d['faqItems']
    ]
    
    full_json = {
        "slug": slug,
        "pageType": "compare-leaf",
        "status": "published",
        "destinations": {
            "destination1": dest1,
            "destination2": dest2
        },
        "seo": {
            "title": title,
            "metaDescription": meta_desc[:200],
            "ogTitle": f"{dest1} vs {dest2}: Which Should You Visit? — tabiji.ai",
            "ogDescription": f"Reddit-backed comparison of {dest1} and {dest2}. Real costs, honest verdicts from travelers who've been to both.",
            "ogImage": og_image,
            "twitterTitle": short_title,
            "twitterDescription": f"Data-backed comparison of {dest1} vs {dest2}. Costs, culture, and traveler verdicts.",
            "twitterImage": og_image,
            "publishedTime": today_iso,
            "modifiedTime": today_iso,
            "canonical": canonical
        },
        "schema": {
            "article": {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": short_title,
                "description": meta_desc[:200],
                "author": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai"},
                "publisher": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai"},
                "datePublished": today,
                "dateModified": today,
                "mainEntityOfPage": canonical,
                "image": og_image,
                "speakable": {
                    "@type": "SpeakableSpecification",
                    "cssSelector": [".hero h1", ".hero .subtitle", ".verdict-box", ".faq-section"]
                }
            },
            "breadcrumb": {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tabiji.ai/"},
                    {"@type": "ListItem", "position": 2, "name": "Compare", "item": "https://tabiji.ai/compare/"},
                    {"@type": "ListItem", "position": 3, "name": f"{dest1} vs {dest2}", "item": canonical}
                ]
            },
            "faq": {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": faq_schema
            }
        },
        "shell": shell,
        "content": {
            "heroHtml": hero_html,
            "tocMobileHtml": toc_mobile_html,
            "methodologyHtml": methodology_html,
            "tocSidebarHtml": toc_sidebar_html,
            "tocItems": toc_items,
            "photoGridHtml": photo_grid_html,
            "verdictHtml": verdict_html,
            "comparisonHtml": comparison_html,
            "deepDiveHtml": deep_dive_html,
            "faqHtml": faq_html,
            "faqItems": [{"question": f["question"], "answer": f["answer"]} for f in d['faqItems']],
            "ctaHtml": cta_html
        },
        "richContent": content_data.get("_richContent", {})
    }

    return full_json


def build_api_json(compare_data):
    """Build the API JSON from compare data."""
    slug = compare_data['slug']
    dest1 = compare_data['destinations']['destination1']
    dest2 = compare_data['destinations']['destination2']
    
    # Extract verdict from content
    verdict = ""
    for t in compare_data['content'].get('faqItems', [])[:1]:
        verdict = t.get('answer', '')[:300]
    
    # Use the verdict summary from verdictHtml if available
    verdict_match = re.search(r'<strong>(.*?)</strong>', compare_data['content']['verdictHtml'])
    if verdict_match:
        verdict = html_module.unescape(re.sub(r'<[^>]+>', '', verdict_match.group(1)))
    
    categories = []
    comparison_html = compare_data['content']['comparisonHtml']
    # Parse from the deep dive sections
    for dd in compare_data['content']['deepDiveHtml']:
        h2_match = re.search(r'<h2[^>]*>.*?</h2>', dd)
        name_match = re.search(r'<h2[^>]*>[^<]*?([A-Z][\w\s&]+)', dd)
        winner_match = re.search(r'<strong>Winner:</strong>\s*(\w+)', dd)
        why_match = re.search(r'<strong>Why:</strong>\s*(.*?)</li>', dd)
        
        if name_match:
            # Clean emoji from name
            raw_name = re.sub(r'^[^\w]+', '', h2_match.group(0) if h2_match else '')
            raw_name = re.sub(r'<[^>]+>', '', raw_name).strip()
            # Remove leading emoji
            raw_name = re.sub(r'^[\U00010000-\U0010ffff\u2600-\u27bf\u2702-\u27b0]+\s*', '', raw_name).strip()
            
            categories.append({
                "name": raw_name,
                "edge": html_module.unescape(winner_match.group(1)) if winner_match else "Tie",
                "summary": html_module.unescape(re.sub(r'<[^>]+>', '', why_match.group(1))) if why_match else ""
            })
    
    return {
        "slug": slug,
        "title": compare_data['seo']['twitterTitle'],
        "destination1": dest1,
        "destination2": dest2,
        "verdict": verdict[:300],
        "categories": categories[:10],
        "faq": [{"question": f["question"], "answer": f["answer"]} for f in compare_data['content']['faqItems']],
        "url": f"/compare/{slug}/",
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%d")
    }


def build_inventory_card(compare_data):
    """Build an inventory card for the compare index page."""
    slug = compare_data['slug']
    dest1 = compare_data['destinations']['destination1']
    dest2 = compare_data['destinations']['destination2']
    
    return {
        "slug": slug,
        "title": f"{dest1} vs {dest2}",
        "description": compare_data['seo']['metaDescription'][:200],
        "tags": [],
        "image1": f"https://img.tabiji.ai/compare/{slug}/dest1.jpg",
        "image2": f"https://img.tabiji.ai/compare/{slug}/dest2.jpg",
        "destination1": dest1,
        "destination2": dest2
    }


def _get_serpapi_key():
    return subprocess.run(
        ['security', 'find-generic-password', '-s', 'serpapi-key', '-w'],
        capture_output=True, text=True
    ).stdout.strip()

def _get_r2_token():
    return subprocess.run(
        ['security', 'find-generic-password', '-s', 'cloudflare-api-token', '-w'],
        capture_output=True, text=True
    ).stdout.strip()

R2_ACCOUNT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"

def search_destination_image(dest_name, serpapi_key):
    """Search SerpAPI for a travel photo. Returns image URL or None."""
    import urllib.parse
    query = f"{dest_name} travel destination scenic"
    url = f"https://serpapi.com/search.json?engine=google_images&q={urllib.parse.quote(query)}&api_key={serpapi_key}&ijn=0"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'tabiji/1.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        for img in data.get('images_results', [])[:10]:
            w = img.get('original_width', 0)
            h = img.get('original_height', 0)
            orig = img.get('original', '')
            if w >= 600 and h >= 400 and orig and not orig.endswith('.svg'):
                return orig
        results = data.get('images_results', [])
        if results:
            return results[0].get('original', '')
    except Exception as e:
        print(f"  ⚠️ Image search failed for {dest_name}: {e}")
    return None

def download_image(url, local_path):
    """Download image to local path. Returns True on success."""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Accept': 'image/*,*/*'
        })
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
            if len(data) < 5000:
                return False
            with open(local_path, 'wb') as f:
                f.write(data)
            return True
    except Exception as e:
        print(f"  ⚠️ Download failed: {e}")
        return False

def upload_to_r2(local_path, r2_key, r2_token):
    """Upload file to R2. Returns True on success."""
    try:
        result = subprocess.run(
            ['curl', '-s', '-X', 'PUT',
             '-H', f'Authorization: Bearer {r2_token}',
             '-H', 'Content-Type: image/jpeg',
             '--data-binary', f'@{local_path}',
             f'https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{r2_key}'],
            capture_output=True, text=True, timeout=30
        )
        resp = json.loads(result.stdout) if result.stdout else {}
        return resp.get('success', False)
    except Exception as e:
        print(f"  ⚠️ R2 upload failed for {r2_key}: {e}")
        return False

def upload_compare_images(slug, dest1, dest2):
    """Search, download, and upload dest1.jpg, dest2.jpg, hero.jpg for a compare page."""
    serpapi_key = _get_serpapi_key()
    r2_token = _get_r2_token()
    if not serpapi_key or not r2_token:
        print("  ⚠️ Missing SerpAPI or R2 credentials, skipping images")
        return
    
    tmpdir = Path(f"/tmp/compare-images/{slug}")
    tmpdir.mkdir(parents=True, exist_ok=True)
    r2_prefix = f"compare/{slug}"
    
    for label, dest_name, filename in [("dest1", dest1, "dest1.jpg"), ("dest2", dest2, "dest2.jpg")]:
        print(f"  📷 Searching image for {dest_name}...")
        img_url = search_destination_image(dest_name, serpapi_key)
        if not img_url:
            print(f"  ⚠️ No image found for {dest_name}")
            continue
        local = tmpdir / filename
        if download_image(img_url, local):
            if upload_to_r2(local, f"{r2_prefix}/{filename}", r2_token):
                print(f"  ✅ Uploaded {filename}")
                # Also use dest1 as hero.jpg
                if filename == "dest1.jpg":
                    if upload_to_r2(local, f"{r2_prefix}/hero.jpg", r2_token):
                        print(f"  ✅ Uploaded hero.jpg")
            local.unlink(missing_ok=True)
        time.sleep(0.3)
    
    # Cleanup
    for f in tmpdir.iterdir():
        f.unlink()
    tmpdir.rmdir()


def process_slug(slug):
    """Process a single slug: generate content, build JSON, render HTML, create API JSON, upload images."""
    dest1, dest2 = slug_to_names(slug)
    print(f"  Generating content for {dest1} vs {dest2}...")
    
    # Check if already exists
    data_path = DATA_DIR / f"{slug}.json"
    html_path = COMPARE_DIR / slug / "index.html"
    
    if html_path.exists():
        print(f"  ⏭️  {slug} already has HTML, skipping")
        return True
    
    # Generate content via Gemini
    try:
        content = generate_compare_content(slug, dest1, dest2)
    except Exception as e:
        print(f"  ❌ Failed to generate content for {slug}: {e}")
        return False

    # Generate rich structured data (cost table, weather, itineraries, etc.)
    print(f"  Generating rich structured data...")
    rich = generate_rich_content(slug, dest1, dest2, content)
    if rich:
        content['_richContent'] = rich
        print(f"  ✅ Rich content generated")
    else:
        content['_richContent'] = {}
        print(f"  ⚠️ Rich content skipped (will use basic template)")

    # Build full JSON
    try:
        compare_json = build_compare_json(slug, content)
    except Exception as e:
        print(f"  ❌ Failed to build JSON for {slug}: {e}")
        return False
    
    # Save compare-data JSON
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    data_path.write_text(json.dumps(compare_json, indent=2, ensure_ascii=False) + "\n")
    print(f"  ✅ Saved {data_path.name}")
    
    # Render HTML using build_compare.py's render function
    sys.path.insert(0, str(REPO_ROOT / "generators" / "compare"))
    from build_compare import render_page
    
    try:
        html_output = render_page(compare_json)
        html_path.parent.mkdir(parents=True, exist_ok=True)
        html_path.write_text(html_output)
        print(f"  ✅ Built {slug}/index.html")
    except Exception as e:
        print(f"  ❌ Failed to render HTML for {slug}: {e}")
        return False
    
    # Create API JSON
    api_json = build_api_json(compare_json)
    API_COMPARE_DIR.mkdir(parents=True, exist_ok=True)
    api_path = API_COMPARE_DIR / f"{slug}.json"
    api_path.write_text(json.dumps(api_json, indent=2, ensure_ascii=False) + "\n")
    print(f"  ✅ Created API JSON")
    
    # Upload destination images to R2
    try:
        upload_compare_images(slug, dest1, dest2)
    except Exception as e:
        print(f"  ⚠️ Image upload failed (non-fatal): {e}")
    
    return True


def update_queue(slugs, status="complete"):
    """Update compare-queue.json statuses."""
    queue = json.loads(QUEUE_PATH.read_text())
    slug_set = set(slugs)
    for item in queue:
        if item['slug'] in slug_set:
            item['status'] = status
    QUEUE_PATH.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n")
    print(f"Updated queue: {len(slugs)} items → {status}")


def update_inventory(new_cards):
    """Add new cards to inventory.json."""
    inv = json.loads(INVENTORY_PATH.read_text())
    existing_slugs = {c['slug'] for c in inv.get('cards', [])}
    added = 0
    for card in new_cards:
        if card['slug'] not in existing_slugs:
            inv['cards'].append(card)
            added += 1
    INVENTORY_PATH.write_text(json.dumps(inv, indent=2, ensure_ascii=False) + "\n")
    print(f"Inventory: added {added} new cards (total: {len(inv['cards'])})")


def update_sitemap(slugs):
    """Add new compare URLs to sitemap.xml."""
    sitemap = SITEMAP_PATH.read_text()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    new_entries = []
    for slug in slugs:
        url = f"https://tabiji.ai/compare/{slug}/"
        if url not in sitemap:
            new_entries.append(f"""  <url>
    <loc>{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>""")
    
    if new_entries:
        # Insert before closing </urlset>
        insert_point = sitemap.rfind("</urlset>")
        if insert_point > 0:
            sitemap = sitemap[:insert_point] + "\n".join(new_entries) + "\n" + sitemap[insert_point:]
            SITEMAP_PATH.write_text(sitemap)
            print(f"Sitemap: added {len(new_entries)} new URLs")
    else:
        print("Sitemap: no new URLs to add")


def cmd_generate(slug):
    """Generate a single compare page."""
    success = process_slug(slug)
    if success:
        update_queue([slug], "complete")
    return 0 if success else 1


def cmd_batch(slugs_file):
    """Process a batch of slugs from a JSON file."""
    slugs = json.loads(Path(slugs_file).read_text())
    print(f"Processing batch of {len(slugs)} slugs...")
    
    succeeded = []
    failed = []
    
    for i, slug in enumerate(slugs):
        print(f"\n[{i+1}/{len(slugs)}] {slug}")
        try:
            success = process_slug(slug)
            if success:
                succeeded.append(slug)
            else:
                failed.append(slug)
        except Exception as e:
            print(f"  ❌ Exception: {e}")
            failed.append(slug)
        
        # Small delay to avoid rate limits
        if i < len(slugs) - 1:
            time.sleep(0.5)
    
    # Update queue for succeeded items
    if succeeded:
        update_queue(succeeded, "complete")
    
    print(f"\n{'='*60}")
    print(f"✅ Succeeded: {len(succeeded)}")
    print(f"❌ Failed: {len(failed)}")
    if failed:
        print(f"Failed slugs: {json.dumps(failed)}")
    
    # Save results
    results = {"succeeded": succeeded, "failed": failed}
    results_path = Path(f"/tmp/compare-batch-results-{int(time.time())}.json")
    results_path.write_text(json.dumps(results, indent=2))
    print(f"Results saved to {results_path}")
    
    return 0 if not failed else 1


def cmd_finalize():
    """Update inventory, sitemap after all pages are built."""
    # Find all compare-data JSONs that have HTML pages
    new_cards = []
    new_slugs = []
    
    for json_file in sorted(DATA_DIR.glob("*.json")):
        slug = json_file.stem
        html_path = COMPARE_DIR / slug / "index.html"
        if html_path.exists():
            data = json.loads(json_file.read_text())
            card = build_inventory_card(data)
            new_cards.append(card)
            new_slugs.append(slug)
    
    update_inventory(new_cards)
    update_sitemap(new_slugs)
    print(f"Finalized {len(new_slugs)} compare pages")
    return 0


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    
    cmd = sys.argv[1]
    if cmd == "generate" and len(sys.argv) >= 3:
        return cmd_generate(sys.argv[2])
    elif cmd == "batch" and len(sys.argv) >= 3:
        return cmd_batch(sys.argv[2])
    elif cmd == "finalize":
        return cmd_finalize()
    else:
        print(__doc__)
        return 1


if __name__ == "__main__":
    sys.exit(main())
