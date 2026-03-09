/**
 * day-photos.js — Find and add real photos for each day of an itinerary.
 *
 * For each day: pick the most iconic attraction → SerpAPI Google Images search →
 * download top 5 → Gemini vision score → pick winner → optimize (800px, 80% JPEG) →
 * upload to R2 CDN → inject <img> into the HTML file.
 *
 * Usage (standalone):
 *   node day-photos.js <slug> <destination>
 *
 * Usage (as module):
 *   const addDayPhotos = require('./day-photos');
 *   const results = addDayPhotos(slug, itineraryData);
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');

const REPO_ROOT = path.resolve(__dirname, '..');
const R2_ACCOUNT = '9ce95ed3e1df4a7e1d2a401e116c3c6f';
const R2_BUCKET = 'tabiji-media';
const R2_PUBLIC = 'https://img.tabiji.ai';
const MAX_CANDIDATES = 5;
const IMG_WIDTH = 800;
const IMG_QUALITY = 80;

/**
 * Pick the most iconic attraction from a day's data using Gemini.
 */
function pickBestAttraction(day, destination) {
  // Extract attraction names from time blocks
  const attractions = [];
  if (day.timeBlocks) {
    for (const block of day.timeBlocks) {
      if (block.spots) {
        for (const spot of block.spots) {
          if (spot.name) attractions.push(spot.name);
        }
      }
    }
  }

  if (attractions.length === 0) {
    // Fall back to day title
    return day.title || null;
  }

  if (attractions.length === 1) {
    return attractions[0];
  }

  // Use Gemini to pick the most iconic/photogenic one
  const apiKey = execSync('security find-generic-password -s "google-api-key" -w', { stdio: 'pipe' }).toString().trim();
  const prompt = `You are helping select the most iconic and photogenic attraction for a travel photo. The destination is ${destination}. From this list of attractions for Day ${day.num}, pick THE ONE that would make the best, most recognizable photo. Reply with ONLY the attraction name, nothing else.\n\nAttractions:\n${attractions.map((a, i) => `${i + 1}. ${a}`).join('\n')}`;

  try {
    const result = execSync(
      `curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}" -H "Content-Type: application/json" -d '${JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: { temperature: 0.1, maxOutputTokens: 100 }
      }).replace(/'/g, "'\\''")}'`,
      { stdio: 'pipe', timeout: 30000 }
    ).toString();
    const parsed = JSON.parse(result);
    const text = parsed?.candidates?.[0]?.content?.parts?.[0]?.text?.trim();
    if (text) {
      // Find the closest match from the original list
      const lower = text.toLowerCase();
      const match = attractions.find(a => lower.includes(a.toLowerCase()) || a.toLowerCase().includes(lower));
      return match || text;
    }
  } catch (err) {
    console.error(`  ⚠️ Gemini pick failed for day ${day.num}, using first attraction:`, err.message);
  }

  return attractions[0];
}

/**
 * Search SerpAPI Google Images for an attraction.
 * Returns array of { url, title, width, height }.
 */
function searchImages(query) {
  const serpKey = execSync('security find-generic-password -s "serpapi-key" -w', { stdio: 'pipe' }).toString().trim();
  const params = new URLSearchParams({
    engine: 'google_images',
    q: query,
    api_key: serpKey,
    num: '10',
    ijn: '0',
    tbs: 'isz:m', // medium+ size
  });

  try {
    const result = execSync(
      `curl -s "https://serpapi.com/search.json?${params.toString()}"`,
      { stdio: 'pipe', timeout: 30000 }
    ).toString();
    const data = JSON.parse(result);
    const images = (data.images_results || []).slice(0, MAX_CANDIDATES);
    return images.map(img => ({
      url: img.original,
      thumbnail: img.thumbnail,
      title: img.title || '',
      width: img.original_width || 0,
      height: img.original_height || 0,
    }));
  } catch (err) {
    console.error(`  ⚠️ SerpAPI search failed for "${query}":`, err.message);
    return [];
  }
}

/**
 * Download an image to a local path. Returns true if successful and > 10KB.
 */
function downloadImage(url, destPath) {
  try {
    execSync(
      `curl -sL -o "${destPath}" --max-time 15 "${url}"`,
      { stdio: 'pipe', timeout: 20000 }
    );
    const stat = fs.statSync(destPath);
    if (stat.size < 10000) {
      // Too small — likely broken
      try { fs.unlinkSync(destPath); } catch (_) {}
      return false;
    }
    return true;
  } catch (err) {
    try { fs.unlinkSync(destPath); } catch (_) {}
    return false;
  }
}

/**
 * Vision-score downloaded photos using Gemini.
 * Returns the index (0-based) of the best photo, or -1 if all fail.
 */
