const fulfillOrder = require('../functions/fulfill-order');
const path = require('path');

const order = {
  id: 'order_1773102537468_obvawo',
  email: 'colandroangela@gmail.com',
  destination: 'Japan',
  startDate: '2029-05-06',
  endDate: '2029-05-23',
  groupSize: '5+',
  requests: 'Shibuya, Harajuku, Akihabara, Ginza, Central Tokyo, Asakusa, Poke Park Kanto, Ghibli Park, Shinjuku, Kichijoji Ghibli Museum, Gotokuji Cat Temple, Izu Shaboten Zoo, Mt Fuji, Osaka + Osaka Aquarium, Kyoto, Nara Deer Park, Toba Aquarium, Hiroshima'
};

// Load days from JSON files
const days1to3 = require(path.join(__dirname, 'fulfill-order_1773102537468_obvawo-day1-3.json'));
const days4to6 = require(path.join(__dirname, 'fulfill-order_1773102537468_obvawo-day4-6.json'));
const days7to9 = require(path.join(__dirname, 'fulfill-order_1773102537468_obvawo-day7-9.json'));
const days10to12 = require(path.join(__dirname, 'fulfill-order_1773102537468_obvawo-day10-12.json'));
const days13to15 = require(path.join(__dirname, 'fulfill-order_1773102537468_obvawo-day13-15.json'));
const days16to17 = require(path.join(__dirname, 'fulfill-order_1773102537468_obvawo-day16-17.json'));

