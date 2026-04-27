# Tabiji book polishing guide

The running playbook for taking a scam-data JSON set from "raw scraped prose"
to "KDP-ready Kindle EPUB + paperback PDF." Distilled from 15 volumes
(Japan → Brazil → Canada → Portugal → Vietnam → Greece → UK → Turkey → China →
Spain → Thailand → France → Germany → Indonesia → US) worth of KDP rejection
loops and copyedit iterations.

> **Read this before touching a new country volume.** Every trap below has
> blocked a KDP upload at least once.

---

## The 5 categories of polish

| Category                     | Lives in                             | Caught by             |
| ---------------------------- | ------------------------------------ | --------------------- |
| **Prose sanitization**       | `scripts/polish_scam_prose.py`       | Build-time regex      |
| **American-English consistency** | `scripts/polish_scam_prose.py`   | UK→US normalizer      |
| **Reddit-citation scrub**    | `scripts/polish_scam_prose.py`       | Pattern A–F + D2      |
| **Layout / KDP geometry**    | `scripts/build_paperback_interior.py`| WeasyPrint + xelatex  |
| **Cover safe zones**         | `scripts/build_paperback_cover.py`   | SVG + rsvg-convert    |

---

## 1. The polish script (`polish_scam_prose.py`)

This is the single most-important file in the book pipeline. It runs over
every `description` / `avoidance` / `location` field in every scam JSON, plus
once more over the whole assembled manuscript. Every pattern in it was added
because a real human spotted a real rendering bug in a real book.

### 1a. Reddit citation scrub (Patterns A–F)

The raw JSONs cite Reddit threads verbatim (`r/bali 'Title' (comments/1hpfieg, 2025)
is the canonical anchor: 'evidence.'`). Readers don't want to see those. The
scrubber has six patterns, each catching a different shape:

| Pattern | Shape                                                            | Notes |
| ------- | ---------------------------------------------------------------- | ----- |
| **A**   | `r/SUB 'title' verb-clause: 'evidence.'`                         | Colon + quoted evidence. Cap evidence at `[^.\n]{5,400}?` to prevent cross-sentence over-matching when quotes have internal contractions. Append a trailing `[^.\n]{0,200}\.` to consume orphan tails. |
| **B**   | `r/SUB 'title' (comments/hash) documents the pattern.`           | Citation verb + continues through next period. |
| **C**   | `r/SUB 'title' (comments/hash) — bare citation.`                 | No verb, through next period. |
| **D**   | `per r/SUB 'title'` / standalone, nothing after.                 | |
| **D2**  | `(r/sub 'title')` — parenthesized bare citation.                 | Old Pattern D required closing quote followed by whitespace/open-paren; parens-enclosed titles passed through untouched. |
| **E**   | Malformed `r/sub (...` with no closing paren.                    | Line-ending cleanup. |
| **F**   | Bare `r/sub` trailing no title.                                  | Final sweep. |

**Critical Pattern A detail**: the *title* match uses `.+?` (allows periods,
Reddit titles are often truncated like "Robbed at HCM airport by fake Grab
driver. Be"). The *evidence* match uses `[^.\n]{5,400}?` (must be within a
single sentence — otherwise unclosed quotes with internal contractions like
`'It's a scam.'` match all the way to the next quoted scam-term in a later
paragraph, leaving orphan fragments like "even if no work was actually done.").

### 1b. UK → US normalizer

Every volume ships en-US. The list is long and keeps growing:

- `colour / colours / coloured / colouring` → `color / colors / colored / coloring`
- `traveller / travellers / travelling / travelled` → `traveler / travelers / traveling / traveled`
- `defence / offence / licence / pretence` → `defense / offense / license / pretense`
- `centre / centres / centred` → `center / centers / centered`
- `flavour / flavours / flavoured / favour / favourite` → `flavor / flavors / flavored / favor / favorite`
- `behaviour / neighbour / neighbourhood` → `behavior / neighbor / neighborhood`
- `realise / recognise / minimise / organise / materialise / authorise / specialise / emphasise / prioritise / finalise / monetise / commercialise / rationalise / familiarise / customise / pedestrianise / modernise / characterise / criticise / hospitalise / utilise` + all inflections → `-ize / -ized / -izes / -izing / -ization`
- `metre / kilometre / litre / theatre / catalogue / programme / jewellery` → `meter / kilometer / liter / theater / catalog / program / jewelry`
- `honour / labour / humour / favouring / labouring` → `honor / labor / humor / favoring / laboring`
- `cancelled / cancelling` → `canceled / canceling`
- `analyse / analysed` → `analyze / analyzed`
- `fulfil / fulfilled` → `fulfill / fulfilled`
- `storey / storeys` → `story / stories`

