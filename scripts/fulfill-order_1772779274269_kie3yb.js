const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772779274269_kie3yb',
  email: 'paulhblasjr@gmail.com',
  destination: 'Tokyo, Osaka, Kyoto (Japan)',
  startDate: '2026-05-15',
  endDate: '2026-05-31',
  groupSize: '5+',
  requests: 'NO PORK. NO GUNDAM. 3 adults, 2 children ages 3 and 2. Matcha mornings, late-night eating/shopping. Adventurous pace even with toddlers.'
};

const itineraryData = {
  destination: 'Tokyo · Osaka · Kyoto, Japan',
  countryEmoji: '🇯🇵',
  title: 'Family Japan: Tokyo, Osaka & Kyoto with Little Ones',
  subtitle: '13 days of temples, character cafés, matcha mornings & late-night adventures for a family of five',
  description: "A meticulously planned family odyssey through Japan's three greatest cities — built for two toddlers (ages 2 and 3) and three adventurous adults who want it all. This itinerary weaves together morning matcha rituals, world-class temples, every must-visit character café and anime store, Disneyland, deer feeding in Nara, bamboo groves in Arashiyama, and Osaka's legendary street food scene — all 100% pork-free. Expect stroller-friendly routes, nap-window flexibility, late-night konbini runs, and enough Don Quijote time to fill an extra suitcase. From Shinjuku's neon canyons to Fushimi Inari's vermillion gates, this is the Japan trip your family will talk about forever.",
  duration: '13 days',
  dates: 'May 15 – May 31, 2026',
  budget: '$$$',
  pace: 'Adventurous',
  bestFor: 'Families with Toddlers · Anime & Character Fans · Foodies',

  highlights: [
    'Full day at Tokyo Disneyland — toddler rides, parades, Baby Centers & Disney magic',
    'Feed the sacred deer at Nara Park and explore Tōdai-ji\'s Great Buddha Hall',
    'Walk through thousands of vermillion torii gates at Fushimi Inari Taisha',
    'Wander the enchanting Arashiyama Bamboo Grove and meet snow monkeys at Iwatayama',
    'Kirby Café, Pokémon Center Mega, Pikachu Sweets, One Piece Store & more character heaven',
    'Matcha mornings at Kyoto\'s Rokujuan, Shinjuku Gyoen\'s SASAYAIORI+, and Harajuku\'s Chacha no Ma',
    'teamLab Planets — barefoot immersive art the whole family will love',
    'Late-night Dotonbori street food crawl — takoyaki, okonomiyaki, and chicken ramen (zero pork)',
    'Sunrise at Sensō-ji, sunset from Shibuya Sky, and Tokyo Tower after dark',
    'Gotokuji — the "lucky cat temple" where thousands of maneki-neko statues await'
  ],

  essentials: [
    { title: '🚫 Pork-Free Dining', text: 'This entire itinerary is pork-free. Every restaurant recommendation avoids pork. For ramen, we suggest chicken shio/shoyu broth (Afuri, Soranoiro, Ayam-Ya). For yakitori, order tori (chicken) or beef skewers. Okonomiyaki can be made with seafood/chicken — just say "buta nashi" (no pork). Konbini onigiri: salmon, tuna, umeboshi, and kombu are safe picks.' },
    { title: '👶 Toddler Essentials', text: 'Japan is incredibly family-friendly. Most train stations have elevators (look for signs). Strollers are welcome everywhere except some temples with stairs. Baby rooms (授乳室) with changing tables, hot water for formula, and nursing privacy are in every major mall, department store, and train station. Bring a lightweight umbrella stroller for crowded streets; use a carrier for temples with steps.' },
    { title: '🚄 Getting Around', text: 'Buy a 7-day Japan Rail Pass (covers Shinkansen Tokyo→Osaka, JR lines in Tokyo, Nara). Children under 6 ride free on all trains. Get a Suica/Pasmo IC card for subway and buses. In Osaka, a 1-day Osaka Amazing Pass covers metro + attractions. Taxis are affordable for short hops with tired toddlers — just show the driver your destination in Japanese on your phone.' },
    { title: '🍵 Matcha Mornings', text: 'Start each day with matcha at a carefully chosen café. Highlights: SASAYAIORI+ inside Shinjuku Gyoen (300-year-old Kyoto confectioner), Chacha no Ma in Harajuku (single-origin flights), Rokujuan Tea House in Kyoto (stone-ground ceremonial grade), and Atelier Matcha in Omotesando (by 160-year-old Yamamasa Koyamaen). Most open by 10am.' },
    { title: '🌙 Late-Night Guide', text: 'Don Quijote stores are open until midnight or 24hrs. Konbini (7-Eleven, FamilyMart, Lawson) are 24/7 — perfect for late-night onigiri, ice cream, and drinks. Omoide Yokocho, Kabukicho, Golden Gai, and Dotonbori stay lively until late. Many ramen shops (Ichiran, Afuri) are open past midnight.' },
    { title: '☀️ May Weather', text: 'Mid-to-late May is ideal — warm (20–26°C/68–79°F), low humidity, occasional light rain. Cherry blossom season is over but fresh green everywhere. Pack layers for cool mornings, sunscreen for park days, a compact rain jacket, and comfortable walking shoes. Bring sun hats for the toddlers.' }
  ],

  days: [
    // ===== DAY 1 — MAY 15 (FRIDAY) =====
    {
      num: 1,
      date: '2026-05-15',
      neighborhoods: 'Narita · Shinjuku',
      title: 'Landing in Tokyo — Shinjuku After Dark',
      description: "Touch down at Narita at 1pm and ride the Narita Express straight to Shinjuku. By the time you clear customs, collect bags, and reach your Airbnb, it'll be late afternoon. Settle in, then step into the electric maze of Shinjuku's west side for your first taste of Tokyo nightlife — smoky yakitori alleys, neon towers, and sensory overload in the best possible way.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Narita Express to Shinjuku',
              description: 'The Narita Express (N\'EX) is the fastest, most comfortable way to reach Shinjuku — reserved seats, luggage space, and direct service. Buy tickets at the JR ticket counter in Narita Terminal 1 or 2. The 90-minute ride gives the family time to decompress after a long flight.',
              details: [
                '🎫 ¥3,250 adult one-way (kids under 6 free). Show your Japan Rail Pass if you have one.',
                '🧳 Overhead racks and floor space for luggage and strollers',
                '⏰ Trains run every 30–60 minutes. Aim for the 2:30–3pm departure.'
              ]
            },
            {
              title: 'Check in to Shinjuku Airbnb',
              description: 'Drop your bags, set up the stroller, let the toddlers stretch out. Take a moment to walk to the nearest konbini (convenience store) for water, snacks, and diapers if needed. FamilyMart and 7-Eleven are everywhere in Shinjuku.',
              details: [
                '🏠 Most Airbnbs have washing machines — start a load of travel clothes',
                '🍙 Konbini tip: grab onigiri (rice balls) for the kids — salmon and umeboshi are pork-free winners',
                '👶 Stock up on baby supplies: diapers (merries brand), wipes, and barley tea for toddlers'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Omoide Yokochō (Memory Lane)',
              description: 'Just steps from Shinjuku Station\'s west exit, this narrow alley of tiny yakitori stalls is pure old-school Tokyo. The smoke, the lanterns, the sizzling skewers — it\'s atmospheric heaven. Order chicken yakitori (negima, tsukune, kawa) and beef skewers. Many stalls have counter seating only, so take turns with the kids or find one of the slightly larger spots.',
              details: [
                '🍢 Order "tori" (chicken) yakitori — tsukune (meatball), negima (thigh + scallion), kawa (crispy skin)',
                '🥩 Beef skewers (gyutan/tongue, harami/skirt) are also pork-free options',
                '⚠️ Skip any stall that only serves "motsu" (offal) — these are usually pork',
                '👶 Narrow alleys + smoke = go quick with toddlers. 30–45 min max.'
              ]
            },
            {
              title: 'Kabukichō & Golden Gai',
              description: 'Walk through the blazing neon gateway of Kabukichō — Tokyo\'s most famous entertainment district. The massive 3D digital billboards and Godzilla head on the Hotel Gracery are stunning at night. Then peek into Golden Gai, a labyrinth of 200+ tiny bars in ramshackle buildings. Some welcome families in the early evening — just pop your head in and ask.',
              details: [
                '🦖 Godzilla Head: Hotel Gracery rooftop, visible from the street',
                '🍶 Golden Gai: best before 9pm with kids. Some bars charge a ¥500–1000 seating fee.',
                '🏮 Kabuki Yokochō (food hall under the Gracery) has family-friendly izakaya stalls'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Kabuki Yokochō Food Hall',
              description: 'A covered food hall under Hotel Gracery with themed izakaya stalls representing different Japanese regions. Great for families — proper seating, diverse menu, and a lively atmosphere. Try the chicken nanban, seafood tempura, or beef sukiyaki. Everything is labeled and tourist-friendly.',
              meta: '💰 $$ · 📍 Kabukichō 1-chōme, Shinjuku · Open until 11pm'
            }
          ],
          tips: [
            { type: 'tip', text: 'Jet lag is real with toddlers. Don\'t force a late night — if the kids crash at 7pm, order konbini food and rest. Tomorrow is a big day.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6896, lng: 139.7006, label: 'Shinjuku Station', num: 1, cat: 'transport', desc: 'Narita Express terminal — your gateway to Shinjuku' },
        { lat: 35.6938, lng: 139.6989, label: 'Omoide Yokochō', num: 2, cat: 'food', desc: 'Atmospheric yakitori alley — chicken & beef skewers' },
        { lat: 35.6945, lng: 139.7030, label: 'Kabukichō Gate', num: 3, cat: 'attraction', desc: 'Tokyo\'s neon entertainment district' },
        { lat: 35.6940, lng: 139.7035, label: 'Golden Gai', num: 4, cat: 'nightlife', desc: 'Labyrinth of 200+ tiny bars' },
        { lat: 35.6942, lng: 139.7017, label: 'Kabuki Yokochō', num: 5, cat: 'food', desc: 'Regional izakaya food hall under Hotel Gracery' },
        { lat: 35.6944, lng: 139.7013, label: 'Hotel Gracery (Godzilla)', num: 6, cat: 'attraction', desc: 'Giant Godzilla head on the rooftop' }
      ]
    },

    // ===== DAY 2 — MAY 16 (SATURDAY) =====
    {
      num: 2,
      date: '2026-05-16',
      neighborhoods: 'Harajuku · Omotesandō · Shibuya',
      title: 'Matcha, Meiji Jingū & Shibuya Sky',
      description: "Start with matcha in Harajuku, then worship at one of Tokyo's most sacred shrines surrounded by ancient forest. Spend the afternoon bouncing between Takeshita Street's candy-colored chaos and Shibuya's iconic crossing. End the day 230 meters above the city at Shibuya Sky as the sun sets over Tokyo.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Matcha at Chacha no Ma',
              description: 'This serene Harajuku matcha café offers single-origin matcha flights — taste the difference between Uji, Yame, and Nishio regions. Beautifully presented in ceramic bowls with wagashi sweets. A calm, meditative start before the Harajuku madness begins.',
              details: [
                '🍵 Matcha flight: ¥1,500 — three single-origin matchas side by side',
                '📍 Jingūmae 5-chōme, Shibuya — 5 min walk from Meiji-jingūmae Station',
                '⏰ Opens 11am. Arrive early to avoid the lunch rush.',
                '👶 Calm atmosphere, but no high chairs. Bring a clip-on booster.'
              ]
            },
            {
              title: 'Meiji Jingū Shrine',
              description: 'Walk under the massive torii gate and into a 175-acre forest in the middle of Tokyo. This shrine, dedicated to Emperor Meiji, is one of Japan\'s holiest. The gravel paths are stroller-friendly (use wide tires or carry the kids). Write wishes on an ema wooden plaque and watch for traditional Shinto wedding processions.',
              details: [
                '⛩️ Free entry. Open sunrise to sunset (~5am–6:30pm in May).',
                '🌳 The forest has 100,000 trees donated from across Japan — it feels like another world.',
                '🍼 No baby room on-site, but there\'s one at the nearby Harajuku Station JR building.',
                '📸 The main torii gate (12m tall) is the classic photo op.'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Eggs \'n Things Harajuku',
              description: 'Hawaiian-style pancake house beloved by Japanese families. Towering whipped cream pancakes, omelettes, and fruit bowls. High chairs available, kid-friendly menu, and a fun vibe. No pork on the menu if you skip the bacon — order the loco moco with beef or the fruit pancakes.',
              meta: '💰 $$ · 📍 Jingūmae 4-30-2, Shibuya · Opens 8am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Takeshita Street & Harajuku Shopping',
              description: 'The most colorful street in Tokyo — packed with crepe shops, kawaii fashion, candy stores, and character goods. It\'s overwhelming, exciting, and the toddlers will love the cotton candy, giant rainbow crepes, and toy capsule machines (gachapon). Hit the One Piece Mugiwara Store and Brandy Melville while you\'re here.',
              details: [
                '🍦 Marion Crepes: get the strawberry banana with whipped cream — the OG Harajuku snack',
                '🏴‍☠️ One Piece Mugiwara Store: Jingūmae 1-6-8 (official merch from keychains to figures)',
                '👗 Brandy Melville: Jingūmae 1-8-2 (one-size trendy basics)',
                '🎰 Gachapon machines: ¥100–500 per capsule — the toddlers will be OBSESSED',
                '⚠️ Stroller tip: Takeshita is very crowded on weekends. Use a carrier here and stroller in the parks.'
              ]
            },
            {
              title: 'Yoyogi Park',
              description: 'A massive green oasis right next to Harajuku — perfect for the toddlers to run free after the stimulation of Takeshita. In May, the park is lush and green with open lawns. Bring a blanket, grab konbini snacks, and let the kids burn energy. You might catch street performers or a weekend festival.',
              details: [
                '🌿 Free entry, open 24/7 (gated areas close at dusk)',
                '👶 Wide paved paths = stroller heaven',
                '🎪 Weekend events are common — look for food festivals and craft markets',
                '🚻 Clean public restrooms with baby-changing facilities'
              ]
            },
            {
              title: 'Café Reissue (Latte Art)',
              description: 'Adorable Harajuku café famous for latte art — they\'ll draw any character on your drink. The toddlers will go wild watching the barista create Pikachu, Hello Kitty, or even their own faces on the foam. Small space but very Instagram-worthy.',
              details: [
                '☕ Character latte art: ¥800–1,200. Show them a photo of what you want.',
                '📍 Jingūmae 3-25-7, 3rd floor',
                '📸 Perfect Instagram moment — order one for each kid'
              ]
            }
          ]
        },
        {
          label: 'Late Afternoon',
          activities: [
            {
              title: 'Shibuya Crossing & Hachikō',
              description: 'Walk from Harajuku south to Shibuya (15 min) and witness the world\'s most famous intersection. Stand on the Shibuya Station pedestrian bridge or the Starbucks Reserve above to watch up to 3,000 people cross at once. Pet the Hachikō statue — the loyal dog who waited 9 years for his owner.',
              details: [
                '📸 Best viewing: Shibuya Station 2F pedestrian deck (free) or Mag\'s Park rooftop',
                '🐕 Hachikō statue: outside Shibuya Station\'s Hachikō Exit',
                '🛍️ Shibuya 109 and Center-gai shopping street are right here'
              ]
            },
            {
              title: 'Pokémon Center Shibuya',
              description: 'Inside Shibuya PARCO (6F), this Pokémon Center is themed around Mewtwo with a neon cityscape aesthetic. Exclusive Shibuya-only merchandise, plushies, trading cards, and clothing. The toddlers will love the giant Pikachu displays.',
              details: [
                '🎮 Shibuya PARCO 6F — take the elevator for stroller access',
                '🛍️ Shibuya-exclusive merch (t-shirts, pins, plushies with Shibuya design)',
                '⏰ 10am–9pm daily'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Afuri Ramen (Harajuku or Shibuya)',
              description: 'Light, refreshing yuzu shio (citrus salt) chicken roth ramen — the polar opposite of heavy tonkotsu. Made with chicken and dashi broth, no pork whatsoever. The yuzu aroma is incredible. Kid portions available, and the clean flavors are toddler-approved.',
              meta: '💰 $ · 📍 Multiple locations in Harajuku & Shibuya · No reservations needed'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shibuya Sky (Sunset)',
              description: 'The rooftop observation deck of Shibuya Scramble Square — 230 meters above the crossing. An open-air sky stage with 360° views of Tokyo at sunset. On clear May evenings, you can see Mt. Fuji glowing orange. Book tickets online in advance for the sunset time slot.',
              details: [
                '🎫 ¥2,000 adults, free for children under 3 (age 4–5: ¥600). Book at shibuya-sky.com.',
                '🌅 Sunset in May: ~6:30pm. Arrive 30 min before for the best light.',
                '📸 The glass floor area and neon lighting at night are incredible',
                '👶 Strollers must be folded — baby carriers recommended for the observation deck'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'After Shibuya Sky, walk 2 blocks to Don Quijote Shibuya for late-night shopping. Open until midnight, packed with souvenirs, snacks, and weird wonderful Japanese goods.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6691, lng: 139.6994, label: 'Chacha no Ma', num: 1, cat: 'food', desc: 'Single-origin matcha flights in serene Harajuku' },
        { lat: 35.6764, lng: 139.6993, label: 'Meiji Jingū Shrine', num: 2, cat: 'attraction', desc: 'Sacred Shinto shrine in a 175-acre forest' },
        { lat: 35.6702, lng: 139.7026, label: 'Takeshita Street', num: 3, cat: 'shopping', desc: 'Harajuku\'s colorful kawaii shopping street' },
        { lat: 35.6715, lng: 139.6951, label: 'Yoyogi Park', num: 4, cat: 'attraction', desc: 'Sprawling green park — perfect for toddler playtime' },
        { lat: 35.6613, lng: 139.7006, label: 'Shibuya Crossing', num: 5, cat: 'attraction', desc: 'World\'s most famous pedestrian scramble' },
        { lat: 35.6620, lng: 139.6988, label: 'Pokémon Center Shibuya', num: 6, cat: 'shopping', desc: 'Mewtwo-themed Pokémon store in PARCO' },
        { lat: 35.6580, lng: 139.7016, label: 'Shibuya Sky', num: 7, cat: 'attraction', desc: '230m open-air observation deck with sunset views' },
        { lat: 35.6605, lng: 139.6985, label: 'Afuri Ramen', num: 8, cat: 'food', desc: 'Yuzu chicken broth ramen — 100% pork-free' }
      ]
    },

    // ===== DAY 3 — MAY 17 (SUNDAY) =====
    {
      num: 3,
      date: '2026-05-17',
      neighborhoods: 'Tsukiji · Ginza · Asakusa · Sumida',
      title: 'Tsukiji Market, Sensō-ji & Tokyo Skytree',
      description: "An east-side Tokyo day hitting three iconic destinations connected by subway. Start with the freshest sushi and ichigo daifuku (strawberry mochi) at Tsukiji, dive into Ginza's Art Aquarium, then explore ancient Asakusa and its thundering Sensō-ji temple. End with panoramic views from 450 meters up at Tokyo Skytree.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tsukiji Outer Market',
              description: 'The legendary fish market\'s outer market is a sensory feast — rows of stalls selling the freshest sushi, tamago (egg omelette on a stick), grilled seafood, and seasonal fruits. This is where you find the famous ichigo daifuku (strawberry wrapped in mochi and red bean). Go hungry. Go early.',
              details: [
                '🍓 Ichigo Daifuku: try Tsukiji Sano (佐野) — pillowy mochi with a whole strawberry inside',
                '🍣 Stand-up sushi counters serve omakase from ¥2,000. Kids can eat tamago (sweet egg) nigiri.',
                '🦐 Try: grilled scallop on a stick, uni (sea urchin) on rice, melon pan from the bakeries',
                '⏰ Best time: 7–10am. Some stalls close by noon. Sundays can be busy.',
                '👶 Narrow lanes — stroller is ok but a carrier is easier for peak hours'
              ]
            },
            {
              title: 'Art Aquarium Museum',
              description: 'A mesmerizing fusion of art and aquarium — goldfish swim in illuminated glass sculptures that shift colors and patterns. It\'s dark, cool, and dreamlike — toddlers will be transfixed by the glowing fish. Located in the Ginza area, a short walk from Tsukiji.',
              details: [
                '🐟 Location: Ginza Mitsui Building (moved from original Nihonbashi location)',
                '🎫 ¥2,400 adults, ¥1,000 children 4+ (under 4 free)',
                '📸 The giant goldfish bowls are otherworldly — excellent photo ops',
                '👶 Dark + calm = potential nap opportunity for toddlers. Win-win.'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Tsukiji Market Stalls',
              description: 'Graze your way through the market — tamago on a stick, fresh sushi, grilled shrimp skewers, and melon bread. This is a "eating is the activity" morning. Everything is pork-free by default since it\'s a fish market.',
              meta: '💰 $–$$ · 📍 Tsukiji 4-chōme, Chūō · Open from 5am, best before 10am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Sensō-ji Temple & Nakamise-dōri',
              description: 'Tokyo\'s oldest and most visited temple — the massive red Kaminarimon (Thunder Gate) with its giant lantern is an instant classic. Walk through Nakamise-dōri, a 200-meter shopping street selling traditional snacks, chopsticks, and souvenirs. The temple complex itself is vast, colorful, and stroller-friendly on the main paths.',
              details: [
                '⛩️ Free entry, open 24/7 (main hall: 6am–5pm in May)',
                '🏮 Kaminarimon lantern weighs 700kg — the toddlers will stare up in awe',
                '🍘 Nakamise snacks: senbei (rice crackers), ningyo-yaki (red bean filled cakes), melon pan',
                '📸 Evening illumination is magical if you come back after dark',
                '👶 Stroller-friendly on main paths. Steps at the main hall — park stroller at the base.'
              ]
            },
            {
              title: 'Samurai Ninja Museum',
              description: 'Interactive museum in Asakusa where you can handle real katanas (supervised), try on samurai armor, watch ninja shows, and practice throwing stars. The toddlers might be too young for the full experience, but the armor photo ops and ninja show are visually exciting for all ages.',
              details: [
                '🗡️ ¥3,000 adults, children under 3 free. Guided tours every 30 min.',
                '📍 Nishi-Asakusa 1-8-13 — 10 min walk from Sensō-ji',
                '📸 The samurai armor photo booth is an unforgettable family photo',
                '⏰ Allow 60–90 min. Book online for English tour.'
              ]
            }
          ]
        },
        {
          label: 'Late Afternoon',
          activities: [
            {
              title: 'Ōyokogawa Shinsui Park',
              description: 'A hidden gem — a long, narrow waterway park in Sumida perfect for toddlers. Shallow wading areas, small waterfalls, bridges, and shaded walking paths. In May the greenery is lush. A perfect palate cleanser between temples and observation decks.',
              details: [
                '💧 Shallow water play areas — bring a change of clothes for the kids',
                '📍 Near Kinshichō Station, between Asakusa and Skytree',
                '🌿 Free, open anytime. Beautiful cherry tree-lined paths.'
              ]
            },
            {
              title: 'Tokyo Skytree',
              description: 'At 634 meters, Tokyo Skytree is the tallest tower in the world. The Tembo Deck (350m) and Tembo Gallery (450m) offer mind-bending views of the Tokyo sprawl. On a clear May evening, you can see Mt. Fuji. The base (Tokyo Solamachi) is a massive shopping mall with character stores and restaurants.',
              details: [
                '🗼 Tembo Deck: ¥2,100 adults, free for under-4 (4–5: ¥1,000). Tembo Gallery: +¥1,000.',
                '🛍️ Solamachi Mall: Pokémon Center Skytree, Studio Ghibli shop, Kirby pop-ups',
                '📸 The glass floor panels at 340m are thrilling — toddlers pressed against the glass = adorable',
                '⏰ Open 10am–9pm. Less crowded on weekday evenings.'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Asakusa Gyūkatsu Ichi-Ni-San',
              description: 'Deep-fried beef cutlet (gyūkatsu) — a pork-free alternative to tonkatsu that\'s crispy on the outside, rare and juicy inside. You grill your slices on a hot stone at your table. Kids love the interactive element. 100% beef, zero pork.',
              meta: '💰 $$ · 📍 Asakusa 2-17-10 · Expect a 20–30 min wait (worth it)'
            }
          ],
          tips: [
            { type: 'tip', text: 'If the toddlers are fading, skip the Skytree interior and just enjoy the illuminated tower from the base. Tokyo Solamachi mall stays open until 9pm with plenty of food options.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6654, lng: 139.7707, label: 'Tsukiji Outer Market', num: 1, cat: 'food', desc: 'Iconic fish market — sushi, ichigo daifuku, seafood stalls' },
        { lat: 35.6674, lng: 139.7687, label: 'Art Aquarium Museum', num: 2, cat: 'attraction', desc: 'Illuminated goldfish art installation' },
        { lat: 35.7148, lng: 139.7967, label: 'Sensō-ji Temple', num: 3, cat: 'attraction', desc: 'Tokyo\'s oldest temple with iconic Thunder Gate' },
        { lat: 35.7120, lng: 139.7940, label: 'Samurai Ninja Museum', num: 4, cat: 'attraction', desc: 'Interactive samurai armor and ninja experience' },
        { lat: 35.6905, lng: 139.8145, label: 'Ōyokogawa Shinsui Park', num: 5, cat: 'attraction', desc: 'Waterway park with toddler wading areas' },
        { lat: 35.7101, lng: 139.8107, label: 'Tokyo Skytree', num: 6, cat: 'attraction', desc: '634m tower — world\'s tallest, with panoramic views' },
        { lat: 35.7126, lng: 139.7978, label: 'Gyūkatsu Ichi-Ni-San', num: 7, cat: 'food', desc: 'Deep-fried beef cutlet — pork-free tonkatsu alternative' }
      ]
    },

    // ===== DAY 4 — MAY 18 (MONDAY) =====
    {
      num: 4,
      date: '2026-05-18',
      neighborhoods: 'Shinjuku · Ikebukuro',
      title: 'Shinjuku Garden, Character Cafés & Ikebukuro',
      description: "A morning of zen in Shinjuku Gyoen's gardens with matcha from a 300-year-old Kyoto confectioner, followed by an afternoon in Ikebukuro — the mecca of character cafés, anime stores, and Sunshine City. End the evening at Toyosu Manyo Club, a luxurious onsen with Tokyo Bay views.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinjuku Gyoen National Garden',
              description: 'One of Tokyo\'s most beautiful parks — 144 acres of Japanese gardens, English landscapes, and French formal gardens. In May, the roses and irises are in full bloom. The wide paved paths are perfect for strollers, and the expansive lawns let the toddlers run. Inside the park, visit the SASAYAIORI+ matcha café.',
              details: [
                '🌿 ¥500 adults, free for children under 15',
                '⏰ 9am–5:30pm (last entry 5pm). Closed Mondays — today is Monday!',
                '⚠️ CLOSED MONDAYS — move this to an alternative plan or swap days',
                '🍵 SASAYAIORI+ inside the park: 300-year-old Kyoto confectioner, matcha + wagashi set ¥1,200'
              ]
            },
            {
              title: 'Shinjuku 3D Cat Billboard',
              description: 'Just outside Shinjuku Station\'s east exit, the massive curved LED screen displays a hyper-realistic 3D cat that appears to pop out of the building. It\'s a quick 5-minute stop but the toddlers will be delighted. The cat "wakes up" at the top of each hour.',
              details: [
                '🐱 Cross Shinjuku Vision building, above Shinjuku Station east exit',
                '📸 Best viewed from across the street. Plays hourly animations.',
                '⏰ The cat appears frequently throughout the day — just stand and wait a minute'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Sarabeth\'s Shinjuku',
              description: 'NYC-famous brunch spot with a beautiful Shinjuku location. Fluffy eggs Benedict (with salmon or avocado — no pork), lemon ricotta pancakes, and fresh-squeezed juice. High chairs available, spacious seating, very family-friendly.',
              meta: '💰 $$ · 📍 Shinjuku Lumine 2, 2F · Opens 9am'
            }
          ],
          tips: [
            { type: 'tip', text: 'Shinjuku Gyoen is CLOSED on Mondays (May 18 is Monday). Alternative: visit the TMG North Observatory (free, opens 9:30am) for panoramic views of Tokyo instead, and save Shinjuku Gyoen for Day 11 or 12 (your return Tokyo days).' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Sunshine City (Ikebukuro)',
              description: 'A massive entertainment complex in Ikebukuro that\'s basically a full day of character heaven. Under one roof: Pokémon Center Mega Tokyo (the biggest in Japan), Pikachu Sweets café, Ghibli Store (official merch), Naruto store, and the Sunshine Aquarium on the rooftop. This is THE destination for anime-loving families.',
              details: [
                '🎮 Pokémon Center Mega: Japan\'s largest — exclusive plushies, clothing, and trading cards',
                '🍰 Pikachu Sweets: adorable Pikachu-shaped desserts and drinks',
                '🌿 Ghibli Store (donguri kyowakoku): Totoro, Kiki, Spirited Away merch',
                '🍥 Jump Shop: Naruto, One Piece, JJK merch all in one place',
                '🐠 Sunshine Aquarium: rooftop aquarium with penguin sky garden (¥2,600 adult)',
                '👶 Elevators throughout, baby rooms on multiple floors, very stroller-friendly'
              ]
            },
            {
              title: 'Kirby Café Tokyo',
              description: 'The permanent Kirby Café inside Tokyo Solamachi at Skytree — wait, actually it\'s in the same Sunshine City complex! Adorable Kirby-themed food: waddle dee burger steaks, Kirby curry, and dream land desserts. Every dish is a work of art. RESERVATIONS ARE REQUIRED — book online 1 month before your trip.',
              details: [
                '🎀 Location: Sunshine City Alpa B1F, Ikebukuro',
                '🎫 RESERVATION REQUIRED — book at kirbycafe.jp exactly 1 month before (opens at noon JST)',
                '💰 ¥1,500–3,000 per person plus mandatory souvenir item purchase (¥700+)',
                '👶 High chairs available, kid-friendly portions. The Kirby-shaped food delights all ages.',
                '⏰ Time slots are 80 minutes. Book the earliest available.'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Toyosu Manyo Club (Onsen)',
              description: 'A luxurious hot spring resort on the 24th–25th floor of a Toyosu skyscraper with views of Tokyo Bay, Rainbow Bridge, and the city skyline. Multiple baths, saunas, relaxation rooms, and a restaurant. Kids are welcome (unusual for Japanese onsen). A perfect way to soak away the day\'s adventures.',
              details: [
                '♨️ ¥3,850 adults, ¥1,980 children (3+). Under 3: ¥1,100. Includes yukata rental.',
                '📍 Urban Dock LaLaport Toyosu — take the Yurakucho Line from Ikebukuro',
                '🌃 The nighttime city view from the outdoor bath is spectacular',
                '👶 Diapered children can use specific family baths. Call ahead to confirm.',
                '⏰ Open 24hrs. Best to arrive by 7pm for a relaxed soak before bedtime.'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Toyosu Manyo Club Restaurant',
              description: 'Eat in your yukata at the onsen\'s in-house restaurant. Sashimi platters, chicken karaage, tempura udon, and soba — all pork-free. Relaxing atmosphere after your bath.',
              meta: '💰 $$ · 📍 Inside Toyosu Manyo Club · No reservation needed'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6852, lng: 139.7100, label: 'Shinjuku Gyoen', num: 1, cat: 'attraction', desc: '144-acre national garden (closed Mondays — backup plan in tips)' },
        { lat: 35.6938, lng: 139.7030, label: '3D Cat Billboard', num: 2, cat: 'attraction', desc: 'Hyper-realistic 3D cat on curved LED screen' },
        { lat: 35.7293, lng: 139.7194, label: 'Sunshine City', num: 3, cat: 'shopping', desc: 'Pokémon Mega, Ghibli Store, Pikachu Sweets, Naruto & more' },
        { lat: 35.7290, lng: 139.7190, label: 'Kirby Café Tokyo', num: 4, cat: 'food', desc: 'Adorable Kirby-themed café (reservation required!)' },
        { lat: 35.6490, lng: 139.7920, label: 'Toyosu Manyo Club', num: 5, cat: 'attraction', desc: 'Skyline onsen with Tokyo Bay views — family-friendly' },
        { lat: 35.6905, lng: 139.7003, label: 'TMG North Observatory', num: 6, cat: 'attraction', desc: 'Free 202m observation deck — backup if Gyoen is closed' }
      ]
    },

    // ===== DAY 5 — MAY 19 (TUESDAY) =====
    {
      num: 5,
      date: '2026-05-19',
      neighborhoods: 'Maihama · Urayasu',
      title: 'Tokyo Disneyland — The Full Magic Day',
      description: "Your last full Tokyo day before heading to Osaka — and it's going to be pure Disney magic. Tokyo Disneyland is consistently rated the most magical Disney park in the world, and with two toddlers, you'll find an incredible number of rides with no height restriction. Plan around the parade times, use the stroller parking areas, and lean into the Baby Centers for diaper changes and feeding breaks.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Park Opening & Fantasyland',
              description: 'Arrive at Maihama Station by 8am (park opens 8:30 or 9am). Head straight to Fantasyland — the heart of toddler Disney. "It\'s a Small World," Dumbo the Flying Elephant, Castle Carrousel, Pooh\'s Hunny Hunt (use Standby Pass), and the Alice in Wonderland teacups are all no-height-restriction rides perfect for ages 2–3.',
              details: [
                '🎫 1-Day Passport: ¥9,400 adult, ¥5,600 child (4–11). Under 4: FREE!',
                '🚂 Take JR Keiyō Line from Shinjuku → Tokyo Station → Maihama (45 min total)',
                '🎠 Must-do toddler rides: Pooh\'s Hunny Hunt, Dumbo, Small World, Haunted Mansion, Jungle Cruise',
                '📱 Download Tokyo Disney Resort app for wait times and Standby Passes',
                '👶 Baby Center in World Bazaar: diapers, formula, nursing rooms, microwave'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Great American Waffle Co. (World Bazaar)',
              description: 'Mickey-shaped waffles with fruit and whipped cream — the toddlers will lose their minds. No pork on this menu. Grab coffee for the adults and fuel up before the rides.',
              meta: '💰 $$ · 📍 World Bazaar, Tokyo Disneyland · Opens with the park'
            }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Toontown & Parade',
              description: 'Toontown is designed for little kids — Goofy\'s Paint \'n Play House, Chip \'n\' Dale\'s Treehouse, Donald\'s Boat, and Minnie\'s house. The area is colorful, interactive, and safe for wandering toddlers. Claim a parade viewing spot 30 minutes early along the route — the Dreaming Up parade is spectacular.',
              details: [
                '🏡 Toontown Baby Center: full nursing room, bottle warming, diaper station',
                '🎪 Dreaming Up Parade: ~2pm daily. Find a spot near Toontown for less crowds.',
                '📸 Character meet & greets throughout — Toontown is the best spot for Mickey & friends',
                '💤 Nap strategy: bring a blanket, claim a shady parade spot, and let toddlers snooze in the stroller while waiting'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Queen of Hearts Banquet Hall',
              description: 'A whimsical Alice in Wonderland-themed restaurant with set meals — roast chicken, seafood doria, and hamburg steak (beef). The interiors are magical with oversized playing cards and chandeliers. High chairs available.',
              meta: '💰 $$ · 📍 Fantasyland · No reservation (counter service), ~30 min wait'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Adventureland & Westernland',
              description: 'Jungle Cruise (bilingual boat ride), Western River Railroad (train ride), Pirates of the Caribbean (dark ride — may be too intense for the 2yo), and Tom Sawyer Island (playground island). These areas have great theming and lots of shaded walking paths.',
              details: [
                '🏴‍☠️ Pirates: dark with loud cannons — assess your kids\' tolerance for noise/dark',
                '🚂 Western River Railroad: gentle train ride, great for tired toddlers',
                '🏝️ Tom Sawyer Island: raft ride + playground. Open until 30 min before park close.',
                '🍦 Grab soft serve from the cart near Adventureland entrance'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Tomorrowland, Shopping & Fireworks',
              description: 'End the day in Tomorrowland — Buzz Lightyear (shooting ride, all ages), Monsters Inc. Ride & Go Seek (flashlight ride, toddler-favorite), and Star Tours (may be too intense for under-3). After rides, shop at the World Bazaar for Disney exclusive merch. If the toddlers can hang on, the nighttime fireworks are unforgettable.',
              details: [
                '🔫 Buzz Lightyear: interactive shooting ride — zero height requirement, huge toddler hit',
                '👹 Monsters Inc: flashlight scavenger hunt ride — gentle and fun',
                '🎆 Fireworks: ~8:30pm (schedule varies). Best viewed from the hub in front of the castle.',
                '🛍️ World Bazaar shops stay open 30 min after park close',
                '🚂 Last train from Maihama to Shinjuku: ~11:30pm. Leave by 9:30 to be safe with tired kids.'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Grandma Sara\'s Kitchen (Critter Country)',
              description: 'Cozy log-cabin restaurant serving chicken, rice, and comfort food. No pork options clearly marked. Great for refueling before the evening push. High chairs and a calm atmosphere.',
              meta: '💰 $$ · 📍 Critter Country, Tokyo Disneyland'
            }
          ],
          tips: [
            { type: 'tip', text: 'Disney pro tip: download the TDR app and check wait times obsessively. With toddlers, skip anything over 30 min wait. Use the "Rider Switch" system — one adult waits with kids while others ride, then swap without re-queuing.' },
            { type: 'tip', text: 'Pack snacks from the konbini — Disney food is expensive and the lines are long. The toddlers will need constant fuel.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6329, lng: 139.8804, label: 'Tokyo Disneyland', num: 1, cat: 'attraction', desc: 'Full day of Disney magic — toddler-friendly rides & parades' },
        { lat: 35.6320, lng: 139.8810, label: 'Fantasyland', num: 2, cat: 'attraction', desc: 'Pooh\'s Hunny Hunt, Dumbo, Small World — toddler paradise' },
        { lat: 35.6338, lng: 139.8795, label: 'Toontown', num: 3, cat: 'attraction', desc: 'Interactive play area with Baby Center' },
        { lat: 35.6310, lng: 139.8780, label: 'Adventureland', num: 4, cat: 'attraction', desc: 'Jungle Cruise and Pirates of the Caribbean' },
        { lat: 35.6335, lng: 139.8830, label: 'World Bazaar', num: 5, cat: 'shopping', desc: 'Disney shopping + Baby Center' },
        { lat: 35.6345, lng: 139.8812, label: 'Maihama Station', num: 6, cat: 'transport', desc: 'JR Keiyō Line — 45 min from Shinjuku' }
      ]
    },

    // ===== DAY 6 — MAY 20 (WEDNESDAY) =====
    {
      num: 6,
      date: '2026-05-20',
      neighborhoods: 'Shinkansen · Nara · Osaka',
      title: 'Bullet Train to Osaka & Nara Deer Park',
      description: "Say goodbye to Tokyo (for now) and rocket to Osaka on the Shinkansen — a thrilling experience in itself. Drop your bags at the Osaka hotel, then take a quick train to Nara to meet the famous sacred deer, visit the colossal Great Buddha, and explore the charming town. Return to Osaka for your first taste of the Kansai food capital.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinkansen: Tokyo → Shin-Osaka',
              description: 'The Tōkaidō Shinkansen is one of the great travel experiences in the world. The Nozomi train covers Tokyo to Shin-Osaka in 2 hours 27 minutes at 285 km/h. Book reserved seats (Car 12–16 for the most space) and enjoy the view of Mt. Fuji from the right side (seats E/D). Kids under 6 ride free on laps or in free seats.',
              details: [
                '🚄 Nozomi: ¥14,720 one-way (not covered by regular JR Pass — need "All Japan" pass or buy tickets)',
                '🗻 Mt. Fuji view: right side (seats D/E), ~40 min after departure, near Shin-Fuji Station',
                '🍱 Buy ekiben (station bento) at Tokyo Station before boarding — look for chicken or seafood ones',
                '👶 Green Car (first class) has more legroom but isn\'t necessary. Standard reserved is fine.',
                '🎒 Large luggage: reserve oversized luggage space (last row) when booking'
              ]
            },
            {
              title: 'Check in to Osaka Accommodation',
              description: 'Drop bags at your Osaka hotel or Airbnb. Namba or Shinsaibashi area is ideal — central to Dotonbori, easy subway access to Nara and Kyoto. Take 30 minutes to settle in before heading to Nara.',
              details: [
                '🏨 Shin-Osaka Station → Namba: Midōsuji Line, 15 min, ¥280',
                '🧳 If check-in isn\'t ready, use coin lockers at Namba Station (¥400–700)'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nara Park & Sacred Deer',
              description: 'Just 45 minutes from Osaka by train, Nara is home to over 1,200 sacred deer that roam freely. Buy shika senbei (deer crackers, ¥200) and the deer will bow to you before eating from your hand. The toddlers will be in absolute heaven — but keep a close eye, as the deer can be pushy when they smell crackers.',
              details: [
                '🦌 Deer crackers (shika senbei): ¥200 from vendors throughout the park',
                '⚠️ Deer safety: Don\'t let toddlers hold crackers — deer will crowd them. Adults hold crackers, kids pet the deer.',
                '👶 The deer are generally gentle but can nip at clothing/bags. Keep snack bags closed.',
                '🚂 Kintetsu Namba → Kintetsu Nara: 40 min express, ¥680. JR also runs from Namba.'
              ]
            },
            {
              title: 'Tōdai-ji Temple (Great Buddha Hall)',
              description: 'Home to Japan\'s largest bronze Buddha statue (15 meters tall) inside the world\'s largest wooden building. Walking through the giant Nandaimon gate with its fierce guardian statues is awe-inspiring. Inside, try squeezing through the "Buddha\'s nostril" pillar hole — said to grant enlightenment (adults might not fit, but toddlers will slide through!).',
              details: [
                '🙏 ¥600 adults, ¥300 children (6–12), under 6 free',
                '🕳️ The pillar hole is the same size as the Buddha\'s nostril — a fun challenge for the whole family',
                '📸 The Great Buddha is genuinely jaw-dropping even for little kids'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Maguro Koya (Nara)',
              description: 'Fresh tuna rice bowl restaurant near Nara Park. All-tuna menu — negitoro (minced tuna), tekka-don (tuna sashimi bowl), and grilled tuna steak. 100% pork-free. Family-friendly with counter and table seating.',
              meta: '💰 $$ · 📍 Higashimuki Shopping Street, Nara · 5 min walk from Kintetsu Nara Station'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'First Walk Through Dōtonbori',
              description: 'Return to Osaka and take an evening stroll along the Dōtonbori canal — the most famous food street in Japan. The neon signs, giant crab robots, and Glico Running Man sign are a feast for the eyes. Tonight is just a preview — you\'ll do a deeper food crawl on Day 8.',
              details: [
                '🦀 Look for the giant mechanical crab (Kani Dōraku) and the Glico Running Man sign',
                '🍢 Grab kushi-katsu (deep-fried skewers — order chicken/shrimp/veggie) from a street stall',
                '📸 The canal reflections at night are perfect for photos',
                '🌙 Dōtonbori stays lively until midnight — but with toddlers, a 9pm stroll is perfect'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Chibo Dotonbori (Okonomiyaki)',
              description: 'A legendary okonomiyaki restaurant with a dedicated Muslim-friendly/pork-free branch on the 7th floor. They use halal-certified meat and no pork or alcohol in cooking. The signature Chibo-yaki is cooked right on your table\'s teppan griddle. Spectacular and interactive — the toddlers will stare at the sizzling pancake.',
              meta: '💰 $$ · 📍 Dōtonbori 1-5-5, 7F (Muslim-friendly branch) · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.7336, lng: 135.5001, label: 'Shin-Osaka Station', num: 1, cat: 'transport', desc: 'Shinkansen arrival — 2h27m from Tokyo' },
        { lat: 34.6851, lng: 135.7728, label: 'Nara Park', num: 2, cat: 'attraction', desc: '1,200+ sacred deer roaming free — feed and pet them' },
        { lat: 34.6891, lng: 135.7398, label: 'Tōdai-ji', num: 3, cat: 'attraction', desc: 'World\'s largest wooden building with 15m bronze Buddha' },
        { lat: 34.6834, lng: 135.7682, label: 'Maguro Koya', num: 4, cat: 'food', desc: 'Fresh tuna bowls near Nara Park' },
        { lat: 34.6687, lng: 135.5013, label: 'Dōtonbori', num: 5, cat: 'food', desc: 'Osaka\'s legendary neon-lit food street' },
        { lat: 34.6690, lng: 135.5020, label: 'Chibo Okonomiyaki', num: 6, cat: 'food', desc: 'Pork-free okonomiyaki on a teppan griddle' }
      ]
    },

    // ===== DAY 7 — MAY 21 (THURSDAY) =====
    {
      num: 7,
      date: '2026-05-21',
      neighborhoods: 'Fushimi · Arashiyama · Gion · Nishiki',
      title: 'Kyoto Day — Torii Gates, Bamboo & Geisha Streets',
      description: "A full day in Kyoto — Japan's ancient capital and spiritual heart. Start at the famous vermillion torii gates of Fushimi Inari, sip ceremonial matcha at a historic tea house, wander through the otherworldly Arashiyama Bamboo Grove, and explore Gion's geisha district as lanterns flicker on at dusk. This is the Japan of your imagination.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Fushimi Inari Taisha',
              description: 'The iconic shrine with thousands of vermillion torii gates winding up Mount Inari. You don\'t need to hike to the summit (2 hours) — the first section through the Senbon Torii (thousand gates) takes just 15 minutes and is the most photogenic. Go early to beat crowds. The gates are mesmerizing for toddlers — they love running through the "orange tunnel."',
              details: [
                '⛩️ Free entry, open 24/7. Best time: 7–9am for photos without crowds.',
                '🚂 From Osaka: JR Nara Line to Inari Station (40 min), shrine is right at the station exit.',
                '👶 Stroller works for the first section. Stone steps begin after the first intersection.',
                '📸 The double row of torii (Senbon Torii) is THE Instagram shot. Go early!'
              ]
            },
            {
              title: 'Rokujūan Tea House (Matcha)',
              description: 'A traditional Kyoto tea house near Fushimi Inari serving stone-ground ceremonial matcha with seasonal wagashi. This is matcha the way it\'s been drunk for centuries — whisked by hand in a quiet tatami room. One of the customer\'s must-visit spots.',
              details: [
                '🍵 Matcha set with wagashi: ¥1,000–1,500',
                '📍 Near Fushimi Inari — check Google Maps for current location (some branches)',
                '👶 Tatami seating — shoes off. Toddlers can sit on the floor mats.',
                '⏰ Opens around 10am'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arashiyama Bamboo Grove',
              description: 'The towering bamboo stalks create a natural cathedral of swaying green — the sound of wind through bamboo is unlike anything else. The main path is paved and stroller-friendly. Combine with Tenryū-ji Temple\'s beautiful garden (¥500) just steps away.',
              details: [
                '🎋 Free entry to the bamboo path. Best time: before 10am or late afternoon.',
                '🚂 From Fushimi: JR Nara Line to Kyoto, then JR Sagano Line to Saga-Arashiyama (~1hr total).',
                '📸 The path is short (500m) — walk slowly, soak it in.',
                '👶 Fully stroller-accessible on the main path'
              ]
            },
            {
              title: 'Miffy Kitchen Bakery (Arashiyama)',
              description: 'An adorable Miffy-themed bakery in the Arashiyama shopping street. Miffy-shaped breads, pastries, and drinks. Everything is cute and the toddlers will love pointing at the Miffy faces on every pastry. A sweet afternoon snack stop.',
              details: [
                '🐰 Miffy-shaped melon pan, Miffy cream puffs, and Miffy hot chocolate',
                '📍 Arashiyama main shopping street, near the bamboo grove entrance',
                '💰 ¥300–800 per item. Takeaway-style — eat while you walk.'
              ]
            },
            {
              title: 'Iwatayama Monkey Park',
              description: 'A 20-minute uphill hike brings you to a mountainside park where 120+ Japanese macaques roam free. At the top, YOU\'RE inside the cage-like feeding area while the monkeys play outside. Stunning views of Kyoto from the summit. Important: the hike is steep with no stroller access — use carriers for the toddlers or split the group.',
              details: [
                '🐒 ¥550 adults, ¥250 children (4–15), under 4 free',
                '⏰ Open 9am–4:30pm (last entry 4pm)',
                '⛰️ 20-minute uphill climb — NO strollers. Baby carrier essential.',
                '👶 Consider splitting: 1 adult stays at the base with one toddler, 2 adults take the other toddler up',
                '📸 Baby monkeys in May are adorable — they cling to their mothers\' backs'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Arashiyama Yoshimura (Soba)',
              description: 'Handmade soba noodles with a view of the Togetsu-kyō Bridge and the Hozu River. Tempura soba with shrimp and vegetable tempura is the move — all pork-free. The cold zaru soba is refreshing on warm days. Window seats are worth the wait.',
              meta: '💰 $$ · 📍 Arashiyama, right by Togetsu-kyō Bridge · Expect 20–30 min wait for window seat'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Nishiki Market',
              description: 'Kyoto\'s "kitchen" — a 400-year-old covered market street with 100+ stalls selling pickles, mochi, fresh tofu, matcha everything, and grilled skewers. Grab snacks as you walk: dango (sweet rice dumplings), yuba (tofu skin), and roasted chestnuts. The narrow covered street is easy to navigate with a stroller.',
              details: [
                '🍡 Must-try: Kyoto-style dango, fresh yuba, dashimaki tamago (rolled omelette)',
                '📍 Nishiki-kōji Dōri, between Teramachi and Takakura streets',
                '⏰ Most stalls open 9am–5pm. Go by 4pm for full selection.',
                '👶 Covered = rain-proof. Narrow but manageable with a compact stroller.'
              ]
            },
            {
              title: 'Gion District Evening Walk',
              description: 'The historic geisha district comes alive at dusk when the lanterns light up and the wooden machiya townhouses glow warmly. Walk along Hanami-kōji and keep your eyes peeled for a real geiko (geisha) or maiko (apprentice) heading to an evening engagement. Yasaka Shrine at the end of Shijō Dōri is beautiful lit up at night.',
              details: [
                '🏮 Hanami-kōji: the most photographed street in Kyoto',
                '👘 Spot geiko/maiko: best chances between 5:30–7pm along Hanami-kōji',
                '⛩️ Yasaka Shrine: free, open 24/7, stunning with lanterns at night',
                '📸 Photography note: never block or chase geiko — it\'s their workplace'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Gion Kappa Restaurant',
              description: 'Traditional Kyoto cuisine (kyo-kaiseki) in a relaxed setting near Yasaka Shrine. Tofu-focused menu with vegetable tempura, grilled chicken, and seasonal Kyoto vegetables. Completely pork-free. Private tatami rooms available — great for containing energetic toddlers.',
              meta: '💰 $$$ · 📍 Gion, near Yasaka Shrine · Reservations recommended'
            }
          ],
          tips: [
            { type: 'tip', text: 'The last train from Kyoto back to Osaka is around 11:30pm. Aim to be at Kyoto Station by 9pm with the toddlers. The JR Special Rapid takes 30 minutes to Osaka Station.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari Taisha', num: 1, cat: 'attraction', desc: 'Thousands of vermillion torii gates up Mount Inari' },
        { lat: 34.9680, lng: 135.7740, label: 'Rokujūan Tea House', num: 2, cat: 'food', desc: 'Traditional stone-ground ceremonial matcha' },
        { lat: 35.0173, lng: 135.6717, label: 'Arashiyama Bamboo Grove', num: 3, cat: 'attraction', desc: 'Towering bamboo forest — paved and stroller-friendly' },
        { lat: 35.0150, lng: 135.6740, label: 'Miffy Kitchen Bakery', num: 4, cat: 'food', desc: 'Miffy-shaped breads and pastries in Arashiyama' },
        { lat: 35.0105, lng: 135.6736, label: 'Iwatayama Monkey Park', num: 5, cat: 'attraction', desc: '120+ wild macaques on a mountainside lookout' },
        { lat: 35.0050, lng: 135.7641, label: 'Nishiki Market', num: 6, cat: 'food', desc: 'Kyoto\'s 400-year-old covered food market' },
        { lat: 34.9998, lng: 135.7762, label: 'Gion District', num: 7, cat: 'attraction', desc: 'Historic geisha district with lantern-lit streets' },
        { lat: 35.0136, lng: 135.6747, label: 'Arashiyama Yoshimura', num: 8, cat: 'food', desc: 'Handmade soba with Togetsu-kyō Bridge views' }
      ]
    },

    // ===== DAY 8 — MAY 22 (FRIDAY) =====
    {
      num: 8,
      date: '2026-05-22',
      neighborhoods: 'Umeda · Tempozan · Dōtonbori',
      title: 'Osaka — Pokémon Café, Aquarium & Dōtonbori Feast',
      description: "Full Osaka day hitting the big three: Pokémon Café (book well in advance!), the magnificent Kaiyūkan Aquarium (one of the world's best), and a proper late-night Dōtonbori street food crawl. Osaka is Japan's kitchen — and tonight you feast.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Pokémon Café (Reservation Required)',
              description: 'An utterly adorable café where every dish is Pokémon-themed — Pikachu curry rice, Eevee pancakes, Gengar parfaits. A giant Pikachu chef appears tableside. Reservations open exactly 31 days before your date at pokemoncafe-reservation.com (noon JST). This WILL sell out — set an alarm.',
              details: [
                '🎮 Location: Daimaru Shinsaibashi or Grand Front Osaka (check which location when booking)',
                '🎫 RESERVE at pokemoncafe-reservation.com — opens 31 days before, noon JST',
                '💰 ¥1,500–3,000/person + mandatory souvenir drink coaster/plate (¥700+)',
                '⏰ 70-minute time slots. Book the earliest slot for toddler energy levels.',
                '👶 High chairs available. The Pikachu chef visit will make your toddlers\' trip.'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Pokémon Café',
              description: 'Make the Pokémon Café your breakfast/brunch — the themed food is the activity. Pikachu omelette rice, Snorlax pancake stack, and Jigglypuff fruit plate.',
              meta: '💰 $$ · 📍 Book online 31 days in advance · 70-min time slot'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kaiyūkan Aquarium',
              description: 'One of the world\'s largest aquariums — the centerpiece is a massive Pacific Ocean tank with whale sharks, manta rays, and sunfish. The spiral walkway descends 8 floors around this central tank. Touch pools at the bottom let the toddlers pet sharks and rays. In May, the outdoor area has sea otter and seal shows.',
              details: [
                '🐋 ¥2,700 adults, ¥1,200 children (4–11), under 4 free',
                '📍 Tempozan, Osaka — 5 min walk from Osakakō Station (Chūō Line)',
                '⏰ 10am–8pm (last entry 7pm). Allow 2–3 hours.',
                '👶 Touch pool: toddlers can safely pet small sharks and rays under supervision',
                '🎡 The Tempozan Giant Ferris Wheel next door has see-through gondolas (¥800, 15 min)'
              ]
            },
            {
              title: 'Tempozan Giant Ferris Wheel',
              description: 'Right next to Kaiyūkan, this 112-meter Ferris wheel offers views of Osaka Bay, Osaka city, and on clear days, Mt. Rokko. Choose a see-through gondola if you\'re brave — the toddlers will either love it or hide.',
              details: [
                '🎡 ¥800 per person, under 3 free',
                '⏰ Open until 10pm. The night ride with city lights is magical.',
                '📸 The LED illumination at night changes based on tomorrow\'s weather forecast'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Naniwa Kuishinbo Yokochō',
              description: 'A retro food court inside Tempozan Marketplace recreating 1960s Osaka. Multiple stalls serving takoyaki, okonomiyaki, udon, and yakisoba. Easy to find pork-free options — try the seafood takoyaki and chicken okonomiyaki.',
              meta: '💰 $ · 📍 Tempozan Marketplace, next to Kaiyūkan · Family-friendly seating'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dōtonbori Street Food Crawl',
              description: 'Tonight is THE food night. Walk the length of Dōtonbori and eat everything (pork-free edition): tako-yaki (octopus balls) from Takoyaki Jūhachiban, chicken karaage from street vendors, kushikatsu chicken and shrimp skewers, beef yakisoba, and finish with matcha soft-serve. The neon signs reflect on the canal, the hawkers call out, and the energy is electric.',
              details: [
                '🐙 Takoyaki: crispy outside, gooey inside. ¥600–800 for 6–8 balls.',
                '🍗 Chicken karaage: fried chicken available at many stalls and shops',
                '🦐 Kushikatsu: deep-fried skewers — order chicken, shrimp, eggplant, lotus root (no pork)',
                '🥩 Matsusakagyu beef skewers: premium beef on a stick, no pork',
                '🍦 Pablo cheesecake tart or matcha soft-serve for dessert',
                '📸 Glico Running Man sign: best photo from the Ebisu-bashi Bridge'
              ]
            }
          ],
          meals: [
            {
              type: '🌙 Late Night',
              name: 'Halal Ramen Ayam-Ya (Dōtonbori)',
              description: 'Chicken-broth ramen paradise in the heart of Dōtonbori. Rich, creamy chicken paitan ramen that rivals any tonkotsu — but with zero pork. Also serves gyoza made with chicken. Open late, toddler-friendly with booth seating.',
              meta: '💰 $ · 📍 Dōtonbori 1-chōme · Open until midnight'
            }
          ],
          tips: [
            { type: 'tip', text: 'Pro tip for Dōtonbori with toddlers: go between 6–8pm when it\'s lively but not overwhelming. After 9pm the crowd swells and it gets harder with a stroller. Use a carrier for maximum mobility.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6673, lng: 135.5020, label: 'Pokémon Café', num: 1, cat: 'food', desc: 'Pikachu-themed café — reservation required 31 days ahead' },
        { lat: 34.6545, lng: 135.4290, label: 'Kaiyūkan Aquarium', num: 2, cat: 'attraction', desc: 'World-class aquarium with whale sharks & touch pools' },
        { lat: 34.6530, lng: 135.4280, label: 'Tempozan Ferris Wheel', num: 3, cat: 'attraction', desc: '112m wheel with see-through gondolas over Osaka Bay' },
        { lat: 34.6687, lng: 135.5013, label: 'Dōtonbori', num: 4, cat: 'food', desc: 'Osaka\'s legendary neon food street' },
        { lat: 34.6692, lng: 135.5015, label: 'Glico Running Man', num: 5, cat: 'attraction', desc: 'Iconic neon sign on Ebisu-bashi Bridge' },
        { lat: 34.6695, lng: 135.5030, label: 'Halal Ramen Ayam-Ya', num: 6, cat: 'food', desc: 'Chicken broth ramen — 100% pork-free' }
      ]
    },

    // ===== DAY 9 — MAY 23 (SATURDAY) =====
    {
      num: 9,
      date: '2026-05-23',
      neighborhoods: 'Ōsaka-jō · Shinsaibashi · Namba',
      title: 'Osaka Castle, Shopping & Final Kansai Night',
      description: "Your last full day in the Kansai region — start with the majestic Osaka Castle surrounded by cherry tree-lined moats, explore Shinsaibashi's covered shopping arcade, and spend a relaxed afternoon letting the toddlers play in a park. Tonight, have a farewell Kansai feast before heading to Guam tomorrow.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Osaka Castle & Nishinomaru Garden',
              description: 'The gleaming white-and-gold Osaka Castle sits atop a stone wall surrounded by moats. Inside is a museum of Osaka history (elevator to the 8th floor observation deck for panoramic views). The surrounding Nishinomaru Garden has open lawns perfect for toddler running, and the castle is stunning against a blue May sky.',
              details: [
                '🏯 Castle tower: ¥600 adults, free for children under 15',
                '🌿 Nishinomaru Garden: ¥200 entry. Wide lawns, cherry trees, castle views.',
                '📍 Osakajōkōen Station (JR Loop Line) or Tanimachi 4-chōme Station (Metro)',
                '👶 Stroller fine in the gardens. Inside the castle, use the elevator to skip stairs.',
                '⏰ 9am–5pm. Go early for fewer crowds.'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Café at Miraiza Osaka-jō',
              description: 'Located inside the former army headquarters building right next to the castle, this café serves Western-style breakfast and light meals. Eggs, toast, fresh juice, and coffee with a view of the castle keep. Open early and peaceful.',
              meta: '💰 $ · 📍 Miraiza Osaka-jō, inside the castle grounds · Opens 9am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shinsaibashi Shopping Arcade',
              description: 'Osaka\'s premier covered shopping street stretching 600 meters from Shinsaibashi to Namba. Department stores, Uniqlo flagship, drug stores (Daikoku Drug for Japanese cosmetics and snacks), character goods shops, and Don Quijote. The covered arcade means it\'s weatherproof and comfortable.',
              details: [
                '🛍️ Uniqlo Shinsaibashi: massive flagship with exclusive Osaka designs',
                '💊 Daikoku Drug / Matsumoto Kiyoshi: Japanese skincare, snacks, and souvenirs at drug store prices',
                '🐻 Character stores along the arcade — look for Sanrio, San-X (Sumikko Gurashi)',
                '👶 Don Quijote Dōtonbori: open until midnight, great for late-night souvenir shopping'
              ]
            },
            {
              title: 'Utsubo Park (Toddler Playtime)',
              description: 'A tranquil city park 15 minutes from Shinsaibashi with a rose garden (in full bloom in May!) and playground equipment. Give the toddlers a solid hour of free play before the evening. The adults can take turns browsing nearby Horie\'s trendy boutiques.',
              details: [
                '🌹 Rose garden: 450 varieties, May = peak bloom',
                '🛝 Playground with slides, climbing structures, and sandbox',
                '📍 Utsubohon-machi Station, 5 min walk',
                '🆓 Free entry, open anytime'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Farewell Kansai Dinner & Night Walk',
              description: 'Last night in the Kansai region before Guam tomorrow. Take a final walk along the Dōtonbori canal, watch the street performers, and soak in the chaotic energy of Osaka. Pick up last-minute omiyage (souvenirs) from the food stalls — Osaka\'s famous 551 Horai sells pork-free chicken shumai to take home.',
              details: [
                '🛍️ 551 Horai: famous for meat buns (these ARE pork — skip these) but they also sell chicken shumai',
                '🍡 Last-chance street food: takoyaki, chicken karaage, beef yakisoba',
                '📦 Pack omiyage tonight — Osaka\'s selection is incredible'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Matsusaka Beef Yakiniku M (Namba)',
              description: 'Premium yakiniku (Japanese BBQ) featuring top-grade Matsusaka wagyu beef — one of Japan\'s three great beef brands. Grill paper-thin slices of marbled beef over charcoal at your table. An unforgettable final Kansai meal. 100% beef, zero pork.',
              meta: '💰 $$$ · 📍 Namba area · Reservations recommended for dinner service'
            }
          ],
          tips: [
            { type: 'tip', text: 'Pack tonight! Tomorrow is travel day to Guam. Have the kids\' bags ready and a change of clothes accessible. Double-check your Osaka → KIX transport time.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6873, lng: 135.5262, label: 'Osaka Castle', num: 1, cat: 'attraction', desc: 'Gleaming castle with panoramic views and open gardens' },
        { lat: 34.6750, lng: 135.5010, label: 'Shinsaibashi Arcade', num: 2, cat: 'shopping', desc: '600m covered shopping street — Uniqlo, Don Quijote, character stores' },
        { lat: 34.6850, lng: 135.4930, label: 'Utsubo Park', num: 3, cat: 'attraction', desc: 'Rose garden + playground for toddler playtime' },
        { lat: 34.6687, lng: 135.5013, label: 'Dōtonbori (Night Walk)', num: 4, cat: 'food', desc: 'Final Kansai night — street food and canal views' },
        { lat: 34.6630, lng: 135.5015, label: 'Matsusaka Beef Yakiniku M', num: 5, cat: 'food', desc: 'Premium wagyu beef BBQ — unforgettable farewell dinner' }
      ]
    },

    // ===== DAY 10 — MAY 24 (SUNDAY) =====
    {
      num: 10,
      date: '2026-05-24',
      neighborhoods: 'Osaka · Kansai International Airport',
      title: 'Sayonara Osaka — Off to Guam',
      description: "A relaxed departure morning — no need to rush. Enjoy a final breakfast in the Namba area, pick up last souvenirs from the airport, and catch your flight to Guam. You'll be back in Tokyo on May 29 for the final chapter of your Japan adventure.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Final Osaka Morning',
              description: 'Sleep in if the toddlers allow it. Take a last morning walk around your neighborhood — pop into a konbini for onigiri breakfast, visit a shrine you may have passed but never entered, or simply sit at a café and watch Osaka wake up. Check out and head to the airport.',
              details: [
                '✈️ KIX from Namba: Nankai Rapi:t limited express, 38 min, ¥1,450',
                '🧳 Alternatively: JR Haruka to KIX from Tennōji, 35 min',
                '🛍️ KIX Terminal 1 has good souvenir shops — Osaka banana, matcha KitKats, rice crackers'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Last Konbini Breakfast',
              description: 'A Japanese convenience store breakfast is a genuine pleasure — onigiri, melon pan, egg sandwiches, and surprisingly good coffee. FamilyMart\'s chicken karaage and 7-Eleven\'s egg salad sandwiches are iconic. Stock up on snacks for the Guam flight.',
              meta: '💰 $ · 📍 Any 7-Eleven, FamilyMart, or Lawson'
            }
          ],
          tips: [
            { type: 'tip', text: 'You\'re coming back to Tokyo on May 29! Leave any extra luggage at a Yamato Transport counter (found in most konbini and hotels) and ship it to your Tokyo accommodation for ¥2,000–3,000. Lighter travel = happier toddlers on the Guam flights.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6659, lng: 135.4987, label: 'Namba Station', num: 1, cat: 'transport', desc: 'Nankai Rapi:t to KIX — 38 min' },
        { lat: 34.4340, lng: 135.2440, label: 'Kansai International Airport', num: 2, cat: 'transport', desc: 'Departure to Guam — see you in Tokyo on May 29!' }
      ]
    },

    // ===== DAY 11 — MAY 29 (FRIDAY) =====
    {
      num: 11,
      date: '2026-05-29',
      neighborhoods: 'Setagaya · Minato · Toyosu · Shinjuku',
      title: 'Back in Tokyo — Temples, Towers & teamLab',
      description: "You're back in Tokyo! Fresh from Guam, spend this day hitting the attractions that didn't fit in the first visit. Start at the magical cat temple of Gotokuji, then work your way through Hie Shrine, Prince Shiba Park with its Tokyo Tower views, teamLab Planets (the barefoot immersive art experience), and end with sunset from the free TMG Observatory.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Gotokuji Temple (Lucky Cat Temple)',
              description: 'The birthplace of the maneki-neko (beckoning cat) — thousands of white lucky cat figurines cover every surface of this serene temple. Buy your own maneki-neko (¥300–3,000), make a wish, and leave it among the sea of cats. The toddlers will be fascinated by the sheer number of cat statues.',
              details: [
                '🐱 Free entry. Maneki-neko available for purchase at the temple office.',
                '🚂 Miyanosaka Station (Tokyu Setagaya Line) — 2 min walk',
                '📸 The "cat altar" area with hundreds of figurines is the money shot',
                '⏰ Open 6am–6pm. Quieter in the morning.',
                '👶 Flat grounds, stroller-friendly. The gravel paths add sensory fun for toddlers.'
              ]
            },
            {
              title: 'Hie Shrine',
              description: 'A striking Shinto shrine in Akasaka with a beautiful tunnel of red torii gates (mini Fushimi Inari vibes). The main approach has a dramatic stone staircase, but there\'s an elevator for strollers. The shrine is the spiritual guardian of Tokyo and hosts one of Japan\'s three great festivals.',
              details: [
                '⛩️ Free entry. The torii tunnel is on the west side of the shrine.',
                '📍 Akasaka — between Tameike-Sannō and Akasaka-Mitsuke Stations',
                '🛗 Elevator access from the street level to the main shrine area',
                '📸 The red torii tunnel is photogenic and much less crowded than Fushimi Inari'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Atelier Matcha (Omotesandō)',
              description: 'Run by Yamamasa Koyamaen, a 160-year-old Uji tea company. Their matcha latte is made with ceremonial-grade powder — rich, earthy, zero bitterness. Pair with a matcha financier. The sleek modern interior contrasts beautifully with the ancient art of tea.',
              meta: '💰 $$ · 📍 Omotesandō area · Opens 10am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Prince Shiba Park & Tokyo Tower',
              description: 'Shiba Park is an underrated green space with perfect views of Tokyo Tower. Let the toddlers play on the lawns while the adults admire the 333-meter tower. Then visit Tokyo Tower itself — the main observation deck at 150m gives classic Tokyo views, and the tower\'s retro orange-and-white design is more photogenic than Skytree.',
              details: [
                '🗼 Main Deck (150m): ¥1,200 adults, free for under-4. Top Deck (250m): +¥2,200.',
                '🌿 Prince Shiba Park: free entry, green lawns, temple ruins, and the Zōjō-ji temple complex nearby',
                '📸 The classic "Tokyo Tower framed by trees" shot is from the park',
                '👶 Stroller-friendly park. Tower has elevators throughout.'
              ]
            },
            {
              title: 'teamLab Planets',
              description: 'A full-body immersive art museum where you wade barefoot through ankle-deep water, walk through infinite mirror rooms, and lie in fields of digital flowers. It\'s sensory magic for all ages — the toddlers will squeal with delight at the water rooms and light projections. One of the most unique experiences in Tokyo.',
              details: [
                '🎨 ¥3,800 adults, ¥1,500 children (4–12), under 4 free',
                '📍 Toyosu, near Shin-Toyosu Station (Yurikamome Line)',
                '👣 You MUST go barefoot. Roll up pants to the knee. Shorts recommended.',
                '💧 Ankle-deep warm water rooms — toddlers will LOVE splashing through',
                '👶 No strollers inside — baby carriers work well. Free stroller parking at entrance.',
                '📸 The infinity mirror rooms and waterfall rooms are jaw-dropping',
                '⏰ Book time slots online at teamlab.art. Allow 90 min–2 hrs.'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'TMG North Observatory (Free Views)',
              description: 'The Tokyo Metropolitan Government Building in Shinjuku has a FREE observation deck at 202 meters. The north observatory is open until 10pm — perfect for a nighttime visit. The views of the Shinjuku skyline and distant Tokyo landmarks are stunning. No reservation needed, just show up and take the elevator.',
              details: [
                '🆓 Completely free entry',
                '📍 Shinjuku — 10 min walk from Shinjuku Station west exit',
                '⏰ North Observatory: 9:30am–10pm (last entry 9:30pm). Closed 2nd & 4th Mondays.',
                '📸 Night views of Shinjuku\'s skyline are spectacular',
                '👶 Quick visit — 20–30 min is enough. Elevator access.'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Soranoiro Ramen (Tokyo Station)',
              description: 'Innovative ramen shop in Tokyo Station\'s Ramen Street famous for their veggie and chicken-based ramens. The chicken paitan (creamy chicken broth) is rich and satisfying — no pork anywhere on the menu. The colorful beet-noodle vegan ramen is also worth trying.',
              meta: '💰 $ · 📍 Tokyo Station Ramen Street (Yaesu side, B1F) · No reservation, expect short wait'
            }
          ],
          tips: [
            { type: 'tip', text: 'teamLab Planets tip: bring a waterproof phone case. The water rooms are incredible photo ops but phones do get splashed. Also bring a small towel to dry your feet afterward.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6532, lng: 139.6454, label: 'Gotokuji Temple', num: 1, cat: 'attraction', desc: 'Thousands of lucky cat (maneki-neko) figurines' },
        { lat: 35.6756, lng: 139.7379, label: 'Hie Shrine', num: 2, cat: 'attraction', desc: 'Red torii tunnel in Akasaka — elevator accessible' },
        { lat: 35.6567, lng: 139.7468, label: 'Prince Shiba Park', num: 3, cat: 'attraction', desc: 'Green oasis with perfect Tokyo Tower views' },
        { lat: 35.6586, lng: 139.7454, label: 'Tokyo Tower', num: 4, cat: 'attraction', desc: '333m retro tower — more photogenic than Skytree' },
        { lat: 35.6426, lng: 139.7895, label: 'teamLab Planets', num: 5, cat: 'attraction', desc: 'Barefoot immersive art — water rooms, mirrors, and light' },
        { lat: 35.6905, lng: 139.6922, label: 'TMG North Observatory', num: 6, cat: 'attraction', desc: 'Free 202m observation deck — open until 10pm' },
        { lat: 35.6651, lng: 139.7028, label: 'Atelier Matcha', num: 7, cat: 'food', desc: 'Ceremonial-grade matcha from a 160-year-old company' }
      ]
    },

    // ===== DAY 12 — MAY 30 (SATURDAY) =====
    {
      num: 12,
      date: '2026-05-30',
      neighborhoods: 'Shinjuku · Shibuya',
      title: 'Anime Shopping, JJK Pilgrimage & Farewell Dinner',
      description: "The final full day in Japan — dedicated to hitting every character store, anime reference, and shopping spot on your list. SURUGA-YA for vintage collectibles, Seria for ¥100 treasures, JJK photo ops at Shinjuku Station, and Shibuya's character stores. End with a memorable farewell dinner overlooking Tokyo's glittering skyline.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinjuku Gyoen National Garden',
              description: 'Since the garden was closed on Monday (Day 4), today is your day. Stroll through the Japanese, English, and French gardens in May\'s lush greenery. Visit SASAYAIORI+ inside the park for matcha and wagashi from a 300-year-old Kyoto confectioner. Let the toddlers run on the wide lawns while you sip tea.',
              details: [
                '🌿 ¥500 adults, free for children under 15. Closed Mondays.',
                '⏰ 9am–5:30pm (last entry 5pm). Saturday will be busy but manageable.',
                '🍵 SASAYAIORI+ matcha & wagashi set: ¥1,200. Inside the central rest area.',
                '👶 Wide paved paths, open lawns, and clean restrooms with baby-changing facilities.'
              ]
            },
            {
              title: 'SURUGA-YA Shinjuku',
              description: 'A multi-floor treasure trove of used anime figures, manga, retro games, trading cards, and collectibles. Think of it as the nerdier, more curated alternative to Akihabara. Prices are fair and the selection is enormous. Look for vintage Pokémon cards, One Piece figures, and JJK merch.',
              details: [
                '📍 Shinjuku 3-chōme area — multiple floors of anime/game goods',
                '🎮 Retro game section: Famicom, Super Famicom, N64 — great collector finds',
                '💰 Used goods are significantly cheaper than new — great for souvenirs',
                '⏰ 10am–9pm daily'
              ]
            },
            {
              title: 'Seria Shinjuku (¥100 Shop)',
              description: 'Japan\'s most stylish ¥100 store — everything is ¥110 (including tax). Unlike the chaotic Daiso, Seria has a curated, aesthetic selection. Stock up on Japanese stationery, bento accessories, cute kitchen items, and seasonal decorations. The best souvenir shop you didn\'t know existed.',
              details: [
                '💴 Everything ¥110. Bring a basket — you WILL overbuy.',
                '🎁 Best buys: chopsticks, mini plates, character stationery, bento boxes, washi tape',
                '📍 Multiple locations in Shinjuku — the one near Shinjuku Station east exit is convenient'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Matcha Morning',
              name: 'SASAYAIORI+ at Shinjuku Gyoen',
              description: 'Hand-whisked matcha with seasonal wagashi (traditional Japanese confection) inside the park\'s rest area. A 300-year-old Kyoto confectioner operating a café in one of Tokyo\'s most beautiful gardens. The perfect final matcha morning.',
              meta: '💰 $$ · 📍 Inside Shinjuku Gyoen, central rest area'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'JJK Pilgrimage — Shinjuku Station East Exit',
              description: 'Jujutsu Kaisen fans, this is your moment. The Shinjuku Station East Exit area is where the epic Domain Expansion battle took place in the manga. Stand at the iconic intersection and recreate the scenes. The large open plaza in front of Studio Alta is the recognizable backdrop.',
              details: [
                '📸 Stand at the east exit plaza and face Studio Alta for the classic JJK shot',
                '🏙️ The surrounding buildings and pedestrian areas match the manga panels',
                '📍 Shinjuku Station East Exit — you\'ve been walking past this all trip!'
              ]
            },
            {
              title: 'Shibuya Character Street & Shopping',
              description: 'Final shopping blitz in Shibuya. Hit the character stores in Shibuya PARCO (Pokémon Center, Nintendo, Capcom), browse Shibuya 109 for fashion, and explore the backstreets of Udagawachō for vintage and streetwear. Don Quijote Shibuya for final souvenir hauls.',
              details: [
                '🎮 Nintendo TOKYO (Shibuya PARCO 6F): exclusive Nintendo merch, Mario, Zelda, Splatoon',
                '🐉 Capcom Store (Shibuya PARCO 6F): Street Fighter, Monster Hunter, Resident Evil',
                '🛍️ Shibuya 109: 10 floors of Japanese fashion — trendy and unique',
                '🏪 Don Quijote Shibuya: final souvenir run. Open until midnight.'
              ]
            },
            {
              title: 'Uniqlo Shibuya (Flagship)',
              description: 'Three floors of Uniqlo with Japan-exclusive designs — UT graphic tees featuring anime collaborations (JJK, Pokémon, Studio Ghibli), AIRism innerwear, and kids\' clothing. Prices are cheaper than US Uniqlo and the designs are often Japan-only.',
              details: [
                '👕 Japan-exclusive UT tees: look for current anime collabs (¥1,500 each)',
                '👶 Kids\' section has adorable character prints at great prices',
                '📍 Udagawachō, Shibuya — near Shibuya 109'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Farewell Dinner with a View',
              description: 'Your last night in Japan deserves something special. Book a table at a restaurant with Tokyo skyline views — this is the dinner you\'ll remember. Dress up (as much as you can with toddlers), raise a glass of sake, and toast to an incredible 13 days across Japan.',
              details: [
                '🌃 Alternatively: return to Omoide Yokochō for a nostalgic bookend to the trip',
                '📦 Pack suitcases tonight — departure tomorrow',
                '🎁 Final Don Quijote run for any last souvenirs'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Sumiyoshi Ginza Steak (Shinjuku)',
              description: 'Teppanyaki steak restaurant where the chef grills premium wagyu beef right in front of you. The sizzling sounds, the flames, the theatrical presentation — toddlers love watching the cooking show. All beef, no pork. A spectacular farewell to Japan.',
              meta: '💰 $$$$ · 📍 Shinjuku area · Reservations strongly recommended'
            }
          ],
          tips: [
            { type: 'tip', text: 'Ship your souvenirs home! Most post offices and Yamato Transport counters (in konbini) offer international shipping. A medium box to the US costs ¥5,000–8,000 by surface mail (2–3 months) or ¥10,000+ by air (1 week). Much better than paying overweight luggage fees.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6852, lng: 139.7100, label: 'Shinjuku Gyoen', num: 1, cat: 'attraction', desc: 'Beautiful national garden with SASAYAIORI+ matcha café' },
        { lat: 35.6920, lng: 139.7040, label: 'SURUGA-YA Shinjuku', num: 2, cat: 'shopping', desc: 'Multi-floor vintage anime, figures & retro games' },
        { lat: 35.6925, lng: 139.7035, label: 'Seria Shinjuku', num: 3, cat: 'shopping', desc: 'Stylish ¥100 store — best souvenir shop in Japan' },
        { lat: 35.6938, lng: 139.7030, label: 'JJK — Shinjuku East Exit', num: 4, cat: 'attraction', desc: 'Jujutsu Kaisen battle location photo op' },
        { lat: 35.6620, lng: 139.6988, label: 'Shibuya PARCO', num: 5, cat: 'shopping', desc: 'Pokémon Center, Nintendo TOKYO, Capcom Store' },
        { lat: 35.6610, lng: 139.6980, label: 'Uniqlo Shibuya', num: 6, cat: 'shopping', desc: 'Flagship with Japan-exclusive anime collabs' },
        { lat: 35.6615, lng: 139.6975, label: 'Don Quijote Shibuya', num: 7, cat: 'shopping', desc: 'Final souvenir haul — open until midnight' }
      ]
    },

    // ===== DAY 13 — MAY 31 (SUNDAY) =====
    {
      num: 13,
      date: '2026-05-31',
      neighborhoods: 'Shinjuku · Narita',
      title: 'Sayonara Japan — Heading Home to DFW',
      description: "The final morning. Soak in one last Tokyo sunrise, grab a farewell konbini breakfast, and make your way to Narita Airport. It's been 13 unforgettable days across three cities, countless temples, dozens of character cafés, and a lifetime of matcha. Japan will miss you — and you'll be planning the return trip before you land in Dallas.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Final Morning in Shinjuku',
              description: 'Wake up one last time in Shinjuku. If time allows, take a quiet walk through the neighborhood — the early morning energy of Tokyo is different from the nighttime chaos. Workers rushing to trains, shop owners sweeping sidewalks, the smell of fresh bread from bakeries. One last moment to feel the rhythm of this incredible city.',
              details: [
                '☕ Grab one final matcha from the nearest café or konbini',
                '📦 Double-check luggage, passports, and souvenirs',
                '🚂 Narita Express from Shinjuku: 90 min. Check your flight time and work backward.'
              ]
            },
            {
              title: 'Narita Express to Airport',
              description: 'The N\'EX will take you back to Narita in 90 minutes. Book reserved seats for a stress-free ride. At the airport, use the remaining time to browse the duty-free shops — Royce chocolate, Tokyo Banana, matcha KitKats, and Japanese whisky.',
              details: [
                '🎫 ¥3,250 adult one-way. Children under 6 free.',
                '🛍️ NRT Terminal 1/2 duty-free: Royce Nama Chocolate (must-buy), matcha KitKats, sake',
                '🍌 Tokyo Banana: the classic souvenir — buy a box for the folks back home',
                '✈️ Allow 3 hours before your flight for international departure with toddlers'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Final Konbini Farewell',
              description: 'One last Japanese convenience store breakfast. Grab an egg sandwich (tamago sando), an onigiri, a melon pan, and a canned coffee. This is Japan distilled into ¥500.',
              meta: '💰 $ · 📍 Any konbini near your Airbnb'
            }
          ],
          tips: [
            { type: 'tip', text: 'Tax-free shopping: if you bought items at duty-free counters, keep the receipts stapled in your passport. Customs may check at Narita departure.' },
            { type: 'tip', text: 'Flight tip: pack a bag of new gachapon toys and konbini snacks for the toddlers to discover on the plane. Ration them out every 30 minutes for maximum peace.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6896, lng: 139.7006, label: 'Shinjuku Station (N\'EX)', num: 1, cat: 'transport', desc: 'Narita Express departure — 90 min to airport' },
        { lat: 35.7720, lng: 140.3929, label: 'Narita Airport', num: 2, cat: 'transport', desc: 'Final departure — sayonara, Japan! ✈️ → DFW' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (family)', budget: '¥10,000–20,000/night', midrange: '¥20,000–40,000/night', luxury: '¥40,000–80,000/night' },
    { category: 'Meals (family of 5)', budget: '¥5,000–10,000/day', midrange: '¥10,000–20,000/day', luxury: '¥20,000–50,000/day' },
    { category: 'Transport', budget: '¥2,000–5,000/day', midrange: '¥5,000–10,000/day', luxury: '¥10,000–20,000/day' },
    { category: 'Activities', budget: '¥3,000–6,000/day', midrange: '¥6,000–15,000/day', luxury: '¥15,000–30,000/day' },
    { category: 'Shinkansen (Tokyo→Osaka)', budget: '¥14,720/adult', midrange: '¥14,720/adult', luxury: '¥22,000/adult (Green Car)' },
    { category: '13-Day Total (family of 5)', budget: '¥400,000–600,000', midrange: '¥600,000–1,000,000', luxury: '¥1,000,000–2,000,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Narita Airport (NRT): main international hub. Narita Express to Shinjuku: 90 min, ¥3,250', 'Haneda Airport (HND): closer to city center. Monorail/Keikyu to Shinjuku: 45–60 min', 'Children under 6 ride FREE on all trains (JR, subway, Shinkansen free seats)', 'Japan Rail Pass: consider the 7-day or 14-day pass if using Shinkansen + JR lines extensively'] },
    { title: '🏨 Where to Stay', items: ['Tokyo: Shinjuku is ideal — central, accessible, nightlife-adjacent. Your Airbnb is perfectly located.', 'Osaka: Namba or Shinsaibashi — walking distance to Dōtonbori, easy metro to Nara and Kyoto', 'Look for places with washing machines (essential with toddlers) and elevator access', 'Japanese apartments often have deep soaking tubs — great for toddler bath time'] },
    { title: '👶 Toddler Tips', items: ['Baby rooms (授乳室) in every major station and department store: changing tables, hot water, nursing', 'Rent a stroller in Japan if you don\'t want to bring one — several rental services at Narita and Tokyo', 'Japanese diapers (Merries, Moony) are among the best in the world — buy at any drug store', 'Most restaurants provide kids\' chopsticks or spoons. High chairs at chain restaurants and family restaurants (ファミレス)', 'Japanese public toilets often have child seats built into the stall wall — genius design'] },
    { title: '📱 Connectivity', items: ['Rent a pocket WiFi at Narita (¥800–1,200/day) or buy an eSIM (Ubigi, Airalo)', 'Google Maps works perfectly in Japan — use it for all train navigation', 'Download Google Translate with Japanese offline pack for menu reading', 'Suica/Pasmo IC card works on all trains, buses, and even vending machines'] },
    { title: '🚫 Pork-Free Quick Guide', items: ['"Buta nashi" (豚なし) = "no pork" — say this at restaurants', '"Buta" (豚) on a menu = pork — avoid these items', 'Safe bets: chicken (tori/鶏), beef (gyū/牛), seafood (sakana/魚), tofu (tōfu)', 'Ramen: ask for "tori paitan" (chicken broth) or "shio" (salt-based)', 'Convenience stores: salmon, tuna, umeboshi, and kombu onigiri are always pork-free', 'Many dashi stocks use bonito (fish) — this is fine. Some use pork — ask at fancy kaiseki restaurants.'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
