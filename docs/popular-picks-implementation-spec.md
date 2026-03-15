# Popular Picks Implementation Spec

_Last updated: 2026-03-15_

This document turns the higher-level takeover plan into concrete implementation work.

It defines:

- the structured source schema
- the generated output contract
- renderer responsibilities
- validator rules
- file/folder layout
- first-page migration procedure

This is the spec the generator should be built against.

## Reality check from Psy's feedback

A few constraints need to stay explicit so the implementation does not become fake certainty:

- There is no existing magic template to inherit. The Popular Picks renderer has to be built for real, and the hardest part is preserving the current page behavior without copying accidental mess.
- Reddit research quality is not a solved automation problem. The system can standardize structure, but it should not pretend to automate local judgment, disagreement detection, or quote taste.
- Photo sourcing is fragile. The data model and renderer must tolerate missing images and support fallback workflows instead of assuming every place gets a clean hero photo.
- Enrichment timing is a tradeoff. Doing Places enrichment earlier improves data quality, but it shifts cost forward. The pipeline should make that choice explicit.
- Existing HTML backfill matters. We should support extraction from old pages so the 36 missing API JSONs do not require re-research.
- IndexNow / GSC submission is a downstream publishing step, not a prerequisite for proving the renderer.

## 1. Scope

This spec applies only to `/popular-picks/` pages.

It does **not** apply to:

- paid itinerary generation
- `/compare/`
- `/alerts/`
- `/itineraries/`
- other page types

## 2. System model

A Popular Picks page has three layers:

1. **Source data** — structured content owned by humans + enrichment scripts
2. **Generated artifact** — final `index.html`
3. **Derived indexes/metadata** — listing metadata, API-supporting data, sitemap/index updates if needed

The key rule is simple:

**HTML is compiled output. Source data is the source of truth.**

## 3. Proposed file layout

```text
popular-picks-data/
  shinjuku-cheap-restaurants.json
  accra-jollof-rice.json

generators/popular-picks/
  schema.md
  render-page.js
  render-meta.js
  render-schema.js
  validate-source.js
  validate-output.js
  update-indexes.js
  utils.js

popular-picks/
  {slug}/index.html
```

Optional later:

```text
popular-picks-build/
  reports/
  diffs/
  validation/
```

## 4. Source schema

Use JSON first.

Why:

- strict enough to validate
- easy for scripts to consume
- no ambiguity from YAML formatting edge cases
- acceptable for hand editing at this stage

If editing pain becomes real, we can revisit YAML later. Not now.

## 5. Canonical source object

Each page file should contain one object with this top-level shape:

```json
{
  "slug": "shinjuku-cheap-restaurants",
  "pageType": "popular-picks",
  "status": "published",
  "taxonomy": {},
  "seo": {},
  "hero": {},
  "intro": {},
  "summary": {},
  "map": {},
  "picks": [],
  "faq": [],
  "related": {},
  "provenance": {},
  "verification": {},
  "publishing": {}
}
```

## 6. Top-level field spec

### 6.1 Required fields

These fields are required on every page:

- `slug`
- `pageType`
- `status`
- `taxonomy`
- `seo`
- `hero`
- `intro`
- `summary`
- `picks`
- `faq`
- `related`
- `verification`
- `publishing`

### 6.2 Field definitions

#### `slug`
- type: string
- required: yes
- rule: lowercase kebab-case
- rule: must match output path `popular-picks/{slug}/index.html`

#### `pageType`
- type: string
- required: yes
- value: `popular-picks`

#### `status`
- type: string
- required: yes
- allowed values:
  - `draft`
  - `reviewed`
  - `published`
  - `archived`

#### `taxonomy`
- type: object
- required: yes
- fields:
  - `city` string, required
  - `region` string, optional
  - `country` string, required
  - `countryCode` string, optional
  - `neighborhood` string, optional
  - `category` string, required
  - `subcategory` string, optional
  - `vertical` string, required
  - `badgeEmoji` string, required

Recommended `vertical` values:
- `restaurants-food`
- `bars-nightlife`
- `cafes-desserts`
- `street-food`
- `markets`
- `nature-outdoors`
- `activities`
- `shopping`
- `lodging`
- `mixed`

#### `seo`
- type: object
- required: yes
- fields:
  - `title` string, required
  - `h1` string, required
  - `metaTitle` string, required
  - `metaDescription` string, required
  - `canonicalPath` string, required
  - `ogTitle` string, optional
  - `ogDescription` string, optional
  - `twitterTitle` string, optional
  - `twitterDescription` string, optional
  - `heroImage` string, optional
  - `publishedTime` string ISO datetime, required
  - `modifiedTime` string ISO datetime, required
  - `robots` string, default `index, follow, max-image-preview:large`

