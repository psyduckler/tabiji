#!/usr/bin/env node
/**
 * add-related-links.js
 * Injects a "Related Attractions" section into each tabiji popular-picks article.
 *
 * Usage:
 *   node tabiji/functions/add-related-links.js              # update ALL articles
 *   node tabiji/functions/add-related-links.js <slug>       # update ONE article
 *
 * e.g.: node tabiji/functions/add-related-links.js shinjuku-cheap-restaurants
 */

'use strict';

const fs   = require('fs');
const path = require('path');

const PICKS_DIR     = path.resolve(__dirname, '../popular-picks');
const INDEX_HTML    = path.join(PICKS_DIR, 'index.html');
const METADATA_FILE = path.join(PICKS_DIR, 'picks-metadata.json');

// ─── City mapping ─────────────────────────────────────────────────────────────
// Slug prefix → parent city. Longer keys are matched first (see inferCity()).
const CITY_MAP = {
  // Tokyo area
  'shinjuku':       'Tokyo',
  'shibuya':        'Tokyo',
  'asakusa':        'Tokyo',
  'shimokitazawa':  'Tokyo',
  'tokyo':          'Tokyo',
  // Other Japan
  'kyoto':          'Kyoto',
  'osaka':          'Osaka',
  // France
  'paris':          'Paris',
  'le-marais':      'Paris',
  // Italy
  'rome':           'Rome',
  'trastevere':     'Rome',
  'milan':          'Milan',
  // Thailand
  'bangkok':        'Bangkok',
  'yaowarat':       'Bangkok',
  'chiang-mai':     'Chiang Mai',
  // Spain
  'barcelona':      'Barcelona',
  'el-born':        'Barcelona',
  'madrid':         'Madrid',
  // UK
  'london':         'London',
  'soho':           'London',
  // Mexico
  'mexico-city':    'Mexico City',
  'roma-condesa':   'Mexico City',
  'tulum':          'Tulum',
  'oaxaca':         'Oaxaca',
  // Bali
  'canggu':         'Bali',
  'ubud':           'Bali',
  'bali':           'Bali',
  // South America
  'buenos-aires':   'Buenos Aires',
  'bogota':         'Bogotá',
  'cartagena':      'Cartagena',
  'lima':           'Lima',
  // South-east Asia
  'singapore':      'Singapore',
  'penang':         'Penang',
  'manila':         'Manila',
  'hanoi':          'Hanoi',
  'ho-chi-minh':    'Ho Chi Minh City',
  'hong-kong':      'Hong Kong',
  'taipei':         'Taipei',
  // Korea
  'seoul':          'Seoul',
  // Portugal
  'lisbon':         'Lisbon',
  'porto':          'Porto',
  // Turkey
  'istanbul':       'Istanbul',
  // Morocco
  'marrakech':      'Marrakech',
  'fez':            'Fez',
  // Middle East
  'tel-aviv':       'Tel Aviv',
  'amman':          'Amman',
  // Africa
  'cairo':          'Cairo',
  'cape-town':      'Cape Town',
  'kingston':       'Kingston',
  // Europe
  'amsterdam':      'Amsterdam',
  'budapest':       'Budapest',
  'prague':         'Prague',
  'athens':         'Athens',
  'santorini':      'Santorini',
  'copenhagen':     'Copenhagen',
  // Americas
  'new-york':       'New York',
  'new-orleans':    'New Orleans',
  // India
  'delhi':          'Delhi',
};

// ─── Infer city from slug ─────────────────────────────────────────────────────
function inferCity(slug) {
  const parts = slug.split('-');
  // Try longest prefix first
  for (let len = parts.length - 1; len >= 1; len--) {
    const prefix = parts.slice(0, len).join('-');
    if (CITY_MAP[prefix]) return CITY_MAP[prefix];
  }
  return slug; // fallback
}