function visionScore(photoPaths, attractionName, destination) {
  const apiKey = execSync('security find-generic-password -s "google-api-key" -w', { stdio: 'pipe' }).toString().trim();

  // Build parts array with images
  const parts = [];
  const validIndices = [];

  for (let i = 0; i < photoPaths.length; i++) {
    if (!fs.existsSync(photoPaths[i])) continue;
    try {
      const imgData = fs.readFileSync(photoPaths[i]);
      const base64 = imgData.toString('base64');
      // Detect mime type from magic bytes
      let mimeType = 'image/jpeg';
      if (imgData[0] === 0x89 && imgData[1] === 0x50) mimeType = 'image/png';
      else if (imgData[0] === 0x47 && imgData[1] === 0x49) mimeType = 'image/gif';
      else if (imgData[0] === 0x52 && imgData[1] === 0x49) mimeType = 'image/webp';

      parts.push({ inlineData: { mimeType, data: base64 } });
      parts.push({ text: `Photo ${i + 1}` });
      validIndices.push(i);
    } catch (_) {
      continue;
    }
  }

  if (validIndices.length === 0) return -1;
  if (validIndices.length === 1) return validIndices[0];

  parts.push({
    text: `Score each photo 1-10 on how well it represents "${attractionName}" in ${destination}. Consider: visual quality, composition, clarity, showing what makes this place special and recognizable. For each photo give a brief assessment and score. Then on the last line write ONLY: BEST: N (where N is the photo number).`
  });

  const payload = JSON.stringify({
    contents: [{ parts }],
    generationConfig: { temperature: 0.1, maxOutputTokens: 500 }
  });

  // Write payload to temp file to avoid shell escaping issues
  const tmpPayload = path.join(os.tmpdir(), `vision-score-${Date.now()}.json`);
  fs.writeFileSync(tmpPayload, payload);

  try {
    const result = execSync(
      `curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}" -H "Content-Type: application/json" -d @"${tmpPayload}"`,
      { stdio: 'pipe', timeout: 60000 }
    ).toString();
    fs.unlinkSync(tmpPayload);

    const parsed = JSON.parse(result);
    const text = parsed?.candidates?.[0]?.content?.parts?.[0]?.text || '';
    console.log(`  Vision scores:\n${text.split('\n').map(l => `    ${l}`).join('\n')}`);

    // Extract BEST: N
    const match = text.match(/BEST:\s*(\d+)/i);
    if (match) {
      const photoNum = parseInt(match[1], 10);
      // photoNum is 1-indexed, map back to original index
      if (photoNum >= 1 && photoNum <= validIndices.length) {
        return validIndices[photoNum - 1];
      }
    }

    // Fallback: return first valid photo
    return validIndices[0];
  } catch (err) {
    console.error(`  ⚠️ Vision scoring failed:`, err.message);
    try { fs.unlinkSync(tmpPayload); } catch (_) {}
    return validIndices[0];
  }
}

/**
 * Optimize an image: resize to 800px wide, 80% JPEG quality.
 */
function optimizeImage(srcPath, destPath) {
  try {
    // Copy first, then resize in place
    fs.copyFileSync(srcPath, destPath);
    execSync(`sips -Z ${IMG_WIDTH} --setProperty format jpeg --setProperty formatOptions ${IMG_QUALITY} "${destPath}"`, {
      stdio: 'pipe', timeout: 15000
    });
    return true;
  } catch (err) {
    console.error(`  ⚠️ Image optimization failed:`, err.message);
    // Fallback: just copy as-is
    try { fs.copyFileSync(srcPath, destPath); return true; } catch (_) {}
    return false;
  }
}

/**
 * Upload a file to Cloudflare R2 and return the public URL.
 */
function uploadToR2(localPath, r2Key) {
  const r2Token = execSync('security find-generic-password -s "cloudflare-pages-token" -w', { stdio: 'pipe' }).toString().trim();
  try {
    execSync(
      `curl -s -X PUT -H "Authorization: Bearer ${r2Token}" -H "Content-Type: image/jpeg" --data-binary @"${localPath}" "https://api.cloudflare.com/client/v4/accounts/${R2_ACCOUNT}/r2/buckets/${R2_BUCKET}/objects/${r2Key}"`,
      { stdio: 'pipe', timeout: 60000 }
    );
    return `${R2_PUBLIC}/${r2Key}`;
  } catch (err) {
    console.error(`  ⚠️ R2 upload failed for ${r2Key}:`, err.message);
    return null;
  }
}

/**
 * Inject an <img> tag into the HTML file after the <h2> for a specific day.
 * Looks for: </h2> inside the day's div, inserts img right after.
 */
