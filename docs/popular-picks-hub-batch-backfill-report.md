# Popular Picks Hub Batch Backfill Report

_Last updated: 2026-03-15_

## Result

Ran hub extractor batch backfill across detected hub/index-style Popular Picks pages.

### Outcome

- **50 hub pages detected**
- **50 hub pages extracted successfully**
- **0 failures**

This confirms the hub/index family is stable enough for bulk recovery into structured source data.

## Detection rule used

Pages were treated as hub candidates when the HTML contained both:

- `.city-section`
- `.pick-card`

That matched the outlier family discovered during leaf-page backfill triage.

## Output location

Recovered JSON files were written to:

- `popular-picks-hub-data/`

A machine-readable run report was written to:

- `tmp/hub-backfill/batch-report.json`

## What this means

The Popular Picks estate now cleanly splits into two recovered source-model families:

1. **Leaf pages**
   - `popular-picks-data/`
   - rich ranked guides

2. **Hub/index pages**
   - `popular-picks-hub-data/`
   - grouped directory pages linking to leaf guides

## Recommendation

Land the hub batch backfill as a separate commit from the leaf batch.

That preserves the architectural distinction and makes future renderer/extractor work much easier to reason about.
