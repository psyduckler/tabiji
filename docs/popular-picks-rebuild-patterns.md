# Popular Picks Rebuild - Known Issues & Patterns

**Created:** 2026-04-12  
**Context:** Audit of 291 "completed" pages from the 2026-04-11 broken pages fix batch

## Issues Found During Audit

### Critical Issues (require full rebuild)

1. **Empty Body (13 pages)**
   - JSON-LD schema in `<head>` has full venue data
   - HTML body has 0 `<section class="restaurant-section">` elements
   - Pages: austin-fine-dining, baltimore-coffee-shops, bangkok-street-food, bilbao-guggenheim, chicago-art-galleries, chicago-fine-dining, le-morne-snorkeling, london-afternoon-tea, london-sunday-roast, los-angeles-ramen, new-york-korean-bbq, san-juan-mofongo, singapore-craft-beer

2. **Partial Body / One-Section Bug (6 pages)**
   - Original template bug persists: only 1 venue renders
   - H1 claims 12+ venues, body has 1
   - Pages: ayutthaya-street-food, da-nang-coffee-shops, hua-hin-seafood-restaurants, kota-kinabalu-seafood, lisbon-natural-wine-bars, singapore-laksa

### Issues Fixed in This Batch

1. **Duplicate #1 Bug (181 pages)**
   - **Pattern:** Partial leftover section from original broken page between `<section class="pick-list">` and `<!-- VENUE 1 -->` comment
   - **Cause:** Rebuild script appended new content but didn't remove partial old content
   - **Fix:** Remove content between `<section class="pick-list">` and `<!-- VENUE 1 -->`

2. **Entire Venue List Duplicated (3 pages)**
   - **Pattern:** Full VENUE 1-10 list appears twice
   - **Pages:** portland-food-carts, st-louis-ribs, osaka-takoyaki
   - **Fix:** Remove duplicate venue list section

3. **H1 Count Mismatch (46 pages)**
   - **Pattern:** H1 says "X Best..." but body has Y venues (usually Y > X)
   - **Cause:** Rebuild added more venues than H1 claimed
   - **Fix:** Update H1 number to match actual venue count

4. **Wrong Source Attribution (233 pages)**
   - **Pattern:** "NYC food discussion" appears in non-NYC pages
   - **Cause:** Template placeholder not replaced with city-specific source
   - **Fix:** Replace with "Local food community" or city-specific subreddit

5. **Broken Anchor Links (252 pages)**
   - **Pattern:** Sidebar legend `href="#X"` doesn't match section `id="Y"`
   - **Cause:** Legend generated from map config anchorIds, sections have different IDs
   - **Fix:** Update legend hrefs to match actual section IDs by rank number

6. **Unicode Escapes (31 pages)**
   - **Pattern:** `\uXXXX` sequences in HTML text instead of rendered characters
   - **Cause:** JSON encoding leaked into HTML
   - **Fix:** Decode \u sequences to actual UTF-8 characters (skip surrogates)

7. **Empty Map Picks Array (2 pages)**
   - **Pattern:** `"picks": []` in `__POPULAR_PICKS_MAP__` config
   - **Cause:** Rebuild didn't generate map coordinates
   - **Fix:** Research and populate coordinates for each venue

8. **Zero Venue Coordinates (143 pages)**
   - **Pattern:** `data-map-lat="0"` in venue section HTML
   - **Note:** Cosmetic issue - map still works from picks array
   - **Impact:** Low priority, map functionality unaffected

## Patterns for Cron Job Rebuild Script

### Pre-rebuild Checks
1. Verify source page has JSON-LD ItemList schema to salvage venue data
2. Check if page already has partial content (one-section bug signature)
3. Detect if map config has real coordinates vs zeros

### During Rebuild
1. **CRITICAL:** Remove ALL content between `<section class="pick-list">` and first venue before inserting new content
2. Generate venue section IDs consistently (slugify venue name)
3. Use same ID in both section `id=""` and sidebar legend `href="#"`
4. Ensure H1 count matches actual venue count
5. Use city-specific source attribution, not generic "NYC food discussion"
6. Render unicode characters properly, don't escape to \uXXXX

### Post-rebuild Validation
1. Count `<section class="restaurant-section">` - must match H1 claim
2. Count `class="restaurant-number">1<` - must be exactly 1
3. Verify no `<!-- VENUE 1 -->` appears before actual first venue section
4. Check map picks array is populated with real coordinates
5. Verify sidebar legend anchors match section IDs

### Map Coordinate Sources
- Primary: Google Maps CID from original page JSON-LD (has real lat/lng)
- Fallback: OpenStreetMap search
- Fallback: Address geocoding via nominatim

## Statistics

| Issue | Count | Status |
|-------|-------|--------|
| Duplicate #1 | 181 | Fixed |
| Duplicate venue list | 3 | Fixed |
| H1 mismatch | 46 | Fixed |
| Wrong source | 233 | Fixed |
| Broken anchors | 202 | Fixed |
| Unicode escapes | 17 | Fixed |
| Empty map | 2 | Fixed |
| Empty body (P1) | 13 | Unchecked, needs rebuild |
| Partial body (P2) | 6 | Unchecked, needs rebuild |

**Total pages audited:** 291  
**Pages successfully fixed:** 272  
**Pages returned to queue:** 19
