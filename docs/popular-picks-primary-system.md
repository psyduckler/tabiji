# Popular Picks Generation — Primary System Policy

_Last updated: 2026-03-15_

## Status

**Popular Picks generation is now the primary system.**

That means:

- structured source is the source of truth
- generated HTML is the artifact
- handcrafted page HTML is legacy, not default

## Two supported families

### 1. Leaf pages
Use:
- `popular-picks-data/{slug}.json`

These are ranked pages with rich item-level editorial content.

### 2. Hub pages
Use:
- `popular-picks-hub-data/{slug}.json`

These are grouped index/directory pages linking to leaf pages.

## Default rule for new work

For any new Popular Picks work:

- do **not** start by hand-authoring `popular-picks/{slug}/index.html`
- start from structured source
- build/generated output should be reviewed, then written to the page path

Handcrafted HTML should only be used as a temporary exception, not the normal workflow.

## Maintenance rule for old pages

If an existing page already has structured source:
- edit the structured source first
- regenerate the HTML

If an existing page does not yet have structured source:
- backfill it first when practical before major edits

## Operational commands

The system now has a standard operator surface.

Examples:

```bash
# Build a leaf page
node generators/popular-picks/build.js <repo-root> popular-picks-data/shinjuku-cheap-restaurants.json popular-picks/shinjuku-cheap-restaurants/index.html

# Build a hub page
node generators/popular-picks/build-hub.js <repo-root> popular-picks-hub-data/italy.json popular-picks/italy/index.html

# Validate a leaf page
node generators/popular-picks/validate-source.js popular-picks-data/shinjuku-cheap-restaurants.json

# Validate a hub page
node generators/popular-picks/validate-hub.js popular-picks-hub-data/italy.json
```

## Lessons from merge review

Psy's merge edits clarified the quality bar.

Treat these as standing rules:

- do **not** generate synthetic lead-in prose for `whatToOrder`
- on non-food pages, suppress filler recommendation text instead of inventing restaurant-style copy
- do **not** emit null/empty date meta tags on hub pages
- prefer omission over obviously templated fluff

## What “done” means now

The project is no longer in proof mode.

The remaining work is rollout and maintenance:

- cut over more pages in small batches
- improve renderer polish where it matters
- keep source models clean
- avoid reintroducing artisanal HTML as the default workflow