Use a proper-noun exception list for cultural references — **"Theatre District"
in Toronto stays as `Theatre District`** (official city neighborhood name),
**"Foreign and Commonwealth Office" keeps the UK spelling**, Toronto's "Honest
Ed's" stays. Inspect your per-country proper-noun list before running.

### 1c. Age-framing removal

Early Tabiji drafts framed every "defensive playbook" as *"For older travelers,
the practical defense:"* — well-intentioned but narrowed the audience. Strip
all variants:

```
For older travelers, → For travelers,
For older cruise passengers (4–10 hour stops) → For cruise passengers
For older cruise passengers AND X → For cruise passengers
older traveler / older travelers (mid-sentence) → traveler / travelers
```

**Compound modifiers** (added when book-Canada surfaced them):
`For older business / female / male / solo / cruise / budget / independent /
first-time / luxury / family / senior / package-holiday / retired / vacation /
retiree <traveler | passenger | tourist | visitor | holidaymaker>` → `For <modifier>
<noun>`.

**Catch-all at the end** (added when book-Portugal surfaced hyphenated and
multi-word modifiers like `"For older cruise-passengers"` and
`"For older UK, Irish, and Northern European travelers"`):

```python
md = re.sub(r"\bFor older (?=[a-zA-Z])", "For ", md, flags=re.IGNORECASE)
md = re.sub(r"\bfor older (?=[a-zA-Z])", "for ", md, flags=re.IGNORECASE)
```

**Legitimate uses to preserve**: `elderly Nazaré widows in the traditional
sete saias` (cultural reference, not age-framing). Run a final audit and
manually whitelist cultural/demographic descriptions.

### 1d. Mid-word truncation repair

Scraped Reddit HTML sometimes inserts stray apostrophe-space mid-word:
`get' ting`, `plac' es`, `bean' s`, `obtaine' d`, `protect' ing`, `figur' ing`,
`meaningl' ess`, `reputa' tion`, `flash' ed`, `especial' ly`, `indi' cating`,
`b' ecause`, `involv' ed`, `s' seasoned`, `t' axis`, `Book' ing`, `V' ietnam`.

Real hit rate: **~1–8 truncations per 75-scam volume**. The audit regex is:

```python
r"\b[a-zA-Z]{2,}' (ing|ed|tion|sion|ly|ment|able|ible|ful|less|ness|age|ance|ence|ship|hood|ary|ity|ive|ate|est|ism|ist|ous|ize|ise|ere|ess|ery)\b"
```

**Detection — not auto-repair.** Fixes go in the source JSON
(`api/v1/scams/<city>.json`) because wrong-sounding concatenations like
`bean's` vs `beans` vs `bean s` need human review.

---

## 2. Pandoc math-dollar fix (the single most-dangerous bug)

**Symptom**: a paragraph containing two `$` signs (currency quotes + another
`$` later) renders as `10foracoupleofhoursYoupayLater...` — every letter wrapped
in `<em>` tags with all spaces stripped.

**Root cause**: pandoc's default markdown mode enables `tex_math_dollars`.
`$10-20 for a couple of hours... P$ Montreal app` looks like LaTeX math to
pandoc.

**Fix** — already baked into `book/build.py` and `book/scripts/build_paperback_interior.py`:

```python
"--from", "markdown-tex_math_dollars-tex_math_single_backslash-tex_math_double_backslash-raw_tex-raw_attribute",
```

Applies to **both** the EPUB build and the paperback HTML-fallback build.
For the LaTeX-direct path in `build_pdf_direct()`, the same flag must appear
on that pandoc invocation too.

