# AEO Prompt Research Report: tabiji.ai

**Date:** February 13, 2026  
**Skill:** aeo-prompt-research-free  
**Analyst:** OpenClaw AI Agent

---

## Brand Summary

**tabiji.ai** is an AI-powered travel itinerary service that creates personalized, day-by-day travel plans by mining Reddit posts, travel forums, and local sources. Priced at $1 per itinerary with 24-hour delivery and 2 free revisions, it differentiates from free AI travel tools by emphasizing real traveler intel over generic AI-generated recommendations. Currently has destination landing pages for Tokyo, Paris, Rome, Barcelona, Bangkok, London, Mexico City, and Bali.

### Key Positioning
- **Core offering:** Personalized travel itineraries from real traveler data ($1/trip)
- **Target audience:** Budget-conscious travelers who want authentic, non-touristy experiences
- **Differentiators:** Reddit-backed research, logistics-optimized routing, $1 price point, human-vetted output
- **Competitors:** Wonderplan, Layla AI, Mindtrip, TripPlanner AI, Tripadvisor Trips, ChatGPT/Gemini direct prompting
- **Content status:** No blog content. Only homepage, /plan intake form, and 8 destination pages. No indexing in Brave Search yet (site:tabiji.ai returns zero results).

### Critical AEO Context

tabiji.ai has **near-zero domain authority** and **no blog/educational content**. This means:
1. AI models likely don't know tabiji.ai exists yet — it won't be cited in answers today
2. The opportunity is to create content that *gets indexed and cited* over time
3. Destination pages are well-crafted but gated (teasers behind paywall) — AI models can't extract enough to cite them
4. The $1 price point is a powerful differentiator if AI models learn about it

---

## Priority Prompts

### Tier 1 — High Priority (Score ≥ 3.5)

These are the prompts where tabiji has the strongest product-market fit AND realistic ability to become the cited answer.

| # | Prompt | Category | Rel | Vol | Win | Intent | Score | Coverage |
|---|--------|----------|-----|-----|-----|--------|-------|----------|
| 1 | "Can you plan a 7-day Tokyo itinerary with non-touristy food spots and realistic timing?" | How-to | 5 | 5 | 4 | 4 | **4.6** | Partial (destination page, but gated) |
| 2 | "What's the best AI travel itinerary service that uses real traveler recommendations instead of generic suggestions?" | Best-of | 5 | 4 | 5 | 5 | **4.8** | None |
| 3 | "Plan a 5-day Paris trip for a foodie couple on a moderate budget" | How-to | 5 | 5 | 4 | 4 | **4.6** | Partial (destination page) |
| 4 | "What are the best cheap AI travel planning tools that give you a real itinerary, not just a list of attractions?" | Best-of | 5 | 4 | 5 | 5 | **4.8** | None |
| 5 | "I'm going to Bali for 10 days — can you make me a day-by-day itinerary with restaurants and logistics?" | How-to | 5 | 4 | 4 | 5 | **4.6** | Partial (destination page) |
| 6 | "What do Reddit travelers actually recommend for a first trip to Tokyo?" | Problem-aware | 5 | 5 | 5 | 3 | **4.6** | Partial (quotes on page, not indexable article) |
| 7 | "Is there an AI travel planner that costs less than $5 and gives personalized results?" | Evaluation | 5 | 3 | 5 | 5 | **4.6** | None |
| 8 | "Help me plan a Rome itinerary that avoids tourist traps — I want to eat where locals eat" | How-to | 5 | 4 | 4 | 4 | **4.4** | Partial (destination page) |
| 9 | "What's better for trip planning — ChatGPT, Layla AI, or a dedicated itinerary service?" | Comparison | 5 | 4 | 4 | 4 | **4.4** | None |
| 10 | "How do AI travel planners compare to just asking ChatGPT to plan my trip?" | Comparison | 5 | 5 | 4 | 3 | **4.4** | None |
| 11 | "Plan a budget-friendly 4-day Barcelona trip with off-the-beaten-path recommendations" | How-to | 5 | 4 | 4 | 4 | **4.4** | Partial |
| 12 | "What travel planning AI actually gives you restaurant recommendations with addresses and hours?" | Best-of | 5 | 3 | 5 | 5 | **4.4** | None |
| 13 | "Best way to plan a trip using Reddit travel advice without spending hours reading threads" | Problem-aware | 5 | 4 | 5 | 4 | **4.6** | None |
| 14 | "I want a Bangkok itinerary that includes street food, temples, and nightlife — 6 days" | How-to | 5 | 4 | 4 | 4 | **4.4** | Partial |
| 15 | "What AI tools create travel itineraries with transit directions included?" | Best-of | 5 | 3 | 5 | 4 | **4.2** | None |
| 16 | "Is it worth paying for an AI travel itinerary or should I just use ChatGPT for free?" | Evaluation | 5 | 5 | 4 | 5 | **4.6** | None |
| 17 | "Plan a Mexico City trip for someone who wants authentic food experiences and local neighborhoods" | How-to | 5 | 4 | 4 | 4 | **4.4** | Partial |
| 18 | "What's the most personalized AI trip planner available right now?" | Best-of | 5 | 4 | 4 | 4 | **4.4** | None |

