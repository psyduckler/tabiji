# Barcelona Travel Keyword Research — 2026-04-08

**Source:** Semrush API (`phrase_fullsearch`), US database, 161 compound seed phrases across 15 travel categories.
**Raw:** 44,537 keywords pulled → **43,524 cleaned** after filtering FC Barcelona football, US Barcelona Wine Bar chain, and Venezuela namesake noise.
**Total monthly search volume captured:** ~2.4M (US database).

Files:
- `scripts/semrush_barcelona_research.py` — pull script
- `scripts/refilter_barcelona.py` — noise filter + categorizer
- `scripts/barcelona-research/clean_keywords.csv` — full dataset (43,524 rows)
- `scripts/barcelona-research/clean_keywords.json` — same, JSON
- `scripts/barcelona-research/clean_summary.json` — bucket + category rollups

---

## 1. Volume Buckets

| Bucket | Range (monthly US searches) | Keywords | Total Volume | Notes |
|---|---|---|---|---|
| **Head** | 10,000+ | 6 | 134,800 | Brand-level "barcelona X" terms |
| **High** | 5,000–10,000 | 26 | 193,500 | Top-of-funnel discovery |
| **Mid** | 1,000–5,000 | 355 | 600,200 | Best ROI sweet spot |
| **Low** | 500–1,000 | 396 | 281,600 | Long-tail with intent |
| **Long-tail** | 100–500 | 2,984 | 653,680 | Programmatic SEO play |
| **Tail** | <100 | 39,743 | 548,130 | Aggregate-only value |

**Key insight:** the long-tail bucket (100–500) holds **more total volume than head + high + mid + low combined** in the 1k+ range. Programmatic templates (per-month weather, per-route trains, per-neighborhood guides, per-attraction tickets) capture this.

---

## 2. Category Leaderboard (sorted by total volume)

