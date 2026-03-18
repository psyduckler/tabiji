#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT / "resources"
OUT = RESOURCES / "RESOURCE_PAGE_AUDIT_2026-03-18.md"

CHECKS = [
    ("canonical", lambda t: 'rel="canonical"' in t),
    ("meta_description", lambda t: 'name="description"' in t),
    ("og_image", lambda t: 'property="og:image"' in t),
    ("twitter_image", lambda t: 'name="twitter:image"' in t),
    ("article_schema", lambda t: '"@type":"Article"' in t or '"@type": "Article"' in t),
    ("breadcrumb_schema", lambda t: 'BreadcrumbList' in t),
    ("faq_schema", lambda t: 'FAQPage' in t),
    ("sticky_toc", lambda t: 'toc-sidebar' in t or 'toc-mobile-wrapper' in t),
    ("takeaways_block", lambda t: 'key takeaways' in t.lower() or 'quick takeaways' in t.lower() or 'tldr' in re.sub(r'[^a-z]','', t.lower())),
    ("cta_block", lambda t: 'cta-section' in t or 'Get a Free Itinerary' in t or 'Start planning with tabiji' in t),
    ("shared_partials", lambda t: '@include:shared-head' in t and '@include:nav:start' in t and '@include:footer:start' in t),
]


def detect_type(slug: str, text: str) -> str:
    s = slug.lower()
    if 'vs' in s or 'comparison' in s or 'best-' in s:
        return 'comparison'
    if 'packing-list' in s or 'forgotten' in s or 'how-' in s or 'does-' in s or 'can-' in s or 'why-' in s:
        return 'guide'
    return 'data-teardown'


def status(v: bool) -> str:
    return '✅' if v else '—'


pages = []
for path in sorted(RESOURCES.glob('*/index.html')):
    text = path.read_text()
    row = {'slug': path.parent.name, 'type': detect_type(path.parent.name, text)}
    for key, fn in CHECKS:
        row[key] = bool(fn(text))
    pages.append(row)

summary = {key: sum(1 for p in pages if p[key]) for key, _ in CHECKS}

total = len(pages)
lines = []
lines.append('# Resource Page Audit — 2026-03-18')
lines.append('')
lines.append(f'Audited **{total}** `/resources/` leaf pages against the proposed locked resource-page standard.')
lines.append('')
lines.append('## Headline findings')
lines.append('')
lines.append(f'- Shared nav/head/footer partials are already in place on **{summary["shared_partials"]}/{total}** pages.')
lines.append(f'- Sticky/mobile TOC exists on **{summary["sticky_toc"]}/{total}** pages.')
lines.append(f'- `BreadcrumbList` schema exists on **{summary["breadcrumb_schema"]}/{total}** pages.')
lines.append(f'- `og:image` exists on **{summary["og_image"]}/{total}** pages; `twitter:image` on **{summary["twitter_image"]}/{total}** pages.')
lines.append(f'- Visible takeaway/TL;DR blocks exist on **{summary["takeaways_block"]}/{total}** pages.')
lines.append(f'- `FAQPage` schema exists on **{summary["faq_schema"]}/{total}** pages.')
lines.append('')
lines.append('## Page-by-page matrix')
lines.append('')
headers = ['slug', 'type'] + [key for key, _ in CHECKS]
lines.append('| ' + ' | '.join(headers) + ' |')
lines.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')
for p in pages:
    lines.append('| ' + ' | '.join([p['slug'], p['type']] + [status(p[key]) for key, _ in CHECKS]) + ' |')
lines.append('')
lines.append('## Priorities')
lines.append('')
lines.append('1. Add a locked resource shell so takeaways / FAQ / CTA are required, not optional.')
lines.append('2. Backfill missing social metadata and Breadcrumb schema across all legacy pages.')
lines.append('3. Stop hand-rolling page architecture; generate from page data + a small number of article-type templates.')
lines.append('4. Use one upgraded page as the visual and structural reference implementation before migrating the full set.')
lines.append('')
lines.append('## Raw JSON')
lines.append('')
lines.append('```json')
lines.append(json.dumps(pages, indent=2))
lines.append('```')
lines.append('')
OUT.write_text('\n'.join(lines) + '\n')
print(f'Wrote {OUT.relative_to(ROOT)}')
