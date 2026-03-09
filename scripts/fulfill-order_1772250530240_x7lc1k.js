const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772250530240_x7lc1k',
  email: 'ell_gee@yahoo.com',
  destination: 'Almaty, Kazakhstan',
  startDate: '2026-03-04',
  endDate: '2026-03-10',
  groupSize: 2,
  requests: 'Skiing, Adventure, Cultural'
};

const itineraryData = {
  destination: 'Almaty, Kazakhstan',
  countryEmoji: '🇰🇿',
  title: 'Peaks, Plov & Powder: An Almaty Adventure',
  subtitle: '6 days of mountain skiing, Silk Road culture & Central Asian feasts for two',
  description: "Almaty sits at the foot of the snow-capped Trans-Ili Alatau mountains — a city where you can ski world-class slopes in the morning and explore Soviet-era architecture and bustling bazaars by afternoon. This itinerary blends adrenaline-pumping days at Shymbulak ski resort with deep cultural immersion: Silk Road museums, the legendary Green Bazaar, traditional bathhouses, and frozen alpine lakes. March brings crisp mountain air, reliable snow, and the first hints of spring in the city below.",
  duration: '6 nights',
  dates: 'Mar 4 – Mar 10, 2026',
  budget: '$–$$',
  pace: 'Active',
  bestFor: 'Adventure Couples',
  highlights: [
    'Two full days skiing at Shymbulak — Central Asia\'s largest resort',
    'Medeu — the world\'s highest Olympic-size ice skating rink',
    'Green Bazaar sensory overload: spices, dried fruits, horse meat',
    'Zenkov Cathedral — one of the world\'s tallest wooden buildings',
    'Frozen Big Almaty Lake at 2,500m altitude',
    'Traditional Kazakh bathhouse experience at Arasan Baths'
  ],

  essentials: [
    { title: '🏔️ March Weather', text: 'Expect -5°C to 5°C in the city, colder in the mountains (-10°C to -5°C). Snow is reliable at Shymbulak through March. Pack warm layers, a good ski jacket, and sunscreen — the mountain sun is intense at altitude.' },
    { title: '🚡 Getting to Shymbulak', text: 'Take the Medeu–Shymbulak gondola from Medeu ice rink (15 min from city center by taxi). The gondola ride itself is spectacular — rising through pine forests into the alpine zone. Day pass ~5,000 KZT (~$10).' },
    { title: '💰 Budget-Friendly', text: 'Kazakhstan is remarkably affordable. A full meal for two runs $10-20, taxis across the city $2-4 via Yandex Go, and ski passes are a fraction of European prices. The tenge (KZT) is roughly 470 to $1 USD.' },
    { title: '📱 Getting Around', text: 'Download Yandex Go (like Uber) — it\'s the primary ride-hailing app. The metro is clean and beautiful with Soviet-era mosaics, covering central routes for 120 KZT. Most attractions are walkable from the city center.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-04',
      neighborhoods: 'City Center · Panfilov Park · Dostyk Avenue',
      title: 'Arrival & First Impressions',
      description: "Land in Almaty and feel the mountain air hit your lungs. The Tien Shan peaks tower above the city skyline — a dramatic welcome. Today is about getting oriented: the historic heart of the city, the iconic cathedral, and your first taste of Kazakh hospitality.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Panfilov Park & Zenkov Cathedral',
              description: 'After checking in, walk to Panfilov Park — the green heart of Almaty. The Zenkov Cathedral (Ascension Cathedral) is a stunning wooden church built in 1907 that survived a massive earthquake. Stroll the tree-lined paths past the Eternal Flame war memorial.',
              details: [
                '⛪ Zenkov Cathedral — one of the tallest wooden buildings in the world, no nails used',
                '🎵 Museum of Folk Musical Instruments nearby — traditional dombra and kobyz',
                '🌳 The park is peaceful and photogenic, even in winter'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Late Lunch',
              name: 'Navat',
              description: 'Ornate Uzbek-Kazakh restaurant with stunning tilework interiors. Try the plov (pilaf), lagman (hand-pulled noodle soup), and fresh tandoor bread.',
              meta: '💰 $ · 📍 Dostyk Avenue · Traditional Central Asian cuisine'
            }
          ],
          tips: [
            { type: 'tip', text: 'Jet lag tip: the mountain air and cold will wake you right up. Take a brisk walk down Dostyk Avenue — Almaty\'s main boulevard lined with Soviet-era buildings and modern cafés.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Kok Tobe Hill at Sunset',
              description: 'Ride the cable car from the city center up to Kok Tobe, the highest point in Almaty. Watch the sunset paint the snow-capped mountains pink while the city lights flicker on below. There\'s a quirky Beatles statue and panoramic viewpoints.',
              details: [
                '🚡 Cable car from Dostyk Avenue — runs until 11pm',
                '📸 Best panoramic views of the city and mountains',
                '🎸 The Beatles statue is a fun photo op'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Gosti Restaurant',
              description: 'Modern Kazakh cuisine in a stylish setting. Try beshbarmak (the national dish — boiled meat with flat noodles), kumys (fermented mare\'s milk), and horse meat delicacies for the adventurous.',
              meta: '💰 $$ · 📍 City Center · Book ahead for weekend evenings'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 43.2580, lng: 76.9570, label: 'Panfilov Park', num: 1, cat: 'attraction', desc: 'Historic park with Zenkov Cathedral and war memorial' },
        { lat: 43.2575, lng: 76.9565, label: 'Zenkov Cathedral', num: 2, cat: 'attraction', desc: 'Stunning 1907 wooden cathedral — survived earthquakes' },
        { lat: 43.2350, lng: 76.9830, label: 'Kok Tobe', num: 3, cat: 'attraction', desc: 'Hilltop viewpoint with cable car and panoramic city views' },
        { lat: 43.2560, lng: 76.9500, label: 'Navat', num: 4, cat: 'food', desc: 'Ornate Uzbek-Kazakh restaurant with incredible plov' },
        { lat: 43.2480, lng: 76.9450, label: 'Gosti Restaurant', num: 5, cat: 'food', desc: 'Modern Kazakh cuisine — try the beshbarmak' }
      ]
    },
    {
      num: 2,
      date: '2026-03-05',
      neighborhoods: 'Medeu Valley · Shymbulak Ski Resort',
      title: 'First Day on the Slopes — Shymbulak',
      description: "Your first full ski day at Shymbulak, Central Asia's premier resort. The gondola ride up through pine forests is spectacular, and the slopes range from gentle groomers to challenging off-piste terrain at 3,200m. March snow conditions are typically excellent.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Medeu & Gondola to Shymbulak',
              description: 'Take a Yandex taxi to Medeu (15 min from city center), then ride the gondola up to Shymbulak at 2,260m. Rent equipment at the base — quality gear is available at very affordable prices. The views from the gondola are jaw-dropping.',
              details: [
                '🎿 Rental gear at Shymbulak base — ~$15-20/day for full setup',
                '🎫 Day pass ~$10-15 — a fraction of European/US prices',
                '🚡 Gondola runs 9am-5pm, get there by 9:30 to beat crowds'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Skiing & Snowboarding at Shymbulak',
              description: 'The resort has runs for all levels across three zones. The Talgar Pass area (3,200m) offers thrilling advanced terrain with stunning views of the Tien Shan range. Intermediates will love the long groomed runs through the pine forests.',
              details: [
                '🏔️ Top elevation: 3,200m at Talgar Pass — breathtaking views',
                '⛷️ 7 lifts, multiple runs ranging from beginner to expert',
                '☀️ March sunshine is strong at altitude — wear goggles and sunscreen'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Chalet at Shymbulak',
              description: 'Cozy slope-side restaurant at the base area. Warm up with lagman soup, shashlik (grilled meat skewers), and hot chocolate after a morning of skiing.',
              meta: '💰 $$ · 📍 Shymbulak base area · Hearty mountain food'
            }
          ],
          tips: [
            { type: 'tip', text: 'Altitude matters! Shymbulak base is at 2,260m and the top is 3,200m. Take it easy your first runs, stay hydrated, and don\'t push too hard on day one.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Medeu Ice Skating Rink',
              description: 'On the way back down, stop at Medeu — the world\'s highest Olympic-standard ice skating rink at 1,691m. Skating under the mountain twilight with the peaks glowing is unforgettable.',
              details: [
                '⛸️ Skate rental available — rink is open until 11pm',
                '🏔️ The setting is dramatic — mountains tower on all sides',
                '📸 The rink is beautifully lit at night'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Kishlak',
              description: 'Atmospheric Uzbek restaurant decorated like a traditional Central Asian courtyard. Outstanding manty (steamed dumplings), plov, and grilled meats. A local favorite.',
              meta: '💰 $ · 📍 Near Dostyk Avenue · Cozy, authentic atmosphere'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 43.1575, lng: 77.0581, label: 'Medeu Ice Rink', num: 1, cat: 'attraction', desc: 'World\'s highest Olympic skating rink at 1,691m' },
        { lat: 43.1350, lng: 77.0770, label: 'Shymbulak Ski Resort', num: 2, cat: 'attraction', desc: 'Central Asia\'s largest ski resort — slopes up to 3,200m' },
        { lat: 43.1355, lng: 77.0775, label: 'Chalet Restaurant', num: 3, cat: 'food', desc: 'Cozy slope-side dining at Shymbulak base' },
        { lat: 43.2500, lng: 76.9580, label: 'Kishlak', num: 4, cat: 'food', desc: 'Atmospheric Uzbek restaurant with incredible manty' }
      ]
    },
    {
      num: 3,
      date: '2026-03-06',
      neighborhoods: 'Green Bazaar · Arasan Baths · Central State Museum',
      title: 'Culture Day — Bazaars, Baths & History',
      description: "Rest your ski legs and dive into Almaty's cultural soul. The Green Bazaar is a sensory explosion of spices, dried fruits, and horse meat. The Arasan Baths will soak away any soreness, and the Central State Museum tells the story of the Kazakh steppe.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Green Bazaar (Zelyony Bazaar)',
              description: 'Almaty\'s legendary market is a feast for the senses. Mountains of dried apricots, walnuts, and spices. Vendors selling kurt (dried yogurt balls), horse meat sausages (kazy), and fresh tandoor bread. This is where locals shop — dive in.',
              details: [
                '🧀 Try kurt — dried salty yogurt balls, a Kazakh staple snack',
                '🍖 Kazy — horse meat sausage, a delicacy. Try it!',
                '🫖 Fresh honey, dried fruits, and nuts make great souvenirs',
                '📸 The meat hall and spice section are incredibly photogenic'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Bowler Coffee Roasters',
              description: 'Almaty\'s best specialty coffee. Excellent flat whites, pour-overs, and pastries in a minimalist, modern space. A surprising gem in Central Asia.',
              meta: '💰 $ · 📍 Near Green Bazaar · Specialty coffee'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arasan Baths',
              description: 'One of the largest bathhouses in Central Asia, operating since 1982. Choose from Russian, Finnish, or Turkish baths. The steam, cold plunge, and relaxation cycle will erase any ski soreness. A quintessential Almaty experience.',
              details: [
                '🧖 Choose Russian (banya), Finnish (sauna), or Turkish (hammam)',
                '💆 Massage and scrub services available',
                '💰 Entry ~$5-8 · Open 8am-10pm daily',
                '🧴 Bring your own towel or rent one'
              ]
            },
            {
              title: 'Central State Museum of Kazakhstan',
              description: 'A comprehensive journey through Kazakh history — from Bronze Age nomadic warriors and the Golden Man (Altyn Adam) to Soviet-era transformation and independence. The Golden Man replica alone is worth the visit.',
              details: [
                '👑 The Golden Man — iconic Scythian warrior armor, Kazakhstan\'s national symbol',
                '🏛️ Soviet-era exhibits show Almaty\'s transformation',
                '💰 Entry ~$2 · Allow 1.5-2 hours'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Alasha',
              description: 'Upscale Kazakh restaurant set in a traditional yurt-style interior. This is where you experience Kazakh hospitality at its finest — beshbarmak, kumys, and live dombra music.',
              meta: '💰 $$ · 📍 Al-Farabi Avenue · Traditional Kazakh fine dining · Book ahead'
            }
          ],
          tips: [
            { type: 'tip', text: 'Almaty\'s food scene is a crossroads of Central Asian cultures. You\'ll find Uzbek plov, Korean-Kazakh (koryo-saram) cuisine, Georgian khachapuri, and Russian borshch all within a few blocks.' }
          ]
        }
      ],
      mapPins: [
        { lat: 43.2560, lng: 76.9420, label: 'Green Bazaar', num: 1, cat: 'attraction', desc: 'Legendary market — spices, dried fruits, horse meat' },
        { lat: 43.2620, lng: 76.9400, label: 'Arasan Baths', num: 2, cat: 'attraction', desc: 'Historic Central Asian bathhouse — Russian, Finnish, Turkish' },
        { lat: 43.2380, lng: 76.9440, label: 'Central State Museum', num: 3, cat: 'attraction', desc: 'Kazakh history from Golden Man to independence' },
        { lat: 43.2570, lng: 76.9430, label: 'Bowler Coffee Roasters', num: 4, cat: 'food', desc: 'Almaty\'s best specialty coffee' },
        { lat: 43.2200, lng: 76.9260, label: 'Alasha', num: 5, cat: 'food', desc: 'Upscale traditional Kazakh dining with live music' }
      ]
    },
    {
      num: 4,
      date: '2026-03-07',
      neighborhoods: 'Shymbulak · Talgar Pass · Mountain Trails',
      title: 'Back on the Mountain — Advanced Runs & Backcountry',
      description: "Day two at Shymbulak with fresh legs and acclimatized lungs. Push into the advanced terrain at Talgar Pass, explore off-piste options, and soak in the high-altitude Tien Shan panorama. Après-ski in the mountain village wraps up a perfect powder day.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Talgar Pass Advanced Skiing',
              description: 'Head straight for the top. The Talgar Pass chairlift takes you to 3,200m where the views stretch across the entire Tien Shan range. The runs here are steeper, less groomed, and absolutely thrilling. Off-piste options abound for confident skiers.',
              details: [
                '🏔️ 3,200m summit — panoramic views into Kyrgyzstan on clear days',
                '⛷️ Steep, ungroomed terrain for advanced skiers',
                '🌨️ March often brings fresh powder overnight — check conditions at base'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Forest Runs & Exploration',
              description: 'Descend through the pine forest runs — long, sweeping turns through beautiful terrain. If snow conditions allow, try the tree runs between marked pistes for a backcountry feel without the commitment.',
              details: [
                '🌲 The forest runs are magical — quiet, beautiful, and uncrowded',
                '📸 Stop at the mid-station viewpoint for photos',
                '☕ Warm up at one of the mid-mountain cafés'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Big Chefs at Shymbulak',
              description: 'Popular slope-side restaurant with a varied menu — Turkish-inspired dishes, burgers, and warming soups. Good views of the slopes from the terrace.',
              meta: '💰 $$ · 📍 Shymbulak mid-station area'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Après-Ski & Hot Springs',
              description: 'After skiing, unwind with a hot drink at one of the base area bars. If energy allows, head back to town for a second session at Arasan Baths or try a local sauna for deep muscle recovery.',
              details: [
                '🍺 Après drinks at the base area — local Shymkent beer is solid',
                '♨️ Recovery is key — baths or sauna tonight'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Parmigiano',
              description: 'Excellent Italian restaurant in the city center. After days of Central Asian cuisine, a wood-fired pizza and a glass of Georgian wine hits differently. Popular with locals and expats.',
              meta: '💰 $$ · 📍 City Center · Great wine list'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 43.1200, lng: 77.0850, label: 'Talgar Pass (3,200m)', num: 1, cat: 'attraction', desc: 'Summit of Shymbulak — advanced skiing and Tien Shan panorama' },
        { lat: 43.1350, lng: 77.0770, label: 'Shymbulak Base', num: 2, cat: 'attraction', desc: 'Base area with rentals, restaurants, and après-ski' },
        { lat: 43.1300, lng: 77.0800, label: 'Big Chefs', num: 3, cat: 'food', desc: 'Slope-side restaurant at mid-station' },
        { lat: 43.2530, lng: 76.9500, label: 'Parmigiano', num: 4, cat: 'food', desc: 'Excellent Italian restaurant — wood-fired pizza and wine' }
      ]
    },
    {
      num: 5,
      date: '2026-03-08',
      neighborhoods: 'Big Almaty Lake · Almaty Museum of Arts · Arbat Street',
      title: 'Frozen Lake, Art & the City',
      description: "A day of contrasts: morning adventure to Big Almaty Lake — a frozen turquoise gem at 2,500m surrounded by peaks — followed by afternoon art and culture in the city. The lake is one of Kazakhstan's most spectacular natural sights.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Big Almaty Lake',
              description: 'Hire a 4x4 taxi or join a tour to Big Almaty Lake, about 30 minutes from the city. In March, the lake is frozen and surrounded by snow-covered peaks — an otherworldly landscape at 2,511m. The drive up through the gorge is half the adventure.',
              details: [
                '🏔️ Altitude: 2,511m — dress warmly, it\'s significantly colder than the city',
                '🚗 4x4 required in winter — arrange through your hotel or Yandex',
                '📸 The frozen turquoise lake against snow peaks is iconic Kazakhstan',
                '⏰ Go early morning for the best light and fewer people'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The road to Big Almaty Lake can be icy in March. Use a reputable driver with a proper 4x4. The trip takes about 1.5 hours round trip plus time at the lake.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Almaty Museum of Arts',
              description: 'A sleek contemporary art space showcasing Kazakh and Central Asian art. The permanent collection spans traditional nomadic art to Soviet-era propaganda posters to contemporary installations. A window into Kazakhstan\'s cultural evolution.',
              details: [
                '🖼️ Mix of traditional, Soviet, and contemporary Kazakh art',
                '🏛️ The building itself is architecturally interesting',
                '💰 Entry ~$2-3 · Allow 1-1.5 hours'
              ]
            },
            {
              title: 'Arbat Street (Zhibek Zholy)',
              description: 'Almaty\'s pedestrian boulevard — street performers, cafés, souvenir shops, and people-watching. Named after Moscow\'s famous Arbat, this is where Almaty comes to stroll and socialize.',
              details: [
                '🚶 Pedestrian-only — great for an afternoon stroll',
                '🛍️ Pick up Kazakh souvenirs: felt crafts, traditional textiles, miniature yurts',
                '☕ Plenty of cafés for people-watching'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Tyubeteika',
              description: 'Casual, popular chain serving excellent Uzbek and Kazakh staples at great prices. The samsa (baked meat pastries) are legendary. A perfect quick lunch.',
              meta: '💰 $ · 📍 Multiple locations · Fast, delicious, authentic'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Vista Restaurant — The Ritz-Carlton Almaty',
              description: 'Almaty\'s finest dining experience with panoramic mountain views from the upper floors. International cuisine with Kazakh touches, an excellent wine list, and impeccable service. A splurge-worthy farewell-eve dinner.',
              meta: '💰 $$$ · 📍 The Ritz-Carlton Almaty · Book ahead · Smart casual'
            }
          ],
          tips: [
            { type: 'tip', text: 'Request a window table at Vista for sunset — watching the mountains turn pink while dining is unforgettable.' }
          ]
        }
      ],
      mapPins: [
        { lat: 43.0500, lng: 76.9830, label: 'Big Almaty Lake', num: 1, cat: 'attraction', desc: 'Frozen turquoise alpine lake at 2,511m — stunning' },
        { lat: 43.2400, lng: 76.9350, label: 'Almaty Museum of Arts', num: 2, cat: 'attraction', desc: 'Contemporary art space with Kazakh and Central Asian works' },
        { lat: 43.2570, lng: 76.9450, label: 'Arbat Street (Zhibek Zholy)', num: 3, cat: 'attraction', desc: 'Pedestrian boulevard with cafés and street performers' },
        { lat: 43.2550, lng: 76.9460, label: 'Tyubeteika', num: 4, cat: 'food', desc: 'Popular Uzbek-Kazakh casual dining — great samsa' },
        { lat: 43.2380, lng: 76.9570, label: 'Vista Restaurant', num: 5, cat: 'food', desc: 'Ritz-Carlton fine dining with mountain panorama' }
      ]
    },
    {
      num: 6,
      date: '2026-03-09',
      neighborhoods: 'First President\'s Park · Dostyk Avenue · City Center',
      title: 'Last Day — Mountains, Markets & Farewell Feast',
      description: "Your final full day. One last mountain morning — whether it's a half-day of skiing, a hike, or simply riding the gondola for the views. Afternoon for last-minute souvenir shopping and a farewell dinner celebrating the best of Kazakh cuisine.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Morning Gondola & Last Ski Runs',
              description: 'Head up to Shymbulak one final time. Even if you\'re skied out, the gondola ride is worth it for the views. Get a few last runs in, or simply sit at a mountain café with hot chocolate and take in the Tien Shan panorama one last time.',
              details: [
                '⛷️ Half-day pass available if you want just a morning session',
                '📸 Last chance for mountain photos — the light is beautiful in the morning',
                '☕ Savor a final mountain hot chocolate at Chalet'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'First President\'s Park & Souvenir Shopping',
              description: 'Visit the manicured First President\'s Park for mountain views and fountains, then hit Dostyk Avenue for last-minute shopping. Pick up Kazakh chocolate (Rakhat brand), traditional felt goods, or a miniature yurt.',
              details: [
                '🏛️ First President\'s Park — grand Soviet-scale landscaping with mountain backdrop',
                '🛍️ Dostyk Avenue — Almaty\'s main shopping boulevard',
                '🍫 Rakhat chocolate factory shop — local institution since 1942'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Del Papa',
              description: 'Popular Georgian-Italian fusion restaurant with a great terrace. Try the khachapuri (Georgian cheese bread) and khinkali (soup dumplings) — the Georgian food in Almaty is outstanding.',
              meta: '💰 $$ · 📍 Dostyk Avenue · Georgian-Italian fusion'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Farewell Evening Walk',
              description: 'Take a final evening stroll through illuminated Panfilov Park. The Zenkov Cathedral glows beautifully at night, and the park is peaceful and atmospheric. A perfect moment to reflect on a week of mountains and culture.',
              details: [
                '🌃 The cathedral is lit up at night — stunning',
                '🌟 The park is safe and lovely for an evening walk'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Zheti Kazyna',
              description: 'Grand farewell feast at one of Almaty\'s finest traditional restaurants. Seven treasures of Kazakh cuisine — beshbarmak, kazy, baursak (fried bread), manty, and more. Live dombra music and genuine Kazakh hospitality.',
              meta: '💰 $$ · 📍 City Center · Traditional Kazakh banquet · Book ahead'
            }
          ],
          tips: [
            { type: 'tip', text: 'The Kazakh word for "bon appétit" is "tамақ дәмді болсын" (tamaq dämdi bolsyn). Your hosts will love hearing you try it!' }
          ]
        }
      ],
      mapPins: [
        { lat: 43.1350, lng: 77.0770, label: 'Shymbulak (Final Session)', num: 1, cat: 'attraction', desc: 'One last morning on the mountain' },
        { lat: 43.2180, lng: 76.9290, label: 'First President\'s Park', num: 2, cat: 'attraction', desc: 'Manicured park with mountain views and fountains' },
        { lat: 43.2500, lng: 76.9550, label: 'Dostyk Avenue', num: 3, cat: 'attraction', desc: 'Main boulevard — shopping and cafés' },
        { lat: 43.2510, lng: 76.9540, label: 'Del Papa', num: 4, cat: 'food', desc: 'Georgian-Italian fusion — great khachapuri' },
        { lat: 43.2560, lng: 76.9480, label: 'Zheti Kazyna', num: 5, cat: 'food', desc: 'Grand Kazakh farewell feast with live music' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$30–60/night', midrange: '$60–120/night', luxury: '$120–250/night' },
    { category: 'Meals (per couple)', budget: '$15–25/day', midrange: '$30–60/day', luxury: '$80–150/day' },
    { category: 'Transport', budget: '$5–10/day', midrange: '$10–25/day', luxury: '$30–60/day (private)' },
    { category: 'Ski Pass + Rental', budget: '$20–30/day', midrange: '$30–50/day', luxury: '$50–80/day' },
    { category: 'Activities', budget: '$5–15/day', midrange: '$15–40/day', luxury: '$40–100/day' },
    { category: '6-Day Total (couple)', budget: '$600–1,000', midrange: '$1,200–2,500', luxury: '$3,000–5,500' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Almaty International Airport (ALA) is 25 min from city center', 'Direct flights from Istanbul, Dubai, Seoul, Bangkok', 'Yandex Go taxi from airport costs ~$5-8', 'Most nationalities get visa-free entry for 30 days'] },
    { title: '🏨 Where to Stay', items: ['The Ritz-Carlton Almaty — luxury with mountain views', 'Rahat Palace Hotel — central, reliable, great value', 'Dostyk Hotel — budget-friendly, walkable to everything', 'Stay near Dostyk Ave or Panfilov Park for best access'] },
    { title: '🌡️ Weather', items: ['March averages -2°C to 8°C in the city', 'Mountains are -10°C to -5°C — proper ski gear essential', 'Sunny days are common — sunglasses and sunscreen a must', 'Snow reliable at Shymbulak through late March'] },
    { title: '💳 Money', items: ['Currency: Kazakhstani Tenge (KZT), ~470 per $1 USD', 'Card payments widely accepted in the city', 'Bazaars and small shops prefer cash', 'ATMs are everywhere — Kaspi Bank ATMs are most reliable'] },
    { title: '📱 Connectivity', items: ['Buy a local SIM at the airport — Beeline or Kcell', 'Data is very cheap (~$5 for 10GB)', 'WiFi available at most cafés and hotels', 'Download Yandex Go and 2GIS (offline maps) before arrival'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
