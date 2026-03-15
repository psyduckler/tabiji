# Popular Picks Standardization + Takeover Plan

_Last updated: 2026-03-15_

## Why this exists

The current `/popular-picks/` system works, but it is too manual and too inconsistent to scale safely.

Right now, page quality depends too much on whoever made the page, how carefully they followed prior examples, and how many post-processing steps got remembered. That creates drift in:

- layout and section order
- metadata and schema quality
- intro quality and AEO formatting
- internal linking
- enrichment completeness
- long-term maintainability

The goal is to turn Popular Picks from an artisanal page-making process into a controlled publishing system.

## Core decision

We should **not** preserve the current workflow as a human checklist.

We should:

1. extract the recurring logic
2. define one canonical page standard
3. store page content as structured data
4. generate HTML + metadata from that data
5. validate outputs before publishing
6. migrate old pages into the standard over time

In blunt terms: **the standard should own the page, not the operator.**

## Desired end state

A Popular Picks page should become a compiled artifact, not a hand-edited source file.

That means each page is generated from a structured source record containing:

- page-level metadata
- intro/summary content
- pick list and ordering
- per-pick facts
- FAQ content
- SEO/AEO fields
- related links inputs
- verification metadata

The generator should then produce:

- canonical HTML page
- title / meta description / OG fields
- JSON-LD / schema block
- optional API-facing normalized JSON
- index updates / listing updates if needed

## Non-goals

This project does **not** require:

- refactoring paid itinerary generation
- changing live URLs
- changing the enrichment pipeline contract unless needed
- redesigning all page types at once
- introducing a heavy framework

This is a **Popular Picks systemization project**, not a repo rewrite.

## Principles

### 1. Structured source > handwritten HTML
If content matters, it should exist in data first.

### 2. One canonical template
There should be one primary Popular Picks renderer, not many near-duplicates.

### 3. Deterministic output
The same input should generate the same page every time.

### 4. Post-processing should become explicit pipeline stages
Enrichment, AEO, related links, validation, and index updates should be named steps, not tribal memory.

### 5. Migration must be incremental
We do not need a risky big-bang rewrite.

### 6. Preserve URL stability
Existing slugs and page paths stay put.

## Current problem areas

### Content drift
Pages vary in structure, section naming, tone, and completeness.

### Metadata drift
Schema, answer-first formatting, and meta fields are not consistently guaranteed at creation time.

### Manual dependency risk
The current process depends on remembering that after page creation we also need enrichment, AEO upgrade, and related links.

### Hard-to-audit quality
There is no single validator that can say whether a page is structurally complete and publishable.

### Hard-to-batch update
If we want to change one recurring pattern, we currently have to touch many pages individually.

## Proposed architecture

## 1. Canonical page data model
Create a single structured schema for Popular Picks pages.

Suggested shape:

```json
{
  "slug": "shinjuku-cheap-restaurants",
  "pageType": "popular-picks",
  "category": "restaurants",
  "city": "Tokyo",
  "neighborhood": "Shinjuku",
  "country": "Japan",
  "title": "Best Cheap Restaurants in Shinjuku",
  "h1": "Best Cheap Restaurants in Shinjuku",
  "metaTitle": "Best Cheap Restaurants in Shinjuku (Local Favorites + Budget Picks)",
  "metaDescription": "The best cheap restaurants in Shinjuku, from ramen counters to tonkatsu spots, with prices, ratings, maps links, and what to order.",
  "hero": {
    "eyebrow": "Tokyo Popular Picks",
    "title": "Best Cheap Restaurants in Shinjuku",
    "dek": "Budget-friendly places actually worth your time."
  },
  "intro": {
    "answerFirst": "The best cheap restaurants in Shinjuku typically cost about $6-$18 per person, with top value concentrated around ramen, curry, soba, and casual set-meal spots near Shinjuku Station.",
    "body": [
      "This guide focuses on reliable low-cost meals, not just the absolute cheapest calories.",
      "The emphasis is on places travelers can realistically use without excessive planning."
    ]
  },
  "summary": {
    "totalOptions": 12,
    "priceRangeUSD": "$6-$18",
    "bestBudgetOption": "...",
    "bestOverall": "...",
    "topPick": "...",
    "sourcesAnalyzed": "Reddit threads, traveler discussions, Google Maps signals"
  },
  "picks": [
    {
      "rank": 1,
      "name": "Place Name",
      "slug": "place-name",
      "priceRange": "$",
      "priceRangeUSD": "$8-$12",
      "googleRating": 4.4,
      "reviewCount": 1842,
      "address": "...",
      "neighborhood": "Shinjuku",
      "googleMapsUrl": "...",
      "website": "...",
      "phone": "...",
      "openingHours": [],
      "photo": "https://img.tabiji.ai/popular-picks/...jpg",
      "whyItMadeTheList": "...",
      "whatToOrder": "...",
      "insiderTip": "...",
      "tags": ["ramen", "late-night", "solo-friendly"],
      "redditQuotes": []
    }
  ],
  "faq": [
    {
      "question": "What area of Shinjuku is best for cheap food?",
      "answer": "..."
    }
  ],
  "related": {
    "manual": [],
    "topics": ["tokyo-ramen", "tokyo-budget-food"]
  },
  "verification": {
    "lastVerified": "2026-03",
    "pipelineVersion": "v1"
  }
}
```

This does not need to be the exact final schema, but it should be close in spirit:

- explicit
- normalized
- generator-friendly
- validator-friendly

## 2. Renderer layer
Build a renderer that converts the structured source into final HTML.

