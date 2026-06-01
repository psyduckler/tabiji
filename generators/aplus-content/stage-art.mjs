/* ============================================================
   Stage A+ comic art + owl from img.tabiji.ai → templates/assets/source/.
   Media is NOT committed (repo policy: binaries live on Cloudflare R2),
   so the build fetches what it needs on demand. Already-present files are
   left untouched. generate.mjs calls stage(slug) automatically; you can also
   run it standalone:  node stage-art.mjs <slug>
   ============================================================ */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SRC = path.join(HERE, 'templates', 'assets', 'source');
const BASE = 'https://img.tabiji.ai';

// Local filename → CDN path. Owl is the shared brand mark; one map per book.
export const OWL = '/tabiji-owl-logo.png';
export const ART = {
  china: {
    'beijing-airport.webp':    '/scams/beijing/scam-1.webp',
    'beijing-artstudent.webp': '/scams/beijing/scam-2.webp',
    'shanghai-nanjing.webp':   '/scams/shanghai/scam-1.webp',
    'xian-terracotta.webp':    '/scams/xian/scam-1.webp',
    'xian-muslimquarter.webp': '/scams/xian/scam-2.webp',
  },
  japan: {
    'tokyo-tout.webp':      '/scams/tokyo/scam-2.webp?v=3',
    'tokyo-bottakuri.webp': '/scams/tokyo/scam-1.webp?v=3',
    'tokyo-monk.webp':      '/scams/tokyo/scam-7.webp?v=2',
    'kyoto-otoshi.webp':    '/scams/kyoto/scam-3.webp?v=2',
    'kyoto-rickshaw.webp':  '/scams/kyoto/scam-4.webp?v=2',
    'nara-deer.webp':       '/scams/nara/scam-1.webp?v=2',
  },
};

async function fetchTo(url, dest) {
  if (fs.existsSync(dest) && fs.statSync(dest).size > 0) return false;  // re-fetch 0-byte/partial files
  const r = await fetch(url, { headers: { 'User-Agent': 'tabiji-aplus' }, signal: AbortSignal.timeout(30000) });
  if (!r.ok) throw new Error(`${r.status} fetching ${url}`);
  fs.writeFileSync(dest, Buffer.from(await r.arrayBuffer()));
  return true;
}

export async function stage(slug) {
  fs.mkdirSync(SRC, { recursive: true });
  const map = ART[slug];
  if (!map) throw new Error(`no art map for "${slug}" — add one in stage-art.mjs`);
  let n = 0;
  if (await fetchTo(BASE + OWL, path.join(SRC, 'owl.png'))) n++;
  for (const [name, p] of Object.entries(map)) {
    if (await fetchTo(BASE + p, path.join(SRC, name))) n++;
  }
  return n;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const slug = process.argv[2];
  if (!slug) { console.error('usage: node stage-art.mjs <slug>'); process.exit(1); }
  stage(slug).then((n) => console.log(`✓ staged ${n} new file(s) for ${slug}`));
}
