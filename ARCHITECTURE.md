# tabiji.ai — Architecture Document

> 旅路 (tabiji) = "journey" in Japanese
> An AI-operated travel itinerary business, autonomously run by Psy.

---

## 1. System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        CUSTOMER FLOW                            │
│                                                                 │
│  Customer → Landing Page → Order Form → Stripe Checkout         │
│                                              │                  │
│                                    webhook (payment.success)    │
│                                              │                  │
│                                              ▼                  │
│                                   ┌──────────────────┐          │
│                                   │   Order Queue    │          │
│                                   │  (KV / D1 / R2)  │          │
│                                   └────────┬─────────┘          │
│                                            │                    │
│                                            ▼                    │
│                              ┌─────────────────────────┐        │
│                              │     PSY (AI Agent)      │        │
│                              │                         │        │
│                              │  1. Research (Reddit,   │        │
│                              │     web, forums)        │        │
│                              │  2. Generate itinerary  │        │
│                              │  3. Format & QA         │        │
│                              │  4. Email to customer   │        │
│                              └─────────────────────────┘        │
│                                            │                    │
│                                            ▼                    │
│                                   Gmail (psyduckler)            │
│                                   → Customer inbox              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     MARKETING FLOW                              │
│                                                                 │
│  Psy → Research trending destinations → Generate SEO pages      │
│      → Publish to /destinations/[slug]                          │
│      → Monitor rankings → Refresh stale content                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Frontend** | Next.js (App Router) | SSR/SSG for SEO, React ecosystem, easy programmatic pages |
| **Hosting** | Cloudflare Pages | Edge-first, cheap at scale, D1/KV/R2 built-in, no cold starts |
| **Payments** | Stripe Checkout | Industry standard, webhooks, no PCI hassle |
| **Database** | Cloudflare D1 (SQLite) | Orders, customers, itinerary metadata. Free tier is generous |
| **File Storage** | Cloudflare R2 | Store generated itinerary PDFs, images. S3-compatible, no egress fees |
| **KV Store** | Cloudflare KV | Session data, feature flags, rate limits |
| **Email (outbound)** | Gmail API (psyduckler@gmail.com) | Already set up, works now. Migrate to Resend/Postmark at scale |
| **Email (inbound)** | Cloudflare Email Workers | Route support@tabiji.ai to Psy |
| **AI Agent** | Psy (OpenClaw) | Already has Reddit scraping, web research, Playwright, Gmail |
| **Monitoring** | Cloudflare Analytics + UptimeRobot | Free, sufficient for v1 |
| **CI/CD** | GitHub Actions → Cloudflare Pages | Auto-deploy on push to main |

### Why Cloudflare over Vercel?
- D1/KV/R2 = integrated data layer, no external DB needed
- Email Workers = inbound email handling without third-party service
- Cheaper at scale (generous free tier, no per-seat pricing)
- Edge-first = fast globally (travel customers are worldwide)

---

## 3. Repo Structure

```
tabiji/
├── README.md
├── ARCHITECTURE.md          ← this file
├── package.json
├── next.config.js
├── wrangler.toml            ← Cloudflare config
│
├── src/
│   ├── app/
│   │   ├── layout.tsx       ← root layout, nav, footer
│   │   ├── page.tsx         ← landing page
│   │   ├── order/
│   │   │   └── page.tsx     ← order form (destination, dates, preferences)
│   │   ├── checkout/
│   │   │   ├── page.tsx     ← Stripe checkout redirect
│   │   │   └── success/
│   │   │       └── page.tsx ← post-payment confirmation
│   │   ├── destinations/
│   │   │   ├── page.tsx     ← destination index (SEO hub)
│   │   │   └── [slug]/
│   │   │       └── page.tsx ← programmatic SEO pages
│   │   ├── blog/
│   │   │   ├── page.tsx
│   │   │   └── [slug]/
│   │   │       └── page.tsx
│   │   └── api/
│   │       ├── webhook/
│   │       │   └── stripe/route.ts   ← Stripe webhook handler
│   │       ├── order/route.ts        ← create order
│   │       └── contact/route.ts      ← support form
│   │
│   ├── lib/
│   │   ├── stripe.ts
│   │   ├── db.ts            ← D1 helpers
│   │   ├── email.ts         ← Gmail send wrapper
│   │   └── queue.ts         ← order queue helpers
│   │
│   ├── components/
│   │   ├── Hero.tsx
│   │   ├── Pricing.tsx
│   │   ├── OrderForm.tsx
│   │   └── ...
│   │
│   └── content/
│       ├── destinations/    ← MDX or JSON for programmatic pages
│       └── blog/            ← blog posts
│
├── scripts/
│   ├── generate-seo-pages.ts    ← Psy runs this to create destination content
│   └── seed-destinations.ts
│
├── public/
│   ├── favicon.ico
│   ├── og-image.png
│   └── ...
│
└── .github/
    └── workflows/
        └── deploy.yml
```

