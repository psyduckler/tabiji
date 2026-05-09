# Authoring Rules — The Scam Atlas (A–Z Field Guide)

These thirteen rules govern every chapter of the atlas book. Apply them
during drafting and during the editorial pass. The polish script
(`scripts/polish_atlas_prose.py`, ported from `book-india`) enforces the
mechanical ones. The voice rules require human judgment.

The rules exist because the source material on `/scams/atlas/` was
written for SEO and reference. Books are read linearly. Without these
rules a 65-chapter A–Z reads as 65 disconnected reference cards bound
together. With them it reads as a book.

---

## 1. Scene-open ≤ 200 words

Every chapter opens with a scene starring one of the four protagonists
(Margie 62F retiree, Priya 34F solo female traveler, Harry 64M,
Marcus 34M digital nomad) or, where none of them fits naturally, an
anonymous traveler type ("a backpacker," "a young couple," "a family
of four"). Cap the scene at 200 words. The hook of the chapter
(the bend, the price reveal, the door closing) must land before
word 60.

## 2. One literary device per scene-open

Pick one sensory anchor: light, sound, weather, smell. Not three.
"Steel-blue Seine" or "saxophonist tuning up" but not both. Save the
prose budget for what happens, not for what it looked like.

## 3. Translate every foreign term inline, the first time

The first time *bouquinistes* appears in a chapter, gloss it as
"riverside booksellers (*bouquinistes*)." Same for *plainte*,
*commissariat*, *koban*, *baksheesh*, *cambio*, *galabeya*, *ZTL*,
*FIR*, and any other non-English word. Keep the foreign term for color.
Drop the friction of readers having to Google.

## 4. Switch to "you" the moment analysis starts

The scene is "she" (Margie, Priya). The analysis is "you." That switch
is where the reader becomes the protagonist of the chapter. Don't say
"the operator does X to the tourist." Say "the scammer does X to you."

## 5. Active voice, present tense for analysis

The trick *is* brass. The bend *happens*. The script *runs*. Present
tense makes the scam ongoing, which it is. Past tense ("the trick was
brass") puts distance between the reader and the threat.

## 6. Vary paragraph length

Mix one-sentence paragraphs with three- and four-sentence builds. Every
section should contain at least one one-sentence paragraph. Without
variation, prose reads as monotonous. With variation, the page has
rhythm and the eye moves.

## 7. ≤ 25 words per sentence on average; cap maximum at 35

Some sentences run longer for variety. Most should run shorter. Long
sentences in the analytical sections kill momentum. Short sentences
in the scene-opens read as breathless.

## 8. Sentence fragments are tools, not tics

Cap at two per chapter. "Volume play." "Don't apologize." "She had
time." Used sparingly they punch. Used six times in a chapter they
become a stylistic crutch.

## 9. Replace "the operator" / "the script"

Use *the scammer*, *the trick*, *the play*, *the hustler*, *the
hustle*. The atlas page voice was journalistic. The book voice is
slightly dramatic. Less wire-service, more thriller.

## 10. Concrete numbers in headers, not vague modifiers

"Where it runs (12 cities, half in Paris)" beats "Where it runs."
"The five red flags" beats "The red flags." Reader knows the weight
before reading the section.

## 11. Reframe "If you got hit" for pre-scam readers too

Most readers haven't been scammed yet. They're reading prevention.
Open the recovery section neutral: "If this happens to you, the next
sixty minutes matter most." Don't open with "You paid the ten euros
and walked away embarrassed."

## 12. Each chapter ends on the cross-reference, not the pattern callback

Move the *Pattern: Manufactured Reciprocity* tag UP to the chapter
header (where readers see it before they read). Let the chapter close
on country-book referrals, which drives series sales.

## 13. Reduce em-dashes; prefer commas, periods, colons

Em-dashes are a literary tic that, used four or five times per chapter,
flatten into background noise and drag the prose toward essay register.
Cap at two em-dashes per chapter. Replace with:

- A comma, where the parenthetical is short and tight.
- Parentheses, where the aside is genuinely parenthetical.
- A period and a new sentence, where the aside is doing real work.
- A colon, where the second clause is a list, definition, or
  cumulative reveal.

The pattern to avoid: *"the bend — performed at exactly the right
distance from your approach — is what sells it."* The pattern to
prefer: *"What sells it is the bend, performed at exactly the right
distance from your approach."*

---

## How rules interact

Rules 1, 2, 4, 6, 8, 9, 11, 13 govern voice. Rules 3, 5, 7, 10, 12
govern structure. Voice rules are harder to enforce mechanically; they
need human reading. Structure rules can be linted.

Where a rule conflicts with itself across sections of a chapter
(e.g., Rule 1 says scene-open ≤ 200 words, but Rule 6 wants varied
paragraph length), Rule 1 wins. The scene-open is the first 200 words.
Variation lives inside that envelope.

## Per-chapter checklist (apply during editorial pass)

Before locking a chapter, verify:

- [ ] Scene-open ≤ 200 words; hook by word 60
- [ ] Pattern tag in header, not in closing
- [ ] All foreign terms glossed inline on first use
- [ ] Voice is "you" by the second section
- [ ] Present tense throughout the analytical body
- [ ] At least one one-sentence paragraph per section
- [ ] No sentence over 35 words
- [ ] No more than 2 sentence fragments
- [ ] No "operator" or "script" left from atlas-page source
- [ ] Section headers include concrete numbers where applicable
- [ ] Recovery section reads for pre-scam and post-scam audiences
- [ ] Closes on country-book cross-references
- [ ] Two em-dashes maximum
- [ ] American English (karat not carat, color not colour, etc.)

## Part II chapter template

Every chapter in Part II (the thirty A–Z entries) follows this
structure exactly. Word-count target: 1,400–1,600 per chapter.

```
# [Letter] · [Scam Name]

> **Pattern: [one of seven]** · [N mechanics] · [N countries]
> · [pricing range or impact descriptor] · *Updated [month year]*

## [Scene-open subhead — a distinctive image, not a generic header]

[Scene ≤ 200 words. Named protagonist (Margie, Priya, Harry, Marcus)
or deliberate second-person "you" for high-velocity action chapters.
Hook lands by word 60. One sensory anchor only. Foreign terms glossed
inline.]

## The trick

[The mechanic. 250–350 words. Present tense. Switch to "you" voice
the moment the analytical mode begins. Use scammer / trick / play /
hustler — never "operator" or "script." Active voice throughout.]

## The N mechanics
*(or: The N variants / The N tiers, depending on how the source
material categorizes the sub-types)*

[Each sub-variant gets a bolded label and a 50–80 word breakdown.
Include "most reported in:" geography for each sub-variant where
known. 200–350 words total for this section.]

## Where it runs (N countries, X dominant)

[Geographic distribution prose, 150–200 words. Always include the
dominant country in the header. Cover where the scam is *and* where
it isn't, with the cultural / enforcement / structural reason for
the asymmetry.]

## The five red flags

[Always bulleted, always five items, always opens with a sentence
specifying the trigger threshold ("Two or more in the first ten
seconds: change direction"). Each bullet has a one-line vivid
detail. 100–150 words total.]

## The phrases that shut it down

[Phrase table. Local-language refusal + escalation + universal
de-escalator (police). For non-verbal scams (Airbnb, online fraud),
reframe as "the messages that shut it down" with example chat
replies. 100–150 words.]

## If this happens to you

[Recovery section. Frame for both pre-scam reader (preventive) and
post-scam reader (remediation). Open with the specific scenario
that brought the reader here. Time-window structure
(immediate / first hour / first day) where applicable. 200–300
words.]

---

*[One-sentence italic cross-reference to country books that cover
this scam in destination detail. End the chapter on this line — no
zinger closer.]*
```

### Per-chapter checklist (apply during editorial pass)

- [ ] Pattern tag uses one of the seven canonical patterns. No
      invented sub-variants ("transaction variant", "social
      variant"). If the scam blends two patterns, name both.
- [ ] Scene-open ≤ 200 words; hook by word 60
- [ ] All foreign terms glossed inline on first use
- [ ] Voice is "you" by the second section
- [ ] Present tense throughout the analytical body
- [ ] At least one one-sentence paragraph per section
- [ ] No sentence over 35 words
- [ ] No more than 2 sentence fragments
- [ ] No "operator" or "script" left from atlas-page source
- [ ] Section headers include concrete numbers where applicable
      (especially "Where it runs (N countries, X dominant)")
- [ ] Recovery section reads for pre-scam and post-scam audiences
- [ ] Closes on the country-book cross-reference, not a moralizing
      one-liner
- [ ] Two em-dashes maximum (cap from rule 13)
- [ ] American English (karat not carat, color not colour, etc.)
- [ ] Protagonist (if named) returns at the closer with a 2-sentence
      callback. Anonymous "you" chapters do not need a callback.
- [ ] No phrase repeats from the previous chapter (especially
      "ninety seconds," "the same script," numerical-mnemonic
      closers)

### The seven patterns

Every chapter tags exactly one. If the scam genuinely blends two
patterns, name both in the tag separated by a slash (e.g., *Pattern:
Manufactured Reciprocity / Captive-Position Lever*). Do not invent
sub-variant labels.

1. **The Captive-Position Lever** — physical capture (boat, taxi,
   shop) then price reveal.
2. **The Authority Costume** — uniform-mimicry by an unauthorized
   actor.
3. **The Sub-Market Quote** — too-cheap quote as bait into a
   captive-position trap.
4. **The Commission Detour** — third-location detour with
   kickback chain.
5. **The Made-Up Closure** — fabricated unavailability with a
   conveniently-ready alternative.
6. **The Brand-Mimicry Storefront** — look-alike entity (storefront,
   website, ATM, lanyard) impersonating a real one.
7. **Manufactured Reciprocity** — unsolicited gift or favor
   creating debt-by-acceptance.

## American English baseline

The book is written in American English. The polish script catches the
common British-spelling and British-vocabulary leakages. Hand-author
with the substitutions below.

| Don't write | Write |
|---|---|
| paces, pace ahead | steps, step ahead |
| carats (when discussing gold purity) | karats |
| amongst, whilst | among, while |
| learnt, spelt, dreamt, burnt | learned, spelled, dreamed, burned |
| travelled, cancelled, modelled | traveled, canceled, modeled |
| behaviour, colour, neighbourhood, favourite, centre, metres, theatre | behavior, color, neighborhood, favorite, center, meters, theater |
| tyre, kerb, lift (elevator), flat (apartment) | tire, curb, elevator, apartment |
| organise, realise, recognise, criticise | organize, realize, recognize, criticize |
| programme (general), defence, offence | program, defense, offense |
| cheque (bank) | check |
| queue (the line) | line, in line |
