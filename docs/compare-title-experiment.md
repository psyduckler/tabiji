# /compare/ Title CTR Experiment

History of CTR-driven title-tag experiments on `/compare/{X}-vs-{Y}/` pages. Each round's setup, baseline, results, and follow-up plan recorded below in chronological order.

> Doc location follows the same pattern as `docs/title-ctr-experiment.md` (the /scams/ experiment) — `docs/` is not deployed, so it's a durable home for experiment artifacts that should outlive deploys.

---

## Round 1 — 2026-05-09

### Motivation

The /compare/ section is the biggest CTR opportunity on the site. Aggregate stats from the 2026-05-08 GSC export (post tier-1 restoration):

| Section | Pages | Imps | CTR | Avg Pos |
|---|---|---|---|---|
| /scams/ | 137 | 14,245 | **2.47%** | 7.18 |
| /compare/ | ~835 | ~96,028 | **0.44%** | 10.38 |
| Sitewide | ~1000 | ~235,000 | 0.83% | — |

Compare runs ~5.6× worse CTR than scams while ranking at similar positions, indicating title/snippet (not ranking) is the binding constraint.

### Pre-test pattern analysis (2026-05-08 GSC export, live pages only)

The biggest pattern surfaced before this experiment:

| Pair type | Pages | Imps | CTR | Note |
|---|---|---|---|---|
| niche-vs-niche | 470 | — | **0.67%** | Already winning — Tabiji is often the only quality content for these pairs |
| big-vs-niche | 266 | — | 0.45% | Mid-tier |
| big-vs-big | 98 | — | **0.21%** | Losing 3× harder than niche at the same position — competing with TripAdvisor/Reddit/Lonely Planet on famous queries |

Position is *not* the issue (most pages cluster at pos 5–10). The CTR delta is title/snippet/intent.

### Hypothesis

Different title framings will lift CTR on big-vs-big and big-vs-niche pages where the current generic template (`{X} vs {Y}: Which Should You Visit? (2026 Comparison)`) loses to authority-site brand recognition. The /scams/ round 1 test (2026-04-17) showed that a title matching natural query phrasing — "Is X Safe for Tourists?" — lifted CTR +1.93pp; the same logic should apply here.

### Cohort selection

**Included:** big-vs-niche + big-vs-big pages = **364 pages**. These are the pages with measurable CTR upside; current titles are clearly failing here.

**Excluded:** 470 niche-vs-niche pages. They're already winning at 0.67% CTR — risk of breaking what works exceeds the upside of changing it.

### Cohort assignment

364 pages stratified-snake balanced across 11 arms by `popularityScore` (from `compare/inventory.json` — used by the hub builder for ranking; serves as proxy for organic demand in the absence of a per-page GSC dump). 11-page-block deterministic-shuffle pattern produced these per-arm balances:

| Arm | Pages | AvgScore | TotInboundLinks | Big-vs-Big share |
|---|---:|---:|---:|---:|
| Control | 33 | 111.9 | 146 | 8 |
| A | 33 | 112.2 | 96 | 10 |
| B | 33 | 112.7 | 99 | 8 |
| C | 33 | 115.5 | 122 | 6 |
| D | 33 | 112.4 | 103 | 11 |
| E | 33 | 112.5 | 132 | 9 |
| F | 33 | 113.2 | 120 | 9 |
| G | 33 | 116.4 | 119 | 7 |
| H | 34 | 109.4 | 125 | 11 |
| I | 33 | 114.2 | 118 | 8 |
| J | 33 | 113.3 | 129 | 11 |

Average popularity score is within ~6% across arms (109–116). Big-vs-big share is 6–11 per arm.

### Per-arm GSC baseline (T+0, from 2026-05-09 export)

The 2026-05-09 GSC export was pulled the same day round 1 deployed, so it represents pre-treatment baseline for these pages (28-day window of data with the *old* titles). Snapshot stored at [docs/data/gsc-snapshots/compare-pages-2026-05-09.csv](data/gsc-snapshots/compare-pages-2026-05-09.csv).

