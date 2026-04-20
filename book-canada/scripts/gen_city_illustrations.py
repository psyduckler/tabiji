#!/usr/bin/env python3
"""
Generate 12 per-city cover illustrations for the Indonesia book via Wavespeed
(Nano Banana Pro).

Style brief — matches Japan/Italy/France/Thailand/Vietnam volume city covers:
  - Flat vector illustration, mid-century travel-book poster aesthetic
  - Warm cream / saffron / burgundy / deep-purple / muted teal palette,
    golden-hour light
  - Tourist figure in deep-burgundy jacket with small backpack, stylised
  - 1:1 aspect, 2K resolution, JPEG

Output: book-indonesia/assets/cities/<slug>.jpg

Usage:
    python3 book-indonesia/scripts/gen_city_illustrations.py               # all 12
    python3 book-indonesia/scripts/gen_city_illustrations.py bali          # one
    python3 book-indonesia/scripts/gen_city_illustrations.py bali lombok   # multiple
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
# Reading order: toronto → niagara-falls → ottawa → montreal → quebec-city →
# halifax → calgary → banff → jasper → whistler → vancouver → victoria-bc
CITIES: list[tuple[str, str, str]] = [
    (
        "toronto",
        "Toronto's skyline at golden hour — the CN Tower and Rogers Centre "
        "silhouetted against a warm orange-amber evening sky, Lake Ontario "
        "reflecting the city lights in the foreground, a single red "
        "TTC streetcar passing in the middle distance, soft late-afternoon "
        "haze, autumn maple leaves drifting across the frame.",
        "m",
    ),
    (
        "niagara-falls",
        "Horseshoe Falls at Niagara in late afternoon, the curved cascade of "
        "water in silvery mist, the Maid of the Mist boat approaching the "
        "base of the falls, the Niagara Parkway and Canadian observation "
        "deck in the foreground, warm golden-hour light, a rainbow catching "
        "in the spray.",
        "f",
    ),
    (
        "ottawa",
        "Parliament Hill in Ottawa at dusk — the Centre Block's Gothic "
        "Revival spires and Peace Tower silhouetted against a warm saffron "
        "sky, the Ottawa River in the foreground, a single RCMP sentry in "
        "red serge beside the Eternal Flame, autumn maple trees, soft "
        "indigo-purple dusk.",
        "m",
    ),
    (
        "montreal",
        "Montreal's Vieux-Port at sunset — the Basilique Notre-Dame's twin "
        "neo-Gothic spires in the middle distance, cobblestone streets of "
        "Old Montreal with warm gas-lamp glow, the St. Lawrence River "
        "reflecting the sky, a horse-drawn calèche passing in the "
        "foreground, early winter soft snow.",
        "f",
    ),
    (
        "quebec-city",
        "Château Frontenac at golden hour, its copper-green mansard roof "
        "and red-brick turrets silhouetted against a warm autumn sky, the "
        "Dufferin Terrace wooden boardwalk along the cliff, the St. "
        "Lawrence River and Île d'Orléans visible below, a single "
        "Quebecois street musician in the foreground.",
        "m",
    ),
    (
        "halifax",
        "Halifax Harbour at golden hour — the Halifax Citadel fortress on "
        "its hill, the historic Town Clock silhouetted, tall-ship masts "
        "along the waterfront boardwalk, a Nova Scotia red-and-white "
        "lighthouse in the middle distance, Maritime fog rolling in, warm "
        "amber late-afternoon light.",
        "f",
    ),
    (
        "calgary",
        "Calgary's skyline at sunset with the Calgary Tower silhouetted "
        "against warm prairie-orange sky, the Canadian Rocky Mountains "
        "visible on the western horizon, a Calgary Stampede cowboy "
        "silhouette at a ranch fence in the foreground, soft chinook-wind "
        "clouds, autumn prairie grass.",
        "m",
    ),
    (
        "banff",
        "Moraine Lake at dawn in Banff National Park — the ten-peaks "
        "ridgeline reflected in perfectly still turquoise glacial water, "
        "pine-forested shoreline, warm pink-gold Rocky Mountain dawn light "
        "breaking over the peaks, a single canoe drawn up on the rocky "
        "shore in the foreground.",
        "f",
    ),
    (
        "jasper",
        "Maligne Lake in Jasper National Park at golden hour with Spirit "
        "Island's iconic trio of pines silhouetted on its small rocky "
        "peninsula, the Canadian Rocky Mountains rising in the distance, "
        "mirror-still lake surface reflecting the peaks, warm late-"
        "afternoon alpine light, misty boreal shoreline.",
        "m",
    ),
    (
        "whistler",
        "Whistler Village at dusk in winter — snow-covered Blackcomb and "
        "Whistler mountain peaks rising above the pedestrian village, "
        "gondolas running across the slopes, warm cabin-window glow from "
        "the chalet-style buildings, lift-lines of skiers descending the "
        "mountain, a soft pink-orange alpine-glow sky.",
        "f",
    ),
    (
        "vancouver",
        "Vancouver's Coal Harbour at sunset — the downtown Vancouver "
        "skyline with Canada Place's white sails, Stanley Park's seawall "
        "and the Lions Gate Bridge in the middle distance, the North Shore "
        "mountains silhouetted beyond, a single kayaker in the foreground, "
        "warm pink-gold Pacific sky.",
        "m",
    ),
    (
        "victoria-bc",
        "Victoria Inner Harbour at golden hour — the British Columbia "
        "Parliament Buildings with their lit outline silhouetted against "
        "a warm evening sky, the historic Fairmont Empress Hotel's ivy-"
        "covered brick facade, a heritage seaplane floating at the dock, "
        "Pacific Dogwood flowers in the foreground, soft West Coast light.",
        "f",
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
