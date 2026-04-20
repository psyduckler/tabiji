#!/usr/bin/env python3
"""
Pull Semrush US search volumes for every popular-picks page.
Keyword = slug with dashes replaced by spaces (e.g. nara-udon -> "nara udon").
Outputs sorted CSV + tiered CSV + summary.
"""

import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter

API_KEY = "466c49b8794c2ba3d09ad2afd1964cd0"
DATABASE = "us"

ROOT = "/Users/bjh/Documents/tabiji/.claude/worktrees/happy-tharp-5601b2"
PICKS_DIR = os.path.join(ROOT, "popular-picks")
METADATA = os.path.join(PICKS_DIR, "picks-metadata.json")
ANALYSIS = os.path.join(ROOT, "scripts", "compare-analysis")  # reuse dir
OUT_CSV = os.path.join(ANALYSIS, "picks-search-volumes.csv")
TIERS_CSV = os.path.join(ANALYSIS, "picks-tiers.csv")
SUMMARY_MD = os.path.join(ANALYSIS, "picks-tiers-summary.md")

BATCH_SIZE = 100


def list_slugs():
    # Use filesystem — authoritative
    slugs = []
    for entry in sorted(os.listdir(PICKS_DIR)):
        if os.path.isdir(os.path.join(PICKS_DIR, entry)):
            slugs.append(entry)
    return slugs


def load_metadata():
    with open(METADATA) as f:
        return json.load(f)


def slug_to_keyword(slug):
    return slug.replace("-", " ")


def fetch_batch(phrases):
    payload = ";".join(phrases)
    url = (
        "https://api.semrush.com/?type=phrase_these"
        f"&key={API_KEY}"
        f"&phrase={urllib.parse.quote(payload)}"
        f"&database={DATABASE}"
        "&export_columns=Ph,Nq"
    )
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8").strip()
    except Exception as e:
        print(f"  Batch error: {e}", file=sys.stderr)
        return {}

    out = {}
    lines = body.split("\n")
    if len(lines) < 2:
        return out
    for line in lines[1:]:
        parts = line.split(";")
        if len(parts) >= 2:
            try:
                out[parts[0]] = int(parts[1])
            except ValueError:
                out[parts[0]] = 0
    return out


def tier_of(vol):
    # Pick tiers — popular-picks are longer-tail than compare pages
    if vol >= 500:
        return 1
    if vol >= 100:
        return 2
    if vol >= 20:
        return 3
    return 0  # drop


