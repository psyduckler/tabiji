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


def isoformat_mtime(path):
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def make_id(record_type, slug):
    return f"{record_type}:{slug}"


def normalize_record_type(record_type):
    return "compare" if record_type == "comparison" else record_type


def unique_list(values):
    seen = set()
    result = []
    for value in values:
        if value in (None, '', []):
            continue
        value = clean_text(str(value)) if not isinstance(value, (int, float, bool)) else value
        if value in (None, '', []):
            continue
        if value in seen:
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


def build_search_item(item, *, item_type, slug, title, subtitle, url, site_url, tags=None, extra=None):
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
        record.update({k: v for k, v in extra.items() if v not in (None, '', [])})
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


def normalize_location_key(value):
    value = slugify(clean_text(value).lower()).replace('-', ' ')
    value = re.sub(r'\s+', ' ', value).strip()
    return value


def slug_to_name(slug):
    return clean_text(slug.replace('-', ' ').title())


METRO_PARENT_ALIASES = {
    'shinjuku': 'tokyo', 'shibuya': 'tokyo', 'ginza': 'tokyo', 'asakusa': 'tokyo', 'ueno': 'tokyo',
    'yanaka': 'tokyo', 'tsukiji': 'tokyo', 'toyosu': 'tokyo', 'roppongi': 'tokyo', 'ebisu': 'tokyo',
    'nakameguro': 'tokyo', 'daikanyama': 'tokyo', 'harajuku': 'tokyo', 'akita': 'tokyo',
    'de pijp': 'amsterdam', 'jordaan': 'amsterdam', 'oud west': 'amsterdam', 'watergraafsmeer': 'amsterdam',
    'plantage': 'amsterdam', 'centrum': 'amsterdam', 'vijzelstraat': 'amsterdam', 'singel': 'amsterdam',
    'trastevere': 'rome', 'le marais': 'paris', 'el born': 'barcelona', 'hongdae': 'seoul',
    'gangnam': 'seoul', 'itaewon': 'seoul', 'jongno': 'seoul', 'myeongdong': 'seoul', 'sinchon': 'seoul',
    'yeonnam dong': 'seoul', 'samcheong dong': 'seoul', 'mapo gu': 'seoul', 'bukchon': 'seoul',
    'namdaemun': 'seoul', 'shimokitazawa': 'tokyo', 'yaowarat': 'bangkok', 'bang rak': 'bangkok',
    'banglamphu': 'bangkok', 'victory monument': 'bangkok', 'rawai beach': 'phuket', 'old town phuket': 'phuket',
    'poblacion makati': 'manila', 'roma condesa': 'mexico city', 'miraflores': 'lima', 'barranco': 'lima'
}


DESTINATION_SCORE_OVERRIDES = {
    'tokyo': {'nightlifeScore': 0.95, 'walkabilityScore': 0.83, 'transitScore': 0.99, 'safetyScore': 0.93},
    'kyoto': {'walkabilityScore': 0.74, 'transitScore': 0.72, 'safetyScore': 0.92},
    'osaka': {'nightlifeScore': 0.91, 'walkabilityScore': 0.81, 'transitScore': 0.9, 'safetyScore': 0.9},
    'new york': {'nightlifeScore': 0.95, 'walkabilityScore': 0.88, 'transitScore': 0.91, 'safetyScore': 0.68},
    'london': {'nightlifeScore': 0.9, 'walkabilityScore': 0.86, 'transitScore': 0.93, 'safetyScore': 0.74},
    'paris': {'nightlifeScore': 0.88, 'walkabilityScore': 0.87, 'transitScore': 0.89, 'safetyScore': 0.75},
    'singapore': {'nightlifeScore': 0.78, 'walkabilityScore': 0.8, 'transitScore': 0.95, 'safetyScore': 0.95},
    'seoul': {'nightlifeScore': 0.9, 'walkabilityScore': 0.82, 'transitScore': 0.94, 'safetyScore': 0.88},
}


def destination_aliases(detail):
    aliases = set()
    name = clean_text(detail.get('name', ''))
    slug = clean_text(detail.get('slug', ''))
    region = clean_text(detail.get('region', ''))
    for value in [name, slug, region]:
        key = normalize_location_key(value)
        if key:
            aliases.add(key)
            parts = [p for p in key.split() if p]
            if parts:
                aliases.add(parts[0])
            if len(parts) >= 2:
                aliases.add(' '.join(parts[:2]))
    if ',' in name:
        aliases.add(normalize_location_key(name.split(',', 1)[0]))
    return {a for a in aliases if a}


