# Workflow — 8 stages

Follow these stages in order. Each stage writes its output to
`tmp/scam-skill/<slug>/state.json` so the build can resume after any
interruption. Hard checkpoints (where you wait for user approval) are
marked **🛑**.

---

## Stage 1 · Research prep (~15 min)

### 1.1 Resolve corpus mapping
```python
import json
mapping = json.load(open(".claude-skills/general-scams-article/corpus-mapping.json"))
corpus_keys = mapping[slug]["corpus_keys"]
```
If `slug` is not in the mapping, halt and ask the user to add it.

### 1.2 Pull top threads
```bash
python3 .claude-skills/general-scams-article/helpers/extract_top_threads.py <slug>
```
Outputs `tmp/scam-skill/<slug>/top_threads.json` with the top 8 threads
sorted by upvote score, plus their top 5 comments each.

### 1.3 Cluster variants
For each thread:
1. Extract: entry-channel, pivot-mechanism, extraction-mechanism, target-demographic, financial-loss-range
2. Group threads by extraction-mechanism (the most stable axis)
3. Drop any cluster with <2 supporting threads
4. Order clusters by narrative arc: entry vectors → trap mechanism → relational damage → meta-scam (if applicable)

Output: `tmp/scam-skill/<slug>/variant-proposal.md` with each candidate
variant + supporting thread count + brief description.

### 1.4 Verify federal + NGO + industry + press sources
Read the required source list from `source-mapping.json`. The mapping
specifies a minimum of 1 source from each of 4 buckets (federal, academic/NGO,
industry, press).

For each source:
1. Use `WebSearch` for the latest figures
2. **MANDATORY:** Use `WebFetch` on each cited URL to get the verbatim quote
3. If `WebFetch` cannot reach the source or no verbatim quote can be extracted, **drop the claim** — do not paraphrase under deadline pressure
4. Write each verified claim to `tmp/scam-skill/<slug>/sources.md`:

```
| claim | source URL | access date | verbatim quote | section | status |
| --- | --- | --- | --- | --- | --- |
| FBI IC3 attributed $5.8B... | https://... | 2026-04-28 | "Investment scams accounted for $5.8 billion..." | numbers | ✓verified |
```

Status legend:
- `✓verified` — verbatim quote on file from primary source
- `⚠estimated` — NGO estimate, not government-reported (label as such on the page)
- `❌unverifiable` — DO NOT USE on the page

### 1.5 Archive every cited URL
```bash
python3 .claude-skills/general-scams-article/helpers/archive_urls.py <slug>
```
Submits each URL in `sources.md` to `https://web.archive.org/save/<URL>`.
Stores the archive URLs in `tmp/scam-skill/<slug>/archive-cache.json`.

### 🛑 Checkpoint 1 — present to user:
- Variant proposal (the cluster output)
- Source verification table (sources.md)
- Anything that came back ❌unverifiable

User confirms before Stage 2 begins.

---

## Stage 2 · Plan + audit (~15 min)

### 2.1 Draft v1 plan
Use `page-anatomy.yaml` as the section blueprint. Per slot, plan:
- Specific content angle (channel label, severity rating, etc.)
- Word-count target
- Sources cited (from sources.md)
- Schema entries it contributes to

### 2.2 Score against external checklists
Run each of the 4 plan-stage checklists:
- `audit-checklists/plan-thoroughness.md`
- `audit-checklists/plan-accuracy.md`
- `audit-checklists/plan-seo.md`
- `audit-checklists/plan-narrative.md`

Each checklist is a list of binary checks. Score = (passed / total) × 10.

If any score < 9, iterate the plan and re-score. Cap at 3 iterations; if
still under 9, present to user with the specific unmet items flagged.

### 🛑 Checkpoint 2 — present to user:
- Final plan with scoring table
- Any unmet items from the checklists
- Variant ordering rationale
- Word-count target

User approves the plan before any HTML is written. **Per
`memory/feedback_research_before_pages.md`, this is non-negotiable.**

---

## Stage 3 · Build (~30 min)

### 3.1 Generate HTML using `page-anatomy.yaml`
For each section in the anatomy YAML:
1. Read the slot definition (required fields, optional fields, max words)
2. Generate content matching the spec
3. Use existing CSS classes from `assets/scams.css` plus the page-specific
   classes already in the pig-butchering page (`.tldr-box`, `.hook-section`,
   `.assessment-box`, `.context-sidebar`, `.glossary-toggle`,
   `.transition-line`, `.assessment-skip`, `.stat-strip`,
   `.legal-disclaimer`, `.intl-list`, `.help-list`, `.phase-list`)

