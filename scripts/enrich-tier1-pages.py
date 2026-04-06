#!/usr/bin/env python3
"""
Audit, fix, and enrich Tier 1 compare pages with:
1. Fix empty canonical URLs
2. Fix empty og:url
3. Remove sports quotes
4. Add sample itineraries (generated from destination knowledge)
5. Add internal links (compare pages + popular picks)

Usage:
    python3 scripts/enrich-tier1-pages.py
"""
import json, re, os, html as html_mod
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
COMPARE_DIR = REPO / "compare"

# ─── Load target slugs ───
with open('/tmp/tier1_remaining.json') as f:
    TARGET_SLUGS = json.load(f)

# ─── Build index of all compare + popular-picks pages ───
ALL_COMPARES = sorted([
    d for d in os.listdir(COMPARE_DIR)
    if '-vs-' in d and (COMPARE_DIR / d / "index.html").is_file()
])

PP_DIR = REPO / "popular-picks"
ALL_PICKS = sorted([
    d for d in os.listdir(PP_DIR)
    if (PP_DIR / d / "index.html").is_file()
]) if PP_DIR.is_dir() else []


def extract_dests(html):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if not m: return None, None
    raw = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    vm = re.match(r'^(.+?)\s+vs\.?\s+(.+?)(?:\s*[:—–\-].+)?$', raw, re.I)
    if vm: return vm.group(1).strip(), vm.group(2).strip()
    return None, None


def find_related_compares(slug, dest1, dest2, limit=6):
    d1_words = [w for w in slug.split('-vs-')[0].split('-') if len(w) > 3]
    d2_words = [w for w in slug.split('-vs-')[1].split('-') if len(w) > 3]
    related = []
    for c in ALL_COMPARES:
        if c == slug: continue
        cl = c.lower()
        if any(w in cl for w in d1_words) or any(w in cl for w in d2_words):
            related.append(c)
    return related[:limit]


def find_related_picks(slug, dest1, dest2, limit=8):
    d1_words = [w for w in dest1.lower().split() if len(w) > 3]
    d2_words = [w for w in dest2.lower().split() if len(w) > 3]
    # Also use slug parts
    d1_slug_words = [w for w in slug.split('-vs-')[0].split('-') if len(w) > 3]
    d2_slug_words = [w for w in slug.split('-vs-')[1].split('-') if len(w) > 3]
    all_words = set(d1_words + d2_words + d1_slug_words + d2_slug_words)

    related = []
    for p in ALL_PICKS:
        pl = p.lower()
        if any(w in pl for w in all_words):
            related.append(p)
    return related[:limit]


def slug_to_title(slug):
    return slug.replace('-', ' ').title().replace(' Vs ', ' vs ')


