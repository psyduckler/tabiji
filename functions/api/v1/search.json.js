export async function onRequestGet(context) {
  const { request } = context;
  const url = new URL(request.url);
  const q = (url.searchParams.get('q') || '').trim().toLowerCase();
  const type = (url.searchParams.get('type') || '').trim().toLowerCase();
  const limitParam = Number.parseInt(url.searchParams.get('limit') || '20', 10);
  const limit = Number.isFinite(limitParam) ? Math.min(Math.max(limitParam, 1), 100) : 20;

  const indexUrl = new URL('/api/v1/search-index.json', url);
  // TODO: If search traffic grows, avoid fetching/parsing the full ~2MB index on every request.
  // Options: KV caching, edge cache warming, or splitting the index by type/prefix.
  const assetFetch = context.env?.ASSETS?.fetch?.bind(context.env.ASSETS)
    || context.fetch?.bind(context)
    || fetch;
  const upstream = await assetFetch(indexUrl.toString(), { headers: { 'Accept': 'application/json' } });
  if (!upstream.ok) {
    return new Response(JSON.stringify({ error: 'search index unavailable' }), {
      status: 503,
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
    });
  }

  const payload = await upstream.json();
  let items = Array.isArray(payload.items) ? payload.items : [];

  if (type) {
    items = items.filter((item) => item.type === type);
  }

  if (q) {
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
        ].join(' ').toLowerCase();
        const score = tokens.reduce((acc, token) => acc + (haystack.includes(token) ? 1 : 0), 0);
        return { item, score };
      })
      .filter(({ score }) => score > 0)
      .sort((a, b) => b.score - a.score || a.item.title.localeCompare(b.item.title))
      .map(({ item }) => item);
  }

  const result = {
    query: q,
    type: type || null,
    count: items.length,
    items: items.slice(0, limit),
  };

  return new Response(JSON.stringify(result, null, 2), {
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'public, max-age=300',
    },
  });
}
