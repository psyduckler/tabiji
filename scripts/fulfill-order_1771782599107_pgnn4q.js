const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771782599107_pgnn4q',
  email: 'bonaxa9981@advarm.com',
  destination: 'Japan',
  start_date: '2026-05-13',
  end_date: '2026-05-27',
  groupSize: 2,
  travelStyle: 'Adventure, Cultural, Foodie',
  dining: 'Mix of everything',
  budget: '$1,000-2,000',
  requests: ''
};

const itineraryData = {
  destination: 'Japan',
  countryEmoji: '🇯🇵',
  title: 'The Ultimate Japan Adventure',
  subtitle: '14 days of ramen lanes, ancient shrines, bamboo forests & street-food magic',
  description: "Japan in May is a dream: the cherry blossoms have given way to lush green landscapes, the days are warm but not sweltering, and the crowds thin just enough to let you breathe it all in. This 14-night itinerary weaves Tokyo's electric neighborhoods, Kyoto's UNESCO-listed temples, Hakone's volcanic drama and Mt. Fuji views, the soul of Hiroshima, and Osaka's legendary food scene into one unforgettable journey for two.",
  duration: '14 nights',
  dates: 'May 13 – May 27, 2026',
  budget: '$$–$$$',
  pace: 'Moderate',
  bestFor: 'Couples & Adventure-Seekers',

  highlights: [
    'Sunrise hike up Fushimi Inari through thousands of vermilion torii gates',
    'Float in an outdoor onsen in Hakone with Mt. Fuji as your backdrop',
    'Midnight street-food crawl through Osaka\'s Dotonbori neon jungle',
    'Row a boat through Arashiyama\'s jade bamboo grove at dawn',
    'Slurp the perfect bowl of tonkotsu ramen in Shibuya at 2am',
    'Stand in the Peace Park in Hiroshima — one of the most moving places on Earth',
    'Tsukiji outer market breakfast: sushi, tamagoyaki, and tuna on toast'
  ],

  essentials: [
    { title: '🚄 Getting Around', text: 'Buy a 14-day Japan Rail Pass before you leave home — it covers Shinkansen (bullet train) and most JR lines. Tap IC card (Suica/Pasmo) for local subway, buses, and convenience store purchases. Download Google Maps offline for Japan.' },
    { title: '🌸 May Weather', text: 'May is prime Japan weather — 18–25°C in Tokyo and Kyoto, lower in the mountains. Light jacket for evenings, sunscreen for daytime. Rain jacket for the odd shower. No cherry blossoms but fresh vivid green everywhere.' },
    { title: '💴 Money', text: 'Japan is still largely cash-based. Withdraw yen at 7-Eleven ATMs (most reliable for foreign cards). Budget around ¥5,000–10,000/day per person for food and local transport. Most restaurants don\'t split bills — settle per table.' },
    { title: '📱 Connectivity', text: 'Get a data SIM (IIJmio, Sakura Mobile) or pocket Wi-Fi at the airport. Unlimited data is essential for navigation and translation. Google Translate camera mode reads Japanese menus instantly.' },
    { title: '🍣 Foodie Tips', text: 'Conbini (convenience stores: 7-Eleven, Lawson, FamilyMart) are a foodie revelation — onigiri, sandos, hot oden, and craft beer 24/7. Lunch sets (teishoku) are the best value eat — a restaurant\'s dinner menu at half the price. Tip: never tip in Japan, it can be seen as rude.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-05-13',
      neighborhoods: 'Shinjuku · Golden Gai · Omoide Yokocho',
      title: 'Tokyo Arrival — Neon, Ramen & Midnight Alleys',
      description: "Land at Narita or Haneda, grab your JR Pass and Suica card, and dive straight into the organized chaos of Shinjuku. Tonight's mission: get lost in Golden Gai's 200 tiny bars and eat yakitori under the railway tracks at Omoide Yokocho.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive & Orient in Shinjuku',
              description: "Check into your hotel near Shinjuku Station — the perfect base for your first few Tokyo days. Walk the famous Shinjuku crossing, wander into Kabukicho's colorful streets, and visit the free Tokyo Metropolitan Government Building observation deck for a first panoramic take on this endless city.",
              details: [
                '🏨 Stay near Shinjuku or Shibuya for subway access in all directions',
                '🆓 Tokyo Metropolitan Government Building observation deck: free, open until 10:30pm',
                '🗺️ Pick up a pocket map at the tourist info desk in Shinjuku Station'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Activate your JR Pass and get your Suica card loaded with ¥3,000 at Shinjuku Station on arrival. Saves time every single day.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Omoide Yokocho & Golden Gai',
              description: "\"Memory Lane\" — a narrow smoke-filled alley of tiny yakitori stalls that hasn't changed since the 1950s. Sit at the counter, order skewers of chicken, and share a cold Sapporo. Then drift into Golden Gai: 200 micro-bars packed into six tiny alleys, each with its own eccentric personality.",
              details: [
                '🍢 Omoide Yokocho: north side of Shinjuku Station, West Exit',
                '🍺 Golden Gai: order a "mama-san\'s special" at any bar — they\'re all different',
                '⚠️ Many Golden Gai bars charge a ¥500–1,000 seating/cover fee — totally normal'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Late Dinner',
              name: 'Ichiran Ramen, Shinjuku',
              description: "The world's most famous solo ramen chain — but going as a couple makes it even better. Customise every element of your tonkotsu broth in your private booth, slurp in deliberate silence, and understand why Japan does ramen better than anyone.",
              meta: '💰 ¥1,200/bowl · 📍 Multiple Shinjuku locations, open 24h'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6896, lng: 139.6917, label: 'Shinjuku Station', num: 1, cat: 'transport', desc: 'Busiest station in the world — your Tokyo hub' },
        { lat: 35.6939, lng: 139.6994, label: 'Kabukicho', num: 2, cat: 'attraction', desc: 'Tokyo\'s famous entertainment and neon district' },
        { lat: 35.6895, lng: 139.6917, label: 'Tokyo Metropolitan Gov. Building', num: 3, cat: 'attraction', desc: 'Free observation deck with sweeping city views' },
        { lat: 35.6938, lng: 139.7001, label: 'Omoide Yokocho', num: 4, cat: 'food', desc: 'Memory Lane — smoky 1950s yakitori alley' },
        { lat: 35.6932, lng: 139.7028, label: 'Golden Gai', num: 5, cat: 'food', desc: '200 eccentric micro-bars in six narrow alleys' },
        { lat: 35.6918, lng: 139.6995, label: 'Ichiran Ramen Shinjuku', num: 6, cat: 'food', desc: 'Private-booth tonkotsu ramen perfection' }
      ]
    },
    {
      num: 2,
      date: '2026-05-14',
      neighborhoods: 'Harajuku · Omotesando · Shibuya',
      title: 'Tokyo Fashion, Culture & the World\'s Busiest Crossing',
      description: "Crepes in Harajuku, high fashion along Omotesando Keyaki-namiki, and the hypnotic chaos of Shibuya Crossing at rush hour. End the evening with a rooftop cocktail watching Tokyo spread to every horizon.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Meiji Shrine & Yoyogi Park',
              description: "Start with tranquility inside the city. Meiji Shrine is one of Japan's most important Shinto shrines, set in 70 hectares of forested parkland. Walk the gravel path under towering cedar torii, write a wish on an ema wooden plaque, and watch a ritual ceremony if timing is right.",
              details: [
                '⛩️ Free entry · Open sunrise to sunset',
                '🌳 May: Yoyogi Park is at its lush green best — perfect for a picnic',
                '📸 The main gate (O-torii) is dramatic for photos — arrive early before crowds'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Takeshita Street & Omotesando',
              description: "Walk ten seconds from Meiji Shrine\'s serene forest to Takeshita Street\'s sensory explosion — rainbow cotton candy, extreme fashion, and cosplay culture in full force. Then turn the corner to Omotesando\'s tree-lined boulevard of flagship architecture (Louis Vuitton by Aoki, Prada by Herzog & de Meuron).",
              details: [
                '🍭 Try a crepe from Marion Crepes — a Harajuku institution since 1976',
                '🏛️ Omotesando Hills by Tadao Ando is worth a look even if you don\'t shop',
                '🛍️ Kiddy Land: six floors of Japanese character goods — dangerously fun'
              ]
            }
          ],
          meals: [
            {
              type: '🥢 Lunch',
              name: 'Afuri Ramen, Harajuku',
              description: "Light, citrus-forward yuzu shio ramen — a perfect counterpoint to the heavy tonkotsu of last night. Their harajuku location has a beautiful open kitchen and seasonal specials.",
              meta: '💰 ¥1,300 · 📍 1F RTO Harajuku, Harajuku'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shibuya Crossing at Rush Hour',
              description: "Position yourself on the second floor of the Shibuya Scramble Square skyscraper or grab a window seat at Starbucks Shibuya Tsutaya to watch the crossing from above. Then join the flow — cross it yourself in every direction. It\'s chaotic, electric, and uniquely Tokyo.",
              details: [
                '📸 Best crossing views: Scramble Square rooftop (paid) or Mag\'s Park (free)',
                '🌆 Hit it at 5:30–6:30pm on a weekday for maximum visual impact',
                '🛍️ Shibuya 109 and Loft are rabbit warrens of Japanese pop culture'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Ushigoro Bambina, Shibuya',
              description: "Wagyu beef sukiyaki in a stylish Shibuya setting. Thinly sliced A5 Wagyu dipped in sweet soy broth with raw egg — one of Japan's most indulgent and accessible high-end food experiences.",
              meta: '💰 ¥4,000–8,000/person · 📍 Shibuya'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6763, lng: 139.6993, label: 'Meiji Shrine', num: 1, cat: 'attraction', desc: 'Tokyo\'s most important Shinto shrine in forested parkland' },
        { lat: 35.6701, lng: 139.7026, label: 'Takeshita Street', num: 2, cat: 'attraction', desc: 'Harajuku\'s famous street for extreme fashion & crepes' },
        { lat: 35.6654, lng: 139.7070, label: 'Omotesando Hills', num: 3, cat: 'attraction', desc: 'Tadao Ando-designed luxury shopping complex' },
        { lat: 35.6652, lng: 139.7076, label: 'Afuri Ramen Harajuku', num: 4, cat: 'food', desc: 'Light yuzu shio ramen with seasonal specials' },
        { lat: 35.6585, lng: 139.7013, label: 'Shibuya Scramble Crossing', num: 5, cat: 'attraction', desc: 'World\'s busiest pedestrian crossing — pure Tokyo energy' },
        { lat: 35.6601, lng: 139.7025, label: 'Ushigoro Bambina', num: 6, cat: 'food', desc: 'A5 Wagyu sukiyaki in a stylish Shibuya setting' }
      ]
    },
    {
      num: 3,
      date: '2026-05-15',
      neighborhoods: 'Asakusa · Ueno · Akihabara',
      title: 'Old Tokyo — Temples, Markets & Electric Town',
      description: "Asakusa is downtown Tokyo's soul — centuries-old Senso-ji temple, rickshaws, and craft shops. Ueno's park and museum corridor, then Akihabara's surreal universe of anime, electronics, and maid cafés.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Senso-ji Temple & Nakamise Shopping Street',
              description: "Senso-ji is Tokyo's oldest and most visited temple. Walk through the Kaminarimon (Thunder Gate) under its giant lantern, run the gauntlet of Nakamise's souvenir stalls (best ningyo-yaki fish-shaped cakes here), and explore the five-storey pagoda and inner shrine grounds.",
              details: [
                '⛩️ Free entry · Grounds open 24h, inner hall 6am–5pm',
                '🎋 Omikuji fortune slips: tie a bad fortune to the rack to leave it behind',
                '📸 Arrive at 7am for the best light and minimal crowds at Kaminarimon',
                '🛍️ Nakamise Street: try ningen-yaki cakes, ningyo-yaki, agemanju'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Pelican Café, Asakusa',
              description: "A cult Asakusa bakery that\'s been making thick-cut toast and pillowy white bread since 1942. The cafe is legendary for morning toast and coffee — arrive early, the queue is worth it.",
              meta: '💰 ¥500–800 · 📍 Kotobuki 3-chome, Taito-ku'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ueno Park & Ameyoko Market',
              description: "Ueno Park is Tokyo's cultural heartland — the Tokyo National Museum, Ueno Zoo, multiple art galleries, and a gorgeous pond lotus garden. Then plunge into Ameyoko Market street: a chaotic, buzzing open-air market under the elevated train tracks, selling dried fish, fresh produce, street snacks, and surplus goods.",
              details: [
                '🏛️ Tokyo National Museum: world\'s largest collection of Japanese art and artifacts',
                '🦛 Ueno Zoo: Japan\'s oldest zoo, pandas are a big draw',
                '🛒 Ameyoko: best for snacking — grilled scallops, fresh fruit on sticks, dried squid'
              ]
            },
            {
              title: 'Akihabara Electric Town',
              description: "Akihabara is unlike anywhere on Earth — eight-storey electronics stores, floors dedicated entirely to anime figures, retro game arcades, and maid cafés where servers call you \"master\" and draw latte art. Even if you\'re not an anime fan, the sheer maximalism is worth an hour.",
              details: [
                '🎮 Super Potato: legendary retro game store on the 5th floor of its building',
                '🤖 Yodobashi Camera: the mother of all electronics stores — genuinely impressive',
                '☕ @home café: the most famous maid café, good introduction to the genre'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍣 Dinner',
              name: 'Tsuruhashi Fugetsu, Ueno',
              description: "Osaka-style okonomiyaki (savory pancakes) done right in downtown Tokyo. The table grill format is interactive and fun — a great one for two, especially over cold Asahi.",
              meta: '💰 ¥2,000–3,000/person · 📍 4-6-2 Ueno, Taito-ku'
            }
          ],
          tips: [
            { type: 'tip', text: 'After dinner, head to Kaminarimon at night — the illuminated lantern and sparsely crowded temple area is genuinely magical and completely different from the daytime experience.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: 'Senso-ji Temple', num: 1, cat: 'attraction', desc: 'Tokyo\'s oldest temple with iconic Kaminarimon Thunder Gate' },
        { lat: 35.7148, lng: 139.7947, label: 'Nakamise Shopping Street', num: 2, cat: 'food', desc: 'Traditional souvenir stalls leading to Senso-ji' },
        { lat: 35.7189, lng: 139.7747, label: 'Pelican Café', num: 3, cat: 'food', desc: 'Cult 1942 bakery famous for thick-cut morning toast' },
        { lat: 35.7154, lng: 139.7719, label: 'Ueno Park & Tokyo National Museum', num: 4, cat: 'attraction', desc: 'Cultural heartland with world-class Japanese art collection' },
        { lat: 35.7073, lng: 139.7730, label: 'Ameyoko Market', num: 5, cat: 'food', desc: 'Bustling open-air street market under the train tracks' },
        { lat: 35.7023, lng: 139.7743, label: 'Akihabara Electric Town', num: 6, cat: 'attraction', desc: 'Anime, electronics, arcades and maid cafés' }
      ]
    },
    {
      num: 4,
      date: '2026-05-16',
      neighborhoods: 'Tsukiji · Ginza · Shimokitazawa',
      title: 'Market Breakfast, High Design & Tokyo\'s Coolest Village',
      description: "Start at Tsukiji for the world's greatest breakfast, drift through Ginza's art and architecture, then escape to Shimokitazawa — Tokyo's vinyl, coffee and vintage clothing village where the locals actually live.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tsukiji Outer Market Breakfast',
              description: "The inner wholesale market moved to Toyosu, but Tsukiji's outer market is still the ultimate Japanese food pilgrim's breakfast. Arrive by 8am for peak freshness: thick tamagoyaki egg omelette from Yamachō, tuna sashimi on rice, sea urchin toast, and grilled scallops — each from a different tiny stall.",
              details: [
                '🐟 Yamachō: famous tamagoyaki omelette — eat warm from the pan',
                '🍣 Sushi Dai (Toyosu): if you want the full omakase breakfast, queue early at Toyosu',
                '🦪 Try fresh oysters and sea urchin (uni) on buttered toast — unforgettable',
                '⏰ Outer market is busiest 8–10am, most stalls close by noon'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ginza Art Walk',
              description: "Ginza is not just Chanel and Hermès — it's also architecture and art. Walk past the Itoya stationery cathedral (10 floors of Japanese paper and pens), duck into the free Ginza Sony Park, and explore the 21_21 Design Sight in Roppongi (a short subway hop) for Japan's cutting-edge design exhibitions.",
              details: [
                '📚 Itoya: 10-floor stationery heaven — pick up a techo planner or washi tape',
                '🏛️ Mori Art Museum (Roppongi Hills): 52F contemporary art + city views',
                '☕ Blue Bottle Coffee Roppongi: Japan has elevated even American coffee culture'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Sushi Kanesaka, Ginza',
              description: "A Michelin-starred counter serving Edomae-style sushi — the Ginza tradition of vinegared rice and pristine Edo Bay seafood. Opt for the lunch omakase (¥15,000–20,000) for a life-changing experience at a fraction of the dinner price.",
              meta: '💰 ¥¥¥¥ · 📍 Ginza — book at least 2 weeks ahead'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shimokitazawa Village Wander',
              description: "Shimokitazawa is where young creative Tokyo actually lives. Narrow lanes crammed with vintage clothing shops, kissaten coffee bars straight from the 1970s, tiny live music venues, and Tokyo's best indie record stores. No agenda — just wander, listen, and buy a record.",
              details: [
                '🎵 Village Vanguard: Tokyo\'s best music/culture/book shop hybrid — perfect for gifts',
                '☕ Bear Pond Espresso: notorious for the best espresso in Tokyo (and a grumpy owner)',
                '🎸 Disc Union: legendary multi-floor record store — jazz, city pop, and electronic'
              ]
            }
          ],
          meals: [
            {
              type: '🍶 Dinner',
              name: 'Izakaya Juban, Shimokitazawa',
              description: "A proper hole-in-the-wall izakaya with locals packed elbow-to-elbow. Cold nama beer, plates of karaage, yakitori, edamame, and grilled tofu. This is authentic Tokyo night-eating — loud, warm, cheap, and perfect.",
              meta: '💰 ¥2,500/person · 📍 Shimokitazawa · No English menu but point-ordering works'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6655, lng: 139.7697, label: 'Tsukiji Outer Market', num: 1, cat: 'food', desc: 'Ultimate Japanese breakfast market — tamagoyaki, uni, sashimi' },
        { lat: 35.6717, lng: 139.7651, label: 'Ginza', num: 2, cat: 'attraction', desc: 'Tokyo\'s luxury and architecture district' },
        { lat: 35.6698, lng: 139.7625, label: 'Itoya Stationery', num: 3, cat: 'attraction', desc: '10-floor stationery cathedral — Japanese paper and pens' },
        { lat: 35.6604, lng: 139.7293, label: 'Roppongi Hills / Mori Art Museum', num: 4, cat: 'attraction', desc: '52nd floor contemporary art with panoramic Tokyo views' },
        { lat: 35.6612, lng: 139.6678, label: 'Shimokitazawa', num: 5, cat: 'attraction', desc: 'Tokyo\'s coolest village — vinyl, vintage, coffee and live music' },
        { lat: 35.6612, lng: 139.6683, label: 'Bear Pond Espresso', num: 6, cat: 'food', desc: 'Cult espresso bar in the heart of Shimokitazawa' }
      ]
    },
    {
      num: 5,
      date: '2026-05-17',
      neighborhoods: 'Nikkō · Tōshō-gū · Kegon Falls',
      title: 'Day Trip — Nikkō: Ornate Shrines & Jungle Waterfalls',
      description: "Two hours north of Tokyo lies Nikkō — a UNESCO-listed complex of jaw-droppingly ornate Edo-era shrines buried in cedar forest, plus the thundering Kegon Waterfall and the turquoise waters of Lake Chūzenji. The perfect adventure day from the city.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tōshō-gū Shrine Complex',
              description: "Tōshō-gū is one of Japan's most elaborately decorated shrine complexes — every surface gilded, lacquered, or carved with mythological animals. The 207 stone steps up to Tokugawa Ieyasu's mausoleum through ancient cedar trees are unforgettable. Spot the famous \"see no evil, hear no evil\" monkey carvings.",
              details: [
                '⛩️ Entry ¥1,300 for main complex · Best in early morning mist',
                '🐒 Famous Sansaru (three wise monkeys) carving — look for it on the stable wall',
                '🌲 The 500-year-old sugi cedar avenue leading to the complex sets the mood perfectly'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Take the 7:40am Tobu Nikko Line limited express from Shinjuku (JR Pass covers some connections — check the route). Arrive before tour buses at 10am for the best atmosphere.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Lake Chūzenji & Kegon Waterfall',
              description: "Bus up the winding Irohazaka mountain road (48 hairpin turns — thrilling) to Lake Chūzenji at 1,269m. Walk along the crater lake shore, then visit Kegon Falls: 97 meters of thundering white water crashing into a deep gorge. Take the elevator down for the dramatic close-up view.",
              details: [
                '🌊 Kegon Falls elevator: ¥570 round trip, absolutely worth it',
                '🏔️ Lake Chūzenji: calm, cold, and extraordinarily beautiful in May',
                '🍜 Lunch at one of the lakeside restaurants — yuba (tofu skin) is a Nikkō specialty'
              ]
            }
          ],
          meals: [
            {
              type: '🥢 Lunch',
              name: 'Yuba Ryori at Nikko Kanaya Hotel',
              description: "Japan's oldest resort hotel (est. 1873) serves Nikkō's signature dish — yuba (fresh tofu skin) in elegant traditional dining. An authentic taste of historic Meiji-era Japan.",
              meta: '💰 ¥3,000–5,000 · 📍 Nikkō — reservations recommended'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Tokyo',
              description: "Head back to Tokyo in time for dinner. The return Tobu Limited Express is a comfortable 2-hour ride. Grab dinner near your hotel — tonight is a great opportunity to explore your neighborhood's local ramen-ya or izakaya.",
              details: [
                '🕰️ Last comfortable return train leaves Nikkō around 5:30pm',
                '🍜 Look for any small counter restaurant near your hotel with a line outside — that\'s always the right choice'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 36.7583, lng: 139.6041, label: 'Tōshō-gū Shrine', num: 1, cat: 'attraction', desc: 'Ornate UNESCO-listed Edo shrine complex with gilded gates' },
        { lat: 36.7472, lng: 139.5882, label: 'Futarasan Shrine', num: 2, cat: 'attraction', desc: 'Ancient mountain shrine in the cedar forest below Tōshō-gū' },
        { lat: 36.7506, lng: 139.4945, label: 'Kegon Waterfall', num: 3, cat: 'attraction', desc: '97-meter thundering waterfall — take the elevator for the close view' },
        { lat: 36.7300, lng: 139.4810, label: 'Lake Chūzenji', num: 4, cat: 'attraction', desc: 'Volcanic crater lake at 1,269m — strikingly beautiful in May' },
        { lat: 36.7571, lng: 139.6074, label: 'Nikko Kanaya Hotel', num: 5, cat: 'food', desc: 'Japan\'s oldest resort hotel — yuba cuisine since 1873' }
      ]
    },
    {
      num: 6,
      date: '2026-05-18',
      neighborhoods: 'Hakone · Owakudani · Gōra',
      title: 'Hakone — Mt. Fuji Views, Black Eggs & Onsen Bliss',
      description: "Trade Tokyo's concrete for Hakone's volcanic drama. Board the famous Romancecar train, ride the mountain railway and cable car over a steaming volcanic crater, eat black eggs boiled in sulfur springs, and soak in a cedar-tub onsen with Mt. Fuji reflected in the water.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Romancecar to Hakone & Hakone Open Air Museum',
              description: "Board the Odakyu Romancecar from Shinjuku (bookable in advance — do it) for the most scenic train ride near Tokyo. Arrive in Hakone-Yumoto and take the mountain railway up. The Hakone Open Air Museum is a stunning outdoor sculpture park with Rodin, Picasso, and Moore set against forested mountain slopes — easily one of Japan's best museums.",
              details: [
                '🚂 Romancecar: book the front-facing seats for the driver\'s view',
                '🎨 Hakone Open Air Museum: ¥1,600 · Picasso pavilion alone is worth the entry',
                '⏰ Allow 2 hours at the museum — it\'s much bigger than it looks'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Owakudani Volcanic Valley & Black Eggs',
              description: "Board the Hakone Ropeway and ascend over Owakudani — a dramatic volcanic caldera of boiling sulfur vents, ash-grey rocks, and acrid steam. At the top, eat kuro-tamago: hard-boiled eggs cooked in the sulfur springs that turn the shells jet black. Legend says each one adds seven years to your life.",
              details: [
                '🥚 Kuro-tamago: ¥500 for 5 eggs — eat them with salt, simple and eerie',
                '🌋 The ropeway gives spectacular Fuji views on clear days — May is often perfect',
                '⚠️ Owakudani station occasionally closes when volcanic activity spikes — check ahead'
              ]
            },
            {
              title: 'Lake Ashi Boat Cruise',
              description: "Drift across the volcanic crater lake on a pirate ship (yes, really — the Hakone Sightseeing Cruise runs cartoonish galleons). The lake frames Mt. Fuji on clear days in one of Japan's most iconic views. Disembark at Moto-Hakone and walk along the old Tokaido cedar avenue.",
              details: [
                '⛵ Covered by Hakone Freepass (worth buying if spending the night in Hakone)',
                '🏔️ Mt. Fuji view point: best from Moto-Hakone pier facing NW',
                '🌲 Old Tokaido cedar walk: 500-year-old cryptomeria avenue — atmospheric even in light rain'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Onsen Soak at Hakone Yuryo or Tenzan',
              description: "End the day in Japan's most primal pleasure: a rotenburo (outdoor onsen) with forest views. Hakone Yuryo has a beautiful cedar-scented open-air bath, and Tenzan is a larger bath complex with river sounds. The mineral waters here are volcanic and genuinely therapeutic.",
              details: [
                '♨️ Hakone Yuryo: beautiful cedar tubs, mixed forest setting, ¥1,300',
                '♨️ Tenzan Tohji-kyo: more rustic, riverside location, also excellent',
                '💡 Leave valuables at your hotel — bring just a small towel and wash fee',
                '🚫 Tattoo policy varies — check ahead if you have visible tattoos'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Dinner',
              name: 'Hakone Tozan Railway Station Restaurants',
              description: "If staying overnight in Hakone, many ryokan include a kaiseki dinner — a 10-course parade of seasonal Japanese cuisine in your room. Worth paying for at least one night if budget allows.",
              meta: '💰 ¥8,000–15,000pp for full kaiseki ryokan dinner'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.2306, lng: 139.1063, label: 'Hakone Open Air Museum', num: 1, cat: 'attraction', desc: 'Stunning outdoor sculpture park with Rodin and Picasso' },
        { lat: 35.2411, lng: 139.0239, label: 'Owakudani Volcanic Valley', num: 2, cat: 'attraction', desc: 'Active volcanic crater — steaming vents and black eggs' },
        { lat: 35.1927, lng: 139.0239, label: 'Lake Ashi / Moto-Hakone', num: 3, cat: 'attraction', desc: 'Crater lake with Mt. Fuji views and pirate ship cruise' },
        { lat: 35.2312, lng: 139.0700, label: 'Hakone Yuryo Onsen', num: 4, cat: 'attraction', desc: 'Cedar-tub outdoor onsen in the Hakone forest' },
        { lat: 35.2325, lng: 139.1068, label: 'Gora', num: 5, cat: 'attraction', desc: 'Hakone\'s mountain village — ryokan hub and garden walks' }
      ]
    },
    {
      num: 7,
      date: '2026-05-19',
      neighborhoods: 'Kyoto Station · Gion · Pontocho',
      title: 'Shinkansen to Kyoto — Geisha District & River Dining',
      description: "Board the Nozomi Shinkansen and arrive in Kyoto in under 2.5 hours. Check into your ryokan or boutique hotel, then spend the evening in Japan's most beautiful city on foot — through Gion's lantern-lit lanes and Pontocho's riverside dining alley.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinkansen to Kyoto',
              description: "The bullet train to Kyoto is a journey worth savouring — grab an ekiben (station bento) from Odawara or Tokyo Station and watch the Japanese countryside blur past. If the weather is clear, Mt. Fuji appears on the left side around Shin-Fuji Station.",
              details: [
                '🚄 Nozomi from Shinagawa or Tokyo Station: 2h 15min to Kyoto',
                '🍱 Tokyo Station Ekiben: buy a bento from the lower level — premium quality',
                '🏔️ Mt. Fuji view: sit on the left side (seats A/B/C) heading to Kyoto'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Gion District Walk',
              description: "Gion is Japan's most famous geisha district — a neighborhood of preserved machiya wooden townhouses, stone-paved Hanamikoji Street, and the chance (with patience and luck) to spot a maiko (apprentice geisha) in full kimono hurrying to an appointment. Walk south through Ninenzaka and Sannenzaka cobblestone lanes.",
              details: [
                '👘 Wear or rent a kimono — several rental shops in Gion, from ¥3,000',
                '📸 Hanamikoji Street: the most photogenic lane in Japan — best at dusk',
                '⚠️ Do NOT block or photograph geiko/maiko without permission — signage is clear',
                '🏮 Yasaka Shrine at the top of Gion: beautiful at twilight'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Pontocho Alley at Night',
              description: "Pontocho is a single narrow alley running parallel to the Kamogawa River — 80+ restaurants and bars stacked in ancient wooden buildings. In summer, restaurants extend platforms (yuka) over the river. The combination of lantern light, flowing water, and the smell of charcoal grills is pure Kyoto.",
              details: [
                '🌊 Kawayuka river platforms: available late May–September, book for dinner',
                '🏮 Walk the full length before choosing a restaurant — peek at menus and atmosphere',
                '💡 Mid-alley restaurants tend to be better than the ends (tourist traps)'
              ]
            }
          ],
          meals: [
            {
              type: '🍶 Dinner',
              name: 'Yoshiya, Pontocho',
              description: "One of Kyoto's most respected kappo restaurants — watch the chef prepare your multi-course meal at the open counter. Sashimi, tempura, seasonal kyō-kaiseki dishes, and excellent sake. The river view makes it perfect.",
              meta: '💰 ¥6,000–12,000pp · 📍 Pontocho Alley · Reserve ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9858, lng: 135.7588, label: 'Kyoto Station', num: 1, cat: 'transport', desc: 'Stunning Hiroshi Hara-designed station — your Kyoto hub' },
        { lat: 35.0036, lng: 135.7759, label: 'Hanamikoji Street, Gion', num: 2, cat: 'attraction', desc: 'Most photogenic lane in Japan — geisha district heart' },
        { lat: 35.0010, lng: 135.7794, label: 'Ninenzaka & Sannenzaka', num: 3, cat: 'attraction', desc: 'Ancient cobblestone lanes with preserved wooden shophouses' },
        { lat: 35.0037, lng: 135.7734, label: 'Pontocho Alley', num: 4, cat: 'food', desc: 'Narrow lantern-lit alley of restaurants over the Kamogawa River' },
        { lat: 35.0041, lng: 135.7724, label: 'Yoshiya Restaurant', num: 5, cat: 'food', desc: 'Traditional kappo kaiseki with river platform seating' },
        { lat: 35.0039, lng: 135.7786, label: 'Yasaka Shrine', num: 6, cat: 'attraction', desc: 'Ancient shrine at the heart of Gion — magical at twilight' }
      ]
    },
    {
      num: 8,
      date: '2026-05-20',
      neighborhoods: 'Fushimi Inari · Nishiki Market · Downtown Kyoto',
      title: 'The Thousand Torii Gates & Kyoto\'s Kitchen',
      description: "Climb Fushimi Inari's mountain of vermilion gates before the crowds arrive, then descend to Kyoto's downtown for lunch at the ancient Nishiki Market food lane and an afternoon browsing Teramachi Street's antique shops and kissaten cafés.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Fushimi Inari Taisha — Dawn Hike',
              description: "Arrive at Fushimi Inari by 6am (it never closes) to hike through thousands of vermilion torii gates in almost complete solitude. The full hike to the summit and back takes 2–3 hours through dense cedar forest, ascending past smaller shrines, stone fox statues, and increasingly eerie atmospheric silence.",
              details: [
                '⛩️ Free entry, open 24 hours — early morning is essential for the magic',
                '🦊 Foxes (kitsune) are the shrine\'s messengers — spot them in many forms along the path',
                '⏰ The first large gate tunnel: 15 min walk from the main gate',
                '🥾 Wear proper shoes — the path gets steep and stone after the first half'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Most tourists stop at the first two gate tunnels (30 min in). Keep climbing — the real magic and the view of Kyoto is from Yotsutsuji intersection, about halfway up.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nishiki Market — Kyoto\'s Kitchen',
              description: "Nishiki is a 400-year-old indoor market lane of 100+ stalls — pickled vegetables, fresh tofu, grilled skewers, green tea mochi, and seasonal Kyoto produce. Walk end-to-end eating as you go: this is the most concentrated foodie experience in Kyoto.",
              details: [
                '🥒 Tsukemono (pickled vegetables): try the yuzu and miso varieties',
                '🍡 Yuba (tofu skin) on a stick: the definitive Kyoto street food',
                '🍵 Matcha everything: soft serve, mochi, chocolate — Kyoto matcha is the standard',
                '🐙 Takoyaki from the stall near the west entrance: fresh, crispy, molten inside'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Tofu Kaiseki at Tousuiro',
              description: "Kyoto is famous for shojin ryori (Buddhist vegetarian) and yudofu (tofu hot pot). Tousuiro in central Kyoto does a beautiful tofu kaiseki lunch — silken tofu in various preparations with seasonal vegetable sides. Delicate, nourishing, and unlike anything outside Japan.",
              meta: '💰 ¥4,000–8,000 · 📍 Nakagyō-ku, Kyoto · Reserve ahead'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Teramachi Street & Kyoto Crafts',
              description: "Teramachi-dori is a covered shopping street blending antique dealers, incense shops, calligraphy supply stores, and traditional confectionery. Browse for authentic omiyage (souvenirs): Kyoto pickles, washi paper, ceramic sake cups, or a piece of Japanese lacquerware.",
              details: [
                '🏺 Antique shops cluster at the north end of Teramachi — quality pieces at fair prices',
                '🕯️ Yamakien: the most atmospheric incense shop — staff let you sample dozens of scents',
                '🍵 Kagizen Yoshifusa: Kyoto\'s most respected wagashi sweets shop since 1711'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari Taisha', num: 1, cat: 'attraction', desc: '10,000 torii gates on a sacred mountain — arrive at dawn' },
        { lat: 34.9950, lng: 135.7661, label: 'Nishiki Market', num: 2, cat: 'food', desc: '400-year-old indoor food market — Kyoto\'s Kitchen' },
        { lat: 34.9971, lng: 135.7690, label: 'Tousuiro Restaurant', num: 3, cat: 'food', desc: 'Exquisite Kyoto tofu kaiseki in the city center' },
        { lat: 35.0062, lng: 135.7684, label: 'Teramachi Street', num: 4, cat: 'attraction', desc: 'Covered street of antiques, incense, and Kyoto crafts' },
        { lat: 34.9961, lng: 135.7705, label: 'Kagizen Yoshifusa', num: 5, cat: 'food', desc: 'Kyoto\'s most revered wagashi sweet shop since 1711' }
      ]
    },
    {
      num: 9,
      date: '2026-05-21',
      neighborhoods: 'Arashiyama · Tenryu-ji · Kinkaku-ji',
      title: 'Arashiyama Bamboo & the Golden Pavilion',
      description: "Kyoto's most iconic day: the rustling Arashiyama Bamboo Grove, a riverside boat through forested gorge, the UNESCO-listed Zen garden of Tenryu-ji, and the breathtaking Golden Pavilion reflected in its mirror pond.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Arashiyama Bamboo Grove',
              description: "The bamboo grove at Arashiyama is one of Japan's most surreal natural experiences — a path through towering stalks that creak and sway in the wind, filtering green light and creating an almost musical rustling. Arrive at 6:30am for solitude; by 9am the path is crowded.",
              details: [
                '🎋 Free to walk through · Open always · Arrive by 7am for magic',
                '📸 The best photo: standing dead-center in the path looking into the green tunnel',
                '🚲 Rent a bike from the station — Arashiyama is excellent cycling territory'
              ]
            },
            {
              title: 'Tenryu-ji Zen Garden',
              description: "One of Japan\'s most perfect dry garden compositions — a ¥14th-century landscape of raked gravel, shaped pines, and a central pond designed by Musō Soseki. The garden was designed to \"borrow\" the Arashiyama mountains as its backdrop.",
              details: [
                '🏮 Entry ¥500 (garden) or ¥1,000 (includes main hall) — worth the full entry',
                '🌸 May: fresh green maple leaves contrast beautifully with the raked stone',
                '🍵 Cafe inside the temple grounds serves matcha and wagashi — perfect rest stop'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Hozu River Gorge Boat Ride',
              description: "Board a traditional wooden boat at Kameoka and drift 16km downstream through the stunning Hozu River gorge — forested cliffs, white water rapids, and ancient villages. Skilled boatmen navigate the rapids with long poles. It\'s exhilarating and deeply scenic.",
              details: [
                '⛵ Book via Sagano Scenic Railway + Hozu River Cruise combo',
                '⏰ The cruise takes 2 hours — wear layers, it\'s cooler on the water',
                '🦅 Watch for herons and cormorants fishing in the clear mountain river'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Shigetsu, Tenryu-ji',
              description: "Authentic shojin ryori (Zen Buddhist cuisine) inside the Tenryu-ji temple complex. Monks have prepared this vegetarian feast for centuries — seasonal tofu, wild mushrooms, pickles, and dashi. A meditative meal.",
              meta: '💰 ¥5,000–8,000 · 📍 Inside Tenryu-ji temple grounds · Reserve ahead'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Kinkaku-ji — The Golden Pavilion',
              description: "Kinkaku-ji is covered in real gold leaf and reflects perfectly in its mirror pond at sunset — it genuinely looks unreal. Arrive in the late afternoon when the light turns warm gold and the tourist crush slightly thins.",
              details: [
                '💛 Entry ¥400 · Open until 5pm',
                '📸 One photograph spot — you\'ll be ushered along — but it\'s magnificent',
                '🏮 The path continues through a lovely garden with a tea house'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Kyoto Ramen Koji (Ramen Street in Kyoto Station)',
              description: "Kyoto Station\'s basement ramen street has 8 legendary regional ramen shops — you\'ll find Kyoto\'s creamy chicken-soy (tori paitan) here alongside Sapporo miso and Fukuoka tonkotsu. Easy, cheap, and excellent after a big walking day.",
              meta: '💰 ¥900–1,300/bowl · 📍 B1F Kyoto Station Tower'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0174, lng: 135.6724, label: 'Arashiyama Bamboo Grove', num: 1, cat: 'attraction', desc: 'Japan\'s most magical bamboo forest — arrive at dawn' },
        { lat: 35.0171, lng: 135.6761, label: 'Tenryu-ji Garden', num: 2, cat: 'attraction', desc: 'UNESCO Zen garden with borrowed mountain landscape' },
        { lat: 35.0174, lng: 135.6765, label: 'Shigetsu Restaurant', num: 3, cat: 'food', desc: 'Shojin ryori Buddhist cuisine inside Tenryu-ji' },
        { lat: 35.0394, lng: 135.7292, label: 'Kinkaku-ji (Golden Pavilion)', num: 4, cat: 'attraction', desc: 'Gold-leafed Zen pavilion reflected in its mirror pond' },
        { lat: 35.1013, lng: 135.5689, label: 'Hozu River Gorge (Kameoka)', num: 5, cat: 'attraction', desc: 'Dramatic wooden boat ride through forested river gorge' }
      ]
    },
    {
      num: 10,
      date: '2026-05-22',
      neighborhoods: 'Nara · Tōdai-ji · Kasuga-taisha',
      title: 'Nara Day Trip — Wild Deer, Giant Buddha & Ancient Shrines',
      description: "45 minutes from Kyoto, Nara was Japan's first permanent capital and still feels like a place out of time — 1,000+ deer roam freely through the ancient park, bowing for crackers and photobombing tourists with total indifference.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Nara Deer Park & Tōdai-ji Temple',
              description: "Nara's deer (called shika) are considered divine messengers and have the run of the park. They\'ll bow for shika-senbei crackers (sold everywhere) and are gentle despite being totally wild. Tōdai-ji is home to Japan's largest bronze Buddha — 15 meters high inside the world\'s largest wooden building.",
              details: [
                '🦌 Deer crackers: ¥200/bundle from vendors — keep your bag zipped, deer are bold',
                '🏛️ Tōdai-ji entry ¥600 — the Great Buddha Hall (Daibutsuden) is genuinely awe-inspiring',
                '🕳️ The wooden pillar with the hole: legend says those who can squeeze through will be blessed'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast/Coffee',
              name: 'Kintetsu Nara Station Cafés',
              description: "Grab coffee and morning pastries from the cafés near Kintetsu Nara Station before diving into the park. Japanese conbini also have excellent morning options if the cafés are crowded.",
              meta: '💰 ¥500–800 · 📍 Kintetsu Nara Station area'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kasuga-taisha Shrine & Isuien Garden',
              description: "Kasuga Grand Shrine is one of Japan's most important Shinto complexes, famous for its 3,000 hanging lanterns lit twice a year. The forested approach through 1,000-year-old cryptomeria is haunting and beautiful. Isuien Garden next door is a classical Japanese landscape garden with borrowed Tōdai-ji scenery.",
              details: [
                '⛩️ Kasuga-taisha outer grounds: free · Inner sanctuary: ¥500',
                '🌿 Isuien Garden: ¥900 — one of Japan\'s most beautiful Meiji-era gardens',
                '🏮 The lantern-lit forest path: atmosphere peaks in early morning or late afternoon'
              ]
            },
            {
              title: 'Naramachi Historic Merchant District',
              description: "Nara\'s former merchant quarter is a well-preserved grid of machiya townhouses now home to craft workshops, sake breweries, small galleries, and excellent lunch spots. A quieter, more authentic counterpoint to the deer park crowds.",
              details: [
                '🍶 Imanishi Sake Brewery: Nara has been making sake for 500 years — try a tasting flight',
                '🏺 Naramachi Koshi-no-ie: a restored machiya house museum, free entry'
              ]
            }
          ],
          meals: [
            {
              type: '🥢 Lunch',
              name: 'Menyanamidori, Naramachi',
              description: "A beloved local ramen shop in Naramachi serving Nara\'s regional style — milder, cleaner broth than Tokyo or Osaka. Counter seating and a warm welcome.",
              meta: '💰 ¥1,000–1,500 · 📍 Naramachi district'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Kyoto for Dinner',
              description: "Head back to Kyoto in time for a relaxed evening. Tonight is ideal for an early dinner in Gion and a twilight walk along the Shirakawa canal — one of Kyoto\'s most beautiful and least-visited evening scenes.",
              details: [
                '🌙 Shirakawa canal at dusk: the reflection of weeping willows and stone lanterns in the water — a Kyoto postcard',
                '🏮 Gion in the evening: the geiko and maiko are heading to appointments from around 5:30–6:30pm'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Izuju Sushi, Gion',
              description: "A Gion institution since 1940 serving Kyoto\'s unique saba oshi-zushi (pressed mackerel sushi) — the local style long before maki rolls existed. Counter seating, cedar fish smell, sake served old-school.",
              meta: '💰 ¥2,000–4,000 · 📍 Gion, Kyoto · Opens 11am'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6890, lng: 135.8398, label: 'Nara Deer Park', num: 1, cat: 'attraction', desc: '1,000 free-roaming sacred deer — bow for crackers' },
        { lat: 34.6888, lng: 135.8398, label: 'Tōdai-ji Temple', num: 2, cat: 'attraction', desc: 'World\'s largest wooden building with a 15-meter Great Buddha' },
        { lat: 34.6814, lng: 135.8493, label: 'Kasuga-taisha Shrine', num: 3, cat: 'attraction', desc: '3,000 lanterns, ancient cedar forest, Shinto pilgrimage site' },
        { lat: 34.6739, lng: 135.8378, label: 'Naramachi District', num: 4, cat: 'attraction', desc: 'Preserved merchant quarter with sake brewery and craft shops' },
        { lat: 34.6814, lng: 135.8418, label: 'Isuien Garden', num: 5, cat: 'attraction', desc: 'Classical Japanese garden with Tōdai-ji borrowed scenery' }
      ]
    },
    {
      num: 11,
      date: '2026-05-23',
      neighborhoods: 'Hiroshima · Peace Memorial Park · Miyajima Island',
      title: 'Hiroshima & Miyajima — Peace, Memory & the Floating Torii',
      description: "A day of profound beauty and reflection. The Peace Memorial Museum is one of the most important places on Earth. Then a ferry across to Miyajima — the \"Island of the Gods\" with its iconic orange torii gate rising from the sea.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Hiroshima Peace Memorial Park & Museum',
              description: "The A-Bomb Dome (Genbaku Dōmu) is the haunting skeleton of a building that survived the blast directly below the atomic bomb's detonation point — it stands exactly as it was on August 6, 1945. The Peace Memorial Museum is deeply moving, carefully presented, and essential. Allow at least 2 hours.",
              details: [
                '🕊️ A-Bomb Dome: free to view · Peace Park: free · Museum: ¥200',
                '🌸 The park\'s 10,000 trees create a peaceful, emotional landscape in May',
                '📖 Children\'s Peace Monument: 1,000 paper cranes — the Sadako story',
                '⏰ Take the Shinkansen from Kyoto (about 1h 40min on Nozomi)'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The Peace Memorial Museum is emotionally intense. Budget 2 full hours and take breaks in the park afterwards. It\'s one of the most important visits you\'ll ever make.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Miyajima Island — Floating Torii & Sacred Island',
              description: "A 15-minute ferry from Hiroshima brings you to Miyajima, where the great orange torii of Itsukushima Shrine appears to float in the sea at high tide. Deer (like Nara\'s) roam the island freely. Hike to the top of Mt. Misen for views across the Seto Inland Sea.",
              details: [
                '⛩️ Itsukushima Shrine entry ¥300 · Check tide times — high tide = floating torii',
                '🦌 Island deer are tamer than Nara\'s and equally camera-ready',
                '🏔️ Mt. Misen: ropeway (¥1,000 up) or 90-min hike — views are spectacular',
                '🦞 Miyajima\'s famous food: momiji manju (maple-leaf cakes) and grilled oysters'
              ]
            }
          ],
          meals: [
            {
              type: '🦪 Lunch',
              name: 'Grilled Oysters on Miyajima',
              description: "The Inland Sea around Miyajima is Japan\'s oyster heartland. The island\'s street stalls grill massive fresh oysters over open charcoal and hand them to you in their shells, steaming and briny. The most seasonal, local, and delicious possible meal.",
              meta: '💰 ¥300–500/oyster · 📍 Main shopping street, Miyajima'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Hiroshima Okonomiyaki District',
              description: "Hiroshima-style okonomiyaki is entirely different from the Osaka version — layers of noodles, cabbage, egg, and pork stacked and pressed on the teppan. Okonomi-mura (\"okonomiyaki village\") has three floors of restaurants dedicated to the dish. Watch your chef build it live.",
              details: [
                '🥞 Hiroshima okonomiyaki: noodles are the key difference from Osaka style',
                '🏢 Okonomi-mura: three floors, 25+ stalls — point and sit at any counter',
                '🍺 Cold Hiroshima Lemon beer pairs perfectly with the savory pancake'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.3955, lng: 132.4534, label: 'A-Bomb Dome', num: 1, cat: 'attraction', desc: 'UNESCO World Heritage atomic bomb survivor — Hiroshima' },
        { lat: 34.3916, lng: 132.4523, label: 'Peace Memorial Museum', num: 2, cat: 'attraction', desc: 'Profoundly important museum on the 1945 atomic bombing' },
        { lat: 34.2955, lng: 132.3198, label: 'Itsukushima Shrine, Miyajima', num: 3, cat: 'attraction', desc: 'Floating torii gate at high tide — one of Japan\'s three great views' },
        { lat: 34.2867, lng: 132.3223, label: 'Mt. Misen Ropeway', num: 4, cat: 'attraction', desc: 'Summit views over the Seto Inland Sea — spectacular on clear days' },
        { lat: 34.3983, lng: 132.4566, label: 'Okonomi-mura', num: 5, cat: 'food', desc: '25-stall building dedicated to Hiroshima-style okonomiyaki' }
      ]
    },
    {
      num: 12,
      date: '2026-05-24',
      neighborhoods: 'Osaka · Dotonbori · Namba · Kuromon Market',
      title: 'Welcome to Osaka — Eat Till You Can\'t',
      description: "Osaka lives by \"kuidaore\" — eat until you drop. Dotonbori\'s neon-soaked canal district is Japan\'s greatest street-food theater. From crab-claw signs to takoyaki on skewers to the freshest fish at Kuromon Market, today is a full-day feast.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Travel to Osaka & Kuromon Ichiba Market',
              description: "Shinkansen from Hiroshima (or morning train from Kyoto) gets you to Osaka by mid-morning. Drop your bags at the hotel then head straight to Kuromon Ichiba — Osaka\'s famous covered food market, known as \"Osaka\'s Kitchen.\" 170+ stalls selling the freshest local seafood, wagyu beef, and produce.",
              details: [
                '🐟 Kuromon Market: best 9am–noon before tour groups arrive',
                '🦐 Try the spot prawns, fugu (blowfish) sashimi, and grilled wagyu skewers',
                '🗺️ Stay near Namba or Shinsaibashi — ideal central location in Osaka'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Kuromon Market stalls',
              description: "Eat your way through the market: one stall for maguro sashimi on rice, another for grilled scallops, a third for fresh strawberries. Osaka market culture means every vendor wants you to taste before you buy.",
              meta: '💰 ¥1,500–3,000 to graze · 📍 Kuromon Ichiba Market'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Dotonbori — Osaka\'s Food Stage',
              description: "Walk the Dotonbori canal promenade and understand why Osaka is Asia\'s food city. The Glico Running Man, the giant mechanical crab claws, neon in every direction — it\'s maximalist and joyful. Find the original Takoyaki Juhachiban stall and watch the balls get filled and flipped.",
              details: [
                '🐙 Takoyaki: buy a plate of 8 at Wanaka, Juhachiban, or any stall — all excellent',
                '🦀 Kani Doraku restaurant: the giant mechanical crab arms on the facade have been turning since 1960',
                '🍣 Ganko Sushi: for a proper sit-down Osaka sushi lunch at fair prices'
              ]
            },
            {
              title: 'Shinsaibashi Shopping Arcade',
              description: "Japan\'s longest covered shopping arcade runs 600 meters through Shinsaibashi and Namba — Japanese fashion brands, cosmetics, sweets shops, and specialty stores. A perfect afternoon browse.",
              details: [
                '🛍️ Don Quijote (Donki): Osaka\'s famous discount megastore — a surreal Japanese retail experience',
                '💊 Matsumoto Kiyoshi: Japan\'s famous pharmacy chain — great for skincare, snacks, and collagen drinks'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dotonbori Neon Night Walk',
              description: "After dark, Dotonbori becomes even more theatrical — neon reflections in the canal, outdoor izakayas spilling onto the street, takoyaki smoke drifting between the crowds. Grab a Osaka kushikatsu (deep-fried skewers) at a counter bar and watch the city perform.",
              details: [
                '🍢 Kushikatsu: deep-fried skewers of meat, vegetables, and cheese — dip once only in the communal sauce (it\'s a rule)',
                '🌙 Ebisu Bridge: the best spot for selfies with the illuminated Glico Man sign'
              ]
            }
          ],
          meals: [
            {
              type: '🍢 Dinner',
              name: 'Daruma Kushikatsu, Dotonbori',
              description: "The original kushikatsu chain since 1929 — crispy panko-fried skewers of everything imaginable. The red-faced daruma mascot marks the entrance. Order the mixed set and work your way through the menu.",
              meta: '💰 ¥1,500–3,000 · 📍 Dotonbori, Chuo-ku'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6674, lng: 135.5052, label: 'Kuromon Ichiba Market', num: 1, cat: 'food', desc: 'Osaka\'s Kitchen — 170 stalls of the city\'s freshest food' },
        { lat: 34.6687, lng: 135.5011, label: 'Dotonbori Canal', num: 2, cat: 'attraction', desc: 'Osaka\'s neon-lit food and entertainment canal district' },
        { lat: 34.6686, lng: 135.5005, label: 'Glico Running Man Sign', num: 3, cat: 'attraction', desc: 'Osaka\'s most iconic landmark — Ebisu Bridge selfie spot' },
        { lat: 34.6721, lng: 135.5013, label: 'Shinsaibashi Shopping Arcade', num: 4, cat: 'attraction', desc: 'Japan\'s longest covered shopping street — 600 meters' },
        { lat: 34.6691, lng: 135.5019, label: 'Daruma Kushikatsu', num: 5, cat: 'food', desc: 'Osaka\'s original kushikatsu restaurant since 1929' }
      ]
    },
    {
      num: 13,
      date: '2026-05-25',
      neighborhoods: 'Osaka Castle · Shinsekai · Tennōji',
      title: 'Osaka Castle, Retro Shinsekai & the Wild Flavours of Tennōji',
      description: "Osaka Castle on a May morning is surrounded by green moats and crisp mountain views. Then descend to Shinsekai — a fascinatingly retro district of blowfish lamps, kushikatsu legends, and old-man pachinko parlors that time forgot.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Osaka Castle & Nishinomaru Garden',
              description: "Osaka Castle is the most visually dramatic castle in Japan — a gleaming white and green tower rising above massive stone walls and a double moat. In May the moat walls are vivid green from moss and wisteria. Climb the main keep for city-wide views and a history museum of the Warring States period.",
              details: [
                '🏯 Castle tower entry ¥600 · Nishinomaru Garden ¥200 · Open 9am–5pm',
                '📸 Best photo: from the stone bridge over the outer moat looking up at the tower',
                '⚔️ The 8-floor museum inside has samurai armor, weapons, and Toyotomi Hideyoshi\'s story',
                '🌿 May morning: the castle moat and garden are at their green-lush peak'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shinsekai — Osaka\'s Retro Quarter',
              description: "Built as a \'new world\' in 1912 modeled on Paris and Coney Island, Shinsekai fell into decline and then became beloved for its retro authenticity. It\'s now a neighborhood of Tsutenkaku Tower, fugu restaurant signs shaped like blowfish, classic pachinko parlors, and the most unpretentious kushikatsu in the city.",
              details: [
                '🏯 Tsutenkaku Tower: Osaka\'s original \'Eiffel Tower\' — the view is solid, the kitsch is excellent',
                '🦡 Lucky god statues called Billiken: rub his feet for good fortune',
                '🍢 Kushikatsu Daruma Shinsekai branch: the atmosphere in this neighborhood version is unbeatable'
              ]
            }
          ],
          meals: [
            {
              type: '🥢 Lunch',
              name: 'Kushikatsu Matsui, Shinsekai',
              description: "A longtime Shinsekai institution — standing room at the counter, beer in a glass mug, and a parade of skewered and fried things emerging from the fryer. Order by pointing. This is Osaka as it was meant to be experienced.",
              meta: '💰 ¥1,500–2,500 · 📍 Shinsekai, Naniwa-ku'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Tennōji & Abeno Harukas Sky View',
              description: "Tennōji is one of Osaka\'s most authentic and underrated neighborhoods — locals shopping, the stunning Tennōji Zoo and botanical garden, and Abeno Harukas (Japan\'s tallest building, 300m) with a twilight observation deck that captures the entire Osaka-Kyoto-Kobe megalopolis glowing at dusk.",
              details: [
                '🏙️ Harukas 300 observation deck: ¥1,800 · Open until 10pm — twilight is spectacular',
                '🌳 Tennōji Kōen (park) and botanical garden: beautiful and surprisingly uncrowded',
                '📍 Tennōji is also a great neighborhood for cheap, authentic ramen and izakaya'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Ichifuji Ramen, Tennōji',
              description: "A local Tennōji ramen shop serving thick chicken-soy broth in the Osaka style. Counter seats, wooden bowls, big portions. The kind of place that defines neighborhood eating in Japan.",
              meta: '💰 ¥800–1,200 · 📍 Tennōji area'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6873, lng: 135.5262, label: 'Osaka Castle', num: 1, cat: 'attraction', desc: 'Japan\'s most dramatic castle with double moat and green tower' },
        { lat: 34.6520, lng: 135.5059, label: 'Shinsekai', num: 2, cat: 'attraction', desc: '1912 retro district — Tsutenkaku Tower and kushikatsu country' },
        { lat: 34.6526, lng: 135.5061, label: 'Tsutenkaku Tower', num: 3, cat: 'attraction', desc: 'Osaka\'s retro Eiffel Tower — Billiken god statues inside' },
        { lat: 34.6461, lng: 135.5135, label: 'Tennōji / Abeno Harukas', num: 4, cat: 'attraction', desc: 'Japan\'s tallest building — twilight sky deck at 300m' },
        { lat: 34.6524, lng: 135.5057, label: 'Kushikatsu Matsui', num: 5, cat: 'food', desc: 'Counter kushikatsu institution in the heart of Shinsekai' }
      ]
    },
    {
      num: 14,
      date: '2026-05-26',
      neighborhoods: 'Umeda · Osaka Station · Dotombori (Farewell)',
      title: 'Final Osaka Morning — Department Store Food Halls & Sayōnara',
      description: "Your last full day in Japan. The Umeda underground city for a final coffee ritual, Osaka\'s legendary department store basement food halls (depachika) for the most beautiful take-away picnic imaginable, and a final farewell walk along the Dotonbori canal as the city wakes up.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Umeda Underground City & Morning Coffee',
              description: "Osaka\'s Umeda district has one of the world\'s great underground shopping complexes — kilometers of passages connecting shopping malls, restaurants, and stations. Find a standing coffee bar for espresso alongside the morning commuter rush, then emerge into the daylight at Hankyu Department Store.",
              details: [
                '☕ Drip coffee (standing): find any kissaten-style standing bar in Umeda underground',
                '🏬 Hankyu Umeda: the store\'s architecture alone is worth the visit — soaring atrium',
                '🗺️ The Osaka underground: download a map before you go — it\'s genuinely labyrinthine'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Depachika: Japan\'s Greatest Food Basements',
              description: "The depachika (department store basement food halls) of Umeda are the most civilized food shopping in the world. Daimaru, Isetan, Hankyu — each has basement floors of pristine pastry cases, bento art, fresh wagashi, premium pickles, and individually wrapped gifts. This is your final souvenir and omiyage opportunity.",
              details: [
                '🎁 Omiyage gifts to bring home: Royce chocolate, Shiroi Koibito cookies, wasabi KitKats, Kyoto pickles',
                '🍱 Build the perfect picnic bento: rice balls, tamago, grilled fish, fresh fruit — for the flight or a final park sit',
                '🍰 Osaka-specific: try Dorayaki filled with matcha cream — the local style'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Farewell Lunch',
              name: 'Depachika picnic in Nakanoshima Park',
              description: "Collect your ideal items from the department store food hall and take them to Nakanoshima Park — a long island in the middle of the Osaka river, lined with trees and the sound of water. Your last Japanese meal in the most Japanese of settings.",
              meta: '💰 ¥2,000–4,000 · 📍 Nakanoshima Park, Kita-ku'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Dotonbori Walk & Farewell Drinks',
              description: "One last walk through Dotonbori as the evening lights come on. Find a riverside table at one of the open-air cafés over the canal, order a cold Asahi and look back at 14 days of bullet trains, bamboo forests, onsen, volcanic craters, deer, ramen, and wonder.",
              details: [
                '🌆 Best twilight spot: the terrace at Café de Crié Dotonbori, overlooking the canal',
                '🍺 Order an Osaka tower beer (those tall glasses) and toast properly',
                '✈️ Kansai International Airport (KIX): 30–45min by train from Namba — allow plenty of time'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Mizuno Okonomiyaki, Dotonbori',
              description: "Your final meal in Japan should feel like a celebration. Mizuno has served Osaka-style okonomiyaki since 1945 — you mix and cook it yourself on the table grill. Simple, fun, absolutely delicious, and a perfect last-night memory.",
              meta: '💰 ¥1,500–2,500/person · 📍 Dotonbori 1-4-15 · Queue expected'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.7024, lng: 135.4959, label: 'Hankyu Umeda / Depachika', num: 1, cat: 'food', desc: 'Osaka\'s greatest department store basement food hall' },
        { lat: 34.6904, lng: 135.5053, label: 'Nakanoshima Park', num: 2, cat: 'attraction', desc: 'River island park — perfect for a final Japanese picnic' },
        { lat: 34.6687, lng: 135.5011, label: 'Dotonbori Canal (farewell)', num: 3, cat: 'attraction', desc: 'Final evening walk through Osaka\'s neon heart' },
        { lat: 34.6691, lng: 135.5013, label: 'Mizuno Okonomiyaki', num: 4, cat: 'food', desc: 'DIY okonomiyaki since 1945 — perfect farewell dinner' },
        { lat: 34.4347, lng: 135.2440, label: 'Kansai International Airport (KIX)', num: 5, cat: 'transport', desc: 'Departure airport — 30–45 min from Namba by train' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '¥8,000–12,000/night', midrange: '¥12,000–25,000/night', luxury: '¥25,000–60,000/night' },
    { category: 'Meals (per couple)', budget: '¥3,000–5,000/day', midrange: '¥6,000–12,000/day', luxury: '¥15,000–40,000/day' },
    { category: 'Transport (JR Pass)', budget: '¥50,000 14-day pass (both)', midrange: '¥50,000 + IC cards', luxury: '¥50,000 + private car' },
    { category: 'Activities & Museums', budget: '¥1,000–2,000/day', midrange: '¥2,000–5,000/day', luxury: '¥5,000–15,000/day' },
    { category: 'Onsen / Experiences', budget: '¥500–1,500/session', midrange: '¥3,000–8,000/night ryokan', luxury: '¥15,000–40,000/night ryokan' },
    { category: '14-Night Total (couple)', budget: '$1,800–2,500', midrange: '$3,500–6,000', luxury: '$8,000–18,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Tokyo Narita (NRT) or Haneda (HND)', 'Buy a 14-day JR Pass before leaving home (must purchase outside Japan)', 'Narita Express to Shinjuku: 80 min, covered by JR Pass', 'Arrive rested — hit the ground running is the Japan way'] },
    { title: '🚄 Trains & Getting Around', items: ['JR Pass covers all Shinkansen (except Nozomi/Mizuho — use Hikari instead)', 'IC card (Suica/Pasmo): tap-on for subways, buses, convenience stores', 'Google Maps Japan is extremely reliable for transit directions', 'Taxis are expensive — train and walking covers 95% of needs'] },
    { title: '🌡️ May Weather', items: ['Tokyo: 18–25°C, mostly sunny, occasional rain', 'Kyoto: similar, slightly warmer, green-season foliage is stunning', 'Osaka: 20–27°C, comfortable sightseeing weather', 'Pack light layers, a rain jacket, and good walking shoes'] },
    { title: '💴 Money Tips', items: ['Withdraw yen at 7-Eleven ATMs — most reliable for foreign cards', 'Daily budget ¥5,000–8,000/person covers meals, transit, and sights', 'Carry cash: many small restaurants, temples, and markets are cash-only', 'Never tip — it\'s not part of Japanese culture and can cause confusion'] },
    { title: '📱 Apps & Essentials', items: ['Google Translate (camera mode for menus)', 'Japan Official Travel App for offline maps and transit', 'Tabelog for finding local restaurants (Japanese Yelp)', 'Download the Suica app for digital IC card on iPhone'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
