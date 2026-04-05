#!/usr/bin/env node
/**
 * Comprehensive hub data quality cleanup script.
 * Fixes: wrong-country entries, bogus slugs, sentence-length titles, generic country buckets.
 *
 * Strategy for bogus detection: A card is bogus if its slug appears in a DIFFERENT
 * hub's data as well (meaning it was copied from another country's hub), OR if the
 * slug's page (popular-picks/{slug}/index.html) doesn't exist at all.
 *
 * Usage: node scripts/audit-fix-hubs.js [--dry-run]
 */

const fs = require('fs');
const path = require('path');

const DRY_RUN = process.argv.includes('--dry-run');
const HUB_DIR = path.join(__dirname, '..', 'popular-picks-hub-data');
const PP_DIR = path.join(__dirname, '..', 'popular-picks');
const PP_DATA_DIR = path.join(__dirname, '..', 'popular-picks-data');

// Build set of all existing popular-picks page directories
const existingPages = new Set(
  fs.readdirSync(PP_DIR, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name)
);

// Build set of all existing popular-picks-data source JSON files
const existingSourceData = new Set(
  fs.readdirSync(PP_DATA_DIR)
    .filter(f => f.endsWith('.json'))
    .map(f => f.replace('.json', ''))
);

// Step 1: Build a map of slug -> which hub(s) contain it
// and slug -> source data country (from popular-picks-data JSON)
const allHubFiles = fs.readdirSync(HUB_DIR).filter(f => f.endsWith('.json'));
const allHubData = {};
const slugToHubs = {}; // slug -> [hubSlug, ...]

for (const filename of allHubFiles) {
  const hubSlug = filename.replace('.json', '');
  const filepath = path.join(HUB_DIR, filename);
  try {
    const data = JSON.parse(fs.readFileSync(filepath, 'utf8'));
    allHubData[hubSlug] = data;
    for (const section of (data.sections || [])) {
      for (const card of (section.cards || [])) {
        if (!slugToHubs[card.slug]) slugToHubs[card.slug] = [];
        slugToHubs[card.slug].push(hubSlug);
      }
    }
  } catch (e) {
    console.error(`Error reading ${filename}: ${e.message}`);
  }
}

// Known wrong-hub cards: slug -> correct hub (manually verified from HTML content)
// These pages lack source data JSON so can't be auto-detected
const KNOWN_WRONG_HUB = {
  // In usa.json but belong elsewhere
  'tromso-northern-lights-tours': 'norway',
  'taipei-tamsui-riverside-evening': 'taiwan',
  'toronto-street-food': 'canada',
  'bilbao-guggenheim': 'spain',
  'brisbane-craft-beer': 'australia',
  // In hungary.json but belongs to slovakia
  'bratislava-rooftop-bars': 'slovakia',
  // In italy.json with wrong slugs
  'kathmandu-buff-momo-dumplings': 'nepal',
  'strasbourg-tarte-flambee': 'france',
  'bologna-mortadella-shops': 'italy', // correct country but wrong section
  // In barbados
  'san-juan-rum-bars': 'puerto-rico',
  'port-of-spain-doubles': 'trinidad-and-tobago',
  // In brazil
  'medellin-coworking-cafes': 'colombia',
  'medellin-craft-beer': 'colombia',
  // In colombia
  'santiago-craft-beer': 'chile',
  // In romania
  'rome-nightlife': 'italy',
  // In south-africa
  'hackney-natural-wine-bars': 'united-kingdom',
  // In turkey
  'nakameguro-canal-cafes': 'japan',
  // In united-kingdom with wrong slugs
  'zagreb-craft-beer': 'croatia',
  // In mexico
  'bordeaux-canele': 'france',
  // In canada
  'riga-art-nouveau': 'latvia',
  // In france
  'montmartre-cafes': 'france', // actually correct country, wrong section ID
  // In finland
  'yanaka-craft-shops': 'japan',
};

// Step 2: For each slug, determine its "true" hub by reading its source data
function getSlugCountry(slug) {
  const sourcePath = path.join(PP_DATA_DIR, slug + '.json');
  if (!fs.existsSync(sourcePath)) return null;
  try {
    const data = JSON.parse(fs.readFileSync(sourcePath, 'utf8'));
    return {
      country: data.taxonomy?.country || null,
      city: data.taxonomy?.city || null,
    };
  } catch (e) {
    return null;
  }
}

