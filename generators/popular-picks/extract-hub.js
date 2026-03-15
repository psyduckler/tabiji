#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { writeText } = require('./utils');

function matchOne(html, regex) {
  const match = html.match(regex);
  if (!match) return null;
  const value = match[1] !== undefined ? match[1] : match[0];
  return value != null ? String(value).trim() : null;
}

function stripTags(value = '') {
  return String(value)
    .replace(/<br\s*\/?>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function decodeBasicEntities(value = '') {
  return String(value)
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&nbsp;/g, ' ')
    .trim();
}

function extractJsonLdBlocks(html) {
  const blocks = [];
  const regex = /<script type="application\/ld\+json">\s*([\s\S]*?)\s*<\/script>/g;
  let match;
  while ((match = regex.exec(html))) {
    try {
      blocks.push(JSON.parse(match[1]));
    } catch {
      blocks.push({ parseError: true, raw: match[1].slice(0, 500) });
    }
  }
  return blocks;
}

function extractToc(html) {
  const toc = [];
  for (const m of html.matchAll(/<li><a href="#([^"]+)">(.*?)<\/a><\/li>/g)) {
    const id = m[1];
    const label = stripTags(m[2]);
    if (!toc.find((item) => item.id === id)) toc.push({ id, label });
  }
  return toc;
}

function extractHubSections(html) {
  const sections = [];
  const regex = /<section class="city-section" id="([^"]+)">([\s\S]*?)(?=<section class="city-section"|<\/div>\s*<\/div>\s*<!-- @include:footer:start -->|<footer>)/g;
  let match;
  while ((match = regex.exec(html))) {
    const id = match[1];
    const block = match[2];
    const title = stripTags(matchOne(block, /<h2>(.*?)<\/h2>/s) || id);
    const cards = [];
    for (const cm of block.matchAll(/<a href="([^"]+)" class="pick-card">([\s\S]*?)<\/a>/g)) {
      const href = cm[1];
      const cardHtml = cm[2];
      const image = decodeBasicEntities(matchOne(cardHtml, /<img src="([^"]+)"/) || '');
      const imageAlt = stripTags(matchOne(cardHtml, /alt="([^"]+)"/) || '');
      const badge = stripTags(matchOne(cardHtml, /<span class="card-badge">(.*?)<\/span>/s) || '');
      const cardTitle = stripTags(matchOne(cardHtml, /<h3>(.*?)<\/h3>/s) || '');
      const description = stripTags(matchOne(cardHtml, /<p>(.*?)<\/p>/s) || '');
      const meta = [...cardHtml.matchAll(/<div class="card-meta">([\s\S]*?)<\/div>/g)]
        .flatMap((m) => [...m[1].matchAll(/<span>(.*?)<\/span>/g)].map((s) => stripTags(s[1])));
      const slug = href.replace(/^\/popular-picks\//, '').replace(/\/$/, '');
      cards.push({
        slug,
        href,
        title: cardTitle,
        description,
        badge,
        meta,
        image,
        imageAlt,
      });
    }
    sections.push({ id, title, cards });
  }
  return sections;
}

function buildHubJson(html, slug) {
  const jsonLd = extractJsonLdBlocks(html);
  const article = jsonLd.find((block) => block['@type'] === 'Article') || {};
  const faq = (jsonLd.find((block) => block['@type'] === 'FAQPage')?.mainEntity || []).map((item) => ({
    question: item.name,
    answer: item.acceptedAnswer?.text || '',
  }));
  const heroMetaHtml = [...html.matchAll(/<div class="hero-meta">([\s\S]*?)<\/div>/g)][0]?.[1] || '';
  const heroMeta = [...heroMetaHtml.matchAll(/<div[^>]*><strong>(.*?)<\/strong>\s*(.*?)<\/div>/g)].map((m) => `${stripTags(m[1])} ${stripTags(m[2])}`);
  const sections = extractHubSections(html);
  const toc = extractToc(html);
  const canonical = matchOne(html, /<link rel="canonical" href="([^"]+)">/i) || `https://tabiji.ai/popular-picks/${slug}/`;
  const canonicalPath = canonical.replace('https://tabiji.ai', '');
  const ogImage = matchOne(html, /<meta property="og:image" content="([^"]+)">/i);

  return {
    slug,
    pageType: 'popular-picks-hub',
    status: 'published',
    taxonomy: {
      scope: 'country-or-region-hub',
      label: stripTags(matchOne(html, /<h1[^>]*>(.*?)<\/h1>/i) || slug),
    },
    seo: {
      title: decodeBasicEntities(article.headline || matchOne(html, /<title>(.*?)<\/title>/i) || ''),
      h1: stripTags(matchOne(html, /<h1[^>]*>(.*?)<\/h1>/i) || ''),
      metaTitle: decodeBasicEntities(matchOne(html, /<title>(.*?)<\/title>/i) || ''),
      metaDescription: decodeBasicEntities(matchOne(html, /<meta name="description" content="([^"]+)">/i) || article.description || ''),
      canonicalPath,
      ogTitle: decodeBasicEntities(matchOne(html, /<meta property="og:title" content="([^"]+)">/i) || ''),
      ogDescription: decodeBasicEntities(matchOne(html, /<meta property="og:description" content="([^"]+)">/i) || ''),
      twitterTitle: decodeBasicEntities(matchOne(html, /<meta name="twitter:title" content="([^"]+)">/i) || ''),
      twitterDescription: decodeBasicEntities(matchOne(html, /<meta name="twitter:description" content="([^"]+)">/i) || ''),
      heroImage: ogImage || null,
      publishedTime: matchOne(html, /<meta property="article:published_time" content="([^"]+)">/i) || null,
      modifiedTime: matchOne(html, /<meta property="article:modified_time" content="([^"]+)">/i) || null,
      robots: decodeBasicEntities(matchOne(html, /<meta name="robots" content="([^"]+)">/i) || 'index, follow, max-image-preview:large'),
    },
    hero: {
      title: stripTags(matchOne(html, /<h1[^>]*>(.*?)<\/h1>/i) || ''),
      dek: stripTags(matchOne(html, /<section class="hero">[\s\S]*?<p>(.*?)<\/p>/s) || ''),
      backLink: matchOne(html, /<a href="([^"]+)" class="back-link">/),
      meta: heroMeta,
    },
    toc,
    sections,
    faq,
    provenance: {
      importedFromHtml: true,
      notes: 'Backfilled from an existing Popular Picks hub/index page.',
    },
    publishing: {
      outputPath: `popular-picks/${slug}/index.html`,
    },
  };
}

if (require.main === module) {
  const input = process.argv[2];
  const output = process.argv[3];
  if (!input || !output) {
    console.error('Usage: node generators/popular-picks/extract-hub.js <html-file> <output-json>');
    process.exit(1);
  }
  const html = fs.readFileSync(input, 'utf8');
  const slug = path.basename(path.dirname(input));
  const hubJson = buildHubJson(html, slug);
  writeText(output, `${JSON.stringify(hubJson, null, 2)}\n`);
  console.log(`Extracted hub ${slug} -> ${output}`);
}

module.exports = { buildHubJson, extractHubSections, extractToc, extractJsonLdBlocks };
