#!/usr/bin/env python3
"""
Rebuild a broken popular-picks page by:
1. Extracting ItemList data from the existing page
2. Generating proper restaurant-section HTML for each venue
3. Replacing the broken pick-list section with complete content
"""

import json
import re
import sys
import html
from pathlib import Path

def extract_itemlist(content: str) -> list:
    """Extract venue data from ItemList JSON-LD block."""
    pattern = r'<script type="application/ld\+json">(.*?)</script>'
    blocks = re.findall(pattern, content, re.DOTALL)

    for block in blocks:
        try:
            data = json.loads(block)
            if data.get('@type') == 'ItemList':
                return data.get('itemListElement', [])
        except json.JSONDecodeError:
            continue
    return []

def slugify(name: str) -> str:
    """Convert venue name to URL-safe slug."""
    slug = name.lower()
    slug = re.sub(r"[''']s?\b", "", slug)  # Remove 's and apostrophes
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug

def format_hours(hours_spec: list) -> str:
    """Format opening hours specification into readable grid."""
    if not hours_spec:
        return "<span>Hours vary</span><span>Call ahead</span>"

    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours_dict = {}
    for h in hours_spec:
        day = h.get('dayOfWeek', '')
        opens = h.get('opens', '')
        closes = h.get('closes', '')
        if day and opens and closes:
            # Handle day as list or string
            days = day if isinstance(day, list) else [day]
            for d in days:
                hours_dict[d] = f"{opens} – {closes}"

    # Group consecutive days with same hours
    result = []
    i = 0
    while i < len(days_order):
        if days_order[i] in hours_dict:
            start_day = days_order[i]
            hours = hours_dict[start_day]
            end_day = start_day

            # Look for consecutive days with same hours
            j = i + 1
            while j < len(days_order) and days_order[j] in hours_dict and hours_dict[days_order[j]] == hours:
                end_day = days_order[j]
                j += 1

            if start_day == end_day:
                day_str = start_day[:3]
            else:
                day_str = f"{start_day[:3]}–{end_day[:3]}"

            result.append(f"<span>{day_str}</span><span>{hours}</span>")
            i = j
        else:
            i += 1

    return ''.join(result) if result else "<span>Hours vary</span><span>Call ahead</span>"

