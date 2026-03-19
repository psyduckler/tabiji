# How to Build a Popular Picks Page (End-to-End)

_Complete step-by-step guide for creating a new popular-picks leaf page from scratch._

---

## Prerequisites

- macOS with Keychain access (for API keys)
- Node.js installed
- Access to the `tabiji` repo
- API keys in Keychain: `serpapi-key`, `cloudflare-pages-token`, `google-places-api-key`

---

## Step 1: Choose a Topic

Format: `{city}-{category}` (e.g., `bangkok-rooftop-bars`, `lisbon-pastel-de-nata`)

Check it doesn't already exist:
```bash
ls popular-picks-data/ | grep "<slug>"
ls popular-picks/ | grep "<slug>"
```

---

## Step 2: Reddit Research

Search Reddit for real traveler recommendations. This is the foundation — no Reddit sourcing = not a tabiji page.

```bash
SERPAPI_KEY=$(security find-generic-password -s serpapi-key -w)

# Search travel subreddits
curl -s "https://serpapi.com/search.json?engine=google&q=site:reddit.com+best+<TOPIC>+<CITY>&api_key=$SERPAPI_KEY&num=15"
```

**Target subreddits:** `r/travel`, `r/solotravel`, `r/backpacking`, plus regional subs (e.g., `r/JapanTravel`, `r/ThailandTourism`)

**Alternative:** Use direct Reddit JSON API (append `.json` to any Reddit URL):
```bash
curl -s "https://www.reddit.com/r/travel/search.json?q=best+coffee+tokyo&restrict_sr=1&sort=relevance&limit=25" \
  -H "User-Agent: tabiji-research/1.0"
```

**What to collect per pick:**
- Place name (exact, including any local-language name)
- Neighborhood / address
- What people recommend ordering or doing
- Price range (local currency + USD)
- 1-2 notable Reddit quotes with thread URLs
- Google Maps URL (search `"Place Name" city` on Google Maps, grab the link)

**Minimum:** 10 Reddit threads, 50+ comments synthesized. Aim for 8-18 picks per page.

---

## Step 3: Create the JSON Data File

Create `popular-picks-data/<slug>.json`. This is the single source of truth — the HTML page is generated from this file.

**Template structure:**
```json
{
  "slug": "tokyo-vintage-shopping",
  "pageType": "popular-picks",
  "status": "reviewed",
  "taxonomy": {
    "city": "Tokyo",
    "neighborhood": null,
    "country": "Japan",
    "countryCode": "JP",
    "category": "shopping",
    "vertical": "shopping",
    "badgeEmoji": "🛍️"
  },
  "seo": {
    "title": "12 Best Vintage Shops in Tokyo — tabiji.ai",
    "h1": "12 Best Vintage Shops in Tokyo",
    "metaTitle": "12 Best Vintage Shops in Tokyo (2026) — Reddit-Backed Guide | tabiji.ai",
    "metaDescription": "The best vintage and thrift shops in Tokyo — curated from hundreds of Reddit reviews. Shimokitazawa, Harajuku, Koenji and more.",
    "canonicalPath": "/popular-picks/tokyo-vintage-shopping/",
    "heroImage": "",
    "publishedTime": "2026-03-16T00:00:00Z",
    "modifiedTime": "2026-03-16T00:00:00Z",
    "robots": "index, follow, max-image-preview:large"
  },
  "hero": {
    "eyebrow": "Popular Picks — Tokyo",
    "title": "12 Best Vintage Shops in Tokyo",
    "dek": "Description of the page...",
    "badge": "🛍️ Tokyo",
    "metaSpans": ["📍 Tokyo", "🛍️ 12 spots", "🗺️ Interactive Map"]
  },
  "intro": {
    "answerFirst": "One-sentence answer: the single best pick and why.",
    "body": [
      "First paragraph of intro...",
      "Second paragraph..."
    ]
  },
  "summary": {
    "totalOptions": 12,
    "priceRangeLocal": "¥0–5,000",
    "priceRangeUSD": "$0–$35",
    "bestBudgetOption": "Name of cheapest good option",
    "bestOverall": "Name of #1 pick",
    "topPick": "Name of #1 pick",
    "sourcesAnalyzed": "87 Reddit threads across r/JapanTravel, r/tokyo",
    "lastVerifiedLabel": "2026-03"
  },
  "map": {
    "enabled": true,
    "title": "Vintage Shop Map",
    "ctaLabel": "Open in Google Maps",
    "ctaUrl": null
  },
  "picks": [
    {
      "rank": 1,
      "name": "Shop Name",
      "neighborhood": "Shimokitazawa",
      "address": "2-25-8 Kitazawa, Setagaya",
      "priceRangeLocal": "¥500–3,000",
      "priceRangeUSD": "$3–$20",
      "googleMapsUrl": "https://maps.google.com/?cid=...",
      "website": "https://example.com",
      "photo": "",
      "whatToOrder": ["Item 1", "Item 2"],
      "ourTake": "Why this place is good — opinionated, specific.",
      "redditQuotes": [
        {
          "text": "Actual quote from a Redditor...",
          "source": "r/JapanTravel",
          "url": "https://reddit.com/r/JapanTravel/comments/..."
        }
      ],
      "tags": ["vintage", "thrift"]
    }
  ],
  "faq": [
    {
      "question": "Where is the best area for vintage shopping in Tokyo?",
      "answer": "Shimokitazawa is the consensus pick. It has the highest density of vintage shops within walking distance..."
    }
  ],
  "related": {
    "manual": ["shimokitazawa-coffee", "tokyo-cheap-eats"],
    "topics": []
  },
  "verification": {
    "lastVerified": "2026-03",
    "pipelineVersion": "v3",
    "reviewedByHuman": false
  },
  "publishing": {
    "outputPath": "popular-picks/tokyo-vintage-shopping/index.html",
    "includeInMetadataIndex": true,
    "includeInSitemap": true,
    "includeInApiBuild": true
  }
}
```

