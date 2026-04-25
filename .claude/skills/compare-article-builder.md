---
name: compare-article-builder
description: Build a complete compare article from scratch — generate content via Gemini, research real Reddit quotes via SerpAPI, add photos (SerpAPI + Gemini Vision + R2), enrich, validate, and deploy. Trigger when user says "build compare [slug]", "compare-article-builder", or wants to create a new comparison page. Also handles batch builds from the compare queue.
user_invocable: true
---

# Compare Article Builder

Build a complete tabiji.ai compare page from queue to deployment.

## When to use
- When creating a new compare page (e.g., "build compare madrid-vs-barcelona")
- When batch-building compare pages from the queue
- When rebuilding or refreshing an existing compare page
- When the user says "build compare [slug]" or "/compare-article-builder"
- When running as a cron job to process the compare queue

## Required input
A slug in `{dest1}-vs-{dest2}` format (e.g., `madrid-vs-barcelona`, `tokyo-vs-kyoto`), or the word `batch` to process pending items from `scripts/queues/compare-queue.json`.

## Reference implementation
**`tokyo-vs-kyoto`** and **`madrid-vs-barcelona`** are the gold standards — both score 100/100 on the canonical quality gate. New pages must match their structure, tone, and quality bar. Both include: score ticker, Quick Answers, Visual Scorecard, Personalize widget, cost widget, weather chart, 4-tab sample itineraries, deep-dive sections with `tabiji-verdict` callouts, Reddit quotes, FAQ with 16+ items, and a related-comparisons section.

## Quality standard (mandatory) — 100/100 quality gate

Every compare page MUST score 100/100 on `scripts/score_compare.py`. The build pipeline aborts if any check fails when `STRICT_QUALITY_GATE=1` is set. The rubric:

