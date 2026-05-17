# GSC snapshots

Durable archive of Google Search Console Pages exports used for baseline + post-experiment measurement. Files in `docs/` aren't deployed (Cloudflare Pages 20K-file cap concerns), so this is a safe persistent home.

## Naming convention

`{section}-pages-{YYYY-MM-DD}.csv`

- `{section}` — `compare`, `scams`, `travel guides`, or `all` depending on what GSC filter was applied at export time.
- `{YYYY-MM-DD}` — date the CSV was exported, not the date range it covers.

GSC Pages exports default to the last 28 days at the rolled-up Page level. Snapshots are taken at experiment milestones (rollout, mid-test, decision). Always confirm the actual date range from the exporting user — the filename is an export-date stamp, not a coverage window.

## Files

| File | Notes |
|---|---|
| `compare-pages-2026-05-09.csv` | Compare-section filter; T+0 baseline for /compare/ title-CTR experiment (PR #1498). 1,000 rows. |

## Why this matters

Earlier in the experiment-tracking work the source CSV at `~/Desktop/tabiji.ai-Performance-on-Search-{date}/` was overwritten between sessions, which forced cohort balancing for /compare/ round 1 to fall back on `inventory.json` `popularityScore` instead of real GSC impressions. Saving snapshots here prevents that loss for future cohort balancing and post-test deltas.

## Add a new snapshot

```bash
mkdir -p docs/data/gsc-snapshots
cp ~/Desktop/tabiji.ai-Performance-on-Search-{YYYY-MM-DD}/Pages.csv \
   docs/data/gsc-snapshots/{section}-pages-{YYYY-MM-DD}.csv
```

Add a row to the table above and commit on whatever branch you're working on.
