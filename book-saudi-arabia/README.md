# Book generator — Tabiji Travel Safety Series (Saudi Arabia)

Build the Kindle EPUB from structured scam data (`api/v1/scams/*.json`) plus
hand-written manuscript markdown.

## Quickstart

```bash
pip3 install pyyaml
python3 build.py
```

Output: `build/saudi-arabia-scams.epub` — 64 scams across 10 cities.

## Directory layout

```
book-saudi-arabia/
  config.yaml              # title, author, cities in reading order
  build.py                 # the generator
  manuscript/              # hand-written chapters
    01-copyright.md            # copyright + disclaimer
    02-introduction.md         # "how to use this book"
    03-red-flag-patterns.md    # the 6 universal patterns
    04-cities-section.md       # intro + <!-- CITIES --> insertion marker
    cities-<slug>-intro.md     # per-city written intro (riyadh, jeddah, …)
    90-appendix-phrase-card.md # Saudi Arabic exit phrases
    91-appendix-recovery.md    # post-scam playbook
    92-appendix-contacts.md    # emergency contacts (999 / 997 / 998)
    95-about.md                # about Tabiji
    99-cta.md                  # review CTA + series tease
  templates/
    style.css              # Kindle-friendly CSS
  assets/
    cover.jpg              # KDP-spec JPG (rendered from svg/front.svg)
    svg/                   # Al-Qatt Al-Asiri folk-art cover source (front.svg, back.svg)
    images/<city>/         # full-color city plates per chapter
  build/                   # generator output (gitignored)
```

## How city chapters are generated

The string `<!-- CITIES -->` in any manuscript file triggers auto-insertion of
one chapter per city in the order defined by `config.yaml`. Chapter content
for each city is drawn from `../api/v1/scams/<city>.json`, one section per scam.

The ten cities, in reading order — capital, then the Hejaz pilgrimage corridor,
then the northwest heritage sites, then the Asir south, then the Gulf east:

| City | Slug | Scams |
|---|---|---|
| Riyadh | `riyadh` | 6 |
| Jeddah | `jeddah` | 7 |
| Mecca | `mecca` | 6 |
| Medina | `medina` | 6 |
| Taif | `taif` | 6 |
| AlUla | `alula` | 6 |
| Tabuk | `tabuk` | 7 |
| Abha | `abha` | 7 |
| Dammam | `dammam` | 6 |
| Al-Khobar | `al-khobar` | 7 |
| **Total** | | **64** |

To add a written intro for a specific city, drop a file in the manuscript folder
named `cities-<slug>-intro.md` (e.g. `cities-alula-intro.md`). The build picks
it up automatically.

## Swapping volumes (other regions, other countries)

The generator is data-driven. For a new volume:

1. Copy `book-saudi-arabia/` to a new directory or branch.
2. Update `config.yaml` — title, subtitle, cities list, output filename, bleed colors.
3. Rewrite the front-matter markdown (intro, red-flag patterns for that region).
4. Run `python3 build.py`.

The per-scam rendering is reused for free.

## Validating

```bash
# Install epubcheck (requires Java):
brew install epubcheck

# Check EPUB:
epubcheck build/saudi-arabia-scams.epub
```

## TODO gates

Run `python3 build.py` and the summary lists remaining `**TODO**` markers.
All TODOs must be resolved before KDP submission.
