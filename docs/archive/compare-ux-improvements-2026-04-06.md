# Compare Pages UX Improvements — 2026-04-06

## Current page flow (top to bottom)
1. Nav → 2. Mobile TOC → 3. Hero → 4. Desktop TOC sidebar + article content → 5. Methodology box → 6. Photo grid → 7. TL;DR Verdict → 8. Quick Comparison table → 9. Deep dive sections (9-13 of them, each: prose + Reddit quotes + verdict) → 10. Decision Framework (duplicated) → 11. FAQ → 12. CTA → 13. Viator tours → 14. Footer

## Core UX problem
The page is built for **reading**, not **deciding**. But users searching "[city A] vs [city B]" want to **make a decision**, not read a 4,000-word article. The content is excellent — the problem is information architecture, not information quality.

---

## IMPROVEMENT 1: Interactive "What matters to you?" filter at the top

**The problem:** Every user has different priorities (budget, food, beaches, nightlife, safety). Right now they all get the same linear article and have to scroll to find what they care about.

**The fix:** Add an interactive section immediately after the hero:

```
What matters most to you?
[Budget] [Food] [Beaches] [Nightlife] [Culture] [Safety] [Family] [Solo travel]
```

Clicking a tag:
- Scrolls to that deep-dive section
- OR (better) reorders the page to show that section first
- OR (simplest) highlights that row in the quick comparison table and shows a one-line personalized verdict: "For **budget travelers**, Madrid wins — expect to save €200+ over a 5-day trip."

**Why:** Turns a passive reading experience into an active decision-making tool. Reduces bounce rate from users who don't want to read 4,000 words.

---

## IMPROVEMENT 2: Visual scorecard replacing/augmenting the comparison table

**The problem:** The comparison table is a 4-column text table. It requires reading every cell to understand who wins. There's no visual signal — no color, no bars, no scores.

**The fix:** Replace or augment with a visual scorecard:

```
                    Madrid    Barcelona
Overall Score        6.8        7.2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Budget       ████████░░  ██████░░░░   Madrid wins
Food         ████████░░  ████████░░   Tie
Beaches      ██░░░░░░░░  █████████░   Barcelona wins
Nightlife    ████████░░  ████████░░   Tie
Culture      █████████░  ███████░░░   Madrid wins
Safety       ████████░░  ██████░░░░   Madrid wins
Architecture ██████░░░░  ██████████   Barcelona wins
Day Trips    █████████░  ███████░░░   Madrid wins
Getting Around████████░░  ████████░░   Tie
```

- Use horizontal bars with destination colors (red/blue)
- Clickable rows → scroll to deep-dive section for that category
- Overall score at top gives the "at a glance" answer
- Mobile: stack vertically with swipeable comparison

**Why:** Users can answer "who wins?" in 2 seconds instead of 2 minutes. The table becomes the primary navigation tool, not just a summary.

---

## IMPROVEMENT 3: Collapsible deep-dive sections

**The problem:** 9-13 deep-dive sections stacked vertically create a 4,000+ word scroll. Most users care about 3-4 categories, not all of them. The page feels exhausting.

**The fix:** Make deep-dive sections accordion-style:
- Default state: collapsed, showing only the H2 heading + winner badge + 1-sentence summary
- Click to expand full content (prose, Reddit quotes, verdict)
- Auto-expand the first 2-3 sections to show the page isn't empty
- "Expand all" toggle for users who want the full read

```
🏙️ City Character & Vibe                    [Madrid wins]
  "Barcelona dazzles on first impression; Madrid grows on you..."
  ▼ Read full comparison

🏛️ Architecture & Culture                   [Barcelona wins]
  "Gaudí's Sagrada Família alone justifies the trip..."
  ▼ Read full comparison

🍽️ Food & Dining                            [Tie]
  "Madrid wins everyday eating; Barcelona wins fine dining..."
  ▼ Read full comparison
```

**Why:** Reduces cognitive load. Users scan headings + winners, then drill into what they care about. Pages feel more interactive and less like a term paper. Also improves Core Web Vitals (less DOM on initial paint).

---

## IMPROVEMENT 4: Sticky "score ticker" while scrolling

**The problem:** As users scroll through deep dives, they lose context of the overall picture. The comparison table is far above. The verdict is at the top. There's no persistent summary.

**The fix:** A minimal sticky bar below the nav (or integrated into the mobile TOC) that shows:

```
Madrid 4 — 3 Barcelona  (2 ties)  |  Currently reading: 🍽️ Food
```

