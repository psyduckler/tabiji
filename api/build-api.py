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
import unicodedata
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
API_VERSION = "1.5.0"
API_SCHEMA_VERSION = "1.0"
COUNTRY_FACTS_PATH = BASE_DIR / "api" / "data" / "country-facts.json"
DESTINATION_COUNTRY_MAP_PATH = BASE_DIR / "api" / "data" / "destination-country-map.json"

CONFIDENCE_EDITORIAL = 0.9
CONFIDENCE_PICK_SUMMARY = 0.78
CONFIDENCE_PLACE_CATALOG = 0.74
EDITORIAL_SIGNAL_STRONG = 0.7
EDITORIAL_SIGNAL_WEAK = 0.35


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


def make_freshness(updated_at, *, confidence="editorial", confidence_score=CONFIDENCE_EDITORIAL, operational_fields_may_change=False):
    return {
        "updatedAt": updated_at,
        "lastVerifiedAt": updated_at,
        "confidence": confidence,
        "confidenceScore": confidence_score,
        "operationalFieldsMayChange": operational_fields_may_change,
    }


def make_provenance(*, source_path, source_url, updated_at, sources=None):
    provenance = {
        "sources": unique_list(sources or ["tabiji_static_page"]),
        "sourceUrl": source_url,
        "lastVerifiedAt": updated_at,
    }
    if source_path:
        provenance["sourcePath"] = source_path
    return provenance


def make_summary_meta(*, record_type, slug, updated_at, source_url, tags=None, source_path=None, confidence="editorial", confidence_score=CONFIDENCE_EDITORIAL, operational_fields_may_change=False):
    normalized_type = normalize_record_type(record_type)
    meta = {
        "id": make_id(record_type, slug),
        "type": normalized_type,
        "entityType": normalized_type,
        "schemaVersion": API_SCHEMA_VERSION,
        "updatedAt": updated_at,
        "sourceUrl": source_url,
        "tags": unique_list(tags or []),
        "freshness": make_freshness(updated_at, confidence=confidence, confidence_score=confidence_score, operational_fields_may_change=operational_fields_may_change),
        "provenance": make_provenance(source_path=source_path, source_url=source_url, updated_at=updated_at),
    }
    if source_path:
        meta["sourceMeta"] = {
            "sourceType": "tabiji-static-page",
            "sourcePath": source_path,
            "sourceUrl": source_url,
            "lastVerified": updated_at,
        }
    return meta


def attach_record_meta(payload, *, record_type, slug, source_path, source_url, tags=None):
    updated_at = isoformat_mtime(source_path)
    source_path_value = str(source_path.relative_to(BASE_DIR)) if source_path.is_relative_to(BASE_DIR) else str(source_path)
    payload.update(make_summary_meta(
        record_type=record_type,
        slug=slug,
        updated_at=updated_at,
        source_url=source_url,
        source_path=source_path_value,
        tags=tags,
    ))
    return payload


def load_json_if_exists(path):
    if not path.exists():
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def title_case_slug(slug):
    return ' '.join(part.capitalize() for part in (slug or '').split('-') if part)