| Arm | Pages | WithGSC | Imps | Clicks | CTR | WeightedPos |
|---|---:|---:|---:|---:|---:|---:|
| Control | 33 | 19 | 3,982 | 4 | **0.10%** | 11.64 |
| A | 33 | 17 | 1,680 | 11 | **0.65%** | 12.64 |
| B | 33 | 18 | 2,367 | 7 | 0.30% | 13.12 |
| C | 33 | 16 | 2,063 | 11 | 0.53% | 10.77 |
| D | 33 | 18 | 2,584 | 4 | 0.15% | 11.57 |
| E | 33 | 24 | 3,044 | 11 | 0.36% | 10.39 |
| F | 33 | 20 | 2,515 | 6 | 0.24% | 11.65 |
| G | 33 | 21 | 1,680 | 3 | 0.18% | 8.94 |
| H | 34 | 19 | 1,631 | 2 | 0.12% | 14.96 |
| I | 33 | 18 | 6,376 | 7 | 0.11% | 12.45 |
| J | 33 | 22 | 3,476 | 12 | 0.35% | 10.48 |
| **Total cohort** | **364** | **212** | **31,398** | **78** | **0.25%** | — |

Two findings worth flagging at T+0:

1. **The cohort baseline CTR is 0.25%**, lower than the section-wide 0.44% reported in the pre-test analysis. This is consistent with the hypothesis: big-vs-niche + big-vs-big pages are the *underperforming subset*. Niche-vs-niche pages (excluded from this cohort) carry the section average up.

2. **Per-arm baseline CTR varies 0.10%–0.65%** — wider than the popularityScore-based balance suggested. With ~17–24 GSC-data pages per arm and only 78 clicks total in the cohort, single high- or zero-CTR pages dominate arm averages. The *delta* (post-treatment – baseline) per arm is the cleaner read at review time, not absolute post-treatment CTR. Arm A's 0.65% baseline already runs above the 0.44% section average — beating that bar takes a real lift, not a regression to the mean.

### Position imbalance worth tracking

Weighted-position spread is 8.94 (G) to 14.96 (H) — a 6-position gap. If a variant arm shifts >0.5 weighted positions during the test that's a confound; flag any arm whose post position drifts meaningfully.

### Variant title patterns

All variants set `<title>`, `<meta property="og:title">`, and `<meta name="twitter:title">` in sync. Meta description, H1, body, URL unchanged.

#### Control — Current default
**Pattern:** `{X} vs {Y}: Which Should You Visit? (2026 Comparison) | tabiji.ai`
**Hypothesis:** baseline. Tests how the existing template performs against alternatives.
**Example:** `Spain vs Italy: Which Should You Visit? (2026 Comparison) | tabiji.ai`

#### A — Sharpen current
**Pattern:** `{X} vs {Y}: Honest 2026 Comparison | tabiji.ai`
**Hypothesis:** Drop "Which Should You Visit?" (which every listicle says) for "Honest" — a credibility signal that signals editorial stance. Tightens by ~15 chars.
**Example:** `Ireland vs England: Honest 2026 Comparison | tabiji.ai`

#### B — Question-match ("Is X Better Than Y?")
**Pattern:** `Is {X} Better Than {Y} in 2026? Honest Comparison | tabiji.ai`
**Hypothesis:** Direct mirror of the /scams/ V3 winner ("Is X Safe for Tourists?"). Searchers literally type "is bali better than hawaii" — current title ignores this query. Yes/no question is psychologically stronger.
**Example:** `Is Japan Better Than Italy in 2026? Honest Comparison | tabiji.ai`

#### C — Concrete tradeoff hook
**Pattern:** `{X} vs {Y}: Cost, Safety & Vibe Compared (2026) | tabiji.ai`
**Hypothesis:** Promise specific dimensions in the title. Travelers comparing want budget + crowds + culture answers. Concreteness wins; also captures axis-specific queries.
**Example:** `Japan vs South Korea: Cost, Safety & Vibe Compared (2026) | tabiji.ai`

#### D — Reddit / community authority
**Pattern:** `{X} vs {Y}: What Reddit Travelers Picked (2026) | tabiji.ai`
**Hypothesis:** Lean into the actual content moat. Meta descriptions already reference Reddit-backed data — title should foreground it. "Reddit" is also a search modifier ("X vs Y reddit" is a real query).
**Example:** `Italy vs Portugal: What Reddit Travelers Picked (2026) | tabiji.ai`