Updates as the user scrolls through sections. On mobile, this replaces the current TOC active label with something more useful.

**Why:** Maintains orientation. Users always know the running score and where they are in the page.

---

## IMPROVEMENT 5: "Quick answer" cards for common questions

**The problem:** Users coming from Google often have a specific question: "Is Madrid or Barcelona cheaper?", "Which has better food?", "Is Barcelona safe?". The FAQ section answers these but it's at the bottom. The deep-dive sections answer these but they're buried in prose.

**The fix:** Add a "Quick Answers" section right after the verdict with scannable Q&A cards:

```
┌─────────────────────────────┐  ┌─────────────────────────────┐
│ Which is cheaper?           │  │ Which has better food?      │
│ Madrid — save ~€200/5 days  │  │ Tie — Madrid for tapas,     │
│ [See full cost breakdown →] │  │ Barcelona for fine dining    │
└─────────────────────────────┘  └─────────────────────────────┘
┌─────────────────────────────┐  ┌─────────────────────────────┐
│ Which has beaches?          │  │ Which is safer?             │
│ Barcelona — 4.5km coastline │  │ Madrid — less pickpocketing │
│ Madrid: 300km from coast    │  │ Both safe by global norms   │
└─────────────────────────────┘  └─────────────────────────────┘
```

Each card links to the relevant deep-dive section. These map directly to the most common search queries (visible in FAQPage schema questions).

