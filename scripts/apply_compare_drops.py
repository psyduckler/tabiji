#!/usr/bin/env python3
"""
Apply the <50-volume compare-page drops:

  1. Load drop slugs from compare-tiers.csv (rows with total_vol < 50).
  2. Compute slug -> hub redirect mapping using inventory.json cluster/region.
  3. Remove drops from:
       - compare/inventory.json         (cards array)
       - api/v1/compare.json            (comparisons array)
       - api/v1/search-index.json       (items array, type=compare only)
       - sitemap.xml                    (<url> blocks)
  4. Strip drop slugs from relatedSlugs of kept cards.
  5. Update counts in api/v1/index.json.
  6. Delete compare/<slug>/ directories.
  7. Append 301 redirects to _redirects.
  8. Run `node scripts/rebuild-compare-hubs.mjs` to regenerate hub HTML.

Use --dry-run to preview without touching files.
"""

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = "/Users/bjh/Documents/tabiji/.claude/worktrees/happy-tharp-5601b2"

TIERS_CSV = os.path.join(ROOT, "scripts", "compare-analysis", "compare-tiers.csv")
INVENTORY = os.path.join(ROOT, "compare", "inventory.json")
API_COMPARE = os.path.join(ROOT, "api", "v1", "compare.json")
SEARCH_INDEX = os.path.join(ROOT, "api", "v1", "search-index.json")
SITEMAP = os.path.join(ROOT, "sitemap.xml")
API_INDEX = os.path.join(ROOT, "api", "v1", "index.json")
REDIRECTS = os.path.join(ROOT, "_redirects")
COMPARE_DIR = os.path.join(ROOT, "compare")

VOL_THRESHOLD = 50

# Existing hub dirs under /compare/
HUBS = {
    "asia", "australia", "bali", "cities", "colombia", "countries", "croatia",
    "culture", "egypt", "europe", "global-mixed", "greece", "hawaii", "iceland",
    "islands", "italy", "japan", "latin-america", "luxury", "maldives", "mexico",
    "middle-east-africa", "morocco", "nature", "new-zealand", "north-america",
    "oceania", "portugal", "spain", "taiwan", "thailand", "trip-style-guides",
    "vietnam",
}

# inventory.json region -> hub slug
REGION_HUB = {
    "Europe": "europe",
    "Asia": "asia",
    "North America": "north-america",
    "Latin America": "latin-america",
    "Middle East & Africa": "middle-east-africa",
    "Oceania": "oceania",
    "Global & Mixed": "global-mixed",
}


def load_drops():
    with open(TIERS_CSV) as f:
        rows = list(csv.DictReader(f))
    return [r["slug"] for r in rows if int(r["total_vol"]) < VOL_THRESHOLD]


def build_redirect_map(drop_slugs, inv_cards):
    slug_to_card = {c["slug"]: c for c in inv_cards}
    mapping = {}  # slug -> hub path (e.g. /compare/japan/)
    fallback = "/compare/"
    missing = []
    for slug in drop_slugs:
        card = slug_to_card.get(slug)
        if not card:
            mapping[slug] = fallback
            missing.append(slug)
            continue
        cluster = (card.get("cluster") or "").strip().lower()
        region = (card.get("region") or "").strip()
        if cluster and cluster in HUBS:
            mapping[slug] = f"/compare/{cluster}/"
        elif region in REGION_HUB and REGION_HUB[region] in HUBS:
            mapping[slug] = f"/compare/{REGION_HUB[region]}/"
        else:
            mapping[slug] = fallback
    return mapping, missing


def remove_drops_from_inventory(drops_set, dry_run):
    with open(INVENTORY) as f:
        inv = json.load(f)
    before = len(inv["cards"])
    kept = [c for c in inv["cards"] if c["slug"] not in drops_set]
    # Strip drop refs from relatedSlugs
    stripped_refs = 0
    for c in kept:
        related = c.get("relatedSlugs", [])
        cleaned = [s for s in related if s not in drops_set]
        if len(cleaned) != len(related):
            stripped_refs += len(related) - len(cleaned)
            c["relatedSlugs"] = cleaned
    after = len(kept)
    print(f"  inventory.json: {before} -> {after} cards (removed {before-after}; stripped {stripped_refs} stale relatedSlugs)")
    if not dry_run:
        inv["cards"] = kept
        with open(INVENTORY, "w") as f:
            json.dump(inv, f, indent=2)


