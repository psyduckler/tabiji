#!/usr/bin/env python3
"""
Generate 16 per-city cover illustrations for the China book via Wavespeed
(Nano Banana Pro).

Style brief — matches the prior volumes' city covers for series consistency:
  - Flat vector illustration, mid-century travel-book poster aesthetic
  - Warm cream / saffron / burgundy / deep-purple / muted teal palette,
    golden-hour light
  - Tourist figure in deep-burgundy jacket with small backpack, stylised
  - 1:1 aspect, 2K resolution, JPEG

Output: book-china/assets/cities/<slug>.jpg

Usage:
    python3 book-china/scripts/gen_city_illustrations.py              # all 16 cities
    python3 book-china/scripts/gen_city_illustrations.py beijing       # just beijing
    python3 book-china/scripts/gen_city_illustrations.py beijing xian
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
OUT = BOOK / "assets" / "cities"
OUT.mkdir(parents=True, exist_ok=True)

STYLE_BASE = (
    "Flat vector travel-poster illustration in mid-century style. "
    "Warm cream background, palette of saffron-gold, deep burgundy, "
    "dusty purple and muted teal. Soft golden-hour light. "
    "Clean geometric shapes, visible paper-grain texture, "
    "no text, no words, no logos, no watermark. "
    "Square 1:1 composition, gentle depth, soft shadows."
)

TRAVELER_M = (
    "One stylised solo male traveler, short dark hair, wearing a "
    "deep-burgundy jacket and a small backpack, seen from behind or "
    "three-quarter view, looking toward the scene. "
)

TRAVELER_F = (
    "One stylised solo female traveler, shoulder-length dark hair, "
    "wearing a deep-burgundy jacket and a small backpack, seen from "
    "behind or three-quarter view, looking toward the scene. "
)

# (slug, subject, gender) — manuscript reading order; alternating gender.
CITIES: list[tuple[str, str, str]] = [
    (
        "beijing",
        "The glazed golden-tiled rooftops of the Forbidden City seen from Jingshan "
        "Park in late afternoon, the central axis of Beijing stretching south with "
        "the silhouette of the Drum Tower in the middle distance, a single cypress "
        "tree in the foreground, warm Beijing haze on the horizon.",
        "f",
    ),
    (
        "shanghai",
        "The Bund waterfront of Shanghai at golden hour, the neoclassical 1920s "
        "stone buildings on the west bank with the futuristic Pudong skyline of the "
        "Oriental Pearl Tower and Shanghai Tower rising across the Huangpu River, "
        "warm peach twilight sky, a single barge on the water.",
        "m",
    ),
    (
        "xian",
        "The medieval city wall of Xi'an at golden hour, the tiled South Gate "
        "pavilion with upturned eaves above a crenelated wall, bicycles passing "
        "along the top of the wall in silhouette, warm ochre stone, a single "
        "red lantern hanging in the archway.",
        "f",
    ),
    (
        "chengdu",
        "A giant panda sitting in a bamboo grove at the Chengdu Research Base of "
        "Giant Panda Breeding, warm morning mist filtering through green bamboo, "
        "soft dappled light on the panda's black-and-white fur, Sichuan basin "
        "hills in the distance.",
        "m",
    ),
    (
        "chongqing",
        "The Hongya Cave stilt-house complex on the Yangtze River cliff face at "
        "twilight, ochre wooden pavilions stacked in terraces illuminated by warm "
        "lantern glow, the confluence of the Jialing and Yangtze rivers in the "
        "middle distance, a single passing ferry.",
        "f",
    ),
    (
        "guangzhou",
        "The slim spire of the Canton Tower rising above the Pearl River at blue "
        "hour, illuminated violet-to-blue along its latticed steel structure, a "
        "distant skyline of Pearl River New Town, a small river boat in the "
        "foreground, warm evening haze.",
        "m",
    ),
    (
        "shenzhen",
        "The Ping An Finance Center supertall tower rising above Shenzhen Bay at "
        "late afternoon, the modernist curves of the Shenzhen Bay Sports Center "
        "in the middle distance, palm trees along a promenade in the foreground, "
        "warm Cantonese coastal light.",
        "f",
    ),
    (
        "hangzhou",
        "The Leifeng Pagoda rising above West Lake at golden hour, a single "
        "willow-lined arched stone bridge (the Broken Bridge) crossing the water "
        "in the middle distance, lotus leaves floating in the foreground, warm "
        "misty late-afternoon light over the Jiangnan hills.",
        "m",
    ),
    (
        "suzhou",
        "A moon-gate and a weeping-willow branch framing a quiet canal inside the "
        "Humble Administrator's Garden in Suzhou at golden hour, a slim white-washed "
        "pavilion with upturned black-tiled roof reflected in still water, koi fish "
        "visible below, warm Jiangnan light.",
        "f",
    ),
    (
        "guilin",
        "Karst limestone peaks rising dramatically from a mist-covered Li River at "
        "dawn, a single bamboo fishing raft crossing the water in the foreground, "
        "warm silver-grey morning haze shading into saffron at the horizon, "
        "painterly brush-style stylised composition.",
        "m",
    ),
    (
        "yangshuo",
        "A cormorant fisherman with his trained birds on a bamboo raft on the Li "
        "River at sunset, flanked by the iconic karst peaks of Yangshuo, warm "
        "peach-gold evening sky reflected on the water, a single rice paddy in "
        "the foreground.",
        "f",
    ),
    (
        "lijiang",
        "A stone-paved lane in Lijiang Old Town at twilight, flanked by Naxi "
        "traditional wooden storefronts with upturned eaves, a narrow canal with "
        "water running alongside the path, lanterns beginning to glow warm in the "
        "fading dusk, Jade Dragon Snow Mountain silhouetted in the distance.",
        "m",
    ),
    (
        "kunming",
        "The Stone Forest of Shilin outside Kunming at golden hour, towering "
        "karst limestone pinnacles eroded into blade-like formations, a narrow "
        "path winding between them, warm Yunnan sun casting long shadows, a "
        "distant view of the Yunnan-Guizhou Plateau.",
        "f",
    ),
    (
        "pingyao",
        "The Ming-dynasty grey-brick city wall of Pingyao at sunset, the corner "
        "watchtower with upturned eaves silhouetted against a warm saffron sky, "
        "the tiled rooftops of the ancient town stretching to the horizon, a "
        "single red lantern hanging from a gate.",
        "m",
    ),
    (
        "harbin",
        "The green-domed Saint Sophia Cathedral of Harbin in winter snow, its "
        "red-brick Russian Orthodox facade dusted with white, a gentle snowfall "
        "in the air, warm amber streetlamp light, a single figure in a fur hat "
        "crossing the empty square in the foreground.",
        "f",
    ),
    (
        "zhangjiajie",
        "The towering sandstone pillars of Zhangjiajie National Forest Park rising "
        "out of a sea of morning clouds, pine trees clinging to their cliff tops, "
        "warm saffron light catching the peaks from the east, misty blue-grey "
        "valleys below.",
        "m",
    ),
]


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
    r = requests.post(url, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }, json={
        "prompt": prompt,
        "aspect_ratio": "1:1",
        "resolution": "2k",
        "output_format": "jpeg",
    }, timeout=60)
    r.raise_for_status()
    data = r.json()
    if "data" in data and "id" in data["data"]:
        return data["data"]["id"]
    if "id" in data:
        return data["id"]
    raise RuntimeError(f"unexpected submit response: {data}")


def poll(api_key: str, task_id: str, timeout: int = 300) -> str:
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
    filter_slugs = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    cities = [c for c in CITIES if not filter_slugs or c[0] in filter_slugs]
    if not cities:
        sys.exit(f"no cities matched {filter_slugs}. valid slugs: {[c[0] for c in CITIES]}")

    api_key = get_api_key()
    errors: list[tuple[str, str]] = []
    for slug, subject, gender in cities:
        dest = OUT / f"{slug}.jpg"
        if dest.exists() and not filter_slugs:
            print(f"· {slug}: already exists ({dest.stat().st_size / 1024:.0f} KB) — skipping")
            continue
        traveler = TRAVELER_F if gender == "f" else TRAVELER_M
        prompt = f"{subject} {traveler}{STYLE_BASE}"
        try:
            print(f"→ {slug}: submitting…")
            task = submit(api_key, prompt)
            print(f"  task {task}; polling…")
            out_url = poll(api_key, task, timeout=360)
            download(out_url, dest)
            print(f"✓ {slug}: saved {dest.name} ({dest.stat().st_size / 1024:.0f} KB)")
        except Exception as e:
            print(f"✗ {slug}: {e}", file=sys.stderr)
            errors.append((slug, str(e)))
    if errors:
        print("\nerrors:")
        for s, e in errors:
            print(f"  {s}: {e}")
        sys.exit(1)
    print(f"\ndone. images in {OUT}")


if __name__ == "__main__":
    main()
