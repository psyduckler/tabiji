#!/usr/bin/env python3
"""
Regenerate api/v1/safety.json index from all 55 country files.
"""

import json
from pathlib import Path

SAFETY_DIR = Path(__file__).parent.parent / "api" / "v1" / "safety"
INDEX_FILE = Path(__file__).parent.parent / "api" / "v1" / "safety.json"
LAST_UPDATED = "2026-03-31T00:00:00Z"
BASE_URL = "https://tabiji.ai/api/v1/safety"


def main():
    profiles = []

    for filepath in sorted(SAFETY_DIR.glob("*.json")):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        iso2 = data.get("iso2", "").lower()
        name = data.get("name", "")
        last_updated = data.get("lastUpdated", LAST_UPDATED)
        advisory = data.get("travelAdvisory", {})
        advisory_level = advisory.get("level", None)
        advisory_level_text = advisory.get("levelText", "")

        entry = {
            "id": f"safety:{iso2}",
            "iso2": data.get("iso2", iso2.upper()),
            "name": name,
            "lastUpdated": last_updated,
            "advisoryLevel": advisory_level,
            "advisoryLevelText": advisory_level_text,
            "url": f"{BASE_URL}/{iso2}.json"
        }
        profiles.append(entry)

    # Sort alphabetically by country name
    profiles.sort(key=lambda x: x["name"])

    index = {
        "count": len(profiles),
        "lastUpdated": LAST_UPDATED,
        "profiles": profiles
    }

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Written {INDEX_FILE} with {len(profiles)} profiles.")
    for p in profiles:
        print(f"  {p['iso2']} — {p['name']} (level {p['advisoryLevel']})")


if __name__ == "__main__":
    main()
