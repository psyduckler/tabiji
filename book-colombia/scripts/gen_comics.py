#!/usr/bin/env python3
"""
Generate the Argentina book cover art via Wavespeed (Nano Banana Pro):
 - front cover (single dramatic 2:3 portrait scene, Argentine scam in action)
 - back cover (single 2:3 portrait scene of porteño atmosphere with
   upper-third negative space for cover-copy overlay)

Scam-comic assets for the 66 Argentina scams already live on R2 at
img.tabiji.ai/scams/<slug>/scam-N.jpg and are downloaded into
book-argentina/assets/images/<slug>/NN.jpg by the pull_comics.py one-off.
This script only generates the two covers.

Usage:
    python3 book-argentina/scripts/gen_comics.py              # both covers
    python3 book-argentina/scripts/gen_comics.py --front-only
    python3 book-argentina/scripts/gen_comics.py --back-only
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


STYLE_COMIC = (
    "Watercolor-storybook illustration in soft hand-painted lines, pastel "
    "palette with warm cream and muted ochre background, gentle shading. "
    "Matches a travel-safety book interior illustration style. English text "
    "in speech bubbles must be clear, grammatically correct, and legible. "
    "No logos, no watermarks, no signatures."
)


# --- COVER PROMPTS --------------------------------------------------------

COVERS = [
    (
        "front",
        (
            "A single dramatic watercolor-storybook scene, portrait 2:3 aspect, "
            "depicting an Argentine tourist scam in action on Calle Florida in "
            "Buenos Aires: a female tourist in a light sun hat and a tan "
            "crossbody bag stands on the pedestrian shopping street with the "
            "ornate Galerías Pacífico facade and a tango-mural shopfront in the "
            "background, looking uncertain, while a smiling young porteño in a "
            "cream button-down leans from a doorway holding a clipboard with a "
            "hand-drawn exchange rate and says '¡Cambio! Best rate today!' in a "
            "white speech bubble. The palette is warm porteño cream, soft "
            "mustard, dusty rose, and gentle sky-blue — echoing a Quino Mafalda "
            "newspaper-strip sensibility. Composition leaves generous empty sky "
            "and upper-building silhouette in the upper third of the frame for "
            "a book cover title to be overlaid. No book title text, no "
            "watermark, no logo — just the illustration."
        ),
        "2:3",
    ),
    (
        "back",
        (
            "A single watercolor-storybook scene, portrait 2:3 aspect, depicting "
            "a calm San Telmo evening street scene in Buenos Aires from a "
            "three-quarter overhead view: a narrow cobblestone street lined with "
            "19th-century Italianate facades, wrought-iron balconies with "
            "cascading jasmine, a warm-lit parrilla lantern glowing warmly, a "
            "couple dancing tango in silhouette in the middle distance, and "
            "the distant silhouette of the Iglesia de San Pedro González Telmo "
            "bell tower against a twilight sky. Composition is atmospheric and "
            "calm, with substantial empty dusty-purple sky in the upper "
            "two-thirds of the frame to leave space for back-cover copy to be "
            "overlaid. Palette: pastel watercolor, warm lantern glow, hints of "
            "dusty rose and sage and porteño cream. No text, no watermark, no "
            "book title."
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

    tasks: list[tuple[str, Path, str]] = []
    for name, subject, aspect in COVERS:
        if args.front_only and name != "front":
            continue
        if args.back_only and name != "back":
            continue
        dest = COVERS_DIR / f"{name}.jpg"
        if dest.exists():
            print(f"· {name}.jpg exists — skipping (delete to regen)")
            continue
        prompt = f"{subject}\n\n{STYLE_COMIC}"
        tasks.append((prompt, dest, aspect))

    print(f"→ Queuing {len(tasks)} generations…")
    ok = 0
    for prompt, dest, aspect in tasks:
        print(f"  → {dest.relative_to(BOOK)} ({aspect})…")
        if generate(api_key, prompt, dest, aspect):
            ok += 1
            size_kb = dest.stat().st_size / 1024
            print(f"  ✓ {dest.name} ({size_kb:.0f} KB)")
    print(f"\nDone: {ok} / {len(tasks)} succeeded")


if __name__ == "__main__":
    main()
