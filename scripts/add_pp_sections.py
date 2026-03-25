#!/usr/bin/env python3
"""
Add methodology, related, and viator sections to popular-picks pages.
Inserts before </main> tag.
"""
import os
import re
import sys
from pathlib import Path

TABIJI = Path.home() / "tabiji"
PP_DIR = TABIJI / "popular-picks"
DEST_DIR = TABIJI / "destinations"

METHODOLOGY_HTML = """    <section class="methodology-section">
      <h2>How we built this list</h2>
      <p>We analyzed hundreds of Reddit posts and thousands of comments across relevant subreddits spanning 2019 to 2026. Places were ranked by frequency of independent recommendations and verified with Google ratings. Every spot was mentioned in at least 2 separate threads by different users.</p>
    </section>
"""

def extract_city_and_title(html: str, slug: str) -> tuple[str, str]:
    """Extract city name and page title from HTML."""
    # Try h1
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    title = ""
    if h1_match:
        title = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()

    # Try <title> tag if no h1
    if not title:
        t_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
        if t_match:
            title = re.sub(r'<[^>]+>', '', t_match.group(1)).strip()
            # Remove site suffix
            title = re.sub(r'\s*[|—–-].*tabiji.*', '', title, flags=re.IGNORECASE).strip()

    # Extract city from slug (first word before first hyphen, unless it's a common word)
    # Use breadcrumb or h1 for city
    city = extract_city_from_context(html, slug)
    return city, title


def extract_city_from_context(html: str, slug: str) -> str:
    """Extract the primary city name from the page."""
    # Try breadcrumb
    bc_match = re.search(r'breadcrumb.*?<a[^>]*href="[^"]*destinations/([^/"]+)"[^>]*>', html, re.DOTALL | re.IGNORECASE)
    if bc_match:
        city_slug = bc_match.group(1)
        return slug_to_city(city_slug)

    # Try og:url or canonical
    url_match = re.search(r'popular-picks/([^/"]+)/', html)
    if url_match:
        page_slug = url_match.group(1)
        return city_from_slug(page_slug)

    return city_from_slug(slug)


def slug_to_city(s: str) -> str:
    """Convert a slug like 'new-york' → 'New York'."""
    return s.replace('-', ' ').title()


def city_from_slug(slug: str) -> str:
    """Extract city from page slug by taking the first meaningful part."""
    # slug like 'amsterdam-brunch' → 'Amsterdam'
    # slug like 'new-york-pizza' → 'New York'
    # slug like 'tokyo-ramen' → 'Tokyo'
    # Special cases: multi-word cities
    multi_word_cities = [
        'new-york', 'new-zealand', 'new-orleans', 'new-delhi',
        'hong-kong', 'san-francisco', 'san-jose', 'san-diego',
        'los-angeles', 'las-vegas', 'sao-paulo', 'buenos-aires',
        'rio-de-janeiro', 'costa-rica', 'cape-town', 'kuala-lumpur',
        'addis-ababa', 'antigua-guatemala', 'abu-dhabi', 'tel-aviv',
        'kuala-lumpur', 'puerto-rico', 'puerto-vallarta', 'punta-cana',
        'mexico-city', 'el-salvador', 'port-au-prince', 'ho-chi-minh',
        'phnom-penh', 'palma-de-mallorca', 'palma-mallorca', 'gran-canaria',
        'costa-brava', 'lake-como', 'lake-bled', 'lake-district',
        'mekong-delta', 'rio-grande', 'south-korea', 'south-africa',
        'sri-lanka', 'saudi-arabia', 'saudi-arabia', 'santa-fe',
        'santa-barbara', 'san-sebastian', 'san-miguel', 'porto-alegre',
        'north-vietnam', 'south-vietnam', 'central-vietnam',
    ]
    
    slug_lower = slug.lower()
    for mc in multi_word_cities:
        if slug_lower.startswith(mc):
            return slug_to_city(mc)
    
    # Default: first hyphen-separated word
    first_part = slug.split('-')[0]
    return first_part.title()


def city_to_url_encoded(city: str) -> str:
    """Convert city name to URL-encoded form with + signs."""
    return city.replace(' ', '+')


def build_index() -> dict:
    """Build index: slug → {title, city, path, has_methodology, has_related, has_viator}"""
    index = {}
    for page_dir in PP_DIR.iterdir():
        if not page_dir.is_dir():
            continue
        idx = page_dir / "index.html"
        if not idx.exists():
            continue
        slug = page_dir.name
        try:
            html = idx.read_text(encoding='utf-8')
        except Exception as e:
            print(f"ERROR reading {idx}: {e}", file=sys.stderr)
            continue
        
        city, title = extract_city_and_title(html, slug)
        
        index[slug] = {
            'title': title,
            'city': city,
            'path': idx,
            'html': html,
            'has_methodology': 'methodology-section' in html,
            'has_related': 'related-section' in html,
            'has_viator': 'viator-section' in html,
        }
    
    return index


def find_related_pages(slug: str, city: str, index: dict, limit: int = 4) -> list[dict]:
    """Find related popular-picks pages for the same city."""
    results = []
    city_lower = city.lower()
    
    for s, info in index.items():
        if s == slug:
            continue
        # Match by city name in the slug or in the extracted city
        if (info['city'].lower() == city_lower or 
            s.lower().startswith(city_lower.replace(' ', '-')) or
            s.lower().replace('-', ' ').startswith(city_lower.lower())):
            results.append({'slug': s, 'title': info['title']})
    
    return results[:limit]


