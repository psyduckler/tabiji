#!/usr/bin/env node
/**
 * Round 2 hub data quality fixes:
 * 1. Fix wrong emoji on non-food cards (🍽️ → appropriate emoji)
 * 2. Remove duplicate slugs within same hub
 * 3. Fix 16 remaining long titles
 * 4. Populate hero.meta with guide/city counts
 * 5. Populate publishedTime/modifiedTime
 * 6. Clean up empty Twitter meta strings
 *
 * Usage: node scripts/fix-hubs-round2.js [--dry-run]
 */

const fs = require('fs');
const path = require('path');

const DRY_RUN = process.argv.includes('--dry-run');
const HUB_DIR = path.join(__dirname, '..', 'popular-picks-hub-data');

const stats = {
  emojisFixed: 0,
  duplicatesRemoved: 0,
  titlesFixed: 0,
  heroMetaPopulated: 0,
  datesPopulated: 0,
  twitterCleaned: 0,
  filesModified: 0,
};

// --- Emoji mapping ---
// Keywords in slug/title that indicate non-food content
const NON_FOOD_KEYWORDS = {
  // Accommodation
  '♨️': ['onsen', 'hot-spring', 'geothermal', 'thermal-bath', 'bathhouse', 'sento'],
  '🏨': ['ryokan', 'hotel', 'hostel', 'lodge', 'guesthouse', 'farmhouse', 'homestay', 'glamping', 'safari-camp', 'safari-lodge'],
  // Nature/Outdoors
  '🥾': ['hike', 'hiking', 'trek', 'trekking', 'trail', 'mountain', 'boulder', 'canyon', 'volcano', 'sunrise-hike', 'walk', 'nature'],
  '🏖️': ['beach', 'surf', 'surfing', 'island', 'snorkel', 'snorkeling', 'diving', 'dive', 'kayak', 'kayaking', 'paraglid', 'rock-climbing'],
  '🚣': ['cruise', 'boat', 'ferry', 'river', 'canal', 'houseboat', 'backwater', 'fjord'],
  // Culture/Sights
  '⛩️': ['temple', 'shrine', 'mosque', 'church', 'cathedral', 'monastery', 'pagoda', 'wat', 'relic', 'sacred'],
  '🏛️': ['museum', 'gallery', 'galleries', 'art-gallery', 'guggenheim', 'architecture', 'castle', 'palace', 'fort', 'ruin', 'ruins', 'archaeological', 'underground-vault', 'ghost-tour', 'old-town', 'heritage'],
  '🎨': ['art', 'craft', 'workshop', 'batik', 'pottery', 'weaving', 'puppet', 'tie-dye', 'amber', 'leather', 'calligraphy'],
  // Shopping
  '🛍️': ['shopping', 'vintage', 'fashion', 'thrift', 'flea-market', 'bazaar', 'market-square', 'bookshop', 'antique'],
  // Photography/Views
  '📸': ['instagram', 'photography', 'viewpoint', 'photo', 'illumination', 'northern-lights', 'aurora'],
  // Experiences
  '🎭': ['performance', 'music', 'jazz', 'concert', 'dance', 'festival', 'theater', 'theatre'],
  '👘': ['kimono', 'rental', 'calesa', 'rickshaw'],
  '🌿': ['garden', 'bamboo', 'grove', 'park', 'flower', 'botanical'],
  '🚲': ['cycling', 'bike', 'bicycle'],
  // Day trips
  '🗺️': ['day-trip', 'day-trips'],
  // Nightlife (non-food)
  '🍸': ['cocktail', 'rooftop-bar', 'nightlife', 'bar-hop', 'wine-bar', 'natural-wine', 'sake-bar', 'craft-beer', 'beer-bar', 'pub', 'speakeasy'],
  // Wellness
  '🧘': ['yoga', 'meditation', 'wellness', 'spa', 'retreat'],
  // Coffee/Tea (not restaurant food)
  '☕': ['coffee', 'cafe', 'cafes', 'tea-house', 'teahouse', 'fika', 'kopitiam', 'kaya-toast'],
  // Accommodation-like
  '🏡': ['gassho', 'farmhouse', 'cobblestone'],
};

function getAppropriateEmoji(slug, title) {
  const text = (slug + ' ' + (title || '').toLowerCase()).toLowerCase();

  for (const [emoji, keywords] of Object.entries(NON_FOOD_KEYWORDS)) {
    for (const kw of keywords) {
      if (text.includes(kw)) return emoji;
    }
  }
  return null; // Keep original
}

function isNonFoodCard(slug, title) {
  const text = (slug + ' ' + (title || '').toLowerCase()).toLowerCase();
  const allKeywords = Object.values(NON_FOOD_KEYWORDS).flat();
  return allKeywords.some(kw => text.includes(kw));
}

