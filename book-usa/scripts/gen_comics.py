#!/usr/bin/env python3
"""
Generate the Egypt book cover art via Wavespeed (Nano Banana Pro):
 - front cover (dramatic 2:3 portrait scene, Giza camel-handler scam in action)
 - back cover (2:3 portrait scene of a calm Aswan Nile felucca at golden hour)

Both prompts use the locked Egypt scam-comic style (modern-cairo-illustrated:
gouache + ink, sand-gold/Nile-blue palette) adapted to a single hero scene
rather than the 4-panel layout used for the per-scam comics.

Saves to assets/svg/{front,back}.jpg so the same-directory SVGs resolve their
relative xlink:href image references. Also mirrors to assets/covers/ so the
desktop-bundle pattern (02-cover-art/front-raw.jpg etc.) picks them up.

Usage:
    python3 book-egypt/scripts/gen_comics.py
    python3 book-egypt/scripts/gen_comics.py --front-only
    python3 book-egypt/scripts/gen_comics.py --back-only
    python3 book-egypt/scripts/gen_comics.py --force      # regenerate
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import requests


HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
SVG_DIR = BOOK / "assets" / "svg"
COVERS_DIR = BOOK / "assets" / "covers"
SVG_DIR.mkdir(parents=True, exist_ok=True)
COVERS_DIR.mkdir(parents=True, exist_ok=True)


STYLE_COMIC = (
    "Classic American Silver-Age comic-book cover style (Marvel/DC circa "
    "Kirby and Ditko): bold flat primary colors (classic red, royal blue, "
    "chrome yellow, white), confident black ink outlines with expressive "
    "cross-hatching, halftone Ben-Day dot shading in the mid-tones, dynamic "
    "composition with subtle speed lines. Single full-bleed hero scene — NO "
    "panel borders, NO grid layout, NO numbered panels. No logos, no "
    "watermarks, no signatures, no real-world brand marks or trademarked "
    "characters."
)


COVERS = [
    (
        "front",
        (
            "A single dramatic Silver-Age American comic-book HERO cover "
            "scene, portrait 2:3 aspect, depicting a classic US tourist scam "
            "in action on a bright, bustling American city sidewalk with "
            "generic neon signs and skyscrapers behind (NO real brand names "
            "or logos on any sign). Foreground (lower two-thirds): a "
            "62-year-old Western woman tourist with shoulder-length "
            "silver-gray hair under a woven straw sun hat, warm friendly "
            "face, a coral scarf, cream linen blouse and tan travel pants, a "
            "small tan crossbody bag — standing at three-quarter view, "
            "hesitant, one hand half-raised. Beside her a slick, grinning "
            "street hustler in a hi-vis orange vest over a t-shirt holds out "
            "a smartphone showing a generic QR code and gestures for "
            "payment. A bright jagged yellow starburst behind them carries "
            "the bold sound-effect 'SCAM!' in blocky red comic letters. Both "
            "figures are roughly half the frame height — clearly the focal "
            "subjects, not tiny. Bold black ink outlines, flat primary "
            "colors, halftone Ben-Day dot shading, classic Silver-Age comic "
            "look. The composition reserves a roughly 18%-tall band of "
            "high-contrast sky at the very top edge for a book-cover title "
            "to be overlaid, and the very bottom edge has darker tones for a "
            "hook block. Apart from the single 'SCAM!' sound-effect, NO "
            "other text, NO book title, NO watermark, NO logo, NO real brand "
            "names, NO signature — just the bold comic illustration."
        ),
        "2:3",
    ),
    (
        "back",
        (
            "A single calm Silver-Age American comic-book style landscape, "
            "portrait 2:3 aspect, depicting a quiet classic American "
            "small-town Main Street at golden hour — brick storefronts with "
            "blank unbranded awnings, a striped barber pole, vintage "
            "streetlamps, the American flag on a pole, soft warm evening "
            "light. NO PEOPLE. NO HUMAN FIGURES. NO FOREGROUND CHARACTERS. "
            "Bold black ink outlines, flat primary colors, gentle halftone "
            "Ben-Day dot shading. Substantial calm sky in the upper two- "
            "thirds of the frame for back-cover copy to be overlaid. "
            "ABSOLUTELY NO TEXT, NO LETTERS, NO WORDS, NO SPEECH BUBBLES, NO "
            "STORE NAMES, NO TYPOGRAPHY, NO CAPTIONS, NO WATERMARK, NO BOOK "
            "TITLE, NO REAL BRAND NAMES, NO SIGNATURE — pure illustration "
            "only."
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
                    help="Regenerate even if the destination already exists")
    args = ap.parse_args()

    api_key = get_api_key()

    tasks = []
    for name, subject, aspect in COVERS:
        if args.front_only and name != "front":
            continue
        if args.back_only and name != "back":
            continue
        # Save next to the SVG so xlink:href="front.jpg" resolves automatically.
        dest = SVG_DIR / f"{name}.jpg"
        if dest.exists() and not args.force:
            print(f"· {name}.jpg exists — skipping (use --force to override)")
            continue
        prompt = f"{subject}\n\n{STYLE_COMIC}"
        tasks.append((prompt, dest, aspect))

    print(f"→ Queuing {len(tasks)} generations…")
    ok = 0
    for prompt, dest, aspect in tasks:
        print(f"  → {dest.relative_to(BOOK)} ({aspect})…", flush=True)
        if generate(api_key, prompt, dest, aspect):
            # Mirror to assets/covers/ for the desktop-bundle pattern.
            mirror = COVERS_DIR / dest.name
            shutil.copy(dest, mirror)
            ok += 1
            print(f"  ✓ {dest.name} ({dest.stat().st_size / 1024:.0f} KB)")
    print(f"\nDone: {ok} / {len(tasks)} succeeded")


if __name__ == "__main__":
    main()