def main():
    os.makedirs(ANALYSIS, exist_ok=True)

    slugs = list_slugs()
    meta = load_metadata()
    print(f"Popular-picks pages on disk: {len(slugs)}")
    print(f"Metadata entries: {len(meta)}")
    missing_meta = [s for s in slugs if s not in meta]
    print(f"Slugs without metadata: {len(missing_meta)}")

    # Build keyword list
    pairs = [(s, slug_to_keyword(s)) for s in slugs]
    keywords = [kw for _, kw in pairs]

    # Dedupe for fetch (unlikely but safe)
    seen = set()
    uniq = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            uniq.append(kw)

    print(f"Unique keywords to fetch: {len(uniq)}")
    print(f"Batches of {BATCH_SIZE}: {(len(uniq) + BATCH_SIZE - 1) // BATCH_SIZE}")

    fetched = {}
    for i in range(0, len(uniq), BATCH_SIZE):
        batch = uniq[i : i + BATCH_SIZE]
        res = fetch_batch(batch)
        for p in batch:
            fetched[p] = res.get(p, 0)
        print(
            f"  batch {i // BATCH_SIZE + 1}: {len(batch)} phrases, "
            f"sample: {batch[0]}={res.get(batch[0], 0)}"
        )
        time.sleep(0.3)

    # Build result rows — distinguish hub pages from topic pages
    rows = []
    for slug, kw in pairs:
        card = meta.get(slug, {})
        vol = fetched.get(kw, 0)
        title = card.get("title", "")
        # Hub pages are countrywide rollups titled "Popular Picks in X"
        page_type = "hub" if title.startswith("Popular Picks in ") else "topic"
        rows.append({
            "slug": slug,
            "url": f"https://tabiji.ai/popular-picks/{slug}/",
            "keyword": kw,
            "volume": vol,
            "title": title,
            "city": card.get("city", ""),
            "category": card.get("category", ""),
            "page_type": page_type,
            "tier": tier_of(vol),
        })

    rows.sort(key=lambda r: (-r["volume"], r["slug"]))

    fields_raw = ["slug", "url", "keyword", "volume", "title", "city", "category", "page_type"]
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields_raw)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in fields_raw})
    print(f"\nWrote {OUT_CSV}")

    fields_tier = fields_raw + ["tier"]
    with open(TIERS_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields_tier)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in fields_tier})
    print(f"Wrote {TIERS_CSV}")

    # Split: hubs vs topics (very different volume profiles)
    hubs = [r for r in rows if r["page_type"] == "hub"]
    topics = [r for r in rows if r["page_type"] == "topic"]

    def tier_breakdown(rows_subset):
        c = Counter(r["tier"] for r in rows_subset)
        return c

    tc_all = tier_breakdown(rows)
    tc_hub = tier_breakdown(hubs)
    tc_top = tier_breakdown(topics)

    print()
    print("=" * 60)
    print(f"Total pages: {len(rows)} ({len(hubs)} hubs, {len(topics)} topics)")
    print()
    print(f"{'':24} {'ALL':>6} {'HUBS':>6} {'TOPICS':>7}")
    print(f"Tier 1 (>=500 vol):    {tc_all[1]:>6} {tc_hub[1]:>6} {tc_top[1]:>7}")
    print(f"Tier 2 (100-499):      {tc_all[2]:>6} {tc_hub[2]:>6} {tc_top[2]:>7}")
    print(f"Tier 3 (20-99):        {tc_all[3]:>6} {tc_hub[3]:>6} {tc_top[3]:>7}")
    print(f"Drop   (<20):          {tc_all[0]:>6} {tc_hub[0]:>6} {tc_top[0]:>7}")

    # Markdown summary
    t1 = [r for r in topics if r["tier"] == 1]
    t2 = [r for r in topics if r["tier"] == 2]
    t3 = [r for r in topics if r["tier"] == 3]
    drop = [r for r in topics if r["tier"] == 0]

    cats = Counter(r["category"] for r in topics if r["volume"] >= 20)
    cities = Counter(r["city"] for r in topics if r["volume"] >= 20)

    lines = [
        "# Popular-picks search-volume tier list",
        "",
        f"- **Total pages:** {len(rows)}  ({len(hubs)} country-hub pages + {len(topics)} topic pages)",
        "- **Method:** Semrush US `phrase_these`, one lookup per page using slug-as-keyword",
        "  (e.g. `nara-udon` → `\"nara udon\"`). No direction variants.",
        "",
        "## ⚠️ Two page types — tier separately",
        "",
        f"**Country-hub pages ({len(hubs)})** have slugs like `iran`, `japan`, `mexico`. Raw volumes ",
        "are astronomical (iran = 1.5M) but that's news/politics, not travel intent. These should be ",
        "kept on brand/taxonomy grounds, not SEO — treat as navigation, not landing pages.",
        "",
        f"**Topic pages ({len(topics)})** have slugs like `nara-udon`, `chicago-pizza`. These are the ",
        "real editorial decisions — their volume reflects actual travel-intent demand.",
        "",
        "## Tier breakdown — TOPIC pages only",
        "",
        "| Tier | Volume | Count | Action |",
        "|------|-------:|------:|--------|",
        f"| **1 — Flagship** | ≥ 500 | {tc_top[1]} | Heavy content investment |",
        f"| **2 — Solid** | 100–499 | {tc_top[2]} | Moderate upkeep |",
        f"| **3 — Maintain** | 20–99 | {tc_top[3]} | Keep alive |",
        f"| **Drop** | < 20 | {tc_top[0]} | Consider removing |",
        "",
        f"**Topic keep:** {tc_top[1] + tc_top[2] + tc_top[3]}   |   **Topic drop:** {tc_top[0]}",
        "",
        "## Tier breakdown — HUB pages",
        "",
        "| Tier | Volume | Count |",
        "|------|-------:|------:|",
        f"| 1 (≥ 500) | keep all | {tc_hub[1]} |",
        f"| 2 (100–499) | keep all | {tc_hub[2]} |",
        f"| 3 (20–99) | review | {tc_hub[3]} |",
        f"| Drop (< 20) | review | {tc_hub[0]} |",
        "",
        "_Hub pages should generally be kept regardless of volume — they're navigation, not landing SEO._",
        "",
        "## TOPIC Tier 1 — Flagship (top 60)",
        "",
        "| Vol | Slug | Title |",
        "|----:|------|-------|",
    ]
    for r in t1[:60]:
        t = r["title"].replace("|", "\\|")
        lines.append(f"| {r['volume']:,} | [{r['slug']}](popular-picks/{r['slug']}/) | {t} |")
    if len(t1) > 60:
        lines.append(f"| ... | {len(t1) - 60} more in CSV | |")
    lines.append("")

    lines.append("## TOPIC Tier 2 sample (top 30)")
    lines.append("")
    lines.append("| Vol | Slug |")
    lines.append("|----:|------|")
    for r in t2[:30]:
        lines.append(f"| {r['volume']:,} | {r['slug']} |")
    lines.append("")

    lines.append("## TOPIC Tier 3 sample (top 25)")
    lines.append("")
    lines.append("| Vol | Slug |")
    lines.append("|----:|------|")
    for r in t3[:25]:
        lines.append(f"| {r['volume']:,} | {r['slug']} |")
    lines.append("")

    lines.append("## Top categories among kept topic pages (≥ 20 vol)")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("|----------|------:|")
    for cat, n in cats.most_common(20):
        lines.append(f"| {cat} | {n} |")
    lines.append("")

    lines.append("## Top cities among kept topic pages (≥ 20 vol)")
    lines.append("")
    lines.append("| City | Count |")
    lines.append("|------|------:|")
    for city, n in cities.most_common(20):
        lines.append(f"| {city} | {n} |")
    lines.append("")

    lines.append("## TOPIC drop sample — highest vol below the < 20 cutoff")
    lines.append("")
    lines.append("| Vol | Slug |")
    lines.append("|----:|------|")
    for r in drop[:20]:
        lines.append(f"| {r['volume']:,} | {r['slug']} |")
    lines.append("")

    with open(SUMMARY_MD, "w") as f:
        f.write("\n".join(lines))
    print(f"Wrote {SUMMARY_MD}")


if __name__ == "__main__":
    main()
