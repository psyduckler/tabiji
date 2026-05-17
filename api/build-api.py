#!/usr/bin/env python3
"""
Tabiji API v1 — Static JSON API Builder

Reads tabiji data sources (destinations, itineraries, compare)
and generates static JSON files for a free REST API hosted on Cloudflare Pages.

Usage: python3 api/build-api.py
"""

import hashlib
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

# Canonical in-memory store for destination details.
# Populated by build_destinations() from destinations-full.json; read by
# detail-enrichment, build_filter(), and knowledge-chunk builders.
# Written back to destinations-full.json at end of the enrichment pass.
_DEST_DETAILS: dict = {}


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
            "tags": ["editorial"],
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
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def reset_json_dir(path):
    """Remove stale generated JSON details before rebuilding a collection."""
    path = Path(path)
    if path.is_dir():
        for fp in path.glob("*.json"):
            fp.unlink()
    path.mkdir(parents=True, exist_ok=True)


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

# Fields kept in the in-memory slim summaries used by downstream builders
# (build_catalog, build_search, build_relationships). This drops fat-bundle
# duplicates (languages/timezones) and internal refs (alertsRef/safetyRef/
# scamsRef); everything else stays so build_catalog can read freshness/
# provenance/id/schemaVersion/updatedAt for catalog payloads.
SLIM_DROP_FIELDS = {
    "languages", "timezones", "alertsRef", "safetyRef", "scamsRef",
}

# Fields written to the public catalog at /api/v1/destinations.json.
# Strict allowlist — anyone needing the full destination payload uses the
# per-slug Worker at /api/v1/destinations/<slug>.json (which serves out of
# destinations-full.json). Excludes redundant fields (type/entityType both
# == "destination"; editorialSummary == pitch; bestFor == vibes+travelStyles)
# and per-slug operational data (timezone, dialCode, drivingSide, plugType,
# tapWaterSafe, tippingCustom, visaNote) and internal provenance metadata
# (freshness, provenance, sourceMeta, schemaVersion, updatedAt).
CATALOG_KEEP_FIELDS = {
    # Identity
    "id", "slug", "name", "url",
    # Geography
    "region", "continent", "country", "countryCode", "coordinates",
    # Cultural quick-reference
    "currency", "language", "flag",
    # Catalog facets (filterable)
    "budget", "season", "vibes", "travelStyles", "tags",
    # Editorial preview
    "pitch", "photo",
    # Cross-references (populated by build_relationships)
    "relatedItineraries", "relatedComparisons", "relatedDestinations",
}


def _slim_projection(details: dict) -> list:
    """Project _DEST_DETAILS-shaped dict into sorted slim-summary list.

    Used in-memory by downstream builders. NOT what gets written to disk —
    write_slim_destinations() applies CATALOG_KEEP_FIELDS for that.
    """
    return [
        {k: v for k, v in details[slug].items() if k not in SLIM_DROP_FIELDS}
        for slug in sorted(details.keys())
    ]


def _catalog_projection(summaries: list) -> list:
    """Project enriched in-memory summaries down to public-catalog fields."""
    catalog = []
    for s in summaries:
        row = {k: v for k, v in s.items() if k in CATALOG_KEEP_FIELDS}
        slug = row.get("slug")
        if slug and not row.get("url"):
            row["url"] = f"{API_BASE_URL}/destinations/{slug}.json"
        catalog.append(row)
    return catalog


def build_destinations():
    """Load destinations-full.json as canonical source, populate _DEST_DETAILS.

    destinations-full.json is the canonical, hand-edited source of truth
    (batch photo work, dedup, etc. all target this file). Per-slug detail
    responses are served at runtime by the Cloudflare Pages Function at
    functions/api/v1/destinations/[slug].js, which reads from this bundle
    — build-api.py no longer writes per-slug JSONs.

    Populates _DEST_DETAILS (module global) for downstream readers:
    detail enrichment (relatedItineraries/Comparisons, safetyRef), build_filter(),
    and knowledge-chunk builders. Returns a slim-projected summaries list
    that build_relationships() mutates in place with related* fields.
    The on-disk slim destinations.json is written later by the main build
    flow after those mutations land (see write_slim_destinations()).
    """
    src = OUTPUT_DIR / "destinations-full.json"
    if not src.exists():
        print("  ⚠️  destinations-full.json not found")
        return [], 0

    with open(src) as f:
        _DEST_DETAILS.clear()
        _DEST_DETAILS.update(json.load(f))

    summaries = _slim_projection(_DEST_DETAILS)
    return summaries, len(summaries)


def write_slim_destinations(summaries):
    """Write api/v1/destinations.json — the public catalog.

    Applies CATALOG_KEEP_FIELDS projection to strip the in-memory summaries
    down to fields catalog browsers actually need. Anything richer (operational
    data, provenance, full freshness blocks) is served per-slug by the Worker
    at /api/v1/destinations/<slug>.json (backed by destinations-full.json).

    Call AFTER build_relationships has mutated summaries with related* fields.
    """
    catalog = _catalog_projection(summaries)
    with open(OUTPUT_DIR / "destinations.json", 'w') as f:
        json.dump({"count": len(catalog), "destinations": catalog}, f, indent=2, ensure_ascii=False)



def extract_meta_content(soup, attr_name, attr_value):
    tag = soup.find('meta', attrs={attr_name: attr_value})
    return tag.get('content', '').strip() if tag and tag.get('content') else ''


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
    # Strip travel-package noise that frequently dangles after a destination phrase
    # ("Tokyo Itinerary" → "Tokyo", "Costa Rica Adventure" → "Costa Rica"), and a
    # leading article that the case-insensitive regex sometimes drags in
    # ("the Pacific Coast" → "Pacific Coast").
    value = re.sub(r'^(the|a|an|of)\s+', '', value, flags=re.IGNORECASE)
    # Trim at known modifier words that frequently appear AFTER the destination
    # ("Cairo After Dark" → "Cairo", "Tokyo with Tiny Explorers" → "Tokyo").
    value = re.split(r'\s+(?:After|Before|With|Without|For|Beyond|During)\s+', value, maxsplit=1, flags=re.IGNORECASE)[0]
    value = re.sub(
        r'\b('
        r'Itinerary|Guide|Adventure|Adventures|Relaxation|Foodie|Cultural|Romantic'
        r'|Family Visit|Family|Long Weekend|Escape|Escapes|Getaway|Getaways|Trip|Trips'
        r'|Travel|Tour|Tours|Vacation|Holiday|Holidays|Honeymoon|Bachelorette'
        r'|Solo Adventure|Solo|Foodie Adventure|Food Trail|Food Crawl'
        r')\b',
        '', value, flags=re.IGNORECASE,
    ).strip(' :-—()')
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


# Caps phrase used by the fallback patterns: 1-3 capitalized words. Case-sensitive
# on purpose — the inner letter classes must NOT match lowercase, otherwise
# IGNORECASE on the surrounding pattern would extend captures into arbitrary
# lowercase text ("from Madrid to Mallorca" → "Madrid to Mallorca").
_FALLBACK_CAPS = r'[A-Z][A-Za-zÀ-ÿ]+(?:[\s/&·\-][A-Z][A-Za-zÀ-ÿ]+){0,2}'


def _fallback_destination_candidates(title):
    """Secondary extraction patterns, only used when the primary set is empty.

    Adds:
      - Case-insensitive prepositions (catches "Through Tokyo" as well as "through Tokyo").
      - Leading caps phrase ending at a lowercase connector ("Tokyo with Tiny Explorers").
      - First chunk before an arrow/em-dash separator ("Tokyo → Hakone → Kyoto").
      - First caps phrase after the first colon ("Two Worlds, One Journey: Sri Lanka & ...").

    Kept separate from extract_destination_candidates so we don't regress titles
    that already extract correctly with the original two patterns. Only kicks
    in for the ~95 itineraries the original patterns leave with destination=''.
    """
    if not title:
        return []
    candidates = []
    # Strip a leading "N-Day / N-Night" prefix so the destination is the next phrase.
    body = re.sub(r'^\s*\d+\s*[-–]?\s*(?:day|days|night|nights)\b\s*[:—-]?\s*', '', title, flags=re.IGNORECASE)

    # Case-insensitive preposition (scoped flag keeps the capture case-sensitive).
    for m in re.finditer(rf'\b(?i:in|through|across|around|from|to|on)\s+({_FALLBACK_CAPS})', title):
        c = clean_itinerary_destination(m.group(1))
        if c:
            candidates.append(c)

    # Leading caps phrase ending at a lowercase word.
    m = re.match(rf'^({_FALLBACK_CAPS})\b', body)
    if m:
        c = clean_itinerary_destination(m.group(1))
        if c:
            candidates.append(c)

    # First chunk before an arrow / em-dash / en-dash / middot separator.
    parts = re.split(r'\s*[—–→·]\s*', body)
    if len(parts) > 1:
        head = parts[0].strip()
        m = re.match(rf'^({_FALLBACK_CAPS})\b', head)
        if m:
            c = clean_itinerary_destination(m.group(1))
            if c:
                candidates.append(c)

    # After the first colon ("Two Worlds, One Journey: Sri Lanka & the Maldives").
    if ':' in body:
        rest = body.split(':', 1)[1].strip()
        m = re.match(rf'^({_FALLBACK_CAPS})\b', rest)
        if m:
            c = clean_itinerary_destination(m.group(1))
            if c:
                candidates.append(c)

    return unique_list(candidates)


# Words that can appear inside a caps run but never identify a destination on
# their own. If a candidate's tokens are all bad, we drop it. Tunable list:
# add words sparingly — overzealous filtering excludes real city/country names.
_BAD_DEST_TOKENS = {
    'solo', 'adventure', 'relaxation', 'trip', 'days', 'nights', 'foodie',
    'cultural', 'budget', 'family', 'guide', 'itinerary', 'full', 'bloom',
    'through', 'under', 'big', 'with', 'after', 'before',
    'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
    'one', 'worlds', 'journey', 'wisteria', 'romantic',
}


def _candidate_passes_token_filter(candidate):
    words = [w.lower() for w in re.split(r'\s+', candidate) if w]
    if not words:
        return False
    if all(word in _BAD_DEST_TOKENS for word in words):
        return False
    if len(words) == 1 and words[0] in _BAD_DEST_TOKENS:
        return False
    return True


def choose_itinerary_destination(title, slug):
    # Primary patterns — preserve existing extraction so previously-correct
    # destinations don't churn.
    for candidate in extract_destination_candidates(title):
        if _candidate_passes_token_filter(candidate):
            return candidate
    # Fallback patterns — only used when the primary set yields nothing usable.
    # This is what closes the 95 itineraries with destination="" from the audit.
    for candidate in _fallback_destination_candidates(title):
        if _candidate_passes_token_filter(candidate):
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
    url = f"{SITE_URL}/i/{slug}/"

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
    reset_json_dir(output_itin_dir)

    summaries = []
    all_itineraries = []
    src_path = BASE_DIR / "i"
    if src_path.exists():
        slugs = sorted([d for d in os.listdir(src_path) if (src_path / d / "index.html").exists()])
        for slug in slugs:
            result = parse_itinerary_page(src_path / slug / "index.html", slug, "i")
            if result:
                title = (result.get("title") or "").strip().lower()
                # Do not publish placeholder/broken itinerary records into API artifacts.
                if title and "undefined" not in title:
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

    # Per-file /api/v1/compare/<slug>.json endpoints removed (2026-04-20) to
    # stay under Cloudflare Pages 20,000-file deployment cap. Canonical compare
    # detail lives at HTML /compare/<slug>/ and is also included in the
    # aggregate /api/v1/compare.json index below.
    output_compare_dir = None

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

        # Per-file compare JSON removed — see note at top of build_compare().
        # if output_compare_dir is not None:
        #     with open(output_compare_dir / f"{slug}.json", 'w') as f:
        #         json.dump(detail, f, indent=2, ensure_ascii=False)

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


