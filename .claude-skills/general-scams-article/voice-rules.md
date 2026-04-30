# Voice Rules — for every /scams/everywhere/ page

## POV split

| Section type | Voice | Example |
|---|---|---|
| Hero subhead | Declarative, second-person framing | "$5.8B stolen from Americans in 2024." |
| TL;DR card | Definitional, third-person | "Pig-butchering is a long-con investment fraud." |
| Quick safety rules | Imperative, second-person | "If a dating-app match pushes to WhatsApp..., end the conversation." |
| Self-assessment | Direct second-person questions | "Did the conversation move from a dating app...?" |
| Hook story | **Third-person narrative** (not Claude composite — real Reddit content anonymized) | "The author is a tech worker. He matched with a woman on Hinge..." |
| Definition | Explanatory, third-person + occasional second-person | "By the time crypto enters the conversation..." |
| Variant story paragraphs | Third-person narrative | "A 28-year-old in tech matches with 'Linda' on Hinge..." |
| Variant mechanics paragraph | Advisory, second-person | "The single sentence to remember: any platform that requires you to..." |
| Red flags | Observable third-person | "Match pushes to WhatsApp within the first three messages..." |
| Defenses | Imperative, second-person | "Make a hard rule: dating-app matches who push to WhatsApp..." |
| Recovery section | Explanatory, second-person + third-person mix | "Visit the originating bank in person and ask specifically for the fraud department." |
| Action grid | Imperative + procedural | "File at ic3.gov within 24-48 hours." |
| FAQ answers | Direct, definitional | First 30 words contain the answer; rest is detail. |

## Hard anti-patterns (never use)

These are AI-generated-text tells. Pass 8 (`verify_anti_tics.py`) greps for
each. Any hit is a hard fail.

### Banned phrases (literal greps)
```
- "It's worth noting"
- "It's important to remember"
- "Ultimately"
- "essentially"          (allow ≤2 instances per 5,000 words)
- "delve" / "delving"
- "tapestry"
- "navigate the complexities"
- "it's a testament to"
- "in today's world"
- "in the digital age"
- "in this day and age"
- "at the end of the day"
- "the simple truth"
- "the bottom line"
- "rest assured"
```

### Banned constructions
```
- "X is not Y, but Z" (balanced-clause AI tic — allow ≤3 per 5,000 words)
- Em-dash density > 1.5 per 100 words
- Em-dash:period ratio > 0.4
- "Furthermore," "Moreover," "However," each capped at 2 occurrences per 5,000 words
- "On one hand... on the other hand..."
- Repeated noun-pair within 500 words ("calibrated/engineered/industrial" trio is the canonical example)
```

### Banned tonal patterns
```
- "Common sense should tell you..."
- "Anyone with half a brain..."
- "If you're stupid enough to..."
- "Of course..."  (when introducing the obvious; Claude's hedge)
- "Let me be clear..."
- Lecturing absolutes ("There is no benign continuation of...")  → soften to "There is no legitimate reason for..."
- "This is not [X]. This is [Y]." (allow once per page max)
- "Without exception, in any jurisdiction" (allow ≤2 per page)
```

### Banned cross-page formula tics (caught in 2026-04-29 corpus audit)
These are the patterns that emerged when the 5-variant template was applied
across multiple pages. Each one was caught because a careful reader hit the
same sentence-shape on two pages in one session and lost trust.
```
- "The script is one. The N masks it wears are below."
  (use a page-specific transition framed around the actual taxonomy)
- "The defense is..." as the paragraph-3 opener of every variant.
  (rotate openers across variants: imperative, question, Reddit-quote-led,
   climax-beat, structural-not-exhortative — see Variant openers below)
- "The single decision rule:" / "The single sentence to remember:" /
  "The single sentence:" — bolded-imperative formula closing every variant.
  (vary closings: direct fact-then-imperative; Reddit-quote-led; question
   that lands the answer; declarative without a labeled "rule")
```

## Variant paragraph-3 opener rotation

Every variant's paragraph 3 (the defense / what-works paragraph) used to open
with "The defense is..." across every page. Caught in the corpus audit. Going
forward, rotate openers across the variants on a single page so the reader
never hits the same construction twice in the same article. Pick from this
set:

