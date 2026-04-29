#!/usr/bin/env python3
"""
extract.py — reads /api/v1/scams/*.json, normalizes each scam against the
canonical atlas taxonomy in data/entries.json + data/synonyms.json, and
emits build-time data:

  output/auto-assigned.json    — scams confidently mapped to an atlas entry
  output/ambiguous-queue.json  — scams that need Claude API recategorization
  output/dropped.json          — scams matching DROP rules (noise tags)
  output/entry-inventory.json  — per-entry counts + country/city coverage

No public API surface. Pure stdlib. Run from repo root or this directory.

Usage:
    python3 generators/scam-atlas/extract.py
    python3 generators/scam-atlas/extract.py --verbose
"""

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

# Paths — robust to invocation directory
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
SCAMS_DIR = REPO_ROOT / "api" / "v1" / "scams"
DATA_DIR = HERE / "data"
OUT_DIR = HERE / "output"


def load_taxonomy():
    entries_doc = json.loads((DATA_DIR / "entries.json").read_text())
    synonyms_doc = json.loads((DATA_DIR / "synonyms.json").read_text())

    entries = [e for e in entries_doc["entries"] if "slug" in e]
    canonical_slugs = {e["slug"] for e in entries}

    # Reverse index: synonym → canonical slug
    # Order matters: longer synonyms first to prefer specific over broad
    synonym_to_slug = {}
    for e in entries:
        for syn in e.get("synonyms", []):
            synonym_to_slug.setdefault(syn.lower(), e["slug"])
        synonym_to_slug[e["slug"].lower()] = e["slug"]

    category_map = {k: v for k, v in synonyms_doc["categoryMap"].items() if not k.startswith("$")}
    tag_map = {k: v for k, v in synonyms_doc["tagMap"].items() if not k.startswith("$")}
    noise_patterns = [re.compile(p, re.I) for p in synonyms_doc["noiseTagPatterns"]["patterns"]]

    return entries, canonical_slugs, synonym_to_slug, category_map, tag_map, noise_patterns


def is_noise(tag: str, noise_patterns) -> bool:
    return any(p.match(tag) for p in noise_patterns)


