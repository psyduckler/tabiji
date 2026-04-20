from __future__ import annotations

import json
import re
import unicodedata
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE_SOURCE = ROOT / 'find' / 'destinations.json'
GEONAMES_ZIP = ROOT / 'tmp' / 'geonames' / 'cities5000.zip'
COUNTRY_INFO = ROOT / 'tmp' / 'geonames' / 'countryInfo.txt'
ADMIN1_INFO = ROOT / 'tmp' / 'geonames' / 'admin1CodesASCII.txt'
OUTPUT_SNAPSHOT = ROOT / 'scripts' / 'data' / 'next-3000-destinations-source.json'
TARGET_ADD = 3000
FALLBACK_PHOTO = 'https://img.tabiji.ai/owl-logo.png'

CONTINENT_MAP = {
    'AF': 'Africa',
    'AS': 'Asia',
    'EU': 'Europe',
    'NA': 'North America',
    'OC': 'Oceania',
    'SA': 'South America',
    'AN': 'Polar',
}

EXCLUDED_COUNTRIES = {
    'Afghanistan', 'Iraq', 'Yemen', 'Sudan',
    'Somalia', 'Central African Republic', 'Haiti',
    'North Korea', 'Syria', 'Libya',
}

HIGH_BUDGET = {
    'AD','AE','AT','AU','BE','BM','BS','CA','CH','DE','DK','FI','FR','GB','HK','IE','IL','IS','JP','KR','KW','LU','MO','NL','NO','NZ','QA','SE','SG','US'
}
MID_BUDGET = {
    'AR','AZ','BA','BH','BN','BR','BW','CL','CN','CO','CR','CY','CZ','EE','ES','GR','HR','HU','IT','JO','KZ','LB','LT','LV','ME','MX','MY','OM','PA','PL'
}
LOW_BUDGET = {
    'AL','AM','BD','BG','BO','BY','DZ','EC','EG','ET','GE','GH','GT','HN','ID','IN','IQ','IR','KE','KG','KH','LK','MA','MD','MK','MN','NP','PE','PH','PK','PY','RO','RS','RW','TH','TJ','TN','TR','TW','TZ','UA','UG','UY','UZ','VN','ZA'
}

SKIP_NAME_KEYS = {
    'ueruemqi', 'koeln', 'goeteborg', 'malmoe', 'saarbruecken', 'linkoeping', 'goelbasi',
    'bingoel', 'joenkoeping', 'klagenfurt am woerthersee', 'the bronx', 'phasi charoen',
    'khlong toei', 'dharavi', 'new kingston', 'new south memphis'
}

CITY_PITCHES = [
    '{name} is a strong city break for travelers who want food, walkable neighborhoods, and enough cultural weight to keep the trip from feeling generic.',
    '{name} works best as an easy urban base with strong local food, day-trip range, and enough personality to justify more than a stopover.',
    '{name} is the kind of city that rewards unhurried wandering: markets, street life, and enough texture to keep a short trip interesting.',
    '{name} earns its keep with local food, busy public life, and enough regional identity to feel specific instead of interchangeable.',
]