// Country code -> hub slug mapping
const countryCodeToHub = {
  JP: 'japan', US: 'usa', GB: 'united-kingdom', UK: 'united-kingdom',
  FR: 'france', DE: 'germany', IT: 'italy', ES: 'spain', PT: 'portugal',
  NL: 'netherlands', BE: 'belgium', AT: 'austria', CH: 'switzerland',
  GR: 'greece', TR: 'turkey', IE: 'ireland',
  CA: 'canada', MX: 'mexico', BR: 'brazil', AR: 'argentina', CO: 'colombia',
  PE: 'peru', CL: 'chile', EC: 'ecuador', PA: 'panama', CR: 'costa-rica',
  CU: 'cuba', JM: 'jamaica', BB: 'barbados', LC: 'saint-lucia', TT: 'trinidad-and-tobago',
  CN: 'china', KR: 'south-korea', TW: 'taiwan', TH: 'thailand', VN: 'vietnam',
  SG: 'singapore', MY: 'malaysia', ID: 'indonesia', PH: 'philippines',
  KH: 'cambodia', MM: 'myanmar', LA: 'laos', IN: 'india', LK: 'sri-lanka',
  NP: 'nepal', PK: 'pakistan', BD: 'bangladesh', BT: 'bhutan',
  AU: 'australia', NZ: 'new-zealand',
  ZA: 'south-africa', MA: 'morocco', EG: 'egypt', KE: 'kenya', TZ: 'tanzania',
  ET: 'ethiopia', GH: 'ghana', NG: 'nigeria', TN: 'tunisia', BW: 'botswana',
  CZ: 'czech-republic', PL: 'poland', HU: 'hungary', RO: 'romania',
  BG: 'bulgaria', HR: 'croatia', SI: 'slovenia', RS: 'serbia',
  BA: 'bosnia-and-herzegovina', ME: 'montenegro', MK: 'north-macedonia',
  SK: 'slovakia', LT: 'lithuania', LV: 'latvia', EE: 'estonia',
  SE: 'sweden', NO: 'norway', DK: 'denmark', FI: 'finland', IS: 'iceland',
  RU: 'russia', UA: 'ukraine', GE: 'georgia', AM: 'armenia', AZ: 'azerbaijan',
  UZ: 'uzbekistan', KZ: 'kazakhstan', KG: 'kyrgyzstan',
  AE: 'uae', SA: 'saudi-arabia', QA: 'qatar', OM: 'oman', BH: 'bahrain',
  KW: 'kuwait', JO: 'jordan', LB: 'lebanon', IL: 'israel', IR: 'iran', IQ: 'iraq',
  HK: 'hong-kong', MO: 'macau',
  PR: 'puerto-rico',
};

const stats = {
  filesProcessed: 0,
  filesModified: 0,
  bogusRemoved: 0,
  titlesFixed: 0,
  bucketsDissolved: 0,
  sectionsRemoved: 0,
};

const report = [];

