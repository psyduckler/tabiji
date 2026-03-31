#!/usr/bin/env python3
"""
Task 1a: Add sectionFreshness block to all api/v1/safety/ profiles.
Idempotent — skips files that already have sectionFreshness.
Uses each file's existing top-level lastUpdated for all section timestamps.
"""

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
SAFETY_DIR = ROOT / "api" / "v1" / "safety"

SECTION_KEYS = [
    ("emergency", 30),
    ("travelAdvisory", 14),
    ("travelAdvisoryUK", 14),
    ("healthcare", 90),
    ("medications", 90),
    ("scams", 60),
    ("connectivity", 60),
    ("hospitals", 180),
    ("disasterResponse", 180),
    ("practical", 180),
]


def build_section_freshness(last_updated: str) -> dict:
    return {
        key: {"lastUpdated": last_updated, "ttlDays": ttl}
        for key, ttl in SECTION_KEYS
    }


def process_file(path: Path) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))

    if "sectionFreshness" in data:
        print(f"  SKIP (already has sectionFreshness): {path.name}")
        return False

    last_updated = data.get("lastUpdated", "2026-03-31T00:00:00Z")
    data["sectionFreshness"] = build_section_freshness(last_updated)

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  PATCHED: {path.name}  (lastUpdated={last_updated})")
    return True


def main():
    files = sorted(SAFETY_DIR.glob("*.json"))
    # Exclude index file if it exists
    files = [f for f in files if f.name != "safety.json"]

    patched = 0
    skipped = 0
    for f in files:
        if process_file(f):
            patched += 1
        else:
            skipped += 1

    print(f"\nDone. Patched={patched}, Skipped={skipped}, Total={len(files)}")


if __name__ == "__main__":
    main()
