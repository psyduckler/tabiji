# Popular Picks Hub Trial Report

_Last updated: 2026-03-15_

## Goal

Test whether the outlier family of country/region pages can be handled by a dedicated hub/index extractor and schema.

## Trial set

- `italy`
- `spain`
- `ethiopia`
- `japan`
- `taiwan`
- `thailand`
- `turkey`
- `usa`
- `united-kingdom`
- `france`

## Result

All 10 trial pages extracted successfully as:

- `pageType: popular-picks-hub`

## Summary counts

- `italy` — sections: 5, toc: 4
- `spain` — sections: 5, toc: 5
- `ethiopia` — sections: 2, toc: 2
- `japan` — sections: 20, toc: 20
- `taiwan` — sections: 2, toc: 2
- `thailand` — sections: 12, toc: 12
- `turkey` — sections: 1, toc: 1
- `usa` — sections: 4, toc: 4
- `united-kingdom` — sections: 3, toc: 2
- `france` — sections: 3, toc: 3

## Decision

The hub family is real and coherent.

These pages should be treated as a separate page type from the leaf Popular Picks guides.

## What the hub extractor successfully captures

- hero title + intro/dek
- TOC/navigation structure
- grouped sections (city/region groupings)
- linked cards inside each section
- card title / description / badge / meta / image
- FAQ when present in JSON-LD

## Important observation

These pages are not malformed leaf pages.
They are functioning index/hub pages with a stable pattern.

That means the architecture split is justified:

- leaf-page extractor/schema
- hub-page extractor/schema

## Recommendation

Proceed with a controlled hub backfill batch next.

These pages no longer need to block the main Popular Picks migration system.