def normalize_name_key(value):
    value = clean_text(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = value.lower()
    value = re.sub(r'[^a-z0-9]+', ' ', value)
    return re.sub(r'\s+', ' ', value).strip()


def make_destination_country_key(name, region):
    return normalize_name_key(f"{name} {region}")


def load_country_facts():
    if COUNTRY_FACTS_PATH.exists():
        with open(COUNTRY_FACTS_PATH) as f:
            return json.load(f)
    return {}


def load_destination_country_map():
    if DESTINATION_COUNTRY_MAP_PATH.exists():
        with open(DESTINATION_COUNTRY_MAP_PATH) as f:
            return json.load(f)
    return {}


DESTINATION_ALIASES = {
    'nyc': 'new-york-city',
    'new york city': 'new-york-city',
    'saigon': 'ho-chi-minh',
    'hcmc': 'ho-chi-minh',
    'ho chi minh city': 'ho-chi-minh',
    'petaling jaya': 'petaling-jaya',
    'pj': 'petaling-jaya',
    'mauritius': 'mauritius',
    'zanzibar': 'zanzibar',
    'gili islands': 'gili-islands',
}


def truncate_list(items, limit=6):
    return items[:limit]


def make_related_summary(*, item_type, slug, title, url, extra=None):
    summary = {
        "id": make_id(item_type, slug),
        "type": normalize_record_type(item_type),
        "slug": slug,
        "title": title,
        "url": url,
    }
    if extra:
        summary.update({k: v for k, v in extra.items() if v not in (None, "", [])})
    return summary


def collect_field_source_labels(field_sources):
    labels = []
    for values in (field_sources or {}).values():
        if isinstance(values, list):
            labels.extend(values)
        elif values:
            labels.append(values)
    return unique_list(labels)


def infer_area_from_address(address):
    address = clean_text(address)
    if not address:
        return ""
    parts = [part.strip() for part in re.split(r'[·•,|]', address) if part.strip()]
    if not parts:
        return ""
    candidate = parts[0]
    if re.search(r'\d', candidate) and len(parts) > 1:
        candidate = parts[1]
    candidate = re.sub(r'^(near|in|at|behind)\s+', '', candidate, flags=re.IGNORECASE).strip()
    return candidate if len(candidate) <= 60 else ""


def enrich_place(place, *, guide_slug, guide_title, guide_url, city, category):
    place = dict(place)
    if place.get("googleMapsUrl"):
        place["mapsLinks"] = {"google": place["googleMapsUrl"]}
    if place.get("address") and not place.get("area"):
        area = infer_area_from_address(place.get("address", ""))
        if area:
            place["area"] = area
    if place.get("verdict") and not place.get("editorialSummary"):
        place["editorialSummary"] = place["verdict"]
    if place.get("comparison", {}).get("best for") and not place.get("bestFor"):
        place["bestFor"] = place["comparison"].get("best for")
    if not place.get("sourceMeta"):
        field_sources = {
            "name": ["editorial"],
            "position": ["editorial"],
            "cuisineTags": ["editorial"],
            "whatToOrder": ["editorial"],
            "insiderTip": ["editorial"],
            "verdict": ["editorial"],
            "editorialSummary": ["editorial"],
            "bestFor": ["editorial"],
            "address": ["editorial", "maps"],
            "area": ["editorial", "derived"],
            "website": ["maps"],
            "phone": ["maps"],
            "googleRating": ["maps"],
            "reviewCount": ["maps"],
            "priceRange": ["maps", "editorial"],
            "openingHours": ["maps"],
            "googleMapsUrl": ["maps"],
            "mapsLinks": ["derived"],
            "photo": ["editorial"],
            "redditQuotes": ["reddit"],
        }
        present_field_sources = {
            key: value for key, value in field_sources.items() if key in place and place.get(key) not in (None, "", [])
        }
        place["sourceMeta"] = {
            "guideSlug": guide_slug,
            "guideTitle": guide_title,
            "guideUrl": guide_url,
            "collectionCity": city,
            "collectionCategory": category,
            "fieldSources": present_field_sources,
        }
    return place


def write_json(path, payload):
    with open(path, 'w') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def same_record_ignoring_updated_at(left, right):
    if not isinstance(left, dict) or not isinstance(right, dict):
        return left == right
    left = dict(left)
    right = dict(right)
    left.pop("updatedAt", None)
    right.pop("updatedAt", None)
    return left == right


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

    country_facts = load_country_facts()
    destination_country_map = load_destination_country_map()

    summaries = []
    used_slugs = set()
    for dest in destinations:
        slug = make_unique_slug(slugify(dest.get("name", "")), dest, used_slugs)
        if not slug:
            continue

        destination_country_key = make_destination_country_key(dest.get("name", ""), dest.get("region", ""))
        country_mapping = destination_country_map.get(destination_country_key, {})
        country_fact = country_facts.get(country_mapping.get("countryCode", ""), {})

        detail_path = dest_dir / f"{slug}.json"
        detail = attach_record_meta({
            "slug": slug,
            "name": dest.get("name", ""),
            "region": dest.get("region", ""),
            "continent": dest.get("continent", ""),
            "country": country_fact.get("country", country_mapping.get("country", "")),
            "countryCode": country_mapping.get("countryCode", ""),
            "currency": country_fact.get("currency", {}),
            "language": country_fact.get("language", ""),
            "languages": country_fact.get("languages", []),
            "flag": country_fact.get("flag", {}),
            "timezone": country_fact.get("timezone", ""),
            "timezones": country_fact.get("timezones", []),
            "coordinates": country_mapping.get("coordinates", country_fact.get("coordinates", {})),
            "plugType": country_fact.get("plugType", []),
            "drivingSide": country_fact.get("drivingSide", ""),
            "dialCode": country_fact.get("dialCode", ""),
            "tapWaterSafe": country_fact.get("tapWaterSafe"),
            "tippingCustom": country_fact.get("tippingCustom", ""),
            "visaNote": country_fact.get("visaNote", ""),
            "photo": dest.get("photo", ""),
            "pitch": dest.get("pitch", ""),
            "budget": dest.get("budget", ""),
            "season": dest.get("season", ""),
            "vibes": dest.get("vibes", []),
            "travelStyles": dest.get("travel", []),
            "url": f"{SITE_URL}/find/?q={slug}"
        }, record_type="destination", slug=slug, source_path=src, source_url=f"{SITE_URL}/find/?q={slug}", tags=[dest.get("region", ""), dest.get("continent", ""), country_fact.get("country", ""), country_mapping.get("countryCode", ""), *(dest.get("vibes", []) or []), *(dest.get("travel", []) or [])])

        existing_detail = load_json_if_exists(detail_path)
        if same_record_ignoring_updated_at(existing_detail, detail) and existing_detail:
            detail["updatedAt"] = existing_detail.get("updatedAt", detail["updatedAt"])
            detail = existing_detail | {"updatedAt": detail["updatedAt"]}
        else:
            write_json(detail_path, detail)

        updated_at = isoformat_mtime(src)
        summary_tags = [dest.get("region", ""), dest.get("continent", ""), country_fact.get("country", ""), country_mapping.get("countryCode", ""), *(dest.get("vibes", []) or []), *(dest.get("travel", []) or [])]
        summaries.append({
            "slug": slug,
            "name": dest.get("name", ""),
            "region": dest.get("region", ""),
            "continent": dest.get("continent", ""),
            "country": country_fact.get("country", country_mapping.get("country", "")),
            "countryCode": country_mapping.get("countryCode", ""),
            "currency": country_fact.get("currency", {}),
            "language": country_fact.get("language", ""),
            "flag": country_fact.get("flag", {}),
            "timezone": country_fact.get("timezone", ""),
            "coordinates": country_mapping.get("coordinates", country_fact.get("coordinates", {})),
            "plugType": country_fact.get("plugType", []),
            "drivingSide": country_fact.get("drivingSide", ""),
            "dialCode": country_fact.get("dialCode", ""),
            "tapWaterSafe": country_fact.get("tapWaterSafe"),
            "tippingCustom": country_fact.get("tippingCustom", ""),
            "visaNote": country_fact.get("visaNote", ""),
            "budget": dest.get("budget", ""),
            "season": dest.get("season", ""),
            "vibes": dest.get("vibes", []),
            "photo": dest.get("photo", ""),
            "pitch": dest.get("pitch", "")
        } | make_summary_meta(
            record_type="destination",
            slug=slug,
            updated_at=updated_at,
            source_url=f"{SITE_URL}/find/?q={slug}",
            source_path=str(src.relative_to(BASE_DIR)) if src.is_relative_to(BASE_DIR) else str(src),
            tags=summary_tags,
        ))

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

        updated_at = isoformat_mtime(html_path)
        summaries.append({
            "slug": slug,
            "title": title,
            "description": desc,
            "city": city,
            "category": category,
            "placeCount": len(places),
            "url": f"{SITE_URL}/popular-picks/{slug}/"
        } | make_summary_meta(
            record_type="pick",
            slug=slug,
            updated_at=updated_at,
            source_url=f"{SITE_URL}/popular-picks/{slug}/",
            source_path=str(html_path.relative_to(BASE_DIR)) if html_path.is_relative_to(BASE_DIR) else str(html_path),
            tags=[city, category],
            confidence="mixed",
            confidence_score=0.78,
            operational_fields_may_change=True,
        ))

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
            "slug": filename,
            "title": itin["title"],
            "destination": itin["destination"],
            "duration": itin["duration"],
            "tripType": itin["tripType"],
            "url": itin["url"],
            "dayCount": itin["dayCount"]
        } | make_summary_meta(
            record_type="itinerary",
            slug=filename,
            updated_at=itin["updatedAt"],
            source_url=itin["sourceUrl"],
            source_path=itin.get("sourceMeta", {}).get("sourcePath"),
            tags=[itin["destination"], *(itin["tripType"] or [])],
        ))

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

        updated_at = isoformat_mtime(html_path)
        summaries.append({
            "slug": slug,
            "title": title,
            "destination1": destination1,
            "destination2": destination2,
            "categoryCount": len(categories),
            "url": f"{SITE_URL}/compare/{slug}/"
        } | make_summary_meta(
            record_type="comparison",
            slug=slug,
            updated_at=updated_at,
            source_url=f"{SITE_URL}/compare/{slug}/",
            source_path=str(html_path.relative_to(BASE_DIR)) if html_path.is_relative_to(BASE_DIR) else str(html_path),
            tags=[destination1, destination2],
        ))

    with open(OUTPUT_DIR / "compare.json", 'w') as f:
        json.dump({"count": len(summaries), "comparisons": summaries}, f, indent=2, ensure_ascii=False)
    return summaries, len(summaries)


