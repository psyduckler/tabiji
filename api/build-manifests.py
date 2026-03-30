#!/usr/bin/env python3
import hashlib
import json
import mimetypes
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
API_DIR = BASE_DIR / "api"
V1_DIR = API_DIR / "v1"
COUNTRIES_DIR = V1_DIR / "countries"
API_VERSION = "1.5.0"
SCHEMA_VERSION = "1.0"
COMPATIBILITY = {
    "manifest": "1.0",
    "country_manifest": "1.0",
    "breakingChangePolicy": "Increment schemaVersion major for breaking changes; increment datasetVersion whenever generated payloads or checksums change.",
}
TOP_LEVEL_DATASETS = [
    "index.json",
    "destinations.json",
    "picks.json",
    "itineraries.json",
    "compare.json",
    "search-index.json",
    "catalog.json",
    "countries.json",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iso_mtime(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def content_type_for(path: Path) -> str:
    guessed, _ = mimetypes.guess_type(path.name)
    return guessed or "application/json"


def build_file_meta(path: Path) -> dict:
    rel = path.relative_to(V1_DIR).as_posix()
    return {
        "path": rel,
        "contentType": content_type_for(path),
        "sizeBytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "updatedAt": iso_mtime(path),
    }


def dataset_version_for(paths: list[Path]) -> str:
    latest = max(p.stat().st_mtime for p in paths)
    dt = datetime.fromtimestamp(latest, tz=timezone.utc)
    return dt.strftime("%Y.%m.%d.%H%M%S")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_country_indexes() -> tuple[dict[str, Counter], dict[str, list[str]]]:
    counts: dict[str, Counter] = defaultdict(Counter)
    slugs: dict[str, list[str]] = defaultdict(list)

    destinations = load_json(V1_DIR / "destinations.json").get("destinations", [])
    for dest in destinations:
        iso2 = (dest.get("countryCode") or "").upper()
        if not iso2:
            continue
        counts[iso2]["destinations"] += 1
        slugs[iso2].append(dest.get("slug", ""))

    return counts, slugs


def build_global_manifest() -> dict:
    dataset_paths = [V1_DIR / name for name in TOP_LEVEL_DATASETS if (V1_DIR / name).exists()]
    country_files = sorted(COUNTRIES_DIR.glob("*.json"))
    all_paths = dataset_paths + country_files
    country_counts, _ = build_country_indexes()

    manifest = {
        "apiVersion": API_VERSION,
        "schemaVersion": SCHEMA_VERSION,
        "datasetVersion": dataset_version_for(all_paths),
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "compatibility": COMPATIBILITY,
        "datasets": {path.name: build_file_meta(path) for path in dataset_paths},
        "countries": [],
    }

    for country_file in country_files:
        iso2 = country_file.stem.upper()
        manifest["countries"].append({
            "iso2": iso2,
            "manifestPath": f"countries/{country_file.stem}/manifest.json",
            "datasetVersion": dataset_version_for([country_file]),
            "entityCounts": dict(country_counts.get(iso2, {})),
            "countryFactsPath": f"countries/{country_file.name}",
            "countryFactsSha256": sha256_file(country_file),
            "updatedAt": iso_mtime(country_file),
        })

    return manifest


def build_country_manifest(country_path: Path, country_record: dict, counts: Counter, slugs: list[str]) -> dict:
    dataset_paths = [country_path]
    manifest = {
        "apiVersion": API_VERSION,
        "schemaVersion": SCHEMA_VERSION,
        "manifestType": "country",
        "iso2": country_record.get("iso2", country_path.stem.upper()),
        "iso3": country_record.get("iso3", ""),
        "name": country_record.get("name", country_path.stem.upper()),
        "datasetVersion": dataset_version_for(dataset_paths),
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "compatibility": COMPATIBILITY,
        "files": {
            "countryFacts": build_file_meta(country_path),
        },
        "entityCounts": dict(counts),
        "relatedDestinationSlugs": sorted([slug for slug in slugs if slug])[:50],
        "staleAfter": iso_mtime(country_path),
    }
    return manifest


def main():
    if not V1_DIR.exists():
        raise SystemExit("api/v1 does not exist; generate API outputs first")

    countries_payload = load_json(V1_DIR / "countries.json")
    country_by_iso2 = {row.get("iso2", "").upper(): row for row in countries_payload.get("countries", [])}
    country_counts, country_slugs = build_country_indexes()

    global_manifest = build_global_manifest()
    (V1_DIR / "manifest.json").write_text(json.dumps(global_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for country_path in sorted(COUNTRIES_DIR.glob("*.json")):
        iso2 = country_path.stem.upper()
        out_dir = COUNTRIES_DIR / country_path.stem
        out_dir.mkdir(parents=True, exist_ok=True)
        manifest = build_country_manifest(
            country_path,
            country_by_iso2.get(iso2, {"iso2": iso2, "name": iso2}),
            country_counts.get(iso2, Counter()),
            country_slugs.get(iso2, []),
        )
        (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Wrote global manifest and {len(list(COUNTRIES_DIR.glob('*/manifest.json')))} country manifests")


if __name__ == "__main__":
    main()
