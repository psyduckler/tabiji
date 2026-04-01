#!/usr/bin/env python3
"""
Fix critical popular-picks issues identified in the 2026-04-01 audit.

Categories:
1. Stub file: istanbul-fish-sandwich-bosphorus (needs regeneration — skip, flag for manual)
2. Missing og:image meta tags (6 articles)
3. Malformed JSON-LD: paris-natural-wine-bars (extra closing brace)
4. Missing JSON-LD Article schema: bruges-beer-bars (V0 template — add schema)
5. Title count mismatches (38 articles — update title/h1/meta/JSON-LD numbers)
"""

import re
import json
import os
import sys

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'popular-picks')

def read_file(slug):
    path = os.path.join(BASE, slug, 'index.html')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(slug, content):
    path = os.path.join(BASE, slug, 'index.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def count_numbered_entries(html):
    """Count numbered entries in the article (restaurant-number spans or numbered h2s)."""
    # V2 pattern: <h2><span class="restaurant-number">N</span>
    v2_entries = re.findall(r'<span class="restaurant-number">(\d+)</span>', html)
    if v2_entries:
        return max(int(n) for n in v2_entries)
    # V1/V0 pattern: <h2>N. Name</h2>
    v1_entries = re.findall(r'<h2[^>]*>(\d+)\.\s', html)
    if v1_entries:
        return max(int(n) for n in v1_entries)
    return 0

def get_title_count(html):
    """Extract the claimed count from <title> tag."""
    m = re.search(r'<title>(\d+)\s+Best', html)
    if m:
        return int(m.group(1))
    return None

def fix_title_count(html, old_count, new_count):
    """Replace old_count with new_count in title, h1, og:title, twitter:title, and JSON-LD headline."""
    old_str = str(old_count)
    new_str = str(new_count)
    changes = 0

    # <title>N Best ... 
    html, n = re.subn(
        rf'(<title>){old_str}(\s+Best)',
        rf'\g<1>{new_str}\2',
        html
    )
    changes += n

    # <h1>N Best ...
    html, n = re.subn(
        rf'(<h1>){old_str}(\s+Best)',
        rf'\g<1>{new_str}\2',
        html
    )
    changes += n

    # og:title content="N Best ...
    html, n = re.subn(
        rf'(og:title"\s+content="){old_str}(\s+Best)',
        rf'\g<1>{new_str}\2',
        html
    )
    changes += n

    # twitter:title content="N Best ...
    html, n = re.subn(
        rf'(twitter:title"\s+content="){old_str}(\s+Best)',
        rf'\g<1>{new_str}\2',
        html
    )
    changes += n

    # JSON-LD "headline": "N Best ...
    html, n = re.subn(
        rf'("headline":\s*"){old_str}(\s+Best)',
        rf'\g<1>{new_str}\2',
        html
    )
    changes += n

    return html, changes

def fix_og_image(html, slug):
    """Add og:image and twitter:image meta tags after og:url if missing."""
    if 'og:image' in html:
        return html, 0

    # Construct image URL from the first entry name
    # Use a generic hero image pattern: https://img.tabiji.ai/popular-picks/{slug}/hero.jpg
    img_url = f"https://img.tabiji.ai/popular-picks/{slug}/hero.jpg"

    og_image_tags = f'''    <meta property="og:image" content="{img_url}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="675">'''

    twitter_image_tag = f'    <meta name="twitter:image" content="{img_url}">'

    # Insert og:image after og:url or og:type
    html_new = re.sub(
        r'(<meta property="og:url"[^>]*>)',
        rf'\1\n{og_image_tags}',
        html,
        count=1
    )
    if html_new == html:
        # Fallback: insert after og:type
        html_new = re.sub(
            r'(<meta property="og:type"[^>]*>)',
            rf'\1\n{og_image_tags}',
            html,
            count=1
        )

    # Insert twitter:image after twitter:description
    html_final = re.sub(
        r'(<meta name="twitter:description"[^>]*>)',
        rf'\1\n{twitter_image_tag}',
        html_new,
        count=1
    )
    if html_final == html_new:
        # Fallback: insert after twitter:title
        html_final = re.sub(
            r'(<meta name="twitter:title"[^>]*>)',
            rf'\1\n{twitter_image_tag}',
            html_new,
            count=1
        )

    # Also add 'image' to JSON-LD Article schema if missing
    if '"@type": "Article"' in html_final or '"@type":"Article"' in html_final:
        # Check if Article JSON-LD has image
        ld_blocks = re.findall(r'(<script type="application/ld\+json">)(.*?)(</script>)', html_final, re.DOTALL)
        for full_match_pre, block, full_match_post in ld_blocks:
            try:
                data = json.loads(block)
                if data.get('@type') == 'Article' and 'image' not in data:
                    # Add image after headline
                    new_block = block.replace(
                        '"headline"',
                        f'"image": "{img_url}",\n  "headline"'
                    )
                    html_final = html_final.replace(block, new_block)
            except json.JSONDecodeError:
                pass

    changed = 1 if html_final != html else 0
    return html_final, changed

def fix_paris_jsonld(html):
    """Fix the malformed JSON-LD in paris-natural-wine-bars (extra closing brace)."""
    # The issue: last item in ItemList ends with }}} instead of }}
    # Find the ItemList JSON-LD block
    ld_blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    for block in ld_blocks:
        try:
            json.loads(block)
        except json.JSONDecodeError:
            # This is the broken block — fix the triple brace
            # The pattern: ..."url":"..."}}} should be ..."url":"..."}}
            fixed_block = re.sub(r'\}\}\}(\s*\])', r'}}\1', block)
            try:
                json.loads(fixed_block)
                html = html.replace(block, fixed_block)
                return html, 1
            except json.JSONDecodeError as e:
                print(f"  WARNING: Fix attempt still invalid: {e}")
                return html, 0
    return html, 0

def fix_bruges_jsonld(html):
    """Add Article JSON-LD schema to bruges-beer-bars (V0 template missing it entirely)."""
    if '"@type":"Article"' in html or '"@type": "Article"' in html:
        return html, 0

    # Extract title and description from existing meta
    title_m = re.search(r'<title>(.*?)</title>', html)
    desc_m = re.search(r'<meta name="description" content="(.*?)"', html)
    url_m = re.search(r'<link rel="canonical" href="(.*?)"', html)

    title = title_m.group(1) if title_m else "Best Beer Bars in Bruges"
    desc = desc_m.group(1) if desc_m else ""
    url = url_m.group(1) if url_m else "https://tabiji.ai/popular-picks/bruges-beer-bars/"

    article_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title.replace(' | tabiji.ai', ''),
        "description": desc,
        "author": {
            "@type": "Organization",
            "name": "tabiji.ai",
            "url": "https://tabiji.ai"
        },
        "publisher": {
            "@type": "Organization",
            "name": "tabiji.ai",
            "url": "https://tabiji.ai"
        },
        "url": url,
        "image": f"https://img.tabiji.ai/popular-picks/bruges-beer-bars/hero.jpg"
    }, indent=2)

    schema_tag = f'    <script type="application/ld+json">{article_schema}</script>'

    # Insert before </head>
    html = html.replace('</head>', f'{schema_tag}\n</head>', 1)
    return html, 1

