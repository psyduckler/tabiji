#!/usr/bin/env python3
"""Generate the front and back cover paintings for the Costa Rica book.

Uses the locked tico naïf primitivist tropical-painting style (selected
2026-04-27 via 5-way bake-off) but as a single full-bleed scene rather than
the 4-panel comic grid used for per-scam comics.

  - front.jpg: Manuel Antonio fake-park-ranger Route 618 roadblock
               (Margie × the headline Costa Rica scam, with speech bubble)
  - back.jpg:  Arenal Volcano + rainforest atmospheric backdrop
               (no characters, no speech bubble — pure setting, the dim
               overlay carries back-cover copy)

Output: book-costa-rica/assets/svg/front.jpg and back.jpg

Usage:
    python3 book-costa-rica/scripts/gen_cover_paintings.py
    python3 book-costa-rica/scripts/gen_cover_paintings.py front
    python3 book-costa-rica/scripts/gen_cover_paintings.py back
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
OUT = BOOK / "assets" / "svg"
OUT.mkdir(parents=True, exist_ok=True)

TICO_NAIF_STYLE = (
    "Painted in the lush Costa Rican naïf primitivist tropical-painting "
    "tradition — saturated tropical rainforest alive with biodiversity, "
    "bold flat hand-painted shapes with confident black outline, layered "
    "green canopy of emerald, lime, sage, and jungle-shadow teal, accents "
    "of macaw scarlet, toucan yellow, hibiscus pink, and Pacific cobalt, "
    "decorative heart-of-palm fronds and bromeliads at scene edges, hidden "
    "sloths, frogs, and toucans tucked into the foliage as joyful Easter "
    "eggs, naive-folk figure proportions with friendly oversized eyes and "
    "simple expressive faces, dense joyful 'pura vida' tico storybook "
    "composition with every surface filled with hand-painted biodiversity, "
    "warm equatorial sunlight. A single full-bleed illustrated scene "
    "(NOT a comic page, NO panels, NO grid, NO panel borders). "
    "Portrait composition with strong vertical depth, painterly brushwork. "
    "No watermark, no logos, no extra text or numbers anywhere outside "
    "the explicit speech bubble."
)

MARGIE = (
    "A 62-year-old Western woman with shoulder-length silver-gray hair "
    "worn under a woven straw sun hat with a cream ribbon, warm blue eyes "
    "behind tortoiseshell reading glasses often perched on her head, light "
    "olive complexion with gentle laugh lines and a friendly curious "
    "expression. She wears a cream linen blouse, tan wide-leg travel "
    "pants, and white canvas sneakers, with a small tan leather crossbody "
    "bag and a coral scarf. Gracious, cheerful, a little too trusting."
)

SCENES: dict[str, str] = {
    "front": (
        f"A Manuel Antonio fake park-ranger roadblock scam scene on Costa "
        f"Rican Route 618 near the entrance to Manuel Antonio National "
        f"Park. CHARACTER: {MARGIE} She stands beside a small parked "
        f"rental sedan on a narrow jungle road, hand at her chin in "
        f"hesitation. A local man in a fake official-looking olive-green "
        f"vest with a clipboard blocks the road in front of her, gesturing "
        f"officiously. The dense Manuel Antonio rainforest canopy presses "
        f"in on both sides — emerald and lime greens, heliconia flowers, "
        f"a sloth tucked into the upper foliage, a scarlet macaw on a "
        f"branch, a tiny red poison-dart frog on a leaf in the foreground. "
        f"Pacific Ocean glimpsed through a gap in the trees. Warm "
        f"equatorial light. ONE clean white rounded speech bubble emerging "
        f"from the fake ranger's mouth, with a small pointer tail, holding "
        f'this short printed English dialogue in simple black comic '
        f'lettering — text must be legible, in English only, and correctly '
        f'spelled: "Park closed — $40 access fee." '
    ),
    "back": (
        "A serene Costa Rican rainforest landscape scene at golden hour, "
        "no people, no characters. Arenal Volcano rises in the middle "
        "distance — a perfect symmetrical cone with a wisp of cloud at "
        "the summit, warm volcanic-rock browns catching late afternoon "
        "light. The foreground and middle ground are dense Caribbean-slope "
        "rainforest in layered emerald, lime, and jungle-shadow teal, "
        "with heart-of-palm fronds and bromeliads framing the scene. "
        "Hidden biodiversity Easter eggs — a three-toed sloth in the "
        "upper canopy, a keel-billed toucan on a branch, a red-eyed tree "
        "frog on a heliconia leaf, blue morpho butterflies drifting through "
        "the middle distance. A small thermal stream curls toward the "
        "viewer in the foreground. Warm equatorial sunlight bathing the "
        "canopy from the upper right. NO speech bubbles, NO text, NO "
        "people, NO buildings — pure tropical atmosphere. "
    ),
}


def get_api_key() -> str:
    key = os.environ.get("WAVESPEED_API_KEY")
    if key:
        return key.strip()
    result = subprocess.run(
        ["security", "find-generic-password", "-s", "wavespeed-api-key", "-w"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        sys.exit("could not read WAVESPEED_API_KEY from keychain or env")
    return result.stdout.strip()


def submit(api_key: str, prompt: str) -> str:
    url = "https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image"
    r = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "prompt": prompt,
            # 9:16 is the closest portrait ratio to the SVG's 5:8 viewbox; the
            # SVG uses preserveAspectRatio="xMidYMid slice" so the image will
            # be center-cropped to fit anyway.
            "aspect_ratio": "9:16",
            "resolution": "2k",
            "output_format": "jpeg",
        },
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    if "data" in data and "id" in data["data"]:
        return data["data"]["id"]
    if "id" in data:
        return data["id"]
    raise RuntimeError(f"unexpected submit response: {data}")


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
    targets = sys.argv[1:] or list(SCENES.keys())
    invalid = [t for t in targets if t not in SCENES]
    if invalid:
        sys.exit(f"unknown target(s): {invalid}. valid: {list(SCENES.keys())}")

    api_key = get_api_key()
    for name in targets:
        dest = OUT / f"{name}.jpg"
        prompt = f"{SCENES[name]} {TICO_NAIF_STYLE}"
        print(f"→ {name}: submitting…")
        task = submit(api_key, prompt)
        print(f"  task {task}; polling…")
        out_url = poll(api_key, task, timeout=420)
        download(out_url, dest)
        print(f"✓ {name}: saved {dest.name} ({dest.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
