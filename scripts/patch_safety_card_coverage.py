#!/usr/bin/env python3
"""
Patch each api/v1/safety/{iso2}.json with cardCoverage from coverage-by-country.json.
Skips files that already have cardCoverage.
"""

import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAFETY_DIR = os.path.join(REPO_ROOT, "api/v1/safety")
COVERAGE_FILE = os.path.join(REPO_ROOT, "api/v1/cards/coverage-by-country.json")


def main():
    with open(COVERAGE_FILE) as f:
        coverage = json.load(f)
    countries = coverage["countries"]

    patched = 0
    skipped = 0
    missing = 0

    for fname in sorted(os.listdir(SAFETY_DIR)):
        if not fname.endswith(".json") or fname == "safety.json":
            continue
        path = os.path.join(SAFETY_DIR, fname)
        with open(path) as f:
            data = json.load(f)

        if "cardCoverage" in data:
            skipped += 1
            continue

        iso2 = (data.get("iso2") or "").upper()
        if not iso2 or iso2 not in countries:
            missing += 1
            continue

        country_coverage = countries[iso2]
        top_cards = country_coverage["topCards"]

        # Build stripped-down topCards (no score field for the safety profile)
        card_list = [
            {
                "slug": tc["slug"],
                "name": tc["name"],
                "relevantBenefits": tc["relevantBenefits"],
                "cardUrl": tc["cardUrl"],
            }
            for tc in top_cards
        ]

        data["cardCoverage"] = {
            "topCards": card_list,
            "scoringFactors": country_coverage["scoringFactors"],
            "coverageGuideUrl": "/api/v1/cards/coverage-by-country.json",
        }

        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        patched += 1

    print(f"Patched: {patched}, Skipped (already had cardCoverage): {skipped}, Missing from coverage: {missing}")


if __name__ == "__main__":
    main()
