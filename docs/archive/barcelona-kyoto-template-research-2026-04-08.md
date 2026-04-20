# Barcelona × Kyoto — Cross-City Templating Research — 2026-04-08

**Goal:** Use two structurally different cities (a Western European hub and an Asian cultural capital) as a 2-point sample to identify which travel-keyword patterns are **templatizable across destinations** versus which are **city-specific**.

**Data sources:**
- `scripts/barcelona-research/clean_keywords.json` — 43,510 keywords, 2.41M aggregate vol
- `scripts/kyoto-research/clean_keywords.json` — 29,714 keywords, 1.72M aggregate vol
- `scripts/cross-ref-templates.json` — pattern-normalized cross-reference (raw)
- `scripts/cross-ref-templates-modifiers.json` — modifier-cluster cross-reference (deeper)

---

## 1. Side-by-side scale

| Bucket | BCN kws | BCN vol | KYO kws | KYO vol |
|---|---:|---:|---:|---:|
| Head (10k+) | 6 | 134,800 | **11** | **183,500** |
| High (5k–10k) | 26 | 193,500 | **39** | **277,800** |
| Mid (1k–5k) | 355 | 600,200 | 220 | 411,700 |
| Low (500–1k) | 396 | 281,600 | 210 | 149,050 |
| Long-tail (100–500) | 2,984 | 653,680 | 1,623 | 348,560 |
| Tail (<100) | 39,743 | 548,130 | 27,611 | 344,520 |
| **TOTAL** | **43,510** | **2,411,910** | **29,714** | **1,715,130** |

**Observation:** Kyoto is *less broad* (30k vs 44k unique keywords) but *more concentrated at the head* (11 head terms vs 6, and 39 high-tier vs 26). Western searchers express Kyoto interest through a smaller set of canonical phrases — the famous landmarks, ryokan, and shinkansen dominate. Barcelona's interest is spread across hundreds of named hotels, neighborhoods, and long-tail variants.

This is the first signal of **what templatizes:** the structures both cities share (transport routes, itineraries, day trips) are universal. The structures one city has and the other doesn't (Sagrada Familia vs. Fushimi Inari, paella vs. ramen) are city-specific landmark plays.

---

## 2. Pattern symmetry — what shows up in BOTH

I normalized every keyword in both datasets by replacing the city name with `[CITY]`, then matched identical patterns. Of the resulting patterns:

- BCN had **41,313** unique normalized patterns
- KYO had **25,320** unique normalized patterns
- **2,341** patterns appear in BOTH cities
- **384** of those have ≥50 monthly volume in **each** city (the templatizable set)

Symmetry score = `min(BCN_vol, KYO_vol) / max(BCN_vol, KYO_vol)`. A score of 1.0 means the pattern is equally important to both cities; 0.0 means it's effectively one-sided.

---

## 3. Tier 1 — Universal templates (high symmetry, build for every city)

These patterns have meaningful volume and high symmetry across both cities. Build a templated content type once, populate per destination, scale across the catalog.

| Template | BCN vol | KYO vol | Symmetry | Combined | Notes |
|---|---:|---:|---:|---:|---|
| **`[city] to [other city] train`** (transit routes) | 104,410 | 63,830 | 0.61 | **168,240** | The single biggest universal template. Madrid↔Barcelona = 32k; Tokyo↔Kyoto = 25k. Build a per-route page generator. |
| **`day trips from [city]`** | 21,830 | 11,860 | 0.54 | **33,690** | Universal. Each city needs a "day trips from" hub + per-destination sub-pages. |
| **`[city] [N] days itinerary`** (1, 2, 3, 4, 5, 7, 10, 14) | 18,920 | 6,560 | varies | **25,480** | All N-day variants exist in both cities. Strongest: 3-day (5,240+1,620), 2-day (3,480+1,190), 10-day (4,270+1,140). |
| **`walking tour [city]`** | 8,350 | 2,690 | 0.32 | 11,040 | Self-guided + guided variants. Affiliate-friendly. |
| **`vegan/vegetarian [city]`** | 5,400 | 2,730 | 0.51 | 8,130 | Audience template — fragmented but consistent. |
| **`[city] flea market / vintage / antique`** | 2,390 | 2,320 | **0.97** | 4,710 | **Highest symmetry of any pattern.** Almost identical volume in both cities. Universal underserved niche. |
| **`food tour [city]`** | 4,550 | 1,050 | 0.23 | 5,600 | High commercial intent — Devour, Secret Food Tours, Magical Trip affiliates. |
| **`[city] cooking class`** | 1,020 | 850 | **0.83** | 1,870 | Very symmetric. Paella in BCN, kaiseki/sushi in KYO — same template, different cuisine slot. |
| **`private tour / private guide [city]`** | 1,850 | 620 | 0.34 | 2,470 | Premium affiliate. |
| **`[city] luggage storage`** | 580 | 420 | **0.72** | 1,000 | Tiny volume but **high symmetry, ultra-high intent**. Bounce/Stasher affiliate. Build once, deploy everywhere. |
| **`romantic / couples / honeymoon [city]`** | 1,110 | 410 | 0.37 | 1,520 | Audience template. |
| **`[city] itinerary 1 day`** | 440 | 820 | 0.54 | 1,260 | Kyoto actually leads here — day-trippers from Osaka/Tokyo. |

