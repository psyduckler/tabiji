#!/usr/bin/env python3
"""
Generate 16 per-city cover illustrations for the France book via Wavespeed
(Nano Banana Pro).

Style: flat vector mid-century travel-poster, same palette as prior volumes.

Output: book-france/assets/cities/<slug>.jpg

Usage:
    python3 book-france/scripts/gen_city_illustrations.py
    python3 book-france/scripts/gen_city_illustrations.py paris nice
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import requests


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

CITIES: list[tuple[str, str, str]] = [
    (
        "paris",
        "The Eiffel Tower seen from across the Trocadéro plaza at golden hour, "
        "its iron lattice silhouette glowing warm saffron against a dusty-purple "
        "twilight sky, a Haussmann-era stone balustrade in the foreground, the "
        "Seine just visible curving past the Champ de Mars in the middle distance, "
        "a few stylised plane trees framing the view.",
        "f",
    ),
    (
        "nice",
        "The Promenade des Anglais curving along the Baie des Anges at sunset, "
        "the pebble beach and turquoise Mediterranean to one side, the "
        "pastel-painted Belle Époque facades of the Negresco-style hotels along "
        "the promenade, a line of palm trees, warm Côte d'Azur peach-and-purple "
        "sky, the Castle Hill silhouetted at the eastern end of the bay.",
        "m",
    ),
    (
        "cannes",
        "The Croisette palm-lined promenade at sunset with the Palais des "
        "Festivals visible at one end, a line of stylised yachts moored along "
        "the Vieux Port, the wedding-cake silhouette of the Carlton Hotel rising "
        "above the boulevard, warm peach and saffron sky, the Mediterranean "
        "lapping the sand-and-pebble beach in the foreground.",
        "f",
    ),
    (
        "st-tropez",
        "The old harbor of Saint-Tropez at golden hour with the campanile of "
        "Notre-Dame de l'Assomption rising above the pastel quayside houses in "
        "ochre, salmon, and faded rose, a row of varnished wooden fishing boats "
        "(pointus) and one or two yachts in the foreground, warm Provençal sun, "
        "a sweep of pink bougainvillea climbing a stone wall.",
        "m",
    ),
    (
        "marseille",
        "The Vieux-Port of Marseille at late afternoon with the Notre-Dame de "
        "la Garde basilica crowning the hill above, a forest of small white "
        "fishing-boat masts in the harbor below, the ochre-and-cream facades of "
        "the quay buildings catching warm Mediterranean light, the Fort "
        "Saint-Jean stone silhouette to one side, a stylised sweep of dusty-blue "
        "sea behind.",
        "f",
    ),
    (
        "avignon",
        "The Pont Saint-Bénézet (the famous truncated Pont d'Avignon) reaching "
        "out into the Rhône with its four surviving arches, the massive crenellated "
        "ramparts of the Palais des Papes rising on the hill behind in honey-coloured "
        "stone, warm Provençal late-afternoon light, the Rhône flowing past in "
        "muted teal, a few cypresses framing the foreground.",
        "m",
    ),
    (
        "montpellier",
        "The Place de la Comédie at golden hour with the Three Graces fountain "
        "in the foreground and the curved 19th-century facade of the Opéra Comédie "
        "rising at the far end of the egg-shaped square, stone-paved plaza, a few "
        "plane trees in dusty teal, warm Languedoc afternoon light, the Esplanade "
        "Charles-de-Gaulle stretching into the distance.",
        "f",
    ),
    (
        "toulouse",
        "The pink-brick facade of the Capitole de Toulouse glowing warm rose at "
        "golden hour above the great cobbled Place du Capitole, the Garonne river "
        "curving past in the middle distance with the dome of the Hôpital de la "
        "Grave silhouetted on the far bank, a few stylised plane trees, warm "
        "Languedoc southern light, a Toulouse rugby motif barely suggested.",
        "m",
    ),
    (
        "lyon",
        "The Saône river curving through Lyon at golden hour with the Basilique "
        "Notre-Dame de Fourvière crowning the hill above the Vieux Lyon district, "
        "the pastel facades of the Renaissance old town along the riverbank in "
        "ochre and cream, a stone bridge spanning the river in the foreground, "
        "warm Rhône-Alpes late-afternoon light.",
        "f",
    ),
    (
        "chamonix",
        "The summit of Mont Blanc and the Aiguille du Midi rising above the "
        "Chamonix valley at golden hour, the Alpine peaks dusted with snow in "
        "warm peach and dusty purple light, a cluster of chalet rooftops in the "
        "valley below with steep tiled roofs, a few stylised pine trees, the "
        "Arve river just visible flowing through the village.",
        "m",
    ),
    (
        "annecy",
        "The Palais de l'Île standing on its boat-shaped islet in the middle of "
        "the Thiou canal in Annecy, the pastel-painted arcaded houses of the old "
        "town flanking the canal in faded rose and ochre, Lake Annecy and the "
        "surrounding peaks visible in the background, warm Alpine afternoon light, "
        "a few flower boxes in pink and saffron along the bridges.",
        "f",
    ),
    (
        "bordeaux",
        "The Place de la Bourse at golden hour with the 18th-century stone "
        "facade reflected in the Miroir d'eau (mirror pool) in the foreground, "
        "honey-coloured limestone buildings, the Garonne river just visible to "
        "one side, a few stylised plane trees, warm late-afternoon Aquitaine "
        "light, a tram quietly suggested in the middle distance.",
        "m",
    ),
    (
        "biarritz",
        "The Hôtel du Palais (a grand pink-and-cream Belle Époque palace) on "
        "its headland above the Grande Plage at sunset, the Bay of Biscay rolling "
        "in long Atlantic swells, a couple of surfers silhouetted on the wave, "
        "the Phare de Biarritz lighthouse just visible on the rocky point, warm "
        "Basque coast peach-and-saffron sky.",
        "f",
    ),
    (
        "strasbourg",
        "The pink-sandstone spire of the Cathédrale Notre-Dame de Strasbourg "
        "rising above the half-timbered houses of the Petite France quarter at "
        "golden hour, the Ill river canal in the foreground with a low covered "
        "stone bridge, the half-timbered Alsatian houses with steep tiled roofs "
        "and overflowing flower boxes, warm Rhine-Valley late-afternoon light.",
        "m",
    ),
    (
        "colmar",
        "The half-timbered houses of the Petite Venise quarter of Colmar lining "
        "the narrow Lauch canal at golden hour, painted in pastel ochre, salmon, "
        "and dusty teal, flower boxes overflowing with red geraniums, a single "
        "small flat-bottomed boat moored at a stone landing, warm Alsatian "
        "afternoon light filtering between the steep tiled roofs.",
        "f",
    ),
    (
        "mont-saint-michel",
        "The abbey-island silhouette of Mont Saint-Michel rising from the wet "
        "sand of the tidal flats at dawn, the spire of the abbey cathedral "
        "catching the first warm peach light, a thin mirror of receding tide "
        "reflecting the island in the foreground, the long Norman causeway just "
        "visible, dusty purple distant horizon, a single tiny figure walking "
        "the flats for scale.",
        "m",
    ),
]


def get_api_key() -> str:
    key = os.environ.get("WAVESPEED_API_KEY")
    if key:
        return key.strip()
    result = subprocess.run(
        ["security", "find-generic-password", "-s", "wavespeed-api-key", "-w"],
        capture_output=True, text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        sys.exit("could not read WAVESPEED_API_KEY from keychain or env")
    return result.stdout.strip()


def submit(api_key: str, prompt: str) -> str:
    url = "https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image"
    r = requests.post(url, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }, json={
        "prompt": prompt,
        "aspect_ratio": "1:1",
        "resolution": "2k",
        "output_format": "jpeg",
    }, timeout=60)
    r.raise_for_status()
    data = r.json()
    if "data" in data and "id" in data["data"]:
        return data["data"]["id"]
    if "id" in data:
        return data["id"]
    raise RuntimeError(f"unexpected submit response: {data}")


def poll(api_key: str, task_id: str, timeout: int = 360) -> str:
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
    filter_slugs = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    cities = [c for c in CITIES if not filter_slugs or c[0] in filter_slugs]
    if not cities:
        sys.exit(f"no cities matched {filter_slugs}")

    api_key = get_api_key()
    errors = []
    for slug, subject, gender in cities:
        dest = OUT / f"{slug}.jpg"
        if dest.exists() and not filter_slugs:
            print(f"· {slug}: exists — skipping")
            continue
        traveler = TRAVELER_F if gender == "f" else TRAVELER_M
        prompt = f"{subject} {traveler}{STYLE_BASE}"
        try:
            print(f"→ {slug}: submitting…")
            task = submit(api_key, prompt)
            out_url = poll(api_key, task, timeout=360)
            download(out_url, dest)
            print(f"✓ {slug}: saved ({dest.stat().st_size / 1024:.0f} KB)")
        except Exception as e:
            print(f"✗ {slug}: {e}", file=sys.stderr)
            errors.append((slug, str(e)))
    if errors:
        for s, e in errors:
            print(f"  {s}: {e}")
        sys.exit(1)
    print(f"\ndone. images in {OUT}")


if __name__ == "__main__":
    main()
