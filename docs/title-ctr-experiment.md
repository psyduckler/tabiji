# /scams/ Title CTR Experiment

History of CTR-driven title-tag experiments on `/scams/{city}/` pages. Each round's setup, results, and follow-up plan is recorded below in chronological order.

> **Doc location note:** Originally lived at `scams/research/title-ctr-experiment-2026-04-17.md`; that path was deleted in PR #283 (2026-04-20) to fit Cloudflare Pages's 20K-file deploy cap. `docs/` is not deployed, so this file is the durable home going forward.

---

## Round 1 — 2026-04-17

### Hypothesis
The original title template — `{N} Tourist Scams in {City} (2026) — Real Stories & How to Avoid Them | tabiji.ai` — was uniform across all 354 scam pages and had never been varied. Different title framings (authority, loss-aversion, question-match) might lift SERP CTR above the cluster's 1.86% average without changing rank.

### Selection: top 20 /scams/ city pages by impressions
Source: `tabiji.ai-Performance-on-Search-2026-04-17/Pages.csv` (top 1,000 pages, pulled 2026-04-17). Cluster totals for `/scams/`: 99 pages, 100 clicks, 5,383 impressions, CTR 1.86%, weighted avg pos ~6.3. Top 20 captured ~45% of cluster impressions.

### Arm assignment (snake-balanced by baseline CTR)

| Arm | Pages | Pattern | Cities |
|---|---|---|---|
| Control | 5 | (no change) | Kyoto, Seoul, Mumbai, San Juan, Budapest |
| V1 — Authority | 5 | `{N} {City} Scams Locals Want Tourists to Know (2026) \| tabiji.ai` | Vienna, Copenhagen, Riga, Prague, Medellín |
| V2 — Loss-aversion | 5 | `Don't Fall for These {N} Tourist Scams in {City} (2026) \| tabiji.ai` | Bratislava, Tunis, Buenos Aires, Tokyo, Lima |
| V3 — Question-match | 5 | `Is {City} Safe for Tourists? {N} Scams to Avoid (2026) \| tabiji.ai` | Kathmandu, Hong Kong, Bucharest, Sofia, Hurghada |

Held constant: meta description, H1, body content, URL, internal links.

### Round 1 results — pulled 2026-05-08 (~21 days post-treatment)

**Critical caveat:** PR #1458 (2026-05-05, 3 days before the export) bulk-rewrote the scam template. It overwrote 4 variant pages back to the new short default and changed all 5 Control titles. So Control ran on its experimental title for 18 of 21 days; 4 variant pages got contaminated.

- **Variant pages overwritten (lost their experimental title):** Vienna (V1), Medellín (V1), Buenos Aires (V2), Hong Kong (V3)
- **Control pages (titles changed at day 18):** the old long template was replaced with the new short `N Tourist Scams in X — How to Avoid` everywhere

#### Per-arm aggregate (cities still on their assigned variant title)

| Arm | Pages | Baseline CTR | Post CTR | ΔCTR |
|---|---|---|---|---|
| Control | 4 | 1.92% | 1.50% | **−0.42pp** |
| V1 — "Locals Want Tourists to Know" | 3 | 0.55% | 1.08% | **+0.53pp** |
| V2 — "Don't Fall for These" | 3 | 1.89% | 1.61% | **−0.28pp** |
| V3 — "Is X Safe for Tourists?" | 3 | 0.93% | 2.85% | **+1.93pp** |

#### Per-page detail

**V3 (winner, every page positive):**
- Kathmandu: 3.85% → **7.61%** (+3.76pp) on 184 imps
- Sofia: 0.00% → **2.07%** (+2.07pp) on 290 imps
- Bucharest: 0.46% → **1.09%** (+0.63pp) on 367 imps
- Hong Kong: title overwritten before measurement

**V1 (mixed):**
- Riga: 0.62% → **1.77%** (+1.15pp) on 565 imps — drove most of the V1 lift
- Prague: 0.00% → 0.00% on 375 imps (flat; position improved 1.25)
- Copenhagen: 1.41% → 1.33% (flat) on 75 imps

**V2 (wash/negative):**
- Bratislava: 4.35% → **1.89%** (−2.46pp) — clear regression, position also worsened +0.66
- Tunis: 2.56% → 3.22% (+0.66pp)
- Tokyo: 0.00% → 0.18% (flat) on 543 imps

