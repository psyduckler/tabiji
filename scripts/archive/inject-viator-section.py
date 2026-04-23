#!/usr/bin/env python3
"""
inject-viator-section.py

Injects a Viator "Book Experiences" affiliate section into all existing
popular-picks pages between the FAQ section and the Related section.

Usage:
    python3 inject-viator-section.py [--dry-run] [--slug SLUG]
"""

import os
import re
import json
import glob
import argparse
from urllib.parse import quote

POPULAR_PICKS_DIR = os.path.expanduser('~/tabiji/popular-picks')
DATA_DIR = os.path.expanduser('~/tabiji/popular-picks-data')

PID = 'P00292930'
MCID = '42383'
MEDIUM = 'link'
AFFILIATE_PARAMS = f'pid={PID}&mcid={MCID}&medium={MEDIUM}'

VIATOR_CSS = """\
      .viator-section { background:linear-gradient(135deg,#fff9f0 0%,#fff 100%); border:1px solid var(--sand); border-radius:18px; padding:1.35rem 1.4rem; margin-bottom:1.4rem; }
      .viator-section h2 { font-size:1.3em; margin-bottom:6px; }
      .viator-subtitle { font-size:0.95em; color:#666; margin-bottom:20px; }
      .viator-cards { display:grid; grid-template-columns:1fr 1fr; gap:14px; }
      @media(max-width:600px) { .viator-cards { grid-template-columns:1fr; } }
      .viator-card { background:#fff; border:1px solid #e8e8e8; border-radius:10px; padding:18px; text-decoration:none; color:inherit; transition:border-color .2s,box-shadow .2s; display:flex; flex-direction:column; gap:8px; }
      .viator-card:hover { border-color:var(--primary,#0696D7); box-shadow:0 2px 12px rgba(6,150,215,.12); }
      .viator-card .tour-type { font-size:.75em; text-transform:uppercase; letter-spacing:.5px; color:var(--primary,#0696D7); font-weight:600; }
      .viator-card .tour-name { font-size:1em; font-weight:600; line-height:1.3; }
      .viator-powered { font-size:.75em; color:#bbb; text-align:right; margin-top:14px; }"""


def city_to_enc(city):
    return quote(city, safe='')


def get_cards(city, category):
    city_enc = city_to_enc(city)
    cat = category.lower()

    def url(suffix):
        return f'https://www.viator.com/search/{city_enc}+{suffix}?{AFFILIATE_PARAMS}'

    explore_url = f'https://www.viator.com/search/{city_enc}+tours?{AFFILIATE_PARAMS}'

    food_keywords = ['restaurant', 'food', 'eat', 'cafe', 'café', 'street food', 'dining', 'brunch', 'lunch', 'dinner', 'coffee', 'ramen', 'sushi', 'pizza', 'burger', 'taco', 'curry', 'noodle', 'seafood', 'vegetarian', 'vegan', 'bakery', 'pastry', 'dessert', 'sweet', 'ice cream', 'chocolate', 'wine', 'cheese', 'foodie', 'culinary', 'tasting', 'jollof', 'injera', 'shawarma', 'mansaf', 'frites', 'stroopwafel', 'nordic']
    shop_keywords = ['shop', 'market', 'boutique', 'fashion', 'vintage', 'antique', 'flea', 'bazaar', 'mall', 'souk', 'bazar', 'handicraft', 'craft', 'artisan']
    bar_keywords = ['bar', 'night', 'nightlife', 'drink', 'cocktail', 'pub', 'club', 'beer', 'gin', 'whisky', 'whiskey', 'rooftop', 'speakeasy', 'jazz', 'live music', 'lounge']
    culture_keywords = ['temple', 'culture', 'museum', 'heritage', 'historic', 'art', 'gallery', 'monument', 'palace', 'castle', 'cathedral', 'church', 'mosque', 'shrine', 'archaeological', 'ruins', 'unesco', 'opera', 'theater', 'ceremony', 'ritual']

    def matches(keywords):
        return any(k in cat for k in keywords)

    if matches(food_keywords):
        cards = [
            ('Food Tour', f'Best {city} Food Tours & Tastings', url('food+tour')),
            ('Night Food Tour', f'{city} Night Street Food Tour', url('night+food+tour')),
            ('Cooking Class', f'{city} Cooking Class & Market Visit', url('cooking+class')),
        ]
    elif matches(shop_keywords):
        cards = [
            ('Shopping Tour', f'{city} Shopping & Style Tour', url('shopping+tour')),
            ('Market Tour', f'{city} Local Market Experience', url('market+tour')),
            ('Cultural Walk', f'{city} Cultural Walking Tour', url('cultural+walk')),
        ]
    elif matches(bar_keywords):
        cards = [
            ('Bar Crawl', f'{city} Bar Crawl & Nightlife Tour', url('bar+crawl')),
            ('Night Tour', f'Guided {city} Night Tour', url('night+tour')),
            ('Food & Drink Tour', f'{city} Food & Drink Experience', url('food+drink+tour')),
        ]
    elif matches(culture_keywords):
        cards = [
            ('Walking Tour', f'{city} Guided Walking Tour', url('walking+tour')),
            ('Cultural Tour', f'{city} Cultural Highlights Tour', url('cultural+tour')),
            ('Day Trip', f'Best Day Trips from {city}', url('day+trip')),
        ]
    else:
        cards = [
            ('Walking Tour', f'{city} Guided Walking Tour', url('walking+tour')),
            ('Food Tour', f'Best {city} Food Tours & Tastings', url('food+tour')),
            ('Day Trip', f'Best Day Trips from {city}', url('day+trip')),
        ]

    # Add Explore More card
    cards.append(('Explore More', f'All {city} Tours & Activities \u2192', explore_url))
    return cards


