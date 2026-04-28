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
    "Contemporary illustrated Egyptian travel-comic style: confident fine "
    "black ink outlines with richly digital-painted watercolor-and-gouache "
    "fills, realistic character proportions and expressive faces, visible "
    "painterly texture, soft shadows. Single full-bleed hero scene — NO "
    "panel borders, NO grid layout, NO numbered panels. Palette of "
    "sand-gold, terracotta, Nile-blue, dusty rose, and warm cream. Soft "
    "golden-hour light, visible paper-grain texture. No logos, no "
    "watermarks, no signatures."
)


COVERS = [
    (
        "front",
        (
            "A single dramatic richly-painted watercolor-and-gouache hero "
            "scene, portrait 2:3 aspect, depicting the iconic Egypt tourist "
            "scam in action on the Giza pyramids plateau in late-afternoon "
            "golden raking light. Foreground (lower two-thirds): a female "
            "tourist with shoulder-length brown hair, mid-30s, wearing a "
            "tan canvas sun hat, a pale-blue button-down rolled at the "
            "sleeves, beige hiking trousers, a small leather camera bag at "
            "her hip — standing on the warm golden sand at three-quarter "
            "view, hesitant body language, hand half-raised. Beside her, a "
            "friendly tan-skinned Egyptian camel handler with a short black "
            "beard, mid-30s, in a long ivory galabeya and a crisp white "
            "turban, gesturing with an open hand toward a richly decorated "
            "kneeling camel with red-and-orange tasseled saddle blankets, "
            "small brass bells, embroidered halter. He says \"Free photo, "
            "just one minute!\" in a clean white speech bubble with a small "
            "pointer tail, in clear printed black comic lettering. Both "
            "figures are roughly half the frame height — clearly readable "
            "as the focal subjects, not tiny. Background (upper third): "
            "the three pyramids of Khufu, Khafre, and Menkaure rise as "
            "BOLD warm sandstone silhouettes against a deep saffron-and-"
            "amber sky — substantial, dominant, unmistakably the Pyramids "
            "of Giza, NOT faint or distant. Confident fine black ink "
            "outlines around figures and architecture, richly painted "
            "watercolor-and-gouache fills with visible painterly texture, "
            "soft cast shadows on the sand. Palette: deep saffron, warm "
            "sand-gold, burnt terracotta, deep ochre, Nile-blue mid-shadows, "
            "rich amber sky. Composition reserves a roughly 18%-tall area "
            "of high-contrast sky at the very top edge for a book-cover "
            "title to be overlaid, and the very bottom edge has darker "
            "ground-shadow tones for a hook block. No book title text, no "
            "watermark, no logo, no hieroglyphs, no signature — just the "
            "richly-painted illustration."
        ),
        "2:3",
    ),
    (
        "back",
        (
            "A single quiet richly-painted watercolor-and-gouache landscape "
            "painting, portrait 2:3 aspect, depicting a calm Aswan Nile "
            "scene at golden hour, viewed from a low vantage point on the "
            "sandstone riverbank. A single empty traditional Egyptian "
            "felucca with a tall white triangular sail is moored at a "
            "sandstone Nile bank in the lower foreground; date palms and "
            "the soft silhouette of Elephantine Island rise in the middle "
            "distance; warm amber-and-saffron Nubian sky fills the upper "
            "half. NO PEOPLE. NO HUMAN FIGURES. NO FOREGROUND CHARACTERS. "
            "Substantial empty calm sky in the upper two-thirds of the "
            "frame to leave space for back-cover copy to be overlaid. "
            "Confident fine black ink outlines, richly painted gouache "
            "fills, visible painterly paper-grain texture. Palette: warm "
            "amber sunset glow, sand-gold, terracotta, dusty rose, "
            "Nile-blue and deep indigo shadows. ABSOLUTELY NO TEXT, NO "
            "LETTERS, NO WORDS, NO SPEECH BUBBLES, NO SIGNS, NO TYPOGRAPHY, "
            "NO CAPTIONS, NO WATERMARK, NO BOOK TITLE, NO HIEROGLYPHS, NO "
            "ANNOTATIONS, NO LANGUAGE OF ANY KIND ANYWHERE IN THE IMAGE — "
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
