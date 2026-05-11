# The Dental Tourism Field Guide — Designer & Typesetting Brief

**Companion document to:** `the-dental-tourism-field-guide-COMPLETE.md`
**Audience:** Print and ebook designer / typesetter
**Goal:** Translate a 50,000-word patient-protection field guide into a usable, scannable, screenshot-friendly book for stressed readers who often open it in panic.

This document is not part of the manuscript. Do not include any of it in the printed book.

---

## 1. Voice and tone the design must support

The manuscript voice is **calm, authoritative, protective**. The reader is often in a high-stress moment — they may have just received a surprise dental quote, may be about to send a deposit, may be standing in a foreign airport with a swollen jaw. The design should reduce stress, not add to it.

**Avoid:** sensational red banners, fear-marketing typography, busy infographics, dental-cliché imagery (smiling models, white teeth close-ups, "before/after" mockups).

**Favor:** generous white space, calm color palette, clear hierarchy, large body type for readability under fatigue, scannable subheads, marginal navigation cues.

---

## 2. Recurring structural elements that need visual treatment

These elements appear repeatedly throughout the manuscript and should each have a consistent, recognizable visual treatment so a returning reader can spot them by glance.

### 2.1 Composite Scenarios

Twelve composite patient scenarios appear, labeled A through L. They open most chapters and serve as narrative anchors.

- **Visual treatment:** Tinted background panel or shaded sidebar treatment that visually separates them from the surrounding instructional text. A small consistent symbol or icon on the corner (e.g., a quote-mark or "person" glyph) identifies them at a glance.
- **Purpose:** Skimmers should be pulled into the chapter by the scenario, then handed off to the chapter's instructional content.
- **Locations in manuscript:** Search for `### Composite Scenario A:` through `### Composite Scenario K:` (eleven within chapters) and `# Composite Scenario L —` (one standalone before the Final Note).

### 2.2 Decision Gates

These appear as `### Decision Gate: …` headings (in Chapters 1–4) and as `**Decision Gate**` bold labels (in Chapters 7–12 and 13). They are decision-point pause cues for the reader.

- **Visual treatment:** A consistent boxed/bordered treatment, perhaps with a stop-sign icon or a "🛑" equivalent glyph rendered in the design's icon family. Distinct from the scenario panels and from pull quotes.
- **Purpose:** A reader skimming for "what should make me stop?" can find these instantly.

### 2.3 Green / Yellow / Red Flags

Five chapters in Part III (and selected later chapters) include trichromatic flag lists: Green flags, Yellow flags, Red flags.

- **Visual treatment:** Color-coded by flag — green, yellow, red — but in restrained, accessible tones (avoid stoplight-poster intensity). Bullets or small dot marks in the matching color preceding each item. A returning reader should be able to visually scan and find "Red flags" sections from across a page spread.
- **Locations in manuscript:** Search for `### Green, Yellow, and Red Flags:` (5 instances), `### Red Flags Before Deposit` (1 instance), and `### Red Flag: …` headings in Chapter 16 (6 instances).
- **Accessibility:** Make sure color is not the only carrier of meaning — the words "Green flags," "Yellow flags," "Red flags" should remain.

### 2.4 Pull quotes (5 locations marked in manuscript)

Five sentences are flagged with `<!-- PULL QUOTE — designer: … -->` HTML comments immediately after the source sentence in the manuscript. Each should be set as a large centered sidebar callout on the relevant page or spread.

Marked pull quotes are:

1. **"Hope is important. It is not enough to sign consent."** — front matter, end of the 20-Minute Safety Pause section.
2. **"The moment you feel rescued is the moment to ask better questions."** — closing line of Chapter 1.
3. **"A lifetime warranty with no written terms is not a warranty; it is a slogan."** — Chapter 12.
4. **"A patient who can be pressured in chat can be pressured in the chair."** — Chapter 16.
5. **"Cheaper dental work is only cheaper when you can finish it well."** — Part II close (end of Chapter 14).

These should also appear on the back-cover copy and any social-media promotional graphics — they are the book's signature lines.