def build_relationships(dest_summaries, itin_summaries, compare_summaries):
    destination_lookup = {}
    destination_slug_by_name = {}
    for dest in dest_summaries:
        destination_lookup[dest["slug"]] = dest
        destination_slug_by_name[normalize_name_key(dest.get("name", ""))] = dest["slug"]

    # Build cross-ref lookups for safety/alerts/scams
    safety_data_dir = BASE_DIR / "app" / "data" / "safety"
    scam_data_dir = OUTPUT_DIR / "scams"
    _safety_iso2s = set()
    if safety_data_dir.exists():
        _safety_iso2s = {f.stem.upper() for f in safety_data_dir.glob("*.json")}
    _alert_iso2s = set()
    _alerts_api_dir = OUTPUT_DIR / "alerts"
    if _alerts_api_dir.exists():
        _alert_iso2s = {f.stem.upper() for f in _alerts_api_dir.glob("*.json")}
    _scams_by_country = {}
    if scam_data_dir.exists():
        for _scam_path in scam_data_dir.glob("*.json"):
            try:
                _scam_info = json.loads(_scam_path.read_text(encoding="utf-8"))
                _cc = _scam_info.get("countryCode", "")
                if _cc:
                    _scams_by_country.setdefault(_cc, []).append(_scam_path.stem)
            except (json.JSONDecodeError, OSError):
                continue

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

    for dest in dest_summaries:
        slug = dest["slug"]
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

        detail = _DEST_DETAILS.get(slug)
        if detail:
            detail["editorialSummary"] = detail.get("editorialSummary") or detail.get("pitch", "")
            detail["bestFor"] = detail.get("bestFor") or unique_list([*(detail.get("vibes", []) or []), *(detail.get("travelStyles", []) or [])])[:6]
            detail["relatedItineraries"] = truncate_list(related_itins)
            detail["relatedComparisons"] = truncate_list(related_compares)
            detail["relatedDestinations"] = truncate_list(nearby_destinations)

            _dest_cc = detail.get("countryCode", "")
            if _dest_cc:
                _dest_cc_upper = _dest_cc.upper()
                _dest_cc_lower = _dest_cc.lower()
                if _dest_cc_upper in _safety_iso2s:
                    detail["safetyRef"] = f"{API_BASE_URL}/safety/{_dest_cc_lower}.json"
                elif "safetyRef" in detail:
                    del detail["safetyRef"]
                if _dest_cc_upper in _alert_iso2s:
                    detail["alertsRef"] = f"{API_BASE_URL}/alerts/{_dest_cc_lower}.json"
                elif "alertsRef" in detail:
                    del detail["alertsRef"]
                _dest_scam_slugs = _scams_by_country.get(_dest_cc_upper, [])
                if _dest_scam_slugs:
                    detail["scamsRef"] = [f"{API_BASE_URL}/scams/{s}.json" for s in sorted(_dest_scam_slugs)]
                elif "scamsRef" in detail:
                    del detail["scamsRef"]

        dest["relatedItineraries"] = truncate_list(related_itins)
        dest["relatedComparisons"] = truncate_list(related_compares)
        dest["relatedDestinations"] = truncate_list(nearby_destinations)

    for itin in itin_summaries:
        slug = itin["slug"]
        destination_slug = itin.get("destinationSlug", "")
        detail_path = OUTPUT_DIR / "itineraries" / f"{slug}.json"
        detail = load_json_if_exists(detail_path)
        if detail:
            detail.update(itin_detail_updates.get(slug, {}))
            detail["editorialSummary"] = detail.get("editorialSummary") or detail.get("description", "")
            detail["relatedComparisons"] = truncate_list([
                make_related_summary(item_type="comparison", slug=compare["slug"], title=compare["title"], url=compare["url"])
                for compare in compares_by_destination.get(destination_slug, [])
            ]) if destination_slug else []
            write_json(detail_path, detail)

    write_slim_destinations(_slim_projection(_DEST_DETAILS))
    with open(OUTPUT_DIR / "destinations-full.json", "w") as _full_f:
        json.dump(_DEST_DETAILS, _full_f, separators=(",", ":"), ensure_ascii=False)
    write_json(OUTPUT_DIR / "itineraries.json", {"count": len(itin_summaries), "itineraries": itin_summaries})
    write_json(OUTPUT_DIR / "compare.json", {"count": len(compare_summaries), "comparisons": compare_summaries})


def build_search(dest_summaries, itin_summaries, compare_summaries,
                 country_items=None, safety_items=None, alert_items=None,
                 scam_items=None):
    records = []
    for d in dest_summaries:
        records.append(build_search_item(
            item_type="destination", slug=d["slug"], title=d["name"], subtitle=d.get("pitch", ""),
            url=f"{API_BASE_URL}/destinations/{d['slug']}.json", site_url=d.get("sourceUrl", ""),
            tags=d.get("tags", []), extra={"region": d.get("region", ""), "continent": d.get("continent", "")}
        ))
    for i in itin_summaries:
        records.append(build_search_item(
            item_type="itinerary", slug=i["slug"], title=i["title"], subtitle=i.get("duration", ""),
            url=f"{API_BASE_URL}/itineraries/{i['slug']}.json", site_url=i["url"], tags=i.get("tags", []), extra={"destination": i.get("destination", "")}
        ))
    for c in compare_summaries:
        records.append(build_search_item(
            # url points to HTML canonical page (per-file /api/v1/compare/<slug>.json endpoints removed 2026-04-20)
            item_type="compare", slug=c["slug"], title=c["title"], subtitle=f"{c.get('destination1', '')} vs {c.get('destination2', '')}".strip(),
            url=c["url"], site_url=c["url"], tags=c.get("tags", []),
            extra={"destination1": c.get("destination1", ""), "destination2": c.get("destination2", "")}
        ))

    # New entity types
    for ct in (country_items or []):
        records.append(build_search_item(
            item_type="country", slug=ct.get("slug", ""), title=ct.get("name", ""),
            subtitle=ct.get("region", ""),
            url=ct.get("url", f"{API_BASE_URL}/countries/{ct.get('slug','')}.json"),
            site_url=f"{SITE_URL}/countries/{ct.get('slug','')}/",
            tags=[ct.get("iso2","").lower(), ct.get("region","").lower()],
            extra={"iso2": ct.get("iso2",""), "capital": ct.get("capital","")}
        ))
    for sf in (safety_items or []):
        records.append(build_search_item(
            item_type="safety", slug=sf.get("slug", sf.get("iso2","").lower()),
            title=sf.get("name", ""), subtitle=sf.get("advisoryLevelText", ""),
            url=sf.get("url", f"{API_BASE_URL}/safety/{sf.get('iso2','').lower()}.json"),
            site_url=f"{SITE_URL}/safety/{sf.get('iso2','').lower()}/",
            tags=[sf.get("iso2","").lower(), "safety"],
        ))
    for al in (alert_items or []):
        records.append(build_search_item(
            item_type="alert", slug=al.get("slug", al.get("iso2","").lower()),
            title=al.get("name", ""), subtitle=al.get("combinedLevel", "") or "",
            url=al.get("url", f"{API_BASE_URL}/alerts/{al.get('iso2','').lower()}.json"),
            site_url=f"{SITE_URL}/alerts/{al.get('iso2','').lower()}/",
            tags=[al.get("iso2","").lower(), "alert"],
        ))
    for sc in (scam_items or []):
        records.append(build_search_item(
            item_type="scam", slug=sc.get("slug", ""),
            title=f"{sc.get('city','')} Scams" if sc.get("city") else sc.get("name",""),
            subtitle=sc.get("country", ""),
            url=sc.get("url", f"{API_BASE_URL}/scams/{sc.get('slug','')}.json"),
            site_url=f"{SITE_URL}/scams/{sc.get('slug','')}/",
            tags=[sc.get("countryCode","").lower(), sc.get("city","").lower(), "scam"],
        ))

    type_counts = {
        "destination": len(dest_summaries),
        "itinerary": len(itin_summaries),
        "compare": len(compare_summaries),
        "country": len(country_items or []),
        "safety": len(safety_items or []),
        "alert": len(alert_items or []),
        "scam": len(scam_items or []),
    }
    payload = {
        "count": len(records),
        "types": {k: v for k, v in type_counts.items() if v > 0},
        "items": records,
    }
    with open(OUTPUT_DIR / "search-index.json", 'w') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return payload


CATALOG_MAX_CHUNK_BYTES = 10 * 1024 * 1024  # 10 MB item budget (wrapper overhead brings actual file to ~12 MB)


def _write_catalog_chunks(items, generated_at):
    """Write chunked catalog files and per-type shard files. Returns (chunks_written, shard_names)."""
    catalog_dir = OUTPUT_DIR / "catalog"
    catalog_dir.mkdir(parents=True, exist_ok=True)

    # --- Per-type shard files ---
    items_by_type = {}
    for item in items:
        et = item.get("entityType", "unknown")
        items_by_type.setdefault(et, []).append(item)

    shard_names = []
    type_to_shard = {
        "destination": "destinations",
        "itinerary": "itineraries",
        "compare": "comparisons",
        "country": "countries",
        "safety": "safety",
        "alert": "alerts",
        "scam": "scams",
    }
    for entity_type, shard_file in type_to_shard.items():
        type_items = items_by_type.get(entity_type, [])
        if not type_items:
            continue
        shard_payload = {
            "version": API_VERSION,
            "schemaVersion": API_SCHEMA_VERSION,
            "generatedAt": generated_at,
            "entityType": entity_type,
            "itemCount": len(type_items),
            "items": type_items,
        }
        write_json(catalog_dir / f"{shard_file}.json", shard_payload)
        shard_names.append(shard_file)

    # --- Numbered chunk files (max 12MB each) ---
    # Use indent=2 size estimate since write_json uses indent=2
    chunks = []
    current_chunk = []
    current_size = 0
    for item in items:
        item_bytes = len(json.dumps(item, indent=2, ensure_ascii=False).encode("utf-8"))
        if current_chunk and (current_size + item_bytes) > CATALOG_MAX_CHUNK_BYTES:
            chunks.append(current_chunk)
            current_chunk = []
            current_size = 0
        current_chunk.append(item)
        current_size += item_bytes
    if current_chunk:
        chunks.append(current_chunk)

    total_chunks = len(chunks)
    for i, chunk_items in enumerate(chunks, 1):
        chunk_payload = {
            "version": API_VERSION,
            "schemaVersion": API_SCHEMA_VERSION,
            "generatedAt": generated_at,
            "chunk": i,
            "totalChunks": total_chunks,
            "itemCount": len(chunk_items),
            "items": chunk_items,
        }
        write_json(catalog_dir / f"{i}.json", chunk_payload)

    return total_chunks, shard_names


