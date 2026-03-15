#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { loadJson, validateSource } = require('./validate-source');
const { renderPage } = require('./render-page');

function buildPage(inputPath, outputPath) {
  const data = loadJson(path.resolve(inputPath));
  const result = validateSource(data);
  if (result.errors.length) {
    throw new Error(result.errors.join('\n'));
  }

  const html = renderPage(data);
  const finalOutput = path.resolve(outputPath || path.join('tmp', data.publishing.outputPath));
  fs.mkdirSync(path.dirname(finalOutput), { recursive: true });
  fs.writeFileSync(finalOutput, html);
  return { outputPath: finalOutput, warnings: result.warnings };
}

if (require.main === module) {
  const [inputPath, outputPath] = process.argv.slice(2);
  if (!inputPath) {
    console.error('Usage: node build-page.js <input.json> [output.html]');
    process.exit(1);
  }

  const result = buildPage(inputPath, outputPath);
  result.warnings.forEach((warning) => console.warn(`WARN: ${warning}`));
  console.log(`Built ${result.outputPath}`);
}

module.exports = { buildPage };
