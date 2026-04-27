#!/bin/bash
# scam-rebuild-cron.sh — Rebuild scam city pages from the no-comic queue.
#
# Drives the scam-page-builder skill via `claude -p` headless mode, one city
# at a time. Each city is a fresh rewrite (Step 1 outcome 3) — the skill's
# "already book-ready" abort gate is overridden by the prompt. Comics emit
# 404 placeholders; comic art is a separate downstream pass.
#
# Designed to run on a 30-min schedule. Default batch size is 1
# (1 page per 30 min = 2 pages/hour, ~4.7 days to drain the 224-page queue). Override with:
#   ./scam-rebuild-cron.sh <N>
# This conservative default keeps token spend bounded while quality is
# being monitored. Bump the batch size or shorten the cron cadence later
# once output is consistently good.
#
# Per-city flow:
#   1. claude -p drives Steps 2–12 of scam-page-builder.md
#   2. Skill commits its own changes locally on main (no push)
#   3. Parent script collects results, updates queue, pushes once at end
set -uo pipefail

# Source repo (the user's main checkout — used only as a worktree parent).
SOURCE_REPO="/Users/psy/repos/tabiji"
# Dedicated worktree for this cron — keeps us OUT of any branch held by
# active Claude Code sessions, Pinterest automation, or other tooling.
# Always detached, always reset to origin/main at the start of each run.
WORK="${WORK:-/Users/psy/.cache/scam-rebuild-cron-worktree}"
QUEUE="$WORK/scripts/queues/scam-no-comic-rebuild-queue.json"
LOGDIR="$SOURCE_REPO/logs/scam-rebuild"
BATCH_SIZE="${1:-1}"
PER_CITY_TIMEOUT="${PER_CITY_TIMEOUT:-2400}"  # 40 min hard cap per city
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
LOGFILE="$LOGDIR/run-${TIMESTAMP}.log"

mkdir -p "$LOGDIR"

exec > >(tee -a "$LOGFILE") 2>&1

echo "═══════════════════════════════════════════════════════════════"
echo "  Scam Rebuild Cron — $(date '+%Y-%m-%d %H:%M:%S')"
echo "  Batch size: $BATCH_SIZE   Per-city timeout: ${PER_CITY_TIMEOUT}s"
echo "  Worktree: $WORK"
echo "  Log: $LOGFILE"
echo "═══════════════════════════════════════════════════════════════"

# ─── Auth: load credentials in this priority order ─────────────────────────
# 1. Already in environment (interactive testing, launchd UserAgent context)
# 2. ~/.config/tabiji/cron-secrets.env (cron context — written manually
#    once, mode 600. Required because cron jobs cannot reach the macOS
#    keychain — `security find-generic-password` returns empty even though
#    the call succeeds, since the keychain is locked at session start.)
# 3. macOS keychain via `security find-generic-password` (interactive shell
#    fallback — `gh auth token` and the `anthropic-api-key` keychain item
#    work here because the login keychain is unlocked.)
SECRETS_FILE="${SECRETS_FILE:-$HOME/.config/tabiji/cron-secrets.env}"
if [ -f "$SECRETS_FILE" ]; then
    set -a; . "$SECRETS_FILE"; set +a
    SECRETS_SOURCE="file"
fi
# CLAUDE_CODE_OAUTH_TOKEN is the preferred auth — opus-4-7 only accepts
# the headless CLI's default thinking config under OAuth (Max sub) auth.
# Under raw ANTHROPIC_API_KEY, the API rejects with "thinking.type.enabled
# is not supported for this model" no matter what --effort level you pass.
# Fall back to ANTHROPIC_API_KEY only if OAuth is unavailable.
if [ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ] && [ -z "${ANTHROPIC_API_KEY:-}" ]; then
    ANTHROPIC_API_KEY=$(security find-generic-password -a "$USER" -s "anthropic-api-key" -w 2>/dev/null || true)
    [ -n "$ANTHROPIC_API_KEY" ] && SECRETS_SOURCE="${SECRETS_SOURCE:-keychain}"
