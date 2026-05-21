#!/usr/bin/env node
'use strict';

/**
 * Tabiji order watchdog.
 *
 * Safety net for itinerary fulfillment:
 * - clears dead stale fulfillment locks
 * - resets stale in-progress orders whose worker died/timed out
 * - re-wakes OpenClaw for new pending orders that are older than MIN_PENDING_AGE_MS
 *
 * It intentionally does NOT generate itineraries itself; fulfillment must still go
 * through functions/fulfill-order.js inside the agent run.
 */

const fs = require('fs');
const http = require('http');
const path = require('path');
const os = require('os');
const { execFileSync } = require('child_process');

const REPO_ROOT = path.resolve(__dirname, '..');
const ORDERS_DIR = path.join(REPO_ROOT, 'orders');
const PENDING_FILE = path.join(ORDERS_DIR, 'pending.json');
const STATE_FILE = path.join(ORDERS_DIR, 'watchdog-state.json');
const LOCK_DIR = path.join(REPO_ROOT, '.fulfillment.lockdir');
const WEBHOOK_PLIST = path.join(os.homedir(), 'Library/LaunchAgents/ai.tabiji.webhook-server.plist');

const MIN_PENDING_AGE_MS = Number(process.env.TABIJI_WATCHDOG_MIN_PENDING_MS || 5 * 60 * 1000);
const RETRY_AFTER_MS = Number(process.env.TABIJI_WATCHDOG_RETRY_MS || 30 * 60 * 1000);
const STALE_IN_PROGRESS_MS = Number(process.env.TABIJI_WATCHDOG_STALE_IN_PROGRESS_MS || 45 * 60 * 1000);
const HARD_STALE_IN_PROGRESS_MS = Number(process.env.TABIJI_WATCHDOG_HARD_STALE_IN_PROGRESS_MS || 2 * 60 * 60 * 1000);
const STALE_LOCK_MS = Number(process.env.TABIJI_WATCHDOG_STALE_LOCK_MS || 15 * 60 * 1000);
const MAX_RETRIES = Number(process.env.TABIJI_WATCHDOG_MAX_RETRIES || 4);

const args = new Set(process.argv.slice(2));
const DRY_RUN = args.has('--dry-run');
const INCLUDE_EXISTING = args.has('--include-existing');
const FORCE = args.has('--force');

function log(...parts) {
  console.log(`${new Date().toISOString()} ${parts.join(' ')}`);
}

function readJson(file, fallback) {
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); }
  catch { return fallback; }
}

function writeJsonAtomic(file, data) {
  const tmp = `${file}.tmp-${process.pid}`;
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2));
  fs.renameSync(tmp, file);
}

function parseTime(value) {
  if (!value) return 0;
  if (typeof value === 'number') return value > 10_000_000_000 ? value : value * 1000;
  const parsed = Date.parse(value);
  return Number.isFinite(parsed) ? parsed : 0;
}

function orderTime(order) {
  return parseTime(order.timestamp) || parseTime(order.createdAt) || parseTime(order.created_at) || 0;
}

function pidAlive(pid) {
  if (!pid || !Number.isFinite(Number(pid))) return false;
  try {
    process.kill(Number(pid), 0);
    return true;
  } catch (err) {
    return err.code === 'EPERM';
  }
}

function loadToken() {
  if (process.env.OPENCLAW_HOOKS_TOKEN) return process.env.OPENCLAW_HOOKS_TOKEN;
  try {
    return execFileSync('/usr/bin/plutil', [
      '-extract', 'EnvironmentVariables.OPENCLAW_HOOKS_TOKEN', 'raw', WEBHOOK_PLIST,
    ], { encoding: 'utf8' }).trim();
  } catch {
    return '';
  }
}

