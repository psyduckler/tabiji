#!/usr/bin/env python3
"""
Deep-clean popular-picks drop references from every API/JSON file.

Handles three patterns:
  1. Objects in lists where obj.slug is a drop  → remove the object.
     Common in:  picks[], relatedPicks[], items[] (type=pick)
  2. String fields (heroImage, photo, image, url) containing /popular-picks/{drop}/
     → clear the string.
  3. Updates coverage/count/checksum/sizeBytes after modifying packs.

Scans: api/, popular-picks/picks-metadata.json, popular-picks-data/
Skips: sitemap.xml (already handled), search-index.json (already clean)
"""

import csv
import hashlib
import json
import os
import sys

ROOT = "/Users/bjh/Documents/tabiji/.claude/worktrees/happy-tharp-5601b2"
TIERS = os.path.join(ROOT, "scripts", "compare-analysis", "picks-tiers.csv")


def load_drops():
    with open(TIERS) as f:
        return {
            r["slug"] for r in csv.DictReader(f)
            if r["page_type"] == "topic" and int(r["volume"]) == 0
        }


def clean(obj, drops, stats):
    """Recursively clean a JSON object in-place. Returns the cleaned object."""
    if isinstance(obj, list):
        new_list = []
        for item in obj:
            if isinstance(item, dict) and item.get("slug") in drops:
                stats["objects_removed"] += 1
                continue
            # Also match search-index style: type=pick + id=pick:<slug>
            if isinstance(item, dict) and item.get("type") == "pick":
                sid = item.get("id", "")
                if sid.startswith("pick:") and sid[5:] in drops:
                    stats["objects_removed"] += 1
                    continue
            new_list.append(clean(item, drops, stats))
        return new_list
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            if isinstance(v, str):
                # Any URL-ish field pointing to a dropped pick → clear
                if any(f"/popular-picks/{d}/" in v for d in drops):
                    # But keep url-only fields if we're going to remove the parent object anyway
                    # (that already happened above). Here we just clear.
                    stats["strings_cleared"] += 1
                    new_dict[k] = ""
                    continue
            new_dict[k] = clean(v, drops, stats)
        return new_dict
    return obj


def should_skip(relpath):
    return relpath.endswith("sitemap.xml") or "scripts/compare-analysis/" in relpath


def process_file(path, drops):
    try:
        with open(path) as f:
            content = f.read()
    except Exception:
        return None

    # Quick skip if no drop ref
    if not any(f"/popular-picks/{d}/" in content for d in drops):
        return None

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return None

    stats = {"objects_removed": 0, "strings_cleared": 0}
    cleaned = clean(data, drops, stats)

    # Update pack-specific fields if present
    if isinstance(cleaned, dict):
        if "data" in cleaned and isinstance(cleaned["data"], dict):
            # coverage.picks
            if "coverage" in cleaned and isinstance(cleaned["coverage"], dict):
                if isinstance(cleaned["data"].get("picks"), list):
                    cleaned["coverage"]["picks"] = len(cleaned["data"]["picks"])
        # top-level count
        if "count" in cleaned:
            for list_key in ("picks", "items", "comparisons"):
                if isinstance(cleaned.get(list_key), list):
                    cleaned["count"] = len(cleaned[list_key])
                    break
        # Recompute checksum/sizeBytes for pack-style
        if "checksum" in cleaned and "sizeBytes" in cleaned:
            body_obj = {k: v for k, v in cleaned.items() if k not in ("sizeBytes", "checksum")}
            body_ser = json.dumps(body_obj, separators=(",", ":"), sort_keys=True, ensure_ascii=False)
            cleaned["checksum"] = f"sha256:{hashlib.sha256(body_ser.encode('utf-8')).hexdigest()}"
            cleaned["sizeBytes"] = len(json.dumps(cleaned, indent=2, ensure_ascii=False).encode("utf-8"))

    with open(path, "w") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    return stats


def main():
    drops = load_drops()
    print(f"Drops: {len(drops)}")

    # Collect candidate files
    targets = []
    for base in ["api", "popular-picks-data"]:
        base_path = os.path.join(ROOT, base)
        if not os.path.exists(base_path):
            continue
        for root_dir, _, files in os.walk(base_path):
            for f in files:
                if f.endswith(".json"):
                    p = os.path.join(root_dir, f)
                    rel = os.path.relpath(p, ROOT)
                    if should_skip(rel):
                        continue
                    targets.append(p)

    # Also always handle these top-level files
    for extra in ["popular-picks/picks-metadata.json"]:
        p = os.path.join(ROOT, extra)
        if os.path.exists(p):
            targets.append(p)

    total_objects = 0
    total_strings = 0
    touched = 0
    for path in targets:
        stats = process_file(path, drops)
        if stats is None:
            continue
        if stats["objects_removed"] == 0 and stats["strings_cleared"] == 0:
            continue
        touched += 1
        total_objects += stats["objects_removed"]
        total_strings += stats["strings_cleared"]
        rel = os.path.relpath(path, ROOT)
        print(f"  {rel}: -{stats['objects_removed']} objects, "
              f"-{stats['strings_cleared']} strings")

    print(f"\nTotal: {touched} files touched, "
          f"{total_objects} objects removed, {total_strings} strings cleared")


if __name__ == "__main__":
    main()
