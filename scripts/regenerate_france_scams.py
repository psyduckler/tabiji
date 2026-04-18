#!/usr/bin/env python3
"""Regenerate France scam pages + APIs from authoritative batch files.

Source of truth: scams/research/batch-<city>.json
Outputs:
  - scams/<slug>/index.html                 (per-city HTML)
  - scams/country/fr/index.html             (country hub HTML)
  - api/v1/scams/<slug>.json                (per-city API)
  - api/v1/countries/fr/scams.json          (aggregate API)

Previously drifted because scams/generate_pages.py prefers enriched_master.json
which is stale; we bypass that by loading batch files directly and running only
the French subset.
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
API_COUNTRY_DIR = BASE / "api" / "v1" / "countries" / "fr"

# Make scams/ importable
sys.path.insert(0, str(SCAMS_DIR))
from generate_pages import (  # noqa: E402
    generate_page,
    generate_country_page,
    build_country_data,
    build_related_cities_map,
    CITY_SLUGS,
)

FRANCE_CITIES = [
    "Nice", "Cannes", "Paris", "Marseille", "Avignon", "Bordeaux",
    "Chamonix", "Lyon", "St Tropez", "Strasbourg", "Toulouse", "Annecy",
    "Biarritz", "Colmar", "Mont-Saint-Michel", "Montpellier",
]

SEVERITY_MAP = {"high": "high", "medium": "moderate", "low": "low"}


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return re.sub(r"-+", "-", s)


def load_all_batch_data():
    """Load every batch file and dedupe by city, keeping the record with the most scams.

    Older batch files (batch7.json, tier_d_batch1.json, etc.) contain stale Nice/Paris/
    Marseille entries that were never removed when dedicated batch-<city>.json files
    were added during the 2026-04-17 book-readiness pass. Without dedup, iteration
    order decides which wins and the stale ones clobber the rich ones.
    """
    files = sorted(
        glob.glob(str(RESEARCH_DIR / "batch*.json"))
        + glob.glob(str(RESEARCH_DIR / "tier_b_batch*.json"))
        + glob.glob(str(RESEARCH_DIR / "tier_c_batch*.json"))
        + glob.glob(str(RESEARCH_DIR / "tier_d_batch*.json"))
        + glob.glob(str(RESEARCH_DIR / "new_batch_*.json"))
    )
    by_city: dict[str, dict] = {}
    for path in files:
        with open(path) as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                continue
        if not isinstance(data, list):
            continue
        for rec in data:
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
    if "taxi" in n or "meter" in n or "uber" in n:
        return "transport"
    if "atm" in n or "card skim" in n or "skimming" in n:
        return "financial-fraud"
    if "petition" in n or "bracelet" in n or "ring" in n or "rose" in n or "distraction" in n:
        return "distraction"
    if "fake police" in n or "fake official" in n or "impersonat" in n:
        return "impersonation"
    if "overcharg" in n or "tourist trap" in n or "menu" in n or "bill" in n:
        return "tourist-trap"
    if "rental" in n or "hotel" in n or "accommodation" in n or "vacation rental" in n or "airbnb" in n:
        return "accommodation"
    if "theft" in n or "grab" in n or "snatch" in n or "robbery" in n:
        return "theft"
    if "currency" in n or "conversion" in n or "exchange" in n:
        return "financial-fraud"
    if "ticket" in n:
        return "tourist-trap"
    return "street-scam"


def batch_scam_to_api(scam: dict, city_slug: str, existing_by_name: dict) -> dict:
    """Map a batch-format scam record to the API schema, reusing existing metadata where possible."""
    name = scam.get("scam_name", "").strip()
    key = name.lower()
    existing = existing_by_name.get(key, {})

    # Build description from story; fall back to tldr if present
    story = scam.get("story", "").strip()
    tldr = scam.get("tldr", "").strip()
    description = story or tldr or ""

    # how_to_avoid list → avoidance single string
    avoid = scam.get("how_to_avoid", [])
    if isinstance(avoid, list):
        avoidance = " ".join(s.strip().rstrip(".") + "." for s in avoid if s.strip())
    else:
        avoidance = str(avoid or "").strip()

    # sources: concat reddit/news/official if present, else preserve existing
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


def emergency_contacts_from_batch(ec: dict | list | None) -> dict:
    """Normalize batch emergency_contacts into the API's flat dict shape."""
    if not ec:
        return {}
    if isinstance(ec, dict):
        # Already close to flat — normalize known keys
        out = {}
        key_map = {
            "police": "police", "ambulance": "ambulance", "fire": "fire",
            "emergency": "general", "general": "general", "medical": "ambulance",
        }
        for k, v in ec.items():
            nk = key_map.get(str(k).lower().strip(), str(k))
            out[nk] = v
        return out
    # batch sometimes uses a list of {type, number}
    if isinstance(ec, list):
        out = {}
        for item in ec:
            if not isinstance(item, dict):
                continue
            t = str(item.get("type", "")).lower()
            num = item.get("number") or item.get("value")
            if t and num:
                out[t] = num
        return out
    return {}


