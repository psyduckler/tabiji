from __future__ import annotations

import csv
import io
import json
import math
import re
import subprocess
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'find' / 'destinations.json'
FALLBACK_PHOTO = 'https://img.tabiji.ai/owl-logo.png'
TARGET_ADD = 1000

WORLD_CITIES_URL = 'https://gist.githubusercontent.com/curran/13d30e855d48cdd6f22acdf0afe27286/raw/0635f14817ec634833bb904a47594cc2f5f9dbf8/worldcities_clean.csv'
COUNTRY_CONTINENTS_URL = 'https://gist.githubusercontent.com/stevewithington/20a69c0b6d2ff846ea5d35e5fc47f26c/raw/country-and-continent-codes-list-csv.csv'

COUNTRY_OVERRIDES = {
    'Czechia': 'Czech Republic',
    'Republic of the Congo': 'Congo',
    'Democratic Republic of the Congo': 'Democratic Republic of the Congo',
    'Bosnia and Herzegovina': 'Bosnia and Herzegovina',
    'North Macedonia': 'North Macedonia',
    'Myanmar': 'Myanmar',
    'Eswatini': 'Eswatini',
    'United States': 'United States',
    'United Kingdom': 'United Kingdom',
    'Russia': 'Russia',
    'South Korea': 'South Korea',
    'North Korea': 'North Korea',
    'Laos': 'Laos',
    'Moldova': 'Moldova',
    'Syria': 'Syria',
    'Venezuela': 'Venezuela',
    'Bolivia': 'Bolivia',
    'Vietnam': 'Vietnam',
    'Taiwan': 'Taiwan',
    'Tanzania': 'Tanzania',
    'Cape Verde': 'Cape Verde',
    'Palestine': 'Palestine',
    'Macau': 'Macau',
    'Hong Kong': 'Hong Kong',
}

NAME_RENAMES = {
    'Ad Damman': 'Dammam',
    'Ad Diwaniyah': 'Diwaniyah',
    'Al Amarah': 'Amarah',
    'Al Ayn': 'Al Ain',
    'Al Hillah': 'Hillah',
    'Al Hudaydah': 'Hodeidah',
    'Al Hufuf': 'Hofuf',
    'An Najaf': 'Najaf',
    'An Nasiriyah': 'Nasiriyah',
    'As Sulaymaniyah': 'Sulaymaniyah',
    'At Taif': 'Taif',
    'Az Zarqa': 'Zarqa',
    'Bandjarmasin': 'Banjarmasin',
    'Antwerpen': 'Antwerp',
    'Archangel': 'Arkhangelsk',
    'Allahabad': 'Prayagraj',
    'Baguio City': 'Baguio',
    'Ho Chi Minh City': 'Ho Chi Minh',
    'Kuwait': 'Kuwait City',
    'Bandar-e-Abbas': 'Bandar Abbas',
    'Al-Qatif': 'Qatif',
    # Fix romanization issues from review
    'Mudangiang': 'Mudanjiang',
    'Dehra Dun': 'Dehradun',
}

MANUAL_CONTINENTS = {
    'Taiwan': 'Asia',
    'Hong Kong': 'Asia',
    'Macau': 'Asia',
    'Palestine': 'Asia',
    'Kosovo': 'Europe',
    'Curaçao': 'North America',
}

