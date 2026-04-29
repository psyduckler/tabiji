# Scam Atlas Pages — Implementation Plan

**Status:** Draft, pending decisions
**Author:** Bernard Huang (with Claude)
**Date:** 2026-04-29
**Last revised:** 2026-04-29 (consolidation pass — dropped types/playbook split, unified under `/scams/atlas/`; added navigation & cross-link architecture)
**Related surfaces:** `/scams/`, `/books/`, `/api/v1/scams/`

A new page-type system that introduces ~80–100 SEO/AEO atlas entries (plus ~150 selective country cross-cuts) funneling to the 22 Travel Safety Series Kindle books, built off the existing 2,836-scam inventory.

---

## 1. What we found that shaped the plan

The infrastructure already supports this — the data layer exists, only the surfaces and taxonomy are missing.

1. **`/api/v1/scams/{slug}.json`** — 446 per-city files, **2,836 scams already indexed** with structured fields: `id, name, category, severity, frequency, description, avoidance, location, tags[], sources[], tldr`.
2. **60 categories already tagged on scams** but messy — `tourist-trap` (1,481 entries) is a useless catch-all; long tail of typo'd duplicates (`rental_scam` vs `rental-fraud`, `taxi_scam` vs `taxi`).
3. **955 tags** but most are city/country names polluting the tag space, not type taxonomy.
4. **Build patterns to copy:** `generators/popular-picks/` (extract → build → render → validate → update-indexes) and `generators/compare/` already exist.
5. **Shared partials** via `_includes/` + `scripts/build-partials.py` + pre-commit + CI drift check enables safe rail injection across 517 city pages.
6. **`/api/build-api.py`** is the canonical place to expose new entity types as static JSON.
7. **AEO pattern is documented** (`ARCHITECTURE.md` §2.0): answer-first paragraph + JSON-LD with `additionalProperty`, `lastVerified`, `sourcesAnalyzed`.

---

## 2. URL hierarchy

```
/scams/                                      ← existing master hub
  /scams/{city}/                             ← existing × 517
  /scams/country/{cc}/                       ← existing × 60
  /scams/atlas/                              ← NEW: unified atlas hub
    /scams/atlas/{entry-slug}/               ← NEW × 80–100
  /scams/atlas/{entry-slug}/{country-cc}/    ← NEW × ~150 (selective Phase 2)
```

**One namespace, one template family.** No types/playbook split. Each atlas entry is named by its strongest search query — broad-sounding ones capture head queries, specific ones capture long-tail.

Examples:
- `/scams/atlas/taxi-meter-manipulation/` — captures "taxi scam" head query
- `/scams/atlas/atm-skimming/` — captures "atm skimming" head query
- `/scams/atlas/the-gold-ring-trick/` — captures named long-tail query
- `/scams/atlas/tourist-trap-restaurants/` — captures "tourist trap" head query
- `/scams/atlas/three-card-monte/` — captures both head + named
- `/scams/atlas/friendship-bracelet-trap/` — captures "friendship bracelet scam"

---

## 3. Data foundation — taxonomy normalization

`generators/scam-atlas/data/entries.json` is the source of truth — a flat list of atlas entries:

```jsonc
{
  "entries": [
    {
      "slug": "taxi-meter-manipulation",
      "name": "Taxi Meter Manipulation",
      "entryStyle": "broad",                 // broad | specific
      "synonyms": ["taxi-scams", "cab-scam", "taxi-fraud", "fake-taxi-meter"],
      "subTypes": [                          // populated for broad-style entries
        "cloned-meter",
        "long-route",
        "counterfeit-return",
        "unlicensed-curb-tout"
      ],
      "minScamThreshold": 10,                // page only generates if ≥10 across ≥4 countries
      "primaryBookFunnels": ["argentina", "italy", "mexico", "thailand"],
      "primaryQueryTarget": "taxi scam"
    },
    {
      "slug": "the-gold-ring-trick",
      "name": "The Gold Ring Trick",
      "entryStyle": "specific",
      "synonyms": ["gold-ring-scam", "gold-ring-trick"],
      "parentEntry": "distraction-theft",    // optional — soft hierarchy for cross-links
      "variantsByCity": ["paris", "madrid", "rome", "vienna", "budapest"],
      "primaryBookFunnels": ["france", "italy", "spain"],
      "primaryQueryTarget": "the gold ring trick"
    }
    // ...80–100 total entries
  ]
}
```