def exit_phrases_from_batch(phrases) -> list:
    if not phrases:
        return []
    out = []
    for p in phrases:
        if not isinstance(p, dict):
            continue
        out.append({
            "french": p.get("french") or p.get("phrase") or "",
            "english": p.get("english") or "",
            "pronunciation": p.get("pronunciation") or "",
        })
    return [p for p in out if p["french"]]


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

    # emergency contacts
    ec = emergency_contacts_from_batch(city_data.get("emergency_contacts"))
    if not ec and existing.get("emergencyContacts"):
        ec = existing["emergencyContacts"]

    # exit phrases
    phrases = (
        city_data.get("french_exit_phrases")
        or city_data.get("french_phrases")
        or []
    )
    exit_phrases = exit_phrases_from_batch(phrases) or existing.get("exitPhrases") or []

    payload = {
        "id": existing.get("id") or f"scams:{slug}",
        "slug": slug,
        "city": city,
        "country": city_data.get("country", existing.get("country", "France")),
        "countryCode": (city_data.get("country_code") or existing.get("countryCode") or "FR").upper(),
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scamCount": len(scams_api),
        "scams": scams_api,
        "emergencyContacts": ec,
        "exitPhrases": exit_phrases,
        "sourceUrl": existing.get("sourceUrl", f"https://tabiji.ai/scams/{slug}/"),
        "relatedAlerts": existing.get("relatedAlerts", "/api/v1/alerts/fr.json"),
        "relatedSafety": existing.get("relatedSafety", "/api/v1/safety/fr.json"),
    }
    return payload


def build_aggregate_country_api(french_city_data: list, per_city_payloads: dict) -> dict:
    """Build api/v1/countries/fr/scams.json by summing per-city payloads."""
    cities = []
    all_scams = []
    for cd in french_city_data:
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
        "id": "country-scams:fr",
        "iso2": "FR",
        "country": "France",
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scamCount": len(all_scams),
        "cities": cities,
        "scams": all_scams,
    }


def preserve_dropped_scams(french_cities: list):
    """Save API-only scams (present in per-city API but not batch) to a research file.

    Reads API state from git HEAD so the result is stable across re-runs — reading
    the working-tree API would capture whatever the last run clobbered.
    """
    import subprocess
    out = RESEARCH_DIR / "_france_api_extras_to_curate.json"
    if out.exists():
        print(f"  Skip preserve: {out.name} already exists")
        return
    extras = []
    for city in french_cities:
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
    print(f"Loaded {len(all_cities)} city records from batch files")

    french_cities = []
    for cd in all_cities:
        if cd.get("city") in FRANCE_CITIES and cd.get("city") in CITY_SLUGS:
            french_cities.append(cd)

    found_names = {c["city"] for c in french_cities}
    missing = [c for c in FRANCE_CITIES if c not in found_names]
    if missing:
        print(f"WARNING: missing batch data for: {missing}")
    print(f"Found {len(french_cities)} French cities in batch data")

    # Preserve any scams we're dropping before overwriting per-city API
    preserve_dropped_scams(french_cities)

    # Build related-cities map from the full dataset so cross-links stay accurate
    related_map = build_related_cities_map(all_cities)

    # 1) Regenerate per-city HTML
    for cd in french_cities:
        slug = CITY_SLUGS[cd["city"]]
        html = generate_page(cd, related_map)
        out = SCAMS_DIR / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w") as f:
            f.write(html)
        print(f"  HTML   {cd['city']:<20} → scams/{slug}/ ({len(cd.get('scams',[]))} scams)")

    # 2) Regenerate per-city API JSON
    per_city_payloads = {}
    for cd in french_cities:
        payload = rebuild_per_city_api(cd)
        slug = CITY_SLUGS[cd["city"]]
        per_city_payloads[slug] = payload
        out = API_SCAMS_DIR / f"{slug}.json"
        with open(out, "w") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        print(f"  API    {cd['city']:<20} → api/v1/scams/{slug}.json ({payload['scamCount']} scams)")

    # 3) Country hub HTML (use all_cities so build_country_data gets full context;
    #    generate_country_page handles France entry)
    country_data = build_country_data(all_cities)
    fr_cd = country_data.get("France")
    if not fr_cd:
        raise RuntimeError("France not found in country_data")
    total_built = sum(len(cd.get("scams", [])) for cd in all_cities if cd.get("city") in CITY_SLUGS)
    hub_html = generate_country_page("France", "FR", fr_cd["flag"], fr_cd["cities"], total_built)
    hub_out = SCAMS_DIR / "country" / "fr" / "index.html"
    hub_out.parent.mkdir(parents=True, exist_ok=True)
    with open(hub_out, "w") as f:
        f.write(hub_html)
    print(f"  HUB    France → scams/country/fr/index.html ({len(fr_cd['cities'])} cities)")

    # 4) Aggregate API JSON
    aggregate = build_aggregate_country_api(french_cities, per_city_payloads)
    API_COUNTRY_DIR.mkdir(parents=True, exist_ok=True)
    with open(API_COUNTRY_DIR / "scams.json", "w") as f:
        json.dump(aggregate, f, indent=2, ensure_ascii=False)
    print(f"  AGG    api/v1/countries/fr/scams.json ({aggregate['scamCount']} scams across {len(aggregate['cities'])} cities)")

    print("\nDone.")


if __name__ == "__main__":
    main()
