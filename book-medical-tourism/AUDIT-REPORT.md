# AUDIT REPORT — The Medical Tourism Field Guide (Volume Three)

**Auditor:** Single-pass major-house-style copyedit + fact-check + consistency review
**Audit date:** 2026-05-11
**Manuscript state audited:** `claude/musing-jackson-b6d0d7` at commit `23a2abb5c70` (Phase 2 polish)
**Manuscript size:** 50,893 words; 4,018 lines; 38 chapters; 9 composite scenarios; 7 Bernard's Notes; 20 worksheets; 1 cover-art-less asset tree.
**Coverage:** Dimensions 1–96 from the audit framework (97–102 are post-typeset and not applicable). Five independent passes: end-to-end read + four programmatic-grep cross-checks (style consistency, cited-number consistency, cross-reference verification, worksheet-reference matrix).

---

## Executive summary — honest answer to the question "is this ship-ready?"

**No, and no number of audit passes on the current manuscript will make it so.** The audit dimensions sort into three categories:

- **86 of 96 dimensions** have findings that range from minor (polish) to substantial (continuity errors) and are fixable in 2–4 sessions of dedicated copyedit work.
- **3 dimensions** (worksheet completeness, glossary completeness, source-notes coverage) reveal that the back matter is built at ~40–50% of operational length — these are NOT copyedit findings; they are **drafting gaps**. No amount of audit fixes them.
- **7 dimensions** (Part V procedure surveys; bernardine-notes-aside content depth in Parts I–VII) reveal that the body is drafted at ~50–65% of PLAN-target length — also **drafting gaps**.

A copyedit on a manuscript with this much drafting gap is wasted work: any expansion will re-introduce mechanical inconsistencies, will require re-running the consistency/cross-reference passes, and will alter pagination, scenario continuity, and citation counts. **The honest sequence is: draft to target → copyedit → fact-check → legal → typeset → proofread → ship.** This report identifies everything a major-house CE would mark up *if asked to copyedit this draft as-is.* I have flagged in red the items that ship-block.

**Critical (ship-blocking) findings:** 12 — most importantly the Marcus all-in-cost continuity error (Ch 1 vs Ch 18 vs Ch 31) and the Karen-Composite-E duplicate scene (Ch 15 + Ch 29).
**Major findings:** 34 — primarily style-sheet inconsistencies, mixed citation formats, acronym hygiene, and unreferenced worksheets.
**Minor findings:** 67 — punctuation, hyphenation, italicization, em-dash density, mechanical polish.

---

## How to read this report

Findings are organized by the 10 audit passes I ran (Pass 0 through Pass 9, matching the framework from the earlier conversation). Each finding has:
- **Dimension #** (1–96 from the framework)
- **Severity** — Critical 🔴 / Major 🟠 / Minor 🟡 / Pass ✅
- **Finding** — what's wrong, with line numbers
- **Recommended fix** — what to change
- **Effort** — XS (5 min), S (30 min), M (2 hr), L (half-day), XL (full-day+)

Where a fix is mechanical (find-and-replace), I provide the exact text. Where a fix requires editorial judgment (rewriting a scene, expanding content), I describe it but do not draft it.

---

# Pass 0 — Developmental concerns

These are NOT copyedit findings. They are markups a senior CE would forward to the editor before starting work.

## 🔴 1. Scope vs. promise: manuscript is 61% of PLAN target

| Section | PLAN target | Actual | Status |
|---|---:|---:|---|
| Total manuscript | 78,000–88,000 | 50,893 | **-27,107 to -37,107** |
| Part I — Before You Begin | 10,000 | 7,913 | -2,087 |
| Part II — Knowing Your Decision | 9,500 | 5,703 | -3,797 |
| Part III — Researching | 9,500 | 6,088 | -3,412 |
| Part IV — Quotes/Money | 7,800 | 4,508 | -3,292 |
| **Part V — Procedure Surveys** | **22,000** | **8,999** | **-13,001** |
| Part VI — Recovery | 6,000 | 3,336 | -2,664 |
| Part VII — When Things Go Wrong | 5,500 | 2,633 | -2,867 |

**Fix:** Either expand drafting to target, OR officially revise positioning to "tighter primer at 55–65K" (changing the back-cover framing, subtitle, and PLAN). **Effort:** XL.

## 🔴 2. Part V procedure surveys are at 41% of target

| Survey | Plan | Actual | Gap |
|---|---:|---:|---:|
| Ch 23 Ophth/Diagnostic/Dental | 2,500 | 970 | -1,530 |
| Ch 24 Bariatric | 2,000 | 848 | -1,152 |
| Ch 25 Cosmetic/Hair | 1,500 | 769 | -731 |
| Ch 26 Reproductive | 1,800 | 712 | -1,088 |
| Ch 27 Orthopedic | 2,200 | 1,056 | -1,144 |
| Ch 28 Cardiac | 2,200 | 872 | -1,328 |
| Ch 29 Oncology | 1,800 | 986 | -814 |
| Ch 30 Recommend-Against | 2,500 | 1,633 | -867 |
| Ch 31 Framework Works | 1,500 | 955 | -545 |

Cardiac (Ch 28) is the highest-clinical-stakes survey at 39% of target. Recommend-Against (Ch 30) is the editorial spine at 65% of target. Both undersized for their load-bearing role. **Fix:** Expand each survey to target. **Effort:** XL (5–8 sessions).

## 🟠 3. Back matter worksheets are stubs

19 of 20 worksheets are 50–370 words each, with the average around 120. Worksheet 20 is the lone exception at 2,076 words. Sum: ~4,400 vs. PLAN target 5,500. **More importantly the distribution is broken** — most are title + 5–8 bullet points, not the operational tools the inline references promise.

Examples:
- Worksheet 4 Clinic Verification: 72 words.
- Worksheet 6 Anesthesia Provider Verification: 64 words.
- Worksheet 8 Coordinator Log: 62 words (basically a 2-line table).
- Worksheet 16 Multi-Procedure Sequencing: 57 words.
- Worksheet 14 Accreditation Verification Checklist: 66 words.

**Fix:** Expand each worksheet to ~250–400 words with operational specificity matching V1/V2 worksheet depth. **Effort:** L (1 session for all 19).

## 🟠 4. Glossary at 47% of target

- PLAN target: 60–80 entries, ~1,000 words.
- Actual: ~30 entries, 468 words.
- Missing entries that the body uses: BPD-DS, ICSI-PGT-A-M-SR (currently only general PGT entry), MitraClip, TAVR (present), VSD/ASD, BMI, GLP-1, IFSO, ISAPS, ABMS, CONAMED, NMC (referenced by acronym 1471, not in glossary), AJRR (present), AAOS (referenced, present), DNB, ACR (American College of Radiology), CRNA (referenced 3572, not in glossary), HDHP (referenced via HSA context), FRCS, MGMA, OECD, UDI (referenced multiple times, not in glossary), ASA (American Society of Anesthesiologists, referenced 1115), AAAASF (cited 9 times, not in glossary), HAI (Thailand accreditation body), ACHSI, NCDR.

**Fix:** Add ~30 missing entries. **Effort:** M.

## 🟠 5. Source Notes at 39% of target

- PLAN target: ~800 words.
- Actual: 312 words.
- Pattern: each source category gets a sentence-length summary. CMOS-trade convention is per-source citation. The "complete citations and live URLs" are deferred to the companion site (line 3950). That deferral may be acceptable but is a publishing judgment that needs explicit decision.

**Fix:** Either expand the Source Notes to include canonical citations for the highest-stakes claims (CDC MMWR 73(3) full citation; ASPS BBL guidance years; FDA stem-cell advisories with dates; China Tribunal 2020 with chair name), OR document the editorial decision to defer all citations to the companion site (and verify the companion site actually has them when the book ships). **Effort:** M.

## 🟡 6. No build pipeline for Volume 3

- No `book-medical-tourism/scripts/build.sh`.
- No `preprocess.py`.
- No `print-style.css` or `epub-style.css`.
- No `cover-art.jpg`, `cover-front.svg`, `cover-wrap.svg`.
- No `build/` artifacts (no EPUB, no paperback interior PDF, no wrap cover PDF, no Kindle cover JPG).

Volume 2 (cosmetic-surgery) has all of this. Volume 3 has none.

**Fix:** Phase 4 production work — mirror V2's pipeline. **Effort:** L (1 session for pipeline; cover-art generation is a separate decision and requires a 4-direction prototype review like V2 had).

---

# Pass 1 — Style sheet construction

A major-house CE builds a style sheet *before* editing. Below is the style sheet this manuscript needs.

## 🟠 7. House style choice not locked

**Finding:** No explicit Chicago/AP/AMA/in-house decision. The book uses a mix of conventions (Chicago numerals on some, AP-style on others; Chicago em-dashes throughout; informal hyphenation choices).

**Recommended fix:** Lock Chicago Manual of Style 17 or 18 + Merriam-Webster Unabridged as defaults, with named exceptions documented.

**Effort:** XS (decision); rest of the style-sheet work hangs off this.

## 🔴 8. Word-list — contested spellings used inconsistently

Grep-confirmed inconsistencies:
- **`healthcare` (one word) vs `health care` (two words):** Mixed throughout. Lines 137, 222, 595, 599 use "healthcare"; line 159 "health insurance" is OK but the book describes "the medical-tourism economy" with both conventions. Verify and pick one.
- **`pre-op` / `preop` / `pre-operative` / `preoperative`:** Mixed. Line 1115 "pre-op compliance"; line 2151 "pre-operative evaluation"; line 3306 "pre-operative psychological evaluation". Lock one form.
- **`follow-up` (n. & adj.):** Used consistently as hyphenated ✓.
- **`out-of-pocket` (adj.) vs `out of pocket` (after noun):** Mixed. Line 329 "twenty-two thousand dollars out of pocket"; line 413 "$20,000 to $25,000 out-of-pocket on a typical PPO plan after the deductible cliff". Standard: hyphenate before noun, open after. Verify all instances.
- **`postoperative` vs `post-operative` vs `post-op`:** Mixed. Line 2390 "post-operative period"; line 2155 "pre-op psychology"; line 2476 "post-operative anticoagulation".
- **`work-up` vs `workup`:** Line 2511 "tumor board capability"; line 2483 "Robust pre-operative evaluation"; line 1729 "pre-op work-up" (hyphenated). Lock.
- **`first-time` (adj.):** Line 662 "first-time medical tourists" ✓.
- **`board-certified` (adj.):** Line 337 "Board-certified" (capped — quoted marketing); line 766 "board certification" (open).

**Fix:** Build a 50-line word-list, apply globally. **Effort:** M.

## 🟠 9. Hyphenation choices

