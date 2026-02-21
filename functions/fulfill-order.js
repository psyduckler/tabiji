const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const generateSlug = require('./generate-slug');
const generateItineraryHTML = require('./generate-itinerary-html');

const REPO_ROOT = path.resolve(__dirname, '..');
const LOCK_FILE = path.join(REPO_ROOT, '.fulfillment.lock');
const LOCK_DIR = path.join(REPO_ROOT, '.fulfillment.lockdir'); // atomic mkdir lock
const PENDING_FILE = path.join(REPO_ROOT, 'orders', 'pending.json');
const FULFILLED_FILE = path.join(REPO_ROOT, 'orders', 'fulfilled.json');
const STALE_LOCK_MS = 10 * 60 * 1000; // 10 min

// Atomic write helper — write to .tmp then rename to avoid corruption mid-write
function atomicWrite(filePath, data) {
  const tmpPath = filePath + '.tmp';
  fs.writeFileSync(tmpPath, JSON.stringify(data, null, 2));
  fs.renameSync(tmpPath, filePath);
}

/**
 * Acquire an atomic lock using mkdir (POSIX atomic).
 * Returns true if lock acquired, throws if another process holds it.
 */
function acquireLock(orderId) {
  try {
    fs.mkdirSync(LOCK_DIR);
  } catch (err) {
    if (err.code === 'EEXIST') {
      // Lock exists — check if stale
      try {
        const infoPath = path.join(LOCK_DIR, 'info.json');
        const lockData = JSON.parse(fs.readFileSync(infoPath, 'utf8'));
        const lockAge = Date.now() - new Date(lockData.ts).getTime();
        if (lockAge < STALE_LOCK_MS) {
          throw new Error(`Fulfillment locked by order ${lockData.orderId} (pid ${lockData.pid}, ${Math.round(lockAge / 1000)}s ago). Another agent is already fulfilling.`);
        }
        console.warn(`Stale lock found (${Math.round(lockAge / 1000)}s old) — breaking it`);
        fs.rmSync(LOCK_DIR, { recursive: true });
        fs.mkdirSync(LOCK_DIR);
      } catch (innerErr) {
        if (innerErr.message.includes('Fulfillment locked')) throw innerErr;
        // Couldn't read lock info — try to break and re-acquire
        try { fs.rmSync(LOCK_DIR, { recursive: true }); } catch (_) {}
        fs.mkdirSync(LOCK_DIR);
      }
    } else {
      throw err;
    }
  }
  // Write lock info
  const infoPath = path.join(LOCK_DIR, 'info.json');
  fs.writeFileSync(infoPath, JSON.stringify({ orderId, ts: new Date().toISOString(), pid: process.pid }));
  return true;
}

function releaseLock() {
  try { fs.rmSync(LOCK_DIR, { recursive: true }); } catch (_) {}
}

/**
 * Fulfills an order by generating an HTML itinerary and deploying it.
 * @param {Object} order - The order object from pending.json
 * @param {Object} itineraryData - Structured itinerary data (without slug)
 * @returns {Object} { slug, url, filePath }
 */
function fulfillOrder(order, itineraryData) {
  // --- Normalize order ID: accept id or orderId from caller ---
  const _orderId = order.id || order.orderId;
  if (!_orderId) {
    throw new Error('Order must have an "id" or "orderId" field');
  }

  // --- Claim check: prevent duplicate fulfillment of same order ---
  try {
    const pending = JSON.parse(fs.readFileSync(PENDING_FILE, 'utf8'));
    const match = pending.find(o => (o.id || o.orderId) === _orderId);
    if (match && match.status === 'in-progress') {
      throw new Error(`Order ${_orderId} is already being fulfilled (status: in-progress). Aborting to prevent duplicate.`);
    }
    if (match && match.status === 'fulfilled') {
      throw new Error(`Order ${_orderId} is already fulfilled (slug: ${match.slug}). Aborting.`);
    }
    // Claim it — atomic write to avoid race conditions
    if (match) {
      match.status = 'in-progress';
      match.claimedAt = new Date().toISOString();
      match.claimedBy = process.pid;
      atomicWrite(PENDING_FILE, pending);
      console.log(`✅ Claimed order ${_orderId} (pid ${process.pid}, status → in-progress)`);
    }
  } catch (err) {
    if (err.message.includes('already')) throw err;
    console.warn('Could not check/claim order in pending.json:', err.message);
  }

  // --- Atomic lock: prevent concurrent fulfillments (mkdir is POSIX-atomic) ---
  acquireLock(_orderId);

  // Wrap in try/finally to always release lock
  try {
    return _doFulfill(order, itineraryData, _orderId);
  } finally {
    releaseLock();
    // Clean up legacy lock file if present
    try { fs.unlinkSync(LOCK_FILE); } catch (_) {}
  }
}

