#!/usr/bin/env python3
"""
Compare pages SEO fix script — handles fixes 2-8 from the audit:
  2. Fix dateModified mismatch between JSON-LD and meta tags
  3. Add internal links to pages missing them
  4. Generate 301 redirects for reverse slugs
  5. Shorten title tags to <60 chars
  6. Add width/height to all images
  7. Extract inline CSS to shared external file
  8. Fix 22 pages with duplicate IDs
"""

import os
import re
import json
import glob
import sys
from pathlib import Path
from datetime import datetime

BASE = Path("/Users/bjh/Documents/tabiji")
COMPARE_DIR = BASE / "compare"
INVENTORY_PATH = COMPARE_DIR / "inventory.json"

# ──────────────────────────────────────────────────────────
# Fix 2: Sync dateModified between JSON-LD and meta tags
# ──────────────────────────────────────────────────────────
def fix_date_modified(html, filepath):
    """Make JSON-LD dateModified match meta article:modified_time"""
    changes = 0

    # Extract meta article:modified_time
    meta_match = re.search(
        r'<meta\s+content="(\d{4}-\d{2}-\d{2})T[^"]*"\s+property="article:modified_time"',
        html
    )
    if not meta_match:
        return html, changes

    meta_date = meta_match.group(1)

    # Fix JSON-LD Article dateModified to match
    def replace_jsonld_date(m):
        nonlocal changes
        block = m.group(0)
        if '"Article"' in block:
            old_block = block
            block = re.sub(
                r'"dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})"',
                f'"dateModified": "{meta_date}"',
                block
            )
            if block != old_block:
                changes += 1
        return block

    html = re.sub(
        r'<script type="application/ld\+json">\{[^}]*"@type"\s*:\s*"Article"[^<]*\}</script>',
        replace_jsonld_date,
        html,
        flags=re.DOTALL
    )

    return html, changes


# ──────────────────────────────────────────────────────────
# Fix 3: Add internal links to pages missing them
# ──────────────────────────────────────────────────────────
def load_inventory():
    """Load inventory.json and build lookup structures"""
    with open(INVENTORY_PATH) as f:
        data = json.load(f)
    cards = data.get("cards", data) if isinstance(data, dict) else data
    slug_map = {}
    cluster_map = {}  # cluster -> list of slugs
    for card in cards:
        slug = card.get("slug", "")
        slug_map[slug] = card
        cluster = card.get("cluster", "")
        if cluster:
            cluster_map.setdefault(cluster, []).append(slug)
    return slug_map, cluster_map


def find_related_slugs(slug, slug_map, cluster_map):
    """Find related slugs for a page from inventory relatedSlugs or cluster"""
    card = slug_map.get(slug, {})
    related = card.get("relatedSlugs", [])

    # If we have relatedSlugs, use them
    if related:
        # Verify they exist
        valid = [s for s in related if os.path.isdir(COMPARE_DIR / s)]
        if len(valid) >= 4:
            return valid[:6]

    # Fallback: find pages in same cluster
    cluster = card.get("cluster", "")
    if cluster and cluster in cluster_map:
        candidates = [s for s in cluster_map[cluster] if s != slug and os.path.isdir(COMPARE_DIR / s)]
        if candidates:
            return candidates[:6]

    # Fallback: find pages sharing a destination name
    parts = slug.split("-vs-")
    if len(parts) == 2:
        d1, d2 = parts
        candidates = set()
        for other_slug in slug_map:
            if other_slug == slug:
                continue
            if d1 in other_slug or d2 in other_slug:
                if os.path.isdir(COMPARE_DIR / other_slug):
                    candidates.add(other_slug)
            if len(candidates) >= 6:
                break
        if candidates:
            return list(candidates)[:6]

    return []


def slug_to_title(slug):
    """Convert slug like 'tokyo-vs-kyoto' to 'Tokyo vs Kyoto'"""
    parts = slug.split("-vs-")
    if len(parts) == 2:
        def titleize(s):
            return " ".join(w.capitalize() for w in s.split("-"))
        return f"{titleize(parts[0])} vs {titleize(parts[1])}"
    return slug.replace("-", " ").title()


def has_internal_compare_links(html):
    """Check if page already has related compare links"""
    # Look for related links section or multiple compare links
    if 'ux-related-links' in html:
        return True
    if 'Related Guides' in html and '/compare/' in html:
        # Check if there are actual compare links in a related section
        count = len(re.findall(r'href="/compare/[^"]+/"', html))
        # Every page has at least breadcrumb link; check for more than the hub link
        return count > 5
    # Check for "More X Comparisons" sections
    if re.search(r'More \w+ Comparisons', html):
        return True
    return False


