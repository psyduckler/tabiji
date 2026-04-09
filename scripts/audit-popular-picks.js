#!/usr/bin/env node
/**
 * Popular Picks Quality Audit
 *
 * Scores every popular-picks JSON against the golden standard
 * (shibuya-ramen) and outputs CSV + JSON reports.
 *
 * Usage: node scripts/audit-popular-picks.js
 */

const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '..', 'popular-picks-data');
const OUT_DIR = path.join(__dirname, '..', 'docs', 'audits');

// --------------- scoring rubric ---------------

function scorePage(data) {
  const issues = [];
  const picks = data.picks || [];
  const numPicks = picks.length;

  if (numPicks === 0) {
    return { total: 0, tier1: 0, tier2: 0, tier3: 0, issues: ['NO_PICKS'], critical: true };
  }

  // Helper: percentage of picks that have a truthy field
  const pct = (field) => {
    const count = picks.filter(p => {
      const val = p[field];
      if (Array.isArray(val)) return val.length > 0;
      return val != null && val !== '' && val !== 'N/A';
    }).length;
    return count / numPicks;
  };

  // ---- TIER 1: Must Have (60 pts) ----
  let tier1 = 0;

  // Map + coordinates (10 pts)
  const mapEnabled = data.map && data.map.enabled;
  const latLngPct = pct('lat') * pct('lng');
  if (mapEnabled && latLngPct === 1) tier1 += 10;
  else if (mapEnabled) { tier1 += Math.round(latLngPct * 10); issues.push(`MISSING_COORDS:${Math.round((1 - latLngPct) * numPicks)} picks`); }
  else { issues.push('MAP_DISABLED'); }

  // Photos (8 pts)
  const photoPct = pct('photo');
  tier1 += Math.round(photoPct * 8);
  if (photoPct < 1) issues.push(`MISSING_PHOTOS:${Math.round((1 - photoPct) * numPicks)} picks`);

  // whyItMadeTheList (8 pts)
  const whyPct = pct('whyItMadeTheList');
  tier1 += Math.round(whyPct * 8);
  if (whyPct < 1) issues.push(`MISSING_WHY:${Math.round((1 - whyPct) * numPicks)} picks`);

  // whatToOrder (8 pts)
  const whatPct = pct('whatToOrder');
  tier1 += Math.round(whatPct * 8);
  if (whatPct < 1) issues.push(`MISSING_WHAT_TO_ORDER:${Math.round((1 - whatPct) * numPicks)} picks`);

  // insiderTip (8 pts)
  const tipPct = pct('insiderTip');
  tier1 += Math.round(tipPct * 8);
  if (tipPct < 1) issues.push(`MISSING_INSIDER_TIP:${Math.round((1 - tipPct) * numPicks)} picks`);

  // redditQuotes (8 pts)
  const quotePct = pct('redditQuotes');
  tier1 += Math.round(quotePct * 8);
  if (quotePct < 1) issues.push(`MISSING_REDDIT_QUOTES:${Math.round((1 - quotePct) * numPicks)} picks`);

  // googleRating + reviewCount (5 pts)
  const ratingPct = pct('googleRating');
  tier1 += Math.round(ratingPct * 5);
  if (ratingPct < 1) issues.push(`MISSING_RATING:${Math.round((1 - ratingPct) * numPicks)} picks`);

  // FAQ (5 pts)
  const faqCount = (data.faq || []).length;
  if (faqCount >= 4) tier1 += 5;
  else if (faqCount >= 2) { tier1 += 3; issues.push(`LOW_FAQ:${faqCount}`); }
  else if (faqCount >= 1) { tier1 += 1; issues.push(`LOW_FAQ:${faqCount}`); }
  else issues.push('NO_FAQ');

  // ---- TIER 2: Should Have (30 pts) ----
  let tier2 = 0;

  // hoursNote (5 pts)
  const hoursPct = pct('hoursNote');
  tier2 += Math.round(hoursPct * 5);
  if (hoursPct < 0.8) issues.push(`MISSING_HOURS:${Math.round((1 - hoursPct) * numPicks)} picks`);

  // website (5 pts)
  const webPct = pct('website');
  tier2 += Math.round(webPct * 5);
  if (webPct < 0.8) issues.push(`MISSING_WEBSITE:${Math.round((1 - webPct) * numPicks)} picks`);

  // phone (3 pts)
  const phonePct = pct('phone');
  tier2 += Math.round(phonePct * 3);
  if (phonePct < 0.5) issues.push(`MISSING_PHONE:${Math.round((1 - phonePct) * numPicks)} picks`);

  // priceRangeLocal (5 pts)
  const pricePct = pct('priceRangeLocal');
  tier2 += Math.round(pricePct * 5);
  if (pricePct < 0.8) issues.push(`MISSING_PRICE:${Math.round((1 - pricePct) * numPicks)} picks`);

  // methodology (4 pts)
  const hasMeth = data.intro && data.intro.methodology && data.intro.methodology.length > 20;
  if (hasMeth) tier2 += 4;
  else issues.push('NO_METHODOLOGY');

  // hero.dek (3 pts)
  const hasDek = data.hero && data.hero.dek && data.hero.dek.length > 5;
  if (hasDek) tier2 += 3;
  else issues.push('NO_HERO_DEK');

  // summary block (5 pts)
  let summaryPts = 0;
  if (data.summary) {
    if (data.summary.bestOverall) summaryPts += 2;
    if (data.summary.topPick) summaryPts += 1;
    if (data.summary.priceRangeLocal) summaryPts += 2;
  }
  tier2 += summaryPts;
  if (summaryPts < 5) issues.push('INCOMPLETE_SUMMARY');

  // ---- TIER 3: Nice to Have (10 pts) ----
  let tier3 = 0;

  // touristyLevel (3 pts)
  const touristyPct = pct('touristyLevel');
  tier3 += Math.round(touristyPct * 3);

  // provenance (3 pts)
  const provPct = pct('provenance');
  tier3 += Math.round(provPct * 3);

  // 6+ FAQs (2 pts)
  if (faqCount >= 6) tier3 += 2;
  else if (faqCount >= 5) tier3 += 1;

  // related.manual (2 pts)
  const relCount = (data.related && data.related.manual || []).length;
  if (relCount >= 3) tier3 += 2;
  else if (relCount >= 1) tier3 += 1;

  const total = tier1 + tier2 + tier3;
  const critical = photoPct < 1 || latLngPct < 0.5 || faqCount === 0 || numPicks < 3;

  return { total, tier1, tier2, tier3, issues, critical, numPicks, faqCount };
}