def build_related_section(slug: str, city: str, index: dict) -> str:
    """Build the related section HTML."""
    related = find_related_pages(slug, city, index)
    
    # Check if destination page exists
    dest_slug = city.lower().replace(' ', '-')
    dest_path = DEST_DIR / dest_slug
    has_dest = dest_path.exists() and (dest_path / "index.html").exists()
    
    cards = []
    
    if has_dest:
        cards.append(f'''      <a class="intent-card" href="/destinations/{dest_slug}/">
        <span class="intent-type">destination guide</span>
        <strong>{city} Travel Guide</strong>
      </a>''')
    
    for r in related:
        cards.append(f'''      <a class="intent-card" href="/popular-picks/{r['slug']}/">
        <span class="intent-type">popular picks</span>
        <strong>{r['title']}</strong>
      </a>''')
    
    if not cards:
        # Generic fallback: 3 random other cities
        other_cities = [
            {'slug': 'tokyo-ramen', 'title': 'Best Ramen Spots in Tokyo'},
            {'slug': 'paris-bistros', 'title': 'Best Bistros in Paris'},
            {'slug': 'barcelona-tapas', 'title': 'Best Tapas Bars in Barcelona'},
        ]
        for o in other_cities:
            if o['slug'] in index and o['slug'] != slug:
                cards.append(f'''      <a class="intent-card" href="/popular-picks/{o['slug']}/">
        <span class="intent-type">popular picks</span>
        <strong>{o['title']}</strong>
      </a>''')
        heading = "Related Popular Picks"
        intro = "More top-rated spot guides from around the world."
    else:
        heading = f"More {city} Picks"
        intro = "Adjacent topical guides in the same city."
    
    if not cards:
        return ""
    
    cards_html = "\n".join(cards)
    return f"""    <section class="related-section intent-section">
      <h2>{heading}</h2>
      <p class="related-intro">{intro}</p>
      <div class="intent-grid">
{cards_html}
      </div>
    </section>
"""


def build_viator_section(city: str) -> str:
    """Build the viator section HTML."""
    city_encoded = city_to_url_encoded(city)
    return f"""    <section class="viator-section">
      <h2>🎫 Book {city} Experiences</h2>
      <p class="viator-subtitle">Tours and activities hand-picked for this guide — book with free cancellation</p>
      <div class="viator-cards">
        <a class="viator-card" href="https://www.viator.com/search/{city_encoded}+tours?pid=P00292930&amp;mcid=42383&amp;medium=link" target="_blank" rel="noopener sponsored">
          <span class="tour-type">Explore</span>
          <span class="tour-name">All {city} Tours &amp; Activities →</span>
        </a>
      </div>
    </section>
"""


def inject_sections(html: str, sections_html: str) -> str:
    """Inject sections before </main> tag."""
    # Try to insert before </main>
    main_close = html.rfind('</main>')
    if main_close != -1:
        return html[:main_close] + sections_html + html[main_close:]
    
    # Fallback: before <footer
    footer_pos = html.rfind('<footer')
    if footer_pos != -1:
        return html[:footer_pos] + sections_html + html[footer_pos:]
    
    # Last resort: before </body>
    body_close = html.rfind('</body>')
    if body_close != -1:
        return html[:body_close] + sections_html + html[body_close:]
    
    return html


def main():
    print("Building index of popular-picks pages...")
    index = build_index()
    print(f"Found {len(index)} pages")
    
    # Count missing
    missing_m = [s for s, d in index.items() if not d['has_methodology']]
    missing_r = [s for s, d in index.items() if not d['has_related']]
    missing_v = [s for s, d in index.items() if not d['has_viator']]
    
    print(f"Missing methodology: {len(missing_m)}")
    print(f"Missing related: {len(missing_r)}")
    print(f"Missing viator: {len(missing_v)}")
    print()
    
    # All slugs that need ANY update
    needs_update = set(missing_m) | set(missing_r) | set(missing_v)
    print(f"Total pages to update: {len(needs_update)}")
    print()
    
    updated = 0
    errors = 0
    
    for slug in sorted(needs_update):
        info = index[slug]
        html = info['html']
        city = info['city']
        original_html = html
        
        sections_to_add = ""
        added = []
        
        # Build sections in order: methodology, viator, related
        # (they'll be inserted together before </main>)
        if not info['has_methodology']:
            sections_to_add += METHODOLOGY_HTML
            added.append('methodology')
        
        if not info['has_viator']:
            sections_to_add += build_viator_section(city)
            added.append('viator')
        
        if not info['has_related']:
            rel = build_related_section(slug, city, index)
            if rel:
                sections_to_add += rel
                added.append('related')
        
        if not sections_to_add:
            continue
        
        new_html = inject_sections(html, sections_to_add)
        
        if new_html == original_html:
            print(f"  WARNING: No change for {slug} (no </main> found?)")
            errors += 1
            continue
        
        try:
            info['path'].write_text(new_html, encoding='utf-8')
            updated += 1
            print(f"  ✓ {slug} [{city}] — added: {', '.join(added)}")
        except Exception as e:
            print(f"  ERROR writing {slug}: {e}")
            errors += 1
    
    print()
    print(f"Done. Updated: {updated}, Errors: {errors}")


if __name__ == '__main__':
    main()
