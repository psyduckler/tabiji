#!/bin/bash
# Point git at the repo-tracked hooks in .githooks/ so every clone picks them up.
#
# Why this exists:
#   Git does NOT follow .githooks/ by default — core.hooksPath is per-clone
#   config and points to .git/hooks/ unless you tell it otherwise. That means
#   pre-commit protections (verify-only partials check, hero-bg guard) are
#   silently inactive on every fresh clone until someone runs this.
#
# Run once per clone. Idempotent — re-running just rewrites the same path.

set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

if [ ! -d .githooks ]; then
  echo "❌ .githooks/ directory not found at repo root. Run from a Tabiji checkout."
  exit 1
fi

# core.hooksPath accepts relative paths; they're resolved against the worktree
# root per git-config(1). Relative is preferable so the config is portable
# across different users' absolute paths.
git config --local core.hooksPath .githooks

# Ensure all hook files are executable (in case a `git clone` on a system
# that doesn't preserve executable bits unpacked them read-only).
chmod +x .githooks/*

echo "✓ core.hooksPath = .githooks"
echo "✓ hooks marked executable"
echo ""
echo "Active hooks:"
ls .githooks | grep -v README | sed 's/^/  /'
