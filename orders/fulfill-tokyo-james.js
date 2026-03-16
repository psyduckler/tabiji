const fulfillOrder = require('../functions/fulfill-order');
const fs = require('fs');
const path = require('path');

// Load day data from split JSON files
const days1_4 = JSON.parse(fs.readFileSync(path.join(__dirname, 'fulfill-tokyo-james-days1-4.json'), 'utf8'));
const days5_8 = JSON.parse(fs.readFileSync(path.join(__dirname, 'fulfill-tokyo-james-days5-8.json'), 'utf8'));
const days9_11 = JSON.parse(fs.readFileSync(path.join(__dirname, 'fulfill-tokyo-james-days9-11.json'), 'utf8'));

const order = {
  id: 'order_1773607951654_nei8rm',
  orderId: 'order_1773607951654_nei8rm',
  email: 'jamesogbeide@gmail.com',
  customerName: null,
  startDate: '2026-10-13'
};

const itineraryData = {
  destination: 'Tokyo, Japan',
  countryEmoji: '🇯🇵',
  title: 'Tokyo to Kyoto: Neon, Temples & Private Onsen',
  subtitle: '11 days across Japan — from teamLab\'s digital cosmos to Nintendo\'s playground, Himeji\'s white heron castle, a private Hakone onsen, and two nights at the Park Hyatt\'s Lost in Translation bar',
  description: 'A multi-city journey through the beating heart of Japan. Start in electric Tokyo with teamLab Borderless and Golden Gai. Bullet train to Kyoto for Fushimi Inari, the Nintendo Museum, and a chopstick making class. Day trip to Himeji Castle. Eat your way through Osaka. Escape to Hakone for a private onsen night in the mountains. Return to Tokyo in style at the Park Hyatt, where Lost in Translation\'s New York Bar awaits on the 52nd floor. Every special request woven in, every meal researched, every minute considered.',
  duration: '11 days',
  dates: 'October 13–24, 2026',
  budget: 'Mid-range to Upscale',
  pace: 'Active but balanced — big days followed by relaxation',
  bestFor: 'Adventure · Cultural · Foodie · Relaxation · Nightlife',
  highlights: [
    'teamLab Borderless at Azabudai Hills — immersive digital art',
    'Nintendo Museum in Uji — lottery tickets, interactive exhibits',
    'Chopstick making class in Kyoto — handmade souvenir',
    'Himeji Castle — Japan\'s greatest original castle',
    'Private onsen night in Hakone — volcanic mountain hot springs',
    'Park Hyatt Tokyo — Lost in Translation\'s New York Bar on the 52nd floor',
    'Fushimi Inari\'s 10,000 torii gates at golden hour',
    'Osaka\'s Dōtonbori food crawl — takoyaki, okonomiyaki, and more',
    'Golden Gai\'s 200+ tiny themed bars in Shinjuku',
    'Nara\'s bowing deer and the Great Buddha at Todai-ji'
  ],

  essentials: [
    {
      title: '🌡️ Weather in October',
      text: 'Mid-to-late October in Japan is gorgeous — comfortable 15–22°C (59–72°F) with low humidity and occasional rain. Pack layers: light jacket for evenings, rain layer, comfortable walking shoes. Hakone will be cooler (10–16°C). Early autumn colors are starting, especially in Kyoto and Hakone. Typhoon season is winding down but keep an eye on forecasts.'
    },
    {
      title: '🚄 Getting Around',
      text: 'This itinerary uses shinkansen (bullet trains) between cities. Individual tickets are recommended over a JR Pass for this route — you\'ll take 3-4 long-distance trains. IC cards (Suica/Pasmo) handle all local trains, buses, and convenience store payments. In Hakone, the Hakone Free Pass covers everything. Tokyo subway is straightforward — Google Maps works perfectly.'
    },
    {
      title: '💴 Money & Budget',
      text: 'Japan is still largely cash-friendly, though card acceptance has improved dramatically. Carry ¥10,000–20,000 in cash at all times for small restaurants and markets. 7-Eleven ATMs accept international cards. Expected daily spend: ¥8,000–15,000/person for food, ¥2,000–5,000 for transport, ¥1,000–3,000 for attractions. The Hakone ryokan night will be the biggest single expense (¥30,000–80,000 for two including meals).'
    },
    {
      title: '📱 Connectivity & Apps',
      text: 'Get an eSIM or pocket WiFi (pick up at NRT or order ahead). Must-have apps: Google Maps (excellent in Japan), Suica (Apple Wallet), SmartEX (shinkansen booking), Google Translate (camera mode for menus). Download offline maps for areas with spotty signal (Hakone mountains, temple areas).'
    },
    {
      title: '🎫 Advance Booking Required',
      text: '⚠️ CRITICAL BOOKINGS: (1) Nintendo Museum tickets — LOTTERY ONLY via Nintendo Account, enter the drawing for October when it opens (~2 months ahead). (2) teamLab Borderless — sells out weeks ahead, book immediately when tickets open. (3) Hakone ryokan with private onsen — October is peak season, book 2-3 months early. (4) Park Hyatt Tokyo — Oct 22-24, book now. (5) Chopstick making class in Kyoto — book online 1-2 weeks ahead.'
    },
    {
      title: '✈️ Flight Info',
      text: 'Arrival: NRT at 4:30 PM on October 13. Plan for 1–1.5 hours for immigration/customs. Departure: NRT at 5:20 PM on October 24. Leave central Tokyo by 1:00 PM — Narita Express from Shinjuku is ~80 minutes, plus check-in buffer.'
    }
  ],

  days: [...days1_4, ...days5_8, ...days9_11],

  budgetTable: [
    { category: 'Flights (in-country)', estimate: '¥45,000–55,000/pp', notes: 'Shinkansen Tokyo↔Kyoto, Kyoto→Himeji, Himeji→Osaka, Kyoto→Odawara, Hakone→Shinjuku' },
    { category: 'Hotels (9 nights)', estimate: '¥150,000–250,000 total', notes: '7 nights mid-range + 2 nights Park Hyatt (~¥60,000–80,000/night)' },
    { category: 'Hakone Ryokan (1 night)', estimate: '¥30,000–80,000 total', notes: 'Private onsen room, includes kaiseki dinner + breakfast' },
    { category: 'Food', estimate: '¥5,000–10,000/pp/day', notes: 'Casual throughout — street food, ramen, izakayas, market grazes' },
    { category: 'Attractions', estimate: '¥15,000–20,000/pp total', notes: 'teamLab, Nintendo Museum, castles, shrines, gardens, Hakone loop' },
    { category: 'Local Transport', estimate: '¥2,000–4,000/pp/day', notes: 'Subway, buses, Hakone Free Pass, taxis' },
    { category: 'Nightlife', estimate: '¥3,000–8,000/pp/night', notes: 'Golden Gai, Osaka bars, New York Bar cocktails' }
  ],

  practicalInfo: [
    {
      title: '🚅 Shinkansen Booking',
      items: [
        'Use the SmartEX app to book shinkansen tickets with a credit card (English interface, seat selection, mobile tickets)',
        'Book 1-2 days ahead for peace of mind, though same-day unreserved seats usually work',
        'The Nozomi is fastest but doesn\'t accept JR Pass — not relevant for you since individual tickets are better value for this route'
      ]
    },
    {
      title: '♨️ Onsen Etiquette',
      items: [
        'Wash thoroughly at the shower stations BEFORE entering the bath',
        'No swimsuits allowed. No towels in the water (small towel goes on your head)',
        'Tattoos: many public onsen ban tattoos — your PRIVATE onsen in Hakone avoids this issue entirely',
        'Soak, relax, repeat — there\'s no time limit'
      ]
    },
    {
      title: '🏯 Temple & Shrine Etiquette',
      items: [
        'At shrines: bow before the torii gate, wash hands at the temizuya (purification fountain), bow twice, clap twice, bow once at the main hall',
        'At temples: don\'t clap (that\'s for shrines). Remove shoes where indicated. Keep voice low inside'
      ]
    },
    {
      title: '🍽️ Dining Tips',
      items: [
        'Most restaurants have plastic food displays or photo menus — pointing works fine',
        'Don\'t tip (it\'s considered rude in Japan)',
        'Say "itadakimasu" before eating and "gochisousama" after',
        'Slurping noodles is not only OK, it\'s expected and considered polite',
        'Many restaurants are cash-only — especially small ramen shops and izakayas'
      ]
    },
    {
      title: '🗑️ Trash & Manners',
      items: [
        'Japan has almost no public trash cans — carry a small bag for your trash and dispose at convenience stores or your hotel',
        'Don\'t eat while walking (it\'s considered rude)',
        'Stand on the left side of escalators in Tokyo (right in Osaka)',
        'Be quiet on trains — phone conversations are frowned upon'
      ]
    },
    {
      title: '📦 Luggage Forwarding (Takkyubin)',
      items: [
        'Japan\'s luggage forwarding service is magical — drop bags at any convenience store, hotel front desk, or luggage counter',
        'Delivery to your next hotel by the next day (~¥2,000/bag)',
        'Use this when traveling between cities to explore hands-free',
        'Essential for the Himeji day trip and the Kyoto→Hakone→Tokyo transitions'
      ]
    }
  ]
};

// Run fulfillment
try {
  const result = fulfillOrder(order, itineraryData);
  console.log('\n🎉 FULFILLMENT COMPLETE!');
  console.log('Slug:', result.slug);
  console.log('URL:', result.url);
  console.log('Email sent:', result.emailSent);
} catch (err) {
  console.error('\n❌ FULFILLMENT FAILED:', err.message);
  process.exit(1);
}