**The `entryStyle` field drives template adaptation:**
- `broad` → renders sub-type taxonomy, geographic distribution, aggregate stats
- `specific` → renders single-mechanism breakdown, city variants, language-specific refusals

**Recategorization pipeline:** `extract.py` reads all 2,836 indexed scams and applies synonym mapping to assign each scam to a parent atlas entry. The 1,481 `tourist-trap` entries get re-distributed via Claude API (with prompt caching) into the right atlas-entry bucket; low-confidence rows go to a human review queue.

---

## 4. Page template (single, adaptive)

Single page anatomy. The `entryStyle` field switches certain blocks on/off.

**All entries get:**
- Bold answer-first paragraph (e.g., "Tabiji has documented N variants of this scam across X countries as of April 2026.")
- "Where it runs" mini-table (top countries by frequency)
- Universal red flags
- Refusal scripts (with HowTo schema)
- 3-card book-funnel rail: top 3 most-relevant country books with Amazon CTAs (UTM-tagged `?ref=tabiji_atlas_{slug}`)
- Sources block (police + press citations)
- Comic illustration (remixed from existing per-country comic assets)
- Cross-links to related atlas entries + city pages
- Article + FAQPage + HowTo + BreadcrumbList JSON-LD
- Speakable spec on the answer-first paragraph + refusal scripts

**`entryStyle: "broad"` adds:**
- Sub-type taxonomy section (named sub-variants with one-line descriptions)
- Geographic distribution heat map (country + city frequency)
- "Tabiji 2026 frequency snapshot" (count + YoY delta)

**`entryStyle: "specific"` adds:**
- Origin/history with press citation
- Single-mechanism step-by-step (3–5 steps)
- City-by-city variants block (using existing per-city scam descriptions)
- Per-language refusal phrases (IPA + audio)

The renderer (`render-page.js`) selects template fragments based on `entryStyle`, but the URL, hub indexing, and cross-link logic are unified.

---

## 5. Navigation & cross-link architecture

The atlas is wired into the rest of the site through **four layers**: top-level nav, the master `/scams/` hub redesign, lateral managed-include rails on existing pages, and outbound links from atlas pages.

### 5.1 Top-level nav — minimal change

**Don't add a new top-level nav element.** The existing nav already has "Tourist Scams" as a flat link to `/scams/`; a sibling "Scam Atlas" creates redundancy because the atlas is conceptually part of /scams/, not a peer.

**Single change: add one entry to the existing "Explore" dropdown.**

```html
<div class="nav-dropdown-menu">
    <a href="/popular-picks/">⭐ Popular Picks</a>
    <a href="/countries/">🗺 Country Guides</a>
    <a href="/compare/">🆚 Compare Destinations</a>
    <a href="/scams/atlas/">📋 Scam Atlas</a>   <!-- NEW -->
    <a href="/health/">🏥 Travel Health Tips</a>
    <a href="/api/">🔌 API</a>
</div>
```

Footer "Explore" column receives the same one-line addition. This is the only nav change.

### 5.2 Hub gateway — `/scams/` master hub redesign

The `/scams/` master hub becomes the canonical gateway. Restructure its top so the atlas is the editorial entry point and the city/country directories are deeper drill-downs.

```
/scams/                                    ← master scam hub
  ├── 📋 The Scam Atlas         (NEW prominent section, top of page)
  │   "Browse 80 documented scam playbooks — the gold ring trick,
  │    ATM skimming, taxi meter manipulation, and more →"
  │   [link to /scams/atlas/]
  │
  ├── 📍 Browse by City          (existing — 517 cities)
  ├── 🗺 Browse by Country       (existing — 60+ country hubs)
  └── 🚨 Got scammed? What to do  (future Recovery Hub idea, not in this scope)
```