**Why:** Gives 80% of users their answer in 10 seconds. Reduces pogo-sticking (users going back to Google because they couldn't find the answer fast enough). Also excellent for AI citation — these short, direct answers are exactly what AI Overviews extract.

---

## IMPROVEMENT 6: Remove the duplicate Decision Framework

**The problem:** There are TWO "Decision Framework" sections (🔀 and 🎯) with nearly identical content. One uses `<ul>` lists, the other uses `decision-grid` cards. This is confusing and looks like a bug.

**The fix:** Merge into one. Keep the card-based `decision-grid` version (more visual, more scannable). Remove the duplicate `<ul>` version.

---

## IMPROVEMENT 7: Remove sports/soccer Reddit quotes

**The problem:** Multiple sections contain Reddit match thread quotes like "42' Goal! Atletico Madrid 1, Barcelona 1..." These are clearly from soccer subreddits, not travel discussions. They look like a scraping bug.

**The fix:** Filter these out during generation. They damage credibility and confuse users.

---

## IMPROVEMENT 8: "Tell me about my trip" personalization

**The problem:** The page treats all users the same. A solo backpacker and a family with kids have fundamentally different needs.

**The fix:** Add a lightweight personalization widget after the hero:

```
I'm traveling...
[Solo] [As a couple] [With family] [With friends]

My budget is...
[Backpacker] [Mid-range] [Luxury]

I care most about...
[Food] [Culture] [Beaches] [Nightlife] [Nature]
```

Based on selections, show a personalized 2-3 sentence recommendation at the top:
> "For a **solo traveler on a mid-range budget who cares about food**, we'd recommend **Madrid**. The tapas culture is more authentic, the prices are lower, and solo travelers consistently report feeling more welcome. [See why →]"

**Implementation:** No backend needed. Pure JavaScript — the content already exists in the decision framework and verdicts, just surface the right combination.

**Why:** Transforms a one-size-fits-all article into a personalized recommendation engine. Dramatically increases engagement and time on page.

---

## IMPROVEMENT 9: Side-by-side photo comparisons in deep dives

**The problem:** Deep-dive sections are text-heavy with occasional single images. For a page about deciding between two visually distinct destinations, there's surprisingly little visual comparison.

**The fix:** In key sections (beaches, architecture, neighborhoods, food), add side-by-side photo pairs:

```
┌──────────────────────┐  ┌──────────────────────┐
│  [Madrid tapas bar]  │  │ [Barcelona seafood]  │
│  Cava Baja tapas     │  │  Barceloneta fideuà  │
│  crawl — €3-5/plate  │  │  — €12-18/plate      │
└──────────────────────┘  └──────────────────────┘
```

**Why:** Travel decisions are inherently visual. Photos help users *feel* the difference, not just read about it. Also improves time-on-page and reduces bounce.

---

## IMPROVEMENT 10: Progressive disclosure on mobile

**The problem:** On mobile, this is an extremely long single-column scroll. The mobile TOC helps navigate, but doesn't reduce the cognitive weight.

**The fix:**
- Default to collapsed sections on mobile (improvement #3)
- Show the scorecard (#2) as the primary mobile view
- Make the quick answers (#5) swipeable cards
- Keep the sticky score ticker (#4) as a thin bar under the mobile TOC
- Add a "Jump to verdict" floating button that appears after 3 seconds of scrolling

**Why:** Mobile users are even more task-oriented than desktop users. They want the answer, not the essay.

---

## IMPROVEMENT 11: "Travelers also compared" recommendation engine

**The problem:** Related comparisons exist on some pages (Vietnam-vs-Thailand has cross-links) but most pages end with just a CTA and Viator links. Users who've decided against one pairing have no easy path to explore alternatives.

**The fix:** Add a "Travelers also compared" section before the footer:

```
People who viewed Madrid vs Barcelona also looked at:
┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ Rome vs        │ │ Lisbon vs      │ │ Madrid vs      │
│ Barcelona      │ │ Porto          │ │ Valencia       │
│ ★ 1,900/mo     │ │ ★ 1,900/mo     │ │ ★ 1,900/mo     │
└────────────────┘ └────────────────┘ └────────────────┘
```

Cards should include: destination photos, the one-line verdict, and search volume as a popularity signal.

**Why:** Keeps users in the tabiji ecosystem. Reduces exit rate. Creates the internal link mesh that SEO needs. Mimics the "customers also viewed" pattern that Amazon proved works.

---

## IMPROVEMENT 12: Animated/visual cost comparison

**The problem:** Cost data is buried in paragraphs. "Madrid daily costs: Hostel dorm €20–30/night | Budget hotel €70–100..." is hard to scan and compare.

**The fix:** Visual cost comparison widget:

```
Daily Budget Breakdown
                        Madrid          Barcelona
┌─────────────────────────────────────────────────┐
│ 🛏️ Hostel dorm        €25             €34       │
│ 🏨 Budget hotel        €85            €115       │
│ 🍽️ Menu del día        €13             €16       │
│ 🍺 Beer                €4              €5        │
│ 🚇 Metro ride          €1.50           €1.15     │
│ ☕ Coffee              €1.75           €2.50     │
├─────────────────────────────────────────────────┤
│ 📊 DAILY TOTAL         €85-110        €100-130   │
│                    ████████░░░░    ███████████░░  │
│                    🏆 Save ~€25/day with Madrid   │
└─────────────────────────────────────────────────┘
```

**Why:** Cost is the #1 or #2 deciding factor for most travelers. Making it scannable and visual respects the importance of this data point.

---

## IMPROVEMENT 13: Weather/climate visual comparison

**The problem:** Weather info is in the "Best Time to Visit" prose section. Users can't quickly compare temperatures or rainfall across months.

**The fix:** Add a month-by-month visual comparison (like Vietnam-vs-Thailand already has, but better):

```
Best time to visit: May, Sep-Oct (both cities)

     Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec
MAD   10°  12°  15°  17°  21°  27°  32°  31°  26°  19°  13°  10°
BCN   12°  13°  15°  17°  20°  24°  28°  28°  25°  21°  16°  13°

[Green highlighting on May, Sep, Oct columns]
[Red highlighting on Jul, Aug for both]
```

Include rainfall bars below. Flag festival dates (San Isidro May, La Mercè Sep).

**Why:** "When should I go?" is one of the top FAQ questions. A visual chart answers it instantly.

---

## Priority order for implementation

### Tier 1 — Highest impact, reasonable effort
1. **Remove duplicate Decision Framework** (#6) — instant quality improvement
2. **Remove sports quotes** (#7) — instant quality improvement
3. **Visual scorecard** (#2) — transforms the comparison table from text to visual
4. **Quick answer cards** (#5) — serves the majority use case fast
5. **Collapsible deep dives** (#3) — reduces page overwhelm

### Tier 2 — High impact, moderate effort
6. **"What matters to you?" filter** (#1) — adds interactivity
7. **Cost comparison widget** (#12) — visualizes the #1 decision factor
8. **Weather visual** (#13) — answers a top FAQ visually
9. **"Travelers also compared"** (#11) — keeps users on site

### Tier 3 — Transformative, higher effort
10. **Trip personalization widget** (#8) — requires JS logic
11. **Side-by-side photos** (#9) — requires more images
12. **Sticky score ticker** (#4) — requires scroll tracking JS
13. **Mobile progressive disclosure** (#10) — mobile-specific rework
