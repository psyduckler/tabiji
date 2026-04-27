#!/usr/bin/env python3
"""
Generate the Morocco book cover art via Wavespeed (Nano Banana Pro):
 - front cover (dramatic 2:3 portrait scene, Marrakech 'that way's closed' fake-guide play)
 - back cover (2:3 portrait scene of a Marrakech medina alley at evening with copper lantern glow)

Scam-comic assets for the 61 Moroccan scams already live on R2 and are downloaded
into book-morocco/assets/images/<slug>/NN.jpg by the initial setup step.
This script only needs to generate the two covers.

Usage:
    python3 book-morocco/scripts/gen_comics.py
    python3 book-morocco/scripts/gen_comics.py --front-only
    python3 book-morocco/scripts/gen_comics.py --back-only
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
    "palette with warm cream and muted saffron background, gentle shading. "
    "Matches a travel-safety book interior illustration style. English text "
    "in speech bubbles must be clear, grammatically correct, and legible. "
    "No logos, no watermarks, no signatures."
)


COVERS = [
    (
        "front",
        (
            "A single dramatic watercolor-storybook scene, portrait 2:3 aspect, "
            "depicting a Morocco tourist scam in action in the Marrakech medina: "
            "a female tourist with a small daypack stands in a narrow ochre-walled "
            "alley near the entrance to Djemaa el-Fna, looking confused at her "
            "phone. A friendly-looking Moroccan man in a striped djellaba is "
            "gesturing down a side street saying 'My friend! That way is closed "
            "today — festival! I show you good way!' in a white speech bubble. "
            "The brick minaret of the Koutoubia Mosque is visible in the upper "
            "distance against a saffron-to-dusty-purple sunset sky. Composition "
            "leaves generous empty sky in the upper third for a book cover title "
            "overlay. Palette: warm ochre, terracotta, saffron, deep burgundy, "
            "muted teal shadows. No book title text, no watermark, no logo — "
            "just the illustration."
        ),
        "2:3",
    ),
    (
        "back",
        (
            "A single watercolor-storybook scene, portrait 2:3 aspect, depicting "
            "a quiet Marrakech medina alley in the early evening from a three-"
            "quarter view: warm copper lanterns hanging from the ochre and "
            "terracotta walls of a narrow medina lane casting pools of "
            "saffron-amber light on the stone-paved floor, hanging carpets in "
            "deep burgundy and saffron lining one wall, a brass tea-pot stall in "
            "the middle distance, a few silhouetted figures walking deeper into "
            "the medina, the silhouette of a minaret in the upper distance. "
            "Composition is atmospheric and calm, with substantial empty "
            "dusty-purple-and-saffron upper-wall and sky area in the upper "
            "two-thirds for back-cover copy to be overlaid. Palette: pastel "
            "watercolor, warm amber lantern glow, hints of saffron, burgundy, "
            "and indigo shadows. No text, no watermark, no book title."
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
        prompt = f"{subject}\n\n{STYLE_COMIC}"
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
