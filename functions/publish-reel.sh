#!/bin/bash
# publish-reel.sh — Upload video to R2, publish as Instagram Reel, then delete from R2
#
# Usage: ./publish-reel.sh <video_path> <caption>
#
# Requires macOS Keychain keys:
#   - instagram-access-token
#   - instagram-account-id
#   - cloudflare-pages-token
# Optional:
#   - facebook-page-id
#
# R2 bucket: tabiji-media
# Public URL: https://img.tabiji.ai

set -euo pipefail

VIDEO_PATH="${1:?Usage: ./publish-reel.sh <video_path> <caption>}"
CAPTION="${2:?Caption required}"
THUMB_OFFSET="${THUMB_OFFSET:-500}"

if [[ ! -f "$VIDEO_PATH" ]]; then
  echo "❌ Video file not found: $VIDEO_PATH" >&2
  exit 1
fi

CF_TOKEN=$(security find-generic-password -s "cloudflare-pages-token" -w)
IG_TOKEN=$(security find-generic-password -s "instagram-access-token" -w)
IG_ACCOUNT=$(security find-generic-password -s "instagram-account-id" -w)

R2_ACCOUNT="9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET="tabiji-media"
R2_PUBLIC_BASE="https://img.tabiji.ai"
FILENAME="reel-$(date +%s)-$(basename "$VIDEO_PATH")"
R2_KEY="instagram/${FILENAME}"
VIDEO_URL="${R2_PUBLIC_BASE}/${R2_KEY}"
TIKTOK_KEY="tmp/tiktok/${FILENAME}"
TIKTOK_TXT_KEY="tmp/tiktok/${FILENAME%.mp4}.txt"

cleanup_ig_r2() {
  curl -s -X DELETE \
    -H "Authorization: Bearer ${CF_TOKEN}" \
    "https://api.cloudflare.com/client/v4/accounts/${R2_ACCOUNT}/r2/buckets/${R2_BUCKET}/objects/${R2_KEY}" >/dev/null || true
}

upload_r2() {
  local src="$1"
  local key="$2"
  local content_type="$3"
  curl -s -X PUT \
    -H "Authorization: Bearer ${CF_TOKEN}" \
    -H "Content-Type: ${content_type}" \
    --data-binary "@${src}" \
    "https://api.cloudflare.com/client/v4/accounts/${R2_ACCOUNT}/r2/buckets/${R2_BUCKET}/objects/${key}"
}

upload_r2_stdin() {
  local key="$1"
  local content_type="$2"
  curl -s -X PUT \
    -H "Authorization: Bearer ${CF_TOKEN}" \
    -H "Content-Type: ${content_type}" \
    --data-binary @- \
    "https://api.cloudflare.com/client/v4/accounts/${R2_ACCOUNT}/r2/buckets/${R2_BUCKET}/objects/${key}"
}

ig_get() {
  local path="$1"
  curl -s "https://graph.facebook.com/v22.0/${path}?access_token=${IG_TOKEN}"
}

ig_post() {
  local path="$1"
  shift
  curl -s -X POST "https://graph.facebook.com/v22.0/${path}" -d "access_token=${IG_TOKEN}" "$@"
}

echo "📤 Uploading to R2: ${R2_KEY}"
UPLOAD_RESULT=$(upload_r2 "$VIDEO_PATH" "$R2_KEY" "video/mp4")
echo "$UPLOAD_RESULT" | python3 -c 'import sys,json; d=json.load(sys.stdin); sys.exit(0 if d.get("success") else 1)'

echo "✅ Uploaded: ${VIDEO_URL}"

echo "⏳ Waiting for R2 propagation..."
sleep 5

HTTP_STATUS=$(curl -sI "$VIDEO_URL" -o /dev/null -w "%{http_code}")
if [[ "$HTTP_STATUS" != "200" ]]; then
  echo "⏳ Edge not ready yet (HTTP ${HTTP_STATUS}), waiting a bit longer..."
  sleep 10
  HTTP_STATUS=$(curl -sI "$VIDEO_URL" -o /dev/null -w "%{http_code}")