def norm_text(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', ' ', text).strip()


def slugify(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', norm_text(text)).strip('-')


def parse_country_info() -> dict[str, dict[str, str]]:
    countries = {}
    for line in COUNTRY_INFO.read_text(encoding='utf-8').splitlines():
        if not line or line.startswith('#'):
            continue
        parts = line.split('\t')
        if len(parts) < 18:
            continue
        iso = parts[0]
        countries[iso] = {
            'name': parts[4],
            'continent': CONTINENT_MAP.get(parts[8], parts[8]),
        }
    return countries


def parse_admin1() -> dict[str, str]:
    mapping = {}
    for line in ADMIN1_INFO.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        code, name, ascii_name, _ = line.split('\t')
        mapping[code] = ascii_name or name
    return mapping


def budget_for(country_code: str, continent: str) -> str:
    if country_code in HIGH_BUDGET:
        return '$$$'
    if country_code in LOW_BUDGET:
        return '$'
    if country_code in MID_BUDGET:
        return '$$'
    return '$$$' if continent in {'Europe', 'North America', 'Oceania'} else '$$'


def season_for(continent: str, country_code: str) -> str:
    if continent in {'Europe', 'North America'}:
        return 'Apr–Oct'
    if continent == 'Asia':
        return 'Oct–Apr'
    if continent == 'Africa':
        return 'Oct–Apr'
    if continent == 'South America':
        return 'Apr–Nov'
    if continent == 'Oceania':
        return 'Oct–Apr'
    if country_code in {'SG', 'MY', 'ID', 'CO', 'EC'}:
        return 'Year-round'
    return 'Year-round'


def vibes_for(population: int) -> list[str]:
    if population >= 1_500_000:
        return ['City', 'Food', 'Nightlife']
    if population >= 500_000:
        return ['City', 'Cultural', 'Food']
    return ['City', 'Cultural', 'Local Life']


def travel_for(population: int) -> list[str]:
    if population >= 1_500_000:
        return ['solo', 'food', 'nightlife']
    if population >= 500_000:
        return ['solo', 'food', 'weekend']
    return ['solo', 'food', 'local-life']


def pitch_for(name: str, population: int) -> str:
    return CITY_PITCHES[population % len(CITY_PITCHES)].format(name=name)


def load_baseline() -> tuple[list[dict], set[str], set[str]]:
    baseline = json.loads(BASELINE_SOURCE.read_text(encoding='utf-8'))
    name_keys = {norm_text(item['name']) for item in baseline}
    slug_keys = {slugify(item['name']) for item in baseline}
    return baseline, name_keys, slug_keys


def iter_geonames():
    with zipfile.ZipFile(GEONAMES_ZIP) as zf:
        with zf.open('cities5000.txt') as fh:
            for raw in fh:
                parts = raw.decode('utf-8').rstrip('\n').split('\t')
                if len(parts) < 19:
                    continue
                yield {
                    'geonameid': int(parts[0]),
                    'name': parts[1].strip(),
                    'asciiname': parts[2].strip(),
                    'latitude': parts[4],
                    'longitude': parts[5],
                    'feature_class': parts[6],
                    'feature_code': parts[7],
                    'country_code': parts[8],
                    'admin1_code': parts[10],
                    'population': int(parts[14] or 0),
                }


def is_usable_name(name: str) -> bool:
    if not name or len(name) < 3:
        return False
    if any(ch.isdigit() for ch in name):
        return False
    if '(' in name or ')' in name or '/' in name:
        return False
    return True


def choose_name(record: dict) -> str:
    name = (record['asciiname'] or record['name']).strip()
    if not is_usable_name(name):
        name = record['name'].strip()
    return name.strip()


def main() -> None:
    countries = parse_country_info()
    admin1 = parse_admin1()
    baseline, existing_names, existing_slugs = load_baseline()
    additions = []
    new_names = set()
    new_slugs = set()

    allowed_feature_codes = {'PPLC', 'PPLA', 'PPLA2'}

    for record in sorted(iter_geonames(), key=lambda r: (-r['population'], norm_text(r['asciiname'] or r['name']), r['geonameid'])):
        if record['feature_class'] != 'P':
            continue
        if record['feature_code'] not in allowed_feature_codes:
            continue
        if record['population'] < 50000:
            continue
        if record['country_code'] not in countries:
            continue

        country = countries[record['country_code']]
        if country['name'] in EXCLUDED_COUNTRIES:
            continue

        name = choose_name(record)
        if not is_usable_name(name):
            continue
        lower_name = name.lower()
        if 'district' in lower_name or 'new town' in lower_name or lower_name in SKIP_NAME_KEYS:
            continue

        name_key = norm_text(name)
        slug_key = slugify(name)
        if not name_key or not slug_key:
            continue
        if name_key in existing_names or slug_key in existing_slugs:
            continue
        if name_key in new_names or slug_key in new_slugs:
            continue

        continent = country['continent']
        region_key = f"{record['country_code']}.{record['admin1_code']}"
        region = admin1.get(region_key) or country['name']
        population = record['population']

        addition = {
            'name': name,
            'region': region,
            'continent': continent,
            'photo': FALLBACK_PHOTO,
            'pitch': pitch_for(name, population),
            'budget': budget_for(record['country_code'], continent),
            'season': season_for(continent, record['country_code']),
            'vibes': vibes_for(population),
            'travel': travel_for(population),
            'source': {
                'geonameid': record['geonameid'],
                'country_code': record['country_code'],
                'population': population,
                'admin1_code': record['admin1_code'],
                'latitude': record['latitude'],
                'longitude': record['longitude'],
            }
        }
        additions.append(addition)
        new_names.add(name_key)
        new_slugs.add(slug_key)
        if len(additions) == TARGET_ADD:
            break

    if len(additions) != TARGET_ADD:
        raise SystemExit(f'Only found {len(additions)} additions, expected {TARGET_ADD}')

    OUTPUT_SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_SNAPSHOT.write_text(json.dumps(additions, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    merged = baseline + [
        {
            'name': item['name'],
            'region': item['region'],
            'continent': item['continent'],
            'photo': item['photo'],
            'pitch': item['pitch'],
            'budget': item['budget'],
            'season': item['season'],
            'vibes': item['vibes'],
            'travel': item['travel'],
        }
        for item in additions
    ]
    merged.sort(key=lambda item: norm_text(item['name']))
    BASELINE_SOURCE.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    print(f'Added {len(additions)} destinations; new total: {len(merged)}')
    print('first10=', [item['name'] for item in additions[:10]])
    print('last10=', [item['name'] for item in additions[-10:]])


if __name__ == '__main__':
    main()
