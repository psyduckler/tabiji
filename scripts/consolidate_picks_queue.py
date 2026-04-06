#!/usr/bin/env python3
"""
Consolidate all popular-picks idea sources into one master queue.

Sources merged:
  - popular-picks-queue.json (4,995 entries with status)
  - popular-picks-search-volume.csv (1,692 with volume)
  - popular-picks-round2-all.csv (16,694 with volume)
  - popular-picks-niche-opportunities.csv (8,200 with volume)
  - popular-picks-new-opportunities.csv (2,640 with volume)
  - popular-picks-top1000-niche.csv (1,999 with volume)
  - popular-picks-round2-top2500.csv (2,500 with volume)
  - docs/popular-picks-*-ideas.md (2,300 ideas)
  - popular-picks-research-240.json (120 prioritized)
  - research/popular-picks-targets-1000.json (1,000 targets)

Output: popular-picks-master-queue.json — single source of truth
"""

import csv, json, os, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PP_DIR = ROOT / "popular-picks"

# Track all entries by slug
master = {}  # slug -> entry dict


def ensure_entry(slug):
    if slug not in master:
        master[slug] = {
            "slug": slug,
            "city": "",
            "country": "",
            "category": "",
            "title": "",
            "keyword": "",
            "search_volume": 0,
            "cpc": 0,
            "competition": 0,
            "status": "pending",
            "sources": [],
        }
    return master[slug]


def merge_field(entry, field, value):
    """Set field if not already set (first non-empty wins)."""
    if value and not entry.get(field):
        entry[field] = value


def merge_volume(entry, vol, cpc=0, comp=0):
    """Take the highest search volume across sources."""
    try:
        vol = int(float(vol)) if vol else 0
    except (ValueError, TypeError):
        vol = 0
    if vol > entry.get("search_volume", 0):
        entry["search_volume"] = vol
    try:
        cpc_f = float(cpc) if cpc else 0
    except (ValueError, TypeError):
        cpc_f = 0
    if cpc_f > entry.get("cpc", 0):
        entry["cpc"] = cpc_f
    try:
        comp_f = float(comp) if comp else 0
    except (ValueError, TypeError):
        comp_f = 0
    if comp_f > entry.get("competition", 0):
        entry["competition"] = comp_f


def add_source(entry, source):
    if source not in entry["sources"]:
        entry["sources"].append(source)


# ═══════════════════════════════════════════════════════════
# 1. Load existing queue (has status info)
# ═══════════════════════════════════════════════════════════
print("Loading popular-picks-queue.json...")
queue_file = ROOT / "popular-picks-queue.json"
if queue_file.exists():
    queue = json.loads(queue_file.read_text())
    for item in queue:
        slug = item.get("slug", "").strip()
        if not slug:
            continue
        e = ensure_entry(slug)
        merge_field(e, "city", item.get("city", ""))
        merge_field(e, "country", item.get("country", ""))
        merge_field(e, "category", item.get("category", ""))
        merge_field(e, "title", item.get("title", ""))
        if item.get("status") == "done":
            e["status"] = "done"
        add_source(e, "queue")
    print(f"  → {len(queue)} entries loaded")


# ═══════════════════════════════════════════════════════════
# 2. Load CSV search volume files
# ═══════════════════════════════════════════════════════════
csv_files = [
    ("popular-picks-search-volume.csv", "sv1"),
    ("popular-picks-round2-all.csv", "round2"),
    ("popular-picks-niche-opportunities.csv", "niche"),
    ("popular-picks-new-opportunities.csv", "new-opps"),
    ("popular-picks-top1000-niche.csv", "top1k-niche"),
    ("popular-picks-round2-top2500.csv", "round2-top"),
]

for filename, source_name in csv_files:
    filepath = ROOT / filename
    if not filepath.exists():
        print(f"  SKIP {filename} (not found)")
        continue
    print(f"Loading {filename}...")
    count = 0
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            slug = row.get("slug", "").strip()
            if not slug:
                continue
            e = ensure_entry(slug)
            merge_field(e, "city", row.get("city", ""))
            merge_field(e, "country", row.get("country", ""))
            merge_field(e, "category", row.get("category", ""))
            merge_field(e, "title", row.get("title", ""))
            merge_field(e, "keyword", row.get("keyword", ""))
            merge_volume(e, row.get("search_volume", 0),
                         row.get("cpc", 0), row.get("competition", 0))
            add_source(e, source_name)
            count += 1
    print(f"  → {count} rows loaded")


# ═══════════════════════════════════════════════════════════
# 3. Load markdown idea docs
# ═══════════════════════════════════════════════════════════
md_files = [
    "docs/popular-picks-100-ideas.md",
    "docs/popular-picks-200-more-ideas.md",
    "docs/popular-picks-500-more-ideas.md",
    "docs/popular-picks-500-even-more-ideas.md",
    "docs/popular-picks-1000-more-ideas.md",
]

