#!/usr/bin/env python3
"""
Batch enrichment for all popular-picks pages.

Phase 1: Fix summary, hero dek, ratings, hours, websites via SerpAPI + LLM
Phase 2: Fix missing/duplicate photos via SerpAPI image search

Usage:
  python3 scripts/enrich-popular-picks-batch.py --phase 1          # Data enrichment
  python3 scripts/enrich-popular-picks-batch.py --phase 2          # Photo fix
  python3 scripts/enrich-popular-picks-batch.py --phase 1 --dry-run
  python3 scripts/enrich-popular-picks-batch.py --phase 1 --slug tokyo-ramen
  python3 scripts/enrich-popular-picks-batch.py --phase 1 --limit 10
"""

import json
import os
import re
import subprocess
import sys
import time
import tempfile
import base64
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from datetime import datetime, timezone

REPO = Path(__file__).resolve().parents[1]
DATA_DIR = REPO / "popular-picks-data"
PROGRESS_PATH = Path("/tmp/enrich-pp-progress.json")

R2_ACCOUNT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"
R2_BASE = f"https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects"
IMG_CDN = "https://img.tabiji.ai"


def get_key(name):
    return subprocess.run(
        ['security', 'find-generic-password', '-s', name, '-w'],
        capture_output=True, text=True
    ).stdout.strip()


SERPAPI_KEY = os.environ.get("SERPAPI_KEY") or get_key('serpapi-key') or '3d4b51ea3336e8eb9c73d5a3a28594bf11ec8d9219655903acf9719a6711f639'
R2_TOKEN = get_key('cloudflare-api-token')
GEMINI_KEY = os.environ.get("GEMINI_KEY") or get_key("gemini-api-key")
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_KEY}"


def call_gemini(prompt, max_retries=3, json_mode=True):
    """Call Gemini and return text response."""
    config = {"temperature": 0.7, "maxOutputTokens": 2048}
    if json_mode:
        config["responseMimeType"] = "application/json"

    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": config
    })

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(GEMINI_URL, data=body.encode(),
                headers={"Content-Type": "application/json"})
            resp = urllib.request.urlopen(req, timeout=60)
            result = json.loads(resp.read())
            text = result['candidates'][0]['content']['parts'][0]['text']
            text = re.sub(r'^```json\s*', '', text.strip())
            text = re.sub(r'\s*```$', '', text.strip())
            return text
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 2 + attempt * 3
                print(f"      Gemini retry {attempt+1}: {e} (waiting {wait}s)")
                time.sleep(wait)
            else:
                raise


def serpapi_maps_search(query):
    """Search Google Maps via SerpAPI."""
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
    except:
        return []


def serpapi_google_search(query):
    """Regular Google search for knowledge graph data."""
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
    """Convert SerpAPI hours dict to our string format."""
    if not hours_dict or not isinstance(hours_dict, dict):
        return None
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day_abbr = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    parts = []
    for day, abbr in zip(days, day_abbr):
        val = hours_dict.get(day, '')
        if isinstance(val, dict):
            opens = val.get('opens', '')
            closes = val.get('closes', '')
            if opens == 'Closed' or closes == 'Closed':
                parts.append(f"{abbr}: Closed")
            elif opens and closes:
                parts.append(f"{abbr}: {opens} – {closes}")
        elif isinstance(val, str):
            parts.append(f"{abbr}: {val}")
    return '; '.join(parts) if parts else None


# ==================== PHASE 1: Data enrichment ====================

def generate_hero_dek(data):
    """Generate a hero dek (subtitle) from page data."""
    title = data.get('seo', {}).get('h1', '')
    city = data.get('taxonomy', {}).get('city', '')
    category = data.get('taxonomy', {}).get('category', '')
    num_picks = len(data.get('picks', []))

    prompt = f"""Write a one-sentence subtitle (dek) for a travel guide page titled "{title}" about {city}.
The page has {num_picks} picks. Category: {category}.

Requirements:
- 15-25 words max
- Mention "Reddit" or "Reddit-backed" naturally
- Include the city name
- Hint at what makes this guide unique
- No quotes around the output

Output ONLY the subtitle text as a JSON string: {{"dek": "your subtitle here"}}"""

    try:
        text = call_gemini(prompt)
        result = json.loads(text)
        return result.get('dek', '')
    except:
        # Fallback template
        return f"Reddit-backed guide to {num_picks} top picks in {city} — curated from real traveler recommendations."


