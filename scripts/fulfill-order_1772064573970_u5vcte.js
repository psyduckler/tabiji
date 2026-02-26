const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772064573970_u5vcte',
  email: 'anon718@gmail.com',
  destination: 'Tokyo, Japan',
  startDate: '2026-03-27',
  endDate: '2026-03-30',
  groupSize: '3-4',
  requests: 'Adventure, Cultural, Foodie, Relaxation, Family-friendly. Mix of everything dining.'
};

const itineraryData = {
  destination: 'Tokyo, Japan',
  countryEmoji: '🇯🇵',
  title: 'Cherry Blossom Tokyo: Adventure, Culture & Flavour',
  subtitle: '3 nights of sakura strolls, hidden ramen alleys & family-friendly wonder',
  description: "You're arriving in Tokyo at peak cherry blossom season — the city will be draped in pink. This itinerary balances iconic cultural landmarks with foodie adventures, family fun, and genuine relaxation. From morning hanami under ancient sakura trees to electric Shibuya nights, intimate ramen counters to serene temple gardens, every day is packed with variety while leaving room to breathe. With 3-4 people, you'll move easily through Tokyo\'s world-class transit system and discover why this city is unlike anywhere else on earth.",
  duration: '3 nights',
  dates: 'Mar 27 – Mar 30, 2026',
  budget: '$$–$$$',
  pace: 'Moderate',
  bestFor: 'Families & Groups',
  highlights: [
    'Cherry blossoms at Shinjuku Gyoen in full bloom',
    'Senso-ji Temple & Nakamise Street in Asakusa',
    'teamLab Borderless immersive digital art',
    'Tsukiji Outer Market street food crawl',
    'Shibuya Crossing & Shibuya Sky observation deck',
    'Ueno Park hanami under 800+ cherry trees'
  ],

  essentials: [
    { title: '🌸 Cherry Blossom Season', text: 'Late March is peak sakura in Tokyo — expect full bloom around March 25-31. Shinjuku Gyoen, Ueno Park, and Meguro River are the top spots. Arrive early (before 10am) to beat crowds. Evening illuminations (yozakura) are magical.' },
    { title: '🚇 Getting Around', text: 'Get a Suica or Pasmo IC card (or use Apple Pay Suica) for seamless travel on all trains, subways, and buses. A 72-hour Tokyo Subway Ticket (¥1,500) is great value. Google Maps works perfectly for transit routing.' },
    { title: '👨‍👩‍👧‍👦 Family Tips', text: 'Tokyo is incredibly family-friendly. Most restaurants welcome kids, train stations have elevators, and convenience stores (konbini) are everywhere for snacks and essentials. Carry a small towel — many restrooms lack paper towels.' },
    { title: '🍜 Food Culture', text: "No tipping in Japan — it\'s considered rude. Many restaurants use ticket vending machines (shokkenki) to order. Convenience store food (7-Eleven, Lawson, FamilyMart) is genuinely excellent. Don't skip the depachika (department store basement food halls)." }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-27',
      neighborhoods: 'Asakusa · Ueno · Akihabara',
      title: 'Temples, Cherry Blossoms & Electric Town',
      description: "Start your Tokyo adventure in the historic heart of the city. Morning at Senso-ji temple, a hanami picnic under Ueno Park's 800+ cherry trees, then plunge into the neon-lit wonderland of Akihabara. Today covers culture, relaxation, and family fun in one sweep.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Senso-ji Temple & Nakamise Street',
              description: "Tokyo\'s oldest temple is stunning in cherry blossom season. Walk through the iconic Kaminarimon (Thunder Gate), browse the traditional shops along Nakamise-dori, and explore the temple grounds. The five-story pagoda framed by sakura is unforgettable.",
              details: [
                '⛩️ Free entry · Open 24hrs (main hall 6am-5pm)',
                '🛍️ Nakamise-dori has traditional snacks — try ningyo-yaki (custard-filled cakes)',
                '📸 Best photo: Kaminarimon lantern at dawn or framed by cherry blossoms',
                '👶 Flat, stroller-friendly paths throughout'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Asakusa Street Food',
              description: 'Grab melon pan (sweet bread) from Kagetsudo, freshly grilled senbei (rice crackers), and matcha soft serve along Nakamise-dori. A fun walking breakfast for the whole group.',
              meta: '💰 $ · 📍 Nakamise-dori, Asakusa'
            }
          ],
          tips: [
            { type: 'tip', text: 'Arrive before 9am to see Senso-ji without crowds. The incense smoke at the main hall is said to have healing properties — waft it toward you!' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ueno Park Cherry Blossom Hanami',
              description: "With over 800 cherry trees, Ueno Park is Tokyo\'s most beloved hanami spot. Spread a picnic blanket under the sakura canopy and soak it in. The central path between rows of trees is magical in full bloom. Kids can enjoy the playground and Shinobazu Pond swan boats.",
              details: [
                '🌸 800+ cherry trees line the central pathway',
                '🚣 Swan boats on Shinobazu Pond — ¥700 for 30 min, kids love it',
                '🎨 Tokyo National Museum nearby if you want world-class art',
                '🍱 Pick up a bento box from a konbini or Ueno Station for the picnic'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Hanami Picnic in Ueno Park',
              description: 'Grab bento boxes, onigiri, and drinks from a nearby konbini (7-Eleven or Lawson) and picnic under the cherry blossoms. This is peak Tokyo spring — embrace it.',
              meta: '💰 $ · 📍 Ueno Park central pathway'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Akihabara Electric Town',
              description: "Walk south from Ueno to Akihabara — Tokyo\'s famous electronics and anime district. Browse multi-story arcades, figure shops, and game centres. Kids and adults alike will be mesmerized by the sensory overload. Try your hand at UFO catchers (crane games).",
              details: [
                '🎮 Super Potato — retro game paradise across multiple floors',
                '🎪 Taito Station & SEGA arcades — crane games, rhythm games, photo booths',
                '🛒 Yodobashi Camera Akiba — 9 floors of everything electronic',
                '👾 Mandarake — multi-floor anime/manga collectibles'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Fuunji (Shinjuku)',
              description: "Head to Shinjuku for Tokyo\'s most legendary tsukemen (dipping ramen). The thick, intensely flavourful fish-pork broth and perfectly chewy noodles are worth the short queue. A must for any foodie visiting Tokyo.",
              meta: '💰 $ · 📍 Yoyogi, near Shinjuku Station South Exit · Expect 15-20 min queue'
            }
          ],
          tips: [
            { type: 'tip', text: "After ramen, take a short walk through Shinjuku's Omoide Yokocho (Memory Lane) — a narrow alley of tiny yakitori bars glowing with lanterns. Atmospheric and family-safe to walk through, even if you don\'t eat." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: 'Senso-ji Temple', num: 1, cat: 'attraction', desc: "Tokyo\'s oldest and most visited temple" },
        { lat: 35.7146, lng: 139.7966, label: 'Nakamise-dori', num: 2, cat: 'food', desc: 'Traditional shopping street with street food' },
        { lat: 35.7146, lng: 139.7732, label: 'Ueno Park', num: 3, cat: 'attraction', desc: '800+ cherry trees — premier hanami spot' },
        { lat: 35.7121, lng: 139.7704, label: 'Shinobazu Pond', num: 4, cat: 'attraction', desc: 'Swan boats and lotus pond in Ueno Park' },
        { lat: 35.6984, lng: 139.7731, label: 'Akihabara', num: 5, cat: 'attraction', desc: 'Electric Town — arcades, anime, electronics' },
        { lat: 35.6886, lng: 139.6998, label: 'Fuunji', num: 6, cat: 'food', desc: 'Legendary tsukemen ramen near Shinjuku' }
      ]
    },
    {
      num: 2,
      date: '2026-03-28',
      neighborhoods: 'Shibuya · Harajuku · Shinjuku Gyoen',
      title: 'Sakura Gardens, Harajuku Style & Shibuya Lights',
      description: "Today is pure Tokyo energy — start with a serene morning in Shinjuku Gyoen's spectacular cherry blossom gardens, dive into Harajuku's colourful fashion streets, then experience the electric pulse of Shibuya Crossing and sky-high city views. Something for everyone.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinjuku Gyoen National Garden',
              description: "Tokyo\'s most beautiful cherry blossom garden — 1,000+ trees of 65 varieties mean something is always blooming. The Japanese landscape garden with its pond and tea house is pure serenity. Unlike the party atmosphere at Ueno, Gyoen is peaceful (no alcohol allowed).",
              details: [
                '🌸 1,000+ cherry trees, 65 varieties — incredible diversity',
                '🎫 ¥500 entry · Open 9am-5:30pm (last entry 5pm)',
                '🍵 Traditional tea house serves matcha with seasonal wagashi',
                '📸 The French Formal Garden with sakura backdrop is iconic',
                '🚫 No alcohol, sports, or musical instruments — it stays peaceful'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "Arrive right at 9am opening — by 11am it\'s packed during cherry blossom season. The Shinjuku Gate entrance has shorter lines than the Okido Gate." }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Harajuku & Takeshita Street',
              description: "Walk from Shinjuku Gyoen to Harajuku — Tokyo\'s youth fashion epicentre. Takeshita Street is a narrow, colourful lane packed with quirky fashion, crêpe shops, and candy stores. Kids will love the energy. Then stroll the elegant tree-lined Omotesando for a contrast in style.",
              details: [
                '🍦 Marion Crêpes — Tokyo\'s most famous crêpe stand, always a queue',
                '👗 Takeshita Street — kawaii fashion, accessories, purikura photo booths',
                '⛩️ Meiji Shrine is a 5-min walk — serene forest shrine, free entry',
                '🛍️ Omotesando — Tokyo\'s Champs-Élysées, with flagship stores'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Afuri Ramen (Harajuku)',
              description: 'Light, refreshing yuzu shio (citrus salt) ramen — a perfect counterpoint to rich tonkotsu. The clear golden broth is aromatic and delicate. Great for those who want ramen without the heaviness.',
              meta: '💰 $$ · 📍 Harajuku/Ebisu · Order via ticket machine'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shibuya Crossing & Shibuya Sky',
              description: "Experience the world\'s busiest pedestrian crossing — up to 3,000 people cross at once. Then head up to Shibuya Sky, the rooftop observation deck 230m above the city. The open-air sky stage at sunset with Tokyo sprawling to the horizon is breathtaking. At night, the city lights are mesmerizing.",
              details: [
                '📸 Best Shibuya Crossing photos: from Starbucks 2F or Mag\'s Park rooftop',
                '🏙️ Shibuya Sky — book online in advance, ¥2,000 · Open until 10:30pm',
                '🌅 Time your visit for 30 min before sunset for both golden hour and night views',
                '🐕 Hachiko statue at the station — iconic Tokyo photo spot'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Gonpachi Nishi-Azabu',
              description: "The restaurant that inspired the crazy scene in Kill Bill. Dramatic wooden interior across multiple levels, with excellent yakitori, soba, and tempura. Lively atmosphere that\'s family-friendly early evening. A real experience.",
              meta: '💰 $$$ · 📍 Nishi-Azabu · Book ahead · Kids welcome'
            }
          ],
          tips: [
            { type: 'tip', text: 'After dinner, walk through Shibuya Center-gai for the full neon Tokyo experience. The energy at night is incredible — safe and family-friendly despite the buzz.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6852, lng: 139.7100, label: 'Shinjuku Gyoen', num: 1, cat: 'attraction', desc: "Tokyo\'s finest cherry blossom garden — 1,000+ trees" },
        { lat: 35.6702, lng: 139.7026, label: 'Takeshita Street', num: 2, cat: 'attraction', desc: 'Colourful Harajuku fashion and crêpe street' },
        { lat: 35.6764, lng: 139.6993, label: 'Meiji Shrine', num: 3, cat: 'attraction', desc: 'Serene Shinto shrine in a forested park' },
        { lat: 35.6595, lng: 139.7004, label: 'Shibuya Crossing', num: 4, cat: 'attraction', desc: "World\'s busiest pedestrian crossing" },
        { lat: 35.6580, lng: 139.7016, label: 'Shibuya Sky', num: 5, cat: 'attraction', desc: '230m rooftop observation deck with panoramic views' },
        { lat: 35.6624, lng: 139.7261, label: 'Gonpachi Nishi-Azabu', num: 6, cat: 'food', desc: 'Kill Bill restaurant — yakitori, soba, great atmosphere' }
      ]
    },
    {
      num: 3,
      date: '2026-03-29',
      neighborhoods: 'Toyosu · Odaiba · Ginza',
      title: 'Market Feasts, Digital Art & Tokyo Bay',
      description: "A day that hits every style — foodie heaven at Tsukiji/Toyosu markets, mind-bending immersive art at teamLab, waterfront relaxation at Odaiba, and sophisticated Ginza for your farewell evening. The perfect finale to your Tokyo adventure.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tsukiji Outer Market Food Crawl',
              description: "While the inner fish market moved to Toyosu, the Tsukiji Outer Market is still the ultimate Tokyo food experience. Dozens of stalls serve fresh sushi, tamagoyaki (sweet omelette), grilled seafood skewers, and Japanese street food. Walk and eat your way through — this is foodie paradise.",
              details: [
                '🍣 Sushi Dai queues are legendary — try smaller stalls for equal quality',
                '🥚 Tsukimura or Yamacho for fresh tamagoyaki on a stick',
                '🦀 Grilled king crab legs, uni (sea urchin), and tuna skewers everywhere',
                '🍡 Japanese pickles, mochi, and matcha desserts for the sweet-toothed',
                '⏰ Best from 7am-11am — many stalls close by early afternoon'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Tsukiji Outer Market Grazing',
              description: 'Skip a sit-down breakfast — graze through the market instead. Fresh sushi at 8am hits different. Budget ¥2,000-3,000 per person for a feast.',
              meta: '💰 $$ · 📍 Tsukiji Outer Market · Go hungry'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'teamLab Borderless (Azabudai Hills)',
              description: "One of Tokyo\'s most spectacular experiences — a massive digital art museum where immersive light installations flow seamlessly between rooms. Walk through waterfalls of light, fields of flowers, and infinite crystal universes. Kids and adults are equally mesmerized. Allow 2-3 hours.",
              details: [
                '🎫 Book online well in advance — sells out during sakura season',
                '💡 Wear white or light colours — the projections look amazing on you',
                '📍 Located in Azabudai Hills (moved from Odaiba)',
                '⏰ Allow 2-3 hours · Less crowded on weekdays before noon',
                '👶 Stroller-friendly, though some rooms are dark'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Midtown Food Hall (Azabudai Hills)',
              description: 'After teamLab, eat at the excellent food hall in Azabudai Hills. Tonkatsu, curry rice, udon — quality casual Japanese food in a sleek setting.',
              meta: '💰 $$ · 📍 Azabudai Hills · Multiple options'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Ginza Stroll & Farewell',
              description: "End your Tokyo adventure in Ginza — Tokyo\'s most elegant district. Wide boulevards, luxury boutiques, and incredible department store food halls (depachika). The basement floors of Mitsukoshi and Ginza Six have stunning prepared foods, wagashi (sweets), and desserts — a feast for the eyes.",
              details: [
                '🏬 Ginza Six basement — one of the best depachika in Tokyo',
                '🍰 Mitsukoshi B1 — wagashi, cakes, and beautifully packaged souvenirs',
                '🚶 Chuo-dori is pedestrian-only on weekends — wide and relaxing',
                '🌸 Bonus: cherry blossoms along the Meguro River are stunning at night (20 min away)'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Tempura Kondo',
              description: "One of Tokyo\'s most celebrated tempura restaurants. Master chef Fumio Kondo's sweet potato tempura is legendary — impossibly light, almost caramelized. A memorable farewell dinner. Book well in advance.",
              meta: '💰 $$$$ · 📍 Ginza · Lunch is more affordable than dinner · Reservations essential'
            }
          ],
          tips: [
            { type: 'tip', text: "If Tempura Kondo is fully booked, Ginza has incredible alternatives: Kyubey for sushi, Ginza Kagari for chicken ramen, or the depachika food halls for an amazing casual feast." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6654, lng: 139.7707, label: 'Tsukiji Outer Market', num: 1, cat: 'food', desc: 'Street food paradise — sushi, tamagoyaki, seafood skewers' },
        { lat: 35.6604, lng: 139.7392, label: 'teamLab Borderless', num: 2, cat: 'attraction', desc: 'Immersive digital art museum at Azabudai Hills' },
        { lat: 35.6713, lng: 139.7640, label: 'Ginza', num: 3, cat: 'attraction', desc: "Tokyo\'s elegant shopping and dining district" },
        { lat: 35.6713, lng: 139.7640, label: 'Ginza Six', num: 4, cat: 'food', desc: 'Stunning depachika basement food hall' },
        { lat: 35.6709, lng: 139.7653, label: 'Tempura Kondo', num: 5, cat: 'food', desc: 'Legendary tempura — the sweet potato is life-changing' },
        { lat: 35.6396, lng: 139.7153, label: 'Meguro River', num: 6, cat: 'attraction', desc: 'Spectacular nighttime cherry blossom illuminations' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '¥8,000–15,000/night', midrange: '¥15,000–35,000/night', luxury: '¥35,000–80,000/night' },
    { category: 'Meals (per person)', budget: '¥3,000–5,000/day', midrange: '¥5,000–12,000/day', luxury: '¥15,000–30,000/day' },
    { category: 'Transport', budget: '¥1,000–1,500/day', midrange: '¥1,500–3,000/day', luxury: '¥5,000–15,000/day (taxi)' },
    { category: 'Activities', budget: '¥0–2,000/day', midrange: '¥2,000–5,000/day', luxury: '¥5,000–15,000/day' },
    { category: 'teamLab Borderless', budget: '¥3,800pp', midrange: '¥3,800pp', luxury: '¥3,800pp' },
    { category: '3-Night Total (per person)', budget: '¥40,000–70,000', midrange: '¥70,000–160,000', luxury: '¥160,000–350,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Narita Airport (NRT): 60-90 min to central Tokyo via Narita Express (¥3,070) or Skyliner (¥2,520)', 'Haneda Airport (HND): 20-40 min to central Tokyo via monorail or Keikyu line — much closer', 'Pocket WiFi or eSIM essential — rent at the airport or order in advance'] },
    { title: '🏨 Where to Stay', items: ['Shinjuku — central hub, great transit, lively nightlife, close to Gyoen', 'Shibuya — trendy, walkable, great for families who want energy', 'Asakusa — traditional atmosphere, near Senso-ji, budget-friendly', 'Ginza/Tokyo Station — elegant, central, easy Shinkansen access'] },
    { title: '🌡️ Weather', items: ['Late March: 10-18°C (50-64°F) — pleasant but bring layers', 'Cherry blossoms typically peak March 25-April 2', 'Occasional rain — pack a compact umbrella', 'Evenings can be cool (8-10°C) — light jacket essential'] },
    { title: '💳 Money', items: ['Japan is still cash-heavy — carry ¥10,000-20,000 for small shops and ramen counters', 'Konbini (7-Eleven, Lawson) ATMs accept international cards', 'IC cards (Suica/Pasmo) work for transit and many vending machines/konbini', 'No tipping — ever. It can actually cause confusion.'] },
    { title: '📱 Useful Apps', items: ['Google Maps — excellent for Tokyo transit directions', 'Suica app (Apple Wallet) — tap-and-go transit from your phone', 'Tabelog — Japan\'s top restaurant rating app (like a local Yelp)', 'Google Translate camera mode — point at Japanese menus for instant translation'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