### 5.3 Lateral linking — three managed-include rails

This is where the value compounds. Three new `<!-- @include:scam-atlas-rail:* -->` rails, propagated by `scripts/build-partials.py`:

**Rail A — On every `/scams/{city}/` page** (per-scam atlas backlinks):
Every individual scam description on every city page gets a one-line link to its atlas entry. Turns 2,836 scam descriptions into 2,836 links into the atlas.

```
Scam #3: The Bird Poop / Mustard Distraction Pickpocket
[existing scam description]
📋 Atlas entry → The Bird Poop Distraction (12 country variants) →
```

**Rail B — On every `/scams/country/{cc}/` page** (atlas entries by frequency):
```
Atlas entries documented in Argentina:
  📋 Counterfeit Currency Returns (8 variants)
  📋 Taxi Meter Manipulation (6 variants)
  📋 ATM Skimming (4 variants)
  ...
```

**Rail C — On every `/books/{country}-tourist-scams/` lander** (atlas-coverage rail):
```
What's in the Italy book — 14 atlas entries:
  📋 Taxi Meter Manipulation · 📋 Restaurant Bill Padding ·
  📋 The Gold Ring Trick · 📋 Gladiator Photo Shakedown · ...
[Buy on Amazon →]
```

All three rails are managed-include blocks updated by `scripts/build-partials.py` — never manually edited across 517+ pages.

### 5.4 Outbound from atlas pages

Each `/scams/atlas/{slug}/` page links out to:
- **Sister atlas entries** (via `parentEntry` or shared sub-types) — "Related atlas entries" section
- **Cities where this scam runs** — links to `/scams/{city}/#scam-N` (anchor to the specific scam on city page)
- **Country code hubs** — links to `/scams/country/{cc}/`
- **Top 3 country book landers** — multi-book CTA strip with UTM-tagged Amazon links
- **Master `/scams/` hub** — via breadcrumb

### 5.5 Breadcrumbs

Consistent BreadcrumbList JSON-LD on every atlas page:

```
Home > Scams > Atlas > The Gold Ring Trick
Home > Scams > Atlas > Taxi Meter Manipulation > Italy   (cross-cut pages, Phase 2)
```

The visible breadcrumb label can read "Scam Atlas" even though the URL token is `/atlas/`.

### 5.6 Linking graph — visual summary

```
                    ┌───────────────────────────┐
                    │  HOMEPAGE (no direct link)│
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │  Nav "Explore" dropdown   │
                    │  + Footer Explore column  │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │     /scams/ master hub    │
                    │  (atlas section on top)   │
                    └─────────────┬─────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        ▼                         ▼                         ▼
┌──────────────┐         ┌─────────────────┐       ┌────────────────┐
│ /scams/{city}│ ◄──────►│  /scams/atlas/  │◄──────│/scams/country/ │
│   (517)      │ Rail A  │  hub + 80–100   │ Rail B│   (60)         │
└──────────────┘         │   entry pages   │       └────────────────┘
                         └────────┬────────┘
                                  │ Rail C
                                  ▼
                    ┌──────────────────────────┐
                    │ /books/{country}-...     │
                    │ (multi-book CTA strip,   │
                    │  UTM-tagged Amazon)      │
                    └──────────────────────────┘
```

---

## 6. Build pipeline

```
generators/scam-atlas/
├── data/
│   ├── entries.json               ← ~80–100 atlas entries, flat list
│   ├── synonyms.json              ← old-tag → canonical-slug mapping
│   └── review-queue.json          ← editorial queue for low-confidence recategorizations
├── extract.py                     ← reads /api/v1/scams/*.json → emits build-time recategorized data (not public)
├── recategorize.py                ← Claude API + prompt caching, re-tags ambiguous rows
├── build-atlas-page.js            ← single page builder (--slug, --all, --validate-only, --dry-run)
├── build-atlas-hub.js             ← /scams/atlas/index.html
├── render-page.js                 ← adapts based on entryStyle (broad vs specific)
├── render-meta.js
├── render-schema.js               ← Article + FAQPage + HowTo + BreadcrumbList + Speakable
├── update-cross-links.py          ← injects @include rails (A, B, C) into city/country/book pages
├── update-indexes.js              ← sitemap.xml, llms.txt, agents.json, /scams/index.html, nav/footer Explore
└── validate.js                    ← word count, schema, dup-content vs city pages, link integrity
```