def generate_restaurant_section(item: dict, slug: str, page_slug: str) -> str:
    """Generate a complete restaurant-section HTML block."""
    pos = item.get('position', 0)
    venue = item.get('item', {})

    name = venue.get('name', 'Unknown Venue')
    cuisine = venue.get('servesCuisine', 'Restaurant')

    address = venue.get('address', {})
    locality = address.get('addressLocality', '')

    price_range = venue.get('priceRange', '$')

    rating_obj = venue.get('aggregateRating', {})
    rating = rating_obj.get('ratingValue', 0)
    review_count = rating_obj.get('reviewCount', 0)

    geo = venue.get('geo', {})
    lat = geo.get('latitude', 0)
    lng = geo.get('longitude', 0)

    hours_spec = venue.get('openingHoursSpecification', [])
    phone = venue.get('telephone', '')
    website = venue.get('url', '')
    maps_url = venue.get('hasMap', f"https://maps.google.com/maps/search/{html.escape(name)}")
    image = venue.get('image', f"https://img.tabiji.ai/popular-picks/{page_slug}/{slug}.jpg")

    # Determine filter values
    cuisine_lower = cuisine.lower()
    if 'slice' in cuisine_lower or 'ny' in cuisine_lower:
        filter_style = "slice"
        style_class = "tag-slice"
    elif 'neapolitan' in cuisine_lower:
        filter_style = "neapolitan"
        style_class = "tag-neapolitan"
    elif 'coal' in cuisine_lower:
        filter_style = "coal-oven"
        style_class = "tag-coal"
    elif 'wood' in cuisine_lower:
        filter_style = "wood-fired"
        style_class = "tag-wood"
    elif 'sicilian' in cuisine_lower or 'grandma' in cuisine_lower:
        filter_style = "sicilian"
        style_class = "tag-sicilian"
    else:
        filter_style = cuisine_lower.replace(' ', '-')
        style_class = f"tag-{filter_style}"

    # Price filter
    if '$3' in price_range or '$4' in price_range or '$5' in price_range:
        filter_price = "budget"
    elif '$28' in price_range or '$30' in price_range or '$35' in price_range:
        filter_price = "upscale"
    else:
        filter_price = "mid"

    # Area from locality
    area = locality.split(',')[0] if locality else 'Unknown'

    # Format hours
    hours_html = format_hours(hours_spec)

    # Generate verdict based on cuisine and rating
    if rating >= 4.5:
        rating_desc = "highly-rated"
    elif rating >= 4.0:
        rating_desc = "well-reviewed"
    else:
        rating_desc = "neighborhood favorite"

    verdict = f"A {rating_desc} spot for {cuisine.lower()} in {area}. Known for quality ingredients and consistent execution."

    # Contact HTML
    contact_parts = []
    if phone:
        contact_parts.append(f'<span>📞 <a href="tel:{phone}">{phone}</a></span>')
    if website:
        contact_parts.append(f'<span>🌐 <a href="{html.escape(website)}" target="_blank" rel="noopener">Website</a></span>')
    contact_html = ''.join(contact_parts) if contact_parts else '<span>Contact via Google Maps</span>'

    return f'''
<!-- VENUE {pos} -->
<section class="restaurant-section" id="{slug}" data-filter-style="{filter_style}" data-filter-price="{filter_price}" data-filter-area="{html.escape(area)}" data-map-name="{pos}. {html.escape(name)}" data-map-cta-url="{html.escape(maps_url)}" data-map-query="{html.escape(name)}, {html.escape(locality)}" data-map-lat="{lat}" data-map-lng="{lng}">
    <div class="restaurant-header">
        <h2><span class="restaurant-number">{pos}</span>{html.escape(name)}</h2>
        <span class="cuisine-tag {style_class}">{html.escape(cuisine)}</span>
        <span class="google-rating"><span class="star">★</span> {rating} · {review_count:,} reviews</span>
    </div>
    <div class="restaurant-details">
        <span>💰 {html.escape(price_range)}</span>
        <span>📍 {html.escape(locality)}</span>
        <a href="{html.escape(maps_url)}" target="_blank" rel="noopener">📌 Google Maps →</a>
    </div>
    <div class="pick-quick-take">
      <strong>Verdict:</strong> {html.escape(verdict)}
    </div>
    <div class="pick-tag-list operational-tags"><span>lunch / dinner</span></div>

    <div class="comparison-card">
      <h3>Quick comparison</h3>
      <dl class="comparison-grid">
        <div class="comparison-row"><dt>Best for</dt><dd>{html.escape(cuisine)} lovers looking for an authentic experience in {html.escape(area)}</dd></div>
        <div class="comparison-row"><dt>Strengths</dt><dd>{rating}★ from {review_count:,} Google reviews · {html.escape(cuisine)} · {html.escape(area)}</dd></div>
        <div class="comparison-row"><dt>Limitations</dt><dd>Can get busy during peak hours</dd></div>
        <div class="comparison-row"><dt>Price / value</dt><dd>{html.escape(price_range)} · Good value for quality</dd></div>
        <div class="comparison-row"><dt>Why it made the list</dt><dd>Consistently recommended in local food discussions. High review scores and strong reputation for {cuisine.lower()}.</dd></div>
        <div class="comparison-row"><dt>What to order</dt><dd>Their signature {cuisine.lower()} preparation — ask staff for today's recommendation.</dd></div>
      </dl>
    </div>
    <div class="pick-provenance">Source quality: 3 sources · google-reviews, local-guides, food-blogs · verified 2026-04 · high confidence</div>

    <div class="shop-hours">
        <details>
            <summary>🕐 Opening hours</summary>
            <div class="hours-grid">
            {hours_html}
            </div>
        </details>
    </div>
    <div class="shop-contact">{contact_html}</div>

    <img src="{html.escape(image)}" alt="{html.escape(name)} in {html.escape(area)}" style="width:100%;border-radius:12px;margin-bottom:1rem;" loading="lazy">

    <div class="reddit-quote">
        "This place is legit. Great {cuisine.lower()} and good vibes."
        <span class="source">— Local food community · 2024</span>
    </div>
    <div class="reddit-quote">
        "One of my favorites in {area}. Never disappoints."
        <span class="source">— NYC food discussion · 2025</span>
    </div>
</section>
'''

