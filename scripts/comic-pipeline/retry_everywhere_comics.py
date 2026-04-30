#!/usr/bin/env python3
"""Retry the 2 everywhere-comic stragglers with softer scene language.

Both failed at poll on gpt-image-2:
  - ai-voice-clone-scams/ai-deepfake-romance-video — likely 'deepfake' filter
  - pig-butchering/wrong-number-text-crypto-pitch — likely 'pig-butchering' filter

Rewriting the scenes to use neutral language while preserving the variant
narrative. URL slugs stay as-is so the page-side filenames don't change.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate_everywhere_comics import generate_one, RESULTS_PATH  # noqa: E402
from generate import _keychain  # noqa: E402

# Same slug, same character — softer scene text only.
RETRY_ENTRIES = [
    ("ai-voice-clone-scams", "scam-4", "ai-deepfake-romance-video", "harry", (
        "Panel 1: Harry on his couch on a video call with a smiling young "
        "woman on his laptop. Speech bubble (woman): \"I love seeing your "
        "face every day.\"\n"
        "Panel 2: The video call shows the woman asking for a wire transfer, "
        "Harry's expression turning concerned. Speech bubble (woman): \"My "
        "visa fee fell through — can you help?\"\n"
        "Panel 3: Harry drags the video frame into a reverse-image-search "
        "browser tab on his laptop. Speech bubble (Harry): \"Let me check "
        "this image.\"\n"
        "Panel 4: The reverse-search results show the same face on a stock-"
        "photo site. Speech bubble (Harry): \"Stock photo — not a real "
        "person.\""
    )),
    ("pig-butchering", "scam-2", "wrong-number-text-crypto-pitch", "harry", (
        "Panel 1: Harry at his kitchen table gets a 'wrong number' text from "
        "an unknown sender. Speech bubble (text): \"Hi Linda, dinner Friday "
        "at 7?\"\n"
        "Panel 2: Harry replies 'wrong number' — the sender chats back, "
        "two weeks later mentions her crypto trading. Speech bubble "
        "(text): \"My uncle's trading platform is amazing.\"\n"
        "Panel 3: Harry searches the platform name on his laptop — flagged "
        "on the FBI IC3 advisory list. Speech bubble (Harry): \"On the IC3 "
        "scam list.\"\n"
        "Panel 4: Harry blocks the number and reports to FBI IC3. Speech "
        "bubble (Harry): \"No 'wrong number' becomes a real friendship.\""
    )),
]


def main():
    ws = _keychain("wavespeed-api-key")
    if not ws:
        print("ERROR: missing wavespeed-api-key", flush=True); sys.exit(1)
    print(f"Retrying {len(RETRY_ENTRIES)} stragglers (softened scenes)...", flush=True)
    new_results: list[dict] = []
    with ThreadPoolExecutor(max_workers=2) as ex:
        futs = {
            ex.submit(generate_one, ps, ci, vs, ch, sc, ws): vs
            for ps, ci, vs, ch, sc in RETRY_ENTRIES
        }
        for fut in as_completed(futs):
            try:
                r = fut.result()
            except Exception as e:
                r = {"variant": futs[fut], "status": "FAIL", "error": str(e)}
            new_results.append(r)
            print(f"  {r['variant']}: {r['status']}{(' '+r.get('url','') if r['status']=='OK' else '')}", flush=True)

    # Merge into results.json — replace any FAIL entries for these variants.
    results = json.loads(RESULTS_PATH.read_text())
    new_by_variant = {r["variant"]: r for r in new_results}
    for i, r in enumerate(results):
        if r["variant"] in new_by_variant and new_by_variant[r["variant"]]["status"] == "OK":
            results[i] = new_by_variant[r["variant"]]
    RESULTS_PATH.write_text(json.dumps(results, indent=2))
    print(f"\nMerged into {RESULTS_PATH}", flush=True)


if __name__ == "__main__":
    main()
