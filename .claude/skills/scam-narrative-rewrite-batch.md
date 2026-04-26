---
name: scam-narrative-rewrite-batch
description: Process the next 5 pending cities from scripts/queues/scam-narrative-rewrite-queue.json, rewriting each scam page to the NYC 3-beat narrative spec end-to-end by hand via Edit tool. One PR per batch — STOP at gh pr create (a separate local merge cron handles bulk-merging). Used by remote routine. Trigger when user types /scam-narrative-rewrite-batch or when the routine fires it.
user_invocable: true
---

# Scam narrative rewrite batch

Rewrite up to **5 pending cities** to the NYC 3-beat narrative spec in a single batch. One PR per batch covering all cities in the run.

## Pre-flight (run once at start)

```bash
git fetch origin main && git status
```

If there are uncommitted local changes that aren't from a prior batch, stop and ask the user.

## Step 1: Read the pending queue

```bash
python3 -c "
import json
with open('scripts/queues/scam-narrative-rewrite-queue.json') as f:
    data = json.load(f)
pending = [i for i in data['queue'] if i.get('status') == 'pending']
print(f'pending: {len(pending)}')
print('next 7:')
for i in pending[:7]:
    print(f'  {i[\"slug\"]}  ({i.get(\"tier\",\"?\")}, {i.get(\"scam_count\",6)} scams)')
"
```

If `pending: 0`, **stop**. The campaign is complete. Tell the user to delete the cron job (`CronList` then `CronDelete`).

## Step 2: Branch from latest main

```bash
git fetch origin main
BATCH_TAG=$(date -u +%Y%m%d-%H%M)
git checkout -b "claude/scam-rewrite-batch-${BATCH_TAG}" origin/main
```

If a worktree conflict prevents `git checkout main`, just branch directly from `origin/main` as shown above.

## Step 3: Rewrite each city (up to 5)

Take the top 5 pending entries. **One city at a time, one scam at a time, by hand via the `Edit` tool only.** No Python find/replace scripts on body content (sed for hero/meta scrubs is fine; Python for sync/lint/audit is fine).

For each city slug:

1. **Read the scam HTML structure**:
   ```bash
   grep -nE 'scam-tldr|scam-story-body' scams/<slug>/index.html | head -30
   ```
   Note which scams have TLDRs vs bodies-only, how many bodies each has, and any sanitizer-leak fragments (Reddit-quote shards, `(, mid-2025)` voids, broken sentence joins).

2. **Rewrite each of the 6 scam-cards end-to-end** via individual `Edit` tool calls. Each scam-card needs:
   - **TLDR** (`<p class="scam-tldr">`): a **trap-summary sentence** containing actor + location + mechanic + cost + variant. Never a narrative-opener fragment ("Paris is famous for...").
   - **Body 1** (Setup beat): place + actors + lure context.
   - **Body 2** (Pivot beat): the trap mechanic — how setup turns into pressure/cost.
   - **Body 3** (Defense beat): a single bolded `<strong>` core defense as a natural sentence inside flowing prose, plus surrounding context. **Not** the bolt-on pattern `<strong>X</strong> (1) ... (2) ...`.

3. **Add missing TLDRs**: If a scam has only `<p class="scam-story-body">` paragraphs and no `<p class="scam-tldr">`, add a trap-summary TLDR as the first paragraph.

4. **Expand short structures**: If a scam has `TLDR + 1 body` (Sardinia/Yokohama-style), expand to `TLDR + 3 bodies` covering the full setup → pivot → defense beat structure.

5. **Lint after each city**:
   ```bash
   python3 scripts/lint_scam_content.py --html-city <slug>
   ```
   Must return `0 REJECT 0 WARN`. If anything fails, fix before moving on.

6. **Sync API JSON**:
   ```bash
   python3 scripts/sync_api_from_html.py <slug>
   ```
   This rewrites `api/v1/scams/<slug>.json` from the corrected HTML and marks the queue entry `complete`. The script may print a `WARNING: N scams in API not found in HTML` if you renamed any scam titles — that's a cosmetic mismatch and acceptable for a single batch but flag it in the PR body.

7. Move to next slug.

## Step 4: Sync partials (once at end of batch)

If main has moved forward since you branched, the pre-commit hook will reject the commit with "stale managed blocks." Run:

```bash
bash scripts/sync-partials.sh
git add scams/
```

