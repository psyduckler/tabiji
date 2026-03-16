# Compare Page Runbook

_The definitive guide to building compare pages on tabiji.ai. Follow this exactly._

## Reference Page

**`tokyo-vs-kyoto`** is the current reference implementation. New compare pages should match its structure, tone, and quality bar. When in doubt, open `compare/tokyo-vs-kyoto/index.html` and study the pattern — but always verify against `main` for the latest production shell, since details can evolve.

---

## 1. Page Structure (Required Sections)

Every compare page has these sections in this order:

| # | Section | HTML ID | Required? |
|---|---------|---------|-----------|
| 1 | Hero | `.hero` | ✅ |
| 2 | Photo Grid | `.photo-grid` | ✅ (2 photos, one per destination) |
| 3 | TL;DR Verdict | `#the-tl-dr-verdict` (`.verdict-box`) | ✅ |
| 4 | Quick Comparison Table | `#quick-comparison` (`.comparison-table`) | ✅ |
| 5–N | Deep Dive Sections | `<section class="deep-dive">` | ✅ (8–10 sections typical) |
| N+1 | Decision Framework | `#the-decision-framework` | ✅ |
| N+2 | FAQ | `#frequently-asked-questions` (`.faq-section`) | ✅ |
| N+3 | CTA Footer | — | ✅ |

### Deep Dive Sections (typical set)

Pick 8–10 from this list based on what's relevant to the comparison:

- 🍜 Food & Dining
- ⛩️ Temples, Shrines & Culture / Cultural Attractions
- 💰 Cost Comparison
- 🚃 Getting Around / Transit
- 🌸 Best Time to Visit / Weather & Seasons
- 🏨 Where to Stay / Neighborhoods
- 🎒 Day Trips
- 🔀 Why Not Both? (for nearby destinations)
- 🏖️ Beaches
- 🌿 Nature & Outdoors
- 🛡️ Safety
- 🎉 Nightlife & Entertainment
- 🛍️ Shopping
- 👨‍👩‍👧 Family-Friendliness
- ✈️ Getting There / Logistics

Not every section applies to every comparison. A `bali-vs-fiji` page needs Beaches; a `tokyo-vs-kyoto` page doesn't. Use judgment — but always hit at least 8 deep-dive sections.

---

## 2. Content Quality Bar

### What makes a compare page "good enough" to publish

1. **Reddit-sourced insights.** Every deep-dive section should reference real traveler opinions from Reddit. Use `r/<relevant-subreddit>` threads. Include 1–2 `reddit-quote` blocks per section where impactful.

2. **Specific numbers.** Costs in local currency + USD. Distances/times between destinations. Hotel price ranges. Transit costs. No vague "it's affordable" — give the number.

3. **tabiji verdict per section.** Every deep-dive section ends with a `<div class="tabiji-verdict">` giving a clear, opinionated take. Not wishy-washy — pick a side or explain the tradeoff.

4. **Quick comparison table with Edge column.** The summary table must have a clear "Edge" for each category. Use `<span class="edge-{destination}">` or `<span class="edge-tie">Tie</span>`. ~10 rows.

5. **Decision Framework.** Two-column "Choose A If…" / "Choose B If…" with bullet points. Concrete, not generic.

6. **7+ FAQ questions with real answers.** FAQ section with `FAQPage` schema in `<head>`. Answers should be 2–4 sentences, specific, citing numbers where possible.

7. **Internal links to tabiji pages.** Link to relevant `/popular-picks/`, `/i/` (itinerary), and other `/compare/` pages where natural. This is critical for SEO interlinking.

8. **4 images minimum.** 2 in the hero photo grid, 2+ as `section-img` in deep-dive sections. All hosted on R2 at `img.tabiji.ai/compare/{slug}/`.

### What makes a compare page NOT good enough

- Generic AI filler with no Reddit sourcing
- No specific costs or numbers
- Fewer than 8 deep-dive sections
- Missing FAQ schema
- No internal links to other tabiji pages
- Wishy-washy verdicts that don't pick sides

---

## 3. Technical Spec

### File structure
```
compare/{slug}/index.html     ← the page
```

Images go to Cloudflare R2, NOT the git repo:
```
img.tabiji.ai/compare/{slug}/{image-name}.jpg
```

### Required `<head>` elements