def build_itinerary_html(dest1, dest2, slug, deep_dive_headings):
    """Generate template-based itineraries from destination names and page content."""

    # Determine what categories the page covers
    has_food = any('food' in h.lower() or 'dining' in h.lower() or 'drink' in h.lower() for h in deep_dive_headings)
    has_beach = any('beach' in h.lower() or 'coast' in h.lower() or 'water' in h.lower() for h in deep_dive_headings)
    has_nature = any('nature' in h.lower() or 'outdoor' in h.lower() or 'scenery' in h.lower() or 'hiking' in h.lower() for h in deep_dive_headings)
    has_culture = any('culture' in h.lower() or 'history' in h.lower() or 'art' in h.lower() or 'architecture' in h.lower() for h in deep_dive_headings)
    has_nightlife = any('nightlife' in h.lower() or 'entertainment' in h.lower() for h in deep_dive_headings)

    # Find related picks for inline links
    picks = find_related_picks(slug, dest1, dest2, 4)
    d1_picks = [p for p in picks if any(w in p for w in dest1.lower().split() if len(w) > 3)]
    d2_picks = [p for p in picks if any(w in p for w in dest2.lower().split() if len(w) > 3)]

    def pick_link(picks_list, idx=0):
        if idx < len(picks_list):
            title = slug_to_title(picks_list[idx])
            return f' Check out our <a href="/popular-picks/{picks_list[idx]}/">{title}</a> guide.'
        return ''

    # Build activity descriptions based on page content
    d1_activities = []
    d2_activities = []

    if has_culture:
        d1_activities.append(f"Explore the top cultural attractions and historic landmarks of {dest1}.")
        d2_activities.append(f"Visit the key museums, monuments, and cultural sites of {dest2}.")
    if has_food:
        d1_activities.append(f"Sample local cuisine and signature dishes.{pick_link(d1_picks, 0)}")
        d2_activities.append(f"Dive into the local food scene and must-try specialties.{pick_link(d2_picks, 0)}")
    if has_beach:
        d1_activities.append(f"Enjoy the best beaches and waterfront areas.")
        d2_activities.append(f"Hit the top beaches and coastal spots.")
    if has_nature:
        d1_activities.append(f"Take in the natural scenery and outdoor activities.")
        d2_activities.append(f"Explore the natural landscapes and hiking trails.")
    if has_nightlife:
        d1_activities.append(f"Experience the nightlife and entertainment scene.")
        d2_activities.append(f"Check out the bars, clubs, and evening entertainment.")

    # Ensure we have at least 3 activities per dest
    while len(d1_activities) < 3:
        d1_activities.append(f"Wander the neighborhoods and soak up the local atmosphere.")
    while len(d2_activities) < 3:
        d2_activities.append(f"Get lost in the streets and discover hidden gems.")

    # Find related compares for "do both" suggestion
    related = find_related_compares(slug, dest1, dest2, 2)
    both_link = ''
    if related:
        both_link = f' Also consider <a href="/compare/{related[0]}/">{slug_to_title(related[0])}</a>.'

    itineraries = f'''<div class="ux-itineraries" id="sample-itineraries">
<h2>&#128197; Sample Itineraries</h2>
<div class="ux-itin-tabs">
<button class="ux-itin-tab active" data-panel="itin-0">3 Days {dest1}</button>
<button class="ux-itin-tab" data-panel="itin-1">3 Days {dest2}</button>
<button class="ux-itin-tab" data-panel="itin-2">7 Days {dest1}</button>
<button class="ux-itin-tab" data-panel="itin-3">7 Days {dest2}</button>
</div>
<div class="ux-itin-panel active" id="itin-0"><div class="ux-itin-card"><h3>Weekend in {dest1} (3 Days)</h3>
<div class="ux-itin-day"><span class="day-num">Day 1</span><span class="day-desc">Arrive and get oriented. {d1_activities[0]}</span></div>
<div class="ux-itin-day"><span class="day-num">Day 2</span><span class="day-desc">{d1_activities[1]}</span></div>
<div class="ux-itin-day"><span class="day-num">Day 3</span><span class="day-desc">{d1_activities[2]} Consider a day trip to see the surrounding area before departure.</span></div>
<p class="ux-itin-tip">&#128161; Three days gives you a solid taste of {dest1}. Focus on the highlights and save the deeper exploration for a longer trip.</p>
</div></div>
<div class="ux-itin-panel" id="itin-1"><div class="ux-itin-card"><h3>Weekend in {dest2} (3 Days)</h3>
<div class="ux-itin-day"><span class="day-num">Day 1</span><span class="day-desc">Settle in and explore the main area. {d2_activities[0]}</span></div>
<div class="ux-itin-day"><span class="day-num">Day 2</span><span class="day-desc">{d2_activities[1]}</span></div>
<div class="ux-itin-day"><span class="day-num">Day 3</span><span class="day-desc">{d2_activities[2]} Wrap up with a memorable final meal.</span></div>
<p class="ux-itin-tip">&#128161; A long weekend in {dest2} covers the essentials. Book key attractions in advance to avoid queues.</p>
</div></div>
<div class="ux-itin-panel" id="itin-2"><div class="ux-itin-card"><h3>Week in {dest1} (7 Days)</h3>
<div class="ux-itin-day"><span class="day-num">Days 1&ndash;2</span><span class="day-desc">{d1_activities[0]} {d1_activities[1]}</span></div>
<div class="ux-itin-day"><span class="day-num">Days 3&ndash;4</span><span class="day-desc">{d1_activities[2]} Take a day trip to explore nearby destinations.{both_link}</span></div>
<div class="ux-itin-day"><span class="day-num">Days 5&ndash;6</span><span class="day-desc">Go deeper into the neighborhoods and local life. Revisit favorite spots and discover areas off the tourist trail.{pick_link(d1_picks, 1)}</span></div>
<div class="ux-itin-day"><span class="day-num">Day 7</span><span class="day-desc">Final explorations and departure. Pick up any souvenirs and enjoy one last local meal.</span></div>
<p class="ux-itin-tip">&#128161; A full week lets you move at a relaxed pace and truly get to know {dest1} beyond the highlights.</p>
</div></div>
<div class="ux-itin-panel" id="itin-3"><div class="ux-itin-card"><h3>Week in {dest2} (7 Days)</h3>
<div class="ux-itin-day"><span class="day-num">Days 1&ndash;2</span><span class="day-desc">{d2_activities[0]} {d2_activities[1]}</span></div>
<div class="ux-itin-day"><span class="day-num">Days 3&ndash;4</span><span class="day-desc">{d2_activities[2]} Venture out on a day trip to a nearby town or natural attraction.</span></div>
<div class="ux-itin-day"><span class="day-num">Days 5&ndash;6</span><span class="day-desc">Slow down and live like a local. Explore the residential neighborhoods, visit local markets, and find your favorite caf&eacute; or restaurant.{pick_link(d2_picks, 1)}</span></div>
<div class="ux-itin-day"><span class="day-num">Day 7</span><span class="day-desc">Last-day highlights and departure. Revisit your favorite spot one more time.</span></div>
<p class="ux-itin-tip">&#128161; With 7 days you can combine {dest2} with nearby destinations for the ultimate trip.</p>
</div></div>
</div>
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

    return itineraries


def build_links_html(slug, dest1, dest2):
    related_compares = find_related_compares(slug, dest1, dest2, 6)
    related_picks = find_related_picks(slug, dest1, dest2, 8)

    if not related_compares and not related_picks:
        return ''

    groups = []

    # Split compares by destination
    d1_slug = slug.split('-vs-')[0]
    d2_slug = slug.split('-vs-')[1]
    d1_compares = [c for c in related_compares if d1_slug in c][:3]
    d2_compares = [c for c in related_compares if d2_slug in c and c not in d1_compares][:3]

    if d1_compares:
        items = ''.join(f'<li><a href="/compare/{c}/">&rarr; {slug_to_title(c)}</a></li>' for c in d1_compares)
        groups.append(f'<h3 style="font-size:0.92rem;margin:0.5rem 0 0.3rem;color:var(--indigo,#2D3A5C)">More {dest1} Comparisons</h3><ul>{items}</ul>')

    if d2_compares:
        items = ''.join(f'<li><a href="/compare/{c}/">&rarr; {slug_to_title(c)}</a></li>' for c in d2_compares)
        groups.append(f'<h3 style="font-size:0.92rem;margin:0.5rem 0 0.3rem;color:var(--indigo,#2D3A5C)">More {dest2} Comparisons</h3><ul>{items}</ul>')

    if related_picks:
        items = ''.join(f'<li><a href="/popular-picks/{p}/">&rarr; {slug_to_title(p)}</a></li>' for p in related_picks)
        groups.append(f'<h3 style="font-size:0.92rem;margin:0.5rem 0 0.3rem;color:var(--indigo,#2D3A5C)">Destination Guides</h3><ul>{items}</ul>')

    if not groups:
        return ''

    return f'''<div class="ux-related-links">
