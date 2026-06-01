/* ============================================================
   tabiji.ai — A+ asset exporter (Claude Code / Node + Playwright)
   Renders every A+ module at EXACT KDP pixel dimensions, crisp
   (2× supersampled, no upscale — unlike the in-browser sandbox).

   Setup (once):
     npm install
     npx playwright install chromium

   Run:
     node generate.mjs                 # exports whatever templates/data.jsx holds
   Output: ./out/*.png

   Per book: stage that book's art in templates/assets/source/ and edit
   templates/data.jsx (IMG paths + the C copy object). See README.md.
   ============================================================ */
import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { chromium } from 'playwright';
import sharp from 'sharp';
import { stage } from './stage-art.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, 'templates');

// Optional per-book arg: `node generate.mjs <slug>` loads templates/data.<slug>.jsx
// (e.g. china, japan) into data.jsx and renders to out/<slug>/.
// No arg → render whatever data.jsx currently holds, to out/.
const slug = process.argv[2];
if (slug) {
  const src = path.join(ROOT, `data.${slug}.jsx`);
  if (!fs.existsSync(src)) { console.error(`No templates/data.${slug}.jsx found`); process.exit(1); }
  fs.copyFileSync(src, path.join(ROOT, 'data.jsx'));
  await stage(slug);  // fetch this book's comics + owl from the CDN if not already local
}
const OUT = path.join(__dirname, 'out', slug || '');
fs.mkdirSync(OUT, { recursive: true });

const MIME = { '.html': 'text/html', '.jsx': 'text/babel', '.js': 'text/javascript',
  '.png': 'image/png', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.css': 'text/css' };

// tiny static server so <script src="*.jsx"> + local art load over http (Babel needs http, not file://)
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  if (p === '/') p = '/export.html';
  const fp = path.join(ROOT, p);
  if (!fp.startsWith(ROOT) || !fs.existsSync(fp) || fs.statSync(fp).isDirectory()) { res.writeHead(404); return res.end('not found'); }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(fp)] || 'application/octet-stream', 'Access-Control-Allow-Origin': '*' });
  fs.createReadStream(fp).pipe(res);
});

// key → output file + exact KDP dimensions (h:0 = natural height, width-locked to 970)
const ASSETS = [
  { key: 'logo',   out: '01-company-logo-600x180.png',           w: 600, h: 180 },
  { key: 'header', out: '02-image-header-970x300.png',            w: 970, h: 300 },
  { key: 'q0',     out: '03a-four-image-ambush-300x300.png',      w: 300, h: 300 },
  { key: 'q1',     out: '03b-four-image-charm-300x300.png',       w: 300, h: 300 },
  { key: 'q2',     out: '03c-four-image-counterfeit-300x300.png', w: 300, h: 300 },
  { key: 'q3',     out: '03d-four-image-gouge-300x300.png',       w: 300, h: 300 },
  { key: 'ma',     out: '04-multiple-image-A-300x300.png',        w: 300, h: 300 },
  { key: 'inside', out: '04-multiple-image-A-FULL-970.png',       w: 970, h: 300 },
  { key: 'desc',   out: '05-product-description-970.png',         w: 970, h: 300 },
];

const PORT = 5188;
await new Promise((r) => server.listen(PORT, r));
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: 2 });

for (const a of ASSETS) {
  await page.goto(`http://localhost:${PORT}/export.html?key=${a.key}&scale=1`, { waitUntil: 'networkidle' });
  await page.waitForFunction(() => document.title === 'READY', { timeout: 20000 });
  const el = await page.$('#asset');
  const box = await el.boundingBox();
  const buf = await page.screenshot({ clip: { x: box.x, y: box.y, width: box.width, height: box.height }, omitBackground: true });
  const targetW = a.w;
  const targetH = a.h || Math.round(a.w * box.height / box.width);
  // flatten onto the cream page colour so KDP never sees transparency
  await sharp(buf).resize(targetW, targetH, { fit: 'fill' })
    .flatten({ background: '#FBF6EC' }).png().toFile(path.join(OUT, a.out));
  console.log('✓', a.out, `${targetW}×${targetH}`);
}

await browser.close();
server.close();
console.log('\nDone →', OUT);
