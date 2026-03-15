#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { renderMeta, escapeHtml, absoluteUrl } = require('./render-meta');
const { renderSchema } = require('./render-schema');
const { loadJson, validateSource } = require('./validate-source');

function renderRichTextParagraphs(items = []) {
  return items.map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`).join('');
}

function formatPhone(phone) {
  if (!phone) return '';
  return phone.replace(/\s+/g, ' ').trim();
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

function buildDerivedMap(data) {
  const query = [data.taxonomy.neighborhood, data.taxonomy.city, data.taxonomy.category]
    .filter(Boolean)
    .join(' ');
  const embedUrl = data.map?.embedUrl || `https://www.google.com/maps?q=${encodeURIComponent(query)}&output=embed`;
  const ctaUrl = data.map?.ctaUrl || `https://www.google.com/maps/search/${encodeURIComponent(query)}`;
  return {
    enabled: data.map?.enabled !== false,
    title: data.map?.title || 'Area map',
    embedUrl,
    ctaLabel: data.map?.ctaLabel || 'Open in Google Maps',
    ctaUrl,
  };
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

function renderMapPanel(mapData, picks, mobile = false) {
  if (!mapData.enabled) return '';
  const topPicks = picks.slice(0, 6).map((pick) => `
      <li>
        <a href="#pick-${pick.rank}">${pick.rank}. ${escapeHtml(pick.name)}</a>
      </li>`).join('');

  return `
    <section class="${mobile ? 'map-inline' : 'map-sidebar'}">
      <h2>${escapeHtml(mapData.title)}</h2>
      <iframe src="${escapeHtml(mapData.embedUrl)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      <div class="map-legend">
        <strong>Start with:</strong>
        <ul>${topPicks}</ul>
        <p><a href="${escapeHtml(mapData.ctaUrl)}" target="_blank" rel="noopener">${escapeHtml(mapData.ctaLabel)} →</a></p>
      </div>
    </section>`;
}

function renderPick(pick) {
  const hours = parseHoursNote(pick.hoursNote);
  const tags = (pick.cuisineTags || []).map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`).join('');
  const quotes = (pick.redditQuotes || []).map((quote) => `
        <blockquote class="reddit-quote">
          <p>“${escapeHtml(quote.quote)}”</p>
          ${quote.source ? `<footer>${escapeHtml(quote.source)}</footer>` : ''}
        </blockquote>`).join('');

  const metaBits = [
    pick.priceRangeLocal ? `💴 ${escapeHtml(pick.priceRangeLocal)}` : '',
    pick.googleRating ? `★ ${escapeHtml(String(pick.googleRating))}${pick.reviewCount ? ` · ${escapeHtml(pick.reviewCount.toLocaleString())} reviews` : ''}` : '',
    pick.address ? `📍 ${escapeHtml(pick.address)}` : ''
  ].filter(Boolean).map((item) => `<span>${item}</span>`).join('');

  const utilityLinks = [
    pick.googleMapsUrl ? `<span>📌 <a href="${escapeHtml(pick.googleMapsUrl)}" target="_blank" rel="noopener">Google Maps</a></span>` : '',
    pick.phone ? `<span>📞 <a href="tel:${escapeHtml(formatPhone(pick.phone))}">${escapeHtml(formatPhone(pick.phone))}</a></span>` : '',
    pick.website ? `<span>🌐 <a href="${escapeHtml(pick.website)}" target="_blank" rel="noopener">Website</a></span>` : ''
  ].filter(Boolean).join('');

  return `
      <article class="pick-card" id="pick-${pick.rank}">
        <div class="pick-header">
          <h2><span class="rank">${pick.rank}</span>${escapeHtml(pick.name)}</h2>
          <div class="tag-row">${tags}</div>
        </div>

        ${pick.photo ? `<img class="pick-photo" src="${escapeHtml(absoluteUrl(pick.photo))}" alt="${escapeHtml(pick.name)}" loading="lazy">` : ''}

        <div class="pick-meta">${metaBits}</div>
        ${utilityLinks ? `<div class="pick-links">${utilityLinks}</div>` : ''}

        <div class="pick-copy">
          <p><strong>Why it made the list:</strong> ${escapeHtml(pick.whyItMadeTheList)}</p>
          <div class="what-to-order"><strong>What to order:</strong> ${escapeHtml(pick.whatToOrder)}</div>
          <p><strong>tabiji verdict:</strong> ${escapeHtml(pick.insiderTip)}</p>
          ${quotes}
        </div>

        ${hours.length ? `
          <details class="shop-hours">
            <summary>Hours</summary>
            <div class="hours-grid">
              ${hours.map((item) => `<span>${escapeHtml(item.day)}</span><span>${escapeHtml(item.hours)}</span>`).join('')}
            </div>
          </details>` : ''}
      </article>`;
}

function renderPage(data) {
  const validation = validateSource(data);
  if (validation.errors.length) {
    throw new Error(`Cannot render invalid source:\n${validation.errors.join('\n')}`);
  }

  const mapData = buildDerivedMap(data);
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
      * { box-sizing:border-box; }
      body { margin:0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif; background:var(--white); color:var(--text); line-height:1.6; }
      a { color:var(--terracotta); text-decoration:none; }
      nav {
        position:sticky; top:0; z-index:100; background:rgba(254,252,249,.92); backdrop-filter:blur(20px);
        border-bottom:1px solid var(--sand); padding:1rem 1.5rem; display:flex; justify-content:space-between; align-items:center;
      }
      nav .logo { font-size:1.3rem; font-weight:700; color:var(--indigo); }
      nav .cta-nav { background:var(--terracotta); color:white; padding:.55rem 1rem; border-radius:8px; }
      .hero { padding:6.5rem 1.5rem 2rem; max-width:840px; margin:0 auto; }
      .hero-badge { display:inline-block; background:var(--sand); color:var(--earth); padding:.35rem 1rem; border-radius:999px; font-size:.9rem; margin-bottom:1rem; }
      .hero h1 { font-size:clamp(2rem, 4.7vw, 3rem); line-height:1.12; color:var(--indigo); margin:0 0 1rem; letter-spacing:-.03em; }
      .subtitle { font-size:1.08rem; color:var(--text-muted); max-width:680px; }
      .hero-meta { display:flex; flex-wrap:wrap; gap:1rem 1.5rem; color:var(--earth); font-size:.92rem; margin-top:1.2rem; }
      .page-layout { max-width:1260px; margin:0 auto; padding:0 1.5rem 4rem; display:grid; grid-template-columns:minmax(0, 1fr) 320px; gap:2rem; }
      .content { min-width:0; }
      .map-sidebar { position:sticky; top:92px; align-self:start; background:var(--warm-cream); border:1px solid var(--sand); border-radius:18px; padding:1rem; }
      .map-sidebar iframe, .map-inline iframe { width:100%; height:360px; border:0; border-radius:12px; background:var(--sand); }
      .map-sidebar h2, .map-inline h2 { margin:.2rem 0 .8rem; color:var(--indigo); font-size:1.05rem; }
      .map-legend ul { margin:.75rem 0; padding-left:1.2rem; }
      .intro-section, .methodology-section, .faq-section, .related-section {
        background:white; border:1px solid var(--sand); border-radius:18px; padding:1.35rem 1.4rem; margin-bottom:1.4rem;
      }
      .map-inline { display:none; background:var(--warm-cream); border:1px solid var(--sand); border-radius:18px; padding:1rem; margin-bottom:1.4rem; }
      .pick-list { display:grid; gap:1.3rem; }
      .pick-card { background:white; border:1px solid var(--sand); border-radius:18px; overflow:hidden; }
      .pick-header { padding:1.2rem 1.2rem 0; display:flex; justify-content:space-between; gap:1rem; align-items:flex-start; }
      .pick-card h2 { margin:0; color:var(--indigo); font-size:1.45rem; line-height:1.2; }
      .rank { display:inline-flex; width:2rem; height:2rem; margin-right:.7rem; border-radius:999px; background:var(--indigo); color:white; align-items:center; justify-content:center; font-size:.92rem; vertical-align:middle; }
      .tag-row { display:flex; flex-wrap:wrap; gap:.4rem; }
      .tag { display:inline-block; background:var(--warm-cream); border-radius:999px; padding:.22rem .62rem; font-size:.83rem; color:var(--earth); }
      .pick-photo { width:100%; max-height:330px; object-fit:cover; display:block; margin-top:1rem; }
      .pick-meta, .pick-links { padding:0 1.2rem; display:flex; flex-wrap:wrap; gap:.7rem 1rem; color:var(--earth); font-size:.95rem; margin-top:1rem; }
      .pick-copy { padding:1rem 1.2rem 1.2rem; }
      .what-to-order { background:var(--warm-cream); border-left:3px solid var(--terracotta); padding:.85rem 1rem; border-radius:10px; margin:1rem 0; }
      .reddit-quote { margin:1rem 0 0; padding:1rem; background:#faf7f3; border-left:3px solid var(--terracotta); }
      .reddit-quote p { margin:0 0 .4rem; }
      .reddit-quote footer { color:var(--earth); font-size:.92rem; }
      .shop-hours { border-top:1px solid var(--sand); padding:0 1.2rem 1.2rem; }
      .shop-hours summary { cursor:pointer; color:var(--indigo); font-weight:700; padding-top:1rem; }
      .hours-grid { display:grid; grid-template-columns:auto 1fr; gap:.4rem 1rem; margin-top:.75rem; color:var(--text-muted); font-size:.94rem; }
      .faq-item + .faq-item { border-top:1px solid var(--sand); padding-top:1rem; margin-top:1rem; }
      .faq-item h3 { color:var(--indigo); margin:.2rem 0 .45rem; }
      ul.related { padding-left:1.2rem; margin:0; }
      footer { max-width:1260px; margin:0 auto; padding:0 1.5rem 3rem; color:var(--text-muted); }
      @media (max-width: 980px) {
        .page-layout { grid-template-columns:1fr; }
        .map-sidebar { display:none; }
        .map-inline { display:block; }
      }
    </style>
</head>
<body>
  <nav>
    <a class="logo" href="/">tabiji.ai</a>
    <a class="cta-nav" href="/plan.html">Plan My Trip</a>
  </nav>

  ${renderHero(data)}

  <div class="page-layout">
    <main class="content">
      <section class="intro-section">
        <p><strong>${escapeHtml(data.intro.answerFirst)}</strong></p>
        ${renderRichTextParagraphs(data.intro.body)}
      </section>

      ${renderMapPanel(mapData, data.picks, true)}

      ${data.intro.methodology ? `
        <section class="methodology-section">
          <h2>How we built this list</h2>
          <p>${escapeHtml(data.intro.methodology)}</p>
        </section>` : ''}

      <section class="pick-list">
        ${data.picks.map(renderPick).join('')}
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

    <aside>
      ${renderMapPanel(mapData, data.picks, false)}
    </aside>
  </div>

  <footer>Generated from structured source data.</footer>
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

module.exports = { renderPage, parseHoursNote, buildDerivedMap };