function injectDayPhoto(htmlPath, dayNum, imgUrl, altText) {
  let html = fs.readFileSync(htmlPath, 'utf8');

  // Pattern: find the <h2>...</h2> inside the day's section
  // The day section starts with <div class="day" id="dayN">
  const dayDivRegex = new RegExp(
    `(<div class="day" id="day${dayNum}">\\s*<div class="day-header">[\\s\\S]*?</div>\\s*<h2>[\\s\\S]*?</h2>)`,
    'm'
  );

  const match = html.match(dayDivRegex);
  if (!match) {
    console.error(`  ⚠️ Could not find <h2> for day ${dayNum} in HTML`);
    return false;
  }

  const imgTag = `\n        <img src="${imgUrl}" alt="${altText.replace(/"/g, '&quot;')}" style="width:100%;border-radius:12px;margin:1rem 0;" loading="lazy">`;

  // Check if an img already exists right after the h2
  const afterH2 = html.substring(match.index + match[0].length, match.index + match[0].length + 200);
  if (afterH2.trimStart().startsWith('<img')) {
    console.log(`  ℹ️ Day ${dayNum} already has a photo, skipping injection`);
    return false;
  }

  html = html.substring(0, match.index + match[0].length) + imgTag + html.substring(match.index + match[0].length);
  fs.writeFileSync(htmlPath, html, 'utf8');
  return true;
}

/**
 * Main: add day photos to an itinerary.
 *
 * @param {string} slug - Itinerary slug
 * @param {Object} itineraryData - Full itinerary data with days array
 * @returns {Object} { added: number, skipped: number, details: [] }
 */
function addDayPhotos(slug, itineraryData, opts = {}) {
  const fastMode = opts.fast !== false; // Default: fast mode ON (skip vision scoring)
  const destination = itineraryData.destination || 'travel destination';
  const days = itineraryData.days || [];
  const htmlPath = path.join(REPO_ROOT, 'i', slug, 'index.html');
  const tmpDir = path.join(os.tmpdir(), `tabiji-day-photos-${slug}`);

  if (!fs.existsSync(htmlPath)) {
    console.error(`❌ HTML file not found: ${htmlPath}`);
    return { added: 0, skipped: days.length, details: [] };
  }

  fs.mkdirSync(tmpDir, { recursive: true });

  const results = { added: 0, skipped: 0, details: [] };

  // Fallback: if days data is sparse, extract attractions from the HTML
  const html = fs.readFileSync(htmlPath, 'utf8');
  function extractAttractionsFromHTML(dayNum) {
    // Match h3 headings within the day section
    const dayRegex = new RegExp(`id="day-${dayNum}"[\\s\\S]*?(?=id="day-${dayNum + 1}"|<footer|$)`);
    const section = html.match(dayRegex);
    if (!section) return [];
    const h3s = section[0].match(/<h3>(.*?)<\/h3>/g);
    if (!h3s) return [];
    return h3s.map(h => h.replace(/<[^>]+>/g, '').trim()).filter(h => h && !h.includes('undefined'));
  }

  for (const day of days) {
    const dayNum = day.num;
    console.log(`\n📷 Day ${dayNum}: Finding photo...`);

    // 1. Pick best attraction (fall back to HTML extraction if data is sparse)
    let attraction = pickBestAttraction(day, destination);
    if (!attraction) {
      const htmlAttractions = extractAttractionsFromHTML(dayNum);
      if (htmlAttractions.length > 0) {
        attraction = htmlAttractions[0]; // Use first h3 from the day section
        console.log(`  📄 Extracted from HTML: ${attraction}`);
      }
    }
    if (!attraction) {
      console.log(`  ⏭ No attractions found for day ${dayNum}, skipping`);
      results.skipped++;
      results.details.push({ day: dayNum, status: 'skipped', reason: 'no attractions' });
      continue;
    }
    console.log(`  🎯 Best attraction: ${attraction}`);

    // 2. Search for images
    const query = `${attraction} ${destination}`;
    const images = searchImages(query);
    if (images.length === 0) {
      console.log(`  ⏭ No images found for "${query}", skipping`);
      results.skipped++;
      results.details.push({ day: dayNum, attraction, status: 'skipped', reason: 'no search results' });
      continue;
    }
    console.log(`  🔍 Found ${images.length} candidate images`);

    // 3. Download candidates (fast mode: top 2 only, skip vision scoring)
    const maxDownloads = fastMode ? 2 : images.length;
    const downloaded = [];
    for (let i = 0; i < Math.min(maxDownloads, images.length); i++) {
      const dlPath = path.join(tmpDir, `day${dayNum}-candidate-${i}.jpg`);
      if (downloadImage(images[i].url, dlPath)) {
        downloaded.push({ index: i, path: dlPath, url: images[i].url });
        if (fastMode) break; // In fast mode, use first successful download
      }
    }
    if (downloaded.length === 0) {
      console.log(`  ⏭ All downloads failed for day ${dayNum}, skipping`);
      results.skipped++;
      results.details.push({ day: dayNum, attraction, status: 'skipped', reason: 'downloads failed' });
      continue;
    }
    console.log(`  ⬇️ Downloaded ${downloaded.length} photos`);

    // 4. Vision score (skipped in fast mode — SerpAPI ranking is good enough)
    let winner;
    if (fastMode) {
      winner = downloaded[0];
      console.log(`  ⚡ Fast mode: using top SerpAPI result`);
    } else {
      const bestIdx = visionScore(downloaded.map(d => d.path), attraction, destination);
      if (bestIdx === -1) {
        console.log(`  ⏭ Vision scoring failed for day ${dayNum}, skipping`);
        results.skipped++;
        results.details.push({ day: dayNum, attraction, status: 'skipped', reason: 'vision scoring failed' });
        continue;
      }
      winner = downloaded.find(d => d.index === bestIdx) || downloaded[0];
      console.log(`  🏆 Winner: candidate ${bestIdx + 1}`);
    }

    // 5. Optimize
    const optimizedPath = path.join(tmpDir, `day${dayNum}-final.jpg`);
    if (!optimizeImage(winner.path, optimizedPath)) {
      console.log(`  ⏭ Optimization failed for day ${dayNum}, skipping`);
      results.skipped++;
      results.details.push({ day: dayNum, attraction, status: 'skipped', reason: 'optimization failed' });
      continue;
    }

    // 6. Upload to R2
    const r2Key = `i/${slug}/day-${dayNum}.jpg`;
    const publicUrl = uploadToR2(optimizedPath, r2Key);
    if (!publicUrl) {
      console.log(`  ⏭ R2 upload failed for day ${dayNum}, skipping`);
      results.skipped++;
      results.details.push({ day: dayNum, attraction, status: 'skipped', reason: 'R2 upload failed' });
      continue;
    }
    console.log(`  ☁️ Uploaded: ${publicUrl}`);

    // 7. Inject into HTML
    const altText = `${attraction}, ${destination}`;
    const injected = injectDayPhoto(htmlPath, dayNum, publicUrl, altText);
    if (injected) {
      console.log(`  ✅ Day ${dayNum}: ${attraction} — photo added`);
      results.added++;
      results.details.push({ day: dayNum, attraction, status: 'added', url: publicUrl });
    } else {
      console.log(`  ℹ️ Day ${dayNum}: photo already present or injection failed`);
      results.skipped++;
      results.details.push({ day: dayNum, attraction, status: 'skipped', reason: 'already has photo or injection failed' });
    }

    // Clean up downloaded candidates (keep final)
    for (const d of downloaded) {
      try { fs.unlinkSync(d.path); } catch (_) {}
    }
    try { fs.unlinkSync(optimizedPath); } catch (_) {}
  }

  // Clean up tmp dir
  try { fs.rmSync(tmpDir, { recursive: true }); } catch (_) {}

  console.log(`\n📷 Day photos complete: ${results.added} added, ${results.skipped} skipped`);
  return results;
}

