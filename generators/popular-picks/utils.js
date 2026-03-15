const fs = require('fs');
const path = require('path');

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function writeText(filePath, content) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, content);
}

function escapeHtml(value = '') {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function slugToPath(slug) {
  return `popular-picks/${slug}/index.html`;
}

function canonicalUrl(canonicalPath) {
  return `https://tabiji.ai${canonicalPath}`;
}

function isValidUrl(value) {
  try {
    new URL(value);
    return true;
  } catch {
    return false;
  }
}

function formatJsonLd(value) {
  return JSON.stringify(value, null, 2);
}

function toPlainText(value = '') {
  return String(value).replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
}

module.exports = {
  readJson,
  writeText,
  escapeHtml,
  slugToPath,
  canonicalUrl,
  isValidUrl,
  formatJsonLd,
  toPlainText,
};