### 3.2 Generate variants using `variant-template.yaml`
For each variant cluster from Stage 1:
1. Header (variant number + title + severity badge)
2. Channel field (with appropriate emoji per `voice-rules.md`)
3. TLDR sentence (≤30 words)
4. Story paragraphs (3 × 150–300 words, third-person narrative voice)
5. Mechanics paragraph (100–200 words, second-person advisory voice)
6. 5 red flags (exactly)
7. 5 defenses (exactly)
8. **MANDATORY:** 1 verbatim Reddit pull-quote with date-stamped upvote count

### 3.3 Embed schema
Write 4 JSON-LD blocks to the page `<head>`:
- `Article`
- `FAQPage` (8–10 questions, each answer 60–80 words, front-loaded)
- `HowTo` (5 steps from the Quick Safety Rules)
- `BreadcrumbList`

### 3.4 Generate Open Graph image stub
If a real OG image exists at `https://img.tabiji.ai/scams-everywhere-<slug>-og.jpg`,
use it. Otherwise fall back to `https://img.tabiji.ai/scams-everywhere-default-og.jpg`
(generic) and add `<slug>` to the comic-illustration TODO list.

### 3.5 Apply voice rules
Strictly follow `voice-rules.md`:
- Second-person for advice/instructions
- Third-person for victim stories
- No banned phrases
- Em-dash density ≤ 1.5 per 100 words

---

## Stage 4 · 8x audit pass (~20 min)

Run each pass in order. Apply fixes from each pass before moving to the next.

Each checklist file (`audit-checklists/pass-N-*.md`) has a YAML preamble
with the binary checks and a markdown body explaining each check.

| Pass | Focus | Pass threshold |
|---|---|---|
| 1 | Clarity & narrative | All checks ✓ |
| 2 | Voice & tone | All checks ✓, em-dash density ≤ 1.5/100w |
| 3 | Design & template | All slot fields present, page-anatomy.yaml conformance |
| 4 | Editorial / authority | All sources cited inline, ✓verified or ⚠estimated label |
| 5 | Grammar & spelling | Pass spell-check, no homophone errors, AmE consistency |
| 6 | Source reread | Re-fetch every cited URL, confirm verbatim quote still present |
| 7 | Accessibility (WCAG AA) | Color contrast, alt text, keyboard nav, ARIA |
| 8 | AI-tic detection (automated) | `helpers/verify_anti_tics.py` returns 0 violations |

If any pass fails after 2 fix iterations, halt and present to user.

### 🛑 Checkpoint 3 — present to user:
- Finished page (preview link)
- 8-pass audit report with scores
- All edits applied
- Any remaining caveats

User reads the page and signs off before Stage 5.

---

## Stage 5 · Update hub + sitemap + cross-links + LLMs.txt (~5 min)

