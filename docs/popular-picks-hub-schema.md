# Popular Picks Hub Schema

_Last updated: 2026-03-15_

This schema is for country/region/index-style Popular Picks pages that group child leaf pages.

It is intentionally separate from the leaf-page schema.

## Core idea

A hub page is a directory of grouped links, not a ranked leaf-page guide.

Examples:

- `italy`
- `spain`
- `ethiopia`

## Top-level shape

```json
{
  "slug": "italy",
  "pageType": "popular-picks-hub",
  "status": "published",
  "taxonomy": {
    "scope": "country-or-region-hub",
    "label": "Italy"
  },
  "seo": {},
  "hero": {},
  "toc": [],
  "sections": [],
  "faq": [],
  "provenance": {},
  "publishing": {}
}
```

## Section shape

```json
{
  "id": "rome",
  "title": "Rome",
  "cards": [
    {
      "slug": "rome-cacio-e-pepe",
      "href": "/popular-picks/rome-cacio-e-pepe/",
      "title": "15 Best Cacio e Pepe in Rome",
      "description": "The best cacio e pepe restaurants in Rome...",
      "badge": "📍 Rome",
      "meta": ["🍽️ 15 spots", "🗺️ Interactive Map"],
      "image": "https://img.tabiji.ai/popular-picks/rome-cacio-e-pepe/felice-a-testaccio.jpg",
      "imageAlt": "15 Best Cacio e Pepe in Rome"
    }
  ]
}
```

## Notes

- `sections` correspond to `.city-section`
- `cards` correspond to linked `.pick-card` elements
- `toc` captures in-page navigation structure for desktop/mobile sidebars
- FAQ may exist and can still be extracted from JSON-LD
- no ranked-pick assumptions belong here

## Why separate from leaf schema

Leaf pages contain rich per-pick editorial records.
Hub pages contain grouped child-page references.

Trying to collapse those into one model would make both worse.
