#!/usr/bin/env python3
"""
SEO/AEO upgrade for all popular-picks pages.
Fixes:
1. Broken og:image (generic hero-bg.jpg → actual R2 image or first photo)
2. Add Article schema with datePublished/dateModified (where missing)
3. Add BreadcrumbList schema (where missing)
4. Add speakable schema to Article
5. Fix twitter:image to match og:image
"""
import os
import re
import json
import sys
from pathlib import Path
from datetime import datetime

TABIJI_DIR = Path(os.path.expanduser("~/tabiji"))
PP_DIR = TABIJI_DIR / "popular-picks"
TODAY = "2026-03-08"

stats = {"og_image_fixed": 0, "article_added": 0, "breadcrumb_added": 0, "speakable_added": 0, "total_processed": 0, "errors": []}

def get_slug_name(slug):
    """Convert slug to human-readable name."""
    return slug.replace("-", " ").title()

def find_first_photo_url(slug, html):
    """Find the best og:image for a popular-picks page."""
    # Check if R2 has a hero image for this slug
    r2_hero = f"https://img.tabiji.ai/popular-picks/{slug}/hero-bg.jpg"
    # Check if there's a photo-0 in R2
    r2_photo0 = f"https://img.tabiji.ai/popular-picks/{slug}/photo-0.jpg"
    
    # Look for any img tags in the HTML pointing to R2 for this slug
    r2_pattern = re.findall(rf'https://img\.tabiji\.ai/popular-picks/{re.escape(slug)}/[^"\'>\s]+', html)
    if r2_pattern:
        return r2_pattern[0]
    
    # Check if current og:image is already good
    og_match = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    if og_match:
        current = og_match.group(1)
        if "hero-bg.jpg" not in current and slug in current:
            return current  # Already specific to this slug
    
    # Default to photo-0 on R2
    return r2_photo0

def extract_title(html):
    """Extract page title from <title> tag."""
    m = re.search(r'<title>([^<]+)</title>', html)
    return m.group(1).split(" — ")[0].split(" | ")[0].strip() if m else ""

def extract_description(html):
    """Extract meta description."""
    m = re.search(r'<meta name="description" content="([^"]+)"', html)
    return m.group(1) if m else ""

def extract_dates(html):
    """Extract published/modified dates from meta tags or default to today."""
    pub = re.search(r'article:published_time" content="([^"]+)"', html)
    mod = re.search(r'article:modified_time" content="([^"]+)"', html)
    pub_date = pub.group(1)[:10] if pub else TODAY
    mod_date = mod.group(1)[:10] if mod else TODAY
    return pub_date, mod_date

def extract_og_image(html):
    """Get current og:image."""
    m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    return m.group(1) if m else ""

def build_article_schema(title, description, url, image, pub_date, mod_date):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "author": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai"},
        "publisher": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai"},
        "datePublished": pub_date,
        "dateModified": mod_date,
        "mainEntityOfPage": url,
        "image": image,
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": [".hero h1", ".hero .subtitle", ".faq-section"]
        }
    }, indent=8)

def build_breadcrumb_schema(slug, title):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tabiji.ai/"},
            {"@type": "ListItem", "position": 2, "name": "Popular Picks", "item": "https://tabiji.ai/popular-picks/"},
            {"@type": "ListItem", "position": 3, "name": title, "item": f"https://tabiji.ai/popular-picks/{slug}/"}
        ]
    }, indent=8)

def process_page(page_dir):
    slug = page_dir.name
    index_file = page_dir / "index.html"
    if not index_file.exists():
        return
    
    html = index_file.read_text(encoding="utf-8")
    original = html
    title = extract_title(html)
    description = extract_description(html)
    pub_date, mod_date = extract_dates(html)
    url = f"https://tabiji.ai/popular-picks/{slug}/"
    og_image = extract_og_image(html)
    
    # 1. Fix broken og:image
    if "popular-picks/hero-bg.jpg" in og_image or (og_image and slug not in og_image and "popular-picks" in og_image):
        best_image = find_first_photo_url(slug, html)
        if best_image != og_image:
            html = html.replace(f'content="{og_image}"', f'content="{best_image}"', 2)  # og:image and twitter:image
            og_image = best_image
            stats["og_image_fixed"] += 1
    
    # 2. Add Article schema (if missing)
    if '"Article"' not in html:
        article_json = build_article_schema(title, description, url, og_image, pub_date, mod_date)
        schema_block = f'\n    <script type="application/ld+json">\n    {article_json}\n    </script>'
        # Insert before the first existing ld+json block
        first_ld = html.find('<script type="application/ld+json">')
        if first_ld > 0:
            html = html[:first_ld] + schema_block.lstrip('\n') + '\n    ' + html[first_ld:]
        else:
            # Insert before </head>
            html = html.replace('</head>', f'{schema_block}\n    </head>')
        stats["article_added"] += 1
    else:
        # Add speakable to existing Article schema if missing
        if '"speakable"' not in html and '"Article"' in html:
            # Find the Article schema block and add speakable
            html = re.sub(
                r'("@type"\s*:\s*"Article"[^}]*"image"\s*:\s*"[^"]*")',
                r'\1,\n        "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".hero h1", ".hero .subtitle", ".faq-section"]}',
                html, count=1
            )
            stats["speakable_added"] += 1
    
    # 3. Add BreadcrumbList (if missing)
    if "BreadcrumbList" not in html:
        breadcrumb_json = build_breadcrumb_schema(slug, title)
        schema_block = f'\n    <script type="application/ld+json">\n    {breadcrumb_json}\n    </script>'
        html = html.replace('</head>', f'{schema_block}\n    </head>')
        stats["breadcrumb_added"] += 1
    
    # Write if changed
    if html != original:
        index_file.write_text(html, encoding="utf-8")
        stats["total_processed"] += 1

def main():
    if not PP_DIR.exists():
        print(f"ERROR: {PP_DIR} does not exist")
        sys.exit(1)
    
    # Process all popular-picks subdirectories
    dirs = sorted([d for d in PP_DIR.iterdir() if d.is_dir() and (d / "index.html").exists()])
    print(f"Found {len(dirs)} popular-picks pages to process")
    
    for page_dir in dirs:
        try:
            process_page(page_dir)
        except Exception as e:
            stats["errors"].append(f"{page_dir.name}: {str(e)}")
            print(f"ERROR processing {page_dir.name}: {e}")
    
    print(f"\n=== Results ===")
    print(f"Total pages modified: {stats['total_processed']}")
    print(f"og:image fixed: {stats['og_image_fixed']}")
    print(f"Article schema added: {stats['article_added']}")
    print(f"BreadcrumbList added: {stats['breadcrumb_added']}")
    print(f"Speakable added: {stats['speakable_added']}")
    if stats["errors"]:
        print(f"Errors ({len(stats['errors'])}):")
        for e in stats["errors"]:
            print(f"  - {e}")

if __name__ == "__main__":
    main()
