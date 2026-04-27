#!/usr/bin/env python3
"""
Generate 13 per-city cover illustrations for the Turkey book via Wavespeed
(Nano Banana Pro).

Style: flat vector mid-century travel-poster, same palette as prior volumes.

Output: book-turkey/assets/cities/<slug>.jpg

Usage:
    python3 book-turkey/scripts/gen_city_illustrations.py
    python3 book-turkey/scripts/gen_city_illustrations.py istanbul cappadocia
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
        "istanbul",
        "Sultanahmet Square at dusk with the cascading domes and six minarets of "
        "the Blue Mosque (Sultan Ahmed Mosque) in the middle distance and the "
        "massive dome of Hagia Sophia silhouetted to one side, a pair of cypress "
        "trees in the foreground, warm saffron-to-dusty-purple twilight sky, "
        "a trace of the Bosphorus barely visible in the background.",
        "f",
    ),
    (
        "cappadocia",
        "The Göreme valley at sunrise with dozens of hot-air balloons rising in "
        "silent silhouette above the otherworldly fairy-chimney rock formations, "
        "warm golden-hour light catching the balloon envelopes in saffron, "
        "ochre, and deep burgundy, soft morning mist in the valleys below, "
        "cave dwellings carved into the stone in the middle distance.",
        "m",
    ),
    (
        "izmir",
        "Konak Square in İzmir at golden hour with the ornate Ottoman-style "
        "Saat Kulesi (clock tower) in the foreground, the Aegean waterfront "
        "and a line of ferries crossing the bay in the middle distance, palm "
        "trees along the promenade, warm Mediterranean late-afternoon light.",
        "f",
    ),
    (
        "ephesus",
        "The two-story marble facade of the Library of Celsus at late afternoon, "
        "honey-colored stone columns and pediments catching the warm sun, a "
        "broad ancient marble-paved avenue leading toward it lined with "
        "fragmentary columns, cypress trees framing the scene, a stylised "
        "warm-gold sky.",
        "m",
    ),
    (
        "kusadasi",
        "Pigeon Island (Güvercinada) with its stone causeway and castle "
        "silhouetted against the Aegean at sunset, small fishing boats in "
        "the foreground harbor, the Kuşadası seafront promenade with palm "
        "trees along the quay, warm peach-gold sky, dusty purple distant "
        "islands.",
        "f",
    ),
    (
        "bodrum",
        "The Castle of St Peter (Bodrum Castle) on its peninsula above the "
        "twin crescent harbors of Bodrum at golden hour, white-washed "
        "stepped houses climbing the hillsides, a line of gulet wooden "
        "sailing boats anchored in the bay, warm Aegean light, a single "
        "bougainvillea in the foreground.",
        "m",
    ),
    (
        "marmaris",
        "The crescent bay of Marmaris seen from a ridge above the marina "
        "at blue hour, forested pine-clad peninsulas extending into the "
        "Mediterranean, a quay of white yachts with their masts stylised "
        "in a line, warm pink-and-teal sky fading to indigo, the Taurus "
        "mountain foothills silhouetted in the distance.",
        "f",
    ),
    (
        "fethiye",
        "The turquoise Ölüdeniz Blue Lagoon seen from the Babadağ ridge, "
        "a paraglider silhouetted mid-flight above the lagoon in golden-hour "
        "light, the ridge cascading down to the beach, a sweep of pine forest, "
        "warm Lycian Mediterranean light, a stylised cove curving into "
        "the deep blue water.",
        "m",
    ),
    (
        "antalya",
        "Kaleiçi old-town harbor at late afternoon with the Ottoman "
        "Yivli Minare minaret rising from the old quarter, stone-walled "
        "harbor with traditional wooden boats, the silhouette of the "
        "Taurus Mountains framing the view, warm Mediterranean light, "
        "a row of palms along the promenade.",
        "f",
    ),
    (
        "alanya",
        "The iconic Red Tower (Kızıl Kule) and the castle-crowned rocky "
        "peninsula of Alanya rising above Cleopatra Beach at golden hour, "
        "warm Mediterranean sea washing the crescent beach, the Seljuk "
        "shipyard visible at the base of the cliff, stylised palms in "
        "the foreground.",
        "m",
    ),
    (
        "side-turkey",
        "The colonnaded ruins of the Temple of Apollo at the end of the Side "
        "peninsula at sunset, six honey-colored marble columns standing "
        "against a warm peach sky above the Mediterranean, a fragment of "
        "the ancient theater visible in the middle distance, stylised "
        "waves on the rocks below.",
        "f",
    ),
    (
        "pamukkale",
        "The surreal white travertine terraces of Pamukkale cascading down "
        "the hillside at dawn, each terrace a shallow turquoise pool "
        "reflecting the warm pink-saffron sky, the cliff face stained "
        "calcium-white, the plain of Denizli extending in the distance.",
        "m",
    ),
    (
        "konya",
        "The turquoise-domed Mevlana Museum (Mausoleum of Rumi) at golden "
        "hour, its fluted green-blue tiled conical dome rising above the "
        "central Konya plaza, a few stylised cypress trees, warm Anatolian "
        "afternoon light, a whirling-dervish silhouette barely visible in "
        "the foreground.",
        "f",
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