**Touched existing files:**
- `_includes/nav-main.html` — add "📋 Scam Atlas" entry to Explore dropdown
- `_includes/footer-default.html` — add "Scam Atlas" to Explore column
- `scripts/build-partials.py` — extended to manage scam-atlas-rail blocks (A, B, C)
- `.githooks/pre-commit` — extended: reject scams w/o canonical atlas-entry assignment
- `.github/workflows/check-partials.yml` — extended: scam-atlas-rail drift check

**Not touched:** No public API surface (`/api/v1/scam-atlas/`). The HTML pages themselves are AI-citable, and existing `/api/v1/scams/{city}.json` already exposes the underlying data. If AI agents start citing atlas pages heavily later, we can expose a public JSON in a v1.6 release — not a v0 problem.

---

## 7. Phasing & gates

| Phase | Weeks | Pages | Gate to next |
|---|---|---|---|
| **0. Foundation** | W1 | Entries list + recategorization + review queue resolved + nav/footer updated | Editorial sign-off on ~80–100 entry list |
| **V0 Pilot** | W2 | 3 atlas entries (mix: 1 broad + 1 specific + 1 hybrid) + atlas hub + Rail A on a sample of 10 city pages | 4-week measurement: CTR to /books/ ≥ baseline /scams/{city}/ rate |
| **1. Atlas full** | W3–10 | Remaining ~85 entries + Rails A/B/C rolled out across all 517 city pages, 60 country hubs, 22 book landers | All pages pass validate.js; AEO spot-check on 5 random pages |
| **2. Country cross-cuts** | W11–14 | ~150 selective entry × country pages | Funnel attribution dashboard live; bundle SKU decision |

**Net deliverable:** ~230–250 new pages, 22 books × 3-card CTA visibility on every one of them, and a managed cross-link rail across the entire existing /scams/ surface.

---

## 8. Audit trail

### Audit 1 — SEO/AEO

**Gaps found:**
- HowTo schema not in initial plan
- Slug-aliasing risk without 301s
- `/api/v1/` doesn't expose atlas entities
- `llms.txt` + `agents.json` need updating
- Duplicate-content risk if atlas pages just list scams from city pages

**Refinements applied:**
- Added HowTo schema for refusal scripts
- Canonical-redirect map in entries.json + `_redirects` file injection
- Auto-update `llms.txt`, `agents.json` via `update-indexes.js`
- Required net-new content per atlas page (frequency snapshot + YoY delta + universal refusal scripts) — none of which appear on city pages
- **Decided NOT to ship a public `/api/v1/scam-atlas/` JSON surface** — over-engineering for v0. HTML pages are already AI-citable; existing `/api/v1/scams/{city}.json` exposes the underlying data. Defer public JSON to v1.6 if needed.

### Audit 2 — Engineering

**Gaps found:**
- Recategorizing 1,481 `tourist-trap` rows is high-stakes
- Future scams need pre-categorized cleanly to prevent drift
- Rail injection across 517 pages is most error-prone
- Risk of building 80+ pages before measuring ROI
- No CI guardrail for missing atlas-entry assignment

**Refinements applied:**
- **Step 0a:** `recategorize.py` runs Claude API w/ prompt caching against ambiguous rows; high-confidence (>0.85) auto-applied, low-confidence to `review-queue.json` for editorial
- **Step 0b:** Update scam-authoring schema to require `atlasEntry` field. Update `.githooks/pre-commit` to reject scam JSONs without canonical atlas-entry
- Rail injection uses managed-include pattern via `scripts/build-partials.py`
- **V0 gate:** 3 pilot pages, 4-week measurement window, only proceed to Phase 1 if CTR to `/books/*` from atlas pages ≥ CTR from `/scams/{city}/`
- Generator script flags: `--slug`, `--all`, `--validate-only`, `--dry-run` (mirror compare/ + popular-picks/)

