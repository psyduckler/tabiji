const fs = require('fs');
const path = require('path');
const { readJson, writeText } = require('./utils');

function todayISO() {
  return new Date().toISOString().slice(0, 10);
}

function updateSitemap(repoRoot, data) {
  const sitemapPath = path.join(repoRoot, 'sitemap.xml');
  let xml = fs.readFileSync(sitemapPath, 'utf8');
  const pageUrl = `https://tabiji.ai/popular-picks/${data.slug}/`;

  // Skip if already present
  if (xml.includes(`<loc>${pageUrl}</loc>`)) {
    return false;
  }

  const entry = [
    '  <url>',
    `    <loc>${pageUrl}</loc>`,
    `    <lastmod>${todayISO()}</lastmod>`,
    '    <changefreq>monthly</changefreq>',
    '    <priority>0.6</priority>',
    '  </url>',
  ].join('\n');

  // Insert before closing </urlset>
  xml = xml.replace('</urlset>', `${entry}\n</urlset>`);
  fs.writeFileSync(sitemapPath, xml);
  return true;
}

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

  // Add to sitemap.xml if not already present
  const added = updateSitemap(repoRoot, data);
  if (added) {
    console.log(`Added ${data.slug} to sitemap.xml`);
  }
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

module.exports = { updateIndexes, updateSitemap, buildMetadataEntry };
