# book-dental — The Dental Tourism Field Guide

Source files and build pipeline for **The Dental Tourism Field Guide**, a
consumer-protection field guide for cost-shocked patients considering dental
work abroad. This is a different format from the country-scam books in this
repo — single long-form manuscript, ~52,000 words, designed as a 6×9" trade
paperback and Kindle ebook.

**Editor:** Bernard Huang
**Publisher:** Tabiji
**Companion site:** [tabiji.ai/book/dental](https://tabiji.ai/book/dental)
**Status as of last commit:** v2 elaborate-CSS pass complete; ready for human
clinical/copy/legal review then KDP upload.

---

## Directory layout

```
book-dental/
├── README.md                      ← this file
├── DESIGNER-BRIEF.md              ← typesetter spec (callout boxes, pull quotes, etc.)
├── amazon-listing.md              ← KDP metadata (title, subtitle, description, keywords, categories)
├── manuscript/
│   └── 00-the-dental-tourism-field-guide.md   ← canonical source (~52k words)
├── assets/
│   ├── css/
│   │   ├── print-style.css        ← v2 CSS for paperback PDF (callout boxes, etc.)
│   │   └── epub-style.css         ← v2 CSS for EPUB
│   └── svg/
│       ├── cover-front.svg        ← chosen front cover (Direction 2: Field Guide aesthetic)
│       ├── cover-wrap.svg         ← full wrap cover (back + spine + front, KDP bleed)
│       └── cover-prototypes/      ← 5 cover concepts explored, kept for reference
│           ├── 1-kitchen-table.svg
│           ├── 2-field-guide.svg
│           ├── 3-pause.svg
│           ├── 4-typography.svg
│           ├── 5-redacted.svg
│           └── index.html         ← side-by-side comparison page
├── scripts/
│   ├── build.sh                   ← rebuild all KDP-ready artifacts
│   └── preprocess.py              ← adds pandoc semantic divs to manuscript
└── build/                         ← generated output (gitignored)
    ├── manuscript-source.md       ← HTML-comments-stripped manuscript
    ├── manuscript-processed.md    ← + pandoc fenced divs from preprocess.py
    ├── manuscript.html            ← intermediate HTML
    ├── kindle-cover.jpg           ← final Kindle cover (1600×2400 sRGB)
    ├── cover-1600x2400.png        ← intermediate PNG
    ├── the-dental-tourism-field-guide.epub  ← Kindle upload file
    ├── paperback-interior.pdf     ← KDP paperback manuscript upload
    └── paperback-wrap-cover.pdf   ← KDP paperback cover upload
```

---

## Quickstart — rebuild all KDP files

```bash
bash book-dental/scripts/build.sh
```

This regenerates everything in `book-dental/build/` from the source files in
`manuscript/`, `assets/svg/`, and `assets/css/`. Takes about 10 seconds.

### Tool requirements

```
pandoc        ≥ 3.0      (markdown → EPUB / HTML)
weasyprint    ≥ 60       (HTML + CSS → paperback PDF)
rsvg-convert             (SVG → PNG / PDF for covers)
sips                     (PNG → JPG for Kindle cover; macOS built-in)
python3       ≥ 3.10     (preprocess.py)
```

On macOS via Homebrew: `brew install pandoc weasyprint librsvg`

---

## What the build pipeline does

```
manuscript/00-the-dental-tourism-field-guide.md
        │
        │ 1. Strip HTML <!-- designer comments -->
        ▼
build/manuscript-source.md
        │
        │ 2. preprocess.py adds pandoc fenced divs:
        │    ::: {.scenario}, ::: {.decision-gate}, ::: {.green-flags}, etc.
        ▼
build/manuscript-processed.md
        │
        ├──► pandoc + epub-style.css ──► EPUB
        │
        └──► pandoc → HTML + print-style.css ──► weasyprint ──► paperback PDF

assets/svg/cover-front.svg ──► rsvg-convert + sips ──► Kindle cover JPG
assets/svg/cover-wrap.svg  ──► rsvg-convert ──► paperback wrap cover PDF
```

---

## When to update the spine width

The wrap cover SVG includes a hard-coded spine width that depends on the
**interior page count**. KDP requires these to match exactly.

After running `build.sh`, the script prints the required spine width based
on the actual page count of the rebuilt interior PDF. If the printed
"required spine width" doesn't match the spine width baked into
`assets/svg/cover-wrap.svg`, edit the SVG and re-run.

**KDP spine formula:** `spine_inches = page_count × 0.002252` (60# white paper)

The wrap cover dimensions need to be recomputed and the PDF regenerated
whenever:
- The manuscript materially grows or shrinks
- The print stylesheet's margins/font sizes change (changes line breaks,
  which changes page count)

---

## What needs human review before KDP upload

These cannot be done by the build pipeline — see `DESIGNER-BRIEF.md` for full detail.

| Task | Owner | Estimate |
|---|---|---|
| Clinical review (practicing dentist) | external | $300–$800, 1 day |
| Professional copyedit | external | $1,500–$3,000, 1–2 weeks |
| Proofread after typesetting | external | $800–$1,500, 1 week |
| Legal review of disclaimers | external | $300–$600, 1 hour |
| Expand About the Editor with Bernard's bio | Bernard | 1 hour |
| 3–6 endorsement blurbs | outreach | varies |
| Cover designer refinement (Direction 2 + 1) | external | $1,500–$3,500, 2 weeks |

---

## Editing the manuscript

The canonical source is `manuscript/00-the-dental-tourism-field-guide.md`.
Edit this file directly — `build.sh` always reads from it.

The manuscript contains some HTML comments like `<!-- PULL QUOTE — designer:
extract the previous sentence … -->` which are designer instructions for
human typesetters. The build script strips these before generating the EPUB
and PDF, so they appear in the source but never in published output.

---

## KDP upload reference

| KDP field | File |
|---|---|
| Kindle eBook → Manuscript | `build/the-dental-tourism-field-guide.epub` |
| Kindle eBook → Cover | `build/kindle-cover.jpg` |
| Paperback → Manuscript | `build/paperback-interior.pdf` |
| Paperback → Cover | `build/paperback-wrap-cover.pdf` |

For all other KDP listing form fields (title, subtitle, description, keywords,
categories, pricing), copy from `amazon-listing.md`.

---

## History

- **2026-05-10:** Initial commit. Source manuscript transferred from
  `~/Desktop/the-dental-tourism-field-guide-COMPLETE.md`. Build pipeline
  designed around pandoc + weasyprint + rsvg-convert. Direction 2 (Field
  Guide aesthetic) chosen as the front cover. v2 elaborate CSS pass
  implements scenario callout boxes, pull quotes, color-coded green/yellow/red
  flag treatments, Decision Gate boxes, and the styled Journey Map.