EXCLUDED_NAMES = {
    'The Hague',
    'Quezon City',
    'Giza',
    'Luxor',
    'Jerusalem', 'Tel Aviv', 'Haifa', 'Beirut', 'Baku', 'Yerevan', 'Tbilisi',
    'Kuala Lumpur', 'Taipei', 'Guadalajara', 'Lima', 'Madrid', 'Vienna', 'Athens',
    'London', 'Istanbul', 'Cairo', 'Milan', 'Naples', 'Porto', 'Valencia', 'Seville',
    'Hanoi', 'Jakarta', 'Yogyakarta', 'Taiwan', 'South Korea', 'Japan', 'Indonesia',
    'Cambodia', 'Siem Reap', 'Havana', 'Cusco', 'Santiago', 'Rio de Janeiro',
    'New York City', 'Miami', 'Amsterdam', 'Brussels', 'Antwerp', 'Ghent', 'Zurich',
    'Geneva', 'Salzburg', 'Innsbruck', 'Bratislava', 'Tirana', 'Bucharest', 'Warsaw',
    'Vilnius', 'Stockholm', 'Oslo', 'Alexandria', 'Johannesburg', 'Goa', 'Mumbai',
    'Delhi', 'Manila', 'Cebu', 'Fukuoka', 'Kobe', 'Shenzhen', 'Suzhou', 'Hangzhou',
    'Tainan', 'Kaohsiung', 'Marrakesh', 'Abu Dhabi', 'Doha', 'Austin', 'Berlin',
    'Copenhagen', 'Dublin', 'Munich', 'Nashville', 'Panama City', 'Pasay City',
    # Duplicates with existing entries (different romanization)
    'Bangalore',  # Bengaluru already exists
}

BAD_TOKENS = ('Province', 'District', 'County', 'Prefecture')
EXCLUDED_REGIONS = {
    'Afghanistan', 'Iraq', 'Yemen', 'Sudan',
    # Added from review — active conflict / unsafe for tourists
    'Somalia', 'Central African Republic', 'Haiti',
    'North Korea', 'Syria', 'Libya',
}

# ---------------------------------------------------------------------------
# Vibes & travel assignment — geography-aware
# ---------------------------------------------------------------------------

# Known coastal / beach cities (manually curated for top candidates)
BEACH_CITIES = {
    'Acapulco', 'Gold Coast', 'Honolulu', 'Mombasa', 'Durban', 'Cape Town',
    'Santos', 'Recife', 'Salvador', 'Fortaleza', 'Barranquilla', 'Busan',
    'Xiamen', 'Qingdao', 'Chittagong', 'Muscat', 'Batam', 'Palembang',
    'Makassar', 'Semarang', 'Surabaya', 'Denpasar', 'Malaga', 'Split',
    'Genoa', 'Marseille', 'Nice', 'Tel Aviv', 'Tunis', 'Casablanca',
    'Mazatlan', 'Veracruz', 'Cartagena', 'Santa Marta', 'Natal',
    'Maceio', 'Vitoria', 'Florianopolis', 'Colombo', 'Galle', 'Aden',
    'Jeddah', 'Aqaba', 'Vladivostok', 'Odessa', 'Constanta', 'Varna',
    'Thessaloniki', 'Haiphong', 'Da Nang', 'Nha Trang', 'Hai Phong',
    'Port Elizabeth', 'Dakar', 'Abidjan', 'Lagos', 'Accra', 'Luanda',
    'Maputo', 'Dar es Salaam', 'Mombasa', 'Djibouti', 'Oran',
    'San Juan', 'Havana', 'Montego Bay', 'Nassau',
    'Antalya', 'Izmir', 'Bodrum', 'Trabzon',
    'Dalian', 'Fuzhou', 'Wenzhou', 'Zhuhai', 'Shantou', 'Haikou',
    'Taizhou', 'Nantong', 'Yantai',
    'Chennai', 'Kochi', 'Visakhapatnam', 'Mangalore',
    'Perth', 'Brisbane', 'Sydney', 'Auckland',
    'Tangier', 'Rabat', 'Agadir',
}

