#!/bin/bash
# scam-rebuild-cron.sh — Rebuild scam city pages from the no-comic queue.
#
# Drives the scam-page-builder skill via `claude -p` headless mode, one city
# at a time. Each city is a fresh rewrite (Step 1 outcome 3) — the skill's
# "already book-ready" abort gate is overridden by the prompt. Comics emit
# 404 placeholders; comic art is a separate downstream pass.
#
# Designed to run on an hourly schedule. Default batch size is 1
# (1 page/hour, ~9.3 days to drain the 224-page queue). Override with:
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

REPO="/Users/psy/repos/tabiji"
QUEUE="$REPO/scripts/queues/scam-no-comic-rebuild-queue.json"
LOGDIR="$REPO/logs/scam-rebuild"
BATCH_SIZE="${1:-1}"
PER_CITY_TIMEOUT="${PER_CITY_TIMEOUT:-2400}"  # 40 min hard cap per city
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
LOGFILE="$LOGDIR/run-${TIMESTAMP}.log"

cd "$REPO"
mkdir -p "$LOGDIR"

exec > >(tee -a "$LOGFILE") 2>&1

echo "═══════════════════════════════════════════════════════════════"
echo "  Scam Rebuild Cron — $(date '+%Y-%m-%d %H:%M:%S')"
echo "  Batch size: $BATCH_SIZE   Per-city timeout: ${PER_CITY_TIMEOUT}s"
echo "  Log: $LOGFILE"
echo "═══════════════════════════════════════════════════════════════"

# Pick a timeout binary (macOS ships without `timeout` by default)
TIMEOUT=""
if command -v gtimeout >/dev/null 2>&1; then
    TIMEOUT="gtimeout"
elif command -v timeout >/dev/null 2>&1; then
    TIMEOUT="timeout"
fi
[ -z "$TIMEOUT" ] && echo "(no timeout binary available; running without per-city cap)"

# ─── Step 0: Sync with main ────────────────────────────────────────────────
echo ""
echo "▶ Step 0: Sync with main"
git checkout main 2>/dev/null
git pull --rebase origin main || echo "  ⚠️  pull failed, continuing with local state"

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
git push origin main 2>/dev/null || echo "  ⚠️  push of in-progress markers failed (will retry at end)"

# ─── Step 3: Drive each rebuild via claude -p ──────────────────────────────
declare -a SUCCESS_SLUGS
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

Execution:
- Run Steps 2–12 of the skill (Step 1 already resolved by the rules above).
- Lint must pass (0 REJECT, 0 WARN). If lint fails, fix and re-lint.
- After parser-verify, stage scams/${slug}/index.html, api/v1/scams/${slug}.json, scams/research/${cc}_batchN.json (whichever batch you chose), and any necessary edits to scams/generate_pages.py (CITY_SLUGS, SAFETY_TIPS, FAQS, EMERGENCY_INFO).
- Commit (do NOT push) on the current branch (main) with message: 'scams: rebuild ${city} (${country}) — N Reddit-cited scams (no-comic queue)'
- Use Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
- The parent cron script will batch-push all commits at the end. Do not push yourself.

