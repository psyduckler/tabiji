#!/usr/bin/env python3
"""Generate 5 Malaysian comic-style candidates × 2 image models for comparison.

Fires the same 5 style prompts at:
  - Nano Banana Pro (Google)         — /api/v3/google/nano-banana-pro/text-to-image
  - GPT Image 2 (OpenAI)             — /api/v3/openai/gpt-image-2/text-to-image

Test scene: Priya at Kuala Lumpur International Airport (KLIA2) being hustled
by an unofficial "teksi sapu" tout while the legitimate Coupon Taxi counter
is steps away.

Outputs (both models, 5 styles each = 10 images):
  - Local: /tmp/malaysia-style-tests/<slug>-<model>.jpg
  - R2:    https://img.tabiji.ai/scam-comics/my/style-tests/<slug>-<model>.jpg
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from cast import CHARACTERS  # noqa: E402

NB2_EP = "https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image"
GPT2_EP = "https://api.wavespeed.ai/api/v3/openai/gpt-image-2/text-to-image"
RESULT_EP = "https://api.wavespeed.ai/api/v3/predictions/{}/result"

R2_ACCT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"

CHARACTER = CHARACTERS["priya"]

SCENE_SCRIPT = """CHARACTER (appears in every panel, consistent across all four):
""" + CHARACTER + """

SCAM CONTEXT: Kuala Lumpur International Airport (KLIA2) unofficial "teksi sapu" taxi overcharge — unlicensed drivers intercept arrivals with inflated fares while the official authorized Coupon Taxi counter sells pre-paid tickets steps away.

PANEL 1 — Just past the KLIA2 arrivals customs door. A man in a polo shirt holding a handwritten "TAXI — HOTEL" cardboard sign waves at Priya. Malaysian airport signage visible (bilingual English/Malay). SPEECH BUBBLE: "Taxi madam? One hundred fifty!"

PANEL 2 — Priya glances past him and sees a clearly-marked "COUPON TAXI — TEKSI KUPON RASMI" counter inside the terminal with a posted fare board showing "KL SENTRAL: RM 74.30". She points at it with her phone. SPEECH BUBBLE: "The official counter is right there."

PANEL 3 — Priya at the authorized Coupon Taxi counter, a uniformed clerk hands her a pre-paid taxi voucher. The posted rate card shows RM 74.30 for KL Sentral. SPEECH BUBBLE: "Seventy-four ringgit — half the price."

