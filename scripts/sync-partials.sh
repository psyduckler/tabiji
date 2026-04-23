#!/bin/bash
# Explicit sync of managed shared-head/nav/footer blocks across all HTML.
#
# Use this AFTER editing any file in _includes/ to propagate the changes
# into every HTML page. The pre-commit hook only verifies the files you
# staged, so propagation is now an intentional operation.
#
# Usage:
#   scripts/sync-partials.sh          # rewrite all HTML, show summary
#   scripts/sync-partials.sh --stage  # also `git add` the updated files

set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

python3 scripts/build-partials.py

if [ "${1:-}" = "--stage" ]; then
  git add _includes assets/shared-shell.css assets/shared-shell.js scripts/build-partials.py
  # Stage any HTML files that the sweep just modified.
  git ls-files -mz -- '*.html' ':(exclude)tmp/**' | xargs -0 -r git add --
  echo ""
  echo "Staged updated files. Review with: git status --short"
fi
