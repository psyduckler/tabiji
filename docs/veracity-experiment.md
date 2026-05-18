# Veracity Slop-Cleanup Experiment

Treatment vs holdout test of whether running compare pages through
[VeracityAPI](https://veracityapi.com/docs) and addressing the high/medium-severity
findings improves GSC performance over a 28-day measurement window.

> Doc location follows the pattern from `docs/title-ctr-experiment.md` and
> `docs/compare-title-experiment.md` — `docs/` is not deployed, so it's a durable
> home for experiment artifacts that should outlive any one deploy.

---

## Round 1 — 2026-05-18

### Motivation

After PR #1559 closed the audit_compare gap (all 834 compare pages now score
100/100 on the audit's gold-standard checks: structural completeness, ai_tells
regex, etc.), we wanted to test a different quality lens — VeracityAPI's
slop / synthetic-text detector. Hypothesis: there's residual AI-texture slop
audit_compare's regex layer doesn't catch, and addressing it improves GSC
ranking/CTR signal.

### Cohort selection

- **Source:** GSC export 2026-05-18 (cached at
  `docs/data/veracity-experiment/gsc-pages-2026-05-18.csv`), the prior ~28-day
  window of impressions data.
- **Filter chain:**
  - `/compare/{slug}/` pages only
  - ≥200 impressions in the window (to give the 28-day post-test window
    measurable signal)
  - NOT in the `/compare/` title-CTR experiment cohort (PR #1498 / 364 pages)
    — two simultaneous experiments on the same page produce unreadable results
  - Local page file must exist
- **Result:** 55 candidates → top 40 by impressions kept.

### Veracity baseline (T+0)

All 40 pages scored against `POST https://api.veracityapi.com/v1/analyze` with
`{type: "text", auto_revise: false, context: {format: "article", intended_use: "publish"}, store_content: false}`.
Prose was extracted from the article body (skipping nav, footer, JSON-LD,
methodology box, photo grid, score ticker, comparison/cost tables).

Distribution across the 40-page cohort:

| Metric | Mean | Median | Range |
|---|---|---|---|
| `slop_risk` | 0.51 | 0.58 | 0.28–0.58 |
| `synthetic_risk` | 0.52 | 0.62 | 0.25–0.62 |
| `specificity_risk` | 0.51 | 0.58 | 0.28–0.58 |
| `provenance_weakness` | 0.51 | 0.58 | 0.28–0.58 |

**Action breakdown:** 37 `revise`, 3 `allow`. **Primary reason:** 39/40 pages = `generic_phrasing`.

Veracity emits coarse discrete buckets (only 6 distinct slop_risk values across
40 pages). 24 of 40 pages clustered at exactly slop=0.58. This reflects the
build pipeline producing uniform AI-texture across the compare corpus.

Per-page baselines stored at `docs/data/veracity-experiment/cohort-scores-unified.json`
and individual responses at `docs/data/veracity-experiment/scores/{slug}.json`.

### Pilot: testing the fix recipe on puerto-rico-vs-dominican-republic

Before committing to a cohort-wide treatment, we tested each fix category in
sequence on the highest-impression page in the cohort:

| Stage | slop_risk | What changed |
|---|---|---|
| Baseline | 0.55 | Original page |
| + #1 generic_phrasing (10 spans) | 0.58 | "shines", "sheer X", "excels in" stripped |
| + #2 hedging_and_absolutes | 0.58 | "While both islands share… excels in" de-templated |
| + #4 weak_provenance (9 quotes) | 0.55–0.58 (bouncing) | "a Redditor noted", "a hiker shared", etc. deleted |
| + #5 repetitive_structure (10 verdict blocks) | **0.38** | `tabiji verdict` list converted to varied prose |

**Key empirical findings:**

1. Veracity scores are discrete and non-deterministic at the precision shown.
   Identical inputs across runs produce 0.55 or 0.58 in the same bucket. Don't
   read sub-bucket movement as signal.
2. Findings #1 + #2 + #4 alone produced **no net score movement** — Veracity
   simply flagged different surface spans on the next run (cf.
   `unparalleled diversity`, `unique natural phenomena` after we removed
   `shines/sheer`). Whack-a-mole on surface phrasing doesn't work.
3. **The verdict-template restructure (#5) was the heavy lever.** Converting
   all 10 `<ul><li>Winner/Why/Who</li></ul>` blocks to varied prose dropped
   slop_risk, spec_risk, and prov_weakness from 0.55–0.58 to 0.38 — and lifted
   content_trust_score from 0.42 to 0.62. This is the kind of bucket-crossing
   that constitutes a real treatment.
4. `recommended_action` stayed `revise` even at 0.38 — to cross to `allow`
   Veracity wants real sourced data on price ranges + verified Reddit
   usernames+dates, neither of which is achievable as a per-page editorial
   pass. ~0.38 is the practical floor for editorial work within the existing
   template.

### Hypothesis

Applying the full fix recipe (#1 + #2 + #4 + #5) to a 19-page treated arm,
while leaving a matched 18-page holdout arm untouched, will produce a
detectable difference in GSC outcomes over 28 days:

- **Primary outcomes:** impressions delta + position delta (quality signals
  move ranking first, before user behavior)
- **Secondary outcomes:** CTR + clicks delta
- **Treatment sanity check:** treated pages should drop one Veracity-score
  bucket (e.g. 0.55–0.58 → ~0.38)

### Cohort assignment

37 `revise`-action pages stratified into 3 impression tiers (high ≥417,
mid 280–415, low 240–277), then snake-balanced into arms. Seed 20260518.
puerto-rico-vs-dominican-republic forced into treated (already piloted).

Full assignment at `docs/data/veracity-experiment/cohort-assignment.json`.

| Arm | Pages | Total impr | Total clicks | Mean CTR | Mean pos |
|---|---|---|---|---|---|
| Treated | 19 | 8,086 | 50 | 0.74% | 10.65 |
| Holdout | 18 | 6,961 | 45 | 0.54% | 10.84 |

(Holdout CTR mean is lower mainly because the 2.17%-CTR st-lucia-vs-martinique
page landed there. With only ~50 clicks per arm, small-N noise dominates;
the *delta* per arm vs baseline is the cleaner read at review time.)

### Treatment recipe (locked)

Each treated page receives, in order:

1. **#1 generic_phrasing** — Strip templated intensifiers: `shines`, `sheer X`,
   `excels in`, `boasts`, `unparalleled`. Replace with concrete fact or remove.
2. **#2 hedging_and_absolutes** — De-templatize `While X, Y excels in Z`
   constructions: split into declarative statements or vary structure.
3. **#4 weak_provenance** — Delete every paraphrased attribution pattern
   (`"<quote>", a/an/another <noun> <verb>` with verb ∈
   {noted, said, shared, mentioned, loved, praised, wrote, commented, ...}).
   Keep any factual claim that stands on its own; remove the quote + attribution.
4. **#5 repetitive_structure** — Convert each `<div class="tabiji-verdict">
   <strong>tabiji verdict:</strong> <ul><li>Winner...Why...Who</li></ul></div>`
   block to varied prose inside the same wrapper div. Each block uses a
   different sentence structure (Topic-first / Winner-first / Why-first / etc.)
   to avoid creating a new templated pattern.

**Out of scope (and why):**
- **#3 low_specificity** — Adding date+source to price ranges (e.g.
  `Booking.com Q1 2026 median`) would require ground-truth sourcing data
  we don't have. Faking attribution would be worse than not having it.
- **Cross-cutting build-script changes** — A persistent slop fix would
  require changes to the compare build pipeline (real Reddit usernames,
  sourced price metadata). That's a separate scope.

### Recipe application (2026-05-18)

Treatment applied to all 19 treated pages via
`scripts/veracity_apply_recipe.py --all-treated`. Aggregate edits across the
arm:

| Fix category | Total edits across 19 pages |
|---|---|
| #1 generic_phrasing replacements | 60 |
| #2 hedge_absolute substitutions | 0 (pattern too narrow) |
| #4 paraphrased-attribution deletions | 5 (only `essaouira-vs-taghazout` still had them) |
| #5 verdict-template restructures | 127 |
| Net char delta across arm | −62,074 (~−3,267 / page) |

The #2 pattern matched zero pages because the build pipeline doesn't emit the
specific "While both X share Y, Z excels in W" construction we initially saw
on puerto-rico. The #4 pattern matched only 1 page — most compare pages had
already been migrated from paraphrased "a Redditor noted" attribution to
structured `<div class="reddit-quote">` blocks with real URLs by PR #1559's
Reddit URL-backfill work. So #1 + #5 carried the recipe.

### Empirical findings from running the recipe

**Finding 1 — Veracity scoring is highly non-deterministic.** Re-scoring the
same content multiple times produced different bucket assignments:

| Page | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 |
|---|---|---|---|---|---|
| puerto-rico (post-all-fixes) | 0.38 | — | — | — | **0.58** |
| st-barts (post-recipe) | 0.58 | **0.48** | — | — | — |

Per-page variance is ±0.10–0.20, comparable to or larger than any plausible
treatment effect. **`slop_risk` is not a reliable per-page treatment metric.**
The 0.55→0.38 puerto-rico drop earlier in the pilot was largely noise.

**Finding 2 — Aggregate slop_risk did not move on the treated arm.**

| Metric | Pre-recipe (19 treated) | Post-recipe (19 treated) | Δ |
|---|---|---|---|
| Mean slop_risk | 0.526 | 0.526 | +0.000 |
| Median slop_risk | 0.580 | 0.580 | +0.000 |
| `recommended_action` distribution | 19× `revise` | 19× `revise` | (no boundary crossings) |

Possible explanations (likely all true):
- The 4-pattern prose template I cycled across verdicts ("Winner. Why. Best
  for Who.") is itself a template that Veracity learns fast — 190 instances
  across 19 pages × 10 verdicts.
- Per-run variance is large enough that a 0.05 aggregate shift wouldn't
  cleanly surface in single-pass scoring.
- Veracity may be detecting build-pipeline template uniformity that
  per-page editorial edits can't break.

**Finding 3 — The treatment is real at the content layer even though
Veracity can't see it.**

- −62K chars of content removed across the arm (~10% of body prose per page)
- 127 `<ul><li>Winner/Why/Who</li></ul>` lists replaced with prose
- 60 generic intensifiers stripped
- All paraphrased Reddit attributions removed where present

The hypothesis becomes: *Does this editorial cleanup move GSC outcomes?* —
which is now answerable independently of Veracity's verdict.

### Measurement

- **T+0 snapshot:** this document + `cohort-scores-unified.json` +
  `treated-scores-post-recipe.json`
- **T+28 review:** 2026-06-15. Pull fresh GSC export, compute per-arm deltas
  in impressions, position, CTR, clicks. Log results below as
  "Round 1 — Results".

### Reframed hypothesis

Because slop_risk turned out to be uninformative as a treatment-effect
signal, the round-1 question reframes to:

> *Did the applied editorial cleanup (verdict-template restructure +
> generic-phrasing stripping + paraphrased-attribution removal) produce a
> detectable difference in GSC outcomes vs the untouched holdout arm?*

If yes → editorial polish moves the needle on this corpus, and Veracity's
findings (despite the scoring noise) were a useful prioritization signal.
If no → either the editorial changes didn't matter, or the holdout-vs-treated
arms aren't well-matched enough to detect a real effect.

### Files

- `docs/data/veracity-experiment/gsc-pages-2026-05-18.csv` — T+0 GSC snapshot
- `docs/data/veracity-experiment/cohort.json` — 40-page candidate cohort
- `docs/data/veracity-experiment/cohort-scores-unified.json` — pre-recipe Veracity scores
- `docs/data/veracity-experiment/treated-scores-post-recipe.json` — post-recipe scores (19 treated)
- `docs/data/veracity-experiment/cohort-assignment.json` — treated/holdout arms
- `docs/data/veracity-experiment/scores/{slug}.json` — raw Veracity responses
- `docs/data/veracity-experiment/scores/{slug}.pre-recipe.json` — pre-recipe per-page responses
- `scripts/veracity_score.py` — Veracity API client + prose extractor
- `scripts/veracity_apply_recipe.py` — applies the #1/#2/#4/#5 recipe to a page
