const HEADERS = {
  'Content-Type': 'text/plain; charset=utf-8',
  'Cache-Control': 'no-store',
  'X-Robots-Tag': 'noindex, nofollow',
  'X-Content-Type-Options': 'nosniff',
};

export function onRequest() {
  return new Response('Gone\n', {
    status: 410,
    headers: HEADERS,
  });
}
