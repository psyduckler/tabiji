#!/bin/bash
# Send email via Resend API for tabiji.ai
# Usage: send-email.sh --to EMAIL --subject SUBJECT --body-file FILE [--from NAME]
# Usage: send-email.sh --to EMAIL --subject SUBJECT --body "inline text"
#
# ⚠️ THIS IS THE ONLY WAY TO SEND TABIJI CUSTOMER EMAILS.
# DO NOT use gog gmail send. DO NOT use psyduckler@gmail.com.
# All customer emails go from hello@tabiji.ai via Resend.
#
# Requires: resend-api-key in macOS Keychain

set -euo pipefail

FROM_NAME="tabiji"
FROM_EMAIL="hello@tabiji.ai"
TO=""
SUBJECT=""
BODY_FILE=""
BODY_TEXT=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --to) TO="$2"; shift 2 ;;
    --subject) SUBJECT="$2"; shift 2 ;;
    --body-file) BODY_FILE="$2"; shift 2 ;;
    --body) BODY_TEXT="$2"; shift 2 ;;
    --from) FROM_NAME="$2"; shift 2 ;;
    --from-email) FROM_EMAIL="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if [[ -z "$TO" || -z "$SUBJECT" ]]; then
  echo "Usage: send-email.sh --to EMAIL --subject SUBJECT (--body-file FILE | --body TEXT)"
  exit 1
fi

if [[ -z "$BODY_FILE" && -z "$BODY_TEXT" ]]; then
  echo "Error: provide --body-file or --body"
  exit 1
fi

API_KEY=$(security find-generic-password -s "resend-api-key" -w)

if [[ -n "$BODY_FILE" ]]; then
  BODY_JSON=$(python3 -c "import json,sys; print(json.dumps(open(sys.argv[1]).read()))" "$BODY_FILE")
else
  BODY_JSON=$(python3 -c "import json,sys; print(json.dumps(sys.argv[1]))" "$BODY_TEXT")
fi

SUBJECT_JSON=$(python3 -c "import json,sys; print(json.dumps(sys.argv[1]))" "$SUBJECT")

RESPONSE=$(curl -s -X POST https://api.resend.com/emails \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"from\": \"${FROM_NAME} <${FROM_EMAIL}>\",
    \"to\": [\"${TO}\"],
    \"subject\": ${SUBJECT_JSON},
    \"text\": ${BODY_JSON}
  }")

echo "$RESPONSE"

# Check for errors
if echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if 'id' in d else 1)" 2>/dev/null; then
  echo "✅ Email sent successfully from ${FROM_EMAIL} to ${TO}"
else
  echo "❌ Email send failed!"
  exit 1
fi
