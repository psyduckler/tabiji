const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772171765693_5d72jl',
  email: 'mangostickyricecreations@gmail.com',
  destination: 'Đà Nẵng, Vietnam',
  startDate: '2026-03-16',
  endDate: '2026-03-27',
  groupSize: '3-4',
  style: 'Adventure, Cultural, Family-friendly',
  dining: 'Mix of everything',
  budget: 'Under $1,000',
  requests: ''
};

const itineraryData = {
  destination: 'Đà Nẵng, Vietnam',
  countryEmoji: '🇻🇳',
  title: 'Central Vietnam Uncovered: Đà Nẵng & Beyond',
  subtitle: '11 nights of beaches, ancient temples, hill-top castles & lantern-lit streets for the whole family',
  description: "Đà Nẵng sits at the heart of Vietnam's most storied stretch of coastline — golden beaches on one side, misty mountain valleys on the other, and two UNESCO World Heritage sites a short drive away. This itinerary weaves together My Khe's surf-lapped sand, the surreal Golden Bridge in the clouds at Bà Nà Hills, lantern-strewn Hội An Ancient Town, the ancient Cham towers of Mỹ Sơn, and the imperial grandeur of Huế. Family-friendly, culturally rich, and priced for smart travellers — this is Central Vietnam at its very best.",
  duration: '11 nights',
  dates: 'Mar 16 – Mar 27, 2026',
  budget: '$',
  pace: 'Moderate',
  bestFor: 'Families · Adventure seekers · Culture lovers',

  highlights: [
    'Walk the Golden Bridge held by giant stone hands at Bà Nà Hills',
    'Cycle through the lantern-lit lanes of Hội An Ancient Town',
    'Sunrise hike in the marble grottoes of Ngũ Hành Sơn',
    'Watch Dragon Bridge breathe fire and spray water on weekend nights',
    'Boat the Thu Bồn River to Mỹ Sơn — 1,500-year-old Cham temples',
    'Day trip to Huế — Imperial Citadel and Thien Mu Pagoda'
  ],

  essentials: [
    { title: '🌤️ March Weather', text: 'March sits in Đà Nẵng\'s dry season — expect 25–30°C, mostly sunny skies, and low humidity. Perfect beach and sightseeing weather. Bà Nà Hills can be cooler (~18°C) and misty, so bring a light layer.' },
    { title: '🛵 Getting Around', text: 'Grab (Vietnam\'s Uber) is cheap and reliable for city rides. For day trips, book a private car or join a small-group tour — usually $20–40 per vehicle. Cycling in Hội An is easy and highly recommended.' },
    { title: '💵 Budget Tips', text: 'Street food meals cost $1–3. Sit-down local restaurants run $4–8 per person. Big day-trip attractions like Bà Nà Hills cost ~$38/adult entry. Budget accommodation starts around $25–50/night for a good family room.' },
    { title: '👨‍👩‍👧 Family Notes', text: 'Bà Nà Hills has rides, a fantasy castle, and plenty for kids. Hội An lantern-releasing on the river is magical for all ages. Beaches have calm conditions in March — great for swimming with kids. Book Bà Nà Hills tickets online in advance to avoid queues.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-16',
      neighborhoods: 'Đà Nẵng City Center · Han River',
      title: 'Arrival & Dragon Bridge Night Show',
      description: 'Touch down in Đà Nẵng and ease into the city with a riverside stroll, street food dinner, and the weekend Dragon Bridge fire-and-water show.',
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In & Han River Walk',
              description: 'Get settled in your hotel and take a relaxing stroll along the Han River promenade. The riverfront is lined with cafés, sculpture parks, and great views of the Dragon Bridge and Trần Thị Lý Bridge.',
              details: [
                '🏨 Stay near the Han River for central access to everything',
                '🌉 Dragon Bridge is 666m long and shaped like a dragon',
                '📸 Trần Thị Lý Bridge (the "Sail Bridge") is stunning at dusk'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dragon Bridge Fire & Water Show',
              description: 'Every Saturday and Sunday night at 9pm, the Dragon Bridge spouts fire and water as crowds gather along the riverbanks. March 16 is a Monday, but check the bridge website — special shows sometimes happen on holidays. Either way, it\'s spectacular lit up at night.',
              details: [
                '🐉 Fire/water show: Sat & Sun 9pm (check schedule for special events)',
                '📍 Best viewing from the east bank promenade',
                '🌙 The bridge is illuminated every night — beautiful even without the show'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Con Market Area Street Food',
              description: 'Đà Nẵng\'s Con Market neighborhood comes alive at night with street food stalls. Try Bún Chả Cá (fish cake noodle soup — a Đà Nẵng specialty), Bánh Tráng Cuốn Thịt Heo (rice paper rolls), and fresh spring rolls.',
              meta: '💰 $ · 📍 Con Market area, Hải Châu District'
            }
          ],
          tips: [
            { type: 'tip', text: 'Grab app works great in Đà Nẵng. Download it before you arrive — far cheaper than taxis for the family.' }
          ]
        }
      ],
      mapPins: [
        { lat: 16.0610, lng: 108.2298, label: 'Dragon Bridge', num: 1, cat: 'attraction', desc: 'Iconic fire-breathing dragon bridge over the Han River' },
        { lat: 16.0678, lng: 108.2241, label: 'Trần Thị Lý Bridge', num: 2, cat: 'attraction', desc: 'The beautiful Sail Bridge — stunning at dusk' },
        { lat: 16.0605, lng: 108.2218, label: 'Con Market', num: 3, cat: 'food', desc: 'Street food hub and local market' }
      ]
    },
    {
      num: 2,
      date: '2026-03-17',
      neighborhoods: 'My Khe Beach · Son Tra Peninsula',
      title: 'My Khe Beach & Lady Buddha on Son Tra',
      description: 'A slow beach morning on one of Asia\'s best urban beaches, then up to Son Tra Peninsula to visit the towering Lady Buddha and a quiet pagoda in the jungle.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'My Khe Beach',
              description: 'Đà Nẵng\'s My Khe Beach stretches 33km of white sand — calm, clean, and rarely crowded in March. Swim, build sandcastles, or try surfing with a local instructor. The water is warm (~25°C) and wave-free in the morning.',
              details: [
                '🏄 Surf lessons available ($10–15/hr with board)',
                '🏖️ Head to the less touristy central section for more space',
                '🧴 March UV is strong — SPF and hats essential'
              ]
            }
          ],
          meals: [
            {
              type: '🥐 Breakfast',
              name: 'Bread of Life Bakery',
              description: 'A beloved local bakery run by a social enterprise, with excellent Vietnamese sandwiches, fresh baguettes, and strong coffee.',
              meta: '💰 $ · 📍 Đỗ Quang, Ngũ Hành Sơn'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Son Tra Peninsula & Linh Ứng Pagoda',
              description: 'Drive up to Son Tra Peninsula — a jungle-covered headland jutting into the sea. Linh Ứng Pagoda is home to the 67-metre Lady Buddha statue, one of the tallest in Vietnam. Wander the grounds, enjoy sweeping views over Đà Nẵng, and spot red-shanked douc langurs in the trees.',
              details: [
                '🗿 Lady Buddha is 67m tall — visible from miles away',
                '🐒 Red-shanked douc langurs are endemic to Son Tra — look carefully in the trees',
                '🌊 Bãi Bắc Beach at the base of the peninsula is calm and uncrowded',
                '🆓 Free entry to pagoda'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Apsara Restaurant',
              description: 'Known for excellent Đà Nẵng-style Bún Chả Cá and Mi Quảng noodles. Local, casual, and very cheap.',
              meta: '💰 $ · 📍 Bạch Đằng Street, Han River area'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Madame Lân',
              description: 'A Đà Nẵng institution serving traditional Central Vietnamese cuisine in a beautiful restored house. Try the Bún Bò Huế, Mì Quảng, and the house-made Bánh Xèo crispy pancakes.',
              meta: '💰 $$ · 📍 4 Bạch Đằng, Đà Nẵng · Very popular — arrive early'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 16.0600, lng: 108.2472, label: 'My Khe Beach', num: 1, cat: 'attraction', desc: '33km of white sand — one of Asia\'s finest urban beaches' },
        { lat: 16.1027, lng: 108.2866, label: 'Linh Ứng Pagoda', num: 2, cat: 'attraction', desc: '67m Lady Buddha statue with panoramic city views' },
        { lat: 16.0755, lng: 108.2736, label: 'Son Tra Peninsula', num: 3, cat: 'attraction', desc: 'Jungle headland with douc langurs and sea views' },
        { lat: 16.0600, lng: 108.2241, label: 'Madame Lân', num: 4, cat: 'food', desc: 'Top Central Vietnamese restaurant in Đà Nẵng' }
      ]
    },
    {
      num: 3,
      date: '2026-03-18',
      neighborhoods: 'Bà Nà Hills · French Village',
      title: 'Bà Nà Hills & The Golden Bridge',
      description: 'A full day at one of Vietnam\'s most spectacular theme attractions — a French hill station in the clouds, a fantasy castle, and the famous Golden Bridge held aloft by giant stone hands.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Cable Car Up to Bà Nà Hills',
              description: 'Take the record-breaking cable car — the world\'s longest non-stop cable car — up through the clouds to Bà Nà Hills at 1,487m. The ascent is spectacular, passing through multiple climate zones. At the top, the air is cool and fresh, a welcome break from coastal heat.',
              details: [
                '🚡 Cable car: ~20 min ride, world-record length (5,042m)',
                '💰 Entry tickets ~$38/adult, $30/child (book online to avoid queues)',
                '⏰ Arrive early — opens 7:30am, crowds build fast'
              ]
            },
            {
              title: 'The Golden Bridge',
              description: 'The most photographed sight in Vietnam — a 150m pedestrian bridge held up by two enormous stone hands emerging from the mountain. The bridge sits above the clouds on clear days, offering surreal views of the forested valleys below.',
              details: [
                '📸 Go early morning for the fewest crowds and best light',
                '🌫️ Often misty in the morning — add a mystical atmosphere',
                '👶 Very accessible with young kids — flat and easy walk'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Fantasy Park & French Village',
              description: 'Bà Nà\'s Fantasy Park has rides, arcade games, wax figures, and indoor attractions — a hit with kids. The "French Village" (Làng Pháp) is a whimsical, European-style village at the top with cafés, gardens, and wine cellars built into the hillside.',
              details: [
                '🎢 Fantasy Park rides included in entry ticket',
                '🏰 Debay Wine Cellar — carved into the mountain since 1923, fascinating even for kids',
                '⛪ Linh Phong and Le Jardin D\'Amour gardens are beautiful at this altitude'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Bà Nà Hills Buffet',
              description: 'Several buffet restaurants at the top offer Vietnamese and international cuisine included with your entry ticket (check current package). Sit outdoors in the cool mountain air.',
              meta: '💰 Included or $$ · 📍 Various locations at the summit'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Cable Car Back & Riverside Rest',
              description: 'Descend by cable car as the sun begins to soften. Head back to the hotel for a rest before dinner — the kids will be happily exhausted.',
              details: [
                '🚡 Last cable car down around 5:30pm — don\'t miss it!',
                '📏 Wear comfortable shoes — you\'ll walk 5–8km at the top'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Bé Mặn Restaurant',
              description: 'Hugely popular local seafood spot with excellent grilled fish, fresh squid, and clams at very low prices. A Đà Nẵng staple.',
              meta: '💰 $$ · 📍 Lê Đình Lý Street area · Busy — arrive by 6pm'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 15.9967, lng: 107.9919, label: 'Bà Nà Hills Cable Car Station', num: 1, cat: 'attraction', desc: 'Base station for the world\'s longest non-stop cable car' },
        { lat: 15.9977, lng: 107.9892, label: 'Golden Bridge', num: 2, cat: 'attraction', desc: 'Iconic bridge held by giant stone hands — most photographed in Vietnam' },
        { lat: 15.9990, lng: 107.9875, label: 'French Village', num: 3, cat: 'attraction', desc: 'Whimsical European-style village at 1,487m altitude' },
        { lat: 16.0438, lng: 108.2085, label: 'Bé Mặn Restaurant', num: 4, cat: 'food', desc: 'Local seafood favourite — grilled fish and clams' }
      ]
    },
    {
      num: 4,
      date: '2026-03-19',
      neighborhoods: 'Ngũ Hành Sơn · Non Nuoc Beach',
      title: 'Marble Mountains & Non Nuoc Beach',
      description: 'Explore the sacred caves and pagodas carved inside five marble mountains, then relax on the quieter, more local Non Nuoc Beach in the afternoon.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Marble Mountains (Ngũ Hành Sơn)',
              description: 'Five marble-and-limestone peaks rise dramatically from the coastal plain, each named for a natural element (Metal, Wood, Water, Fire, Earth). Climb Thủy Sơn (Water Mountain) — the largest and most visited — to explore hidden cave pagodas, Confucian temples, and panoramic views of both the city and ocean.',
              details: [
                '🪨 Entry: ~30,000 VND (~$1.20) per person; elevator also available',
                '🕌 Huyền Không Cave — the largest cave, with a natural skylight streaming light onto Buddha statues',
                '⏰ Go early (8am) before tour groups arrive',
                '👟 Wear non-slip shoes — the stone steps can be steep',
                '🛍️ Non Nuoc stone-carving village is right below — great for souvenirs'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Non Nuoc Beach',
              description: 'Just steps from the Marble Mountains, Non Nuoc Beach is quieter and more local than My Khe. The water is crystal-clear and the beach is backed by casuarina trees providing natural shade. Perfect for a relaxed afternoon swim.',
              details: [
                '🏖️ Less crowded than My Khe — families prefer this stretch',
                '🌊 Calm, swimmable conditions in March',
                '🍹 Several beachfront cafés with sun loungers'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'My Hanh Restaurant',
              description: 'A local gem near the Marble Mountains famous for their Mì Quảng Đà Nẵng — turmeric-infused noodles with shrimp, pork, and peanuts. Authentic and very cheap.',
              meta: '💰 $ · 📍 Ngũ Hành Sơn District'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Cơm Nhà Restaurant',
              description: 'Meaning "home cooking," Cơm Nhà serves family-style Vietnamese dishes in a cozy house setting. Excellent for groups — order a spread of rice, stir-fried morning glory, caramelised pork, and fish clay pot.',
              meta: '💰 $ · 📍 Near Han River, Đà Nẵng'
            }
          ],
          tips: [
            { type: 'tip', text: 'Stock up on marble carvings and lacquerware at the workshops at the base of the Marble Mountains — prices are much better than city shops.' }
          ]
        }
      ],
      mapPins: [
        { lat: 16.0030, lng: 108.2624, label: 'Marble Mountains (Thủy Sơn)', num: 1, cat: 'attraction', desc: 'Sacred marble peaks with cave pagodas and panoramic views' },
        { lat: 15.9981, lng: 108.2711, label: 'Non Nuoc Beach', num: 2, cat: 'attraction', desc: 'Quieter beach below the Marble Mountains' },
        { lat: 16.0035, lng: 108.2620, label: 'Huyền Không Cave', num: 3, cat: 'attraction', desc: 'Largest cave with dramatic natural skylight over Buddha statues' },
        { lat: 16.0030, lng: 108.2624, label: 'Non Nuoc Stone Village', num: 4, cat: 'attraction', desc: 'Stone-carving workshops — great for souvenirs' }
      ]
    },
    {
      num: 5,
      date: '2026-03-20',
      neighborhoods: 'Hội An Ancient Town',
      title: 'Hội An Day Trip — Ancient Town & Lanterns',
      description: 'A full day in the UNESCO-listed Ancient Town of Hội An — cycling its narrow lanes, crossing the Japanese Covered Bridge, browsing tailor shops, and watching lanterns float on the Thu Bồn River at dusk.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive to Hội An & Ancient Town Exploration',
              description: 'Hội An is 30km south of Đà Nẵng — about 45 minutes by car or 1 hour by motorbike taxi. Arrive early before the heat and tour groups. Pick up a combined ticket (120,000 VND) granting entry to five heritage sites.',
              details: [
                '🏛️ Japanese Covered Bridge (Chùa Cầu) — the symbol of Hội An',
                '🏠 Tấn Ký Merchant House — beautifully preserved 18th-century trading house',
                '🏯 Phúc Kiến Assembly Hall — ornate Chinese temple with family blessing rituals',
                '🚲 Rent bicycles in town (~$2/day) — ideal for exploring'
              ]
            }
          ],
          meals: [
            {
              type: '🥐 Breakfast',
              name: 'Morning Glory Street Food Restaurant',
              description: 'One of Hội An\'s most famous restaurants, opened by celebrated chef Ms. Vy. Try Cao Lầu (Hội An\'s signature noodle dish), Bánh Mì, and White Rose dumplings.',
              meta: '💰 $ · 📍 9 Hoàng Diệu Street, Hội An'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Riverside Stroll & Tailor Shops',
              description: 'Wander the riverside promenade, browse the tailors that made Hội An famous (custom clothes made in 24 hours!), and explore the colourful Central Market. If the kids need a break from walking, the An Hội Island in the middle of the river has cafés and games.',
              details: [
                '👗 Custom tailoring: $20–60 for a dress or shirt, ready next day',
                '🛍️ Yaly Couture and Bảo Khách are well-regarded tailors',
                '🌸 Central Market — pick up local lanterns, silk goods, and spices'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Mì Quảng Bà Mua',
              description: 'A legendary street-food stall serving the best Mì Quảng in Hội An — turmeric noodles with shrimp, pork, herbs, peanuts, and crispy rice crackers.',
              meta: '💰 $ · 📍 Street stall, Trần Phú area, Hội An'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Lantern Boat on Thu Bồn River',
              description: 'As dusk falls, hundreds of paper lanterns are lit across Hội An. Buy floating paper lanterns at riverside stalls ($1 each) and release them on the Thu Bồn River — a truly magical experience with children. The ancient town lights up beautifully at night.',
              details: [
                '🏮 Lanterns available at riverside stalls (~$1)',
                '🌙 The river reflection is most beautiful after 8pm',
                '🎎 Full Moon Festival (Phố Cổ) — if your dates align, vehicles are banned and it\'s extraordinary'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'The Cargo Club',
              description: 'Beautifully situated overlooking the river with a terrace, serving both Vietnamese and Western dishes. Famous for their French-Vietnamese fusion and incredible desserts.',
              meta: '💰 $$ · 📍 107 Nguyễn Thái Học, riverside, Hội An'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 15.8801, lng: 108.3380, label: 'Japanese Covered Bridge', num: 1, cat: 'attraction', desc: 'Symbol of Hội An — 400-year-old covered bridge' },
        { lat: 15.8801, lng: 108.3380, label: 'Hội An Ancient Town', num: 2, cat: 'attraction', desc: 'UNESCO World Heritage merchant town' },
        { lat: 15.8819, lng: 108.3356, label: 'Morning Glory Restaurant', num: 3, cat: 'food', desc: 'Best Cao Lầu and White Rose dumplings in town' },
        { lat: 15.8780, lng: 108.3390, label: 'Thu Bồn River', num: 4, cat: 'attraction', desc: 'Release floating lanterns at dusk — magical family moment' },
        { lat: 15.8796, lng: 108.3371, label: 'The Cargo Club', num: 5, cat: 'food', desc: 'Riverside terrace dining with Vietnamese-French fusion' }
      ]
    },
    {
      num: 6,
      date: '2026-03-21',
      neighborhoods: 'Hội An Beaches · An Bàng Beach',
      title: 'Hội An Beach Day & Cooking Class',
      description: 'Morning at one of Vietnam\'s best beaches, then a hands-on Vietnamese cooking class in the afternoon where the whole family learns to make Cao Lầu, spring rolls, and Bánh Xèo.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'An Bàng Beach',
              description: 'An Bàng is 3km from Hội An Ancient Town — a gorgeous, unhurried stretch of beach lined with beach bars and hammocks. In March, the water is clear and calm. Rent sunbeds, snorkel in the clear water, and enjoy Vietnamese iced coffee at a beachfront café.',
              details: [
                '🏖️ One of the most beautiful and relaxed beaches in Vietnam',
                '🌊 Calm conditions in March — perfect for kids',
                '🍹 Soul Kitchen and La Plage beach bars have great vibes and food'
              ]
            }
          ],
          meals: [
            {
              type: '🥐 Breakfast',
              name: 'An Bàng Beach Cafés',
              description: 'Grab fresh fruit, Bánh Mì, and strong Vietnamese iced coffee (cà phê sữa đá) from the small cafés at An Bàng.',
              meta: '💰 $ · 📍 An Bàng Beach, Hội An'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Vietnamese Cooking Class',
              description: 'Join a half-day cooking class — a fantastic family activity. Classes typically start with a market visit at Hội An\'s Central Market, then you learn to make 3–4 dishes: fresh spring rolls, Cao Lầu, Bánh Xèo (sizzling pancakes), and a local dessert. Everything you cook, you eat.',
              details: [
                '👨‍🍳 Many great schools: Red Bridge Cooking School, Morning Glory Cooking Class, Vy\'s Market Tour & Cooking Class',
                '💰 ~$30–40/person including market tour, recipes, and meal',
                '👶 Very family-friendly — kids love rolling spring rolls',
                '⏰ Book ahead — popular activity'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Evening in Ancient Town',
              description: 'Return to the Ancient Town for a relaxed evening. Browse the night market, enjoy a drink on a rooftop bar, or simply wander the illuminated lanes.',
              details: [
                '🌆 Ancient Town at night with lanterns is completely different to daytime',
                '🍹 The Rooftop Bar at Mango Mango has great cocktails and views'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Phố Xưa Restaurant',
              description: 'An excellent, affordable family restaurant serving traditional Hội An dishes including the famous White Rose dumplings, Hải Sản (seafood), and local wonton soup.',
              meta: '💰 $ · 📍 Hội An Ancient Town area'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 15.9054, lng: 108.3669, label: 'An Bàng Beach', num: 1, cat: 'attraction', desc: 'Lovely, relaxed beach 3km from Hội An Ancient Town' },
        { lat: 15.8801, lng: 108.3380, label: 'Hội An Central Market', num: 2, cat: 'attraction', desc: 'Local market — start of most cooking class tours' },
        { lat: 15.8835, lng: 108.3392, label: 'Red Bridge Cooking School', num: 3, cat: 'attraction', desc: 'Highly rated cooking class with river boat transfer' },
        { lat: 15.8801, lng: 108.3380, label: 'Hội An Night Market', num: 4, cat: 'attraction', desc: 'Lantern-lit night market on An Hội island' }
      ]
    },
    {
      num: 7,
      date: '2026-03-22',
      neighborhoods: 'Mỹ Sơn Sanctuary · Countryside',
      title: 'Mỹ Sơn — Ancient Cham Temples in the Jungle',
      description: 'A half-day excursion to the UNESCO World Heritage Mỹ Sơn Sanctuary — 70+ red-brick Cham towers built between the 4th and 14th centuries, hidden in a lush jungle valley surrounded by misty mountains.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Mỹ Sơn Sanctuary',
              description: 'Often called "Vietnam\'s Angkor Wat," Mỹ Sơn is a remarkable complex of Hindu temples built by the ancient Cham civilisation. The towers rise from a forested valley with a dramatic mountain backdrop. Arrive by 8am to beat the heat and tour groups — the morning light through the jungle is spectacular.',
              details: [
                '🏛️ UNESCO World Heritage Site since 1999',
                '⏰ Plan 2–3 hours to explore properly',
                '💰 Entry: ~150,000 VND/person (~$6)',
                '🎭 Traditional Cham dance performances at 9:30am and 10:30am',
                '🌿 Wear light clothing — it gets humid in the jungle by mid-morning'
              ]
            }
          ],
          meals: [
            {
              type: '🥐 Breakfast',
              name: 'Hotel or Roadside Café',
              description: 'Grab a Bánh Mì and coffee before departure — you\'ll want to arrive at Mỹ Sơn early.',
              meta: '💰 $ · 📍 Along route from Đà Nẵng'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Return via Thu Bồn Boat (Optional)',
              description: 'Some tours offer a scenic return by traditional wooden boat on the Thu Bồn River — 45 minutes drifting past rice paddies and small fishing villages back to Hội An. Highly recommended if available.',
              details: [
                '⛵ Boat return option usually costs an extra $5–10/person',
                '🌾 Pass traditional riverside villages untouched by tourism',
                '📸 The mountain backdrop and river together are stunning'
              ]
            },
            {
              title: 'Afternoon in Hội An or Beach',
              description: 'If energy allows, stop again in Hội An for last-minute tailor pickups (if you ordered on Day 5), or head to An Bàng Beach for a final dip.',
              details: [
                '👗 Day 5 tailor orders will be ready — this is your pickup day',
                '🏖️ An Bàng is only 10 minutes from the Ancient Town'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Hội An Street Food',
              description: 'Stop in Hội An on the way back for a quick street food lunch — Bánh Mì Phượng is legendary (featured by Anthony Bourdain).',
              meta: '💰 $ · 📍 Bánh Mì Phượng, 2B Phan Chu Trinh, Hội An'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Nhà Hàng Trần Restaurant',
              description: 'A fantastic local restaurant in Đà Nẵng known for Central Vietnamese classics. Order the Nem Lụi (grilled pork skewers wrapped in rice paper) and Bún Bò Huế.',
              meta: '💰 $ · 📍 Đà Nẵng city'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 15.7736, lng: 108.1231, label: 'Mỹ Sơn Sanctuary', num: 1, cat: 'attraction', desc: 'UNESCO Cham temple complex in jungle valley — Vietnam\'s Angkor Wat' },
        { lat: 15.8780, lng: 108.3390, label: 'Thu Bồn River', num: 2, cat: 'attraction', desc: 'Scenic boat return from Mỹ Sơn through rural villages' },
        { lat: 15.8796, lng: 108.3345, label: 'Bánh Mì Phượng', num: 3, cat: 'food', desc: 'World-famous Bánh Mì spot — Anthony Bourdain approved' }
      ]
    },
    {
      num: 8,
      date: '2026-03-23',
      neighborhoods: 'Đà Nẵng City · Han Market · Museum of Cham Sculpture',
      title: 'City Day — Cham Museum, Han Market & Food Tour',
      description: 'Explore Đà Nẵng\'s cultural core: the world-class Museum of Cham Sculpture, the bustling Han Market, and an evening street food tour through the city\'s best local eats.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Museum of Cham Sculpture',
              description: 'The Museum of Cham Sculpture houses the world\'s largest collection of Cham artefacts — over 2,000 sandstone sculptures dating from the 5th to 15th centuries. An essential stop for understanding the Mỹ Sơn temples you visited yesterday.',
              details: [
                '🏛️ Founded in 1915 by the French, expanded multiple times since',
                '💰 Entry: 60,000 VND (~$2.50)',
                '⏰ Allow 1–1.5 hours',
                '📸 No flash photography inside, but sculptures are incredibly photogenic'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Cong Caphe',
              description: 'Vietnam\'s most popular chain café with a military-aesthetic design and excellent cà phê cốt dừa (coconut coffee). Kids love the smoothies.',
              meta: '💰 $ · 📍 Multiple locations, Đà Nẵng'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Han Market',
              description: 'Đà Nẵng\'s central market is a sensory riot — fresh tropical fruits, live seafood tanks, local spices, silk clothing, and hundreds of stalls. The ground floor is food; upper floors have clothing and handicrafts. Great for picking up local specialties: dried shrimp, Hội An noodles, and Vietnamese ground pepper.',
              details: [
                '🦐 Try fresh coconut juice and exotic tropical fruits at the fruit stalls',
                '🧧 Silk and clothing — prices are negotiable',
                '🌶️ Pick up local Quảng Nam peppercorns as a great souvenir',
                '⏰ Best visited in the morning, but open all day'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Đà Nẵng Street Food Evening Walk',
              description: 'Join a street food tour or self-guide through the local food streets. Start at Bạch Đằng riverside, then work inland through the "food streets" near Lê Duẩn. Sample Bánh Tráng Cuốn Thịt Heo (rice paper rolls with pork), Bột Lọc (tapioca dumplings), and Chè (sweet dessert soups).',
              details: [
                '🍢 Stick to stalls with high turnover and local crowds',
                '💰 Eat for $5–8 per person hitting 4–5 dishes',
                '🌙 The riverside food streets are liveliest after 6:30pm'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Bà Tám Restaurant',
              description: 'Local favourite for "com tam" broken rice plates with grilled pork, fried egg, and pickled vegetables. Very cheap, very good, and very Đà Nẵng.',
              meta: '💰 $ · 📍 Hải Châu District, Đà Nẵng'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 16.0624, lng: 108.2219, label: 'Museum of Cham Sculpture', num: 1, cat: 'attraction', desc: 'World\'s largest collection of Cham stone sculpture' },
        { lat: 16.0669, lng: 108.2241, label: 'Han Market', num: 2, cat: 'attraction', desc: 'Central market with fresh food, textiles, and local goods' },
        { lat: 16.0610, lng: 108.2241, label: 'Bạch Đằng Food Street', num: 3, cat: 'food', desc: 'Riverfront street food area — best after 6:30pm' },
        { lat: 16.0624, lng: 108.2219, label: 'Cong Caphe', num: 4, cat: 'food', desc: 'Beloved café chain — coconut coffee is a must' }
      ]
    },
    {
      num: 9,
      date: '2026-03-24',
      neighborhoods: 'My Khe Beach · Water Sports · Phạm Văn Đồng',
      title: 'Adventure Beach Day & Water Sports',
      description: 'A pure adventure day on the water — kayaking, jet skiing, banana boats, and paddleboarding along Đà Nẵng\'s coastline, followed by a relaxed seafood feast at sunset.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Water Sports at My Khe Beach',
              description: 'The beach clubs along My Khe offer a full menu of water sports at very reasonable prices. As a group of 3–4, you can try surfing, kayaking, paddleboarding, banana boats, and jet skis — great fun for both adults and kids.',
              details: [
                '🏄 Surfing lessons: ~$15/hr with instructor and board',
                '🛶 Kayaking: ~$8/hr per kayak',
                '🍌 Banana boat ride: ~$8/person per round',
                '🚤 Jet ski: ~$30–40 for 30 minutes',
                '📍 Best operators cluster around the central section of My Khe'
              ]
            }
          ],
          meals: [
            {
              type: '🥐 Breakfast',
              name: 'Beach Café',
              description: 'Eat light before water sports — fresh baguette, fruit, and Vietnamese iced coffee from any beachfront café.',
              meta: '💰 $ · 📍 My Khe Beach area'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Leisure Beach & Rest',
              description: 'After a morning of activity, claim sun loungers and chill out. Read, nap, swim at leisure. This is the downtime the group has earned after a packed first week.',
              details: [
                '🌅 The section in front of the large beach hotels has cleanest facilities',
                '🏊 March water temperature ~25°C — perfect'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🦞 Dinner',
              name: 'Bé Mặn Seafood 2',
              description: 'Return to a beloved local seafood spot for a proper feast — tiger prawns, steamed clams with lemongrass, whole grilled fish, and ice-cold Larue beer (Đà Nẵng\'s local brew). Order family-style.',
              meta: '💰 $$ · 📍 Phạm Văn Đồng area, near the beach'
            }
          ],
          tips: [
            { type: 'tip', text: 'Larue Beer is brewed in Đà Nẵng and is the local beer of choice. Incredibly cheap and refreshing. Order a 333 or Huda if you want variety.' }
          ]
        }
      ],
      mapPins: [
        { lat: 16.0600, lng: 108.2472, label: 'My Khe Beach Water Sports', num: 1, cat: 'attraction', desc: 'Water sports hub — surfing, kayaking, jet skis, banana boats' },
        { lat: 16.0800, lng: 108.2466, label: 'Phạm Văn Đồng Seafood Strip', num: 2, cat: 'food', desc: 'Local seafood restaurants along the beach road' }
      ]
    },
    {
      num: 10,
      date: '2026-03-25',
      neighborhoods: 'Huế · Imperial City · Thừa Thiên Huế Province',
      title: 'Day Trip to Huế — Imperial Citadel & Royal Tombs',
      description: 'A full day exploring Vietnam\'s former imperial capital — the grand citadel, the mystical Thien Mu Pagoda on the Perfume River, and ornate royal tombs in the surrounding hills.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive to Huế via Hải Vân Pass',
              description: 'The 90-minute drive north from Đà Nẵng over the Hải Vân Pass is one of Vietnam\'s most dramatic roads — dense cloud forest, sweeping ocean views, and old French fortifications. The pass appears in The Grand Tour "Vietnam Special." Highly recommend having a driver for this.',
              details: [
                '🌊 Hải Vân Pass offers jaw-dropping views of Lăng Cô Bay below',
                '🏰 Old French artillery fortifications line the ridge',
                '🚌 Or take the train through the tunnel (faster but misses the scenery)'
              ]
            },
            {
              title: 'Huế Imperial Citadel (Đại Nội)',
              description: 'The Imperial Citadel is a walled city within a city — built in the early 1800s by Emperor Gia Long. Explore the UNESCO-listed complex of gates, throne rooms, ceremonial halls, and beautiful lotus-filled moats. Much of it was damaged in the Vietnam War but ongoing restoration is impressive.',
              details: [
                '💰 Entry: 200,000 VND/adult, 40,000 VND/child (~$8/adult)',
                '⏰ Allow 2 hours minimum for the main citadel',
                '👘 Dress modestly for temple areas',
                '📸 The Ngọ Môn Gate and Thai Hoa Palace are the highlights'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Thien Mu Pagoda & Perfume River',
              description: 'The 7-storey Thien Mu Pagoda is the most famous landmark in Huế, perched on a bluff above the Perfume River. Take a dragon boat up the river to reach it. The serene gardens and the ancient car of Buddhist monk Thích Quảng Đức (who self-immolated in protest in 1963) are sobering and profound.',
              details: [
                '🛶 Dragon boat from city center: ~$5–10 return per boat',
                '🏯 The pagoda dates from 1601 — one of Vietnam\'s oldest',
                '🌸 The Perfume River at this point is incredibly peaceful'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Hanh Restaurant',
              description: 'Famous for authentic Huế royal cuisine — Bún Bò Huế (spicy beef noodle soup), Cơm Hến (tiny clam rice), and Bánh Khoái (crispy Huế pancake). Huế food is arguably Vietnam\'s most complex and refined.',
              meta: '💰 $ · 📍 Trần Hưng Đạo Street, Huế'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Đà Nẵng',
              description: 'Head back via the Hải Vân Tunnel (faster, toll road) in time for dinner. Stop at Lăng Cô Beach if energy allows — a stunning lagoon beach at the base of the pass.',
              details: [
                '🏖️ Lăng Cô Beach: 5-minute detour, beautiful crescent bay',
                '⏰ Aim to be back in Đà Nẵng by 7pm'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Trúc Lâm Viên Restaurant',
              description: 'A stunning garden restaurant in Đà Nẵng set in a replica traditional Vietnamese village. Live traditional music, excellent local food, and atmospheric bamboo surroundings.',
              meta: '💰 $$ · 📍 Hòa Hải Ward, Ngũ Hành Sơn District'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 16.2872, lng: 107.5764, label: 'Huế Imperial Citadel', num: 1, cat: 'attraction', desc: 'UNESCO imperial walled city — 19th-century Vietnamese capital' },
        { lat: 16.4523, lng: 107.5449, label: 'Hải Vân Pass', num: 2, cat: 'attraction', desc: 'Dramatic mountain pass with ocean views — as seen on The Grand Tour' },
        { lat: 16.2981, lng: 107.5568, label: 'Thien Mu Pagoda', num: 3, cat: 'attraction', desc: '7-storey pagoda on the Perfume River — Huế\'s most iconic sight' },
        { lat: 16.2174, lng: 108.0727, label: 'Lăng Cô Beach', num: 4, cat: 'attraction', desc: 'Beautiful lagoon beach at the base of Hải Vân Pass' }
      ]
    },
    {
      num: 11,
      date: '2026-03-26',
      neighborhoods: 'Đà Nẵng · Dragon Bridge · Asia Park',
      title: 'Final Day — Asia Park, Souvenirs & Dragon Bridge Send-Off',
      description: 'A relaxed final full day — morning shopping and souvenirs, afternoon at Asia Park Sun World for the kids, and a proper farewell dinner on the Han River.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Final Shopping & Big C / Han Market',
              description: 'Stock up on last-minute Vietnamese souvenirs and food gifts. Lotte Mart and Big C have well-priced cashews, dried fruit, Phú Quốc fish sauce, and packaged coffee. Han Market is great for lacquerware, silk scarves, and marble figurines (from the Non Nuoc stone village).',
              details: [
                '☕ Vietnamese drip coffee (Trung Nguyên) makes an excellent gift',
                '🥜 Cashews, macadamia nuts, and dried mango are great for the flight home',
                '🎁 Marble figurines, silk lanterns, and lacquerware from Han Market'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Breakfast / Brunch',
              name: 'Bánh Mì Stall',
              description: 'Final Đà Nẵng Bánh Mì moment — grab a freshly filled baguette from any street stall. Pâté, pickled vegetables, chilli sauce, and fresh herbs.',
              meta: '💰 $ · 📍 Any street stall in Đà Nẵng'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Asia Park Sun World',
              description: 'Đà Nẵng\'s large amusement park is a great final afternoon activity for families. Highlights include the Sun Wheel (one of the largest Ferris wheels in Asia at 115m), rollercoasters, and a themed zone recreating landscapes from across Asia.',
              details: [
                '🎡 Sun Wheel: 115m high — views over the whole city',
                '💰 Entry: ~$12/person',
                '⏰ Open from noon, best in the afternoon when the light is softer'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dragon Bridge Fire Show (Final Night)',
              description: 'If today is Saturday or Sunday, make sure to be at the Dragon Bridge at 9pm for the legendary fire and water show. Even if it\'s a weekday, the illuminated bridge is a perfect final memory of Đà Nẵng.',
              details: [
                '🐉 Fire show: Sat & Sun 9pm — if March 26 is a Thursday, the bridge is still gorgeous lit',
                '📍 East bank of the Han River for best views',
                '📸 Golden hour on the river before dinner is stunning'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Riverside Dining at Waterfront Restaurant',
              description: 'A beautiful farewell dinner on the Han River waterfront — the Waterfront Restaurant (or similar riverfront spot) serves excellent Vietnamese and international dishes with views of the illuminated Dragon Bridge.',
              meta: '💰 $$ · 📍 Bach Dang Street, Han River, Đà Nẵng'
            }
          ],
          tips: [
            { type: 'tip', text: 'Exchange remaining VND at the airport or your hotel before departure — rates at the airport are fair. ATMs in town give better rates than exchange counters.' }
          ]
        }
      ],
      mapPins: [
        { lat: 16.0669, lng: 108.2241, label: 'Han Market', num: 1, cat: 'attraction', desc: 'Final souvenir shopping — silk, marble, coffee, cashews' },
        { lat: 16.0447, lng: 108.2328, label: 'Asia Park Sun World', num: 2, cat: 'attraction', desc: '115m Sun Wheel Ferris wheel and family amusement park' },
        { lat: 16.0610, lng: 108.2298, label: 'Dragon Bridge Final Night', num: 3, cat: 'attraction', desc: 'Iconic dragon bridge — fire show Sat/Sun 9pm' },
        { lat: 16.0570, lng: 108.2219, label: 'Waterfront Restaurant', num: 4, cat: 'food', desc: 'Han River waterfront farewell dinner with bridge views' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (per room)', budget: '$25–50/night', midrange: '$50–100/night', luxury: '$100–250/night' },
    { category: 'Meals (per person)', budget: '$8–15/day', midrange: '$15–30/day', luxury: '$40–80/day' },
    { category: 'Transport (car/Grab)', budget: '$10–20/day', midrange: '$20–40/day', luxury: '$50–100/day' },
    { category: 'Bà Nà Hills Entry', budget: '$38/adult', midrange: '$38/adult', luxury: '$38/adult' },
    { category: 'Activities', budget: '$5–20/day', midrange: '$20–40/day', luxury: '$50–100/day' },
    { category: '11-Night Total (group of 4)', budget: '$1,200–1,800', midrange: '$2,200–3,500', luxury: '$5,000–8,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Đà Nẵng International Airport (DAD) is in the city — 15 min to most hotels', 'Direct flights from Bangkok, Singapore, Seoul, Tokyo, and many Chinese cities', 'Grab is the easiest airport transfer — book from the arrivals hall'] },
    { title: '🏨 Where to Stay', items: ['My Khe Beach area — best for beach access, many family-friendly hotels', 'Han River area — central, walkable to museums and restaurants', 'Budget options: $25–50/night for a clean family room', 'Mid-range: Fusion Suites, Premier Village, Grandvrio ($80–150/night)'] },
    { title: '🌡️ March Weather', items: ['Dry season, 25–30°C, excellent beach weather', 'Bà Nà Hills is cooler (~18°C) and can be misty — bring a light jacket', 'UV is strong — SPF 50, hats, and rash vests for kids'] },
    { title: '💵 Money', items: ['Vietnamese Đồng (VND) — 25,000 VND ≈ $1 USD', 'ATMs widely available — Vietcombank and BIDV have low fees', 'Most markets are cash-only; restaurants increasingly accept cards', 'Budget comfortably on under $60–80/day for a family of 4'] },
    { title: '🌐 Connectivity', items: ['Buy a Viettel or Mobifone SIM at the airport (~$5 for 10GB)', 'WiFi is excellent at all hotels and most restaurants', 'Grab app is essential — download before arrival'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
