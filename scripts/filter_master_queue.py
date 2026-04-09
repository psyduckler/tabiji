#!/usr/bin/env python3
"""
Filter the master queue to produce a clean pending list:
1. Remove items with 0 search volume
2. Remove items already published (status=done)
3. Remove near-duplicate slugs where a published page covers the same topic
4. Sort by search volume descending
"""

import json, os, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PP_DIR = ROOT / "popular-picks"

# Load master queue
data = json.load(open(ROOT / "popular-picks-master-queue.json"))

# Get published slugs
published = set()
for d in os.listdir(PP_DIR):
    if (PP_DIR / d / "index.html").is_file():
        published.add(d)

print(f"Master queue: {len(data):,} total entries")
print(f"Published pages: {len(published):,}")

# ── Step 1: Separate done vs pending ──
done = [e for e in data if e["status"] == "done"]
pending = [e for e in data if e["status"] == "pending"]
print(f"Done: {len(done):,}, Pending: {len(pending):,}")

# ── Step 2: Remove zero volume ──
pending = [e for e in pending if e["search_volume"] > 0]
print(f"After removing vol=0: {len(pending):,}")

# ── Step 3: Remove near-duplicates of published pages ──
# Build a normalized mapping: strip common suffixes to find the "core topic"
def normalize_slug(slug):
    """Reduce slug to its core topic for dedup matching.
    Only collapses truly synonymous suffixes, NOT different categories."""
    # Map of suffix pairs that mean the same thing
    synonym_map = {
        "-shops": "",       # chicago-ramen-shops → chicago-ramen
        "-scene": "",       # kansas-city-bbq-scene → kansas-city-bbq
        "-joints": "",      # memphis-bbq-joints → memphis-bbq
        "-spots": "",       # denver-brunch-spots → denver-brunch
        "-places": "",      # tokyo-ramen-places → tokyo-ramen
        "-eats": "",        # new-york-late-night-eats → new-york-late-night
    }
    normalized = slug
    for suffix, replacement in synonym_map.items():
        if normalized.endswith(suffix):
            normalized = normalized[:-len(suffix)] + replacement
            break
    return normalized

# Build normalized published set
published_normalized = {}
for slug in published:
    norm = normalize_slug(slug)
    published_normalized[norm] = slug

# Check each pending item against normalized published set
deduped = []
removed_dupes = []
for e in pending:
    norm = normalize_slug(e["slug"])
    # Check if a published page covers this topic
    if norm in published_normalized and e["slug"] != published_normalized[norm]:
        removed_dupes.append((e["slug"], published_normalized[norm], e["search_volume"]))
        continue
    # Also check if the exact slug matches a published page (shouldn't happen but safety check)
    if e["slug"] in published:
        continue
    deduped.append(e)

print(f"After dedup vs published: {len(deduped):,} ({len(removed_dupes)} duplicates removed)")
if removed_dupes:
    print(f"\nDuplicates removed (top 20 by volume):")
    for slug, pub, vol in sorted(removed_dupes, key=lambda x: -x[2])[:20]:
        print(f"  {slug} (vol={vol:,}) → already covered by: {pub}")

# ── Step 4: Remove internal duplicates (same city + very similar slug) ──
# Check for slugs where one is a subset of another in the pending set
seen_norms = {}
final = []
internal_dupes = []
for e in sorted(deduped, key=lambda x: -x["search_volume"]):
    norm = normalize_slug(e["slug"])
    if norm in seen_norms:
        internal_dupes.append((e["slug"], seen_norms[norm], e["search_volume"]))
        continue
    seen_norms[norm] = e["slug"]
    final.append(e)

print(f"After internal dedup: {len(final):,} ({len(internal_dupes)} internal dupes removed)")
if internal_dupes:
    print(f"\nInternal duplicates removed (top 10):")
    for slug, kept, vol in sorted(internal_dupes, key=lambda x: -x[2])[:10]:
        print(f"  {slug} (vol={vol:,}) → keeping: {kept}")

# ── Step 5: Sort by volume ──
final.sort(key=lambda x: (-x["search_volume"], x["slug"]))

# ── Stats ──
print(f"\n{'='*60}")
print(f"FINAL MASTER QUEUE")
print(f"{'='*60}")
print(f"Total pending with volume: {len(final):,}")
print(f"Volume >= 10,000:          {sum(1 for e in final if e['search_volume'] >= 10000):,}")
print(f"Volume >= 1,000:           {sum(1 for e in final if e['search_volume'] >= 1000):,}")
print(f"Volume >= 100:             {sum(1 for e in final if e['search_volume'] >= 100):,}")
print(f"Volume 1-99:               {sum(1 for e in final if 0 < e['search_volume'] < 100):,}")

# ── Write final queue ──
output_data = {
    "meta": {
        "generated": "2026-04-06",
        "total_pending": len(final),
        "total_done": len(done),
        "sources_consolidated": [
            "popular-picks-queue.json",
            "popular-picks-search-volume.csv",
            "popular-picks-round2-all.csv",
            "popular-picks-niche-opportunities.csv",
            "popular-picks-new-opportunities.csv",
            "popular-picks-top1000-niche.csv",
            "popular-picks-round2-top2500.csv",
            "docs/popular-picks-*-ideas.md (5 files)",
            "popular-picks-research-240.json",
            "research/popular-picks-targets-1000.json",
        ],
        "filters_applied": [
            "Removed entries with 0 search volume",
            "Removed entries already published",
            "Removed near-duplicates of published pages",
            "Removed internal slug duplicates (kept higher volume)",
        ],
    },
    "pending": final,
    "done": [{"slug": e["slug"], "city": e["city"], "category": e["category"],
              "search_volume": e["search_volume"]} for e in done],
}

output_path = ROOT / "popular-picks-master-queue.json"
output_path.write_text(json.dumps(output_data, indent=2, ensure_ascii=False))
print(f"\nWrote {output_path}")

# Also write CSV of just the pending items
import csv
csv_path = ROOT / "popular-picks-master-queue.csv"
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["slug", "city", "country", "category", "title", "keyword",
                     "search_volume", "cpc", "competition", "sources"])
    for e in final:
        writer.writerow([
            e["slug"], e["city"], e["country"], e["category"], e["title"],
            e["keyword"], e["search_volume"], e["cpc"], e["competition"],
            "|".join(e["sources"])
        ])
print(f"Wrote {csv_path} (pending only)")

print(f"\nTOP 30 PENDING:")
for i, e in enumerate(final[:30]):
    print(f"  {i+1:2d}. {e['slug']:45s} vol={e['search_volume']:>7,}  {e['city']}")
