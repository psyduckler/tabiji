# Shinjuku Generator Parity Decision

_Last updated: 2026-03-15_

## Question

Is the current generated version of `shinjuku-cheap-restaurants` good enough to treat the Popular Picks generator as **proven for a real page**?

## Short answer

**Yes — for proof-of-system, not for final broad rollout.**

That distinction matters.

The generator is now good enough to say:

- a real, non-trivial Popular Picks page can be represented in structured source data
- the renderer can reproduce the core page contract
- schema/meta output survives the transition
- hours, contact links, map placement, FAQ, verdicts, and related links all render in a site-native way
- parity work is now in the realm of refinement, not invention

It is **not** yet good enough to say:

- all Popular Picks pages can be migrated safely without page-specific review
- the renderer has reached final visual parity for every legacy quirk
- the map system is done forever
- source normalization rules are fully settled

## What is now true

### 1. The page is genuinely source-driven
`popular-picks-data/shinjuku-cheap-restaurants.json` is not toy data anymore. It is rich enough to drive:

- hero
- intro
- methodology
- 20 picks
- contact info
- hours
- FAQs
- related links
- schema/meta
- map treatment

That is the main threshold that mattered.

### 2. The renderer now matches the live page contract closely enough
The renderer now emits live-style semantics, including:

- `restaurant-section`
- `restaurant-header`
- `restaurant-number`
- `cuisine-tag`
- `google-rating`
- `restaurant-details`
- `shop-contact`
- `tabiji-verdict`
- live-style hours summaries (`Open now` / `Closed now`)

This is no longer a generic card renderer pretending to be parity.

### 3. The important parity checks are passing
The generated Shinjuku page now has:

- 20 rendered picks
- 6 FAQs matching the live parity target
- working map panels for desktop + mobile placement
- matching per-section contact rows in markup
- matching per-section verdict blocks in markup
- output validation passing

### 4. Remaining issues are refinement issues
What remains is mostly:

- visual polish
- exact legacy micro-copy parity
- map fidelity decisions
- broader source normalization policy
- proving generalization on a second page

Those are real, but they are not blockers to calling the first page conversion **successful enough to continue**.

## Why this is good enough

Because the hard question was never:

> “Can we produce HTML from JSON?”

That part was always trivial.

The real question was:

> “Can a structured source + renderer reproduce a serious Popular Picks page without collapsing into generic slop or losing the site’s operational pattern?”

At this point, the answer is **yes**.

Not perfect yes.
Not final yes.
But real yes.

## What this decision does NOT mean

Calling this “good enough” does **not** mean:

- switch every Popular Picks page immediately
- stop reviewing source quality
- assume the renderer is now universal
- treat visual parity as complete

It means:

- the architecture is validated
- the generator lane is real
- the next work should focus on controlled iteration, not existential doubt

## Recommended next move after approval

### Immediate next step
Open a focused PR with:

- Shinjuku parity improvements
- source normalization updates
- renderer contract improvements
- decision note that this is the first successful proof page

### Then
Do one of these two, in order of preference:

1. convert a second, simpler page to prove the renderer generalizes
2. strengthen extraction/backfill tooling for the 36 missing JSONs

My bias:
- do **one second page** first
- then do backfill tooling

That gives us confidence that the renderer is not secretly overfit to Shinjuku.

## Final recommendation

**Submit this as PR-worthy work.**

The right framing is:

- first end-to-end parity proof for Popular Picks generator system
- not final renderer completion
- not mass migration ready yet

That is honest and strong.