def resolve_location_alias(value):
    key = normalize_location_key(value)
    if key in METRO_PARENT_ALIASES:
        return METRO_PARENT_ALIASES[key]
    return key


def infer_budget_band(budget_text):
    budget_text = clean_text(budget_text)
    if not budget_text:
        return ''
    dollar_count = budget_text.count('$')
    if dollar_count <= 1:
        return 'budget'
    if dollar_count == 2:
        return 'midrange'
    if dollar_count == 3:
        return 'medium-high'
    return 'luxury'


def clamp_score(value, minimum=0.0, maximum=1.0):
    return max(minimum, min(maximum, round(value, 2)))


def infer_destination_attributes(detail):
    vibes = {clean_text(v).lower() for v in detail.get('vibes', [])}
    travel_styles = {clean_text(v).lower() for v in detail.get('travelStyles', [])}
    budget_band = infer_budget_band(detail.get('budget', ''))

    name_aliases = destination_aliases(detail)
    override = None
    for alias in sorted(name_aliases, key=len, reverse=True):
        if alias in DESTINATION_SCORE_OVERRIDES:
            override = DESTINATION_SCORE_OVERRIDES[alias]
            break

    nightlife = 0.92 if 'nightlife' in vibes else 0.62 if 'city' in vibes else None
    family = 0.86 if 'family' in vibes else 0.55
    walkability = 0.8 if 'city' in vibes else None
    transit = 0.86 if 'city' in vibes else None
    safety = None
    hassle = 0.58 if 'adventure' in travel_styles else 0.36 if 'city' in vibes else 0.28

    if budget_band == 'budget':
        hassle += 0.06
    elif budget_band == 'luxury':
        family += 0.04
        if walkability is not None:
            walkability += 0.02

    if 'relaxation' in travel_styles:
        trip_pace = 'slow'
    elif 'adventure' in travel_styles:
        trip_pace = 'fast'
    elif 'photography' in travel_styles or 'cultural' in vibes:
        trip_pace = 'medium'
    else:
        trip_pace = 'medium-fast' if 'city' in vibes else 'medium'

    normalized = {
        'budgetBand': budget_band,
        'tripPace': trip_pace,
        'familyFriendliness': clamp_score(family),
        'nightlifeScore': clamp_score(nightlife) if nightlife is not None else None,
        'walkabilityScore': clamp_score(walkability) if walkability is not None else None,
        'transitScore': clamp_score(transit) if transit is not None else None,
        'safetyScore': clamp_score(safety) if safety is not None else None,
        'hassleLevel': clamp_score(hassle),
        'bestForTags': [clean_text(tag).lower() for tag in unique_list([*(detail.get('travelStyles') or []), *(detail.get('vibes') or [])])],
        'recommendedTripLengthsDays': [3, 4, 5] if 'city' in vibes else [4, 5, 7],
    }
    if override:
        for key, value in override.items():
            normalized[key] = clamp_score(value)

    return {'normalized': normalized}


def infer_price_tier(price_range):
    price_range = clean_text(price_range)
    if not price_range:
        return None
    if any(token in price_range for token in ['100–', '120–', '€3', '€4', '$3', '$4', '¥100', '¥200', '¥300']):
        return 1
    if any(token in price_range for token in ['¥3', '¥4', '¥5', '¥6', '¥7', '$8', '$9', '$10', '$11', '$12', '€8', '€9', '€10', '€11', '€12']):
        return 2
    if any(token in price_range for token in ['¥1,', '$13', '$14', '$15', '$16', '$17', '$18', '€13', '€14', '€15', '€16', '€17', '€18']):
        return 3
    return 4


def compact_known_for_values(place, cuisine_tags):
    values = list(cuisine_tags)
    raw = clean_text(place.get('whatToOrder', ''))
    raw = re.split(r'[.!?]', raw)[0]
    for piece in re.split(r',|;|\band\b|\bwith\b', raw):
        piece = clean_text(piece).strip(' -–:')
        if not piece:
            continue
        if len(piece) > 40:
            continue
        if re.search(r'\b(get|add|order|arrive|same price|best)\b', piece.lower()):
            continue
        values.append(piece)
    return unique_list(values)[:5]