| # | Category | Keywords | Total Vol | Avg CPC | Comment |
|---|---|---|---|---|---|
| 1 | **Lodging — Hotels** | 5,437 | 548,890 | $0.58 | Dominant. Brand hotel queries (Nobu, Hotel Arts, 1898, Cotton House) drive most. |
| 2 | **Transport — Intercity** | 1,844 | 235,120 | $0.37 | Madrid↔Barcelona is enormous. Paris, Valencia, Seville also strong. |
| 3 | **Practical — Weather** | 519 | 216,990 | $0.03 | Per-month long-tail goldmine ("weather barcelona november/may/october…"). |
| 4 | **Sights — Attractions** | 2,294 | 156,500 | $0.17 | "Things to do in Barcelona" is the #2 head term overall (18,100). |
| 5 | **Food — Restaurants** | 1,859 | 122,260 | $0.07 | "Barcelona restaurant" 9,900 + "best restaurants in barcelona" 4,400. |
| 6 | **Transport — Airport** | 1,879 | 97,430 | $0.23 | "Barcelona airport" 18,100, plus airport code, BCN, El Prat queries. |
| 7 | **Lodging — Apartments / Rentals** | 2,132 | 82,820 | $0.62 | Vacation rentals (4,400) + Airbnb + car rental confused in here. |
| 8 | **Sights — Sagrada Familia** | 117 | 73,620 | $0.90 | Highest CPC in the dataset. Tickets keyword cluster pays. |
| 9 | **Transport — Local** | 2,061 | 72,820 | $0.10 | Metro, Uber, hop-on-hop-off bus. |
| 10 | **Drinks — Nightlife / Clubs** | 1,651 | 59,610 | $0.06 | Opium, Pacha, Razzmatazz brand-led. |
| 11 | **Planning — General** | 1,978 | 58,410 | $0.30 | "Barcelona vacation/tourism/travel" generic intent. |
| 12 | **Sights — Tours** | 1,480 | 55,640 | $0.65 | Day trips (Montserrat) + walking tours. **High CPC** = affiliate-friendly. |
| 13 | **Sights — Beaches** | 356 | 54,150 | $0.15 | "Best beaches near Barcelona" 8,100 alone. |
| 14 | **Drinks — Bars** | 1,810 | 49,020 | $0.05 | Per-bar branded queries (Bar Cañete, Bar Mut, Bar Brutal). |
| 15 | **Lodging — Hostels** | 677 | 48,560 | $0.72 | Generator, Yeah, Kabul, Casa Gracia branded. |
| 16 | **Food — Tapas / Paella** | 1,129 | 46,330 | $0.13 | Iconic dish, evergreen. |
| 17 | **Shopping** | 778 | 39,930 | $0.19 | "Barcelona shop" 3,600 + Christmas market. |
| 18 | **Sights — Gaudí (Park Güell, Casa Batlló, etc.)** | 289 | 35,840 | $0.46 | Tickets terms convert. |
| 19 | **Sights — Museums** | 410 | 32,620 | $0.51 | Picasso, Dalí, Moco, Banksy. |
| 20 | **Lodging — Neighborhoods** | 1,025 | 31,230 | $0.28 | "Where to stay in Barcelona" 4,400. |
| 21 | **Sights — Gothic Quarter** | 281 | 22,870 | $0.31 | "Gothic quarter barcelona" 9,900 — concentrated head term. |
| 22 | **Transport — Cruise** | 299 | 22,350 | $0.56 | Cruise port queries; cruise affiliate angle. |
| 23 | **Food — Specific Meal (brunch/breakfast/dinner)** | 1,445 | 21,530 | $0.06 | Brunch & Cake brand dominates. |
| 24 | **Food — Markets / Tours (Boqueria)** | 733 | 19,670 | $0.19 | La Boqueria 1,900 + market variants. |
| 25 | **Food — Cafes / Coffee** | 1,164 | 19,660 | $0.02 | Fragmented; no single head term. |
| 26 | **Sights — Parks (Tibidabo, Montjuïc)** | 216 | 19,630 | $0.28 | Beyond Park Güell. |
| 27 | **Sights — Picasso Museum** | 62 | 15,630 | $0.45 | "Picasso museum barcelona" 8,100 = single concentrated cluster. |
| 28 | **Practical — Language** | 477 | 14,420 | $0.24 | "What language is spoken in Barcelona" cluster. |
| 29 | **Itinerary** | 943 | 13,590 | $0.19 | 1/2/3/4/5/7-day templates — programmatic play. |
| 30 | **Safety** | 826 | 13,220 | $0.02 | "Is Barcelona safe" 1,900 — low CPC, high informational value. |
| 31 | **Health / Insurance** | 1,077 | 12,380 | $0.03 | Mostly hospital lookups, not insurance intent. |
| 32 | **Food — Michelin** | 494 | 11,930 | $0.06 | Concentrated, decent CPC. |
| 33 | **Practical — Money / Cost** | 350 | 9,720 | $0.01 | Currency + cost of living. |
| 34 | **Food — Bakery / Dessert** | 876 | 8,960 | $0.05 | Royals Mollete, Praktik, chocolate museum. |
| 35 | **Remote Living / Digital Nomad** | 681 | 6,340 | $0.09 | Smaller than expected. Coworking has the volume. |
| 36 | **Food — Dietary (Vegan/Vegetarian/GF)** | 337 | 4,710 | $0.02 | Niche but evergreen. |
| 37 | **Visa / Entry** | 375 | 2,030 | $0.05 | Surprisingly small for Barcelona-specific; Spain-level dwarfs it. |
| 38 | **Practical — Misc (dress code, adapter)** | 227 | 1,890 | $0.01 | "Opium dress code" cluster is biggest. |
| 39 | **Practical — Connectivity (SIM, eSIM, wifi)** | 277 | 1,080 | $0.12 | Tiny but high-intent. |
| 40 | **Drinks — Sangria / Cava / Vermouth** | 132 | 1,070 | $0.06 | Niche. |

---

## 3. Top Head Terms (10k+/month)

| Volume | Keyword | Category | CPC |
|---|---|---|---|
| 27,100 | barcelona hotels | lodging | $1.63 |
| 27,100 | barcelona weather | weather | $0.01 |
| 22,200 | hotels in barcelona | lodging | $1.65 |
| 22,200 | barcelona church sagrada de familia | sagrada | $1.79 |
| 18,100 | barcelona airport | airport | $1.41 |
| 18,100 | things to do in barcelona | attractions | $0.38 |

