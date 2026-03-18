# Resource Page Audit — 2026-03-18

Audited **21** `/resources/` leaf pages against the proposed locked resource-page standard.

## Headline findings

- Shared nav/head/footer partials are already in place on **19/21** pages.
- Sticky/mobile TOC exists on **19/21** pages.
- `BreadcrumbList` schema exists on **1/21** pages.
- `og:image` exists on **9/21** pages; `twitter:image` on **2/21** pages.
- Visible takeaway/TL;DR blocks exist on **6/21** pages.
- `FAQPage` schema exists on **7/21** pages.

## Page-by-page matrix

| slug | type | canonical | meta_description | og_image | twitter_image | article_schema | breadcrumb_schema | faq_schema | sticky_toc | takeaways_block | cta_block | shared_partials |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ai-image-generation-comparison | comparison | ✅ | ✅ | ✅ | — | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| ai-music-generation-comparison | comparison | ✅ | ✅ | — | — | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| ai-reels-what-actually-works | data-teardown | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| ai-trip-planner-vs-chatgpt-tokyo | comparison | ✅ | ✅ | — | — | ✅ | — | — | ✅ | — | ✅ | ✅ |
| best-ai-travel-planners-2026 | comparison | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| best-short-form-video-services | comparison | ✅ | ✅ | ✅ | — | ✅ | — | ✅ | ✅ | — | ✅ | ✅ |
| best-travel-planning-ai | comparison | ✅ | ✅ | — | — | ✅ | — | — | ✅ | — | ✅ | ✅ |
| business-trip-packing-list-essentials | guide | ✅ | ✅ | ✅ | — | ✅ | — | — | ✅ | — | ✅ | ✅ |
| can-chatgpt-help-travel-planning | guide | ✅ | ✅ | — | — | ✅ | — | — | ✅ | — | ✅ | ✅ |
| does-costco-do-travel-planning | guide | ✅ | ✅ | — | — | ✅ | — | — | ✅ | — | ✅ | ✅ |
| essential-packing-list-international-travel | guide | ✅ | ✅ | ✅ | — | ✅ | — | — | ✅ | — | ✅ | ✅ |
| essential-travel-packing-list-categories | guide | ✅ | ✅ | ✅ | — | ✅ | — | — | ✅ | — | ✅ | ✅ |
| how-we-use-reddit-to-build-itineraries | guide | ✅ | ✅ | — | — | ✅ | — | — | ✅ | — | ✅ | ✅ |
| is-1-dollar-ai-itinerary-worth-it | data-teardown | ✅ | ✅ | — | — | ✅ | — | — | ✅ | — | ✅ | ✅ |
| nano-banana-vs-grok | comparison | ✅ | ✅ | ✅ | — | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| often-forgotten-beach-vacation-items | guide | ✅ | ✅ | ✅ | — | ✅ | — | — | ✅ | — | ✅ | ✅ |
| slop-iterate-curate-ai-content | data-teardown | ✅ | ✅ | — | — | ✅ | — | — | — | — | ✅ | — |
| true-cost-of-ai-content-production | data-teardown | ✅ | ✅ | — | — | ✅ | — | — | — | — | ✅ | — |
| veo-3-vs-hailuo-minimax-cogvideox-video-generation | comparison | ✅ | ✅ | — | — | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| which-travel-planner-app-best | data-teardown | ✅ | ✅ | — | — | ✅ | — | — | ✅ | — | ✅ | ✅ |
| why-ai-travel-planners-give-generic-recommendations | guide | ✅ | ✅ | — | — | ✅ | — | — | ✅ | — | ✅ | ✅ |

## Priorities

1. Add a locked resource shell so takeaways / FAQ / CTA are required, not optional.
2. Backfill missing social metadata and Breadcrumb schema across all legacy pages.
3. Stop hand-rolling page architecture; generate from page data + a small number of article-type templates.
4. Use one upgraded page as the visual and structural reference implementation before migrating the full set.

## Raw JSON

