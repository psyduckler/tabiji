const { escapeHtml } = require('./utils');

function absoluteUrl(value = '') {
  if (!value) return '';
  if (/^https?:\/\//i.test(value)) return value;
  return `https://tabiji.ai${value.startsWith('/') ? value : `/${value}`}`;
}

function renderMeta(data) {
  const { seo } = data;
  const canonical = absoluteUrl(seo.canonicalPath);
  const heroImage = absoluteUrl(seo.heroImage || '');

  return [
    '<meta charset="UTF-8">',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
    '<link rel="icon" type="image/x-icon" href="/favicon.ico">',
    '<link rel="apple-touch-icon" sizes="180x180" href="https://img.tabiji.ai/apple-touch-icon.png">',
    '<link rel="icon" type="image/png" sizes="192x192" href="https://img.tabiji.ai/icon-192.png">',
    `<title>${escapeHtml(seo.metaTitle)}</title>`,
    `<meta name="description" content="${escapeHtml(seo.metaDescription)}">`,
    `<meta name="robots" content="${escapeHtml(seo.robots || 'index, follow, max-image-preview:large')}">`,
    `<link rel="canonical" href="${escapeHtml(canonical)}">`,
    `<meta property="og:title" content="${escapeHtml(seo.ogTitle || seo.metaTitle)}">`,
    `<meta property="og:description" content="${escapeHtml(seo.ogDescription || seo.metaDescription)}">`,
    '<meta property="og:type" content="article">',
    `<meta property="og:url" content="${escapeHtml(canonical)}">`,
    heroImage ? `<meta property="og:image" content="${escapeHtml(heroImage)}">` : '',
    '<meta property="og:site_name" content="tabiji.ai">',
    '<meta name="twitter:card" content="summary_large_image">',
    `<meta name="twitter:title" content="${escapeHtml(seo.twitterTitle || seo.ogTitle || seo.metaTitle)}">`,
    `<meta name="twitter:description" content="${escapeHtml(seo.twitterDescription || seo.ogDescription || seo.metaDescription)}">`,
    heroImage ? `<meta name="twitter:image" content="${escapeHtml(heroImage)}">` : '',
    `<meta property="article:published_time" content="${escapeHtml(seo.publishedTime)}">`,
    `<meta property="article:modified_time" content="${escapeHtml(seo.modifiedTime)}">`
  ].filter(Boolean).join('\n    ');
}

module.exports = { renderMeta, escapeHtml, absoluteUrl };
