# API Milestone 2 — dataset/version infrastructure

This milestone adds the minimum sync/import contract needed for offline clients.

## Objective

Make the API syncable and importable without forcing clients to infer freshness from ad hoc file mtimes.

## New endpoints

- `GET /api/v1/manifest.json`
- `GET /api/v1/countries/{iso2}/manifest.json`

## Deliverables

- global manifest endpoint contract
- country manifest endpoint contract
- dataset versioning rules
- schema versioning rules
- file metadata contract
  - `path`
  - `contentType`
  - `sizeBytes`
  - `sha256`
  - `updatedAt`
- sample generated manifests
- compatibility policy

## Versioning rules

### `apiVersion`
Public API surface version.

### `schemaVersion`
Contract version for manifest/entity shapes.

Rules:
- increment **major** for breaking schema changes
- increment **minor** for additive schema changes

### `datasetVersion`
Generated payload version for sync/import.

Rules:
- update whenever generated JSON/checksums change
- clients use this to detect stale local data
- manifests expose the current dataset version without needing to redownload payloads

## Compatibility policy

- breaking manifest/schema changes require a new `schemaVersion` major
- additive fields may ship under the same major version
- file checksum changes always produce a new `datasetVersion`
- offline clients should trust `datasetVersion` + `sha256`, not only timestamps
- `staleAfter` = `generatedAt` + 7 days (configurable via `STALE_TTL_DAYS`); clients should re-fetch when past this date

## Low-CPU implementation note

To avoid blowing up local generation cost, Milestone 2 uses a separate lightweight manifest builder:

- `api/build-manifests.py`

That script scans already-generated API outputs and writes:

- `api/v1/manifest.json`
- `api/v1/countries/{iso2}/manifest.json`

This keeps manifest/version work decoupled from the heavy full API rebuild path.
