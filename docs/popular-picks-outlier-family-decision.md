# Popular Picks Outlier Family Decision

_Last updated: 2026-03-15_

## Representative outlier inspected

- `popular-picks/italy/index.html`

## What it is

This page is **not** a standard ranked pick page.

It is a **hub/index-style page** with:

- multiple `city-section` blocks
- linked `pick-card` children
- each card pointing to a deeper Popular Picks leaf page
- no per-pick verdict blocks
- no section-per-ranked-item structure like:
  - `restaurant-section`
  - `pick-section`
  - `stay-section`

In other words: it is a curated directory page, not a normal compiled leaf page.

## Why the parser failed

The current backfill parser expects leaf-page structures where each item is a content-rich section.

`italy` instead contains:

- city sections
- link cards
- summary snippets
- internal navigation / scrollspy

That means the current validation error:

- `At least 1 pick is required`

is actually a useful signal.

The parser is correct to say:
- “this page is not the same thing as the leaf pages we know how to backfill.”

## Decision

These outlier pages should **not** be forced into the same source schema right now.

They should be treated as a **separate page family**.

Suggested label:

- `popular-picks-hub`
- or `popular-picks-index`

## Why separate them

Because their source model is fundamentally different.

A leaf page model is about:

- ranked picks
- rich per-pick editorial blocks
- quotes, verdicts, hours, maps, contact info

A hub/index page model is about:

- grouped destinations or neighborhoods
- internal navigation sections
- cards linking to child leaf pages
- lightweight summaries, not deep pick records

Trying to jam those into the same schema would make both models worse.

## Recommended source shape for hub pages

Something closer to:

```json
{
  "slug": "italy",
  "pageType": "popular-picks-hub",
  "status": "published",
  "seo": {},
  "hero": {},
  "intro": {},
  "sections": [
    {
      "id": "rome",
      "title": "Rome",
      "cards": [
        {
          "slug": "rome-cacio-e-pepe",
          "title": "15 Best Cacio e Pepe in Rome",
          "description": "...",
          "badge": "📍 Rome",
          "meta": ["🍽️ 15 spots", "🗺️ Interactive Map"],
          "image": "..."
        }
      ]
    }
  ],
  "publishing": {}
}
```

That would preserve the actual product structure instead of faking ranked picks where none exist.

## What this means operationally

### For the current backfill batch
Do nothing more.

These hub/index pages should stay outside the current leaf-page backfill lane.

### For the next parser phase
Create a separate extractor for hub/index pages.

Target markup patterns include:

- `.city-section`
- `.pick-card`
- `.card-badge`
- `.card-meta`
- mobile/desktop TOC structures

## Recommendation

Treat the remaining outlier failures as **schema-family mismatches**, not parser defects.

That means:

1. keep the current leaf-page backfill system as-is
2. create a new hub/index schema + extractor for country/region directory pages
3. do not let hub pages contaminate the leaf-page model

## Bottom line

The outlier family is real.

It should be handled intentionally as a separate page type.
That is cleaner than stretching the leaf-page schema until it becomes incoherent.
