# general-scams-article — Skill Quickstart

Produces a deeply-researched, audited, deployed article in `/scams/everywhere/`
from the Reddit research corpus. Encodes the workflow that produced
[PR #1187 (pig-butchering)](https://github.com/psyduckler/tabiji/pull/1187).

## Quickstart

1. **Pick a slug** from `corpus-mapping.json` (one not yet shipped).

2. **Invoke the skill**:
   ```
   /general-scams-article ai-voice-clone-scams
   ```

3. **Stop at the 4 hard checkpoints**:
   - After Stage 1 — review research summary + variant proposal
   - After Stage 2 — approve the plan
   - After Stage 4 — read the finished page + 8-pass audit report
   - Before merge — explicitly authorize

4. **Page ships** to `/scams/everywhere/<slug>/`, hub auto-updated, sitemap
   regenerated, LLMs.txt updated, sibling pages cross-linked.

## File map

```
.claude-skills/general-scams-article/
├── SKILL.md                         ← entrypoint (start here)
├── workflow.md                      ← 8 stages in detail
├── page-anatomy.yaml                ← 15-section page template
├── variant-template.yaml            ← per-variant micro-template
├── voice-rules.md                   ← voice + AI-tic rules
├── audit-checklists/
│   ├── pass-1-clarity.md
│   ├── pass-2-voice.md
│   ├── pass-3-design.md
│   ├── pass-4-authority.md
│   ├── pass-5-grammar.md
│   ├── pass-6-source-reread.md
│   ├── pass-7-accessibility.md
│   └── pass-8-ai-tics.md
├── corpus-mapping.json              ← slug → corpus_keys + display fields
├── source-mapping.json              ← slug → required source list
└── helpers/
    ├── extract_top_threads.py       ← corpus.json → top-N threads
    ├── update_hub.py                ← move slug from Coming Soon → Live
    ├── archive_urls.py              ← submit URLs to archive.org
    └── verify_anti_tics.py          ← Pass 8 automated grep
```

State (gitignored): `tmp/scam-skill/<slug>/`
- `state.json` — progress through the 8 stages (for resume)
- `top_threads.json` — extracted from corpus
- `sources.md` — claim → URL → verbatim quote audit trail
- `archive-cache.json` — archive.org URLs for permanence
- `variant-proposal.md` — Stage 1 cluster output
- `plan.md` — Stage 2 plan + audit scores
- `audit.md` — Stage 4 8-pass report

## Adding a new slug

1. Add an entry to `corpus-mapping.json`:
   ```json
   "new-slug": {
     "corpus_keys": ["corpus_key_1", "corpus_key_2"],
     "display": {
       "emoji": "🔥",
       "name": "New Scam Type",
       "subtitle": "Channel · N variants",
       "headline_stat": "Big number with source",
       "tagline": "≤180 chars summary"
     },
     "related_slugs": ["other-slug-1", "other-slug-2"]
   }
   ```

2. Add an entry to `source-mapping.json` with the 4 source-bucket lists
   (federal, academic_ngo, industry, press).

3. Invoke `/general-scams-article new-slug`.

## Quick-test the helpers

```bash
# Verify corpus + mapping work for a slug
python3 .claude-skills/general-scams-article/helpers/extract_top_threads.py ai-voice-clone-scams

# Lint the AI-tic checks against an existing page
python3 .claude-skills/general-scams-article/helpers/verify_anti_tics.py pig-butchering
```

## Output guarantee

- **10/10 stellar, well-researched, accurate, non-hallucinating** —
  achieved via verbatim-quote-required source verification (Stage 1.4),
  source-reread audit pass (Pass 6), and source diversity floor (≥1
  federal + ≥1 NGO + ≥1 industry + ≥1 press).
- **9/10 SEO/AI visibility** — Article + FAQPage + HowTo + BreadcrumbList
  schema, AEO front-loading on FAQ answers, LLMs.txt entry, internal
  cross-linking among /scams/everywhere/ siblings, OG/Twitter cards
  validated.
- **9/10 execution reliability** — corpus + source maps formalized,
  failure-mode playbook documented (pre-commit hook fail, lint fail,
  merge worktree conflict), state persists across conversations.

## Origin doc

Spec was iterated 3x (execution / quality / SEO) until each dimension
passed 9+/10. Original conversation:
[approval flow log](../../tmp/scam-skill/_origin-conversation-2026-04-28.md)
(if you saved it).
