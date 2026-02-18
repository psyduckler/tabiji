#!/usr/bin/env bash
# wait-for-deploy.sh — Poll a URL until Cloudflare Pages returns 200
# Usage: bash wait-for-deploy.sh <url> [max_seconds] [interval_seconds]
# Exit 0 = live, Exit 1 = timed out

set -euo pipefail

URL="${1:?Usage: wait-for-deploy.sh <url> [max_seconds] [interval_seconds]}"
MAX_SECONDS="${2:-180}"
INTERVAL="${3:-5}"

echo "⏳ Waiting for $URL to return 200 (max ${MAX_SECONDS}s, polling every ${INTERVAL}s)..."

START=$(date +%s)
while true; do
  ELAPSED=$(( $(date +%s) - START ))
  if [ "$ELAPSED" -ge "$MAX_SECONDS" ]; then
    echo "❌ Timed out after ${MAX_SECONDS}s — $URL is NOT live"
    exit 1
  fi

  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL" 2>/dev/null || echo "000")
  if [ "$STATUS" = "200" ]; then
    echo "✅ $URL is live after ${ELAPSED}s"
    exit 0
  fi

  sleep "$INTERVAL"
done
