#!/bin/bash
TUNNEL_TOKEN=$(security find-generic-password -a "psy" -s "cloudflare-tunnel-token" -w)
exec /opt/homebrew/bin/cloudflared tunnel --no-autoupdate run --token "$TUNNEL_TOKEN"