---

## 4. The "Psy as Operator" Model

Psy is not a microservice — Psy is the operator. The system is designed so webhooks and queues trigger Psy to do work, like a human checking their inbox.

### Trigger → Work → Deliver Pattern

```
Trigger (webhook/cron/email)
    → OpenClaw receives notification
    → Psy picks up task
    → Psy does research + generation
    → Psy delivers output (email/publish/reply)
    → Psy logs completion
```

### Queue System

Orders are stored in D1 with status tracking:

```sql
CREATE TABLE orders (
    id TEXT PRIMARY KEY,
    stripe_session_id TEXT,
    customer_email TEXT NOT NULL,
    customer_name TEXT,
    destination TEXT NOT NULL,
    travel_dates TEXT,
    preferences TEXT,        -- JSON: budget, pace, interests, dietary, etc.
    status TEXT DEFAULT 'paid',  -- paid → researching → generating → review → delivered → complete
    itinerary_url TEXT,      -- R2 URL to final PDF
    created_at INTEGER,
    updated_at INTEGER
);
```

Status flow: `paid → researching → generating → review → delivered`

### Escalation Paths

- **Generation fails 2x** → Psy alerts Bernard via Slack
- **Customer complaint** → Psy attempts resolution, escalates if unresolved after 1 exchange
- **Refund request** → Psy processes if within policy, otherwise escalates
- **System error** → Logged + Slack alert to Bernard

---

## 5. Itinerary Generation Pipeline

When Psy receives a new order:

### Step 1: Research (5-10 min)
```
1. Reddit search: "best things to do in {destination}" across:
   - r/travel, r/solotravel, r/backpacking
   - r/{destination} (city-specific subs)
   - Sort by top/year for current recs
2. Web scraping: local blogs, tourism sites
3. Google Maps: distances, opening hours, logistics
4. Cross-reference: identify consensus recommendations vs tourist traps
```

### Step 2: Generate (2-5 min)
```
1. Build day-by-day itinerary based on:
   - Travel dates & duration
   - Customer preferences (budget, pace, interests)
   - Logical geographic clustering (minimize transit)
   - Mix of highlights + hidden gems from Reddit
2. Include for each activity:
   - Why it's recommended (cite Reddit/source)
   - Practical details (hours, cost, booking links)
   - Insider tips from real travelers
3. Add logistics: transport between areas, SIM card, money tips
```

### Step 3: Format & QA
```
1. Generate clean HTML email version
2. Generate PDF version (store in R2)
3. Self-review: check for hallucinated info, broken links
4. Verify all dates/days-of-week are correct
```

### Step 4: Deliver
```
1. Send email via Gmail with:
   - Inline HTML itinerary
   - PDF attachment link
   - "Reply to this email for questions" CTA
2. Update order status to 'delivered'
3. Schedule follow-up email (3 days post-trip-start)
```

---

## 6. Customer Support Flow

```
Inbound email (support@tabiji.ai or reply)
    → Cloudflare Email Worker → forwards to Psy
    → Psy classifies:
        ├─ Question about itinerary → Answer from order context
        ├─ Modification request → Update + re-deliver
        ├─ Complaint → Attempt resolution → escalate if needed
        ├─ Refund → Check policy → process or escalate
        └─ Spam → Ignore
    → Psy responds via Gmail
    → Log interaction
```

### Support Policies (Psy enforces autonomously)
- **Free modifications**: up to 2 revisions within 7 days of delivery
- **Refunds**: full refund if itinerary not delivered within 48h
- **Response time**: within 4 hours during business hours
- **Escalation**: anything Psy is uncertain about → Slack ping to Bernard

---

## 7. Marketing / SEO / AEO Automation

### Programmatic SEO Pages

Psy generates destination pages at `/destinations/{city-slug}`:

```
/destinations/tokyo
/destinations/kyoto
/destinations/barcelona
/destinations/lisbon
...
```

Each page includes:
- H1: "{City} Travel Itinerary — AI-Powered, Reddit-Backed"
- Best time to visit, budget breakdown, top neighborhoods
- Sample 3-day itinerary teaser
- Reddit quotes/testimonials
- CTA: "Get your custom {city} itinerary"
- Schema.org markup (TravelAction, Place)

**Generation cadence**: Psy creates 5-10 new destination pages per week, prioritizing:
1. High search volume destinations
2. Trending destinations (from Reddit/social signals)
3. Destinations with existing orders (social proof)

### AEO (Answer Engine Optimization)

- FAQ schema on every destination page
- Direct answers in H2s ("How many days do you need in Tokyo?")
- Structured data for Google's AI Overviews
- Conversational content style that LLMs can extract

### Blog Content

Psy writes 2-3 blog posts per week:
- "X Days in {Destination}: What Reddit Actually Recommends"
- "Hidden Gems in {City} That Tourists Miss"
- Seasonal content: "Best {Season} Destinations 2026"

### Social (v2+)
- Auto-generate Twitter/X threads from itinerary highlights
- Reddit participation (helpful comments linking back, carefully)

---

## 8. Infrastructure

### Hosting & Deploy
```
GitHub (psyduckler/tabiji)
    → Push to main
    → GitHub Actions
    → Build Next.js
    → Deploy to Cloudflare Pages
```

### Environment Variables
```
STRIPE_SECRET_KEY        → Cloudflare env (encrypted)
STRIPE_WEBHOOK_SECRET    → Cloudflare env (encrypted)
GMAIL_CREDENTIALS        → macOS Keychain (Psy's machine)
DATABASE_URL             → Cloudflare D1 binding
R2_BUCKET                → Cloudflare R2 binding
```

### Monitoring
- **Uptime**: UptimeRobot (free, pings every 5 min)
- **Errors**: Cloudflare dashboard + Sentry (free tier)
- **Orders**: D1 query for stuck orders (status != delivered after 24h)
- **Revenue**: Stripe dashboard
- **SEO**: Google Search Console (Psy checks weekly)

### Domain & DNS
- `tabiji.ai` → Cloudflare DNS (nameservers)
- `@` → Cloudflare Pages deployment
- `mail` → Cloudflare Email Routing (support@tabiji.ai → Psy)

---

## 9. Gaps & Open Questions

- **Gmail sending limits**: 500/day free, 2000/day with Workspace. Fine for v1, need Resend/Postmark at scale.
- **PDF generation**: Need a solution. Options: Puppeteer on Cloudflare (no), or generate on Psy's machine and upload to R2.
- **Payment for custom domain email**: Need Google Workspace or Cloudflare email routing + Gmail send-as.
- **Order notification to Psy**: Webhook → where? Options: OpenClaw webhook endpoint, or Slack notification that Psy monitors.
- **Rate limiting**: Need to prevent order spam. Cloudflare rate limiting (free tier).
- **Legal**: Terms of service, refund policy, privacy policy pages needed.

---

## 10. Phased Rollout

### v1 — MVP (Week 1-2)
- Landing page live on tabiji.ai
- Stripe checkout for single itinerary ($29)
- Manual-ish pipeline: Stripe webhook → Slack notification → Psy generates → emails customer
- 3-5 destination SEO pages
- Basic support via email reply

**Goal**: First paying customer. Validate demand.

### v2 — Automation (Week 3-6)
- Full automated pipeline: webhook → queue → Psy auto-generates
- Order status tracking (customer can check)
- 50+ destination SEO pages
- Blog content engine running
- Support email auto-routing
- Follow-up emails (feedback request, review ask)
- Itinerary PDF generation

**Goal**: Psy handles 90% of operations without Bernard.

### v3 — Scale (Month 2-3)
- Tiered pricing: Basic ($19) / Premium ($39) / Luxury ($79)
- Customer accounts + order history
- Itinerary customization UI (drag-and-drop days)
- Referral program
- Multi-language support (Japanese market!)
- Social media automation
- Migrate email to Resend/Postmark
- A/B testing on landing page

**Goal**: $1k+ MRR, fully autonomous.

---

*Document authored by Psy. Last updated: 2026-02-09.*