Rules:
- `canonicalPath` must equal `/popular-picks/{slug}/`
- `metaTitle` target length: 40-70 chars
- `metaDescription` target length: 120-170 chars
- if OG/Twitter title/description omitted, renderer derives them from meta fields

#### `hero`
- type: object
- required: yes
- fields:
  - `eyebrow` string, required
  - `title` string, optional if same as `seo.h1`
  - `dek` string, required
  - `badge` string, required
  - `metaSpans` array of strings, required

#### `intro`
- type: object
- required: yes
- fields:
  - `answerFirst` string, required
  - `body` array of strings, required, min 1
  - `methodology` string, optional

Rules:
- `answerFirst` must be a self-contained summary statement
- it must mention at least the page subject plus one factual qualifier like price, ranking basis, location, or scope

#### `summary`
- type: object
- required: yes
- fields:
  - `totalOptions` integer, required
  - `priceRangeLocal` string, optional
  - `priceRangeUSD` string, optional
  - `bestBudgetOption` string, optional
  - `bestLuxuryOption` string, optional
  - `bestOverall` string, optional
  - `topPick` string, required
  - `sourcesAnalyzed` string, required
  - `lastVerifiedLabel` string, optional

Rules:
- `totalOptions` must equal `picks.length`
- `topPick` should match pick rank 1 unless explicitly overridden

#### `map`
- type: object
- required: no for v1, recommended
- fields:
  - `enabled` boolean
  - `title` string
  - `embedUrl` string
  - `ctaLabel` string
  - `ctaUrl` string

#### `picks`
- type: array of objects
- required: yes
- min length: 3

Each pick object:

```json
{
  "rank": 1,
  "name": "Fuunji",
  "placeType": "restaurant",
  "neighborhood": "Shinjuku",
  "address": "...",
  "priceRangeSymbol": "$",
  "priceRangeLocal": "¥800-¥1,200",
  "priceRangeUSD": "$5-$8",
  "googleRating": 4.4,
  "reviewCount": 1842,
  "googleMapsUrl": "https://...",
  "website": "https://...",
  "phone": "+81 ...",
  "photo": "/popular-picks/shinjuku-cheap-restaurants/fuunji.jpg",
  "cuisineTags": ["tsukemen", "ramen"],
  "whyItMadeTheList": "...",
  "whatToOrder": "...",
  "insiderTip": "...",
  "redditQuotes": [
    {
      "quote": "...",
      "source": "Reddit",
      "url": "https://..."
    }
  ],
  "hoursNote": "...",
  "editorialFlags": {
    "cashOnly": false,
    "longLines": true,
    "closedOn": ["Sunday"]
  }
}
```

Required pick fields:
- `rank`
- `name`
- `placeType`
- `priceRangeLocal` or `priceRangeUSD`
- `whyItMadeTheList`
- `whatToOrder`
- `insiderTip`

Recommended fields:
- `googleRating`
- `reviewCount`
- `googleMapsUrl`
- `photo`
- `cuisineTags`
- `redditQuotes`

Rules:
- `rank` must be unique and contiguous starting at 1
- `name` must be unique within the page unless a duplicate is explicitly justified
- `whyItMadeTheList` must start with a self-contained answer-first sentence
- if `googleRating` is present, it must be between 0 and 5
- if `reviewCount` is present, it must be a non-negative integer
- if `googleMapsUrl` is present, it must be a valid URL
- each pick should have at least one meaningful descriptive paragraph across `whyItMadeTheList`, `whatToOrder`, and `insiderTip`

#### `faq`
- type: array of objects
- required: yes
- min length: 3

Each FAQ object:
- `question` string, required
- `answer` string, required

Rules:
- no empty answers
- no duplicate questions
- answers should be plain text or clean HTML-safe text only

#### `related`
- type: object
- required: yes
- fields:
  - `manual` array of slugs
  - `topics` array of strings
  - `minimumCount` integer, optional

#### `provenance`
- type: object
- required: no in v1, recommended
- fields:
  - `researchSources` array
  - `notes` string
  - `importedFromHtml` boolean

#### `verification`
- type: object
- required: yes
- fields:
  - `lastVerified` string `YYYY-MM`, required
  - `pipelineVersion` string, required
  - `contentVersion` string, optional
  - `reviewedByHuman` boolean, optional