**Tier 1 takeaway:** there are ~12 truly universal patterns that justify building shared templates and populating per-city. The strongest is `[city]-to-[city] train` — Madrid↔Barcelona alone is 32k/month, Tokyo↔Kyoto is 25k/month, and the same structure works for any country with intercity rail.

---

## 4. Tier 2 — Templatizable but destination-type-specific

These patterns are strong in **one city type** and weak/absent in the other. They templatize within a destination class (Western European city, Asian cultural capital, beach destination, etc.) but not universally.

### 2a. Western/European destination patterns (Barcelona-heavy, Kyoto-light)

| Template | BCN vol | KYO vol | Why the asymmetry |
|---|---:|---:|---|
| **`[city] weather [month]`** (12 monthly variants) | 90,000+ | ~8,000 | **Asian destinations don't search "weather in [month]" — they search "cherry blossom" / "autumn leaves" instead.** Build per-month weather pages for European/American cities; build seasonal pages for Asian ones. |
| **`is [city] safe`** | 7,520 | 240 | Kyoto is famously safe, so the question isn't asked. Build safety hubs only for cities with active safety reputations (Barcelona, Naples, Marseille, Mexico City, etc.). |
| **`[city] currency / tipping / cost`** | 9,590 | 750 | Searchers know Japan uses yen and doesn't tip. Build money-and-tipping pages for destinations where these conventions are unfamiliar (most of Europe, Latin America, parts of Asia). |
| **`what language do they speak in [city]`** | 14,720 | 320 | Catalan vs. Spanish confusion drives BCN volume. Japan is monolingual so the question doesn't exist. Build for cities with linguistic ambiguity (Barcelona, Brussels, Geneva, Hong Kong, Montreal). |
| **`[city] gay / LGBTQ`** | 5,930 | 680 | BCN has Eixample/Sitges as recognized gay destinations; Kyoto doesn't have an equivalent reputation. Build LGBTQ hubs only for cities with established gay scenes. |
| **`[city] solo female travel`** | 920 | 60 | Higher search intent for cities perceived as risky for solo women. |
| **`[city] with kids / family`** | 6,440 | 970 | Barcelona is positioned as a family destination; Kyoto less so. Both worth building, but BCN has 6× the demand. |

### 2b. Japan/Asian destination patterns (Kyoto-heavy, Barcelona-light)

| Template | BCN vol | KYO vol | Why the asymmetry |
|---|---:|---:|---|
| **`[city] cherry blossom / sakura / autumn leaves / koyo`** | ~0 | 15,310 | Pure seasonal Japan template. Use for Japan + Korea + parts of China cities. |
| **`[city] ryokan / machiya / traditional accommodation`** | ~0 | 59,330 | Japan-only lodging type. Templatizable across Japanese cities (Tokyo, Kyoto, Osaka, Hakone). |
| **`[city] tea ceremony / kimono experience / cultural class`** | 1,150 | 16,330 | Japan-cultural template. Could extend to Vietnam (ao dai), Korea (hanbok), Bali (batik). |
| **`[city] temple / shrine / shojin ryori`** | 41,640 (Sagrada) | 69,500 (other temples) | BCN has Sagrada Familia as one cathedral; Kyoto has dozens. Asian cultural cities need a "temples + shrines" template; European cities need a "cathedrals + churches" variant. |
| **`[city] kaiseki / sushi / ramen / matcha`** | n/a | 99,210 | Japan-specific dish templates. Each cuisine type is its own template — paella for Spain, pho for Vietnam, dim sum for Hong Kong, etc. |

### 2c. Insight — destination archetypes

Cross-referencing Tier 2 reveals at least **four destination archetypes** where different sub-templates dominate:

