#!/usr/bin/env python3
"""
Focused SerpAPI enrichment: only fetch Google ratings, review counts,
phone, website, and hours for places missing googleRating.

Usage:
  python3 scripts/enrich-ratings-only.py --limit 100 --dry-run
  python3 scripts/enrich-ratings-only.py --limit 100
"""

import json, os, re, subprocess, sys, time, urllib.parse, urllib.request
from pathlib import Path
from datetime import datetime, timezone

REPO = Path(__file__).resolve().parents[1]
DATA_DIR = REPO / "popular-picks-data"
API_DIR = REPO / "api" / "v1" / "picks"
PROGRESS_PATH = Path("/tmp/enrich-ratings-progress.json")
REQUEST_DELAY = 0.3


def get_key(name):
    return subprocess.run(
        ['security', 'find-generic-password', '-s', name, '-w'],
        capture_output=True, text=True
    ).stdout.strip()


SERPAPI_KEY = os.environ.get("SERPAPI_KEY") or get_key('serpapi-key')
if not SERPAPI_KEY:
    print("ERROR: No SerpAPI key found. Set SERPAPI_KEY env var or add to Keychain as 'serpapi-key'.")
    sys.exit(1)


def serpapi_maps_search(query):
    params = urllib.parse.urlencode({
        'engine': 'google_maps',
        'q': query,
        'api_key': SERPAPI_KEY,
        'hl': 'en',
        'type': 'search'
    })
    try:
        req = urllib.request.Request(f'https://serpapi.com/search.json?{params}')
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            return data.get('local_results', [])
    except Exception as e:
        print(f"      SerpAPI error: {e}")
        return []


def serpapi_google_search(query):
    params = urllib.parse.urlencode({
        'engine': 'google',
        'q': query,
        'api_key': SERPAPI_KEY,
        'hl': 'en',
    })
    try:
        req = urllib.request.Request(f'https://serpapi.com/search.json?{params}')
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except:
        return {}


def format_hours(hours_dict):
    if not hours_dict or not isinstance(hours_dict, dict):
        return None
    parts = []
    for day, times in hours_dict.items():
        if isinstance(times, list):
            parts.append(f"{day}: {', '.join(times)}")
        elif isinstance(times, str):
            parts.append(f"{day}: {times}")
    return "; ".join(parts) if parts else None


def enrich_place(place, city):
    """Enrich a single place with SerpAPI data. Returns True if enriched."""
    name = place['name']

    # Try Google Maps first
    results = serpapi_maps_search(f"{name} {city}")
    if results:
        r = results[0]
        enriched = False
        if not place.get('googleRating') and r.get('rating'):
            place['googleRating'] = r['rating']
            place['reviewCount'] = r.get('reviews')
            enriched = True
        if not place.get('phone') and r.get('phone'):
            place['phone'] = r['phone']
            enriched = True
        if not place.get('website') and r.get('website'):
            place['website'] = r['website']
            enriched = True
        if not place.get('hoursNote'):
            hrs = format_hours(r.get('operating_hours') or r.get('hours'))
            if hrs:
                place['hoursNote'] = hrs
                enriched = True
        time.sleep(REQUEST_DELAY)
        return enriched

    time.sleep(REQUEST_DELAY)

    # Fallback to regular Google search
    result = serpapi_google_search(f"{name} {city} rating")
    kg = result.get('knowledge_graph', {})
    if kg:
        enriched = False
        if not place.get('googleRating') and kg.get('rating'):
            place['googleRating'] = kg['rating']
            place['reviewCount'] = kg.get('review_count')
            enriched = True
        if not place.get('phone') and kg.get('phone'):
            place['phone'] = kg['phone']
            enriched = True
        if not place.get('website') and kg.get('website'):
            place['website'] = kg['website']
            enriched = True
        time.sleep(REQUEST_DELAY)
        return enriched

    time.sleep(REQUEST_DELAY)
    return False


