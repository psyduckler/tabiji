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

  // Git commit and push
  const gitOpts = { cwd: REPO_ROOT, stdio: 'pipe' };
  try {
    execSync(`git add "i/${slug}/index.html"`, gitOpts);
    execSync(`git commit -m "Add itinerary: ${slug} (${data.destination || 'custom'})"`, gitOpts);
    execSync('git push', gitOpts);
  } catch (err) {
    console.error('Git push failed (itinerary still written locally):', err.message);
  }

  const url = `https://tabiji.ai/i/${slug}/`;
  return { slug, url, filePath };
}

module.exports = fulfillOrder;