def build_catalog(dest_summaries, itin_summaries, compare_summaries,
                  country_items=None, safety_items=None, alert_items=None,
                  scam_items=None):
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    items = []

    for dest in dest_summaries:
        # A small number of legacy destination records (e.g. `arches`) lack the
        # `id` / `entityType` fields that newer builds add; fall back to slug so
        # build_catalog doesn't abort when it hits them.
        dest_id = dest.get("id") or f"destination:{dest.get('slug', 'unknown')}"
        items.append({
            "id": dest_id,
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
            "url": compare.get("url", f"{SITE_URL}/compare/{compare['slug']}/"),
            "freshness": compare.get("freshness", make_freshness(compare.get("updatedAt", generated_at))),
            "provenance": compare.get("provenance", {}),
        })

    # --- New entity types from index files ---
    for country in (country_items or _load_index_items("countries.json", "countries")):
        iso2 = country.get("iso2", "")
        items.append({
            "id": f"country:{iso2.lower()}",
            "entityType": "country",
            "schemaVersion": API_SCHEMA_VERSION,
            "source": "countries",
            "slug": iso2.lower(),
            "name": country.get("name", ""),
            "iso2": country.get("iso2", ""),
            "iso3": country.get("iso3", ""),
            "capital": country.get("capital", ""),
            "region": country.get("region", ""),
            "subregion": country.get("subregion", ""),
            "tags": unique_list([iso2.lower(), country.get("region","").lower(), country.get("subregion","").lower()]),
            "url": f"{API_BASE_URL}/countries/{iso2.lower()}.json",
            "freshness": make_freshness(generated_at),
            "provenance": {"sources": ["countries"], "lastVerifiedAt": generated_at},
        })

    for profile in (safety_items or _load_index_items("safety.json", "profiles")):
        iso2 = profile.get("iso2", "")
        items.append({
            "id": profile.get("id", f"safety:{iso2.lower()}"),
            "entityType": "safety",
            "schemaVersion": API_SCHEMA_VERSION,
            "source": "safety",
            "slug": iso2.lower(),
            "name": profile.get("name", ""),
            "iso2": iso2,
            "advisoryLevel": profile.get("advisoryLevel"),
            "advisoryLevelText": profile.get("advisoryLevelText", ""),
            "tags": unique_list([iso2.lower(), "safety"]),
            "url": profile.get("url", f"{API_BASE_URL}/safety/{iso2.lower()}.json"),
            "freshness": make_freshness(generated_at),
            "provenance": {"sources": ["safety"], "lastVerifiedAt": generated_at},
        })

    for alert in (alert_items or _load_index_items("alerts.json", "alerts")):
        iso2 = alert.get("iso2", "")
        items.append({
            "id": alert.get("id", f"alerts:{iso2.lower()}"),
            "entityType": "alert",
            "schemaVersion": API_SCHEMA_VERSION,
            "source": "alerts",
            "slug": iso2.lower(),
            "name": alert.get("name", ""),
            "iso2": iso2,
            "combinedLevel": alert.get("combinedLevel"),
            "usLevel": alert.get("usLevel"),
            "tags": unique_list([iso2.lower(), "alert", str(alert.get("combinedLevel",""))]),
            "url": alert.get("url", f"{API_BASE_URL}/alerts/{iso2.lower()}.json"),
            "freshness": make_freshness(generated_at),
            "provenance": {"sources": ["alerts"], "lastVerifiedAt": generated_at},
        })

    for city in (scam_items or _load_index_items("scams.json", "items")):
        slug = city.get("slug", "")
        items.append({
            "id": city.get("id", f"scam:{slug}"),
            "entityType": "scam",
            "schemaVersion": API_SCHEMA_VERSION,
            "source": "scams",
            "slug": city.get("slug", ""),
            "name": f"{city.get('city','')} Scams",
            "city": city.get("city", ""),
            "country": city.get("country", ""),
            "countryCode": city.get("countryCode", ""),
            "scamCount": city.get("scamCount", 0),
            "tags": unique_list([city.get("countryCode","").lower(), city.get("city","").lower(), "scam"]),
            "url": city.get("url", f"{API_BASE_URL}/scams/{slug}.json"),
            "freshness": make_freshness(generated_at),
            "provenance": {"sources": ["scams"], "lastVerifiedAt": generated_at},
        })

    # --- Write chunked output ---
    total_chunks, shard_names = _write_catalog_chunks(items, generated_at)

    # Write catalog.json as lightweight index pointing to chunks
    chunk_urls = [f"/api/v1/catalog/{i}.json" for i in range(1, total_chunks + 1)]
    catalog_index = {
        "version": API_VERSION,
        "schemaVersion": API_SCHEMA_VERSION,
        "generatedAt": generated_at,
        "itemCount": len(items),
        "chunks": total_chunks,
        "chunkUrls": chunk_urls,
        "shards": {name: f"/api/v1/catalog/{name}.json" for name in shard_names},
    }
    write_json(OUTPUT_DIR / "catalog.json", catalog_index)
    return {"itemCount": len(items), "chunks": total_chunks, "shards": shard_names}


# ============================================================
# SAFETY
# ============================================================

def build_safety():
    """Build /api/v1/safety.json index and /api/v1/safety/{iso2}.json detail files."""
    safety_data_dir = BASE_DIR / "app" / "data" / "safety"
    if not safety_data_dir.exists():
        return 0

    safety_profiles = []
    out_dir = OUTPUT_DIR / "safety"
    out_dir.mkdir(parents=True, exist_ok=True)

    for profile_path in sorted(safety_data_dir.glob("*.json")):
        try:
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue

        iso2 = profile.get("iso2", "")
        if not iso2:
            continue

        # Write individual safety detail file
        out_file = out_dir / f"{iso2.lower()}.json"
        out_file.write_text(json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8")

        # Build summary for index
        ta = profile.get("travelAdvisory") or {}
        safety_profiles.append({
            "id": profile.get("id"),
            "iso2": iso2,
            "name": profile.get("name"),
            "lastUpdated": profile.get("lastUpdated"),
            "advisoryLevel": ta.get("level"),
            "advisoryLevelText": ta.get("levelText"),
            "url": f"{API_BASE_URL}/safety/{iso2.lower()}.json",
        })

    index = {
        "count": len(safety_profiles),
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "profiles": safety_profiles,
    }
    (OUTPUT_DIR / "safety.json").write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    return len(safety_profiles)


# ============================================================
# ALERTS
# ============================================================

_COMBINED_LEVEL_MAP = {1: "low", 2: "moderate", 3: "high", 4: "extreme"}

# US State Dept uses FIPS 10-4 codes; tabiji uses ISO 3166-1 alpha-2.
# This map normalizes non-standard keys before writing files.
_FIPS_TO_ISO = {
    "AV": "AI",   # Anguilla
    "AY": "AQ",   # Antarctica
    "CJ": "KY",   # Cayman Islands
    "KV": "XK",   # Kosovo
    "NN": "SX",   # Sint Maarten
    "UC": "CW",   # Cura\u00e7ao
    "A1": None,    # Saba \u2014 no standalone ISO alpha-2 (part of BQ)
    "A2": "GF",   # French Guiana
    "A3": None,    # French West Indies \u2014 no single ISO code (GP/MQ)
    # Full-name keys from US data
    "Hong Kong": "HK",
    "Macau": "MO",
}


def build_alerts():
    """Build /api/v1/alerts.json index and /api/v1/alerts/{iso2}.json detail files."""
    us_path = BASE_DIR / "app" / "data" / "advisories-us.json"
    uk_path = BASE_DIR / "app" / "data" / "advisories-uk.json"

    if not us_path.exists() and not uk_path.exists():
        return 0

    us_raw = {}
    if us_path.exists():
        try:
            us_raw = json.loads(us_path.read_text(encoding="utf-8")).get("advisories", {})
        except (json.JSONDecodeError, OSError):
            pass

    # Normalize US advisory keys: FIPS->ISO, full names->ISO, skip unmappable
    us_advisories = {}
    for raw_key, entry in us_raw.items():
        if raw_key in _FIPS_TO_ISO:
            mapped = _FIPS_TO_ISO[raw_key]
            if mapped is None:
                continue  # Skip entries with no valid ISO code (Saba, French West Indies)
            iso2 = mapped
        else:
            iso2 = raw_key
        # Merge duplicates (e.g. HK appears as both "HK" and "Hong Kong"):
        # keep the entry with a non-None level, or the first one
        if iso2 in us_advisories:
            existing = us_advisories[iso2]
            if existing.get("level") is None and entry.get("level") is not None:
                us_advisories[iso2] = entry
        else:
            us_advisories[iso2] = entry

    uk_raw_data = {}
    if uk_path.exists():
        try:
            uk_raw_data = json.loads(uk_path.read_text(encoding="utf-8")).get("advisories", {})
        except (json.JSONDecodeError, OSError):
            pass

    # Build UK lookup by iso2 and by slug
    uk_by_iso2 = {}
    uk_by_slug = {}
    for _key, entry in uk_raw_data.items():
        iso2 = entry.get("iso2")
        slug = entry.get("slug")
        if iso2:
            uk_by_iso2[iso2] = entry
        if slug:
            uk_by_slug[slug] = entry

    # Load country names from countries.json for enrichment
    country_names = {}
    countries_path = OUTPUT_DIR / "countries.json"
    if countries_path.exists():
        try:
            cdata = json.loads(countries_path.read_text(encoding="utf-8"))
            for c in cdata.get("countries", []):
                if c.get("iso2"):
                    country_names[c["iso2"]] = c.get("name", c["iso2"])
        except (json.JSONDecodeError, OSError):
            pass

    # Collect all iso2 codes that have US or UK data
    all_iso2 = set(us_advisories.keys()) | set(uk_by_iso2.keys())

    out_dir = OUTPUT_DIR / "alerts"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Clean previous alert files to avoid stale entries from renamed/removed codes
    for old_file in out_dir.glob("*.json"):
        old_file.unlink()

    alert_summaries = []

    for iso2 in sorted(all_iso2):
        us_adv = us_advisories.get(iso2)
        uk_adv = uk_by_iso2.get(iso2)

        def _clean_country_name(raw):
            if not raw:
                return ""
            return re.sub(r"\s+travel\s+advi\w+", "", raw, flags=re.IGNORECASE).strip()

        name = (
            country_names.get(iso2)
            or _clean_country_name(us_adv and us_adv.get("country"))
            or _clean_country_name(uk_adv and uk_adv.get("country", ""))
            or iso2
        )

        # US section
        if us_adv:
            us_level = us_adv.get("level")
            us_section = {
                "level": us_level,
                "levelText": us_adv.get("levelText"),
                "summary": us_adv.get("summary"),
                "dateIssued": us_adv.get("publishedDate"),
                "url": us_adv.get("url"),
                "regions": [],
            }
        else:
            us_level = None
            us_section = None

        # UK section
        if uk_adv:
            uk_section = {
                "summary": uk_adv.get("summary") or None,
                "dateIssued": uk_adv.get("lastUpdated"),
                "url": uk_adv.get("url"),
                "entryRequirements": None,
                "healthNotes": None,
                "safetyWarnings": [],
            }
        else:
            uk_section = None

        # Combined level: prefer US level, fall back to UK-derived level
        combined_level = _COMBINED_LEVEL_MAP.get(us_level) if us_level else None
        if combined_level is None and uk_adv:
            # UK FCDO doesn't use numbered levels, so default to "unknown"
            # rather than leaving null -- lets consumers know data exists
            combined_level = "unknown"
        if combined_level == "low":
            combined_summary = f"Normal precautions apply for {name}."
        elif combined_level == "moderate":
            combined_summary = f"Exercise increased caution in {name}."
        elif combined_level == "high":
            combined_summary = f"Reconsider travel to {name}."
        elif combined_level == "extreme":
            combined_summary = f"Do not travel to {name}."
        elif combined_level == "unknown":
            combined_summary = f"UK FCDO advisory available for {name}. No US State Dept level assigned."
        else:
            combined_summary = None

        detail = {
            "id": f"alerts:{iso2.lower()}",
            "iso2": iso2,
            "name": name,
            "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "combinedLevel": combined_level,
            "combinedSummary": combined_summary,
        }
        if us_section:
            detail["us"] = us_section
        if uk_section:
            detail["uk"] = uk_section

        out_file = out_dir / f"{iso2.lower()}.json"
        out_file.write_text(json.dumps(detail, indent=2, ensure_ascii=False), encoding="utf-8")

        alert_summaries.append({
            "id": detail["id"],
            "iso2": iso2,
            "name": name,
            "combinedLevel": combined_level,
            "usLevel": us_level,
            "url": f"{API_BASE_URL}/alerts/{iso2.lower()}.json",
        })

    index = {
        "count": len(alert_summaries),
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "alerts": alert_summaries,
    }
    (OUTPUT_DIR / "alerts.json").write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    return len(alert_summaries)


# ============================================================
# INDEX
# ============================================================

def build_index(dest_count, itin_count, compare_count, search_count,
                safety_count=0, alerts_count=0, country_count=0, scam_count=0):
    index = {
        "name": "tabiji.ai API",
        "version": API_VERSION,
        "description": "Free REST API for AI-curated travel data — destinations, itineraries, comparisons, a normalized catalog, and unified search. No API key required.",
        "baseUrl": API_BASE_URL,
        "documentation": f"{SITE_URL}/api/",
        "openapi": f"{SITE_URL}/api/openapi.json",
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stats": {
            "destinations": dest_count,
            "itineraries": itin_count,
            "comparisons": compare_count,
            "searchDocuments": search_count,
            "safetyProfiles": safety_count,
            "alertCountries": alerts_count,
            "countries": country_count,
            "scamCities": scam_count,
        },
        "endpoints": [
            {"path": "/destinations.json", "description": f"All {dest_count} destinations with budget, season, vibes, and travel styles", "method": "GET"},
            {"path": "/destinations/{slug}.json", "description": "Single destination detail", "method": "GET"},
            {"path": "/itineraries.json", "description": f"All {itin_count} day-by-day travel itineraries", "method": "GET"},
            {"path": "/itineraries/{slug}.json", "description": "Full itinerary with day-by-day activities", "method": "GET"},
            {"path": "/compare.json", "description": f"All {compare_count} head-to-head destination comparisons", "method": "GET"},
            {"path": "/countries.json", "description": f"All {country_count} country facts", "method": "GET"},
            {"path": "/safety.json", "description": f"All {safety_count} country safety profiles", "method": "GET"},
            {"path": "/alerts.json", "description": f"All {alerts_count} country travel alerts", "method": "GET"},
            {"path": "/scams.json", "description": f"All {scam_count} scam city guides", "method": "GET"},
            {"path": "/search.json", "description": f"Unified search across {search_count} documents", "method": "GET"},
            {"path": "/catalog.json", "description": "Normalized catalog chunk index", "method": "GET"},
            {"path": "/manifest.json", "description": "Machine-readable file manifest", "method": "GET"},
        ],
        "license": "CC BY 4.0",
        "attribution": "Data provided by tabiji.ai — include link to https://tabiji.ai when using.",
    }
    write_json(OUTPUT_DIR / "index.json", index)