### Audit 3 — Content quality

**Gaps found:**
- Some entries may be too thin (e.g., "tipping scams" only ~4 examples)
- 80–100 × ~1,500 words = 120k–150k words; QC cost is real
- No comic strategy for atlas pages
- Editorial ownership unclear

**Refinements applied:**
- **Volume threshold:** An entry renders only if ≥10 scams across ≥4 countries. Below threshold get folded into a parent entry via `parentEntry`.
- **Net-new content requirements (codified in `validate.js`):** every atlas page must contain
  1. "Tabiji 2026 frequency snapshot" (count + YoY delta + top countries)
  2. Universal red-flags list (synthesized)
  3. Universal refusal scripts (synthesized, with HowTo schema)
  4. Sources block
  5. ≥800 words of original synthesis (validate.js enforces word count + duplicate-content check vs city pages)
- **Comic montage:** atlas pages get a 4-panel comic remixed from existing per-country comic assets. Existing comic-cast convention (Margie/Priya/Harry/Marcus) keeps brand consistent.
- **Editorial owner:** Rebecca sets the bar (per existing convention), Bernard's byline.

### Audit 4 — Funnel to books

**Gaps found:**
- Generic CTAs underperform
- No attribution loop on Amazon links
- No bundle SKU to capture cross-sell intent
- Multi-book CTA strip absent in initial design

**Refinements applied:**
- **Per-page multi-book CTA strip:** 3 cards w/ cover thumbnail + Amazon CTA, ranked by atlas-entry frequency in that country
- **UTM convention on every Amazon link:** `?ref=tabiji_atlas_{slug}`
- **Specific copy per CTA:** "12 taxi scams documented in Italy — the full atlas →" instead of generic "$4.99 on Kindle"
- **Future: bundle product** — recommend creating "Travel Safety Bundle: All 22 books" SKU at $49.99 (vs $109.78 á la carte). Atlas pages naturally generate bundle-buyer intent.
- Add "most-scam-prone country" + "fastest-growing scam type" data points as natural urgency drivers tied to specific book CTAs

### Audit 5 — Consolidation pass (post-V4)

**Gaps found:**
- Original plan split content into `/scams/types/` (categories) and `/scams/playbook/` (named scams) — artificial binary that doesn't match how scams actually exist (many entries are *both* a category AND a named pattern, e.g., ATM skimming, three-card monte, express kidnapping)
- Two hubs fragment internal-linking signal
- Two generators / two templates / two CI checks for the same conceptual job
- Forces every new entry into a binary classification on edge cases

**Refinements applied:**
- **Single namespace:** `/scams/atlas/` for all entries
- **Single template** with `entryStyle: "broad" | "specific"` field that toggles conditional blocks (sub-type taxonomy for broad; mechanism + city variants for specific)
- **Single hub** at `/scams/atlas/` with visual sub-sections if needed (paginated/filtered, not URL-split)
- **Slug discipline:** each entry slug is named by its strongest search query (some end up broad-sounding, some specific) — `validate.js` lints for slug collisions
- **Entry count drops** from 110 (30 + 80) to ~80–100 (a single curated list, prioritized by aggregate query potential rather than artificial broad/specific split)
- **Generator simplification:** one `build-atlas-page.js` instead of two builders
- **Soft hierarchy preserved** via optional `parentEntry` field — used for cross-linking sister entries, not URL nesting

### Audit 6 — Navigation & cross-link architecture

