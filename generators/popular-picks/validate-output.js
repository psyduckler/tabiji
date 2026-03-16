#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function countMatches(html, regex) {
  return (html.match(regex) || []).length;
}

function validateOutput(html, sourceData) {
  const errors = [];
  const warnings = [];

  const requiredPatterns = [
    { label: '<title>', regex: /<title>.*?<\/title>/is },
    { label: 'meta description', regex: /<meta\s+name="description"/i },
    { label: 'canonical', regex: /<link\s+rel="canonical"/i },
    { label: 'hero H1', regex: /<h1>.*?<\/h1>/is },
    { label: 'FAQ schema', regex: /"@type":\s*"FAQPage"/i },
    { label: 'ItemList schema', regex: /"@type":\s*"ItemList"/i },
    { label: 'TouristTrip schema', regex: /"@type":\s*"TouristTrip"/i },
    { label: 'intro section', regex: /<section class="[^"]*intro-section[^"]*">\s*<p><strong>/i },
    { label: 'related recommendations', regex: /Related Recommendations/i }
  ];

  for (const item of requiredPatterns) {
    if (!item.regex.test(html)) errors.push(`Missing ${item.label}`);
  }

  const pickCount = Math.max(
    countMatches(html, /<article class="pick-card"/g),
    countMatches(html, /<section class="restaurant-section"/g)
  );
  if (pickCount < 3) errors.push('Rendered output must contain at least 3 rendered picks');

  const faqCount = countMatches(html, /<div class="faq-item">/g);
  if (faqCount < 3) warnings.push('Rendered output has fewer than 3 FAQ items');

  if (sourceData) {
    if (sourceData.picks && pickCount !== sourceData.picks.length) {
      errors.push(`rendered pick count mismatch: rendered ${pickCount}, expected ${sourceData.picks.length}`);
    }
    if (sourceData.faq && faqCount !== sourceData.faq.length) {
      errors.push(`faq-item count mismatch: rendered ${faqCount}, expected ${sourceData.faq.length}`);
    }
  }

  if (html.length > 250000) warnings.push('HTML output is unusually large');
  if (!/Generated from structured source data\./.test(html)) warnings.push('Footer marker missing');

  return { errors, warnings, stats: { pickCount, faqCount, htmlBytes: Buffer.byteLength(html) } };
}

if (require.main === module) {
  const filePath = process.argv[2];
  if (!filePath) {
    console.error('Usage: node validate-output.js <file.html>');
    process.exit(1);
  }

  const html = fs.readFileSync(path.resolve(filePath), 'utf8');
  const result = validateOutput(html);
  result.warnings.forEach((warning) => console.warn(`WARN: ${warning}`));
  result.errors.forEach((error) => console.error(`ERROR: ${error}`));
  if (result.errors.length) process.exit(1);
  console.log(`OK: ${path.basename(filePath)} passed output validation (${result.stats.pickCount} picks, ${result.stats.faqCount} FAQs, ${result.stats.htmlBytes} bytes)`);
}

module.exports = { validateOutput };
