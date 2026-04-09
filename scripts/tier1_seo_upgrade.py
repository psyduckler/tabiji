#!/usr/bin/env python3
"""
Tier 1 Compare Pages — Comprehensive SEO/AEO/GEO Upgrade

Fixes applied per page:
  P0 — dateModified schema sync (all 128)
  P1 — empty/generic image alt text → descriptive (70-100 pages)
  P2 — cost breakdown table (125 pages)
  P2 — weather comparison table (128 pages)
  P2 — internal cross-link enrichment (~120 pages)
  P3 — itinerary venue specificity (~118 pages)

Usage:
    python3 scripts/tier1_seo_upgrade.py              # all remaining
    python3 scripts/tier1_seo_upgrade.py 0 20          # first 20
    python3 scripts/tier1_seo_upgrade.py --reset        # clear progress, start over
"""

import csv, json, os, re, subprocess, sys, time, traceback
from pathlib import Path
from datetime import date
from html import escape as html_escape

ROOT = Path(__file__).resolve().parents[1]
COMPARE_DIR = ROOT / "compare"
PP_DIR = ROOT / "popular-picks"
TODAY = date.today().isoformat()
PROGRESS_FILE = Path("/tmp/tier1_seo_upgrade_progress.json")
CACHE_DIR = Path("/tmp/tier1_seo_cache")
CACHE_DIR.mkdir(exist_ok=True)

# ── Gemini ──────────────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or subprocess.check_output(
    ["security", "find-generic-password", "-s", "gemini-api-key", "-w"], text=True
).strip()

import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)
gemini = genai.GenerativeModel("gemini-2.5-flash")

# ── Page indexes ────────────────────────────────────────────────
ALL_COMPARES = sorted([
    d for d in os.listdir(COMPARE_DIR)
    if '-vs-' in d and (COMPARE_DIR / d / "index.html").is_file()
])
ALL_PICKS = sorted([
    d for d in os.listdir(PP_DIR)
    if (PP_DIR / d / "index.html").is_file()
]) if PP_DIR.is_dir() else []


