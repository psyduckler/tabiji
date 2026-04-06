#!/usr/bin/env python3
"""
Upgrade a compare page to the new UX format (13-point UX overhaul).

Usage:
    python3 scripts/upgrade-compare-ux.py <slug>
    python3 scripts/upgrade-compare-ux.py madrid-vs-barcelona
    python3 scripts/upgrade-compare-ux.py --all    # upgrade all pages
    python3 scripts/upgrade-compare-ux.py --batch slugs.txt  # one slug per line

Reference implementation: compare/madrid-vs-barcelona/index.html

This script:
1. Reads the existing page HTML
2. Extracts content data (destinations, winners, costs, FAQs, images)
3. Generates the new UX components (scorecard, quick answers, collapsible sections, etc.)
4. Writes the upgraded page

NOTE: Personalization recommendations require AI generation — this script
creates a placeholder that should be filled by running the companion
generate-personalization.py script or manually.
"""
from __future__ import annotations

import html as html_mod
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
COMPARE_DIR = REPO_ROOT / "compare"
SCRIPTS_DIR = REPO_ROOT / "scripts"

# Destination color pairs (warm for dest1, cool for dest2)
DEST1_COLOR = "#C0392B"
DEST2_COLOR = "#2E86C1"
TIE_COLOR = "#7A8B6F"

# ─── CSS & JS Templates ─────────────────────────────────────────────
def load_ux_css() -> str:
    """Load the UX CSS from the reference file."""
    css_path = SCRIPTS_DIR / "compare-ux-styles.css"
    if css_path.exists():
        return css_path.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Missing {css_path} — extract from madrid-vs-barcelona first")


def load_ux_js() -> str:
    """Load the UX JS from the reference file."""
    js_path = SCRIPTS_DIR / "compare-ux-scripts.js"
    if js_path.exists():
        return js_path.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Missing {js_path} — extract from madrid-vs-barcelona first")


# ─── Content extraction ──────────────────────────────────────────────
def extract_destinations(page_html: str) -> Tuple[str, str]:
    """Extract destination names from the h1 tag."""
    m = re.search(r'<h1[^>]*>(.*?)</h1>', page_html, re.DOTALL)
    if not m:
        raise ValueError("No h1 found")
    h1_text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    # Pattern: "City1 vs City2: ..."
    vs_match = re.match(r'^(.+?)\s+vs\s+(.+?):', h1_text, re.I)
    if vs_match:
        return vs_match.group(1).strip(), vs_match.group(2).strip()
    vs_match = re.match(r'^(.+?)\s+vs\s+(.+)', h1_text, re.I)
    if vs_match:
        return vs_match.group(1).strip(), vs_match.group(2).strip()
    raise ValueError(f"Cannot parse destinations from: {h1_text}")


def extract_section_winners(page_html: str, dest1: str, dest2: str) -> List[Dict]:
    """Extract winner info from deep-dive sections."""
    sections = []
    # Find all deep-dive section headings with their IDs and verdicts
    # Pattern: section with h2 id, then tabiji-verdict or section-winner
    section_pattern = re.compile(
        r'<h2\s+id="([^"]+)"[^>]*>(.*?)</h2>.*?(?:tabiji.verdict|section-winner)[^<]*<[^>]*>(.*?)</(?:div|p)>',
        re.DOTALL | re.I
    )
    for m in section_pattern.finditer(page_html):
        section_id = m.group(1)
        heading_raw = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        verdict_text = re.sub(r'<[^>]+>', '', m.group(3)).strip()

        # Determine winner
        d1_lower = dest1.lower()
        d2_lower = dest2.lower()
        verdict_lower = verdict_text.lower()

        if 'tie' in verdict_lower or 'both' in verdict_lower:
            winner = 'tie'
        elif d1_lower in verdict_lower and ('wins' in verdict_lower or 'better' in verdict_lower or 'safer' in verdict_lower or 'cheaper' in verdict_lower or 'stronger' in verdict_lower):
            winner = 'dest1'
        elif d2_lower in verdict_lower and ('wins' in verdict_lower or 'better' in verdict_lower or 'safer' in verdict_lower or 'cheaper' in verdict_lower or 'stronger' in verdict_lower):
            winner = 'dest2'
        else:
            winner = 'tie'

        sections.append({
            'id': section_id,
            'heading': heading_raw,
            'winner': winner,
            'verdict_snippet': verdict_text[:120],
        })

    return sections