def build_relationships(dest_summaries, pick_summaries, itin_summaries, compare_summaries):
    destination_lookup = {}
    destination_slug_by_name = {}
    for dest in dest_summaries:
        destination_lookup[dest["slug"]] = dest
        destination_slug_by_name[normalize_name_key(dest.get("name", ""))] = dest["slug"]

    picks_by_destination = {}
    itins_by_destination = {}
    compares_by_destination = {}
    compare_pairs = {}

    destination_name_pairs = sorted(destination_slug_by_name.items(), key=lambda item: len(item[0]), reverse=True)

    def destination_slug_for_name(name):
        key = normalize_name_key(name)
        if not key:
            return ''
        alias_slug = DESTINATION_ALIASES.get(key, '')
        if alias_slug in destination_lookup:
            return alias_slug
        if key in destination_slug_by_name:
            return destination_slug_by_name[key]
        slug_guess = slugify(key.replace(' ', '-')) if key else ''
        return slug_guess if slug_guess in destination_lookup else ''

    def destination_slug_for_text(*values):
        haystack = normalize_name_key(' '.join(value for value in values if value))
        if not haystack:
            return ''
        for name_key, slug in destination_name_pairs:
            if len(name_key) < 4:
                continue
            if re.search(rf'(^| )' + re.escape(name_key) + r'( |$)', haystack):
                return slug
        return ''

    pick_detail_updates = {}
    for pick in pick_summaries:
        destination_slug = (
            destination_slug_for_name(pick.get("city", ""))
            or destination_slug_for_text(pick.get("title", ""), pick.get("description", ""), pick.get("city", ""), pick.get("slug", "").replace('-', ' '))
        )
        pick["destinationSlug"] = destination_slug
        pick["destinationName"] = destination_lookup.get(destination_slug, {}).get("name", pick.get("city", "")) if destination_slug else pick.get("city", "")
        if destination_slug:
            picks_by_destination.setdefault(destination_slug, []).append(pick)
        pick_detail_updates[pick["slug"]] = {
            "destinationSlug": destination_slug,
            "destinationName": pick.get("destinationName", ""),
        }

    itin_detail_updates = {}
    for itin in itin_summaries:
        destination_slug = (
            destination_slug_for_name(itin.get("destination", ""))
            or destination_slug_for_text(itin.get("title", ""), itin.get("description", ""), itin.get("destination", ""), itin.get("slug", "").replace('-', ' '))
        )
        itin["destinationSlug"] = destination_slug
        if destination_slug:
            itins_by_destination.setdefault(destination_slug, []).append(itin)
        itin_detail_updates[itin["slug"]] = {"destinationSlug": destination_slug}

    compare_detail_updates = {}
    for compare in compare_summaries:
        dest1_slug = destination_slug_for_name(compare.get("destination1", ""))
        dest2_slug = destination_slug_for_name(compare.get("destination2", ""))
        compare["destination1Slug"] = dest1_slug
        compare["destination2Slug"] = dest2_slug
        compare["destinationSlugs"] = [slug for slug in [dest1_slug, dest2_slug] if slug]
        for slug in compare["destinationSlugs"]:
            compares_by_destination.setdefault(slug, []).append(compare)
        if dest1_slug and dest2_slug:
            compare_pairs[frozenset([dest1_slug, dest2_slug])] = compare
        compare_detail_updates[compare["slug"]] = {
            "destination1Slug": dest1_slug,
            "destination2Slug": dest2_slug,
            "destinationSlugs": compare["destinationSlugs"],
        }

    for dest in dest_summaries:
        slug = dest["slug"]
        related_picks = [
            make_related_summary(item_type="pick", slug=pick["slug"], title=pick["title"], url=pick["url"], extra={"category": pick.get("category", "")})
            for pick in picks_by_destination.get(slug, [])
        ]
        related_itins = [
            make_related_summary(item_type="itinerary", slug=itin["slug"], title=itin["title"], url=itin["url"], extra={"duration": itin.get("duration", "")})
            for itin in itins_by_destination.get(slug, [])
        ]
        related_compares = [
            make_related_summary(item_type="comparison", slug=compare["slug"], title=compare["title"], url=compare["url"], extra={"vs": [compare.get("destination1", ""), compare.get("destination2", "")]})
            for compare in compares_by_destination.get(slug, [])
        ]
        nearby_destinations = []
        seen_nearby = set()
        for compare in compares_by_destination.get(slug, []):
            other_slug = compare.get("destination1Slug") if compare.get("destination2Slug") == slug else compare.get("destination2Slug")
            if not other_slug or other_slug in seen_nearby or other_slug not in destination_lookup:
                continue
            seen_nearby.add(other_slug)
            other_dest = destination_lookup[other_slug]
            nearby_destinations.append(make_related_summary(item_type="destination", slug=other_slug, title=other_dest["name"], url=f"{API_BASE_URL}/destinations/{other_slug}.json", extra={"region": other_dest.get("region", "")}))

        detail_path = OUTPUT_DIR / "destinations" / f"{slug}.json"
        detail = load_json_if_exists(detail_path)
        if detail:
            detail["editorialSummary"] = detail.get("editorialSummary") or detail.get("pitch", "")
            detail["bestFor"] = detail.get("bestFor") or unique_list([*(detail.get("vibes", []) or []), *(detail.get("travelStyles", []) or [])])[:6]
            detail["relatedPicks"] = truncate_list(related_picks)
            detail["relatedItineraries"] = truncate_list(related_itins)
            detail["relatedComparisons"] = truncate_list(related_compares)
            detail["relatedDestinations"] = truncate_list(nearby_destinations)
            write_json(detail_path, detail)

        dest["relatedPicks"] = truncate_list(related_picks)
        dest["relatedItineraries"] = truncate_list(related_itins)
        dest["relatedComparisons"] = truncate_list(related_compares)
        dest["relatedDestinations"] = truncate_list(nearby_destinations)

    for pick in pick_summaries:
        slug = pick["slug"]
        destination_slug = pick.get("destinationSlug", "")
        sibling_picks = []
        if destination_slug:
            sibling_picks = [
                make_related_summary(item_type="pick", slug=other["slug"], title=other["title"], url=other["url"], extra={"category": other.get("category", "")})
                for other in picks_by_destination.get(destination_slug, []) if other["slug"] != slug
            ]
        detail_path = OUTPUT_DIR / "picks" / f"{slug}.json"
        detail = load_json_if_exists(detail_path)
        if detail:
            detail.update(pick_detail_updates.get(slug, {}))
            detail["editorialSummary"] = detail.get("editorialSummary") or detail.get("description", "")
            detail["bestFor"] = detail.get("bestFor") or unique_list([detail.get("city", ""), detail.get("category", "")])
            detail["relatedPicks"] = truncate_list(sibling_picks)
            detail["relatedItineraries"] = truncate_list([
                make_related_summary(item_type="itinerary", slug=itin["slug"], title=itin["title"], url=itin["url"], extra={"duration": itin.get("duration", "")})
                for itin in itins_by_destination.get(destination_slug, [])
            ])
            detail["relatedComparisons"] = truncate_list([
                make_related_summary(item_type="comparison", slug=compare["slug"], title=compare["title"], url=compare["url"])
                for compare in compares_by_destination.get(destination_slug, [])
            ]) if destination_slug else []
            detail["places"] = [enrich_place(place, guide_slug=slug, guide_title=detail.get("title", slug), guide_url=detail.get("url", ""), city=detail.get("city", ""), category=detail.get("category", "")) for place in detail.get("places", [])]
            write_json(detail_path, detail)
        pick["relatedPicks"] = truncate_list(sibling_picks)

    for itin in itin_summaries:
        slug = itin["slug"]
        destination_slug = itin.get("destinationSlug", "")
        detail_path = OUTPUT_DIR / "itineraries" / f"{slug}.json"
        detail = load_json_if_exists(detail_path)
        if detail:
            detail.update(itin_detail_updates.get(slug, {}))
            detail["editorialSummary"] = detail.get("editorialSummary") or detail.get("description", "")
            detail["relatedPicks"] = truncate_list([
                make_related_summary(item_type="pick", slug=pick["slug"], title=pick["title"], url=pick["url"], extra={"category": pick.get("category", "")})
                for pick in picks_by_destination.get(destination_slug, [])
            ])
            detail["relatedComparisons"] = truncate_list([
                make_related_summary(item_type="comparison", slug=compare["slug"], title=compare["title"], url=compare["url"])
                for compare in compares_by_destination.get(destination_slug, [])
            ]) if destination_slug else []
            write_json(detail_path, detail)

    for compare in compare_summaries:
        slug = compare["slug"]
        detail_path = OUTPUT_DIR / "compare" / f"{slug}.json"
        detail = load_json_if_exists(detail_path)
        if detail:
            detail.update(compare_detail_updates.get(slug, {}))
            related_destinations = []
            for dest_slug in detail.get("destinationSlugs", []):
                if dest_slug in destination_lookup:
                    destination = destination_lookup[dest_slug]
                    related_destinations.append(make_related_summary(item_type="destination", slug=dest_slug, title=destination.get("name", title_case_slug(dest_slug)), url=f"{API_BASE_URL}/destinations/{dest_slug}.json", extra={"region": destination.get("region", "")}))
            detail["relatedDestinations"] = truncate_list(related_destinations)
            related_itins = []
            related_picks = []
            seen_itins = set()
            seen_picks = set()
            for dest_slug in detail.get("destinationSlugs", []):
                for itin in itins_by_destination.get(dest_slug, []):
                    if itin["slug"] in seen_itins:
                        continue
                    seen_itins.add(itin["slug"])
                    related_itins.append(make_related_summary(item_type="itinerary", slug=itin["slug"], title=itin["title"], url=itin["url"], extra={"duration": itin.get("duration", "")}))
                for pick in picks_by_destination.get(dest_slug, []):
                    if pick["slug"] in seen_picks:
                        continue
                    seen_picks.add(pick["slug"])
                    related_picks.append(make_related_summary(item_type="pick", slug=pick["slug"], title=pick["title"], url=pick["url"], extra={"category": pick.get("category", "")}))
            detail["relatedItineraries"] = truncate_list(related_itins)
            detail["relatedPicks"] = truncate_list(related_picks)
            detail["editorialSummary"] = detail.get("editorialSummary") or detail.get("description", "")
            write_json(detail_path, detail)

    write_json(OUTPUT_DIR / "destinations.json", {"count": len(dest_summaries), "destinations": dest_summaries})
    write_json(OUTPUT_DIR / "picks.json", {"count": len(pick_summaries), "picks": pick_summaries})
    write_json(OUTPUT_DIR / "itineraries.json", {"count": len(itin_summaries), "itineraries": itin_summaries})
    write_json(OUTPUT_DIR / "compare.json", {"count": len(compare_summaries), "comparisons": compare_summaries})


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


