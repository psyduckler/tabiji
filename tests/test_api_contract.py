import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
API = ROOT / "api" / "v1"


def load_json(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def test_public_counts_are_self_consistent():
    picks = load_json("api/v1/picks.json")
    compare = load_json("api/v1/compare.json")
    search = load_json("api/v1/search-index.json")
    catalog = load_json("api/v1/catalog.json")
    index = load_json("api/v1/index.json")
    openapi = load_json("api/openapi.json")
    agents = load_json(".well-known/agents.json")

    assert picks["count"] == len(picks["picks"])
    assert picks["totalPlaces"] == sum(p.get("placeCount", 0) for p in picks["picks"])
    assert compare["count"] == len(compare["comparisons"])
    assert search["count"] == len(search["items"])
    assert catalog["itemCount"] == sum(load_json(f"api/v1/catalog/{i}.json")["itemCount"] for i in range(1, catalog["chunks"] + 1))

    stats = index["stats"]
    assert stats["picksGuides"] == picks["count"]
    assert stats["totalPlaces"] == picks["totalPlaces"]
    assert stats["comparisons"] == compare["count"]
    assert stats["searchDocuments"] == search["count"]
    assert f'{picks["count"]} curated picks guides' in openapi["info"]["description"]
    assert f'across {picks["count"]} guides' in agents["skills"][0]["description"]


def test_catalog_schema_matches_catalog_index_and_chunks():
    spec = load_json("api/openapi.json")
    schemas = spec["components"]["schemas"]
    catalog_ref = spec["paths"]["/catalog.json"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
    assert catalog_ref == {"$ref": "#/components/schemas/CatalogIndex"}
    assert "chunkUrls" in schemas["CatalogIndex"]["required"]
    assert "items" not in schemas["CatalogIndex"]["required"]
    assert "CatalogChunk" in schemas
    assert "/catalog/{chunk}.json" in spec["paths"]
    assert "/catalog/{shard}.json" in spec["paths"]


def test_api_data_linter_passes_current_artifacts():
    import subprocess

    result = subprocess.run(
        ["python3", "scripts/audit-api-contract.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
