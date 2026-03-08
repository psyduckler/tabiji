#!/usr/bin/env python3
"""Fetch travel-relevant country info from REST Countries API (v3.1).

Usage:
    python3 restcountries.py <country_name> [country_name_2]
    python3 restcountries.py Japan
    python3 restcountries.py "South Korea" Thailand

Outputs JSON with: name, capital, region, languages, currencies, population,
area, timezones, borders, flag emoji, driving side, calling code.
"""
import sys, json, urllib.request, urllib.error

API = "https://restcountries.com/v3.1/name"

def fetch_country(name: str) -> dict:
    url = f"{API}/{urllib.request.quote(name)}?fields=name,capital,region,subregion,languages,currencies,population,area,timezones,borders,flag,car,idd,maps,continents"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "tabiji/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())[0]
    except (urllib.error.HTTPError, IndexError) as e:
        return {"error": f"Country not found: {name}", "detail": str(e)}

    currencies = {}
    for code, info in (data.get("currencies") or {}).items():
        currencies[code] = {"name": info.get("name", ""), "symbol": info.get("symbol", "")}

    return {
        "name": data["name"].get("common", name),
        "official_name": data["name"].get("official", ""),
        "capital": data.get("capital", []),
        "region": data.get("region", ""),
        "subregion": data.get("subregion", ""),
        "continents": data.get("continents", []),
        "languages": data.get("languages", {}),
        "currencies": currencies,
        "population": data.get("population", 0),
        "area_km2": data.get("area", 0),
        "timezones": data.get("timezones", []),
        "borders": data.get("borders", []),
        "flag_emoji": data.get("flag", ""),
        "driving_side": data.get("car", {}).get("side", ""),
        "calling_code": (data.get("idd", {}).get("root", "") +
                         (data.get("idd", {}).get("suffixes", [""])[0] if data.get("idd", {}).get("suffixes") else "")),
        "google_maps": data.get("maps", {}).get("googleMaps", ""),
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 restcountries.py <country> [country2]")
        sys.exit(1)
    results = [fetch_country(c) for c in sys.argv[1:]]
    print(json.dumps(results if len(results) > 1 else results[0], indent=2, ensure_ascii=False))
