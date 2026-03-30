# API Milestone 1 — normalized entity layer

This milestone introduces a stable internal/app-facing contract without breaking the public website-oriented endpoints.

## What changed

- added a shared entity envelope across destinations, picks, itineraries, and comparisons
- added stable canonical IDs everywhere (`destination:*`, `pick:*`, `itinerary:*`, `comparison:*`)
- added `entityType` and `schemaVersion` to record payloads
- kept `type` as a deprecated compatibility alias for older consumers; new integrations should use `entityType`
- added `freshness` and `provenance` metadata to major record summaries/details
- promoted `/api/v1/catalog.json` into a generated normalized catalog instead of a stale checked-in artifact
- added JSON Schema files for the entity envelope and catalog contract

## Milestone 1 scope

Applied to:

- destinations
- picks
- itineraries
- comparisons
- place records inside picks, exposed through the generated catalog

## Design intent

The current public endpoints remain useful projections for the website.

The new normalized layer makes it possible to build:

- SQLite importers
- sync/version manifests later
- country/entity packs later
- stable app-side caching
- retrieval/AI flows grounded in durable IDs instead of page shapes

## New canonical fields

### Common envelope

- `id`
- `type`
- `entityType`
- `schemaVersion`
- `updatedAt`
- `sourceUrl`
- `tags`
- `freshness`
- `provenance`

### Catalog contract

`/api/v1/catalog.json` now acts as the normalized entity index for:

- destination
- pick
- place
- itinerary
- compare

## Notes

This is intentionally not the final offline app contract.

It is the first stabilization step so later milestones can add:

- manifests
- dataset versions
- country packs
- delta sync
- operational utility entity families
