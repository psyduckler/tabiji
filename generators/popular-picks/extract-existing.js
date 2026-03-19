const fs = require('fs');
const path = require('path');
const { writeText } = require('./utils');

function matchOne(html, regex) {
  const match = html.match(regex);
  if (!match) return null;
  const value = match[1] !== undefined ? match[1] : match[0];
  return value != null ? String(value).trim() : null;
}

function stripTags(value = '') {
  return String(value)
    .replace(/<br\s*\/?>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function decodeBasicEntities(value = '') {
  const decoded = String(value)
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&nbsp;/g, ' ')
    .trim();
  return decoded === 'null' ? '' : decoded;
}

function extractJsonLdBlocks(html) {
  const blocks = [];
  const regex = /<script type="application\/ld\+json">\s*([\s\S]*?)\s*<\/script>/g;
  let match;
  while ((match = regex.exec(html))) {
    try {
      blocks.push(JSON.parse(match[1]));
    } catch {
      blocks.push({ parseError: true, raw: match[1].slice(0, 500) });
    }
  }
  return blocks;
}

function parseHours(block = '') {
  const entries = [...block.matchAll(/<span>(Mon|Tue|Wed|Thu|Fri|Sat|Sun)<\/span><span>(.*?)<\/span>/g)]
    .map((m) => `${m[1]}: ${stripTags(m[2])}`);
  return entries.length ? entries.join('; ') : null;
}

function extractFaqFromJsonLd(blocks = []) {
  const faq = blocks.find((block) => block['@type'] === 'FAQPage');
  if (!faq?.mainEntity) return [];
  return faq.mainEntity.map((item) => ({
    question: item.name,
    answer: item.acceptedAnswer?.text || '',
  }));
}

function extractSummaryFromTouristTrip(blocks = []) {
  const trip = blocks.find((block) => block['@type'] === 'TouristTrip');
  const props = Object.fromEntries((trip?.additionalProperty || []).map((item) => [item.name, item.value]));
  return props;
}

function extractItemListFromJsonLd(blocks = []) {
  const list = blocks.find((block) => block['@type'] === 'ItemList');
  return list?.itemListElement || [];
}

function pickAddressLocality(item) {
  return item?.item?.address?.addressLocality || null;
}

function detectVertical(slug, html, heroBadge = '', picks = []) {
  const text = `${slug} ${heroBadge} ${html.slice(0, 4000)}`.toLowerCase();
  const names = picks.map((pick) => `${pick.name} ${(pick.cuisineTags || []).join(' ')}`.toLowerCase()).join(' ');
  const combined = `${text} ${names}`;
  if (/(restaurant|restaurants|shawarma|coffee|cafe|brunch|eat|food|jollof|ramen|yatai)/.test(slug.toLowerCase())) return 'restaurants-food';
  if (/(hotel|stay|stays|hostel|villa|resort|ryokan|hanok)/.test(combined)) return 'lodging';
  if (/(hiking|snorkeling|dive|beach|trek|trail|climb|safari|kayak|surf|pool)/.test(combined)) return 'activities';
  if (/(shop|shopping|market|souvenir|mall|boutique)/.test(combined)) return 'shopping';
  if (/(country|region|island|guide to|where to go|best of)/.test(combined) && picks.length < 5) return 'destination-overview';
  if (/(restaurant|shawarma|coffee|cafe|brunch|eat|food|jollof|ramen|yatai)/.test(combined)) return 'restaurants-food';
  return 'mixed';
}

function detectCategory(slug, vertical) {
  const lower = slug.toLowerCase();
  if (vertical === 'lodging') return 'lodging';
  if (vertical === 'shopping') return 'shopping';
  if (vertical === 'activities') return 'activities';
  if (vertical === 'destination-overview') return 'destination';
  if (lower.includes('coffee')) return 'coffee shops';
  if (lower.includes('shawarma')) return 'shawarma';
  if (lower.includes('restaurants')) return 'restaurants';
  if (lower.includes('jollof')) return 'jollof rice';
  return 'restaurants/food';
}

function inferPlaceType(vertical, cuisine = '') {
  if (vertical === 'lodging') return 'lodging';
  if (vertical === 'activities') return 'activity';
  if (vertical === 'shopping') return 'shop';
  if (/coffee|cafe/i.test(cuisine)) return 'cafe';
  if (/bar|pub|rooftop/i.test(cuisine)) return 'bar';
  if (/market/i.test(cuisine)) return 'market';
  return 'restaurant';
}

function extractQuotes(block = '') {
  return [...block.matchAll(/<div class="reddit-quote">\s*"([\s\S]*?)"\s*<span class="source">([\s\S]*?)<\/span>/g)].map((m) => ({
    quote: decodeBasicEntities(stripTags(m[1])),
    source: decodeBasicEntities(stripTags(m[2])),
  }));
}

function buildGenericSection(sectionId, rank, name, block, opts = {}) {
  const verticalHint = opts.verticalHint || 'restaurants-food';
  const cuisine = decodeBasicEntities(stripTags(matchOne(block, opts.cuisineRegex || /<span class="cuisine-tag [^"]+">(.*?)<\/span>/s) || ''));
  const rating = matchOne(block, /<span class="google-rating"><span class="star">★<\/span> ([0-9.]+)/);
  const reviewCount = matchOne(block, /· ([0-9,]+) reviews/);
  const priceRangeLocal = decodeBasicEntities(stripTags(matchOne(block, /<span>[^<]*[₵$¥£€₩¥][^<]*<\/span>/s) || matchOne(block, /<span>[💴💰]\s*(.*?)<\/span>/s) || '')).replace(/^[^₵$¥£€₩¥0-9]+/, '');
  const address = decodeBasicEntities(stripTags(matchOne(block, opts.addressRegex || /<span>📍 (.*?)<\/span>/s) || ''));
  const googleMapsUrl = decodeBasicEntities(matchOne(block, /<a href="([^"]+)" target="_blank" rel="noopener">📌 Google Maps →<\/a>/));
  const phone = decodeBasicEntities(matchOne(block, /tel:([^"]+)/));
  const website = decodeBasicEntities(matchOne(block, /🌐 <a href="([^"]+)"/));
  const photo = decodeBasicEntities(matchOne(block, opts.photoRegex || /<img[^>]+src="([^"]+)"/));
  const whatToOrder = decodeBasicEntities(stripTags(matchOne(block, opts.whatRegex || /<div class="what-to-order">\s*<strong>What to order:<\/strong>(.*?)<\/div>/s) || matchOne(block, /<div class="what-to-expect">\s*<strong>What to expect:<\/strong>(.*?)<\/div>/s) || '')).replace(/^What to (order|expect):\s*/i, '').trim();
  const verdict = decodeBasicEntities(stripTags(matchOne(block, opts.verdictRegex || /<div class="tabiji-verdict">\s*<strong>tabiji verdict:<\/strong>(.*?)<\/div>/s) || /<div class="verdict">\s*<strong>The Verdict:<\/strong>(.*?)<\/div>/s || ''));
  const quotes = extractQuotes(block);

  return {
    sectionId,
    rank,
    name,
    placeType: inferPlaceType(verticalHint, cuisine),
    neighborhood: address || null,
    address: address || null,
    priceRangeLocal: priceRangeLocal || null,
    googleRating: rating ? Number(rating) : null,
    reviewCount: reviewCount ? Number(reviewCount.replace(/,/g, '')) : null,
    googleMapsUrl: googleMapsUrl || null,
    website: website || null,
    phone: phone || null,
    photo: photo || null,
    cuisineTags: cuisine ? [cuisine] : [],
    knownForTags: cuisine ? [cuisine] : [],
    whyItMadeTheList: verdict || `${name} appears as a featured pick in the existing HTML page.`,
    whatToOrder: whatToOrder || `${name} is a featured pick in this guide.`,
    insiderTip: verdict || `${name} is worth reviewing manually after extraction.`,
    redditQuotes: quotes,
    hoursNote: parseHours(block),
    editorialFlags: {
      openNow: /🕐 Open now/.test(block) ? true : /🕐 Closed now/.test(block) ? false : undefined,
    },
    provenance: {
      sourceCount: quotes.length || undefined,
      sourceTypes: quotes.length ? ['reddit', 'legacy-html'] : ['legacy-html'],
      lastVerified: null,
      confidence: 'low',
      matchMethod: 'html-extraction',
    },
  };
}

function extractRestaurantSections(html, verticalHint = 'restaurants-food') {
  const regex = /<section class="restaurant-section" id="([^"]+)">([\s\S]*?)(?=<section class="restaurant-section"|<section class="faq-section")/g;
  const sections = [];
  let match;
  while ((match = regex.exec(html))) {
    const sectionId = match[1];
    const block = match[2];
    const rank = Number(matchOne(block, /<h2><span class="restaurant-number">(\d+)<\/span>/));
    const name = decodeBasicEntities(stripTags(matchOne(block, /<h2><span class="restaurant-number">\d+<\/span>(.*?)<\/h2>/s) || ''));
    sections.push(buildGenericSection(sectionId, rank, name, block, { verticalHint }));
  }
  return sections;
}

function extractPickSections(html, verticalHint = 'restaurants-food') {
  const regex = /<section class="pick-section" id="([^"]+)">([\s\S]*?)(?=<section class="pick-section"|<section class="faq-section")/g;
  const sections = [];
  let match;
  while ((match = regex.exec(html))) {
    const sectionId = match[1];
    const block = match[2];
    const rank = Number(matchOne(block, /<div class="pick-number"[^>]*>(\d+)<\/div>/));
    const name = decodeBasicEntities(stripTags(matchOne(block, /<h2>(.*?)<small>/s) || matchOne(block, /<h2>(.*?)<\/h2>/s) || ''));
    sections.push(buildGenericSection(sectionId, rank, name, block, {
      verticalHint,
      cuisineRegex: /<div class="pick-meta">[\s\S]*?<span>(.*?)<\/span>/s,
      photoRegex: /<img class="pick-img" src="([^"]+)"/,
      verdictRegex: /<div class="verdict">\s*<strong>The Verdict:<\/strong>(.*?)<\/div>/s,
    }));
  }
  return sections;
}

function extractStaySections(html, verticalHint = 'lodging') {
  const regex = /<section class="stay-section" id="([^"]+)">([\s\S]*?)(?=<section class="stay-section"|<section class="faq-section")/g;
  const sections = [];
  let match;
  while ((match = regex.exec(html))) {
    const sectionId = match[1];
    const block = match[2];
    const rank = Number(matchOne(block, /<h2><span class="stay-number">(\d+)<\/span>/));
    const name = decodeBasicEntities(stripTags(matchOne(block, /<h2><span class="stay-number">\d+<\/span>(.*?)<\/h2>/s) || ''));
    sections.push(buildGenericSection(sectionId, rank, name, block, {
      verticalHint,
      cuisineRegex: /<span class="style-tag [^"]+">(.*?)<\/span>/s,
      addressRegex: /<span>📍 (.*?)<\/span>/s,
      whatRegex: /<div class="what-to-expect">\s*<strong>What to expect:<\/strong>(.*?)<\/div>/s,
    }));
  }
  return sections;
}

