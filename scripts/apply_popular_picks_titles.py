#!/usr/bin/env python3
"""
Apply title-CTR experiment titles to /popular-picks/{slug}/index.html pages.

Reads scripts/data/popular-picks-title-experiment-assignments.json — an
ENRICHED mapping with each slug's arm + canonical {n, topic, city} display
values pre-computed once (from the original/clean page state). Re-running
the script is idempotent because it never re-parses the live title — it
only uses the stored canonical values.

Cohort: top 300 live pages by live-page impressions, drawn from topics with
≥500 live-page imps and <1.0% CTR (excludes winners like bbq, and the
long tail of low-data one-off cuisine topics). Stratified-snake balanced
across 6 arms × 50 pages.

Arms:
- Control : "{N} Best {Topic} in {City} (2026)"
- A       : "Where Are the Best {Topic} in {City}? (2026 Honest Guide)"
- B       : "Best {Topic} in {City}: Where Locals Actually Go (2026)"
- C       : "{N} {Topic} in {City} Most Tourists Miss (2026)"
- D       : "{N} {Topic} in {City} Worth Knowing (No Tourist Traps) (2026)"
- E       : "{Topic} in {City}: What Reddit Locals Recommend (2026)"

All three meta tags (<title>, og:title, twitter:title) are set in sync per
the existing popular-picks pattern. Meta description, H1, body, URL, and
inventory data unchanged.
"""
import json, re, sys
from pathlib import Path
from typing import Tuple

ROOT = Path(__file__).resolve().parent.parent
ASSIGNMENTS = ROOT / "scripts" / "data" / "popular-picks-title-experiment-assignments.json"

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def build_main_title(arm: str, n: int, topic: str, city: str) -> str:
    if arm == "Control":
        return f"{n} Best {topic} in {city} (2026)"
    if arm == "A":
        return f"Where Are the Best {topic} in {city}? (2026 Honest Guide)"
    if arm == "B":
        return f"Best {topic} in {city}: Where Locals Actually Go (2026)"
    if arm == "C":
        return f"{n} {topic} in {city} Most Tourists Miss (2026)"
    if arm == "D":
        return f"{n} {topic} in {city} Worth Knowing (No Tourist Traps) (2026)"
    if arm == "E":
        return f"{topic} in {city}: What Reddit Locals Recommend (2026)"
    raise ValueError(f"Unknown arm: {arm}")


def replace_meta(content: str, attr_name: str, attr_value: str, new_content: str) -> Tuple[str, int]:
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


def apply_to_page(slug: str, entry: dict) -> dict:
    arm = entry["arm"]
    n = entry["n"]
    topic = entry["topic"]
    city = entry["city"]

    path = ROOT / "popular-picks" / slug / "index.html"
    if not path.exists():
        return {"slug": slug, "ok": False, "error": "missing"}

    content = path.read_text()
    if not TITLE_RE.search(content):
        return {"slug": slug, "ok": False, "error": "no <title>"}

    main = build_main_title(arm, n, topic, city)
    full = f"{main} | tabiji.ai"

    new_content, t_n = TITLE_RE.subn(lambda mt: f"<title>{full}</title>", content, count=1)
    new_content, og_n = replace_meta(new_content, "property", "og:title", full)
    new_content, tw_n = replace_meta(new_content, "name", "twitter:title", full)

    if t_n == 0 or og_n == 0 or tw_n == 0:
        return {"slug": slug, "ok": False,
                "error": f"replacements: title={t_n}, og={og_n}, tw={tw_n}"}

    if new_content != content:
        path.write_text(new_content)
        return {"slug": slug, "ok": True, "arm": arm,
                "len_pre_brand": len(main), "new_title": full}
    return {"slug": slug, "ok": True, "arm": arm, "noop": True}


def main():
    enriched = json.loads(ASSIGNMENTS.read_text())
    arms = ["Control", "A", "B", "C", "D", "E"]
    results = {a: [] for a in arms}
    errors = []

    for slug in sorted(enriched.keys()):
        r = apply_to_page(slug, enriched[slug])
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
        over = sum(1 for l in all_lens if l > 60)
        print(f"\nTitle length (pre-brand): min={min(all_lens)} max={max(all_lens)}, "
              f"{over}/{len(all_lens)} > 60 chars")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
