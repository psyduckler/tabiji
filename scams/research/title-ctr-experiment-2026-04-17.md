# /scams/ Title CTR Experiment — 2026-04-17

## Hypothesis
The current title template — `{N} Tourist Scams in {City} (2026) — Real Stories & How to Avoid Them | tabiji.ai` — is uniform across all 354 scam pages and has never been varied. Different title framings (authority, loss-aversion, question-match) may lift SERP CTR above the current 1.86% cluster average, without changing rank.

## Selection: top 20 /scams/ city pages by impressions

Source: `/Users/bjh/Desktop/tabiji.ai-Performance-on-Search-2026-04-17/Pages.csv` (top 1,000 pages by impressions, pulled 2026-04-17).

Cluster totals for `/scams/`: **99 pages, 100 clicks, 5,383 impressions, CTR 1.86%, weighted avg pos ~6.3.**

Top 20 city pages capture **45% of all /scams/ impressions (2,420 of 5,383)** and span a wide performance range — from pages at 0% CTR despite 130+ impressions (Sofia, Tokyo, Prague) to pages at 4–5% CTR (Vienna, Kyoto, Bratislava). The 0-CTR high-impression pages are the primary learning opportunity: something about the current title isn't hooking searchers at all.

| Rank | City | Clicks | Impr. | CTR | Position | Scam count |
|---|---|---:|---:|---:|---:|---:|
| 1 | Bucharest | 1 | 219 | 0.46% | 7.1 | 7 |
| 2 | Buenos Aires | 1 | 188 | 0.53% | 8.6 | 7 |
| 3 | Vienna | 8 | 179 | 4.47% | 6.7 | 7 |
| 4 | Hong Kong | 6 | 176 | 3.41% | 6.3 | 5 |
| 5 | Riga | 1 | 160 | 0.62% | 6.7 | 6 |
| 6 | Sofia | 0 | 135 | 0.00% | 6.5 | 6 |
| 7 | Tokyo | 0 | 132 | 0.00% | 7.2 | 9 |
| 8 | Prague | 0 | 130 | 0.00% | 9.3 | 7 |
| 9 | Tunis | 3 | 117 | 2.56% | 6.1 | 7 |
| 10 | Kyoto | 6 | 116 | 5.17% | 6.2 | 8 |
| 11 | San Juan | 0 | 111 | 0.00% | 7.3 | 6 |
| 12 | Budapest | 0 | 109 | 0.00% | 8.5 | 8 |
| 13 | Mumbai | 1 | 106 | 0.94% | 8.2 | 8 |
| 14 | Medellín | 0 | 93 | 0.00% | 6.3 | 8 |
| 15 | Seoul | 1 | 84 | 1.19% | 5.7 | 6 |
| 16 | Kathmandu | 3 | 78 | 3.85% | 6.5 | 8 |
| 17 | Lima | 0 | 75 | 0.00% | 7.6 | 7 |
| 18 | Hurghada | 0 | 72 | 0.00% | 7.7 | 7 |
| 19 | Copenhagen | 1 | 71 | 1.41% | 7.4 | 5 |
| 20 | Bratislava | 3 | 69 | 4.35% | 6.0 | 5 |
| | **Total (20)** | **35** | **2,420** | **1.45%** | ~7.12 | |

## Arm assignment: snake-assigned by CTR rank (balanced baselines)

Round-robin by impression rank would cluster high-CTR pages into some arms and 0-CTR pages into others, producing arm-level baseline CTRs from 0.89% to 2.14% — a 2.4× gap that would confound post-experiment attribution. Snake assignment by CTR rank (1→2→3→4, 4→3→2→1, …) produces arms with baselines within 0.4pp of each other.

