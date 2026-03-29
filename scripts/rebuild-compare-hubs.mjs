#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const repoRoot = process.cwd();
const compareDir = path.join(repoRoot, 'compare');
const inventoryPath = path.join(compareDir, 'inventory.json');
const apiPath = path.join(repoRoot, 'api', 'v1', 'compare.json');
const sitemapPath = path.join(repoRoot, 'sitemap.xml');

const inventory = JSON.parse(fs.readFileSync(inventoryPath, 'utf8')).cards || [];
const api = JSON.parse(fs.readFileSync(apiPath, 'utf8')).comparisons || [];
const apiBySlug = new Map(api.map(item => [item.slug, item]));

const regionDefinitions = [
  { slug: 'asia', label: 'Asia', intro: 'Compare Japan, Korea, Southeast Asia, and other Asia trip decisions.', needles: ['asia', 'japan', 'korea', 'thailand', 'taiwan', 'vietnam', 'indonesia', 'bali', 'philippines', 'india', 'sri lanka', 'malaysia', 'singapore', 'hong kong', 'china', 'nepal', 'bhutan', 'cambodia', 'laos', 'myanmar', 'tokyo', 'kyoto', 'osaka', 'bangkok', 'phuket', 'chiang mai', 'hanoi', 'ho chi minh', 'seoul', 'taipei', 'maldives', 'okinawa', 'hokkaido', 'fukuoka', 'sapporo', 'krabi', 'koh samui', 'penang', 'langkawi', 'cebu', 'palawan', 'ubud', 'lombok', 'goa', 'jaipur', 'delhi', 'mumbai', 'kathmandu', 'siem reap', 'luang prabang', 'sukhothai', 'ayutthaya'] },
  { slug: 'europe', label: 'Europe', intro: 'Compare city breaks, islands, and country trips across Europe.', needles: ['europe', 'italy', 'spain', 'france', 'greece', 'croatia', 'portugal', 'england', 'scotland', 'ireland', 'netherlands', 'germany', 'austria', 'switzerland', 'norway', 'sweden', 'denmark', 'iceland', 'belgium', 'prague', 'budapest', 'vienna', 'london', 'paris', 'rome', 'barcelona', 'amsterdam', 'berlin', 'lisbon', 'madrid', 'florence', 'munich', 'dubrovnik', 'split', 'santorini', 'mykonos', 'mallorca', 'ibiza', 'amalfi', 'cinque terre', 'krakow', 'warsaw'] },
  { slug: 'north-america', label: 'North America', intro: 'Compare US, Canada, Mexico, Hawaii, and Caribbean-style decisions.', needles: ['north america', 'usa', 'united states', 'canada', 'mexico', 'hawaii', 'california', 'new york', 'texas', 'florida', 'quebec', 'alaska', 'caribbean'] },
  { slug: 'latin-america', label: 'Latin America', intro: 'Compare Central and South America routes, cities, and nature trips.', needles: ['latin america', 'south america', 'central america', 'peru', 'colombia', 'brazil', 'argentina', 'chile', 'guatemala', 'costa rica', 'ecuador', 'bolivia', 'uruguay'] },
  { slug: 'oceania', label: 'Oceania', intro: 'Compare Australia, New Zealand, Fiji, Tahiti, Bora Bora, and Pacific trips.', needles: ['oceania', 'australia', 'new zealand', 'fiji', 'tahiti', 'french polynesia', 'bora bora'] },
  { slug: 'middle-east-africa', label: 'Middle East & Africa', intro: 'Compare safari, desert, island, and culture-heavy trips across Africa and the Middle East.', needles: ['middle east', 'africa', 'morocco', 'egypt', 'uae', 'dubai', 'abu dhabi', 'jordan', 'oman', 'saudi', 'seychelles', 'south africa', 'tanzania', 'kenya', 'madagascar'] },
  { slug: 'global-mixed', label: 'Global & Mixed', intro: 'Cross-region comparisons that do not fit one clean geography bucket.', needles: [] }
];

const typeDefinitions = [
  { slug: 'cities', label: 'City breaks', intro: 'Fast urban decisions: capitals, food cities, weekend breaks, and major metros.' },
  { slug: 'countries', label: 'Countries', intro: 'Country vs country and country-scale trip decisions.' },
  { slug: 'islands', label: 'Islands & beaches', intro: 'Island-hopping, beaches, coastlines, and tropical escape decisions.' },
  { slug: 'nature', label: 'Nature & outdoors', intro: 'Mountains, lakes, hikes, safaris, and outdoors-heavy trip choices.' },
  { slug: 'culture', label: 'Food & culture', intro: 'History, food, wine, nightlife, and culture-led travel comparisons.' },
  { slug: 'luxury', label: 'Luxury & honeymoon', intro: 'Resort, romance, and higher-end trip decisions.' },
  { slug: 'trip-style-guides', label: 'Trip style guides', intro: 'Everything else that is useful but does not fit the main browse buckets cleanly.' }
];