The renderer should own:

- page shell
- section ordering
- repeated card markup
- FAQ markup
- nav/footer inclusion strategy used by Popular Picks pages
- consistent class names and HTML structure

The renderer should also produce:

- `<title>`
- meta description
- canonical URL
- OG/Twitter meta
- JSON-LD

This removes the need to handcraft every page body.

## 3. Schema/meta renderer
Separate content rendering from metadata rendering.

Why:

- easier testing
- easier upgrades to AEO/SEO output
- easier bulk regeneration if schema requirements change

Outputs should include at minimum:

- `TouristTrip` or successor schema block used by current AEO logic
- FAQ schema when relevant
- consistent `lastVerified`
- summary facts derived from structured data, not retyped manually

## 4. Index updater
Any page generation flow should optionally update whatever listing/index data Popular Picks depends on.

If there are multiple downstream surfaces, make them explicit:

- `/popular-picks/index.html`
- `popular-picks/picks-metadata.json`
- API build inputs
- sitemap if applicable

The key rule: **page publish should not rely on someone remembering side effects.**

## 5. Validator
Create a validator that checks both source data and generated output.

Validation should catch things like:

- missing required page fields
- duplicate ranks
- missing pick names or descriptions
- malformed URLs
- impossible price ranges
- empty FAQ answers
- missing answer-first intro
- missing schema block
- broken section ordering
- missing related links block if required

The validator should be able to fail fast before publish.

## Publishing pipeline target

The eventual Popular Picks pipeline should look like this:

1. create or update structured page data
2. validate source data
3. render HTML
4. render schema/meta
5. write page output
6. run enrichment step where needed
7. run related links step where needed
8. validate final output
9. update indexes / metadata files
10. commit and publish

That is much safer than: “make HTML, then remember three more things.”

## Phased rollout

## Phase 1 — Define the standard
Deliverables:

- canonical data schema
- canonical page contract
- required sections and metadata list
- validation rules
- migration constraints

Exit criteria:

- we can describe exactly what a compliant Popular Picks page is
- ambiguity is removed from the workflow

## Phase 2 — Build the generator foundation
Deliverables:

- page data schema implementation
- HTML renderer
- schema/meta renderer
- index updater
- validator

Exit criteria:

- one structured source file can generate one valid page
- generator output is stable and repeatable

## Phase 3 — Convert one page end-to-end
Recommended first test page:

- `shinjuku-cheap-restaurants`
- or `accra-jollof-rice` if preserving current mental continuity matters more

Deliverables:

- source data file for the page
- generated HTML that reproduces the live page quality
- successful enrichment/AEO/related-link compatibility
- documented diff between old handcrafted version and generated version

Exit criteria:

- one real page fully round-trips through the system
- output quality is equal or better
- no manual drift remains for that page

## Phase 4 — Batch migration + new production
Deliverables:

- migration workflow for old pages
- batched conversion process
- rules for all net-new pages to use structured generation only

Recommended order:

1. convert the easiest, most formulaic pages first
2. handle weird outliers later
3. freeze creation of new handcrafted pages once generator confidence is high

Exit criteria:

- new pages use the generator by default
- legacy pages are migrated in controlled batches
- standards are enforced, not aspirational

## Migration strategy

### Track A — Forward production
All new Popular Picks pages should move to the structured system as soon as the first test page is proven.

### Track B — Legacy conversion
Old pages should be migrated in batches, likely grouped by:

- same city cluster
- same category type
- same existing template pattern
- same quality tier / cleanup complexity

### Rule for migration
Do not hand-polish every old page forever.

If a page is worth maintaining, move it into the standard.
If it is not worth maintaining, leave it alone until there is a reason.

## Guardrails

### Do not break URL permanence
Generated output must continue writing to the existing page path.

### Do not entangle this with paid itinerary fulfillment
Keep Popular Picks work isolated from the revenue-critical order pipeline.

### Do not overfit to today’s markup quirks
Some existing HTML oddities are accidental. The new standard should preserve what matters, not every historical wart.

### Keep the source editable by humans
Structured does not mean unreadable. Use a format that is easy to inspect and patch.

## Implementation notes

Reasonable implementation options:

- JSON files for strictness
- YAML if hand-editability matters more
- JS/TS objects if the renderer will live in Node and benefit from shared utilities

My bias: use whatever is easiest to validate and regenerate consistently. Fancy is unnecessary.

A simple folder pattern would be enough:

```text
popular-picks-data/
  shinjuku-cheap-restaurants.json
  accra-jollof-rice.json

generators/popular-picks/
  render-page.js
  render-meta.js
  validate.js
  update-indexes.js
```

The exact paths can change. The important part is separation of concerns.

## Definition of done

This project is done when:

- a Popular Picks page can be rebuilt from structured source alone
- the output includes all required HTML, meta, and schema elements
- validation catches incomplete pages before publish
- new pages stop depending on artisanal assembly
- migration becomes a repeatable process instead of bespoke cleanup

## Ownership stance

Psy’s existing workflow is valuable as operational knowledge.
But it should be treated as reference material for extracting the system — not as the system itself.

That is the takeover:

- human judgment stays where it matters
- repetitive assembly moves into code
- standards become enforceable
- Sno can operate the lane reliably

## Recommended next artifact

The next concrete step should be a build spec that turns this plan into implementation work.

That spec should define:

1. final field-by-field schema
2. output HTML contract
3. renderer responsibilities
4. validator rules
5. first test page selection
6. migration checklist

If we do that well, the rest becomes execution.