// --- Manual long title fixes ---
const MANUAL_TITLE_FIXES = {
  'bishkek-osh-bazaar': '12 Best Osh Bazaar Finds in Bishkek',
  'detroit-coney-island-dogs': '12 Best Coney Island Hot Dogs in Detroit',
  'pokhara-sarangkot-paragliding': '12 Best Paragliding in Pokhara',
  'haifa-german-colony-brunch': '12 Best German Colony Brunch Spots in Haifa',
  'rishikesh-ganga-aarti-ceremony': '12 Best Ganga Aarti Ceremonies in Rishikesh',
  'kandy-tooth-relic-temple-visit': '12 Best Temple of the Tooth Experiences in Kandy',
  'kashgar-polo-mutton': '12 Best Polo (Plov) and Mutton in Kashgar',
  'charleston-shrimp-and-grits': '12 Best Shrimp and Grits in Charleston',
  'almaty-big-almaty-lake-hike': '12 Best Big Almaty Lake Hikes',
  'catania-arancini': '12 Best Arancini in Catania',
  'venice-ghost-tours': '12 Best Ghost Tours in Venice',
  'mysore-palace-sunday-illumination': '12 Best Mysore Palace Illumination Experiences',
  'kotor-old-town-walk': '12 Best Old Town Walks in Kotor',
  'florence-aperitivo-bars': '12 Best Aperitivo Bars in Florence',
  'valletta-pastizzi': '12 Best Pastizzi in Valletta',
  'genoa-focaccia': '12 Best Focaccia in Genoa',
};

function processHub(filepath) {
  const filename = path.basename(filepath);
  const raw = fs.readFileSync(filepath, 'utf8');
  let data;
  try {
    data = JSON.parse(raw);
  } catch (e) {
    console.error(`Invalid JSON: ${filename}`);
    return;
  }
  if (!data.sections) return;

  let modified = false;

  // --- Fix 1: Wrong emoji ---
  for (const section of data.sections) {
    for (const card of (section.cards || [])) {
      if (!card.meta || !Array.isArray(card.meta)) continue;

      const hasFoodEmoji = card.meta.some(m => m.includes('🍽️'));
      if (!hasFoodEmoji) continue;

      if (isNonFoodCard(card.slug, card.title)) {
        const newEmoji = getAppropriateEmoji(card.slug, card.title);
        if (newEmoji) {
          card.meta = card.meta.map(m =>
            m.includes('🍽️') ? m.replace('🍽️', newEmoji) : m
          );
          stats.emojisFixed++;
          modified = true;
        }
      }
    }
  }

  // --- Fix 2: Remove duplicate slugs ---
  for (const section of data.sections) {
    if (!section.cards) continue;
    const seen = new Set();
    const originalCount = section.cards.length;
    section.cards = section.cards.filter(card => {
      if (seen.has(card.slug)) {
        stats.duplicatesRemoved++;
        modified = true;
        return false;
      }
      seen.add(card.slug);
      return true;
    });
  }

  // --- Fix 3: Long titles ---
  for (const section of data.sections) {
    for (const card of (section.cards || [])) {
      if (MANUAL_TITLE_FIXES[card.slug]) {
        const newTitle = MANUAL_TITLE_FIXES[card.slug];
        if (card.title !== newTitle) {
          if (card.imageAlt === card.title) {
            card.imageAlt = newTitle;
          }
          card.title = newTitle;
          stats.titlesFixed++;
          modified = true;
        }
      }
    }
  }

  // --- Fix 4: Populate hero.meta ---
  if (data.hero && (!data.hero.meta || data.hero.meta.length === 0)) {
    const totalGuides = data.sections.reduce((sum, s) => sum + (s.cards || []).length, 0);
    const totalCities = data.sections.length;
    if (totalGuides > 0) {
      data.hero.meta = [
        `📋 ${totalGuides} curated guide${totalGuides !== 1 ? 's' : ''}`,
        `🏙️ ${totalCities} ${totalCities !== 1 ? 'areas' : 'area'}`,
      ];
      stats.heroMetaPopulated++;
      modified = true;
    }
  }

  // --- Fix 5: Populate publishedTime/modifiedTime ---
  if (data.seo) {
    if (!data.seo.publishedTime) {
      data.seo.publishedTime = '2026-01-15T00:00:00Z';
      stats.datesPopulated++;
      modified = true;
    }
    if (!data.seo.modifiedTime) {
      data.seo.modifiedTime = '2026-04-04T00:00:00Z';
      stats.datesPopulated++;
      modified = true;
    }
  }

  // --- Fix 6: Clean up empty Twitter meta ---
  if (data.seo) {
    if (data.seo.twitterTitle === '') {
      delete data.seo.twitterTitle;
      stats.twitterCleaned++;
      modified = true;
    }
    if (data.seo.twitterDescription === '') {
      delete data.seo.twitterDescription;
      stats.twitterCleaned++;
      modified = true;
    }
  }

  // --- Write ---
  if (modified) {
    stats.filesModified++;
    if (!DRY_RUN) {
      fs.writeFileSync(filepath, JSON.stringify(data, null, 2) + '\n');
    }
  }
}

// Process all hubs
const files = fs.readdirSync(HUB_DIR).filter(f => f.endsWith('.json'));
for (const f of files) {
  processHub(path.join(HUB_DIR, f));
}

console.log(`\n=== ROUND 2 FIXES (${DRY_RUN ? 'DRY RUN' : 'APPLIED'}) ===\n`);
console.log(`Files modified: ${stats.filesModified}/${files.length}`);
console.log(`Emojis fixed: ${stats.emojisFixed}`);
console.log(`Duplicates removed: ${stats.duplicatesRemoved}`);
console.log(`Titles fixed: ${stats.titlesFixed}`);
console.log(`Hero meta populated: ${stats.heroMetaPopulated}`);
console.log(`Dates populated: ${stats.datesPopulated}`);
console.log(`Twitter fields cleaned: ${stats.twitterCleaned}`);