**Gaps found:**
- Earlier plan covered the rails but didn't decide where the atlas surfaces in global nav
- Risk of fragmenting authority by adding a new top-level nav peer to "Tourist Scams"
- Master `/scams/` hub didn't have a defined gateway treatment for the atlas
- Per-scam atlas backlinks (Rail A) weren't explicitly specified — just "atlas links from city pages"
- Breadcrumb labels and JSON-LD structure for atlas pages weren't spec'd

**Refinements applied:**
- **No new top-level nav.** Single one-line addition to existing "Explore" dropdown (`📋 Scam Atlas`) + matching footer link. Avoids authority fragmentation.
- **`/scams/` hub redesign** elevates atlas to the top section ("Browse 80 documented scam playbooks…") with city/country directories below.
- **Three named rails** (A: per-scam atlas backlinks on city pages; B: atlas-by-frequency on country hubs; C: atlas-coverage strip on book landers), all managed-include via `scripts/build-partials.py`.
- **Rail A specifies per-scam granularity** — every scam description on every city page gets a one-line link to its atlas entry. Turns 2,836 scam blocks into 2,836 atlas links.
- **Breadcrumb structure spec'd:** `Home > Scams > Atlas > {Entry}`; `Home > Scams > Atlas > {Entry} > {Country}` for cross-cuts. Visible label "Scam Atlas" even though URL token is `/atlas/`.
- **Outbound link spec from atlas pages:** sister entries → cities (with `#scam-N` anchors) → country hubs → 3 book CTAs → master `/scams/` (breadcrumb).
- `_includes/nav-main.html` and `_includes/footer-default.html` both updated; `update-indexes.js` keeps them in sync.

---

## 9. Final implementation plan (post-audit)

### Stack changes from V1 → V6
- ✅ Added HowTo schema for refusal scripts
- ✅ Added canonical-redirect rules to handle slug aliases
- ✅ Decided NOT to ship `/api/v1/scam-atlas/` (deferred — HTML pages are AI-citable, existing `/api/v1/scams/{city}.json` exposes underlying data)
- ✅ Added `recategorize.py` with Claude API + confidence scoring + review queue
- ✅ Updated scam-authoring schema to require canonical atlas-entry assignment
- ✅ Added pre-commit guardrail rejecting scams without atlas-entry
- ✅ V0 pilot gate (3 pages, 4-week measurement) before scaling
- ✅ Volume threshold (10 scams ≥4 countries) prevents thin pages
- ✅ Required net-new content per entry, enforced by `validate.js`
- ✅ Comic montage strategy (remix existing assets)
- ✅ Multi-book CTA strip with country-specific copy + UTM tags
- ✅ llms.txt + agents.json + sitemap.xml auto-update
- ✅ Consolidated under `/scams/atlas/` — single namespace, single template family, ~80–100 entries
- ✅ **Navigation & cross-link architecture spec'd** — Explore dropdown entry, /scams/ hub gateway, three rails (A/B/C), breadcrumbs, outbound links

---

## 10. What needs human decisions before W1 starts

1. **Approve the ~80–100 atlas entry list** (Bernard / Rebecca). Draft pulled from data; final naming + scope is editorial.
2. **Approve `/scams/atlas/` as the URL** (or veto and pick alternate, e.g., `/scams/types/`, `/scams/handbook/`, `/scams/all/`).
3. **Approve V0 pilot gate criteria** — what CTR-to-books threshold counts as "go for Phase 1"?
4. **Bundle SKU decision** — create "All 22 books" product? Affects CTA design.
5. **Editorial capacity** — who writes the ~80–100 atlas synth blocks? Bernard, Rebecca, or contracted help?

---

## 11. References

- `ARCHITECTURE.md` — site architecture, AEO pattern §2.0
- `generators/popular-picks/` — generator pattern to follow
- `generators/compare/` — alternative generator pattern
- `_includes/README.md` — partials/build-partials.py pattern
- `_includes/nav-main.html` — nav partial (will receive Atlas dropdown entry)
- `_includes/footer-default.html` — footer partial (will receive Atlas link)
- `/api/v1/scams/*.json` — existing structured scam data (input)
- `/api/v1/scams.json` + `/api/v1/catalog/scams.json` — master indexes
