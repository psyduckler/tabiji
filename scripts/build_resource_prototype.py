#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'resources' / '_templates' / 'resource-page-prototype.html'
EXAMPLE = ROOT / 'resources' / '_templates' / 'resource-page-fields.example.json'
OUT = ROOT / 'tmp' / 'resource-page-prototype.example.html'


def li(items: list[str], *, escape: bool = True) -> str:
    if escape:
        return '\n'.join(f'<li>{html.escape(item)}</li>' for item in items)
    return '\n'.join(f'<li>{item}</li>' for item in items)


def faq_html(items: list[dict[str, str]]) -> str:
    return '\n'.join(
        f'<details><summary>{html.escape(item["question"])}</summary><p>{html.escape(item["answer"])}</p></details>'
        for item in items
    )


def faq_schema(items: list[dict[str, str]]) -> str:
    data = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {
                '@type': 'Question',
                'name': item['question'],
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': item['answer'],
                },
            }
            for item in items
        ],
    }
    return json.dumps(data, separators=(',', ':'))


page = json.loads(EXAMPLE.read_text())
template = TEMPLATE.read_text()
article_schema = json.dumps({
    '@context': 'https://schema.org',
    '@type': 'Article',
    'headline': page['title'],
    'description': page['description'],
    'author': {'@type': 'Organization', 'name': page['author']},
    'publisher': {'@type': 'Organization', 'name': 'tabiji.ai', 'url': 'https://tabiji.ai'},
    'datePublished': page['published'],
    'dateModified': page['updated'],
    'mainEntityOfPage': f'https://tabiji.ai/resources/{page["slug"]}/',
    'image': page['og_image'],
}, separators=(',', ':'))
breadcrumb_schema = json.dumps({
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': 'https://tabiji.ai/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Resources', 'item': 'https://tabiji.ai/resources/'},
        {'@type': 'ListItem', 'position': 3, 'name': page['title'], 'item': f'https://tabiji.ai/resources/{page["slug"]}/'},
    ],
}, separators=(',', ':'))
replacements = {
    '{{ title }}': page['title'],
    '{{ description }}': page['description'],
    '{{ slug }}': page['slug'],
    '{{ og_image }}': page['og_image'],
    '{{ author }}': page['author'],
    '{{ published }}': page['published'],
    '{{ updated }}': page['updated'],
    '{{ article_type }}': page['article_type'],
    '{{ hero_label }}': page['hero_label'],
    '{{ read_time }}': page['read_time'],
    '{{ toc_items_html }}': li([f'<a href="#{item["id"]}">{html.escape(item["label"])}</a>' for item in page['toc']], escape=False),
    '{{ takeaways_html }}': li(page['key_takeaways']),
    '{{ body_html }}': '<section id="quick-verdict"><h2>Quick verdict</h2><p>Reference implementation body goes here.</p></section>',
    '{{ faq_html }}': faq_html(page['faq']),
    '{{ cta_eyebrow }}': page['cta']['eyebrow'],
    '{{ cta_title }}': page['cta']['title'],
    '{{ cta_body }}': page['cta']['body'],
    '{{ cta_href }}': page['cta']['href'],
    '{{ cta_label }}': page['cta']['label'],
    '{{ article_schema_json }}': article_schema,
    '{{ breadcrumb_schema_json }}': breadcrumb_schema,
    '{{ faq_schema_json }}': faq_schema(page['faq']),
}

for old, new in replacements.items():
    template = template.replace(old, new)

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(template)
print(f'Wrote {OUT.relative_to(ROOT)}')
