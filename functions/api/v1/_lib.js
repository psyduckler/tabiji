const JSON_HEADERS = {
  'Content-Type': 'application/json; charset=utf-8',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function json(data, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { ...JSON_HEADERS, ...extraHeaders },
  });
}

export function handleOptions() {
  return new Response(null, { headers: JSON_HEADERS });
}

async function fetchAssetJson(context, path) {
  const url = new URL(path, context.request.url);
  const response = await context.env.ASSETS.fetch(new Request(url.toString(), { method: 'GET' }));
  if (!response.ok) {
    throw new Error(`Failed to load asset ${path}: ${response.status}`);
  }
  return response.json();
}

export async function loadCatalog(context) {
  return fetchAssetJson(context, '/api/v1/catalog.json');
}

export async function readInput(context) {
  const method = context.request.method.toUpperCase();
  if (method === 'GET') {
    const url = new URL(context.request.url);
    const data = {};
    for (const [key, value] of url.searchParams.entries()) {
      if (value.includes(',')) {
        data[key] = value.split(',').map((item) => item.trim()).filter(Boolean);
      } else if (value === 'true') {
        data[key] = true;
      } else if (value === 'false') {
        data[key] = false;
      } else {
        data[key] = value;
      }
    }
    return data;
  }

  if (method === 'POST') {
    return context.request.json().catch(() => ({}));
  }

  return {};
}

export function normalizeList(value) {
  if (!value) return [];
  if (Array.isArray(value)) return value.flatMap((item) => normalizeList(item));
  return String(value)
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);
}

export function tokenize(value) {
  return String(value || '')
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .split(/\s+/)
    .filter(Boolean);
}

function includesNormalized(haystack, needle) {
  return String(haystack || '').toLowerCase().includes(String(needle || '').toLowerCase());
}

function listIntersects(values, wanted) {
  if (!wanted.length) return true;
  const lowerSet = new Set((values || []).map((item) => String(item).toLowerCase()));
  return wanted.some((item) => lowerSet.has(String(item).toLowerCase()));
}

export function applyFilters(items, filters = {}) {
  const entityTypes = normalizeList(filters.entity_types || filters.entityType);
  const city = filters.city || filters.location;
  const category = filters.category;
  const tags = normalizeList(filters.tags || filters.good_for || filters.goodFor);
  const budget = normalizeList(filters.budget || filters.price_level || filters.priceLevel);
  const openNow = typeof filters.open_now === 'boolean' ? filters.open_now : filters.openNow;

  return items.filter((item) => {
    if (entityTypes.length && !entityTypes.includes(item.entityType)) return false;
    if (city && !includesNormalized(item.city, city) && !includesNormalized(item.locationLabel, city)) return false;
    if (category && !includesNormalized(item.category, category)) return false;
    if (tags.length && !listIntersects(item.tags, tags) && !listIntersects(item.goodFor, tags)) return false;
    if (budget.length && !budget.includes(item.priceLevel)) return false;
    if (typeof openNow === 'boolean' && item.openNow !== openNow) return false;
    return true;
  });
}

export function scoreSearch(item, query, context = {}) {
  const queryTokens = tokenize(query);
  const haystack = tokenize([
    item.name,
    item.title,
    item.description,
    item.city,
    item.category,
    item.locationLabel,
    ...(item.tags || []),
    ...(item.goodFor || []),
    ...(item.highlights || []),
  ].join(' '));

  const haystackSet = new Set(haystack);
  let score = 0;
  const matchedOn = [];

  for (const token of queryTokens) {
    if (haystackSet.has(token)) {
      score += 6;
      matchedOn.push(`keyword:${token}`);
    }
  }

  if (context.city && includesNormalized(item.city, context.city)) {
    score += 8;
    matchedOn.push(`city:${item.city}`);
  }

  if (context.entityTypes?.length && context.entityTypes.includes(item.entityType)) {
    score += 4;
    matchedOn.push(`entity_type:${item.entityType}`);
  }

  if (context.tags?.length) {
    const tagMatches = context.tags.filter((tag) => listIntersects(item.tags, [tag]) || listIntersects(item.goodFor, [tag]));
    if (tagMatches.length) {
      score += tagMatches.length * 5;
      matchedOn.push(...tagMatches.map((tag) => `tag:${tag}`));
    }
  }

  if (item.openNow) {
    score += 1;
  }

  if (item.ratingNormalized) {
    score += item.ratingNormalized * 3;
  }

  if (item.editorialSignal) {
    score += item.editorialSignal * 2;
  }

  return { score, matchedOn: [...new Set(matchedOn)] };
}