<h2>&#128279; Related Guides &amp; Comparisons</h2>
{''.join(groups)}
</div>'''


def process_page(slug):
    path = COMPARE_DIR / slug / "index.html"
    html = path.read_text('utf-8')
    fixes = []

    dest1, dest2 = extract_dests(html)
    if not dest1 or not dest2:
        return f"SKIP {slug}: cannot extract destinations"

    # ─── FIX 1: Empty canonical URL ───
    canonical_url = f"https://tabiji.ai/compare/{slug}/"
    if re.search(r'<link[^>]*rel="canonical"[^>]*href=""', html):
        html = re.sub(
            r'(<link[^>]*rel="canonical"[^>]*href=)"(")',
            rf'\1"{canonical_url}"',
            html
        )
        fixes.append('fixed_canonical')

    # ─── FIX 2: Empty og:url ───
    if re.search(r'property="og:url"[^>]*content=""', html) or re.search(r'content=""[^>]*property="og:url"', html):
        html = re.sub(
            r'(<meta[^>]*property="og:url"[^>]*content=)"(")',
            rf'\1"{canonical_url}"',
            html
        )
        fixes.append('fixed_og_url')

    # ─── FIX 3: Remove sports quotes ───
    sports_removed = 0
    def remove_sports(m):
        nonlocal sports_removed
        if re.search(r'Goal!|⚽.*\d+[\'′]|match thread', m.group(0), re.I):
            sports_removed += 1
            return ''
        return m.group(0)
    html = re.sub(r'<(?:div|blockquote)\s+class="reddit-quote"[^>]*>.*?</(?:div|blockquote)>', remove_sports, html, flags=re.DOTALL)
    if sports_removed:
        fixes.append(f'removed_{sports_removed}_sports_quotes')

    # ─── ENRICH: Add itineraries + links before FAQ ───
    if 'ux-itineraries' not in html:
        # Get deep dive headings for context
        headings = [re.sub(r'<[^>]+>', '', h).strip() for h in re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.DOTALL)]

        itin_html = build_itinerary_html(dest1, dest2, slug, headings)
        links_html = build_links_html(slug, dest1, dest2)
        inject = f'\n{itin_html}\n{links_html}\n'

        if '<section class="faq-section"' in html:
            html = html.replace('<section class="faq-section"', inject + '<section class="faq-section"')
            fixes.append('added_itineraries')
            fixes.append('added_internal_links')
        elif '<div class="cta-section"' in html:
            html = html.replace('<div class="cta-section"', inject + '<div class="cta-section"')
            fixes.append('added_itineraries')
            fixes.append('added_internal_links')
        else:
            fixes.append('WARN:no_injection_point')

    path.write_text(html, 'utf-8')
    return f"OK   {slug}: {', '.join(fixes) if fixes else 'no changes'}"


# ─── Main ───
def main():
    print(f"Processing {len(TARGET_SLUGS)} pages...")
    print()

    success = 0
    errors = []
    for i, slug in enumerate(TARGET_SLUGS):
        try:
            result = process_page(slug)
            print(f"[{i+1:3d}/{len(TARGET_SLUGS)}] {result}")
            if result.startswith('OK'):
                success += 1
            else:
                errors.append(result)
        except Exception as e:
            err = f"FAIL {slug}: {e}"
            print(f"[{i+1:3d}/{len(TARGET_SLUGS)}] {err}")
            errors.append(err)

    print(f"\nDone: {success} OK, {len(errors)} issues")
    if errors:
        print("\nIssues:")
        for e in errors:
            print(f"  {e}")


if __name__ == "__main__":
    main()