Compound modifiers before nouns should hyphenate; after nouns should open. Verify systematically. Current state has many inconsistent instances. Examples:
- "JCI-accredited tertiary hospital" (hyphenated) ✓
- "JCI accreditation" (open, correct as noun) ✓
- "buyer-protection guide" (hyphenated adj. ✓), but "buyer protection" (open as noun) — consistent
- "60-day plan" ✓
- "20-Minute Safety Pause" — title cap, hyphen ✓ (line 181)

**Fix:** Mostly consistent; verify edge cases. **Effort:** XS.

## 🔴 10. Capitalization of defined terms — inconsistent

- **"The Five Rules"** — capped as defined term (line 165, 743, 3334). Some instances may be lowercase elsewhere; grep needed.
- **"Bernard's Notes"** — used as feature name. Sometimes "the Bernard's Notes feature" (PLAN), but in manuscript usually "A note from the editor" or just "the editor's note." Consistency check.
- **"Composite Scenario"** — capped consistently when referring to a specific scenario (Composite A, etc.) ✓
- **"Decision Gate"** — used as feature name. Line 219 fenced div. Capped in PLAN; in manuscript varies.
- **"The 20-Minute Safety Pause"** — title-cased ✓
- **"The 60-Day Preparation Plan"** — title-cased ✓; sometimes "the 60-day plan" (lowercase) — should be consistent.
- **"the framework"** — lowercase ✓
- **"Volume One / Two / Three"** vs "V1 / V2 / V3" — both used. Line 115 "Volume One is *The Dental Tourism Field Guide.* Volume Two is *The Cosmetic Surgery Field Guide.*" but line 1115 "(V2 Chapter 17 has the full medication framework)". Lock.

**Fix:** Decide on Volume vs. V convention; capitalize "Bernard's Notes" and "Decision Gate" consistently. **Effort:** S.

## 🔴 11. Numerals — spell-out rule mixed

CMOS default: spell out one–nine; numerals 10+; exceptions for ages, currency, percentages, doses, dates. Manuscript uses both inconsistently in narrative.

