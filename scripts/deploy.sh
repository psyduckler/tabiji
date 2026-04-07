#!/bin/zsh
# Push committed code only; production deploys should come from Cloudflare Pages' git integration.
set -euo pipefail
cd "$(dirname "$0")"

if [[ -n "$(git status --porcelain)" ]]; then
  echo "❌ Refusing to deploy from a dirty working tree. Commit or stash changes first."
  exit 1
fi

echo "📤 Pushing committed changes..."
git push "$@"
echo "✅ Push complete. Cloudflare Pages will deploy from the pushed commit on main."
