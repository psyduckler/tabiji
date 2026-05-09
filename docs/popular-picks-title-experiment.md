# /popular-picks/ Title CTR Experiment

History of CTR-driven title-tag experiments on `/popular-picks/{slug}/` pages. Each round's setup, baseline, results, and follow-up plan recorded below in chronological order.

> Doc location follows `docs/title-ctr-experiment.md` (/scams/) and `docs/compare-title-experiment.md` (/compare/) — `docs/` is not deployed, durable home for experiment artifacts.

---

## Round 1 — 2026-05-09

### Motivation

After /scams/ (round 1 done, round 2 deployed) and /compare/ (round 1 deployed), /popular-picks/ is the third major page-type CTR test. The 2026-05-09 GSC export shows the section running at 0.52% CTR — between /compare/ (0.44%) and /scams/ (2.47%) — but with the largest impression base on the site. Position is barely a factor (pos 4–10 → 0.56% CTR vs pos 11–20 → 0.51% — almost flat); same lesson as scams + compare: title/snippet is the lever, not ranking.

### Pre-test pattern analysis (2026-05-09 export)

Heads-up: same deletion pattern we hit on /compare/ — but worse. Across 1,000 popular-picks URLs in the GSC export:

| Subset | URLs | Clicks | Imps | CTR |
|---|---:|---:|---:|---:|
| **Live URLs** | 370 | 308 | 64,711 | 0.48% |
| **Deleted URLs** | 630 | 769 | 141,230 | 0.54% |

**63% of GSC popular-picks URLs are deleted** — they account for 71% of clicks and 69% of impressions. The Casablanca cluster I'd previously flagged as a "CTR sinkhole" turns out to be all 404s/redirects (`casablanca-coffee-shops`, `casablanca-working-cafes`, `casablanca-bakeries`, etc.). Restoration is a separate workstream — same pattern as the /compare/ tier-1 restoration in PR #1487.

After restricting to the 876 live pages, topic-CTR distribution looks like this:

| Bucket | Pages | Imps | CTR | Top topics by imps |
|---|---:|---:|---:|---|
| **Losers** (high imps, <0.5% CTR) | 117 | 14,285 | **0.29%** | fine-dining, rooftop-bars, street-food, coffee-shops, speakeasy |
| **Mid-tier** (some signal, mid CTR) | 489 | 42,170 | 0.47% | pizza, cocktail-bars, restaurants, sushi, omakase, ramen, craft-beer, art-galleries |
| **Winners** (>1% CTR with substantive imps) | 20 | 1,908 | **1.83%** | bbq, tea-houses, mochi, mofongo, yuba |
| **Low-data** (<200 imps each topic) | 250 | 6,305 | 0.54% | long tail of one-off cuisine topics |

### Hypothesis

Specificity wins on this section (top performers are bookshops/jjimjilbangs/jazz-bars/mochi — niche topics in less-covered cities), but the section's biggest impression haul flows through generic-topic pages (coffee-shops, rooftop-bars, fine-dining) that are losing the SERP click war to authority listicle generators. Different title framings — particularly insider/locals, hidden-gem discovery, and Reddit-authority hooks — should lift CTR on the generic-topic + struggling mid-tier subset. Niche winners are excluded; they're already at 1–5% CTR and a worse title risks downside.

### Cohort selection

**Filter:**
- INCLUDE: live pages whose *topic* has ≥500 total live-page imps in the snapshot AND topic CTR <1.0% (i.e., the loser + struggling mid-tier subset)
- EXCLUDE: winning topics (bbq is the only one meeting >1% CTR with ≥500 imps from live pages)
- EXCLUDE: low-data topics (212 of 245 topics have <500 imps from live pages — signal too noisy)

**Result:** 440 candidate pages from 32 topics → top 300 by live-page impressions selected. Cohort baseline CTR: **199 clicks / 44,536 imps = 0.45%**.

### Cohort assignment

300 pages stratified-snake balanced across 6 arms × 50 pages by live-page impressions (block-of-6 deterministic shuffle). Per-arm baseline (from 2026-05-09 GSC snapshot, [docs/data/gsc-snapshots/popular-picks-pages-2026-05-09.csv](data/gsc-snapshots/popular-picks-pages-2026-05-09.csv)):

