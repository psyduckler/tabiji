#!/bin/bash
# compare-cron.sh — Build one compare page from the queue, finalize, and git push.
# Designed to run as a cron shell command (no AI sub-agent needed).
set -euo pipefail

REPO="/Users/psy/tabiji"
QUEUE="$REPO/compare-queue.json"
SCRIPT="$REPO/scripts/batch-compare-gen.py"

cd "$REPO"

# Find first pending slug
SLUG=$(python3 -c "
import json
q = json.load(open('$QUEUE'))
pending = [x['slug'] for x in q if x.get('status') == 'pending']
if pending:
    print(pending[0])
else:
    print('')
")

if [ -z "$SLUG" ]; then
    echo "Queue empty — no pending compare pages."
    exit 0
fi

echo "Building compare page: $SLUG"

# Generate content + HTML + API JSON
python3 "$SCRIPT" generate "$SLUG"

# Update inventory + sitemap
python3 "$SCRIPT" finalize

# Git add, commit, push (with rebase retry)
git add -A
git commit -m "compare: $SLUG" || { echo "Nothing to commit"; exit 0; }

for i in 1 2 3; do
    if git push; then
        echo "✅ Pushed compare: $SLUG"
        exit 0
    fi
    echo "Push failed (attempt $i), pulling with rebase..."
    git pull --rebase
done

echo "❌ Failed to push after 3 attempts"
exit 1