def build_catalog(dest_summaries, pick_summaries, itin_summaries, compare_summaries):
    # Catalog place entities are hydrated from generated pick detail files,
    # so this must run after build_picks() has written api/v1/picks/*.json.
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    items = []

    for dest in dest_summaries:
        items.append({
            "id": dest["id"],
            "entityType": "destination",
            "schemaVersion": dest.get("schemaVersion", API_SCHEMA_VERSION),
            "source": "destinations",
            "slug": dest["slug"],
            "name": dest.get("name", ""),
            "title": dest.get("name", ""),
            "description": dest.get("pitch", ""),
            "countryCode": dest.get("countryCode", ""),
            "country": dest.get("country", ""),
            "region": dest.get("region", ""),
            "continent": dest.get("continent", ""),
            "locationLabel": dest.get("country", "") or dest.get("region", ""),
            "category": "destination",
            "tags": dest.get("tags", []),
            "highlights": unique_list([*(dest.get("vibes", []) or []), *(dest.get("travelStyles", []) or [])]),
            "priceLevel": dest.get("budget", ""),
            "url": f"{API_BASE_URL}/destinations/{dest['slug']}.json",
            "freshness": dest.get("freshness", make_freshness(dest.get("updatedAt", generated_at))),
            "provenance": dest.get("provenance", {}),
        })

    for pick in pick_summaries:
        items.append({
            "id": pick["id"],
            "entityType": "pick",
            "schemaVersion": pick.get("schemaVersion", API_SCHEMA_VERSION),
            "source": "picks",
            "slug": pick["slug"],
            "title": pick.get("title", ""),
            "description": pick.get("description", ""),
            "city": pick.get("city", ""),
            "destinationSlug": pick.get("destinationSlug", ""),
            "locationLabel": pick.get("city", ""),
            "category": pick.get("category", ""),
            "tags": pick.get("tags", []),
            "highlights": unique_list([pick.get("city", ""), pick.get("category", "")]),
            "itemCount": pick.get("placeCount", 0),
            "url": f"{API_BASE_URL}/picks/{pick['slug']}.json",
            "freshness": pick.get("freshness", make_freshness(pick.get("updatedAt", generated_at), confidence="mixed", confidence_score=CONFIDENCE_PICK_SUMMARY, operational_fields_may_change=True)),
            "provenance": pick.get("provenance", {}),
        })

        detail = load_json_if_exists(OUTPUT_DIR / "picks" / f"{pick['slug']}.json") or {}
        for place in detail.get("places", []):
            place_id = place.get("id") or f"place:{pick['slug']}:{slugify(place.get('name', 'place'))}"
            items.append({
                "id": place_id,
                "entityType": "place",
                "schemaVersion": API_SCHEMA_VERSION,
                "source": "picks",
                "slug": pick["slug"],
                "parentId": pick["id"],
                "name": place.get("name", ""),
                "title": pick.get("title", ""),
                "description": place.get("editorialSummary") or place.get("verdict") or pick.get("description", ""),
                "city": detail.get("city", pick.get("city", "")),
                "destinationSlug": pick.get("destinationSlug", ""),
                "locationLabel": place.get("address") or place.get("area") or detail.get("city", pick.get("city", "")),
                "category": detail.get("category", pick.get("category", "")),
                "tags": unique_list([*(place.get("tags", []) or []), *(place.get("cuisineTags", []) or []), *(pick.get("tags", []) or [])]),
                "highlights": place.get("bestFor") if isinstance(place.get("bestFor"), list) else unique_list([place.get("bestFor", ""), *(place.get("highlights", []) or [])]),
                "priceLevel": place.get("priceRange", ""),
                "ratingNormalized": place.get("googleRating"),
                "editorialSignal": EDITORIAL_SIGNAL_STRONG if place.get("editorialSummary") or place.get("verdict") else EDITORIAL_SIGNAL_WEAK,
                "url": f"{API_BASE_URL}/picks/{pick['slug']}.json#{slugify(place.get('name', 'place'))}",
                "freshness": make_freshness(
                    detail.get("updatedAt", generated_at),
                    confidence="mixed",
                    confidence_score=CONFIDENCE_PLACE_CATALOG,
                    operational_fields_may_change=True,
                ),
                "provenance": {
                    "sources": unique_list(["tabiji_static_page", "tabiji_editorial", *collect_field_source_labels(place.get("sourceMeta", {}).get("fieldSources", {}))]),
                    "parentId": pick["id"],
                    "sourceUrl": detail.get("sourceUrl", pick.get("sourceUrl", "")),
                    "lastVerifiedAt": detail.get("updatedAt", generated_at),
                },
            })

    for itin in itin_summaries:
        items.append({
            "id": itin["id"],
            "entityType": "itinerary",
            "schemaVersion": itin.get("schemaVersion", API_SCHEMA_VERSION),
            "source": "itineraries",
            "slug": itin["slug"],
            "title": itin.get("title", ""),
            "description": itin.get("editorialSummary") or itin.get("title", ""),
            "destination": itin.get("destination", ""),
            "destinationSlug": itin.get("destinationSlug", ""),
            "locationLabel": itin.get("destination", ""),
            "category": "itinerary",
            "tags": itin.get("tags", []),
            "highlights": itin.get("tripType", []),
            "duration": itin.get("duration", ""),
            "itemCount": itin.get("dayCount", 0),
            "url": f"{API_BASE_URL}/itineraries/{itin['slug']}.json",
            "freshness": itin.get("freshness", make_freshness(itin.get("updatedAt", generated_at))),
            "provenance": itin.get("provenance", {}),
        })

    for compare in compare_summaries:
        items.append({
            "id": compare["id"],
            "entityType": "compare",
            "schemaVersion": compare.get("schemaVersion", API_SCHEMA_VERSION),
            "source": "compare",
            "slug": compare["slug"],
            "title": compare.get("title", ""),
            "description": compare.get("editorialSummary") or compare.get("title", ""),
            "destination1": compare.get("destination1", ""),
            "destination2": compare.get("destination2", ""),
            "destinationSlugs": compare.get("destinationSlugs", []),
            "locationLabel": f"{compare.get('destination1', '')} vs {compare.get('destination2', '')}".strip(),
            "category": "compare",
            "tags": compare.get("tags", []),
            "highlights": unique_list(compare.get("destinationSlugs", [])),
            "itemCount": compare.get("categoryCount", 0),
            "url": f"{API_BASE_URL}/compare/{compare['slug']}.json",
            "freshness": compare.get("freshness", make_freshness(compare.get("updatedAt", generated_at))),
            "provenance": compare.get("provenance", {}),
        })

    payload = {
        "version": API_VERSION,
        "schemaVersion": API_SCHEMA_VERSION,
        "generatedAt": generated_at,
        "itemCount": len(items),
        "items": items,
    }
    write_json(OUTPUT_DIR / "catalog.json", payload)
    return payload