# Known historical / cultural heritage cities
HISTORICAL_CITIES = {
    'Fez', 'Lucknow', 'Varanasi', 'Jaipur', 'Agra', 'Lahore', 'Multan',
    'Isfahan', 'Shiraz', 'Tabriz', 'Samarkand', 'Bukhara', 'Kazan',
    'Krakow', 'Prague', 'Florence', 'Rome', 'Granada', 'Toledo',
    'Kyoto', 'Nara', 'Xi\'an', 'Luoyang', 'Nanjing', 'Chengdu',
    'Kandy', 'Mandalay', 'Bagan', 'Hue', 'Merida', 'Oaxaca',
    'Cusco', 'Arequipa', 'Cartagena', 'Quito', 'Sucre',
    'Antigua', 'San Miguel de Allende', 'Guanajuato',
    'Saint Petersburg', 'Moscow', 'Tbilisi', 'Baku',
    'Thessaloniki', 'Cordoba', 'Seville', 'Bruges',
    'Kanazawa', 'Kamakura', 'Matsumoto',
    'Hyderabad', 'Mysore', 'Jodhpur', 'Udaipur', 'Amritsar',
    'Chiang Mai', 'Luang Prabang', 'Phnom Penh',
    'Fes', 'Meknes', 'Essaouira',
}

# Known nature / mountain / adventure destinations
NATURE_CITIES = {
    'Kathmandu', 'Pokhara', 'Lhasa', 'Kunming', 'Lijiang',
    'Medellín', 'Medellin', 'Quito', 'La Paz', 'Bogota',
    'Nairobi', 'Addis Ababa', 'Kampala', 'Kigali',
    'Innsbruck', 'Interlaken', 'Queenstown',
    'Reykjavik', 'Tromso', 'Bergen',
    'Almaty', 'Bishkek', 'Tbilisi', 'Yerevan',
    'Cusco', 'Huaraz', 'Bariloche',
    'Chiang Mai', 'Chiang Rai', 'Da Lat',
    'Colorado Springs', 'Denver', 'Salt Lake City', 'Boise',
    'Anchorage', 'Juneau',
}

# Countries known for specific vibes
FOOD_COUNTRIES = {
    'Japan', 'South Korea', 'Thailand', 'Vietnam', 'India', 'Mexico',
    'Italy', 'France', 'Spain', 'Turkey', 'Peru', 'China', 'Taiwan',
    'Greece', 'Morocco', 'Lebanon', 'Portugal', 'Malaysia', 'Singapore',
}

NIGHTLIFE_COUNTRIES = {
    'Spain', 'Brazil', 'Colombia', 'Argentina', 'Thailand',
    'Germany', 'United Kingdom', 'Netherlands',
}


def assign_vibes(name: str, country: str, continent: str, lat: float, lng: float, population: int) -> list[str]:
    """Assign vibes based on city characteristics, geography, and known attributes."""
    vibes = []

    # Beach cities
    if name in BEACH_CITIES:
        vibes = ['Beach', 'Relaxation', 'Food']
    # Historical cities
    elif name in HISTORICAL_CITIES:
        vibes = ['Cultural', 'History', 'Romantic']
    # Nature cities
    elif name in NATURE_CITIES:
        vibes = ['Nature', 'Adventure', 'Hiking']
    # Megacities — always City + Food + Cultural
    elif population >= 8_000_000:
        vibes = ['City', 'Food', 'Cultural']
    # Large cities with nightlife countries
    elif population >= 2_000_000 and country in NIGHTLIFE_COUNTRIES:
        vibes = ['City', 'Nightlife', 'Food']
    # High-latitude cities (above 55°N) — nature-leaning
    elif abs(lat) > 55:
        vibes = ['Nature', 'City', 'Cultural']
    # Tropical islands / small island nations
    elif abs(lat) < 25 and continent == 'Oceania':
        vibes = ['Beach', 'Nature', 'Relaxation']
    # Tropical African coast
    elif abs(lat) < 15 and continent == 'Africa':
        vibes = ['Cultural', 'Nature', 'Adventure']
    # Food countries — large cities
    elif country in FOOD_COUNTRIES and population >= 1_000_000:
        vibes = ['City', 'Food', 'Cultural']
    # Food countries — smaller cities
    elif country in FOOD_COUNTRIES:
        vibes = ['Food', 'Cultural', 'City']
    # Desert / arid belt (lat 15-35, Middle East / North Africa)
    elif 15 <= abs(lat) <= 35 and continent in ('Asia', 'Africa') and country in (
        'Saudi Arabia', 'United Arab Emirates', 'Oman', 'Qatar', 'Bahrain',
        'Egypt', 'Libya', 'Tunisia', 'Algeria', 'Morocco', 'Jordan',
        'Iran', 'Pakistan',
    ):
        vibes = ['Cultural', 'City', 'History']
    # European cities — lean cultural/romantic
    elif continent == 'Europe':
        if population >= 1_000_000:
            vibes = ['City', 'Cultural', 'Food']
        else:
            vibes = ['Cultural', 'Romantic', 'City']
    # Large Asian cities
    elif continent == 'Asia' and population >= 2_000_000:
        vibes = ['City', 'Food', 'Cultural']
    elif continent == 'Asia':
        vibes = ['Cultural', 'Food', 'City']
    # South American cities
    elif continent == 'South America':
        if population >= 2_000_000:
            vibes = ['City', 'Food', 'Cultural']
        else:
            vibes = ['Cultural', 'Nature', 'Food']
    # North American cities
    elif continent == 'North America':
        if population >= 1_000_000:
            vibes = ['City', 'Food', 'Cultural']
        else:
            vibes = ['City', 'Food', 'Cultural']
    # African cities
    elif continent == 'Africa':
        if population >= 2_000_000:
            vibes = ['City', 'Cultural', 'Food']
        else:
            vibes = ['Cultural', 'Adventure', 'Nature']
    else:
        vibes = ['City', 'Cultural', 'Food']

    return vibes