// Fix a sentence-length title
function fixLongTitle(title, slug, badge) {
  if (!title || title.length <= 80) return null;

  // Extract the number prefix
  const numMatch = title.match(/^(\d+\s+(?:Best|Hidden|Top))\s+/i);
  // Also handle "The N Best" pattern
  const theMatch = title.match(/^(The\s+\d+\s+(?:Best|Hidden|Top))\s+/i);
  const match = theMatch || numMatch;
  if (!match) return null;

  const prefix = match[1];
  const rest = title.slice(match[0].length);

  // Check if rest starts with a verb (sentence pattern)
  const verbPattern = /^[""]?(sip|sleep|soak|paddle|take|pick|photograph|stroll|wander|explore|discover|bar-hop|hop|ride|watch|taste|sample|sail|hike|climb|walk|shop|browse|visit|experience|enjoy|try|find|hunt|search|seek|savor|feast|indulge|cruise|float|drift|cycle|trek|surf|dive|snorkel|kayak|swim|ski|snowboard|relax|unwind|meditate|pray|worship|celebrate|dance|sing|play|learn|study|cook|bake|brew|distill|craft|paint|draw|sculpt|weave|carve|forge|mold|build|design|create|make|grow|harvest|pick up|step into|head to|venture|cross|navigate|roam|meander|zigzag|loop|circle|detour|clip-clop|scramble|bite|slurp|eat|drink|graze|warm|chase|linger|haggle|marvel|attend|ferry|scale|tour|warm up|slow|farm|james|the largest|rainbow|stone-ground|kansas|shrimp)/i;

  if (verbPattern.test(rest)) {
    // Sentence-as-title: derive a proper title from slug
    const city = (badge || '').replace(/^📍\s*/, '').trim();
    const slugWords = slug.split('-');

    // Remove city words from slug to get topic
    const cityLower = city.toLowerCase();
    const cityWords = cityLower.split(/[\s,]+/).filter(w => w.length > 2);
    const topicWords = slugWords.filter(w => !cityWords.includes(w.toLowerCase()));
    const topic = topicWords.map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');

    if (city && topic) {
      const newTitle = `${prefix} ${topic} in ${city}`;
      if (newTitle.length <= 80) return newTitle;
    }
    return null; // Can't auto-fix safely
  }

  // Not a sentence — try trimming year/source markers
  let fixed = title
    .replace(/\s*\(2026\)/g, '')
    .replace(/\s*—\s*Reddit[- ]Backed Guide/gi, '')
    .replace(/\s*—\s*Reddit's Top Picks/gi, '')
    .replace(/\s*—\s*The Unfiltered Guide/gi, '')
    .replace(/\s*—\s*Reddit-Approved Guide/gi, '')
    .replace(/\s*—\s*An? Unfiltered Guide/gi, '');

  if (fixed.length <= 80 && fixed !== title) return fixed;
  return null;
}

function processHub(hubSlug) {
  const data = allHubData[hubSlug];
  if (!data || !data.sections) return;

  stats.filesProcessed++;
  let modified = false;
  const fileIssues = [];

  // --- Pass 1: Remove bogus/wrong-country cards ---
  for (const section of data.sections) {
    if (!section.cards) continue;

    const originalCount = section.cards.length;
    section.cards = section.cards.filter(card => {
      // Check known wrong-hub list first
      if (KNOWN_WRONG_HUB[card.slug] && KNOWN_WRONG_HUB[card.slug] !== hubSlug) {
        fileIssues.push({
          type: 'WRONG_COUNTRY_REMOVED',
          section: section.id,
          slug: card.slug,
          title: card.title,
          sourceCountry: 'manual',
          expectedHub: KNOWN_WRONG_HUB[card.slug],
        });
        stats.bogusRemoved++;
        modified = true;
        return false;
      }

      // Check if this card's slug has source data
      const sourceInfo = getSlugCountry(card.slug);

      if (sourceInfo && sourceInfo.country) {
        // We have source data — check if its country matches this hub
        const expectedHub = countryCodeToHub[sourceInfo.country];
        if (expectedHub && expectedHub !== hubSlug) {
          fileIssues.push({
            type: 'WRONG_COUNTRY_REMOVED',
            section: section.id,
            slug: card.slug,
            title: card.title,
            sourceCountry: sourceInfo.country,
            expectedHub: expectedHub,
          });
          stats.bogusRemoved++;
          modified = true;
          return false;
        }
      }

      // Check if the page actually exists
      if (!existingPages.has(card.slug)) {
        fileIssues.push({
          type: 'MISSING_PAGE_REMOVED',
          section: section.id,
          slug: card.slug,
          title: card.title,
        });
        stats.bogusRemoved++;
        modified = true;
        return false;
      }

      return true;
    });
  }

  // --- Pass 2: Remove empty sections ---
  data.sections = data.sections.filter(section => {
    if (!section.cards || section.cards.length === 0) {
      fileIssues.push({
        type: 'EMPTY_SECTION_REMOVED',
        section: section.id,
      });
      stats.sectionsRemoved++;
      modified = true;
      return false;
    }
    return true;
  });

  // --- Pass 3: Fix long titles ---
  for (const section of data.sections) {
    for (const card of section.cards) {
      if (card.title && card.title.length > 80) {
        const fixed = fixLongTitle(card.title, card.slug, card.badge);
        if (fixed && fixed !== card.title) {
          fileIssues.push({
            type: 'TITLE_FIXED',
            slug: card.slug,
            oldTitle: card.title,
            newTitle: fixed,
          });
          // Also fix imageAlt if it matches old title
          if (card.imageAlt === card.title) {
            card.imageAlt = fixed;
          }
          card.title = fixed;
          stats.titlesFixed++;
          modified = true;
        } else if (!fixed) {
          fileIssues.push({
            type: 'TITLE_STILL_LONG',
            slug: card.slug,
            title: card.title,
            length: card.title.length,
          });
        }
      }
    }
  }

  // --- Pass 4: Dissolve generic country buckets ---
  const countryBucket = data.sections.find(s => s.id === hubSlug);
  if (countryBucket && countryBucket.cards.length > 0) {
    const cardsToMove = [...countryBucket.cards];
    let moved = 0;

    for (const card of cardsToMove) {
      // Try to find the right city section from the slug
      const slugParts = card.slug.split('-');
      let placed = false;

      // Try matching against existing sections by checking if slug starts with section id
      for (const section of data.sections) {
        if (section.id === hubSlug) continue;
        if (card.slug.startsWith(section.id + '-') || card.slug.startsWith(section.id)) {
          section.cards.push(card);
          placed = true;
          moved++;
          break;
        }
      }

      if (!placed) {
        // Try source data for city info
        const sourceInfo = getSlugCountry(card.slug);
        if (sourceInfo && sourceInfo.city) {
          const cityId = sourceInfo.city.toLowerCase()
            .normalize('NFKD').replace(/[\u0300-\u036f]/g, '')
            .replace(/[^a-z0-9\s-]/g, '').replace(/\s+/g, '-').trim();

          const existingSection = data.sections.find(s => s.id === cityId);
          if (existingSection && existingSection.id !== hubSlug) {
            existingSection.cards.push(card);
            placed = true;
            moved++;
          } else if (cityId !== hubSlug) {
            // Create new section
            data.sections.push({
              id: cityId,
              title: sourceInfo.city,
              cards: [card],
            });
            placed = true;
            moved++;
          }
        }
      }

      if (!placed) {
        // Last resort: derive from slug prefix
        const cityId = slugParts[0];
        if (cityId !== hubSlug) {
          const existingSection = data.sections.find(s => s.id === cityId);
          if (existingSection) {
            existingSection.cards.push(card);
          } else {
            data.sections.push({
              id: cityId,
              title: cityId.charAt(0).toUpperCase() + cityId.slice(1),
              cards: [card],
            });
          }
          moved++;
        }
      }
    }

    if (moved > 0) {
      data.sections = data.sections.filter(s => s.id !== hubSlug);
      data.sections.sort((a, b) => a.id.localeCompare(b.id));
      fileIssues.push({
        type: 'COUNTRY_BUCKET_DISSOLVED',
        cardsRedistributed: moved,
      });
      stats.bucketsDissolved++;
      modified = true;
    }
  }

  // --- Pass 5: Sync TOC ---
  if (modified && data.toc) {
    data.toc = data.sections.map(s => ({
      id: s.id,
      label: s.title || s.id.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
    }));
  }

  // --- Write ---
  if (modified) {
    stats.filesModified++;
    if (!DRY_RUN) {
      const filepath = path.join(HUB_DIR, hubSlug + '.json');
      fs.writeFileSync(filepath, JSON.stringify(data, null, 2) + '\n');
    }
  }

  if (fileIssues.length > 0) {
    report.push({ file: hubSlug + '.json', issues: fileIssues });
  }
}

// Process all hubs
for (const hubSlug of Object.keys(allHubData).sort()) {
  processHub(hubSlug);
}

// Print report
console.log(`\n=== HUB CLEANUP REPORT (${DRY_RUN ? 'DRY RUN' : 'APPLIED'}) ===\n`);
console.log(`Files processed: ${stats.filesProcessed}`);
console.log(`Files modified: ${stats.filesModified}`);
console.log(`Bogus/wrong-country cards removed: ${stats.bogusRemoved}`);
console.log(`Titles fixed: ${stats.titlesFixed}`);
console.log(`Country buckets dissolved: ${stats.bucketsDissolved}`);
console.log(`Empty sections removed: ${stats.sectionsRemoved}`);

let titleStillLong = 0;
for (const entry of report) {
  const counts = {};
  for (const issue of entry.issues) {
    counts[issue.type] = (counts[issue.type] || 0) + 1;
    if (issue.type === 'TITLE_STILL_LONG') titleStillLong++;
  }
  console.log(`\n[${entry.file}] ${Object.entries(counts).map(([k, v]) => `${k}: ${v}`).join(', ')}`);

  for (const issue of entry.issues) {
    if (issue.type === 'WRONG_COUNTRY_REMOVED') {
      console.log(`  - Removed (${issue.sourceCountry}->${issue.expectedHub}): ${issue.slug}`);
    } else if (issue.type === 'MISSING_PAGE_REMOVED') {
      console.log(`  - Removed (no page): ${issue.slug}`);
    } else if (issue.type === 'TITLE_FIXED') {
      console.log(`  - Title: "${issue.newTitle}"`);
    } else if (issue.type === 'TITLE_STILL_LONG') {
      console.log(`  - LONG (${issue.length}): ${issue.slug}`);
    } else if (issue.type === 'COUNTRY_BUCKET_DISSOLVED') {
      console.log(`  - Dissolved: ${issue.cardsRedistributed} cards moved`);
    } else if (issue.type === 'EMPTY_SECTION_REMOVED') {
      console.log(`  - Empty section removed: ${issue.section}`);
    }
  }
}
console.log(`\nTitles still long (need manual fix): ${titleStillLong}`);
