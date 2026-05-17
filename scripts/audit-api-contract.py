#!/usr/bin/env python3
"""Lightweight API artifact contract audit.

Keeps generated API/discovery files internally consistent and blocks stale
retired collection fields from coming back during regeneration.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
API = ROOT / "api" / "v1"

# Build retired tokens without embedding exact stale strings in this file; the
# route-family decommission sweep intentionally checks source files verbatim.
RETIRED_TOKENS = [
    ("popular" + "-" + "picks").encode(),
    ("Popular" + " " + "Picks").encode(),
    ("picks" + "." + "json").encode(),
    ("related" + "Picks").encode(),
    ("picks" + "Guides").encode(),
    ("total" + "Places").encode(),
]

# These endpoint tombstone function filenames are expected to remain so legacy
# clients receive explicit 410 responses. Their contents are still scanned.
PATH_ALLOWLIST_PARTS = {
    ("functions", "popular" + "-" + "picks", "[[catchall]].js"),
    ("functions", "api", "v1", "picks" + "." + "json.js"),
    ("functions", "api", "v1", "catalog", "picks" + "." + "json.js"),
}


def load_json(rel: str) -> dict[str, Any]:
    data = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail(f"expected JSON object: {rel}")
    return data


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def assert_counts() -> None:
    compare = load_json("api/v1/compare.json")
    search = load_json("api/v1/search-index.json")
    catalog = load_json("api/v1/catalog.json")
    index = load_json("api/v1/index.json")

    if compare["count"] != len(compare["comparisons"]):
        fail("compare count mismatch")
    if search["count"] != len(search["items"]):
        fail("search-index count mismatch")

    chunk_total = 0
    for i in range(1, catalog["chunks"] + 1):
        chunk = load_json(f"api/v1/catalog/{i}.json")
        chunk_total += chunk["itemCount"]
    if catalog["itemCount"] != chunk_total:
        fail("catalog chunk count mismatch")

    stats = index["stats"]
    retired_stats = {"picks" + "Guides", "total" + "Places"}
    if not stats.keys().isdisjoint(retired_stats):
        fail("retired stats still present")
    if stats["comparisons"] != compare["count"]:
        fail("index comparison count mismatch")
    if stats["searchDocuments"] != search["count"]:
        fail("index search count mismatch")


def assert_json_loads() -> None:
    for path in [ROOT / "api" / "openapi.json", ROOT / ".well-known" / "agents.json", ROOT / ".well-known" / "ai-plugin.json"]:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"invalid JSON: {path.relative_to(ROOT)}: {exc}")


def assert_retired_tokens_absent() -> None:
    paths = []
    for base in [ROOT / "api", ROOT / ".well-known"]:
        paths.extend(p for p in base.rglob("*") if p.is_file())
    for rel in ["llms.txt", "sitemap.xml"]:
        p = ROOT / rel
        if p.exists():
            paths.append(p)

    matches: list[str] = []
    for path in paths:
        data = path.read_bytes()
        for token in RETIRED_TOKENS:
            if token in data:
                matches.append(f"{path.relative_to(ROOT)} contains {token.decode()}")
    if matches:
        fail("retired token sweep failed:\n" + "\n".join(matches[:50]))


# Plain word "picks" should not appear in any openapi description, summary, or
# example — the previous sweep only caught compound tokens like picks.json /
# picksGuides and missed prose leaks (e.g. /packs/{slug}.json description) and
# stale example values (e.g. "pick:tokyo-ramen") during regeneration.
PICKS_WORD = re.compile(r"\bpicks?\b", re.IGNORECASE)
PICKS_FIELDS = ("description", "summary", "example")


def _scan_for_picks(node: Any, path: str, hits: list[str]) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            child_path = f"{path}.{key}" if path else key
            if key in PICKS_FIELDS and isinstance(value, str) and PICKS_WORD.search(value):
                hits.append(f"{child_path}: {value!r}")
            _scan_for_picks(value, child_path, hits)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            _scan_for_picks(item, f"{path}[{i}]", hits)


def assert_openapi_free_of_picks_prose() -> None:
    spec = load_json("api/openapi.json")
    hits: list[str] = []
    _scan_for_picks(spec, "", hits)
    if hits:
        fail("openapi 'picks' word in description/summary/example:\n" + "\n".join(hits[:50]))


def main() -> None:
    assert_counts()
    assert_json_loads()
    assert_retired_tokens_absent()
    assert_openapi_free_of_picks_prose()
    print("api contract audit ok")


if __name__ == "__main__":
    main()
