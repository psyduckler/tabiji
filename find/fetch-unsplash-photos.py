#!/usr/bin/env python3
"""Fetch Unsplash photos for destinations missing images. Processes 22 per run.

Each Unsplash search costs 2 API calls (search + download tracking).
With a 50 req/hr limit, we can safely do 22 destinations per hour.
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
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
QUEUE_FILE = SCRIPT_DIR / "photo-queue.json"
FIND_DEST_FILE = SCRIPT_DIR / "destinations.json"
API_DEST_DIR = REPO_ROOT / "api" / "v1" / "destinations"
LOG_FILE = SCRIPT_DIR / "unsplash-fetch.log"

BATCH_SIZE = 22  # 50 req/hr limit, 2 calls per destination → 25 max, 22 for safety
UNSPLASH_ACCESS_KEY = os.environ.get(
    "UNSPLASH_ACCESS_KEY", "BCCK9bkNIOgkZULC_K5FYLHluSH_ro4T1MPD1pQbjWk"
)
PLACEHOLDER = "https://img.tabiji.ai/owl-logo.png"


def log(msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def search_unsplash(query):
    """Search Unsplash for a landscape photo. Returns (photo_url, download_location) or (None, None)."""
    params = urllib.parse.urlencode({
        "query": query,
        "per_page": "1",
        "orientation": "landscape",
        "content_filter": "high",
    })
    url = f"https://api.unsplash.com/search/photos?{params}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Client-ID {UNSPLASH_ACCESS_KEY}")
    req.add_header("Accept-Version", "v1")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            headers = dict(resp.headers)
            remaining = headers.get("X-Ratelimit-Remaining", "?")
            log(f"  Unsplash rate limit remaining: {remaining}")
    except urllib.error.HTTPError as e:
        if e.code == 403:
            log(f"  RATE LIMITED (403) — stopping batch early")
            return None, None, True
        raise

    results = data.get("results", [])
    if not results:
        return None, None, False

    photo = results[0]
    photo_url = photo["urls"]["regular"]
    dl_location = photo.get("links", {}).get("download_location", "")

    # Trigger download event per Unsplash API guidelines
    if dl_location:
        try:
            dl_req = urllib.request.Request(f"{dl_location}?client_id={UNSPLASH_ACCESS_KEY}")
            with urllib.request.urlopen(dl_req, timeout=10):
                pass
        except Exception:
            pass  # Non-critical

    return photo_url, photo.get("user", {}).get("name", ""), False


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
    """Update photo in the find/destinations.json data (in-memory). Returns True if found."""
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
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return result

    # Stash tracked changes so pull --rebase works on a clean tree
    stash_result = run_git(["git", "stash"])
    stashed = "No local changes" not in stash_result.stdout

    # Pull latest from origin
    pull = run_git(["git", "pull", "origin", "main", "--rebase"])
    if pull.returncode != 0:
        log(f"  git pull ERROR: {pull.stderr[:200]}")
        if stashed:
            run_git(["git", "stash", "pop"])
        return

    # Restore stashed changes
    if stashed:
        pop = run_git(["git", "stash", "pop"])
        if pop.returncode != 0:
            log(f"  git stash pop ERROR: {pop.stderr[:200]}")
            return

    # Stage and commit our changes
    run_git(["git", "add", "api/v1/destinations/", "find/destinations.json", "find/photo-queue.json"])

    commit = run_git(["git", "commit", "-m", f"Add Unsplash photos for {count} destinations (batch #{batch_num})"])
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
    pending = [i for i, item in enumerate(items) if item["status"] == "pending"]
    done_count = sum(1 for item in items if item["status"] == "done")

    if not pending:
        log("All items processed! Queue is empty.")
        return

    log(f"Queue: {len(pending)} pending, {done_count} done, {queue['total']} total")

    batch = pending[:BATCH_SIZE]
    batch_num = (done_count // BATCH_SIZE) + 1
    log(f"Starting batch #{batch_num}: processing {len(batch)} destinations")

    # Load find/destinations.json once
    with open(FIND_DEST_FILE) as f:
        find_destinations = json.load(f)

    processed = 0
    skipped = 0
    rate_limited = False

    for step, idx in enumerate(batch):
        item = items[idx]
        slug = item["slug"]
        name = item["name"]
        region = item.get("region", "")
        country = item.get("country", region)

        # Build search query — use name + country for better results
        query = f"{name} {country}" if country else name
        log(f"[{step+1}/{len(batch)}] Searching: {name} ({region})")

        try:
            photo_url, photographer, hit_limit = search_unsplash(query)
        except Exception as e:
            log(f"  ERROR searching Unsplash: {str(e)[:150]}")
            item["status"] = "error"
            item["error"] = str(e)[:200]
            skipped += 1
            time.sleep(2)
            continue

        if hit_limit:
            log("Rate limited — stopping batch early")
            rate_limited = True
            break

        if not photo_url:
            log(f"  No results for '{query}', marking skipped")
            item["status"] = "no_results"
            skipped += 1
            time.sleep(1)
            continue

        # Update API JSON file
        api_updated = update_api_json(slug, photo_url)

        # Update find/destinations.json in memory
        find_updated = update_find_json(name, photo_url, find_destinations)

        item["status"] = "done"
        item["photo_url"] = photo_url
        if photographer:
            item["photographer"] = photographer
        item["completed_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        processed += 1

        log(f"  OK: {name} -> {photo_url[:80]}...")

        # Respect rate limits — small delay between requests
        time.sleep(1.5)

    # Save find/destinations.json
    with open(FIND_DEST_FILE, "w") as f:
        json.dump(find_destinations, f, indent=2, ensure_ascii=False)
        f.write("\n")
    log(f"Updated find/destinations.json")

    # Save queue
    queue["last_run"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    queue["last_batch"] = batch_num
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)
        f.write("\n")
    log(f"Updated photo-queue.json")

    log(f"Batch #{batch_num} complete: {processed} added, {skipped} skipped")

    if processed > 0:
        git_commit_and_push(processed, batch_num)

    remaining = len(pending) - processed - skipped
    if remaining > 0:
        hours_left = remaining / BATCH_SIZE
        log(f"Remaining: {remaining} destinations (~{hours_left:.0f} hours at {BATCH_SIZE}/hr)")
    else:
        log("All destinations processed!")


if __name__ == "__main__":
    main()
