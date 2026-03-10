#!/usr/bin/env python3
"""
Google Discover optimization — batch fixes for all tabiji HTML pages.

Fix #1: Add <meta name="robots" content="max-image-preview:large"> to ALL pages
Fix #2: Add og:image + og:image:width + og:image:height to itinerary pages (if hero-bg exists)
Fix #3: Add "image" field to Article JSON-LD schema on itinerary pages (if hero-bg exists)

Also: Add og:image:width + og:image:height to popular-picks pages that already have og:image

Run: python3 scripts/discover-optimize.py [--dry-run]
"""

import os
import re
import sys
import json
from pathlib import Path

DRY_RUN = '--dry-run' in sys.argv
TABIJI_ROOT = Path(__file__).resolve().parent.parent
R2_BASE = "https://img.tabiji.ai"

stats = {
    'fix1_robots_updated': 0,
    'fix1_robots_added': 0,
    'fix2_og_image_added': 0,
    'fix2_og_dimensions_added': 0,
    'fix3_schema_image_added': 0,
    'popular_picks_dimensions_added': 0,
    'skipped_no_hero': 0,
    'files_modified': 0,
    'files_scanned': 0,
    'errors': [],
}


def fix_robots_meta(html):
    """Fix #1: Update or add max-image-preview:large to robots meta tag."""
    changed = False

    # Case 1: Existing robots meta tag — replace it to include max-image-preview:large
    robots_pattern = r'<meta\s+name="robots"\s+content="([^"]*)">'
    match = re.search(robots_pattern, html)
    if match:
        current_content = match.group(1)
        if 'max-image-preview:large' not in current_content:
            new_content = current_content.rstrip(', ') + ', max-image-preview:large'
            new_tag = f'<meta name="robots" content="{new_content}">'
            html = html[:match.start()] + new_tag + html[match.end():]
            changed = True
            stats['fix1_robots_updated'] += 1
    else:
        # Case 2: No robots meta tag — add one after the last <meta> in <head>
        # Find the position right before </head> or after the last meta tag
        head_end = html.find('</head>')
        if head_end != -1:
            insert_tag = '    <meta name="robots" content="index, follow, max-image-preview:large">\n'
            # Try to insert after the last meta tag before </head>
            last_meta = -1
            for m in re.finditer(r'<meta[^>]*>', html[:head_end]):
                last_meta = m.end()
            if last_meta != -1:
                html = html[:last_meta] + '\n' + insert_tag + html[last_meta:]
            else:
                html = html[:head_end] + insert_tag + html[head_end:]
            changed = True
            stats['fix1_robots_added'] += 1

    return html, changed


def fix_og_image_itinerary(html, slug):
    """Fix #2: Add og:image for itinerary pages that have hero-bg."""
    changed = False
    image_url = f"{R2_BASE}/i/{slug}/hero-bg.jpg"

    # Only add if page references hero-bg (meaning the image exists on R2)
    if 'hero-bg' not in html:
        stats['skipped_no_hero'] += 1
        return html, changed

    # Check if og:image already exists
    if 'og:image' in html:
        return html, changed

    # Find where to insert — after the last og: meta tag
    og_pattern = r'<meta\s+property="og:[^"]*"[^>]*>'
    last_og_end = -1
    for m in re.finditer(og_pattern, html):
        last_og_end = m.end()

    if last_og_end != -1:
        og_tags = (
            f'\n    <meta property="og:image" content="{image_url}">'
            f'\n    <meta property="og:image:width" content="1200">'
            f'\n    <meta property="og:image:height" content="675">'
        )
        html = html[:last_og_end] + og_tags + html[last_og_end:]
        changed = True
        stats['fix2_og_image_added'] += 1
    
    return html, changed


def fix_og_dimensions_popular_picks(html):
    """Add og:image:width and og:image:height to popular-picks pages that have og:image but no dimensions."""
    changed = False

    if 'og:image"' not in html:
        return html, changed
    if 'og:image:width' in html:
        return html, changed  # already has dimensions

    # Find the og:image tag and insert dimensions after it
    og_image_match = re.search(r'<meta\s+property="og:image"\s+content="[^"]*">', html)
    if og_image_match:
        insert_pos = og_image_match.end()
        dim_tags = (
            '\n    <meta property="og:image:width" content="1200">'
            '\n    <meta property="og:image:height" content="675">'
        )
        html = html[:insert_pos] + dim_tags + html[insert_pos:]
        changed = True
        stats['popular_picks_dimensions_added'] += 1

    return html, changed


