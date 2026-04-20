#!/usr/bin/env python3
"""
Fix minor popular-picks issues identified in the 2026-04-01 audit.

Categories:
1. Empty ItemList JSON-LD (528 articles) — populate with entry names from article body
2. Competitor links (9 occurrences in 8 articles) — remove TripAdvisor/Yelp/Booking links
3. JSON-LD Article missing 'image' (1 remaining: kobe-beef) — add image field
4. Test/placeholder directories (slug, test) — delete
"""

import re
import json
import os
import sys
import shutil
import html as html_module

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'popular-picks')

def read_file(slug):
    path = os.path.join(BASE, slug, 'index.html')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(slug, content):
    path = os.path.join(BASE, slug, 'index.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def extract_entries_rank_pattern(html):
    """Extract entries from restaurant-rank pattern: <div class="restaurant-rank">#N</div> ... <h2>Name</h2>"""
    entries = re.findall(
        r'<div class="restaurant-rank">#(\d+)</div>\s*<div>\s*<h2>(.*?)</h2>',
        html
    )
    return [(int(n), html_module.unescape(name.strip())) for n, name in entries]

def extract_entries_number_pattern(html):
    """Extract entries from restaurant-number pattern: <span class="restaurant-number">N</span>Name</h2>"""
    entries = re.findall(
        r'<span class="restaurant-number">(\d+)</span>(.*?)</h2>',
        html
    )
    return [(int(n), html_module.unescape(name.strip())) for n, name in entries]

def extract_section_ids(html):
    """Extract section/element IDs that correspond to entries."""
    # Match both <section ...id="..."> and standalone id= near restaurant entries
    ids = re.findall(r'<section[^>]*\bid="([^"]+)"', html)
    if not ids:
        # Try div or article patterns
        ids = re.findall(r'<(?:div|article)[^>]*\bid="([^"]+)"', html)
    return ids

def get_canonical_url(html):
    """Extract canonical URL from the page."""
    m = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    return m.group(1) if m else None

def build_itemlist_entries(entries, section_ids, canonical_url):
    """Build ItemList entries from extracted data."""
    items = []
    for i, (pos, name) in enumerate(entries):
        item = {
            "@type": "ListItem",
            "position": pos,
            "name": name
        }
        # Add URL with anchor if we have section IDs
        if i < len(section_ids) and canonical_url:
            item["url"] = f"{canonical_url}#{section_ids[i]}"
        items.append(item)
    return items

def populate_itemlist(html, slug):
    """Populate empty ItemList JSON-LD with entry data from the article body."""
    # Extract entries using appropriate pattern
    entries = extract_entries_rank_pattern(html)
    if not entries:
        entries = extract_entries_number_pattern(html)
    if not entries:
        return html, 0, "no entries found"

    section_ids = extract_section_ids(html)
    canonical_url = get_canonical_url(html)

    # Build the new ItemList entries
    items = build_itemlist_entries(entries, section_ids, canonical_url)

    # Find and replace the empty ItemList JSON-LD block
    ld_blocks = list(re.finditer(
        r'(<script type="application/ld\+json">)(.*?)(</script>)',
        html, re.DOTALL
    ))

    for match in ld_blocks:
        block_text = match.group(2)
        try:
            data = json.loads(block_text)
        except json.JSONDecodeError:
            continue

        if data.get('@type') == 'ItemList' and data.get('numberOfItems', -1) == 0:
            # Update the ItemList
            data['numberOfItems'] = len(items)
            data['itemListElement'] = items

            # Also fix name if it has count mismatch
            if data.get('name'):
                name_match = re.match(r'^(\d+)\s+', data['name'])
                if name_match and int(name_match.group(1)) != len(items):
                    data['name'] = re.sub(r'^\d+', str(len(items)), data['name'])

            # Also populate description and url if empty
            if not data.get('url') and canonical_url:
                data['url'] = canonical_url
            if not data.get('description'):
                desc_match = re.search(r'<meta name="description" content="([^"]*)"', html)
                if desc_match:
                    data['description'] = html_module.unescape(desc_match.group(1))

            new_block = json.dumps(data, indent=2, ensure_ascii=False)
            html = html[:match.start(2)] + new_block + html[match.end(2):]
            return html, 1, f"{len(items)} items"

    return html, 0, "no empty ItemList found"

def remove_competitor_links(html, slug):
    """Remove competitor links (TripAdvisor, Yelp, Booking.com) from article bodies."""
    # Pattern: <a href="https://www.tripadvisor.com/...">Website</a>
    # Replace with just the text content (no link)
    original = html
    html = re.sub(
        r'<a[^>]*href="https?://(?:www\.)?(?:tripadvisor|yelp|booking)\.[^"]*"[^>]*>(.*?)</a>',
        r'\1',
        html
    )
    changes = 1 if html != original else 0
    return html, changes

def fix_jsonld_image(html, slug):
    """Add image field to Article JSON-LD if missing."""
    ld_blocks = list(re.finditer(
        r'(<script type="application/ld\+json">)(.*?)(</script>)',
        html, re.DOTALL
    ))

    for match in ld_blocks:
        block_text = match.group(2)
        try:
            data = json.loads(block_text)
        except json.JSONDecodeError:
            continue

        if data.get('@type') == 'Article' and 'image' not in data:
            img_url = f"https://img.tabiji.ai/popular-picks/{slug}/hero.jpg"
            data['image'] = img_url
            new_block = json.dumps(data, indent=2, ensure_ascii=False)
            html = html[:match.start(2)] + new_block + html[match.end(2):]
            return html, 1

    return html, 0


# ============================================================
# MAIN
# ============================================================

print("=" * 60)
print("Popular Picks Minor Issue Fixer")
print("=" * 60)

total_fixes = 0
fix_log = []
errors = []

# --- 1. EMPTY ITEMLIST JSON-LD (528 articles) ---
print("\n[1/4] Populating empty ItemList JSON-LD schemas...")
empty_count = 0
populated_count = 0
skip_count = 0

for slug in sorted(os.listdir(BASE)):
    path = os.path.join(BASE, slug, 'index.html')
    if not os.path.isfile(path):
        continue

    html = read_file(slug)

    # Check if has empty ItemList
    has_empty = False
    ld_blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    for block in ld_blocks:
        try:
            d = json.loads(block)
            if d.get('@type') == 'ItemList' and d.get('numberOfItems', -1) == 0:
                has_empty = True
                break
        except:
            pass

    if not has_empty:
        continue

    empty_count += 1
    html_new, changed, detail = populate_itemlist(html, slug)
    if changed:
        write_file(slug, html_new)
        populated_count += 1
        fix_log.append(f"{slug}: Populated ItemList JSON-LD ({detail})")
        if populated_count <= 5 or populated_count % 100 == 0:
            print(f"  ✅ {slug}: {detail}")
    else:
        skip_count += 1
        errors.append(f"{slug}: Failed to populate ItemList — {detail}")
        if skip_count <= 5:
            print(f"  ⚠️  {slug}: {detail}")

print(f"\n  Summary: {populated_count}/{empty_count} populated, {skip_count} skipped")
total_fixes += populated_count

# --- 2. COMPETITOR LINKS ---
print("\n[2/4] Removing competitor links...")
competitor_articles = [
    'athens-tavernas', 'chinatown-singapore-chicken-rice', 'essaouira-seafood',
    'gyeongju-craft-beer', 'hanoi-pho', 'hoi-an-banh-mi',
    'mandalay-shan-noodles', 'maun-budget-stays'
]
for slug in competitor_articles:
    try:
        html = read_file(slug)
        html, changed = remove_competitor_links(html, slug)
        if changed:
            write_file(slug, html)
            total_fixes += 1
            fix_log.append(f"{slug}: Removed competitor links (TripAdvisor)")
            print(f"  ✅ {slug}: removed competitor links")
        else:
            print(f"  ⏭️  {slug}: no competitor links found")
    except FileNotFoundError:
        print(f"  ⚠️  {slug}: file not found")

# --- 3. JSON-LD ARTICLE MISSING IMAGE ---
print("\n[3/4] Adding missing image to Article JSON-LD...")
jsonld_image_articles = ['kobe-beef']  # Only one remaining after critical fixes
for slug in jsonld_image_articles:
    try:
        html = read_file(slug)
        html, changed = fix_jsonld_image(html, slug)
        if changed:
            write_file(slug, html)
            total_fixes += 1
            fix_log.append(f"{slug}: Added image to Article JSON-LD")
            print(f"  ✅ {slug}: added image to Article JSON-LD")
        else:
            print(f"  ⏭️  {slug}: already has image in Article JSON-LD")
    except FileNotFoundError:
        print(f"  ⚠️  {slug}: file not found")

# --- 4. TEST/PLACEHOLDER DIRECTORIES ---
print("\n[4/4] Removing test/placeholder directories...")
test_dirs = ['slug', 'test']
for dirname in test_dirs:
    dirpath = os.path.join(BASE, dirname)
    if os.path.isdir(dirpath):
        shutil.rmtree(dirpath)
        total_fixes += 1
        fix_log.append(f"{dirname}/: Removed test/placeholder directory")
        print(f"  ✅ Removed {dirname}/")
    else:
        print(f"  ⏭️  {dirname}/ not found")

# --- SUMMARY ---
print("\n" + "=" * 60)
print(f"DONE — {total_fixes} fixes applied")
print("=" * 60)

if errors:
    print(f"\n⚠️  {len(errors)} warnings:")
    for e in errors[:10]:
        print(f"  - {e}")
    if len(errors) > 10:
        print(f"  ... and {len(errors) - 10} more")

# Write fix log
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output')
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, 'minor-fix-log.txt')
with open(log_path, 'w') as f:
    f.write("Popular Picks Minor Fix Log — 2026-04-01\n")
    f.write("=" * 50 + "\n\n")
    for entry in fix_log:
        f.write(f"- {entry}\n")
    f.write(f"\nTotal: {total_fixes} fixes applied\n")
    if errors:
        f.write(f"\nWarnings ({len(errors)}):\n")
        for e in errors:
            f.write(f"  - {e}\n")

print(f"\nFix log written to: {log_path}")
