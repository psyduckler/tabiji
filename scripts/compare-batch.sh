#!/bin/bash
# compare-batch.sh — Build N compare pages from the queue in one batch.
# Usage: compare-batch.sh [count] [parallelism]
set -uo pipefail

REPO="/Users/psy/tabiji"
QUEUE="$REPO/compare-queue.json"
SCRIPT="$REPO/scripts/batch-compare-gen.py"
COUNT="${1:-10}"
PARALLEL="${2:-5}"

cd "$REPO"

# Get pending slugs into a temp file
python3 -c "
import json
q = json.load(open('$QUEUE'))
pending = [x['slug'] for x in q if x.get('status') == 'pending']
for s in pending[:$COUNT]:
    print(s)
" > /tmp/compare-batch-slugs.txt

TOTAL=$(wc -l < /tmp/compare-batch-slugs.txt | tr -d ' ')
if [ "$TOTAL" -eq 0 ]; then
    echo "Queue empty — no pending compare pages."
    exit 0
fi

echo "🚀 Generating $TOTAL compare pages ($PARALLEL parallel workers)..."
echo ""

# Worker function
worker() {
    local slug="$1"
    echo "  ⏳ $slug"
    if python3 "$SCRIPT" generate "$slug" > /tmp/compare-gen-${slug}.log 2>&1; then
        echo "  ✅ $slug"
    else
        echo "  ❌ $slug"
    fi
}
export -f worker
export SCRIPT REPO

# Run in parallel
cat /tmp/compare-batch-slugs.txt | xargs -P "$PARALLEL" -I {} bash -c 'worker "$@"' _ {} 2>&1 | tee /tmp/compare-batch.log

# Count results
SUCCESS=$(grep -c "✅" /tmp/compare-batch.log || true)
FAIL=$(grep -c "❌" /tmp/compare-batch.log || true)

echo ""
echo "Generation complete: $SUCCESS succeeded, $FAIL failed out of $TOTAL"

if [ "$SUCCESS" -eq 0 ]; then
    echo "No pages generated — skipping finalize and push."
    exit 1
fi

# Finalize once (inventory + sitemap)
echo "📋 Finalizing inventory + sitemap..."
python3 "$SCRIPT" finalize

# Git push once
echo "📤 Pushing to git..."
git add -A
git commit -m "compare: batch of $SUCCESS pages" || { echo "Nothing to commit"; exit 0; }

for i in 1 2 3; do
    if git push; then
        echo ""
        echo "✅ All done! $SUCCESS compare pages built and pushed."
        exit 0
    fi
    echo "Push failed (attempt $i), pulling with rebase..."
    git pull --rebase
done

echo "❌ Failed to push after 3 attempts"
exit 1