def generate_summary(data):
    """Generate summary fields from pick data."""
    picks = data.get('picks', [])
    if not picks:
        return {}

    # Find best overall (highest rated or #1 ranked)
    rated = [p for p in picks if p.get('googleRating')]
    best_overall = None
    if rated:
        top = max(rated, key=lambda p: (p['googleRating'], p.get('reviewCount', 0)))
        best_overall = f"{top['name']} — {top['googleRating']}★"
        if top.get('reviewCount'):
            best_overall += f" ({top['reviewCount']:,} reviews)"
    elif picks:
        best_overall = picks[0]['name']

    # Price range
    prices = [p.get('priceRangeLocal') for p in picks if p.get('priceRangeLocal')]
    price_range = prices[0] if len(prices) == 1 else None
    if len(prices) > 1:
        price_range = f"{prices[0].split('–')[0] if '–' in prices[0] else prices[0]} – {prices[-1].split('–')[-1] if '–' in prices[-1] else prices[-1]}"

    # Budget option (lowest priced with rating)
    budget = None
    for p in picks:
        pr = p.get('priceRangeLocal', '')
        if pr and p.get('googleRating'):
            budget = f"{p['name']} — from {pr.split('–')[0] if '–' in pr else pr}"
            break

    top_pick = picks[0]['name'] if picks else None

    return {
        'bestOverall': best_overall,
        'topPick': top_pick,
        'priceRangeLocal': price_range,
        'totalOptions': len(picks),
    }


def enrich_picks_serpapi(picks, city, category):
    """Enrich picks missing ratings/hours/website via SerpAPI. Returns count of enriched picks."""
    enriched = 0
    for pick in picks:
        needs = []
        if not pick.get('googleRating'):
            needs.append('rating')
        if not pick.get('hoursNote'):
            needs.append('hours')
        if not pick.get('website'):
            needs.append('website')
        if not pick.get('phone'):
            needs.append('phone')

        if not needs:
            continue

        name = pick['name']
        # Try Google Maps first
        results = serpapi_maps_search(f"{name} {city}")
        if results:
            r = results[0]
            if 'rating' in needs and r.get('rating'):
                pick['googleRating'] = r['rating']
                pick['reviewCount'] = r.get('reviews')
            if 'phone' in needs and r.get('phone'):
                pick['phone'] = r['phone']
            if 'website' in needs and r.get('website'):
                pick['website'] = r['website']
            if 'hours' in needs:
                hrs = format_hours(r.get('operating_hours') or r.get('hours'))
                if hrs:
                    pick['hoursNote'] = hrs
            enriched += 1
            time.sleep(0.3)
            continue

        # Fallback to regular Google search
        result = serpapi_google_search(f"{name} {city} rating hours website")
        kg = result.get('knowledge_graph', {})
        if kg:
            if 'rating' in needs and kg.get('rating'):
                pick['googleRating'] = kg['rating']
                pick['reviewCount'] = kg.get('review_count')
            if 'phone' in needs and kg.get('phone'):
                pick['phone'] = kg['phone']
            if 'website' in needs and kg.get('website'):
                pick['website'] = kg['website']
            if 'hours' in needs:
                hrs = format_hours(kg.get('hours'))
                if hrs:
                    pick['hoursNote'] = hrs
            enriched += 1

        time.sleep(0.5)

    return enriched


