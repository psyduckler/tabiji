#!/usr/bin/env node
/* eslint-disable max-len */
const fs = require('fs');
const path = require('path');
const { renderMeta, escapeHtml, absoluteUrl } = require('./render-meta');
const { renderSchema } = require('./render-schema');
const { loadJson, validateSource } = require('./validate-source');

const GOOGLE_MAPS_API_KEY = 'AIzaSyBP0yidMjJEECgkIiZz2lw1NLsQ7jdASYc';
const REPO_ROOT = path.resolve(__dirname, '..', '..');

let siteInventoryCache = null;

// ============================================================
// Small helpers
// ============================================================
function readTextIfExists(filePath) {
  try { return fs.readFileSync(filePath, 'utf8'); } catch { return ''; }
}

function titleFromSlug(slug = '') {
  return String(slug).split('-').filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1)).join(' ');
}

function decodeEntities(s = '') {
  return String(s)
    .replace(/&#x([0-9a-fA-F]+);/g, (_, h) => String.fromCodePoint(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(parseInt(d, 10)))
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"').replace(/&apos;/g, "'")
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&nbsp;/g, ' ')
    .replace(/&ldquo;/g, '“').replace(/&rdquo;/g, '”')
    .replace(/&lsquo;/g, '‘').replace(/&rsquo;/g, '’')
    .replace(/&mdash;/g, '—').replace(/&ndash;/g, '–')
    .replace(/&middot;/g, '·').replace(/&hellip;/g, '…');
}

function extractHtmlTitle(filePath, fallbackSlug = '') {
  const html = readTextIfExists(filePath);
  if (!html) return titleFromSlug(fallbackSlug);
  const h1 = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  if (h1) return decodeEntities(h1[1].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim());
  const t = html.match(/<title>([\s\S]*?)<\/title>/i);
  if (t) return decodeEntities(t[1].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim());
  return titleFromSlug(fallbackSlug);
}

function loadDirectoryEntries(dirPath, type, urlPrefix) {
  if (!fs.existsSync(dirPath)) return [];
  return fs.readdirSync(dirPath, { withFileTypes: true })
    .filter((e) => e.isDirectory())
    .map((e) => {
      const slug = e.name;
      const htmlPath = path.join(dirPath, slug, 'index.html');
      if (!fs.existsSync(htmlPath)) return null;
      const title = extractHtmlTitle(htmlPath, slug);
      return { type, slug, url: `${urlPrefix}/${slug}/`, title, searchText: normalize(`${slug} ${title}`) };
    }).filter(Boolean);
}

function getSiteInventory() {
  if (siteInventoryCache) return siteInventoryCache;
  siteInventoryCache = {
    destinations: loadDirectoryEntries(path.join(REPO_ROOT, 'destinations'), 'destination', '/destinations'),
    compares: loadDirectoryEntries(path.join(REPO_ROOT, 'compare'), 'compare', '/compare'),
    popularPicks: loadDirectoryEntries(path.join(REPO_ROOT, 'popular-picks'), 'popular-picks', '/popular-picks'),
  };
  return siteInventoryCache;
}

function firstNonEmpty(...values) {
  for (const v of values) {
    if (typeof v === 'string' && v.trim()) return v.trim();
  }
  return '';
}

function normalize(text = '') {
  return String(text).toLowerCase().normalize('NFKD')
    .replace(/[“”‘’]/g, "'").replace(/[^a-z0-9\s]/g, ' ').replace(/\s+/g, ' ').trim();
}

