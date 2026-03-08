#!/usr/bin/env python3
"""Fetch climate/weather data for a city using Open-Meteo Historical API.

Usage:
    python3 openmeteo-climate.py <city> [--lat X --lon Y]
    python3 openmeteo-climate.py Tokyo
    python3 openmeteo-climate.py "Buenos Aires" --lat -34.6 --lon -58.4

Returns monthly averages: temp high/low (°C/°F), precipitation, sunshine hours,
and best-months-to-visit recommendation. Uses 2023-2024 data for averages.
"""
import sys, json, urllib.request, urllib.parse, argparse
from collections import defaultdict

GEOCODE_API = "https://geocoding-api.open-meteo.com/v1/search"
ARCHIVE_API = "https://archive-api.open-meteo.com/v1/archive"
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def geocode(city: str) -> tuple:
    url = f"{GEOCODE_API}?name={urllib.parse.quote(city)}&count=1"
    req = urllib.request.Request(url, headers={"User-Agent": "tabiji/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    results = data.get("results", [])
    if not results:
        raise ValueError(f"City not found: {city}")
    r = results[0]
    return r["latitude"], r["longitude"], r.get("name", city), r.get("country", "")

def fetch_climate(lat: float, lon: float) -> dict:
    """Fetch 2 years of daily data and compute monthly averages."""
    params = {
        "latitude": lat, "longitude": lon,
        "start_date": "2023-01-01", "end_date": "2024-12-31",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,sunshine_duration",
        "timezone": "auto"
    }
    url = f"{ARCHIVE_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "tabiji/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())

def c_to_f(c: float) -> float:
    return round(c * 9 / 5 + 32, 1)

def analyze(data: dict, city: str, country: str) -> dict:
    daily = data.get("daily", {})
    times = daily.get("time", [])
    highs = daily.get("temperature_2m_max", [])
    lows = daily.get("temperature_2m_min", [])
    precip = daily.get("precipitation_sum", [])
    sunshine = daily.get("sunshine_duration", [])  # seconds

    # Aggregate by month
    monthly_data = defaultdict(lambda: {"highs": [], "lows": [], "precip": [], "sunshine": []})
    for i, date_str in enumerate(times):
        month_idx = int(date_str[5:7]) - 1  # 0-indexed
        if i < len(highs) and highs[i] is not None:
            monthly_data[month_idx]["highs"].append(highs[i])
        if i < len(lows) and lows[i] is not None:
            monthly_data[month_idx]["lows"].append(lows[i])
        if i < len(precip) and precip[i] is not None:
            monthly_data[month_idx]["precip"].append(precip[i])
        if i < len(sunshine) and sunshine[i] is not None:
            monthly_data[month_idx]["sunshine"].append(sunshine[i])

    months = []
    for i in range(12):
        md = monthly_data[i]
        avg_high = round(sum(md["highs"]) / len(md["highs"]), 1) if md["highs"] else 0
        avg_low = round(sum(md["lows"]) / len(md["lows"]), 1) if md["lows"] else 0
        total_precip = round(sum(md["precip"]) / 2, 1) if md["precip"] else 0  # avg over 2 years
        rain_days = round(sum(1 for p in md["precip"] if p > 1.0) / 2, 1)  # avg rain days (>1mm)
        avg_sunshine_hrs = round(sum(md["sunshine"]) / len(md["sunshine"]) / 3600, 1) if md["sunshine"] else 0

        months.append({
            "month": MONTHS[i],
            "high_c": avg_high, "high_f": c_to_f(avg_high),
            "low_c": avg_low, "low_f": c_to_f(avg_low),
            "precip_mm": total_precip,
            "rain_days": rain_days,
            "sunshine_hrs_per_day": avg_sunshine_hrs
        })

    # Best months: comfortable temps (18-28°C high), low rain, high sunshine
    scored = []
    for i, m in enumerate(months):
        temp_score = max(0, 10 - abs(m["high_c"] - 23) * 0.5)
        rain_score = max(0, 10 - m["rain_days"] * 0.7)
        sun_score = min(10, m["sunshine_hrs_per_day"])
        scored.append((i, temp_score + rain_score + sun_score))
    scored.sort(key=lambda x: -x[1])
    best = [MONTHS[s[0]] for s in scored[:3]]

    hottest = max(range(12), key=lambda i: months[i]["high_c"])
    coldest = min(range(12), key=lambda i: months[i]["low_c"])
    wettest = max(range(12), key=lambda i: months[i]["precip_mm"])

    return {
        "city": city,
        "country": country,
        "monthly": months,
        "best_months_to_visit": best,
        "hottest_month": {"month": MONTHS[hottest], "high_c": months[hottest]["high_c"], "high_f": months[hottest]["high_f"]},
        "coldest_month": {"month": MONTHS[coldest], "low_c": months[coldest]["low_c"], "low_f": months[coldest]["low_f"]},
        "wettest_month": {"month": MONTHS[wettest], "precip_mm": months[wettest]["precip_mm"]},
        "annual_precip_mm": round(sum(m["precip_mm"] for m in months), 1),
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("city", help="City name")
    parser.add_argument("--lat", type=float)
    parser.add_argument("--lon", type=float)
    args = parser.parse_args()

    if args.lat and args.lon:
        lat, lon, name, country = args.lat, args.lon, args.city, ""
    else:
        lat, lon, name, country = geocode(args.city)

    raw = fetch_climate(lat, lon)
    result = analyze(raw, name, country)
    print(json.dumps(result, indent=2, ensure_ascii=False))
