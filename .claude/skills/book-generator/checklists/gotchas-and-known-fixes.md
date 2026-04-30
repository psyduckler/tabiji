# Gotchas + Known Fixes

Every anti-pattern I've hit while shipping 10 volumes of the Travel Safety Series, with the fix for each.

## 1. Chrome headless PDF — no TOC page numbers

**Symptom:** Paperback PDF built via `chrome --headless=new --print-to-pdf` has TOC entries but no page numbers next to each.

**Cause:** Chrome's CSS Paged Media implementation does not support `content: target-counter(attr(href), page)`.

**Fix:** Use `pandoc --pdf-engine=xelatex` instead. The book-class LaTeX output renders a Contents page with real page numbers automatically. See `book-spain/scripts/build_paperback_interior.py` `build_pdf_direct()` function.

**Install xelatex (if not present):**
```bash
curl -sL "https://yihui.org/tinytex/install-bin-unix.sh" | sh
export PATH=$PATH:/Users/bjh/Library/TinyTeX/bin/universal-darwin
```

---

## 2. Unnumbered chapters — running-head bleeds from last numbered chapter

**Symptom:** The last city's name (e.g. "KONYA" in Turkey, "LANZAROTE" in Spain, "ZHANGJIAJIE" in China) bleeds into every appendix page's running header.

**Cause:** LaTeX's `\chapter*` does not call `\chaptermark` by default, so `\markboth` is never updated on `{-}` unnumbered chapters.

**Fix:** Ship `templates/header-includes.tex` with:
```latex
\makeatletter
\let\origschapter\@schapter
\def\@schapter#1{\origschapter{#1}\markboth{\MakeUppercase{#1}}{\MakeUppercase{#1}}}
\makeatother
```
Then pass `-H <path-to-header-includes.tex>` to pandoc.

See `book-spain/templates/header-includes.tex` and `book-spain/scripts/build_paperback_interior.py` lines 230-255.

---

## 3. Rsvg-convert silently drops absolute-path images in SVG

**Symptom:** Paperback wraparound cover PDF renders as a blank/near-blank 1600-byte file, OR renders the navy bleed gradient but no cover-art.

**Cause:** `rsvg-convert` 2.62+ silently refuses to load `<image xlink:href="/absolute/path/cover.jpg" />`. No warning. No error.

**Fix:** At compose time, read the referenced JPG, base64-encode it, and inline it as a data URI:
```python
encoded = base64.b64encode(src.read_bytes()).decode("ascii")
return f'xlink:href="data:image/jpeg;base64,{encoded}"'
```

See `book-spain/scripts/build_paperback_cover.py` `extract_inner()` function.

---

## 4. Country-specific currency symbols missing from Arial Unicode MS

**Symptom:** LaTeX warnings during paperback build: `Missing character: There is no ₺ (U+20BA) in font Arial Unicode MS/OT`. PDF shows hollow-box missing-glyph placeholders wherever the symbol appears.

**Known-missing glyphs:**
- Turkish lira ₺ (U+20BA)
- Indian rupee ₹ (U+20B9)
- Bangladeshi taka ৳ (U+09F3)
- Vietnamese đồng ₫ (U+20AB) — partially supported

**Known-working glyphs:** $, €, £, ¥, ₱ (peso), ₦ (naira)

**Fix:** Add a build-time normalizer in `book-<country>/build.py`:
```python
def _normalize_turkish_currency(md: str) -> str:
    # Range: ₺N1 - ₺N2 → N1–N2 TL (with en-dash)
    md = re.sub(r"₺([\d,.]+)\s*[–-]\s*₺([\d,.]+)", r"\1–\2 TL", md)
    md = re.sub(r"([\d,.]+)\s*[–-]\s*₺([\d,.]+)", r"\1–\2 TL", md)
    md = re.sub(r"₺([\d,.]+)\s*[–-]\s*([\d,.]+)", r"\1–\2 TL", md)
    # Single: ₺N → N TL
    md = re.sub(r"₺([\d,.]+)", r"\1 TL", md)
    md = md.replace("₺", "TL")
    return md

def assemble_markdown() -> str:
    # ... existing logic ...
    return _normalize_turkish_currency("".join(parts))
```

See `book-turkey/build.py` for the full implementation.

---

## 5. Pandoc `+smart` does not convert hyphens in numeric ranges to en-dashes

**Symptom:** Paperback PDF shows `300-400 lira` (hyphen) where `300–400 lira` (en-dash) is correct.

**Cause:** Pandoc `+smart` converts `--` → `—` (em-dash) and `----` → `—` (multi-em), but single hyphens between digits are left as-is.

**Fix:** Include in the build-time normalizer:
```python
# Hyphens in numeric currency ranges → en-dashes
md = re.sub(
    r"(\b[\d,.]+)-([\d,.]+\s*(?:TL|TRY|lira|euro|euros|€|\$|RMB|\u00a5|peso))",
    r"\1–\2",
    md,
)
md = re.sub(r"(\$[\d,.]+)-(\$?[\d,.]+)", r"\1–\2", md)
```

---