1. **Western European city** (Barcelona, Rome, Paris, Lisbon, Amsterdam): heavy on weather-by-month, currency, safety, language confusion, named cathedral/museum, bars/nightlife, tapas-equivalent food.
2. **Asian cultural capital** (Kyoto, Hanoi, Luang Prabang, Chiang Mai): heavy on temples/shrines, traditional accommodation, seasonal beauty (sakura/koyo), cultural classes, signature cuisine.
3. **Beach destination** (Cancún, Bali, Phuket): would likely heavy-skew toward beach clubs, day trips to islands, water sports, all-inclusive resorts.
4. **Mega-metro** (Tokyo, NYC, London): would skew toward neighborhood guides, metro maps, multi-day itineraries, district-level food scenes.

To validate the archetype model you'd want a third sample point from each archetype before locking templates.

---

## 5. Tier 3 — Named-landmark hubs (city-specific, not templatable, but the *meta-pattern* is)

Each city has a small handful of named landmarks that pull 5k–100k+ vol on their own. The landmarks themselves don't templatize (Sagrada Familia ≠ Fushimi Inari), but the **structure** does: every city has 5–10 named landmarks worth dedicated hub pages.

### Barcelona named landmarks
| Landmark | Keywords | Vol |
|---|---:|---:|
| Sagrada Familia | 117 | 73,620 |
| Beaches (Barceloneta + day trips) | 356 | 54,150 |
| Park Güell + Gaudí buildings | 289 | 35,840 |
| Gothic Quarter | 281 | 22,870 |
| Parks (Tibidabo, Montjuïc) | 216 | 19,630 |
| Picasso Museum | 62 | 15,630 |

### Kyoto named landmarks
| Landmark | Keywords | Vol |
|---|---:|---:|
| Arashiyama (bamboo grove + monkey park) | 1,192 | 156,370 |
| Fushimi Inari Taisha | 813 | 95,570 |
| Kinkaku-ji (Golden Pavilion) | 835 | 93,810 |
| Kiyomizu-dera | 668 | 76,410 |
| Nijō Castle / Imperial Palace | 810 | 50,010 |
| Gion / Geisha district | 921 | 37,370 |
| Tenryū-ji (Arashiyama) | 89 | 14,510 |
| Ginkaku-ji (Silver Pavilion) | 125 | 13,260 |
| Higashiyama district | 86 | 6,560 |
| Ryōan-ji | 110 | 5,460 |

**Templatable meta-pattern:** every city in your catalog should have a "**top 5–10 named landmarks**" hub + per-landmark sub-pages with:
- History / why it's famous
- How to get there (with transit cluster)
- Tickets affiliate (highest CPC of any travel content — see Sagrada Familia at $0.90 CPC)
- Best time of day / crowd-avoidance tips
- Nearby food + things to do

The landmarks change per city; the page structure does not. This is a **template at the page-structure level**, not at the keyword level.

---

## 6. Long-tail templating — the highest-leverage moves

Ranked by which templates have the **best ratio of (combined volume) × (symmetry) × (commercial intent)**:

### Build first

1. **Per-route train pages (`[city] to [city] train`)**
   - Combined volume across just these two cities: **168k**
   - Pattern: one page per origin-destination pair (24 pages from 5 hub cities × 5 destinations each)
   - Estimated total volume across 30 European + 20 Asian cities: 1M+ monthly
   - Affiliate angle: Trainline, Omio, Klook (Asian rail)

2. **Per-day-count itinerary template (`[city] in N days`, 1/2/3/4/5/7/10/14)**
   - Combined volume: **25k+** for just two cities
   - Pattern: 8 day-count variants × N cities = scalable
   - High commercial intent — itinerary readers book hotels, tours, transit
   - Build the 3-day variant first (highest volume in both cities)

3. **Day-trips-from-[city] hubs + sub-pages**
   - Combined volume: **34k**
   - Pattern: parent hub + 4–6 destination sub-pages per city (Montserrat, Sitges, Girona for BCN; Nara, Osaka, Hakone for KYO)
   - Each sub-page captures its own train-route long-tail

4. **Luggage storage pages**
   - Combined volume: only **1k** but **0.72 symmetry**, very high commercial intent
   - One page per city, very thin content, Bounce/Stasher affiliate
   - This is the easiest template to ship — likely <1 hour per city

5. **Cooking class hub per city (paella/kaiseki/pho/pizza/etc.)**
   - Combined volume: **1.9k** at 0.83 symmetry
   - GetYourGuide / Cookly affiliate
   - Slot the signature dish per destination

