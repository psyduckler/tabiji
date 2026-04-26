#!/usr/bin/env python3
"""
Generate the Mexico book cover art via Wavespeed (Nano Banana Pro):
 - front cover (dramatic 2:3 portrait scene, Lotería tarjeta style — matches
   the Don Clemente Lotería interior scam comics)
 - back cover (2:3 portrait scene of a Mexican mercado evening, also Lotería)

Scam-comic assets for the 114 Mexican scams already live on R2 and are
downloaded into book-mexico/assets/images/<slug>/NN.jpg by the initial setup
step. This script only needs to generate the two covers.

Usage:
    python3 book-mexico/scripts/gen_comics.py
    python3 book-mexico/scripts/gen_comics.py --front-only
    python3 book-mexico/scripts/gen_comics.py --back-only
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

import requests


HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
COVERS_DIR = BOOK / "assets" / "covers"
COVERS_DIR.mkdir(parents=True, exist_ok=True)


# Lotería tarjeta style — the iconic Don Clemente deck aesthetic. Same visual
# track as the 114 interior scam comics. Distinct from the rest of the
# series (which uses watercolor-storybook for covers) because Mexico's
# interior comics are Lotería and the cover should be visually consistent
# with what's inside.
STYLE_LOTERIA = (
    "Lotería tarjeta illustration in the classic Don Clemente Mexican playing-"
    "card style. Flat saturated palette of chili red, marigold yellow, "
    "sky blue, cactus green, and cream paper background. Bold black ink "
    "outlines, ornamental Mexican folk-art panel border at the edges of the "
    "frame. Visible cream paper-grain texture. No text in any speech bubbles, "
    "no captions, no Lotería numbers — pure visual scene only. No watermark, "
    "no logo, no signature."
)


COVERS = [
    (
        "front",
        (
            "A single dramatic Lotería tarjeta scene, full bleed, portrait 2:3 "
            "aspect, depicting a Mexico tourist scam in action on the Mexico City "
            "Zócalo (Plaza de la Constitución): a female tourist with shoulder-"
            "length dark hair stands on the wide stone-paved plaza, the massive "
            "twin-spired Catedral Metropolitana rising on one side and the "
            "giant Mexican flag pole at the center of the square. In the middle "
            "ground, an Aztec ceremonial dancer in a feathered Quetzal headdress "
            "is gesturing at a clipboard with a wide friendly smile, while in "
            "the background a yellow-and-white sitio taxi with its meter visibly "
            "broken (springs popping out) waits at the curb. The composition "
            "leaves generous empty saffron-and-coral sky in the upper third of "
            "the frame for a book cover title to be overlaid. Lotería style: "
            "chili red, marigold yellow, sky blue, cactus green, ornamental "
            "panel border, cream paper grain. No book title text, no watermark, "
            "no logo — just the illustration."
        ),
        "2:3",
    ),
    (
        "back",
        (
            "A single Lotería tarjeta scene, portrait 2:3 aspect, depicting an "
            "atmospheric Mexican mercado evening from a three-quarter overhead "
            "view: rows of papel-picado paper banners in chili red, marigold, "
            "and turquoise strung overhead, market stalls below piled with "
            "talavera ceramics, woven sarapes, dried chilies, and pan dulce, "
            "warm hanging hojalata tin lanterns glowing amber, a few silhouetted "
            "figures browsing the aisles, the distant glow of a comal griddle "
            "at the end of the arcade. Composition is atmospheric and calm, "
            "with substantial empty marigold-and-violet upper-area space in the "
            "upper two-thirds of the frame to leave room for back-cover copy "
            "to be overlaid. Lotería style: flat saturated palette, ornamental "
            "panel border at the frame edge, visible cream paper grain, bold "
            "black ink outlines. No text, no watermark, no book title."
        ),
        "2:3",
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


def submit(api_key: str, prompt: str, aspect_ratio: str = "2:3") -> str:
    url = "https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image"
    r = requests.post(url, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }, json={
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "resolution": "2k",
        "output_format": "jpeg",
    }, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data["data"]["id"] if "data" in data and "id" in data["data"] else data["id"]


def poll(api_key: str, task_id: str, timeout: int = 420) -> str:
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
            return outputs if isinstance(outputs, str) else outputs[0]
        if status == "failed":
            raise RuntimeError(f"task failed: {body}")
        time.sleep(3)
    raise TimeoutError(f"task {task_id} timed out")


def download(url: str, dest: Path) -> None:
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    dest.write_bytes(r.content)


def generate(api_key: str, prompt: str, dest: Path, aspect_ratio: str) -> bool:
    try:
        task = submit(api_key, prompt, aspect_ratio)
        out_url = poll(api_key, task)
        download(out_url, dest)
        return True
    except Exception as e:
        print(f"✗ {dest}: {e}", file=sys.stderr)
        return False


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--front-only", action="store_true")
    ap.add_argument("--back-only", action="store_true")
    args = ap.parse_args()

    api_key = get_api_key()

    tasks = []
    for name, subject, aspect in COVERS:
        if args.front_only and name != "front": continue
        if args.back_only and name != "back": continue
        dest = COVERS_DIR / f"{name}.jpg"
        if dest.exists():
            print(f"· {name}.jpg exists — skipping")
            continue
        prompt = f"{subject}\n\n{STYLE_LOTERIA}"
        tasks.append((prompt, dest, aspect))

    print(f"→ Queuing {len(tasks)} generations…")
    ok = 0
    for prompt, dest, aspect in tasks:
        print(f"  → {dest.relative_to(BOOK)} ({aspect})…")
        if generate(api_key, prompt, dest, aspect):
            ok += 1
            print(f"  ✓ {dest.name} ({dest.stat().st_size / 1024:.0f} KB)")
    print(f"\nDone: {ok} / {len(tasks)} succeeded")


if __name__ == "__main__":
    main()