## 4. High Tier (5k–10k)

| Volume | Keyword | Category |
|---|---|---|
| 9,900 | barcelona restaurant | food |
| 9,900 | hotel barcelona | lodging |
| 9,900 | nobu hotel barcelona | lodging |
| 9,900 | things to do in barcelona spain | sights |
| 9,900 | basilica de sagrada familia barcelona | sagrada |
| 9,900 | sagrada familia barcelona | sagrada |
| 9,900 | gothic quarter barcelona | gothic |
| 8,100 | madrid to barcelona train | intercity |
| 8,100 | madrid to barcelona | intercity |
| 8,100 | picasso museum barcelona | museums |
| 8,100 | best beaches near barcelona | beaches |
| 6,600 | hotel arts barcelona | lodging |
| 6,600 | hotel colon barcelona | lodging |
| 6,600 | hotels in barcelona spain | lodging |
| 6,600 | barcelona to madrid train | intercity |
| 6,600 | barcelona to madrid | intercity |
| 6,600 | barcelona beaches | beaches |
| 6,600 | weather barcelona | weather |
| 6,600 | weather in barcelona | weather |
| 5,400 | best hotels in barcelona | lodging |
| 5,400 | hotels barcelona | lodging |
| 5,400 | barcelona spain weather | weather |
| 5,400 | barcelona beach | beaches |
| 5,400 | train from barcelona to madrid | intercity |
| 5,400 | train from madrid to barcelona | intercity |

---

## 5. Strategic Buckets — Where to Build

These are grouped not by volume but by **content opportunity** for tabiji.ai.

### Tier S — Programmatic SEO goldmines (build templates, fill the long-tail)

These categories have a head term + a massive long-tail of permutations that scale through templates:

1. **Per-month weather pages** — `barcelona weather [month]`. Head: 27,100. Long-tail: every month variant (january–december, plus "this month", "by month", "in [month] spain"). One template, 12+ canonical pages, captures ~217k volume.
2. **Per-route train/transport pages** — `barcelona to [city] train`, `[city] to barcelona`. Madrid alone is 32k combined; Paris, Valencia, Seville, Marseille, Lyon, Zaragoza all have 1k+. ~235k aggregate.
3. **Per-attraction ticket pages** — Sagrada Familia, Park Güell, Casa Batlló, Casa Milà, Picasso Museum, Camp Nou (stadium tour, not football news). High CPC ($0.45–$0.90), strong affiliate margins via GetYourGuide/Tiqets.
4. **Per-day-count itineraries** — `barcelona [N] days` and `[N] days in barcelona` for N=1,2,3,4,5,7. ~13k aggregated.
5. **Per-neighborhood guides** — Born, Gothic, Eixample, Gracia, Barceloneta, Raval, Poble Sec. "Where to stay in barcelona" 4,400 head. Attach hotel/Airbnb affiliate widgets.

### Tier A — High-volume, high-intent verticals (single hub pages can rank)

1. **Sagrada Familia hub** — 73k vol concentrated in <120 keywords. One excellent guide page + tickets affiliate.
2. **Things to Do in Barcelona** — 18k head term, 156k category total. Classic editorial hub.
3. **Barcelona Hotels hub + neighborhood subhubs** — 549k category vol. Heaviest commercial intent in the dataset.
4. **Barcelona Airport (BCN/El Prat) guide** — 97k category vol, transfer + accommodation upsells.
5. **Best Beaches near Barcelona** — 54k category vol, 8,100 head term, ties to day-trip content.
6. **Best Restaurants in Barcelona** — 122k category vol; combine with tapas (46k) for a dining cluster.

### Tier B — Mid-volume but underserved or unique

