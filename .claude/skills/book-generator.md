---
name: book-generator
description: Package a country's scam JSON data into a complete, publish-ready Tabiji Travel Safety Series Kindle + paperback book (EPUB + paperback interior PDF with TOC page numbers + KDP wraparound cover PDF + Kindle cover JPG). Trigger when the user says "build book for <country>", "package <country> as a book", "book-generator <country>", or "turn <country> scams into a book". Follows the 10-phase playbook proven across Japan, Italy, France, Thailand, Spain, Vietnam, China, Indonesia, Canada, and Turkey.
user_invocable: true
---

# Book Generator — Tabiji Travel Safety Series

Package a country's scam data into a complete, publish-ready Kindle + paperback book.

## When to use

- User says "build book for <country>", "package <country> as a book", "book-generator <country>", or any variant
- User pastes a country name with a verb like "turn into a book" or "make ready for Kindle"
- Triggering this skill commits to the full 10-phase workflow below — do not truncate early
- Reference implementations: `book-spain/`, `book-china/`, `book-turkey/` are the gold standards

## Required input

A country slug / name. Examples: `germany`, `mexico`, `portugal`, `greece`, `south-korea`. From the country name, derive:
- `<country>` slug (lowercase, hyphens): used for directory names (`book-<country>/`, `books/<country>-tourist-scams/`)
- ISO 2-letter country code (`DE`, `MX`, `PT`, `GR`, `KR`): used to filter `api/v1/scams/*.json`
- Display name with proper capitalization and diacritics for the book title

## Reference volumes (already shipped — study these)

| Vol | Country | Cities | Scams | Pages | Notes |
|---|---|---|---|---|---|
| 1 | Japan | 9 | 60 | — | Original template |
| 2 | Italy | — | 149 | — | — |
| 3 | France | 16 | 191 | 287 | — |
| 4 | Thailand | 11 | 67 | 220 | First xelatex PDF with TOC page numbers |
| 5 | Spain | 16 | 103 | 358 | `book-spain/` — canonical reference |
| 6 | Vietnam | 11 | 66 | 282 | Đông Hồ woodblock comics |
| 7 | China | 16 | 98 | 328 | `book-china/` — Mainland only; HK/Macau separate volumes |
| 8 | Indonesia | 12 | 73 | 328 | Balinese Lontar palm-leaf comics |
| 9 | Turkey | 13 | 78 | 268 | `book-turkey/` — Added build-time ₺→TL currency normalizer |
| 10 | Canada | 12 | 75 | — | Drawn & Quarterly indie-comic style |

## Critical technical requirements (MUST be satisfied in every book)

1. **TOC page numbers in paperback PDF** — use `pandoc --pdf-engine=xelatex`, NOT Chrome headless. Chrome's `target-counter(attr(href), page)` is unsupported.
2. **Running-head fix** — unnumbered chapters (`{-}`) need the `\@schapter` LaTeX override in `templates/header-includes.tex`, otherwise the last city's name bleeds into the appendices.
3. **Rsvg-convert 2.62+ silently drops absolute-path images** — embed SVG `<image href>` as base64 data URIs at compose time.
4. **Country-specific currency symbols may be missing from Arial Unicode MS** (Turkish ₺, Indian ₹, Bangladeshi ৳, etc.). Add a build-time normalizer in `build.py` that replaces the symbol with its ASCII abbreviation (TL, Rs, Tk) when needed.
5. **Paperback spine math**: `spine = pages × 0.0025"` for cream paper, `pages × 0.002252"` for white. Wraparound = `0.25" + 2×6" + spine` (width) × `9.25"` (height) for 6×9 trim with 0.125" bleed.
6. **Kindle cover**: 1600×2560 JPG, ~300 dpi, ~1.6:1 aspect ratio.

## Full Workflow (10 phases)

---

### PHASE 1 — SETUP

1. Sync the worktree: `git fetch origin main && git merge origin/main --no-edit`
2. Inventory the country's scam data:
   ```python
   # List all api/v1/scams/*.json with countryCode == <ISO>
   # Tally scam counts per city
   # Print total scams + city count
   ```
3. Verify comic availability on R2 by HEAD-ing `https://img.tabiji.ai/scams/<slug>/scam-<N>.jpg` for each scam. Comics should be 100% present for countries that went through the country-hub rollout.
4. Scaffold `book-<country>/`:
   ```bash
   mkdir -p book-<country>/{manuscript,scripts,templates,assets/{cities,images,covers,svg},build}
   ```