### 2.5 Scripts and message templates

Many chapters include word-for-word scripts the reader is meant to copy, paste, and send. They appear inside markdown blockquotes (`>`).

- **Visual treatment:** Distinct from pull quotes. A monospace or alternate font, perhaps in a tinted box that signals "this is for you to use, not just to read." A small icon (envelope, copy-paste mark) helps.
- **Purpose:** The reader should be able to take a phone photo of one and send it to a clinic without typing.

### 2.6 Checklists and worksheets in chapters

Chapters contain checklists with `☐` (empty checkbox) marks. The back matter contains 15 reusable worksheets that mirror many of these.

- **Visual treatment:** Real checkbox graphics, large enough to actually tick on paper. Generous line spacing.
- **Cross-reference fix:** Throughout the manuscript, italicized notes appear like *"A reusable copy is Worksheet 4 in the back matter."* During typesetting, **replace each "in the back matter" with the actual page number** (e.g., "on page 247"). Search the manuscript for `Worksheet [0-9]\+ in the back matter` (13 instances) and update each.

### 2.7 The Journey Map (Introduction)

A table titled **"The Journey at a Glance"** appears in the Introduction (Seven Leverage Points section). It contains an HTML comment specifying that the designer should render it as a horizontal flow / visual timeline graphic, not as a plain table.

- **Visual treatment:** A facing-page or full-page horizontal flow showing the ten stages left-to-right, with the "Leverage" line above (high → low → recovering), the worksheet references below, and irreversible-decision moments marked distinctly.
- The plain table beneath the comment is the data; the visual is the deliverable.
- This is one of the most important diagrams in the book — readers will photograph it and share it.

---

## 3. Front-matter structure

The book opens with deliberate sequencing. Preserve the order:

1. Title page
2. Subtitle paragraph
3. **Contents** (full TOC, generated)
4. **Note to the Reader** — warm, emotional opening
5. **Important Disclaimer** — legal scope
6. **How This Book Makes Money** — business-model transparency
7. **The Five Rules** — five principles
8. **Read This First: The 20-Minute Safety Pause** ← critical: should be visually distinct, almost a tabbed "emergency" section. Consider an edge marker or thumb-tab on the page edges so a panicked reader can find it by feel. The TOC line for this section is bolded with an arrow hint and should keep that visual emphasis.
9. **Scenario Index** — quick reference to all 12 composites
10. **Introduction: The Seven Leverage Points** — chapter-spine introduction with the Journey Map

The 20-Minute Safety Pause is the single most-likely-to-be-screenshotted section in the entire book. Treat it accordingly.

---

## 4. Back-matter structure

After the Final Note:

1. Back Matter title page
2. **How to Use This Back Matter** — instructions
3. **Worksheets and Scripts (1–15)** — each worksheet starts on a new page, with full-page real estate so the reader can write on them. Worksheets are the second-most-likely-to-be-screenshotted content (after the 20-Minute Pause).
4. **Glossary**
5. **Source Notes and Further Reading**
6. **About Tabiji**
7. **About the Editor** *(needs additional bio detail from Bernard before final layout — see Section 7.4)*
8. **Acknowledgments**
9. **Appendix Disclaimer**

---

## 5. Specific designer notes embedded in the manuscript

The manuscript contains the following HTML comments that are designer instructions, not content. Strip them all from the printed text but follow each instruction:

- `<!-- PULL QUOTE — designer: … -->` — 5 instances (Section 2.4 above)
- `<!-- DESIGNER: render this as a single-page visual timeline / flowchart … -->` — 1 instance (the Journey Map, Section 2.7 above)

Search and remove pattern: `<!-- ` … ` -->` from the typeset output.

---

## 6. Cross-references that need page-number substitution

Replace each italicized phrase with the actual print page number during typesetting:

