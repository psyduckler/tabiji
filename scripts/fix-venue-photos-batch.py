#!/usr/bin/env python3
"""
Fix batch-generated popular-picks pages:
1. Replace per-venue photos (all pointing to hero-bg.jpg) with venue-specific slugged URLs
2. Update og:image and twitter:image to use first venue's photo
3. Add speakable to Article schema if missing

Usage:
    python3 scripts/fix-venue-photos-batch.py [--dry-run] [--slug SLUG]
"""

import os
import re
import sys
import argparse
from pathlib import Path

PP_DIR = Path(__file__).resolve().parents[1] / "popular-picks"

def venue_slug(name):
    """Convert venue name to URL-safe slug."""
    s = name.lower().strip()
    s = re.sub(r"[''`]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:40]


def fix_page(slug, dry_run=False):
    """Fix a single page's venue photo URLs."""
    html_path = PP_DIR / slug / "index.html"
    if not html_path.exists():
        return "missing"
    
    html = html_path.read_text()
    
    # Only process pages with restaurant-photo divs (batch-gen pages)
    if "restaurant-photo" not in html:
        return "skip-not-batch"
    
    original = html
    
    # Find all venue names and their corresponding photo blocks
    # Pattern: <h2>Venue Name</h2> ... <img src="...hero-bg.jpg" alt="Venue Name">
    
    # Strategy: find each restaurant-section, extract venue name from h2, update img src
    sections = re.finditer(
        r'(<section class="restaurant-section".*?</section>)',
        html, re.DOTALL
    )
    
    for section_match in sections:
        section = section_match.group(1)
        
        # Extract venue name from h2
        h2_match = re.search(r'<h2>([^<]+)</h2>', section)
        if not h2_match:
            continue
        
        venue_name = h2_match.group(1).strip()
        v_slug = venue_slug(venue_name)
        
        # Replace hero-bg.jpg with venue-specific photo
        old_src = f'src="https://img.tabiji.ai/popular-picks/{slug}/hero-bg.jpg"'
        new_src = f'src="https://img.tabiji.ai/popular-picks/{slug}/{v_slug}.jpg"'
        
        new_section = section.replace(old_src, new_src, 1)
        
        if new_section != section:
            html = html.replace(section, new_section, 1)
    
    # Update og:image and twitter:image to first venue's photo
    first_h2 = re.search(r'<section class="restaurant-section".*?<h2>([^<]+)</h2>', html, re.DOTALL)
    if first_h2:
        first_v_slug = venue_slug(first_h2.group(1).strip())
        new_og = f'https://img.tabiji.ai/popular-picks/{slug}/{first_v_slug}.jpg'
        
        html = re.sub(
            r'<meta property="og:image" content="[^"]*">',
            f'<meta property="og:image" content="{new_og}">',
            html
        )
        html = re.sub(
            r'<meta name="twitter:image" content="[^"]*">',
            f'<meta name="twitter:image" content="{new_og}">',
            html
        )
        # Update Article schema image
        html = re.sub(
            r'"image":\s*"https://img\.tabiji\.ai/popular-picks/' + re.escape(slug) + r'/hero-bg\.jpg"',
            f'"image": "{new_og}"',
            html
        )
    
    if html == original:
        return "no-changes"
    
    if dry_run:
        return "dry-run-ok"
    
    html_path.write_text(html)
    return "updated"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--slug", help="Process single slug")
    args = parser.parse_args()
    
    if args.slug:
        slugs = [args.slug]
    else:
        slugs = sorted(d.name for d in PP_DIR.iterdir() if d.is_dir() and (d / "index.html").exists())
    
    counts = {"updated": 0, "skip-not-batch": 0, "no-changes": 0, "missing": 0, "dry-run-ok": 0}
    
    for slug in slugs:
        result = fix_page(slug, args.dry_run)
        counts[result] = counts.get(result, 0) + 1
        if result in ("updated", "dry-run-ok"):
            print(f"[{result}] {slug}")
    
    print(f"\n--- Summary ---")
    for k, v in counts.items():
        if v:
            print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
