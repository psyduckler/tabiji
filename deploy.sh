#!/bin/bash
# Deploy tabiji to Cloudflare Pages via direct upload
# Usage: ./deploy.sh [commit message]
# Or just: git push (if using the pre-push hook)

set -e
cd "$(dirname "$0")"

CLOUDFLARE_API_TOKEN=$(security find-generic-password -s "cloudflare-pages-token" -w) \
CLOUDFLARE_ACCOUNT_ID=$(security find-generic-password -s "cloudflare-zonted-account-id" -w) \
wrangler pages deploy . --project-name=tabiji --branch=main

echo "✅ Deployed to tabiji.ai"
