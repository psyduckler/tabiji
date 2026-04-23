# Scam Pages Style Guide

**Canonical style reference for every page under `/scams/<city>/` and `/scams/country/<cc>/`.** Applies to the prose that ships in `scams/research/<cc>_batch*.json`, to the `SAFETY_TIPS` / `FAQS` / country-hub entries in `scams/generate_pages.py`, and to any manual HTML touch-ups in `scams/<city>/index.html`.

The scam-page corpus feeds the paperback KDP books under `book-<country>/` — the house style must match. All 10 shipped book `config.yaml` files declare `language: en-US`; the scam pages must author in the same register.

---

## 1. Default English variant — **American English**

**Use American spellings everywhere.** The house variant for all tabiji.ai editorial prose — scam pages, country hubs, safety tips, FAQs, book manuscripts — is **American English (en-US)**.

- `traveler` / `travelers` — not *traveller* / *travellers*
- `favor` / `favorite` — not *favour* / *favourite*
- `color` / `colors` / `colored` — not *colour* / *coloured*
- `center` / `centered` — not *centre* / *centred*
- `neighbor` / `neighborhood` — not *neighbour* / *neighbourhood*
- `organize` / `organized` / `organization` — not *organise* / *organised* / *organisation*
- `authorize` / `recognize` / `analyze` / `realize` / `emphasize` / `apologize` / `summarize` — `-ize` not `-ise`
- `theater` — not *theatre*
- `jewelry` — not *jewellery*
- `defense` — not *defence*
- `license` as both noun and verb (AmE has no *licence* noun/verb split)
- `aluminum` — not *aluminium*
- `behavior` — not *behaviour*
- `program` — not *programme* (exception: UK-institution proper nouns like "BBC Programme Archive")

### Never-touch cases (preserve verbatim)

- **Reddit thread titles** quoted in single quotes: reproduce the original casing and spelling, including any British English ("`r/Brazil 'How organised is the Amazon tour mafia?'`"). These are citations.
- **Proper nouns** with language-specific spellings: `São Paulo`, `Brasília`, `Búzios`, `Foz do Iguaçu`, `Zürich`, `München`, `Málaga`.
- **Institutions + brands**: `Metropolitan Centre for Tropical Medicine`, `Programme National`, `Tripadvisor` (lowercase "a" is correct per 2020 rebrand), `WhatsApp` (camelCase), `Airbnb` (lowercase "b").
- **Place names** that happen to use British spellings: `Theatre District` in New York, `Centre Pompidou` in Paris, etc.
- **Legal / regulatory citations**: `Lei 13.419/2017`, `IBAMA`, `DEATUR`, `IPHAN`, `FUNAI`, `ICMBio`, `PROCON`, `INMETRO`, `IBGM`, `AMAZONASTUR`, `Disque 100`. These are named institutions — keep as-is regardless of variant.

### What changed