// --------------- main ---------------

function main() {
  const files = fs.readdirSync(DATA_DIR).filter(f => f.endsWith('.json'));
  const results = [];

  for (const file of files) {
    try {
      const raw = fs.readFileSync(path.join(DATA_DIR, file), 'utf8');
      const data = JSON.parse(raw);

      // Skip non-popular-picks pages
      if (data.pageType !== 'popular-picks') continue;

      const score = scorePage(data);
      results.push({
        slug: data.slug || file.replace('.json', ''),
        city: (data.taxonomy && data.taxonomy.city) || '',
        country: (data.taxonomy && data.taxonomy.country) || '',
        category: (data.taxonomy && data.taxonomy.category) || '',
        ...score,
      });
    } catch (err) {
      console.error(`Error processing ${file}: ${err.message}`);
    }
  }

  // Sort by score ascending (worst first)
  results.sort((a, b) => a.total - b.total);

  // ---- Console summary ----
  const scores = results.map(r => r.total);
  const avg = (scores.reduce((s, v) => s + v, 0) / scores.length).toFixed(1);
  const criticalCount = results.filter(r => r.critical).length;

  console.log('\n=== POPULAR PICKS AUDIT REPORT ===\n');
  console.log(`Total pages audited: ${results.length}`);
  console.log(`Average score: ${avg}/100`);
  console.log(`Critical issues: ${criticalCount} pages`);

  // Distribution
  const buckets = { '0-19': 0, '20-39': 0, '40-59': 0, '60-79': 0, '80-89': 0, '90-100': 0 };
  for (const s of scores) {
    if (s < 20) buckets['0-19']++;
    else if (s < 40) buckets['20-39']++;
    else if (s < 60) buckets['40-59']++;
    else if (s < 80) buckets['60-79']++;
    else if (s < 90) buckets['80-89']++;
    else buckets['90-100']++;
  }
  console.log('\nScore distribution:');
  for (const [range, count] of Object.entries(buckets)) {
    const bar = '█'.repeat(Math.ceil(count / 5));
    console.log(`  ${range.padStart(6)}: ${String(count).padStart(4)} ${bar}`);
  }

  // Most common issues
  const issueCounts = {};
  for (const r of results) {
    for (const iss of r.issues) {
      const key = iss.split(':')[0];
      issueCounts[key] = (issueCounts[key] || 0) + 1;
    }
  }
  const topIssues = Object.entries(issueCounts).sort((a, b) => b[1] - a[1]).slice(0, 15);
  console.log('\nTop issues (by page count):');
  for (const [issue, count] of topIssues) {
    console.log(`  ${issue.padEnd(28)} ${count} pages (${(count / results.length * 100).toFixed(0)}%)`);
  }

  // Bottom 20
  console.log('\n--- Bottom 20 pages ---');
  for (const r of results.slice(0, 20)) {
    console.log(`  ${String(r.total).padStart(3)}/100  ${r.slug.padEnd(45)} [T1:${r.tier1} T2:${r.tier2} T3:${r.tier3}] ${r.critical ? '⚠ CRITICAL' : ''}`);
  }

  // Top 20
  console.log('\n--- Top 20 pages ---');
  for (const r of results.slice(-20).reverse()) {
    console.log(`  ${String(r.total).padStart(3)}/100  ${r.slug.padEnd(45)} [T1:${r.tier1} T2:${r.tier2} T3:${r.tier3}]`);
  }

  // ---- Write CSV ----
  if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

  const csvHeader = 'slug,city,country,category,total,tier1,tier2,tier3,numPicks,faqCount,critical,issues';
  const csvRows = results.map(r =>
    `"${r.slug}","${r.city}","${r.country}","${r.category}",${r.total},${r.tier1},${r.tier2},${r.tier3},${r.numPicks},${r.faqCount},${r.critical},"${r.issues.join('; ')}"`
  );
  const csvPath = path.join(OUT_DIR, 'popular-picks-audit-results.csv');
  fs.writeFileSync(csvPath, [csvHeader, ...csvRows].join('\n'));
  console.log(`\nCSV written to: ${csvPath}`);

  // ---- Write JSON ----
  const jsonPath = path.join(OUT_DIR, 'popular-picks-audit-results.json');
  fs.writeFileSync(jsonPath, JSON.stringify(results, null, 2));
  console.log(`JSON written to: ${jsonPath}`);

  // Shibuya-ramen score
  const shibuya = results.find(r => r.slug === 'shibuya-ramen');
  if (shibuya) {
    console.log(`\n🏆 Golden Standard: shibuya-ramen = ${shibuya.total}/100 [T1:${shibuya.tier1} T2:${shibuya.tier2} T3:${shibuya.tier3}]`);
    if (shibuya.issues.length) console.log(`   Remaining issues: ${shibuya.issues.join(', ')}`);
  }
}

main();
