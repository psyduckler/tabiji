#!/usr/bin/env python3
"""
Patch each api/v1/safety/{iso2}.json with mapIntegration guidance.
Skips files that already have mapIntegration.
Also syncs to kit/data/safety/{iso2}.json.
"""

import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_SAFETY_DIR = os.path.join(REPO_ROOT, "api/v1/safety")
KIT_SAFETY_DIR = os.path.join(REPO_ROOT, "kit/data/safety")


def make_map_integration(data):
    """Build mapIntegration block based on what's available in the safety profile."""
    embassies = data.get("embassies") or []
    embassy_coords = (
        isinstance(embassies, list)
        and len(embassies) > 0
        and all("lat" in e and "lng" in e for e in embassies)
    )

    return {
        "recommendedZoom": {"city": 13, "country": 7},
        "offlineTileSizeEstimate": "~50–100MB at zoom 10–15 for full country coverage",
        "coordinateSystem": "WGS84 (EPSG:4326)",
        "embassyCoordinatesAvailable": embassy_coords,
        "hospitalCoordinatesAvailable": False,
        "provider": "openstreetmap",
        "offlineMapsGuideUrl": "/api/v1/offline-maps.json",
    }


def patch_file(path, dry_run=False):
    with open(path) as f:
        data = json.load(f)

    if "mapIntegration" in data:
        return False

    data["mapIntegration"] = make_map_integration(data)

    if not dry_run:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    return True


def main():
    api_patched = 0
    api_skipped = 0
    kit_patched = 0
    kit_skipped = 0
    kit_missing = 0

    for fname in sorted(os.listdir(API_SAFETY_DIR)):
        if not fname.endswith(".json") or fname == "safety.json":
            continue

        api_path = os.path.join(API_SAFETY_DIR, fname)
        if patch_file(api_path):
            api_patched += 1
        else:
            api_skipped += 1

        # Sync to kit
        kit_path = os.path.join(KIT_SAFETY_DIR, fname)
        if not os.path.exists(kit_path):
            kit_missing += 1
            continue

        with open(api_path) as f:
            api_data = json.load(f)
        mi = api_data.get("mapIntegration")
        if not mi:
            continue

        with open(kit_path) as f:
            kit_data = json.load(f)
        if "mapIntegration" in kit_data:
            kit_skipped += 1
            continue

        kit_data["mapIntegration"] = mi
        with open(kit_path, "w") as f:
            json.dump(kit_data, f, indent=2)
        kit_patched += 1

    print(
        f"API — Patched: {api_patched}, Skipped: {api_skipped}\n"
        f"Kit — Patched: {kit_patched}, Skipped: {kit_skipped}, Missing: {kit_missing}"
    )


if __name__ == "__main__":
    main()