function slugify(value = '') {
  return String(value).toLowerCase().normalize('NFKD')
    .replace(/[^-\x7F]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}

function pickAnchorId(pick) { return pick.sectionId || slugify(pick.name); }

function isLikelyPriceRange(value = '') {
  return /[$€£¥₩฿₵₫₹]|\bfree\b|\d+\s*(?:-|–|to)\s*[$€£¥₩฿₵₫₹]?\d+/i.test(String(value));
}

function formatPhone(phone) { return phone ? phone.replace(/\s+/g, ' ').trim() : ''; }

function parseHoursNote(hoursNote = '') {
  if (!hoursNote) return [];
  return hoursNote.split(';').map((e) => e.trim()).filter(Boolean).map((e) => {
    const parts = e.split(':');
    if (parts.length < 2) return null;
    return { day: parts.shift().trim(), hours: parts.join(':').trim() };
  }).filter(Boolean);
}

function hoursSummary(pick, hours) {
  if (typeof pick?.editorialFlags?.openNow === 'boolean') {
    return pick.editorialFlags.openNow ? '🕐 Open now' : '🕐 Closed now';
  }
  if (hours.some((i) => /open 24 hours/i.test(i.hours))) return '🕐 Open now';
  return '🕐 Opening hours';
}

function cuisineTagClass(pick) {
  const first = ((pick.tags || [])[0] || '').toLowerCase();
  const map = {
    ramen: 'tag-ramen', tonkatsu: 'tag-tonkatsu', tsukemen: 'tag-tsukemen',
    yakitori: 'tag-yakitori', tempura: 'tag-tempura', sushi: 'tag-sushi',
    gyukatsu: 'tag-gyukatsu', udon: 'tag-udon', gyudon: 'tag-gyudon',
    kushikatsu: 'tag-kushikatsu', shabu: 'tag-shabu', sukiyaki: 'tag-shabu',
    omurice: 'tag-omurice', hamburg: 'tag-hamburg', snack: 'tag-snack',
    pizza: 'tag-pizza', steak: 'tag-steak', bbq: 'tag-bbq',
    classic: 'tag-classic', historic: 'tag-historic', modern: 'tag-modern',
    korean: 'tag-korean',
  };
  for (const k of Object.keys(map)) if (first.includes(k)) return map[k];
  return 'tag-regional';
}

function firstSentence(text = '') { return String(text).split(/(?<=[.!?])\s+/)[0].trim(); }

function firstSentenceClean(text = '') {
  const s = firstSentence(text).replace(/^[\s"'“”‘’]+|[\s"'“”‘’]+$/g, '').trim();
  return s || String(text).trim();
}

function stripWhatToOrderLead(text) {
  if (!text) return '';
  const m = String(text).match(/What to (?:order|expect):\s*(.*)/s);
  return m ? m[1].trim() : String(text);
}

function buildVerdictText(pick) {
  return firstNonEmpty(
    firstSentenceClean(pick.insiderTip),
    firstSentenceClean(pick.whyItMadeTheList),
    firstSentenceClean(stripWhatToOrderLead(pick.whatToOrder)),
  );
}

function dedupeIntroBody(answerFirst = '', body = []) {
  if (!Array.isArray(body) || !body.length) return [];
  if (!answerFirst) return body;
  const a = normalize(answerFirst);
  return body.filter((p) => {
    const pn = normalize(p);
    if (!pn) return false;
    if (pn === a) return false;
    if (a.startsWith(pn) || pn.startsWith(a)) return false;
    return true;
  });
}

// ============================================================
// Map data
// ============================================================
function buildDerivedMap(data) {
  const h1Clean = (data.seo.h1 || '').replace(/^\d+\s+Best\s+/i, '').trim();
  const query = h1Clean || [data.taxonomy.neighborhood, data.taxonomy.city, data.taxonomy.category]
    .filter(Boolean).join(' ');
  return {
    enabled: data.map?.enabled !== false,
    title: data.map?.title || `${data.taxonomy?.category ? capitalize(data.taxonomy.category) + ' ' : ''}Map`.trim(),
    ctaLabel: data.map?.ctaLabel || 'Open in Google Maps',
    ctaUrl: data.map?.ctaUrl || `https://www.google.com/maps/search/${encodeURIComponent(query)}`,
    fallbackQuery: query,
  };
}

function capitalize(s = '') { return s ? s.charAt(0).toUpperCase() + s.slice(1) : ''; }

function buildPickMapQuery(pick, data) {
  return [pick.name, pick.address || pick.neighborhood, data.taxonomy.city, data.taxonomy.countryCode || data.taxonomy.country]
    .filter(Boolean).join(', ');
}

function buildMapPicks(picks, data, mapData) {
  return picks
    .filter((p) => typeof p.lat === 'number' && typeof p.lng === 'number')
    .map((p) => ({
      anchorId: pickAnchorId(p),
      rank: p.rank,
      name: p.name,
      label: `${p.rank}. ${p.name}`,
      lat: p.lat,
      lng: p.lng,
      ctaUrl: p.googleMapsUrl || mapData.ctaUrl,
      mapQuery: buildPickMapQuery(p, data),
    }));
}

// ============================================================
// Related links (for the related-section intent-card grid)
// ============================================================
function uniqueBy(items, keyFn) {
  const seen = new Set();
  const out = [];
  for (const it of items) {
    const k = keyFn(it);
    if (!k || seen.has(k)) continue;
    seen.add(k);
    out.push(it);
  }
  return out;
}

function tokensFor(text = '') {
  return new Set(normalize(text).split(' ').filter((t) => t.length >= 4));
}

function pageTokens(data) {
  const t = new Set();
  for (const x of [data.taxonomy?.city, data.taxonomy?.country, data.taxonomy?.category]) {
    if (x) for (const tok of tokensFor(x)) t.add(tok);
  }
  for (const part of String(data.slug || '').split('-')) if (part.length >= 4) t.add(part.toLowerCase());
  return t;
}

function buildRelatedIntentCards(data, limit = 4) {
  const inventory = getSiteInventory();
  const tokens = pageTokens(data);
  const cityToken = normalize(data.taxonomy?.city || '');
  const countryToken = normalize(data.taxonomy?.country || '');
  const citySlug = slugify(data.taxonomy?.city || '');
  const countrySlug = slugify(data.taxonomy?.country || '');

  const cards = [];

  // 1) Country hub if present
  if (countrySlug) {
    const countryHub = inventory.popularPicks.find((e) => e.slug === countrySlug);
    if (countryHub) {
      cards.push({ type: 'Country Hub', title: countryHub.title || `Popular Picks in ${data.taxonomy.country}`, url: countryHub.url });
    }
  }

  // 2) Sibling popular-picks in same city (different category)
  const siblings = inventory.popularPicks
    .filter((e) => e.slug !== data.slug)
    .filter((e) => cityToken && (e.searchText || '').includes(cityToken))
    .filter((e) => e.slug !== citySlug && e.slug !== countrySlug)
    .filter((e) => !(data.related?.manual || []).includes(e.slug))
    .map((e) => ({ entry: e, score: [...tokens].reduce((s, t) => s + ((e.searchText || '').includes(t) ? 1 : 0), 0) }))
    .sort((a, b) => b.score - a.score || a.entry.title.localeCompare(b.entry.title))
    .slice(0, Math.max(0, limit - cards.length - 1))
    .map(({ entry }) => ({ type: data.taxonomy.city || 'Same city', title: entry.title, url: entry.url }));
  cards.push(...siblings);

  // 3) Trip planner CTA card
  if (cards.length < limit) {
    const cityName = data.taxonomy.city || data.taxonomy.country || 'this destination';
    cards.push({ type: 'Trip Planner', title: `Free ${cityName} Itinerary`, url: '/plan' });
  }

  return cards.slice(0, limit);
}

// ============================================================
// Section renderers
// ============================================================
function renderHero(data) {
  const badge = data.hero?.badge || `${data.taxonomy?.category ? '⭐ ' : ''}Popular Picks${data.taxonomy?.city ? ' — ' + data.taxonomy.city : ''}`;
  return `    <section class="hero">
      <div class="hero-badge">${escapeHtml(badge)}</div>
      <h1>${escapeHtml(data.seo.h1)}</h1>
      <p class="subtitle">${escapeHtml(data.hero?.dek || data.seo.metaDescription || '')}</p>
    </section>`;
}

function renderMapPanel(mapData, mapPicks, mobile = false) {
  if (!mapData.enabled || !mapPicks.length) return '';
  const firstPick = mapPicks[0];
  const legend = mapPicks.map((p) => `        <li><a href="#${p.anchorId}">${escapeHtml(p.label)}</a></li>`).join('\n');
  return `    <section class="${mobile ? 'map-inline' : 'map-sidebar'}" data-map-panel="${mobile ? 'mobile' : 'desktop'}">
      <h2>${escapeHtml(mapData.title)}</h2>
      <div class="map-active-pick" data-map-active-pick>${escapeHtml(firstPick.label)}</div>
      <div class="popular-picks-map" data-map-canvas aria-label="${escapeHtml(mapData.title)}"></div>
      <div class="map-legend">
        <strong>Start with:</strong>
        <ul>
${legend}
        </ul>
        <p><a href="${escapeHtml(firstPick.ctaUrl || mapData.ctaUrl)}" target="_blank" rel="noopener" data-map-cta>${escapeHtml(mapData.ctaLabel)} →</a></p>
      </div>
    </section>`;
}

function resolveBestOverall(data) {
  const c = data.summary?.bestOverall || data.summary?.topPick || '';
  if (!c || !data.picks.length) return data.picks[0] ? data.picks[0].name : '';
  const m = data.picks.find((p) => p.name === c || c.startsWith(p.name));
  if (m && typeof m.reviewCount === 'number' && m.reviewCount < 10 && data.picks[0] && data.picks[0].name !== m.name) {
    return data.picks[0].name;
  }
  return m ? m.name : c;
}

function renderQuickAnswer(data) {
  const verdicts = data.picks.slice(0, 3)
    .map((p) => `            <li><strong>${escapeHtml(p.name)}:</strong> ${escapeHtml(buildVerdictText(p))}</li>`)
    .join('\n');
  const rows = [
    ['Best overall', resolveBestOverall(data)],
    ['Price range', data.summary?.priceRangeLocal || data.summary?.priceRangeUSD || ''],
    ['Top pick', data.summary?.topPick || (data.picks[0] ? data.picks[0].name : '')],
    ['Must-try', data.summary?.mustTry || data.summary?.bestBudgetOption || ''],
  ].filter(([, v]) => v);
  const rowsHtml = rows.map(([label, value]) => `              <div class="comparison-row"><dt>${escapeHtml(label)}</dt><dd>${escapeHtml(value)}</dd></div>`).join('\n');
  return `        <section class="quick-answer-section">
          <div class="quick-answer-card">
            <p class="eyebrow">Quick answer</p>
            <p class="quick-answer-lead"><strong>${escapeHtml(data.intro.answerFirst)}</strong></p>
            <dl class="quick-answer-grid">
${rowsHtml}
            </dl>
          </div>
          <div class="quick-answer-card">
            <p class="eyebrow">Top verdicts</p>
            <ul class="top-verdicts-list">
${verdicts}
            </ul>
          </div>
        </section>`;
}

function renderIntroSection(data) {
  const body = dedupeIntroBody(data.intro.answerFirst, data.intro.body || []);
  const paragraphs = body.map((p) => `        <p>${escapeHtml(p)}</p>`).join('\n');
  if (!paragraphs) return '';
  return `      <section class="intro-section">
${paragraphs}
      </section>`;
}

function renderMethodologySection(data) {
  if (!data.intro?.methodology) return '';
  return `        <section class="methodology-section">
          <h2>How we built this list</h2>
          <p>${escapeHtml(data.intro.methodology)}</p>
        </section>`;
}

function renderComparisonTable(data) {
  if (!data.picks.length) return '';
  const rows = data.picks.map((p) => {
    const style = p.styleLabel || (p.tags || [])[0] || '';
    const price = p.priceTier || p.priceRangeLocal || '';
    const rating = (typeof p.googleRating === 'number') ? `${p.googleRating}★` : '';
    const area = p.neighborhood || (p.address || '').split(',')[0] || '';
    return `          <tr>
            <td>${p.rank}</td>
            <td><a href="#${pickAnchorId(p)}">${escapeHtml(p.name)}</a></td>
            <td>${escapeHtml(style)}</td>
            <td>${escapeHtml(price)}</td>
            <td>${escapeHtml(rating)}</td>
            <td>${escapeHtml(area)}</td>
          </tr>`;
  }).join('\n');
  return `      <section class="comparison-table-section">
        <h2>All ${data.picks.length} spots at a glance</h2>
        <div class="comparison-table-wrapper">
          <table class="comparison-table">
            <thead>
              <tr><th>#</th><th>Name</th><th>Style</th><th>Price</th><th>Rating</th><th>Area</th></tr>
            </thead>
            <tbody>
${rows}
            </tbody>
          </table>
        </div>
      </section>`;
}

function renderFilterBar(data) {
  // Derive filter chips from per-pick fields. Only render if we have at least 2 distinct
  // values within a group — single-value groups offer nothing to filter.
  const groups = {};
  for (const p of data.picks) {
    if (p.styleLabel) (groups.style ||= new Set()).add(p.styleLabel);
    if (p.priceTier) (groups.price ||= new Set()).add(p.priceTier);
    if (p.neighborhood) (groups.area ||= new Set()).add(p.neighborhood);
  }
  const labels = { style: 'Style', price: 'Price', area: 'Area' };
  const chipParts = [];
  for (const [group, values] of Object.entries(groups)) {
    if (values.size < 2) continue;
    chipParts.push(`<span class="filter-label">${labels[group]}:</span>`);
    for (const v of [...values].sort()) {
      chipParts.push(`<span class="filter-chip" data-filter-group="${group}" data-filter-value="${escapeHtml(v)}">${escapeHtml(v)}</span>`);
    }
  }
  if (!chipParts.length) return '';
  return `      <div class="filter-bar">
        ${chipParts.join('\n        ')}
      </div>`;
}

function renderRestaurantSection(pick, data, mapData, isFirst = false) {
  const mapQuery = buildPickMapQuery(pick, data);
  const hours = parseHoursNote(pick.hoursNote);
  const firstTag = (pick.tags || [])[0] || pick.placeType || 'Spot';
  const verdictText = buildVerdictText(pick);

  const dataAttrs = [
    `id="${pickAnchorId(pick)}"`,
    pick.styleLabel ? `data-filter-style="${escapeHtml(pick.styleLabel)}"` : '',
    pick.priceTier ? `data-filter-price="${escapeHtml(pick.priceTier)}"` : '',
    pick.neighborhood ? `data-filter-area="${escapeHtml(pick.neighborhood)}"` : '',
    `data-map-name="${escapeHtml(`${pick.rank}. ${pick.name}`)}"`,
    `data-map-cta-url="${escapeHtml(pick.googleMapsUrl || mapData.ctaUrl)}"`,
    `data-map-query="${escapeHtml(mapQuery)}"`,
    typeof pick.lat === 'number' ? `data-map-lat="${pick.lat}"` : '',
    typeof pick.lng === 'number' ? `data-map-lng="${pick.lng}"` : '',
  ].filter(Boolean).join(' ');

  const ratingHtml = pick.googleRating
    ? `<span class="google-rating"><span class="star">★</span> ${pick.googleRating}${pick.reviewCount ? ` · ${Number(pick.reviewCount).toLocaleString()} reviews` : ''}</span>`
    : '';

  const detailsParts = [
    pick.priceRangeLocal ? `<span>💴 ${escapeHtml(pick.priceRangeLocal)}</span>` : '',
    pick.address || pick.neighborhood ? `<span>📍 ${escapeHtml(pick.address || pick.neighborhood)}</span>` : '',
    pick.googleMapsUrl ? `<a href="${escapeHtml(pick.googleMapsUrl)}" target="_blank" rel="noopener">📌 Google Maps →</a>` : '',
  ].filter(Boolean);

  const operationalTags = [
    pick.mealType,
    pick.reservationNeeded === true ? 'reservations-essential' : pick.reservationNeeded === false ? 'walk-in friendly' : '',
    pick.bestTimeToGo,
    pick.touristyLevel,
    ...(pick.paymentHints || []),
  ].filter(Boolean);

  const comparisonRows = [
    ['Best for', pick.bestFor || `${firstTag} in ${pick.neighborhood || data.taxonomy.city || ''}`.trim()],
    ['Strengths', buildStrengthsLine(pick)],
    ['Limitations', pick.limitations || ''],
    ['Price / value', buildValueLine(pick)],
    ['Why it made the list', pick.whyItMadeTheList || ''],
    ['What to order', stripWhatToOrderLead(pick.whatToOrder || '')],
    ['Best time to go', pick.bestTimeToGo || ''],
    ['Wait expectation', pick.waitExpectation || ''],
    ['Reservation', pick.reservationNeeded === true ? 'Recommended' : pick.reservationNeeded === false ? 'Usually not needed' : ''],
  ].filter(([, v]) => v);
  const comparisonHtml = comparisonRows
    .map(([label, value]) => `        <div class="comparison-row"><dt>${escapeHtml(label)}</dt><dd>${escapeHtml(value)}</dd></div>`)
    .join('\n');

  const provenance = buildProvenanceLine(pick);
  const hoursBlock = hours.length
    ? `\n    <div class="shop-hours">
        <details>
            <summary>${escapeHtml(hoursSummary(pick, hours))}</summary>
            <div class="hours-grid">
${hours.map((h) => `              <span>${escapeHtml(h.day)}</span><span>${escapeHtml(h.hours)}</span>`).join('\n')}
            </div>
        </details>
    </div>`
    : '';
  const contactHtml = (pick.phone || pick.website)
    ? `\n    <div class="shop-contact">${[
        pick.phone ? `<span>📞 <a href="tel:${escapeHtml(formatPhone(pick.phone))}">${escapeHtml(formatPhone(pick.phone))}</a></span>` : '',
        pick.website ? `<span>🌐 <a href="${escapeHtml(pick.website)}" target="_blank" rel="noopener">Website</a></span>` : '',
      ].filter(Boolean).join('')}</div>`
    : '';
  const imgAttrs = isFirst
    ? 'loading="eager" fetchpriority="high"'
    : 'loading="lazy"';
  const imageHtml = pick.photo
    ? `\n    <img src="${escapeHtml(absoluteUrl(pick.photo))}" alt="${escapeHtml(pick.name)} in ${escapeHtml(pick.neighborhood || pick.address || data.taxonomy.city || '')}" style="width:100%;border-radius:12px;margin-bottom:1rem;" ${imgAttrs} width="1200" height="675" decoding="async">`
    : '';
  const quotesHtml = (pick.redditQuotes || []).map((q) => `\n    <div class="reddit-quote">
        “${escapeHtml(q.quote)}”
        ${q.source ? `<span class="source">— ${escapeHtml(q.source)}</span>` : ''}
    </div>`).join('');

  return `<!-- VENUE ${pick.rank} -->
<section class="restaurant-section" ${dataAttrs}>
    <div class="restaurant-header">
        <h2><span class="restaurant-number">${pick.rank}</span>${escapeHtml(pick.name)}</h2>
        <span class="cuisine-tag ${cuisineTagClass(pick)}">${escapeHtml(firstTag)}</span>
        ${ratingHtml}
    </div>
    <div class="restaurant-details">${detailsParts.join('')}</div>
    <div class="pick-quick-take">
      <strong>Verdict:</strong> ${escapeHtml(verdictText)}
    </div>${operationalTags.length ? `\n    <div class="pick-tag-list operational-tags"><span>${escapeHtml(operationalTags.join(' / '))}</span></div>` : ''}

    <div class="comparison-card">
      <h3>Quick comparison</h3>
      <dl class="comparison-grid">
${comparisonHtml}
      </dl>
    </div>${provenance ? `\n    <div class="pick-provenance">${escapeHtml(provenance)}</div>` : ''}${hoursBlock}${contactHtml}${imageHtml}${quotesHtml}
</section>`;
}

function buildStrengthsLine(pick) {
  const out = [];
  if (typeof pick.googleRating === 'number' && pick.reviewCount) out.push(`${pick.googleRating}★ from ${Number(pick.reviewCount).toLocaleString()} reviews`);
  if (Array.isArray(pick.knownForTags) && pick.knownForTags.length) out.push(`Known for ${pick.knownForTags.slice(0, 2).join(', ')}`);
  if (pick.address) out.push(pick.address);
  return out.slice(0, 3).join(' · ');
}

function buildValueLine(pick) {
  if (pick.priceRangeLocal && isLikelyPriceRange(pick.priceRangeLocal)) {
    return `${pick.priceRangeLocal}${pick.googleRating ? ` · ${pick.googleRating}★` : ''}`;
  }
  if (pick.googleRating && pick.reviewCount) return `${pick.googleRating}★ from ${Number(pick.reviewCount).toLocaleString()} reviews`;
  if (pick.googleRating) return `${pick.googleRating}★ Google rating`;
  return '';
}

function buildProvenanceLine(pick) {
  const p = pick?.provenance || {};
  const bits = [];
  if (p.sourceCount != null) bits.push(`${p.sourceCount} sources`);
  if (Array.isArray(p.sourceTypes) && p.sourceTypes.length) bits.push(p.sourceTypes.join(', '));
  if (p.lastVerified) bits.push(`verified ${p.lastVerified}`);
  if (p.confidence) bits.push(`${p.confidence} confidence`);
  return bits.length ? `Source quality: ${bits.join(' · ')}` : '';
}

function renderFaqSection(data) {
  if (!Array.isArray(data.faq) || !data.faq.length) return '';
  const items = data.faq.map((q) => `        <div class="faq-item">
          <h3>${escapeHtml(q.question)}</h3>
          <p>${escapeHtml(q.answer)}</p>
        </div>`).join('\n');
  return `      <section class="faq-section">
        <h2>Frequently asked questions</h2>
${items}
      </section>`;
}

function renderRelatedSection(data) {
  const cards = buildRelatedIntentCards(data, 4);
  if (!cards.length) return '';
  const cityOrCountry = data.taxonomy.city || data.taxonomy.country || '';
  const subtitle = cityOrCountry ? `More Popular Picks from ${cityOrCountry}:` : 'More Popular Picks:';
  const html = cards.map((c) => `          <a href="${escapeHtml(c.url)}" class="intent-card">
            <span class="intent-type">${escapeHtml(c.type)}</span>
            <strong>${escapeHtml(c.title)}</strong>
          </a>`).join('\n');
  return `      <section class="related-section">
        <h2>Related guides</h2>
        <p class="related-intro">${escapeHtml(subtitle)}</p>
        <div class="intent-grid">
${html}
        </div>
      </section>`;
}

function renderPlanningIntroSection(data) {
  const paragraphs = data.intro?.planningParagraphs || [];
  if (!paragraphs.length) return '';
  const cityOrCountry = data.taxonomy.city || data.taxonomy.country || '';
  const heading = data.intro?.planningHeading || `Planning your ${cityOrCountry} ${data.taxonomy?.category || 'trip'}`;
  const html = paragraphs.map((p, i) => i === 0
    ? `        <p><strong>${escapeHtml(p)}</strong></p>`
    : `        <p>${escapeHtml(p)}</p>`).join('\n');
  return `      <section class="intro-section" style="margin-top:1.4rem;">
        <h2>${escapeHtml(heading)}</h2>
${html}
      </section>`;
}

function renderCtaSection(data) {
  const place = data.taxonomy.city || data.taxonomy.country || 'your trip';
  return `<!-- social-proof:end --><section class="cta-section">
  <h2>Plan your ${escapeHtml(place)} trip</h2>
  <p>Get a free custom itinerary for ${escapeHtml(place)} — built from real traveler insights.</p>
  <a href="/plan" class="cta-btn">Get a Free Itinerary →</a>
</section>`;
}

// ============================================================
// Page-shell renderers (nav, footer, head includes)
// ============================================================
function renderNav() {
  return `  <!-- @include:nav:start -->
<a class="skip-link" href="#main">Skip to main content</a>
<nav>
    <a href="/" class="logo"><img class="owl-default" src="https://img.tabiji.ai/tabiji-owl-logo.png" alt="tabiji.ai" style="height:32px;" loading="lazy" width="32" height="32" decoding="async"><img class="owl-fly" src="https://img.tabiji.ai/tabiji-owl-logo-flying.png?v=2" alt="" style="height:32px;" width="32" height="32" decoding="async">tabiji<span>.ai</span></a>
    <button class="hamburger" onclick="document.querySelector('.nav-links').classList.toggle('open')" aria-label="Menu">☰</button>
    <div class="nav-links">
        <div class="nav-dropdown">
            <button class="nav-dropdown-toggle" onclick="this.parentElement.classList.toggle('open')">Explore</button>
            <div class="nav-dropdown-menu">
                <a href="/popular-picks/">⭐ Popular Picks</a>
                <a href="/countries/">🗺 Country Guides</a>
                <a href="/compare/">🆚 Compare Destinations</a>
                <a href="/health/">🏥 Travel Health Tips</a>
                <a href="/api/">🔌 API</a>
            </div>
        </div>
        <a href="/trip-planner/">Trip Planner</a>
        <a href="/scams/">Tourist Scams</a>
        <a href="/about/">About</a>
        <a href="/books/" class="cta-nav">Get Travel Safety Books</a>
    </div>
</nav>
<!-- @include:nav:end -->`;
}

function renderFooter() {
  return `<!-- @include:footer:start -->
<footer>
  <div class="footer-inner">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="/" class="footer-logo">tabiji<span>.ai</span></a>
        <p class="footer-tagline">Travel safety, country by country.</p>
      </div>
      <div class="footer-col">
        <h4>Explore</h4>
        <ul>
          <li><a href="/books/">Travel Safety Books</a></li>
          <li><a href="/scams/">Tourist Scams</a></li>
          <li><a href="/countries/">Country Guides</a></li>
          <li><a href="/popular-picks/">Popular Picks</a></li>
          <li><a href="/trip-planner/">Trip Planner</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Follow</h4>
        <ul>
          <li><a href="https://www.instagram.com/tabiji.ai/" target="_blank" rel="noopener">Instagram</a></li>
          <li><a href="https://www.youtube.com/@tabijiai" target="_blank" rel="noopener">YouTube</a></li>
          <li><a href="https://www.pinterest.com/tabijiai/" target="_blank" rel="noopener">Pinterest</a></li>
          <li><a href="https://x.com/tabijiai" target="_blank" rel="noopener">X</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <ul>
          <li><a href="/about/">About</a></li>
          <li><a href="/media/">Media Studio</a></li>
          <li><a href="/api/">API</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-legal">
      <p class="footer-copyright">© 2026 tabiji.ai</p>
      <div class="footer-legal-links">
        <a href="/terms/">Terms of Service</a><span class="footer-sep" aria-hidden="true">·</span><a href="/privacy/">Privacy Policy</a><span class="footer-sep" aria-hidden="true">·</span><a href="/delete-data/">Delete My Data</a>
      </div>
    </div>
  </div>
</footer>
<!-- @include:footer:end -->`;
}

function renderSharedHeadIncludes() {
  return `<!-- @include:shared-head:start -->
<link rel="preconnect" href="https://maps.googleapis.com" crossorigin>
<link rel="dns-prefetch" href="https://maps.googleapis.com">
<link rel="stylesheet" href="/assets/shared-shell.css">
<meta name="theme-color" content="#2D3A5C">
<script defer src="/assets/shared-shell.js"></script>
<!-- @include:shared-head:end -->`;
}

// ============================================================
// Inline <style> block — copies the gold-standard CSS from
// new-york-steak. Kept inline (not externalised) so each page
// renders with no additional network requests beyond shared-shell.css.
// ============================================================
function renderInlineStyle() {
  return `<style>
      :root {
        --indigo:#2D3A5C; --indigo-light:#3D4E7A; --warm-cream:#F5F0E8; --sand:#E8DFD0;
        --earth:#7A6343; --terracotta:#A85A37; --white:#FEFCF9; --text:#2C2419; --text-muted:#6B5D4F;
      }
      * { margin:0; padding:0; box-sizing:border-box; }
      body { font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif; color:var(--text); background:var(--white); line-height:1.6; -webkit-font-smoothing:antialiased; }
      a { color:var(--terracotta); text-decoration:none; }
      .skip-link { position:absolute; left:-9999px; top:0; padding:.6rem 1rem; background:var(--indigo); color:#fff; z-index:200; }
      .skip-link:focus { left:1rem; top:1rem; }
      .hero { padding:0.5rem 1.5rem 2rem; max-width:840px; margin:0 auto; }
      .hero-badge { display:inline-block; background:var(--sand); color:var(--earth); padding:.35rem 1rem; border-radius:999px; font-size:.9rem; margin-bottom:1rem; }
      .hero h1 { font-size:clamp(2rem,4.7vw,3rem); line-height:1.12; color:var(--indigo); margin:0 0 1rem; letter-spacing:-.03em; }
      .subtitle { font-size:1.08rem; color:var(--text-muted); max-width:680px; }
      .page-layout { max-width:1260px; margin:0 auto; padding:0 1.5rem 4rem; display:grid; grid-template-columns:320px minmax(0,1fr); gap:2rem; }
      .content { min-width:0; }
      .map-sidebar { position:sticky; top:92px; align-self:start; background:var(--warm-cream); border:1px solid var(--sand); border-radius:18px; padding:1rem; }
      .popular-picks-map { width:100%; height:360px; border-radius:12px; background:var(--sand); overflow:hidden; }
      .map-sidebar h2, .map-inline h2 { margin:.2rem 0 .35rem; color:var(--indigo); font-size:1.05rem; }
      .map-active-pick { color:var(--earth); font-size:.92rem; font-weight:700; margin:0 0 .8rem; }
      .map-legend ul { margin:.75rem 0; padding-left:1.2rem; }
      .map-inline { display:none; background:var(--warm-cream); border:1px solid var(--sand); border-radius:18px; padding:1rem; margin-bottom:1.4rem; }
      .restaurant-section { scroll-margin-top:100px; transition:background-color .18s ease, box-shadow .18s ease, border-radius .18s ease; border-bottom:1px solid var(--sand); padding:2.5rem 0; }
      .restaurant-section:first-of-type { padding-top:0; }
      .restaurant-section:last-of-type { border-bottom:none; }
      .restaurant-section.active { background:#fffaf4; border-radius:14px; box-shadow:0 0 0 1px var(--sand) inset; padding-left:1rem; padding-right:1rem; }
      .restaurant-section.filtered-out { display:none !important; }
      .quick-answer-section { display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:1rem; margin-bottom:1.4rem; }
      .quick-answer-card, .intro-section, .methodology-section, .faq-section, .related-section, .comparison-table-section { background:white; border:1px solid var(--sand); border-radius:18px; padding:1.35rem 1.4rem; }
      .quick-answer-section, .intro-section, .methodology-section, .faq-section, .related-section, .comparison-table-section { margin-bottom:1.4rem; }
      .eyebrow { text-transform:uppercase; letter-spacing:.08em; font-size:.78rem; font-weight:700; color:var(--earth); margin-bottom:.55rem; }
      .quick-answer-lead { margin-bottom:1rem; }
      .quick-answer-grid, .comparison-grid { display:grid; gap:.7rem; }
      .comparison-row { display:grid; grid-template-columns:150px minmax(0, 1fr); gap:.5rem 1rem; align-items:start; }
      .comparison-row dt { font-weight:700; color:var(--indigo); }
      .comparison-row dd { color:var(--text); }
      .top-verdicts-list { padding-left:1.1rem; display:grid; gap:.75rem; }
      .restaurant-header { display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:.75rem; flex-wrap:wrap; gap:.5rem; }
      .restaurant-header h2 { font-size:1.35rem; font-weight:700; color:var(--indigo); }
      .restaurant-number { display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:50%; background:var(--terracotta); color:white; font-size:.8rem; font-weight:700; margin-right:.5rem; flex-shrink:0; }
      .cuisine-tag { display:inline-block; padding:.2rem .6rem; border-radius:6px; font-size:.78rem; font-weight:600; white-space:nowrap; }
      .tag-ramen{background:#FFF3E0;color:#E65100}.tag-tonkatsu{background:#FBE9E7;color:#BF360C}.tag-gyudon{background:#EFEBE9;color:#4E342E}.tag-udon{background:#E8EAF6;color:#283593}.tag-tempura{background:#E0F2F1;color:#00695C}.tag-sushi{background:#E3F2FD;color:#1565C0}.tag-yakitori{background:#FCE4EC;color:#AD1457}.tag-tsukemen{background:#FFF8E1;color:#FF8F00}.tag-gyukatsu{background:#F1F8E9;color:#558B2F}.tag-kushikatsu{background:#F3E5F5;color:#7B1FA2}.tag-shabu{background:#EDE7F6;color:#512DA8}.tag-omurice{background:#FFFDE7;color:#F9A825}.tag-hamburg{background:#EFEBE9;color:#6D4C41}.tag-snack{background:#FCE4EC;color:#C2185B}.tag-pizza{background:#FFE0B2;color:#BF360C}.tag-steak{background:#EFEBE9;color:#3E2723}.tag-bbq{background:#FFCCBC;color:#BF360C}.tag-classic{background:#E8DFD0;color:#5D4037}.tag-historic{background:#D7CCC8;color:#3E2723}.tag-modern{background:#E1F5FE;color:#01579B}.tag-korean{background:#FCE4EC;color:#880E4F}.tag-regional{background:#ECEFF1;color:#455A64}
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
      .intent-grid { display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:.9rem; }
      .intent-card { display:block; background:var(--warm-cream); border:1px solid var(--sand); border-radius:14px; padding:1rem; color:var(--text); }
      .intent-card:hover { border-color:var(--terracotta); transform:translateY(-1px); }
      .intent-type { display:block; text-transform:uppercase; letter-spacing:.08em; font-size:.72rem; font-weight:700; color:var(--earth); margin-bottom:.45rem; }
      .comparison-table-wrapper { overflow-x:auto; }
      .comparison-table { width:100%; border-collapse:collapse; font-size:.92rem; }
      .comparison-table th { text-align:left; padding:.55rem .6rem; background:var(--warm-cream); color:var(--indigo); border-bottom:1px solid var(--sand); }
      .comparison-table td { padding:.55rem .6rem; border-bottom:1px solid var(--sand); color:var(--text); }
      .comparison-table tr:last-child td { border-bottom:none; }
      .filter-bar { display:flex; flex-wrap:wrap; gap:.5rem; margin-bottom:1.4rem; padding:1rem; background:white; border:1px solid var(--sand); border-radius:18px; align-items:center; }
      .filter-bar .filter-label { font-weight:700; color:var(--indigo); font-size:.85rem; margin-right:.5rem; }
      .filter-chip { display:inline-flex; align-items:center; padding:.35rem .8rem; border-radius:999px; border:1px solid var(--sand); background:white; color:var(--text-muted); font-size:.82rem; cursor:pointer; transition:all .15s; user-select:none; }
      .filter-chip:hover { border-color:var(--terracotta); color:var(--terracotta); }
      .filter-chip.active { background:var(--terracotta); color:white; border-color:var(--terracotta); }
      .cta-section { max-width:900px; margin:1.5rem auto; padding:2rem 1.5rem; background:var(--warm-cream); border:1px solid var(--sand); border-radius:18px; text-align:center; }
      .cta-section h2 { color:var(--indigo); margin-bottom:.5rem; }
      .cta-section p { color:var(--text-muted); margin-bottom:1rem; }
      .cta-btn { display:inline-block; background:var(--terracotta); color:#fff; padding:.65rem 1.2rem; border-radius:8px; font-weight:600; }
      .cta-btn:hover { background:var(--indigo); }
      @media (max-width:980px) { .page-layout { grid-template-columns:1fr; } .map-sidebar { display:none; } .map-inline { display:block; } .quick-answer-section { grid-template-columns:1fr; } .comparison-row { grid-template-columns:1fr; } .restaurant-section { padding:2rem 0; } .restaurant-section.active { padding-left:.85rem; padding-right:.85rem; } }
    </style>`;
}

// ============================================================
// Bottom scripts: map config + IO observer (FIXED) + Maps loader + filter chips
// ============================================================
function renderBottomScripts(mapData, mapPicks) {
  const enabled = mapData.enabled && mapPicks.length > 0;
  const config = JSON.stringify({
    enabled,
    title: mapData.title,
    ctaLabel: mapData.ctaLabel,
    defaultCtaUrl: mapData.ctaUrl,
    picks: mapPicks,
  });

  return `  <script>
    window.__POPULAR_PICKS_MAP__ = ${config};
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
              fillColor: isActive ? '#2D3A5C' : '#A85A37',
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
              label: { text: String(pick.rank), color: '#FFFFFF', fontWeight: '700' }
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
        // Thin trigger stripe near top-third of viewport. threshold:0 fires on any pixel
        // crossing, avoiding the prior bug where tall sections never reached the 0.2 ratio
        // and the active highlight only updated intermittently.
        var inStripe = new Set();
        var observer = new IntersectionObserver(function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) inStripe.add(entry.target);
            else inStripe.delete(entry.target);
          });
          var active = sections.find(function (s) { return inStripe.has(s); });
          if (active) setActive(active);
        }, { rootMargin: '-35% 0px -55% 0px', threshold: 0 });
        sections.forEach(function (section) { observer.observe(section); });
      }
    }());
  </script>${enabled ? `\n  <script async src="https://maps.googleapis.com/maps/api/js?key=${GOOGLE_MAPS_API_KEY}&callback=initPopularPicksMaps"></script>` : ''}

<script>
document.addEventListener('DOMContentLoaded', function() {
    const chips = document.querySelectorAll('.filter-chip');
    const sections = document.querySelectorAll('.restaurant-section');

    chips.forEach(chip => {
        chip.addEventListener('click', function() {
            const group = this.dataset.filterGroup;

            if (this.classList.contains('active')) {
                this.classList.remove('active');
            } else {
                document.querySelectorAll(\`.filter-chip[data-filter-group="\${group}"]\`).forEach(c => c.classList.remove('active'));
                this.classList.add('active');
            }

            const activeFilters = {};
            document.querySelectorAll('.filter-chip.active').forEach(c => {
                activeFilters[c.dataset.filterGroup] = c.dataset.filterValue;
            });

            sections.forEach(section => {
                let show = true;
                if (activeFilters.style && (section.dataset.filterStyle || '').toLowerCase() !== activeFilters.style.toLowerCase()) show = false;
                if (activeFilters.price && section.dataset.filterPrice !== activeFilters.price) show = false;
                if (activeFilters.area && section.dataset.filterArea !== activeFilters.area) show = false;
                section.classList.toggle('filtered-out', !show);
            });
        });
    });
});
</script>`;
}

// ============================================================
// Top-level renderer
// ============================================================
function renderPage(data) {
  const validation = validateSource(data);
  if (validation.errors.length) {
    throw new Error(`Cannot render invalid source:\n${validation.errors.join('\n')}`);
  }

  const mapData = buildDerivedMap(data);
  const mapPicks = buildMapPicks(data.picks, data, mapData);

  const restaurantSections = data.picks
    .map((p, i) => renderRestaurantSection(p, data, mapData, i === 0))
    .join('\n');

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
    ${renderInlineStyle()}
${renderSharedHeadIncludes()}
</head>
<body>
${renderNav()}

${renderHero(data)}

  <div class="page-layout">
    <aside>
${renderMapPanel(mapData, mapPicks, false)}
    </aside>

    <main id="main" tabindex="-1" class="content">
${renderQuickAnswer(data)}

${renderIntroSection(data)}

${renderMapPanel(mapData, mapPicks, true)}

${renderMethodologySection(data)}

${renderComparisonTable(data)}

      <section class="pick-list">
${renderFilterBar(data)}
${restaurantSections}
      </section>

${renderFaqSection(data)}

${renderRelatedSection(data)}

${renderPlanningIntroSection(data)}

    </main>
  </div>

${renderCtaSection(data)}

${renderFooter()}

${renderBottomScripts(mapData, mapPicks)}
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
