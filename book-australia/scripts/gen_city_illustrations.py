#!/usr/bin/env python3
"""
Generate 14 per-city cover illustrations for the Australia book via Wavespeed
(Nano Banana Pro).

Style brief — must match the Japan book's 9 city covers:
  - Flat vector illustration, mid-century travel-book poster aesthetic
  - Warm cream / saffron / burgundy / deep-purple / muted teal palette,
    golden-hour light
  - Tourist figure in deep-burgundy jacket with small backpack, stylised
  - 1:1 aspect, 2K resolution, JPEG

Output: book-australia/assets/cities/<slug>.jpg

Usage:
    python3 book-australia/scripts/gen_city_illustrations.py              # all 14 cities
    python3 book-australia/scripts/gen_city_illustrations.py sydney       # just sydney
    python3 book-australia/scripts/gen_city_illustrations.py sydney perth # multiple specific cities
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
        "sydney",
        "Sydney Opera House sails lit warm white at dusk on the harbor, the steel arch of the "
        "Sydney Harbour Bridge crossing the deep turquoise water in the middle ground, "
        "a green-and-yellow ferry crossing toward Circular Quay.",
        "m",
    ),
    (
        "melbourne",
        "The yellow clock tower facade of Flinders Street Station at the corner of Swanston and "
        "Flinders, a green W-class tram clattering past in the foreground, warm-cream Edwardian "
        "stonework against a deep-purple evening sky.",
        "f",
    ),
    (
        "brisbane",
        "The steel cantilever truss of the Story Bridge spanning the Brisbane River at golden hour, "
        "the South Bank Wheel of Brisbane glowing amber in the middle distance, jacaranda trees in "
        "lavender bloom on the riverbank.",
        "m",
    ),
    (
        "perth",
        "The Perth city skyline on the north bank of the Swan River seen from Kings Park at sunset, "
        "the Swan Bell Tower spire catching the last light, a stylised black swan gliding across the "
        "burgundy-tinged water.",
        "f",
    ),
    (
        "adelaide",
        "Glenelg's pier and the historic seaside tram terminus, warm-cream colonial sandstone facades "
        "lining the foreshore, deep turquoise Gulf St Vincent water with a single sailboat offshore "
        "at late afternoon.",
        "m",
    ),
    (
        "hobart",
        "Salamanca Place's row of warm sandstone Georgian warehouses with awnings, a glimpse of the "
        "Derwent River at the end of the street, Mount Wellington's bulk rising behind in deep "
        "burgundy shadow against a saffron sky.",
        "f",
    ),
    (
        "darwin",
        "Mindil Beach at sunset with Darwin's silhouetted frangipani palms in the foreground, the "
        "deep-orange tropical sky melting into the Timor Sea, a single dragon-prowed Indonesian "
        "fishing boat anchored offshore.",
        "m",
    ),
    (
        "canberra",
        "Australia's Parliament House on Capital Hill with its iconic flagpole spire above the "
        "lawns, Lake Burley Griffin's Captain Cook Memorial Jet fountain rising on the water in the "
        "middle distance, Brindabella Range in the background haze.",
        "f",
    ),
    (
        "cairns",
        "The Cairns Esplanade Lagoon's curved saltwater pool with the silhouette of the Great "
        "Barrier Reef catamaran fleet at the marina in the middle distance, tropical palms and "
        "frangipani framing the foreground, deep turquoise Trinity Bay beyond.",
        "m",
    ),
    (
        "gold-coast",
        "The high-rise crescent of Surfers Paradise rising directly behind a long white-sand beach, "
        "the Q1 tower's needle spire catching the last sun, three small surfers paddling out into "
        "the turquoise Pacific in the foreground.",
        "f",
    ),
    (
        "byron-bay",
        "Cape Byron Lighthouse white-painted on the easternmost headland of mainland Australia at "
        "sunset, deep-burgundy basalt cliffs falling to the turquoise Pacific below, a single "
        "humpback whale's tail breaching offshore.",
        "m",
    ),
    (
        "alice-springs",
        "Uluru/Ayers Rock at sunset glowing deep burgundy-orange against the spinifex-dotted red-"
        "earth Outback plain, the smaller Kata Tjuta domes silhouetted on the horizon, a deep-"
        "purple desert sky overhead.",
        "f",
    ),
    (
        "whitsundays",
        "The pure-white silica sand swirl of Whitehaven Beach meeting the turquoise water of "
        "Hill Inlet from a stylised aerial three-quarter view, a single white sailing yacht "
        "anchored offshore, lush green Whitsunday island headlands framing the cove.",
        "m",
    ),
    (
        "port-douglas",
        "Four Mile Beach's long curve of golden sand with Daintree-rainforest-clad headlands at "
        "the far end, a Great Barrier Reef catamaran moored at Port Douglas marina in the middle "
        "distance, palms framing the foreground at golden hour.",
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