def city_from_slug(slug):
    """Extract city name from slug like 'tokyo-morning-markets' -> 'Tokyo'."""
    # Common multi-word city prefixes
    multi_word = [
        'abu-dhabi', 'addis-ababa', 'buenos-aires', 'cape-town', 'chiang-mai',
        'chiang-rai', 'da-nang', 'dar-es-salaam', 'el-nido', 'ho-chi-minh',
        'hong-kong', 'koh-lanta', 'koh-phangan', 'koh-samui', 'kuala-lumpur',
        'la-paz', 'las-vegas', 'los-angeles', 'mexico-city', 'new-orleans',
        'new-york', 'nusa-penida', 'playa-del-carmen', 'porto-alegre',
        'rio-de-janeiro', 'salt-lake-city', 'san-antonio', 'san-diego',
        'san-francisco', 'san-jose', 'san-juan', 'san-miguel', 'san-sebastian',
        'santa-fe', 'sao-paulo', 'sri-lanka', 'st-louis', 'stone-town',
        'tel-aviv', 'white-plains',
    ]
    for prefix in sorted(multi_word, key=len, reverse=True):
        if slug.startswith(prefix + '-'):
            return prefix.replace('-', ' ').title()
    # Single word city = first segment
    parts = slug.split('-')
    return parts[0].title()


def load_progress():
    if PROGRESS_PATH.exists():
        return json.loads(PROGRESS_PATH.read_text())
    return {"completed": [], "failed": []}


def save_progress(progress):
    PROGRESS_PATH.write_text(json.dumps(progress, indent=2))


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Enrich top N pages with Google ratings via SerpAPI")
    parser.add_argument('--limit', type=int, default=100, help='Max pages to process')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    progress = load_progress()
    completed_set = set(progress['completed'])

    # Collect pages needing rating enrichment, sorted by most missing
    work = []
    for f in sorted(DATA_DIR.glob('*.json')):
        if ' 2.' in f.name:
            continue
        try:
            data = json.loads(f.read_text())
        except:
            continue
        if data.get('pageType') != 'popular-picks':
            continue
        picks = data.get('picks', [])
        if not picks:
            continue
        slug = data['slug']
        if slug in completed_set:
            continue

        missing_count = sum(1 for p in picks if not p.get('googleRating'))
        if missing_count > 0:
            work.append((f, data, missing_count))

    # Sort: pages with ALL places missing first (most value per page)
    work.sort(key=lambda x: (-x[2], x[1]['slug']))
    work = work[:args.limit]

    total_places = sum(w[2] for w in work)
    print(f"{'DRY RUN — ' if args.dry_run else ''}Processing {len(work)} pages ({total_places} places to enrich)\n")

    total_enriched = 0
    total_api_calls = 0
    pages_done = 0

    for i, (path, data, missing) in enumerate(work):
        slug = data['slug']
        city = data.get('taxonomy', {}).get('city', '') or city_from_slug(slug)
        picks = data['picks']
        print(f"[{i+1}/{len(work)}] {slug} — {missing} places missing ratings (city: {city})")

        if args.dry_run:
            for p in picks:
                if not p.get('googleRating'):
                    print(f"    WOULD_ENRICH: {p['name']}")
            continue

        page_enriched = 0
        for p in picks:
            if not p.get('googleRating'):
                total_api_calls += 1
                if enrich_place(p, city):
                    page_enriched += 1
                    rating = p.get('googleRating', '?')
                    reviews = p.get('reviewCount', '?')
                    print(f"    ✅ {p['name']}: {rating}★ ({reviews} reviews)")
                else:
                    print(f"    ⚠️  {p['name']}: no data found")

        total_enriched += page_enriched
        pages_done += 1

        # Save enriched data
        if page_enriched > 0:
            data['seo']['modifiedTime'] = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00Z")
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')

            # Also update api/v1/picks if it exists
            api_path = API_DIR / f"{slug}.json"
            if api_path.exists():
                try:
                    api_data = json.loads(api_path.read_text())
                    places = api_data.get('places', [])
                    for pick in picks:
                        for place in places:
                            if place.get('name') == pick['name']:
                                if pick.get('googleRating'):
                                    place['googleRating'] = pick['googleRating']
                                    place['reviewCount'] = pick.get('reviewCount')
                                if pick.get('phone') and not place.get('phone'):
                                    place['phone'] = pick['phone']
                                if pick.get('website') and not place.get('website'):
                                    place['website'] = pick['website']
                                break
                    api_path.write_text(json.dumps(api_data, indent=2, ensure_ascii=False) + '\n')
                except:
                    pass

        progress['completed'].append(slug)
        save_progress(progress)
        print(f"    → {page_enriched}/{missing} enriched\n")

    print(f"\n{'DRY RUN ' if args.dry_run else ''}DONE: {total_enriched} places enriched across {pages_done} pages ({total_api_calls} API calls)")


if __name__ == '__main__':
    main()
