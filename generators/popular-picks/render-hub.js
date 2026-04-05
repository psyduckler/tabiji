#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { renderMeta, escapeHtml, absoluteUrl } = require('./render-meta');

function slugToTitle(value = '') {
  return String(value)
    .split('-')
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ');
}

function getHubFaq(data) {
  if (Array.isArray(data.faq) && data.faq.length) return data.faq;

  const sectionTitles = (data.sections || []).map((section) => section.title).filter(Boolean);
  const firstSection = sectionTitles[0] || slugToTitle(data.slug || 'this destination');
  const title = data.hero?.title || data.seo?.h1 || slugToTitle(data.slug || 'this destination');
  const totalLists = (data.sections || []).reduce((sum, section) => sum + ((section.cards || []).length ? 1 : 0), 0);
  const destination = data.slug === 'usa' ? 'the USA' : title;

  return [
    {
      question: `What kinds of popular picks are included in ${title}?`,
      answer: `${title} groups together Reddit-backed lists for its strongest food and travel categories, starting with ${firstSection}${totalLists > 1 ? ` and ${Math.max(totalLists - 1, 0)} other curated list${totalLists === 2 ? '' : 's'}` : ''}. Each card links to a deeper guide with specific places, context, and map support.`
    },
    {
      question: `How are Tabiji's ${title} picks chosen?`,
      answer: `These picks are built from real traveler discussion patterns, then organized into curated shortlists rather than paid placements or generic roundups. The goal is to surface the places and experiences people repeatedly mention when planning trips to ${destination}.`
    },
    {
      question: `Should I start with the hub page or open the individual guides for ${title}?`,
      answer: `Use the hub page to decide which city or category fits what you want, then open the individual guides for ranked picks, more detailed context, and map links. The hub is the shortlist; the leaf guides are where the decision-making detail lives.`
    }
  ];
}

function renderJsonLd(obj) {
  return `<script type="application/ld+json">${JSON.stringify(obj, null, 2)}</script>`;
}

function renderHubSchema(data) {
  const canonical = absoluteUrl(data.seo.canonicalPath);
  const heroImage = absoluteUrl(data.seo.heroImage || '');
  const publishedDate = typeof data?.seo?.publishedTime === 'string' ? data.seo.publishedTime.slice(0, 10) : undefined;
  const modifiedDate = typeof data?.seo?.modifiedTime === 'string' ? data.seo.modifiedTime.slice(0, 10) : undefined;
  const faq = getHubFaq(data);

  const totalGuides = (data.sections || []).reduce((sum, s) => sum + (s.cards || []).length, 0);
  const itemListElements = [];
  let position = 0;
  for (const section of (data.sections || [])) {
    for (const card of (section.cards || [])) {
      position++;
      itemListElements.push({
        '@type': 'ListItem',
        position,
        url: absoluteUrl(card.href || `/popular-picks/${card.slug}/`),
        name: card.title,
      });
    }
  }

  const collectionPage = {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: data.hero?.title || data.seo?.h1,
    description: data.seo?.metaDescription,
    url: canonical,
    author: { '@type': 'Organization', name: 'tabiji.ai', url: 'https://tabiji.ai' },
    publisher: { '@type': 'Organization', name: 'tabiji.ai', url: 'https://tabiji.ai' },
    ...(publishedDate ? { datePublished: publishedDate } : {}),
    ...(modifiedDate ? { dateModified: modifiedDate } : {}),
    mainEntityOfPage: canonical,
    ...(heroImage ? { image: heroImage } : {}),
    mainEntity: {
      '@type': 'ItemList',
      numberOfItems: totalGuides,
      itemListElement: itemListElements,
    },
  };

  const breadcrumb = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://tabiji.ai/' },
      { '@type': 'ListItem', position: 2, name: 'Popular Picks', item: 'https://tabiji.ai/popular-picks/' },
      { '@type': 'ListItem', position: 3, name: data.hero?.title || data.seo?.h1, item: canonical }
    ]
  };

  const faqSchema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faq.map((item) => ({
      '@type': 'Question',
      name: item.question,
      acceptedAnswer: { '@type': 'Answer', text: item.answer }
    }))
  };

  return [collectionPage, breadcrumb, faqSchema].map(renderJsonLd).join('\n    ');
}

function renderToc(data) {
  const items = data.toc || [];
  if (!items.length) return '';
  const links = items.map((item) => `<li><a href="#${escapeHtml(item.id)}">${escapeHtml(item.label)}</a></li>`).join('');
  return `
<div class="toc-mobile-sticky" id="toc-mobile">
  <button class="toc-mobile-toggle" onclick="this.parentElement.classList.toggle('open')">
    <span class="toc-active-label" id="toc-active-label">${escapeHtml(items[0].label)}</span>
    <span class="toc-chevron">▼</span>
  </button>
  <div class="toc-mobile-dropdown"><ul>${links}</ul></div>
</div>

<div class="content-wrapper">
  <aside class="toc-sidebar">
    <h2>Sections</h2>
    <ul>${links}</ul>
  </aside>`;
}

