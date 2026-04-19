# Scam Comic Pipeline — Generator, Storage, HTML

How every scam comic goes from prompt → generated image → R2 → the live scam page.

## 1. Generator: Nano Banana Pro (Gemini 2K) via Wavespeed

Nano Banana Pro is Google's Gemini image model, accessed through Wavespeed. It was selected for this project because it:
- Renders custom English dialogue reliably (Midjourney did not — "SARPER TOLT" gibberish in v6 tests)
- Supports style-anchoring via reference images (tighter consistency across a batch)
- Handles 2x2 comic-panel layouts correctly when prompted explicitly

### Credentials

- `wavespeed-api-key` in macOS keychain: `security find-generic-password -s wavespeed-api-key -w`
- `cloudflare-api-token` in macOS keychain: `security find-generic-password -s cloudflare-api-token -w` (R2-scoped; does NOT have zone/purge privileges)

### Endpoints

```
POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image
POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit
GET  https://api.wavespeed.ai/api/v3/predictions/<task_id>/result
```

### Text-to-image (first comic in a new country)

```json
POST /api/v3/google/nano-banana-pro/text-to-image
Authorization: Bearer <WAVESPEED_KEY>

{
  "prompt": "<full 3-block prompt>",
  "aspect_ratio": "1:1",
  "resolution": "2k",
  "output_format": "jpeg"
}
```

Response:
```json
{"code":200, "data": {"id":"<task_id>", "status":"created", ...}}
```

### Edit (every subsequent comic — tighter style lock)

```json
POST /api/v3/google/nano-banana-pro/edit
Authorization: Bearer <WAVESPEED_KEY>

{
  "prompt": "<full 3-block prompt>",
  "images": [
    "https://img.tabiji.ai/scams/<city>/scam-1.jpg",
    "https://img.tabiji.ai/scams/<city>/scam-2.jpg",
    "https://img.tabiji.ai/scams/<city>/scam-3.jpg"
  ],
  "aspect_ratio": "1:1",
  "output_format": "jpeg"
}
```

**Tip:** Pass 2–3 approved prior comics from the same country as `images`. They anchor palette, linework, and paper texture much tighter than text-only prompts. Too few → style drift; too many → the model sometimes copies characters from references. Three anchors is the sweet spot.

**Gotcha:** `edit-multi` does NOT support `aspect_ratio: "1:1"` (only 3:2, 2:3, 3:4, 4:3). Use plain `/edit` which supports 1:1 and accepts multiple images in the `images` array.

### Polling

```json
GET /api/v3/predictions/<task_id>/result
Authorization: Bearer <WAVESPEED_KEY>

-> {"code":200, "data": {"id":..., "status":"completed"|"failed"|"processing", "outputs":["<url>"], "error":""}}
```

Poll every 6–7 seconds. A typical generation completes in 30–90 seconds. Set a timeout of 10 minutes per job.

### Rate limits

Wavespeed enforces rate limits. Empirical behavior:
- **~5–10 concurrent submissions** is safe
- **~30 concurrent submissions** will start returning HTTP 429
- **~40+ concurrent submissions** will reliably 429

Strategies:
1. **Throttled sequential submit**: `sleep 0.5` between each `POST`. Works reliably up to ~200 scams.
2. **Parallel with backoff**: fire 10 at a time with retry on 429 (`sleep 3 + attempt*2`).
3. **Polling does NOT rate-limit** — polling 100 jobs in parallel is fine.

### Content filter

Gemini flags some prompts as "potentially sensitive" (empirically ~5% of scam comics). Retry with `text-to-image` endpoint (no reference images, more permissive filter). Examples seen:
- Beach/swim themes
- Nightlife venues
- Some restaurant scenes with bill shock
- Staged-violence scenarios (not present in our prompts, but if they appear, rephrase)

Rerunning the exact same prompt via `text-to-image` almost always succeeds.

## 2. Storage: Cloudflare R2 (bucket `tabiji-media`)

### Path convention

```
scams/<city-slug>/scam-<N>.jpg
```

Example: `scams/paris/scam-3.jpg`. N is the scam's 1-indexed position on the city page (match the order of `<div class="scam-card" id="scam-N">` in the HTML).