#### E — "Should I Visit X or Y?"
**Pattern:** `Should I Visit {X} or {Y}? (2026 Decision Guide) | tabiji.ai`
**Hypothesis:** Captures a different natural query phrasing ("should I go to X or Y") than B. First-person verb feels personal vs the impersonal "vs".
**Example:** `Should I Visit Greece or Italy? (2026 Decision Guide) | tabiji.ai`

#### F — Best-for / traveler-type segmentation
**Pattern:** `{X} vs {Y}: Best for Couples, Solo, or Family? (2026) | tabiji.ai`
**Hypothesis:** Same destination pair, different answers per traveler type. Captures multiple long-tail queries ("X vs Y for couples", "X vs Y solo travel").
**Example:** `Lisbon vs Barcelona: Best for Couples, Solo, or Family? (2026) | tabiji.ai`

#### G — Pros, Cons & Verdict
**Pattern:** `{X} vs {Y}: Pros, Cons & 2026 Verdict | tabiji.ai`
**Hypothesis:** Promise a definitive editorial verdict, structured deliverable.
**Example:** `Costa Rica vs Mexico: Pros, Cons & 2026 Verdict | tabiji.ai`

#### H — Year-prominent showdown
**Pattern:** `2026 Showdown: {X} vs {Y} (Real Costs, Honest Take) | tabiji.ai`
**Hypothesis:** Lead with the year + a dramatic word. Tests whether stronger emotional framing on a comparison-shopping query lifts clicks. Risk: edge of clickbait.
**Example:** `2026 Showdown: Brazil vs Argentina (Real Costs, Honest Take) | tabiji.ai`

#### I — Numbered-differences listicle
**Pattern:** `{X} vs {Y}: 7 Differences That Decide Your Trip (2026) | tabiji.ai`
**Hypothesis:** Concrete number + listicle format is a proven CTR winner (BuzzFeed effect). Captures "differences between X and Y" queries.
**Example:** `Greece vs Spain: 7 Differences That Decide Your Trip (2026) | tabiji.ai`

#### J — Trip-duration / planning frame
**Pattern:** `{X} vs {Y}: Where to Spend a Week in 2026 | tabiji.ai`
**Hypothesis:** Reframes from abstract "which is better" to a concrete planning decision (which destination gets my week of vacation?). Captures upstream planning intent.
**Example:** `Colombia vs Mexico: Where to Spend a Week in 2026 | tabiji.ai`

### Hypothesis families

| Family | Variants |
|---|---|
| Baseline | Control |
| Sharpen current | A |
| Question-match (natural query) | B, E |
| Concrete tradeoff/data | C, I |
| Authority signal | D |
| Segmentation / planning frame | F, J |
| Editorial stance / dramatic | G, H |

### Title length

23% (85/364) of titles run >60 chars pre-brand-suffix — mostly long compound destination names (Cinque Terre, San Francisco, Costa Rica, etc.). Truncation is consistent across arms, so it does not bias the comparison.

### What's held constant (so title can be attributed as the sole variable)

- Meta description
- H1 on page
- Body content
- URL
- Internal links
- Page structure
- inventory.json card data (used by hubs)

### Cohort assignments

#### Control (33 pages)
argentina-vs-croatia, bali-vs-new-caledonia, bali-vs-thailand, bangkok-vs-chiang-mai, barcelona-vs-granada, berlin-vs-munich, berlin-vs-prague, cayman-islands-vs-bahamas, croatia-vs-czech-republic, cuba-vs-jamaica, cuba-vs-puerto-rico, dubai-vs-doha, england-vs-senegal, france-vs-slovenia, georgia-vs-spain, germany-vs-poland, honduras-vs-mexico, hungary-vs-ireland, ireland-vs-senegal, japan-vs-australia, japan-vs-china, kyoto-vs-nara, london-vs-amsterdam, netherlands-vs-portugal, new-york-vs-london, portugal-vs-uruguay, prague-vs-budapest, rome-vs-barcelona, san-diego-vs-los-angeles, san-francisco-vs-seattle, spain-vs-italy, vietnam-vs-philippines, washington-dc-vs-new-york

