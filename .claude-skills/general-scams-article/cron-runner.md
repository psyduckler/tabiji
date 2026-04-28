# Cron-Runner Mode — autonomous execution of the general-scams-article skill

This is the operational doc for the **scheduled-tasks** cron that runs the
skill every 12 hours. The cron spawns a fresh Claude with no conversation
history; the prompt below is what it executes.

## Differences from interactive mode

| Stage | Interactive mode | Cron mode |
|---|---|---|
| Checkpoint 1 (Stage 1, research summary) | 🛑 wait for user | ✓ auto-approve, log to PR body |
| Checkpoint 2 (Stage 2, plan approval) | 🛑 wait for user | ✓ auto-approve IF all 4 plan-audit dimensions ≥ 9/10; if any < 9, halt and leave queue entry as `failed` for human review |
| Checkpoint 3 (Stage 4, audit report) | 🛑 wait for user | ✓ auto-merge IF all 8 audit passes ✓ AND CI green; otherwise leave PR open and mark queue entry `pr-open-review-needed` |
| Checkpoint 4 (pre-merge) | 🛑 wait for user | Combined with Checkpoint 3 |

## Failure modes (cron behavior)

| Failure | Cron behavior |
|---|---|
| Slug not in `corpus-mapping.json` | Skip, mark `failed`, move to next queued slug |
| Required corpus categories empty in `corpus.json` | Skip, mark `failed` with reason, move to next |
| Stage 1 source verification: cannot find ≥1 source per bucket | Halt, mark `failed-source-verification`, surface to user |
| Stage 2 plan score < 9 on any dimension after 2 iterations | Halt, mark `failed-plan-quality`, surface |
| Stage 3 build error (template mismatch) | Halt, mark `failed-build` with traceback |
| Stage 4 any audit pass hard fail after 2 fix iterations | PR opens but does NOT auto-merge; mark `pr-open-review-needed` |
| Stage 5 hub-update conflict | Halt, mark `failed-hub-update`, surface |
| Stage 6 schema/link/anti-tic validation hard fail | Halt before PR open, mark `failed-validation` |
| Stage 7 CI failure on PR | Mark `pr-open-ci-fail`, do not retry, surface |
| Stage 7 merge conflict | Auto-rebase once; if still conflicting, mark `pr-open-merge-conflict`, surface |
| Auto-merge succeeds | Mark `merged`, advance queue |

## State updates

After every queue entry's run, the cron edits `queue.json`:

```json
{"slug": "ai-voice-clone-scams", "priority": 1, "tier": "S", "status": "merged",
 "pr": 1198, "merged_at": "2026-04-29T09:00:00Z"}
```

Status values:
- `pending` — not yet started
- `in-progress` — current run is processing this slug
- `merged` — successfully shipped + merged to main
- `pr-open-review-needed` — PR opened but flagged for human review (audit issues)
- `pr-open-ci-fail` — PR opened, CI failed
- `pr-open-merge-conflict` — PR opened, can't merge cleanly
- `failed-source-verification` / `failed-plan-quality` / `failed-build` / `failed-hub-update` / `failed-validation` — halted before PR open

## The cron prompt (verbatim)

This is what the scheduled-tasks invocation runs. Self-contained — assumes
no prior conversation context.

```
You are running the general-scams-article skill in autonomous cron mode.

1. Read .claude-skills/general-scams-article/SKILL.md, workflow.md, and
   cron-runner.md to understand the workflow.

2. Read .claude-skills/general-scams-article/queue.json. Find the FIRST
   entry with status="pending". Mark it "in-progress" and commit the
   queue.json change to a new branch.

3. If no pending entries exist, exit cleanly with "queue empty" message.

4. Execute the skill's 8 stages on the chosen slug, in CRON MODE:
   - Auto-approve checkpoints 1, 2, 3 if quality gates pass
   - Halt and mark "failed-*" if any quality gate fails (per
     cron-runner.md failure-modes table)
   - Open the PR with the standard PR body template

5. If all 8 audit passes are clean AND all CI checks pass:
   - Auto-merge the PR (gh pr merge <PR#> --squash)
   - Delete the remote branch
   - Update queue.json: mark slug "merged" with PR# and timestamp
   - Move shipped slug from "queue" array to "completed" array
   - Commit the queue update to a new tiny PR and merge it
     (this is the only PR that auto-merges without going through the skill's audit)

6. If any audit pass fails OR CI fails:
   - Leave PR open
   - Update queue.json: mark slug "pr-open-review-needed" or appropriate failure status
   - Surface the failure in the run notification

7. Use only the tools/scripts already in .claude-skills/general-scams-article/.
   Do NOT improvise corpus categories, source-mapping entries, or page
   structures outside what the skill provides.

8. Strict no-hallucination rule: every stat must have a verbatim quote
   in tmp/scam-skill/<slug>/sources.md. If WebSearch + WebFetch cannot
   produce a verbatim quote, drop the claim. Do not paraphrase.

9. When done, send a notification with: slug processed, PR number, merge
   status, and any flags requiring human attention.
```

## Manual trigger (kick off a run outside the schedule)

```
mcp__scheduled-tasks__update_scheduled_task --taskId=general-scams-article-cron --... # (or use the runOnDemand UI)
```

Or run the cron prompt above as a one-time agent.
