# tabiji.ai — Architecture Document

> 旅路 (tabiji) = "journey" in Japanese
> An AI-operated travel itinerary business, autonomously run by Psy.

---

## 1. System Overview

tabiji.ai is a **static HTML site** deployed on **Cloudflare Pages**. There is no framework — no Next.js, no SSR, no build step. Every page is a self-contained `index.html` with inline `<style>` and `<script>`. The site is generated and maintained by Python and JavaScript scripts orchestrated by Psy (an AI agent running on OpenClaw).

```
┌─────────────────────────────────────────────────────────────────┐
│                        CUSTOMER FLOW                            │
│                                                                 │
│  Customer → tabiji.ai → /plan.html → Stripe Checkout            │
│                                              │                  │
│                                    webhook (payment.success)    │
│                                              │                  │
│                                              ▼                  │
│                                   ┌──────────────────┐          │
│                                   │ orders/pending.json│         │
│                                   └────────┬─────────┘          │
│                                            │                    │
│                                            ▼                    │
│                              ┌─────────────────────────┐        │
│                              │     PSY (AI Agent)      │        │
│                              │                         │        │
│                              │  fulfill-order.js:      │        │
│                              │  1. Generate slug       │        │
│                              │  2. Build HTML page     │        │
│                              │  3. Generate hero image │        │
│                              │  4. Git push → CF Pages │        │
│                              │  5. Poll until live     │        │
│                              │  6. Email customer      │        │
│                              └─────────────────────────┘        │
│                                            │                    │
│                                   orders/fulfilled.json         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     MARKETING / SEO FLOW                        │
│                                                                 │
│  Psy → Research destinations → Generate static HTML pages       │
│      → Enrich with Google Places data → AEO upgrade             │
│      → Git push → Cloudflare Pages auto-deploys                 │
└─────────────────────────────────────────────────────────────────┘
```

### Deploy Flow

```
git push to main → GitHub → Cloudflare Pages auto-builds → Live at tabiji.ai
```

No build command. Cloudflare Pages serves the repo directory as-is. `deploy.sh` is a convenience wrapper for clean commits + push.

---

## 1.5. ⚠️ Itinerary Fulfillment Rules (MANDATORY)

**ALL itinerary fulfillments MUST go through `functions/fulfill-order.js`.**

Do NOT manually:
- Build HTML, git push, and send email as separate steps
- Send email without verifying the Cloudflare Pages deployment is live
- Bypass the polling/verification logic

`fulfill-order.js` handles: slug generation → HTML build → hero image → git push → **poll URL until 200** → send email → update pending.json → fulfilled.json.

### Pipeline Detail

```
Stripe webhook → orders/pending.json → Psy claims order →
  fulfill-order.js runs:
    1. generate-slug.js (unique slug)
    2. generate-itinerary-html.js (full HTML page)
    3. day-photos.js (hero image via AI)
    4. git add + commit + push
    5. Poll Cloudflare until page returns 200 (wait-for-deploy.sh)
    6. send-email.sh (Resend, from hello@tabiji.ai)
    7. Move order from pending.json → fulfilled.json
```

**Locking:** `fulfill-order.js` uses atomic mkdir (`.fulfillment.lockdir/`) to prevent concurrent fulfillments.

**Git hook:** `.githooks/pre-commit` rejects new `/i/` pages without a `hero-bg.png` or `hero-bg.jpg`.

### Utilities
- **`functions/wait-for-deploy.sh <url> [max_seconds] [interval_seconds]`** — standalone deploy verification. Used by fulfill-order.js internally. Also available as a safety net.
- **`functions/send-email.sh --verify-url <url>`** — pass `--verify-url` to block email sending until the URL returns 200. Acts as a last-resort safeguard even if fulfill-order.js is bypassed.

### Why?
On Feb 18, 2026, a sub-agent fulfilled the Lima Peru order by manually pushing + emailing without waiting for Cloudflare deployment. Customer received the email but the page was still 404.

---

## 2. Tech Stack

| Layer | Choice | Notes |
|-------|--------|-------|
| **Frontend** | Static HTML (no framework) | Self-contained `index.html` pages with inline CSS/JS |
| **Hosting** | Cloudflare Pages | Auto-deploys from `main` branch, edge-served globally |
| **Payments** | Stripe Checkout | Webhooks trigger order fulfillment |
| **Media Storage** | Cloudflare R2 | All images at `https://img.tabiji.ai/`, no images in git |
| **Email (outbound)** | Resend (hello@tabiji.ai) | Via `functions/send-email.sh` |
| **AI Agent** | Psy (OpenClaw) | Generates content, fulfills orders, manages SEO |
| **Maps** | Google Maps Embed API | Key: `AIzaSyBP0yidMjJEECgkIiZz2lw1NLsQ7jdASYc` |
| **API** | Static JSON (`/api/v1/`) | Pre-built by `api/build-api.py`, zero runtime cost |
| **CI/CD** | GitHub → Cloudflare Pages | Push to `main` auto-deploys, no build step |
| **DNS** | Cloudflare | `tabiji.ai` nameservers on Cloudflare |
| **Monitoring** | Cloudflare Analytics + Google Search Console | |

