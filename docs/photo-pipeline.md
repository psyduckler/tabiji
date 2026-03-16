# Popular Picks Photo Pipeline

_How to find, score, optimize, and add photos to popular-picks pages. Used by the `article-instagram-photo-adder` skill and adaptable for the popular-picks page builder._

---

## Overview

Every popular-picks leaf page needs photos for each recommendation. Photos are sourced from Google Images via SerpAPI, vision-scored for quality, optimized, uploaded to Cloudflare R2, and referenced in the HTML. **No images are stored in the git repo** — all images are served from `img.tabiji.ai` (R2 CDN).

---

## Step-by-Step Pipeline

### 1. Search for photos (SerpAPI Google Images)

For each pick/recommendation, search Google Images via SerpAPI:

```bash
SERPAPI_KEY=$(security find-generic-password -s serpapi-key -w)

curl -s "https://serpapi.com/search.json?engine=google_images&q=$(python3 -c "import urllib.parse; print(urllib.parse.quote('ATTRACTION_NAME CITY'))")&api_key=$SERPAPI_KEY"
```

Returns `images_results` array with:
- `original` — full-size image URL
- `thumbnail` — smaller preview
- `title`, `source`, `link` (source page)
- `original_width`, `original_height`

**Tips:**
- Include the city/neighborhood in the query for accuracy: `"Bear Pond Espresso Shimokitazawa"`
- Take the top 5 candidates — more than that wastes vision-scoring tokens
- Filter out results with tiny dimensions (<400px) or suspicious domains

### 2. Download candidate photos

```bash
curl -sL -o /tmp/photo-candidates/photo_1.jpg "IMAGE_URL"
curl -sL -o /tmp/photo-candidates/photo_2.jpg "IMAGE_URL"
# ... up to 5 candidates
```

Skip any download under 10KB (broken image or placeholder).

### 3. Vision-score photos

Use the `image` tool (or Gemini/Claude vision) to score all candidates in one call:

**Prompt:**
```
Score each photo 1-10 on how well it represents "[ATTRACTION NAME]", a [TYPE] in [NEIGHBORHOOD], [CITY].

Consider:
- Visual quality (sharpness, lighting, composition)
- Atmosphere (does it capture what makes this place special?)
- Iconic-ness (would a traveler recognize this as THE photo of this place?)
- No watermarks, no heavy text overlays, no collages

For each photo: 1-line description + score. Pick the single best one.
```

### 4. Optimize the winning photo

Resize to 800px wide, JPEG ~80% quality:

```bash
# macOS (sips)
sips -Z 800 --setProperty formatOptions 80 /tmp/photo-candidates/winner.jpg

# Alternative (ImageMagick)
convert winner.jpg -resize 800x -quality 80 optimized.jpg
```

Target file size: 50-150KB per photo.

### 5. Upload to Cloudflare R2

```bash
CF_TOKEN=$(security find-generic-password -s "cloudflare-pages-token" -w)
CF_ACCOUNT="9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_KEY="popular-picks/<slug>/<filename>.jpg"

curl -s -X PUT \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: image/jpeg" \
  --data-binary @"/tmp/photo-candidates/optimized.jpg" \
  "https://api.cloudflare.com/client/v4/accounts/$CF_ACCOUNT/r2/buckets/tabiji-media/objects/$R2_KEY"
```

**Public URL:** `https://img.tabiji.ai/popular-picks/<slug>/<filename>.jpg`

**Key naming convention:**
- Pick photos: `popular-picks/<slug>/photo-0.jpg`, `photo-1.jpg`, etc. (by rank, 0-indexed)
- Or descriptive: `popular-picks/<slug>/bear-pond-espresso.jpg`

### 6. Update the HTML

Set the `<img>` tag's `src` to the R2 URL:

```html
<img src="https://img.tabiji.ai/popular-picks/<slug>/<filename>.jpg" 
     alt="Bear Pond Espresso in Shimokitazawa, Tokyo" 
     style="width:100%;border-radius:12px;margin-bottom:1rem;" 
     loading="lazy">
```

**Image placement in the HTML structure:**
```html
<section class="restaurant-section" id="pick-slug">
  <div class="restaurant-header">
    <h2><span class="restaurant-number">1</span> Bear Pond Espresso</h2>
    ...
  </div>
  <div class="restaurant-details">
    ...
  </div>
  <!-- ✅ Image goes HERE — after details, before what-to-order -->
  <img src="https://img.tabiji.ai/..." alt="..." loading="lazy">
  <div class="what-to-order">
    ...
  </div>
</section>
```

### 7. Git commit (HTML only, never images)

```bash
cd ~/tabiji
git add popular-picks/<slug>/index.html
git commit -m "Add photos for <slug> popular picks"
git push origin main
```

---

## API Keys Required

| Key | Keychain name | Used for |
|-----|--------------|----------|
| SerpAPI | `serpapi-key` | Google Images search |
| Cloudflare R2 token | `cloudflare-pages-token` | Image upload to R2 |

Read from macOS Keychain:
```bash
security find-generic-password -s "serpapi-key" -w
security find-generic-password -s "cloudflare-pages-token" -w
```

---

## Integration with Popular Picks Page Builder

When building a new popular-picks page from scratch, the photo pipeline runs as part of the build:

1. **Create JSON data** (`popular-picks-data/<slug>.json`) with all picks
2. **Run photo pipeline** for each pick (search → score → optimize → upload to R2)
3. **Generate HTML** via `render-page.js` with R2 image URLs in the data
4. **Enrich with Google Places** data (ratings, hours, Maps links)
5. **Git push** HTML only

If the page already exists but has missing/placeholder photos, run the photo pipeline on just the gaps (check which picks already have working R2 images).

---

## Common Issues

- **SerpAPI returns no results:** Try broader query (just attraction + city, drop neighborhood). If still nothing, try a different search angle (e.g., "best coffee Shimokitazawa" instead of "Bear Pond Espresso").
- **Downloaded image is tiny/broken:** Skip files under 10KB. Some URLs return 403/404 — that's normal, just use the next candidate.
- **Vision scoring is expensive:** Batch all 5 candidates into one call, not 5 separate calls.
- **R2 upload fails:** Check the token hasn't expired. The `cloudflare-pages-token` has R2 Storage Edit scope.
- **Images not showing after push:** R2 URLs are instant (no build needed). If broken, check the key path matches exactly.