fi
if [[ "$HTTP_STATUS" != "200" ]]; then
  echo "❌ Video not accessible at ${VIDEO_URL} (HTTP ${HTTP_STATUS})" >&2
  cleanup_ig_r2
  exit 1
fi

echo "📱 Creating Instagram Reel container..."
CONTAINER_RESPONSE=$(ig_post "${IG_ACCOUNT}/media" \
  -d "media_type=REELS" \
  --data-urlencode "video_url=${VIDEO_URL}" \
  --data-urlencode "caption=${CAPTION}" \
  -d "thumb_offset=${THUMB_OFFSET}")

CONTAINER_ID=$(echo "$CONTAINER_RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('id',''))")
if [[ -z "$CONTAINER_ID" ]]; then
  echo "❌ Failed to create container: ${CONTAINER_RESPONSE}" >&2
  cleanup_ig_r2
  exit 1
fi

echo "📦 Container ID: ${CONTAINER_ID}"
echo "⏳ Waiting for processing..."
STATUS_CODE="UNKNOWN"
for i in $(seq 1 24); do
  sleep 10
  STATUS_RESPONSE=$(curl -s "https://graph.facebook.com/v22.0/${CONTAINER_ID}?fields=status_code,status&access_token=${IG_TOKEN}")
  STATUS_CODE=$(echo "$STATUS_RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin).get('status_code','UNKNOWN'))")
  echo "  Attempt ${i}/24: ${STATUS_CODE}"
  if [[ "$STATUS_CODE" == "FINISHED" ]]; then
    break
  elif [[ "$STATUS_CODE" == "ERROR" ]]; then
    echo "❌ Processing failed: ${STATUS_RESPONSE}" >&2
    cleanup_ig_r2
    exit 1
  fi
done

if [[ "$STATUS_CODE" != "FINISHED" ]]; then
  echo "❌ Timed out waiting for processing" >&2
  cleanup_ig_r2
  exit 1
fi

echo "🚀 Publishing Reel..."
PUBLISH_RESPONSE=$(ig_post "${IG_ACCOUNT}/media_publish" -d "creation_id=${CONTAINER_ID}")
POST_ID=$(echo "$PUBLISH_RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('id',''))")
if [[ -z "$POST_ID" ]]; then
  echo "❌ Publish failed: ${PUBLISH_RESPONSE}" >&2
  cleanup_ig_r2
  exit 1
fi

sleep 5
PERMALINK=$(ig_get "${POST_ID}&fields=permalink" | python3 -c "import json,sys; print(json.load(sys.stdin).get('permalink',''))")
echo "✅ Published! ${PERMALINK}"

echo "📎 Copying to TikTok staging folder..."
TIKTOK_UPLOAD=$(upload_r2 "$VIDEO_PATH" "$TIKTOK_KEY" "video/mp4")
echo "$TIKTOK_UPLOAD" | python3 -c 'import sys,json; d=json.load(sys.stdin); sys.exit(0 if d.get("success") else 1)'

TIKTOK_CAPTION="$CAPTION"
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
echo "$TIKTOK_META" | upload_r2_stdin "$TIKTOK_TXT_KEY" "text/plain; charset=utf-8" >/dev/null

echo "✅ TikTok staging: ${R2_PUBLIC_BASE}/${TIKTOK_KEY}"

echo "📘 Cross-posting to Facebook Page Reel..."
FB_URL=$(python3 "$HOME/.openclaw/workspace/scripts/publish_fb_reel.py" "$VIDEO_PATH" "$CAPTION" 2>&1 | tail -1)
if [[ "$FB_URL" == https* ]]; then
  echo "✅ Facebook: ${FB_URL}"
else
  echo "⚠️  FB Reel cross-post failed (non-blocking)"
fi

echo "🗑️  Cleaning up R2 (IG temp)..."
cleanup_ig_r2
echo "✅ R2 cleanup complete"

echo ""
echo "📊 Summary:"
echo "  Post ID:    ${POST_ID}"
echo "  Permalink:  ${PERMALINK}"
echo "  TikTok:     ${R2_PUBLIC_BASE}/${TIKTOK_KEY}"
echo "  TikTok txt: ${R2_PUBLIC_BASE}/${TIKTOK_TXT_KEY}"