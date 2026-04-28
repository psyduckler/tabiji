---
name: general-scams-article
description: |
  Produce a single deeply-researched, audited, deployed article in /scams/everywhere/ from the existing Reddit research corpus. Implements the workflow we used for the pig-butchering page (PR #1187): research → plan → build → 8-pass audit → hub-update → deploy.

  Trigger on: "/general-scams-article <slug>", "produce a general scams article", "write a /scams/everywhere page", or any request to author a new general (non-travel) scam page.
type: project-skill
invocation: /general-scams-article <slug>
---

# General-Scams Article Producer

## What this skill does

Produces a single article at `/scams/everywhere/<slug>/index.html` plus all
required supporting changes (hub update, sitemap regen, LLMs.txt entry,
internal cross-links, schema validation, deploy + merge). The output target
is a 10/10 stellar, well-researched, accurate, non-hallucinating article
with maximum SEO/AI-search visibility.

## Origin

This skill encodes the workflow that produced [PR #1187 (pig-butchering article)](https://github.com/psyduckler/tabiji/pull/1187)
and [PR #1190 (nav link)](https://github.com/psyduckler/tabiji/pull/1190),
audited 3x for execution / quality / SEO and iterated until each dimension
passed 9+/10.

## Inputs

A slug from the Coming-Soon list on `/scams/everywhere/`. Currently
supported (per `corpus-mapping.json`):

- `ai-voice-clone-scams`
- `bank-impersonation-and-zelle`
- `tech-support-scams`
- `package-text-scams` (USPS / FedEx / Amazon)
- `real-estate-wire-fraud`
- `fake-job-offers`
- `marketplace-scams-fb-craigslist`
- `medicare-and-elder-scams`
- `recovery-scams`
- `gift-card-scams`
- `concert-and-event-ticket-scams`
- `sextortion`
- `door-to-door-contractor-scams`

Add more by editing `corpus-mapping.json` and `source-mapping.json`.

## Outputs (atomic, single PR)

1. `/scams/everywhere/<slug>/index.html` — flagship 6,000–8,500-word page
2. `/scams/everywhere/index.html` — hub updated (slug moved Coming Soon → Live Guides)
3. `sitemap.xml` — regenerated
4. `llms.txt` + `llms-full.txt` — entry added
5. Other `/scams/everywhere/<sibling>/index.html` pages — Related Reading sections updated to cross-link to the new page
6. `sources.md` sidecar at `tmp/scam-skill/<slug>/sources.md` (gitignored audit trail)

## Hard checkpoints (the skill stops and waits for you here)

- **After Stage 1** — research summary + variant cluster proposal
- **After Stage 2** — final plan with audit scores
- **After Stage 4** — finished page + 8-pass audit report
- **Before merge** — explicit user authorization to merge

## How to invoke

```
/general-scams-article ai-voice-clone-scams
```

The skill will read this directory, walk through the 8 stages, and stop at
each checkpoint for your approval.

## File map

| File | Purpose |
|---|---|
| `SKILL.md` | This file (entrypoint) |
| `workflow.md` | The 8 stages in detail with exact commands |
| `page-anatomy.yaml` | The 15-section page template with slot definitions |
| `variant-template.yaml` | Per-variant micro-template (7 elements) |
| `voice-rules.md` | Voice + tone rules + AI-tic anti-patterns |
| `audit-checklists/pass-1-clarity.md` | Pass 1 checks |
| `audit-checklists/pass-2-voice.md` | Pass 2 checks |
| `audit-checklists/pass-3-design.md` | Pass 3 checks |
| `audit-checklists/pass-4-authority.md` | Pass 4 checks |
| `audit-checklists/pass-5-grammar.md` | Pass 5 checks |
| `audit-checklists/pass-6-source-reread.md` | Pass 6 checks (re-fetch sources) |
| `audit-checklists/pass-7-accessibility.md` | Pass 7 WCAG AA checks |
| `audit-checklists/pass-8-ai-tics.md` | Pass 8 anti-AI-pattern grep |
| `corpus-mapping.json` | slug → corpus-keys (in `tmp/scam_research/corpus.json`) |
| `source-mapping.json` | slug → required federal/NGO/industry/press sources |
| `helpers/extract_top_threads.py` | Pull top-N threads from corpus, sorted by relevance |
| `helpers/update_hub.py` | Move slug from Coming Soon → Live Guides on hub |
| `helpers/archive_urls.py` | Submit cited URLs to archive.org for permanence |
| `helpers/verify_anti_tics.py` | Pass 8 automated grep |
| `README.md` | Quickstart for first-time use |

## State persistence (resume)

Per-build state is written to `tmp/scam-skill/<slug>/state.json` after each
stage. Resuming is automatic if the state file exists.

## Source-of-truth corpus

The Reddit research corpus is at `tmp/scam_research/corpus.json` (39 categories,
276 threads, 3,769 comments — produced by the original research run).
The skill reads from this corpus; it does not perform fresh Reddit searches
unless the user explicitly requests an update.
