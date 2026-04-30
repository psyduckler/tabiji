#!/usr/bin/env python3
"""
Generate the Malaysia book cover art via Wavespeed (Nano Banana Pro):
 - front cover (dramatic 2:3 portrait scene, KLIA2 'teksi sapu' airport-tout shakedown)
 - back cover (2:3 portrait scene of George Town shophouse street at golden hour)

Style is the locked Malaysia comic style — Peranakan / Nyonya pastel
heritage watercolor. Both covers are scam-in-action / atmospheric scenes
that match the series quality bar set by Egypt + Australia.

Usage:
    python3 book-malaysia/scripts/gen_comics.py
    python3 book-malaysia/scripts/gen_comics.py --front-only
    python3 book-malaysia/scripts/gen_comics.py --back-only
    python3 book-malaysia/scripts/gen_comics.py --force         # overwrite existing
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


# Locked Malaysia comic style block — Peranakan / Nyonya pastel heritage.
# Single-panel cover variant of the 2x2 comic style block from
# memory:project_scam_comics_style_malaysia.md (no panel grid, single scene).
STYLE_PERANAKAN = (
    "Warm Peranakan / Nyonya heritage illustration style drawn from the "
    "Straits-Chinese aesthetic of Penang and Melaka shophouses — soft "
    "pastel palette of porcelain pink, mint green, butter yellow, sky "
    "blue, powder lavender, with cream backgrounds and delicate gilt "
    "accents. Gentle fine black ink line drawing with transparent "
    "watercolor wash interior, rounded friendly characters with soft "
    "expressive faces, location-accurate Malaysian architecture and "
    "landmarks, gentle storybook composition with visible watercolor "
    "texture. English text in any speech bubble must be clear, "
    "grammatically correct, and legible. No book title, no logos, "
    "no watermarks, no signatures, no decorative tile border around "
    "the edge of the canvas."
)


COVERS = [
    (
        "front",
        (
            "A single dramatic watercolor-storybook scene, portrait 2:3 "
            "aspect, depicting a Malaysia tourist scam in action at the "
            "KLIA2 airport taxi rank in Kuala Lumpur: a female tourist in "
            "a sun hat with a rolling suitcase stands on the curb beside "
            "the open back door of a red-and-white Malaysian taxi, the "
            "meter inside the cab clearly visible and reading 'OUT OF "
            "ORDER' in red. In the foreground, a friendly-looking "
            "Malaysian taxi tout in a short-sleeved batik shirt is "
            "gesturing at a small printed paper saying 'Meter rosak — "
            "RM 250, special airport rate' in a clean white speech "
            "bubble with a pointer tail. In the distance, the iconic "
            "twin spires of the Petronas Towers and the rounded silver "
            "control tower of KLIA2 silhouetted against a warm "
            "golden-hour sky. Palette: porcelain pink, mint green, "
            "butter yellow, sky blue, powder lavender, with cream "
            "highlights and gentle gilt accents on the cab's chrome. "
            "Composition leaves generous empty pastel sky in the upper "
            "third of the frame for a book cover title to be overlaid. "
            "Composition leaves a clear darker band across the lower "
            "fifth of the frame for a hook overlay. No book title text, "
            "no watermark, no logo — just the illustration."
        ),
        "2:3",
    ),
    (
        "back",
        (
            "A single watercolor-storybook scene, portrait 2:3 aspect, "
            "depicting a George Town, Penang shophouse street at golden "
            "hour from a three-quarter low view: a row of pastel "
            "Peranakan shophouses in porcelain pink, mint green, butter "
            "yellow and sky blue with gilt-accented shuttered windows "
            "and Chinese-character signboards along Lebuh Armenian, a "
            "rickshaw driver pedaling away from the camera in the "
            "middle ground, lanterns and bougainvillea spilling over "
            "wrought-iron balconies, the warm dusty-pink sky melting "
            "from coral overhead to butter-gold along the horizon. "
            "Composition is atmospheric and calm, with substantial "
            "empty pastel sky in the upper two-thirds of the frame to "
            "leave space for back-cover copy to be overlaid. Palette: "
            "soft pastel watercolor — porcelain pink, mint green, "
            "butter yellow, sky blue, powder lavender, with warm cream "
            "highlights. No text, no watermark, no book title, no "
            "decorative tile border around the edge of the canvas."
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
    ap.add_argument("--force", action="store_true",
                    help="overwrite existing cover JPGs")
    args = ap.parse_args()

    api_key = get_api_key()

    tasks = []
    for name, subject, aspect in COVERS:
        if args.front_only and name != "front":
            continue
        if args.back_only and name != "back":
            continue
        dest = COVERS_DIR / f"{name}.jpg"
        if dest.exists() and not args.force:
            print(f"· {name}.jpg exists — skipping (pass --force to overwrite)")
            continue
        prompt = f"{subject}\n\n{STYLE_PERANAKAN}"
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
