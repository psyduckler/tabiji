const JSON_HEADERS = {
  'Content-Type': 'application/json; charset=utf-8',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
  'Access-Control-Allow-Headers': 'Accept, Content-Type',
  'Cache-Control': 'no-store',
  'X-Robots-Tag': 'noindex, nofollow',
  'X-Content-Type-Options': 'nosniff',
};

const PAYLOAD = JSON.stringify({
  error: {
    code: 'gone',
    message: 'This retired API resource is no longer available.',
    status: 410,
    resource: 'catalog-places',
  },
}, null, 2);

export function onRequest(context) {
  if (context.request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: JSON_HEADERS });
  }
  return new Response(context.request.method === 'HEAD' ? null : PAYLOAD, {
    status: 410,
    headers: JSON_HEADERS,
  });
}
