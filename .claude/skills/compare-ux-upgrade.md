---
name: compare-ux-upgrade
description: Apply the full 13-point UX upgrade to a compare page, transforming it from a reading experience into a decision-making tool
user_invocable: true
---

# Compare Page UX Upgrade

Apply all 13 UX improvements to a tabiji.ai compare page. This transforms the page from a linear article into an interactive decision-making tool.

## When to use
- When creating a new compare page
- When upgrading an existing compare page to the new UX format
- Reference implementation: `/compare/madrid-vs-barcelona/index.html`

## Required input
The user provides a compare page slug (e.g., `chile-vs-argentina`). The existing page HTML at `/compare/{slug}/index.html` contains all the raw content needed.

## The 13 UX components to add

### 1. "What matters to you?" filter tags
Interactive tag buttons after the hero that scroll to relevant deep-dive sections.
- Tags map to section IDs: Budget, Food, Beaches, Nightlife, Culture, Safety, Day Trips, Weather
- JS: `filterJump(btn)` — removes active from all, adds to clicked, scrolls to section, auto-opens if collapsed

### 2. Trip personalization widget
Three pill-group rows: travel style (Solo/Couple/Family/Friends), budget (Backpacker/Mid-range/Luxury), priority (Food/Culture/Beaches/Nightlife).
- Generates a personalized recommendation from a lookup table
- Need 15-25 unique recommendations per page based on the destinations
- Use Gemini/Claude to generate recommendations specific to the two destinations

### 3. Visual scorecard
Color-coded horizontal bars showing relative strength per category.
- Extract winners from each deep-dive section's verdict
- Assign bar percentages (winner gets 80-95%, loser gets 40-65%, tie both get 75-85%)
- Count total wins per destination for the overall score
- CSS: `.sc-bar-wrap` and `.sc-bar` MUST have `display:block` (they're spans)

### 4. Quick answer cards
6 cards answering the most common search queries for the comparison.
- Extract from FAQ items + deep-dive verdicts
- Each card: question, 1-sentence answer, winner badge (dest1/dest2/tie)
- Link to the relevant deep-dive section

### 5. Collapsible deep-dive sections
Convert each `<section class="deep-dive">` to accordion format.
- Add `dd-header` with h2 + winner badge + toggle arrow
- Add `dd-summary` (1-sentence teaser from the verdict)
- Wrap content in `dd-body > dd-content`
- First section and Decision Framework default to `class="open"`
- JS: `toggleSection(el)` toggles `.open` class
- NOTE: Use `addEventListener` not inline `onclick` (Cloudflare Rocket Loader blocks inline handlers)

### 6. Side-by-side photo pairs
In key deep-dive sections (City Character, Architecture, Neighborhoods), add:
```html
<div class="photo-pair">
  <div><img src="..." alt="..." loading="lazy"><p class="photo-caption">...</p></div>
  <div><img src="..." alt="..." loading="lazy"><p class="photo-caption">...</p></div>
</div>
```
Use existing page images (hero.jpg, dest1.jpg, dest2.jpg) or section-specific images.

### 7. Cost comparison widget
Structured table with line items: Hostel, Hotel, Menu/meal, Beer, Metro, Coffee, Daily total.
- Extract cost data from the Cost Comparison deep-dive section
- Add a savings callout bar at the bottom

### 8. Weather/climate chart
12-month temperature grid with best/avoid month highlighting.
- Extract from Best Time to Visit section or use Open-Meteo data
- Highlight best months (class="best") and avoid months (class="avoid")
- Color-code temps per destination

### 9. "Travelers also compared" cards
3 related comparison cards with images at the bottom.
- Pull from the page's related comparisons or inventory.json `relatedSlugs`
- Each card: image, title, 1-line description, search volume if available
- Verify image URLs exist (use dest1.jpg/dest2.jpg/hero.jpg patterns)

### 10. Sticky score ticker
A thin bar below the nav showing "Dest1 X — Y Dest2 | Current section".
- `position:sticky; top:64px` (nav is ~64px tall)
- Hidden by default, appears when hero scrolls out of view
- Updates current section name on scroll

### 11. Mobile jump-to-verdict button
Floating button on mobile: "Jump to Verdict".
- Shows after 400px scroll, hides when verdict is visible
- `position:fixed; bottom:1.25rem; right:1.25rem`

### 12. Remove duplicate Decision Framework
Many pages have two nearly identical Decision Framework sections. Merge into one clean card-based version using `decision-grid` layout.

### 13. Remove sports/soccer quotes
Filter out Reddit quotes that contain match scores, goal notifications, or sports content. Pattern: quotes containing "Goal!", scorelines like "1-0", "2-1", match thread references.

## CSS variables for destination colors
```css
--madrid: #C0392B;  /* or --dest1 */
--barcelona: #2E86C1; /* or --dest2 */
```
Assign warm color (red/terracotta) to dest1, cool color (blue/teal) to dest2.

## Critical CSS notes
- `.sc-bar-wrap` and `.sc-bar` need `display:block` (they're `<span>` elements)
- `.toc-mobile-sticky` and `.score-ticker` need `top:64px` (not 56px — nav is 64px tall)
- All interactive JS should use `addEventListener` in a `<script>` block at page bottom, NOT inline `onclick` attributes (Cloudflare Rocket Loader prepends blocking code to inline handlers)

## Step-by-step process

1. **Read the existing page** at `compare/{slug}/index.html`
2. **Extract data** from existing content:
   - Destination names from h1/hero
   - Winner per category from verdict/section-winner blocks
   - Cost data from Cost Comparison section
   - FAQ items from faq-section
   - Image URLs from existing img tags
   - Related comparison slugs from inventory or related-comparisons section
3. **Generate page-specific content** (use AI):
   - 15-25 personalization recommendations for the trip widget
   - Quick answer card text (6 cards)
   - 1-sentence summary for each collapsible section
   - Weather data (if not in existing page)
4. **Rewrite the page** using the madrid-vs-barcelona template as reference
5. **Verify**:
   - All internal links work
   - All images load (curl -sI to check)
   - Schema JSON-LD is valid
   - No duplicate Decision Framework sections
   - No sports quotes
6. **Commit, push, PR, merge**

## Reference implementation
The canonical example is `/compare/madrid-vs-barcelona/index.html`. Use it as the HTML/CSS template. The CSS block in that page contains all styles needed for the 13 components.