function extractSections(html, verticalHint = 'restaurants-food') {
  if (/class="restaurant-section"/.test(html)) return extractRestaurantSections(html, verticalHint);
  if (/class="pick-section"/.test(html)) return extractPickSections(html, verticalHint);
  if (/class="stay-section"/.test(html)) return extractStaySections(html, verticalHint);
  return [];
}

function buildSourceJson(html, slug) {
  const jsonLd = extractJsonLdBlocks(html);
  const article = jsonLd.find((block) => block['@type'] === 'Article') || {};
  const itemList = extractItemListFromJsonLd(jsonLd);
  const faq = extractFaqFromJsonLd(jsonLd);
  const tripProps = extractSummaryFromTouristTrip(jsonLd);
  const heroBadge = stripTags(matchOne(html, /<div class="hero-badge">([\s\S]*?)<\/div>/s) || '');
  let sections = extractSections(html);
  const vertical = detectVertical(slug, html, heroBadge, sections);
  const category = detectCategory(slug, vertical);
  sections = extractSections(html, vertical);

  const heroDek = stripTags(matchOne(html, /<p class="subtitle">([\s\S]*?)<\/p>/s) || matchOne(html, /<div class="hero">[\s\S]*?<p>([\s\S]*?)<\/p>/s) || '');
  const heroMeta = [...html.matchAll(/<div class="hero-meta">([\s\S]*?)<\/div>/g)][0];
  const heroMetaHtml = heroMeta?.[1] || '';
  const heroMetaSpans = heroMetaHtml
    ? (() => {
        const spans = [...heroMetaHtml.matchAll(/<span[^>]*>([\s\S]*?)<\/span>/g)].map((m) => stripTags(m[1]));
        if (spans.length) return spans;
        return [...heroMetaHtml.matchAll(/<div[^>]*><strong>(.*?)<\/strong>\s*(.*?)<\/div>/g)].map((m) => `${stripTags(m[1])} ${stripTags(m[2])}`);
      })()
    : [];
  const introSectionMatch = html.match(/<(section|div) class="intro-section">([\s\S]*?)<\/(section|div)>/);
  const introStrong = introSectionMatch ? stripTags(matchOne(introSectionMatch[2], /<p><strong>([\s\S]*?)<\/strong><\/p>/s) || '') : '';
  const introBody = introSectionMatch ? [...introSectionMatch[2].matchAll(/<p>([\s\S]*?)<\/p>/g)].map((m) => stripTags(m[1])).filter(Boolean).slice(introStrong ? 1 : 0) : [];
  const methodology = stripTags(matchOne(html, /How we built this list[\s\S]*?<p[^>]*>([\s\S]*?)<\/p>/s) || matchOne(html, /<section class="methodology-section">[\s\S]*?<p>([\s\S]*?)<\/p>[\s\S]*?<\/section>/s) || '');
  const canonical = matchOne(html, /<link rel="canonical" href="([^"]+)">/i) || `https://tabiji.ai/popular-picks/${slug}/`;
  const canonicalPath = canonical.replace('https://tabiji.ai', '');
  const ogImage = matchOne(html, /<meta property="og:image" content="([^"]+)">/i);
  const itemListName = decodeBasicEntities((jsonLd.find((block) => block['@type'] === 'ItemList') || {}).name || '');
  const locality = pickAddressLocality(itemList[0]) || '';
  const city = locality.split(',').pop()?.trim() || locality || stripTags(heroBadge).split('—').pop()?.trim() || '';

  return {
    slug,
    pageType: 'popular-picks',
    status: 'reviewed',
    taxonomy: {
      city: city || null,
      country: itemList[0]?.item?.address?.addressCountry || null,
      countryCode: itemList[0]?.item?.address?.addressCountry || null,
      category,
      vertical,
      badgeEmoji: heroBadge.split(' ')[0] || '🍽️',
    },
    seo: {
      title: decodeBasicEntities(article.headline || matchOne(html, /<title>(.*?)<\/title>/i) || ''),
      h1: stripTags(matchOne(html, /<h1[^>]*>(.*?)<\/h1>/i) || itemListName),
      metaTitle: decodeBasicEntities(matchOne(html, /<title>(.*?)<\/title>/i) || ''),
      metaDescription: decodeBasicEntities(matchOne(html, /<meta name="description" content="([^"]+)">/i) || article.description || ''),
      canonicalPath,
      ogTitle: decodeBasicEntities(matchOne(html, /<meta property="og:title" content="([^"]+)">/i) || ''),
      ogDescription: decodeBasicEntities(matchOne(html, /<meta property="og:description" content="([^"]+)">/i) || ''),
      twitterTitle: decodeBasicEntities(matchOne(html, /<meta name="twitter:title" content="([^"]+)">/i) || ''),
      twitterDescription: decodeBasicEntities(matchOne(html, /<meta name="twitter:description" content="([^"]+)">/i) || ''),
      heroImage: ogImage || null,
      publishedTime: matchOne(html, /<meta property="article:published_time" content="([^"]+)">/i) || null,
      modifiedTime: matchOne(html, /<meta property="article:modified_time" content="([^"]+)">/i) || null,
      robots: decodeBasicEntities(matchOne(html, /<meta name="robots" content="([^"]+)">/i) || 'index, follow, max-image-preview:large'),
    },
    hero: {
      eyebrow: heroBadge ? `Popular Picks — ${stripTags(heroBadge)}` : 'Popular Picks',
      title: stripTags(matchOne(html, /<h1[^>]*>(.*?)<\/h1>/i) || itemListName),
      dek: heroDek,
      badge: heroBadge,
      metaSpans: heroMetaSpans || [],
    },
    intro: {
      answerFirst: introStrong || article.description || '',
      body: introBody.length ? introBody : [article.description || ''],
      methodology: methodology || undefined,
    },
    summary: {
      totalOptions: sections.length,
      priceRangeLocal: tripProps.priceRangeLocal || null,
      priceRangeUSD: tripProps.priceRangeUSD || null,
      bestBudgetOption: tripProps.bestBudgetOption || null,
      bestLuxuryOption: tripProps.bestLuxuryOption || null,
      bestOverall: tripProps.bestOverall || null,
      topPick: tripProps.topPick || sections[0]?.name || null,
      sourcesAnalyzed: tripProps.sourcesAnalyzed || 'Extracted from existing HTML page',
      lastVerifiedLabel: tripProps.lastVerified || null,
    },
    map: {
      enabled: /map-sidebar|map-inline/.test(html),
      title: stripTags(matchOne(html, /<aside class="map-sidebar">[\s\S]*?<h2>(.*?)<\/h2>/s) || matchOne(html, /<div class="map-inline">[\s\S]*?<h2>(.*?)<\/h2>/s) || 'Area map'),
      embedUrl: matchOne(html, /<iframe src="([^"]+)"/i) || null,
      ctaLabel: /Open in Google Maps/.test(html) ? 'Open in Google Maps' : null,
      ctaUrl: null,
    },
    picks: sections,
    faq,
    related: {
      manual: [...html.matchAll(/<a href="\/popular-picks\/([^"/]+)\/"/g)].map((m) => m[1]).filter((value) => value !== slug).slice(0, 12),
      topics: [],
    },
    provenance: {
      researchStatus: 'extracted-from-html',
      sourceCount: sections.reduce((sum, pick) => sum + (pick?.provenance?.sourceCount || 0), 0),
      sourceTypes: ['legacy-html', 'reddit'],
      lastVerified: null,
      confidence: 'low',
      notes: 'Backfilled from an existing Popular Picks HTML page; requires editorial review before claiming clean structured provenance.',
      importedFromHtml: true,
    },
    verification: {
      lastVerified: tripProps.lastVerified || ((matchOne(html, /<meta property="article:modified_time" content="(\d{4}-\d{2})/i) || '').slice(0, 7)) || '2026-03',
      pipelineVersion: 'html-backfill-v3',
      reviewedByHuman: false,
    },
    publishing: {
      outputPath: `popular-picks/${slug}/index.html`,
      includeInMetadataIndex: true,
      includeInSitemap: true,
      includeInApiBuild: true,
    },
  };
}

function extractExisting(html, slug) {
  const title = matchOne(html, /<title>(.*?)<\/title>/i);
  const description = matchOne(html, /<meta name="description" content="(.*?)">/i);
  const canonical = matchOne(html, /<link rel="canonical" href="(.*?)">/i);
  const h1 = matchOne(html, /<h1[^>]*>(.*?)<\/h1>/i);
  const jsonLd = extractJsonLdBlocks(html);
  const sourceJson = buildSourceJson(html, slug);

  return {
    slug,
    extractedFromExistingHtml: true,
    title,
    description,
    canonical,
    h1,
    jsonLdTypes: jsonLd.map((item) => item['@type'] || 'unknown'),
    jsonLd,
    sourceJson,
    notes: [
      'This extractor is intended for backfill/bootstrap of structured source JSON from existing Popular Picks HTML.',
      'It captures section-level data, FAQ, metadata, and schema-derived summaries.',
      'Editorial cleanup is still required after extraction.',
    ],
  };
}

if (require.main === module) {
  const input = process.argv[2];
  const output = process.argv[3];
  if (!input || !output) {
    console.error('Usage: node generators/popular-picks/extract-existing.js <html-file> <output-json>');
    process.exit(1);
  }
  const html = fs.readFileSync(input, 'utf8');
  const slug = path.basename(path.dirname(input));
  const extracted = extractExisting(html, slug);
  writeText(output, `${JSON.stringify(extracted, null, 2)}\n`);
  console.log(`Extracted ${slug} -> ${output}`);
}

module.exports = {
  extractExisting,
  buildSourceJson,
  extractSections,
  extractJsonLdBlocks,
  detectVertical,
  detectCategory,
  extractRestaurantSections,
  extractPickSections,
  extractStaySections,
};
