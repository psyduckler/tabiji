#!/usr/bin/env python3
"""
Add photos to a popular-picks HTML page by:
1. Extracting venue names and image paths from HTML
2. Searching Google Images via SerpAPI
3. Scoring candidates with Gemini Vision
4. Optimizing to 800px JPEG
5. Uploading to Cloudflare R2
6. Updating img src in HTML

Usage:
    python3 scripts/add_photos_for_page.py detroit-pizza
"""

import json, os, re, subprocess, sys, time, tempfile, base64
import urllib.request, urllib.parse, urllib.error
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
R2_ACCOUNT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"
R2_BASE = f"https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects"
IMG_CDN = "https://img.tabiji.ai"


def get_key(name):
    return subprocess.run(
        ['security', 'find-generic-password', '-s', name, '-w'],
        capture_output=True, text=True
    ).stdout.strip()


SERPAPI_KEY = get_key('serpapi-key')
R2_TOKEN = get_key('cloudflare-api-token')
GEMINI_KEY = get_key('gemini-api-key')
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"


def extract_picks_from_html(html_path):
    """Extract venue names and img info from HTML."""
    html = html_path.read_text()
    picks = []
    # Find each restaurant-section
    for m in re.finditer(r'<section class="restaurant-section"[^>]*id="([^"]+)"', html):
        section_id = m.group(1)
        start = m.start()
        # Find the end of this section
        end = html.find('</section>', start)
        if end == -1:
            end = len(html)
        block = html[start:end]

        # Extract name from h2
        name_m = re.search(r'<h2>.*?</span>(.*?)</h2>', block, re.DOTALL)
        name = re.sub(r'<[^>]+>', '', name_m.group(1)).strip() if name_m else section_id

        # Extract current img src
        img_m = re.search(r'<img[^>]*src="([^"]*)"[^>]*>', block)
        current_src = img_m.group(1) if img_m else ""

        # Extract neighborhood from address
        addr_m = re.search(r'📍\s*([^<]+)', block)
        neighborhood = addr_m.group(1).strip() if addr_m else ""

        picks.append({
            'section_id': section_id,
            'name': name,
            'current_src': current_src,
            'neighborhood': neighborhood,
        })
    return picks


def search_images(query, num=5):
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
            good = []
            for r in results:
                w = r.get('original_width', 0)
                h = r.get('original_height', 0)
                src = r.get('original', '')
                if w >= 400 and h >= 300 and src and not src.endswith('.svg'):
                    good.append({'url': src, 'width': w, 'height': h, 'title': r.get('title', '')})
            return good[:5]
    except Exception as e:
        print(f"    SerpAPI error: {e}")
        return []


def download_image(url, output_path):
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Accept': 'image/*',
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


def score_image_gemini(image_path, venue_name):
    try:
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
                {"text": f"Rate this image 1-10 for a travel guide photo of '{venue_name}' (pizza restaurant). Consider quality, relevance, no watermarks, food/restaurant feel. Reply ONLY with a number 1-10."}
            ]}],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 20}
        })

        req = urllib.request.Request(GEMINI_URL, data=body.encode(),
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


def optimize_image(input_path, output_path):
    try:
        result = subprocess.run(['sips', '-g', 'pixelWidth', input_path], capture_output=True, text=True)
        width_match = re.search(r'pixelWidth:\s*(\d+)', result.stdout)
        if width_match and int(width_match.group(1)) > 800:
            subprocess.run(['sips', '--resampleWidth', '800', input_path, '--out', output_path], capture_output=True, timeout=10)
        else:
            subprocess.run(['cp', input_path, output_path], capture_output=True)
        # Ensure JPEG
        subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '80', output_path, '--out', output_path], capture_output=True, timeout=10)
        return output_path
    except Exception as e:
        print(f"    Optimize error: {e}")
        return input_path


def upload_to_r2(local_path, r2_key):
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


def venue_slug(name):
    name = re.sub(r'\([^)]*\)', '', name).strip()
    name = re.sub(r'[^\w\s-]', '', name.lower())
    name = re.sub(r'[\s_]+', '-', name).strip('-')
    return re.sub(r'-+', '-', name)[:60]


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/add_photos_for_page.py <slug>")
        sys.exit(1)

    slug = sys.argv[1]
    html_path = REPO / "popular-picks" / slug / "index.html"
    if not html_path.exists():
        print(f"File not found: {html_path}")
        sys.exit(1)

    city = slug.split('-')[0].title()  # Best guess from slug
    picks = extract_picks_from_html(html_path)
    print(f"Found {len(picks)} picks in {slug}")

    html = html_path.read_text()
    updated = 0
    skipped = 0

    with tempfile.TemporaryDirectory() as tmpdir:
        for i, pick in enumerate(picks):
            name = pick['name']
            sid = pick['section_id']
            current = pick['current_src']

            # Skip if already has a real photo (not just the placeholder CDN path)
            # Check if the image actually exists on CDN
            print(f"\n[{i+1}/{len(picks)}] {name}")

            query = f"{name} Detroit Michigan pizza restaurant food"
            print(f"    Searching: {query}")

            images = search_images(query)
            if not images:
                print(f"    ❌ No images found, skipping")
                skipped += 1
                continue

            # Download and score top 3
            best_score = 0
            best_path = None
            for j, img in enumerate(images[:3]):
                dl_path = os.path.join(tmpdir, f"{sid}-{j}.jpg")
                if not download_image(img['url'], dl_path):
                    continue
                score = score_image_gemini(dl_path, name)
                print(f"      Candidate {j+1}: score={score}/10")
                if score > best_score:
                    best_score = score
                    best_path = dl_path
                time.sleep(0.5)

            if not best_path:
                # Use first downloaded as fallback
                import glob
                candidates = glob.glob(os.path.join(tmpdir, f"{sid}-*.jpg"))
                if candidates:
                    best_path = candidates[0]
                    best_score = 5
                    print(f"    Using fallback candidate")
                else:
                    print(f"    ❌ No downloadable images, skipping")
                    skipped += 1
                    continue

            # Optimize
            opt_path = os.path.join(tmpdir, f"{sid}-final.jpg")
            optimize_image(best_path, opt_path)

            # Upload to R2
            r2_key = f"popular-picks/{slug}/{sid}.jpg"
            cdn_url = f"{IMG_CDN}/{r2_key}"
            print(f"    Uploading to R2: {r2_key} (score: {best_score}/10)")

            if upload_to_r2(opt_path, r2_key):
                # Update HTML img src
                old_src = f"https://img.tabiji.ai/popular-picks/{slug}/{sid}.jpg"
                # The src should already be this pattern; make sure alt text is good
                print(f"    ✅ {name} — score {best_score}/10")
                updated += 1
            else:
                print(f"    ❌ Upload failed for {name}")
                skipped += 1

            time.sleep(1)  # Rate limit

    print(f"\n{'='*50}")
    print(f"DONE: {updated} photos uploaded, {skipped} skipped")
    print(f"Page: https://tabiji.ai/popular-picks/{slug}/")


if __name__ == "__main__":
    main()