function _doFulfill(order, itineraryData, _orderId) {
  // Validate: every day MUST have mapPins with lat/lng
  if (itineraryData.days && itineraryData.days.length) {
    const missingMaps = itineraryData.days.filter(d => !d.mapPins || !d.mapPins.length);
    if (missingMaps.length) {
      const nums = missingMaps.map(d => d.num).join(', ');
      throw new Error(`VALIDATION FAILED: Days [${nums}] are missing mapPins. Every day MUST have at least 2 mapPins with {lat, lng, label, num, cat, desc}. Regenerate the itinerary data with mapPins for ALL days.`);
    }
    // Validate each pin has required fields
    for (const day of itineraryData.days) {
      for (const pin of day.mapPins) {
        if (typeof pin.lat !== 'number' || typeof pin.lng !== 'number' || !pin.label) {
          throw new Error(`VALIDATION FAILED: Day ${day.num} has invalid mapPin. Each pin needs: {lat: number, lng: number, label: string, num: number, cat: string, desc: string}`);
        }
      }
    }
  }

  // Generate unique slug
  const slug = generateSlug(REPO_ROOT);

  // Merge slug into data
  const data = { ...itineraryData, slug };

  // Generate HTML
  const html = generateItineraryHTML(data);

  // Write to /i/{slug}/index.html
  const dir = path.join(REPO_ROOT, 'i', slug);
  fs.mkdirSync(dir, { recursive: true });
  const filePath = path.join(dir, 'index.html');
  fs.writeFileSync(filePath, html, 'utf8');

  // Generate hero background image via nano-banana-pro (Gemini image gen)
  const heroPath = path.join(dir, 'hero-bg.png');
  const destination = data.destination || 'a beautiful travel destination';

  // Derive season from travel dates for seasonal hero imagery
  const seasonDesc = (() => {
    const startDate = order.startDate || order.start_date || (data.days && data.days[0] && data.days[0].date);
    if (!startDate) return '';
    const d = new Date(startDate);
    if (isNaN(d.getTime())) return '';
    const month = d.getMonth(); // 0-indexed
    // Detect southern hemisphere by keywords (rough heuristic)
    const dest = destination.toLowerCase();
    const southern = /\b(australia|new zealand|argentina|chile|south africa|brazil|peru|bali|indonesia|patagonia|buenos aires|sydney|melbourne|cape town|queenstown|lima|santiago|rio)\b/.test(dest);
    const seasonMonth = southern ? (month + 6) % 12 : month;
    // Map to season + visual cues
    if (seasonMonth >= 2 && seasonMonth <= 4) {
      // Spring
      const cues = dest.includes('japan') || dest.includes('tokyo') || dest.includes('kyoto') || dest.includes('osaka')
        ? 'spring cherry blossom season, pink sakura petals floating in the air'
        : 'springtime, fresh green foliage, blooming flowers, clear skies';
      return cues;
    } else if (seasonMonth >= 5 && seasonMonth <= 7) {
      return 'summer, warm golden sunlight, lush green landscape, vibrant colors';
    } else if (seasonMonth >= 8 && seasonMonth <= 10) {
      return 'autumn, warm amber and red fall foliage, golden hour lighting';
    } else {
      return 'winter, cool blue tones, bare trees or snow-dusted landscape, cozy atmosphere';
    }
  })();

  const seasonClause = seasonDesc ? ` During ${seasonDesc}.` : '';
  const heroPrompt = `Anime-style illustrated landscape of ${destination}.${seasonClause} Wide cinematic composition, soft atmospheric lighting, muted watercolor palette, Studio Ghibli aesthetic. Scenic vista with natural landmarks characteristic of ${destination}. No people, no text, no UI elements. Wide horizontal composition, serene and inviting mood.`;
  const HERO_MAX_RETRIES = 3;
  const apiKey = execSync('security find-generic-password -s "nano-banana-pro" -w', { stdio: 'pipe' }).toString().trim();
  for (let attempt = 1; attempt <= HERO_MAX_RETRIES; attempt++) {
    try {
      execSync(
        `uv run /Users/psy/.openclaw/workspace/skills/nano-banana-pro/scripts/generate_image.py --prompt "${heroPrompt.replace(/"/g, '\\"')}" --filename "${heroPath}" --resolution 2K --api-key "${apiKey}"`,
        { cwd: REPO_ROOT, stdio: 'pipe', timeout: 120000 }
      );
      console.log(`Hero image generated (attempt ${attempt}):`, heroPath);
      break;
    } catch (err) {
      console.error(`⚠️ Hero gen attempt ${attempt}/${HERO_MAX_RETRIES} failed:`, err.message);
      if (attempt === HERO_MAX_RETRIES) {
        console.error('❌ Hero image generation failed after all retries — itinerary will render without background');
      } else {
        execSync('sleep 3');
      }
    }
  }

  // Git commit and push
  const gitOpts = { cwd: REPO_ROOT, stdio: 'pipe' };
  try {
    execSync(`git add "i/${slug}/"`, gitOpts);
    execSync(`git commit -m "Add itinerary: ${slug} (${data.destination || 'custom'})"`, gitOpts);
    execSync('git push', gitOpts);
  } catch (err) {
    console.error('Git push failed (itinerary still written locally):', err.message);
  }

  const url = `https://tabiji.ai/i/${slug}/`;

  // Poll the URL until Cloudflare Pages build is live (avoid 404 race condition)
  const MAX_POLL_SECONDS = 180;
  const POLL_INTERVAL_MS = 5000;
  const pollStart = Date.now();
  let urlLive = false;
  console.log(`Waiting for ${url} to go live...`);
  while ((Date.now() - pollStart) < MAX_POLL_SECONDS * 1000) {
    try {
      const status = execSync(`curl -s -o /dev/null -w "%{http_code}" "${url}"`, { stdio: 'pipe', timeout: 10000 }).toString().trim();
      if (status === '200') {
        urlLive = true;
        const elapsed = ((Date.now() - pollStart) / 1000).toFixed(1);
        console.log(`✅ URL is live after ${elapsed}s`);
        break;
      }
    } catch (_) {}
    execSync(`sleep ${POLL_INTERVAL_MS / 1000}`);
  }
  if (!urlLive) {
    throw new Error(`URL ${url} did not return 200 after ${MAX_POLL_SECONDS}s. Itinerary deployed but NOT emailed — verify manually and resend.`);
  }

  // Generate deploy token — this is the ONLY way send-email.sh will allow sending
  const crypto = require('crypto');
  const deployToken = crypto.randomBytes(32).toString('hex');
  const tokenFile = path.join(REPO_ROOT, `.deploy-token-${slug}`);
  fs.writeFileSync(tokenFile, JSON.stringify({
    slug,
    url,
    token: deployToken,
    verifiedAt: new Date().toISOString(),
    httpStatus: 200,
    pid: process.pid,
  }, null, 2));
  console.log(`🔑 Deploy token written: ${tokenFile}`);

  // Send email via Resend (hello@tabiji.ai) — NEVER use gog gmail send
  let emailSent = false;
  if (order.email) {
    const generateEmailText = require('./email-template');
    const emailBody = generateEmailText({
      customerName: order.customerName || order.name,
      destination: data.destination,
      url,
      duration: data.duration,
      highlights: data.highlights,
    });

    // Write body to temp file to avoid shell escaping issues with newlines/quotes
    const tmpFile = path.join(REPO_ROOT, '.tmp-email-body.txt');
    fs.writeFileSync(tmpFile, emailBody, 'utf8');

    const sendScript = path.join(__dirname, 'send-email.sh');
    const subject = `Your ${data.destination || ''} Itinerary is Ready!`.trim();
    try {
      const result = execSync(
        `bash "${sendScript}" --to "${order.email}" --subject "${subject}" --body-file "${tmpFile}" --deploy-token "${tokenFile}"`,
        { cwd: REPO_ROOT, stdio: 'pipe' }
      );
      console.log('Email sent:', result.toString());
      emailSent = true;
    } catch (err) {
      console.error('❌ EMAIL SEND FAILED:', err.message);
      if (err.stderr) console.error('stderr:', err.stderr.toString());
      console.error('⚠️ Itinerary is live at', url, '— send email manually via send-email.sh');
    } finally {
      try { fs.unlinkSync(tmpFile); } catch (_) {}
    }
  }

  // Mark order as fulfilled: update, move from pending.json → fulfilled.json
  try {
    const pending = JSON.parse(fs.readFileSync(PENDING_FILE, 'utf8'));
    const matchIdx = pending.findIndex(o => (o.id || o.orderId) === _orderId);
    if (matchIdx !== -1) {
      const match = pending[matchIdx];
      match.status = 'fulfilled';
      match.fulfilledAt = new Date().toISOString();
      match.slug = slug;
      match.itinerary_url = url;
      match.url = url;

      // Remove from pending array
      const remaining = pending.filter((_, i) => i !== matchIdx);

      // Append to fulfilled.json
      let fulfilled = [];
      try { fulfilled = JSON.parse(fs.readFileSync(FULFILLED_FILE, 'utf8')); } catch {}
      fulfilled.push(match);

      // Atomic writes — pending first, then fulfilled (order matters for crash safety)
      atomicWrite(PENDING_FILE, remaining);
      atomicWrite(FULFILLED_FILE, fulfilled);
      console.log(`✅ Order ${_orderId} moved from pending.json → fulfilled.json (slug: ${slug})`);
    } else {
      console.warn(`Order ${_orderId} not found in pending.json — could not update status`);
    }
  } catch (err) {
    console.error('Failed to move order to fulfilled.json:', err.message);
  }

  if (!emailSent && order.email) {
    console.error(`\n🚨 CRITICAL: Itinerary ${slug} deployed but email to ${order.email} FAILED. Send manually!\n`);
  }

  return { slug, url, filePath, emailSent };
}

module.exports = fulfillOrder;
