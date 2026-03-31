#!/usr/bin/env python3
"""
Task 2a: Generate per-pack manifest files at api/v1/packs/{slug}/manifest.json.
Idempotent — overwrites existing manifests.
"""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
PACKS_DIR = ROOT / "api" / "v1" / "packs"

SECTION_ORDER = ["countries", "safety", "destinations", "picks", "itineraries", "scams", "alerts"]


def sha256_of(data: object) -> str:
    raw = json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def size_of(data: object) -> int:
    return len(json.dumps(data, ensure_ascii=False).encode("utf-8"))


def process_pack(pack_path: Path) -> dict:
    slug = pack_path.stem
    data = json.loads(pack_path.read_text(encoding="utf-8"))

    pack_id = data.get("id", f"pack:{slug}")
    version = data.get("version", 1)
    generated_at = data.get("generatedAt", "2026-03-31T00:00:00Z")
    pack_data = data.get("data", {})

    sections = {}
    for key in SECTION_ORDER:
        if key not in pack_data:
            continue
        section_data = pack_data[key]
        item_count = len(section_data) if isinstance(section_data, list) else 1
        sections[key] = {
            "hash": sha256_of(section_data),
            "itemCount": item_count,
            "sizeBytes": size_of(section_data),
            "lastUpdated": generated_at,
        }

    # Also capture any extra sections not in SECTION_ORDER
    for key in pack_data:
        if key not in sections:
            section_data = pack_data[key]
            item_count = len(section_data) if isinstance(section_data, list) else 1
            sections[key] = {
                "hash": sha256_of(section_data),
                "itemCount": item_count,
                "sizeBytes": size_of(section_data),
                "lastUpdated": generated_at,
            }

    total_size = sum(s["sizeBytes"] for s in sections.values())
    checksum = sha256_of(pack_data)

    manifest = {
        "packId": pack_id,
        "slug": slug,
        "version": version,
        "generatedAt": generated_at,
        "totalSizeBytes": total_size,
        "checksum": checksum,
        "sections": sections,
    }

    # Write manifest to api/v1/packs/{slug}/manifest.json
    manifest_dir = PACKS_DIR / slug
    manifest_dir.mkdir(exist_ok=True)
    manifest_path = manifest_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    section_names = list(sections.keys())
    print(f"  {slug}/manifest.json  sections={section_names}  totalSizeBytes={total_size}")
    return manifest


def main():
    pack_files = sorted(PACKS_DIR.glob("*.json"))

    count = 0
    for pack_path in pack_files:
        process_pack(pack_path)
        count += 1

    print(f"\nDone. Generated manifests for {count} packs.")


if __name__ == "__main__":
    main()
