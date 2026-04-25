#!/usr/bin/env python3
"""Canonical quality gate for /compare/ leaf pages.

Scores a page 0-100 across three dimensions:
  - Template & structure (35)
  - Content fundamentals (35)
  - Technical hygiene    (30)

Usage:
  score_compare.py <slug>                    # print score + breakdown
  score_compare.py <slug> --gate 100         # exit non-zero if score < 100
  score_compare.py --all                     # score every leaf, summary table
  score_compare.py --all --below 90          # list pages scoring < 90
  score_compare.py --json <slug>             # machine-readable

The score gate is the source of truth for "is this page production-ready."
build_compare.py and the compare-article-builder skill both call this before
allowing a commit.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from collections import Counter
from typing import Dict, List, Optional, Tuple

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    sys.stderr.write("score_compare.py requires beautifulsoup4 (pip install beautifulsoup4)\n")
    sys.exit(2)


REPO = pathlib.Path(__file__).resolve().parent.parent
COMPARE = REPO / "compare"

# Sub-hubs aren't leaf pages — they have a different rubric.
SUBHUBS = {
    'asia', 'australia', 'bali', 'cities', 'colombia', 'countries', 'croatia',
    'culture', 'egypt', 'europe', 'global-mixed', 'greece', 'hawaii', 'iceland',
    'islands', 'italy', 'japan', 'latin-america', 'luxury', 'maldives', 'mexico',
    'middle-east-africa', 'morocco', 'nature', 'new-zealand', 'north-america',
    'oceania', 'portugal', 'spain', 'taiwan', 'thailand', 'trip-style-guides',
    'vietnam',
}


# ─────────────────────── scoring rubric ───────────────────────
# Each check returns (points_earned, max_points, label, status_msg).
# A 100/100 page passes every check.
RUBRIC: List[Tuple[str, str, int]] = [
    # (key, human_label, max_points)
    ("ct",       "Comparison table",            5),
    ("faq",      "FAQ items (≥16)",            10),
    ("qa",       "Quick Answers section",       8),
    ("sc",       "Visual Scorecard",            7),
    ("pers",     "Personalize widget",          5),
    ("title",    "Title length (35–65c)",      10),
    ("meta",     "Meta desc length (90–160c)", 10),
    ("byline",   "Bernard Huang byline",        5),
    ("tv",       "tabiji-verdict callout",      5),
    ("photos",   "Photo-grid (≥2 images)",      5),
    ("anchors",  "All in-page anchors resolve", 8),
    ("amp",      "No `&amp;amp;` encoding bug", 6),
    ("mobile",   "Mobile-overflow tables wrapped", 6),
    ("lcp",      "LCP image not lazy-loaded",   5),
    ("fp",       "LCP image has fetchpriority", 5),
]


def score_page(slug: str) -> Optional[Dict]:
    """Score a single leaf page. Returns None if file missing or redirect stub."""
    path = COMPARE / slug / "index.html"
    if not path.exists():
        return None
    txt = path.read_text(errors="replace")
    if 'http-equiv="refresh"' in txt:
        return None

    soup = BeautifulSoup(txt, "html.parser")
    body = soup.find("body")
    if body is None:
        return None

    parts: Dict[str, int] = {}
    issues: Dict[str, str] = {}

    # ── Template & structure (35) ──
    if soup.find("table", class_=re.compile(r"comparison-table")):
        parts["ct"] = 5
    else:
        parts["ct"] = 0; issues["ct"] = "no <table class=\"comparison-table\"> found"

    faq_n = (
        len(soup.find_all(class_=re.compile(r"faq-item"))) +
        len(soup.find_all(attrs={"itemtype": re.compile(r"Question")}))
    )
    if faq_n >= 16:
        parts["faq"] = 10
    elif faq_n >= 7:
        parts["faq"] = 5; issues["faq"] = f"only {faq_n} FAQ items (need 16+)"
    else:
        parts["faq"] = 0; issues["faq"] = f"only {faq_n} FAQ items (need 16+)"

    if soup.find(class_="quick-answers"):
        parts["qa"] = 8
    else:
        parts["qa"] = 0; issues["qa"] = "no .quick-answers section (server-render, don't rely on JS injection)"

    if soup.find(class_=re.compile(r"\bscorecard\b")):
        parts["sc"] = 7
    else:
        parts["sc"] = 0; issues["sc"] = "no .scorecard element"

    if soup.find(class_="personalize-widget"):
        parts["pers"] = 5
    else:
        parts["pers"] = 0; issues["pers"] = "no .personalize-widget"

    # ── Content fundamentals (35) ──
    title_tag = soup.find("title")
    title_len = len(title_tag.get_text().strip()) if title_tag else 0
    if 35 <= title_len <= 65:
        parts["title"] = 10
    else:
        diff = max(35 - title_len, title_len - 65, 0)
        parts["title"] = max(0, 10 - 2 * (diff // 5 + 1))
        issues["title"] = f"title is {title_len} chars (target 35–65)"

    md = soup.find("meta", attrs={"name": "description"})
    meta_len = len((md.get("content", "") if md else "").strip())
    if 90 <= meta_len <= 160:
        parts["meta"] = 10
    else:
        diff = max(90 - meta_len, meta_len - 160, 0)
        parts["meta"] = max(0, 10 - 2 * (diff // 10 + 1))
        issues["meta"] = f"meta description is {meta_len} chars (target 90–160)"

    if soup.find(class_=re.compile(r"\bpage-byline\b")) or "bernard-huang" in txt.lower():
        parts["byline"] = 5
    else:
        parts["byline"] = 0; issues["byline"] = "no Bernard Huang byline (E-E-A-T)"

    if soup.find(class_="tabiji-verdict"):
        parts["tv"] = 5
    else:
        parts["tv"] = 0; issues["tv"] = "no .tabiji-verdict callout"

    pg = soup.find(class_="photo-grid")
    pg_imgs = pg.find_all("img") if pg else []
    if len(pg_imgs) >= 2:
        parts["photos"] = 5
    else:
        parts["photos"] = 0; issues["photos"] = f"photo-grid has {len(pg_imgs)} imgs (need 2+)"

    # ── Technical hygiene (30) ──
    ids = {tag.get("id") for tag in body.find_all(id=True) if tag.get("id")}
    bad_anchors: List[str] = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("#") and len(href) > 1 and href[1:] not in ids:
            bad_anchors.append(href)
    if not bad_anchors:
        parts["anchors"] = 8
    else:
        parts["anchors"] = 0
        sample = ", ".join(sorted(set(bad_anchors))[:3])
        issues["anchors"] = f"{len(bad_anchors)} broken anchor(s): {sample}"

    body_html = str(body)
    if "&amp;amp;" not in body_html:
        parts["amp"] = 6
    else:
        parts["amp"] = 0; issues["amp"] = "&amp;amp; (double-encoded ampersand) appears in body"

    mobile_overflow_unwrapped = False
    overflow_table_count = 0
    for tbl in soup.find_all("table"):
        st = (tbl.get("style", "") or "")
        m = re.search(r"min-width\s*:\s*(\d+)\s*px", st)
        if m and int(m.group(1)) > 480:
            parent_st = (tbl.parent.get("style", "") or "") if tbl.parent else ""
            if "overflow-x" not in parent_st:
                mobile_overflow_unwrapped = True
                overflow_table_count += 1
    if not mobile_overflow_unwrapped:
        parts["mobile"] = 6
    else:
        parts["mobile"] = 0
        issues["mobile"] = f"{overflow_table_count} table(s) with min-width >480px lack overflow-x wrapper"

    first_pg_img = pg_imgs[0] if pg_imgs else None
    if first_pg_img and first_pg_img.get("loading") != "lazy":
        parts["lcp"] = 5
    else:
        parts["lcp"] = 0
        issues["lcp"] = "first photo-grid <img> has loading=\"lazy\" — LCP regression"

    if first_pg_img and first_pg_img.get("fetchpriority") == "high":
        parts["fp"] = 5
    else:
        parts["fp"] = 0
        issues["fp"] = "first photo-grid <img> missing fetchpriority=\"high\""

    score = sum(parts.values())
    tier = (
        "FULL" if (parts.get("qa") and parts.get("sc"))
        else "MED" if parts.get("tv")
        else "LITE"
    )

    return {
        "slug": slug,
        "score": score,
        "tier": tier,
        "parts": parts,
        "issues": issues,
        "title_len": title_len,
        "meta_len": meta_len,
        "faq_n": faq_n,
    }


def print_report(r: Dict, *, gate: Optional[int] = None) -> int:
    """Pretty-print a single page's score + issue list. Returns exit code."""
    print(f"\n{r['slug']}: {r['score']}/100  ({r['tier']} tier)")
    print(f"  title={r['title_len']}c  meta={r['meta_len']}c  FAQ={r['faq_n']}")
    print()
    for key, label, maxp in RUBRIC:
        earned = r["parts"].get(key, 0)
        mark = "✓" if earned == maxp else ("△" if earned > 0 else "✗")
        line = f"  {mark} {earned:>2}/{maxp:<2}  {label}"
        if key in r["issues"]:
            line += f"  — {r['issues'][key]}"
        print(line)
    if gate is not None and r["score"] < gate:
        print(f"\n❌ FAIL: score {r['score']} < gate {gate}")
        return 1
    if gate is not None:
        print(f"\n✅ PASS: score {r['score']} ≥ gate {gate}")
    return 0