for md_file in md_files:
    filepath = ROOT / md_file
    if not filepath.exists():
        print(f"  SKIP {md_file} (not found)")
        continue
    print(f"Loading {md_file}...")
    text = filepath.read_text(encoding='utf-8')
    # Parse markdown tables: | slug | city | category | title |
    count = 0
    for line in text.split('\n'):
        line = line.strip()
        if not line.startswith('|') or line.startswith('|--') or line.startswith('| Slug') or line.startswith('| slug'):
            continue
        parts = [p.strip().strip('`') for p in line.split('|')[1:-1]]
        if len(parts) < 2:
            continue
        slug = parts[0].strip()
        if not slug or slug == 'Slug' or slug == '---':
            continue
        e = ensure_entry(slug)
        if len(parts) >= 2:
            merge_field(e, "city", parts[1])
        if len(parts) >= 3:
            merge_field(e, "category", parts[2])
        if len(parts) >= 4:
            merge_field(e, "title", parts[3])
        add_source(e, md_file.split('/')[-1].replace('.md', ''))
        count += 1
    print(f"  → {count} ideas parsed")


# ═══════════════════════════════════════════════════════════
# 4. Load research JSON files
# ═══════════════════════════════════════════════════════════
research_files = [
    "popular-picks-research-240.json",
    "research/popular-picks-targets-1000.json",
]

for rf in research_files:
    filepath = ROOT / rf
    if not filepath.exists():
        print(f"  SKIP {rf} (not found)")
        continue
    print(f"Loading {rf}...")
    data = json.loads(filepath.read_text())
    items = data if isinstance(data, list) else data.get("targets", data.get("items", []))
    count = 0
    for item in items:
        slug = item.get("slug", "").strip()
        if not slug:
            continue
        e = ensure_entry(slug)
        merge_field(e, "city", item.get("city", ""))
        merge_field(e, "country", item.get("country", ""))
        merge_field(e, "category", item.get("category", ""))
        merge_field(e, "title", item.get("title", ""))
        add_source(e, rf.split('/')[-1].replace('.json', ''))
        count += 1
    print(f"  → {count} entries loaded")


# ═══════════════════════════════════════════════════════════
# 5. Mark published pages as "done"
# ═══════════════════════════════════════════════════════════
print("\nChecking published pages...")
published = 0
if PP_DIR.is_dir():
    for d in os.listdir(PP_DIR):
        if (PP_DIR / d / "index.html").is_file():
            e = ensure_entry(d)
            e["status"] = "done"
            add_source(e, "published")
            published += 1
print(f"  → {published} published pages marked as done")


# ═══════════════════════════════════════════════════════════
# 6. Generate keyword from slug if missing
# ═══════════════════════════════════════════════════════════
for slug, entry in master.items():
    if not entry["keyword"]:
        entry["keyword"] = slug.replace("-", " ")


# ═══════════════════════════════════════════════════════════
# 7. Sort and write output
# ═══════════════════════════════════════════════════════════
entries = sorted(master.values(), key=lambda x: (-x["search_volume"], x["slug"]))

# Stats
total = len(entries)
done = sum(1 for e in entries if e["status"] == "done")
pending = total - done
with_vol = sum(1 for e in entries if e["search_volume"] > 0)
high_vol = sum(1 for e in entries if e["search_volume"] >= 1000)

print(f"\n{'='*60}")
print(f"MASTER QUEUE STATS")
print(f"{'='*60}")
print(f"Total unique slugs:     {total:,}")
print(f"  Done (published):     {done:,}")
print(f"  Pending:              {pending:,}")
print(f"  With search volume:   {with_vol:,}")
print(f"  Volume >= 1,000:      {high_vol:,}")
print(f"  Volume >= 10,000:     {sum(1 for e in entries if e['search_volume'] >= 10000):,}")

# Top 20 pending by volume
print(f"\nTOP 20 PENDING BY SEARCH VOLUME:")
pending_entries = [e for e in entries if e["status"] == "pending" and e["search_volume"] > 0]
for i, e in enumerate(pending_entries[:20]):
    print(f"  {i+1:2d}. {e['slug']:40s} vol={e['search_volume']:>7,}  ({e['city']}, {e['category']})")

# Write master queue
output = ROOT / "popular-picks-master-queue.json"
output.write_text(json.dumps(entries, indent=2, ensure_ascii=False))
print(f"\nWrote {output} ({total:,} entries)")

# Also write a CSV for easy spreadsheet viewing
csv_output = ROOT / "popular-picks-master-queue.csv"
with open(csv_output, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["slug", "city", "country", "category", "title", "keyword",
                     "search_volume", "cpc", "competition", "status", "sources"])
    for e in entries:
        writer.writerow([
            e["slug"], e["city"], e["country"], e["category"], e["title"],
            e["keyword"], e["search_volume"], e["cpc"], e["competition"],
            e["status"], "|".join(e["sources"])
        ])
print(f"Wrote {csv_output}")
