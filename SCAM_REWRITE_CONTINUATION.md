# SCAM_REWRITE_CONTINUATION.md
## Handoff for the next Claude session

You are continuing a long-running multi-session task: rewriting every scam-page narrative across all city pages in the tabiji.ai corpus to match the **NYC 3-beat narrative pattern** with **trap-summary TLDRs** and **city-specific factual specificity**.

**Read this entire document before doing any work.** It encodes a quality bar the user has restated repeatedly. Skimming it and starting fast will produce work the user rejects.

---

## 0. WHERE YOU ARE RIGHT NOW

**Branch**: `claude/bold-bhabha-956437` (rebased on `main`)

**Worktree**: `/Users/psy/repos/tabiji/.claude/worktrees/bold-bhabha-956437/`

**Source of truth for queue state**: `scripts/queues/scam-narrative-rewrite-queue.json`

**Current progress** (as of this handoff write — 2026-04-25):
- ✅ Tier 1 flagships — 13 cities, 99 cards (PR #497 merged)
- ✅ Book-secondary P15–P40 — 26 cities (PRs #502 #503 merged)
- ✅ Book-secondary P41–P85 — 45 cities (PRs #520 #547 #572 #600 #620 merged)
- ✅ Book-secondary P86–P93 — 8 cities, 48 scams (PR #640 OPEN — Frankfurt → Hamburg)
- ⏳ **Next up: P94 Ho Chi Minh City (Vietnam, 6 scams)** — DEFERRED from P86–P95 batch
- ⏳ Then P95 Hoi An (Vietnam, 6 scams), then P96+

**Branch state**:
- Worktree branch: `claude/bold-bhabha-956437-p86` (PR #640 awaiting review/merge)
- Once #640 merges, start fresh from `origin/main` for the P94+ batch (do NOT continue on -p86 branch).

**P94 / P95 audit notes** (use these to plan the next batch):
- ho-chi-minh-city: 6 scams, TOC=Y, sanit=0, BrE=0, redd=4, miss_T=3, miss_S=6, non3body=0
- hoi-an: 6 scams, TOC=Y, sanit=0, BrE=7, redd=4, miss_T=1, miss_S=6, non3body=1
  - HCMC: 4 Reddit shards in body (not just hero/meta) — scrub during rewrite
  - Hoi An: 7 BrE hits, 4 Reddit body shards, scam #1 has non-3-body — needs structural attention

To verify the next pending priority before starting:

```bash
python3 -c "
import json
data = json.load(open('scripts/queues/scam-narrative-rewrite-queue.json'))
secondary = [c for c in data['queue'] if c.get('tier') == 'book-secondary' and c.get('status') == 'pending']
print(sorted(secondary, key=lambda c: c.get('priority', 999))[0])
"
```

The queue tracks `slug` (the directory name under `scams/`), `priority`, `scam_count`, and `status`. `slug` is what you pass to lint and API-sync scripts.

---

## 1. THE QUALITY BAR (read this carefully — re-read it if you start to drift)

The user has been extremely explicit, multiple times across multiple sessions:

> "We are not taking shortcuts here, each page must be done by hand, one at a time, when the page is marked as done, then you can move onto the next item."

> "Do you understand that each rewrite happens one at a time using opus 4.7 max care?"

> "Be extra thorough on how thorough we need these jobs to be."

This means:

### 1.1 No batching
- **One city per commit.** Not two, not three. One.
- Lint, sync API, sync partials, commit, push — all per city.
- Push every 5–10 cities. Open a PR every 10–15 cities.
- Do NOT use sub-agents to parallelize. The user explicitly said no shortcuts.

### 1.2 No skimming
- Read the **full HTML** for the city (every scam card, top to bottom) before editing anything.
- Audit each scam individually — what's wrong? What needs fixing?
- Identify all problems before you start writing — drift fixes are part of the same commit, not "I'll get to it later."

### 1.3 No template-pasting
- Each scam needs city-specific factual specificity:
  - **Real prefecture-set or city-mandated taxi rates** (€32 Nice→center, €50 Marseille airport→center daytime, €240–€275 Nice→St-Tropez, ¥31 Ciampino→Rome, etc.) — not generic "official prices."
  - **Named real licensed operators** (Co.Ta.Ca. Capri taxi, Cooperativa Battellieri Capresi, Compagnie des Guides de Chamonix IFMGA, Free Tours by Foot Montreal, MYBA/ECPY Mediterranean yacht brokers, Authentique Bouchon Lyonnais Lyon).
  - **Exact attraction admission prices** (€19.09 Alhambra, €13 Mont Saint-Michel Abbey, €22 Pompei adult, €17.50 Funchal Monte Palace Tropical Garden).
  - **Real police protocols** (carte professionnelle ID requirement in France, "Tourist Police" doesn't exist in France diagnostic, 17/112 EU emergency, 1155 Thailand Tourist Police, +351 21 864 1000 Polícia Judiciária Portugal).
  - **Specific named scam operators** (Klass Wagen Faro/Lisbon, Walker Tours Granada, Madeira.fun aggregator, Olafemi Tours Rio favela, Diamond Karaoke Sri Don Chai Chiang Mai, "Marc the Beggar" Osaka, Le Nouveau Duluth fake-TripAdvisor #1 Montreal).

### 1.4 No fluff sentences
Every sentence in a TLDR or body must carry weight: **actor + mechanic + cost + variant**.

| ❌ NOT acceptable | ✅ Acceptable |
|-----------------|--------------|
| "Beware of taxi scams in Nice." | "Nice taxi drivers quote €60–€80 'flat rates' from the airport when the prefecture-set rate is exactly €32 to Nice city center, €85 to Cannes, and €95 to Monaco — and 'broken meter' claims with cash-only demands strip another 50–100% off tourists who don't know the regulated numbers." |
| "Pickpockets are common in tourist areas." | "Pickpocket teams work Lyon's Tram Lines A and B during morning rush (7–9 AM) and evening rush (5–7 PM) — they use a directions-ask or staged-fall distraction at the Saint-Charles transfer while accomplices lift wallets and phones from back pockets and outer backpack compartments." |
| "Fake monks ask tourists for money." | "Saffron-robed 'monks' near Wat Phra That Doi Suthep, the Old City Sunday Walking Street, and the northeast moat corner present laminated 'temple project' cards with donation books listing pre-filled £20–$50 amounts to social-pressure 200–2,000 baht out of you — real Theravada monks never solicit cash from tourists, and many of these 'monks' are Chinese nationals running a known scam." |

### 1.5 The bolded defensive move is REQUIRED
Every scam must have a `<strong>` tagged actionable defense in the third body paragraph.

**Format**: `<strong>[Specific actionable advice with exact venue/operator/protocol names]</strong>.`

| ❌ NOT acceptable | ✅ Acceptable |
|-----------------|--------------|
| `<strong>Be vigilant in tourist areas.</strong>` | `<strong>Use only official taxis from the marked rank outside Nice Côte d'Azur Arrivals — confirm the €32 prefecture rate before bags go in the trunk, demand the meter ("au compteur, s'il vous plaît") for non-airport runs, and never follow anyone who solicits inside the terminal.</strong>` |
| `<strong>Don't trust strangers.</strong>` | `<strong>If anyone in plain clothes claims to be police in Marseille, do not produce your wallet — show only a photocopy of your passport, ask to see the officer's "carte professionnelle" (legally required ID with photo and badge number), and insist on continuing any inspection at the nearest commissariat ("nous allons au commissariat ensemble").</strong>` |

### 1.6 TLDR is trap-summary, not narrative-opener, not descriptive

The TLDR is the single most-read sentence on the scam card. It must be a **trap-summary**: actor + location + mechanic + cost + variant — in plain English, in one or two sentences max.

**Three failure modes to avoid:**

1. **Narrative-opener TLDR**: "You are walking through Place Bellecour when a man approaches..." — this belongs in Beat 1, not the TLDR.

2. **Descriptive TLDR**: "Lyon has many pickpockets in tourist areas." — generic, no specifics, useless.

3. **Sanitizer-leaked subjectless TLDR**: "often as 'Marc.' He explains he's a fellow traveler..." — broken mid-sentence (a Reddit username got stripped from the start, leaving an orphan).

**The structural rule**: `[Actor] in [specific location] do [specific mechanic] for [specific amount range] — [variant or context].`

---

## 2. THE 3-BEAT NARRATIVE ARC

After the TLDR, each scam has 3 body paragraphs with `<p class="scam-story-body">`:

### Beat 1 — Setup + Hook
- Concrete sensory scene: where you are, what you're doing, what catches your attention.
- The bait or opening move — what the scammer says, hands you, or stages.
- Reader is now invested in "what happens next."

**Example (Capri Blue Grotto)**: "It's a sunny morning at Marina Grande and you're queuing for the Capri must-do — the boat ride to the Grotta Azzurra, the famous blue-light cave. The signage at the harbor advertises '€18 boat tour' and you're prepared. By the time you've paid four separate parties at the cave mouth, the actual cost is €35–€45 per person."

### Beat 2 — Pivot + Pressure
- The reveal — when you realize something is wrong, or the mechanic crystallizes.
- Specific dollar/euro/baht amounts.
- Variants and edge cases (named scam operators, alternate venues).
- Real citations or news anchors when available (Le Parisien, CBC News, Repubblica Napoli, Metropolis, Fanpage, NHK, Bangkok Post, etc.).

**Example (Capri Blue Grotto)**: "Four separate parties collect money at the cave mouth: the transfer boat from Marina Grande (€18), the Cooperativa Battellieri Capresi rowboat-plus-entry (€18), a customary €2–€5 tip the rower states out loud while you're already inside the cave, and a €2 Comune tax. A 2025 Capri.it review titled 'Truffa al 100%' documents operators charging €24 per person for a boat tour that never enters the grotto, issuing no refund — and an August 2024 Ferragosto incident captured by Fanpage showed two rival boatmen physically fighting at the cave mouth in front of tourists."

### Beat 3 — Mechanism + Defense
- Why the scam works structurally.
- The bolded defensive move with `<strong>` tag.
- Real escape options and verified alternatives.
- Police hotlines, official URLs, real licensed operator names.

**Example (Capri Blue Grotto)**: "The Cooperativa Battellieri has a monopoly on the rowboat transfer and has been flagged to the Comune di Capri repeatedly without consistent action. <strong>Budget €35–€45 per person if you go and accept all four fees as the real cost — never get on a boat tour that promises 'guaranteed grotto entry' on a windy day, because operators charge the boat-tour fare anyway and refuse refunds when the sea is too rough for entry.</strong> The April 2026 Comune ordinance against tourist 'accerchiamento' (with €500 fines for aggressive solicitation) applies to every tout funneling tourists toward this stack — any 'come with me, special price' grotto offer from someone not stationed at a signed counter is now both an overcharge risk and an illegal approach."

---

## 3. DRIFT PATTERNS TO FIX INLINE

When you read a scam page, you'll find some or all of these drift types. **Fix them in the same commit.** Don't note-and-skip.

### 3.1 Sanitizer-leaked subjectless TLDR
TLDR starts mid-sentence because a Reddit username or thread title was stripped:
- "often as 'Marc.' He explains he's a fellow traveler..." (Osaka)
- "a barrier-island lagoon with boat trips to uninhabited sand islands." (Faro)
- "Souda' names a specific station near Chania's main road junction..." (Heraklion)
- "the Romani community performs zambra flamenco in whitewashed hillside caves..." (Granada)

**Fix**: Rewrite the TLDR as a proper trap-summary. Restore the subject in the body opener.

### 3.2 Narrative-opener TLDR
TLDR is a story opener:
- "You are walking through Place Bellecour when..." (Lyon)
- "You park your car on a side street in Old Montreal." (Montreal)
- "Sometimes the Alhambra official site really is sold out for your dates." (Granada)

**Fix**: Rewrite as trap-summary. The narrative belongs in Beat 1.

### 3.3 Descriptive TLDR
TLDR is a generic statement:
- "Faro Airport is the Algarve's main gateway with massive UK/Irish/German package-tourism volume." (Faro)
- "Heraklion taxis are metered by Greek law and Tariff 1 (daytime urban) should read €1.06 per kilometre." (Heraklion)
- "Flamenco is Seville's soul — raw, passionate, born in these streets." (Seville)

**Fix**: Rewrite with actor + location + mechanic + cost.

### 3.4 Sanitizer-leaked body
References that lost their subject:
- " is the canonical 2025 victim account: '...'"
- " adds: '...'"
- " I'm a local, but sometimes I like to visit..."
- " gives the historical framing"
- "iews are suspect" (word-split: "Google reviews are suspect" → got truncated)
- "(u/anon, 2024)" — floating attribution tags

**Fix**: Restore the subject as a generic descriptor:
- "One canonical first-person account:"
- "Travelers report:"
- "Local residents confirm:"
- "Community consensus:"

Preserve the quoted content but give it a proper subject.

### 3.5 Curly-quote / curly-accent drift
API JSON has typographic quotes (`'`/`'`) or accents (é, ô, à) where HTML has straight or different. The sync script will warn about "scams not found in HTML."

**Fix**: Inline Python edit to align the API name to the HTML — see section 6.2.

### 3.6 Truncated word splits
Body has "from a fore" (cut mid-word "foreign country") or "Extens' ive" (apostrophe inserted in word) or "non' -violent" (hyphen-split):

**Fix**: Complete the word/sentence using context.

### 3.7 City-mismatch boilerplate
Emergency section references the wrong city's police body — e.g., Montreal had a "Vancouver Police Department" reference at the bottom of the page (template drift from another city). Liverpool had **"Metropolitan Police"** (London's force) when the correct force is **Merseyside Police**.

**Fix**: Replace with the correct city's police body and contact info. Verify against multiple known examples.

### 3.8 Missing table of contents (TOC)
Some pages were generated without the `<div class="toc">` block that links to each scam card. Without it, the page has no jump-navigation between scams.

**Reference**: https://tabiji.ai/scams/new-york-city/ — and any of Lake Garda, Liverpool, Madrid, Mykonos in this corpus already have the correct structure.

**Required structure** (insert just above the `<h2 class="section-heading">The N Scams</h2>` heading):

```html
<div class="toc">
    <h2>Jump to a Scam</h2>
    <ol class="toc-list">
        <li><a href="#scam-1"><span class="toc-badge high">High</span> Title 1</a></li>
        <li><a href="#scam-2"><span class="toc-badge high">High</span> Title 2</a></li>
        ...
    </ol>
</div>
```

**Required IDs**: every `<div class="scam-card">` must have an `id="scam-N"` attribute matching the TOC anchor. If the existing scam cards have no IDs, add them.

**Severity badge classes**: `high` (⚠️ High), `medium` (🔶 Medium), `low` (🟢 Low) — match the danger-badge severity in the scam-header.

**Fix**: When auditing a city, the very first check is `grep -q '<div class="toc">' scams/<slug>/index.html`. If missing, build one from the scam titles + severities and insert it.

### 3.9 British English drift
Tabiji.ai is American-English, but body content has accumulated British spellings — `centre`, `colour`, `behaviour`, `metres`, `kilometres`, `neighbourhood`, `jewellery`, `personalised`, `programme`, `favour`, `honour`, `labour`, `recognise`, `organise`, `analyse`, `defence`, `licence`, `catalogue`, `cancelled`, `traveller`, `harbour`, `summarise`, `coloured`, `behavioural`, `memorise`, `specialise`, `traumatise`, `finalise`.

This includes UK-context cities (Liverpool) that you might be tempted to leave in BrE for "authenticity" — DON'T. The site standard is American English, period.

**Fix**: Run the AmE grep before committing (see section 5). Use Python `replace_all` for systematic conversion. Watch for capitalized variants (e.g., `Centre` in proper-noun positions like "Liverpool City Centre BID" → "Liverpool City Center BID"). Watch for legitimate non-replacements (Spanish "Centro" / Italian "Centro" / French "centre-ville" stay — only replace English-language British spellings).

### 3.10 Reddit-shard citations
The original sanitization pipeline left two patterns visible to readers:

**Pattern A — hero shards** (template-wide):
- `<p>Real stories from Reddit travelers...` → `<p>Real stories from real travelers...`
- `<span>⭐ Reddit-sourced & verified</span>` → `<span>⭐ Community-verified</span>`

**Pattern B — body/FAQ shards** (sanitizer-leak vestiges in your own rewrites):
- `(traveler reports 2025)` parenthetical citations → strip
- `, per traveler reports)` → `)`
- `'a well known scam place' on traveler reports for` → `'a well known scam place' for`
- `documented in 2025 traveler reports warnings` → `documented in 2025 traveler reports`
- `the traveler reports moderator team posted` → `Travel forum moderators posted`
- `community reports across Reddit and Spanish-language travel forums anchor this` → `this is consistently reported by travelers`

**Exception**: Where Reddit is the actual scam vector (e.g., Mykonos #5 "Scorpios DM scam" where strangers contact tourists via Reddit DM), keep the Reddit mention in the TLDR/body — it's load-bearing. The moderator's actual quoted warning ('DON'T TRUST ANY OFFERS YOU RECEIVE THROUGH REDDIT') can stay; the framing around it should be cleaner.

**Fix**: Run the Reddit-shard grep before committing (see section 5).

---

## 4. THE WORKFLOW PER CITY (every step matters)

```
1. Read the queue file → identify next pending priority + slug
2. Read the city's full HTML with Read tool, top to bottom
3. STRUCTURAL CHECKS first (one grep, three answers):
   a. TOC present? → grep -q '<div class="toc">' scams/<slug>/index.html
      If missing: build TOC + add id="scam-N" to each scam-card (see 3.8)
   b. Hero subhead "Reddit travelers"? → grep -q 'from Reddit travelers'
      If yes: scrub (see 3.10 Pattern A)
   c. Hero meta "Reddit-sourced & verified"? → grep -q 'Reddit-sourced'
      If yes: scrub (see 3.10 Pattern A)
4. Audit each scam:
   - Does it have a TLDR? Trap-summary, narrative-opener, descriptive, or sanitizer-leaked?
   - Body: 3 paragraphs? Sanitizer leaks? Truncated words?
   - Is the defensive move bolded with <strong>?
   - Are there Reddit-shard citations in the body/FAQ? (see 3.10 Pattern B)
5. Rewrite each scam by hand, one Edit per scam:
   - Preserve red_flags and how_to_avoid lists unless they have leaks
   - Add or fix TLDR
   - Restore subject in body openers if sanitizer-leaked
   - Add bolded defense in Beat 3 if missing
   - Use American English throughout (see 3.9)
6. Run lint:
   python3 scripts/lint_scam_content.py --html-city <slug>
   → must return "0 REJECT 0 WARN"
7. Run API sync:
   python3 /tmp/sync_api_from_html.py <slug>
   → no warnings = success
   → "WARNING: N scams in API not found in HTML" → curly-quote drift OR full rebuild needed
8. Handle drift inline:
   - 1–2 stale scams = curly-quote/accent drift, fix via inline Python (see 6.2)
   - 3+ stale scams = full HTML-driven API rebuild (see 6.1)
9. Run partials sync:
   bash scripts/sync-partials.sh
   → "Updated 0 HTML file(s)" = success
10. Run the detection greps (see section 5):
    a. Sanitizer-leak grep (must return 0)
    b. British-English grep (must return 0)
    c. Reddit-shard grep (must return 0 for hero/meta; body Reddit only allowed where it is the scam vector)
11. Stage + commit per city with detailed audit message:
    - Per-card breakdown (what was wrong, what was fixed)
    - Sync notes (API regenerated, drift fixes)
    - Queue marked complete
12. Push every 5–10 cities
13. Open a PR every 10–15 cities with consolidated summary (or smaller batches per user direction)
```

**Time per city**: 30–45 minutes for a typical city; 60+ minutes for a city full of leaks (Faro, Funchal, Granada). This is the bar. Going faster means cutting corners — do not.

---

## 5. THE DETECTION GREPS

Run all three against the city HTML before committing. Any match = fix before commit.

### 5.1 Sanitizer-leak grep
```bash
grep -nE "( is the (canonical|named-anchor|locals-only|umbrella))| (adds|reinforces|gives|frames|flags|captures|documents|discusses|explains): '" scams/<slug>/index.html
```

**Why these patterns**: They catch sanitizer-stripped Reddit attributions where the leading subject (often a Reddit username) was removed but the verb + colon-quote remained. Examples that match:
- " is the canonical first-person account: '..."
- " adds: '..."
- " gives the historical framing"
- " flags Granada as part of..."

This pattern misses some leaks (especially ones with different verbs or no colon-quote). When in doubt, search the HTML for `'` followed by space-and-lowercase-letter — that's often a leak.

### 5.2 British-English grep
```bash
grep -nEi "\b(centre|colour|behaviour|metres|kilometres|neighbourhood|jewellery|personalised|programme|favour|honour|labour|recognise|organise|analyse|defence|licence|catalogue|cancelled|traveller|harbour|summaris|coloured|behavioural|memoris|specialis|traumatis|finalis)\w*\b" scams/<slug>/index.html
```

**Must return 0 hits**. Convert all British spellings to American — even in proper-noun positions like "Liverpool City Centre BID" → "Liverpool City Center BID". Spanish/Italian/French foreign-language proper nouns (Comisaría de Centro, Centro Storico, centre-ville) stay — only English-language British forms get replaced.

Inline Python for systematic conversion:
```python
replacements = [
    ('centre', 'center'), ('Centre', 'Center'),
    ('colour', 'color'), ('Colour', 'Color'),
    ('behaviour', 'behavior'),
    ('metres', 'meters'), ('kilometres', 'kilometers'),
    ('neighbourhood', 'neighborhood'),
    ('jewellery', 'jewelry'), ('Jewellery', 'Jewelry'),
    ('personalised', 'personalized'), ('Personalised', 'Personalized'),
    ('honour', 'honor'),
    ('cancelled', 'canceled'),
    ('traumatised', 'traumatized'),
    ('summarises', 'summarizes'),
    ('behavioural', 'behavioral'),
    ('harbour', 'harbor'),
    ('memorise', 'memorize'),
    ('finalise', 'finalize'), ('finalised', 'finalized'),
    ('organised', 'organized'), ('Organised', 'Organized'),
    # Add more as needed
]
```

### 5.3 Reddit-shard grep
```bash
grep -nE "Reddit travelers|Reddit-sourced|\(traveler reports 2025\)|, per traveler reports\)|on traveler reports for|traveler reports warnings|the traveler reports moderator team|community reports across Reddit" scams/<slug>/index.html
```

**Must return 0 hits**. The hero subhead and meta tag patterns are template-wide; the body/FAQ patterns are sanitizer-leak vestiges from your own rewrites. Strip parentheticals, replace awkward framings, integrate cited facts as direct statements.

**Exception**: Where Reddit is the actual scam vector (e.g., Mykonos #5 Scorpios DM scam), keep "Reddit DM" / "DON'T TRUST ANY OFFERS YOU RECEIVE THROUGH REDDIT" as load-bearing content — only the surrounding framing should be cleaner.

---

## 6. INLINE FIX SCRIPTS

### 6.1 Full API rebuild (when sync_api warns about ≥3 stale scams)

```python
import json, re
from datetime import datetime, timezone
from pathlib import Path
from bs4 import BeautifulSoup

repo = Path("/Users/psy/repos/tabiji/.claude/worktrees/bold-bhabha-956437")
slug = "<city-slug>"  # e.g. "kyoto", "osaka", "rome"
html_path = repo / f"scams/{slug}/index.html"
api_path = repo / f"api/v1/scams/{slug}.json"

soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
api = json.loads(api_path.read_text(encoding="utf-8"))

def sev(t):
    return "high" if "high" in (t or "").lower() else ("medium" if "medium" in (t or "").lower() else "low")

new_scams = []
for card in soup.select(".scam-card"):
    title_el = card.select_one(".scam-title")
    if not title_el: continue
    name = title_el.get_text(strip=True)
    location = (card.select_one(".scam-location").get_text(strip=True) if card.select_one(".scam-location") else "").lstrip("📍").strip()
    severity = sev(card.select_one(".danger-badge").get_text() if card.select_one(".danger-badge") else "")
    tldr = card.select_one(".scam-tldr").get_text(strip=True) if card.select_one(".scam-tldr") else ""
    description = "\n\n".join(p.get_text(strip=True) for p in card.select(".scam-story-body"))
    red_flags = [li.get_text(strip=True) for li in card.select(".red-flags ul li")]
    how_to_avoid = [li.get_text(strip=True) for li in card.select(".avoid ul li")]
    base_slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    new_scams.append({
        "id": f"{slug}-{base_slug}",
        "name": name,
        "tldr": tldr,
        "severity": severity,
        "category": "tourist-trap",
        "location": location,
        "description": description,
        "redFlags": red_flags,
        "howToAvoid": how_to_avoid,
    })

api["scams"] = new_scams
api["lastUpdated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
api_path.write_text(json.dumps(api, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Rebuilt {slug}.json with {len(new_scams)} scams")
```

After rebuild, re-run `python3 /tmp/sync_api_from_html.py <slug>` to verify no warnings.

### 6.2 Curly-quote/accent drift fix

When sync warns "1 scam in API not found in HTML" with a name like "Festival d'Avignon Crowd Scams" (curly apostrophe vs. straight in HTML):

```python
import json
p = "/Users/psy/repos/tabiji/.claude/worktrees/bold-bhabha-956437/api/v1/scams/<city-slug>.json"
api = json.load(open(p))
for s in api['scams']:
    # Match by partial name to catch curly-quote drift
    if "Festival d" in s['name']:  # adjust per case
        # Replace curly apostrophe with straight
        s['name'] = s['name'].replace("'", "'").replace("'", "'")
        print(f"Fixed: {s['name']!r}")
with open(p, 'w') as f:
    json.dump(api, f, indent=2, ensure_ascii=False)
    f.write('\n')
```

For curly-accent drift (é → e or vice versa), use the same pattern:
```python
s['name'] = s['name'].replace("Mère", "Mere")  # or whatever the HTML uses
```

After the inline fix, run `python3 /tmp/sync_api_from_html.py <slug>` again to verify.

---

## 7. ARCHETYPES (the structural patterns repeat across cities)

Most scams fall into one of these archetypes. The TLDR shape stays consistent; the city-specific specifics swap in. **Don't paste; lift the framework, swap the specifics.**

### Pickpocket archetype
- Actor: teams of N people (specify the count)
- Locations: 3–5 named hot spots (transit hubs, photo spots, markets, festivals)
- Technique: distraction-and-lift, bump-and-step-off, door-close grab, child-swarm, clipboard-distraction
- Specific timings (rush hour, festival days, peak season)
- Defense: cross-body bag in front, money belt, front zipped trouser pocket, away from doors

### Taxi overcharge archetype
- Fake-quote range vs. prefecture-set / metered range
- Specific amounts to specific destinations
- Tariff / meter / route variant (Tarif A vs Tarif B in France, "broken meter," long-route padding)
- Alternative transport (named train/bus/Uber/Bolt with route + fare)

### Restaurant overcharge archetype
- Dual-menu English vs. French price gap (€3–€10/dish typical)
- Couvert / cover / seat / share supplement charges
- €6–€8 bottled water vs. legal "carafe d'eau" / "tap water"
- 15–20% pre-fill tip vs. legal "service compris"
- Named reputable alternatives (specific restaurants by name)
- 1-block-off the main square pricing drop (25–40% typical)

### Petition / clipboard archetype
- "Deaf-mute charity" or "earthquake fundraiser" framing
- Chest-height clipboard mechanic (eyes-down, blind-spot-pocket access)
- English-only diagnostic (real French petitions in French)
- €5–€20 cash donation demand
- Accomplice lift while clipboard is being read
- Defense: never take any clipboard, real charities at Monoprix / Mairie / branded bibs

### Gold ring archetype
- Fake-stamped brass ring "found" at your feet
- Two plays: finder's fee (€10–€50) OR sale at "discount" (€20–€80)
- Accomplice lift while you examine the ring
- Specific tourist locations (bridges, plazas, gardens, pedestrian streets)
- Defense: don't break stride, lost-and-found goes to Mairie / Police Municipale

### Friendship bracelet archetype
- Slip-knot construction tightens-when-you-tug
- Specific tourist locations (Sacré-Cœur, Spanish Steps, Rome Forum, Lapa)
- €10–€20 demand
- Restaurant-staff intervention defense
- Hands in front pockets / crossed-at-chest defensive move

### Fake police archetype
- Plainclothes badge-flash + counterfeit-currency-check pretext
- Tourist-accomplice variant ("can you break a 50?")
- "Tourist Police" framing diagnostic (doesn't exist in France)
- Carte professionnelle ID requirement (France)
- Commissariat insistence ("we go together")
- 17 / 112 emergency numbers

### Rental car break-in archetype
- Specific viewpoint / trailhead / beach lots
- 30–90 minute timing window
- Rental-tell signals (sticker, foreign plate, sterile interior, no floor mats, GPS marks)
- "Trunk-marking" diagnostic (the moment you open the trunk at arrival)
- Region break-in rate stat (France highest in Western Europe)
- Defense: check into hotel first + empty trunk + Plainte filing within 24 hours

### ATM skimming archetype
- Standalone vs. bank-lobby distinction
- Skimmer overlay + fake keypad + pinhole camera variants
- False-slot-jam helper variant
- DCC (Dynamic Currency Conversion) decline at Euronet/Travelex
- Transaction-alert SMS defense
- Bank-lobby ATM only during business hours

### Beach theft archetype
- 60-second swim window
- Watcher demographic identification
- Pair-team variant (distractor + grabber)
- Waterproof neck pouch + hotel safe defense
- Named beach hot spots
- Plainte filing within 24 hours

### Fake accommodation archetype
- Phantom listings at 30–50% below market
- IBAN / wire / cryptocurrency demands
- "Let's handle off-platform" diagnostic
- Cancel-and-relist variant for festival weeks
- Reverse-image-search defense (Google Lens / TinEye)
- Google Street View address verification
- Chain-hotel 6–9 month booking alternative for peak weeks

### Festival fraud archetype
- Fake "official" ticket sites (Cannes Film Festival, Festival d'Avignon, Yi Peng Lantern Festival)
- 3–5× cancel-and-relist accommodation pricing
- Bolded "official URL only" defense (festival-cannes.com, festival-avignon.com, khomloy.com)
- Named real venues + their direct sites

When you encounter a city's archetype scam, the structure is reusable. **But the specifics MUST be the city's specifics, never copy-pasted.** Each scam's "defense" must include real licensed operator names, real police hotlines, real prefecture-set rates for THAT city.

---

## 8. REFERENCE CITIES (gold-standard templates)

When in doubt about voice, tone, or specificity bar, read the most recent committed city. The pattern is consistent.

### Best examples of trap-summary TLDR + 3-beat body in original spec
- **Pompeii** (`c1986e4fed`) — 8 scams, Italian-press citations (Repubblica Napoli, Metropolis, Fanpage), specific Italian-law references (Art. 7 Codice della Strada, Art. 180 TULPS), exact prices and named operators throughout.
- **Capri** (`1179555761`) — 7 scams, exact prices (€200 La Fontelina minimum, €115 Da Luigi, €17 Co.Ta.Ca. fixed-rate, €5.50 Piazzetta cornetto), April 2026 Comune ordinance citation, real operator names.

### Best examples of substantial narrative rewrite from scratch
- **Cannes** (`4402fcfb27`) — 14 scams, $8.3M Alpes-Maritimes 2024 watch-theft stat, MYBA/ECPY yacht-broker registries, specific named scam operators.
- **Marseille** (`779f8b0359`) — 13 scams, Calanques National Park trailhead specifics, Vieux-Port restaurant tactics, named reputable bouchons (Chez Fonfon, Le Petit Nice, Chez Madie).
- **Avignon** (`229a8f223d`) — 12 scams, Festival d'Avignon force multiplier, cancel-and-relist mechanics, Mercure / Novotel / Hôtel d'Europe alternatives.

### Best examples of API rebuild + sanitizer cleanup
- **Kyoto** (`e1f5900fdb`) — 8 scams rewritten + full API rebuild (8 stale scams replaced).
- **Osaka** (`a641eee072`) — 8 scams rewritten + full API rebuild + truncated body completion + duplicate red-flag cleanup.

### Best examples of full sanitizer-leak cleanup
- **Funchal** (`b55295071c`) — 7 scams, all TLDRs rewritten or added, body sanitizer leaks cleaned across all paragraphs.
- **Faro** (`0d61714d96`) — 7 scams, similar pattern.
- **Heraklion** (`efd223b8a4`) — 7 scams, similar pattern with 2025 enforcement context preserved.

To read a reference city's commit:

```bash
git log --oneline | grep -i pompeii   # find the commit hash
git show c1986e4fed                   # see the full diff
```

---

## 9. WHAT TO DO WHEN YOU'RE NOT SURE

- **Voice / tone / specificity bar**: read the most recent committed city via `git log --oneline | head -5` then `git show <hash>`.
- **Pattern matching**: check the archetype list in section 7.
- **City-specific facts you don't know**: the user's MEMORY.md says to use SerpAPI (keychain `serpapi-key`) for Reddit/police/embassy/currency research before enriching scam pages. Use WebFetch / WebSearch for ".../scam" or "tourist trap" content for the city.
- **Dimensions you can't research**: omit them rather than fabricating. Better to leave a slot generic ("Travelers report" instead of a specific Reddit username) than to invent a "prefecture-set rate" you don't actually know.
- **Whether a TLDR meets the bar**: if you can't extract `actor + location + mechanic + cost + variant` from your TLDR in one read, rewrite it.
- **Whether a city is "already in spec"**: run the detection grep + count `<p class="scam-tldr">` matches. If TLDRs are present and trap-summary, and grep is empty, do an API resync only with a short commit message (see Pompeii / Capri commits as templates).

---

## 10. CADENCE CHECKPOINTS

- **Every city**: lint clean + sync API + sync partials + commit + drift fixes inline.
- **Every 5 cities**: push to remote (`git push`).
- **Every 10–15 cities**: open a PR with consolidated summary, wait for it to merge, rebase on main, continue.
- **Every PR**: cleanup-sweep against merged commits with the detection grep — fix any residuals in a small follow-up PR (#506 was the model).
- **Every 50 cities**: pause and tell the user where you are, what's left, and any patterns that emerged.

---

## 11. WHAT NOT TO DO (review this list every time you start a new city)

- ❌ Don't batch. **One city per commit.**
- ❌ Don't paste TLDRs from one city to another verbatim — the specifics must change.
- ❌ Don't write generic "be vigilant" defenses — the bolded defense must include real operator names, real hotlines, real protocols.
- ❌ Don't skip the lint. Don't skip the API sync. Don't skip the partials sync.
- ❌ Don't commit without the detection grep returning empty.
- ❌ Don't fake citations. If you don't have a real Le Parisien / Reddit / News anchor, write generically: "Travelers report:", "Community consensus:", "Local sources confirm:" — but never invent a specific named source.
- ❌ Don't dispatch sub-agents to parallelize. The user explicitly said no shortcuts.
- ❌ Don't work past the point of obvious context-degradation. If you find yourself tempted to skim, pause, push, and report status to the user.

---

## 12. RESUMPTION SEQUENCE (post-compact, fresh session)

When a fresh session opens:

```bash
# 1. Read this file
cat /Users/psy/repos/tabiji/.claude/worktrees/bold-bhabha-956437/SCAM_REWRITE_CONTINUATION.md

# 2. Read the queue file to find the next city
cd /Users/psy/repos/tabiji/.claude/worktrees/bold-bhabha-956437
python3 -c "
import json
data = json.load(open('scripts/queues/scam-narrative-rewrite-queue.json'))
secondary = [c for c in data['queue'] if c.get('tier') == 'book-secondary' and c.get('status') == 'pending']
remaining = sorted(secondary, key=lambda c: c.get('priority', 999))
print(f'{len(remaining)} cities remaining')
for c in remaining[:5]:
    print(f\"  P{c.get('priority', '?'):>3} {c['city']:<30} {c.get('country', ''):<14} slug={c['slug']:<25} scams={c.get('scam_count', '?')}\")
"

# 3. Read the most recent committed city for tone/voice reference
git log --oneline | head -5
git show <most-recent-hash>

# 4. Start the next city in queue with the workflow in section 4
```

---

## 13. A CLOSING NOTE

This work matters. The user has been explicit and patient: each scam is read by a real person who's about to travel to a real city, and a thin or templated TLDR misses the point of the entire project.

The bar is not "comprehensive"; it's **actionable**. A reader scanning the page should be able to:
- Identify the scam in 5 seconds (from the title + TLDR)
- Understand the cost in 10 (from the TLDR)
- Have a concrete defensive move in 20 (from the bolded defense in Beat 3)

The 26 cities done so far averaged 30–45 minutes per city for a typical case, 60+ minutes for cities full of leaks. **Don't try to go faster — the per-card audit IS the work.**

When a city's content was already in spec (Pompeii, Capri), commit just the API resync with a short note. When a city is full of leaks and drift (Faro, Funchal, Granada, Heraklion), it's a 60-minute job. Either way: the per-card audit is the work; the commit message is the proof.

Good luck. The next session inherits a real, deployed corpus that 39 cities (13 flagships + 26 book-secondary) already trust.

---

## 14. APPENDIX: TOOL PATHS AND COMMANDS

| Purpose | Command |
|---------|---------|
| Worktree root | `cd /Users/psy/repos/tabiji/.claude/worktrees/bold-bhabha-956437` |
| Branch | `claude/bold-bhabha-956437` |
| Queue file | `scripts/queues/scam-narrative-rewrite-queue.json` |
| Lint a city | `python3 scripts/lint_scam_content.py --html-city <slug>` |
| Sync API | `python3 /tmp/sync_api_from_html.py <slug>` |
| Sync partials | `bash scripts/sync-partials.sh` |
| TOC presence check | `grep -q '<div class="toc">' scams/<slug>/index.html && echo PRESENT \|\| echo MISSING` |
| Sanitizer-leak grep | `grep -nE "( is the (canonical\|named-anchor\|locals-only\|umbrella))\| (adds\|reinforces\|gives\|frames\|flags\|captures\|documents\|discusses\|explains): '" scams/<slug>/index.html` |
| British-English grep | `grep -nEi "\b(centre\|colour\|behaviour\|metres\|kilometres\|neighbourhood\|jewellery\|personalised\|programme\|favour\|honour\|labour\|recognise\|organise\|analyse\|defence\|licence\|catalogue\|cancelled\|traveller\|harbour\|summaris\|coloured\|behavioural\|memoris\|specialis\|traumatis\|finalis)\w*\b" scams/<slug>/index.html` |
| Reddit-shard grep | `grep -nE "Reddit travelers\|Reddit-sourced\|\(traveler reports 2025\)\|, per traveler reports\)\|on traveler reports for\|traveler reports warnings\|the traveler reports moderator team\|community reports across Reddit" scams/<slug>/index.html` |
| Push branch | `git push` (or `--force-with-lease` after rebase) |
| Open PR | `gh pr create --base main --head claude/bold-bhabha-956437 --title "..." --body "..."` |
| Wait for checks | `until gh pr view <num> --json statusCheckRollup --jq '.statusCheckRollup \| all(.status == "COMPLETED")' \| grep -q true; do sleep 15; done` (run with `run_in_background: true`) |
| Merge PR | `gh pr merge <num> --squash` |

`/tmp/sync_api_from_html.py` is a helper script that may need to be reconstructed from prior commits if not present after compaction. Its core logic:

```python
# Reads scams/<slug>/index.html, extracts each scam-card's name, tldr, body
# paragraphs, red_flags, how_to_avoid. Updates api/v1/scams/<slug>.json by
# matching scam name. Refreshes lastUpdated. Marks queue entry complete.
# Warns if API has scams not found in HTML (drift signal).
```

If `/tmp/sync_api_from_html.py` is missing, look at any recent commit's API change — it's a 50-line BeautifulSoup-based script that you can reconstruct in 5 minutes from the full-rebuild script in section 6.1.

---

End of handoff doc. Read it again if you start drifting from the bar.
