#!/usr/bin/env python3
"""Generate sitemap.xml from all index.html files in the repo."""
import os
from datetime import datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://tabiji.ai'
EXCLUDE_DIRS = {'tmp', 'scam', 'archive', '_includes', '.git', 'node_modules', '.next', '.wrangler', '.well-known'}

def get_priority(path):
    if path == '/': return '1.0'
    if path == '/plan/': return '0.9'
    if path in ('/destinations/', '/compare/', '/popular-picks/', '/scams/', '/alerts/'): return '0.8'
    if path.startswith('/destinations/') and path.count('/') == 3: return '0.7'
    if path.startswith('/compare/') and '-vs-' in path: return '0.6'
    if path.startswith('/popular-picks/'): return '0.6'
    if path.startswith('/scams/'): return '0.7'
    if path.startswith('/i/'): return '0.5'
    if path.startswith('/alerts/'): return '0.4'
    if path.startswith('/resources/'): return '0.5'
    return '0.5'

def get_changefreq(path):
    if path == '/': return 'daily'
    if path in ('/compare/', '/popular-picks/', '/destinations/', '/alerts/', '/scams/'): return 'weekly'
    if path.startswith('/alerts/'): return 'weekly'
    return 'monthly'

def main():
    pages = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        if 'index.html' in files:
            rel = os.path.relpath(root, REPO)
            path = '/' if rel == '.' else f'/{rel}/'
            pages.append(path)
    pages.sort()

    today = datetime.now().strftime('%Y-%m-%d')
    lines = ["<?xml version='1.0' encoding='utf-8'?>", '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path in pages:
        lines.append(f'  <url>\n    <loc>{BASE}{path}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>{get_changefreq(path)}</changefreq>\n    <priority>{get_priority(path)}</priority>\n  </url>')
    lines.append('</urlset>')

    out = os.path.join(REPO, 'sitemap.xml')
    with open(out, 'w') as f:
        f.write('\n'.join(lines))
    print(f'sitemap.xml: {len(pages)} URLs')

if __name__ == '__main__':
    main()
