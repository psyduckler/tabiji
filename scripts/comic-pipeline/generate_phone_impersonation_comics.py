#!/usr/bin/env python3
"""Generate the 5 phone-impersonation-government comics via gpt-image-2."""
from __future__ import annotations

import json, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate_everywhere_comics import generate_one, RESULTS_PATH  # noqa: E402
from everywhere_comics_manifest import MANIFEST  # noqa: E402
from generate import _keychain  # noqa: E402

NEW_PAGE = "phone-impersonation-government"
TARGETS = [m for m in MANIFEST if m[0] == NEW_PAGE]


def main():
    ws = _keychain("wavespeed-api-key")
    if not ws: print("ERROR: missing wavespeed-api-key", flush=True); sys.exit(1)
    print(f"Generating {len(TARGETS)} comics for {NEW_PAGE}...", flush=True)
    new_results = []
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(generate_one, ps, ci, vs, ch, sc, ws): vs for ps, ci, vs, ch, sc in TARGETS}
        for fut in as_completed(futs):
            try: r = fut.result()
            except Exception as e: r = {"variant": futs[fut], "status": "FAIL", "error": str(e)}
            new_results.append(r)
            print(f"  [{r['status']}] {r.get('variant', '?')}: {r.get('url', r.get('error', '?'))}", flush=True)
    if RESULTS_PATH.exists():
        existing = json.loads(RESULTS_PATH.read_text())
    else: existing = []
    existing.extend(new_results)
    RESULTS_PATH.write_text(json.dumps(existing, indent=2))
    print(f"\nMerged into {RESULTS_PATH}", flush=True)


if __name__ == "__main__": main()
