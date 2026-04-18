#!/usr/bin/env python3
"""Fetch Google Images photos via SerpAPI for destinations that Unsplash couldn't find.
Downloads best result, converts to webp, uploads to R2 CDN, updates JSON files.
Processes 20 per run.
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
import tempfile
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
QUEUE_FILE = SCRIPT_DIR / "photo-queue.json"
FIND_DEST_FILE = SCRIPT_DIR / "destinations.json"
API_DEST_DIR = REPO_ROOT / "api" / "v1" / "destinations"
LOG_FILE = SCRIPT_DIR / "serpapi-fetch.log"

BATCH_SIZE = 20
SERPAPI_KEY = os.environ.get(
    "SERPAPI_KEY", "3d4b51ea3336e8eb9c73d5a3a28594bf11ec8d9219655903acf9719a6711f639"
)
PLACEHOLDER = "https://img.tabiji.ai/owl-logo.png"

# R2 config
R2_ACCOUNT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"
R2_PUBLIC = "https://img.tabiji.ai"


def log(msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def get_cf_token():
    """Get Cloudflare token from macOS keychain."""
    try:
        result = subprocess.run(
            ["security", "find-generic-password", "-s", "cloudflare-pages-token", "-w"],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip()
    except Exception as e:
        log(f"  ERROR getting CF token: {e}")
        return None


def search_google_images(query):
    """Search Google Images via SerpAPI. Returns list of image results."""
    params = urllib.parse.urlencode({
        "engine": "google_images",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": "5",
        "ijn": "0",
        "tbs": "isz:m",  # medium+ size
    })
    url = f"https://serpapi.com/search.json?{params}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())

        results = data.get("images_results", [])[:5]
        return [{
            "url": img.get("original", ""),
            "title": img.get("title", ""),
            "width": img.get("original_width", 0),
            "height": img.get("original_height", 0),
        } for img in results if img.get("original")]
    except Exception as e:
        log(f"  ERROR searching SerpAPI: {str(e)[:150]}")
        return []


def download_image(url, dest_path):
    """Download image to local path. Returns True if successful and > 10KB."""
    try:
        result = subprocess.run(
            ["curl", "-sL", "-o", str(dest_path), "--max-time", "15", url],
            capture_output=True, timeout=20
        )
        if result.returncode != 0:
            return False
        size = dest_path.stat().st_size if dest_path.exists() else 0
        if size < 10000:
            dest_path.unlink(missing_ok=True)
            return False
        return True
    except Exception:
        dest_path.unlink(missing_ok=True)
        return False


def convert_to_webp(src_path, dest_path):
    """Convert image to webp using sips (macOS). Returns True if successful."""
    try:
        # First resize to 1080px wide max, convert to jpeg as intermediate
        tmp_jpg = src_path.with_suffix(".opt.jpg")
        subprocess.run(
            ["sips", "-Z", "1080", "--setProperty", "format", "jpeg",
             "--setProperty", "formatOptions", "85", str(src_path), "--out", str(tmp_jpg)],
            capture_output=True, timeout=15
        )
        # Try cwebp for webp conversion
        result = subprocess.run(
            ["cwebp", "-q", "80", str(tmp_jpg), "-o", str(dest_path)],
            capture_output=True, timeout=15
        )
        tmp_jpg.unlink(missing_ok=True)
        if result.returncode == 0 and dest_path.exists() and dest_path.stat().st_size > 5000:
            return True
        # Fallback: just use the jpg renamed
        dest_path.unlink(missing_ok=True)
        return False
    except Exception as e:
        log(f"  WARNING: convert failed: {e}")
        return False


def upload_to_r2(local_path, r2_key, content_type="image/webp"):
    """Upload file to Cloudflare R2. Returns public URL or None."""
    cf_token = get_cf_token()
    if not cf_token:
        return None

    try:
        result = subprocess.run(
            ["curl", "-s", "-X", "PUT",
             "-H", f"Authorization: Bearer {cf_token}",
             "-H", f"Content-Type: {content_type}",
             "--data-binary", f"@{local_path}",
             f"https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{r2_key}"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            resp = json.loads(result.stdout) if result.stdout else {}
            if resp.get("success", True):  # R2 API returns success field
                return f"{R2_PUBLIC}/{r2_key}"
        log(f"  R2 upload response: {result.stdout[:200]}")
        return None
    except Exception as e:
        log(f"  ERROR uploading to R2: {e}")
        return None


def process_destination(slug, name, region, country):
    """Search, download, convert, upload photo for a destination. Returns photo URL or None."""
    # Build search query - try destination + country for best results
    query = f"{name} {country} travel landscape photography" if country else f"{name} travel landscape photography"
    log(f"  Searching Google Images: '{name} {country}'")

    results = search_google_images(query)
    if not results:
        # Try simpler query
        query = f"{name} {region} travel"
        results = search_google_images(query)

    if not results:
        log(f"  No Google Images results for '{name}'")
        return None

    # Try downloading each result until one works
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        for i, img in enumerate(results):
            raw_path = tmpdir / f"raw_{i}.jpg"
            webp_path = tmpdir / f"{slug}.webp"

            if not download_image(img["url"], raw_path):
                continue

            # Convert to webp
            if convert_to_webp(raw_path, webp_path):
                # Upload to R2
                r2_key = f"find/img/{slug}.webp"
                public_url = upload_to_r2(webp_path, r2_key)
                if public_url:
                    log(f"  OK: uploaded to {public_url}")
                    return public_url

            # If webp failed, try uploading as jpeg
            jpg_path = tmpdir / f"{slug}.jpg"
            try:
                subprocess.run(
                    ["sips", "-Z", "1080", "--setProperty", "format", "jpeg",
                     "--setProperty", "formatOptions", "85", str(raw_path), "--out", str(jpg_path)],
                    capture_output=True, timeout=15
                )
                if jpg_path.exists() and jpg_path.stat().st_size > 5000:
                    r2_key = f"find/img/{slug}.jpg"
                    public_url = upload_to_r2(jpg_path, r2_key, "image/jpeg")
                    if public_url:
                        log(f"  OK: uploaded as jpg to {public_url}")
                        return public_url
            except Exception:
                pass

            raw_path.unlink(missing_ok=True)

    log(f"  FAILED: could not download/convert any image for '{name}'")
    return None


def update_api_json(slug, photo_url):
    """Update the photo field in api/v1/destinations/{slug}.json."""
    api_file = API_DEST_DIR / f"{slug}.json"
    if not api_file.exists():
        log(f"  WARNING: {api_file} not found, skipping API update")
        return False

    with open(api_file) as f:
        data = json.load(f)

    data["photo"] = photo_url
    data["updatedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if "freshness" in data:
        data["freshness"]["updatedAt"] = data["updatedAt"]

    with open(api_file, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return True


def update_find_json(name, photo_url, find_destinations):
    """Update photo in the find/destinations.json data (in-memory)."""
    for entry in find_destinations:
        if entry.get("name") == name:
            entry["photo"] = photo_url
            return True
    return False


def git_commit_and_push(count, batch_num):
    """Pull, add changed files, commit, and push."""
    os.chdir(REPO_ROOT)

    def run_git(cmd):
        log(f"  git: {' '.join(cmd[:5])}")
        return subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    # Stash tracked changes so pull works
    stash_result = run_git(["git", "stash"])
    stashed = "No local changes" not in stash_result.stdout

    # Pull latest
    pull = run_git(["git", "pull", "origin", "main", "--rebase"])
    if pull.returncode != 0:
        log(f"  git pull ERROR: {pull.stderr[:200]}")
        if stashed:
            run_git(["git", "stash", "pop"])
        return

    # Restore stash
    if stashed:
        pop = run_git(["git", "stash", "pop"])
        if pop.returncode != 0:
            log(f"  git stash pop ERROR: {pop.stderr[:200]}")
            return

    # Stage and commit
    run_git(["git", "add", "api/v1/destinations/", "find/destinations.json", "find/photo-queue.json"])
    commit = run_git(["git", "commit", "-m",
                       f"Add Google Images photos for {count} destinations (serpapi batch #{batch_num})"])
    if commit.returncode != 0:
        if "nothing to commit" in commit.stdout:
            log("  git: nothing to commit")
        else:
            log(f"  git commit ERROR: {commit.stderr[:200]}")
        return

    # Push
    push = run_git(["git", "push", "origin", "main"])
    if push.returncode != 0:
        log(f"  git push ERROR: {push.stderr[:200]}")
    else:
        log("  git: pushed successfully")


def main():
    if not QUEUE_FILE.exists():
        log("ERROR: photo-queue.json not found")
        sys.exit(1)

    with open(QUEUE_FILE) as f:
        queue = json.load(f)

    items = queue["items"]
    # Find items that Unsplash couldn't find
    no_results_indices = [i for i, item in enumerate(items) if item["status"] == "no_results"]
    done_serpapi = sum(1 for item in items if item.get("serpapi_status") == "done")

    if not no_results_indices:
        log("All no_results items have been processed!")
        return

    log(f"Queue: {len(no_results_indices)} no_results items, {done_serpapi} already done via SerpAPI")

    # Take next batch (skip ones already processed by serpapi)
    batch = []
    for idx in no_results_indices:
        if items[idx].get("serpapi_status") in ("done", "serpapi_no_results"):
            continue
        batch.append(idx)
        if len(batch) >= BATCH_SIZE:
            break

    if not batch:
        log("All no_results items processed by SerpAPI!")
        return

    batch_num = (done_serpapi // BATCH_SIZE) + 1
    log(f"Starting SerpAPI batch #{batch_num}: processing {len(batch)} destinations")

    # Load find/destinations.json once
    with open(FIND_DEST_FILE) as f:
        find_destinations = json.load(f)

    processed = 0
    skipped = 0

    for step, idx in enumerate(batch):
        item = items[idx]
        slug = item["slug"]
        name = item["name"]
        region = item.get("region", "")
        country = item.get("country", region)

        log(f"[{step+1}/{len(batch)}] Processing: {name} ({region})")

        photo_url = process_destination(slug, name, region, country)

        if photo_url:
            # Update API JSON
            update_api_json(slug, photo_url)
            # Update find/destinations.json in memory
            update_find_json(name, photo_url, find_destinations)

            item["serpapi_status"] = "done"
            item["status"] = "done"
            item["photo_url"] = photo_url
            item["photo_source"] = "google_images"
            item["completed_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            processed += 1
        else:
            item["serpapi_status"] = "serpapi_no_results"
            skipped += 1

        # Small delay between searches
        time.sleep(1)

    # Save find/destinations.json
    with open(FIND_DEST_FILE, "w") as f:
        json.dump(find_destinations, f, indent=2, ensure_ascii=False)
        f.write("\n")
    log("Updated find/destinations.json")

    # Save queue
    queue["last_serpapi_run"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    queue["last_serpapi_batch"] = batch_num
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)
        f.write("\n")
    log("Updated photo-queue.json")

    log(f"SerpAPI batch #{batch_num} complete: {processed} added, {skipped} skipped")

    if processed > 0:
        git_commit_and_push(processed, batch_num)

    remaining = sum(1 for item in items
                    if item["status"] == "no_results"
                    and item.get("serpapi_status") not in ("done", "serpapi_no_results"))
    if remaining > 0:
        log(f"Remaining: {remaining} destinations")
    else:
        log("All destinations processed!")


if __name__ == "__main__":
    main()
