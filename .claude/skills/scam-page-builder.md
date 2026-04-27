---
name: scam-page-builder
description: Build one new tabiji scam-city page end-to-end — SerpAPI research (Reddit/news/embassy/fares), write 3–6 book-ready scams into scams/research/<cc>_batchN.json, update CITY_SLUGS/SAFETY_TIPS/FAQS/EMERGENCY_INFO in scams/generate_pages.py, regenerate, parser-verify, and open a single-city PR. Trigger when the user says "build scam page for <city>", "add <city> to scams", or "scam-page <city>".
user_invocable: true
---

# Scam Page Builder

Build one complete book-ready tabiji.ai scam-city page from SerpAPI research to single-city PR. Works within the existing research JSON schema (no new fields) — data-accuracy and design improvements land through prose, lint, and out-of-band audit trails.

## When to use

- User asks to "build scam page for <city>" or "add <city> to scams"
- Expanding coverage into an entire country's new cities (run this skill **one city at a time**, one PR each)
- Not for enriching an already-published page (that's a separate workflow)

## Required input

- City name (e.g., "Taipei")
- Country (e.g., "Taiwan")
- ISO country code (e.g., "TW")
- Flag emoji (e.g., "🇹🇼")

If only the city is given, infer the other three and confirm with the user.

## Pipeline landscape

- **Research JSON**: `scams/research/<cc>_batchN.json` — append one city object per run. Shape:
  ```json
  {
    "city": "<City>",
    "country": "<Country>",
    "country_code": "<CC>",
    "flag": "<flag emoji>",
    "scams": [
      {
        "scam_name": "<≤60 chars>",
        "danger_level": "high|medium|low",
        "category": "<fixed vocab>",
        "location": "<≤5 comma-separated spots>",
        "story": "<4–6 paragraphs separated by \\n\\n, 40–110 words each (target 60–90), total 280–500 words>",
        "red_flags": ["<fragment>", ... 5 items],
        "how_to_avoid": ["<complete imperative sentence ending .?!>", ... 5 items],
        "reddit_sources": ["r/<sub> '<title verbatim>' (comments/<id>, <year>)", ... 5 items]
      }
    ]
  }
  ```
- **Generator**: [scams/generate_pages.py](scams/generate_pages.py) — single source of truth. Exports `regenerate_city(city_name)`, `regenerate_country_hub(country_name)`, `load_all_research_batches()`, plus the `EMERGENCY_INFO`, `CITY_SLUGS`, `SAFETY_TIPS`, `FAQS` dicts (search by name — avoid hard-coded line numbers).
- **Style contract**: [docs/scam-pages-style-guide.md](docs/scam-pages-style-guide.md). American English (en-US). Don't write prose that violates this.
- **Sanitizer**: `_sanitize_reddit_shards` in `scams/generate_pages.py` imports `clean_text` from [scripts/clean_us_reddit_shards.py](scripts/clean_us_reddit_shards.py). Runs on all prose at render time; strips `r/<sub> '<title>' (comments/xxx, YEAR)` strings. **Has a known orphan-phrase bug** — see Known Traps.
- **Lint**: [scripts/lint_scam_content.py](scripts/lint_scam_content.py). Pre-generation gate. Build on first skill run if absent (spec in Step 5).
- **Comics**: Deferred. A separate comic-batch PR uses [docs/comic-pipeline/pipeline.md](docs/comic-pipeline/pipeline.md) with per-country style at [docs/comic-pipeline/styles/](docs/comic-pipeline/styles/). The generator writes `<img class="scam-comic" src="https://img.tabiji.ai/scams/<slug>/scam-<N>.jpg?v=1" ...>` tags that 404 until comics are uploaded — acceptable until the comic follow-up PR.

## Secrets

- **SerpAPI key** — macOS keychain entry `serpapi-key` (account `serpapi`, **not** `$USER`); also available as env `SERPAPI_KEY`.
  ```bash
  SERPAPI_KEY=$(security find-generic-password -a "serpapi" -s "serpapi-key" -w)
  ```

## Full workflow (12 steps)

### Step 1: Scope gate

```bash
# Confirm city is not already covered
grep -n '"<City>"' scams/generate_pages.py | grep CITY_SLUGS
ls scams/<slug>/ 2>/dev/null
```

Three outcomes:

1. **New city** — `CITY_SLUGS["<City>"]` absent and `scams/<slug>/index.html` absent → proceed normally.
2. **Already book-ready** — existing page has ≥ 3 scams with valid `comments/<id>` Reddit IDs in `reddit_sources` (verify via `grep -c 'comments/[a-z0-9]\{6,8\}' scams/<slug>/index.html`) **and** ≥ 1 T1/T2 news/gov citation per scam → **abort**. This skill does not enrich already-book-ready pages.
3. **Pre-book-ready page (rewrite-override)** — existing page is from an earlier era (no verifiable Reddit IDs, no T1/T2 sources, style-guide violations like missing currency spacing or pre-2025 anchors) → **only proceed if the user explicitly authorizes a fresh rewrite**. Confirm in one sentence: "Existing `<city>` page is pre-book-ready; OK to rewrite from scratch?"

When rewriting:
- Keep the existing `CITY_SLUGS["<City>"]` entry (don't duplicate).
- **Replace** any existing `SAFETY_TIPS["<City>"]` and `FAQS["<City>"]` entries with freshly-researched values (don't merge — the old ones were written to a lower bar).
- Add the city to a country research batch as if new (the generator will overwrite `scams/<slug>/index.html` regardless).
- Commit message template: `scams: rewrite <City> (<Country>) to book-ready — <N> Reddit-cited scams`.

If the country is brand-new (not in any `scams/research/*_batch*.json`), confirm with the user before proceeding.

### Step 2: SerpAPI research — 4 passes

All fetches saved to `/tmp/scam-research/<slug>/` as the audit trail (not committed). Create the directory first:

```bash
mkdir -p /tmp/scam-research/<slug>/{serpapi,reddit,news,gov,operator}
```

#### Pass A — Reddit deep dive

SerpAPI `google` engine with `site:reddit.com` scoping. Run 8–12 queries spanning common scam categories:

```
"<city> tourist scam" site:reddit.com
"<city> taxi overcharge" site:reddit.com
"<city> scammed" site:reddit.com 2025..2026
"<city> fake police" site:reddit.com
"<city> gem scam" site:reddit.com
"<city> ATM skimming" site:reddit.com
"<city> QR code scam" site:reddit.com
"<city> airport taxi" site:reddit.com
"<city> rental deposit" site:reddit.com
r/<countrysub> <city> scam
```

For every plausible thread returned, fetch the raw Reddit thread JSON:

```bash
curl -sS -H "User-Agent: tabiji-research/1.0" \
  "https://www.reddit.com/r/<sub>/comments/<id>.json" \
  > /tmp/scam-research/<slug>/reddit/<id>.json
```

From each JSON, extract and record in `/tmp/scam-research/<slug>/reddit-index.json`:
- subreddit, thread_id, title (verbatim — preserve BrE spellings, emoji, casing)
- created_utc → year
- upvote count, comment count
- top 3 comments with ≥5 upvotes (paraphrase highlights only — no usernames)

**Reject** any Reddit source that:
- 404s on the `.json` fetch
- has `<5` upvotes on the parent post
- comes from a `<30 day old` account (if determinable)
- is `locked` or `removed`

#### Pass B — News / police (last 24 months)

SerpAPI `google_news` engine with date filter `tbs=qdr:y` (past year) for each of:

```
"<city> tourist scam arrest"
"<city> tourist overcharged fine"
"<city> fake taxi" OR "<city> tout fined"
"<country> tourist police"
```

Tier whitelist (Tier-1 / Tier-2 only; reject content farms, aggregators):
- **T1** (government/operator): `.gov`, `.gov.<cc>`, airport authority, consulate, tourism board
- **T2** (reputable news): national newspapers with a masthead + editorial staff (e.g., NST, Malay Mail, O Globo, Folha, BBC, Reuters, AFP, local equivalents)

For every accepted URL:

```bash
# Save the live article HTML
curl -sS -o /tmp/scam-research/<slug>/news/<pub>-<yyyymmdd>.html "<url>"
# Wayback snapshot (primary)
curl -sS "https://web.archive.org/save/<url>"
# Archive.ph fallback (optional, in case wayback fails)
curl -sS "https://archive.ph/newest/<url>"
```

Record in `/tmp/scam-research/<slug>/news-index.json`:
- publication, date, URL, archive_url, article title, 3-sentence summary
- **claim tokens** — exact numbers (currency amounts, fines, phone numbers), named entities (people, orgs), dates — extracted from the article body

#### Pass C — Embassy + tourist police

Fetch directly from the consulate/embassy `.gov` site — **do not rely on SerpAPI summary** (these numbers change annually):

```bash
# e.g., for Taipei
curl -sS -o /tmp/scam-research/<slug>/gov/embassy-us-tw.html \
  "https://tw.usembassy.gov/emergency-contact/"
curl -sS -o /tmp/scam-research/<slug>/gov/tourist-police-tw.html \
  "https://<tourist-police-url>"
```

Extract:
- Country emergency number (fire/ambulance)
- National police number
- Tourist police hotline (if any)
- Consumer-protection hotline (if any)
- At least one embassy address + phone (US + 1–2 other major-country embassies)

Cross-check against `EMERGENCY_INFO` in `scams/generate_pages.py`. Update if stale or missing.

#### Pass D — Prices, fares, operator data

For every numeric claim that will appear in scam prose (airport taxi, ticket price, transit fare, exchange rate), fetch the primary operator page:

```bash
curl -sS -o /tmp/scam-research/<slug>/operator/airport-<cc>.html "<airport authority URL>"
curl -sS -o /tmp/scam-research/<slug>/operator/transit-<city>.html "<metro/rail URL>"
curl -sS -o /tmp/scam-research/<slug>/operator/attraction-<name>.html "<operator URL>"
```

**Every currency amount in the final scam prose must correspond to an operator-page snapshot or a T2 news citation in the audit trail.** If a price has no T1/T2 source, do not include it.

### Step 3: Scam selection

- **3–6 scams per city** — target 6, minimum 3. Fewer than 3 → the city doesn't clear the quality bar; defer or skip.
- **Danger mix**: aim 3 high / 2 medium / 1 low on a 6-scam page; adjust proportionally for smaller pages. (HTML-side `danger_level` vocabulary — the api/v1 sibling field uses high/moderate/low and is synced from the HTML in Step 9b.)
- **Category diversity** — pick from fixed vocab, prefer no repeats on the same page:
  - `transport` (taxi/airport/rideshare)
  - `counterfeit` (fake goods/tickets/police ID/MDAC-style digital fraud)
  - `overcharging` (menu-swap, temple donation, vendor markup)
  - `distraction` (petty theft, bag snatch with accomplice)
  - `gem` (investment-grade stone confidence scam)
  - `fake-police` (shakedown, wallet/passport inspection)
  - `digital` (QR swap, fake-website, phishing-SMS)
  - `rental` (Airbnb/car/scooter deposit)
  - `temple-beg` (donation clipboard, "gift" with invoice)
  - `romance` (tea-house, date-bar bill)
  - `food-scam` (scale rigged, menu bait-and-switch)
  - `petty-theft` (pickpocket, motorcycle snatch)
- **Corroboration rule**: every scam must have ≥2 independent sources, at least 1 from T1 or T2. Reddit-only scams are rejected.
- **Emerging rule**: if all sources are from 2026 with no 2024/2025 baseline, include only if T1/T2 news confirms the pattern.

### Step 4: Write each scam

Follow the style guide (`docs/scam-pages-style-guide.md`) strictly. Key rules:

**`scam_name`**
- ≤ 60 characters
- ≤ 2 keywords
- No all-caps stuffing
- Title case, sentence-like

**`danger_level`** — lowercased literal `"high"`, `"medium"`, or `"low"`. Generator handles badges and severity-summary counts. **Use `"medium"`, not `"moderate"` — the generator's hero severity-pill counter matches `== "medium"` exactly; "moderate" silently drops out of the count and ships a wrong severity strip.**

There are **two parallel severity fields**, and they use **different vocabularies on purpose**:

| Field | Lives in | Vocabulary | Set by |
|---|---|---|---|
| `danger_level` | research JSON → HTML page | `high` / `medium` / `low` | you (writer), via the research JSON |
| `severity` | `api/v1/scams/<slug>.json` | `high` / `moderate` / `low` | [scripts/sync_api_from_html.py](scripts/sync_api_from_html.py), mapped from the rendered HTML's `danger-badge` class — never edit by hand |

`medium` (HTML) → `moderate` (api/v1) is the only mapping that changes; `high` and `low` pass through. Anything else (notably the legacy `minor` value from older synthesis runs) fails the lint at rule 22. If you ever see `severity: minor` or `severity: medium` in api/v1, the fix is to re-run the sync after the HTML is rebuilt — not to hand-edit the JSON.

**`category`** — one value from the fixed vocab above.

**`location`**
- ≤ 5 comma-separated named spots
- Pick the most diagnostic, not the exhaustive list
- Example: "KLIA arrivals, KL Sentral hotel drop-offs, Bukit Bintang pedestrian corridors" — not 7 airport gate numbers

**`story`** — pure narrative. **3 to 5 paragraphs** separated by `\n\n`, each 60–120 words (target 80–110), 2–5 sentences. Total 250–450 words. Monolithic walls are rejected.

The story walks the reader through the **encounter as theater**, not a checklist. Defense lives in `how_to_avoid[5]`, not the story — never duplicate avoidance steps inside the prose.

Readability mandate: the scam-page corpus also ships as paperback KDP books under `book-<country>/`. Dense 150+ word paragraphs that look OK on desktop become unreadable on mobile and brutal in print. Split aggressively.

The narrative is structured as **3 beats**:

- **Beat 1 — Setup + Hook (paragraph 1).** Where the encounter starts and what the scammer does in the first 30 seconds: the smile, the script, the prop in their hand, the way they step into your path. Concrete street-name specificity: "Walk Times Square between 42nd and 47th Street and you'll see the setup before the trap closes." ~80–110 words.
- **Beat 2 — Pivot + Pressure (paragraph 2).** The moment the script flips. The demand lands. What the scammer does if you resist: friends materializing, voice rising, body blocking the sidewalk. Named price ranges + concrete consequences: "$20 demanded, two or three other men step into the gap on your other side." ~80–110 words.
- **Beat 3 — Mechanism + Social Proof + Defense Cue (paragraph 3, optionally split into 3–4).** Why the scam works (the psychological hook). Reddit/police/Council social proof woven in as one sentence — no username, no comment URL: `r/AskNYC and r/nyc threads document the same play running daily on 42nd Street...`. Close with one defensive move wrapped in `<strong>...</strong>` that the reader can act on immediately: `<strong>The defensive move is to ask for the indoor menu before you sit.</strong>` ~80–120 words.

For longer scams (multi-stage frauds, regulatory context, recovery paths), split Beat 3 across 2–3 paragraphs — but never re-introduce defense steps the `how_to_avoid` list already covers. The story is *what happens to the reader*, not *what the reader should do*.

**Bold-emphasis must be raw HTML, never markdown.** Write `<strong>...</strong>` directly in the JSON `story` field. Markdown `**...**` does NOT get converted at render time — it ships to readers as literal asterisks. (Caught in Egypt audit, 2026-04: 5 Alexandria scams shipped `**The defensive move is...**` text on the live page.)

**Reddit citations: never embed `r/<sub> '<title>' (comments/xxx, YEAR)` strings in prose** — the sanitizer will strip them and leave orphan fragments. Use bare attribution (`r/AskNYC threads document...`) and let `reddit_sources[]` carry the verifiable links.

**Anti-patterns from past audits — REJECT all of these in story prose:**

- *Hedge attribution that names no source.* Banned phrases: "as travelers note", "as reported on travel forums", "community forums document", "community reports indicate", "traveler reports note", "Reddit's traveler community", "Redditors on traveler reports". These are sanitizer-leak artifacts (the original Reddit citation was stripped and the editorial hedge was left dangling) and read as placeholder language. Either cite a concrete subreddit (`r/Egypt threads document...`) or remove the hedge clause entirely.
- *"Real stories from Reddit travelers" mismatch.* If the prose uses zero specific subreddit citations, do not also rely on the hero's templated "Reddit-sourced" claim — either add real `r/<sub>` mentions to ≥ 3 scam bodies or accept that the hero will be inaccurate.
- *Date-stamped prices that age the book.* Banned phrases: "as of 2024", "as of 2025", "as of 2024–2025", "(2024)", "(2025)". Just state the price; the page is dated by `dateModified` in the JSON-LD.
- *ASCII double-hyphen as em-dash.* Use real em-dashes `—` (U+2014). Lint rule 5 enforces spacing but not character class — write `—` directly.
- *TLDR as scene-setter.* Banned openers: "You arrive at...", "You're walking...", "You've just landed...", "It was a hot afternoon...". TLDRs must name the actor and the cost in one sentence.
- *Defamation risk in scam prose.* Naming a specific real business as a scammer (e.g., `"Al-Attar Spice Store swaps your bottle"`) is print-book legal exposure. Genericize to "a spice stall in the souk" unless a T1/T2 source explicitly named the business in a published exposé.

**Canonical example: [`/scams/new-york-city/`](/scams/new-york-city/).** All 6 cards on that page follow this beat structure exactly.

**`tldr`** — derived automatically by `make_tldr()` from the first sentence of `story`, so the **first sentence is a load-bearing TLDR**. It must:
- Be a complete sentence ending in `.`, `!`, or `?`
- Function as a trap-summary that names the actor + the cost: "A man on 42nd Street presses a CD into your hand saying it's a free mixtape, then circles back demanding $20–$50."
- **Not be a narrative opener** like "It was a hot July afternoon…" or "You'd just landed at JFK…" — these read fine inside a paragraph but are useless as standalone snippets in search results, voice answers, or the rendered TLDR pull-quote.
- Pass the search-snippet test: read just the first sentence — does a stranger know what the scam is?

**`red_flags[5]`**
- Fragments acceptable; short; parallel structure
- Start with noun or present-participle
- Voice: descriptive, third-person

**`how_to_avoid[5]`**
- Complete imperative sentences
- First word is a verb (`REFUSE`, `IGNORE`, `BOOK`, `CHECK`, `NEVER`, `ALWAYS`, `CALL`, `USE`, `CONFIRM`, `PHOTOGRAPH`, etc.)
- Must end on `.`, `?`, or `!` (generator will not fix truncations)
- Voice: direct, second-person (`you` implicit)

**`reddit_sources[5]`**
- Format exactly: `r/<subreddit> '<title verbatim>' (comments/<id>, <year>)`
- Thread ID = 6–8 lowercase alphanumeric (verified against cached JSON)
- Title matches thread title exactly, including BrE spellings, emoji, question marks, casing
- ≥ 80% must be 2025 or 2026
- All 5 IDs must have a cached JSON under `/tmp/scam-research/<slug>/reddit/`

### Step 4b: Write the page-level sections

A finished NYC-canonical page is more than scam cards. The writer's job covers every block in this anatomy — the generator emits the structure, but the **content quality of these sections is the difference between a default page and a book-ready page**:

| Section | Source | Writer's responsibility |
|---|---|---|
| `<title>` + meta description | auto from city + scam names | scam_name choices must read as a clean title sequence |
| Hero + severity strip | auto from `danger_level` counts | use `"medium"` not `"moderate"` (generator literal-matches) |
| Key Takeaways | auto from scam data | scam_name #1 must be the highest-impact scam (it gets surfaced as "The #1 reported scam is X") |
| Quick Safety Tips | `SAFETY_TIPS["<City>"]` dict | **MUST populate per city — see quality bar below.** The fallback ships generic boilerplate ("Keep phones in pockets…") |
| Table of Contents | auto from scam list | scam_name + `danger_level` are what the reader sees |
| Scam cards | scams[] (Step 4) | already covered |
| What to Do If You Get Scammed | `EMERGENCY_INFO["<Country>"]` (or city override) | per-city override uses key `"<Country> (<City>)"` for cities with distinct Tourist Police lines |
| FAQ | `FAQS["<City>"]` dict | **MUST populate — see quality bar below.** Fallback is empty |
| Related cities | auto from full corpus | none — Step 9 handles |

**American English non-negotiable.** Every prose surface (`story`, `red_flags`, `how_to_avoid`, `SAFETY_TIPS`, `FAQS`, scam_name) must be en-US. Not "labelled," "colour," "centre," "neighbourhood," "whilst," "amongst," "travelling," "organised," "realised," "favourite," "behaviour." Lint rule 1 enforces this on all surfaces; if you draft prose that quotes a Reddit title with BrE spelling, leave it inside `reddit_sources[]` only — never paste it into rendered prose.

**Quality bar — `SAFETY_TIPS["<City>"]` (4 bullets):**

Each tip is a complete, imperative sentence with a verb up front. Each one names a specific street, station, neighborhood, currency amount, or operator the reader can act on. NYC-grade examples:

```python
"New York City": [
    "Ignore anyone offering you a CD, friendship bracelet, or any unsolicited item on Times Square — it will cost you.",
    "Use only licensed yellow cabs (medallion taxis), green boro taxis, or the Uber/Lyft apps — unlicensed cars are illegal and unaccountable.",
    "Keep phones in pockets at all times on the subway — phone snatches through closing doors are a known and increasing pattern.",
    "At Times Square and Penn Station, ignore scalpers offering discounted Broadway or concert tickets — use TodayTix or official box offices.",
],
```

Anti-pattern (don't ship this — these are the generic fallbacks the generator inserts when `SAFETY_TIPS["<City>"]` is missing):

```python
# REJECT — generic, no city specificity, no named places, no prices
"Keep phones and valuables in secure pockets when in crowded areas",
"Use only licensed taxis or app-based ride services",
"Book tours and tickets through verified operators with online reviews",
"Keep a copy of your passport separate from the original",
```

If your draft tips read like the rejected list — rewrite. Each tip must name something a reader couldn't infer from the city name alone.

**Quality bar — `FAQS["<City>"]` (5 questions):**

Each Q&A is 2–4 sentences, names specific neighborhoods/operators/prices, and answers a question a real traveler would search. NYC-grade examples:

```python
"New York City": [
    ("How do I get from JFK Airport to Manhattan?",
     "The AirTrain to Jamaica Station, then LIRR to Penn Station costs about $15 total and takes 45–55 minutes — cheap but requires luggage management. The AirTrain to Jamaica then E/J/Z subway costs about $8.75 and takes 60–70 minutes. Licensed yellow taxis have a flat rate of $70 to Manhattan (plus tolls and tip). Uber/Lyft are typically $55–$90 depending on traffic. Avoid any driver who approaches you inside the airport."),
    # …4 more, each city-specific
],
```

Required slots in the 5 Q&As:
1. "Is `<city>` safe for tourists?" — neighborhood-level safety, not abstract
2. "What is the most common scam in `<city>`?" — references the #1 scam from your scams[] (and ideally the runner-up)
3. Transport question — airport-to-city or local-transit fare and routing, with prices
4. Free/safe-walking question — name actual neighborhoods, parks, or attractions
5. Money/ATM/exchange question — name actual banks, ATM locations, or rates

**Quality bar — `EMERGENCY_INFO["<Country>"]` (or city override):**

Confirm by direct fetch from the embassy `.gov` site (Step 2C); never copy from SerpAPI summaries (numbers change annually). Required keys (see existing entries in `scams/generate_pages.py`):

```python
"Egypt": {
    "police_name": "Egyptian Police / Tourist Police",
    "police_number": "122 (Police) or 123 (Emergency)",
    "report_url": "https://www.moi.gov.eg/",
    "report_site": "moi.gov.eg",
    "lost_passport": "<embassy address + emergency phone — verbatim from the embassy site>",
    # ...follow the existing shape exactly
},
```

City-level override (use when a city's Tourist Police line, US Consulate phone, or passport-replacement office differs from the country default — common in Egypt where Cairo, Sharm El Sheikh, and Hurghada each publish distinct Tourist Police numbers):

```python
"Egypt (Sharm El Sheikh)": { ... },
```

The generator looks up `EMERGENCY_INFO[f"{country} ({city})"]` first, falls back to `EMERGENCY_INFO[country]`, and finally falls back to UK as a last resort. **Never let a page ship with the UK fallback — that's a critical bug.**

### Step 5: Lint — pre-generation gate

Run [scripts/lint_scam_content.py](scripts/lint_scam_content.py) against the drafted city JSON. If the script does not yet exist, build it with this spec (same file, `.py`):

**Lint rules (all REJECT unless marked WARN):**

1. **AmE/BrE drift** — regex over 17 word pairs:
   ```
   \b(travell?ers?|favou?r(?:ite|ed)?|colou?r(?:ed|ful)?|centred?|neighbou?r(?:hood)?|organis(?:e|ed|ation)|authoris(?:e|ed)|recognis(?:e|ed)|analys(?:e|ed)|realis(?:e|ed)|emphasis(?:e|ed)|apologis(?:e|ed)|summaris(?:e|ed)|theatre|jewellery|defence|licence|aluminium|behaviou?r|programme|holidaymakers?|whilst|amongst)\b
   ```
   Match on BrE forms only (e.g., `traveller`, `favour`, `colourful`, `centre`, `organised`, `theatre`, `jewellery`, `defence`, `licence`, `aluminium`, `behaviour`, `programme`, `holidaymaker`, `whilst`, `amongst`). Allowlist: proper nouns from style guide §1 never-touch list (`Centre Pompidou`, `Theatre District`, `Metropolitan Centre for Tropical Medicine`, `Programme National`, etc.), and any match inside single-quoted Reddit titles in `reddit_sources[]`.

2. **Reddit citation in prose** — regex `r/\w+\s*['"]|comments/[a-z0-9]{6,8}\b` present in any of `story`, `red_flags[*]`, `how_to_avoid[*]` → REJECT (use `reddit_sources[]` only).

3. **Currency spacing** — any `[A-Z]{1,3}\$?\d` (no space between symbol and number) → REJECT. Exception: inside `reddit_sources[]` titles.

4. **Currency range** — any range using hyphen `-` instead of en-dash `–` between currency amounts, or any range that drops the symbol on the second amount (e.g., `RM 50–100` instead of `RM 50–RM 100`) → REJECT.

5. **Em-dash spacing** — `—` without a surrounding space on at least one side (mid-word hyphen `-` OK) → REJECT.

6. **Sentence length** — any sentence > 50 words → WARN; > 70 words → REJECT.

7. **Paragraph length** — any `story` paragraph > 120 words → REJECT; > 100 → WARN.

7b. **Paragraph count** — `story` has fewer than 3 paragraphs (count `\n\n` separators: must be ≥ 2) → REJECT. More than 5 → WARN. The 3-beat narrative (setup → pivot → mechanism) is the floor; longer scams may extend Beat 3 across 2–3 paragraphs but should not re-introduce defense steps the `how_to_avoid` list already carries.

8. **ALL-CAPS budget per story** — count of ALL-CAPS tokens (`[A-Z]{3,}`) > 12 → WARN; > 18 → REJECT.

9. **Age-gating** — `\b(older travell?ers?|seniors?|pensioners?|retirees?|elderly travell?ers?)\b` → REJECT.

10. **Alarmist / breezy interjections** — `\b(OMG|pro tip|literally|insane|crazy|sketchy af|legit)\b` → REJECT. Also `\bwhilst\b` and `\bamongst\b` (caught by rule 1 too).

11. **Opening repetition** — if ≥ 3 scams on the same page share a 2-word opening (case-folded), WARN.

12. **Bullet completeness** — every `how_to_avoid[i]` must end in `.`, `?`, or `!`. Every `red_flags[i]` must contain ≥ 4 words. → REJECT.

13. **`scam_name` length** — > 60 chars → REJECT.

14. **`location` length** — > 5 comma-separated entries → WARN.

15. **`reddit_sources[]` year mix** — < 80% from 2025/2026 → WARN.

16. **`reddit_sources[]` count** — ≠ 5 per scam → REJECT.

17. **`red_flags` + `how_to_avoid` counts** — ≠ 5 each → REJECT.

Lint output: `/tmp/scam-research/<slug>/lint-report.json`. All REJECT rules must pass before Step 6. WARN rules surface to the user for judgment.

### Step 6: Claim-token audit

For each scam, extract all numeric and named-entity tokens from `story`, `red_flags`, `how_to_avoid`:

```python
import re, spacy
nlp = spacy.load("en_core_web_sm")

def extract_tokens(text):
    # Numbers with currency prefix
    currency = re.findall(r'\b(?:RM|R\$|€|£|\$|¥|USD|EUR|THB|JPY|ARS|BRL)\s?\d[\d,\.]*\b', text)
    # Standalone numbers (ages, years, counts)
    standalone = re.findall(r'\b\d{2,}\b', text)
    # Named entities
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents if ent.label_ in ('PERSON','ORG','GPE','FAC','LAW','MONEY','DATE','PERCENT')]
    return currency + standalone + entities
```

For every extracted token, search the audit trail (`/tmp/scam-research/<slug>/`) for a substring or token-set match. Tokens with zero matches → claim is unsupported → **rewrite or remove** the sentence.

Save `/tmp/scam-research/<slug>/claim-tokens.json` with one row per claim, its source match(es), and match confidence.

### Step 7: Update `scams/generate_pages.py`

Add entries (alphabetical order within each dict):

**`CITY_SLUGS`** (grep `^CITY_SLUGS = ` in `scams/generate_pages.py`):
```python
"<City>": "<slug>",
```

**`SAFETY_TIPS`** (grep `^SAFETY_TIPS = `):
```python
"<City>": [
    "<imperative tip 1, ≤ 20 words, verb-first>",
    "<tip 2>",
    "<tip 3>",
    "<tip 4>",
],
```

**`FAQS`** (grep `^FAQS = `):
```python
"<City>": [
    ("Is <city> safe for tourists?", "<answer, 2–3 sentences, covers common sense + neighborhoods to prefer/avoid>"),
    ("What is the most common scam in <city>?", "<answer, references the #1 scam from the 6>"),
    ("<city-specific question — e.g., 'Is Grab safe in Kuala Lumpur?', 'How much should a taxi from <airport> cost?'>", "<answer>"),
    ("Where is it safe to walk in <city>?", "<answer, neighborhood recommendations>"),
    ("<city-specific question — e.g., 'Is it safe to change money on the street?', 'Are ATMs safe in <city>?'>", "<answer>"),
],
```

**`EMERGENCY_INFO`** (grep `^EMERGENCY_INFO = `) — only if country is missing, or if the city needs an override:
```python
"<Country>": {
    "police_name": "<official name>",
    "emergency": "<dialable number>",
    "police": "<dialable number>",
    "tourist_police": "<dialable number or None>",
    "consumer_protection": "<dialable number or None>",
    "embassy_us": "<phone>",
    # ... follow the existing shape in the file
},
```

Per-city override uses key `"<Country> (<City>)"`.

### Step 8: Append to `scams/research/<cc>_batchN.json`

Check for the latest batch file for this country:

```bash
ls scams/research/<cc>_batch*.json 2>/dev/null | sort -V | tail -1
```

If the latest batch has ≥ 5 cities, create `scams/research/<cc>_batch<N+1>.json` as a new JSON array. Otherwise append to the latest.

Preserve 2-space JSON indent (`json.dumps(..., indent=2, ensure_ascii=False)`). Trailing newline required.

### Step 9: Regenerate

Use the `regenerate_city()` helper — it loads every research batch and builds the full `related_cities_map` internally, so `.related-section` always renders.

```python
import sys
sys.path.insert(0, "scams")
from generate_pages import regenerate_city
regenerate_city("<City>")  # writes scams/<slug>/index.html
```

If the country has ≥ 2 cities, regenerate its country hub too:

```python
from generate_pages import regenerate_country_hub
regenerate_country_hub("<Country>")  # returns None if < 2 cities, else the output Path
```

**If the country has a live Amazon book** (japan, italy, france, indonesia, brazil, portugal, canada, united-kingdom, vietnam, germany, spain, greece, thailand — authoritative list in [scripts/book-cta-rollout/apply_book_ctas.py](scripts/book-cta-rollout/apply_book_ctas.py) `COUNTRIES` dict), run the book-CTA insertion next so the new page matches existing pages in that country:

```bash
python3 scripts/book-cta-rollout/apply_book_ctas.py
```

### Step 9b: Sync `api/v1/scams/<slug>.json` (single source of truth)

Per ARCHITECTURE.md and PR #1001, `api/v1/scams/` is the canonical machine-readable feed for the site (consumed by book builders, the public `/api/` endpoint, and any cross-city compare workflows). HTML is the source; api/v1 is synced from it. **Never let a new city ship with HTML but no api/v1 entry — book builders and the API both go silent on that city.**

```bash
python3 scripts/sync_api_from_html.py <slug>
```

The script reads `scams/<slug>/index.html`, walks every `.scam-card`, and writes the matching `tldr` + `description` + `severity` fields into `api/v1/scams/<slug>.json`. `severity` is mapped from each card's `danger-badge` class (`danger-high → high`, `danger-medium → moderate`, `danger-low → low`) — the HTML page is the single source of truth, and any stale value in the api/v1 JSON gets overwritten on sync. If the JSON file does not yet exist for a brand-new city, **stop and ask**: a fresh JSON skeleton has to be hand-bootstrapped (id, name, category, frequency, location, tags) before sync will populate prose and severity. Existing-city re-syncs Just Work.

### Step 10: Parser-based verification

```python
from bs4 import BeautifulSoup
import json, re, sys
sys.path.insert(0, "scripts/book-cta-rollout")
from apply_book_ctas import COUNTRIES as _BOOK_COUNTRIES
COUNTRIES_WITH_BOOKS = {v["name"] for v in _BOOK_COUNTRIES.values()}

html = open("scams/<slug>/index.html").read()
soup = BeautifulSoup(html, "html.parser")

# Editorial-v2 shell
body = soup.select_one("body")
assert body and "editorial-v2" in body.get("class", []), "missing body.editorial-v2"

h1 = soup.select_one("h1")
assert h1 and h1.select_one("em"), "H1 must wrap city in <em>"

required_blocks = [".hero", ".hero-badge", ".severity-summary", ".reading-time",
    ".takeaways-box", ".safety-box", ".toc", ".emergency-fab",
    ".back-to-top", ".action-grid"]
for sel in required_blocks:
    assert soup.select_one(sel), f"missing {sel}"

# Related-section requires full corpus from Step 9
rel = soup.select_one(".related-section")
assert rel, "missing .related-section (did Step 9 load ALL research batches?)"
assert len(rel.select(".related-card")) >= 3, "related-section needs ≥3 cards"

# TOC entry count matches scam count
toc_entries = soup.select(".toc-list li")
cards = soup.select(".scam-card")
assert len(toc_entries) == len(cards), f"TOC has {len(toc_entries)} entries, {len(cards)} scam cards"

# Per-card structural checks
assert len(cards) == <N>, f"expected <N> cards, got {len(cards)}"
for i, card in enumerate(cards, 1):
    assert card.select_one(".scam-header"), f"scam {i} missing header"
    assert card.select_one(".scam-location"), f"scam {i} missing location"
    assert card.select_one("p.scam-tldr"), f"scam {i} missing tldr"
    tldr = card.select_one("p.scam-tldr").get_text()
    assert len(tldr) >= 30, f"scam {i} tldr too short: {tldr!r}"
    assert tldr.strip()[-1] in ".?!", f"scam {i} tldr doesn't end in .?!: {tldr!r}"
    bodies = card.select("p.scam-story-body")
    assert 3 <= len(bodies) <= 6, f"scam {i} expected 3–6 body paragraphs, got {len(bodies)}"
    for p in bodies:
        text = p.get_text()
        word_count = len(text.split())
        assert len(text) >= 80, f"scam {i} has short story paragraph"
        assert word_count <= 120, f"scam {i} has paragraph > 120 words ({word_count})"
    red_flags = card.select(".red-flags li")
    avoid = card.select(".avoid li")
    assert len(red_flags) == 5 and len(avoid) == 5, f"scam {i} bullet count wrong"
    for li in red_flags + avoid:
        assert li.get_text().strip(), f"scam {i} has empty <li>"

# Schema.org JSON-LD
scripts = soup.find_all("script", {"type": "application/ld+json"})
for s in scripts:
    json.loads(s.string)  # must parse
ld = json.loads(scripts[0].string)
faq = next((g for g in ld["@graph"] if g["@type"] == "FAQPage"), None)
assert faq and len(faq["mainEntity"]) == 5, "FAQ schema count wrong"

# Book-CTA check (COUNTRIES_WITH_BOOKS imported above from apply_book_ctas.py)
if "<Country>" in COUNTRIES_WITH_BOOKS:
    assert soup.select_one(".book-mid-cta"), "country has live book — run apply_book_ctas.py"
    assert soup.select_one(".book-end-cta"), "country has live book — run apply_book_ctas.py"

# Orphan-phrase check (known sanitizer bug)
orphans = re.findall(
    r"(?:is|are|establishes?|documents?|captures?|tracks?)\s+the\s+(?:2025|2026|canonical|community|baseline|recurring|first[- ]person|named)\s+(?:anchor|baseline|reference)",
    html
)
assert not orphans, f"orphan sanitizer phrases found: {orphans[:5]}"

# Scam-comic img — deferred to comic-batch PR, expected absent on first-pass
# (If adding comics at the same time: assert card.select_one("img.scam-comic") per card)
```

Any failure → fix, re-run Step 9, re-verify. **Do not commit broken HTML.**

### Step 11: Hub integration

**11a. Regenerate the master `/scams/index.html` hub:**

```bash
python3 scripts/regenerate_scams_hub.py
```

This scans every `scams/<slug>/index.html`, rebuilds the stats-bar, country-filter pills, city-grid (alphabetical), and JSON-LD `numberOfItems` — all from the filesystem (authoritative). Replaces the old manual card-insertion + 3-stat-bump + 2-JSON-LD-counter workflow with a single command. If a warning about an unknown country code appears, add it to `COUNTRY_META` in the script.

**11b. Country hub (if country has ≥2 cities):**

Option A — country hub already exists (e.g. `/scams/country/us/`): append a new `<a class="city-card">` entry (same format as the existing cards in that file) and update the top stats. Use the surrounding entries as template.

Option B — country hub does not yet exist and this new city crosses the 2-city threshold: call `generate_country_page()` per Step 9.

**11c. If the country has a live Amazon book**, run the hub-stats audit script afterwards to sync every per-city scam count visible on the country hub:

```bash
python3 scripts/book-cta-rollout/audit_country_hub_scam_counts.py --only <cc>
```

This fixes: country-hub meta-description totals, hero subtitle, hero stat-pill, body intro paragraph, per-city `.city-card-count` and `.city-risk-badge` counts.

### Step 12: Commit + PR

One city = one PR.

```bash
# Branch is already set (claude/...)
git add scams/<slug>/ scams/country/<cc>/ scams/research/<cc>_batchN.json scams/generate_pages.py scams/index.html
git commit -m "$(cat <<'EOF'
scams: add <City> (<Country>) — <N> Reddit-cited scams

- <N> scams documented (<high>H/<mod>M/<low>L)
- <N> × 5 Reddit sources, ≥80% from 2025/2026
- <N> × T1/T2 corroborating source (gov/operator/reputable news)
- Lint: 0 REJECT, <W> WARN
- Comics: deferred to comic-batch PR

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

PR body template:

```markdown
## Summary

Adds `<City>` to tabiji scam coverage with <N> Reddit-cited scams.

## Scams added
1. **<scam_name>** (<danger>) — authoritative source: <T1/T2 URL>
2. ...

## Data quality
- ≥ 80% Reddit sources from 2025/2026: ✅
- T1/T2 corroboration per scam: ✅
- Lint: 0 REJECT, <W> WARN
- Parser verification: ✅

## Out of scope (follow-up PRs)
- [ ] Comic generation — next comic-batch PR
- [ ] If AmE drift / orphan-phrase bugs found in existing pages: [pending_scam_cleanup_prs memory]

## Test plan
- [ ] `regenerate_city("<City>")` runs clean and emits editorial-v2 shell
- [ ] `/scams/<slug>/` loads with all scam cards + `.related-section` + `.toc-list`
- [ ] `/scams/country/<cc>/` lists the new city with correct scam count
- [ ] `/scams/` hub (after `python3 scripts/regenerate_scams_hub.py`) shows the new city in the grid + stats-bar reflects it
- [ ] Schema.org validates (no JSON-LD errors)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## Known traps

1. **Sanitizer orphan-phrase bug** — `_sanitize_reddit_shards` (from `scripts/clean_us_reddit_shards.py`) strips `r/<sub> '<title>' (comments/xxx, YEAR)` strings from prose at render time, but sometimes leaves trailing editorial tags like "is the community baseline", "established the recurring pattern", "are first-person anchors". **Prevention**: never embed Reddit citations in `story`/`red_flags`/`how_to_avoid` prose. Thread links go in `reddit_sources[]` only. Rule 2 of the lint catches this.

2. **`make_tldr` mid-sentence cuts** — the generator's first-sentence splitter (`make_tldr` in `scams/generate_pages.py`) falls back to a char-100 nearest-word cut when it can't find `. ` or ` — ` in the first 160 chars. If the first sentence is long and has no mid-sentence period/em-dash, the TLDR becomes a truncated fragment. **Prevention**: open Para 1 with a ≤ 160-char complete sentence ending in `.` or ` — `. Also beware of `"St. "` / `"Dr. "` / `"Mt. "` abbreviations at the start — the period gets treated as sentence-end. Use `"Saint Louis"` spelling in the first sentence to work around.

3. **AmE drift** — style guide locked en-US on 2026-04, but drift recurs (e.g., `colourful` in `scams/kuala-lumpur/index.html:416`). Lint rule 1 catches 17 pairs but will miss new forms. Add any new drift to the regex as it's discovered.

4. **Proper-noun allowlist** — `Centre Pompidou`, `Theatre District`, `Metropolitan Centre`, `Programme National`, `Lei 13.419/2017`, `IBAMA`, `DEATUR`, `INMETRO`, etc. Treat as literal identifiers; lint must not flag.

5. **Reddit thread ID verification** — IDs are 6–8 lowercase alphanumeric. Any deviation (`comments/1qru2ox_wrong`, longer IDs, uppercase) is a typo. Always verify via `.json` fetch.

6. **Hardcoded paths** — ignore `scripts/generate_new_scam_pages.py` (hardcoded `BASE = "/Users/bjh/Documents/tabiji"`, wrong machine). Always use the `regenerate_city()` / `regenerate_country_hub()` helpers from `scams/generate_pages.py`.

7. **Comic URL cache-bust** — when comics are later uploaded in the comic-batch PR, the generator already writes `?v=1` by default; bump to `?v=2`, `?v=3` on re-upload.

8. **Per-country research-batch file conventions** — some countries have multiple batches (`ar_batch1..6`), some have one (`my_batch1`). New countries → start at `<cc>_batch1.json`.

9. **Country hub auto-build threshold** — `build_country_data` in `scams/generate_pages.py` only builds a country hub if the country has ≥ 2 cities. The first city in a new country creates no country hub; it appears once the second city is added. This is expected.

10. **Reddit privacy** — Reddit is public; no username attribution in prose is required. Use `r/<sub>` + thread-link in `reddit_sources[]`. Never lift DM content or deleted-post content (even if cached in the audit trail).

11. **Regulatory citations** — original language + English gloss on first mention (e.g., "IBAMA (Brazil's environmental protection agency)"). Style guide §5.

12. **Never-touch fields** — Reddit thread titles in `reddit_sources[]` are verbatim citations; preserve BrE spellings, emoji, question marks, casing. Lint rule 1 has an exception for single-quoted strings inside `reddit_sources[]`.

## Audit-trail layout (`/tmp/scam-research/<slug>/`)

```
/tmp/scam-research/<slug>/
├── serpapi/
│   ├── reddit-<query-hash>.json
│   └── news-<query-hash>.json
├── reddit/
│   └── <thread-id>.json
├── news/
│   ├── <pub>-<yyyymmdd>.html
│   └── <pub>-<yyyymmdd>.archive.txt       # wayback URL + archive.ph URL
├── gov/
│   ├── embassy-<country>.html
│   └── tourist-police-<country>.html
├── operator/
│   ├── airport.html
│   ├── transit-<city>.html
│   └── attraction-<name>.html
├── reddit-index.json                       # parsed Reddit metadata per thread
├── news-index.json                         # parsed news metadata + claim tokens
├── claim-tokens.json                       # token → source match matrix
└── lint-report.json                        # lint output
```

This directory is intentionally outside the repo (not `.gitignore`d, just `/tmp/`). It's an audit trail for the single PR. Refer to specific files in the PR body where helpful.

## Quality gates (all must pass before PR)

- [ ] 3–6 scams × (3-paragraph story, 5 red flags, 5 how-to-avoid, 5 Reddit sources)
- [ ] ≥ 80% Reddit sources from 2025/2026
- [ ] Every scam has ≥ 1 T1/T2 (gov/operator/reputable news) corroboration
- [ ] Lint: 0 REJECT (WARN surfaced and judged)
- [ ] Claim-token audit: every numeric and named claim has a source match
- [ ] Parser verification: 0 failures
- [ ] `scams/<slug>/index.html` ≥ 20 KB
- [ ] `<body class="editorial-v2">` + `<h1>` with `<em>{city}</em>` wrap (PR #420)
- [ ] `.toc-list`, `.emergency-fab`, `.back-to-top`, `.action-grid` all present
- [ ] `.related-section` renders with ≥ 3 related cards (load full batch corpus in Step 9)
- [ ] `.book-mid-cta` + `.book-end-cta` present if country has live Amazon book
- [ ] `scams/country/<cc>/index.html` lists new city with correct count
- [ ] `scams/index.html` has a new `.city-card` anchor + stats-bar + meta-description updated
- [ ] `api/v1/scams/<slug>.json` populated via `scripts/sync_api_from_html.py <slug>` (book builders + public API consume this — see Step 9b)
- [ ] Schema.org JSON-LD parses cleanly; FAQPage has 5 entries
- [ ] Emergency contacts on defense paragraph of every scam
- [ ] Audit trail complete under `/tmp/scam-research/<slug>/`

## Not in scope (separate PRs)

1. **Comic generation** — defer to next comic-batch PR using `docs/comic-pipeline/` + per-country style. The generator writes `<img class="scam-comic">` tags with 404-until-uploaded URLs; acceptable until comic follow-up.
2. **AmE drift sweep on existing pages** — see memory `pending_scam_cleanup_prs.md`. Use this skill's lint script as the audit tool.
3. **`_sanitize_reddit_shards` / `make_tldr` bug fixes** — see memory `pending_scam_cleanup_prs.md`. New pages written via this skill avoid the bug by never embedding Reddit citations in prose.
4. **Enriching already-published pages** — this skill builds from scratch only; enrichment (adding scams 7–10 to a page that already has 6) is a separate workflow.