def inject_related_links(html, slug, slug_map, cluster_map):
    """Inject related comparisons section before the footer"""
    changes = 0

    if has_internal_compare_links(html):
        return html, changes

    related = find_related_slugs(slug, slug_map, cluster_map)
    if not related:
        return html, changes

    # Build the related links HTML
    links_html = []
    for rs in related:
        title = slug_to_title(rs)
        links_html.append(f'<li><a href="/compare/{rs}/">{title}</a></li>')

    section = f'''<section class="ux-related-links">
<h2>Related Comparisons</h2>
<ul>
{"".join(links_html)}
</ul>
</section>
'''

    # Insert before the footer
    footer_marker = '<!-- @include:footer:start -->'
    if footer_marker in html:
        html = html.replace(footer_marker, section + footer_marker)
        changes = 1

    return html, changes


# ──────────────────────────────────────────────────────────
# Fix 5: Shorten title tags to <60 chars
# ──────────────────────────────────────────────────────────
def shorten_title(html, filepath):
    """Remove ' | tabiji.ai' from title tags to keep under 60 chars"""
    changes = 0

    def replace_title(m):
        nonlocal changes
        title = m.group(1)
        if len(title) > 60 and '| tabiji.ai' in title:
            new_title = title.replace(' | tabiji.ai', '')
            changes += 1
            return f'<title>{new_title}</title>'
        return m.group(0)

    html = re.sub(r'<title>([^<]+)</title>', replace_title, html)
    return html, changes


# ──────────────────────────────────────────────────────────
# Fix 6: Add width/height to all images
# ──────────────────────────────────────────────────────────
def add_image_dimensions(html, filepath):
    """Add width and height attributes to img tags missing them"""
    changes = 0

    def add_dims(m):
        nonlocal changes
        tag = m.group(0)

        # Skip if already has width/height
        if 'width=' in tag or 'height=' in tag:
            return tag

        # Determine dimensions based on context
        if 'owl-logo' in tag or 'logo' in tag.lower():
            return tag  # Skip logo images — they have inline styles

        # Hero images (og:image referenced ones tend to be larger)
        if 'photo-grid' in html[max(0, m.start()-200):m.start()]:
            w, h = 600, 400
        elif 'hero' in html[max(0, m.start()-500):m.start()]:
            w, h = 800, 500
        else:
            w, h = 800, 500

        # Insert before the closing >
        tag = tag.rstrip('>')
        if tag.endswith('/'):
            tag = tag.rstrip('/')
            tag = f'{tag} width="{w}" height="{h}" />'
        else:
            tag = f'{tag} width="{w}" height="{h}">'

        changes += 1
        return tag

    # Match img tags that don't already have width/height
    html = re.sub(r'<img\s[^>]*>', add_dims, html)
    return html, changes


# ──────────────────────────────────────────────────────────
# Fix 7: Extract inline CSS to shared external file
# ──────────────────────────────────────────────────────────
CSS_FILE = BASE / "assets" / "compare-shared.css"

def extract_inline_css(html, filepath):
    """Replace large inline <style> blocks with link to shared CSS file"""
    changes = 0

    # Find the main inline style block — starts with <style> containing :root
    # and ends with </style> before the shared-head include
    pattern = r'<style>\s*\n?\s*:root\s*\{.*?</style>'
    match = re.search(pattern, html, re.DOTALL)

    if not match:
        return html, changes

    css_link = '<link rel="stylesheet" href="/assets/compare-shared.css">'

    if 'compare-shared.css' not in html:
        # Extract any page-specific CSS (destination colors) before replacing
        block = match.group(0)
        # Check for page-specific dest color overrides like --dest1-color
        specific_css = []
        for line in block.split('\n'):
            stripped = line.strip()
            # Keep destination-specific emoji overrides in list-item::before
            if '::before' in stripped and 'content:' in stripped:
                if any(emoji in stripped for emoji in ['🏙', '⛩', '🌴', '🏔', '🏖', '🌆', '🌇', '🏛', '🌊', '🏜', '🗼', '🌺']):
                    specific_css.append(stripped)

        replacement = css_link
        if specific_css:
            replacement = css_link + '\n<style>\n' + '\n'.join(specific_css) + '\n</style>'

        html = html[:match.start()] + replacement + html[match.end():]
        changes += 1
    else:
        # Already has the link, just remove the inline block
        html = html[:match.start()] + html[match.end():]
        changes += 1

    return html, changes


