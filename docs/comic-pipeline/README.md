# Scam Comic Pipeline

Per-scam 2x2 comic illustrations on tabiji country scam pages
(`tabiji.ai/scams/country/<cc>/` and each city page underneath).

Every country gets a **culturally-anchored visual style**, a **shared cast of
four canonical protagonists**, and the **same Nano Banana Pro generation
pipeline**. This folder documents everything needed for another agent (or a
human) to generate a new batch of comics without re-deriving the system.

## Status

29 countries with locked illustration styles. Comic counts as of 2026-04-26 (note: locked-style countries with 0 live comics are awaiting batch generation through the v2 pipeline).

| Country | Style | Comics live | File |
|---|---|---:|---|
| Argentina | Quino / Mafalda Argentine newspaper-strip | 0 | [styles/argentina.md](styles/argentina.md) |
| Australia | Percy Trompf / Gert Sellheim 1930s-50s art-deco travel poster | 84 | [styles/australia.md](styles/australia.md) |
| Austria | Jean-Jacques Sempé pen-and-ink wash | 8 | [styles/austria.md](styles/austria.md) |
| Brazil | Aldemir Martins folk-modernist | 72 | [styles/brazil.md](styles/brazil.md) |
| Canada | Drawn & Quarterly Toronto indie-comic | 75 | [styles/canada.md](styles/canada.md) |
| China | Feng Zikai poetic brush cartoon | 98 | [styles/china.md](styles/china.md) |
| Colombia | "Macondo" magical-realism watercolor | 33 | [styles/colombia.md](styles/colombia.md) |
| Costa Rica | 1950s Pan American Airways tropical-deco travel poster | 0 | [styles/costa-rica.md](styles/costa-rica.md) |
| Croatia | Ivan Generalić / Hlebine School naïve-art | 16 | [styles/croatia.md](styles/croatia.md) |
| France | Hergé / Tintin ligne claire | 191 | [styles/france.md](styles/france.md) |
| Germany | Heinrich Zille Berlin Milljöh observational | 88 | [styles/germany.md](styles/germany.md) |
| Greece | Ancient red-figure pottery | 41 | [styles/greece.md](styles/greece.md) |
| Egypt | Contemporary illustrated Egyptian travel-comic (warm watercolor + gouache) | 0 | [styles/egypt.md](styles/egypt.md) |
| Hong Kong | Shaw Brothers 1960s-70s painted cinema poster | 8 | [styles/hong-kong.md](styles/hong-kong.md) |
| India | Classical Mughal miniature painting (jewel-tone court ateliers) | 0 | [styles/india.md](styles/india.md) |
| Indonesia | Balinese Lontar palm-leaf manuscript | 73 | [styles/indonesia.md](styles/indonesia.md) |
| Italy | Warm hand-drawn travel-sketchbook (pencil + watercolor wash, yellow title banner) | 107 | [styles/italy.md](styles/italy.md) |
| Japan | Contemporary illustrated travel-comic (neon night + warm day) | 60 | [styles/japan.md](styles/japan.md) |
| Malaysia | Yusof Gajah vibrant naïve folk-art | 0 | [styles/malaysia.md](styles/malaysia.md) |
| Mexico | Lotería card / Don Clemente tarjeta | 60 | [styles/mexico.md](styles/mexico.md) |
| Morocco | Matisse Tangier-period vibrant watercolor (fauve color-as-emotion) | 0 | [styles/morocco.md](styles/morocco.md) |
| Portugal | José de Guimarães folk-pop modernist | 65 | [styles/portugal.md](styles/portugal.md) |
| Saudi Arabia | Contemporary illustrated Gulf travel-comic (Najd-pink heritage accents) | 0 | [styles/saudi-arabia.md](styles/saudi-arabia.md) |
| Spain | Paco Roca contemporary graphic novel | 103 | [styles/spain.md](styles/spain.md) |
| Thailand | Warm watercolor storybook | 3 | [styles/thailand.md](styles/thailand.md) |
| Turkey | Ottoman Iznik-tile + illustrated travel-comic | 78 | [styles/turkey.md](styles/turkey.md) |
| United Kingdom | Quentin Blake loose pen-and-watercolor (Roald Dahl illustrator) | 82 | [styles/united-kingdom.md](styles/united-kingdom.md) |
| United States | Silver-Age American superhero-comic-book (Kirby/Ditko) | 238 | [styles/united-states.md](styles/united-states.md) |
| Vietnam | Contemporary Vietnamese travel-comic with red lotus/cloud folk-art motifs | 72 | [styles/vietnam.md](styles/vietnam.md) |

