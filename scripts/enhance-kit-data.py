#!/usr/bin/env python3
"""Enhance emergency kit safety JSONs with health-data and scam data."""

import json
import os
from pathlib import Path

TABIJI = Path(os.path.expanduser("~/tabiji"))
SAFETY_DIR = TABIJI / "api/v1/safety"
HEALTH_DIR = TABIJI / "health-data"
SCAMS_DIR = TABIJI / "api/v1/scams"

# Country name -> ISO2 mapping for scam files
COUNTRY_TO_ISO = {
    "Argentina": "ar", "Australia": "au", "Brazil": "br", "Chile": "cl",
    "China": "cn", "Colombia": "co", "Costa Rica": "cr", "Czech Republic": "cz",
    "Germany": "de", "Egypt": "eg", "Spain": "es", "France": "fr",
    "United Kingdom": "gb", "Greece": "gr", "Croatia": "hr", "Hungary": "hu",
    "Indonesia": "id", "India": "in", "Italy": "it", "Japan": "jp",
    "Kenya": "ke", "South Korea": "kr", "Sri Lanka": "lk", "Morocco": "ma",
    "Mexico": "mx", "Malaysia": "my", "Norway": "no", "New Zealand": "nz",
    "Peru": "pe", "Philippines": "ph", "Poland": "pl", "Portugal": "pt",
    "Sweden": "se", "Singapore": "sg", "Thailand": "th", "Turkey": "tr",
    "Tanzania": "tz", "United States": "us", "Vietnam": "vn", "South Africa": "za",
    # Extra mappings
    "UAE": "ae", "Austria": "at", "Belgium": "be", "Canada": "ca",
    "Switzerland": "ch", "Cuba": "cu", "Ireland": "ie", "Israel": "il",
    "Iceland": "is", "Jordan": "jo", "Cambodia": "kh", "Netherlands": "nl",
    "Nepal": "np", "Denmark": "dk", "Hong Kong": "hk", "Puerto Rico": "pr",
}

def load_json(path):
    with open(path) as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

# ── Part 1: Merge health-data ──
print("=" * 60)
print("PART 1: Merging health-data into safety JSONs")
print("=" * 60)

health_merged = 0
for safety_file in sorted(SAFETY_DIR.glob("*.json")):
    iso_lower = safety_file.stem
    iso_upper = iso_lower.upper()
    health_file = HEALTH_DIR / f"{iso_upper}.json"
    
    if not health_file.exists():
        print(f"  {iso_lower}: no health-data found, skipping")
        continue
    
    safety = load_json(safety_file)
    health = load_json(health_file)
    
    # Merge medications
    safety["medications"] = {
        "commonOTC": health.get("commonOTC", []),
        "prescriptionRules": health.get("prescriptionRules", ""),
        "restrictedMeds": health.get("restrictedMeds", []),
        "bringDocumentation": health.get("bringDocumentation", ""),
    }
    
    # Merge into healthcare (don't overwrite existing keys)
    hc = safety.get("healthcare", {})
    if not isinstance(hc, dict):
        hc = {}
    
    hc["pharmacy"] = {
        "access": health.get("pharmacyAccess", ""),
        "hours": health.get("pharmacyHours", ""),
        "tips": health.get("pharmacyTips", []),
    }
    hc["vaccinations"] = health.get("vaccinations", [])
    hc["water"] = {
        "safety": health.get("waterSafety", ""),
        "notes": health.get("waterNotes", ""),
    }
    hc["foodSafetyTips"] = health.get("foodSafetyTips", [])
    hc["travelInsurance"] = health.get("travelInsurance", "")
    
    if "qualityRating" not in hc:
        hc["qualityRating"] = health.get("qualityRating", "")
    if "qualityNotes" not in hc:
        hc["qualityNotes"] = health.get("qualityNotes", "")
    
    safety["healthcare"] = hc
    save_json(safety_file, safety)
    health_merged += 1
    print(f"  ✅ {iso_lower}: merged health-data (OTC: {len(safety['medications']['commonOTC'])}, restricted: {len(safety['medications']['restrictedMeds'])})")

print(f"\nHealth-data merged into {health_merged}/40 safety files\n")

# ── Part 2: Fill scams ──
print("=" * 60)
print("PART 2: Filling scams from city-level data")
print("=" * 60)

# Build country -> city scams mapping
country_scams = {}  # iso2 -> list of (scam, city)
for scam_file in sorted(SCAMS_DIR.glob("*.json")):
    city = scam_file.stem
    data = load_json(scam_file)
    country_name = data.get("country", "")
    iso = COUNTRY_TO_ISO.get(country_name, "").lower()
    if not iso:
        print(f"  ⚠️  Unknown country '{country_name}' in {city}.json")
        continue
    
    scams = data.get("scams", data.get("common_scams", []))
    if iso not in country_scams:
        country_scams[iso] = []
    for s in scams:
        country_scams[iso].append({"scam": s, "city": city})

scams_filled = 0
for safety_file in sorted(SAFETY_DIR.glob("*.json")):
    iso = safety_file.stem
    if iso not in country_scams:
        print(f"  {iso}: no scam data found")
        continue
    
    safety = load_json(safety_file)
    
    # Deduplicate by scam name, track cities
    seen = {}
    for item in country_scams[iso]:
        s = item["scam"]
        name = s.get("name", s.get("title", "Unknown"))
        if name not in seen:
            seen[name] = {
                "name": name,
                "description": s.get("description", s.get("how_it_works", "")),
                "cities": [item["city"]],
            }
        else:
            if item["city"] not in seen[name]["cities"]:
                seen[name]["cities"].append(item["city"])
    
    # Pick top 5 (prefer those appearing in most cities, then alphabetical)
    ranked = sorted(seen.values(), key=lambda x: (-len(x["cities"]), x["name"]))
    top5 = ranked[:5]
    
    # Truncate descriptions to keep file sizes reasonable
    for scam in top5:
        desc = scam["description"]
        if len(desc) > 300:
            scam["description"] = desc[:297] + "..."
    
    safety["scams"] = top5
    save_json(safety_file, safety)
    scams_filled += 1
    scam_names = [s["name"] for s in top5]
    print(f"  ✅ {iso}: {len(top5)} scams added — {', '.join(scam_names[:3])}...")

print(f"\nScams filled for {scams_filled}/40 safety files")
print("\n✅ Done!")