| Search pattern | Replace with |
|---|---|
| *"is Worksheet 2 in the back matter"* | *"is Worksheet 2 on page X"* |
| *"is Worksheet 3 in the back matter"* | *"is Worksheet 3 on page X"* |
| *"is Worksheet 4 in the back matter"* | *"is Worksheet 4 on page X"* |
| *"is Worksheet 5 in the back matter"* | *"is Worksheet 5 on page X"* |
| *"is Worksheet 6 in the back matter"* | *"is Worksheet 6 on page X"* |
| *"is Worksheet 7 in the back matter"* | *"is Worksheet 7 on page X"* |
| *"is Worksheet 8 in the back matter"* | *"is Worksheet 8 on page X"* |
| *"is Worksheet 9 in the back matter"* | *"is Worksheet 9 on page X"* |
| *"Worksheet 10 (Plan Change Script) from the back matter"* | *"Worksheet 10 (Plan Change Script) on page X"* |
| *"is Worksheet 11 in the back matter"* | *"is Worksheet 11 on page X"* |
| *"is Worksheet 12 in the back matter"* | *"is Worksheet 12 on page X"* |
| *"is Worksheet 13 in the back matter"* | *"is Worksheet 13 on page X"* |
| *"Worksheet 14 (Emergency Contact Sheet) in the back matter"* | *"Worksheet 14 (Emergency Contact Sheet) on page X"* |

---

## 7. Items still pending before final layout (not designer's responsibility but flagging here)

### 7.1 About the Editor expansion

The current "About the Editor" section is a deliberately conservative scaffold. **Before final layout, Bernard Huang should expand this with personal credentials, prior work, and any author-photo or contact information desired.** The designer will need final copy and (if used) a headshot at print resolution.

### 7.2 Endorsement blurbs

The book has no front-matter blurbs/endorsements yet. Design should leave space (typically a 2-page front-matter spread) for 3–6 named blurbs to be inserted before final printing. Suggested blurb sources: a prosthodontist, a consumer-health journalist, a travel-medicine professional.

### 7.3 ISBN / Library of Congress data

Standard publication data block on the copyright page — not yet included in the manuscript. Designer to add per publisher convention.

### 7.4 Author photo (optional)

If used, request from Bernard at print-quality resolution (300dpi minimum at intended print size, sRGB color space).

---

## 8. Format-specific considerations

### Print

- Recommended format: 6×9" trade paperback (industry-standard for self-help / consumer-protection books).
- Estimated extent: 280–340 pages depending on typesetting choices, scenario callout box sizes, and worksheet layout.
- Worksheet section: consider a slightly heavier paper stock or a thumb-tab system for the worksheets so they survive being written on and flipped through.

### Ebook (EPUB / Kindle)

- All HTML designer comments must be stripped.
- Pull quotes can be styled as block quotes with larger font; sidebar callouts do not translate well to reflowable formats — stack them inline.
- The Journey Map table renders as a regular table in ebook (acceptable fallback); the print version gets the visual flowchart treatment.
- Worksheets in ebook should remain as rendered text for accessibility; offer the companion-site PDF as the writable version (`tabiji.ai/book/dental`).

### Audiobook (if produced)

- Skip the worksheets, the Journey Map table, and the Scenario Index in narration — direct listeners to the companion site for those.
- Pull quotes can be subtly emphasized by the narrator's pacing; do not announce them.

---

## 9. Final QA before press

- [ ] All `<!-- … -->` HTML comments removed from typeset text.
- [ ] All "Worksheet N in the back matter" replaced with "Worksheet N on page X."
- [ ] All composite scenarios in consistent sidebar treatment.
- [ ] All Decision Gates in consistent treatment.
- [ ] All Green/Yellow/Red flag sections color-coded with words preserved for accessibility.
- [ ] Pull quotes set in oversized centered display style on their respective spreads.
- [ ] Journey Map rendered as a visual flowchart, not the plain table from the source.
- [ ] About the Editor expanded with final bio content from Bernard.
- [ ] Endorsement blurb pages laid out (even if blurbs are still pending).
- [ ] Companion site URL (`tabiji.ai/book/dental`) verified as live.
- [ ] Edge / thumb tab for the 20-Minute Safety Pause page, if format allows.

---

*This brief is a working document. Send questions, ambiguities, or design-system tradeoffs back to the editor for resolution before press.*