def assign_scam(scam, category_map, tag_map, synonym_to_slug, noise_patterns, canonical_slugs):
    """Return (atlas_entry_slug | None, confidence_label)."""
    cat = (scam.get("category") or "").lower().strip()
    tags = [(t or "").lower().strip() for t in scam.get("tags", [])]
    title = (scam.get("name") or "").lower()

    # Step 1: direct category match
    if cat in category_map:
        target = category_map[cat]
        if target not in ("AMBIGUOUS", "DROP"):
            return target, "category-direct"

    # Step 2: tag match (prefer specific over generic — sort tags by tagMap match priority)
    tag_hits = []
    for t in tags:
        if t in tag_map:
            v = tag_map[t]
            if v not in ("AMBIGUOUS", "DROP"):
                tag_hits.append(v)
    if tag_hits:
        # If multiple distinct tag hits, prefer the most specific entry (one with parentEntry)
        # For now: take first match
        return tag_hits[0], "tag-direct"

    # Step 3: synonym in title (fuzzy)
    # Sort synonyms by length descending to prefer longer/more-specific matches
    for syn in sorted(synonym_to_slug.keys(), key=len, reverse=True):
        if len(syn) < 4:  # skip very short synonyms to avoid false positives
            continue
        if syn in title:
            return synonym_to_slug[syn], "title-synonym-match"

    # Step 4: noise check — if all tags are noise, drop
    non_noise_tags = [t for t in tags if t and not is_noise(t, noise_patterns)]
    if not non_noise_tags and not cat:
        return None, "drop-noise"

    # Step 5: ambiguous — needs Claude
    return None, "ambiguous"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    entries, canonical_slugs, synonym_to_slug, category_map, tag_map, noise_patterns = load_taxonomy()
    OUT_DIR.mkdir(exist_ok=True)

    auto_assigned = []
    ambiguous = []
    dropped = []
    confidence_counts = defaultdict(int)

    scam_files = sorted(SCAMS_DIR.glob("*.json"))
    for f in scam_files:
        try:
            d = json.loads(f.read_text())
        except json.JSONDecodeError as exc:
            print(f"  ⚠ skipping {f.name}: {exc}")
            continue

        city = d.get("slug", f.stem)
        country = d.get("country", "")
        cc = d.get("countryCode", "")

        for s in d.get("scams", []):
            target, confidence = assign_scam(
                s, category_map, tag_map, synonym_to_slug, noise_patterns, canonical_slugs
            )
            confidence_counts[confidence] += 1
            record = {
                "scamId": s.get("id"),
                "city": city,
                "country": country,
                "cc": cc,
                "name": s.get("name", ""),
                "origCategory": s.get("category", ""),
                "origTags": s.get("tags", []),
                "severity": s.get("severity", ""),
                "frequency": s.get("frequency", ""),
            }
            if confidence == "drop-noise":
                dropped.append(record)
            elif target:
                record["atlasEntry"] = target
                record["confidence"] = confidence
                auto_assigned.append(record)
            else:
                record["tldr"] = s.get("tldr", "")
                record["description"] = (s.get("description") or "")[:400]
                ambiguous.append(record)

    # Per-entry inventory + threshold check
    by_entry = defaultdict(list)
    for r in auto_assigned:
        by_entry[r["atlasEntry"]].append(r)

    inventory = {}
    for entry in entries:
        slug = entry["slug"]
        scams = by_entry.get(slug, [])
        countries = sorted({s["country"] for s in scams if s["country"]})
        cities = sorted({s["city"] for s in scams if s["city"]})
        inventory[slug] = {
            "name": entry["name"],
            "entryStyle": entry["entryStyle"],
            "parentEntry": entry.get("parentEntry"),
            "count": len(scams),
            "countryCount": len(countries),
            "cityCount": len(cities),
            "countries": countries,
            "cities": cities[:20],  # cap for readability
            "meetsThreshold": len(scams) >= 10 and len(countries) >= 4,
        }

    # Write outputs
    (OUT_DIR / "auto-assigned.json").write_text(json.dumps(auto_assigned, indent=2))
    (OUT_DIR / "ambiguous-queue.json").write_text(json.dumps(ambiguous, indent=2))
    (OUT_DIR / "dropped.json").write_text(json.dumps(dropped, indent=2))
    (OUT_DIR / "entry-inventory.json").write_text(json.dumps(inventory, indent=2))

    # Stats
    total = len(auto_assigned) + len(ambiguous) + len(dropped)
    print(f"\n=== EXTRACT REPORT ===")
    print(f"Source files:      {len(scam_files)} city scam JSONs")
    print(f"Total scams:       {total}")
    print(f"  Auto-assigned:   {len(auto_assigned):>5}  ({100*len(auto_assigned)/max(total,1):.1f}%)")
    print(f"  Ambiguous queue: {len(ambiguous):>5}  ({100*len(ambiguous)/max(total,1):.1f}%)  → recategorize.py")
    print(f"  Dropped (noise): {len(dropped):>5}  ({100*len(dropped)/max(total,1):.1f}%)")

    print(f"\nAuto-assignment confidence breakdown:")
    for conf, n in sorted(confidence_counts.items(), key=lambda x: -x[1]):
        print(f"  {n:>5}  {conf}")

    # Threshold check
    below = [(s, v) for s, v in inventory.items() if not v["meetsThreshold"]]
    above = len(inventory) - len(below)
    print(f"\nEntry threshold (≥10 scams across ≥4 countries):")
    print(f"  Pass: {above} / {len(inventory)}")
    print(f"  Fail: {len(below)}")

    if below and args.verbose:
        print(f"\nEntries below threshold (consider folding):")
        for slug, v in sorted(below, key=lambda x: x[1]["count"]):
            print(f"  [{v['count']:>3}] {slug}  ({v['countryCount']} countries)")

    print(f"\nOutputs written to: {OUT_DIR.relative_to(REPO_ROOT)}/")


if __name__ == "__main__":
    main()
