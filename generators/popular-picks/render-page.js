#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { renderMeta, escapeHtml, absoluteUrl } = require('./render-meta');
const { renderSchema } = require('./render-schema');
const { loadJson, validateSource } = require('./validate-source');

const GOOGLE_MAPS_API_KEY = 'AIzaSyBP0yidMjJEECgkIiZz2lw1NLsQ7jdASYc';
const REPO_ROOT = path.resolve(__dirname, '..', '..');

let siteInventoryCache = null;

function readTextIfExists(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf8');
  } catch {
    return '';
  }
}

function titleFromSlug(slug = '') {
  return String(slug)
    .split('-')
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ');
}

function extractHtmlTitle(filePath, fallbackSlug = '') {
  const html = readTextIfExists(filePath);
  if (!html) return titleFromSlug(fallbackSlug);
  const h1 = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  if (h1) return h1[1].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
  const title = html.match(/<title>([\s\S]*?)<\/title>/i);
  if (title) return title[1].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
  return titleFromSlug(fallbackSlug);
}

function loadDirectoryEntries(dirPath, type, urlPrefix) {
  if (!fs.existsSync(dirPath)) return [];
  return fs.readdirSync(dirPath, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => {
      const slug = entry.name;
      const htmlPath = path.join(dirPath, slug, 'index.html');
      if (!fs.existsSync(htmlPath)) return null;
      return {
        type,
        slug,
        url: `${urlPrefix}/${slug}/`,
        title: extractHtmlTitle(htmlPath, slug),
        searchText: normalizeIntroText(`${slug} ${extractHtmlTitle(htmlPath, slug)}`),
      };
    })
    .filter(Boolean);
}

function getSiteInventory() {
  if (siteInventoryCache) return siteInventoryCache;
  siteInventoryCache = {
    destinations: loadDirectoryEntries(path.join(REPO_ROOT, 'destinations'), 'destination', '/destinations'),
    itineraries: loadDirectoryEntries(path.join(REPO_ROOT, 'itineraries'), 'itinerary', '/itineraries'),
    compares: loadDirectoryEntries(path.join(REPO_ROOT, 'compare'), 'compare', '/compare'),
    popularPicks: loadDirectoryEntries(path.join(REPO_ROOT, 'popular-picks'), 'popular-picks', '/popular-picks'),
  };
  return siteInventoryCache;
}

function renderRichTextParagraphs(items = []) {
  return items.map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`).join('');
}

function firstNonEmpty(...values) {
  for (const value of values) {
    if (typeof value === 'string' && value.trim()) return value.trim();
  }
  return '';
}

function normalizeIntroText(text = '') {
  return String(text)
    .toLowerCase()
    .normalize('NFKD')
    .replace(/[“”‘’]/g, "'")
    .replace(/[^a-z0-9\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

const INTRO_STOPWORDS = new Set([
  'about', 'after', 'also', 'among', 'and', 'are', 'around', 'because', 'been', 'being', 'best', 'between',
  'both', 'but', 'can', 'city', 'closest', 'from', 'good', 'guide', 'have', 'into', 'just', 'list', 'local',
  'more', 'most', 'near', 'offer', 'offers', 'often', 'only', 'over', 'page', 'people', 'person', 'places',
  'recommendation', 'recommendations', 'reddit', 'range', 'ranging', 'spot', 'spots', 'that', 'their', 'these',
  'they', 'this', 'those', 'through', 'top', 'travelers', 'travellers', 'very', 'when', 'where', 'with', 'your'
]);

function tokenSet(text = '') {
  return new Set(
    normalizeIntroText(text)
      .split(' ')
      .filter((token) => token.length >= 4 && !INTRO_STOPWORDS.has(token))
  );
}

function overlapRatio(a, b) {
  const aTokens = tokenSet(a);
  const bTokens = tokenSet(b);
  if (!aTokens.size || !bTokens.size) return 0;
  let overlap = 0;
  for (const token of aTokens) {
    if (bTokens.has(token)) overlap += 1;
  }
  return overlap / Math.min(aTokens.size, bTokens.size);
}

function firstSentence(text = '') {
  return String(text).split(/(?<=[.!?])\s+/)[0].trim();
}

function isDuplicateIntroParagraph(answerFirst = '', paragraph = '') {
  if (!answerFirst || !paragraph) return false;
  const normalizedAnswer = normalizeIntroText(answerFirst);
  const normalizedParagraph = normalizeIntroText(paragraph);
  const sharedRatio = overlapRatio(answerFirst, paragraph);
  const firstSentenceRatio = overlapRatio(firstSentence(answerFirst), firstSentence(paragraph));
  const containsOther = normalizedAnswer.includes(normalizedParagraph) || normalizedParagraph.includes(normalizedAnswer);
  const sameOpening = normalizedAnswer.slice(0, 140) && normalizedAnswer.slice(0, 140) === normalizedParagraph.slice(0, 140);

  return containsOther || sharedRatio >= 0.67 || firstSentenceRatio >= 0.72 || sameOpening;
}

function dedupeIntroBody(answerFirst = '', body = []) {
  if (!Array.isArray(body) || !body.length) return [];
  if (!answerFirst) return body;

  let index = 0;
  while (index < body.length && isDuplicateIntroParagraph(answerFirst, body[index])) {
    index += 1;
  }
  // Never strip every paragraph — keep at least the final one
  return body.slice(Math.min(index, body.length - 1));
}

function formatPhone(phone) {
  if (!phone) return '';
  return phone.replace(/\s+/g, ' ').trim();
}

function slugify(value = '') {
  return String(value)
    .toLowerCase()
    .normalize('NFKD')
    .replace(/[^-\x7F]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function parseHoursNote(hoursNote = '') {
  if (!hoursNote) return [];
  return hoursNote
    .split(';')
    .map((entry) => entry.trim())
    .filter(Boolean)
    .map((entry) => {
      const parts = entry.split(':');
      if (parts.length < 2) return null;
      const day = parts.shift().trim();
      const hours = parts.join(':').trim();
      return { day, hours };
    })
    .filter(Boolean);
}

function hoursSummary(pick, hours) {
  if (typeof pick?.editorialFlags?.openNow === 'boolean') {
    return pick.editorialFlags.openNow ? '🕐 Open now' : '🕐 Closed now';
  }
  if (hours.some((item) => /open 24 hours/i.test(item.hours))) return '🕐 Open now';
  return 'Hours';
}

function cuisineTagClass(pick) {
  const first = (pick.tags || [])[0] || '';
  const map = {
    ramen: 'tag-ramen',
    tonkatsu: 'tag-tonkatsu',
    tsukemen: 'tag-tsukemen',
    yakitori: 'tag-yakitori',
    tempura: 'tag-tempura',
    sushi: 'tag-sushi',
    gyukatsu: 'tag-gyukatsu',
    udon: 'tag-udon',
    gyudon: 'tag-gyudon',
    kushikatsu: 'tag-kushikatsu',
    shabu: 'tag-shabu',
    sukiyaki: 'tag-shabu',
    omurice: 'tag-omurice',
    hamburg: 'tag-hamburg',
    snack: 'tag-snack',
    sardine: 'tag-regional',
    washoku: 'tag-regional',
  };
  const key = first.toLowerCase();
  for (const token of Object.keys(map)) {
    if (key.includes(token)) return map[token];
  }
  return 'tag-regional';
}

function buildDerivedMap(data) {
  const h1Clean = (data.seo.h1 || '').replace(/^\d+\s+Best\s+/i, '').trim();
  const query = h1Clean || [data.taxonomy.neighborhood, data.taxonomy.city, data.taxonomy.category]
    .filter(Boolean)
    .join(' ');
  const ctaUrl = data.map?.ctaUrl || `https://www.google.com/maps/search/${encodeURIComponent(query)}`;
  return {
    enabled: data.map?.enabled !== false,
    title: data.map?.title || 'Area map',
    ctaLabel: data.map?.ctaLabel || 'Open in Google Maps',
    ctaUrl,
    fallbackQuery: query,
  };
}

