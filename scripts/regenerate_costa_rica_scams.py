#!/usr/bin/env python3
"""Regenerate Costa Rica scam pages + APIs from authoritative batch files.

Source of truth: scams/research/cr_batch*.json (dict-wrapped format with "cities" key)
Outputs:
  - scams/<slug>/index.html                 (per-city HTML — 8 cities)
  - scams/country/cr/index.html             (country hub HTML)
  - api/v1/scams/<slug>.json                (per-city API — 8 files)
  - api/v1/countries/cr/scams.json          (aggregate API)

Mirrors scripts/regenerate_france_scams.py. Bypasses scams/generate_pages.py
main() which expects older list-format batch files and won't load the new
dict-wrapped cr_batch*.json schema.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SCAMS_DIR = BASE / "scams"
RESEARCH_DIR = SCAMS_DIR / "research"
API_SCAMS_DIR = BASE / "api" / "v1" / "scams"
API_COUNTRY_DIR = BASE / "api" / "v1" / "countries" / "cr"

sys.path.insert(0, str(SCAMS_DIR))
from generate_pages import (  # noqa: E402
    generate_page,
    generate_country_page,
    build_country_data,
    build_related_cities_map,
    CITY_SLUGS,
)

COSTA_RICA_CITIES = [
    "San Jose", "Tamarindo", "Manuel Antonio", "La Fortuna",
    "Puerto Viejo", "Liberia", "Jacó", "Monteverde",
]

SEVERITY_MAP = {"high": "high", "medium": "moderate", "low": "low"}


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return re.sub(r"-+", "-", s)


def load_all_batch_data():
    """Load batch files — supports both new dict-wrapped format (cr_batch*) and old list format.

    The Costa Rica batches (cr_batch1-4.json) use the newer schema:
      {"batch": ..., "scope": ..., "cities": [ {city, country, country_code, flag, scams}, ... ]}

    The France regen pipeline used older flat-list batch files. We also pick up any
    list-format files for cross-links (related cities map).
    """
    all_files = sorted(
        glob.glob(str(RESEARCH_DIR / "batch*.json"))
        + glob.glob(str(RESEARCH_DIR / "tier_b_batch*.json"))
        + glob.glob(str(RESEARCH_DIR / "tier_c_batch*.json"))
        + glob.glob(str(RESEARCH_DIR / "tier_d_batch*.json"))
        + glob.glob(str(RESEARCH_DIR / "new_batch_*.json"))
        + glob.glob(str(RESEARCH_DIR / "cr_batch*.json"))
        + glob.glob(str(RESEARCH_DIR / "ar_batch*.json"))
        + glob.glob(str(RESEARCH_DIR / "mx_batch*.json"))
        + glob.glob(str(RESEARCH_DIR / "uk_batch*.json"))
    )
    by_city: dict[str, dict] = {}
    for path in all_files:
        with open(path) as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                continue
        # Normalize to a list of city records
        if isinstance(data, dict) and "cities" in data:
            records = data["cities"]
        elif isinstance(data, list):
            records = data
        else:
            continue
        for rec in records:
            if not isinstance(rec, dict):
                continue
            city = rec.get("city")
            if not city:
                continue
            n_new = len(rec.get("scams", []))
            existing = by_city.get(city)
            if existing is None or len(existing.get("scams", [])) < n_new:
                by_city[city] = rec
    return list(by_city.values())


def derive_category(scam_name: str, existing: str | None = None) -> str:
    if existing:
        return existing
    n = scam_name.lower()
    if "pickpocket" in n:
        return "pickpocket"
    if "taxi" in n or "meter" in n or "uber" in n or "shuttle" in n or "transfer" in n:
        return "transport"
    if "atm" in n or "card skim" in n or "skimming" in n or "currency" in n or "exchange" in n or "cambista" in n:
        return "financial-fraud"
    if "petition" in n or "bracelet" in n or "distraction" in n or "monkey" in n or "capuchin" in n:
        return "distraction"
    if "fake police" in n or "fake official" in n or "impersonat" in n or "fake 'park" in n or "ranger" in n or "watchmen" in n or "watchman" in n or "guachim" in n:
        return "impersonation"
    if "overcharg" in n or "tourist trap" in n or "menu" in n or "bill" in n or "gringo" in n or "commission" in n:
        return "tourist-trap"
    if "rental" in n or "hotel" in n or "accommodation" in n or "vacation rental" in n or "airbnb" in n or "vrbo" in n or "home-invasion" in n or "home invasion" in n:
        return "accommodation"
    if "theft" in n or "grab" in n or "snatch" in n or "robbery" in n or "break-in" in n or "key-fob" in n or "jammer" in n or "relay" in n or "pinchonazo" in n or "machete" in n:
        return "theft"
    if "insurance" in n or "mandatory" in n or "deposit" in n or "damage" in n:
        return "financial-fraud"
    if "drug" in n or "dealer" in n or "spiking" in n or "drink" in n:
        return "drug-crime"
    if "ticket" in n or "park" in n or "reserve" in n or "guide" in n or "tour" in n:
        return "tourist-trap"
    if "copycat" in n or "domain" in n or "advance-fee" in n or "deposit" in n:
        return "online-fraud"
    if "sim" in n:
        return "financial-fraud"
    return "street-scam"


def batch_scam_to_api(scam: dict, city_slug: str, existing_by_name: dict) -> dict:
    """Map a batch-format scam record to the API schema, reusing existing metadata where possible."""
    name = scam.get("scam_name", "").strip()
    key = name.lower()
    existing = existing_by_name.get(key, {})

    story = scam.get("story", "").strip()
    tldr = scam.get("tldr", "").strip()
    description = story or tldr or ""

    avoid = scam.get("how_to_avoid", [])
    if isinstance(avoid, list):
        avoidance = " ".join(s.strip().rstrip(".") + "." for s in avoid if s.strip())
    else:
        avoidance = str(avoid or "").strip()

    sources = []
    for key_name in ("reddit_sources", "news_sources", "official_sources"):
        v = scam.get(key_name)
        if isinstance(v, list):
            sources.extend([str(x) for x in v if x])
    if not sources:
        sources = existing.get("sources") or [f"tabiji:scams/{city_slug}"]

    scam_id = existing.get("id") or f"scam:{city_slug}:{slugify(name)}"
    severity = SEVERITY_MAP.get((scam.get("danger_level") or "").lower(), "moderate")

    return {
        "id": scam_id,
        "name": name,
        "category": derive_category(name, existing.get("category")),
        "severity": severity,
        "frequency": existing.get("frequency", "common"),
        "description": description,
        "avoidance": avoidance,
        "location": scam.get("location", "") or existing.get("location", ""),
        "tags": existing.get("tags") or [derive_category(name)],
        "sources": sources,
    }


def emergency_contacts_default_cr() -> dict:
    """Default Costa Rica emergency contacts (used in API payloads).

    These are the canonical CR emergency numbers per U.S. Embassy San José
    and OIJ. ICT and Tourist Police included for completeness.
    """
    return {
        "general": "911",
        "police": "911",
        "ambulance": "911",
        "fire": "911",
        "oij_tip_line": "800-8000-645",
        "tourist_police": "2258-1008",
        "ict_tourist_info": "2286-1473",
        "us_embassy": "+506 2519-2000",
        "us_embassy_after_hours": "+506 2220-3127",
    }


def rebuild_per_city_api(city_data: dict) -> dict:
    """Construct the per-city API JSON from batch data, reusing existing metadata where possible."""
    city = city_data["city"]
    slug = CITY_SLUGS[city]
    api_path = API_SCAMS_DIR / f"{slug}.json"

    existing = {}
    existing_by_name = {}
    if api_path.exists():
        with open(api_path) as f:
            existing = json.load(f)
        for s in existing.get("scams", []):
            nm = (s.get("name") or "").lower()
            if nm:
                existing_by_name[nm] = s

    scams_api = [
        batch_scam_to_api(s, slug, existing_by_name)
        for s in city_data.get("scams", [])
    ]

    # Emergency contacts — batch files don't carry these for CR, default to country-wide values.
    ec = existing.get("emergencyContacts") or emergency_contacts_default_cr()

    payload = {
        "id": existing.get("id") or f"scams:{slug}",
        "slug": slug,
        "city": city,
        "country": city_data.get("country", existing.get("country", "Costa Rica")),
        "countryCode": (city_data.get("country_code") or existing.get("countryCode") or "CR").upper(),
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scamCount": len(scams_api),
        "scams": scams_api,
        "emergencyContacts": ec,
        "exitPhrases": existing.get("exitPhrases") or [],
        "sourceUrl": existing.get("sourceUrl", f"https://tabiji.ai/scams/{slug}/"),
        "relatedAlerts": existing.get("relatedAlerts", "/api/v1/alerts/cr.json"),
        "relatedSafety": existing.get("relatedSafety", "/api/v1/safety/cr.json"),
    }
    return payload


def build_aggregate_country_api(cr_city_data: list, per_city_payloads: dict) -> dict:
    """Build api/v1/countries/cr/scams.json by summing per-city payloads."""
    cities = []
    all_scams = []
    for cd in cr_city_data:
        slug = CITY_SLUGS[cd["city"]]
        api_pl = per_city_payloads[slug]
        cities.append({
            "slug": slug,
            "city": cd["city"],
            "scamCount": api_pl["scamCount"],
            "url": f"https://tabiji.ai/api/v1/scams/{slug}.json",
        })
        all_scams.extend(api_pl["scams"])
    return {
        "id": "country-scams:cr",
        "iso2": "CR",
        "country": "Costa Rica",
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scamCount": len(all_scams),
        "cities": cities,
        "scams": all_scams,
    }


def preserve_dropped_scams(cr_cities: list):
    """Save API-only scams (present in per-city API but not batch) to a research file.

    Reads API state from git HEAD so the result is stable across re-runs — reading
    the working-tree API would capture whatever the last run clobbered.
    """
    import subprocess
    out = RESEARCH_DIR / "_costa_rica_api_extras_to_curate.json"
    if out.exists():
        print(f"  Skip preserve: {out.name} already exists")
        return
    extras = []
    for city in cr_cities:
        slug = CITY_SLUGS[city["city"]]
        try:
            res = subprocess.run(
                ["git", "show", f"HEAD:api/v1/scams/{slug}.json"],
                capture_output=True, text=True, cwd=str(BASE), check=True,
            )
            api = json.loads(res.stdout)
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            continue
        batch_names = {s.get("scam_name", "").lower() for s in city.get("scams", [])}
        for s in api.get("scams", []):
            if (s.get("name") or "").lower() not in batch_names:
                extras.append({**s, "_city": city["city"], "_slug": slug})
    if extras:
        with open(out, "w") as f:
            json.dump(extras, f, indent=2, ensure_ascii=False)
        print(f"  Preserved {len(extras)} API-only scams → {out}")


def main():
    all_cities = load_all_batch_data()
    print(f"Loaded {len(all_cities)} city records from batch files (all countries — needed for cross-links)")

    cr_cities = []
    for cd in all_cities:
        if cd.get("city") in COSTA_RICA_CITIES and cd.get("city") in CITY_SLUGS:
            cr_cities.append(cd)

    found_names = {c["city"] for c in cr_cities}
    missing = [c for c in COSTA_RICA_CITIES if c not in found_names]
    if missing:
        print(f"WARNING: missing batch data for: {missing}")
    print(f"Found {len(cr_cities)} Costa Rica cities in batch data")

    # Preserve any scams we're dropping before overwriting per-city API
    preserve_dropped_scams(cr_cities)

    # Build related-cities map from the full dataset so cross-links stay accurate
    related_map = build_related_cities_map(all_cities)

    # 1) Regenerate per-city HTML
    for cd in cr_cities:
        slug = CITY_SLUGS[cd["city"]]
        html = generate_page(cd, related_map)
        out = SCAMS_DIR / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w") as f:
            f.write(html)
        print(f"  HTML   {cd['city']:<20} → scams/{slug}/ ({len(cd.get('scams',[]))} scams, {len(html)} chars)")

    # 2) Regenerate per-city API JSON
    per_city_payloads = {}
    for cd in cr_cities:
        payload = rebuild_per_city_api(cd)
        slug = CITY_SLUGS[cd["city"]]
        per_city_payloads[slug] = payload
        out = API_SCAMS_DIR / f"{slug}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        print(f"  API    {cd['city']:<20} → api/v1/scams/{slug}.json ({payload['scamCount']} scams)")

    # 3) Country hub HTML
    country_data = build_country_data(all_cities)
    cr_cd = country_data.get("Costa Rica")
    if not cr_cd:
        raise RuntimeError("Costa Rica not found in country_data — check CITY_COUNTRY map")
    total_built = sum(len(cd.get("scams", [])) for cd in all_cities if cd.get("city") in CITY_SLUGS)
    hub_html = generate_country_page("Costa Rica", "CR", cr_cd["flag"], cr_cd["cities"], total_built)
    hub_out = SCAMS_DIR / "country" / "cr" / "index.html"
    hub_out.parent.mkdir(parents=True, exist_ok=True)
    with open(hub_out, "w") as f:
        f.write(hub_html)
    print(f"  HUB    Costa Rica → scams/country/cr/index.html ({len(cr_cd['cities'])} cities)")

    # 4) Aggregate API JSON
    aggregate = build_aggregate_country_api(cr_cities, per_city_payloads)
    API_COUNTRY_DIR.mkdir(parents=True, exist_ok=True)
    with open(API_COUNTRY_DIR / "scams.json", "w") as f:
        json.dump(aggregate, f, indent=2, ensure_ascii=False)
    print(f"  AGG    api/v1/countries/cr/scams.json ({aggregate['scamCount']} scams across {len(aggregate['cities'])} cities)")

    print("\nDone.")


if __name__ == "__main__":
    main()