## 6. Rsvg-convert emits PDFs in pixels, not inches

**Symptom:** `pdfinfo` shows `Page size: 12.968 × 9.250 pts` — but the cover should be that dimension in INCHES, not points.

**Cause:** When the outer SVG uses `width="1314.5" height="925.0"` (SVG units), rsvg-convert interprets those as pixels at 96 DPI, which maps to PDF points weirdly.

**Fix:** Declare SVG dimensions with explicit physical units on the outer `<svg>`:
```python
svg = f"""<svg width="{total_w_in}in" height="{total_h_in}in"
     viewBox="0 0 {total_w} {total_h}" ...>"""
```
This makes the PDF's MediaBox exactly `total_w_in × total_h_in`.

See `book-spain/scripts/build_paperback_cover.py` line 178-180.

---

## 7. KDP wraparound cover dimension math

**Given:** 6×9 trim, 0.125" bleed, N pages, cream paper.

**Math:**
- `per_page = 0.0025" (cream) or 0.002252" (white)`
- `spine = pages × per_page`
- `total_w = 0.125 + 6 + spine + 6 + 0.125 = 12.25 + spine`
- `total_h = 0.125 + 9 + 0.125 = 9.25`

**Check your output:** `pdfinfo` reports `Page size: (total_w × 72) × (9.25 × 72) pts`. For 358 cream pages: `13.145 × 9.25 = 946.44 × 666 pts`.

**KDP cover calculator** at https://kdp.amazon.com/en_US/cover-calculator — verify your numbers against its output before upload.

---

## 8. Markdown single-newline collapses in Thai/Chinese phrase cards

**Symptom:** Phrase card lines like:
```
**No, thank you.**
不要,谢谢。
Bù yào, xièxie.
*Boo yow, shyeh-shyeh.*
```
render on a single line in the PDF.

**Cause:** Markdown treats consecutive single-newlines as spaces. Pandoc's `+hard_line_breaks` is NOT enabled by default.

**Fix:** Add 2 trailing spaces to every line in the phrase card where you want a hard break:
```markdown
**No, thank you.**  ← 2 spaces here
不要,谢谢。  ← 2 spaces
Bù yào, xièxie.  ← 2 spaces
*Boo yow, shyeh-shyeh.*
```

This was fixed for the Thailand book via a scripted `sed` pass that added 2-space trailing markers to the entire phrase card.

---

## 9. The GitHub worktree + PR merge dance

**Symptom:** `gh pr merge --delete-branch` fails with `fatal: 'main' is already used by worktree at '/Users/bjh/Documents/tabiji'`.

**Cause:** gh uses git locally to switch branches during merge; the main worktree (not this one) has main checked out.

**Fix:** The *remote-side* merge succeeds even though the local step fails. Verify:
```bash
gh pr view <PR-NUMBER> --json state,mergedAt
# Expect: "state": "MERGED"
```

Then manually clean up the remote branch:
```bash
git push origin --delete claude/<branch-name>
```

Local branch stays checked out in this worktree and cannot be deleted while this worktree is active; the main worktree will clean it up later. That's fine.

---

## 10. Corrupt git refs from prior worktree operations

**Symptom:** `git fetch origin main` fails with `bad object refs/remotes/origin/main 2` (literally with a space-and-2 appended).

**Cause:** macOS Finder duplicated a `.git/refs/remotes/origin/main` file when the repo was `.zip`-backed-up or synced via iCloud.

**Fix:**
```bash
git update-ref -d "refs/remotes/origin/main 2"
git update-ref -d "refs/stash 2"  # sometimes this too
git fetch origin main
```

Add the Finder-duplicate pattern to `.gitignore` (already done in this repo):
```gitignore
*\ [0-9].*
*\ [0-9]
```

---

## 11. Files get edited mid-session by a linter or side process

**Symptom:** `Edit` tool fails with `File has been modified since read, either by the user or by a linter. Read it again before attempting to write it.`

**Fix:** Re-Read the file, then retry the Edit. Don't panic — the changes are almost always trivial (a linter re-formatted whitespace or a background cron touched it). If the Edit target string no longer matches, use a larger-context Edit or switch to Bash + sed.

---

## 12. City-name diacritics drop from the upstream JSON but must appear in the book

**Symptom:** `api/v1/scams/malaga.json` has `"city": "Malaga"` (no accent), but the book should display **Málaga**.

**Fix:** Don't modify the upstream JSON. Instead, add a display-name override in `book-<country>/build.py`:
```python
def city_display_name(slug: str, data: dict) -> str:
    DISPLAY = {
        "malaga": "Málaga",
        "cordoba": "Córdoba",
        "xian": "Xi'an",
        "kusadasi": "Kuşadası",
        # ...
    }
    if slug in DISPLAY:
        return DISPLAY[slug]
    return data.get("city", slug.title()).strip()
```

Already implemented in `book-spain/build.py`, `book-china/build.py`, `book-turkey/build.py`.

---

## 13. Long H2 scam titles truncate the running header

