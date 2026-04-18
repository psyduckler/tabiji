#!/bin/bash
# publish-video.sh — Shell wrapper for publish-video.py
#
# Usage: ./publish-video.sh <video_path> "<caption>" [thumb_offset] [source]
#
# Backward-compatible with old publish-reel.sh call signature.
# For full options, call publish-video.py directly.

set -euo pipefail

VIDEO="${1:?Usage: publish-video.sh <video> <caption> [thumb_offset] [source]}"
CAPTION="${2:?Caption required}"
THUMB="${3:-1000}"
SOURCE="${4:-}"

exec python3 "$(dirname "$0")/publish-video.py" \
  --video "$VIDEO" \
  --caption "$CAPTION" \
  --thumb-offset "$THUMB" \
  --source "$SOURCE"
