#!/usr/bin/env node
/**
 * rebuild.js — single-shot CLI for the popular-picks rebuild loop.
 *
 *   node generators/popular-picks/rebuild.js <slug>
 *     1. Loads source JSON from api/data/popular-picks/<slug>.json
 *        (or extracts it on the fly from the live HTML if not present).
 *     2. Renders gold-standard HTML via render-page.js.
 *     3. Validates the rendered HTML against the gold-standard checklist.
 *     4. Writes popular-picks/<slug>/index.html only if validation passes
 *        (or with --force to write anyway and surface the errors).
 *     5. Prints a tight delta report so the human reviewer can eyeball
 *        what changed without re-reading the whole file.
 *
 *   Flags:
 *     --force         write output even if checklist fails
 *     --dry-run       render + validate without writing
 *     --check-only    skip render; just run checklist on the existing live page
 *     --json          output machine-readable summary
 *
 * Exit codes: 0 = pass; 1 = checklist failed; 2 = source error; 3 = bad args.
 */
const fs = require('fs');
const path = require('path');
const { renderPage } = require('./render-page');
const { validateSource, loadJson } = require('./validate-source');
const { validateGoldStandard, summarize } = require('./validate-gold-standard');
const { extractExisting } = require('./extract-existing');

const REPO_ROOT = path.resolve(__dirname, '..', '..');
const SOURCE_DIR = path.join(REPO_ROOT, 'api', 'data', 'popular-picks');
const OUT_DIR = path.join(REPO_ROOT, 'popular-picks');

function getPublishedSlugs() {
  if (!fs.existsSync(OUT_DIR)) return new Set();
  return new Set(
    fs.readdirSync(OUT_DIR, { withFileTypes: true })
      .filter((d) => d.isDirectory())
      .map((d) => d.name),
  );
}

function loadSource(slug) {
  const jsonPath = path.join(SOURCE_DIR, `${slug}.json`);
  if (fs.existsSync(jsonPath)) {
    return { source: loadJson(jsonPath), origin: 'json' };
  }
  const htmlPath = path.join(OUT_DIR, slug, 'index.html');
  if (!fs.existsSync(htmlPath)) {
    throw new Error(`No source JSON at ${jsonPath} and no live HTML at ${htmlPath}`);
  }
  const html = fs.readFileSync(htmlPath, 'utf8');
  const extracted = extractExisting(html, slug);
  return { source: extracted.sourceJson, origin: 'extracted-from-html' };
}

function renderAndValidate(source, slug, publishedSlugs) {
  const validation = validateSource(source);
  if (validation.errors.length) {
    return { ok: false, stage: 'source', errors: validation.errors, warnings: validation.warnings };
  }
  const html = renderPage(source);
  const checks = validateGoldStandard(html, { slug, publishedSlugs });
  const summary = summarize(checks);
  return { ok: summary.pass, html, checks, summary, sourceWarnings: validation.warnings };
}

function writeIndex(slug, html) {
  const out = path.join(OUT_DIR, slug, 'index.html');
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, html);
  return out;
}

function readExistingHtml(slug) {
  const p = path.join(OUT_DIR, slug, 'index.html');
  return fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : null;
}

function buildDelta(oldHtml, newHtml) {
  if (!oldHtml) return { sections: [], summary: 'new file' };
  const before = analyseHtml(oldHtml);
  const after = analyseHtml(newHtml);
  const lines = [];
  const tag = (k, oldV, newV) => {
    if (oldV !== newV) lines.push(`  ${k}: ${oldV} → ${newV}`);
  };
  tag('restaurant sections', before.sections, after.sections);
  tag('faq.faq-item count', before.faqItems, after.faqItems);
  tag('jsonld blocks', before.jsonLd, after.jsonLd);
  tag('word count', before.words, after.words);
  tag('related-picks-module', before.hasOldRelated, after.hasOldRelated);
  tag('email-capture', before.hasEmailCapture, after.hasEmailCapture);
  tag('inline footer override', before.hasFooterOverride, after.hasFooterOverride);
  tag('IO observer (fixed)', before.hasFixedIO, after.hasFixedIO);
  tag('Person byline schema', before.hasPersonByline, after.hasPersonByline);
  return { lines };
}

