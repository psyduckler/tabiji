#!/usr/bin/env python3
import json
import re
from pathlib import Path
from html import unescape

ROOT = Path(__file__).resolve().parents[1]
PP_DIR = ROOT / "popular-picks"
API_DIR = ROOT / "api" / "v1" / "picks"

DAY_MAP = {
    "Mon": "Monday",
    "Tue": "Tuesday",
    "Wed": "Wednesday",
    "Thu": "Thursday",
    "Fri": "Friday",
    "Sat": "Saturday",
    "Sun": "Sunday",
}


def clean_price(value: str | None) -> str | None:
    if not value:
        return None
    return re.sub(r"^[^\d$€£¥₩฿₺₹]+\s*", "", value).strip()


def infer_place_type(page_slug: str, title: str, category: str, tags: list[str], name: str) -> str:
    hay = " ".join([page_slug, title, category, name] + tags).lower()
    if any(k in hay for k in ["riad", "ryokan", "hotel", "lodge", "lodges", "stay", "stays"]):
        return "Hotel"
    if "campground" in hay:
        return "Campground"
    if any(k in hay for k in ["camp", "camps"]):
        return "LodgingBusiness"
    if any(k in hay for k in ["bar", "bars", "pub", "pubs", "mezcaleria", "mezcalerias", "beer", "brewery", "breweries", "cocktail"]):
        return "BarOrPub"
    if any(k in hay for k in ["cafe", "cafes", "coffee", "brunch", "bakery", "bakeries"]):
        return "CafeOrCoffeeShop"
    if any(k in hay for k in ["market", "markets", "street food", "food", "restaurant", "restaurants", "bbq", "ramen", "sushi", "gelato", "pizza", "shawarma", "falafel", "tacos", "brunch"]):
        return "Restaurant"
    if any(k in hay for k in ["tour", "tours", "museum", "museums", "art", "viewpoint", "viewpoints", "temple", "temples", "sanctuary", "village", "vintage shopping", "shopping", "massage", "snorkeling", "snorkelling", "diving", "dive", "beach club", "beach clubs", "beach", "beaches", "hiking", "trail", "trails", "sunset", "cruise", "cruises", "farm", "farms", "cooking class", "cooking classes"]):
        return "TouristAttraction"
    return "LocalBusiness"


def parse_time(token: str, fallback_suffix: str | None = None) -> str | None:
    token = token.strip()
    if not token:
        return None
    if token.endswith(("AM", "PM")):
        suffixed = token
    elif fallback_suffix:
        suffixed = f"{token} {fallback_suffix}"
    else:
        return None
    m = re.match(r"^(\d{1,2})(?::(\d{2}))?\s*(AM|PM)$", suffixed)
    if not m:
        return None
    hour = int(m.group(1))
    minute = int(m.group(2) or "0")
    suffix = m.group(3)
    if hour == 12:
        hour = 0
    if suffix == "PM":
        hour += 12
    return f"{hour:02d}:{minute:02d}"


def opening_hours_spec(hours: dict | None):
    if not hours:
        return None
    specs = []
    for short_day, value in hours.items():
        value = (value or "").strip()
        if not value or value.lower() == "closed":
            continue
        if value.lower() == "open 24 hours":
            specs.append({
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": DAY_MAP.get(short_day, short_day),
                "opens": "00:00",
                "closes": "23:59",
            })
            continue
        parts = re.split(r"\s*[–-]\s*", value)
        if len(parts) != 2:
            continue
        open_raw, close_raw = parts
        close_suffix_match = re.search(r"(AM|PM)$", close_raw.strip())
        close_suffix = close_suffix_match.group(1) if close_suffix_match else None
        open_24 = parse_time(open_raw, close_suffix)
        close_24 = parse_time(close_raw)
        if open_24 and close_24:
            specs.append({
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": DAY_MAP.get(short_day, short_day),
                "opens": open_24,
                "closes": close_24,
            })
    return specs or None


def extract_geo_by_position(html: str):
    matches = re.findall(
        r'<section class="restaurant-section"[^>]*data-map-name="(\d+)\.[^"]*"[^>]*data-map-lat="([^"]+)"[^>]*data-map-lng="([^"]+)"',
        html,
    )
    geo = {}
    for pos, lat, lng in matches:
        try:
            geo[int(pos)] = {"latitude": float(lat), "longitude": float(lng)}
        except ValueError:
            pass
    return geo


def extract_existing_itemlist(html: str):
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL):
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        if data.get("@type") == "ItemList":
            return data
    return None


def index_existing_items(existing_itemlist: dict | None):
    by_position = {}
    by_name = {}
    for entry in (existing_itemlist or {}).get("itemListElement", []):
        if not isinstance(entry, dict):
            continue
        pos = entry.get("position")
        item = entry.get("item") or {}
        name = item.get("name")
        if pos is not None:
            by_position[pos] = entry
        if name:
            by_name[name] = entry
    return by_position, by_name


def merge_item_object(existing_obj: dict | None, new_obj: dict):
    merged = dict(existing_obj or {})

    # Keep existing rich Google Places / JSON-LD fields. Add priceRange from
    # SerpAPI when present, plus any non-conflicting fields the old schema lacks.
    for key, value in new_obj.items():
        if value in (None, "", [], {}):
            continue
        if key == "priceRange":
            merged[key] = value
        elif key not in merged:
            merged[key] = value

    # Preserve sameAs as a de-duped union if both exist.
    existing_same_as = merged.get("sameAs") or []
    new_same_as = new_obj.get("sameAs") or []
    if existing_same_as or new_same_as:
        merged["sameAs"] = list(dict.fromkeys([*existing_same_as, *new_same_as]))

    return merged


