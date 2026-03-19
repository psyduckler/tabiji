# Data Enrichment Roadmap — Phase 1 shipped shape

This PR establishes the first agent-facing enrichment layer in the generated API.

## What it adds

### 1. Cross-linking across core entities

Generated relationship fields now connect:

- destinations -> picks / itineraries / comparisons
- picks -> destination / related itineraries / related comparisons
- itineraries -> destination / related picks / related comparisons
- comparisons -> destination slugs / related picks / related itineraries

This turns the API into a basic travel graph instead of isolated records.

### 2. Normalized destination attributes

Destination detail and list records now include a `normalized` object with:

- `budgetBand`
- `tripPace`
- `familyFriendliness`
- `nightlifeScore`
- `walkabilityScore`
- `transitScore`
- `safetyScore`
- `hassleLevel`
- `bestForTags`
- `recommendedTripLengthsDays`

Current values are heuristic/backfilled from existing destination metadata. They are meant to be immediately useful and easy to improve later.

### 3. Picks operational metadata

Each place inside a picks guide now includes an `operational` object with:

- `category`
- `mealTypes`
- `priceTier`
- `reservationNeeded`
- `idealTimeToGo`
- `knownFor`
- `waitTimeLevel`
- `dietaryTags`
- `paymentTypes`
- `touristyLevel`

### 4. Itinerary operational fields

Itinerary detail and list records now include:

- `durationDays`
- `pace`
- `estimatedDailyBudget`
- `familySuitability`
- `averageDayIntensityScore`
- per-day `dayIntensityScore`
- placeholder structures for `transitSegments`, `rainyDayAlternatives`, `reservationRequirements`, and `openingHoursVerified`

## Intent

This is deliberately the lowest-regret first cut:

- graph linkage first
- structured fields over prose-only richness
- backfillable heuristics now, richer source-backed values later
- no CMS migration required to start benefiting agents immediately

## Next recommended follow-ups

1. replace heuristic destination scores with source-backed editorial values
2. add seasonality fields (`bestMonths`, `crowdByMonth`, `costByMonth`)
3. add structured comparison winners beyond current partial extraction
4. add provenance fields (`lastVerifiedAt`, `sourceTypes`, `sourceCount`, `confidenceScore`)
5. add geo normalization (`coordinates`, `timezone`, `countryCode`, `region`)
