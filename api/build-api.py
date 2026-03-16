#!/usr/bin/env python3
"""
Tabiji API v1 — Static JSON API Builder

Reads all tabiji data sources (destinations, popular-picks, itineraries, compare)
and generates static JSON files for a free REST API hosted on Cloudflare Pages.

Usage:
  python3 -m pip install -r api/requirements.txt
  python3 api/build-api.py
"""

import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

try:
    from bs4 import BeautifulSoup
except ImportError as exc:
    print(
        "Missing dependency: beautifulsoup4\n"
        "Install API build dependencies first:\n"
        "  python3 -m pip install -r api/requirements.txt",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc


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
    """Build destinations JSON from find/destinations.json."""
    src = BASE_DIR / "find" / "destinations.json"
    if not src.exists():
        print("  ⚠️  destinations.json not found")
        return [], 0

    with open(src) as f:
        destinations = json.load(f)

    # Build individual destination files
    dest_dir = OUTPUT_DIR / "destinations"
    dest_dir.mkdir(parents=True, exist_ok=True)

    summaries = []
    for dest in destinations:
        slug = slugify(dest.get("name", ""))
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

        # Write individual file
        with open(dest_dir / f"{slug}.json", 'w') as f:
            json.dump(detail, f, indent=2, ensure_ascii=False)

        summaries.append({
            "slug": slug,
            "name": dest["name"],
            "region": dest.get("region", ""),
            "continent": dest.get("continent", ""),
            "budget": dest.get("budget", ""),
            "season": dest.get("season", ""),
            "vibes": dest.get("vibes", []),
            "photo": dest.get("photo", ""),
            "pitch": dest.get("pitch", "")
        })

    # Write summary file
    with open(OUTPUT_DIR / "destinations.json", 'w') as f:
        json.dump({
            "count": len(summaries),
            "destinations": summaries
        }, f, indent=2, ensure_ascii=False)

    return summaries, len(summaries)


# ============================================================
# POPULAR PICKS
# ============================================================

def extract_pick_places(soup, slug):
    """Extract all places from a popular-picks page."""
    places = []
    sections = soup.find_all('section', class_='restaurant-section')

    for section in sections:
        place = {}

        # Name
        h2 = section.find('h2')
        if h2:
            # Remove the number span
            num_span = h2.find('span', class_='restaurant-number')
            number = num_span.text.strip() if num_span else ""
            name_text = h2.get_text(strip=True)
            if number and name_text.startswith(number):
                name_text = name_text[len(number):].strip()
            place["name"] = name_text
            place["position"] = int(number) if number.isdigit() else None

        # Cuisine tags
        tags = section.find_all('span', class_=lambda x: x and 'cuisine-tag' in x)
        if tags:
            place["cuisineTags"] = [t.text.strip() for t in tags]

        # Google rating
        rating_span = section.find('span', class_='google-rating')
        if rating_span:
            rating_text = rating_span.get_text(strip=True)
            # Parse "★ 4.5 · 1,859 reviews"
            match = re.search(r'([\d.]+)\s*[·•]\s*([\d,]+)', rating_text)
            if match:
                place["googleRating"] = float(match.group(1))
                place["reviewCount"] = int(match.group(2).replace(',', ''))

        # Restaurant details (price, location, maps)
        details = section.find('div', class_='restaurant-details')
        if details:
            spans = details.find_all('span')
            for span in spans:
                text = span.get_text(strip=True)
                if '💰' in text or '¥' in text or '€' in text or '$' in text or '£' in text:
                    place["priceRange"] = text.replace('💰', '').strip()
                elif '📍' in text:
                    place["address"] = text.replace('📍', '').strip()

            maps_link = details.find('a', href=re.compile(r'maps\.google|google.*maps|goo\.gl/maps'))
            if maps_link:
                place["googleMapsUrl"] = maps_link.get('href', '')

        # Opening hours
        hours_div = section.find('div', class_='shop-hours')
        if hours_div:
            hours_grid = hours_div.find('div', class_='hours-grid')
            if hours_grid:
                spans = hours_grid.find_all('span')
                hours = {}
                for i in range(0, len(spans) - 1, 2):
                    day = spans[i].text.strip()
                    time = spans[i + 1].text.strip()
                    hours[day] = time
                if hours:
                    place["openingHours"] = hours

            # Open/closed status
            summary = hours_div.find('summary')
            if summary:
                status_text = summary.get_text(strip=True)
                if 'Open' in status_text:
                    place["openNow"] = True
                elif 'Closed' in status_text:
                    place["openNow"] = False

        # Contact (phone, website)
        contact = section.find('div', class_='shop-contact')
        if contact:
            phone_link = contact.find('a', href=re.compile(r'tel:'))
            if phone_link:
                place["phone"] = phone_link.get('href', '').replace('tel:', '')

            website_link = contact.find('a', href=re.compile(r'^https?://'))
            if website_link and 'maps.google' not in website_link.get('href', ''):
                place["website"] = website_link.get('href', '')

        # Photo
        img = section.find('img')
        if img and img.get('src', '').startswith('https://img.tabiji.ai'):
            place["photo"] = img.get('src', '')
        elif img and img.get('src'):
            place["photo"] = img.get('src', '')

        # What to order
        order_div = section.find('div', class_='what-to-order')
        if order_div:
            order_text = order_div.get_text(strip=True)
            order_text = re.sub(r'^What to order:\s*', '', order_text)
            place["whatToOrder"] = order_text

        # Reddit quotes
        quotes = section.find_all('div', class_='reddit-quote')
        if quotes:
            place["redditQuotes"] = []
            for q in quotes:
                quote_text = q.get_text(strip=True)
                source_span = q.find('span', class_='source')
                source = source_span.get_text(strip=True) if source_span else ""
                # Clean up the quote text — remove source from end
                if source and quote_text.endswith(source):
                    quote_text = quote_text[:-len(source)].strip()
                # Remove leading/trailing quotes
                quote_text = quote_text.strip('""\u201c\u201d')
                place["redditQuotes"].append({
                    "text": quote_text,
                    "source": source
                })

        # Tabiji verdict / insider tip
        verdict_div = section.find('div', class_='tabiji-verdict')
        if verdict_div:
            verdict_text = verdict_div.get_text(strip=True)
            verdict_text = re.sub(r'^tabiji verdict:\s*', '', verdict_text)
            place["insiderTip"] = verdict_text

        if place.get("name"):
            places.append(place)

    return places


def extract_pick_places_generic(soup, slug):
    """Extract places from pages with non-standard section classes (bath-section, pick-item, etc.)."""
    places = []

    # Try various section/item patterns
    items = (
        soup.find_all('section', class_=re.compile(r'bath-section|lodge-section|hammam-section|club-section|bar-section|view-section|stay-section|spot-section')) or
        soup.find_all('div', class_=re.compile(r'pick-item'))
    )

    if not items:
        return places

    for i, item in enumerate(items):
        place = {}
        place["position"] = i + 1

        # Name from h2 or h3
        heading = item.find(['h2', 'h3'])
        if heading:
            # Remove number spans
            num_span = heading.find('span', class_=re.compile(r'number|pick-number|bath-number'))
            name_text = heading.get_text(strip=True)
            if num_span:
                num_text = num_span.text.strip()
                if name_text.startswith(num_text):
                    name_text = name_text[len(num_text):].strip()
            # Remove leading "01. " patterns
            name_text = re.sub(r'^\d+\.\s*', '', name_text)
            place["name"] = name_text

        # Tags
        tags = item.find_all('span', class_=re.compile(r'tag(?!-)|bath-tag|cuisine-tag'))
        if tags:
            tag_texts = [t.text.strip() for t in tags if not any(skip in t.text for skip in ['📍', '💰', '🪙', '🕐'])]
            if tag_texts:
                place["cuisineTags"] = tag_texts

        # Details / meta
        details = item.find(class_=re.compile(r'details|meta|bath-details|pick-details|spot-details'))
        if details:
            spans = details.find_all('span')
            for span in spans:
                text = span.get_text(strip=True)
                if any(c in text for c in ['💰', '💶', '¥', '€', '$', '£', '🪙']):
                    place["priceRange"] = re.sub(r'^[💰💶🪙]\s*', '', text).strip()
                elif '📍' in text:
                    place["address"] = text.replace('📍', '').strip()

            maps_link = details.find('a', href=re.compile(r'maps\.google|google.*maps'))
            if maps_link:
                place["googleMapsUrl"] = maps_link.get('href', '')

        # Subtitle (for pick-item template)
        subtitle = item.find(class_='subtitle')
        if subtitle and not place.get("address"):
            parts = subtitle.get_text(strip=True).split('•')
            if len(parts) >= 1:
                place["address"] = parts[0].strip()
            if len(parts) >= 3:
                place["priceRange"] = parts[-1].strip()

        # Google rating
        rating_el = item.find(class_='google-rating')
        if rating_el:
            match = re.search(r'([\d.]+)\s*[·•]\s*([\d,]+)', rating_el.text)
            if match:
                place["googleRating"] = float(match.group(1))
                place["reviewCount"] = int(match.group(2).replace(',', ''))

        # Photo
        img = item.find('img')
        if img and img.get('src'):
            place["photo"] = img.get('src', '')

        # What to order / what to know
        order = item.find(class_=re.compile(r'what-to-order|what-to-know'))
        if order:
            text = order.get_text(strip=True)
            text = re.sub(r'^(What to order|What to know):\s*', '', text)
            place["whatToOrder"] = text

        # Description
        desc_p = item.find('p', class_='description')
        if desc_p:
            place["whatToOrder"] = desc_p.get_text(strip=True)

        # Reddit quotes
        quotes = item.find_all('div', class_='reddit-quote')
        if quotes:
            place["redditQuotes"] = []
            for q in quotes:
                qt = q.get_text(strip=True)
                src = q.find('span', class_='source')
                source = src.get_text(strip=True) if src else ""
                if source and qt.endswith(source):
                    qt = qt[:-len(source)].strip()
                qt = qt.strip('""\u201c\u201d')
                place["redditQuotes"].append({"text": qt, "source": source})

        # Verdict / tabiji verdict
        verdict = item.find(class_=re.compile(r'verdict|tabiji-verdict'))
        if verdict:
            text = verdict.get_text(strip=True)
            text = re.sub(r'^tabiji verdict:\s*', '', text)
            place["insiderTip"] = text

        # Hours
        hours_div = item.find(class_=re.compile(r'hours'))
        if hours_div:
            grid = hours_div.find(class_='hours-grid')
            if grid:
                spans = grid.find_all('span')
                hours = {}
                for j in range(0, len(spans) - 1, 2):
                    hours[spans[j].text.strip()] = spans[j + 1].text.strip()
                if hours:
                    place["openingHours"] = hours

        if place.get("name"):
            places.append(place)

    return places


def extract_pick_places_alt(soup, slug):
    """Extract places from older-template popular-picks pages using entry-body structure."""
    places = []
    entries = soup.find_all('div', class_='entry-body')

    for i, entry in enumerate(entries):
        place = {}
        place["position"] = i + 1

        # Name
        name_el = entry.find(class_='entry-name')
        if name_el:
            place["name"] = name_el.get_text(strip=True)

        # Local name
        local_name = entry.find(class_='entry-local-name')
        if local_name:
            place["localName"] = local_name.get_text(strip=True)

        # Tags
        tags = entry.find_all('span', class_=lambda x: x and 'tag' in x and x != 'entry-tags')
        if tags:
            place["cuisineTags"] = [t.text.strip() for t in tags]

        # Meta (price, address, hours)
        meta = entry.find(class_='entry-meta')
        if meta:
            spans = meta.find_all('span')
            for span in spans:
                text = span.get_text(strip=True)
                if '💶' in text or '💰' in text or '¥' in text or '€' in text or '$' in text or '£' in text:
                    place["priceRange"] = re.sub(r'^[💶💰]\s*', '', text).strip()
                elif '📍' in text:
                    place["address"] = text.replace('📍', '').strip()
                    maps_link = span.find('a', href=re.compile(r'maps\.google|google.*maps'))
                    if maps_link:
                        place["googleMapsUrl"] = maps_link.get('href', '')
                        place["address"] = maps_link.get_text(strip=True)
                elif '🕐' in text or '🕑' in text:
                    place["hoursText"] = re.sub(r'^[🕐🕑]\s*', '', text).strip()

        # Google rating (some alt templates have it)
        rating_el = entry.find(class_='google-rating')
        if rating_el:
            rating_text = rating_el.get_text(strip=True)
            match = re.search(r'([\d.]+)\s*[·•]\s*([\d,]+)', rating_text)
            if match:
                place["googleRating"] = float(match.group(1))
                place["reviewCount"] = int(match.group(2).replace(',', ''))

        # Photo
        img = entry.find('img')
        if img and img.get('src'):
            place["photo"] = img.get('src', '')

        # What to order
        order_div = entry.find(class_='what-to-order')
        if order_div:
            p = order_div.find('p')
            if p:
                place["whatToOrder"] = p.get_text(strip=True)

        # Reddit quotes (quote-block)
        quotes_div = entry.find(class_='quotes')
        if quotes_div:
            quote_blocks = quotes_div.find_all(class_='quote-block')
            if quote_blocks:
                place["redditQuotes"] = []
                for qb in quote_blocks:
                    text = qb.get_text(strip=True)
                    cite = qb.find('cite')
                    source = cite.get_text(strip=True) if cite else ""
                    if source and text.endswith(source):
                        text = text[:-len(source)].strip()
                    text = text.strip('""\u201c\u201d')
                    place["redditQuotes"].append({"text": text, "source": source})

        # Verdict
        verdict = entry.find(class_='verdict-box')
        if verdict:
            p = verdict.find('p')
            if p:
                place["insiderTip"] = p.get_text(strip=True)

        # Contact section
        contact = entry.find(class_='entry-contact') or entry.find(class_='shop-contact')
        if contact:
            phone_link = contact.find('a', href=re.compile(r'tel:'))
            if phone_link:
                place["phone"] = phone_link.get('href', '').replace('tel:', '')
            website_link = contact.find('a', href=re.compile(r'^https?://'))
            if website_link and 'maps.google' not in website_link.get('href', ''):
                place["website"] = website_link.get('href', '')

        # Hours grid (some alt pages have it)
        hours_div = entry.find(class_='shop-hours') or entry.find(class_='hours-section')
        if hours_div:
            hours_grid = hours_div.find(class_='hours-grid')
            if hours_grid:
                spans = hours_grid.find_all('span')
                hours = {}
                for j in range(0, len(spans) - 1, 2):
                    day = spans[j].text.strip()
                    time = spans[j + 1].text.strip()
                    hours[day] = time
                if hours:
                    place["openingHours"] = hours

        if place.get("name"):
            places.append(place)

    return places


def extract_meta_content(soup, attr_name, attr_value):
    """Extract a meta tag content value by name/property."""
    tag = soup.find('meta', attrs={attr_name: attr_value})
    return tag.get('content', '').strip() if tag and tag.get('content') else ''


def extract_pick_hub_cards(soup):
    """Extract linked cards from a hub-style popular-picks page."""
    cards = []
    for link in soup.find_all('a', class_='pick-card'):
        href = link.get('href', '').strip()
        if not href:
            continue

        title_el = link.find(['h2', 'h3'])
        desc_el = link.find('p')
        badge_el = link.find(class_='card-badge')
        img_el = link.find('img')
        meta_els = link.find_all('span')
        meta = []
        for span in meta_els:
            classes = span.get('class', [])
            if 'card-badge' in classes:
                continue
            text = span.get_text(' ', strip=True)
            if text:
                meta.append(text)

        slug = href.strip('/').split('/')[-1] if href else ''
        cards.append({
            "name": title_el.get_text(' ', strip=True) if title_el else slug,
            "slug": slug,
            "url": f"{SITE_URL}{href}" if href.startswith('/') else href,
            "description": desc_el.get_text(' ', strip=True) if desc_el else '',
            "badge": badge_el.get_text(' ', strip=True) if badge_el else '',
            "photo": img_el.get('src', '').strip() if img_el else '',
            "meta": meta,
        })

    return cards


def build_picks():
    """Build popular picks JSON from popular-picks/*/index.html."""
    picks_dir = BASE_DIR / "popular-picks"
    if not picks_dir.exists():
        print("  ⚠️  popular-picks/ not found")
        return [], 0

    output_picks_dir = OUTPUT_DIR / "picks"
    output_picks_dir.mkdir(parents=True, exist_ok=True)

    summaries = []
    total_places = 0

    # Get all pick page directories (skip country pages without index.html containing restaurant-section)
    slugs = sorted([d for d in os.listdir(picks_dir)
                     if (picks_dir / d / "index.html").exists()])

    for slug in slugs:
        html_path = picks_dir / slug / "index.html"
        try:
            html = html_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"  ⚠️  Error reading {slug}: {e}")
            continue

        soup = BeautifulSoup(html, 'html.parser')
        json_ld = extract_json_ld(soup)

        # Get metadata from Article JSON-LD
        article = find_json_ld_by_type(json_ld, 'Article')
        item_list = find_json_ld_by_type(json_ld, 'ItemList')

        title = ""
        if article:
            title = article.get('headline', '')
        if not title:
            title_tag = soup.find('title')
            title = title_tag.text.strip().split('|')[0].strip() if title_tag else slug

        # Extract city from breadcrumb or title
        city = ""
        desc = ""
        if article:
            desc = article.get('description', '')

        # Try to extract city from the slug or title
        # Common pattern: "12 Best Brunch Spots in Amsterdam 2026"
        city_match = re.search(r'(?:in|of)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', title)
        if city_match:
            city = city_match.group(1)

        # Extract category from title
        category = ""
        cat_match = re.search(r'Best\s+(.+?)\s+(?:in|of|for)', title, re.IGNORECASE)
        if cat_match:
            category = cat_match.group(1).strip()

        # Extract places — try main template, then alt, then generic, then hub cards
        places = extract_pick_places(soup, slug)
        if not places:
            places = extract_pick_places_alt(soup, slug)
        if not places:
            places = extract_pick_places_generic(soup, slug)
        is_hub_page = False
        if not places:
            places = extract_pick_hub_cards(soup)
            is_hub_page = len(places) > 0
        total_places += len(places)

        # Get hero image
        hero_img = ""
        if article and article.get('image'):
            hero_img = article['image']
        if isinstance(hero_img, list):
            hero_img = hero_img[0] if hero_img else ""
        if not hero_img:
            hero_img = extract_meta_content(soup, 'property', 'og:image') or extract_meta_content(soup, 'name', 'twitter:image')

        if not desc:
            desc = extract_meta_content(soup, 'name', 'description')

        if not city and is_hub_page:
            h1 = soup.find('h1')
            if h1:
                city = h1.get_text(' ', strip=True)

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

        # Write individual file
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

    # Write summary file
    with open(OUTPUT_DIR / "picks.json", 'w') as f:
        json.dump({
            "count": len(summaries),
            "totalPlaces": total_places,
            "picks": summaries
        }, f, indent=2, ensure_ascii=False)

    return summaries, total_places


