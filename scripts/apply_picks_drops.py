#!/usr/bin/env python3
"""
Apply zero-volume popular-picks drops:

  1. Load zero-vol topic slugs from picks-tiers.csv (volume == 0, page_type == topic).
  2. Compute slug -> redirect target using progressive prefix match against
     destinations.json (longest city slug prefix -> country -> hub slug).
     Fallback: /popular-picks/ root.
  3. Remove drops from:
       - popular-picks/picks-metadata.json
       - api/v1/picks.json (count + picks array)
       - api/v1/search-index.json (items of type=pick)
       - sitemap.xml (<url> blocks)
  4. Delete popular-picks/<slug>/ directories.
  5. Append 301 redirects to _redirects.

Use --dry-run to preview.
"""

import argparse
import csv
import json
import os
import re
import shutil
import sys

ROOT = "/Users/bjh/Documents/tabiji/.claude/worktrees/happy-tharp-5601b2"
TIERS_CSV = os.path.join(ROOT, "scripts", "compare-analysis", "picks-tiers.csv")
PICKS_DIR = os.path.join(ROOT, "popular-picks")
METADATA = os.path.join(PICKS_DIR, "picks-metadata.json")
API_PICKS = os.path.join(ROOT, "api", "v1", "picks.json")
SEARCH_INDEX = os.path.join(ROOT, "api", "v1", "search-index.json")
SITEMAP = os.path.join(ROOT, "sitemap.xml")
DESTINATIONS = os.path.join(ROOT, "api", "v1", "destinations.json")
REDIRECTS = os.path.join(ROOT, "_redirects")

# Country name -> hub slug (109 country hubs under /popular-picks/)
COUNTRY_OVERRIDES = {
    "united arab emirates": "uae",
    "uae": "uae",
    "south korea": "south-korea",
    "united kingdom": "united-kingdom",
    "uk": "united-kingdom",
    "great britain": "united-kingdom",
    "england": "united-kingdom",
    "scotland": "united-kingdom",
    "wales": "united-kingdom",
    "united states": "usa",
    "usa": "usa",
    "u.s.": "usa",
    "united states of america": "usa",
    "czech republic": "czech-republic",
    "czechia": "czech-republic",
    "bosnia and herzegovina": "bosnia-and-herzegovina",
    "bosnia": "bosnia-and-herzegovina",
    "saint lucia": "saint-lucia",
    "st. lucia": "saint-lucia",
    "new zealand": "new-zealand",
    "costa rica": "costa-rica",
    "dominican republic": "dominican-republic",
    "el salvador": "el-salvador",
    "hong kong": "hong-kong",
    "south africa": "south-africa",
    "sri lanka": "sri-lanka",
}


def load_zero_vol_topics():
    with open(TIERS_CSV) as f:
        rows = list(csv.DictReader(f))
    return [
        r["slug"] for r in rows
        if r["page_type"] == "topic" and int(r["volume"]) == 0
    ]


def load_city_to_country():
    with open(DESTINATIONS) as f:
        dest = json.load(f)
    out = {}
    for d in dest["destinations"]:
        slug = d.get("slug")
        country = d.get("country")
        if slug and country:
            out[slug] = country
    return out


def load_country_hubs():
    with open(METADATA) as f:
        meta = json.load(f)
    return {s for s, c in meta.items() if c.get("title", "").startswith("Popular Picks in ")}


def country_to_hub_slug(country, hubs):
    if not country:
        return None
    n = country.lower().strip()
    if n in COUNTRY_OVERRIDES:
        o = COUNTRY_OVERRIDES[n]
        return o if (o and o in hubs) else None
    slug = n.replace(" ", "-").replace(".", "").replace(",", "")
    return slug if slug in hubs else None


def resolve_hub(slug, city_slugs, city_to_country, hubs):
    # Progressive prefix match: longest city slug that's a prefix of the topic slug
    parts = slug.split("-")
    for i in range(len(parts) - 1, 0, -1):
        prefix = "-".join(parts[:i])
        if prefix in city_slugs:
            country = city_to_country.get(prefix)
            hub = country_to_hub_slug(country, hubs)
            if hub:
                return f"/popular-picks/{hub}/"
            return "/popular-picks/"
    return "/popular-picks/"


def remove_from_metadata(drops_set, dry_run):
    with open(METADATA) as f:
        meta = json.load(f)
    before = len(meta)
    kept = {k: v for k, v in meta.items() if k not in drops_set}
    after = len(kept)
    print(f"  picks-metadata.json: {before} -> {after} (removed {before-after})")
    if not dry_run:
        with open(METADATA, "w") as f:
            json.dump(kept, f, indent=2)


