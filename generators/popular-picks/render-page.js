#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { renderMeta, escapeHtml, absoluteUrl } = require('./render-meta');
const { renderSchema } = require('./render-schema');
const { loadJson, validateSource } = require('./validate-source');

const GOOGLE_MAPS_API_KEY = 'AIzaSyBP0yidMjJEECgkIiZz2lw1NLsQ7jdASYc';

function renderRichTextParagraphs(items = []) {
  return items.map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`).join('');
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
  const first = (pick.cuisineTags || [])[0] || '';
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

function renderMapPanel(mapData, mapPicks, mobile = false) {
  if (!mapData.enabled || !mapPicks.length) return '';
  const firstPick = mapPicks[0];
  const topPicks = mapPicks.slice(0, 6).map((pick) => `
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

function renderPick(pick, data, mapData) {
  const mapQuery = buildPickMapQuery(pick, data);
  const hours = parseHoursNote(pick.hoursNote);
  const firstTag = (pick.cuisineTags || [])[0] || pick.placeType || 'Restaurant';
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
        ${pick.priceRangeLocal ? `<span>💴 ${escapeHtml(pick.priceRangeLocal)}</span>` : ''}
        ${pick.address ? `<span>📍 ${escapeHtml(pick.address)}</span>` : ''}
        ${pick.googleMapsUrl ? `<a href="${escapeHtml(pick.googleMapsUrl)}" target="_blank" rel="noopener">📌 Google Maps →</a>` : ''}
    </div>
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
${(pick.whatToOrder && !pick.whatToOrder.includes('is a featured pick in this guide')) ? `<div class="what-to-order">
        <strong>What to order:</strong> ${escapeHtml(stripWhatToOrderLead(pick.whatToOrder))}</div>` : ''}
    ${quoteBlocks}
    <div class="tabiji-verdict">
        <strong>tabiji verdict:</strong> ${escapeHtml(pick.insiderTip)}
    </div>
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
  const relatedLinks = (data.related.manual || []).map((slug) => `
        <li><a href="/popular-picks/${escapeHtml(slug)}/">${escapeHtml(slug.replace(/-/g, ' '))}</a></li>`).join('');

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
      .intro-section, .methodology-section, .faq-section, .related-section { background:white; border:1px solid var(--sand); border-radius:18px; padding:1.35rem 1.4rem; margin-bottom:1.4rem; }
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
      .shop-hours { margin-bottom:.9rem; }
      .shop-hours summary { cursor:pointer; color:var(--indigo); font-weight:700; }
      .hours-grid { display:grid; grid-template-columns:auto 1fr; gap:.4rem 1rem; margin-top:.75rem; color:var(--text-muted); font-size:.94rem; }
      .what-to-order { background:var(--warm-cream); border-left:3px solid var(--terracotta); padding:.85rem 1rem; border-radius:10px; margin:1rem 0; }
      .reddit-quote { margin:1rem 0 0; padding:1rem; background:#faf7f3; border-left:3px solid var(--terracotta); }
      .source { display:block; margin-top:.4rem; color:var(--earth); font-size:.92rem; }
      .tabiji-verdict { margin-top:1rem; padding:1rem; background:#fffaf4; border:1px solid var(--sand); border-radius:12px; }
      .faq-item + .faq-item { border-top:1px solid var(--sand); padding-top:1rem; margin-top:1rem; }
      .faq-item h3 { color:var(--indigo); margin:.2rem 0 .45rem; }
      ul.related { padding-left:1.2rem; margin:0; }
      footer { max-width:1260px; margin:0 auto; padding:0 1.5rem 3rem; color:var(--text-muted); }
      @media (max-width:980px) { .page-layout { grid-template-columns:1fr; } .map-sidebar { display:none; } .map-inline { display:block; } .restaurant-section { padding:2rem 0; } .restaurant-section.active { padding-left:.85rem; padding-right:.85rem; } }
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
      <section class="intro-section">
        <p><strong>${escapeHtml(data.intro.answerFirst)}</strong></p>
        ${renderRichTextParagraphs(introBody)}
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

      <section class="related-section">
        <h2>Related Recommendations</h2>
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