const featuredSlugs = ['tokyo-vs-kyoto','tokyo-vs-osaka','kyoto-vs-osaka','london-vs-amsterdam','madrid-vs-barcelona','amalfi-coast-vs-cinque-terre'];

function safeText(value = '') {
  return String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function normalizeText(...parts) {
  return parts.filter(Boolean).join(' ').toLowerCase();
}

function titleCaseFromSlug(slug) {
  return slug.split('-').map(part => part.charAt(0).toUpperCase() + part.slice(1)).join(' ');
}

function getMtime(slug) {
  try { return fs.statSync(path.join(compareDir, slug, 'index.html')).mtime.toISOString(); }
  catch { return null; }
}

function scanInboundCompareLinks() {
  const inbound = new Map();
  for (const item of inventory) inbound.set(item.slug, 0);
  for (const item of inventory) {
    const pagePath = path.join(compareDir, item.slug, 'index.html');
    if (!fs.existsSync(pagePath)) continue;
    const text = fs.readFileSync(pagePath, 'utf8');
    const matches = [...text.matchAll(/href=["'](?:https:\/\/tabiji\.ai)?(\/compare\/([^"'/]+)\/)["']/g)];
    const seen = new Set();
    for (const match of matches) {
      const linkedSlug = match[2];
      if (!linkedSlug || linkedSlug === item.slug || seen.has(linkedSlug)) continue;
      seen.add(linkedSlug);
      inbound.set(linkedSlug, (inbound.get(linkedSlug) || 0) + 1);
    }
  }
  return inbound;
}

const inboundLinks = scanInboundCompareLinks();
const destinationFrequency = new Map();
for (const item of inventory) {
  for (const dest of [item.destination1, item.destination2]) {
    if (!dest) continue;
    const key = dest.toLowerCase();
    destinationFrequency.set(key, (destinationFrequency.get(key) || 0) + 1);
  }
}

function needleMatch(haystack, needle) {
  // Use word-boundary matching to avoid substring false positives (e.g. "uk" in "Phuket")
  const re = new RegExp(`(?:^|\\W)${needle.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?:$|\\W)`, 'i');
  return re.test(haystack);
}

function inferRegion(item) {
  // Check destination names first (high signal) before falling back to description text
  const destHaystack = normalizeText(item.destination1, item.destination2);
  const destMatch = regionDefinitions.find(def => def.needles.length && def.needles.some(needle => needleMatch(destHaystack, needle)));
  if (destMatch) return destMatch.label;
  // Fall back to full text including tags, category, description
  const haystack = normalizeText(item.category, ...(item.tags || []), item.description, item.title);
  const match = regionDefinitions.find(def => def.needles.length && def.needles.some(needle => needleMatch(haystack, needle)));
  return match ? match.label : 'Global & Mixed';
}

function inferType(item) {
  const text = ` ${normalizeText(item.category, ...(item.tags || []), item.destination1, item.destination2, item.description, item.title)} `;
  const pair = ` ${(item.destination1 || '').toLowerCase()} ${(item.destination2 || '').toLowerCase()} `;
  if (/(^|\s)(japan|spain|italy|france|greece|thailand|portugal|germany|austria|mexico|croatia|vietnam|india|peru|brazil|canada|australia|colombia|argentina|chile|morocco|egypt)(\s|$)/.test(pair)) return 'Countries';
  if (/(island|islands|beach|beaches|coast|coastal|bay|caye|cay|reef|atoll|tropical)/.test(text)) return 'Islands & beaches';
  if (/(mountain|mountains|lake|lakes|forest|national park|hiking|nature|outdoors|adventure|desert|volcano|safari|falls)/.test(text)) return 'Nature & outdoors';
  if (/(luxury|honeymoon|romance|resort|romantic)/.test(text)) return 'Luxury & honeymoon';
  if (/(food|culture|history|wine|seafood|nightlife|art|museum|shopping)/.test(text)) return 'Food & culture';
  if (/(city|cities|city break|city breaks|urban|capital|downtown|neighborhood|neighbourhood|metro)/.test(text) || !/(country|island|beach|coast|mountain|lake|park)/.test(text)) return 'City breaks';
  return 'Trip style guides';
}

const cards = inventory.map(item => {
  const apiItem = apiBySlug.get(item.slug) || {};
  const updatedAt = item.lastUpdated || apiItem.updatedAt || getMtime(item.slug);
  const tags = [...new Set([...(item.tags || []), ...(apiItem.tags || []), apiItem.category].filter(Boolean))].slice(0, 6);
  const destinationScore = (destinationFrequency.get((item.destination1 || '').toLowerCase()) || 0) + (destinationFrequency.get((item.destination2 || '').toLowerCase()) || 0);
  const inboundScore = inboundLinks.get(item.slug) || 0;
  const recencyScore = updatedAt ? Math.max(0, 45 - Math.floor((Date.now() - Date.parse(updatedAt)) / 86400000)) : 0;
  const popularityScore = inboundScore * 10 + destinationScore * 2 + recencyScore;
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
    region: inferRegion({ ...item, ...apiItem, tags }),
    tripType: inferType({ ...item, ...apiItem, tags }),
    tags,
    inboundLinks: inboundScore,
    destinationScore,
    popularityScore
  };
});