def phase1_enrich_page(data, dry_run=False):
    """Phase 1: Enrich a single page with summary, dek, and SerpAPI data."""
    slug = data['slug']
    city = data.get('taxonomy', {}).get('city', '')
    category = data.get('taxonomy', {}).get('category', '')
    picks = data.get('picks', [])
    actions = []
    changed = False

    # 1. Hero dek
    if not data.get('hero', {}).get('dek'):
        if dry_run:
            actions.append('WOULD_ADD_DEK')
        else:
            dek = generate_hero_dek(data)
            if dek:
                data['hero']['dek'] = dek
                actions.append('ADDED_DEK')
                changed = True

    # 2. Summary
    summary = data.get('summary', {})
    if not summary.get('bestOverall') or not summary.get('priceRangeLocal'):
        if dry_run:
            actions.append('WOULD_FIX_SUMMARY')
        else:
            new_summary = generate_summary(data)
            for k, v in new_summary.items():
                if v and not summary.get(k):
                    summary[k] = v
            data['summary'] = summary
            actions.append('FIXED_SUMMARY')
            changed = True

    # 3. SerpAPI enrichment for picks
    missing_rating = sum(1 for p in picks if not p.get('googleRating'))
    missing_hours = sum(1 for p in picks if not p.get('hoursNote'))
    missing_web = sum(1 for p in picks if not p.get('website'))

    if missing_rating or missing_hours or missing_web:
        if dry_run:
            actions.append(f'WOULD_ENRICH({missing_rating}r/{missing_hours}h/{missing_web}w)')
        else:
            count = enrich_picks_serpapi(picks, city, category)
            actions.append(f'SERPAPI_ENRICHED:{count}_picks')
            if count > 0:
                changed = True

    return changed, actions


# ==================== PHASE 2: Photo enrichment ====================

def venue_slug(name):
    name = re.sub(r'\([^)]*\)', '', name).strip()
    name = re.sub(r'[^\w\s-]', '', name.lower())
    name = re.sub(r'[\s_]+', '-', name).strip('-')
    return re.sub(r'-+', '-', name)[:60]