def assign_travel(name: str, vibes: list[str], population: int, country: str) -> list[str]:
    """Assign travel styles based on vibes and city characteristics."""
    vibe_set = set(vibes)

    if 'Beach' in vibe_set:
        if population >= 1_000_000:
            return ['beach', 'food', 'couples']
        return ['couples', 'beach', 'relaxation']
    elif 'Nature' in vibe_set and 'Adventure' in vibe_set:
        return ['adventure', 'photography', 'hiking']
    elif 'Nature' in vibe_set and 'Hiking' in vibe_set:
        return ['adventure', 'photography', 'hiking']
    elif 'History' in vibe_set:
        return ['history', 'solo', 'couples']
    elif 'Nightlife' in vibe_set:
        return ['solo', 'food', 'friends']
    elif 'Romantic' in vibe_set:
        return ['couples', 'photography', 'relaxation']
    elif population >= 5_000_000:
        return ['solo', 'food', 'weekend']
    elif population >= 1_000_000:
        return ['solo', 'food', 'couples']
    elif country in FOOD_COUNTRIES:
        return ['food', 'solo', 'couples']
    else:
        return ['solo', 'food', 'weekend']


# ---------------------------------------------------------------------------
# Budget — country-level where possible, continent fallback
# ---------------------------------------------------------------------------

BUDGET_COUNTRY = {
    # Expensive
    'Japan': '$$$', 'South Korea': '$$$', 'Singapore': '$$$$',
    'Australia': '$$$$', 'New Zealand': '$$$',
    'Switzerland': '$$$$', 'Norway': '$$$$', 'Sweden': '$$$', 'Denmark': '$$$',
    'Iceland': '$$$$', 'Finland': '$$$', 'Ireland': '$$$',
    'United Kingdom': '$$$', 'France': '$$$', 'Netherlands': '$$$',
    'United States': '$$$', 'Canada': '$$$',
    'United Arab Emirates': '$$$', 'Qatar': '$$$$', 'Israel': '$$$',
    'Saudi Arabia': '$$',
    # Mid-range
    'Spain': '$$', 'Italy': '$$', 'Portugal': '$$', 'Greece': '$$',
    'Turkey': '$$', 'Mexico': '$$', 'Brazil': '$$', 'Argentina': '$$',
    'Colombia': '$$', 'Peru': '$$', 'Chile': '$$',
    'China': '$$', 'Taiwan': '$$', 'Malaysia': '$$',
    'Thailand': '$', 'Vietnam': '$', 'Indonesia': '$',
    'Philippines': '$', 'Myanmar': '$', 'Cambodia': '$', 'Laos': '$',
    'India': '$', 'Nepal': '$', 'Sri Lanka': '$', 'Bangladesh': '$', 'Pakistan': '$',
    'Egypt': '$', 'Morocco': '$$', 'Tunisia': '$',
    'Kenya': '$$', 'Tanzania': '$$', 'South Africa': '$$',
    'Ethiopia': '$', 'Uganda': '$', 'Ghana': '$', 'Nigeria': '$',
    'Poland': '$$', 'Czech Republic': '$$', 'Hungary': '$$',
    'Romania': '$', 'Bulgaria': '$', 'Croatia': '$$', 'Serbia': '$',
    'Russia': '$$', 'Ukraine': '$', 'Georgia': '$',
    'Iran': '$', 'Jordan': '$$', 'Oman': '$$',
    'Bolivia': '$', 'Ecuador': '$', 'Paraguay': '$',
}

