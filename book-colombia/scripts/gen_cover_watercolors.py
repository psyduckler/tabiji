#!/usr/bin/env python3
"""Generate the front and back cover watercolor backgrounds for the Colombia book.

Uses the locked Macondo / magical-realism watercolor style from
scripts/comic-pipeline/styles.py, but as a single full-bleed scene (not the
4-panel comic grid). Matches the SVG comments:
  - front.jpg: Bogotá paseo-millonario scene (Harry × Bogotá)
  - back.jpg:  Cartagena walled-city rose-seller scene

Output: book-colombia/assets/svg/front.jpg and back.jpg (referenced by the SVG)

Usage:
    python3 book-colombia/scripts/gen_cover_watercolors.py
    python3 book-colombia/scripts/gen_cover_watercolors.py front
    python3 book-colombia/scripts/gen_cover_watercolors.py back
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
OUT = BOOK / "assets" / "svg"
OUT.mkdir(parents=True, exist_ok=True)

MACONDO_STYLE = (
    "Painted in the dreamlike magical-realism watercolor style evoking Gabriel "
    "García Márquez's 'Macondo' and the Caribbean-coastal Colombian literary "
    "imagination — delicate ink outlines with lush layered watercolor washes in "
    "a saturated tropical palette of papaya orange, Caribbean teal, mango yellow, "
    "hibiscus pink, and deep jungle green, soft blooming pigment edges, expressive "
    "dreamy faces, hints of butterflies and tropical foliage at scene edges, "
    "Macondo-era mid-20th-century nostalgia, literary storybook sensibility, "
    "warm humid Caribbean atmosphere. A single full-bleed illustrated scene "
    "(NOT a comic page, NO panels, NO grid, NO speech bubbles, NO text, "
    "NO words, NO numbers, NO logos, NO watermark). "
    "Portrait composition with strong vertical depth, painterly brushwork."
)

SCENES: dict[str, str] = {
    "front": (
        "A Bogotá paseo-millonario taxi-kidnapping scene at dusk in La Candelaria — "
        "a yellow Bogotá street taxi parked at a dim corner under colonial balconies "
        "with the silhouette of Cerro Monserrate rising above the painted facades, "
        "warm sodium streetlight glow, an older male traveler in a deep-burgundy "
        "jacket standing uncertainly beside the taxi while two figures emerge from "
        "the shadows of the next doorway, the moment of recognition just before the "
        "trap closes. Andean highland evening light, the misty cordillera behind "
        "the city. "
    ),
    "back": (
        "A Cartagena walled-city rose-seller scene at golden hour on Plaza Santo "
        "Domingo — a young Afro-Colombian woman in a colorful palenquera dress "
        "with a wide basket of red and pink roses leaning over an outdoor "
        "restaurant table where two seated travelers look up uncertainly, the "
        "Botero reclining-bronze sculpture in soft silhouette behind, "
        "bougainvillea-draped colonial balconies above, warm Caribbean afternoon "
        "light bouncing off pastel walls, the cathedral bell tower in the middle "
        "distance. "
    ),
}


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
            # 9:16 is the closest portrait ratio to the SVG's 5:8 viewbox; the
            # SVG uses preserveAspectRatio="xMidYMid slice" so the image will
            # be center-cropped to fit anyway.
            "aspect_ratio": "9:16",
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
    targets = sys.argv[1:] or list(SCENES.keys())
    invalid = [t for t in targets if t not in SCENES]
    if invalid:
        sys.exit(f"unknown target(s): {invalid}. valid: {list(SCENES.keys())}")

    api_key = get_api_key()
    for name in targets:
        dest = OUT / f"{name}.jpg"
        prompt = f"{SCENES[name]} {MACONDO_STYLE}"
        print(f"→ {name}: submitting…")
        task = submit(api_key, prompt)
        print(f"  task {task}; polling…")
        out_url = poll(api_key, task, timeout=420)
        download(out_url, dest)
        print(f"✓ {name}: saved {dest.name} ({dest.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
