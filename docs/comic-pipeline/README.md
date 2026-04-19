# Scam Comic Pipeline

Per-scam 2x2 comic illustrations on tabiji country scam pages
(`tabiji.ai/scams/country/<cc>/` and each city page underneath).

Every country gets a **culturally-anchored visual style**, a **shared cast of
four canonical protagonists**, and the **same Nano Banana Pro generation
pipeline**. This folder documents everything needed for another agent (or a
human) to generate a new batch of comics without re-deriving the system.

## Status

| Country | Style | Comics live | File |
|---|---|---:|---|
| Thailand | Warm watercolor storybook | 50 | [styles/thailand.md](styles/thailand.md) |
| France | Hergé / Tintin ligne-claire | 191 | [styles/france.md](styles/france.md) |
| Greece | Ancient red-figure pottery | 41 | [styles/greece.md](styles/greece.md) |
| Spain | Paco Roca contemporary graphic novel | pending | [styles/spain.md](styles/spain.md) |
| Austria | Jean-Jacques Sempé pen-and-ink wash | 8 | [styles/austria.md](styles/austria.md) |
| Hong Kong / China | Shaw Brothers 1960s-70s painted cinema poster | — | [styles/hong-kong.md](styles/hong-kong.md) |
| Croatia | Ivan Generalić / Hlebine School naïve-art | — | [styles/croatia.md](styles/croatia.md) |
| Japan | Manga (planned) | — | — |
| USA | American comic book (planned) | — | — |
| Italy | Fumetti / bande dessinée (planned) | — | — |

## What to read in this folder

Start here and branch out:

- **[cast.md](cast.md)** — the 4 canonical protagonists (Margie, Priya, Harry, Marcus), with the verbatim paragraphs to paste into every prompt and the scam-type pairing rules. Read this first.
- **[pipeline.md](pipeline.md)** — the generator (Nano Banana Pro via Wavespeed), R2 storage, HTML injection pattern, cache-busting, and rate-limit handling. Read this second.
- **[prompt-template.md](prompt-template.md)** — the 3-block prompt format (`STYLE` + `CHARACTER` + `SCENE`) and per-panel dialogue rules. Read this third.
- **[styles/](styles/)** — one file per country, each with the locked STYLE block verbatim. Copy-paste from the target country's file.

## Quick-start for a new country

1. Pick a culturally-anchored illustration style (bake off 3–5 candidates — see [style-exploration.md](style-exploration.md))
2. Create `styles/<country>.md` with the locked STYLE block
3. Generate the **first** comic via `text-to-image` (no reference image yet)
4. Confirm the style is right with the user
5. Generate the rest via `edit` with 2–3 approved prior comics as `images` anchors (tighter style lock than text-to-image)
6. Upload to R2 at `scams/<city>/scam-<N>.jpg`
7. Inject the img tag into each city's `index.html`
8. Commit, open PR, merge, deploy

## Core principles

1. **Style is locked per country, cast is shared cross-country.** Each country is visually distinct; each protagonist is visually identical wherever they appear.
2. **Dialogue is always in English.** Readability for the global audience beats linguistic authenticity.
3. **Protagonist pairing is by scam type.** Margie on trust scams, Priya on transit/rental/accommodation, Harry on authority/charm/ATM, Marcus on nightlife/beach/street games. See [cast.md](cast.md).
4. **Panel 4 is always the lesson.** The protagonist walks away wiser, reports to Tourist Police, or demonstrates the safer alternative.
5. **Cache-bust with `?v=2` when replacing existing images.** R2 bucket has a Cloudflare CDN cache; overwriting a file does not invalidate the cache. Append `?v=2` (or higher integer) to the `src` in HTML.