def extract_images(page_html: str, slug: str) -> Dict[str, str]:
    """Extract all image URLs from the page."""
    images = {}
    for m in re.finditer(r'<img[^>]+src="([^"]+)"[^>]*>', page_html):
        url = m.group(1)
        if f'/compare/{slug}/' in url or 'img.tabiji.ai' in url:
            # Classify: hero, dest1, dest2, or section images
            if 'hero' in url:
                images['hero'] = url
            elif 'dest1' in url:
                images['dest1'] = url
            elif 'dest2' in url:
                images['dest2'] = url
            else:
                # Use filename as key
                fname = url.rsplit('/', 1)[-1].split('.')[0]
                images[fname] = url
    # Ensure we have at least hero, dest1, dest2
    base_url = f"https://img.tabiji.ai/compare/{slug}"
    images.setdefault('hero', f"{base_url}/hero.jpg")
    images.setdefault('dest1', f"{base_url}/dest1.jpg")
    images.setdefault('dest2', f"{base_url}/dest2.jpg")
    return images


def extract_faq_items(page_html: str) -> List[Dict]:
    """Extract FAQ question/answer pairs."""
    items = []
    for m in re.finditer(r'<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>', page_html, re.DOTALL):
        q = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        a = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if '?' in q:
            items.append({'question': q, 'answer': a})
    return items


def extract_related_slugs(slug: str) -> List[str]:
    """Get related comparison slugs from inventory."""
    inv_path = COMPARE_DIR / "inventory.json"
    if not inv_path.exists():
        return []
    try:
        inv = json.loads(inv_path.read_text(encoding="utf-8"))
        items = inv.get('items', []) if isinstance(inv, dict) else inv
        for item in items:
            if isinstance(item, dict) and item.get('slug') == slug:
                return item.get('relatedSlugs', [])[:3]
    except Exception:
        pass
    return []


def check_image_exists(url: str) -> bool:
    """Quick check if a CDN image URL exists (returns True/False)."""
    import urllib.request
    try:
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except Exception:
        return False


# ─── Extraction summary ──────────────────────────────────────────────
def extract_page_data(slug: str) -> Dict:
    """Extract all data needed to rebuild a page with new UX."""
    page_path = COMPARE_DIR / slug / "index.html"
    if not page_path.exists():
        raise FileNotFoundError(f"Page not found: {page_path}")

    page_html = page_path.read_text(encoding="utf-8")
    dest1, dest2 = extract_destinations(page_html)
    sections = extract_section_winners(page_html, dest1, dest2)
    images = extract_images(page_html, slug)
    faq_items = extract_faq_items(page_html)
    related = extract_related_slugs(slug)

    # Count wins
    d1_wins = sum(1 for s in sections if s['winner'] == 'dest1')
    d2_wins = sum(1 for s in sections if s['winner'] == 'dest2')
    ties = sum(1 for s in sections if s['winner'] == 'tie')

    return {
        'slug': slug,
        'dest1': dest1,
        'dest2': dest2,
        'sections': sections,
        'images': images,
        'faq_items': faq_items,
        'related_slugs': related,
        'score': {'dest1': d1_wins, 'dest2': d2_wins, 'ties': ties},
    }


# ─── Main ────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/upgrade-compare-ux.py <slug>")
        print("       python3 scripts/upgrade-compare-ux.py --analyze <slug>")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "--analyze":
        slug = sys.argv[2]
        data = extract_page_data(slug)
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    if cmd == "--all":
        # Find all compare pages with -vs- in slug
        slugs = sorted([
            p.parent.name for p in COMPARE_DIR.glob("*/index.html")
            if '-vs-' in p.parent.name
        ])
        print(f"Found {len(slugs)} compare pages")
        for slug in slugs:
            print(f"  {slug}")
        return

    # Single slug
    slug = cmd
    data = extract_page_data(slug)
    print(f"Extracted data for: {data['dest1']} vs {data['dest2']}")
    print(f"Score: {data['dest1']} {data['score']['dest1']} — {data['score']['dest2']} {data['dest2']} ({data['score']['ties']} ties)")
    print(f"Sections: {len(data['sections'])}")
    print(f"FAQ items: {len(data['faq_items'])}")
    print(f"Related: {data['related_slugs']}")
    print(f"Images: {list(data['images'].keys())}")
    print()
    print("To upgrade this page, use the compare-ux-upgrade skill in Claude Code:")
    print(f"  /compare-ux-upgrade {slug}")


if __name__ == "__main__":
    main()