def infer_place_operational_fields(place, guide):
    text = ' '.join([
        clean_text(guide.get('title', '')),
        clean_text(guide.get('category', '')),
        clean_text(place.get('name', '')),
        clean_text(place.get('whatToOrder', '')),
        clean_text(place.get('insiderTip', '')),
        clean_text(place.get('verdict', ''))
    ]).lower()
    cuisine_tags = [clean_text(tag) for tag in place.get('cuisineTags', [])]
    category = cuisine_tags[0] if cuisine_tags else clean_text(guide.get('category', ''))

    meal_types = []
    if any(token in text for token in ['breakfast', 'brunch']):
        meal_types.append('breakfast')
    if any(token in text for token in ['lunch', 'market lunch']):
        meal_types.append('lunch')
    if any(token in text for token in ['dinner', 'izakaya', 'bar', 'cocktail', 'late-night']):
        meal_types.append('dinner')
    if any(token in text for token in ['late-night', 'golden gai', 'nightlife', 'bar']):
        meal_types.append('late-night')
    if not meal_types:
        meal_types = ['anytime']

    reservation_needed = any(token in text for token in ['reservation', 'reserve', 'book ahead', 'prebook'])
    if any(token in text for token in ['arrive early', 'queue', 'line moves fast', 'wait']) and not reservation_needed:
        wait_time_level = 'medium'
    elif any(token in text for token in ['long waits', 'longest waits', 'crowded', 'fills up fast']):
        wait_time_level = 'high'
    else:
        wait_time_level = 'low' if place.get('openNow') else 'unknown'

    ideal_time = []
    if place.get('openingHours'):
        hours_blob = ' '.join(place['openingHours'].values()).lower()
        if '24 hours' in hours_blob or '4:00 am' in hours_blob or '7:30 am' in hours_blob:
            ideal_time.append('morning')
        if '10:00 pm' in hours_blob or '11:00 pm' in hours_blob or '3:00 am' in hours_blob:
            ideal_time.append('evening')
    if any(token in text for token in ['sunset', 'evening']):
        ideal_time.append('evening')
    if any(token in text for token in ['late-night', 'nightlife']):
        ideal_time.append('late-night')
    if not ideal_time:
        ideal_time = ['lunch', 'dinner'] if 'food' in text or 'restaurant' in text else ['daytime']

    dietary_tags = []
    if any(token in text for token in ['vegan', 'plant-based']):
        dietary_tags.append('vegan-friendly')
    if 'vegetarian' in text:
        dietary_tags.append('vegetarian-friendly')
    if any(token in text for token in ['seafood', 'sushi', 'fish']):
        dietary_tags.append('seafood')
    if any(token in text for token in ['beef', 'pork', 'meat', 'yakitori']):
        dietary_tags.append('meat-focused')

    payment_types = ['card'] if place.get('website') else []
    if any(token in text for token in ['cash', 'cash-only', 'cash friendly']):
        payment_types.append('cash')
    if not payment_types:
        payment_types = ['cash', 'card']

    touristy = 'high' if any(token in text for token in ['tourist', 'first-timer', 'legendary', 'famous']) else 'medium'
    if any(token in text for token in ['locals', 'neighborhood', 'under the tourist radar']):
        touristy = 'low-medium'

    return {
        'category': category,
        'mealTypes': unique_list(meal_types),
        'priceTier': infer_price_tier(place.get('priceRange', '')),
        'reservationNeeded': reservation_needed,
        'idealTimeToGo': unique_list(ideal_time),
        'knownFor': compact_known_for_values(place, cuisine_tags),
        'waitTimeLevel': wait_time_level,
        'dietaryTags': unique_list(dietary_tags),
        'paymentTypes': unique_list(payment_types),
        'touristyLevel': touristy,
    }


