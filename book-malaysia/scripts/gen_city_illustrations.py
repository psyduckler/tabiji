#!/usr/bin/env python3
"""
Generate 20 per-city cover illustrations for the Italy book via Wavespeed
(Nano Banana Pro).

Style brief — must match the Japan book's 9 city covers:
  - Flat vector illustration, mid-century travel-book poster aesthetic
  - Warm cream / saffron / burgundy / deep-purple / muted teal palette,
    golden-hour light
  - Tourist figure in deep-burgundy jacket with small backpack, stylised
  - 1:1 aspect, 2K resolution, JPEG

Output: book-italy/assets/cities/<slug>.jpg

Usage:
    python3 book-italy/scripts/gen_city_illustrations.py              # all 20 cities
    python3 book-italy/scripts/gen_city_illustrations.py rome         # just rome
    python3 book-italy/scripts/gen_city_illustrations.py rome venice  # multiple specific cities
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
        "kuala-lumpur",
        "Kuala Lumpur's skyline at golden hour - the Petronas Twin Towers rising above the KLCC park pool, the KL Tower silhouetted to the right, tropical palms in the foreground, warm saffron sky, soft evening glow on the polished glass facades, a blue-and-white TEKSI 1Malaysia pulling up to a corner.",
        "f",
    ),
    (
        "melaka",
        "Melaka's Christ Church and Stadthuys Red Square at golden hour - the vivid red-ochre Dutch colonial facade, the brick windmill at Dataran Pahlawan behind, a Hello Kitty-decorated trishaw passing under the Jonker Walk arch, river boat in background, warm evening light on cobblestone.",
        "m",
    ),
    (
        "johor-bahru",
        "Johor Bahru's Sultan Iskandar CIQ complex at dusk - the massive crossing terminal lit up, the causeway bridge crossing to Singapore visible in the foreground, KSL City Mall silhouette behind, warm twilight sky, queues of cars and buses crossing the border.",
        "m",
    ),
    (
        "genting-highlands",
        "Genting Highlands at sunset - the First World Hotel's candy-striped pink facade rising through mountain mist, SkyWorlds theme park roller coasters wrapping the hilltop, Awana SkyWay cable-car gondolas descending, pine trees in the foreground, soft amber light filtering through tropical clouds.",
        "f",
    ),
    (
        "cameron-highlands",
        "Cameron Highlands' BOH tea plantation at dawn - neat terraced rows of vibrant green tea bushes cascading down hillsides, a solitary tea-picker in a white head-wrap walking between rows, soft misty valley below, warm golden-hour sunlight breaking over the ridge, a wooden viewing platform to the right.",
        "f",
    ),
    (
        "ipoh",
        "Ipoh Old Town at golden hour - a terrace of colorful peranakan shophouses with green shutters along Jalan Sultan Yussuf, a kopitiam awning in the foreground, white-and-green limestone cliffs rising behind the town, a hand-pulled rickshaw resting at the corner, warm amber light.",
        "m",
    ),
    (
        "penang",
        "Penang's George Town UNESCO core at golden hour - a row of pastel peranakan shophouses with Chinese clan inscriptions along Armenian Street, the KOMTAR tower in the distance, a trishaw with a Hello Kitty umbrella passing in the foreground, a Zacharevic mural visible on the brick wall behind, warm evening light.",
        "f",
    ),
    (
        "langkawi",
        "Langkawi's Eagle Square at golden hour - the giant bronze reddish-brown eagle statue on its plinth, the turquoise Andaman Sea behind, the SkyBridge silhouetted on Machinchang mountain in the distance, two cable cars crossing, tropical palms in the foreground, warm sunset sky with pink-orange clouds.",
        "m",
    ),
    (
        "kuching",
        "Kuching's Sarawak River waterfront at golden hour - the golden-domed Astana (Governor's palace) across the river, the Darul Hana Bridge curving overhead, sampans (small river boats) with bamboo roofs, the Cat Museum behind the hills, warm late-afternoon light on the muddy-brown river water, tropical foliage in the foreground.",
        "f",
    ),
    (
        "kota-kinabalu",
        "Kota Kinabalu at golden hour - the jagged silhouette of Mt Kinabalu looming in the distance, the South China Sea in the foreground with silhouetted palm fronds, the city waterfront with Suria Sabah mall and City Mosque visible, warm pink-and-orange sunset sky, a small fishing boat near shore.",
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
    # If slugs are passed on the command line, generate only those. Otherwise all 20.
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
