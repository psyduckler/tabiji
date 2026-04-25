const { escapeHtml } = require('./utils');

function absoluteUrl(value = '') {
  if (!value) return '';
  if (/^https?:\/\//i.test(value)) {
    return value.replace('https://tabiji.ai/popular-picks/', 'https://img.tabiji.ai/popular-picks/');
  }
  return `https://tabiji.ai${value.startsWith('/') ? value : `/${value}`}`;
}

// Trim the rendered <title> to avoid SERP truncation (Google cuts off ~60 chars,
// most templates target 70 max). Sources are stored with the full marketing
// suffix; if the page name itself is long enough that the suffix pushes total
// length past 70 chars, drop pieces of the suffix in this order:
//   1. " (2026)"             — year tag (7 chars)
//   2. " — Reddit-Backed Guide" — marketing claim (22 chars)
//   3. " | tabiji.ai"         — site brand (12 chars; last resort, prefer to keep)
// We never trim the page name itself — that's the searchable content.
function trimTitle(title = '', limit = 70) {
  let t = String(title);
  if (t.length <= limit) return t;
  t = t.replace(/\s\(20\d{2}\)/, '');
  if (t.length <= limit) return t;
  t = t.replace(/\s—\sReddit-Backed Guide/, '');
  if (t.length <= limit) return t;
  t = t.replace(/\s\|\stabiji\.ai$/, '');
  return t;
}

function renderMeta(data) {
  const { seo } = data;
  const canonical = absoluteUrl(seo.canonicalPath);
  const heroImage = absoluteUrl(seo.heroImage || '');
  const title = trimTitle(seo.metaTitle);
  const ogTitle = trimTitle(seo.ogTitle || seo.metaTitle);
  const twitterTitle = trimTitle(seo.twitterTitle || seo.ogTitle || seo.metaTitle);

  return [
    '<meta charset="UTF-8">',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
    '<link rel="preconnect" href="https://img.tabiji.ai">',
    '<link rel="icon" type="image/x-icon" href="/favicon.ico">',
    '<link rel="apple-touch-icon" sizes="180x180" href="https://img.tabiji.ai/apple-touch-icon.png">',
    '<link rel="icon" type="image/png" sizes="192x192" href="https://img.tabiji.ai/icon-192.png">',
    `<title>${escapeHtml(title)}</title>`,
    `<meta name="description" content="${escapeHtml(seo.metaDescription)}">`,
    `<meta name="robots" content="${escapeHtml(seo.robots || 'index, follow, max-image-preview:large')}">`,
    `<link rel="canonical" href="${escapeHtml(canonical)}">`,
    `<meta property="og:title" content="${escapeHtml(ogTitle)}">`,
    `<meta property="og:description" content="${escapeHtml(seo.ogDescription || seo.metaDescription)}">`,
    '<meta property="og:type" content="article">',
    `<meta property="og:url" content="${escapeHtml(canonical)}">`,
    heroImage ? `<meta property="og:image" content="${escapeHtml(heroImage)}">` : '',
    heroImage ? '<meta property="og:image:width" content="1200">' : '',
    heroImage ? '<meta property="og:image:height" content="675">' : '',
    '<meta property="og:site_name" content="tabiji.ai">',
    '<meta name="twitter:card" content="summary_large_image">',
    `<meta name="twitter:title" content="${escapeHtml(twitterTitle)}">`,
    `<meta name="twitter:description" content="${escapeHtml(seo.twitterDescription || seo.ogDescription || seo.metaDescription)}">`,
    heroImage ? `<meta name="twitter:image" content="${escapeHtml(heroImage)}">` : '',
    seo.publishedTime && seo.publishedTime !== 'null' ? `<meta property="article:published_time" content="${escapeHtml(seo.publishedTime)}">` : '',
    seo.modifiedTime && seo.modifiedTime !== 'null' ? `<meta property="article:modified_time" content="${escapeHtml(seo.modifiedTime)}">` : ''
  ].filter(Boolean).join('\n    ');
}

module.exports = { renderMeta, escapeHtml, absoluteUrl };