PANEL 4 — Priya in the back of a blue-and-white official Teksi 1Malaysia with a visible meter and driver ID card on the dash, heading toward the KL skyline. SPEECH BUBBLE: "Always the kaunter rasmi, never the curb."
"""

STYLES: list[dict[str, str]] = [
    {
        "slug": "1-lat-kampung-boy-cartoon",
        "label": "Lat (Mohammad Nor Khalid) Kampung Boy cartoonist",
        "prompt": (
            "A single illustrated comic book page in the warm hand-drawn newspaper-"
            "cartoon style of Mohammad Nor Khalid (known as Lat), the beloved "
            "Malaysian cartoonist behind 'Kampung Boy' and the New Straits Times "
            "editorial cartoons — confident hand-drawn black-ink linework with "
            "rich cross-hatched shadow, gentle humor, rounded soft-figured people "
            "with big expressive eyes and small smiles, everyday-Malaysian-life "
            "observational tone, warm off-white paper background with subtle "
            "newsprint texture, occasional light watercolor wash in pale lemon, "
            "muted chili red, and soft banana yellow. Showing four sequential "
            "panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the "
            "upper-left corner of each panel, separated by thin hand-drawn black "
            "panel borders with narrow cream gutters. Each panel contains one "
            "clean white rounded speech bubble with a small pointer tail, holding "
            "short printed English dialogue in simple black hand-lettered text — "
            "text must be legible, in English only, and correctly spelled. Square "
            "1:1 composition, 2K resolution."
        ),
    },
    {
        "slug": "2-batik-bordered-travel-comic",
        "label": "Batik-bordered contemporary Malaysian travel comic",
        "prompt": (
            "A single illustrated comic book page framed inside an ornate Malaysian "
            "batik-motif border — rich decorative batik rim in deep indigo, turmeric "
            "gold, crimson, and cream, with stylized parang (dagger-diagonal), "
            "kawung (four-petal medallion), and mega mendung (cloud) patterns drawn "
            "as flat dyed-fabric shapes. Interior of each panel rendered in a warm "
            "contemporary illustrated-travel-comic style: confident fine black ink "
            "outlines with richly-painted watercolor and gouache fills, a warm "
            "tropical palette of parchment cream, banana yellow, chili red, palm "
            "green, teak brown, and turquoise, detailed Malaysian urban and rural "
            "backgrounds (KL skyline, Petronas Towers, kampung wooden stilt houses, "
            "kopitiam shopfronts, batik stalls), travelers in modern casual "
            "clothing alongside Malaysian characters in baju melayu, songkok, or "
            "sarong, storybook-rich composition with visible painterly texture. "
            "Showing four sequential panels arranged in a 2x2 grid with small "
            "numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated "
            "by thin cream gutters inside the batik border. Each panel contains "
            "one clean white rounded speech bubble with a small pointer tail, "
            "holding short printed English dialogue in simple black comic "
            "lettering — text must be legible, in English only, and correctly "
            "spelled. Square 1:1 composition, 2K resolution."
        ),
    },
    {
        "slug": "3-wayang-kulit-shadow-puppet",
        "label": "Wayang kulit shadow-puppet theatre",
        "prompt": (
            "A single illustrated comic book page rendered as traditional Malay "
            "wayang kulit shadow-puppet storytelling — figures rendered as "
            "silhouetted dalang-carved leather puppets in deep sepia-black and "
            "burnt umber against a warm amber-and-ochre backlit parchment "
            "background, with intricately fretwork-carved figure edges and "
            "decorative flourishes, stylized tropical vegetation silhouettes in "
            "the foreground, subtle flickering-lamp warmth, classical Kelantanese "
            "shadow-play aesthetic merged with a modern sequential-comic layout. "
            "Showing four sequential panels arranged in a 2x2 grid with small "
            "numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated "
            "by thin dark-brown panel borders with narrow amber gutters. Each "
            "panel contains one clean white rounded speech bubble with a small "
            "pointer tail, holding short printed English dialogue in simple black "
            "comic lettering — text must be legible, in English only, and "
            "correctly spelled. Square 1:1 composition, 2K resolution."
        ),
    },
    {
        "slug": "4-yusof-gajah-folk-naif",
        "label": "Yusof Gajah naive folk-art",
        "prompt": (
            "A single illustrated comic book page in the vibrant naive folk-art "
            "style of Yusof Gajah, Malaysia's beloved illustrator — bold flat "
            "saturated colors (hot pink, marigold, turquoise, emerald, violet, "
            "sunset orange) with confident black ink outlines, richly patterned "
            "clothing and backgrounds with intricate dot-and-line decoration and "
            "elephant and flora motifs, naive-folk figure proportions with "
            "oversized friendly eyes, decorative repeating motifs of lotus, "
            "tropical leaves, and batik flourishes, warm cream paper background "
            "with subtle grain, cheerful Malaysian-children's-book sensibility. "
            "Showing four sequential panels arranged in a 2x2 grid with small "
            "numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated "
            "by thin black panel borders with narrow cream gutters. Each panel "
            "contains one clean white rounded speech bubble with a small pointer "
            "tail, holding short printed English dialogue in simple black comic "
            "lettering — text must be legible, in English only, and correctly "
            "spelled. Square 1:1 composition, 2K resolution."
        ),
    },
    {
        "slug": "5-modern-kl-graphic-novel",
        "label": "Modern Malaysian graphic-novel",
        "prompt": (
            "A single illustrated comic book page in the contemporary Malaysian "
            "graphic-novel style of Arif Rafhan and the urban-Malaysia indie-comic "
            "scene — clean precise dark ink outlines with warm muted watercolor "
            "wash, palette of cream paper, tropical teal, banana yellow, chili "
            "red, and soft coffee brown, realistic character proportions with "
            "sensitive humanist rendering of everyday KL street life, detailed "
            "Malaysian urban backgrounds (LRT stations, kopitiam, mamak stalls, "
            "PJ shopfronts, monorail overhead), quiet storytelling tone of modern "
            "Southeast Asian indie comics, visible painterly watercolor texture, "
            "subtle spot blacks for depth. Showing four sequential panels arranged "
            "in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner "
            "of each panel, separated by thin black panel borders with narrow "
            "white gutters. Each panel contains one clean white rounded speech "
            "bubble with a small pointer tail, holding short printed English "
            "dialogue in simple black comic-book lettering — text must be legible, "
            "in English only, and correctly spelled. Square 1:1 composition, 2K "
            "resolution."
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


def submit(endpoint: str, body: dict, ws_token: str) -> str | None:
    payload = json.dumps(body).encode()
    for attempt in range(5):
        try:
            d = _post(endpoint, payload, ws_token)
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
    # Handle both JPEG and PNG — convert PNG→JPEG via sips
    out.write_bytes(data)
    if data[:3] != b"\xff\xd8\xff":
        # Not JPEG — convert (likely PNG from GPT-Image)
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


def gen_one(style: dict, model: str, endpoint: str, ws_token: str, r2_token: str) -> dict:
    slug = f"{style['slug']}-{model}"
    out_path = Path(f"/tmp/malaysia-style-tests/{slug}.jpg")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    full_prompt = "STYLE:\n" + style["prompt"] + "\n\nSCENE:\n" + SCENE_SCRIPT

    # NB2 accepts resolution="2k" + output_format; GPT-Image-2 prefers size + output_format
    if model == "nb2":
        body = {"prompt": full_prompt, "resolution": "2k", "output_format": "jpeg"}
    else:  # gpt2
        body = {"prompt": full_prompt, "size": "1024x1024", "output_format": "jpeg"}

    t0 = time.time()
    tid = submit(endpoint, body, ws_token)
    if not tid:
        return {"slug": slug, "status": "submit_failed", "elapsed": time.time() - t0}
    url = poll(tid, ws_token)
    if not url:
        return {"slug": slug, "status": "poll_failed", "elapsed": time.time() - t0}
    if not download(url, out_path):
        return {"slug": slug, "status": "download_failed", "url": url}
    r2_key = f"scam-comics/my/style-tests/{slug}.jpg"
    if not upload_r2(out_path, r2_key, r2_token):
        return {"slug": slug, "status": "r2_upload_failed"}
    return {
        "slug": slug,
        "status": "ok",
        "bytes": out_path.stat().st_size,
        "r2": f"https://img.tabiji.ai/{r2_key}",
        "elapsed": round(time.time() - t0, 1),
    }


def main() -> int:
    ws_token = _keychain("wavespeed-api-key")
    r2_token = _keychain("cloudflare-api-token")

    jobs: list[tuple[dict, str, str]] = []
    for style in STYLES:
        jobs.append((style, "nb2", NB2_EP))
        jobs.append((style, "gpt2", GPT2_EP))

    t0 = time.time()
    print(f"generating {len(jobs)} Malaysia style tests (5 styles × 2 models)", flush=True)
    with ThreadPoolExecutor(max_workers=len(jobs)) as ex:
        results = list(ex.map(lambda j: gen_one(j[0], j[1], j[2], ws_token, r2_token), jobs))

    print(f"\ndone in {time.time()-t0:.0f}s\n", flush=True)
    for r in results:
        print(json.dumps(r), flush=True)
    bad = [r for r in results if r["status"] != "ok"]
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