**First seen**: book-Canada, Montreal "Street Parking Fake Attendant" scam
(page 104 of the paperback). Since then caught on book-China (¥500 + $30
dual-currency prose), book-Turkey (TL + EUR + USD), book-Portugal (€20 + $30
+ `infraestruturasdeportugal.pt` URL-lookalike).

**Test**: after every build, scan `build/manuscript.md` for:
```python
re.findall(r'[a-z]{25,}[.,]', text)
```
Filter out `.pt`, `.com`, `.org`, `.cn`, URL-like concats, and legitimate long
words. Any remaining hit is the bug.

---

## 3. KDP paperback interior geometry

KDP rules (verified with actual rejections):

| Pages    | Min gutter (inside) | Min outside/top/bottom |
| -------- | ------------------- | ---------------------- |
| 24–150   | 0.375"              | 0.25"                  |
| 151–300  | 0.5"                | 0.25"                  |
| 301–500  | 0.625"              | 0.25"                  |
| 501–700  | 0.75"               | 0.25"                  |
| 701+     | 0.875"              | 0.25"                  |

**What actually works** (baked into `build_paperback_interior.py`):

```python
"-V", "geometry:inner=0.875in",   # comfortable above the 0.625" requirement
"-V", "geometry:outer=0.5in",     # 2x KDP 0.25" min
"-V", "geometry:top=0.75in",      # room for running head
"-V", "geometry:bottom=0.75in",   # room for page number
"-V", "classoption=twoside",      # mirrored margins — inner flips automatically
"-V", "documentclass=book",
```

**Verify every page passes** before upload:

```python
# Render every page to 72 DPI, find leftmost/rightmost dark pixel per page,
# compute distance from trim edge based on whether page is odd (left) or even (right).
# Any page where gutter < 0.625" is a blocker.
```

See `book/scripts/build_paperback_interior.py`'s final gutter-check pass for the
reference implementation.

### Common interior content issues

**Wide tables in pipe syntax** — pandoc's `longtable` auto-sizes columns by
content width. A cell with `King Charles III (reverse: Sir Winston Churchill)`
on page 324 (UK book) pushed the whole table 0.3" beyond `\textwidth`, dropping
that page's gutter to 0.014". **Fix**: shorten cell content (`Charles III
(Churchill)`) or break into two rows.

**Unicode glyphs not in the body font**: Georgia ships without `→` (U+2192).
Pandoc warns `Missing character: There is no →` and renders blank tofu.
**Fix**: replace with ` to ` at the polish stage.

**Missing LaTeX packages** (TinyTeX default is sparse):

```bash
tlmgr install setspace fancyhdr xurl seqsplit
```

`setspace` is required when pandoc emits `\linestretch`. `xurl` + `seqsplit`
allow long URLs to break cleanly at slashes.

---

## 4. KDP paperback cover safe zones

**KDP requirement**: text ≥ 0.375" from trim on all four sides. For headroom
(and to pass KDP's overly-sensitive automated check), **aim for 0.5"**.

**At 300 DPI**, 0.375" = 112.5 units, 0.5" = 150 units.

**Traps we've actually hit:**

1. **ISBN barcode placeholder overflow** (Brazil). The cream `<rect>` in the
   bottom-right only had 0.25" to the right + bottom trim. KDP flagged it
   even though it's not text. **Fix**: either inset it to 0.5" or remove
   entirely — KDP adds the real barcode automatically; a placeholder isn't
   required.

2. **Cream text on cream box** (Brazil). Footer `PAPERBACK EDITION · 2026 ·
   TABIJI.AI` at `#f4e6a8` sat on top of the barcode placeholder rect (same
   color). Invisible where they overlapped. **Fix**: shorten the footer OR
   move it outside the barcode-rect's y-range OR drop the placeholder.

3. **Headline too wide** (Brazil). `"What the guidebooks won't tell you."`
   at 96pt extended past the red safe-zone marker. **Fix**: reduce to 78pt.
   Recalculate: at Georgia serif, 36 chars × (font-size × 0.55 + letter-
   spacing) must fit within `trim_width - 2 × safe_margin = 1800 - 300 = 1500`
   units at 300 DPI.

