#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const repoRoot = process.cwd();
const compareDir = path.join(repoRoot, 'compare');
const inventoryPath = path.join(compareDir, 'inventory.json');
const apiPath = path.join(repoRoot, 'api', 'v1', 'compare.json');
const sitemapPath = path.join(repoRoot, 'sitemap.xml');

const inventoryRaw = JSON.parse(fs.readFileSync(inventoryPath, 'utf8'));
const inventory = inventoryRaw.cards || [];
const existingApi = JSON.parse(fs.readFileSync(apiPath, 'utf8')).comparisons || [];
const apiBySlug = new Map(existingApi.map(item => [item.slug, item]));

const regionDefinitions = [
  { slug: 'asia', label: 'Asia', needles: ['asia','japan','korea','thailand','taiwan','vietnam','indonesia','bali','philippines','india','sri lanka','malaysia','singapore','hong kong','china','nepal','bhutan','cambodia','laos','myanmar'] },
  { slug: 'europe', label: 'Europe', needles: ['europe','italy','spain','france','greece','croatia','portugal','uk','england','scotland','ireland','netherlands','germany','austria','switzerland','norway','sweden','denmark','iceland','belgium','czech','hungary','poland'] },
  { slug: 'north-america', label: 'North America', needles: ['north america','usa','united states','canada','mexico','hawaii','caribbean','puerto rico'] },
  { slug: 'latin-america', label: 'Latin America', needles: ['latin america','south america','central america','peru','colombia','brazil','argentina','chile','guatemala','costa rica','ecuador','bolivia','uruguay'] },
  { slug: 'oceania', label: 'Oceania', needles: ['oceania','australia','new zealand','fiji','tahiti','french polynesia','bora bora'] },
  { slug: 'middle-east-africa', label: 'Middle East & Africa', needles: ['middle east','africa','morocco','egypt','uae','dubai','abu dhabi','jordan','oman','saudi','seychelles','south africa','tanzania','kenya','madagascar'] }
];

const clusterDefinitions = [
  { slug: 'japan', label: 'Japan', aliases: ['japan','tokyo','kyoto','osaka','nara','hokkaido','okinawa','hakone','kanazawa','fukuoka','kyushu','kansai','kanto','naoshima','miyajima','nikko','kamakura','yakushima','otaru','hakodate'] },
  { slug: 'italy', label: 'Italy', aliases: ['italy','rome','florence','venice','milan','naples','amalfi coast','cinque terre','puglia','sicily','tuscany','dolomites','lake como','capri','positano','sardinia'] },
  { slug: 'thailand', label: 'Thailand', aliases: ['thailand','bangkok','chiang mai','phuket','krabi','koh samui','koh phangan','koh lanta','pai','ayutthaya','sukhothai'] },
  { slug: 'bali', label: 'Bali', aliases: ['bali','ubud','canggu','seminyak','uluwatu','amed','nusa penida'] },
  { slug: 'greece', label: 'Greece', aliases: ['greece','athens','santorini','crete','peloponnese','cyclades','mykonos','corfu','zakynthos'] },
  { slug: 'spain', label: 'Spain', aliases: ['spain','madrid','barcelona','seville','granada','malaga','costa brava','andalusia','cadiz','toledo','segovia','mallorca','ibiza'] },
  { slug: 'portugal', label: 'Portugal', aliases: ['portugal','lisbon','porto','algarve','madeira','azores','sintra'] },
  { slug: 'croatia', label: 'Croatia', aliases: ['croatia','hvar','korcula','split','dubrovnik','vis','brac','zagreb','dalmatian coast'] },
  { slug: 'vietnam', label: 'Vietnam', aliases: ['vietnam','hanoi','ho chi minh','da nang','hoi an','ninh binh','ha long bay','phu quoc','sapa'] },
  { slug: 'mexico', label: 'Mexico', aliases: ['mexico','mexico city','oaxaca','yucatan','riviera maya','playa del carmen','cancun','cabo','guanajuato','san miguel de allende'] },
  { slug: 'iceland', label: 'Iceland', aliases: ['iceland','reykjavik'] },
  { slug: 'maldives', label: 'Maldives', aliases: ['maldives'] },
  { slug: 'morocco', label: 'Morocco', aliases: ['morocco','marrakech','fes','chefchaouen'] },
  { slug: 'egypt', label: 'Egypt', aliases: ['egypt','cairo','luxor','aswan'] },
  { slug: 'australia', label: 'Australia', aliases: ['australia','sydney','melbourne','tasmania','queensland','whitsundays','blue mountains'] },
  { slug: 'new-zealand', label: 'New Zealand', aliases: ['new zealand','queenstown','wanaka','milford sound','abel tasman','south island','north island'] },
  { slug: 'taiwan', label: 'Taiwan', aliases: ['taiwan','taipei','taichung','tainan','alishan','taroko gorge','jiufen','shifen','kaohsiung'] },
  { slug: 'sri-lanka', label: 'Sri Lanka', aliases: ['sri lanka'] },
  { slug: 'hawaii', label: 'Hawaii', aliases: ['hawaii','maui','kauai','oahu','big island'] },
  { slug: 'colombia', label: 'Colombia', aliases: ['colombia','medellin','bogota','cartagena'] }
];

