#!/usr/bin/env python3
"""Batch-enrich popular-picks JSON picks with latitude/longitude via Google Places API.

Usage:
  GOOGLE_PLACES_API_KEY=... python3 generators/popular-picks/enrich-coordinates.py
  python3 generators/popular-picks/enrich-coordinates.py --slug paris-jazz-clubs
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import ssl

REQUEST_DELAY = 0.12
PLACES_API_URL = 'https://places.googleapis.com/v1/places:searchText'
FIELD_MASK = ','.join([
    'places.id',
    'places.displayName',
    'places.formattedAddress',
    'places.googleMapsUri',
    'places.location',
])


def load_api_key():
    api_key = os.environ.get('GOOGLE_PLACES_API_KEY')
    if api_key:
        return api_key
    try:
        return subprocess.check_output(
            ['security', 'find-generic-password', '-s', 'google-places-api-key', '-w'],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        print('ERROR: No Google Places API key found. Set GOOGLE_PLACES_API_KEY or add to keychain.', file=sys.stderr)
        sys.exit(1)


API_KEY = load_api_key()
SSL_CONTEXT = ssl._create_unverified_context()


def search_place(text_query):
    body = json.dumps({'textQuery': text_query, 'maxResultCount': 1}).encode()
    req = Request(
        PLACES_API_URL,
        data=body,
        method='POST',
        headers={
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': API_KEY,
            'X-Goog-FieldMask': FIELD_MASK,
        },
    )
    try:
        with urlopen(req, timeout=20, context=SSL_CONTEXT) as resp:
            data = json.loads(resp.read())
            places = data.get('places', [])
            return places[0] if places else None
    except HTTPError as e:
        body = e.read().decode() if e.fp else ''
        print(f'  API error ({e.code}): {body[:300]}', file=sys.stderr)
        return None
    except Exception as e:
        print(f'  Request error: {e}', file=sys.stderr)
        return None


def build_queries(data, pick):
    country = data.get('taxonomy', {}).get('country') or data.get('taxonomy', {}).get('countryCode') or ''
    city = data.get('taxonomy', {}).get('city') or ''
    neighborhood = pick.get('neighborhood') or ''
    address = pick.get('address') or ''
    queries = []

    primary = ', '.join(part for part in [pick.get('name', ''), address, city, country] if part)
    if primary:
        queries.append(primary)

    secondary = ', '.join(part for part in [pick.get('name', ''), neighborhood, city, country] if part)
    if secondary and secondary not in queries:
        queries.append(secondary)

    fallback = ', '.join(part for part in [pick.get('name', ''), city, country] if part)
    if fallback and fallback not in queries:
        queries.append(fallback)

    return queries


def enrich_file(path, dry_run=False):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    changed = False
    found = skipped = missing = 0

    print(f'\n{path.name}')
    for pick in data.get('picks', []):
        if pick.get('lat') is not None and pick.get('lng') is not None:
            skipped += 1
            continue

        place = None
        used_query = None
        for query in build_queries(data, pick):
            used_query = query
            place = search_place(query)
            time.sleep(REQUEST_DELAY)
            if place and place.get('location', {}).get('latitude') is not None and place.get('location', {}).get('longitude') is not None:
                break

        if place and place.get('location', {}).get('latitude') is not None and place.get('location', {}).get('longitude') is not None:
            pick['lat'] = place['location']['latitude']
            pick['lng'] = place['location']['longitude']
            if place.get('googleMapsUri') and not pick.get('googleMapsUrl'):
                pick['googleMapsUrl'] = place['googleMapsUri']
            changed = True
            found += 1
            print(f"  ✓ #{pick.get('rank')} {pick.get('name')} -> {pick['lat']:.6f}, {pick['lng']:.6f} [{used_query}]")
        else:
            missing += 1
            print(f"  ! #{pick.get('rank')} {pick.get('name')} -> no coordinate match")

    if changed and not dry_run:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write('\n')

    print(f'  Summary: found={found} skipped={skipped} missing={missing} changed={changed}')
    return changed, found, skipped, missing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--slug')
    parser.add_argument('--limit', type=int)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    files = sorted((repo_root / 'popular-picks-data').glob('*.json'))
    if args.slug:
        files = [p for p in files if p.stem == args.slug]
    if args.limit:
        files = files[:args.limit]
    if not files:
        print('No files selected.', file=sys.stderr)
        sys.exit(1)

    totals = {'changed_files': 0, 'found': 0, 'skipped': 0, 'missing': 0}
    for path in files:
        changed, found, skipped, missing = enrich_file(path, dry_run=args.dry_run)
        totals['changed_files'] += int(changed)
        totals['found'] += found
        totals['skipped'] += skipped
        totals['missing'] += missing

    print('\nDone: ' + ', '.join(f'{k}={v}' for k, v in totals.items()))


if __name__ == '__main__':
    main()
