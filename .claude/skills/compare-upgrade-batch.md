---
name: compare-upgrade-batch
description: Process the next 20 sub-100 compare pages, upgrading each to 100/100. Used by hourly cron. Trigger when user types /compare-upgrade-batch or when cron fires it.
user_invocable: true
---

# Compare upgrade batch

Process up to **20 compare pages** from sub-100 to 100/100 in a single batch, one at a time.

## Pre-flight (run once at start)

```bash
git fetch origin main && git status
```

If there are uncommitted local changes that aren't from a prior batch, stop and ask the user.

## Step 1: Regenerate pending queue

The queue file is rewritten each batch from live scores so we never act on stale data:

```bash
python3 -c "
import sys, json, pathlib
sys.path.insert(0, 'scripts')
from score_compare import score_all
results = score_all()
sub = [{'slug':r['slug'],'score':r['score'],'tier':r['tier'],'faq_n':r['faq_n']} for r in results if r['score']<100]
sub.sort(key=lambda x:(x['score'], -x['faq_n']))
pathlib.Path('scripts/queues/compare-pending-queue.json').write_text(json.dumps(sub, indent=2))
print(f'pending: {len(sub)} pages')
print('next 22:')
for r in sub[:22]: print(f'  {r[\"score\"]:>3}  faq={r[\"faq_n\"]:>2}  {r[\"slug\"]}')
"
```

If `pending: 0`, **stop**. The campaign is complete. Tell the user to delete the cron job (`CronList` then `CronDelete`).

## Step 2: Process each page (up to 20)

Take the top entries from `compare-pending-queue.json` and process them in order. **One page at a time.** Do not write helper scripts. Do not batch edits. Each page goes through individual `Edit` tool calls.

For each slug, follow the full workflow in `scripts/queues/compare-batch-50-resume.md`:

1. `git fetch origin main && git checkout -b compare/upgrade-<slug> origin/main`
2. Audit: `python3 scripts/score_compare.py <slug>` — note title length, FAQ count, photo-grid first img, body anchor IDs.
3. **Apply each transformation as a separate Edit call**:
   - **Title trim**: drop ` (2026 Comparison)` and ` | tabiji.ai` suffixes if total chars >65.
   - **section-winner replacement**: `replace_all` `<div class="section-winner"><h3>Winner takeaway</h3><ul>` → `<div class="tabiji-verdict"><strong>tabiji verdict:</strong> <ul>` (harmless if 0 occurrences).
   - **LCP fix** on first photo-grid `<img>`: remove `loading="lazy"`, add `fetchpriority="high"`.
   - **Insert custom Quick Answers + Personalize widget + Visual Scorecard** between the photo-grid closing `</div>` and the verdict-box `<div class="verdict-box">`. **Custom content per city pair** — never templated. Use 6 QA cards anchored to **existing** body IDs only (grep `id="..."` first). Personalize widget: 3 pill groups × 36 keyed recommendations. Scorecard: 9 dimensions.
   - **`&amp;amp;` fix** if present: `replace_all '&amp;amp;' → '&amp;'`.
   - **FAQ expansion** if `faq_n < 16`: append visible items to reach 16+, mirror in FAQPage JSON-LD. Verify after each expansion (count is `faq-item` count + `itemtype="Question"` count).
4. **Verify**: `python3 scripts/score_compare.py <slug> --gate 100` must exit 0.
5. **Commit + PR + merge**:
   ```bash
   git add compare/<slug>/index.html && \
   git commit -m "compare: <slug> XX → 100" && \
   git push -u origin compare/upgrade-<slug> 2>&1 | tail -2 && \
   gh pr create --title "compare: <slug> XX → 100" --body "QA + Personalize + Scorecard + LCP fix + tabiji-verdict + title trim. Score 100/100." 2>&1 | tail -2 && \
   PR=$(gh pr list --head compare/upgrade-<slug> --json number --jq '.[0].number') && \
   gh pr merge $PR --squash --delete-branch 2>&1 | tail -2 && \
   gh pr view $PR --json state,mergedAt
   ```
6. Move to next slug.

## Hard rules from the user

- **No shortcuts.** Don't write helper scripts that auto-fix multiple pages. Every transformation goes through individual `Edit` tool calls.
- **One page at a time.** Branch → edit → score gate → commit → PR → squash-merge → next page.
- **Custom content per city pair** — Quick Answers, Personalize, and Scorecard text must be specific to the destinations. Never templated.
- Pages must pass `python3 scripts/score_compare.py <slug> --gate 100` before commit.

## Common gotchas (refer to `scripts/queues/compare-batch-50-resume.md` for full list)

- **MED tier template**: photo-grid is followed by blank lines, NOT directly by `<div class="verdict-box">`. Don't inject a duplicate verdict-box opening. Score gate audit shows tabiji-verdict already 5/5 if MED tier.
- **FAQ off-by-one**: target is 16 — for FAQ=7 add 9 items; for FAQ=8 add 8 items; for pages with `itemtype="https://schema.org/Question"` the count doubles (visible + itemtype).
- **Quick Answers anchor IDs** must exist in the body. Run `grep -oE 'id="[a-z-]+"' <file> | sort -u` first.
- **`gh pr merge` worktree errors** are non-blocking — verify with `gh pr view <#> --json state,mergedAt`. PRs that say "Pull request was already merged" mean it succeeded.
- **`oahu-vs-maui`** is a stub. If it appears in the queue, skip it.

## End of batch

After 20 pages (or fewer if queue ran out):

1. Print summary: how many pages completed this batch, how many remain.
2. If queue is empty, tell the user to run `CronList` and `CronDelete <id>` to stop the job.
3. End the turn. Do **not** schedule another batch — the cron handles that.

## Reference pages (passing 100/100)

- `compare/tokyo-vs-kyoto/` — gold standard
- `compare/croatia-vs-montenegro/` — full template
- `compare/quebec-city-vs-montreal/` — recent example
- `scripts/queues/compare-batch-50-resume.md` — canonical workflow doc
