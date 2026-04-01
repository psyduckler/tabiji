#!/bin/bash
# publish-reel.sh — Upload video to R2, publish as Instagram Reel, then delete from R2
#
# Usage: ./publish-reel.sh <video_path> <caption>
#
# Requires:
#   - wrangler (authenticated via OAuth)
#   - macOS Keychain: instagram-access-token, instagram-account-id
#
# R2 bucket: tabiji-media
# Public URL: https://pub-594f3e518acc4d3b9c1e2860aff31bc9.r2.dev

set -euo pipefail

VIDEO_PATH="$1"
CAPTION="$2"

if [[ ! -f "$VIDEO_PATH" ]]; then
  echo "❌ Video file not found: $VIDEO_PATH" >&2
  exit 1
fi

R2_BUCKET="tabiji-media"
R2_PUBLIC_BASE="https://pub-594f3e518acc4d3b9c1e2860aff31bc9.r2.dev"
FILENAME="reel-$(date +%s)-$(basename "$VIDEO_PATH")"
R2_KEY="instagram/${FILENAME}"

IG_TOKEN=$(security find-generic-password -s "instagram-access-token" -w)
IG_ACCOUNT=$(security find-generic-password -s "instagram-account-id" -w)

# 1. Upload to R2
echo "📤 Uploading to R2: ${R2_KEY}"
cat "$VIDEO_PATH" | wrangler r2 object put "${R2_BUCKET}/${R2_KEY}" \
  --pipe --content-type="video/mp4" --remote 2>/dev/null

VIDEO_URL="${R2_PUBLIC_BASE}/${R2_KEY}"
echo "✅ Uploaded: ${VIDEO_URL}"

# Verify it's accessible
HTTP_STATUS=$(curl -sI "$VIDEO_URL" -o /dev/null -w "%{http_code}")
if [[ "$HTTP_STATUS" != "200" ]]; then
  echo "❌ Video not accessible at ${VIDEO_URL} (HTTP ${HTTP_STATUS})" >&2
  exit 1
fi

# 2. Create Reel container
echo "📱 Creating Instagram Reel container..."
CONTAINER_RESPONSE=$(curl -s -X POST "https://graph.facebook.com/v21.0/${IG_ACCOUNT}/media" \
  -d "media_type=REELS" \
  --data-urlencode "video_url=${VIDEO_URL}" \
  --data-urlencode "caption=${CAPTION}" \
  -d "access_token=${IG_TOKEN}")

CONTAINER_ID=$(echo "$CONTAINER_RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('id',''))")

if [[ -z "$CONTAINER_ID" ]]; then
  echo "❌ Failed to create container: ${CONTAINER_RESPONSE}" >&2
  # Cleanup R2
  wrangler r2 object delete "${R2_BUCKET}/${R2_KEY}" --remote 2>/dev/null
  exit 1
fi

echo "📦 Container ID: ${CONTAINER_ID}"

# 3. Poll until FINISHED (max 10 attempts, 15s each = 2.5 min)
echo "⏳ Waiting for processing..."
for i in $(seq 1 10); do
  sleep 15
  STATUS_RESPONSE=$(curl -s "https://graph.facebook.com/v21.0/${CONTAINER_ID}?fields=status_code,status&access_token=${IG_TOKEN}")
  STATUS_CODE=$(echo "$STATUS_RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin).get('status_code','UNKNOWN'))")
  
  echo "  Attempt ${i}/10: ${STATUS_CODE}"
  
  if [[ "$STATUS_CODE" == "FINISHED" ]]; then
    break
  elif [[ "$STATUS_CODE" == "ERROR" ]]; then
    echo "❌ Processing failed: ${STATUS_RESPONSE}" >&2
    wrangler r2 object delete "${R2_BUCKET}/${R2_KEY}" --remote 2>/dev/null
    exit 1
  fi
done

if [[ "$STATUS_CODE" != "FINISHED" ]]; then
  echo "❌ Timed out waiting for processing" >&2
  wrangler r2 object delete "${R2_BUCKET}/${R2_KEY}" --remote 2>/dev/null
  exit 1
fi

# 4. Publish
echo "🚀 Publishing Reel..."
PUBLISH_RESPONSE=$(curl -s -X POST "https://graph.facebook.com/v21.0/${IG_ACCOUNT}/media_publish" \
  -d "creation_id=${CONTAINER_ID}" \
  -d "access_token=${IG_TOKEN}")

POST_ID=$(echo "$PUBLISH_RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('id',''))")

if [[ -z "$POST_ID" ]]; then
  echo "❌ Publish failed: ${PUBLISH_RESPONSE}" >&2
  wrangler r2 object delete "${R2_BUCKET}/${R2_KEY}" --remote 2>/dev/null
  exit 1
fi

# 5. Get permalink
PERMALINK=$(curl -s "https://graph.facebook.com/v21.0/${POST_ID}?fields=permalink&access_token=${IG_TOKEN}" \
  | python3 -c "import json,sys; print(json.load(sys.stdin).get('permalink',''))")

echo "✅ Published! ${PERMALINK}"

# 6. Copy to TikTok staging folder on R2 (for manual TikTok posting)
echo "📎 Copying to TikTok staging folder..."
TIKTOK_KEY="tmp/tiktok/${FILENAME}"
TIKTOK_TXT_KEY="tmp/tiktok/${FILENAME%.mp4}.txt"

cat "$VIDEO_PATH" | wrangler r2 object put "${R2_BUCKET}/${TIKTOK_KEY}" \
  --pipe --content-type="video/mp4" --remote 2>/dev/null

# Generate TikTok metadata sidecar
TIKTOK_CAPTION=$(echo "$CAPTION" | sed 's/#\([a-zA-Z0-9_]*\)/#\1/g')
TIKTOK_META=$(cat <<EOF
TITLE: ${TIKTOK_CAPTION}

HASHTAGS: $(echo "$CAPTION" | grep -oE '#[a-zA-Z0-9_]+' | tr '\n' ' ')

PRIVACY: PUBLIC_TO_EVERYONE
ALLOW COMMENTS: Yes
ALLOW DUET: Yes
ALLOW STITCH: Yes
AI-GENERATED CONTENT: Yes

VIDEO URL: ${R2_PUBLIC_BASE}/${TIKTOK_KEY}
SOURCE REEL: ${PERMALINK}
DATE: $(date '+%Y-%m-%d %H:%M')
EOF
)
echo "$TIKTOK_META" | wrangler r2 object put "${R2_BUCKET}/${TIKTOK_TXT_KEY}" \
  --pipe --content-type="text/plain; charset=utf-8" --remote 2>/dev/null

echo "✅ TikTok staging: ${R2_PUBLIC_BASE}/${TIKTOK_KEY}"

# 7. Cleanup — delete temp IG video from R2 (TikTok copy persists)
echo "🗑️  Cleaning up R2 (IG temp)..."
wrangler r2 object delete "${R2_BUCKET}/${R2_KEY}" --remote 2>/dev/null
echo "✅ R2 cleanup complete"

echo ""
echo "📊 Summary:"
echo "  Post ID:   ${POST_ID}"
echo "  Permalink: ${PERMALINK}"
echo "  TikTok:    ${R2_PUBLIC_BASE}/${TIKTOK_KEY}"
echo "  TikTok txt: ${R2_PUBLIC_BASE}/${TIKTOK_TXT_KEY}"
