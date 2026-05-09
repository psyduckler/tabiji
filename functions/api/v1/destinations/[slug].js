const JSON_HEADERS = {
  'Content-Type': 'application/json; charset=utf-8',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Cache-Control': 'public, max-age=300, s-maxage=300',
};

let bundleCache = null;
let bundlePromise = null;

async function loadBundle(context) {
  if (bundleCache) return bundleCache;
  if (bundlePromise) return bundlePromise;

  const assetFetch = context.env?.ASSETS?.fetch?.bind(context.env.ASSETS)
    || context.fetch?.bind(context)
    || fetch;
  const url = new URL('/api/v1/destinations-full.json', context.request.url);

  bundlePromise = assetFetch(url.toString(), { headers: { Accept: 'application/json' } })
    .then(async (res) => {
      if (!res.ok) throw new Error(`destinations-full.json upstream ${res.status}`);
      const data = await res.json();
      bundleCache = data;
      return data;
    })
    .catch((err) => {
      bundlePromise = null;
      throw err;
    });

  return bundlePromise;
}

export function onRequestOptions() {
  return new Response(null, { headers: JSON_HEADERS });
}

export async function onRequestGet(context) {
  const { params } = context;
  let slug = (params?.slug || '').toString().toLowerCase();
  if (slug.endsWith('.json')) slug = slug.slice(0, -5);
  if (!slug) {
    return new Response(JSON.stringify({ error: 'slug required' }), {
      status: 400,
      headers: JSON_HEADERS,
    });
  }

  let bundle;
  try {
    bundle = await loadBundle(context);
  } catch (err) {
    return new Response(JSON.stringify({ error: 'destinations data unavailable' }), {
      status: 503,
      headers: JSON_HEADERS,
    });
  }

  const destination = bundle[slug];
  if (!destination) {
    return new Response(JSON.stringify({ error: 'Destination not found', slug }), {
      status: 404,
      headers: JSON_HEADERS,
    });
  }

  return new Response(JSON.stringify(destination), { headers: JSON_HEADERS });
}

// RFC 7231 §4.3.2: HEAD must return the same headers (and status) as GET, with
// no body. Without an explicit handler the Pages router returns 404 for HEAD,
// breaking monitors and CDN warmers that probe with HEAD before issuing GET.
export async function onRequestHead(context) {
  const response = await onRequestGet(context);
  return new Response(null, { status: response.status, headers: response.headers });
}
