const fs = require('fs');
const path = require('path');
const { readJson, writeText } = require('./utils');

function buildMetadataEntry(data) {
  return {
    slug: data.slug,
    title: data.seo.title,
    description: data.seo.metaDescription,
    heroImage: data.seo.heroImage || null,
    badge: data.hero.badge,
    metaSpans: data.hero.metaSpans.map((value) => `<span>${value}</span>`),
    city: data.taxonomy.city,
    category: data.taxonomy.category,
  };
}

function updateIndexes(repoRoot, data) {
  const metadataPath = path.join(repoRoot, 'popular-picks', 'picks-metadata.json');
  const metadata = readJson(metadataPath);
  metadata[data.slug] = buildMetadataEntry(data);
  const ordered = Object.fromEntries(Object.entries(metadata).sort(([a], [b]) => a.localeCompare(b)));
  writeText(metadataPath, `${JSON.stringify(ordered, null, 2)}\n`);
}

if (require.main === module) {
  const repoRoot = process.argv[2];
  const jsonFile = process.argv[3];
  if (!repoRoot || !jsonFile) {
    console.error('Usage: node generators/popular-picks/update-indexes.js <repo-root> <json-file>');
    process.exit(1);
  }
  const data = readJson(jsonFile);
  updateIndexes(repoRoot, data);
}

module.exports = { updateIndexes, buildMetadataEntry };
