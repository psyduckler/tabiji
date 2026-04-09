# Compare Pages SEO/GEO/AEO Audit — 2026-04-06

## Scope
128 compare pages with 500+ monthly search volume (out of 851 total).
Total addressable search volume: ~1.57M/mo across all pages.

---

## Current State (from auditing 5 pages)

**What's working well:**
- Article + BreadcrumbList + FAQPage schema on every page
- SpeakableSpecification targeting hero, subtitle, verdict, FAQ
- 8 FAQ Q&As per page, well-targeted to search intent
- 10-category comparison table with Winner column
- Reddit social proof (4-8 quotes with attribution)
- Decision framework ("Choose X If..." / "Choose Y If...")
- CDN-served images (img.tabiji.ai)
- Clean canonical URLs and OG tags

**What's inconsistent across pages:**
- Vietnam-vs-Thailand = gold standard (18 internal links, 3 tables, great alt text)
- Madrid-vs-Barcelona = good (9 links, 4 images, year in title)
- Chile, Mykonos, Cabo = bare minimum (5 links, generic alt text, no year)

---

## PRIORITY IMPROVEMENTS

### 1. INTERNAL LINKING (Highest SEO impact)

**Problem:** Most pages have only 5 internal links (breadcrumbs + /plan CTAs). Vietnam-vs-Thailand has 18. This is the single biggest gap.

**Fix for all 128 top pages:**
- Add 2-3 cross-links to related compare pages (e.g., chile-vs-argentina links to peru-vs-argentina, colombia-vs-peru)
- Add 2-4 links to relevant popular-picks pages (food, activities)
- Add a "Related Comparisons" section at page bottom with 4-6 links
- Link from verdict/decision sections to destination guide pages

**Why it matters:** Internal links distribute PageRank, help crawl discovery, and signal topical clusters to Google. The compare pages should form a tight mesh, not isolated islands.

### 2. IMAGE ALT TEXT (Quick win, big impact)

**Problem:** Chile, Mykonos, Cabo (and likely most pages) have:
- Hero images with NO alt text
- Destination images with generic text like "Chile travel destination"

**Fix:** Every image needs descriptive, keyword-rich alt text like Vietnam page:
- "Ha Long Bay, Vietnam — limestone karsts rising from emerald waters"
- NOT "Vietnam travel destination"

**Apply to all 128 pages.** This is automatable — pull destination + landmark data to generate proper alt text.

### 3. TITLE TAG FRESHNESS (Quick win)

**Problem:** Only Madrid has "(2026)" in the title. All others don't.

**Fix:** Add current year to all title tags:
- "Chile vs Argentina: Which Should You Visit? (2026) — tabiji.ai"

**Why:** Year in title improves CTR in SERPs and signals freshness to Google.

### 4. ADDITIONAL DATA TABLES (GEO/AEO impact)

**Problem:** Most pages have only 1 comparison table. Vietnam has 3 (comparison + cost breakdown + weather).

**Add to all 128 pages:**
- **Cost Breakdown Table** — line items: hostel, hotel, street food, restaurant, beer, local transport, daily total
- **Weather/Climate Table** — 12 months, temperature + rainfall for both destinations
- **Flight Cost Table** — avg roundtrip from major US hubs

**Why for GEO/AEO:** AI models (ChatGPT, Perplexity, Google AI Overviews) prefer structured, tabular data they can cite. Tables with specific numbers get extracted into AI answers far more than prose.

### 5. SCHEMA ENHANCEMENTS (AEO impact)

**Currently have:** Article, BreadcrumbList, FAQPage, SpeakableSpecification

**Add:**
- **ItemList schema** for the comparison table (each category as a ListItem with properties)
- **Table schema** (or WebPage with mainEntity pointing to comparison data)
- **HowTo schema** for "How to choose between X and Y" — earns rich snippets
- **Place schema** for each destination (geo coordinates, containedInPlace for country)
- **AggregateRating or editorial score** — structured rating for each destination across categories

**Why:** More schema = more chances for rich results, AI citation, and voice assistant answers.

### 6. "WHY NOT BOTH?" SECTION (Content depth)

**Problem:** Only Vietnam-vs-Thailand has a "Why Not Both?" combined itinerary section.

**Add to all applicable pages:**
- 2-3 combined itinerary suggestions (1-week, 2-week, 3-week)
- Logistics (how to get between destinations, border crossings, flight connections)
- Best time to combine both

**Why:** Captures the long-tail "X and Y itinerary" queries. Also signals comprehensive content to AI models.

### 7. E-E-A-T SIGNALS (Trust/authority)

**Problem:** Author is just "tabiji.ai" Organization. No individual expert, no credentials, no methodology detail on page.

**Add:**
- Visible "Reviewed by [travel expert name]" with bio link
- Methodology section: "Based on analysis of X Reddit threads, Y travel forums, and Z data points"
- Visible "Last updated: [date]" on page (not just in schema)
- "Sources" section at bottom with links to data sources

**Why:** Google's E-E-A-T framework rewards pages with clear expertise signals. AI models also prefer citing pages with visible authority markers.

### 8. SPEAKABLE + FEATURED SNIPPET OPTIMIZATION (AEO)

