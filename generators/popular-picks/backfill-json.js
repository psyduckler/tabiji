#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { writeText } = require('./utils');
const { buildSourceJson } = require('./extract-existing');
const { validateSource } = require('./validate-source');

function backfillOne(htmlFile, outputFile) {
  const html = fs.readFileSync(htmlFile, 'utf8');
  const slug = path.basename(path.dirname(htmlFile));
  const sourceJson = buildSourceJson(html, slug);
  const validation = validateSource(sourceJson);
  writeText(outputFile, `${JSON.stringify(sourceJson, null, 2)}\n`);
  return { slug, outputFile, validation };
}

function walkPopularPicks(rootDir) {
  const files = [];
  for (const entry of fs.readdirSync(rootDir, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const htmlFile = path.join(rootDir, entry.name, 'index.html');
    if (fs.existsSync(htmlFile)) files.push(htmlFile);
  }
  return files.sort();
}

if (require.main === module) {
  const repoRoot = process.argv[2];
  const slug = process.argv[3];
  const all = process.argv.includes('--all');
  if (!repoRoot || (!slug && !all)) {
    console.error('Usage: node generators/popular-picks/backfill-json.js <repo-root> <slug|--all>');
    process.exit(1);
  }

  const popularPicksRoot = path.join(repoRoot, 'popular-picks');
  const outputRoot = path.join(repoRoot, 'popular-picks-data');
  const targets = all
    ? walkPopularPicks(popularPicksRoot)
    : [path.join(popularPicksRoot, slug, 'index.html')];

  let ok = 0;
  let failed = 0;

  for (const htmlFile of targets) {
    if (!fs.existsSync(htmlFile)) {
      console.error(`ERROR missing HTML file: ${htmlFile}`);
      failed += 1;
      continue;
    }
    const out = path.join(outputRoot, `${path.basename(path.dirname(htmlFile))}.json`);
    const result = backfillOne(htmlFile, out);
    const errorCount = result.validation.errors.length;
    const warningCount = result.validation.warnings.length;
    if (errorCount) {
      console.error(`ERROR ${result.slug}: ${errorCount} validation error(s)`);
      result.validation.errors.forEach((msg) => console.error(`  - ${msg}`));
      failed += 1;
    } else {
      console.log(`OK ${result.slug}: wrote ${out} (${warningCount} warning(s))`);
      ok += 1;
    }
  }

  console.log(`Done. ok=${ok} failed=${failed}`);
  process.exit(failed ? 1 : 0);
}

module.exports = { backfillOne, walkPopularPicks };
