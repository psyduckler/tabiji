#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const {
  ALLOWED_DIETARY_TAGS,
  ALLOWED_PAYMENT_HINTS,
  ALLOWED_TOURISTY_LEVELS,
  ALLOWED_MEAL_TYPES,
} = require('./serpapi-enrichment-rules');

const SEARCH_SCRIPT = '/Users/psyduck/.openclaw/workspace/skills/serpapi-search/scripts/search.js';

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function writeJson(filePath, data) {
  fs.writeFileSync(filePath, `${JSON.stringify(data, null, 2)}\n`);
}

function search(query, num = 6, gl = 'us', hl = 'en') {
  const stdout = execFileSync('node', [SEARCH_SCRIPT, '--q', query, '--num', String(num), '--gl', gl, '--hl', hl], {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'inherit'],
  });
  return JSON.parse(stdout);
}

function normalize(text = '') {
  return String(text).toLowerCase();
}

function snippetsText(result = {}) {
  const kg = result.knowledge_graph || {};
  const organics = (result.organic_results || []).map((item) => `${item.title || ''} ${item.snippet || ''}`).join(' ');
  return normalize([
    kg.title,
    kg.description,
    kg.merchant_description,
    kg.raw_hours,
    organics,
  ].filter(Boolean).join(' '));
}

function uniq(items) {
  return [...new Set(items.filter(Boolean))];
}

function inferMealType(text) {
  if (/sunset|rooftop|sky bar|cocktail|dj/.test(text)) return 'sunset drinks / late-night';
  if (/late night|bar/.test(text)) return 'dinner / late-night / drinks';
  if (/breakfast/.test(text)) return 'breakfast';
  if (/brunch/.test(text)) return 'brunch';
  if (/lunch/.test(text) && /dinner/.test(text)) return 'lunch / dinner';
  if (/dinner/.test(text)) return 'dinner';
  if (/snack|takeaway|take away|counter-serve|counter serve|kiosk/.test(text)) return 'snack / lunch';
  return null;
}

function inferDietaryTags(text) {
  const tags = [];
  if (/vegetarian friendly/.test(text)) tags.push('vegetarian-friendly');
  if (/vegetarian option|vegetarian dishes|vegetarian/.test(text)) tags.push('vegetarian-options');
  if (/vegan option|vegan sauces|vegan/.test(text)) tags.push('vegan-options');
  if (/gluten free fries/.test(text)) tags.push('gluten-free-fries');
  else if (/gluten free/.test(text)) tags.push('gluten-free-options');
  if (/halal/.test(text)) tags.push('halal');
  return uniq(tags).filter((item) => ALLOWED_DIETARY_TAGS.includes(item));
}

function inferPaymentHints(text) {
  const tags = [];
  if (/cash only/.test(text)) tags.push('cash-only');
  if (/accepts credit cards|credit cards accepted/.test(text)) tags.push('credit-cards-accepted');
  if (/digital payments/.test(text)) tags.push('digital-payments');
  if (/cash[\-, ]+pin[\-, ]+or creditcard|cash, pin- or creditcard|cash pin or creditcard/.test(text)) tags.push('cash', 'pin', 'credit-card');
  if (/cards accepted|accepts cards|credit card|visa|mastercard/.test(text)) tags.push('cards-accepted');
  return uniq(tags).filter((item) => ALLOWED_PAYMENT_HINTS.includes(item));
}

