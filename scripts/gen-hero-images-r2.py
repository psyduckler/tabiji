#!/usr/bin/env python3
"""
Generate hero-bg.jpg images for popular-picks pages that don't have one on R2,
then upload to Cloudflare R2.

Usage:
    python3 scripts/gen-hero-images-r2.py [--dry-run] [--limit N] [--slug SLUG]
    
Reads the list of popular-picks pages, checks R2 for existing hero-bg.jpg,
generates missing ones with Gemini image generation, and uploads to R2.
"""

import json
import os
import re
import subprocess
import sys
import time
import argparse
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PP_DIR = REPO / "popular-picks"

R2_ACCOUNT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"
R2_BASE = f"https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects"
IMG_BASE = "https://img.tabiji.ai"

# Get API keys
def get_key(name):
    return subprocess.check_output(
        ["security", "find-generic-password", "-s", name, "-w"],
        text=True, stderr=subprocess.DEVNULL
    ).strip()

R2_TOKEN = get_key("cloudflare-pages-token")
GEMINI_KEY = get_key("google-api-key")

import google.generativeai as genai
genai.configure(api_key=GEMINI_KEY)

# Use imagen-3.0-generate-002 for image generation
from google import genai as genai2
client = genai2.Client(api_key=GEMINI_KEY)


def check_r2_exists(r2_key):
    """Check if an object exists on R2 by doing a HEAD request to the CDN."""
    url = f"{IMG_BASE}/{r2_key}"
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip() == "200"
    except Exception:
        return False


def extract_page_info(slug):
    """Extract city, country, category from an existing page's HTML."""
    html_path = PP_DIR / slug / "index.html"
    if not html_path.exists():
        return None
    
    html = html_path.read_text()
    
    # Extract from hero badge: "🏆 Popular Picks — City, Country"
    badge = re.search(r'Popular Picks\s*—\s*([^<"]+?)(?:,\s*([^<"]+?))?(?:<|")', html)
    city = badge.group(1).strip() if badge else slug.replace("-", " ").title()
    country = badge.group(2).strip() if badge and badge.group(2) else ""
    
    # Extract title/category from <title> or <h1>
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    title = h1.group(1).strip() if h1 else slug.replace("-", " ").title()
    title = re.sub(r'<[^>]+>', '', title)  # strip HTML tags
    
    return {"city": city, "country": country, "title": title}


def generate_hero_image(city, country, title, output_path):
    """Generate a hero image using Gemini Imagen."""
    location = f"{city}, {country}" if country else city
    
    # Create a descriptive prompt for a travel hero image
    prompt = (
        f"A beautiful, cinematic travel photograph of {location}. "
        f"The image should evoke the theme of '{title}'. "
        f"Wide landscape composition, golden hour lighting, vibrant colors, "
        f"high quality travel photography style. No text, no watermarks, no people's faces."
    )
    
    try:
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config=genai2.types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="16:9",
                output_mime_type="image/jpeg",
            )
        )
        
        if response.generated_images:
            img_data = response.generated_images[0].image.image_bytes
            with open(output_path, "wb") as f:
                f.write(img_data)
            return True
        else:
            print(f"  ⚠️ No image generated")
            return False
    except Exception as e:
        print(f"  ❌ Image gen error: {e}")
        return False


def upload_to_r2(local_path, r2_key):
    """Upload a file to Cloudflare R2."""
    url = f"{R2_BASE}/{r2_key}"
    try:
        result = subprocess.run(
            [
                "curl", "-s", "-X", "PUT",
                "-H", f"Authorization: Bearer {R2_TOKEN}",
                "-H", "Content-Type: image/jpeg",
                "--data-binary", f"@{local_path}",
                url
            ],
            capture_output=True, text=True, timeout=30
        )
        response = json.loads(result.stdout) if result.stdout else {}
        if response.get("success"):
            return True
        else:
            print(f"  ⚠️ R2 upload response: {result.stdout[:200]}")
            return False
    except Exception as e:
        print(f"  ❌ R2 upload error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--slug", help="Process single slug")
    args = parser.parse_args()
    
    if args.slug:
        slugs = [args.slug]
    else:
        # Find pages built by batch generator (have restaurant-photo divs)
        slugs = []
        for d in sorted(PP_DIR.iterdir()):
            if not d.is_dir():
                continue
            html = d / "index.html"
            if html.exists():
                content = html.read_text()
                if "restaurant-photo" in content:
                    slugs.append(d.name)
    
    print(f"Found {len(slugs)} pages to check")
    
    if args.limit:
        slugs = slugs[:args.limit]
        print(f"Limited to {args.limit} pages")
    
    stats = {"exists": 0, "generated": 0, "failed": 0, "skipped": 0}
    
    for i, slug in enumerate(slugs, 1):
        r2_key = f"popular-picks/{slug}/hero-bg.jpg"
        print(f"[{i}/{len(slugs)}] {slug}")
        
        # Check if already on R2
        if check_r2_exists(r2_key):
            print(f"  ✅ Already exists on R2")
            stats["exists"] += 1
            continue
        
        if args.dry_run:
            print(f"  🔍 Would generate + upload {r2_key}")
            stats["skipped"] += 1
            continue
        
        # Get page info
        info = extract_page_info(slug)
        if not info:
            print(f"  ⚠️ Could not extract page info, skipping")
            stats["failed"] += 1
            continue
        
        # Generate image
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            print(f"  🎨 Generating hero for {info['city']}...")
            if generate_hero_image(info["city"], info["country"], info["title"], tmp_path):
                # Upload to R2
                print(f"  ☁️ Uploading to R2: {r2_key}")
                if upload_to_r2(tmp_path, r2_key):
                    print(f"  ✅ Done!")
                    stats["generated"] += 1
                else:
                    stats["failed"] += 1
            else:
                stats["failed"] += 1
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        
        # Rate limit: ~2 sec between generations
        if i < len(slugs):
            time.sleep(2)
    
    print(f"\n{'='*40}")
    print(f"Done! Already existed: {stats['exists']}, Generated: {stats['generated']}, "
          f"Failed: {stats['failed']}, Skipped: {stats['skipped']}")
    return 0 if stats["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