The Brazil/Portugal/UK scam batches written 2026-04-18 through 2026-04-20 drifted into British English ("older travellers", "favour", "organised"). The 2026-04-21 Brazil framing edit (PR #337) and a prior Brazil copyedit pass (PR #326) corrected substantial portions. **Going forward, every new scam page, every rewrite, and every copyedit pass defaults to American English unless the content is explicitly a quoted citation or a proper noun.**

---

## 2. Voice + tone

### Audience
Adult travelers planning an international trip. Broad age band — do **not** gate content with "for older travelers" or "for seniors" framing. Write for everyone.

### Voice register
- Direct, specific, authoritative, calm.
- **Not** alarmist. Name the scam, explain the mechanic, give the defensive play, move on.
- **Not** breezy-influencer. No exclamation marks, no "OMG", no "pro tip" interjections.
- **Not** legalese. Don't quote statutes unless relevant; cite by short name ("Lei 13.419/2017 makes service charge OPTIONAL") and move on.

### Second person vs. third person
Use **second person** ("you") when giving defensive advice. Use **third person** ("the tourist", "visitors") when describing the scam mechanic abstractly.

> ✅ *"The tourist is handed a 'free' ribbon, then asked for R\$ 50 'donation'. Refuse firmly — say 'não obrigado' and walk on."*

### ALL-CAPS emphasis
Use sparingly for true emphasis — typically imperatives: `REFUSE`, `AVOID`, `NEVER`, `VERIFY`, `IGNORE`, `CONFIRM`. Budget ~8–12 per scam story maximum; more reads shouty. Do not ALL-CAPS proper nouns or ordinary adjectives.

### Em-dashes
Use em-dashes (`—`, U+2014) with spaces around them for parenthetical pauses. AP-style no-space `word—word` is acceptable but inconsistent with the existing corpus; keep the space-wrapped style.

---

## 3. Currency + numbers

- **Always prefix the currency symbol with a space before the number**: `R$ 50`, `€ 30`, `£ 20`, `$ 100`, `¥ 1,000`, `AR$ 35,000`, `USD 500`.
- Exception: quoted Reddit titles or proper-noun business names may drop the space if that's how the source wrote it.
- **Use en-dash `–` (U+2013)** for price ranges: `R$ 50–R$ 100`, not `R$ 50-R$ 100` (hyphen) and not `R$ 50 - R$ 100` (spaces).
- Repeat the currency symbol on both sides of a range: `R$ 50–R$ 100`, not `R$ 50–100`.
- Thousand separator: comma in US English. `R$ 1,500`, `$ 10,000`, `2,500 km`.
- Decimal separator: period. `2.5 hours`, `R$ 99.50`. (Portuguese-language prose quoted in citations may use comma — leave as-is.)

### Named local-currency usage
Don't translate local currency into USD unless the scam mechanic specifically involves USD quoting:
- ✅ *"A private speedboat quote of R\$ 800 is standard-scam-tier; the official catamarã is R\$ 130–R\$ 220."*
- ❌ *"A private speedboat quote of \$160 is standard-scam-tier..."* (loses the local specificity, confuses on-ground verification)

---

## 4. Page structure (mandated)

Each scam card must contain, in this order:

1. **`<div class="scam-header">`** — number, title, danger badge
2. **`<div class="scam-location">`** — location string with `📍` prefix
3. **`<img class="scam-comic">`** — per-scam comic illustration (see `docs/comic-pipeline/README.md`)
4. **`<p class="scam-tldr">`** — one-sentence summary opening the story
5. **4–6 × `<p class="scam-story-body">`** — the scam story, split into short paragraphs
6. **5 × red-flag chip** — short, parallel, starts with a noun or present-participle
7. **5 × how-to-avoid chip** — short, parallel, starts with an imperative verb
8. **5 × Reddit source link** — canonical 2025/2026 Reddit thread citations

### Paragraph sizing — readability + book-print mandate

**Every scam story must split into 4–6 paragraphs, 40–110 words each (target 60–90), 2–5 sentences each.** Monolithic 150+ word prose blocks are rejected: they're unscannable on the web and unreadable when packaged into the paperback KDP books under `book-<country>/`.

In the research JSON `story` field, separate paragraphs with `\n\n`. The generator's `_render_paragraphs` (in `scams/generate_pages.py`) splits on that separator and emits one `<p class="scam-story-body">` per paragraph.

### Narrative structure across paragraphs

The scam story still covers three beats — **context**, **mechanic**, **defense** — but now distributed across 4–6 paragraphs so no single one becomes a wall:

- **Para 1 (context)** — Name the scam locale; community baseline. ~60–80 words.
- **Para 2 (the hook)** — How the approach begins; the first 30 seconds of the encounter. ~60–90 words.
- **Para 3 (variants + evidence)** — Enumerate 2–3 variants with concrete local-currency prices and named locations; cite the 2025/2026 anchor qualitatively. ~60–90 words.
- **Para 4 (defense, steps 1–2)** — First two numbered actionable steps. ~50–80 words.
- **Para 5 (defense, steps 3 + emergency contacts)** — Final step plus dialable phones: tourist police, national emergency, consumer-protection hotline, relevant embassy. ~60–100 words.
- **Optional Para 6** — Only if a single scam needs an additional nuance (e.g., a regulatory citation, a specific recovery path). ~50–80 words.

---

## 5. Regulatory citations + institutions

Cite regulatory names in their **original language** with an English gloss on first mention:

- *"Lei 13.419/2017 (Brazilian consumer-protection law) makes the 10% service charge optional."*
- *"IBAMA (Brazil's environmental protection agency) banned pink-dolphin contact tourism in 2025."*
- *"INMETRO (Brazilian metrology institute) certifies all commercial kg-buffet scales."*
- *"IBGM (Instituto Brasileiro de Gemas e Metais Nobres) is the gemstone certification authority."*

Tourist police (country-specific): DEATUR (Brazil), Politur (Dominican Republic), Policía Turística (Spain, Mexico), Jandarma (Turkey). Always include the dialable phone on final defense step.

---

## 6. Reddit citations

- Include **5 Reddit thread citations per scam** in the `reddit_sources` array.
- Each citation format: `r/<subreddit> '<title>' (comments/<id>, <year>)`.
- Prefer **2025/2026 anchors**. One or two older citations (2023/2024) are fine as "community baseline" context.
- Name one as `CANONICAL` when it's the single defining community thread.
- Reddit IDs are 6–8 character lowercase alphanumeric — verify shape: `comments/1qru2oj`, not `comments/1qru2ox_wrong`.
- Thread titles: reproduce verbatim, including British spellings, abbreviations, and casing.

---

## 7. Comic illustrations

Each scam card carries one 2×2 comic panel at `scams/<city>/scam-<N>.jpg` on R2 (`img.tabiji.ai/...`). See `docs/comic-pipeline/README.md` + `docs/comic-pipeline/styles/<country>.md` for per-country style blocks.

Injection pattern (always directly below `scam-location`):

```html
<img class="scam-comic"
     src="https://img.tabiji.ai/scams/<city>/scam-<N>.jpg?v=1"
     alt="<scam title> — comic illustration"
     loading="lazy"
     style="width:100%;height:auto;border-radius:12px;margin:1rem 0 1.25rem;display:block;">
```

Bump `?v=<N>` whenever you overwrite the R2 file (CDN cache-bust).

---

## 8. Accessibility + internationalization

- `<html lang="en-US">` — default for every scam page. Only override for explicit non-English content (none currently in scope).
- All `<img>` tags require meaningful `alt`. For scam comics, use the scam title + "— comic illustration".
- Use `loading="lazy"` on all below-the-fold images.

---

## 9. Quick checklist for every new page

Before committing a new city scam page:

- [ ] American English throughout prose (not Reddit citations)
- [ ] No "older travelers" framing — just "travelers" or "you"
- [ ] Currency: `R$ 50` (space), `R$ 50–R$ 100` (en-dash, repeated symbol)
- [ ] 6 scams × 5 FAQs per city page
- [ ] Each scam = 4–6 paragraph story (40–110 words/para, target 60–90), 5 red flags, 5 how-to-avoid, 5 Reddit sources
- [ ] No `story` paragraph exceeds 120 words (lint reject)
- [ ] At least 80% of Reddit citations from 2025/2026
- [ ] Regulatory citations (Lei, IBAMA, DEATUR, PROCON, etc.) kept in original language
- [ ] Proper nouns preserve diacritics (São Paulo, Brasília)
- [ ] Comic img tag injected below `scam-location` with matching alt
- [ ] `<html lang="en-US">`
- [ ] Emergency contacts on final step of every defense paragraph

---

## 10. Linter / audit helpers

Ad-hoc audit scripts under `/tmp/<country>/copyedit_pass*_*.py` from prior passes can be reused:

- **Pass 1 mechanical** — flags American/British mix, double spaces, malformed currency
- **Pass 2 factual** — phones, Reddit IDs, regulatory citations, year consistency
- **Pass 3 editorial** — list parallelism, voice consistency, ALL-CAPS budget, redundancy

When sweeping an existing country to align with this guide, run all three. A typical clean country audit returns 0–5 mechanical hits and 0 factual/editorial issues.