5. Copy reference scripts **from the skill's `templates/` folder**, NOT from any shipped `book-X/` (see gotcha #19). Shipped books are frozen at their ship date and may carry pre-fix scripts (book-turkey's LaTeX header, for example, predates gotcha #18's fancyhdr + KDP-gutter fix). The canonical versions live in:
   ```bash
   BG=book-<country>
   cp .claude/skills/book-generator/templates/scripts/build.py.template                       $BG/build.py
   cp .claude/skills/book-generator/templates/scripts/build_paperback_interior.py.template    $BG/scripts/build_paperback_interior.py
   cp .claude/skills/book-generator/templates/scripts/build_paperback_cover.py.template       $BG/scripts/build_paperback_cover.py
   cp .claude/skills/book-generator/templates/scripts/polish_scam_prose.py.template           $BG/scripts/polish_scam_prose.py
   cp .claude/skills/book-generator/templates/scripts/gen_city_illustrations.py.template      $BG/scripts/gen_city_illustrations.py
   cp .claude/skills/book-generator/templates/scripts/gen_comics.py.template                  $BG/scripts/gen_comics.py
   cp .claude/skills/book-generator/templates/build-templates/style.css                       $BG/templates/style.css
   cp .claude/skills/book-generator/templates/build-templates/header-includes.tex             $BG/templates/header-includes.tex
   ```

   **Verify the copy took the fix:** `grep -c "fancyhdr\|xurl" $BG/templates/header-includes.tex` must return ≥ 2. `grep -c "geometry:inner\|classoption=twoside" $BG/scripts/build_paperback_interior.py` must return ≥ 2. If either is 0 you got the wrong source — re-copy from the skill templates.

**Kick off parallel work immediately:** the scam-comic download (Phase 2.3) and the city-illustration generation (Phase 2.4) are both long-running and should run as background processes while you write the manuscript in Phase 3.

---

### PHASE 2 — GENERATE ASSETS

1. Write `book-<country>/config.yaml`:
   ```yaml
   title: "<Country> Tourist Scams 2026"
   subtitle: "<N> Real Scams Across <flagship-city-1>, <flagship-city-2>, <flagship-city-3> & <N-3> More Cities — Drawn from <country-adjective> News Reports and Tourist Police Records"
   author: "The Tabiji Team"
   publisher: "Tabiji"
   language: en-US
   rights: "Copyright (c) 2026 Tabiji. All rights reserved."
   description: >
     Don't lose $<dollar-threshold> in <country>. This book documents <N> tourist scams
     across <city-count> <country-adjective> cities... [150-300 words]
   cities:
     - <slug-1>    # flagship city first
     - <slug-2>
     # ... in narrative reading order (e.g., capital → coast → islands → inland)
   scam_data_dir: ../api/v1/scams
   output_dir: build
   output_filename: <country>-scams
   ```

