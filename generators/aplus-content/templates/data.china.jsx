/* ============================================================
   tabiji.ai — China A+ Content · DATA  (Set A "Field Guide", terracotta)
   Real CDN art (staged locally) + locked, A+-compliant copy.
   NOTE: export.jsx reads legacy slot keys — IMG.beijing2 = HEADER hero comic,
   IMG.shanghai1 = INSIDE/Module-A comic. Quad tiles use t1..t4 via C.quad.
   ============================================================ */

const IMG = {
  owl:     'assets/source/owl.png',
  owlFly:  'assets/source/owl.png',
  beijing2:  'assets/source/beijing-artstudent.webp', // HERO slot → Art-student gallery (cover scene)
  shanghai1: 'assets/source/shanghai-nanjing.webp',   // INSIDE slot → Nanjing-Rd tea house
  t1:      'assets/source/beijing-airport.webp',      // tile · THE AMBUSH
  t2:      'assets/source/shanghai-nanjing.webp',     // tile · THE CHARM
  t3:      'assets/source/xian-terracotta.webp',      // tile · THE COUNTERFEIT
  t4:      'assets/source/xian-muslimquarter.webp',   // tile · THE GOUGE
  cover:   'assets/source/beijing-artstudent.webp',
};

// ---- Locked copy (A+ compliant: no price / rating / refund / "free") ----
const C = {
  brand: { tagline: 'Travel safety, country by country.', series: 'TRAVEL SAFETY SERIES', vol: 'VOL. 7', country: 'CHINA', dom: 'tabiji.ai', stamp3: 'VOL 7' },
  stat:  { scams: '98', cities: '16',
           sources: ['China Daily', 'Global Times', 'Xinhua', 'Shanghai Daily', 'PSB · 110'],
           sourcesLine: 'CHINESE PRESS · REDDIT REPORTS · REAL TRAVELER STORIES · PSB 110' },

  hero: {
    authority:   { kicker: '98 DOCUMENTED SCAMS · 16 MAINLAND CITIES',
                   head: ['Sourced from the', 'Chinese press, Reddit', 'threads & real travelers.'],
                   sub: 'China Daily · Global Times · Xinhua · Shanghai Daily · Reddit reports · Public Security Bureau (110).' },
    loss:        { kicker: 'BEIJING · WANGFUJING',
                   head: ['Don’t lose ¥2,000', 'to a “student', 'gallery” gift.'],
                   sub: '98 documented scams across 16 mainland-Chinese cities — and the moves that stop every one.' },
    provocative: { kicker: 'CASE FILE · CHINA · 2026',
                   head: ['What the', 'guidebooks won’t', 'tell you.'],
                   sub: 'The exact scripts, the red flags, and the Mandarin phrases that shut every scam down.' },
  },

  quadHead: { A: 'Four ways China separates tourists from their money.',
              B: 'Same four moves. Every city.',
              C: 'Four documented patterns — ninety-eight in the book.' },

  quad: [
    { n: '01', tag: 'THE AMBUSH', city: 'BEIJING', title: 'Airport Black-Taxi Switch',
      tl: 'A ¥120–180 ride to your hotel ticks up to ¥600 — “night rate, traffic surcharge, special road.”',
      loss: '¥600', img: IMG.t1 },
    { n: '02', tag: 'THE CHARM', city: 'SHANGHAI', title: 'The Nanjing-Road Tea House',
      tl: 'Four small cups in a 12-seat room — then a ¥3,000–10,000 bill for two. Your new friend vanishes.',
      loss: '¥10,000', img: IMG.t2 },
    { n: '03', tag: 'THE COUNTERFEIT', city: 'XI’AN', title: 'Fake Terracotta Army',
      tl: 'Mass-produced replicas 35 km short of the real pits — and a ¥150 “tour” that’s four shopping stops.',
      loss: '¥150', img: IMG.t3 },
    { n: '04', tag: 'THE GOUGE', city: 'XI’AN', title: 'The “Small Slice” Cake',
      tl: 'A “thin slice” of Xinjiang cake hits the scale at 200 g — a ¥2,400 snack.',
      loss: '¥2,400', img: IMG.t4 },
  ],

  inside: {
    head: 'Every scam, fully worked out — and the phrase that ends it.',
    img: IMG.shanghai1,
    caption: 'SHANGHAI · NANJING-RD TEA HOUSE',
    items: [
      ['Six universal red-flags', 'Learn them once — spot all 98.'],
      ['Exact scripts + RMB amounts', 'City by city, scam by scam.'],
      ['A comic for every scam', '98 watercolor strips, like these.'],
      ['Mandarin exit-phrase card', 'Pinyin + characters — screenshot it.'],
      ['Post-scam recovery playbook', 'First 15 minutes, first hour, first day.'],
      ['Emergency contacts', '110 PSB · 12301 tourist · 12315 consumer.'],
    ],
    phrases: [
      ['bù yào, xièxie', '不要，谢谢', 'No thanks.'],
      ['qǐng dǎ biǎo', '请打表', 'Use the meter.'],
      ['wǒ yào bàojǐng', '我要报警', 'Calling the police.'],
    ],
  },

  desc: {
    head: { A: 'Read it on the flight over.', B: 'Read it on the flight over.', C: 'The whole file, before you fly.' },
    body: [
      'China: Tourist Scams is Volume 7 of the tabiji.ai Travel Safety Series. Every scam is documented against Chinese and China-facing press — China Daily, Global Times, Xinhua, Shanghai Daily — plus Public Security Bureau (110), tourist-help (12301) and market-regulator (12315) bulletins, and real traveler reports.',
      '98 specific scams across Beijing, Shanghai, Xi’an, Chengdu and 12 more mainland cities. The exact scripts, the red flags that give them away, and the Mandarin phrases that shut them down — with Pinyin and simplified characters you can show on your phone.',
      'Scams evolve, so the book is re-researched and updated every year — when a new edition ships, it appears in your Kindle library. Built for the traveler who wants to move through China relaxed, not braced.',
    ],
    badges: ['CHINESE-PRESS SOURCED', 'UPDATED ANNUALLY', '16 MAINLAND CITIES', '98 DOCUMENTED SCAMS'],
    price: 'VOL. 7 · ~260 PAGES',
  },
};

const SERIF = '"Newsreader", Georgia, "Times New Roman", serif';
const SANS  = '"Public Sans", system-ui, -apple-system, sans-serif';
const COND  = '"Saira Condensed", "Public Sans", sans-serif';
const MONO  = '"Spline Sans Mono", ui-monospace, monospace';

const THEMES = {
  A: {
    key: 'A', name: 'Field Guide', blurb: 'Terracotta editorial · authority voice · framed comics',
    dark: false,
    pageBg: '#F3EADB', surface: '#FBF6EC', surfaceAlt: '#F2E6D4',
    ink: '#2A2117', sub: '#6E5E49',
    onPage: '#7A6A52', onPageSub: '#9A8B72',
    terra: '#A8472A', terraDeep: '#7C3019', wash: '#E7D4BF',
    line: '#DAC8AD', lineSoft: '#E7DAC3',
    serif: SERIF, sans: SANS, mono: MONO, cond: COND,
  },
};

window.TABIJI = { IMG, C, THEMES };