# ============================================================
# INDEX
# ============================================================

def build_index(dest_count, picks_count, places_count, itin_count, compare_count, search_count):
    index = {
        "name": "tabiji.ai API",
        "version": API_VERSION,
        "description": "Free REST API for AI-curated travel data — destinations, restaurant picks, itineraries, comparisons, a normalized catalog, and unified search. No API key required.",
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
            {"path": "/catalog.json", "description": "Normalized entity catalog spanning destinations, picks, places, itineraries, and comparisons", "method": "GET"},
            {"path": "/manifest.json", "description": "Global dataset manifest with versions, checksums, and file metadata", "method": "GET"},
            {"path": "/countries/{iso2}/manifest.json", "description": "Per-country manifest with version/checksum metadata for importable country data", "method": "GET"},
            {"path": "/search.json?q={query}", "description": f"Cross-collection search across {search_count} documents", "method": "GET"},
        ],
        "dataSource": "Curated from Tabiji editorial pages, traveler discussions, and selective place enrichment. Records include cross-links plus provenance/freshness metadata.",
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
- [Single Picks Guide](https://tabiji.ai/api/v1/picks/{{slug}}.json): Full guide with all places, editorial summaries, maps links, source metadata, "what to order" tips, Reddit quotes, and insider tips (e.g., `amsterdam-brunch.json`, `tokyo-ramen.json`)

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
Each place includes: name, position, cuisineTags, googleRating, reviewCount, priceRange, address, area, googleMapsUrl, mapsLinks, openingHours (weekly grid), phone, website, photo, verdict, editorialSummary, bestFor, comparison, whatToOrder, redditQuotes (with source + sourceUrl), insiderTip, sourceMeta

### Itinerary Day Object
Each day includes: dayLabel, neighborhoods, title, description, activities (with time, name, description, details, tips)

### Destination Object
Each destination includes: slug, name, region, continent, budget ($–$$$$), season, vibes (array), travelStyles (array), photo, pitch, editorialSummary, bestFor, relatedPicks, relatedItineraries, relatedComparisons, relatedDestinations, sourceMeta

## What Makes This Data Unique
Unlike generic travel APIs, tabiji data is curated from real traveler discussions plus Tabiji editorial judgment, then cross-linked across destinations, picks, itineraries, and comparisons. Records now expose provenance/freshness metadata and lighter-weight enrichment fields so agents can traverse the graph instead of scraping pages.

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
                "description": f"Find the best restaurants, cafes, bars, or attractions in any city. Returns curated picks with editorial summaries, source metadata, 'what to order' tips, and traveler quotes across {picks_count} guides.",
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


def build_country_facts():
    """Build country facts API from restcountries.com data. Idempotent."""
    import subprocess
    script = BASE_DIR / "api" / "build-country-facts.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ⚠️  Country facts build failed:\n{result.stderr}")
        return 0
    # Count generated files
    countries_dir = OUTPUT_DIR / "countries"
    if countries_dir.exists():
        return len(list(countries_dir.glob("*.json")))
    return 0