fi
if [ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ] && [ -z "${ANTHROPIC_API_KEY:-}" ]; then
    echo "❌ no claude auth available. Set CLAUDE_CODE_OAUTH_TOKEN (preferred — copy from interactive shell where claude is logged in) or ANTHROPIC_API_KEY in $SECRETS_FILE (mode 600). Aborting."
    exit 1
fi
[ -n "${CLAUDE_CODE_OAUTH_TOKEN:-}" ] && export CLAUDE_CODE_OAUTH_TOKEN
[ -n "${ANTHROPIC_API_KEY:-}" ] && export ANTHROPIC_API_KEY

if [ -z "${GH_TOKEN:-}" ]; then
    GH_TOKEN=$(gh auth token 2>/dev/null || true)
fi
if [ -z "$GH_TOKEN" ]; then
    echo "❌ no GH_TOKEN available. Set it in env, in $SECRETS_FILE (mode 600), or run 'gh auth login' from an interactive shell. Aborting."
    exit 1
fi
export GH_TOKEN
# git push will use this URL form to auth — no credential-helper / keychain dependency.
PUSH_URL="https://x-access-token:${GH_TOKEN}@github.com/psyduckler/tabiji.git"
AUTH_KIND="OAuth (Max)"
[ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ] && AUTH_KIND="API key (NOTE: opus-4-7 may fail — prefer OAuth)"
echo "  ✓ claude auth: $AUTH_KIND, GH_TOKEN (len ${#GH_TOKEN}) loaded from ${SECRETS_SOURCE:-env}"

# Pick a timeout binary (macOS ships without `timeout` by default)
TIMEOUT=""
if command -v gtimeout >/dev/null 2>&1; then
    TIMEOUT="gtimeout"
elif command -v timeout >/dev/null 2>&1; then
    TIMEOUT="timeout"
fi
[ -z "$TIMEOUT" ] && echo "(no timeout binary available; running without per-city cap)"

# ─── Step 0a: Self-update — pull SOURCE_REPO to current origin/main so the
# script file the next cron picks up reflects the latest merged version.
# Fast-forward only — never destroys local work. Silently no-ops if SOURCE_REPO
# has uncommitted changes or has diverged.
echo ""
echo "▶ Step 0a: Self-update SOURCE_REPO"
git -C "$SOURCE_REPO" fetch origin main 2>/dev/null || true
git -C "$SOURCE_REPO" pull --ff-only origin main 2>&1 | tail -2 || echo "  (skipped — local has divergent state)"

# ─── Step 0b: Provision dedicated worktree at origin/main ──────────────────
echo ""
echo "▶ Step 0b: Provision dedicated worktree at origin/main"
if [ ! -d "$WORK/.git" ] && [ ! -e "$WORK/.git" ]; then
    # First run: create the worktree as a sibling, detached at origin/main.
    git -C "$SOURCE_REPO" fetch origin main
    git -C "$SOURCE_REPO" worktree add --detach "$WORK" origin/main
    echo "  ✓ created worktree at $WORK"
fi
cd "$WORK"
# Always force-sync to origin/main — discards any leftover local commits
# from a previous failed cron run (which would otherwise rebase-block).
git fetch origin main
git reset --hard origin/main
echo "  branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'detached') (HEAD = $(git rev-parse --short HEAD))"

# ─── Step 1: Pick top N pending entries by priority ────────────────────────
echo ""
echo "▶ Step 1: Selecting top $BATCH_SIZE pending entries"