---

## 3. Repo Structure

### 3.1 Current Stats

| Metric | Value |
|--------|-------|
| **Total HTML pages** | ~3,542 |
| **Total JSON files** | ~12,913 |
| **JS scripts** | ~142 |
| **Python scripts** | ~97 |
| **Repo size** | ~1.7 GB (1.1 GB in `.git`) |

### 3.2 Content Directories (Live Pages)

| Directory | Count | Description |
|-----------|-------|-------------|
| `popular-picks/` | ~1,439 | Food & activity guides (SEO backbone) |
| `compare/` | ~1,158 | VS comparison pages (e.g., Bali vs Thailand) |
| `i/` | ~352 | Paid customer itineraries (delivered products) |
| `alerts/` | ~224 | Travel safety alerts by country |
| `scams/` | ~99 | Scam awareness pages by destination |
| `health/` | ~52 | Health & vaccination info by destination |
| `credit-cards/` | ~50 | Travel credit card reviews |
| `itineraries/` | ~49 | Free curated itineraries |
| `resources/` | ~35 | Blog / resource articles |
| `best-places-to-visit-in-*/` | 12 | Monthly destination guides |
| `destinations/` | 9 | Legacy city destination pages |

### 3.3 Top-Level Layout

```
tabiji/
├── ARCHITECTURE.md          ← this file
├── REFACTOR-BRIEF.md        ← refactor guide for contributors
├── index.html               ← landing page
├── plan.html                ← order form (revenue-critical)
├── success.html             ← post-payment confirmation
├── 404.html                 ← custom error page
├── robots.txt / sitemap.xml ← SEO
├── manifest.json / sw.js    ← PWA support
├── deploy.sh                ← clean-push deploy helper
│
├── i/                       ← paid itineraries (352 slugs)
├── popular-picks/           ← food/activity guides (1,439 slugs)
├── compare/                 ← VS comparison pages (1,158 slugs)
├── alerts/                  ← travel safety alerts (224 countries)
├── scams/                   ← scam awareness pages (99 destinations)
├── health/                  ← health info pages (52 destinations)
├── credit-cards/            ← credit card reviews (50 cards)
├── itineraries/             ← free curated itineraries (49 slugs)
├── resources/               ← blog/articles (35 slugs)
├── best-places-to-visit-in-*/ ← monthly guides (12 months)
├── destinations/            ← legacy city pages (9 cities)
├── country/                 ← country info pages
│
├── find/                    ← destination finder tool
├── owl/                     ← Owl interactive assistant
├── spin/                    ← destination spinner tool
├── kit/                     ← travel kit builder
├── recommend/               ← recommendation pages by theme
├── trends/                  ← travel trends tool
├── about/                   ← about page
├── privacy/                 ← privacy policy
├── terms/                   ← terms of service
├── delete-data/             ← data deletion page
│
├── functions/               ← core scripts (fulfillment, enrichment, email)
├── scripts/                 ← batch generators, one-off scripts, utilities
├── generators/              ← page generators (compare, popular-picks)
├── api/                     ← static JSON API + build script (~10,991 JSON files)
├── _includes/               ← shared HTML partials (nav, footer, head)
├── .well-known/             ← agent discovery (ai-plugin.json, agents.json)
├── .githooks/               ← pre-commit hooks (itinerary safeguards)
│
├── orders/                  ← order data (pending.json, fulfilled.json)
├── popular-picks-data/      ← data files for popular picks
├── popular-picks-hub-data/  ← hub page data
├── compare-data/            ← data files for compare pages
├── emergency-data/          ← emergency info data
├── health-data/             ← health data files
├── research/                ← research notes and data
├── docs/                    ← internal documentation
├── logs/                    ← operation logs
├── emails/                  ← email drafts/records
├── archive/                 ← archived scripts and data
├── tmp/                     ← temporary working files
├── samples/                 ← sample pages/templates
│
├── *-queue.json             ← batch processing queues (root)
└── export-doc/              ← export utilities
```

### 3.4 Key Scripts

**Fulfillment Pipeline** (`functions/`):
| Script | Purpose |
|--------|---------|
| `fulfill-order.js` | **Orchestrator** — runs the entire fulfillment pipeline |
| `generate-itinerary-html.js` | Generates HTML for paid itineraries |
| `generate-slug.js` | Creates unique URL slugs |
| `day-photos.js` | Generates hero images via AI |
| `send-email.sh` | Sends delivery email via Resend |
| `wait-for-deploy.sh` | Polls Cloudflare until page is live |
| `email-template.js` | Email formatting |