**Symptom:** A scam with a long name like "Puerto del Carmen & Playa Blanca Restaurant & Beach-Strip Overcharge" shows up as `PUERTO DEL CARMEN & PLAYA BLANCA RESTAURANT & BEACH-STRIP O` (truncated mid-word) in the running header.

**Fix:** Either shorten the H2 scam title in the source JSON, or add a manual `\markright{shorter}` directive. For a one-off, the manual override in the page's LaTeX is simpler. For a common pattern, raise the trim width or the running-header font size.

---

## 14. Wavespeed cover generation content-filters

**Symptom:** Certain prompt words trigger Wavespeed's safety filter and the generation fails: "Negresco-era" (brand-like), "Sultan" (religious tension risk in Turkey), "drug test" (drug content).

**Fix:** Rephrase to avoid trigger words:
- "Negresco-era pink-domed grand hotel" → "a pink-domed grand hotel silhouette"
- "Sultan-era" → "Ottoman-era"
- "drug test" → "urine-sample check"

Keep the semantic detail; change the exact trigger word.

---

## 15. Parallel agent audits are much faster than sequential

**Observation:** Running 3 publisher audits sequentially takes ~8-10 minutes. Running them in parallel (one message, three Agent tool calls) takes ~3-4 minutes and the cumulative output is better because the agents reason independently.

**Use this pattern:**
```python
# Single message, three tool calls:
Agent(description="Audit 1 — content", ..., run_in_background=True)
Agent(description="Audit 2 — typography", ..., run_in_background=True)
Agent(description="Audit 3 — voice", ..., run_in_background=True)
```

While they run, work on site page copy, hub updates, or anything unrelated. Don't idle-block.

---

## 16. Raw JSON scam prose reads as gibberish without the polish module

**Symptom:** Built EPUB/paperback has `(comments/a1b2c3)` URL fragments sprinkled through every chapter, scam descriptions render as 2,000-char single paragraphs, and "avoidance" fields render as unbroken run-on walls of text. Readers (and KDP reviewers) will flag this as unpolished, URL-stuffed, and unprofessional.

**Cause:** The upstream JSON scam data carries Reddit-URL citation fragments from the synth pipeline (`r/SouthEastAsia 'comments/pqz72r' thread`) and stores each field as a single newline-free string because it was generated from a structured prompt.

**Fix:** Every build.py MUST import the polish module and call it on each scam field before render. `scripts/polish_scam_prose.py` ships with the skill templates:

```python
# Top of build.py, after HERE/BUILD constants:
sys.path.insert(0, str(HERE / "scripts"))
from polish_scam_prose import polish_description, polish_avoidance, polish_location  # noqa: E402

# Inside scam_md():
description = polish_description(scam["description"])
avoidance = polish_avoidance(scam["avoidance"])
location = polish_location(scam["location"])
parts.extend([
    f'### How this scam works\n\n{description}\n\n',
    f'### How to avoid it\n\n{avoidance}\n\n',
    f'**Where it happens:** {location}\n\n',
])
```

The module does three transforms:

1. `strip_reddit_fragments()` — removes `(comments/HASH)` and `(comments/HASH, YEAR)` patterns.
2. `break_description_paragraphs()` — inserts `\n\n` before strong sub-pattern signal phrases like "A separate variant", "Another 2024 version", "The defence is", "For older travellers, the practical defence:", "Crucially:".
3. `bulletize_avoidance()` — splits a single-paragraph avoidance string into a markdown bullet list using a curated list of imperative/conditional starter words (Use, Book, Verify, NEVER, ALWAYS, If, For, When, etc.). Returns the original string if fewer than 2 plausible bullets are detected.

**Verification after rebuild:** `grep -c "comments/[a-z0-9]" build/manuscript.md` should return 0. `grep -c "^- " build/manuscript.md` should return roughly 5-8× the scam count (multiple bullets per scam).

**When to extend the starter word list:** if a bullet in the output runs two imperatives together without a period (e.g. "Use the metro Be alert at turnstiles"), add the missing starter word to `_AVOIDANCE_BULLET_STARTERS`. When a description has a new sub-pattern signal phrase that didn't get a paragraph break, add it to `_DESCRIPTION_PARA_BREAKS`.

---

## 17. Patching existing build.py files — never write `\\n\\n` in a Python patch script

**Symptom:** After a bulk regex patch, `python3 -c "import ast; ast.parse(open('build.py').read())"` raises `SyntaxError: EOL while scanning string literal` on lines that used to contain `\n\n` inside an f-string.

**Cause:** A Python patch script written as `text.replace(old, "\\n\\n")` in the *source* of the patcher passes the literal 4-character sequence `\n\n` to `.replace`. But if the patcher is written as a single-quoted literal `'\\n\\n'`, those backslashes get processed by Python's string interpretation and the replacement becomes real newlines — corrupting the target file.

**Fix:** When using `Edit` tool for this, hand-write the before/after strings. When using a Python script, use a raw string for both sides of the replacement: `r'\n\n'` — or prefer the Edit tool, which sidesteps the escaping problem entirely.

