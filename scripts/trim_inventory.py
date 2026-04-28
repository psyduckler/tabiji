#!/usr/bin/env python3
"""Trim compare/inventory.json and api/v1/compare.json to only include cards
whose leaf page exists on disk.

Drops stale entries (mostly inverse-name-order duplicates and unbuilt pairings)
that point to /compare/<slug>/ directories that don't exist. After running, the
two data files are aligned with the actual leaf-page count (~821).

Run this BEFORE `node scripts/rebuild-compare-hubs.mjs` so the rebuild produces
hubs and cards-data.json with the trimmed set.

Usage:
  python3 scripts/trim_inventory.py            # trim and write
  python3 scripts/trim_inventory.py --dry-run  # report only
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COMPARE = REPO / "compare"
INVENTORY = COMPARE / "inventory.json"
API_COMPARE = REPO / "api" / "v1" / "compare.json"

# Sub-hub directories aren't leaves — exclude when computing on-disk leaf set.
HUBS = {
    "asia", "australia", "bali", "cities", "colombia", "countries", "croatia",
    "culture", "egypt", "europe", "global-mixed", "greece", "hawaii", "iceland",
    "islands", "italy", "japan", "latin-america", "luxury", "maldives", "mexico",
    "middle-east-africa", "morocco", "nature", "new-zealand", "north-america",
    "oceania", "portugal", "spain", "taiwan", "thailand", "trip-style-guides",
    "vietnam",
}


def on_disk_leaves() -> set[str]:
    return {p.parent.name for p in COMPARE.glob("*/index.html") if p.parent.name not in HUBS}


def trim_inventory(disk: set[str], dry_run: bool) -> tuple[int, int]:
    data = json.loads(INVENTORY.read_text())
    cards = data["cards"]
    kept = [c for c in cards if c["slug"] in disk]
    dropped = len(cards) - len(kept)
    if not dry_run:
        data["cards"] = kept
        INVENTORY.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return len(kept), dropped


def trim_api(disk: set[str], dry_run: bool) -> tuple[int, int]:
    data = json.loads(API_COMPARE.read_text())
    comparisons = data["comparisons"]
    kept = [c for c in comparisons if c["slug"] in disk]
    dropped = len(comparisons) - len(kept)
    if not dry_run:
        data["comparisons"] = kept
        data["count"] = len(kept)
        API_COMPARE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return len(kept), dropped


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    disk = on_disk_leaves()
    print(f"On-disk leaves: {len(disk)}")

    inv_kept, inv_dropped = trim_inventory(disk, args.dry_run)
    print(f"inventory.json:          kept {inv_kept:>4}, dropped {inv_dropped:>4}")

    api_kept, api_dropped = trim_api(disk, args.dry_run)
    print(f"api/v1/compare.json:     kept {api_kept:>4}, dropped {api_dropped:>4}")

    if args.dry_run:
        print("\n[dry-run — no files modified]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
