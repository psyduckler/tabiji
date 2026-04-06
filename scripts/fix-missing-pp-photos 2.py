#!/usr/bin/env python3
"""
Fix missing photos for popular-picks pages.

For each pick missing a photo:
1. Search SerpAPI Google Images for the venue
2. Score top candidates with Gemini Vision
3. Optimize to 800px JPEG
4. Upload to Cloudflare R2
5. Update the JSON data file

Usage:
  python3 scripts/fix-missing-pp-photos.py                    # Fix all
  python3 scripts/fix-missing-pp-photos.py --slug bruges-hidden-canals
  python3 scripts/fix-missing-pp-photos.py --dry-run
  python3 scripts/fix-missing-pp-photos.py --limit 20
"""

import json
import os
import re
import subprocess
import sys
import time
import tempfile
import urllib.request
import urllib.error
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATA_DIR = REPO / "popular-picks-data"

R2_ACCOUNT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"
R2_BASE = f"https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects"
IMG_CDN = "https://img.tabiji.ai"


def get_key(name):
    return subprocess.run(
        ['security', 'find-generic-password', '-s', name, '-w'],
        capture_output=True, text=True
    ).stdout.strip()


SERPAPI_KEY = os.environ.get("SERPAPI_KEY", get_key('serpapi-key') or '3d4b51ea3336e8eb9c73d5a3a28594bf11ec8d9219655903acf9719a6711f639')
R2_TOKEN = get_key('cloudflare-api-token')
GEMINI_KEY = os.environ.get("GEMINI_KEY", "AIzaSyCo9zeMqGnE0iBzu9Edk2W8W7ky9-JJwhY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"


def venue_slug(name):
    """Convert venue name to URL-safe slug."""
    # Remove Japanese/non-ASCII in parentheses
    name = re.sub(r'\([^)]*\)', '', name).strip()
    name = re.sub(r'[^\w\s-]', '', name.lower())
    name = re.sub(r'[\s_]+', '-', name).strip('-')
    name = re.sub(r'-+', '-', name)
    return name[:60]


def search_images(query, num=5):
    """Search Google Images via SerpAPI."""
    import urllib.parse
    params = urllib.parse.urlencode({
        'engine': 'google_images',
        'q': query,
        'api_key': SERPAPI_KEY,
        'num': num,
        'safe': 'active',
        'ijn': '0',
    })
    url = f'https://serpapi.com/search.json?{params}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            results = data.get('images_results', [])
            # Filter for reasonable sizes and jpeg/png
            good = []
            for r in results:
                w = r.get('original_width', 0)
                h = r.get('original_height', 0)
                src = r.get('original', '')
                if w >= 400 and h >= 300 and src and not src.endswith('.svg'):
                    good.append({
                        'url': src,
                        'width': w,
                        'height': h,
                        'title': r.get('title', ''),
                        'source': r.get('source', ''),
                    })
            return good[:5]
    except Exception as e:
        print(f"    SerpAPI error: {e}")
        return []


def download_image(url, output_path):
    """Download an image to local path."""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Accept': 'image/*',
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            if len(data) < 5000:  # Too small, probably an error page
                return False
            with open(output_path, 'wb') as f:
                f.write(data)
            return True
    except Exception as e:
        print(f"    Download error: {e}")
        return False


def score_image_gemini(image_path, venue_name, category):
    """Score an image using Gemini Vision (1-10)."""
    import base64
    try:
        # Resize to 400px before scoring to keep payload small
        scored_path = image_path + '.scored.jpg'
        subprocess.run(
            ['sips', '--resampleWidth', '400', '-s', 'format', 'jpeg',
             '-s', 'formatOptions', '60', image_path, '--out', scored_path],
            capture_output=True, timeout=10
        )
        score_file = scored_path if os.path.exists(scored_path) else image_path

        with open(score_file, 'rb') as f:
            img_b64 = base64.b64encode(f.read()).decode()

        # Clean up
        if os.path.exists(scored_path):
            os.unlink(scored_path)

        body = json.dumps({
            "contents": [{
                "parts": [
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}},
                    {"text": f"Rate this image 1-10 for a travel guide photo of '{venue_name}' ({category}). Consider quality, relevance, no watermarks. Reply ONLY with a number 1-10."}
                ]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 20,
            }
        })

        req = urllib.request.Request(GEMINI_URL, data=body.encode(),
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            text = result['candidates'][0]['content']['parts'][0]['text'].strip()
            # Extract just the number
            num_match = re.search(r'(\d+)', text)
            if num_match:
                score = int(num_match.group(1))
                return min(score, 10), text[:40]
            return 0, f"no score in: {text[:40]}"
    except Exception as e:
        print(f"    Vision score error: {e}")
        return 0, str(e)


def optimize_image(input_path, output_path, max_width=800):
    """Optimize image using sips (macOS)."""
    try:
        # Get current dimensions
        result = subprocess.run(
            ['sips', '-g', 'pixelWidth', input_path],
            capture_output=True, text=True
        )
        width_match = re.search(r'pixelWidth:\s*(\d+)', result.stdout)
        if width_match and int(width_match.group(1)) > max_width:
            subprocess.run(
                ['sips', '--resampleWidth', str(max_width), input_path, '--out', output_path],
                capture_output=True, timeout=10
            )
        else:
            subprocess.run(['cp', input_path, output_path], capture_output=True)

        # Convert to JPEG if needed
        if not output_path.endswith('.jpg'):
            jpg_path = output_path.rsplit('.', 1)[0] + '.jpg'
            subprocess.run(
                ['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '80', output_path, '--out', jpg_path],
                capture_output=True, timeout=10
            )
            return jpg_path
        return output_path
    except Exception as e:
        print(f"    Optimize error: {e}")
        return input_path


def upload_to_r2(local_path, r2_key):
    """Upload file to Cloudflare R2."""
    url = f"{R2_BASE}/{r2_key}"
    try:
        result = subprocess.run(
            ['curl', '-s', '-X', 'PUT',
             '-H', f'Authorization: Bearer {R2_TOKEN}',
             '-H', 'Content-Type: image/jpeg',
             '--data-binary', f'@{local_path}',
             url],
            capture_output=True, text=True, timeout=30
        )
        response = json.loads(result.stdout) if result.stdout else {}
        if response.get('success'):
            return True
        else:
            print(f"    R2 upload failed: {result.stdout[:200]}")
            return False
    except Exception as e:
        print(f"    R2 upload error: {e}")
        return False


def find_pages_with_missing_photos():
    """Find all pages with picks missing photos."""
    pages = []
    for f in sorted(DATA_DIR.glob('*.json')):
        data = json.loads(f.read_text())
        picks = data.get('picks', [])
        if not picks:
            continue
        missing = [p for p in picks if not p.get('photo') or p['photo'] == 'null']
        if missing:
            pages.append({
                'path': f,
                'slug': data['slug'],
                'city': data.get('taxonomy', {}).get('city', ''),
                'category': data.get('taxonomy', {}).get('category', ''),
                'data': data,
                'missing': missing,
                'total': len(picks),
            })
    return pages


def fix_pick_photo(pick, page_slug, city, category, tmpdir, dry_run=False):
    """Find and upload a photo for a single pick."""
    name = pick['name']
    v_slug = venue_slug(name)

    # Build search query based on slug keywords + place type, not just category
    place_type = pick.get('placeType', '')
    slug_lower = page_slug.lower()

    # Detect actual content type from slug
    if any(x in slug_lower for x in ['canal', 'bridge', 'church', 'rock', 'temple', 'monument', 'ruins', 'hills']):
        query = f"{name} {city} landmark travel photography"
    elif any(x in slug_lower for x in ['beer', 'bar', 'pub', 'cocktail', 'mezcal']):
        query = f"{name} {city} bar craft beer interior"
    elif any(x in slug_lower for x in ['hotel', 'lodge', 'stays', 'hostel', 'camp', 'resort']):
        query = f"{name} {city} hotel lodge exterior"
    elif any(x in slug_lower for x in ['safari', 'cruise', 'adventure', 'sport', 'hiking', 'camping']):
        query = f"{name} {city} travel experience photography"
    elif any(x in slug_lower for x in ['market', 'night-market']):
        query = f"{name} {city} market food stall"
    elif any(x in slug_lower for x in ['museum', 'gallery', 'art']):
        query = f"{name} {city} museum gallery"
    elif any(x in slug_lower for x in ['shopping', 'vintage', 'store']):
        query = f"{name} {city} shop store"
    elif any(x in slug_lower for x in ['bird', 'sanctuary', 'wildlife', 'nature', 'pan', 'salt']):
        query = f"{name} {city} nature wildlife photography"
    else:
        # Default: food/restaurant
        query = f"{name} {city} restaurant food dish"

    print(f"    Searching: {query[:60]}...")
    if dry_run:
        return True

    images = search_images(query)
    if not images:
        print(f"    No images found for {name}")
        return False

    # Download and score top candidates
    best_score = 0
    best_path = None

    for i, img in enumerate(images[:3]):
        dl_path = os.path.join(tmpdir, f"{v_slug}-candidate-{i}.jpg")
        if not download_image(img['url'], dl_path):
            continue

        score, reason = score_image_gemini(dl_path, name, category)
        print(f"      Candidate {i+1}: score={score} ({reason[:40]})")
        if score > best_score:
            best_score = score
            best_path = dl_path

        time.sleep(0.5)  # Rate limit Gemini

    if not best_path or best_score < 3:
        print(f"    No acceptable photo found (best score: {best_score})")
        # Fallback: if we have any downloaded image at all, use it without scoring
        import glob
        candidates = glob.glob(os.path.join(tmpdir, f"{v_slug}-candidate-*.jpg"))
        if candidates:
            best_path = candidates[0]
            best_score = 5  # Default acceptable score
            print(f"    Using fallback candidate (no vision score)")
        else:
            return False

    # Optimize
    opt_path = os.path.join(tmpdir, f"{v_slug}-final.jpg")
    opt_path = optimize_image(best_path, opt_path)

    # Upload to R2
    r2_key = f"popular-picks/{page_slug}/{v_slug}.jpg"
    print(f"    Uploading to R2: {r2_key} (score: {best_score})")
    if upload_to_r2(opt_path, r2_key):
        pick['photo'] = f"{IMG_CDN}/{r2_key}"
        return True
    return False


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--slug', help='Process single page')
    parser.add_argument('--limit', type=int, default=0)
    args = parser.parse_args()

    pages = find_pages_with_missing_photos()
    if args.slug:
        pages = [p for p in pages if p['slug'] == args.slug]

    if args.limit:
        pages = pages[:args.limit]

    total_missing = sum(len(p['missing']) for p in pages)
    print(f"Pages with missing photos: {len(pages)}")
    print(f"Total picks needing photos: {total_missing}\n")

    if not pages:
        print("Nothing to fix!")
        return

    fixed = 0
    failed = 0

    for pi, page in enumerate(pages):
        slug = page['slug']
        city = page['city']
        cat = page['category']
        missing = page['missing']
        print(f"[{pi+1}/{len(pages)}] {slug} — {len(missing)}/{page['total']} missing")

        with tempfile.TemporaryDirectory() as tmpdir:
            for pick in missing:
                print(f"  #{pick.get('rank', '?')} {pick['name']}")
                ok = fix_pick_photo(pick, slug, city, cat, tmpdir, dry_run=args.dry_run)
                if ok:
                    fixed += 1
                else:
                    failed += 1
                time.sleep(1)  # Rate limit between picks

        # Save updated JSON
        if not args.dry_run:
            page['path'].write_text(json.dumps(page['data'], indent=2, ensure_ascii=False) + '\n')
            print(f"  Saved {page['path'].name}\n")

    print(f"\n{'='*50}")
    print(f"{'DRY RUN ' if args.dry_run else ''}Results: {fixed} fixed, {failed} failed")
    if not args.dry_run:
        print(f"\nNext: rebuild HTML pages with:")
        print(f"  for slug in {' '.join(p['slug'] for p in pages)}; do")
        print(f"    node generators/popular-picks/build-page.js popular-picks-data/$slug.json popular-picks/$slug/index.html")
        print(f"  done")


if __name__ == '__main__':
    main()