**Key rules:**
- Every pick needs `name`, `neighborhood`, `rank`, `ourTake`, and at least 1 `redditQuote`
- `googleMapsUrl` — search the place on Google Maps, click Share → Copy Link
- `priceRangeLocal` + `priceRangeUSD` — include both currencies
- `whatToOrder` — specific items, not generic ("try the pork ribs" not "good food")
- `faq` — minimum 3 questions, specific answers with numbers

**Non-ASCII place names:** The build script's `slugify()` function handles Turkish (ı, ş, ç, ğ), Nordic (ø, æ), German (ß), and other common non-Latin characters. These are converted to ASCII equivalents before slug generation (e.g., "Kahvaltı" → "kahvalti", "Frederikshøj" → "frederikshoj"). If you encounter a language with characters not covered, add a `.replace()` line to the `slugify()` function in `generators/popular-picks/render-page.js`. Empty section IDs break the map scroll-sync feature.

---

## Step 4: Validate the JSON

```bash
cd tabiji
node generators/popular-picks/build-page.js popular-picks-data/<slug>.json
```

This validates the JSON and generates HTML to `tmp/`. Fix any errors before proceeding.

---

## Step 5: Find Photos (Photo Pipeline)

For each pick, find a high-quality photo:

```bash
SERPAPI_KEY=$(security find-generic-password -s serpapi-key -w)

# Search Google Images for each pick
curl -s "https://serpapi.com/search.json?engine=google_images&q=PLACE_NAME+CITY&api_key=$SERPAPI_KEY"
```

1. Download top 5 candidates per pick
2. Vision-score them (use `image` tool — batch all 5 in one call)
3. Pick the winner, optimize: `sips -Z 800 --setProperty formatOptions 80 photo.jpg`
4. Upload to R2:
```bash
CF_TOKEN=$(security find-generic-password -s "cloudflare-pages-token" -w)
curl -s -X PUT \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: image/jpeg" \
  --data-binary @"photo.jpg" \
  "https://api.cloudflare.com/client/v4/accounts/9ce95ed3e1df4a7e1d2a401e116c3c6f/r2/buckets/tabiji-media/objects/popular-picks/<slug>/<filename>.jpg"
```
5. Update the JSON: set `"photo": "https://img.tabiji.ai/popular-picks/<slug>/<filename>.jpg"` for each pick
6. Set `seo.heroImage` to the first pick's photo URL

**Full details:** See `docs/photo-pipeline.md`

---

## Step 6: Enrich with Google Places Data

```bash
python3 functions/enrich-popular-picks.py --slug <slug>
```

This adds Google ratings, review counts, hours, and Google Maps links to each pick in the JSON.

---

## Step 7: Add Lat/Lng Coordinates

```bash
python3 generators/popular-picks/enrich-coordinates.py --slug <slug>
```

This geocodes each pick via Google Places API and adds `lat`/`lng` to the JSON. Required for the JS API map.

---

## Step 8: Generate the HTML Page

```bash
node generators/popular-picks/build-page.js \
  popular-picks-data/<slug>.json \
  popular-picks/<slug>/index.html
```

This generates the full HTML page with:
- Responsive layout with sidebar map (desktop) / inline map (mobile)
- Google Maps JS API with numbered markers + scroll sync
- Reddit quotes, verdicts, FAQ section
- Schema markup (Article, FAQPage)
- Standard nav/footer

