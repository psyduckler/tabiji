#!/usr/bin/env python3
"""
Task 3b: Sync emergencyWorkflows from api/v1/safety/ to kit/data/safety/.
Reads each api file, extracts emergencyWorkflows, patches the matching kit file.
Idempotent — skips kit files that already have emergencyWorkflows.
"""

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
API_SAFETY_DIR = ROOT / "api" / "v1" / "safety"
KIT_SAFETY_DIR = ROOT / "kit" / "data" / "safety"


def main():
    patched = 0
    skipped = 0
    missing = 0

    for api_path in sorted(API_SAFETY_DIR.glob("*.json")):
        if api_path.name == "safety.json":
            continue

        api_data = json.loads(api_path.read_text(encoding="utf-8"))
        workflows = api_data.get("emergencyWorkflows")
        if not workflows:
            print(f"  NO WORKFLOWS in API: {api_path.name}")
            continue

        kit_path = KIT_SAFETY_DIR / api_path.name
        if not kit_path.exists():
            print(f"  KIT FILE MISSING: {api_path.name}")
            missing += 1
            continue

        kit_data = json.loads(kit_path.read_text(encoding="utf-8"))
        if "emergencyWorkflows" in kit_data:
            print(f"  SKIP (already has emergencyWorkflows): {kit_path.name}")
            skipped += 1
            continue

        kit_data["emergencyWorkflows"] = workflows
        kit_path.write_text(json.dumps(kit_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        patched += 1
        print(f"  PATCHED: {kit_path.name}")

    print(f"\nDone. Patched={patched}, Skipped={skipped}, Missing={missing}")


if __name__ == "__main__":
    main()
