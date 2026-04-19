#!/usr/bin/env python3
"""
Generate 11 per-city cover illustrations for the Vietnam book via Wavespeed
(Nano Banana Pro).

Style brief — matches Japan/Italy/France/Thailand volume city covers:
  - Flat vector illustration, mid-century travel-book poster aesthetic
  - Warm cream / saffron / burgundy / deep-purple / muted teal palette,
    golden-hour light
  - Tourist figure in deep-burgundy jacket with small backpack, stylised
  - 1:1 aspect, 2K resolution, JPEG

Output: book-vietnam/assets/cities/<slug>.jpg

Usage:
    python3 book-vietnam/scripts/gen_city_illustrations.py              # all 11
    python3 book-vietnam/scripts/gen_city_illustrations.py hanoi        # one
    python3 book-vietnam/scripts/gen_city_illustrations.py hanoi hue    # multiple
"""
from __future__ import annotations

import concurrent.futures
import os
import subprocess
import sys
import time
from pathlib import Path

import requests  # noqa: pip install requests


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

# (slug, subject, gender) — alternating m/f within reading order.
# Reading order: hanoi → ha-long-bay → sapa → hue → hoi-an → da-nang →
# nha-trang → dalat → ho-chi-minh-city → can-tho → phu-quoc
CITIES: list[tuple[str, str, str]] = [
    (
        "hanoi",
        "Hanoi's Old Quarter at golden hour — a narrow street of yellow-ochre "
        "French-colonial facades with wooden shutters, red paper lanterns "
        "strung between balconies, a pho cart with steam rising, the "
        "silhouette of the One Pillar Pagoda in the middle distance, warm "
        "saffron evening sky.",
        "m",
    ),
    (
        "ha-long-bay",
        "Ha Long Bay karst limestone islands rising out of jade-green water "
        "in the late afternoon, a traditional wooden junk boat with "
        "russet-red sails silhouetted against the dramatic karst cliffs, "
        "soft mist between the peaks, warm golden light.",
        "f",
    ),
    (
        "sapa",
        "Terraced rice fields of Sapa cascading down a misty mountainside, "
        "small H'mong village houses nestled into the slopes, the Hoang Lien "
        "Son mountain range rising in the distance, Fansipan peak in silhouette, "
        "warm late-afternoon light breaking through the clouds.",
        "m",
    ),
    (
        "hue",
        "The Perfume River at dusk with the Thien Mu Pagoda's seven-tiered "
        "octagonal tower silhouetted on the far bank, a traditional dragon "
        "boat drifting in the foreground, soft reflection of the warm "
        "saffron sky on the water, gentle mountain silhouettes beyond.",
        "f",
    ),
    (
        "hoi-an",
        "Hoi An Ancient Town at night — the Japanese Covered Bridge lit by "
        "warm lantern-glow, wooden shop-house facades along the canal, "
        "colorful silk lanterns floating on the water, stylised couple "
        "releasing a single paper lantern, deep-indigo twilight sky.",
        "m",
    ),
    (
        "da-nang",
        "Da Nang's Dragon Bridge (Cau Rong) arching across the Han River "
        "at dusk, its dragon head lit warm gold, distant My Khe Beach "
        "curve and Marble Mountains silhouette, a long-tail fishing boat "
        "on the water in the foreground, warm evening light.",
        "f",
    ),
    (
        "nha-trang",
        "Nha Trang's long crescent beach at sunset, Po Nagar Cham Towers "
        "silhouetted on the headland, palm trees along the Tran Phu "
        "seafront promenade, turquoise South China Sea water, warm "
        "pink-gold sky, a few fishing boats anchored in the shallows.",
        "m",
    ),
    (
        "dalat",
        "Dalat's misty pine-forest highlands at dawn, the pastel colonial "
        "Cremaillere railway station and its steam locomotive in the middle "
        "distance, Xuan Huong Lake mirror-calm in the foreground, warm "
        "morning light breaking through the pines, crisp highland air.",
        "f",
    ),
    (
        "ho-chi-minh-city",
        "Ho Chi Minh City's Notre-Dame Cathedral Basilica with its twin red-brick "
        "spires at golden hour, the Saigon Central Post Office's yellow-ochre "
        "colonial facade beside it, a swarm of motorbikes passing in the "
        "foreground, warm saffron late-afternoon sky.",
        "m",
    ),
    (
        "can-tho",
        "Cai Rang floating market at dawn on the Mekong Delta, wooden sampan "
        "boats piled with pineapples, watermelons and dragonfruit, river mist, "
        "the silhouette of a larger trader boat with a tall bamboo pole "
        "showing its goods, warm misty sunrise light on the water.",
        "f",
    ),
    (
        "phu-quoc",
        "Phu Quoc's west-coast beach at sunset — Sao Beach's curve of white "
        "sand meeting turquoise Gulf-of-Thailand water, coconut palms "
        "silhouetted against a vivid pink-orange sky, a single traditional "
        "fishing basket-boat anchored offshore.",
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
    r = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "prompt": prompt,
            "aspect_ratio": "1:1",
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


def generate_one(api_key: str, slug: str, subject: str, gender: str) -> tuple[str, bool, str]:
    dest = OUT / f"{slug}.jpg"
    traveler = TRAVELER_F if gender == "f" else TRAVELER_M
    prompt = f"{subject} {traveler}{STYLE_BASE}"
    try:
        task = submit(api_key, prompt)
        out_url = poll(api_key, task, timeout=360)
        download(out_url, dest)
        return (slug, True, f"{dest.stat().st_size / 1024:.0f} KB")
    except Exception as e:
        return (slug, False, str(e))


def main() -> None:
    filter_slugs = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    cities = [c for c in CITIES if not filter_slugs or c[0] in filter_slugs]
    if not cities:
        sys.exit(f"no cities matched {filter_slugs}. valid slugs: {[c[0] for c in CITIES]}")

    api_key = get_api_key()

    todo = []
    for slug, subject, gender in cities:
        dest = OUT / f"{slug}.jpg"
        if dest.exists() and not filter_slugs:
            print(f"· {slug}: exists ({dest.stat().st_size / 1024:.0f} KB) — skip")
            continue
        todo.append((slug, subject, gender))

    if not todo:
        print("· nothing to generate")
        return

    print(f"→ Generating {len(todo)} city illustrations (6 workers)…")
    errors = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(generate_one, api_key, s, sub, g): s for s, sub, g in todo}
        for fut in concurrent.futures.as_completed(futures):
            slug, ok, info = fut.result()
            if ok:
                print(f"  ✓ {slug}: {info}")
            else:
                print(f"  ✗ {slug}: {info}", file=sys.stderr)
                errors.append((slug, info))
    if errors:
        sys.exit(1)
    print(f"\ndone. images in {OUT}")


if __name__ == "__main__":
    main()
