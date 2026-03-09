const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772316298153_mhjna2',
  email: 'rm_blakemore@xtra.co.nz',
  destination: 'Tokyo, Osaka and Kyoto, Japan',
  startDate: '2026-10-13',
  endDate: '2026-11-02',
  groupSize: 2,
  requests: 'We are both 70 years old, want to travel by train where possible and are also interested in design and technology'
};

const itineraryData = {
  destination: 'Tokyo, Osaka & Kyoto, Japan',
  countryEmoji: '🇯🇵',
  title: 'Japan by Rail — Design, Culture & Flavour',
  subtitle: '21 days through Tokyo, Kyoto & Osaka for curious minds who travel at their own pace',
  description: "This itinerary is built for two travellers who love design, technology, and good food — and prefer to explore at a comfortable pace. Japan's rail network is the world's finest, and a 21-day JR Pass unlocks the entire country. From Tokyo's cutting-edge design museums and Akihabara's tech wonderland, through Kyoto's serene temples and artisan workshops, to Osaka's legendary street food scene — every day balances discovery with rest. Flat walking routes, accessible transit, and plenty of sit-down meals make this a trip to savour, not survive.",
  duration: '21 nights',
  dates: 'Oct 13 – Nov 2, 2026',
  budget: '$$–$$$',
  pace: 'Relaxed',
  bestFor: 'Couples · Design Lovers · Foodies',
  highlights: [
    '21-day Japan Rail Pass — bullet trains, local lines, everything',
    'teamLab Borderless & 21_21 DESIGN SIGHT in Tokyo',
    'Miraikan (National Museum of Emerging Science) & Akihabara tech district',
    'Fushimi Inari at dawn & Kinkaku-ji golden pavilion in Kyoto',
    'Nara deer park & ancient temples day trip',
    'Osaka street food crawl through Dōtonbori & Shinsekai',
    'Hakone day trip — hot springs, open-air museum & lake cruise',
    'Naoshima Art Island day trip from Osaka'
  ],

  essentials: [
    { title: '🚄 Japan Rail Pass', text: 'A 21-day JR Pass (¥100,020 / ~$670 USD each) covers all JR trains including Shinkansen bullet trains, JR local lines, and the Narita Express. Activate on Day 1. Reserve Shinkansen seats free at JR ticket offices — highly recommended for Tōkaidō route (Tokyo↔Kyoto/Osaka).' },
    { title: '🍂 Autumn Weather', text: 'Mid-October to early November is one of Japan\'s best seasons. Expect 15-22°C in Tokyo, slightly cooler in Kyoto. Early autumn colour (kōyō) may begin in late October. Pack layers, a light rain jacket, and comfortable walking shoes.' },
    { title: '♿ Accessibility & Pace', text: 'Japan is remarkably accessible. All major stations have elevators, escalators, and staff who will help. Trains are punctual and smooth. This itinerary avoids steep hikes and keeps daily walking moderate. Many temples have flat paths, and taxis are affordable for tired legs.' },
    { title: '💳 Money & IC Cards', text: 'Get a Suica or PASMO IC card for convenience stores, vending machines, and non-JR transit (metro, buses). Most places accept cash; cards are increasingly accepted in cities. 7-Eleven ATMs work with international cards.' }
  ],

  days: [
    // ===== TOKYO: Days 1-7 =====
    {
      num: 1,
      date: '2026-10-13',
      neighborhoods: 'Narita Airport · Shinjuku',
      title: 'Arrival — Welcome to Tokyo',
      description: "Arrive at Narita, activate your JR Pass, and take the Narita Express to Shinjuku. Settle into your hotel in one of Tokyo's most convenient neighbourhoods. An easy evening to recover and get oriented.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Narita Express to Shinjuku',
              description: 'Activate your 21-day JR Pass at the JR ticket office in Narita Airport. The Narita Express (N\'EX) whisks you to Shinjuku Station in about 90 minutes — covered by your pass.',
              details: [
                '🎫 Activate JR Pass at JR East Travel Service Center in Narita',
                '🚃 Narita Express runs every 30 mins — clean, quiet, spacious',
                '🏨 Stay in Shinjuku for excellent rail connections everywhere'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Pick up a Suica IC card from the machines at Narita — you\'ll use it constantly for metro, buses, and convenience store purchases.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shinjuku Evening Stroll',
              description: 'Take a gentle evening walk around Shinjuku. The neon-lit streets are mesmerising even when you\'re jet-lagged. Omoide Yokocho (Memory Lane) is a narrow alley of tiny yakitori bars — the perfect first taste of Tokyo.',
              details: [
                '🏮 Omoide Yokocho — atmospheric alley of tiny yakitori joints',
                '🌆 Shinjuku is sensory overload in the best way'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Fuunji Tsukemen',
              description: 'Outstanding tsukemen (dipping ramen) near Shinjuku Station. Rich, concentrated broth with thick noodles. Counter-style, no frills, incredible flavour.',
              meta: '💰 $ · 📍 Yoyogi, 2-min walk from south exit'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6896, lng: 139.6922, label: 'Shinjuku Station', num: 1, cat: 'transport', desc: 'Tokyo\'s busiest hub — your base for the trip' },
        { lat: 35.6937, lng: 139.6984, label: 'Omoide Yokocho', num: 2, cat: 'food', desc: 'Atmospheric alley of tiny yakitori bars' },
        { lat: 35.6878, lng: 139.6978, label: 'Fuunji', num: 3, cat: 'food', desc: 'Famous tsukemen near Shinjuku Station' }
      ]
    },
    {
      num: 2,
      date: '2026-10-14',
      neighborhoods: 'Roppongi · Midtown · Azabu',
      title: 'Design Day — 21_21 & Midtown',
      description: "A day dedicated to Japanese design. 21_21 DESIGN SIGHT is one of the world's great design museums, housed in a Tadao Ando building. Then explore the curated shops of Tokyo Midtown and the Roppongi Art Triangle.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: '21_21 DESIGN SIGHT',
              description: 'Issey Miyake\'s design museum in Midtown Garden. The building itself — by Tadao Ando — is a masterpiece of concrete and light. Exhibitions rotate and always explore the intersection of design and daily life.',
              details: [
                '🏛️ Tadao Ando\'s signature concrete + natural light architecture',
                '🎨 Rotating exhibitions on product design, materials, future living',
                '♿ Fully accessible — elevator to all levels',
                '⏰ Opens 10am · ¥1,200 admission'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tokyo Midtown Design Hub & Suntory Museum of Art',
              description: 'Tokyo Midtown is a design lover\'s paradise. Browse the Design Hub (free exhibitions on Japanese design), Suntory Museum of Art (traditional Japanese art and crafts), and the curated shops below.',
              details: [
                '🛍️ Midtown shops feature Japanese stationery, ceramics, and homewares',
                '🖼️ Suntory Museum — beautiful rotating Japanese art exhibitions',
                '🆓 Design Hub is always free'
              ]
            },
            {
              title: 'The National Art Center, Tokyo',
              description: 'Kisho Kurokawa\'s undulating glass masterpiece — Japan\'s largest exhibition space. Even if you skip the exhibits, the building and Brasserie Paul Bocuse inside are worth the visit.',
              details: [
                '🏛️ The wavy glass façade is one of Tokyo\'s architectural icons',
                '🆓 The building and café are free to enter',
                '📍 10-min walk from Midtown'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Brasserie Paul Bocuse le Musée',
              description: 'French bistro inside the National Art Center — sit in the iconic cone-shaped dining room floating above the atrium. Excellent lunch sets.',
              meta: '💰 $$ · 📍 Inside National Art Center, 3F'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Gonpachi Nishi-Azabu',
              description: 'The restaurant that inspired the Kill Bill fight scene. Multi-level traditional Japanese building serving yakitori, soba, and tempura. Atmospheric and casual.',
              meta: '💰 $$ · 📍 Nishi-Azabu · No reservation needed for ground floor'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6655, lng: 139.7310, label: '21_21 DESIGN SIGHT', num: 1, cat: 'attraction', desc: 'Tadao Ando-designed museum dedicated to design' },
        { lat: 35.6660, lng: 139.7313, label: 'Tokyo Midtown', num: 2, cat: 'attraction', desc: 'Design shops, galleries, and gardens' },
        { lat: 35.6652, lng: 139.7262, label: 'National Art Center', num: 3, cat: 'attraction', desc: 'Kurokawa\'s glass masterpiece — Japan\'s largest gallery' },
        { lat: 35.6628, lng: 139.7262, label: 'Brasserie Paul Bocuse', num: 4, cat: 'food', desc: 'French bistro inside the National Art Center' },
        { lat: 35.6575, lng: 139.7260, label: 'Gonpachi Nishi-Azabu', num: 5, cat: 'food', desc: 'The "Kill Bill" restaurant — yakitori and soba' }
      ]
    },
    {
      num: 3,
      date: '2026-10-15',
      neighborhoods: 'Odaiba · Toyosu',
      title: 'Tech & Science — Miraikan & Odaiba',
      description: "Today is all about the future. Miraikan — Japan's National Museum of Emerging Science — has robots, space exhibits, and the famous Geo-Cosmos globe. Then explore Odaiba's futuristic waterfront.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Miraikan (National Museum of Emerging Science & Innovation)',
              description: 'One of the world\'s best science museums. See Honda\'s ASIMO robot demonstration, the stunning Geo-Cosmos LED globe, and exhibits on AI, space exploration, and the deep ocean. Spend 2-3 hours easily.',
              details: [
                '🤖 ASIMO demo times vary — check schedule on arrival',
                '🌍 Geo-Cosmos — 6m LED globe showing real-time Earth data',
                '♿ Fully accessible — wheelchairs available',
                '⏰ 10am–5pm · ¥630 admission'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'teamLab Borderless (Azabudai Hills)',
              description: 'The relocated teamLab Borderless is a mind-bending digital art museum where artworks flow across rooms and respond to your presence. An immersive, accessible experience — flat floors throughout.',
              details: [
                '🎨 Book timed tickets online in advance — sells out',
                '⏰ Allow 2+ hours to explore',
                '♿ Flat floors, fully accessible',
                '📍 Now at Azabudai Hills (opened 2024)'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Bills Odaiba',
              description: 'Famous Australian-born café with a waterfront terrace on Odaiba. Known for ricotta hotcakes and excellent coffee.',
              meta: '💰 $$ · 📍 Decks Tokyo Beach, Odaiba'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Odaiba Sunset & Rainbow Bridge Views',
              description: 'Walk along the Odaiba waterfront promenade as the sun sets behind Rainbow Bridge and the Tokyo skyline. The mini Statue of Liberty replica makes for fun photos.',
              details: [
                '🌅 Sunset around 5pm in mid-October',
                '🌉 Rainbow Bridge illumination starts at dusk'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Toyosu Market area restaurants',
              description: 'Head to Toyosu for ultra-fresh sushi near the wholesale market. Many restaurants serve the same fish that was auctioned that morning.',
              meta: '💰 $$ · 📍 Toyosu · Best sushi value in Tokyo'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6190, lng: 139.7765, label: 'Miraikan', num: 1, cat: 'attraction', desc: 'Japan\'s National Museum of Emerging Science' },
        { lat: 35.6588, lng: 139.7310, label: 'teamLab Borderless', num: 2, cat: 'attraction', desc: 'Immersive digital art museum at Azabudai Hills' },
        { lat: 35.6272, lng: 139.7753, label: 'Odaiba Waterfront', num: 3, cat: 'attraction', desc: 'Futuristic waterfront with Rainbow Bridge views' },
        { lat: 35.6283, lng: 139.7745, label: 'Bills Odaiba', num: 4, cat: 'food', desc: 'Waterfront café with famous ricotta hotcakes' },
        { lat: 35.6455, lng: 139.7814, label: 'Toyosu Market area', num: 5, cat: 'food', desc: 'Ultra-fresh sushi near the wholesale market' }
      ]
    },
    {
      num: 4,
      date: '2026-10-16',
      neighborhoods: 'Akihabara · Nihonbashi · Ginza',
      title: 'Tech District & Traditional Crafts',
      description: "From Akihabara's electronics wonderland to Ginza's refined design shops — a day that spans Japan's love of technology and tradition. Browse gadgets in the morning, artisan craftsmanship in the afternoon.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Akihabara Electric Town',
              description: 'Japan\'s legendary electronics district. Browse multi-floor gadget stores, retro gaming shops, and hobby electronics. Yodobashi Camera Akiba is an 8-floor tech department store with everything imaginable.',
              details: [
                '🔌 Yodobashi Camera Akiba — 8 floors of electronics heaven',
                '🎮 Super Potato — retro gaming museum/shop',
                '🔧 Radio Kaikan — hobby electronics and model kits',
                '♿ Yodobashi has elevators to all floors'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nihonbashi — Heritage & Innovation',
              description: 'The historic heart of Edo-period commerce, now reimagined. COREDO Muromachi showcases traditional Japanese crafts in a modern setting — lacquerware, knives, textiles. Visit the Mitsui Memorial Museum for exquisite tea ceremony objects.',
              details: [
                '🔪 COREDO Muromachi — traditional crafts and food in a modern mall',
                '🏛️ Mitsui Memorial Museum — tea ceremony art and National Treasures',
                '🌉 Nihonbashi bridge — original "kilometre zero" of Japan\'s road network'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Taimeiken',
              description: 'Tokyo institution since 1931 — famous for their omurice (fluffy omelette over rice) and Napolitan spaghetti. Old-school yoshoku (Western-Japanese fusion).',
              meta: '💰 $$ · 📍 Nihonbashi · Queue is worth it'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Ginza Design Walk',
              description: 'Stroll down Ginza\'s main avenue (car-free on weekends). Visit the Ginza Six rooftop garden, Itoya stationery store (12 floors!), and the Uniqlo flagship for Japan-exclusive designs.',
              details: [
                '📎 Itoya — 12 floors of stationery perfection',
                '🏬 Ginza Six — luxury mall with rooftop garden and art installations',
                '👕 Uniqlo Ginza — 12-floor flagship with Japan exclusives'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ginza Kagari',
              description: 'Tiny ramen shop famous for their creamy chicken paitan ramen. Rich, smooth, unforgettable broth. A Michelin Bib Gourmand winner.',
              meta: '💰 $ · 📍 Ginza · Counter seating only, short queue'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6984, lng: 139.7711, label: 'Akihabara', num: 1, cat: 'attraction', desc: 'Electronics and tech wonderland' },
        { lat: 35.6851, lng: 139.7740, label: 'Nihonbashi', num: 2, cat: 'attraction', desc: 'Historic commercial district with traditional crafts' },
        { lat: 35.6852, lng: 139.7739, label: 'Taimeiken', num: 3, cat: 'food', desc: 'Classic omurice since 1931' },
        { lat: 35.6717, lng: 139.7639, label: 'Ginza', num: 4, cat: 'attraction', desc: 'Tokyo\'s luxury design and shopping avenue' },
        { lat: 35.6711, lng: 139.7650, label: 'Ginza Kagari', num: 5, cat: 'food', desc: 'Michelin-listed chicken paitan ramen' }
      ]
    },
    {
      num: 5,
      date: '2026-10-17',
      neighborhoods: 'Asakusa · Ueno · Yanaka',
      title: 'Old Tokyo — Temples, Museums & Shitamachi',
      description: "Step back in time through Tokyo's traditional heart. Sensō-ji temple in Asakusa, world-class museums in Ueno Park, and the nostalgic neighbourhood of Yanaka — untouched by wartime bombing and still full of old-world charm.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sensō-ji Temple & Nakamise-dōri',
              description: 'Tokyo\'s oldest temple (628 AD) is still its most atmospheric. Walk through the iconic Kaminarimon gate, browse the traditional stalls of Nakamise-dōri, and find peace in the temple\'s incense-filled grounds.',
              details: [
                '⛩️ Kaminarimon — the "Thunder Gate" with its giant red lantern',
                '🛍️ Nakamise-dōri — traditional snacks, fans, and crafts',
                '🍡 Try freshly grilled senbei (rice crackers) and melon pan',
                '⏰ Visit by 9am to avoid crowds'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ueno Park & Tokyo National Museum',
              description: 'Ueno Park is Tokyo\'s cultural heart. The Tokyo National Museum houses the world\'s largest collection of Japanese art — samurai armour, ukiyo-e prints, ceramics, and Buddhist sculpture spanning thousands of years.',
              details: [
                '🏛️ Tokyo National Museum — Japan\'s oldest and largest museum',
                '🎨 The Gallery of Hōryū-ji Treasures (Taniguchi-designed building) is stunning',
                '♿ Mostly flat paths, elevators in museum buildings',
                '⏰ ¥1,000 admission · Closed Mondays'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Kamachiku',
              description: 'Beautiful udon restaurant in a converted 1920s wooden house in Ueno. Hand-made udon, tempura, and a serene garden setting. A hidden gem.',
              meta: '💰 $$ · 📍 Near Nezu Station · Reservations recommended'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Yanaka — Tokyo\'s Nostalgic Neighbourhood',
              description: 'Yanaka survived WWII bombing and feels like stepping into 1950s Tokyo. Narrow lanes, family-run shops, cat sculptures, and the atmospheric Yanaka Cemetery with ancient trees. The Yanaka Ginza shopping street is charmingly old-school.',
              details: [
                '🐱 Yanaka is famous for its cats — real and sculptured',
                '🛒 Yanaka Ginza — traditional shopping street with local food stalls',
                '🌅 "Sunset Steps" (Yūyake Dandan) — great evening light'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Hantei',
              description: 'Beautiful 3-storey wooden building from 1927 serving kushiage (deep-fried skewers) course-style. One of Tokyo\'s most atmospheric dining experiences.',
              meta: '💰 $$ · 📍 Nezu · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: 'Sensō-ji Temple', num: 1, cat: 'attraction', desc: 'Tokyo\'s oldest and most visited temple (628 AD)' },
        { lat: 35.7189, lng: 139.7746, label: 'Tokyo National Museum', num: 2, cat: 'attraction', desc: 'World\'s largest Japanese art collection' },
        { lat: 35.7154, lng: 139.7666, label: 'Kamachiku', num: 3, cat: 'food', desc: 'Hand-made udon in a 1920s wooden house' },
        { lat: 35.7260, lng: 139.7672, label: 'Yanaka Ginza', num: 4, cat: 'attraction', desc: 'Nostalgic old-town shopping street' },
        { lat: 35.7210, lng: 139.7652, label: 'Hantei', num: 5, cat: 'food', desc: 'Kushiage in a stunning 1927 wooden building' }
      ]
    },
    {
      num: 6,
      date: '2026-10-18',
      neighborhoods: 'Harajuku · Omotesandō · Shibuya',
      title: 'Architecture & Street Culture',
      description: "Tokyo's most architecturally exciting corridor. Omotesandō is lined with buildings by Ando, Ito, Ban, and Herzog & de Meuron. Harajuku brings youthful energy, and Shibuya Crossing is the city's iconic heartbeat.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Meiji Jingū Shrine & Garden',
              description: 'Start the day with peace. Meiji Shrine sits in a vast forested park in the heart of the city. The gravel paths through towering trees are deeply calming. The inner garden (¥500) has irises and a beautiful tea house.',
              details: [
                '⛩️ Walk through the massive torii gate — Japan\'s largest',
                '🌳 The forest was planted in 1920 — 100,000 trees donated from across Japan',
                '♿ Main path is wide gravel — walkable but can be tiring; take it slow',
                '🍵 Inner garden is tranquil and less visited'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Omotesandō Architecture Walk',
              description: 'Japan\'s most architecturally significant shopping street. Every major fashion house commissioned a star architect: Tadao Ando (Omotesando Hills), Toyo Ito (Tod\'s), SANAA, Kengo Kuma, and more. An open-air architecture museum.',
              details: [
                '🏗️ Omotesando Hills — Tadao Ando\'s spiralling interior',
                '🏛️ Tod\'s by Toyo Ito — tree-inspired concrete structure',
                '🏗️ Dior by SANAA — translucent glass façade',
                '📸 Flat, tree-lined boulevard — beautiful for walking'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Anniversaire Café',
              description: 'Elegant café on the Omotesandō boulevard with terrace seating under zelkova trees. Perfect for people-watching with a croque monsieur.',
              meta: '💰 $$ · 📍 Omotesandō boulevard'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shibuya Crossing & Shibuya Sky',
              description: 'Experience the world\'s busiest pedestrian crossing from above. Shibuya Sky is a rooftop observation deck 230m up with an outdoor terrace — stunning at sunset. Then descend to street level and walk the crossing yourself.',
              details: [
                '🌆 Shibuya Sky — book timed tickets online (¥2,000)',
                '🚶 Walk Shibuya Crossing at dusk when the neon lights up',
                '📸 Best Crossing photo: Shibuya Sky or Starbucks on the corner'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Uobei Shibuya',
              description: 'High-tech conveyor belt sushi — order on a touchscreen and plates arrive by express lane. Fun, fresh, and incredibly cheap. ¥100-200 per plate.',
              meta: '💰 $ · 📍 Shibuya · No reservation needed'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6764, lng: 139.6993, label: 'Meiji Jingū Shrine', num: 1, cat: 'attraction', desc: 'Serene Shinto shrine in a vast urban forest' },
        { lat: 35.6654, lng: 139.7122, label: 'Omotesandō', num: 2, cat: 'attraction', desc: 'Architecture-lined boulevard by world-class designers' },
        { lat: 35.6650, lng: 139.7127, label: 'Anniversaire Café', num: 3, cat: 'food', desc: 'Terrace café on Omotesandō boulevard' },
        { lat: 35.6595, lng: 139.7004, label: 'Shibuya Crossing', num: 4, cat: 'attraction', desc: 'World\'s busiest pedestrian crossing' },
        { lat: 35.6584, lng: 139.7022, label: 'Shibuya Sky', num: 5, cat: 'attraction', desc: '230m observation deck with outdoor terrace' },
        { lat: 35.6599, lng: 139.6988, label: 'Uobei Shibuya', num: 6, cat: 'food', desc: 'High-tech conveyor belt sushi — ¥100/plate' }
      ]
    },
    {
      num: 7,
      date: '2026-10-19',
      neighborhoods: 'Hakone (day trip)',
      title: 'Hakone Day Trip — Hot Springs, Art & Lake Views',
      description: "Escape Tokyo for Hakone — a mountain resort town famous for hot springs, the Open-Air Museum, and views of Mt Fuji across Lake Ashi. The Hakone Free Pass covers trains, cable cars, boats, and buses in a scenic loop.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Romancecar to Hakone & Open-Air Museum',
              description: 'Take the Odakyu Romancecar from Shinjuku (85 mins, reserved seats, scenic). The Hakone Open-Air Museum displays large-scale sculptures by Picasso, Moore, and Miró in a hillside garden with mountain views.',
              details: [
                '🚃 Romancecar departs Shinjuku — front seats have panoramic windows',
                '🎨 Picasso Pavilion with 300+ works',
                '♿ Garden paths are mostly accessible (some slopes)',
                '⏰ ¥1,600 admission · Allow 2 hours'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The Hakone Free Pass (¥6,100 from Shinjuku, 2-day) covers the Romancecar, all Hakone transport, and discounts at museums. Great value even for a day trip.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Lake Ashi Cruise & Hakone Shrine',
              description: 'Ride the Hakone Ropeway over volcanic Ōwakudani valley, then board a pirate-ship replica across Lake Ashi. Hakone Shrine\'s red torii gate stands in the lake — iconic and serene.',
              details: [
                '🚡 Ropeway over Ōwakudani — volcanic steam vents and sulphur smell',
                '🥚 Try the famous black eggs (kuro-tamago) at Ōwakudani — adds 7 years to your life!',
                '⛩️ Hakone Shrine — vermillion torii gate in the lake',
                '🗻 Clear days: Mt Fuji visible across the lake'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Hakone Bakery & Table',
              description: 'Charming café near the Open-Air Museum with fresh-baked bread, soups, and mountain views from the terrace.',
              meta: '💰 $ · 📍 Near Open-Air Museum station'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Tokyo',
              description: 'Take the Romancecar back to Shinjuku (evening service). Rest your legs and enjoy the mountain scenery fading into city lights.',
              details: [
                '🚃 Last Romancecar departs around 8pm',
                '♨️ If time allows, soak tired feet at a free ashiyu (foot bath) near the station'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ichiran Ramen Shinjuku',
              description: 'Iconic tonkotsu ramen chain with individual booth seating. Customise your broth richness, noodle firmness, and garlic level on a paper form.',
              meta: '💰 $ · 📍 Shinjuku · Open late'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.2417, lng: 139.0051, label: 'Hakone Open-Air Museum', num: 1, cat: 'attraction', desc: 'Sculpture garden with Picasso Pavilion' },
        { lat: 35.2292, lng: 139.0206, label: 'Ōwakudani', num: 2, cat: 'attraction', desc: 'Volcanic valley with black eggs and views' },
        { lat: 35.2037, lng: 139.0225, label: 'Lake Ashi', num: 3, cat: 'attraction', desc: 'Scenic lake with Mt Fuji views and pirate ship cruises' },
        { lat: 35.2107, lng: 139.0036, label: 'Hakone Shrine', num: 4, cat: 'attraction', desc: 'Lakeside shrine with iconic red torii gate' },
        { lat: 35.2380, lng: 139.0071, label: 'Hakone Bakery & Table', num: 5, cat: 'food', desc: 'Charming mountain café near the Open-Air Museum' }
      ]
    },
    // ===== TRAVEL DAY: Day 8 — Tokyo to Kyoto =====
    {
      num: 8,
      date: '2026-10-20',
      neighborhoods: 'Tokyo Station · Kyoto Station · Higashiyama',
      title: 'Bullet Train to Kyoto',
      description: "Board the Tōkaidō Shinkansen and watch the landscape transform from urban sprawl to rice paddies and mountains in just over 2 hours. Settle into Kyoto and take an evening stroll through the atmospheric Higashiyama district.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinkansen to Kyoto',
              description: 'Take the Nozomi-class bullet train from Tokyo Station to Kyoto — 2 hours 15 minutes of smooth, silent speed at 285 km/h. Covered by your JR Pass (use Hikari service). On a clear day, Mt Fuji appears on the right side about 45 minutes in.',
              details: [
                '🚄 Hikari Shinkansen — covered by JR Pass (Nozomi is not)',
                '🗻 Sit on the right side (E seat) for Mt Fuji views',
                '🍱 Buy an ekiben (station bento) at Tokyo Station — it\'s a ritual',
                '⏰ Departs every 20-30 mins · Reserve seats at the JR office'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Tokyo Station\'s "Ekiben Matsuri" (Gransta underground) has 200+ bento varieties from across Japan. Pick a beautifully packaged one — it\'s half the Shinkansen experience.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In & Higashiyama Stroll',
              description: 'Settle into your Kyoto hotel and head to the Higashiyama district. Walk the gentle slopes of Ninenzaka and Sannenzaka — preserved Edo-period lanes lined with tea houses, ceramic shops, and sweet shops.',
              details: [
                '🏮 Ninenzaka & Sannenzaka — picturesque stone-paved lanes',
                '🍵 Stop for matcha and wagashi at a traditional tea house',
                '📸 Yasaka Pagoda (Hōkan-ji) — the iconic five-storey pagoda',
                '♿ Gentle slopes but some stone steps — take it slowly'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Gion Evening Walk',
              description: 'As dusk falls, walk through Gion — Kyoto\'s famous geisha district. Hanami-koji is the main street, lined with traditional machiya townhouses. If lucky, you\'ll spot a maiko (apprentice geisha) heading to an evening engagement.',
              details: [
                '🏮 Hanami-koji — the quintessential Kyoto street',
                '🎭 Respectful observation — don\'t chase or block geiko/maiko',
                '🌙 The lantern-lit streets are magical after dark'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Gion Kappa',
              description: 'Casual izakaya in Gion serving Kyoto-style obanzai (home cooking). Small dishes of seasonal vegetables, tofu, grilled fish — simple and delicious.',
              meta: '💰 $$ · 📍 Gion · Reservations helpful'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0116, lng: 135.7681, label: 'Kyoto Station', num: 1, cat: 'transport', desc: 'Futuristic station — gateway to Kyoto' },
        { lat: 34.9987, lng: 135.7806, label: 'Ninenzaka & Sannenzaka', num: 2, cat: 'attraction', desc: 'Preserved Edo-period lanes' },
        { lat: 34.9983, lng: 135.7808, label: 'Yasaka Pagoda', num: 3, cat: 'attraction', desc: 'Iconic five-storey pagoda' },
        { lat: 35.0037, lng: 135.7756, label: 'Gion', num: 4, cat: 'attraction', desc: 'Kyoto\'s famous geisha district' },
        { lat: 35.0040, lng: 135.7757, label: 'Gion Kappa', num: 5, cat: 'food', desc: 'Casual Kyoto-style obanzai izakaya' }
      ]
    },
    // ===== KYOTO: Days 9-13 =====
    {
      num: 9,
      date: '2026-10-21',
      neighborhoods: 'Fushimi · Southern Higashiyama',
      title: 'Fushimi Inari & Tofuku-ji',
      description: "Two of Kyoto's most powerful sights. Fushimi Inari's thousands of vermillion torii gates are mesmerising — go early to have them almost to yourself. Tōfuku-ji's bridge over a maple valley is one of Japan's greatest autumn views.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Fushimi Inari Taisha',
              description: 'The iconic tunnel of 10,000 vermillion torii gates climbing Mt Inari. You don\'t need to climb the full mountain — the first section (Senbon Torii) is the most photogenic and takes about 30 minutes of gentle walking.',
              details: [
                '⛩️ 10,000+ vermillion torii gates — Japan\'s most photographed shrine',
                '⏰ Arrive by 7am for empty corridors (shrine is 24/7)',
                '🥾 Walk the first loop only — flat to gentle incline (30-40 mins)',
                '🆓 Free admission always'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tōfuku-ji Temple',
              description: 'One of Kyoto\'s great Zen temples. The Tsūten-kyō (Bridge to Heaven) spans a valley that erupts in autumn colour. Even before peak foliage, the moss gardens and Zen rock gardens designed by Mirei Shigemori are stunning.',
              details: [
                '🍁 The bridge view over the maple valley is extraordinary',
                '🪨 Mirei Shigemori\'s modernist Zen garden — chequered moss and stone',
                '♿ Some areas have steps but main gardens are accessible',
                '⏰ ¥600 for gardens · ¥600 for bridge area'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Vermillion Café',
              description: 'Charming café right at the entrance to Fushimi Inari. Australian-owned, serving great coffee and Japanese-fusion brunch in a renovated machiya.',
              meta: '💰 $$ · 📍 Outside Fushimi Inari main gate'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Nishiki Market area',
              description: 'Explore Kyoto\'s "Kitchen" — a 400-year-old market street. Many stalls close by 5pm, but surrounding restaurants serve the same fresh ingredients. Try yuba (tofu skin), pickles, and grilled seafood skewers.',
              meta: '💰 $–$$ · 📍 Nishiki Market, Nakagyō · Best before 5pm for stalls'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari Taisha', num: 1, cat: 'attraction', desc: '10,000 vermillion torii gates' },
        { lat: 34.9769, lng: 135.7742, label: 'Tōfuku-ji Temple', num: 2, cat: 'attraction', desc: 'Zen temple with bridge over maple valley' },
        { lat: 34.9667, lng: 135.7734, label: 'Vermillion Café', num: 3, cat: 'food', desc: 'Great coffee right at Fushimi Inari\'s gate' },
        { lat: 35.0050, lng: 135.7649, label: 'Nishiki Market', num: 4, cat: 'food', desc: 'Kyoto\'s 400-year-old Kitchen market' }
      ]
    },
    {
      num: 10,
      date: '2026-10-22',
      neighborhoods: 'Kinkaku-ji · Ryōan-ji · Arashiyama',
      title: 'Golden Pavilion, Zen Garden & Bamboo Grove',
      description: "Three of Kyoto's most iconic experiences in one day. The shimmering Golden Pavilion, the enigmatic rock garden at Ryōan-ji, and the otherworldly bamboo grove of Arashiyama — connected by a scenic bus ride.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kinkaku-ji (Golden Pavilion)',
              description: 'The gold-leaf covered pavilion reflected in its mirror pond is one of Japan\'s most unforgettable sights. Arrive when it opens at 9am for calmer crowds and perfect morning light.',
              details: [
                '✨ Upper two floors covered in actual gold leaf',
                '📸 The reflection in the pond is the classic shot',
                '♿ Mostly flat paths around the pond',
                '⏰ 9am–5pm · ¥500'
              ]
            },
            {
              title: 'Ryōan-ji Zen Rock Garden',
              description: 'The world\'s most famous Zen garden — 15 rocks on raked white gravel, arranged so you can never see all 15 from any single viewpoint. Sit on the veranda and contemplate. The surrounding moss garden and pond are beautiful too.',
              details: [
                '🪨 15 rocks, 15 mysteries — a masterpiece of minimalism',
                '🧘 Sit quietly and let the garden work its magic',
                '📍 20 mins by bus from Kinkaku-ji',
                '⏰ ¥500 admission'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arashiyama Bamboo Grove & Tenryū-ji',
              description: 'Walk through the towering bamboo stalks of the Sagano Bamboo Grove — an otherworldly experience as light filters through swaying green canopies. Then visit Tenryū-ji, a UNESCO World Heritage temple with a spectacular borrowed-scenery garden.',
              details: [
                '🎋 Bamboo Grove — arrive early or late for fewer crowds',
                '🏯 Tenryū-ji garden designed by Musō Soseki (14th century)',
                '♿ Bamboo path is flat and paved',
                '🌊 The garden "borrows" Arashiyama mountain as backdrop'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Arashiyama Yoshimura',
              description: 'Handmade soba noodles with a view of the Togetsukyo Bridge and Arashiyama mountains. Simple, perfect, and quintessentially Kyoto.',
              meta: '💰 $$ · 📍 Overlooking Togetsukyo Bridge'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Togetsukyo Bridge at Dusk',
              description: 'The "Moon Crossing Bridge" is Arashiyama\'s centrepiece. Watch the mountains turn purple at dusk, then head back to central Kyoto by train.',
              details: [
                '🌙 Beautiful at dusk — mountains silhouetted against the sky',
                '🚃 JR Saga-Arashiyama station → Kyoto Station in 17 mins'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Omen Kodai-ji',
              description: 'Famous udon restaurant near Kodai-ji temple. Their signature udon comes with a basket of seasonal vegetables to dip in broth. Beautiful machiya building.',
              meta: '💰 $$ · 📍 Higashiyama · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0394, lng: 135.7292, label: 'Kinkaku-ji', num: 1, cat: 'attraction', desc: 'The Golden Pavilion — gold-leaf covered icon' },
        { lat: 35.0345, lng: 135.7183, label: 'Ryōan-ji', num: 2, cat: 'attraction', desc: 'World\'s most famous Zen rock garden' },
        { lat: 35.0173, lng: 135.6722, label: 'Arashiyama Bamboo Grove', num: 3, cat: 'attraction', desc: 'Towering bamboo forest pathway' },
        { lat: 35.0155, lng: 135.6749, label: 'Tenryū-ji', num: 4, cat: 'attraction', desc: 'UNESCO temple with borrowed-scenery garden' },
        { lat: 35.0122, lng: 135.6780, label: 'Togetsukyo Bridge', num: 5, cat: 'attraction', desc: '"Moon Crossing Bridge" — Arashiyama icon' },
        { lat: 35.0130, lng: 135.6790, label: 'Arashiyama Yoshimura', num: 6, cat: 'food', desc: 'Handmade soba with bridge views' }
      ]
    },
    {
      num: 11,
      date: '2026-10-23',
      neighborhoods: 'Nara (day trip)',
      title: 'Nara Day Trip — Deer, Great Buddha & Ancient Temples',
      description: "A gentle day trip to Japan's first permanent capital. Nara's friendly deer roam freely among 1,300-year-old temples and shrines. The Great Buddha at Tōdai-ji is awe-inspiring, and Nara Park is flat and perfect for a leisurely stroll.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'JR Train to Nara & Nara Park',
              description: 'Take the JR Nara Line from Kyoto (45 mins, covered by JR Pass). Walk from the station into Nara Park where over 1,000 sacred deer roam freely. Buy "shika senbei" (deer crackers) and make friends.',
              details: [
                '🦌 The deer are sacred messengers of the gods — treat them gently',
                '🍘 Shika senbei (¥200) — the deer know the drill',
                '♿ Nara Park is flat and spacious',
                '🚃 JR Nara Line: Kyoto → Nara, 45 mins'
              ]
            },
            {
              title: 'Tōdai-ji — The Great Buddha',
              description: 'One of Japan\'s most impressive temples. The Daibutsuden (Great Buddha Hall) is the world\'s largest wooden building, housing a 15-metre bronze Buddha cast in 752 AD. The scale is breathtaking.',
              details: [
                '🪷 15m bronze Vairocana Buddha — cast in 752 AD',
                '🏛️ World\'s largest wooden building (even after being rebuilt smaller!)',
                '♿ Flat approach, accessible interior',
                '⏰ ¥600 admission'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kasuga Taisha & Lantern Path',
              description: 'Walk the atmospheric path to Kasuga Grand Shrine, lined with 3,000 stone and bronze lanterns donated over centuries. During festivals they\'re all lit — but even by daylight, the moss-covered stone lanterns are magical.',
              details: [
                '🏮 3,000 lanterns — stone and bronze, centuries old',
                '🌿 The approach path through ancient cedar forest is beautiful',
                '♿ Mostly flat path with some gravel sections'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Kasuga-an',
              description: 'Traditional restaurant near Kasuga Shrine serving kakinoha-zushi (sushi wrapped in persimmon leaves) — a Nara specialty. Beautiful garden seating.',
              meta: '💰 $$ · 📍 Near Kasuga Taisha'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Kyoto',
              description: 'Take the JR train back to Kyoto. The ride is short enough that you\'ll be back in time for a relaxed dinner.',
              details: [
                '🚃 Trains run frequently until late evening'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Pontocho Alley restaurants',
              description: 'Pontocho is a narrow atmospheric alley along the Kamo River. Many restaurants have riverside terraces (kawadoko in summer). Choose any place that appeals — the setting is unbeatable.',
              meta: '💰 $$–$$$ · 📍 Pontocho, along the Kamo River'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6851, lng: 135.8048, label: 'Nara Park', num: 1, cat: 'attraction', desc: 'Open parkland with 1,000+ sacred deer' },
        { lat: 34.6890, lng: 135.8399, label: 'Tōdai-ji', num: 2, cat: 'attraction', desc: 'Great Buddha Hall — world\'s largest wooden building' },
        { lat: 34.6813, lng: 135.8498, label: 'Kasuga Taisha', num: 3, cat: 'attraction', desc: 'Grand shrine with 3,000 lanterns' },
        { lat: 34.6830, lng: 135.8470, label: 'Kasuga-an', num: 4, cat: 'food', desc: 'Persimmon-leaf sushi — a Nara specialty' },
        { lat: 35.0044, lng: 135.7707, label: 'Pontocho', num: 5, cat: 'food', desc: 'Atmospheric riverside dining alley in Kyoto' }
      ]
    },
    {
      num: 12,
      date: '2026-10-24',
      neighborhoods: 'Kyoto Design · Nishijin · Imperial Palace',
      title: 'Kyoto Crafts, Textiles & Design',
      description: "Kyoto is where Japan's design heritage lives. Today explores traditional craftsmanship — Nishijin textile weaving, the Kyoto Museum of Crafts, and the serene Imperial Palace grounds. A quieter, more reflective day.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Nishijin Textile Center',
              description: 'Nishijin is Kyoto\'s historic textile district, famous for elaborate kimono fabrics woven for centuries. The Textile Center has live weaving demonstrations, a small museum, and beautiful textiles for sale.',
              details: [
                '🧵 Live weaving demonstrations of Nishijin-ori silk brocade',
                '👘 Kimono fashion shows (schedule varies)',
                '🛍️ Beautiful scarves, ties, and accessories as souvenirs',
                '🆓 Free admission'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kyoto Museum of Crafts and Design',
              description: 'Hands-on museum showcasing 74 categories of Kyoto traditional crafts — ceramics, lacquerware, bamboo work, fans, dolls. Some days you can try hands-on workshops.',
              details: [
                '🎨 74 categories of traditional Kyoto crafts on display',
                '🖌️ Check for workshop availability — hands-on craft experiences',
                '♿ Fully accessible modern building',
                '🆓 Free admission'
              ]
            },
            {
              title: 'Kyoto Imperial Palace & Gardens',
              description: 'The former residence of Japan\'s emperor until 1868. The palace grounds are a vast, serene park with pine-lined gravel paths, ancient gates, and no crowds. Free self-guided tours of the palace interior.',
              details: [
                '🏯 Free entry and self-guided audio tour of palace interior',
                '🌳 Vast grounds perfect for a quiet walk',
                '♿ Flat gravel paths — wide and accessible',
                '📍 Enter from Imadegawa-gomon gate'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Saryō Hōsen',
              description: 'Beautiful kaiseki-style lunch in a traditional machiya near the Imperial Palace. Seasonal set meals with exquisite presentation — this is Kyoto dining at its most refined yet affordable.',
              meta: '💰 $$ · 📍 Near Imadegawa · Reservations recommended'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Giro Giro Hitoshina',
              description: 'Modern kaiseki in a casual, counter-seating setting. Watch the chef prepare each course — Japanese fine dining made approachable. A Michelin-starred favourite.',
              meta: '💰 $$$ · 📍 Kiyamachi, Kyoto · Book well ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0323, lng: 135.7508, label: 'Nishijin Textile Center', num: 1, cat: 'attraction', desc: 'Traditional silk weaving demonstrations' },
        { lat: 35.0115, lng: 135.7752, label: 'Kyoto Museum of Crafts', num: 2, cat: 'attraction', desc: '74 categories of Kyoto traditional crafts' },
        { lat: 35.0254, lng: 135.7624, label: 'Kyoto Imperial Palace', num: 3, cat: 'attraction', desc: 'Former emperor\'s residence with vast gardens' },
        { lat: 35.0260, lng: 135.7630, label: 'Saryō Hōsen', num: 4, cat: 'food', desc: 'Seasonal kaiseki lunch in a machiya' },
        { lat: 35.0035, lng: 135.7695, label: 'Giro Giro Hitoshina', num: 5, cat: 'food', desc: 'Michelin-starred casual kaiseki counter' }
      ]
    },
    {
      num: 13,
      date: '2026-10-25',
      neighborhoods: 'Philosopher\'s Path · Nanzen-ji · Ginkaku-ji',
      title: 'Philosopher\'s Path — Silver Pavilion to Nanzen-ji',
      description: "One of the world's great walks. The Philosopher's Path is a 2km canal-side path lined with cherry and maple trees, connecting Ginkaku-ji (Silver Pavilion) to Nanzen-ji temple. Flat, gentle, and profoundly beautiful.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Ginkaku-ji (Silver Pavilion)',
              description: 'Despite its name, the Silver Pavilion was never covered in silver — its beauty lies in its restrained wabi-sabi aesthetics. The sand garden with its perfect cone (representing Mt Fuji) and the moss garden are exquisite.',
              details: [
                '🏯 Wabi-sabi perfection — understated beauty over gold',
                '🪨 Unique sand garden with sculpted cone and wave patterns',
                '🌿 Moss garden and hillside trail with panoramic views',
                '⏰ ¥500 · Opens 8:30am'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Philosopher\'s Path Walk',
              description: 'Named after philosopher Nishida Kitarō who walked this route daily. The 2km stone path follows a canal shaded by cherry and maple trees. Stop at small temples, tea houses, and craft shops along the way.',
              details: [
                '🚶 2km flat canal-side path — gentle and beautiful',
                '🍁 Early autumn colour may be starting on the maples',
                '🍵 Several tea houses along the path for rest stops',
                '🐱 Famous for its neighbourhood cats'
              ]
            },
            {
              title: 'Nanzen-ji Temple',
              description: 'A vast Zen temple complex at the path\'s southern end. The massive Sanmon gate offers panoramic views (steep stairs), but the grounds, gardens, and the brick Roman-style aqueduct are all at ground level and stunning.',
              details: [
                '🏛️ Brick aqueduct — a surprising East-meets-West architectural gem',
                '🪨 Multiple sub-temple gardens to explore',
                '♿ Grounds and aqueduct are accessible; Sanmon gate has steep stairs (optional)',
                '⏰ Grounds free · Sub-temples ¥300-600'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Ōmen Philosopher\'s Path',
              description: 'Branch of the famous udon restaurant right on the Philosopher\'s Path. Their signature udon with seasonal vegetable basket is perfect fuel for the walk.',
              meta: '💰 $$ · 📍 On the Philosopher\'s Path'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Eikan-dō (Zenrin-ji) Temple',
              description: 'Just south of the Philosopher\'s Path, Eikan-dō is famous for its autumn illumination (late November) but the gardens and the unique "looking-back Amida Buddha" are worth visiting anytime.',
              details: [
                '🪷 The Mikaeri Amida — a Buddha statue looking over its shoulder',
                '🍁 One of Kyoto\'s top autumn colour spots'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Hiranoya',
              description: 'Traditional tofu restaurant near Nanzen-ji, serving yudofu (simmered tofu) — Kyoto\'s most iconic dish. Simple, warming, and deeply satisfying in a historic building.',
              meta: '💰 $$ · 📍 Near Nanzen-ji'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0270, lng: 135.7983, label: 'Ginkaku-ji', num: 1, cat: 'attraction', desc: 'Silver Pavilion — wabi-sabi perfection' },
        { lat: 35.0196, lng: 135.7940, label: 'Philosopher\'s Path', num: 2, cat: 'attraction', desc: '2km canal walk lined with maples' },
        { lat: 35.0107, lng: 135.7928, label: 'Nanzen-ji', num: 3, cat: 'attraction', desc: 'Grand Zen temple with brick aqueduct' },
        { lat: 35.0130, lng: 135.7946, label: 'Eikan-dō', num: 4, cat: 'attraction', desc: 'Beautiful temple with autumn fame' },
        { lat: 35.0220, lng: 135.7950, label: 'Ōmen', num: 5, cat: 'food', desc: 'Famous udon on the Philosopher\'s Path' },
        { lat: 35.0100, lng: 135.7920, label: 'Hiranoya', num: 6, cat: 'food', desc: 'Traditional yudofu near Nanzen-ji' }
      ]
    },
    // ===== TRAVEL DAY: Day 14 — Kyoto to Osaka =====
    {
      num: 14,
      date: '2026-10-26',
      neighborhoods: 'Kyoto Station · Osaka · Namba',
      title: 'Train to Osaka — Japan\'s Kitchen',
      description: "A short JR ride from Kyoto to Osaka (30 mins) brings you to Japan's most food-obsessed city. The locals say 'kuidaore' — eat until you drop. Tonight, that's exactly the plan in Dōtonbori.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'JR Special Rapid to Osaka',
              description: 'Take the JR Special Rapid from Kyoto Station to Osaka Station — just 29 minutes and covered by your JR Pass. Drop bags at your hotel in the Namba area.',
              details: [
                '🚃 JR Special Rapid: Kyoto → Osaka in 29 mins',
                '🏨 Stay near Namba or Shinsaibashi for food and nightlife access',
                '🎫 JR Pass covers this route'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Osaka Castle & Park',
              description: 'Osaka Castle is the city\'s icon — a reconstructed castle tower surrounded by huge stone walls and a beautiful park. The top floor has panoramic city views. An elevator goes to the 5th floor, reducing stair climbing.',
              details: [
                '🏯 5th floor elevator + stairs to 8th floor observation deck',
                '🌳 Castle park is flat and perfect for a gentle stroll',
                '📸 Best castle photos from the southwest side across the moat',
                '⏰ ¥600 admission · 9am–5pm'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Osaka Castle area — Mitsui Garden Hotel Buffet',
              description: 'Many restaurants near the castle serve Osaka comfort food. Try okonomiyaki or a casual set lunch.',
              meta: '💰 $$ · 📍 Osaka Castle Park area'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dōtonbori — Osaka\'s Neon Food Paradise',
              description: 'The most exciting food street in Japan. Giant animated signs (the running Glico Man, the moving crab), street food stalls, and more restaurants per square metre than anywhere else. Walk, eat, repeat.',
              details: [
                '🦀 Kani Dōraku — iconic giant mechanical crab sign',
                '🏃 Glico Running Man sign — the photo everyone takes',
                '🍢 Street food heaven — takoyaki, okonomiyaki, kushikatsu everywhere',
                '📍 Walk along the canal for the full neon spectacle'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Dōtonbori Street Food Crawl',
              description: 'Skip the sit-down restaurant — eat your way through Dōtonbori. Must-tries: takoyaki from Kukuru, okonomiyaki from Mizuno, and kushikatsu from Daruma.',
              meta: '💰 $–$$ · 📍 Dōtonbori, Namba · No reservations needed'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6873, lng: 135.5262, label: 'Osaka Castle', num: 1, cat: 'attraction', desc: 'Osaka\'s iconic castle with panoramic views' },
        { lat: 34.6687, lng: 135.5013, label: 'Dōtonbori', num: 2, cat: 'food', desc: 'Osaka\'s legendary neon-lit food street' },
        { lat: 34.6685, lng: 135.5012, label: 'Glico Man Sign', num: 3, cat: 'attraction', desc: 'The iconic running man — Osaka\'s selfie spot' },
        { lat: 34.6690, lng: 135.5023, label: 'Kukuru Takoyaki', num: 4, cat: 'food', desc: 'Famous takoyaki (octopus balls)' },
        { lat: 34.6686, lng: 135.5008, label: 'Mizuno Okonomiyaki', num: 5, cat: 'food', desc: 'Legendary okonomiyaki since 1945' }
      ]
    },
    // ===== OSAKA: Days 15-17 =====
    {
      num: 15,
      date: '2026-10-27',
      neighborhoods: 'Shinsekai · Tennōji · Abeno',
      title: 'Retro Osaka — Shinsekai & Tennōji',
      description: "Explore Osaka's most characterful neighbourhood. Shinsekai (\"New World\") is a wonderfully retro district of neon-lit kushikatsu joints, Tsūtenkaku Tower, and old-school arcade vibes. Then visit the tranquil Tennōji Temple and park.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinsekai District',
              description: 'This wonderfully tacky neighbourhood was built in 1912 inspired by Paris and Coney Island. Now it\'s a nostalgic maze of neon signs, kushikatsu restaurants, retro game centres, and the Tsūtenkaku Tower. Maximum Osaka character.',
              details: [
                '🗼 Tsūtenkaku Tower — Osaka\'s retro Eiffel Tower. Observation deck with city views.',
                '🍡 Kushikatsu alley — deep-fried skewers are king here',
                '🎮 Retro game centres and pachinko parlours',
                '♿ Flat streets, easy walking'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Kushikatsu Daruma (Shinsekai)',
              description: 'The original Daruma — Osaka\'s most famous kushikatsu restaurant. Crispy deep-fried skewers of everything: shrimp, lotus root, quail eggs. The golden rule: no double-dipping in the communal sauce!',
              meta: '💰 $ · 📍 Shinsekai · Counter service'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tennōji Park & Keitaku-en Garden',
              description: 'A calm contrast to Shinsekai\'s energy. Tennōji Park has a beautiful Edo-period garden (Keitaku-en) with a circular walking path around a central pond. Flat, quiet, and lovely.',
              details: [
                '🌿 Keitaku-en — circular pond garden, beautifully maintained',
                '♿ Flat paths throughout',
                '🏛️ Adjacent Osaka City Museum of Fine Arts',
                '⏰ ¥150 garden admission'
              ]
            },
            {
              title: 'Abeno Harukas',
              description: 'Japan\'s tallest building (300m) with an observation deck called Harukas 300. On clear days, you can see from Kobe to Nara. The 360° views are spectacular.',
              details: [
                '🏙️ Japan\'s tallest building — 300m observation deck',
                '♿ Elevator access to all floors',
                '⏰ ¥1,500 admission for Harukas 300'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ajinoya (Namba)',
              description: 'Outstanding okonomiyaki restaurant in Namba. Watch the chef expertly prepare your savoury pancake on the teppan grill right in front of you. Try the "mix modern" with pork, shrimp, and squid.',
              meta: '💰 $$ · 📍 Namba · Teppan counter seating'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6524, lng: 135.5063, label: 'Shinsekai', num: 1, cat: 'attraction', desc: 'Retro neon district with kushikatsu and arcades' },
        { lat: 34.6534, lng: 135.5065, label: 'Tsūtenkaku Tower', num: 2, cat: 'attraction', desc: 'Osaka\'s retro Eiffel Tower' },
        { lat: 34.6524, lng: 135.5063, label: 'Kushikatsu Daruma', num: 3, cat: 'food', desc: 'The original — no double-dipping!' },
        { lat: 34.6476, lng: 135.5133, label: 'Tennōji Park', num: 4, cat: 'attraction', desc: 'Tranquil Edo-period garden in the city' },
        { lat: 34.6462, lng: 135.5133, label: 'Abeno Harukas', num: 5, cat: 'attraction', desc: 'Japan\'s tallest building — 300m views' },
        { lat: 34.6667, lng: 135.5018, label: 'Ajinoya', num: 6, cat: 'food', desc: 'Top-rated okonomiyaki in Namba' }
      ]
    },
    {
      num: 16,
      date: '2026-10-28',
      neighborhoods: 'Naoshima Island (day trip)',
      title: 'Naoshima Art Island Day Trip',
      description: "A bucket-list day trip to Naoshima — the art island. Tadao Ando's museums, Yayoi Kusama's pumpkins, and art installations scattered across a sleepy fishing village. Accessible by ferry and surprisingly easy from Osaka.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinkansen + Ferry to Naoshima',
              description: 'Take the Shinkansen from Shin-Osaka to Okayama (50 mins), then JR Marine Liner to Uno Port (50 mins), and ferry to Naoshima (20 mins). Sounds complex but it\'s smooth — all JR segments covered by your pass.',
              details: [
                '🚄 Shin-Osaka → Okayama: Hikari Shinkansen, 50 mins',
                '🚃 Okayama → Uno: JR Marine Liner, 50 mins',
                '⛴️ Uno → Naoshima (Miyanoura): ferry 20 mins (¥300)',
                '⏰ Depart Osaka by 7:30am to arrive by 10am'
              ]
            },
            {
              title: 'Chichu Art Museum',
              description: 'Tadao Ando\'s masterpiece — a museum built entirely underground to preserve the landscape. Three artists: Monet water lilies (in natural light), James Turrell light installations, and Walter De Maria\'s sphere room. Profoundly moving.',
              details: [
                '🏛️ Tadao Ando\'s concrete masterwork — entirely underground',
                '🎨 Monet\'s Water Lilies in a room of pure natural light',
                '💡 James Turrell light rooms — transcendent experience',
                '🎫 ¥2,100 · Book timed tickets online in advance'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Art House Project & Village Walk',
              description: 'Abandoned village houses converted into art installations by renowned artists. Walk through the quiet streets of Honmura village, popping into houses that have been transformed into immersive artworks. James Turrell\'s "Backside of the Moon" is unforgettable.',
              details: [
                '🏘️ 7 house-installations across the village',
                '🎫 ¥1,050 for all houses (or ¥420 each)',
                '♿ Mostly flat village streets, some narrow entries',
                '🎨 Turrell, Miyajima, Ōtake — world-class artists'
              ]
            },
            {
              title: 'Yayoi Kusama\'s Yellow Pumpkin',
              description: 'The polka-dotted yellow pumpkin on the pier at Benesse House is one of the world\'s most photographed sculptures. A playful icon of the island\'s creative spirit.',
              details: [
                '🎃 Yellow Pumpkin — on the pier at Benesse House area',
                '📸 Also look for the Red Pumpkin at Miyanoura port',
                '🆓 Outdoor sculptures are free to view'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Café Salon Naka-Oku',
              description: 'Tiny café in a renovated village house serving homemade curry and coffee. The kind of place that captures Naoshima\'s spirit perfectly.',
              meta: '💰 $ · 📍 Honmura village'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Osaka',
              description: 'Reverse the morning journey: ferry to Uno, JR to Okayama, Shinkansen to Osaka. You\'ll be back by early evening.',
              details: [
                '⛴️ Last useful ferry: ~4:30pm',
                '🚄 Back in Osaka by ~7pm'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ippudo Namba',
              description: 'Legendary tonkotsu ramen chain born in Fukuoka. The "Akamaru Modern" — rich pork broth with garlic oil and miso — is pure comfort after a day of art and travel.',
              meta: '💰 $ · 📍 Namba'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.4603, lng: 133.9953, label: 'Chichu Art Museum', num: 1, cat: 'attraction', desc: 'Tadao Ando\'s underground museum — Monet, Turrell' },
        { lat: 34.4554, lng: 134.0024, label: 'Art House Project', num: 2, cat: 'attraction', desc: 'Village houses transformed into art installations' },
        { lat: 34.4530, lng: 133.9960, label: 'Yellow Pumpkin', num: 3, cat: 'attraction', desc: 'Kusama\'s iconic polka-dot pumpkin' },
        { lat: 34.4570, lng: 134.0020, label: 'Café Salon Naka-Oku', num: 4, cat: 'food', desc: 'Tiny village café with homemade curry' },
        { lat: 34.6690, lng: 135.5010, label: 'Ippudo Namba', num: 5, cat: 'food', desc: 'Legendary tonkotsu ramen' }
      ]
    },
    {
      num: 17,
      date: '2026-10-29',
      neighborhoods: 'Umeda · Nakanoshima · Kitahama',
      title: 'North Osaka — Design, Markets & River Walks',
      description: "Explore Osaka's sophisticated northern districts. Umeda Sky Building's futuristic architecture, the riverside art district of Nakanoshima, and the morning market scene at Kuromon — a perfect balance of modern design and street-level culture.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kuromon Ichiba Market',
              description: 'Osaka\'s "Kitchen" — a 190-year-old covered market packed with fresh seafood stalls, street food vendors, and local produce. Try fresh sashimi, grilled scallops, tamagoyaki (sweet omelette), and seasonal fruits.',
              details: [
                '🦐 Fresh uni, crab legs, and tuna sashimi at the stalls',
                '🍳 Tamagoyaki — fluffy Japanese omelette on a stick',
                '🍊 Japanese fruits are works of art (and expensive!)',
                '⏰ Best before noon — stalls wind down by 4pm'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nakanoshima — River Island Art District',
              description: 'A peaceful island between two rivers, home to the Nakanoshima Museum of Art (opened 2022), the beautiful brick-built Central Public Hall, and tree-lined riverside walks.',
              details: [
                '🏛️ Nakanoshima Museum of Art — modern/contemporary collection in striking black building',
                '🧱 Osaka Central Public Hall (1918) — gorgeous neo-Renaissance building',
                '🌳 Riverside promenades are flat and perfect for a stroll'
              ]
            },
            {
              title: 'Umeda Sky Building',
              description: 'Hiroshi Hara\'s futuristic twin towers connected by a "Floating Garden Observatory" on the 39th floor. The glass-tube escalator between the towers is a design experience itself.',
              details: [
                '🏗️ Visionary 1993 design — still looks like it\'s from the future',
                '🌆 360° open-air rooftop deck',
                '♿ Elevators to all levels',
                '⏰ ¥1,500 admission'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Garb Weeks (Nakanoshima)',
              description: 'Stylish riverside café-restaurant on Nakanoshima with terrace seating overlooking the river. Great lunch sets and craft beer.',
              meta: '💰 $$ · 📍 Nakanoshima, riverside'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Takoyaki Wanaka (Namba)',
              description: 'Join the locals for Osaka\'s signature dish — takoyaki (octopus balls). Wanaka makes them crispy outside, creamy inside. Get the "negi-ponzu" version for a refreshing twist.',
              meta: '💰 $ · 📍 Namba area'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6688, lng: 135.5072, label: 'Kuromon Market', num: 1, cat: 'food', desc: 'Osaka\'s 190-year-old Kitchen market' },
        { lat: 34.6917, lng: 135.4925, label: 'Nakanoshima Museum of Art', num: 2, cat: 'attraction', desc: 'Modern art in a striking black building (2022)' },
        { lat: 34.6932, lng: 135.5033, label: 'Central Public Hall', num: 3, cat: 'attraction', desc: 'Beautiful 1918 neo-Renaissance building' },
        { lat: 34.7052, lng: 135.4879, label: 'Umeda Sky Building', num: 4, cat: 'attraction', desc: 'Futuristic twin towers with floating observatory' },
        { lat: 34.6930, lng: 135.4940, label: 'Garb Weeks', num: 5, cat: 'food', desc: 'Riverside café on Nakanoshima' },
        { lat: 34.6665, lng: 135.5015, label: 'Takoyaki Wanaka', num: 6, cat: 'food', desc: 'Osaka\'s best takoyaki' }
      ]
    },
    // ===== RETURN TO TOKYO: Days 18-21 =====
    {
      num: 18,
      date: '2026-10-30',
      neighborhoods: 'Osaka · Tokyo · Shimokitazawa',
      title: 'Back to Tokyo — Shimokitazawa & Vinyl',
      description: "Return to Tokyo by Shinkansen for your final stretch. Spend the afternoon in Shimokitazawa — Tokyo's bohemian neighbourhood of vintage shops, independent cafés, and live music venues. A completely different Tokyo vibe.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinkansen to Tokyo',
              description: 'Hikari Shinkansen from Shin-Osaka to Tokyo (2 hrs 45 mins). One last ekiben for the road — Osaka\'s specialty bentos are different from Tokyo\'s.',
              details: [
                '🚄 Hikari: Shin-Osaka → Tokyo, 2h45m · JR Pass covered',
                '🍱 Try an Osaka ekiben — different specialties than Tokyo'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shimokitazawa — Tokyo\'s Bohemian Village',
              description: 'A walkable neighbourhood of narrow lanes filled with vintage clothing shops, second-hand record stores, independent cafés, and tiny theatres. Recently reimagined with new low-rise development under the train tracks.',
              details: [
                '🎵 Disk Union and other vinyl record shops',
                '👕 Vintage clothing — some of Tokyo\'s best thrift stores',
                '☕ Bear Pond Espresso — cult-status coffee shop',
                '🏗️ Bonus Track — new mixed-use development under the tracks'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'City Country City',
              description: 'Tiny second-floor café in Shimokitazawa with records, books, and excellent coffee. Run by a former music journalist. Very "Shimokita."',
              meta: '💰 $ · 📍 Shimokitazawa · Look for the narrow staircase'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Shirube (Shimokitazawa)',
              description: 'Cosy standing bar and izakaya popular with locals. Natural wine, small plates, and friendly Shimokita atmosphere. A perfect neighbourhood dinner.',
              meta: '💰 $$ · 📍 Shimokitazawa'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6614, lng: 139.6681, label: 'Shimokitazawa', num: 1, cat: 'attraction', desc: 'Bohemian neighbourhood — vintage, vinyl, cafés' },
        { lat: 35.6610, lng: 139.6677, label: 'Bear Pond Espresso', num: 2, cat: 'food', desc: 'Cult-status coffee shop' },
        { lat: 35.6619, lng: 139.6672, label: 'Bonus Track', num: 3, cat: 'attraction', desc: 'New development under the train tracks' },
        { lat: 35.6612, lng: 139.6685, label: 'City Country City', num: 4, cat: 'food', desc: 'Records, books, and coffee upstairs' },
        { lat: 35.6608, lng: 139.6679, label: 'Shirube', num: 5, cat: 'food', desc: 'Local standing bar and izakaya' }
      ]
    },
    {
      num: 19,
      date: '2026-10-31',
      neighborhoods: 'Tsukiji · Toyosu · Kappabashi · Tokyo Skytree',
      title: 'Markets, Kitchen Street & Skytree',
      description: "Explore Tokyo's food culture at ground level. The old Tsukiji Outer Market is still thriving with food stalls, Kappabashi is a street of kitchen supply shops (knives!), and Tokyo Skytree offers the highest views in the city.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tsukiji Outer Market',
              description: 'While the inner wholesale market moved to Toyosu, the outer market remains — a dense warren of food stalls, sushi restaurants, and vendors selling the freshest fish, omelettes, and street snacks in Tokyo.',
              details: [
                '🍣 Fresh sushi breakfast at the small counter restaurants',
                '🥚 Tamagoyaki (sweet omelette) stalls — eat on the spot',
                '🔪 Kitchen knife shops with English-speaking staff',
                '⏰ Best 7am–11am · Many stalls close by 2pm'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kappabashi Kitchen Street',
              description: 'A whole street dedicated to kitchen and restaurant supplies. Over 170 shops selling Japanese knives, ceramics, plastic food samples (sampuru), lacquerware, and everything a cook could want. Great for souvenirs.',
              details: [
                '🔪 Japanese kitchen knives — world-class craftsmanship',
                '🍱 Bento boxes, chopsticks, and beautiful ceramics',
                '🍜 Plastic food samples (sampuru) — unique Japanese art form',
                '📍 Between Ueno and Asakusa — flat, easy walking'
              ]
            },
            {
              title: 'Tokyo Skytree',
              description: 'At 634m, the tallest tower in Japan. The observation decks at 350m and 450m offer views to the horizon on clear days. The design references traditional Japanese aesthetics with a modern twist.',
              details: [
                '🗼 634m — tallest structure in Japan',
                '♿ Fully accessible — elevators to all decks',
                '🌅 Late afternoon visit for daylight + sunset + night views',
                '⏰ ¥2,100 for Tembo Deck (350m)'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Asakusa area soba',
              description: 'Stop for handmade soba noodles near Kappabashi/Asakusa. Many traditional soba shops have been serving the same recipes for generations.',
              meta: '💰 $ · 📍 Asakusa area'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Hoppy Street (Asakusa)',
              description: 'A festive alley of outdoor izakayas near Sensō-ji. Locals gather here for hoppy (a beer-like drink), grilled skewers, and nikomi (beef stew). Rowdy, fun, and very Shitamachi.',
              meta: '💰 $ · 📍 Near Sensō-ji, Asakusa'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6654, lng: 139.7707, label: 'Tsukiji Outer Market', num: 1, cat: 'food', desc: 'Legendary food market — sushi, omelettes, knives' },
        { lat: 35.7129, lng: 139.7837, label: 'Kappabashi Kitchen Street', num: 2, cat: 'attraction', desc: '170+ kitchen supply shops — knives, ceramics, sampuru' },
        { lat: 35.7101, lng: 139.8107, label: 'Tokyo Skytree', num: 3, cat: 'attraction', desc: '634m tower with panoramic observation decks' },
        { lat: 35.7150, lng: 139.7960, label: 'Hoppy Street', num: 4, cat: 'food', desc: 'Festive izakaya alley near Sensō-ji' }
      ]
    },
    {
      num: 20,
      date: '2026-11-01',
      neighborhoods: 'Daikanyama · Nakameguro · Ebisu',
      title: 'Tokyo\'s Design Triangle — Daikanyama, Nakameguro & Ebisu',
      description: "Your penultimate day explores Tokyo's most design-forward neighbourhoods. Daikanyama T-Site is the world's most beautiful bookstore, Nakameguro's canal is lined with boutiques, and Ebisu has craft beer and photography.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Daikanyama T-Site (Tsutaya Books)',
              description: 'Often called the world\'s most beautiful bookstore. Three interlocking buildings by Klein Dytham Architecture, wrapped in a lattice of T-shaped panels. Inside: a curated selection of art, design, travel, and lifestyle books, plus a Starbucks and magazine lounge.',
              details: [
                '📚 Stunning architecture + curated design/art book selection',
                '☕ Anjin lounge upstairs — cocktails and vinyl in a book-lined room',
                '🏗️ Klein Dytham Architecture — lattice façade is beautiful',
                '♿ Accessible ground floor; some steps to upper lounge'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nakameguro Canal Walk',
              description: 'The Meguro River canal is lined with cherry trees (famous in spring) and year-round boutiques, cafés, and design shops. A flat, relaxing walk through one of Tokyo\'s most stylish areas.',
              details: [
                '🌸 Famous for cherry blossoms in spring, lovely in autumn too',
                '🛍️ Independent boutiques and design shops along the canal',
                '☕ Onibus Coffee — one of Tokyo\'s best speciality roasters',
                '📍 Walk from Daikanyama — they\'re adjacent'
              ]
            },
            {
              title: 'Tokyo Photographic Art Museum (Ebisu)',
              description: 'Japan\'s first museum dedicated to photography and moving image. Rotating exhibitions of Japanese and international photography in a modern building within Yebisu Garden Place.',
              details: [
                '📷 Rotating exhibitions — check what\'s on',
                '♿ Fully accessible',
                '🍺 Yebisu Garden Place has the Museum of Yebisu Beer next door',
                '⏰ ¥700–1,200 depending on exhibition'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Onibus Coffee + Sandwich',
              description: 'Outstanding speciality coffee roaster in Nakameguro. Simple, beautiful space in a converted house. Their pour-over is exceptional.',
              meta: '💰 $ · 📍 Nakameguro canal area'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Yebisu Beer Museum & Garden Place',
              description: 'Free self-guided tour of the Yebisu Beer Museum (birthplace of Yebisu brand), followed by a tasting set. Yebisu Garden Place is a pleasant European-style complex for an evening stroll.',
              details: [
                '🍺 Free entry · Tasting set ¥400',
                '🎄 The central plaza is beautifully lit in the evening'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Afuri Ramen (Ebisu)',
              description: 'Famous for their yuzu shio (citrus salt) ramen — light, fragrant, and completely different from heavy tonkotsu. The perfect penultimate dinner.',
              meta: '💰 $ · 📍 Ebisu · Counter service'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6498, lng: 139.7006, label: 'Daikanyama T-Site', num: 1, cat: 'attraction', desc: 'World\'s most beautiful bookstore' },
        { lat: 35.6440, lng: 139.6990, label: 'Nakameguro Canal', num: 2, cat: 'attraction', desc: 'Stylish canal-side neighbourhood' },
        { lat: 35.6460, lng: 139.6982, label: 'Onibus Coffee', num: 3, cat: 'food', desc: 'Tokyo\'s top speciality coffee' },
        { lat: 35.6472, lng: 139.7133, label: 'Tokyo Photographic Art Museum', num: 4, cat: 'attraction', desc: 'Japan\'s first photography museum' },
        { lat: 35.6467, lng: 139.7134, label: 'Yebisu Beer Museum', num: 5, cat: 'attraction', desc: 'Free beer museum with tastings' },
        { lat: 35.6470, lng: 139.7100, label: 'Afuri Ramen', num: 6, cat: 'food', desc: 'Famous yuzu shio ramen — light and citrusy' }
      ]
    },
    {
      num: 21,
      date: '2026-11-02',
      neighborhoods: 'Shinjuku · Narita Airport',
      title: 'Farewell Tokyo — Last Bites & Departure',
      description: "Your final morning in Japan. Enjoy a relaxed breakfast, pick up last-minute souvenirs at the station, and take the Narita Express to the airport. Sayōnara — until next time.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinjuku Gyoen National Garden',
              description: 'If time allows before checkout, visit this stunning garden — Japanese, English, and French garden styles in one park. Chrysanthemums may be blooming in early November. A peaceful farewell to Tokyo.',
              details: [
                '🌳 Three garden styles — Japanese, English, French',
                '🌼 Early November may bring chrysanthemum displays',
                '♿ Mostly flat paths, accessible',
                '⏰ ¥500 · Opens 9am · Closed Mondays'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Sarabeth\'s Shinjuku',
              description: 'Popular brunch spot with excellent eggs benedict and fluffy pancakes. A comfortable, Western-style farewell breakfast.',
              meta: '💰 $$ · 📍 Lumine 2, Shinjuku Station building'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Last Souvenirs & Narita Express',
              description: 'Tokyo Station and Shinjuku have excellent souvenir areas (look for "Tokyo Banana," matcha Kit-Kats, and regional wagashi). Then board the Narita Express for the airport — your JR Pass covers it one last time.',
              details: [
                '🎁 Tokyo Banana, Royce chocolate, matcha Kit-Kats — classic omiyage',
                '🚃 Narita Express: Shinjuku → Narita, 90 mins · JR Pass covered',
                '✈️ Arrive at airport 3 hours before international flights',
                '🙏 Sayōnara — thank you, Japan!'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Don\'t forget to return your Suica IC card at the airport JR counter for a refund of the ¥500 deposit plus remaining balance. Or keep it as a souvenir — it works for 10 years.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6852, lng: 139.7100, label: 'Shinjuku Gyoen', num: 1, cat: 'attraction', desc: 'Beautiful garden — a peaceful farewell' },
        { lat: 35.6896, lng: 139.6922, label: 'Shinjuku Station', num: 2, cat: 'transport', desc: 'Souvenir shops and Narita Express departure' },
        { lat: 35.6896, lng: 139.6930, label: 'Sarabeth\'s', num: 3, cat: 'food', desc: 'Farewell brunch in Shinjuku' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$80–150/night', midrange: '$150–300/night', luxury: '$300–600/night' },
    { category: 'Meals (per couple)', budget: '$50–80/day', midrange: '$80–150/day', luxury: '$150–300/day' },
    { category: 'JR Pass (21-day)', budget: '$670pp', midrange: '$670pp', luxury: '$670pp (or Green Car $890pp)' },
    { category: 'Local Transport (IC card)', budget: '$5–10/day', midrange: '$10–20/day', luxury: '$20–40/day' },
    { category: 'Activities & Museums', budget: '$10–20/day', midrange: '$20–40/day', luxury: '$40–80/day' },
    { category: '21-Day Total (couple)', budget: '$5,000–7,000', midrange: '$8,000–14,000', luxury: '$15,000–25,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Narita (NRT) or Haneda (HND) — both connect to central Tokyo by train', 'Narita Express (N\'EX) to Shinjuku: 90 mins, covered by JR Pass', 'Haneda Monorail/Keikyu line: 30 mins to central Tokyo'] },
    { title: '🚄 Getting Around', items: ['21-day JR Pass covers ALL JR trains including Shinkansen (Hikari/Sakura class)', 'Suica/PASMO IC card for metro, buses, convenience stores', 'Taxis are clean, safe, and reasonably priced for short hops', 'All major stations have elevators and accessibility features'] },
    { title: '🏨 Where to Stay', items: ['Tokyo: Shinjuku (best rail connections) or Marunouchi (near Tokyo Station)', 'Kyoto: Near Kyoto Station or Gion/Higashiyama for atmosphere', 'Osaka: Namba or Shinsaibashi for food and nightlife access', 'Consider booking ryokan (traditional inn) for one night in Kyoto or Hakone'] },
    { title: '🌡️ Weather (Mid-Oct to Early Nov)', items: ['Tokyo: 15-22°C, mild autumn days, occasional rain', 'Kyoto: 12-20°C, cooler especially mornings/evenings', 'Osaka: 14-22°C, similar to Tokyo', 'Early autumn colour begins late October — Kyoto maples peak mid-November'] },
    { title: '💳 Money & Practicalities', items: ['Cash is still important — many small restaurants are cash-only', '7-Eleven ATMs accept all international cards', 'Tipping is NOT expected (and can be confusing)', 'Tax-free shopping available at major stores (show passport, ¥5,000+ purchase)'] },
    { title: '📱 Connectivity', items: ['Rent a pocket WiFi device at the airport (recommended for 21 days)', 'Or buy an eSIM — IIJmio, Ubigi, or Airalo work well', 'Free WiFi at stations, convenience stores, and most hotels', 'Google Maps works perfectly for train navigation in Japan'] },
    { title: '♿ Accessibility Notes', items: ['Japan\'s rail system is among the world\'s most accessible', 'Elevators and escalators at virtually all major stations', 'Station staff will assist with platform gaps and luggage', 'Many temples have flat main paths (sub-trails may have stairs)', 'Taxis accommodate mobility needs — drivers assist with doors'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
