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
A slug in `{dest1}-vs-{dest2}` format (e.g., `madrid-vs-barcelona`, `tokyo-vs-kyoto`), or the word `batch` to process pending items from `compare-queue.json`.

## Reference implementation
**`tokyo-vs-kyoto`** and **`amsterdam-vs-berlin`** are the current reference implementations. New pages must match their structure, tone, and quality bar.

## Full Workflow (6 steps)

### Step 1: Generate Content (Gemini)

Generate the compare-data JSON with all content blocks:

```bash
python3 scripts/batch-compare-gen.py generate <slug>
```

This creates:
- `compare-data/<slug>.json` — master data file (~70KB)
- `compare/<slug>/index.html` — rendered HTML page
- `api/v1/compare/<slug>.json` — API endpoint
- Uploads hero photos (dest1.jpg, dest2.jpg, hero.jpg) to R2

If the page already exists, it will be skipped. To force regeneration, delete the HTML first.

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

After enrichment and photos, rebuild HTML and validate:

```bash
python3 generators/compare/build_compare.py build
python3 generators/compare/build_compare.py validate
```

Validation checks:
- Minimum 2 verdict cards with meaningful text
- Comparison table with 4+ rows
- 3+ bullets per deep-dive section
- FAQ items meet length requirements
- No placeholder text
- All required schema blocks present

### Step 6: Finalize + Deploy

Update indexes and commit:

```bash
# Update inventory, sitemap, API index
python3 scripts/batch-compare-gen.py finalize

# Commit and deploy
git add compare/<slug>/index.html compare-data/<slug>.json api/v1/compare/<slug>.json
git commit -m "Add compare page: <slug>"
git push origin main
```

Cloudflare Pages auto-deploys from main.

## Batch Building

### From the queue
Process pending items from `compare-queue.json`:

```bash
# Check what's pending
python3 -c "import json; q=json.load(open('compare-queue.json')); print(f'{sum(1 for i in q if i[\"status\"]==\"pending\")} pending')"

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
Process the next 3 pending items from compare-queue.json through the full compare-article-builder pipeline. For each: generate content, research Reddit, enrich, add photos, validate. Then finalize all and commit with message "Add compare pages: [slugs] (automated build)". Skip any that fail and log the failure.
```

**Pipeline per slug (automated):**
1. `python3 scripts/batch-compare-gen.py generate <slug>`
2. `python3 scripts/reddit_research.py <slug> --save` (non-fatal if no threads found)
3. `python3 generators/compare/enrich_compare.py --run --slug <slug>`
4. `python3 scripts/add_compare_photos.py <slug>`
5. `python3 generators/compare/build_compare.py build`
6. `python3 generators/compare/build_compare.py validate`

After all slugs:
7. `python3 scripts/batch-compare-gen.py finalize`
8. Git add + commit + push

## Quality Checklist

Before committing any page, verify:

### Content
- [ ] TL;DR verdict is clear and opinionated
- [ ] Quick comparison table has 8+ rows with Edge column
- [ ] 8+ deep-dive sections, each with `tabiji-verdict` or `section-winner`
- [ ] 3+ Reddit quotes (real preferred, synthesized acceptable)
- [ ] 7+ FAQ questions with specific answers
- [ ] Decision framework with concrete bullet points
- [ ] Costs include local currency estimates
- [ ] No leftover template text or wrong destination names

### Technical
- [ ] All 3 schema blocks: Article (with speakable), BreadcrumbList, FAQPage
- [ ] `<title>` follows format: `{A} vs {B}: Which Should You Visit? (2026 Comparison) | tabiji.ai`
- [ ] Canonical URL correct: `https://tabiji.ai/compare/<slug>/`
- [ ] OG image points to actual R2 image
- [ ] GA4 tag present (`G-D7QHNRXLHJ`)
- [ ] Validates: `python3 generators/compare/build_compare.py validate`

### Images
- [ ] 4+ images on R2 at `img.tabiji.ai/compare/<slug>/`
- [ ] Hero photo grid has 2 images (dest1.jpg, dest2.jpg)
- [ ] hero.jpg exists for social sharing
- [ ] All images optimized (800px wide, JPEG ~80%)

### Index & API
- [ ] `compare/inventory.json` updated
- [ ] `api/v1/compare/<slug>.json` created
- [ ] `sitemap.xml` updated with new URL

## Common Mistakes to Avoid

- **Don't hand-write HTML** — always generate via `build_compare.py build` from compare-data JSON
- **Don't skip Reddit research** — the brand is "Reddit-backed, not AI filler"
- **Don't forget R2 upload** — images go to R2, not git. Dead image links = broken page
- **Don't use generic verdicts** — "Both are great!" is not a verdict. Pick a side
- **Don't skip finalize** — every new page needs inventory, API, sitemap updates

## Related Files
- Content generator: `scripts/batch-compare-gen.py`
- Reddit research: `scripts/reddit_research.py`
- Photo pipeline: `scripts/add_compare_photos.py`
- Enrichment: `generators/compare/enrich_compare.py`
- HTML builder: `generators/compare/build_compare.py`
- Shell template: `scripts/compare-shell-template.json`
- Compare queue: `compare-queue.json`
- Inventory: `compare/inventory.json`
- Photo pipeline docs: `docs/photo-pipeline.md`
- Full runbook: `docs/compare-page-runbook.md`
