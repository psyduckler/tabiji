# Phase 2 Complete — First-Draft Manuscript Ready for Phase 3 Editorial

**Last updated:** 2026-05-11 (back matter committed; Phase 2 COMPLETE)
**Manuscript word count:** 74,407 words
**Status:** First-draft complete. Ready for Phase 3 editorial passes.

---

## Phase 2 final inventory

| Section | Words | Status |
|---|---:|---|
| Front matter | ~5,000 | ✅ |
| Part I — Before You Ask for a Quote (Chs 1-4) | ~9,000 | ✅ |
| Part II — Money and Quotes (Chs 5-6) | ~5,500 | ✅ |
| Part III — Clinic and Surgeon Due Diligence (Chs 7-12 + DG) | ~11,600 | ✅ |
| Part IV — Deposits, Payment, Commitment (Chs 13-14) | ~6,800 | ✅ |
| Part V — Before You're Wheeled In (Chs 15-21 + DG) | ~10,300 | ✅ |
| Part VI — Recovery and Coming Home (Chs 22-27 + DG) | ~8,850 | ✅ |
| Part VII — When the Pattern Is the Risk (Chs 28-31) | ~6,500 | ✅ |
| Composite Scenario L (Iris) | ~1,000 | ✅ |
| Final Note — What Prepared Looks Like | ~750 | ✅ |
| Back Matter (How to Use + 19 worksheets) | ~7,700 | ✅ |
| Glossary (42 terms) | ~1,000 | ✅ |
| Source Notes (14 source categories) | ~900 | ✅ |
| About Tabiji + About the Editor + Acknowledgments | ~750 | ✅ |
| Appendix Disclaimer | ~900 | ✅ |
| **Total** | **74,407** | **✅** |

(Words above are summary estimates; exact total is 74,407 per `wc -w`.)

---

## Editorial position summary (for Phase 5 reviewer briefing)

The first-draft manuscript holds the editorial positions set in `BRIEF.md`:

1. **High-risk procedure list (BRIEF §6)** is delivered in Chapter 28 as the seven-item editorial recommendation against specific patterns: BBL with intramuscular fat injection anywhere; combination procedures involving BBL; the CDC MMWR DR pattern by structural criteria (non-accredited / combination / comorbid); stem-cell and unapproved regenerative cosmetic biologics; non-accredited "boutique" facilities Step 3+; unverifiable surgeon credentials; unverifiable anesthesia provider credentials. Each entry is sourced.
2. **Anesthesia framing (BRIEF §6, §7)** is delivered in Chapter 18 as the three-question framework (named provider + monitoring + emergency protocol), with the provider-type literature framing per BRIEF §7 — no statistically significant mortality difference physician vs CRNA when patient/procedure factors controlled.
3. **BDD screening (BRIEF §6)** is delivered in Chapter 19 with the BDDQ + DCQ referenced in Worksheet 12. Editorial frame: "Your body. Your decision. The book's job is to make sure the decision is made under conditions that protect you."
4. **Composite scenarios show near-misses, not deaths (BRIEF §10).** All 12 composites (A–L) hold this discipline.
5. **No clinic recommendations.** The book recommends *against* specific patterns; it does not recommend *for* specific clinics, surgeons, destinations, or facilitators.
6. **Buyer's-seat editorial voice.** The editor is consumer journalist, not clinician. The disclaimer (Appendix) is strong.

---

## What Phase 3 should address

The first draft is shippable to reviewers in principle. Phase 3 sharpens it before reviewer outreach. Suggested structure mirrors the dental Phase 3 pattern:

### Tier 1 — Structural, factual, clinical-safety pass

Items the editorial team can address from inside the manuscript before reviewer involvement:

- **Cross-reference verification.** The book uses inline references like "(Chapter 19)" or "Worksheet 12 in the back matter." Verify every cross-reference points to the right place.
- **Pull-quote tagging consistency.** Pull quotes are marked `::: {.pullquote}`. Verify each is on its own paragraph and the designer can extract them.
- **Cited-number consistency.** Numbers cited multiple times across chapters (BBL mortality 1:3,000–1:6,241, CDC MMWR 93 deaths 2009–2022 92% BBL, anesthesia mortality 1/M baseline + 0.01–0.016% cosmetic, BDD prevalence 7–18%, etc.) should match exactly between mentions.
- **Source-note coverage.** Every clinical claim in the manuscript should have a source category in the Source Notes that covers it. If a clinical claim lacks coverage, either remove the claim or add a source category.
- **Composite scenario consistency.** Twelve composites (A–L); verify each scenario's character details are internally consistent across mentions (e.g., Aisha is 32 in Ch 1 and again in Ch 16).
- **Worksheet cross-references.** The manuscript references Worksheet 3 (Ch 13), Worksheet 12 (Ch 19), Worksheet 16 (Ch 26). Verify each exists at the referenced number and contains what the manuscript says it does.
- **Chapter 28 sourcing.** Every item on the seven-item list cites its evidence base. Phase 5 plastic-surgeon reviewer will pressure-test specifically here.