export function buildResult(item, extra = {}) {
  return {
    id: item.id,
    entityType: item.entityType,
    name: item.name,
    title: item.title,
    city: item.city,
    category: item.category,
    url: item.url,
    description: item.description,
    tags: item.tags,
    goodFor: item.goodFor,
    priceLevel: item.priceLevel,
    openNow: item.openNow,
    location: item.locationLabel ? { label: item.locationLabel, city: item.city } : { city: item.city },
    source: item.source,
    freshness: item.freshness,
    provenance: item.provenance,
    ...extra,
  };
}

export function rankRecommendations(items, input = {}) {
  const intent = String(input.intent || '').toLowerCase();
  const preferences = input.preferences || {};
  const travelerType = input.party?.traveler_type || input.traveler_type || input.travelerType;
  const desiredTags = normalizeList(preferences.tags || preferences.atmosphere || preferences.want);
  const avoidTags = normalizeList(preferences.avoid);

  return items
    .map((item) => {
      let score = 0;
      const why = [];
      const tradeoffs = [];

      score += (item.ratingNormalized || 0) * 30;
      score += (item.editorialSignal || 0) * 20;
      score += (item.freshness?.confidenceScore || 0) * 15;

      if (travelerType && listIntersects(item.goodFor, [travelerType])) {
        score += 18;
        why.push(`Strong fit for ${travelerType.replace(/_/g, ' ')}`);
      }

      if (desiredTags.length) {
        const matched = desiredTags.filter((tag) => listIntersects(item.tags, [tag]) || listIntersects(item.goodFor, [tag]));
        if (matched.length) {
          score += matched.length * 12;
          why.push(`Matches ${matched.join(', ')}`);
        }
      }

      if (avoidTags.length) {
        const matchedAvoid = avoidTags.filter((tag) => listIntersects(item.tags, [tag]));
        if (matchedAvoid.length) {
          score -= matchedAvoid.length * 15;
          tradeoffs.push(`Includes ${matchedAvoid.join(', ')}`);
        }
      }

      if (intent) {
        if (intent.includes('dinner')) {
          if (listIntersects(item.tags, ['dinner', 'restaurant', 'izakaya', 'tapas', 'romantic', 'food', 'nightlife'])) {
            score += 16;
            why.push('Good fit for dinner intent');
          } else {
            score -= 20;
            tradeoffs.push('Weak dinner fit');
          }
          if (listIntersects(item.tags, ['breakfast', 'remote_work'])) {
            score -= 10;
            tradeoffs.push('Leans more daytime than dinner');
          }
          if (!listIntersects(item.tags, ['food', 'nightlife']) && !/restaurant|bar|izakaya|tapas|steak|ramen|pizza|wine|cocktail/i.test(`${item.category} ${item.title}`)) {
            score -= 18;
            tradeoffs.push('Not a food-first category');
          }
        }
        if (intent.includes('coffee') || intent.includes('work')) {
          if (listIntersects(item.tags, ['cafe', 'coffee', 'wifi', 'remote_work'])) {
            score += 14;
            why.push('Good fit for coffee / work intent');
          }
          if (listIntersects(item.tags, ['nightlife'])) {
            score -= 6;
          }
        }
        if (intent.includes('stay') || intent.includes('neighborhood')) {
          if (item.entityType === 'destination') {
            score += 10;
            why.push('Destination-level fit for stay / neighborhood planning');
          }
        }
      }

      if (item.openNow) {
        score += 4;
        why.push('Operationally available now');
      } else if (item.entityType === 'place') {
        tradeoffs.push('May not be open right now');
      }

      if (item.priceLevel) {
        why.push(`Budget band ${item.priceLevel}`);
      }

      return { item, score, why: [...new Set(why)].slice(0, 4), tradeoffs: [...new Set(tradeoffs)].slice(0, 3) };
    })
    .sort((a, b) => b.score - a.score);
}

export { json };
