const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1773128916505_s8eles',
  email: 'galaxycats510@gmail.com',
  customerName: null,
  startDate: '2026-03-21'
};

const itineraryData = {
  destination: 'Sapporo, Hokkaido, Japan',
  countryEmoji: '🇯🇵',
  title: 'Sapporo: Snowy Sanctuaries & Steaming Springs',
  subtitle: 'Architectural wonders, hidden shrines, chocolate dreams & hot spring bliss — 2 days from your Sapporo base',
  description: 'A carefully timed 2-day journey through Sapporo\'s most extraordinary attractions. From Tadao Ando\'s breathtaking Hill of the Buddha to the atmospheric torii gates of Sapporo\'s own Fushimi Inari, the sweet indulgence of Shiroi Koibito Park, and the restorative waters of Jōzankei Onsen — all as day trips from central Sapporo. Late March means lingering snow, crisp mountain air, and the first whispers of spring in Hokkaido.',
  duration: '2 days',
  dates: 'March 21–23, 2026',
  budget: 'Surprise me',
  pace: 'Moderate — packed but balanced with relaxation',
  bestFor: 'Adventure · Cultural · Relaxation',
  highlights: [
    'Tadao Ando\'s Hill of the Buddha at Makomanai Takino Cemetery',
    'Sapporo\'s own Fushimi Inari Shrine with 27 vermilion torii gates',
    'Shiroi Koibito Park — Hokkaido\'s famous chocolate factory',
    'Jōzankei Onsen — hot spring town in a snowy gorge',
    'Honest take on Shirahige Waterfall (in Biei, 2.5h away)',
    'Detailed timings for every stop'
  ],

  essentials: [
    {
      title: '🌡️ Weather',
      text: 'Late March in Sapporo: expect -2°C to 5°C. Snow still covers the ground, especially at higher elevations and Jōzankei. Roads may be icy. Dress in warm layers — thermal base layer, fleece, waterproof outer shell, insulated boots with grip. Bring hand warmers.'
    },
    {
      title: '🚗 Getting Around',
      text: 'For a group of 3-4 visiting spread-out attractions, renting a car is strongly recommended (¥5,000-8,000/day from Sapporo Station area). Alternatively, taxis work but add up fast (~¥5,000-8,000 each way to Takino Cemetery). Sapporo subway covers central areas but not the attractions on this itinerary.'
    },
    {
      title: '⚠️ Shirahige Waterfall Note',
      text: 'Shirahige Waterfall (白ひげの滝) is located in Biei, approximately 2.5-3 hours from Sapporo by car. With only 2 days and so many great spots closer to Sapporo, we\'ve included it as a "bonus option" with logistics rather than squeezing it into the main itinerary. If you want to visit, consider extending your trip by a day or swapping it for Jōzankei Onsen on Day 2.'
    },
    {
      title: '💴 Budget Quick Guide',
      text: 'Shiroi Koibito Park: ¥800 admission. Makomanai Takino Cemetery: free entry. Fushimi Inari Shrine: free. Jōzankei Onsen day bath: ¥980-2,500 depending on facility. Car rental: ~¥6,000-8,000/day. Meals: ¥800-2,000 per person per meal for casual dining.'
    },
    {
      title: '📱 Useful Apps',
      text: 'Google Maps works well for driving in Hokkaido. Download offline maps in advance. For transit: use Navitime or Japan Transit Planner. Most attractions accept cash (carry ¥10,000-20,000/day per person). IC cards (Kitaca/Suica) work on Sapporo subway and some buses.'
    }
  ],

  days: [
    {
      num: 1,
      title: 'Hill of the Buddha, Fushimi Inari & Shiroi Koibito Park',
      neighborhoods: 'Takino · Fushimi · Miyanosawa',
      description: 'A full day covering three of your must-sees, starting with the iconic Tadao Ando-designed Buddha, through atmospheric shrine gates, ending with chocolate indulgence.',

      timeBlocks: [
        {
          label: '🌅 8:30 AM — Depart Sapporo',
          activities: [
            {
              title: 'Drive to Makomanai Takino Cemetery',
              description: 'Head south from central Sapporo toward Takino. The drive takes approximately 40-50 minutes via Route 453 through increasingly rural scenery.',
              details: [
                '📍 Drive time: ~40-50 min from central Sapporo',
                '🅿️ Free parking available at the cemetery — follow signs to "Hill of the Buddha" lot',
                '🧥 It\'s colder here than the city center — bundle up'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Arrive by 9:30 AM to have the Buddha largely to yourself. Tour buses typically arrive after 10:30 AM.' }
          ]
        },
        {
          label: '🗿 9:30 AM — Makomanai Takino Cemetery (真駒内滝野霊園)',
          activities: [
            {
              title: 'Hill of the Buddha (頭大仏)',
              description: 'Tadao Ando\'s masterpiece: a 13.5-meter tall Buddha statue enclosed within a concrete rotunda, crowned by a hill of lavender (snow-covered in March). You approach through a 40-meter tunnel that opens dramatically to the seated Buddha. One of Hokkaido\'s most surreal and moving architectural experiences.',
              details: [
                '⏰ Winter hours (Nov-Mar): 10:00 AM - 3:00 PM — arrive early!',
                '💰 Free admission to the cemetery grounds',
                '⏱️ Allow 60-90 minutes to explore',
                '📸 Photography permitted — the tunnel approach is the iconic shot',
                '🗿 Don\'t miss the 33 Moai statues (6.5m tall!) and Stonehenge replica near the entrance',
                '☕ Café at the Rotunda offers lavender soft-serve (winter: vanilla only)'
              ]
            }
          ],
          tips: [
            { type: 'reddit', text: '"Snow accumulates on the Buddha\'s head in winter. What remains hidden from view sparks the creativity." — Tadao Ando himself, on why the Buddha is partially hidden', cite: 'Japan Travel article' },
            { type: 'tip', text: '🚶 The path to the Buddha can be slippery with snow/ice in March. Wear boots with good grip.' }
          ]
        },
        {
          label: '🍜 11:30 AM — Lunch near Makomanai',
          meals: [
            {
              type: '🍜 LUNCH',
              name: 'Restaurant Moai (inside Takino Cemetery)',
              description: 'Surprisingly good restaurant right on the cemetery grounds with views of the Moai statues. Serves ramen, curry, udon, and seasonal set meals (teishoku).',
              meta: '💰 ¥800-1,200 per person · No reservations · Cash preferred'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 If you prefer more options, head to Makomanai Station area (20 min drive) for several ramen shops.' }
          ]
        },
        {
          label: '⛩️ 12:30 PM — Drive to Sapporo Fushimi Inari Shrine',
          activities: [
            {
              title: 'Sapporo Fushimi Inari Shrine (伏見稲荷神社)',
              description: 'Sapporo\'s own Fushimi Inari — not the Kyoto one, but a charming smaller shrine in the forested hills south of the city. A line of 27 bright vermilion torii gates leads up a hillside, gorgeous against the late-winter snow. Much less crowded than its Kyoto counterpart.',
              details: [
                '📍 Address: 2-2-17 Fushimi, Chuo-ku, Sapporo',
                '⏰ Hours: 9:00 AM - 4:00 PM (shrine office)',
                '💰 Free admission',
                '🚗 Drive time from Takino: ~30 min | From central Sapporo: ~15 min by car or taxi',
                '🚌 By transit: 20-min walk from Ropeway Iriguchi tram stop',
                '⏱️ Allow 30-45 minutes to walk the torii gates and explore',
                '📸 Best photos: looking up through the snow-dusted red gates'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: '⚠️ The steps can be icy in March. Take it slow going up and coming down the torii path.' }
          ]
        },
        {
          label: '🍫 2:00 PM — Shiroi Koibito Park (白い恋人パーク)',
          activities: [
            {
              title: 'Shiroi Koibito Park',
              description: 'Hokkaido\'s beloved chocolate theme park by Ishiya, makers of the famous Shiroi Koibito cookies (white chocolate sandwiched between butter cookies). Tour the factory, watch cookies being made through observation windows, and even make your own.',
              details: [
                '📍 Address: 2-11-36 Miyanosawa 2-jo, Nishi-ku, Sapporo',
                '⏰ Hours: 10:00 AM - 5:30 PM (last entry 4:30 PM)',
                '💰 Paid area: ¥800/person | Free area: shop, café, garden',
                '🚗 Drive from Fushimi Inari: ~25 min',
                '🚇 By transit: Miyanosawa Station (Tozai Line), 10-min walk',
                '⏱️ Allow 1.5-2 hours to explore',
                '🍪 Cookie-making workshop: ¥1,500 (book in advance recommended)',
                '🛍️ The shop has exclusive Shiroi Koibito flavors not sold elsewhere'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: '🎁 The park\'s exterior is a Tudor-style European building with an ornate clock tower — it puts on a mechanical show every hour. Time your visit to catch it!' },
            { type: 'reddit', text: '"Don\'t skip the chocolate drink at the café. It\'s made with real Ishiya chocolate and it\'s ridiculously good."', cite: 'r/JapanTravel' }
          ]
        },
        {
          label: '🍺 4:30 PM — Return to Central Sapporo',
          activities: [
            {
              title: 'Susukino & Tanukikoji Evening',
              description: 'Head back to central Sapporo for an evening exploring the entertainment district. Susukino is Hokkaido\'s biggest nightlife area, and adjacent Tanukikoji is a covered shopping arcade stretching 7 blocks.',
              details: [
                '🚗 Drive time from Shiroi Koibito Park: ~20 min to Susukino area',
                '🚇 Or take Tozai Line from Miyanosawa → Odori, then walk south',
                '⏱️ Spend the evening at your own pace'
              ]
            }
          ]
        },
        {
          label: '🍜 6:00 PM — Dinner in Susukino',
          meals: [
            {
              type: '🍜 DINNER',
              name: 'Ramen Yokocho (Ramen Alley)',
              description: 'An iconic Sapporo institution — a narrow alley in Susukino with 17 small ramen shops side by side, each with their own specialty. Try miso ramen, Sapporo\'s signature style.',
              meta: '📍 South 5 West 3, Chuo-ku · 💰 ¥800-1,100 per bowl · Open until late'
            },
            {
              type: '🍺 ALTERNATIVE',
              name: 'Sapporo Beer Garden (サッポロビール園)',
              description: 'If you want a bigger meal, head to the iconic Sapporo Beer Garden in the historic red-brick brewery for all-you-can-eat "Genghis Khan" (jingisukan) grilled lamb with Sapporo draft.',
              meta: '📍 Kita 7 Higashi 9 · 💰 ¥3,500-5,000 per person · Reservations recommended'
            }
          ],
          tips: [
            { type: 'tip', text: '🍺 Genghis Khan lamb + Sapporo beer is THE quintessential Hokkaido food experience. If you only do one dinner in Sapporo, make it this.' }
          ]
        }
      ],

      mapPins: [
        { lat: 42.9667, lng: 141.3558, label: 'Makomanai Takino Cemetery', num: 1, cat: 'attraction', desc: 'Hill of the Buddha by Tadao Ando' },
        { lat: 43.0361, lng: 141.3419, label: 'Sapporo Fushimi Inari Shrine', num: 2, cat: 'attraction', desc: 'Vermilion torii gates in the snow' },
        { lat: 43.0813, lng: 141.2756, label: 'Shiroi Koibito Park', num: 3, cat: 'attraction', desc: 'Chocolate factory theme park' },
        { lat: 43.0562, lng: 141.3563, label: 'Ramen Yokocho', num: 4, cat: 'food', desc: 'Iconic ramen alley in Susukino' },
        { lat: 43.0652, lng: 141.3716, label: 'Sapporo Beer Garden', num: 5, cat: 'food', desc: 'Genghis Khan lamb & beer' }
      ]
    },
    {
      num: 2,
      title: 'Jōzankei Onsen & Sapporo Snow Walk',
      neighborhoods: 'Jōzankei · Nakajima Park · Odori',
      description: 'A relaxation-focused day starting with a hot spring morning in the snowy Jōzankei gorge, followed by a leisurely afternoon exploring central Sapporo\'s winter charm.',

      timeBlocks: [
        {
          label: '🌅 8:30 AM — Drive to Jōzankei Onsen',
          activities: [
            {
              title: 'Drive to Jōzankei Onsen (定山渓温泉)',
              description: 'Head south from Sapporo into the Toyohira River gorge. The drive takes about 50-60 minutes and the scenery is spectacular — snow-covered mountains and river valleys.',
              details: [
                '🚗 Drive time: ~50-60 min from central Sapporo via Route 230',
                '🚌 Bus option: Jōzan-kei-sen bus from Sapporo Station, ~75 min, ¥800',
                '⏱️ Plan to spend 3-4 hours in Jōzankei'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: '💡 If driving, the road to Jōzankei can be snowy/icy in March. Use winter tires (all rental cars in Hokkaido come equipped) and drive cautiously.' }
          ]
        },
        {
          label: '♨️ 9:30 AM — Jōzankei Onsen',
          activities: [
            {
              title: 'Hot Spring Bathing',
              description: 'Jōzankei has been a beloved hot spring retreat since 1866. The mineral-rich sodium chloride waters are said to relieve muscle fatigue and improve circulation — perfect after a full day of sightseeing yesterday. Multiple ryokan and bath houses offer day-use bathing.',
              details: [
                '♨️ Top day-bath picks:',
                '• Jōzankei View Hotel Annex (¥1,000-2,500) — mega spa resort, 16 floors, panoramic views',
                '• Nukumori no Yado Furukawa (¥1,500) — traditional inn with outdoor rotenburo',
                '• Hatagoya Jōzankei Shōten (¥980) — budget-friendly, modern, stylish. Age 13+ only',
                '• Jōzankei Tsuruga Resort Spa Mori no Uta (¥3,900 incl meal) — forest-inspired luxury',
                '⏰ Day bathing hours: typically 10:00 AM - 3:00 PM (varies by facility)',
                '🧖 Bring your own towel or rent one (¥200-300)',
                '⚠️ Tattoo policy: Most traditional baths prohibit tattoos. Hatagoya Shōten is more relaxed'
              ]
            },
            {
              title: 'Jōzankei Onsen Town Walk',
              description: 'Between soaks, explore the charming onsen town. Look for the kappa (water sprite) statues scattered throughout — there are over 20 hiding along the river. Free foot baths (ashiyu) are available at several spots along the main street.',
              details: [
                '🦎 Kappa Trail: follow the riverside path to spot all 20+ kappa statues',
                '♨️ Free foot baths: try the one near Futami Suspension Bridge',
                '🌉 Futami Suspension Bridge: great viewpoint over the snowy gorge',
                '⏱️ Town walk: 30-60 minutes'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: '♨️ Onsen etiquette: Wash thoroughly before entering the bath. No swimsuits. Tie up long hair. Small towel stays out of the water.' },
            { type: 'reddit', text: '"Jōzankei in winter is magical. Snow falling while you\'re in the outdoor bath is one of those \'only in Japan\' moments."', cite: 'r/JapanTravel' }
          ]
        },
        {
          label: '🍜 12:30 PM — Lunch in Jōzankei',
          meals: [
            {
              type: '🍜 LUNCH',
              name: 'Onsen Street Restaurants',
              description: 'Several restaurants along the main road serve Hokkaido comfort food. Try the local specialty: Indian curry at Onsen Shokudo, or warm soba noodles at any of the small eateries near the bus terminal.',
              meta: '💰 ¥900-1,500 per person · Cash preferred'
            }
          ],
          tips: [
            { type: 'tip', text: '🍡 Pick up onsen manju (steamed buns) from the shops near the bridge — a classic onsen town snack.' }
          ]
        },
        {
          label: '🚗 1:30 PM — Return to Sapporo',
          activities: [
            {
              title: 'Drive Back & Afternoon in Central Sapporo',
              description: 'Head back to the city for a relaxed afternoon exploring the sights you haven\'t covered yet.',
              details: [
                '🚗 Drive time: ~50-60 min back to central Sapporo',
                '⏱️ Arrive around 2:30 PM — plenty of time for afternoon exploring'
              ]
            }
          ]
        },
        {
          label: '🏛️ 3:00 PM — Odori Park & Sapporo TV Tower',
          activities: [
            {
              title: 'Odori Park & TV Tower',
              description: 'The heart of Sapporo — a 1.5km-long park cutting through the city center. In late March, it may still have remnants of snow sculptures from the winter season. Climb Sapporo TV Tower for a panoramic view of the city and surrounding mountains.',
              details: [
                '📍 TV Tower: Odori Nishi 1-chome, Chuo-ku',
                '⏰ TV Tower hours: 9:00 AM - 10:00 PM',
                '💰 TV Tower observation deck: ¥1,000',
                '⏱️ Allow 30-45 minutes for the tower + park stroll'
              ]
            },
            {
              title: 'Tanukikoji Shopping Arcade',
              description: 'A covered shopping street stretching nearly 1 km. Browse local crafts, Hokkaido sweets, and quirky shops. Great for picking up souvenirs.',
              details: [
                '📍 Between South 2 and South 3, parallel to Odori Park',
                '⏰ Most shops: 10:00 AM - 7:00 PM',
                '🛍️ Look for: Rokkatei sweets, Royce chocolate, local crafts',
                '⏱️ Allow 30-60 minutes'
              ]
            }
          ]
        },
        {
          label: '🦀 5:30 PM — Farewell Dinner',
          meals: [
            {
              type: '🦀 DINNER',
              name: 'Nijo Market (二条市場) Fresh Seafood',
              description: 'Sapporo\'s central fish market — smaller and more intimate than Tsukiji. Grab a seat at one of the small stalls for incredibly fresh uni (sea urchin), crab, salmon, and ikura (salmon roe) donburi bowls.',
              meta: '📍 Minami 3 Higashi 1, Chuo-ku · 💰 ¥1,500-3,500 · Open 7:00 AM - 6:00 PM (some stalls to 8 PM)'
            },
            {
              type: '🍜 ALTERNATIVE',
              name: 'Soup Curry in Sapporo',
              description: 'Sapporo invented soup curry — a thin, spiced curry broth loaded with large vegetables and tender chicken. Try Suage+ or Garaku, two of the city\'s most popular soup curry spots.',
              meta: '💰 ¥1,200-1,800 per person · Garaku can have 1hr+ waits — go early'
            }
          ],
          tips: [
            { type: 'tip', text: '🦀 Sapporo has three must-eat foods: miso ramen (Day 1 ✅), jingisukan lamb, and fresh seafood. Don\'t leave without trying all three!' }
          ]
        },
        {
          label: '🌙 Evening — Bonus: Night View',
          activities: [
            {
              title: 'Mt. Moiwa Ropeway Night View',
              description: 'If you still have energy, catch the famous Sapporo night view from Mt. Moiwa — rated one of Japan\'s "New Three Major Night Views." The city lights stretch to the horizon.',
              details: [
                '📍 Moiwayama, Chuo-ku, Sapporo',
                '⏰ Ropeway hours: until 10:00 PM (winter)',
                '💰 Round trip: ¥2,100 (ropeway + mini cable car)',
                '🚗 From central Sapporo: ~15 min drive to ropeway base'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: '🌃 The night view is best on clear nights. Check weather before heading up — cloudy nights mean zero visibility.' }
          ]
        }
      ],

      mapPins: [
        { lat: 42.9694, lng: 141.1661, label: 'Jōzankei Onsen', num: 1, cat: 'attraction', desc: 'Historic hot spring town in snowy gorge' },
        { lat: 42.9672, lng: 141.1647, label: 'Futami Suspension Bridge', num: 2, cat: 'attraction', desc: 'Scenic bridge with gorge views & foot bath' },
        { lat: 43.0610, lng: 141.3567, label: 'Odori Park & TV Tower', num: 3, cat: 'attraction', desc: 'City center park with panoramic tower' },
        { lat: 43.0582, lng: 141.3538, label: 'Tanukikoji Shopping Arcade', num: 4, cat: 'shopping', desc: 'Covered shopping street for souvenirs' },
        { lat: 43.0597, lng: 141.3604, label: 'Nijo Market', num: 5, cat: 'food', desc: 'Fresh seafood market — uni & crab donburi' },
        { lat: 43.0230, lng: 141.3355, label: 'Mt. Moiwa Ropeway', num: 6, cat: 'attraction', desc: 'Famous night view spot' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Attraction',   item: 'Shiroi Koibito Park',          perPerson: '¥800',    group4: '¥3,200' },
    { category: 'Attraction',   item: 'Sapporo TV Tower',             perPerson: '¥1,000',  group4: '¥4,000' },
    { category: 'Attraction',   item: 'Mt. Moiwa Ropeway',            perPerson: '¥2,100',  group4: '¥8,400' },
    { category: 'Onsen',        item: 'Jōzankei Day Bath',            perPerson: '¥1,000-2,500', group4: '¥4,000-10,000' },
    { category: 'Transport',    item: 'Car Rental (2 days)',           perPerson: '—',       group4: '¥12,000-16,000' },
    { category: 'Transport',    item: 'Fuel (2 days)',                 perPerson: '—',       group4: '¥3,000-4,000' },
    { category: 'Food',         item: 'Day 1 Meals (casual)',          perPerson: '¥3,000-5,000', group4: '¥12,000-20,000' },
    { category: 'Food',         item: 'Day 2 Meals (casual)',          perPerson: '¥3,000-5,000', group4: '¥12,000-20,000' },
    { category: 'TOTAL (est.)', item: 'Per person for 2 days',         perPerson: '¥12,000-18,000', group4: '¥50,000-75,000' }
  ],

  practicalInfo: [
    {
      title: '🏔️ Bonus: Shirahige Waterfall Day Trip',
      items: [
        'Shirahige Falls (白ひげの滝) is in Biei, about 2.5-3 hours from Sapporo by car',
        'It\'s a 30-meter waterfall flowing into the stunning blue Biei River — gorgeous in winter with ice formations',
        'Nearby: Shirogane Blue Pond (青い池) is just 3.4 km away — equally beautiful frozen in winter',
        'If you want to visit: leave Sapporo by 7:00 AM, arrive ~10:00 AM, combine with Blue Pond, return by 3-4 PM',
        'This would replace either Day 1 or Day 2 of this itinerary — it\'s a full-day commitment',
        'Route: Sapporo → Asahikawa Expressway → Route 966 to Biei/Shirogane area',
        'The waterfall is viewable from a bridge (Shirahige no Taki Bashi) — no hiking needed',
        'Winter driving on this route requires confidence with snowy roads'
      ]
    },
    {
      title: '🚗 Car Rental Tips',
      items: [
        'Major rental companies near Sapporo Station: Toyota Rent-a-Car, Nippon Rent-a-Car, Times Car Rental',
        'Book in advance — winter season can sell out. English booking available via ToCoo or Klook',
        'All winter rentals include studless snow tires standard in Hokkaido',
        'Get the basic insurance package (about ¥1,000-1,500/day extra)',
        'An International Driving Permit (IDP) is required for most foreign licenses',
        'Roads to Jōzankei and Takino Cemetery are well-maintained but bring sunglasses — snow glare is real'
      ]
    },
    {
      title: '🚌 Without a Car',
      items: [
        'Makomanai Takino Cemetery: Take Namboku subway to Makomanai Station, then taxi (~¥3,000, 20 min) or seasonal bus (check operation dates)',
        'Fushimi Inari: Streetcar to Ropeway Iriguchi stop, then 20-min uphill walk',
        'Shiroi Koibito Park: Tozai subway to Miyanosawa Station, 10-min walk',
        'Jōzankei Onsen: Jōzan-kei-sen bus from Sapporo Station Bus Terminal, 75 min, ¥800 each way',
        'Central Sapporo (Odori, Susukino, Nijo Market): all walkable from most hotels'
      ]
    },
    {
      title: '🍜 Sapporo Food Guide',
      items: [
        'Miso Ramen: Sapporo\'s signature dish. Top spots: Sumire, Ramen Shingen, or Ramen Yokocho for the classic experience',
        'Soup Curry: Invented in Sapporo. Try Suage+, Garaku, or Treasure. Spiciness is customizable (usually 1-5 scale)',
        'Jingisukan (Genghis Khan): Grilled mutton/lamb — Sapporo Beer Garden or Daruma in Susukino',
        'Seafood: Nijo Market for uni/crab donburi, or Curb Market (Jogai Shijo) near Central Wholesale Market',
        'Hokkaido Sweets: Rokkatei, LeTAO, Royce chocolate — available at Sapporo Station or Tanukikoji',
        'Convenience stores (Seicomart) carry Hokkaido-exclusive items: melon bread, Yubari melon sweets'
      ]
    },
    {
      title: '☀️ March Weather & Packing',
      items: [
        'Average temps: -2°C to 5°C. Snow on the ground. Can feel colder with wind chill.',
        'Pack: Waterproof insulated boots (non-negotiable), warm hat, gloves, scarf',
        'Layers: thermal base → fleece mid → waterproof outer shell',
        'Sunglasses for snow glare on clear days',
        'Hand warmers (kairo) available at any convenience store for ~¥100',
        'Hokkaido in late March may have occasional snowfall — check forecasts daily'
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