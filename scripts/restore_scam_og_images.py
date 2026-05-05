#!/usr/bin/env python3
"""Restore city-specific OG/Twitter/Article images on scam pages.

Background: PR #1454 swapped city-specific OG image URLs for the default
tabiji-owl-logo.png because some city-specific R2 OG assets were unreliable.
Side effect: every city's social share preview is now identical, killing the
destination signal on Twitter, iMessage, Slack, etc.

Each city page already references a scam-1 comic in the page body that's
verified loadable from R2 (it renders in-page). This script reuses that
image as the og:image, twitter:image, and Article JSON-LD image. The
Organization publisher logo and nav owl logo are left unchanged.

Run from repo root: python3 scripts/restore_scam_og_images.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCAMS = REPO / "scams"
DEFAULT_OG = "https://img.tabiji.ai/tabiji-owl-logo.png"
SKIP_DIRS = {"atlas", "everywhere", "country", "research"}


def first_scam_comic_src(text: str) -> str | None:
    m = re.search(r'<img\s[^>]*class="scam-comic"[^>]*>', text)
    if not m:
        return None
    src_m = re.search(r'src="([^"]+)"', m.group(0))
    return src_m.group(1) if src_m else None


def replace_og_targets(text: str, src: str) -> str:
    # UTF-8 (Bangkok-style) template — property/name first, content second
    text = text.replace(
        f'property="og:image" content="{DEFAULT_OG}"',
        f'property="og:image" content="{src}"',
    )
    text = text.replace(
        f'name="twitter:image" content="{DEFAULT_OG}"',
        f'name="twitter:image" content="{src}"',
    )
    # utf-8/ (Alanya-style) template — content first, property/name second
    text = text.replace(
        f'content="{DEFAULT_OG}" property="og:image"',
        f'content="{src}" property="og:image"',
    )
    text = text.replace(
        f'content="{DEFAULT_OG}" name="twitter:image"',
        f'content="{src}" name="twitter:image"',
    )
    # Article JSON-LD image field (publisher.logo.url uses "url" key, not "image")
    text = text.replace(
        f'"image": "{DEFAULT_OG}"',
        f'"image": "{src}"',
    )
    return text


def main() -> int:
    updated: list[str] = []
    skipped_no_comic: list[str] = []

    for child in sorted(SCAMS.iterdir()):
        if not child.is_dir() or child.name in SKIP_DIRS:
            continue
        index = child / "index.html"
        if not index.exists():
            continue

        text = index.read_text()
        if DEFAULT_OG not in text:
            continue

        src = first_scam_comic_src(text)
        if not src:
            skipped_no_comic.append(child.name)
            continue

        new_text = replace_og_targets(text, src)
        if new_text != text:
            index.write_text(new_text)
            updated.append(child.name)

    print(f"Updated: {len(updated)} city pages")
    if skipped_no_comic:
        print(f"Skipped {len(skipped_no_comic)} (no scam-comic image): {skipped_no_comic[:10]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
