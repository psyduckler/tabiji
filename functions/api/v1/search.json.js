const JSON_HEADERS = {
  'Content-Type': 'application/json; charset=utf-8',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
  'Access-Control-Allow-Headers': 'Accept, Content-Type',
  'X-Content-Type-Options': 'nosniff',
};

const SEARCH_TYPES = new Set(['destination', 'pick', 'itinerary', 'compare', 'country', 'safety', 'alert', 'scam']);
const TYPE_ALIASES = new Map([['comparison', 'compare'], ['comparisons', 'compare']]);

function jsonResponse(payload, status = 200, cacheControl = 'public, max-age=300') {
  return new Response(JSON.stringify(payload, null, 2), {
    status,
    headers: {
      ...JSON_HEADERS,
      'Cache-Control': cacheControl,
    },
  });
}

function errorResponse(status, code, message, extra = {}) {
  return jsonResponse({ error: { code, message, status, ...extra } }, status, 'no-store');
}

function normalizeQuery(value) {
  return (value || '')
    .trim()
    .toLowerCase()
    .replace(/[-_]+/g, ' ')
    .replace(/\s+/g, ' ');
}

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: JSON_HEADERS });
}

export async function onRequestPost() {
  return errorResponse(405, 'method_not_allowed', 'Use GET /api/v1/search.json with q, type, and limit query parameters.');
}

// RFC 7231 §4.3.2: HEAD must return the same headers as GET. Without this,
// HEAD /api/v1/search.json?q=… falls through to a static-asset 404, even
// though the GET handler responds 200 for the same URL.
export async function onRequestHead(context) {
  const response = await onRequestGet(context);
  return new Response(null, { status: response.status, headers: response.headers });
}

export async function onRequestGet(context) {
  const { request } = context;
  const url = new URL(request.url);
  const rawQ = url.searchParams.get('q');
  const q = normalizeQuery(rawQ);
  if (!q) {
    return errorResponse(400, 'invalid_query', 'Search query parameter `q` is required and must be non-empty.', { parameter: 'q' });
  }

  let type = (url.searchParams.get('type') || '').trim().toLowerCase();
  type = TYPE_ALIASES.get(type) || type;
  if (type && !SEARCH_TYPES.has(type)) {
    return errorResponse(400, 'invalid_type', `Search type must be one of: ${Array.from(SEARCH_TYPES).join(', ')}.`, { parameter: 'type', value: type });
  }

  const rawLimit = url.searchParams.get('limit') || '20';
  if (!/^\d+$/.test(rawLimit)) {
    return errorResponse(400, 'invalid_limit', 'Search limit must be an integer from 1 to 100.', { parameter: 'limit', value: rawLimit });
  }
  const limit = Number.parseInt(rawLimit, 10);
  if (limit < 1 || limit > 100) {
    return errorResponse(400, 'invalid_limit', 'Search limit must be an integer from 1 to 100.', { parameter: 'limit', value: rawLimit });
  }

  const indexUrl = new URL('/api/v1/search-index.json', url);
  // TODO: If search traffic grows, avoid fetching/parsing the full ~2MB index on every request.
  // Options: KV caching, edge cache warming, or splitting the index by type/prefix.
  const assetFetch = context.env?.ASSETS?.fetch?.bind(context.env.ASSETS)
    || context.fetch?.bind(context)
    || fetch;
  const upstream = await assetFetch(indexUrl.toString(), { headers: { 'Accept': 'application/json' } });
  if (!upstream.ok) {
    return errorResponse(503, 'search_index_unavailable', 'Search index unavailable.');
  }

  const payload = await upstream.json();
  let items = Array.isArray(payload.items) ? payload.items : [];

  if (type) {
    items = items.filter((item) => item.type === type);
  }

  const tokens = q.split(/\s+/).filter(Boolean);
  items = items
    .map((item) => {
      const haystack = [
        item.title,
        item.subtitle,
        item.city,
        item.destination,
        item.destination1,
        item.destination2,
        ...(Array.isArray(item.tokens) ? item.tokens : []),
      ].join(' ').toLowerCase().replace(/[-_]+/g, ' ');
      const score = tokens.reduce((acc, token) => acc + (haystack.includes(token) ? 1 : 0), 0);
      return { item, score };
    })
    .filter(({ score }) => score > 0)
    .sort((a, b) => b.score - a.score || a.item.title.localeCompare(b.item.title))
    .map(({ item }) => item);

  const result = {
    query: q,
    type: type || null,
    count: items.length,
    items: items.slice(0, limit),
  };

  return jsonResponse(result);
}