def remove_drops_from_api_compare(drops_set, dry_run):
    with open(API_COMPARE) as f:
        api = json.load(f)
    before = len(api["comparisons"])
    kept = [c for c in api["comparisons"] if c["slug"] not in drops_set]
    after = len(kept)
    print(f"  api/v1/compare.json: {before} -> {after} comparisons (removed {before-after})")
    if not dry_run:
        api["comparisons"] = kept
        api["count"] = after
        with open(API_COMPARE, "w") as f:
            json.dump(api, f, indent=2)


def remove_drops_from_search_index(drops_set, dry_run):
    with open(SEARCH_INDEX) as f:
        si = json.load(f)
    before = len(si["items"])
    drop_ids = {f"compare:{s}" for s in drops_set}
    kept = [
        i for i in si["items"]
        if not (i.get("type") == "compare" and (i.get("slug") in drops_set or i.get("id") in drop_ids))
    ]
    after = len(kept)
    # Recount types
    from collections import Counter
    types = Counter(i.get("type", "unknown") for i in kept)
    print(f"  api/v1/search-index.json: {before} -> {after} items (removed {before-after})")
    if not dry_run:
        si["items"] = kept
        si["count"] = after
        si["types"] = dict(types)
        with open(SEARCH_INDEX, "w") as f:
            json.dump(si, f, indent=2)


def remove_drops_from_sitemap(drops_set, dry_run):
    with open(SITEMAP) as f:
        content = f.read()
    # Remove <url> blocks whose <loc> is in drops
    url_re = re.compile(
        r"\s*<url>\s*<loc>https://tabiji\.ai/compare/([a-z0-9\-]+)/</loc>.*?</url>",
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


def update_api_index(new_compare_count, dry_run):
    with open(API_INDEX) as f:
        idx = json.load(f)
    old = idx.get("stats", {}).get("comparisons")
    print(f"  api/v1/index.json: comparisons {old} -> {new_compare_count}")
    if not dry_run:
        idx.setdefault("stats", {})["comparisons"] = new_compare_count
        with open(API_INDEX, "w") as f:
            json.dump(idx, f, indent=2)


def delete_compare_dirs(drops_set, dry_run):
    missing = []
    deleted = 0
    for slug in drops_set:
        path = os.path.join(COMPARE_DIR, slug)
        if os.path.isdir(path):
            if not dry_run:
                shutil.rmtree(path)
            deleted += 1
        else:
            missing.append(slug)
    print(f"  compare/<slug>/: deleted {deleted} dirs ({len(missing)} already missing)")
    return deleted


def append_redirects(mapping, dry_run):
    # Append new 301s at the end of _redirects
    new_lines = []
    for slug in sorted(mapping):
        new_lines.append(f"/compare/{slug}/ {mapping[slug]} 301")
    header = "\n\n# Low-volume compare pages (< 50 total search vol) redirected to hubs\n"
    payload = header + "\n".join(new_lines) + "\n"
    print(f"  _redirects: appending {len(new_lines)} new 301 rules")
    if not dry_run:
        with open(REDIRECTS, "a") as f:
            f.write(payload)


def run_hub_rebuild(dry_run):
    print("  rebuild-compare-hubs.mjs: ", end="", flush=True)
    if dry_run:
        print("(skipped in dry-run)")
        return
    res = subprocess.run(
        ["node", "scripts/rebuild-compare-hubs.mjs"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if res.returncode != 0:
        print(f"FAILED\nSTDERR: {res.stderr}")
        sys.exit(1)
    print(res.stdout.strip() or "ok")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.dry_run:
        print("=== DRY RUN (no files modified) ===\n")

    drops = load_drops()
    drops_set = set(drops)
    print(f"Drop count (<{VOL_THRESHOLD} vol): {len(drops)}")

    with open(INVENTORY) as f:
        inv = json.load(f)

    mapping, missing = build_redirect_map(drops, inv["cards"])
    # Print distribution
    from collections import Counter
    dist = Counter(mapping.values())
    print(f"Redirect distribution:")
    for hub, n in dist.most_common():
        print(f"  {n:>4}  {hub}")
    print(f"  (missing from inventory: {len(missing)})\n")

    new_compare_count = len(inv["cards"]) - len([c for c in inv["cards"] if c["slug"] in drops_set])
    print("Applying changes:")
    remove_drops_from_inventory(drops_set, args.dry_run)
    remove_drops_from_api_compare(drops_set, args.dry_run)
    remove_drops_from_search_index(drops_set, args.dry_run)
    remove_drops_from_sitemap(drops_set, args.dry_run)
    update_api_index(new_compare_count, args.dry_run)
    delete_compare_dirs(drops_set, args.dry_run)
    append_redirects(mapping, args.dry_run)
    run_hub_rebuild(args.dry_run)

    print(f"\nDone. {'(dry run)' if args.dry_run else 'Changes applied.'}")


if __name__ == "__main__":
    main()