# ============================================================
# ITINERARIES
# ============================================================

def extract_itinerary_days(soup):
    """Extract day-by-day itinerary from HTML."""
    days = []
    day_divs = soup.find_all('div', class_='day')

    for day_div in day_divs:
        day = {}

        # Day header
        day_header = day_div.find('div', class_='day-header')
        if day_header:
            day_num = day_header.find('span', class_='day-num')
            day_neighborhoods = day_header.find('span', class_='day-neighborhoods')
            if day_num:
                day["dayLabel"] = day_num.text.strip()
            if day_neighborhoods:
                day["neighborhoods"] = day_neighborhoods.text.strip()

        # Day title
        h2 = day_div.find('h2')
        if h2:
            day["title"] = h2.get_text(strip=True)
            # Skip overview/glance sections
            title_lower = day["title"].lower()
            if any(skip in title_lower for skip in ['at a glance', 'overview', 'essentials', 'before you go', 'packing']):
                continue

        # Day description
        first_p = day_div.find('p')
        if first_p and not first_p.find_parent('div', class_='time-block'):
            day["description"] = first_p.get_text(strip=True)

        # Time blocks (activities)
        time_blocks = day_div.find_all('div', class_='time-block')
        activities = []
        for tb in time_blocks:
            activity = {}
            time_label = tb.find('div', class_='time-label')
            if time_label:
                activity["time"] = time_label.get_text(strip=True)
            h3 = tb.find('h3')
            if h3:
                activity["name"] = h3.get_text(strip=True)
            # Get description paragraphs
            paras = tb.find_all('p')
            if paras:
                activity["description"] = ' '.join(p.get_text(strip=True) for p in paras[:2])

            # Spot details
            spot_details = tb.find_all('div', class_='spot-detail')
            if spot_details:
                activity["details"] = [sd.get_text(strip=True) for sd in spot_details]

            # Tips
            tips = tb.find_all('div', class_='tip')
            if tips:
                activity["tips"] = [t.get_text(strip=True) for t in tips]

            if activity.get("name"):
                activities.append(activity)

        if activities:
            day["activities"] = activities

        if day.get("title") or day.get("activities"):
            days.append(day)

    return days


