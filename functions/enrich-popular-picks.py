#!/usr/bin/env python3
"""
Enrich a tabiji popular-picks page with Google Places API data.

Usage:
    python3 enrich-popular-picks.py <path-to-index.html> [--dry-run] [--report-only]
    python3 enrich-popular-picks.py --batch [--dry-run] [--report-only] [--skip-enriched]
    
Adds: Google rating badges, opening hours, contact info, direct Maps links, JSON-LD enrichment.
Outputs a JSON report of all shops with ratings (for flagging low-rated places).

Requires: GOOGLE_PLACES_API_KEY env var or reads from macOS Keychain.
"""

import json, os, re, sys, subprocess, time, html, argparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# --- Config ---
PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
if not PLACES_API_KEY:
    try:
        PLACES_API_KEY = subprocess.check_output(
            ["security", "find-generic-password", "-s", "google-places-api-key", "-w"],
            text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        print("ERROR: No Google Places API key found. Set GOOGLE_PLACES_API_KEY or add to keychain.")
        sys.exit(1)

PLACES_API_URL = "https://places.googleapis.com/v1/places:searchText"
FIELD_MASK = ",".join([
    "places.displayName", "places.formattedAddress", "places.rating",
    "places.userRatingCount", "places.currentOpeningHours.openNow",
    "places.regularOpeningHours.weekdayDescriptions", "places.websiteUri",
    "places.internationalPhoneNumber", "places.googleMapsUri", "places.id"
])

# Rate limiting
REQUEST_DELAY = 0.15  # seconds between API calls

# --- CSS to inject ---
ENRICHMENT_CSS = """
        .google-rating {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            background: #FFF8E1;
            border: 1px solid #FFE082;
            border-radius: 6px;
            padding: 0.15rem 0.5rem;
            font-size: 0.78rem;
            font-weight: 600;
            color: #F57F17;
            white-space: nowrap;
        }
        .google-rating .star { color: #F9A825; }
        .shop-hours {
            font-size: 0.82rem;
            color: #6B5B4F;
            margin-bottom: 0.75rem;
            line-height: 1.5;
        }
        .shop-hours summary {
            cursor: pointer;
            font-weight: 600;
            color: #4A3728;
        }
        .shop-hours .hours-grid {
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 0.15rem 0.75rem;
            margin-top: 0.35rem;
            padding-left: 0.25rem;
        }
        .shop-contact {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            font-size: 0.82rem;
            color: #6B5B4F;
            margin-bottom: 0.5rem;
        }
        .shop-contact a {
            color: #C75B39;
            text-decoration: none;
            font-weight: 500;
        }
        .shop-contact a:hover { text-decoration: underline; }"""


def search_place(query):
    """Search Google Places API for a single place."""
    body = json.dumps({"textQuery": query, "maxResultCount": 1}).encode()
    req = Request(PLACES_API_URL, data=body, method="POST", headers={
        "Content-Type": "application/json",
        "X-Goog-Api-Key": PLACES_API_KEY,
        "X-Goog-FieldMask": FIELD_MASK,
    })
    try:
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            places = data.get("places", [])
            return places[0] if places else None
    except HTTPError as e:
        err_body = e.read().decode() if e.fp else ""
        print(f"  API error ({e.code}): {err_body[:200]}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  Request error: {e}", file=sys.stderr)
        return None


def extract_shops(content):
    """Extract shop info from HTML content."""
    shops = []
    # Find each restaurant-section
    sections = list(re.finditer(
        r'<section class="restaurant-section" id="([^"]+)">(.*?)</section>',
        content, re.DOTALL
    ))
    
    for match in sections:
        section_id = match.group(1)
        section_html = match.group(2)
        
        # Extract shop name
        name_match = re.search(
            r'<span class="restaurant-number">\d+</span>(.+?)</h2>',
            section_html
        )
        name = name_match.group(1).strip() if name_match else None
        
        # Extract maps search link for query context
        maps_match = re.search(
            r'href="https://www\.google\.com/maps/search/([^"]+)"',
            section_html
        )
        maps_query = maps_match.group(1).replace("+", " ").replace("%26", "&") if maps_match else ""
        
        # Extract location hint from the details line
        loc_match = re.search(r'📍\s*(.+?)(?:<|$)', section_html)
        location = loc_match.group(1).strip() if loc_match else ""
        # Clean HTML entities
        location = html.unescape(re.sub(r'<[^>]+>', '', location))
        
        if name:
            shops.append({
                "section_id": section_id,
                "name": html.unescape(name),
                "maps_query": maps_query,
                "location": location,
                "start": match.start(),
                "end": match.end(),
                "full_match": match.group(0),
            })
    
    return shops


def build_search_query(shop):
    """Build a good Places API search query from shop info."""
    name = shop["name"]
    location = shop["location"]
    
    # Use the maps query if it has useful location context, otherwise build from name + location
    if shop["maps_query"]:
        return shop["maps_query"]
    
    # Fallback: name + first part of location
    return f"{name} {location}"


def build_hours_html(place_data):
    """Build collapsible hours HTML from Places API data."""
    hours = place_data.get("regularOpeningHours", {}).get("weekdayDescriptions", [])
    if not hours:
        return ""
    
    open_now = place_data.get("currentOpeningHours", {}).get("openNow")
    status = "Open now" if open_now else "Closed now" if open_now is False else "Hours"
    
    grid_rows = []
    for day_str in hours:
        # Format: "Monday: 12:00 – 9:00 PM" or "Monday: Closed"
        parts = day_str.split(": ", 1)
        if len(parts) == 2:
            day_name = parts[0][:3]  # Mon, Tue, etc.
            time_str = html.escape(parts[1])
            grid_rows.append(f'            <span>{day_name}</span><span>{time_str}</span>')
        else:
            grid_rows.append(f'            <span>{html.escape(day_str)}</span><span></span>')
    
    return f"""    <div class="shop-hours">
        <details>
            <summary>🕐 {status}</summary>
            <div class="hours-grid">
{chr(10).join(grid_rows)}
            </div>
        </details>
    </div>
"""


def build_contact_html(place_data):
    """Build contact info HTML from Places API data."""
    phone = place_data.get("internationalPhoneNumber")
    website = place_data.get("websiteUri")
    
    if not phone and not website:
        return ""
    
    parts = []
    if phone:
        phone_clean = phone.replace(" ", "").replace("-", "")
        parts.append(f'<span>📞 <a href="tel:{html.escape(phone_clean)}">{html.escape(phone)}</a></span>')
    if website:
        parts.append(f'<span>🌐 <a href="{html.escape(website)}" target="_blank" rel="noopener">Website</a></span>')
    
    return f'    <div class="shop-contact">\n        {chr(10)+"        ".join(parts)}\n    </div>\n'


def build_rating_html(place_data):
    """Build rating badge HTML."""
    rating = place_data.get("rating")
    count = place_data.get("userRatingCount")
    
    if not rating:
        return ""
    
    count_str = f"{count:,}" if count else "?"
    return f'<span class="google-rating"><span class="star">★</span> {rating} · {count_str} reviews</span>'


def enrich_section(section_html, place_data):
    """Enrich a single shop section with Places API data."""
    if not place_data:
        return section_html
    
    modified = section_html
    
    # A) Add rating badge after cuisine tag
    rating_html = build_rating_html(place_data)
    if rating_html:
        # Insert after the last cuisine-tag span in the header
        modified = re.sub(
            r'(class="cuisine-tag[^"]*">[^<]+</span>)',
            rf'\1\n        {rating_html}',
            modified,
            count=1
        )
    
    # B) Replace Google Maps search link with direct link
    maps_uri = place_data.get("googleMapsUri")
    if maps_uri:
        modified = re.sub(
            r'href="https://www\.google\.com/maps/search/[^"]+"',
            f'href="{html.escape(maps_uri)}"',
            modified,
            count=1
        )
    
    # C) Add hours and contact after restaurant-details div, before img
    hours_html = build_hours_html(place_data)
    contact_html = build_contact_html(place_data)
    insert_html = hours_html + contact_html
    
    if insert_html:
        # Insert after the closing </div> of restaurant-details and before the <img
        modified = re.sub(
            r'(📌 Google Maps →</a>\s*</div>)',
            rf'\1\n{insert_html}',
            modified,
            count=1
        )
    
    return modified


def enrich_jsonld(content, shops_data):
    """Enrich JSON-LD ItemList with Places API data."""
    # Find the ItemList JSON-LD block
    jsonld_pattern = r'(<script type="application/ld\+json">\s*\{[^}]*"@type":\s*"ItemList".*?</script>)'
    match = re.search(jsonld_pattern, content, re.DOTALL)
    if not match:
        return content
    
    jsonld_block = match.group(1)
    
    for shop_name, place_data in shops_data.items():
        if not place_data:
            continue
        
        rating = place_data.get("rating")
        count = place_data.get("userRatingCount")
        phone = place_data.get("internationalPhoneNumber")
        website = place_data.get("websiteUri")
        
        # Find this shop's ListItem in the JSON-LD and add fields
        # Look for the store by name (fuzzy match)
        escaped_name = re.escape(shop_name)
        # Match the Store object for this shop
        store_pattern = rf'("name":\s*"{escaped_name}"[^}}]*?"priceRange":\s*"[^"]*")'
        store_match = re.search(store_pattern, jsonld_block)
        
        if store_match:
            original = store_match.group(1)
            additions = []
            
            if rating:
                additions.append(
                    f'"aggregateRating":{{"@type":"AggregateRating","ratingValue":{rating},"reviewCount":{count or 0},"bestRating":5}}'
                )
            if phone:
                additions.append(f'"telephone":"{phone}"')
            if website:
                additions.append(f'"url":"{website}"')
            
            if additions:
                enriched = original + "," + ",".join(additions)
                jsonld_block = jsonld_block.replace(original, enriched)
    
    content = content[:match.start()] + jsonld_block + content[match.end():]
    return content


def inject_css(content):
    """Inject enrichment CSS if not already present."""
    if "google-rating" in content:
        return content  # Already has enrichment CSS
    
    # Insert before the closing of .restaurant-details a:hover rule or any suitable point
    # Find a good insertion point in the <style> block
    insert_point = content.find(".restaurant-details a:hover { text-decoration: underline; }")
    if insert_point != -1:
        insert_after = content.find("}", insert_point) + 1
        content = content[:insert_after] + ENRICHMENT_CSS + content[insert_after:]
    else:
        # Fallback: insert before </style>
        content = content.replace("</style>", ENRICHMENT_CSS + "\n    </style>", 1)
    
    return content


def update_date_modified(content):
    """Update dateModified to today."""
    today = time.strftime("%Y-%m-%d")
    today_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Update meta tag
    content = re.sub(
        r'<meta property="article:modified_time" content="[^"]*">',
        f'<meta property="article:modified_time" content="{today_iso}">',
        content
    )
    
    # Update JSON-LD dateModified
    content = re.sub(
        r'"dateModified":\s*"[^"]*"',
        f'"dateModified": "{today}"',
        content
    )
    
    return content


def enrich_page(filepath, dry_run=False, report_only=False):
    """Enrich a single popular-picks page. Returns list of shop report dicts."""
    with open(filepath, "r") as f:
        content = f.read()
    
    # Skip if already enriched
    if "google-rating" in content and not report_only:
        print(f"  Already enriched, skipping.")
        return []
    
    shops = extract_shops(content)
    if not shops:
        print(f"  No shop sections found, skipping.")
        return []
    
    print(f"  Found {len(shops)} shops")
    
    report = []
    shops_data = {}  # name -> place_data for JSON-LD enrichment
    
    if not report_only:
        content = inject_css(content)
    
    # Process each shop
    for i, shop in enumerate(shops):
        query = build_search_query(shop)
        print(f"  [{i+1}/{len(shops)}] Searching: {shop['name']}")
        
        place_data = search_place(query)
        time.sleep(REQUEST_DELAY)
        
        if place_data:
            display_name = place_data.get("displayName", {}).get("text", "?")
            rating = place_data.get("rating", "N/A")
            count = place_data.get("userRatingCount", 0)
            print(f"    Found: {display_name} — ★ {rating} ({count} reviews)")
            
            report.append({
                "page": os.path.basename(os.path.dirname(filepath)),
                "shop_name": shop["name"],
                "google_name": display_name,
                "rating": rating,
                "review_count": count,
                "phone": place_data.get("internationalPhoneNumber"),
                "website": place_data.get("websiteUri"),
                "has_hours": bool(place_data.get("regularOpeningHours", {}).get("weekdayDescriptions")),
                "maps_uri": place_data.get("googleMapsUri"),
            })
            
            shops_data[shop["name"]] = place_data
        else:
            print(f"    Not found in API")
            report.append({
                "page": os.path.basename(os.path.dirname(filepath)),
                "shop_name": shop["name"],
                "google_name": None,
                "rating": None,
                "review_count": 0,
                "not_found": True,
            })
            shops_data[shop["name"]] = None
    
    if report_only or dry_run:
        return report
    
    # Apply enrichments to each section (process in reverse to preserve positions)
    sections = list(re.finditer(
        r'<section class="restaurant-section" id="([^"]+)">(.*?)</section>',
        content, re.DOTALL
    ))
    
    for match in reversed(sections):
        section_id = match.group(1)
        section_html = match.group(0)
        
        # Find the corresponding shop
        shop = next((s for s in shops if s["section_id"] == section_id), None)
        if shop and shops_data.get(shop["name"]):
            enriched = enrich_section(section_html, shops_data[shop["name"]])
            content = content[:match.start()] + enriched + content[match.end():]
    
    # Enrich JSON-LD
    content = enrich_jsonld(content, shops_data)
    
    # Update date
    content = update_date_modified(content)
    
    # Write back
    with open(filepath, "w") as f:
        f.write(content)
    
    print(f"  ✅ Enriched {sum(1 for v in shops_data.values() if v)} of {len(shops)} shops")
    
    return report


def main():
    parser = argparse.ArgumentParser(description="Enrich popular-picks pages with Google Places data")
    parser.add_argument("path", nargs="?", help="Path to a single index.html")
    parser.add_argument("--batch", action="store_true", help="Process all popular-picks pages")
    parser.add_argument("--dry-run", action="store_true", help="Don't write changes")
    parser.add_argument("--report-only", action="store_true", help="Only generate report, no changes")
    parser.add_argument("--skip-enriched", action="store_true", help="Skip already-enriched pages")
    parser.add_argument("--report-file", default="/tmp/places-enrichment-report.json", help="Report output path")
    parser.add_argument("--start-from", help="Start batch from this slug (alphabetical)")
    parser.add_argument("--limit", type=int, help="Max pages to process")
    args = parser.parse_args()
    
    if not args.path and not args.batch:
        parser.error("Provide a path or use --batch")
    
    all_reports = []
    
    if args.batch:
        picks_dir = os.path.expanduser("~/tabiji/popular-picks")
        pages = sorted([
            os.path.join(picks_dir, d, "index.html")
            for d in os.listdir(picks_dir)
            if os.path.isfile(os.path.join(picks_dir, d, "index.html"))
        ])
        
        # Filter to pages with actual shop sections
        pages = [p for p in pages if "restaurant-section" in open(p).read()]
        
        if args.skip_enriched:
            pages = [p for p in pages if "google-rating" not in open(p).read()]
        
        if args.start_from:
            pages = [p for p in pages if os.path.basename(os.path.dirname(p)) >= args.start_from]
        
        if args.limit:
            pages = pages[:args.limit]
        
        print(f"Processing {len(pages)} pages...")
        
        for i, page in enumerate(pages):
            slug = os.path.basename(os.path.dirname(page))
            print(f"\n[{i+1}/{len(pages)}] {slug}")
            try:
                report = enrich_page(page, dry_run=args.dry_run, report_only=args.report_only)
                all_reports.extend(report)
            except Exception as e:
                print(f"  ERROR: {e}")
                all_reports.append({
                    "page": slug,
                    "error": str(e),
                })
        
        # Git commit if not dry run
        if not args.dry_run and not args.report_only:
            print("\nCommitting changes...")
            os.system("cd ~/tabiji && git add popular-picks/ && git commit -m 'Batch enrich popular-picks with Google Places API data' && git push")
    
    else:
        filepath = os.path.expanduser(args.path)
        slug = os.path.basename(os.path.dirname(filepath))
        print(f"Processing: {slug}")
        all_reports = enrich_page(filepath, dry_run=args.dry_run, report_only=args.report_only)
    
    # Write report
    with open(args.report_file, "w") as f:
        json.dump(all_reports, f, indent=2)
    
    # Summary
    total = len(all_reports)
    found = sum(1 for r in all_reports if r.get("rating") is not None)
    not_found = sum(1 for r in all_reports if r.get("not_found"))
    low_rated = [r for r in all_reports if r.get("rating") and r["rating"] < 3.0]
    below_35 = [r for r in all_reports if r.get("rating") and r["rating"] < 3.5]
    
    print(f"\n{'='*60}")
    print(f"ENRICHMENT REPORT")
    print(f"{'='*60}")
    print(f"Total shops processed: {total}")
    print(f"Found in Google Places: {found}")
    print(f"Not found: {not_found}")
    print(f"Below 3.0 stars: {len(low_rated)}")
    print(f"Below 3.5 stars: {len(below_35)}")
    
    if low_rated:
        print(f"\n⚠️ SHOPS BELOW 3.0 STARS:")
        for r in sorted(low_rated, key=lambda x: x.get("rating", 0)):
            print(f"  ★ {r['rating']} ({r['review_count']} reviews) — {r['shop_name']} [{r['page']}]")
    
    if below_35:
        print(f"\n⚠️ SHOPS BELOW 3.5 STARS:")
        for r in sorted(below_35, key=lambda x: x.get("rating", 0)):
            print(f"  ★ {r['rating']} ({r['review_count']} reviews) — {r['shop_name']} [{r['page']}]")
    
    print(f"\nFull report: {args.report_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