function moveStaleLock(now) {
  if (!fs.existsSync(LOCK_DIR)) return { changed: false, reason: 'no-lock' };
  const infoPath = path.join(LOCK_DIR, 'info.json');
  const info = readJson(infoPath, {});
  const ts = parseTime(info.ts);
  const age = ts ? now - ts : Number.POSITIVE_INFINITY;
  const alive = pidAlive(info.pid);
  if (age < STALE_LOCK_MS || alive) {
    return { changed: false, reason: `active-lock order=${info.orderId || '?'} pid=${info.pid || '?'} alive=${alive} ageSec=${Math.round(age / 1000)}` };
  }
  const backup = path.join(REPO_ROOT, `.fulfillment.lockdir.stale-${Math.floor(now / 1000)}`);
  if (!DRY_RUN) fs.renameSync(LOCK_DIR, backup);
  return { changed: true, reason: `moved stale lock order=${info.orderId || '?'} pid=${info.pid || '?'} backup=${backup}` };
}

function resetStaleInProgress(orders, now) {
  const reset = [];
  for (const order of orders) {
    if (order.status !== 'in-progress') continue;
    const claimedAt = parseTime(order.claimedAt);
    const age = claimedAt ? now - claimedAt : Number.POSITIVE_INFINITY;
    const alive = pidAlive(order.claimedBy);
    if ((!alive && age >= STALE_IN_PROGRESS_MS) || age >= HARD_STALE_IN_PROGRESS_MS) {
      reset.push({ id: order.id || order.orderId, destination: order.destination, claimedBy: order.claimedBy, ageMs: age, alive });
      order.status = 'pending';
      order.watchdogResetAt = new Date(now).toISOString();
      order.watchdogResetReason = alive ? 'hard-stale-in-progress' : 'dead-worker-stale-in-progress';
      delete order.claimedBy;
      delete order.claimedAt;
    }
  }
  return reset;
}

function buildAgentMessage(order, attempt) {
  return `Before starting, read these files for context:\n1. memory/${new Date().toISOString().slice(0, 10)}.md (today's date)\n2. MEMORY.md (long-term context)\n3. memory/tabiji.md\n4. tabiji/ARCHITECTURE.md section 1.5\n\n⛔ CRITICAL API KEYS — use these EXACT keys, do NOT use any other:\n- Google Maps API key (ALL tabiji pages): AIzaSyBP0yidMjJEECgkIiZz2lw1NLsQ7jdASYc\n- For any other API keys, read them from macOS Keychain at runtime (see TOOLS.md)\n\n---\n\n🎌 TABIJI WATCHDOG: pending order needs fulfillment. Attempt ${attempt}.\n\nOrder details:\n- ID: ${order.id || order.orderId}\n- Destination: ${order.destination}\n- Email: ${order.email}\n- Dates: ${order.start_date || order.startDate || ''} to ${order.end_date || order.endDate || ''}\n- Group size: ${order.group_size || order.groupSize || ''}\n- Style: ${order.travel_style || order.travelStyle || ''}\n- Dining: ${order.dining || ''}\n- Budget: ${order.budget || ''}\n- Requests: ${order.requests || ''}\n- Amount: $${order.amount || '0.00'}\n\n⛔ MANDATORY: Use tabiji/functions/fulfill-order.js for ALL fulfillment.\n⛔ BEFORE starting: read /Users/psy/.openclaw/workspace/tabiji/orders/pending.json and check this order's status. If it is in-progress or fulfilled, STOP — another agent already claimed it.\n⛔ DO NOT manually create HTML, git push, or send email as separate steps.\n⛔ DO NOT bypass fulfill-order.js for any reason.\n\nSteps:\n1. Read tabiji/scripts/fulfill-sydney.js completely as the template for itineraryData.\n2. Research the destination using web_search.\n3. Build complete itineraryData with required mapPins for every day.\n4. Write a fulfillment script for this order under tabiji/scripts/.\n5. Run that script so it calls fulfillOrder(order, itineraryData).\n6. Report final status, slug, URL, and email result.\n\nThe watchdog will retry/escalate if the order remains pending.`;
}

