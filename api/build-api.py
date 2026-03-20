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


def isoformat_mtime(path):
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def normalize_record_type(record_type):
    return "compare" if record_type == "comparison" else record_type


def make_id(record_type, slug):
    return f"{normalize_record_type(record_type)}:{slug}"


def unique_list(values):
    seen = set()
    result = []
    for value in values:
        if not value:
            continue
        value = clean_text(str(value))
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def attach_record_meta(payload, *, record_type, slug, source_path, source_url, tags=None):
    payload["id"] = make_id(record_type, slug)
    payload["type"] = normalize_record_type(record_type)
    payload["updatedAt"] = isoformat_mtime(source_path)
    payload["sourceUrl"] = source_url
    payload["tags"] = unique_list(tags or [])
    return payload


def build_search_item(*, item_type, slug, title, subtitle, url, site_url, tags=None, extra=None):
    record = {
        "id": make_id(item_type, slug),
        "type": normalize_record_type(item_type),
        "slug": slug,
        "title": title,
        "subtitle": subtitle,
        "url": url,
        "siteUrl": site_url,
        "tags": unique_list(tags or []),
    }
    if extra:
        record.update({k: v for k, v in extra.items() if v not in (None, "", [])})
    record["tokens"] = unique_list([title, subtitle, *(record.get("tags", []))] + [str(v) for v in (extra or {}).values() if isinstance(v, str)])
    return record


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

        detail = attach_record_meta({
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
        }, record_type="destination", slug=slug, source_path=src, source_url=f"{SITE_URL}/find/?q={slug}", tags=[dest.get("region", ""), dest.get("continent", ""), *(dest.get("vibes", []) or []), *(dest.get("travel", []) or [])])

        with open(dest_dir / f"{slug}.json", 'w') as f:
            json.dump(detail, f, indent=2, ensure_ascii=False)

        summaries.append({
            "id": make_id("destination", slug),
            "type": "destination",
            "slug": slug,
            "name": dest.get("name", ""),
            "region": dest.get("region", ""),
            "continent": dest.get("continent", ""),
            "budget": dest.get("budget", ""),
            "season": dest.get("season", ""),
            "vibes": dest.get("vibes", []),
            "photo": dest.get("photo", ""),
            "pitch": dest.get("pitch", ""),
            "updatedAt": isoformat_mtime(src),
            "sourceUrl": f"{SITE_URL}/find/?q={slug}",
            "tags": unique_list([dest.get("region", ""), dest.get("continent", ""), *(dest.get("vibes", []) or []), *(dest.get("travel", []) or [])])
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

        order_div = section.find('div', class_='what-to-order')
        if order_div:
            order_text = clean_text(order_div.get_text())
            order_text = re.sub(r'^What to order:\s*', '', order_text, flags=re.IGNORECASE)
            place["whatToOrder"] = order_text

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
    """Extract places from pages with non-standard section classes (bath-section, lodge-section, pick-item, etc.)."""
    places = []
    items = (
        soup.find_all('section', class_=re.compile(r'bath-section|lodge-section|hammam-section|club-section|bar-section|view-section|stay-section|spot-section'))
        or soup.find_all('div', class_=re.compile(r'pick-item'))
    )

    if not items:
        return places

    for i, item in enumerate(items):
        place = {"position": i + 1}

        heading = item.find(['h2', 'h3'])
        if heading:
            num_span = heading.find('span', class_=re.compile(r'number|pick-number|bath-number'))
            name_text = clean_text(heading.get_text())
            if num_span:
                num_text = clean_text(num_span.get_text())
                if name_text.startswith(num_text):
                    name_text = name_text[len(num_text):].strip()
            name_text = re.sub(r'^\d+\.\s*', '', name_text)
            place["name"] = name_text

        tags = item.find_all('span', class_=re.compile(r'tag(?!-)|bath-tag|cuisine-tag'))
        if tags:
            tag_texts = [clean_text(t.get_text()) for t in tags if not any(skip in clean_text(t.get_text()) for skip in ['📍', '💰', '🪙', '🕐'])]
            if tag_texts:
                place["cuisineTags"] = tag_texts

        details = item.find(class_=re.compile(r'details|meta|bath-details|pick-details|spot-details'))
        if details:
            spans = details.find_all('span')
            for span in spans:
                text = clean_text(span.get_text())
                if any(c in text for c in ['💰', '💶', '💴', '¥', '€', '$', '£', '🪙']):
                    place["priceRange"] = normalize_price_range(text)
                elif '📍' in text:
                    place["address"] = text.replace('📍', '').strip()
            maps_link = details.find('a', href=re.compile(r'maps\.google|google.*maps'))
            if maps_link:
                place["googleMapsUrl"] = maps_link.get('href', '')

        subtitle = item.find(class_='subtitle')
        if subtitle and not place.get("address"):
            parts = [clean_text(p) for p in subtitle.get_text(strip=True).split('•')]
            if len(parts) >= 1:
                place["address"] = parts[0].strip()
            if len(parts) >= 3:
                place["priceRange"] = normalize_price_range(parts[-1])

        rating_el = item.find(class_='google-rating')
        if rating_el:
            match = re.search(r'([\d.]+)\s*[·•]\s*([\d,]+)', rating_el.get_text())
            if match:
                place["googleRating"] = float(match.group(1))
                place["reviewCount"] = int(match.group(2).replace(',', ''))

        img = item.find('img')
        if img and img.get('src'):
            place["photo"] = img.get('src', '')

        order = item.find(class_=re.compile(r'what-to-order|what-to-know'))
        if order:
            text = clean_text(order.get_text())
            text = re.sub(r'^(What to order|What to know):\s*', '', text, flags=re.IGNORECASE)
            place["whatToOrder"] = text

        desc_p = item.find('p', class_='description')
        if desc_p and not place.get("whatToOrder"):
            place["whatToOrder"] = clean_text(desc_p.get_text())

        quotes = item.find_all('div', class_='reddit-quote')
        if quotes:
            place["redditQuotes"] = [split_quote_and_source(q) for q in quotes]

        verdict = item.find(class_=re.compile(r'verdict|tabiji-verdict'))
        if verdict:
            text = clean_text(verdict.get_text())
            text = re.sub(r'^tabiji verdict:\s*', '', text, flags=re.IGNORECASE)
            place["insiderTip"] = text

        hours_div = item.find(class_=re.compile(r'hours'))
        if hours_div:
            grid = hours_div.find(class_='hours-grid')
            if grid:
                spans = grid.find_all('span')
                hours = {}
                for j in range(0, len(spans) - 1, 2):
                    hours[clean_text(spans[j].get_text())] = clean_text(spans[j + 1].get_text())
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
        place = {"position": i + 1}

        name_el = entry.find(class_='entry-name')
        if name_el:
            place["name"] = clean_text(name_el.get_text())

        local_name = entry.find(class_='entry-local-name')
        if local_name:
            place["localName"] = clean_text(local_name.get_text())

        tags = entry.find_all('span', class_=lambda x: x and 'tag' in x and x != 'entry-tags')
        if tags:
            place["cuisineTags"] = [clean_text(t.get_text()) for t in tags]

        meta = entry.find(class_='entry-meta')
        if meta:
            spans = meta.find_all('span')
            for span in spans:
                text = clean_text(span.get_text())
                if any(c in text for c in ['💶', '💰', '💴', '¥', '€', '$', '£', '🪙']):
                    place["priceRange"] = normalize_price_range(text)
                elif '📍' in text:
                    place["address"] = text.replace('📍', '').strip()
                    maps_link = span.find('a', href=re.compile(r'maps\.google|google.*maps'))
                    if maps_link:
                        place["googleMapsUrl"] = maps_link.get('href', '')
                        place["address"] = clean_text(maps_link.get_text())
                elif '🕐' in text or '🕑' in text:
                    place["hoursText"] = re.sub(r'^[🕐🕑]\s*', '', text).strip()

        rating_el = entry.find(class_='google-rating')
        if rating_el:
            rating_text = clean_text(rating_el.get_text())
            match = re.search(r'([\d.]+)\s*[·•]\s*([\d,]+)', rating_text)
            if match:
                place["googleRating"] = float(match.group(1))
                place["reviewCount"] = int(match.group(2).replace(',', ''))

        img = entry.find('img')
        if img and img.get('src'):
            place["photo"] = img.get('src', '')

        order_div = entry.find(class_='what-to-order')
        if order_div:
            p = order_div.find('p')
            if p:
                place["whatToOrder"] = clean_text(p.get_text())
            else:
                place["whatToOrder"] = clean_text(order_div.get_text())

        quotes_div = entry.find(class_='quotes')
        if quotes_div:
            quote_blocks = quotes_div.find_all(class_='quote-block')
            if quote_blocks:
                place["redditQuotes"] = []
                for qb in quote_blocks:
                    cite = qb.find('cite')
                    source = clean_text(cite.get_text()) if cite else ""
                    quote_clone = BeautifulSoup(str(qb), 'html.parser')
                    cite_clone = quote_clone.find('cite')
                    if cite_clone:
                        cite_clone.decompose()
                    text = clean_text(quote_clone.get_text()).strip('""“”')
                    place["redditQuotes"].append({"text": text, "source": source, "sourceUrl": ""})

        verdict = entry.find(class_='verdict-box')
        if verdict:
            p = verdict.find('p')
            if p:
                place["insiderTip"] = clean_text(p.get_text())

        contact = entry.find(class_='entry-contact') or entry.find(class_='shop-contact')
        if contact:
            phone_link = contact.find('a', href=re.compile(r'tel:'))
            if phone_link:
                place["phone"] = phone_link.get('href', '').replace('tel:', '')
            website_link = contact.find('a', href=re.compile(r'^https?://'))
            if website_link and 'maps.google' not in website_link.get('href', ''):
                place["website"] = website_link.get('href', '')

        hours_div = entry.find(class_='shop-hours') or entry.find(class_='hours-section')
        if hours_div:
            hours_grid = hours_div.find(class_='hours-grid')
            if hours_grid:
                spans = hours_grid.find_all('span')
                hours = {}
                for j in range(0, len(spans) - 1, 2):
                    hours[clean_text(spans[j].get_text())] = clean_text(spans[j + 1].get_text())
                if hours:
                    place["openingHours"] = hours

        if place.get("name"):
            places.append(place)

    return places


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
        if not places:
            places = extract_pick_places_alt(soup, slug)
        if not places:
            places = extract_pick_places_generic(soup, slug)
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

        detail = attach_record_meta({
            "slug": slug,
            "title": title,
            "description": desc,
            "city": city,
            "category": category,
            "heroImage": hero_img,
            "placeCount": len(places),
            "url": f"{SITE_URL}/popular-picks/{slug}/",
            "places": places
        }, record_type="pick", slug=slug, source_path=html_path, source_url=f"{SITE_URL}/popular-picks/{slug}/", tags=[city, category])

        with open(output_picks_dir / f"{slug}.json", 'w') as f:
            json.dump(detail, f, indent=2, ensure_ascii=False)

        summaries.append({
            "id": make_id("pick", slug),
            "type": "pick",
            "slug": slug,
            "title": title,
            "city": city,
            "category": category,
            "placeCount": len(places),
            "url": f"{SITE_URL}/popular-picks/{slug}/",
            "updatedAt": isoformat_mtime(html_path),
            "sourceUrl": f"{SITE_URL}/popular-picks/{slug}/",
            "tags": unique_list([city, category])
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
        if day.get("dayLabel") or day.get("title") or day.get("activities"):
            days.append(day)
    return days


def derive_destination_from_itinerary_slug(slug):
    slug_match = re.match(r'^(\d+)-(?:day|days|night|nights)-([a-z0-9-]+)', slug)
    if not slug_match:
        return ""
    slug_tail = slug_match.group(2)
    slug_parts = slug_tail.split('-')
    stopwords = {'first','time','food','nightlife','romantic','relaxation','adventure','eco','culture','nature','march','april','may','june','july','august','september','october','november','december','winter','summer','spring','fall','classic','route','family','solo','budget','beach','countryside','road','trip','wellness','art','guide','itinerary','hopping'}
    dest_parts = []
    for part in slug_parts:
        if dest_parts and part in stopwords:
            break
        dest_parts.append(part)
        if len(dest_parts) >= 3:
            break
    return ' '.join(p.title() for p in dest_parts)


def clean_itinerary_destination(value):
    value = re.sub(r'\b(Itinerary|Guide|Solo Adventure|Adventure|Relaxation|Foodie|Cultural|Family Visit|Long Weekend|Escape|Getaway|Trip|Travel)\b', '', value, flags=re.IGNORECASE).strip(' :-—()')
    value = re.sub(r'\s+', ' ', value).strip()
    return value


def extract_destination_candidates(title):
    patterns = [
        r'\b(?:in|through|across|around|from|to)\s+([A-Z][A-Za-zÀ-ÿ]+(?:[\s/&·-][A-Z][A-Za-zÀ-ÿ]+){0,3})',
        r'^([A-Z][A-Za-zÀ-ÿ]+(?:[\s/&·-][A-Z][A-Za-zÀ-ÿ]+){0,3})(?::|\s+in\s+\d+|\s+—)',
    ]
    candidates = []
    for pattern in patterns:
        for match in re.finditer(pattern, title):
            candidate = clean_itinerary_destination(match.group(1))
            if candidate:
                candidates.append(candidate)
    return unique_list(candidates)


def choose_itinerary_destination(title, slug):
    bad_tokens = {'solo', 'adventure', 'relaxation', 'trip', 'days', 'nights', 'foodie', 'cultural', 'budget', 'family', 'guide', 'itinerary', 'full', 'bloom', 'through', 'under', 'big'}
    for candidate in extract_destination_candidates(title):
        words = [w.lower() for w in re.split(r'\s+', candidate) if w]
        if not words or all(word in bad_tokens for word in words):
            continue
        if len(words) == 1 and words[0] in bad_tokens:
            continue
        return candidate
    return clean_itinerary_destination(derive_destination_from_itinerary_slug(slug))


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

    destination = choose_itinerary_destination(title, slug)

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

    return attach_record_meta({
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
    }, record_type="itinerary", slug=slug, source_path=html_path, source_url=url, tags=[destination, *(trip_type if isinstance(trip_type, list) else [trip_type] if trip_type else [])])


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
        filename = itin["slug"]
        api_itin = dict(itin)
        api_itin["slug"] = filename
        api_itin["id"] = make_id("itinerary", filename)
        with open(output_itin_dir / f"{filename}.json", 'w') as f:
            json.dump(api_itin, f, indent=2, ensure_ascii=False)
        summaries.append({
            "id": make_id("itinerary", filename),
            "type": "itinerary",
            "slug": filename,
            "title": itin["title"],
            "destination": itin["destination"],
            "duration": itin["duration"],
            "tripType": itin["tripType"],
            "url": itin["url"],
            "dayCount": itin["dayCount"],
            "updatedAt": itin["updatedAt"],
            "sourceUrl": itin["sourceUrl"],
            "tags": unique_list([itin["destination"], *(itin["tripType"] or [])])
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
            if category.get("summary") or category.get("highlights") or category.get("redditQuotes") or category.get("winnerSummary"):
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

        detail = attach_record_meta({
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
        }, record_type="comparison", slug=slug, source_path=html_path, source_url=f"{SITE_URL}/compare/{slug}/", tags=[destination1, destination2])

        with open(output_compare_dir / f"{slug}.json", 'w') as f:
            json.dump(detail, f, indent=2, ensure_ascii=False)

        summaries.append({
            "id": make_id("comparison", slug),
            "type": normalize_record_type("comparison"),
            "slug": slug,
            "title": title,
            "destination1": destination1,
            "destination2": destination2,
            "categoryCount": len(categories),
            "url": f"{SITE_URL}/compare/{slug}/",
            "updatedAt": isoformat_mtime(html_path),
            "sourceUrl": f"{SITE_URL}/compare/{slug}/",
            "tags": unique_list([destination1, destination2])
        })

    with open(OUTPUT_DIR / "compare.json", 'w') as f:
        json.dump({"count": len(summaries), "comparisons": summaries}, f, indent=2, ensure_ascii=False)
    return summaries, len(summaries)


def build_search(dest_summaries, pick_summaries, itin_summaries, compare_summaries):
    records = []
    for d in dest_summaries:
        records.append(build_search_item(
            item_type="destination", slug=d["slug"], title=d["name"], subtitle=d.get("pitch", ""),
            url=f"{API_BASE_URL}/destinations/{d['slug']}.json", site_url=d.get("sourceUrl", f"{SITE_URL}/find/?q={d['slug']}"),
            tags=d.get("tags", []), extra={"region": d.get("region", ""), "continent": d.get("continent", "")}
        ))
    for p in pick_summaries:
        records.append(build_search_item(
            item_type="pick", slug=p["slug"], title=p["title"], subtitle=p.get("category", ""),
            url=f"{API_BASE_URL}/picks/{p['slug']}.json", site_url=p["url"], tags=p.get("tags", []), extra={"city": p.get("city", "")}
        ))
    for i in itin_summaries:
        records.append(build_search_item(
            item_type="itinerary", slug=i["slug"], title=i["title"], subtitle=i.get("duration", ""),
            url=f"{API_BASE_URL}/itineraries/{i['slug']}.json", site_url=i["url"], tags=i.get("tags", []), extra={"destination": i.get("destination", "")}
        ))
    for c in compare_summaries:
        records.append(build_search_item(
            item_type="comparison", slug=c["slug"], title=c["title"], subtitle=f"{c.get('destination1', '')} vs {c.get('destination2', '')}".strip(),
            url=f"{API_BASE_URL}/compare/{c['slug']}.json", site_url=c["url"], tags=c.get("tags", []),
            extra={"destination1": c.get("destination1", ""), "destination2": c.get("destination2", "")}
        ))

    payload = {
        "count": len(records),
        "types": {
            "destination": len(dest_summaries),
            "pick": len(pick_summaries),
            "itinerary": len(itin_summaries),
            "compare": len(compare_summaries),
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
        "version": "1.2.0",
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



def build_llms_txt(dest_count, picks_count, places_count, itin_count, compare_count):
    content = f'''# tabiji.ai

> Free AI-curated travel data API — Reddit-sourced restaurant picks, day-by-day itineraries, destination guides, and trending travel data for {dest_count} destinations. No API key required.

## API Documentation
- [API Docs](https://tabiji.ai/api/): Full endpoint documentation with examples
- [OpenAPI Spec](https://tabiji.ai/api/openapi.json): Machine-readable API specification (OpenAPI 3.1)
- [agents.json](https://tabiji.ai/.well-known/agents.json): AI agent workflow definitions

## Endpoints

### Destinations
- [All Destinations](https://tabiji.ai/api/v1/destinations.json): {dest_count} destinations with budget, season, vibes, travel styles, and pitch
- [Single Destination](https://tabiji.ai/api/v1/destinations/{{slug}}.json): Full details for one destination (e.g., `tokyo.json`, `paris.json`)

### Popular Picks (Restaurant & Attraction Guides)
- [All Picks](https://tabiji.ai/api/v1/picks.json): {picks_count} curated "best of" guides covering {places_count:,} places
- [Single Picks Guide](https://tabiji.ai/api/v1/picks/{{slug}}.json): Full guide with all places, Google ratings, hours, maps links, "what to order" tips, Reddit quotes, and insider tips (e.g., `amsterdam-brunch.json`, `tokyo-ramen.json`)

### Itineraries
- [All Itineraries](https://tabiji.ai/api/v1/itineraries.json): {itin_count} day-by-day travel itineraries
- [Single Itinerary](https://tabiji.ai/api/v1/itineraries/{{slug}}.json): Full itinerary with day-by-day activities, times, tips, and logistics

### Comparisons
- [All Comparisons](https://tabiji.ai/api/v1/compare.json): {compare_count} head-to-head destination comparisons
- [Single Comparison](https://tabiji.ai/api/v1/compare/{{slug}}.json): Full comparison with categories, Reddit quotes, verdict, and FAQs (e.g., `tokyo-vs-kyoto.json`)

### Cross-Collection Search
- [Unified Search](https://tabiji.ai/api/v1/search.json?q=tokyo): Search destinations, picks, itineraries, and comparisons from one endpoint (`q`, optional `type`, optional `limit`)

## Data Fields

### Place Object (in Picks)
Each place includes: name, position, cuisineTags, googleRating, reviewCount, priceRange, address, googleMapsUrl, openingHours (weekly grid), phone, website, photo, verdict, comparison, whatToOrder, redditQuotes (with source + sourceUrl), insiderTip

### Itinerary Day Object
Each day includes: dayLabel, neighborhoods, title, description, activities (with time, name, description, details, tips)

### Destination Object
Each destination includes: slug, name, region, continent, budget ($–$$$$), season, vibes (array), travelStyles (array), photo, pitch

## What Makes This Data Unique
Unlike generic travel APIs, tabiji data is curated from real traveler discussions (Reddit, forums) and enriched with Google Places data (ratings, hours, maps links). Every pick includes "what to order" recommendations and actual traveler quotes. Itineraries are time-blocked daily plans with real logistics, not just lists of places.

## Usage
No authentication required. All endpoints return static JSON files served via Cloudflare CDN. CORS is permissive — call from any origin. Free for non-commercial use.
'''
    (BASE_DIR / 'llms.txt').write_text(content, encoding='utf-8')


def build_agents_json(dest_count, picks_count, itin_count, compare_count):
    payload = {
        "$schema": "https://specs.openagents.com/agents-json/0.1/schema.json",
        "version": "0.1",
        "name": "tabiji.ai Travel API",
        "description": f"Free AI-curated travel data — Reddit-sourced restaurant picks, day-by-day itineraries, destination guides, destination comparisons, and unified search for {dest_count}+ destinations worldwide. No API key required.",
        "url": "https://tabiji.ai",
        "logo": "https://img.tabiji.ai/owl-logo.png",
        "contactEmail": "hello@tabiji.ai",
        "openapi": "https://tabiji.ai/api/openapi.json",
        "capabilities": {"streaming": False, "pushNotifications": False, "stateTransitionHistory": False},
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
        "skills": [
            {
                "id": "find-restaurants",
                "name": "Find Restaurants & Places",
                "description": f"Find the best restaurants, cafes, bars, or attractions in any city. Returns curated picks with ratings, hours, 'what to order' tips, and traveler quotes across {picks_count} guides.",
                "tags": ["restaurants", "food", "travel", "bars", "cafes", "attractions"],
                "examples": [
                    "Find the best ramen in Tokyo",
                    "Best brunch spots in Amsterdam",
                    "Where should I eat in Mexico City tonight?",
                    "Best rooftop bars in Bangkok"
                ],
                "inputModes": ["text"],
                "outputModes": ["text"],
                "steps": [
                    {"id": "search", "description": "Search all public travel data for relevant matches", "endpoint": {"method": "GET", "url": "https://tabiji.ai/api/v1/search.json?q={query}&type=pick"}},
                    {"id": "get-guide", "description": "Fetch the full guide with all places and details", "endpoint": {"method": "GET", "url": "https://tabiji.ai/api/v1/picks/{slug}.json"}}
                ]
            },
            {
                "id": "plan-trip",
                "name": "Plan a Trip",
                "description": f"Get a detailed day-by-day travel itinerary with activities, logistics, and timing across {itin_count} itineraries.",
                "tags": ["itinerary", "travel", "planning", "trip"],
                "examples": [
                    "Plan a 5-day trip to Tokyo",
                    "Weekend trip to Barcelona",
                    "Build me a 10-day Portugal itinerary",
                    "I need a honeymoon itinerary for Bali"
                ],
                "inputModes": ["text"],
                "outputModes": ["text"],
                "steps": [
                    {"id": "search", "description": "Search itinerary records by destination or trip style", "endpoint": {"method": "GET", "url": "https://tabiji.ai/api/v1/search.json?q={query}&type=itinerary"}},
                    {"id": "get-itinerary", "description": "Fetch the full itinerary", "endpoint": {"method": "GET", "url": "https://tabiji.ai/api/v1/itineraries/{slug}.json"}}
                ]
            },
            {
                "id": "compare-destinations",
                "name": "Compare Destinations",
                "description": f"Compare two destinations head-to-head across food, culture, cost, transport, seasonality, and fit across {compare_count} published comparisons.",
                "tags": ["compare", "travel", "destinations", "decision"],
                "examples": [
                    "Bali vs Thailand",
                    "Tokyo vs Kyoto",
                    "Portugal or Croatia for summer?",
                    "Mexico City vs Buenos Aires"
                ],
                "inputModes": ["text"],
                "outputModes": ["text"],
                "steps": [
                    {"id": "search", "description": "Search comparisons by either destination", "endpoint": {"method": "GET", "url": "https://tabiji.ai/api/v1/search.json?q={query}&type=compare"}},
                    {"id": "get-comparison", "description": "Fetch the full comparison with categories and verdict", "endpoint": {"method": "GET", "url": "https://tabiji.ai/api/v1/compare/{slug}.json"}}
                ]
            },
            {
                "id": "discover-destinations",
                "name": "Discover Destinations",
                "description": f"Browse and filter {dest_count} travel destinations by region, budget, season, vibes, and travel style.",
                "tags": ["destinations", "travel", "discover", "explore"],
                "examples": [
                    "Budget-friendly destinations in Asia",
                    "Romantic destinations in Europe",
                    "Warm places for a March trip",
                    "Adventure destinations with good food"
                ],
                "inputModes": ["text"],
                "outputModes": ["text"],
                "steps": [
                    {"id": "search", "description": "Search destinations by query", "endpoint": {"method": "GET", "url": "https://tabiji.ai/api/v1/search.json?q={query}&type=destination"}},
                    {"id": "get-destination", "description": "Get destination details", "endpoint": {"method": "GET", "url": "https://tabiji.ai/api/v1/destinations/{slug}.json"}}
                ]
            }
        ],
        "provider": {"organization": "tabiji.ai", "url": "https://tabiji.ai"}
    }
    out = BASE_DIR / '.well-known' / 'agents.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')


def build_docs_page(dest_count, picks_count, places_count, itin_count, compare_count):
    """Render api/index.html from api/index.html.template with live counts.

    The template uses {{TOKEN}} placeholders (e.g. {{DEST_COUNT}}).
    Formatted tokens get comma-separated numbers; _RAW tokens get plain ints.
    """
    template_path = BASE_DIR / 'api' / 'index.html.template'
    html_path = BASE_DIR / 'api' / 'index.html'
    content = template_path.read_text(encoding='utf-8')

    tokens = {
        'DEST_COUNT':    (f'{dest_count:,}', str(dest_count)),
        'PLACES_COUNT':  (f'{places_count:,}', str(places_count)),
        'PICKS_COUNT':   (f'{picks_count:,}', str(picks_count)),
        'ITIN_COUNT':    (f'{itin_count:,}', str(itin_count)),
        'COMPARE_COUNT': (f'{compare_count:,}', str(compare_count)),
    }

    for name, (formatted, raw) in tokens.items():
        content = content.replace('{{' + name + '}}', formatted)
        content = content.replace('{{' + name + '_RAW}}', raw)

    html_path.write_text(content, encoding='utf-8')


def build_openapi(dest_count, picks_count, places_count, itin_count, compare_count):
    openapi_path = BASE_DIR / 'api' / 'openapi.json'
    spec = json.loads(open(openapi_path, encoding='utf-8').read())

    spec['info']['version'] = '1.2.0'
    spec['info']['description'] = (
        f"Free REST API for AI-curated travel data — {dest_count} destinations, "
        f"{picks_count} curated picks guides ({places_count:,} place records), "
        f"{itin_count} day-by-day itineraries, {compare_count} destination comparisons, "
        f"and unified search. No API key required."
    )

    paths = spec.setdefault('paths', {})
    if '/search.json' in paths:
        search_get = paths['/search.json'].setdefault('get', {})
        for param in search_get.get('parameters', []):
            if param.get('name') == 'type':
                param.setdefault('schema', {})['enum'] = ['destination', 'pick', 'itinerary', 'compare']

    openapi_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False), encoding='utf-8')


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

    print("🧭 Regenerating agent/discovery docs...")
    build_openapi(dest_count, picks_count, places_count, itin_count, compare_count)
    build_llms_txt(dest_count, picks_count, places_count, itin_count, compare_count)
    build_agents_json(dest_count, picks_count, itin_count, compare_count)
    print("   ✅ openapi.json, llms.txt, agents.json")

    print("📄 Updating API docs page...")
    build_docs_page(dest_count, picks_count, places_count, itin_count, compare_count)
    print("   ✅ api/index.html")


if __name__ == "__main__":
    main()
