# Popular Picks Remediation Plan — 2026-03-29

## What I found

The audit issues are not random. They cluster into a small number of repeatable page families:

### Family A — healthy structured-render pages
- Signature: `viator + related + speakable + map CTA + rating`, no generic map embed
- Count: 253
- Samples: `jaipur-rooftop-cafes`, `uluwatu-surf-camps`, `rome-pizza`
- Source path: `generators/popular-picks/render-page.js`

### Family B — structured-render pages with bad image pipeline
- Signature: same as Family A, but still uses `hero-bg.jpg`
- Count before remediation: 272
- Samples: `kadikoy-street-food`, `fukuoka-ramen`, `sydney-brunch`
- Root cause: broken per-venue image fallback / OG image selection
- Fix path: `scripts/fix-venue-photos-batch.py`

### Family C — newer broken batch-template family
- Signature: has `viator + related + rating`, but missing `speakable` and per-place `map CTA`; still uses generic `maps/embed/v1/search`; many also use `hero-bg.jpg`
- Count before remediation: 242
- Samples: `tokyo-brunch`, `bordeaux-natural-wine-bars`, `belize-city-street-food`
- Root cause: legacy Gemini batch generator output (`scripts/gen_popular_picks_batch.py`) diverged from the structured renderer

### Family D — semi-upgraded pages
- Signature: has `speakable`, still missing per-place `map CTA`; still uses generic map embed; mixed image state
- Count before remediation: 135 (87 + 48 in the audit family split)
- Samples: `montreal-craft-beer`, `vancouver-craft-beer`, `tokyo-sushi`
- Root cause: partial SEO/schema upgrades without full map/data parity

### Family E — outlier / country-shell / malformed pages
- Signature: missing `viator` and `related`, often odd slugs or country-level pages mixed into `popular-picks`
- Count before remediation: 62
- Samples: `usa`, `kenya`, `botswana`, `nusa-dua-beach-clubs`, `slug`, `test`
- Root cause: mixed page types and malformed legacy content living in the same directory

## Priority order

### P0 — stop shipping worse pages
1. Stop using the legacy batch template as the default generator.
2. Patch reusable remediation scripts so they work against the real repo root, not `~/tabiji`.
3. Keep the structured renderer as the canonical target state.

### P1 — remediate the highest-volume visible breakage
1. Fix `hero-bg.jpg` image usage in page body and social cards.
2. Backfill missing `viator` and `related` sections.
3. Backfill missing `speakable` schema.

### P2 — restore navigation / utility parity
1. Backfill per-place Google Maps CTA data.
2. Replace generic `maps/embed/v1/search` experiences with per-pick map data where possible.
3. Backfill visible Google rating blocks on pages still missing them.

### P3 — clean content quality defects
1. Fix awkward possessive / malformed H1 patterns.
2. Remove malformed test/outlier pages from the production build path or migrate them to a separate shell.
3. Normalize malformed source JSON/API files that block automated upgrades.

## Work completed on this branch

### 1) Script reliability fixes
- `scripts/add_pp_sections.py`
  - fixed hardcoded repo path so it works in the actual checkout
- `scripts/upgrade-popular-picks-schema-richness.py`
  - now skips malformed API JSON instead of crashing the whole batch

### 2) Batch remediation already applied
- Added missing `methodology`, `viator`, and `related` sections to 68 pages
- Added / refreshed richer schema and `speakable` on 783 pages
- Fixed venue-photo / OG-image `hero-bg.jpg` usage on 321 pages

## Current post-remediation counts

These are the remaining rough counts after the automated passes above:

- Missing Viator: 2
- Missing related links: 2
- Missing speakable: 2
- Missing per-place map CTA data: 553
- Missing visible Google rating markup: 153
- Still using generic `maps/embed/v1/search`: 475
- Still using `hero-bg.jpg` as OG image: 48
- Still using `hero-bg.jpg` in body images: 404
- Awkward H1s still needing cleanup: 210

## Immediate next pass recommended

1. **Map/rating backfill pass**
   - use `functions/enrich-popular-picks.py` on the remaining legacy restaurant-section pages
   - target missing `data-map-cta-url`, missing rating blocks, and generic map embeds together

2. **Image pass #2**
   - patch remaining `hero-bg.jpg` cases that are not in the simple batch-family shape
   - likely requires a second fixer for nonstandard section markup

3. **H1 cleanup pass**
   - generate a deterministic rewrite list from the 210 awkward titles
   - fix obvious possessive/template bugs first, then hand-review edge cases

4. **Outlier family decision**
   - decide whether country/test/malformed pages belong in `popular-picks` at all
   - if not, remove them from the build/audit set or move them to a separate shell

## Known blockers

- `api/v1/picks/*.json` contains at least 4 malformed JSON files, which prevents fully clean automated upgrades until they are fixed
- map/rating backfill at full scale will require a controlled SerpAPI enrichment pass and should be done in batches

## Recommendation

Ship this branch as **phase 1 remediation** now:
- fixes the highest-volume obvious defects
- documents the exact template families
- leaves the heavier map/rating/H1 cleanup as phase 2, with the path now clear