## What to read in this folder

Start here and branch out:

- **[cast.md](cast.md)** — the 4 canonical protagonists (Margie, Priya, Harry, Marcus), verbatim paragraphs to paste into every prompt + scam-type pairing rules. Read this first.
- **[pipeline.md](pipeline.md)** — the image generator (Nano Banana Pro via Wavespeed), R2 storage, HTML injection pattern, cache-busting, rate limits. Read this second.
- **[prompt-synthesis.md](prompt-synthesis.md) ← current production pipeline (v2)** — per-scam bespoke prompt synthesis via Gemini 2.5 Pro. One scam at a time. Replaces the deprecated keyword-classified themed-template approach and is what all new batches must use.
- **[prompt-template.md](prompt-template.md)** — reference doc for the 3-block prompt format that Nano Banana Pro consumes. The format is unchanged in v2; only the way the SCENE block is authored changed (Gemini writes it per-scam).
- **[style-exploration.md](style-exploration.md)** — the 5-way bake-off process for picking a new country's style.
- **[styles/](styles/)** — one file per country, each with the locked STYLE block verbatim. Copy-paste from the target country's file.
- **[../../scripts/comic-pipeline/](../../scripts/comic-pipeline/)** — the runnable v2 pipeline code: `cast.py`, `styles.py`, `synthesize.py`, `generate.py`.

## Quick-start for a new country (v2)

1. **Pick a culturally-anchored illustration style.** Bake off 3–5 candidates on the same anchor scam. See [style-exploration.md](style-exploration.md) for the process and [styles/](styles/) for inspiration.
2. **Lock the winner.** Create `styles/<country>.md` with the verbatim STYLE block, and add it to `STYLES` + `PILOTS` in [`scripts/comic-pipeline/styles.py`](../../scripts/comic-pipeline/styles.py).
3. **Generate the pilot** (via `/text-to-image`, no reference yet). Upload to `scam-comics/<cc>/style-tests/`. Get user approval.
4. **Run the v2 pipeline to regenerate every scam** in every city:
   ```bash
   python3 scripts/comic-pipeline/generate.py <country> <city1> <city2> ... --force --batch-size 3
   ```
   This calls Gemini 2.5 Pro to synthesize each scam's bespoke script, submits to Nano Banana Pro with the locked style + pilot anchor, quality-gates each output, and uploads to R2.
5. **Review the flag log** (`/tmp/<country>-flagged.log`) — anything here needs manual attention.
6. **Inject img tags** into each city's `index.html` (pattern in [pipeline.md](pipeline.md)).
7. **Commit + PR + merge + deploy.**

## Core principles

1. **Style is locked per country, cast is shared cross-country.** Each country is visually distinct; each protagonist is visually identical wherever they appear.
2. **Dialogue is always in English.** Readability for the global audience beats linguistic authenticity.
3. **Protagonist pairing is by scam type.** Margie on trust scams, Priya on transit/rental/accommodation, Harry on authority/charm/ATM, Marcus on nightlife/beach/street games. See [cast.md](cast.md).
4. **Panel 4 is always the lesson.** The protagonist walks away wiser, reports to Tourist Police, or demonstrates the safer alternative.
5. **Cache-bust with `?v=2` when replacing existing images.** R2 bucket has a Cloudflare CDN cache; overwriting a file does not invalidate the cache. Append `?v=2` (or higher integer) to the `src` in HTML.
