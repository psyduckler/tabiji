/* ============================================================
   tabiji.ai — Japan A+ Content · DATA  (Set A "Field Guide", indigo)
   Real CDN art (staged locally) + locked, A+-compliant copy.
   NOTE: export.jsx reads legacy slot keys — IMG.beijing2 = HEADER hero comic,
   IMG.shanghai1 = INSIDE/Module-A comic. Quad tiles use t1..t4 via C.quad.
   ============================================================ */

const IMG = {
  owl:     'assets/source/owl.png',
  owlFly:  'assets/source/owl.png',
  beijing2:  'assets/source/tokyo-tout.webp',     // HERO slot  → Kabukicho street tout
  shanghai1: 'assets/source/kyoto-rickshaw.webp', // INSIDE slot → Higashiyama rickshaw
  t1:      'assets/source/tokyo-bottakuri.webp',  // tile · THE TRAP
  t2:      'assets/source/tokyo-monk.webp',       // tile · THE BLESSING
  t3:      'assets/source/kyoto-otoshi.webp',     // tile · THE SURPRISE
  t4:      'assets/source/nara-deer.webp',        // tile · THE AMBUSH
  cover:   'assets/source/tokyo-tout.webp',
};

const C = {
  brand: { tagline: 'Travel safety, country by country.', series: 'TRAVEL SAFETY SERIES', vol: '', country: 'JAPAN', dom: 'tabiji.ai', stamp3: '60 SCAMS' },
  stat:  { scams: '60', cities: '9',
           sources: ['TMPD', 'NCAC 188', 'r/JapanTravel', 'Nara Pref. Gov.', 'local police'],
           sourcesLine: 'TOKYO POLICE · CONSUMER AFFAIRS CENTER 188 · r/JAPANTRAVEL · LOCAL NEWS' },

  hero: {
    authority:   { kicker: '60 DOCUMENTED SCAMS · 9 CITIES',
                   head: ['Sourced from Japanese', 'police records, r/JapanTravel', '& real traveler reports.'],
                   sub: 'Tokyo Metropolitan Police · National Consumer Affairs Center (188) · r/JapanTravel · verified local news.' },
    loss:        { kicker: 'TOKYO · KABUKICHO',
                   head: ['Don’t lose ¥130,000', 'to a “¥500 beer”', 'bar tout.'],
                   sub: '60 documented scams across 9 Japanese cities — and the moves that stop every one.' },
    provocative: { kicker: 'CASE FILE · JAPAN · 2026',
                   head: ['Safe country.', 'Specific traps.', 'Know them cold.'],
                   sub: 'The exact scripts, the red flags, and the Japanese phrases that shut every scam down.' },
  },

  quadHead: { A: 'Four ways Japan catches tourists off guard.',
              B: 'Same few moves. Every district.',
              C: 'Four documented patterns — sixty in the book.' },

  quad: [
    { n: '01', tag: 'THE TRAP', city: 'TOKYO', title: 'The Kabukicho Bottakuri Bar',
      tl: 'A tout waves you into a “cheap drinks” bar; when the ¥80,000+ bill lands, four bouncers block the door. Shinjuku Police logged 190 cases in 2024.',
      loss: '¥130,000', img: IMG.t1 },
    { n: '02', tag: 'THE BLESSING', city: 'TOKYO', title: 'The Fake Monk’s Bracelet',
      tl: 'A robed “monk” near Sensoji slips a gold bracelet onto your wrist as a “gift,” then opens a donation book for ¥3,000–¥10,000. Real monks don’t solicit on the street.',
      loss: '¥10,000', img: IMG.t2 },
    { n: '03', tag: 'THE SURPRISE', city: 'KYOTO', title: 'The Otoshi Cover Charge',
      tl: 'The little dish you never ordered? In Gion’s worst izakayas, “otoshi” plus hidden seat charges quietly stack ¥3,000+ onto the bill.',
      loss: '¥3,000', img: IMG.t3 },
    { n: '04', tag: 'THE AMBUSH', city: 'NARA', title: 'The Nara Park Deer',
      tl: 'The “bowing” deer turn the instant the ¥200 crackers appear — head-butts, bites, gored thighs. The prefecture logged 159 injuries in 2024.',
      loss: '159 hurt', img: IMG.t4 },
  ],

  inside: {
    head: 'Every scam, fully worked out — and the line that ends it.',
    img: IMG.shanghai1,
    caption: 'KYOTO · HIGASHIYAMA RICKSHAW',
    items: [
      ['Six universal red-flags', 'Learn them once — spot all 60.'],
      ['Exact scripts + yen amounts', 'City by city, scam by scam.'],
      ['A comic for every scam', 'Ghibli-style strips, like these.'],
      ['A Japanese exit-phrase card', 'Kana + romaji — screenshot it.'],
      ['Post-scam recovery playbook', 'First 15 minutes, first hour, first day.'],
      ['Emergency contacts', '110 police · 119 ambulance · 188 consumer.'],
    ],
    phrases: [
      ['kekkō desu', '結構です', 'No thank you.'],
      ['ikura desu ka?', 'いくらですか？', 'How much is it?'],
      ['keisatsu o yobimasu', '警察を呼びます', 'Calling the police.'],
    ],
  },

  desc: {
    head: { A: 'Read it on the flight over.', B: 'Read it on the flight over.', C: 'The whole file, before you fly.' },
    body: [
      'Japan: Tourist Scams is part of the tabiji.ai Travel Safety Series. Every scam is documented against Japanese police and consumer-agency records — the Tokyo Metropolitan Police, the National Consumer Affairs Center (188), and the Nara Prefectural Government — plus r/JapanTravel reports and verified local news. Not a recycled blog list.',
      '60 specific scams across Tokyo, Kyoto, Osaka, Sapporo and five more cities. The exact scripts, the red flags that give them away, and the Japanese phrases that shut them down — with kana and romaji you can show on your phone.',
      'Scams evolve, so the book is re-researched and updated every year — when a new edition ships, it appears in your Kindle library. Built for the traveler who wants to move through Japan relaxed, not braced.',
    ],
    badges: ['POLICE & CONSUMER-AGENCY SOURCED', 'UPDATED ANNUALLY', '9 CITIES', '60 DOCUMENTED SCAMS'],
    price: 'JAPAN · TRAVEL SAFETY SERIES',
  },
};

const SERIF = '"Newsreader", Georgia, "Times New Roman", serif';
const SANS  = '"Public Sans", system-ui, -apple-system, sans-serif';
const COND  = '"Saira Condensed", "Public Sans", sans-serif';
const MONO  = '"Spline Sans Mono", ui-monospace, monospace';

const THEMES = {
  A: {
    key: 'A', name: 'Field Guide', blurb: 'Indigo editorial · authority voice · framed comics',
    dark: false,
    pageBg: '#F3EADB', surface: '#FBF6EC', surfaceAlt: '#F2E6D4',
    ink: '#2A2117', sub: '#6E5E49',
    onPage: '#7A6A52', onPageSub: '#9A8B72',
    terra: '#34507F', terraDeep: '#1F2D4D', wash: '#DDE4EF',
    line: '#DAC8AD', lineSoft: '#E7DAC3',
    serif: SERIF, sans: SANS, mono: MONO, cond: COND,
  },
};

window.TABIJI = { IMG, C, THEMES };