// Deduplicate by slug — inventory.json may have both orderings (e.g. "A vs B" and "B vs A")
const seenSlugs = new Set();
const dedupedCards = [];
for (const card of cards) {
  if (seenSlugs.has(card.slug)) continue;
  seenSlugs.add(card.slug);
  dedupedCards.push(card);
}
cards.length = 0;
cards.push(...dedupedCards);

function sortByPopularity(list) {
  return [...list].sort((a, b) => b.popularityScore - a.popularityScore || b.inboundLinks - a.inboundLinks || a.title.localeCompare(b.title));
}

function sortByNewest(list) {
  return [...list].sort((a, b) => (b.updatedAt || '').localeCompare(a.updatedAt || '') || b.popularityScore - a.popularityScore || a.title.localeCompare(b.title));
}

const regionByLabel = new Map(regionDefinitions.map(def => [def.label, def]));
const typeByLabel = new Map(typeDefinitions.map(def => [def.label, def]));
const featured = featuredSlugs.map(slug => cards.find(card => card.slug === slug)).filter(Boolean);

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
    <div class="mini-top"><strong>${safeText(card.destination1)} vs ${safeText(card.destination2)}</strong><span>${safeText(card.updatedLabel)}</span></div>
    <p>${safeText(card.description)}</p>
  </a>`;
}

function renderBrowseGroup(group, hrefPrefix) {
  return `<section class="browse-card">
    <div class="browse-head"><h3><a href="${hrefPrefix}/${group.slug}/">${safeText(group.label)}</a></h3><span>${group.items.length} pages</span></div>
    <div class="browse-links">${sortByPopularity(group.items).slice(0,4).map(card => `<a href="${card.url}">${safeText(card.destination1)} vs ${safeText(card.destination2)}</a>`).join('')}</div>
    <a class="chip browse-chip" href="${hrefPrefix}/${group.slug}/">Open hub</a>
  </section>`;
}

function baseStyles() {
  return `
  <style>
    :root { --indigo:#2D3A5C; --terracotta:#C4704B; --sand:#E8DFD0; --cream:#FEFCF9; --warm:#F5F0E8; --text:#2C2419; --muted:#6B5D4F; --sage:#7A8B6F; --shadow:0 18px 40px rgba(45,58,92,.08); }
    * { box-sizing:border-box; } html { scroll-behavior:smooth; } body { margin:0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif; background:var(--cream); color:var(--text); line-height:1.55; }
    a { color:inherit; } .shell { max-width:1180px; margin:0 auto; padding:0 24px; }
    .topbar { position:sticky; top:0; z-index:20; background:rgba(254,252,249,.92); backdrop-filter:blur(16px); border-bottom:1px solid rgba(232,223,208,.9); }
    .topbar .shell { display:flex; justify-content:space-between; align-items:center; min-height:72px; gap:20px; }
    .brand { font-size:1.35rem; font-weight:800; text-decoration:none; color:var(--indigo); } .brand span { color:var(--terracotta); }
    .navlinks { display:flex; gap:18px; align-items:center; font-size:.95rem; } .navlinks a { text-decoration:none; color:var(--muted); } .navcta { background:var(--terracotta); color:#fff !important; padding:.7rem 1rem; border-radius:10px; font-weight:700; }
    .hero { padding:72px 0 36px; } .hero-grid { display:grid; grid-template-columns:1.3fr .9fr; gap:28px; align-items:stretch; }
    .hero-copy, .hero-panel, .search-panel, .browse-card, .pillars-card { background:#fff; border:1px solid var(--sand); border-radius:24px; box-shadow:var(--shadow); }
    .hero-copy { padding:34px; } .hero-kicker { display:inline-flex; gap:10px; align-items:center; background:var(--warm); color:var(--terracotta); border-radius:999px; padding:.45rem .85rem; font-size:.9rem; font-weight:700; }
    h1 { font-size:clamp(2.4rem,5vw,4.4rem); line-height:1.04; letter-spacing:-.04em; color:var(--indigo); margin:18px 0 16px; } .hero-copy p { font-size:1.08rem; color:var(--muted); max-width:58ch; margin:0 0 22px; }
    .hero-actions { display:flex; flex-wrap:wrap; gap:12px; } .button,.chip { display:inline-flex; align-items:center; justify-content:center; gap:10px; padding:.95rem 1.25rem; border-radius:12px; text-decoration:none; font-weight:700; border:1px solid transparent; background:#fff; }
    .button.primary { background:var(--indigo); color:#fff; } .button.secondary,.chip { border-color:var(--sand); color:var(--indigo); }
    .hero-stats { margin-top:22px; padding-top:22px; border-top:1px solid var(--sand); display:grid; grid-template-columns:repeat(3,1fr); gap:16px; } .hero-stats strong { display:block; font-size:1.55rem; color:var(--indigo); } .hero-stats span { font-size:.95rem; color:var(--muted); }
    .hero-panel { padding:28px; display:grid; gap:16px; } .hero-panel h2,.pillars-card h2 { margin:0; color:var(--indigo); font-size:1.15rem; } .hero-list,.pillar-list,.browse-links { display:grid; gap:12px; }
    .hero-list a,.pillar-list a { text-decoration:none; padding:14px 16px; border-radius:16px; background:var(--warm); border:1px solid transparent; } .hero-list a:hover,.pillar-list a:hover { border-color:var(--sand); }
    .hero-list strong,.pillar-list strong { display:block; } .hero-list span,.pillar-list span { display:block; color:var(--muted); font-size:.92rem; margin-top:4px; }
    .section { padding:18px 0; } .section-header { display:flex; justify-content:space-between; align-items:end; gap:20px; margin-bottom:18px; } .section-header h2 { margin:0; color:var(--indigo); font-size:1.8rem; letter-spacing:-.03em; } .section-header p { margin:6px 0 0; color:var(--muted); max-width:56ch; }
    .feature-grid,.mini-grid,.browse-grid,.pillar-grid { display:grid; gap:18px; grid-template-columns:repeat(3,1fr); }
    .feature-card,.mini-card,.archive-row { background:#fff; border:1px solid var(--sand); border-radius:20px; overflow:hidden; text-decoration:none; box-shadow:var(--shadow); }
    .feature-image { height:190px; background:linear-gradient(135deg, rgba(45,58,92,.15), rgba(196,112,75,.15)); background-size:cover; background-position:center; }
    .feature-body { padding:18px; } .eyebrow { font-size:.82rem; text-transform:uppercase; letter-spacing:.08em; font-weight:700; color:var(--terracotta); } .feature-body h3,.mini-card strong,.archive-row h3,.browse-head h3 { margin:8px 0 10px; color:var(--indigo); font-size:1.15rem; }
    .feature-body p,.mini-card p,.archive-row p,.browse-card p { margin:0; color:var(--muted); } .feature-link { display:inline-block; margin-top:14px; font-weight:700; color:var(--indigo); }
    .mini-card { padding:18px; } .mini-top { display:flex; justify-content:space-between; gap:16px; align-items:flex-start; } .mini-top span { color:var(--muted); font-size:.88rem; white-space:nowrap; }
    .pillars-card,.browse-card,.search-panel { padding:20px 24px; }
    .browse-head,.archive-meta { display:flex; justify-content:space-between; gap:14px; align-items:baseline; margin-bottom:14px; } .browse-head span,.archive-label,.archive-meta,.browse-links a { color:var(--muted); font-size:.92rem; text-decoration:none; }
    .browse-chip { margin-top:14px; } .archive-toolbar { display:grid; grid-template-columns:2fr repeat(3,1fr); gap:12px; margin-top:18px; } .field { border:1px solid var(--sand); background:#fff; border-radius:12px; min-height:48px; padding:0 14px; font:inherit; color:var(--text); }
    .quick-chips { display:flex; flex-wrap:wrap; gap:10px; margin-top:16px; } .archive-list { margin-top:18px; display:grid; gap:12px; } .archive-row { display:grid; grid-template-columns:minmax(0,1.4fr) .65fr .65fr 96px; gap:16px; align-items:start; padding:18px; }
    .archive-row p { font-size:.95rem; } .archive-label strong { color:var(--indigo); } .archive-empty { padding:26px; border-radius:18px; background:var(--warm); color:var(--muted); border:1px dashed var(--sand); }
    .footer { padding:42px 0 60px; color:var(--muted); }
    @media (max-width: 1040px) { .hero-grid,.feature-grid,.mini-grid,.browse-grid,.pillar-grid{grid-template-columns:1fr 1fr;} .archive-toolbar{grid-template-columns:1fr 1fr;} .archive-row{grid-template-columns:1fr 1fr;} }
    @media (max-width: 720px) { .shell{padding:0 16px;} .navlinks a:not(.navcta){display:none;} .hero-grid,.feature-grid,.mini-grid,.browse-grid,.pillar-grid,.archive-toolbar,.archive-row,.hero-stats{grid-template-columns:1fr;} .hero{padding-top:34px;} .section-header,.archive-meta,.mini-top,.browse-head{display:block;} }
  </style>`;
}

function navHtml() {
  return `<header class="topbar"><div class="shell"><a class="brand" href="/">tabi<span>ji</span></a><nav class="navlinks"><a href="/destinations/">Destinations</a><a href="/compare/">Compare</a><a href="/plan">Plan a trip</a><a class="navcta" href="/plan">Get itinerary</a></nav></div></header>`;
}

function renderArchiveScript(cardsForPage, searchOptions = { region: true, type: true }) {
  return `<script>
    const cards = ${JSON.stringify(cardsForPage)};
    const searchInput = document.getElementById('searchInput');
    const regionFilter = document.getElementById('regionFilter');
    const typeFilter = document.getElementById('typeFilter');
    const sortFilter = document.getElementById('sortFilter');
    const archiveList = document.getElementById('archiveList');
    const resultCount = document.getElementById('resultCount');
    function rowTemplate(card) {
      return '<a class="archive-row" href="' + card.url + '">' + '<div><h3>' + card.destination1 + ' vs ' + card.destination2 + '</h3><p>' + card.description + '</p></div>' + '<div class="archive-label"><strong>Region</strong><br>' + card.region + '</div>' + '<div class="archive-label"><strong>Type</strong><br>' + card.tripType + '</div>' + '<div class="archive-label"><strong>Signals</strong><br>' + card.inboundLinks + ' links</div>' + '</a>';
    }
    function applyFilters() {
      const query = searchInput ? searchInput.value.trim().toLowerCase() : '';
      const region = regionFilter ? regionFilter.value : '';
      const type = typeFilter ? typeFilter.value : '';
      const sort = sortFilter ? sortFilter.value : 'popular';
      let filtered = cards.filter(card => {
        const haystack = [card.title, card.description, card.destination1, card.destination2, card.region, card.tripType, ...(card.tags || [])].join(' ').toLowerCase();
        return (!query || haystack.includes(query)) && (!region || card.region === region) && (!type || card.tripType === type);
      });
      filtered = filtered.sort((a,b) => sort === 'az' ? a.title.localeCompare(b.title) : sort === 'newest' ? ((b.updatedAt||'').localeCompare(a.updatedAt||'') || b.popularityScore - a.popularityScore) : (b.popularityScore - a.popularityScore || (b.updatedAt||'').localeCompare(a.updatedAt||'')));
      resultCount.textContent = 'Showing ' + filtered.length + ' comparison' + (filtered.length === 1 ? '' : 's');
      archiveList.innerHTML = filtered.length ? filtered.map(rowTemplate).join('') : '<div class="archive-empty">No matches. Try a broader search.</div>';
    }
    [searchInput, regionFilter, typeFilter, sortFilter].filter(Boolean).forEach(el => { el.addEventListener('input', applyFilters); el.addEventListener('change', applyFilters); });
    applyFilters();
  </script>`;
}

function pageHtml({ title, metaDescription, canonicalPath, heroKicker, heroTitle, heroText, heroStats, sidebarTitle, sidebarItems, sections, archiveCards, archivePrefillRegion = '', archivePrefillType = '', introCards = [] }) {
  const regionOptions = [...new Set(cards.map(card => card.region))].sort();
  const typeOptions = [...new Set(cards.map(card => card.tripType))].sort();
  const canonicalUrl = `https://tabiji.ai${canonicalPath}`;
  const ogImage = 'https://img.tabiji.ai/compare-default-og.jpg';
  const breadcrumbName = heroTitle;
  const faqItems = [
    {
      question: `What is the ${heroTitle} compare hub?`,
      answer: `This page is a compare hub for ${heroTitle.toLowerCase()}. It groups related destination matchups into one ranked archive so travelers can browse by theme instead of hunting through a flat compare index.`
    },
    {
      question: 'How are comparisons ranked here?',
      answer: 'Ranking blends inbound compare-page links, destination frequency across the catalog, and freshness. It is designed to surface stronger traveler-decision pages before long-tail comparisons.'
    },
    {
      question: 'How should I use this page?',
      answer: 'Use the popular and newest sections as a quick shortlist, then use the ranked archive filters to narrow by region, trip type, or destination keywords.'
    }
  ];
  return `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>${safeText(title)}</title><meta name="description" content="${safeText(metaDescription)}"><link rel="canonical" href="${canonicalUrl}"><meta property="og:title" content="${safeText(title)}"><meta property="og:description" content="${safeText(metaDescription)}"><meta property="og:type" content="website"><meta property="og:url" content="${canonicalUrl}"><meta property="og:image" content="${ogImage}"><meta property="og:site_name" content="tabiji.ai"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="${safeText(title)}"><meta name="twitter:description" content="${safeText(metaDescription)}"><meta name="twitter:image" content="${ogImage}"><meta name="robots" content="index, follow, max-image-preview:large"><script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":${JSON.stringify(title)},"headline":${JSON.stringify(title)},"description":${JSON.stringify(metaDescription)},"url":${JSON.stringify(canonicalUrl)},"image":${JSON.stringify(ogImage)},"publisher":{"@type":"Organization","name":"tabiji.ai","url":"https://tabiji.ai"},"mainEntity":{"@type":"ItemList","numberOfItems":${archiveCards.length}}}</script><script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://tabiji.ai/"},{"@type":"ListItem","position":2,"name":"Compare","item":"https://tabiji.ai/compare/"},{"@type":"ListItem","position":3,"name":${JSON.stringify(breadcrumbName)},"item":${JSON.stringify(canonicalUrl)}}]}</script><script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":${JSON.stringify(faqItems.map(item => ({ '@type': 'Question', name: item.question, acceptedAnswer: { '@type': 'Answer', text: item.answer } })))}}</script>${baseStyles()}</head><body>${navHtml()}<main><section class="hero"><div class="shell hero-grid"><div class="hero-copy"><div class="hero-kicker">${safeText(heroKicker)}</div><h1>${safeText(heroTitle)}</h1><p>${safeText(heroText)}</p><div class="hero-actions"><a class="button primary" href="#archive">Browse ranked comparisons</a><a class="button secondary" href="/compare/">Back to compare home</a></div><div class="hero-stats">${heroStats.map(stat => `<div><strong>${safeText(stat.value)}</strong><span>${safeText(stat.label)}</span></div>`).join('')}</div></div><aside class="hero-panel"><h2>${safeText(sidebarTitle)}</h2><div class="hero-list">${sidebarItems.map(item => `<a href="${item.href}"><strong>${safeText(item.title)}</strong><span>${safeText(item.text)}</span></a>`).join('')}</div></aside></div></section><section class="section" id="toc"><div class="shell"><div class="search-panel toc-panel"><div class="section-header"><div><h2>On this page</h2><p>Use the hub like a real browse surface, not a dead-end index.</p></div></div><div class="quick-chips"><a class="chip" href="#popular">Popular picks</a><a class="chip" href="#newest">Newest</a><a class="chip" href="#archive">Ranked archive</a><a class="chip" href="#faq">FAQ</a><a class="chip" href="#cta">Plan a trip</a></div></div></div></section>${sections.join('')}<section class="section" id="faq"><div class="shell"><div class="search-panel"><div class="section-header"><div><h2>FAQ</h2><p>Quick answers so these compare hubs read like intentional landing pages, not orphaned utility pages.</p></div></div><div class="archive-list">${faqItems.map(item => `<div class="archive-row"><div><h3>${safeText(item.question)}</h3><p>${safeText(item.answer)}</p></div><div class="archive-label"><strong>Page type</strong><br>Compare hub</div><div class="archive-label"><strong>Use case</strong><br>Browse + shortlist</div><div class="archive-label"><strong>Scope</strong><br>${archiveCards.length} pages</div></div>`).join('')}</div></div></div></section><section class="section" id="archive"><div class="shell"><div class="search-panel"><div class="section-header"><div><h2>Ranked archive</h2><p>Popularity uses inbound compare-page links plus destination frequency and recency, so this is better than pure alphabetical dumping.</p></div></div><div class="archive-toolbar"><input id="searchInput" class="field" type="search" placeholder="Search destinations, tags, or themes…">${archivePrefillRegion ? `<input id="regionFilter" class="field" value="${safeText(archivePrefillRegion)}" disabled>` : `<select id="regionFilter" class="field"><option value="">All regions</option>${regionOptions.map(region => `<option value="${safeText(region)}">${safeText(region)}</option>`).join('')}</select>`}${archivePrefillType ? `<input id="typeFilter" class="field" value="${safeText(archivePrefillType)}" disabled>` : `<select id="typeFilter" class="field"><option value="">All trip types</option>${typeOptions.map(type => `<option value="${safeText(type)}">${safeText(type)}</option>`).join('')}</select>`}<select id="sortFilter" class="field"><option value="popular">Most popular</option><option value="newest">Newest</option><option value="az">A–Z</option></select></div><div class="archive-meta"><div id="resultCount">Showing ${archiveCards.length} comparisons</div><div>Signals: inbound compare links + destination demand + freshness</div></div><div id="archiveList" class="archive-list"></div></div></div></section><section class="section" id="cta"><div class="shell"><div class="search-panel"><div class="section-header"><div><h2>Need a trip recommendation?</h2><p>If this hub helped you narrow the field, Tabiji can turn the shortlist into an actual route, city split, or day-by-day plan.</p></div></div><div class="hero-actions"><a class="button primary" href="/plan">Get itinerary</a><a class="button secondary" href="/compare/">Browse all compare pages</a></div></div></div></section></main><footer class="footer"><div class="shell">Tabiji compare hubs now have dedicated browse pages and ranking, instead of one flat directory.</div></footer>${renderArchiveScript(archiveCards)}</body></html>`;
}

function homepageSections(cards) {
  const newest = sortByNewest(cards).slice(0, 6);
  const mostPopular = sortByPopularity(cards).slice(0, 6);
  const regionGroups = regionDefinitions.map(def => ({ ...def, items: cards.filter(card => card.region === def.label) })).filter(group => group.items.length);
  const typeGroups = typeDefinitions.map(def => ({ ...def, items: cards.filter(card => card.tripType === def.label) })).filter(group => group.items.length);
  return {
    sections: [
      `<section class="section"><div class="shell"><div class="section-header"><div><h2>Featured comparisons</h2><p>High-intent matchups that work well as front doors into the rest of the catalog.</p></div></div><div class="feature-grid">${featured.map(renderFeaturedCard).join('')}</div></div></section>`,
      `<section class="section"><div class="shell"><div class="section-header"><div><h2>Most popular right now</h2><p>Ranked using inbound compare-page links, destination demand across the catalog, and freshness.</p></div></div><div class="mini-grid">${mostPopular.map(renderMiniCard).join('')}</div></div></section>`,
      `<section class="section"><div class="shell"><div class="section-header"><div><h2>Newest comparisons</h2><p>Freshly updated pages, kept visible without making the homepage a giant dump.</p></div></div><div class="mini-grid">${newest.map(renderMiniCard).join('')}</div></div></section>`,
      `<section class="section"><div class="shell"><div class="section-header"><div><h2>Browse by region</h2><p>Dedicated regional hubs now act as entry points instead of forcing a global browse.</p></div></div><div class="browse-grid">${regionGroups.map(group => renderBrowseGroup(group, '/compare')).join('')}</div></div></section>`,
      `<section class="section"><div class="shell"><div class="section-header"><div><h2>Browse by trip type</h2><p>Use type hubs when the traveler knows the kind of trip but not the destination yet.</p></div></div><div class="browse-grid">${typeGroups.map(group => renderBrowseGroup(group, '/compare')).join('')}</div></div></section>`
    ],
    sidebarItems: mostPopular.slice(0,4).map(card => ({ href: card.url, title: `${card.destination1} vs ${card.destination2}`, text: `${card.inboundLinks} internal compare links · ${card.region}` }))
  };
}

function writePage(relPath, html) {
  const filePath = path.join(repoRoot, relPath);
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, html);
}

const home = homepageSections(cards);
writePage('compare/index.html', pageHtml({
  title: `Travel Comparisons | Compare ${cards.length}+ Destinations Side by Side | Tabiji`,
  metaDescription: `Compare ${cards.length}+ destinations side by side with Tabiji. Search ranked comparisons, browse region hubs, and explore trip-type hubs without wading through a flat archive.`,
  canonicalPath: '/compare/',
  heroKicker: 'Compare destinations faster',
  heroTitle: 'The compare homepage, not a giant pile of cards.',
  heroText: `Search ${cards.length}+ side-by-side destination guides, jump into regional sub-indexes, and use ranking signals instead of alphabetical sludge.`,
  heroStats: [{ value: String(cards.length), label: 'published comparisons' }, { value: String(regionDefinitions.length - 1), label: 'regional hubs' }, { value: String(typeDefinitions.length), label: 'trip-type hubs' }],
  sidebarTitle: 'Popular routes',
  sidebarItems: home.sidebarItems,
  sections: home.sections,
  archiveCards: sortByPopularity(cards)
}));

const sitemapUrls = ['/compare/'];
for (const def of regionDefinitions) {
  const items = cards.filter(card => card.region === def.label);
  if (!items.length) continue;
  const top = sortByPopularity(items);
  writePage(`compare/${def.slug}/index.html`, pageHtml({
    title: `${def.label} Travel Comparisons | Tabiji`,
    metaDescription: `${def.intro} Browse ranked ${def.label.toLowerCase()} comparisons by popularity, freshness, and internal traveler-path signals.`,
    canonicalPath: `/compare/${def.slug}/`,
    heroKicker: 'Regional compare hub',
    heroTitle: `${def.label} comparisons`,
    heroText: def.intro,
    heroStats: [{ value: String(items.length), label: 'comparisons in this hub' }, { value: String(top.filter(card => card.inboundLinks > 0).length), label: 'pages with internal-link signals' }, { value: String(Math.max(...top.map(card => card.inboundLinks), 0)), label: 'top inbound-link count' }],
    sidebarTitle: `Top ${def.label} decisions`,
    sidebarItems: top.slice(0,4).map(card => ({ href: card.url, title: `${card.destination1} vs ${card.destination2}`, text: `${card.inboundLinks} internal compare links · ${card.tripType}` })),
    sections: [
      `<section class="section" id="popular"><div class="shell"><div class="section-header"><div><h2>Most popular ${safeText(def.label)} comparisons</h2><p>These are the strongest candidates for internal linking, navigation modules, and future editorial support.</p></div></div><div class="mini-grid">${top.slice(0,6).map(renderMiniCard).join('')}</div></div></section>`,
      `<section class="section" id="newest"><div class="shell"><div class="section-header"><div><h2>Newest in ${safeText(def.label)}</h2><p>Fresh pages in this region stay visible without taking over the whole compare homepage.</p></div></div><div class="mini-grid">${sortByNewest(items).slice(0,6).map(renderMiniCard).join('')}</div></div></section>`
    ],
    archiveCards: top,
    archivePrefillRegion: def.label
  }));
  sitemapUrls.push(`/compare/${def.slug}/`);
}

for (const def of typeDefinitions) {
  const items = cards.filter(card => card.tripType === def.label);
  if (!items.length) continue;
  const top = sortByPopularity(items);
  writePage(`compare/${def.slug}/index.html`, pageHtml({
    title: `${def.label} Travel Comparisons | Tabiji`,
    metaDescription: `${def.intro} Browse ranked ${def.label.toLowerCase()} comparisons built for faster destination decisions.`,
    canonicalPath: `/compare/${def.slug}/`,
    heroKicker: 'Trip-type compare hub',
    heroTitle: `${def.label} comparisons`,
    heroText: def.intro,
    heroStats: [{ value: String(items.length), label: 'comparisons in this hub' }, { value: String(top.filter(card => card.inboundLinks > 0).length), label: 'pages with internal-link signals' }, { value: String(Math.max(...top.map(card => card.inboundLinks), 0)), label: 'top inbound-link count' }],
    sidebarTitle: `Top ${def.label} picks`,
    sidebarItems: top.slice(0,4).map(card => ({ href: card.url, title: `${card.destination1} vs ${card.destination2}`, text: `${card.inboundLinks} internal compare links · ${card.region}` })),
    sections: [
      `<section class="section" id="popular"><div class="shell"><div class="section-header"><div><h2>Most popular ${safeText(def.label)} comparisons</h2><p>Use this hub as a better browse surface than the flat archive.</p></div></div><div class="mini-grid">${top.slice(0,6).map(renderMiniCard).join('')}</div></div></section>`,
      `<section class="section" id="newest"><div class="shell"><div class="section-header"><div><h2>Newest in ${safeText(def.label)}</h2><p>Recently updated pages in this category.</p></div></div><div class="mini-grid">${sortByNewest(items).slice(0,6).map(renderMiniCard).join('')}</div></div></section>`
    ],
    archiveCards: top,
    archivePrefillType: def.label
  }));
  sitemapUrls.push(`/compare/${def.slug}/`);
}

if (fs.existsSync(sitemapPath)) {
  let sitemap = fs.readFileSync(sitemapPath, 'utf8');
  const existing = new Set([...sitemap.matchAll(/<loc>https:\/\/tabiji\.ai([^<]+)<\/loc>/g)].map(m => m[1]));
  const additions = sitemapUrls.filter(url => !existing.has(url)).map(url => `  <url>\n    <loc>https://tabiji.ai${url}</loc>\n  </url>`).join('\n');
  if (additions) sitemap = sitemap.replace('</urlset>', `${additions}\n</urlset>`);
  fs.writeFileSync(sitemapPath, sitemap);
}

console.log(`Generated compare homepage + ${sitemapUrls.length - 1} hub pages.`);
