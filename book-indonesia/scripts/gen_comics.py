#!/usr/bin/env python3
"""
Generate the Indonesia book cover assets via Wavespeed (Nano Banana Pro).

The 73 per-scam comics were already generated in PR #243 (Indonesia
Lontar palm-leaf scam comics) and live on R2 at
`https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`. They are downloaded
into `book-indonesia/assets/scam-comics/` at book-assembly time.

This script only generates the two book covers:
 - front cover (single dramatic Lontar-style scene, 2:3 aspect)
 - back cover (single Lontar-style scene, 2:3, with empty upper portion
   for text overlay)

Style is locked to the project_scam_comics_style_indonesia.md spec —
Balinese Lontar palm-leaf manuscript illustration, fine dark-brown
linework on cream palm-leaf with visible fiber texture.

Usage:
    python3 book-indonesia/scripts/gen_comics.py
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
COVERS_DIR = BOOK / "assets" / "covers"
COVERS_DIR.mkdir(parents=True, exist_ok=True)


STYLE_LONTAR = (
    "A single illustrated cover rendered as a Balinese Lontar palm-leaf "
    "manuscript illustration — fine dark-brown line drawings on pale cream "
    "palm-leaf background with visible leaf-fiber texture, intricate "
    "decorative linework, stylized classical Balinese figures in formal "
    "profile, sparse minimalist ink with architectural and costume details, "
    "subtle ochre-brown accents, ancient manuscript aesthetic with occasional "
    "punched binding-hole motifs at panel edges. Text on the illustration "
    "must be legible English only; speech bubbles if any are clean white "
    "rounded rectangles with thin black borders. No logos, no watermarks, "
    "no signatures."
)

COVERS = [
    (
        "front",
        (
            "A single dramatic Balinese Lontar palm-leaf manuscript scene, "
            "portrait 2:3 aspect, depicting an Indonesia tourist-scam moment: "
            "Priya (age 41, South Asian, shoulder-length brown hair, olive "
            "linen shirt), a female tourist standing at the iconic Uluwatu "
            "cliff temple silhouette with the Indian Ocean behind, while a "
            "friendly-looking Balinese man in a white udeng headdress and "
            "ceremonial sash offers her a small jade pendant and says "
            "'Special price, just for you — 2,000,000 rupiah!' in a white "
            "speech bubble. A small frangipani flower and a traditional "
            "bamboo offering basket sit in the foreground. The scene is "
            "composed to leave generous empty cream-palm-leaf sky in the "
            "upper third of the frame for a book-cover title to be overlaid "
            "later. No book title, no watermark, no logo — just the "
            "illustration."
        ),
        "2:3",
    ),
    (
        "back",
        (
            "A single Balinese Lontar palm-leaf manuscript scene, portrait "
            "2:3 aspect, depicting a bustling Ubud rice-terrace morning from "
            "a three-quarter overhead view: terraced rice paddies stepping "
            "down a hillside, a small stone temple with parasol, palm trees, "
            "a traditional wood gazebo (bale), and a small group of tourists "
            "walking along the edge of a paddy. The scene includes visible "
            "palm-leaf fiber texture and a thin decorative binding-hole motif "
            "at the edges. Composition leaves substantial empty deep-sepia "
            "sky in the upper two-thirds of the frame to leave space for "
            "back-cover copy to be overlaid. No text, no watermark, no book "
            "title."
        ),
        "2:3",
    ),
]


def get_api_key() -> str:
    key = os.environ.get("WAVESPEED_API_KEY")
    if key:
        return key.strip()
    r = subprocess.run(
        ["security", "find-generic-password", "-s", "wavespeed-api-key", "-w"],
        capture_output=True, text=True,
    )
    if r.returncode != 0 or not r.stdout.strip():
        sys.exit("could not read WAVESPEED_API_KEY from keychain or env")
    return r.stdout.strip()


def submit(api_key: str, prompt: str, aspect_ratio: str = "1:1") -> str:
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
    d = r.json()
    return d["data"]["id"] if "data" in d and "id" in d["data"] else d["id"]


def poll(api_key: str, task_id: str, timeout: int = 360) -> str:
    url = f"https://api.wavespeed.ai/api/v3/predictions/{task_id}/result"
    headers = {"Authorization": f"Bearer {api_key}"}
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        body = r.json()
        p = body.get("data", body)
        if p.get("status") == "completed":
            out = p.get("outputs") or p.get("output") or []
            return out if isinstance(out, str) else out[0]
        if p.get("status") == "failed":
            raise RuntimeError(f"task failed: {body}")
        time.sleep(3)
    raise TimeoutError(f"task {task_id} timed out")


def download(url: str, dest: Path) -> None:
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    dest.write_bytes(r.content)


def main() -> None:
    api_key = get_api_key()
    for name, subject, aspect in COVERS:
        dest = COVERS_DIR / f"{name}.jpg"
        if dest.exists():
            print(f"· {name}.jpg exists — skip")
            continue
        prompt = f"{subject}\n\n{STYLE_LONTAR}"
        print(f"→ {name}.jpg: submitting…")
        task = submit(api_key, prompt, aspect)
        out_url = poll(api_key, task)
        download(out_url, dest)
        print(f"✓ {name}.jpg ({dest.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