def load_slugs(min_vol=500, max_vol=999999):
    slugs = []
    with open(ROOT / "compare-search-volumes.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vol = int(row["best_vol"])
            if min_vol <= vol <= max_vol:
                slugs.append(row["slug"])
    return slugs


def extract_dests(html):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if not m:
        return None, None
    raw = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    vm = re.match(r'^(.+?)\s+vs\.?\s+(.+?)(?:\s*[:—–\-].+)?$', raw, re.I)
    if vm:
        return vm.group(1).strip(), vm.group(2).strip()
    return None, None


def slug_to_title(slug):
    return slug.replace('-', ' ').title().replace(' Vs ', ' vs ')


# ════════════════════════════════════════════════════════════════
# DETECTION
# ════════════════════════════════════════════════════════════════

def needs_alt_fix(html):
    return bool(re.search(r'alt=""', html)) or \
           bool(re.search(r'alt="[A-Z][^"]*travel destination"', html))


def has_cost_table(html):
    return 'ux-cost-table' in html


def has_weather_table(html):
    return 'ux-weather-table' in html


GENERIC_ITIN = [
    "Explore the top cultural attractions",
    "Sample local cuisine and signature dishes",
    "Wander the neighborhoods and soak up",
    "Get lost in the streets and discover hidden gems",
    "Visit the key museums, monuments",
    "Dive into the local food scene",
    "Take in the natural scenery",
    "Check out the bars, clubs",
    "Enjoy the best beaches",
    "Hit the top beaches",
    "Explore the natural landscapes",
    "Experience the nightlife and entertainment",
]


def has_generic_itineraries(html):
    if 'ux-itineraries' not in html:
        return False
    m = re.search(r'<div class="ux-itineraries".*?</script>', html, re.DOTALL)
    if not m:
        return False
    block = m.group(0)
    return any(phrase in block for phrase in GENERIC_ITIN)


# ════════════════════════════════════════════════════════════════
# P0: dateModified sync
# ════════════════════════════════════════════════════════════════

def fix_date_modified(html):
    return re.sub(r'"dateModified"\s*:\s*"[^"]*"', f'"dateModified": "{TODAY}"', html)


# ════════════════════════════════════════════════════════════════
# P1: Image alt text
# ════════════════════════════════════════════════════════════════

def fix_alt_text(html, dest1, dest2, ai_data):
    alts = ai_data.get("imageAlts", {})

    # Replace generic "X travel destination"
    if alts.get("dest1Hero"):
        html = re.sub(
            rf'alt="{re.escape(dest1)} travel destination"',
            f'alt="{html_escape(alts["dest1Hero"])}"',
            html
        )
    if alts.get("dest2Hero"):
        html = re.sub(
            rf'alt="{re.escape(dest2)} travel destination"',
            f'alt="{html_escape(alts["dest2Hero"])}"',
            html
        )

    # Fix empty alts on non-decorative images
    def _fix_empty(m):
        tag = m.group(0)
        src_m = re.search(r'src="([^"]*)"', tag)
        if not src_m:
            return tag
        src = src_m.group(1).lower()
        # Decorative images stay empty
        if any(k in src for k in ['logo', 'owl', 'icon', 'favicon']):
            return tag
        # Match to a destination
        d1_words = [w for w in dest1.lower().split() if len(w) > 2]
        d2_words = [w for w in dest2.lower().split() if len(w) > 2]
        if any(w in src for w in d1_words):
            alt = alts.get("dest1Hero", f"{dest1} cityscape and landmarks")
        elif any(w in src for w in d2_words):
            alt = alts.get("dest2Hero", f"{dest2} cityscape and landmarks")
        else:
            alt = f"{dest1} and {dest2} travel comparison"
        return tag.replace('alt=""', f'alt="{html_escape(alt)}"')

    html = re.sub(r'<img[^>]*alt=""[^>]*>', _fix_empty, html)
    return html


# ════════════════════════════════════════════════════════════════
# P2: Cost breakdown table
# ════════════════════════════════════════════════════════════════

def build_cost_table(dest1, dest2, ai_data):
    cost = ai_data.get("costTable", {})
    currency = cost.get("currency", "$")
    items = cost.get("items", [])
    if not items:
        return ""

    rows = ""
    for item in items:
        is_total = "total" in item.get("label", "").lower()
        border = "border-top:2px solid var(--sand,#d4c5a9);" if is_total else ""
        td_style = f' style="{border}padding:.45rem .6rem;"'
        label = item.get("label", "")
        v1 = item.get("dest1", "")
        v2 = item.get("dest2", "")
        if is_total:
            rows += f'<tr><td{td_style}><strong>{html_escape(label)}</strong></td><td{td_style}><strong>{currency}{html_escape(v1)}</strong></td><td{td_style}><strong>{currency}{html_escape(v2)}</strong></td></tr>\n'
        else:
            rows += f'<tr><td{td_style}>{html_escape(label)}</td><td{td_style}>{currency}{html_escape(v1)}</td><td{td_style}>{currency}{html_escape(v2)}</td></tr>\n'

    return f'''<div class="ux-cost-table" id="cost-breakdown" style="margin-bottom:1.4rem;background:white;border:1px solid var(--sand,#d4c5a9);border-radius:18px;padding:1.35rem 1.4rem;">
<h2 style="color:var(--indigo,#2D3A5C);margin:0 0 1rem;font-size:1.15rem;">&#128176; Daily Cost Breakdown</h2>
<div style="overflow-x:auto;">
<table style="width:100%;border-collapse:collapse;font-size:.9rem;">
<thead><tr style="border-bottom:2px solid var(--sand,#d4c5a9);text-align:left;">
<th style="padding:.5rem .6rem;color:var(--earth,#8B7355);font-size:.82rem;">Expense</th>
<th style="padding:.5rem .6rem;color:var(--earth,#8B7355);font-size:.82rem;">{html_escape(dest1)}</th>
<th style="padding:.5rem .6rem;color:var(--earth,#8B7355);font-size:.82rem;">{html_escape(dest2)}</th>
</tr></thead>
<tbody>{rows}</tbody>
</table>
</div>
<p style="font-size:.78rem;color:var(--text-muted,#6B7280);margin-top:.6rem;margin-bottom:0;">Approximate daily costs for 2026. Actual prices vary by season and travel style.</p>
</div>
'''


# ════════════════════════════════════════════════════════════════
# P2: Weather comparison table
# ════════════════════════════════════════════════════════════════

def build_weather_table(dest1, dest2, ai_data):
    weather = ai_data.get("weatherTable", {})
    months = weather.get("months", [])
    if not months:
        return ""

    rows = ""
    for i, m in enumerate(months):
        bg = ' style="background:var(--sand-light,#faf7f2);"' if i % 2 == 0 else ''
        rows += f'<tr{bg}>'
        rows += f'<td style="padding:.4rem .5rem;font-weight:600;">{html_escape(m.get("month",""))}</td>'
        rows += f'<td style="padding:.4rem .5rem;">{html_escape(m.get("dest1Temp",""))}</td>'
        rows += f'<td style="padding:.4rem .5rem;">{html_escape(m.get("dest1Rain",""))}</td>'
        rows += f'<td style="padding:.4rem .5rem;">{html_escape(m.get("dest2Temp",""))}</td>'
        rows += f'<td style="padding:.4rem .5rem;">{html_escape(m.get("dest2Rain",""))}</td>'
        rows += '</tr>\n'

    return f'''<div class="ux-weather-table" id="weather-comparison" style="margin-bottom:1.4rem;background:white;border:1px solid var(--sand,#d4c5a9);border-radius:18px;padding:1.35rem 1.4rem;">
<h2 style="color:var(--indigo,#2D3A5C);margin:0 0 1rem;font-size:1.15rem;">&#127780;&#65039; Monthly Weather Comparison</h2>
<div style="overflow-x:auto;">
<table style="width:100%;border-collapse:collapse;font-size:.85rem;min-width:520px;">
<thead><tr style="border-bottom:2px solid var(--sand,#d4c5a9);text-align:left;">
<th style="padding:.5rem;color:var(--earth,#8B7355);font-size:.8rem;">Month</th>
<th style="padding:.5rem;color:var(--earth,#8B7355);font-size:.8rem;">{html_escape(dest1)} Temp</th>
<th style="padding:.5rem;color:var(--earth,#8B7355);font-size:.8rem;">{html_escape(dest1)} Rain</th>
<th style="padding:.5rem;color:var(--earth,#8B7355);font-size:.8rem;">{html_escape(dest2)} Temp</th>
<th style="padding:.5rem;color:var(--earth,#8B7355);font-size:.8rem;">{html_escape(dest2)} Rain</th>
</tr></thead>
<tbody>{rows}</tbody>
</table>
</div>
<p style="font-size:.78rem;color:var(--text-muted,#6B7280);margin-top:.6rem;margin-bottom:0;">Average monthly high temperatures and rainfall based on historical climate data.</p>
</div>
'''


# ════════════════════════════════════════════════════════════════
# P2: Cross-link enrichment
# ════════════════════════════════════════════════════════════════

def find_related_compares(slug, limit=10):
    parts = slug.split('-vs-')
    d1_words = set(w for w in parts[0].split('-') if len(w) > 2)
    d2_words = set(w for w in parts[1].split('-') if len(w) > 2)
    related = []
    for c in ALL_COMPARES:
        if c == slug:
            continue
        if any(w in c for w in d1_words) or any(w in c for w in d2_words):
            related.append(c)
    return related[:limit]


def find_related_picks(slug, dest1, dest2, limit=12):
    words = set()
    for part in slug.split('-vs-'):
        words.update(w for w in part.split('-') if len(w) > 2)
    for name in [dest1.lower(), dest2.lower()]:
        words.update(w for w in name.split() if len(w) > 2)
    related = []
    for p in ALL_PICKS:
        if any(w in p for w in words):
            related.append(p)
    return related[:limit]


def enrich_cross_links(html, slug, dest1, dest2):
    """Add more internal links to ux-related-links if below 6 compare + 6 picks."""
    existing_compare = set(re.findall(r'href="/compare/([^/]+)/"', html))
    existing_picks = set(re.findall(r'href="/popular-picks/([^/]+)/"', html))

    compare_count = len(existing_compare)
    picks_count = len(existing_picks)

    if compare_count >= 6 and picks_count >= 6:
        return html, False

    new_compares = [c for c in find_related_compares(slug, 10)
                    if c not in existing_compare][:max(0, 6 - compare_count)]
    new_picks = [p for p in find_related_picks(slug, dest1, dest2, 12)
                 if p not in existing_picks][:max(0, 6 - picks_count)]

    if not new_compares and not new_picks:
        return html, False

    # Build new link groups
    new_html = ""
    d1_slug = slug.split('-vs-')[0]
    d2_slug = slug.split('-vs-')[1]

    if new_compares:
        d1_links = [c for c in new_compares if d1_slug in c][:3]
        d2_links = [c for c in new_compares if d2_slug in c and c not in d1_links][:3]
        others = [c for c in new_compares if c not in d1_links and c not in d2_links][:2]
        for links, label in [
            (d1_links, f"More {dest1} Comparisons"),
            (d2_links, f"More {dest2} Comparisons"),
            (others, "Related Comparisons"),
        ]:
            if links:
                items = ''.join(f'<li><a href="/compare/{c}/">&rarr; {slug_to_title(c)}</a></li>' for c in links)
                new_html += f'<h3 style="font-size:0.92rem;margin:0.5rem 0 0.3rem;color:var(--indigo,#2D3A5C)">{label}</h3><ul>{items}</ul>'

    if new_picks:
        items = ''.join(f'<li><a href="/popular-picks/{p}/">&rarr; {slug_to_title(p)}</a></li>' for p in new_picks)
        new_html += f'<h3 style="font-size:0.92rem;margin:0.5rem 0 0.3rem;color:var(--indigo,#2D3A5C)">Destination Guides</h3><ul>{items}</ul>'

    if not new_html:
        return html, False

    # Inject into existing ux-related-links
    if 'ux-related-links' in html:
        m = re.search(r'<div class="ux-related-links"[^>]*>', html)
        if m:
            start = m.end()
            remaining = html[start:]
            depth = 1
            pos = 0
            while depth > 0 and pos < len(remaining):
                next_open = remaining.find('<div', pos)
                next_close = remaining.find('</div>', pos)
                if next_close == -1:
                    break
                if next_open != -1 and next_open < next_close:
                    depth += 1
                    pos = next_open + 4
                else:
                    depth -= 1
                    if depth == 0:
                        insert_at = start + next_close
                        html = html[:insert_at] + new_html + '\n' + html[insert_at:]
                        return html, True
                    pos = next_close + 6
    else:
        # Create new section before CTA
        section = f'''<div class="ux-related-links" style="margin-bottom:1.4rem;background:white;border:1px solid var(--sand,#d4c5a9);border-radius:18px;padding:1.35rem 1.4rem;">
<h2 style="color:var(--indigo,#2D3A5C);margin:0 0 1rem;font-size:1.15rem;">&#128279; Related Guides &amp; Comparisons</h2>
{new_html}
</div>'''
        if '<div class="cta-section"' in html:
            html = html.replace('<div class="cta-section"', section + '\n' + '<div class="cta-section"')
        elif '<section class="faq-section"' in html:
            html = html.replace('<section class="faq-section"', section + '\n' + '<section class="faq-section"')

    return html, True


# ════════════════════════════════════════════════════════════════
# P3: Itinerary venue specificity
# ════════════════════════════════════════════════════════════════

def build_itinerary_html(dest1, dest2, ai_data, slug):
    itins = ai_data.get("itineraries", {})
    if not itins:
        return None

    picks = find_related_picks(slug, dest1, dest2, 4)
    d1_picks = [p for p in picks if any(w in p for w in dest1.lower().split() if len(w) > 3)]
    d2_picks = [p for p in picks if any(w in p for w in dest2.lower().split() if len(w) > 3)]

    def pick_link(pl, idx=0):
        if idx < len(pl):
            return f' Check out our <a href="/popular-picks/{pl[idx]}/">{slug_to_title(pl[idx])}</a> guide.'
        return ''

    def render_days(days):
        out = ""
        for d in days:
            day_label = str(d.get("day", d.get("days", "")))
            desc = d.get("desc", d.get("activities", ""))
            out += f'<div class="ux-itin-day"><span class="day-num">{html_escape(day_label)}</span><span class="day-desc">{desc}</span></div>\n'
        return out

    panels_data = [
        ("dest1_3day", f"3 Days {dest1}", f"Weekend in {dest1} (3 Days)", dest1, d1_picks),
        ("dest2_3day", f"3 Days {dest2}", f"Weekend in {dest2} (3 Days)", dest2, d2_picks),
        ("dest1_7day", f"7 Days {dest1}", f"Week in {dest1} (7 Days)", dest1, d1_picks),
        ("dest2_7day", f"7 Days {dest2}", f"Week in {dest2} (7 Days)", dest2, d2_picks),
    ]

    tabs = ""
    panels = ""
    panel_count = 0
    for key, tab_label, card_title, dest, dest_picks in panels_data:
        days = itins.get(key, [])
        if not days:
            continue
        active = " active" if panel_count == 0 else ""
        tabs += f'<button class="ux-itin-tab{active}" data-panel="itin-{panel_count}">{html_escape(tab_label)}</button>\n'

        days_html = render_days(days)
        dur = "Three days" if "3day" in key else "A full week"
        tip = f"{dur} gives you a great taste of {dest}.{pick_link(dest_picks, 0)}"

        panels += f'''<div class="ux-itin-panel{active}" id="itin-{panel_count}"><div class="ux-itin-card"><h3>{html_escape(card_title)}</h3>
{days_html}<p class="ux-itin-tip">&#128161; {tip}</p>
</div></div>
'''
        panel_count += 1

    if panel_count == 0:
        return None

    return f'''<div class="ux-itineraries" id="sample-itineraries">
<h2>&#128197; Sample Itineraries</h2>
<div class="ux-itin-tabs">
{tabs}</div>
{panels}</div>
<script>
document.querySelectorAll('.ux-itin-tab').forEach(function(tab){{
    tab.addEventListener('click', function(){{
        document.querySelectorAll('.ux-itin-tab').forEach(function(t){{ t.classList.remove('active'); }});
        document.querySelectorAll('.ux-itin-panel').forEach(function(p){{ p.classList.remove('active'); }});
        this.classList.add('active');
        var panel = document.getElementById(this.getAttribute('data-panel'));
        if(panel) panel.classList.add('active');
    }});
}});
</script>'''


def replace_itineraries(html, dest1, dest2, slug, ai_data):
    new_html = build_itinerary_html(dest1, dest2, ai_data, slug)
    if not new_html:
        return html, False
    # Replace entire ux-itineraries block + script
    m = re.search(r'<div class="ux-itineraries"[^>]*>.*?</script>', html, re.DOTALL)
    if m:
        html = html[:m.start()] + new_html + html[m.end():]
        return html, True
    return html, False


# ════════════════════════════════════════════════════════════════
# GEMINI: One call per page
# ════════════════════════════════════════════════════════════════

def generate_content(dest1, dest2, slug):
    """Single Gemini call for all AI content needed by a page."""
    cache_file = CACHE_DIR / f"{slug}.json"
    if cache_file.exists():
        try:
            return json.loads(cache_file.read_text())
        except:
            pass

    prompt = f"""You are a travel data expert. For the comparison "{dest1} vs {dest2}", generate structured travel data.

Return ONLY a valid JSON object (no markdown fences, no explanation):

{{
  "imageAlts": {{
    "dest1Hero": "Vivid 10-15 word scene description of iconic {dest1} landmark or landscape",
    "dest2Hero": "Vivid 10-15 word scene description of iconic {dest2} landmark or landscape"
  }},
  "costTable": {{
    "currency": "primary currency symbol for these destinations ($ € £ ¥ ฿ ₹ etc.)",
    "items": [
      {{"label": "Hostel dorm", "dest1": "low-high", "dest2": "low-high"}},
      {{"label": "Budget hotel", "dest1": "low-high", "dest2": "low-high"}},
      {{"label": "Street food meal", "dest1": "low-high", "dest2": "low-high"}},
      {{"label": "Restaurant meal", "dest1": "low-high", "dest2": "low-high"}},
      {{"label": "Beer/drink", "dest1": "low-high", "dest2": "low-high"}},
      {{"label": "Local transport (day)", "dest1": "low-high", "dest2": "low-high"}},
      {{"label": "Daily budget total", "dest1": "low-high", "dest2": "low-high"}}
    ]
  }},
  "weatherTable": {{
    "months": [
      {{"month": "Jan", "dest1Temp": "high°C/high°F", "dest1Rain": "Xmm", "dest2Temp": "high°C/high°F", "dest2Rain": "Xmm"}},
      {{"month": "Feb", "dest1Temp": "...", "dest1Rain": "...", "dest2Temp": "...", "dest2Rain": "..."}},
      {{"month": "Mar", "dest1Temp": "...", "dest1Rain": "...", "dest2Temp": "...", "dest2Rain": "..."}},
      {{"month": "Apr", "dest1Temp": "...", "dest1Rain": "...", "dest2Temp": "...", "dest2Rain": "..."}},
      {{"month": "May", "dest1Temp": "...", "dest1Rain": "...", "dest2Temp": "...", "dest2Rain": "..."}},
      {{"month": "Jun", "dest1Temp": "...", "dest1Rain": "...", "dest2Temp": "...", "dest2Rain": "..."}},
      {{"month": "Jul", "dest1Temp": "...", "dest1Rain": "...", "dest2Temp": "...", "dest2Rain": "..."}},
      {{"month": "Aug", "dest1Temp": "...", "dest1Rain": "...", "dest2Temp": "...", "dest2Rain": "..."}},
      {{"month": "Sep", "dest1Temp": "...", "dest1Rain": "...", "dest2Temp": "...", "dest2Rain": "..."}},
      {{"month": "Oct", "dest1Temp": "...", "dest1Rain": "...", "dest2Temp": "...", "dest2Rain": "..."}},
      {{"month": "Nov", "dest1Temp": "...", "dest1Rain": "...", "dest2Temp": "...", "dest2Rain": "..."}},
      {{"month": "Dec", "dest1Temp": "...", "dest1Rain": "...", "dest2Temp": "...", "dest2Rain": "..."}}
    ]
  }},
  "itineraries": {{
    "dest1_3day": [
      {{"day": "Day 1", "desc": "Arrive and settle in [specific neighborhood]. Walk to [specific landmark]. Lunch at [specific restaurant/market]. Afternoon at [specific attraction]. Dinner at [specific food street/restaurant]."}},
      {{"day": "Day 2", "desc": "Morning at [specific site]. Coffee at [specific café]. Visit [specific museum/temple/area]. Sunset from [specific viewpoint]."}},
      {{"day": "Day 3", "desc": "Day trip to [specific nearby place] or [alternative]. Return for farewell dinner at [specific spot]."}}
    ],
    "dest1_7day": [
      {{"day": "Days 1&ndash;2", "desc": "[Specific activities days 1-2 with real venue names]"}},
      {{"day": "Days 3&ndash;4", "desc": "[Specific activities and day trips days 3-4]"}},
      {{"day": "Days 5&ndash;6", "desc": "[Deeper exploration, specific neighborhoods and markets]"}},
      {{"day": "Day 7", "desc": "[Final highlights and farewell at specific restaurant]"}}
    ],
    "dest2_3day": [
      {{"day": "Day 1", "desc": "..."}},
      {{"day": "Day 2", "desc": "..."}},
      {{"day": "Day 3", "desc": "..."}}
    ],
    "dest2_7day": [
      {{"day": "Days 1&ndash;2", "desc": "..."}},
      {{"day": "Days 3&ndash;4", "desc": "..."}},
      {{"day": "Days 5&ndash;6", "desc": "..."}},
      {{"day": "Day 7", "desc": "..."}}
    ]
  }}
}}

CRITICAL REQUIREMENTS:
- Image alts: vivid specific scene descriptions (e.g. "Santorini blue-domed churches overlooking the caldera at golden hour" NOT "Santorini travel destination")
- Costs: realistic 2025/2026 price ranges. Just numbers in "low-high" format (no currency symbol in values — that's in the currency field). Use $ for Americas/generic, € for Europe, £ for UK, ¥ for Japan/China, ฿ for Thailand, ₹ for India, etc.
- Weather: accurate monthly average HIGH temps and total rainfall. Format: "25°C/77°F" and "45mm"
- Itineraries: MUST name REAL specific landmarks, restaurants, neighborhoods, temples, beaches, markets, cafés. NEVER use generic phrases like "explore cultural attractions" or "sample local cuisine"
- For country-level comparisons, use the capital or primary tourist city for costs/weather
- Keep itinerary descriptions to 2-3 sentences per entry
- All text must be plain text or basic HTML entities only (no markdown)
"""

    for attempt in range(3):
        try:
            response = gemini.generate_content(prompt)
            text = response.text.strip()
            text = re.sub(r'^```json\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
            data = json.loads(text)
            # Cache for resume
            cache_file.write_text(json.dumps(data, indent=2, ensure_ascii=False))
            return data
        except Exception as e:
            print(f"    Gemini attempt {attempt+1}/3 failed: {e}")
            if attempt < 2:
                time.sleep(3 * (attempt + 1))
    return {}


# ════════════════════════════════════════════════════════════════
# MAIN PAGE PROCESSOR
# ════════════════════════════════════════════════════════════════

def process_page(slug):
    path = COMPARE_DIR / slug / "index.html"
    if not path.exists():
        return f"SKIP {slug}: not found"

    html = path.read_text('utf-8')
    orig_len = len(html)
    dest1, dest2 = extract_dests(html)
    if not dest1 or not dest2:
        return f"SKIP {slug}: cannot parse destinations from H1"

    fixes = []

    # ── P0: dateModified ──
    html = fix_date_modified(html)
    fixes.append("P0:date")

    # ── Assess what needs AI ──
    _needs_alts = needs_alt_fix(html)
    _has_cost = has_cost_table(html)
    _has_weather = has_weather_table(html)
    _generic_itin = has_generic_itineraries(html)
    needs_ai = _needs_alts or not _has_cost or not _has_weather or _generic_itin

    # ── Gemini (one call) ──
    ai_data = {}
    if needs_ai:
        ai_data = generate_content(dest1, dest2, slug)
        if not ai_data:
            fixes.append("AI:FAILED")

    # ── P1: alt text ──
    if _needs_alts and ai_data:
        html = fix_alt_text(html, dest1, dest2, ai_data)
        fixes.append("P1:alts")

    # ── P3: itineraries (BEFORE table injection so injection point is clean) ──
    if _generic_itin and ai_data:
        html, did = replace_itineraries(html, dest1, dest2, slug, ai_data)
        if did:
            fixes.append("P3:itin")

    # ── P2: cost table ──
    if not _has_cost and ai_data:
        table = build_cost_table(dest1, dest2, ai_data)
        if table:
            if '<div class="ux-itineraries"' in html:
                html = html.replace('<div class="ux-itineraries"', table + '<div class="ux-itineraries"')
                fixes.append("P2:cost")
            elif '<div class="faq-section"' in html:
                html = html.replace('<div class="faq-section"', table + '<div class="faq-section"')
                fixes.append("P2:cost")
            elif '<section class="faq-section"' in html:
                html = html.replace('<section class="faq-section"', table + '<section class="faq-section"')
                fixes.append("P2:cost")
            else:
                fixes.append("P2:cost:NO_INJECT")
    elif _has_cost:
        fixes.append("P2:cost:EXISTS")

    # ── P2: weather table ──
    if not _has_weather and ai_data:
        table = build_weather_table(dest1, dest2, ai_data)
        if table:
            if '<div class="ux-itineraries"' in html:
                html = html.replace('<div class="ux-itineraries"', table + '<div class="ux-itineraries"')
                fixes.append("P2:weather")
            elif '<div class="faq-section"' in html:
                html = html.replace('<div class="faq-section"', table + '<div class="faq-section"')
                fixes.append("P2:weather")
            elif '<section class="faq-section"' in html:
                html = html.replace('<section class="faq-section"', table + '<section class="faq-section"')
                fixes.append("P2:weather")
            else:
                fixes.append("P2:weather:NO_INJECT")
    elif _has_weather:
        fixes.append("P2:weather:EXISTS")

    # ── P2: cross-links ──
    html, links_added = enrich_cross_links(html, slug, dest1, dest2)
    if links_added:
        fixes.append("P2:links")

    # ── Write ──
    new_len = len(html)
    delta = new_len - orig_len
    path.write_text(html, 'utf-8')
    return f"OK {slug}: delta={delta:+,} | {' '.join(fixes)}"


# ════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset', action='store_true')
    parser.add_argument('--min-vol', type=int, default=500)
    parser.add_argument('--max-vol', type=int, default=999999)
    parser.add_argument('start', nargs='?', type=int, default=0)
    parser.add_argument('batch', nargs='?', type=int, default=999)
    args = parser.parse_args()

    if args.reset:
        if PROGRESS_FILE.exists():
            PROGRESS_FILE.unlink()
        print("Progress reset.")

    slugs = load_slugs(args.min_vol, args.max_vol)
    print(f"Loaded {len(slugs)} slugs (vol {args.min_vol}-{args.max_vol})")

    done = set()
    if PROGRESS_FILE.exists():
        try:
            done = set(json.loads(PROGRESS_FILE.read_text()))
        except:
            done = set()

    remaining = [s for s in slugs if s not in done]
    print(f"{len(done)} already done, {len(remaining)} remaining\n")

    if not remaining:
        print("All pages already processed!")
        return

    batch = remaining[args.start:args.start + args.batch]

    success = 0
    failed = []

    for i, slug in enumerate(batch):
        print(f"[{i+1}/{len(batch)}] {slug}")
        try:
            result = process_page(slug)
            print(f"  {result}")
            if result.startswith("OK"):
                success += 1
                done.add(slug)
                PROGRESS_FILE.write_text(json.dumps(sorted(done)))
        except Exception as e:
            msg = f"FAIL {slug}: {e}"
            print(f"  {msg}")
            traceback.print_exc()
            failed.append(msg)

    print(f"\n{'='*60}")
    print(f"DONE: {success} succeeded, {len(failed)} failed of {len(batch)}")
    if failed:
        print(f"\nFailed:")
        for f in failed:
            print(f"  {f}")


if __name__ == "__main__":
    main()
