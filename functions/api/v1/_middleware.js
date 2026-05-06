const JSON_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
  'Access-Control-Allow-Headers': 'Accept, Content-Type',
  'X-Content-Type-Options': 'nosniff',
};

function jsonError(status, code, message, extra = {}) {
  return new Response(JSON.stringify({ error: { code, message, status, ...extra } }, null, 2), {
    status,
    headers: {
      ...JSON_HEADERS,
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
    },
  });
}

function apiPath(request) {
  return new URL(request.url).pathname;
}

function jsonResource(pathname) {
  return pathname.startsWith('/api/v1/') && pathname.endsWith('.json');
}

function inferResource(pathname) {
  const parts = pathname.replace(/^\/api\/v1\//, '').replace(/\.json$/, '').split('/').filter(Boolean);
  return {
    resource: parts[0] || 'api',
    id: parts.slice(1).join('/') || null,
  };
}

export async function onRequest(context) {
  const { request, next } = context;
  const pathname = apiPath(request);

  if (!jsonResource(pathname)) {
    return next();
  }

  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: JSON_HEADERS });
  }

  if (!['GET', 'HEAD'].includes(request.method)) {
    return jsonError(405, 'method_not_allowed', `${request.method} is not allowed for JSON API resources.`, inferResource(pathname));
  }

  const response = await next();
  const headers = new Headers(response.headers);
  for (const [key, value] of Object.entries(JSON_HEADERS)) {
    headers.set(key, value);
  }

  if (response.status === 404) {
    return jsonError(404, 'not_found', 'JSON API resource not found.', inferResource(pathname));
  }

  if (response.status === 400) {
    headers.set('Content-Type', headers.get('Content-Type') || 'application/json; charset=utf-8');
    headers.set('Cache-Control', 'no-store');
  }

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}