def build_manifests():
    """Build lightweight dataset manifests from already-generated api/v1 outputs."""
    import subprocess
    script = BASE_DIR / "api" / "build-manifests.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ⚠️  Manifest build failed:\n{result.stderr}")
        return False
    return True


def build_docs_page(dest_count, picks_count, places_count, itin_count, compare_count, country_count=0):
    """Render api/index.html from api/index.html.template with live counts.

    The template uses {{TOKEN}} placeholders (e.g. {{DEST_COUNT}}).
    Formatted tokens get comma-separated numbers; _RAW tokens get plain ints.
    """
    template_path = BASE_DIR / 'api' / 'index.html.template'
    html_path = BASE_DIR / 'api' / 'index.html'
    content = template_path.read_text(encoding='utf-8')

    tokens = {
        'DEST_COUNT':     (f'{dest_count:,}', str(dest_count)),
        'PLACES_COUNT':   (f'{places_count:,}', str(places_count)),
        'PICKS_COUNT':    (f'{picks_count:,}', str(picks_count)),
        'ITIN_COUNT':     (f'{itin_count:,}', str(itin_count)),
        'COMPARE_COUNT':  (f'{compare_count:,}', str(compare_count)),
        'COUNTRY_COUNT':  (f'{country_count:,}', str(country_count)),
    }

    for name, (formatted, raw) in tokens.items():
        content = content.replace('{{' + name + '}}', formatted)
        content = content.replace('{{' + name + '_RAW}}', raw)

    html_path.write_text(content, encoding='utf-8')


