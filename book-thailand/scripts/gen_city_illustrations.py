#!/usr/bin/env python3
"""
Generate 16 per-city cover illustrations for the France book via Wavespeed
(Nano Banana Pro).

Style brief — must match the Japan and Italy volumes' city covers:
  - Flat vector illustration, mid-century travel-book poster aesthetic
  - Warm cream / saffron / burgundy / deep-purple / muted teal palette,
    golden-hour light
  - Tourist figure in deep-burgundy jacket with small backpack, stylised
  - 1:1 aspect, 2K resolution, JPEG

Output: book-france/assets/cities/<slug>.jpg

Usage:
    python3 book-france/scripts/gen_city_illustrations.py              # all 16 cities
    python3 book-france/scripts/gen_city_illustrations.py paris        # just paris
    python3 book-france/scripts/gen_city_illustrations.py paris nice   # multiple specific cities
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import requests  # noqa: pip install requests


HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
OUT = BOOK / "assets" / "cities"
OUT.mkdir(parents=True, exist_ok=True)

STYLE_BASE = (
    "Flat vector travel-poster illustration in mid-century style. "
    "Warm cream background, palette of saffron-gold, deep burgundy, "
    "dusty purple and muted teal. Soft golden-hour light. "
    "Clean geometric shapes, visible paper-grain texture, "
    "no text, no words, no logos, no watermark. "
    "Square 1:1 composition, gentle depth, soft shadows."
)

TRAVELER_M = (
    "One stylised solo male traveler, short dark hair, wearing a "
    "deep-burgundy jacket and a small backpack, seen from behind or "
    "three-quarter view, looking toward the scene. "
)

TRAVELER_F = (
    "One stylised solo female traveler, shoulder-length dark hair, "
    "wearing a deep-burgundy jacket and a small backpack, seen from "
    "behind or three-quarter view, looking toward the scene. "
)

# (slug, subject, gender) — gender alternates within the reading order
CITIES: list[tuple[str, str, str]] = [
    (
        "bangkok",
        "Wat Arun temple on the west bank of the Chao Phraya river at dusk, the prang spire "
        "silhouetted in silver against a warm saffron sky, longtail boats on the river in the "
        "foreground, soft golden-hour haze.",
        "m",
    ),
    (
        "chiang-mai",
        "The naga-balustrade stairs leading up to Doi Suthep temple at late afternoon, dappled "
        "light through surrounding forest, the golden chedi visible at the top of the climb, "
        "soft warm mountain light.",
        "f",
    ),
    (
        "ayutthaya",
        "The stone Buddha head tangled in the roots of a banyan tree at Wat Mahathat, ancient "
        "brick ruins in the middle distance, warm sunset over the Ayutthaya historical park, "
        "soft ochre tones.",
        "m",
    ),
    (
        "pattaya",
        "Pattaya Beach Road at dusk, a crescent of sand curving along the Gulf of Thailand, "
        "palms silhouetted against the warm twilight sky, distant hotels and the neon glow of "
        "Walking Street visible inland.",
        "f",
    ),
    (
        "hua-hin",
        "The Hua Hin royal railway-station pavilion at golden hour, its ornate Thai-royal "
        "wooden gables with red-and-cream paintwork, palm trees and a slow-moving train in the "
        "background, warm late-afternoon light.",
        "m",
    ),
    (
        "phuket",
        "Karon Beach at sunset with a row of longtail boats tied up in the shallows, their "
        "brightly painted bows and long stern poles silhouetted against a warm pink-orange "
        "Andaman sky, soft turquoise water.",
        "f",
    ),
    (
        "krabi",
        "The Railay peninsula karst cliffs rising vertically out of turquoise Andaman water, "
        "a few longtail boats anchored at the beach, dramatic limestone formations, warm "
        "late-afternoon sun casting long shadows on the cliffs.",
        "m",
    ),
    (
        "koh-samui",
        "Chaweng Beach at sunset, a long palm-fringed sand curve with gentle waves, a few "
        "beach umbrellas and lounge chairs in the middle distance, warm pink-gold sky, "
        "soft Gulf of Thailand water.",
        "f",
    ),
    (
        "koh-phangan",
        "The Haad Rin headland at moonrise, rocky outcroppings meeting the Gulf of Thailand, "
        "the beach curving out of sight, soft-blue dusk sky with a full moon rising over the "
        "sea, a hint of distant beach-party lights.",
        "m",
    ),
    (
        "koh-tao",
        "The Nang Yuan twin-island sandbar viewpoint — three small islands joined by a narrow "
        "white-sand spit surrounded by turquoise water, seen from the elevated viewpoint, "
        "warm late-afternoon Gulf of Thailand light, palm silhouettes.",
        "f",
    ),
    (
        "koh-phi-phi",
        "Maya Bay limestone cliffs curving around a shallow turquoise cove at golden hour, "
        "the iconic Leonardo DiCaprio beach with a single longtail boat anchored offshore, "
        "dramatic karst walls in warm afternoon light.",
        "m",
    ),
]


# (slug, subject, gender) — France/prior-volume cities kept here as reference so we can
# regenerate them from the same script if ever needed. We only iterate the Thailand set
# for the current volume because the book-thailand config.yaml lists only Thai cities.
_PRIOR_VOLUME_CITIES: list[tuple[str, str, str]] = [
    (
        "paris",
        "The Eiffel Tower at dusk viewed from across the Seine, Haussmann-era rooftops in the "
        "middle distance, the tower silhouetted against a saffron sky, soft golden-hour haze.",
        "m",
    ),
    (
        "nice",
        "The curve of the Promenade des Anglais along the Baie des Anges in Nice, pastel "
        "Belle-Époque seafront hotel facades, a pink-domed grand hotel silhouette, palm fronds, "
        "turquoise Mediterranean water at late-afternoon golden hour.",
        "f",
    ),
    (
        "cannes",
        "La Croisette palm-lined promenade at golden hour, the Palais des Festivals in the "
        "middle distance, the Mediterranean beyond, a few stylised palm silhouettes.",
        "m",
    ),
    (
        "st-tropez",
        "The Vieux Port of Saint-Tropez at dusk, pastel port-front houses, superyacht silhouettes "
        "in the harbor, warm Provençal ochre and dusty purple tones.",
        "f",
    ),
    (
        "marseille",
        "Notre-Dame de la Garde basilica crowning the hill above the Vieux-Port of Marseille, "
        "fishing boats in the foreground, late-afternoon Mediterranean light, the Château d'If "
        "in the haze.",
        "m",
    ),
    (
        "avignon",
        "The Palais des Papes rising above the Rhône river, the Pont Saint-Bénézet (Pont "
        "d'Avignon) reaching into the water in the foreground, warm Provençal stone, dusty "
        "purple evening sky.",
        "f",
    ),
    (
        "montpellier",
        "Place de la Comédie with the Three Graces fountain in the center, surrounding Haussmann "
        "buildings in warm cream, an outdoor café umbrella in silhouette, late-afternoon "
        "southern light.",
        "m",
    ),
    (
        "toulouse",
        "La Ville Rose at golden hour — pink-brick facades of Place du Capitole, the Basilique "
        "Saint-Sernin bell tower rising in the distance, a warm rosy glow over the rooftops.",
        "f",
    ),
    (
        "lyon",
        "Fourvière Basilica crowning the hill above the Saône river, the traboules of Vieux "
        "Lyon winding below, red-tile rooftops of the Presqu'île, warm golden-hour tones.",
        "m",
    ),
    (
        "chamonix",
        "The Aiguille du Midi and the Mont Blanc massif rising above the Chamonix valley, a "
        "single alpine chalet in the foreground, snow-capped peaks, clear blue-purple dusk sky.",
        "f",
    ),
    (
        "annecy",
        "The Palais de l'Île on its small triangular island in the canal of Annecy old town, "
        "pastel half-timbered facades along the water, turquoise Lake Annecy visible beyond, "
        "Alpine foothills in the distance.",
        "m",
    ),
    (
        "bordeaux",
        "The Place de la Bourse at golden hour with its Miroir d'Eau reflecting the "
        "eighteenth-century facade, warm honey-stone, a tram passing in the foreground, "
        "plane-tree silhouettes on the quay.",
        "f",
    ),
    (
        "biarritz",
        "The Grande Plage of Biarritz with the Rocher de la Vierge rock formation offshore, "
        "Basque surf-town coastline, late-afternoon Atlantic light, pastel Belle-Époque hotel "
        "facades on the bluff.",
        "m",
    ),
    (
        "strasbourg",
        "Strasbourg Cathedral rising above the half-timbered houses of Petite France reflected "
        "in the Ill river canals, warm gothic sandstone, winter Christmas-market lantern glow at "
        "dusk.",
        "f",
    ),
    (
        "colmar",
        "Petite Venise canal in Colmar with flower-boxed half-timbered Alsatian houses lining "
        "the water, pastel facades in cream and burgundy, a small flat-bottomed boat on the "
        "canal, late-afternoon warm light.",
        "m",
    ),
    (
        "mont-saint-michel",
        "The silhouette of Mont-Saint-Michel abbey rising from the tidal mudflats at dusk, the "
        "causeway reaching toward it across the bay, warm saffron sky, calm water reflecting "
        "the monastery.",
        "f",
    ),
]


def get_api_key() -> str:
    key = os.environ.get("WAVESPEED_API_KEY")
    if key:
        return key.strip()
    result = subprocess.run(
        ["security", "find-generic-password", "-s", "wavespeed-api-key", "-w"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        sys.exit("could not read WAVESPEED_API_KEY from keychain or env")
    return result.stdout.strip()


def submit(api_key: str, prompt: str) -> str:
    url = "https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image"
    r = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "prompt": prompt,
            "aspect_ratio": "1:1",
            "resolution": "2k",
            "output_format": "jpeg",
        },
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    if "data" in data and "id" in data["data"]:
        return data["data"]["id"]
    if "id" in data:
        return data["id"]
    raise RuntimeError(f"unexpected submit response: {data}")


def poll(api_key: str, task_id: str, timeout: int = 300) -> str:
    url = f"https://api.wavespeed.ai/api/v3/predictions/{task_id}/result"
    headers = {"Authorization": f"Bearer {api_key}"}
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        body = r.json()
        payload = body.get("data", body)
        status = payload.get("status")
        if status == "completed":
            outputs = payload.get("outputs") or payload.get("output") or []
            if isinstance(outputs, str):
                return outputs
            if outputs:
                return outputs[0]
            raise RuntimeError(f"completed but no outputs: {body}")
        if status == "failed":
            raise RuntimeError(f"task failed: {body}")
        time.sleep(3)
    raise TimeoutError(f"task {task_id} did not complete in {timeout}s")


def download(url: str, dest: Path) -> None:
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    dest.write_bytes(r.content)


def main() -> None:
    # If slugs are passed on the command line, generate only those. Otherwise all 16.
    filter_slugs = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    cities = [c for c in CITIES if not filter_slugs or c[0] in filter_slugs]
    if not cities:
        sys.exit(f"no cities matched {filter_slugs}. valid slugs: {[c[0] for c in CITIES]}")

    api_key = get_api_key()
    errors: list[tuple[str, str]] = []
    for slug, subject, gender in cities:
        dest = OUT / f"{slug}.jpg"
        if dest.exists() and not filter_slugs:
            print(f"· {slug}: already exists ({dest.stat().st_size / 1024:.0f} KB) — skipping")
            continue
        traveler = TRAVELER_F if gender == "f" else TRAVELER_M
        prompt = f"{subject} {traveler}{STYLE_BASE}"
        try:
            print(f"→ {slug}: submitting…")
            task = submit(api_key, prompt)
            print(f"  task {task}; polling…")
            out_url = poll(api_key, task, timeout=360)
            download(out_url, dest)
            print(f"✓ {slug}: saved {dest.name} ({dest.stat().st_size / 1024:.0f} KB)")
        except Exception as e:
            print(f"✗ {slug}: {e}", file=sys.stderr)
            errors.append((slug, str(e)))
    if errors:
        print("\nerrors:")
        for s, e in errors:
            print(f"  {s}: {e}")
        sys.exit(1)
    print(f"\ndone. images in {OUT}")


if __name__ == "__main__":
    main()