#### `publishing`
- type: object
- required: yes
- fields:
  - `outputPath` string, required
  - `includeInMetadataIndex` boolean, default true
  - `includeInSitemap` boolean, default true
  - `includeInApiBuild` boolean, default true

Rule:
- `outputPath` must equal `popular-picks/{slug}/index.html`

## 7. Generated HTML contract

The renderer must produce a complete standalone HTML document.

### 7.1 Head requirements

Required output in `<head>`:

- charset
- viewport
- favicon links consistent with existing site
- title tag
- meta description
- canonical
- OG tags
- Twitter tags
- robots
- article published/modified times
- structured data script blocks
- existing analytics tag if that remains standard on this page type
- inline style block or approved page-style inclusion strategy

### 7.2 Body requirements

Required body sections, in order:

1. nav
2. hero
3. intro section
4. picks list section
5. map section if enabled
6. FAQ section
7. related links section
8. footer
9. page scripts

The exact wrapper class names may change, but section order should be standardized.

### 7.3 Hero contract

Hero should render:
- eyebrow
- H1
- supporting dek
- badge/meta row

### 7.4 Intro contract

The intro section must begin with the answer-first block.

Suggested structure:

```html
<section class="intro-section">
  <p><strong>...</strong></p>
  <p>...</p>
  <p>...</p>
</section>
```

### 7.5 Pick card contract

Each pick card should render at minimum:

- rank
- name
- price cue
- rating/review summary if available
- address/location cue if available
- maps link if available
- photo if available
- why-it-made-the-list block
- what-to-order block
- insider tip block
- Reddit quotes block if available

The first sentence of the main editorial block must remain answer-first and citable.

### 7.6 FAQ contract

FAQ must render both visible HTML and FAQ schema data from the same source array.

### 7.7 Related links contract

Related links should render from either:

- manually declared slugs, or
- post-process generated related links,

but the final page should not omit the section if site standard requires it.

## 8. Metadata + schema contract

Split metadata/schema generation into dedicated functions.

### 8.1 Minimum schema output

Each page should generate:

- `Article`
- `ItemList`
- `FAQPage` when FAQ exists
- `TouristTrip` block for current AEO compatibility

### 8.2 `ItemList` rules

- `numberOfItems` must equal `picks.length`
- each `ListItem.position` must match `pick.rank`
- each item name must match the visible page content

### 8.3 `TouristTrip` rules

Until the AEO strategy changes, preserve the current support fields through `additionalProperty`, including:

- `totalOptions`
- `priceRangeUSD` if available
- `bestBudgetOption` if available
- `bestLuxuryOption` if available
- `bestOverall` if available
- `topPick`
- `sourcesAnalyzed`
- `lastVerified`

### 8.4 Derivation rules

Prefer generating metadata from source fields rather than repeating text manually.

Examples:
- `ItemList.numberOfItems` from `picks.length`
- `topPick` from rank 1
- `lastVerified` from `verification.lastVerified`
- canonical URL from `seo.canonicalPath`

## 9. Renderer responsibilities

## 9.1 `render-page.js`
Owns:
- full HTML document assembly
- body section markup
- section ordering
- injection of metadata and schema blocks
- inclusion of nav/footer shell for this page type

Does not own:
- source validation logic
- output validation logic
- mutation of index files

## 9.2 `render-meta.js`
Owns:
- title
- meta description
- canonical
- OG/Twitter tags
- article dates
- robots

## 9.3 `render-schema.js`
Owns:
- `Article`
- `ItemList`
- `FAQPage`
- `TouristTrip`

## 9.4 `update-indexes.js`
Owns:
- `popular-picks/picks-metadata.json` update behavior
- any derived listing metadata needed by `/popular-picks/index.html`
- optional sitemap touchpoints if adopted

## 10. Index update contract

At minimum, the generator must be able to produce or update the metadata entry used by `popular-picks/picks-metadata.json`.

For each page, index payload should include at least:

```json
{
  "slug": "shinjuku-cheap-restaurants",
  "title": "20 Best Cheap Restaurants in Shinjuku 2026",
  "description": "The best budget restaurants in Shinjuku, Tokyo...",
  "heroImage": "/popular-picks/shinjuku-cheap-restaurants/akiyoshi.jpg",
  "badge": "🍜 Shinjuku",
  "metaSpans": ["<span>🍜 20 spots</span>", "<span>🗺️ Interactive Map</span>"],
  "city": "Tokyo",
  "category": "budget eats"
}
```

The exact description copy may differ, but the shape must stay compatible with current consumers.

## 11. Validator rules

There should be two validators.

## 11.1 Source validator

