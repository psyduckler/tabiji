#!/usr/bin/env python3
"""
Generate 12 per-city cover illustrations for the Indonesia book via Wavespeed
(Nano Banana Pro).

Style brief — matches Japan/Italy/France/Thailand/Vietnam volume city covers:
  - Flat vector illustration, mid-century travel-book poster aesthetic
  - Warm cream / saffron / burgundy / deep-purple / muted teal palette,
    golden-hour light
  - Tourist figure in deep-burgundy jacket with small backpack, stylised
  - 1:1 aspect, 2K resolution, JPEG

Output: book-indonesia/assets/cities/<slug>.jpg

Usage:
    python3 book-indonesia/scripts/gen_city_illustrations.py               # all 12
    python3 book-indonesia/scripts/gen_city_illustrations.py bali          # one
    python3 book-indonesia/scripts/gen_city_illustrations.py bali lombok   # multiple
"""
from __future__ import annotations

import concurrent.futures
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

# (slug, subject, gender) — alternating m/f within reading order.
# Reading order: jakarta → yogyakarta → mount-bromo → ijen-crater → bali →
# ubud → seminyak → nusa-penida → gili-islands → lombok → labuan-bajo → batam
CITIES: list[tuple[str, str, str]] = [
    (
        "jakarta",
        "Jakarta's Kota Tua (Old Town) square at golden hour — Dutch colonial "
        "facades of Fatahillah Square in cream and ochre with the Jakarta "
        "History Museum in the middle distance, a traditional brightly "
        "painted ontel bicycle-rental in the foreground, warm saffron "
        "late-afternoon sky, a few stylised palm silhouettes.",
        "m",
    ),
    (
        "yogyakarta",
        "Borobudur temple silhouette at sunrise, the stepped Buddhist stupa "
        "pyramid rising from misty Java rice fields, Mount Merapi volcano "
        "in the far distance, warm saffron pre-dawn sky breaking into "
        "gold, a single pilgrim walking the outer causeway.",
        "f",
    ),
    (
        "mount-bromo",
        "Mount Bromo's caldera at sunrise — the smoking active volcanic "
        "cone rising out of the Sea of Sand, Mount Semeru's snow-capped "
        "peak in the distance, a lone horse-and-rider silhouette on the "
        "ash plain, warm pink-gold pre-dawn sky with volcanic haze.",
        "m",
    ),
    (
        "ijen-crater",
        "The turquoise acid-lake crater of Mount Ijen at dawn, sulfur "
        "miners with traditional baskets climbing the rim trail, pale "
        "yellow sulfur deposits at the crater edge, the famous blue-flame "
        "vents visible at the base, soft cool dawn light in teal and "
        "deep-purple tones.",
        "f",
    ),
    (
        "bali",
        "Tanah Lot sea-temple at sunset, the offshore pagoda silhouette "
        "on its rocky outcrop with the Indian Ocean waves breaking around "
        "it, frangipani flower and traditional bamboo offering basket in "
        "the foreground, warm deep-orange sky with purple clouds.",
        "m",
    ),
    (
        "ubud",
        "Tegallalang rice terraces at golden hour — stepped emerald rice "
        "paddies cascading down a valley, a few palm trees along the "
        "terrace edges, a small stone temple with black-and-white-checker "
        "parasol (saput poleng), warm late-afternoon tropical light.",
        "f",
    ),
    (
        "seminyak",
        "Seminyak Beach at sunset with the low-tide bungalows and thatch "
        "beach-bar silhouettes along the sand, bean-bag loungers in the "
        "foreground, Mount Agung volcano silhouette on the horizon, warm "
        "pink-gold Indian Ocean sky.",
        "m",
    ),
    (
        "nusa-penida",
        "Kelingking Beach cliff viewpoint at golden hour — the iconic "
        "T-Rex-shaped limestone peninsula reaching into turquoise water, "
        "dramatic karst cliffs, warm late-afternoon light on the rock, "
        "a single stylised traveler silhouette on the viewpoint.",
        "f",
    ),
    (
        "gili-islands",
        "A Gili island beach from a wooden jetty at sunset — perfectly "
        "clear turquoise water, a traditional outrigger fishing boat on "
        "the sand, palm trees silhouetted against a pink-orange sky, "
        "Mount Rinjani's volcanic cone visible in the distance across "
        "the strait.",
        "m",
    ),
    (
        "lombok",
        "Mount Rinjani's caldera lake (Segara Anak) at dawn, the volcanic "
        "cone rising above a misty crater lake with the inner Mount Baru "
        "cone visible inside the caldera, warm pink-orange dawn light, "
        "small hiking silhouettes on the rim trail.",
        "f",
    ),
    (
        "labuan-bajo",
        "Labuan Bajo's Komodo National Park bay at golden hour — Phinisi "
        "sailing schooners anchored in turquoise water, Padar Island's "
        "three-cove viewpoint silhouette on the horizon, a Komodo dragon "
        "motif barely visible on a distant rocky outcrop, warm tropical "
        "late-afternoon light.",
        "m",
    ),
    (
        "batam",
        "Batam's Nagoya Hill waterfront at dusk — the distinctive red "
        "Barelang Bridge arching across the strait toward Singapore's "
        "skyline in the far distance, small fishing boats in the "
        "foreground, palm silhouettes, warm purple-pink twilight.",
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


def generate_one(api_key: str, slug: str, subject: str, gender: str) -> tuple[str, bool, str]:
    dest = OUT / f"{slug}.jpg"
    traveler = TRAVELER_F if gender == "f" else TRAVELER_M
    prompt = f"{subject} {traveler}{STYLE_BASE}"
    try:
        task = submit(api_key, prompt)
        out_url = poll(api_key, task, timeout=360)
        download(out_url, dest)
        return (slug, True, f"{dest.stat().st_size / 1024:.0f} KB")
    except Exception as e:
        return (slug, False, str(e))


def main() -> None:
    filter_slugs = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    cities = [c for c in CITIES if not filter_slugs or c[0] in filter_slugs]
    if not cities:
        sys.exit(f"no cities matched {filter_slugs}. valid slugs: {[c[0] for c in CITIES]}")

    api_key = get_api_key()

    todo = []
    for slug, subject, gender in cities:
        dest = OUT / f"{slug}.jpg"
        if dest.exists() and not filter_slugs:
            print(f"· {slug}: exists ({dest.stat().st_size / 1024:.0f} KB) — skip")
            continue
        todo.append((slug, subject, gender))

    if not todo:
        print("· nothing to generate")
        return

    print(f"→ Generating {len(todo)} city illustrations (6 workers)…")
    errors = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(generate_one, api_key, s, sub, g): s for s, sub, g in todo}
        for fut in concurrent.futures.as_completed(futures):
            slug, ok, info = fut.result()
            if ok:
                print(f"  ✓ {slug}: {info}")
            else:
                print(f"  ✗ {slug}: {info}", file=sys.stderr)
                errors.append((slug, info))
    if errors:
        sys.exit(1)
    print(f"\ndone. images in {OUT}")


if __name__ == "__main__":
    main()
