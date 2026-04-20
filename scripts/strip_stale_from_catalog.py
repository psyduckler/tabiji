#!/usr/bin/env python3
"""
Strip dead/stale entries from api/v1/catalog/ files so the public catalog API
reflects what actually lives on the site.

Strategy:
  For each catalog file, iterate items and keep those whose (entityType, slug)
  exists in the live set. Entity types that aren't disk-backed (alert, insurance,
  place) or that use a non-slug ID scheme (country / safety — both ISO-keyed)
  pass through untouched.

Live sources of truth:
  - compare    — /compare/<slug>/ directories (-vs- pattern)
  - pick       — /popular-picks/<slug>/ directories
  - itinerary  — /itineraries/<slug>/ ∪ /i/<slug>/
  - destination— /api/v1/destinations-full.json keys
  - card       — /credit-cards/<slug>/
  - scam       — /scams/<slug>/

Preserves as-is (not disk-backed, or ISO-keyed):
  - alert, insurance, place, country, safety

Updates itemCount + sizeBytes metadata where present.
"""

import argparse
import csv
import hashlib
import json
import os

ROOT = "/Users/bjh/Documents/tabiji/.claude/worktrees/happy-tharp-5601b2"
CATALOG_DIR = os.path.join(ROOT, "api", "v1", "catalog")
MANIFEST = os.path.join(ROOT, "api", "v1", "catalog.json")

# Entity types whose catalog entries are still live if their slug exists on disk.
DISK_BACKED = {"compare", "pick", "itinerary", "destination", "card", "scam"}
# Entity types we leave alone.
PASS_THROUGH = {"alert", "insurance", "place", "country", "safety"}


def list_dirs(path):
    if not os.path.exists(path):
        return set()
    return {e for e in os.listdir(path) if os.path.isdir(os.path.join(path, e))}


def build_live():
    live = {
        "compare": {e for e in list_dirs(os.path.join(ROOT, "compare")) if "-vs-" in e},
        "pick": list_dirs(os.path.join(ROOT, "popular-picks")),
        "itinerary": list_dirs(os.path.join(ROOT, "itineraries"))
                     | list_dirs(os.path.join(ROOT, "i")),
        "card": list_dirs(os.path.join(ROOT, "credit-cards")),
        "scam": list_dirs(os.path.join(ROOT, "scams")),
    }
    # Destinations come from the Pages Function data source.
    with open(os.path.join(ROOT, "api", "v1", "destinations-full.json")) as f:
        df = json.load(f)
    live["destination"] = set(df.keys()) if isinstance(df, dict) else set()
    return live


def keep(item, live):
    if not isinstance(item, dict):
        return True
    t = item.get("entityType", "")
    if t in PASS_THROUGH:
        return True
    if t in DISK_BACKED:
        return item.get("slug") in live.get(t, set())
    # Unknown type — pass through rather than drop (safer default).
    return True


def process(path, live, stats, dry_run):
    with open(path) as f:
        data = json.load(f)

    # Every catalog file is either {..., "items": [...]} or a list
    if isinstance(data, dict) and isinstance(data.get("items"), list):
        items = data["items"]
        container = "dict"
    elif isinstance(data, list):
        items = data
        container = "list"
    else:
        return None

    before = len(items)
    kept_items = [i for i in items if keep(i, live)]
    after = len(kept_items)
    if after == before:
        return None

    if container == "dict":
        data["items"] = kept_items
        if "itemCount" in data:
            data["itemCount"] = after
        if "sizeBytes" in data:
            data["sizeBytes"] = 0  # recomputed after serialization below
        if "checksum" in data:
            body = {k: v for k, v in data.items() if k not in ("sizeBytes", "checksum")}
            ser = json.dumps(body, separators=(",", ":"), sort_keys=True, ensure_ascii=False)
            data["checksum"] = f"sha256:{hashlib.sha256(ser.encode('utf-8')).hexdigest()}"
    else:
        data = kept_items

    # Track what we stripped, per-type, for the summary
    dropped = [i for i in items if not keep(i, live)]
    from collections import Counter
    drop_counter = Counter(d.get("entityType", "?") for d in dropped if isinstance(d, dict))
    for t, n in drop_counter.items():
        stats.setdefault(t, 0)
        stats[t] += n

    if not dry_run:
        with open(path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        if isinstance(data, dict) and "sizeBytes" in data:
            data["sizeBytes"] = os.path.getsize(path)
            with open(path, "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    return before, after, dict(drop_counter)


def update_manifest(live, dry_run):
    """Update catalog.json's itemCount by summing chunks + non-chunk shards."""
    with open(MANIFEST) as f:
        m = json.load(f)

    # Chunks are 1-4.json; itemCount on manifest = sum of all chunks + extras in shards
    # Keep it simple: itemCount = sum of all catalog files' itemCount where applicable
    total = 0
    for fname in sorted(os.listdir(CATALOG_DIR)):
        if not fname.endswith(".json") or fname == "places-index.json":
            continue
        p = os.path.join(CATALOG_DIR, fname)
        try:
            with open(p) as f:
                d = json.load(f)
        except Exception:
            continue
        if isinstance(d, dict) and isinstance(d.get("items"), list):
            total += len(d["items"])
        elif isinstance(d, list):
            total += len(d)
    # Don't double-count: chunks include everything from shards (except places-shard-*).
    # Just take the chunks total.
    chunks_total = 0
    for i in range(1, 5):
        p = os.path.join(CATALOG_DIR, f"{i}.json")
        if os.path.exists(p):
            with open(p) as f:
                d = json.load(f)
            chunks_total += len(d.get("items", []))
    # places-shard files live outside chunks
    places_total = 0
    for i in range(1, 5):
        p = os.path.join(CATALOG_DIR, f"places-shard-{i}.json")
        if os.path.exists(p):
            with open(p) as f:
                d = json.load(f)
            places_total += len(d if isinstance(d, list) else d.get("items", []))
    new_total = chunks_total + places_total

    old_total = m.get("itemCount", 0)
    m["itemCount"] = new_total
    print(f"  catalog.json manifest: itemCount {old_total} -> {new_total}")

    if not dry_run:
        with open(MANIFEST, "w") as f:
            json.dump(m, f, indent=2, ensure_ascii=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.dry_run:
        print("=== DRY RUN ===\n")

    live = build_live()
    print("Live set sizes:")
    for k in sorted(live):
        print(f"  {k:<12} {len(live[k]):>6,}")

    print("\nProcessing catalog files:")
    files = sorted(f for f in os.listdir(CATALOG_DIR)
                   if f.endswith(".json") and f != "places-index.json")
    total_stripped = 0
    per_type_totals = {}

    for f in files:
        path = os.path.join(CATALOG_DIR, f)
        stats = {}
        result = process(path, live, stats, args.dry_run)
        if result is None:
            continue
        before, after, drop_counter = result
        total_stripped += (before - after)
        for t, n in stats.items():
            per_type_totals[t] = per_type_totals.get(t, 0) + n
        print(f"  {f:<28} {before:>7,} -> {after:>7,}   (stripped {before-after}, by type: {drop_counter})")

    print(f"\nTotal stripped entries: {total_stripped}")
    print(f"Per-type totals: {per_type_totals}")

    print("\nRecomputing manifest counts:")
    update_manifest(live, args.dry_run)

    print(f"\nDone. {'(dry run)' if args.dry_run else 'Changes applied.'}")


if __name__ == "__main__":
    main()