def parse_itinerary_page(html_path, slug, source_dir):
    """Parse a single itinerary page and return structured data."""
    try:
        html = html_path.read_text(encoding='utf-8')
    except Exception:
        return None

    soup = BeautifulSoup(html, 'html.parser')
    json_ld = extract_json_ld(soup)

    article = find_json_ld_by_type(json_ld, 'Article')
    tourist_trip = find_json_ld_by_type(json_ld, 'TouristTrip')

    title = ""
    desc = ""
    destination = ""
    duration = ""
    trip_type = []
    hero_image = ""

    if article:
        title = article.get('headline', '')
        desc = article.get('description', '')
        hero_image = article.get('image', '')

    if tourist_trip:
        if not title:
            title = tourist_trip.get('name', '')
        if not desc:
            desc = tourist_trip.get('description', '')
        trip_type = tourist_trip.get('touristType', [])

    if not title:
        title_tag = soup.find('title')
        title = title_tag.text.strip().split('|')[0].strip() if title_tag else slug

    # Extract destination from title
    # Patterns: "5 Day Tokyo Food Guide", "9 Nights in Nosara"
    dest_match = re.search(r'(?:Day[s]?\s+(?:in\s+)?|Night[s]?\s+(?:in\s+)?)([A-Z][a-z]+(?:[\s-][A-Z][a-z]+)*)', title)
    if dest_match:
        destination = dest_match.group(1)
    else:
        # Try "in <City>"
        dest_match2 = re.search(r'in\s+([A-Z][a-z]+(?:[\s-][A-Z][a-z]+)*)', title)
        if dest_match2:
            destination = dest_match2.group(1)

    # Extract duration
    dur_match = re.search(r'(\d+)\s*(?:Day|Night)', title, re.IGNORECASE)
    if dur_match:
        duration = f"{dur_match.group(1)} days"

    # If no duration from title, count day divs
    if not duration:
        day_divs = soup.find_all('div', class_='day')
        if day_divs:
            # Filter out overview days
            actual_days = [d for d in day_divs
                          if d.find('h2') and not any(
                              skip in d.find('h2').get_text(strip=True).lower()
                              for skip in ['glance', 'overview', 'essentials']
                          )]
            if actual_days:
                duration = f"{len(actual_days)} days"

    # Extract day-by-day
    days = extract_itinerary_days(soup)

    # Determine URL based on source
    if source_dir == "i":
        url = f"{SITE_URL}/i/{slug}/"
    else:
        url = f"{SITE_URL}/itineraries/{slug}/"

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
    """Build itineraries JSON from i/*/index.html and itineraries/*/index.html."""
    output_itin_dir = OUTPUT_DIR / "itineraries"
    output_itin_dir.mkdir(parents=True, exist_ok=True)

    summaries = []
    all_itineraries = []

    # Process both /i/ and /itineraries/
    for source_dir in ["i", "itineraries"]:
        src_path = BASE_DIR / source_dir
        if not src_path.exists():
            continue

        slugs = sorted([d for d in os.listdir(src_path)
                         if (src_path / d / "index.html").exists()])

        for slug in slugs:
            html_path = src_path / slug / "index.html"
            result = parse_itinerary_page(html_path, slug, source_dir)
            if result:
                all_itineraries.append(result)

    # Write individual files — use source-slug for uniqueness
    for itin in all_itineraries:
        slug = itin["slug"]
        source = itin["source"]
        filename = f"{source}-{slug}" if source == "itineraries" else slug

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

    # Write summary file
    with open(OUTPUT_DIR / "itineraries.json", 'w') as f:
        json.dump({
            "count": len(summaries),
            "itineraries": summaries
        }, f, indent=2, ensure_ascii=False)

    return summaries, len(summaries)