PICKS=$(python3 -c "
import json
q = json.load(open('$QUEUE'))
pending = [it for it in q['queue'] if it['status'] == 'pending']
picks = sorted(pending, key=lambda x: x['priority'])[:$BATCH_SIZE]
for it in picks:
    print('|'.join([it['slug'], it['city'], it['country'], it['country_code'], it['flag']]))
")

if [ -z "$PICKS" ]; then
    echo "  Queue empty — nothing to rebuild."
    exit 0
fi

declare -a SLUGS CITIES COUNTRIES CODES FLAGS
i=0
while IFS='|' read -r slug city country cc flag; do
    SLUGS[$i]="$slug"
    CITIES[$i]="$city"
    COUNTRIES[$i]="$country"
    CODES[$i]="$cc"
    FLAGS[$i]="$flag"
    echo "  [$((i+1))] $slug — $city, $country ($cc) $flag"
    i=$((i+1))
done <<< "$PICKS"
TOTAL=${#SLUGS[@]}

# ─── Step 2: Mark in-progress, commit + push immediately ───────────────────
# Push the in-progress markers so concurrent cron runs don't grab the same cities.
echo ""
echo "▶ Step 2: Marking $TOTAL entries in-progress"

SLUG_CSV=$(IFS=,; echo "${SLUGS[*]}")
SLUG_CSV="$SLUG_CSV" python3 -c "
import json, os
q = json.load(open('$QUEUE'))
slugs = set(os.environ['SLUG_CSV'].split(','))
now = '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
for it in q['queue']:
    if it['slug'] in slugs:
        it['status'] = 'in-progress'
        it['created_at'] = now
json.dump(q, open('$QUEUE', 'w'), indent=2, ensure_ascii=False)
open('$QUEUE','a').write('\n')
"

git add "$QUEUE"
git commit -m "scam-rebuild: mark $TOTAL in-progress (${SLUGS[*]})" 2>/dev/null || true
git push "$PUSH_URL" HEAD:main 2>/dev/null || echo "  ⚠️  push of in-progress markers failed (will retry at end)"

# ─── Step 3: Drive each rebuild via claude -p ──────────────────────────────
declare -a SUCCESS_SLUGS
declare -a SUCCESS_PRS  # entries like "slug=https://github.com/.../pull/N"
declare -a FAILED_SLUGS
declare -a FAIL_REASONS

for idx in $(seq 0 $((TOTAL-1))); do
    slug="${SLUGS[$idx]}"
    city="${CITIES[$idx]}"
    country="${COUNTRIES[$idx]}"
    cc="${CODES[$idx]}"
    flag="${FLAGS[$idx]}"
    city_log="$LOGDIR/${slug}-${TIMESTAMP}.log"

    echo ""
    echo "──────────────────────────────────────────────────────────────"
    echo "▶ [$((idx+1))/$TOTAL] Rebuilding $slug — $city, $country $flag"
    echo "  Per-city log: $city_log"
    echo "  Started: $(date '+%H:%M:%S')"

    # Hard-reset to current origin/main between cities. Aggressive cleanup is
    # required because:
    # - the previous city's claude session may have left untracked files in $WORK
    # - the post-claude amend step may have left staged/unstaged changes if a
    #   force-push race aborted mid-flight
    # - both situations cause the next iteration's `git pull --rebase` to fail
    #   with "cannot rebase: You have unstaged changes", which kills the rest
    #   of the batch (the failure mode we hit with parallel batches today).
    # `reset --hard` + `clean -fd` wipes everything; we're on a dedicated
    # worktree so there's no user work to preserve.
    git fetch origin main 2>&1 | tail -1
    git reset --hard origin/main 2>&1 | tail -1
    git clean -fd 2>&1 | tail -1

    PROMPT="You are executing the scam-page-builder skill (.claude/skills/scam-page-builder.md) for a FORCED REBUILD of an existing scam city page.

City: ${city}
Country: ${country}
Country code: ${cc}
Flag: ${flag}
Slug: ${slug}
Page path: scams/${slug}/index.html
API path: api/v1/scams/${slug}.json

Forced-rebuild rules (override the skill's Step 1 gates):
- Treat this as Step 1 outcome 3 (pre-book-ready rewrite) regardless of how the existing page looks. Do NOT abort even if the page would otherwise pass the 'already book-ready' gate (≥3 scams, valid Reddit IDs, T1/T2 citations).
- The user has explicitly authorized the rewrite. Skip the 'OK to rewrite from scratch?' confirmation.
- Replace any existing SAFETY_TIPS[\"${city}\"] and FAQS[\"${city}\"] entries with freshly-researched values (don't merge — old entries were written to a lower bar).
- Keep the existing CITY_SLUGS[\"${city}\"] entry (don't duplicate).

Comics — explicitly deferred:
- The page will emit <img class=\"scam-comic\" src=\"https://img.tabiji.ai/scams/${slug}/scam-N.jpg?v=1\" ...> placeholders that 404 until a separate comic-pipeline pass uploads art. This is acceptable and expected.

Execution (PR flow — do NOT commit to main):
- Run Steps 2–12 of the skill (Step 1 already resolved by the rules above).
- Lint must pass (0 REJECT, 0 WARN). If lint fails, fix and re-lint.
- Create a branch named 'scam-rebuild/${slug}' off the current HEAD.
- After parser-verify, stage scams/${slug}/index.html, scams/research/${cc}_batchN.json (whichever batch you chose), and any necessary edits to scams/generate_pages.py (CITY_SLUGS, SAFETY_TIPS, FAQS, EMERGENCY_INFO). DON'T worry about api/v1/scams/${slug}.json — the parent cron script regenerates that and amends the commit after you finish.
- Commit on the branch with message: 'scams: rebuild ${city} (${country}) — N Reddit-cited scams (no-comic queue)' and Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
- Push the branch and open a single-city PR via 'gh pr create' titled 'scams: rebuild ${city} (${country}) — book-ready, comics deferred'. PR body should include: list of N scams (name + danger level), lint status (0 REJECT, 0 WARN), sources summary (Reddit T1/T2 counts), and 'Comics: deferred — placeholder <img> tags emit 404s until comic-pipeline pass'.
- Do NOT merge the PR — a separate process handles bulk merges.

Output one final message before exiting (no other formatting): a single JSON object on its own line. The status field MUST be the literal string \"complete\" on success or \"failed\" on failure — do NOT paraphrase as \"ok\", \"success\", \"done\", etc., or the cron will mis-mark this run. Schema: {\"status\": \"complete\"|\"failed\", \"slug\": \"${slug}\", \"pr_url\": \"<url>\"|null, \"branch\": \"scam-rebuild/${slug}\", \"error\": \"<short reason if failed>\"|null, \"scam_count\": <int>|null, \"notes\": \"<one-line summary of what changed>\"}.

Proceed autonomously. Do not ask the user any questions."

    # Run claude headless with structured JSON output.
    # IMPORTANT: --add-dir is variadic — it consumes args until the next flag.
    # The prompt MUST come after another flag (here: -p) or after `--`,
    # otherwise claude swallows the prompt as a directory and hangs waiting on stdin.
    set +e
    if [ -n "$TIMEOUT" ]; then
        $TIMEOUT "$PER_CITY_TIMEOUT" claude \
            --model claude-opus-4-7 \
            --effort medium \
            --output-format json \
            --dangerously-skip-permissions \
            --add-dir "$WORK" \
            -p \
            -- "$PROMPT" < /dev/null > "$city_log" 2>&1
        RC=$?
    else
        claude \
            --model claude-opus-4-7 \
            --effort medium \
            --output-format json \
            --dangerously-skip-permissions \
            --add-dir "$WORK" \
            -p \
            -- "$PROMPT" < /dev/null > "$city_log" 2>&1
        RC=$?
    fi
    set -e

    echo "  Finished: $(date '+%H:%M:%S')   Exit: $RC"

    # Parse the final result line from the claude output
    # The --output-format json wraps the response; the model's last line is in result.result
    RESULT_JSON=$(python3 -c "
import json, sys
try:
    data = json.load(open('$city_log'))
    text = data.get('result', '') if isinstance(data, dict) else ''
except Exception:
    text = open('$city_log').read()

# Find last JSON object with our keys
import re
matches = re.findall(r'\{[^{}]*\"slug\"[^{}]*\}', text)
if matches:
    print(matches[-1])
else:
    print('')
" 2>/dev/null)

    if [ -n "$RESULT_JSON" ]; then
        STATUS=$(python3 -c "import json; print(json.loads('''$RESULT_JSON''').get('status',''))" 2>/dev/null || echo "")
        PR_URL=$(python3 -c "import json; print(json.loads('''$RESULT_JSON''').get('pr_url') or '')" 2>/dev/null || echo "")
        BRANCH=$(python3 -c "import json; print(json.loads('''$RESULT_JSON''').get('branch') or '')" 2>/dev/null || echo "")
    else
        STATUS=""; PR_URL=""; BRANCH=""
    fi
    [ -z "$BRANCH" ] && BRANCH="scam-rebuild/${slug}"

    # Accept any positive status the model emits — observed variants in the
    # 5-city kickoff: "complete", "ok", "success". The prompt asks for
    # "complete" but the model paraphrases ~40% of the time, and a successful
    # rebuild shouldn't be mis-marked as failed just because of word choice.
    case "$STATUS" in
        complete|ok|success|succeeded|done) IS_OK=1 ;;
        *) IS_OK=0 ;;
    esac

    if [ "$RC" -eq 0 ] && [ "$IS_OK" -eq 1 ]; then
        echo "  ✅ $slug — $STATUS (PR ${PR_URL:-?})"
        SUCCESS_PRS+=("${slug}=${PR_URL}")

        # Belt-and-suspenders: claude was told to skip api/v1/scams/<slug>.json
        # since the cron regenerates it from the research JSON. Check out the
        # feature branch claude pushed, run backfill_scams.py, amend the tip,
        # force-push so the PR's diff includes both HTML and the API JSON.
        if git fetch origin "$BRANCH" 2>/dev/null && git checkout "$BRANCH" 2>/dev/null; then
            if python3 "$WORK/scripts/backfill_scams.py" --slug "$slug" > "$LOGDIR/${slug}-${TIMESTAMP}-apijson.log" 2>&1; then
                git add "$WORK/api/v1/scams/${slug}.json" "$WORK/api/v1/scams.json"
                if ! git diff --cached --quiet; then
                    if git commit --amend --no-edit --no-verify >/dev/null 2>&1 \
                       && git push --force-with-lease "$PUSH_URL" HEAD:"$BRANCH" 2>&1 | tail -2; then
                        echo "     ↳ amended api/v1/scams/${slug}.json onto $BRANCH and force-pushed"
                    else
                        echo "     ⚠️  amend or force-push failed — PR has HTML only"
                    fi
                else
                    echo "     ↳ api/v1/scams/${slug}.json was already current — no amend needed"
                fi
            else
                echo "     ⚠️  backfill_scams.py --slug ${slug} failed (see ${slug}-${TIMESTAMP}-apijson.log) — PR has HTML only"
            fi
            # Force-clean back to origin/main — handles aborted amends / failed
            # force-pushes that left staged changes hanging on the feature branch.
            # Plain `git checkout --detach origin/main` silently fails on dirty
            # state; reset --hard always succeeds.
            git fetch origin main 2>&1 | tail -1
            git reset --hard origin/main 2>&1 | tail -1
            git clean -fd 2>&1 | tail -1
        else
            echo "     ⚠️  could not fetch/checkout $BRANCH — claude may not have pushed it. PR may have HTML only."
        fi

        SUCCESS_SLUGS+=("$slug")
    else
        REASON="$STATUS"
        [ -z "$REASON" ] && REASON="exit-$RC (no JSON status emitted)"
        echo "  ❌ $slug — $REASON"
        FAILED_SLUGS+=("$slug")
        FAIL_REASONS+=("$REASON")
    fi
done

# ─── Step 4: Update queue (PR opened → in-progress with pr_number) ──────────
# In PR-flow, success means a PR was opened, NOT that the page is on main.
# Queue entry stays in-progress until a separate merge process flips it to
# complete. Only the failed cities get a terminal "failed" status.
echo ""
echo "▶ Step 4: Updating queue (PRs opened → in-progress, failures → failed)"

SUCCESS_PRS_CSV=$(IFS=,; echo "${SUCCESS_PRS[*]:-}")
FAILED_CSV=$(IFS=,; echo "${FAILED_SLUGS[*]:-}")

SUCCESS_PRS_CSV="$SUCCESS_PRS_CSV" FAILED_CSV="$FAILED_CSV" python3 -c "
import json, os, re
from datetime import datetime, timezone
q = json.load(open('$QUEUE'))
prs = {}
for entry in os.environ['SUCCESS_PRS_CSV'].split(','):
    if not entry or '=' not in entry: continue
    slug, url = entry.split('=', 1)
    m = re.search(r'/pull/(\d+)', url or '')
    prs[slug] = {'pr_number': int(m.group(1)) if m else None, 'pr_url': url or None}
failed = set(s for s in os.environ['FAILED_CSV'].split(',') if s)
now = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
for it in q['queue']:
    if it['slug'] in prs:
        # Stay in-progress; record PR for the bulk-merge step. Don't mark
        # completed_at yet — that happens when the PR merges.
        it['status'] = 'in-progress'
        it['pr_number'] = prs[it['slug']]['pr_number']
        if not it.get('created_at'):
            it['created_at'] = now
    elif it['slug'] in failed:
        it['status'] = 'failed'
        it['completed_at'] = now
totals = {'pending': 0, 'in-progress': 0, 'complete': 0, 'failed': 0, 'skipped': 0}
for it in q['queue']:
    totals[it['status']] = totals.get(it['status'], 0) + 1
q['meta']['progress'] = totals
json.dump(q, open('$QUEUE', 'w'), indent=2, ensure_ascii=False)
open('$QUEUE','a').write('\n')
print(f'  prs={len(prs)} failed={len(failed)} totals={totals}')
"

# ─── Step 5: Commit + push the queue update only ───────────────────────────
# In PR-flow there are no rebuild commits to push — those are on feature
# branches behind PRs. Only the queue.json change goes to main.
echo ""
echo "▶ Step 5: Committing queue update and pushing to main"

git add "$QUEUE"
if ! git diff --cached --quiet; then
    SUMMARY="${#SUCCESS_PRS[@]} PRs opened"
    [ ${#FAILED_SLUGS[@]} -gt 0 ] && SUMMARY="$SUMMARY, ${#FAILED_SLUGS[@]} failed"
    git commit -m "scam-rebuild queue: $SUMMARY (${SUCCESS_SLUGS[*]:-}${FAILED_SLUGS[*]:+ FAILED: ${FAILED_SLUGS[*]}})" || true
fi

# Retry push up to 5 times to handle concurrent cron pushes — main moves
# fast (other cron jobs land 1-2 commits/min) so the rebase race is real.
# Uses $PUSH_URL with embedded GH_TOKEN to bypass macOS keychain credential
# helper (cron has no tty / keychain access).
for attempt in 1 2 3 4 5; do
    if git push "$PUSH_URL" HEAD:main; then
        break
    fi
    echo "  push failed (attempt $attempt/5), rebasing..."
    git fetch origin main && git rebase origin/main || true
done

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Run complete — $(date '+%Y-%m-%d %H:%M:%S')"
echo "  PRs opened: ${#SUCCESS_PRS[@]} (${SUCCESS_SLUGS[*]:-})"
for entry in "${SUCCESS_PRS[@]:-}"; do
    [ -n "$entry" ] && echo "    → ${entry}"
done
echo "  Failed:    ${#FAILED_SLUGS[@]} (${FAILED_SLUGS[*]:-})"
echo "═══════════════════════════════════════════════════════════════"

exit 0