### Public URL

```
https://img.tabiji.ai/scams/<city-slug>/scam-<N>.jpg
```

### Uploading via the Cloudflare API

```
PUT https://api.cloudflare.com/client/v4/accounts/9ce95ed3e1df4a7e1d2a401e116c3c6f/r2/buckets/tabiji-media/objects/<key>
Authorization: Bearer <R2_TOKEN>
Content-Type: image/jpeg
Body: <raw jpeg bytes>
```

Response: `{"success": true, ...}`

### CDN cache

R2 files are cached by Cloudflare at the CDN edge. Consequences:
- **First fetch after upload** occasionally returns 404 if the path was negative-cached (empirically: if you `curl` a non-existent path before uploading, the 404 is cached for ~60 seconds).
- **Overwriting a file** does NOT invalidate the cache — browsers/curl continue serving the stale version until the cache naturally expires.

**Workarounds:**
1. Wait: cache TTL is short (1–5 minutes typical).
2. Cache-bust via query string: append `?v=2` (or higher integer) to the src in HTML. This forces a fresh fetch from R2.
3. Purge via the Cloudflare Zone API — **not available with the current token** (needs zone-scoped privileges; the R2 token is R2-scoped only). If you need purge, ask the human for a `cloudflare-purge-token`.

### Browser vs curl

`urllib.request` with the default User-Agent (`Python-urllib/3.x`) gets **HTTP 403 Forbidden** from `img.tabiji.ai` — Cloudflare's bot filter. Set `User-Agent: Mozilla/5.0` for verification requests. `curl` is unaffected.

## 3. HTML injection pattern

Each scam card on a city page gets an `<img class="scam-comic">` tag immediately after the `<div class="scam-location">`, before the story paragraphs.

### Exact tag

```html
<img class="scam-comic"
     src="https://img.tabiji.ai/scams/<city>/scam-<N>.jpg"
     alt="<short title> — comic illustration"
     loading="lazy"
     style="width:100%;height:auto;border-radius:12px;margin:1rem 0 1.25rem;display:block;">
```

Alt text is the scam title with parenthetical notes stripped, truncated to ~70 chars, plus `— comic illustration`.

Styling is **inline** — there is no `.scam-comic` CSS rule. (An older `.scam-illustration` rule exists in `assets/scams.css` from Japan but is no longer used.)

### Insertion point

Between `</div>` of `scam-location` and the opening `<p class="scam-story">` or `<p class="scam-story-body">` / `<p class="scam-tldr">`.

### Cache-busting when replacing

When you're replacing an existing comic (not a first-time add), append `?v=<N>` to the src:

```html
src="https://img.tabiji.ai/scams/paris/scam-1.jpg?v=2"
```

Increment the integer each time you replace. This forces browsers and the CDN to fetch fresh bytes even though the R2 path is unchanged.

## 4. Worked example: generate-and-ship for one city

See [example-city-walkthrough.md](example-city-walkthrough.md) for a full worked example of adding 8 comics to a new city end-to-end.

Or in short:

```bash
# 1. Extract scam titles + ids from the city HTML
python3 extract_scams.py --city barcelona > scams.json

# 2. Build prompts: one body JSON per scam with STYLE + CHARACTER + SCENE
python3 build_prompts.py --country spain --scams scams.json

# 3. Submit all to Wavespeed with throttled concurrency
python3 submit_jobs.py --endpoint edit --throttle 0.5

# 4. Poll until all completed
python3 poll_jobs.py --timeout 600

# 5. Download the completed image URLs
python3 download_results.py --out /tmp/comics/

# 6. Upload to R2 at scams/<city>/scam-<N>.jpg
python3 upload_r2.py --src /tmp/comics/ --path-prefix scams/

# 7. Inject img tags into city HTML
python3 inject_html.py --city barcelona

# 8. Commit + PR + merge + deploy
git add scams/barcelona/index.html
git commit -m "Add N Paco Roca scam comics to Barcelona"
gh pr create && gh pr merge --squash --delete-branch
```

(These scripts are not yet checked in — each country's scale-up has used ad-hoc versions in `/tmp/`. Promoting a canonical `scripts/comic-pipeline/` is a future clean-up task.)
