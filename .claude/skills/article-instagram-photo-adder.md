---
name: article-instagram-photo-adder
description: Find and add photos to a tabiji popular-picks page. For each recommendation, search Google Images via SerpAPI, score candidates with Gemini Vision, optimize to 800px JPEG, upload to Cloudflare R2, and update the HTML. Trigger when user says "add photos to [slug]" or "article-instagram-photo-adder".
user_invocable: true
---

# Article Photo Adder

Add high-quality photos to every recommendation on a tabiji popular-picks page.

## When to use
- After building a new popular-picks page
- When a page is missing photos
- User says "add photos to [slug]" or "article-instagram-photo-adder"

## Required input
A popular-picks slug (e.g., `detroit-pizza`). The HTML page must already exist at `popular-picks/[slug]/index.html`.

## Quick method (recommended)

Run the existing script:
```bash
python3 scripts/add_photos_for_page.py [slug]
```

This handles the full workflow automatically. For batch processing:
```bash
for slug in page1 page2 page3; do
  python3 -u scripts/add_photos_for_page.py "$slug" >> "/tmp/photos-$slug.log" 2>&1 &
done
```

## Manual workflow (if script fails)

### 1. Parse the page
Read `popular-picks/[slug]/index.html`. Extract each recommendation:
- `<h2>` with `restaurant-number` span = venue name
- `<img>` tag = target image path
- Section ID = filename for the image

### 2. Search for photos
Use SerpAPI Google Images:
```bash
SERPAPI_KEY=$(security find-generic-password -s serpapi-key -w)
curl -s "https://serpapi.com/search.json?engine=google_images&q=[VENUE]+[CITY]+restaurant+food&api_key=$SERPAPI_KEY&num=5&safe=active"
```

Filter results: width >= 400, height >= 300, not SVG.

### 3. Score with Gemini Vision
For each candidate image:
1. Download to temp directory
2. Resize to 400px for scoring payload
3. Send to Gemini with prompt: "Rate this image 1-10 for a travel guide photo of '[venue name]'. Consider quality, relevance, no watermarks."
4. Pick the highest-scoring candidate (minimum score: 3)

```
GEMINI_KEY=$(security find-generic-password -s gemini-api-key -w)
GEMINI_URL="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GEMINI_KEY"
```

### 4. Optimize the winner
```bash
sips --resampleWidth 800 input.jpg --out output.jpg
sips -s format jpeg -s formatOptions 80 output.jpg --out output.jpg
```
Target: 800px wide, ~80% JPEG quality.

### 5. Upload to Cloudflare R2
```bash
CF_TOKEN=$(security find-generic-password -s cloudflare-api-token -w)
CF_ACCOUNT="9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_KEY="popular-picks/[slug]/[section-id].jpg"

curl -s -X PUT \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: image/jpeg" \
  --data-binary @"output.jpg" \
  "https://api.cloudflare.com/client/v4/accounts/$CF_ACCOUNT/r2/buckets/tabiji-media/objects/$R2_KEY"
```

The public URL will be: `https://img.tabiji.ai/popular-picks/[slug]/[section-id].jpg`

### 6. Verify
The HTML already has `<img src="https://img.tabiji.ai/popular-picks/[slug]/[section-id].jpg">`. No HTML changes needed — the image just needs to exist at the R2 path.

### 7. Report
Log progress for each venue:
```
✅ [2/10] Venue Name — scored 3 candidates, winner: score 8/10
❌ [5/10] Venue Name — no images found, skipped
```

## Important notes
- Images are served from `img.tabiji.ai` (Cloudflare R2 CDN) — never commit image files to the git repo
- The HTML repo only contains the `<img>` tags with CDN URLs
- If SerpAPI returns no results for a venue, skip it (don't fail the whole run)
- Clean up temp download directories after completion
- Rate limit: 0.5-1s between Gemini scoring calls, 1s between SerpAPI calls

## Related files
- Photo script: `scripts/add_photos_for_page.py`
- Existing photo fixer: `scripts/fix-missing-pp-photos.py`