// CLI mode
if (require.main === module) {
  const slug = process.argv[2];
  const destination = process.argv[3];
  if (!slug || !destination) {
    console.error('Usage: node day-photos.js <slug> <destination>');
    process.exit(1);
  }
  // Build minimal itinerary data from the HTML by reading the day sections
  const htmlPath = path.join(REPO_ROOT, 'i', slug, 'index.html');
  if (!fs.existsSync(htmlPath)) {
    console.error(`HTML not found: ${htmlPath}`);
    process.exit(1);
  }
  const html = fs.readFileSync(htmlPath, 'utf8');
  // Extract day titles and neighborhoods from the HTML
  const dayRegex = /<div class="day" id="day(\d+)">[\s\S]*?<span class="day-neighborhoods">(.*?)<\/span>[\s\S]*?<h2>(.*?)<\/h2>/g;
  const days = [];
  let m;
  while ((m = dayRegex.exec(html)) !== null) {
    const num = parseInt(m[1], 10);
    const neighborhoods = m[2].replace(/&amp;/g, '&');
    const title = m[3].replace(/&amp;/g, '&');
    // Build spot names from neighborhoods
    const spots = neighborhoods.split('·').map(n => n.trim()).filter(Boolean);
    days.push({
      num,
      title,
      neighborhoods,
      timeBlocks: [{ spots: spots.map(name => ({ name })) }],
    });
  }
  if (days.length === 0) {
    console.error('No days found in HTML');
    process.exit(1);
  }
  const results = addDayPhotos(slug, { destination, days });
  console.log(JSON.stringify(results, null, 2));
}

module.exports = addDayPhotos;