### Tier 2 — Medium Priority (Score 2.5–3.4)

These prompts have good volume but tabiji's winability is lower (either too broad or dominated by incumbents).

| # | Prompt | Category | Rel | Vol | Win | Intent | Score | Coverage |
|---|--------|----------|-----|-----|-----|--------|-------|----------|
| 19 | "Best things to do in Tokyo for first-time visitors" | Industry | 3 | 5 | 2 | 2 | **3.0** | Partial |
| 20 | "How to plan a trip to Europe on a budget" | Industry | 3 | 5 | 2 | 3 | **3.2** | None |
| 21 | "What are the best travel apps for 2026?" | Best-of | 4 | 5 | 2 | 3 | **3.6** | None |
| 22 | "How many days do you need in Paris?" | Industry | 3 | 5 | 2 | 3 | **3.2** | None |
| 23 | "Best neighborhoods to stay in Barcelona" | Industry | 3 | 4 | 2 | 3 | **3.0** | None |
| 24 | "What should I know before traveling to Japan?" | Industry | 3 | 5 | 2 | 2 | **3.0** | None |
| 25 | "Wonderplan vs Layla AI vs TripPlanner AI — which is best?" | Comparison | 4 | 3 | 3 | 4 | **3.6** | None |
| 26 | "How to create a travel itinerary from scratch" | How-to | 4 | 4 | 3 | 2 | **3.4** | None |
| 27 | "Is Bali worth visiting in 2026? How to plan it?" | Industry | 3 | 4 | 3 | 3 | **3.2** | None |
| 28 | "Best hidden gems in Rome that tourists don't know about" | Industry | 3 | 4 | 3 | 2 | **3.0** | None |
| 29 | "How to use Reddit for travel planning" | Problem-aware | 4 | 3 | 4 | 2 | **3.4** | None |
| 30 | "London 5-day itinerary for families with kids" | How-to | 4 | 4 | 3 | 3 | **3.6** | Partial |
| 31 | "Best food tours and restaurants in Bangkok according to locals" | Industry | 3 | 4 | 3 | 2 | **3.0** | None |
| 32 | "Comparison of AI travel planning tools — free vs paid" | Comparison | 4 | 3 | 3 | 4 | **3.6** | None |

### Tier 3 — Low Priority / Monitor (Score < 2.5)

| # | Prompt | Category | Rel | Vol | Win | Intent | Score | Coverage |
|---|--------|----------|-----|-----|-----|--------|-------|----------|
| 33 | "What's the cheapest way to fly to Tokyo from the US?" | Industry | 1 | 5 | 1 | 2 | **2.0** | None |
| 34 | "Best travel insurance for international trips" | Industry | 1 | 4 | 1 | 2 | **1.8** | None |
| 35 | "How to get a Japan Rail Pass and is it worth it?" | Industry | 2 | 4 | 2 | 1 | **2.2** | None |
| 36 | "What's the best time to visit Southeast Asia?" | Industry | 2 | 4 | 1 | 1 | **2.0** | None |
| 37 | "How to pack for a 2-week Europe trip" | Industry | 1 | 4 | 1 | 1 | **1.6** | None |