| City | Impr. | Baseline CTR | Position | Arm |
|---|---:|---:|---:|---|
| Kyoto | 116 | 5.17% | 6.2 | **Control** |
| Vienna | 179 | 4.47% | 6.7 | V1 |
| Bratislava | 69 | 4.35% | 6.0 | V2 |
| Kathmandu | 78 | 3.85% | 6.5 | V3 |
| Hong Kong | 176 | 3.41% | 6.3 | V3 |
| Tunis | 117 | 2.56% | 6.1 | V2 |
| Copenhagen | 71 | 1.41% | 7.4 | V1 |
| Seoul | 84 | 1.19% | 5.7 | **Control** |
| Mumbai | 106 | 0.94% | 8.2 | **Control** |
| Riga | 160 | 0.62% | 6.7 | V1 |
| Buenos Aires | 188 | 0.53% | 8.6 | V2 |
| Bucharest | 219 | 0.46% | 7.1 | V3 |
| Sofia | 135 | 0.00% | 6.5 | V3 |
| Tokyo | 132 | 0.00% | 7.2 | V2 |
| Prague | 130 | 0.00% | 9.3 | V1 |
| San Juan | 111 | 0.00% | 7.3 | **Control** |
| Budapest | 109 | 0.00% | 8.5 | **Control** |
| Medellín | 93 | 0.00% | 6.3 | V1 |
| Lima | 75 | 0.00% | 7.6 | V2 |
| Hurghada | 72 | 0.00% | 7.7 | V3 |

### Arm baseline totals

| Arm | Pages | Impressions | Clicks | Baseline CTR | Weighted pos |
|---|---:|---:|---:|---:|---:|
| **Control** (no change) | 5 | 526 | 8 | **1.52%** | 7.32 |
| **V1** (Authority framing) | 5 | 633 | 10 | **1.58%** | 7.16 |
| **V2** (Loss-aversion) | 5 | 581 | 7 | **1.20%** | 7.62 |
| **V3** (Question-match) | 5 | 680 | 10 | **1.47%** | 6.79 |

Arm CTRs now span 1.20–1.58% (0.38pp gap) — tight enough for fair post-comparison. V2 runs a bit low on baseline, which means any lift it shows has a slightly lower bar than the others — worth noting when interpreting results.

## Variant title patterns

All three variants are ~50–55 characters before the ` | tabiji.ai` brand suffix — well under Google's ~60-char mobile truncation threshold. The current Control titles are ~68 chars, so any CTR lift could be partially attributable to "full title shown" vs "truncated." Acceptable confound for round 1; if a winner emerges, round 2 can test shorter-vs-current Control.

### V1 — Authority / "Locals Want Tourists to Know"
**Pattern:** `{N} {City} Scams Locals Want Tourists to Know (2026)`
**Thesis:** Implied local-insider framing differentiates from generic listicle competitors on the SERP.

| Page | New title |
|---|---|
| Vienna | `7 Vienna Scams Locals Want Tourists to Know (2026) \| tabiji.ai` |
| Copenhagen | `5 Copenhagen Scams Locals Want Tourists to Know (2026) \| tabiji.ai` |
| Riga | `6 Riga Scams Locals Want Tourists to Know (2026) \| tabiji.ai` |
| Prague | `7 Prague Scams Locals Want Tourists to Know (2026) \| tabiji.ai` |
| Medellín | `8 Medellín Scams Locals Want Tourists to Know (2026) \| tabiji.ai` |

### V2 — Loss-aversion / "Don't Fall for These"
**Pattern:** `Don't Fall for These {N} Tourist Scams in {City} (2026)`
**Thesis:** Loss-aversion imperative creates a stronger curiosity gap than the neutral "How to Avoid Them."

| Page | New title |
|---|---|
| Bratislava | `Don't Fall for These 5 Tourist Scams in Bratislava (2026) \| tabiji.ai` |
| Tunis | `Don't Fall for These 7 Tourist Scams in Tunis (2026) \| tabiji.ai` |
| Buenos Aires | `Don't Fall for These 7 Tourist Scams in Buenos Aires (2026) \| tabiji.ai` |
| Tokyo | `Don't Fall for These 9 Tourist Scams in Tokyo (2026) \| tabiji.ai` |
| Lima | `Don't Fall for These 7 Tourist Scams in Lima (2026) \| tabiji.ai` |

