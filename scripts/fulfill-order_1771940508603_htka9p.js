const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771940508603_htka9p',
  email: 'galaxycats510@gmail.com',
  destination: 'Osaka, Japan',
  startDate: '2026-03-11',
  endDate: '2026-03-14',
  groupSize: '3-4',
  requests: 'My father is vegetarian. USJ is a must see, and im planning a day trip to Kyoto on one of the days im there as well. we really enjoy scenic views and a little bit of shopping and the city'
};

const itineraryData = {
  destination: 'Osaka, Japan',
  countryEmoji: '🇯🇵',
  title: 'Osaka Unleashed — Neon Streets, USJ & a Kyoto Escape',
  subtitle: '4 days of street food, theme parks, ancient temples & city adventure for 3–4',
  description: "Osaka is Japan's most exhilarating city — a place where neon-soaked streets, world-class street food, and deep cultural history exist side by side. This four-day adventure hits everything: a full day at Universal Studios Japan (with Super Nintendo World!), a day trip through Kyoto's legendary temples and bamboo groves, vibrant Dotonbori at night, and Osaka's iconic castle. Vegetarian-friendly at every turn, endlessly photogenic, and absolutely unforgettable.",
  duration: '3 nights',
  dates: 'Mar 11 – Mar 14, 2026',
  budget: '$$–$$$',
  pace: 'Energetic',
  bestFor: 'Families & small groups',
  highlights: [
    'Full day at Universal Studios Japan — Super Nintendo World & Harry Potter',
    'Kyoto day trip: Fushimi Inari torii gates & Arashiyama bamboo grove',
    'Dotonbori at night — neon lights, street food & canal views',
    'Osaka Castle panoramic views and cherry blossom gardens',
    'Umeda Sky Building floating observatory at sunset'
  ],

  essentials: [
    {
      title: '🌸 March in Osaka',
      text: 'Mid-March is early spring — expect mild temperatures (10–17°C), occasional rain, and the very start of cherry blossom season. Pack layers and a compact umbrella. Osaka Castle Park may have early blossoms by March 14.'
    },
    {
      title: '🥦 Vegetarian in Osaka',
      text: 'Japan can be tricky for vegetarians due to dashi (fish stock) in many broths. Look for shojin ryori (Buddhist cuisine — fully plant-based), tofu restaurants, and establishments marked with 精進料理. Convenience stores (7-Eleven, FamilyMart) carry onigiri, tofu packs, and veggie snacks. Ask staff: "Niku to sakana nashi de onegaishimasu" (No meat or fish, please).'
    },
    {
      title: '🎢 USJ Express Pass',
      text: 'Book USJ tickets and Express Passes online before you travel — they sell out, especially on weekends. The Express Pass 7 covers Super Nintendo World, Harry Potter, Jurassic Park & more. Arrive at park opening (usually 8:30–9am) to minimise waits on the most popular rides.'
    },
    {
      title: '🚃 Getting Around',
      text: 'Get a Suica, ICOCA, or Welcome Suica IC card at the airport and tap on/off all trains, subways, and buses. The Osaka Metro day pass (¥820) is excellent value. Kyoto is 15 mins by Shinkansen (¥1,420) or 75 mins by cheaper JR Rapid service (¥560) from Osaka.'
    }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-11',
      neighborhoods: 'Dotonbori · Namba · Shinsaibashi · Kuromon Market',
      title: 'Arrival Day — Into the Neon Heart of Osaka',
      description: "Touch down and dive straight into Osaka's legendary food and nightlife district. Dotonbori at dusk is one of the great travel moments — giant neon signs reflecting off the canal, the smell of takoyaki in the air, and street after street of incredible food. Tonight is all about orientation, atmosphere, and eating way too much.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In & Kuromon Ichiba Market',
              description: "After settling into your hotel, head to Kuromon Ichiba — Osaka's legendary 'Kitchen Market', a covered arcade packed with fresh seafood, skewers, fruit, and local produce. A perfect introduction to Osaka's eating culture.",
              details: [
                '🏨 Stay in Namba or Shinsaibashi for walkable access to everything',
                '🦑 Kuromon is a 580m covered market — arrive hungry',
                '🥬 Vegetarian finds: fresh fruit stalls, tamagoyaki (egg omelette), pickled vegetables, steamed corn, and roasted chestnut vendors',
                '⏰ Market is most lively 9am–5pm; plan to arrive 3–4pm'
              ]
            }
          ],
          tips: [
            {
              type: 'tip',
              text: 'Most Kuromon vendors encourage you to eat right there at their stall. Grab skewers and stand-eat — that\'s the Osaka way!'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dotonbori Neon Walk & Canal Views',
              description: "As dusk falls, make your way to Dotonbori — Osaka's most iconic street. The giant Glico Running Man sign, the mechanical crab, and the blazing neon canal reflections are unmissable. Walk from Ebisubashi Bridge along the canal for the best photos, then explore the backstreets of Namba.",
              details: [
                '📸 Ebisubashi Bridge — best spot for the Glico Man + canal reflection shot',
                '🌃 Neon is most spectacular after 7pm',
                '🛍️ Shinsaibashi-suji shopping arcade is covered — perfect if it rains',
                '🎮 Den Den Town (Nipponbashi) nearby for anime/gaming nerds in the group'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Mizuno (Dotonbori) — Okonomiyaki',
              description: "Osaka's most famous okonomiyaki restaurant. This Osaka-style savoury pancake is a must — watch the chefs cook it on the iron griddle in front of you. Vegetarian versions are available (just ask them to skip the bonito flakes).",
              meta: '💰 $$ · 📍 1-4-15 Dotonbori, Namba · Expect a short queue'
            },
            {
              type: '🍡 Street Food',
              name: 'Takoyaki & Kushikatsu Crawl',
              description: "Graze Dotonbori's street stalls for takoyaki (octopus balls — non-veg), kushikatsu (deep-fried skewers), and for Dad: tofu-based snacks and vegetable tempura at dedicated stalls.",
              meta: '💰 $ · 📍 Dotonbori street stalls · Many vegetarian skewer options available'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6686, lng: 135.5030, label: 'Dotonbori', num: 1, cat: 'attraction', desc: 'Osaka\'s neon heart — iconic Glico Man sign and canal' },
        { lat: 34.6685, lng: 135.5027, label: 'Ebisubashi Bridge', num: 2, cat: 'attraction', desc: 'Best photo spot for the famous canal reflection' },
        { lat: 34.6706, lng: 135.5054, label: 'Kuromon Ichiba Market', num: 3, cat: 'food', desc: 'Osaka\'s Kitchen — 580m covered food market' },
        { lat: 34.6722, lng: 135.5005, label: 'Shinsaibashi-suji', num: 4, cat: 'attraction', desc: 'Covered shopping arcade for fashion and souvenirs' },
        { lat: 34.6684, lng: 135.5040, label: 'Mizuno Okonomiyaki', num: 5, cat: 'food', desc: 'Legendary Osaka-style okonomiyaki restaurant' }
      ]
    },
    {
      num: 2,
      date: '2026-03-12',
      neighborhoods: 'Universal City · Sakurajima · USJ',
      title: 'USJ Day — Super Nintendo World & Wizarding Magic',
      description: "Today is all USJ, all day. Universal Studios Japan is one of the world's best theme parks — and with Super Nintendo World and The Wizarding World of Harry Potter both in the park, you'll need every minute. Get there at opening, hit the big rides early, and stay for the evening light show.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Early Entry — Beat the Crowds',
              description: "Take the JR Loop Line to Universal City Station and arrive before park opening (usually 8:30–9:00am). Head directly to Super Nintendo World as soon as the gates open — the interactive AR wristband experience and Mario Kart ride fill up fast.",
              details: [
                '🚃 JR Osaka Loop Line → Universal City Station (15 min from Namba)',
                '⏰ Gates open 8:30–9am; arrive 30 min before opening',
                '🎮 Super Nintendo World: Mario Kart: Koopa\'s Challenge is the headline ride',
                '🍄 Buy the Power-Up Band (¥3,500) for interactive AR challenges throughout the area',
                '📱 Download the USJ app and book ride times digitally from the app'
              ]
            }
          ],
          tips: [
            {
              type: 'tip',
              text: 'Secure a timed entry pass for Super Nintendo World via the USJ app immediately upon entering the park — they go fast and are required to enter the area during peak periods.'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Wizarding World of Harry Potter & Jurassic Park',
              description: "After Super Nintendo World, head to Hogsmeade and explore The Wizarding World of Harry Potter. Harry Potter and the Forbidden Journey is a must-ride. Then hit Jurassic Park: The Ride (prepare to get soaked!) and The Flying Dinosaur rollercoaster — USJ's signature.",
              details: [
                '🧙 Butterbeer (¥990) is available in both regular and non-alcoholic versions',
                '🦕 The Flying Dinosaur: Japan\'s longest rollercoaster — spectacular',
                '🌊 Jurassic Park water ride = you WILL get wet. Bring a spare layer.',
                '🎭 Minion Park and Hollywood Dream are great for younger/less-thrill members of the group'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Three Broomsticks (Wizarding World)',
              description: "Eat lunch in Hogsmeade at Three Broomsticks — roasted chicken, pumpkin juice, and a full Harry Potter atmosphere. Vegetarian options available.",
              meta: '💰 $$ · 📍 Inside Wizarding World of Harry Potter at USJ'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Evening Show & Night Parade',
              description: "Stay for the park's evening entertainment — USJ's night-time shows and parade are spectacular with illuminations and character appearances. Check the park schedule for the day's final show times.",
              details: [
                '✨ Evening illuminations are especially beautiful in spring',
                '🎆 Check USJ app for night parade and show times on your date',
                '🛍️ Universal City Walk (just outside the park) has shopping and dining for after'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6654, lng: 135.4322, label: 'Universal Studios Japan', num: 1, cat: 'attraction', desc: 'USJ main entrance — full-day theme park experience' },
        { lat: 34.6658, lng: 135.4330, label: 'Super Nintendo World', num: 2, cat: 'attraction', desc: 'Interactive Mario-themed zone with AR wristbands' },
        { lat: 34.6660, lng: 135.4318, label: 'Wizarding World of Harry Potter', num: 3, cat: 'attraction', desc: 'Hogsmeade replica with Butterbeer and Forbidden Journey ride' },
        { lat: 34.6656, lng: 135.4325, label: 'The Flying Dinosaur', num: 4, cat: 'attraction', desc: 'Japan\'s longest rollercoaster — spectacular views' },
        { lat: 34.6648, lng: 135.4320, label: 'Universal City Walk', num: 5, cat: 'food', desc: 'Shopping and dining just outside the park gates' }
      ]
    },
    {
      num: 3,
      date: '2026-03-13',
      neighborhoods: 'Fushimi · Higashiyama · Arashiyama · Gion',
      title: 'Kyoto Day Trip — Torii Gates, Bamboo & Ancient Kyoto',
      description: "Kyoto is just 15 minutes from Osaka by Shinkansen and a world away in feeling. Today you'll walk through thousands of vermillion torii gates at Fushimi Inari, stroll the magical bamboo grove at Arashiyama, and wander the geisha district of Gion. Kyoto's culinary scene is exceptional for vegetarians — shojin ryori (Buddhist cuisine) was invented here.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Early Train to Kyoto & Fushimi Inari Taisha',
              description: "Catch an early train to Kyoto and head straight to Fushimi Inari — the shrine famous for thousands of vermillion torii gates winding up a forested mountain. Go before 9am for a spiritual, crowd-free experience. You don't need to climb all the way to the top — the first two 'stages' (about 45 minutes round trip) are the most dramatic.",
              details: [
                '🚃 Shinkansen (Hikari/Sakura): Shin-Osaka → Kyoto in 15 min (¥1,420)',
                '🚃 JR Rapid (budget): Osaka → Kyoto in 75 min (¥560)',
                '⛩️ Fushimi Inari: take the JR Nara Line from Kyoto Station to Inari Station (5 min)',
                '🌅 Arrive before 9am for golden light and fewer crowds',
                '📸 The tunnel of gates is most photogenic in the first 30 minutes of the hike'
              ]
            }
          ],
          tips: [
            {
              type: 'tip',
              text: 'The full Fushimi Inari mountain circuit takes 2–3 hours. With limited time, hike to Yotsutsuji intersection (about 45 min up) for a panoramic view of Kyoto — then head back down.'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arashiyama Bamboo Grove & Tenryu-ji Garden',
              description: "Take a train across Kyoto to Arashiyama — the bamboo grove is one of Japan's most iconic sights. The towering stalks sway and creak in the wind; it's eerie, beautiful, and utterly unique. Just beyond the grove, Tenryu-ji temple garden offers perfectly composed views over a koi pond with bamboo-covered mountains behind.",
              details: [
                '🎋 Bamboo Grove is most atmospheric early morning or late afternoon',
                '🌿 Tenryu-ji Garden: ¥500 entry — one of Kyoto\'s finest Zen gardens',
                '🛶 Hozu River boat ride: optional scenic 2-hour drift down the river (¥4,100)',
                '🐒 Monkey Park on the hill above: great for younger members of the group'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Shigetsu at Tenryu-ji — Shojin Ryori',
              description: "Inside Tenryu-ji temple, Shigetsu serves traditional shojin ryori — Japan's ancient Buddhist vegetarian cuisine. Multi-course meals of seasonal vegetables, tofu, and rice. Fully vegetarian, exquisite, and deeply immersive. Perfect for Dad.",
              meta: '💰 $$$ · 📍 Tenryu-ji Temple, Arashiyama · Reservation recommended'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Gion District Stroll & Nishiki Market',
              description: "Spend your final Kyoto hours in Gion — the preserved geisha district of wooden machiya townhouses, stone-paved alleys, and traditional tea houses. If you're lucky, you may spot a geiko or maiko in the late afternoon. Then swing through Nishiki Market ('Kyoto's Kitchen') for food souvenirs before the train back to Osaka.",
              details: [
                '🏮 Hanamikoji Street in Gion: best preserved traditional streetscape',
                '👘 Geiko and maiko are most visible between 5–6pm heading to evening engagements',
                '🛒 Nishiki Market: 400-year-old covered market, 100+ vendors',
                '🥢 Nishiki highlights for vegetarians: yudofu (tofu), pickled vegetables (tsukemono), sesame snacks, matcha sweets',
                '🚃 Train back to Osaka from Kyoto Station (15–75 min depending on service)'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner (back in Osaka)',
              name: 'Ganso Kushikatsu Daruma — Shinsekai',
              description: "Return to Osaka and head to Shinsekai — the city's retro 1920s entertainment district — for kushikatsu (deep-fried skewers on sticks). Daruma is the original chain; vegetable and cheese skewers are delicious for vegetarians. The double-dipping ban is sacred — don't break it!",
              meta: '💰 $ · 📍 Shinsekai, Naniwa Ward · Buzzing atmosphere, affordable'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari Taisha', num: 1, cat: 'attraction', desc: 'Thousands of vermillion torii gates up a sacred mountain' },
        { lat: 35.0168, lng: 135.6727, label: 'Arashiyama Bamboo Grove', num: 2, cat: 'attraction', desc: 'Iconic towering bamboo forest — otherworldly beauty' },
        { lat: 35.0165, lng: 135.6759, label: 'Tenryu-ji Temple', num: 3, cat: 'attraction', desc: 'UNESCO Zen garden — and home to Shigetsu shojin ryori' },
        { lat: 35.0038, lng: 135.7784, label: 'Gion District', num: 4, cat: 'attraction', desc: 'Historic geisha district with preserved wooden machiya' },
        { lat: 35.0046, lng: 135.7665, label: 'Nishiki Market', num: 5, cat: 'food', desc: 'Kyoto\'s Kitchen — 400-year-old covered food market' },
        { lat: 34.6527, lng: 135.5065, label: 'Shinsekai', num: 6, cat: 'attraction', desc: 'Retro 1920s district — kushikatsu and Tsutenkaku Tower' }
      ]
    },
    {
      num: 4,
      date: '2026-03-14',
      neighborhoods: 'Osaka Castle · Nakanoshima · Umeda · Tenjinbashisuji',
      title: 'Osaka Grand Finale — Castle, Sky & Shopping',
      description: "Your last day in Osaka is a perfect blend of history, panoramic views, and shopping. Start at Osaka Castle — a stunning feudal fortress surrounded by early spring gardens — then float up to the Umeda Sky Building's 'Floating Garden' observatory for city views. Wrap up with a stroll through Japan's longest shopping arcade before a farewell dinner.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Osaka Castle & Castle Park',
              description: "Start early at Osaka Castle — one of Japan's most iconic landmarks. The five-story main keep contains a fascinating museum of feudal Japan history. The surrounding park is spectacular in early spring, with plum blossoms (February) giving way to early cherry blossoms (late March). Climb to the top floor for 360° city panoramas.",
              details: [
                '🏯 Castle entry: ¥600 per person · Open 9am–5pm',
                '🌸 Osaka Castle Park has 600 cherry trees — early bloomers may show by March 14',
                '📸 Best exterior shot: approach from the Otemon gate to the south',
                '📖 Museum inside: 8 floors of samurai armour, maps, and Toyotomi history'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Hotel breakfast or Nakanoshima café',
              description: "Fuel up at your hotel or grab coffee and pastries at one of the Nakanoshima riverside cafés on the way to the castle. Many modern café-bakeries in this area open at 8am.",
              meta: '💰 $ · 📍 Nakanoshima, along the river'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Umeda Sky Building — Floating Garden Observatory',
              description: "The Umeda Sky Building is one of Osaka's most distinctive architectural icons — two towers connected at the top by a glass 'Floating Garden' walkway at 170m. The views over the sprawling city grid, with Rokko mountains in the background, are breathtaking. Go in the late afternoon for golden light.",
              details: [
                '🏙️ Floating Garden Observatory: ¥1,500 per person · Open 9:30am–10:30pm',
                '📸 The outdoor rooftop ring walkway is open-air — thrilling and photogenic',
                '🌆 On clear days you can see Akashi Kaikyo Bridge in the distance',
                '🛒 Takimi-koji underground is a retro 1920s-themed food market with great vegetarian options'
              ]
            },
            {
              title: 'Tenjinbashisuji Shopping Arcade',
              description: "Stroll the full 2.6km of Tenjinbashisuji — Japan's longest covered shopping arcade. It stretches through working-class Osaka with local shops, traditional sweets, vintage stores, and no tourist markup. Perfect for final souvenir hunting.",
              details: [
                '🛍️ Japan\'s longest shotengai (shopping street) — 2.6km of covered shops',
                '🍡 Mochi, wagashi (traditional sweets), and dorayaki make perfect souvenirs',
                '👘 A few shops sell second-hand kimono and yukata at good prices'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset at Umeda Sky Building',
              description: "Time your visit to the Umeda Sky Building observation deck to catch the sunset — the sky turns gold and then purple over the Osaka grid. A perfect final memory.",
              details: [
                '🌅 Sunset in mid-March is around 6:10pm',
                '💡 Book entry online to avoid queues at the lift'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Ajino Mise Nakamura — Tofu Kaiseki',
              description: "Go out in style with a tofu kaiseki dinner — multi-course refined Japanese cuisine centred around silken tofu in an elegant setting. The delicate flavours of dashi-braised tofu, agedashi, and seasonal vegetable dishes make it perfect for Dad, and spectacular for everyone. A truly memorable final meal.",
              meta: '💰 $$–$$$ · 📍 Kitashinchi / Umeda area · Reservation recommended for groups'
            },
            {
              type: '🍺 Nightcap',
              name: 'Dotonbori Bar Crawl',
              description: "End the trip back on Dotonbori's electric streets — grab a last round of Asahi draft beer, takoyaki, and soak up the neon one final time.",
              meta: '💰 $ · 📍 Dotonbori canal walk'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6873, lng: 135.5259, label: 'Osaka Castle', num: 1, cat: 'attraction', desc: 'Iconic feudal fortress with museum and spring gardens' },
        { lat: 34.6934, lng: 135.4900, label: 'Umeda Sky Building', num: 2, cat: 'attraction', desc: 'Floating Garden Observatory — 170m open-air panorama' },
        { lat: 34.7053, lng: 135.5103, label: 'Tenjinbashisuji Arcade', num: 3, cat: 'attraction', desc: 'Japan\'s longest covered shopping street — 2.6km' },
        { lat: 34.6934, lng: 135.4905, label: 'Takimi-koji Underground', num: 4, cat: 'food', desc: 'Retro 1920s-themed underground food market at Sky Building' },
        { lat: 34.6872, lng: 135.5270, label: 'Otemon Gate', num: 5, cat: 'attraction', desc: 'Main castle entrance — best approach for photos' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '¥8,000–12,000/night', midrange: '¥15,000–25,000/night', luxury: '¥30,000–60,000/night' },
    { category: 'Meals (per person)', budget: '¥2,000–3,500/day', midrange: '¥4,000–7,000/day', luxury: '¥8,000–15,000/day' },
    { category: 'USJ Tickets (per person)', budget: '¥9,400 standard', midrange: '+¥6,000–10,000 Express Pass', luxury: 'VIP Experience ¥40,000+' },
    { category: 'Transport (local)', budget: '¥800–1,500/day', midrange: '¥1,500–3,000/day', luxury: '¥5,000+/day (taxis)' },
    { category: 'Kyoto Day Trip', budget: '¥560 each way (JR Rapid)', midrange: '¥1,420 each way (Shinkansen)', luxury: 'Private car from ¥30,000' },
    { category: '4-Day Total (per person)', budget: '¥40,000–55,000', midrange: '¥70,000–110,000', luxury: '¥150,000+' }
  ],

  practicalInfo: [
    {
      title: '✈️ Getting There',
      items: [
        'Kansai International Airport (KIX) serves Osaka — about 50 min from the city',
        'Haruka Express train: KIX → Shin-Osaka in 50 min (¥2,900); buy in advance for discounts',
        'NANKAI Rapi:t express: KIX → Namba in 38 min (¥1,430) — great if staying in Namba'
      ]
    },
    {
      title: '🏨 Where to Stay',
      items: [
        'Namba / Dotonbori — best location for food, nightlife and metro access',
        'Shinsaibashi — central, great for shopping, easy subway connections',
        'Umeda / Osaka Station — convenient for USJ, Kyoto day trip, and Sky Building',
        'Recommended hotels: Cross Hotel Osaka, The Blossom Namba, OMO7 Osaka (Hoshino Resorts)'
      ]
    },
    {
      title: '🌡️ March Weather',
      items: [
        'Average temps: 8–17°C — cool mornings, mild afternoons',
        'Occasional rain; pack a lightweight waterproof layer and compact umbrella',
        'UV is mild; no serious sun protection needed',
        'Cherry blossoms typically begin in Osaka around March 25 — you may catch early buds!'
      ]
    },
    {
      title: '💴 Money',
      items: [
        'Japan is still largely cash-based — carry ¥10,000–20,000 in cash daily',
        'IC cards (Suica/ICOCA) work for trains, convenience stores, vending machines',
        '7-Eleven and Japan Post ATMs accept international cards',
        'Tipping is not customary in Japan — never expected, sometimes politely refused'
      ]
    },
    {
      title: '📱 Connectivity',
      items: [
        'Buy a Pocket WiFi or eSIM at the airport — fast and affordable',
        'Recommended eSIM providers: Airalo, IIJmio Tourist SIM',
        'Google Maps works perfectly in Japan — download Osaka and Kyoto offline maps',
        'Hyperdia app is the best for train journey planning'
      ]
    }
  ]
};

fulfillOrder(order, itineraryData)
  .then(result => {
    console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
  })
  .catch(err => {
    console.error('❌ Error:', err.message);
    process.exit(1);
  });
