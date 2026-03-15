#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function loadJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function isNonEmptyString(value) {
  return typeof value === 'string' && value.trim().length > 0;
}

function validateHub(data) {
  const errors = [];
  const warnings = [];

  for (const field of ['slug', 'pageType', 'status', 'seo', 'hero', 'sections', 'publishing']) {
    if (!(field in data)) errors.push(`Missing top-level field: ${field}`);
  }

  if (!/^[a-z0-9-]+$/.test(data.slug || '')) errors.push('slug must be lowercase kebab-case');
  if (data.pageType !== 'popular-picks-hub') errors.push('pageType must equal "popular-picks-hub"');

  const expectedOutputPath = `popular-picks/${data.slug}/index.html`;
  if (data?.publishing?.outputPath !== expectedOutputPath) {
    errors.push(`publishing.outputPath must equal ${expectedOutputPath}`);
  }

  if (!isNonEmptyString(data?.seo?.metaTitle)) errors.push('seo.metaTitle is required');
  if (!isNonEmptyString(data?.seo?.metaDescription)) errors.push('seo.metaDescription is required');
  if (!isNonEmptyString(data?.hero?.title)) errors.push('hero.title is required');
  if (!isNonEmptyString(data?.hero?.dek)) warnings.push('hero.dek is missing');

  if (!Array.isArray(data.sections) || data.sections.length < 1) {
    errors.push('At least 1 hub section is required');
  } else {
    const ids = new Set();
    data.sections.forEach((section, index) => {
      if (!isNonEmptyString(section.id)) errors.push(`Section #${index + 1} missing id`);
      if (!isNonEmptyString(section.title)) errors.push(`Section #${index + 1} missing title`);
      if (ids.has(section.id)) errors.push(`Duplicate section id: ${section.id}`);
      ids.add(section.id);
      if (!Array.isArray(section.cards) || section.cards.length < 1) {
        errors.push(`Section ${section.id || index + 1} must include at least 1 card`);
      } else {
        const cardSlugs = new Set();
        section.cards.forEach((card, cardIndex) => {
          for (const field of ['slug', 'href', 'title', 'description']) {
            if (!isNonEmptyString(card[field])) {
              errors.push(`Section ${section.id || index + 1} card #${cardIndex + 1} missing ${field}`);
            }
          }
          if (cardSlugs.has(card.slug)) warnings.push(`Duplicate card slug within section ${section.id}: ${card.slug}`);
          cardSlugs.add(card.slug);
          if (!Array.isArray(card.meta)) warnings.push(`Card ${card.slug} missing meta array`);
          if (!isNonEmptyString(card.image)) warnings.push(`Card ${card.slug} missing image`);
          if (!isNonEmptyString(card.badge)) warnings.push(`Card ${card.slug} missing badge`);
        });
      }
    });
  }

  if (Array.isArray(data.toc) && data.toc.length) {
    const sectionIds = new Set((data.sections || []).map((section) => section.id));
    for (const item of data.toc) {
      if (!sectionIds.has(item.id)) warnings.push(`TOC references unknown section id: ${item.id}`);
    }
  } else {
    warnings.push('toc is empty or missing');
  }

  return { errors, warnings };
}

if (require.main === module) {
  const filePath = process.argv[2];
  if (!filePath) {
    console.error('Usage: node validate-hub.js <hub.json>');
    process.exit(1);
  }
  const result = validateHub(loadJson(path.resolve(filePath)));
  result.warnings.forEach((warning) => console.warn(`WARN: ${warning}`));
  result.errors.forEach((error) => console.error(`ERROR: ${error}`));
  if (result.errors.length) process.exit(1);
  console.log(`OK: ${path.basename(filePath)} passed hub validation with ${result.warnings.length} warning(s)`);
}

module.exports = { validateHub, loadJson };
