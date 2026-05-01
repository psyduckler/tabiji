#!/usr/bin/env python3
"""Everywhere-scams style bake-off — gpt-image-2 sister run.

Same 5 styles + same Margie / gift-card-by-phone scene as
bakeoff_everywhere_2026_04_30.py, but submitted to openai/gpt-image-2
via WaveSpeed instead of Nano Banana Pro. The hypothesis is that
gpt-image-2 renders speech-bubble text more reliably, which matters
because our scam-comic format leans heavily on dialogue.

Run this in parallel with the NBP bakeoff so the two vendors can be
compared style-by-style on identical prompts.
"""
from __future__ import annotations

import sys
import urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import (  # noqa: E402
    submit_nbp, poll_nbp, _keychain,
)
from cast import CHARACTERS  # noqa: E402
from bakeoff_everywhere_2026_04_30 import CANDIDATES, GENERIC_SCENE  # noqa: E402

GPT_T2I_EP = "https://api.wavespeed.ai/api/v3/openai/gpt-image-2/text-to-image"

OUT_DIR = Path("/tmp/bakeoff-everywhere-2026-04-30-gpt")
OUT_DIR.mkdir(exist_ok=True)


def build_prompt(style_block: str) -> str:
    char = CHARACTERS["margie"]
    return f"{style_block}\n\nCHARACTER: {char}\n\n{GENERIC_SCENE}"


def _download_any(url: str, out_path_no_ext: Path) -> tuple[bool, str, Path | None]:
    """Download whatever the URL returns. Accept JPEG or PNG; pick extension
    from the magic bytes. Returns (ok, note, final_path)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
    except Exception as e:
        return False, f"download err: {e}", None
    if len(data) < 50_000:
        return False, f"too small ({len(data)}B)", None
    if data[:3] == b"\xff\xd8\xff":
        ext = "jpg"
    elif data[:8] == b"\x89PNG\r\n\x1a\n":
        ext = "png"
    elif data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        ext = "webp"
    else:
        return False, f"unknown format (head={data[:8]!r})", None
    final = out_path_no_ext.with_suffix(f".{ext}")
    final.write_bytes(data)
    return True, f"ok ({ext}, {len(data)}B)", final


def generate_one(slug: str, prompt: str, ws: str) -> tuple[str, str]:
    body = {
        "prompt": prompt,
        "aspect_ratio": "1:1",
        "resolution": "2k",
        "quality": "medium",
    }
    tid = submit_nbp(body, GPT_T2I_EP, ws)
    if not tid:
        return slug, "FAIL: submit"
    raw_url = poll_nbp(tid, ws, timeout=1500)
    if not raw_url:
        return slug, "FAIL: poll"
    base = OUT_DIR / f"everywhere-gpt-{slug}"
    ok, note, final = _download_any(raw_url, base)
    if not ok:
        return slug, f"FAIL: dl {note}"
    return slug, f"OK: {final} ({note})"


def main():
    ws = _keychain("wavespeed-api-key")
    if not ws:
        print("ERROR: missing wavespeed-api-key", flush=True)
        sys.exit(1)

    print(f"Submitting {len(CANDIDATES)} gpt-image-2 everywhere-style generations...", flush=True)
    results: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(generate_one, slug, build_prompt(sb), ws): slug
                for slug, sb in CANDIDATES}
        for fut in as_completed(futs):
            slug = futs[fut]
            try:
                _, result = fut.result()
            except Exception as e:
                result = f"FAIL: {e}"
            results[slug] = result
            print(f"  {slug}: {result}", flush=True)

    print("\n=== RESULTS (gpt-image-2) ===", flush=True)
    for slug, _ in CANDIDATES:
        print(f"  {slug}: {results.get(slug, 'missing')}", flush=True)


if __name__ == "__main__":
    main()