2. Customize `book-<country>/build.py`:
   - Set `CITY_ALT_TEXT` dict: slug → screen-reader-friendly one-liner for each city (used in EPUB + PDF)
   - Set `city_display_name()` DISPLAY dict: slug → display name with proper accents (Málaga, İzmir, Xi'an, Kuşadası, Kyōto, etc.)
   - If the country's currency symbol is NOT in Arial Unicode MS, add a `_normalize_currency()` function and call it in `assemble_markdown()`. See `book-turkey/build.py` for the Turkish lira ₺→TL example.
   - Update the TODO placeholder comment (`Policía Nacional comisaría` etc.) to the country's equivalent.
   - **The polish module must be wired up.** Copy `templates/scripts/polish_scam_prose.py.template` to `book-<country>/scripts/polish_scam_prose.py`. Confirm the build.py has `sys.path.insert(0, str(HERE / "scripts"))` + `from polish_scam_prose import polish_description, polish_avoidance, polish_location`, and that `scam_md()` calls `polish_description(scam["description"])` etc. before the `parts.extend([...])` render. Without this step the EPUB will render `(comments/HASH)` fragments inline and run-on single-paragraph descriptions. See gotcha #16.

3. **Download comics from R2** (parallelizable, takes ~1-2 minutes):
   ```python
   # For each city in config.cities:
   #   For each scam index 1..N:
   #     Download img.tabiji.ai/scams/<slug>/scam-<N>.jpg → book-<country>/assets/images/<slug>/<NN>.jpg
   ```

4. **Generate city illustrations via Wavespeed** (long-running, ~10-15 min background):
   - Write `scripts/gen_city_illustrations.py` — copy `.claude/skills/book-generator/templates/scripts/gen_city_illustrations.py.template` into `book-<country>/scripts/` and replace the `CITIES` list with `[(slug, subject-prompt, gender)]` tuples for the new country.
   - Each prompt: 2-3 sentences describing an iconic landmark or scene for that city, with warm-light/cream-palette framing consistent with the rest of the series.
   - Gender alternates m/f across the city reading order.
   - Style block (shared across series, do not change):
     ```
     Flat vector travel-poster illustration in mid-century style. Warm cream
     background, palette of saffron-gold, deep burgundy, dusty purple and
     muted teal. Soft golden-hour light. Clean geometric shapes, visible
     paper-grain texture, no text, no words, no logos, no watermark. Square
     1:1 composition, gentle depth, soft shadows.
     ```
   - Each illustration: one "stylised solo traveler in deep-burgundy jacket with small backpack" figure (alternating m/f)
   - Run: `PYTHONUNBUFFERED=1 python3 book-<country>/scripts/gen_city_illustrations.py` in the background

5. **Generate front + back cover art via Wavespeed** (long-running, ~4-6 min background):
   - Write `scripts/gen_comics.py` — copy `.claude/skills/book-generator/templates/scripts/gen_comics.py.template` into `book-<country>/scripts/` and rewrite the `COVERS` list.
   - **Front cover MUST include ALL six elements** (gotcha #23 — Malaysia Vol 17 shipped without these and KDP cover-QA flagged it):
     1. A clearly-female-or-male tourist figure (matches one of the 4 canonical cast: Margie 62F, Priya 34F, Harry 64M, Marcus 34M). Specify hat/suitcase/posture.
     2. A scam perpetrator in a recognizable role (taxi tout, vendor, "free photo" guide, etc.).
     3. A speech bubble with the *actual scam-line in English* (e.g., "Meter rosak — RM 250, special airport rate", "Free photo, just one minute!", "Plus airport top-up — eighty-five mate").
     4. A recognizable local landmark in the background.
     5. Generous empty sky / negative space in the upper third for title overlay.
     6. A darker band across the lower fifth for hook overlay.
     **Read the prompt aloud before submitting.** If it only describes a landmark or vista, rewrite it — the prompt must describe a scene where someone is being scammed *right now*. References: `book-turkey/scripts/gen_comics.py` Sultanahmet shoe-shine, `book-egypt/` Giza camel-handler, `book-australia/` Sydney taxi-tout.
   - **Back cover**: a moody atmospheric 2:3 scene of the destination (bazaar, market, old town, harbor at evening) with substantial upper-area negative space for copy overlay. No characters, no speech bubble.
   - Style block (shared across series, do not change):
     ```
     Watercolor-storybook illustration in soft hand-painted lines, pastel
     palette with warm cream and muted saffron background, gentle shading.
     Matches a travel-safety book interior illustration style. English text
     in speech bubbles must be clear, grammatically correct, and legible.
     No logos, no watermarks, no signatures.
     ```
   - Run: `PYTHONUNBUFFERED=1 python3 book-<country>/scripts/gen_comics.py` in the background

6. **Pick `bleed_colors` AFTER the cover art renders, not during scaffolding** (gotcha #24 — Malaysia shipped with a marigold/teal Yusof-Gajah-flag pair that clashed against the eventual Peranakan-pastel watercolor):
   Once front.jpg + back.jpg exist, view them and pick a 2-color gradient that synergizes with the dominant tones — *not* generic country-flag colors. Top color = deeper version of the warm tones (sky/sunset). Bottom color = deeper version of the cool tones (foreground/landmarks). Both saturated enough that cream spine title (`#F5E9D3`) reads against the mid-band.
   ```yaml
   bleed_colors:
     - "#xxxxxx"   # top — describe (e.g., "heritage rose terracotta")
     - "#xxxxxx"   # bottom — describe (e.g., "deep Peranakan teal")
   ```
   Reference palettes shipped: Egypt `#C9A24A → #1F4E6B` (sand-gold → Nile-blue), Australia `#1B7FA8 → #E8A454` (harbor-sky → ochre), Malaysia `#C68870 → #2F5E5A` (rose terracotta → Peranakan teal).

---

### PHASE 3 — WRITE MANUSCRIPT

Write the manuscript files WHILE the Wavespeed generations run in the background. The build tools don't need illustrations to validate structure, so you can build+rebuild multiple times.

Every country has **9 front/back-matter files + N city intros**:

| File | Purpose | Word count |
|---|---|---|
| `01-copyright.md` | Copyright + disclaimer + emergency numbers one-liner | ~250 |
| `02-introduction.md` | "How to Use This Book" — hook, framing, book structure | ~800 |
| `03-red-flag-patterns.md` | The 6 universal patterns + country-specific examples | ~2,500 |
| `04-cities-section.md` | "The Scams: City by City" opener + one-paragraph glance at each city (includes `<!-- CITIES -->` marker) | ~1,500 |
| `cities-<slug>-intro.md` × N | One per city, 400-500 words each | ~400-500 each |
| `90-appendix-phrase-card.md` | Exit-phrase card in the country's language | ~2,000 |
| `91-appendix-recovery.md` | Post-scam recovery playbook (15 min / 1 hour / 24 hours / 1 week) | ~2,000 |
| `92-appendix-contacts.md` | Emergency numbers, tourist police desks, hospitals, embassies | ~2,500 |
| `95-about.md` | About Tabiji section | ~200 |
| `99-cta.md` | Stay safe + CTA to leave an Amazon review | ~250 |

**Every file MUST use `{-}` on front/back-matter headings** (copyright, how-to-use, six-patterns, appendices, about, CTA) so LaTeX treats them as unnumbered. City chapters are numbered (no `{-}`).

**The `<!-- CITIES -->` marker in `04-cities-section.md` is critical** — `build.py` inserts city chapters there. Place it after the city glance paragraphs but inside the same document.

**Voice rules** (apply consistently across every chapter):
- American English (realize, color, traveling — not realise, colour, travelling)
- No AI-isms: no "delve," "bustling," "nestled," "vibrant tapestry," "in today's world," "navigate the landscape"
- Numbered, specific, sourced: cite country-specific press outlets by name, link to a named street or venue, give a dollar/currency amount
- Warm but dry. Respect the reader. No smugness.
- Italicize foreign-language terms on first mention: `*denuncia*`, `*pàichūsuǒ*`, `*dolmuş*`, `*hoş geldiniz*`

**City intro structure** (follow for every city):
1. Opening paragraph: what the city is known for + its scam ecosystem intensity + the 2-4 corridors where risk concentrates
2. "The <signature-scam-name> is the volume risk..." — full paragraph narrating the top scam
3. "The risk radiates out in three corridors..." — three more scam vignettes, each named and with a dollar/currency amount (this phrase is a series tic, fine to reuse; vary phrasing if a country already uses it 3+ times in the same chapter)
4. "A safe default: ..." — single paragraph summarizing transit, payment, shop, emergency-number defenses, including the local Tourist Police / police desk address

---

### PHASE 4 — COPYEDIT (5 PASSES)

Run these as a single Python diagnostic script that scans `book-<country>/manuscript/*.md`:

**Pass 1 — Typography**
- Double-hyphens `--` inside words (should be em-dash `—` via pandoc `+smart`, but verify)
- Triple dots `...` (acceptable for markdown; ellipsis converted by pandoc)
- Double-spaces in prose
- Tab characters (should be zero)
- Bare hyphens in numeric ranges (e.g., `300-400 RMB` should be `300–400 RMB` with en-dash; `pandoc +smart` does NOT convert these, so the build script's `_normalize_currency()` must handle them OR sweep the manuscript

**Pass 2 — AI-isms + content padding**
Flag every instance of:
```
delve, delving, navigating the landscape, in today's world,
it's important to note, in the realm of, embark on, unveil,
plethora, tapestry, myriad, kaleidoscope, in essence,
moreover, furthermore, ultimately, in conclusion,
seamless, bustling, nestled, enchanting, vibrant,
culturally rich, hidden gem
```

**Pass 3 — British → American English**
```
realise → realize, organis → organiz, colour → color, favour → favor,
neighbour → neighbor, behaviour → behavior, defence → defense,
centre → center, metre → meter, travelling → traveling,
cancelled → canceled, whilst → while, amongst → among,
towards → toward, learnt → learned
```

**Pass 4 — Country-specific terminology**
- Verify accents on place names (Málaga, São Paulo, Kraków, Düsseldorf, etc.)
- Verify foreign-language terms are italicized on first mention
- Verify country name convention (Türkiye vs Turkey; Myanmar vs Burma; Côte d'Ivoire)

**Pass 5 — Structural**
- Every `[0-9][0-9]-*.md` has a top-level `#` heading
- Front/back-matter headings use `{-}`
- `04-cities-section.md` contains `<!-- CITIES -->` marker
- No city-intro file has a top-level `#` (build.py adds it)

Apply all findings before proceeding.

---

### PHASE 5 — BUILD ARTIFACTS (INITIAL)

1. Build EPUB:
   ```bash
   python3 book-<country>/build.py
   # → book-<country>/build/<country>-scams.epub
   ```
   Verify: word count ~40-70k, scam count matches config, 0 TODOs remaining.

2. Build paperback interior PDF with xelatex:
   ```bash
   export PATH=$PATH:/Users/bjh/Library/TinyTeX/bin/universal-darwin
   python3 book-<country>/scripts/build_paperback_interior.py
   # → book-<country>/build/<country>-scams-paperback.pdf
   ```
   Verify with `pdfinfo`: page count typically 200-360 depending on scam density.

3. Verify TOC page numbers are present:
   ```bash
   /opt/homebrew/bin/pdftotext -layout -f 3 -l 6 book-<country>/build/<country>-scams-paperback.pdf -
   # Should show: "Contents" heading + each chapter with its page number
   ```

4. Confirm the illustrations and covers have finished generating. If not, wait for them.

5. Build Kindle cover (generated automatically by `render_cover()` in build.py from `assets/svg/front.svg` + the Wavespeed art at `assets/covers/front.jpg`). The SVG composes the title/subtitle/stat badge text overlays over the Wavespeed-generated cover art.

   **Cover-art verification (BLOCKING — silent failure mode, see gotcha #20):** confirm the SVGs actually embed the artwork and the rendered Kindle cover is not text-only:
   ```bash
   # Both SVGs must reference the Wavespeed art via <image href> — not just gradients
   grep -cE '<image[^>]+(xlink:)?href=' book-<country>/assets/svg/front.svg book-<country>/assets/svg/back.svg
   # ↑ must be 1 1 (one image tag in each); 0 0 means the SVG is text-only and the
   # cover will render as a gradient with text floating over it (no art behind).

   # build.py's render_cover() must base64-inline image hrefs (rsvg-convert
   # silently drops relative + absolute hrefs without inlining)
   grep -c "base64.b64encode" book-<country>/build.py
   # ↑ must be ≥ 1.

   # build_paperback_cover.py's extract_inner() must fall back to assets/covers/
   # when an image isn't next to the SVG (gen_comics.py writes there)
   grep -c 'assets" / "covers"' book-<country>/scripts/build_paperback_cover.py
   # ↑ must be ≥ 1.

   # Visual: the Kindle JPG should be ≥ 600 KB. Text-only renders are ~470 KB;
   # real cover-with-watercolor-art renders are typically 800-1200 KB.
   ls -la book-<country>/assets/cover.jpg

   # Pre-flight against gotcha #22 (stat-badge box width): legacy 116-unit
   # rect overflows "DOCUMENTED SCAMS" letter-spaced text. Should be 144.
   grep -E '<rect[^>]*width="116"' book-<country>/assets/svg/front.svg
   # ↑ must return 0 lines. Any match → widen to 144 and shift x to -72.
   ```
   If any grep check fails, fix BEFORE moving to Phase 6 (audits will not catch this — it's a build-pipeline bug, not an editorial issue).

   **Visual-only checks (gotchas #21 and #22 — no automation possible):** open the rendered Kindle JPG at 50% zoom (thumbnail scale).
   - Tagline ("A TRAVELER'S FIELD GUIDE · MMXXVI") and hook headline must be readable against the watercolor sky band. If they ghost-render, retro-fit a `paint-order: stroke; stroke: <book-deep-color>; stroke-width: 1.5–2px` on every overlay text line below the masthead (gotcha #21).
   - "DOCUMENTED SCAMS" letter-spaced caption must fit inside the gold stat-badge rect — not overflow either edge (gotcha #22).

6. Build paperback wraparound cover PDF:
   ```bash
   PAGES=$(/opt/homebrew/bin/pdfinfo book-<country>/build/<country>-scams-paperback.pdf | awk '/^Pages:/{print $2}')
   python3 book-<country>/scripts/build_paperback_cover.py --pages "$PAGES" --paper cream
   # → book-<country>/build/<country>-paperback-cover.pdf
   ```
   **Verify the wraparound also embeds the art:** `grep -c "data:image" book-<country>/build/<country>-paperback-cover.svg` must return ≥ 2 (front + back). 0 means the same `extract_inner` covers/ fallback bug fired and the wraparound is text-only.

   **Spine-title verification (BLOCKING — this caused a UK paperback to ship with "CANADA" on the spine):** the template script derives `spine_title` from `CONFIG["title"]` so the spine should never carry a stale country name. If you cloned a non-template script (e.g. from another `book-<X>/scripts/build_paperback_cover.py`), explicitly verify:
   ```bash
   # No previous-country slug should appear anywhere in the build script.
   grep -nE '"[A-Z]{4,}"' book-<country>/scripts/build_paperback_cover.py
   # ↑ should match only generic words ("TABIJI", "KDP", etc.); any country name
   #   like CANADA/TURKEY/JAPAN/SPAIN means the clone kept hardcoded text — port
   #   the spine_title CONFIG.get() pattern in from .claude/skills/book-generator/
   #   templates/scripts/build_paperback_cover.py.template before re-running.

   # The rendered spine SVG must reflect the current country.
   grep -c ">$(echo $COUNTRY | tr a-z A-Z)<" book-<country>/build/<country>-paperback-cover.svg
   # ↑ must be ≥ 1; 0 means the spine title is wrong.
   ```

---

### PHASE 6 — PUBLISHER AUDITS (3 PARALLEL)

Launch **three Agent tool invocations in parallel** (one message, three tool calls). Brief each agent with a ~300-word prompt listing the files and the specific things to check. See `.claude/skills/book-generator/checklists/publisher-audit-prompts.md` for the canonical three-agent brief template.

- **Audit 1: Content + fact-check** — emergency numbers, airport taxi fare ranges, attraction ticket prices, embassy addresses, bank emergency lines, phone-number current-ness. Target: catch stale numbers and bad URLs.
- **Audit 2: Typography + layout** — em-dash vs en-dash, curly quotes, currency symbol rendering, diacritic rendering, TOC display, running headers on appendix pages, italic convention for foreign terms.
- **Audit 3: Voice + final sign-off** — AI-isms, smugness, cultural sensitivity, politically-fraught claims, date-stamp exposure ("2024/2025" references that'll read stale in 2027), voice consistency, back-cover count verification.

Each agent returns a ~600-word report with numbered findings + GO/HOLD verdict.

---

### PHASE 7 — APPLY FIXES + REBUILD

Apply every BLOCKER finding from each audit. Typical fixes:
- Outdated ticket prices → switch to Ministry-euro-convention with day-rate hedge
- Outdated taxi fares → widen range and add "as this edition goes to press"
- Stale year stamps → soften to "as of this edition"
- URL typos → fix
- Address typos → fix
- Running-head truncation → shorten the subsection heading that's too long
- Currency-symbol rendering → add build-time normalizer

Rebuild:
```bash
rm -f book-<country>/assets/cover.jpg
python3 book-<country>/build.py
python3 book-<country>/scripts/build_paperback_interior.py
PAGES=$(/opt/homebrew/bin/pdfinfo book-<country>/build/<country>-scams-paperback.pdf | awk '/^Pages:/{print $2}')
python3 book-<country>/scripts/build_paperback_cover.py --pages "$PAGES" --paper cream
```

Page count may change. Cover SVG regenerates with updated spine automatically.

---

### PHASE 8 — SITE INTEGRATION

1. **Create `books/<country>-tourist-scams/` site page**:
   - Copy a recent book's page as a template (any of `books/{argentina,japan,turkey}-tourist-scams/index.html` works — all current landers carry the canonical structure including the `@book-sneak-peek:start ... :end` block)
   - Copy covers: `mkdir -p books/<country>-tourist-scams/covers && cp book-<country>/assets/covers/{front,back}.jpg books/<country>-tourist-scams/covers/`
   - Do a bulk search-and-replace through the HTML:
     - URL/slug swaps (`turkey-tourist-scams` → `<country>-tourist-scams`, `country/tr` → `country/<iso>`)
     - Title, meta descriptions, canonical, og:title, og:description, Schema.org Book metadata
     - Cover SVG text overlays (volume number, page count, scam count, city count, hook copy)
     - Hero H1 + subtitle (with country-specific signature scam)
     - 3 teaser cards (one per flagship scam — write fresh for the new country)
     - 13-city / 16-city / N-city grid with Turkish-specific emoji + city names
     - Back-cover SVG text overlays
     - **`@book-sneak-peek:start ... :end` "A look inside" block** — every lander page MUST keep this 2-comic sample section. Customize:
       - 2 city slugs from this book (point to `https://img.tabiji.ai/scams/<city-slug>/scam-1.jpg`)
       - 2 short scam titles matching each city's actual scam-1 (read from `scams/<city>/index.html` `alt="... — comic illustration"`)
       - "A sneak peek of two of the N" — N is this book's total scam count
       - Then add the new country to `scripts/book-cta-rollout/add_book_sneak_peek.py` (PAIRS + TOTALS) so the section can be re-injected idempotently if it's ever lost
     - "Why we write these books" 3 cards (press outlets, phrasebook angle, annual updates)
     - Roadmap tiles — promote all previously-live volumes to "Live" status
     - FAQ page count
     - Bottom CTA "free links" to country-specific city scam pages
   - After bulk replace, verify 0 residue of the template country (`grep -c "Turkey\|Turkish\|Istanbul\|Bodrum"` should return only legitimate series-roadmap mentions, typically 3-5).

2. **Update `books/index.html` hub**:
   - Add the new book to the Schema.org `hasPart` array (before the closing `]}</script>`)
   - Add a featured-book `<div class="featured-book">` block after the most-recent book's block
   - Promote the country in the roadmap grid from "coming" to "Launching 2026 · Kindle" (replace `book-tile-coming` anchor with a live `book-tile` anchor)
   - Decrement the roadmap "more queued" count by 1

---

### PHASE 9 — DEPLOY

1. Sync + merge latest origin/main:
   ```bash
   git fetch origin main --quiet && git merge origin/main --no-edit
   ```
   If the merge introduces conflicts in `books/index.html`, re-apply the Schema.org + featured block + roadmap changes on top of the latest.

2. Add gitignore entries:
   ```
   book-<country>/build/
   book-<country>/__pycache__/
   ```

3. **Self code-review 3x** (compose as 3 separate diagnostic scripts):
   - Review 1: File inventory — count manuscripts, illustrations, comics, build outputs
   - Review 2: Content validation — PDF page count, TOC page numbers present, 0 currency-symbol residue, site-page country residue check
   - Review 3: Hub integration — `hasPart` book count, featured-block country mentions

4. Stage + commit:
   ```bash
   git add .gitignore books/index.html books/<country>-tourist-scams/ book-<country>/
   git commit -m "$(cat <<'EOF'
   <Country> book (Volume N): complete Kindle + paperback package
   
   Ship Volume N of the Tabiji Travel Safety Series — <scam-count> scams
   across <city-count> <country-adjective> cities.
   
   Deliverables (gitignored build/):
   - <country>-scams.epub (<size>, <word-count> words, Kindle-ready)
   - <country>-scams-paperback.pdf (<page-count> pages, 6x9 trim, TOC with page numbers)
   - <country>-paperback-cover.pdf (<width> x 9.25" KDP wraparound, <spine>" spine)
   - Kindle cover JPG (1600x2560)
   
   Workspace, editorial, and site details inline...
   
   Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
   EOF
   )"
   ```

5. Push + PR + merge + cleanup:
   ```bash
   git push origin HEAD
   gh pr create --title "<Country> book (Volume N): complete Kindle + paperback package" --body "<detailed-pr-body>"
   gh pr merge <PR-NUMBER> --squash --delete-branch
   # The local branch-delete step fails with "main is already used by worktree"; ignore.
   git push origin --delete claude/<branch-name>
   ```

---

### PHASE 10 — SHIP

Build the desktop asset folder with the canonical 7-subfolder structure:

```bash
DEST=~/Desktop/<country>-tourist-scams
rm -rf "$DEST"
mkdir -p "$DEST"/{01-final-deliverables,02-cover-art,03-city-illustrations,04-scam-comics,05-manuscript-source,06-build-scripts,07-build-artifacts}

# 01 — final deliverables (ready-to-upload)
cp book-<country>/build/<country>-scams.epub                  "$DEST/01-final-deliverables/<country>-scams.epub"
cp book-<country>/build/<country>-scams-paperback.pdf         "$DEST/01-final-deliverables/<country>-scams-paperback-interior.pdf"
cp book-<country>/build/<country>-paperback-cover.pdf         "$DEST/01-final-deliverables/<country>-paperback-wraparound-cover.pdf"
cp book-<country>/assets/cover.jpg                             "$DEST/01-final-deliverables/<country>-kindle-cover-1600x2560.jpg"

# 02 — cover art sources
cp book-<country>/assets/covers/front.jpg                      "$DEST/02-cover-art/front-raw.jpg"
cp book-<country>/assets/covers/back.jpg                       "$DEST/02-cover-art/back-raw.jpg"
cp book-<country>/assets/svg/front.svg                         "$DEST/02-cover-art/front-with-text-overlay.svg"
cp book-<country>/assets/svg/back.svg                          "$DEST/02-cover-art/back-with-text-overlay.svg"

# 03 — city illustrations
cp book-<country>/assets/cities/*.jpg                          "$DEST/03-city-illustrations/"

# 04 — scam comics, flattened to <slug>-NN.jpg
for dir in book-<country>/assets/images/*/; do
  slug=$(basename "$dir")
  for f in "$dir"*.jpg; do
    fname=$(basename "$f")
    cp "$f" "$DEST/04-scam-comics/${slug}-${fname}"
  done
done

# 05 — editable manuscript source
cp book-<country>/manuscript/*.md                              "$DEST/05-manuscript-source/"
cp book-<country>/config.yaml                                  "$DEST/05-manuscript-source/config.yaml"

# 06 — build scripts
cp book-<country>/build.py                                     "$DEST/06-build-scripts/"
cp book-<country>/scripts/*.py                                 "$DEST/06-build-scripts/"
cp book-<country>/templates/*.css                              "$DEST/06-build-scripts/"
cp book-<country>/templates/*.tex                              "$DEST/06-build-scripts/"

# 07 — intermediate build artifacts (reference)
cp book-<country>/build/manuscript.md                          "$DEST/07-build-artifacts/assembled-manuscript-epub.md"
cp book-<country>/build/paperback-manuscript.md                "$DEST/07-build-artifacts/assembled-manuscript-paperback.md"
cp book-<country>/build/<country>-paperback-cover.svg          "$DEST/07-build-artifacts/<country>-paperback-cover-source.svg"
```

Write a `README.txt` at the folder root using `checklists/desktop-readme-template.txt` as the canonical layout. Include:
- Country name + volume number + series tagline
- **Amazon KDP listing block (top of README, after the header)** — Title, Subtitle, ~4,000-char HTML description, and 7 KDP keywords. See the template comments for the description structure (hook → angle → what's inside → who it's for → why we wrote it → CTA) and the keyword distribution (country/region × 2, persona × 2, pain × 2, recovery × 1). Verify the description is between 3,800-4,000 chars with `wc -c` and each keyword is ≤50 chars with `awk '{print length, $0}'` BEFORE writing the README.
- Folder map (what's in each of the 7 subfolders)
- Build stats (scam count, city count, word count, page count, spine width, wraparound dimensions)
- Series context (Vol 1-N list)
- Online references (book page URL, series hub URL, free data URL)
- Editorial process note
- KDP upload checklist (Kindle + Paperback separately) — references the listing block above for Title/Subtitle/Description/Keywords
- Key helpline numbers from the recovery appendix
- Major Tourist Police / police desk directory if applicable

---

## Success criteria

At the end of a successful `book-generator <country>` run, all of the following are true:

- [ ] PR has been opened, merged to origin/main, and the branch cleaned up
- [ ] `/books/<country>-tourist-scams/` is live on the site
- [ ] `/books/` hub features the new volume and promotes it in the roadmap
- [ ] `~/Desktop/<country>-tourist-scams/` exists with 7 subfolders + README + all 4 final deliverables
- [ ] Paperback PDF has real TOC page numbers (verified via `pdftotext`)
- [ ] Zero currency-symbol residue or missing-glyph warnings in the final PDF
- [ ] 3 publisher audits ran and every BLOCKER finding was applied before final rebuild
- [ ] Schema.org `hasPart` array contains the new book
- [ ] Book number of pages drives the wraparound cover's spine width math

## Anti-patterns (do not)

- ❌ Do not use Chrome headless for the paperback PDF — TOC page numbers break
- ❌ Do not skip the `\@schapter` override — appendix running heads will bleed
- ❌ Do not hardcode absolute image paths in SVGs — rsvg-convert silently drops them
- ❌ Do not skip the 5 copyedit passes or the 3 publisher audits
- ❌ Do not commit `build/` artifacts to git (they're 50-100 MB; gitignore them)
- ❌ Do not write a city intro without naming at least 3 specific scams with venue/street/currency amounts
- ❌ Do not include political commentary (Kurdish/Xinjiang/Tibet/Taiwan/dissidents/etc.) — travel-safety only
- ❌ Do not date-stamp specific USD-to-local-currency exchange rates; use the edition-neutral disclaimer pattern
- ❌ Do not bill the book as an itinerary planner; it's a scam-avoidance manual

## Supporting files (in `.claude/skills/book-generator/`)

- `templates/manuscript/*.md.template` — skeleton files for each manuscript chapter with placeholder tokens
- `templates/scripts/*.py` — canonical build scripts (the working set copied from `book-turkey/`)
- `templates/build-templates/{style.css,header-includes.tex}` — EPUB CSS + LaTeX override
- `checklists/publisher-audit-prompts.md` — the three pre-built audit-agent prompts
- `checklists/readme-template.txt` — the `~/Desktop/<country>-tourist-scams/README.txt` template

## Reference commits

- Spain (Vol 5): `160df07ea2` — `Books: Vietnam (V6) + Spain (V5) — complete Kindle + paperback packages (#245)`
- China (Vol 7): `55cb0d69e5` — `China book (Volume 7): complete Kindle + paperback package (#250)`
- Turkey (Vol 9): `f5e1f223e8` — `Turkey book (Volume 9) + Canada book (Volume 10): complete Kindle + paperback packages (#262)`

Study these commits' diffs if you need to see the full shape of a shipped book.