### 5.1 Update `/scams/everywhere/index.html`
```bash
python3 .claude-skills/general-scams-article/helpers/update_hub.py <slug>
```
Moves the slug from the Coming-Soon `<ul>` to the `.city-grid` as a
`<a class="city-card">`. The card contains:
- Emoji icon (from `corpus-mapping.json` → `display.emoji`)
- Page name
- "Channel · N variants" subtitle
- Headline stat (the page's biggest number)
- Tagline (3-variant summary, ≤180 chars)
- "Updated [Month] [Year]"

### 5.2 Regenerate sitemap
```bash
python3 scripts/generate_sitemap.py
```
The new page (and the hub mod) will appear automatically.

### 5.3 Update `llms.txt` and `llms-full.txt`
Add an 80-word page summary entry for the new page. Lock the format
to whatever is already in those files.

### 5.4 Cross-link from sibling general-scam pages
For each existing `/scams/everywhere/<sibling>/index.html`:
1. Find the "Related reading" section
2. If the new slug is topically related (per `corpus-mapping.json` →
   `related_slugs`), add a link
3. Use a single Edit per file

Per user spec: cross-links are limited to `/scams/everywhere/` siblings.
Do NOT update city scam pages.

---

## Stage 6 · Pre-launch validation (~10 min)

Run all of these locally before opening the PR. Hard fails halt the build;
warnings are surfaced to the user but don't block.

| Check | Hard fail or warn? |
|---|---|
| Schema validation (JSON-LD parses + matches Article/FAQPage/HowTo/BreadcrumbList types) | Hard fail |
| Link validation (every internal + external link returns 2xx) | Hard fail |
| Anti-AI-tics grep (`helpers/verify_anti_tics.py`) returns 0 violations | Hard fail |
| Reading-level (Flesch ease ≥ 50, sentence-length variance > 5) | Hard fail |
| Lighthouse: LCP < 2.5s, CLS < 0.1, FID < 100ms | **Warn only** (per user spec) |
| Render-test in `Claude_Preview` at 360px / 768px / 1440px | Warn only |
| OG image returns 2xx (or fall back to default) | Warn only |
| Hub edit + sitemap entry are present in staged diff | Hard fail |

---

## Stage 7 · Deploy + merge

### 7.1 Stage + commit
```bash
git add .claude-skills/general-scams-article/  # if updated
git add scams/everywhere/<slug>/
git add scams/everywhere/index.html  # hub update
git add sitemap.xml
git add llms.txt llms-full.txt
# All sibling /scams/everywhere/<sibling>/index.html updated for cross-links
git add scams/everywhere/*/index.html

git commit -m "scams/everywhere/<slug>: launch <human-readable-title>"
```

### 7.2 Push + PR
```bash
git push -u origin claude/scams-everywhere-<slug>
gh pr create --title "scams/everywhere/<slug>: launch <human-readable-title>" --body "$(cat <<'EOF'
[structured PR body — see workflow.md template below]
EOF
)"
```

### 7.3 Monitor CI
Use the `Monitor` tool with a poll loop on `gh pr checks <PR#>`.
Required checks: `Cloudflare Pages`, `check-partials`, (and `lint-scam-content`
if scam-content paths changed).

### 7.4 Known failure modes + fixes
| Failure | Fix |
|---|---|
| Pre-commit hook: stale partials | `bash scripts/sync-partials.sh`, restage, retry commit |
| `lint-scam-content` failure on `everywhere/` page | Should not occur (exclusion in `_scam_sweep_common.py`); if it does, debug |
| Merge worktree conflict on `gh pr merge --delete-branch` | Use `gh api -X DELETE repos/.../git/refs/heads/<branch>` for cleanup |
| `mergeStateStatus: DIRTY` | Rebase: `git fetch origin && git rebase origin/main`, force-push with `--force-with-lease` |

### 🛑 Checkpoint 4 — explicit user authorization to merge

```bash
gh pr merge <PR#> --squash
gh api -X DELETE repos/psyduckler/tabiji/git/refs/heads/claude/scams-everywhere-<slug>
```

---

## Stage 8 · Post-launch (no merge gate)

Per user spec: a page can be live without AI-citation evidence.

Schedule the following as background tasks (don't block):
- 48h post-launch: query Perplexity / ChatGPT search / Claude search /
  Google AI Overview for the primary keyword; record citations (or absence)
- 90-day refresh: re-verify all federal sources, check Reddit thread upvote
  counts, regenerate `archive-cache.json` if URLs have rotted

---

## Resume instructions

If the build was interrupted, read `tmp/scam-skill/<slug>/state.json`. The
file has shape:
```json
{
  "slug": "ai-voice-clone-scams",
  "stage_completed": 3,
  "next_stage": 4,
  "checkpoint_pending": false,
  "artifacts": {
    "top_threads": "tmp/scam-skill/<slug>/top_threads.json",
    "sources": "tmp/scam-skill/<slug>/sources.md",
    "variant_proposal": "tmp/scam-skill/<slug>/variant-proposal.md",
    "plan": "tmp/scam-skill/<slug>/plan.md",
    "audit_report": "tmp/scam-skill/<slug>/audit.md",
    "page_html": "scams/everywhere/<slug>/index.html"
  }
}
```

Resume from `next_stage`. If `checkpoint_pending: true`, ask the user to
re-confirm the most recent checkpoint before continuing.

## PR body template

```markdown
## Summary
- Adds /scams/everywhere/<slug>/ — flagship page on <scam category>
- N variants documented from <N> Reddit threads + <N> comments in tmp/scam_research/corpus.json
- Updates hub to move <slug> from Coming Soon → Live Guides
- Sitemap regenerated; llms.txt + llms-full.txt updated; <N> sibling general-scam pages cross-linked

## Variants documented
1. <variant 1 title>
2. <variant 2 title>
... etc.

## Research provenance
Sourced from <N> Reddit threads in tmp/scam_research/corpus.json
(categories: <corpus_keys>). Cross-verified against:
- <federal source 1>
- <federal source 2>
- <NGO/academic source>
- <industry source>
- <press source>

All citations have verbatim quote + access date in tmp/scam-skill/<slug>/sources.md
(gitignored audit trail).

## Schema
Article + FAQPage (N Q's) + HowTo (N steps) + BreadcrumbList. All validated.

## Audit / quality
8-pass audit complete (clarity, voice, design, authority, grammar,
source reread, accessibility, AI-tic detection). All passes ✓.

## Hub + sitemap
- /scams/everywhere/index.html: <slug> moved from Coming Soon → Live Guides
- sitemap.xml: regenerated, new URL indexed
- llms.txt + llms-full.txt: entry added

## Test plan
- [ ] Page loads at /scams/everywhere/<slug>/
- [ ] Hub shows <slug> as Live Guide
- [ ] Breadcrumbs resolve
- [ ] FAQ accordions toggle
- [ ] Schema validates in Google Rich Results Test
- [ ] Mobile layout intact down to 360px

🤖 Generated by .claude-skills/general-scams-article
```
