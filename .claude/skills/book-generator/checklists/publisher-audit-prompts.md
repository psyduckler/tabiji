# Publisher Audit Agent Prompts

Three prompts to hand to three parallel Agent invocations (general-purpose subagent) during Phase 6 of the book-generator skill. Substitute `<COUNTRY>`, `<N>`, `<CITY-COUNT>`, `<VOL-NUM>`, `<COUNTRY-CODE-ISO2>`, `<CITY-LIST>` as you go.

---

## Audit 1 — Content + Fact-Check

```
You are a master publisher/editor auditing a travel-safety book manuscript for
publication. This is AUDIT 1 of 3 for the <COUNTRY> book (Volume <VOL-NUM> of
the Tabiji Travel Safety Series). Your focus is **content accuracy and
fact-check**.

Repo: /Users/bjh/Documents/tabiji/.claude/worktrees/laughing-greider-c17f13

Files to audit:
- book-<COUNTRY>/manuscript/*.md — <N-FILES> manuscript files (front-matter, city
  intros, back-matter)
- book-<COUNTRY>/build/<COUNTRY>-scams-paperback.pdf — compiled PDF
- api/v1/scams/{<CITY-LIST>}.json — the <N> source scam entries

Verify these factual claims that appear in the manuscript:
1. Emergency numbers — police, ambulance, fire, tourist-help, consumer protection
2. Airport-to-central-city metered taxi fare ranges (verify 2026 real rates)
3. Metro/airport-express fares (verify current post-most-recent-hike)
4. Top-attraction ticket prices (national-park, museum, ancient-site entry)
5. Named tour-operator URLs (verify they resolve)
6. Embassy / consulate addresses (US, UK, Canada, Australia, Ireland main + major
   consulates)
7. Bank emergency lines (country's top 5 banks)
8. Carrier lost-SIM lines (country's major mobile carriers)
9. Volume numbering consistency across copyright, CTA, about pages
10. Country-specific conventions (Türkiye vs Turkey, Myanmar vs Burma, etc.)

Also check:
- Country-specific diacritics render correctly in the PDF (spot-check via
  `pdftotext`)
- Place-name spelling consistent (e.g., Xi'an with curly apostrophe everywhere;
  İzmir with capital dotted-I)
- No TODO / placeholder / draft markers
- No stale year-stamps ("in 2024" that will read as dated in 2027)

Report only real issues you would flag in a pre-publication review. Produce
report under 600 words with numbered findings + GO/HOLD verdict.
```

---

## Audit 2 — Typography + Layout

```
You are a master publisher/editor auditing the <COUNTRY> book (Volume <VOL-NUM>
of the Tabiji Travel Safety Series) for **typography and layout**.

Repo: /Users/bjh/Documents/tabiji/.claude/worktrees/laughing-greider-c17f13

Files:
- book-<COUNTRY>/manuscript/*.md
- book-<COUNTRY>/build/<COUNTRY>-scams-paperback.pdf
- book-<COUNTRY>/build/<COUNTRY>-scams.epub
- book-<COUNTRY>/templates/style.css

Check specifically:
1. **Em-dash vs en-dash**: em-dashes for parenthetical asides, en-dashes for
   numeric ranges. Flag misuse. Pandoc `+smart` converts `--` to em-dash but
   leaves `200-300` bare — these should be `200–300`.
2. **Curly quotes**: pandoc +smart should convert. Verify no stray straight
   quotes in rendered PDF.
3. **Country-specific currency symbol rendering**: if the country uses a
   currency symbol outside Latin-1 (Turkish ₺, Indian ₹, Bangladeshi ৳,
   Vietnamese ₫, etc.), confirm Arial Unicode MS renders it correctly. If
   missing, a build-time normalizer must be in place. Count occurrences in the
   final PDF.
4. **Diacritic rendering**: every country-specific accent (à á â ã ç è é ê ë ì
   í î ï ñ ò ó ô õ ö ù ú û ü ý, plus country-specific like ş ı ğ or ā ē ī ō ū)
   renders correctly.
5. **TOC city names** render with proper capitalization and diacritics.
6. **Running headers**: Open the PDF at late-in-book pages (around the
   appendices) — do the running headers correctly show the appendix names
   rather than the last city? The `\@schapter` LaTeX override should prevent
   bleed.
7. **Phone-number format**: `+<country-code> XXX XXX XXXX` consistent across
   the contacts appendix.
8. **Italic convention for foreign terms**: first-mention of country-specific
   terms (e.g. *denuncia*, *pàichūsuǒ*, *dolmuş*, *şikayet*, *comisaría*) in
   italic.
9. **PDF spot-check pp. 1-25 and pp. (last-25)** for layout problems: orphaned
   H2 at bottom of page, widowed headings, broken H1+figure pairs.

Keep it tight: under 600 words, numbered findings, clear GO/HOLD.
```