#### A (33 pages) — Sharpen
bolivia-vs-brazil, brazil-vs-portugal, brazil-vs-scotland, brazil-vs-south-korea, canada-vs-sweden, colorado-vs-san-francisco, denmark-vs-sweden, egypt-vs-greece, england-vs-finland, england-vs-jamaica, england-vs-switzerland, france-vs-germany, germany-vs-austria, ghana-vs-japan, greece-vs-israel, greece-vs-lithuania, india-vs-ireland, ireland-vs-england, jamaica-vs-trinidad-and-tobago, japan-vs-mexico, japan-vs-taiwan, lombok-vs-bali, mexico-vs-morocco, mexico-vs-turkey, norway-vs-iceland, osaka-vs-kyoto, paris-vs-new-york, spain-vs-switzerland, spain-vs-turkey, sweden-vs-usa, taipei-vs-hong-kong, taiwan-vs-thailand, thailand-vs-singapore

#### B (33 pages) — Is X Better Than Y?
andaman-islands-vs-maldives, argentina-vs-france, argentina-vs-portugal, bali-vs-fiji, belgium-vs-france, belgium-vs-portugal, bermuda-vs-bahamas, bermuda-vs-jamaica, brazil-vs-ecuador, brazil-vs-germany, england-vs-india, england-vs-italy, england-vs-panama, france-vs-guatemala, ghana-vs-portugal, greece-vs-ireland, greece-vs-slovakia, hong-kong-vs-south-korea, iceland-vs-ireland, india-vs-maldives, japan-vs-colombia, japan-vs-india, japan-vs-italy, kuala-lumpur-vs-singapore, maldives-vs-mauritius, mexico-vs-portugal, mexico-vs-spain, phoenix-vs-las-vegas, scotland-vs-ireland, seoul-vs-busan, slovenia-vs-sweden, south-korea-vs-mexico, vietnam-vs-indonesia

#### C (33 pages) — Cost, Safety & Vibe
azerbaijan-vs-france, boston-vs-new-york, brazil-vs-morocco, denmark-vs-germany, england-vs-portugal, england-vs-scotland, england-vs-serbia, finland-vs-greece, france-vs-morocco, georgia-vs-greece, guatemala-vs-jamaica, hong-kong-vs-sri-lanka, jakarta-vs-bali, jamaica-vs-barbados, japan-vs-germany, japan-vs-indonesia, japan-vs-south-korea, japan-vs-vietnam, mexico-vs-south-africa, miami-vs-vancouver, milan-vs-barcelona, norway-vs-sweden, rome-vs-florence, scotland-vs-united-states, spain-vs-usa, sri-lanka-vs-thailand, st-barts-vs-maldives, stuttgart-vs-munich, taiwan-vs-vietnam, tampa-vs-miami, tokyo-vs-seoul, toronto-vs-new-york, turks-and-caicos-vs-bahamas

#### D (33 pages) — Reddit Travelers Picked
azerbaijan-vs-iceland, bali-vs-koh-samui, bora-bora-vs-maldives, brazil-vs-uruguay, brussels-vs-amsterdam, bulgaria-vs-greece, canada-vs-mexico, chicago-vs-new-england, costa-rica-vs-germany, croatia-vs-turkey, england-vs-germany, england-vs-ghana, finland-vs-germany, france-vs-portugal, france-vs-senegal, germany-vs-spain, greece-vs-croatia, hawaii-vs-samoa, italy-vs-portugal, italy-vs-usa, jamaica-vs-bahamas, jamaica-vs-mexico, jamaica-vs-panama, luxembourg-vs-sweden, maldives-vs-tahiti, mexico-vs-panama, mexico-vs-switzerland, nagoya-vs-osaka, naples-vs-rome, san-francisco-vs-los-angeles, spain-vs-sweden, tokyo-vs-london, vietnam-vs-thailand

#### E (33 pages) — Should I Visit?
albania-vs-england, argentina-vs-spain, bangkok-vs-kuala-lumpur, bangkok-vs-singapore, barcelona-vs-amsterdam, berlin-vs-hamburg, brazil-vs-peru, china-vs-hong-kong, cuba-vs-dominican-republic, curacao-vs-jamaica, denmark-vs-portugal, england-vs-latvia, england-vs-new-zealand, england-vs-spain, fiji-vs-maldives, frankfurt-vs-munich, greece-vs-italy, iceland-vs-alaska, incheon-vs-seoul, ireland-vs-portugal, istanbul-vs-athens, japan-vs-korea, japan-vs-singapore, japan-vs-thailand, liverpool-vs-paris, maldives-vs-hawaii, mexico-vs-puerto-rico, new-york-vs-los-angeles, norway-vs-finland, peru-vs-mexico, portugal-vs-turkey, shenzhen-vs-hong-kong, vietnam-vs-laos

