#!/usr/bin/env python3
"""
Pull search volume from Semrush API for all pending compare pages.
Checks both forward and backward keyword variations.
Outputs CSV: slug, keyword_1, vol_1, keyword_2, vol_2, best_keyword, best_vol, total_vol
"""

import json
import csv
import time
import urllib.request
import urllib.parse
import sys
import os

API_KEY = "466c49b8794c2ba3d09ad2afd1964cd0"
DATABASE = "us"
QUEUE_FILE = "/Users/bjh/Documents/tabiji/compare-queue.json"
OUTPUT_FILE = "/Users/bjh/Documents/tabiji/compare-pending-search-volumes.csv"
PROGRESS_FILE = "/Users/bjh/Documents/tabiji/scripts/semrush-volume-progress.json"

def slug_to_keywords(slug):
    """Convert slug like 'tokyo-vs-lisbon' to forward and backward keyword pairs."""
    parts = slug.split("-vs-")
    if len(parts) != 2:
        return None, None
    dest1 = parts[0].replace("-", " ")
    dest2 = parts[1].replace("-", " ")
    return f"{dest1} vs {dest2}", f"{dest2} vs {dest1}"

def get_search_volume(keyword):
    """Query Semrush API for search volume of a keyword."""
    url = (
        f"https://api.semrush.com/"
        f"?type=phrase_this"
        f"&key={API_KEY}"
        f"&phrase={urllib.parse.quote(keyword)}"
        f"&database={DATABASE}"
        f"&export_columns=Ph,Nq"
    )
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8").strip()
            lines = body.split("\n")
            if len(lines) >= 2:
                parts = lines[1].split(";")
                if len(parts) >= 2:
                    try:
                        return int(parts[1])
                    except ValueError:
                        return 0
            return 0
    except Exception as e:
        print(f"  Error for '{keyword}': {e}", file=sys.stderr)
        return 0

def load_progress():
    """Load progress from previous runs."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {}

def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)

def main():
    with open(QUEUE_FILE) as f:
        queue = json.load(f)

    pending = [item["slug"] for item in queue if item["status"] == "pending"]
    print(f"Total pending compare pages: {len(pending)}")

    progress = load_progress()
    results = []

    # Restore already-completed results
    already_done = 0
    remaining = []
    for slug in pending:
        if slug in progress:
            results.append(progress[slug])
            already_done += 1
        else:
            remaining.append(slug)

    print(f"Already completed: {already_done}")
    print(f"Remaining: {len(remaining)}")

    for i, slug in enumerate(remaining):
        kw1, kw2 = slug_to_keywords(slug)
        if kw1 is None:
            print(f"[{i+1}/{len(remaining)}] Skipping malformed slug: {slug}")
            continue

        print(f"[{i+1}/{len(remaining)}] {slug}: querying '{kw1}' + '{kw2}'...", end=" ", flush=True)

        vol1 = get_search_volume(kw1)
        time.sleep(0.15)  # rate limit
        vol2 = get_search_volume(kw2)
        time.sleep(0.15)

        if vol1 >= vol2:
            best_kw, best_vol = kw1, vol1
        else:
            best_kw, best_vol = kw2, vol2

        total = vol1 + vol2

        row = {
            "slug": slug,
            "url": f"https://tabiji.ai/compare/{slug}/",
            "keyword_1": kw1,
            "vol_1": vol1,
            "keyword_2": kw2,
            "vol_2": vol2,
            "best_keyword": best_kw,
            "best_vol": best_vol,
            "total_vol": total,
        }

        results.append(row)
        progress[slug] = row
        print(f"vol1={vol1}, vol2={vol2}, total={total}")

        # Save progress every 25 items
        if (i + 1) % 25 == 0:
            save_progress(progress)
            print(f"  [Progress saved at {i+1}]")

    # Final save
    save_progress(progress)

    # Sort by total volume descending
    results.sort(key=lambda r: r["total_vol"], reverse=True)

    # Write CSV
    fieldnames = ["slug", "url", "keyword_1", "vol_1", "keyword_2", "vol_2", "best_keyword", "best_vol", "total_vol"]
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nDone! CSV written to {OUTPUT_FILE}")
    print(f"Total rows: {len(results)}")

    # Quick stats
    with_volume = [r for r in results if r["total_vol"] > 0]
    print(f"Pages with search volume > 0: {len(with_volume)}")
    if with_volume:
        top = with_volume[0]
        print(f"Top opportunity: {top['slug']} ({top['total_vol']:,} total volume)")

if __name__ == "__main__":
    main()