| Arm | Pages | WithGSC | Imps | Clicks | CTR | WeightedPos |
|---|---:|---:|---:|---:|---:|---:|
| Control | 50 | 36 | 7,105 | 32 | **0.45%** | 19.54 |
| A | 50 | 36 | 7,599 | 27 | **0.36%** | 24.88 |
| B | 50 | 36 | 7,310 | 37 | **0.51%** | 17.65 |
| C | 50 | 36 | 7,886 | 34 | **0.43%** | 22.64 |
| D | 50 | 37 | 7,356 | 36 | **0.49%** | 18.70 |
| E | 50 | 37 | 7,280 | 33 | **0.45%** | 17.22 |
| **Total cohort** | **300** | **218** | **44,536** | **199** | **0.45%** | — |

Per-arm baseline CTR is within 0.36–0.51% (0.15pp range — tighter than /compare/ round 1). Weighted-position spread is 7 positions (B 17.65 → A 24.88) — wider than ideal. Variants whose post-rollout position drifts >1 should be flagged at review time.

### Variant title patterns

All three meta tags (`<title>`, `<meta property="og:title">`, `<meta name="twitter:title">`) are kept in sync — that matches the existing popular-picks pattern (different from /scams/ and /compare/, where they diverge slightly).

#### Control — Current default
**Pattern:** `{N} Best {Topic} in {City} (2026) | tabiji.ai`
**Example:** `10 Best Ramen in Tokyo (2026) | tabiji.ai`

#### A — Where-to query match
**Pattern:** `Where Are the Best {Topic} in {City}? (2026 Honest Guide) | tabiji.ai`
**Hypothesis:** Mirror of /scams/ V3 winner ("Is X Safe?"). Searchers type "where are the best coffee shops in casablanca" — current titles ignore the question form. "Honest" signals editorial stance.
**Example:** `Where Are the Best Coffee Shops in Amman? (2026 Honest Guide) | tabiji.ai`

#### B — Where Locals Actually Go (insider voice)
**Pattern:** `Best {Topic} in {City}: Where Locals Actually Go (2026) | tabiji.ai`
**Hypothesis:** "Actually" cuts the doubt every traveler has about generic listicles. The top-CTR pages (bookshops, jjimjilbangs, tea-houses) are already winning on a similar trust axis — formalizes that signal in the title. Highly shareable on Pinterest/Reddit/IG.
**Example:** `Best Shawarma in Amman: Where Locals Actually Go (2026) | tabiji.ai`

#### C — Most Tourists Miss (curiosity gap)
**Pattern:** `{N} {Topic} in {City} Most Tourists Miss (2026) | tabiji.ai`
**Hypothesis:** Strong curiosity gap with concrete payoff. "Hidden gems / off-the-beaten-path" framing is travel-content evergreen — searchers WANT this exact promise. Differentiates structurally from "10 Best X" listicles (every authority site has those).
**Example:** `9 Stroopwafel in Amsterdam Most Tourists Miss (2026) | tabiji.ai`

#### D — No Tourist Traps (editorial filter)
**Pattern:** `{N} {Topic} in {City} Worth Knowing (No Tourist Traps) (2026) | tabiji.ai`
**Hypothesis:** "No tourist traps" hits a specific anxiety travelers carry. Implies aggressive editorial filtering — fewer items but higher confidence per item. Different from B (cites locals) and C (promises hidden things) — D promises *what's been excluded*.
**Example:** `12 Fine Dining in Bangkok Worth Knowing (No Tourist Traps) (2026) | tabiji.ai`

#### E — Reddit Locals Recommend (authority/community)
**Pattern:** `{Topic} in {City}: What Reddit Locals Recommend (2026) | tabiji.ai`
**Hypothesis:** Reddit is one of the most-appended search modifiers in travel queries — searchers actively distrust SEO listicles and seek community-vetted answers. Front-loads the trust signal currently buried in meta descriptions. Same hypothesis we're testing for /compare/ round 1 D — if it wins both we have a portable lesson.
**Example:** `Cocktail Bars in Bucharest: What Reddit Locals Recommend (2026) | tabiji.ai`

