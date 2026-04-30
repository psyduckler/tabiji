#!/usr/bin/env python3
"""Audit sitemap.xml against the deployed site:
  1) Find URLs in sitemap that point to non-existent files (DEAD).
  2) Find indexable HTML routes on disk that are missing from sitemap (MISSING).

Honors robots.txt disallows, _redirects 301/410 entries, and per-page
<meta name="robots" content="noindex"> tags.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITEMAP = REPO / "sitemap.xml"
ORIGIN = "https://tabiji.ai/"

# Filesystem-level excludes (never indexable / never on prod)
EXCLUDE_DIRS = {
    ".git", ".github", ".claude", ".claude-skills",
    "node_modules", "tmp", "scripts", "_includes", "samples",
    "popular-picks-data", "compare-data", "delete-data", "pending",
    "tabiji-books",
}
# Path prefixes (relative to repo root) we never want in the sitemap.
EXCLUDE_PATH_PREFIXES = (
    "api/v1/",                 # robots disallow
    "tmp/",                    # robots disallow
    "book-",                   # source/build trees, NOT served
    "export-doc/",             # exports
    "research/",               # raw research dumps
    "popular-picks-master",    # raw queue files
    "country-fills-queue",
)
# Known root-level files that aren't routes
EXCLUDE_FILES = {
    "404.html", "success.html", "thanks.html", "plan.html",
    "CLAUDE.md", "DESIGN.md", "ARCHITECTURE.md", "SECURITY.md",
}
# Robots / 410 patterns (URLs that exist on disk but should NOT be indexed).
INDEX_DENY_PATTERNS = [
    re.compile(r"^https://tabiji\.ai/api/v1/"),
    re.compile(r"^https://tabiji\.ai/tmp/"),
    re.compile(r"^https://tabiji\.ai/credit-cards/"),
    re.compile(r"^https://tabiji\.ai/i/[^/]+/?$"),  # itinerary export pages — usually noindex
]


def url_to_relpath(url: str) -> str | None:
    """Reverse-map a sitemap URL to the file path that would serve it."""
    if not url.startswith(ORIGIN):
        return None
    p = url[len(ORIGIN):].rstrip("/")
    if p == "":
        return "index.html"
    return f"{p}/index.html"


def relpath_to_url(rel: Path) -> str:
    parts = rel.parts
    if rel.name == "index.html":
        if len(parts) == 1:
            return ORIGIN
        return ORIGIN + "/".join(parts[:-1]) + "/"
    return ORIGIN + "/".join(parts)


def is_excluded_path(parts: tuple[str, ...]) -> bool:
    if any(p in EXCLUDE_DIRS for p in parts):
        return True
    rel = "/".join(parts)
    if any(rel.startswith(prefix) for prefix in EXCLUDE_PATH_PREFIXES):
        return True
    return False


def is_noindex(html_path: Path) -> bool:
    """Cheap check: scan first ~5KB for noindex meta tag."""
    try:
        head = html_path.read_text(errors="ignore")[:5000].lower()
    except OSError:
        return False
    return 'name="robots"' in head and "noindex" in head.split('name="robots"', 1)[1][:200]


def is_redirected(rel: str, redirects: dict[str, str]) -> bool:
    """Check if a path is a 301/410 source in _redirects."""
    rel_norm = "/" + rel.replace("index.html", "")
    return rel_norm in redirects


def load_redirects() -> dict[str, str]:
    """Map source→destination from _redirects file (301/410 entries)."""
    redirects: dict[str, str] = {}
    redirects_file = REPO / "_redirects"
    if not redirects_file.exists():
        return redirects
    for line in redirects_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 3 and parts[2] in ("301", "302", "410"):
            src = parts[0].rstrip("/") + "/"
            redirects[src] = parts[1]
    return redirects


def main() -> None:
    sitemap_text = SITEMAP.read_text()
    sitemap_urls = set(re.findall(r"<loc>([^<]+)</loc>", sitemap_text))

    redirects = load_redirects()

    # 1. DEAD: sitemap URL → no file on disk
    dead = []
    for url in sorted(sitemap_urls):
        rel = url_to_relpath(url)
        if rel is None:
            dead.append((url, "non-tabiji domain"))
            continue
        path = REPO / rel
        if not path.exists():
            dead.append((url, "no file"))
        elif is_noindex(path):
            dead.append((url, "page is noindex"))

    # 2. MISSING: HTML route exists, but URL not in sitemap
    missing = []
    for html_path in REPO.rglob("index.html"):
        rel = html_path.relative_to(REPO)
        if is_excluded_path(rel.parts):
            continue
        if rel.name in EXCLUDE_FILES:
            continue
        if is_noindex(html_path):
            continue
        url = relpath_to_url(rel)
        # Skip if covered by an INDEX_DENY pattern
        if any(p.match(url) for p in INDEX_DENY_PATTERNS):
            continue
        # Skip if the URL is a 301/410 source
        rel_path = url[len(ORIGIN) - 1:]  # leading slash
        if rel_path in redirects:
            continue
        if url not in sitemap_urls:
            missing.append(url)

    # 3. Report
    print(f"Sitemap URLs:        {len(sitemap_urls):>5}")
    print(f"DEAD (in sitemap, file gone or noindex): {len(dead)}")
    print(f"MISSING (file exists, not in sitemap):   {len(missing)}")
    print()

    if dead:
        print(f"=== DEAD URLs ({len(dead)}) ===")
        from collections import Counter
        reasons = Counter(reason for _, reason in dead)
        for r, n in reasons.most_common():
            print(f"  · {n} × {r}")
        print()
        for url, reason in dead[:20]:
            print(f"    [{reason}] {url}")
        if len(dead) > 20:
            print(f"    … and {len(dead) - 20} more")
        print()

    if missing:
        print(f"=== MISSING URLs ({len(missing)}) ===")
        # Group by top-level path segment for sanity
        from collections import Counter
        prefixes = Counter()
        for url in missing:
            seg = url[len(ORIGIN):].split("/", 1)[0]
            prefixes[seg] += 1
        for seg, n in prefixes.most_common():
            print(f"  · {n} × /{seg}/")
        print()
        for url in missing[:30]:
            print(f"    {url}")
        if len(missing) > 30:
            print(f"    … and {len(missing) - 30} more")


if __name__ == "__main__":
    main()