def build_openapi(dest_count, picks_count, places_count, itin_count, compare_count):
    openapi_path = BASE_DIR / 'api' / 'openapi.json'
    spec = json.loads(open(openapi_path, encoding='utf-8').read())

    spec['info']['version'] = API_VERSION
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

    paths['/catalog.json'] = {
        'get': {
            'summary': 'Normalized entity catalog spanning destinations, picks, places, itineraries, and comparisons',
            'responses': {
                '200': {
                    'description': 'Catalog response',
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/CatalogResponse'}
                        }
                    }
                }
            }
        }
    }
    paths['/manifest.json'] = {
        'get': {
            'summary': 'Global dataset manifest with versions, checksums, and file metadata',
            'responses': {
                '200': {
                    'description': 'Global manifest response',
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/GlobalManifest'}
                        }
                    }
                }
            }
        }
    }
    paths['/countries/{iso2}/manifest.json'] = {
        'get': {
            'summary': 'Per-country manifest with versions, checksums, and file metadata',
            'parameters': [
                {
                    'name': 'iso2',
                    'in': 'path',
                    'required': True,
                    'schema': {'type': 'string', 'pattern': '^[A-Z]{2}$'}
                }
            ],
            'responses': {
                '200': {
                    'description': 'Country manifest response',
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/CountryManifest'}
                        }
                    }
                }
            }
        }
    }

    schemas = spec.setdefault('components', {}).setdefault('schemas', {})

    schemas['RelatedRecordSummary'] = {
        'type': 'object',
        'properties': {
            'id': {'type': 'string', 'example': 'pick:tokyo-ramen'},
            'type': {'type': 'string', 'enum': ['destination', 'pick', 'itinerary', 'compare']},
            'slug': {'type': 'string', 'example': 'tokyo-ramen'},
            'title': {'type': 'string', 'example': '12 Best Ramen in Tokyo'},
            'url': {'type': 'string', 'format': 'uri'},
        },
        'additionalProperties': True,
    }
    schemas['RecordSourceMeta'] = {
        'type': 'object',
        'properties': {
            'sourceType': {'type': 'string', 'example': 'tabiji-static-page'},
            'sourcePath': {'type': 'string', 'example': 'popular-picks/tokyo-ramen/index.html'},
            'sourceUrl': {'type': 'string', 'format': 'uri'},
            'lastVerified': {'type': 'string', 'format': 'date-time'},
        },
    }
    schemas['PlaceSourceMeta'] = {
        'type': 'object',
        'properties': {
            'guideSlug': {'type': 'string'},
            'guideTitle': {'type': 'string'},
            'guideUrl': {'type': 'string', 'format': 'uri'},
            'collectionCity': {'type': 'string'},
            'collectionCategory': {'type': 'string'},
            'fieldSources': {
                'type': 'object',
                'additionalProperties': {
                    'type': 'array',
                    'items': {'type': 'string'}
                }
            },
        },
    }
    schemas['FreshnessMeta'] = {
        'type': 'object',
        'properties': {
            'updatedAt': {'type': 'string', 'format': 'date-time'},
            'lastVerifiedAt': {'type': 'string', 'format': 'date-time'},
            'confidence': {'type': 'string'},
            'confidenceScore': {'type': 'number'},
            'operationalFieldsMayChange': {'type': 'boolean'},
        },
    }
    schemas['ProvenanceMeta'] = {
        'type': 'object',
        'properties': {
            'sources': {'type': 'array', 'items': {'type': 'string'}},
            'sourcePath': {'type': 'string'},
            'sourceUrl': {'type': 'string', 'format': 'uri'},
            'lastVerifiedAt': {'type': 'string', 'format': 'date-time'},
            'parentId': {'type': 'string'},
        },
        'additionalProperties': True,
    }
    schemas['CatalogEntity'] = {
        'type': 'object',
        'required': ['id', 'entityType', 'schemaVersion', 'source', 'slug', 'tags', 'freshness', 'provenance'],
        'properties': {
            'id': {'type': 'string'},
            'entityType': {'type': 'string', 'enum': ['destination', 'pick', 'place', 'itinerary', 'compare']},
            'schemaVersion': {'type': 'string'},
            'source': {'type': 'string'},
            'slug': {'type': 'string'},
            'title': {'type': 'string'},
            'name': {'type': 'string'},
            'description': {'type': 'string'},
            'tags': {'type': 'array', 'items': {'type': 'string'}},
            'freshness': {'$ref': '#/components/schemas/FreshnessMeta'},
            'provenance': {'$ref': '#/components/schemas/ProvenanceMeta'},
        },
        'additionalProperties': True,
    }
    schemas['CatalogResponse'] = {
        'type': 'object',
        'properties': {
            'version': {'type': 'string'},
            'schemaVersion': {'type': 'string'},
            'generatedAt': {'type': 'string', 'format': 'date-time'},
            'itemCount': {'type': 'integer'},
            'items': {'type': 'array', 'items': {'$ref': '#/components/schemas/CatalogEntity'}},
        },
        'required': ['version', 'schemaVersion', 'generatedAt', 'itemCount', 'items'],
    }
    schemas['ManifestFileMeta'] = {
        'type': 'object',
        'required': ['path', 'contentType', 'sizeBytes', 'sha256', 'updatedAt'],
        'properties': {
            'path': {'type': 'string'},
            'contentType': {'type': 'string'},
            'sizeBytes': {'type': 'integer'},
            'sha256': {'type': 'string'},
            'updatedAt': {'type': 'string', 'format': 'date-time'},
        },
    }
    schemas['GlobalManifest'] = {
        'type': 'object',
        'required': ['apiVersion', 'schemaVersion', 'datasetVersion', 'generatedAt', 'compatibility', 'datasets', 'countries'],
        'properties': {
            'apiVersion': {'type': 'string'},
            'schemaVersion': {'type': 'string'},
            'datasetVersion': {'type': 'string'},
            'generatedAt': {'type': 'string', 'format': 'date-time'},
            'compatibility': {'type': 'object', 'additionalProperties': True},
            'datasets': {'type': 'object', 'additionalProperties': {'$ref': '#/components/schemas/ManifestFileMeta'}},
            'countries': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'iso2': {'type': 'string'},
                        'manifestPath': {'type': 'string'},
                        'datasetVersion': {'type': 'string'},
                        'entityCounts': {'type': 'object', 'additionalProperties': {'type': 'integer'}},
                        'countryFactsPath': {'type': 'string'},
                        'countryFactsSha256': {'type': 'string'},
                        'updatedAt': {'type': 'string', 'format': 'date-time'},
                    },
                    'required': ['iso2', 'manifestPath', 'datasetVersion', 'countryFactsPath', 'countryFactsSha256', 'updatedAt'],
                }
            },
        },
    }
    schemas['CountryManifest'] = {
        'type': 'object',
        'required': ['apiVersion', 'schemaVersion', 'manifestType', 'iso2', 'name', 'datasetVersion', 'generatedAt', 'compatibility', 'files', 'entityCounts', 'relatedDestinationSlugs', 'staleAfter'],
        'properties': {
            'apiVersion': {'type': 'string'},
            'schemaVersion': {'type': 'string'},
            'manifestType': {'type': 'string', 'enum': ['country']},
            'iso2': {'type': 'string'},
            'iso3': {'type': 'string'},
            'name': {'type': 'string'},
            'datasetVersion': {'type': 'string'},
            'generatedAt': {'type': 'string', 'format': 'date-time'},
            'compatibility': {'type': 'object', 'additionalProperties': True},
            'files': {'type': 'object', 'additionalProperties': {'$ref': '#/components/schemas/ManifestFileMeta'}},
            'entityCounts': {'type': 'object', 'additionalProperties': {'type': 'integer'}},
            'relatedDestinationSlugs': {'type': 'array', 'items': {'type': 'string'}},
            'staleAfter': {'type': 'string', 'format': 'date-time'},
        },
    }

    destination_summary = schemas.setdefault('DestinationSummary', {}).setdefault('properties', {})
    destination_summary['id'] = {'type': 'string', 'example': 'destination:tokyo'}
    destination_summary['type'] = {'type': 'string', 'enum': ['destination']}
    destination_summary['updatedAt'] = {'type': 'string', 'format': 'date-time'}
    destination_summary['sourceUrl'] = {'type': 'string', 'format': 'uri'}
    destination_summary['tags'] = {'type': 'array', 'items': {'type': 'string'}}
    destination_summary['sourceMeta'] = {'$ref': '#/components/schemas/RecordSourceMeta'}
    destination_summary['editorialSummary'] = {'type': 'string'}
    destination_summary['bestFor'] = {'type': 'array', 'items': {'type': 'string'}}
    destination_summary['relatedPicks'] = {'type': 'array', 'items': {'$ref': '#/components/schemas/RelatedRecordSummary'}}
    destination_summary['relatedItineraries'] = {'type': 'array', 'items': {'$ref': '#/components/schemas/RelatedRecordSummary'}}
    destination_summary['relatedComparisons'] = {'type': 'array', 'items': {'$ref': '#/components/schemas/RelatedRecordSummary'}}
    destination_summary['relatedDestinations'] = {'type': 'array', 'items': {'$ref': '#/components/schemas/RelatedRecordSummary'}}

    place_props = schemas.setdefault('Place', {}).setdefault('properties', {})
    place_props['area'] = {'type': 'string', 'example': 'De Pijp'}
    place_props['verdict'] = {'type': 'string'}
    place_props['editorialSummary'] = {'type': 'string'}
    place_props['bestFor'] = {'type': 'string'}
    place_props['comparison'] = {'type': 'object', 'additionalProperties': True}
    place_props['mapsLinks'] = {
        'type': 'object',
        'properties': {'google': {'type': 'string', 'format': 'uri'}}
    }
    place_props['sourceMeta'] = {'$ref': '#/components/schemas/PlaceSourceMeta'}

    picks_summary = schemas.setdefault('PicksSummary', {}).setdefault('properties', {})
    picks_summary['description'] = {'type': 'string'}
    picks_summary['destinationSlug'] = {'type': 'string'}
    picks_summary['destinationName'] = {'type': 'string'}
    picks_summary['relatedPicks'] = {'type': 'array', 'items': {'$ref': '#/components/schemas/RelatedRecordSummary'}}

    picks_detail = schemas.setdefault('PicksDetail', {}).setdefault('properties', {})
    picks_detail['id'] = {'type': 'string', 'example': 'pick:tokyo-ramen'}
    picks_detail['type'] = {'type': 'string', 'enum': ['pick']}
    picks_detail['updatedAt'] = {'type': 'string', 'format': 'date-time'}
    picks_detail['sourceUrl'] = {'type': 'string', 'format': 'uri'}
    picks_detail['tags'] = {'type': 'array', 'items': {'type': 'string'}}
    picks_detail['sourceMeta'] = {'$ref': '#/components/schemas/RecordSourceMeta'}
    picks_detail['destinationSlug'] = {'type': 'string'}
    picks_detail['destinationName'] = {'type': 'string'}
    picks_detail['editorialSummary'] = {'type': 'string'}
    picks_detail['bestFor'] = {'type': 'array', 'items': {'type': 'string'}}
    picks_detail['relatedPicks'] = {'type': 'array', 'items': {'$ref': '#/components/schemas/RelatedRecordSummary'}}
    picks_detail['relatedItineraries'] = {'type': 'array', 'items': {'$ref': '#/components/schemas/RelatedRecordSummary'}}
    picks_detail['relatedComparisons'] = {'type': 'array', 'items': {'$ref': '#/components/schemas/RelatedRecordSummary'}}

    itin_summary = schemas.setdefault('ItinerarySummary', {}).setdefault('properties', {})
    itin_summary['destinationSlug'] = {'type': 'string'}

    itin_detail = schemas.setdefault('ItineraryDetail', {}).setdefault('properties', {})
    itin_detail['id'] = {'type': 'string', 'example': 'itinerary:tokyo-4-days'}
    itin_detail['type'] = {'type': 'string', 'enum': ['itinerary']}
    itin_detail['updatedAt'] = {'type': 'string', 'format': 'date-time'}
    itin_detail['sourceUrl'] = {'type': 'string', 'format': 'uri'}
    itin_detail['tags'] = {'type': 'array', 'items': {'type': 'string'}}
    itin_detail['sourceMeta'] = {'$ref': '#/components/schemas/RecordSourceMeta'}
    itin_detail['destinationSlug'] = {'type': 'string'}
    itin_detail['editorialSummary'] = {'type': 'string'}
    itin_detail['relatedPicks'] = {'type': 'array', 'items': {'$ref': '#/components/schemas/RelatedRecordSummary'}}
    itin_detail['relatedComparisons'] = {'type': 'array', 'items': {'$ref': '#/components/schemas/RelatedRecordSummary'}}

    compare_summary = schemas.setdefault('ComparisonSummary', {}).setdefault('properties', {})
    compare_summary['destination1Slug'] = {'type': 'string'}
    compare_summary['destination2Slug'] = {'type': 'string'}
    compare_summary['destinationSlugs'] = {'type': 'array', 'items': {'type': 'string'}}

    compare_detail = schemas.setdefault('ComparisonDetail', {}).setdefault('properties', {})
    compare_detail['id'] = {'type': 'string', 'example': 'compare:kyoto-vs-osaka'}
    compare_detail['type'] = {'type': 'string', 'enum': ['compare']}
    compare_detail['updatedAt'] = {'type': 'string', 'format': 'date-time'}
    compare_detail['sourceUrl'] = {'type': 'string', 'format': 'uri'}
    compare_detail['tags'] = {'type': 'array', 'items': {'type': 'string'}}
    compare_detail['sourceMeta'] = {'$ref': '#/components/schemas/RecordSourceMeta'}
    compare_detail['destination1Slug'] = {'type': 'string'}
    compare_detail['destination2Slug'] = {'type': 'string'}
    compare_detail['destinationSlugs'] = {'type': 'array', 'items': {'type': 'string'}}
    compare_detail['editorialSummary'] = {'type': 'string'}
    compare_detail['relatedDestinations'] = {'type': 'array', 'items': {'$ref': '#/components/schemas/RelatedRecordSummary'}}
    compare_detail['relatedItineraries'] = {'type': 'array', 'items': {'$ref': '#/components/schemas/RelatedRecordSummary'}}
    compare_detail['relatedPicks'] = {'type': 'array', 'items': {'$ref': '#/components/schemas/RelatedRecordSummary'}}

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

    print("🕸️  Building cross-links and editorial enrichment...")
    build_relationships(dest_summaries, picks_summaries, itin_summaries, compare_summaries)
    print("   ✅ related records, provenance, freshness")

    print("🧭 Building normalized catalog...")
    catalog_payload = build_catalog(dest_summaries, picks_summaries, itin_summaries, compare_summaries)
    print(f"   ✅ {catalog_payload['itemCount']} entities")

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

    print("🌍 Building country facts...")
    country_count = build_country_facts()
    print(f"   ✅ {country_count} countries")

    print("🧾 Building dataset manifests...")
    manifest_ok = build_manifests()
    print("   ✅ manifest.json and country manifests" if manifest_ok else "   ⚠️ manifest generation skipped")

    print("📄 Updating API docs page...")
    build_docs_page(dest_count, picks_count, places_count, itin_count, compare_count, country_count)
    print("   ✅ api/index.html")


if __name__ == "__main__":
    main()