### Title length

108/300 (36%) titles run >60 chars pre-brand-suffix, mostly variant D (which is structurally the longest pattern) and pages with long compound city names (San Francisco, Buenos Aires, Ho Chi Minh City). Truncation is consistent across arms; doesn't bias the comparison.

### What's held constant

- Meta description
- H1 on page
- Body content (item list, descriptions, internal links)
- URL
- Schema (Article, ItemList, numberOfItems)
- Inventory data (descriptions used by hubs)

### Cohort assignments

#### Control (50)
accra-street-food, albuquerque-pizza, amsterdam-craft-beer, antwerp-art-galleries, asheville-pizza, athens-art-galleries, athens-pizza, atlanta-fine-dining, austin-cooking-classes, austin-speakeasy, austin-vegetarian-restaurants, bangkok-rooftop-bars, bangkok-street-food, barcelona-art-galleries, beijing-craft-beer, belgrade-rooftop-bars, bogota-arepas, boston-cocktail-bars, bratislava-coffee-shops, charlotte-steak, chicago-cooking-classes, cleveland-pizza, da-nang-coffee-shops, dallas-steak, edinburgh-restaurants, hamburg-cocktail-bars, istanbul-rooftop-restaurants, knoxville-coffee-shops, kolkata-street-food, lisbon-restaurants, madrid-restaurants, manchester-pizza, marrakech-street-food, miami-coffee-shops, new-orleans-restaurants, nungwi-beach-bars, osaka-cheap-eats, oslo-restaurants, prague-restaurants, roppongi-cocktail-bars, san-diego-pizza, san-diego-speakeasy, sapporo-ramen, seattle-cocktail-bars, shoreditch-coffee-shops, singapore-craft-beer, tokyo-craft-beer, tokyo-omakase, tokyo-ramen, zurich-craft-beer

#### A (50) — Where Are the Best
adelaide-art-galleries, adelaide-street-food, almaty-street-food, amman-coffee-shops, amsterdam-fine-dining, amsterdam-restaurants, amsterdam-street-food, ann-arbor-sushi, athens-restaurants, atlanta-pizza, auckland-art-galleries, austin-art-galleries, austin-pizza, austin-steak, baku-fine-dining, baltimore-coffee-shops, bangkok-restaurants, boston-dim-sum, boston-kebab, boston-omakase, bratislava-craft-beer, bruges-beer-bars, budapest-ruin-bars, chiang-mai-cooking-classes, chicago-dim-sum, chicago-fine-dining, chicago-restaurants, chicago-rooftop-bars, colombo-coffee-shops, copenhagen-bakeries, dallas-bars, dallas-restaurants, houston-cooking-classes, kobe-sushi, kyoto-restaurants, lima-restaurants, louisville-pizza, mexico-city-coffee-shops, miami-rooftop-bars, montreal-restaurants, new-york-ramen, oslo-seafood-restaurants, paris-restaurants, phoenix-speakeasy, prague-cheap-eats, rome-cooking-classes, san-diego-omakase, seattle-fine-dining, siena-pizza, washington-dc-pizza

#### B (50) — Where Locals Actually Go
abu-dhabi-cheap-eats, abu-dhabi-street-food, amman-rooftop-bars, amman-shawarma, amman-street-food, amsterdam-cheap-eats, amsterdam-photography-spots, atlanta-cooking-classes, atlanta-speakeasy, austin-craft-beer, austin-photography-spots, austin-ramen, austin-sushi, bangkok-art-galleries, bangkok-sushi, barcelona-fine-dining, barcelona-restaurants, boston-restaurants, bucharest-craft-beer, cairo-street-food, canggu-beach-clubs, chicago-art-galleries, chicago-deep-dish-pizza, chicago-speakeasy, chicago-vegetarian-restaurants, copenhagen-restaurants, dallas-pizza, florence-restaurants, harajuku-crepes, hong-kong-dim-sum, ipoh-dim-sum, kanazawa-sushi, kuala-lumpur-rooftop-bars, kyoto-ramen, las-vegas-speakeasy, lisbon-rooftop-bars, miami-omakase, miami-restaurants, new-orleans-cocktail-bars, oaxaca-street-food, philadelphia-restaurants, portland-coffee-shops, porto-restaurants, providence-pizza, san-antonio-steak, san-francisco-omakase, seattle-cooking-classes, shibuya-ramen, tampa-pizza, zurich-coffee-shops