const intentKeywords = {
  beach: ['beach','beaches','island','islands','coast','coastal','snorkel','dive','reef','surf','tropical'],
  culture: ['culture','history','temple','museum','old town','heritage','architecture','tradition'],
  food: ['food','wine','seafood','dining','restaurant','street food','coffee'],
  nightlife: ['nightlife','party','bars','cocktails','club','social'],
  budget: ['budget','cheap','affordable','cost','costs'],
  nature: ['nature','mountain','hiking','forest','lake','safari','wildlife','trail','park','volcano','falls'],
  luxury: ['luxury','honeymoon','romantic','resort','private'],
  family: ['family','kids','child','children'],
  city: ['city','cities','urban','capital','weekend'],
  adventure: ['adventure','trek','trekking','rafting','climbing','outdoors']
};

function slugify(text='') { return String(text).toLowerCase().normalize('NFKD').replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, ''); }
function safeText(v='') { return String(v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function normalizeText(...parts) { return parts.filter(Boolean).join(' ').toLowerCase(); }

function scanInboundLinks() {
  const inbound = new Map();
  for (const card of inventory) inbound.set(card.slug, 0);
  for (const card of inventory) {
    const p = path.join(compareDir, card.slug, 'index.html');
    if (!fs.existsSync(p)) continue;
    const text = fs.readFileSync(p, 'utf8');
    const seen = new Set();
    for (const m of text.matchAll(/href=["'](?:https:\/\/tabiji\.ai)?\/compare\/([^"'/]+)\//g)) {
      const slug = m[1];
      if (!slug || slug === card.slug || seen.has(slug)) continue;
      seen.add(slug);
      inbound.set(slug, (inbound.get(slug) || 0) + 1);
    }
  }
  return inbound;
}

const inboundLinks = scanInboundLinks();
const destinationCounts = new Map();
for (const card of inventory) {
  for (const dest of [card.destination1, card.destination2]) {
    if (!dest) continue;
    const key = slugify(dest);
    destinationCounts.set(key, (destinationCounts.get(key) || 0) + 1);
  }
}

function inferRegion(card) {
  const text = normalizeText(card.destination1, card.destination2, card.title, card.description, ...(card.tags || []));
  const hit = regionDefinitions.find(def => def.needles.some(n => text.includes(n)));
  return hit ? hit.label : 'Global & Mixed';
}

function inferTripType(card) {
  const text = normalizeText(card.destination1, card.destination2, card.title, card.description, ...(card.tags || []));
  if (/(country|countries)/.test(text)) return 'Countries';
  if (/(island|beach|coast|reef|surf|tropical)/.test(text)) return 'Islands & beaches';
  if (/(mountain|lake|hiking|nature|safari|trail|park|volcano|falls|outdoors)/.test(text)) return 'Nature & outdoors';
  if (/(luxury|honeymoon|romantic|resort)/.test(text)) return 'Luxury & honeymoon';
  if (/(food|wine|museum|history|culture|nightlife|shopping|art)/.test(text)) return 'Food & culture';
  return 'City breaks';
}

function inferIntents(card) {
  const text = normalizeText(card.destination1, card.destination2, card.title, card.description, ...(card.tags || []));
  const intents = Object.entries(intentKeywords)
    .filter(([, words]) => words.some(word => text.includes(word)))
    .map(([intent]) => intent);
  return intents.length ? intents.slice(0, 4) : ['culture'];
}

function inferCluster(card) {
  const text = normalizeText(card.destination1, card.destination2, card.title, ...(card.tags || []));
  const hit = clusterDefinitions.find(def => def.aliases.some(alias => text.includes(alias)));
  if (hit) return hit.slug;
  const d1 = slugify(card.destination1 || '');
  if ((destinationCounts.get(d1) || 0) >= 4) return d1;
  return null;
}

function getUpdatedAt(card, apiItem) {
  if (card.lastUpdated) return /T/.test(card.lastUpdated) ? card.lastUpdated : `${card.lastUpdated}T00:00:00Z`;
  if (apiItem?.updatedAt) return apiItem.updatedAt;
  try { return fs.statSync(path.join(compareDir, card.slug, 'index.html')).mtime.toISOString(); } catch { return null; }
}

const enriched = inventory.map(card => {
  const apiItem = apiBySlug.get(card.slug) || {};
  const region = inferRegion(card);
  const tripType = inferTripType(card);
  const intents = inferIntents(card);
  const cluster = inferCluster(card);
  const updatedAt = getUpdatedAt(card, apiItem);
  const destinationScore = (destinationCounts.get(slugify(card.destination1 || '')) || 0) + (destinationCounts.get(slugify(card.destination2 || '')) || 0);
  const inbound = inboundLinks.get(card.slug) || 0;
  const recency = updatedAt ? Math.max(0, 30 - Math.floor((Date.now() - Date.parse(updatedAt)) / 86400000)) : 0;
  const popularityScore = inbound * 10 + destinationScore * 2 + recency;
  return {
    ...card,
    region,
    tripType,
    intents,
    cluster,
    popularityScore,
    inboundLinks: inbound,
    updatedAt,
    url: `https://tabiji.ai/compare/${card.slug}/`
  };
});

function relatedScore(a, b) {
  let score = 0;
  if (a.slug === b.slug) return -1;
  if (a.cluster && a.cluster === b.cluster) score += 40;
  if (a.region === b.region) score += 18;
  if (a.tripType === b.tripType) score += 12;
  score += a.intents.filter(x => b.intents.includes(x)).length * 8;
  const sharedTags = (a.tags || []).filter(tag => (b.tags || []).includes(tag)).length;
  score += sharedTags * 3;
  const aDest = [slugify(a.destination1), slugify(a.destination2)];
  const bText = normalizeText(b.destination1, b.destination2, ...(b.tags || []), b.title);
  score += aDest.filter(d => d && bText.includes(d.replace(/-/g, ' '))).length * 6;
  score += Math.min(10, b.inboundLinks || 0);
  return score;
}

const bySlug = new Map(enriched.map(card => [card.slug, card]));
for (const card of enriched) {
  card.relatedSlugs = enriched
    .map(other => ({ slug: other.slug, score: relatedScore(card, other) }))
    .filter(x => x.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 6)
    .map(x => x.slug);
}

fs.writeFileSync(inventoryPath, JSON.stringify({ cards: enriched }, null, 2) + '\n');

const aggregateApi = {
  count: enriched.length,
  comparisons: enriched
    .slice()
    .sort((a, b) => b.popularityScore - a.popularityScore || a.slug.localeCompare(b.slug))
    .map(card => ({
      id: `compare:${card.slug}`,
      type: 'compare',
      slug: card.slug,
      title: card.title,
      destination1: card.destination1,
      destination2: card.destination2,
      url: card.url,
      sourceUrl: card.url,
      updatedAt: card.updatedAt,
      tags: card.tags || [],
      region: card.region,
      tripType: card.tripType,
      intents: card.intents,
      cluster: card.cluster,
      popularityScore: card.popularityScore,
      inboundLinks: card.inboundLinks,
      relatedSlugs: card.relatedSlugs
    }))
};
fs.writeFileSync(apiPath, JSON.stringify(aggregateApi, null, 2) + '\n');

const relatedStyles = `
.related-comparisons { border-top: 1px solid var(--sand); padding-top: 2.5rem; margin-top: 2.5rem; }
.related-comparisons h2 { font-size: 1.5rem; color: var(--indigo); margin-bottom: .75rem; }
.related-comparisons > p { color: var(--text-muted); margin-bottom: 1.25rem; }
.related-grid { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }
.related-card { display:block; text-decoration:none; border:1px solid var(--sand); border-radius:14px; padding:1rem 1.1rem; background:rgba(245,240,232,.32); }
.related-card h3 { font-size: 1rem; color: var(--indigo); margin-bottom: .35rem; }
.related-card p { font-size: .92rem; color: var(--text-muted); margin-bottom: .55rem; }
.related-meta { font-size: .8rem; color: var(--earth); }
`;

for (const card of enriched) {
  const filePath = path.join(compareDir, card.slug, 'index.html');
  if (!fs.existsSync(filePath)) continue;
  let html = fs.readFileSync(filePath, 'utf8');
  html = html.replace(/<!-- compare-related:start -->[\s\S]*?<!-- compare-related:end -->\n?/g, '');
  if (!html.includes('.related-comparisons')) html = html.replace('</style>', `${relatedStyles}\n</style>`);
  const relatedCards = card.relatedSlugs.map(slug => bySlug.get(slug)).filter(Boolean);
  const clusterDef = clusterDefinitions.find(def => def.slug === card.cluster);
  const hubLink = clusterDef ? `<p><a href="/compare/${clusterDef.slug}/">Browse all ${safeText(clusterDef.label)} comparisons →</a></p>` : '';
  const sectionHtml = `<!-- compare-related:start -->\n<section class="related-comparisons">\n<h2>Related comparisons</h2>\n<p>If you're still deciding, these are the closest next reads based on destination cluster, trip type, and internal compare-link patterns.</p>\n<div class="related-grid">\n${relatedCards.map(item => `<a class="related-card" href="/compare/${item.slug}/"><h3>${safeText(item.destination1)} vs ${safeText(item.destination2)}</h3><p>${safeText(item.description || '')}</p><div class="related-meta">${safeText(item.region)} · ${safeText(item.tripType)}</div></a>`).join('\n')}\n</div>\n${hubLink}\n</section>\n<!-- compare-related:end -->\n`;
  if (html.includes('<div class="cta-section">')) html = html.replace('<div class="cta-section">', `${sectionHtml}<div class="cta-section">`);
  else if (html.includes('<section class="viator-section">')) html = html.replace('<section class="viator-section">', `${sectionHtml}<section class="viator-section">`);
  else if (html.includes('<!-- @include:footer:start -->')) html = html.replace('<!-- @include:footer:start -->', `${sectionHtml}<!-- @include:footer:start -->`);
  fs.writeFileSync(filePath, html);
}

function basePage(title, desc, canonical, heroTitle, heroText, cards) {
  return `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>${safeText(title)}</title><meta name="description" content="${safeText(desc)}"><link rel="canonical" href="https://tabiji.ai${canonical}"><meta property="og:title" content="${safeText(title)}"><meta property="og:description" content="${safeText(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="https://tabiji.ai${canonical}"><style>:root{--indigo:#2D3A5C;--terracotta:#C4704B;--sand:#E8DFD0;--cream:#FEFCF9;--warm:#F5F0E8;--text:#2C2419;--muted:#6B5D4F;--shadow:0 18px 40px rgba(45,58,92,.08)}*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;background:var(--cream);color:var(--text);line-height:1.55}a{color:inherit}.shell{max-width:1160px;margin:0 auto;padding:0 24px}.topbar{position:sticky;top:0;z-index:20;background:rgba(254,252,249,.92);backdrop-filter:blur(16px);border-bottom:1px solid rgba(232,223,208,.9)}.topbar .shell{display:flex;justify-content:space-between;align-items:center;min-height:72px}.brand{font-size:1.35rem;font-weight:800;text-decoration:none;color:var(--indigo)}.brand span{color:var(--terracotta)}.hero{padding:72px 0 28px}.hero-card,.section-card,.row{background:#fff;border:1px solid var(--sand);border-radius:22px;box-shadow:var(--shadow)}.hero-card{padding:32px}.eyebrow{display:inline-block;background:var(--warm);color:var(--terracotta);border-radius:999px;padding:.42rem .8rem;font-weight:700;font-size:.88rem}h1{font-size:clamp(2.2rem,5vw,4rem);line-height:1.05;color:var(--indigo);margin:16px 0 12px;letter-spacing:-.04em}.hero-card p{font-size:1.05rem;color:var(--muted);max-width:62ch}.statgrid,.grid{display:grid;gap:16px}.statgrid{grid-template-columns:repeat(3,1fr);margin-top:22px;padding-top:20px;border-top:1px solid var(--sand)}.statgrid strong{display:block;font-size:1.5rem;color:var(--indigo)}.section{padding:18px 0}.section-head{margin-bottom:16px}.section-head h2{margin:0;color:var(--indigo);font-size:1.75rem}.section-head p{margin:.4rem 0 0;color:var(--muted)}.grid{grid-template-columns:repeat(3,1fr)}.row{display:block;padding:18px;text-decoration:none}.row h3{margin:0 0 .4rem;color:var(--indigo);font-size:1.05rem}.row p{margin:0 0 .55rem;color:var(--muted);font-size:.95rem}.meta{font-size:.83rem;color:#8B7355}.footer{padding:40px 0 60px;color:var(--muted)}@media(max-width:900px){.grid,.statgrid{grid-template-columns:1fr 1fr}}@media(max-width:680px){.shell{padding:0 16px}.grid,.statgrid{grid-template-columns:1fr}}</style><script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":${JSON.stringify(title)},"description":${JSON.stringify(desc)},"url":${JSON.stringify('https://tabiji.ai' + canonical)},"publisher":{"@type":"Organization","name":"tabiji.ai","url":"https://tabiji.ai"}}</script></head><body><header class="topbar"><div class="shell"><a class="brand" href="/">tabi<span>ji</span></a></div></header><main><section class="hero"><div class="shell"><div class="hero-card"><div class="eyebrow">Destination cluster hub</div><h1>${safeText(heroTitle)}</h1><p>${safeText(heroText)}</p><div class="statgrid"><div><strong>${cards.length}</strong><span>comparisons</span></div><div><strong>${cards.filter(c => c.inboundLinks > 0).length}</strong><span>already internally linked</span></div><div><strong>${Math.max(...cards.map(c => c.popularityScore), 0)}</strong><span>top popularity score</span></div></div></div></div></section><section class="section"><div class="shell"><div class="section-head"><h2>Top comparisons</h2><p>Ranked by explicit popularity signals, not alphabetical order.</p></div><div class="grid">${cards.slice(0,12).map(c => `<a class="row" href="/compare/${c.slug}/"><h3>${safeText(c.destination1)} vs ${safeText(c.destination2)}</h3><p>${safeText(c.description || '')}</p><div class="meta">${safeText(c.tripType)} · ${c.inboundLinks} internal links · score ${c.popularityScore}</div></a>`).join('')}</div></div></section></main><footer class="footer"><div class="shell">Tabiji compare hubs are now layered: homepage, region/type hubs, and destination clusters.</div></footer></body></html>`;
}

const clusterCounts = new Map();
for (const card of enriched) if (card.cluster) clusterCounts.set(card.cluster, (clusterCounts.get(card.cluster) || 0) + 1);
const clusterPages = [];
for (const def of clusterDefinitions) {
  const cardsForCluster = enriched.filter(card => card.cluster === def.slug).sort((a,b) => b.popularityScore - a.popularityScore || a.slug.localeCompare(b.slug));
  if (cardsForCluster.length < 4) continue;
  const relDir = path.join(compareDir, def.slug);
  fs.mkdirSync(relDir, { recursive: true });
  fs.writeFileSync(path.join(relDir, 'index.html'), basePage(`${def.label} Travel Comparisons | Tabiji`, `Browse ${def.label} destination comparisons with related reads and explicit ranking signals.`, `/compare/${def.slug}/`, `${def.label} comparisons`, `This hub groups ${def.label}-related compare pages into one browse surface, then ranks them using internal compare links, destination demand, and freshness.`, cardsForCluster));
  clusterPages.push(`/compare/${def.slug}/`);
}

if (fs.existsSync(sitemapPath)) {
  let sitemap = fs.readFileSync(sitemapPath, 'utf8');
  const existing = new Set([...sitemap.matchAll(/<loc>https:\/\/tabiji\.ai([^<]+)<\/loc>/g)].map(m => m[1]));
  const additions = clusterPages.filter(url => !existing.has(url)).map(url => `  <url>\n    <loc>https://tabiji.ai${url}</loc>\n  </url>`).join('\n');
  if (additions) sitemap = sitemap.replace('</urlset>', `${additions}\n</urlset>`);
  fs.writeFileSync(sitemapPath, sitemap);
}

console.log(`Enriched ${enriched.length} compare records, updated related modules, and generated ${clusterPages.length} destination cluster hubs.`);
