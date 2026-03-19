# Popular Picks SerpAPI Enrichment Rules

This locks the first production rules for low-cost place enrichment using SerpAPI-backed Google search only.

## Goal

Use SerpAPI as the default enrichment layer for place-level operational metadata before spending on Places/Maps APIs.

Principles:
- prefer cheap, broad-coverage search evidence first
- publish only high-confidence or medium-confidence fields
- attach provenance on every enriched pick
- leave uncertain fields blank instead of inventing precision

## Allowed vocab

### `mealType`

Allowed values:
- `breakfast`
- `brunch`
- `lunch`
- `dinner`
- `late-night`
- `drinks`
- `snack`
- `snack / lunch`
- `lunch / dinner`
- `dinner / late-night`
- `dinner / late-night / drinks`
- `sunset drinks`
- `sunset drinks / dinner / late-night`
- `sunset drinks / late-night`

Rule:
- keep this operational, not editorial
- describe when the place is actually useful, not every possible service window

### `dietaryTags`

Allowed values:
- `vegetarian-friendly`
- `vegetarian-options`
- `vegan-options`
- `gluten-free-options`
- `gluten-free-fries`
- `halal`

Rule:
- only publish when explicit on official/menu pages or repeated in strong third-party snippets
- do not infer from cuisine alone

### `paymentHints`

Allowed values:
- `cash-only`
- `cards-accepted`
- `credit-cards-accepted`
- `digital-payments`
- `cash`
- `pin`
- `credit-card`

Rule:
- use only explicit evidence
- if sources conflict, either keep multiple concrete tags when they truly coexist or leave blank

### `touristyLevel`

Allowed values:
- `mostly-local`
- `mixed`
- `mixed-leaning-touristy`
- `touristy`
- `tourist-magnet`

Rule:
- keep this coarse
- never imply fake measurement precision

### `provenance.confidence`

Allowed values:
- `low`
- `medium`
- `medium-high`
- `high`

### `provenance.sourceTypes`

Current allowed source types:
- `google-serp-kg`
- `official-site`
- `booking-page`
- `menu-page`
- `faq-page`
- `brand-page`
- `reservation-snippet`
- `dress-code-page`
- `dress-code-snippet`
- `tripadvisor-snippet`
- `happycow-snippet`
- `instagram-snippet`
- `facebook-snippet`
- `travel-blog-snippet`
- `promo-snippet`
- `promo-page`
- `delivery-snippet`
- `thefork-snippet`
- `opentable-snippet`
- `quandoo-snippet`
- `kimpton-page`
- `skywalk-page`
- `attraction-page`
- `venue-guide-snippet`
- `yelp-snippet`
- `google-places`
- `legacy-html`
- `reddit`

## Confidence thresholds

### Publish at `high`

Allowed when:
- official/booking source is explicit, or
- 2+ strong sources agree with no contradiction

Typical fields:
- `reservationNeeded`
- `paymentHints`
- `mealType`

### Publish at `medium-high`

Allowed when:
- one strong source is explicit, plus one supporting source, or
- Google KG + official site strongly imply the same answer

Typical fields:
- `bestTimeToGo`
- `knownForTags`
- `dietaryTags`
- `waitExpectation`

### Publish at `medium`

Allowed when:
- evidence is useful but partly indirect
- no strong contradiction exists

Typical fields:
- `touristyLevel`
- `waitExpectation`
- nightlife timing recommendations

### Do not publish at `low`

Use `low` in provenance only when:
- the search path found weak signals
- the field is being preserved as a draft candidate
- the field should not ship into user-facing logic yet

## Source-priority rules

Field-by-field source priority:

### `reservationNeeded`
1. `booking-page`
2. `official-site`
3. `faq-page`
4. `reservation-snippet`
5. `google-serp-kg`
6. `tripadvisor-snippet`
7. `yelp-snippet`

### `bestTimeToGo`
1. `google-serp-kg`
2. `official-site`
3. `promo-snippet`
4. `instagram-snippet`
5. `tripadvisor-snippet`
6. `reddit`

### `waitExpectation`
1. `google-serp-kg`
2. `reservation-snippet`
3. `tripadvisor-snippet`
4. `yelp-snippet`
5. `reddit`

### `mealType`
1. `google-serp-kg`
2. `menu-page`
3. `official-site`
4. `tripadvisor-snippet`

### `dietaryTags`
1. `official-site`
2. `menu-page`
3. `happycow-snippet`
4. `tripadvisor-snippet`
5. `google-serp-kg`

### `paymentHints`
1. `official-site`
2. `faq-page`
3. `tripadvisor-snippet`
4. `yelp-snippet`

### `touristyLevel`
1. `google-serp-kg`
2. `tripadvisor-snippet`
3. `reddit`
4. `travel-blog-snippet`

### `knownForTags`
1. `official-site`
2. `menu-page`
3. `google-serp-kg`
4. `tripadvisor-snippet`
5. `reddit`

## Automation rules

Automation should:
- query SerpAPI first
- summarize evidence into a normalized candidate object
- only write fields that meet vocab and confidence rules
- always write `provenance`
- never overwrite stronger human-reviewed fields with weaker inferred values

## Current recommendation

Production pipeline order:
1. structured source JSON exists
2. SerpAPI enrichment pass proposes operational fields
3. validator enforces locked vocab
4. renderer shows only accepted fields
5. later expensive APIs are optional upgrades, not prerequisites
