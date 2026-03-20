from __future__ import annotations

import csv
import io
import json
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
    'Giza',  # already present as a better travel-facing record
    'Luxor',  # use the more travel-facing Luxor West Bank already present
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
}

BAD_TOKENS = ('Province', 'District', 'County', 'Prefecture')
EXCLUDED_REGIONS = {'Afghanistan', 'Iraq', 'Yemen', 'Sudan'}

CITY_VIBES = ['City', 'Food', 'Cultural']
CITY_TRAVEL = ['solo', 'food', 'weekend']
BUDGET_MAP = {
    'Europe': '$$$',
    'Asia': '$$',
    'Africa': '$$',
    'North America': '$$$',
    'South America': '$$',
    'Oceania': '$$$',
}
SEASON_MAP = {
    'Europe': 'Apr–Oct',
    'Asia': 'Oct–May',
    'Africa': 'Nov–Apr',
    'North America': 'Apr–Oct',
    'South America': 'Apr–Nov',
    'Oceania': 'May–Oct',
}


def curl(url: str) -> str:
    return subprocess.check_output(['curl', '-L', '--fail', '--silent', url], text=True)


def normalize_ascii(text: str) -> str:
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    return text


def slugify(name: str) -> str:
    s = normalize_ascii(name).casefold().replace('’', "'")
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
    # extra aliases used by the city dataset / repo
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


def pitch_for(name: str, country: str, population: int) -> str:
    if population >= 8_000_000:
        return f'{name} is a true megacity destination: dense, food-rich, and big enough to justify building an entire trip around its neighborhoods alone.'
    if population >= 3_000_000:
        return f'{name} is a major city break in {country} with enough food, street life, and cultural weight to support a real stay rather than a quick stop.'
    if population >= 1_000_000:
        return f'{name} is a high-utility urban base in {country} with strong local food, walkable core districts, and enough city energy to earn a few full days.'
    return f'{name} is a worthwhile secondary city in {country} that works best for travelers who want a less obvious urban stop without giving up food or cultural payoff.'


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
        additions.append({
            'name': name,
            'region': country,
            'continent': continent,
            'photo': FALLBACK_PHOTO,
            'pitch': pitch_for(name, country, population),
            'budget': BUDGET_MAP.get(continent, '$$'),
            'season': SEASON_MAP.get(continent, 'Year-round'),
            'vibes': CITY_VIBES,
            'travel': CITY_TRAVEL,
        })
        seen_addition_slugs.add(slug)
        if len(additions) >= TARGET_ADD:
            break

    if len(additions) != TARGET_ADD:
        raise SystemExit(f'Expected {TARGET_ADD} additions, got {len(additions)}')

    data.extend(additions)
    data.sort(key=lambda r: normalize_ascii(r.get('name', '')).casefold())
    SOURCE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')

    print(f'added={len(additions)} total={len(data)}')
    print('first10=', [r['name'] for r in additions[:10]])
    print('last10=', [r['name'] for r in additions[-10:]])


if __name__ == '__main__':
    main()
