# Locked Resource Page Standard

This is the production standard for `/resources/` pages.

## Goal

Make resource pages feel intentional and reusable instead of essay-shaped one-offs.

The shell should be predictable enough that:
- writers fill a schema instead of hand-rolling layout
- metadata and structured data stay consistent
- readers always get the same scanning affordances
- audits can be automated

## Required article types

### 1) Data / teardown article
Use for experiments, tests, benchmarks, or original findings.

Required flow:
1. hero
2. key takeaways
3. methodology / dataset / setup
4. findings
5. implications / what this means
6. FAQ
7. CTA

### 2) Comparison article
Use for product, tool, service, or option comparisons.

Required flow:
1. hero
2. quick verdict
3. key takeaways
4. comparison table
5. deep dives
6. who should choose what / decision framework
7. FAQ
8. CTA

### 3) Guide / explainer article
Use for evergreen how-to, packing-list, or educational pages.

Required flow:
1. hero
2. TL;DR / key takeaways
3. steps / framework / categories
4. examples or supporting evidence
5. FAQ
6. CTA

## Required shell blocks on every page

1. shared head partial
2. shared nav partial
3. hero
4. sticky TOC + mobile TOC
5. visible summary block (`key-takeaways`, `quick-verdict`, or `tldr`)
6. main article body
7. FAQ section
8. CTA section
9. shared footer partial

## Required metadata

Every resource page must include:
- canonical
- title
- meta description
- robots
- `og:title`
- `og:description`
- `og:type`
- `og:url`
- `og:image`
- `twitter:card`
- `twitter:title`
- `twitter:description`
- `twitter:image`
- author
- publish date
- modified date

## Required schema

Every resource page must include:
- `Article`
- `BreadcrumbList`
- `FAQPage` when an FAQ section exists

Preferred for the reference shell:
- `mainEntityOfPage`
- `image`
- `speakable`

## Recommended page-data contract

Each page should declare structured page data with at least:

```json
{
  "slug": "best-ai-travel-planners-2026",
  "title": "The Best AI Travel Planners in 2026: An Honest Comparison",
  "description": "We compared 8 AI travel planners...",
  "article_type": "comparison",
  "published": "2026-02-11",
  "updated": "2026-03-18",
  "author": "tabiji.ai",
  "hero_label": "AI travel planning",
  "hero_image": "https://img.tabiji.ai/resources/hero-default.jpg",
  "og_image": "https://img.tabiji.ai/resources/hero-default.jpg",
  "read_time": "9 min read",
  "key_takeaways": [
    "Dedicated planners beat ChatGPT when structure matters.",
    "ChatGPT is still strong for open-ended ideation.",
    "The right tool depends on whether you need ideas, logistics, or collaboration."
  ],
  "faq": [
    {
      "question": "What is the best free AI travel planner?",
      "answer": "..."
    }
  ],
  "cta_variant": "plan-trip"
}
```

## Reference implementation choice

Use `resources/best-ai-travel-planners-2026/index.html` as the first reference implementation for the comparison shell.

Why:
- strategically important query cluster
- currently missing several standard elements
- broad enough to act as the reusable comparison archetype
- easy to judge visually and structurally after migration

## Migration checklist

For each legacy resource page:
- classify article type
- add missing social metadata
- add `BreadcrumbList`
- add or normalize visible takeaways/TL;DR
- add or normalize FAQ section
- add or normalize CTA section
- normalize TOC markup and section anchors
- confirm shared partial markers are intact
- validate shell against the audit script