function buildPickMapQuery(pick, data) {
  return [pick.name, pick.address || pick.neighborhood, data.taxonomy.city, data.taxonomy.countryCode || data.taxonomy.country]
    .filter(Boolean)
    .join(', ');
}

function renderHero(data) {
  return `
    <section class="hero">
      <div class="hero-badge">${escapeHtml(data.hero.badge)}</div>
      <h1>${escapeHtml(data.seo.h1)}</h1>
      <p class="subtitle">${escapeHtml(data.hero.dek)}</p>
      <div class="hero-meta">
        ${data.hero.metaSpans.map((item) => `<span>${escapeHtml(item)}</span>`).join('')}
      </div>
    </section>`;
}

function pickAnchorId(pick) {
  return pick.sectionId || slugify(pick.name);
}

function buildMapPicks(picks, data, mapData) {
  return picks
    .filter((pick) => typeof pick.lat === 'number' && typeof pick.lng === 'number')
    .map((pick) => ({
      anchorId: pickAnchorId(pick),
      rank: pick.rank,
      name: pick.name,
      label: `${pick.rank}. ${pick.name}`,
      lat: pick.lat,
      lng: pick.lng,
      ctaUrl: pick.googleMapsUrl || mapData.ctaUrl,
      mapQuery: buildPickMapQuery(pick, data),
    }));
}

function uniqueBy(items, keyFn) {
  const seen = new Set();
  const result = [];
  for (const item of items) {
    const key = keyFn(item);
    if (!key || seen.has(key)) continue;
    seen.add(key);
    result.push(item);
  }
  return result;
}

function buildIntentTokens(data) {
  const city = firstNonEmpty(data.taxonomy?.city, '');
  const country = firstNonEmpty(data.taxonomy?.country, '');
  const category = firstNonEmpty(data.taxonomy?.category, '');
  const slugParts = String(data.slug || '').split('-').filter(Boolean);
  const slugPhrases = [];
  if (slugParts.length >= 2) slugPhrases.push(slugParts.slice(0, 2).join(' '));
  if (slugParts.length >= 3) slugPhrases.push(slugParts.slice(0, 3).join(' '));
  const cuisineTokens = uniqueBy((data.picks || []).flatMap((pick) => (pick.tags || []).map((tag) => normalizeIntroText(tag))).filter(Boolean), (value) => value)
    .flatMap((value) => value.split(' '))
    .filter((token) => token.length >= 4);
  return uniqueBy([
    meaningfulToken(city),
    meaningfulToken(country),
    meaningfulToken(category),
    ...slugPhrases.map((value) => meaningfulToken(value)),
    ...cuisineTokens,
  ].filter(Boolean), (value) => value);
}

function meaningfulToken(value = '') {
  const normalized = normalizeIntroText(value);
  return normalized.length >= 4 ? normalized : '';
}

function countTokenMatches(searchText = '', tokens = []) {
  return tokens.reduce((count, token) => count + (searchText.includes(token) ? 1 : 0), 0);
}

function scoreEntry(entry, data, tokens, options = {}) {
  if (!entry || !entry.url || entry.slug === data.slug) return -Infinity;
  const text = entry.searchText || '';
  let score = countTokenMatches(text, tokens);
  const cityToken = meaningfulToken(data.taxonomy?.city || '');
  const countryToken = meaningfulToken(data.taxonomy?.country || '');
  const categoryToken = meaningfulToken(data.taxonomy?.category || '');
  const slugText = normalizeIntroText(entry.slug || '');
  const locationMatched = Boolean((cityToken && text.includes(cityToken)) || (countryToken && text.includes(countryToken)));

  if (cityToken && text.includes(cityToken)) score += 4;
  if (countryToken && text.includes(countryToken)) score += 2;
  if (categoryToken && text.includes(categoryToken)) score += 1;
  if (options.requireCity && cityToken && !text.includes(cityToken)) return -Infinity;
  if (options.requireCountry && countryToken && !text.includes(countryToken)) return -Infinity;
  if (options.requireLocation && !locationMatched) return -Infinity;
  if (options.excludeCategory && categoryToken && text.includes(categoryToken)) score -= 2;
  if (slugText.includes(normalizeIntroText(data.slug))) score -= 3;
  return score;
}

function pickTopEntries(entries, data, tokens, options = {}) {
  return entries
    .map((entry) => ({ entry, score: scoreEntry(entry, data, tokens, options) }))
    .filter(({ score }) => Number.isFinite(score) && score >= (options.minScore ?? 1))
    .sort((a, b) => b.score - a.score || a.entry.title.localeCompare(b.entry.title))
    .slice(0, options.limit || 3)
    .map(({ entry }) => entry);
}