**Current:** SpeakableSpecification targets `.hero h1`, `.hero .subtitle`, `.verdict-box`, `.faq-section`

**Improve:**
- Add a **TL;DR / Quick Answer box** at the top of each page:
  > "For most travelers, [City A] is better for [X] while [City B] is better for [Y]. Choose [City A] if you want [key reason]. Choose [City B] if you want [key reason]."
- Mark this with `data-speakable` and include in SpeakableSpecification
- Format verdict boxes as direct-answer paragraphs (not just section headers)

**Why:** This is the content AI assistants and voice search will extract. Google's AI Overviews, Siri, Alexa all pull from speakable/concise answer content.

### 9. REVERSE KEYWORD COVERAGE

**Problem:** Pages exist as "chile-vs-argentina" but "argentina vs chile" has 22,200 monthly searches too.

**Fix options:**
- Add `<link rel="alternate">` or canonical handling for reverse order
- Include both orderings naturally in content: "Whether you're searching for Chile vs Argentina or Argentina vs Chile..."
- Ensure the H1 or early content includes both orderings for keyword coverage

**Top pages where the reverse keyword has significant volume:**

| Page slug | Main KW vol | Reverse KW vol | Reverse captures |
|-----------|-------------|----------------|------------------|
| portugal-vs-spain | 301,000 | 165,000 (spain vs portugal) | Partial |
| colombia-vs-mexico | 18,100 | 110,000 (mexico vs colombia) | Page has WRONG order in slug |
| valencia-vs-barcelona | 40,500 | 74,000 (barcelona vs valencia) | Page has WRONG order |
| costa-rica-vs-mexico | 2,900 | 49,500 (mexico vs costa rica) | Page has WRONG order |
| peru-vs-argentina | 1,000 | 3,600 (argentina vs peru) | Reverse is 3.6x higher |
| nice-vs-monaco | 260 | 3,600 (monaco vs nice) | Reverse is 14x higher |
| greece-vs-spain | 260 | 2,400 (spain vs greece) | Reverse is 9x higher |

**High-priority slug flips** (where the reverse keyword has significantly more volume):
- `colombia-vs-mexico` → should be `mexico-vs-colombia` (110K vs 18K)
- `valencia-vs-barcelona` → should be `barcelona-vs-valencia` (74K vs 40K)
- `costa-rica-vs-mexico` → should be `mexico-vs-costa-rica` (49K vs 2.9K)
- `nice-vs-monaco` → should be `monaco-vs-nice` (3.6K vs 260)
- `greece-vs-spain` → should be `spain-vs-greece` (2.4K vs 260)

### 10. CONTENT GAPS FOR AI CITATION (GEO)

AI models cite pages that provide **specific, quotable facts**. Add to each page:

- **Exact flight times** between destinations from major hubs
- **Visa requirements** comparison (US passport holders)
- **Safety index** comparison (Global Peace Index scores or similar)
- **Language barrier** comparison with specific tips
- **WiFi/connectivity** comparison (important for digital nomad queries)
- **Healthcare/insurance** comparison
- **Currency and payment** info (card acceptance, ATM fees)

These create "citation-worthy" data points that AI models prefer to extract.

---

## IMPLEMENTATION PRIORITY FOR 128 PAGES

### Phase 1: Quick wins (all 128 pages, automatable)
1. Fix image alt text (generic → descriptive)
2. Add "(2026)" to all title tags
3. Add visible "Last updated" date
4. Ensure both keyword orderings appear in content

### Phase 2: Content enrichment (start with 10K+ bracket, 10 pages)
5. Add cost breakdown table
6. Add weather/climate table
7. Add "Why Not Both?" section
8. Add TL;DR quick-answer box

### Phase 3: Linking & schema (all 128 pages)
9. Add 6-8 internal cross-links per page
10. Add "Related Comparisons" bottom section
11. Add ItemList + Place + HowTo schema
12. Add editorial scoring schema

### Phase 4: Authority signals (all pages)
13. Add methodology section
14. Add expert reviewer attribution
15. Add sources section

### Phase 5: Slug optimization (5-7 pages)
16. Redirect wrong-order slugs to higher-volume ordering
    (301 redirect old → new, update internal links)

---

## VOLUME IMPACT ESTIMATE

If improvements bring these pages from current average position ~15-20 to top 5:
- 10K+ bracket (10 pages): ~100K+ monthly clicks potential
- 5K-10K bracket (3 pages): ~5K+ monthly clicks
- 2K-5K bracket (25 pages): ~15K+ monthly clicks
- 1K-2K bracket (42 pages): ~15K+ monthly clicks
- 500-999 bracket (48 pages): ~10K+ monthly clicks

**Total organic traffic potential: ~145K+ monthly visits from compare pages alone.**

---

## SPORTS INTENT WARNING

The top 3 pages by volume (portugal-vs-spain, spain-vs-france, colombia-vs-mexico) likely have heavy sports/soccer search intent mixed with travel intent. Consider:
- Adding "travel" or "to visit" in title tags for these pages
- Monitoring CTR — if low despite high impressions, the traffic is sports-driven
- These pages may never rank well for pure travel intent against sports results