def build_llms_txt(dest_count, itin_count, compare_count):
    content = f'''# tabiji.ai

> Free AI-curated travel data API — destination guides, day-by-day itineraries, comparisons, country facts, alerts, scam guides, and unified search for {dest_count} destinations. No API key required.

## API Documentation
- [API Docs](https://tabiji.ai/api/): Full endpoint documentation with examples
- [OpenAPI Spec](https://tabiji.ai/api/openapi.json): Machine-readable API specification (OpenAPI 3.1)
- [agents.json](https://tabiji.ai/.well-known/agents.json): AI agent workflow definitions

## Endpoints

### Destinations
- [All Destinations](https://tabiji.ai/api/v1/destinations.json): {dest_count} destinations with budget, season, vibes, travel styles, and pitch
- [Single Destination](https://tabiji.ai/api/v1/destinations/{{slug}}.json): Full details for one destination (e.g., `tokyo.json`, `paris.json`)

### Itineraries
- [All Itineraries](https://tabiji.ai/api/v1/itineraries.json): {itin_count} day-by-day travel itineraries
- [Single Itinerary](https://tabiji.ai/api/v1/itineraries/{{slug}}.json): Full itinerary with day-by-day activities, times, tips, and logistics

### Comparisons
- [All Comparisons](https://tabiji.ai/api/v1/compare.json): {compare_count} head-to-head destination comparisons, each linking to its canonical HTML page
- Single Comparison (HTML canonical): `https://tabiji.ai/compare/{{slug}}/` — full comparison with categories, verdict, and FAQs.

### Search & Catalog
- [Search](https://tabiji.ai/api/v1/search.json?q=tokyo): Unified search across all public API data
- [Catalog](https://tabiji.ai/api/v1/catalog.json): Normalized catalog chunk index for agents
- [Manifest](https://tabiji.ai/api/v1/manifest.json): Machine-readable file manifest

## Usage
All endpoints are public JSON. No API key required. Please attribute tabiji.ai when using the data.

## Contact
- Website: https://tabiji.ai
- Email: hello@tabiji.ai
'''
    (BASE_DIR / 'llms.txt').write_text(content, encoding='utf-8')


def build_agents_json(dest_count, itin_count, compare_count):
    payload = {
        "$schema": "https://specs.openagents.com/agents-json/0.1/schema.json",
        "version": "0.1",
        "name": "tabiji.ai Travel API",
        "description": f"Free AI-curated travel data — day-by-day itineraries, destination guides, destination comparisons, country facts, alerts, scam guides, and unified search for {dest_count}+ destinations worldwide. No API key required.",
        "url": "https://tabiji.ai",
        "logo": "https://img.tabiji.ai/owl-logo.png",
        "contactEmail": "hello@tabiji.ai",
        "openapi": "https://tabiji.ai/api/openapi.json",
        "capabilities": {"streaming": False, "pushNotifications": False, "stateTransitionHistory": False},
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
        "skills": [
            {
                "id": "research-destination",
                "name": "Research a Destination",
                "description": f"Get structured destination intelligence across {dest_count} destinations: budget, best season, travel styles, safety refs, alerts, scams, and related comparisons.",
                "tags": ["destinations", "travel", "budget", "season", "safety"],
                "examples": ["What should I know before visiting Tokyo?", "Find safe beach destinations for June"],
                "inputModes": ["text"],
                "outputModes": ["text"],
                "steps": [
                    {"id": "search", "description": "Search all public travel data for relevant matches", "endpoint": {"method": "GET", "url": "https://tabiji.ai/api/v1/search.json?q={query}&type=destination"}},
                    {"id": "get-destination", "description": "Fetch a destination detail JSON", "endpoint": {"method": "GET", "url": "https://tabiji.ai/api/v1/destinations/{slug}.json"}}
                ]
            },
            {
                "id": "compare-destinations",
                "name": "Compare Destinations",
                "description": f"Compare destinations using {compare_count} head-to-head comparison pages and normalized catalog/search data.",
                "tags": ["compare", "destinations", "travel-planning"],
                "examples": ["Tokyo vs Kyoto", "Bali vs Thailand"],
                "inputModes": ["text"],
                "outputModes": ["text"],
                "steps": [
                    {"id": "search", "description": "Search comparison data", "endpoint": {"method": "GET", "url": "https://tabiji.ai/api/v1/search.json?q={query}&type=compare"}},
                    {"id": "list-comparisons", "description": "List all comparison summaries", "endpoint": {"method": "GET", "url": "https://tabiji.ai/api/v1/compare.json"}}
                ]
            },
            {
                "id": "plan-itinerary",
                "name": "Find Itineraries",
                "description": f"Find structured day-by-day itinerary examples from {itin_count} public itineraries.",
                "tags": ["itinerary", "travel-planning", "days"],
                "examples": ["Find a 5 day Japan itinerary", "Show me family-friendly Italy itineraries"],
                "inputModes": ["text"],
                "outputModes": ["text"],
                "steps": [
                    {"id": "search", "description": "Search itinerary data", "endpoint": {"method": "GET", "url": "https://tabiji.ai/api/v1/search.json?q={query}&type=itinerary"}},
                    {"id": "list-itineraries", "description": "List public itinerary summaries", "endpoint": {"method": "GET", "url": "https://tabiji.ai/api/v1/itineraries.json"}}
                ]
            }
        ],
    }
    out_path = BASE_DIR / '.well-known' / 'agents.json'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(out_path, payload)


def build_docs_page(dest_count, itin_count, compare_count, country_count=0):
    """Render api/index.html from api/index.html.template with live counts."""
    template_path = BASE_DIR / 'api' / 'index.html.template'
    html_path = BASE_DIR / 'api' / 'index.html'
    content = template_path.read_text(encoding='utf-8')

    tokens = {
        'DEST_COUNT':     (f'{dest_count:,}', str(dest_count)),
        'ITIN_COUNT':     (f'{itin_count:,}', str(itin_count)),
        'COMPARE_COUNT':  (f'{compare_count:,}', str(compare_count)),
        'COUNTRY_COUNT':  (f'{country_count:,}', str(country_count)),
    }

    for name, (formatted, raw) in tokens.items():
        content = content.replace('{{' + name + '}}', formatted)
        content = content.replace('{{' + name + '_RAW}}', raw)

    html_path.write_text(content, encoding='utf-8')
    _sync_partials_in_place(html_path)


