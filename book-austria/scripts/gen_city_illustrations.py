#!/usr/bin/env python3
"""
Generate 9 per-city chapter-opener illustrations for the Austria book via
Wavespeed (Nano Banana Pro).

Style brief — the SHARED Tabiji series poster style (NOT the country's locked
Sempé comic style used for the per-scam comics):
  - Flat vector illustration, mid-century travel-book poster aesthetic
  - Warm cream / saffron / burgundy / deep-purple / muted teal palette,
    golden-hour light
  - Tourist figure in deep-burgundy jacket with small backpack, stylised
  - 1:1 aspect, 2K resolution, JPEG

Output: book-austria/assets/cities/<slug>.jpg

Usage:
    python3 book-austria/scripts/gen_city_illustrations.py                # all 9
    python3 book-austria/scripts/gen_city_illustrations.py vienna         # just vienna
    python3 book-austria/scripts/gen_city_illustrations.py vienna graz    # multiple specific cities
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
        "vienna",
        "The Gothic spire of St. Stephen's Cathedral (Stephansdom) rising above the warm-cream "
        "rooftops of Vienna's old town, the green dome of the Hofburg in the middle distance, "
        "a horse-drawn Fiaker carriage in silhouette on the square, golden-hour light.",
        "m",
    ),
    (
        "wachau",
        "The UNESCO Wachau valley of the Danube, the blue baroque church tower of Dürnstein "
        "rising above terracotta-roofed houses, terraced vineyards climbing the hillside, "
        "the river curving below, a small cruise boat on the water at golden hour.",
        "f",
    ),
    (
        "linz",
        "The vast baroque Hauptplatz of Linz with its tall white Trinity Column, pastel facades, "
        "the Pöstlingberg church on the hill across the Danube in the distance, "
        "warm late-afternoon light over the river city.",
        "m",
    ),
    (
        "salzburg",
        "The Hohensalzburg Fortress on its hill above the baroque domes and spires of Salzburg's "
        "old town, the green Salzach river curving through the foreground, "
        "the Alps rising behind, warm golden-hour light.",
        "f",
    ),
    (
        "hallstatt",
        "The iconic Hallstatt lakeside view: pastel houses and a slender church spire stacked along "
        "the shore of the still Hallstätter See, steep forested alpine cliffs rising directly behind, "
        "a small wooden boat on the mirror-calm water, soft morning light.",
        "m",
    ),
    (
        "bad-gastein",
        "The dramatic Belle Époque grand hotels of Bad Gastein stacked up the steep gorge walls "
        "around the famous Gastein waterfall cascading through the town center, "
        "snowy alpine peaks above, warm late-day light.",
        "f",
    ),
    (
        "zell-am-see",
        "The lakeside town of Zell am See on the still blue Zeller See, the snow-capped Kitzsteinhorn "
        "glacier and the Hohe Tauern peaks rising behind, a church tower on the shore, "
        "a small sailboat on the lake, golden-hour alpine light.",
        "m",
    ),
    (
        "innsbruck",
        "The colorful pastel facades of Maria-Theresien-Strasse and the gilded Golden Roof "
        "(Goldenes Dachl) in Innsbruck's old town, the dramatic snow-dusted Nordkette mountain range "
        "rising directly above the rooftops, crisp warm afternoon light.",
        "f",
    ),
    (
        "graz",
        "The Schlossberg hill above Graz crowned by the iconic Uhrturm clock tower, "
        "the sea of red-tiled rooftops of the UNESCO old town spilling below, "
        "the Mur river in the distance, warm golden-hour light.",
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
