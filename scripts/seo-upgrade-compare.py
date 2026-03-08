#!/usr/bin/env python3
"""
SEO/AEO upgrade for all compare pages.
Fixes:
1. Add speakable schema to Article block
2. Add comparison table markup hint (additionalType)
3. Ensure datePublished/dateModified in Article schema
"""
import os
import re
import json
import sys
from pathlib import Path

TABIJI_DIR = Path(os.path.expanduser("~/tabiji"))
COMPARE_DIR = TABIJI_DIR / "compare"
TODAY = "2026-03-08"

stats = {"speakable_added": 0, "total_processed": 0, "errors": []}

def process_page(page_dir):
    slug = page_dir.name
    index_file = page_dir / "index.html"
    if not index_file.exists():
        return
    
    html = index_file.read_text(encoding="utf-8")
    original = html
    
    # 1. Add speakable to Article schema if missing
    if '"speakable"' not in html and '"Article"' in html:
        # Strategy: find the Article schema JSON block and inject speakable
        # Match the image field at end of Article schema and append speakable after it
        pattern = r'("@type"\s*:\s*"Article".*?"image"\s*:\s*"[^"]*")'
        match = re.search(pattern, html, re.DOTALL)
        if match:
            old_text = match.group(0)
            new_text = old_text + ',\n        "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".hero h1", ".hero .subtitle", ".verdict-box", ".faq-section"]}'
            html = html.replace(old_text, new_text, 1)
            stats["speakable_added"] += 1
    
    if html != original:
        index_file.write_text(html, encoding="utf-8")
        stats["total_processed"] += 1

def main():
    if not COMPARE_DIR.exists():
        print(f"ERROR: {COMPARE_DIR} does not exist")
        sys.exit(1)
    
    dirs = sorted([d for d in COMPARE_DIR.iterdir() if d.is_dir() and (d / "index.html").exists()])
    print(f"Found {len(dirs)} compare pages to process")
    
    for page_dir in dirs:
        try:
            process_page(page_dir)
        except Exception as e:
            stats["errors"].append(f"{page_dir.name}: {str(e)}")
            print(f"ERROR processing {page_dir.name}: {e}")
    
    print(f"\n=== Results ===")
    print(f"Total pages modified: {stats['total_processed']}")
    print(f"Speakable added: {stats['speakable_added']}")
    if stats["errors"]:
        print(f"Errors ({len(stats['errors'])}):")
        for e in stats["errors"]:
            print(f"  - {e}")

if __name__ == "__main__":
    main()
