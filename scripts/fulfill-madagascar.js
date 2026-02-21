const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771635198527_d7lht7',
  email: 'psyduckler@gmail.com',
  destination: 'Madagascar',
  startDate: '2026-02-27',
  endDate: '2026-03-02',
  groupSize: 2,
  requests: ''
};

const itineraryData = {
  destination: 'Antananarivo, Madagascar',
  countryEmoji: '🇲🇬',
  title: 'Lemurs, Nightlife & Family Magic in Madagascar',
  subtitle: '3 nights of wildlife wonder, vibrant nightlife & family-friendly adventure for two',
  description: "Madagascar is unlike anywhere else on Earth — a biodiversity hotspot where lemurs leap through ancient rainforests and chameleons change colour before your eyes. This itinerary balances Antananarivo's surprisingly lively nightlife scene with family-friendly wildlife encounters, cultural exploration, and unforgettable day trips. From the hilltop Rova palace to lemur parks, bustling street markets to rooftop cocktail bars, this is Madagascar at its most accessible and exciting.",
  duration: '3 nights',
  dates: 'Feb 27 – Mar 2, 2026',
  budget: '$–$$',
  pace: 'Moderate',
  bestFor: 'Couples, Families',
  highlights: [
    'Meet free-roaming lemurs at Lemurs\' Park',
    'Explore the historic Rova palace with panoramic city views',
    'Night out in Antananarivo\'s vibrant bar and club scene',
    'Day trip to Andasibe-Mantadia rainforest to hear Indri lemurs sing',
    'Stroll the colourful Analakely street market',
    'Sundowners overlooking the city at a rooftop bar'
  ],

  essentials: [
    { title: '🌧️ Rainy Season', text: 'Late February is peak rainy season in Madagascar. Expect afternoon downpours (mornings are often clear). Pack a light rain jacket, waterproof bag, and quick-dry clothes. Roads to Andasibe can be muddy — a 4x4 transfer is recommended.' },
    { title: '💰 Currency & Costs', text: 'The Malagasy Ariary (MGA) is the local currency. Madagascar is very affordable — a great meal costs $5-10, taxis $2-5. ATMs exist in Tana but carry some cash. Many places are cash-only.' },
    { title: '🚗 Getting Around', text: 'Taxis are the main way to get around Antananarivo. Agree on the fare before getting in (no meters). For day trips, hire a driver through your hotel — much safer and more reliable than self-driving.' },
    { title: '🦠 Health & Safety', text: 'Antimalarial medication is recommended. Drink bottled water only. Street food is delicious but choose busy stalls. Antananarivo is generally safe but watch for pickpockets in crowded markets.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-02-27',
      neighborhoods: 'Haute-Ville · Analakely · Isoraka',
      title: 'Arrival — Royal Hill, Markets & Tana After Dark',
      description: "Touch down in Madagascar's capital and immediately feel its energy. Explore the historic upper town, haggle at the sprawling Analakely market, and discover why Antananarivo's nightlife punches well above its weight.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Rova of Antananarivo (Queen\'s Palace)',
              description: 'Start at the highest point in the city — the Rova royal palace complex. Perched atop the central hill, it offers 360° views over Antananarivo\'s colourful, chaotic rooftops. The palace tells the story of the Merina monarchy and Madagascar\'s pre-colonial history.',
              details: [
                '🏛️ Entrance fee ~10,000 MGA (~$2). Guide mandatory but inexpensive',
                '📸 The panoramic views of the city are spectacular — bring your camera',
                '⏰ Open until 5pm — arrive by 3pm for good light'
              ]
            },
            {
              title: 'Analakely Market & Street Life',
              description: 'Descend from the Rova into the bustling Analakely market — the beating heart of Tana. Stalls overflow with vanilla, spices, woven raffia goods, carved wooden lemurs, and tropical fruit. The energy is intoxicating.',
              details: [
                '🛍️ Vanilla pods are a must-buy — Madagascar produces 80% of the world\'s vanilla',
                '🍌 Try fresh tropical fruit — lychees, mangoes, and jackfruit in season',
                '📸 The colourful umbrella-covered stalls make for great photos'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'La Varangue',
              description: 'One of Antananarivo\'s finest restaurants, set in a beautifully restored colonial-era building. French-Malagasy fusion cuisine with dishes like zebu steak, fresh seafood, and exotic fruit desserts.',
              meta: '💰 $$ · 📍 Haute-Ville, near Independence Avenue · Reservations recommended'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Antananarivo Nightlife Crawl',
              description: 'Tana comes alive after dark. Start with rooftop cocktails at Le Lounge (Hotel Colbert), then head to the lively Isoraka neighbourhood where expats and locals mix at bars playing everything from Malagasy salegy music to international hits. End at Cabaret du Glacier or Le Pandora for dancing.',
              details: [
                '🍸 Le Lounge at Hotel Colbert — sophisticated rooftop cocktails with city views',
                '🎵 Isoraka district — the hub of Tana nightlife, walkable cluster of bars',
                '💃 Cabaret du Glacier — legendary Tana nightclub, open late',
                '🎶 Salegy music (Malagasy dance music) is infectious — let the rhythm move you'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Taxis are cheap but harder to find late at night. Ask your hotel to arrange a return pickup or get your driver\'s number.' }
          ]
        }
      ],
      mapPins: [
        { lat: -18.9167, lng: 47.5333, label: 'Rova of Antananarivo', num: 1, cat: 'attraction', desc: 'Historic royal palace with panoramic city views' },
        { lat: -18.9100, lng: 47.5250, label: 'Analakely Market', num: 2, cat: 'attraction', desc: 'Bustling central market — vanilla, crafts, tropical fruit' },
        { lat: -18.9119, lng: 47.5228, label: 'La Varangue', num: 3, cat: 'food', desc: 'Fine French-Malagasy fusion in a colonial setting' },
        { lat: -18.9080, lng: 47.5220, label: 'Hotel Colbert / Le Lounge', num: 4, cat: 'nightlife', desc: 'Rooftop bar with city views — start the evening here' },
        { lat: -18.9050, lng: 47.5200, label: 'Isoraka Nightlife District', num: 5, cat: 'nightlife', desc: 'Cluster of bars and clubs — the heart of Tana after dark' }
      ]
    },
    {
      num: 2,
      date: '2026-02-28',
      neighborhoods: 'Andasibe-Mantadia National Park',
      title: 'Rainforest Day Trip — Indri Lemurs & Ancient Forest',
      description: "Rise early for an unforgettable day trip to Andasibe-Mantadia National Park — home to the largest living lemur, the Indri. Their haunting, whale-like calls echo through the misty rainforest. A family-friendly adventure that will stay with you forever.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive to Andasibe-Mantadia National Park',
              description: 'Depart Tana early (6am recommended) for the 3-hour drive east through the highlands. The journey itself is stunning — terraced rice paddies, red-earth villages, and misty mountains. Stop at roadside stalls for fresh baguettes and coffee.',
              details: [
                '🚗 Hire a driver through your hotel (~$80-100 for the day trip)',
                '🛣️ Route Nationale 2 — paved but winding. Leave early to maximize park time',
                '☕ Stop in Moramanga for breakfast at a local hotely (roadside café)'
              ]
            },
            {
              title: 'Andasibe-Mantadia Guided Rainforest Walk',
              description: 'Enter the park with a local guide and track the famous Indri lemurs. These black-and-white giants sing to each other across the canopy — the sound is otherworldly. You\'ll also spot chameleons, geckos, colourful frogs, and orchids.',
              details: [
                '🦎 Park entrance ~25,000 MGA + guide fee ~20,000 MGA per group',
                '🐒 Indri are the star but you\'ll also see diademed sifaka and brown lemurs',
                '🌺 The rainforest is dripping with orchids and ferns — magical in the mist',
                '👨‍👩‍👧 Very family-friendly — guides adjust pace for all ages'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Vakona Forest Lodge — Lemur Island',
              description: 'After the park, visit nearby Vakona Lodge\'s famous Lemur Island. Here, rescued lemurs roam free on small islands and will hop onto your shoulders for photos. Kids and adults alike lose their minds — it\'s pure joy.',
              details: [
                '🐒 Lemurs will literally jump on you — an unforgettable family photo op',
                '🏝️ Small canoe ride to the island adds to the adventure',
                '💰 ~15,000 MGA entrance. Worth every ariary'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Vakona Forest Lodge Restaurant',
              description: 'Enjoy a Malagasy lunch at the lodge — zebu steak, rice, fresh vegetables, and tropical fruit. The setting is gorgeous, surrounded by rainforest.',
              meta: '💰 $ · 📍 Vakona Forest Lodge, Andasibe'
            }
          ],
          tips: [
            { type: 'tip', text: 'Bring rain gear, insect repellent, and sturdy shoes. The rainforest floor can be slippery. A headlamp is useful if you do a night walk (optional, highly recommended for spotting nocturnal lemurs and chameleons).' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Antananarivo & Chill Night',
              description: 'Drive back to Tana (arrive around 7-8pm). After a big adventure day, keep the evening relaxed. Grab dinner at a casual spot and enjoy a quiet drink at your hotel or a neighbourhood bar.',
              details: [
                '🍺 La Boussole — relaxed French-Malagasy bistro in Isoraka, great for unwinding',
                '🌙 If you have energy, a late-night rum punch at a local bar is the Malagasy way'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'La Boussole',
              description: 'Cosy bistro popular with both locals and expats. Excellent Malagasy dishes, French classics, and cold Three Horses Beer (THB) — the national brew.',
              meta: '💰 $ · 📍 Isoraka, Antananarivo'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -18.9333, lng: 48.4167, label: 'Andasibe-Mantadia National Park', num: 1, cat: 'attraction', desc: 'Rainforest park — home of the singing Indri lemurs' },
        { lat: -18.9280, lng: 48.4250, label: 'Vakona Forest Lodge & Lemur Island', num: 2, cat: 'attraction', desc: 'Rescued lemurs hop on your shoulders — unforgettable' },
        { lat: -18.9280, lng: 48.4250, label: 'Vakona Restaurant', num: 3, cat: 'food', desc: 'Malagasy lunch in a rainforest setting' },
        { lat: -18.9500, lng: 48.2167, label: 'Moramanga', num: 4, cat: 'attraction', desc: 'Midway town — coffee and baguette stop' },
        { lat: -18.9050, lng: 47.5200, label: 'La Boussole', num: 5, cat: 'food', desc: 'Cosy Isoraka bistro for post-adventure dinner' }
      ]
    },
    {
      num: 3,
      date: '2026-03-01',
      neighborhoods: 'Lemurs\' Park · Lake Anosy · Haute-Ville',
      title: 'Lemurs\' Park, Culture & A Final Night Out',
      description: "Your last full day blends a morning with lemurs at the accessible Lemurs' Park just outside the city, afternoon cultural exploration around Lake Anosy and the artisan quarter, and one more unforgettable Tana night out.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Lemurs\' Park',
              description: 'A 30-minute drive west of Tana, this beautifully maintained botanical garden is home to nine species of free-roaming lemurs — including ring-tailed, brown, and bamboo lemurs. Guided walks last about 90 minutes and are perfect for families.',
              details: [
                '🐒 9 lemur species roaming free in a lush botanical garden',
                '🌿 Also home to chameleons, tortoises, and native plants',
                '👶 Very kid-friendly — lemurs are habituated to people',
                '💰 Entrance ~25,000 MGA (~$5) including guided tour'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Café de la Gare',
              description: 'A Tana institution housed in the old Soarano train station. Great coffee, fresh pastries, and Malagasy breakfast dishes in an atmospheric heritage building.',
              meta: '💰 $ · 📍 Soarano, near the old railway station'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Lake Anosy & War Memorial',
              description: 'Stroll around the heart-shaped Lake Anosy, a peaceful green oasis in the middle of the city. The Monument aux Morts on the island honours Malagasy soldiers from World War I. Jacaranda trees bloom purple around the lake (in season).',
              details: [
                '💜 Jacaranda season is October-November, but the lake is lovely year-round',
                '📸 The angel statue on the island is a classic Tana photo'
              ]
            },
            {
              title: 'Digue Market & Artisan Quarter',
              description: 'Browse the Digue artisan market near the city centre for handmade souvenirs — embroidered tablecloths, wooden carvings, gemstones, and woven baskets. This is where locals shop, so prices are fair.',
              details: [
                '🎁 Hand-carved wooden lemurs, baobab trees, and vanilla pods make perfect gifts',
                '💎 Madagascar is famous for sapphires and semi-precious stones',
                '🤝 Gentle bargaining is expected and welcome'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Farewell Dinner & Final Night Out',
              description: 'Celebrate your last night with a special dinner, then hit the town one more time. Tana\'s weekend nightlife is livelier than weeknights — expect live Malagasy music, dancing, and a warm, inclusive atmosphere.',
              details: [
                '🎵 Check if any live salegy or tsapiky music is playing — ask your hotel',
                '💃 Le Pandora or B-Club for dancing until late',
                '🥃 Try local rum (toaka gasy) or Dzama rum — Madagascar\'s finest export'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Sakamanga Restaurant',
              description: 'Iconic Tana restaurant-hotel with eclectic décor, live music some evenings, and a menu spanning Malagasy, French, and Indian Ocean cuisine. A beloved institution and the perfect farewell dinner.',
              meta: '💰 $$ · 📍 Isoraka · Live music some nights — ask when booking'
            }
          ],
          tips: [
            { type: 'tip', text: 'Saturday night is the best night out in Tana. Clubs don\'t really get going until after 11pm. Pace yourself with a long dinner first!' }
          ]
        }
      ],
      mapPins: [
        { lat: -18.9667, lng: 47.4500, label: 'Lemurs\' Park', num: 1, cat: 'attraction', desc: 'Botanical garden with 9 free-roaming lemur species' },
        { lat: -18.9170, lng: 47.5170, label: 'Café de la Gare', num: 2, cat: 'food', desc: 'Heritage café in the old Soarano train station' },
        { lat: -18.9220, lng: 47.5260, label: 'Lake Anosy', num: 3, cat: 'attraction', desc: 'Heart-shaped lake with war memorial and jacarandas' },
        { lat: -18.9130, lng: 47.5240, label: 'Digue Market', num: 4, cat: 'attraction', desc: 'Artisan market — carvings, gemstones, woven goods' },
        { lat: -18.9080, lng: 47.5210, label: 'Sakamanga Restaurant', num: 5, cat: 'food', desc: 'Iconic Tana restaurant with live music and eclectic décor' },
        { lat: -18.9060, lng: 47.5190, label: 'Le Pandora / B-Club', num: 6, cat: 'nightlife', desc: 'Dancing and late-night vibes — Tana\'s best clubs' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$20–40/night', midrange: '$50–100/night', luxury: '$120–250/night' },
    { category: 'Meals (per couple)', budget: '$10–20/day', midrange: '$25–50/day', luxury: '$60–120/day' },
    { category: 'Transport', budget: '$5–15/day', midrange: '$20–40/day', luxury: '$50–100/day (private driver)' },
    { category: 'Activities', budget: '$5–15/day', midrange: '$20–50/day', luxury: '$50–100/day' },
    { category: 'Andasibe Day Trip', budget: '$80–100 (shared)', midrange: '$120–160 (private)', luxury: '$200–300 (luxury)' },
    { category: '3-Night Total (couple)', budget: '$400–700', midrange: '$800–1,500', luxury: '$2,000–4,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Ivato International Airport (TNR) is 16km from the city centre', 'Airport taxi to central Tana costs ~30,000-50,000 MGA ($7-12)', 'Some hotels offer airport transfers — arrange in advance', 'Visa on arrival for most nationalities (~$35 USD)'] },
    { title: '🏨 Where to Stay', items: ['Hôtel Colbert — central, rooftop bar, reliable (midrange-luxury)', 'Sakamanga Hotel — eclectic, great restaurant, backpacker-friendly', 'Carlton Madagascar — upscale, pool, near Anosy lake', 'Isoraka neighbourhood — walkable to nightlife and restaurants'] },
    { title: '🌡️ Weather', items: ['Late February averages 25-28°C (77-82°F) — warm and humid', 'Rainy season: expect afternoon/evening downpours, clear mornings', 'UV is strong — wear sunscreen even on cloudy days', 'Pack layers for cool mornings in the highlands and Andasibe forest'] },
    { title: '💳 Money & Tips', items: ['Malagasy Ariary (MGA): ~4,500 MGA = $1 USD', 'ATMs available in Tana (BFV-SG, BOA) — withdraw in Ariary', 'Cash is king outside the capital — bring enough for day trips', 'Tipping: 10% at restaurants, small tips for guides (~5,000-10,000 MGA)'] },
    { title: '📱 Connectivity', items: ['Buy a Telma or Airtel SIM at the airport for cheap data', 'Coverage is good in Tana, patchy on rural roads', 'WiFi available at most hotels and upscale restaurants', 'Download offline maps — Google Maps works well for Tana'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
