#!/usr/bin/env python3
"""
Generate 16 per-city cover illustrations for the Germany book via Wavespeed
(Nano Banana Pro).

Style: flat vector mid-century travel-poster, same palette as prior volumes.

Output: book-germany/assets/cities/<slug>.jpg

Usage:
    python3 book-germany/scripts/gen_city_illustrations.py
    python3 book-germany/scripts/gen_city_illustrations.py berlin munich
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
        "berlin",
        "Pariser Platz at dusk with the neoclassical Brandenburg Gate and its "
        "bronze quadriga statue in the middle distance, the Fernsehturm (TV "
        "Tower) silhouetted in the background, a couple of lime trees in the "
        "foreground, warm saffron-to-dusty-purple twilight sky.",
        "f",
    ),
    (
        "potsdam",
        "The terraced baroque gardens of Sanssouci Palace in late-afternoon "
        "light, the yellow palace facade crowning a hillside of vine-covered "
        "garden terraces, formal box-hedge parterres in the foreground, warm "
        "golden light, soft shadows from rows of poplar trees.",
        "m",
    ),
    (
        "hamburg",
        "The red-brick warehouses of the Speicherstadt district along the "
        "canals at early evening, the futuristic glass sail of the Elbphilharmonie "
        "concert hall rising in the middle distance, a traditional working barge "
        "on the canal in the foreground, warm maritime light.",
        "f",
    ),
    (
        "bremen",
        "The Marktplatz of Bremen at midday with the ornate Weser-Renaissance "
        "gable of the Rathaus (town hall) in the foreground, the bronze statue "
        "of the Town Musicians of Bremen (donkey, dog, cat, rooster stacked in "
        "a pyramid) on the left, the twin spires of Bremen Cathedral behind, "
        "warm pale sandstone light.",
        "m",
    ),
    (
        "dresden",
        "The baroque colonnade of the Zwinger palace courtyard at golden hour, "
        "the reconstructed sandstone dome of the Frauenkirche visible over the "
        "rooftops, the Elbe river reflecting the warm sandstone facades, soft "
        "evening light on Saxon sandstone.",
        "f",
    ),
    (
        "leipzig",
        "The monumental stone pyramid of the Völkerschlachtdenkmal (Monument "
        "to the Battle of the Nations) at sunrise, surrounded by formal "
        "reflecting pools, the Leipzig skyline and the Augustusplatz opera "
        "house in the distance, warm pale-gold early-morning light.",
        "m",
    ),
    (
        "munich",
        "The Marienplatz at blue hour with the neo-Gothic New Town Hall "
        "(Neues Rathaus) facade in the foreground, the twin onion-domed towers "
        "of the Frauenkirche silhouetted against the deep-blue evening sky in "
        "the background, warm streetlamp glow below, a whiff of Alpine light.",
        "f",
    ),
    (
        "nuremberg",
        "The Kaiserburg castle walls and watchtowers rising above the "
        "half-timbered roofs of the Altstadt at golden hour, the dark-red "
        "sandstone walls catching the late sun, a tiled rooftops sea flowing "
        "down to the Pegnitz river, warm Franconian afternoon light.",
        "m",
    ),
    (
        "frankfurt",
        "The Römerberg square at dusk with the distinctive stepped-gable "
        "timber-frame Römer town hall in the foreground, the modern banking "
        "skyline — Commerzbank Tower, Main Tower — glowing in the background, "
        "a contrast between medieval timber and glass-steel modernity.",
        "f",
    ),
    (
        "stuttgart",
        "The Schlossplatz in early evening with the long white baroque facade "
        "of the Neues Schloss on one side, the Jubiläumssäule victory column "
        "rising in the centre of the square, formal gardens and warm "
        "Swabian evening light, the Schwabentor hills in the distance.",
        "m",
    ),
    (
        "cologne",
        "The twin Gothic spires of the Kölner Dom (Cologne Cathedral) rising "
        "above the Rhine, the steel-lattice Hohenzollern Bridge crossing the "
        "river in the foreground with its thousands of love-locks, a KD river "
        "cruise ship passing under the bridge, warm late-afternoon Rhineland "
        "light.",
        "f",
    ),
    (
        "dusseldorf",
        "The Rheinturm telecommunications tower at sunset reflected in the "
        "Rhine, the curvaceous Frank-Gehry glass-and-steel buildings of the "
        "MedienHafen in the foreground, warm golden-hour light on the glass "
        "facades, a river promenade below.",
        "m",
    ),
    (
        "heidelberg",
        "The red-sandstone ruin of Heidelberg Castle above the Neckar river "
        "at golden hour, the five stone arches of the Alte Brücke (Old Bridge) "
        "spanning the river, the Old Town red-tile rooftops climbing the "
        "hillside below, warm Baden afternoon light.",
        "f",
    ),
    (
        "baden-baden",
        "The colonnaded Trinkhalle (pump room) at late-afternoon light, "
        "fresco-painted arcades of warm saffron sandstone, the formal Kurpark "
        "gardens extending in the foreground, the Black Forest hills in the "
        "background, gentle spa-town elegance.",
        "m",
    ),
    (
        "rothenburg",
        "The iconic Plönlein fork in Rothenburg ob der Tauber at blue hour, "
        "the narrow half-timbered yellow house standing where two medieval "
        "streets fork downhill, a pair of stone watchtowers flanking the "
        "cobblestone lanes, warm lamplight glow, deep-blue twilight sky.",
        "f",
    ),
    (
        "fussen",
        "Neuschwanstein Castle rising from forested hills at dawn, the pale "
        "grey romantic-revival stone silhouette with its tall round tower and "
        "pitched roofs, a morning mist drifting through the surrounding "
        "Bavarian Alpine forest, the distant Alps on the horizon, soft pink-"
        "gold sunrise light.",
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
