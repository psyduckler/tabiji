#!/bin/bash
# publish-youtube-short.sh — Upload a video to YouTube Shorts after IG publish
#
# Usage: ./publish-youtube-short.sh <video_path> "<title>" "<description>" "<tags>"
#
# Reads OAuth creds from macOS Keychain (youtube-client-id, youtube-client-secret, youtube-refresh-token)
# Returns the YouTube Shorts URL on success.

set -euo pipefail

VIDEO_PATH="${1:?Usage: publish-youtube-short.sh <video> <title> [description] [tags]}"
TITLE="${2:?Title required}"
DESCRIPTION="${3:-}"
TAGS="${4:-travel,tabiji}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
UPLOAD_SCRIPT="$HOME/.openclaw/workspace/scripts/youtube-upload.py"

if [ ! -f "$VIDEO_PATH" ]; then
    echo "❌ Video not found: $VIDEO_PATH" >&2
    exit 1
fi

if [ ! -f "$UPLOAD_SCRIPT" ]; then
    echo "❌ YouTube upload script not found: $UPLOAD_SCRIPT" >&2
    exit 1
fi

echo "📺 Uploading to YouTube Shorts: $TITLE"

python3 "$UPLOAD_SCRIPT" upload "$VIDEO_PATH" \
    --title "$TITLE" \
    --description "$DESCRIPTION" \
    --tags "$TAGS" \
    --privacy public

echo "📺 YouTube Shorts upload complete"
