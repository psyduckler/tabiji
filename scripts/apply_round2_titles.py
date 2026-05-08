#!/usr/bin/env python3
"""
Apply round-2 title-CTR experiment titles to /scams/{city}/index.html pages.

Reads /tmp/title-rollout/assignments.json and /tmp/title-rollout/variant_c_scams.json,
rewrites <title>, og:title, and twitter:title in each city page per its arm assignment.

Arms:
- V3       : "Is {City} Safe for Tourists? {N} Scams to Avoid (2026)"
- Control  : "{N} Tourist Scams in {City} (2026) — How to Avoid"
- A        : "Is {City} Safe for Tourists? {N} Scams + Red Flags (2026)"
- B        : "What Locals Wish Tourists Knew: {N} {City} Scams (2026)"
- C        : "The {Top Scam} & {N-1} More: {City} Tourist Scams (2026)"
- D        : "Before You Visit {City}: {N} Tourist Scams to Avoid (2026)"
- E        : "Trending Tourist Scams in {City}: {N} to Watch in 2026"
"""
import json, re, sys, glob
from pathlib import Path
from typing import Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
ASSIGNMENTS = ROOT / "scripts" / "data" / "title-ctr-round2-assignments.json"
VARIANT_C_SCAMS = ROOT / "scripts" / "data" / "title-ctr-round2-variant-c-scams.json"


def extract_city_display(slug: str, current_title: str) -> str:
    """Extract the display city name from the current title."""
    patterns = [
        r"Is\s+(.+?)\s+Safe for Tourists",
        r"^\d+\s+(.+?)\s+Scams Locals Want",
        r"Don.t Fall for These \d+ Tourist Scams in\s+(.+?)\s*\(2026\)",
        r"What Locals Wish Tourists Knew:\s+\d+\s+(.+?)\s+Scams",
        r"The\s+.+?\s+&\s+\d+\s+More:\s+(.+?)\s+Tourist Scams",
        r"Before You Visit\s+(.+?):",
        r"Trending Tourist Scams in\s+(.+?):",
        r"\d+\s+(?:Tourist|Pilgrim)\s+Scam(?:s)?\s+(?:in|on|at)\s+(.+?)\s*\(2026\)",
    ]
    for pat in patterns:
        m = re.search(pat, current_title)
        if m:
            return m.group(1).strip()
    # Fallback: slug → title case
    return slug.replace("-", " ").title()


def build_titles(arm: str, city_display: str, n: int, top_scam: Optional[str]) -> dict:
    """Return dict with title, og_title, twitter_title for the given arm."""
    if arm == "V3":
        main = f"Is {city_display} Safe for Tourists? {n} Scams to Avoid (2026)"
    elif arm == "Control":
        main = f"{n} Tourist Scams in {city_display} (2026) — How to Avoid"
    elif arm == "A":
        main = f"Is {city_display} Safe for Tourists? {n} Scams + Red Flags (2026)"
    elif arm == "B":
        main = f"What Locals Wish Tourists Knew: {n} {city_display} Scams (2026)"
    elif arm == "C":
        if not top_scam:
            raise ValueError(f"Variant C requires top_scam for {city_display}")
        n_minus_1 = n - 1
        main = f"The {top_scam} & {n_minus_1} More: {city_display} Tourist Scams (2026)"
    elif arm == "D":
        main = f"Before You Visit {city_display}: {n} Tourist Scams to Avoid (2026)"
    elif arm == "E":
        main = f"Trending Tourist Scams in {city_display}: {n} to Watch in 2026"
    else:
        raise ValueError(f"Unknown arm: {arm}")

    return {
        "title": f"{main} | tabiji.ai",
        "og_title": f"{main} — tabiji.ai",
        "twitter_title": main,
    }


def replace_meta(content: str, attr_name: str, attr_value: str, new_content: str) -> Tuple[str, int]:
    """Replace the content="..." in a meta tag identified by attr_name=attr_value.
    Handles both attribute orders (content-first or property/name-first).
    Returns (new_html, replacements_made).
    """
    if attr_name == "property":
        # og:title-style, two attribute orderings
        patterns = [
            (rf'(<meta\s+property="{re.escape(attr_value)}"\s+content=")[^"]*(")', 1),
            (rf'(<meta\s+content=")[^"]*("\s+property="{re.escape(attr_value)}")', 1),
        ]
    elif attr_name == "name":
        # twitter:title-style
        patterns = [
            (rf'(<meta\s+name="{re.escape(attr_value)}"\s+content=")[^"]*(")', 1),
            (rf'(<meta\s+content=")[^"]*("\s+name="{re.escape(attr_value)}")', 1),
        ]
    else:
        raise ValueError(attr_name)

    total = 0
    for pat, _ in patterns:
        content, n = re.subn(pat, lambda m: m.group(1) + new_content + m.group(2), content)
        total += n
    return content, total


TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
NOF_RE = re.compile(r'"numberOfItems"\s*:\s*(\d+)')
SCAM_CARD_RE = re.compile(r'<div class="scam-card"\s+id="scam-\d+"')


def get_n(content: str, current_title: str) -> int:
    """Extract authoritative scam count, prioritizing the schema (idempotent across reruns)."""
    m = NOF_RE.search(content)
    if m:
        return int(m.group(1))
    cards = SCAM_CARD_RE.findall(content)
    if cards:
        return len(cards)
    # Last resort: title's first digit (only correct if title is in default/V3-style format)
    m = re.search(r"\b(\d+)\b", current_title)
    return int(m.group(1)) if m else 6


def apply_to_page(slug: str, arm: str, top_scam: Optional[str]) -> dict:
    path = ROOT / "scams" / slug / "index.html"
    if not path.exists():
        return {"slug": slug, "ok": False, "error": "missing"}

    content = path.read_text()
    m = TITLE_RE.search(content)
    if not m:
        return {"slug": slug, "ok": False, "error": "no <title>"}

    current_title = m.group(1).strip()
    city_display = extract_city_display(slug, current_title)
    n = get_n(content, current_title)

    new_titles = build_titles(arm, city_display, n, top_scam)

    # Replace <title>
    new_content, title_n = TITLE_RE.subn(
        lambda mt: f"<title>{new_titles['title']}</title>", content, count=1
    )

    # Replace og:title (handles both attribute orders)
    new_content, og_n = replace_meta(new_content, "property", "og:title", new_titles["og_title"])

    # Replace twitter:title
    new_content, tw_n = replace_meta(new_content, "name", "twitter:title", new_titles["twitter_title"])

    if title_n == 0 or og_n == 0 or tw_n == 0:
        return {
            "slug": slug, "ok": False,
            "error": f"replacements: title={title_n}, og={og_n}, tw={tw_n}",
            "current_title": current_title,
        }

    if new_content != content:
        path.write_text(new_content)
        return {
            "slug": slug, "ok": True, "arm": arm,
            "city_display": city_display, "n": n,
            "old_title": current_title, "new_title": new_titles["title"],
            "len_pre_brand": len(new_titles["twitter_title"]),
        }
    return {"slug": slug, "ok": True, "arm": arm, "noop": True, "new_title": new_titles["title"]}


def main():
    assignments = json.loads(ASSIGNMENTS.read_text())
    variant_c_scams = json.loads(VARIANT_C_SCAMS.read_text())

    results = {"V3": [], "Control": [], "A": [], "B": [], "C": [], "D": [], "E": []}
    errors = []

    for slug in sorted(assignments.keys()):
        arm = assignments[slug]
        top_scam = variant_c_scams.get(slug) if arm == "C" else None
        r = apply_to_page(slug, arm, top_scam)
        if r["ok"]:
            results[r["arm"]].append(r)
        else:
            errors.append(r)

    print("Per-arm rollout summary:")
    for arm in ["V3", "Control", "A", "B", "C", "D", "E"]:
        n = len(results[arm])
        print(f"  {arm}: {n} pages")
    print(f"Errors: {len(errors)}")

    if errors:
        print("\nERRORS:")
        for e in errors:
            print(f"  {e['slug']}: {e.get('error')}")
        sys.exit(1)

    # Length stats
    all_lens = [r["len_pre_brand"] for arm_results in results.values() for r in arm_results if "len_pre_brand" in r]
    if all_lens:
        over_60 = sum(1 for l in all_lens if l > 60)
        max_l = max(all_lens)
        print(f"\nTitle length (pre-brand): min={min(all_lens)} max={max_l}, {over_60}/{len(all_lens)} > 60 chars")


if __name__ == "__main__":
    main()
