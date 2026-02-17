const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const generateSlug = require('./generate-slug');
const generateItineraryHTML = require('./generate-itinerary-html');

const REPO_ROOT = path.resolve(__dirname, '..');

/**
 * Fulfills an order by generating an HTML itinerary and deploying it.
 * @param {Object} order - The order object from pending.json
 * @param {Object} itineraryData - Structured itinerary data (without slug)
 * @returns {Object} { slug, url, filePath }
 */
function fulfillOrder(order, itineraryData) {
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
  const heroPrompt = `Anime-style illustrated landscape of ${destination}.${seasonClause} Wide cinematic composition, soft atmospheric lighting, muted watercolor palette, Studio Ghibli aesthetic. Scenic vista with natural landmarks characteristic of ${destination}. No people, no text, no UI elements. Horizontal 16:9 aspect ratio, serene and inviting mood.`;
  try {
    const apiKey = execSync('security find-generic-password -s "nano-banana-pro" -w', { stdio: 'pipe' }).toString().trim();
    execSync(
      `uv run /Users/psy/.openclaw/workspace/skills/nano-banana-pro/scripts/generate_image.py --prompt "${heroPrompt.replace(/"/g, '\\"')}" --filename "${heroPath}" --resolution 2K --api-key "${apiKey}"`,
      { cwd: REPO_ROOT, stdio: 'pipe', timeout: 120000 }
    );
    console.log('Hero image generated:', heroPath);
  } catch (err) {
    console.error('⚠️ Hero image generation failed (itinerary will render without background):', err.message);
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
        `bash "${sendScript}" --to "${order.email}" --subject "${subject}" --body-file "${tmpFile}"`,
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

  // Mark order as fulfilled in pending.json
  try {
    const pendingFile = path.join(REPO_ROOT, 'orders', 'pending.json');
    const pending = JSON.parse(fs.readFileSync(pendingFile, 'utf8'));
    const match = pending.find(o => o.id === order.id || o.orderId === order.orderId);
    if (match) {
      match.status = 'fulfilled';
      match.fulfilledAt = new Date().toISOString();
      match.slug = slug;
      match.url = url;
      fs.writeFileSync(pendingFile, JSON.stringify(pending, null, 2));
      console.log(`Order ${order.id || order.orderId} marked fulfilled in pending.json`);
    } else {
      console.warn(`Order ${order.id || order.orderId} not found in pending.json — could not update status`);
    }
  } catch (err) {
    console.error('Failed to update pending.json status:', err.message);
  }

  if (!emailSent && order.email) {
    console.error(`\n🚨 CRITICAL: Itinerary ${slug} deployed but email to ${order.email} FAILED. Send manually!\n`);
  }

  return { slug, url, filePath, emailSent };
}

module.exports = fulfillOrder;
