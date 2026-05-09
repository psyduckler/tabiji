#!/usr/bin/env python3
"""
Apply title-CTR experiment titles to /compare/{slug}/index.html pages.

Reads scripts/data/compare-title-experiment-assignments.json and rewrites
<title>, og:title, and twitter:title in each page per its arm assignment.

Cohort: big-vs-niche + big-vs-big pages only (364 total). Niche-vs-niche
pages are excluded — already winning at 0.67% CTR, don't break.

Arms (11):
- Control : "{X} vs {Y}: Which Should You Visit? (2026 Comparison)"
- A       : "{X} vs {Y}: Honest 2026 Comparison"
- B       : "Is {X} Better Than {Y} in 2026? Honest Comparison"
- C       : "{X} vs {Y}: Cost, Safety & Vibe Compared (2026)"
- D       : "{X} vs {Y}: What Reddit Travelers Picked (2026)"
- E       : "Should I Visit {X} or {Y}? (2026 Decision Guide)"
- F       : "{X} vs {Y}: Best for Couples, Solo, or Family? (2026)"
- G       : "{X} vs {Y}: Pros, Cons & 2026 Verdict"
- H       : "2026 Showdown: {X} vs {Y} (Real Costs, Honest Take)"
- I       : "{X} vs {Y}: 7 Differences That Decide Your Trip (2026)"
- J       : "{X} vs {Y}: Where to Spend a Week in 2026"

Title, og:title, and twitter:title are kept in sync per arm. Meta
description, H1, body, URL are unchanged.
"""
import json, re, sys
from pathlib import Path
from typing import Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
ASSIGNMENTS = ROOT / "scripts" / "data" / "compare-title-experiment-assignments.json"
INVENTORY = ROOT / "compare" / "inventory.json"


def build_main_title(arm: str, x: str, y: str) -> str:
    """Return the main title (without brand suffix) for the given arm + destination pair."""
    if arm == "Control":
        return f"{x} vs {y}: Which Should You Visit? (2026 Comparison)"
    if arm == "A":
        return f"{x} vs {y}: Honest 2026 Comparison"
    if arm == "B":
        return f"Is {x} Better Than {y} in 2026? Honest Comparison"
    if arm == "C":
        return f"{x} vs {y}: Cost, Safety & Vibe Compared (2026)"
    if arm == "D":
        return f"{x} vs {y}: What Reddit Travelers Picked (2026)"
    if arm == "E":
        return f"Should I Visit {x} or {y}? (2026 Decision Guide)"
    if arm == "F":
        return f"{x} vs {y}: Best for Couples, Solo, or Family? (2026)"
    if arm == "G":
        return f"{x} vs {y}: Pros, Cons & 2026 Verdict"
    if arm == "H":
        return f"2026 Showdown: {x} vs {y} (Real Costs, Honest Take)"
    if arm == "I":
        return f"{x} vs {y}: 7 Differences That Decide Your Trip (2026)"
    if arm == "J":
        return f"{x} vs {y}: Where to Spend a Week in 2026"
    raise ValueError(f"Unknown arm: {arm}")


def build_titles(arm: str, x: str, y: str) -> dict:
    main = build_main_title(arm, x, y)
    return {
        "title": f"{main} | tabiji.ai",
        "og_title": f"{main} — tabiji.ai",
        "twitter_title": main,
    }


TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def replace_meta(content: str, attr_name: str, attr_value: str, new_content: str) -> Tuple[str, int]:
    """Replace content="..." in a <meta> identified by attr_name=attr_value, both attr orderings."""
    if attr_name == "property":
        patterns = [
            rf'(<meta\s+property="{re.escape(attr_value)}"\s+content=")[^"]*(")',
            rf'(<meta\s+content=")[^"]*("\s+property="{re.escape(attr_value)}")',
        ]
    elif attr_name == "name":
        patterns = [
            rf'(<meta\s+name="{re.escape(attr_value)}"\s+content=")[^"]*(")',
            rf'(<meta\s+content=")[^"]*("\s+name="{re.escape(attr_value)}")',
        ]
    else:
        raise ValueError(attr_name)

    total = 0
    for pat in patterns:
        content, n = re.subn(pat, lambda m: m.group(1) + new_content + m.group(2), content)
        total += n
    return content, total


def apply_to_page(slug: str, arm: str, x: str, y: str) -> dict:
    path = ROOT / "compare" / slug / "index.html"
    if not path.exists():
        return {"slug": slug, "ok": False, "error": "missing"}

    content = path.read_text()
    if not TITLE_RE.search(content):
        return {"slug": slug, "ok": False, "error": "no <title>"}

    new_titles = build_titles(arm, x, y)

    new_content, title_n = TITLE_RE.subn(
        lambda mt: f"<title>{new_titles['title']}</title>", content, count=1
    )
    new_content, og_n = replace_meta(new_content, "property", "og:title", new_titles["og_title"])
    new_content, tw_n = replace_meta(new_content, "name", "twitter:title", new_titles["twitter_title"])

    if title_n == 0 or og_n == 0 or tw_n == 0:
        return {
            "slug": slug, "ok": False,
            "error": f"replacements: title={title_n}, og={og_n}, tw={tw_n}",
        }

    if new_content != content:
        path.write_text(new_content)
        return {
            "slug": slug, "ok": True, "arm": arm,
            "len_pre_brand": len(new_titles["twitter_title"]),
            "new_title": new_titles["title"],
        }
    return {"slug": slug, "ok": True, "arm": arm, "noop": True}


def main():
    assignments = json.loads(ASSIGNMENTS.read_text())
    inventory = json.loads(INVENTORY.read_text())
    by_slug = {c["slug"]: c for c in inventory["cards"]}

    arms = ["Control", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    results = {a: [] for a in arms}
    errors = []

    for slug, arm in sorted(assignments.items()):
        card = by_slug.get(slug)
        if not card:
            errors.append({"slug": slug, "error": "not in inventory"})
            continue
        x = card.get("destination1") or slug.split("-vs-")[0].title()
        y = card.get("destination2") or slug.split("-vs-")[1].title()
        r = apply_to_page(slug, arm, x, y)
        if r["ok"]:
            results[r["arm"]].append(r)
        else:
            errors.append(r)

    print("Per-arm rollout summary:")
    for a in arms:
        n = len(results[a])
        wrote = sum(1 for r in results[a] if "len_pre_brand" in r)
        print(f"  {a}: {n} pages ({wrote} writes, {n - wrote} no-op)")
    print(f"Errors: {len(errors)}")
    for e in errors:
        print(f"  ! {e['slug']}: {e.get('error')}")

    all_lens = [r["len_pre_brand"] for ars in results.values() for r in ars if "len_pre_brand" in r]
    if all_lens:
        over_60 = sum(1 for l in all_lens if l > 60)
        print(f"\nTitle length (pre-brand): min={min(all_lens)} max={max(all_lens)}, "
              f"{over_60}/{len(all_lens)} > 60 chars")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