1. **Imperative-first** — "Kill the browser via Task Manager — never via the page's own buttons."
2. **Question-led** — "So what stops it?" / "So how do you verify a verification?"
3. **Reddit-quote-led** — Open with the canonical victim or community quote and let it carry the framing.
4. **Climax-beat-led** — Lead with what happens next ("The friend who turned off Wi-Fi didn't avoid the worst because he was lucky — he avoided it because he stopped engaging within minutes.")
5. **Structural-not-exhortative** — "What works at scale is structural, not exhortative." Frame the rule as system design.
6. **Diagnostic-led** — Open on what the diagnostic signal is ("The 'social worker' intermediary is the tell.")

Use each opener at most once per page. By V5 the reader should not be able
to predict the rhythm of the defense paragraph.

## Diction variation rules

If you find yourself reaching for the same word 3+ times in a 1,500-word
section, stop and vary. The pig-butchering page had 8 instances of
"calibrated / engineered / industrial" — caught in audit, varied to:
- "built around"
- "runs at scale"
- "sized to"
- "carefully built"
- "maps to"
- "designed to"
- "written for"
- "manufactured by"

Common over-reached words to watch for:
- "calibrated" / "engineered" / "industrial" / "tuned"
- "leverages" / "leverage"
- "robust"
- "comprehensive"
- "myriad" / "plethora"
- "showcase" / "highlight"

### Diction-trio hard-cap (added 2026-04-30 from recovery-scams audit)

The combined count of **calibrated + engineered + industrial** must
stay ≤ 4 per page. `verify_anti_tics.py` enforces this as a HARD FAIL.
Recovery-scams initial draft hit 7× because "calibrated" felt natural
in scam-pattern writing ("the pitch is calibrated for...", "the script
is calibrated to...", "the most psychologically calibrated variant").

Pre-emptive rewrites — when you find yourself reaching for "calibrated":
- "the pitch is calibrated for X" → "the pitch is **written for** X"
- "the script is calibrated to X" → "the script is **built for** / **tuned to** X"
- "calibrated to feel like Y" → "**written to feel like** Y"
- "calibrated to the size of Z" → "**scales to** the size of Z"
- "the most psychologically calibrated" → "the most psychologically **loaded**"

If a page absolutely needs more than 2 instances of "calibrated", that
is a signal to vary the surrounding prose, not a signal to use the
trio cap up to its max.

## American English (en-US)

Per `docs/scam-pages-style-guide.md`:
- "color" not "colour"
- "behavior" not "behaviour"
- "labor" not "labour"
- "check" (financial instrument) not "cheque"
- "license" (verb and noun) not "licence"
- "-ize" not "-ise" (organize, recognize, realize)
- Oxford comma optional but consistent within a paragraph

Exceptions:
- Verbatim quotes from non-US Reddit users keep their original spelling
- Proper nouns keep their canonical spelling (Action Fraud, not Action Frawd; An Garda Síochána keeps the diacritics)

## Hook ↔ Variant #1 decoupling

The hook story and Variant #1's body must not be the same Reddit case.
The first major audit of the corpus caught all five pages doing this:
the hook would set up a case, then Variant #1's first paragraph would
retell it with added age/timestamp/zip-code specifics. The reader hits
the variants section already knowing the story, and engagement decays
immediately.

Rule: the hook is its own scene. Variant #1's body must be either
- a different demographic (different age, role, channel, dollar magnitude); or
- a near-miss where the page's central defense actually fires in real time
  (best option — demonstrates the rule rather than asserting it).

Examples that work:
- ai-voice-clone V1: a near-miss where "What's the safe word?" comes out
  of the mother's mouth before the social worker can finish his sentence.
- pig-butchering V1: a different victim who googles the platform name in
  week 6 and finds the Reddit thread describing her own situation.
- bank-impersonation V1: hook = Chase $5K case; V1 primary = US Bank
  variant + a $7,200 BoA loss case where the script did not break.

If you can't find a near-miss, find a different demographic. If you can't
find either, cut the variant or shrink the page to fewer variants. Do not
ship hook-recap V1.

## Tone calibration — the friend test

Before shipping any paragraph, ask: "Would a friend who has read 4,000+
Reddit threads and is genuinely trying to help me say this?"

If the answer is "no, this sounds like a corporate compliance officer" or
"no, this sounds like an AI trying to sound smart" — rewrite.

The friend:
- Never lectures
- Names specific things (Wealth Fims, ETRDStocks — not "fraudulent platforms")
- Tells the story first, gives the rule second
- Acknowledges the victim's intelligence ("you are not stupid, the script is engineered")
- Uses concrete numbers ("$5.8B in 2024") not vague magnitudes ("billions of dollars")
- Cites sources without hiding behind them
