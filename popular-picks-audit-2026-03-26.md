# Popular-Picks Audit Report — 2026-03-26

**Auditor:** Subagent automated audit  
**Date:** 2026-03-26  
**Pages audited:** 12 most recent pages (Mar 25–26, 2026)  
**Total popular-picks pages:** 762

---

## Summary

| Check | Result | Pages Affected |
|---|---|---|
| HTML structure (doctype, head, body) | ✅ PASS | All 12 |
| JSON-LD schemas (Article, ItemList, FAQPage, TouristTrip, BreadcrumbList) | ✅ PASS | All 12 |
| Schema JSON validity | ✅ PASS | All 12 |
| Meta tags (title, description, canonical, og:, twitter:) | ✅ PASS | All 12 |
| Hero images (og:image, place photos) | ❌ FAIL | All 12 — 404 |
| Individual place photos | ❌ FAIL | All 12 — all use hero-bg.jpg |
| Viator affiliate section (body HTML) | ❌ FAIL | All 12 — missing |
| Related links section (body HTML) | ❌ FAIL | All 12 — missing |
| Speakable schema | ❌ FAIL | All 12 — missing |
| Google Maps CID links per place | ❌ FAIL | All 12 — missing |
| Place-level Google ratings + review counts | ⚠️ PARTIAL | All 12 — missing from HTML |
| H1 phrasing quality | ⚠️ WARNING | 10/12 — "12 Best X's Y" phrasing |
| Content accuracy (places real, correct city) | ✅ PASS | Verified sample |
| Duplicate content across pages | ✅ PASS | None found |
| Methodology section | ✅ PASS | All 12 |
| FAQ section (6 questions) | ✅ PASS | All 12 |
| BreadcrumbList schema present | ✅ PASS | All 12 |
| Viator PID/MCID in affiliate links | N/A | No links present |

**Pass:** 9/18 checks  
**Fail:** 7/18 checks  
**Warning:** 2/18 checks

---

## Issues Found

### 🔴 CRITICAL

#### 1. All 12 place images are 404
**Pages:** All 12  
**Details:** Every place card (`restaurant-section`) uses `https://img.tabiji.ai/popular-picks/{slug}/hero-bg.jpg` as its photo. This file does not exist on the CDN (HTTP 404 confirmed via `curl`). The same URL is used for:
- Every individual place photo (12 per page × 12 pages = 144 broken images)
- `og:image` (social sharing preview will be broken)
- `twitter:image`
- Article schema `image` field

This means social sharing cards will show no image, and all place photos on the page are broken.

**Root cause:** The `gen_popular_picks_batch.py` generator hardcodes `hero-bg.jpg` for all place photos (line 127) and no upload step was run for these 12 new pages. The file was never uploaded to R2/CDN.

**Scope:** Affects ~162 pages total (not just these 12) based on full-site scan — all pages built after the generator template was introduced with `hero-bg.jpg` placeholder.

---

