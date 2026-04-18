#!/usr/bin/env python3
"""Re-inject comic illustrations into regenerated French scam pages.

Comics were added in commit 2931b5192e (Wavespeed nano-banana-pro). They're
keyed by (city, scam title) and served from img.tabiji.ai/scams/<city>/scam-N.jpg.

When we regenerated the HTML from batch files, we lost the <img class="scam-comic">
tags. This script rebuilds a title→img map from git HEAD and re-injects the tag
immediately after the scam-location div (matching commit cdb3a6b9e5's layout).

Scams that didn't exist in the pre-regen HTML are skipped — no fabricated URLs.
Run after regenerate_france_scams.py.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SCAMS_DIR = BASE / "scams"

FRENCH_SLUGS = [
    "nice", "cannes", "paris", "marseille", "avignon", "bordeaux",
    "chamonix", "lyon", "st-tropez", "strasbourg", "toulouse", "annecy",
    "biarritz", "colmar", "mont-saint-michel", "montpellier",
]


def build_title_to_img_map() -> dict[tuple[str, str], str]:
    """Parse git HEAD HTML for each French city and map scam-title → img tag."""
    pattern = re.compile(
        r'<div class="scam-title">([^<]+)</div>.*?(<img class="scam-comic"[^>]+>)',
        re.DOTALL,
    )
    mapping: dict[tuple[str, str], str] = {}
    for slug in FRENCH_SLUGS:
        res = subprocess.run(
            ["git", "show", f"HEAD:scams/{slug}/index.html"],
            capture_output=True, text=True, cwd=str(BASE),
        )
        if res.returncode != 0:
            continue
        for m in pattern.finditer(res.stdout):
            title = m.group(1).strip()
            img_tag = m.group(2).strip()
            mapping[(slug, title)] = img_tag
    return mapping


STOPWORDS = {
    "the", "a", "an", "of", "and", "or", "with", "for", "to", "in", "on", "at",
    "scam", "trick", "fake", "tourist", "trap",
}


def _key(title: str) -> frozenset:
    """Normalize a title to a set of significant words for fuzzy matching."""
    words = re.findall(r"[a-z0-9]+", title.lower())
    return frozenset(w for w in words if w not in STOPWORDS and len(w) > 2)


def inject_into_page(html: str, slug: str, mapping: dict) -> tuple[str, int]:
    """Return updated html + count of comics injected.

    Exact match first; then fuzzy match by significant-word overlap ≥ 50% of
    the shorter title's keyword set (catches "Friendship Bracelet Ambush" ↔
    "Friendship Bracelet Scam"-style rewrites).
    """
    if 'class="scam-comic"' in html:
        return html, 0

    # Pre-compute fuzzy index for this slug
    city_entries = [(t, img) for (s, t), img in mapping.items() if s == slug]
    fuzzy_index = [(t, img, _key(t)) for t, img in city_entries]

    def fuzzy_match(new_title: str) -> str | None:
        nk = _key(new_title)
        if not nk:
            return None
        best = None
        best_score = 0.0
        for old_title, img, ok in fuzzy_index:
            if not ok:
                continue
            overlap = len(nk & ok)
            # Require ≥2 significant words overlap — a single generic word is
            # too noisy (e.g. "fake" matches every impersonation scam).
            if overlap < 2:
                continue
            score = overlap / min(len(nk), len(ok))
            if score >= 0.5 and score > best_score:
                best = img
                best_score = score
        return best

    card_re = re.compile(
        r'(<div class="scam-card"[^>]*>.*?<div class="scam-title">([^<]+)</div>.*?<div class="scam-location">[^<]*</div>)',
        re.DOTALL,
    )

    injected = 0
    used_imgs: set[str] = set()

    def replace(match: re.Match) -> str:
        nonlocal injected
        head = match.group(1)
        title = match.group(2).strip()
        img_tag = mapping.get((slug, title)) or fuzzy_match(title)
        if not img_tag or img_tag in used_imgs:
            return head
        used_imgs.add(img_tag)
        injected += 1
        return head + "\n        " + img_tag

    new_html = card_re.sub(replace, html)
    return new_html, injected


def main():
    mapping = build_title_to_img_map()
    print(f"Loaded {len(mapping)} (city, title) → img mappings from git HEAD")

    total_injected = 0
    total_missing = 0
    for slug in FRENCH_SLUGS:
        path = SCAMS_DIR / slug / "index.html"
        if not path.exists():
            print(f"  ⚠ {slug}: missing HTML")
            continue
        html = path.read_text()
        new_html, injected = inject_into_page(html, slug, mapping)
        # Count scam cards to know how many lacked comics
        card_count = len(re.findall(r'<div class="scam-card"', new_html))
        missing = card_count - injected
        total_injected += injected
        total_missing += missing
        if new_html != html:
            path.write_text(new_html)
        note = "(idempotent no-op)" if 'class="scam-comic"' in html and injected == 0 else ""
        print(f"  {slug:<22} injected {injected}/{card_count} (missing {missing}) {note}")

    print(f"\nTotal: injected {total_injected}, {total_missing} scam cards without comic")


if __name__ == "__main__":
    main()
