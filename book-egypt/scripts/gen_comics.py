#!/usr/bin/env python3
"""
Generate the Italy book cover art via Wavespeed (Nano Banana Pro):
 - front cover (dramatic 2:3 portrait scene, Colosseum gladiator photo extortion)
 - back cover (2:3 portrait scene of a Venetian canal at golden hour)

Saves to assets/svg/{front,back}.jpg so the same-directory SVGs resolve their
relative xlink:href image references. Also mirrors to assets/covers/ so the
desktop-bundle pattern (02-cover-art/front-raw.jpg etc.) picks them up.

Usage:
    python3 book-italy/scripts/gen_comics.py
    python3 book-italy/scripts/gen_comics.py --front-only
    python3 book-italy/scripts/gen_comics.py --back-only
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
            "depicting the iconic Italy tourist scam in action outside the "
            "Roman Colosseum: a young female tourist with shoulder-length brown "
            "hair, wearing a light cream linen sundress and a small straw "
            "shoulder bag, stands on the warm-stone Via Sacra. A man dressed as "
            "a Roman gladiator-centurion (red plumed helmet, leather "
            "breastplate, sandals, a short red tunic) has just draped his arm "
            "across her shoulders for a photograph; her travel companion is "
            "lifting a phone to take the picture. The gladiator's face has "
            "shifted from a smile to a hard demanding look. He is saying "
            "'Trenta euro!' in a clean white speech bubble with a small "
            "pointer tail. Two more costumed Roman 'friends' in similar red "
            "tunics are visible in the middle distance, watching from the "
            "Colosseum entrance. The massive curve of the Colosseum's outer "
            "wall fills the right background, with umbrella-pine silhouettes "
            "and the Arch of Constantine partly visible to the left. Warm "
            "golden-hour Roman sky in saffron, dusty rose, and pale cream — "
            "composition leaves generous empty sky in the upper third for a "
            "book-cover title to be overlaid. Palette: warm ochre, saffron, "
            "deep burgundy, muted teal shadows, terracotta. No book title "
            "text, no watermark, no logo — just the illustration."
        ),
        "2:3",
    ),
    (
        "back",
        (
            "A single quiet watercolor-storybook landscape painting, portrait "
            "2:3 aspect, depicting a calm Venetian canal scene at golden hour, "
            "viewed from a low vantage point on the water: warm-terracotta and "
            "pale-yellow Venetian palazzo facades line both sides of a narrow "
            "rio, their lower floors weathered by water; arched bridges cross "
            "in the middle distance. A single empty black-prowed gondola is "
            "moored at a striped mooring pole in the foreground, water "
            "reflecting the warm sky. NO PEOPLE. NO HUMAN FIGURES. NO "
            "FOREGROUND CHARACTERS. Late-afternoon Venetian sky filling the "
            "upper half of the frame in saffron, dusty rose, and pale gold — "
            "substantial empty calm sky in the upper two-thirds of the frame "
            "to leave space for back-cover copy to be overlaid. Composition "
            "is atmospheric, calm, completely empty of figures, and entirely "
            "wordless. Palette: pastel watercolor, warm amber lantern glow, "
            "hints of saffron, terracotta, deep burgundy and indigo shadows. "
            "ABSOLUTELY NO TEXT, NO LETTERS, NO WORDS, NO SPEECH BUBBLES, NO "
            "SIGNS, NO TYPOGRAPHY, NO CAPTIONS, NO WATERMARK, NO BOOK TITLE, "
            "NO ANNOTATIONS, NO LANGUAGE OF ANY KIND ANYWHERE IN THE IMAGE — "
            "this is a pure landscape painting only."
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
