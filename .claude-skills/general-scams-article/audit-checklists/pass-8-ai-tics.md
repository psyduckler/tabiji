# Pass 8 · AI-Tic Detection (automated)

Hard-coded greps and ratio checks. Fully automated via
`helpers/verify_anti_tics.py`. Any failure = hard fail; no Claude judgment.

## Em-dash density

- [ ] Em-dash count / (body word count / 100) ≤ 1.5
- [ ] Em-dash count / sentence count ≤ 0.4

## Banned phrases (case-insensitive grep)

```
"It's worth noting"
"It's important to remember"
"At the end of the day"
"In today's world"
"In the digital age"
"In this day and age"
"Rest assured"
"The bottom line"
"The simple truth"
"It's a testament to"
"Navigate the complexities"
"Tapestry"
"Delve" / "Delving"
"Let me be clear"
"Of course," (when used as hedge — flag for human review)
```

Each match = 1 violation. Threshold: 0 violations allowed.

## Soft-banned phrases (count caps)

| Phrase | Max per 5,000 words |
|---|---|
| "essentially" | 2 |
| "ultimately" | 2 |
| "Furthermore," | 2 |
| "Moreover," | 2 |
| "However," | 4 |
| "Indeed," | 2 |

## Banned constructions

- [ ] "X is not Y, but Z" balanced-clause pattern ≤ 3 occurrences per 5,000 words
- [ ] "On one hand... on the other hand..." 0 occurrences
- [ ] "This is not [X]. This is [Y]." pattern ≤ 1 per page
- [ ] "Without exception, in any jurisdiction" ≤ 2 per page

## Diction over-reach

For each canonical AI noun pair:
- [ ] "calibrated" + "engineered" + "industrial" trio: total ≤ 4 per page (was 8 in pig-butchering v1)
- [ ] "leverages" / "leverage" ≤ 1 per page
- [ ] "robust" ≤ 2 per page
- [ ] "comprehensive" ≤ 2 per page
- [ ] "myriad" / "plethora" 0 occurrences
- [ ] "showcase" / "highlight" 0 occurrences (use specific verbs)

## Reading level

- [ ] Flesch Reading Ease ≥ 50 (intermediate-readable)
- [ ] Average sentence length: 12-22 words
- [ ] Sentence-length standard deviation > 5 (avoid AI's monotone rhythm)
- [ ] Paragraph length: 50-200 words (AI loves the 50-word paragraph; mix it up)

## Hedge density

- [ ] "essentially" + "ultimately" + "arguably" + "largely" + "primarily" + "fundamentally" combined ≤ 8 per 5,000 words

## Tonal patterns (Claude judgment, manual)

These can't be greppped reliably; flag for human review:
- [ ] No paragraph sounds preachy
- [ ] No paragraph sounds like a corporate compliance officer wrote it
- [ ] No paragraph sounds like an AI trying to sound smart wrote it
- [ ] No "I see what you did there" cleverness
- [ ] No "let me explain" / "let me unpack" condescension
