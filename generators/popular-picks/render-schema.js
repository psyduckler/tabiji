const { absoluteUrl } = require('./render-meta');

const AUTHOR_PERSON = {
  '@type': 'Person',
  name: 'Bernard Huang',
  jobTitle: 'Editor',
  url: 'https://tabiji.ai/about/',
  image: 'https://img.tabiji.ai/authors/bernard-huang.jpg',
  worksFor: { '@type': 'Organization', name: 'tabiji.ai', url: 'https://tabiji.ai' },
};

const PUBLISHER_ORG = { '@type': 'Organization', name: 'tabiji.ai', url: 'https://tabiji.ai' };

function isLikelyPriceRange(value = '') {
  return /[$€£¥₩฿₵₫₹]|\bfree\b|\d+\s*(?:-|–|to)\s*[$€£¥₩฿₵₫₹]?\d+/i.test(String(value));
}

const NON_CUISINE_PATTERNS = /^(local favorite|hidden gem|traditional|luxury|classic|premium|mid-range|budget|boutique|historic|legendary|iconic|neighborhood gem|upscale|fine dining|budget pick|budget-friendly|local gem|advanced|intermediate|beginner|landmark|modern|restaurant|night market|street stall|hawker centre|cocktail bar|beer bar|brewpub|natural wine|mezcal bar|specialty coffee|\d+(st|nd|rd|th)\s+floor|[🏖🐠🐢🚢🌱🐙🦈🪸🚤🗿])/i;

function isLikelyCuisine(tag = '') {
  return tag.trim().length > 0 && !NON_CUISINE_PATTERNS.test(tag.trim());
}

function renderJsonLd(obj) {
  return `<script type="application/ld+json">${JSON.stringify(obj, null, 2)}</script>`;
}

function buildBreadcrumb(data) {
  const canonical = absoluteUrl(data.seo.canonicalPath);
  const country = data.taxonomy?.country || '';
  const items = [
    { name: 'Home', url: 'https://tabiji.ai/' },
    { name: 'Popular Picks', url: 'https://tabiji.ai/popular-picks/' },
  ];
  if (country) {
    items.push({ name: country, url: `https://tabiji.ai/popular-picks/${country.toLowerCase().replace(/\s+/g, '-')}/` });
  }
  items.push({ name: data.seo.h1, url: canonical });
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: item.url,
    })),
  };
}

function renderSchema(data) {
  const canonical = absoluteUrl(data.seo.canonicalPath);
  const heroImage = absoluteUrl(data.seo.heroImage || '');
  const publishedDate = typeof data?.seo?.publishedTime === 'string' ? data.seo.publishedTime.slice(0, 10) : undefined;
  const modifiedDate = typeof data?.seo?.modifiedTime === 'string' ? data.seo.modifiedTime.slice(0, 10) : undefined;

  const article = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: data.seo.h1,
    description: data.seo.metaDescription,
    author: AUTHOR_PERSON,
    publisher: PUBLISHER_ORG,
    ...(publishedDate ? { datePublished: publishedDate } : {}),
    ...(modifiedDate ? { dateModified: modifiedDate } : {}),
    mainEntityOfPage: canonical,
    ...(heroImage ? { image: heroImage } : {}),
    speakable: {
      '@type': 'SpeakableSpecification',
      cssSelector: ['.hero h1', '.hero .subtitle', '.quick-answer-section', '.faq-section'],
    },
  };

  const itemList = {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    name: data.seo.h1,
    description: data.seo.metaDescription,
    url: canonical,
    numberOfItems: data.picks.length,
    itemListElement: data.picks.map((pick) => {
      const foodTypes = new Set(['Restaurant', 'CafeOrCoffeeShop', 'BarOrPub']);
      const typeMap = { restaurant: 'Restaurant', cafe: 'CafeOrCoffeeShop', bar: 'BarOrPub', market: 'LocalBusiness' };
      const resolvedType = typeMap[pick.placeType] || 'LocalBusiness';
      const cuisines = (pick.tags || []).filter(isLikelyCuisine);
      return {
        '@type': 'ListItem',
        position: pick.rank,
        item: {
          '@type': resolvedType,
          name: pick.name,
          ...(foodTypes.has(resolvedType) && cuisines.length ? { servesCuisine: cuisines.join(' / ') } : {}),
          ...(pick.address
            ? {
                address: {
                  '@type': 'PostalAddress',
                  addressLocality: pick.address,
                  addressCountry: data.taxonomy.countryCode || data.taxonomy.country,
                },
              }
            : {}),
          ...(pick.priceRangeLocal && isLikelyPriceRange(pick.priceRangeLocal) ? { priceRange: pick.priceRangeLocal } : {}),
          ...(typeof pick.googleRating === 'number' && typeof pick.reviewCount === 'number'
            ? {
                aggregateRating: {
                  '@type': 'AggregateRating',
                  ratingValue: pick.googleRating,
                  reviewCount: pick.reviewCount,
                  bestRating: 5,
                },
              }
            : {}),
          ...(typeof pick.lat === 'number' && typeof pick.lng === 'number'
            ? { geo: { '@type': 'GeoCoordinates', latitude: pick.lat, longitude: pick.lng } }
            : {}),
          ...(pick.googleMapsUrl ? { hasMap: pick.googleMapsUrl } : {}),
          ...(pick.website ? { url: pick.website } : pick.googleMapsUrl ? { url: pick.googleMapsUrl } : {}),
        },
      };
    }),
  };

  const faq = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: data.faq.map((item) => ({
      '@type': 'Question',
      name: item.question,
      acceptedAnswer: { '@type': 'Answer', text: item.answer },
    })),
  };

  const breadcrumb = buildBreadcrumb(data);

  return [article, itemList, faq, breadcrumb].map(renderJsonLd).join('\n    ');
}

module.exports = { renderSchema, AUTHOR_PERSON, PUBLISHER_ORG };
