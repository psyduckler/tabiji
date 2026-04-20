#!/usr/bin/env python3
"""
Generate the Canada book cover assets via Wavespeed (Nano Banana Pro).

The 75 per-scam comics were already generated in PR #246 (Canada
Drawn & Quarterly scam comics) and live on R2 at
`https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`. They are downloaded
into `book-canada/assets/scam-comics/` at book-assembly time.

This script only generates the two book covers, matching the locked
Canada style block (Drawn & Quarterly Toronto indie-comic — Seth /
Chester Brown / Michael DeForge).

Usage:
    python3 book-canada/scripts/gen_comics.py
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


STYLE_DNQ = (
    "A single illustrated cover in the Toronto indie-comic style of "
    "Drawn & Quarterly artists (Seth, Chester Brown, Michael DeForge) — "
    "clean precise black ink outlines with quiet duotone pencil hatching, "
    "muted palette of cream paper and olive-teal wash, understated "
    "quietly-melancholic tone, nostalgic mid-century Canadian small-town "
    "sensibility, thoughtful composition, subtle spot-blacks, refined "
    "comic-book-as-literature feel. Text on the illustration must be "
    "legible English only; speech bubbles if any are clean white rounded "
    "rectangles with thin black borders. No logos, no watermarks, no "
    "signatures."
)

COVERS = [
    (
        "front",
        (
            "A single dramatic Toronto indie-comic scene in the Drawn & "
            "Quarterly style, portrait 2:3 aspect, depicting a Canada "
            "tourist-scam moment: Priya (age 34, South Asian, shoulder-"
            "length brown hair, olive linen shirt and warm jacket), a "
            "female tourist standing outside Toronto's Union Station under "
            "the CN Tower silhouette, while a man in a dark coat and toque "
            "holds up a phone screen that looks like a taxi app and says "
            "'Got a ride waiting, $60 fixed to your hotel!' in a white "
            "speech bubble. Soft falling snow, a streetcar passing in the "
            "background, warm evening light, quiet understated mood. "
            "Generous empty cream sky in the upper third for a book-cover "
            "title to be overlaid later. No book title, no watermark, no "
            "logo — just the illustration."
        ),
        "2:3",
    ),
    (
        "back",
        (
            "A single Toronto indie-comic scene in the Drawn & Quarterly "
            "style, portrait 2:3 aspect, depicting a quiet winter evening "
            "at Montreal's Old Port: cobblestone streets with soft snow, "
            "ornate grey stone facades of the Vieux-Montréal district, "
            "the Notre-Dame Basilica's silhouette in the middle distance, "
            "a lone cyclist and a small group of tourists walking under "
            "warm gas-lamp glow, quiet duotone olive-teal wash over cream "
            "paper. Composition leaves substantial empty deep-sepia sky "
            "in the upper two-thirds of the frame for back-cover copy to "
            "be overlaid. No text, no watermark, no book title."
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
        prompt = f"{subject}\n\n{STYLE_DNQ}"
        print(f"→ {name}.jpg: submitting…")
        task = submit(api_key, prompt, aspect)
        out_url = poll(api_key, task)
        download(out_url, dest)
        print(f"✓ {name}.jpg ({dest.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