def generate_shared_css():
    """Extract the common CSS from a sample page and save to shared file"""
    sample = COMPARE_DIR / "tokyo-vs-kyoto" / "index.html"
    with open(sample) as f:
        content = f.read()

    # Extract full style block
    match = re.search(r'<style>\s*\n?\s*(:root\s*\{.*?)</style>', content, re.DOTALL)
    if not match:
        print("ERROR: Could not extract CSS from sample page")
        return

    css = match.group(1)

    # Deduplicate viator CSS — keep only the first occurrence
    viator_block = re.search(
        r'(\.viator-section\s*\{.*?\.viator-powered\s*\{[^}]+\})',
        css, re.DOTALL
    )
    if viator_block:
        first_viator = viator_block.group(1)
        # Remove all viator blocks then add one back
        css_no_viator = re.sub(
            r'\s*\.viator-section\s*\{.*?\.viator-powered\s*\{[^}]+\}',
            '', css, flags=re.DOTALL
        )
        css = css_no_viator.rstrip() + '\n\n      ' + first_viator + '\n'

    css_content = f"""/* ══════════════════════════════════════════════════════════
   Compare Page — Shared CSS
   Extracted from inline styles for caching across 1300+ pages.
   Loaded via <link> for browser caching benefit.
   ══════════════════════════════════════════════════════════ */

{css}
"""

    with open(CSS_FILE, 'w') as f:
        f.write(css_content)
    print(f"  Generated shared CSS: {CSS_FILE} ({len(css_content)} bytes)")


# ──────────────────────────────────────────────────────────
# Fix 8: Fix duplicate IDs
# ──────────────────────────────────────────────────────────
DUPLICATE_ID_PAGES = [
    "buenos-aires-vs-santiago",
    "cape-town-vs-marrakech",
    "copenhagen-vs-stockholm",
    "goa-vs-kerala",
    "greece-vs-turkey",
    "gyeongju-vs-andong",
    "hampi-vs-varanasi",
    "hong-kong-vs-singapore",
    "india-vs-nepal",
    "istanbul-vs-cairo",
    "jaipur-vs-udaipur",
    "jordan-vs-egypt",
    "kochi-vs-munnar",
    "kota-kinabalu-vs-kuching",
    "lisbon-vs-barcelona",
    "malacca-vs-george-town",
    "morocco-vs-jordan",
    "prague-vs-budapest",
    "rishikesh-vs-dharamsala",
    "shirakawa-go-vs-takayama",
    "taipei-vs-hong-kong",
    "zanzibar-vs-mauritius",
]


def fix_duplicate_ids(html, filepath):
    """Fix duplicate id='the-decision-framework' by renaming the second occurrence"""
    changes = 0

    occurrences = list(re.finditer(r'id="the-decision-framework"', html))
    if len(occurrences) > 1:
        # Rename second (and subsequent) occurrences
        for i, match in enumerate(occurrences[1:], 2):
            new_id = f'id="the-decision-framework-{i}"'
            html = html[:match.start()] + new_id + html[match.end():]
            changes += 1

        # Also fix any TOC links that might point to the duplicate
        # Update the second TOC link if it exists
        toc_links = list(re.finditer(r'href="#the-decision-framework"', html))
        if len(toc_links) > 1:
            for i, match in enumerate(toc_links[1:], 2):
                new_href = f'href="#the-decision-framework-{i}"'
                html = html[:match.start()] + new_href + html[match.end():]

    return html, changes


# ──────────────────────────────────────────────────────────
# Fix 4: Generate reverse slug redirects
# ──────────────────────────────────────────────────────────
def generate_reverse_redirects():
    """Create redirect pages for reverse-order slugs"""
    created = 0
    existing_slugs = set()

    for d in os.listdir(COMPARE_DIR):
        if os.path.isdir(COMPARE_DIR / d) and '-vs-' in d:
            existing_slugs.add(d)

    for slug in list(existing_slugs):
        parts = slug.split("-vs-")
        if len(parts) != 2:
            continue

        reverse = f"{parts[1]}-vs-{parts[0]}"
        if reverse in existing_slugs:
            continue  # Both directions already exist

        # Create redirect page
        redirect_dir = COMPARE_DIR / reverse
        redirect_dir.mkdir(exist_ok=True)

        canonical = f"https://tabiji.ai/compare/{slug}/"
        title = slug_to_title(reverse)

        redirect_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=/compare/{slug}/">
