#!/usr/bin/env python3
"""Collect Google Trends data for travel destinations via SerpAPI."""

import json, subprocess, time, requests
from datetime import datetime

DESTINATIONS = [
    "Tokyo", "Bali", "Paris", "Barcelona", "Lisbon", "Bangkok", "Rome",
    "London", "New York", "Istanbul", "Dubai", "Singapore", "Seoul",
    "Amsterdam", "Prague", "Budapest", "Marrakech", "Cape Town", "Sydney",
    "Kyoto", "Cancun", "Dubrovnik", "Reykjavik", "Santorini", "Maldives",
    "Phuket", "Vietnam", "Mexico City", "Buenos Aires", "Cartagena",
    "Amalfi Coast", "Tulum", "Costa Rica", "Portugal", "Greece",
    "Croatia", "Colombia", "Peru", "Morocco", "Japan", "Thailand",
    "Hawaii", "Alaska", "Patagonia", "Lake Como", "Swiss Alps",
    "Zanzibar", "Sri Lanka", "Montenegro", "Madeira"
]

def get_api_key():
    return subprocess.run(
        ["security", "find-generic-password", "-s", "serpapi-key", "-w"],
        capture_output=True, text=True
    ).stdout.strip()

def fetch_batch(queries, api_key):
    """Fetch trends for up to 5 queries."""
    q = ",".join(queries)
    resp = requests.get("https://serpapi.com/search.json", params={
        "engine": "google_trends",
        "q": q,
        "data_type": "TIMESERIES",
        "date": "today 12-m",
        "cat": "67",
        "api_key": api_key
    })
    resp.raise_for_status()
    return resp.json()

def calc_velocity(values):
    """% change: last 4 weeks avg vs prior 4 weeks avg."""
    if len(values) < 8:
        return 0
    recent = sum(values[-4:]) / 4
    prior = sum(values[-8:-4]) / 4
    if prior == 0:
        return 0
    return round((recent - prior) / prior * 100, 1)

def main():
    api_key = get_api_key()
    results = []
    queries = [f"{d} travel" for d in DESTINATIONS]

    for i in range(0, len(queries), 5):
        batch = queries[i:i+5]
        batch_dests = DESTINATIONS[i:i+5]
        print(f"Fetching batch {i//5 + 1}/{(len(queries)+4)//5}: {batch_dests}")

        try:
            data = fetch_batch(batch, api_key)
            timeline = data.get("interest_over_time", {}).get("timeline_data", [])

            # Extract per-query timeseries
            for j, dest in enumerate(batch_dests):
                values = []
                dates = []
                for point in timeline:
                    dates.append(point.get("date", ""))
                    vals = point.get("values", [])
                    v = int(vals[j]["extracted_value"]) if j < len(vals) else 0
                    values.append(v)

                velocity = calc_velocity(values)
                results.append({
                    "destination": dest,
                    "query": batch[j],
                    "values": values,
                    "dates": dates,
                    "velocity": velocity,
                    "current": values[-1] if values else 0
                })
        except Exception as e:
            print(f"  Error: {e}")
            for dest in batch_dests:
                results.append({"destination": dest, "query": f"{dest} travel",
                                "values": [], "dates": [], "velocity": 0, "current": 0})

        if i + 5 < len(queries):
            time.sleep(2)

    results.sort(key=lambda x: x["velocity"], reverse=True)
    out = {"updated": datetime.now().isoformat(), "destinations": results}

    with open("tabiji/trends/trends-data.json", "w") as f:
        json.dump(out, f, indent=2)

    print(f"\nDone! {len(results)} destinations saved to trends-data.json")
    rising = [r for r in results if r["velocity"] > 0]
    falling = [r for r in results if r["velocity"] < 0]
    print(f"🔥 {len(rising)} rising | 📉 {len(falling)} falling")

if __name__ == "__main__":
    main()