#### 2. Viator affiliate section missing from all 12 pages
**Pages:** All 12  
**Details:** The `<section class="viator-section">` block is completely absent from the body HTML of all 12 new pages. The CSS for `.viator-section` is present in `<style>` (it's part of the shared CSS template) but the actual HTML content is never injected.

For comparison: pages built Mar 22 (e.g., `budapest-ruin-bars`, `barcelona-brunch`) have working viator sections with correct PID `P00292930` and MCID `42383`.

**Root cause:** The `gen_popular_picks_batch.py` generator template does not include viator section generation. The Mar 25 template update (`1d8bcbb1`) patched 141 existing pages via `add_pp_sections.py`, but new pages built after 08:39 on Mar 25 were generated from the unpatched template.

**Revenue impact:** These 12 pages generate no Viator affiliate clicks. Combined, that's 12 pages × ~144 Viator card impressions/mo with zero conversion.

---

#### 3. Related links section missing from all 12 pages
**Pages:** All 12  
**Details:** No `<section class="related-section">` in body HTML. The compare/related links section (which links to `/compare/` pages and related `/popular-picks/` pages) is entirely absent. This hurts internal linking, SEO juice distribution, and time-on-site.

**Root cause:** Same as viator issue — generator template was not updated.

---

### 🟡 WARNING

#### 4. No individual place photos (all use hero-bg.jpg)
**Pages:** All 12 (also ~162 pages total)  
**Details:** Older pages (e.g., `budapest-ruin-bars`) have unique photos per place (e.g., `szimpla-kert.jpg`, `vittula.jpg`). All 12 new pages reuse `hero-bg.jpg` for every single place card. Even if the hero image were uploaded, showing the same photo 12 times on a page is poor UX and may hurt engagement.

**Example:** On `oslo-restaurants`, every one of 12 places shows the same Oslo hero image, making the visual grid look like a template artifact.

---

#### 5. No Google Maps CID links per place
**Pages:** All 12  
**Details:** Older pages (e.g., `oslo-seafood-restaurants`, `budapest-ruin-bars`) have `data-map-cta-url` and `data-map-query` attributes on each place section, including CID-based Google Maps links like:
```
https://www.google.com/maps/place/?q=place_id:ChIJZz...
```
The 12 new pages have only a generic Google Maps iframe embed for the whole city — no per-place navigation links. Users can't click through to a specific restaurant on Maps from these pages.

---

#### 6. No per-place Google ratings and review counts in HTML
**Pages:** All 12  
**Details:** Older pages display `★ 4.6 · 71,528 reviews` via `<span class="google-rating">`. The new pages have the `.google-rating` CSS class defined but never used in the body — no star ratings, no review counts are shown. The only per-place data shown is neighborhood and price range.

This is a trust and quality signal difference compared to older pages.

---

#### 7. Speakable schema missing
**Pages:** All 12  
**Details:** The Mar 25 template update (`42b21128a`) added speakable schema to existing pages alongside BreadcrumbList. New pages have BreadcrumbList (from the generator) but not speakable. BreadcrumbList is implemented correctly in JSON-LD.

---

#### 8. Awkward H1 phrasing (10/12 pages)
**Pages:** muscat-seafood, beirut-street-food, beirut-nightlife, gothenburg-seafood, helsinki-restaurants, oslo-restaurants, yerevan-restaurants, zagreb-restaurants (conditional), tallinn-old-town-restaurants  
**Details:** H1 and headline schema use constructions like:
- `"12 Best Muscat's Fresh Seafood"` (grammatically awkward)
- `"12 Best Beirut's Street Food Scene"` (same issue)
- `"12 Best Gothenburg's Seafood Culture"` (same)
- `"12 Best Helsinki's Food Scene"` (same)
- `"12 Best Oslo's New Nordic Restaurant Scene"` (same)

The generator prompt instructs: `"N Best {title.replace('Best ', '').replace('best ', '')}"` which strips "Best" from titles that already contain it, but doesn't handle possessive/genitive city names. Older pages have proper H1s like `"18 Best Ruin Bars in Budapest"` or `"12 Best Seafood Restaurants in Oslo"`.

Good: `reykjavik-craft-beer` ("12 Best Reykjavik Craft Beer Bars") and `zagreb-restaurants` ("The 12 Best Restaurants in Zagreb Right Now") have clean phrasing.

---

### 🔵 INFO

#### 9. BreadcrumbList last item missing `item` URL (inconsistent with some older pages)
**Pages:** All 12  
**Details:** The BreadcrumbList schema's last item (current page) has `name` but no `item` URL. This is technically valid per Schema.org spec (current page URL is optional for the last breadcrumb), and most older pages do the same. However, `oslo-seafood-restaurants` does include it. Minor inconsistency.

#### 10. Gothenburg-seafood includes Hönö Klåva location (archipelago, ~30km away)
**Pages:** gothenburg-seafood  
**Details:** `Tullhuset` is listed in `Hönö Klåva (Archipelago)` — Hönö is an island ~30km from Gothenburg, requiring a ferry. This is a debatable inclusion for a city guide. Mention in description that it requires travel if kept.

#### 11. Oslo-restaurants includes a coffee chain (Stockfleths)
**Pages:** oslo-restaurants  
**Details:** Stockfleths is a multi-location Oslo coffee chain. It's the #12 entry in a "New Nordic Restaurant Scene" guide. While it has Nordic credentials, it's arguably off-category. Not a hard error but dilutes the restaurant focus.

#### 12. All places in Reykjavik-craft-beer are in Miðbær (10/12)
**Pages:** reykjavik-craft-beer  
**Details:** 10 of 12 bars are in the same neighborhood. This is plausibly accurate for Reykjavik's small, walkable center, but worth noting as potential over-concentration.

#### 13. Map embed uses generic title search (not per-place markers)
**Pages:** All 12  
**Details:** The sidebar map uses `maps/embed/v1/search?q={page title}+{city}` — a generic search, not pins for individual places. This works but is less useful than per-place markers on older pages. The newer generator doesn't include per-place coordinates.

---

## Template Comparison: Old vs New

| Feature | Old pages (pre-Mar 19) | Mar 22 pages (Budapest/Barcelona) | 12 New pages (Mar 25–26) |
|---|---|---|---|
| Unique place photos | ✅ Per-place JPEGs | ✅ Per-place JPEGs | ❌ hero-bg.jpg (404) |
| Google ratings + reviews | ✅ In HTML | ✅ In HTML | ❌ CSS only, not in HTML |
| Google Maps CID per place | ✅ Yes | ✅ Yes | ❌ No |
| Viator section | ❌ No | ✅ Yes | ❌ No |
| Related links section | ❌ No | ✅ Yes | ❌ No |
| BreadcrumbList schema | ❌ No | ✅ Yes | ✅ Yes |
| Speakable schema | ❌ No | ✅ Yes | ❌ No |
| Methodology section | ✅ Yes | ✅ Yes | ✅ Yes |
| FAQ section | ✅ Yes | ✅ Yes | ✅ Yes |

---

## Recommendations

### Priority 1 — Immediate (before more pages are built)

1. **Fix the generator** (`gen_popular_picks_batch.py`): 
   - Add viator section generation (reuse `inject-viator-section.py` logic)
   - Add related links section generation
   - Add speakable schema
   - Fix H1 phrasing template to produce natural language (e.g., `"N Best [category] in [city]"`)
   - Optionally: add Google Places data lookup per venue (ratings, CID maps links)

2. **Run `add_pp_sections.py` / `inject-viator-section.py` on all 12 new pages** to retroactively add viator + related sections.

3. **Upload hero-bg.jpg images for all 12 new pages** to R2/CDN, or switch to a different placeholder image strategy. Also consider uploading individual place photos (or using a photo-fetching step in the generator).

### Priority 2 — Medium Term

4. **Run the inject/patch scripts on all ~160 pages** that are missing viator/related sections (full audit shows ~160/762 pages affected — all built with the new generator template).

5. **Fix the individual place photo pipeline** — the generator should either:
   a. Include a step to fetch/upload per-place photos from SerpAPI/Google Images, OR
   b. Use a city-level fallback image that actually exists on the CDN (not hero-bg.jpg)

6. **Add per-place Google Maps links** — the `google-places-api-key` is available to fetch `place_id` + `googleMapsUri` during generation.

### Priority 3 — Quality

7. **Review H1 phrasing** for the 10 affected pages and update to natural language titles.

8. **Consider adding Google ratings to HTML** for the 12 new pages — the `enrich-popular-picks.py` script likely handles this.

9. **Content review**: `oslo-restaurants` includes a coffee chain (Stockfleths) as a restaurant recommendation — consider replacing with a more appropriate restaurant entry.

---

## Files Audited

| Page | Build Date | Structural | Schema | Images | Viator | Related |
|---|---|---|---|---|---|---|
| tallinn-old-town-restaurants | 2026-03-25 18:23 | ✅ | ✅ | ❌ 404 | ❌ | ❌ |
| zagreb-restaurants | 2026-03-25 18:37 | ✅ | ✅ | ❌ 404 | ❌ | ❌ |
| yerevan-restaurants | 2026-03-25 18:52 | ✅ | ✅ | ❌ 404 | ❌ | ❌ |
| split-old-town-food | 2026-03-25 19:26 | ✅ | ✅ | ❌ 404 | ❌ | ❌ |
| oslo-restaurants | 2026-03-25 20:37 | ✅ | ✅ | ❌ 404 | ❌ | ❌ |
| helsinki-restaurants | 2026-03-25 21:40 | ✅ | ✅ | ❌ 404 | ❌ | ❌ |
| bergen-hiking-cafes | 2026-03-25 23:40 | ✅ | ✅ | ❌ 404 | ❌ | ❌ |
| reykjavik-craft-beer | 2026-03-26 01:38 | ✅ | ✅ | ❌ 404 | ❌ | ❌ |
| gothenburg-seafood | 2026-03-26 04:34 | ✅ | ✅ | ❌ 404 | ❌ | ❌ |
| beirut-nightlife | 2026-03-26 08:06 | ✅ | ✅ | ❌ 404 | ❌ | ❌ |
| beirut-street-food | 2026-03-26 10:41 | ✅ | ✅ | ❌ 404 | ❌ | ❌ |
| muscat-seafood | 2026-03-26 11:43 | ✅ | ✅ | ❌ 404 | ❌ | ❌ |

---

## Template Update Status (Mar 25)

| Update | Commit | Applied to existing pages | Applied to 12 new pages |
|---|---|---|---|
| BreadcrumbList schema | `42b21128` (08:38) | ✅ Yes | ✅ Yes (generator includes it) |
| Speakable schema | `42b21128` (08:38) | ✅ Yes | ❌ No (generator missing) |
| Methodology section | `1d8bcbb1` (08:39) | ✅ Yes | ✅ Yes (generator includes it) |
| Viator section | `1d8bcbb1` (08:39) | ✅ Yes (141 pages) | ❌ No (generator missing) |
| Related links section | `1d8bcbb1` (08:39) | ✅ Yes (141 pages) | ❌ No (generator missing) |

All 12 new pages were committed after 18:23 (after the template updates at 08:38–08:39), but the generator script was not updated to include the new sections. This is the root cause of the missing viator/related/speakable sections.