BUDGET_CONTINENT_FALLBACK = {
    'Europe': '$$$',
    'Asia': '$$',
    'Africa': '$$',
    'North America': '$$$',
    'South America': '$$',
    'Oceania': '$$$',
}


def assign_budget(country: str, continent: str) -> str:
    return BUDGET_COUNTRY.get(country, BUDGET_CONTINENT_FALLBACK.get(continent, '$$'))


# ---------------------------------------------------------------------------
# Season — more granular by country/region
# ---------------------------------------------------------------------------

SEASON_COUNTRY = {
    # Tropical year-round
    'Singapore': 'Year-round', 'Malaysia': 'Year-round', 'Indonesia': 'Year-round',
    'Thailand': 'Nov–Apr', 'Vietnam': 'Oct–Apr', 'Cambodia': 'Nov–Apr',
    'Philippines': 'Dec–May', 'Myanmar': 'Nov–Feb', 'Laos': 'Nov–Feb',
    'Sri Lanka': 'Dec–Mar', 'Bangladesh': 'Nov–Mar',
    'Colombia': 'Year-round', 'Ecuador': 'Year-round', 'Kenya': 'Year-round',
    'Tanzania': 'Jun–Oct', 'Uganda': 'Jun–Sep',
    'Ghana': 'Nov–Mar', 'Nigeria': 'Nov–Mar',
    'Ethiopia': 'Oct–Jun',
    # Desert / arid
    'Egypt': 'Oct–Apr', 'Morocco': 'Mar–May', 'Tunisia': 'Apr–Oct',
    'Jordan': 'Mar–May', 'Oman': 'Oct–Mar',
    'Saudi Arabia': 'Nov–Feb', 'United Arab Emirates': 'Nov–Mar',
    'Iran': 'Apr–Jun',
    # Temperate
    'Japan': 'Mar–May', 'South Korea': 'Apr–Jun',
    'China': 'Apr–Oct', 'Taiwan': 'Oct–Dec',
    'India': 'Oct–Mar', 'Nepal': 'Oct–Dec', 'Pakistan': 'Oct–Mar',
    'Turkey': 'Apr–Oct', 'Greece': 'Apr–Oct',
    'Spain': 'Apr–Oct', 'Italy': 'Apr–Oct', 'Portugal': 'Apr–Oct',
    'France': 'May–Sep', 'Germany': 'May–Sep',
    'United Kingdom': 'May–Sep', 'Ireland': 'Jun–Sep',
    'Netherlands': 'Apr–Sep',
    'Mexico': 'Nov–Apr', 'Brazil': 'Apr–Oct',
    'Argentina': 'Oct–Apr', 'Chile': 'Oct–Mar', 'Peru': 'May–Sep',
    'Australia': 'Sep–Nov', 'New Zealand': 'Dec–Feb',
    'South Africa': 'Sep–Apr',
    'United States': 'Apr–Oct', 'Canada': 'Jun–Sep',
    'Russia': 'Jun–Sep',
    'Poland': 'May–Sep', 'Czech Republic': 'May–Sep', 'Hungary': 'Apr–Oct',
    'Croatia': 'May–Sep', 'Romania': 'May–Sep',
    'Iceland': 'Jun–Aug', 'Norway': 'Jun–Aug', 'Sweden': 'Jun–Aug',
    'Finland': 'Jun–Aug', 'Denmark': 'Jun–Aug',
}