Fail on:

- missing required top-level fields
- invalid slug format
- `pageType !== popular-picks`
- `outputPath` mismatch
- `summary.totalOptions !== picks.length`
- pick ranks not contiguous
- duplicate pick ranks
- duplicate FAQ questions
- fewer than 3 picks
- fewer than 3 FAQs
- empty answer-first intro
- empty pick narrative fields
- invalid URLs where required
- impossible rating values
- invalid `lastVerified` format

Warn on:

- missing Google rating
- missing review count
- missing photo
- missing Reddit quotes
- missing map section
- unusually short meta description
- unusually long title

## 11.2 Output validator

Fail on:

- missing `<title>`
- missing meta description
- missing canonical
- missing required schema blocks
- missing hero H1
- missing intro section
- missing picks section
- visible pick count not matching source count
- FAQ HTML count not matching FAQ schema count
- broken section ordering

Warn on:

- duplicate meta fields
- unusually large HTML size
- likely missing related links content
- empty image src
- suspicious schema/content mismatch

## 12. Rendering determinism rules

To make diffs usable:

- sort object-derived output consistently
- preserve stable script block order
- preserve stable section order
- avoid injecting timestamps except where explicitly required
- do not include random IDs

If the source has not changed, the generator should not churn the page.

## 13. First-page migration spec

Recommended first page:
- `shinjuku-cheap-restaurants`

Fallback:
- `accra-jollof-rice`

### Why `shinjuku-cheap-restaurants`

It is a good test case because it appears to include:

- mature SEO metadata
- multiple schema blocks
- substantial pick volume
- FAQ content
- visible AEO-style structure
- a realistic level of complexity for proving the system

That makes it a strong stress test, not a toy example.

## 14. First-page migration checklist

### Step 1 — Freeze the reference page
Capture the current page as the baseline artifact.

Required notes:
- slug
- current title
- current meta description
- current schema block types
- pick count
- FAQ count
- page-specific quirks worth preserving

### Step 2 — Create source JSON
Manually extract the page into `popular-picks-data/shinjuku-cheap-restaurants.json`.

Do not try to fully automate extraction on day one.
Manual extraction is fine for the first proving pass.

### Step 3 — Implement minimal renderer
Support only enough features to fully regenerate the first page.
Do not overgeneralize before the first successful round-trip.

### Step 4 — Generate HTML
Write generated output to a temporary path first, for example:

```text
tmp/popular-picks/shinjuku-cheap-restaurants/index.html
```

Compare against the live source page.

### Step 5 — Validate equivalence
Check:
- same visible section set
- same pick count
- same FAQ count
- same canonical URL
- same or better metadata quality
- same or better schema coverage
- no obvious quality regression in prose

### Step 6 — Integrate index update
Ensure the page can also produce a compatible metadata entry for `picks-metadata.json`.

### Step 7 — Swap output path
Once confidence is high, write generated output to:

```text
popular-picks/shinjuku-cheap-restaurants/index.html
```

### Step 8 — Re-run downstream steps if needed
If the current operational path still expects them, confirm compatibility with:

1. `functions/enrich-popular-picks.py`
2. `scripts/aeo-upgrade-popular-picks.py`
3. `functions/add-related-links.js`

If any of those become redundant, document that explicitly before removing them from the pipeline.

## 15. Definition of acceptable parity

The first generated page does not need to be byte-for-byte identical.
It does need to meet this threshold:

- equal or better information quality
- equal or better metadata quality
- equal or better schema coverage
- no layout breakage
- no SEO regression
- no AEO regression
- no omitted picks or FAQs

That is the real bar.

## 16. Suggested implementation sequence

1. create source JSON schema examples
2. build source validator
3. build metadata/schema renderer
4. build body renderer
5. build output validator
6. build index updater
7. convert `shinjuku-cheap-restaurants`
8. document deltas and pain points
9. refine schema once, not five times midstream
10. convert second page only after first page proves the pattern

## 17. Hard guardrails

- do not change page URLs
- do not touch paid itinerary fulfillment
- do not introduce a framework for this alone
- do not batch-migrate pages before the first example is proven
- do not let the generated page depend on manual cleanup as part of “normal” operation

## 18. Recommended next build tasks

The immediate next coding tasks should be:

1. create `popular-picks-data/` and add one hand-authored test JSON
2. implement `validate-source.js`
3. implement `render-meta.js`
4. implement `render-schema.js`
5. implement `render-page.js`
6. implement `update-indexes.js`
7. generate and inspect the first page

That is enough to move from planning into real execution.
