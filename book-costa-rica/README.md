# Book generator — Tabiji Travel Safety Series · Costa Rica volume

Build the Kindle EPUB from structured Costa Rica scam data (`api/v1/scams/*.json`) plus
hand-written manuscript markdown.

## Quickstart

```bash
pip3 install pyyaml
python3 book-costa-rica/build.py
```

Output: `book-costa-rica/build/costa-rica-scams.epub`

## Directory layout

```
book-costa-rica/
  config.yaml              # title, subtitle, 11 cities in reading order
  build.py                 # the generator (verbatim copy from book-italy/)
  manuscript/              # hand-written chapters
    01-copyright.md        # copyright + disclaimer
    02-introduction.md     # "how to use this book"
    03-red-flag-patterns.md# the 6 universal patterns for Costa Rica
    04-cities-section.md   # gallery intro + <!-- CITIES --> insertion marker
    90-appendix-phrase-card.md  # Costa Rican Spanish exit phrases
    91-appendix-recovery.md     # post-scam playbook (911 → OIJ → embassy → chargeback)
    92-appendix-contacts.md     # emergency contacts (police, ICT, SINAC, US Embassy, hospitals)
    95-about.md                 # about Tabiji
    99-cta.md                   # review CTA + series tease
    cities-<slug>-intro.md      # per-city intros (one per city in config.yaml)
  templates/
    style.css              # Kindle-friendly CSS
  scripts/                 # general-purpose helpers (polish_scam_prose, gen illustrations, paperback layout)
  assets/
    cover.jpg              # KDP-spec 1600x2560 JPG (produced from svg/front.svg)
    svg/                   # cover source (front.svg, back.svg)
    cities/<slug>.jpg      # per-city chapter-opener illustrations
    images/<slug>/NN.jpg   # per-scam illustrations (optional)
  build/                   # generator output (gitignored)
```

## How city chapters are generated

The string `<!-- CITIES -->` in any manuscript file triggers auto-insertion of
one chapter per city in the order defined by `config.yaml`. Chapter content
for each city is drawn from `api/v1/scams/<slug>.json`, one section per scam.

To add a written intro for a specific city, drop a file in the manuscript folder
named `cities-<slug>-intro.md` (e.g. `cities-quepos-intro.md`). The build picks
it up automatically.

## Cities covered (v2 — 11 destinations, 69 scams)

Reading order is capital → Arenal → cloud forest → Central Pacific arc → Nicoya tip → Guanacaste gateway → Caribbean / eco:

1. San José
2. La Fortuna (Arenal volcano)
3. Monteverde (cloud forest)
4. Manuel Antonio
5. Quepos
6. Jacó
7. Tamarindo
8. Santa Teresa
9. Liberia (LIR airport)
10. Tortuguero
11. Puerto Viejo de Talamanca

## Validating

```bash
# Install epubcheck (requires Java):
brew install epubcheck

# Check EPUB:
epubcheck book-costa-rica/build/costa-rica-scams.epub
```

## TODOs (v2 expansion, 2026-04-27)

The book was originally shipped at 8 cities / 54 scams; this scaffold expands to
11 cities / 69 scams by adding **Quepos**, **Santa Teresa**, and **Tortuguero**.
The following are out of scope for the scaffold step but required before reship:

- **Cover regeneration** — `assets/svg/front.svg` and `assets/svg/back.svg`
  hardcode "54 DOCUMENTED SCAMS" and "8 CITIES" and use the v1 turquoise-Pacific
  palette. Regenerate at the new emerald-rainforest palette specified in
  `config.yaml` (`bleed_colors: ["#0F4D2E", "#082A1A"]`) with the v2 counts
  ("69 DOCUMENTED SCAMS", "11 DESTINATIONS").
- **City illustrations** — `assets/cities/quepos.jpg`,
  `assets/cities/santa-teresa.jpg`, and `assets/cities/tortuguero.jpg` need to
  be generated to match the existing 1950s Pan American tropical-deco
  travel-poster style of the eight v1 city plates.
- **Paperback re-spine** — interior page count grows from 184 to ~220+; rerun
  `scripts/build_paperback_interior.py` and `scripts/build_paperback_cover.py`
  with the updated spine width.
- **Phrase-card native review** — Appendix A is in Costa Rican Spanish but
  should be sanity-checked by a native CR Spanish speaker before reship.

Run `python3 build.py` and the summary lists remaining `**TODO**` markers.
All TODOs must be resolved before KDP submission.
