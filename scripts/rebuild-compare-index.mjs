#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const repoRoot = path.resolve(process.cwd(), 'tabiji');
const inventoryPath = path.join(repoRoot, 'compare', 'inventory.json');
const apiPath = path.join(repoRoot, 'api', 'v1', 'compare.json');
const outputPath = path.join(repoRoot, 'compare', 'index.html');

const inventory = JSON.parse(fs.readFileSync(inventoryPath, 'utf8')).cards || [];
const api = JSON.parse(fs.readFileSync(apiPath, 'utf8')).comparisons || [];
const apiBySlug = new Map(api.map(item => [item.slug, item]));

const featuredSlugs = [
  'tokyo-vs-kyoto',
  'tokyo-vs-osaka',
  'kyoto-vs-osaka',
  'london-vs-amsterdam',
  'madrid-vs-barcelona',
  'amalfi-coast-vs-cinque-terre'
];

const regionRules = [
  ['Asia', ['asia', 'japan', 'korea', 'thailand', 'taiwan', 'vietnam', 'indonesia', 'bali', 'philippines', 'india', 'sri lanka', 'malaysia', 'singapore', 'hong kong', 'china', 'nepal', 'bhutan', 'cambodia', 'laos', 'myanmar']],
  ['Europe', ['europe', 'italy', 'spain', 'france', 'greece', 'croatia', 'portugal', 'uk', 'england', 'scotland', 'ireland', 'amsterdam', 'netherlands', 'germany', 'austria', 'switzerland', 'norway', 'sweden', 'denmark', 'iceland', 'belgium', 'prague', 'budapest', 'vienna']],
  ['North America', ['north america', 'usa', 'united states', 'canada', 'mexico', 'hawaii', 'california', 'new york', 'texas', 'florida', 'quebec', 'alaska', 'caribbean']],
  ['Latin America', ['latin america', 'south america', 'central america', 'peru', 'colombia', 'brazil', 'argentina', 'chile', 'guatemala', 'costa rica', 'ecuador', 'bolivia', 'uruguay']],
  ['Oceania', ['oceania', 'australia', 'new zealand', 'fiji', 'tahiti', 'french polynesia', 'bora bora']],
  ['Middle East & Africa', ['middle east', 'africa', 'morocco', 'egypt', 'uae', 'dubai', 'abu dhabi', 'jordan', 'oman', 'saudi', 'seychelles', 'south africa', 'tanzania', 'kenya', 'madagascar']]
];

const typeRules = [
  ['City breaks', [' city ', 'cities', 'city break', 'city breaks', 'urban', 'capital', 'downtown']],
  ['Countries', ['country', 'countries']],
  ['Islands & beaches', ['island', 'islands', 'beach', 'beaches', 'coast', 'coastal', 'bay', 'caye', 'cay', 'reef', 'atoll']],
  ['Nature & outdoors', ['mountain', 'mountains', 'lake', 'lakes', 'forest', 'national park', 'hiking', 'nature', 'outdoors', 'adventure', 'desert', 'volcano']],
  ['Food & culture', ['food', 'culture', 'history', 'wine', 'seafood', 'nightlife', 'art']],
  ['Luxury & honeymoon', ['luxury', 'honeymoon', 'romance', 'resort']]
];

function normalizeText(...parts) {
  return parts.filter(Boolean).join(' ').toLowerCase();
}

function titleCaseFromSlug(slug) {
  return slug.split('-').map(part => part.charAt(0).toUpperCase() + part.slice(1)).join(' ');
}

