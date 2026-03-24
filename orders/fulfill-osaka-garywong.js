const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1774267963325_pqmiw3',
  email: 'garywong79@me.com',
  customerName: null,
  startDate: '2026-04-30'
};

const itineraryData = {
  destination: 'Osaka, Japan',
  countryEmoji: '🇯🇵',
  title: 'Osaka: Neon Nights, Nintendo Worlds & Namba Bites',
  subtitle: '7 days of USJ thrills, teamLab wonder, Kobe beef, and Pokémon magic — the ultimate Osaka family adventure',
  description: 'A packed 7-day family adventure through Osaka and beyond, perfectly timed for Golden Week. Ride through The Wizarding World of Harry Potter at USJ, get lost in teamLab\'s glowing Botanical Garden, hunt down Pokémon at the famous Shinsaibashi café, shop the premium outlets in Kobe, and cap each night with some of Japan\'s finest dining. This is Osaka turned up to eleven — where neon-lit food streets meet world-class museums and roller coasters.',
  duration: '7 days',
  dates: 'April 30 – May 6, 2026',
  budget: '$2,000–5,000',
  pace: 'Active — full days with early starts (Golden Week crowds demand it)',
  bestFor: 'Family · Foodies · Theme Parks · Night Art',
  highlights: [
    'Universal Studios Japan — Wizarding World, Super Nintendo World, Express Passes are non-negotiable in Golden Week',
    'teamLab Botanical Garden Osaka — luminous night art installations in Nagai Park',
    'Pokémon Cafe Osaka (Shinsaibashi) — themed food and exclusive merch',
    'Kobe Premium Outlet — designer brands + harbor views in 30 min from Osaka',
    'Osaka\'s 3-Michelin-star dining scene — Fujiya 1935, Hajime, and more',
    'Osaka Castle, Dotonbori, Shinsekai & Kuromon Market — the city\'s iconic backbone',
    '⚠️ Golden Week survival guide — how to beat the crowds at every stop'
  ],

  essentials: [
    {
      title: '⚠️ Golden Week Warning',
      text: 'You\'re visiting during Golden Week (April 29 – May 5) — Japan\'s biggest holiday when the entire country travels at once. Expect 30–50% longer queues everywhere. Hotels cost 2–3× normal rates. Book EVERYTHING now: USJ Express Passes, Pokémon Cafe reservations, teamLab tickets, and restaurant reservations. The good news: the atmosphere is electric and the energy is unlike any other time of year.'
    },
    {
      title: '🚇 Getting Around',
      text: 'Buy an ICOCA card at Osaka/Kansai Airport (or any JR station). Loads like a debit card, works on all trains, subways, and buses throughout Osaka, Kobe, and Nara. For Kobe: take the JR Kobe Line from Osaka Station (~30 min, ¥410). For Nara: take the Kintetsu Nara Line from Namba (~45 min, ¥680). Within Osaka, the Midosuji subway line covers most attractions. Taxis are plentiful but expensive; Uber operates in Osaka.'
    },
    {
      title: '🏨 Where to Stay',
      text: 'Best base: Namba/Shinsaibashi area — walking distance to Dotonbori, Pokémon Cafe, and easy subway to everywhere else. Top picks: Conrad Osaka (Nakanoshima, luxury), Cross Hotel Osaka (Namba, mid-range), Dormy Inn Premium Namba (budget, great breakfast). Book well in advance — Golden Week hotels sell out months ahead.'
    },
    {
      title: '📱 Apps & Essentials',
      text: 'Google Maps (download Osaka offline map). Google Translate with camera mode (Japanese menus). HyperDia or Navitime for train routes. JPY cash — bring more than you think, many smaller restaurants are cash-only. Pocket Wi-Fi or Japan SIM (rent at airport). Comfortable shoes — you\'ll walk 15,000–20,000 steps/day.'
    },
    {
      title: '💰 Budget Reality Check',
      text: '$2,000–5,000 for 3–4 people over 7 days. Fine dining dinners average ¥15,000–30,000/person (more for Michelin 3-stars). USJ Express Passes run ¥6,500–10,000/person. teamLab ¥3,200/person. Pokémon Cafe set menus ~¥2,500/person. With fine dining every night, budget $150–250/person/night for dinner alone. Lunches can be casual (¥1,000–2,500/person). Total is achievable if you\'re selective about which nights go full Michelin vs. premium casual.'
    },
    {
      title: '🌸 May Weather',
      text: 'Late April/early May in Osaka: 16–24°C. Light jacket for evenings. Occasional brief showers — bring a compact umbrella. USJ is outdoors for much of it; comfortable walking shoes essential. The golden hour light during Golden Week is stunning for photos.'
    }
  ],

  days: [
    {
      num: 1,
      title: 'Arrival, Dotonbori & Namba',
      neighborhoods: 'Namba · Dotonbori · Shinsaibashi · Kuromon',
      description: 'Touch down in Osaka, get your bearings in the city\'s buzzing entertainment core, and ease into the trip with a stroll through Dotonbori\'s neon wonderland and a dinner to remember.',

      timeBlocks: [
        {
          label: '✈️ Arriving at Kansai International Airport',
          activities: [
            {
              title: 'Airport → Namba (Haruka Express or Airport Limousine)',
              description: 'From KIX, the fastest option to Namba is the JR Haruka Express (45 min, ¥2,410/person to Osaka Station) or Airport Limousine Bus (50–60 min, ¥1,600/person, drops near Namba OCAT). Buy ICOCA cards at the airport JR station — they\'ll be your lifeline for the whole trip.',
              details: [
                '🚂 JR Haruka: Kansai Airport Station → Osaka/Tennoji (45 min, IC discount ¥1,080 with advance purchase)',
                '🚌 Limousine Bus: Easiest with luggage, drops at Namba OCAT, ¥1,600/person',
                '🛏️ Check in to hotel first — most check-ins from 3 PM; ask to store luggage if early',
                '💴 Pick up ¥50,000–80,000 JPY cash from airport 7-Eleven ATM (accepts all foreign cards)'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: '💡 At the airport, visit the USJ ticket counter or kiosk to pick up Express Passes if you haven\'t pre-booked. Golden Week stock sells out fast.' }
          ]
        },
        {
          label: '🏮 3:00 PM — Kuromon Ichiba Market (黒門市場)',
          activities: [
            {
              title: 'Kuromon Ichiba — Osaka\'s Kitchen',
              description: 'Called "Osaka\'s Kitchen," this 580-meter covered market has been feeding the city since 1902. Vendors line up selling wagyu beef skewers, fresh seafood, tamagoyaki, and everything in between. Perfect for an afternoon snack and food photo fest.',
              details: [
                '📍 2-4-1 Nipponbashi, Namba — 10 min walk from Namba Station',
                '⏰ Hours: Most stalls 8 AM – 6 PM. Busiest mid-afternoon.',
                '💰 Snacks: ¥200–800 each. Perfect for grazers.',
                '⏱️ Allow 45–60 minutes to wander and eat',
                '🦀 Must-try: fresh scallop grilled on-the-half-shell, wagyu beef skewer, tamagoyaki roll',
                '📸 The market is photogenic — old neon signs, fresh seafood displays, vendors calling out'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: '🦐 Golden Week means this market will be packed. Arrive before 3 PM if possible — lines at popular stalls grow quickly.' }
          ]
        },
        {
          label: '🌆 5:00 PM — Dotonbori',
          activities: [
            {
              title: 'Dotonbori Canal Walk',
              description: 'Osaka\'s most iconic neighborhood — a riot of neon signs, giant mechanical crabs, and the famous Glico running man billboard. Walk the Tombori Riverwalk along the canal for the best vantage point. This stretch is even more electric at night, so come back after dinner.',
              details: [
                '📍 Along Dotonbori Canal, accessible from Namba Station exits',
                '🦀 Kani Doraku: the giant moving crab sign is the classic Osaka photo',
                '🏃 Glico Man Billboard: iconic illuminated sign at the east end of the canal',
                '🌉 Tombori Riverwalk: boardwalk beneath the bridges — great canal perspective',
                '🎡 Ebisu-bashi Bridge: most popular selfie spot in all of Osaka',
                '⏱️ Allow 1 hour for photos + evening stroll before dinner'
              ]
            }
          ]
        },
        {
          label: '🍽️ 7:30 PM — Fine Dining Dinner',
          meals: [
            {
              type: '⭐ DINNER',
              name: 'Fujiya 1935 (藤家 1935) — 3 Michelin Stars',
              description: 'Chef Tetsuya Fujiwara\'s 3-star restaurant is one of Osaka\'s finest achievements — a contemporary Japanese experience fusing kaiseki principles with avant-garde technique. The tasting menu changes seasonally and is a masterclass in precision and flavor. Set menus ¥30,000+/person.',
              meta: '📍 1-4-19 Shimanouchi, Chuo-ku · ✉️ Reservations essential — book months in advance · 💰 ¥30,000–50,000/person'
            },
            {
              type: '⭐ ALTERNATIVE',
              name: 'Hajime (一) — 3 Michelin Stars',
              description: 'Chef Hajime Yoneda\'s landmark French-Japanese restaurant — one of Osaka\'s two 3-star establishments. The signature dish "Earth" (a hemisphere of compacted vegetables) is legendary. 8-course dinner menus from ¥30,000/person.',
              meta: '📍 1-9-11 Edobori, Nishi-ku · ✉️ Reserve months ahead · 💰 ¥30,000+/person'
            },
            {
              type: '⭐⭐ ACCESSIBLE ALTERNATIVE',
              name: 'Kahala (カハラ) — 1 Michelin Star',
              description: 'If the 3-stars are fully booked, Kahala offers a 1-star creative Japanese experience that\'s slightly easier to reserve. Located near Shinsaibashi, chef Hirohito Shichi\'s inventive cuisine is a revelatory introduction to Osaka\'s dining scene. ¥20,000–25,000/person.',
              meta: '📍 2-3-8 Nishishinsaibashi · ✉️ Book 2–4 weeks ahead · 💰 ¥20,000–25,000/person'
            }
          ],
          tips: [
            { type: 'tip', text: '⚠️ Golden Week fills even the most obscure restaurants. Book ALL dinners before you land in Japan. Tableall, Tablecheck, and Omakase apps allow English reservations at Michelin establishments.' }
          ]
        }
      ],

      mapPins: [
        { lat: 34.6659, lng: 135.5087, label: 'Kuromon Ichiba Market', num: 1, cat: 'food', desc: 'Osaka\'s Kitchen — snacks and wagyu skewers' },
        { lat: 34.6687, lng: 135.5024, label: 'Dotonbori Canal', num: 2, cat: 'attraction', desc: 'Neon signs, Glico Man, crab billboard' },
        { lat: 34.6673, lng: 135.5019, label: 'Ebisu-bashi Bridge', num: 3, cat: 'attraction', desc: 'Most iconic selfie spot in Osaka' },
        { lat: 34.6754, lng: 135.5003, label: 'Fujiya 1935 / Kahala', num: 4, cat: 'food', desc: '3-star fine dining in Shimanouchi' }
      ]
    },
    {
      num: 2,
      title: 'Universal Studios Japan (USJ)',
      neighborhoods: 'Sakurajima · USJ',
      description: 'A full day at one of Japan\'s most thrilling theme parks. During Golden Week, crowds are at maximum — your Express Pass is not optional. Hit the headliners first thing, then rotate through the rest of the day.',

      timeBlocks: [
        {
          label: '🎢 7:30 AM — Arrive at USJ (Beat the Crowds)',
          activities: [
            {
              title: 'Getting to Universal Studios Japan',
              description: 'Take the JR Sakurajima Line from Osaka Station (Umeda) to Universal City Station — about 13 minutes, ¥160/person. Gates typically open at 8:30–9:00 AM during Golden Week; queues form from 7:30 AM. Arrive early.',
              details: [
                '🚂 Osaka Station (Umeda) → Universal City Station: JR Sakurajima Line, 13 min, ¥160',
                '⏰ Park opening: 8:30–9:00 AM (check USJ website day before — Golden Week often opens early)',
                '🎟️ 1-Day Ticket: ~¥9,400/adult, ¥6,300/child (4–11)',
                '🚀 Express Pass 7: ~¥9,000–15,000/person. Covers 7 headliner attractions. ESSENTIAL for Golden Week.',
                '⚠️ Express Pass for Super Nintendo World sells separately as "Express: Super Nintendo World Area" (~¥3,000 add-on)',
                '⏱️ Plan for 10–11 hours in the park'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: '⚡ USJ\'s Virtual Line system (via the app) replaces physical queues for Super Nintendo World — download the USJ app and set up Virtual Line entry as soon as you\'re in the park. Slots for popular time windows fill within minutes of park opening.' }
          ]
        },
        {
          label: '⚡ 9:00 AM — The Wizarding World of Harry Potter (First)',
          activities: [
            {
              title: 'Harry Potter & the Forbidden Journey + Hogwarts Castle',
              description: 'Head here the INSTANT the park opens — before Golden Week crowds descend. Harry Potter and the Forbidden Journey is USJ\'s crown jewel: a stunning 4D simulation ride through the Hogwarts universe. Walking into Hogsmeade village with its snow-dusted rooftops and butterbeer carts is genuinely magical.',
              details: [
                '⏱️ Ride: ~4 min. Queue without Express Pass: 60–120 min on Golden Week',
                '🏰 Spend 20 min just walking through Hogwarts Castle before the ride',
                '🍺 Butterbeer: hot or cold, ~¥900. Also try pumpkin juice (¥700)',
                '🛍️ Ollivanders wand shop: ¥5,500 for an interactive wand + map of casting spots throughout Hogsmeade',
                '📸 Best photo: standing at the bottom of the Hogwarts hill looking up'
              ]
            }
          ],
          tips: [
            { type: 'reddit', text: '"Get to Hogsmeade when the gates open and go straight to Forbidden Journey. The 8:30 AM line is 20 min. By 11 AM it\'s 2 hours. The Express Pass for this ride alone pays for itself."', cite: 'r/USAirlines → USJ thread' }
          ]
        },
        {
          label: '🎮 11:00 AM — Super Nintendo World',
          activities: [
            {
              title: 'Super Nintendo World — Mario Kart: Koopa\'s Challenge',
              description: 'The most visually stunning area in any theme park in the world — every wall is interactive, every corner hides a surprise, and the Mario Kart ride is genuinely next-level. Buy the wristband (included with some Express Passes) to interact with question blocks and collect coins throughout the area.',
              details: [
                '⏱️ Mario Kart ride: ~5 min. Express Pass or Virtual Line required on Golden Week.',
                '🎮 Power-Up Band wristband: ¥3,300 — connects to your phone to track points and compete',
                '🏁 1-2-Switch-style competitions at various interactive points throughout the area',
                '🍄 Kinopio\'s Cafe inside the area: Mario-themed food (¥1,500–2,500/person) — reserve in advance',
                '⏱️ Budget 2–3 hours to fully explore Super Nintendo World'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: '🎮 Kids will want to stay here forever. If you have time, do a second circuit — there are hidden interactions kids discover each time. The Yoshi\'s Adventure ride is great for younger children (no height restriction).' }
          ]
        },
        {
          label: '🍔 1:30 PM — Lunch in the Park',
          meals: [
            {
              type: '🍔 LUNCH',
              name: 'Park Dining (budget for speed)',
              description: 'USJ has decent themed food, but Golden Week means long lunch queues. Strategic approach: bring snacks for mid-morning, eat lunch at 1:30 PM when the main rush dies down. Park Food Court (Minion Park area) has shorter lines than themed restaurants.',
              meta: '💰 ¥1,500–2,500/person for park food · Pre-order on the USJ app where possible'
            }
          ]
        },
        {
          label: '🎭 3:00 PM — Minion Park + Jaws/Jurassic Park Area',
          activities: [
            {
              title: 'Minion Park & Hollywood Area',
              description: 'Minion Mayhem is a 4D motion simulator that\'s perfect for kids — hilarious and not too intense. Minion Park is also the best area for themed merchandise and character meet-and-greets. Follow with a ride on Jaws (classic, underrated) or Hollywood Dream (the rollercoaster with music selection).',
              details: [
                '🎭 Minion Mayhem: 4D ride, ~4 min. Queue 30–60 min without Express',
                '🦈 Jaws: 8-min boat tour, surprisingly fun, 20–40 min wait',
                '🎢 Hollywood Dream: USJ\'s main rollercoaster, up to 120 km/h, J-pop soundtrack',
                '🛍️ Minion merch is unique to USJ — the plushies and accessories are legitimately charming'
              ]
            }
          ]
        },
        {
          label: '🌙 6:00 PM — Evening Entertainment + Exit',
          activities: [
            {
              title: 'Nighttime Spectacular',
              description: 'Golden Week USJ often runs extended hours to 9 PM or later. The park at night is a different vibe — Hogwarts Castle gets spectacular projection mapping after dark. The parade route lights up and the crowds actually thin out slightly as families with young kids leave.',
              details: [
                '🎇 Check USJ app for Golden Week evening shows and parade times',
                '📸 Hogwarts at night with projection mapping is one of the best photo ops in Japan',
                '🚂 Return to Osaka: Universal City → Osaka Station (JR Sakurajima), 13 min'
              ]
            }
          ]
        },
        {
          label: '🍽️ 8:30 PM — Fine Dining Dinner',
          meals: [
            {
              type: '⭐ DINNER',
              name: 'La Becasse (ラ ベカス) — 2 Michelin Stars',
              description: 'Chef Yukimasa Kinoshita\'s elegant French restaurant has held 2 Michelin stars for over a decade. The cuisine leans into Japan\'s finest seasonal ingredients — a French technique meets Japanese terroir approach. Refined, unhurried — perfect after a full day of rides and queues.',
              meta: '📍 2-4-14 Kitakyuhoji-machi, Chuo-ku · ✉️ Reservations required · 💰 ¥20,000–30,000/person'
            },
            {
              type: '⭐ ALTERNATIVE',
              name: 'Ristorante Honda — 2 Michelin Stars (Italian-Japanese)',
              description: 'Chef Satoshi Honda\'s Italian-Japanese restaurant is one of Osaka\'s most celebrated crossover dining experiences. Inventive courses draw on both Japanese and Italian traditions. Reservations easier to get than the top French houses.',
              meta: '📍 Nishi-ku area · ✉️ Book 2–3 weeks ahead · 💰 ¥18,000–25,000/person'
            }
          ]
        }
      ],

      mapPins: [
        { lat: 34.6654, lng: 135.4323, label: 'Universal Studios Japan', num: 1, cat: 'attraction', desc: 'USJ main entrance — arrive 30 min before opening' },
        { lat: 34.6679, lng: 135.4310, label: 'Wizarding World of Harry Potter', num: 2, cat: 'attraction', desc: 'Hogsmeade, Hogwarts Castle, Forbidden Journey' },
        { lat: 34.6671, lng: 135.4351, label: 'Super Nintendo World', num: 3, cat: 'attraction', desc: 'Mario Kart: Koopa\'s Challenge, Power-Up Bands' }
      ]
    },
    {
      num: 3,
      title: 'Osaka Castle, Shinsekai & Tennoji',
      neighborhoods: 'Osaka-jo · Shinsekai · Tennoji · Abeno',
      description: 'A day exploring Osaka\'s historic heart and retro entertainment district — from the gleaming castle towers to the neon-lit kushikatsu alleys of Shinsekai. Finish with sunset drinks at Japan\'s highest bar.',

      timeBlocks: [
        {
          label: '🏯 9:00 AM — Osaka Castle Park (大阪城公園)',
          activities: [
            {
              title: 'Osaka Castle & Museum',
              description: 'The magnificent golden-roofed Osaka Castle is one of Japan\'s most recognizable landmarks, originally built by Toyotomi Hideyoshi in 1583. The castle interior is an excellent modern museum covering Osaka\'s turbulent history. The surrounding 106-hectare park is stunning — during early May, some late cherry blossoms and fresh green foliage frame the castle tower.',
              details: [
                '⏰ Hours: 9:00 AM – 5:00 PM (last entry 4:30 PM)',
                '💰 Castle museum: ¥600/adult, free for children under 15',
                '⏱️ Allow 2–2.5 hours for castle + park walk',
                '🗼 8th floor observatory: panoramic views of modern Osaka surrounding the ancient keep',
                '🚇 Nearest station: Osakajokoen Station (JR Loop Line) or Tanimachi 4-chome (subway)',
                '⚠️ Golden Week means the castle interior queues can run 30–45 min. Go early morning.'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: '📸 Best photo of the castle: walk through the Ote-mon gate (main entrance) and look back at the castle over the moat. Morning light before 10 AM is golden.' },
            { type: 'reddit', text: '"Most visitors just do the castle museum but the surrounding park is massive. Walk north to Nishinomaru Garden for a different perspective of the castle over the cherry blossom area."', cite: 'r/JapanTravel' }
          ]
        },
        {
          label: '🍱 12:00 PM — Lunch Near Castle',
          meals: [
            {
              type: '🍜 LUNCH',
              name: 'Osaka Castle Park Food Stalls',
              description: 'During Golden Week, food trucks and stalls set up throughout the park. Great for casual eating between sightseeing — takoyaki, grilled corn, yakisoba, and cold drinks available throughout.',
              meta: '💰 ¥800–1,500 per person · Perfect casual post-castle lunch'
            }
          ]
        },
        {
          label: '🗼 2:00 PM — Abeno Harukas 300 (あべのハルカス)',
          activities: [
            {
              title: 'Abeno Harukas — Highest Building in Japan',
              description: 'At 300 meters, the Harukas 300 observation deck on floors 58–60 offers a 360-degree panorama that stretches from Kobe to Kyoto on a clear day. The ticket includes access to the outdoor sky walk — wind rushing past, the entire Osaka basin spread below. A must for geography nerds and anyone who loves a skyline view.',
              details: [
                '📍 1-1-43 Abenosuji, Abeno-ku (connected to Tennoji Station)',
                '⏰ Hours: 9:00 AM – 10:00 PM',
                '💰 ¥2,000/adult, ¥1,200/child',
                '⏱️ Allow 45–60 minutes',
                '☁️ Check visibility forecast — a clear May day can show mountains 80 km away',
                '🚇 Tennoji Station: connected directly to the building'
              ]
            }
          ]
        },
        {
          label: '⚡ 3:30 PM — Shinsekai (新世界)',
          activities: [
            {
              title: 'Shinsekai — Old Osaka\'s Neon Nostalgia',
              description: 'Shinsekai is a fascinatingly retro district built in 1912 to evoke both Paris (north half) and Coney Island (south half). Today it\'s the spiritual home of kushikatsu (deep-fried skewers), pachinko parlors, and vintage Billiken statues. It\'s gritty, quirky, and utterly unlike anywhere else in Japan.',
              details: [
                '📍 5-min walk from Tennoji Station, south of Tsutenkaku Tower',
                '🗼 Tsutenkaku Tower: ¥800, retro 1956 tower with great Shinsekai views',
                '🍢 Kushikatsu: deep-fried skewers of every imaginable ingredient — the rule is NO double-dipping in communal sauce. Sacred.',
                '⏱️ Allow 1.5–2 hours for walk, tower, and snacks',
                '🎰 The pachinko noise is intense. Either lean into it or wear headphones while walking through.'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: '🍢 Daruma is the legendary Shinsekai kushikatsu institution. Queue outside for 15–20 min is worth it. Order the "standard set" of 10 skewers to start.' }
          ]
        },
        {
          label: '🍽️ 7:00 PM — Fine Dining Dinner',
          meals: [
            {
              type: '⭐ DINNER',
              name: 'Mizai (水暉) — 3 Michelin Stars',
              description: 'One of Osaka\'s most rarefied dining experiences: a classic kaiseki progression through Japan\'s finest seasonal ingredients. Chef Kunio Tokuoka\'s menu changes monthly and features course after course of exquisite seasonal dishes — dashi so clear it\'s almost translucent, local fish with perfect texture, wagyu that dissolves into silk. Count on ¥40,000+ per person.',
              meta: '📍 Hotel Monterey La Soeur Osaka area · ✉️ Reserve 2+ months in advance · 💰 ¥40,000+/person'
            },
            {
              type: '⭐⭐ ACCESSIBLE ALTERNATIVE',
              name: 'Sushi Saito Osaka (or equivalent Michelin sushi)',
              description: 'For a slightly more accessible fine dining night, seek out one of Osaka\'s top omakase sushi counters (8–12 courses, chef\'s selection). Osaka has a rich sushi tradition. ¥25,000–35,000/person.',
              meta: '💰 ¥25,000–35,000/person · Reserve 2–4 weeks ahead'
            }
          ]
        }
      ],

      mapPins: [
        { lat: 34.6873, lng: 135.5262, label: 'Osaka Castle', num: 1, cat: 'attraction', desc: 'Toyotomi Hideyoshi\'s 16th-century masterpiece' },
        { lat: 34.6464, lng: 135.5138, label: 'Abeno Harukas 300', num: 2, cat: 'attraction', desc: 'Japan\'s highest observation deck at 300m' },
        { lat: 34.6522, lng: 135.5063, label: 'Shinsekai', num: 3, cat: 'attraction', desc: 'Retro district — kushikatsu and Tsutenkaku Tower' },
        { lat: 34.6530, lng: 135.5068, label: 'Tsutenkaku Tower', num: 4, cat: 'attraction', desc: 'Iconic 1956 tower in Shinsekai' }
      ]
    },
    {
      num: 4,
      title: 'Kobe Day Trip: Premium Outlet, Harborland & Kobe Beef',
      neighborhoods: 'Kobe · Suma · Harborland · Nankinmachi',
      description: 'A full day in Japan\'s most cosmopolitan port city — shop until you drop at Kobe Premium Outlet, stroll the scenic harbor, and close out the day with Kobe beef teppanyaki.',

      timeBlocks: [
        {
          label: '🛍️ 9:30 AM — Kobe Premium Outlets',
          activities: [
            {
              title: 'Kobe Premium Outlets (三井アウトレットパーク マリンピア神戸)',
              description: 'Located in the Suma district of Kobe, right on the waterfront with views of Osaka Bay, this premium outlet mall houses 200+ stores including Gucci, Prada, Burberry, Coach, and many Japanese brand outlets. Golden Week means great sales and slightly longer crowds than usual, but the outdoor layout keeps it from feeling claustrophobic.',
              details: [
                '🚂 Getting there: JR Osaka → Sannomiya (30 min, ¥410), then Kobe subway Seishin-Yamate Line to Myodani (15 min, ¥250), then taxi/bus to Marine Pia Kobe (10 min)',
                '📍 OR direct from Osaka Umeda/Namba by highway bus (~50 min, ¥750/person)',
                '⏰ Hours: 10:00 AM – 8:00 PM',
                '🏪 Featured brands: Gucci, Prada, Burberry, Coach, Polo Ralph Lauren, Armani, Kate Spade, plus Nike, Adidas, and 140+ others',
                '⏱️ Budget 2.5–3 hours for a proper outlet sweep'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: '💳 Bring your passport — many stores offer a tax-free discount (8% back) for foreign visitors on purchases ¥5,000+. Bring a big empty bag.' }
          ]
        },
        {
          label: '🌊 1:00 PM — Kobe Harborland & Mosaic',
          activities: [
            {
              title: 'Kobe Harborland (神戸ハーバーランド)',
              description: 'From the outlet, hop on the subway to central Kobe\'s stunning waterfront development. The Mosaic shopping center sits on a pier with spectacular views back toward the city and the Akashi Kaikyo Bridge in the distance. The harbor promenade is one of Japan\'s most pleasant walks.',
              details: [
                '🚂 Marine Pia Kobe → Harborland: ~20 min by bus or return to Sannomiya then walk',
                '🛍️ Mosaic: mid-range shops, food halls, a small carousel, waterfront restaurants',
                '🎡 Mosaic Garden: free outdoor area with great harbor views and photo spots',
                '⏱️ 45–60 min for harbor walk + light shopping'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: '📸 The best harbor photo is from the end of the Mosaic pier — look back toward the city skyline with the Ferris wheel and cruise ships behind you.' }
          ]
        },
        {
          label: '🥟 2:30 PM — Nankinmachi Chinatown (南京町)',
          activities: [
            {
              title: 'Nankinmachi — Japan\'s Most Beautiful Chinatown',
              description: 'One of Japan\'s three major Chinatowns (alongside Yokohama and Nagasaki), Nankinmachi is compact but packed with atmosphere. Browse the colorful stalls selling steamed pork buns, chilled sesame noodles, and roast pork. The ornate gate and painted architecture make for a striking color contrast to the rest of Kobe.',
              details: [
                '📍 Motomachi 1-chome, Chuo-ku, Kobe — 5 min walk from Motomachi Station',
                '⏱️ 30–45 min to walk and snack',
                '🥟 Must-try: steamed butaman pork buns (¥300), roast duck rice, dan dan noodles',
                '⚠️ Golden Week turns this small alley extremely crowded. Move slowly and enjoy the chaos.'
              ]
            }
          ]
        },
        {
          label: '🥩 7:00 PM — Kobe Beef Dinner',
          meals: [
            {
              type: '🥩 DINNER',
              name: 'Kobe Plaisir (神戸プレジール) — A5 Kobe Beef Set',
              description: 'The quintessential Kobe beef fine dining experience. Chef-operated teppanyaki restaurant serving certified A5 Hyogo Prefecture wagyu — the beef so marbled it cooks in its own fat in seconds. The tenderloin set runs ¥25,000–40,000/person but this is the real Kobe beef on its home turf.',
              meta: '📍 Sannomiya area, Kobe · ✉️ Reservations highly recommended · 💰 ¥25,000–40,000/person'
            },
            {
              type: '🥩 ALTERNATIVE',
              name: 'Steak Land Kobe (ステーキランド神戸) — Lunch/Dinner Teppanyaki',
              description: 'More accessible Kobe beef teppanyaki — great quality at a fraction of the price. Sets from ¥6,500 for filet mignon, up to ¥18,000 for premium wagyu loin. Bustling, fun atmosphere where the chefs put on a show at the grill.',
              meta: '📍 1-8-2 Kitanagasadori, Chuo-ku, Kobe · Walk-in friendly · 💰 ¥6,500–18,000/person'
            }
          ],
          tips: [
            { type: 'tip', text: '🐄 Look for the "Kobe Beef" authentication card — real Kobe beef must come from Tajima cattle raised in Hyogo Prefecture and certified by the Kobe Beef Marketing & Distribution Promotion Association. The sticker/certificate should have a serial number.' }
          ]
        }
      ],

      mapPins: [
        { lat: 34.6362, lng: 135.0869, label: 'Kobe Premium Outlets (Marine Pia)', num: 1, cat: 'shopping', desc: '200+ designer and outlet stores by the bay' },
        { lat: 34.6739, lng: 135.1827, label: 'Kobe Harborland / Mosaic', num: 2, cat: 'attraction', desc: 'Waterfront shopping and harbor views' },
        { lat: 34.6892, lng: 135.1883, label: 'Nankinmachi Chinatown', num: 3, cat: 'food', desc: 'Steamed pork buns and roast duck' },
        { lat: 34.6950, lng: 135.1954, label: 'Kobe Beef Restaurant (Sannomiya)', num: 4, cat: 'food', desc: 'A5 Kobe wagyu teppanyaki' }
      ]
    },
    {
      num: 5,
      title: 'Pokémon Cafe, Shinsaibashi & teamLab Botanical Garden',
      neighborhoods: 'Shinsaibashi · Namba · Nagai · America-mura',
      description: 'The most exclusively Osaka day on the itinerary — a Pokémon-powered morning, afternoon shopping in Japan\'s best street fashion district, and an evening bathed in living light art.',

      timeBlocks: [
        {
          label: '☕ 10:00 AM — Pokémon Cafe Osaka',
          activities: [
            {
              title: 'Pokémon Cafe Osaka (ポケモンカフェ)',
              description: 'Located inside Daimaru Shinsaibashi Department Store (6F), the Pokémon Cafe serves elaborately themed food and drinks where every dish is shaped like a Pokémon character. Each table gets a welcome from Pikachu, and the merch area stocks exclusives you can\'t find anywhere else. Reservations are mandatory and notoriously difficult to get.',
              details: [
                '📍 6F, Daimaru Shinsaibashi, 1-7-1 Shinsaibashisuji, Chuo-ku',
                '🔗 Reserve at: pokemoncafe.net (English available). Slots open ~1 month in advance.',
                '⏰ Opening: 10:00 AM. Sessions: ~70 min each. Golden Week has multiple slots per day.',
                '💰 Set meal: ~¥2,000–3,500/person (food + non-alcoholic drink). Character items extra.',
                '⚠️ CRITICAL: Reservations for Golden Week slots open around early April. If you haven\'t booked, check cancellations daily via the app — they do appear.',
                '🛍️ The merch area is accessible without a reservation — exclusive plushies, cups, tins, accessories'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: '🎮 If the cafe is fully booked, visit the Pokémon Center Osaka DX on the 6F of Daimaru Shinsaibashi — it\'s the largest Pokémon merchandise store in Kansai and no reservation needed. Hours 10 AM–8 PM.' }
          ]
        },
        {
          label: '🛍️ 12:30 PM — Shinsaibashi & America-mura',
          activities: [
            {
              title: 'Shinsaibashisuji Shopping Arcade',
              description: 'Japan\'s most famous covered shopping arcade stretches 600 meters and features everything from fast fashion to luxury brands, including a flagship Zara, Uniqlo, H&M, and dozens of Japanese-only brands you can\'t find at home. The covered arcade means weather is never an issue.',
              details: [
                '📍 Shinsaibashisuji 1–2 chome (runs parallel to Midosuji boulevard)',
                '⏰ Most shops: 11:00 AM – 9:00 PM',
                '⏱️ Allow 1 hour for the full arcade sweep'
              ]
            },
            {
              title: 'America-mura (アメリカ村)',
              description: 'Osaka\'s version of Harajuku — a labyrinth of vintage clothing shops, sneaker stores, streetwear boutiques, and tattoo parlors packed into a few tight Nishi-Shinsaibashi blocks. The energy is young, loud, and creative. Triangle Park in the center is a prime people-watching spot.',
              details: [
                '📍 Nishi-Shinsaibashi, 5 min walk west of Shinsaibashisuji arcade',
                '👟 Key finds: vintage Levi\'s, American streetwear, rare sneakers, Japanese indie brands',
                '⏱️ Allow 45–60 min to wander',
                '📸 Triangle Park: sit on the steps and watch Osaka\'s most eclectic fashion parade'
              ]
            }
          ]
        },
        {
          label: '🍜 3:00 PM — Lunch / Cafe Break in Shinsaibashi',
          meals: [
            {
              type: '🍜 LUNCH',
              name: 'Standing Ramen or Izakaya — Hozenji Yokocho Area',
              description: 'The tiny stone-paved alley of Hozenji Yokocho off Dotonbori has some of Osaka\'s most atmospheric lunch spots — small izakayas and ramen shops with ivy-covered walls and moss-covered statues. Far less touristy than the main Dotonbori strip.',
              meta: '📍 Behind Shochikuza theater, south of Dotonbori · 💰 ¥1,000–1,800/person'
            }
          ]
        },
        {
          label: '🌿 6:00 PM — teamLab Botanical Garden Osaka',
          activities: [
            {
              title: 'teamLab Botanical Garden Osaka (チームラボ ボタニカルガーデン 大阪)',
              description: 'One of teamLab\'s most beautiful installations — a real botanical garden transformed by night into a living light art landscape. Paths wind through illuminated flowers that respond to your presence, ponds shimmer with digital fish, and ancient trees are wrapped in flowing light patterns. Unlike teamLab\'s white-cube galleries, this one uses the natural outdoor environment as its canvas.',
              details: [
                '📍 Nagai Botanical Garden, 1-108 Nagaipark, Higashisumiyoshi-ku',
                '🚇 Subway: Midosuji Line to Nagai Station, 5-min walk to park entrance',
                '⏰ Opens at sunset (~6:30–7:00 PM), closes 10:00 PM',
                '💰 ¥3,200/adult, ¥1,600/children 4–12, free under 4',
                '🔗 Book online at: teamlab.art (sold out on Golden Week — book as soon as possible)',
                '⏱️ Allow 90–120 min to walk the full garden circuit',
                '👟 Wear walking shoes — the paths wind through the full garden grounds',
                '📸 No professional cameras with tripods; phone photos are fine and stunning'
              ]
            }
          ],
          tips: [
            { type: 'reddit', text: '"teamLab Botanical Garden is WAY better than Planets for families. The kids run ahead and trigger different light patterns — they\'re basically part of the art. Go on a weeknight if possible; weekends during Golden Week are wall-to-wall people."', cite: 'r/JapanTravel' }
          ]
        },
        {
          label: '🍽️ 9:00 PM — Fine Dining Dinner',
          meals: [
            {
              type: '⭐ DINNER',
              name: 'Zurriola (ズリオラ) — Michelin Recommended, Modern Spanish',
              description: 'Chef Honda Kazuhiro\'s modern Basque-inspired cuisine is one of Osaka\'s best-kept secrets. The 8-course tasting menu features Japanese-sourced seafood and meats prepared through contemporary Spanish technique — a unique and exciting departure from the kaiseki circuit. Reservations significantly easier than the French houses.',
              meta: '📍 Shinsaibashi area · ✉️ Book 1–2 weeks ahead · 💰 ¥15,000–20,000/person'
            },
            {
              type: '⭐ ALTERNATIVE',
              name: 'Osaka Teppanyaki (Various) — Michelin Bib Gourmand',
              description: 'After teamLab, a theatrical teppanyaki dinner is a satisfying counterpoint. Several excellent counter-style teppanyaki restaurants in the Namba/Shinsaibashi area offer premium wagyu and seafood around the grill. ¥10,000–15,000/person.',
              meta: '💰 ¥10,000–15,000/person'
            }
          ]
        }
      ],

      mapPins: [
        { lat: 34.6736, lng: 135.5009, label: 'Pokémon Cafe & Center Osaka DX', num: 1, cat: 'attraction', desc: 'Daimaru Shinsaibashi 6F — exclusive Pokémon merch + themed cafe' },
        { lat: 34.6724, lng: 135.5019, label: 'Shinsaibashisuji Arcade', num: 2, cat: 'shopping', desc: '600m covered shopping arcade — fashion and brands' },
        { lat: 34.6710, lng: 135.4988, label: 'America-mura', num: 3, cat: 'shopping', desc: 'Osaka\'s Harajuku — vintage, streetwear, sneakers' },
        { lat: 34.6186, lng: 135.5182, label: 'teamLab Botanical Garden', num: 4, cat: 'attraction', desc: 'Nagai Park night art installations — opens at sunset' }
      ]
    },
    {
      num: 6,
      title: 'Nara Day Trip — Deer, Temples & Giant Buddha',
      neighborhoods: 'Nara · Nara Park · Naramachi',
      description: 'A 45-minute train ride transforms the busy urban Osaka trip into a serene encounter with 1,200 free-roaming deer and ancient temples. Nara\'s World Heritage sites feel timeless, and kids absolutely love the deer.',

      timeBlocks: [
        {
          label: '🚂 8:30 AM — Osaka → Nara (Kintetsu Express)',
          activities: [
            {
              title: 'Getting to Nara from Osaka',
              description: 'The fastest and easiest way to Nara is the Kintetsu Railways Nara Line from Osaka Namba or Kintetsu Osaka Namba Station — 40 minutes, ¥680/person on the express (Kintetsu Nara Line Rapid Express). Buy tickets at the station.',
              details: [
                '🚂 Kintetsu Nara Line: Osaka Namba (Kintetsu) → Kintetsu Nara, 40 min, ¥680 express',
                '🚂 JR Option: JR Namba → Nara via Yamatoji Rapid, 50 min, ¥800',
                '⏱️ Plan 6 hours in Nara before heading back for dinner',
                '🦌 Get shika senbei (deer crackers, ¥200) immediately after arriving — deer will find you'
              ]
            }
          ]
        },
        {
          label: '🦌 9:30 AM — Nara Deer Park (奈良公園)',
          activities: [
            {
              title: 'Nara Deer Park',
              description: 'Over 1,200 wild sika deer roam freely through the entire park — bowing for crackers, photobombing tourists, and occasionally being cheeky about it. They\'re considered messengers of the gods (Kasuga Shrine\'s deity arrived on a white deer) and have been protected since 768 AD. This is one of Japan\'s most charming wildlife encounters.',
              details: [
                '📍 Deer roam throughout Nara Park — a 10-min walk from Kintetsu Nara Station',
                '💰 Free to enter the park. Shika senbei (deer crackers) sold everywhere: ¥200/pack',
                '🦌 Deer bow their heads when you hold crackers — they learned this from watching humans bow',
                '⚠️ Deer will aggressively approach if they see crackers. Feed one at a time, don\'t wave the bag.',
                '🏃 Young children should be supervised — deer are friendly but can push and nip for food',
                '⏱️ You\'ll spend at least 30–45 min just being surrounded by deer'
              ]
            }
          ],
          tips: [
            { type: 'reddit', text: '"The deer near Todai-ji are more aggressive because they get fed constantly. Walk toward the southern end of the park (Kasuga Shrine area) for calmer, less crowded deer interactions."', cite: 'r/JapanTravel' }
          ]
        },
        {
          label: '🛕 10:30 AM — Todai-ji (東大寺) — Great Buddha',
          activities: [
            {
              title: 'Todai-ji Temple & the Giant Daibutsu',
              description: 'The world\'s largest wooden building houses the world\'s largest bronze Buddha (Daibutsu) — 15 meters tall, cast in 752 AD. Walking through the Nandaimon gate (flanked by ferocious guardian statues from 1203 AD) and entering the dim hall to encounter the massive golden Buddha is one of Japan\'s most awe-inspiring experiences.',
              details: [
                '⏰ Hours: 7:30 AM – 5:30 PM (Nov–Feb: 8 AM – 5 PM)',
                '💰 ¥600/adult, ¥300/child (elementary)',
                '🐘 Inside the hall: a large wooden pillar with a hole at the base — legend says crawling through it gives the same merit as meditating in the Daibutsu\'s nostril. Kids love this.',
                '⏱️ Allow 45–60 min for the temple complex',
                '📸 Frame the Buddha from the far end of the hall for the full scale shot'
              ]
            }
          ]
        },
        {
          label: '⛩️ 12:00 PM — Kasuga Taisha Shrine',
          activities: [
            {
              title: 'Kasuga Taisha (春日大社) — 3,000 Lanterns',
              description: 'Founded in 768 AD, Kasuga Taisha is one of Japan\'s most sacred Shinto shrines. The forest path lined with thousands of stone lanterns is hauntingly beautiful — there are 3,000 bronze and stone lanterns throughout the shrine complex. During the February Mantoro festival they\'re all lit at once, but even unlit they create an incredible atmosphere among ancient cedars.',
              details: [
                '📍 160 Kasugano-cho, Nara — 20-min walk through Nara Park from Todai-ji',
                '⏰ Hours: 6:30 AM – 5:30 PM (Mar–Oct)',
                '💰 Free to enter grounds. Inner sanctuary (Honden): ¥500',
                '⏱️ Allow 30–45 min for the approach and shrine grounds'
              ]
            }
          ]
        },
        {
          label: '🍜 1:30 PM — Lunch in Naramachi',
          meals: [
            {
              type: '🍜 LUNCH',
              name: 'Naramachi (奈良町) — Traditional Townhouse Cafes',
              description: 'Head south of the main park area to Naramachi, Nara\'s beautifully preserved old merchant district. Machiya townhouses converted into cafes and restaurants serve Nara\'s local cuisine: kakinoha-zushi (pressed sushi wrapped in persimmon leaf), warm miso soup, and miwa somen (the region\'s famous thin noodles).',
              meta: '📍 Naramachi, Nara — south of Kofukuji · 💰 ¥1,200–2,000/person · Browse and pick what looks inviting'
            }
          ],
          tips: [
            { type: 'tip', text: '🍱 Kakinoha-zushi (persimmon leaf sushi) is Nara\'s signature food — try it from Hiraso or Yoshino Sushi. The persimmon leaf acts as both wrapper and natural preservative; the flavor is subtler than standard sushi.' }
          ]
        },
        {
          label: '🚂 3:30 PM — Return to Osaka',
          activities: [
            {
              title: 'Nara → Osaka (Kintetsu Express)',
              description: 'Head back on the Kintetsu Nara Line. Arrive at Osaka Namba by 4:30 PM — enough time to refresh at the hotel before the evening\'s fine dining reservation.',
              details: [
                '🚂 Kintetsu Nara → Osaka Namba, 40 min, ¥680',
                '⏰ Hotel check-in/refresh: ~5:00 PM',
                '⏱️ Dinner reservation 7:00–7:30 PM'
              ]
            }
          ]
        },
        {
          label: '🍽️ 7:00 PM — Fine Dining Dinner',
          meals: [
            {
              type: '⭐ DINNER',
              name: 'Kigawa (木側) — 2 Michelin Stars, Classic Kaiseki',
              description: 'One of Osaka\'s most respected kaiseki restaurants, Kigawa offers a traditional multi-course kaiseki journey that traces the Japanese culinary calendar. Chef Yoshihiro Murata\'s careful sourcing ensures every ingredient is at its seasonal peak — May kaiseki features bamboo shoots, cherry blossoms preserved in salt, and spring vegetables rarely seen outside Japan.',
              meta: '📍 Kitahama area, Chuo-ku · ✉️ Reserve 3–4 weeks ahead · 💰 ¥25,000–35,000/person'
            }
          ]
        }
      ],

      mapPins: [
        { lat: 34.6851, lng: 135.8328, label: 'Nara Deer Park', num: 1, cat: 'attraction', desc: '1,200 free-roaming sacred deer' },
        { lat: 34.6888, lng: 135.8399, label: 'Todai-ji Temple', num: 2, cat: 'attraction', desc: 'World\'s largest wooden building — 15m Bronze Buddha' },
        { lat: 34.6814, lng: 135.8448, label: 'Kasuga Taisha Shrine', num: 3, cat: 'attraction', desc: '3,000 stone lanterns through ancient cedar forest' },
        { lat: 34.6771, lng: 135.8322, label: 'Naramachi', num: 4, cat: 'food', desc: 'Traditional townhouse district — kakinoha-zushi and somen' }
      ]
    },
    {
      num: 7,
      title: 'Farewell Morning: Umeda, Kuromon & Departure',
      neighborhoods: 'Umeda · Daimaru · Namba · Kansai Airport',
      description: 'A relaxed final morning for last-minute shopping and a proper Osaka breakfast before heading to Kansai Airport.',

      timeBlocks: [
        {
          label: '🌅 8:30 AM — Morning in Umeda (梅田)',
          activities: [
            {
              title: 'Umeda Sky Building — Floating Garden Observatory',
              description: 'If your flight is afternoon/evening, start the day with a visit to the Umeda Sky Building\'s rooftop Floating Garden — a glass ring suspended between two towers at 170m. Clear May mornings give stunning views south over Osaka toward Kobe and Awaji Island.',
              details: [
                '📍 1-1-88 Oyodonaka, Kita-ku (5 min walk from JR Osaka Station North Exit)',
                '⏰ 9:30 AM – 10:30 PM',
                '💰 ¥1,500/adult',
                '⏱️ Allow 30–45 min',
                '📸 Morning light is best — by noon it gets bright and hazy'
              ]
            }
          ]
        },
        {
          label: '🛍️ 10:00 AM — Final Shopping: Daimaru/Takashimaya',
          activities: [
            {
              title: 'Department Store Final Run',
              description: 'The basement food halls (depachika) of Daimaru Umeda or Takashimaya Namba are the perfect place to stock up on carefully packaged Japanese confectionery, tea, sake, and food gifts. Everything is beautifully wrapped. These items pass customs easily and keep well.',
              details: [
                '🎁 Best omiyage (souvenirs): Juchheim Baumkuchen, Henri Charpentier madeleines, Royce chocolate (keep cool), matcha KitKats (any convenience store), Osaka takoyaki snacks',
                '💰 Budget ¥5,000–15,000 for food gift shopping',
                '⏰ Depachika opens 10 AM, food halls sometimes 10:30 AM',
                '⚠️ Buy chocolates/dairy last — they need to go in carry-on or checked bag with cooling'
              ]
            }
          ]
        },
        {
          label: '🍜 12:00 PM — Final Osaka Meal',
          meals: [
            {
              type: '🐙 LUNCH',
              name: 'Takoyaki at Wanaka or Aizuya',
              description: 'End where Osaka cooking began — with takoyaki. These crispy-outside, molten-inside octopus balls are Osaka\'s defining street food. Wanaka near Namba is consistently rated the city\'s best. A proper farewell to a city that fed you this well.',
              meta: '📍 Wanaka: 1-2-22 Namba, Chuo-ku · 💰 ¥500–600 for 8 balls · Perfect pre-airport snack'
            }
          ]
        },
        {
          label: '✈️ 2:00 PM — Head to Kansai Airport',
          activities: [
            {
              title: 'Osaka Namba → Kansai International Airport',
              description: 'Allow at least 2.5 hours before international departure. The Nankai Rapi:t express from Namba Station to KIX takes 38–45 minutes (¥1,450/person). International terminal has excellent duty-free — Japanese whisky, cosmetics, and more KitKat flavors.',
              details: [
                '🚂 Nankai Rapi:t: Namba Station (Nankai) → KIX Terminal 1, 38 min, ¥1,450',
                '🚂 JR Kansai Airport Express Haruka: Osaka/Tennoji → KIX, 45 min',
                '⏰ Arrive at airport 2–2.5 hours before departure',
                '🛒 Duty-free buys: Japanese single malt whisky (Yamazaki, Hibiki), Shiseido cosmetics, sake, premium KitKat gift sets',
                '⚠️ Don\'t pack Japanese knives in carry-on (common souvenir problem!)'
              ]
            }
          ]
        }
      ],

      mapPins: [
        { lat: 34.7025, lng: 135.4964, label: 'Umeda Sky Building', num: 1, cat: 'attraction', desc: 'Floating Garden Observatory — 170m rooftop ring' },
        { lat: 34.7026, lng: 135.4978, label: 'JR Osaka / Daimaru Umeda', num: 2, cat: 'shopping', desc: 'Final shopping — depachika food hall' },
        { lat: 34.6654, lng: 135.5012, label: 'Namba Station (Nankai)', num: 3, cat: 'transport', desc: 'Rapi:t express to Kansai Airport (38 min)' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Tickets',      item: 'USJ 1-Day Ticket (adult)',         perPerson: '¥9,400',       group4: '¥37,600' },
    { category: 'Tickets',      item: 'USJ Express Pass 7',               perPerson: '¥9,000–15,000', group4: '¥36,000–60,000' },
    { category: 'Tickets',      item: 'teamLab Botanical Garden',         perPerson: '¥3,200',       group4: '¥12,800' },
    { category: 'Tickets',      item: 'Osaka Castle Museum',              perPerson: '¥600',         group4: '¥2,400' },
    { category: 'Tickets',      item: 'Abeno Harukas 300',                perPerson: '¥2,000',       group4: '¥8,000' },
    { category: 'Tickets',      item: 'Todai-ji, Nara',                   perPerson: '¥600',         group4: '¥2,400' },
    { category: 'Food/Dining',  item: 'Pokémon Cafe set menu',            perPerson: '¥2,500',       group4: '¥10,000' },
    { category: 'Food/Dining',  item: 'Fine dining dinner (avg/night)',   perPerson: '¥20,000–30,000', group4: '¥80,000–120,000/night' },
    { category: 'Food/Dining',  item: 'Casual lunches (per day)',         perPerson: '¥1,500–2,500', group4: '¥6,000–10,000/day' },
    { category: 'Transport',    item: 'ICOCA card loading (per person)',  perPerson: '¥10,000',      group4: '¥40,000' },
    { category: 'Transport',    item: 'KIX Airport → Namba (Rapi:t)',     perPerson: '¥1,450',       group4: '¥5,800' },
    { category: 'Shopping',     item: 'Kobe Premium Outlet budget',       perPerson: 'varies',       group4: '¥50,000–150,000' },
    { category: 'TOTAL (est.)', item: 'Excluding fine dining & shopping', perPerson: '¥40,000–60,000', group4: '¥160,000–240,000' }
  ],

  practicalInfo: [
    {
      title: '🎢 USJ: Golden Week Survival Guide',
      items: [
        'Buy tickets online before you arrive in Japan — USJ sells directly at usj.co.jp/e/ (English). Day-of-park tickets often sell out during Golden Week.',
        'Express Pass 7 is MANDATORY in Golden Week. Without it, expect 60–120 min waits per ride.',
        'Harry Potter Express Pass vs. Virtual Line: Forbidden Journey uses Express Pass. Super Nintendo World uses Virtual Line (app-based queue slot). Download the USJ app before arriving.',
        'Arrive 30 min before park opening. First 20 min: run to Wizarding World, join Harry Potter queue before the main crowd enters.',
        'Kinopio\'s Cafe inside Super Nintendo World: reserve at kinopioscafe.com when your Virtual Line slot is confirmed. Very limited capacity.',
        'Character meet-and-greets with Mario, Luigi, Minions — schedules change daily, check the app on arrival morning.'
      ]
    },
    {
      title: '🌿 teamLab Botanical Garden: Booking Tips',
      items: [
        'Book at teamlab.art — select "teamLab Botanical Garden Osaka" (not Planets or Borderless).',
        'Ticket tiers: Standard ¥3,200, also weekend premium pricing during Golden Week. Book as early as possible.',
        'The garden opens at sunset — arrival time is flexible (between open and 9 PM last entry).',
        'Wear comfortable outdoor shoes — the garden paths are uneven in places.',
        'Golden Week crowds: the garden handles it better than indoor venues. Paths spread the crowd out naturally.',
        'Photography is encouraged and looks stunning. Bring a wide-angle lens if you have one — the light patterns are expansive.'
      ]
    },
    {
      title: '🍽️ Fine Dining Reservation Strategy',
      items: [
        'Book ALL restaurants before departure from home. Golden Week fills Michelin tables 2–3 months out.',
        'Use these booking platforms: Tableall (tableall.com), Tablecheck (tablecheck.com), Omakase (omakase.app) — all have English interfaces.',
        'Cancellation policy: most Michelin restaurants charge full course price for no-shows. Mark reservations in your phone calendar.',
        'Dress code: smart casual at minimum. No flip-flops or shorts at 2–3 star restaurants. Nice shoes matter.',
        'Tipping: never in Japan. Service charge is included. Saying "oishikatta desu" (it was delicious) to the chef as you leave is the appropriate appreciation.',
        'For emergency alternatives if bookings fall through: Osaka Grill Kuishinbo, Kitamura (2-star, sometimes available short notice), or the excellent Bib Gourmand restaurants in the Namba/Shinsaibashi area.'
      ]
    },
    {
      title: '🦌 Nara Practical Notes',
      items: [
        'The train timing makes Nara a perfect day 6 trip — you\'ve seen Osaka\'s highlights and are ready for a change of pace.',
        'Nara is extremely walkable — the main sites (Deer Park, Todai-ji, Kasuga Taisha) are within a 30-min walk of each other.',
        'Spring May weather in Nara: 18–25°C, comfortable walking weather. Fresh green foliage everywhere.',
        'Deer are wild. They bow for crackers but can also chase, headbutt, and steal food. Bags of crackers attract aggressive behavior from multiple deer — feed them one cracker at a time.',
        'Kofuku-ji Pagoda (free exterior view) is right in the center of town — great photo with the deer in the foreground.',
        'Nara overnight option: if you want to skip day 6 of Osaka hotels, Nara has excellent ryokan (traditional inns). Edohanamikoji and Asukasou are beautiful options.'
      ]
    },
    {
      title: '🛍️ Kobe Premium Outlet Tips',
      items: [
        'Brands with significant savings: Gucci, Prada, Burberry, Coach, Kate Spade, Armani Exchange — expect 20–40% off retail.',
        'Tax-free shopping: bring your passport, purchase ¥5,000+ at a single store. Staff will give you a tax-free counter form — process takes 5 min per store.',
        'IC Card luggage delivery (takkyubin): ship shopping bags directly to your hotel or airport from inside the outlet. Far easier than carrying bags on trains.',
        'Opening time is 10 AM — arrive early on Golden Week as the most popular stores (Gucci, Coach) run ticket systems for entry after 11 AM.',
        'Access: Marin Pia Kobe bus runs from JR Suma Station (2 stops west of Sannomiya on JR Kobe Line). Or take a taxi from Sannomiya (~¥2,500, 20 min).',
        'There\'s a food court with Kobe beef burger options inside the outlet — decent quality for a shopping-day lunch.'
      ]
    },
    {
      title: '🌸 May Golden Week Context',
      items: [
        'Golden Week = April 29 (Showa Day), May 3 (Constitution Day), May 4 (Greenery Day), May 5 (Children\'s Day). May 1–2 are regular weekdays but treated as bridge holidays by most people.',
        'Crowds peak on May 3–5. May 1–2 and May 6 are noticeably less packed.',
        'Prices: hotels and some tours charge premium Golden Week rates — often 1.5–3× normal.',
        'ATMs: every 7-Eleven and Lawson has international-card-friendly ATMs. Stock up on cash at the start of each day.',
        'Convenience stores: 7-Eleven, FamilyMart, and Lawson are genuinely good for breakfast, snacks, and late-night meals. The onigiri and sandwiches are excellent and available 24/7.',
        'If plans fall apart: Osaka is one of the world\'s great spontaneous cities. Any random alley in Namba or Shinsaibashi will have excellent, affordable food. You can\'t really have a bad meal here.'
      ]
    }
  ]
};

console.log('Order:', order.id);
console.log('Destination:', itineraryData.destination);
console.log('Days:', itineraryData.days.length);
console.log('Budget rows:', itineraryData.budgetTable.length);
console.log('Practical sections:', itineraryData.practicalInfo.length);
console.log('');
console.log('Starting fulfillment...');

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('\n✅ FULFILLMENT COMPLETE');
  console.log('Slug:', result.slug);
  console.log('URL:', result.url);
  console.log('Email sent:', result.emailSent);
} catch (err) {
  console.error('\n❌ FULFILLMENT FAILED:', err.message);
  process.exit(1);
}