def _sync_partials_in_place(html_path):
    """Re-run scripts/build-partials.py:process_file on a single HTML page.

    Imports the sync logic dynamically so build-api.py doesn't gain an import-time
    dependency on the partials script.
    """
    import importlib.util
    script_path = BASE_DIR / "scripts" / "build-partials.py"
    if not script_path.exists():
        return
    spec = importlib.util.spec_from_file_location("_build_partials_inline", script_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.process_file(Path(html_path), write=True)


def build_openapi(dest_count, itin_count, compare_count):
    openapi_path = BASE_DIR / 'api' / 'openapi.json'
    spec = json.loads(open(openapi_path, encoding='utf-8').read())

    spec['info']['version'] = API_VERSION
    spec['info']['description'] = (
        f"Free REST API for AI-curated travel data — {dest_count} destinations, "
        f"{itin_count} day-by-day itineraries, {compare_count} destination comparisons, "
        f"country facts, alerts, scam guides, and unified search. No API key required."
    )

    paths = spec.setdefault('paths', {})
    for path_key in list(paths.keys()):
        if 'pick' in path_key.lower():
            del paths[path_key]

    endpoint_desc_updates = {
        '/destinations.json': f"Returns all {dest_count} destinations with budget level, best season, vibes, travel styles, and a one-line pitch.",
        '/itineraries.json': f"Returns all {itin_count} day-by-day travel itineraries with summary metadata.",
        '/compare.json': f"Returns all {compare_count} head-to-head destination comparisons with summary metadata.",
    }
    for path_key, desc in endpoint_desc_updates.items():
        if path_key in paths and 'get' in paths[path_key]:
            paths[path_key]['get']['description'] = desc

    components = spec.setdefault('components', {})
    schemas = components.setdefault('schemas', {})
    for schema_key in list(schemas.keys()):
        if 'pick' in schema_key.lower():
            del schemas[schema_key]

    if 'tags' in spec:
        spec['tags'] = [tag for tag in spec['tags'] if 'pick' not in json.dumps(tag).lower()]

    write_json(openapi_path, spec)


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



# ============================================================
# FILTER & FACETS (Sprint 3)
# ============================================================

_BUDGET_TIER_MAP = {"$": "budget", "$$": "moderate", "$$$": "premium", "$$$$": "luxury"}

_MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
_MONTH_LOOKUP = {m.lower(): m for m in _MONTH_NAMES}
_MONTH_IDX = {m.lower(): i for i, m in enumerate(_MONTH_NAMES)}


def _parse_season(raw):
    """Parse season strings like 'Mar–May, Oct–Nov' or 'Year-round' into month arrays."""
    if not raw:
        return []
    raw_clean = raw.replace("\u2013", "-").replace("\u2014", "-").strip()
    if raw_clean.lower() in ("year-round", "year round", "all year"):
        return list(_MONTH_NAMES)
    months = []
    for part in raw_clean.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            pieces = [p.strip()[:3] for p in part.split("-", 1)]
            start = _MONTH_IDX.get(pieces[0].lower())
            end = _MONTH_IDX.get(pieces[1].lower()) if len(pieces) > 1 else None
            if start is not None and end is not None:
                if end >= start:
                    months.extend(_MONTH_NAMES[start:end + 1])
                else:
                    months.extend(_MONTH_NAMES[start:] + _MONTH_NAMES[:end + 1])
            elif start is not None:
                months.append(_MONTH_NAMES[start])
        else:
            m = _MONTH_LOOKUP.get(part[:3].lower())
            if m:
                months.append(m)
    seen = set()
    return [m for m in months if not (m in seen or seen.add(m))]




def build_filter():
    """Build /api/v1/filter.json — filterable destination index with normalized dimensions."""
    if not _DEST_DETAILS:
        return [], 0

    # Load safety data by iso2
    safety_by_iso2 = {}
    safety_dir = OUTPUT_DIR / "safety"
    if safety_dir.exists():
        for sp in safety_dir.glob("*.json"):
            try:
                sd = json.loads(sp.read_text(encoding="utf-8"))
                iso2 = sd.get("iso2", sp.stem.upper())
                safety_section = sd.get("safety", {})
                ta = sd.get("travelAdvisory", {})
                # Normalize soloFemaleSafety/lgbtSafety from free text to enum
                def _normalize_safety_text(text):
                    if not text or not isinstance(text, str):
                        return None
                    t = text.lower()
                    if "very safe" in t or "extremely safe" in t:
                        return "very-safe"
                    if "generally safe" in t or "safe" in t:
                        return "safe"
                    if "moderate" in t or "exercise caution" in t:
                        return "moderate"
                    if "caution" in t or "avoid" in t:
                        return "caution"
                    return None

                safety_by_iso2[iso2.upper()] = {
                    "overallRisk": safety_section.get("overallRisk"),
                    "soloFemaleSafety": _normalize_safety_text(safety_section.get("soloFemaleSafety")),
                    "lgbtSafety": _normalize_safety_text(safety_section.get("lgbtSafety")),
                    "advisoryLevel": ta.get("level"),
                }
            except (json.JSONDecodeError, OSError):
                continue

    # Load alert combinedLevel by iso2
    alert_levels = {}
    alerts_dir = OUTPUT_DIR / "alerts"
    if alerts_dir.exists():
        for ap in alerts_dir.glob("*.json"):
            try:
                ad = json.loads(ap.read_text(encoding="utf-8"))
                iso2 = ad.get("iso2", ap.stem.upper())
                alert_levels[iso2.upper()] = {
                    "combinedLevel": ad.get("combinedLevel"),
                    "advisoryLevel": ad.get("us", {}).get("level") if ad.get("us") else None,
                }
            except (json.JSONDecodeError, OSError):
                continue

    items = []
    for slug in sorted(_DEST_DETAILS.keys()):
        d = _DEST_DETAILS[slug]

        cc = (d.get("countryCode") or "").upper()
        budget_raw = d.get("budget", "")
        budget_tier = _BUDGET_TIER_MAP.get(budget_raw)

        season_raw = d.get("season", "")
        season_best = _parse_season(season_raw)

        vibes = [v.lower() for v in (d.get("vibes") or [])]
        travel_styles = [s.lower() for s in (d.get("travelStyles") or [])]

        # Safety data
        safety_data = safety_by_iso2.get(cc, {})
        alert_data = alert_levels.get(cc, {})
        safety_entry = {
            "overallRisk": safety_data.get("overallRisk"),
            "advisoryLevel": safety_data.get("advisoryLevel") or alert_data.get("advisoryLevel"),
            "combinedLevel": alert_data.get("combinedLevel"),
            "soloFemaleSafety": safety_data.get("soloFemaleSafety"),
            "lgbtSafety": safety_data.get("lgbtSafety"),
        }

        practical = {
            "tapWaterSafe": d.get("tapWaterSafe"),
            "drivingSide": d.get("drivingSide"),
            "dialCode": d.get("dialCode"),
        }

        editorial_score = (d.get("freshness") or {}).get("confidenceScore", 0.7)

        items.append({
            "slug": d.get("slug", slug),
            "name": d.get("name", ""),
            "country": d.get("country", ""),
            "countryCode": cc,
            "continent": d.get("continent", ""),
            "region": d.get("region", ""),
            "photo": d.get("photo", ""),
            "budget": {"tier": budget_tier, "raw": budget_raw} if budget_raw else None,
            "season": {"best": season_best, "raw": season_raw} if season_raw else None,
            "vibes": vibes,
            "travelStyles": travel_styles,
            "safety": safety_entry,
            "practical": practical,
            "scores": {"editorial": editorial_score},
            "url": f"{API_BASE_URL}/destinations/{d.get('slug', slug)}.json",
        })

    payload = {
        "count": len(items),
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "facetsUrl": f"{API_BASE_URL}/facets.json",
        "items": items,
    }
    write_json(OUTPUT_DIR / "filter.json", payload)
    return items, len(items)


def build_facets(filter_items):
    """Build /api/v1/facets.json — dimension value counts for UI faceted search."""
    from collections import Counter

    facet_defs = {
        "continent": lambda it: [it.get("continent")] if it.get("continent") else [],
        "budget.tier": lambda it: [it["budget"]["tier"]] if it.get("budget") and it["budget"].get("tier") else [],
        "safety.overallRisk": lambda it: [it["safety"]["overallRisk"]] if it.get("safety") and it["safety"].get("overallRisk") else [],
        "safety.advisoryLevel": lambda it: [it["safety"]["advisoryLevel"]] if it.get("safety") and it["safety"].get("advisoryLevel") is not None else [],
        "safety.soloFemaleSafety": lambda it: [it["safety"]["soloFemaleSafety"]] if it.get("safety") and it["safety"].get("soloFemaleSafety") else [],
        "vibes": lambda it: it.get("vibes", []),
        "practical.tapWaterSafe": lambda it: [it["practical"]["tapWaterSafe"]] if it.get("practical") and it["practical"].get("tapWaterSafe") is not None else [],
    }

    facets = {}
    for facet_name, extractor in facet_defs.items():
        counter = Counter()
        for item in filter_items:
            for val in extractor(item):
                counter[val] += 1
        values = [{"value": v, "count": c} for v, c in counter.most_common()]
        if values:
            facets[facet_name] = {"values": values}

    payload = {
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "facets": facets,
    }
    write_json(OUTPUT_DIR / "facets.json", payload)





def _sha256_file(path):
    """Return sha256 hex digest of a file's contents."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _dir_size(directory):
    """Return total byte size of all .json files in a directory."""
    total = 0
    p = Path(directory)
    if p.is_dir():
        for fp in p.rglob("*.json"):
            total += fp.stat().st_size
    return total


def build_manifest():
    """Scan all api/v1/ collections and emit manifest.json with counts, sizes, checksums."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    collections_def = [
        ("destinations",  "/api/v1/destinations.json",   "/api/v1/destinations/{slug}.json"),
        ("countries",     "/api/v1/countries.json",       "/api/v1/countries/{iso2}.json"),
        # compare per-slug JSON retired 2026-04-20 (Cloudflare Pages 20k file cap). Canonical detail lives at HTML URLs; see htmlPattern.
        ("itineraries",   "/api/v1/itineraries.json",     "/api/v1/itineraries/{slug}.json"),
        ("compare",       "/api/v1/compare.json",         None),
        ("safety",        "/api/v1/safety.json",          "/api/v1/safety/{iso2}.json"),
        ("alerts",        "/api/v1/alerts.json",          "/api/v1/alerts/{iso2}.json"),
        ("scams",         "/api/v1/scams.json",           "/api/v1/scams/{slug}.json"),
        ("filter",        "/api/v1/filter.json",          None),
        ("facets",        "/api/v1/facets.json",          None),
    ]

    collections = {}
    total_bytes = 0

    for col_name, index_url, detail_pattern in collections_def:
        index_path = OUTPUT_DIR / f"{col_name}.json"
        if not index_path.exists():
            continue

        # Count from index file
        try:
            with open(index_path) as f:
                index_data = json.load(f)
            count = index_data.get("count", 0)
            if count == 0:
                # Try common count keys
                for key in ("itemCount", "totalCount"):
                    if key in index_data:
                        count = index_data[key]
                        break
        except Exception:
            count = 0

        index_size = index_path.stat().st_size
        detail_dir = OUTPUT_DIR / col_name
        detail_size = _dir_size(detail_dir)
        size_bytes = index_size + detail_size
        total_bytes += size_bytes
        checksum = _sha256_file(index_path)
        updated_at = isoformat_mtime(index_path)

        entry = {
            "count": count,
            "indexUrl": index_url,
            "sizeBytes": size_bytes,
            "checksum": f"sha256:{checksum}",
            "updatedAt": updated_at,
        }
        if detail_pattern:
            entry["detailPattern"] = detail_pattern

        html_patterns = {
            "compare": "/compare/{slug}/",
        }
        if col_name in html_patterns:
            entry["htmlPattern"] = html_patterns[col_name]

        collections[col_name] = entry

    manifest = {
        "version": API_VERSION,
        "generatedAt": now,
        "collections": collections,
        "totalSizeBytes": total_bytes,
        "packsUrl": "/api/v1/packs.json",
    }
    write_json(OUTPUT_DIR / "manifest.json", manifest)
    return manifest


# Pack definitions -------------------------------------------------------

COUNTRY_PACKS = [
    ("japan",          "Japan Travel Pack",           "JP", ["asia", "safe", "cultural"],       "Japanese",   "110"),
    ("thailand",       "Thailand Travel Pack",        "TH", ["asia", "beach", "budget"],         "Thai",       "191"),
    ("italy",          "Italy Travel Pack",           "IT", ["europe", "cultural", "food"],       "Italian",    "112"),
    ("france",         "France Travel Pack",          "FR", ["europe", "cultural", "romantic"],   "French",     "15"),
    ("spain",          "Spain Travel Pack",           "ES", ["europe", "beach", "food"],          "Spanish",    "112"),
    ("mexico",         "Mexico Travel Pack",          "MX", ["latin-america", "beach", "food"],   "Spanish",    "911"),
    ("germany",        "Germany Travel Pack",         "DE", ["europe", "cultural", "beer"],       "German",     "112"),
    ("australia",      "Australia Travel Pack",       "AU", ["oceania", "nature", "beach"],       "English",    "000"),
    ("south-korea",    "South Korea Travel Pack",     "KR", ["asia", "cultural", "food"],         "Korean",     "112"),
    ("united-kingdom", "United Kingdom Travel Pack",  "GB", ["europe", "cultural", "city"],       "English",    "999"),
]