// ─── Infer category from slug + badge ────────────────────────────────────────
function inferCategory(slug, badge = '') {
  const t = (slug + ' ' + badge).toLowerCase();

  if (/surf\b|day.hike|hike|hiking/.test(t))                                   return 'outdoor/nature';
  if (/rooftop.pool|rooftop-pool/.test(t))                                     return 'rooftop pools';
  if (/rooftop/.test(t))                                                        return 'rooftop bars';
  if (/temple|shrine|museum|heritage|hammam|massage|bookshop|viewpoint|sunset/.test(t)) return 'culture/experiences';
  if (/jazz.bar|jazz.club|jazz-bar|jazz-club/.test(t))                         return 'jazz/music bars';
  if (/ruin.bar|ruin-bar|craft.beer|craft-beer/.test(t))                       return 'bars/drinks';
  if (/wine.bar|wine-bar/.test(t))                                              return 'wine bars';
  if (/mezcal|cocktail|pub|izakaya|aperitivo/.test(t))                         return 'bars/drinks';
  if (/beer/.test(t))                                                           return 'bars/drinks';
  if (/beach.club|beach-club|beach/.test(t))                                   return 'beach clubs';
  if (/working.cafe|working-cafe|cowork/.test(t))                              return 'coffee/cafes';
  if (/coffee|cafe|kissaten/.test(t))                                           return 'coffee/cafes';
  if (/bakery|bakeries|croissant|pastry|patisserie|dessert|gelato|matcha|mochi|nata/.test(t)) return 'bakeries/desserts';
  if (/ramen|pho|noodle|khao.soi|khao-soi|udon/.test(t))                      return 'noodles';
  if (/street.food|street-food/.test(t))                                        return 'street food';
  if (/cheap.eat|cheap-eat|cheap.restaurant|cheap-restaurant|budget/.test(t))  return 'budget eats';
  if (/vintage|shopping|market/.test(t))                                        return 'shopping';
  return 'restaurants/food';
}

// ─── Deterministic "shuffle" seeded by source slug ───────────────────────────
function hashCode(str) {
  let h = 0;
  for (let i = 0; i < str.length; i++) h = (Math.imul(31, h) + str.charCodeAt(i)) | 0;
  return h;
}

function deterministicSort(arr, seed) {
  return [...arr].sort((a, b) => hashCode(seed + ':' + a.slug) - hashCode(seed + ':' + b.slug));
}

// ─── Parse all cards from the popular-picks index page ───────────────────────
function parseIndexCards() {
  const html  = fs.readFileSync(INDEX_HTML, 'utf8');
  const cards = {};

  // Split by pick-card anchors
  const pattern = /<a href="\/popular-picks\/([^/"]+)\/" class="pick-card">([\s\S]*?)(?=\n        <a href="\/popular-picks\/|<\/div>\s*\n<\/div>\s*\n\n<footer)/g;
  let m;
  while ((m = pattern.exec(html)) !== null) {
    const slug  = m[1];
    const block = m[2];

    // Image – may be missing (some cards have no img)
    const imgM    = block.match(/<img src="([^"]+)"/);
    let heroImage = null;
    if (imgM) {
      const src = imgM[1];
      heroImage = src.startsWith('/') ? src : `/popular-picks/${src}`;
    }

    const badgeM = block.match(/class="card-badge">([^<]+)<\/span>/);
    const badge  = badgeM ? badgeM[1].trim() : '';

    const titleM = block.match(/<h3>([^<]+)<\/h3>/);
    const title  = titleM ? titleM[1].trim() : '';

    const descM  = block.match(/<p>([^<]+)<\/p>/);
    const desc   = descM ? descM[1].trim() : '';

    // Collect all <span> inside card-meta
    const metaM = block.match(/class="card-meta">([\s\S]*?)<\/div>/);
    const metaSpans = metaM
      ? (metaM[1].match(/<span>[^<]*<\/span>/g) || [])
      : [];

    cards[slug] = {
      slug,
      title,
      description: desc,
      heroImage,
      badge,
      metaSpans,
      city:     inferCity(slug),
      category: inferCategory(slug, badge),
    };
  }
  return cards;
}

// ─── Emoji badge for non-indexed articles ─────────────────────────────────────
const CATEGORY_EMOJI = {
  'noodles':             '🍜',
  'coffee/cafes':        '☕',
  'bars/drinks':         '🍺',
  'wine bars':           '🍷',
  'jazz/music bars':     '🎺',
  'bakeries/desserts':   '🥐',
  'street food':         '🍢',
  'budget eats':         '🍽️',
  'rooftop bars':        '🍸',
  'rooftop pools':       '🏊',
  'beach clubs':         '🏖️',
  'culture/experiences': '⛩️',
  'outdoor/nature':      '🥾',
  'shopping':            '🛍️',
  'restaurants/food':    '🍽️',
};

