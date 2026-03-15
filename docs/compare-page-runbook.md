# Compare-page runbook

Use this runbook for work on `compare/*` pages and their supporting inventory files.

## Core rule

Produce artifacts, not status theater.

Do not say a compare-page task is underway unless you have already done at least one of these:
- written or edited a file
- generated a page or support file
- run validation
- created a commit or PR

## Locked compare-page standard

Use `compare/tokyo-vs-kyoto/index.html` as the shell reference.

Every compare leaf should preserve this page shape:
1. shared head/meta/social/schema
2. shared nav
3. hero
4. sticky TOC
5. TL;DR verdict
6. quick comparison table
7. deep-dive sections
8. decision framework
9. FAQ
10. CTA
11. shared footer

Canonical shared sources:
- `_includes/shared-head.html`
- `_includes/nav-main.html`
- `_includes/footer-default.html`

Required schema/meta expectations:
- canonical
- title + meta description
- OG tags
- Twitter tags
- `Article` JSON-LD
- `BreadcrumbList` JSON-LD
- `FAQPage` JSON-LD
- `speakable` in `Article` when used by the active standard

## Build workflow

### 1) Anchor on the reference

Before editing, inspect:
- `compare/tokyo-vs-kyoto/index.html`
- target compare page(s)
- `compare/index.html`
- `api/v1/compare.json`
- `sitemap.xml`

If the task is standardization or migration, compare the target page against `tokyo-vs-kyoto` first.

### 2) Decide the work type

Use one of these paths:

- **New compare page**: create a new compare leaf and add supporting inventory references
- **Standardization/migration**: normalize an existing compare page to the locked shell
- **Inventory pruning/rebuild**: remove or re-add compare pages and keep index/API/sitemap in sync

### 3) Apply the shell consistently

Normalize these first:
- TOC behavior and anchors
- verdict box
- comparison table
- decision framework
- FAQ section
- CTA section
- shared-nav/footer expectations
- metadata/schema consistency

Preserve topic-specific deep-dive headings where they still fit the compare shell.

### 4) Update supporting files

When adding a page, update all of:
- `compare/index.html`
- `api/v1/compare.json`
- `api/v1/compare/<slug>.json` if that system is in use
- `sitemap.xml`
- any API examples or docs that need the new slug

When removing a page, remove all of the same references.

### 5) Validate before claiming progress

Minimum validation:
- confirm no obvious broken references to the slug
- confirm compare index/API/sitemap are in sync
- confirm schema blocks still exist
- confirm expected shell elements exist on the page

Prefer quick scripted validation over eyeballing when possible.

### 6) Commit cleanly

Use clear commits for meaningful progress. Examples:
- `Define compare-page runbook and production checklist`
- `Create compare page: <slug>`
- `Normalize compare shell on <slug>`
- `Update compare inventory for <slug>`

## Gold-standard production checklist

Use this checklist for any new compare page.

### Inputs
- comparison topic is actually worth publishing
- slug is final
- destination names are final
- evidence/research packet is present or source material is identified
- image plan is known

### Page
- leaf page created at `compare/<slug>/index.html`
- follows locked compare shell
- hero is present
- verdict box is present
- quick comparison table is present
- deep-dive sections are coherent and useful
- decision framework is present
- FAQ is present
- CTA is present

### Metadata + schema
- canonical correct
- title correct
- meta description correct
- OG tags correct
- Twitter tags correct
- `Article` JSON-LD present
- `BreadcrumbList` JSON-LD present
- `FAQPage` JSON-LD matches on-page FAQ
- `speakable` present if required by current shell

### Inventory
- compare card added/updated in `compare/index.html`
- aggregate entry added/updated in `api/v1/compare.json`
- per-page API JSON added/updated if required
- sitemap updated
- API docs/examples updated if needed

### Validation
- slug references are consistent
- no stale references to old slugs
- no missing required sections
- no obviously broken internal anchors
- files staged cleanly

### Shipping
- commit made
- branch pushed
- PR opened when requested

## What to report back

Report only artifact-level progress, for example:
- file created
- checklist completed
- validation passed
- commit hash
- PR URL

Bad update: “I’m working on it.”
Good update: “Runbook written in `docs/compare-page-runbook.md`, checklist included, committed as `<hash>`.”
