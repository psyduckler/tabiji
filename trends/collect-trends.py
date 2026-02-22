#!/usr/bin/env python3
"""Collect Google Trends data for travel destinations via SerpAPI."""

import json, subprocess, time, requests
from datetime import datetime

DESTINATIONS = [
    # Original 50
    "Tokyo", "Bali", "Paris", "Barcelona", "Lisbon", "Bangkok", "Rome",
    "London", "New York", "Istanbul", "Dubai", "Singapore", "Seoul",
    "Amsterdam", "Prague", "Budapest", "Marrakech", "Cape Town", "Sydney",
    "Kyoto", "Cancun", "Dubrovnik", "Reykjavik", "Santorini", "Maldives",
    "Phuket", "Vietnam", "Mexico City", "Buenos Aires", "Cartagena",
    "Amalfi Coast", "Tulum", "Costa Rica", "Portugal", "Greece",
    "Croatia", "Colombia", "Peru", "Morocco", "Japan", "Thailand",
    "Hawaii", "Alaska", "Patagonia", "Lake Como", "Swiss Alps",
    "Zanzibar", "Sri Lanka", "Montenegro", "Madeira",
    # Europe (30 new)
    "Hallstatt", "Tromsø", "Helsinki", "Dolomites", "Valletta", "Bruges",
    "Transylvania", "Lake Bled", "Tuscany", "Provence", "Cinque Terre",
    "Scotland", "Azores", "Slovenia", "Lofoten", "Norway Fjords", "Faroe Islands",
    "Isle of Skye", "Albania", "Lake Ohrid", "Copenhagen", "Belgrade", "Sintra",
    "San Sebastian", "Romania", "Ireland", "Norway", "Vienna", "Bergen", "Tirana",
    # Asia (25 new)
    "Jaipur", "Tbilisi", "Cappadocia", "Luang Prabang", "Palawan", "Hokkaido",
    "Bhutan", "Mongolia", "Uzbekistan", "Philippines", "Nepal", "Kerala",
    "Rajasthan", "Siem Reap", "Hanoi", "Ha Long Bay", "Udaipur", "Myanmar",
    "Azerbaijan", "Hoi An", "Georgia", "Japan Alps", "Kyrgyzstan", "Borneo", "Laos",
    # North America (20 new)
    "Oaxaca", "Cuba", "New Orleans", "Vancouver", "San Miguel de Allende", "Havana",
    "Banff National Park", "Puerto Rico", "Quebec City", "Toronto",
    "Yellowstone", "Belize", "Guatemala", "San Juan", "Barbados",
    "Antigua", "Martinique", "Napa Valley", "Maui", "Montreal",
    # South America (12 new)
    "Bogotá", "Mendoza", "Easter Island", "Salar de Uyuni", "Medellín", "Atacama",
    "Galápagos", "Rio de Janeiro", "Cusco", "Machu Picchu", "Santiago", "Ushuaia",
    # Africa (10 new)
    "Seychelles", "Kenya", "Rwanda", "Namibia", "Cairo", "Egypt",
    "Serengeti", "Nairobi", "Chefchaouen", "Fez",
    # Oceania (7 new)
    "Queenstown", "New Zealand", "Melbourne", "Bora Bora", "Fiji", "Tasmania", "Wellington",
    # Middle East (4 new)
    "Wadi Rum", "Petra", "Oman", "Tel Aviv",
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
