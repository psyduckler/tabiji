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
