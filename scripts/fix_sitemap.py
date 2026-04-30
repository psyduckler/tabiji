#!/usr/bin/env python3
"""Fix sitemap.xml based on audit_sitemap.py findings:
  - Remove URLs pointing to noindex pages (DEAD).
  - Add HTML routes that exist on disk but aren't in the sitemap (MISSING).

Re-uses the same exclusion + url-mapping logic as audit_sitemap.py.
Idempotent: re-running on a clean sitemap is a no-op.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITEMAP = REPO / "sitemap.xml"
ORIGIN = "https://tabiji.ai/"

# Mirror audit_sitemap.py
EXCLUDE_DIRS = {
    ".git", ".github", ".claude", ".claude-skills",
    "node_modules", "tmp", "scripts", "_includes", "samples",
    "popular-picks-data", "compare-data", "delete-data", "pending",
    "tabiji-books",
}
EXCLUDE_PATH_PREFIXES = (
    "api/v1/", "tmp/", "book-", "export-doc/", "research/",
    "popular-picks-master", "country-fills-queue",
)
EXCLUDE_FILES = {"404.html", "success.html", "thanks.html", "plan.html"}
INDEX_DENY_PATTERNS = [
    re.compile(r"^https://tabiji\.ai/api/v1/"),
    re.compile(r"^https://tabiji\.ai/tmp/"),
    re.compile(r"^https://tabiji\.ai/credit-cards/"),
    re.compile(r"^https://tabiji\.ai/i/[^/]+/?$"),
]


def url_to_relpath(url: str) -> str | None:
    if not url.startswith(ORIGIN):
        return None
    p = url[len(ORIGIN):].rstrip("/")
    return "index.html" if p == "" else f"{p}/index.html"


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
    return any(rel.startswith(p) for p in EXCLUDE_PATH_PREFIXES)


def is_noindex(html_path: Path) -> bool:
    try:
        head = html_path.read_text(errors="ignore")[:5000].lower()
    except OSError:
        return False
    return 'name="robots"' in head and "noindex" in head.split('name="robots"', 1)[1][:200]


def load_redirects() -> set[str]:
    redirects: set[str] = set()
    f = REPO / "_redirects"
    if not f.exists():
        return redirects
    for line in f.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 3 and parts[2] in ("301", "302", "410"):
            redirects.add(parts[0].rstrip("/") + "/")
    return redirects


def git_lastmod(rel_path: str) -> str:
    """YYYY-MM-DD of the file's last commit, or today if untracked."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ai", "--", rel_path],
            capture_output=True, text=True, cwd=REPO, timeout=10,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip().split(" ")[0]
    except Exception:
        pass
    from datetime import date
    return date.today().isoformat()


def main() -> None:
    text = SITEMAP.read_text()
    # Parse <url>…</url> blocks
    block_re = re.compile(r"  <url>.*?</url>\n", re.DOTALL)
    blocks = block_re.findall(text)
    header = text.split("  <url>", 1)[0]
    footer = "</urlset>\n"

    # 1. Filter out blocks whose URL points to noindex / missing files
    keep, removed = [], []
    for blk in blocks:
        m = re.search(r"<loc>([^<]+)</loc>", blk)
        if not m:
            continue
        url = m.group(1)
        rel = url_to_relpath(url)
        if rel is None:
            removed.append((url, "non-tabiji"))
            continue
        path = REPO / rel
        if not path.exists():
            removed.append((url, "no file"))
            continue
        if is_noindex(path):
            removed.append((url, "noindex"))
            continue
        keep.append(blk)

    existing_urls = {re.search(r"<loc>([^<]+)</loc>", b).group(1) for b in keep}

    # 2. Find missing URLs
    redirects = load_redirects()
    additions = []
    for html_path in REPO.rglob("index.html"):
        rel = html_path.relative_to(REPO)
        if is_excluded_path(rel.parts) or rel.name in EXCLUDE_FILES:
            continue
        if is_noindex(html_path):
            continue
        url = relpath_to_url(rel)
        if any(p.match(url) for p in INDEX_DENY_PATTERNS):
            continue
        rel_url_path = url[len(ORIGIN) - 1:]
        if rel_url_path in redirects:
            continue
        if url in existing_urls:
            continue
        additions.append((url, str(rel)))

    # 3. Determine changefreq/priority by URL prefix
    def freq_priority(url: str) -> tuple[str, str]:
        path = url[len(ORIGIN):]
        if path.startswith("scams/atlas/"):
            return ("weekly", "0.7")
        if path.startswith("scams/"):
            return ("weekly", "0.7")
        if path.startswith("books/"):
            return ("monthly", "0.7")
        if path.startswith("countries/"):
            return ("monthly", "0.7")
        if path.startswith("compare/"):
            return ("monthly", "0.6")
        if path.startswith("popular-picks/"):
            return ("monthly", "0.6")
        return ("monthly", "0.5")

    # 4. Build new <url> blocks for additions
    new_blocks = []
    for url, rel in additions:
        lastmod = git_lastmod(rel)
        cf, pr = freq_priority(url)
        new_blocks.append(
            f"  <url>\n"
            f"    <loc>{url}</loc>\n"
            f"    <lastmod>{lastmod}</lastmod>\n"
            f"    <changefreq>{cf}</changefreq>\n"
            f"    <priority>{pr}</priority>\n"
            f"  </url>\n"
        )

    # 5. Sort all blocks alphabetically by URL for stable diffs
    all_blocks = keep + new_blocks
    all_blocks.sort(key=lambda b: re.search(r"<loc>([^<]+)</loc>", b).group(1))

    new_text = header + "".join(all_blocks) + footer
    SITEMAP.write_text(new_text)

    print(f"Removed: {len(removed)} URL(s)")
    for url, reason in removed[:5]:
        print(f"  - [{reason}] {url}")
    if len(removed) > 5:
        print(f"  … and {len(removed) - 5} more")
    print(f"\nAdded: {len(additions)} URL(s)")
    for url, _ in additions:
        print(f"  + {url}")
    print(f"\nFinal: {len(all_blocks)} URLs in sitemap")


if __name__ == "__main__":
    main()
