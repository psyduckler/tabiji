#!/usr/bin/env python3
"""
Generate 9 per-city cover illustrations via Wavespeed (Nano Banana Pro).

Style brief — must match the existing 60 scam illustrations:
  - Flat vector illustration, mid-century travel-book poster aesthetic
  - Warm cream / saffron / burgundy / deep-purple palette, golden-hour light
  - Tourist figure in deep-burgundy jacket with small backpack, stylised
  - 1:1 aspect, 2K resolution, JPEG

Output: book/assets/cities/<slug>.jpg
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

# (slug, subject, gender) — gender: "m" or "f"
CITIES: list[tuple[str, str, str]] = [
    (
        "tokyo",
        "Nighttime Shibuya crossing skyline with neon signs glowing warmly, "
        "iconic Tokyo Tower in the distance, crowded scramble below.",
        "m",
    ),
    (
        "kyoto",
        "Fushimi Inari torii gate tunnel on a stone path, red-orange gates "
        "receding into a forested hillside, lanterns, dusk light.",
        "f",
    ),
    (
        "osaka",
        "Dotonbori canal at golden hour with the iconic Glico running-man "
        "sign silhouette, bright signboards, bridge, reflections on water.",
        "m",
    ),
    (
        "sapporo",
        "Sapporo TV Tower rising above Odori Park in late autumn, yellow "
        "ginkgo trees, wide boulevard, soft snow flurries in the sky.",
        "f",
    ),
    (
        "fukuoka",
        "Hakata yatai food-stall row along a canal at dusk, paper lanterns, "
        "steam rising from a tonkotsu ramen cart, warm glow.",
        "m",
    ),
    (
        "hiroshima",
        "Itsukushima Shrine's floating torii gate at high tide, calm sea, "
        "Miyajima hillside behind, soft pink-orange sunset sky.",
        "m",
    ),
    (
        "nara",
        "Todai-ji Great Buddha Hall with wooden temple facade, tame deer "
        "grazing on a grassy path in the foreground, lantern lines.",
        "f",
    ),
    (
        "okinawa",
        "Shuri Castle's vermilion gate against turquoise sea and palm trees, "
        "Naha skyline in distance, warm Ryukyuan coastal light.",
        "m",
    ),
    (
        "yokohama",
        "Minato Mirai waterfront at dusk: Landmark Tower, Cosmo Clock Ferris "
        "wheel glowing, Yokohama Bay Bridge, reflections on the harbor.",
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
    # Wavespeed returns { "data": { "id": ..., "status": ... } } or similar
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
    api_key = get_api_key()
    errors: list[tuple[str, str]] = []
    for slug, subject, gender in CITIES:
        dest = OUT / f"{slug}.jpg"
        if dest.exists():
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
