#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function count(text, pattern) {
  return (text.match(pattern) || []).length;
}

function reportLeaf(liveHtml, genHtml) {
  return {
    family: 'leaf',
    liveBytes: Buffer.byteLength(liveHtml),
    generatedBytes: Buffer.byteLength(genHtml),
    livePicks: Math.max(count(liveHtml, /class="restaurant-section"/g), count(liveHtml, /class="pick-card"/g)),
    generatedPicks: Math.max(count(genHtml, /class="restaurant-section"/g), count(genHtml, /class="pick-card"/g)),
    liveFaq: count(liveHtml, /"@type":\s*"Question"/g),
    generatedFaq: count(genHtml, /"@type":\s*"Question"/g),
  };
}

function reportHub(liveHtml, genHtml) {
  return {
    family: 'hub',
    liveBytes: Buffer.byteLength(liveHtml),
    generatedBytes: Buffer.byteLength(genHtml),
    liveSections: count(liveHtml, /class="city-section"/g),
    generatedSections: count(genHtml, /class="city-section"/g),
    liveCards: count(liveHtml, /class="pick-card"/g),
    generatedCards: count(genHtml, /class="pick-card"/g),
    liveTocSidebar: count(liveHtml, /class="toc-sidebar"/g),
    generatedTocSidebar: count(genHtml, /class="toc-sidebar"/g),
    liveTocMobile: count(liveHtml, /class="toc-mobile-sticky"/g),
    generatedTocMobile: count(genHtml, /class="toc-mobile-sticky"/g),
  };
}

if (require.main === module) {
  const family = process.argv[2];
  const liveFile = process.argv[3];
  const genFile = process.argv[4];
  if (!family || !liveFile || !genFile) {
    console.error('Usage: node parity-report.js <leaf|hub> <live.html> <generated.html>');
    process.exit(1);
  }
  const liveHtml = fs.readFileSync(path.resolve(liveFile), 'utf8');
  const genHtml = fs.readFileSync(path.resolve(genFile), 'utf8');
  const report = family === 'hub' ? reportHub(liveHtml, genHtml) : reportLeaf(liveHtml, genHtml);
  console.log(JSON.stringify(report, null, 2));
}

module.exports = { reportLeaf, reportHub };
