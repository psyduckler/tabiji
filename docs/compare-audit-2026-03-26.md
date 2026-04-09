# Compare Pages Audit — March 26, 2026

**Auditor:** Psy (subagent)  
**Date:** 2026-03-26  
**Pages audited:** 90 (85 from batch commit `581341ce1` + 5 individual builds)  
**Individual builds checked:** portugal-vs-spain, colombia-vs-mexico, japan-vs-thailand, greece-vs-italy, vietnam-vs-indonesia

---

## Summary

| Check | Result | Pass | Fail | Notes |
|-------|--------|------|------|-------|
| HTML structure (all sections present) | ✅ PASS | 90/90 | 0 | |
| Schema markup (Article, BreadcrumbList, FAQPage) | ✅ PASS | 90/90 | 0 | All valid JSON |
| Meta tags (canonical, og:url, og:image) | ✅ PASS | 90/90 | 0 | |
| GA4 tracking (G-D7QHNRXLHJ) | ✅ PASS | 90/90 | 0 | |
| Viator affiliate links (correct PID/MCID) | ✅ PASS | 90/90 | 0 | |
| Content uniqueness (no cross-page duplication) | ✅ PASS | 90/90 | 0 | |
| FAQ uniqueness per page | ✅ PASS | 90/90 | 0 | |
| inventory.json presence | ✅ PASS | 90/90 | 0 | |
| API JSON files present | ✅ PASS | 90/90 | 0 | |
| Compare-data JSON files present | ✅ PASS | 90/90 | 0 | |
| Section consistency (H2 count) | ✅ PASS | 90/90 | 0 | All have exactly 16 H2s |
| FAQ item count | ✅ PASS | 90/90 | 0 | All have exactly 8 FAQ items |
| HTML validity | ✅ PASS | 90/90 | 0 | |
| Word count adequacy (>1000 words) | ✅ PASS | 90/90 | 0 | Range: 2,836–4,237 |
| Inline destination images (dest1.jpg, dest2.jpg) | ❌ FAIL | 0/90 | 90 | All 404 |
| OG hero image (hero.jpg) | ❌ FAIL | 0/90 | 90 | All 404 |
| Live page accessibility | ⚠️ PARTIAL | 89/90 | 1 | vietnam-vs-indonesia 404 |
| CSS template cleanliness | ℹ️ INFO | — | — | Unused ishigaki/miyako rules |

**Overall health: 89/90 pages live, all pass structural/content/schema checks. Two image issues affecting all pages.**

---

## Issues Found

### 🔴 CRITICAL

#### 1. Destination images missing on all 90 pages
**Affected pages:** All 90  
**Pattern:** Each page contains a `photo-grid` section with two `<img>` tags pointing to:
- `https://img.tabiji.ai/compare/<slug>/dest1.jpg`
- `https://img.tabiji.ai/compare/<slug>/dest2.jpg`

All of these return HTTP 404. These images appear in the middle of the article body (after the verdict box) and render as broken image icons for every visitor.

**Evidence:**
```html
<div class="photo-grid">
  <div>
    <img alt="Amsterdam travel destination" loading="lazy" src="https://img.tabiji.ai/compare/amsterdam-vs-copenhagen/dest1.jpg">
    <div class="caption">Amsterdam</div>
  </div>
  <div>
    <img alt="Copenhagen travel destination" loading="lazy" src="https://img.tabiji.ai/compare/amsterdam-vs-copenhagen/dest2.jpg">
    <div class="caption">Copenhagen</div>
  </div>
</div>
```

Verified via `curl -sI` for: amsterdam-vs-copenhagen, bangkok-vs-bali, tokyo-vs-paris, vietnam-vs-indonesia, portugal-vs-spain, greece-vs-italy, japan-vs-thailand, colombia-vs-mexico, bora-bora-vs-maldives — all return 404.

**Note:** This is an existing gap across all compare pages, not specific to today's batch. Older pages (e.g., cairo-vs-marrakech) also have 404 dest images. Pages built before ~March 8 used named images (e.g., `london-tower-bridge.jpg`) which *are* uploaded and working.

**Fix:** Generate/upload `dest1.jpg` and `dest2.jpg` for all 90 pages to R2 at `img.tabiji.ai/compare/<slug>/`.

---

#### 2. OG image (hero.jpg) missing on all 90 pages
**Affected pages:** All 90  
**Pattern:** All meta og:image tags point to `https://img.tabiji.ai/compare/<slug>/hero.jpg`, which returns 404 for all new batch pages.

This means social previews (Twitter/X cards, Facebook/LinkedIn link shares, Slack unfurls) will show broken/no image for every compare page in this batch.

**Note:** Pages built before the batch style was introduced (e.g., london-vs-amsterdam) use named images in og:image and *do* work. The hero.jpg naming convention was introduced for batch builds but images haven't been generated or uploaded.

**Fix:** Generate hero images and upload to R2 as `img.tabiji.ai/compare/<slug>/hero.jpg` for all 90 pages.

---

### 🟡 WARNING

#### 3. vietnam-vs-indonesia returns 404 on production
**Affected pages:** 1 (vietnam-vs-indonesia)  
**Live check:** `https://tabiji.ai/compare/vietnam-vs-indonesia/` → HTTP 404

The files exist locally and are tracked in git (committed in commit `c25b88436` alongside popular-picks: muscat-restaurants). All supporting files present:
- `compare/vietnam-vs-indonesia/index.html` ✅
- `api/v1/compare/vietnam-vs-indonesia.json` ✅  
- `compare-data/vietnam-vs-indonesia.json` ✅