def score_all() -> List[Dict]:
    results = []
    for p in sorted(COMPARE.glob("*/index.html")):
        slug = p.parent.name
        if slug in SUBHUBS:
            continue
        r = score_page(slug)
        if r:
            results.append(r)
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("slug", nargs="?", help="leaf slug, e.g. tokyo-vs-kyoto")
    ap.add_argument("--gate", type=int, help="exit non-zero if score < N")
    ap.add_argument("--all", action="store_true", help="score every leaf")
    ap.add_argument("--below", type=int, help="with --all: list pages scoring < N")
    ap.add_argument("--json", action="store_true", help="emit JSON for piping")
    args = ap.parse_args()

    if args.all:
        results = score_all()
        if args.json:
            print(json.dumps([{k: v for k, v in r.items() if k != "issues"} for r in results], indent=2))
            return 0
        buckets = Counter()
        for r in results:
            s = r["score"]
            if s >= 90: buckets["A+ (≥90)"] += 1
            elif s >= 80: buckets["A  (80-89)"] += 1
            elif s >= 70: buckets["B+ (70-79)"] += 1
            elif s >= 60: buckets["B  (60-69)"] += 1
            elif s >= 50: buckets["C  (50-59)"] += 1
            else: buckets["F  (<50)"] += 1
        print(f"Scored {len(results)} leaf pages\n")
        for tier in ["A+ (≥90)", "A  (80-89)", "B+ (70-79)", "B  (60-69)", "C  (50-59)", "F  (<50)"]:
            print(f"  {tier:<11} {buckets.get(tier, 0):>4}")
        if args.below is not None:
            below = sorted([r for r in results if r["score"] < args.below], key=lambda x: x["score"])
            print(f"\n{len(below)} pages below {args.below}:")
            for r in below[:30]:
                print(f"  {r['score']:>3}  {r['tier']:<5}  FAQ={r['faq_n']:<2}  {r['slug']}")
        return 0

    if not args.slug:
        ap.error("provide a slug or --all")

    r = score_page(args.slug)
    if not r:
        sys.stderr.write(f"page not found or is a redirect stub: {args.slug}\n")
        return 2
    if args.json:
        print(json.dumps(r, indent=2))
        return 0
    return print_report(r, gate=args.gate)


if __name__ == "__main__":
    sys.exit(main())