```json
[
  {
    "slug": "ai-image-generation-comparison",
    "type": "comparison",
    "canonical": true,
    "meta_description": true,
    "og_image": true,
    "twitter_image": false,
    "article_schema": true,
    "breadcrumb_schema": false,
    "faq_schema": true,
    "sticky_toc": true,
    "takeaways_block": true,
    "cta_block": true,
    "shared_partials": true
  },
  {
    "slug": "ai-music-generation-comparison",
    "type": "comparison",
    "canonical": true,
    "meta_description": true,
    "og_image": false,
    "twitter_image": false,
    "article_schema": true,
    "breadcrumb_schema": false,
    "faq_schema": true,
    "sticky_toc": true,
    "takeaways_block": true,
    "cta_block": true,
    "shared_partials": true
  },
  {
    "slug": "ai-reels-what-actually-works",
    "type": "data-teardown",
    "canonical": true,
    "meta_description": true,
    "og_image": true,
    "twitter_image": true,
    "article_schema": true,
    "breadcrumb_schema": false,
    "faq_schema": true,
    "sticky_toc": true,
    "takeaways_block": true,
    "cta_block": true,
    "shared_partials": true
  },
  {
    "slug": "ai-trip-planner-vs-chatgpt-tokyo",
    "type": "comparison",
    "canonical": true,
    "meta_description": true,
    "og_image": false,
    "twitter_image": false,
    "article_schema": true,
    "breadcrumb_schema": false,
    "faq_schema": false,
    "sticky_toc": true,
    "takeaways_block": false,
    "cta_block": true,
    "shared_partials": true
  },
  {
    "slug": "best-ai-travel-planners-2026",
    "type": "comparison",
    "canonical": true,
    "meta_description": true,
    "og_image": true,
    "twitter_image": true,
    "article_schema": true,
    "breadcrumb_schema": true,
    "faq_schema": true,
    "sticky_toc": true,
    "takeaways_block": true,
    "cta_block": true,
    "shared_partials": true
  },
  {
    "slug": "best-short-form-video-services",
    "type": "comparison",
    "canonical": true,
    "meta_description": true,
    "og_image": true,
    "twitter_image": false,
    "article_schema": true,
    "breadcrumb_schema": false,
    "faq_schema": true,
    "sticky_toc": true,
    "takeaways_block": false,
    "cta_block": true,
    "shared_partials": true
  },
  {
    "slug": "best-travel-planning-ai",
    "type": "comparison",
    "canonical": true,
    "meta_description": true,
    "og_image": false,
    "twitter_image": false,
    "article_schema": true,
    "breadcrumb_schema": false,
    "faq_schema": false,
    "sticky_toc": true,
    "takeaways_block": false,
    "cta_block": true,
    "shared_partials": true
  },
  {
    "slug": "business-trip-packing-list-essentials",
    "type": "guide",
    "canonical": true,
    "meta_description": true,
    "og_image": true,
    "twitter_image": false,
    "article_schema": true,
    "breadcrumb_schema": false,
    "faq_schema": false,
    "sticky_toc": true,
    "takeaways_block": false,
    "cta_block": true,
    "shared_partials": true
  },
  {
    "slug": "can-chatgpt-help-travel-planning",
    "type": "guide",
    "canonical": true,
    "meta_description": true,
    "og_image": false,
    "twitter_image": false,
    "article_schema": true,
    "breadcrumb_schema": false,
    "faq_schema": false,
    "sticky_toc": true,
    "takeaways_block": false,
    "cta_block": true,
    "shared_partials": true
  },
  {
    "slug": "does-costco-do-travel-planning",
    "type": "guide",
    "canonical": true,
    "meta_description": true,
    "og_image": false,
    "twitter_image": false,
    "article_schema": true,
    "breadcrumb_schema": false,
    "faq_schema": false,
    "sticky_toc": true,
    "takeaways_block": false,
    "cta_block": true,
    "shared_partials": true
  },
  {
    "slug": "essential-packing-list-international-travel",
    "type": "guide",
    "canonical": true,
    "meta_description": true,
    "og_image": true,
    "twitter_image": false,
    "article_schema": true,
    "breadcrumb_schema": false,
    "faq_schema": false,
    "sticky_toc": true,
    "takeaways_block": false,
    "cta_block": true,
    "shared_partials": true
  },
  {
    "slug": "essential-travel-packing-list-categories",
    "type": "guide",
    "canonical": true,
    "meta_description": true,
    "og_image": true,
    "twitter_image": false,
    "article_schema": true,
    "breadcrumb_schema": false,
    "faq_schema": false,
    "sticky_toc": true,
    "takeaways_block": false,
    "cta_block": true,
    "shared_partials": true
  },
  {
    "slug": "how-we-use-reddit-to-build-itineraries",
    "type": "guide",
    "canonical": true,
    "meta_description": true,
    "og_image": false,
    "twitter_image": false,
    "article_schema": true,
    "breadcrumb_schema": false,
    "faq_schema": false,
    "sticky_toc": true,
    "takeaways_block": false,
    "cta_block": true,
    "shared_partials": true
  },
  {
    "slug": "is-1-dollar-ai-itinerary-worth-it",
    "type": "data-teardown",
    "canonical": true,
    "meta_description": true,
    "og_image": false,
    "twitter_image": false,
    "article_schema": true,
    "breadcrumb_schema": false,
    "faq_schema": false,
    "sticky_toc": true,
    "takeaways_block": false,
    "cta_block": true,
    "shared_partials": true
  },
  {
    "slug": "nano-banana-vs-grok",
    "type": "comparison",
    "canonical": true,
    "meta_description": true,
    "og_image": true,
    "twitter_image": false,
    "article_schema": true,
    "breadcrumb_schema": false,
    "faq_schema": true,
    "sticky_toc": true,
    "takeaways_block": true,
    "cta_block": true,
    "shared_partials": true
  },
  {
    "slug": "often-forgotten-beach-vacation-items",
    "type": "guide",
    "canonical": true,
    "meta_description": true,
    "og_image": true,
    "twitter_image": false,
    "article_schema": true,
    "breadcrumb_schema": false,
    "faq_schema": false,
    "sticky_toc": true,
    "takeaways_block": false,
    "cta_block": true,
    "shared_partials": true
  },
  {
    "slug": "slop-iterate-curate-ai-content",
    "type": "data-teardown",
    "canonical": true,
    "meta_description": true,
    "og_image": false,
    "twitter_image": false,
    "article_schema": true,
    "breadcrumb_schema": false,
    "faq_schema": false,
    "sticky_toc": false,
    "takeaways_block": false,
    "cta_block": true,
    "shared_partials": false
  },
  {
    "slug": "true-cost-of-ai-content-production",
    "type": "data-teardown",
    "canonical": true,
    "meta_description": true,
    "og_image": false,
    "twitter_image": false,
    "article_schema": true,
    "breadcrumb_schema": false,
    "faq_schema": false,
    "sticky_toc": false,
    "takeaways_block": false,
    "cta_block": true,
    "shared_partials": false
  },
  {
    "slug": "veo-3-vs-hailuo-minimax-cogvideox-video-generation",
    "type": "comparison",
    "canonical": true,
    "meta_description": true,
    "og_image": false,
    "twitter_image": false,
    "article_schema": true,
    "breadcrumb_schema": false,
    "faq_schema": true,
    "sticky_toc": true,
    "takeaways_block": true,
    "cta_block": true,
    "shared_partials": true
  },
  {
    "slug": "which-travel-planner-app-best",
    "type": "data-teardown",
    "canonical": true,
    "meta_description": true,
    "og_image": false,
    "twitter_image": false,
    "article_schema": true,
    "breadcrumb_schema": false,
    "faq_schema": false,
    "sticky_toc": true,
    "takeaways_block": false,
    "cta_block": true,
    "shared_partials": true
  },
  {
    "slug": "why-ai-travel-planners-give-generic-recommendations",
    "type": "guide",
    "canonical": true,
    "meta_description": true,
    "og_image": false,
    "twitter_image": false,
    "article_schema": true,
    "breadcrumb_schema": false,
    "faq_schema": false,
    "sticky_toc": true,
    "takeaways_block": false,
    "cta_block": true,
    "shared_partials": true
  }
]
```

