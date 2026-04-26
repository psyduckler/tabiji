#!/usr/bin/env python3
"""
Generate 19 per-city cover illustrations for the Mexico book via Wavespeed
(Nano Banana Pro).

Style: flat vector mid-century travel-poster, same palette as prior volumes
(saffron-gold, deep burgundy, dusty purple, muted teal). The city
illustrations are intentionally on a different visual track than the
interior scam comics (which are Lotería tarjeta) — they act as warm,
reader-friendly chapter openers.

Output: book-mexico/assets/cities/<slug>.jpg

Usage:
    python3 book-mexico/scripts/gen_city_illustrations.py
    python3 book-mexico/scripts/gen_city_illustrations.py mexico-city tulum
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
    "three-quarter view, looking toward the scene. Two arms, two hands, "
    "connected at the shoulders — anatomically clean."
)

TRAVELER_F = (
    "One stylised solo female traveler, shoulder-length dark hair, "
    "wearing a deep-burgundy jacket and a small backpack, seen from "
    "behind or three-quarter view, looking toward the scene. Two arms, "
    "two hands, connected at the shoulders — anatomically clean."
)


# 19 Mexican cities in narrative reading order
# (capital → highland heritage → Yucatán → Caribbean coast/islands → Pacific)
CITIES: list[tuple[str, str, str]] = [
    (
        "mexico-city",
        "The Zócalo (Plaza de la Constitución) at golden hour with the massive "
        "Catedral Metropolitana spires rising on one side and the giant Mexican "
        "flag pole at the center of the square, the National Palace's red-tezontle "
        "facade in the middle distance, jacaranda trees in bloom along the edge, "
        "warm late-afternoon saffron sky.",
        "f",
    ),
    (
        "puebla",
        "A row of Puebla's iconic Talavera-tiled colonial facades on Calle de los "
        "Dulces, blue-and-yellow ceramic patterns covering church and townhouse "
        "fronts, the snow-capped Popocatépetl volcano rising on the horizon "
        "beyond the rooftops, warm afternoon light catching the tiled domes.",
        "m",
    ),
    (
        "oaxaca",
        "The honey-colored cantera-stone facade of the Templo de Santo Domingo "
        "de Guzmán in Oaxaca's centro at golden hour, twin baroque towers "
        "illuminated, a row of jacaranda trees with purple blossoms in the plaza "
        "below, the green Sierra Madre del Sur silhouetted in the distance.",
        "f",
    ),
    (
        "guanajuato",
        "The famous Callejón del Beso with its narrow stone alley climbing "
        "between pastel-painted houses in coral, marigold, and dusty rose, the "
        "city's tiered hillside bursting with multicolored facades cascading down "
        "to the Templo de San Diego and the Jardín de la Unión, warm Mexican "
        "highland afternoon light.",
        "m",
    ),
    (
        "san-miguel-de-allende",
        "The pink-spired neogothic Parroquia de San Miguel Arcángel rising over "
        "the Jardín Principal at golden hour, its rose-cantera facade catching "
        "the late sun, jacarandas and laurel trees in the plaza below, rooftops "
        "of the colonial Centro Histórico extending in warm terracotta tones "
        "toward the Bajío hills beyond.",
        "f",
    ),
    (
        "guadalajara",
        "The twin yellow-tile spires of the Catedral de Guadalajara above Plaza "
        "de Armas at late afternoon, mariachi musicians silhouetted in the plaza, "
        "the kiosk's wrought-iron filigree in the foreground, the Teatro Degollado "
        "facade visible to one side, warm saffron Jalisco sky.",
        "m",
    ),
    (
        "merida",
        "The white limestone Plaza Grande of Mérida at midday with the twin-towered "
        "Catedral de San Ildefonso on one side, the rose-stone Casa de Montejo "
        "facade with its conquistador carvings opposite, royal-poinciana flame "
        "trees in bloom over the white plaza tiles, a flamboyán in scarlet flower "
        "in the foreground, warm Yucatán sun.",
        "f",
    ),
    (
        "san-cristobal-de-las-casas",
        "The yellow-and-white baroque Templo de Santo Domingo facade in San "
        "Cristóbal at late afternoon, the cobblestone Real de Guadalupe street "
        "with low colonial buildings in cream and earth tones, pine-clad Chiapas "
        "highlands rising in the misty background, a Tzotzil weaver in "
        "traditional huipil silhouetted near the church steps.",
        "m",
    ),
    (
        "cancun",
        "An aerial three-quarter view of the Cancún Hotel Zone's crescent of "
        "turquoise Caribbean lagoon and white-sand beach, palm trees lining the "
        "boulevard, a curving line of low pyramidal hotels in cream and saffron, "
        "the deep-blue open Caribbean on one horizon and the Nichupté lagoon on "
        "the other, warm tropical golden hour.",
        "f",
    ),
    (
        "playa-del-carmen",
        "Quinta Avenida (5th Avenue) in Playa del Carmen at dusk, a stylised "
        "cobblestone pedestrian street lined with low palm-shaded shops, paper "
        "papel-picado banners strung overhead, the Cozumel ferry terminal pier "
        "visible at the end of the avenue with the deep-teal Caribbean beyond, "
        "warm saffron-and-coral sunset sky.",
        "m",
    ),
    (
        "tulum",
        "The cliffside El Castillo Mayan pyramid of Tulum perched on a limestone "
        "bluff above the turquoise Caribbean, the curved white-sand crescent of "
        "Playa Ruinas below, agave and palm trees in the foreground, a single "
        "sea bird gliding past, warm late-afternoon Yucatán light, deep teal "
        "water beneath the ruin.",
        "f",
    ),
    (
        "cozumel",
        "The San Miguel de Cozumel waterfront Malecón at golden hour, a row of "
        "low pastel-colored buildings in cream and turquoise facing the harbor, "
        "the Cozumel reef-edge ferry pier extending into the Caribbean, a few "
        "stylised silhouettes of cruise ships on the horizon, warm tropical sun.",
        "m",
    ),
    (
        "isla-mujeres",
        "Playa Norte on Isla Mujeres at late morning, shallow ankle-deep "
        "turquoise water lapping a powdery white-sand beach, palm-thatched "
        "palapas casting striped shadows, a wooden golf-cart boardwalk curving "
        "along the shore, the silhouette of Cancún just visible across the "
        "shallows, warm Caribbean light.",
        "f",
    ),
    (
        "holbox",
        "The sandy unpaved main street of Holbox island at sunset, palm-thatched "
        "palapa restaurants in saffron and burgundy on either side, a flamingo "
        "wading in a shallow lagoon to one side of the lane, a hand-painted street "
        "mural visible on a low wall, no cars — only golf carts — warm saffron "
        "Yucatán sky.",
        "m",
    ),
    (
        "puerto-vallarta",
        "The Malecón seawall promenade of Puerto Vallarta at sunset with one of "
        "the iconic bronze sculptures silhouetted against the sky, the curve of "
        "Banderas Bay extending toward Mismaloya in the distance, the Sierra "
        "Madre ridges descending into the Pacific, warm coral-and-saffron sunset.",
        "f",
    ),
    (
        "mazatlan",
        "The Old Lighthouse cliff (El Faro) above the Pacific at Mazatlán at "
        "golden hour, the curve of Olas Altas beach below, a stylised malecón "
        "lined with palm trees, the deep blue Pacific stretching toward Stone "
        "Island, warm saffron-and-burgundy sky behind the lighthouse silhouette.",
        "m",
    ),
    (
        "acapulco",
        "The La Quebrada cliffs of Acapulco at dusk, a single stylised cliff "
        "diver mid-leap arched out from the rock face above the narrow Pacific "
        "inlet far below, the curve of Acapulco Bay and the Costera Miguel "
        "Alemán lit in golden window-glow in the distance, warm coral-and-violet "
        "twilight sky.",
        "f",
    ),
    (
        "cabo-san-lucas",
        "El Arco de Cabo San Lucas — the natural granite rock arch at Land's "
        "End where the Sea of Cortez meets the Pacific — at golden hour, sea "
        "lions silhouetted on the rocks, the Friar Rocks behind, a stylised "
        "panga fishing boat passing through the arch, warm saffron sun on the "
        "water, deep teal Sea of Cortez color.",
        "m",
    ),
    (
        "puerto-escondido",
        "Zicatela Beach at Puerto Escondido at golden hour with a stylised "
        "barreling Pipeline wave breaking offshore, two surfer silhouettes "
        "paddling out, the long curve of dark sand stretching toward the "
        "headland, palms in the foreground, deep coral-and-saffron Pacific "
        "sunset sky.",
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
        prompt = f"{subject} {traveler} {STYLE_BASE}"
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
