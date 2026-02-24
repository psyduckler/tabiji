#!/bin/zsh
# Push to git + deploy to Cloudflare Pages
set -e
cd "$(dirname "$0")"
git push "$@"
echo "🚀 Deploying to Cloudflare Pages..."
wrangler pages deploy . --project-name tabiji --branch main --commit-dirty=true 2>&1 | tail -3