<link rel="canonical" href="{canonical}">
<title>{title} | tabiji.ai</title>
<meta name="robots" content="noindex, follow">
<script>window.location.replace("/compare/{slug}/");</script>
</head>
<body>
<p>Redirecting to <a href="/compare/{slug}/">{slug_to_title(slug)}</a>...</p>
</body>
</html>'''

        with open(redirect_dir / "index.html", 'w') as f:
            f.write(redirect_html)
        created += 1

    print(f"  Created {created} reverse-slug redirect pages")
    return created


# ──────────────────────────────────────────────────────────
# Main runner
# ──────────────────────────────────────────────────────────
def main():
    fixes = sys.argv[1:] if len(sys.argv) > 1 else ['2', '3', '4', '5', '6', '7', '8']

    print(f"Running fixes: {', '.join(fixes)}")
    print(f"Compare directory: {COMPARE_DIR}")

    # Pre-load inventory for fix 3
    slug_map, cluster_map = {}, {}
    if '3' in fixes:
        print("\nLoading inventory.json...")
        slug_map, cluster_map = load_inventory()
        print(f"  Loaded {len(slug_map)} cards, {len(cluster_map)} clusters")

    # Generate shared CSS file first (fix 7)
    if '7' in fixes:
        print("\n[Fix 7] Generating shared CSS file...")
        generate_shared_css()

    # Generate reverse redirects (fix 4)
    if '4' in fixes:
        print("\n[Fix 4] Generating reverse slug redirects...")
        generate_reverse_redirects()

    # Process all compare pages
    compare_dirs = sorted([
        d for d in os.listdir(COMPARE_DIR)
        if os.path.isdir(COMPARE_DIR / d) and '-vs-' in d
    ])

    print(f"\nProcessing {len(compare_dirs)} compare pages...")

    stats = {f: 0 for f in ['2', '3', '5', '6', '7', '8']}
    errors = []

    for i, slug in enumerate(compare_dirs):
        filepath = COMPARE_DIR / slug / "index.html"
        if not filepath.exists():
            continue

        # Skip redirect pages (they have meta refresh)
        try:
            with open(filepath) as f:
                html = f.read()
        except Exception as e:
            errors.append(f"{slug}: {e}")
            continue

        if 'http-equiv="refresh"' in html:
            continue  # This is a redirect page

        original = html
        page_changes = {}

        # Fix 2: dateModified mismatch
        if '2' in fixes:
            html, n = fix_date_modified(html, filepath)
            if n:
                page_changes['2'] = n
                stats['2'] += n

        # Fix 3: Add internal links
        if '3' in fixes:
            html, n = inject_related_links(html, slug, slug_map, cluster_map)
            if n:
                page_changes['3'] = n
                stats['3'] += n

        # Fix 5: Shorten titles
        if '5' in fixes:
            html, n = shorten_title(html, filepath)
            if n:
                page_changes['5'] = n
                stats['5'] += n

        # Fix 6: Image dimensions
        if '6' in fixes:
            html, n = add_image_dimensions(html, filepath)
            if n:
                page_changes['6'] = n
                stats['6'] += n

        # Fix 7: Extract inline CSS
        if '7' in fixes:
            html, n = extract_inline_css(html, filepath)
            if n:
                page_changes['7'] = n
                stats['7'] += n

        # Fix 8: Duplicate IDs
        if '8' in fixes:
            html, n = fix_duplicate_ids(html, filepath)
            if n:
                page_changes['8'] = n
                stats['8'] += n

        # Write back if changed
        if html != original:
            with open(filepath, 'w') as f:
                f.write(html)

        if (i + 1) % 200 == 0:
            print(f"  Processed {i + 1}/{len(compare_dirs)} pages...")

    print(f"\nDone! Processed {len(compare_dirs)} pages.")
    print("\nResults:")
    fix_names = {
        '2': 'dateModified fixes',
        '3': 'internal links added',
        '5': 'titles shortened',
        '6': 'image dimensions added',
        '7': 'CSS externalized',
        '8': 'duplicate IDs fixed',
    }
    for fix_id in sorted(stats):
        if fix_id in fixes:
            print(f"  Fix {fix_id} ({fix_names[fix_id]}): {stats[fix_id]} pages")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors[:10]:
            print(f"  {e}")


if __name__ == "__main__":
    main()