function inferReservationNeeded(text) {
  if (/walk-in only|walk in only|no reservations required|they don't take reservations|no reservations/.test(text)) return false;
  if (/reserve your table|make a booking|reservations required|reservations are highly recommended|reservation.*recommended|for reservation/.test(text)) return true;
  return null;
}

function inferTouristyLevel(text, reviewCount = 0) {
  if (/tourist trap|iconic destination|hangover/.test(text) || reviewCount > 5000) return 'tourist-magnet';
  if (/locals and tourists|expats and experienced travelers/.test(text)) return 'mixed';
  if (/under the radar|mostly locals|local favorite/.test(text)) return 'mostly-local';
  return reviewCount > 1500 ? 'mixed-leaning-touristy' : null;
}

function inferKnownForTags(text) {
  const candidates = [
    ['360-degree views', /360 degree|360°/],
    ['sunset cocktails', /sunset/],
    ['live DJs', /live dj|regular live djs|dj/],
    ['happy hour deals', /happy hour|buy 1 get 1|free-flow/],
    ['river skyline', /river view|river skyline|chao phraya/],
    ['dress code', /dress code|smart casual|contemporary cool/],
    ['skywalk', /skywalk/],
    ['rooftop party bar', /party atmosphere|hottest rooftop|party bar/],
    ['vegetarian options', /vegetarian/],
  ];
  return candidates.filter(([, rx]) => rx.test(text)).map(([label]) => label).slice(0, 3);
}

function buildSourceTypes(result) {
  const text = snippetsText(result);
  const types = [];
  const kg = result.knowledge_graph || {};
  if (Object.keys(kg).length) types.push('google-serp-kg');
  for (const item of (result.organic_results || [])) {
    const url = item.url || '';
    const title = normalize(item.title || '');
    const snippet = normalize(item.snippet || '');
    if (/tripadvisor/.test(url)) types.push('tripadvisor-snippet');
    else if (/happycow/.test(url)) types.push('happycow-snippet');
    else if (/instagram/.test(url)) types.push('instagram-snippet');
    else if (/facebook/.test(url)) types.push('facebook-snippet');
    else if (/thefork/.test(url)) types.push('thefork-snippet');
    else if (/quandoo/.test(url)) types.push('quandoo-snippet');
    else if (/yelp/.test(url)) types.push('yelp-snippet');
    else if (/sevenrooms|opentable|resy|tablecheck/.test(url)) types.push('booking-page');
    else if (/menu/.test(url) || /menu/.test(title)) types.push('menu-page');
    else if (/faq/.test(url) || /faq/.test(title)) types.push('faq-page');
    else if (/dress code/.test(title) || /dress code/.test(snippet)) types.push('dress-code-page');
    else if (/official website|home|contact|location/.test(title) || /^https?:\/\/(www\.)?[^/]+\/?$/.test(url) || /hyatt|lebua|kimpton|king power/.test(url)) types.push('official-site');
  }
  if (/dress code/.test(text) && !types.includes('dress-code-snippet')) types.push('dress-code-snippet');
  if (/reservation/.test(text) && !types.includes('reservation-snippet')) types.push('reservation-snippet');
  if (/happy hour|promotion|free-flow/.test(text)) types.push('promo-snippet');
  return uniq(types);
}

function inferConfidence(candidate) {
  let score = 0;
  const sourceCount = candidate.provenance.sourceCount || 0;
  score += Math.min(sourceCount, 4);
  if (candidate.reservationNeeded != null) score += 1;
  if (candidate.paymentHints?.length) score += 1;
  if (candidate.dietaryTags?.length) score += 1;
  if (candidate.bestTimeToGo) score += 1;
  if (score >= 6) return 'high';
  if (score >= 5) return 'medium-high';
  if (score >= 3) return 'medium';
  return 'low';
}

function enrichPick(data, pick) {
  const query = `${pick.name} ${data.taxonomy.city} ${data.seo.h1} reservations best time wait dress code vegetarian cards official site`;
  const result = search(query, 6, data.taxonomy.countryCode?.toLowerCase() || 'us', 'en');
  const text = snippetsText(result);
  const kg = result.knowledge_graph || {};
  const sourceTypes = buildSourceTypes(result);
  const candidate = {
    reservationNeeded: inferReservationNeeded(text),
    bestTimeToGo: /sunset/.test(text) ? 'Go around sunset' : null,
    waitExpectation: /crowded|busy/.test(text) ? 'Can get busy at peak times' : null,
    mealType: inferMealType(text),
    dietaryTags: inferDietaryTags(text),
    paymentHints: inferPaymentHints(text),
    touristyLevel: inferTouristyLevel(text, kg.review_count || 0),
    knownForTags: inferKnownForTags(text),
    provenance: {
      sourceCount: sourceTypes.length,
      sourceTypes,
      lastVerified: new Date().toISOString().slice(0, 7),
      confidence: 'medium',
      matchMethod: 'serpapi-search-inference',
    },
  };
  candidate.provenance.confidence = inferConfidence(candidate);

  if (candidate.mealType && !ALLOWED_MEAL_TYPES.includes(candidate.mealType)) delete candidate.mealType;
  if (candidate.touristyLevel && !ALLOWED_TOURISTY_LEVELS.includes(candidate.touristyLevel)) delete candidate.touristyLevel;
  return { query, result, candidate };
}

function main() {
  const filePath = process.argv[2];
  const limit = Number(process.argv[3] || 3);
  if (!filePath) {
    console.error('Usage: node enrich-serpapi.js <popular-picks-data.json> [limit]');
    process.exit(1);
  }

  const data = readJson(path.resolve(filePath));
  const report = [];
  for (const pick of data.picks.slice(0, limit)) {
    const { query, candidate } = enrichPick(data, pick);
    Object.assign(pick, Object.fromEntries(Object.entries(candidate).filter(([, value]) => value != null && (!(Array.isArray(value)) || value.length))));
    report.push({ pick: pick.name, query, candidate });
  }

  writeJson(path.resolve(filePath), data);
  console.log(JSON.stringify(report, null, 2));
}

if (require.main === module) main();
