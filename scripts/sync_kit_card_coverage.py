#!/usr/bin/env python3
"""
Sync cardCoverage from api/v1/safety/{iso2}.json into kit/data/safety/{iso2}.json.
Skips kit files that already have cardCoverage.
"""

import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_SAFETY_DIR = os.path.join(REPO_ROOT, "api/v1/safety")
KIT_SAFETY_DIR = os.path.join(REPO_ROOT, "kit/data/safety")


def main():
    patched = 0
    skipped = 0
    missing_kit = 0
    no_coverage = 0

    for fname in sorted(os.listdir(API_SAFETY_DIR)):
        if not fname.endswith(".json") or fname == "safety.json":
            continue

        api_path = os.path.join(API_SAFETY_DIR, fname)
        with open(api_path) as f:
            api_data = json.load(f)

        card_coverage = api_data.get("cardCoverage")
        if not card_coverage:
            no_coverage += 1
            continue

        kit_path = os.path.join(KIT_SAFETY_DIR, fname)
        if not os.path.exists(kit_path):
            missing_kit += 1
            continue

        with open(kit_path) as f:
            kit_data = json.load(f)

        if "cardCoverage" in kit_data:
            skipped += 1
            continue

        kit_data["cardCoverage"] = card_coverage

        with open(kit_path, "w") as f:
            json.dump(kit_data, f, indent=2)

        patched += 1

    print(
        f"Patched: {patched}, Skipped (already had cardCoverage): {skipped}, "
        f"Missing kit file: {missing_kit}, API file had no cardCoverage: {no_coverage}"
    )


if __name__ == "__main__":
    main()