#### F (33 pages) — Best for Couples/Solo/Family
argentina-vs-germany, bahrain-vs-japan, bali-vs-hawaii, bali-vs-maldives, bali-vs-phuket, bangkok-vs-ho-chi-minh, chile-vs-mexico, colombia-vs-spain, denmark-vs-scotland, denver-vs-san-francisco, england-vs-south-africa, france-vs-england, france-vs-poland, france-vs-usa, germany-vs-turkey, greece-vs-scotland, guatemala-vs-mexico, hiroshima-vs-kyoto, honduras-vs-jamaica, iceland-vs-scotland, italy-vs-norway, italy-vs-slovenia, japan-vs-brazil, japan-vs-philippines, lisbon-vs-barcelona, manchester-vs-london, new-zealand-vs-norway, philippines-vs-thailand, prague-vs-krakow, rome-vs-paris, tokyo-vs-osaka, tokyo-vs-shanghai, yokohama-vs-tokyo

#### G (33 pages) — Pros, Cons & Verdict
amsterdam-vs-berlin, amsterdam-vs-copenhagen, barcelona-vs-frankfurt, belgium-vs-italy, brazil-vs-senegal, brazil-vs-usa, bulgaria-vs-spain, california-vs-hawaii, chicago-vs-new-york, chicago-vs-vancouver, costa-rica-vs-mexico, croatia-vs-england, croatia-vs-spain, cuba-vs-mexico, dominican-republic-vs-mexico, ecuador-vs-mexico, england-vs-greece, germany-vs-italy, hungary-vs-portugal, iceland-vs-new-zealand, iceland-vs-slovenia, jamaica-vs-st-lucia, japan-vs-nepal, lyon-vs-paris, morocco-vs-spain, nepal-vs-scotland, norway-vs-switzerland, portugal-vs-usa, sacramento-vs-san-francisco, san-diego-vs-san-francisco, shanghai-vs-hong-kong, sweden-vs-turkey, vienna-vs-budapest

#### H (34 pages) — 2026 Showdown
armenia-vs-portugal, barcelona-vs-guadalajara, barcelona-vs-monaco, beijing-vs-hong-kong, berlin-vs-vienna, bolivia-vs-japan, brazil-vs-argentina, cuba-vs-nicaragua, florence-vs-barcelona, germany-vs-montenegro, germany-vs-scotland, germany-vs-sweden, germany-vs-usa, greece-vs-turkey, hawaii-vs-caribbean, japan-vs-netherlands, lisbon-vs-rome, london-vs-paris, los-angeles-vs-las-vegas, madrid-vs-barcelona, mexico-vs-uruguay, mexico-vs-usa, munich-vs-vienna, netherlands-vs-spain, new-york-vs-miami, paris-vs-barcelona, poland-vs-portugal, portugal-vs-slovenia, san-francisco-vs-new-york, seychelles-vs-maldives, sweden-vs-united-states, thailand-vs-cambodia, tokyo-vs-beijing, vienna-vs-prague

#### I (33 pages) — 7 Differences
argentina-vs-italy, argentina-vs-mexico, bahamas-vs-costa-rica, bangkok-vs-hanoi, bangkok-vs-phuket, belgium-vs-england, brazil-vs-colombia, bulgaria-vs-ireland, colombia-vs-portugal, costa-rica-vs-hawaii, croatia-vs-montenegro, dubai-vs-abu-dhabi, faroe-islands-vs-iceland, france-vs-iceland, france-vs-mexico, germany-vs-netherlands, germany-vs-slovenia, greece-vs-rome, greece-vs-spain, hong-kong-vs-japan, hungary-vs-sweden, ireland-vs-new-zealand, ireland-vs-south-africa, kyoto-vs-marrakech, mexico-vs-thailand, miami-vs-porto, netherlands-vs-scotland, portugal-vs-morocco, rome-vs-athens, thailand-vs-indonesia, thailand-vs-maldives, tokyo-vs-hong-kong, vietnam-vs-cambodia