#### C (50) — Most Tourists Miss
abu-dhabi-photography-spots, adelaide-bakeries, adelaide-cocktail-bars, adelaide-coffee-shops, amsterdam-coffee-shops, amsterdam-stroopwafel, antwerp-fine-dining, antwerp-street-food, atlanta-coffee-shops, atlanta-steak, auckland-seafood-restaurants, austin-fine-dining, ayutthaya-street-food, baltimore-fine-dining, baltimore-street-food, beijing-photography-spots, beijing-street-food, berlin-craft-beer, boston-ramen, brussels-beer-bars, bucharest-coffee-shops, buenos-aires-cocktail-bars, buenos-aires-pizza, cartagena-street-food, chicago-cocktail-bars, chicago-omakase, chicago-pizza, chicago-sushi, cusco-restaurants, dallas-coffee-shops, delhi-restaurants, denver-restaurants, denver-steak, fukuoka-ramen, ho-chi-minh-rooftop-bars, honolulu-sushi, kyoto-street-food, minneapolis-coffee-shops, new-york-craft-beer, new-york-steak, osaka-okonomiyaki, penang-street-food, rome-pizza, seattle-speakeasy, split-beach-bars, tbilisi-coffee-shops, tucson-pizza, tulum-beach-clubs, verona-pizza, victoria-pizza

#### D (50) — Worth Knowing (No Tourist Traps)
albuquerque-sushi, amsterdam-art-galleries, antwerp-cheap-eats, antwerp-coffee-shops, athens-street-food, atlanta-sushi, austin-cheap-eats, austin-street-food, baltimore-pizza, bangkok-fine-dining, barcelona-cheap-eats, barcelona-photography-spots, beijing-cheap-eats, belgrade-art-galleries, belgrade-street-food, boston-cooking-classes, boston-craft-beer, boston-sushi, budapest-langos, cairo-kebab, charlotte-pizza, chicago-bars, cincinnati-pizza, cleveland-steak, dallas-speakeasy, dubai-rooftop-bars, guangzhou-dim-sum, hanoi-restaurants, houston-steak, istanbul-street-food, kadikoy-street-food, los-angeles-pizza, los-angeles-ramen, milan-pizza, nagoya-sushi, new-york-matcha, new-york-restaurants, palermo-pizza, paris-cheap-eats, pittsburgh-speakeasy, portland-craft-beer, portland-restaurants, rome-restaurants, san-diego-coffee-shops, santa-fe-art-galleries, scottsdale-sushi, seattle-omakase, shanghai-dim-sum, singapore-rooftop-bars, sofia-pizza

#### E (50) — Reddit Locals Recommend
adelaide-fine-dining, adelaide-photography-spots, albuquerque-coffee-shops, amalfi-pizza, asakusa-street-food, athens-fine-dining, athens-photography-spots, athens-rooftop-bars, atlanta-rooftop-bars, atlanta-vegetarian-restaurants, auckland-fine-dining, austin-coffee-shops, baku-street-food, bali-cooking-classes, bali-fine-dining, barcelona-pizza, barcelona-street-food, berlin-doner-kebab, boston-bars, boston-coffee-shops, boston-pizza, boston-speakeasy, bucharest-cocktail-bars, chiang-mai-coffee-shops, chicago-coffee-shops, chicago-steak, columbus-pizza, dallas-cooking-classes, denver-coffee-shops, denver-cooking-classes, genoa-pizza, ghent-craft-beer, hiroshima-okonomiyaki, kyoto-matcha, kyoto-sushi, london-restaurants, marrakech-hammams, miami-cocktail-bars, montreal-steak, nashville-bars, new-york-dollar-pizza, new-york-omakase, new-york-speakeasy, phnom-penh-rooftop-bars, porto-pizza, prague-svickova, san-antonio-speakeasy, seattle-coffee-shops, st-louis-pizza, tokyo-steak