**Control:**
- Kyoto: 5.17% → 3.47% (−1.70pp) — biggest drag
- Seoul, Mumbai: flat
- San Juan: 0% → 0.75% (small gain)
- Budapest: dropped out of top-1000 GSC

### Round 1 read

- **V3 ("Is X Safe for Tourists?") is the clear winner.** Every measured page lifted; aggregate +1.93pp; the hypothesis (0-CTR pages were ranking for *is X safe* queries the old title ignored) was confirmed by Sofia and Bucharest moving 0%→1-2%.
- **V1 ("Locals Want Tourists to Know") is a soft second.** Riga drove most of the result; with n=3 and one driving page, treat as suggestive not conclusive.
- **V2 ("Don't Fall for These") did not work.** Bratislava's regression is large and not noise.
- **Decision:** roll out V3 as the new default for /scams/ pages. Round 2 expands V3 to a 200-page cohort and tests 5 fresh variants on smaller cohorts.

---

## Round 2 — 2026-05-08

### Goals
1. Confirm V3 lift holds on a much larger cohort (200 pages vs round 1's 5).
2. Hold a true 200-page Control on the post-#1458 short default — that's the new comparison baseline, since the old long template is extinct.
3. Test 5 fresh hypotheses on smaller (25-page) cohorts to surface candidates for round 3.

### Cohort

525 /scams/ city pages assigned across 7 arms by stratified-snake balancing on baseline impressions (block-of-21 pattern: 8 V3 + 8 Control + 1 each variant). Pre-locks before the snake-balance:

- **4 existing V3 cities** (bucharest, hurghada, kathmandu, sofia) → V3, to preserve continuity from round 1.
- **17 stragglers** (13 cities still on the deprecated long template + 4 small one-off variants) → Control, so the test starts from a clean uniform baseline. The 17: bergen, brasov, capri, cesky-krumlov, hakone, kanazawa, lake-garda, ljubljana, lofoten, mecca, nikko, pai, plovdiv, takayama, tromso, zagreb, zermatt.

| Arm | Pages | Baseline imps | Baseline CTR |
|---|---:|---:|---:|
| **V3** (winner from round 1, scaled) | **200** | 5,264 | 2.56% |
| **Control** (post-#1458 short default) | **200** | 4,692 | 2.88% |
| **A** (sharpen V3 deliverable) | **25** | 466 | 4.29% |
| **B** (insider voice) | **25** | 507 | 3.35% |
| **C** (named-scam concreteness) | **25** | 563 | 1.78% |
| **D** (pre-trip framing) | **25** | 854 | 2.22% |
| **E** (trending / current-state) | **25** | 488 | 1.84% |

Variant arm baselines run between 1.78% and 4.29% — wider spread than round 1's 0.38pp gap, an unavoidable cost of having 7 arms instead of 4. V3 vs Control (the head-to-head decision test) is well-balanced at 2.56% vs 2.88%.

The 17 stragglers were force-locked to Control after the initial snake assignment scattered them across non-Control arms; an 8-city impression-matched swap pulled them back to Control without disturbing per-arm baseline imps/CTR (all 8 swapped pairs had 0 baseline imps). Variant C's 25th city changed from `ljubljana` to `austin` as part of the swap; new headline scam name picked accordingly.

### Variant title patterns

All variants set `<title>`, `<meta property="og:title">`, and `<meta name="twitter:title">` in sync. Meta description, H1, body, URL, internal links are unchanged.

#### V3 — Question-match (round-1 winner, scaled)
**Pattern:** `Is {City} Safe for Tourists? {N} Scams to Avoid (2026) | tabiji.ai`
**Examples:**
- `Is Athens Safe for Tourists? 6 Scams to Avoid (2026) | tabiji.ai`
- `Is Copenhagen Safe for Tourists? 6 Scams to Avoid (2026) | tabiji.ai`

#### Control — Current default short
**Pattern:** `{N} Tourist Scams in {City} (2026) — How to Avoid | tabiji.ai`
**Examples:**
- `6 Tourist Scams in Abu Dhabi (2026) — How to Avoid | tabiji.ai`
- `6 Tourist Scams in Barcelona (2026) — How to Avoid | tabiji.ai`

#### Variant A — Sharpen V3 deliverable
**Pattern:** `Is {City} Safe for Tourists? {N} Scams + Red Flags (2026) | tabiji.ai`
**Hypothesis:** "Scams to Avoid" is generic; "+ Red Flags" promises a *recognition tool* (pattern-matching cues), which is what nervous travelers actually want. Holds the question constant so any delta is attributable to the deliverable change.
**Example:** `Is Singapore Safe for Tourists? 6 Scams + Red Flags (2026) | tabiji.ai`

#### Variant B — Insider voice (POV shift)
**Pattern:** `What Locals Wish Tourists Knew: {N} {City} Scams (2026) | tabiji.ai`
**Hypothesis:** V1's "Locals Want" was a soft positive in round 1; moving the insider hook to the *front* and switching to "wish you knew" (regret framing implies missed insider knowledge) promises privileged information instead of just listing it. Loses "is X safe" intent match — opens a different SEO/social surface.
**Example:** `What Locals Wish Tourists Knew: 6 Vancouver Scams (2026) | tabiji.ai`

#### Variant C — Named-scam concreteness
**Pattern:** `The {Top Scam} & {N-1} More: {City} Tourist Scams (2026) | tabiji.ai`
**Hypothesis:** Concrete named scam in title pulls clicks (specificity > generic count). Also captures long-tail queries for the specific scam name (e.g. "airport taxi scam Sofia") — structural SEO upside no listicle competitor can match without first scraping us.
**Examples:**
- `The Marble Factory Tour & 4 More: Agra Tourist Scams (2026) | tabiji.ai`
- `The QR Parking Scam & 6 More: Austin Tourist Scams (2026) | tabiji.ai`
- `The Tinder Bar Scam & 6 More: Kyiv Tourist Scams (2026) | tabiji.ai`
- `The Free Camel Ride & 5 More: Petra Tourist Scams (2026) | tabiji.ai`

Top scam names hand-picked from each page's first scam-card title (mapping in `scripts/apply_round2_titles.py` via `/tmp/title-rollout/variant_c_scams.json`).

#### Variant D — Pre-trip framing
**Pattern:** `Before You Visit {City}: {N} Tourist Scams to Avoid (2026) | tabiji.ai`
**Hypothesis:** Captures upstream funnel intent (people *planning* to visit) — different from V3's reactive "is X safe" worry-query. Tests whether the planning-intent traffic cluster is meaningful.
**Example:** `Before You Visit Mexico City: 6 Tourist Scams to Avoid (2026) | tabiji.ai`

#### Variant E — Trending / current-state
**Pattern:** `Trending Tourist Scams in {City}: {N} to Watch in 2026 | tabiji.ai`
**Hypothesis:** "Trending" implies the page tracks current/active scams (vs recycled 2018 listicles competitors run) — credibility lever travel-safety publishers can uniquely play.
**Example:** `Trending Tourist Scams in Cairo: 7 to Watch in 2026 | tabiji.ai`

### Cohort assignments

#### V3 (200 cities)
acapulco, addis-ababa, adelaide, agadir, albufeira, almaty, amalfi-coast, amman, amsterdam, anaheim, annecy, antigua-guatemala, arequipa, aruba, arusha, athens, auckland, bangkok, bariloche, batam, battambang, beirut, belgrade, berlin, biarritz, bodrum, bora-bora, brasilia, bratislava, bremen, brighton, bucharest, busan, buzios, cabo-san-lucas, calgary, can-tho, cancun, cannes, cape-town, cascais, castries, charleston, chennai, chiang-mai, colmar, cologne, copenhagen, cozumel, cusco, dahab, dallas, dammam, dhaka, dubai, dublin, dubrovnik, durban, ephesus, essaouira, fethiye, florence, fort-lauderdale, galveston, geneva, ghent, gold-coast, gothenburg, granada-spain, guanajuato, guangzhou, guatape, guatemala-city, ha-long-bay, hamburg, harbin, havana, helsinki, hoi-an, hua-hin, hurghada, ibiza, innsbruck, ipoh, isla-mujeres, istanbul, izmir, jaipur, jasper, johor-bahru, kampala, kathmandu, kingston, koh-phangan, koh-phi-phi, kota-kinabalu, krabi, kusadasi, kyoto, lagos, lagos-portugal, lake-bled, lake-como, lake-district, las-vegas, leipzig, lima, liverpool, lombok, london, luang-prabang, luxor, manchester, manila, manuel-antonio, maputo, mar-del-plata, marseille, maui, melaka, mendoza, merida, merzouga, meteora, minneapolis, monaco, montevideo, muscat, myrtle-beach, napa-valley, naples, nashville, nazare, negril, niagara-falls, ninh-binh, nuremberg, nusa-penida, oslo, ouarzazate, palermo, paphos, paris, pattaya, penang, philadelphia, phnom-penh, phu-quoc, phuket, pingyao, portland, porto, potsdam, puerto-escondido, puerto-iguazu, puerto-vallarta, punta-cana, quepos, rosario, salento, salta, salvador, samarkand, san-cristobal-de-las-casas, san-francisco, san-salvador, san-sebastian, santa-marta, santiago-de-compostela, santo-domingo, sapa, sapporo, sardinia, seattle, shenzhen, siargao, side-turkey, sofia, stockholm, stone-town, stonehenge, suzhou, sydney, taichung, taipei, tamarindo, taormina, tigre, tokyo, tortuguero, toulouse, tulum, tunis, turks-and-caicos, ubud, venice, washington-dc, whistler, whitsundays, windsor

#### Control (200 cities — includes the 17 stragglers force-locked here)
alexandria, antigua, aswan, baden-baden, bali, banff, bangalore, barcelona, beijing, bergen, bilbao, birmingham, bogota, bologna, boracay, branson, brasov, brisbane, bruges, brussels, budapest, buenos-aires, bukhara, cairns, cali, cambridge, cameron-highlands, canberra, cappadocia, capri, carmel, cartagena, casablanca, cebu, cesky-krumlov, chicago, chongqing, coimbra, colombo, cordoba-spain, curacao, da-nang, dakar, dar-es-salaam, darwin, delhi, delphi, doha, dusseldorf, edinburgh, el-calafate, el-chalten, el-nido, faro, foz-do-iguacu, frankfurt, fukuoka, funchal, galle, genting-highlands, gili-islands, goa, gran-canaria, granada-nicaragua, guayaquil, hakone, halifax, hammamet, hanoi, heidelberg, heraklion, hobart, hong-kong, honolulu, houston, hue, hvar, hyderabad, inverness, jeddah, jerusalem, johannesburg, kanazawa, key-west, koh-samui, koh-tao, kolkata, kos, kotor, krakow, kuching, la-fortuna, la-paz, labadee, lake-garda, langkawi, lanzarote, lijiang, lisbon, ljubljana, lofoten, los-angeles, lusaka, lviv, lyon, macau, madrid, maldives, manaus, mandalay, marmaris, mauritius, mecca, memphis, milan, mombasa, montego-bay, monteverde, montpellier, moscow, mount-bromo, mumbai, munich, nafplio, nara, nassau, new-orleans, nha-trang, nikko, oaxaca, ocho-rios, okinawa, orlando, osaka, ottawa, pai, palma-de-mallorca, pamukkale, paros, phoenix, pisa, playa-del-carmen, plovdiv, pokhara, port-douglas, prague, puebla, quebec-city, queenstown, quito, recife, reykjavik, riyadh, rome, rothenburg, san-miguel-de-allende, santa-teresa, santiago, santorini, sao-paulo, sarajevo, savannah, sedona, seminyak, seoul, seychelles, sharm-el-sheikh, siena, sintra, sorrento, split, st-maarten, stratford-upon-avon, suva, takayama, tangier, tayrona, tel-aviv, tenerife, tirana, toledo, toronto, tromso, ushuaia, valencia, valparaiso, varanasi, vienna, vientiane, villa-de-leyva, warsaw, windhoek, xian, yangshuo, yerevan, york, zagreb, zakynthos, zermatt, zurich

#### A (25 cities)
alanya, alice-springs, asheville, bermuda, budva, chengdu, corfu, denver, fussen, hiroshima, jakarta, konya, liberia-costa-rica, lucerne, miami, nairobi, nice, panama-city, roatan, san-diego, siem-reap, singapore, tallinn, verona, yangon

#### B (25 cities)
accra, antalya, avignon, ayutthaya, baku, bridgetown, chefchaouen, dalat, djerba, fortaleza, hangzhou, ho-chi-minh-city, kuala-lumpur, mazatlan, montreal, naxos, pompeii, positano, puerto-viejo-costa-rica, san-andres, tainan, tashkent, vancouver, vilnius, yokohama

#### C (25 cities)
agra, austin, bath, bordeaux, cardiff, cinque-terre, fez, florianopolis, guadalajara, ijen-crater, jaco-costa-rica, kaohsiung, kyiv, marrakech, melbourne, milos, ouro-preto, paraty, petra, salzburg, san-antonio, san-juan, stuttgart, tbilisi, zanzibar

#### D (25 cities)
abu-dhabi, belize-city, byron-bay, chamonix, chiang-rai, fiji, gatlinburg, grand-cayman, guilin, holbox, jeju, kandy, labuan-bajo, medina, mexico-city, mykonos, new-york-city, rabat, riga, rishikesh, san-jose-costa-rica, st-tropez, strasbourg, victoria-bc, zhangjiajie

#### E (25 cities)
atlanta, belfast, boston, cairo, chania, cordoba-argentina, dresden, glasgow, interlaken, kigali, kunming, malaga, medellin, mont-saint-michel, oxford, perth, rhodes, rio-de-janeiro, seville, shanghai, st-louis, st-petersburg, thessaloniki, udaipur, yogyakarta

### Title length sanity

Stratified-snake assignment + variant-specific patterns produced 22 of 525 titles >60 chars pre-brand-suffix (mostly cities with long compound names: Castries St. Lucia, Mont-Saint-Michel, Rothenburg ob der Tauber, Ho Chi Minh City, etc.). These will likely be truncated on mobile SERPs but the truncation is consistent across arms, so it does not bias the comparison.

### Measurement plan

1. **Wait 3–14 days** for Google to recrawl and reindex titles. Spot-check via `site:tabiji.ai/scams/` queries.
2. **Run for ≥21 days** post-reindex to accumulate enough impressions per arm. Variant arms (n=25) need more time per-arm than V3/Control to see signal.
3. **Pull a fresh GSC Pages export** ~2 weeks from rollout (target: 2026-05-22) and again at 4 weeks for confirmation.
4. **Compute per-arm CTR delta vs baseline + V3 vs Control head-to-head.** Use round-1 baselines for cities that participated; use 28-day pre-rollout window for fresh cities.
5. **Decision rules:**
   - V3 vs Control: if V3 still beats Control by ≥0.3pp aggregate CTR with no position regression → confirm V3 as the new permanent default for the 17 stragglers (now folded into Control) and any future scam pages.
   - Variant arms: a variant beating V3 by ≥0.5pp on ≥20 pages with positive deltas → roll out as round-3 expansion (replicate to ~100 pages for confirmation).
   - A clearly losing variant (≤−0.3pp on ≥20 pages) → eliminate from further testing.

### Risks / confounds

- **PR #1458 contamination:** see round-1 results section. Round 2 is uncontaminated.
- **Position drift:** Google may re-rank after title change. Report position alongside CTR; flag any arm shifting >0.5 weighted position.
- **Title length truncation:** consistent across arms; doesn't bias comparison.
- **Title rewriting by Google:** Google sometimes rewrites titles in SERPs. Spot-check a sample per arm during the test.
- **Variant arm sample size:** n=25 with ~6 cities having GSC data per arm is small. Single-page outliers (à la Kathmandu in round 1) can dominate aggregate signal — interpret cautiously.
- **Post-rollout newly-added scam cities:** any new /scams/ city created between now and the next pull will use round-2 templates depending on which generator script handles them. Worth confirming the generator picks Control/V3 by default rather than the deprecated long template (the 13 stragglers from before were created that way).

### Round 2 review checklist (target: 2026-05-22)

- [ ] Pull fresh GSC Pages export
- [ ] Compute per-arm CTR delta vs baseline
- [ ] V3 vs Control head-to-head: which wins, by how much
- [ ] Per-variant deltas: identify candidates for round 3
- [ ] Append round-2 results section to this doc
- [ ] Decide rollout scope based on decision rules above

### Rollout artifacts

- Script: [scripts/apply_round2_titles.py](../scripts/apply_round2_titles.py)
- Cohort assignments and Variant C scam-name picks captured in commit message; can be regenerated from the script if needed.