**Content Generation** (`functions/` + `scripts/`):
| Script | Purpose |
|--------|---------|
| `functions/enrich-popular-picks.py` | Google Places enrichment (ratings, hours, links) |
| `scripts/aeo-upgrade-popular-picks.py` | AEO answer-first + JSON-LD injection |
| `functions/add-related-links.js` | Cross-links between related picks |
| `functions/build-travel-alerts.py` | Generates all 224 alert pages |
| `api/build-api.py` | Builds static JSON API from HTML pages |

**Publishing** (`functions/`):
| Script | Purpose |
|--------|---------|
| `publish-reel.sh` | Publish video reel to Instagram |
| `publish-tiktok.sh` | Publish to TikTok |
| `publish-youtube-short.sh` | Publish to YouTube Shorts |

---

## 4. The "Psy as Operator" Model

Psy is not a microservice — Psy is the operator. The system is designed so that Psy runs scripts, generates content, fulfills orders, and manages the site like a human operator would.

### Trigger → Work → Deliver Pattern

```
Trigger (Stripe webhook / queue file / Bernard's request)
    → Psy picks up task
    → Psy runs appropriate script(s)
    → Output generated (HTML pages, emails, data)
    → Git push → Cloudflare Pages auto-deploys
    → Psy confirms delivery / logs completion
```

### Queue System

Orders and batch jobs are tracked via JSON files:

| File | Purpose |
|------|---------|
| `orders/pending.json` | Active paid order queue |
| `orders/fulfilled.json` | Completed orders archive |
| `popular-picks-queue.json` | Batch popular-picks creation queue |
| `compare-queue.json` | Compare page batch queue |
| `country-fills-queue.json` | Country page fill queue |

### Escalation Paths

- **Fulfillment fails** → Psy alerts Bernard via Slack
- **Customer complaint** → Psy attempts resolution, escalates if unresolved
- **Refund request** → Psy processes if within policy, otherwise escalates
- **System error** → Logged + Slack alert to Bernard

---

## 5. Page Architecture

### 5.1 Self-Contained Pages

Every page is **fully self-contained HTML** with inline CSS. There are NO shared stylesheets or JS bundles in production. Each page type uses CSS variables for theming:

```css
:root {
  --indigo: #1a1a2e;
  --sand: #c2b280;
  --cream: #faf8f5;
}
```

### 5.2 Page Generation Sources

| Page Type | Generated By |
|-----------|-------------|
| `/i/` (paid itineraries) | `functions/fulfill-order.js` → `generate-itinerary-html.js` |
| `/popular-picks/` | Sub-agents + enrichment pipeline |
| `/compare/` | Sub-agents + generator scripts |
| `/alerts/` | `functions/build-travel-alerts.py` |
| `/scams/` | Sub-agents |
| `/health/` | `scripts/build-health-page.py` |
| `/credit-cards/` | Sub-agents |
| `/best-places-to-visit-in-*/` | Sub-agents (reference: `best-places-template.html`) |
| Landing pages | Hand-crafted (`index.html`, `plan.html`, `success.html`) |

### 5.3 Navigation & Footer

Every page has its **own copy** of the nav and footer baked in. Shared partials exist in `_includes/` (`nav-main.html`, `footer-default.html`, `shared-head.html`) but are injected at generation time, not at serve time.

**⚠️ Changing the nav/footer means updating ~3,500 pages.** Use `_includes/` partials + a build script for bulk updates.

### 5.4 Images & Media

- **ALL images served from Cloudflare R2** via `https://img.tabiji.ai/`
- The git repo has **no content images** — only HTML/CSS/JS/JSON
- R2 key structure mirrors repo paths: `i/{slug}/hero-bg.jpg`, `popular-picks/{slug}/{photo}.jpg`
- Google Maps embeds use the shared API key

---

## 6. API Layer

Static JSON API at `/api/v1/` — **~10,991 pre-built JSON files**. Built by `api/build-api.py` which reads all HTML pages and extracts structured data. Zero runtime cost — just static files served by Cloudflare Pages.

Agent discovery files in `.well-known/` (`ai-plugin.json`, `agents.json`) allow AI tools to discover and use the API.

OpenAPI spec at `api/openapi.json`.

---

## 7. Enrichment & Content Pipelines

### 7.1 Popular Picks Pipeline

After creating a new popular-picks page:
1. `python3 functions/enrich-popular-picks.py <slug>` — Google Places data (ratings, hours, Maps links)
2. `python3 scripts/aeo-upgrade-popular-picks.py --slug <slug>` — AEO answer-first + JSON-LD
3. `node functions/add-related-links.js` — cross-links to related picks
4. Git commit + push

### 7.2 Compare Pipeline