# ============================================================
# COMPARE
# ============================================================

def build_compare():
    """Build compare JSON from compare/*/index.html."""
    compare_dir = BASE_DIR / "compare"
    if not compare_dir.exists():
        print("  ⚠️  compare/ not found")
        return [], 0

    output_compare_dir = OUTPUT_DIR / "compare"
    output_compare_dir.mkdir(parents=True, exist_ok=True)

    summaries = []

    slugs = sorted([d for d in os.listdir(compare_dir)
                     if (compare_dir / d / "index.html").exists()])

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

        title = ""
        desc = ""
        hero_image = ""

        if article:
            title = article.get('headline', '')
            desc = article.get('description', '')
            hero_image = article.get('image', '')

        if not title:
            title_tag = soup.find('title')
            title = title_tag.text.strip().split('|')[0].strip() if title_tag else slug

        # Parse destinations from slug (format: "dest1-vs-dest2")
        parts = slug.split('-vs-')
        destination1 = parts[0].replace('-', ' ').title() if len(parts) >= 2 else ""
        destination2 = parts[1].replace('-', ' ').title() if len(parts) >= 2 else ""

        # Extract comparison categories from deep-dive sections
        categories = []
        deep_dives = soup.find_all('section', class_='deep-dive')
        for dd in deep_dives:
            h2 = dd.find('h2')
            if h2:
                cat_title = h2.get_text(strip=True)
                # Get key points
                paragraphs = dd.find_all('p')
                summary_text = ""
                if paragraphs:
                    summary_text = paragraphs[0].get_text(strip=True)[:300]

                # Reddit quotes
                quotes = dd.find_all('div', class_='reddit-quote')
                quote_texts = []
                for q in quotes:
                    qt = q.get_text(strip=True).strip('""\u201c\u201d')[:200]
                    quote_texts.append(qt)

                categories.append({
                    "title": cat_title,
                    "summary": summary_text,
                    "redditQuotes": quote_texts[:2]
                })

        # Verdict
        verdict_box = soup.find('div', class_='verdict-box')
        verdict = ""
        if verdict_box:
            verdict = verdict_box.get_text(strip=True)[:500]

        # FAQs
        faqs = []
        if faq and faq.get('mainEntity'):
            for q in faq['mainEntity']:
                faqs.append({
                    "question": q.get('name', ''),
                    "answer": q.get('acceptedAnswer', {}).get('text', '')[:300]
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

    # Write summary file
    with open(OUTPUT_DIR / "compare.json", 'w') as f:
        json.dump({
            "count": len(summaries),
            "comparisons": summaries
        }, f, indent=2, ensure_ascii=False)

    return summaries, len(summaries)


# ============================================================
# INDEX
# ============================================================

def build_index(dest_count, picks_count, places_count, itin_count, compare_count):
    """Build the API index/metadata file."""
    index = {
        "name": "tabiji.ai API",
        "version": "1.0.0",
        "description": "Free REST API for AI-curated travel data — destinations, restaurant picks, itineraries, and more. No API key required.",
        "baseUrl": API_BASE_URL,
        "documentation": f"{SITE_URL}/api/",
        "openapi": f"{SITE_URL}/api/openapi.json",
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stats": {
            "destinations": dest_count,
            "picksGuides": picks_count,
            "totalPlaces": places_count,
            "itineraries": itin_count,
            "comparisons": compare_count
        },
        "endpoints": [
            {
                "path": "/destinations.json",
                "description": f"All {dest_count} destinations with budget, season, vibes, and travel styles",
                "method": "GET"
            },
            {
                "path": "/destinations/{slug}.json",
                "description": "Single destination detail",
                "method": "GET"
            },
            {
                "path": "/picks.json",
                "description": f"All {picks_count} curated 'best of' guides",
                "method": "GET"
            },
            {
                "path": "/picks/{slug}.json",
                "description": "Full picks guide with all places, ratings, hours, and quotes",
                "method": "GET"
            },
            {
                "path": "/itineraries.json",
                "description": f"All {itin_count} day-by-day travel itineraries",
                "method": "GET"
            },
            {
                "path": "/itineraries/{slug}.json",
                "description": "Full itinerary with day-by-day activities",
                "method": "GET"
            },
            {
                "path": "/compare.json",
                "description": f"All {compare_count} head-to-head destination comparisons",
                "method": "GET"
            },
            {
                "path": "/compare/{slug}.json",
                "description": "Full comparison with categories, verdicts, and FAQs",
                "method": "GET"
            }
        ],
        "dataSource": "Curated from Reddit discussions, enriched with Google Places data (ratings, hours, maps links). Every pick includes 'what to order' recommendations and real traveler quotes.",
        "license": "Free for non-commercial use. Attribution appreciated: tabiji.ai",
        "contact": "hello@tabiji.ai"
    }

    with open(OUTPUT_DIR / "index.json", 'w') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


# ============================================================
# MAIN
# ============================================================

def main():
    print("🦉 Building Tabiji API v1...")
    print(f"   Source: {BASE_DIR}")
    print(f"   Output: {OUTPUT_DIR}")
    print()

    # Clean output dir
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Build each section
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

    print("📋 Building index...")
    build_index(dest_count, picks_count, places_count, itin_count, compare_count)
    print("   ✅ index.json")

    # Count total files
    total_files = 0
    total_size = 0
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for f in files:
            if f.endswith('.json'):
                total_files += 1
                total_size += os.path.getsize(os.path.join(root, f))

    print()
    print("=" * 50)
    print(f"🦉 Tabiji API v1 Build Complete!")
    print(f"   Destinations:  {dest_count}")
    print(f"   Picks guides:  {picks_count} ({places_count} places)")
    print(f"   Itineraries:   {itin_count}")
    print(f"   Comparisons:   {compare_count}")
    print(f"   Total files:   {total_files}")
    print(f"   Total size:    {total_size / 1024 / 1024:.1f} MB")
    print("=" * 50)


if __name__ == "__main__":
    main()