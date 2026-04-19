#!/usr/bin/env python3
"""
Generate 16 per-city cover illustrations for the Spain book via Wavespeed
(Nano Banana Pro).

Style brief — must match the Japan, Italy, France, and Thailand volumes:
  - Flat vector illustration, mid-century travel-book poster aesthetic
  - Warm cream / saffron / burgundy / deep-purple / muted teal palette,
    golden-hour light
  - Tourist figure in deep-burgundy jacket with small backpack, stylised
  - 1:1 aspect, 2K resolution, JPEG

Output: book-spain/assets/cities/<slug>.jpg

Usage:
    python3 book-spain/scripts/gen_city_illustrations.py              # all 16 cities
    python3 book-spain/scripts/gen_city_illustrations.py madrid       # just madrid
    python3 book-spain/scripts/gen_city_illustrations.py madrid barcelona
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

# (slug, subject, gender) — in manuscript reading order; alternating gender.
CITIES: list[tuple[str, str, str]] = [
    (
        "madrid",
        "Puerta del Sol at dusk with the iconic Tío Pepe illuminated sign on a "
        "corner rooftop, the clock tower of the Real Casa de Correos in the "
        "middle distance, warm ochre cast of Spanish evening light, a gentle "
        "haze over the plaza.",
        "f",
    ),
    (
        "barcelona",
        "The unfinished spires of the Sagrada Família rising above the Eixample "
        "rooftops of Barcelona at golden hour, warm Mediterranean light, a hint "
        "of Mediterranean haze beyond, the stylised silhouette of a cypress tree "
        "in the foreground.",
        "m",
    ),
    (
        "seville",
        "The Giralda bell tower rising above the Catedral de Sevilla at golden "
        "hour, orange-tree silhouettes in the foreground plaza, warm Andalusian "
        "sun casting long ochre shadows, pastel Moorish detailing.",
        "f",
    ),
    (
        "granada-spain",
        "The Alhambra fortress-palace complex silhouetted against the "
        "snow-capped Sierra Nevada at golden hour, the red-ochre walls of the "
        "Alcazaba glowing warm against a dusty-purple sky, cypress trees in "
        "the foreground.",
        "m",
    ),
    (
        "cordoba",
        "The striped red-and-white arches of the Mezquita-Catedral of Córdoba, "
        "the Roman Bridge crossing the Guadalquivir river in the foreground, "
        "warm Andalusian afternoon light, the Torre de la Calahorra in the "
        "middle distance.",
        "f",
    ),
    (
        "malaga",
        "The Moorish Alcazaba fortress above the port of Málaga, the "
        "Mediterranean Sea stretching to a warm peach horizon, cruise ships in "
        "soft silhouette, palm trees along the promenade at sunset.",
        "m",
    ),
    (
        "valencia",
        "The futuristic white curves of the Ciudad de las Artes y las Ciencias "
        "reflected in its long pools at blue hour, clean geometric architecture, "
        "a warm late-afternoon sky shading into dusty purple, soft "
        "Mediterranean haze.",
        "f",
    ),
    (
        "bilbao",
        "The titanium curves of the Guggenheim Museum Bilbao along the Nervión "
        "river at late afternoon, reflections on the water, La Salve bridge "
        "in the background, warm Atlantic-northern light, the Maman spider "
        "sculpture visible in silhouette.",
        "m",
    ),
    (
        "san-sebastian",
        "The perfect crescent of La Concha bay at sunset, Santa Clara island "
        "in the middle of the bay, Monte Urgull rising to the right, Belle "
        "Époque hotel facades along the promenade, warm Cantabrian light.",
        "f",
    ),
    (
        "santiago-de-compostela",
        "The Baroque twin towers of the Catedral de Santiago de Compostela at "
        "golden hour, the Praza do Obradoiro plaza below with a few pilgrims "
        "with shell and staff in silhouette, warm Galician granite glowing "
        "saffron-gold.",
        "m",
    ),
    (
        "toledo",
        "The medieval walled city of Toledo seen from across the Tajo river "
        "gorge at golden hour, the Alcázar fortress crowning the skyline, the "
        "Cathedral spire visible among the ochre rooftops, a single stone "
        "bridge crossing to the city.",
        "f",
    ),
    (
        "palma-de-mallorca",
        "La Seu Cathedral of Palma de Mallorca rising above the harbor at "
        "sunset, sailboats on the Mediterranean in the foreground, warm peach "
        "and dusty-purple sky, the Tramuntana mountains softly in the "
        "distance.",
        "m",
    ),
    (
        "ibiza",
        "The walled citadel of Dalt Vila on Ibiza town rising above the "
        "harbor at twilight, pastel houses climbing the hill to the Cathedral "
        "at the top, warm Mediterranean sunset casting pink light on the "
        "white walls.",
        "f",
    ),
    (
        "tenerife",
        "Mount Teide volcano rising above a sea of clouds at golden hour, the "
        "caldera's ochre volcanic landscape in the foreground, warm Canary "
        "light, dwarf pines in stylised silhouette, a single dirt trail "
        "climbing toward the summit.",
        "m",
    ),
    (
        "gran-canaria",
        "The Maspalomas sand dunes curving toward the Atlantic at sunset, warm "
        "saffron light raking across the rippled sand, a single palm cluster "
        "at the Charca de Maspalomas lagoon, dusty-purple Atlantic horizon.",
        "f",
    ),
    (
        "lanzarote",
        "The Timanfaya volcanic badlands on Lanzarote at golden hour, ochre "
        "and black lava fields rolling to the horizon, a single low white "
        "cottage with green shutters in the middle distance, the warm Canary "
        "sun low and glowing.",
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