// ─── Parse metadata from an article's own HTML (for non-index articles) ───────
function parseArticleHtml(slug) {
  const file = path.join(PICKS_DIR, slug, 'index.html');
  if (!fs.existsSync(file)) return null;

  // Strip any existing related section before parsing to avoid grabbing
  // images from a prior injection
  let html = fs.readFileSync(file, 'utf8');
  html = html.replace(/<!-- RELATED_ATTRACTIONS -->[\s\S]*?<!-- \/RELATED_ATTRACTIONS -->/g, '');

  // Title
  let title = '';
  const ogT = html.match(/<meta property="og:title" content="([^"]+)"/);
  if (ogT) {
    title = ogT[1]
      .replace(/ — tabiji\.ai$/, '')
      .replace(/ \| tabiji\.ai$/, '')
      .replace(/ 2026$/, '')
      .replace(/ — Reddit-Backed Guide$/, '')
      .trim();
  }
  if (!title) {
    const titleTag = html.match(/<title>([^<]+)<\/title>/);
    if (titleTag) title = titleTag[1].replace(/ [—|].*/, '').trim();
  }
  if (!title) {
    const h1 = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/);
    if (h1) title = h1[1].replace(/<[^>]+>/g, '').trim();
  }

  // Description
  const descM = html.match(/<meta name="description" content="([^"]+)"/);
  const description = descM ? descM[1].trim() : '';

  // Hero image: og:image → first non-logo <img> in body → first image file in dir
  let heroImage = null;
  const ogImg = html.match(/<meta property="og:image" content="([^"]+)"/);
  if (ogImg) {
    heroImage = ogImg[1].replace(/^https:\/\/tabiji\.ai/, '');
  }
  if (!heroImage) {
    for (const img of html.matchAll(/<img src="([^"]+\.(?:jpg|jpeg|webp|png))"/gi)) {
      const src = img[1];
      // Skip nav logo, icons, and absolute paths to OTHER pick directories
      if (src.includes('logo') || src.includes('icon')) continue;
      if (src.startsWith('/popular-picks/') && !src.startsWith(`/popular-picks/${slug}/`)) continue;
      heroImage = src.startsWith('/') ? src : `/popular-picks/${slug}/${src}`;
      break;
    }
  }
  if (!heroImage) {
    const dir   = path.join(PICKS_DIR, slug);
    const files = fs.readdirSync(dir).filter(f => /\.(jpg|jpeg|webp|png)$/i.test(f));
    if (files.length) heroImage = `/popular-picks/${slug}/${files[0]}`;
  }

  // Generate a badge with emoji from city + category
  const city     = inferCity(slug);
  const category = inferCategory(slug);
  const emoji    = CATEGORY_EMOJI[category] || '📍';
  const badge    = `${emoji} ${city}`;

  return {
    slug,
    title,
    description,
    heroImage,
    badge,
    metaSpans: ['<span>🗺️ Interactive Map</span>'],
    city,
    category,
  };
}

// ─── Collect slugs from filesystem ───────────────────────────────────────────
function getAllSlugs() {
  return fs.readdirSync(PICKS_DIR)
    .filter(d => {
      if (d === 'index.html' || d === 'picks-metadata.json' || d === 'hero-bg.png') return false;
      const full = path.join(PICKS_DIR, d);
      return fs.statSync(full).isDirectory() && fs.existsSync(path.join(full, 'index.html'));
    })
    .sort();
}

// ─── Build metadata index ─────────────────────────────────────────────────────
function buildMetadata() {
  const indexCards = parseIndexCards();
  const allSlugs   = getAllSlugs();
  const metadata   = {};

  for (const slug of allSlugs) {
    if (indexCards[slug]) {
      metadata[slug] = indexCards[slug];
    } else {
      const article = parseArticleHtml(slug);
      if (article) metadata[slug] = article;
    }
  }
  return metadata;
}

// ─── Select 3 related articles ────────────────────────────────────────────────
function selectRelated(slug, metadata) {
  const current    = metadata[slug];
  const candidates = Object.values(metadata).filter(m => m.slug !== slug);

  const sameCity       = candidates.filter(m => m.city === current.city);
  const sameCatDiffCity = candidates.filter(m => m.category === current.category && m.city !== current.city);
  const rest           = candidates.filter(m => m.city !== current.city && m.category !== current.category);

  const selected = [];

  // 1. Up to 2 same-city
  const sortedSameCity = deterministicSort(sameCity, slug);
  selected.push(...sortedSameCity.slice(0, 2));

  // 2. 1 same-category from different city
  if (selected.length < 3) {
    const sortedSameCat = deterministicSort(sameCatDiffCity, slug);
    const remaining = sortedSameCat.filter(m => !selected.find(s => s.slug === m.slug));
    selected.push(...remaining.slice(0, 3 - selected.length));
  }

  // 3. Fill any gaps from any remaining candidates
  if (selected.length < 3) {
    const sortedRest = deterministicSort(rest, slug);
    const remaining  = sortedRest.filter(m => !selected.find(s => s.slug === m.slug));
    selected.push(...remaining.slice(0, 3 - selected.length));
  }

  // 4. Final fallback: any candidate (in case city+category combos are thin)
  if (selected.length < 3) {
    const allSorted  = deterministicSort(candidates, slug);
    const remaining  = allSorted.filter(m => !selected.find(s => s.slug === m.slug));
    selected.push(...remaining.slice(0, 3 - selected.length));
  }

  return selected.slice(0, 3);
}