def fix_schema_image_itinerary(html, slug):
    """Fix #3: Add 'image' field to Article JSON-LD schema on itinerary pages."""
    changed = False
    image_url = f"{R2_BASE}/i/{slug}/hero-bg.jpg"

    # Only add if page has hero-bg
    if 'hero-bg' not in html:
        return html, changed

    # Find Article schema JSON-LD
    # Pattern: script type="application/ld+json" containing "@type": "Article"
    ld_pattern = r'(<script\s+type="application/ld\+json">\s*\{[^}]*"@type"\s*:\s*"Article"[^<]*</script>)'

    # More robust: find all ld+json blocks, parse the Article one
    ld_blocks = list(re.finditer(r'<script\s+type="application/ld\+json">\s*(\{.*?\})\s*</script>', html, re.DOTALL))

    for block in ld_blocks:
        try:
            data = json.loads(block.group(1))
        except json.JSONDecodeError:
            continue

        if data.get('@type') == 'Article' and 'image' not in data:
            # Add image field after mainEntityOfPage or dateModified
            json_str = block.group(1)
            
            # Find the last property before the closing }
            # Insert "image": "..." before the final }
            last_brace = json_str.rfind('}')
            if last_brace != -1:
                # Find the last non-whitespace before the }
                pre = json_str[:last_brace].rstrip()
                if not pre.endswith(','):
                    pre += ','
                new_json = pre + f'\n        "image": "{image_url}"\n    ' + '}' 
                
                # Validate the new JSON
                try:
                    json.loads(new_json)
                except json.JSONDecodeError:
                    # Fallback: try simpler insertion
                    # Add after "mainEntityOfPage" line
                    mep_match = re.search(r'("mainEntityOfPage"\s*:\s*"[^"]*")', json_str)
                    if mep_match:
                        new_json = json_str[:mep_match.end()] + f',\n        "image": "{image_url}"' + json_str[mep_match.end():]
                    else:
                        stats['errors'].append(f"Could not inject schema image for {slug}")
                        continue

                html = html[:block.start(1)] + new_json + html[block.end(1):]
                changed = True
                stats['fix3_schema_image_added'] += 1
                break  # Only one Article block per page

    return html, changed


def process_file(filepath):
    """Process a single HTML file with all applicable fixes."""
    stats['files_scanned'] += 1

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original = f.read()
    except Exception as e:
        stats['errors'].append(f"Read error {filepath}: {e}")
        return

    html = original
    rel_path = str(filepath.relative_to(TABIJI_ROOT))

    # Fix #1: robots meta — ALL pages
    html, _ = fix_robots_meta(html)

    # Fix #2 & #3: itinerary-specific
    if rel_path.startswith('i/'):
        parts = rel_path.split('/')
        if len(parts) >= 2:
            slug = parts[1]
            html, _ = fix_og_image_itinerary(html, slug)
            html, _ = fix_schema_image_itinerary(html, slug)

    # Popular-picks: add dimensions to existing og:image
    if rel_path.startswith('popular-picks/'):
        html, _ = fix_og_dimensions_popular_picks(html)

    # Write if changed
    if html != original:
        stats['files_modified'] += 1
        if not DRY_RUN:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)


def main():
    print(f"{'[DRY RUN] ' if DRY_RUN else ''}Scanning tabiji HTML files...")
    print(f"Root: {TABIJI_ROOT}\n")

    # Find all HTML files
    html_files = sorted(TABIJI_ROOT.rglob('*.html'))
    # Exclude template files and non-page files
    html_files = [f for f in html_files if 'node_modules' not in str(f) 
                  and 'template' not in f.name
                  and '.git' not in str(f)]

    print(f"Found {len(html_files)} HTML files\n")

    for filepath in html_files:
        process_file(filepath)

    # Print results
    print("=" * 60)
    print(f"{'[DRY RUN] ' if DRY_RUN else ''}RESULTS")
    print("=" * 60)
    print(f"Files scanned:                   {stats['files_scanned']}")
    print(f"Files modified:                  {stats['files_modified']}")
    print(f"")
    print(f"Fix #1 — robots meta tag:")
    print(f"  Updated existing tag:          {stats['fix1_robots_updated']}")
    print(f"  Added new tag:                 {stats['fix1_robots_added']}")
    print(f"  Total:                         {stats['fix1_robots_updated'] + stats['fix1_robots_added']}")
    print(f"")
    print(f"Fix #2 — og:image on itineraries:")
    print(f"  Added og:image + dimensions:   {stats['fix2_og_image_added']}")
    print(f"  Skipped (no hero-bg):          {stats['skipped_no_hero']}")
    print(f"")
    print(f"Fix #3 — schema image on itineraries:")
    print(f"  Added image to Article JSON-LD: {stats['fix3_schema_image_added']}")
    print(f"")
    print(f"Bonus — popular-picks dimensions:")
    print(f"  Added og:image dimensions:     {stats['popular_picks_dimensions_added']}")

    if stats['errors']:
        print(f"\nErrors ({len(stats['errors'])}):")
        for e in stats['errors']:
            print(f"  ⚠️  {e}")

    print()


if __name__ == '__main__':
    main()
