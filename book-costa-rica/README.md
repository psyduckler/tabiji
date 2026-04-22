# Book generator — Tabiji Travel Safety Series

Build the Kindle EPUB from structured scam data (`app/data/scams/*.json`) plus
hand-written manuscript markdown.

## Quickstart

```bash
pip3 install pyyaml
python3 book/build.py
```

Output: `book/build/japan-scams.epub`

## Directory layout

```
book/
  config.yaml              # title, author, cities in reading order
  build.py                 # the generator
  manuscript/              # hand-written chapters
    00-title.md            # title page
    01-copyright.md        # copyright + disclaimer
    02-introduction.md     # "how to use this book" — STUB
    03-red-flag-patterns.md# the 6 universal patterns — STUB
    04-cities-section.md   # intro + <!-- CITIES --> insertion marker
    90-appendix-phrase-card.md  # Japanese exit phrases — STUB, native-speaker review required
    91-appendix-recovery.md     # post-scam playbook — STUB
    92-appendix-contacts.md     # emergency contacts — STUB
    95-about.md                 # about Tabiji — STUB
    99-cta.md                   # review CTA + series tease
  templates/
    style.css              # Kindle-friendly CSS
  assets/
    cover.jpg              # KDP-spec 1600x2560 JPG (produced from Desktop SVG)
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
