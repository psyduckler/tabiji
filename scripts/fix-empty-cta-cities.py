#!/usr/bin/env python3
"""Fix popular-picks CTA sections that have empty city names.
Extracts city from the directory name (e.g., aarhus-art-galleries → Aarhus)."""

import os
import re
import glob

PICKS_DIR = os.path.expanduser("~/tabiji/popular-picks")
fixed = 0
skipped = 0

# Map of known multi-word cities
CITY_OVERRIDES = {
    "abu-dhabi": "Abu Dhabi",
    "buenos-aires": "Buenos Aires",
    "cape-town": "Cape Town",
    "chiang-mai": "Chiang Mai",
    "dar-es-salaam": "Dar es Salaam",
    "hong-kong": "Hong Kong",
    "ho-chi-minh": "Ho Chi Minh City",
    "kuala-lumpur": "Kuala Lumpur",
    "las-vegas": "Las Vegas",
    "los-angeles": "Los Angeles",
    "mexico-city": "Mexico City",
    "new-orleans": "New Orleans",
    "new-york": "New York",
    "playa-del-carmen": "Playa del Carmen",
    "rio-de-janeiro": "Rio de Janeiro",
    "san-francisco": "San Francisco",
    "san-sebastian": "San Sebastián",
    "santa-fe": "Santa Fe",
    "siem-reap": "Siem Reap",
    "sri-lanka": "Sri Lanka",
    "st-petersburg": "St. Petersburg",
    "tel-aviv": "Tel Aviv",
    "la-paz": "La Paz",
    "el-nido": "El Nido",
    "porto-alegre": "Porto Alegre",
    "san-miguel-de-allende": "San Miguel de Allende",
    "mar-del-plata": "Mar del Plata",
    "punta-cana": "Punta Cana",
    "costa-rica": "Costa Rica",
}

def extract_city(dirname):
    """Extract city name from popular-picks directory name like 'tokyo-street-food' → 'Tokyo'."""
    # Try known multi-word cities first (longest match)
    for slug, name in sorted(CITY_OVERRIDES.items(), key=lambda x: -len(x[0])):
        if dirname.startswith(slug + "-"):
            return name
    # Otherwise, take the first word
    parts = dirname.split("-")
    return parts[0].title()

for page_dir in sorted(glob.glob(os.path.join(PICKS_DIR, "*/index.html"))):
    with open(page_dir, "r") as f:
        content = f.read()
    
    if 'Plan your  trip' not in content:
        continue
    
    dirname = os.path.basename(os.path.dirname(page_dir))
    city = extract_city(dirname)
    
    new_content = content.replace(
        'Plan your  trip',
        f'Plan your {city} trip'
    ).replace(
        'Get a free custom itinerary for  —',
        f'Get a free custom itinerary for {city} —'
    )
    
    if new_content != content:
        with open(page_dir, "w") as f:
            f.write(new_content)
        fixed += 1
    else:
        skipped += 1

print(f"Fixed {fixed} pages, skipped {skipped}")