---

## Audit 3 — Voice + Final Sign-Off

```
You are a master publisher/editor doing a final pre-publication sign-off on the
<COUNTRY> book (Volume <VOL-NUM> of the Tabiji Travel Safety Series). Your
focus is the **master-reader voice + embarrassment check**.

Repo: /Users/bjh/Documents/tabiji/.claude/worktrees/laughing-greider-c17f13

Read 8-10 of these files:
- book-<COUNTRY>/manuscript/02-introduction.md
- book-<COUNTRY>/manuscript/03-red-flag-patterns.md
- (pick 5 city-intro files representing the reading range)
- book-<COUNTRY>/manuscript/90-appendix-phrase-card.md
- book-<COUNTRY>/manuscript/91-appendix-recovery.md
- book-<COUNTRY>/manuscript/99-cta.md

Imagine you are an American traveler, age 40-60, reading this on a flight to
<FLAGSHIP-CITY>. Flag:

1. **AI-isms** — "delve," "in today's world," "navigate the landscape,"
   "nestled," "bustling," "vibrant tapestry," textbook register.
2. **Smug or condescending** — any phrase that assumes the reader is dim.
3. **Padding / repetition** — structural tics ("radiates out in three
   corridors") that appear in every city intro. Flag if the repetition feels
   robotic; don't flag if it's a series-cohesive structural device.
4. **Cultural insensitivity** — descriptions of the country's people as a
   monolith, Orientalist language, religious-majority framing issues.
5. **Politically fraught claims** — for <COUNTRY> specifically, watch for:
   Erdoğan / Kurdish / 2016 coup (Turkey); Xinjiang / Tibet / Taiwan / dissidents
   (China); Narendra Modi / Kashmir / religious tensions (India); Prabowo /
   West Papua / separatism (Indonesia); Gaza / Netanyahu / settlements
   (Israel); etc. For a travel-safety book the default should be neutral.
6. **Date-stamp exposure** — references that will look wrong in 2027 ("in
   2025," "a new 2024 update").
7. **Suspicious numbers** — specific dollar/currency claims without a source.
8. **Unfinished** — broken cross-references, placeholders.
9. **Voice consistency** across intro, city intros, appendices.
10. **Verify counts**: back cover should say "<N> scams across <CITY-COUNT>
    <country-adjective> cities and [scenic regions / islands / etc.]."
11. **Country-name convention** applied consistently per the copyright-page
    note.

Book publishes as both Kindle and paperback. Final read-through before press.
Under 600 words, numbered findings + single GO/HOLD verdict.
```

---

## How to invoke all three in parallel

Send a single message with three Agent tool calls. They run concurrently and
typically complete within 2-3 minutes each.

```python
# Pseudocode — invoke three agents in parallel:
Agent(description="Publisher audit 1 — content",     subagent_type="general-purpose", prompt=AUDIT_1_PROMPT, run_in_background=True)
Agent(description="Publisher audit 2 — typography",  subagent_type="general-purpose", prompt=AUDIT_2_PROMPT, run_in_background=True)
Agent(description="Publisher audit 3 — voice",       subagent_type="general-purpose", prompt=AUDIT_3_PROMPT, run_in_background=True)
```

While they run, work on adjacent Phase 6/7/8 tasks (site page copy, hub update,
etc.) so you're not idle-blocking.

## When to apply findings

- **BLOCKER findings** (HOLD verdict) — apply immediately, rebuild, re-verify
- **Polish findings** (GO-with-recommendations verdict) — apply all of them
  anyway; the cost is minutes and the quality lift is meaningful

Only rebuild once after applying all fixes from all three audits. Don't
rebuild between audits.