SEASON_CONTINENT_FALLBACK = {
    'Europe': 'Apr–Oct',
    'Asia': 'Oct–May',
    'Africa': 'Nov–Apr',
    'North America': 'Apr–Oct',
    'South America': 'Apr–Nov',
    'Oceania': 'May–Oct',
}


def assign_season(country: str, continent: str, lat: float) -> str:
    if country in SEASON_COUNTRY:
        return SEASON_COUNTRY[country]
    # Tropical belt — year-round if near equator
    if abs(lat) < 10:
        return 'Year-round'
    return SEASON_CONTINENT_FALLBACK.get(continent, 'Year-round')


# ---------------------------------------------------------------------------
# Pitch templates — more variety
# ---------------------------------------------------------------------------

def pitch_for(name: str, country: str, population: int, vibes: list[str]) -> str:
    vibe_set = set(vibes)

    if population >= 8_000_000:
        return f'{name} is a true megacity: dense, layered, and big enough to justify building an entire trip around its neighborhoods, food scenes, and back streets.'
    if 'Beach' in vibe_set and population >= 1_000_000:
        return f'{name} pairs a serious coastline with real urban energy — enough restaurants, markets, and nightlife to fill a full week without repeating yourself.'
    if 'Beach' in vibe_set:
        return f'{name} is a coastal base in {country} where the beach life comes with good local food and a pace that rewards slowing down.'
    if 'History' in vibe_set and population >= 1_000_000:
        return f'{name} is one of {country}\'s deepest historical cities — layers of architecture, old quarters worth getting lost in, and a food culture that\'s been evolving for centuries.'
    if 'History' in vibe_set:
        return f'{name} trades tourist polish for lived-in authenticity — a {country} city where the history is still part of daily life, not behind ropes.'
    if 'Nature' in vibe_set and 'Adventure' in vibe_set:
        return f'{name} is an adventure base in {country}: close enough to mountains, trails, or wild landscapes to justify the trip, with urban comforts to return to.'
    if 'Nightlife' in vibe_set:
        return f'{name} is a {country} city that comes alive after dark — strong food scene, good bars, and enough local energy to make it worth staying a few nights.'
    if population >= 3_000_000:
        return f'{name} is a major city break in {country} with enough food, street life, and cultural weight to support a real stay rather than a quick stop.'
    if population >= 1_000_000:
        return f'{name} is a high-utility urban base in {country} with strong local food, walkable core districts, and enough city energy to earn a few full days.'
    if 'Romantic' in vibe_set:
        return f'{name} is the kind of {country} city that rewards wandering — smaller scale, local food, and atmosphere that works better in pairs.'
    if 'Cultural' in vibe_set and 'Nature' in vibe_set:
        return f'{name} blends culture and natural surroundings in {country} — a good base for travelers who want both city texture and easy escapes.'
    return f'{name} is a worthwhile secondary city in {country} that works best for travelers who want a less obvious stop without giving up food or cultural payoff.'


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def curl(url: str) -> str:
    return subprocess.check_output(['curl', '-L', '--fail', '--silent', url], text=True)


def normalize_ascii(text: str) -> str:
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    return text


def slugify(name: str) -> str:
    s = normalize_ascii(name).casefold().replace('\u2019', "'")
    s = re.sub(r"[^a-z0-9\s-]", '', s)
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')


def clean_country(name: str) -> str:
    name = name.strip()
    name = COUNTRY_OVERRIDES.get(name, name)
    return name


def clean_city(name: str) -> str:
    return NAME_RENAMES.get(name.strip(), name.strip())


