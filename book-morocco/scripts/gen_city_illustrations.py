#!/usr/bin/env python3
"""
Generate 10 per-city cover illustrations for the Morocco book via Wavespeed
(Nano Banana Pro).

Style: flat vector mid-century travel-poster, same palette as prior volumes.

Output: book-morocco/assets/cities/<slug>.jpg

Usage:
    python3 book-morocco/scripts/gen_city_illustrations.py
    python3 book-morocco/scripts/gen_city_illustrations.py marrakech fez
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
        "marrakech",
        "Djemaa el-Fna in Marrakech at dusk — the sprawling stone-paved square "
        "at the heart of the medina with the tall brick minaret of the Koutoubia "
        "Mosque rising in the middle distance, soft smoke drifting from a few "
        "food stalls in the foreground, ochre walls of the medina to one side, "
        "the Atlas Mountains a faint silhouette on the far horizon, warm "
        "saffron-to-dusty-purple twilight sky.",
        "f",
    ),
    (
        "fez",
        "The leather tanneries of Chouara in Fez seen from a rooftop terrace "
        "at golden hour — circular stone vats filled with deep red, "
        "mustard-yellow, and indigo dyes laid out in a honeycomb pattern, the "
        "dense terracotta-and-cream rooftops of Fez al-Bali medina cascading "
        "away behind, the green-tiled minaret of the Qarawiyyin Mosque rising "
        "in the distance, warm late-afternoon light.",
        "m",
    ),
    (
        "casablanca",
        "The Hassan II Mosque in Casablanca on its Atlantic-facing terrace at "
        "sunset, the world's tallest minaret rising above the carved white-stone "
        "walls, the Atlantic Ocean breaking against rocks below, the modern "
        "Casablanca skyline silhouetted to one side, warm peach-and-saffron "
        "evening sky, a faint hint of fishing boats in the harbor.",
        "f",
    ),
    (
        "rabat",
        "The Kasbah des Oudayas in Rabat at golden hour — white-and-blue "
        "painted houses lining narrow lanes inside ochre stone fortress walls, "
        "the kasbah perched above the Bouregreg river estuary, fishing boats "
        "on the water below, the city of Salé visible across the river, the "
        "Atlantic stretching out to one side, warm late-afternoon light.",
        "m",
    ),
    (
        "tangier",
        "The Bay of Tangier seen from the kasbah at sunset — the curving "
        "white-painted medina cascading down the hillside to the harbor, the "
        "Strait of Gibraltar where the Mediterranean meets the Atlantic, a "
        "faint silhouette of the Spanish coast on the horizon, ferries moving "
        "across the bay, dusty-purple-to-saffron sky, palm trees in the "
        "foreground.",
        "f",
    ),
    (
        "chefchaouen",
        "The blue-painted alleys of the Chefchaouen medina at golden hour — "
        "every wall, door, and step painted pale-blue and indigo, hanging "
        "baskets of red geraniums at the eaves, the green flanks of the Rif "
        "Mountains rising directly behind the town, warm afternoon light "
        "spilling between the buildings.",
        "m",
    ),
    (
        "essaouira",
        "The white-and-blue medina walls of Essaouira at sunset — the long "
        "Atlantic-facing ramparts with their bronze cannons, a line of small "
        "blue-hulled fishing boats in the harbor below, seagulls in flight "
        "overhead, the medina's red-tile rooftops cascading toward the sea, "
        "warm golden-hour light glancing off blue-painted shutters.",
        "f",
    ),
    (
        "agadir",
        "The crescent of Agadir Bay at golden hour — the long curving beach "
        "lined with palms and white-walled apartment buildings, Atlantic surf "
        "rolling in, the ruins of the Agadir Oufella kasbah visible on the hill "
        "above, warm late-afternoon light, a few small fishing boats in the "
        "near-shore distance.",
        "m",
    ),
    (
        "merzouga",
        "The Erg Chebbi dunes outside Merzouga at sunrise — towering ochre and "
        "cinnamon-colored sand dunes rising hundreds of feet, a single line of "
        "camels and a Berber guide silhouetted against the sky on a dune crest, "
        "the village of Merzouga a distant low line of buildings far below, "
        "warm coral-pink sunrise sky.",
        "f",
    ),
    (
        "ouarzazate",
        "The Aït Benhaddou ksar near Ouarzazate at golden hour — the iconic "
        "terracotta-red mud-brick fortified village rising from the dry riverbed "
        "of the Ounila with its stacked towers and crenellated walls, the High "
        "Atlas peaks faint in the background, a cluster of palm trees along "
        "the riverbed, warm late-afternoon desert light.",
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