function buildIntentLinks(data) {
  const inventory = getSiteInventory();
  const tokens = buildIntentTokens(data);
  const citySlug = slugify(data.taxonomy?.city || '');
  const countrySlug = slugify(data.taxonomy?.country || '');
  const slugParts = String(data.slug || '').split('-').filter(Boolean);
  const locationPhrases = uniqueBy([
    meaningfulToken(data.taxonomy?.city || ''),
    meaningfulToken(data.taxonomy?.country || ''),
    meaningfulToken(citySlug.replace(/-/g, ' ')),
    meaningfulToken(countrySlug.replace(/-/g, ' ')),
    ...(slugParts.length >= 2 ? [meaningfulToken(slugParts.slice(0, 2).join(' '))] : []),
    ...(slugParts.length >= 3 ? [meaningfulToken(slugParts.slice(0, 3).join(' '))] : []),
  ].filter(Boolean), (value) => value);
  const manualPopularPicks = new Set((data.related?.manual || []).map((slug) => `/popular-picks/${slug}/`));

  const directLocationEntries = (entries) => uniqueBy(entries.filter((entry) => locationPhrases.some((phrase) => (entry.searchText || '').includes(phrase))), (entry) => entry.url);

  const destinationMatches = uniqueBy([
    ...[citySlug, countrySlug].map((slug) => inventory.destinations.find((entry) => entry.slug === slug)).filter(Boolean),
    ...directLocationEntries(inventory.destinations),
  ], (entry) => entry.url).slice(0, 2);

  const hubMatches = uniqueBy([
    ...[citySlug, countrySlug].map((slug) => inventory.popularPicks.find((entry) => entry.slug === slug && entry.slug !== data.slug)).filter(Boolean),
    ...directLocationEntries(inventory.popularPicks.filter((entry) => entry.slug !== data.slug && !manualPopularPicks.has(entry.url))),
  ], (entry) => entry.url)
    .filter((entry) => !entry.slug.includes('-') || entry.slug === citySlug || entry.slug === countrySlug)
    .slice(0, 2);

  const itineraryMatches = pickTopEntries(inventory.itineraries, data, tokens, { limit: 3, minScore: 2, requireLocation: true });
  const compareMatches = pickTopEntries(inventory.compares, data, tokens, { limit: 3, minScore: 3, requireLocation: true });
  const adjacentPopularPicks = pickTopEntries(
    inventory.popularPicks.filter((entry) => !manualPopularPicks.has(entry.url) && entry.slug !== citySlug && entry.slug !== countrySlug),
    data,
    tokens,
    { limit: 4, minScore: 2, requireLocation: true, excludeCategory: true }
  );

  return [
    {
      key: 'destinations',
      title: `Plan ${data.taxonomy?.city || data.taxonomy?.country || 'this destination'}`,
      description: 'Broader destination guides and country hubs for travelers still shaping the trip around this pick list.',
      links: uniqueBy([...destinationMatches, ...hubMatches], (entry) => entry.url).slice(0, 4),
    },
    {
      key: 'itineraries',
      title: 'Turn these picks into an itinerary',
      description: 'Day-by-day routes that match the same destination and traveler intent.',
      links: itineraryMatches,
    },
    {
      key: 'compares',
      title: 'Compare nearby options',
      description: 'Compare pages for travelers deciding between this destination and close alternatives.',
      links: compareMatches,
    },
    {
      key: 'adjacent',
      title: `More ${data.taxonomy?.city || data.taxonomy?.country || 'travel'} picks`,
      description: 'Adjacent topical guides in the same city so readers can keep drilling into the trip they are already planning.',
      links: adjacentPopularPicks,
    },
  ].filter((section) => section.links.length);
}

function renderIntentLinkSections(data) {
  const sections = buildIntentLinks(data);
  if (!sections.length) return '';
  return sections.map((section) => `
      <section class="related-section intent-section">
        <h2>${escapeHtml(section.title)}</h2>
        <p class="related-intro">${escapeHtml(section.description)}</p>
        <div class="intent-grid">
          ${section.links.map((link) => `
            <a class="intent-card" href="${escapeHtml(link.url)}">
              <span class="intent-type">${escapeHtml(link.type.replace(/-/g, ' '))}</span>
              <strong>${escapeHtml(link.title)}</strong>
            </a>`).join('')}
        </div>
      </section>`).join('');
}

function buildRelatedPopularPickLinks(data, limit = 5) {
  const inventory = getSiteInventory();
  const tokens = buildIntentTokens(data);
  const manualLinks = (data.related?.manual || [])
    .map((slug) => inventory.popularPicks.find((item) => item.slug === slug))
    .filter(Boolean);
  const excluded = new Set([data.slug, ...manualLinks.map((entry) => entry.slug)]);
  const candidates = inventory.popularPicks.filter((entry) => !excluded.has(entry.slug));
  const strictMatches = pickTopEntries(candidates, data, tokens, {
    limit: Math.max(limit * 2, 10),
    minScore: 1,
    requireLocation: true,
  });
  const remainingCandidates = candidates.filter((entry) => !strictMatches.some((match) => match.url === entry.url));
  const broadMatches = pickTopEntries(remainingCandidates, data, tokens, { limit: Math.max(limit * 2, 10), minScore: 1 });
  const fillerMatches = remainingCandidates
    .filter((entry) => !broadMatches.some((match) => match.url === entry.url))
    .sort((a, b) => a.title.localeCompare(b.title))
    .slice(0, limit);

  return uniqueBy([...manualLinks, ...strictMatches, ...broadMatches, ...fillerMatches], (entry) => entry.url).slice(0, limit);
}

function renderMapPanel(mapData, mapPicks, mobile = false) {
  if (!mapData.enabled || !mapPicks.length) return '';
  const firstPick = mapPicks[0];
  // Show all picks in the legend so the sidebar mirrors the full page,
  // not just an arbitrary first-6 slice. The legend itself scrolls if
  // needed, so there's no overflow concern.
  const topPicks = mapPicks.map((pick) => `
      <li>
        <a href="#${pick.anchorId}">${pick.label}</a>
      </li>`).join('');

  return `
    <section class="${mobile ? 'map-inline' : 'map-sidebar'}" data-map-panel="${mobile ? 'mobile' : 'desktop'}">
      <h2>${escapeHtml(mapData.title)}</h2>
      <div class="map-active-pick" data-map-active-pick>${escapeHtml(firstPick.label)}</div>
      <div class="popular-picks-map" data-map-canvas aria-label="${escapeHtml(mapData.title)}"></div>
      <div class="map-legend">
        <strong>Start with:</strong>
        <ul>${topPicks}</ul>
        <p><a href="${escapeHtml(firstPick.ctaUrl || mapData.ctaUrl)}" target="_blank" rel="noopener" data-map-cta>${escapeHtml(mapData.ctaLabel)} →</a></p>
      </div>
    </section>`;
}

function stripWhatToOrderLead(text) {
  if (!text) return '';
  const match = text.match(/What to (?:order|expect):\s*(.*)/s);
  return match ? match[1].trim() : text;
}

