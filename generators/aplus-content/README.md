# A+ Content kit generator

Builds an Amazon KDP **A+ Content** kit for any book in the Travel Safety Series,
leveraging that country's existing city scam comics from `img.tabiji.ai`.

A+ Content is uploaded by hand in KDP's A+ Content Manager: you pick a module
type, type text into its fields, and upload an image at that module's exact
pixel size. This tool produces everything you paste/upload.

## Usage

```bash
python3 generators/aplus-content/build_aplus.py book-china
```

Output (gitignored, under the book's `build/`):

```
book-china/build/aplus/
  kit.html        # visual preview — open in a browser, eyeball before submitting
  copy.md         # every module's headline / body / alt-text, paste-ready
  img/            # upload-ready PNGs at exact KDP dimensions
    1-logo.png    2-hero.png    3-tile-{1..4}.png    4-feature.png
```

## The 5-module template (standard, non-Premium A+)

| # | KDP module | Image | Content |
|---|------------|-------|---------|
| 1 | Standard Company Logo | 600×180 | Tabiji owl + wordmark |
| 2 | Standard Image Header With Text | 970×300 | Hero — cover-scene comic + baked title; KDP headline shows above |
| 3 | Standard Four Image & Text | 4× 300×300 | The comic showcase — four distinct scam archetypes, each captioned |
| 4 | Standard Multiple Image Module A | 300×300 | One comic + the "what's inside" value stack |
| 5 | Standard Product Description Text | — | Closing trust block (text only) |

Comics are 16:9-ish square (1024²) and cover-crop cleanly to KDP's squares. The
generator reads each comic's URL **and caption from the live scam page**
(`scams/<city>/index.html`), so the Nth comic always matches scam N, version
cache-busts included.

> KDP text fields are plain text — apply bold/bullets with the editor toolbar,
> don't paste HTML. Module names vary slightly by account; match by description.
> This template avoids the Comparison Chart module on purpose (it requires other
> ASINs as columns, which would cross-sell away from the book).

## Per-book config: `book-<country>/aplus.yaml`

China is the first instance. To make a kit for another book, copy
`book-china/aplus.yaml`, swap the copy, and point each module's `comic`/`tiles`
at that country's cities + scam numbers (1-based, matching the scam page order):

```yaml
book:   { title: "...", subtitle: "..." }
brand:  { logo_url: ..., wordmark: TABIJI, series: Travel Safety Series }
modules:
  - type: logo
  - type: hero
    headline: "..."          # KDP text field, renders above the image
    title: "JAPAN"           # baked into the banner
    title_sub: "..."
    hook: "..."
    stat: "..."
    comic: { city: tokyo, n: 1 }
  - type: quad
    headline: "..."
    tiles:
      - { city: tokyo, n: 1, title: "...", body: "..." }   # x4
  - type: feature
    headline: "..."
    comic:   { city: osaka, n: 2 }
    bullets: ["Label — detail", ...]   # preview bolds the label before the em-dash
  - type: text
    headline: "..."
    body: "..."
```

`alt` text auto-resolves from the comic's caption when omitted.

## Requirements

`Pillow`, `pyyaml`. Comics are fetched from `img.tabiji.ai` and cached under
`build/aplus/.cache/`. Fonts use macOS system Georgia/Arial, falling back to
Pillow's default if absent (e.g. in CI).