# ============================================================
# MAIN
# ============================================================

print("=" * 60)
print("Popular Picks Critical Issue Fixer")
print("=" * 60)

total_fixes = 0
fix_log = []

# --- 1. STUB FILE ---
print("\n[1/4] Stub file: istanbul-fish-sandwich-bosphorus")
stub_path = os.path.join(BASE, 'istanbul-fish-sandwich-bosphorus', 'index.html')
if os.path.exists(stub_path):
    content = open(stub_path).read().strip()
    if len(content) < 50:
        print(f"  ⚠️  STUB CONFIRMED (content: '{content[:30]}') — flagged for regeneration")
        fix_log.append("istanbul-fish-sandwich-bosphorus: STUB — needs full regeneration (not auto-fixable)")
    else:
        print(f"  ✅ File looks normal now ({len(content)} bytes)")

# --- 2. MISSING og:image ---
print("\n[2/4] Missing og:image meta tags")
og_image_missing = [
    'antwerp-fashion-shopping',
    'bruges-beer-bars',
    'kyoto-hidden-temples',
    'mexico-city-coffee-shops',
    'porto-wine-bars',
    'tulum-beach-clubs',
]
for slug in og_image_missing:
    html = read_file(slug)
    html, changed = fix_og_image(html, slug)
    if changed:
        write_file(slug, html)
        total_fixes += 1
        fix_log.append(f"{slug}: Added og:image + twitter:image meta tags")
        print(f"  ✅ {slug}: added og:image")
    else:
        print(f"  ⏭️  {slug}: already has og:image")

# --- 3. MALFORMED JSON-LD ---
print("\n[3/4] Malformed JSON-LD fixes")