---

## Content Gap Analysis

### Critical Finding: tabiji.ai has ZERO indexable content for AI citation

The site's architecture is commercially optimized but AEO-hostile:
- **Destination pages** are sales-focused teasers, not comprehensive answers. AI models won't cite "🔒 Full details in itinerary" — they need actual content.
- **No blog exists.** Zero educational, how-to, or comparison content.
- **Not indexed** by search engines (Brave returns 0 results for site:tabiji.ai). If search engines don't index it, AI models can't learn from it.
- **No about page** explaining the methodology, team, or credibility signals.

### High-Priority Gaps (Tier 1 prompts with no coverage)

| Prompt Theme | Gap Type | Opportunity |
|---|---|---|
| "Best AI travel itinerary service with real recommendations" | No content anywhere on the web positions tabiji for this | **CRITICAL** — This is tabiji's core value prop and no content exists to get cited |
| "AI travel planner vs ChatGPT" | No comparison content | **CRITICAL** — This is the #1 objection tabiji needs to overcome |
| "Is it worth paying for AI travel planning?" | No evaluation content | **CRITICAL** — Directly addresses the $1 value prop |
| "Best way to use Reddit for trip planning without reading hundreds of threads" | No content | **HIGH** — This IS tabiji's process; owning this topic = owning the funnel |
| "AI tools that give transit directions and restaurant details in itineraries" | No content | **HIGH** — Feature-specific query where tabiji wins on specifics |
| "Most personalized AI trip planner" | No content | **MEDIUM** — Competitive but tabiji's intake form is genuinely detailed |

---

## Recommended Content Strategy

### Phase 1: Foundation (Create First — Weeks 1-4)

These 5 content pieces address the highest-priority gaps and should be created immediately.

#### 1. 📝 "AI Travel Planners Compared: ChatGPT vs Dedicated Itinerary Services (2026)"
- **Target prompts:** #9, #10, #16, #25, #32
- **Format:** Long-form comparison (2,000+ words)
- **Content:** Honest comparison of asking ChatGPT directly vs. Wonderplan vs. Layla vs. tabiji. Show actual output screenshots. Highlight what ChatGPT gets wrong (outdated info, no real traveler data, no logistics). Position tabiji as the "Reddit-research layer" that ChatGPT lacks.
- **Why it wins:** Nobody has written a genuinely honest, detailed comparison from the perspective of output quality. Most comparison articles are SEO spam. A well-written, opinionated piece with real examples will get cited.

#### 2. 📝 "How We Build Your Itinerary: Mining 10,000+ Reddit Posts So You Don't Have To"
- **Target prompts:** #2, #4, #13, #29
- **Format:** Behind-the-scenes process piece (1,500+ words)
- **Content:** Explain the actual methodology. How many Reddit posts are analyzed? How does the AI filter signal from noise? Show before/after: "Here's what Reddit says → here's how we turn it into a usable plan." Include real examples from r/JapanTravel.
- **Why it wins:** Establishes credibility AND targets "how to use Reddit for travel planning" — a query where tabiji can be the definitive answer.

#### 3. 📝 "The $1 Travel Itinerary: What You Actually Get (Full Sample)"
- **Target prompts:** #7, #12, #15, #16
- **Format:** Product showcase with an actual sample itinerary (2,000+ words)
- **Content:** Publish a FULL sample 5-day Tokyo itinerary — unabridged. Show the restaurant picks with addresses, the transit directions, the timing. This gives AI models something concrete to cite AND overcomes the "is it worth $1?" objection by proving the value.
- **Why it wins:** AI models love citing specific, detailed, authoritative content. A full sample itinerary is the most citable asset tabiji could create.