REGION_PACKS = [
    ("se-asia",          "Southeast Asia Pack",     ["TH","VN","ID","MY","PH","KH","LA","MM","SG"],    ["asia","backpacker","beach"]),
    ("europe-western",   "Western Europe Pack",     ["FR","ES","PT","IT","DE","NL","BE","AT","CH"],    ["europe","cultural","city"]),
    ("europe-eastern",   "Eastern Europe Pack",     ["PL","CZ","HU","HR","RO","BG","RS","SI","SK","BA","ME","MK","AL"], ["europe","budget","cultural"]),
    ("central-america",  "Central America Pack",    ["CR","PA","BZ","GT","HN","NI","SV","MX"],         ["latin-america","nature","adventure"]),
    ("south-america",    "South America Pack",      ["CO","PE","AR","BR","CL","EC","BO","UY"],         ["latin-america","adventure","nature"]),
]

THEME_PACKS = [
    ("solo-female-safe",   "Solo Female Safe Pack"),
    ("budget-backpacker",  "Budget Backpacker Pack"),
]


def _load_index_items(index_file, list_key):
    """Load items list from an index JSON file."""
    path = OUTPUT_DIR / index_file
    if not path.exists():
        return []
    with open(path) as f:
        data = json.load(f)
    return data.get(list_key, [])


def _reindex_scams_index_from_disk():
    """Rewrite api/v1/scams.json from the actual contents of api/v1/scams/*.json.

    Eliminates a class of drift where PRs add a per-slug scam JSON without
    updating the catalog index — the audit + verify_catalog_disk used to either
    fail loudly or silently delete the unindexed JSON. This pulls the index back
    in line with disk every build.
    """
    scams_dir = OUTPUT_DIR / "scams"
    items = []
    if scams_dir.is_dir():
        for path in sorted(scams_dir.glob("*.json")):
            slug = path.stem
            items.append({
                "slug": slug,
                "url": f"{SITE_URL}/scams/{slug}/",
            })
    payload = {
        "count": len(items),
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "items": items,
    }
    write_json(OUTPUT_DIR / "scams.json", payload)
    return items


def _read_json_file(path):
    """Read a JSON file, return None if missing."""
    p = Path(path)
    if not p.exists():
        return None
    try:
        with open(p) as f:
            return json.load(f)
    except Exception:
        return None


def _pack_checksum(data_bytes):
    return "sha256:" + hashlib.sha256(data_bytes).hexdigest()