#### J (33 pages) — Where to Spend a Week
atlanta-vs-miami, barcelona-vs-mallorca, brussels-vs-paris, colombia-vs-mexico, croatia-vs-france, denmark-vs-greece, dubai-vs-qatar, dubai-vs-singapore, dublin-vs-london, ecuador-vs-germany, england-vs-sweden, estonia-vs-norway, france-vs-norway, germany-vs-mexico, germany-vs-portugal, germany-vs-slovakia, hawaii-vs-puerto-rico, hong-kong-vs-singapore, iceland-vs-switzerland, israel-vs-italy, jamaica-vs-usa, lithuania-vs-sweden, macau-vs-hong-kong, new-york-vs-tokyo, osaka-vs-fukuoka, palma-vs-barcelona, paris-vs-amsterdam, portugal-vs-croatia, portugal-vs-uzbekistan, pyongyang-vs-seoul, slovenia-vs-croatia, tokyo-vs-kyoto, vietnam-vs-malaysia

### Measurement plan

1. **Wait 3–14 days** for Google to recrawl and reindex titles. Spot-check via `site:tabiji.ai/compare/` queries to confirm the variant titles show up in SERPs (Google occasionally rewrites titles).
2. **Run for ≥21 days** post-reindex to accumulate enough impressions per arm. With ~33 pages per arm and the section's ~96K imps spread across ~835 pages, expect ~3,800 imps per arm over 21 days — adequate but not abundant; single-page outliers can still dominate.
3. **Pull a fresh GSC Pages export** and:
   - Compute per-arm CTR delta vs. each arm's pre-rollout 28-day baseline.
   - Compare each variant against Control head-to-head.
   - Report position alongside CTR; flag any arm shifting >0.5 weighted position (titles affecting rank is a confound).
   - Per-fame-bucket breakdown: arm × {big-vs-big, big-vs-niche} CTR. The big-vs-big subset is where the upside is biggest — variants that win big-vs-big are the rollout candidates even if average CTR is unchanged.

### Decision rules

- **A variant beats Control by ≥0.3pp aggregate CTR** with no position regression and positive delta on ≥60% of pages → roll out to remaining /compare/ cohort (big-vs-big + big-vs-niche).
- **A variant wins specifically on big-vs-big** by ≥0.5pp with ≥6 of ~10 BvB pages positive → roll out only to BvB pages, retest on big-vs-niche separately.
- **Multiple variants beat Control** → roll out the strongest. Retest runners-up against the new winner in round 2.
- **A variant clearly loses** (≤−0.3pp, ≥60% of pages negative) → eliminate.
- **No variant beats Control** → no rollout. Hypothesize different angles for round 2 (specific dollar amounts, named-destination concreteness, etc.).

### Risks / confounds

- **Sample size:** ~33 pages per arm is small; a single high-CTR or 0-CTR page can dominate aggregate. Per-fame-bucket reads (BvB vs BvN) are cleaner signals for the BvB subset where the leverage is.
- **Position drift:** Google may re-rank after title change. Report position alongside CTR; flag drift >0.5.
- **Title rewriting by Google:** Google sometimes substitutes its own title in SERPs. Spot-check 5–10 cities per arm during the test.
- **Title length truncation:** 23% over 60 chars; consistent across arms, doesn't bias.
- **Niche-vs-niche cohort untouched:** intentional. If a winning variant emerges, decide *separately* whether to roll out to niche pages — they're already at 0.67% CTR and may have different optimal hooks.
- **Generator regression:** any future compare-page generator that runs on these pages must respect the test (don't rewrite titles back to Control template). Worth checking `scripts/batch-compare-gen.py` and any generator before next batch.

### Round 1 review checklist (target: 2026-05-30)

- [ ] Pull fresh GSC Pages export
- [ ] Per-arm aggregate CTR delta vs. baseline
- [ ] Per-arm head-to-head vs Control
- [ ] BvB-subset CTR per arm (highest leverage)
- [ ] Position drift check per arm
- [ ] Title-rewrite spot-check (`site:` queries)
- [ ] Append round-1 results section to this doc
- [ ] Decide rollout scope per decision rules above

### Rollout artifacts

- Script: [scripts/apply_compare_titles.py](../scripts/apply_compare_titles.py) — idempotent; reads assignment from `scripts/data/`.
- Cohort assignments: [scripts/data/compare-title-experiment-assignments.json](../scripts/data/compare-title-experiment-assignments.json) — 364 slugs → arm map.
- Pre-test analysis (informed cohort design): documented in this PR's description; key patterns also captured in conversation transcripts referenced by `MEMORY.md`.