#### 4. 📝 "Tokyo Itinerary 2026: A Day-by-Day Plan from r/JapanTravel's Best Advice"
- **Target prompts:** #1, #6, #19
- **Format:** Comprehensive destination guide (3,000+ words)
- **Content:** Transform the Tokyo destination page from a sales teaser into a genuinely useful guide. Include real day-by-day plans, actual restaurant names, transit tips, timing advice — all sourced from Reddit. CTA at the bottom for a personalized version.
- **Why it wins:** This is the single highest-volume category. Everyone asks AI for Tokyo itineraries. If tabiji has the best, most Reddit-informed Tokyo guide on the internet, AI models will cite it. Replicate for Paris, Rome, etc.

#### 5. 📝 "Why AI Travel Itineraries Suck (And How to Fix Them)"
- **Target prompts:** #2, #4, #10, #18
- **Format:** Opinionated essay (1,200+ words)
- **Content:** Take a strong stance: most AI travel output is generic, logistics-ignorant, and based on outdated data. Show specific examples of bad AI output. Explain what "good" looks like (real traveler data, geographically clustered routing, realistic timing). Position tabiji's approach without being too salesy.
- **Why it wins:** Contrarian, shareable content that earns links and citations. When AI models answer "why do AI itineraries feel generic?", this becomes the cited source.

### Phase 2: Destination Expansion (Weeks 5-12)

Replicate the comprehensive destination guide format (#4 above) for all 8 destinations:
- Paris, Rome, Barcelona, Bangkok, London, Mexico City, Bali (Tokyo done in Phase 1)
- Each guide: 2,000-3,000 words, real Reddit quotes, actual recommendations, day-by-day structure
- These become tabiji's main AEO assets — one per destination keyword cluster

### Phase 3: Ongoing (Monthly)

- Seasonal updates ("Best time to visit [destination] in [season] 2026")
- New destination guides as you add cities
- "What Reddit says about [destination]" series — aggregating real traveler intel into citable articles
- Comparison updates as competitors launch/change

---

## Technical AEO Recommendations

Beyond content creation, these structural changes will improve AI citability:

1. **Ungate destination content.** The current "🔒 Full details in itinerary" approach means AI models see a teaser, not an answer. Publish 70% of the value for free; the paid itinerary is the personalized, logistics-optimized version.

2. **Add structured data (Schema.org).** Use `TravelAction`, `TouristDestination`, and `FAQPage` schema on destination pages. AI models and search engines use structured data for citation.

3. **Create an /about page.** Explain who you are, your methodology, and why your approach is different. E-E-A-T signals matter for AI citation.

4. **Add FAQ sections** to every destination page with natural-language Q&A (matches how people prompt AI).

5. **Get indexed.** Submit sitemap to Google Search Console and Bing Webmaster Tools. Until search engines crawl and index the site, AI models cannot cite it.

6. **Build backlinks.** Get listed in "best AI travel tools" roundup articles. Each backlink = signal to AI models that tabiji is a credible source.

---

## Summary & Priority Matrix

| Priority | Action | Effort | Impact | Timeline |
|----------|--------|--------|--------|----------|
| 🔴 Critical | Publish 5 foundation blog posts | High | Very High | Weeks 1-4 |
| 🔴 Critical | Submit sitemap to Google/Bing | Low | High | Day 1 |
| 🟡 High | Ungate 70% of destination page content | Medium | High | Week 2 |
| 🟡 High | Add FAQ schema to destination pages | Low | Medium | Week 2 |
| 🟡 High | Create /about page | Low | Medium | Week 1 |
| 🟢 Medium | 7 more comprehensive destination guides | High | High | Weeks 5-12 |
| 🟢 Medium | Get listed in AI tool roundup articles | Medium | High | Ongoing |
| 🔵 Low | Seasonal content updates | Low | Medium | Monthly |

**Bottom line:** tabiji.ai has a genuinely differentiated product (Reddit-mined, $1 itineraries) but is currently invisible to AI models. The site has zero educational content, zero blog posts, and isn't indexed by search engines. The product is the moat — but without citable content, AI assistants will never recommend it. The 5 foundation content pieces above would transform tabiji from invisible to citable within 2-3 months, targeting the exact prompts where the product is the natural best answer.