### Tier 2 — Voice consistency and redundancy pass

- The book is long (74K words); some redundancy has accumulated. Identify passages that repeat the same point across chapters with minor variation, and either tighten or remove.
- Voice should remain consistent: calm, protective, non-judgmental. Spot-check for any passage that drifts to alarmist, dismissive, or paternalistic tone.
- "We" vs. "you" pronoun usage: review for consistency. The dental book established "we" (editorial) and "you" (reader) as the two voices; "I" is rare.
- Sentence-length variation: long technical chapters (Ch 18, Ch 28) benefit from occasional short declarative sentences as structure.

### Tier 3 — Line-level polish

- Comma usage, em-dash usage, hyphenation consistency.
- US English spelling (the dental book is US English; maintain consistency).
- Numbers: spell out one to nine, numerals from 10 onward, with consistent exceptions (currency, percentages, dates, ages, doses).
- Procedure names lowercase (rhinoplasty, abdominoplasty) per medical convention; brand names (Ozempic, Mentor MentorPromise) capitalized per source.

---

## How to continue in Phase 3

Suggested approach for the editorial pass:

1. **Read the entire manuscript first.** Tier 1 audit notes go into a single working document — a Phase 3 audit log — listing every issue by location (chapter, section, paragraph or line reference).
2. **Batch the fixes by tier.** Tier 1 first (one commit per Part), then Tier 2 (voice/redundancy, one commit), then Tier 3 (polish, one commit). Avoid mixing tiers in a single commit.
3. **Use the dental book pattern.** The dental book had three iterative passes; the same iterative discipline applies here.
4. **Stop short of reviewer-territory issues.** Phase 3 is internal editorial; Phase 5 is external review. Do not over-engineer language Chapter 28 reviewers should weigh in on. If a passage seems likely to draw reviewer pushback, flag it in the audit log rather than pre-editing it.

After Phase 3, the manuscript should be reviewer-ready.

---

## Realistic remaining timeline

Per BRIEF §13, the realistic launch window from Phase 0 sign-off is 11–13 weeks. We are at:

- **Phase 0** (brief): complete
- **Phase 1** (research + outline + framework adaptation): complete
- **Phase 2** (first-draft manuscript): complete ← we are here
- **Phase 3** (editorial passes): 1–2 sessions
- **Phase 4** (production: CSS, EPUB, KDP paperback, cover): 1 session, mirrors dental
- **Phase 5** (human reviewers, in parallel): 4–6 weeks external

If Phase 3 begins immediately and reviewer outreach is already in flight (per BRIEF §17), the book remains on track for late August / early September 2026 launch.

---

## What still requires user action

1. **Reviewer outreach.** Per BRIEF §11 the reviewer panel is plastic surgeon, anesthesiologist (especially for Ch 18), mental-health clinician (for Ch 19), malpractice attorney (for Ch 28 and Appendix Disclaimer), sensitivity reader, copyeditor, proofreader. Outreach should be in flight now; book budget $4,400–$8,800.
2. **About the Editor expansion.** Phase 4 prereq.
3. **Cover production direction.** BRIEF §12 — continue Direction 2 (Field Guide aesthetic) per dental volume for series consistency, or change.
4. **Phase 5 reviewer attribution.** Acknowledgments section reserves named acknowledgments with each reviewer's consent.

---

## What this session deliberately did NOT do

- Did not begin Phase 3 editorial pass within this session. The first-draft commit is a clean handoff point; Phase 3 deserves a dedicated session with fresh context and the full manuscript readable in one pass.
- Did not begin Phase 4 production setup. Phase 4 happens after Phase 3 and after final word count and chapter count are locked.
- Did not produce reviewer briefing materials. Those are derived from BRIEF.md + this PROGRESS file + the manuscript; preparing them is a small task best done at Phase 5 outreach time.

---

## Honest assessment

The book is a strong first draft. The editorial discipline of the dental volume held through 74,000 words. The two highest-stakes net-new chapters (Ch 18 Anesthesia, Ch 19 Mental-Health Pre-Op, Ch 28 Procedures We Recommend Against) are drafted to the BRIEF's editorial position with sourced citations. Phase 5 reviewer pressure-testing remains the binding constraint on whether the editorial positions ship as drafted or require softening; the structural decisions hold either way.

The book is on a credible path to launch in the BRIEF's stated 11-13 week window if reviewer outreach starts now (or is already underway).