**Verification:** After any patch to build.py, always run:
```bash
python3 -c "import ast; ast.parse(open('build.py').read()); print('OK')"
```
If that fails, read the file and look for f-strings that span multiple lines where they should be single-line with `\n\n` escapes.

---

## 18. KDP paperback rejection — insufficient gutter + text outside margins

**Symptom:** After uploading a 6"×9" paperback PDF to KDP, their print previewer rejects with two errors:

1. **"This text is outside the margins"** on a long list of pages (often 20-30+ pages). Running headers show long scam titles being cut off mid-word like `FAKE PRADO MUSEUM & ROYAL PALACE 'SKIP-THE-LINE' TICKET` ⚠ or `CÓRDOBA JUDERÍA PICKPOCKETS & PATIO-FESTIVAL CROWD TH` ⚠.
2. **"Insufficient gutter. Books with 324 pages require at least 0.625" for the gutter (inside margin)..."** on specific page numbers.

**Cause:** Two unrelated issues that compound:

1. **Uniform geometry.** The default pandoc+xelatex command uses `-V geometry:margin=0.75in` which sets all four sides to 0.75" — no twoside distinction between inside (gutter, spine-side) and outside. Technically 0.75" > 0.625" so KDP *should* accept it, but their validator is strict about explicit inner/outer declarations.
2. **Default LaTeX running header.** `book.cls` shows `\leftmark` (chapter name) OR `\rightmark` (section name, which is the scam title at H2) in the running head — and my earlier `\@schapter` override added `\MakeUppercase{#1}` which forced section marks to ALL-CAPS. Scam titles like "Fake Prado Museum & Royal Palace 'Skip-the-Line' Ticket Scam" become way too wide for a 4.5" running header line and overflow.

**Fix (pandoc command — Spain/China/Turkey xelatex books):**

```python
# Replace `-V "geometry:margin=0.75in"` with explicit twoside geometry:
"-V", "geometry:paperwidth=6in",
"-V", "geometry:paperheight=9in",
"-V", "geometry:inner=0.875in",  # gutter — KDP min 0.625" for 151-400 pp
"-V", "geometry:outer=0.5in",    # outer — KDP min 0.25"
"-V", "geometry:top=0.75in",     # room for running head
"-V", "geometry:bottom=0.75in",  # room for page number
"-V", "classoption=twoside",     # ensures inner/outer are respected
"-V", "documentclass=book",
```

Text block becomes (6 - 0.875 - 0.5) = 4.625" at 11pt ≈ 62 chars, which is in the 60-75 char optimal readability range.

**Fix (header-includes.tex — running head):**

Use `fancyhdr` with chapter-only running heads in mixed case:

```latex
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE]{\small\nouppercase{\leftmark}}
\fancyhead[RO]{\small\nouppercase{\leftmark}}
\fancyfoot[LE,RO]{\thepage}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\fancypagestyle{plain}{%
  \fancyhf{}%
  \fancyfoot[LE,RO]{\thepage}%
  \renewcommand{\headrulewidth}{0pt}%
}

% Unnumbered chapters ({-}) — store the mark without uppercase so fancyhdr
% renders it mixed-case to match numbered-chapter heads.
\makeatletter
\let\origschapter\@schapter
\def\@schapter#1{\origschapter{#1}\markboth{#1}{#1}}
\makeatother
\renewcommand{\chaptermark}[1]{\markboth{#1}{}}
\renewcommand{\sectionmark}[1]{}  % section mark unused
```

Long chapter names like "Santiago de Compostela" (22 chars) always fit; long scam names never appear in the header.

**Fix (URL + long-word line breaks):**

Add `xurl` and `seqsplit` packages to allow line-breaks in long URLs like `tickets.alhambra-patronato.es` that would otherwise overflow bullet margins:

```latex
\usepackage{xurl}
\usepackage{seqsplit}
\tolerance=3000
\emergencystretch=3em
```

**TinyTeX installation:** If the build fails with `! LaTeX Error: File 'fancyhdr.sty' not found.`, install the packages:

```bash
export PATH=$PATH:~/Library/TinyTeX/bin/universal-darwin
tlmgr install fancyhdr xurl seqsplit
```

**WeasyPrint books (Indonesia, Vietnam, Canada):** these already have proper KDP gutter in their CSS (`@page :right { margin-left: 0.875in; margin-right: 0.5in; }` + `@page :left`) and no LaTeX running header, so they're unaffected. Only the xelatex books (Spain/China/Turkey) need this fix.

**Verification:** after rebuilding, extract text from a previously-problematic page and confirm the running head is a clean chapter name:

```bash
pdftotext -layout -f 115 -l 115 build/spain-scams-paperback.pdf - | head -3
# Expected: "Córdoba" (or whatever chapter that page belongs to),
#           NOT "CÓRDOBA JUDERÍA PICKPOCKETS & PATIO-FESTIVAL CROWD TH..."
```

---

## 19. NEVER scaffold a new book by copying from another `book-<country>/` — always copy from `templates/`

**Symptom:** You build the KDP paperback, upload it, and KDP rejects with `"This text is outside the margins"` on 20+ pages plus `"Insufficient gutter. Books with N pages require at least 0.625"..."` — all the gotcha #18 symptoms — even though gotcha #18 documents the fix and the skill's canonical template already has the fix applied.