# paris-natural-wine-bars
html = read_file('paris-natural-wine-bars')
html, changed = fix_paris_jsonld(html)
if changed:
    write_file('paris-natural-wine-bars', html)
    total_fixes += 1
    fix_log.append("paris-natural-wine-bars: Fixed malformed JSON-LD (extra closing brace)")
    print("  ✅ paris-natural-wine-bars: fixed JSON-LD")
else:
    print("  ⏭️  paris-natural-wine-bars: JSON-LD already valid")

# bruges-beer-bars (missing Article schema entirely)
html = read_file('bruges-beer-bars')
html, changed = fix_bruges_jsonld(html)
if changed:
    write_file('bruges-beer-bars', html)
    total_fixes += 1
    fix_log.append("bruges-beer-bars: Added Article JSON-LD schema")
    print("  ✅ bruges-beer-bars: added Article JSON-LD")
else:
    print("  ⏭️  bruges-beer-bars: already has Article JSON-LD")

# --- 4. TITLE COUNT MISMATCHES ---
print("\n[4/4] Title count mismatches")
mismatch_articles = [
    ('amman-mansaf', 11, 10),
    ('andasibe-lemur-lodges', 11, 10),
    ('angkor-night-market-street-food', 12, 11),
    ('antwerp-frites', 10, 8),
    ('banglamphu-pad-thai', 12, 11),
    ('best-coffee-houses-in-vienna', 12, 11),
    ('best-live-music-venues-in-dakar', 10, 9),
    ('best-pizza-naples', 15, 14),
    ('best-thieboudienne-in-dakar', 10, 9),
    ('dubrovnik-cheap-restaurants', 11, 10),
    ('gukje-market-fish-cake', 10, 9),
    ('hakone-ryokan', 12, 11),
    ('jerusalem-falafel', 10, 9),
    ('jongno-kalguksu', 10, 9),
    ('khon-kaen-isaan-food', 12, 11),
    ('kobe-chinatown', 10, 9),
    ('kyoto-hidden-temples', 12, 11),
    ('london-brunch', 12, 11),
    ('london-cheap-eats', 14, 13),
    ('mechelen-day-trip', 10, 8),
    ('monastiraki-souvlaki', 10, 9),
    ('myeongdong-cat-cafes', 10, 9),
    ('nara-mochi', 10, 9),
    ('osaka-street-food', 15, 14),
    ('paris-cheap-eats', 14, 13),
    ('phnom-penh-rooftop-bars', 8, 7),
    ('poblacion-makati-sinigang', 12, 11),
    ('port-louis-street-food', 11, 10),
    ('porto-wine-bars', 12, 11),
    ('rovinj-seafood', 11, 10),
    ('seoul-buddhist-temple-stays', 5, 4),
    ('split-beach-bars', 11, 10),
    ('taipei-beef-noodle-soup', 12, 11),
    ('tulum-beach-clubs', 12, 11),
    ('vienna-heurigen', 11, 10),
    ('vienna-schnitzel', 11, 10),
    ('wadi-rum-desert-camps', 12, 11),
    ('yangon-tea-houses', 8, 7),
]

for slug, claimed, actual in mismatch_articles:
    html = read_file(slug)
    # Verify the actual count matches
    real_count = count_numbered_entries(html)
    if real_count != actual:
        print(f"  ⚠️  {slug}: expected {actual} entries but found {real_count} — using {real_count}")
        actual = real_count

    html, changes = fix_title_count(html, claimed, actual)
    if changes > 0:
        write_file(slug, html)
        total_fixes += 1
        fix_log.append(f"{slug}: Updated count {claimed} → {actual} in {changes} places")
        print(f"  ✅ {slug}: {claimed} → {actual} ({changes} replacements)")
    else:
        print(f"  ⏭️  {slug}: no changes needed (count may already be correct)")

# --- SUMMARY ---
print("\n" + "=" * 60)
print(f"DONE — {total_fixes} articles fixed")
print("=" * 60)

# Write fix log
log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output', 'fix-log.txt')
os.makedirs(os.path.dirname(log_path), exist_ok=True)
with open(log_path, 'w') as f:
    f.write("Popular Picks Critical Fix Log — 2026-04-01\n")
    f.write("=" * 50 + "\n\n")
    for entry in fix_log:
        f.write(f"- {entry}\n")
    f.write(f"\nTotal: {total_fixes} articles modified\n")

print(f"\nFix log written to: {log_path}")
