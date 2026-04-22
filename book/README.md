# Book generator — Tabiji Travel Safety Series

Build the Kindle EPUB + KDP paperback PDF from structured scam data
(`app/data/scams/*.json`) plus hand-written manuscript markdown.

> **New to the pipeline?** Read [`POLISHING_GUIDE.md`](./POLISHING_GUIDE.md)
> first. It captures 15 volumes worth of KDP-rejection learnings in one
> place: prose sanitization, American-English consistency, Reddit-citation
> scrub patterns, mid-word-truncation repair, KDP gutter + cover safe-zone
> rules, the pandoc math-dollar bug fix, and the 3-pass copyedit workflow.

## Quickstart

```bash
pip3 install pyyaml
python3 book/build.py                                     # → build/japan-scams.epub
python3 book/scripts/build_paperback_interior.py          # → build/japan-scams-paperback.pdf
python3 book/scripts/build_paperback_cover.py --pages 320 # → build/japan-paperback-cover.pdf
```

The build pipeline automatically runs `scripts/polish_scam_prose.py` on every
JSON description/avoidance/location field AND one final sweep over the
assembled manuscript, so citation scaffolding / UK spellings / age-framing /
mid-word truncations get scrubbed without manual editing.

Output: `book/build/japan-scams.epub`

## Directory layout

```
book/
  POLISHING_GUIDE.md       # start here — the playbook for all 5 polish categories
  config.yaml              # title, author, cities in reading order
  build.py                 # Kindle EPUB generator (auto-runs polish_scam_prose.py)
  scripts/
    polish_scam_prose.py           # citation scrub + UK→US + age-framing + truncations
    build_paperback_interior.py    # KDP 6×9 paperback PDF (WeasyPrint or xelatex)
    build_paperback_cover.py       # KDP wraparound cover PDF from back.svg + front.svg
    gen_comics.py                  # per-scam 2×2 comic generator (Wavespeed / Nano Banana Pro)
    gen_city_illustrations.py      # per-city travel-poster generator
  manuscript/              # hand-written chapters
    00-title.md            # title page
    01-copyright.md        # copyright + disclaimer
    02-introduction.md     # "how to use this book"
    03-red-flag-patterns.md# the 6 universal patterns
    04-cities-section.md   # intro + <!-- CITIES --> insertion marker
    cities-<slug>-intro.md # optional per-city intro (e.g. cities-tokyo-intro.md)
    90-appendix-phrase-card.md  # local-language exit phrases
    91-appendix-recovery.md     # post-scam playbook
    92-appendix-contacts.md     # emergency contacts
    95-about.md                 # about Tabiji
    99-cta.md                   # review CTA + series tease
  templates/
    style.css              # Kindle-friendly CSS
    header-includes.tex    # xelatex header (fancyhdr + xurl + TOC fixes)
  assets/
    cover.jpg              # KDP-spec 1600×2560 JPG (auto-rebuilt from svg/front.svg)
    svg/
      front.svg            # vector front cover (editable; rasterized to cover.jpg)
      back.svg             # vector back cover (for paperback wraparound)
    cities/                # per-city chapter-opener JPGs
    images/<city>/NN.jpg   # per-scam 2×2 comic JPGs (gitignored, rebuild with gen_comics)
  build/                   # generator output (gitignored)
```

## How city chapters are generated

The string `<!-- CITIES -->` in any manuscript file triggers auto-insertion of
one chapter per city in the order defined by `config.yaml`. Chapter content
for each city is drawn from `app/data/scams/<city>.json`, one section per scam.

To add a written intro for a specific city, drop a file in the manuscript folder
named `cities-<slug>-intro.md` (e.g. `cities-tokyo-intro.md`). The build picks
it up automatically.

## Swapping volumes (Kyoto region, Southeast Asia, etc.)

The generator is data-driven. For a new volume:

1. Copy `book/` to a new directory or branch.
2. Update `config.yaml` — title, subtitle, cities list.
3. Rewrite the front-matter markdown (intro, red-flag patterns for that region).
4. Run `python3 build.py`.

The per-scam rendering is reused for free.

## Validating

```bash
# Install epubcheck (requires Java):
brew install epubcheck

# Check EPUB:
epubcheck book/build/japan-scams.epub
```

## TODO gates (as of v0.1 scaffold)

Run `python3 build.py` and the summary lists remaining `**TODO**` markers.
All TODOs must be resolved before KDP submission.