def infer_itinerary_operational_fields(detail, destination_detail=None):
    title = clean_text(detail.get('title', '')).lower()
    duration_text = clean_text(detail.get('duration', ''))
    match = re.search(r'(\d+)', duration_text)
    duration_days = int(match.group(1)) if match else max(1, detail.get('dayCount', 1))
    if 'relax' in title:
        pace = 'slow'
    elif any(token in title for token in ['food', 'nightlife', 'adventure']):
        pace = 'medium-fast'
    else:
        pace = 'medium'

    budget_band = ((destination_detail or {}).get('normalized') or {}).get('budgetBand', '')
    if budget_band == 'budget':
        budget = {'budget': 70, 'midrange': 130, 'high': 220}
    elif budget_band == 'luxury':
        budget = {'budget': 150, 'midrange': 280, 'high': 500}
    else:
        budget = {'budget': 90, 'midrange': 180, 'high': 320}

    day_intensity = []
    for day in detail.get('days', []):
        neighborhoods = [part.strip() for part in clean_text(day.get('neighborhoods', '')).split('·') if part.strip()]
        activities = day.get('activities', []) or []
        score = 0.35 + (0.12 * min(len(neighborhoods), 4)) + (0.08 * min(len(activities), 4))
        if pace == 'medium-fast':
            score += 0.1
        elif pace == 'slow':
            score -= 0.08
        day['dayIntensityScore'] = clamp_score(score)
        day['transitSegments'] = day.get('transitSegments', [])
        day['rainyDayAlternatives'] = day.get('rainyDayAlternatives', [])
        day_intensity.append(day['dayIntensityScore'])

    return {
        'durationDays': duration_days,
        'pace': pace,
        'estimatedDailyBudget': budget,
        'reservationRequirements': [],
        'openingHoursVerified': False,
        'familySuitability': clamp_score(0.72 if 'family' in title else 0.58),
        'mobilityNotes': [],
        'averageDayIntensityScore': clamp_score(sum(day_intensity) / len(day_intensity)) if day_intensity else None,
    }


def score_destination_match(text, dest):
    key = resolve_location_alias(text)
    if not key:
        return 0
    aliases = dest.get('_aliases', set())
    if key in aliases:
        return 100
    if any(key in alias or alias in key for alias in aliases):
        return 70
    return 0


def best_destination_match(text_candidates, destinations):
    best = None
    best_score = 0
    for dest in destinations:
        score = max(score_destination_match(text, dest) for text in text_candidates if text)
        if score > best_score:
            best = dest
            best_score = score
    return best if best_score >= 70 else None


def infer_pick_destination_candidates(pick):
    candidates = [pick.get('city', ''), pick.get('title', ''), pick.get('slug', '').split('-')[0]]
    key = resolve_location_alias(pick.get('city', ''))
    if key and key != normalize_location_key(pick.get('city', '')):
        candidates.append(key)
    return unique_list(candidates)


def infer_itinerary_destination_candidates(itin):
    candidates = [itin.get('destination', ''), itin.get('title', ''), itin.get('slug', '')]
    key = resolve_location_alias(itin.get('destination', ''))
    if key and key != normalize_location_key(itin.get('destination', '')):
        candidates.append(key)
    return unique_list(candidates)


def infer_best_for_first_timers(compare):
    texts = [
        clean_text((compare.get('verdict') or {}).get('summary', '')),
        *[clean_text(card.get('text', '')) for card in (compare.get('verdict') or {}).get('cards', [])],
        *[clean_text(item) for item in (compare.get('verdict') or {}).get('takeaways', [])],
    ]
    left = normalize_location_key(compare.get('destination1', ''))
    right = normalize_location_key(compare.get('destination2', ''))
    for text in texts:
        lower = text.lower()
        if 'first-timer' not in lower and 'first timer' not in lower:
            continue
        for dest_key in [left, right]:
            if dest_key and (f'{dest_key} is better for first-timers' in lower or f'choose {dest_key}' in lower or f'{dest_key} for first-timers' in lower):
                return dest_key.replace(' ', '-')
    return ''