function renderCard(card) {
  return `
<a href="${escapeHtml(card.href)}" class="pick-card">
  ${card.image ? `<img src="${escapeHtml(absoluteUrl(card.image))}" alt="${escapeHtml(card.imageAlt || card.title)}" loading="lazy">` : ''}
  <div class="pick-card-body">
    ${card.badge ? `<span class="card-badge">${escapeHtml(card.badge)}</span>` : ''}
    <h3>${escapeHtml(card.title)}</h3>
    <p>${escapeHtml(card.description || '')}</p>
    ${Array.isArray(card.meta) && card.meta.length ? `<div class="card-meta">${card.meta.map((item) => `<span>${escapeHtml(item)}</span>`).join('')}</div>` : ''}
  </div>
</a>`;
}

function renderSections(data) {
  return (data.sections || []).map((section) => `
<section class="city-section" id="${escapeHtml(section.id)}">
  <h2>${escapeHtml(section.title)}</h2>
  <div class="picks-grid">
    ${(section.cards || []).map(renderCard).join('')}
  </div>
</section>`).join('');
}

function renderFaq(data) {
  const faq = getHubFaq(data);
  if (!faq.length) return '';
  return `
<section class="faq-section">
  <h2>Frequently Asked Questions</h2>
  ${faq.map((item) => `<details class="faq-item"><summary>${escapeHtml(item.question)}</summary><p>${escapeHtml(item.answer)}</p></details>`).join('')}
</section>`;
}