The other 4 individual builds (portugal-vs-spain, colombia-vs-mexico, japan-vs-thailand, greece-vs-italy) are all live and return 200.

**Likely cause:** Deployment didn't include this page, possibly because it was committed in a mixed commit (popular-picks + compare) and the deploy may have had an issue, or Cloudflare Pages cache hasn't propagated.

**Fix:** Redeploy or force a cache purge for this specific page. If it still 404s, re-commit the file with a dedicated compare commit.

---

### 🔵 INFO

#### 4. Unused template CSS in all 90 pages
**Affected pages:** All 90  
**Pattern:** All pages include CSS rules for classes that are never used in their HTML bodies:
```css
.edge-ishigaki { color: var(--indigo); font-weight: 700; }
.edge-miyako { color: var(--terracotta); font-weight: 700; }
.edge-tie { color: var(--earth); font-weight: 600; }
.decision-card.ishigaki-card { ... }
.decision-card.miyako-card { ... }
```

These appear to be CSS rules from the Ishigaki vs Miyako comparison template (Japanese islands) that leaked into the shared CSS used by all new batch pages. The HTML body of these pages does NOT use these class names — so there is no visual rendering issue. It's dead CSS.

**Impact:** Minor (~200 bytes of CSS per page × 90 pages = negligible). Does not affect rendering or SEO. 

**Fix:** Remove these CSS rules from the shared CSS template in the compare builder (`build_compare.py` or equivalent).

---

#### 5. Naming inconsistency: st-barts-vs-st-lucia
**Affected pages:** 1 (st-barts-vs-st-lucia)  
**Pattern:** The page title and content use "St. Lucia" (with period) which is the correct geographic name. The slug uses "st-lucia" (no period). This is expected and correct — it's not a real issue.

One minor note: the page title reads "St Barts vs St. Lucia" — "St Barts" has no period while "St. Lucia" does. For perfect consistency, either both should have periods or neither should.

---

## Structural/Content Spot Check

Pages manually reviewed for content accuracy:
- **amsterdam-vs-copenhagen**: Correct verdicts, Amsterdam wins on cost vs Copenhagen slightly pricier. Balanced.
- **tokyo-vs-paris**: Detailed comparison table with sensible winners per category (Tokyo: safety, transport, food; Paris: architecture, day trips). Cost figures reasonable ($150-$250/day Tokyo).
- **bora-bora-vs-maldives**: Luxury cost figures appropriate ($1,000-$3,000/night for overwater villas). Both destinations correctly described.
- **vietnam-vs-indonesia**: Budget-tier costs accurate ($35-$50/night), both destinations well-differentiated.
- **nairobi-vs-cape-town**: Safari vs cosmopolitan split handled correctly, costs in right range.
- **bogota-vs-cartagena**: Climate difference (cool vs hot) correctly flagged as key differentiator.
- **moscow-vs-st-petersburg**: Correctly notes safety/visa considerations for current travel climate.

All sampled pages: no destination mix-ups, no implausible cost figures, no placeholder text, no cross-contamination between pages.

---

## Consistency Check

All 90 pages are perfectly consistent on:
- **H2 sections:** Exactly 16 per page
- **FAQ items:** Exactly 8 per page
- **Viator links:** Exactly 23 Viator references per page, all with correct PID (P00292930) and MCID (42383)
- **Word count:** 2,836–4,237 words (avg 3,511). No outliers suggesting truncation.
- **File size:** 61–72KB. Healthy range.
- **Schema types:** Article + BreadcrumbList + FAQPage in all pages.

Section headers present in all pages:
- How we built this comparison (methodology)
- ⚡ The TL;DR Verdict
- Quick Comparison (comparison table)
- 💰 Costs & Budget
- ✈️ Getting There & Around
- 🏨 Accommodation
- 🍽️ Food & Drink Scene
- 🍻 Nightlife & Entertainment
- 🎨 Culture & Museums
- ✨ Unique Vibe & Atmosphere
- 🌲 Day Trips & Nature
- ☀️ Best Time to Visit (Weather)
- 🚶 Solo Travel & Safety
- ❓ FAQs
- CTA section
- Viator section

---

## Recommendations

### Immediate (before indexing this batch)

1. **Generate and upload dest1.jpg + dest2.jpg** for all 90 pages to `img.tabiji.ai/compare/<slug>/`. These are the main article images and currently broken for all users. Consider using SerpAPI Google Images to find real destination photos, or generate with Nano Banana Pro / Gemini Imagen.

2. **Generate and upload hero.jpg** for all 90 pages to `img.tabiji.ai/compare/<slug>/`. These are the social sharing preview images (og:image). Without them, all social shares look broken.

3. **Investigate vietnam-vs-indonesia 404** on production. Check Cloudflare Pages deploy logs. If not self-resolving, redeploy.

### Medium-term

4. **Fix the dead CSS** in the compare builder — remove `.edge-ishigaki`, `.edge-miyako`, `.ishigaki-card`, `.miyako-card` CSS rules from the shared template. These shouldn't be in pages that don't use those class names.

5. **Standardize image naming convention** across all compare pages. Currently a mix of `hero.jpg` (new batch) and named images like `amsterdam-canal.jpg` (older pages). The named-image approach is better for SEO (descriptive filenames) but creates more work per page. Document which approach is canonical in `ARCHITECTURE.md`.

6. **Add image generation to the batch build pipeline.** The `batch-compare-gen.py` script should either generate images as part of the build or flag that images need to be created before pages go live.

---

*Audit completed: 2026-03-26. 90 pages checked. Shell commands used for batch analysis; ~20 pages spot-checked for content quality.*