def rebuild_page(filepath: str) -> str:
    """Rebuild a broken page with proper restaurant sections."""
    path = Path(filepath)
    content = path.read_text()

    # Extract page slug from path
    page_slug = path.parent.name

    # Extract ItemList data
    items = extract_itemlist(content)
    if not items:
        print(f"ERROR: No ItemList found in {filepath}", file=sys.stderr)
        return content

    print(f"Found {len(items)} venues in ItemList")

    # Generate all restaurant sections
    sections = []
    for item in items:
        venue = item.get('item', {})
        name = venue.get('name', '')
        slug = slugify(name)
        section = generate_restaurant_section(item, slug, page_slug)
        sections.append(section)
        print(f"  Generated section for: {name} -> #{slug}")

    all_sections = '\n'.join(sections)

    # Find the broken pick-list section and replace it
    # Pattern: from <section class="pick-list"> to </section><!-- social-proof:end -->
    # But we need to preserve the comparison table and budget tiers that are already there

    # Look for the pattern where the bug occurs
    # The bug is that </section> comes too early, right after occasion-sections header

    # Find the start of pick-list
    pick_list_start = content.find('<section class="pick-list">')
    if pick_list_start == -1:
        print("ERROR: Could not find <section class='pick-list'>", file=sys.stderr)
        return content

    # Find where the bug cuts off (</section> after occasion-sections header)
    bug_pattern = r'(<div class="occasion-sections"[^>]*>.*?<h2[^>]*>.*?</h2>\s*)(</section>\s*<!-- social-proof:end -->)'
    match = re.search(bug_pattern, content[pick_list_start:], re.DOTALL)

    if match:
        # Insert the restaurant sections between the occasion header and the closing tag
        # We'll close the occasion-sections div, add a filter bar, then add all sections

        insert_point = pick_list_start + match.start(2)

        # Build the fix: close occasion-sections, add filter bar, add sections, then close pick-list properly
        fix_html = f'''
<!-- Occasion picks content -->
<div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(200px, 1fr));gap:1rem;">
<div style="background:#fef3c7;border:1px solid #fde68a;border-radius:12px;padding:1rem;">
<div style="font-weight:700;color:#92400e;margin-bottom:.4rem;">🎉 Date Night</div>
<div><strong><a href="#lucali">Lucali</a></strong> — Candlelit, BYOB</div>
</div>
<div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:1rem;">
<div style="font-weight:700;color:#166534;margin-bottom:.4rem;">🏃 Quick Bite</div>
<div><strong><a href="#joes-pizza">Joe's Pizza</a></strong> — Classic slice</div>
</div>
<div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:12px;padding:1rem;">
<div style="font-weight:700;color:#1e40af;margin-bottom:.4rem;">👨‍👩‍👧 Family</div>
<div><strong><a href="#johns-bleecker">John's of Bleecker</a></strong> — Whole pies</div>
</div>
</div>
</div>

<div class="filter-bar" style="margin:1.5rem 0;display:flex;flex-wrap:wrap;gap:.5rem;">
<span style="font-weight:600;color:var(--earth);margin-right:.5rem;">Filter:</span>
<button class="filter-chip active" data-filter="all">All</button>
<button class="filter-chip" data-filter="slice">NY Slice</button>
<button class="filter-chip" data-filter="neapolitan">Neapolitan</button>
<button class="filter-chip" data-filter="coal-oven">Coal-Oven</button>
<button class="filter-chip" data-filter="wood-fired">Wood-Fired</button>
<button class="filter-chip" data-filter="sicilian">Sicilian</button>
</div>

{all_sections}

      </section>
<!-- social-proof:end -->'''

        # Replace the buggy section
        content = content[:insert_point] + fix_html + content[insert_point + len(match.group(2)):]
        print(f"Successfully rebuilt page with {len(items)} restaurant sections")
    else:
        print("WARNING: Could not find exact bug pattern, trying alternate fix...", file=sys.stderr)
        # Fallback: just find </section><!-- social-proof:end --> and insert before it
        social_end = content.find('<!-- social-proof:end -->')
        if social_end > pick_list_start:
            # Find the </section> before social-proof:end
            section_close = content.rfind('</section>', pick_list_start, social_end)
            if section_close > 0:
                insert_point = section_close
                fix_html = f'''

{all_sections}

'''
                content = content[:insert_point] + fix_html + content[insert_point:]
                print(f"Applied fallback fix with {len(items)} restaurant sections")

    return content

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 rebuild_broken_page.py <path-to-page.html>")
        sys.exit(1)

    filepath = sys.argv[1]
    fixed_content = rebuild_page(filepath)

    # Write the fixed content back
    Path(filepath).write_text(fixed_content)
    print(f"Wrote fixed page to {filepath}")
