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
        "rome",
        "The Colosseum at golden hour, warm-cream Roman arches viewed from the Via Sacra, "
        "umbrella pines in silhouette, warm haze over the Forum stones.",
        "m",
    ),
    (
        "venice",
        "The Rialto Bridge at dusk over the Grand Canal, a single gondola gliding beneath, "
        "Venetian palazzo facades in warm terracotta and cream, reflections on the water.",
        "f",
    ),
    (
        "florence",
        "Brunelleschi's Duomo dome rising above terracotta rooftops of the centro storico, "
        "Arno river bend in the distance, Tuscan cypress silhouettes on the hills.",
        "m",
    ),
    (
        "milan",
        "The glass-and-iron dome of Galleria Vittorio Emanuele II from the cathedral square, "
        "Duomo spires on one side, soft interior lamplight spilling onto the mosaic floor.",
        "f",
    ),
    (
        "naples",
        "Spaccanapoli narrow alley with hanging laundry and a Vespa parked against a warm-ochre wall, "
        "Mount Vesuvius in the hazy distance at sunset.",
        "m",
    ),
    (
        "bologna",
        "The Due Torri (Torre degli Asinelli and Garisenda) rising above a porticoed street, "
        "long sunset shadows through the portico arches, deep-burgundy Bologna brickwork.",
        "f",
    ),
    (
        "palermo",
        "The Quattro Canti baroque crossroads in Palermo, four curved palazzo facades meeting at the corner, "
        "late-afternoon sun, a Sicilian palm in silhouette.",
        "m",
    ),
    (
        "pisa",
        "The Leaning Tower beside the Duomo on the Campo dei Miracoli, crisp green lawn, "
        "a few tourists in silhouette, warm Tuscan afternoon light.",
        "f",
    ),
    (
        "siena",
        "The shell-shaped Piazza del Campo with the Torre del Mangia above the Palazzo Pubblico, "
        "medieval brick facades, warm terracotta and saffron tones, deep shadows.",
        "m",
    ),
    (
        "sorrento",
        "The Sorrento cliffs at Marina Grande, pastel-ochre houses stacked above the fishing harbor, "
        "lemon trees in the foreground, Bay of Naples at dusk.",
        "f",
    ),
    (
        "positano",
        "The iconic Positano hillside of pastel houses cascading down to the Spiaggia Grande beach, "
        "turquoise Tyrrhenian sea, a small boat in the bay at golden hour.",
        "m",
    ),
    (
        "amalfi-coast",
        "A winding SS163 Amalfi Drive clinging to a vertical cliff above the sea, lemon groves, "
        "a small white-painted church tower on the hill, warm late-day sun.",
        "f",
    ),
    (
        "capri",
        "The Faraglioni rock stacks off the coast of Capri, seen from a stylised viewpoint on the cliff path, "
        "turquoise sea, Mediterranean pines framing the composition.",
        "m",
    ),
    (
        "pompeii",
        "The ruined Forum of Pompeii with fluted column fragments in the foreground, "
        "Mount Vesuvius looming in the background against a saffron sky, long ancient shadows.",
        "f",
    ),
    (
        "cinque-terre",
        "The pastel cliff-houses of Manarola cascading down into a small harbor, "
        "turquoise Ligurian sea, a single fishing boat, late-afternoon warm light.",
        "m",
    ),
    (
        "verona",
        "The oval of the Roman Arena viewed from Piazza Bra, warm ochre stone, "
        "outdoor café umbrellas in silhouette in the foreground, soft evening light.",
        "f",
    ),
    (
        "lake-garda",
        "Sirmione castle (Castello Scaligero) on the narrow peninsula, crenellated brick walls, "
        "turquoise Lake Garda water, Alpine foothills in the distance.",
        "m",
    ),
    (
        "lake-como",
        "A view of Bellagio from the water, pastel palazzi stepping up the steep shoreline, "
        "Alpine peaks rising behind, a single classic wooden boat in the foreground.",
        "f",
    ),
    (
        "sardinia",
        "The turquoise coastline of the Costa Smeralda, pink-granite boulders, Mediterranean macchia scrub, "
        "a small white-sand cove with a single sailboat offshore.",
        "m",
    ),
    (
        "taormina",
        "The ruined Teatro Antico of Taormina with its stone arches framing a view of Mount Etna, "
        "a wisp of smoke from the volcano, Ionian sea below, late-afternoon warm light.",
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