function firstSentenceClean(text = '') {
  const sentence = firstSentence(text).replace(/^[\s"'“”‘’]+|[\s"'“”‘’]+$/g, '').trim();
  return sentence || text.trim();
}

function buildVerdictText(pick) {
  return firstNonEmpty(firstSentenceClean(pick.insiderTip), firstSentenceClean(pick.whyItMadeTheList), firstSentenceClean(stripWhatToOrderLead(pick.whatToOrder)));
}

function isLikelyPriceRange(value = '') {
  return /[$€£¥₩฿₵₫₹]|\bfree\b|\d+\s*(?:-|–|to)\s*[$€£¥₩฿₵₫₹]?\d+/i.test(String(value));
}

function buildBestForText(pick, data, firstTag) {
  if (pick.whyItMadeTheList) {
    const text = pick.whyItMadeTheList;
    const patterns = [
      /best\s+(?:for|pick for)\s+([^.;]+)/i,
      /ideal\s+for\s+([^.;]+)/i,
      /worth\s+it\s+for\s+([^.;]+)/i,
      /the\s+spot\s+for\s+([^.;]+)/i,
    ];
    for (const pattern of patterns) {
      const match = text.match(pattern);
      if (match && match[1]) return match[1].trim().replace(/^the\s+/i, '');
    }
  }
  const location = firstNonEmpty(pick.neighborhood, pick.address, data.taxonomy.city);
  if (pick.priceRangeLocal && isLikelyPriceRange(pick.priceRangeLocal) && location) return `${firstTag} in ${location} with a ${pick.priceRangeLocal} spend range`;
  if (location) return `${firstTag} in ${location}`;
  return firstTag;
}

function buildStrengths(pick, firstTag) {
  const strengths = [];
  if (pick.googleRating && pick.reviewCount) strengths.push(`${pick.googleRating}★ from ${pick.reviewCount.toLocaleString()} Google reviews`);
  else if (pick.googleRating) strengths.push(`${pick.googleRating}★ Google rating`);
  if (Array.isArray(pick.knownForTags) && pick.knownForTags.length) strengths.push(`Known for ${pick.knownForTags.slice(0, 2).join(', ')}`);
  if (firstTag) strengths.push(firstTag);
  if (pick.address) strengths.push(pick.address);
  if (pick.hoursNote && /open 24 hours/i.test(pick.hoursNote)) strengths.push('Open 24 hours');
  return strengths.slice(0, 3);
}

function buildLimitations(pick) {
  const limitationText = firstNonEmpty(pick.insiderTip, pick.whyItMadeTheList);
  const patterns = [
    /check recent reviews before booking[^.;]*/i,
    /book ahead[^.;]*/i,
    /worth the splurge[^.;]*/i,
    /more formal than[^.;]*/i,
    /polarizing[^.;]*/i,
    /won't know the menu until it arrives[^.;]*/i,
    /cash only[^.;]*/i,
    /dress code[^.;]*/i,
    /tourist trap[^.;]*/i,
    /overpriced[^.;]*/i,
    /can get busy[^.;]*/i,
    /gets busy[^.;]*/i,
    /line gets brutal[^.;]*/i,
    /just be prepared:?\s*([^.;]+)/i,
    /however,?\s*([^.;]+)/i,
    /but\s+([^.;]+)/i,
  ];
  for (const pattern of patterns) {
    const match = limitationText.match(pattern);
    if (match) {
      return (match[1] || match[0]).replace(/^[:\s-]+/, '').trim();
    }
  }
  if (pick.waitExpectation && /busy|long|crowded|line/i.test(pick.waitExpectation)) return pick.waitExpectation;
  if (pick.priceRangeLocal && isLikelyPriceRange(pick.priceRangeLocal)) return `Price band: ${pick.priceRangeLocal}`;
  return '';
}

function renderComparisonRow(label, value) {
  if (!value) return '';
  return `<div class="comparison-row"><dt>${escapeHtml(label)}</dt><dd>${escapeHtml(value)}</dd></div>`;
}

function resolveBestOverall(data) {
  const candidate = data.summary?.bestOverall || data.summary?.topPick || '';
  if (!candidate || !data.picks.length) return data.picks[0] ? data.picks[0].name : '';
  const match = data.picks.find((p) => p.name === candidate || candidate.startsWith(p.name));
  if (match && typeof match.reviewCount === 'number' && match.reviewCount < 10 && data.picks[0] && data.picks[0].name !== match.name) {
    return data.picks[0].name;
  }
  if (match) return match.name;
  return candidate;
}

function renderTagList(items = [], className = 'pick-tag-list') {
  if (!Array.isArray(items) || !items.length) return '';
  return `<div class="${className}">${items.map((item) => `<span>${escapeHtml(item)}</span>`).join('')}</div>`;
}

function buildProvenanceSummary(pick) {
  const provenance = pick?.provenance || {};
  const bits = [];
  if (provenance.sourceCount != null) bits.push(`${provenance.sourceCount} sources`);
  if (Array.isArray(provenance.sourceTypes) && provenance.sourceTypes.length) bits.push(provenance.sourceTypes.join(', '));
  if (provenance.lastVerified) bits.push(`verified ${provenance.lastVerified}`);
  if (provenance.confidence) bits.push(`${provenance.confidence} confidence`);
  return bits.join(' · ');
}

function renderQuickAnswer(data) {
  const firstThree = data.picks.slice(0, 3).map((pick) => `
            <li><strong>${escapeHtml(pick.name)}:</strong> ${escapeHtml(buildVerdictText(pick))}</li>`).join('');
  const summaryRows = [
    ['Best overall', resolveBestOverall(data)],
    ['Price/value range', data.summary?.priceRangeLocal || data.summary?.priceRangeUSD || data.picks.map((pick) => pick.priceRangeLocal).filter((value) => isLikelyPriceRange(value))[0] || 'Varies by pick'],
    ['Top-ranked pick', data.summary?.topPick || (data.picks[0] ? data.picks[0].name : '')],
    ['Last verified', data.summary?.lastVerifiedLabel || 'See page metadata'],
  ].filter(([, value]) => value);

  return `
        <section class="quick-answer-section">
          <div class="quick-answer-card">
            <p class="eyebrow">Quick answer</p>
            <p class="quick-answer-lead"><strong>${escapeHtml(data.intro.answerFirst)}</strong></p>
            <dl class="quick-answer-grid">
              ${summaryRows.map(([label, value]) => renderComparisonRow(label, value)).join('')}
            </dl>
          </div>
          <div class="quick-answer-card">
            <p class="eyebrow">Top verdicts</p>
            <ul class="top-verdicts-list">${firstThree}</ul>
          </div>
        </section>`;
}

function renderPick(pick, data, mapData) {
  const mapQuery = buildPickMapQuery(pick, data);
  const hours = parseHoursNote(pick.hoursNote);
  const firstTag = (pick.tags || [])[0] || pick.placeType || 'Restaurant';
  const verdictText = buildVerdictText(pick);
  const bestForText = buildBestForText(pick, data, firstTag);
  const strengths = buildStrengths(pick, firstTag);
  const limitations = buildLimitations(pick);
  const operationalTags = [
    pick.reservationNeeded === true ? 'Reservations recommended' : '',
    pick.reservationNeeded === false ? 'Walk-in friendly' : '',
    pick.bestTimeToGo || '',
    pick.waitExpectation ? `Wait: ${pick.waitExpectation}` : '',
    pick.mealType || '',
    pick.touristyLevel || '',
  ].filter(Boolean);
  const provenanceSummary = buildProvenanceSummary(pick);
  const valueSignal = firstNonEmpty(
    pick.priceRangeLocal && isLikelyPriceRange(pick.priceRangeLocal) ? `${pick.priceRangeLocal}${pick.googleRating ? ` · ${pick.googleRating}★` : ''}` : '',
    pick.googleRating && pick.reviewCount ? `${pick.googleRating}★ from ${pick.reviewCount.toLocaleString()} reviews` : '',
    pick.googleRating ? `${pick.googleRating}★ Google rating` : ''
  );
  const whyItMadeTheList = firstNonEmpty(pick.whyItMadeTheList, pick.insiderTip);
  const orderNote = pick.whatToOrder && !pick.whatToOrder.includes('is a featured pick in this guide')
    ? stripWhatToOrderLead(pick.whatToOrder)
    : '';
  const quoteBlocks = (pick.redditQuotes || []).map((quote) => `
    <div class="reddit-quote">
        "${escapeHtml(quote.quote)}"
        ${quote.source ? `<span class="source">${escapeHtml(quote.source)}</span>` : ''}
    </div>`).join('');

  const contactRow = [
    pick.phone ? `<span>📞 <a href="tel:${escapeHtml(formatPhone(pick.phone))}">${escapeHtml(formatPhone(pick.phone))}</a></span>` : '',
    pick.website ? `<span>🌐 <a href="${escapeHtml(pick.website)}" target="_blank" rel="noopener">Website</a></span>` : ''
  ].filter(Boolean).join('');

  const mapAttrs = [
    `data-map-name="${escapeHtml(`${pick.rank}. ${pick.name}`)}"`,
    `data-map-cta-url="${escapeHtml(pick.googleMapsUrl || mapData.ctaUrl)}"`,
    `data-map-query="${escapeHtml(mapQuery)}"`,
  ];
  if (typeof pick.lat === 'number' && typeof pick.lng === 'number') {
    mapAttrs.push(`data-map-lat="${escapeHtml(String(pick.lat))}"`);
    mapAttrs.push(`data-map-lng="${escapeHtml(String(pick.lng))}"`);
  }

  return `
<section class="restaurant-section" id="${pickAnchorId(pick)}" ${mapAttrs.join(' ')}>
    <div class="restaurant-header">
        <h2><span class="restaurant-number">${pick.rank}</span>${escapeHtml(pick.name)}</h2>
        <span class="cuisine-tag ${cuisineTagClass(pick)}">${escapeHtml(firstTag)}</span>
        ${pick.googleRating ? `<span class="google-rating"><span class="star">★</span> ${escapeHtml(String(pick.googleRating))}${pick.reviewCount ? ` · ${escapeHtml(pick.reviewCount.toLocaleString())} reviews` : ''}</span>` : ''}
    </div>
    <div class="restaurant-details">
        ${pick.priceRangeLocal && isLikelyPriceRange(pick.priceRangeLocal) ? `<span>💴 ${escapeHtml(pick.priceRangeLocal)}</span>` : ''}
        ${pick.address ? `<span>📍 ${escapeHtml(pick.address)}</span>` : ''}
        ${pick.googleMapsUrl ? `<a href="${escapeHtml(pick.googleMapsUrl)}" target="_blank" rel="noopener">📌 Google Maps →</a>` : ''}
    </div>
    <div class="pick-quick-take">
      <strong>Verdict:</strong> ${escapeHtml(verdictText)}
    </div>
    ${renderTagList(operationalTags, 'pick-tag-list operational-tags')}
    ${renderTagList(pick.knownForTags, 'pick-tag-list known-for-tags')}
    ${renderTagList(pick.dietaryTags, 'pick-tag-list dietary-tags')}
    ${renderTagList(pick.paymentHints, 'pick-tag-list payment-tags')}
    <div class="comparison-card">
      <h3>Quick comparison</h3>
      <dl class="comparison-grid">
        ${renderComparisonRow('Best for', bestForText)}
        ${renderComparisonRow('Strengths', strengths.join(' · '))}
        ${renderComparisonRow('Limitations', limitations)}
        ${renderComparisonRow('Price / value', valueSignal)}
        ${renderComparisonRow('Why it made the list', whyItMadeTheList)}
        ${renderComparisonRow('What to order', orderNote)}
        ${renderComparisonRow('Best time to go', pick.bestTimeToGo)}
        ${renderComparisonRow('Wait expectation', pick.waitExpectation)}
        ${renderComparisonRow('Reservation', pick.reservationNeeded === true ? 'Recommended' : pick.reservationNeeded === false ? 'Usually not needed' : '')}
      </dl>
    </div>
    ${provenanceSummary ? `<div class="pick-provenance">Source quality: ${escapeHtml(provenanceSummary)}</div>` : ''}
    ${hours.length ? `
    <div class="shop-hours">
        <details>
            <summary>${escapeHtml(hoursSummary(pick, hours))}</summary>
            <div class="hours-grid">
            ${hours.map((item) => `<span>${escapeHtml(item.day)}</span><span>${escapeHtml(item.hours)}</span>`).join('')}
            </div>
        </details>
    </div>` : ''}
    ${contactRow ? `<div class="shop-contact">${contactRow}</div>` : ''}

    ${pick.photo ? `<img src="${escapeHtml(absoluteUrl(pick.photo))}" alt="${escapeHtml(pick.name)} in ${escapeHtml(pick.neighborhood || pick.address || '')}" style="width:100%;border-radius:12px;margin-bottom:1rem;" loading="lazy">` : ''}
    ${quoteBlocks}
</section>`;
}

function renderViatorSection(data) {
  const city = (data.taxonomy && data.taxonomy.city) || 'the destination';
  const category = ((data.taxonomy && (data.taxonomy.category || data.taxonomy.vertical)) || '').toLowerCase();
  const cityEnc = encodeURIComponent(city);
  const pid = 'P00292930';
  const mcid = '42383';
  const medium = 'link';
  const affiliateParams = `pid=${pid}&mcid=${mcid}&medium=${medium}`;
  const exploreUrl = `https://www.viator.com/search/${cityEnc}+tours?${affiliateParams}`;

  let cards;
  if (category.includes('restaurant') || category.includes('food') || category.includes('eat') || category.includes('cafe') || category.includes('café') || category.includes('street food') || category.includes('dining')) {
    cards = [
      { type: 'Food Tour', name: `Best ${city} Food Tours & Tastings`, url: `https://www.viator.com/search/${cityEnc}+food+tour?${affiliateParams}` },
      { type: 'Night Food Tour', name: `${city} Night Street Food Tour`, url: `https://www.viator.com/search/${cityEnc}+night+food+tour?${affiliateParams}` },
      { type: 'Cooking Class', name: `${city} Cooking Class & Market Visit`, url: `https://www.viator.com/search/${cityEnc}+cooking+class?${affiliateParams}` },
    ];
  } else if (category.includes('shop') || category.includes('market') || category.includes('boutique') || category.includes('fashion')) {
    cards = [
      { type: 'Shopping Tour', name: `${city} Shopping & Style Tour`, url: `https://www.viator.com/search/${cityEnc}+shopping+tour?${affiliateParams}` },
      { type: 'Market Tour', name: `${city} Local Market Experience`, url: `https://www.viator.com/search/${cityEnc}+market+tour?${affiliateParams}` },
      { type: 'Cultural Walk', name: `${city} Cultural Walking Tour`, url: `https://www.viator.com/search/${cityEnc}+cultural+walk?${affiliateParams}` },
    ];
  } else if (category.includes('bar') || category.includes('night') || category.includes('drink') || category.includes('cocktail') || category.includes('pub') || category.includes('club')) {
    cards = [
      { type: 'Bar Crawl', name: `${city} Bar Crawl & Nightlife Tour`, url: `https://www.viator.com/search/${cityEnc}+bar+crawl?${affiliateParams}` },
      { type: 'Night Tour', name: `Guided ${city} Night Tour`, url: `https://www.viator.com/search/${cityEnc}+night+tour?${affiliateParams}` },
      { type: 'Food & Drink Tour', name: `${city} Food & Drink Experience`, url: `https://www.viator.com/search/${cityEnc}+food+drink+tour?${affiliateParams}` },
    ];
  } else if (category.includes('temple') || category.includes('culture') || category.includes('museum') || category.includes('heritage') || category.includes('historic') || category.includes('art')) {
    cards = [
      { type: 'Walking Tour', name: `${city} Guided Walking Tour`, url: `https://www.viator.com/search/${cityEnc}+walking+tour?${affiliateParams}` },
      { type: 'Cultural Tour', name: `${city} Cultural Highlights Tour`, url: `https://www.viator.com/search/${cityEnc}+cultural+tour?${affiliateParams}` },
      { type: 'Day Trip', name: `Best Day Trips from ${city}`, url: `https://www.viator.com/search/${cityEnc}+day+trip?${affiliateParams}` },
    ];
  } else {
    cards = [
      { type: 'Walking Tour', name: `${city} Guided Walking Tour`, url: `https://www.viator.com/search/${cityEnc}+walking+tour?${affiliateParams}` },
      { type: 'Food Tour', name: `Best ${city} Food Tours & Tastings`, url: `https://www.viator.com/search/${cityEnc}+food+tour?${affiliateParams}` },
      { type: 'Day Trip', name: `Best Day Trips from ${city}`, url: `https://www.viator.com/search/${cityEnc}+day+trip?${affiliateParams}` },
    ];
  }

  cards.push({ type: 'Explore More', name: `All ${city} Tours & Activities →`, url: exploreUrl });

  const cardHtml = cards.map(c => `
      <a class="viator-card" href="${c.url}" target="_blank" rel="noopener sponsored">
        <span class="tour-type">${c.type}</span>
        <span class="tour-name">${c.name}</span>
      </a>`).join('');

  return `
      <section class="viator-section">
        <h2>🎟️ Book ${city} Experiences</h2>
        <p class="viator-subtitle">Tours and activities hand-picked for this guide — book with free cancellation</p>
        <div class="viator-cards">${cardHtml}
        </div>
        <p class="viator-powered">Experiences via Viator — free cancellation on most tours</p>
      </section>`;
}

function renderPage(data) {
  const validation = validateSource(data);
  if (validation.errors.length) {
    throw new Error(`Cannot render invalid source:\n${validation.errors.join('\n')}`);
  }

  const mapData = buildDerivedMap(data);
  const mapPicks = buildMapPicks(data.picks, data, mapData);
  const introBody = dedupeIntroBody(data.intro.answerFirst, data.intro.body);
  const relatedLinks = buildRelatedPopularPickLinks(data, 5).map((entry) => `
        <li><a href="${escapeHtml(entry.url)}">${escapeHtml(entry.title)}</a></li>`).join('');

  return `<!DOCTYPE html>
<html lang="en">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-D7QHNRXLHJ"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-D7QHNRXLHJ');
    </script>
    ${renderMeta(data)}
    ${renderSchema(data)}
    <style>
      :root {
        --indigo:#2D3A5C; --indigo-light:#3D4E7A; --warm-cream:#F5F0E8; --sand:#E8DFD0;
        --earth:#8B7355; --terracotta:#C4704B; --white:#FEFCF9; --text:#2C2419; --text-muted:#6B5D4F;
      }
      * { margin:0; padding:0; box-sizing:border-box; }
      body { font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif; color:var(--text); background:var(--white); line-height:1.6; -webkit-font-smoothing:antialiased; }
      a { color:var(--terracotta); text-decoration:none; }
      nav { position:sticky; top:0; z-index:100; background:rgba(254,252,249,.92); backdrop-filter:blur(20px); border-bottom:1px solid var(--sand); padding:1rem 1.5rem; display:flex; justify-content:space-between; align-items:center; }
      .logo { font-size:1.3rem; font-weight:700; color:var(--indigo); }
      .cta-nav { background:var(--terracotta); color:white; padding:.55rem 1rem; border-radius:8px; }
      .hero { padding:6.5rem 1.5rem 2rem; max-width:840px; margin:0 auto; }
      .hero-badge { display:inline-block; background:var(--sand); color:var(--earth); padding:.35rem 1rem; border-radius:999px; font-size:.9rem; margin-bottom:1rem; }
      .hero h1 { font-size:clamp(2rem,4.7vw,3rem); line-height:1.12; color:var(--indigo); margin:0 0 1rem; letter-spacing:-.03em; }
      .subtitle { font-size:1.08rem; color:var(--text-muted); max-width:680px; }
      .hero-meta { display:flex; flex-wrap:wrap; gap:1rem 1.5rem; color:var(--earth); font-size:.92rem; margin-top:1.2rem; }
      .page-layout { max-width:1260px; margin:0 auto; padding:0 1.5rem 4rem; display:grid; grid-template-columns:320px minmax(0,1fr); gap:2rem; }
      .content { min-width:0; }
      .map-sidebar { position:sticky; top:92px; align-self:start; background:var(--warm-cream); border:1px solid var(--sand); border-radius:18px; padding:1rem; }
      .popular-picks-map { width:100%; height:360px; border-radius:12px; background:var(--sand); overflow:hidden; }
      .map-sidebar h2, .map-inline h2 { margin:.2rem 0 .35rem; color:var(--indigo); font-size:1.05rem; }
      .map-active-pick { color:var(--earth); font-size:.92rem; font-weight:700; margin:0 0 .8rem; }
      .map-legend ul { margin:.75rem 0; padding-left:1.2rem; }
      .restaurant-section { scroll-margin-top:100px; transition:background-color .18s ease, box-shadow .18s ease, border-radius .18s ease; }
      .restaurant-section.active { background:#fffaf4; border-radius:14px; box-shadow:0 0 0 1px var(--sand) inset; padding-left:1rem; padding-right:1rem; }
      .quick-answer-section { display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:1rem; margin-bottom:1.4rem; }
      .quick-answer-card, .intro-section, .methodology-section, .faq-section, .related-section { background:white; border:1px solid var(--sand); border-radius:18px; padding:1.35rem 1.4rem; }
      .quick-answer-section, .intro-section, .methodology-section, .faq-section, .related-section { margin-bottom:1.4rem; }
      .eyebrow { text-transform:uppercase; letter-spacing:.08em; font-size:.78rem; font-weight:700; color:var(--earth); margin-bottom:.55rem; }
      .quick-answer-lead { margin-bottom:1rem; }
      .quick-answer-grid, .comparison-grid { display:grid; gap:.7rem; }
      .comparison-row { display:grid; grid-template-columns:150px minmax(0, 1fr); gap:.5rem 1rem; align-items:start; }
      .comparison-row dt { font-weight:700; color:var(--indigo); }
      .comparison-row dd { color:var(--text); }
      .top-verdicts-list { padding-left:1.1rem; display:grid; gap:.75rem; }
      .map-inline { display:none; background:var(--warm-cream); border:1px solid var(--sand); border-radius:18px; padding:1rem; margin-bottom:1.4rem; }
      .restaurant-section { border-bottom:1px solid var(--sand); padding:2.5rem 0; }
      .restaurant-section:first-of-type { padding-top:0; }
      .restaurant-section:last-of-type { border-bottom:none; }
      .restaurant-header { display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:.75rem; flex-wrap:wrap; gap:.5rem; }
      .restaurant-header h2 { font-size:1.35rem; font-weight:700; color:var(--indigo); }
      .restaurant-number { display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:50%; background:var(--terracotta); color:white; font-size:.8rem; font-weight:700; margin-right:.5rem; flex-shrink:0; }
      .cuisine-tag { display:inline-block; padding:.2rem .6rem; border-radius:6px; font-size:.78rem; font-weight:600; white-space:nowrap; }
      .tag-ramen { background:#FFF3E0; color:#E65100; } .tag-tonkatsu { background:#FBE9E7; color:#BF360C; } .tag-gyudon { background:#EFEBE9; color:#4E342E; } .tag-udon { background:#E8EAF6; color:#283593; } .tag-tempura { background:#E0F2F1; color:#00695C; } .tag-sushi { background:#E3F2FD; color:#1565C0; } .tag-yakitori { background:#FCE4EC; color:#AD1457; } .tag-tsukemen { background:#FFF8E1; color:#FF8F00; } .tag-gyukatsu { background:#F1F8E9; color:#558B2F; } .tag-kushikatsu { background:#F3E5F5; color:#7B1FA2; } .tag-shabu { background:#EDE7F6; color:#512DA8; } .tag-omurice { background:#FFFDE7; color:#F9A825; } .tag-hamburg { background:#EFEBE9; color:#6D4C41; } .tag-snack { background:#FCE4EC; color:#C2185B; } .tag-regional { background:#ECEFF1; color:#455A64; }
      .google-rating { color:var(--earth); font-size:.95rem; }
      .star { color:#FFB400; }
      .restaurant-details, .shop-contact { display:flex; flex-wrap:wrap; gap:.75rem 1rem; font-size:.95rem; color:var(--earth); margin-bottom:.9rem; }
      .pick-quick-take { margin:0 0 1rem; padding:1rem; background:#fffaf4; border:1px solid var(--sand); border-radius:12px; }
      .pick-tag-list { display:flex; flex-wrap:wrap; gap:.45rem; margin:0 0 .85rem; }
      .pick-tag-list span { display:inline-flex; align-items:center; padding:.28rem .65rem; border-radius:999px; background:#faf7f3; border:1px solid var(--sand); color:var(--earth); font-size:.8rem; }
      .pick-provenance { margin:0 0 1rem; color:var(--text-muted); font-size:.88rem; }
      .comparison-card { margin:0 0 1rem; padding:1rem; background:var(--warm-cream); border:1px solid var(--sand); border-radius:14px; }
      .comparison-card h3 { color:var(--indigo); margin:0 0 .75rem; font-size:1rem; }
      .shop-hours { margin-bottom:.9rem; }
      .shop-hours summary { cursor:pointer; color:var(--indigo); font-weight:700; }
      .hours-grid { display:grid; grid-template-columns:auto 1fr; gap:.4rem 1rem; margin-top:.75rem; color:var(--text-muted); font-size:.94rem; }
      .reddit-quote { margin:1rem 0 0; padding:1rem; background:#faf7f3; border-left:3px solid var(--terracotta); }
      .source { display:block; margin-top:.4rem; color:var(--earth); font-size:.92rem; }
      .faq-item + .faq-item { border-top:1px solid var(--sand); padding-top:1rem; margin-top:1rem; }
      .faq-item h3 { color:var(--indigo); margin:.2rem 0 .45rem; }
      .related-intro { color:var(--text-muted); margin:.25rem 0 1rem; }
      ul.related { padding-left:1.2rem; margin:0; }
      .intent-grid { display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:.9rem; }
      .intent-card { display:block; background:var(--warm-cream); border:1px solid var(--sand); border-radius:14px; padding:1rem; color:var(--text); }
      .intent-card:hover { border-color:var(--terracotta); transform:translateY(-1px); }
      .intent-type { display:block; text-transform:uppercase; letter-spacing:.08em; font-size:.72rem; font-weight:700; color:var(--earth); margin-bottom:.45rem; }
      footer { max-width:1260px; margin:0 auto; padding:0 1.5rem 3rem; color:var(--text-muted); }
      @media (max-width:980px) { .page-layout { grid-template-columns:1fr; } .map-sidebar { display:none; } .map-inline { display:block; } .quick-answer-section { grid-template-columns:1fr; } .comparison-row { grid-template-columns:1fr; } .restaurant-section { padding:2rem 0; } .restaurant-section.active { padding-left:.85rem; padding-right:.85rem; } }
      .viator-section { background:linear-gradient(135deg,#fff9f0 0%,#fff 100%); border:1px solid var(--sand); border-radius:18px; padding:1.35rem 1.4rem; margin-bottom:1.4rem; }
      .viator-section h2 { font-size:1.3em; margin-bottom:6px; }
      .viator-subtitle { font-size:0.95em; color:#666; margin-bottom:20px; }
      .viator-cards { display:grid; grid-template-columns:1fr 1fr; gap:14px; }
      @media(max-width:600px) { .viator-cards { grid-template-columns:1fr; } }
      .viator-card { background:#fff; border:1px solid #e8e8e8; border-radius:10px; padding:18px; text-decoration:none; color:inherit; transition:border-color .2s,box-shadow .2s; display:flex; flex-direction:column; gap:8px; }
      .viator-card:hover { border-color:var(--primary,#0696D7); box-shadow:0 2px 12px rgba(6,150,215,.12); }
      .viator-card .tour-type { font-size:.75em; text-transform:uppercase; letter-spacing:.5px; color:var(--primary,#0696D7); font-weight:600; }
      .viator-card .tour-name { font-size:1em; font-weight:600; line-height:1.3; }
      .viator-powered { font-size:.75em; color:#bbb; text-align:right; margin-top:14px; }
    </style>
</head>
<body>
  <nav>
    <a class="logo" href="/">tabiji.ai</a>
    <a class="cta-nav" href="/plan.html">Plan My Trip</a>
  </nav>

  ${renderHero(data)}

  <div class="page-layout">
    <aside>
      ${renderMapPanel(mapData, mapPicks, false)}
    </aside>

    <main class="content">
      ${renderQuickAnswer(data)}

      <section class="intro-section">
        ${data.intro.answerFirst ? `<p><strong>${escapeHtml(data.intro.answerFirst)}</strong></p>` : ''}
        ${renderRichTextParagraphs(data.intro.answerFirst ? introBody.filter((item) => item !== data.intro.answerFirst) : introBody)}
      </section>

      ${renderMapPanel(mapData, mapPicks, true)}

      ${data.intro.methodology ? `
        <section class="methodology-section">
          <h2>How we built this list</h2>
          <p>${escapeHtml(data.intro.methodology)}</p>
        </section>` : ''}

      <section class="pick-list">
        ${data.picks.map((pick) => renderPick(pick, data, mapData)).join('')}
      </section>

      <section class="faq-section">
        <h2>Frequently Asked Questions</h2>
        ${data.faq.map((item) => `<div class="faq-item"><h3>${escapeHtml(item.question)}</h3><p>${escapeHtml(item.answer)}</p></div>`).join('')}
      </section>

      ${renderViatorSection(data)}

      ${renderIntentLinkSections(data)}

      <section class="related-section">
        <h2>Related Popular Picks</h2>
        <ul class="related">${relatedLinks}</ul>
      </section>
    </main>
  </div>

  <footer>Generated from structured source data.</footer>
  <script>
    window.__POPULAR_PICKS_MAP__ = ${JSON.stringify({
      enabled: mapData.enabled && mapPicks.length > 0,
      title: mapData.title,
      ctaLabel: mapData.ctaLabel,
      defaultCtaUrl: mapData.ctaUrl,
      picks: mapPicks,
    })};
  </script>
  <script>
    (function () {
      var sections = Array.prototype.slice.call(document.querySelectorAll('.restaurant-section'));
      var panels = Array.prototype.slice.call(document.querySelectorAll('[data-map-panel]'));
      var mapConfig = window.__POPULAR_PICKS_MAP__ || {};
      var mapState = { maps: [] };
      if (!sections.length || !panels.length) return;

      function findPickBySection(section) {
        var id = section && section.id;
        if (!id || !Array.isArray(mapConfig.picks)) return null;
        return mapConfig.picks.find(function (pick) { return pick.anchorId === id; }) || null;
      }

      function syncPanels(section, pick) {
        panels.forEach(function (panel) {
          var title = panel.querySelector('[data-map-active-pick]');
          var cta = panel.querySelector('[data-map-cta]');
          if (title) title.textContent = (section && section.dataset.mapName) || (pick && pick.label) || '';
          if (cta) cta.href = (pick && pick.ctaUrl) || (section && section.dataset.mapCtaUrl) || mapConfig.defaultCtaUrl || '#';
        });
      }

      function highlightMarker(activePick) {
        mapState.maps.forEach(function (entry) {
          entry.markers.forEach(function (markerEntry) {
            var isActive = activePick && markerEntry.pick.anchorId === activePick.anchorId;
            markerEntry.marker.setIcon({
              path: google.maps.SymbolPath.CIRCLE,
              scale: isActive ? 12 : 9,
              fillColor: isActive ? '#2D3A5C' : '#C4704B',
              fillOpacity: 1,
              strokeColor: '#FFFFFF',
              strokeWeight: 2,
            });
            markerEntry.marker.setZIndex(isActive ? 1000 : markerEntry.pick.rank);
          });
          if (activePick) {
            entry.map.panTo({ lat: activePick.lat, lng: activePick.lng });
          }
        });
      }

      function setActive(section) {
        if (!section) return;
        var activePick = findPickBySection(section);
        sections.forEach(function (item) {
          item.classList.toggle('active', item === section);
        });
        syncPanels(section, activePick);
        if (window.google && google.maps && activePick) highlightMarker(activePick);
      }

      function initMaps() {
        if (!mapConfig.enabled || !Array.isArray(mapConfig.picks) || !mapConfig.picks.length) return;
        panels.forEach(function (panel) {
          var canvas = panel.querySelector('[data-map-canvas]');
          if (!canvas) return;
          var map = new google.maps.Map(canvas, {
            center: { lat: mapConfig.picks[0].lat, lng: mapConfig.picks[0].lng },
            zoom: 13,
            mapTypeControl: false,
            streetViewControl: false,
            fullscreenControl: false,
            clickableIcons: false,
            styles: [
              { featureType: 'poi', stylers: [{ visibility: 'off' }] },
              { featureType: 'transit', stylers: [{ visibility: 'off' }] }
            ]
          });
          var bounds = new google.maps.LatLngBounds();
          var markers = mapConfig.picks.map(function (pick) {
            var marker = new google.maps.Marker({
              position: { lat: pick.lat, lng: pick.lng },
              map: map,
              title: pick.label,
              label: {
                text: String(pick.rank),
                color: '#FFFFFF',
                fontWeight: '700'
              }
            });
            var infoWindow = new google.maps.InfoWindow({
              content: '<strong>' + pick.label.replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</strong>'
            });
            marker.addListener('click', function () {
              infoWindow.open({ anchor: marker, map: map });
              var target = document.getElementById(pick.anchorId);
              if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            });
            bounds.extend(marker.getPosition());
            return { pick: pick, marker: marker, infoWindow: infoWindow };
          });
          if (mapConfig.picks.length > 1) {
            map.fitBounds(bounds, 48);
          }
          mapState.maps.push({ panel: panel, map: map, markers: markers });
        });
        setTimeout(function () { setActive(sections[0]); }, 0);
      }

      window.initPopularPicksMaps = initMaps;
      setActive(sections[0]);

      if ('IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function (entries) {
          var visible = entries
            .filter(function (entry) { return entry.isIntersecting; })
            .sort(function (a, b) { return b.intersectionRatio - a.intersectionRatio; });
          if (visible[0]) setActive(visible[0].target);
        }, { rootMargin: '-25% 0px -45% 0px', threshold: [0.2, 0.45, 0.7] });
        sections.forEach(function (section) { observer.observe(section); });
      }
    }());
  </script>
  ${mapData.enabled && mapPicks.length ? `<script async src="https://maps.googleapis.com/maps/api/js?key=${GOOGLE_MAPS_API_KEY}&callback=initPopularPicksMaps"></script>` : ''}
</body>
</html>`;
}

if (require.main === module) {
  const [inputPath, outputPath] = process.argv.slice(2);
  if (!inputPath || !outputPath) {
    console.error('Usage: node render-page.js <input.json> <output.html>');
    process.exit(1);
  }
  const data = loadJson(path.resolve(inputPath));
  const html = renderPage(data);
  fs.mkdirSync(path.dirname(path.resolve(outputPath)), { recursive: true });
  fs.writeFileSync(path.resolve(outputPath), html);
  console.log(`Rendered ${outputPath}`);
}

module.exports = { renderPage, parseHoursNote, buildDerivedMap, hoursSummary, pickAnchorId, buildMapPicks };
