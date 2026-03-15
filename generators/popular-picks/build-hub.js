#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { renderHubPage } = require('./render-hub');
const { validateHub, loadJson } = require('./validate-hub');

function writeText(filePath, content) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, content);
}

function validateHubOutput(html, sourceData) {
  const errors = [];
  const warnings = [];
  const sectionCount = (html.match(/class="city-section"/g) || []).length;
  const cardCount = (html.match(/class="pick-card"/g) || []).length;

  if (!/<title>.*<\/title>/i.test(html)) errors.push('Missing <title>');
  if (!/<meta name="description"/i.test(html)) errors.push('Missing meta description');
  if (!/<link rel="canonical"/i.test(html)) errors.push('Missing canonical');
  if (!/class="toc-sidebar"/i.test(html)) errors.push('Missing TOC sidebar');
  if (!/class="toc-mobile-sticky"/i.test(html)) errors.push('Missing mobile TOC');
  if (!/class="city-section"/i.test(html)) errors.push('Missing city-section markup');
  if (!/class="pick-card"/i.test(html)) errors.push('Missing pick-card markup');

  const expectedSections = (sourceData.sections || []).length;
  const expectedCards = (sourceData.sections || []).reduce((sum, section) => sum + (section.cards || []).length, 0);
  if (sectionCount !== expectedSections) errors.push(`city-section count mismatch: rendered ${sectionCount}, expected ${expectedSections}`);
  if (cardCount !== expectedCards) errors.push(`pick-card count mismatch: rendered ${cardCount}, expected ${expectedCards}`);
  if (html.length > 250000) warnings.push('Hub HTML output is unusually large');

  return { errors, warnings, stats: { sectionCount, cardCount, htmlBytes: Buffer.byteLength(html) } };
}

function buildHub(repoRoot, jsonFile, outFile) {
  const data = loadJson(jsonFile);
  const validation = validateHub(data);
  if (validation.errors.length) {
    throw new Error(`Hub source validation failed:\n${validation.errors.join('\n')}`);
  }
  const html = renderHubPage(data);
  writeText(outFile, html);
  const outputValidation = validateHubOutput(html, data);
  if (outputValidation.errors.length) {
    throw new Error(`Hub output validation failed:\n${outputValidation.errors.join('\n')}`);
  }
  return { data, validation, outputValidation, html };
}

if (require.main === module) {
  const repoRoot = process.argv[2];
  const jsonFile = process.argv[3];
  const outFile = process.argv[4] || path.join(repoRoot, 'tmp', 'popular-picks-hub', `${path.basename(jsonFile, '.json')}.html`);
  if (!repoRoot || !jsonFile) {
    console.error('Usage: node build-hub.js <repo-root> <hub-json-file> [out-file]');
    process.exit(1);
  }
  const { validation, outputValidation } = buildHub(repoRoot, jsonFile, outFile);
  validation.warnings.forEach((warning) => console.warn(`WARN: ${warning}`));
  outputValidation.warnings.forEach((warning) => console.warn(`WARN: ${warning}`));
  console.log(`Built hub ${outFile}`);
}

module.exports = { buildHub, validateHubOutput };
