---
name: popular-picks-article-builder
description: Build a complete popular-picks article from scratch — research via web search, build full HTML page with schema/maps/photos, add to country hub, and deploy. Trigger when user says "build [slug]" or "create article for [slug]" for a popular-picks page.
user_invocable: true
---

# Popular Picks Article Builder

Build a complete tabiji.ai popular-picks article from research to deployment.

## When to use
- When creating a new popular-picks page from the master queue
- When the user says "build [slug]" or "create [city]-[food]" for a popular-picks page
- When batch-building multiple articles from the queue

## Required input
A slug from `popular-picks-master-queue.json` (e.g., `detroit-pizza`, `paris-banh-mi`, `kyoto-sushi`).

The queue file contains: slug, city, country, category, keyword, search_volume.

## Template
The reference implementation is `/popular-picks/detroit-pizza/index.html`. ALL new pages must follow this exact HTML structure, CSS, JavaScript, and schema markup.

## Full Workflow (7 steps)

### Step 1: Research (Web Search)

Search for the top 10 spots using multiple queries:

```
"best [food] [city] top restaurants locals recommend 2025 2026"
"best [food] [city] [specific style] recommendations"
"[city] [food] guide address rating hours"
```

For each of the 10 picks, gather:
- Full name
- Address + neighborhood
- Google rating + review count
- Price range (use local currency: $, €, £, ¥, ฿, ₹, S$)
- Phone number
- Website URL
- Google Maps URL or search query
- Latitude/longitude (approximate from address)
- Opening hours
- Cuisine tags / style descriptors
- What to order (signature dish)
- Insider tip
- Verdict (1-2 sentences on why it made the list)
- 2 Reddit-style quotes with attribution

Also research:
- City-specific food context (history, culture, neighborhoods)
- 8 FAQ questions + answers
- Related tabiji pages (check what exists in popular-picks/ and compare/)

### Step 2: Build the HTML Page

Create `popular-picks/[slug]/index.html` following the EXACT template from `popular-picks/detroit-pizza/index.html`.

**CRITICAL RULES:**
1. Use actual UTF-8 emoji characters (🍕 📍 💴 🕐 📞 🌐 📌 🎟️) — NEVER use `\ud83c\udf55` style unicode escape sequences
2. Include ALL 5 JSON-LD schema blocks:
   - Article (with SpeakableSpecification)
   - ItemList (10 Restaurant/LocalBusiness entries with GeoCoordinates, aggregateRating)
   - FAQPage (8 Question/Answer pairs)
   - TouristTrip
   - BreadcrumbList
3. Include the interactive Google Maps config (`window.__POPULAR_PICKS_MAP__`) with all 10 lat/lng coordinates
4. Include both desktop sidebar map AND mobile inline map
5. Include the IntersectionObserver scroll-tracking JavaScript
6. Include filter bar with style + price chips and filter JavaScript

**Required page sections (in order):**
1. `<head>` — GA tag, meta tags, OG/Twitter cards, canonical URL, 5 schema blocks, full CSS
2. `<nav>` — shared navigation (copy from template)
3. Hero section — badge, H1, subtitle
4. Page layout (map sidebar + content):
   - Desktop map sidebar (sticky)
   - Quick answer section (2-column: summary + top verdicts)
   - Intro section (city/food context, 2-3 paragraphs)
   - Mobile map (hidden on desktop)
   - Methodology section (sources cited)
   - Comparison table (all 10 at a glance)
   - Quick Picks by Style/Budget (3 category cards)
   - Filter bar (style + price chips)
   - 10 restaurant sections, each with:
     - Header (rank number, name, cuisine tags, rating)
     - Details (price, address, Google Maps link)
     - Verdict box
     - Comparison card (best for, strengths, price/value, what to order, insider tip)
     - Hours (collapsible `<details>`)
     - Contact (phone, website)
     - Image (`<img>` pointing to `https://img.tabiji.ai/popular-picks/[slug]/[section-id].jpg`)
     - 2 Reddit quotes with source attribution
   - Planning section (reservations, payment, best times, recommended route, getting around)
   - FAQ section (8 items)
   - Viator section (4 tour cards with affiliate PID: `pid=P00292930&mcid=42383&medium=link`)
   - Related sections (compare pages, same-city picks, related picks list)
5. Map JavaScript + Google Maps API script
6. Filter JavaScript

### Step 3: Add Photos (SerpAPI + R2)

Run `python3 scripts/add_photos_for_page.py [slug]` which:
1. Extracts venue names from the HTML
2. Searches Google Images via SerpAPI for each venue
3. Scores candidates with Gemini Vision (1-10)
4. Optimizes to 800px JPEG
5. Uploads to Cloudflare R2 at `popular-picks/[slug]/[section-id].jpg`