Output one final message before exiting (no other formatting): a single JSON object on its own line with the schema {\"status\": \"complete\"|\"failed\", \"slug\": \"${slug}\", \"commit\": \"<hash>\"|null, \"error\": \"<short reason if failed>\"|null, \"scam_count\": <int>|null, \"notes\": \"<one-line summary of what changed>\"}.

Proceed autonomously. Do not ask the user any questions."

    # Run claude headless with structured JSON output.
    # IMPORTANT: --add-dir is variadic — it consumes args until the next flag.
    # The prompt MUST come after another flag (here: -p) or after `--`,
    # otherwise claude swallows the prompt as a directory and hangs waiting on stdin.
    set +e
    if [ -n "$TIMEOUT" ]; then
        $TIMEOUT "$PER_CITY_TIMEOUT" claude \
            --model claude-opus-4-7 \
            --output-format json \
            --dangerously-skip-permissions \
            --add-dir "$REPO" \
            -p \
            -- "$PROMPT" < /dev/null > "$city_log" 2>&1
        RC=$?
    else
        claude \
            --model claude-opus-4-7 \
            --output-format json \
            --dangerously-skip-permissions \
            --add-dir "$REPO" \
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
        COMMIT=$(python3 -c "import json; print(json.loads('''$RESULT_JSON''').get('commit') or '')" 2>/dev/null || echo "")
    else
        STATUS=""
        COMMIT=""
    fi

    if [ "$RC" -eq 0 ] && [ "$STATUS" = "complete" ]; then
        echo "  ✅ $slug — complete (commit $COMMIT)"
        SUCCESS_SLUGS+=("$slug")
    else
        REASON="$STATUS"
        [ -z "$REASON" ] && REASON="exit-$RC (no JSON status emitted)"
        echo "  ❌ $slug — $REASON"
        FAILED_SLUGS+=("$slug")
        FAIL_REASONS+=("$REASON")
    fi
done

# ─── Step 4: Update queue with final statuses ──────────────────────────────
echo ""
echo "▶ Step 4: Updating queue statuses"

SUCCESS_CSV=$(IFS=,; echo "${SUCCESS_SLUGS[*]:-}")
FAILED_CSV=$(IFS=,; echo "${FAILED_SLUGS[*]:-}")

SUCCESS_CSV="$SUCCESS_CSV" FAILED_CSV="$FAILED_CSV" python3 -c "
import json, os
from datetime import datetime, timezone
q = json.load(open('$QUEUE'))
done = set(s for s in os.environ['SUCCESS_CSV'].split(',') if s)
failed = set(s for s in os.environ['FAILED_CSV'].split(',') if s)
now = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
for it in q['queue']:
    if it['slug'] in done:
        it['status'] = 'complete'
        it['completed_at'] = now
    elif it['slug'] in failed:
        it['status'] = 'failed'
        it['completed_at'] = now
totals = {'pending': 0, 'in-progress': 0, 'complete': 0, 'failed': 0, 'skipped': 0}
for it in q['queue']:
    totals[it['status']] = totals.get(it['status'], 0) + 1
q['meta']['progress'] = totals
json.dump(q, open('$QUEUE', 'w'), indent=2, ensure_ascii=False)
open('$QUEUE','a').write('\n')
print(f'  done={len(done)} failed={len(failed)} totals={totals}')
"

# ─── Step 5: Commit queue update + push everything ─────────────────────────
echo ""
echo "▶ Step 5: Committing queue update and pushing all rebuild commits"

git add "$QUEUE"
if ! git diff --cached --quiet; then
    SUMMARY="${#SUCCESS_SLUGS[@]} done"
    [ ${#FAILED_SLUGS[@]} -gt 0 ] && SUMMARY="$SUMMARY, ${#FAILED_SLUGS[@]} failed"
    git commit -m "scam-rebuild queue: $SUMMARY (${SUCCESS_SLUGS[*]:-}${FAILED_SLUGS[*]:+ FAILED: ${FAILED_SLUGS[*]}})" || true
fi

# Retry push up to 3 times to handle concurrent cron pushes
for attempt in 1 2 3; do
    if git push origin main; then
        break
    fi
    echo "  push failed (attempt $attempt/3), rebasing..."
    git pull --rebase origin main || true
done

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Run complete — $(date '+%Y-%m-%d %H:%M:%S')"
echo "  Succeeded: ${#SUCCESS_SLUGS[@]} (${SUCCESS_SLUGS[*]:-})"
echo "  Failed:    ${#FAILED_SLUGS[@]} (${FAILED_SLUGS[*]:-})"
echo "═══════════════════════════════════════════════════════════════"

exit 0
