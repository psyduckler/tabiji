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
│  Visitor → tabiji.ai → /plan.html → free itinerary request      │
│                                              │                  │
│                                    direct order submission       │
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
Free itinerary request → orders/pending.json → Psy claims order →
  fulfill-order.js runs:
    1. generate-slug.js (unique slug)
    2. generate-itinerary-html.js (full HTML page)
    3. day-photos.js (hero image via AI)
    4. git add + commit + push
    5. Poll Cloudflare until page returns 200 (wait-for-deploy.sh)
    6. send-email.sh (Gmail, from psyduckler@gmail.com)
    7. Move order from pending.json → fulfilled.json
```

**Locking:** `fulfill-order.js` uses atomic mkdir (`.fulfillment.lockdir/`) to prevent concurrent fulfillments.

**Git hook:** `.githooks/pre-commit` rejects new `/i/` pages without a `hero-bg.png` or `hero-bg.jpg`, and verifies staged HTML's shared-head/nav/footer blocks are in sync with `_includes/` (see "Shared partials" below).

**Hook install:** `.githooks/` is not wired to `core.hooksPath` by default. Run once per clone:
```bash
bash scripts/install-hooks.sh
```
Without this, commits skip the hook entirely. CI (`.github/workflows/check-partials.yml`) catches drift at PR time regardless.

### Shared partials

`_includes/shared-head.html`, `nav-main.html`, `nav-export.html`, and `footer-default.html` are propagated into every page's managed block (`<!-- @include:*:start -->` … `<!-- @include:*:end -->`) by `scripts/build-partials.py`.

Workflow:
- **Normal page edits:** commit as usual. Pre-commit verifies staged HTML's managed blocks are current.
- **Editing `_includes/*.html`:** run `scripts/sync-partials.sh --stage` to propagate + stage updated files, then commit. CI enforces drift-free main.

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
| **Media Storage** | Cloudflare R2 | All images at `https://img.tabiji.ai/`, no images in git |
| **Email (outbound)** | Gmail + Resend | Itinerary delivery: Gmail (`psyduckler@gmail.com`) via `functions/send-email.sh`. Media-inquiry forwarding: Resend (`hello@tabiji.ai`) via `functions/api/media-inquiry.js` (Cloudflare Function — can't reach host `gws`). |
| **AI Agent** | Psy (OpenClaw) | Generates content, fulfills orders, manages SEO |
| **Maps** | Google Maps Embed API | Key: `AIzaSy...ASYc` |
| **API** | Static JSON (`/api/v1/`) | Pre-built by `api/build-api.py`, zero runtime cost |
| **CI/CD** | GitHub → Cloudflare Pages | Push to `main` auto-deploys, no build step |
| **DNS** | Cloudflare | `tabiji.ai` nameservers on Cloudflare |
| **Monitoring** | Cloudflare Analytics + Google Search Console | |

---

## 3. Repo Structure

### 3.1 Current Stats

*Last verified: 2026-05-01. Counts exclude `.git/` and `.claude/worktrees/`.*

| Metric | Value |
|--------|-------|
| **Total HTML pages** (`*.html` recursive) | ~3,412 |
| **Total JSON files** (`*.json` recursive) | ~2,816 |
| **JS scripts** (`*.js` recursive) | ~74 |
| **Python scripts** (`*.py` recursive) | ~477 |
| **Working tree size** | ~454 MB |
| **`.git` size** | ~604 MB (after PR #1411/#1415 R2 migration + `git gc`) |

### 3.2 Content Directories (Live Pages)

*Counts as of 2026-05-01 (file count of `index.html` per directory).*

| Directory | Count | Description |
|-----------|-------|-------------|
| `compare/` | 855 | VS comparison pages (e.g., Bali vs Thailand) |
| `scams/` | 660 | Scam awareness pages by destination |
| `i/` | 401 | Paid customer itineraries (delivered products) |
| `health/` | 235 | Health & vaccination info by destination |
| `countries/` | 211 | Country info pages |
| `destinations/` | 69 | City destination pages |

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
├── deploy.sh                ← clean-push deploy helper
│
├── i/                       ← paid itineraries (400 slugs)
├── compare/                 ← VS comparison pages (926 slugs)
├── scams/                   ← scam awareness pages (546 destinations)
├── health/                  ← health info pages (228 destinations)
├── countries/               ← country info pages (211 countries)
├── destinations/            ← city destination pages (69 cities)
│
├── owl/                     ← Owl interactive assistant
├── trends/                  ← travel trends tool
├── about/                   ← about page
├── privacy/                 ← privacy policy
├── terms/                   ← terms of service
├── delete-data/             ← data deletion page
│
├── functions/               ← core scripts (fulfillment, enrichment, email)
├── scripts/                 ← batch generators, one-off scripts, utilities
├── generators/              ← page generators (compare)
├── api/                     ← static JSON API + build script (~1,703 JSON files)
├── _includes/               ← shared HTML partials (nav, footer, head)
├── .well-known/             ← agent discovery (ai-plugin.json, agents.json)
├── .githooks/               ← pre-commit hooks (itinerary safeguards)
│
├── orders/                  ← order data (pending.json, fulfilled.json)
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
| `send-email.sh` | Sends delivery email via Gmail |
| `wait-for-deploy.sh` | Polls Cloudflare until page is live |
| `email-template.js` | Email formatting |

**Content Generation** (`functions/` + `scripts/`):
| Script | Purpose |
|--------|---------|
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
Trigger (free itinerary request / queue file / Bernard's request)
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
| `orders/pending.json` | Active itinerary request queue |
| `orders/fulfilled.json` | Completed orders archive |
| `scripts/queues/compare-queue.json` | Compare page batch queue |

### Escalation Paths

- **Fulfillment fails** → Psy alerts Bernard via Slack
- **Customer complaint** → Psy attempts resolution, escalates if unresolved
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
| `/i/` (custom itineraries) | `functions/fulfill-order.js` → `generate-itinerary-html.js` |
| `/compare/` | Sub-agents + generator scripts |
| `/alerts/` | `functions/build-travel-alerts.py` |
| `/scams/` | Sub-agents |
| `/health/` | `scripts/build-health-page.py` |
| Landing pages | Hand-crafted (`index.html`, `plan.html`, `success.html`) |

### 5.3 Navigation & Footer

Every page has its **own copy** of the nav and footer baked in. Shared partials exist in `_includes/` (`nav-main.html`, `footer-default.html`, `shared-head.html`) but are injected at generation time, not at serve time.

**⚠️ Changing the nav/footer means updating ~3,500 pages.** Use `_includes/` partials + a build script for bulk updates.

### 5.4 Images & Media

- **ALL images served from Cloudflare R2** via `https://img.tabiji.ai/`
- The git repo has **no content images** — only HTML/CSS/JS/JSON
- R2 key structure mirrors repo paths for active route families.
- Google Maps embeds use the shared API key

---

## 6. API Layer

Static JSON API at `/api/v1/` — **~1,703 pre-built JSON files (after #289 consolidated 6,907 per-slug destination files into a single bundle served by a Pages Function)**. Built by `api/build-api.py` which reads all HTML pages and extracts structured data. Zero runtime cost — just static files served by Cloudflare Pages.

Agent discovery files in `.well-known/` (`ai-plugin.json`, `agents.json`) allow AI tools to discover and use the API.

OpenAPI spec at `api/openapi.json`.

---

## 7. Enrichment & Content Pipelines

### 7.1 Compare Pipeline

Compare pages are generated in batches via queue files and generator scripts in `generators/compare/`.

### 7.2 Travel Alerts Pipeline

`functions/build-travel-alerts.py` generates all 224 country alert pages from State Department data.

---

---

## 8. Infrastructure

### Domain & DNS
- `tabiji.ai` → Cloudflare DNS (nameservers)
- `img.tabiji.ai` → Cloudflare R2 (media bucket: `tabiji-media`)

### Environment & Secrets
```
gws auth                 → host login for psyduckler@gmail.com (itinerary delivery via functions/send-email.sh)
RESEND_API_KEY           → macOS Keychain (used by functions/api/media-inquiry.js only; not the itinerary path)
CLOUDFLARE_PAGES_TOKEN   → macOS Keychain (cloudflare-pages-token)
R2_BUCKET                → tabiji-media (account: 9ce95ed3e1df4a7e1d2a401e116c3c6f)
```

All secrets accessed via `security find-generic-password` at runtime. Nothing hardcoded in the repo.

### Monitoring
- **Uptime**: Cloudflare Analytics
- **SEO**: Google Search Console (Psy checks regularly)
- **Orders**: `orders/pending.json` monitored for stuck orders

---

## 9. Critical Path Dependencies

```
                    ┌─────────────────┐
                    │ Itinerary Request │
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

**If fulfill-order.js breaks, requesters don't get their itineraries.**

Other dependency chains:
- Travel alerts → `build-travel-alerts.py` generates all 224 alert pages
- API → `api/build-api.py` reads all HTML pages to generate ~1,703 JSON files

---

*Document authored by Psy. Last updated: 2026-04-01.*
