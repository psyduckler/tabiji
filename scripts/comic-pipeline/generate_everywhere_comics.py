#!/usr/bin/env python3
"""Generate all 51 /scams/everywhere/ comics via openai/gpt-image-2.

Reads everywhere_comics_manifest.MANIFEST, fires gpt-image-2 generations
for every entry in parallel batches, uploads each result to R2 at
scam-comics/everywhere/<page_slug>/<variant_slug>.png, and writes a
results JSON for the insertion step.

Style: STYLES["_everywhere"] from styles.py — flat-cel-shaded, locked
2026-04-30 after a 5-style gpt-image-2 bakeoff.
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import submit_nbp, poll_nbp, upload_r2, _keychain  # noqa: E402
from cast import CHARACTERS  # noqa: E402
from styles import STYLES  # noqa: E402
from everywhere_comics_manifest import MANIFEST  # noqa: E402

GPT_T2I_EP = "https://api.wavespeed.ai/api/v3/openai/gpt-image-2/text-to-image"
OUT_DIR = Path("/tmp/everywhere-comics-2026-04-30")
OUT_DIR.mkdir(exist_ok=True)
RESULTS_PATH = OUT_DIR / "results.json"
STYLE_BLOCK = STYLES["_everywhere"]


def build_prompt(character: str, scene: str) -> str:
    char_block = CHARACTERS[character]
    return (
        f"{STYLE_BLOCK}\n\nCHARACTER: {char_block}\n\nSCENE:\n{scene}"
    )


def _download_any(url: str, base: Path) -> tuple[bool, str, Path | None]:
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
    final = base.with_suffix(f".{ext}")
    final.write_bytes(data)
    return True, f"ok ({ext}, {len(data)}B)", final


def generate_one(page_slug: str, card_id: str, variant_slug: str,
                 character: str, scene: str, ws: str) -> dict:
    prompt = build_prompt(character, scene)
    body = {
        "prompt": prompt,
        "aspect_ratio": "1:1",
        "resolution": "2k",
        "quality": "medium",
    }
    tid = submit_nbp(body, GPT_T2I_EP, ws)
    if not tid:
        return {"page": page_slug, "card": card_id, "variant": variant_slug,
                "status": "FAIL", "error": "submit"}
    raw_url = poll_nbp(tid, ws, timeout=1500)
    if not raw_url:
        return {"page": page_slug, "card": card_id, "variant": variant_slug,
                "status": "FAIL", "error": "poll"}
    base = OUT_DIR / f"{page_slug}__{variant_slug}"
    ok, note, final = _download_any(raw_url, base)
    if not ok:
        return {"page": page_slug, "card": card_id, "variant": variant_slug,
                "status": "FAIL", "error": f"dl {note}"}
    ext = final.suffix.lstrip(".")
    r2_key = f"scam-comics/everywhere/{page_slug}/{variant_slug}.{ext}"
    if not upload_r2(final, r2_key, ""):
        return {"page": page_slug, "card": card_id, "variant": variant_slug,
                "status": "FAIL_LOCAL_OK", "local": str(final),
                "error": "r2 upload failed"}
    return {"page": page_slug, "card": card_id, "variant": variant_slug,
            "status": "OK", "url": f"https://img.tabiji.ai/{r2_key}",
            "local": str(final), "note": note}


def main():
    ws = _keychain("wavespeed-api-key")
    if not ws:
        print("ERROR: missing wavespeed-api-key", flush=True)
        sys.exit(1)
    print(f"Generating {len(MANIFEST)} everywhere comics via gpt-image-2...",
          flush=True)
    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {
            ex.submit(generate_one, page_slug, card_id, variant_slug,
                      character, scene, ws):
            (page_slug, card_id, variant_slug)
            for page_slug, card_id, variant_slug, character, scene in MANIFEST
        }
        for i, fut in enumerate(as_completed(futs), 1):
            try:
                r = fut.result()
            except Exception as e:
                page_slug, card_id, variant_slug = futs[fut]
                r = {"page": page_slug, "card": card_id, "variant": variant_slug,
                     "status": "FAIL", "error": f"exc {e}"}
            results.append(r)
            tag = r["status"]
            label = f"{r['page']}/{r['variant']}"
            print(f"  [{i:>2}/{len(MANIFEST)}] {tag:<14} {label}", flush=True)

    RESULTS_PATH.write_text(json.dumps(results, indent=2))
    print(f"\nResults written to {RESULTS_PATH}", flush=True)

    ok = [r for r in results if r["status"] == "OK"]
    fail = [r for r in results if r["status"] != "OK"]
    print(f"\n=== SUMMARY ===\n  OK: {len(ok)}\n  FAIL: {len(fail)}", flush=True)
    if fail:
        print("\nFailures:")
        for r in fail:
            print(f"  - {r['page']}/{r['variant']}: {r.get('error', '?')}")


if __name__ == "__main__":
    main()
