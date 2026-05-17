#!/usr/bin/env python3
"""Audit sitemap.xml against live HTML pages on disk.

Rules:
  - Drop URLs in sitemap whose page has `<meta name="robots" content="noindex...">`.
  - Drop URLs in sitemap whose page isn't on disk at all.
  - Add URLs for live, indexable pages that aren't in sitemap.
  - Preserve existing <lastmod> / <changefreq> / <priority> for kept URLs.
  - Use category-convention defaults for added URLs (inferred from the
    most-common existing values per top-level path segment).

Writes sitemap.xml in place. Run with --dry-run to preview.
"""

from __future__ import annotations

import argparse
import os
import re
from collections import Counter
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SITEMAP = REPO / "sitemap.xml"
SITE = "https://tabiji.ai"

# Directories we never treat as public pages.
# Kept aligned with EXCLUDE_DIRS in scripts/generate_sitemap.py — drift between
# the two leaked /media/ and book-*/assets/cover-prototypes/ URLs into the
# sitemap. Any addition here should be mirrored there (and vice versa).
NON_PAGE_DIRS = {
    ".git", ".claude", "node_modules",
    "scripts", "api", "functions", ".well-known",
    "compare-data", "scam-data",
    "itinerary-data",
    "media",
}


def is_noindex(html: str) -> bool:
    m = re.search(
        r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)',
        html, re.I,
    )
    return bool(m and "noindex" in m.group(1).lower())


def find_live_pages() -> tuple[set[str], set[str]]:
    """Walk the repo for index.html files. Return (indexable, noindex) URL sets."""
    live: set[str] = set()
    noindex: set[str] = set()
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [
            d for d in dirs
            if d not in NON_PAGE_DIRS
            and not d.startswith(".")
            and not d.startswith("book-")
            and d != "book"
        ]
        if "index.html" not in files:
            continue
        rel = os.path.relpath(root, REPO)
        rel = "" if rel == "." else rel.replace(os.sep, "/")
        # /api/ is a public docs page even though we skip subpaths
        url = f"{SITE}/" if not rel else f"{SITE}/{rel}/"
        try:
            html = Path(root, "index.html").read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if is_noindex(html):
            noindex.add(url)
        else:
            live.add(url)

    # Special-case: api/index.html lives under the normally-skipped 'api'
    # directory, but /api/ is a public docs page.
    api_html = REPO / "api" / "index.html"
    if api_html.exists():
        html = api_html.read_text(encoding="utf-8", errors="replace")
        u = f"{SITE}/api/"
        if is_noindex(html):
            noindex.add(u)
        else:
            live.add(u)
    return live, noindex


URL_BLOCK_RE = re.compile(
    r"<url>\s*<loc>(?P<loc>[^<]+)</loc>"
    r"\s*(?:<lastmod>(?P<lastmod>[^<]+)</lastmod>)?"
    r"\s*(?:<changefreq>(?P<cf>[^<]+)</changefreq>)?"
    r"\s*(?:<priority>(?P<pr>[^<]+)</priority>)?"
    r"\s*</url>",
    re.DOTALL,
)


def parse_sitemap(content: str) -> list[dict]:
    """Return list of {loc, lastmod, changefreq, priority} in document order."""
    return [
        {
            "loc": m.group("loc").strip(),
            "lastmod": (m.group("lastmod") or "").strip(),
            "changefreq": (m.group("cf") or "").strip(),
            "priority": (m.group("pr") or "").strip(),
        }
        for m in URL_BLOCK_RE.finditer(content)
    ]


def category_of(url: str) -> str:
    m = re.match(r"https?://[^/]+/([^/]*)", url)
    return m.group(1) if m else ""


def infer_defaults(existing: list[dict]) -> dict[str, tuple[str, str]]:
    """Most-common changefreq+priority per top-level category."""
    cf: dict[str, Counter] = {}
    pr: dict[str, Counter] = {}
    for e in existing:
        c = category_of(e["loc"])
        if e["changefreq"]:
            cf.setdefault(c, Counter())[e["changefreq"]] += 1
        if e["priority"]:
            pr.setdefault(c, Counter())[e["priority"]] += 1
    out: dict[str, tuple[str, str]] = {}
    for c in set(cf) | set(pr):
        top_cf = cf.get(c, Counter()).most_common(1)
        top_pr = pr.get(c, Counter()).most_common(1)
        out[c] = (
            top_cf[0][0] if top_cf else "monthly",
            top_pr[0][0] if top_pr else "0.5",
        )
    return out


def render(entries: list[dict]) -> str:
    lines = ["<?xml version='1.0' encoding='utf-8'?>",
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for e in entries:
        lines.append("  <url>")
        lines.append(f"    <loc>{e['loc']}</loc>")
        if e.get("lastmod"): lines.append(f"    <lastmod>{e['lastmod']}</lastmod>")
        if e.get("changefreq"): lines.append(f"    <changefreq>{e['changefreq']}</changefreq>")
        if e.get("priority"): lines.append(f"    <priority>{e['priority']}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    content = SITEMAP.read_text()
    existing = parse_sitemap(content)
    existing_locs = {e["loc"].rstrip("/") + "/" for e in existing}

    live, noindex = find_live_pages()
    live_norm = {u.rstrip("/") + "/" for u in live}
    noindex_norm = {u.rstrip("/") + "/" for u in noindex}

    # Partition existing
    keep, drop_noindex, drop_missing = [], [], []
    for e in existing:
        loc_norm = e["loc"].rstrip("/") + "/"
        if loc_norm in noindex_norm:
            drop_noindex.append(e["loc"]); continue
        if loc_norm not in live_norm:
            drop_missing.append(e["loc"]); continue
        keep.append(e)

    # Additions
    to_add = sorted(live_norm - existing_locs)

    # Defaults per category from the KEPT entries (keeps old if category already has a pattern)
    defaults = infer_defaults(keep)
    today = date.today().isoformat()
    added = []
    for loc in to_add:
        c = category_of(loc)
        cf, pr = defaults.get(c, ("monthly", "0.5"))
        added.append({"loc": loc, "lastmod": today, "changefreq": cf, "priority": pr})

    # Sort new adds into existing order? We'll append at the end then sort
    # by (category, loc) to keep things tidy.
    final = keep + added
    final.sort(key=lambda e: (category_of(e["loc"]), e["loc"]))

    print(f"Existing URLs: {len(existing)}")
    print(f"  Kept:             {len(keep)}")
    print(f"  Dropped (noindex): {len(drop_noindex)}")
    print(f"  Dropped (missing): {len(drop_missing)}")
    print(f"Added: {len(added)}")
    print(f"Final URLs: {len(final)}")

    if args.dry_run:
        print("\n[dry-run] Not writing sitemap.xml")
        if drop_missing:
            print("Dropping (missing):", drop_missing[:5])
        if added:
            print("Adding (first 5):", [a["loc"] for a in added[:5]])
        return

    SITEMAP.write_text(render(final))
    print(f"\nWrote {SITEMAP}")


if __name__ == "__main__":
    main()
