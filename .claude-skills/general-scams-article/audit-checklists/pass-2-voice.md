# Pass 2 · Voice & Tone

Reads against `voice-rules.md`. Each check is binary.

## Automated checks (greppable)

- [ ] Em-dash density ≤ 1.5 per 100 words of body text
- [ ] Em-dash:period ratio ≤ 0.4
- [ ] No banned phrases from voice-rules.md (literal grep)
- [ ] No banned constructions ("X is not Y, but Z" pattern ≤ 3 instances per 5,000 words)
- [ ] No diction over-reach (no word repeated 3+ times in a 1,500-word section, except domain-required terms like "scam" / "platform" / "victim")
- [ ] American English spelling consistent
- [ ] Banned tonal patterns absent

## Voice-split checks (Claude judgment)

- [ ] Hero subhead is declarative + framing, not preachy
- [ ] TL;DR card is definitional (third-person), not advisory
- [ ] Quick safety rules are imperative second-person
- [ ] Hook story is third-person narrative
- [ ] Variant story paragraphs are third-person
- [ ] Variant mechanics paragraph shifts to advisory voice
- [ ] Red flags are observable third-person ("Match pushes to..." not "You should worry when...")
- [ ] Defenses are imperative second-person ("Make a hard rule..." not "One should...")
- [ ] No first-person plural ("we") except in book CTA + footer
- [ ] No first-person singular ("I") anywhere except direct verbatim quotes

## Friend-test checks

- [ ] No paragraph would feel like a corporate compliance officer wrote it
- [ ] No paragraph would feel like an AI trying to sound smart wrote it
- [ ] Specific platform names / tools are used where appropriate (Wealth Fims, ETRDStocks — not "fraudulent platforms")
- [ ] Story before rule, not rule before story
- [ ] Victim intelligence is acknowledged ("you are not stupid, the script is engineered")
- [ ] Concrete numbers used, not vague magnitudes ("$5.8B in 2024" not "billions of dollars")

## Iteration triggers

Any banned-phrase grep hit = hard fail. Soft caps (em-dash density, hedge
words) trigger a fix iteration. After 2 fix iterations, halt to user.
