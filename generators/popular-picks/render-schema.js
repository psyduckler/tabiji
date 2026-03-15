const { absoluteUrl } = require('./render-meta');

function renderJsonLd(obj) {
  return `<script type="application/ld+json">${JSON.stringify(obj, null, 2)}</script>`;
}

function renderSchema(data) {
  const canonical = absoluteUrl(data.seo.canonicalPath);
  const heroImage = absoluteUrl(data.seo.heroImage || '');

  const article = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: data.seo.h1,
    description: data.seo.metaDescription,
    author: { '@type': 'Organization', name: 'tabiji.ai', url: 'https://tabiji.ai' },
    publisher: { '@type': 'Organization', name: 'tabiji.ai', url: 'https://tabiji.ai' },
    datePublished: data.seo.publishedTime.slice(0, 10),
    dateModified: data.seo.modifiedTime.slice(0, 10),
    mainEntityOfPage: canonical,
    ...(heroImage ? { image: heroImage } : {})
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
      const resolvedType = (() => {
        const typeMap = { restaurant: 'Restaurant', cafe: 'CafeOrCoffeeShop', bar: 'BarOrPub', market: 'LocalBusiness' };
        return typeMap[pick.placeType] || 'LocalBusiness';
      })();
      return ({
      '@type': 'ListItem',
      position: pick.rank,
      item: {
        '@type': resolvedType,
        name: pick.name,
        ...(pick.cuisineTags?.[0] && foodTypes.has(resolvedType) ? { servesCuisine: pick.cuisineTags.join(' / ') } : {}),
        ...(pick.address ? { address: { '@type': 'PostalAddress', addressLocality: pick.address, addressCountry: data.taxonomy.countryCode || data.taxonomy.country } } : {}),
        ...(pick.priceRangeLocal ? { priceRange: pick.priceRangeLocal } : {}),
        ...(pick.googleMapsUrl ? { url: pick.googleMapsUrl } : {})
      }
    });
  })
  };

  const faq = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: data.faq.map((item) => ({
      '@type': 'Question',
      name: item.question,
      acceptedAnswer: { '@type': 'Answer', text: item.answer }
    }))
  };

  const touristTrip = {
    '@context': 'https://schema.org',
    '@type': 'TouristTrip',
    name: data.seo.h1,
    description: `in ${data.hero.eyebrow}, verified ${data.summary.lastVerifiedLabel || data.verification.lastVerified}.`,
    url: canonical,
    additionalProperty: [
      { '@type': 'PropertyValue', name: 'totalOptions', value: String(data.summary.totalOptions) },
      data.summary.bestBudgetOption ? { '@type': 'PropertyValue', name: 'bestBudgetOption', value: data.summary.bestBudgetOption } : null,
      data.summary.bestLuxuryOption ? { '@type': 'PropertyValue', name: 'bestLuxuryOption', value: data.summary.bestLuxuryOption } : null,
      data.summary.bestOverall ? { '@type': 'PropertyValue', name: 'bestOverall', value: data.summary.bestOverall } : null,
      { '@type': 'PropertyValue', name: 'topPick', value: data.summary.topPick },
      (data.summary.sourcesAnalyzed && !/Extracted/i.test(data.summary.sourcesAnalyzed)) ? { '@type': 'PropertyValue', name: 'sourcesAnalyzed', value: data.summary.sourcesAnalyzed } : null,
      { '@type': 'PropertyValue', name: 'lastVerified', value: data.verification.lastVerified }
    ].filter(Boolean)
  };

  return [article, itemList, faq, touristTrip].map(renderJsonLd).join('\n    ');
}

module.exports = { renderSchema };
