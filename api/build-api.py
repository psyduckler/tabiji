#!/usr/bin/env python3
"""
Tabiji API v1 — Static JSON API Builder

Reads all tabiji data sources (destinations, popular-picks, itineraries, compare)
and generates static JSON files for a free REST API hosted on Cloudflare Pages.

Usage: python3 api/build-api.py
"""

import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing beautifulsoup4...")
    os.system("pip3 install --break-system-packages beautifulsoup4")
    from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "api" / "v1"
API_BASE_URL = "https://tabiji.ai/api/v1"
SITE_URL = "https://tabiji.ai"


def slugify(text):
    """Convert text to URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[àáâãäå]', 'a', text)
    text = re.sub(r'[èéêë]', 'e', text)
    text = re.sub(r'[ìíîï]', 'i', text)
    text = re.sub(r'[òóôõö]', 'o', text)
    text = re.sub(r'[ùúûü]', 'u', text)
    text = re.sub(r'[ñ]', 'n', text)
    text = re.sub(r'[ç]', 'c', text)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def clean_text(text):
    if not text:
        return ""
    text = BeautifulSoup(text, 'html.parser').get_text(' ', strip=True)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def split_quote_and_source(quote_div):
    source_span = quote_div.find('span', class_='source')
    source_text = clean_text(source_span.get_text(' ', strip=True)) if source_span else ""
    quote_clone = BeautifulSoup(str(quote_div), 'html.parser')
    source_clone = quote_clone.find('span', class_='source')
    if source_clone:
        source_clone.decompose()
    quote_text = clean_text(quote_clone.get_text(' ', strip=True)).strip('""“”')

    source_link = ""
    source_label = source_text
    if source_span:
        link = source_span.find('a', href=True)
        if link:
            source_link = link.get('href', '').strip()
            source_label = clean_text(source_span.get_text(' ', strip=True)).lstrip('— ').strip()

    return {
        "text": quote_text,
        "source": source_label,
        "sourceUrl": source_link,
    }


def make_unique_slug(base_slug, dest, used_slugs):
    slug = base_slug
    if slug not in used_slugs:
        used_slugs.add(slug)
        return slug

    candidates = [
        slugify(f"{dest.get('name', '')} {dest.get('region', '')}"),
        slugify(f"{dest.get('name', '')} {dest.get('continent', '')}"),
        slugify(f"{dest.get('name', '')} destination"),
    ]
    for candidate in candidates:
        if candidate and candidate not in used_slugs:
            used_slugs.add(candidate)
            return candidate

    counter = 2
    while f"{base_slug}-{counter}" in used_slugs:
        counter += 1
    slug = f"{base_slug}-{counter}"
    used_slugs.add(slug)
    return slug


def extract_json_ld(soup):
    """Extract all JSON-LD blocks from a page."""
    blocks = []
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string)
            blocks.append(data)
        except (json.JSONDecodeError, TypeError):
            continue
    return blocks


def find_json_ld_by_type(blocks, type_name):
    """Find a JSON-LD block by @type."""
    for block in blocks:
        if isinstance(block, dict) and block.get('@type') == type_name:
            return block
    return None


# ============================================================
# DESTINATIONS
# ============================================================

def build_destinations():
    src = BASE_DIR / "find" / "destinations.json"
    if not src.exists():
        print("  ⚠️  destinations.json not found")
        return [], 0

    with open(src) as f:
        destinations = json.load(f)

    dest_dir = OUTPUT_DIR / "destinations"
    dest_dir.mkdir(parents=True, exist_ok=True)

    summaries = []
    used_slugs = set()
    for dest in destinations:
        slug = make_unique_slug(slugify(dest.get("name", "")), dest, used_slugs)
        if not slug:
            continue

        detail = {
            "slug": slug,
            "name": dest.get("name", ""),
            "region": dest.get("region", ""),
            "continent": dest.get("continent", ""),
            "photo": dest.get("photo", ""),
            "pitch": dest.get("pitch", ""),
            "budget": dest.get("budget", ""),
            "season": dest.get("season", ""),
            "vibes": dest.get("vibes", []),
            "travelStyles": dest.get("travel", []),
            "url": f"{SITE_URL}/find/?q={slug}"
        }

        with open(dest_dir / f"{slug}.json", 'w') as f:
            json.dump(detail, f, indent=2, ensure_ascii=False)

        summaries.append({
            "slug": slug,
            "name": dest.get("name", ""),
            "region": dest.get("region", ""),
            "continent": dest.get("continent", ""),
            "budget": dest.get("budget", ""),
            "season": dest.get("season", ""),
            "vibes": dest.get("vibes", []),
            "photo": dest.get("photo", ""),
            "pitch": dest.get("pitch", "")
        })

    with open(OUTPUT_DIR / "destinations.json", 'w') as f:
        json.dump({"count": len(summaries), "destinations": summaries}, f, indent=2, ensure_ascii=False)

    return summaries, len(summaries)


# ============================================================
# POPULAR PICKS
# ============================================================

def normalize_price_range(text):
    text = clean_text(text)
    text = re.sub(r'^[💰💶💴🪙]+\s*', '', text)
    return text.strip()


def extract_pick_places(soup, slug):
    places = []
    sections = soup.find_all('section', class_='restaurant-section')

    for section in sections:
        place = {}
        h2 = section.find('h2')
        if h2:
            num_span = h2.find('span', class_='restaurant-number')
            number = clean_text(num_span.get_text()) if num_span else ""
            name_text = clean_text(h2.get_text())
            if number and name_text.startswith(number):
                name_text = name_text[len(number):].strip()
            place["name"] = name_text
            place["position"] = int(number) if number.isdigit() else None

        tags = section.find_all('span', class_=lambda x: x and 'cuisine-tag' in x)
        if tags:
            place["cuisineTags"] = [clean_text(t.get_text()) for t in tags]

        rating_span = section.find('span', class_='google-rating')
        if rating_span:
            match = re.search(r'([\d.]+)\s*[·•]\s*([\d,]+)', rating_span.get_text(strip=True))
            if match:
                place["googleRating"] = float(match.group(1))
                place["reviewCount"] = int(match.group(2).replace(',', ''))

        details = section.find('div', class_='restaurant-details')
        if details:
            for span in details.find_all('span'):
                text = clean_text(span.get_text())
                if any(c in text for c in ['💰', '💶', '💴', '¥', '€', '$', '£', '🪙']):
                    place["priceRange"] = normalize_price_range(text)
                elif '📍' in text:
                    place["address"] = text.replace('📍', '').strip()
            maps_link = details.find('a', href=re.compile(r'maps\.google|google.*maps|goo\.gl/maps'))
            if maps_link:
                place["googleMapsUrl"] = maps_link.get('href', '')

        hours_div = section.find('div', class_='shop-hours')
        if hours_div:
            hours_grid = hours_div.find('div', class_='hours-grid')
            if hours_grid:
                spans = hours_grid.find_all('span')
                hours = {}
                for i in range(0, len(spans) - 1, 2):
                    hours[clean_text(spans[i].get_text())] = clean_text(spans[i + 1].get_text())
                if hours:
                    place["openingHours"] = hours
            summary = hours_div.find('summary')
            if summary:
                status_text = clean_text(summary.get_text())
                if 'Open' in status_text:
                    place["openNow"] = True
                elif 'Closed' in status_text:
                    place["openNow"] = False

        contact = section.find('div', class_='shop-contact')
        if contact:
            phone_link = contact.find('a', href=re.compile(r'tel:'))
            if phone_link:
                place["phone"] = phone_link.get('href', '').replace('tel:', '')
            website_link = contact.find('a', href=re.compile(r'^https?://'))
            if website_link and 'maps.google' not in website_link.get('href', ''):
                place["website"] = website_link.get('href', '')

        img = section.find('img')
        if img and img.get('src'):
            place["photo"] = img.get('src', '')

        quotes = section.find_all('div', class_='reddit-quote')
        if quotes:
            place["redditQuotes"] = [split_quote_and_source(q) for q in quotes]

        verdict_box = section.find('div', class_='pick-quick-take')
        if verdict_box:
            place["verdict"] = clean_text(verdict_box.get_text()).replace('Verdict:', '').strip()

        comparison_card = section.find('div', class_='comparison-card')
        if comparison_card:
            comparison = {}
            for row in comparison_card.find_all('div', class_='comparison-row'):
                dt = row.find('dt')
                dd = row.find('dd')
                if not dt or not dd:
                    continue
                key = clean_text(dt.get_text()).lower()
                value = clean_text(dd.get_text())
                comparison[key] = value
            if comparison:
                place["comparison"] = comparison
                if not place.get("whatToOrder") and comparison.get("what to order"):
                    place["whatToOrder"] = comparison.get("what to order")
                if not place.get("insiderTip") and comparison.get("why it made the list"):
                    place["insiderTip"] = comparison.get("why it made the list")

        if place.get("name"):
            places.append(place)

    return places


def extract_pick_places_generic(soup, slug):
    return []


def extract_pick_places_alt(soup, slug):
    return []


def extract_meta_content(soup, attr_name, attr_value):
    tag = soup.find('meta', attrs={attr_name: attr_value})
    return tag.get('content', '').strip() if tag and tag.get('content') else ''


def extract_pick_hub_cards(soup):
    cards = []
    for link in soup.find_all('a', class_='pick-card'):
        href = link.get('href', '').strip()
        if not href:
            continue
        title_el = link.find(['h2', 'h3'])
        desc_el = link.find('p')
        badge_el = link.find(class_='card-badge')
        img_el = link.find('img')
        slug = href.strip('/').split('/')[-1] if href else ''
        cards.append({
            "name": clean_text(title_el.get_text()) if title_el else slug,
            "slug": slug,
            "url": f"{SITE_URL}{href}" if href.startswith('/') else href,
            "description": clean_text(desc_el.get_text()) if desc_el else '',
            "badge": clean_text(badge_el.get_text()) if badge_el else '',
            "photo": img_el.get('src', '').strip() if img_el else '',
        })
    return cards


def build_picks():
    picks_dir = BASE_DIR / "popular-picks"
    if not picks_dir.exists():
        print("  ⚠️  popular-picks/ not found")
        return [], 0

    output_picks_dir = OUTPUT_DIR / "picks"
    output_picks_dir.mkdir(parents=True, exist_ok=True)

    summaries = []
    total_places = 0
    slugs = sorted([d for d in os.listdir(picks_dir) if (picks_dir / d / "index.html").exists()])

    for slug in slugs:
        html_path = picks_dir / slug / "index.html"
        try:
            html = html_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"  ⚠️  Error reading {slug}: {e}")
            continue

        soup = BeautifulSoup(html, 'html.parser')
        json_ld = extract_json_ld(soup)
        article = find_json_ld_by_type(json_ld, 'Article')

        title = article.get('headline', '') if article else ""
        desc = article.get('description', '') if article else ""
        if not title:
            title_tag = soup.find('title')
            title = title_tag.text.strip().split('|')[0].strip() if title_tag else slug

        city = ""
        city_match = re.search(r'(?:in|of)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', title)
        if city_match:
            city = city_match.group(1)

        category = ""
        cat_match = re.search(r'Best\s+(.+?)\s+(?:in|of|for)', title, re.IGNORECASE)
        if cat_match:
            category = cat_match.group(1).strip()

        places = extract_pick_places(soup, slug)
        is_hub_page = False
        if not places:
            places = extract_pick_hub_cards(soup)
            is_hub_page = len(places) > 0
        total_places += len(places)

        hero_img = article.get('image', '') if article else ''
        if isinstance(hero_img, list):
            hero_img = hero_img[0] if hero_img else ''
        if not hero_img:
            hero_img = extract_meta_content(soup, 'property', 'og:image') or extract_meta_content(soup, 'name', 'twitter:image')
        if not desc:
            desc = extract_meta_content(soup, 'name', 'description')
        if not city and is_hub_page:
            h1 = soup.find('h1')
            if h1:
                city = clean_text(h1.get_text())

        detail = {
            "slug": slug,
            "title": title,
            "description": desc,
            "city": city,
            "category": category,
            "heroImage": hero_img,
            "placeCount": len(places),
            "url": f"{SITE_URL}/popular-picks/{slug}/",
            "places": places
        }

        with open(output_picks_dir / f"{slug}.json", 'w') as f:
            json.dump(detail, f, indent=2, ensure_ascii=False)

        summaries.append({
            "slug": slug,
            "title": title,
            "city": city,
            "category": category,
            "placeCount": len(places),
            "url": f"{SITE_URL}/popular-picks/{slug}/"
        })

    with open(OUTPUT_DIR / "picks.json", 'w') as f:
        json.dump({"count": len(summaries), "totalPlaces": total_places, "picks": summaries}, f, indent=2, ensure_ascii=False)

    return summaries, total_places


# ============================================================
# ITINERARIES
# ============================================================

def extract_itinerary_days(soup):
    days = []
    for day_div in soup.find_all('div', class_='day'):
        day = {}
        day_header = day_div.find('div', class_='day-header')
        if day_header:
            day_num = day_header.find('span', class_='day-num')
            day_neighborhoods = day_header.find('span', class_='day-neighborhoods')
            if day_num:
                day["dayLabel"] = clean_text(day_num.get_text())
            if day_neighborhoods:
                day["neighborhoods"] = clean_text(day_neighborhoods.get_text())

        h2 = day_div.find('h2')
        if h2:
            day["title"] = clean_text(h2.get_text())
            title_lower = day["title"].lower()
            if any(skip in title_lower for skip in ['at a glance', 'overview', 'essentials', 'before you go', 'packing', 'seasonal', 'tips', 'budget', 'faq']):
                continue

        first_p = day_div.find('p')
        if first_p and not first_p.find_parent('div', class_='time-block'):
            day["description"] = clean_text(first_p.get_text())

        activities = []
        for tb in day_div.find_all('div', class_='time-block'):
            activity = {}
            time_label = tb.find('div', class_='time-label')
            if time_label:
                activity["time"] = clean_text(time_label.get_text())
            h3 = tb.find('h3')
            if h3:
                activity["name"] = clean_text(h3.get_text())
            paras = tb.find_all('p')
            if paras:
                activity["description"] = ' '.join(clean_text(p.get_text()) for p in paras[:2])
            if activity.get("name"):
                activities.append(activity)

        if activities:
            day["activities"] = activities
        if day.get("title") or day.get("activities"):
            days.append(day)
    return days


def parse_itinerary_page(html_path, slug, source_dir):
    try:
        html = html_path.read_text(encoding='utf-8')
    except Exception:
        return None

    soup = BeautifulSoup(html, 'html.parser')
    json_ld = extract_json_ld(soup)
    article = find_json_ld_by_type(json_ld, 'Article')
    tourist_trip = find_json_ld_by_type(json_ld, 'TouristTrip')

    title = article.get('headline', '') if article else ""
    desc = article.get('description', '') if article else ""
    hero_image = article.get('image', '') if article else ""
    trip_type = tourist_trip.get('touristType', []) if tourist_trip else []

    if not title:
        title_tag = soup.find('title')
        title = title_tag.text.strip().split('|')[0].strip() if title_tag else slug

    destination = ""
    if source_dir == "itineraries":
        parts = slug.split('-')
        if len(parts) >= 3 and parts[0].isdigit() and parts[1] == 'day':
            destination = parts[2].replace('-', ' ').title()
    if not destination:
        dest_match = re.match(r'^(\d+)-(?:day|days|night|nights)-([a-z0-9-]+)', slug)
        if dest_match:
            destination = dest_match.group(2).split('-')[0].title()
    if not destination:
        dest_match2 = re.search(r'in\s+([A-Z][a-z]+(?:[\s-][A-Z][a-z]+)*)', title)
        if dest_match2:
            destination = dest_match2.group(1)

    duration = ""
    dur_match = re.match(r'^(\d+)-(?:day|days|night|nights)', slug)
    if dur_match:
        duration = f"{dur_match.group(1)} days"
    if not duration:
        dur_title = re.search(r'(\d+)\s*(?:Day|Night)', title, re.IGNORECASE)
        if dur_title:
            duration = f"{dur_title.group(1)} days"

    days = extract_itinerary_days(soup)
    url = f"{SITE_URL}/i/{slug}/" if source_dir == "i" else f"{SITE_URL}/itineraries/{slug}/"

    return {
        "slug": slug,
        "title": title,
        "description": desc,
        "destination": destination,
        "duration": duration,
        "tripType": trip_type if isinstance(trip_type, list) else [trip_type] if trip_type else [],
        "heroImage": hero_image,
        "url": url,
        "source": source_dir,
        "dayCount": len(days),
        "days": days
    }


def build_itineraries():
    output_itin_dir = OUTPUT_DIR / "itineraries"
    output_itin_dir.mkdir(parents=True, exist_ok=True)

    summaries = []
    all_itineraries = []
    for source_dir in ["i", "itineraries"]:
        src_path = BASE_DIR / source_dir
        if not src_path.exists():
            continue
        slugs = sorted([d for d in os.listdir(src_path) if (src_path / d / "index.html").exists()])
        for slug in slugs:
            result = parse_itinerary_page(src_path / slug / "index.html", slug, source_dir)
            if result:
                all_itineraries.append(result)

    for itin in all_itineraries:
        filename = f"{itin['source']}-{itin['slug']}" if itin["source"] == "itineraries" else itin["slug"]
        with open(output_itin_dir / f"{filename}.json", 'w') as f:
            json.dump(itin, f, indent=2, ensure_ascii=False)
        summaries.append({
            "slug": filename,
            "title": itin["title"],
            "destination": itin["destination"],
            "duration": itin["duration"],
            "tripType": itin["tripType"],
            "url": itin["url"],
            "dayCount": itin["dayCount"]
        })

    with open(OUTPUT_DIR / "itineraries.json", 'w') as f:
        json.dump({"count": len(summaries), "itineraries": summaries}, f, indent=2, ensure_ascii=False)
    return summaries, len(summaries)


# ============================================================
# COMPARE
# ============================================================

def build_compare():
    compare_dir = BASE_DIR / "compare"
    if not compare_dir.exists():
        print("  ⚠️  compare/ not found")
        return [], 0

    output_compare_dir = OUTPUT_DIR / "compare"
    output_compare_dir.mkdir(parents=True, exist_ok=True)

    summaries = []
    slugs = sorted([d for d in os.listdir(compare_dir) if (compare_dir / d / "index.html").exists()])

    for slug in slugs:
        html_path = compare_dir / slug / "index.html"
        try:
            html = html_path.read_text(encoding='utf-8')
        except Exception:
            continue

        soup = BeautifulSoup(html, 'html.parser')
        json_ld = extract_json_ld(soup)
        article = find_json_ld_by_type(json_ld, 'Article')
        faq = find_json_ld_by_type(json_ld, 'FAQPage')

        title = article.get('headline', '') if article else ""
        desc = article.get('description', '') if article else ""
        hero_image = article.get('image', '') if article else ""
        if not title:
            title_tag = soup.find('title')
            title = title_tag.text.strip().split('|')[0].strip() if title_tag else slug

        parts = slug.split('-vs-')
        destination1 = parts[0].replace('-', ' ').title() if len(parts) >= 2 else ""
        destination2 = parts[1].replace('-', ' ').title() if len(parts) >= 2 else ""

        categories = []
        for dd in soup.find_all('section', class_='deep-dive'):
            h2 = dd.find('h2')
            if not h2:
                continue
            category = {"title": clean_text(h2.get_text())}
            paragraphs = [clean_text(p.get_text()) for p in dd.find_all('p') if clean_text(p.get_text())]
            if paragraphs:
                category["summary"] = paragraphs[0]
                if len(paragraphs) > 1:
                    category["highlights"] = paragraphs[1:3]
            quotes = dd.find_all('div', class_='reddit-quote')
            if quotes:
                category["redditQuotes"] = [split_quote_and_source(q) for q in quotes[:3]]
            winner_box = dd.find('div', class_='section-winner')
            if winner_box:
                winner_items = {}
                for li in winner_box.find_all('li'):
                    text = clean_text(li.get_text())
                    if ':' in text:
                        k, v = text.split(':', 1)
                        winner_items[slugify(k).replace('-', '_')] = v.strip()
                if winner_items:
                    category["winnerSummary"] = winner_items
            categories.append(category)

        verdict = {}
        verdict_box = soup.find('div', class_='verdict-box')
        if verdict_box:
            summary = verdict_box.find('p', class_='verdict-summary')
            if summary:
                verdict["summary"] = clean_text(summary.get_text())
            takeaways = []
            for li in verdict_box.find_all('ul', class_='verdict-takeaways'):
                takeaways.extend([clean_text(item.get_text()) for item in li.find_all('li')])
            if takeaways:
                verdict["takeaways"] = takeaways
            cards = []
            for card in verdict_box.find_all('div', class_='verdict-card'):
                heading = card.find(['h3', 'h4'])
                body = card.find('p')
                cards.append({
                    "title": clean_text(heading.get_text()) if heading else "",
                    "text": clean_text(body.get_text()) if body else "",
                })
            cards = [c for c in cards if c['title'] or c['text']]
            if cards:
                verdict["cards"] = cards

        faqs = []
        if faq and faq.get('mainEntity'):
            for q in faq['mainEntity']:
                faqs.append({
                    "question": q.get('name', ''),
                    "answer": q.get('acceptedAnswer', {}).get('text', '')
                })

        detail = {
            "slug": slug,
            "title": title,
            "description": desc,
            "destination1": destination1,
            "destination2": destination2,
            "heroImage": hero_image,
            "url": f"{SITE_URL}/compare/{slug}/",
            "categoryCount": len(categories),
            "categories": categories,
            "verdict": verdict,
            "faqs": faqs
        }

        with open(output_compare_dir / f"{slug}.json", 'w') as f:
            json.dump(detail, f, indent=2, ensure_ascii=False)

        summaries.append({
            "slug": slug,
            "title": title,
            "destination1": destination1,
            "destination2": destination2,
            "categoryCount": len(categories),
            "url": f"{SITE_URL}/compare/{slug}/"
        })

    with open(OUTPUT_DIR / "compare.json", 'w') as f:
        json.dump({"count": len(summaries), "comparisons": summaries}, f, indent=2, ensure_ascii=False)
    return summaries, len(summaries)


def build_search(dest_summaries, pick_summaries, itin_summaries, compare_summaries):
    records = []
    for d in dest_summaries:
        records.append({
            "type": "destination",
            "slug": d["slug"],
            "title": d["name"],
            "subtitle": d.get("pitch", ""),
            "region": d.get("region", ""),
            "continent": d.get("continent", ""),
            "url": f"{API_BASE_URL}/destinations/{d['slug']}.json",
            "siteUrl": f"{SITE_URL}/find/?q={d['slug']}",
            "tokens": [d.get("name", ""), d.get("region", ""), d.get("continent", ""), ' '.join(d.get("vibes", []))]
        })
    for p in pick_summaries:
        records.append({
            "type": "pick",
            "slug": p["slug"],
            "title": p["title"],
            "subtitle": p.get("category", ""),
            "city": p.get("city", ""),
            "url": f"{API_BASE_URL}/picks/{p['slug']}.json",
            "siteUrl": p["url"],
            "tokens": [p.get("title", ""), p.get("city", ""), p.get("category", "")]
        })
    for i in itin_summaries:
        records.append({
            "type": "itinerary",
            "slug": i["slug"],
            "title": i["title"],
            "subtitle": i.get("duration", ""),
            "destination": i.get("destination", ""),
            "url": f"{API_BASE_URL}/itineraries/{i['slug']}.json",
            "siteUrl": i["url"],
            "tokens": [i.get("title", ""), i.get("destination", ""), i.get("duration", "")]
        })
    for c in compare_summaries:
        records.append({
            "type": "comparison",
            "slug": c["slug"],
            "title": c["title"],
            "destination1": c.get("destination1", ""),
            "destination2": c.get("destination2", ""),
            "url": f"{API_BASE_URL}/compare/{c['slug']}.json",
            "siteUrl": c["url"],
            "tokens": [c.get("title", ""), c.get("destination1", ""), c.get("destination2", "")]
        })

    payload = {
        "count": len(records),
        "types": {
            "destinations": len(dest_summaries),
            "picks": len(pick_summaries),
            "itineraries": len(itin_summaries),
            "comparisons": len(compare_summaries),
        },
        "items": records,
    }
    with open(OUTPUT_DIR / "search-index.json", 'w') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return payload


# ============================================================
# INDEX
# ============================================================

def build_index(dest_count, picks_count, places_count, itin_count, compare_count, search_count):
    index = {
        "name": "tabiji.ai API",
        "version": "1.0.0",
        "description": "Free REST API for AI-curated travel data — destinations, restaurant picks, itineraries, comparisons, and unified search. No API key required.",
        "baseUrl": API_BASE_URL,
        "documentation": f"{SITE_URL}/api/",
        "openapi": f"{SITE_URL}/api/openapi.json",
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stats": {
            "destinations": dest_count,
            "picksGuides": picks_count,
            "totalPlaces": places_count,
            "itineraries": itin_count,
            "comparisons": compare_count,
            "searchDocuments": search_count,
        },
        "endpoints": [
            {"path": "/destinations.json", "description": f"All {dest_count} destinations with budget, season, vibes, and travel styles", "method": "GET"},
            {"path": "/destinations/{slug}.json", "description": "Single destination detail", "method": "GET"},
            {"path": "/picks.json", "description": f"All {picks_count} curated 'best of' guides", "method": "GET"},
            {"path": "/picks/{slug}.json", "description": "Full picks guide with all places, ratings, hours, and quotes", "method": "GET"},
            {"path": "/itineraries.json", "description": f"All {itin_count} day-by-day travel itineraries", "method": "GET"},
            {"path": "/itineraries/{slug}.json", "description": "Full itinerary with day-by-day activities", "method": "GET"},
            {"path": "/compare.json", "description": f"All {compare_count} head-to-head destination comparisons", "method": "GET"},
            {"path": "/compare/{slug}.json", "description": "Full comparison with structured verdicts, categories, and FAQs", "method": "GET"},
            {"path": "/search.json?q={query}", "description": f"Cross-collection search across {search_count} documents", "method": "GET"},
        ],
        "dataSource": "Curated from Reddit discussions, enriched with Google Places data (ratings, hours, maps links).",
        "license": "Free for non-commercial use. Attribution appreciated: tabiji.ai",
        "contact": "hello@tabiji.ai"
    }
    with open(OUTPUT_DIR / "index.json", 'w') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


def main():
    print("🦉 Building Tabiji API v1...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("📍 Building destinations...")
    dest_summaries, dest_count = build_destinations()
    print(f"   ✅ {dest_count} destinations")

    print("🍜 Building popular picks...")
    picks_summaries, places_count = build_picks()
    picks_count = len(picks_summaries)
    print(f"   ✅ {picks_count} guides, {places_count} total places")

    print("🗺️  Building itineraries...")
    itin_summaries, itin_count = build_itineraries()
    print(f"   ✅ {itin_count} itineraries")

    print("⚔️  Building comparisons...")
    compare_summaries, compare_count = build_compare()
    print(f"   ✅ {compare_count} comparisons")

    print("🔎 Building search index...")
    search_payload = build_search(dest_summaries, picks_summaries, itin_summaries, compare_summaries)
    print(f"   ✅ {search_payload['count']} documents")

    print("📋 Building index...")
    build_index(dest_count, picks_count, places_count, itin_count, compare_count, search_payload['count'])
    print("   ✅ index.json")


if __name__ == "__main__":
    main()