1. **GA4 tag** (`G-D7QHNRXLHJ`)
2. **Favicon + apple-touch-icon** (standard tabiji set)
3. **`<title>`**: `{A} vs {B}: Which Should You Visit? (2026 Comparison) | tabiji.ai`
4. **`<meta name="description">`**: Mention Reddit, real costs, data-backed
5. **Open Graph**: `og:title`, `og:description`, `og:type=article`, `og:url`, `og:image`, `og:site_name`
6. **Twitter card**: `summary_large_image`
7. **`article:published_time`** and **`article:modified_time`** (ISO 8601)
8. **`<link rel="canonical">`**: `https://tabiji.ai/compare/{slug}/`
9. **Schema: Article** with `speakable` (cssSelector: `.hero h1`, `.hero .subtitle`, `.verdict-box`, `.faq-section`)
10. **Schema: BreadcrumbList** (Home → Compare → {This Page})
11. **Schema: FAQPage** (all FAQ Q&As)

### CSS

Match the current production CSS from `tokyo-vs-kyoto` (the design system is inline per page, no shared stylesheet). Verify against `main` before copying — styles may have been updated since this runbook was written. Key CSS classes:

- `.hero`, `.hero-badge`, `.hero-meta`
- `.toc-sidebar` (sticky sidebar with Contents links)
- `.verdict-box` (TL;DR section)
- `.comparison-table`, `.edge-{name}`, `.edge-tie`
- `.deep-dive` (content sections)
- `.reddit-quote`, `.source` (blockquote styling)
- `.tabiji-verdict` (per-section verdict)
- `.photo-grid`, `.section-img`
- `.decision-matrix` (Choose A If / Choose B If)
- `.faq-section`, `.faq-item`
- `.cta-bottom` (footer CTA)

### Navigation

Standard tabiji nav with:
- Logo (owl + "tabiji")
- Explore dropdown (Itineraries, Compare, Popular Picks, Destinations, Travel Alerts, Resources)
- "Plan Your Trip" CTA button
- Hamburger menu for mobile

### Footer

Standard tabiji footer with copyright, social links, nav links.

---

## 4. Research Workflow

For each new compare page:

### Step 1: Reddit Research
- Search Reddit for `"{A} vs {B}"` and `"{A} or {B}"` in travel subreddits
- Target subs: `r/travel`, `r/solotravel`, `r/backpacking`, plus regional subs (e.g., `r/JapanTravel`)
- Use SerpAPI (preferred) or direct Reddit JSON API (`.json` suffix)
- Collect: real opinions, specific costs mentioned, common questions, neighborhood recommendations
- Minimum: 10 Reddit threads, 50+ comments synthesized

### Step 2: Data Collection
- **Costs:** Numbeo, Budget Your Trip, or recent Reddit reports. Always local currency + USD.
- **Weather:** Open-Meteo API for monthly temperature/rainfall data
- **Transit:** Official transit authority sites for route times and costs
- **Accommodation:** Booking.com/Hostelworld ranges for budget/mid-range/luxury

### Step 3: Image Sourcing
- Use SerpAPI Google Images (`engine=google_images`) for each destination
- Find 4+ high-quality photos: 2 for hero grid, 2+ for deep-dive sections
- Vision-score candidates for quality and iconic-ness
- Optimize: 800px wide, 80% JPEG quality
- Upload to R2: `img.tabiji.ai/compare/{slug}/{descriptive-name}.jpg`

### Step 4: Write the Page
- Use `tokyo-vs-kyoto/index.html` as the reference for structure and required sections (verify against `main` for latest)
- Replace all content — do NOT leave any Tokyo/Kyoto references
- Write in tabiji voice: opinionated, data-backed, traveler-to-traveler (not guidebook corporate)
- Every claim should trace back to Reddit, a data source, or personal research

### Step 5: Internal Linking
- Link to existing tabiji pages wherever relevant:
  - `/popular-picks/{city}-{topic}/` pages
  - `/i/{slug}/` itinerary pages
  - Other `/compare/` pages
- Check what exists first: `ls popular-picks/ | grep {city}` and `ls i/ | grep {city}`

---

## 5. Publish Checklist

Before opening a PR, verify ALL of the following:

### Content
- [ ] TL;DR verdict is clear and opinionated
- [ ] Quick comparison table has 10+ rows with Edge column
- [ ] 8+ deep-dive sections, each with a `tabiji-verdict`
- [ ] 5+ Reddit quotes with source links
- [ ] 7+ FAQ questions with specific answers
- [ ] Decision framework with concrete bullet points
- [ ] All costs include local currency + USD equivalent
- [ ] Internal links to existing tabiji pages (popular-picks, itineraries, other compare)
- [ ] No leftover template text or wrong destination names

### Technical
- [ ] Valid HTML (no unclosed tags)
- [ ] All 3 schema blocks present: Article (with speakable), BreadcrumbList, FAQPage
- [ ] `<title>` follows format: `{A} vs {B}: Which Should You Visit? (2026 Comparison) | tabiji.ai`
- [ ] Canonical URL is correct: `https://tabiji.ai/compare/{slug}/`
- [ ] OG image points to an actual uploaded image on R2
- [ ] All images load from `img.tabiji.ai/compare/{slug}/`
- [ ] GA4 tag present (`G-D7QHNRXLHJ`)
- [ ] Responsive: check hero, table, photo grid at mobile widths

### Index & API Updates
- [ ] `compare/index.html` updated with new page card
- [ ] `api/v1/compare.json` updated (increment count, add entry to comparisons array)
- [ ] `sitemap.xml` updated with new URL + lastmod
- [ ] Per-page API JSON created: `api/v1/compare/{slug}.json`

### Images
- [ ] 4+ images uploaded to R2 at `img.tabiji.ai/compare/{slug}/`
- [ ] Hero photo grid has 2 images (one per destination)
- [ ] At least 2 section images in deep-dive content
- [ ] All images have descriptive `alt` text
- [ ] Images optimized (800px wide, JPEG ~80%)

---

## 6. API JSON Format

Each compare page gets a JSON file at `api/v1/compare/{slug}.json`:

```json
{
  "slug": "tokyo-vs-kyoto",
  "title": "Tokyo vs Kyoto: Which Should You Visit?",
  "destination1": "Tokyo",
  "destination2": "Kyoto",
  "verdict": "Tokyo for variety and energy, Kyoto for culture and temples. Do both if you have 7+ days.",
  "categories": [
    {
      "name": "Food & Dining",
      "edge": "Tokyo",
      "summary": "Tokyo has more Michelin stars and cuisine diversity. Kyoto has the best kaiseki and matcha."
    }
  ],
  "faq": [
    {
      "question": "Is Tokyo or Kyoto better for first-time visitors?",
      "answer": "..."
    }
  ],
  "url": "https://tabiji.ai/compare/tokyo-vs-kyoto/",
  "lastUpdated": "2026-03-08"
}
```

The master index at `api/v1/compare.json`:
```json
{
  "count": 40,
  "comparisons": [
    {
      "slug": "...",
      "title": "...",
      "destination1": "...",
      "destination2": "...",
      "categoryCount": 9,
      "url": "https://tabiji.ai/compare/.../"
    }
  ]
}
```

---

## 7. Tier C Rebuild Plan

10 pages were removed from active inventory (documented in `docs/compare-tier-c-inventory.md`). They need rebuilding because they had bespoke structures that didn't fit the standardized template.

Rebuild sequence:
1. Keep the standard compare shell stable across active inventory
2. Rebuild Tier C pages one by one using this runbook
3. Re-add to index, API, and sitemap only after they pass the publish checklist

Priority rebuilds: `paris-vs-rome`, `barcelona-vs-lisbon`, `iceland-vs-norway`, `bali-vs-thailand`, `greece-vs-italy`

---

## 8. Common Mistakes to Avoid

- **Don't leave template text.** Search the final HTML for any mention of the template destinations.
- **Don't skip the API updates.** Every new page needs `compare.json`, per-page JSON, sitemap, and index updates.
- **Don't use generic verdicts.** "Both are great!" is not a verdict. Pick a side or explain the specific tradeoff.
- **Don't forget R2 image upload.** Images go to R2, not the git repo. Dead image links = broken page.
- **Don't skip Reddit research.** The whole brand promise is "Reddit-backed, not AI filler." If you can't find Reddit threads about this comparison, it might not be a good compare page.
- **Don't hardcode wrong API keys.** Use the standard Tabiji Google Maps API key already used by existing pages. Check the production `tokyo-vs-kyoto` page or project config for the current key — don't guess or use a different one.