def link_records(destinations, picks, itineraries, comparisons):
    dest_by_slug = {}
    for dest in destinations:
        dest['_aliases'] = destination_aliases(dest)
        dest_by_slug[dest['slug']] = dest
        dest.setdefault('related', {})
        dest['related'].update({
            'pickSlugs': [],
            'itinerarySlugs': [],
            'comparisonSlugs': [],
            'nearbyDestinationSlugs': [],
            'dayTripDestinationSlugs': [],
        })

    for pick in picks:
        dest = best_destination_match(infer_pick_destination_candidates(pick), destinations)
        if dest:
            pick['destinationSlug'] = dest['slug']
            dest['related']['pickSlugs'].append(pick['slug'])

    for itin in itineraries:
        dest = best_destination_match(infer_itinerary_destination_candidates(itin), destinations)
        if dest:
            itin['destinationSlug'] = dest['slug']
            dest['related']['itinerarySlugs'].append(itin['slug'])

    for compare in comparisons:
        compare['destinationSlugs'] = []
        for field in ['destination1', 'destination2']:
            dest = best_destination_match([compare.get(field, '')], destinations)
            if dest:
                compare['destinationSlugs'].append(dest['slug'])
                dest['related']['comparisonSlugs'].append(compare['slug'])

    for compare in comparisons:
        related_picks = []
        related_itins = []
        for slug in compare.get('destinationSlugs', []):
            dest = dest_by_slug.get(slug)
            if not dest:
                continue
            related_picks.extend(dest['related']['pickSlugs'])
            related_itins.extend(dest['related']['itinerarySlugs'])
        compare['relatedPickSlugs'] = unique_list(related_picks)[:12]
        compare['relatedItinerarySlugs'] = unique_list(related_itins)[:12]

    for pick in picks:
        pick['relatedItinerarySlugs'] = []
        pick['relatedComparisonSlugs'] = []
        if pick.get('destinationSlug'):
            dest = dest_by_slug.get(pick['destinationSlug'])
            if dest:
                pick['relatedItinerarySlugs'] = unique_list(dest['related']['itinerarySlugs'])[:8]
                pick['relatedComparisonSlugs'] = unique_list(dest['related']['comparisonSlugs'])[:8]

    for itin in itineraries:
        itin['relatedPickSlugs'] = []
        itin['relatedComparisonSlugs'] = []
        if itin.get('destinationSlug'):
            dest = dest_by_slug.get(itin['destinationSlug'])
            if dest:
                itin['relatedPickSlugs'] = unique_list(dest['related']['pickSlugs'])[:10]
                itin['relatedComparisonSlugs'] = unique_list(dest['related']['comparisonSlugs'])[:8]

    for dest in destinations:
        dest.pop('_aliases', None)


