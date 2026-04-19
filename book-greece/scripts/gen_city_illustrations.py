#!/usr/bin/env python3
"""
Generate 10 per-city cover illustrations for the Greece book via Wavespeed
(Nano Banana Pro).

Style brief — flat vector travel-poster, mid-century aesthetic:
  - Warm cream / saffron / burgundy / deep-purple / muted teal palette,
    golden-hour light
  - Tourist figure in deep-burgundy jacket with small backpack, stylised
  - 1:1 aspect, 2K resolution, JPEG

Output: book-greece/assets/cities/<slug>.jpg

Usage:
    python3 book-greece/scripts/gen_city_illustrations.py              # all 10 cities
    python3 book-greece/scripts/gen_city_illustrations.py athens       # just athens
    python3 book-greece/scripts/gen_city_illustrations.py athens santorini  # multiple
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

# (slug, subject, gender) — gender alternates
CITIES: list[tuple[str, str, str]] = [
    (
        "athens",
        "The Parthenon atop the Acropolis at golden hour, ancient marble columns "
        "silhouetted against a warm saffron sky, the rooftops of Plaka below, "
        "Athens cityscape in the haze, soft Mediterranean light.",
        "f",
    ),
    (
        "santorini",
        "The blue-domed churches of Oia perched on the caldera cliff at sunset, "
        "whitewashed cubic buildings cascading down the slope, the Aegean Sea far "
        "below, warm pink-orange sky, iconic Greek island silhouette.",
        "m",
    ),
    (
        "mykonos",
        "The famous Mykonos windmills at Little Venice at dusk, whitewashed stone "
        "windmills with wooden sails against a pink-purple sky, turquoise Aegean "
        "water, bright-colored balconies of Little Venice below.",
        "f",
    ),
    (
        "thessaloniki",
        "The White Tower of Thessaloniki on the waterfront promenade at golden hour, "
        "the Byzantine fortress silhouetted against a warm sky, palm trees along "
        "the seafront, the Thermaic Gulf in soft blue.",
        "m",
    ),
    (
        "rhodes",
        "The medieval walls of Rhodes Old Town with the Palace of the Grand Master "
        "rising above, narrow cobbled streets leading to the fortress gates, warm "
        "honey-stone at late afternoon, turquoise harbour visible beyond.",
        "f",
    ),
    (
        "corfu",
        "The Liston arcade of Corfu Town at dusk, Venetian-style arched colonnade "
        "with café tables beneath, the Old Fortress silhouetted in the distance, "
        "warm Mediterranean light on the ochre facades.",
        "m",
    ),
    (
        "heraklion",
        "The Venetian fortress of Koules guarding Heraklion harbour at golden hour, "
        "fishing boats moored in the old port, Cretan mountains visible in the "
        "distance, warm ochre stone against a soft sky.",
        "f",
    ),
    (
        "chania",
        "The Venetian Lighthouse of Chania at dusk, the horseshoe-shaped Old Harbour "
        "with pastel waterfront buildings, fishing boats moored at the quay, warm "
        "golden light reflecting on the water.",
        "m",
    ),
    (
        "paros",
        "The whitewashed cubic houses of Naoussa fishing village at sunset, blue-"
        "domed church, small fishing boats in the harbour, Cycladic architecture "
        "against a warm pink sky, bougainvillea accents.",
        "f",
    ),
    (
        "naxos",
        "The Portara — the massive marble gateway to the unfinished Temple of Apollo — "
        "silhouetted against a sunset sky on the Naxos peninsula, the Aegean Sea "
        "visible through the ancient doorway, warm golden-hour light.",
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
