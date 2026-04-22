#!/usr/bin/env python3
"""Rewrite compare leaf pages to use destination photos from destinations-full.json.

Replaces hardcoded `img.tabiji.ai/compare/{a}-vs-{b}/dest1.jpg` (and dest2.jpg)
with the canonical photo URL stored on each destination entry — usually
`img.tabiji.ai/find/img/{slug}.webp` or an `images.unsplash.com/...` URL
from the earlier unsplash batch work.

Safe-ish: skips pages where either destination slug isn't present in
destinations-full.json, and skips if no rewrite actually changes the file.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FULL_JSON = REPO / "api" / "v1" / "destinations-full.json"
COMPARE_DIR = REPO / "compare"


def split_pair(pair: str) -> tuple[str, str] | None:
    """Split `a-vs-b` into (a, b). Handles multi-hyphen slugs on either side
    by splitting on the rightmost standalone `-vs-` (it's unambiguous — no
    real destination name contains the literal `-vs-` substring)."""
    parts = pair.split("-vs-")
    if len(parts) != 2:
        return None
    return parts[0], parts[1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    with open(FULL_JSON) as f:
        full = json.load(f)

    leaf_dirs = sorted(p for p in COMPARE_DIR.iterdir() if p.is_dir())
    print(f"Scanning {len(leaf_dirs)} compare leaf dirs")

    updated = 0
    skipped_no_pattern = 0
    skipped_missing_slug = 0
    skipped_bad_pair = 0

    for d in leaf_dirs:
        if args.limit and updated >= args.limit:
            break
        pair = d.name
        index = d / "index.html"
        if not index.exists():
            continue
        html = index.read_text()
        if "dest1.jpg" not in html and "dest2.jpg" not in html:
            skipped_no_pattern += 1
            continue
        split = split_pair(pair)
        if not split:
            skipped_bad_pair += 1
            continue
        a, b = split
        ea, eb = full.get(a), full.get(b)
        if not ea or not eb:
            skipped_missing_slug += 1
            continue
        photo_a = (ea.get("photo") or "").strip()
        photo_b = (eb.get("photo") or "").strip()
        if not photo_a or "owl-logo" in photo_a or not photo_b or "owl-logo" in photo_b:
            # Shouldn't happen post-photo-fetch, but guard anyway.
            skipped_missing_slug += 1
            continue

        # Rewrite dest1.jpg → photo_a, dest2.jpg → photo_b, and hero.jpg
        # (used in og:image / twitter:image / JSON-LD image) → photo_a.
        # Also handle escaped slashes in JSON-LD blobs.
        pair_esc = re.escape(pair)
        old_a_re = re.compile(rf"https?:(?:\\/|/)+img\.tabiji\.ai(?:\\/|/)compare(?:\\/|/){pair_esc}(?:\\/|/)dest1\.jpg")
        old_b_re = re.compile(rf"https?:(?:\\/|/)+img\.tabiji\.ai(?:\\/|/)compare(?:\\/|/){pair_esc}(?:\\/|/)dest2\.jpg")
        hero_re = re.compile(rf"https?:(?:\\/|/)+img\.tabiji\.ai(?:\\/|/)compare(?:\\/|/){pair_esc}(?:\\/|/)hero\.jpg")
        # Escape forward slashes in the replacement if the matched text is in a
        # JSON-LD context (heuristic: if the match contains escaped slashes).
        def _swap(pattern: re.Pattern, repl: str, src: str) -> tuple[str, int]:
            # Detect whether any match uses escaped slashes; if so, emit
            # replacement with escaped slashes to keep the JSON string valid.
            count = 0
            def _sub(m: re.Match) -> str:
                nonlocal count
                count += 1
                return repl.replace("/", r"\/") if r"\/" in m.group(0) else repl
            new = pattern.sub(_sub, src)
            return new, count

        new_html, n_a = _swap(old_a_re, photo_a, html)
        new_html, n_b = _swap(old_b_re, photo_b, new_html)
        new_html, n_h = _swap(hero_re, photo_a, new_html)

        if n_a == 0 and n_b == 0 and n_h == 0:
            skipped_no_pattern += 1
            continue

        if args.dry_run:
            print(f"[dry-run] {pair}: dest1({n_a}) dest2({n_b}) hero({n_h})")
        else:
            index.write_text(new_html)
        updated += 1
        if updated % 50 == 0:
            print(f"  progress: {updated} pages rewritten")

    print()
    print(f"Updated: {updated}")
    print(f"Skipped (no dest1/dest2.jpg): {skipped_no_pattern}")
    print(f"Skipped (missing slug in full.json): {skipped_missing_slug}")
    print(f"Skipped (malformed pair slug): {skipped_bad_pair}")


if __name__ == "__main__":
    main()