4. **Spine width wrong for page count** (UK). Submitted 12.970" for a
   346-page book; KDP expected 13.029" (spine for 346 cream pages =
   346 × 0.00225" = 0.779"). **Fix**: recompute spine AFTER final paperback
   page count is known. `spine_in = pages × 0.00225` for cream,
   `pages × 0.002252` for white; bleed adds 0.125" each side.

5. **Busy-background text wash-out** (Portugal). Full-bleed comic behind a
   translucent gradient overlay made "Travel Safety Series" unreadable in
   thumbnail size. **Fix**: swap to a framed comic panel (380×380 square,
   gold double-line border) with solid cream band above and solid Portuguese-
   flag-green band below. Text sits on solid color, reads crisply at any
   size. See `book-portugal/assets/svg/front.svg` for the template.

6. **Image slice cropping speech bubbles** (Portugal v2). `preserveAspectRatio="xMidYMid slice"`
   on a 1024×1024 source in a 412×360 frame cropped the top/bottom speech
   bubbles. **Fix**: use `xMidYMid meet` with a square frame matching the
   source aspect ratio.

7. **Hardcoded spine text from template copy** (Italy v1). `book-italy` was
   scaffolded by copying `book-canada/scripts/build_paperback_cover.py`,
   which had `>CANADA</text>` baked into the f-string that renders the
   spine. Italy shipped a `CANADA / Tourist Scams` spine in its first cover
   draft. **Fix**: derive spine title from `CONFIG["title"]` at module
   load — `spine_title = re.split(r"\s+Tourist\b", CONFIG["title"])[0].upper()`.
   Override with an explicit `CONFIG["spine_title"]` for countries where
   the first word isn't the spine text (e.g. `"Mont-Saint-Michel"` should
   show `FRANCE`, not `MONT-SAINT-MICHEL`). Fixed in `book/`,
   `book-canada/`, and `book-italy/` — but check any fresh-scaffolded
   volume's `build_paperback_cover.py` before rendering the first cover.

8. **QR code blocks Amazon's auto-placed barcode** (Italy v1). The `back.svg`
   shipped with a SCAN-FOR-UPDATES QR code in the bottom-right — exactly
   where KDP places the ISBN barcode (Amazon reserves a 2" × 1.2" zone at
   bottom-right of the back cover). KDP rejected the cover with "We're
   unable to detect a valid barcode." **Fix**: remove the QR group + label
   from `back.svg`. Leave the bottom-right blank (dark background color is
   fine) so Amazon's barcode has contrast to sit on. `paperback_back_content()`
   in `build_paperback_cover.py` already does this for the generic book-
   canada back template, but a country-specific `back.svg` that was
   hand-edited might still carry the QR — grep for `SCAN FOR UPDATES` /
   `QR` in `assets/svg/back.svg` before building the cover PDF.