const itineraryData = {
  destination: 'Japan',
  countryEmoji: '🇯🇵',
  title: 'The Ultimate Japan — 17 Days from Neon to Nature',
  subtitle: 'Tokyo • Izu Peninsula • Mt Fuji • Nagoya • Toba • Osaka • Kyoto • Nara • Hiroshima',
  description: "This is the Japan trip you've been dreaming about — 17 days that cover everything from Tokyo's electric neon pulse to Hiroshima's solemn peace memorials. Your crew of 5+ will devour street food in Osaka, soak in onsen overlooking Mt Fuji, hug capybaras on the Izu coast, wander Kyoto's bamboo forests, feed deer in Nara, and bar-hop through Golden Gai until the first train. Adventure, relaxation, nightlife — this itinerary delivers all three, with casual dining that'll change how you think about food forever.",
  duration: '17 nights',
  dates: 'May 6 – May 23, 2029',
  budget: '$$–$$$',
  pace: 'Moderate',
  bestFor: 'Groups · Adventure · Nightlife',
  highlights: [
    'Shibuya Crossing and Harajuku street culture',
    'Golden Gai and Shinjuku nightlife bar crawl',
    'Akihabara arcades and Ginza luxury shopping',
    'Sensō-ji Temple and old-world Asakusa',
    'Ghibli Museum in Mitaka and Gōtoku-ji Cat Temple',
    'PokéPark KANTO at Yomiuriland',
    'Capybara encounters at Izu Shaboten Zoo',
    'Mt Fuji views from Kawaguchiko',
    'Ghibli Park in Nagoya — a full day in Miyazaki\'s worlds',
    'Toba Aquarium — one of Japan\'s best ocean experiences',
    'Osaka Aquarium Kaiyukan and Dotonbori street food',
    'Kyoto — Fushimi Inari, Bamboo Grove, Kinkaku-ji, Gion',
    'Nara Deer Park and Tōdai-ji Great Buddha',
    'Hiroshima Peace Memorial and Miyajima Island'
  ],

  essentials: [
    { title: '🚅 Getting Around Japan', text: "Buy a 21-day Japan Rail Pass (¥60,450/~$420) before you arrive — it covers all Shinkansen bullet trains between cities and most JR local lines. For subways and buses within cities, get a Suica or Pasmo IC card at any station — tap-and-go everywhere. The pass will save your group thousands on the Tokyo → Nagoya → Osaka → Kyoto → Hiroshima route." },
    { title: '🌸 May in Japan', text: "May is one of the best months to visit — cherry blossoms are done but temperatures are perfect (18-25°C/65-77°F), flowers are blooming, and it's drier than summer. Golden Week (Apr 29 – May 6) crowds will just be clearing as you arrive May 6. Wisteria and azaleas are in full bloom." },
    { title: '💴 Money & Budget', text: "Japan is more cash-friendly than you'd expect — carry ¥10,000-20,000 daily. 7-Eleven ATMs accept all foreign cards. Budget roughly: casual meals ¥800-2,000/person, trains (with JR Pass) covered, attractions ¥500-2,500. Your $2,000-5,000/person for 17 days is very doable with casual dining and mid-range hotels." },
    { title: '🏨 Accommodation Strategy', text: "For a group of 5+, book Airbnb apartments or family rooms in business hotels. In Tokyo, stay in Shinjuku (central) or Shibuya (vibrant). Move hotels when changing regions: Izu onsen ryokan, Nagoya business hotel, Osaka near Namba, Kyoto near Gion. Book Hiroshima near the Peace Park." },
    { title: '🗣️ Language & Etiquette', text: "Learn: Sumimasen (excuse me), Arigatou (thank you), Onegaishimasu (please). Bow slightly when greeting. Remove shoes entering homes/temples/some restaurants. Don't tip — it's considered rude. Slurp ramen loudly — it's a compliment. Trash cans are rare — carry a small bag." },
    { title: '🍺 Nightlife Tips', text: "Last trains run around midnight in all cities. In Tokyo, if you miss it, stay out until 5am first trains or budget ¥3,000-5,000 for a taxi. Karaoke is open 24/7 and often cheaper after midnight. Golden Gai bars have ¥500-1,000 cover charges — ask before sitting. Convenience stores sell alcohol 24/7." }
  ],

  days: [...days1to3, ...days4to6, ...days7to9, ...days10to12, ...days13to15, ...days16to17],

  budgetTable: [
    { category: 'Accommodation (group rate)', budget: '$30–60/person/night', midrange: '$60–120/person/night', luxury: '$120–250/person/night' },
    { category: 'Meals (per person)', budget: '$20–35/day', midrange: '$35–60/day', luxury: '$60–120/day' },
    { category: 'Transport (with JR Pass)', budget: '$25/day (JR Pass)', midrange: '$30–40/day', luxury: '$50–80/day' },
    { category: 'Activities & Entry Fees', budget: '$10–20/day', midrange: '$20–40/day', luxury: '$40–80/day' },
    { category: 'Nightlife', budget: '$15–30/night', midrange: '$30–60/night', luxury: '$60–120/night' },
    { category: '17-Day Total (per person)', budget: '$2,000–3,500', midrange: '$3,500–6,000', luxury: '$6,000–10,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Tokyo Narita (NRT) or Haneda (HND) — Haneda is closer to the city', 'Narita Express to Shinjuku/Shibuya: 80 min, ~¥3,250 (covered by JR Pass)', 'Haneda to central Tokyo: 30 min by monorail or Keikyu Line', 'Fly out of Hiroshima (HIJ) or take Shinkansen back to Tokyo (~4 hrs)'] },
    { title: '🏨 Where to Stay', items: ['Tokyo: Shinjuku (transit hub) or Shibuya (nightlife central)', 'Izu Peninsula: Traditional ryokan with onsen — splurge night!', 'Nagoya: Near Nagoya Station for easy Ghibli Park access', 'Osaka: Namba or Shinsaibashi for Dotonbori and nightlife', 'Kyoto: Near Gion or Kawaramachi for traditional atmosphere', 'Hiroshima: Near Peace Memorial Park'] },
    { title: '🌡️ Weather in May', items: ['Temperatures: 18-25°C (65-77°F) — perfect for walking', 'Occasional rain — pack a compact umbrella', 'Humidity starts rising late May', 'Comfortable in layers — light jacket for evenings'] },
    { title: '💳 Payments', items: ['Cash is still king at small restaurants and markets', '7-Eleven, Lawson, FamilyMart ATMs accept foreign cards', 'IC cards (Suica/Pasmo) work at convenience stores too', 'Tax-free shopping at major stores with passport (purchases over ¥5,000)'] },
    { title: '📱 Connectivity', items: ['Get a pocket WiFi or eSIM — essential for group navigation', 'Sakura Mobile, Japan Wireless, or Ubigi eSIM are popular', 'Free WiFi at most train stations, convenience stores, and Starbucks', 'Google Maps works perfectly in Japan — download offline maps for subway stations'] }
  ]
};

fulfillOrder(order, itineraryData);
