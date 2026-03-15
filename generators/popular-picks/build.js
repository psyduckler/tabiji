const path = require('path');
const { readJson, writeText } = require('./utils');
const { validateSource } = require('./validate-source');
const { renderPage } = require('./render-page');
const { updateIndexes } = require('./update-indexes');
const { validateOutput } = require('./validate-output');

function buildPage(repoRoot, jsonFile, outFile, options = {}) {
  const data = readJson(jsonFile);
  const validation = validateSource(data);
  const errors = validation.errors || [];
  const warnings = validation.warnings || [];
  if (errors.length) {
    throw new Error(`Source validation failed:\n${errors.join('\n')}`);
  }

  const html = renderPage(data);
  writeText(outFile, html);

  const outputValidation = validateOutput(html, data);
  if ((outputValidation.errors || []).length) {
    throw new Error(`Output validation failed:\n${outputValidation.errors.join('\n')}`);
  }

  if (options.updateIndexes) {
    updateIndexes(repoRoot, data);
  }

  return { data, validation, outputValidation, html };
}

if (require.main === module) {
  const repoRoot = process.argv[2];
  const jsonFile = process.argv[3];
  const outFile = process.argv[4] || path.join(repoRoot, 'tmp', 'popular-picks', `${path.basename(jsonFile, '.json')}.html`);
  const update = process.argv.includes('--update-indexes');
  if (!repoRoot || !jsonFile) {
    console.error('Usage: node generators/popular-picks/build.js <repo-root> <json-file> [out-file] [--update-indexes]');
    process.exit(1);
  }

  const { validation, outputValidation } = buildPage(repoRoot, jsonFile, outFile, { updateIndexes: update });
  for (const warning of (validation.warnings || [])) {
    console.warn(`WARN: ${warning}`);
  }
  for (const warning of (outputValidation.warnings || [])) {
    console.warn(`WARN: ${warning}`);
  }
  console.log(`Built ${outFile}`);
}

module.exports = { buildPage };
