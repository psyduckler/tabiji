# Pass 1 · Clarity & Narrative

Each check is binary (✓ or ✗). Score = (passed / total) × 10.
Threshold to pass: all ✓ except up to 1 ✗ allowed (i.e., score ≥ 9.5).

## Checks

- [ ] **Hero subhead and TL;DR card don't repeat the same claim.** (Pig-butchering v1 had this redundancy.)
- [ ] **TL;DR card body word count matches the title's time claim.** ("30-Second Version" = 60-90 words at 200wpm reading speed.)
- [ ] **Self-assessment skip-link is visually prominent** (button class, not inline text link).
- [ ] **Self-assessment verdict has a clear threshold** ("2+ yes" or similar) and a clear next action.
- [ ] **Hook story uses real verbatim Reddit content**, not Claude-narrated composite.
- [ ] **Hook section heading is specific and evocative**, not bland ("The Anatomy of a $X Loss" not "One Real Story").
- [ ] **Variant order tells a story** (entry vectors → trap mechanism → relational damage → meta-scam, when applicable).
- [ ] **Every variant ends with a transition line** to the next variant. (Last variant doesn't need outgoing transition.)
- [ ] **Variant titles are consistent in shape** (no parentheticals on some and not others).
- [ ] **TOC entries match variant titles verbatim.**
- [ ] **Severity counts in hero match TOC** (e.g., "5 High Risk · 2 Medium" matches 5 high-badge variants + 2 medium-badge variants in TOC).
- [ ] **The "Numbers" section comes BEFORE the "Recovery" section** so the reader has the scale before the impossibility-of-recovery bombshell.
- [ ] **The "Compounds" sidebar (if applicable) sits between Numbers and Recovery** — provides the "why" for recovery being impossible.
- [ ] **The "How to help someone" section sits AFTER the recovery section** — implies "you can't recover but you can prevent further deposits in others."
- [ ] **The Action Grid sits at the very end of advice content**, not buried mid-page.
- [ ] **The FAQ comes AFTER all narrative content** — it's a reference layer, not the main path.
- [ ] **Source threads section is presented as evidence**, not as a "further reading" afterthought.
- [ ] **Related Reading section links to /scams/everywhere/ siblings only** (per user spec — no city scam page links).
- [ ] **Books CTA stub is present** but doesn't overwhelm the page.
- [ ] **Legal disclaimer is the last text on the page**, before footer.

## Iteration triggers

If <9.5: identify the failed checks and fix. Re-run Pass 1 once. If still
<9.5 after one fix iteration, halt and surface to user.