function renderHubPage(data) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-D7QHNRXLHJ"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-D7QHNRXLHJ');
    </script>
    ${renderMeta(data)}
    ${renderHubSchema(data)}
    <style>
      :root { --indigo:#2D3A5C; --warm-cream:#F5F0E8; --sand:#E8DFD0; --earth:#8B7355; --terracotta:#C4704B; --white:#FEFCF9; --text:#2C2419; --text-muted:#6B5D4F; }
      * { margin:0; padding:0; box-sizing:border-box; }
      body { font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif; color:var(--text); background:var(--white); line-height:1.6; }
      a { color:inherit; text-decoration:none; }
      nav { position:sticky; top:0; z-index:100; background:rgba(254,252,249,.92); backdrop-filter:blur(20px); border-bottom:1px solid var(--sand); padding:1rem 1.5rem; display:flex; justify-content:space-between; align-items:center; }
      .logo { font-size:1.3rem; font-weight:700; color:var(--indigo); }
      .cta-nav { background:var(--terracotta); color:white; padding:.55rem 1rem; border-radius:8px; }
      .hero { padding:7rem 1.5rem 2rem; max-width:1080px; margin:0 auto; }
      .back-link { display:inline-block; margin-bottom:1rem; color:var(--earth); }
      .hero h1 { font-size:clamp(2rem,4.7vw,3rem); line-height:1.12; color:var(--indigo); margin-bottom:1rem; }
      .hero p { color:var(--text-muted); max-width:780px; }
      .hero-meta { display:flex; gap:1rem 1.5rem; flex-wrap:wrap; margin-top:1rem; color:var(--earth); font-size:.95rem; }
      .hero-figure { margin-top:1.5rem; border:1px solid var(--sand); border-radius:18px; overflow:hidden; background:var(--warm-cream); }
      .hero-figure img { width:100%; height:min(46vw,420px); min-height:220px; object-fit:cover; display:block; }
      .hero-caption { padding:.85rem 1rem; color:var(--text-muted); font-size:.92rem; border-top:1px solid var(--sand); background:rgba(245,240,232,.65); }
      .toc-sidebar { position:sticky; top:90px; align-self:start; width:220px; border-right:1px solid var(--sand); padding-right:1rem; }
      .toc-sidebar h2 { font-size:1rem; margin-bottom:.8rem; color:var(--indigo); }
      .toc-sidebar ul { list-style:none; }
      .toc-sidebar li { margin-bottom:.4rem; }
      .toc-sidebar a { color:var(--text-muted); }
      .toc-sidebar a:hover, .toc-sidebar a.active { color:var(--terracotta); font-weight:600; }
      .toc-mobile-sticky { display:none; position:sticky; top:73px; z-index:90; background:var(--white); border-bottom:1px solid var(--sand); padding:.75rem 1rem; }
      .toc-mobile-toggle { width:100%; background:var(--warm-cream); border:1px solid var(--sand); border-radius:10px; padding:.85rem 1rem; display:flex; justify-content:space-between; align-items:center; font-size:1rem; }
      .toc-mobile-dropdown { max-height:0; overflow:hidden; transition:max-height .2s ease; }
      .toc-mobile-sticky.open .toc-mobile-dropdown { max-height:60vh; overflow-y:auto; }
      .toc-mobile-dropdown ul { list-style:none; padding-top:.6rem; }
      .toc-mobile-dropdown li { margin-bottom:.3rem; }
      .content-wrapper { max-width:1200px; margin:0 auto; display:grid; grid-template-columns:220px minmax(0,1fr); gap:2rem; padding:0 1.5rem 4rem; }
      .main-content { min-width:0; }
      .city-section { margin-bottom:3rem; }
      .city-section h2 { font-size:1.75rem; color:var(--indigo); margin-bottom:1rem; }
      .picks-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1.25rem; }
      @media (max-width:900px) { .picks-grid { grid-template-columns:repeat(2,1fr); } }
      @media (max-width:560px) { .picks-grid { grid-template-columns:1fr; } }
      .pick-card { background:#FEFCF9; border:1px solid var(--sand); border-radius:14px; overflow:hidden; display:block; transition:transform .15s, box-shadow .15s; }
      .pick-card:hover { transform:translateY(-3px); box-shadow:0 8px 30px rgba(0,0,0,.08); }
      .pick-card img { width:100%; height:180px; object-fit:cover; display:block; }
      .pick-card-body { padding:1rem; }
      .card-badge { display:inline-block; font-size:.82rem; color:var(--earth); margin-bottom:.55rem; }
      .pick-card h3 { font-size:1.12rem; color:var(--indigo); margin-bottom:.5rem; }
      .pick-card p { font-size:.95rem; color:var(--text-muted); margin-bottom:.8rem; }
      .card-meta { display:flex; gap:.75rem; flex-wrap:wrap; color:var(--earth); font-size:.86rem; }
      .faq-section { max-width:1200px; margin:0 auto; padding:0 1.5rem 4rem; }
      .faq-section h2 { color:var(--indigo); margin-bottom:1rem; }
      .faq-item { border-top:1px solid var(--sand); padding:.9rem 0; }
      .faq-item summary { cursor:pointer; font-weight:700; color:var(--indigo); }
      footer { max-width:1200px; margin:0 auto; padding:0 1.5rem 3rem; color:var(--text-muted); }
      @media (max-width: 900px) {
        .toc-sidebar { display:none; }
        .toc-mobile-sticky { display:block; }
        .content-wrapper { grid-template-columns:1fr; }
      }
    </style>
</head>
<body>
  <nav>
    <a class="logo" href="/">tabiji.ai</a>
    <a class="cta-nav" href="/plan">Get a Free Itinerary</a>
  </nav>

  <section class="hero">
    ${data.hero.backLink ? `<a href="${escapeHtml(data.hero.backLink)}" class="back-link">← All Popular Picks</a>` : ''}
    <h1>${escapeHtml(data.hero.title || data.seo.h1)}</h1>
    <p>${escapeHtml(data.hero.dek || '')}</p>
    ${Array.isArray(data.hero.meta) && data.hero.meta.length ? `<div class="hero-meta">${data.hero.meta.map((item) => `<div>${escapeHtml(item)}</div>`).join('')}</div>` : ''}
    ${data.seo.heroImage ? `<figure class="hero-figure"><img src="${escapeHtml(absoluteUrl(data.seo.heroImage))}" alt="${escapeHtml(data.hero.title || data.seo.h1)}" loading="eager">${data.hero.caption ? `<figcaption class="hero-caption">${escapeHtml(data.hero.caption)}</figcaption>` : ''}</figure>` : ''}
  </section>

  ${renderToc(data)}
    <div class="main-content">
      ${renderSections(data)}
    </div>
  </div>

  ${renderFaq(data)}

  <footer>Generated from structured hub source data.</footer>

  <script>
  const sections = document.querySelectorAll('.city-section');
  const tocLinks = document.querySelectorAll('.toc-sidebar a, .toc-mobile-dropdown a');
  const mobileLabel = document.getElementById('toc-active-label');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        tocLinks.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + id));
        if (mobileLabel) mobileLabel.textContent = entry.target.querySelector('h2')?.textContent || 'Sections';
      }
    });
  }, { rootMargin: '-80px 0px -60% 0px', threshold: 0 });
  sections.forEach(s => observer.observe(s));
  document.querySelectorAll('.toc-mobile-dropdown a').forEach(a => {
    a.addEventListener('click', () => document.getElementById('toc-mobile').classList.remove('open'));
  });
  </script>
</body>
</html>`;
}

if (require.main === module) {
  const [inputPath, outputPath] = process.argv.slice(2);
  if (!inputPath || !outputPath) {
    console.error('Usage: node render-hub.js <input.json> <output.html>');
    process.exit(1);
  }
  const data = JSON.parse(fs.readFileSync(path.resolve(inputPath), 'utf8'));
  const html = renderHubPage(data);
  fs.mkdirSync(path.dirname(path.resolve(outputPath)), { recursive: true });
  fs.writeFileSync(path.resolve(outputPath), html);
  console.log(`Rendered hub ${outputPath}`);
}

module.exports = { renderHubPage };