function postAgentHook(order, attempt, token) {
  const orderId = order.id || order.orderId;
  const payload = JSON.stringify({
    message: buildAgentMessage(order, attempt),
    name: 'Tabiji Watchdog Order',
    sessionKey: `hook:tabiji-order:${orderId}:watchdog:${attempt}`,
    wakeMode: 'now',
    deliver: true,
    channel: 'slack',
    model: 'anthropic/claude-opus-4-6',
  });

  return new Promise((resolve) => {
    const req = http.request({
      hostname: '127.0.0.1',
      port: 18789,
      path: '/hooks/agent',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        'Content-Length': Buffer.byteLength(payload),
      },
      timeout: 15000,
    }, (res) => {
      let body = '';
      res.on('data', chunk => { body += chunk; });
      res.on('end', () => resolve({ ok: res.statusCode >= 200 && res.statusCode < 300, statusCode: res.statusCode, body }));
    });
    req.on('timeout', () => { req.destroy(new Error('timeout')); });
    req.on('error', err => resolve({ ok: false, error: err.message }));
    req.write(payload);
    req.end();
  });
}

async function main() {
  const now = Date.now();
  const state = readJson(STATE_FILE, { installedAt: new Date(now).toISOString(), orders: {} });
  if (!state.installedAt) state.installedAt = new Date(now).toISOString();
  if (!state.orders) state.orders = {};
  const installedAtMs = parseTime(state.installedAt) || now;

  const lockResult = moveStaleLock(now);
  log(`lock: ${lockResult.reason}`);

  const orders = readJson(PENDING_FILE, []);
  if (!Array.isArray(orders)) throw new Error(`${PENDING_FILE} is not an array`);

  const reset = resetStaleInProgress(orders, now);
  for (const item of reset) log(`reset stale in-progress: ${JSON.stringify(item)}`);

  if ((lockResult.changed || reset.length) && !DRY_RUN) writeJsonAtomic(PENDING_FILE, orders);

  const token = loadToken();
  const candidates = [];
  for (const order of orders) {
    const orderId = order.id || order.orderId;
    if (!orderId || order.status !== 'pending') continue;
    const ts = orderTime(order);
    const age = ts ? now - ts : Number.POSITIVE_INFINITY;
    if (!FORCE && age < MIN_PENDING_AGE_MS) continue;
    if (!INCLUDE_EXISTING && ts && ts < installedAtMs) {
      log(`skip grandfathered pending order=${orderId} destination=${JSON.stringify(order.destination)} ts=${new Date(ts).toISOString()}`);
      continue;
    }
    const s = state.orders[orderId] || {};
    const attempts = Number(s.attempts || 0);
    const lastTriggeredAt = parseTime(s.lastTriggeredAt);
    if (!FORCE && attempts >= MAX_RETRIES) {
      log(`max retries reached order=${orderId} attempts=${attempts}`);
      continue;
    }
    if (!FORCE && lastTriggeredAt && now - lastTriggeredAt < RETRY_AFTER_MS) {
      log(`skip retry-wait order=${orderId} nextInSec=${Math.round((RETRY_AFTER_MS - (now - lastTriggeredAt)) / 1000)}`);
      continue;
    }
    candidates.push({ order, attempts });
  }

  if (!candidates.length) {
    log(`ok: no eligible pending orders (pending=${orders.filter(o => o.status === 'pending').length}, reset=${reset.length}, dryRun=${DRY_RUN})`);
    if (!DRY_RUN && !fs.existsSync(STATE_FILE)) writeJsonAtomic(STATE_FILE, state);
    return;
  }

  if (!token) throw new Error('OPENCLAW_HOOKS_TOKEN unavailable; cannot wake fulfillment agents');

  for (const { order, attempts } of candidates) {
    const orderId = order.id || order.orderId;
    const nextAttempt = attempts + 1;
    if (DRY_RUN) {
      log(`dry-run would trigger order=${orderId} destination=${JSON.stringify(order.destination)} attempt=${nextAttempt}`);
      continue;
    }
    const result = await postAgentHook(order, nextAttempt, token);
    state.orders[orderId] = {
      attempts: nextAttempt,
      lastTriggeredAt: new Date(now).toISOString(),
      lastResult: result,
      destination: order.destination,
      email: order.email,
    };
    log(`trigger order=${orderId} attempt=${nextAttempt} result=${JSON.stringify(result)}`);
    writeJsonAtomic(STATE_FILE, state);
  }
}

main().catch(err => {
  console.error(`${new Date().toISOString()} fatal: ${err.stack || err.message}`);
  process.exitCode = 1;
});