def build_country_to_continent() -> dict[str, str]:
    raw = curl(COUNTRY_CONTINENTS_URL)
    mapping: dict[str, str] = {}
    for row in csv.DictReader(io.StringIO(raw)):
        country = row['Country_Name'].strip()
        continent = row['Continent_Name'].strip()
        country = re.sub(r',.*$', '', country)
        mapping[country] = continent
    mapping.update(MANUAL_CONTINENTS)
    mapping.update({
        'United States': 'North America',
        'Mexico': 'North America',
        'Puerto Rico': 'North America',
        'Dominican Republic': 'North America',
        'Czech Republic': 'Europe',
        'South Korea': 'Asia',
        'North Korea': 'Asia',
        'Laos': 'Asia',
        'Moldova': 'Europe',
        'Russia': 'Europe',
        'Cape Verde': 'Africa',
        'Palestine': 'Asia',
        'Macau': 'Asia',
        'Hong Kong': 'Asia',
    })
    return mapping


def existing_keys(rows: list[dict]) -> tuple[set[str], set[str]]:
    names = set()
    slugs = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        name = (row.get('name') or '').strip()
        if not name:
            continue
        names.add(name.casefold())
        slugs.add(slugify(name))
    return names, slugs


def is_bad_candidate(name: str, country: str) -> bool:
    if not name or not country:
        return True
    if name in EXCLUDED_NAMES:
        return True
    if any(tok in name for tok in BAD_TOKENS):
        return True
    if len(name) < 3:
        return True
    if re.search(r'\b(arrondissement|municipality|commune)\b', name, flags=re.I):
        return True
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    data = json.loads(SOURCE.read_text())
    existing_names, existing_slugs = existing_keys(data)
    country_to_continent = build_country_to_continent()

    raw = curl(WORLD_CITIES_URL)
    rows = list(csv.DictReader(io.StringIO(raw)))
    rows.sort(key=lambda r: int(float(r['population'] or 0)), reverse=True)

    additions = []
    seen_addition_slugs = set()
    for row in rows:
        name = clean_city(row['city'])
        country = clean_country(row['country'])
        if name == 'Hillah':
            country = 'Iraq'
        continent = country_to_continent.get(country)
        if not continent:
            continue
        if continent == 'Antarctica':
            continue
        if country in EXCLUDED_REGIONS:
            continue
        if is_bad_candidate(name, country):
            continue
        slug = slugify(name)
        if name.casefold() in existing_names or slug in existing_slugs or slug in seen_addition_slugs:
            continue
        population = int(float(row['population'] or 0))
        if population < 250000:
            continue

        lat = float(row.get('lat', 0) or 0)
        lng = float(row.get('lng', 0) or 0)

        vibes = assign_vibes(name, country, continent, lat, lng, population)
        travel = assign_travel(name, vibes, population, country)

        additions.append({
            'name': name,
            'region': country,
            'continent': continent,
            'photo': FALLBACK_PHOTO,
            'pitch': pitch_for(name, country, population, vibes),
            'budget': assign_budget(country, continent),
            'season': assign_season(country, continent, lat),
            'vibes': vibes,
            'travel': travel,
        })
        seen_addition_slugs.add(slug)
        if len(additions) >= TARGET_ADD:
            break

    if len(additions) < TARGET_ADD:
        print(f'Warning: only found {len(additions)} candidates (target was {TARGET_ADD})')

    data.extend(additions)
    data.sort(key=lambda r: normalize_ascii(r.get('name', '')).casefold())
    SOURCE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')

    # Stats
    from collections import Counter
    vibe_combos = Counter(tuple(a['vibes']) for a in additions)
    print(f'added={len(additions)} total={len(data)}')
    print(f'unique vibe combos in new batch: {len(vibe_combos)}')
    for combo, count in vibe_combos.most_common(10):
        print(f'  {list(combo)}: {count}')
    print(f'first10= {[r["name"] for r in additions[:10]]}')
    print(f'last10= {[r["name"] for r in additions[-10:]]}')


if __name__ == '__main__':
    main()