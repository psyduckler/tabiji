# Popular Picks Parser Trial Report

_Last updated: 2026-03-15_

## Goal

Run a small multi-page trial of the HTML → JSON backfill parser before attempting larger backfill work.

## Trial sample

Tested slugs:

- `aarhus-new-nordic-restaurants`
- `amman-shawarma`
- `ardennes-hiking`
- `bangkok-rooftop-pools`
- `best-restaurants-in-kigali`
- `bukchon-hanok-stays`
- `croatia`
- `fukuoka-yatai`
- `kigali-coffee-shops`
- `mnemba-atoll-snorkeling`

## Result summary

### Passed cleanly enough for backfill (with warnings)

- `aarhus-new-nordic-restaurants` — 11 warnings
- `amman-shawarma` — 1 warning
- `bangkok-rooftop-pools` — 7 warnings
- `best-restaurants-in-kigali` — 1 warning
- `fukuoka-yatai` — 7 warnings

These pages produced structured JSON that passed validation without fatal errors.

### Failed validation

- `ardennes-hiking`
- `bukchon-hanok-stays`
- `croatia`
- `kigali-coffee-shops`
- `mnemba-atoll-snorkeling`

## What the failures mean

### Failure type 1 — pages with fewer than 3 picks / fewer than 3 FAQs
Examples:
- `ardennes-hiking`
- `bukchon-hanok-stays`
- `croatia`
- `kigali-coffee-shops`

This is not really a parser failure.
It is a schema/validator mismatch.

The current validator assumes a relatively standard Popular Picks page with:

- at least 3 picks
- at least 3 FAQs

That works for the common restaurant-style pages.
It breaks for:

- broader country / region pages
- pages that are more landing-page-like
- pages with thinner FAQ coverage
- pages using Popular Picks conventions without full list-page density

### Failure type 2 — non-food vertical price extraction
Example:
- `mnemba-atoll-snorkeling`

The parser expects a restaurant-style price pattern and currently misses some non-food / activity pricing patterns.
That means the extracted page shape is mostly right, but the validator rejects it because `priceRangeLocal` is missing.

This is a real extractor gap.

## What the trial proved

### 1. The parser works on the mainstream page shape
The parser is already useful for many mature list pages.

That is important.
It means we do **not** need to start from scratch for the 36-page backfill.

### 2. The parser is currently biased toward restaurant-style Popular Picks pages
That bias comes from both:

- extraction assumptions
- validation assumptions

### 3. “Popular Picks” is not one perfectly uniform page family
The trial exposed at least three subtypes:

1. **standard restaurant / food list pages**
2. **non-food ranked experience/activity pages**
3. **broader landing / destination pages with thinner list or FAQ structure**

That means the backfill path needs either:

- subtype-aware validation, or
- a softer “backfill mode” validator, or
- both

## My blunt diagnosis

The parser is already strong enough to start recovering data from normal pages.

The blocker for larger rollout is **not** “the parser is broken.”
The blocker is:

- the validator is too rigid for page-family variation
- price extraction needs broader patterns
- taxonomy/category detection is still too restaurant-defaulted

That is much better news than needing a brand new parser.

## Recommended next changes

### 1. Add a backfill mode to validation
Backfill mode should allow extraction output to be written even when some publish-level constraints are not met.

Suggested behavior:

- still fail on malformed JSON structure
- still fail on impossible ranks / broken URLs / missing slug/pageType
- downgrade some publish constraints to warnings during backfill, such as:
  - fewer than 3 picks
  - fewer than 3 FAQs
  - missing price range on non-food verticals

This would let us recover structured data first and triage later.

### 2. Add page subtype detection
At minimum, distinguish:

- `restaurants-food`
- `activities`
- `lodging`
- `mixed`
- `destination-overview` or similar

The parser should not assign `restaurants-food` by default to everything.

### 3. Broaden price extraction
Need to support patterns beyond restaurant spend, such as:

- day passes
- room rates
- activity price ranges
- ticket pricing
- non-currency mixed strings already present in live pages

### 4. Split “backfilled but incomplete” from “publish-ready”
That distinction matters.

Not every extracted JSON has to be immediately publish-ready to be useful.

The system should support:

- `extracted-from-html`
- `needs-editorial-review`
- `publish-ready`

## Practical next move

The smartest next step is **not** full 386-page backfill yet.

The smartest next step is:

1. add backfill-mode validation
2. improve subtype + price extraction
3. rerun a broader 20-page trial
4. then decide whether the 36-page target is low-risk enough to automate in batch

## Bottom line

The parser trial is a success.

Not because it handled every page perfectly.
Because it proved the useful part:

- we can recover structured data from many real pages already
- the remaining problems are classification and validation policy problems
- those are tractable

That is exactly where we want to be before scaling the backfill effort.
