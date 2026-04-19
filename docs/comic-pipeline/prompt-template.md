# Prompt Template

Every scam comic prompt has exactly three blocks in this order:

```
{STYLE_BLOCK}

CHARACTER: {cast paragraph}

SCENE:
Panel 1: {what happens}. Speech bubble: "{dialogue}"
Panel 2: {what happens}. Speech bubble: "{dialogue}"
Panel 3: {what happens}. Speech bubble: "{dialogue}"
Panel 4: {what happens}. Speech bubble: "{dialogue}"
```

All three blocks are required. Omitting any one breaks either style lock,
character consistency, or narrative coherence.

## 1. STYLE block

Country-specific. Paste verbatim from [styles/<country>.md](styles/). See the
[style-exploration.md](style-exploration.md) guide for how to pick a new style.

Do not paraphrase. The exact wording is tuned against the model — "ancient
Greek red-figure pottery storytelling" gives the pottery look, while a
paraphrase like "Greek vase style" does not.

## 2. CHARACTER block

One of the four canonical protagonists from [cast.md](cast.md). Paste the full
paragraph verbatim — name, age, ethnicity, hair, hat, clothing, accessories,
demeanor. Do not abbreviate to "a silver-haired woman" — you need the full
60-word block for the model to render the same Margie across panels.

Character selection is by scam type — see the pairing table in [cast.md](cast.md).

## 3. SCENE block

Four panels, each with:
- **Scene description**: who is present, what action, where (with a city-specific landmark if possible)
- **Speech bubble**: short English dialogue, ideally under 8 words

### Dialogue rules

- **English only.** Even in France/Spain/Greece — the target audience is global travelers.
- **Under ~8 words per bubble.** Longer text occasionally mis-spells in Nano Banana Pro.
- **One bubble per panel.** Multi-bubble panels confuse the layout.
- **Avoid digit-heavy dialogue.** "twenty baht" renders more reliably than "20 baht". Spell out amounts under ~100.
- **Panel 4 is the lesson.** The protagonist walks away wiser, reports to Tourist Police, or demonstrates the correct alternative. This gives every comic narrative closure.

### Scene conventions

- **Panel 1**: setup — protagonist in the environment, scammer approaches (or protagonist initiates a vulnerable action: hailing a taxi, using an ATM, etc.)
- **Panel 2**: the scam mechanic — the bait, switch, distraction, or overcharge
- **Panel 3**: the realization or the pushback — protagonist notices loss, or (for "the savvy ones" like Priya) resists and calls the scam out
- **Panel 4**: the aftermath / lesson — Tourist Police, correct alternative, or direct "always [X]" advice in the dialogue

### Good example: Paris Gold Ring (Margie)

```
Panel 1: Margie strolls along the sunny Seine riverside near the Louvre
and Pont des Arts in Paris. A young woman in a dark coat bends down in
front of her, theatrically picking up a shiny gold ring from the pavement
and holding it up with a surprised smile.
Speech bubble: "Madame! Is this yours? Pure gold!"

Panel 2: The woman presses the gold ring into Margie's open palm with wide
excited eyes, her other hand on her own chest as if astonished by the find.
Speech bubble: "Too big for me — you take it!"

Panel 3: The same woman's expression shifts to pleading; she clasps her
hands together in a gentle begging gesture, eyes downcast.
Speech bubble: "A few euros for my sick child?"

Panel 4: Margie sits at an outdoor Paris cafe table with a small coffee
and a croissant, examining the ring skeptically beside her open laptop
showing a webpage headline "Brass — worth pennies," with a relieved wry
smile; the Eiffel Tower visible in the distance.
Speech bubble: "Always ask before accepting!"
```

## Reusable themed templates

For scale-ups (100+ scams across a country), writing each panel script by
hand is impractical. The pipeline uses **themed templates** — per-scam-type
skeletons that take `(city, city_display, landmark)` and produce the 4-panel
script with city-specific customization.

Example themes in current use:
- `gold_ring` → Margie: found ring → pressed → pivot → cafe realization
- `friendship_bracelet` → Marcus: tied-on string → blocked → cut with knife
- `petition_pickpocket` → Harry: clipboard → accomplice lift → Tourist Police
- `fake_police` → Harry: fake badge → refuse → real police
- `taxi_overcharge` → Priya: flat rate → app comparison → alternative
- `restaurant_overcharge` → Margie: no prices on menu → bill shock → local bistro
- `atm_distraction` → Harry: map question → PIN spied → bank report
- `shell_game` → Marcus: dealer → shill bet → loss → "no gambling" sign
- `rental_damage` → Priya: passport deposit → fake scuff → pickup photos
- `accommodation_fraud` → Priya: shabby door → unreachable host → stolen photos → verified hotel

See the country scale-up scripts (`/tmp/build_es_batch.py`, `/tmp/build_fr_batch.py`, etc.) for the full template library. Promoting a canonical `scripts/comic-pipeline/themes.py` is a future clean-up.

## What NOT to do

- ❌ Don't paraphrase the STYLE block to something shorter
- ❌ Don't abbreviate the CHARACTER block
- ❌ Don't put multiple protagonists in one comic
- ❌ Don't write dialogue in the country's language
- ❌ Don't skip Panel 4's lesson/aftermath
- ❌ Don't use digit-heavy amounts in speech bubbles
- ❌ Don't mix different style blocks in the same prompt (e.g. "watercolor with Tintin linework") — pick one country style and commit
