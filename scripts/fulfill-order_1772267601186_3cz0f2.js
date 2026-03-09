const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772267601186_3cz0f2',
  email: 'rm_blakemore@xtra.co.nz',
  destination: 'Tokyo, Kyoto, Osaka',
  startDate: '2026-10-13',
  endDate: '2026-11-02',
  groupSize: 2,
  requests: 'We like fine design and new tecnology'
};

const itineraryData = {
  destination: 'Tokyo, Kyoto & Osaka, Japan',
  countryEmoji: '🇯🇵',
  title: 'Design, Technology & Flavour Across Japan',
  subtitle: '21 days of cutting-edge design, future tech, ancient culture & world-class food for two',
  description: "This itinerary is built for curious minds who love fine design and new technology — woven through Japan's three greatest cities during the stunning autumn foliage season. From teamLab's immersive digital art and Akihabara's neon-lit tech bazaars in Tokyo, to Kyoto's zen temples draped in crimson maples, to Osaka's raucous street-food alleys and avant-garde architecture. Every day balances design museums, technology experiences, cultural immersion, and extraordinary food — Michelin-starred kaiseki, smoky izakayas, perfect ramen, and omakase sushi at intimate counters. October in Japan is magic: comfortable temperatures, fiery autumn colours, and fewer crowds than cherry blossom season.",
  duration: '21 nights',
  dates: 'Oct 13 – Nov 2, 2026',
  budget: '$$$$',
  pace: 'Moderate',
  bestFor: 'Design & Tech Enthusiasts · Foodies · Cultural Explorers',
  highlights: [
    'teamLab Borderless immersive digital art museum',
    'Akihabara deep-dive — retro gaming, electronics, maid cafés',
    'Omakase sushi at a 6-seat Ginza counter',
    'Fushimi Inari shrine at dawn — 10,000 vermilion torii gates',
    'Naoshima Art Island day trip — Tadao Ando architecture + Yayoi Kusama pumpkins',
    'Osaka street food crawl — Dōtonbori, Shinsekai, Kuromon Market',
    'Kyoto autumn foliage at Tōfuku-ji and Arashiyama bamboo grove',
    'Shibuya crossing, Harajuku design shops & Omotesandō architecture',
    '21_21 DESIGN SIGHT and the National Art Center, Tokyo',
    'Nara deer park and ancient wooden temple architecture'
  ],

  essentials: [
    { title: '🍂 Autumn Season', text: 'Mid-October to early November is peak autumn in Japan. Expect 15-22°C in Tokyo/Osaka, slightly cooler in Kyoto. Foliage peaks late October through mid-November. Pack layers and a light jacket for temple visits and evening walks.' },
    { title: '🚄 Getting Around', text: 'A 21-day Japan Rail Pass is essential — covers bullet trains between cities, JR local lines, and even the ferry to Miyajima. Supplement with IC cards (Suica/ICOCA) for subway, buses, and convenience stores. Reserve Shinkansen seats via the SmartEX app.' },
    { title: '💴 Money & Tipping', text: 'Japan is still partly cash-based — carry ¥10,000-20,000 daily for small restaurants, temples, and vending machines. 7-Eleven ATMs accept international cards. Tipping is not customary and can be considered rude.' },
    { title: '🏨 Hotels', text: 'Book design-forward hotels: Trunk Hotel or Muji Hotel in Tokyo, Ace Hotel Kyoto or good machiya (townhouse) stays in Kyoto, W Osaka or Conrad Osaka. Book Michelin restaurants 1-2 months ahead via Tableall, Omakase, or concierge.' },
    { title: '📱 Connectivity', text: 'Rent a pocket WiFi at the airport or buy an eSIM (Ubigi, Airalo). Free WiFi is limited outside hotels and konbini. Google Maps works flawlessly for transit navigation.' },
    { title: '🎌 Design & Tech Tips', text: 'Visit Tsutaya Books in Daikanyama for curated design books. Hit Ginza Six and KITTE for Japanese design retail. Akihabara is best on weekdays (less crowded). teamLab tickets sell out — book 2-3 weeks ahead.' }
  ],

  days: [
    // ===== TOKYO: Days 1-9 =====
    {
      num: 1,
      date: '2026-10-13',
      neighborhoods: 'Shinjuku · Kabukichō',
      title: 'Arrival & Neon-Lit First Night',
      description: "Arrive at Narita or Haneda, settle into your hotel, and ease into Tokyo with a sunset walk through Shinjuku's electric streets. The sensory overload of Kabukichō's neon canyon and a perfect bowl of ramen set the tone.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive & Check In',
              description: 'Take the Narita Express or Haneda monorail to central Tokyo. Check into your design hotel — Trunk Hotel in Shibuya or Muji Hotel in Ginza are excellent choices for design lovers.',
              details: [
                '🚃 Narita Express: 60 min to Shinjuku/Shibuya, covered by JR Pass',
                '🏨 Trunk Hotel Shibuya — local materials, community-focused design',
                '🏨 Muji Hotel Ginza — minimalist perfection above the Muji flagship'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shinjuku & Kabukichō Neon Walk',
              description: "Wander through Shinjuku's west exit camera district, then plunge into the neon-drenched alleys of Kabukichō. Cross to Golden Gai — a labyrinth of 200+ tiny bars, each seating 6-8 people.",
              details: [
                '📸 Kabukichō\'s main gate is iconic at night — the new Godzilla head on the Toho building adds drama',
                '🍺 Golden Gai: pick bars with English signs if you\'re not confident in Japanese. Each has a unique theme.',
                '💡 Tip: many Golden Gai bars charge a ¥500-1000 seating fee — totally normal'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Fuunji (風雲児)',
              description: 'Legendary tsukemen (dipping ramen) in Shinjuku. Rich, creamy fish-pork broth with thick noodles. Queue-worthy.',
              meta: '💰 ¥1,000-1,500 · 📍 Shinjuku, near south exit · Queue 20-40 min'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6896, lng: 139.7006, label: 'Shinjuku Station', num: 1, cat: 'transport', desc: 'World\'s busiest station — your gateway to Tokyo' },
        { lat: 35.6948, lng: 139.7034, label: 'Kabukichō', num: 2, cat: 'attraction', desc: 'Neon entertainment district' },
        { lat: 35.6934, lng: 139.7037, label: 'Golden Gai', num: 3, cat: 'nightlife', desc: '200+ micro-bars in narrow alleys' },
        { lat: 35.6889, lng: 139.6997, label: 'Fuunji', num: 4, cat: 'food', desc: 'Famous tsukemen ramen' }
      ]
    },
    {
      num: 2,
      date: '2026-10-14',
      neighborhoods: 'Odaiba · Toyosu · Ginza',
      title: 'teamLab, Toyosu Market & Ginza Design',
      description: "Start with the mind-bending digital art of teamLab Borderless, fuel up with the freshest sushi at Toyosu's inner market, then explore Ginza's architectural showpieces and design flagships.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'teamLab Borderless',
              description: 'One of the world\'s most ambitious digital art museums — immersive rooms of flowing light, water, and flowers that respond to your movement. A must for anyone who loves design and technology.',
              details: [
                '🎫 Book tickets online 2-3 weeks ahead — sells out daily',
                '⏰ Go at opening (10am) for thinner crowds and better photos',
                '👟 Wear comfortable shoes — you\'ll walk through water installations',
                '📱 No tripods allowed, but phone/camera photos are encouraged'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ginza Architecture & Design Walk',
              description: 'Ginza is an open-air museum of contemporary architecture. Walk the main boulevard admiring buildings by Renzo Piano (Hermès), Kengo Kuma (Tiffany), and Yoshio Taniguchi. Visit Ginza Six for curated Japanese design brands and the rooftop garden.',
              details: [
                '🏛️ GINZA SIX — Tsutaya bookstore inside, curated design retail, rooftop zen garden',
                '🏛️ KITTE building (by JP Tower) — beautiful atrium, Japanese craft shops',
                '🏛️ Mikimoto Ginza 2 — Toyo Ito\'s organic façade is architecture photography gold',
                '📸 Walk from Ginza 4-chome crossing south — every block has an architectural gem'
              ]
            }
          ],
          meals: [
            {
              type: '🍣 Lunch',
              name: 'Sushi Dai (Toyosu Market)',
              description: 'Legendary sushi counter inside Toyosu fish market. The omakase set features the morning\'s freshest catch — tuna, uni, ikura, and seasonal fish.',
              meta: '💰 ¥4,000-5,000 · 📍 Toyosu Market · Queue from 5am for opening'
            },
            {
              type: '🍷 Dinner',
              name: 'Ginza Kojyu',
              description: 'Two-Michelin-star kaiseki in Ginza. Exquisite multi-course Japanese haute cuisine in a serene, intimate setting. A masterclass in Japanese culinary design.',
              meta: '💰 ¥¥¥¥ (¥30,000+/person) · 📍 Ginza · Reserve 1-2 months ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6256, lng: 139.7841, label: 'teamLab Borderless', num: 1, cat: 'attraction', desc: 'Immersive digital art museum' },
        { lat: 35.6426, lng: 139.7810, label: 'Toyosu Market', num: 2, cat: 'food', desc: 'Tokyo\'s main fish market — sushi breakfast' },
        { lat: 35.6699, lng: 139.7638, label: 'Ginza Six', num: 3, cat: 'shopping', desc: 'Luxury design retail and rooftop garden' },
        { lat: 35.6812, lng: 139.7671, label: 'KITTE', num: 4, cat: 'shopping', desc: 'JP Tower — Japanese craft and design shops' },
        { lat: 35.6716, lng: 139.7637, label: 'Ginza Kojyu', num: 5, cat: 'food', desc: 'Two-Michelin-star kaiseki' }
      ]
    },
    {
      num: 3,
      date: '2026-10-15',
      neighborhoods: 'Harajuku · Omotesandō · Shibuya',
      title: 'Harajuku Design Culture & Shibuya Crossing',
      description: "Dive into Tokyo's design heartland. Omotesandō's tree-lined boulevard showcases architecture by Tadao Ando, SANAA, and Herzog & de Meuron. Harajuku's backstreets reveal cutting-edge independent design. End at the world's most famous intersection.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Omotesandō Architecture Walk',
              description: 'Walk the \"Champs-Élysées of Tokyo\" — every luxury flagship is a commissioned architectural masterpiece. Tadao Ando\'s Omotesando Hills, the Prada building by Herzog & de Meuron (diamond-lattice glass), and Toyo Ito\'s Tod\'s building.',
              details: [
                '🏛️ Prada Aoyama — crystalline diamond glass by Herzog & de Meuron',
                '🏛️ Omotesando Hills — Tadao Ando\'s spiraling interior ramp',
                '🏛️ Tod\'s — Toyo Ito\'s tree-branch concrete façade',
                '🛍️ Comme des Garçons, Issey Miyake, and Undercover all have flagship stores here'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Harajuku Backstreets & Cat Street',
              description: 'Leave the main boulevard for the narrow backstreets. Cat Street runs parallel — it\'s lined with independent Japanese designer boutiques, vintage shops, and concept stores.',
              details: [
                '🛍️ Design Festa Gallery — rotating avant-garde art exhibitions, free entry',
                '🛍️ Laforet Harajuku — multi-floor fashion building with Japanese indie brands',
                '🍦 Stop at a Harajuku crêpe stand — the original Japanese street dessert'
              ]
            },
            {
              title: 'Shibuya Crossing & Shibuya Sky',
              description: 'Experience the world\'s most famous scramble crossing, then ascend to Shibuya Sky — the open-air observation deck atop Shibuya Scramble Square for a 360° view of Tokyo.',
              details: [
                '📸 Best Shibuya Crossing photo: from the Starbucks 2F window or the Mag\'s Park rooftop',
                '🏛️ Shibuya Sky — book online, go at sunset for golden-hour views',
                '🐕 Pay respects to the Hachikō statue outside the station'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Afuri (Harajuku)',
              description: 'Yuzu shio ramen — a lighter, citrus-forward ramen that\'s a refreshing change from heavy tonkotsu. Beautiful minimalist restaurant design.',
              meta: '💰 ¥1,200-1,800 · 📍 Harajuku/Omotesandō'
            },
            {
              type: '🍺 Dinner',
              name: 'Shirubee (Shibuya)',
              description: 'Lively standing izakaya in Shibuya\'s Nonbei Yokochō (Drunkard\'s Alley). Grilled skewers, cold beer, and shoulder-to-shoulder locals. Authentic Tokyo nightlife.',
              meta: '💰 ¥2,000-4,000 · 📍 Nonbei Yokochō, Shibuya'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6654, lng: 139.7100, label: 'Omotesandō', num: 1, cat: 'attraction', desc: 'Architecture boulevard — Ando, Ito, Herzog & de Meuron' },
        { lat: 35.6702, lng: 139.7030, label: 'Harajuku / Cat Street', num: 2, cat: 'shopping', desc: 'Independent designer boutiques and street fashion' },
        { lat: 35.6595, lng: 139.7004, label: 'Shibuya Crossing', num: 3, cat: 'attraction', desc: 'World\'s busiest pedestrian scramble' },
        { lat: 35.6584, lng: 139.7023, label: 'Shibuya Sky', num: 4, cat: 'attraction', desc: '360° observation deck, stunning at sunset' },
        { lat: 35.6646, lng: 139.7092, label: 'Afuri Ramen', num: 5, cat: 'food', desc: 'Yuzu shio ramen — light and citrusy' }
      ]
    },
    {
      num: 4,
      date: '2026-10-16',
      neighborhoods: 'Roppongi · Midtown · Aoyama',
      title: 'Design Museums & Art Triangle',
      description: "Tokyo's art and design triangle: 21_21 DESIGN SIGHT (directed by Issey Miyake and Tadao Ando), the Mori Art Museum high above Roppongi, and the undulating National Art Center by Kisho Kurokawa. A day for design lovers.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: '21_21 DESIGN SIGHT',
              description: 'Japan\'s premier design museum, founded by Issey Miyake and housed in a Tadao Ando concrete masterpiece sunken into Tokyo Midtown Garden. Exhibitions explore the intersection of design, technology, and daily life.',
              details: [
                '🏛️ The building itself is a work of art — 80% underground with a folded-steel roof',
                '🎨 Exhibitions rotate every 3-4 months — check the website for current show',
                '🌳 Tokyo Midtown Garden surrounding it is beautiful for a morning stroll'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'National Art Center, Tokyo',
              description: 'Kisho Kurokawa\'s final masterpiece — a massive undulating glass curtain-wall building with no permanent collection. Instead, rotating exhibitions span contemporary art, design, and architecture.',
              details: [
                '🏛️ The wavy glass façade is mesmerizing — best photographed from outside in afternoon light',
                '☕ The Brasserie Paul Bocuse inside has iconic inverted-cone dining pods',
                '🎨 Often hosts major shows: Matisse, teamLab collaborations, Japanese design exhibitions'
              ]
            },
            {
              title: 'Mori Art Museum & Tokyo City View',
              description: 'Contemporary art museum on the 53rd floor of Roppongi Hills. The ticket includes Tokyo City View — an observation deck with stunning views. Night visits are especially atmospheric.',
              details: [
                '🌃 Open until 10pm on most nights — go at sunset for the view transition',
                '🎨 The Mori collection focuses on contemporary Asian art',
                '📸 The outdoor Sky Deck is the highest open-air observation point in Tokyo'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Tsurutontan (Roppongi)',
              description: 'Famous for oversized udon bowls served in comically large ceramic dishes. Creative fusion udon — try the carbonara udon or mentaiko cream.',
              meta: '💰 ¥1,500-2,500 · 📍 Roppongi'
            },
            {
              type: '🍷 Dinner',
              name: 'Florilège (Aoyama)',
              description: 'Two-Michelin-star innovative French-Japanese. Chef Hiroyasu Kawate creates stunning courses using Japanese ingredients with French technique. Open kitchen theatre.',
              meta: '💰 ¥¥¥¥ (¥20,000+/person) · 📍 Aoyama · Reserve ahead via Tableall'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6653, lng: 139.7310, label: '21_21 DESIGN SIGHT', num: 1, cat: 'attraction', desc: 'Issey Miyake + Tadao Ando design museum' },
        { lat: 35.6653, lng: 139.7263, label: 'National Art Center', num: 2, cat: 'attraction', desc: 'Kisho Kurokawa\'s glass curtain-wall masterpiece' },
        { lat: 35.6604, lng: 139.7293, label: 'Mori Art Museum', num: 3, cat: 'attraction', desc: '53F contemporary art + city views' },
        { lat: 35.6671, lng: 139.7256, label: 'Florilège', num: 4, cat: 'food', desc: 'Two-star French-Japanese innovation' },
        { lat: 35.6630, lng: 139.7316, label: 'Tokyo Midtown', num: 5, cat: 'shopping', desc: 'Design retail and Tadao Ando garden' }
      ]
    },
    {
      num: 5,
      date: '2026-10-17',
      neighborhoods: 'Akihabara · Ueno · Yanaka',
      title: 'Akihabara Tech & Old-Town Tokyo',
      description: "Morning deep-dive into Akihabara's neon-lit tech paradise — retro gaming, cutting-edge electronics, anime culture, and robot restaurants. Afternoon contrast: the quiet old-town charm of Yanaka and Ueno's world-class museums.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Akihabara Deep Dive',
              description: 'Tokyo\'s \"Electric Town\" — a sensory overload of electronics shops, retro game arcades, anime stores, and tech gadgets. From vintage synthesizers to the latest Japanese gadgets unavailable anywhere else.',
              details: [
                '🕹️ Super Potato — retro gaming heaven across 5 floors (Famicom, PC Engine, Neo Geo)',
                '🔌 Yodobashi Camera Akihabara — Japan\'s biggest electronics megastore (9 floors)',
                '🤖 Try a maid café for the surreal cultural experience',
                '🎮 Sega, Taito, and Hey! arcade — classic rhythm games and UFO catchers',
                '💡 Radio Kaikan building — tech gadgets, model kits, and rare collectibles'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ueno Park & Tokyo National Museum',
              description: 'Japan\'s oldest public park, home to world-class museums. The Tokyo National Museum houses the finest collection of Japanese art and antiquities — samurai armour, ukiyo-e prints, Buddhist sculpture.',
              details: [
                '🏛️ Tokyo National Museum — the Honkan (Japanese Gallery) is essential',
                '🏛️ Gallery of Hōryū-ji Treasures — Yoshio Taniguchi\'s serene minimalist building',
                '🍁 Ueno Park begins showing autumn colour by mid-October'
              ]
            },
            {
              title: 'Yanaka Old Town Stroll',
              description: 'One of the few Tokyo neighbourhoods that survived WWII bombing. Narrow lanes, wooden houses, neighbourhood cats, traditional craft shops, and a sunset viewpoint from Yanaka Cemetery.',
              details: [
                '🐱 Yanaka is famous for its cats — look for cat-themed shops and real neighbourhood cats',
                '🛍️ Yanaka Ginza shopping street — old-school snack shops and craftspeople',
                '🌅 The \"Yūyake Dandan\" (Sunset Stairs) face due west — gorgeous at golden hour'
              ]
            }
          ],
          meals: [
            {
              type: '🍛 Lunch',
              name: 'Kanda Matsuya',
              description: 'Soba institution since 1884. Hand-cut buckwheat noodles served on bamboo trays. Simple, pure, and deeply Japanese.',
              meta: '💰 ¥1,000-1,800 · 📍 Kanda (between Akihabara and Ueno)'
            },
            {
              type: '🍺 Dinner',
              name: 'Hantei (Yanaka)',
              description: 'Kushiage (deep-fried skewers) served in a stunning 3-story wooden Meiji-era building. Multi-course set with seasonal vegetables and seafood.',
              meta: '💰 ¥4,000-6,000 · 📍 Yanaka/Nezu · The building alone is worth visiting'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6984, lng: 139.7714, label: 'Akihabara', num: 1, cat: 'attraction', desc: 'Electric Town — tech, gaming, anime paradise' },
        { lat: 35.7002, lng: 139.7726, label: 'Super Potato', num: 2, cat: 'shopping', desc: 'Retro gaming store — 5 floors of nostalgia' },
        { lat: 35.7189, lng: 139.7767, label: 'Tokyo National Museum', num: 3, cat: 'attraction', desc: 'Japan\'s finest art and antiquities' },
        { lat: 35.7257, lng: 139.7674, label: 'Yanaka Ginza', num: 4, cat: 'attraction', desc: 'Old-town shopping street and sunset stairs' },
        { lat: 35.7070, lng: 139.7691, label: 'Kanda Matsuya', num: 5, cat: 'food', desc: 'Historic soba noodles since 1884' }
      ]
    },
    {
      num: 6,
      date: '2026-10-18',
      neighborhoods: 'Daikanyama · Nakameguro · Shimokitazawa',
      title: 'Curated Cool — Books, Coffee & Indie Design',
      description: "Tokyo's most stylish residential neighbourhoods. Daikanyama T-Site is a design book lover's paradise. Nakameguro's canal is lined with boutiques. Shimokitazawa is Tokyo's indie-music, vintage-fashion, and third-wave coffee capital.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Daikanyama T-Site (Tsutaya Books)',
              description: 'One of the world\'s most beautiful bookstores — three interconnected buildings wrapped in interlocking T-shaped lattice by Klein Dytham architecture. The design and art sections are extraordinary.',
              details: [
                '📚 The architecture/design book section is curated by experts — you\'ll want to buy everything',
                '☕ Anjin lounge upstairs — gorgeous reading café with vinyl and vintage magazines',
                '🏛️ The building won numerous architecture awards — walk around all three pavilions'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nakameguro Canal Walk',
              description: 'Follow the Meguro River canal — famous for cherry blossoms in spring, but equally charming in autumn with amber-leaved zelkova trees. Lined with independent boutiques, galleries, and cafés.',
              details: [
                '🛍️ 1LDK — curated lifestyle store with Japanese and international design',
                '🛍️ Cow Books — tiny curated used bookshop by the canal',
                '☕ Onibus Coffee — one of Tokyo\'s best third-wave roasters'
              ]
            },
            {
              title: 'Shimokitazawa',
              description: 'Tokyo\'s bohemian village — vintage clothing shops, tiny live-music venues, craft breweries, and some of the city\'s best coffee. Recently redeveloped with the Shimokitazawa railway complex (Bonus Track).',
              details: [
                '🎵 Shimokitazawa has 20+ live-music venues — check listings for shows tonight',
                '☕ Bear Pond Espresso — legendary (and slightly grumpy) espresso bar',
                '🛍️ Bonus Track — new micro-village of independent shops and food stalls',
                '👕 Dozens of vintage shops — Japanese vintage pricing is still reasonable'
              ]
            }
          ],
          meals: [
            {
              type: '🍳 Brunch',
              name: 'Ivy Place (Daikanyama)',
              description: 'Airy garden restaurant inside Daikanyama T-Site complex. Beautiful brunch with Japanese-Western fusion dishes.',
              meta: '💰 ¥2,000-3,500 · 📍 Daikanyama T-Site'
            },
            {
              type: '🍺 Dinner',
              name: 'Shimokitazawa Izakaya Hopping',
              description: 'No single restaurant — instead, hop between 2-3 tiny izakayas in the backstreets. Grilled chicken (yakitori), fried gyoza, cold beer. This is how locals eat.',
              meta: '💰 ¥3,000-5,000 total · 📍 Shimokitazawa backstreets'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6498, lng: 139.7028, label: 'Daikanyama T-Site', num: 1, cat: 'attraction', desc: 'World\'s most beautiful bookstore' },
        { lat: 35.6441, lng: 139.6987, label: 'Nakameguro Canal', num: 2, cat: 'attraction', desc: 'Boutique-lined canal walk' },
        { lat: 35.6610, lng: 139.6683, label: 'Shimokitazawa', num: 3, cat: 'attraction', desc: 'Bohemian vintage and live-music village' },
        { lat: 35.6609, lng: 139.6671, label: 'Bear Pond Espresso', num: 4, cat: 'food', desc: 'Legendary espresso bar' },
        { lat: 35.6500, lng: 139.7035, label: 'Ivy Place', num: 5, cat: 'food', desc: 'Garden brunch at T-Site' }
      ]
    },
    {
      num: 7,
      date: '2026-10-19',
      neighborhoods: 'Asakusa · Sumida · Ryōgoku',
      title: 'Old Edo — Temples, Craft & Sumo',
      description: "Step back to Edo-period Tokyo. Sensō-ji temple at dawn, traditional craft shopping on Kappabashi (\"Kitchen Town\" — the knife district), and the Sumida Hokusai Museum's bold aluminium architecture.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sensō-ji Temple at Sunrise',
              description: 'Tokyo\'s oldest temple (founded 645 AD) is magical before the crowds. Walk through the massive Kaminarimon gate, browse Nakamise-dōri\'s traditional craft stalls, and explore the main hall and five-story pagoda.',
              details: [
                '⏰ Arrive by 6:30am for peaceful photos without crowds',
                '🛍️ Nakamise-dōri sells traditional crafts, rice crackers, and handmade fans',
                '📸 The pagoda reflected in the incense burner smoke is an iconic shot'
              ]
            },
            {
              title: 'Kappabashi-dōri (Kitchen Town)',
              description: 'A full street of kitchen supply stores — professional Japanese knives, ceramic tableware, lacquerware, and those hyper-realistic plastic food samples. Design lovers will spend hours here.',
              details: [
                '🔪 Kama Asa — knife shop since 1908, expert English-speaking staff',
                '🍽️ Ganso Shokuhin Sample-ya — make your own plastic food replica (¥2,500)',
                '🏺 Beautiful handmade ceramics from ¥500 — great souvenirs'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Sumida Hokusai Museum',
              description: 'Dedicated to Katsushika Hokusai (of \"The Great Wave\" fame). The building by Kazuyo Sejima (SANAA) is a gleaming aluminium cube with angled slits — as much an artwork as its contents.',
              details: [
                '🏛️ Kazuyo Sejima\'s mirrored aluminium cube is stunning from every angle',
                '🎨 Rotating exhibitions of Hokusai\'s woodblock prints and manga',
                '📍 Walk along the Sumida River afterward — good Tokyo Skytree views'
              ]
            }
          ],
          meals: [
            {
              type: '🍡 Lunch',
              name: 'Asakusa street food',
              description: 'Graze through Asakusa: freshly grilled senbei (rice crackers), melon pan (sweet bread), ningyo-yaki (cake-filled figures), and matcha soft-serve.',
              meta: '💰 ¥500-1,500 · 📍 Nakamise-dōri & side streets'
            },
            {
              type: '🍲 Dinner',
              name: 'Chanko Tomoegata (Ryōgoku)',
              description: 'Chanko-nabe — the hearty stew that fuels sumo wrestlers. Enormous pot of chicken, tofu, vegetables in rich broth. Ryōgoku is the sumo district.',
              meta: '💰 ¥3,000-5,000 · 📍 Ryōgoku (sumo district)'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: 'Sensō-ji Temple', num: 1, cat: 'attraction', desc: 'Tokyo\'s oldest temple (645 AD)' },
        { lat: 35.7118, lng: 139.7854, label: 'Kappabashi-dōri', num: 2, cat: 'shopping', desc: 'Kitchen Town — knives, ceramics, plastic food' },
        { lat: 35.6961, lng: 139.8043, label: 'Sumida Hokusai Museum', num: 3, cat: 'attraction', desc: 'Sejima\'s aluminium cube — Hokusai prints' },
        { lat: 35.6967, lng: 139.7940, label: 'Ryōgoku', num: 4, cat: 'attraction', desc: 'Sumo district and chanko-nabe restaurants' },
        { lat: 35.7105, lng: 139.7966, label: 'Kaminarimon Gate', num: 5, cat: 'attraction', desc: 'Iconic red lantern gate to Sensō-ji' }
      ]
    },
    {
      num: 8,
      date: '2026-10-20',
      neighborhoods: 'Meiji Shrine · Yoyogi · Ebisu',
      title: 'Forest Shrine, Yoyogi Park & Beer Museum',
      description: "A breather day. Morning walk through Meiji Shrine's ancient forest (150,000 trees in the heart of Tokyo), relax in Yoyogi Park watching street performers, then explore the Yebisu Beer Museum and the Tokyo Photographic Art Museum.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Meiji Shrine (Meiji Jingū)',
              description: 'A Shintō shrine set in a 170-acre forest — feels impossible that this much nature exists minutes from Harajuku. Walk the gravel paths beneath towering camphor trees.',
              details: [
                '⛩️ Enter from the Harajuku gate through the massive torii',
                '🌳 The forest was planted in 1920 — now has 120,000 trees of 365 species',
                '📿 Write a wish on an ema (wooden plaque) — ¥500',
                '🍁 By mid-October, the shrine forest shows early autumn colour'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Yoyogi Park & People Watching',
              description: 'Adjacent to Meiji Shrine — Tokyo\'s Central Park equivalent. Weekend rockabilly dancers, musicians, and cosplayers create a living street performance.',
              details: [
                '🎸 Rockabilly dancers gather near Harajuku entrance on Sundays',
                '🍁 Ginkgo trees start turning gold in October — beautiful park stroll',
                '🛍️ Walk through to nearby Tomigaya — a quiet foodie neighbourhood'
              ]
            },
            {
              title: 'Ebisu: Beer Museum & Photography Museum',
              description: 'Yebisu Beer Museum traces the history of Japan\'s oldest beer brand with a tasting room. Next door, the Tokyo Photographic Art Museum hosts excellent exhibitions in a calm, design-conscious building.',
              details: [
                '🍺 Yebisu Beer Museum — ¥500 for tour + 2 tastings',
                '📸 Tokyo Photographic Art Museum — rotating exhibitions, usually excellent',
                '🏛️ Yebisu Garden Place — pleasant plaza with European-style architecture'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Afuri (Ebisu)',
              description: 'Another outpost of the beloved yuzu shio ramen. The Ebisu location has a great atmosphere and less queue than Harajuku.',
              meta: '💰 ¥1,200-1,800 · 📍 Ebisu'
            },
            {
              type: '🍷 Dinner',
              name: 'Den (Jimbocho)',
              description: 'One-Michelin-star Japanese innovation by Zaiyu Hasegawa. Playful, creative kaiseki with humour — the \"Den-tucky Fried Chicken\" and \"Dentist\" dessert are legendary.',
              meta: '💰 ¥¥¥ (¥15,000-20,000) · 📍 Jimbocho · Reserve via Omakase/Tableall'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6764, lng: 139.6993, label: 'Meiji Shrine', num: 1, cat: 'attraction', desc: 'Shintō shrine in 170-acre ancient forest' },
        { lat: 35.6716, lng: 139.6950, label: 'Yoyogi Park', num: 2, cat: 'attraction', desc: 'Tokyo\'s Central Park — performers and autumn colour' },
        { lat: 35.6465, lng: 139.7133, label: 'Yebisu Beer Museum', num: 3, cat: 'attraction', desc: 'Beer history and tastings' },
        { lat: 35.6468, lng: 139.7139, label: 'Tokyo Photographic Art Museum', num: 4, cat: 'attraction', desc: 'Excellent rotating photography exhibitions' },
        { lat: 35.6953, lng: 139.7564, label: 'Den', num: 5, cat: 'food', desc: 'Playful one-star kaiseki' }
      ]
    },
    {
      num: 9,
      date: '2026-10-21',
      neighborhoods: 'Tsukiji Outer Market · Nihonbashi · Tokyo Station',
      title: 'Morning Market, Coredo & Shinkansen to Kyoto',
      description: "Last Tokyo morning — explore Tsukiji's surviving outer market for a street-food breakfast, visit Nihonbashi's beautifully restored Coredo Muromachi (Japanese craft retail), then catch the Shinkansen to Kyoto.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tsukiji Outer Market',
              description: 'While the inner wholesale market moved to Toyosu, the outer market remains — a vibrant maze of 400+ stalls selling fresh seafood, tamagoyaki (rolled omelette), oysters, and wagyu-on-a-stick.',
              details: [
                '🍣 Grab sushi for breakfast — many stalls open by 7am',
                '🥚 Yamacho — famous for thick, sweet tamagoyaki on a stick',
                '🔪 Several knife shops here too — compare with Kappabashi'
              ]
            },
            {
              title: 'Nihonbashi & Coredo Muromachi',
              description: 'Tokyo\'s historic commercial centre, beautifully revived. Coredo Muromachi is a complex of shops showcasing the best of Japanese craft and design — ceramics, textiles, knives, stationery.',
              details: [
                '🏛️ Nihonbashi Bridge — original Edo-period starting point for all Japan\'s roads',
                '🛍️ Coredo Muromachi Terrace — curated Japanese design shops',
                '🛍️ Nihonbashi Takashimaya — classic department store with incredible basement food hall'
              ]
            }
          ],
          meals: [
            {
              type: '🍣 Breakfast',
              name: 'Tsukiji street food',
              description: 'Graze through the outer market: uni (sea urchin) cups, grilled scallops, tamagoyaki, fresh oysters, and melon.',
              meta: '💰 ¥2,000-4,000 · 📍 Tsukiji Outer Market · Best 7-10am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shinkansen to Kyoto',
              description: 'Board the Nozomi bullet train from Tokyo Station. Sit on the right side (seats E/D) for Mount Fuji views on a clear day. The journey takes 2 hours 15 minutes.',
              details: [
                '🚄 Nozomi: 2h15min Tokyo→Kyoto. Note: Nozomi is NOT covered by JR Pass — take Hikari (2h40min) instead',
                '🗻 Mt Fuji appears ~40 min after departure, right side',
                '🍱 Buy an ekiben (station bento) at Tokyo Station — the Gransta underground has 100+ options'
              ]
            },
            {
              title: 'Check In & Evening Walk: Gion',
              description: 'Arrive in Kyoto, check into your hotel or machiya (traditional townhouse), and take an evening stroll through Gion — the geisha district. If you\'re lucky, you may spot a maiko (apprentice geisha) hurrying between appointments.',
              details: [
                '🏨 Ace Hotel Kyoto — excellent design hotel in a Kengo Kuma-renovated building',
                '🏘️ Or stay in a machiya — beautifully restored wooden townhouses',
                '🎭 Gion\'s Hanami-koji street is most atmospheric after 6pm'
              ]
            }
          ],
          meals: [
            {
              type: '🍶 Dinner',
              name: 'Gion Nishi (Gion)',
              description: 'Intimate kappo (counter-style) kaiseki in the heart of Gion. Watch the chef prepare each course. Seasonal autumn ingredients: matsutake mushroom, sanma (Pacific saury), persimmon.',
              meta: '💰 ¥¥¥ (¥12,000-18,000) · 📍 Gion, Kyoto'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6654, lng: 139.7707, label: 'Tsukiji Outer Market', num: 1, cat: 'food', desc: 'Street food market — sushi, tamagoyaki, oysters' },
        { lat: 35.6842, lng: 139.7745, label: 'Coredo Muromachi', num: 2, cat: 'shopping', desc: 'Curated Japanese craft and design' },
        { lat: 35.6812, lng: 139.7671, label: 'Tokyo Station', num: 3, cat: 'transport', desc: 'Shinkansen departure — buy ekiben here' },
        { lat: 35.0039, lng: 135.7756, label: 'Gion', num: 4, cat: 'attraction', desc: 'Geisha district — atmospheric evening walk' },
        { lat: 35.0044, lng: 135.7735, label: 'Gion Nishi', num: 5, cat: 'food', desc: 'Intimate kappo kaiseki' }
      ]
    },

    // ===== KYOTO: Days 10-16 =====
    {
      num: 10,
      date: '2026-10-22',
      neighborhoods: 'Fushimi · Higashiyama · Kiyomizu',
      title: 'Fushimi Inari at Dawn & Higashiyama Temple Trail',
      description: "The iconic Kyoto day: thousands of vermilion torii gates at Fushimi Inari, then the atmospheric Higashiyama walking trail connecting Kiyomizu-dera, ancient alleyways, and moss-covered temples.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Fushimi Inari Shrine at Dawn',
              description: '10,000 vermilion torii gates climbing through a forest up Mount Inari. Go at sunrise (6am) and you\'ll have the lower trails nearly to yourself. The full loop takes 2-3 hours.',
              details: [
                '⏰ Arrive by 6am — by 9am it\'s packed with tour groups',
                '⛩️ The first 30 minutes of gates are the most densely packed and photogenic',
                '🦊 Fox statues (kitsune) guard the shrine — Inari\'s messenger',
                '🥾 Full mountain loop: 2-3 hours, moderate fitness required'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Higashiyama Walking Trail',
              description: 'Walk the atmospheric route from Kiyomizu-dera south through narrow stone-paved lanes (Sannen-zaka and Ninen-zaka), past wooden tea houses, to Kodai-ji temple and Maruyama Park.',
              details: [
                '🏯 Kiyomizu-dera — the massive wooden stage offers panoramic views of Kyoto',
                '🛍️ Sannen-zaka — traditional shops selling ceramics, fans, and matcha sweets',
                '🍵 Stop at a tea house for matcha and wagashi (traditional sweets)',
                '🍁 Early autumn colour may be visible on the temple grounds'
              ]
            }
          ],
          meals: [
            {
              type: '🍵 Lunch',
              name: 'Omen (Gion)',
              description: 'Handmade udon noodles in a traditional wooden townhouse. The namesake "omen" set comes with an array of vegetables to dip into hot broth.',
              meta: '💰 ¥1,500-2,500 · 📍 Gion, near Kodai-ji'
            },
            {
              type: '🍷 Dinner',
              name: 'Gion Sasaki',
              description: 'Three-Michelin-star kaiseki by the charismatic Chef Sasaki. Expect exquisite seasonal courses served with warmth and humour — matsutake dobin-mushi, grilled sanma, autumn persimmon.',
              meta: '💰 ¥¥¥¥ (¥35,000+) · 📍 Gion · Reserve 2+ months ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari', num: 1, cat: 'attraction', desc: '10,000 vermilion torii gates' },
        { lat: 34.9949, lng: 135.7850, label: 'Kiyomizu-dera', num: 2, cat: 'attraction', desc: 'Wooden stage temple with city views' },
        { lat: 34.9980, lng: 135.7810, label: 'Sannen-zaka', num: 3, cat: 'attraction', desc: 'Historic stone-paved lanes' },
        { lat: 34.9998, lng: 135.7811, label: 'Kodai-ji', num: 4, cat: 'attraction', desc: 'Zen temple with bamboo grove' },
        { lat: 35.0042, lng: 135.7749, label: 'Gion Sasaki', num: 5, cat: 'food', desc: 'Three-Michelin-star kaiseki' }
      ]
    },
    {
      num: 11,
      date: '2026-10-23',
      neighborhoods: 'Arashiyama · Sagano',
      title: 'Bamboo, Monkeys & River Boats',
      description: "Western Kyoto's nature playground. Walk through the towering Arashiyama Bamboo Grove, visit the hilltop Iwatayama Monkey Park, explore the exquisite Tenryū-ji zen garden, and ride the Hozu River scenic boat down the gorge.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Arashiyama Bamboo Grove',
              description: 'A cathedral of soaring bamboo stalks filtering green light. Arrive early before tour groups. Walk through to Ōkōchi Sansō — a private villa garden with stunning views.',
              details: [
                '⏰ Go by 7am — the bamboo grove is deserted and ethereal in early morning light',
                '🌿 Ōkōchi Sansō villa (¥1,000 entry, includes matcha) — the best-kept secret with Kyoto cityscape views',
                '📸 The main path is ~500m — side paths lead to quieter bamboo areas'
              ]
            },
            {
              title: 'Tenryū-ji Temple & Garden',
              description: 'UNESCO World Heritage zen temple with one of Kyoto\'s finest gardens — a "borrowed scenery" composition using the Arashiyama mountains as its backdrop.',
              details: [
                '🍁 The garden\'s pond reflects autumn colours beautifully',
                '🏛️ Founded 1339 — the oldest of Kyoto\'s great zen temples',
                '🧘 The garden exemplifies "shakkei" (borrowed landscape) — the mountains become part of the design'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Iwatayama Monkey Park',
              description: 'Hike 20 minutes up to a hilltop park where 120 wild macaques roam free. You\'re in THEIR space — the views of Kyoto from the top are spectacular.',
              details: [
                '🐒 Monkeys are wild but habituated — don\'t stare or show teeth',
                '🏔️ The hilltop panorama of Kyoto is one of the best viewpoints in the city',
                '🥜 Feed them from inside the shelter building (peanuts and apples available)'
              ]
            },
            {
              title: 'Hozu River Boat Ride',
              description: 'A 16km scenic boat ride down the Hozu River gorge — piloted by boatmen using poles and oars. Dramatic cliff scenery, especially beautiful with autumn foliage.',
              details: [
                '🚣 2-hour ride from Kameoka to Arashiyama — book at Hozu-gawa office',
                '🍁 October: the gorge starts showing autumn colour — gorgeous from the water',
                '💰 ¥4,100/person'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Yoshimura (Arashiyama)',
              description: 'Handmade soba overlooking the Togetsukyō bridge and river. Window seats have one of the most beautiful lunch views in Kyoto.',
              meta: '💰 ¥1,200-2,000 · 📍 Arashiyama, riverfront'
            },
            {
              type: '🍶 Dinner',
              name: 'Tempura Yoshikawa',
              description: 'Intimate counter tempura in a serene traditional inn. Watch the chef fry each piece to translucent perfection — autumn vegetables, shrimp, and anago (sea eel).',
              meta: '💰 ¥¥¥ (¥8,000-15,000) · 📍 Central Kyoto'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0170, lng: 135.6717, label: 'Bamboo Grove', num: 1, cat: 'attraction', desc: 'Towering bamboo cathedral' },
        { lat: 35.0156, lng: 135.6745, label: 'Tenryū-ji', num: 2, cat: 'attraction', desc: 'UNESCO zen temple with borrowed-scenery garden' },
        { lat: 35.0100, lng: 135.6780, label: 'Iwatayama Monkey Park', num: 3, cat: 'attraction', desc: 'Wild macaques with hilltop Kyoto views' },
        { lat: 35.0112, lng: 135.6785, label: 'Togetsukyō Bridge', num: 4, cat: 'attraction', desc: 'Iconic Arashiyama bridge' },
        { lat: 35.0118, lng: 135.6792, label: 'Yoshimura', num: 5, cat: 'food', desc: 'Soba with river views' }
      ]
    },
    {
      num: 12,
      date: '2026-10-24',
      neighborhoods: 'Kinkaku-ji · Ryōan-ji · Kitano',
      title: 'Gold, Zen Rocks & Geisha Craft',
      description: "Northern Kyoto's greatest hits: the gold-leafed Kinkaku-ji pavilion reflected in its mirror pond, the enigmatic rock garden at Ryōan-ji, and an afternoon in the Nishijin textile district watching traditional weaving.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kinkaku-ji (Golden Pavilion)',
              description: 'The gold-leafed pavilion reflected perfectly in its mirror pond — Japan\'s most photographed temple. Rebuilt in 1955 after a monk\'s arson (the subject of Mishima\'s novel).',
              details: [
                '📸 Best photos from the pond\'s edge — the reflection is sharpest on calm mornings',
                '⏰ Opens 9am — arrive early to beat tour buses',
                '🍵 Matcha and gold-flake wagashi available in the garden tea house'
              ]
            },
            {
              title: 'Ryōan-ji Rock Garden',
              description: 'Japan\'s most famous zen rock garden — 15 stones arranged on raked white gravel. Designed so you can never see all 15 from any single viewpoint. Contemplative and profound.',
              details: [
                '🧘 Sit on the wooden platform and just observe — this is meditation through design',
                '🏛️ The surrounding moss garden and pond are equally beautiful, often overlooked',
                '📐 The design is attributed to Sōami (15th century) — 500+ years of zen minimalism'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nishijin Textile Center',
              description: 'Nishijin is Kyoto\'s traditional weaving district — producing obi (kimono sashes) for 500+ years. Visit the textile center for weaving demonstrations and a small museum, then explore nearby workshops.',
              details: [
                '🧵 Free weaving demonstrations using traditional Jacquard-style looms',
                '👘 Try a kimono fitting experience at the center',
                '🛍️ Nishijin ori (textiles) make beautiful, lightweight souvenirs'
              ]
            },
            {
              title: 'Kitano Tenmangū Shrine & Market',
              description: 'Shinto shrine dedicated to learning, surrounded by 2,000 plum trees. If visiting on the 25th, the famous flea market (Tenjin-san) fills the grounds with antiques, kimono, and crafts.',
              details: [
                '🏛️ The ornate Momoyama-style architecture is among Kyoto\'s most impressive',
                '🛍️ The 25th-of-month flea market is legendary — plan around it if dates align',
                '🍁 The garden has early maples alongside the plum trees'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Imai (Kitano)',
              description: 'Yuba (tofu skin) specialist in the Kitano area. Delicate tofu-skin dishes in many preparations — fresh, fried, simmered, wrapped. A Kyoto speciality.',
              meta: '💰 ¥2,000-3,500 · 📍 Near Kitano Tenmangū'
            },
            {
              type: '🍲 Dinner',
              name: 'Nishiki Warai (Kawaramachi)',
              description: 'Kyoto-style okonomiyaki — lighter and more refined than Osaka-style. Located near Nishiki Market for a pre-dinner stroll through Kyoto\'s \"Kitchen.\"',
              meta: '💰 ¥1,500-3,000 · 📍 Kawaramachi area'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0394, lng: 135.7293, label: 'Kinkaku-ji', num: 1, cat: 'attraction', desc: 'Golden Pavilion reflected in mirror pond' },
        { lat: 35.0345, lng: 135.7183, label: 'Ryōan-ji', num: 2, cat: 'attraction', desc: 'Enigmatic 15-stone zen rock garden' },
        { lat: 35.0316, lng: 135.7422, label: 'Nishijin Textile Center', num: 3, cat: 'attraction', desc: 'Traditional weaving demonstrations' },
        { lat: 35.0316, lng: 135.7352, label: 'Kitano Tenmangū', num: 4, cat: 'attraction', desc: 'Shrine of learning and flea market' },
        { lat: 35.0040, lng: 135.7690, label: 'Nishiki Warai', num: 5, cat: 'food', desc: 'Refined Kyoto okonomiyaki' }
      ]
    },
    {
      num: 13,
      date: '2026-10-25',
      neighborhoods: 'Tōfuku-ji · Uji',
      title: 'Peak Autumn Colour & Uji Tea Country',
      description: "Chase autumn foliage at Tōfuku-ji — Kyoto's #1 spot for momiji (maple) viewing — then take the train to Uji, the birthplace of Japanese tea culture. Visit the iconic Byōdō-in temple (it's on the ¥10 coin) and sample the finest matcha.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tōfuku-ji Temple',
              description: 'Kyoto\'s premier autumn foliage temple. The Tsūtenkyō (Bridge to Heaven) crosses a ravine filled with 2,000 maples — when they turn, it\'s a sea of red, orange, and gold.',
              details: [
                '🍁 Peak autumn colour: late October to late November — you\'re in the sweet spot',
                '📸 The bridge view down into the maple ravine is unforgettable',
                '🧘 The Hōjō garden by Mirei Shigemori is a masterpiece of modern zen design (1939)',
                '⏰ Go at opening (8:30am) — this is Kyoto\'s most popular autumn spot'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Uji: Tea Town & Byōdō-in',
              description: 'A 20-minute train ride south to Japan\'s tea capital. Walk the tea-scented streets, visit Byōdō-in\'s Phoenix Hall (a 1,000-year-old temple depicted on the ¥10 coin), and have the best matcha of your life.',
              details: [
                '🏛️ Byōdō-in Phoenix Hall — exquisite 1053 AD Heian architecture reflected in its pond',
                '🍵 Nakamura Tokichi — Uji\'s finest tea house, operating since 1859. Try the matcha parfait.',
                '🍵 Tsuen Tea — Japan\'s oldest tea house (founded 1160!)',
                '🌉 Walk along the Uji River — peaceful and scenic'
              ]
            }
          ],
          meals: [
            {
              type: '🍵 Lunch',
              name: 'Nakamura Tokichi Honten',
              description: 'Uji\'s most famous tea house. The matcha soba, matcha parfait, and fresh-whisked usucha are extraordinary. The building is a registered cultural property.',
              meta: '💰 ¥1,500-3,000 · 📍 Uji · Queue 30-60 min on weekends'
            },
            {
              type: '🍶 Dinner',
              name: 'Pontocho Alley Dining',
              description: 'Back in Kyoto, walk the narrow Pontocho alley along the Kamo River. Pick a restaurant with riverside terrace seating (kawayuka) — the last month for outdoor riverside dining before it closes for winter.',
              meta: '💰 ¥3,000-8,000 · 📍 Pontocho, Kyoto · Kawayuka season ends Oct 31'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9762, lng: 135.7743, label: 'Tōfuku-ji', num: 1, cat: 'attraction', desc: 'Kyoto\'s #1 autumn foliage temple' },
        { lat: 34.8893, lng: 135.8077, label: 'Byōdō-in', num: 2, cat: 'attraction', desc: '1000-year-old Phoenix Hall (on ¥10 coin)' },
        { lat: 34.8907, lng: 135.8073, label: 'Nakamura Tokichi', num: 3, cat: 'food', desc: 'Legendary tea house since 1859' },
        { lat: 35.0040, lng: 135.7702, label: 'Pontocho Alley', num: 4, cat: 'food', desc: 'Narrow alley with riverside dining' },
        { lat: 34.8914, lng: 135.8050, label: 'Uji River', num: 5, cat: 'attraction', desc: 'Scenic riverside walk in tea country' }
      ]
    },
    {
      num: 14,
      date: '2026-10-26',
      neighborhoods: 'Nara',
      title: 'Day Trip: Nara — Deer, Giants & Ancient Wood',
      description: "A day trip to Japan's first permanent capital (710 AD). Nara Park's friendly bowing deer, the colossal Tōdai-ji Buddha (world's largest bronze statue inside the world's largest wooden building), and the serene Kasuga-taisha shrine with 3,000 stone lanterns.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Nara Park & Deer',
              description: '1,200 wild deer roam freely — considered divine messengers in Shinto. Buy shika-senbei (deer crackers, ¥200) and they\'ll bow to you before eating. Genuinely magical.',
              details: [
                '🦌 The deer bow if you bow first — it\'s learned behaviour, not a trick',
                '⚠️ Watch your maps and bags — deer will eat paper',
                '📸 Baby deer (born May-July) are extra cute by October'
              ]
            },
            {
              title: 'Tōdai-ji Temple',
              description: 'The Great Buddha Hall houses a 15-metre bronze Buddha — cast in 752 AD, it\'s staggering in scale. The wooden hall itself is the world\'s largest wooden structure (even after being rebuilt at 2/3 original size).',
              details: [
                '🏛️ The Nandaimon gate\'s guardian statues (Nio) are ferocious 8-metre wooden carvings',
                '🕳️ Try squeezing through the pillar hole — said to guarantee enlightenment',
                '🍁 The approach through Nara Park is especially beautiful in autumn'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kasuga-taisha Shrine',
              description: '3,000 stone and bronze lanterns line the paths to this forest shrine. Twice a year they\'re all lit (Feb & Aug), but even unlit they create an otherworldly atmosphere.',
              details: [
                '🏮 The lantern-lined path through primeval forest is deeply atmospheric',
                '⛩️ The vermilion shrine buildings are rebuilt every 20 years (Shinto tradition)',
                '🦌 Deer wander through the shrine grounds — they\'re everywhere in Nara'
              ]
            },
            {
              title: 'Naramachi Old Town',
              description: 'Nara\'s preserved merchant quarter — narrow lanes of traditional machiya houses converted into cafés, galleries, craft shops, and sake bars.',
              details: [
                '🏘️ The wooden machiya architecture is beautifully preserved',
                '🍶 Several sake breweries offer tastings',
                '🛍️ Ink (sumi) and calligraphy supplies are a Nara speciality'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Kakinoha Sushi (Tanaka)',
              description: 'Nara\'s signature dish — sushi wrapped in persimmon leaves. The leaves gently flavour and preserve the fish. Simple, elegant, and only available in Nara.',
              meta: '💰 ¥1,200-2,000 · 📍 Near Tōdai-ji'
            },
            {
              type: '🍶 Dinner',
              name: 'Sake tasting in Naramachi',
              description: 'Nara is the birthplace of sake — Harushika and Imanishi breweries offer tastings. Pair with small plates at a local izakaya.',
              meta: '💰 ¥2,000-5,000 · 📍 Naramachi'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6851, lng: 135.8399, label: 'Nara Park', num: 1, cat: 'attraction', desc: '1,200 sacred bowing deer' },
        { lat: 34.6890, lng: 135.8398, label: 'Tōdai-ji', num: 2, cat: 'attraction', desc: 'World\'s largest bronze Buddha' },
        { lat: 34.6810, lng: 135.8499, label: 'Kasuga-taisha', num: 3, cat: 'attraction', desc: '3,000 stone lanterns in ancient forest' },
        { lat: 34.6773, lng: 135.8320, label: 'Naramachi', num: 4, cat: 'attraction', desc: 'Preserved merchant quarter' },
        { lat: 34.6870, lng: 135.8380, label: 'Kakinoha Sushi', num: 5, cat: 'food', desc: 'Persimmon-leaf wrapped sushi' }
      ]
    },
    {
      num: 15,
      date: '2026-10-27',
      neighborhoods: 'Nanzen-ji · Philosopher\'s Path · Ginkaku-ji',
      title: 'Philosopher\'s Path & Zen Gardens',
      description: "Walk Kyoto's most contemplative route. Start at the grand Nanzen-ji temple complex, follow the cherry-tree-lined Philosopher's Path canal north past small temples, and end at the Silver Pavilion. A day of zen beauty and design.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Nanzen-ji Temple Complex',
              description: 'One of Kyoto\'s most important zen temples — the massive Sanmon gate (climb for views), the mysterious red-brick aqueduct running through the grounds, and exquisite sub-temples.',
              details: [
                '🏛️ Climb the Sanmon gate — the panoramic view of northern Kyoto is beautiful',
                '📸 The red-brick Meiji-era aqueduct cutting through the temple grounds is surreal',
                '🧘 Tenjuan sub-temple — two contrasting gardens (moss vs dry landscape)',
                '🍁 Nanzen-ji is famous for autumn colour — maples frame the Sanmon gate'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Philosopher\'s Path (Tetsugaku no Michi)',
              description: 'A 2km canal-side walking path named after philosopher Nishida Kitarō, who meditated here on his daily walk. Lined with cherry trees and small temples — sublime in every season.',
              details: [
                '🚶 The walk takes 30-45 min without stops, but budget 2 hours for temple detours',
                '🐱 Cat café and small galleries along the path',
                '⛩️ Detour to Hōnen-in — a tiny thatched-gate temple with raked sand artworks'
              ]
            },
            {
              title: 'Ginkaku-ji (Silver Pavilion)',
              description: 'The understated counterpart to Kinkaku-ji — never actually covered in silver, but its wabi-sabi aesthetic is more profound. The meticulously raked sand garden (Ginshadan) represents the sea under moonlight.',
              details: [
                '🏛️ The sand garden\'s cone (Kogetsudai) represents Mount Fuji — or the moon',
                '🍁 The hillside garden behind has beautiful autumn colour and city views',
                '📐 This is wabi-sabi philosophy made physical — beauty in imperfection and restraint'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Hinode Udon (Philosopher\'s Path)',
              description: 'Simple, perfect udon in a tiny shop near the path. Curry udon is the signature — thick, warming, and the ideal fuel for a day of walking.',
              meta: '💰 ¥800-1,200 · 📍 Near Philosopher\'s Path'
            },
            {
              type: '🍷 Dinner',
              name: 'Kikunoi Honten',
              description: 'Three-Michelin-star kaiseki — one of Kyoto\'s absolute finest. Chef Murata Yoshihiro is a Living National Treasure of Japanese cuisine. Multi-course autumn kaiseki in a centuries-old building.',
              meta: '💰 ¥¥¥¥ (¥30,000-50,000) · 📍 Higashiyama · Reserve 2-3 months ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0112, lng: 135.7932, label: 'Nanzen-ji', num: 1, cat: 'attraction', desc: 'Grand zen temple with brick aqueduct' },
        { lat: 35.0190, lng: 135.7941, label: 'Philosopher\'s Path', num: 2, cat: 'attraction', desc: '2km contemplative canal walk' },
        { lat: 35.0270, lng: 135.7982, label: 'Ginkaku-ji', num: 3, cat: 'attraction', desc: 'Silver Pavilion — wabi-sabi zen beauty' },
        { lat: 35.0230, lng: 135.7950, label: 'Hōnen-in', num: 4, cat: 'attraction', desc: 'Thatched-gate temple with raked sand art' },
        { lat: 35.0006, lng: 135.7830, label: 'Kikunoi Honten', num: 5, cat: 'food', desc: 'Three-Michelin-star kaiseki' }
      ]
    },
    {
      num: 16,
      date: '2026-10-28',
      neighborhoods: 'Nishiki Market · Kawaramachi · Kyoto Station',
      title: 'Nishiki Market, Last Kyoto Stroll & Train to Osaka',
      description: "Final Kyoto morning at Nishiki Market — five blocks of food stalls and pickled-everything shops. Browse, taste, and stock up. Afternoon: catch the train to Osaka (15 min by Shinkansen or 30 min by express) for the second half of your Kansai adventure.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Nishiki Market',
              description: 'Kyoto\'s \"Kitchen\" — a 5-block covered market dating to the 14th century. Pickled vegetables, fresh tofu, matcha sweets, knife shops, and street food stalls. The best one-stop introduction to Kyoto food culture.',
              details: [
                '🥒 Try tsukemono (pickles) — Kyoto\'s are the best in Japan. Dozens of varieties.',
                '🍡 Fresh dango, matcha warabi-mochi, and yuba (tofu skin) snacks',
                '🔪 Aritsugu — knife shop since 1560. Custom-engraved handles available.',
                '📍 Best visited 10am-12pm — some stalls close by 4pm'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Train to Osaka & Namba Check-In',
              description: 'Take the Hankyu or JR line from Kyoto to Osaka (30-50 min). Check into your Osaka hotel — W Osaka in Shinsaibashi or Conrad Osaka for design-forward stays.',
              details: [
                '🚃 JR Special Rapid: 30 min Kyoto→Osaka. Hankyu line to Umeda: 45 min',
                '🏨 W Osaka — bold design hotel on Midōsuji, walkable to Dōtonbori',
                '🏨 Conrad Osaka — sleek, quiet luxury with river views in Nakanoshima'
              ]
            },
            {
              title: 'Dōtonbori Night Walk',
              description: 'Osaka\'s neon-drenched food street — the running Glico Man sign, giant mechanical crabs, and the sweet smell of takoyaki. This is where Osaka\'s food obsession comes alive.',
              details: [
                '📸 The Glico Man sign + canal reflection is the iconic Osaka photo',
                '🐙 Takoyaki stands on every corner — try several and compare',
                '🏮 Walk the side streets for more local izakayas with less tourist markup'
              ]
            }
          ],
          meals: [
            {
              type: '🍡 Lunch',
              name: 'Nishiki Market Grazing',
              description: 'No single restaurant — graze through the market. Must-tries: dashimaki tamago (rolled omelette), fresh yuba, grilled mochi, and Kyoto-style pickles.',
              meta: '💰 ¥1,500-3,000 · 📍 Nishiki Market'
            },
            {
              type: '🐙 Dinner',
              name: 'Dōtonbori Street Food',
              description: 'Takoyaki (Creo-Ru or Wanaka), okonomiyaki preview, kushikatsu, and gyoza — eat your way down the strip.',
              meta: '💰 ¥2,000-4,000 · 📍 Dōtonbori'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0050, lng: 135.7647, label: 'Nishiki Market', num: 1, cat: 'food', desc: 'Kyoto\'s 5-block covered food market' },
        { lat: 34.6687, lng: 135.5013, label: 'Dōtonbori', num: 2, cat: 'attraction', desc: 'Neon food street with Glico Man sign' },
        { lat: 34.6723, lng: 135.5000, label: 'Shinsaibashi', num: 3, cat: 'shopping', desc: 'Osaka\'s main shopping arcade' },
        { lat: 34.6686, lng: 135.5025, label: 'Takoyaki stands', num: 4, cat: 'food', desc: 'Osaka\'s famous octopus balls' },
        { lat: 35.0031, lng: 135.7660, label: 'Aritsugu Knives', num: 5, cat: 'shopping', desc: 'Knife shop since 1560 — custom engraving' }
      ]
    },

    // ===== OSAKA: Days 17-21 =====
    {
      num: 17,
      date: '2026-10-29',
      neighborhoods: 'Shinsekai · Tennō-ji · Abeno',
      title: 'Retro Osaka — Shinsekai, Kushikatsu & Abeno Harukas',
      description: "Dive into Osaka's retro soul. Shinsekai (\"New World\") is a 1920s entertainment district frozen in time — neon, kushikatsu (fried skewers), and Tsūtenkaku Tower. Then ascend Japan's tallest skyscraper, Abeno Harukas, for 360° views.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinsekai District',
              description: 'Built in 1912 as Osaka\'s vision of New York and Paris. Today it\'s a retro wonderland of neon signs, pachinko parlours, and kushikatsu joints. Tsūtenkaku Tower (1956) anchors the district.',
              details: [
                '🗼 Tsūtenkaku Tower — observation deck with Biliken (god of luck) statue. Rub his feet!',
                '🎮 Retro game centres with 1990s arcade cabinets',
                '🏮 The neon signage and Shōwa-era aesthetic are a photographer\'s dream'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Abeno Harukas',
              description: 'Japan\'s tallest building (300m, 60 floors). The Harukas 300 observation deck has floor-to-ceiling glass and an outdoor terrace. The Abeno Harukas Art Museum on 16F hosts excellent exhibitions.',
              details: [
                '🏛️ 300m high — views stretch to Kobe, Nara, and even Awaji Island on clear days',
                '🎨 The 16F art museum rotates impressive exhibitions',
                '🌅 Sunset views from the 60F terrace are spectacular'
              ]
            },
            {
              title: 'Tennō-ji Park & Keitaku-en Garden',
              description: 'A Meiji-era circular garden modelled on famous gardens across Japan. Peaceful, well-designed, and a nice contrast to Shinsekai\'s chaos.',
              details: [
                '🌳 The garden costs only ¥150 — one of Osaka\'s best-kept secrets',
                '🍁 Autumn colour appears in the garden by late October'
              ]
            }
          ],
          meals: [
            {
              type: '🍢 Lunch',
              name: 'Daruma Kushikatsu (Shinsekai)',
              description: 'Shinsekai\'s most famous kushikatsu chain — deep-fried skewers dipped in sweet-savory sauce. Rule: NO DOUBLE DIPPING in the communal sauce.',
              meta: '💰 ¥1,500-3,000 · 📍 Shinsekai · Multiple locations'
            },
            {
              type: '🍷 Dinner',
              name: 'Hajime (Nishi-Shinsaibashi)',
              description: 'Three-Michelin-star French-Japanese by Chef Hajime Yoneda. Famous for the \"planet earth\" opening course — a sphere of 100+ vegetables. Avant-garde, philosophical dining.',
              meta: '💰 ¥¥¥¥ (¥35,000+) · 📍 Nishi-Shinsaibashi · Reserve months ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6525, lng: 135.5063, label: 'Shinsekai', num: 1, cat: 'attraction', desc: 'Retro 1920s neon district' },
        { lat: 34.6533, lng: 135.5064, label: 'Tsūtenkaku Tower', num: 2, cat: 'attraction', desc: 'Retro observation tower with Biliken statue' },
        { lat: 34.6462, lng: 135.5140, label: 'Abeno Harukas', num: 3, cat: 'attraction', desc: 'Japan\'s tallest building — 300m views' },
        { lat: 34.6499, lng: 135.5109, label: 'Tennō-ji Park', num: 4, cat: 'attraction', desc: 'Meiji-era garden, peaceful autumn stroll' },
        { lat: 34.6723, lng: 135.4963, label: 'Hajime', num: 5, cat: 'food', desc: 'Three-star avant-garde French-Japanese' }
      ]
    },
    {
      num: 18,
      date: '2026-10-30',
      neighborhoods: 'Nakanoshima · Umeda · Tenjinbashi',
      title: 'Modern Architecture & Umeda Sky Building',
      description: "Osaka's design side. Nakanoshima is a river island packed with striking modern architecture — Tadao Ando's Nakanoshima Children's Book Forest, the ceramic-tiled National Museum. Then the mind-bending Umeda Sky Building and Tenjinbashi — Japan's longest shopping street.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Nakanoshima Architecture Walk',
              description: 'Osaka\'s cultural island between two rivers. The highlight is Tadao Ando\'s Nakanoshima Children\'s Book Forest (Kodomo Hon no Mori) — a concrete and wood cathedral filled with 25,000 books from floor to ceiling.',
              details: [
                '🏛️ Children\'s Book Forest (Ando, 2020) — free entry, book online. Stunning even without kids.',
                '🏛️ National Museum of Art — underground galleries beneath a dramatic steel-lattice canopy',
                '🏛️ Osaka City Central Public Hall — 1918 neo-Renaissance, beautifully maintained',
                '🌊 Walk along the river promenade — the water reflections of the buildings are gorgeous'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Umeda Sky Building',
              description: 'Hiroshi Hara\'s futuristic twin-tower complex connected by a dramatic floating garden observatory at the top. One of the most striking buildings in Asia — the escalator through the void is vertigo-inducing.',
              details: [
                '🏛️ Built 1993 — the open-air \"Floating Garden\" rooftop is breathtaking at sunset',
                '📸 The glass-tube escalator between the towers is a design experience in itself',
                '🌃 Go at sunset — the transition from day to night views is spectacular',
                '🏮 The basement recreates a 1920s Osaka streetscape — atmospheric restaurant alley'
              ]
            },
            {
              title: 'Tenjinbashi-suji Shopping Street',
              description: 'Japan\'s longest covered shopping arcade (2.6km). Not touristy — this is where locals shop. Vintage clothes, 100-year-old shops, and incredible street food.',
              details: [
                '🛍️ 2.6km of covered arcade — budget 1-2 hours to explore',
                '🍡 Street food stalls: croquettes, korokke, taiyaki',
                '📍 The northern end near Tenjinbashi station has the most character'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Kinryu Ramen (Dōtonbori)',
              description: 'Iconic Dōtonbori ramen — recognizable by the giant dragon sign. Rich tonkotsu (pork bone broth) with thin noodles. Open 24 hours.',
              meta: '💰 ¥800-1,200 · 📍 Dōtonbori'
            },
            {
              type: '🍺 Dinner',
              name: 'Umeda Sky Building Basement (Takimi-koji)',
              description: 'The retro 1920s-themed restaurant street beneath the Sky Building. Yakitori, okonomiyaki, and tempura in atmospheric recreated shopfronts.',
              meta: '💰 ¥2,000-5,000 · 📍 Umeda Sky Building B1'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6914, lng: 135.4942, label: 'Nakanoshima Book Forest', num: 1, cat: 'attraction', desc: 'Tadao Ando\'s book-filled concrete cathedral' },
        { lat: 34.6893, lng: 135.4904, label: 'National Museum of Art', num: 2, cat: 'attraction', desc: 'Underground galleries beneath steel lattice' },
        { lat: 34.7053, lng: 135.4901, label: 'Umeda Sky Building', num: 3, cat: 'attraction', desc: 'Floating Garden observatory — futuristic twin towers' },
        { lat: 34.6973, lng: 135.5113, label: 'Tenjinbashi-suji', num: 4, cat: 'shopping', desc: 'Japan\'s longest covered shopping street (2.6km)' },
        { lat: 34.6687, lng: 135.5015, label: 'Kinryu Ramen', num: 5, cat: 'food', desc: 'Iconic dragon-sign tonkotsu ramen' }
      ]
    },
    {
      num: 19,
      date: '2026-10-31',
      neighborhoods: 'Kuromon Market · Nipponbashi · Amerikamura',
      title: 'Kuromon Market, Den-Den Town & Halloween Night',
      description: "Morning: Osaka's \"Kitchen\" — Kuromon Market for the freshest seafood. Afternoon: Nipponbashi's Den-Den Town (Osaka's Akihabara — electronics and anime). Evening: Osaka goes WILD for Halloween — Dōtonbori and Amerikamura become a massive costumed street party.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kuromon Market',
              description: 'Osaka\'s 190-year-old \"Kitchen\" market. Walk the covered arcade grazing on uni (sea urchin), king crab legs, pufferfish, grilled wagyu, and fresh oysters.',
              details: [
                '🦀 King crab legs grilled to order — ¥1,000-2,000 per set',
                '🐡 Fugu (pufferfish) sashimi — Osaka is the fugu capital of Japan',
                '🍓 Fresh fruit stands with perfect Kyoho grapes and white strawberries (seasonal)',
                '⏰ Best 8am-12pm — some stalls close by 4pm'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nipponbashi Den-Den Town',
              description: 'Osaka\'s tech and otaku district — smaller and more walkable than Akihabara. Retro gaming shops, electronics, manga stores, and cosplay supply shops.',
              details: [
                '🕹️ Super Potato Osaka — retro games, trading cards, vintage consoles',
                '🎌 Cosplay shops line the main street — great for Halloween outfit shopping',
                '📱 Electronics bargains: Japanese-spec gadgets, cables, components'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Halloween Night in Dōtonbori & Amerikamura',
              description: 'October 31st in Osaka is a spectacle. Thousands of costumed revellers flood Dōtonbori and Amerikamura in elaborate costumes. The energy is electric — Japan takes Halloween cosplay incredibly seriously.',
              details: [
                '🎃 Dōtonbori bridge becomes a massive photo op — costumes are next-level',
                '👻 Amerikamura (\"Ame-Mura\") — Osaka\'s youth culture district, packed on Halloween',
                '🍻 Convenience store beers + street festival atmosphere',
                '📸 Japanese Halloween costumes are more creative than scary — expect art'
              ]
            }
          ],
          meals: [
            {
              type: '🦀 Lunch',
              name: 'Kuromon Market Grazing',
              description: 'Eat your way through the market: uni shooters, grilled scallops, wagyu skewers, fresh juice, and tamagoyaki.',
              meta: '💰 ¥3,000-6,000 · 📍 Kuromon Market'
            },
            {
              type: '🍕 Dinner',
              name: 'Okonomiyaki Mizuno (Dōtonbori)',
              description: 'Osaka\'s most famous okonomiyaki. The yamaimo (mountain yam) version is impossibly fluffy. Cooked on the teppan in front of you.',
              meta: '💰 ¥1,500-2,500 · 📍 Dōtonbori · Queue 30+ min'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6687, lng: 135.5081, label: 'Kuromon Market', num: 1, cat: 'food', desc: 'Osaka\'s Kitchen — 190 years of seafood' },
        { lat: 34.6595, lng: 135.5058, label: 'Den-Den Town', num: 2, cat: 'shopping', desc: 'Osaka\'s Akihabara — tech and anime' },
        { lat: 34.6729, lng: 135.4970, label: 'Amerikamura', num: 3, cat: 'attraction', desc: 'Youth culture district — epic on Halloween' },
        { lat: 34.6687, lng: 135.5015, label: 'Dōtonbori', num: 4, cat: 'attraction', desc: 'Halloween street party central' },
        { lat: 34.6689, lng: 135.5010, label: 'Okonomiyaki Mizuno', num: 5, cat: 'food', desc: 'Osaka\'s best fluffy okonomiyaki' }
      ]
    },
    {
      num: 20,
      date: '2026-11-01',
      neighborhoods: 'Naoshima Island (Day Trip)',
      title: 'Art Island — Naoshima Day Trip',
      description: "The crown jewel of Japan's design scene. Naoshima is an island in the Seto Inland Sea transformed into an open-air art museum — Tadao Ando's museums, Yayoi Kusama's pumpkins, James Turrell's light installations, and art embedded in abandoned village houses.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Ferry to Naoshima & Benesse House Museum',
              description: 'Take the Shinkansen from Shin-Osaka to Okayama (50 min), then the Marine Liner to Uno Port, and ferry to Naoshima (20 min). First stop: Benesse House Museum — Tadao Ando\'s concrete masterpiece built into a clifftop.',
              details: [
                '🚄 Shin-Osaka → Okayama: 50 min Shinkansen. Okayama → Uno: 50 min Marine Liner. Uno → Naoshima: 20 min ferry.',
                '🏛️ Benesse House — art and architecture fused: works by Pollock, Warhol, Hockney embedded in Ando\'s concrete',
                '🎨 The outdoor sculpture path along the coast includes works by Niki de Saint Phalle and others',
                '⏰ Start early — the island deserves a full day'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Chichu Art Museum',
              description: 'Ando\'s underground museum — built entirely into a hillside so no architecture is visible from outside. Inside: Monet Water Lilies in natural light, James Turrell\'s light rooms, and Walter De Maria\'s sphere. Profoundly moving.',
              details: [
                '🏛️ The Monet room is life-changing — five large Water Lilies canvases in a white concrete room with natural zenithal light',
                '💡 James Turrell\'s \"Open Sky\" — a room with an open ceiling that dissolves the boundary between inside and sky',
                '🎫 Timed entry — book online in advance'
              ]
            },
            {
              title: 'Art House Project & Kusama Pumpkins',
              description: 'Walk through Honmura village where abandoned houses have been transformed into art installations by Miyajima, Turrell, and others. Then find Yayoi Kusama\'s iconic yellow pumpkin sculpture on the pier.',
              details: [
                '🎨 Minamidera by James Turrell — enter total darkness and wait for light to appear (booking required)',
                '🎃 Yellow Pumpkin — the Instagram icon of Naoshima (replaced after typhoon damage)',
                '🏘️ Each Art House is a unique experience — budget 2 hours for all 7'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Benesse House Restaurant or Café',
              description: 'Dine overlooking the Seto Inland Sea. The museum café serves Japanese lunch sets with local Seto seafood.',
              meta: '💰 ¥2,000-4,000 · 📍 Benesse House, Naoshima'
            },
            {
              type: '🍶 Dinner',
              name: 'Izakaya in Namba (Osaka)',
              description: 'Back in Osaka, unwind in Namba\'s izakaya alleys. Ura-Namba (\"behind Namba\") is a maze of tiny standing bars and local joints.',
              meta: '💰 ¥3,000-6,000 · 📍 Ura-Namba, Osaka'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.4593, lng: 133.9963, label: 'Benesse House Museum', num: 1, cat: 'attraction', desc: 'Ando\'s clifftop art-architecture fusion' },
        { lat: 34.4626, lng: 133.9937, label: 'Chichu Art Museum', num: 2, cat: 'attraction', desc: 'Underground museum — Monet, Turrell, De Maria' },
        { lat: 34.4579, lng: 134.0027, label: 'Art House Project', num: 3, cat: 'attraction', desc: 'Village houses transformed into art installations' },
        { lat: 34.4543, lng: 133.9952, label: 'Yellow Pumpkin', num: 4, cat: 'attraction', desc: 'Kusama\'s iconic pumpkin sculpture' },
        { lat: 34.4617, lng: 133.9950, label: 'Naoshima Ferry Port', num: 5, cat: 'transport', desc: 'Ferry to/from Uno Port' }
      ]
    },
    {
      num: 21,
      date: '2026-11-02',
      neighborhoods: 'Osaka Castle · Minami · Kansai Airport',
      title: 'Osaka Castle, Last Bites & Sayōnara',
      description: "Final day. Morning walk around Osaka Castle's stunning autumn grounds, a farewell lunch of the finest sushi or wagyu, last-minute shopping in the underground malls, and departure from Kansai International Airport. Until next time, Japan.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Osaka Castle & Nishinomaru Garden',
              description: 'Toyotomi Hideyoshi\'s 16th-century fortress, rebuilt in concrete but still imposing. The Nishinomaru Garden offers the best castle views framed by autumn trees.',
              details: [
                '🏯 The castle museum inside has 8 floors of Osaka history — the top floor observation deck has 360° views',
                '🍁 Nishinomaru Garden (¥200) — 600 cherry trees that also show beautiful autumn colour',
                '📸 Best castle photo: from the southwest corner of Nishinomaru Garden',
                '🏃 Runners circle the castle moat in the morning — great walking path'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Last Shopping & Departure',
              description: 'Hit Osaka\'s underground shopping malls (Namba Walk, Umeda Chika) for last-minute souvenirs — Japanese stationery, ceramics, snacks. Then take the Haruka Express to Kansai International Airport (50 min from Tennōji).',
              details: [
                '🚃 JR Haruka Express: 50 min Tennōji → KIX. Or Nankai Rapi:t from Namba (35 min)',
                '🛍️ Don Quijote — chaotic multi-floor discount store, tax-free for tourists',
                '✈️ KIX duty-free has excellent Japanese whisky, sake, and Kit Kat flavours',
                '💌 You can mail postcards from Osaka Central Post Office with special stamps'
              ]
            }
          ],
          meals: [
            {
              type: '🍣 Lunch',
              name: 'Sushi Harasho (Fukushima)',
              description: 'Outstanding neighbourhood sushi in Osaka\'s Fukushima district. Omakase course with pristine Seto Inland Sea fish. A perfect final meal.',
              meta: '💰 ¥¥¥ (¥10,000-15,000) · 📍 Fukushima · Reserve ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6873, lng: 135.5262, label: 'Osaka Castle', num: 1, cat: 'attraction', desc: 'Toyotomi Hideyoshi\'s iconic fortress' },
        { lat: 34.6857, lng: 135.5217, label: 'Nishinomaru Garden', num: 2, cat: 'attraction', desc: 'Castle garden with autumn colour' },
        { lat: 34.6924, lng: 135.4948, label: 'Sushi Harasho', num: 3, cat: 'food', desc: 'Outstanding omakase sushi' },
        { lat: 34.6648, lng: 135.5015, label: 'Namba', num: 4, cat: 'shopping', desc: 'Last-minute shopping and Nankai line to KIX' },
        { lat: 34.4320, lng: 135.2304, label: 'Kansai International Airport', num: 5, cat: 'transport', desc: 'Departure — sayōnara, Japan' }
      ]
    }
  ]
};

const result = fulfillOrder(order, itineraryData);
console.log('✅ Fulfillment complete!');
console.log('Slug:', result.slug);
console.log('URL:', result.url);
console.log('File:', result.filePath);
