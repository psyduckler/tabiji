# Compare Page Audit — 2026-03-27

Scope:
- audited the compare-page inventory and the most recently updated compare pages surfaced by `tabiji/api/v1/compare.json`
- checked compare leaf files against inventory files (`compare/index.html`, `api/v1/compare.json`, `sitemap.xml`)
- checked recent pages for anchor/TOC consistency and obvious content/template defects

## Executive summary

The recent compare pages are close to the locked shell, but the compare system has three real consistency problems:

1. **Inventory files are badly out of sync**
   - `tabiji/compare/` leaf pages: **450**
   - `tabiji/api/v1/compare.json` entries: **172**
   - `tabiji/compare/index.html` linked compare cards: **87**
   - `tabiji/sitemap.xml` compare URLs: **455**

2. **The two newest API-listed pages are inconsistent with the shell in different ways**
   - `hpa-an-vs-inle-lake` has a **literal template-token anchor bug** (`${id}`)
   - `taichung-vs-tainan` has a **broken TOC link** to a missing `#the-decision-framework` section

3. **`api/v1/compare.json` quality is inconsistent**
   - **62 entries** are malformed relative to the newer entry shape
   - some are missing `id`, `type`, and/or `updatedAt`
   - this makes the feed mixed-format and harder to trust downstream

## Recent-page findings

### 1) `tabiji/compare/hpa-an-vs-inle-lake/index.html`

Status: publishable but not clean.

Findings:
- The page includes a broken literal anchor token: **`${id}`**
- That indicates a templating/render step leaked into final HTML instead of resolving
- The rest of the page structure is generally aligned with the compare shell: hero, verdict, quick comparison, deep-dive sections, decision framework, FAQ, CTA

Impact:
- broken in-page navigation / JS behavior
- looks sloppy in production markup
- suggests the page generator is not escaping/rendering consistently

### 2) `tabiji/compare/taichung-vs-tainan/index.html`

Status: stronger prose than average, but structurally inconsistent.

Findings:
- TOC links to `#the-decision-framework`
- there is **no matching element with `id="the-decision-framework"`** on the page
- the page also contains an obvious unresolved fare placeholder in FAQ copy:
  - `"(NT, ~ USD)"`
  - `"(NT–260, ~–8 USD)"`
- that is a hard content-quality defect, not just style

Impact:
- broken TOC behavior
- undermines trust because fare data visibly failed to render

## Inventory inconsistencies

### Compare leaf files vs API

- **285 compare pages exist on disk but are missing from `tabiji/api/v1/compare.json`**
- examples:
  - `abel-tasman-vs-milford-sound`
  - `abu-dhabi-vs-ras-al-khaimah`
  - `addis-ababa-vs-simien-mountains`
  - `al-ula-vs-jeddah`
  - `algarve-vs-costa-brava`

Impact:
- compare API is incomplete
- anything consuming the API gets a partial universe
- internal tooling and category pages can’t reliably reflect production inventory

### Compare leaf files vs compare index

- **365 compare pages exist on disk but are not linked from `tabiji/compare/index.html`**
- the index meta description still says **"157 data-backed destination comparisons"**, while the directory has **450** compare leaf pages

Impact:
- the compare hub dramatically under-represents available pages
- meta copy is stale and misleading
- recent pages are effectively buried even if live

### Compare leaf files vs sitemap

- Sitemap is the only inventory file that appears broadly complete
- all file-backed compare slugs checked were represented in `tabiji/sitemap.xml`

Interpretation:
- the publishing process is updating sitemap more reliably than the compare index or API
- inventory generation is fragmented instead of coming from one source of truth

## API schema inconsistencies

`tabiji/api/v1/compare.json` contains a mixed entry format.

Malformed count found: **62** entries.

Examples:
- `gangneung-vs-sokcho` missing `id`, `type`, `updatedAt`
- `hpa-an-vs-inle-lake` missing `id`, `type`
- `shimokitazawa-vs-golden-gai` missing `id`, `type`, `updatedAt`
- `luang-prabang-vs-siem-reap` missing `id`, `type`, `updatedAt`
- `hue-vs-hoi-an` missing `id`, `type`, `updatedAt`

Impact:
- downstream consumers have to support multiple shapes
- sorting/filtering by freshness becomes unreliable
- mixed-format inventory is usually a sign that part of the catalog bypassed the normal generation path

## Broader structural problems found outside the two newest pages

I also ran a broad anchor-target pass across compare pages.

Result:
- **37 pages** have TOC/anchor mismatches or leaked template placeholders

Examples:
- missing `#the-decision-framework` target:
  - `otaru-vs-hakodate`
  - `pushkar-vs-jodhpur`
  - `bali-vs-vietnam`
  - `kamakura-vs-nikko`
  - `taichung-vs-tainan`
  - `gangneung-vs-sokcho`
- leaked template tokens:
  - `${active.id}` on `bangkok-vs-ho-chi-minh`, `dubai-vs-bangkok`, `hue-vs-hoi-an`, others
  - `${id}` on `hpa-an-vs-inle-lake`, `bagan-vs-luang-prabang`, `alishan-vs-taroko-gorge`, others
  - `"'+id+'"` / similar JS-string leakage on `seoul-vs-taipei`, `scotland-vs-ireland`

This is not random copy noise. It looks like **multiple page-generation variants** are writing slightly different shells and some are emitting raw template tokens into final HTML.

## Priority fixes

### P0 — fix immediately
- `tabiji/compare/taichung-vs-tainan/index.html`
  - add or restore the missing `the-decision-framework` section, or remove the TOC link
  - fix broken fare placeholders in FAQ copy
- `tabiji/compare/hpa-an-vs-inle-lake/index.html`
  - remove/fix leaked `${id}` anchor token

### P1 — fix next
- normalize `tabiji/api/v1/compare.json` so every entry has:
  - `id`
  - `type`
  - `slug`
  - `title`
  - `destination1`
  - `destination2`
  - `url`
  - `updatedAt`
  - `sourceUrl`
  - `tags`
- rebuild `tabiji/compare/index.html` from the same source used for sitemap/API
- update compare hub metadata/count copy to reflect actual inventory

### P2 — systemic cleanup
- standardize compare-page generation on one locked shell based on `tokyo-vs-kyoto`
- add a validation step that fails generation when:
  - a TOC anchor has no matching target id
  - raw template tokens like `${id}` survive in output
  - FAQ copy contains unresolved currency placeholders
  - compare page exists on disk but is missing from API/index/sitemap inventories

## Recommendation

Do **not** keep manually patching compare pages one by one.

The real problem is that compare pages are being produced by **more than one generation path** or by one path with inconsistent templates. The right move is:

1. patch the two newest broken pages now
2. rebuild the compare inventory from disk
3. add a validator so bad pages cannot ship again

## Useful headline numbers

- compare pages on disk: **450**
- compare API entries: **172**
- compare index cards: **87**
- compare sitemap entries: **455**
- API entries with mixed/malformed shape: **62**
- compare pages with anchor/TOC mismatches found in broad pass: **37**
