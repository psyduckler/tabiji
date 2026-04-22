#!/usr/bin/env python3
"""Generate 4 distinct landing-page hero concepts for the /books hub redesign.

Fires 4 visual-design prompts at GPT Image 2 via Wavespeed, downloads, and
mirrors to R2 so we can review them side-by-side in a browser.

Outputs (per concept):
  - Local: /tmp/books-hub-concepts/<slug>.jpg
  - R2:    https://img.tabiji.ai/books/hub-concepts/<slug>.jpg

Usage:
    python3 scripts/book-hub-redesign/generate_hub_concepts.py
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

# Shared brand context baked into every prompt so concepts stay on-brand.
BRAND = (
    "tabiji.ai Travel Safety Series — 13 pocket-sized Kindle books documenting "
    "tourist scams country by country (Japan, Italy, France, Thailand, Greece, "
    "Vietnam, Spain, Indonesia, Canada, Germany, UK, Brazil, Portugal). Every "
    "book $4.99 on Amazon Kindle. The existing tabiji.ai site uses a warm "
    "earthy palette: deep indigo #2D3A5C, warm cream #F5F0E8, terracotta "
    "#C4704B, earth brown #8B7355, sand #E8DFD0."
)

CONCEPTS: list[dict[str, str]] = [
    {
        "slug": "1-editorial-magazine",
        "label": "Editorial magazine (Condé Nast Traveler / New Yorker)",
        "prompt": (
            f"{BRAND}\n\n"
            "Design a full landing-page hero mockup for the books hub in an "
            "editorial magazine aesthetic — the sophisticated print-publication "
            "feel of Condé Nast Traveler, Monocle, and The New Yorker's travel "
            "issue. Large hero photograph at top of a weathered leather-bound "
            "traveler's notebook, a vintage passport, a fountain pen, and "
            "stacked Kindle-size travel safety books in earthy colors laid on "
            "warm cream linen. Above the hero image: a refined serif masthead "
            "reading 'TABIJI.AI TRAVEL SAFETY SERIES' with a thin gold rule "
            "divider. Below: a bold editorial headline in a Didone serif: "
            "'Thirteen Countries. Every Scam. One Pocket Guide.' Sub-deck in "
            "smaller italic serif: 'Documented from local police records, "
            "national press, and real traveler reports.' Below the hero, a "
            "3×4 grid of small book cover thumbnails with country flags and "
            "scam counts below each (Japan 60, Italy 149, France 191, etc.). "
            "Generous negative space, thin hairline rules, pull-quote sidebar. "
            "Palette: deep indigo #2D3A5C, warm cream #F5F0E8, terracotta "
            "#C4704B accents, muted gold. The whole mockup should look like a "
            "polished website screenshot rendered at browser viewport aspect. "
            "Landscape 1536x1024, browser-chrome-free, photographic realism "
            "combined with crisp editorial typography. Legible English text."
        ),
    },
    {
        "slug": "2-noir-evidence-board",
        "label": "Noir / evidence-board thriller",
        "prompt": (
            f"{BRAND}\n\n"
            "Design a full landing-page hero mockup for the books hub with a "
            "noir detective / scam-investigator aesthetic. Dark moody palette "
            "— midnight navy, oxblood red, warm incandescent lamp light. The "
            "hero is a dimly-lit detective's desk viewed from above: a cork "
            "board in the background pinned with the 13 Kindle book covers "
            "connected by red string, crime-scene-photograph-style polaroids "
            "of pickpockets, taxi meters, forged tickets, and tourist traps "
            "scattered across the desk surface. A manila case-file folder "
            "stamped 'TOURIST SCAMS — CASE CLOSED' sits open with a Kindle "
            "device showing one of the book covers. A brass desk lamp glows "
            "warm. Headline across the top in a condensed noir serif, white "
            "on black: 'KNOW THE SCAM BEFORE IT KNOWS YOU.' Sub-deck in "
            "typewriter font: '1,168 documented scams. 13 countries. "
            "$4.99 each on Amazon Kindle.' Below the hero, a dark strip with "
            "the 13 book covers in a single row, tight spacing, hovering on "
            "a thin red underline. The mockup should read like a cinematic "
            "website screenshot — moody, noir, trustworthy, urgent. "
            "Landscape 1536x1024, browser-chrome-free. Legible English text."
        ),
    },
    {
        "slug": "3-brutalist-travel-poster",
        "label": "Brutalist / Saul Bass travel poster",
        "prompt": (
            f"{BRAND}\n\n"
            "Design a full landing-page hero mockup for the books hub in a "
            "bold brutalist travel-poster aesthetic — the stacked-typography "
            "energy of Saul Bass mid-century movie posters, Swiss "
            "International Style, and 1970s TWA/Pan Am travel posters. Flat "
            "design, no photography, oversized type as the hero. Enormous "
            "stacked headline filling the viewport: the words 'DON'T / LOSE / "
            "€1000 / IN / ROME' (or similar) in a massive condensed bold "
            "sans-serif, each line a different vibrant flat color block "
            "(terracotta, sage green, deep indigo, warm cream, chili red). "
            "Each letter stacked tight, baseline-kissing, filling 80% of the "
            "frame. In one corner a small circular seal: 'TABIJI.AI · TRAVEL "
            "SAFETY SERIES · VOLUME 2 OF 13'. Below the hero, a flat 13-cell "
            "grid of country flag squares — each a solid color block with the "
            "country name in small sans-serif type and a scam count number. "
            "'$4.99 EACH · AMAZON KINDLE · UPDATED ANNUALLY' running across "
            "the bottom as a ticker-style rule. The mockup reads like a "
            "polished modern website screenshot with brutalist typography as "
            "the entire design system. Landscape 1536x1024, browser-"
            "chrome-free. Legible English text, correctly spelled."
        ),
    },
    {
        "slug": "4-warm-bookshop-shelf",
        "label": "Warm indie-bookshop shelf",
        "prompt": (
            f"{BRAND}\n\n"
            "Design a full landing-page hero mockup for the books hub with "
            "the warm, cozy, trustworthy aesthetic of a curated independent "
            "travel bookshop — think Daunt Books Marylebone, Shakespeare and "
            "Company, or a small Kyoto used-book shop. Hero photograph: a "
            "warmly-lit wooden bookshelf viewed head-on, filled with the 13 "
            "tabiji.ai Travel Safety Series Kindle-size paperbacks standing "
            "upright, spines facing out, each spine a different country "
            "color (Japan indigo, Italy oxblood, France cream, etc.) with "
            "the country name in a refined serif running vertically up the "
            "spine. Handwritten paper shelf-talkers tucked between books "
            "with small typewriter-style notes ('staff pick', 'bestseller', "
            "'new for 2026'). A brass reading lamp glows warm, a steaming "
            "mug of coffee sits on a nearby stack, a tabiji.ai owl logo "
            "chalk-lettered on a small slate sign propped against the "
            "shelf. Above the shelf, a hand-lettered wooden sign reading "
            "'THIRTEEN COUNTRIES · THIRTEEN POCKET GUIDES.' Below the "
            "hero: a wide tan-paper strip with the line 'A growing series "
            "of pocket-sized Kindle books documenting tourist scams, "
            "country by country.' and three small category pills ('Browse "
            "by region', 'What's inside', 'FAQ'). The mockup should look "
            "like a polished modern website screenshot — warm, inviting, "
            "bookish, trustworthy, quietly premium. Landscape 1536x1024, "
            "browser-chrome-free, photographic realism. Legible English "
            "text, correctly spelled."
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
    # GPT Image 2 may return PNG — convert to JPEG via sips if needed
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
    print(f"generating {len(CONCEPTS)} landing-page concepts with GPT Image 2", flush=True)

    with ThreadPoolExecutor(max_workers=len(CONCEPTS)) as ex:
        results = list(ex.map(lambda c: gen_one(c, ws_token, r2_token), CONCEPTS))

    print(f"\ndone in {time.time()-t0:.0f}s\n", flush=True)
    for r in results:
        print(json.dumps(r, indent=2), flush=True)
    bad = [r for r in results if r["status"] != "ok"]
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