function analyseHtml(html) {
  const text = html.replace(/<script[\s\S]*?<\/script>/g, ' ').replace(/<style[\s\S]*?<\/style>/g, ' ').replace(/<[^>]+>/g, ' ');
  return {
    sections: (html.match(/<section\s+class="restaurant-section"/g) || []).length,
    faqItems: (html.match(/class="faq-item"/g) || []).length,
    jsonLd: (html.match(/<script type="application\/ld\+json">/g) || []).length,
    words: (text.match(/\b[A-Za-z][A-Za-z'-]+\b/g) || []).length,
    hasOldRelated: /class="related-picks-module"/.test(html),
    hasEmailCapture: /class="email-capture"/.test(html),
    hasFooterOverride: /footer\s*\{[^}]*max-width\s*:\s*1260px/.test(html),
    hasFixedIO: /rootMargin: '-35% 0px -55% 0px'/.test(html),
    hasPersonByline: /"@type":\s*"Person"[\s\S]{0,200}?Bernard Huang/.test(html),
  };
}

function printReport(slug, result, delta, opts = {}) {
  if (opts.json) {
    console.log(JSON.stringify({ slug, ok: result.ok, summary: result.summary, delta: delta?.lines || [] }, null, 2));
    return;
  }
  const tag = result.ok ? '\x1b[32m✓ PASS\x1b[0m' : '\x1b[31m✗ FAIL\x1b[0m';
  console.log(`${tag} ${slug}`);
  if (result.summary) {
    console.log(`  ${result.summary.passedCount}/${result.summary.totalCount} checks passed (${result.summary.errorCount} errors, ${result.summary.warningCount} warnings)`);
  }
  if (result.errors) {
    for (const e of result.errors) console.log(`    \x1b[31msource error\x1b[0m ${e}`);
  }
  if (result.summary && !result.summary.pass) {
    for (const e of result.summary.errors) console.log(`    \x1b[31m✗\x1b[0m [${e.id}] ${e.message}`);
  }
  if (result.summary && result.summary.warnings.length) {
    for (const w of result.summary.warnings) console.log(`    \x1b[33m⚠\x1b[0m [${w.id}] ${w.message}`);
  }
  if (delta && delta.lines && delta.lines.length) {
    console.log('  Δ vs previous:');
    for (const l of delta.lines) console.log(l);
  }
}

function parseArgs(argv) {
  const args = { positional: [], flags: {} };
  for (const a of argv) {
    if (a.startsWith('--')) args.flags[a.slice(2)] = true;
    else args.positional.push(a);
  }
  return args;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const slug = args.positional[0];
  if (!slug) {
    console.error('Usage: node generators/popular-picks/rebuild.js <slug> [--force] [--dry-run] [--check-only] [--json]');
    process.exit(3);
  }
  const publishedSlugs = getPublishedSlugs();

  if (args.flags['check-only']) {
    const html = readExistingHtml(slug);
    if (!html) {
      console.error(`No live HTML for ${slug}`);
      process.exit(2);
    }
    const checks = validateGoldStandard(html, { slug, publishedSlugs });
    const summary = summarize(checks);
    printReport(slug, { ok: summary.pass, summary }, null, { json: args.flags.json });
    process.exit(summary.pass ? 0 : 1);
  }

  let source;
  let origin;
  try {
    const loaded = loadSource(slug);
    source = loaded.source;
    origin = loaded.origin;
  } catch (e) {
    console.error(e.message);
    process.exit(2);
  }

  const result = renderAndValidate(source, slug, publishedSlugs);
  if (result.stage === 'source') {
    printReport(slug, result, null, { json: args.flags.json });
    process.exit(2);
  }

  const oldHtml = readExistingHtml(slug);
  const delta = buildDelta(oldHtml, result.html);

  let written = null;
  if (!args.flags['dry-run'] && (result.ok || args.flags.force)) {
    written = writeIndex(slug, result.html);
  }

  printReport(slug, result, delta, { json: args.flags.json });
  if (origin !== 'json' && !args.flags.json) {
    console.log(`  source: ${origin} (no JSON yet at api/data/popular-picks/${slug}.json)`);
  }
  if (written && !args.flags.json) console.log(`  wrote ${path.relative(REPO_ROOT, written)}`);
  if (!result.ok && !args.flags.force && !args.flags.json) {
    console.log('  (not written; pass --force to write despite checklist failures)');
  }

  process.exit(result.ok ? 0 : 1);
}

if (require.main === module) main();

module.exports = { renderAndValidate, loadSource };