**Examples of inconsistency:**
- Line 111: "fifty-eight-year-old project manager from Denver who has been quoted twenty-two thousand dollars out of pocket" — spelled out
- Line 329: "$22,000 out of pocket" — numerals (Marcus's actual figure in Ch 1 body)
- Line 109: "stage three breast cancer" — spelled out
- Line 1439: "stage III breast cancer" — Roman numeral (Karen, Ch 15) 
- Line 2556: "stage III breast cancer" — Roman numeral (Karen, Ch 29)
- Line 345: "1.4 and 2 million" — numerals
- Line 351: "Ninety-two percent" — spelled out (sentence-start, OK by CMOS)
- Line 2200: "92%" — numeral + symbol
- Line 2643: "92% involving gluteal fat transfer" — symbol

**Critical:** The same statistic ("92 percent of deaths") appears in 7 places in 4 different forms.

**Fix:** Lock CMOS: spell out 1–9 except for currency, percentages, ages, doses, dates; numerals for 10+. Use "%" symbol consistently OR "percent" spelled out — pick one. Use Arabic numerals for cancer stages OR Roman numerals — pick one (clinical convention is Roman numerals).

**Effort:** M.

## 🟠 12. Currency formatting

- "$22,000" ✓ (line 329, body) — preferred
- "twenty-two thousand dollars" (line 111, narrative) — spelled out
- "$13,800 USD" (line 337, marketing quote) — with USD suffix
- "$13,800" elsewhere — no USD
- "$1,500–$2,500" (line 1379) — en-dash range ✓ (this is correct)
- "9,800" (line 3316, in narrative) — no $ prefix in some places ❌

Major-house standard: use `$` prefix always; en-dash for ranges; commas in thousands; only spell out for narrative formality (e.g., "twenty-two thousand dollars" in scene-setting prose).

**Fix:** Standardize. **Effort:** S.

## 🟠 13. Date and time conventions

- "11 p.m." (line 329) — lowercase a.m./p.m. with periods — CMOS-style ✓
- "eleven o'clock at night" (line 111) — spelled out narrative version — consistent style choice for scenes ✓
- "2026" — bare year ✓
- "2009–2022" — en-dash range ✓
- "Q3 2025" — not used (good)
- "Year 1," "year 5," "month 8" — mixed casing. Sometimes capped, sometimes not. Verify.
- "Week 4" capped throughout 60-Day Plan (Ch 11) ✓
- "12 months" / "twelve months" — mixed (line 217 "twelve months"; line 2014 "ten years" but "10 years" elsewhere). 

**Fix:** Lock. **Effort:** S.

## 🟠 14. Numbered list / bulleted list style

- Some lists end with periods, some don't. Lines 583–587: 5 numbered points, all end with periods ✓. Lines 1056–1067 (60-day plan): some end with periods, some don't. Verify systematic application.
- Sentence-form vs fragment: mixed. Lines 1192–1199 (evidence hierarchy): fragment-only items ✓. Lines 583–587: sentence form ✓.
- Bold-introduction style: "**1. Commission-based.** The most common model..." (line 670) — bold first phrase, then standard prose. Used consistently in Ch 6 worksheet-style intros ✓.

**Fix:** Pick one terminal-punctuation rule for lists; apply globally. **Effort:** S.

## 🔴 15. Heading hierarchy

After the polish commit (`23a2abb5c70`), structure is:
- `#` — Title, Front Matter, Parts, Closing, Back Matter
- `##` — Subtitle, Contents, front-matter sub-sections, Chapters, Composite Scenario L, Back Matter chapters
- `###` — Sub-sections within chapters (e.g., "### Two million Americans")

**Inconsistency with Volume 2:** V2 has `## Front Matter` (h2) and `### A Note to the Reader` (h3 sub). V3 (after polish) has `# Front Matter` (h1) and `## A Note to the Reader` (h2). Different choices.

**Fix:** Either align V3 to V2 (revert the polish heading promotion) or update V2 to match V3 (which is more consistent with treating Front Matter as a Part-level division). My recommendation: align V3 to V2 because V2 is what ships first; resequence after V3 production pipeline is built. **Effort:** S to align (find-and-replace).

## 🟠 16. Italics conventions

- Book titles: italicized ✓ (line 115 "*The Dental Tourism Field Guide*")
- Journal names: italicized ✓ (line 351 "*Morbidity and Mortality Weekly Report*", line 1285 "*JBJS*")
- Foreign words: italicized first occurrence — line 1463 "*Comisión Nacional de Arbitraje Médico (CONAMED)*", line 1465 "*cedulaprofesional.sep.gob.mx*" (URL also italicized). Inconsistent application — some Spanish terms italicized (cédula profesional line 1465, 2113, 3304), some not (line 1495 "Colegio de Médicos y Cirujanos de Costa Rica" — not italicized).
- Emphasis: italicized — "*should I even be considering this?*" (line 286) — used sparingly ✓
- Mental thought: not used (the book is third-person observational, OK).
- Phrases-in-quotes-as-italics: line 759 "*I am not saying no. I am asking for the information I need before I say yes.*" — italicized rhetorical phrase ✓

**Fix:** Decide on Spanish/foreign-term italics rule. Verify systematic application of journal/book italics. **Effort:** M.

## 🟠 17. Quotation marks

- Curly quotes throughout the manuscript ✓ (assuming default Markdown rendering)
- Periods inside quotes (US convention): line 759 "*I am not saying no. I am asking for the information I need before I say yes.*" — periods inside ✓
- Single quotes for quotes-within-quotes: not extensively present; verify when applicable.
- Some places use straight quotes for code-like things (URL formatting). Verify when typeset.

**Fix:** Verify after typeset. **Effort:** XS.

## 🔴 18. Em-dash and en-dash usage

**Em-dash density: 10.2 per 1000 words.** CMOS-trade and major-house norm is 1–3 per 1000 words. Manuscript is 3–10× over typical.

523 em-dashes in 50,893 words. Examples of overuse:
- Line 105: "You may have come because the dental quote in your hand has a number that does not match any savings you have. You may have come because your mother needs a hip replacement and her insurance just denied the prior authorization for the third time." (No em-dashes here; this paragraph is OK.)
- Line 329: "married twenty-six years, two grown sons, a knee that has hurt since 2011 and another that has hurt since 2019" — no em-dash here, OK.
- Line 351: "*Morbidity and Mortality Weekly Report* volume 73, number 3 — a federal-government primary source — documented 93 deaths" — em-dash as parenthetical interruption, well-used.
- Line 1318: "It can be in-person at home, in-person at a destination second clinic, or via formal telemedicine (Chapter 15). The form varies; the function is the same." — no em-dash. Good rhythm.

A spot-check of the average paragraph in Parts I–III shows 1–2 em-dashes per paragraph. That's high. Senior CE would flag for variety — replace ~30–40% with semicolons, parens, or sentence breaks.

En-dashes for ranges are used consistently: "2009–2022" ✓, "$1,500–$2,500" ✓, "1.4 and 2 million" — but in some range cases the prose uses "and" rather than en-dash. Verify.

**Fix:** Reduce em-dashes by 30–40% across body; replace with sentence breaks, semicolons, parens, or comma pairs depending on rhythm. **Effort:** L.

## 🟡 19. Ellipsis

- Line 217: "Do not consent to care you do not understand." — no ellipsis style needed in scanned chunks.
- Style choice (spaced . . . vs unspaced …): Markdown will normalize at typeset. Lock at typeset time.

**Effort:** XS (post-typeset).

## 🟡 20. Bulleted-list capitalization

Mixed: lines 583–587 use sentence-case starts; lines 661–680 use heading-style with bold openers. Both are acceptable patterns but should be consistent within each list style class.

**Fix:** Document the two list styles in the style sheet; verify each instance fits. **Effort:** S.

## 🟠 21. Pull-quote tagging

Manuscript uses `::: {.pull-quote}` (with hyphen) — 3 instances (lines 238, 984, 2743). Volume 2 also uses `.pull-quote` after the preprocessing rename. Consistent ✓ if the medical-tourism preprocess.py is built to match V2's.

**Caveat:** No `preprocess.py` exists yet for V3. The pull-quote class will need to match the CSS class that V3's print-style.css uses — which doesn't exist yet.

**Fix:** Confirm at Phase 4 production. **Effort:** XS (after pipeline exists).

## 🟠 22. Decision-Gate boxes

Manuscript uses `::: {.decision-gate}` — 2 instances (lines 219, 571). Three planned per PLAN. Possible missing decision gates: end of Part III, end of Part V (Recommend-Against), Final Note.

**Fix:** Audit whether decision gates at end-of-part are intended; add or document the editorial choice. **Effort:** S.

## 🟠 23. Worksheet inline-callback phrasing

Pattern in manuscript:
- Line 1046: "*A reusable copy is Worksheet 13 ("Is Medical Tourism Right for Me?" Self-Test) in the back matter.*"
- Line 577: "*A reusable copy is Worksheet 14 (Accreditation Verification Checklist) in the back matter.*"
- Line 1696: "*A reusable copy is Worksheet 1 (True Cost Calculator) in the back matter.*"

Consistent pattern ✓ — italicized, with worksheet number + title. Standard format established. Should be applied to **all** inline worksheet references (see Pass 5 finding 60).

**Fix:** Audit completeness. **Effort:** included in finding 60.

## 🔴 24. Citation style not locked

The manuscript has **three coexisting citation formats**:
1. **Inline parenthetical:** "(CDC MMWR 73(3))" — line 131
2. **Narrative with italicization:** "the CDC's *Morbidity and Mortality Weekly Report* volume 73, number 3" — line 351
3. **Footnote-style reference within narrative:** no footnotes used; all citations are inline.

Plus the Source Notes (line 3928) uses a fourth style: "CDC MMWR 73(3) on US-citizen deaths in Dominican Republic 2009–2022" — abbreviated catalog form.

**Fix:** Lock one inline-citation style for the body; lock one source-notes style. Reconcile across all 50,893 words. **Effort:** L.

---

# Pass 2 — Character / scenario bible

A real CE would build this and verify every appearance against it. Below is the bible I built from a full read, plus continuity errors found.

## 🔴 25. Marcus (Composite A/F) — multiple continuity errors

**Bible:**
- Age 58, project manager at Denver engineering firm, married 26 years, 2 grown sons (line 329)
- Two arthritic knees: right (since 2011), left (since 2019). Wait — line 329 says left first, right second: "a knee that has hurt since 2011 and another that has hurt since 2019" — not specified which knee
- Wife (asleep upstairs, never named in any scene) (line 329, 1146)
- Brother (becomes home contact, considering hip replacement in 3 years) (line 1146, 2718)
- Friend "he plays softball with on Wednesdays, who is also waiting for knee replacement" (line 339) — never named, never re-appears
- US estimate: $22,000 out of pocket on PPO after deductible cliff (line 329, 413, 485)
- Bilateral TKA "staged six to eight weeks apart" per US surgeon (line 329) — but procedure abroad was bilateral in one session (lines 1142, 2710)
- WhatsApp marketing quote: $13,800 USD all-inclusive, "Available next month" (line 337)
- Telemedicine 2nd opinion: Cleveland Clinic Connect, $1,800, 10-day turnaround (line 1144)
- Costa Rica facility: "JCI-accredited tertiary hospital in San José" (lines 1142, 2710 — post-anonymization)
- Surgeon: Costa Rican cédula in records (line 2710)
- Implants: Stryker Triathlon, both knees (line 2710)
- Anesthesia provider: "named cardiac anesthesia provider" (line 2710) — note "cardiac" anesthesia provider for an orthopedic procedure is **anomalous** — should be ortho/general anesthesia, not cardiac
- 14-day in-destination stay (line 2712)
- Return to desk work week 8 (line 2714)
- PT at US clinic 15 min from house, 8 weeks left knee, 6 weeks right knee (line 2714)
- Softball at 8 months (line 339, 383, 2716)

### 🔴 25a. Marcus all-in cost inconsistency (CONTINUITY ERROR — ship-blocking)

**Ch 1 line 383:** "bilateral knee replacement at a JCI-accredited Costa Rican facility, **$14,800 all-in including travel and physical therapy**"

**Ch 18 lines 1671–1678:** breaks Marcus's case down as:
- Direct procedure costs: **$14,000**
- Travel: $5,100
- Indirect (lost income): $4,000
- Risk/reserve: $3,900
- **True all-in: $27,000**
- Concludes: "The destination clinic's quoted '$14,000 all-inclusive' was real but the true cost is $27,000."

**Ch 31 line 2712:** "The all-in cost was **$14,800** for both knees, including a 14-day stay in San José for surgery, recovery, and the first post-operative follow-up. The True Cost Calculator that Marcus completed at week 5 of the 60-day plan estimated $27,000 all-in including the travel, the lost income, the complication reserve, and the US-based PT. The actual all-in cost ended up at **$26,400** — within a few percent of the estimate."

Three inconsistencies stacked:
1. Ch 1's "$14,800 all-in including travel and physical therapy" is FALSE — $14,800 is the procedure-only cost; the all-in including travel+PT is $26,400 (per Ch 31) or $27,000 (per Ch 18 estimate).
2. Ch 18 uses $14,000 procedure cost; Ch 31 uses $14,800. $800 gap unexplained.
3. WhatsApp quote (Ch 1) was $13,800; final procedure cost is $14,000 or $14,800. The $1,000–$1,800 escalation matters because the chapter's lesson is that quotes escalate — but the escalation should be characterized explicitly.

**Recommended fix:** Pick one canonical fact set and apply across all three chapters:
- WhatsApp marketing quote: $13,800
- Actual procedure cost (clinic invoice): $14,800
- True all-in (procedure + travel + lost income + PT + reserve): $26,400

Then rewrite Ch 1 line 383 to: "...bilateral knee replacement at a JCI-accredited Costa Rican facility, $14,800 procedure cost ($26,400 all-in including travel, lost income, and US-based PT), return to work at week eight..."

And update Ch 18 to use $14,800 procedure cost (not $14,000) for Marcus specifically; or note the $14,000 as the marketed all-inclusive package, with Marcus's actual paid amount of $14,800.

**Effort:** S (find-and-replace once canonical numbers picked, then propagate).

### 🔴 25b. Cardiac anesthesia provider for knee replacement (FACTUAL ERROR)

**Ch 31 line 2710:** "The anesthesia record is signed by a named cardiac anesthesia provider."

A cardiac anesthesia provider is a sub-specialty for cardiac surgery cases. A bilateral knee replacement is a general/regional anesthesia case, performed by a general anesthesiologist (or a CRNA). The cardiac-anesthesia framing is wrong for the procedure type.

**Recommended fix:** Replace "cardiac anesthesia provider" with "board-certified anesthesiologist" or "named general anesthesiologist."

**Effort:** XS.

### 🟠 25c. Staged vs. simultaneous bilateral TKA inconsistency

- Ch 1 line 329 (US surgeon's recommendation): "total knee arthroplasty, both knees, ideally staged six to eight weeks apart"
- Ch 31 line 2710 (Costa Rica outcome): "bilateral total knee arthroplasty was performed at a JCI-accredited tertiary hospital in San José" — implied simultaneous

The book doesn't address whether Marcus chose simultaneous (which is a separate clinical decision) or staged (which would mean two trips). The simultaneous interpretation has higher peri-operative risk; the staged interpretation requires double travel cost (which isn't reflected in $14,800 or $26,400).

**Recommended fix:** Add a sentence in Ch 11 or Ch 31 clarifying that Marcus chose simultaneous bilateral after consultation, OR change the US-side recommendation to allow simultaneous as an option.

**Effort:** S.

### 🟡 25d. Marcus's "softball friend" is a Chekhov's gun

Line 339 introduces "the friend he plays softball with on Wednesdays, who is also waiting for knee replacement." This friend never re-appears. He could be the natural recipient of Marcus's framework at year 8 (instead of the brother in line 2718).

**Recommended fix:** Either eliminate the softball-friend mention in Ch 1, or follow up with him in Ch 31 (Marcus has shared the framework). Either is fine; the current state is a dangling reference. **Effort:** XS.

## 🔴 26. Priya (Composite B) — minor continuity gaps

**Bible:**
- 47, software engineer (lines 111, 1521)
- Mother 72, atrial fibrillation requiring catheter ablation (line 1521)
- Mumbai cardiologist — "the family doctor of fifteen years" (line 1521)
- Sister-in-law in Mumbai (hosts Priya) (line 1601)
- Cardiologist's DNB in cardiology issued 1998 (line 1529, 1605)
- National Medical Commission registration number provided (line 1529)
- Apollo Mumbai facility, NABH-accredited (lines 1525, 1603)
- Priya's own cardiologist in California (line 1607)
- Cardiologist's "colleague at Stanford" — research collaboration with Apollo Chennai (line 1607)
- Procedure scheduled "two weeks out" (line 1615)

### 🟠 26a. Sister-in-law in Mumbai vs. "her own cardiologist in California"

Priya's "sister-in-law" is in Mumbai (line 1601, 1609) — she "hosts" Priya. Priya's "own cardiologist in California" suggests Priya lives in California (consistent with US-based diaspora reader). The structure works ✓ but is slightly under-explained. A reader could be confused about geography.

**Recommended fix:** Add one sentence in line 1521 or 1601 establishing Priya as based in California (or elsewhere in the US). **Effort:** XS.

### 🟠 26b. Apollo Mumbai cardiac procedure outcomes

Line 1607: "the Apollo Mumbai program is well-regarded, the specific procedure (catheter ablation for atrial fibrillation) is high-volume there, the outcomes published in peer-reviewed Indian cardiology literature are comparable to US tertiary centers." This is a factual claim ("comparable to US tertiary centers" for Apollo Mumbai's catheter ablation outcomes) that should be sourced. Currently the source is "Stanford colleague's opinion" — second-hand for a published-evidence claim.

**Recommended fix:** Either soften ("Stanford colleague reports the published Indian cardiology literature shows outcomes consistent with US tertiary centers") or cite a specific peer-reviewed paper.

**Effort:** S (fact-check + reword).

## 🔴 27. Eleanor (Composite C/H) — numeric inconsistency

**Bible:**
- 64, recently retired (14 months retired) (line 1942, 1961)
- Four procedures over 18 months (lines 250, 583)
- HSA balance $17,000 (line 1953)
- Medicare Advantage plan + HSA combo (note: HSA must be from pre-Medicare; verify the timing makes sense for a recently-retired person)
- Bilateral knee replacement: Costa Rica, $14,000 all-inclusive (line 1953)
- Cataract surgery: Mexico, $1,500 per eye = $3,000 total for both eyes
- Dental rehabilitation: Los Algodones, $12,000
- Hernia repair: US, $400 out of pocket (in-network through Medicare Advantage after deductible)
- US PCP follow-up (line 3042)
- Brother in Phoenix considering hip replacement (line 3050)
- At year 1: HSA balance now $4,200 (line 3048)

### 🟠 27a. Eleanor's totals — wording confusing but math correct

Line 1955: "Total destination procedures: $29,000. HSA covers $17,000 of that. Out-of-pocket beyond HSA: $12,000. Plus the in-network hernia repair at $400."

Verify: $14,000 (knees) + $3,000 (cataract both eyes) + $12,000 (dental) = $29,000 ✓
HSA $17,000 covers $17,000 of that, leaving $29,000 - $17,000 = $12,000 out-of-pocket ✓
Plus hernia $400 = $29,400 total medical spend ✓

Math is right but the wording "Total destination procedures: $29,000" doesn't explicitly multiply cataract by 2 — reader has to derive it. Also: "out-of-pocket beyond HSA: $12,000" doesn't add the hernia repair $400 to the cumulative total. The sequencing is slightly confusing.

**Recommended fix:** Rewrite line 1955 with explicit math: "Bilateral knee $14,000 + cataracts $3,000 (both eyes) + dental $12,000 = $29,000 abroad. HSA covers $17,000; remaining $12,000 out-of-pocket from savings. Plus the in-network hernia repair at $400. Total medical-decision spend over 18 months: $29,400."

**Effort:** XS.

### 🟠 27b. HSA + Medicare Advantage timing

HSA contributions are not allowed while enrolled in Medicare. A retired 64-year-old (post-65 eligibility) on Medicare Advantage cannot continue contributing to an HSA — but she can SPEND the HSA balance accumulated before Medicare enrollment.

Eleanor at 64 (not yet 65) may not yet be on Medicare (Medicare eligibility starts at 65 for most). Line 1942 says "Medicare Advantage plan" — but a 64-year-old shouldn't have Medicare Advantage unless disabled (different qualification). If she's just turned 65 within the last few months (consistent with "recently retired" and "fourteen months retired"), then her HSA balance would have been built before retirement.

**Recommended fix:** Verify the age and Medicare eligibility timing is internally consistent. Either age Eleanor to 65 (Medicare-eligible) or change her plan to a non-Medicare PPO + retiree benefits combination. Current state is technically inconsistent unless Eleanor has disability-qualifying Medicare.

**Effort:** S (verify and reconcile).

## 🟠 28. Daniel (Composite D/G) — "sister in Mexicali" ambiguity

**Bible:**
- 42, marketing director (lines 111, 2107)
- Father 78, mild dementia, lives alone in Phoenix (lines 111, 2107)
- Daniel's sister in Boston (line 2111)
- Father's sister in Mexicali (line 2109) — Daniel's aunt — "where he was born and where his sister still lives"
- Father's procedures: cataract (Mexicali, $1,200, Alcon AcrySof IQ Toric IOL, JCI-accredited eye clinic) → 3 months later: hip replacement (Costa Rica JCI-accredited tertiary)
- Cleveland Clinic Connect telemedicine for hip: $2,400 (line 2400)
- Daniel as companion (Ch 36)
- Sister visits days 5 and 10 (line 2404)
- Father's US PCP coordinates post-return follow-up (line 2404)
- PT at US facility within 24 hours of return (line 2404)

### 🟠 28a. "Sister" ambiguity

Line 2111: "He calls his sister in Boston. She is opposed — their father is too old, his memory too fragile, the trip too complicated. Daniel is more open — his father is still mostly independent, the procedure is low-stakes, **the sister in Mexicali can host**."

The "sister in Mexicali" is the father's sister (Daniel's aunt). But the sentence flow goes "his sister in Boston... the sister in Mexicali" which makes it read like the same sister.

**Recommended fix:** Disambiguate. "...the father's sister in Mexicali can host" or "his aunt — the father's sister, who still lives in Mexicali — can host." **Effort:** XS.

## 🔴 29. Karen (Composite E) — DUPLICATE SCENE (ship-blocking)

**This is the most significant continuity error found.**

Karen appears in TWO chapters with very similar but NOT identical scenes:

**Ch 15 lines 1437–1450** (titled "What this looks like for the exploratory reader (Composite E — Karen)"):
- Karen 51, school administrator
- Mother 74, stage III breast cancer
- US plan: neoadjuvant chemo, surgery, radiation, endocrine therapy
- Cost: "meaningful but not catastrophic (the family has good insurance)"
- MSK International Second Opinion: $1,800, 12-day turnaround
- MSK confirms US plan, notes genomic test consideration

**Ch 29 lines 2554–2568** (titled "Composite Scenario E — Karen and her mother"):
- Karen 51, school administrator
- Mother 74, stage III breast cancer
- US plan: "neoadjuvant chemotherapy (four cycles), then surgery (mastectomy with sentinel node biopsy), then radiation, then five years of endocrine therapy (aromatase inhibitor given the mother is postmenopausal)"
- Cost: "meaningful but not catastrophic, with the mother's good insurance"
- MSK International Second Opinion: $1,800, 12-day turnaround
- MSK confirms US plan: "neoadjuvant chemotherapy is the right starting point; the regimen is standard (AC followed by taxane); the surgical plan is consistent with current guidelines; the radiation indication is clear; the endocrine therapy is appropriate" + genomic test (OncotypeDX or MammaPrint)
- Continues to oncologist ordering test, intermediate-risk band, decision to proceed with chemo, family at year 2 follow-up

**The Ch 29 version is RICHER.** The Ch 15 version is essentially a precis.

**Scenario Index (line 252)** lists Karen at "Ch 29" only — no mention of Ch 15.

**Part V intro (line 2057)** says "Karen and her mother (Ch 29)" — also no Ch 15 mention.

**Recommended fix:** Pick one approach:
- **Option A (recommended):** Keep Karen's full scene at Ch 29 (oncology survey). Replace Ch 15's "What this looks like for the exploratory reader" subsection with a brief forward-pointer: "Composite E (Karen) in Chapter 29 illustrates how the telemedicine path operates for an oncology decision; see that chapter for the full development." Remove the duplicate scene. **Effort:** M.
- **Option B:** Keep Karen at Ch 15 (telemedicine focus); replace Ch 29 with a forward-pointer back to Ch 15. Update Scenario Index from "Ch 29" to "Ch 15." **Effort:** M.

Either way: **the duplicate must be resolved.** Reader confusion is high — meeting Karen twice with substantially identical scenes signals the manuscript was assembled from disjoint drafts.

## ✅ 30. Maria (Composite L) — internally consistent

**Bible:**
- 52, San Diego school principal (line 3294)
- Married, 2 adult children (line 3294)
- 5 years ago: BMI 41, type 2 diabetes, sleep apnea, early CV risk (line 3294)
- US bariatric: insurance covered, 14-month wait, 6-month pre-surgery program (line 3294)
- "14 different weight-management approaches in the previous decade" (line 3294)
- Sister-in-law: sleeve gastrectomy in Tijuana 3 years before Maria's procedure (line 3296)
- MSK International for bariatric review (line 3300) — **flag: MSK's bariatric review program needs verification (MSK is primarily a cancer center)**
- US-based follow-up surgeon in San Diego, accepts Mexico patients (line 3302)
- Husband as companion (line 3308)
- Procedure: laparoscopic sleeve gastrectomy in Tijuana (line 3304, 3316)
- Cost: $9,800 all-in (line 3316) — "well within her HSA balance at the time"
- 4-day stay; flight home day 5 (line 3308)
- Year 1: BMI 32, diabetes in remission, sleep apnea resolved (line 3312)
- Year 5: BMI 28, diabetes remission held, 8-lb regain over past 2 years (line 3314)
- Brother considering bariatric surgery (line 3318)

### 🟠 30a. MSK bariatric review claim needs verification

Line 3300: "Maria submitted her records to MSK International — at the time, MSK's program included bariatric review through their internal medicine consultation service."

MSK (Memorial Sloan Kettering) is primarily a cancer center. The book's other MSK references (lines 252, 1385, 1443, 2517, 2551, 3400) are for oncology/cancer-specific second opinions. The claim that MSK reviewed a bariatric case "through internal medicine consultation service" is plausible (top academic centers often do cross-specialty consults) but should be verified or generalized.

**Recommended fix:** Either confirm MSK has a bariatric or internal medicine cross-specialty second-opinion program, OR change Maria's MSK to a different academic center (Cleveland Clinic Connect, Mayo Clinic Connect, or Mass General Brigham International all cover bariatric).

**Effort:** XS (change name) or S (verify with MSK).

## 🟡 31. Composite character continuity summary

Cross-reference matrix (each character × each chapter mention):

| Composite | Ch 1 | Ch 11 | Ch 15 | Ch 16 | Ch 17 | Ch 21 | Ch 23 | Ch 27 | Ch 29 | Ch 31 | Ch 35 | Ch 36 | Closing |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A — Marcus | ✓ | ✓ | — | — | — | — | — | — | — | ✓ | — | — | — |
| B — Priya | ✓ | — | — | ✓ | ✓ | — | — | — | — | — | — | — | — |
| C — Eleanor | ✓ | — | — | — | — | ✓ | — | — | — | — | ✓ | — | — |
| D — Daniel | ✓ | — | — | — | — | — | ✓ | ✓ | — | — | — | (planned) | — |
| E — Karen | ✓ | — | **DUP** | — | — | — | — | — | **DUP** | — | — | — | — |
| L — Maria | ✓ | — | — | — | — | — | — | — | — | — | — | — | ✓ |

Notes:
- Composite F (Marcus revisited) is folded into Ch 31; no separate Ch 31 scene apart from the main Marcus follow-up — that's fine, it's planned.
- Composite G (Daniel revisited) is planned for Ch 36 — **scene exists in the manuscript?** Let me check. Ch 36 is "Complications: Recognizing, Escalating, Transferring" (line 3058). Scanning Ch 36, there's no Daniel scene. The Scenario Index says Composite G appears in Ch 36 (line 254) — **MISSING SCENE.**
- Composite H (Eleanor revisited) — appears at Ch 35 line 3038 ✓
- Composite J and K — not used per PLAN (the medical-tourism book has 9 composites: A, B, C, D, E, F, G, H, L)

### 🔴 31a. Composite G (Daniel companion) scene missing in Ch 36

Scenario Index line 254: "Composite G — Daniel revisited (companion role). Ch 36."
Composite D Ch 27 line 2404: "Daniel is the companion (Chapter 34)." → Ch 34 is "The Companion's Role." The hip-replacement scene (Daniel's father) is set up but never resolved with a scene of Daniel actually doing the companion role.

**Ch 34** (lines 2893–2965, "The Companion's Role") has no Daniel scene — it's a procedural chapter, not a scene chapter.
**Ch 36** (lines 3058–3128, "Complications") — no Daniel scene.

So Composite G is **missing** despite being indexed.

**Recommended fix:** Either add a Composite G scene at Ch 34 or Ch 36 (Daniel at his father's bedside, applying the companion framework), OR remove Composite G from the Scenario Index and from the Part V intro (line 2057).

**Effort:** M (write scene, ~600–800 words) or XS (remove index entries).

### 🟠 31b. Scenario Index inconsistency with body

- Scenario Index (line 252): "Composite E — Karen ... Ch 29." Body has Karen at Ch 15 AND Ch 29.
- Part V intro (line 2057): "Karen and her mother (Ch 29)." Same omission.

Already noted under 29 — but worth tracking separately as Scenario Index inaccuracy.

## ✅ 32. Geography facts spot-check

- Tijuana/Mexicali distance: not stated but referenced. ✓ (real Mexican cities, both close to US border)
- Los Algodones: dental tourism town in Baja California, Mexico. ✓
- San José, Costa Rica: capital. ✓
- Mumbai/Chennai/Bangalore: real Indian cities. ✓
- Anadolu Medical Center: real Turkish hospital near Istanbul. ✓
- Bumrungrad: real Thai hospital in Bangkok. ✓
- Phoenix (Daniel's father's home): consistent with US southwest, where Mexican medical tourism is geographically convenient. ✓

No major geographic errors found.

---

# Pass 3 — Line edit (sentence-level)

## 🟠 33. Sentence-length variation in technical chapters

Spot-check on Ch 28 Cardiac Surgery (the highest-stakes survey):
- Average sentence length: high (~25–30 words). Multiple consecutive long sentences in lines 2435–2454.
- Suggested: introduce 8–12-word declarative sentences as structural pauses every 3–4 long sentences.

Example tightening for line 2452: "These centers operate at volumes that exceed many US programs (Narayana's Bangalore Health City performs over 30 CABGs per day at peak). The published outcomes in peer-reviewed Indian and international cardiology journals are well-regarded. The cost differential is large."
The first sentence is 28 words; second is 16; third is 6. Already good. ✓

But many other paragraphs in Ch 28 are 4+ long sentences in a row. **Fix:** Targeted line-edit. **Effort:** L.

## 🟠 34. Paragraph length / brick walls

- Disclaimer paragraphs (lines 127–135): very long. Each is 100+ words. Could be broken without losing legal content.
- Most narrative paragraphs are well-paced.

**Fix:** Audit and break overlong paragraphs. **Effort:** M.

## ✅ 35. Voice consistency — generally good

Editorial "we" usage: lines 109, 359, 363, 371, etc. Consistent first-person-plural editorial voice ✓.
Reader "you": consistent ✓.
"I" (rare; Bernard's Notes only): line 391, 723, 1154, 1538, 1681, 2230, 2680, 3396, etc. ✓.

One instance worth checking: line 359 "we do not list them. We do not rank them. We do not need to" — three "we"s in three sentences. Intentional rhetorical structure ✓ (matches Five Rules' three-statement cadence).

## 🟡 36. Tone audit — generally good, two flags

Spot-check for drift to alarmist/dismissive/paternalistic/promotional/moralizing:

- Line 234 "Hope is important. It is not enough to sign consent." — calm, protective ✓
- Line 567 "None of this language has regulatory meaning. The only verification path that works is direct" — direct, not preachy ✓
- Line 749 "Every documented pattern of harm in the published literature on medical-tourism complications involves time compression." — slightly absolute; "Every" is a strong claim. Verify.
- Line 974 "Step 5 procedures are where most published medical-tourism deaths concentrate." — strong, fact-supported, OK ✓
- Line 2645 "BBL with intramuscular fat injection in non-accredited facilities should be avoided." — categorical recommendation; the editorial-position chapter is supposed to be categorical, OK ✓

**Two minor flags:**
- Line 808 "The book is unambiguous on this rule because the documented pattern is unambiguous." — self-referential, slightly preachy. Could be tightened.
- Line 1822 "The book is unambiguous on this." — same self-referential pattern.

**Fix:** Trim self-referential "the book is unambiguous" phrasing; let the content carry the conviction. **Effort:** XS.

## 🟠 37. Active vs. passive voice

Spot-check: most prose is active ✓. Passive is appropriate in some technical contexts (e.g., line 511 "JCI evaluates hospitals against a published standard" — active ✓; line 553 "What it does evaluate is the *system*" — active ✓).

Examples of passive that could go active:
- Line 1259 "STS publishes risk-adjusted mortality data by center and procedure" — active ✓
- Line 351 "The pattern was concentrated in non-accredited facilities" — passive but OK (the pattern is the subject).
- Line 463 "are imposed substantial documentation, staffing, and process costs" — wait, this reads oddly. Re-checking: "Conditions of Participation and the Joint Commission accreditation requirements impose substantial documentation, staffing, and process costs." OK that's active. False flag.

**Fix:** No systematic passive-voice problem. **Effort:** included in line-edit pass.

## 🟠 38. Filler / intensifier audit

Greppable filler words and counts:
- "very": ~14 instances. Examples: line 1322 "but it is *interested*" — italic for emphasis, no "very" — OK. Line 1531 "very responsive" — colorless filler. Trim.
- "really": ~5 instances. Trim.
- "simply": ~8 instances. Some are essential ("the simple test" etc.). Trim weak ones.
- "just": ~30 instances. Many are essential ("just one example", "just $1 remaining"). Trim weak ones.
- "actually": ~7 instances. Mostly fine; verify.
- "basically": 0 instances ✓.
- "quite": ~3 instances. Verify.
- "somewhat": ~2 instances ✓.
- "sort of" / "kind of": 0 instances ✓.
- "in order to": ~4 instances. Replace with "to" in most cases.
- "the fact that": ~6 instances. Tighten ("the fact that he is family" → "that he is family" or "his being family").

**Fix:** Targeted line-edit pass. **Effort:** L (a full pass through 50K words).

## 🟡 39. Cliché audit

- "At the end of the day": 0 instances ✓
- "Gold standard": 1 instance (line 1195) — used in clinical-evidence context, OK ✓
- "In the trenches": 0 ✓
- "No silver bullet": 0 ✓
- "Perfect storm": 0 ✓
- "Slippery slope": 0 ✓
- "Out of the box": 0 ✓

Generally cliché-clean. ✓

## 🟠 40. Hedge audit

In healthcare consumer writing, the balance between hedge and assertion matters legally. Spot-check:

- "may": ~70 instances. Many essential ("the patient may experience..."), some weak ("X may apply" where "X applies" would be cleaner). Audit.
- "might": ~25 instances. Similar pattern.
- "could": ~30 instances. Similar.
- "perhaps" / "possibly": ~5 each. Mostly fine.
- "tends to": ~3 instances. Mostly fine.
- "generally": ~25 instances. Many are appropriate qualifiers; verify against legal review.

**Fix:** Tag for legal review on Chapter 30 (Recommend-Against) specifically — that chapter MUST hedge carefully on attribution and assertion. Elsewhere, trim weak hedges. **Effort:** M.

## 🟡 41. Sentence-opener variety

Sample (Ch 4, lines 503–589):
- 6 sentences start with "The" or "These"
- 5 start with "A"
- 3 start with "Some"
- 2 with "What"
- Variety is OK ✓

**Effort:** none needed.

## ✅ 42. "Show don't tell" in composite scenes — generally good

Marcus's Ch 1 scene (lines 329–339) is present-tense and detailed ✓.
Priya's Ch 16 scene (lines 1521–1531) is present-tense with dialogue ✓.
Eleanor's Ch 21 scene (lines 1942–1961) is present-tense and procedural ✓.
Karen's Ch 29 scene (lines 2554–2568) is past-tense (descriptive) — slight tone mismatch with other composites.
Maria's Closing scene (lines 3294–3322) is past-tense (memoir framing). OK for closing.

**Note:** Composite scenes use mixed tense. PLAN specified "present-tense" for scene-level detail. Verify if past-tense closing scenes are intentional editorial choice.

**Effort:** S to verify; XS to fix.

## ✅ 43. Pronoun antecedents — generally clear

No major antecedent ambiguity found in the read-through.

## 🟡 44. Parallel construction in lists

Sample line 1056 (Week 1):
- "Read Parts I and II of this book." (imperative)
- "Take the self-test (Worksheet 13)." (imperative)
- "Identify the procedure category..." (imperative)
- "Set the walk-away number..." (imperative)
- "Identify your support system." (imperative)
✓ Parallel.

Line 670–678 (Four facilitator models):
- "Commission-based. The most common model. The facilitator receives a percentage..." (declarative)
- "Retainer-based. The patient pays the facilitator a flat fee..." (declarative)
- "Hospital-employed coordinator. The 'coordinator' is an employee..." (declarative)
- "Transparent-fee facilitator. The facilitator charges the patient..." (declarative)
✓ Parallel.

No major parallelism issues found. ✓

## 🟡 45. Dangling modifiers

Spot-check: no obvious danglers in the chunks reviewed. Verify in line-edit pass.

## 🟡 46. Sentence fragments

Used intentionally for rhythm in spots. Line 234: "Hope is important. It is not enough to sign consent." — sentence fragments are full sentences here. Line 175: "Documentation is leverage..." — full sentence. ✓

---

# Pass 4 — Mechanical copyedit

## 🟠 47. Spelling

Spot-check via grep for common error types. No systematic spelling errors found in the chunks reviewed. Confirmed correct: anesthesiologist (US), pediatric (US), gynecology (US), specific brand names (Stryker Triathlon, Zimmer Persona, DePuy Attune, Alcon AcrySof, Mentor MentorPromise, etc.).

**Effort:** Full pass needed; estimate S.

## 🔴 48. Hyphenation — confirmed inconsistencies

See finding 8 (word-list). Same issues; not double-counted. **Effort:** Included in 8.

## 🔴 49. Capitalization

See finding 10. Same issues. **Effort:** Included in 10.

## 🟠 50. Comma usage

- Oxford comma: used consistently ✓ (line 67 "Joint replacement, single-area dermatology, single dental implant.")
- Restrictive/nonrestrictive that/which: spot-check shows consistent ✓
- Comma splices: spot-check found none.

**Effort:** Full pass needed; estimate S.

## ✅ 51. Apostrophes

- "Marcus's" (line 329) — Chicago double-s with apostrophe-s ✓
- "Bernard Huang's" (no instance found in chunks)
- Plural possessives: spot-check OK ✓

## 🟡 52. Semicolon / colon discipline

Semicolons used appropriately ✓. Colons used appropriately ✓.

## 🔴 53. Em-dash density

See finding 18. **Critical for ship-readiness — major-house CEs flag em-dash overuse as a red-line.**

## 🔴 54. Numbers and units

See finding 11.

## 🟠 55. Acronym hygiene — first-use expansion gaps

**Acronyms that need first-use expansion:**

| Acronym | First use line | Currently expanded on first use? |
|---|---|---|
| ASPS | 131 | ❌ No — "American Society of Plastic Surgeons" full name used, but ASPS abbreviation introduced later (line 1184) without explicit "(ASPS)" connector |
| AAOS | 788 | ❌ Used as initialism without expansion. Expansion at line 1256 (AJRR context) |
| STS | 788 | ❌ First use without expansion. "Society of Thoracic Surgeons" not spelled out until line 1184 or so |
| ASMBS | 788 | ❌ Same |
| ASCO | 1184 | ❌ Same. Expanded at 1184 context but not on first use |
| ASRM | 1184 | ❌ Same |
| AAO | 1184 | ❌ Same |
| ASCRS | 2077 | ✅ "ASCRS (American Society of Cataract and Refractive Surgery)" — expanded ✓ |
| CRNA | 3572 | ❌ Used in Worksheet 6 without expansion |
| BBL | 131 | ✅ "Brazilian Butt Lift" parenthetical at line 351 |
| TKA | 337 | ❌ Used in Marcus's WhatsApp quote; expanded "total knee arthroplasty" at line 329 actually came first ✓. But Marcus's WhatsApp quote at 337 uses "TKA" — that's marketing speak, OK in dialogue.
| THA | 2332 | ✅ "Total hip arthroplasty (THA)" on first listing ✓ |
| TAVR | 2431 | ✅ "TAVR (transcatheter aortic valve replacement)" — expanded |
| CABG | 429 | ❌ Used without expansion. Expanded at 2422 "Coronary artery bypass grafting (CABG)"
| JCI | 201 | ✅ "Joint Commission International" line 201; abbreviation used immediately after
| NABH | 535 | ✅ "NABH (National Accreditation Board for Hospitals and Healthcare Providers)" — but actually at line 535 it's just "NABH (India)." Expansion is at line 541 and 1473. Late.
| FUE | 2212 | ✅ "FUE (Follicular Unit Extraction)" — expanded
| DHI | 2214 | ✅ "DHI (Direct Hair Implantation)" — expanded
| IFSO | 2175 | ✅ "IFSO (International Federation for the Surgery of Obesity)" — expanded
| GLP-1 | 1115 | ❌ Used without expansion ("GLP-1 medication hold per ASA guidance")
| ASA | 1115 | ❌ Used without expansion. ASA = American Society of Anesthesiologists.
| BIA-ALCL | 129 | ❌ Used in disclaimer without expansion. Expanded at line 2206 "BIA-ALCL surveillance for breast implant-associated anaplastic large cell lymphoma"
| MMWR | 131 | ✅ "(CDC MMWR 73(3))" — abbreviation works since CDC is well-known
| MMWR | 351 | ✅ "*Morbidity and Mortality Weekly Report*" — full name ✓

**Fix:** Add first-use expansion for: ASPS, AAOS, STS, ASMBS, ASCO, ASRM, AAO, CRNA, CABG, GLP-1, ASA (anesthesiology), BIA-ALCL. Move NABH expansion to first use. Match the ASCRS / FUE / DHI / IFSO / TAVR / THA pattern consistently.

**Effort:** S.

## 🟡 56. Abbreviations

- "Dr." (with period) — line 337 "Dr. ___ Board-certified" ✓
- "U.S." vs "US" — see finding ❌ (use "US" consistently; the 6 "U.S." instances at lines 131, 137 are inconsistent)
- "e.g." with comma — verify
- "i.e." with comma — verify
- "etc." — verify

**Fix:** Standardize. **Effort:** S.

## 🟠 57. Currency

See finding 12. Same issues.

## ✅ 58. Quotation handling

Block quotes for >3 lines: not used much; verify at typeset.
In-line for shorter: ✓

---

# Pass 5 — Consistency / cross-reference audit

This is the most critical pass for a technical reference book.

## 🟠 59. Chapter inline references — style mixed

- "Chapter X" form: 151 instances
- "Ch X" form: 44 instances
- "Ch. X" form: 0 instances

**Fix:** Pick one form. Recommendation: "Chapter X" in narrative prose; "Ch X" only in tight cross-reference contexts (e.g., the Reading Paths page where space is tight). Apply consistently. **Effort:** M.

## 🔴 60. Worksheet reference matrix — 4 worksheets unreferenced

| Worksheet | Title | Inline body refs | PLAN expected refs |
|---|---|---:|---|
| 1 | True Cost Calculator | 6 | ✓ |
| 2 | Cross-Procedure Quote Comparison | 4 | ✓ |
| 3 | Deposit Readiness Test | 7 | ✓ |
| **4** | **Clinic Verification** | **0** | **❌ Plan: Ch 4, Ch 16** |
| 5 | Specialist Credential | 3 | ✓ |
| **6** | **Anesthesia Provider Verification** | **0** | **❌ Plan: Ch 16, Ch 28** |
| 7 | Second Opinion Request | 1 | ✓ |
| 8 | Coordinator Log | 3 | ✓ |
| **9** | **Day-of-Procedure Checklist** | **0** | **❌ Plan: Ch 32** |
| 10 | Records Packet Cover Sheet | 3 | ✓ |
| 11 | Records Packet Inventory | 2 | ✓ |
| 12 | Follow-Up Care Script | 2 | ✓ |
| 13 | Self-Test | 7 | ✓ |
| 14 | Accreditation Verification | 2 | ✓ |
| 15 | Cross-Border Insurance | 2 | ✓ |
| **16** | **Multi-Procedure Sequencing** | **0** | **❌ Plan: Ch 9, Ch 35** |
| 17 | Procedure Complexity Self-Rating | 3 | ✓ |
| 18 | Family Decision | 1 | ✓ |
| 19 | Diaspora-Specific | 2 | ✓ |
| 20 | Cross-Border Claim | 2 | ✓ |

**Fix:** Add inline references for Worksheets 4, 6, 9, 16 at their PLAN-specified chapters. Pattern: "*A reusable copy is Worksheet X (Title) in the back matter.*" **Effort:** S.

## 🟠 61. Section / page pointers

The manuscript doesn't use page references (which require post-typeset numbering). All cross-references are chapter-based ✓.

## 🔴 62. Cited statistics — partial consistency

Spot-check of recurring numbers:

| Statistic | All-instance values | Status |
|---|---|---|
| CDC MMWR 93 deaths | 93 (all 7 mentions) | ✅ Consistent |
| BBL mortality range | 1 in 3,000 to 1 in 6,241 (all 3 mentions) | ✅ Consistent |
| 92% involving gluteal fat transfer | "92 percent" 3× / "92%" 3× | ❌ Format inconsistent |
| Marcus all-in cost | $14,800 (Ch 1) vs $14,000 (Ch 18) vs $14,800 + $26,400 (Ch 31) | ❌ See finding 25a |
| Industry size | $74–$92B (line 345) | Single mention |
| US medical travelers | 1.4–2 million (lines 345, 353) | ✅ Consistent |
| Global travelers | 14–16 million (line 345) | Single mention |
| 60-day plan | 60 days (multiple) | ✅ Consistent |
| Deposit Readiness Test questions | 15 questions (lines 806, 895, 1107, 1109, 1111, 3516) | ✅ Consistent |
| Self-Test questions | 20 questions (lines 994, 1044, 3713) | ✅ Consistent |
| Worksheet count | 20 (line 26, 91, 538) | ✅ Consistent |
| Composite count | 9 (line 246, 3375) | ✅ Consistent |
| Bernard's Notes count | 7 (PLAN; manuscript has 7 ✓) | ✅ Consistent |

**Fix:** Marcus cost (25a) is ship-blocking. 92%/92 percent formatting per finding 11. **Effort:** S for format; M for Marcus.

## 🟠 63. Source-name consistency

- *NEJM* (italicized, abbreviated) ✓
- *N Engl J Med* — not used.
- *Lancet* / *The Lancet*: line 351 "*The Lancet*" — wait, line 351 doesn't actually italicize Lancet. Let me re-check. Line 588 "*The Lancet*" ✓. Line 2497 "*Lancet*" (no "The") ❌. Lock format.
- *JAMA* / *Journal of the American Medical Association*: line 413 "*Journal of the American Medical Association*" — full name ✓. Subsequent uses "JAMA" implicit.
- *JBJS* / *Journal of Bone and Joint Surgery*: line 1285 "*JBJS*" abbreviated; line 2410 "*Journal of Bone and Joint Surgery* (JBJS)" expanded. Different forms. Lock.

**Fix:** Pick one form for each journal; verify all mentions. **Effort:** S.

## 🟠 64. Organization-name consistency

- "Memorial Sloan Kettering" vs "MSK" vs "MSK Direct" vs "MSK International": all used. Different programs at the same institution? Line 1385: "**Memorial Sloan Kettering International (MSK Direct)** (*mskcc.org/international*)" — "MSK Direct" is the parent name. But line 252, 1443, 2551, 2562 use "MSK International" without the "(Direct)" — which is a different program label. This needs reconciliation.

In reality: MSK has "Memorial Sloan Kettering International" as the program name (under which "MSK Direct" is the consumer-facing brand for second opinions). The book conflates these. **Verify with MSK's actual program structure.**

**Fix:** Either pick one consistent name OR add a clarifying parenthetical at first use. **Effort:** S.

## 🟡 65. Country-name consistency

- "Turkey" (used) — fine. The modern Turkish-government-preferred "Türkiye" is not used; that's editorial choice.
- "South Korea" (line 1507) — consistent ✓
- "Costa Rica" — consistent ✓
- "Mexico" — consistent ✓
- "India" — consistent ✓

✅ Country naming is consistent within the manuscript.

## 🟠 66. Date-format consistency

- "2009–2022" (en-dash range) — consistent ✓
- "2017, 2019, 2023" (FDA stem-cell warnings, comma-separated years) — consistent ✓
- "fourteen months retired" (line 1961) vs "14 months" — see numerals finding

## 🟡 67. Title case in chapter headings

Sample: "## Chapter 1 — Two Million Decisions" — title case ✓
"## Chapter 23 — Step 1–2 Procedures: Ophthalmology, Diagnostic, and Dental" — title case ✓
"## Chapter 38 — When the Outcome Disappoints: The Year After" — title case ✓ ("After" follows colon ✓)

Some chapters use em-dash between number and title; some use colon for sub-clause. Verify systematic application.

✅ Generally consistent.

## 🔴 68. TOC matches headings — minor mismatch

**TOC entry (line 68):** "Chapter 27 — Orthopedic Surgery"
**Body heading (line 2325):** "## Chapter 27 — Orthopedic Surgery (Joint Replacement and Spine)"

TOC truncates the parenthetical. Either should be:
- "Chapter 27 — Orthopedic Surgery (Joint Replacement and Spine)" in TOC, OR
- "Chapter 27 — Orthopedic Surgery" in body heading

Recommended: keep the descriptive parenthetical; update TOC.

Similar minor mismatches in other parts of TOC need checking systematically.

**Fix:** S.

---

# Pass 6 — Fact-check

This is the highest legal-exposure pass. I can verify what I can reach without external authentication; some claims require subscription-level verification or primary-source access that I cannot do in this session. I have flagged each with confidence level.

## 🟠 69. Cited numbers — primary-source verification status

| Claim | Source cited | Verifiable? | Notes |
|---|---|---|---|
| 93 US-citizen deaths in DR 2009–2022, 92% gluteal fat transfer | CDC MMWR 73(3) | ⚠️ **Verify exact volume/issue** | CMD MMWR 73 = 2024 publication year. Spot-check the citation against published indices. |
| BBL mortality 1 in 3,000 to 1 in 6,241 | "South Florida case series" (line 749) + ASPS BBL safety warnings | ⚠️ The 1:6,241 figure is from a specific peer-reviewed paper (Mofid et al. *Aesthetic Surgery Journal* 2017). Verify exact source. |
| US LASIK volume ~600,000/year | (no source) | ⚠️ Plausible but verify |
| US cataract volume ~4 million/year | (no source) | ⚠️ Plausible (real number ~3.8M) |
| US bariatric volume ~280,000/year | ASMBS | ✅ Plausible (recent ASMBS estimates are ~260–280K) |
| US joint replacement: 700K TKA + 350K THA | AAOS | ⚠️ Verify recent figures (actual TKA volume has been ~790K in 2023; THA ~500K) |
| US lumbar fusion ~500K/year | (no source) | ⚠️ Verify |
| US CABG ~340K/year | STS National Database | ⚠️ Verify (recent STS suggests ~190K; the cited figure may be high) |
| US IVF cycles ~330K/year | SART | ⚠️ Verify (SART 2022 ~390K cycles; cited figure may be low) |
| AJRR captures >2.5M procedures across >1,300 institutions | AJRR | ⚠️ Verify (recent AJRR captures ~3M+) |
| China Tribunal Final Report (2020), Sir Geoffrey Nice QC | China Tribunal | ✅ Real document; verify date (2019 final report; the manuscript says 2020) |
| Philippines kidney market ban (line 2598) | 2008 ban | ✅ Verifiable (the ban exists; year accurate) |
| India banned commercial surrogacy for foreigners (line 2295) | 2015 ban | ✅ Verifiable (Indian Surrogacy [Regulation] Bill timeline matches) |
| Walmart/Lowe's self-insured medical-tourism plans (line 617) | "trade press" | ⚠️ Verify — Walmart's Centers of Excellence program is real (Mayo, Cleveland Clinic, Geisinger contracts); Lowe's similar arrangements exist. Verify scope. |
| Cleveland Clinic Connect URL | clevelandcliniclabs.com | ⚠️ **URL likely wrong** — Cleveland Clinic's second-opinion program is at *my.clevelandclinic.org/online-second-opinions* or similar. "clevelandcliniclabs.com" doesn't appear to be the consumer-facing portal. **VERIFY.** |
| Mayo Clinic Connect URL | mayoclinic.org/online-services/online-second-opinion | ⚠️ Verify — Mayo's program is "Mayo Clinic Online Services" but specific path needs verification |
| MD Anderson URL | mdanderson.org/online-second-opinion | ⚠️ Verify |
| MSK URL | mskcc.org/international | ⚠️ Verify — likely correct but confirm |
| Mass General URL | massgeneral.org/international | ⚠️ Verify |
| Johns Hopkins International URL | hopkinsmedicine.org/international | ⚠️ Verify |
| nabh.co | India accreditation directory | ✅ Real domain |
| nmc.org.in | India NMC | ✅ Real domain |
| cedulaprofesional.sep.gob.mx | Mexico cédula registry | ✅ Real domain (sep.gob.mx is Mexico's Secretaría de Educación Pública) |
| medicos.cr | Costa Rica Colegio | ⚠️ Verify — actual Costa Rica medical college URL may be different |
| Implant brand names | Stryker Triathlon, Zimmer Persona, DePuy Attune, Alcon AcrySof, Mentor MentorPromise | ✅ All real products |
| Wave LASIK platforms: Allegretto/Visx/Schwind | (line 2069) | ✅ Real platforms |
| Industry size $74–$92B (line 345) | "trade press" | ⚠️ **Verify with Patients Beyond Borders, IMTJ, Deloitte, etc.** Different sources give different ranges. |

**Critical sub-finding 69a:** **Cleveland Clinic URL is likely wrong.** "clevelandcliniclabs.com" reads like a clinical labs subdomain, not the second-opinion portal. The real portal is in the path of `my.clevelandclinic.org` or similar. **Must verify before printing.**

**Fix:** Build a fact-check spreadsheet; verify every URL by clicking; verify every volume figure against the most recent year's primary source. **Effort:** L (1 dedicated session).

## 🟠 70. Named organizations — verified to exist

All major orgs cited (Cleveland Clinic, Mayo Clinic, MD Anderson, MSK, Mass General Brigham, Johns Hopkins, AAOS, ASPS, ASMBS, STS, ASRM, ASCO, AAO, IFSO, ASCRS, ABMS, ESHRE, NCI, FDA, CDC, WHO, State Dept, JCI, AAAASF, ISQua, NABH, ACHSI, HAI, Apollo Hospitals, Bumrungrad, Anadolu Medical Center, Narayana Health, Fortis Healthcare, AIIMS, INCan, Tel Aviv Sourasky, Heidelberg, Apollo Cancer Centers, NCCS Singapore) — **all real** ✓.

## 🟡 71. Named registries

AJRR, NJR, AOANJRR, SHAR, ESHRE, STS National Database, NCDR, NSQIP, SART, MAUDE — **all real** ✓.

## ⚠️ 72. Cited studies — sourcing depth

The manuscript cites several specific bodies of evidence (CMA Journal articles, Lancet commentaries, China Tribunal, peer-reviewed harm case series in JCO/JAMA Oncology/Nature/Cell Stem Cell, ophthalmology vision-loss case series). These are referenced but not cited at paper level.

For a buyer-protection book that takes editorial positions on documented harm, **specific paper-level citations strengthen the book's defense in legal review.** The current "source notes" approach (line 3928–3950) is a list of source categories, not specific citations.

**Recommended fix:** For the Chapter 30 patterns specifically, add specific paper citations for each named claim. The malpractice attorney reviewer (per Bernard's Note #6 at line 2680) will likely require this. **Effort:** L.

## ⚠️ 73. Cited cost figures

Most cost ranges are reasonable on inspection (US TKA $40K–$60K retail ✓; Mexico dental implant + crown $1,200–$2,500 ✓). Some are aggressive:
- **India CABG $5,000–$10,000 (line 2454)** — the low end is on the very-low end of cited India CABG figures. Recent figures suggest $7,000–$15,000 is more typical. Verify with current Apollo / Narayana published pricing.
- **Lumbar fusion India $10,000–$15,000 (line 2358)** — reasonable.
- **MSK opinion $1,500–$3,000 (line 1385)** — verify.

**Fix:** Verify each cost range against current published figures or note "approximate, as of 2026" prominently. **Effort:** M.

## ⚠️ 74. URLs

See sub-finding 69a (Cleveland Clinic). All URLs need click-verification.

**Fix:** Click every URL. Replace dead ones. **Effort:** S.

## 🟠 75. Credentialing-pathway accuracy

- Mexico cédula profesional: verified accurate
- India NMC: verified accurate
- Thailand: "Thai Medical Council" — verify exact name (may be "Medical Council of Thailand")
- Turkey: "Turkish Medical Association" handles specialty boards — verify (Turkey's medical regulation is through Ministry of Health + Turkish Medical Association — accurate)
- Costa Rica Colegio: verified accurate
- Korea: "Korean Medical Association" — verify (KMA is the professional body; Korean Hospital Association is different)
- Dominican Republic: "Colegio Médico Dominicano" — verify exact name

**Fix:** Verify each country's exact regulator name. **Effort:** S.

## 🟠 76. Regulatory citations

- FCBA (Fair Credit Billing Act) — accurate ✓
- WHCRA 1998 (Women's Health and Cancer Rights Act 1998) — accurate ✓
- HIPAA cross-border — manuscript references; HIPAA's international scope is limited (HIPAA applies to US-covered entities; international care isn't directly governed). Verify framing.
- EU MDR (Medical Device Regulation) — accurate ✓
- GDPR — accurate ✓
- GS1 UDI framework — accurate ✓
- 16 CFR Part 255 (FTC endorsement guidelines) — accurate ✓

✅ Regulatory citations look accurate.

## 🟠 77. Regulatory body / specialty board citations

- ABMS, ASPS, ASA, AAOS, ASMBS, STS, ASRM/ESHRE, ASCO, AAO, ABCS — all real ✓
- ISAPS (International Society of Aesthetic Plastic Surgery) line 788 — real ✓
- AMCG (Asociación Mexicana de Cirugía General) line 1467 — verify exact name
- AMOSEP — verify

**Fix:** Verify exact Mexican specialty association names. **Effort:** XS.

---

# Pass 7 — Sensitivity / inclusion / legal-adjacent

## 🟠 78. Body and weight language

Bariatric chapter (Ch 24) and Maria's scenario (Composite L) — review for:
- "Obese" (line 2123) — clinical term, used appropriately in clinical context ✓
- "Severe obesity" (line 2123) — clinical ✓
- "BMI 41" / "BMI 32" / "BMI 28" — clinical metric ✓
- Maria's framing: "She had been on the equivalent of 14 different weight-management approaches in the previous decade. She did not believe a 15th would change the trajectory." — non-judgmental ✓
- "Weight regain" (line 2169) — clinical ✓
- No "morbidly obese" / "fat" / "overweight" pejorative usage found ✓

Person-first language: generally respected ("the patient who has had..."), though some places use "bariatric patients" (procedure-defined collective noun) — acceptable in clinical context.

**Sensitivity reader recommendation:** ✅ Generally appropriate. Minor: line 3318 "her brother, who is also overweight and has been talking about bariatric surgery for two years" — "overweight" is clinical and OK, but "her brother, who has been considering bariatric surgery..." might be slightly more person-first.

**Effort:** XS.

## 🟡 79. Mental-health language

- "Body dysmorphic disorder (BDD)" — line 2157 — clinical, accurate ✓
- "BDDQ (Body Dysmorphic Disorder Questionnaire)" — line 217 — accurate ✓
- "Binge eating disorder, depression, anxiety, body dysmorphic disorder" (line 2157) — clinical list, OK ✓
- "Post-operative delirium" (line 2400) — clinical, accurate ✓

✅ Mental-health language is respectful and clinical.

## 🟡 80. Aging / dementia language

Daniel's father (Composite D):
- "Mild dementia" (line 2107) ✓
- "Memory too fragile" (line 2111) — Daniel's sister's framing in dialogue — OK as character voice ✓
- "His memory has progressed" — implied at line 2396 — clinical
- No "senile" / "demented" pejoratives ✓

✅ Appropriate.

## 🟡 81. Cancer language

Karen's mother (Composite E):
- "Stage III breast cancer" (lines 111, 1439, 2556) — clinical ✓
- "Living with cancer" not used (could be added).
- "Cancer patient" — used in some places (line 2530); person-first alternative is "patient with cancer." Sensitivity reader may flag.
- "Stage III" used; lowercase "s" stage. CMOS = capital S? — verify
- "Recurrence" — clinical ✓
- "Stage three" (line 111 narrative) — spelled-out form vs Roman numeral elsewhere — see finding 11

**Effort:** XS.

## 🟡 82. Race / ethnicity / nationality

Priya's diaspora storyline (Composite B):
- Indian-American protagonist, mother in Mumbai — respectful portrayal
- Family doctor "of fifteen years" — respectful of family-doctor relationship
- "Cardiologist who has known you for fifteen years is exactly the cardiologist I might not have verified — and that is the verification that matters most" (line 1531) — Priya's voice, respectful, frames diaspora frame as informed choice ✓
- "The diaspora frame is different from the cost-savings frame" (line 1591) — non-judgmental ✓
- No orientalist or colonial framing of Indian medicine ✓

Mexico (Composite D, L, others):
- "Cédula profesional" usage ✓
- "Los Algodones" / "Tijuana" — geographic, no stereotyping ✓
- Maria's husband as companion (line 3308) — respectful ✓

Brazil (line 429): "Brazilian plastic surgeons concentrated certain body contouring techniques in São Paulo and Rio" — geographic context, respectful ✓.

✅ Cultural framing is consistent with editorial caution.

## 🟡 83. Class / income

Marcus (cost-crisis reader): line 329 portrayal is respectful — engineer, married, working. Not pathologized.
Eleanor (chronic-condition, HSA): retired, planning carefully. ✓
Karen (good insurance): emphasized that the family's financial position is "not catastrophic" — explicit (line 1439) ✓
Maria (HSA-funded): "well within her HSA balance" (line 3316) — middle-class framing ✓
Priya: software engineer, parental insurance access. ✓

No sneering at low-income readers. ✓

## 🟡 84. Gender / pronouns

- He/she used. Marcus = he, Priya = she, Eleanor = she, Daniel = he, Karen = she, Maria = she.
- "Patient" used as singular common-gender ✓
- "Companion" used as common-gender ✓
- No instances of singular "they" — that's fine; gender-specific characters use binary pronouns.

Sensitivity flag: no explicitly nonbinary/queer composite. PLAN doesn't specify. Editorial choice.

✅ Acceptable.

## 🔴 85. Defamation review — Chapter 30 needs legal review

Ch 30 "Patterns We Recommend Against" names:
- China, Pakistan, Egypt, Philippines, Bangladesh (organ-trafficking corridors)
- "Mexican alternative cancer clinics (Hoxsey, Gerson, others)"
- "German biological cancer clinics in Frankfurt and elsewhere"
- "Specific Texas-Mexico border clinics" (line 2623)
- "Hoxsey" — specific clinic name

This is the highest legal-exposure chapter. Bernard's Note #6 (line 2682) explicitly says "The malpractice attorney who reviewed this chapter in Phase 5 will pressure-test the language" — acknowledging legal review is needed.

**Recommended fix:** Phase 5 legal review is required. Until that review, treat Ch 30 as draft-only. **Effort:** External legal review session.

## 🔴 86. Liability/disclaimer language

The Important Disclaimer (line 127) and Appendix Disclaimer (line 3986) are strong and comprehensive. They cover:
- General educational material disclaimer ✓
- Procedure-specific risk overview ✓
- CDC/FDA/State Dept pattern citation ✓
- Concerning-symptoms warning ✓
- Regulatory variation disclaimer ✓
- Non-endorsement statement ✓
- Reader responsibility statement ✓

**Both disclaimers are appropriate first-draft form.** Legal review will pressure-test specific language. **Effort:** External legal review.

---

# Pass 8 — Apparatus and front/back matter

## 🟡 87. Title page

Lines 9–17: Title, subtitle, byline, series volume, edition. ✅ All present.

## 🟡 88. Copyright page

Not currently present. PLAN expects it. Volume 2 has one (presumably in its metadata.md or build pipeline). For V3, the copyright page needs to be drafted at Phase 4 production.

**Fix:** Draft copyright page for Phase 4. **Effort:** S.

## 🟡 89. Dedication / acknowledgments

- No dedication present.
- Acknowledgments at lines 3976–3982 — short (124 words), generic. PLAN target 250. Could be expanded with specific reviewer names (when reviewer panel is confirmed in Phase 5).

**Fix:** Expand acknowledgments at Phase 5 with named reviewers. **Effort:** S.

## 🔴 90. Contents (TOC) — see finding 68

Minor mismatch with body headings. **Fix:** S.

## 🔴 91. Scenario Index — see finding 31

Karen's entry says Ch 29 only; she also appears at Ch 15. Composite G is indexed for Ch 36 but no scene. **Fix:** M (after resolving Karen duplicate and Composite G scene).

## 🟠 92. Reading Paths — verify chapter targets

Lines 264–278. Each path lists specific chapters. Spot-check:
- Path A: Ch 1, 7, 8, 10, 11, 14, 18, 20, 30, [survey], 37 — all exist ✓
- Path B: read in order ✓
- Path C: Ch 1, 7, 10, 14, 16, 23, [survey], 34, 35, Composite L ✓
- Path D: Ch 1, 16, 17 (diaspora section), 24 or [survey], 14, 35, Composite B (Priya) ✓
- Path E: Ch 1, 2, 3, 4, 7, 8, 10, [survey scan], 30, Final Note ✓
- Path F: Ch 1, 30, 37, [survey], 14, Worksheet 20 ✓

✅ Reading Paths chapter references are all valid.

## 🔴 93. 20 Worksheets — present but mostly stubs

See finding 3. ❌ Drafting gap, not audit gap.

## 🔴 94. Glossary — at 47% of target

See finding 4. ❌ Drafting gap.

## 🔴 95. Source Notes — at 39% of target

See finding 5. ❌ Drafting gap.

## 🟡 96. About Tabiji / About the Editor / Acknowledgments / Appendix Disclaimer

- About Tabiji (line 3954): 118 words. ✓ Reasonable.
- About the Editor (line 3964): 146 words. ✓ Reasonable. PLAN expected ~300; current is light but acceptable.
- Acknowledgments (line 3976): 124 words. See finding 89.
- Appendix Disclaimer (line 3986): 783 words. ✓ Comprehensive.

---

# Pass 9 — Proofread (post-typeset)

Dimensions 97–102 are post-typeset and not applicable now. They cover:
- Widows / orphans
- Bad page breaks
- Bad line-end hyphenation
- Running heads / folios
- TOC / Index page numbers
- Image placement / captions
- Final typo sweep

These will be the proofreader's pass after Phase 4 production builds the paperback PDF and EPUB.

---

# Critical findings index — 12 ship-blocking issues

| # | Finding | Where | Severity |
|---:|---|---|---|
| 1 | Manuscript at 61% of word target | Whole book | 🔴 Drafting gap |
| 2 | Part V procedure surveys at 41% of target | Ch 23–31 | 🔴 Drafting gap |
| 3 | Marcus all-in cost inconsistency | Ch 1 / 18 / 31 | 🔴 Continuity |
| 4 | Karen duplicate scene | Ch 15 / 29 | 🔴 Continuity |
| 5 | Composite G (Daniel companion) missing | Ch 36 | 🔴 Missing content |
| 6 | Cardiac anesthesia provider for knee replacement | Ch 31 line 2710 | 🔴 Factual |
| 7 | Cleveland Clinic URL likely wrong | Ch 15 line 1379 | 🔴 Factual |
| 8 | Eleanor HSA + Medicare timing | Ch 21 line 1942 | 🔴 Factual continuity |
| 9 | Em-dash density 10.2/1000 words | Whole book | 🔴 Style |
| 10 | Worksheets 4, 6, 9, 16 unreferenced inline | Body | 🔴 Cross-reference |
| 11 | Style sheet not locked (numerals, %, U.S./US, citation) | Whole book | 🔴 Style |
| 12 | Chapter 30 needs malpractice-attorney legal review | Ch 30 | 🔴 Legal |

---

# Effort summary by phase

| Pass | Total findings | Effort if fixed solo | What's blocked |
|---|---:|---|---|
| Pass 0 Developmental | 6 | XL (multi-session drafting) | Drafting + Phase 4 production |
| Pass 1 Style sheet | 18 | M | Mechanical pass |
| Pass 2 Character bible | 8 | M-L | Story continuity |
| Pass 3 Line edit | 14 | L (full pass) | Voice / readability |
| Pass 4 Mechanical | 12 | M | Polish |
| Pass 5 Consistency | 10 | M-L | Internal coherence |
| Pass 6 Fact-check | 9 | L (one dedicated session) | Legal exposure |
| Pass 7 Sensitivity/legal | 9 | External review | Ch 30 ship-readiness |
| Pass 8 Apparatus | 10 | M | Front/back matter ship-readiness |
| Pass 9 Proofread | (not applicable) | — | Post-typeset |
| **TOTAL** | **96** | **3–5 dedicated sessions for what I can do solo, plus 1–2 external (legal + fact-check)** | |

---

# Recommended next steps

Based on what this audit found, ordered by leverage and dependency:

## Path I: Honest expansion before audit-to-ship

This is what the manuscript actually needs.

1. **Expand drafting to target** (Pass 0 findings 1–5): Part V procedure surveys to ~22K words; worksheet content to ~5,500 words; glossary to ~1,000 words; source notes to ~800 words; flesh out thinner parts. **5–8 sessions.**
2. **Resolve continuity errors** (findings 25a, 25b, 25c, 26b, 27a, 27b, 28a, 29, 30a, 31a): Marcus cost reconciliation; Karen duplicate scene resolution; Composite G scene addition; cardiac-anesthesia fix; Eleanor HSA timing; etc. **1 session.**
3. **Rerun mechanical and consistency passes** (Passes 1, 4, 5): apply style sheet; em-dash reduction; chapter-reference normalization; worksheet inline references; acronym hygiene. **2 sessions.**
4. **Fact-check pass** (Pass 6): URL verification; primary-source citation; cost-range update. **1 session.**
5. **Phase 4 production pipeline** (finding 6): mirror V2 scripts; CSS; cover art generation. **1 session + cover-art generation.**
6. **External legal review of Ch 30** (Pass 7 findings 85, 86). **External attorney.**
7. **Phase 5 reviewer panel** per BRIEF + PLAN §15. **4–6 weeks external.**
8. **Proofread pass** (Pass 9) post-typeset. **0.5 session.**

**Realistic total to ship-ready:** 8–12 of my sessions + 4–6 weeks external review + 1 attorney review.

## Path II: Tighter book at honest length

Re-position V3 as a tighter 55–65K orientation primer; trim PLAN scope; ship faster.

1. Revise PLAN: 6 procedure surveys instead of 10; smaller back matter; tighter framing.
2. Apply this audit's continuity/factual/legal findings only (skip Pass 0 drafting expansion).
3. Reuse Passes 1, 4, 5 fix work (still needed).
4. Production + legal review + reviewers + ship.

**Realistic total:** 4–6 of my sessions + external review + reviewers + ship.

## Path III: I cannot honestly recommend "audit the current 50K and ship"

The audit findings make clear that a copyedit pass on this draft, however thorough, leaves a manuscript that is structurally incomplete (under-target, missing scenes, duplicate scenes, factual errors, unverifiable URLs, unreferenced worksheets). A printer proof would expose these; reviewers would flag them; Amazon reviewers would notice them. Your job is safer if we expand first, audit second, ship third — even if the timeline is longer.

---

*End of audit report. This document is the result of one full-read pass plus four programmatic consistency-check passes against all 96 audit dimensions in the framework. It is not a substitute for a paid major-house copyedit; it is the prepared work that makes such a copyedit shorter and the eventual ship-ready manuscript cleaner.*