The sync only touches the 5 HTML files you edited (it's idempotent on partials already in sync).

## Step 5: Commit, push, PR

```bash
git add scams/ api/ scripts/queues/ && git status --short
```

**Stage only the cities you touched + their APIs + the queue file.** Never `git add -A` — the partials sync can capture unrelated repo-wide changes.

```bash
SLUGS_LIST="<slug1>, <slug2>, <slug3>, <slug4>, <slug5>"
git commit -m "$(cat <<EOF
scams: rewrite ${SLUGS_LIST} by hand to NYC 3-beat spec

End-to-end hand rewrites of 30 scam-cards across 5 cities (TLDR + 3 bodies × 6 scams × 5 cities = 120 paragraph rewrites). Every TLDR is a trap-summary; every body 3 has the bolded core defense as a natural sentence inside flowing prose. APIs resynced.

Lint: 0 REJECT 0 WARN on all 5 cities.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"

git push -u origin "claude/scam-rewrite-batch-${BATCH_TAG}" 2>&1 | tail -3

gh pr create --title "scams: rewrite ${SLUGS_LIST} by hand" --body "$(cat <<EOF
## Summary

- Full end-to-end hand rewrites of 30 scam-cards across 5 cities
- 120 paragraph-level rewrites: TLDR + 3 bodies × 6 scams × 5 cities
- Every TLDR is a trap-summary (actor + location + mechanic + cost + variant)
- Every body 3 has the bolded core defense as a natural sentence inside flowing prose

## Test plan

- [x] Lint all 5 cities: 0 REJECT 0 WARN
- [x] API JSON parity: 30 scam entries resynced
- [x] HTML partials: clean
- [ ] Live verification after deploy

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)" 2>&1 | tail -3
```

## Step 6: STOP after gh pr create

**Do not wait for checks. Do not merge.** A separate local merge cron (fires hourly at :43) bulk-merges any open `claude/scam-rewrite-batch-*` PRs that have passing checks. Your job ends at PR creation.

```bash
echo "PR opened — exiting per skill protocol. Local merge cron at :43 handles squash-merge."
exit 0
```

**Architecture note**: this skill used to wait-for-checks-and-merge, but that step has been moved out. A separate local-session cron at `:43 * * * *` calls a bulk-merge prompt that picks up every open `claude/scam-rewrite-batch-*` PR with passing checks and squashes it. This decoupling keeps the long-running rewrite work isolated to the remote routine and concentrates the merge gate where the user can audit quality.

## Hard rules (from the user — see `memory/scam_rewrite_python_antipattern.md`)

- **No Python scripts for content edits.** Every TLDR rewrite, body rewrite, and `<strong>` defense placement happens via individual `Edit` tool calls. Python find/replace produced bolt-on artefacts (`<strong>X</strong> (1) ... (2) ...`) and sanitizer leaks across P116–P123 — that whole batch had to be rebuilt by hand.
- **One scam at a time, end-to-end.** Read the scam-card, write a fresh TLDR + 3 fresh bodies, place the bolded defense as natural prose. Treat every page as if it were never touched.
- **The bolded `<strong>` defense is a natural sentence inside Beat 3 prose.** Never prepended to an original numbered list.
- **Pages must pass `lint_scam_content.py` before commit.**
- **Stage only the files you touched.** Never `git add -A` — accidentally captures partial-sync rollbacks of accessibility improvements on unrelated pages.

## Common gotchas

- **Partial-sync rollback**: `bash scripts/sync-partials.sh` reads `_includes/` and rewrites every HTML file's managed-block region. If main has accessibility improvements newer than your branch, the sync **rolls them back** on every HTML in the repo. Always stage only `scams/<your-slugs>/index.html` plus `api/v1/scams/<your-slugs>.json` plus `scripts/queues/scam-narrative-rewrite-queue.json` — and let the sync touch only those 5 cities' HTML.
- **API title mismatch**: If your rewrite changed a scam-card `<div class="scam-title">` text, `sync_api_from_html.py` will print `WARNING: N scams in API not found in HTML`. The API still updates the matching scams; the unmatched API entries are stale but harmless. Either accept the cosmetic mismatch or update the API JSON's scam name manually.
- **`gh pr merge` worktree error**: non-blocking — verify with `gh pr view <#> --json state,mergedAt`.
- **Sardinia/Yokohama 1-body structure**: those cities had `TLDR + 1 body` paragraphs. Expand to `TLDR + 3 bodies` for full NYC 3-beat coverage.
- **Cities with no TLDR**: many later-batch cities had only `<p class="scam-story-body">` paragraphs and no TLDR at all. Add the trap-summary TLDR as the first paragraph in each scam-card.

## Reference work (gold standard for the spec)

- `scams/new-york-city/index.html` — pattern-setting reference (PR #491)
- `scams/ouro-preto/index.html` — first hand-rebuild after the Python anti-pattern (PR #804)
- `scams/sao-paulo/index.html` — typical Brazilian 6-scam city, full NYC 3-beat
- `scams/sardinia/index.html` — TLDR+1-body expanded to TLDR+3-bodies

## End of batch

After 5 cities (or fewer if queue ran out):

1. Print summary: how many cities completed this batch, how many remain pending, the new PR number/URL.
2. If queue is empty (`pending: 0`), say so explicitly so the user can disable the remote routine and the local merge cron.
3. End the turn. **Do not** schedule another batch (the remote routine handles that) and **do not** merge the PR (the local merge cron handles that).
