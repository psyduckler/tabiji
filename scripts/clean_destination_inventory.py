from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'find' / 'destinations.json'
SNAPSHOT = ROOT / 'scripts' / 'data' / 'next-2000-destinations-source.json'

DROP_NAMES = {
    'Banska Stiavnica',
    'Brasov',
    'Cesis',
    'Cesky Krumlov',
    'Córdoba Argentina',
    'Jurmala',
    'Kas',
    'Klaipeda',
    'Kosice',
    'Krakow',
    'Maramures',
    'Medellin',
    'Medellin, Colombia',
    'Poznan',
    'Sharm El Sheikh',
    'Sighisoara',
    'Telc',
    'Torshavn',
}

RENAME_MAP = {}


def norm_text(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode().lower()
    text = re.sub(r'[^a-z0-9]+', ' ', text).strip()
    return text


def main() -> None:
    destinations = json.loads(SOURCE.read_text(encoding='utf-8'))
    cleaned = []
    for item in destinations:
        if item['name'] in DROP_NAMES:
            continue
        item = dict(item)
        item['name'] = RENAME_MAP.get(item['name'], item['name'])
        cleaned.append(item)

    cleaned.sort(key=lambda item: norm_text(item['name']))
    SOURCE.write_text(json.dumps(cleaned, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    if SNAPSHOT.exists():
        additions = json.loads(SNAPSHOT.read_text(encoding='utf-8'))
        for item in additions:
            item['name'] = RENAME_MAP.get(item['name'], item['name'])
        additions = [item for item in additions if item['name'] not in DROP_NAMES]
        additions.sort(key=lambda item: norm_text(item['name']))
        SNAPSHOT.write_text(json.dumps(additions, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    print(f'Cleaned inventory to {len(cleaned)} destinations')


if __name__ == '__main__':
    main()
