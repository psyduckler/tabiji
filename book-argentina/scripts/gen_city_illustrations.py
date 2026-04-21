#!/usr/bin/env python3
"""
Generate 11 per-city cover illustrations for the Argentina book via Wavespeed
(Nano Banana Pro).

Style brief — must match the Japan, Italy, France, Thailand, and Spain volumes:
  - Flat vector illustration, mid-century travel-book poster aesthetic
  - Warm cream / saffron / burgundy / deep-purple / muted teal palette,
    golden-hour light
  - Tourist figure in deep-burgundy jacket with small backpack, stylised
  - 1:1 aspect, 2K resolution, JPEG

Output: book-argentina/assets/cities/<slug>.jpg

Usage:
    python3 book-argentina/scripts/gen_city_illustrations.py                       # all 11 cities
    python3 book-argentina/scripts/gen_city_illustrations.py buenos-aires          # just Buenos Aires
    python3 book-argentina/scripts/gen_city_illustrations.py buenos-aires salta    # two cities
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
        "buenos-aires",
        "The pink facade of the Casa Rosada above Plaza de Mayo at golden hour, "
        "the Pirámide de Mayo in the foreground, warm porteño evening light "
        "catching the balcony balustrades, the Cabildo's colonial arcades in "
        "soft silhouette to the side.",
        "f",
    ),
    (
        "cordoba-argentina",
        "The Manzana Jesuítica of Córdoba at golden hour, the Jesuit Iglesia de "
        "la Compañía de Jesús with its cedar-shingled dome rising above Plaza "
        "San Martín, warm sierras light glowing on colonial stucco walls, the "
        "Cathedral's twin bell towers in the middle distance.",
        "m",
    ),
    (
        "rosario",
        "The Monumento Nacional a la Bandera rising above the Paraná river at "
        "golden hour, the great stone prow of the monument catching warm light, "
        "the slow brown water of the Paraná stretching to a dusty-purple "
        "horizon, sailboats in soft silhouette.",
        "f",
    ),
    (
        "mendoza",
        "Vineyard rows in the Uco Valley of Mendoza at golden hour, the "
        "snow-capped Andes Cordillera rising behind, warm saffron light raking "
        "across trellised Malbec vines, a single low bodega building in the "
        "middle distance, dusty-purple altitude haze.",
        "m",
    ),
    (
        "salta",
        "The Cerro San Bernardo above the colonial cathedral of Salta at "
        "golden hour, the cathedral's pink Andalusian facade glowing saffron, "
        "the Siete Colores mountain ridgeline in the middle distance, warm "
        "northwestern Argentine light and a single palo borracho tree in the "
        "foreground.",
        "f",
    ),
    (
        "bariloche",
        "Lake Nahuel Huapi and the alpine peaks of Cerro Catedral at golden "
        "hour, the dark blue Patagonian lake reflecting warm light, the iconic "
        "Swiss-style stone Centro Cívico belltower in the foreground, "
        "snow-capped Andes in the distance.",
        "m",
    ),
    (
        "el-calafate",
        "The cobalt ice face of Perito Moreno Glacier at golden hour, deep blue "
        "crevasses catching warm light, a narrow stretch of Lago Argentino "
        "between the glacier front and the Patagonian forest, a lone viewing "
        "platform in soft silhouette.",
        "f",
    ),
    (
        "el-chalten",
        "The jagged granite spires of Monte Fitz Roy catching warm saffron "
        "alpenglow at golden hour, a Patagonian meadow with pale grasses in "
        "the foreground, a single hiking trail winding toward the base of the "
        "massif, dusty-purple sky.",
        "m",
    ),
    (
        "ushuaia",
        "The Les Eclaireurs lighthouse at the mouth of the Beagle Channel "
        "above dark water at golden hour, snow-capped Andes fuegia in the "
        "background, a single black-and-white lighthouse tower against a warm "
        "peach sky, the Atlantic stretching to a dusty-purple southern horizon.",
        "f",
    ),
    (
        "puerto-iguazu",
        "The Garganta del Diablo at Iguazú Falls at golden hour, a thundering "
        "horseshoe of water cascading into mist, lush subtropical rainforest "
        "in saturated green, warm saffron light catching the spray, a rainbow "
        "arcing across the falls.",
        "m",
    ),
    (
        "tigre",
        "Wooden lanchas tied up at the Estación Fluvial of Tigre at golden "
        "hour, the brown Paraná Delta water in the foreground, an ornate "
        "Belle-Époque riverside casino facade in the middle distance, a soft "
        "rose sky over the Buenos Aires delta.",
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