**Template & structure (35 pts)**
1. **Comparison table** (5) — `<table class="comparison-table">` with at least 4 rows
2. **FAQ items ≥ 16** (10) — full count, not 7 or 8. Cover both common ("which is cheaper?") and operational ("language barrier?", "cash vs card?", "kid-friendly?", "vegetarian options?", "walkability?") questions
3. **Quick Answers section** (8) — `<div class="quick-answers">` with 6 cards, **server-rendered** (don't rely on compare-ux.js JS injection)
4. **Visual Scorecard** (7) — `<div class="scorecard">` with 9 category rows
5. **Personalize widget** (5) — `<div class="personalize-widget">` with style/budget/priority pills + recommendation map

**Content fundamentals (35 pts)**
6. **Title 35–65 chars** (10) — drop "(2026 Comparison)" if it pushes over 65
7. **Meta description 90–160 chars** (10)
8. **Bernard Huang byline** (5) — `<div class="page-byline" data-byline="bernard-huang">` for E-E-A-T
9. **`tabiji-verdict` callout** (5) — at least one per page; deep-dive sections should use this, not the older `section-winner`
10. **Photo-grid with 2+ images** (5) — `<div class="photo-grid">` with `dest1.jpg` + `dest2.jpg`

**Technical hygiene (30 pts)**
11. **All in-page anchors resolve** (8) — every `href="#x"` must have a matching `id="x"` in the body
12. **No `&amp;amp;` encoding bug** (6) — never let `&amp;amp;` leak into output
13. **Mobile-overflow tables wrapped** (6) — any `<table style="...min-width:>480px">` must be inside `<div style="overflow-x:auto">`
14. **LCP image not lazy-loaded** (5) — first `<img>` inside `.photo-grid` must NOT have `loading="lazy"`
15. **LCP image has `fetchpriority="high"`** (5) — must be set on the same first photo-grid `<img>`

To audit: `python3 scripts/score_compare.py <slug> --gate 100`. Exit 0 = ship; exit 1 = fix and re-run.

## Full Workflow (6 steps)

### Step 1: Generate Content (Gemini)

Generate the compare-data JSON with all content blocks:

```bash
python3 scripts/batch-compare-gen.py generate <slug>
```

This creates:
- `compare-data/<slug>.json` — master data file (~100KB, includes richContent)
- `compare/<slug>/index.html` — rendered premium HTML page (~100-110KB, ~1400 lines)
- Uploads hero photos (dest1.jpg, dest2.jpg, hero.jpg) to R2

The generator makes TWO Gemini API calls:
1. **Base content** — categories, verdicts, FAQ, decision framework
2. **Rich structured data** — cost table, weather data, itineraries, quick answers, scorecard, related comparisons

If the rich content call fails, it falls back gracefully to a basic template. If the page already exists, it will be skipped. To force regeneration, delete the HTML first.

### Step 2: Reddit Research (Real Quotes)

Search for actual Reddit threads and extract real traveler quotes:

```bash
python3 scripts/reddit_research.py <slug> --save
```

This:
1. Searches SerpAPI for `"{dest1} vs {dest2}" site:reddit.com` (4 query variations)
2. Fetches comments from top 5 Reddit threads via Reddit JSON API
3. Uses Gemini to select the best 1-2 quotes per deep-dive section from real comments
4. Injects quotes into `compare-data/<slug>.json`
5. Saves research metadata to `compare-data/<slug>.research.json`

**If no Reddit threads are found** (niche comparisons), the script falls back gracefully. Use Step 3 to add synthesized quotes instead.

### Step 3: Enrich (Verdict Cards + Fallback Quotes)

Add verdict cards and fill any remaining quote gaps:

```bash
python3 generators/compare/enrich_compare.py --run --slug <slug>
```

This is idempotent — it only adds missing elements:
- Verdict cards (Choose A / Choose B) if absent
- Reddit-style quotes for sections that still lack them
- Uses Gemini to generate realistic, opinionated quotes

### Step 4: Add Photos (SerpAPI + Gemini Vision + R2)

Add high-quality photos for the page:

```bash
python3 scripts/add_compare_photos.py <slug>
```

Photo slots (minimum 4):
- **dest1.jpg** — iconic photo of destination 1 (hero grid)
- **dest2.jpg** — iconic photo of destination 2 (hero grid)
- **hero.jpg** — OG/social share image (copy of dest1)
- **section-1.jpg, section-2.jpg, section-3.jpg** — deep-dive section images

Pipeline per photo:
1. SerpAPI Google Images search (6 candidates)
2. Download top 4 candidates
3. Gemini Vision scoring (1-10: quality, iconic-ness, no watermarks)
4. Optimize winner: 800px wide, JPEG 80% quality
5. Upload to Cloudflare R2 at `compare/<slug>/`

To check which photos are missing: `python3 scripts/add_compare_photos.py <slug> --check`
To only add hero photos: `python3 scripts/add_compare_photos.py <slug> --hero-only`

**Credentials required:**
- SerpAPI: `security find-generic-password -s serpapi-key -w`
- R2 token: `security find-generic-password -s cloudflare-api-token -w`
- Gemini: `security find-generic-password -s gemini-api-key -w`

### Step 5: Rebuild HTML + Validate

After enrichment and photos, rebuild HTML with strict quality enforcement:

```bash
# For new pages — strict gate enforced; build fails if score < 100
STRICT_QUALITY_GATE=1 python3 generators/compare/build_compare.py build

# Always run the structural validator
python3 generators/compare/build_compare.py validate
```

The strict gate adds parity with `scripts/score_compare.py`'s 100-point rubric to the build's `validate_rendered_output`. If the rendered HTML lacks Quick Answers, Scorecard, Personalize widget, 16+ FAQ items, the LCP fix, or any other rubric item, the build aborts with `[gate]`-prefixed errors so you can see exactly what's missing.

### Step 5.5: Score gate (single-page check)

Before committing, run the score gate explicitly on the new slug:

```bash
python3 scripts/score_compare.py <slug> --gate 100
```

Exits 0 if the page scores 100/100. Exits 1 with an itemized list of failed checks otherwise. **Do not commit a page that doesn't pass this gate.**

If the score is below 100, the failed checks tell you what to fix:
- `only N FAQ items` → extend the FAQ in `compare-data/<slug>.json` to 16+ entries, then rebuild
- `missing .quick-answers/.scorecard/.personalize-widget` → the Gemini rich-content call probably failed; rerun `generate_rich_content` or hand-fill the JSON keys
- `first photo-grid <img> is lazy-loaded` → the builder fix is in `batch-compare-gen.py` photo_grid_html; check it didn't get reverted
- `title is N chars, must be 35–65` → trim the SEO title in `compare-data/<slug>.json#seo.title`

### Step 6: Finalize + Deploy

**Hard rule: do not run any of this until `score_compare.py --gate 100` passes.** A failing gate means the page is sub-standard and shouldn't ship.

Update indexes and commit:

```bash
# Update inventory, sitemap, API index
python3 scripts/batch-compare-gen.py finalize

# Commit and deploy
git add compare/<slug>/index.html compare-data/<slug>.json
git commit -m "Add compare page: <slug> (100/100 gate passed)"
git push origin main
```

Cloudflare Pages auto-deploys from main.

## Batch Building

### From the queue
Process pending items from `scripts/queues/compare-queue.json`:

```bash
# Check what's pending
python3 -c "import json; q=json.load(open('scripts/queues/compare-queue.json')); print(f'{sum(1 for i in q if i[\"status\"]==\"pending\")} pending')"

# Build next N pages
python3 scripts/batch-compare-gen.py batch <slugs.json>
```

### Batch photo addition
```bash
python3 scripts/add_compare_photos.py batch <slugs.json>
```

### Parallel agents
For large batches, launch parallel agents — each handles one slug through the full pipeline:
1. Generate content
2. Reddit research
3. Enrich
4. Add photos
5. Validate

Then finalize all at once and commit.

## Cron Job Setup

To run as a recurring cron job that processes the compare queue:

**Recommended schedule:** Every 2 hours during work hours, or 3x daily.

The cron prompt should be:
```
Process the next 3 pending items from scripts/queues/compare-queue.json through the full compare-article-builder pipeline. For each: generate content, research Reddit, enrich, add photos, build with STRICT_QUALITY_GATE=1, then run scripts/score_compare.py <slug> --gate 100. Skip any slug whose gate fails (do not commit it; log the failed checks). After processing, finalize and commit only the slugs that passed with message "Add compare pages: [passing-slugs] (100/100 automated build)".
```

**Pipeline per slug (automated):**
1. `python3 scripts/batch-compare-gen.py generate <slug>`
2. `python3 scripts/reddit_research.py <slug> --save` (non-fatal if no threads found)
3. `python3 generators/compare/enrich_compare.py --run --slug <slug>`
4. `python3 scripts/add_compare_photos.py <slug>`
5. `STRICT_QUALITY_GATE=1 python3 generators/compare/build_compare.py build`
6. `python3 scripts/score_compare.py <slug> --gate 100` ← **must pass; skip the slug if it fails**
7. `python3 generators/compare/build_compare.py validate`

After all slugs (only those that passed step 6):
8. `python3 scripts/batch-compare-gen.py finalize`
9. Git add + commit + push

## Quality Checklist

Before committing any page, verify:

### Quality gate (mandatory)
- [ ] **`python3 scripts/score_compare.py <slug> --gate 100` exits 0** ← if this fails, do not ship

### Content
- [ ] TL;DR verdict is clear and opinionated
- [ ] Quick comparison table has 8+ rows with Edge column
- [ ] 8+ deep-dive sections, each ending in a `tabiji-verdict` callout (not `section-winner`)
- [ ] 3+ Reddit quotes (real preferred, synthesized acceptable)
- [ ] **16+ FAQ items** with specific answers (cherry blossom, JR Pass, kid-friendliness, language barrier, vegetarian, walkability, cash usage, packing, crowd strategy, etc.)
- [ ] Decision framework with concrete bullet points
- [ ] Costs include local currency estimates
- [ ] No leftover template text, wrong destination names, or `&amp;amp;` encoding bugs

### Technical
- [ ] All 3 schema blocks: Article (with speakable), BreadcrumbList, FAQPage (with all 16+ Qs)
- [ ] `<title>` follows format: `{A} vs {B}: Which Should You Visit?` — **35–65 chars**, drop the "(2026 Comparison)" suffix if it overflows
- [ ] Meta description 90–160 chars
- [ ] Canonical URL correct: `https://tabiji.ai/compare/<slug>/`
- [ ] OG image points to actual R2 image
- [ ] GA4 tag present (`G-D7QHNRXLHJ`)
- [ ] First photo-grid `<img>` has `fetchpriority="high"` and **no `loading="lazy"`**
- [ ] Validates: `STRICT_QUALITY_GATE=1 python3 generators/compare/build_compare.py validate`

### Images
- [ ] 4+ images on R2 at `img.tabiji.ai/compare/<slug>/`
- [ ] Hero photo grid has 2 images (dest1.jpg, dest2.jpg)
- [ ] hero.jpg exists for social sharing
- [ ] All images optimized (800px wide, JPEG ~80%)

### Index & API
- [ ] `compare/inventory.json` updated
- [ ] `sitemap.xml` updated with new URL

## Common Mistakes to Avoid

- **Don't ship a sub-100 page.** Run `scripts/score_compare.py <slug> --gate 100` before every commit. If it fails, fix the listed checks. Never commit with `[gate]`-prefixed errors visible.
- **Don't hand-write HTML** — always generate via `build_compare.py build` from compare-data JSON
- **Don't ship with 7- or 8-item FAQ.** The Gemini prompt asks for 16; if the response comes back short, regenerate or hand-extend before building.
- **Don't rely on `compare-ux.js` to inject Quick Answers / Scorecard.** They must be **server-rendered** (in the HTML at build time). JS injection misses non-JS crawlers and causes layout shift.
- **Don't `loading="lazy"` the LCP image.** The first `<img>` inside `.photo-grid` must have `fetchpriority="high"` and no `loading=` attribute. The builder gets this right; don't undo it.
- **Don't skip Reddit research** — the brand is "Reddit-backed, not AI filler"
- **Don't forget R2 upload** — images go to R2, not git. Dead image links = broken page
- **Don't use generic verdicts** — "Both are great!" is not a verdict. Pick a side
- **Don't skip finalize** — every new page needs inventory, API, sitemap updates

## Related Files
- **Quality gate (run before every commit):** `scripts/score_compare.py`
- Content generator: `scripts/batch-compare-gen.py`
- Reddit research: `scripts/reddit_research.py`
- Photo pipeline: `scripts/add_compare_photos.py`
- Enrichment: `generators/compare/enrich_compare.py`
- HTML builder (with strict-mode gate parity): `generators/compare/build_compare.py`
- Shell template: `scripts/compare-shell-template.json`
- Compare queue: `scripts/queues/compare-queue.json`
- Inventory: `compare/inventory.json`
- Photo pipeline docs: `docs/photo-pipeline.md`
- Full runbook: `docs/compare-page-runbook.md`
