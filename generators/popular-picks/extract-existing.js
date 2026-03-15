const fs = require('fs');
const path = require('path');
const { writeText } = require('./utils');

function matchOne(html, regex) {
  const match = html.match(regex);
  return match ? match[1].trim() : null;
}

function extractJsonLdBlocks(html) {
  const blocks = [];
  const regex = /<script type="application\/ld\+json">\s*([\s\S]*?)\s*<\/script>/g;
  let match;
  while ((match = regex.exec(html))) {
    try {
      blocks.push(JSON.parse(match[1]));
    } catch {
      blocks.push({ parseError: true, raw: match[1].slice(0, 200) });
    }
  }
  return blocks;
}

function extractExisting(html, slug) {
  const title = matchOne(html, /<title>(.*?)<\/title>/i);
  const description = matchOne(html, /<meta name="description" content="(.*?)">/i);
  const canonical = matchOne(html, /<link rel="canonical" href="(.*?)">/i);
  const h1 = matchOne(html, /<h1[^>]*>(.*?)<\/h1>/i);
  const jsonLd = extractJsonLdBlocks(html);

  return {
    slug,
    extractedFromExistingHtml: true,
    title,
    description,
    canonical,
    h1,
    jsonLdTypes: jsonLd.map((item) => item['@type'] || 'unknown'),
    jsonLd,
    notes: [
      'This extractor is intentionally partial.',
      'Use it for backfill/bootstrap, not as a substitute for editorial review.',
      'Designed to help with the 36 missing API JSON backfills from existing HTML.',
    ],
  };
}

if (require.main === module) {
  const input = process.argv[2];
  const output = process.argv[3];
  if (!input || !output) {
    console.error('Usage: node generators/popular-picks/extract-existing.js <html-file> <output-json>');
    process.exit(1);
  }
  const html = fs.readFileSync(input, 'utf8');
  const slug = path.basename(path.dirname(input));
  const extracted = extractExisting(html, slug);
  writeText(output, `${JSON.stringify(extracted, null, 2)}\n`);
  console.log(`Extracted ${slug} -> ${output}`);
}

module.exports = { extractExisting };