6. **Named-landmark hub template (5–10 per city)**
   - Combined volume across just BCN+KYO landmarks: **543k**
   - Highest CPC content in the dataset
   - Page structure templatizes; content fills per-landmark

### Build second (audience overlays)

7. **Vegan/vegetarian [city]** — 8k combined, 0.51 symmetry, builds an audience
8. **[city] with kids / family** — 7k combined (BCN-skewed but universal-ish)
9. **[city] flea market / vintage / antique** — 4.7k combined, 0.97 symmetry — almost no competition

### Build third (destination-archetype overlays)

10. **Per-month weather** — for European/American cities only (one template, 12 pages × N cities)
11. **Cherry-blossom / autumn-leaves seasonal** — for Japanese/Asian cities only (4 seasonal variants)
12. **Currency + tipping** — for cities with unfamiliar conventions
13. **Is [city] safe** — for cities with active safety reputations
14. **LGBTQ guide** — for cities with established gay scenes
15. **Ryokan / traditional accommodation** — for Japan only

---

## 7. False templates — patterns that LOOK universal but aren't

Worth flagging so you don't waste effort:

| Apparent template | Reality |
|---|---|
| **`best restaurants [city]`** | BCN has 16k vol, KYO only 2k. The "best restaurants" search pattern is heavy in Western cities where readers feel they need curation; in Japan, readers default to Tabelog/Google ratings or named-cuisine searches (kaiseki, ramen). Build cuisine-specific lists, not generic "best restaurants." |
| **`best hotels [city]`** | Same: 16k BCN vs 2.5k KYO. Western travelers compare hotel brands; Japan travelers search "ryokan" + property names. |
| **`where to stay [city]`** | BCN 11k vs KYO 1.3k. Neighborhood-comparison content matters most in cities with sharply distinct districts. Kyoto travelers default to "ryokan in Gion." |
| **`is [city] safe`** | Only viable for cities with active safety reputations. |
| **`[city] vacation rentals / airbnb`** | Asymmetric — depends on regulatory environment (BCN heavily regulates STRs, Kyoto less so but the search habit differs). |
| **`hidden gems [city]`** | Saturated in both cities by competitor blog content; low ROI everywhere. |

---

## 8. Sample size caveat

This is a **2-point sample**. Two cities tell you which patterns are *plausibly* universal, not which are *definitively* universal. To lock the templating strategy you'd want to add:

- **One more Western European city** (Lisbon or Rome) — to confirm the Tier 2a archetype
- **One more Asian cultural city** (Hanoi or Chiang Mai) — to confirm Tier 2b
- **One beach destination** (Bali or Cancún) — to start defining the beach archetype
- **One mega-metro** (Tokyo or NYC) — to start defining the metro archetype

Each additional city is ~$0 in API credits (the existing scripts cost ~$2 per city in Semrush units) and ~10 minutes of run time. The script structure in `scripts/semrush_*_research.py` is the template — clone, swap seeds + noise filters, run.

---

## 9. Concrete next-step recommendation

If you want one action item from this report: **build the train-route page template first.**

- It's the highest-volume universal pattern (168k just from BCN + KYO; likely 1M+ across the catalog)
- The page structure is simple: route info + booking widget + duration + price + scenic notes + nearby pages
- Trainline, Omio, and Klook affiliates pay well
- Each page captures both directions (`A to B` and `B to A`) — 2 keywords per page
- 30 European cities × 8 routes each = 240 pages = ~600k aggregate vol

Second action item: **the named-landmark hub template** — page structure standardized, content filled per landmark. Highest CPC content in the entire dataset ($0.90 for Sagrada Familia tickets cluster).

---

## 10. Files

- `scripts/semrush_barcelona_research.py` — Barcelona pull (161 seeds)
- `scripts/semrush_kyoto_research.py` — Kyoto pull (236 seeds)
- `scripts/refilter_barcelona.py` — Barcelona filter + categorizer
- `scripts/refilter_kyoto.py` — Kyoto filter + categorizer
- `scripts/cross_reference_cities.py` — pattern normalization + cross-ref
- `scripts/cross-ref-templates.json` — top 200 normalized patterns
- `scripts/cross-ref-templates-modifiers.json` — modifier-cluster comparison
- `scripts/barcelona-research/clean_keywords.csv|json|summary.json`
- `scripts/kyoto-research/clean_keywords.csv|json|summary.json`
- `docs/barcelona-keyword-research-2026-04-08.md` — original Barcelona deep-dive
- `docs/barcelona-kyoto-template-research-2026-04-08.md` — this report