function safeText(value = '') {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function getMtime(slug) {
  try {
    return fs.statSync(path.join(repoRoot, 'compare', slug, 'index.html')).mtime.toISOString();
  } catch {
    return null;
  }
}

function inferRegion(item) {
  const haystack = normalizeText(item.category, ...(item.tags || []), item.destination1, item.destination2, item.description, item.title);
  const matches = regionRules.filter(([, needles]) => needles.some(needle => haystack.includes(needle)));
  if (matches.length > 0) return matches[0][0];
  return 'Global & mixed';
}

function inferType(item) {
  const d1 = (item.destination1 || '').toLowerCase();
  const d2 = (item.destination2 || '').toLowerCase();
  const haystack = ` ${normalizeText(item.category, ...(item.tags || []), item.destination1, item.destination2, item.description, item.title)} `;
  if (/(^|\s)(japan|spain|italy|france|greece|thailand|portugal|germany|austria|mexico|croatia|vietnam|india|peru|brazil|canada|australia)(\s|$)/.test(` ${d1} ${d2} `)) {
    return 'Countries';
  }
  if (/(city|town|capital|district|neighborhood|neighbourhood)/.test(haystack) || !/(island|beach|coast|mountain|lake|park|country)/.test(haystack)) {
    return 'City breaks';
  }
  for (const [label, needles] of typeRules) {
    if (needles.some(needle => haystack.includes(needle))) return label;
  }
  return 'Trip style guides';
}

const cards = inventory.map((item) => {
  const apiItem = apiBySlug.get(item.slug) || {};
  const updatedAt = item.lastUpdated || apiItem.updatedAt || getMtime(item.slug);
  const tags = [...new Set([...(item.tags || []), ...(apiItem.tags || []), apiItem.category].filter(Boolean))].slice(0, 6);
  const region = inferRegion({ ...item, ...apiItem, tags });
  const tripType = inferType({ ...item, ...apiItem, tags });
  return {
    slug: item.slug,
    title: item.title || `${item.destination1} vs ${item.destination2}`,
    description: (item.description || apiItem.description || `${item.destination1} vs ${item.destination2} comparison.`).trim(),
    destination1: item.destination1 || apiItem.destination1 || titleCaseFromSlug(item.slug.split('-vs-')[0]),
    destination2: item.destination2 || apiItem.destination2 || titleCaseFromSlug(item.slug.split('-vs-')[1] || ''),
    image: item.image1 || item.image2 || '',
    url: `/compare/${item.slug}/`,
    updatedAt,
    updatedLabel: updatedAt ? new Date(updatedAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC' }) : 'Recent',
    region,
    tripType,
    tags
  };
}).sort((a, b) => a.title.localeCompare(b.title));

const totalCount = cards.length;
const newest = [...cards].sort((a, b) => (b.updatedAt || '').localeCompare(a.updatedAt || '')).slice(0, 6);
const featured = featuredSlugs.map(slug => cards.find(card => card.slug === slug)).filter(Boolean);

function groupTop(key, limit = 6) {
  const map = new Map();
  for (const card of cards) {
    const value = card[key] || 'Other';
    if (!map.has(value)) map.set(value, []);
    map.get(value).push(card);
  }
  return [...map.entries()]
    .map(([label, items]) => ({ label, count: items.length, items: items.sort((a, b) => a.title.localeCompare(b.title)).slice(0, 4) }))
    .sort((a, b) => b.count - a.count)
    .slice(0, limit);
}

const regionGroups = groupTop('region');
const typeGroups = groupTop('tripType');

function renderFeaturedCard(card) {
  return `<a class="feature-card" href="${card.url}">
    <div class="feature-image"${card.image ? ` style="background-image:url('${safeText(card.image)}')"` : ''}></div>
    <div class="feature-body">
      <div class="eyebrow">${safeText(card.region)} · ${safeText(card.tripType)}</div>
      <h3>${safeText(card.destination1)} vs ${safeText(card.destination2)}</h3>
      <p>${safeText(card.description)}</p>
      <span class="feature-link">Read comparison →</span>
    </div>
  </a>`;
}

function renderMiniCard(card) {
  return `<a class="mini-card" href="${card.url}">
    <div class="mini-top">
      <strong>${safeText(card.destination1)} vs ${safeText(card.destination2)}</strong>
      <span>${safeText(card.updatedLabel)}</span>
    </div>
    <p>${safeText(card.description)}</p>
  </a>`;
}

function renderBrowseGroup(group, kind) {
  return `<section class="browse-card">
    <div class="browse-head">
      <h3>${safeText(group.label)}</h3>
      <span>${group.count} pages</span>
    </div>
    <div class="browse-links">
      ${group.items.map(card => `<a href="${card.url}">${safeText(card.destination1)} vs ${safeText(card.destination2)}</a>`).join('')}
    </div>
    <button class="chip browse-chip" data-${kind.toLowerCase()}="${safeText(group.label)}">Filter archive</button>
  </section>`;
}

const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Travel Comparisons | Compare Destinations Side by Side | Tabiji</title>
  <meta name="description" content="Compare ${totalCount}+ destinations side by side with Tabiji. Search city, island, country, and trip-style comparisons, then browse featured picks, newest pages, regions, and travel types.">
  <link rel="canonical" href="https://tabiji.ai/compare/">
  <meta property="og:title" content="Travel Comparisons | Compare Destinations Side by Side | Tabiji">
  <meta property="og:description" content="Search ${totalCount}+ travel comparisons, browse featured picks, and find the right destination faster.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://tabiji.ai/compare/">
  <meta property="og:image" content="https://img.tabiji.ai/compare/tokyo-vs-kyoto/tokyo-shibuya-crossing.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Travel Comparisons | Compare Destinations Side by Side | Tabiji">
  <meta name="twitter:description" content="Search ${totalCount}+ travel comparisons, browse featured picks, and find the right destination faster.">
  <meta name="twitter:image" content="https://img.tabiji.ai/compare/tokyo-vs-kyoto/tokyo-shibuya-crossing.jpg">
  <style>
    :root {
      --indigo:#2D3A5C; --terracotta:#C4704B; --sand:#E8DFD0; --cream:#FEFCF9; --warm:#F5F0E8; --text:#2C2419; --muted:#6B5D4F; --sage:#7A8B6F;
      --shadow:0 18px 40px rgba(45,58,92,.08);
    }
    * { box-sizing:border-box; }
    html { scroll-behavior:smooth; }
    body { margin:0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif; background:var(--cream); color:var(--text); line-height:1.55; }
    a { color:inherit; }
    .shell { max-width:1180px; margin:0 auto; padding:0 24px; }
    .topbar { position:sticky; top:0; z-index:20; background:rgba(254,252,249,.92); backdrop-filter:blur(16px); border-bottom:1px solid rgba(232,223,208,.9); }
    .topbar .shell { display:flex; justify-content:space-between; align-items:center; min-height:72px; gap:20px; }
    .brand { font-size:1.35rem; font-weight:800; text-decoration:none; color:var(--indigo); }
    .brand span { color:var(--terracotta); }
    .navlinks { display:flex; gap:18px; align-items:center; font-size:.95rem; }
    .navlinks a { text-decoration:none; color:var(--muted); }
    .navcta { background:var(--terracotta); color:#fff !important; padding:.7rem 1rem; border-radius:10px; font-weight:700; }
    .hero { padding:72px 0 36px; }
    .hero-grid { display:grid; grid-template-columns:1.3fr .9fr; gap:28px; align-items:stretch; }
    .hero-copy, .hero-panel, .section-card, .search-panel, .browse-card { background:#fff; border:1px solid var(--sand); border-radius:24px; box-shadow:var(--shadow); }
    .hero-copy { padding:34px; }
    .hero-kicker { display:inline-flex; gap:10px; align-items:center; background:var(--warm); color:var(--terracotta); border-radius:999px; padding:.45rem .85rem; font-size:.9rem; font-weight:700; }
    h1 { font-size:clamp(2.4rem,5vw,4.4rem); line-height:1.04; letter-spacing:-.04em; color:var(--indigo); margin:18px 0 16px; }
    .hero-copy p { font-size:1.08rem; color:var(--muted); max-width:58ch; margin:0 0 22px; }
    .hero-actions { display:flex; flex-wrap:wrap; gap:12px; }
    .button { display:inline-flex; align-items:center; justify-content:center; gap:10px; padding:.95rem 1.25rem; border-radius:12px; text-decoration:none; font-weight:700; border:1px solid transparent; }
    .button.primary { background:var(--indigo); color:#fff; }
    .button.secondary { background:#fff; border-color:var(--sand); color:var(--indigo); }
    .hero-stats { margin-top:22px; padding-top:22px; border-top:1px solid var(--sand); display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
    .hero-stats strong { display:block; font-size:1.55rem; color:var(--indigo); }
    .hero-stats span { font-size:.95rem; color:var(--muted); }
    .hero-panel { padding:28px; display:grid; gap:16px; }
    .hero-panel h2 { margin:0; color:var(--indigo); font-size:1.15rem; }
    .hero-list { display:grid; gap:12px; }
    .hero-list a { text-decoration:none; padding:14px 16px; border-radius:16px; background:var(--warm); border:1px solid transparent; }
    .hero-list a:hover { border-color:var(--sand); }
    .hero-list strong { display:block; }
    .hero-list span { display:block; color:var(--muted); font-size:.92rem; margin-top:4px; }
    .section { padding:18px 0; }
    .section-header { display:flex; justify-content:space-between; align-items:end; gap:20px; margin-bottom:18px; }
    .section-header h2 { margin:0; color:var(--indigo); font-size:1.8rem; letter-spacing:-.03em; }
    .section-header p { margin:6px 0 0; color:var(--muted); max-width:56ch; }
    .feature-grid, .mini-grid, .browse-grid { display:grid; gap:18px; }
    .feature-grid { grid-template-columns:repeat(3,1fr); }
    .mini-grid, .browse-grid { grid-template-columns:repeat(3,1fr); }
    .feature-card, .mini-card { background:#fff; border:1px solid var(--sand); border-radius:20px; overflow:hidden; text-decoration:none; box-shadow:var(--shadow); }
    .feature-image { height:190px; background:linear-gradient(135deg, rgba(45,58,92,.15), rgba(196,112,75,.15)); background-size:cover; background-position:center; }
    .feature-body { padding:18px; }
    .eyebrow { font-size:.82rem; text-transform:uppercase; letter-spacing:.08em; font-weight:700; color:var(--terracotta); }
    .feature-body h3, .mini-card strong { margin:8px 0 10px; color:var(--indigo); font-size:1.15rem; }
    .feature-body p, .mini-card p, .browse-card p { margin:0; color:var(--muted); }
    .feature-link { display:inline-block; margin-top:14px; font-weight:700; color:var(--indigo); }
    .mini-card { padding:18px; }
    .mini-top { display:flex; justify-content:space-between; gap:16px; align-items:flex-start; }
    .mini-top span { color:var(--muted); font-size:.88rem; white-space:nowrap; }
    .search-panel { padding:24px; }
    .search-toolbar { display:grid; grid-template-columns:2fr repeat(3,1fr); gap:12px; margin-top:18px; }
    .field, .chip { border:1px solid var(--sand); background:#fff; border-radius:12px; min-height:48px; padding:0 14px; font:inherit; color:var(--text); }
    .chip { cursor:pointer; font-weight:700; }
    .archive-meta { display:flex; justify-content:space-between; align-items:center; gap:16px; margin-top:16px; color:var(--muted); font-size:.95rem; }
    .quick-chips { display:flex; flex-wrap:wrap; gap:10px; margin-top:16px; }
    .quick-chips .chip { min-height:auto; padding:.7rem .95rem; }
    .chip.active { background:var(--indigo); color:#fff; border-color:var(--indigo); }
    .browse-card { padding:20px; }
    .browse-head { display:flex; justify-content:space-between; gap:14px; align-items:baseline; margin-bottom:14px; }
    .browse-head h3 { margin:0; color:var(--indigo); font-size:1.1rem; }
    .browse-head span { color:var(--muted); font-size:.9rem; }
    .browse-links { display:grid; gap:10px; }
    .browse-links a { color:var(--muted); text-decoration:none; }
    .browse-chip { margin-top:14px; }
    .archive-list { margin-top:18px; display:grid; gap:12px; }
    .archive-row { display:grid; grid-template-columns:minmax(0,1.4fr) .65fr .65fr 96px; gap:16px; align-items:start; padding:18px; background:#fff; border:1px solid var(--sand); border-radius:18px; text-decoration:none; }
    .archive-row h3 { margin:0 0 6px; color:var(--indigo); font-size:1.05rem; }
    .archive-row p { margin:0; color:var(--muted); font-size:.95rem; }
    .archive-label { font-size:.9rem; color:var(--muted); }
    .archive-row strong { color:var(--indigo); }
    .archive-empty { padding:26px; border-radius:18px; background:var(--warm); color:var(--muted); border:1px dashed var(--sand); }
    .footer { padding:42px 0 60px; color:var(--muted); }
    @media (max-width: 1040px) {
      .hero-grid, .feature-grid, .mini-grid, .browse-grid { grid-template-columns:1fr 1fr; }
      .search-toolbar { grid-template-columns:1fr 1fr; }
      .archive-row { grid-template-columns:1fr 1fr; }
    }
    @media (max-width: 720px) {
      .shell { padding:0 16px; }
      .navlinks a:not(.navcta) { display:none; }
      .hero-grid, .feature-grid, .mini-grid, .browse-grid, .search-toolbar, .archive-row, .hero-stats { grid-template-columns:1fr; }
      .hero { padding-top:34px; }
      .hero-copy, .hero-panel, .search-panel { border-radius:20px; }
      .section-header, .archive-meta, .mini-top, .browse-head { display:block; }
      .archive-row { gap:8px; }
    }
  </style>
</head>
<body>
  <header class="topbar">
    <div class="shell">
      <a class="brand" href="/">tabi<span>ji</span></a>
      <nav class="navlinks">
        <a href="/destinations/">Destinations</a>
        <a href="/compare/">Compare</a>
        <a href="/plan">Plan a trip</a>
        <a class="navcta" href="/plan">Get itinerary</a>
      </nav>
    </div>
  </header>

  <main>
    <section class="hero">
      <div class="shell hero-grid">
        <div class="hero-copy">
          <div class="hero-kicker">Compare destinations faster</div>
          <h1>The compare homepage, not a giant pile of cards.</h1>
          <p>Search ${totalCount}+ side-by-side destination guides, jump into featured matchups, browse by region or trip type, and use the compact archive when you already know what you want.</p>
          <div class="hero-actions">
            <a class="button primary" href="#archive">Search all comparisons</a>
            <a class="button secondary" href="#browse-region">Browse by region</a>
          </div>
          <div class="hero-stats">
            <div><strong>${totalCount}</strong><span>published comparisons</span></div>
            <div><strong>${newest.length}</strong><span>fresh picks surfaced below</span></div>
            <div><strong>6</strong><span>region entry points</span></div>
          </div>
        </div>
        <aside class="hero-panel">
          <h2>Good starting points</h2>
          <div class="hero-list">
            <a href="/compare/tokyo-vs-kyoto/"><strong>Tokyo vs Kyoto</strong><span>Japan’s classic first-timer fork</span></a>
            <a href="/compare/madrid-vs-barcelona/"><strong>Madrid vs Barcelona</strong><span>Spain’s most common city decision</span></a>
            <a href="/compare/amalfi-coast-vs-cinque-terre/"><strong>Amalfi Coast vs Cinque Terre</strong><span>Italy beach-and-scenery showdown</span></a>
            <a href="/compare/london-vs-amsterdam/"><strong>London vs Amsterdam</strong><span>Fast European city-break contrast</span></a>
          </div>
        </aside>
      </div>
    </section>

    <section class="section">
      <div class="shell">
        <div class="section-header">
          <div>
            <h2>Featured comparisons</h2>
            <p>High-intent matchups that work well as front doors into the rest of the catalog.</p>
          </div>
        </div>
        <div class="feature-grid">
          ${featured.map(renderFeaturedCard).join('')}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="shell">
        <div class="section-header">
          <div>
            <h2>Newest comparisons</h2>
            <p>Freshly updated pages, sorted from the current compare inventory and page files.</p>
          </div>
        </div>
        <div class="mini-grid">
          ${newest.map(renderMiniCard).join('')}
        </div>
      </div>
    </section>

    <section class="section" id="browse-region">
      <div class="shell">
        <div class="section-header">
          <div>
            <h2>Browse by region</h2>
            <p>Use these as jump points when you’re shopping broadly rather than deciding between two exact destinations yet.</p>
          </div>
        </div>
        <div class="browse-grid">
          ${regionGroups.map(group => renderBrowseGroup(group, 'Region')).join('')}
        </div>
      </div>
    </section>

    <section class="section" id="browse-type">
      <div class="shell">
        <div class="section-header">
          <div>
            <h2>Browse by trip type</h2>
            <p>Cluster pages by the kind of decision a traveler is making: city break, island escape, country trip, or outdoors-heavy route.</p>
          </div>
        </div>
        <div class="browse-grid">
          ${typeGroups.map(group => renderBrowseGroup(group, 'Type')).join('')}
        </div>
      </div>
    </section>

    <section class="section" id="archive">
      <div class="shell">
        <div class="search-panel">
          <div class="section-header">
            <div>
              <h2>All comparisons</h2>
              <p>Compact archive. Search first, then filter by region, trip type, or sort order.</p>
            </div>
          </div>
          <div class="search-toolbar">
            <input id="searchInput" class="field" type="search" placeholder="Search Tokyo, Sicily, beaches, Japan, budget…" aria-label="Search comparisons">
            <select id="regionFilter" class="field" aria-label="Filter by region">
              <option value="">All regions</option>
              ${[...new Set(cards.map(card => card.region))].sort().map(region => `<option value="${safeText(region)}">${safeText(region)}</option>`).join('')}
            </select>
            <select id="typeFilter" class="field" aria-label="Filter by trip type">
              <option value="">All trip types</option>
              ${[...new Set(cards.map(card => card.tripType))].sort().map(type => `<option value="${safeText(type)}">${safeText(type)}</option>`).join('')}
            </select>
            <select id="sortFilter" class="field" aria-label="Sort comparisons">
              <option value="newest">Newest</option>
              <option value="az">A–Z</option>
            </select>
          </div>
          <div class="quick-chips">
            <button class="chip" data-region="Asia">Asia</button>
            <button class="chip" data-region="Europe">Europe</button>
            <button class="chip" data-type="City breaks">City breaks</button>
            <button class="chip" data-type="Islands &amp; beaches">Islands & beaches</button>
            <button class="chip" data-type="Countries">Countries</button>
            <button class="chip" id="clearFilters">Clear filters</button>
          </div>
          <div class="archive-meta">
            <div id="resultCount">Showing ${totalCount} comparisons</div>
            <div>Inventory source: <code>compare/inventory.json</code></div>
          </div>
          <div id="archiveList" class="archive-list"></div>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="shell">Tabiji destination comparisons are built to help travelers choose faster, then plan better.</div>
  </footer>

  <script>
    const cards = ${JSON.stringify(cards)};
    const searchInput = document.getElementById('searchInput');
    const regionFilter = document.getElementById('regionFilter');
    const typeFilter = document.getElementById('typeFilter');
    const sortFilter = document.getElementById('sortFilter');
    const archiveList = document.getElementById('archiveList');
    const resultCount = document.getElementById('resultCount');
    const chipButtons = [...document.querySelectorAll('.chip')];

    function rowTemplate(card) {
      return '<a class="archive-row" href="' + card.url + '">' +
        '<div>' +
          '<h3>' + card.destination1 + ' vs ' + card.destination2 + '</h3>' +
          '<p>' + card.description + '</p>' +
        '</div>' +
        '<div class="archive-label"><strong>Region</strong><br>' + card.region + '</div>' +
        '<div class="archive-label"><strong>Type</strong><br>' + card.tripType + '</div>' +
        '<div class="archive-label"><strong>Updated</strong><br>' + card.updatedLabel + '</div>' +
      '</a>';
    }

    function applyFilters() {
      const query = searchInput.value.trim().toLowerCase();
      const region = regionFilter.value;
      const type = typeFilter.value;
      const sort = sortFilter.value;

      let filtered = cards.filter(card => {
        const haystack = [card.title, card.description, card.destination1, card.destination2, card.region, card.tripType, ...(card.tags || [])].join(' ').toLowerCase();
        return (!query || haystack.includes(query))
          && (!region || card.region === region)
          && (!type || card.tripType === type);
      });

      filtered = filtered.sort((a, b) => {
        if (sort === 'az') return a.title.localeCompare(b.title);
        return (b.updatedAt || '').localeCompare(a.updatedAt || '') || a.title.localeCompare(b.title);
      });

      resultCount.textContent = 'Showing ' + filtered.length + ' comparison' + (filtered.length === 1 ? '' : 's');
      archiveList.innerHTML = filtered.length
        ? filtered.map(rowTemplate).join('')
        : '<div class="archive-empty">No matches. Try a broader search or clear the filters.</div>';

      chipButtons.forEach(button => {
        const active = (button.dataset.region && button.dataset.region === region)
          || (button.dataset.type && button.dataset.type === type);
        button.classList.toggle('active', active);
      });
    }

    [searchInput, regionFilter, typeFilter, sortFilter].forEach(el => el.addEventListener('input', applyFilters));
    [searchInput, regionFilter, typeFilter, sortFilter].forEach(el => el.addEventListener('change', applyFilters));

    document.querySelectorAll('[data-region]').forEach(button => button.addEventListener('click', () => {
      regionFilter.value = button.dataset.region;
      applyFilters();
      document.getElementById('archive').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }));

    document.querySelectorAll('[data-type]').forEach(button => button.addEventListener('click', () => {
      typeFilter.value = button.dataset.type;
      applyFilters();
      document.getElementById('archive').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }));

    document.getElementById('clearFilters').addEventListener('click', () => {
      searchInput.value = '';
      regionFilter.value = '';
      typeFilter.value = '';
      sortFilter.value = 'newest';
      applyFilters();
    });

    applyFilters();
  </script>
</body>
</html>`;

fs.writeFileSync(outputPath, html);
console.log(`Wrote ${path.relative(process.cwd(), outputPath)} with ${totalCount} cards.`);
