#!/usr/bin/env python3
"""Add 'Related Picks' and cross-link sections to popular-picks pages.

For each popular-picks page, finds other pages for the same city and links to them.
Also links to relevant compare pages if they exist.
"""

import os
import re
import glob
from collections import defaultdict

PICKS_DIR = os.path.expanduser("~/tabiji/popular-picks")
COMPARE_DIR = os.path.expanduser("~/tabiji/compare")

# Map of known multi-word city slugs
MULTI_WORD_CITIES = {
    "abu-dhabi", "buenos-aires", "cape-town", "chiang-mai", "dar-es-salaam",
    "hong-kong", "ho-chi-minh", "kuala-lumpur", "las-vegas", "los-angeles",
    "mexico-city", "new-orleans", "new-york", "playa-del-carmen", "rio-de-janeiro",
    "san-francisco", "san-sebastian", "santa-fe", "siem-reap", "sri-lanka",
    "st-petersburg", "tel-aviv", "la-paz", "el-nido", "porto-alegre",
    "san-miguel-de-allende", "mar-del-plata", "punta-cana", "costa-rica",
    "addis-ababa", "koh-samui", "koh-phangan", "koh-lipe", "phi-phi",
    "ras-al-khaimah", "phu-quoc", "puerto-vallarta", "puerto-rico",
    "nusa-penida", "da-nang", "hoi-an", "ho-chi-minh-city",
    "port-louis", "sharm-el-sheikh", "hurghada",
}

def extract_city_slug(dirname):
    """Extract city slug from directory name."""
    for slug in sorted(MULTI_WORD_CITIES, key=lambda x: -len(x)):
        if dirname.startswith(slug + "-") or dirname == slug:
            return slug
    return dirname.split("-")[0]

def slug_to_title(slug):
    """Convert slug to title case."""
    words = slug.split("-")
    small_words = {"de", "del", "el", "es", "la", "al"}
    return " ".join(w if w in small_words else w.title() for w in words)

def extract_page_title(filepath):
    """Extract h1 or title from page."""
    try:
        with open(filepath, "r") as f:
            content = f.read(5000)  # Just the head
        m = re.search(r'<title>([^<]+)</title>', content)
        if m:
            title = m.group(1).split(" | ")[0].split(" — ")[0].strip()
            return title
    except:
        pass
    return None

# Build city → pages index
city_pages = defaultdict(list)
all_pages = sorted(glob.glob(os.path.join(PICKS_DIR, "*/index.html")))

for page in all_pages:
    dirname = os.path.basename(os.path.dirname(page))
    # Skip country pages
    if "/" not in dirname and "-" not in dirname:
        continue
    city_slug = extract_city_slug(dirname)
    category = dirname[len(city_slug)+1:] if dirname.startswith(city_slug + "-") else ""
    if category:
        city_pages[city_slug].append((dirname, category))

# Build city → compare pages index
city_compares = defaultdict(list)
for page in sorted(glob.glob(os.path.join(COMPARE_DIR, "*/index.html"))):
    dirname = os.path.basename(os.path.dirname(page))
    if "-vs-" in dirname:
        parts = dirname.split("-vs-")
        for part in parts:
            city_compares[part].append(dirname)

RELATED_CSS = """
<style>
.related-picks-module { background: white; border: 1px solid #e0d6c8; border-radius: 18px; padding: 1.35rem 1.4rem; margin-bottom: 1.4rem; }
.related-picks-module h3 { margin: 0 0 .3rem; color: #2D3A5C; font-size: 1.05rem; }
.related-picks-module .related-subtitle { color: #7a6f63; font-size: .85rem; margin: 0 0 .9rem; }
.related-picks-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: .6rem; }
.related-pick-link { display: block; background: #faf7f2; border: 1px solid #e0d6c8; border-radius: 10px; padding: .7rem .9rem; text-decoration: none; color: #2D3A5C; font-size: .88rem; font-weight: 600; transition: border-color .2s; }
.related-pick-link:hover { border-color: #C4704B; }
.related-compare-links { margin-top: .8rem; padding-top: .7rem; border-top: 1px solid #e0d6c8; }
.related-compare-links p { margin: 0 0 .5rem; font-size: .85rem; color: #7a6f63; }
.related-compare-links a { display: inline-block; background: #2D3A5C; color: white; padding: .35rem .8rem; border-radius: 8px; font-size: .82rem; text-decoration: none; margin: .2rem .3rem .2rem 0; }
.related-compare-links a:hover { background: #C4704B; }
</style>
"""

added = 0
for page in all_pages:
    dirname = os.path.basename(os.path.dirname(page))
    city_slug = extract_city_slug(dirname)
    
    with open(page, "r") as f:
        content = f.read()
    
    # Skip if already has related picks module
    if "related-picks-module" in content:
        continue
    
    # Get sibling pages (same city, different category)
    siblings = [(d, c) for d, c in city_pages.get(city_slug, []) if d != dirname]
    compares = city_compares.get(city_slug, [])[:4]  # Max 4 compare links
    
    if not siblings and not compares:
        continue
    
    city_name = slug_to_title(city_slug)
    
    # Build related HTML
    picks_html = ""
    if siblings:
        # Show max 6 related picks
        shown = siblings[:6]
        picks_html = '<div class="related-picks-grid">\n'
        for d, c in shown:
            cat_title = slug_to_title(c)
            picks_html += f'    <a class="related-pick-link" href="/popular-picks/{d}/">{city_name} {cat_title}</a>\n'
        picks_html += '  </div>'
    
    compare_html = ""
    if compares:
        compare_html = '\n  <div class="related-compare-links">\n    <p>Compare destinations:</p>\n'
        for comp in compares:
            comp_title = comp.replace("-", " ").replace(" vs ", " vs ").title()
            compare_html += f'    <a href="/compare/{comp}/">{comp_title}</a>\n'
        compare_html += '  </div>'
    
    module = f"""
<!-- related-picks:start -->
<section class="related-picks-module">
  <h3>More {city_name} Guides</h3>
  <p class="related-subtitle">Explore other popular picks in {city_name}</p>
  {picks_html}{compare_html}
</section>
<!-- related-picks:end -->
"""
    
    # Insert before social-proof or cta-section or footer
    for marker in ["<!-- social-proof:start -->", '<section class="cta-section">', '<div class="cta-section">', "<!-- @include:footer:start -->"]:
        if marker in content:
            content = content.replace(marker, module + "\n" + marker, 1)
            break
    else:
        continue
    
    # Add CSS
    if "related-picks-module" in RELATED_CSS and "related-picks-module" not in content.split("</head>")[0]:
        content = content.replace("</head>", RELATED_CSS + "</head>", 1)
    
    with open(page, "w") as f:
        f.write(content)
    added += 1

print(f"Added related picks module to {added} pages")