def enrich_generated_records(dest_summaries, pick_summaries, itin_summaries, compare_summaries):
    dest_dir = OUTPUT_DIR / 'destinations'
    pick_dir = OUTPUT_DIR / 'picks'
    itin_dir = OUTPUT_DIR / 'itineraries'
    compare_dir = OUTPUT_DIR / 'compare'

    destinations = []
    for summary in dest_summaries:
        path = dest_dir / f"{summary['slug']}.json"
        detail = json.loads(path.read_text())
        detail.update(infer_destination_attributes(detail))
        destinations.append(detail)

    picks = []
    for summary in pick_summaries:
        path = pick_dir / f"{summary['slug']}.json"
        detail = json.loads(path.read_text())
        detail['operational'] = {
            'guideCategory': clean_text(detail.get('category', '')),
            'destinationHint': clean_text(detail.get('city', '')),
        }
        for place in detail.get('places', []):
            place['operational'] = infer_place_operational_fields(place, detail)
        picks.append(detail)

    dest_lookup = {d['slug']: d for d in destinations}

    itineraries = []
    for summary in itin_summaries:
        path = itin_dir / f"{summary['slug']}.json"
        detail = json.loads(path.read_text())
        itineraries.append(detail)

    comparisons = []
    for summary in compare_summaries:
        path = compare_dir / f"{summary['slug']}.json"
        detail = json.loads(path.read_text())
        detail['structured'] = {
            'budgetWinner': '',
            'foodWinner': '',
            'cultureWinner': '',
            'bestForFirstTimers': '',
        }
        for category in detail.get('categories', []):
            title = clean_text(category.get('title', '')).lower()
            winner = clean_text((category.get('winnerSummary') or {}).get('winner', ''))
            if 'food' in title and winner:
                detail['structured']['foodWinner'] = winner.lower()
            elif 'culture' in title and winner:
                detail['structured']['cultureWinner'] = winner.lower()
            elif 'cost' in title and winner:
                detail['structured']['budgetWinner'] = winner.lower()
        detail['structured']['bestForFirstTimers'] = infer_best_for_first_timers(detail)
        comparisons.append(detail)

    link_records(destinations, picks, itineraries, comparisons)

    for detail in itineraries:
        detail.update(infer_itinerary_operational_fields(detail, dest_lookup.get(detail.get('destinationSlug', ''))))

    for detail in destinations:
        detail['related'] = {k: unique_list(v) for k, v in detail.get('related', {}).items()}
        (dest_dir / f"{detail['slug']}.json").write_text(json.dumps(detail, indent=2, ensure_ascii=False), encoding='utf-8')
        for summary in dest_summaries:
            if summary['slug'] == detail['slug']:
                summary['normalized'] = detail.get('normalized', {})
                summary['related'] = {k: detail['related'].get(k, []) for k in ['pickSlugs', 'itinerarySlugs', 'comparisonSlugs']}
                break

    for detail in picks:
        (pick_dir / f"{detail['slug']}.json").write_text(json.dumps(detail, indent=2, ensure_ascii=False), encoding='utf-8')
        for summary in pick_summaries:
            if summary['slug'] == detail['slug']:
                summary['destinationSlug'] = detail.get('destinationSlug', '')
                summary['relatedItinerarySlugs'] = detail.get('relatedItinerarySlugs', [])
                summary['relatedComparisonSlugs'] = detail.get('relatedComparisonSlugs', [])
                break

    for detail in itineraries:
        (itin_dir / f"{detail['slug']}.json").write_text(json.dumps(detail, indent=2, ensure_ascii=False), encoding='utf-8')
        for summary in itin_summaries:
            if summary['slug'] == detail['slug']:
                summary['destinationSlug'] = detail.get('destinationSlug', '')
                summary['pace'] = detail.get('pace', '')
                summary['estimatedDailyBudget'] = detail.get('estimatedDailyBudget', {})
                summary['relatedPickSlugs'] = detail.get('relatedPickSlugs', [])
                summary['relatedComparisonSlugs'] = detail.get('relatedComparisonSlugs', [])
                break

    for detail in comparisons:
        (compare_dir / f"{detail['slug']}.json").write_text(json.dumps(detail, indent=2, ensure_ascii=False), encoding='utf-8')
        for summary in compare_summaries:
            if summary['slug'] == detail['slug']:
                summary['destinationSlugs'] = detail.get('destinationSlugs', [])
                summary['structured'] = detail.get('structured', {})
                break

    (OUTPUT_DIR / 'destinations.json').write_text(json.dumps({'count': len(dest_summaries), 'destinations': dest_summaries}, indent=2, ensure_ascii=False), encoding='utf-8')
    total_places = sum(p.get('placeCount', 0) for p in pick_summaries)
    (OUTPUT_DIR / 'picks.json').write_text(json.dumps({'count': len(pick_summaries), 'totalPlaces': total_places, 'picks': pick_summaries}, indent=2, ensure_ascii=False), encoding='utf-8')
    (OUTPUT_DIR / 'itineraries.json').write_text(json.dumps({'count': len(itin_summaries), 'itineraries': itin_summaries}, indent=2, ensure_ascii=False), encoding='utf-8')
    (OUTPUT_DIR / 'compare.json').write_text(json.dumps({'count': len(compare_summaries), 'comparisons': compare_summaries}, indent=2, ensure_ascii=False), encoding='utf-8')

    return dest_summaries, pick_summaries, itin_summaries, compare_summaries


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
        if day.get("title") or day.get("activities"):
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
    value = re.sub(r'\b(Itinerary|Guide)\b', '', value).strip(' :-—()')
    value = re.sub(r'\s+', ' ', value).strip()
    return value


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
    title_dest_match = re.search(r'(?:Day[s]?\s+(?:in\s+)?|Night[s]?\s+(?:in\s+)?)([A-Z][a-z]+(?:[\s-][A-Z][a-z]+)*)', title)
    if title_dest_match:
        destination = clean_itinerary_destination(title_dest_match.group(1))
    if not destination:
        dest_match2 = re.search(r'in\s+([A-Z][a-z]+(?:[\s-][A-Z][a-z]+)*)', title)
        if dest_match2:
            destination = clean_itinerary_destination(dest_match2.group(1))
    slug_destination = clean_itinerary_destination(derive_destination_from_itinerary_slug(slug))
    destination_words = {word.lower() for word in re.split(r'\s+', destination) if word}
    noisy_destination_words = {'food', 'nightlife', 'romantic', 'relaxation', 'adventure', 'guide', 'itinerary', 'budget', 'family', 'solo', 'culture'}
    if (not destination) or any(token in destination.lower() for token in ['itinerary', 'guide']) or (destination_words & noisy_destination_words):
        if slug_destination:
            destination = slug_destination

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
    for stale in output_itin_dir.glob('*.json'):
        stale.unlink()

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
        api_itin = attach_record_meta({
            **itin,
            "sourceSlug": itin["slug"],
        }, record_type="itinerary", slug=filename, source_path=(BASE_DIR / itin['source'] / itin['slug'] / 'index.html'), source_url=itin['url'], tags=[itin.get('destination', ''), *(itin.get('tripType', []) or [])])
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
            "updatedAt": api_itin["updatedAt"],
            "sourceUrl": itin["url"],
            "tags": unique_list([itin.get('destination', ''), *(itin.get('tripType', []) or [])])
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

        detail = attach_record_meta({
            "slug": slug,
            "title": title,
            "description": desc,
            "destination1": destination1,
            "destination2": destination2,
            "heroImage": hero_image,
            "url": f"{SITE_URL}/compare/{slug}/",
            "categoryCount": len(categories),
            "categories": [c for c in categories if c.get('summary') or c.get('highlights') or c.get('redditQuotes') or c.get('winnerSummary')],
            "verdict": verdict,
            "faqs": faqs
        }, record_type="compare", slug=slug, source_path=html_path, source_url=f"{SITE_URL}/compare/{slug}/", tags=[destination1, destination2])

        with open(output_compare_dir / f"{slug}.json", 'w') as f:
            json.dump(detail, f, indent=2, ensure_ascii=False)

        summaries.append({
            "id": make_id("compare", slug),
            "type": "compare",
            "slug": slug,
            "title": title,
            "destination1": destination1,
            "destination2": destination2,
            "categoryCount": detail["categoryCount"],
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
        records.append(build_search_item(d, item_type="destination", slug=d["slug"], title=d["name"], subtitle=d.get("pitch", ""), url=f"{API_BASE_URL}/destinations/{d['slug']}.json", site_url=d.get("sourceUrl", f"{SITE_URL}/find/?q={d['slug']}"), tags=d.get("tags", []), extra={"region": d.get("region", ""), "continent": d.get("continent", "")}))
    for p in pick_summaries:
        records.append(build_search_item(p, item_type="pick", slug=p["slug"], title=p["title"], subtitle=p.get("category", ""), url=f"{API_BASE_URL}/picks/{p['slug']}.json", site_url=p["url"], tags=p.get("tags", []), extra={"city": p.get("city", "")}))
    for i in itin_summaries:
        records.append(build_search_item(i, item_type="itinerary", slug=i["slug"], title=i["title"], subtitle=i.get("duration", ""), url=f"{API_BASE_URL}/itineraries/{i['slug']}.json", site_url=i["url"], tags=i.get("tags", []), extra={"destination": i.get("destination", "")}))
    for c in compare_summaries:
        records.append(build_search_item(c, item_type="compare", slug=c["slug"], title=c["title"], subtitle=f"{c.get('destination1', '')} vs {c.get('destination2', '')}".strip(), url=f"{API_BASE_URL}/compare/{c['slug']}.json", site_url=c["url"], tags=c.get("tags", []), extra={"destination1": c.get("destination1", ""), "destination2": c.get("destination2", "")}))

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
        "version": "1.1.0",
        "description": "Free REST API for AI-curated travel data — destinations, restaurant picks, itineraries, comparisons, unified search, and agent-friendly linked metadata. No API key required.",
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

    print("🧠 Enriching linked records...")
    dest_summaries, picks_summaries, itin_summaries, compare_summaries = enrich_generated_records(dest_summaries, picks_summaries, itin_summaries, compare_summaries)
    print("   ✅ linked entities + normalized metadata")

    print("🔎 Building search index...")
    search_payload = build_search(dest_summaries, picks_summaries, itin_summaries, compare_summaries)
    print(f"   ✅ {search_payload['count']} documents")

    print("📋 Building index...")
    build_index(dest_count, picks_count, places_count, itin_count, compare_count, search_payload['count'])
    print("   ✅ index.json")


if __name__ == "__main__":
    main()
