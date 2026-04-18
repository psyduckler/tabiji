/**
 * viator-service.js
 * Viator Partner API v2 client (affiliate mode)
 * 
 * API Base: https://www.viator.com/partner-api/v2
 * Auth:     Bearer <API_KEY> header
 * 
 * NOTE: API requires IP whitelisting. If you get 403/CAPTCHA, 
 *       add your server IP to the Viator Partner Dashboard.
 */

const API_KEY = () => {
  try {
    const { execSync } = require('child_process');
    return execSync('security find-generic-password -s "viator-affiliate-key" -w', { encoding: 'utf8' }).trim();
  } catch {
    return null;
  }
};

const BASE_URL = 'https://www.viator.com/partner-api/v2';

const headers = (extra = {}) => ({
  'Authorization': `Bearer ${API_KEY()}`,
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  ...extra,
});

/**
 * Search products by destination
 * @param {string[]} destinations - e.g. ["PARIS", "TOKYO"]
 * @param {object} opts - { currency, pageSize, sortOrder, tags, categoryIds }
 */
async function searchProducts(destinations = [], opts = {}) {
  const { currency = 'USD', pageSize = 10, sortOrder = 'RATING', tags = [], categoryIds = [] } = opts;
  
  const body = {
    destinations,
    currency,
    pageSize,
    sortOrder,
  };
  
  if (tags.length) body.tags = tags;
  if (categoryIds.length) body.categoryIds = categoryIds;
  
  const res = await fetch(`${BASE_URL}/products/search`, {
    method: 'POST',
    headers: headers(),
    body: JSON.stringify(body),
  });
  
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Viator search failed: ${res.status} — ${text.slice(0, 200)}`);
  }
  
  return res.json();
}

/**
 * Get full product details by code
 * @param {string} productCode - e.g. "2220PARI"
 */
async function getProduct(productCode) {
  const res = await fetch(`${BASE_URL}/products/${encodeURIComponent(productCode)}`, {
    method: 'GET',
    headers: headers(),
  });
  
  if (!res.ok) {
    throw new Error(`Viator get product failed: ${res.status}`);
  }
  
  return res.json();
}

/**
 * Bulk fetch products
 * @param {string[]} productCodes
 */
async function bulkProducts(productCodes) {
  const res = await fetch(`${BASE_URL}/products/bulk`, {
    method: 'POST',
    headers: headers(),
    body: JSON.stringify({ productCodes }),
  });
  
  if (!res.ok) throw new Error(`Viator bulk failed: ${res.status}`);
  return res.json();
}

/**
 * Free text search across catalogue
 * @param {string} query
 * @param {object} opts - { currency, pageSize, searchType, tags }
 */
async function freeTextSearch(query, opts = {}) {
  const { currency = 'USD', pageSize = 10, searchType = 'PRODUCTS', tags = [] } = opts;
  
  const res = await fetch(`${BASE_URL}/search/freetext`, {
    method: 'POST',
    headers: headers(),
    body: JSON.stringify({ query, currency, pageSize, searchType, ...(tags.length ? { tags } : {}) }),
  });
  
  if (!res.ok) throw new Error(`Viator freetext failed: ${res.status}`);
  return res.json();
}

/**
 * Get destinations list (geography taxonomy)
 */
async function getDestinations() {
  const res = await fetch(`${BASE_URL}/destinations`, {
    method: 'GET',
    headers: headers(),
  });
  
  if (!res.ok) throw new Error(`Viator destinations failed: ${res.status}`);
  return res.json();
}

/**
 * Check availability for a product
 * @param {string} productCode
 * @param {string} departureDate - ISO date YYYY-MM-DD
 */
async function checkAvailability(productCode, departureDate) {
  const res = await fetch(`${BASE_URL}/availability/check`, {
    method: 'POST',
    headers: headers(),
    body: JSON.stringify({ productCode, departureDate }),
  });
  
  if (!res.ok) throw new Error(`Viator availability failed: ${res.status}`);
  return res.json();
}

/**
 * Get product reviews
 * @param {string} productCode
 */
async function getReviews(productCode) {
  const res = await fetch(`${BASE_URL}/reviews/product`, {
    method: 'POST',
    headers: headers(),
    body: JSON.stringify({ productCode }),
  });
  
  if (!res.ok) throw new Error(`Viator reviews failed: ${res.status}`);
  return res.json();
}

/**
 * Generate affiliate redirect URL for a product.
 * The product object from the API often contains 'deeplinkUrl' or 'partnerRedirectUrl'.
 * If not, construct from the Viator product page.
 */
function getAffiliateUrl(product, partnerId = null) {
  if (product.partnerRedirectUrl) return product.partnerRedirectUrl;
  if (product.deeplinkUrl) return product.deeplinkUrl;
  // Fallback: construct from Viator product page
  const slug = product.urlSlug || product.code;
  return `https://www.viator.com/tours/${product.code}/${slug}?partnerId=${partnerId || 'VIATOR_PARTNER_ID'}`;
}

/**
 * Extract a clean tour card from a product object
 */
function toTourCard(product) {
  const primaryPhoto = product.photos?.[0] || product.heroImage || null;
  const pricing = product.priceFrom
    ? { amount: product.priceFrom, currency: product.currency || 'USD' }
    : null;
  
  return {
    code: product.code,
    title: product.title,
    shortDescription: product.shortDescription || product.description?.slice(0, 120) + '...',
    rating: product.rating,
    reviewCount: product.reviewCount || product.reviewsCount,
    duration: product.duration || product.durationText,
    photos: (product.photos || []).slice(0, 3),
    primaryPhoto,
    pricing,
    tag: product.flags?.join(' · ') || null,
    url: getAffiliateUrl(product),
    // extras
    category: product.category,
    destination: product.destination,
    cancellationPolicy: product.cancellationPolicy,
    highlights: product.highlights?.slice(0, 3),
  };
}

// ── Quick test ──────────────────────────────────────────────
if (require.main === module) {
  (async () => {
    console.log('Testing Viator API...');
    try {
      const key = API_KEY();
      if (!key) { console.log('❌ No API key found in keychain'); process.exit(1); }
      console.log('✅ API key found:', key.slice(0, 8) + '...');
      
      // Test search
      const result = await searchProducts(['PARIS'], { pageSize: 2 });
      console.log('✅ Search OK — total products:', result.total);
      if (result.products?.length) {
        console.log('First product:', JSON.stringify({
          code: result.products[0].code,
          title: result.products[0].title?.slice(0, 50),
          priceFrom: result.products[0].priceFrom,
        }, null, 2));
      }
    } catch (err) {
      console.log('❌ Error:', err.message);
    }
  })();
}

module.exports = {
  searchProducts,
  getProduct,
  bulkProducts,
  freeTextSearch,
  getDestinations,
  checkAvailability,
  getReviews,
  getAffiliateUrl,
  toTourCard,
};