def remove_from_api_picks(drops_set, dry_run):
    with open(API_PICKS) as f:
        api = json.load(f)
    before = len(api["picks"])
    kept = [p for p in api["picks"] if p.get("slug") not in drops_set]
    after = len(kept)
    print(f"  api/v1/picks.json: {before} -> {after} (removed {before-after})")
    if not dry_run:
        api["picks"] = kept
        api["count"] = after
        with open(API_PICKS, "w") as f:
            json.dump(api, f, indent=2)


def remove_from_search_index(drops_set, dry_run):
    with open(SEARCH_INDEX) as f:
        si = json.load(f)
    before = len(si["items"])
    drop_ids = {f"pick:{s}" for s in drops_set}
    kept = [
        i for i in si["items"]
        if not (
            i.get("type") == "pick"
            and (i.get("slug") in drops_set or i.get("id") in drop_ids)
        )
    ]
    after = len(kept)
    from collections import Counter
    types = Counter(i.get("type", "unknown") for i in kept)
    print(f"  api/v1/search-index.json: {before} -> {after} (removed {before-after})")
    if not dry_run:
        si["items"] = kept
        si["count"] = after
        si["types"] = dict(types)
        with open(SEARCH_INDEX, "w") as f:
            json.dump(si, f, indent=2)


def remove_from_sitemap(drops_set, dry_run):
    with open(SITEMAP) as f:
        content = f.read()
    url_re = re.compile(
        r"\s*<url>\s*<loc>https://tabiji\.ai/popular-picks/([a-z0-9\-]+)/</loc>.*?</url>",
        re.DOTALL,
    )
    removed = [0]
    def replace(m):
        if m.group(1) in drops_set:
            removed[0] += 1
            return ""
        return m.group(0)
    new_content = url_re.sub(replace, content)
    print(f"  sitemap.xml: removed {removed[0]} <url> blocks")
    if not dry_run:
        with open(SITEMAP, "w") as f:
            f.write(new_content)


def delete_dirs(drops_set, dry_run):
    deleted = 0
    missing = 0
    for slug in drops_set:
        path = os.path.join(PICKS_DIR, slug)
        if os.path.isdir(path):
            if not dry_run:
                shutil.rmtree(path)
            deleted += 1
        else:
            missing += 1
    print(f"  popular-picks/<slug>/: deleted {deleted} ({missing} missing)")


def append_redirects(mapping, dry_run):
    lines = [f"/popular-picks/{s}/ {mapping[s]} 301" for s in sorted(mapping)]
    header = "\n\n# Zero-volume popular-picks pages redirected to country hubs\n"
    payload = header + "\n".join(lines) + "\n"
    print(f"  _redirects: appending {len(lines)} new 301 rules")
    if not dry_run:
        with open(REDIRECTS, "a") as f:
            f.write(payload)


def update_api_index(new_picks_count, dry_run):
    path = os.path.join(ROOT, "api", "v1", "index.json")
    with open(path) as f:
        idx = json.load(f)
    old = idx.get("stats", {}).get("picksGuides")
    print(f"  api/v1/index.json: picksGuides {old} -> {new_picks_count}")
    if not dry_run:
        idx.setdefault("stats", {})["picksGuides"] = new_picks_count
        with open(path, "w") as f:
            json.dump(idx, f, indent=2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.dry_run:
        print("=== DRY RUN ===\n")

    drops = load_zero_vol_topics()
    drops_set = set(drops)
    print(f"Zero-volume topic drops: {len(drops)}")

    city_to_country = load_city_to_country()
    city_slugs = set(city_to_country.keys())
    hubs = load_country_hubs()

    mapping = {}
    for slug in drops:
        mapping[slug] = resolve_hub(slug, city_slugs, city_to_country, hubs)

    # Distribution
    from collections import Counter
    dist = Counter(mapping.values())
    print(f"\nRedirect distribution (top 20):")
    for tgt, n in dist.most_common(20):
        print(f"  {n:>4}  {tgt}")
    fallback = dist.get("/popular-picks/", 0)
    print(f"\n  → {len(drops) - fallback} to specific hub / {fallback} to root fallback")

    # Count remaining after drop
    with open(METADATA) as f:
        meta = json.load(f)
    new_count = len(meta) - len([k for k in meta if k in drops_set])

    print("\nApplying changes:")
    remove_from_metadata(drops_set, args.dry_run)
    remove_from_api_picks(drops_set, args.dry_run)
    remove_from_search_index(drops_set, args.dry_run)
    remove_from_sitemap(drops_set, args.dry_run)
    update_api_index(new_count, args.dry_run)
    delete_dirs(drops_set, args.dry_run)
    append_redirects(mapping, args.dry_run)

    print(f"\nDone. {'(dry run)' if args.dry_run else 'Changes applied.'}")


if __name__ == "__main__":
    main()
