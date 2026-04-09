#!/usr/bin/env python3
"""
Add photos to a compare page by:
1. Parsing compare HTML/JSON for image slots (hero grid + section images)
2. Searching Google Images via SerpAPI for iconic destination photos
3. Scoring candidates with Gemini Vision
4. Optimizing to 800px JPEG
5. Uploading to Cloudflare R2
6. Updating compare-data JSON and rebuilding HTML

Usage:
    python3 scripts/add_compare_photos.py <slug>               # Add all photos
    python3 scripts/add_compare_photos.py <slug> --hero-only   # Only hero grid photos
    python3 scripts/add_compare_photos.py <slug> --check       # Check which photos are missing
    python3 scripts/add_compare_photos.py batch <slugs.json>   # Process multiple slugs

Requires:
    - SerpAPI key in keychain (serpapi-key)
    - Cloudflare R2 token in keychain (cloudflare-api-token)
    - Gemini API key in keychain (gemini-api-key)
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

REPO_ROOT = Path(__file__).resolve().parents[1]
COMPARE_DIR = REPO_ROOT / "compare"
DATA_DIR = REPO_ROOT / "compare-data"
R2_ACCOUNT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"
R2_BASE = f"https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects"
IMG_CDN = "https://img.tabiji.ai"

# ── Credentials ──────────────────────────────────────────────────────────────

def get_key(name):
    return subprocess.run(
        ['security', 'find-generic-password', '-s', name, '-w'],
        capture_output=True, text=True
    ).stdout.strip()


SERPAPI_KEY = None
R2_TOKEN = None
GEMINI_KEY = None


def init_keys():
    global SERPAPI_KEY, R2_TOKEN, GEMINI_KEY
    SERPAPI_KEY = SERPAPI_KEY or get_key('serpapi-key')
    R2_TOKEN = R2_TOKEN or get_key('cloudflare-api-token')
    GEMINI_KEY = GEMINI_KEY or os.environ.get("GEMINI_KEY") or get_key('gemini-api-key')


# ── Image search ─────────────────────────────────────────────────────────────

def search_images(query, num=8):
    """Search Google Images via SerpAPI. Returns list of candidate dicts."""
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
        req = urllib.request.Request(url, headers={'User-Agent': 'tabiji/1.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        results = data.get('images_results', [])
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
                })
        return good[:num]
    except Exception as e:
        print(f"    SerpAPI error: {e}")
        return []


def download_image(url, output_path):
    """Download image to local path. Returns True on success."""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Accept': 'image/*,*/*',
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        if len(data) < 5000:
            return False
        with open(output_path, 'wb') as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"    Download error: {e}")
        return False


# ── Vision scoring ───────────────────────────────────────────────────────────

def score_image_gemini(image_path, description):
    """Score an image 1-10 using Gemini Vision for travel guide quality."""
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"

    try:
        # Resize for scoring payload
        scored_path = image_path + '.scored.jpg'
        subprocess.run(
            ['sips', '--resampleWidth', '400', '-s', 'format', 'jpeg',
             '-s', 'formatOptions', '60', image_path, '--out', scored_path],
            capture_output=True, timeout=10
        )
        score_file = scored_path if os.path.exists(scored_path) else image_path

        with open(score_file, 'rb') as f:
            img_b64 = base64.b64encode(f.read()).decode()
        if os.path.exists(scored_path):
            os.unlink(scored_path)

        body = json.dumps({
            "contents": [{"parts": [
                {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}},
                {"text": f"Rate this image 1-10 for a travel comparison page photo of '{description}'. "
                         f"Consider: visual quality, iconic-ness (would travelers recognize this?), "
                         f"composition, no watermarks/text overlays, scenic/editorial quality. "
                         f"Reply ONLY with a number 1-10."}
            ]}],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 20}
        })

        req = urllib.request.Request(gemini_url, data=body.encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
        text = result['candidates'][0]['content']['parts'][0]['text'].strip()
        num_match = re.search(r'(\d+)', text)
        if num_match:
            return min(int(num_match.group(1)), 10)
        return 0
    except Exception as e:
        print(f"    Vision score error: {e}")
        return 0


# ── Image optimization ───────────────────────────────────────────────────────

def optimize_image(input_path, output_path, max_width=800):
    """Resize to max_width and optimize as JPEG 80%."""
    try:
        result = subprocess.run(['sips', '-g', 'pixelWidth', input_path],
                                capture_output=True, text=True)
        width_match = re.search(r'pixelWidth:\s*(\d+)', result.stdout)
        if width_match and int(width_match.group(1)) > max_width:
            subprocess.run(['sips', '--resampleWidth', str(max_width),
                            input_path, '--out', output_path],
                           capture_output=True, timeout=10)
        else:
            subprocess.run(['cp', input_path, output_path], capture_output=True)
        subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '80',
                        output_path, '--out', output_path],
                       capture_output=True, timeout=10)
        return output_path
    except Exception as e:
        print(f"    Optimize error: {e}")
        return input_path


# ── R2 upload ────────────────────────────────────────────────────────────────

def upload_to_r2(local_path, r2_key):
    """Upload file to Cloudflare R2. Returns True on success."""
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
        print(f"    R2 upload failed: {result.stdout[:200]}")
        return False
    except Exception as e:
        print(f"    R2 upload error: {e}")
        return False


def check_r2_exists(r2_key):
    """Check if an object exists on R2. Returns True if it does."""
    url = f"{R2_BASE}/{r2_key}"
    try:
        result = subprocess.run(
            ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',
             '-H', f'Authorization: Bearer {R2_TOKEN}',
             url],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip() == '200'
    except Exception:
        return False


# ── Photo pipeline ───────────────────────────────────────────────────────────

def find_best_photo(query, description, tmpdir, prefix):
    """Search, download, score, and return the best photo path + score."""
    print(f"    Searching: {query}")
    images = search_images(query, num=6)
    if not images:
        print(f"    ❌ No images found")
        return None, 0

    best_score = 0
    best_path = None

    for j, img in enumerate(images[:4]):
        dl_path = os.path.join(tmpdir, f"{prefix}-{j}.jpg")
        if not download_image(img['url'], dl_path):
            continue
        score = score_image_gemini(dl_path, description)
        print(f"      Candidate {j+1}: score={score}/10")
        if score > best_score:
            best_score = score
            best_path = dl_path
        time.sleep(0.5)

    if not best_path:
        # Fallback: use first successfully downloaded
        import glob
        candidates = glob.glob(os.path.join(tmpdir, f"{prefix}-*.jpg"))
        if candidates:
            best_path = candidates[0]
            best_score = 3
            print(f"    Using fallback candidate")

    return best_path, best_score


def process_photo(query, description, r2_key, tmpdir, prefix):
    """Full pipeline for one photo: search → score → optimize → upload."""
    best_path, score = find_best_photo(query, description, tmpdir, prefix)
    if not best_path:
        return False

    opt_path = os.path.join(tmpdir, f"{prefix}-final.jpg")
    final_path = optimize_image(best_path, opt_path)

    print(f"    Uploading: {r2_key} (score: {score}/10)")
    success = upload_to_r2(final_path, r2_key)
    if success:
        print(f"    ✅ Uploaded")
    else:
        print(f"    ❌ Upload failed")
    return success


# ── Slug helpers ─────────────────────────────────────────────────────────────

def slug_to_names(slug):
    """Convert slug to destination names."""
    try:
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        from importlib import import_module
        mod = import_module("batch-compare-gen")
        return mod.slug_to_names(slug)
    except Exception:
        parts = slug.split('-vs-')
        if len(parts) != 2:
            raise ValueError(f"Invalid slug: {slug}")
        return tuple(p.replace('-', ' ').title() for p in parts)


def extract_section_topics(slug):
    """Extract deep-dive section topics from compare-data JSON for section images."""
    data_path = DATA_DIR / f"{slug}.json"
    if not data_path.exists():
        return []

    data = json.loads(data_path.read_text())
    topics = []
    for dd in data.get('content', {}).get('deepDiveHtml', []):
        title_match = re.search(r'<h2[^>]*>(.*?)</h2>', dd, re.S)
        if title_match:
            title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
            title = re.sub(r'^[\U00010000-\U0010ffff\u2600-\u27bf\u2702-\u27b0]+\s*', '', title).strip()
            # Skip decision framework and non-imageable sections
            if title.lower() not in ('the decision framework', 'getting around', 'cost comparison'):
                topics.append(title)
    return topics


# ── Main commands ────────────────────────────────────────────────────────────

def cmd_check(slug):
    """Check which photos are missing for a compare page."""
    init_keys()
    dest1, dest2 = slug_to_names(slug)
    r2_prefix = f"compare/{slug}"

    required = {
        f"{r2_prefix}/dest1.jpg": f"{dest1} hero photo",
        f"{r2_prefix}/dest2.jpg": f"{dest2} hero photo",
        f"{r2_prefix}/hero.jpg": "OG/social hero image",
    }

    # Add section image slots
    topics = extract_section_topics(slug)
    for i, topic in enumerate(topics[:3]):
        key = f"{r2_prefix}/section-{i+1}.jpg"
        required[key] = f"Section image: {topic}"

    print(f"Checking photos for {slug} ({dest1} vs {dest2}):")
    missing = []
    for key, desc in required.items():
        exists = check_r2_exists(key)
        status = "✅" if exists else "❌ MISSING"
        print(f"  {status} — {desc} ({IMG_CDN}/{key})")
        if not exists:
            missing.append((key, desc))

    print(f"\n{len(required) - len(missing)}/{len(required)} photos present")
    if missing:
        print(f"{len(missing)} missing — run without --check to add them")
    return missing


def cmd_add_photos(slug, hero_only=False):
    """Add photos to a compare page."""
    init_keys()
    dest1, dest2 = slug_to_names(slug)
    r2_prefix = f"compare/{slug}"

    print(f"\n{'='*60}")
    print(f"Adding photos for: {dest1} vs {dest2}")
    print(f"{'='*60}")

    uploaded = 0
    skipped = 0

    with tempfile.TemporaryDirectory() as tmpdir:
        # ── Hero photos (dest1, dest2, hero) ──
        hero_photos = [
            {
                'query': f"{dest1} travel destination iconic scenic landscape",
                'description': f"{dest1} travel destination",
                'r2_key': f"{r2_prefix}/dest1.jpg",
                'prefix': 'dest1',
            },
            {
                'query': f"{dest2} travel destination iconic scenic landscape",
                'description': f"{dest2} travel destination",
                'r2_key': f"{r2_prefix}/dest2.jpg",
                'prefix': 'dest2',
            },
        ]

        for photo in hero_photos:
            print(f"\n📷 {photo['description']}")
            if process_photo(photo['query'], photo['description'],
                             photo['r2_key'], tmpdir, photo['prefix']):
                uploaded += 1
                # Use dest1 as hero.jpg too
                if photo['prefix'] == 'dest1':
                    opt_path = os.path.join(tmpdir, 'dest1-final.jpg')
                    if os.path.exists(opt_path):
                        hero_key = f"{r2_prefix}/hero.jpg"
                        if upload_to_r2(opt_path, hero_key):
                            print(f"    ✅ Also uploaded as hero.jpg")
                            uploaded += 1
            else:
                skipped += 1
            time.sleep(1)

        # ── Section photos (dest-specific pairs) ──
        if not hero_only:
            topics = extract_section_topics(slug)
            # Pick most imageable sections
            imageable_topics = []
            for topic in topics:
                lower = topic.lower()
                if any(kw in lower for kw in ['food', 'beach', 'architecture', 'temple',
                                                'nature', 'nightlife', 'culture', 'museum',
                                                'neighborhood', 'market', 'shopping',
                                                'character', 'vibe', 'cost', 'safety']):
                    imageable_topics.append(topic)
            for topic in topics:
                if topic not in imageable_topics:
                    imageable_topics.append(topic)
            imageable_topics = imageable_topics[:5]

            # Check if we have section photo queries from rich content
            photo_queries = {}
            data_path = DATA_DIR / f"{slug}.json"
            if data_path.exists():
                import json as _json
                _data = _json.load(open(data_path))
                for sq in _data.get("richContent", {}).get("sectionPhotoQueries", []):
                    idx = sq.get("sectionIndex", -1)
                    photo_queries[idx] = sq

            for i, topic in enumerate(imageable_topics):
                # Upload dest1 image for this section
                pq = photo_queries.get(i, {})
                d1_query = pq.get("dest1Query", f"{dest1} {topic} travel scenic")
                d2_query = pq.get("dest2Query", f"{dest2} {topic} travel scenic")

                print(f"\n📷 Section {i+1}: {topic}")

                # Dest1 photo
                d1_key = f"{r2_prefix}/section-{i+1}-dest1.jpg"
                print(f"  → {dest1}")
                if process_photo(d1_query, f"{dest1} {topic}", d1_key, tmpdir, f"s{i+1}-d1"):
                    uploaded += 1
                else:
                    skipped += 1
                time.sleep(0.5)

                # Dest2 photo
                d2_key = f"{r2_prefix}/section-{i+1}-dest2.jpg"
                print(f"  → {dest2}")
                if process_photo(d2_query, f"{dest2} {topic}", d2_key, tmpdir, f"s{i+1}-d2"):
                    uploaded += 1
                else:
                    skipped += 1
                time.sleep(0.5)

    print(f"\n{'='*60}")
    print(f"DONE: {uploaded} photos uploaded, {skipped} skipped")
    print(f"CDN base: {IMG_CDN}/{r2_prefix}/")
    return uploaded


def cmd_batch(slugs_file):
    """Process multiple slugs from a JSON file."""
    slugs = json.loads(Path(slugs_file).read_text())
    print(f"Processing {len(slugs)} slugs...")

    results = {'succeeded': [], 'failed': []}
    for i, slug in enumerate(slugs):
        print(f"\n[{i+1}/{len(slugs)}] {slug}")
        try:
            count = cmd_add_photos(slug)
            if count > 0:
                results['succeeded'].append(slug)
            else:
                results['failed'].append(slug)
        except Exception as e:
            print(f"  ❌ Error: {e}")
            results['failed'].append(slug)
        time.sleep(2)

    print(f"\n{'='*60}")
    print(f"Batch complete: {len(results['succeeded'])} succeeded, {len(results['failed'])} failed")
    if results['failed']:
        print(f"Failed: {json.dumps(results['failed'])}")
    return results


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == 'batch' and len(sys.argv) >= 3:
        cmd_batch(sys.argv[2])
    elif cmd == '--help':
        print(__doc__)
    else:
        slug = cmd
        if '--check' in sys.argv:
            cmd_check(slug)
        elif '--hero-only' in sys.argv:
            cmd_add_photos(slug, hero_only=True)
        else:
            cmd_add_photos(slug)


if __name__ == "__main__":
    main()
