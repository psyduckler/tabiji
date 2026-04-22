#!/usr/bin/env python3
"""Rewrite compare/ + popular-picks/ hub pages to use destination photos from
destinations-full.json instead of per-compare-asset or per-pick imagery.

compare/index.html:
  background-image:url('https://img.tabiji.ai/compare/{a}-vs-{b}/*.jpg')
    -> https://img.tabiji.ai/find/img/{a}.webp  (first destination of the pair)

popular-picks/index.html:
  .country-card <img> pointing at popular-picks/{slug}/*.jpg
    -> destination photo if pick maps to a known destination (via picks.json)

Pick-card images (per-restaurant shots) are intentionally left alone —
those are pick-specific content, not destination photos.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FULL_JSON = REPO / "api" / "v1" / "destinations-full.json"
PICKS_JSON = REPO / "api" / "v1" / "picks.json"

COMPARE_INDEX = REPO / "compare" / "index.html"
PICKS_INDEX = REPO / "popular-picks" / "index.html"


def load_json(path: Path):
    with open(path) as f:
        return json.load(f)


def rewrite_compare_hub() -> int:
    if not COMPARE_INDEX.exists():
        return 0
    full = load_json(FULL_JSON)
    slugs = set(full.keys())
    html = COMPARE_INDEX.read_text()

    # Match any compare-asset URL: img.tabiji.ai/compare/{pair}/{anything}.(jpg|jpeg|png|webp)
    pattern = re.compile(
        r"https?://img\.tabiji\.ai/compare/([a-z0-9-]+-vs-[a-z0-9-]+)/[a-z0-9._-]+\.(?:jpg|jpeg|png|webp)",
        re.IGNORECASE,
    )
    replaced = 0
    missing = []

    def sub(match: re.Match) -> str:
        nonlocal replaced
        pair = match.group(1)
        parts = pair.split("-vs-")
        if len(parts) != 2:
            return match.group(0)
        a, _ = parts
        ea = full.get(a)
        if not ea:
            missing.append(a)
            return match.group(0)
        photo = (ea.get("photo") or "").strip()
        if not photo or "owl-logo" in photo:
            return match.group(0)
        replaced += 1
        return photo

    new_html = pattern.sub(sub, html)
    if new_html != html:
        COMPARE_INDEX.write_text(new_html)
    print(f"compare/index.html: {replaced} URL(s) rewritten; {len(set(missing))} unique missing slugs")
    return replaced


def rewrite_picks_hub() -> int:
    if not PICKS_INDEX.exists():
        return 0
    full = load_json(FULL_JSON)
    picks_data = load_json(PICKS_JSON)
    picks = picks_data.get("picks") or picks_data.get("items") or []
    pick_to_dest = {
        p.get("slug"): (p.get("destinationSlug") or p.get("destination") or "").lower()
        for p in picks if isinstance(p, dict)
    }

    html = PICKS_INDEX.read_text()

    # Only rewrite <img> tags inside .country-card elements; leave .pick-card
    # images alone. Match <a class="country-card"...>...<img src="..."...
    # through the next </a>.
    country_card_re = re.compile(
        r"(<a[^>]*class=\"country-card\"[^>]*>.*?</a>)",
        re.DOTALL,
    )
    img_re = re.compile(
        r'src="(https?://img\.tabiji\.ai/popular-picks/([a-z0-9-]+)/[a-z0-9._-]+\.(?:jpg|jpeg|png|webp))"',
        re.IGNORECASE,
    )

    replaced = 0
    skipped_no_dest = 0

    def replace_img_in_card(card_match: re.Match) -> str:
        nonlocal replaced, skipped_no_dest
        block = card_match.group(1)

        def inner(m: re.Match) -> str:
            nonlocal replaced, skipped_no_dest
            pick_slug = m.group(2)
            dest_slug = pick_to_dest.get(pick_slug)
            if not dest_slug:
                skipped_no_dest += 1
                return m.group(0)
            entry = full.get(dest_slug)
            if not entry:
                skipped_no_dest += 1
                return m.group(0)
            photo = (entry.get("photo") or "").strip()
            if not photo or "owl-logo" in photo:
                skipped_no_dest += 1
                return m.group(0)
            replaced += 1
            return f'src="{photo}"'

        return img_re.sub(inner, block)

    new_html = country_card_re.sub(replace_img_in_card, html)
    if new_html != html:
        PICKS_INDEX.write_text(new_html)
    print(f"popular-picks/index.html: {replaced} country-card img src rewritten; {skipped_no_dest} skipped")
    return replaced


def main() -> None:
    c = rewrite_compare_hub()
    p = rewrite_picks_hub()
    print(f"\nTotal rewrites: compare={c} picks={p}")


if __name__ == "__main__":
    main()