def search_images(query, num=5):
    params = urllib.parse.urlencode({
        'engine': 'google_images', 'q': query,
        'api_key': SERPAPI_KEY, 'num': num, 'safe': 'active',
    })
    try:
        req = urllib.request.Request(f'https://serpapi.com/search.json?{params}',
            headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            results = data.get('images_results', [])
            return [{'url': r.get('original', ''), 'thumb': r.get('thumbnail', ''),
                     'width': r.get('original_width', 0), 'height': r.get('original_height', 0)}
                    for r in results
                    if r.get('original_width', 0) >= 400 and r.get('original_height', 0) >= 300][:5]
    except:
        return []


def download_image(url, output_path):
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)', 'Accept': 'image/*'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            if len(data) < 5000:
                return False
            with open(output_path, 'wb') as f:
                f.write(data)
            return True
    except:
        return False


def score_image(image_path, venue_name, category):
    """Score with Gemini Vision."""
    try:
        scored_path = image_path + '.s.jpg'
        subprocess.run(['sips', '--resampleWidth', '400', '-s', 'format', 'jpeg',
            '-s', 'formatOptions', '60', image_path, '--out', scored_path],
            capture_output=True, timeout=10)
        sf = scored_path if os.path.exists(scored_path) else image_path
        with open(sf, 'rb') as f:
            img_b64 = base64.b64encode(f.read()).decode()
        if os.path.exists(scored_path):
            os.unlink(scored_path)

        body = json.dumps({
            "contents": [{"parts": [
                {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}},
                {"text": f"Rate 1-10 for travel guide photo of '{venue_name}' ({category}). Consider quality, relevance, no watermarks. Reply ONLY a number."}
            ]}],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 10}
        })
        req = urllib.request.Request(GEMINI_URL, data=body.encode(),
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            text = result['candidates'][0]['content']['parts'][0]['text'].strip()
            m = re.search(r'(\d+)', text)
            return min(int(m.group(1)), 10) if m else 0
    except:
        return 0


def optimize_and_upload(image_path, r2_key):
    """Optimize to 800px JPEG and upload to R2."""
    opt_path = image_path + '.opt.jpg'
    subprocess.run(['sips', '--resampleWidth', '800', '-s', 'format', 'jpeg',
        '-s', 'formatOptions', '80', image_path, '--out', opt_path],
        capture_output=True, timeout=10)
    upload_path = opt_path if os.path.exists(opt_path) else image_path

    url = f"{R2_BASE}/{r2_key}"
    try:
        result = subprocess.run(
            ['curl', '-s', '-X', 'PUT', '-H', f'Authorization: Bearer {R2_TOKEN}',
             '-H', 'Content-Type: image/jpeg', '--data-binary', f'@{upload_path}', url],
            capture_output=True, text=True, timeout=30)
        resp = json.loads(result.stdout) if result.stdout else {}
        if os.path.exists(opt_path):
            os.unlink(opt_path)
        return resp.get('success', False)
    except:
        return False


def build_search_query(pick, slug, city):
    """Build an image search query based on context."""
    name = pick['name']
    slug_lower = slug.lower()
    if any(x in slug_lower for x in ['canal', 'bridge', 'church', 'rock', 'temple', 'monument', 'ruins', 'hills']):
        return f"{name} {city} landmark travel photography"
    elif any(x in slug_lower for x in ['beer', 'bar', 'pub', 'cocktail', 'mezcal', 'heurigen']):
        return f"{name} {city} bar interior"
    elif any(x in slug_lower for x in ['hotel', 'lodge', 'stays', 'hostel', 'camp', 'resort']):
        return f"{name} {city} hotel exterior"
    elif any(x in slug_lower for x in ['safari', 'cruise', 'adventure', 'sport']):
        return f"{name} {city} travel experience"
    elif any(x in slug_lower for x in ['market', 'night-market']):
        return f"{name} {city} market food stall"
    elif any(x in slug_lower for x in ['museum', 'gallery', 'art']):
        return f"{name} {city} museum"
    elif any(x in slug_lower for x in ['shopping', 'vintage', 'store']):
        return f"{name} {city} shop"
    elif any(x in slug_lower for x in ['bird', 'sanctuary', 'wildlife', 'nature']):
        return f"{name} {city} nature wildlife"
    elif any(x in slug_lower for x in ['beach', 'club']):
        return f"{name} {city} beach club"
    elif any(x in slug_lower for x in ['coffee', 'cafe']):
        return f"{name} {city} cafe coffee"
    else:
        return f"{name} {city} restaurant food"


def fix_pick_photo(pick, page_slug, city, category, tmpdir):
    """Find and upload a photo for a single pick."""
    name = pick['name']
    v_slug = venue_slug(name)
    query = build_search_query(pick, page_slug, city)

    images = search_images(query)
    if not images:
        return False

    best_score = 0
    best_path = None
    for i, img in enumerate(images[:3]):
        dl_path = os.path.join(tmpdir, f"{v_slug}-{i}.jpg")
        if not download_image(img['url'], dl_path):
            continue
        score = score_image(dl_path, name, category)
        if score > best_score:
            best_score = score
            best_path = dl_path
        time.sleep(0.3)

    # Fallback: use first downloaded image if scoring failed
    if not best_path or best_score < 3:
        import glob
        candidates = glob.glob(os.path.join(tmpdir, f"{v_slug}-*.jpg"))
        if candidates:
            best_path = candidates[0]
            best_score = 5
        else:
            return False

    r2_key = f"popular-picks/{page_slug}/{v_slug}.jpg"
    if optimize_and_upload(best_path, r2_key):
        pick['photo'] = f"{IMG_CDN}/{r2_key}"
        return True
    return False


def phase2_fix_photos(data, dry_run=False):
    """Phase 2: Fix missing and duplicate photos."""
    slug = data['slug']
    city = data.get('taxonomy', {}).get('city', '')
    category = data.get('taxonomy', {}).get('category', '')
    picks = data.get('picks', [])
    actions = []
    changed = False

    # Find picks needing photos
    needs_photo = []
    photos = {}
    for p in picks:
        photo = p.get('photo', '')
        if not photo:
            needs_photo.append(p)
        elif photo in photos:
            # Duplicate
            needs_photo.append(p)
        else:
            photos[photo] = p

    if not needs_photo:
        return False, ['PHOTOS_OK']

    if dry_run:
        return False, [f'WOULD_FIX_{len(needs_photo)}_PHOTOS']

    fixed = 0
    with tempfile.TemporaryDirectory() as tmpdir:
        for p in needs_photo:
            ok = fix_pick_photo(p, slug, city, category, tmpdir)
            if ok:
                fixed += 1
            time.sleep(1)

    actions.append(f'FIXED_{fixed}/{len(needs_photo)}_PHOTOS')
    return fixed > 0, actions


# ==================== Progress tracking ====================

def load_progress(phase):
    if PROGRESS_PATH.exists():
        data = json.loads(PROGRESS_PATH.read_text())
    else:
        data = {}
    return data.get(f'phase{phase}', {"completed": [], "failed": []})


def save_progress(phase, progress):
    if PROGRESS_PATH.exists():
        data = json.loads(PROGRESS_PATH.read_text())
    else:
        data = {}
    data[f'phase{phase}'] = progress
    PROGRESS_PATH.write_text(json.dumps(data, indent=2))


# ==================== Main ====================

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', type=int, required=True, choices=[1, 2])
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--slug', help='Process single page')
    parser.add_argument('--limit', type=int, default=0)
    args = parser.parse_args()

    progress = load_progress(args.phase)
    completed_set = set(progress['completed'])

    # Collect work
    work = []
    for f in sorted(DATA_DIR.glob('*.json')):
        data = json.loads(f.read_text())
        if data.get('pageType') != 'popular-picks':
            continue
        picks = data.get('picks', [])
        if not picks:
            continue
        slug = data['slug']
        if args.slug and slug != args.slug:
            continue
        if slug in completed_set:
            continue

        # Check if page needs work for this phase
        if args.phase == 1:
            needs_dek = not data.get('hero', {}).get('dek')
            needs_summary = not data.get('summary', {}).get('bestOverall')
            needs_serpapi = any(not p.get('googleRating') for p in picks)
            if needs_dek or needs_summary or needs_serpapi:
                work.append((f, data))
        elif args.phase == 2:
            photos = [p.get('photo', '') for p in picks]
            missing = sum(1 for ph in photos if not ph)
            dupes = len(photos) - len(set(ph for ph in photos if ph))
            if missing > 0 or dupes > 0:
                work.append((f, data))

    if args.limit:
        work = work[:args.limit]

    print(f"{'DRY RUN — ' if args.dry_run else ''}Phase {args.phase}: Processing {len(work)} pages\n")

    succeeded = 0
    failed = 0

    for i, (path, data) in enumerate(work):
        slug = data['slug']
        city = data.get('taxonomy', {}).get('city', '')
        print(f"[{i+1}/{len(work)}] {slug} ({city})")

        try:
            if args.phase == 1:
                changed, actions = phase1_enrich_page(data, dry_run=args.dry_run)
            else:
                changed, actions = phase2_fix_photos(data, dry_run=args.dry_run)

            print(f"  → {', '.join(actions)}")

            if changed and not args.dry_run:
                data['seo']['modifiedTime'] = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00Z")
                path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
                print(f"  ✅ Saved")
                progress['completed'].append(slug)
                save_progress(args.phase, progress)
                succeeded += 1
            elif not changed and not args.dry_run:
                # Mark as done even if no changes needed
                progress['completed'].append(slug)
                save_progress(args.phase, progress)
                succeeded += 1
            else:
                succeeded += 1

            time.sleep(0.5)

        except Exception as e:
            print(f"  ❌ Error: {e}")
            progress['failed'].append(slug)
            save_progress(args.phase, progress)
            failed += 1
            time.sleep(2)

    print(f"\n{'='*50}")
    print(f"{'DRY RUN ' if args.dry_run else ''}Phase {args.phase}: {succeeded} succeeded, {failed} failed")


if __name__ == '__main__':
    main()
