# A+ Content generator — Travel Safety Series

Renders Amazon KDP **A+ Content** assets for the tabiji.ai book series at exact KDP
pixel sizes, baking the "Field Guide" design into the images (so Amazon's generic
text rendering never shows). Each module image drops straight into KDP.

Validated on **China** and **Japan**. This is the pipeline that replaced the earlier
Pillow prototype.

## Setup (once)

```bash
cd generators/aplus-content
npm install                       # playwright + sharp (rendering)
npx playwright install chromium
pip3 install Pillow               # build_all.py (batch staging + JPG fallbacks)
```

## Build books → Desktop folders

```bash
python3 build_all.py                  # every spec in books/specs/ → Desktop folders
python3 build_all.py italy greece     # just these slugs
```

`build_all.py` reads each `books/specs/<slug>.json`, stages its comics + owl from
img.tabiji.ai, generates `templates/data.<slug>.jsx`, renders all modules via `generate.mjs`,
and assembles `~/Desktop/<Country> A+ Content - Ready to Upload/` (images + JPG fallbacks +
`KDP-copy.md` + README). A per-book compliance gate skips anything not A+-clean.

`generate.mjs <slug>` is the low-level renderer (Playwright + sharp, 2× supersampled →
exact size); build_all calls it. China & Japan also ship as hand-authored
`templates/data.{china,japan}.jsx` and render with `node generate.mjs china|japan`.

## The 5 modules (Set A "Field Guide")

| KDP module | Image | px |
|---|---|---|
| Standard Company Logo | logo lockup | **600 × 180** |
| Standard Image Header With Text | hero comic + title | **970 × 300** |
| Standard Four Image & Text | 4 comic tiles | **300 × 300** ×4 |
| Standard Multiple Image Module A | full baked module | **970 × 300** |
| Standard Product Description | full baked module | **970 × 300** |

> ④ and ⑤ are baked as **970 × 300** so they drop into the same image slot as the
> header (e.g. *Image & Dark Text Overlay* / *Image Header With Text*) — upload the
> image and leave KDP's overlay text fields **empty**. A `300 × 300` native variant of
> ④ is also emitted if you prefer the native module + pasted text.

## The spec is the source of truth

For the series batch, `books/specs/<slug>.json` is the only file you edit — copy, the six
comic CDN URLs (hero + inside + 4 tiles), accent, and stats. Everything downstream
(`data.<slug>.jsx`, staged art, rendered PNGs, the Desktop folder) is **generated and
disposable**. To **update a book** (new edition / new comics), edit its spec and re-run
`python3 build_all.py <slug>` — don't hand-edit rendered assets, regenerate them.

Each book uses a distinct accent (China terracotta `#A8472A`, Japan indigo `#34507F`,
Greece Aegean blue, Turkey Iznik turquoise, …). Comic URLs follow
`https://img.tabiji.ai/scams/{city}/scam-{n}.webp`. `export.jsx` reads two legacy slot keys
(`IMG.beijing2` = header hero, `IMG.shanghai1` = inside); build_all maps the spec onto them.

(China & Japan shipped earlier as committed `templates/data.{china,japan}.jsx` — equivalent
source. The 22 other books here are spec-driven.)

## Compliance (important)

Amazon A+ **prohibits** price, star ratings / review references, and
refund/guarantee/"free" wording — these get the submission rejected, and because the
text is baked into the image you can't fix it in KDP. Keep `desc.price`, `desc.badges`
and `desc.body` free of all of that (China/Japan are already clean).

## Art

Comics and the owl are **not committed** (repo policy: binary media lives on Cloudflare
R2 / img.tabiji.ai). `stage-art.mjs` fetches them into `templates/assets/source/` on
build — `generate.mjs <slug>` calls it automatically, or run `node stage-art.mjs <slug>`
yourself. To add a book, add its comic URLs to the `ART` map in `stage-art.mjs`.

## Files

```
build_all.py              batch: spec → stage art → render → Desktop folder (needs Pillow)
generate.mjs              exact-size exporter (Playwright + sharp); low-level renderer
stage-art.mjs             fetches comics + owl from img.tabiji.ai (CDN); ART map per book
books/specs/<slug>.json   ★ the spec — source of truth (copy + comic URLs + accent + stats)
templates/
  export.html export.jsx  the 5 modules as exact-size export tiles
  data.<slug>.jsx         GENERATED from the spec by build_all.py (gitignored)
  data.{china,japan}.jsx  hand-authored originals (committed)
  assets/source/*         staged from the CDN on build (gitignored)
out/<slug>/*.png          rendered assets (gitignored)
```