### Measurement plan

1. **Wait 3–14 days** for Google to recrawl/reindex titles. Spot-check via `site:tabiji.ai/popular-picks/` to confirm titles are showing in SERPs (Google sometimes substitutes its own).
2. **Run for ≥21 days** post-reindex. Cohort baseline is 199 clicks / 44.5K imps in a 28-day window — expect 150–200 imps per page over the test window, modest but adequate for 50-page arms.
3. **Pull a fresh GSC export** at review time and:
   - Per-arm CTR delta vs the 2026-05-09 baseline.
   - Each variant head-to-head vs Control.
   - Position drift per arm — flag any arm shifting >1 position.
   - **Per-topic breakdown**: arm × {coffee-shops, rooftop-bars, fine-dining, street-food, restaurants, etc.} CTR. The biggest leverage is on generic-loser topics (coffee-shops, rooftop-bars, fine-dining); a variant that wins specifically on those is more interesting than one that wins on cheap-eats or pizza which were already mid-tier.

### Decision rules

- **Variant beats Control by ≥0.3pp aggregate CTR** with no position regression and ≥60% of pages positive → roll out to remaining popular-picks cohort (loser + mid-tier topics).
- **Variant wins on generic-loser topics specifically** (coffee-shops + rooftop-bars + fine-dining together) by ≥0.5pp → roll out only to those topics. Retest others separately.
- **Multiple variants beat Control** → roll out the strongest. Retest runners-up against the new winner in round 2.
- **Variant clearly loses** (≤−0.3pp, ≥60% pages negative) → eliminate.
- **No variant beats Control** → no rollout. Hypothesize different angles for round 2 (concrete dollar amounts, neighborhood specificity, time-sensitive freshness, etc.).

### Risks / confounds

- **Sample size:** 50 pages per arm is workable but not abundant. With ~36 GSC-data pages per arm and only ~32–37 clicks per arm at baseline, single high-CTR or 0-CTR pages dominate aggregate. Per-topic reads are cleaner where data permits.
- **Position drift:** weighted positions span 17.22–24.88 across arms — unbalanced going in. If a variant's title also nudges position, the CTR delta gets confounded. Report position alongside CTR.
- **Title length:** 36% over 60 chars (variant D especially); consistent across arms.
- **Niche-winner cohort untouched** (bookshops, jazz-bars, tea-houses, mochi, etc.) — intentional. If a winning variant emerges, decide separately whether to extend to winners.
- **Deleted-page restoration** is a parallel workstream (similar to /compare/ tier-1 in PR #1487). 630 deleted popular-picks pages with 769 clicks of historical traffic represent a separate opportunity that doesn't belong in this title experiment.
- **Generator regression:** any popular-picks generator that runs on these pages must respect the test (don't rewrite assigned titles back to Control).

### Round 1 review checklist (target: 2026-05-30)

- [ ] Pull fresh GSC export, save as `docs/data/gsc-snapshots/popular-picks-pages-2026-05-30.csv`
- [ ] Per-arm aggregate CTR delta vs baseline
- [ ] Per-arm head-to-head vs Control
- [ ] Generic-loser-topic-subset CTR per arm (highest leverage)
- [ ] Position drift check per arm
- [ ] Title-rewrite spot-check (`site:` queries on 3–5 cities per arm)
- [ ] Append round-1 results section to this doc
- [ ] Decide rollout scope per decision rules above

### Rollout artifacts

- Script: [scripts/apply_popular_picks_titles.py](../scripts/apply_popular_picks_titles.py) — idempotent; reads from the enriched assignments JSON.
- Cohort + canonical city/topic/N values: [scripts/data/popular-picks-title-experiment-assignments.json](../scripts/data/popular-picks-title-experiment-assignments.json).
- T+0 baseline: [docs/data/gsc-snapshots/popular-picks-pages-2026-05-09.csv](data/gsc-snapshots/popular-picks-pages-2026-05-09.csv).
