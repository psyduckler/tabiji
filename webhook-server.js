#!/usr/bin/env node
// Compatibility entrypoint for launchd / Cloudflare tunnel hosts that still
// invoke the historical repo-root webhook server path.
require('./scripts/webhook-server');