The HTML already has `<img src="https://img.tabiji.ai/popular-picks/[slug]/[section-id].jpg">` — photos just need to exist at those R2 paths.

**Photo script requirements:**
- SerpAPI key: `security find-generic-password -s serpapi-key -w`
- Cloudflare R2 token: `security find-generic-password -s cloudflare-api-token -w`
- Gemini API key: `security find-generic-password -s gemini-api-key -w`
- R2 account: `9ce95ed3e1df4a7e1d2a401e116c3c6f`
- R2 bucket: `tabiji-media`
- CDN base: `https://img.tabiji.ai`

### Step 4: Add to Country Hub

Find the country hub page and add a pick-card link:

```html
<a href="/popular-picks/[slug]/" class="pick-card">
  <img src="https://img.tabiji.ai/popular-picks/[slug]/[first-pick-id].jpg" alt="[title]" loading="lazy">
  <div class="pick-card-body">
    <span class="card-badge">📍 [City]</span>
    <h3>[Title]</h3>
    <p>[Short description]</p>
    <div class="card-meta"><span>🍽️ 10 spots</span><span>🗺️ Interactive Map</span></div>
  </div>
</a>
```

Country hub mapping:
- US cities → `popular-picks/usa/index.html`
- Japan cities → `popular-picks/japan/index.html`
- France cities → `popular-picks/france/index.html`
- Italy cities → `popular-picks/italy/index.html`
- Singapore → `popular-picks/singapore/index.html`
- Greece → `popular-picks/greece/index.html`
- (Check `popular-picks/[country]/index.html` for others)

Insert the new card before the closing `</div></section>` of the picks grid.

### Step 5: Validate

Run these checks on the new page:
```bash
# Structure check
schema=$(grep -c "application/ld+json" "$f")     # Should be 5
maps=$(grep -c "data-map-lat" "$f")               # Should be 10
h1=$(grep -c "<h1>" "$f")                         # Should be 1
canonical=$(grep -c 'rel="canonical"' "$f")       # Should be ≥1
unicode=$(grep -c '\\u[0-9a-f]' "$f")             # Should be 0

# Content quality check
# - Canonical URL matches slug
# - OG URL matches canonical
# - No leftover template city names (e.g., "Detroit" in a Paris page)
# - All image paths use correct slug
# - Internal links point to existing pages
```

### Step 6: Fix Unicode Escapes (if needed)

If the page was generated with unicode escapes, run this fix:
```python
replacements = {
    r'\ud83c\udf55': '🍕', r'\ud83c\udf63': '🍣', r'\ud83c\udf5c': '🍜',
    r'\ud83c\udf56': '🍖', r'\ud83c\udf57': '🍗', r'\ud83e\udd69': '🥩',
    r'\ud83d\udcb4': '💴', r'\ud83d\udccd': '📍', r'\ud83d\udccc': '📌',
    r'\ud83d\udd50': '🕐', r'\ud83d\udcde': '📞', r'\ud83c\udf10': '🌐',
    # ... (full list in scripts/add_photos_for_page.py)
}
```

### Step 7: Commit & Deploy

```bash
git add popular-picks/[slug]/index.html popular-picks/[country]/index.html
git commit -m "Add [slug] popular picks page ([volume]/mo search volume)"
git push origin main
```

Cloudflare Pages auto-deploys from main.

## Batch Building

When building multiple pages, parallelize with background agents:
1. Launch 5-10 page builder agents simultaneously
2. Each agent reads the detroit-pizza template and creates one page
3. After all complete, run photos in parallel (`&` background jobs)
4. Add all country hub links
5. Validate all pages
6. Single commit with all pages

## Quality Checklist

Before committing any page:
- [ ] 5 schema blocks (Article, ItemList, FAQPage, TouristTrip, BreadcrumbList)
- [ ] 10 restaurant sections with map coordinates
- [ ] 8 FAQ items
- [ ] 0 unicode escape sequences
- [ ] Correct canonical URL and OG URL
- [ ] No template city name leaks
- [ ] All image paths use correct slug
- [ ] Internal links verified (compare + popular-picks pages exist)
- [ ] Added to country hub
- [ ] Photos uploaded to R2 CDN
- [ ] Viator links have correct affiliate PID

## Related Files
- Template: `popular-picks/detroit-pizza/index.html`
- Photo script: `scripts/add_photos_for_page.py`
- Master queue: `popular-picks-master-queue.json`
- Country hubs: `popular-picks/{usa,japan,france,italy,singapore,greece,...}/index.html`
