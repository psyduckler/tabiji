#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { renderMeta, escapeHtml, absoluteUrl } = require('./render-meta');
const { renderSchema } = require('./render-schema');
const { loadJson, validateSource } = require('./validate-source');

function renderPick(pick) {
  const tags = (pick.cuisineTags || []).map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`).join('');
  const quotes = (pick.redditQuotes || []).map((quote) => `
        <blockquote class="reddit-quote">
          <p>“${escapeHtml(quote.quote)}”</p>
          ${quote.source ? `<footer>${escapeHtml(quote.source)}</footer>` : ''}
        </blockquote>`).join('');

  return `
      <article class="pick-card" id="pick-${pick.rank}">
        <div class="pick-header">
          <h2><span class="rank">${pick.rank}</span>${escapeHtml(pick.name)}</h2>
          <div class="tag-row">${tags}</div>
        </div>
        <div class="pick-meta">
          ${pick.priceRangeLocal ? `<span>💴 ${escapeHtml(pick.priceRangeLocal)}</span>` : ''}
          ${pick.googleRating ? `<span>★ ${pick.googleRating}${pick.reviewCount ? ` · ${pick.reviewCount.toLocaleString()} reviews` : ''}</span>` : ''}
          ${pick.address ? `<span>📍 ${escapeHtml(pick.address)}</span>` : ''}
          ${pick.googleMapsUrl ? `<a href="${escapeHtml(pick.googleMapsUrl)}" target="_blank" rel="noopener">Map</a>` : ''}
        </div>
        ${pick.photo ? `<img class="pick-photo" src="${escapeHtml(absoluteUrl(pick.photo))}" alt="${escapeHtml(pick.name)}" loading="lazy">` : ''}
        <div class="pick-copy">
          <p><strong>Why it made the list:</strong> ${escapeHtml(pick.whyItMadeTheList)}</p>
          <p><strong>What to order:</strong> ${escapeHtml(pick.whatToOrder)}</p>
          <p><strong>Insider tip:</strong> ${escapeHtml(pick.insiderTip)}</p>
          ${quotes}
        </div>
      </article>`;
}

function renderPage(data) {
  const validation = validateSource(data);
  if (validation.errors.length) {
    throw new Error(`Cannot render invalid source:\n${validation.errors.join('\n')}`);
  }

  const relatedLinks = (data.related.manual || []).map((slug) => `
        <li><a href="/popular-picks/${escapeHtml(slug)}/">${escapeHtml(slug.replace(/-/g, ' '))}</a></li>`).join('');

  return `<!DOCTYPE html>
<html lang="en">
<head>
    ${renderMeta(data)}
    ${renderSchema(data)}
    <style>
      :root { --bg:#FEFCF9; --text:#2C2419; --muted:#6B5D4F; --line:#E8DFD0; --brand:#2D3A5C; --accent:#C4704B; }
      * { box-sizing:border-box; }
      body { margin:0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif; background:var(--bg); color:var(--text); line-height:1.65; }
      a { color:var(--accent); text-decoration:none; }
      nav, footer { max-width:1100px; margin:0 auto; padding:1.25rem 1.5rem; }
      nav { border-bottom:1px solid var(--line); }
      main { max-width:1100px; margin:0 auto; padding:2rem 1.5rem 4rem; }
      .hero { padding:1rem 0 2rem; border-bottom:1px solid var(--line); }
      .eyebrow, .badge, .tag { display:inline-block; background:#F5F0E8; border-radius:999px; padding:.25rem .7rem; font-size:.9rem; }
      h1, h2 { color:var(--brand); line-height:1.2; }
      .meta-row, .pick-meta { display:flex; flex-wrap:wrap; gap:.75rem 1rem; color:var(--muted); font-size:.95rem; }
      .layout { display:grid; grid-template-columns:minmax(0, 1fr) 320px; gap:2rem; margin-top:2rem; }
      .sidebar { position:sticky; top:1rem; align-self:start; }
      .panel, .pick-card { background:white; border:1px solid var(--line); border-radius:16px; padding:1.25rem; }
      .pick-list { display:grid; gap:1rem; }
      .pick-header { display:flex; justify-content:space-between; gap:1rem; align-items:flex-start; }
      .tag-row { display:flex; flex-wrap:wrap; gap:.4rem; }
      .rank { display:inline-flex; width:2rem; height:2rem; margin-right:.75rem; border-radius:999px; background:var(--brand); color:white; align-items:center; justify-content:center; font-size:.95rem; }
      .pick-photo { width:100%; border-radius:12px; margin:1rem 0; max-height:320px; object-fit:cover; }
      .reddit-quote { margin:1rem 0 0; padding:1rem; background:#faf7f3; border-left:3px solid var(--accent); }
      .section-title { margin:2rem 0 1rem; }
      ul.related { padding-left:1.2rem; }
      @media (max-width: 900px) { .layout { grid-template-columns:1fr; } .sidebar { position:static; } }
    </style>
</head>
<body>
  <nav><strong>tabiji.ai</strong></nav>
  <main>
    <section class="hero">
      <div class="eyebrow">${escapeHtml(data.hero.eyebrow)}</div>
      <h1>${escapeHtml(data.seo.h1)}</h1>
      <p>${escapeHtml(data.hero.dek)}</p>
      <div class="meta-row">${data.hero.metaSpans.map((item) => `<span>${escapeHtml(item)}</span>`).join('')}</div>
    </section>

    <div class="layout">
      <div>
        <section class="panel intro-section">
          <p><strong>${escapeHtml(data.intro.answerFirst)}</strong></p>
          ${data.intro.body.map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`).join('')}
        </section>

        ${data.intro.methodology ? `<section class="panel"><h2>How we built this list</h2><p>${escapeHtml(data.intro.methodology)}</p></section>` : ''}

        <h2 class="section-title">Top picks</h2>
        <section class="pick-list">
          ${data.picks.map(renderPick).join('')}
        </section>

        <section class="panel faq-section">
          <h2>Frequently Asked Questions</h2>
          ${data.faq.map((item) => `<div class="faq-item"><h3>${escapeHtml(item.question)}</h3><p>${escapeHtml(item.answer)}</p></div>`).join('')}
        </section>

        <section class="panel related-section">
          <h2>Related Recommendations</h2>
          <ul class="related">${relatedLinks}</ul>
        </section>
      </div>

      <aside class="sidebar">
        <section class="panel">
          <div class="badge">${escapeHtml(data.hero.badge)}</div>
          <p><strong>${escapeHtml(data.summary.totalOptions.toString())}</strong> spots</p>
          <p><strong>Top pick:</strong> ${escapeHtml(data.summary.topPick)}</p>
          ${data.summary.bestOverall ? `<p><strong>Best overall:</strong> ${escapeHtml(data.summary.bestOverall)}</p>` : ''}
          ${data.map?.enabled && data.map?.ctaUrl ? `<p><a href="${escapeHtml(data.map.ctaUrl)}" target="_blank" rel="noopener">${escapeHtml(data.map.ctaLabel || 'Open map')}</a></p>` : ''}
        </section>
      </aside>
    </div>
  </main>
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

module.exports = { renderPage };