// ─── HTML helpers ─────────────────────────────────────────────────────────────
function esc(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/"/g, '&quot;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

// ─── Build a single related card ─────────────────────────────────────────────
function buildCard(article) {
  const { slug, title, description, heroImage, badge, metaSpans } = article;

  const imgSrc   = heroImage || '';
  const imgHtml  = imgSrc
    ? `\n    <img src="${esc(imgSrc)}" alt="${esc(title)}" loading="lazy" style="width:100%;height:180px;object-fit:cover;display:block;">`
    : '';

  const metaHtml = (metaSpans && metaSpans.length)
    ? metaSpans.join('')
    : '<span>🗺️ Interactive Map</span>';

  return `<a href="/popular-picks/${slug}/" style="background:#FEFCF9;border:1px solid #E8DFD0;border-radius:14px;overflow:hidden;text-decoration:none;color:inherit;display:block;transition:transform 0.15s,box-shadow 0.15s;" onmouseenter="this.style.transform='translateY(-3px)';this.style.boxShadow='0 8px 30px rgba(0,0,0,0.08)'" onmouseleave="this.style.transform='';this.style.boxShadow=''">${imgHtml}
    <div style="padding:1.25rem 1.5rem 1.5rem;">
        <span style="display:inline-block;background:#E8DFD0;color:#8B7355;padding:0.2rem 0.6rem;border-radius:100px;font-size:0.78rem;font-weight:500;margin-bottom:0.5rem;">${badge}</span>
        <h3 style="font-size:1.15rem;font-weight:700;color:#2D3A5C;margin-bottom:0.35rem;">${esc(title)}</h3>
        <p style="font-size:0.9rem;color:#6B5D4F;">${esc(description)}</p>
        <div style="margin-top:0.75rem;font-size:0.8rem;color:#8B7355;display:flex;gap:1.2rem;flex-wrap:wrap;">${metaHtml}</div>
    </div>
</a>`;
}

// ─── Build the full "Related Attractions" section ────────────────────────────
function buildSection(relatedArticles) {
  const cards = relatedArticles.map(buildCard).join('\n        ');

  return `<!-- RELATED_ATTRACTIONS -->
<style>
@media (max-width:900px) { .related-grid { grid-template-columns: repeat(2,1fr) !important; } }
@media (max-width:560px) { .related-grid { grid-template-columns: 1fr !important; } }
</style>
<section style="max-width:900px;margin:3rem auto;padding:0 2rem 3rem;">
    <h2 style="font-size:1.3rem;font-weight:700;color:#2D3A5C;margin-bottom:1rem;padding-bottom:0.5rem;border-bottom:2px solid #E8DFD0;">Related Attractions</h2>
    <div class="related-grid" style="display:grid;gap:1.25rem;grid-template-columns:repeat(3,1fr);">
        ${cards}
    </div>
</section>
<!-- /RELATED_ATTRACTIONS -->`;
}

// ─── Inject or replace section in article HTML ───────────────────────────────
function injectRelated(slug, relatedArticles) {
  const file = path.join(PICKS_DIR, slug, 'index.html');
  let html   = fs.readFileSync(file, 'utf8');

  const section = buildSection(relatedArticles);

  // Remove existing section (idempotent)
  if (html.includes('<!-- RELATED_ATTRACTIONS -->')) {
    html = html.replace(/<!-- RELATED_ATTRACTIONS -->[\s\S]*?<!-- \/RELATED_ATTRACTIONS -->/g, '');
    // Clean up any double blank lines near </body>
    html = html.replace(/\n{3,}(<\/body>)/g, '\n\n$1');
  }

  // Inject before </body>
  html = html.replace('</body>', `\n${section}\n</body>`);

  fs.writeFileSync(file, html, 'utf8');
}

// ─── Main ─────────────────────────────────────────────────────────────────────
function main() {
  const targetSlug = process.argv[2] || null;

  console.log('📚 Building metadata index...');
  const metadata = buildMetadata();
  const count    = Object.keys(metadata).length;

  // Save metadata JSON
  fs.writeFileSync(METADATA_FILE, JSON.stringify(metadata, null, 2), 'utf8');
  console.log(`💾 Saved picks-metadata.json (${count} articles)\n`);

  const slugs = targetSlug
    ? (metadata[targetSlug] ? [targetSlug] : [])
    : Object.keys(metadata).sort();

  if (targetSlug && !metadata[targetSlug]) {
    console.error(`❌  Unknown slug: "${targetSlug}"`);
    process.exit(1);
  }

  for (const slug of slugs) {
    const related = selectRelated(slug, metadata);
    if (related.length < 3) {
      console.warn(`⚠️  Only ${related.length} related found for ${slug}`);
    }
    injectRelated(slug, related);

    const relatedSlugs = related.map(r => r.slug).join(', ');
    console.log(`✅  ${slug}`);
    console.log(`    → ${relatedSlugs}`);
  }

  console.log(`\n🎉  Done! Updated ${slugs.length} article(s).`);
}

main();
