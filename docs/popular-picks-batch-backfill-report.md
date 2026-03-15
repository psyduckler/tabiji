# Popular Picks Batch Backfill Report

_Last updated: 2026-03-15_

## Command run

Backfill run across all current Popular Picks HTML pages using:

- parser with alternate layout support
- backfill-mode validation
- subtype-aware extraction

## Result

- **316 pages backfilled successfully**
- **70 pages failed during batch run**
- dominant failure mode: pages where no ranked picks could be extracted

A log was written to:

- `tmp/backfill-reports/batch-backfill.log`

## Successful backfill coverage by detected vertical

- `restaurants-food`: 158
- `lodging`: 52
- `shopping`: 50
- `mixed`: 29
- `activities`: 27

This is enough coverage to call the backfill lane operational for a large portion of the site.

## Failure pattern

The remaining failures are overwhelmingly one family of problem:

- `At least 1 pick is required`

That means the parser is **not** failing because the extracted JSON is malformed.
It is failing because these pages do not expose a recognizable ranked-pick section in the currently supported markup families.

## Interpretation

### What is now proven

The backfill system works at scale for the majority of list-style Popular Picks pages, including:

- restaurant/food guides
- lodging-style pages
- shopping pages
- many activity pages
- mixed pages that still use ranked pick sections

### What is not yet covered

The remaining failures look like a separate page family, mostly:

- country / region overview pages
- some destination landing pages
- some special activity pages that do not use section-per-pick markup

These should not block committing the successful backfill set.

## Recommended decision

### Do commit now

Commit the successfully backfilled JSON files for the parser-supported family.

Why:

- 316 successful backfills is real leverage
- the output is already validator-clean in backfill mode
- editorial warnings remain visible for later cleanup
- waiting for the overview-family outliers would unnecessarily block progress

### Do not block on these failures first

The 70 failed pages should move into a separate follow-up lane:

- inspect markup family
- decide whether they belong in the same schema
- add a separate extractor path if warranted

## Follow-up work after commit

1. commit the successful batch backfill JSON files
2. create a tracked list of the failed pages
3. inspect 2-3 failed overview pages
4. decide whether to:
   - extend Popular Picks extraction for overview-family pages, or
   - define a separate page model for them

## Bottom line

This batch backfill is worth landing.

Not because it solved everything.
Because it recovered structured source for a **large, useful majority** of the current Popular Picks inventory without manual re-research.
