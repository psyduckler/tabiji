#!/usr/bin/env python3
"""
Generate 7 per-city cover illustrations for the Egypt book via Wavespeed
(Nano Banana Pro).

Style brief — matches the Tabiji Travel Safety Series house style (Japan/Italy):
  - Flat vector illustration, mid-century travel-book poster aesthetic
  - Warm cream / saffron / sand-gold / Nile-blue / soft turquoise palette,
    golden-hour light
  - Tourist figure in deep-burgundy jacket with small backpack, stylised
  - 1:1 aspect, 2K resolution, JPEG

Output: book-egypt/assets/cities/<slug>.jpg

Usage:
    python3 book-egypt/scripts/gen_city_illustrations.py              # all 7 cities
    python3 book-egypt/scripts/gen_city_illustrations.py cairo        # just cairo
    python3 book-egypt/scripts/gen_city_illustrations.py cairo luxor  # multiple specific cities
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
    "Warm cream background, palette of saffron-gold, sand-gold, deep "
    "Nile-blue, dusty terracotta and soft turquoise. Soft golden-hour light. "
    "Clean geometric shapes, visible paper-grain texture, "
    "no text, no words, no logos, no watermark, no Arabic or hieroglyphic script. "
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
        "cairo",
        "The Giza pyramids of Khufu, Khafre, and Menkaure rising above the desert plateau "
        "with the Sphinx in the foreground, golden-hour sand-gold light, palm silhouettes.",
        "m",
    ),
    (
        "luxor",
        "The columned hypostyle hall of Karnak Temple at golden hour, massive stone pillars "
        "with carved capitals, warm sandstone tones, deep shadows between the columns, the Nile in the distance.",
        "f",
    ),
    (
        "aswan",
        "Feluccas with white triangular sails on the Nile at sunset near Elephantine Island, "
        "warm Nile-blue water, sand-gold cliffs of the West Bank, deep-orange sky.",
        "m",
    ),
    (
        "hurghada",
        "Red Sea coral reef and a dive boat anchored over turquoise water off Sahl Hasheesh, "
        "sand-gold beach in the distance, soft Egyptian Eastern Desert mountains on the horizon.",
        "f",
    ),
    (
        "sharm-el-sheikh",
        "The crescent of Naama Bay with palm-shaded promenade, turquoise reef visible just offshore, "
        "Sinai mountains rising behind in the distance at golden hour.",
        "m",
    ),
    (
        "alexandria",
        "The Qaitbay Citadel above the Eastern Harbor at golden hour, warm sandstone walls, "
        "Mediterranean blue water, fishing boats with red sails in the foreground, Alexandria corniche curving away.",
        "f",
    ),
    (
        "dahab",
        "The Blue Hole and palm-shaded shore of the Mashraba strip with the jagged Sinai mountains "
        "rising behind, deep Red Sea blue, warm afternoon light, a single bedouin tea shack.",
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
