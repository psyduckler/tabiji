#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function loadJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function isNonEmptyString(value) {
  return typeof value === 'string' && value.trim().length > 0;
}

function isValidUrl(value) {
  if (!isNonEmptyString(value)) return false;
  try {
    new URL(value.startsWith('/') ? `https://tabiji.ai${value}` : value);
    return true;
  } catch {
    return false;
  }
}

function isNonFoodVertical(vertical = '') {
  return ['activities', 'nature-outdoors', 'shopping', 'lodging', 'mixed', 'destination-overview'].includes(vertical);
}

function validateSource(data, options = {}) {
  const mode = options.mode || 'publish';
  const backfillMode = mode === 'backfill';
  const errors = [];
  const warnings = [];

  const requiredTopLevel = [
    'slug', 'pageType', 'status', 'taxonomy', 'seo', 'hero', 'intro', 'summary',
    'picks', 'faq', 'related', 'verification', 'publishing'
  ];

  for (const key of requiredTopLevel) {
    if (!(key in data)) errors.push(`Missing top-level field: ${key}`);
  }

  if (!/^[a-z0-9-]+$/.test(data.slug || '')) {
    errors.push('slug must be lowercase kebab-case');
  }

  if (data.pageType !== 'popular-picks') {
    errors.push('pageType must equal "popular-picks"');
  }

  const expectedOutputPath = `popular-picks/${data.slug}/index.html`;
  if (data?.publishing?.outputPath !== expectedOutputPath) {
    errors.push(`publishing.outputPath must equal ${expectedOutputPath}`);
  }

  if (data?.summary?.totalOptions !== data?.picks?.length) {
    errors.push('summary.totalOptions must equal picks.length');
  }

  if (!isNonEmptyString(data?.intro?.answerFirst)) {
    errors.push('intro.answerFirst is required');
  }

  if (!Array.isArray(data?.intro?.body) || data.intro.body.length < 1) {
    errors.push('intro.body must contain at least 1 paragraph');
  }

  if (!Array.isArray(data?.picks) || data.picks.length < 1) {
    errors.push('At least 1 pick is required');
  } else if (data.picks.length < 3) {
    (backfillMode ? warnings : errors).push('At least 3 picks are recommended/required for publish-ready pages');
  }

  if (!Array.isArray(data?.faq) || data.faq.length < 1) {
    warnings.push('At least 1 FAQ item is required');
  } else if (data.faq.length < 3) {
    warnings.push('At least 3 FAQ items are recommended/required for publish-ready pages');
  }

  if (!/^\d{4}-\d{2}$/.test(data?.verification?.lastVerified || '')) {
    errors.push('verification.lastVerified must be YYYY-MM');
  }

  const nonFood = isNonFoodVertical(data?.taxonomy?.vertical || '');
  const seenRanks = new Set();
  const seenNames = new Set();
  (data.picks || []).forEach((pick, index) => {
    const expectedRank = index + 1;
    if (pick.rank !== expectedRank) {
      errors.push(`Pick ${pick.name || expectedRank} has rank ${pick.rank}; expected ${expectedRank}`);
    }
    if (seenRanks.has(pick.rank)) {
      errors.push(`Duplicate pick rank: ${pick.rank}`);
    }
    seenRanks.add(pick.rank);

    if (seenNames.has(pick.name)) {
      warnings.push(`Duplicate pick name: ${pick.name}`);
    }
    seenNames.add(pick.name);

    for (const field of ['name', 'placeType', 'whyItMadeTheList', 'whatToOrder', 'insiderTip']) {
      if (!isNonEmptyString(pick[field])) {
        errors.push(`Pick #${expectedRank} missing required field: ${field}`);
      }
    }

    if (!isNonEmptyString(pick.priceRangeLocal) && !isNonEmptyString(pick.priceRangeUSD)) {
      warnings.push(`Pick #${expectedRank} is missing priceRangeLocal/priceRangeUSD`);
    }

    if (pick.googleRating != null && (typeof pick.googleRating !== 'number' || pick.googleRating < 0 || pick.googleRating > 5)) {
      errors.push(`Pick #${expectedRank} has invalid googleRating`);
    }

    if (pick.reviewCount != null && (!Number.isInteger(pick.reviewCount) || pick.reviewCount < 0)) {
      errors.push(`Pick #${expectedRank} has invalid reviewCount`);
    }

    for (const coordField of ['lat', 'lng']) {
      if (pick[coordField] != null && (typeof pick[coordField] !== 'number' || !Number.isFinite(pick[coordField]))) {
        errors.push(`Pick #${expectedRank} has invalid ${coordField}`);
      }
    }

    if ((pick.lat == null) !== (pick.lng == null)) {
      errors.push(`Pick #${expectedRank} must include both lat and lng together`);
    }

    for (const urlField of ['googleMapsUrl', 'website', 'photo']) {
      if (pick[urlField] && !isValidUrl(pick[urlField])) {
        errors.push(`Pick #${expectedRank} has invalid URL in ${urlField}`);
      }
    }

    if (!pick.googleRating) warnings.push(`Pick #${expectedRank} is missing googleRating`);
    if (!pick.reviewCount) warnings.push(`Pick #${expectedRank} is missing reviewCount`);
    if (!pick.photo) warnings.push(`Pick #${expectedRank} is missing photo`);
    if (!Array.isArray(pick.redditQuotes) || pick.redditQuotes.length === 0) {
      warnings.push(`Pick #${expectedRank} is missing redditQuotes`);
    }
  });

  const faqQuestions = new Set();
  (data.faq || []).forEach((item, index) => {
    if (!isNonEmptyString(item.question) || !isNonEmptyString(item.answer)) {
      errors.push(`FAQ #${index + 1} must include question and answer`);
    }
    if (faqQuestions.has(item.question)) {
      errors.push(`Duplicate FAQ question: ${item.question}`);
    }
    faqQuestions.add(item.question);
  });

  if (!isValidUrl(data?.seo?.canonicalPath || '')) {
    warnings.push('seo.canonicalPath is not an absolute URL; renderer will treat it as site-relative');
  }

  if (!data?.map?.enabled) warnings.push('Map section is disabled');
  if ((data?.related?.manual || []).length < 3) warnings.push('Related manual links has fewer than 3 entries');
  if (backfillMode && data?.provenance?.importedFromHtml) warnings.push('Backfill-mode validation: extracted HTML source is not publish-ready until reviewed');

  return { errors, warnings, mode };
}

if (require.main === module) {
  const filePath = process.argv[2];
  const backfill = process.argv.includes('--backfill');
  if (!filePath) {
    console.error('Usage: node validate-source.js <file.json> [--backfill]');
    process.exit(1);
  }

  const result = validateSource(loadJson(path.resolve(filePath)), { mode: backfill ? 'backfill' : 'publish' });
  for (const warning of result.warnings) console.warn(`WARN: ${warning}`);
  for (const error of result.errors) console.error(`ERROR: ${error}`);
  if (result.errors.length) process.exit(1);
  console.log(`OK: ${path.basename(filePath)} passed in ${result.mode} mode with ${result.warnings.length} warning(s)`);
}

module.exports = { validateSource, loadJson, isNonFoodVertical };
