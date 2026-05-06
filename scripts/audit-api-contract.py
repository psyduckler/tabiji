#!/usr/bin/env python3
"""Validate Tabiji generated API artifacts before deploy.

Hard failures cover trust-breaking API contract issues: count parity, stale detail
files, duplicate identifiers, `undefined` text leaks, catalog chunk/shard parity,
and fallback-photo thresholds. Empty optional fields are reported as warnings so
legacy editorial gaps stay visible without blocking count/schema fixes.
"""
from __future__ import annotations

import json
import pathlib
import sys
from collections import Counter, defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[1]
API = ROOT / "api" / "v1"
FALLBACK_PHOTO = "/assets/images/owl-logo.png"
FALLBACK_PHOTO_MAX = 500

ERRORS: list[str] = []
WARNINGS: list[str] = []


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def item_count(payload: dict) -> int:
    for key in ("destinations", "picks", "itineraries", "comparisons", "countries", "profiles", "alerts", "items"):
        if isinstance(payload.get(key), list):
            return len(payload[key])
    return len(payload.get("items", []))


def assert_count(rel: str, key: str | None = None):
    payload = load(rel)
    if key is None:
        count = item_count(payload)
    else:
        count = len(payload.get(key, []))
    advertised = payload.get("count", payload.get("itemCount", count))
    if advertised != count:
        ERRORS.append(f"{rel}: advertised count {advertised} != actual {count}")
    return payload, count


def scan_strings(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            scan_strings(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            scan_strings(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        if "undefined" in obj.lower():
            ERRORS.append(f"undefined text leak at {path}: {obj[:120]!r}")
        if obj == "":
            WARNINGS.append(f"empty string at {path}")


def assert_unique(records, rel: str, fields=("id", "slug")):
    for field in fields:
        values = [r.get(field) for r in records if isinstance(r, dict) and r.get(field)]
        dupes = [v for v, n in Counter(values).items() if n > 1]
        if dupes:
            ERRORS.append(f"{rel}: duplicate {field} values: {dupes[:10]}")


def assert_detail_dir_matches(index_rel: str, key: str, slug_key: str, dirname: str):
    payload = load(index_rel)
    listed = {str(item.get(slug_key) or item.get("iso2", "")).lower() for item in payload.get(key, []) if item.get(slug_key) or item.get("iso2")}
    detail_dir = API / dirname
    if not detail_dir.is_dir():
        return
    on_disk = {p.stem.lower() for p in detail_dir.glob("*.json")}
    missing = sorted(listed - on_disk)
    stale = sorted(on_disk - listed)
    if missing:
        ERRORS.append(f"{dirname}: {len(missing)} listed records missing detail JSON: {missing[:10]}")
    if stale:
        ERRORS.append(f"{dirname}: {len(stale)} stale detail JSON files not listed: {stale[:10]}")


def main() -> int:
    collections = [
        ("api/v1/destinations.json", "destinations"),
        ("api/v1/picks.json", "picks"),
        ("api/v1/itineraries.json", "itineraries"),
        ("api/v1/compare.json", "comparisons"),
        ("api/v1/countries.json", "countries"),
        ("api/v1/safety.json", "profiles"),
        ("api/v1/alerts.json", "alerts"),
        ("api/v1/scams.json", "items"),
    ]

    loaded = {}
    for rel, key in collections:
        path = ROOT / rel
        if path.exists():
            payload, _ = assert_count(rel, key)
            loaded[rel] = payload
            records = payload.get(key, [])
            assert_unique(records, rel)
            scan_strings(records, rel)

    picks = loaded.get("api/v1/picks.json", {})
    if picks:
        total_places = sum(int(p.get("placeCount") or 0) for p in picks.get("picks", []))
        if picks.get("totalPlaces") != total_places:
            ERRORS.append(f"api/v1/picks.json: totalPlaces {picks.get('totalPlaces')} != sum(placeCount) {total_places}")

    search = load("api/v1/search-index.json")
    catalog = load("api/v1/catalog.json")
    if search.get("count") != len(search.get("items", [])):
        ERRORS.append("api/v1/search-index.json count mismatch")

    chunk_total = 0
    for url in catalog.get("chunkUrls", []):
        rel = url.lstrip("/")
        chunk = load(rel)
        if chunk.get("itemCount") != len(chunk.get("items", [])):
            ERRORS.append(f"{rel}: itemCount {chunk.get('itemCount')} != items length {len(chunk.get('items', []))}")
        chunk_total += len(chunk.get("items", []))
    if catalog.get("itemCount") != chunk_total:
        ERRORS.append(f"api/v1/catalog.json: itemCount {catalog.get('itemCount')} != chunk total {chunk_total}")

    for shard_name, url in catalog.get("shards", {}).items():
        rel = url.lstrip("/")
        shard = load(rel)
        if shard.get("itemCount") != len(shard.get("items", [])):
            ERRORS.append(f"{rel}: itemCount {shard.get('itemCount')} != items length {len(shard.get('items', []))}")
        assert_unique(shard.get("items", []), rel, fields=("id",))

    assert_detail_dir_matches("api/v1/alerts.json", "alerts", "iso2", "alerts")
    assert_detail_dir_matches("api/v1/safety.json", "profiles", "iso2", "safety")
    assert_detail_dir_matches("api/v1/countries.json", "countries", "iso2", "countries")
    assert_detail_dir_matches("api/v1/scams.json", "items", "slug", "scams")
    assert_detail_dir_matches("api/v1/itineraries.json", "itineraries", "slug", "itineraries")

    destinations = loaded.get("api/v1/destinations.json", {}).get("destinations", [])
    fallback_count = sum(1 for d in destinations if d.get("photo") == FALLBACK_PHOTO)
    if fallback_count > FALLBACK_PHOTO_MAX:
        ERRORS.append(f"fallback photo count {fallback_count} exceeds threshold {FALLBACK_PHOTO_MAX}")

    if WARNINGS:
        grouped = defaultdict(int)
        for warning in WARNINGS:
            grouped[warning.split(" at ", 1)[0]] += 1
        print("Warnings:")
        for key, count in sorted(grouped.items())[:25]:
            print(f"  - {key}: {count}")
        if len(grouped) > 25:
            print(f"  ... {len(grouped) - 25} more warning groups")

    if ERRORS:
        print("Errors:")
        for error in ERRORS[:100]:
            print(f"  - {error}")
        if len(ERRORS) > 100:
            print(f"  ... {len(ERRORS) - 100} more errors")
        return 1

    print("✅ Tabiji API contract/data lint passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
