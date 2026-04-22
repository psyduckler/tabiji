#!/usr/bin/env python3
"""
Generate 8 per-city cover illustrations for the Costa Rica book via Wavespeed
(Nano Banana Pro).

Style brief — match the book-costa-rica locked interior comic style:
  - 1950s Pan American Airways tropical-deco travel-poster aesthetic
  - Palette of deep turquoise Pacific, emerald jungle, volcano red-orange,
    banana yellow, tropical magenta, and warm cream
  - Single stylized solo traveler in the foreground (alternating m/f)
  - 1:1 aspect, 2K resolution, JPEG

Output: book-costa-rica/assets/cities/<slug>.jpg

Usage:
    python3 book-costa-rica/scripts/gen_city_illustrations.py                      # all 8 cities
    python3 book-costa-rica/scripts/gen_city_illustrations.py san-jose             # just san-jose
    python3 book-costa-rica/scripts/gen_city_illustrations.py san-jose liberia     # multiple
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import urllib.request
import json


HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
OUT = BOOK / "assets" / "cities"
OUT.mkdir(parents=True, exist_ok=True)

STYLE_BASE = (
    "Flat vector travel-poster illustration in the 1950s Pan American "
    "Airways tropical-deco style. Warm cream background, palette of deep "
    "turquoise Pacific, emerald jungle, volcano red-orange, banana yellow, "
    "tropical magenta, and cream. Soft golden-hour tropical light. Clean "
    "bold geometric shapes with crisp black outlines, streamlined "
    "modernist composition, visible paper-grain texture, no text, no "
    "words, no logos, no watermark. Square 1:1 composition, gentle depth, "
    "soft shadows."
)

TRAVELER_M = (
    "One stylized solo male traveler in light linen shirt and khaki "
    "shorts with a small canvas daypack, straw sun hat, seen from behind "
    "or three-quarter view, looking toward the scene. "
)

TRAVELER_F = (
    "One stylized solo female traveler in light cotton dress or linen "
    "travel shirt, woven sun hat, small canvas daypack, seen from "
    "behind or three-quarter view, looking toward the scene. "
)

# (slug, subject, gender) — reading order matches config.yaml
CITIES: list[tuple[str, str, str]] = [
    (
        "san-jose",
        "The Teatro Nacional de Costa Rica in San José at golden hour — "
        "neoclassical facade with Corinthian columns, Plaza de la Cultura "
        "in the foreground, Central Valley mountains hazy in the distance.",
        "f",
    ),
    (
        "liberia",
        "The whitewashed colonial church of Liberia (Iglesia de la Ermita "
        "La Agonía) with Guanacaste tree in the foreground, dry tropical "
        "scrub, Rincón de la Vieja volcano on the horizon.",
        "m",
    ),
    (
        "tamarindo",
        "Playa Tamarindo at sunset — golden-sand crescent, surfers on the "
        "point break, Punta Langosta in silhouette, warm tropical palette.",
        "f",
    ),
    (
        "monteverde",
        "The Monteverde cloud forest canopy with a suspended rope bridge "
        "through emerald mist, giant ficus trees, a quetzal in the canopy, "
        "cool-green tropical palette with warm cream sky.",
        "m",
    ),
    (
        "la-fortuna",
        "The perfect cone of Arenal volcano at golden hour with Catarata "
        "La Fortuna waterfall framed by jungle in the foreground, warm "
        "lava glow on the summit, deep emerald foliage.",
        "f",
    ),
    (
        "jaco",
        "Playa Jacó at sunset — long crescent beach, palm silhouettes, "
        "Avenida Pastor Díaz palm line, warm magenta and turquoise sky, "
        "Central Pacific headland in silhouette.",
        "m",
    ),
    (
        "manuel-antonio",
        "The white-sand cove of Playa Manuel Antonio framed by jungle "
        "headlands, a three-toed sloth silhouette in a cecropia tree, "
        "turquoise Pacific, small boats at anchor.",
        "f",
    ),
    (
        "puerto-viejo",
        "The palm-lined Playa Cocles on the Caribbean coast with a "
        "wooden rancho in the foreground, warm Caribbean cyan water, "
        "scarlet macaw flying across the scene, tropical jungle backdrop.",
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
    req = urllib.request.Request(
        url,
        method="POST",
        data=json.dumps({
            "prompt": prompt,
            "aspect_ratio": "1:1",
            "resolution": "2k",
            "output_format": "jpeg",
        }).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
    if "data" in data and "id" in data["data"]:
        return data["data"]["id"]
    if "id" in data:
        return data["id"]
    raise RuntimeError(f"unexpected submit response: {data}")


def poll(api_key: str, task_id: str, timeout: int = 300) -> str:
    url = f"https://api.wavespeed.ai/api/v3/predictions/{task_id}/result"
    deadline = time.time() + timeout
    while time.time() < deadline:
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}"})
        with urllib.request.urlopen(req, timeout=30) as r:
            body = json.loads(r.read())
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
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        dest.write_bytes(r.read())


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
            print(f"· {slug}: already exists ({dest.stat().st_size / 1024:.0f} KB) — skipping", flush=True)
            continue
        traveler = TRAVELER_F if gender == "f" else TRAVELER_M
        prompt = f"{subject} {traveler}{STYLE_BASE}"
        try:
            print(f"→ {slug}: submitting…", flush=True)
            task = submit(api_key, prompt)
            print(f"  task {task}; polling…", flush=True)
            out_url = poll(api_key, task, timeout=360)
            download(out_url, dest)
            print(f"✓ {slug}: saved {dest.name} ({dest.stat().st_size / 1024:.0f} KB)", flush=True)
        except Exception as e:
            print(f"✗ {slug}: {e}", file=sys.stderr, flush=True)
            errors.append((slug, str(e)))
    if errors:
        print("\nerrors:", flush=True)
        for s, e in errors:
            print(f"  {s}: {e}")
        sys.exit(1)
    print(f"\ndone. images in {OUT}", flush=True)


if __name__ == "__main__":
    main()