def _build_single_pack(pack_id, name, description, pack_type, countries,
                       dest_slug_to_country, all_dest_summaries,
                       all_itin_summaries,
                       scam_slugs_by_country, tags, primary_language="", emergency_number=""):

    """Build a single pack file and return its catalog entry."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    country_set = set(c.upper() for c in countries)

    # countries data
    countries_data = []
    for iso2 in countries:
        c_data = _read_json_file(OUTPUT_DIR / "countries" / f"{iso2.lower()}.json")
        if c_data:
            countries_data.append(c_data)

    # safety data
    safety_data = []
    for iso2 in countries:
        s_data = _read_json_file(OUTPUT_DIR / "safety" / f"{iso2.lower()}.json")
        if s_data:
            safety_data.append(s_data)

    # alerts data
    alerts_data = []
    for iso2 in countries:
        a_data = _read_json_file(OUTPUT_DIR / "alerts" / f"{iso2.lower()}.json")
        if a_data:
            alerts_data.append(a_data)

    # destinations — filter summaries by countryCode
    dest_summaries = [d for d in all_dest_summaries if d.get("countryCode", "").upper() in country_set]


    # itineraries — filter by destination country
    itin_summaries = [
        i for i in all_itin_summaries
        if dest_slug_to_country.get(i.get("destinationSlug", ""), "").upper() in country_set
    ]

    # scams — filter by countryCode (sort for deterministic output)
    scam_cities = []
    scams_data = []
    for iso2 in sorted(countries):
        for slug in sorted(scam_slugs_by_country.get(iso2.upper(), [])):
            scam_detail = _read_json_file(OUTPUT_DIR / "scams" / f"{slug}.json")
            if scam_detail:
                scams_data.append(scam_detail)
                scam_cities.append(scam_detail.get("city", slug))

    payload = {
        "id": f"pack:{pack_id}",
        "name": name,
        "description": description,
        "version": 1,
        "generatedAt": now,
        "coverage": {
            "countries": list(countries),
            "destinationCount": len(dest_summaries),
            "itineraryCount": len(itin_summaries),
            "scamCities": scam_cities,
        },
        "data": {
            "countries": countries_data,
            "safety": safety_data,
            "alerts": alerts_data,
            "destinations": dest_summaries,
            "scams": scams_data,
            "itineraries": itin_summaries,
        },
        "metadata": {
            "packType": pack_type,
            "tags": tags,
            "primaryLanguage": primary_language,
            "emergencyNumber": emergency_number,
        },
    }

    # Pack integrity checksum: sha256 of the canonical form of the embedded
    # `data` object (sorted keys, no whitespace). The previous implementation
    # hashed the file content BEFORE adding sizeBytes/checksum, then wrote the
    # file WITH those fields appended, so the recorded checksum couldn't match
    # any sha256(file) recompute by a consumer. Hashing only `data` makes the
    # value stable and round-trip verifiable: a consumer canonicalises
    # `pack.data` the same way and compares.
    data_canonical = json.dumps(payload["data"], sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    payload["checksum"] = _pack_checksum(data_canonical)
    payload["checksumSubject"] = "data"

    packs_dir = OUTPUT_DIR / "packs"
    packs_dir.mkdir(parents=True, exist_ok=True)
    write_json(packs_dir / f"{pack_id}.json", payload)
    # sizeBytes is the actual size of the pack file as deployed — read it back
    # so the catalog entry matches what HTTP clients see in Content-Length.
    payload["sizeBytes"] = (packs_dir / f"{pack_id}.json").stat().st_size

    return {
        "id": f"pack:{pack_id}",
        "name": name,
        "packType": pack_type,
        "countries": list(countries),
        "destinationCount": len(dest_summaries),
        "sizeBytes": payload["sizeBytes"],
        "url": f"/api/v1/packs/{pack_id}.json",
    }


def build_packs():
    """Build all offline pack files and the packs.json index."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Load shared indexes once
    all_dest_summaries = _load_index_items("destinations.json", "destinations")
    all_itin_summaries = _load_index_items("itineraries.json", "itineraries")
    all_filter_items = _load_index_items("filter.json", "items")

    # Build slug -> countryCode lookup from destinations index
    dest_slug_to_country = {d["slug"]: d.get("countryCode", "") for d in all_dest_summaries}

    # Build scam city slugs grouped by countryCode. We can't read this from
    # api/v1/scams.json[items] — that index is intentionally minimal
    # ({slug, url} only) — so walk the per-slug detail files instead. Without
    # this, every pack's scams[] came out empty because every slug clustered
    # under the empty-string key.
    scams_dir = OUTPUT_DIR / "scams"
    scam_slugs_by_country = {}
    if scams_dir.is_dir():
        for path in sorted(scams_dir.glob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            cc = (data.get("countryCode") or "").upper()
            if cc:
                scam_slugs_by_country.setdefault(cc, []).append(path.stem)

    # Filter records may have nested fields explicitly set to None (not just missing); use `or {}` so
    # the chained .get() doesn't blow up on AttributeError.
    solo_candidates = [
        it for it in all_filter_items
        if (it.get("safety") or {}).get("soloFemaleSafety") in ("very-safe", "safe")
        and (it.get("budget") or {}).get("tier") in ("budget", "moderate")
    ]
    solo_candidates.sort(key=lambda x: (x.get("scores") or {}).get("editorial", 0), reverse=True)
    solo_female_slugs = {m["slug"] for m in solo_candidates[:25]}
    budget_slugs = set()
    budget_countries = set()
    for item in all_filter_items:
        if (item.get("budget") or {}).get("raw") == "$":
            budget_countries.add(item.get("countryCode", "").upper())
            budget_slugs.add(item.get("slug", ""))

    catalog_entries = []

    # --- Country packs ---
    for pack_id, pack_name, iso2, tags, lang, emergency in COUNTRY_PACKS:
        desc = f"Complete offline guide: destinations, safety, scams, and itineraries for {pack_name.replace(' Travel Pack', '')}."
        entry = _build_single_pack(
            pack_id=pack_id,
            name=pack_name,
            description=desc,
            pack_type="country",
            countries=[iso2],
            dest_slug_to_country=dest_slug_to_country,
            all_dest_summaries=all_dest_summaries,
            all_itin_summaries=all_itin_summaries,
            scam_slugs_by_country=scam_slugs_by_country,
            tags=tags,
            primary_language=lang,
            emergency_number=emergency,
        )
        catalog_entries.append(entry)

    # --- Region packs ---
    for pack_id, pack_name, countries, tags in REGION_PACKS:
        desc = f"Offline travel bundle covering {len(countries)} countries in {pack_name.replace(' Pack', '')}: destinations, safety, scams, and itineraries."
        entry = _build_single_pack(
            pack_id=pack_id,
            name=pack_name,
            description=desc,
            pack_type="region",
            countries=countries,
            dest_slug_to_country=dest_slug_to_country,
            all_dest_summaries=all_dest_summaries,
            all_itin_summaries=all_itin_summaries,
            scam_slugs_by_country=scam_slugs_by_country,
            tags=tags,
        )
        catalog_entries.append(entry)

    # --- Theme packs ---
    # solo-female-safe
    solo_countries = sorted({dest_slug_to_country.get(s, "") for s in solo_female_slugs if dest_slug_to_country.get(s)})
    solo_dest_summaries = [d for d in all_dest_summaries if d.get("slug") in solo_female_slugs]
    solo_itin = [i for i in all_itin_summaries if dest_slug_to_country.get(i.get("destinationSlug", ""), "") in set(solo_countries)]

    solo_payload = {
        "id": "pack:solo-female-safe",
        "name": "Solo Female Safe Pack",
        "description": "Top destinations rated safest for solo female travel — curated from editorial recommendations.",
        "version": 1,
        "generatedAt": now,
        "coverage": {
            "countries": solo_countries,
            "destinationCount": len(solo_dest_summaries),
            "itineraryCount": len(solo_itin),
            "scamCities": [],
        },
        "data": {
            "countries": [],
            "safety": [],
            "alerts": [],
            "destinations": solo_dest_summaries,
            "scams": [],
            "itineraries": solo_itin,
        },
        "metadata": {"packType": "theme", "tags": ["solo-female", "safe", "recommended"]},
    }
    # Same canonical-data checksum approach as _build_single_pack — see comment there.
    solo_data_canonical = json.dumps(solo_payload["data"], sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    solo_payload["checksum"] = _pack_checksum(solo_data_canonical)
    solo_payload["checksumSubject"] = "data"
    packs_dir = OUTPUT_DIR / "packs"
    packs_dir.mkdir(parents=True, exist_ok=True)
    write_json(packs_dir / "solo-female-safe.json", solo_payload)
    solo_payload["sizeBytes"] = (packs_dir / "solo-female-safe.json").stat().st_size
    catalog_entries.append({
        "id": "pack:solo-female-safe",
        "name": "Solo Female Safe Pack",
        "packType": "theme",
        "countries": solo_countries,
        "destinationCount": len(solo_dest_summaries),
        "sizeBytes": solo_payload["sizeBytes"],
        "url": "/api/v1/packs/solo-female-safe.json",
    })

    # budget-backpacker
    budget_dest_summaries = [d for d in all_dest_summaries if d.get("slug") in budget_slugs]
    budget_countries_list = sorted(budget_countries)
    budget_itin = [i for i in all_itin_summaries if dest_slug_to_country.get(i.get("destinationSlug", ""), "").upper() in budget_countries]

    budget_payload = {
        "id": "pack:budget-backpacker",
        "name": "Budget Backpacker Pack",
        "description": "Destinations where a daily budget under $50 is realistic — the definitive budget travel collection.",
        "version": 1,
        "generatedAt": now,
        "coverage": {
            "countries": budget_countries_list,
            "destinationCount": len(budget_dest_summaries),
            "itineraryCount": len(budget_itin),
            "scamCities": [],
        },
        "data": {
            "countries": [],
            "safety": [],
            "alerts": [],
            "destinations": budget_dest_summaries,
            "scams": [],
            "itineraries": budget_itin,
        },
        "metadata": {"packType": "theme", "tags": ["budget", "backpacker", "cheap"]},
    }
    budget_data_canonical = json.dumps(budget_payload["data"], sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    budget_payload["checksum"] = _pack_checksum(budget_data_canonical)
    budget_payload["checksumSubject"] = "data"
    write_json(packs_dir / "budget-backpacker.json", budget_payload)
    budget_payload["sizeBytes"] = (packs_dir / "budget-backpacker.json").stat().st_size
    catalog_entries.append({
        "id": "pack:budget-backpacker",
        "name": "Budget Backpacker Pack",
        "packType": "theme",
        "countries": budget_countries_list,
        "destinationCount": len(budget_dest_summaries),
        "sizeBytes": budget_payload["sizeBytes"],
        "url": "/api/v1/packs/budget-backpacker.json",
    })

    packs_index = {
        "count": len(catalog_entries),
        "lastUpdated": now,
        "packs": catalog_entries,
    }
    write_json(OUTPUT_DIR / "packs.json", packs_index)
    return len(catalog_entries)


# ---------------------------------------------------------------------------
# Knowledge chunks
# ---------------------------------------------------------------------------

def _chunk_id(*parts):
    return "chunk:" + ":".join(str(p).lower().replace(" ", "-") for p in parts)


def _safety_chunks(safety_detail, source_url_base):
    """Generate all chunk types from a single safety profile."""
    chunks = []
    iso2 = safety_detail.get("iso2", "").lower()
    name = safety_detail.get("name", iso2.upper())
    updated = safety_detail.get("lastUpdated", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    source_url = f"{source_url_base}/safety/{iso2}.json"

    # countrySafetySummary
    safety = safety_detail.get("safety", {})
    overall = safety.get("overallRisk", "unknown")
    violent = safety.get("violentCrime", "unknown")
    petty = safety.get("pettyCrime", "unknown")
    lgbt = safety.get("lgbtSafety", "")
    solo = safety.get("soloFemaleSafety", "")
    disasters = ", ".join(safety.get("naturalDisasters", [])) or "none documented"
    advisory = safety_detail.get("travelAdvisory", {})
    adv_text = advisory.get("summary", "")
    adv_level = advisory.get("levelText", "")

    text = (
        f"{name} has an overall safety risk rated as {overall}. "
        f"Violent crime is {violent} and petty crime (pickpocketing, scams) is {petty}. "
    )
    if adv_level:
        text += f"The US State Department advises: {adv_level}. "
    if adv_text:
        text += f"{adv_text} "
    if solo:
        text += f"For solo female travelers: {solo}. "
    if lgbt:
        text += f"LGBTQ+ safety: {lgbt}. "
    if disasters != "none documented":
        text += f"Natural disaster risks include: {disasters}."

    chunks.append({
        "id": _chunk_id("safety", iso2, "summary"),
        "type": "countrySafetySummary",
        "entityId": f"safety:{iso2}",
        "text": text.strip(),
        "tags": [iso2, name.lower(), "safety", "risk", overall],
        "sourceUrl": source_url,
        "updatedAt": updated,
        "confidence": CONFIDENCE_EDITORIAL,
        "provenance": "official-sources + editorial",
    })

    # emergencyContact
    emergency = safety_detail.get("emergency", {})
    police = emergency.get("police", "unknown")
    ambulance = emergency.get("ambulance", "unknown")
    fire = emergency.get("fire", "unknown")
    notes = emergency.get("notes", "")
    text = (
        f"In {name}, call {police} for police, {ambulance} for ambulance/medical emergency, "
        f"and {fire} for fire services. "
    )
    if notes:
        text += notes
    embassies = safety_detail.get("embassies", [])
    if embassies:
        emb = embassies[0]
        emb_name = emb.get("name", "US Embassy")
        emb_phone = emb.get("phone", "")
        emb_city = emb.get("city", "")
        if emb_phone:
            text += f" The {emb_name} in {emb_city} can be reached at {emb_phone}."

    chunks.append({
        "id": _chunk_id("safety", iso2, "emergency"),
        "type": "emergencyContact",
        "entityId": f"safety:{iso2}",
        "text": text.strip(),
        "tags": [iso2, name.lower(), "emergency", "police", "ambulance"],
        "sourceUrl": source_url,
        "updatedAt": updated,
        "confidence": CONFIDENCE_EDITORIAL,
        "provenance": "official-sources + editorial",
    })

    # healthcareGuide
    hc = safety_detail.get("healthcare", {})
    if hc:
        system = hc.get("systemType", "")
        quality = hc.get("qualityRating", "")
        cost = hc.get("costForTourists", "")
        pharmacy = hc.get("pharmacyAccess", "")
        hospital_notes = hc.get("hospitalNotes", "")
        vaccinations = ", ".join(hc.get("vaccinationsRecommended", [])) or "routine vaccinations"
        malaria = hc.get("malariaRisk", False)
        insurance_advice = hc.get("insuranceAdvice", "")

        text = f"{name} has a {system} healthcare system, rated {quality} quality. "
        if cost:
            text += f"Typical costs for tourists: {cost}. "
        if pharmacy:
            text += f"Pharmacy access: {pharmacy}. "
        if hospital_notes:
            text += f"{hospital_notes} "
        text += f"Recommended vaccinations: {vaccinations}. "
        if malaria:
            text += "Malaria risk is present — consult a travel doctor before visiting. "
        else:
            text += "Malaria risk is negligible. "
        if insurance_advice:
            text += f"Travel insurance advice: {insurance_advice}"

        chunks.append({
            "id": _chunk_id("safety", iso2, "healthcare"),
            "type": "healthcareGuide",
            "entityId": f"safety:{iso2}",
            "text": text.strip(),
            "tags": [iso2, name.lower(), "healthcare", "hospital", "medical"],
            "sourceUrl": source_url,
            "updatedAt": updated,
            "confidence": CONFIDENCE_EDITORIAL,
            "provenance": "official-sources + editorial",
        })

    # medicationRestriction — one chunk per controlled substance entry
    medications = safety_detail.get("medications", {})
    if isinstance(medications, dict):
        controlled = medications.get("controlledSubstances", [])
    else:
        controlled = medications if isinstance(medications, list) else []
    for med in controlled:
        if not isinstance(med, dict):
            continue
        med_name = med.get("drug") or med.get("name", "")
        status = med.get("status", "")
        notes = med.get("note") or med.get("notes", "")
        if not med_name:
            continue
        text = f"{med_name} is {status} in {name}. "
        if notes:
            text += notes
        chunks.append({
            "id": _chunk_id("safety", iso2, "medication", med_name),
            "type": "medicationRestriction",
            "entityId": f"safety:{iso2}",
            "text": text.strip(),
            "tags": [iso2, name.lower(), "medication", status, med_name.lower()],
            "sourceUrl": source_url,
            "updatedAt": updated,
            "confidence": CONFIDENCE_EDITORIAL,
            "provenance": "official-sources + editorial",
        })

    return chunks


def _alert_chunk(alert_detail, source_url_base):
    """Generate an advisorySnapshot chunk from an alerts detail file."""
    iso2 = alert_detail.get("iso2", "").lower()
    name = alert_detail.get("name", iso2.upper())
    updated = alert_detail.get("lastUpdated", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    source_url = f"{source_url_base}/alerts/{iso2}.json"
    combined_level = alert_detail.get("combinedLevel", "unknown")
    combined_summary = alert_detail.get("combinedSummary", "")

    us = alert_detail.get("us", {})
    uk = alert_detail.get("uk", {})
    us_summary = us.get("summary", "")
    uk_summary = uk.get("summary", "")

    text = f"Travel advisory for {name}: overall risk level is {combined_level}. "
    if combined_summary:
        text += f"{combined_summary} "
    if us_summary:
        text += f"US State Department: {us_summary} "
    if uk_summary:
        text += f"UK FCDO: {uk_summary}"

    return {
        "id": _chunk_id("alert", iso2, "snapshot"),
        "type": "advisorySnapshot",
        "entityId": f"alerts:{iso2}",
        "text": text.strip(),
        "tags": [iso2, name.lower(), "advisory", "travel-warning", combined_level],
        "sourceUrl": source_url,
        "updatedAt": updated,
        "confidence": CONFIDENCE_EDITORIAL,
        "provenance": "official-sources + editorial",
    }


def _scam_chunks(scam_detail, source_url_base):
    """Generate scamPattern chunks from a scam city detail file."""
    chunks = []
    iso2 = scam_detail.get("countryCode", "").lower()
    city = scam_detail.get("city", "")
    country = scam_detail.get("country", "")
    updated = scam_detail.get("lastUpdated", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    source_url = f"{source_url_base}/scams/{scam_detail.get('slug', '')}.json"

    for scam in scam_detail.get("scams", []):
        scam_name = scam.get("name", "")
        description = scam.get("description", "")
        avoidance = scam.get("avoidance", "")
        category = scam.get("category", "")
        severity = scam.get("severity", "")
        if not scam_name:
            continue

        text = f"Scam alert in {city}, {country} — {scam_name} ({category}, severity: {severity}). "
        if description:
            text += f"{description} "
        if avoidance:
            text += f"How to avoid: {avoidance}"

        slug_part = scam.get("id", scam_name).split(":")[-1]
        chunks.append({
            "id": _chunk_id("scam", iso2, city, slug_part),
            "type": "scamPattern",
            "entityId": scam.get("id", f"scam:{city.lower()}:{slug_part}"),
            "text": text.strip(),
            "tags": [iso2, city.lower(), "scam", category, severity],
            "sourceUrl": source_url,
            "updatedAt": updated,
            "confidence": CONFIDENCE_EDITORIAL,
            "provenance": "official-sources + editorial",
        })
    return chunks


def _destination_chunk(dest_detail, source_url_base):
    """Generate a destinationPracticalSummary chunk from a destination detail file."""
    slug = dest_detail.get("slug", "")
    name = dest_detail.get("name", slug)
    country = dest_detail.get("country", "")
    cc = dest_detail.get("countryCode", "").lower()
    updated = dest_detail.get("updatedAt", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    source_url = f"{source_url_base}/destinations/{slug}.json"

    budget = dest_detail.get("budget", "")
    season = dest_detail.get("season", "")
    vibes = ", ".join(dest_detail.get("vibes", [])) or ""
    currency = dest_detail.get("currency", {})
    currency_name = currency.get("name", "") if isinstance(currency, dict) else str(currency)
    currency_code = currency.get("code", "") if isinstance(currency, dict) else ""
    language = dest_detail.get("language", "")
    tap_water = dest_detail.get("tapWaterSafe")
    tipping = dest_detail.get("tippingCustom", "")
    visa = dest_detail.get("visaNote", "")
    pitch = dest_detail.get("pitch", "")
    timezone_str = dest_detail.get("timezone", "")

    text = f"{name} is a destination in {country}. "
    if pitch:
        text += f"{pitch} "
    if vibes:
        text += f"Known for: {vibes}. "
    if budget:
        text += f"Budget level: {budget}. "
    if season:
        text += f"Best time to visit: {season}. "
    if currency_name:
        text += f"Currency: {currency_name}"
        if currency_code:
            text += f" ({currency_code})"
        text += ". "
    if language:
        text += f"Primary language: {language}. "
    if tap_water is not None:
        text += f"Tap water is {'safe to drink' if tap_water else 'not safe to drink — buy bottled water'}. "
    if tipping:
        text += f"Tipping: {tipping}. "
    if visa:
        text += f"Visa: {visa}."

    tags = [cc, country.lower(), name.lower(), "destination", "practical"]
    if vibes:
        tags += [v.lower() for v in dest_detail.get("vibes", [])]

    return {
        "id": _chunk_id("destination", slug, "practical"),
        "type": "destinationPracticalSummary",
        "entityId": f"destination:{slug}",
        "text": text.strip(),
        "tags": list(dict.fromkeys(tags)),
        "sourceUrl": source_url,
        "updatedAt": updated,
        "confidence": CONFIDENCE_EDITORIAL,
        "provenance": "editorial",
    }


def build_knowledge_chunks():
    """Generate AI-ready text chunks from all API data."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    chunks = []

    # Safety chunks (all profiles)
    safety_dir = OUTPUT_DIR / "safety"
    if safety_dir.is_dir():
        for fp in sorted(safety_dir.glob("*.json")):
            detail = _read_json_file(fp)
            if detail and detail.get("iso2"):
                chunks.extend(_safety_chunks(detail, API_BASE_URL))

    # Advisory chunks (all alert detail files)
    alerts_dir = OUTPUT_DIR / "alerts"
    if alerts_dir.is_dir():
        for fp in sorted(alerts_dir.glob("*.json")):
            detail = _read_json_file(fp)
            if detail and detail.get("iso2"):
                chunks.append(_alert_chunk(detail, API_BASE_URL))

    # Scam chunks
    scams_dir = OUTPUT_DIR / "scams"
    if scams_dir.is_dir():
        for fp in sorted(scams_dir.glob("*.json")):
            detail = _read_json_file(fp)
            if detail and detail.get("scams"):
                chunks.extend(_scam_chunks(detail, API_BASE_URL))

    # Destination practical summaries — top 500 by editorial score
    filter_items = _load_index_items("filter.json", "items")
    filter_items_sorted = sorted(
        filter_items,
        key=lambda x: x.get("scores", {}).get("editorial", 0),
        reverse=True,
    )
    top_dest_slugs = [item["slug"] for item in filter_items_sorted[:500]]

    added = 0
    for slug in top_dest_slugs:
        if added >= 500:
            break
        detail = _DEST_DETAILS.get(slug)
        if detail:
            chunks.append(_destination_chunk(detail, API_BASE_URL))
            added += 1

    knowledge_dir = OUTPUT_DIR / "knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "version": API_VERSION,
        "generatedAt": now,
        "chunkCount": len(chunks),
        "chunks": chunks,
    }
    write_json(knowledge_dir / "chunks.json", payload)
    return chunks


def build_knowledge_pack_chunks():
    """For each pack, generate knowledge/chunks/{pack}.json with relevant chunks."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Load all chunks
    chunks_path = OUTPUT_DIR / "knowledge" / "chunks.json"
    if not chunks_path.exists():
        return 0

    with open(chunks_path) as f:
        all_chunks_data = json.load(f)
    all_chunks = all_chunks_data.get("chunks", [])

    # Load packs index
    packs_index = _read_json_file(OUTPUT_DIR / "packs.json") or {}
    packs_list = packs_index.get("packs", [])

    chunks_dir = OUTPUT_DIR / "knowledge" / "chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for pack_entry in packs_list:
        pack_id = pack_entry.get("id", "").replace("pack:", "")
        pack_countries = set(c.upper() for c in pack_entry.get("countries", []))

        # Load the pack detail to get destination slugs
        pack_detail = _read_json_file(OUTPUT_DIR / "packs" / f"{pack_id}.json") or {}
        pack_dest_slugs = set(d.get("slug", "") for d in pack_detail.get("data", {}).get("destinations", []))

        relevant = []
        for chunk in all_chunks:
            tags = set(chunk.get("tags", []))
            entity_id = chunk.get("entityId", "")
            chunk_type = chunk.get("type", "")

            # Match by country code in tags or entityId
            tags_upper = {t.upper() for t in tags if t}
            iso2_from_entity = entity_id.split(":")[-1].upper() if ":" in entity_id else ""
            if (iso2_from_entity and iso2_from_entity in pack_countries) or (tags_upper & pack_countries):
                relevant.append(chunk)
                continue

            # Match destination chunks by slug
            if chunk_type == "destinationPracticalSummary":
                slug = entity_id.replace("destination:", "")
                if slug in pack_dest_slugs:
                    relevant.append(chunk)

        payload = {
            "version": API_VERSION,
            "packId": f"pack:{pack_id}",
            "generatedAt": now,
            "chunkCount": len(relevant),
            "chunks": relevant,
        }
        write_json(chunks_dir / f"{pack_id}.json", payload)
        count += 1

    return count


def main():
    print("🦉 Building Tabiji API v1...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("📍 Building destinations...")
    dest_summaries, dest_count = build_destinations()
    print(f"   ✅ {dest_count} destinations")

    print("🗺️  Building itineraries...")
    itin_summaries, itin_count = build_itineraries()
    print(f"   ✅ {itin_count} itineraries")

    print("⚔️  Building comparisons...")
    compare_summaries, compare_count = build_compare()
    print(f"   ✅ {compare_count} comparisons")

    print("🕸️  Building cross-links and editorial enrichment...")
    build_relationships(dest_summaries, itin_summaries, compare_summaries)
    print("   ✅ related records, provenance, freshness")

    # Load additional entity type indexes for catalog/search.
    country_items = _load_index_items("countries.json", "countries")
    safety_items = _load_index_items("safety.json", "profiles")
    alert_items = _load_index_items("alerts.json", "alerts")

    # Always rebuild scams.json[items] from on-disk api/v1/scams/*.json so the catalog
    # cannot drift behind the per-slug detail JSONs that PRs add directly.
    scam_items = _reindex_scams_index_from_disk()
    print(f"   ✅ scams.json reindexed: {len(scam_items)} items from {OUTPUT_DIR / 'scams'}")

    print("🧭 Building normalized catalog...")
    catalog_payload = build_catalog(dest_summaries, itin_summaries, compare_summaries,
                                    country_items=country_items, safety_items=safety_items,
                                    alert_items=alert_items, scam_items=scam_items)
    print(f"   ✅ {catalog_payload['itemCount']} entities in {catalog_payload['chunks']} chunks")

    print("🔎 Building search index...")
    search_payload = build_search(dest_summaries, itin_summaries, compare_summaries,
                                  country_items=country_items, safety_items=safety_items,
                                  alert_items=alert_items, scam_items=scam_items)
    print(f"   ✅ {search_payload['count']} documents")

    print("🛡️  Building safety profiles...")
    safety_count = build_safety()
    print(f"   ✅ {safety_count} safety profiles")

    print("🚨 Building travel alerts...")
    alerts_count = build_alerts()
    print(f"   ✅ {alerts_count} countries with alerts")

    print("📋 Building index...")
    build_index(dest_count, itin_count, compare_count, search_payload['count'],
                safety_count=safety_count, alerts_count=alerts_count,
                country_count=len(country_items), scam_count=len(scam_items))
    print("   ✅ index.json")

    print("🧭 Regenerating agent/discovery docs...")
    build_openapi(dest_count, itin_count, compare_count)
    build_llms_txt(dest_count, itin_count, compare_count)
    build_agents_json(dest_count, itin_count, compare_count)
    print("   ✅ openapi.json, llms.txt, agents.json")

    print("🌍 Building country facts...")
    country_count = build_country_facts()
    print(f"   ✅ {country_count} countries")

    print("🔍 Building filterable index...")
    filter_items, filter_count = build_filter()
    print(f"   ✅ {filter_count} destinations in filter index")

    print("📊 Building facets...")
    build_facets(filter_items)
    print("   ✅ facets.json")

    print("📄 Updating API docs page...")
    build_docs_page(dest_count, itin_count, compare_count, country_count)
    print("   ✅ api/index.html")

    print("📦 Building manifest...")
    build_manifest()
    print("   ✅ manifest.json")

    print("🗃️  Building offline packs...")
    packs_count = build_packs()
    print(f"   ✅ {packs_count} packs")

    print("🧠 Building knowledge chunks...")
    knowledge_chunks = build_knowledge_chunks()
    print(f"   ✅ {len(knowledge_chunks)} chunks")

    print("🔗 Building per-pack knowledge chunks...")
    pack_chunk_count = build_knowledge_pack_chunks()
    print(f"   ✅ {pack_chunk_count} pack chunk files")

    print("🔍 Verifying catalog ↔ disk reconciliation...")
    issues = verify_catalog_disk()
    if issues:
        print("   ❌ Reconciliation failed:")
        for line in issues:
            print(f"     {line}")
        raise SystemExit(1)
    print("   ✅ all catalogs match on-disk files")


# ---------------------------------------------------------------------------
# Catalog ↔ disk reconciliation
# ---------------------------------------------------------------------------


def _slug_set_from_catalog(path, list_key, slug_key="slug"):
    """Read a catalog JSON and return the set of slugs/ISO codes referenced."""
    if not path.exists():
        return set()
    data = json.load(open(path))
    items = data.get(list_key, [])
    out = set()
    for item in items:
        key = item.get(slug_key) or item.get("iso2")
        if key:
            out.add(key.lower())
    return out


def _slug_set_from_dir(directory, suffix=".json"):
    """Return the set of file stems in a directory (lowercase)."""
    if not directory.is_dir():
        return set()
    return {p.stem.lower() for p in directory.glob(f"*{suffix}")}


def verify_catalog_disk():
    """Assert each catalog index matches the per-slug files on disk.

    Returns a list of human-readable issue strings; empty list means OK.
    Collections checked (catalog file, list-key, detail-dir):
      - alerts.json[alerts]    → alerts/<iso>.json
      - safety.json[profiles]  → safety/<iso>.json
      - countries.json[countries] → countries/<iso>.json
      - scams.json[items]      → scams/<slug>.json
      - itineraries.json[itineraries] → itineraries/<slug>.json
    Skipped: compare (per-slug retired),
             destinations (per-slug served by Worker, no static dir).
    """
    issues = []
    checks = [
        ("alerts.json",     "alerts",     "iso2", "alerts"),
        ("safety.json",     "profiles",   "iso2", "safety"),
        ("countries.json",  "countries",  "iso2", "countries"),
        ("scams.json",      "items",      "slug", "scams"),
        ("itineraries.json","itineraries","slug", "itineraries"),
    ]
    for catalog_file, list_key, slug_key, detail_dir in checks:
        catalog_path = OUTPUT_DIR / catalog_file
        detail_path = OUTPUT_DIR / detail_dir
        listed = _slug_set_from_catalog(catalog_path, list_key, slug_key)
        on_disk = _slug_set_from_dir(detail_path)
        missing = listed - on_disk
        orphan = on_disk - listed
        if missing:
            issues.append(f"{catalog_file}: {len(missing)} listed but missing on disk: {sorted(list(missing))[:5]}")
        if orphan:
            issues.append(f"{catalog_file}: {len(orphan)} files on disk not listed: {sorted(list(orphan))[:5]}")
    return issues


if __name__ == "__main__":
    main()