### V3 — Question-match / "Is {City} Safe for Tourists?"
**Pattern:** `Is {City} Safe for Tourists? {N} Scams to Avoid (2026)`
**Thesis:** Many 0-CTR high-impression pages (Sofia, Bucharest, Hurghada) likely rank partly for "is {city} safe" queries — intent the current title ignores entirely. A question-match hook captures both the "tourist scams in X" query cluster *and* the "is X safe" cluster.

| Page | New title |
|---|---|
| Kathmandu | `Is Kathmandu Safe for Tourists? 8 Scams to Avoid (2026) \| tabiji.ai` |
| Hong Kong | `Is Hong Kong Safe for Tourists? 5 Scams to Avoid (2026) \| tabiji.ai` |
| Bucharest | `Is Bucharest Safe for Tourists? 7 Scams to Avoid (2026) \| tabiji.ai` |
| Sofia | `Is Sofia Safe for Tourists? 6 Scams to Avoid (2026) \| tabiji.ai` |
| Hurghada | `Is Hurghada Safe for Tourists? 7 Scams to Avoid (2026) \| tabiji.ai` |

### Control (no change — baseline for comparison)
- Kyoto, Seoul, Mumbai, San Juan, Budapest

## What's being changed vs held constant

- **Changed:** `<title>` tag, `<meta property="og:title">`, `<meta name="twitter:title">` (kept in sync so social cards match)
- **Held constant (so title can be attributed as the sole variable):**
  - Meta description
  - H1 on page
  - Body content
  - URL
  - Internal links
  - Page structure

## Measurement plan

1. **Wait 3–14 days** after applying changes for Google to re-crawl and re-index the titles. Spot-check via `site:tabiji.ai/scams/sofia/` that the new titles are showing in SERPs.
2. **Let the experiment run for at least 21 days** post-reindex to accumulate enough impressions per arm.
3. **Pull a fresh GSC Pages export** over a comparable date range and compute:
   - CTR per page, before vs after
   - Aggregate CTR per arm (Control, V1, V2, V3)
   - Position per page (should be stable — meaningful drift is a confound)
4. **Decision rule:**
   - If one variant beats Control by ≥0.5pp aggregate CTR with no position regression → roll that pattern out to the remaining ~340 pages.
   - If multiple variants beat Control → roll out the strongest, retest runners-up in round 2.
   - If none beats Control → no rollout; try different hypotheses (named-scam specificity, currency/loss concreteness, etc.).

## Risks / confounds to watch

- **Position drift** — Google may re-rank after title change (up or down). Report CTR at held-constant position where possible, and flag any arm where weighted position shifted by >0.5.
- **Title length confound** — variants are ~15 chars shorter than Control. Part of any lift may be "full title shown in SERP" rather than framing. Round 2 can isolate this by testing shorter Control.
- **Seasonal query mix shift** — tourism queries shift by season. A 3-week window in April–May should be consistent, but flag any news-driven spikes on a specific city.
- **Google rewriting titles** — Google sometimes rewrites titles in SERPs. Spot-check with `site:` queries during the experiment to confirm the variant titles are actually showing.
- **V3 intent match quality** — if "Is {City} Safe?" pulls in queries the page doesn't fully answer (e.g., crime rates, political unrest — not just scams), CTR might rise but bounce rate too. Worth checking bounce in GA/analytics alongside CTR.

## Rollback plan
Each edit is a single commit per page. If CTR regresses meaningfully on any page, revert that page's title via `git revert <sha>`.

## Post-experiment state to record

When the follow-up CSV arrives:
- [ ] Paste new top-20 rows into a new section below
- [ ] Compute per-arm CTR delta vs baseline in this doc
- [ ] Note position changes
- [ ] Declare winner / no-winner
- [ ] Decide rollout scope for the remaining ~334 /scams/ pages
