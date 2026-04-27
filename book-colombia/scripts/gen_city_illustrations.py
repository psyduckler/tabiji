#!/usr/bin/env python3
"""
Generate 10 per-city cover illustrations for the Colombia book via Wavespeed
(Nano Banana Pro).

Style brief — must match the Japan, Italy, France, Thailand, Spain, Argentina,
and Australia volumes:
  - Flat vector illustration, mid-century travel-book poster aesthetic
  - Warm cream / saffron / burgundy / deep-purple / muted teal palette,
    golden-hour light
  - Tourist figure in deep-burgundy jacket with small backpack, stylised
  - 1:1 aspect, 2K resolution, JPEG

Output: book-colombia/assets/cities/<slug>.jpg

Usage:
    python3 book-colombia/scripts/gen_city_illustrations.py                  # all 10 cities
    python3 book-colombia/scripts/gen_city_illustrations.py bogota           # just Bogotá
    python3 book-colombia/scripts/gen_city_illustrations.py bogota medellin  # two cities
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

# (slug, subject, gender) — in book reading order; alternating gender.
CITIES: list[tuple[str, str, str]] = [
    (
        "bogota",
        "La Candelaria's painted colonial balconies in Bogotá at golden hour, "
        "Cerro de Monserrate rising in the background with its hilltop chapel "
        "silhouetted against an Andean dusty-purple sky, cobblestone streets "
        "of the centro histórico catching warm saffron light, a single yellow "
        "Bogotá taxi parked in the middle distance.",
        "f",
    ),
    (
        "medellin",
        "The Comuna 13 hillside escalators rising through brick-red barrios of "
        "Medellín at golden hour, the Aburrá Valley stretching below filled "
        "with warm haze, painted street art on retaining walls in saturated "
        "saffron and teal, palm trees in the middle distance, the Andean "
        "ridges in dusty-purple beyond.",
        "m",
    ),
    (
        "cartagena",
        "The Walled City of Cartagena at golden hour, bougainvillea-draped "
        "colonial balconies in deep burgundy and saffron above Plaza Santo "
        "Domingo, the cathedral bell tower in the middle distance, the "
        "Caribbean sea visible beyond the city walls in muted teal, warm "
        "Caribbean evening light.",
        "f",
    ),
    (
        "cali",
        "The Cristo Rey statue rising above the city of Cali at golden hour, "
        "the Río Cali winding through the centro with palm-lined San Antonio "
        "rooftops, salsa club neon signs glowing in the middle distance, "
        "warm tropical Andean light, the Farallones de Cali ridges in "
        "dusty-purple silhouette.",
        "m",
    ),
    (
        "santa-marta",
        "The colonial cathedral of Santa Marta in the foreground at golden "
        "hour, the Sierra Nevada de Santa Marta rising behind in saturated "
        "deep-purple silhouette, palm-lined Rodadero beach catching warm "
        "Caribbean light, fishing boats in the middle distance, a saffron "
        "sky over the Caribbean.",
        "f",
    ),
    (
        "guatape",
        "La Piedra del Peñol monolith rising above the multi-fingered "
        "Embalse del Peñol-Guatapé reservoir at golden hour, the white "
        "concrete staircase visible up the granite face, the painted "
        "zócalo houses of Guatapé pueblo in the foreground catching warm "
        "saffron light, deep-teal reservoir water reflecting the dusty-"
        "purple Antioquian sky.",
        "m",
    ),
    (
        "salento",
        "The Cocora Valley above Salento at golden hour, towering wax-palm "
        "silhouettes of Ceroxylon quindiuense rising 60 metres above a "
        "rolling green coffee-axis hillside, warm saffron light raking "
        "across the bosque de niebla, the painted bahareque facades of "
        "Salento pueblo in the middle distance, dusty-purple Andean "
        "ridges beyond.",
        "f",
    ),
    (
        "tayrona",
        "Cabo San Juan's twin coves in Parque Nacional Tayrona at golden "
        "hour, granite boulders meeting deep-teal Caribbean water, jungle "
        "palms framing the cove, the Sierra Nevada de Santa Marta rising "
        "behind in dusty-purple silhouette, warm Caribbean light catching "
        "the white sand and the thatched lookout point on the rocks.",
        "m",
    ),
    (
        "san-andres",
        "The seven-color Caribbean shallows around Johnny Cay near San "
        "Andrés at golden hour, gradient bands of muted teal and turquoise "
        "stretching to the horizon, palm-lined white-sand beach in the "
        "foreground, a single wooden boat moored in the shallows, warm "
        "Caribbean light, a saffron sky over the Seaflower reef.",
        "f",
    ),
    (
        "villa-de-leyva",
        "Plaza Mayor in Villa de Leyva at golden hour — the largest "
        "cobblestoned plaza in the Americas, ringed by whitewashed "
        "colonial facades catching warm saffron light, the Iglesia "
        "Parroquial bell tower at the eastern end, the Boyacá altiplano "
        "stretching beyond in dusty-purple, a high-altitude Andean sky.",
        "m",
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