def build_itemlist_schema(page_slug: str, page_data: dict, html: str):
    geo_by_position = extract_geo_by_position(html)
    existing_itemlist = extract_existing_itemlist(html)
    existing_by_position, existing_by_name = index_existing_items(existing_itemlist)
    items = []
    title = page_data.get("title", "")
    category = page_data.get("category", "")

    for idx, place in enumerate(page_data.get("places", []), start=1):
        position = place.get("position", idx)
        tags = place.get("cuisineTags") or []
        place_type = infer_place_type(page_slug, title, category, tags, place.get("name", ""))
        obj = {
            "@type": place_type,
            "name": place["name"],
        }

        if tags and place_type in {"Restaurant", "CafeOrCoffeeShop", "BarOrPub"}:
            obj["servesCuisine"] = ", ".join(tags)
        elif tags:
            obj["additionalType"] = "https://schema.org/" + tags[0].replace(" ", "")

        address = place.get("address")
        if address:
            obj["address"] = {
                "@type": "PostalAddress",
                "addressLocality": address,
            }

        # Recover country code from page-level map query; keep addressLocality-only if unknown.
        country_code = None
        map_query_match = re.search(r'data-map-query="[^"]*?,\s*([A-Z]{2})"', html)
        if map_query_match:
            country_code = map_query_match.group(1)
        if country_code and "address" in obj:
            obj["address"]["addressCountry"] = country_code

        price_range = clean_price(place.get("priceRange"))
        if price_range:
            obj["priceRange"] = price_range

        rating = place.get("googleRating")
        reviews = place.get("reviewCount")
        if rating and reviews:
            obj["aggregateRating"] = {
                "@type": "AggregateRating",
                "ratingValue": rating,
                "reviewCount": reviews,
            }

        specs = opening_hours_spec(place.get("openingHours"))
        if specs:
            obj["openingHoursSpecification"] = specs

        if place.get("phone"):
            obj["telephone"] = place["phone"]
        if place.get("photo"):
            obj["image"] = place["photo"]
        if place.get("website"):
            obj["url"] = place["website"]
        if place.get("googleMapsUrl"):
            obj["hasMap"] = place["googleMapsUrl"]

        same_as = [u for u in [place.get("website"), place.get("googleMapsUrl")] if u]
        if same_as:
            obj["sameAs"] = same_as

        geo = geo_by_position.get(position)
        if geo:
            obj["geo"] = {"@type": "GeoCoordinates", **geo}

        existing_entry = existing_by_position.get(position) or existing_by_name.get(place["name"])
        existing_item = (existing_entry or {}).get("item") or {}
        existing_url = (existing_entry or {}).get("url")
        merged_item = merge_item_object(existing_item, obj)

        items.append({
            "@type": "ListItem",
            "position": position,
            "url": existing_url or f"{page_data['url']}#" + re.sub(r'[^a-z0-9]+', '-', place['name'].lower()).strip('-'),
            "item": merged_item,
        })

    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": title,
        "description": page_data.get("description", ""),
        "url": page_data.get("url", ""),
        "numberOfItems": page_data.get("placeCount", len(items)),
        "itemListOrder": (existing_itemlist or {}).get("itemListOrder") or "https://schema.org/ItemListOrderAscending",
        "itemListElement": items,
    }


def replace_itemlist_block(html: str, new_schema: dict):
    """Replace the ItemList ld+json block without touching other schema blocks.

    The old approach used a single regex with re.DOTALL and a greedy-style
    pattern that could span across multiple <script> tags — when the Article
    block appeared before the ItemList block, the regex matched from the
    Article's <script> open tag all the way to the ItemList's </script>,
    swallowing both blocks and deleting Article schema entirely.

    Fix: match every ld+json block individually with lazy .*? (safe because
    JSON-LD never contains </script>), parse each one, and only replace the
    block whose @type is "ItemList".
    """
    replacement_json = json.dumps(new_schema, indent=2, ensure_ascii=False)

    def replacer(m):
        try:
            data = json.loads(m.group(1))
            if data.get("@type") == "ItemList":
                return f'<script type="application/ld+json">{replacement_json}</script>'
        except (json.JSONDecodeError, KeyError):
            pass
        return m.group(0)

    pattern = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL)
    return pattern.sub(replacer, html)


def maybe_add_speakable_to_article(html: str):
    if '"speakable"' in html:
        return html

    def replacer(m):
        try:
            data = json.loads(m.group(1))
            if data.get("@type") == "Article":
                data["speakable"] = {
                    "@type": "SpeakableSpecification",
                    "cssSelector": [".hero h1", ".hero .subtitle", ".quick-answer-section", ".faq-section"],
                }
                return f'<script type="application/ld+json">{json.dumps(data, indent=2, ensure_ascii=False)}</script>'
        except (json.JSONDecodeError, KeyError):
            pass
        return m.group(0)

    pattern = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL)
    return pattern.sub(replacer, html)


def main():
    changed = 0
    skipped_invalid = 0
    for api_file in sorted(API_DIR.glob('*.json')):
        slug = api_file.stem
        html_file = PP_DIR / slug / 'index.html'
        if not html_file.exists():
            continue
        try:
            page_data = json.loads(api_file.read_text())
        except json.JSONDecodeError as exc:
            skipped_invalid += 1
            print(f'skipped {slug}: invalid api json ({exc})')
            continue
        html = html_file.read_text()
        updated = replace_itemlist_block(html, build_itemlist_schema(slug, page_data, html))
        updated = maybe_add_speakable_to_article(updated)
        if updated != html:
            html_file.write_text(updated)
            changed += 1
            print(f'updated {slug}')
    print(f'changed {changed} pages; skipped invalid api json: {skipped_invalid}')


if __name__ == '__main__':
    main()
