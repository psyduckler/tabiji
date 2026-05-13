#!/usr/bin/env python3
"""Generate sitemap.xml from all index.html files in the repo.

Excludes:
  - Top-level book-* source/manuscript dirs (book-italy/, etc.)
  - Internal/auth/private trees: /i/, /media/, /thanks/, /tmp/, /archive/
  - Pages with <meta name="robots" content="...noindex...">
  - Meta-refresh redirect stubs

Uses per-file last-commit date from git log for <lastmod> (so the sitemap
reflects actual content changes per URL rather than a blanket build-date).
"""
import os
import re
import subprocess
from datetime import datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://tabiji.ai'
EXCLUDE_DIRS = {
    'tmp', 'archive', '_includes', '.git', '.claude', 'node_modules',
    '.next', '.wrangler', '.well-known',
    # Internal/private trees we don't want Google indexing
    'i', 'media', 'thanks',
}

NOINDEX_RE = re.compile(
    r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*noindex',
    re.IGNORECASE,
)


def is_excluded_path(rel_path):
    """Exclude top-level book-* source/manuscript dirs.
    These contain manuscripts, briefs, and dev prototypes — not site content."""
    first = rel_path.split(os.sep, 1)[0]
    return first.startswith('book-') or first == 'book'


def get_priority(path):
    if path == '/': return '1.0'
    if path == '/plan/': return '0.9'
    if path in ('/destinations/', '/compare/', '/popular-picks/', '/scams/', '/countries/', '/health/'): return '0.8'
    if path.startswith('/destinations/') and path.count('/') == 3: return '0.7'
    if path.startswith('/countries/'): return '0.7'
    if path.startswith('/health/'): return '0.7'
    if path.startswith('/compare/') and '-vs-' in path: return '0.6'
    if path.startswith('/popular-picks/'): return '0.6'
    if path.startswith('/scams/'): return '0.7'
    return '0.5'


def get_changefreq(path):
    if path == '/': return 'daily'
    if path in ('/compare/', '/popular-picks/', '/destinations/', '/scams/', '/countries/', '/health/'): return 'weekly'
    if path.startswith('/popular-picks/'): return 'weekly'
    if path.startswith('/scams/'): return 'weekly'
    return 'monthly'


def is_redirect_stub(html_path):
    """Skip pages that immediately redirect — they're not canonical destinations."""
    try:
        with open(html_path, 'r', errors='replace') as f:
            head = f.read(8192)  # meta-refresh always lives in <head>
    except OSError:
        return False
    return 'http-equiv="refresh"' in head or "http-equiv='refresh'" in head


def has_noindex(html_path):
    """Skip pages with a noindex robots meta — they shouldn't be in the sitemap."""
    try:
        with open(html_path, 'r', errors='replace') as f:
            head = f.read(16384)
    except OSError:
        return False
    return bool(NOINDEX_RE.search(head))


def build_git_lastmod_map():
    """Build {repo-relative-path: YYYY-MM-DD} from one git log pass.
    Maps each file to the date of the most recent commit that touched it.
    Returns empty dict if git is unavailable (falls back to today's date)."""
    try:
        out = subprocess.check_output(
            ['git', '-C', REPO, 'log', '--name-only', '--format=__C__ %cs'],
            text=True, stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {}

    file_dates = {}
    current_date = None
    for line in out.split('\n'):
        if line.startswith('__C__ '):
            current_date = line[len('__C__ '):]
        elif line.strip() and current_date and line not in file_dates:
            # First time we see a path = most recent commit (git log is newest-first)
            file_dates[line] = current_date
    return file_dates


def main():
    lastmod_map = build_git_lastmod_map()
    today = datetime.now().strftime('%Y-%m-%d')

    pages = []
    skipped_redirects = 0
    skipped_noindex = 0
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        if 'index.html' not in files:
            continue
        rel = os.path.relpath(root, REPO)
        if rel != '.' and is_excluded_path(rel):
            continue
        html_path = os.path.join(root, 'index.html')
        if is_redirect_stub(html_path):
            skipped_redirects += 1
            continue
        if has_noindex(html_path):
            skipped_noindex += 1
            continue
        path = '/' if rel == '.' else f'/{rel}/'
        rel_file = os.path.relpath(html_path, REPO)
        lastmod = lastmod_map.get(rel_file, today)
        pages.append((path, lastmod))
    pages.sort()

    lines = ["<?xml version='1.0' encoding='utf-8'?>", '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, lastmod in pages:
        lines.append(
            f'  <url>\n    <loc>{BASE}{path}</loc>\n'
            f'    <lastmod>{lastmod}</lastmod>\n'
            f'    <changefreq>{get_changefreq(path)}</changefreq>\n'
            f'    <priority>{get_priority(path)}</priority>\n  </url>'
        )
    lines.append('</urlset>')

    out = os.path.join(REPO, 'sitemap.xml')
    with open(out, 'w') as f:
        f.write('\n'.join(lines))

    unique_dates = len({lm for _, lm in pages})
    print(
        f'sitemap.xml: {len(pages)} URLs, {unique_dates} unique lastmod dates '
        f'({skipped_redirects} redirect stubs, {skipped_noindex} noindex skipped)'
    )


if __name__ == '__main__':
    main()