---

## Step 9: Update Indexes

After the HTML is generated, update the sitemap, API, and hub page:

### Sitemap
Add to `sitemap.xml`:
```xml
<url>
  <loc>https://tabiji.ai/popular-picks/<slug>/</loc>
  <lastmod>2026-03-16</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.7</priority>
</url>
```

### API
Rebuild the API:
```bash
python3 api/build-api.py
```

This creates/updates `api/v1/picks/<slug>.json` and the master `api/v1/picks.json`.

### Country Hub Page (MANDATORY)
**Every new page MUST be linked from its country hub page.** This is not optional — without it, the page has no internal links and won't get crawled properly.

1. Find the country hub: `popular-picks/<country>/index.html` (e.g., `popular-picks/japan/index.html`)
2. Find the correct city section (or create one if the city isn't listed yet)
3. Add a card inside the city's `<div class="picks-grid">`, matching the existing format:

```html
<a href="/popular-picks/<slug>/" class="pick-card">
  <img src="<heroImage URL from JSON>" alt="TITLE" loading="lazy">
  <div class="pick-card-body">
    <span class="card-badge">🍽️ City</span>
    <h3>TITLE</h3>
    <p>SHORT DESCRIPTION</p>
    <div class="card-meta"><span>🍽️ N spots</span><span>🗺️ Interactive Map</span></div>
  </div>
</a>
```

**Use the actual hero image URL** from the JSON's `seo.heroImage` field — don't guess filenames like `photo-0.jpg`.

4. `git add` the country hub page along with the other files in Step 10.

If no country hub page exists yet, note it in your output — but this is rare (most countries already have one).

### Main Hub Page
If the page fits a country section on `popular-picks/index.html`, add it there too.

---

## Step 10: Git Push

```bash
cd tabiji
git add popular-picks-data/<slug>.json
git add popular-picks/<slug>/index.html
git add sitemap.xml
git add api/
# Add country hub if updated
git commit -m "feat: add <slug> popular picks page"
git push origin main
```

Or open a PR for review:
```bash
git checkout -b sno/<slug>
git add .
git commit -m "feat: add <slug> popular picks page"
git push origin sno/<slug>
gh pr create --title "feat: add <slug> popular picks" --body "New popular picks page for <slug>"
```

---

## Step 11: Submit for Indexing

After git push, submit the new URL for faster indexing:

```bash
INDEXNOW_KEY=$(security find-generic-password -s indexnow-key -w)
curl -s -X POST "https://api.indexnow.org/IndexNow" \
  -H "Content-Type: application/json" \
  -d "{\"host\":\"tabiji.ai\",\"key\":\"$INDEXNOW_KEY\",\"keyLocation\":\"https://tabiji.ai/$INDEXNOW_KEY.txt\",\"urlList\":[\"https://tabiji.ai/popular-picks/<slug>/\"]}"
```

This notifies Bing/Yandex immediately. Google picks up from the sitemap.

---

## Step 12: Verify

After deploy (~30 seconds on Cloudflare):
1. Visit `https://tabiji.ai/popular-picks/<slug>/` — page loads, photos show, map works
2. Check the API: `https://tabiji.ai/api/v1/picks/<slug>.json`
3. Check the country hub links to it
4. Check sitemap includes it

---

## Quick Reference: File Locations

| What | Where |
|------|-------|
| JSON data (source of truth) | `popular-picks-data/<slug>.json` |
| Generated HTML | `popular-picks/<slug>/index.html` |
| Photos | `img.tabiji.ai/popular-picks/<slug>/` (R2, NOT git) |
| API entry | `api/v1/picks/<slug>.json` |
| API index | `api/v1/picks.json` |
| Country hub | `popular-picks/<country>/index.html` |
| Main hub | `popular-picks/index.html` |
| Sitemap | `sitemap.xml` |
| Build script | `generators/popular-picks/build-page.js` |
| Validator | `generators/popular-picks/validate-source.js` |
| Enrichment | `functions/enrich-popular-picks.py` |
| Geocoding | `generators/popular-picks/enrich-coordinates.py` |
| Photo pipeline | `docs/photo-pipeline.md` |

## API Keys Required

| Key | Keychain name | Used in |
|-----|--------------|---------|
| SerpAPI | `serpapi-key` | Reddit research + photo search |
| Cloudflare R2 | `cloudflare-pages-token` | Photo upload |
| Google Places | `google-places-api-key` | Enrichment + geocoding |
| Google Maps (client) | Hardcoded in render-page.js | Map on page: `AIzaSyBP0yidMjJEECgkIiZz2lw1NLsQ7jdASYc` |
