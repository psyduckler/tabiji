#!/usr/bin/env python3
"""
Batch-fix destination photos using Unsplash API.
Runs at 50 req/hr (demo tier). Saves progress so it can be resumed.

Usage: python3 scripts/fix-destination-photos-unsplash.py
"""
import json, glob, os, time, urllib.request, urllib.parse, sys

API_KEY = "BCCK9bkNIOgkZULC_K5FYLHluSH_ro4T1MPD1pQbjWk"
DEST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'api', 'v1', 'destinations')
PROGRESS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts', 'unsplash-photo-progress.json')

def search_unsplash(query):
    """Search Unsplash for a landscape photo matching the query."""
    url = f"https://api.unsplash.com/search/photos?query={urllib.parse.quote(query)}&per_page=1&orientation=landscape"
    req = urllib.request.Request(url, headers={"Authorization": f"Client-ID {API_KEY}"})
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read())
        remaining = int(resp.headers.get('X-Ratelimit-Remaining', 0))
        if data['results']:
            photo = data['results'][0]
            # Use the "regular" size (1080px wide)
            return photo['urls']['regular'], photo['user']['name'], remaining
        return None, None, remaining
    except Exception as e:
        print(f"  Error: {e}", file=sys.stderr)
        return None, None, 0

def main():
    # Load progress
    done = set()
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            done = set(json.load(f))
    
    # Find all placeholder destinations
    todo = []
    for f in sorted(glob.glob(os.path.join(DEST_DIR, '*.json'))):
        slug = os.path.basename(f).replace('.json', '')
        if slug in done:
            continue
        with open(f) as fh:
            d = json.load(fh)
        if 'owl-logo' in d.get('photo', ''):
            todo.append((f, d))
    
    print(f"Already done: {len(done)}")
    print(f"Remaining: {len(todo)}")
    
    fixed = 0
    failed = 0
    
    for i, (filepath, dest) in enumerate(todo):
        name = dest.get('name', '')
        country = dest.get('country', '')
        slug = dest.get('slug', '')
        
        query = f"{name} {country} travel landscape" if country else f"{name} travel landscape"
        photo_url, photographer, remaining = search_unsplash(query)
        
        if photo_url:
            dest['photo'] = photo_url
            dest['photoCredit'] = photographer
            with open(filepath, 'w') as fh:
                json.dump(dest, fh, indent=2, ensure_ascii=False)
            fixed += 1
            print(f"  ✅ {name} ({country}) → {photographer} [remaining: {remaining}]")
        else:
            failed += 1
            print(f"  ❌ {name} ({country}) — no results")
        
        done.add(slug)
        
        # Save progress every 10
        if (i + 1) % 10 == 0:
            with open(PROGRESS_FILE, 'w') as f:
                json.dump(list(done), f)
            print(f"  Progress saved: {len(done)} done, {fixed} fixed, {failed} failed")
        
        # Rate limiting: 50/hr = 1 every 72 seconds. Use 75s to be safe.
        if remaining is not None and remaining <= 2:
            print(f"  Rate limit nearly exhausted ({remaining}). Waiting 60 minutes...")
            time.sleep(3600)
        else:
            time.sleep(75)  # 50/hr = every 72 seconds
    
    # Final save
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(list(done), f)
    
    print(f"\nDone! Fixed: {fixed}, Failed: {failed}, Total processed: {len(done)}")

if __name__ == '__main__':
    main()