**Cause:** You scaffolded `book-<newcountry>/` by copying scripts from a previously-shipped `book-<oldcountry>/` folder. The shipped books still carry their original pre-fix scripts (book-turkey's `build_paperback_interior.py` pre-dates gotcha #18; its `templates/header-includes.tex` only has 14 lines and no fancyhdr + no xurl). Each shipped book is frozen at its ship date; the canonical fixes live in `.claude/skills/book-generator/templates/` ONLY.

**Fix — DISPATCH policy:** When scaffolding a new country book, the canonical source of build scripts + LaTeX + CSS is the skill's `templates/` directory, not any shipped `book-X/` folder:

```bash
BG=book-<country>

# CORRECT: copy from skill templates
cp .claude/skills/book-generator/templates/scripts/build.py.template                     $BG/build.py
cp .claude/skills/book-generator/templates/scripts/build_paperback_interior.py.template  $BG/scripts/build_paperback_interior.py
cp .claude/skills/book-generator/templates/scripts/build_paperback_cover.py.template     $BG/scripts/build_paperback_cover.py
cp .claude/skills/book-generator/templates/scripts/polish_scam_prose.py.template         $BG/scripts/polish_scam_prose.py
cp .claude/skills/book-generator/templates/scripts/gen_city_illustrations.py.template    $BG/scripts/gen_city_illustrations.py
cp .claude/skills/book-generator/templates/scripts/gen_comics.py.template                $BG/scripts/gen_comics.py
cp .claude/skills/book-generator/templates/build-templates/style.css                     $BG/templates/style.css
cp .claude/skills/book-generator/templates/build-templates/header-includes.tex           $BG/templates/header-includes.tex

# WRONG — DO NOT DO THIS (may pick up pre-fix scripts):
cp book-turkey/scripts/*.py                                                              $BG/scripts/
cp book-turkey/templates/header-includes.tex                                             $BG/templates/
```

Then personalize only the country-specific parts (CITY_ALT_TEXT, city_display_name DISPLAY dict, currency normalizer if needed, Polizei/Policía placeholder).

**Verification after scaffolding:** run the same checks from gotcha #18:

```bash
# Header should have fancyhdr + xurl:
grep -c "fancyhdr\|xurl\|seqsplit" book-<country>/templates/header-includes.tex
# Expected: 3 or more. If 0, you got the old version — re-copy from templates/.

# Build script should use twoside geometry with inner/outer, NOT uniform margin:
grep -cE "geometry:inner|classoption=twoside" book-<country>/scripts/build_paperback_interior.py
# Expected: 2+. If 0, you got the old uniform `margin=0.75in` — re-copy.
```

**Retro-fix for Germany (this case — 2026-04-21):** I had scaffolded `book-germany/` by copying from `book-turkey/`, which inherited:
- `templates/header-includes.tex` with only `\@schapter` + TOC override (no fancyhdr, no xurl, UPPERCASED marks).
- `scripts/build_paperback_interior.py` with `geometry:margin=0.75in` (uniform).
KDP flagged 20+ pages with `"text outside margins"` and page 78 with `"insufficient gutter"`. Fix: overwrote both files with the skill's canonical versions; rebuilt; 300 → 298 pages; running heads now mixed-case short chapter names ("Berlin", "Hamburg", "How to Use This Book") that always fit within margins.

---

## Gotcha #20 — Cover SVG with no `<image>` layer + missing `assets/covers/` fallback in `extract_inner` = silent text-only Kindle/wraparound covers (Australia case, 2026-04-27)

**Symptom:** Kindle cover JPG ships at ~470 KB and shows the title/subtitle/stat-badge text floating over a sky-to-ochre gradient — no Wavespeed-generated cover artwork composited behind it. Same effect on the paperback wraparound: text overlays render correctly but the watercolor scene is gone.

**Two independent bugs combine to produce this:**

1. **`assets/svg/front.svg` and `back.svg` were hand-built without `<image xlink:href="front.jpg" .../>`** referencing the Wavespeed art at all. When the SVG is just `<rect fill="url(#gradient)"/>` + text, rsvg-convert renders exactly that — no artwork to inline.

2. **`build_paperback_cover.py:extract_inner`'s base64-inlining loop only checks `source_svg_dir / href`** (i.e., `assets/svg/`), but `gen_comics.py` writes the artwork to `assets/covers/`. So even if the SVG correctly references `xlink:href="front.jpg"`, the inliner can't find it and silently leaves the bare `xlink:href="front.jpg"` in the composed output. rsvg-convert then drops it (gotcha #3).

**Australia hit both at once:** the SVG had no `<image>` tag (bug #1), so even after the SVG was fixed to embed `<image xlink:href="front.jpg"/>`, the wraparound STILL came out text-only because of bug #2. Two fixes were needed.

**Fix shipped (#1018):**

- **Restructure both SVGs** to use `<image xlink:href="front.jpg" x="0" y="0" width="500" height="800" preserveAspectRatio="xMidYMid slice"/>` as the first painted element, with a `<linearGradient>` top fade band for title legibility and (for the back cover) a full-bleed dark scrim so the dense back-copy text remains readable over the watercolor.

- **Patch `build.py:render_cover()`** with the canonical base64-inlining version (book-spain/book-turkey have it; older books like Australia's pre-shipped version did not). The function must base64-inline `<image href>` to a data URI before passing to rsvg-convert.

- **Patch `build_paperback_cover.py:extract_inner`** to fall back to `BOOK / "assets" / "covers" / href` when `source_svg_dir / href` doesn't exist. Without this fallback the wraparound silently strips the cover art even when the SVG is correct.

Both `templates/scripts/build.py.template` and `templates/scripts/build_paperback_cover.py.template` in the skill carry the fix as of 2026-04-27. Older book-X/ directories (created before 2026-04-21 for Spain, before 2026-04-27 for Australia's pre-shipped variant) may carry the pre-fix versions and need the same retro-patch.

**Confirmed case 2026-04-30 — Malaysia Vol 17 retrofit (#1313 forthcoming):** Malaysia shipped 2026-04-22 with the *exact same combination of all three sub-bugs as Australia*: (1) front.svg + back.svg were hand-built as Yusof-Gajah gradient designs with NO `<image>` tag, (2) build.py's render_cover() lacked base64 inlining, (3) build_paperback_cover.py's extract_inner() lacked the assets/covers/ fallback. KDP's automated cover-QA preview flagged the resulting cover ("text blends with background, blocked by elements"). The retrofit applied the canonical templates verbatim plus regenerated the comic-style watercolor (Peranakan/Nyonya pastel: KLIA2 teksi-sapu front, George Town shophouse back). Total fix-cycle: ~30 min once the diagnosis was clear. Lesson: when a book ships with non-comic-scene cover art (decorative-frame skyline view, gradient-only design) it almost certainly also has the corresponding pipeline bugs because the SVG is the visible artifact of "we never wired the Wavespeed art in." Audit the SVG → build.py → cover-builder chain together, not separately.

**Why audits don't catch this:** the publisher-audit prompts (Phase 6) inspect the EPUB and paperback PDF for content/typography/voice — they don't load the cover JPG. Phase 5 now contains an explicit cover-art verification step (see book-generator.md) that catches both bugs before audits run:

```bash
# 1. Both SVGs reference the Wavespeed art via <image href>
grep -cE '<image[^>]+(xlink:)?href=' book-<country>/assets/svg/front.svg book-<country>/assets/svg/back.svg
# Expected: 1 1

# 2. build.py base64-inlines the <image> hrefs
grep -c "base64.b64encode" book-<country>/build.py
# Expected: ≥ 1

# 3. build_paperback_cover.py falls back to assets/covers/
grep -c 'assets" / "covers"' book-<country>/scripts/build_paperback_cover.py
# Expected: ≥ 1

# 4. Composed wraparound SVG actually contains the inlined image data
grep -c "data:image" book-<country>/build/<country>-paperback-cover.svg
# Expected: ≥ 2 (front + back)

# 5. Kindle JPG file size is plausible — text-only renders ~470 KB,
#    real watercolor-with-overlay renders are 800–1200 KB
ls -la book-<country>/assets/cover.jpg
```

If any check returns 0/0 or the Kindle JPG is suspiciously small, fix BEFORE Phase 6 audits — they will not catch this.

---

## Gotcha #21 — Cover-overlay tagline goes invisible against light watercolor sky bands (Morocco case, 2026-04-27)

**Symptom:** The "A TRAVELER'S FIELD GUIDE · MMXXVI" line — and any other cream-colored overlay text below the masthead — disappears into the watercolor cover art on books with light/saffron/peach sky bands. Cream `#F5E6CE` fill on pale-saffron watercolor sky has near-zero contrast.

**Cause:** The title text in the canonical SVG (book-australia/book-spain pattern) carries `style="paint-order: stroke; stroke: <deep-color>; stroke-width: 2.5px;"` for legibility, but the smaller subtitle/tagline lines under it do not. On covers where the underlying art is dark (Sydney evening, Istanbul golden-hour blue), the cream fill stays legible. On covers where the underlying art is light (Marrakech saffron sunset, Greek-island whitewash, any Atlantic-coast peach gradient), the tagline ghost-renders.

**Fix:** Add the same paint-order stroke pattern that the title uses to **every overlay text line below the masthead** in the front SVG — at minimum the tagline ("A TRAVELER'S FIELD GUIDE · MMXXVI") and the hook headline ("Don't Lose $X in Country"). Use the book's deepest palette color for the stroke (e.g., `#6E2210` deep burgundy for Morocco, `#0E5573` teal for Australia, `#1a0a0a` for any palette).

```svg
<!-- Before (Morocco V17, shipped with bug): -->
<text x="250" y="232" ... fill="#F5E6CE" ...>A TRAVELER'S FIELD GUIDE · MMXXVI</text>

<!-- After (post-fix #1032): -->
<text x="250" y="232" ... fill="#F5E6CE" ...
      style="paint-order: stroke; stroke: #6E2210; stroke-width: 2px;">A TRAVELER'S FIELD GUIDE · MMXXVI</text>
```

**When to apply:** Apply preemptively to every new book SVG. The cost is two extra characters of XML per text line; the cost of NOT applying is shipping a Kindle cover that's invisible at thumbnail size.

**Verification:** Open the rendered Kindle JPG (book-X/assets/cover.jpg) at 50% zoom. If you cannot read the tagline + hook headline at thumbnail scale, retro-fit. There is no automated check — this requires eyeballing the rendered cover before Phase 6.

---

## Gotcha #22 — Stat-badge box too narrow for letter-spaced "DOCUMENTED SCAMS" text (Morocco case, 2026-04-27)

**Symptom:** "DOCUMENTED SCAMS" text overflows the right edge of the stat-badge rectangle on the front cover. Visible as the letter-spaced caption sitting wider than the gold framing box around the scam-count numeral.

**Cause:** The canonical SVG (copied from book-australia/book-spain pattern) uses `<rect width="116">` with letter-spacing="3" font-size="8" "DOCUMENTED SCAMS" inside. Rendered text width is ~128 units (16 chars × ~5px char + 3px spacing); rect is only 116. The text renders ~12 units wider than the box on each side, which reads as a sloppy mis-alignment.

**Fix:** Widen the rect to `width="144"` and shift `x="-72"` (keeps it centered around the `transform="translate(250 612)"` group):

```svg
<!-- Before (book-australia, book-spain — shipped with bug): -->
<g transform="translate(250 612)">
  <rect x="-58" y="-22" width="116" height="44" fill="none" stroke="#FFDDA6" stroke-width="1" rx="2"/>
  <text x="0" y="-2" ... font-size="22" ...>61</text>
  <text x="0" y="14" ... font-size="8" letter-spacing="3">DOCUMENTED SCAMS</text>
</g>

<!-- After (post-fix #1032): -->
<g transform="translate(250 612)">
  <rect x="-72" y="-22" width="144" height="44" fill="none" stroke="#FFDDA6" stroke-width="1" rx="2"/>
  <text x="0" y="-2" ... font-size="22" ...>61</text>
  <text x="0" y="14" ... font-size="8" letter-spacing="3">DOCUMENTED SCAMS</text>
</g>
```

The `61` numeral is unaffected — it's centered at x=0 and stays exactly where it was.

**When to apply:** Always, when copying the SVG pattern from any reference book. The 116-width version is the legacy Australia/Spain pattern; 144 is the corrected width.

**Verification:** Same as #21 — eyeball the rendered cover. The stat box outline should sit ~5–10 units wider than the letter-spaced text on each side.

**Optional pre-flight grep:** If you want to catch the legacy width during scaffolding, after copying the SVG add:

```bash
grep -E '<rect[^>]*width="116"' book-<country>/assets/svg/front.svg
# Expect 0 hits. Any match → widen to 144 before render.
```

---

## Gotcha #23 — Cover front MUST be a comic-style scam-in-action scene, not a decorative-frame skyline (Malaysia Vol 17 case, 2026-04-30)

**Symptom:** A shipped book has a front cover that is a *decorative-framed skyline view* (Petronas Towers + peony border + empty negative space at top for the title) instead of the series-canonical *full-bleed comic-style scam-in-action scene* (a tourist + a scammer + a recognizable landmark + a speech bubble of the scam line). The cover passes the build pipeline because it has correct dimensions and text overlays; it just doesn't match the series quality bar set by Egypt (camel-handler "Free photo" scam at Giza), Australia (KLIA-style taxi-tout "$48 + $85 mate" at Sydney harbor), Turkey (Sultanahmet shoe-shine brush drop). KDP's automated cover-QA preview later flags it for legibility because there's no scene context — just text floating in negative space.

**Cause:** When a book scaffolder writes `gen_comics.py` with a "scenic landmark + decorative border" prompt instead of "scam in action with two figures + speech bubble + landmark", the resulting cover misses the series identity. The book-generator.md Phase 2.5 wording says "depicting a flagship scam in action" but at that level of generality it's easy to mis-interpret as "a representative landmark scene of the country."

**Fix — make Phase 2.5 prompt requirements explicit:**

The front-cover Wavespeed prompt MUST contain ALL of these elements:

1. **A clearly-female-or-male tourist figure** (matches one of the 4 canonical cast: Margie 62F, Priya 34F, Harry 64M, Marcus 34M). Specify hat, suitcase, posture.
2. **A scam perpetrator in a recognizable role** for the scam (taxi tout, vendor, "free photo" guide, etc.).
3. **A speech bubble with the actual scam-line in English** (e.g., "Meter rosak — RM 250, special airport rate", "Free photo, just one minute!", "Plus airport top-up — eighty-five mate").
4. **A recognizable local landmark visible in the background** (Petronas Towers, pyramids, Opera House, Hagia Sophia).
5. **Generous empty sky / negative space in the upper third** for the title overlay.
6. **A darker band across the lower fifth** for the hook overlay (this is what the dark gradient overlay in the SVG sits over).

The back cover is moody and atmospheric — no characters, no speech bubble, just the destination at golden hour with substantial empty sky for back-cover copy.

**Verification:** before merging the gen_comics.py prompt, read the prompt aloud and confirm: does it describe a *scene where someone is being scammed right now*? If the prompt only describes a landmark or a vista, rewrite it.

**Why audits don't catch this:** publisher-audit prompts (Phase 6) inspect the EPUB and paperback PDF for content/typography/voice — they don't load the cover JPG and they don't compare it against the Egypt/Australia quality bar. The only catch-points are (a) explicit Phase 2.5 prompt requirements (above), (b) eyeballing the rendered cover before Phase 9 deploy, and (c) the KDP-side cover-QA preview, which is post-upload (too late — fix-cycle costs a re-upload + retry).

**Confirmed case 2026-04-30:** Malaysia Vol 17 shipped with a Peranakan-framed Petronas-skyline cover (decorative border, empty negative space, no scam scene) plus the gotcha #20 pipeline bugs. KDP cover-QA flagged it. Retrofit regenerated the comic art (KLIA2 taxi-tout + female tourist + "Meter rosak — RM 250" speech bubble + Petronas Towers + KLIA control tower) and rewrote both SVGs to the full-bleed Egypt/Australia template. ~30-minute fix once diagnosis was clear. The interior PDF + manuscript were untouched — only the cover changed.

---

## Gotcha #24 — `bleed_colors` must synergize with the cover-art palette, not be picked from a generic country flag (Malaysia Vol 17 case, 2026-04-30)

**Symptom:** The KDP wraparound cover renders with a bleed gradient (the spine background + the 0.125" outer-trim margins on front + back) in colors that visually clash with the cover art. Common pattern: cover art is a soft pastel watercolor (Peranakan/Nyonya pinks + mints, Italian terracotta + olive, Spanish saffron + indigo) and the bleed gradient is an unrelated saturated brand pair (marigold→teal, navy→gold). The eye reads the spine as a *separate piece* glued onto the wraparound, not as a continuous part of the art.

**Cause:** `book-<country>/config.yaml` carries a `bleed_colors:` 2-item list that the wraparound build script reads. When this is set during scaffolding before the cover art exists (or set to a generic country-flag pair like Yusof-Gajah marigold/teal for Malaysia), the colors don't pick up the dominant tones the eventual cover ends up using.

**Fix — pick `bleed_colors` AFTER the front + back cover art is rendered, not before:**

1. Open the rendered front.jpg + back.jpg (the Wavespeed output, not the composed SVG).
2. Identify the two dominant tonal poles:
   - **Top color**: a deeper, more saturated version of the warm tones that dominate the upper half of the cover (the sky band — usually corals, peaches, ochres, sand-golds).
   - **Bottom color**: a deeper version of the cool tones in the lower half (the foreground/landmarks — usually teals, deep blues, plums, forest greens).
3. Both colors must be saturated enough to keep the cream spine title (`#F5E9D3`, font-weight 700) legible against the gradient mid-band.

**Reference palettes shipped:**

| Country | bleed_colors | Why |
|---|---|---|
| Egypt (Vol 4) | `#C9A24A` → `#1F4E6B` | Sand-gold pyramid-light → Nile-blue night |
| Australia (Vol N) | `#1B7FA8` → `#E8A454` | Deep harbor-sky → golden-sand ochre |
| Turkey (Vol 9) | (check book-turkey/config.yaml) | Ottoman pottery palette |
| Malaysia retrofit (2026-04-30) | `#C68870` → `#2F5E5A` | Heritage rose terracotta (Peranakan tile clay) → deep Peranakan teal (heritage ceramic mint) — picks up pink shophouse tones at top + mint shophouse accents at bottom |

**Don't pick:**
- Pure flag colors (e.g., Malaysia's red-blue-yellow flag would look garish next to Peranakan pastels).
- Two highly-saturated complementary primaries (e.g., marigold→teal) when the cover is a soft pastel — the spine will scream and the cover will whisper.
- Two colors of similar luminance — the spine title needs gradient contrast to read; cream text needs the mid-band to be at least 50% darker than the cream.

**Verification:** render the wraparound to JPG (`pdftoppm -r 100 ... -jpeg -f 1 -l 1`) and view it next to the rendered front.jpg/back.jpg. The spine + bleed should feel like a continuous tonal frame around the watercolor, not a separate stripe.

**Confirmed case 2026-04-30:** Malaysia Vol 17 shipped with `bleed_colors: ["#E8A454", "#1DA5A0"]` (Yusof Gajah marigold + tropical teal) — chosen during scaffolding when the planned art style was Yusof-Gajah-flat-color. The actual shipped cover used Peranakan/Nyonya pastel watercolor, which clashed with the saturated marigold/teal spine. Retrofit replaced with `["#C68870", "#2F5E5A"]` (heritage rose terracotta → Peranakan teal). Spine title remained legible, and the gradient now reads as a natural extension of the watercolor scenes.
