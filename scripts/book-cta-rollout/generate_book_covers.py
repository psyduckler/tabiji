#!/usr/bin/env python3
"""Generate 4 painted illustrated Kindle-style book covers for Brazil, Portugal,
Germany, UK via GPT Image 2 — matching the aesthetic of the existing Japan
and Thailand covers (cream palette, bold serif country name, illustrated
central motif, prominent tabiji.ai masthead).

Saves:
  - Local: books/<country>-tourist-scams/covers/front-designed.jpg
  - R2:    https://img.tabiji.ai/books/<country>-tourist-scams/covers/front-designed.jpg

Usage:
    python3 scripts/book-cta-rollout/generate_book_covers.py
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

GPT2_EP = "https://api.wavespeed.ai/api/v3/openai/gpt-image-2/text-to-image"
RESULT_EP = "https://api.wavespeed.ai/api/v3/predictions/{}/result"

R2_ACCT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"

REPO = Path(__file__).resolve().parents[2]

STYLE_PREAMBLE = (
    "A single portrait book-cover illustration for a Kindle travel-safety "
    "book, in the clean editorial illustrated style of the existing tabiji.ai "
    "Travel Safety Series covers (Japan, Thailand, Italy). Cream paper "
    "background (#F5F0E8), confident bold serif title in deep oxblood "
    "(#3A1A12) or deep indigo (#2D3A5C), a centered stylized illustrated "
    "motif of the country, a gold ornamental rule separator (#D4A12E), a "
    "small tabiji.ai masthead at the top, italic subtitle \"Tourist Scams\" "
    "below the title, and a small hook block at the bottom. Portrait "
    "aspect ratio 2:3 (1024x1536). Legible English text, correctly "
    "spelled. No hashmarks, no generated artifacts, no fake URLs. "
    "Professional Kindle cover design."
)


COVERS: list[dict] = [
    {
        "country": "brazil",
        "title": "BRAZIL",
        "scams": 72,
        "cities": 12,
        "hook": "Don't Lose R$ 1,000 in Brazil",
        "subhook": "Drawn from DEATUR, PROCON, and traveler reports.",
        "motif": (
            "a stylized illustrated silhouette of Christ the Redeemer "
            "standing atop Corcovado mountain with Sugarloaf Mountain "
            "(Pão de Açúcar) visible behind it, palm fronds curling at "
            "the bottom, in warm sunset tones of amber, terracotta, and "
            "forest green. Flat editorial illustration style, confident "
            "line work with soft color wash. No photographic realism."
        ),
        "palette_note": "warm Brazilian sunset — amber #D98C3E, forest green #0B7D3F, cream #F5E6CE",
        "volume": "VOLUME THIRTEEN",
    },
    {
        "country": "portugal",
        "title": "PORTUGAL",
        "scams": 65,
        "cities": 10,
        "hook": "Don't Lose €500 in Portugal",
        "subhook": "Drawn from PSP, ASAE, and real traveler reports.",
        "motif": (
            "a stylized illustrated yellow Lisbon Tram 28 climbing the "
            "cobbled street of Alfama toward São Jorge Castle, with "
            "azulejo blue-and-white tile pattern accents framing the "
            "lower third of the cover. Flat editorial illustration style "
            "with soft color wash, small tram conductor visible in the "
            "window. Warm terracotta rooftops, ochre-washed walls."
        ),
        "palette_note": "Portuguese coastal — ochre #C99A3D, azulejo blue #2E5F8F, cream #F5F0E8",
        "volume": "VOLUME FOURTEEN",
    },
    {
        "country": "germany",
        "title": "GERMANY",
        "scams": 88,
        "cities": 16,
        "hook": "Don't Lose €300 in Germany",
        "subhook": "Drawn from German press and Bundespolizei records.",
        "motif": (
            "a stylized illustrated silhouette of Neuschwanstein Castle "
            "rising from a misty Bavarian alpine forest with pine trees "
            "in the foreground. Flat editorial illustration style with "
            "soft color wash, Gothic castle spires dark against a pale "
            "golden sky, pine-forest greens below."
        ),
        "palette_note": "Bavarian alpine — deep forest green #2E4A2B, warm stone #C9A366, cream #FDF4E3",
        "volume": "VOLUME ELEVEN",
    },
    {
        "country": "united-kingdom",
        "title": "UNITED KINGDOM",
        "scams": 94,
        "cities": 16,
        "hook": "Don't Lose £1,000 in the UK",
        "subhook": "Drawn from British press and Action Fraud records.",
        "motif": (
            "a stylized illustrated silhouette of Big Ben (Elizabeth "
            "Tower) with its clock face centered, a red London "
            "double-decker bus crossing Westminster Bridge in the "
            "foreground, Thames river ripples beneath, and a small "
            "Union Jack pennant flying atop the clock spire. Flat "
            "editorial illustration style with soft color wash, misty "
            "London atmosphere."
        ),
        "palette_note": "London moody — deep navy #0B1F3A, Union red #C8102E, warm gold #D4A12E, cream #F5E9D3",
        "volume": "VOLUME THIRTEEN",
    },
]


def build_prompt(c: dict) -> str:
    return (
        f"{STYLE_PREAMBLE}\n\n"
        f"Book title on the cover: \"{c['title']}\" set in an enormous "
        f"bold display serif (like Playfair Display or Didone). Below the "
        f"title, an italic serif subtitle reading \"Tourist Scams\", then "
        f"a small caps line \"A Traveler's Field Guide · MMXXVI\". At the "
        f"very top, a tabiji.ai masthead reading \"TABIJI.AI\" in small "
        f"caps with wide letter-spacing, a thin gold rule beneath, then "
        f"\"Travel Safety Series\" in small italic, then \"{c['volume']}\" "
        f"in small caps.\n\n"
        f"Central motif: {c['motif']}\n\n"
        f"Palette: {c['palette_note']}.\n\n"
        f"Near the bottom, a small decorative gold-outlined elongated "
        f"hexagon badge containing the numeral \"{c['scams']}\" in large "
        f"serif, with small-caps \"DOCUMENTED SCAMS\" beneath it. Below "
        f"that, two thin gold rules sandwiching a bold hook headline "
        f"\"{c['hook']}\" and italic subhook \"{c['subhook']}\" Then at "
        f"the very bottom of the cover, small caps letter-spaced line "
        f"reading \"{c['cities']} CITIES · 2026 EDITION · BY TABIJI\". "
        f"Portrait orientation 1024x1536, 2:3 aspect ratio, polished "
        f"Kindle cover composition. Legible correctly-spelled English text."
    )


def _keychain(service: str) -> str:
    return subprocess.run(
        ["security", "find-generic-password", "-s", service, "-w"],
        capture_output=True, text=True,
    ).stdout.strip()


def _post(url: str, body: bytes, token: str) -> dict:
    req = urllib.request.Request(url, method="POST", data=body)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def _get(url: str, token: str) -> dict:
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def submit(body: dict, ws_token: str) -> str | None:
    payload = json.dumps(body).encode()
    for attempt in range(5):
        try:
            d = _post(GPT2_EP, payload, ws_token)
            if d.get("code") == 200:
                return d["data"]["id"]
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(3 + attempt * 2)
                continue
            print(f"    submit err: {e}")
            return None
        except Exception as e:
            print(f"    submit exc: {e}")
            return None
    return None


def poll(task_id: str, ws_token: str, timeout: int = 600) -> str | None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            d = _get(RESULT_EP.format(task_id), ws_token)
            data = d["data"]
            if data["status"] == "completed":
                out = data.get("outputs")
                return out[0] if out else None
            if data["status"] == "failed":
                print(f"    prediction failed: {data.get('error')}")
                return None
        except Exception:
            pass
        time.sleep(7)
    return None


def download(url: str, out: Path) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
    except Exception as e:
        print(f"    download err: {e}")
        return False
    out.write_bytes(data)
    if data[:3] != b"\xff\xd8\xff":
        tmp = out.with_suffix(".raw")
        out.rename(tmp)
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "95",
                        str(tmp), "--out", str(out)], capture_output=True, check=True)
        tmp.unlink()
    return True


def upload_r2(src: Path, key: str, r2_token: str) -> bool:
    url = (f"https://api.cloudflare.com/client/v4/accounts/{R2_ACCT}"
           f"/r2/buckets/{R2_BUCKET}/objects/{key}")
    req = urllib.request.Request(url, method="PUT", data=src.read_bytes())
    req.add_header("Authorization", f"Bearer {r2_token}")
    req.add_header("Content-Type", "image/jpeg")
    with urllib.request.urlopen(req, timeout=60) as r:
        return bool(json.loads(r.read()).get("success"))


def gen_one(c: dict, ws_token: str, r2_token: str) -> dict:
    country = c["country"]
    local_path = REPO / "books" / f"{country}-tourist-scams" / "covers" / "front-designed.jpg"
    local_path.parent.mkdir(parents=True, exist_ok=True)

    body = {
        "prompt": build_prompt(c),
        "size": "1024x1536",
        "output_format": "jpeg",
    }

    t0 = time.time()
    print(f"[{country}] submit…", flush=True)
    tid = submit(body, ws_token)
    if not tid:
        return {"country": country, "status": "submit_failed"}
    print(f"[{country}] task {tid} — polling", flush=True)
    url = poll(tid, ws_token)
    if not url:
        return {"country": country, "status": "poll_failed"}
    if not download(url, local_path):
        return {"country": country, "status": "download_failed", "url": url}
    r2_key = f"books/{country}-tourist-scams/covers/front-designed.jpg"
    if not upload_r2(local_path, r2_key, r2_token):
        return {"country": country, "status": "r2_upload_failed"}
    elapsed = round(time.time() - t0, 1)
    print(f"[{country}] ✓ {elapsed}s", flush=True)
    return {
        "country": country,
        "status": "ok",
        "local": str(local_path),
        "r2": f"https://img.tabiji.ai/{r2_key}",
        "bytes": local_path.stat().st_size,
        "elapsed": elapsed,
    }


def main() -> int:
    ws_token = _keychain("wavespeed-api-key")
    r2_token = _keychain("cloudflare-api-token")
    if not ws_token or not r2_token:
        print("ERROR: missing keychain credentials", file=sys.stderr)
        return 1

    t0 = time.time()
    print(f"generating {len(COVERS)} book covers with GPT Image 2 (1024x1536 portrait)",
          flush=True)
    with ThreadPoolExecutor(max_workers=len(COVERS)) as ex:
        results = list(ex.map(lambda c: gen_one(c, ws_token, r2_token), COVERS))

    print(f"\ndone in {time.time()-t0:.0f}s\n", flush=True)
    for r in results:
        print(json.dumps(r, indent=2), flush=True)
    bad = [r for r in results if r["status"] != "ok"]
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