def render_viator_section(city, category):
    cards = get_cards(city, category)
    card_html = ''
    for tour_type, tour_name, tour_url in cards:
        card_html += f'''
      <a class="viator-card" href="{tour_url}" target="_blank" rel="noopener sponsored">
        <span class="tour-type">{tour_type}</span>
        <span class="tour-name">{tour_name}</span>
      </a>'''

    return f"""
      <section class="viator-section">
        <h2>&#127903;&#65039; Book {city} Experiences</h2>
        <p class="viator-subtitle">Tours and activities hand-picked for this guide — book with free cancellation</p>
        <div class="viator-cards">{card_html}
        </div>
        <p class="viator-powered">Experiences via Viator — free cancellation on most tours</p>
      </section>"""


def get_city_and_category(slug):
    """Try JSON first, fall back to parsing HTML title."""
    json_path = os.path.join(DATA_DIR, f'{slug}.json')
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            taxonomy = data.get('taxonomy', {})
            city = taxonomy.get('city', '')
            category = taxonomy.get('category') or taxonomy.get('vertical') or ''
            if city:
                return city, category
        except Exception:
            pass

    # Fallback: parse from HTML title or hero badge
    html_path = os.path.join(POPULAR_PICKS_DIR, slug, 'index.html')
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Try <title> tag
        title_match = re.search(r'<title>([^<]+)</title>', content)
        if title_match:
            title = title_match.group(1)
            # Common patterns: "20 Best X in City, Country | tabiji.ai"
            city_match = re.search(r' in ([A-Z][^,|]+?)(?:,|\s*\|)', title)
            if city_match:
                return city_match.group(1).strip(), 'default'

        # Try hero badge
        badge_match = re.search(r'Popular Picks.*?—\s*[^<"]+?—\s*([^<"]+?)(?:,|<)', content)
        if badge_match:
            return badge_match.group(1).strip(), 'default'

    # Last resort: derive from slug
    parts = slug.replace('-', ' ').title()
    return parts, 'default'


def inject_into_page(html_path, slug, dry_run=False):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already injected
    if 'viator-section' in content:
        return 'skipped'

    city, category = get_city_and_category(slug)
    if not city:
        city = slug.replace('-', ' ').title()

    viator_html = render_viator_section(city, category)

    # Inject between FAQ section close and related-section
    # The FAQ ends with </section>, then optionally intent sections, then <section class="related-section">
    # We insert right after the FAQ </section> close (before intent or related)
    # Pattern: find </section> immediately before <section class="related-section"> or intent-section
    # Strategy: insert viator section right before <section class="related-section">
    related_pattern = re.compile(r'(\s*<section class="related-section")', re.MULTILINE)
    if related_pattern.search(content):
        new_content = related_pattern.sub(viator_html + r'\1', content, count=1)
    else:
        return 'no-related-section'

    # Add CSS to style block if not already present
    if 'viator-section {' not in new_content:
        # Insert before closing </style>
        new_content = new_content.replace('    </style>', VIATOR_CSS + '\n    </style>', 1)
        # Handle alternate style close
        if 'viator-section {' not in new_content:
            new_content = new_content.replace('</style>', VIATOR_CSS + '\n    </style>', 1)

    if dry_run:
        return 'dry-run-ok'

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return 'updated'


def main():
    parser = argparse.ArgumentParser(description='Inject Viator section into popular-picks pages')
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing')
    parser.add_argument('--slug', help='Process a single slug only')
    args = parser.parse_args()

    if args.slug:
        html_files = [os.path.join(POPULAR_PICKS_DIR, args.slug, 'index.html')]
    else:
        html_files = sorted(glob.glob(os.path.join(POPULAR_PICKS_DIR, '*/index.html')))

    counts = {'updated': 0, 'skipped': 0, 'no-related-section': 0, 'dry-run-ok': 0, 'error': 0}

    for html_path in html_files:
        slug = os.path.basename(os.path.dirname(html_path))
        try:
            result = inject_into_page(html_path, slug, dry_run=args.dry_run)
            counts[result] = counts.get(result, 0) + 1
            if result not in ('skipped',):
                print(f'[{result}] {slug}')
        except Exception as e:
            print(f'[error] {slug}: {e}')
            counts['error'] += 1

    print(f'\n--- Summary ---')
    for k, v in counts.items():
        if v:
            print(f'  {k}: {v}')


if __name__ == '__main__':
    main()