1. **Day trips from Barcelona** — 3,600 head, $0.65 CPC, Montserrat/Costa Brava/Sitges subtopics. Tour affiliate-friendly.
2. **Picasso Museum** — 15,630 vol in 62 keywords (very concentrated, easy win).
3. **Gothic Quarter walking tour cluster** — 22,870 vol, 281 kws, includes "bars in gothic quarter" cross-sell.
4. **Boqueria / food market / food tour** — 19,670 vol with strong affiliate angle (Devour Tours etc.).
5. **Michelin Barcelona guide** — 11,930 vol, niche but high LTV reader.
6. **Brunch in Barcelona** — Brunch & Cake brand drives ~3k by itself; round it out with a "best brunch" hub.

### Tier C — High-intent but low-volume informational (capture for E-E-A-T + brand)

1. **Is Barcelona safe / scams / pickpockets** — 13k category total, $0.02 CPC. Builds trust signal; readers convert downstream.
2. **Barcelona digital nomad / coworking / cost of living** — 6,340 vol; small but a high-LTV audience aligned with insurance/eSIM affiliate.
3. **Barcelona language (Catalan vs. Spanish)** — 14,420 vol. One canonical FAQ page captures the cluster.
4. **Currency / tipping / cost** — 9,720 vol; one practical guide.

### Tier D — Niche but worth a single FAQ entry

- Visa / Schengen (Barcelona-specific is only 2k; route to Spain-level page)
- SIM card / eSIM (1,080 vol but very high-intent — eSIM affiliate)
- Power adapter / dress code (cover in a "first-time visitor" practical hub)
- Sangria / cava / vermouth (cocktail FAQ rounds out the bar content)

---

## 6. Notable Gaps & Surprises

- **Visa/insurance volumes are tiny at city level.** Searchers ask "spain visa" and "spain travel insurance" — Barcelona-specific volume is negligible. If you want this audience, build at the **Spain country level** and link from the city hub.
- **"Camp Nou" was filtered out** because >90% of its volume is football fixtures, not stadium tours. To recover the legitimate stadium-tour traffic, query `camp nou tour` / `camp nou tickets` directly in a follow-up pass.
- **Hotels dominate by 2.3x the next category.** The lodging vertical is by far the most monetizable.
- **Weather is an outlier.** $0.01 CPC means low ad value, but it's the #2 traffic driver — ideal as a top-of-funnel "discovery" page that pipes readers into hotel/itinerary content.
- **Gothic Quarter is over-concentrated** in two head terms (9,900 + 3,600). The 281-keyword long-tail is small; a single excellent page captures the cluster.
- **"Disfrutar" (3-Michelin-star) keywords leaked through** as `dis fru tar restaurant barcelona` (1,900 vol) — Semrush is mis-tokenizing the name. Worth a manual entry in any restaurant content.
- **Per-month weather is the single best programmatic play.** Each month variant (november, may, october, december) shows independent 1,300–2,400 volumes — 12× pages from one template.
- **Brand-name hotel queries are huge** (Nobu, Arts, Colon, 1898, Mandarin, Cotton House, Renaissance — each 2,900–9,900). Booking-affiliate review pages per hotel are easy to scale.

---

## 7. Methodology & Caveats

- **Database:** US (`database=us`). Volumes reflect US-based searchers — UK/EU/AU databases would shift the picture significantly (especially toward "barcelona holidays" UK terminology).
- **Method:** `phrase_fullsearch` with 161 compound seed phrases (`barcelona restaurants`, `barcelona hotels`, etc.), 500-result cap per seed, then dedupe by keyword.
- **Filtering:** dropped FC Barcelona football noise (Spanish-language fixtures, "alineaciones", "estadísticas", "club brujas", player names), US Barcelona Wine Bar chain locations (Stamford, Brookline, Boston, Tampa, etc.), and Barcelona, Venezuela queries.
- **Categorization:** rule-based regex match (first match wins). ~5.7% of keywords land in `other` — mostly typos, mixed-language, and edge cases.
- **What's missing:** I did not pull `phrase_questions` (PAA-style queries), `phrase_kdi` (keyword difficulty), or SERP feature data. Those would refine the Tier-A picks but the volume picture is solid.
- **Re-running:** edit `SEEDS` in `scripts/semrush_barcelona_research.py`, run it (~1 min), then `scripts/refilter_barcelona.py`. The re-filter is fast and doesn't burn API credits.
