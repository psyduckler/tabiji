#!/usr/bin/env python3
"""Generate 4 editorial-magazine variations for the /books hub redesign.

Building on concept #1 (editorial magazine), explores 4 distinct sub-aesthetics
within the editorial-premium family:
  - Monocle-style "issue cover" front page with dense cover lines
  - Wallpaper*-style minimal single-hero with massive negative space
  - Broadsheet newspaper-opinion multi-column layout
  - Travel-almanac / Baedeker-annual with ornamental rules and TOC feel

Outputs (per concept):
  - Local: /tmp/books-hub-concepts/<slug>.jpg
  - R2:    https://img.tabiji.ai/books/hub-concepts/<slug>.jpg

Usage:
    python3 scripts/book-hub-redesign/generate_editorial_variations.py
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

BRAND = (
    "tabiji.ai Travel Safety Series — 13 pocket-sized Kindle books documenting "
    "tourist scams country by country (Japan 60 scams, Italy 149, France 191, "
    "Thailand 67, Greece 65, Vietnam 66, Spain 103, Indonesia 73, Canada 75, "
    "Germany 88, UK 94, Brazil 72, Portugal 65). Every book $4.99 on Amazon "
    "Kindle. The existing tabiji.ai site uses a warm earthy palette: deep "
    "indigo #2D3A5C, warm cream #F5F0E8, terracotta #C4704B, earth brown "
    "#8B7355, sand #E8DFD0, sage #7A8B6F, deep brown #3E2F23."
)

CONCEPTS: list[dict[str, str]] = [
    {
        "slug": "5-monocle-issue-cover",
        "label": "Monocle-style issue-cover with dense cover lines",
        "prompt": (
            f"{BRAND}\n\n"
            "Design a full landing-page hero mockup for the books hub "
            "rendered as a Monocle-magazine-style issue-cover front page. "
            "Enormous refined sans-serif masthead reading 'TABIJI' in crisp "
            "dark indigo at the very top, with a small italic tagline "
            "underneath: 'A travel-safety quarterly · Issue 13 · Spring 2026'. "
            "A single hero photograph fills the upper two-thirds: a neatly "
            "styled flatlay on warm cream linen — one Kindle-size paperback "
            "of 'ITALY: TOURIST SCAMS' (oxblood cover with gold foil) centered, "
            "surrounded by a passport, a brass compass, a vintage gelato "
            "receipt from Rome, a single train ticket. Overlaid on the "
            "photograph, Monocle-style pull-out 'cover lines' in small "
            "clean sans-serif scattered at the edges — short teasers like "
            "'The 191 scams of France', 'Westminster Bridge, explained', "
            "'Why your Tokyo bar bill was ¥130,000', 'The Venice €2,500-a-"
            "day pickpocket ring', each with a small page-number indicator. "
            "Below the hero, a thin rule and a horizontal strip of 13 tiny "
            "country flag squares with scam counts. Bottom strip: '$4.99 · "
            "AMAZON KINDLE · UPDATED ANNUALLY'. Clean grid, tight tracking, "
            "the meticulous editorial feel of Monocle. Palette: deep indigo, "
            "warm cream, terracotta and muted gold accents. Landscape "
            "1536x1024, browser-chrome-free, polished website screenshot. "
            "Legible English text, correctly spelled."
        ),
    },
    {
        "slug": "6-wallpaper-minimal-single-hero",
        "label": "Wallpaper*-style minimal single-hero with vast negative space",
        "prompt": (
            f"{BRAND}\n\n"
            "Design a full landing-page hero mockup for the books hub in a "
            "minimalist high-end design-magazine aesthetic — the restrained "
            "luxury of Wallpaper*, Apartamento, and Architectural Digest. "
            "80% negative space in warm cream #F5F0E8. A single hero "
            "photograph occupies only the left third of the frame: one "
            "Kindle-size paperback of the JAPAN book (deep indigo cover "
            "with a small Mt. Fuji motif and thin gold rule) photographed "
            "at a slight angle in soft museum-quality lighting, casting a "
            "gentle shadow on the cream surface. The right two-thirds is "
            "nearly empty warm cream space with only: a short Didone serif "
            "headline 'Thirteen countries. Every scam.' set very large, "
            "italic, in deep indigo. A one-line sub-deck in small serif: "
            "'Pocket-sized Kindle books from tabiji.ai.' A single "
            "terracotta button 'Browse the series →'. Below the hero, a "
            "thin horizontal rule and a small 13-item strip of country "
            "names in tiny serif type separated by slim gold dividers "
            "('Japan · Italy · France · Thailand · Greece · Vietnam · Spain "
            "· Indonesia · Canada · Germany · UK · Brazil · Portugal'). "
            "Extreme minimalism, generous air, museum-catalog confidence. "
            "The mockup should look like a polished modern website "
            "screenshot with nothing wasted. Landscape 1536x1024, "
            "browser-chrome-free. Legible English text, correctly spelled."
        ),
    },
    {
        "slug": "7-broadsheet-newspaper-spread",
        "label": "Broadsheet-newspaper editorial-page spread",
        "prompt": (
            f"{BRAND}\n\n"
            "Design a full landing-page hero mockup for the books hub "
            "rendered as a broadsheet-newspaper editorial-page spread — "
            "the rigorously typographic feel of the WSJ Magazine front, "
            "the NYT book review front page, and the Financial Times "
            "weekend edition. Warm cream newsprint background with "
            "subtle paper texture. At the top, a classical engraved "
            "blackletter-style masthead 'TABIJI.AI · TRAVEL SAFETY "
            "QUARTERLY' with thin double rules above and below. A dated "
            "dateline beneath: 'SPRING EDITION · MMXXVI · VOL. XIII'. "
            "Below the masthead, an enormous Didone-serif banner "
            "headline across the full width: 'Thirteen Countries. Every "
            "Scam. One Pocket Guide.' in deep indigo with a smaller "
            "italic dek underneath. The body area splits into three "
            "columns of fine-print justified serif text (placeholder "
            "editorial copy about the series), with a small "
            "black-and-white engraved woodcut illustration of a "
            "pickpocket dropping its catch at the top of column two. "
            "A pull-quote in terracotta italic in column three: '"
            "\"Indispensable intelligence for today's traveler.\" "
            "— Condé Nast Traveler.' Below the columns, a horizontal "
            "'BY COUNTRY' index set like a newspaper classifieds "
            "directory: 13 lines in small serif type listing each "
            "country, its scam count, and a fake page-number, with "
            "small dotted leaders. Thin hairline rules throughout. "
            "The mockup reads like a polished modern website screenshot "
            "built entirely from classical editorial typography. "
            "Landscape 1536x1024, browser-chrome-free. Legible English "
            "text, correctly spelled, historically-accurate newspaper "
            "layout conventions."
        ),
    },
    {
        "slug": "8-baedeker-travel-almanac",
        "label": "Baedeker travel-almanac / vintage guide-annual",
        "prompt": (
            f"{BRAND}\n\n"
            "Design a full landing-page hero mockup for the books hub "
            "rendered as a vintage Baedeker travel-almanac or "
            "Lonely-Planet-annual cover-page, updated with modern web "
            "sensibilities. Warm aged-parchment cream background with "
            "very subtle paper grain and a soft vignette. Centered at "
            "the top, an ornamental gilt-foil serif title in deep indigo "
            "and gold: 'TABIJI.AI' with a decorative fleuron separator, "
            "then below: 'Travel Safety Almanac · MMXXVI Edition'. "
            "Flanked by two small engraved compass-rose vignettes. "
            "Below the title, a large centered italic Didone-serif "
            "headline: 'Thirteen Countries. Every Scam. One Pocket Guide.' "
            "Then a decorative gold rule with a small diamond ornament. "
            "The body: a two-column 'TABLE OF CONTENTS' set in classical "
            "serif type with small-caps country names, dotted leaders, "
            "scam counts, and fake page numbers — each country "
            "(Japan … 60, Italy … 149, France … 191, Thailand … 67, "
            "Greece … 65, Vietnam … 66, Spain … 103, Indonesia … 73, "
            "Canada … 75, Germany … 88, UK … 94, Brazil … 72, Portugal … "
            "65) rendered as a proper chapter listing. A small gilt "
            "fleuron border around each column. At the bottom: an "
            "ornamental gold cartouche containing '$4.99 PER VOLUME · "
            "AMAZON KINDLE · UPDATED ANNUALLY' set in small caps. The "
            "whole page rendered with the warmth and ornamental "
            "confidence of a genuine Victorian/Edwardian travel "
            "almanac, but cleanly readable as a modern website. "
            "Landscape 1536x1024, browser-chrome-free. Legible English "
            "text, correctly spelled, accurate classical typography."
        ),
    },
]


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


def gen_one(concept: dict, ws_token: str, r2_token: str) -> dict:
    slug = concept["slug"]
    out_path = Path(f"/tmp/books-hub-concepts/{slug}.jpg")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    body = {
        "prompt": concept["prompt"],
        "size": "1536x1024",
        "output_format": "jpeg",
    }

    t0 = time.time()
    print(f"[{slug}] submit…", flush=True)
    tid = submit(body, ws_token)
    if not tid:
        return {"slug": slug, "status": "submit_failed"}
    print(f"[{slug}] task {tid} — polling", flush=True)
    url = poll(tid, ws_token)
    if not url:
        return {"slug": slug, "status": "poll_failed"}
    if not download(url, out_path):
        return {"slug": slug, "status": "download_failed", "url": url}
    r2_key = f"books/hub-concepts/{slug}.jpg"
    if not upload_r2(out_path, r2_key, r2_token):
        return {"slug": slug, "status": "r2_upload_failed"}
    elapsed = round(time.time() - t0, 1)
    print(f"[{slug}] ✓ {elapsed}s", flush=True)
    return {
        "slug": slug,
        "label": concept["label"],
        "status": "ok",
        "bytes": out_path.stat().st_size,
        "local": str(out_path),
        "r2": f"https://img.tabiji.ai/{r2_key}",
        "elapsed": elapsed,
    }


def main() -> int:
    ws_token = _keychain("wavespeed-api-key")
    r2_token = _keychain("cloudflare-api-token")

    if not ws_token or not r2_token:
        print("ERROR: missing keychain credentials", file=sys.stderr)
        return 1

    t0 = time.time()
    print(f"generating {len(CONCEPTS)} editorial-style variations with GPT Image 2", flush=True)

    with ThreadPoolExecutor(max_workers=len(CONCEPTS)) as ex:
        results = list(ex.map(lambda c: gen_one(c, ws_token, r2_token), CONCEPTS))

    print(f"\ndone in {time.time()-t0:.0f}s\n", flush=True)
    for r in results:
        print(json.dumps(r, indent=2), flush=True)
    bad = [r for r in results if r["status"] != "ok"]
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