Compare pages are generated in batches via queue files and generator scripts in `generators/compare/`.

### 7.3 Travel Alerts Pipeline

`functions/build-travel-alerts.py` generates all 224 country alert pages from State Department data.

---

## 2.0 — AEO (Answer Engine Optimization) Pattern

All popular-picks pages MUST include these two AEO elements. This ensures AI assistants (ChatGPT, Gemini, Perplexity) can extract and cite our content.

### 2.0.1 Answer-First Blocks

Every section's first sentence must be a **self-contained, citable fact** containing: name, key differentiator, price, and location.

**Intro paragraph:** Add a bold `<p><strong>...</strong></p>` as the first paragraph inside `.intro-section`, before the existing descriptive text. This summary should cover: price range across all options, top recommendation, key qualifiers (season, location, etc).

**Each pick's description (`.what-to-order` div):** The first sentence after the `<strong>` label must include the place name, what makes it notable, price, and rating. Example:

```
❌ Before: "Book a 2–3 day trip with overnight island camping. The trust coordinates..."
✅ After: "The Okavango Kopano Mokoro Community Trust is the most affordable mokoro experience in the delta at $35–$65/day, with community-employed polers operating from Boro Village near Maun. Book a 2–3 day trip with overnight island camping..."
```

### 2.0.2 Agent Brief JSON-LD (TouristTrip)

Add a `<script type="application/ld+json">` block with `@type: TouristTrip` before `<style>`. Fields via `additionalProperty`:

- `totalOptions` — number of picks on the page
- `priceRangeUSD` — min–max across all picks
- `bestBudgetOption` — name + price + rating
- `bestLuxuryOption` — name + price + rating (if applicable)
- `bestOverall` — highest rated with most reviews
- `topPick` — #1 pick with details
- `sourcesAnalyzed` — "80+ Reddit posts" etc
- `lastVerified` — "2026-03" (update on each verification pass)

### 2.0.3 Post-Creation Script

After creating a new popular-picks page, run the AEO upgrade as a post-processing step:
```bash
python3 ~/tabiji/scripts/aeo-upgrade-popular-picks.py --slug <new-page-slug>
```
This handles both the answer-first rewrites (via Gemini Flash) and JSON-LD injection automatically.

### 2.0.4 Enrichment Pipeline (Full)

For any new popular-picks page, the complete post-creation pipeline is:
1. `python3 ~/tabiji/functions/enrich-popular-picks.py <slug>` — Google Places data (ratings, hours, phone, Maps links)
2. `python3 ~/tabiji/scripts/aeo-upgrade-popular-picks.py --slug <slug>` — AEO answer-first + JSON-LD
3. `node ~/tabiji/functions/add-related-links.js` — cross-links to related picks
4. Git commit + push

---

## 8. Infrastructure

### Domain & DNS
- `tabiji.ai` → Cloudflare DNS (nameservers)
- `img.tabiji.ai` → Cloudflare R2 (media bucket: `tabiji-media`)

### Environment & Secrets
```
STRIPE_SECRET_KEY        → macOS Keychain
STRIPE_WEBHOOK_SECRET    → macOS Keychain
RESEND_API_KEY           → macOS Keychain
CLOUDFLARE_PAGES_TOKEN   → macOS Keychain (cloudflare-pages-token)
R2_BUCKET                → tabiji-media (account: 9ce95ed3e1df4a7e1d2a401e116c3c6f)
```

All secrets accessed via `security find-generic-password` at runtime. Nothing hardcoded in the repo.

### Monitoring
- **Uptime**: Cloudflare Analytics
- **SEO**: Google Search Console (Psy checks regularly)
- **Revenue**: Stripe dashboard
- **Orders**: `orders/pending.json` monitored for stuck orders

---

## 9. Critical Path Dependencies

```
                    ┌─────────────────┐
                    │  Stripe Webhook  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  pending.json   │ ◄── DO NOT change schema
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ fulfill-order.js│ ◄── Orchestrator (DO NOT refactor)
                    ├─────────────────┤
                    │ • generate-slug │
                    │ • generate-html │
                    │ • day-photos    │
                    │ • git push      │
                    │ • wait-for-deploy│
                    │ • send-email    │
                    │ • update json   │
                    └─────────────────┘
                             │
                    ┌────────┴────────┐
                    │  fulfilled.json │
                    └─────────────────┘
```

**If fulfill-order.js breaks, customers don't get their itineraries and revenue stops.**

Other dependency chains:
- Popular-picks creation → `enrich-popular-picks.py` → `aeo-upgrade-popular-picks.py` → `add-related-links.js`
- Travel alerts → `build-travel-alerts.py` generates all 224 alert pages
- API → `api/build-api.py` reads all HTML pages to generate ~10,991 JSON files

---

*Document authored by Psy. Last updated: 2026-04-01.*