9. **Spine / bleed color hardcoded navy** (Italy v1, sibling of #7). The
   wraparound composition script has a `fullBleed` linearGradient hardcoded
   to Canada's palette `#0F1A2E → #1E2F4D`. Italy's front + back covers
   are oxblood (`#5A1E1A → #3F1612`), so the spine rendered as a navy
   stripe sandwiched between two oxblood halves — broken. **Fix**: make
   bleed colors config-driven. Read `CONFIG["bleed_colors"]` as a
   `[top_hex, bottom_hex]` list, default to navy for back-compat.

   ```python
   bleed_colors = CONFIG.get("bleed_colors", ["#0F1A2E", "#1E2F4D"])
   bleed_top, bleed_bottom = bleed_colors[0], bleed_colors[1]
   ```

   Then reference `{bleed_top}` / `{bleed_bottom}` in the SVG f-string.
   Each volume's `config.yaml` declares its own palette. Italy's:

   ```yaml
   bleed_colors:
     - "#5A1E1A"   # top — matches front-cover oxblood gradient start
     - "#3F1612"   # bottom — matches front-cover oxblood gradient end
   ```

   Inspect `assets/svg/front.svg` for the existing cover-art gradient
   stops and mirror them into `bleed_colors`. Already propagated to
   `book/` (template), `book-canada/`, and `book-italy/`.

---

## 5. The 3-pass copyedit workflow

Run this **every time**, on the built `manuscript.md`, *not* the source JSON:

### Round 1 — AmE + truncations

```python
checks = {
    'UK spellings':          r'\b(traveller|colour|centre|defence|licence|...)\b',
    'Suffix truncations':    r"\b[a-zA-Z]{2,}' (ing|ed|tion|sion|ly|ment|...)\b",
    'r/sub citations':       r'r/\w+ [\u2018\u2019\x27]',
    'Comment hashes':        r'comments/[a-z0-9]{5,}',
    'Age-framing':           r'\b(for older|older travelers?|elderly|...)\b',
    'TODOs':                 r'\bTODO\b',
    'weathe typo':           r'\bweathe\b(?!r)',
    'Math-$ corruption':     r'[a-z]{25,}[.,]',
}
```

Expected output after a clean build: all zero. Anything non-zero is a
real fix — go back to the source JSON, not the built manuscript.

### Round 2 — grammar + orphans

```python
# Orphan sentence fragments — sentence starting lowercase after a period
orphans = re.findall(r'(?<=[.!?])\s+([a-z][a-z\' ,-]{15,100}\.)', text)
# Filter sentence-starting conjunctions: and, but, or, if, for, so, yet, nor,
# when, as, though, while, however, moreover, further, also, then, plus
```

**1-letter prefix truncations** (e.g. `V' ietnam`, `b' ecause`):

```python
r"(?<=[\s\.\,\;\:\(\-])([a-zA-Z])' ([a-z]{3,})\b"
```

**Hanging smart quotes** — paragraphs with unmatched `\u2018` / `\u2019`
(excluding contractions).

### Round 3 — design consistency

Every scam must have **all five elements** in order:

1. `## Scam Name` (H2)
2. `**Category** · Severity: X · Frequency: Y`
3. Comic image (`![alt](path)`)
4. `### How this scam works` + prose
5. `### How to avoid it` + bullet list
6. `**Where it happens:**` + location
7. `*tag1 · tag2 · tag3*` (italic tag line)

```python
# Quick assertion
sev_lines = re.findall(r'\*\*[A-Z][a-zA-Z-]+\*\* · Severity: (\w+) · Frequency: (\w+)', text)
how_works = len(re.findall(r'^### How this scam works', text, re.MULTILINE))
how_avoid = len(re.findall(r'^### How to avoid it', text, re.MULTILINE))
where = len(re.findall(r'\*\*Where it happens:\*\*', text))
assert len(sev_lines) == how_works == how_avoid == where == expected_scam_count
```

Frequency should be uniformly `Common` (or intentionally varied with reason).
Severity distribution should cover High/Moderate/Minor in proportion to the
book's risk profile.

---

## 6. Comic pipeline (`gen_comics.py`)

- Source: Wavespeed / Nano Banana Pro, per-scam bespoke prompt (Gemini 2.5 Pro
  synthesizes a script from the JSON).
- Output: 2×2 comic panel, 1024×1024 JPEG, uploaded to R2 at
  `img.tabiji.ai/scams/<city>/scam-N.jpg`.
- Book ingestion: download from R2 + resize to 1024×1024 + save to
  `assets/images/<city>/NN.jpg` (zero-padded).
- **Cache-bust via `?v=2`** after regens so the CDN serves the new bytes.

**Each country locks a unique art style** (memory of these is distributed
across `project_scam_comics_style_<country>.md` notes):

- Japan — Studio Ghibli painted anime
- Portugal — Paula Rego modernist (not yet generated as of this doc)
- Canada — Drawn & Quarterly indie-comic (Seth-like)
- Brazil — Aldemir Martins folk-modernist
- Vietnam — Đông Hồ folk woodblock on rice paper
- China — Feng Zikai (丰子恺) brush cartoon
- UK — Quentin Blake line + watercolor
- Germany — Heinrich Zille Berlin Milljöh pen-and-ink-wash
- Thailand — watercolor storybook
- France — Hergé ligne-claire (Tintin)
- Austria — Sempé pen-and-ink wash
- Greece — ancient red-figure pottery
- Turkey — Ottoman Iznik tile border + contemporary illustrated comic
- Croatia — Ivan Generalić / Hlebine naïve art
- Hong Kong — 1960s-70s Shaw Brothers painted poster
- Indonesia — Lontar palm-leaf manuscript
- Spain — Paco Roca contemporary graphic novel
- Argentina — Quino / Mafalda

**Cast of protagonists** is shared across all volumes — 4 canonical travelers
(Margie 62F, Priya 34F, Harry 64M, Marcus 34M). Paste cast description verbatim
into every comic prompt; see the per-country style memory notes for the full
style-block + cast-block prompt.

---

## 7. Desktop artifact layout

Final deliverables for each book, copied to `~/Desktop/<country>-scams/`:

```
<country>-scams/
  kindle/
    <country>-scams.epub              # Kindle manuscript upload
    <country>-kindle-cover.jpg        # 1600×2560 JPEG
  paperback/
    <country>-scams-paperback-interior.pdf   # 6×9 interior
    <country>-paperback-cover.pdf            # wraparound cover
    <country>-paperback-cover.svg            # editable vector source
  README.md                                  # volume summary + upload instructions
```

Or (older convention for Japan/Thailand/Greece):

```
<country>-scams-CORRECT/
  01-final-deliverables/                     # everything goes here
  02-cover-art/                              # raw + designed SVGs
  03-city-illustrations/                     # per-city travel-poster JPGs
  04-scam-comics/                            # per-scam 2×2 comic JPGs
  05-manuscript-source/                      # raw build outputs for audit
  06-build-scripts/                          # copies of the scripts used
  07-build-artifacts/                        # intermediate HTMLs etc.
  README.txt
```

Stick with whichever convention already exists for that country; don't mix.

---

## 8. KDP-upload checklist

Before uploading either the Kindle or the paperback:

- [ ] Manuscript shows 0 UK spellings, 0 suffix truncations, 0 r/sub
      citations, 0 comment hashes, 0 age-framing, 0 TODOs, 0 math-$
      corruption.
- [ ] `build/manuscript.md` word count is reasonable (~40k–65k per volume).
- [ ] Every scam has category + severity + frequency + comic + how-it-works
      + how-to-avoid + where + tag line.
- [ ] Paperback PDF: all pages ≥ 0.625" gutter. `pdfinfo` reports Page size =
      432 × 648 pts (6×9). Last page page-number matches interior page count.
- [ ] Paperback cover PDF: width matches `(2 × 6.25) + spine` for the actual
      page count (`spine = pages × 0.00225` for cream). Text/graphics all ≥
      0.5" from trim.
- [ ] Kindle EPUB: ~30–50 MB, validates under `epubcheck`, cover embedded
      (first item in OPF spine), comics visible on every scam page.
- [ ] KDP metadata filled in: title, subtitle, 7 keywords, HTML description
      under 4000 chars, contributor info, Library of Congress / BISAC
      categories, age range, language = en-US.

---

## 9. Known gotchas

- **Pandoc smart-quote autocorrect**: `markdown+smart` enables curly
  apostrophes, which is great for prose but breaks inside `rsvg-convert` text
  that uses `'` as an XML attribute delimiter. Source SVGs should use `&#8217;`
  entities for apostrophes in copy.
- **Unicode in running headers**: book-class `\leftmark` uppercases by default
  via `\chaptermark`. Long scam-title H2s then overflow the 6" running head.
  Fix in `templates/header-includes.tex` via fancyhdr + `\nouppercase{\leftmark}`.
- **Pandoc TOC + LaTeX inter-word ligature bug**: French cities with `L'` /
  `D'` accents render the TOC page number against the wrong dot-leader row.
  Override `\l@chapter` in header-includes.
- **macOS file-system case-insensitivity**: `Lagos` vs `lagos-portugal` — the
  R2 CDN uses `lagos-portugal` but the website slug is `lagos`. Use the R2
  slug when downloading.
- **Desktop folder conventions differ by country** — don't assume a
  `kindle/` + `paperback/` pair. Check first with `ls`.

---

## 10. When in doubt

Copy the nearest-analog country's build. Don't invent. Every bug in this doc
has a real commit that fixed it; every pattern has a reason. The scripts are
boring on purpose. If you're about to add a new regex, first check whether
a more-generic polish rule in `polish_scam_prose.py` catches it.
