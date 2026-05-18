#!/usr/bin/env python3
"""
Score a /compare/{slug}/index.html page with VeracityAPI for slop / synthetic
risk. Used by the veracity experiment (docs/veracity-experiment.md).

Usage:
    VERACITY_API_KEY=vap_... python3 scripts/veracity_score.py <slug>
    VERACITY_API_KEY=vap_... python3 scripts/veracity_score.py --all-cohort

Output: docs/data/veracity-experiment/scores/{slug}.json (raw response + the
prose that was sent + token-cost metadata).

Prose extraction strategy:
  Send only editorial content — hero subtitle, verdict-box prose, deep-dive
  section paragraphs (incl. tabiji-verdict blocks), and FAQ answers.
  Skip: nav, footer, TOC sidebar/mobile, JSON-LD, methodology box (boilerplate),
  photo grids, score ticker, comparison/cost tables, scorecard. These are
  either template fixtures or non-prose data that would pollute the slop signal.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

from bs4 import BeautifulSoup, Tag

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "docs" / "data" / "veracity-experiment" / "scores"
API_URL = "https://api.veracityapi.com/v1/analyze"

# DOM elements to strip before extracting prose. The page-wide layout shell
# (nav, breadcrumb, TOC, score ticker) and tabular/structured data go.
STRIP_TAGS = ("script", "style", "noscript", "nav", "aside", "svg")
STRIP_SELECTORS = (
    ".methodology-box",      # boilerplate "How we built this comparison"
    ".photo-grid",           # img + short captions
    ".toc-mobile",           # mobile TOC
    ".score-ticker",         # header ticker
    ".scorecard",            # number-heavy summary
    ".cost-table",           # all numbers
    ".comparison-table",     # all numbers
    ".quick-comparison",     # facts table
    ".breadcrumb",           # in case any stragglers
    ".page-breadcrumbs",     # JS-injected, but defensive
    "table",                 # any other table
    "[data-byline]",         # byline block (just author name)
    ".hero-meta",            # "Updated:", "Sources:", "Data:"
    ".hero-badge",           # tag-style label
    ".verdict-takeaways",    # short bullets, not prose — left out for round 1
)


def extract_prose(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    # Strip whole elements
    for t in STRIP_TAGS:
        for el in soup.find_all(t):
            el.decompose()
    for sel in STRIP_SELECTORS:
        for el in soup.select(sel):
            el.decompose()
    # Anchor extraction to <main>; outside is nav/footer
    main = soup.find("main")
    root = main if main else soup.body or soup
    # Collapse whitespace, drop empty paragraphs
    text = root.get_text(separator="\n", strip=True)
    # Normalize runs of blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def call_veracity(prose: str, api_key: str) -> dict:
    body = {
        "type": "text",
        "content": prose,
        "auto_revise": False,  # we'll do rewrites ourselves
        "context": {"format": "article", "intended_use": "publish"},
        "store_content": False,
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            # Default Python-urllib UA is blocked by Cloudflare (error 1010);
            # send a normal-looking UA so the request passes the WAF.
            "User-Agent": "tabiji-veracity-experiment/1.0 (+https://tabiji.ai)",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return {"http_status": resp.status, "body": json.loads(resp.read().decode("utf-8"))}
    except urllib.error.HTTPError as e:
        return {"http_status": e.code, "error": e.read().decode("utf-8", errors="replace")}


def score_slug(slug: str, api_key: str) -> dict:
    page_path = REPO_ROOT / "compare" / slug / "index.html"
    if not page_path.exists():
        raise SystemExit(f"page not found: {page_path}")
    html = page_path.read_text(encoding="utf-8")
    prose = extract_prose(html)
    char_len = len(prose)
    word_count = len(prose.split())
    resp = call_veracity(prose, api_key)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "slug": slug,
        "prose_chars": char_len,
        "prose_words": word_count,
        "prose_sent": prose,
        "response": resp,
    }
    out_path = OUT_DIR / f"{slug}.json"
    out_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    return record


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--all-cohort", action="store_true",
                    help="score every page in docs/data/veracity-experiment/cohort.json")
    args = ap.parse_args()
    api_key = os.environ.get("VERACITY_API_KEY")
    if not api_key:
        raise SystemExit("VERACITY_API_KEY env var required")

    if args.all_cohort:
        cohort = json.loads((REPO_ROOT / "docs" / "data" / "veracity-experiment" / "cohort.json").read_text())
        for row in cohort:
            slug = row["slug"]
            print(f"scoring {slug}...", file=sys.stderr)
            rec = score_slug(slug, api_key)
            print(f"  http={rec['response'].get('http_status')}  chars={rec['prose_chars']}", file=sys.stderr)
        return 0

    if not args.slug:
        raise SystemExit("usage: veracity_score.py <slug>  OR  --all-cohort")
    rec = score_slug(args.slug, api_key)
    # Print just the response summary (the full record is on disk)
    print(json.dumps({
        "slug": rec["slug"],
        "prose_chars": rec["prose_chars"],
        "prose_words": rec["prose_words"],
        "response": rec["response"],
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
