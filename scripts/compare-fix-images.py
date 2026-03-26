#!/usr/bin/env python3
"""
Fix missing images for compare pages.
For each page with dest1.jpg/dest2.jpg references:
1. Search SerpAPI Google Images for each destination
2. Download best image
3. Upload to R2 as compare/{slug}/dest1.jpg, dest2.jpg, hero.jpg
4. hero.jpg = dest1 image (for og:image)

Usage:
  python3 compare-fix-images.py                    # Fix all broken pages
  python3 compare-fix-images.py --slug tokyo-vs-kyoto  # Fix one page
  python3 compare-fix-images.py --dry-run          # Just list what needs fixing
  python3 compare-fix-images.py --start 50         # Start from index 50 (resume)
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

REPO = Path(__file__).resolve().parents[1]
COMPARE_DIR = REPO / "compare"
R2_ACCOUNT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"

def get_key(name):
    return subprocess.run(
        ['security', 'find-generic-password', '-s', name, '-w'],
        capture_output=True, text=True
    ).stdout.strip()

SERPAPI_KEY = get_key('serpapi-key')
R2_TOKEN = get_key('cloudflare-pages-token')

def slug_to_names(slug):
    """Convert slug to destination names."""
    parts = slug.split('-vs-')
    if len(parts) != 2:
        return None, None
    # Quick titleize - handles most cases
    specials = {
        'ho-chi-minh': 'Ho Chi Minh City', 'st-lucia': 'St. Lucia',
        'el-calafate': 'El Calafate', 'la-paz': 'La Paz',
        'chiang-mai': 'Chiang Mai', 'buenos-aires': 'Buenos Aires',
        'mexico-city': 'Mexico City', 'rio-de-janeiro': 'Rio de Janeiro',
        'cape-town': 'Cape Town', 'da-nang': 'Da Nang', 'hoi-an': 'Hoi An',
        'lake-bled': 'Lake Bled', 'bora-bora': 'Bora Bora',
        'abu-dhabi': 'Abu Dhabi', 'addis-ababa': 'Addis Ababa',
        'cinque-terre': 'Cinque Terre', 'costa-brava': 'Costa Brava',
        'big-sur': 'Big Sur', 'napa-valley': 'Napa Valley',
        'lake-atitlan': 'Lake Atitlán', 'playa-del-carmen': 'Playa del Carmen',
        'san-miguel-de-allende': 'San Miguel de Allende',
        'turks-and-caicos': 'Turks and Caicos', 'wadi-rum': 'Wadi Rum',
        'dead-sea': 'Dead Sea', 'masai-mara': 'Masai Mara',
        'ras-al-khaimah': 'Ras Al Khaimah', 'al-ula': 'Al Ula',
        'abel-tasman': 'Abel Tasman', 'milford-sound': 'Milford Sound',
        'garden-route': 'Garden Route', 'gold-coast': 'Gold Coast',
        'byron-bay': 'Byron Bay', 'margaret-river': 'Margaret River',
        'simien-mountains': 'Simien Mountains', 'victoria-falls': 'Victoria Falls',
        'okavango-delta': 'Okavango Delta', 'fish-river-canyon': 'Fish River Canyon',
        'torres-del-paine': 'Torres del Paine', 'iguazu-falls': 'Iguazu Falls',
        'sacred-valley': 'Sacred Valley', 'colca-canyon': 'Colca Canyon',
        'faroe-islands': 'Faroe Islands', 'douro-valley': 'Douro Valley',
        'mont-blanc': 'Mont Blanc', 'sharm-el-sheikh': 'Sharm El Sheikh',
        'stone-town': 'Stone Town', 'red-sea': 'Red Sea',
        'santa-fe': 'Santa Fe', 'san-juan': 'San Juan',
        'great-barrier-reef': 'Great Barrier Reef', 'ningaloo-reef': 'Ningaloo Reef',
        'bay-of-islands': 'Bay of Islands', 'new-caledonia': 'New Caledonia',
        'south-island': 'South Island', 'blue-mountains': 'Blue Mountains',
        'hunter-valley': 'Hunter Valley', 'sunshine-coast': 'Sunshine Coast',
        'barossa-valley': 'Barossa Valley', 'kangaroo-island': 'Kangaroo Island',
        'phillip-island': 'Phillip Island', 'death-valley': 'Death Valley',
        'bocas-del-toro': 'Bocas del Toro', 'san-blas': 'San Blas Islands',
    }
    def titleize(s):
        if s in specials:
            return specials[s]
        return ' '.join(w.capitalize() for w in s.split('-'))
    return titleize(parts[0]), titleize(parts[1])


def search_destination_image(dest_name):
    """Search SerpAPI for a travel photo of the destination. Returns image URL or None."""
    import urllib.parse
    query = f"{dest_name} travel destination scenic"
    url = f"https://serpapi.com/search.json?engine=google_images&q={urllib.parse.quote(query)}&api_key={SERPAPI_KEY}&ijn=0"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'tabiji-image-bot/1.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        
        results = data.get('images_results', [])
        # Pick the first result with a reasonable size
        for img in results[:10]:
            w = img.get('original_width', 0)
            h = img.get('original_height', 0)
            orig = img.get('original', '')
            if w >= 600 and h >= 400 and orig and not orig.endswith('.svg'):
                return orig
        # Fallback to first result
        if results:
            return results[0].get('original', '')
    except Exception as e:
        print(f"  ⚠️ SerpAPI search failed for {dest_name}: {e}")
    return None


def download_image(url, local_path):
    """Download image to local path. Returns True on success."""
    try:
        Path(local_path).parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'image/*,*/*'
        })
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
            if len(data) < 5000:  # Too small, probably an error page
                return False
            with open(local_path, 'wb') as f:
                f.write(data)
            return True
    except Exception as e:
        print(f"  ⚠️ Download failed for {url}: {e}")
        return False


def upload_to_r2(local_path, r2_key):
    """Upload file to R2. Returns True on success."""
    try:
        result = subprocess.run(
            ['curl', '-s', '-X', 'PUT',
             '-H', f'Authorization: Bearer {R2_TOKEN}',
             '-H', 'Content-Type: image/jpeg',
             '--data-binary', f'@{local_path}',
             f'https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{r2_key}'],
            capture_output=True, text=True, timeout=30
        )
        resp = json.loads(result.stdout) if result.stdout else {}
        return resp.get('success', False)
    except Exception as e:
        print(f"  ⚠️ R2 upload failed for {r2_key}: {e}")
        return False


def check_r2_exists(r2_path):
    """Check if image already exists on R2 CDN."""
    try:
        req = urllib.request.Request(f"https://img.tabiji.ai/{r2_path}", method='HEAD',
            headers={'User-Agent': 'Mozilla/5.0 (tabiji-bot/1.0)'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except:
        return False


def fix_page(slug, dry_run=False):
    """Fix images for one compare page. Returns (slug, success, details)."""
    dest1, dest2 = slug_to_names(slug)
    if not dest1 or not dest2:
        return (slug, False, "invalid slug")
    
    r2_prefix = f"compare/{slug}"
    
    # Check which images are missing
    needed = {}
    for key in ['dest1.jpg', 'dest2.jpg', 'hero.jpg']:
        if not check_r2_exists(f"{r2_prefix}/{key}"):
            needed[key] = True
    
    if not needed:
        return (slug, True, "all images exist")
    
    if dry_run:
        return (slug, False, f"needs: {', '.join(needed.keys())}")
    
    print(f"  🔍 {slug}: searching images for {dest1}, {dest2}...")
    
    # Search for images
    img1_url = search_destination_image(dest1)
    time.sleep(0.3)  # Rate limit
    img2_url = search_destination_image(dest2)
    time.sleep(0.3)
    
    if not img1_url and not img2_url:
        return (slug, False, "no images found")
    
    tmpdir = Path(f"/tmp/compare-images/{slug}")
    tmpdir.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    # Download and upload dest1
    if img1_url and ('dest1.jpg' in needed or 'hero.jpg' in needed):
        local1 = tmpdir / "dest1.jpg"
        if download_image(img1_url, local1):
            if 'dest1.jpg' in needed:
                if upload_to_r2(local1, f"{r2_prefix}/dest1.jpg"):
                    results.append("dest1✅")
                else:
                    results.append("dest1❌upload")
            if 'hero.jpg' in needed:
                if upload_to_r2(local1, f"{r2_prefix}/hero.jpg"):
                    results.append("hero✅")
                else:
                    results.append("hero❌upload")
        else:
            results.append("dest1❌download")
    
    # Download and upload dest2
    if img2_url and 'dest2.jpg' in needed:
        local2 = tmpdir / "dest2.jpg"
        if download_image(img2_url, local2):
            if upload_to_r2(local2, f"{r2_prefix}/dest2.jpg"):
                results.append("dest2✅")
            else:
                results.append("dest2❌upload")
        else:
            results.append("dest2❌download")
    
    # Cleanup
    if tmpdir.exists():
        for f in tmpdir.iterdir():
            f.unlink()
        tmpdir.rmdir()
    
    success = any("✅" in r for r in results)
    return (slug, success, ", ".join(results))


def get_broken_slugs():
    """Get all compare slugs with generic dest1/dest2.jpg references."""
    slugs = []
    for d in sorted(COMPARE_DIR.iterdir()):
        if d.is_dir() and (d / "index.html").exists():
            html = (d / "index.html").read_text()
            if 'dest1.jpg' in html or 'dest2.jpg' in html:
                slugs.append(d.name)
    return slugs


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--slug', help='Fix one slug')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--start', type=int, default=0, help='Start index for resume')
    parser.add_argument('--limit', type=int, default=0, help='Max pages to process')
    args = parser.parse_args()
    
    if args.slug:
        slugs = [args.slug]
    else:
        slugs = get_broken_slugs()
    
    slugs = slugs[args.start:]
    if args.limit:
        slugs = slugs[:args.limit]
    
    total = len(slugs)
    print(f"{'[DRY RUN] ' if args.dry_run else ''}Processing {total} compare pages...")
    
    success = 0
    failed = 0
    skipped = 0
    
    for i, slug in enumerate(slugs):
        print(f"\n[{i+1}/{total}] {slug}")
        slug_name, ok, details = fix_page(slug, dry_run=args.dry_run)
        if ok:
            if "exist" in details:
                skipped += 1
            else:
                success += 1
        else:
            failed += 1
        print(f"  → {details}")
        
        # Progress report every 25
        if (i + 1) % 25 == 0:
            print(f"\n--- Progress: {i+1}/{total} | ✅ {success} | ❌ {failed} | ⏭️ {skipped} ---\n")
    
    print(f"\n{'='*50}")
    print(f"Done! ✅ {success} fixed | ❌ {failed} failed | ⏭️ {skipped} already ok")
    print(f"Total: {total}")


if __name__ == '__main__':
    main()
