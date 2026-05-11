# PHASE 1 — FRAMEWORK ADAPTATION

**Volume:** *The Medical Tourism Field Guide* (Vol. 3)
**Purpose:** Document what carries from V1 and V2 unchanged, what carries with adaptation, and what is new in V3. Lock the series-continuity decisions so Phase 2 writing stays consistent.

---

## 1. WHAT CARRIES UNCHANGED FROM V1 AND V2

These elements are identical in V3 to their V1/V2 form. The writer does not re-design them.

### Voice and editorial posture (carries 100%)
- Calm, considered, buyer-protection.
- Buyer's-seat editorial voice; Bernard Huang as consumer journalist, not clinician.
- "We" (editorial plural) and "you" (reader); first-person "I" only in About-the-Editor.
- Specific over general; verify over assume; pause over urgency; framework over destination; reader's seat over expert's seat.
- No clinic, surgeon, facilitator, manufacturer, insurer, or destination endorsements.
- Sourced clinical claims with citation.
- No commercial relationships with industry actors.
- Composite scenarios are near-misses, not deaths.

### Front matter conventions
- A Note to the Reader (~700 words).
- Important Disclaimer (~800 words in V3, slightly longer than V2's 700 due to broader procedure coverage and the recommend-against chapter).
- How This Book Makes Money (~400 words). Same template; minor edit to add the cross-volume cross-references.
- The Five Rules section in front matter (~700 words).
- Scenario Index (~300 words; lists 9 composites in V3 vs. 12 in V1/V2).

### Back matter conventions
- How to Use This Back Matter intro page (~400 words).
- Worksheets numbered 1–20 in V3 (was 19 in V2 and 15 in V1).
- Glossary, alphabetized.
- Source Notes organized by source category (longer in V3 than V1/V2 because of broader source base).
- About Tabiji, About the Editor, Acknowledgments, Appendix Disclaimer.

### Production pipeline
- Markdown → preprocess.py (semantic divs) → pandoc → EPUB + HTML.
- HTML → weasyprint → paperback PDF.
- SVG → rsvg-convert → cover JPG.
- SVG → rsvg-convert → wrap PDF.
- CSS: print-style.css for paperback, epub-style.css for EPUB.
- Build pipeline copied from book-cosmetic-surgery/scripts/ at start of Phase 4.

---

## 2. WHAT CARRIES WITH ADAPTATION

These elements are recognizably from V1/V2 but adjusted for V3's scope.

### The Five Rules (adapted to general case)

V1 and V2 wrote the Five Rules with procedure-specific examples (dental quote decoder, cosmetic procedure ladder). V3 writes them at the general case so they apply to any procedure.

| Rule | V1/V2 framing | V3 framing |
|---|---|---|
| Rule 1 — Slow down | The 20-minute pause before deposit (procedure-specific examples) | The 20-minute pause and the 60-day preparation plan (general; applies to any procedure) |
| Rule 2 — Decode the quote | Procedure-specific quote anatomy | General quote anatomy; the cost-component checklist that scales across all procedures |
| Rule 3 — Verify the provider | Dentist or surgeon credential verification | General specialist credential verification across all medical specialties; the country-specific register search pattern |
| Rule 4 — Protect the deposit | Procedure-specific deposit norms | General deposit framework; the 15-question readiness test scales across all procedures |
| Rule 5 — Document everything | Procedure-specific records (X-rays, photos, implant cards) | General records framework; the 22-item universal records inventory |

### The Seven Leverage Points (adapted)

V1 and V2 enumerated 7 leverage points along the procedure-decision journey. V3 keeps the same 7 but adapts the language and the journey-stage examples.

| LP | V1/V2 | V3 |
|---|---|---|
| LP1 | Before the search | Before the search — applies to all medical tourism |
| LP2 | The funnel | The funnel — coordinator/facilitator funnel patterns are procedure-agnostic |
| LP3 | The destination decision | The destination decision — general framework |
| LP4 | The quote | The quote — general quote decoder |
| LP5 | The deposit | The deposit — general deposit framework |
| LP6 | Travel and the in-person exam | Travel and the in-person exam — general |
| LP7 | The procedure room (chair, OR, table) | The procedure room — universal day-of leverage |

### The Procedure Complexity Ladder

V1 wrote a 5-step ladder for dental. V2 wrote a 5-step ladder for cosmetic surgery and hair restoration. V3 writes the **general 5-step ladder** that applies to any procedure category. Procedure surveys in Part V are organized around this ladder.

| Step | General description | Example procedures |
|---|---|---|
| Step 1 | Low-surprise visits (consultations, diagnostic, single-area minor) | Executive physical, LASIK consult, single tooth extraction |
| Step 2 | Outpatient single-procedure cases | LASIK, dental crown, cataract surgery, single-area dermatology |
| Step 3 | Outpatient multi-procedure / combined cases | Mommy makeover, dental rehabilitation, hair restoration |
| Step 4 | Inpatient surgical procedures with implants or general anesthesia | Joint replacement, breast augmentation, bariatric surgery |
| Step 5 | Major combination procedures, transplants, complex inpatient | CABG, valve replacement, complex oncology surgery, transplant |

The leverage question at each step (general):
- **Step 1:** What records will I receive from this visit independent of whether I book a procedure?
- **Step 2:** If the plan changes after in-person exam, will you pause and give me the revised options without losing my deposit?
- **Step 3:** Why is this combination right for my anatomy and goals, and would staging across two trips be lower risk?
- **Step 4:** Surgeon name, anesthesia provider name, facility accreditation, implant specification — all in writing before deposit.
- **Step 5:** Why is a fully accredited tertiary hospital not the right setting? What is the transfer protocol if a complication requires ICU-level care?

### Composite scenario structure

V1/V2 had 12 composites each. V3 has 9. The reduction is because V3 has more system/framework content and procedure surveys, but each composite gets MORE narrative weight (scene-level detail, multiple appearances).

V1/V2 composite arc structure:
- Introduction (often Ch 1 or early Part I).
- Reappearance for full development at a framework chapter.
- Implicit conclusion or named conclusion at end of book.

V3 composite arc structure (same shape, fewer characters, more time-per-character):
- Each composite has 1–3 scene appearances rather than 1 introduction + 1 development.
- Marcus has 3 appearances (Ch 1, Ch 11, Ch 31) to anchor cost-crisis as the primary segment.
- Composites are written as **scenes** (present tense, dialogue, specific detail) — not as summaries.

### Worksheets

V1 had 15 worksheets. V2 had 19. V3 has 20.

Of the 20:
- **12 are adapted from V1/V2** (carry the same purpose, generalized for cross-procedure application).
- **8 are new for V3** (specifically: Is Medical Tourism Right for Me, Accreditation Verification, Cross-Border Insurance, Multi-Procedure Sequencing, Procedure Complexity Self-Rating, Family Decision, Diaspora-Specific, Cross-Border Claim).

Worksheet inline-callback format identical to V1/V2: *"A reusable copy is Worksheet X in the back matter."*

### Pull quotes

V1 had 5 designated pull quotes. V2 had 25 pull quotes (more weaved into chapters). V3 plans 6–8 pull quotes, chosen during Phase 2 writing from the candidate list in research notes §9.

### Decision Gate device

V1 and V2 used **Decision Gate** boxes — short, declarative paragraphs at the end of decision-relevant sections, formatted distinctly (CSS class `.decision-gate-inline` or `.decision-gate`). V3 carries this device unchanged. Estimated 12–18 decision gates throughout V3.

### Closing Decision Gate (per-Part)

V1 and V2 used Part-closing Decision Gates as transitions between Parts. V3 carries this for Parts III, V, and VI (where they map most naturally).

---

## 3. WHAT IS NEW IN V3

These elements do not appear in V1 or V2.

### "Bernard's Notes" feature

Seven short editorial inserts (300–500 words each) at key inflection points where the editor's voice breaks through systematically.

| # | Location | Theme |
|---|---|---|
| 1 | After Ch 1 | Why this book is different |
| 2 | After Ch 6 | The facilitator industry — personal observation |
| 3 | After Ch 11 | The 60-day plan — what "prepared" actually looks like |
| 4 | After Ch 16 | Specialist credentialing — the credential alone doesn't protect you |
| 5 | After Ch 25 (cosmetic survey) | Why V2 was written, what this book inherits |
| 6 | After Ch 30 (recommend-against) | Why the chapter exists, why the editorial position is held |
| 7 | After Final Note | Closing editorial voice on year-5 success |

**Typographic distinction:** CSS class `.bernard-note` — italic block, set off with a horizontal rule, with a labeled header ("A note from the editor").

**Voice in Bernard's Notes:**
- More personal than chapter text.
- Uses "I" (the editor) and "you" (the reader).
- Short (300–500 words).
- Closes with a single declarative sentence the reader can carry.

### "Reading Paths" page

Six paths through the book based on reader situation. ~500 words in the front matter. Comes after Scenario Index, before Introduction. The page is intentionally simple: each path lists 8–14 chapter numbers in order.

### Telemedicine Second-Opinion content (Ch 15)

Net-new chapter. ~1,400 words. Covers Cleveland Clinic Connect, Mayo Clinic Connect, MD Anderson, MSK International, Mass General Brigham International, Johns Hopkins International. The chapter is structured as a buyer's-seat introduction to a meaningful US-based option many readers don't know about.

### Diaspora content (Ch 17 + Worksheet 19)

The diaspora reader segment receives dedicated treatment. Ch 17 contains a ~400-word section specifically on the diaspora frame. Worksheet 19 is a 1.5-page diaspora-specific decision framework. Composite B (Priya) has two full scenes in Chs 16 and 17.

### Year-5 outcomes thread

Ch 38 + Composite I (closing) + Final Note all extend buyer-protection past the procedure week. The framework extends from "what to do before the procedure" to "what success looks like at year 5."

### Edition framing convention

"First Edition — Data current as of 2026" appears on the title page, in the Important Disclaimer, and in the About-the-Editor section.

### Restructured procedure surveys

V2 had a single "patterns we recommend against" chapter (Ch 28) at the end. V3 keeps the same chapter but threads the editorial position throughout:
- Front matter disclaimer mentions the editorial position.
- Ch 1 alludes to the existence of patterns the book recommends against.
- Procedure-survey chapters cross-reference the relevant entry in the recommend-against chapter.
- Ch 30 (recommend-against) is the culmination, not the surprise.

### "What this book solves" reader-segment mapping

Each chapter explicitly maps to which reader segments it primarily serves. Phase 2 writer uses this map to ensure each chapter has a clear primary audience and doesn't try to serve everyone equally.

---

## 4. COMPOSITE SCENARIO CAST — V3

Nine composites. Each is named, with profile, narrative arc, and chapter placements.

| Letter | Name | Age | Profile | Reader segment | Chapter appearances |
|---|---|---:|---|---|---|
| A | Marcus | 58 | Project manager, Denver, bilateral knee replacement, cost-crisis | Cost-crisis | Ch 1, Ch 11, Ch 31 |
| B | Priya | 47 | Software engineer, US-Indian, mother's cardiac procedure | Diaspora | Ch 16, Ch 17 |
| C | Eleanor | 64 | Retired, chronic-condition portfolio (knees, cataracts, dental, hernia) | Chronic-condition portfolio | Ch 21, Ch 35 |
| D | Daniel | 42 | Marketing director, researching for father (cataract, Mexico) | Adult-child researcher | Ch 23, Ch 36 |
| E | Karen | 51 | School administrator, mother's cancer diagnosis | Exploratory | Ch 29 |
| F | Marcus (revisited) | 58 | (same as A) — framework-works closing | Cost-crisis | Ch 31 |
| G | Daniel (revisited) | 42 | (same as D) — companion role at father's procedure | Adult-child | Ch 36 |
| H | Eleanor (revisited) | 64 | (same as C) — multi-procedure year-1 follow-up | Portfolio | Ch 35 |
| I | Maria | 52 | Closing positive, bariatric surgery, year-5 outcome | Closing scenario | Closing chapter |

### Composite voice rules

Each composite scene:
- Present tense.
- Specific named details (kitchen, time of day, what's on the table).
- One or two pieces of dialogue.
- A specific framework element the scene illustrates.
- Resolution: the patient is alive and the situation manageable.

### Why nine, not twelve

V1/V2 had 12 composites because each procedure category needed its own narrative anchor. V3 has more system/framework content and fewer procedure-specific chapters, so fewer composites per chapter ratio. The reader meets each composite more often (some have 3 scenes) so the narrative weight per composite is higher.

---

## 5. EDITORIAL POSITION CONTINUITY

V2 established the editorial-position chapter (V2 Ch 28). V3 expands and threads the position.

### Carried from V2 (unchanged)
- Surgery in non-accredited facilities.
- Unverifiable surgeon credentials.
- Unverifiable anesthesia provider credentials.
- BBL with intramuscular fat injection in non-accredited facilities.
- Surgery in the 12 months after major adverse life events.

### Expanded for V3
- Transplant tourism in documented organ-trafficking corridors.
- Stem-cell, regenerative, exosome, peptide, longevity tourism (broader than V2's brief cosmetic-context mention).
- Unapproved alternative cancer therapies abroad.

### Threading
- Front matter disclaimer.
- Ch 1 hook references the existence of such patterns.
- Procedure-survey chapters reference the relevant editorial-position entry.
- Ch 30 (the chapter) is the full treatment.
- Bernard's Note #6 closes the chapter.

### Legal review
- Malpractice attorney reviews Ch 30 specifically before publication.
- Each entry is per-claim sourced.
- Standalone-appendix fallback path is preserved.

---

## 6. VOICE CONTINUITY RULES (FOR PHASE 2 WRITING)

These are the voice checks Phase 2 must pass. They are written into every chapter draft.

### The five voice commandments
1. **Specific over general.** Name the source. Name the body. Give the figure.
2. **Verify over assume.** Every clinical claim has a citation.
3. **Pause over urgency.** The book never rushes the reader.
4. **Framework over destination.** Never recommend a country or clinic.
5. **Reader's seat over expert's seat.** Every chapter from the consumer's vantage.

### Sentence-level discipline
- Long sentences are okay when the structure carries the meaning. Strings of qualifiers are not.
- "We" (editorial plural) and "you" (reader) are the default pronouns.
- "I" appears only in About-the-Editor, in scripted patient sentences within composite scenes, and in Bernard's Notes.
- Active voice over passive when both work.

### What to never do
- Recommend a country.
- Recommend a clinic.
- Recommend a facilitator.
- Recommend an implant brand by name as superior (mention is okay, endorsement is not).
- Use medical-advice tone ("you should take X mg of Y").
- Use alarmist or paternalistic tone.
- Use destination-essentialist framing.

### What to always do
- Source clinical claims.
- Provide the framework the reader can apply.
- Pause when the decision is being rushed.
- Carry the editorial position from V2 forward with consistency.

---

## 7. WHERE TO FIND MORE DETAIL

- For **specific source citations:** see PHASE1-RESEARCH-NOTES.md.
- For **chapter-by-chapter outline:** see PHASE1-OUTLINE.md.
- For **commercial and execution strategy:** see PLAN.md and BRIEF.md.

---

## 8. BOTTOM LINE

The framework adaptation for V3 is conservative on continuity (most elements carry from V1/V2) and disciplined on expansion (new features are limited to where they materially improve the book: Bernard's Notes, Reading Paths, the telemedicine chapter, the diaspora content, the year-5 outcomes thread, the edition framing).

The reader who finished V1 or V2 will recognize V3 as a Tabiji book. The reader new to the series will not feel they need the previous volumes to understand this one.

That balance — series-continuity without dependence — is the operational definition of "foundation book."
