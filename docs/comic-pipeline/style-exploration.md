# Style Exploration — Picking a New Country's Style

When a new country needs comics, pick a **culturally-anchored illustration style**
that feels uniquely tied to that place and is visually distinct from every
other country already in the set. This doc describes the process we've used
for Thailand, France, Greece, Spain, Austria, Hong Kong, and Croatia.

## Why per-country styles

A single universal comic style (e.g. clean-line cartoon everywhere) looked
generic in early tests — Thailand, Paris, Mykonos, and Kyoto all felt
interchangeable. Country-specific styles are:

- **More memorable** — each page has a visual identity that reinforces the
  place.
- **Authored-feeling** — readers sense intentional design, not template spam.
- **Culturally respectful** — the illustration tradition often *is* part of
  the country's visual heritage (Greek red-figure pottery, Japanese manga,
  French BD).

## The bake-off

For each new country, generate **5 different candidate styles** on the same
scam (one protagonist, one scam, one scene) and compare side-by-side.

### Step-by-step

1. Pick one city's scam #1 as the anchor (typically Barcelona for Spain,
   Athens for Greece, Paris for France, etc.)
2. Write the panel script once — same scene, same dialogue, same protagonist
   for all 5 candidates
3. Write 5 STYLE blocks, one per candidate illustration tradition
4. Submit all 5 via `text-to-image` endpoint in parallel
5. Upload results to R2 under `scam-comics/<cc>/style-tests/<N>-<name>.jpg`
6. Present the 5 URLs + critique to the user
7. Lock the chosen style in `styles/<country>.md`

### Candidate selection heuristics

Look for styles that are:
- **Uniquely identifiable with the country.** Not just "European flat cartoon"
  — go specific. Hergé for France, Sempé for Austria (Paris Match-era), Shaw
  Brothers for Hong Kong cinema, red-figure pottery for Greece.
- **Readable at small sizes.** Highly textured painterly styles lose
  legibility on mobile. Favor clean outlines + flat fills unless the heritage
  is specifically painterly.
- **Warm and non-threatening.** Target audience is older, slightly
  female-skewing. Avoid noir, gritty, horror, edgy.
- **Distinct from every country already in the set.** Check the matrix below
  before generating.

### Style matrix (what's already taken)

| Country | Style | Visual signature |
|---|---|---|
| Thailand | Warm watercolor storybook | Soft pastels, hand-painted texture, Thai golden sunlight |
| France | Hergé / Tintin ligne-claire | Uniform black outlines, flat bright colors, architectural detail |
| Greece | Ancient red-figure pottery | Terracotta + black silhouettes, meander borders |
| Spain | Paco Roca contemporary | Clean dark outlines + warm pastel gouache, muted cream/orange/dusty-rose |
| Austria | Jean-Jacques Sempé pen-and-ink wash | Thin scratchy ink lines + loose watercolor wash |
| Hong Kong | Shaw Brothers painted cinema poster | Bold 60s-70s cinema poster, hand-painted, vivid |
| Croatia | Hlebine School naïve-art oil-on-glass | Naïve art, folksy, painterly glass-oil technique |

### Candidate ideas for future countries

- **Japan**: manga (Akira Toriyama, Osamu Tezuka for warm; Yoshitaka Amano for fine; Taiyō Matsumoto for indie)
- **USA**: American comic book (Kirby, Romita, or indie like Cliff Chiang)
- **Italy**: fumetti / Milo Manara (maybe too spicy) / Hugo Pratt Corto Maltese
- **Germany**: Georg Grosz satirical / Neue Sachlichkeit
- **Mexico**: José Guadalupe Posada engravings / lotería card art
- **India**: Raja Ravi Varma oleographs / Amar Chitra Katha
- **Turkey**: Ottoman miniatures / Iznik tile motifs
- **Morocco**: zellige tile mosaic (similar idea to Spanish azulejo — pick one or the other)
- **Netherlands**: Delftware blue-and-white / Dutch golden-age etchings
- **Korea**: webtoon aesthetic / Joseon-era genre painting (Kim Hong-do)
- **Egypt**: hieroglyphic tomb painting (similar heritage-anchor as Greek red-figure)
- **Vietnam**: Đông Hồ folk woodblock prints

## The Spanish bake-off (worked example)

Anchor scam: Barcelona "La Rambla Pickpocket Gangs" with Margie.

| # | Style | Outcome |
|---|---|---|
| 1 | Sorolla impressionist | Luminous Valencian sunlight, very warm — good fine-art option |
| 2 | **Paco Roca contemporary** ← **CHOSEN** | Modern Spanish indie-comic, clean + humanist + quiet — best match for scam narrative pacing |
| 3 | Miguelanxo Prado painted BD | Moody earthy umbers — slightly too dark for cautionary-travel tone |
| 4 | Azulejo ceramic tile | Cobalt blue + Moorish borders — strong heritage anchor, but too similar to Greek red-figure approach (both heritage-tile moves) |
| 5 | Mariscal Mediterráneo / Cobi | Bold flat Barcelona-'92 pop — too young/loud for older demographic |

Final decision: Paco Roca, for the balance of Spanish identity, narrative pacing, and demographic fit.

## After the bake-off

Once the user approves a candidate:

1. Create `styles/<country>.md` with the locked STYLE block
2. Update the README's status table
3. Use the **approved pilot itself** as the reference image for the first `edit`-endpoint generation, then rotate in the next 2–3 comics as the country batch grows
4. Save a copy of the 5 test URLs in the country style file under "exploration history" — useful when someone asks "why did we pick X?" later
