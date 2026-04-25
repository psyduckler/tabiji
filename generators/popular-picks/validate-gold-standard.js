#!/usr/bin/env node
/**
 * Gold-standard checklist for popular-picks pages.
 *
 * Run on the *rendered HTML* (not the source JSON). Each check returns
 * { id, level: 'error'|'warn', ok: bool, message } so the caller can
 * decide whether to abort the rebuild or just warn.
 *
 * The "gold standard" reference is /popular-picks/new-york-steak/. Any
 * deviation from that page's structure should either be intentional
 * (and added as a documented exception) or fail this checklist.
 */
const fs = require('fs');

function pageBody(html) {
  const m = html.match(/<body[^>]*>([\s\S]*?)<\/body>/);
  return m ? m[1] : html;
}

function visibleText(html) {
  const body = pageBody(html);
  return body
    .replace(/<script[\s\S]*?<\/script>/g, ' ')
    .replace(/<style[\s\S]*?<\/style>/g, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&[a-z#0-9]+;/gi, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function jsonLdBlocks(html) {
  const out = [];
  const re = /<script type="application\/ld\+json">([\s\S]*?)<\/script>/g;
  let m;
  while ((m = re.exec(html))) {
    try { out.push(JSON.parse(m[1])); } catch { out.push({ __parseError: true }); }
  }
  return out;
}

function metaContent(html, name) {
  const re = new RegExp(`<meta\\s+(?:name|property)="${name}"\\s+content="([^"]*)"`, 'i');
  const m = html.match(re);
  return m ? m[1] : '';
}

function check(id, level, ok, message) { return { id, level, ok, message }; }

function validateGoldStandard(html, options = {}) {
  const checks = [];
  const slug = options.slug || '';
  const publishedSlugs = options.publishedSlugs || new Set();

  // ---- DOCTYPE + lang ----
  checks.push(check('doctype', 'error', html.startsWith('<!DOCTYPE html>'), 'Page must start with <!DOCTYPE html>'));
  checks.push(check('lang-en', 'error', /<html lang="en">/.test(html), '<html> must have lang="en"'));

  // ---- Head: meta + canonical + OG ----
  const title = (html.match(/<title>(.*?)<\/title>/) || [, ''])[1].trim();
  checks.push(check('title-present', 'error', title.length >= 20, `<title> too short: "${title}"`));
  checks.push(check('title-length', 'warn', title.length <= 70, `<title> long (${title.length} chars): browsers truncate ~60`));

  const description = metaContent(html, 'description');
  checks.push(check('meta-description', 'error', description.length >= 50, 'meta description missing or short'));
  checks.push(check('meta-description-length', 'warn', description.length <= 165, `meta description ${description.length} chars (>165 truncates in SERP)`));

  checks.push(check('canonical', 'error', /<link rel="canonical"\s+href="https:\/\/tabiji\.ai\//.test(html), 'canonical URL missing or wrong domain'));
  checks.push(check('og-image', 'error', /property="og:image"\s+content="https:\/\/img\.tabiji\.ai\//.test(html), 'og:image must be on img.tabiji.ai'));
  checks.push(check('preconnect-img', 'error', /<link rel="preconnect" href="https:\/\/img\.tabiji\.ai">/.test(html), 'missing img.tabiji.ai preconnect'));
  checks.push(check('shared-head-css', 'error', /href="\/assets\/shared-shell\.css"/.test(html), 'missing shared-shell.css link'));
  checks.push(check('shared-head-js', 'error', /src="\/assets\/shared-shell\.js"/.test(html), 'missing shared-shell.js'));
  checks.push(check('shared-head-include', 'warn', /<!-- @include:shared-head:start -->/.test(html), 'missing @include:shared-head marker'));

  // ---- JSON-LD: all 4 expected types ----
  const blocks = jsonLdBlocks(html);
  const types = blocks.map((b) => b['@type']).filter(Boolean);
  checks.push(check('jsonld-parses', 'error', !blocks.some((b) => b.__parseError), 'one or more JSON-LD blocks failed to parse'));
  checks.push(check('jsonld-article', 'error', types.includes('Article'), 'missing Article JSON-LD'));
  checks.push(check('jsonld-itemlist', 'error', types.includes('ItemList'), 'missing ItemList JSON-LD'));
  checks.push(check('jsonld-faq', 'error', types.includes('FAQPage'), 'missing FAQPage JSON-LD'));
  checks.push(check('jsonld-breadcrumb', 'error', types.includes('BreadcrumbList'), 'missing BreadcrumbList JSON-LD'));

  // ---- Author: Bernard Huang Person schema ----
  const article = blocks.find((b) => b['@type'] === 'Article');
  const author = article && article.author;
  const isPersonByline = author && author['@type'] === 'Person' && /Bernard Huang/i.test(author.name || '');
  checks.push(check('person-byline', 'error', isPersonByline, 'Article author must be Person { name: "Bernard Huang" }'));
  checks.push(check('byline-headshot', 'warn', author && /bernard-huang\.jpg/.test(author.image || ''), 'byline missing headshot image'));

  // ---- Body: nav, hero, page-layout ----
  checks.push(check('skip-link', 'error', /class="skip-link" href="#main"/.test(html), 'missing skip-to-content link'));
  checks.push(check('nav-include', 'warn', /<!-- @include:nav:start -->/.test(html), 'missing @include:nav marker'));
  checks.push(check('hero-section', 'error', /<section class="hero">/.test(html), 'missing hero section'));
  checks.push(check('h1-count', 'error', (html.match(/<h1[^>]*>/g) || []).length === 1, 'must have exactly one <h1>'));
  checks.push(check('main-id', 'error', /<main[^>]*id="main"/.test(html), 'main must have id="main" for skip-link target'));

  // ---- Map (desktop sidebar + mobile inline + config + IO observer) ----
  checks.push(check('map-sidebar', 'error', /<section class="map-sidebar" data-map-panel="desktop">/.test(html), 'missing desktop map sidebar'));
  checks.push(check('map-inline', 'error', /<section class="map-inline" data-map-panel="mobile">/.test(html), 'missing mobile inline map'));
  checks.push(check('map-config', 'error', /window\.__POPULAR_PICKS_MAP__\s*=/.test(html), 'missing __POPULAR_PICKS_MAP__ config'));
  checks.push(check('map-api-loader', 'error', /maps\.googleapis\.com\/maps\/api\/js/.test(html), 'missing Google Maps API loader'));

  // Map config has valid coords
  const cfgMatch = html.match(/window\.__POPULAR_PICKS_MAP__\s*=\s*({[\s\S]*?});/);
  let mapPicks = [];
  if (cfgMatch) {
    try { mapPicks = JSON.parse(cfgMatch[1]).picks || []; } catch (e) {}
  }
  const badCoords = mapPicks.filter((p) => !Number.isFinite(p.lat) || !Number.isFinite(p.lng) || p.lat === 0 || p.lng === 0);
  checks.push(check('map-coords', 'error', mapPicks.length > 0 && badCoords.length === 0, badCoords.length ? `${badCoords.length} picks have invalid coords` : 'map config has zero picks'));

  // The fixed IntersectionObserver pattern (rootMargin -35% / -55%, threshold:0, inStripe Set)
  checks.push(check('io-observer-fixed', 'error', /rootMargin: '-35% 0px -55% 0px', threshold: 0/.test(html), 'IntersectionObserver still uses old broken config'));
  checks.push(check('io-no-old-config', 'error', !/rootMargin: '-25% 0px -45% 0px'/.test(html), 'IntersectionObserver still has the old -25%/-45% rootMargin'));

  // ---- Restaurant sections ----
  const restaurantSectionMatches = html.match(/<section\s+class="restaurant-section"[^>]*>/g) || [];
  checks.push(check('restaurant-sections-count', 'error', restaurantSectionMatches.length >= 3, `expected ≥3 restaurant sections, got ${restaurantSectionMatches.length}`));
  checks.push(check('restaurant-sections-match-map', 'error', restaurantSectionMatches.length === mapPicks.length, `restaurant sections (${restaurantSectionMatches.length}) ≠ map picks (${mapPicks.length})`));
  // Each section needs lat/lng data attrs to drive the map
  const sectionsMissingCoords = restaurantSectionMatches.filter((s) => !/data-map-lat="/.test(s) || !/data-map-lng="/.test(s));
  checks.push(check('restaurant-sections-have-coords', 'error', sectionsMissingCoords.length === 0, `${sectionsMissingCoords.length} restaurant sections missing data-map-lat/lng`));

  // ---- FAQ visible (not just schema) ----
  const faqHtmlItems = (html.match(/class="faq-item"/g) || []).length;
  checks.push(check('faq-visible', 'error', faqHtmlItems >= 3, `FAQ rendered HTML must have ≥3 .faq-item (have ${faqHtmlItems}); schema-only is invisible to users`));

  // ---- Sections forbidden by gold standard ----
  checks.push(check('no-related-picks-module', 'error', !/class="related-picks-module"/.test(html), 'should not contain old related-picks-module'));
  checks.push(check('no-email-capture', 'error', !/class="email-capture"/.test(html), 'should not contain email-capture block'));
  checks.push(check('no-viator', 'warn', !/class="viator-section"/.test(html), 'viator-section is deprecated on popular-picks'));

  // ---- Footer ----
  checks.push(check('footer-include', 'error', /<!-- @include:footer:start -->/.test(html), 'missing @include:footer:start marker'));
  checks.push(check('footer-grid', 'error', /<div class="footer-grid">/.test(html), 'missing standard 4-col footer grid'));
  checks.push(check('no-inline-footer-override', 'error', !/footer\s*\{[^}]*max-width\s*:\s*1260px/.test(html), 'inline footer { max-width:1260px } override breaks shared-shell.css full-width footer'));

  // ---- Word count + Reddit refs ----
  const text = visibleText(html);
  const words = (text.match(/\b[A-Za-z][A-Za-z'-]+\b/g) || []).length;
  checks.push(check('word-count', 'warn', words >= 1500, `thin content: ${words} words (<1500)`));
  checks.push(check('word-count-deep', 'warn', words >= 2500, `lean content: ${words} words (<2500 — gold standard is 3000+)`));
  const redditCount = (text.match(/\bReddit\b/gi) || []).length;
  checks.push(check('reddit-refs', 'warn', redditCount >= 2, `only ${redditCount} Reddit references — page claims "Reddit-backed" but corpus is sparse`));

  // ---- Encoding sanity ----
  checks.push(check('no-double-amp', 'error', !html.includes('&amp;amp;'), 'double-encoded &amp;amp; entities present'));
  const doubleEncodedEntities = html.match(/&amp;(?:[a-zA-Z]+|#[0-9]+|#x[0-9a-fA-F]+);/g);
  checks.push(check('no-double-entity', 'error', !doubleEncodedEntities, doubleEncodedEntities ? `double-encoded entities (e.g., ${doubleEncodedEntities.slice(0, 3).join(', ')}) — decode entities at source` : 'no double-encoded entities'));
  checks.push(check('no-mojibake', 'error', !/Ã©|Ã |â\x80\x99/.test(html), 'mojibake bytes detected'));
  checks.push(check('no-template-leftover', 'error', !/\{\{|\[TODO\]|\[TBD\]|\[PLACEHOLDER\]|TKTKTK|Lorem ipsum/.test(html), 'template placeholder found'));

  // ---- Internal links to other popular-picks pages must resolve ----
  if (publishedSlugs.size) {
    const links = [...html.matchAll(/href="\/popular-picks\/([^"\/]+)\/?"/g)].map((m) => m[1]);
    const broken = [...new Set(links)].filter((s) => s !== slug && !publishedSlugs.has(s) && s !== '');
    checks.push(check('internal-links-resolve', 'error', broken.length === 0, broken.length ? `broken internal popular-picks links: ${broken.slice(0, 3).join(', ')}` : 'all internal popular-picks links resolve'));
  }

  // ---- Hero image ----
  const ogImg = (html.match(/property="og:image"\s+content="([^"]+)"/) || [, ''])[1];
  if (ogImg) {
    const imgPath = ogImg.replace(/^https?:\/\/img\.tabiji\.ai/, '');
    checks.push(check('og-image-pattern', 'error', /^\/popular-picks\/[^\/]+\/[^\/]+\.(?:jpg|jpeg|png|webp)$/i.test(imgPath), `og:image path doesn't follow /popular-picks/<slug>/<file>.jpg pattern: ${imgPath}`));
  }

  return checks;
}

function summarize(checks) {
  const errors = checks.filter((c) => c.level === 'error' && !c.ok);
  const warnings = checks.filter((c) => c.level === 'warn' && !c.ok);
  const passed = checks.filter((c) => c.ok);
  return {
    pass: errors.length === 0,
    errorCount: errors.length,
    warningCount: warnings.length,
    passedCount: passed.length,
    totalCount: checks.length,
    errors,
    warnings,
  };
}

if (require.main === module) {
  const file = process.argv[2];
  if (!file) {
    console.error('Usage: node validate-gold-standard.js <html-file>');
    process.exit(1);
  }
  const html = fs.readFileSync(file, 'utf8');
  const slug = file.split('/').slice(-2, -1)[0] || '';
  const path = require('path');
  const ppDir = path.resolve(__dirname, '..', '..', 'popular-picks');
  const publishedSlugs = fs.existsSync(ppDir)
    ? new Set(fs.readdirSync(ppDir, { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name))
    : new Set();
  const checks = validateGoldStandard(html, { slug, publishedSlugs });
  const summary = summarize(checks);

  for (const c of checks.filter((x) => !x.ok)) {
    console.log(`  ${c.level === 'error' ? '✗' : '⚠'} [${c.id}] ${c.message}`);
  }
  console.log(`\n${summary.pass ? '✓ PASS' : '✗ FAIL'} — ${summary.passedCount}/${summary.totalCount} passed, ${summary.errorCount} errors, ${summary.warningCount} warnings`);
  process.exit(summary.pass ? 0 : 1);
}

module.exports = { validateGoldStandard, summarize };
