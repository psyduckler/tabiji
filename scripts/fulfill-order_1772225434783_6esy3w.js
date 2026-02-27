const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772225434783_6esy3w',
  email: 'paulhblasjr@gmail.com',
  destination: 'Tokyo, Osaka, Kyoto',
  startDate: '2026-05-15',
  endDate: '2026-05-24',
  groupSize: 5,
  requests: '3 adults, two children ages 3 and 2, no pork, Tokyo May 15-19, Osaka base + Kyoto May 20-24, fit in as much as possible, no Gundam'
};

const itineraryData = {
  destination: 'Tokyo, Osaka & Kyoto, Japan',
  countryEmoji: '🇯🇵',
  title: 'Japan with Little Ones: Tokyo, Osaka & Kyoto',
  subtitle: '10 days of temples, street food & toddler-friendly adventure across three iconic cities',
  description: "This family adventure spans Japan's three greatest cities — five days exploring Tokyo's interactive museums, serene gardens, and dazzling neighbourhoods, then five days based in Osaka with day trips to Kyoto's bamboo groves and golden temples. Every activity is toddler-tested, every restaurant is pork-free, and the pace balances big experiences with naptime. Strollers roll easily on Japan's smooth sidewalks, train stations have elevators everywhere, and the whole country adores small children.",
  duration: '10 nights',
  dates: 'May 15 – May 24, 2026',
  budget: '$$–$$$',
  pace: 'Moderate with flex',
  bestFor: 'Families with toddlers',
  highlights: [
    'teamLab Borderless — immersive digital art toddlers love',
    'Senso-ji Temple at sunrise with zero crowds',
    'Tsukiji Outer Market — fresh seafood & tamagoyaki on sticks',
    'Osaka Aquarium Kaiyukan — one of the world\'s largest',
    'Arashiyama Bamboo Grove & monkey park in Kyoto',
    'Fushimi Inari\'s thousand vermillion torii gates',
    'Dotonbori street food crawl — takoyaki, yakitori & yakisoba',
    'Nara\'s friendly bowing deer with the kids'
  ],

  essentials: [
    { title: '👶 Traveling with Toddlers', text: 'Japan is incredibly toddler-friendly. Trains have priority seating, stations have elevators, and most department stores have nursing rooms (赤ちゃん休憩室). Bring a lightweight stroller — sidewalks are smooth and ramps are everywhere. Convenience stores (konbini) carry diapers, baby food, and snacks 24/7.' },
    { title: '🚆 Getting Around', text: 'Get a 5-day Japan Rail Pass for the Tokyo leg, then activate a second pass or buy individual Shinkansen tickets for the Osaka/Kyoto portion. In cities, use IC cards (Suica/ICOCA) for subway and buses — tap-on, tap-off. Kids under 6 ride free on trains.' },
    { title: '🐷 No Pork Guide', text: 'Japanese cuisine uses pork in unexpected places — dashi broth, gyoza, ramen, even some curry. This itinerary sticks to seafood, chicken, beef, and vegetable dishes. At restaurants, say "buta nashi de onegaishimasu" (豚なしでお願いします) — no pork please. Yakitori (chicken skewers), sushi, tempura, and udon are naturally safe bets.' },
    { title: '☀️ May Weather', text: 'Mid-May in Japan is gorgeous — 20-25°C, low humidity, occasional rain. Cherry blossom season is over but fresh green leaves and azaleas are stunning. Pack layers, a rain jacket, and sun hats for the kids.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-05-15',
      neighborhoods: 'Asakusa · Sumida · Skytree',
      title: 'Welcome to Tokyo — Temples & Towers',
      description: "Land in Tokyo and dive straight into the magic. Start with the ancient Senso-ji Temple, wander Nakamise shopping street for treats, then take in the city from the towering Skytree. The kids will love the bustle and the taiyaki (fish-shaped cakes).",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Senso-ji Temple & Nakamise Street',
              description: "Tokyo's oldest temple is stunning and toddler-friendly — wide open courtyards, colourful gates, and Nakamise-dori lined with snack stalls. Let the kids ring the bell and waft incense smoke (said to bring good health).",
              details: [
                '⛩️ The massive Kaminarimon (Thunder Gate) is the iconic photo spot',
                '🍡 Grab ningyo-yaki (custard-filled cakes) and senbei (rice crackers) along Nakamise',
                '👶 Wide, flat paths — easy stroller access throughout'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Arrive by 2-3pm to beat crowds. The temple grounds are open 24/7, but shops close around 5pm.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Tokyo Skytree',
              description: "Japan's tallest structure (634m) has two observation decks with panoramic city views. The Tembo Galleria at 450m has a spiralling glass corridor that toddlers find thrilling. The base has a shopping complex with kid-friendly restaurants.",
              details: [
                '🗼 Book tickets online to skip the queue',
                '🌆 Sunset timing (around 6:30pm in May) is magical',
                '🛍️ Solamachi mall at the base has a Pokémon Center and an aquarium'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Sometarō (Asakusa)',
              description: "Cook-your-own okonomiyaki (savoury pancakes) on a tabletop grill — kids love the interactive experience. Order seafood or vegetable versions — no pork on request. A fun, affordable, and memorable first dinner in Tokyo.",
              meta: '💰 $$ · 📍 2-2-2 Nishi-Asakusa, Taito · No pork available'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: 'Senso-ji Temple', num: 1, cat: 'attraction', desc: "Tokyo's oldest temple with Nakamise shopping street" },
        { lat: 35.7101, lng: 139.8107, label: 'Tokyo Skytree', num: 2, cat: 'attraction', desc: "Japan's tallest tower — 634m with observation decks" },
        { lat: 35.7131, lng: 139.7955, label: 'Sometarō', num: 3, cat: 'food', desc: 'DIY okonomiyaki — seafood & veggie, no pork' }
      ]
    },
    {
      num: 2,
      date: '2026-05-16',
      neighborhoods: 'Odaiba · Toyosu · Tsukiji',
      title: 'Digital Art, Fish Markets & Island Fun',
      description: "A day of sensory wonder — teamLab Borderless's immersive digital art, fresh seafood at the markets, and Odaiba's futuristic waterfront. Toddlers go wild at teamLab, and the markets have endless pork-free snacking.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'teamLab Borderless (Azabudai Hills)',
              description: "One of the world's most spectacular digital art museums. Toddlers are mesmerized by rooms of flowing light, interactive flowers that bloom at their feet, and waterfalls they can touch. The entire experience is barefoot-friendly and stroller-accessible.",
              details: [
                '🎨 Book tickets online weeks ahead — sells out fast',
                '⏰ Go at opening (10am) for smallest crowds',
                '👶 Toddlers can touch everything — it responds to movement',
                '📸 Wear white clothing for the best photo effects'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tsukiji Outer Market',
              description: "The original fish market's outer stalls are still thriving — a sensory wonderland of fresh seafood, tamagoyaki (sweet egg omelette), grilled scallops, and fresh fruit. Everything is pork-free by nature, and kids love eating on sticks.",
              details: [
                '🐟 Must-try: tamagoyaki on a stick, grilled king crab legs, fresh uni',
                '🍣 Sushi Dai and other stalls offer kid-friendly tamago (egg) sushi',
                '🧃 Fresh melon juice and strawberry mochi for the little ones'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Tsukiji Market Grazing',
              description: 'Skip a sit-down lunch and graze your way through the market. Tamagoyaki, grilled seafood, fresh fruit — all pork-free, all kid-friendly, all delicious.',
              meta: '💰 $ · 📍 Tsukiji Outer Market · Open until ~2pm'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Odaiba Waterfront',
              description: "Cross the Rainbow Bridge to Odaiba — a futuristic island with beaches, parks, and a giant Unicorn Gundam statue (the kids can look at the buildings instead!). The seaside park has a small sandy beach where toddlers can play with Tokyo Bay views.",
              details: [
                '🏖️ Odaiba Seaside Park has a sandy beach for the kids',
                '🌉 Rainbow Bridge views are stunning at sunset',
                '🛍️ DiverCity and Aqua City malls have family restaurants'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Bills Odaiba',
              description: "The famous Australian café serves excellent ricotta hotcakes, grilled chicken, and seafood — all naturally pork-free. Great kids' menu and high chairs available. Harbour views from the terrace.",
              meta: '💰 $$$ · 📍 DiverCity Tokyo Plaza, Odaiba'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6596, lng: 139.7312, label: 'teamLab Borderless', num: 1, cat: 'attraction', desc: 'Immersive digital art museum — toddler paradise' },
        { lat: 35.6654, lng: 139.7707, label: 'Tsukiji Outer Market', num: 2, cat: 'food', desc: 'Fresh seafood stalls — tamagoyaki, grilled scallops' },
        { lat: 35.6269, lng: 139.7753, label: 'Odaiba Seaside Park', num: 3, cat: 'attraction', desc: 'Waterfront park with sandy beach and Rainbow Bridge views' },
        { lat: 35.6252, lng: 139.7754, label: 'Bills Odaiba', num: 4, cat: 'food', desc: 'Australian café — ricotta hotcakes & grilled seafood' }
      ]
    },
    {
      num: 3,
      date: '2026-05-17',
      neighborhoods: 'Shinjuku · Shinjuku Gyoen · Meiji Shrine',
      title: 'Gardens, Shrines & Shinjuku Lights',
      description: "A day that balances serenity with spectacle. Morning at the peaceful Meiji Shrine forest, a picnic in Shinjuku Gyoen's sprawling gardens (perfect for toddler running), then the neon explosion of Shinjuku at night.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Meiji Shrine (Meiji Jingū)',
              description: "Walk through the towering torii gate into a 170-acre forest in the heart of Tokyo. The gravel paths through ancient trees feel like entering another world. Toddlers love the wide open spaces, and you might catch a traditional wedding procession.",
              details: [
                '⛩️ The 12m-tall torii gate at the entrance is made from 1,500-year-old cypress',
                '🌳 The forest was planted in 1920 and now feels ancient',
                '👶 Wide gravel paths — strollers work but a carrier is easier',
                '🙏 Write a wish on an ema (wooden plaque) at the shrine'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shinjuku Gyoen National Garden',
              description: "One of Tokyo's finest parks — 144 acres of Japanese, French, and English gardens. In May, the roses are blooming and the lawns are perfect for a family picnic. Toddlers can run free on the vast open meadows while you admire the greenhouse's tropical plants.",
              details: [
                '🌹 Rose garden in full bloom in mid-May',
                '🧺 Bring a picnic from a nearby konbini — no alcohol allowed in the park',
                '🏃 Huge open lawns where toddlers can run safely',
                '🌺 The greenhouse has tropical plants and is stroller-friendly'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Afuri Ramen (Shinjuku)',
              description: "Famous for their yuzu shio (citrus salt) ramen made with chicken broth — naturally pork-free. Light, fragrant, and kid-friendly. They have a dedicated no-pork menu. One of Tokyo's best ramen experiences without any pork.",
              meta: '💰 $$ · 📍 Shinjuku area · Chicken-based broth, no pork'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shinjuku at Night',
              description: "As darkness falls, Shinjuku transforms into a neon wonderland. Walk through Kabukichō's dazzling signs (family-safe on the main streets), peek into the tiny bars of Golden Gai from outside, and let the kids marvel at the lights. The Robot Restaurant area is pure visual spectacle even from the street.",
              details: [
                '🌃 The east side of Shinjuku Station is the neon epicentre',
                '📸 Godzilla head on top of Hotel Gracery — kids love spotting it',
                '🚶 Stick to main streets with toddlers — perfectly safe and well-lit'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Toriyoshi (Shinjuku)',
              description: "An excellent yakitori (chicken skewer) restaurant — every item is chicken, so zero pork risk. Juicy grilled skewers, crispy chicken wings, and chicken meatballs that kids devour. Casual and lively atmosphere.",
              meta: '💰 $$ · 📍 Shinjuku · All chicken, no pork'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6764, lng: 139.6993, label: 'Meiji Shrine', num: 1, cat: 'attraction', desc: 'Serene Shinto shrine in a 170-acre forest' },
        { lat: 35.6852, lng: 139.7100, label: 'Shinjuku Gyoen', num: 2, cat: 'attraction', desc: 'Vast gardens with rose garden and open lawns' },
        { lat: 35.6938, lng: 139.7036, label: 'Afuri Ramen', num: 3, cat: 'food', desc: 'Yuzu chicken ramen — naturally pork-free' },
        { lat: 35.6945, lng: 139.7005, label: 'Shinjuku Neon District', num: 4, cat: 'attraction', desc: 'Kabukichō lights and Godzilla head' },
        { lat: 35.6942, lng: 139.7012, label: 'Toriyoshi', num: 5, cat: 'food', desc: 'All-chicken yakitori — zero pork risk' }
      ]
    },
    {
      num: 4,
      date: '2026-05-18',
      neighborhoods: 'Ueno · Akihabara · Yanaka',
      title: 'Pandas, Parks & the Old Town',
      description: "Ueno is Tokyo's family heartland — a massive park with a zoo (hello, pandas!), world-class museums, and a lake with pedal boats. Then wander into Yanaka, one of Tokyo's last old-fashioned neighbourhoods, where time moves slowly and cats rule the streets.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Ueno Zoo & Ueno Park',
              description: "Japan's oldest zoo is home to giant pandas, and toddlers go absolutely bananas for them. The zoo is compact and manageable, with a petting area for small kids. Ueno Park surrounding the zoo is gorgeous in May — cherry trees in full green leaf, lotus ponds, and wide paths for strolling.",
              details: [
                '🐼 Giant pandas Xiao Xiao and Lei Lei are the stars',
                '🐣 The petting zoo area is perfect for 2-3 year olds',
                '⛲ Ueno Park has a beautiful Shinobazu Pond with pedal boats',
                '🎫 ¥600 adults, free for kids under 6'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Yanaka Ginza & Cat Town',
              description: "One of Tokyo's most charming traditional neighbourhoods. The narrow Yanaka Ginza shopping street is lined with old-school snack shops, and stray cats lounge everywhere. Toddlers love pointing out the cat sculptures and real cats alike. The atmosphere is unhurried and utterly delightful.",
              details: [
                '🐱 Cat statues and real cats throughout the neighbourhood',
                '🍦 Try the famous cat-tail doughnuts (yanaka shippo) — no pork',
                '📸 "Yūyake Dandan" sunset staircase is a classic photo spot',
                '🏘️ Old wooden houses, tiny temples, and zero tourists'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Kamachiku (Ueno)',
              description: "Handmade udon noodles served in a beautiful old wooden house. The cold dipping udon (zaru udon) is refreshing and naturally pork-free. Garden seating where toddlers can wiggle around.",
              meta: '💰 $$ · 📍 Nezu, near Ueno · Wheat noodles, no pork'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Ameyoko Market',
              description: "This bustling market street runs under the JR tracks near Ueno Station. Stalls sell everything from fresh fruit to grilled seafood skewers. The energy is infectious — vendors shout prices, kids get free samples, and you can grab incredible street food for dinner.",
              details: [
                '🦐 Grilled seafood skewers — shrimp, scallop, squid',
                '🍓 Fresh cut fruit cups for the kids',
                '🛍️ Open until about 7pm — go early evening for the best energy'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ameyoko Market Street Food',
              description: 'Graze through the market — grilled seafood skewers, fresh fruit, yakitori chicken, and tamagoyaki. All naturally pork-free, all kid-friendly.',
              meta: '💰 $ · 📍 Ameyoko, Ueno · Street food grazing'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7163, lng: 139.7714, label: 'Ueno Zoo', num: 1, cat: 'attraction', desc: 'Giant pandas and a petting zoo for toddlers' },
        { lat: 35.7146, lng: 139.7734, label: 'Ueno Park', num: 2, cat: 'attraction', desc: 'Huge park with ponds, temples, and pedal boats' },
        { lat: 35.7277, lng: 139.7673, label: 'Yanaka Ginza', num: 3, cat: 'attraction', desc: 'Old Tokyo charm — cat sculptures and snack shops' },
        { lat: 35.7108, lng: 139.7685, label: 'Kamachiku', num: 4, cat: 'food', desc: 'Handmade udon in a traditional wooden house' },
        { lat: 35.7109, lng: 139.7745, label: 'Ameyoko Market', num: 5, cat: 'food', desc: 'Bustling market with grilled seafood and fresh fruit' }
      ]
    },
    {
      num: 5,
      date: '2026-05-19',
      neighborhoods: 'Shibuya · Harajuku · Omotesando',
      title: 'Shibuya Crossing, Harajuku & Farewell Tokyo',
      description: "Your last Tokyo day is all about iconic moments — the famous Shibuya Crossing, Harajuku's candy-coloured streets, and a farewell dinner in Omotesando. Pack up and take the Shinkansen to Osaka in the evening.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shibuya Crossing & Hachikō',
              description: "Stand at the world's busiest intersection and cross with hundreds of people — toddlers find the organized chaos hilarious. Pet the Hachikō statue (the loyal dog), then head up to the Shibuya Sky observation deck for a bird's-eye view of the crossing below.",
              details: [
                '🐕 Hachikō statue outside Shibuya Station — touch the nose for luck',
                '📸 Watch from the Starbucks above for the classic overhead shot',
                '🏙️ Shibuya Sky rooftop (230m) — book online, stroller-friendly'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Harajuku & Takeshita Street',
              description: "Harajuku is a wonderland for all ages — Takeshita Street is packed with crepe shops, candy stores, and colourful fashion. Toddlers love the cotton candy, rainbow crepes, and character goods. Afterwards, stroll down the elegant tree-lined Omotesando boulevard.",
              details: [
                '🍦 Giant rainbow cotton candy and custom crepes',
                '🎀 Character shops for souvenirs — Sanrio, Ghibli goods',
                '🌳 Omotesando boulevard is wide and stroller-friendly',
                '🧸 Kiddy Land — 6 floors of toys, a toddler dream'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Maisen Tonkatsu (Chicken Katsu)',
              description: "Famous for katsu in a converted bathhouse — order the chicken katsu (チキンカツ) instead of pork. Crispy, juicy, and served with shredded cabbage and rice. The building itself is beautiful.",
              meta: '💰 $$ · 📍 Omotesando · Order chicken katsu — no pork'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shinkansen to Osaka',
              description: "Head to Tokyo Station and board the Shinkansen (bullet train) to Osaka — 2.5 hours of smooth, quiet comfort. Kids love watching the countryside blur past at 300km/h. Buy ekiben (train bento boxes) at the station for dinner aboard.",
              details: [
                '🚄 Nozomi or Hikari to Shin-Osaka — about 2h30m',
                '🍱 Buy ekiben at Tokyo Station — seafood and chicken options (no pork)',
                '👶 Reserve seats near the multi-purpose room (car 11) for families',
                '🧳 Large luggage storage behind the last row of each car'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Dinner',
              name: 'Ekiben on the Shinkansen',
              description: "Train bento boxes are a Japanese travel tradition. Tokyo Station has an incredible ekiben shop — try the seafood chirashi or chicken teriyaki bento. The kids will be too excited watching out the window to fuss about food.",
              meta: '💰 $$ · 📍 Tokyo Station ekiben shops · No pork options available'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6595, lng: 139.7004, label: 'Shibuya Crossing', num: 1, cat: 'attraction', desc: "World's busiest pedestrian crossing" },
        { lat: 35.6598, lng: 139.7006, label: 'Hachikō Statue', num: 2, cat: 'attraction', desc: 'The loyal dog statue outside Shibuya Station' },
        { lat: 35.6702, lng: 139.7027, label: 'Takeshita Street', num: 3, cat: 'attraction', desc: 'Colourful Harajuku street — crepes and candy' },
        { lat: 35.6651, lng: 139.7122, label: 'Maisen', num: 4, cat: 'food', desc: 'Chicken katsu in a converted bathhouse' },
        { lat: 35.6812, lng: 139.7671, label: 'Tokyo Station', num: 5, cat: 'attraction', desc: 'Shinkansen departure to Osaka' }
      ]
    },
    {
      num: 6,
      date: '2026-05-20',
      neighborhoods: 'Osaka Castle · Dotonbori · Namba',
      title: 'Osaka — Castle, Street Food & Neon River',
      description: "Welcome to Osaka — Japan's kitchen! Start with the stunning Osaka Castle and its surrounding park (perfect for toddler energy), then dive into Dotonbori for the best street food crawl of your life. All pork-free, all incredible.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Osaka Castle & Park',
              description: "The gleaming white-and-gold castle sits in a massive park with moats, gardens, and open lawns. The castle museum inside has samurai armour and panoramic views from the 8th floor. The park is perfect for toddler running — wide paths, cherry trees, and a playground near the south entrance.",
              details: [
                '🏯 Elevator to the top floor — stroller-friendly museum',
                '🌳 Nishinomaru Garden has open lawns and castle views',
                '🎠 Playville by Børnelund — indoor/outdoor playground in the park',
                '🚣 Water bus from the castle moat — kids love it'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Mizuno Okonomiyaki (Dotonbori)',
              description: "Osaka's most famous okonomiyaki (savoury pancake) restaurant. Order the seafood mix (ミックス) or squid version — cooked on a sizzling griddle right in front of you. Ask for no pork (buta nashi). Kids love watching the cooking show.",
              meta: '💰 $$ · 📍 Dotonbori · Seafood okonomiyaki — specify no pork'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Dotonbori Street Food Crawl',
              description: "Osaka's legendary food street is a sensory explosion — giant mechanical crabs, glowing signs, and endless food stalls. This is the ultimate pork-free street food crawl: takoyaki (octopus balls), kushikatsu (deep-fried skewers — get the shrimp and veggie), and yakisoba with seafood.",
              details: [
                '🐙 Takoyaki — Osaka\'s signature octopus balls, naturally pork-free',
                '🦐 Kushikatsu Daruma — get shrimp, squid, and vegetable skewers (skip the pork)',
                '🍦 Pablo cheese tarts for dessert — the kids will beg for seconds',
                '🦀 The giant Kani Doraku crab sign is a must-see photo op'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dotonbori Canal & Namba Night Walk',
              description: "As the neon reflects on the Dotonbori Canal, the whole area transforms into a river of light. The Glico Running Man sign is the classic Osaka photo. Walk along the canal with the kids — the energy is electric but the wide walkways make it easy with a stroller.",
              details: [
                '📸 Glico Running Man sign — THE Osaka photo',
                '🚶 Canal-side walkway is flat and wide — great for strollers',
                '🌙 The neon reflections on the water are magical after dark'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Kani Doraku (Dotonbori)',
              description: "The famous crab restaurant with the giant moving crab sign. Full crab course meals — grilled, tempura, sashimi, and hot pot. Entirely pork-free by nature. Kids love cracking the crab legs.",
              meta: '💰 $$$ · 📍 Dotonbori · All crab, no pork · Book ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6873, lng: 135.5262, label: 'Osaka Castle', num: 1, cat: 'attraction', desc: 'Iconic castle with museum and vast park' },
        { lat: 34.6687, lng: 135.5013, label: 'Dotonbori', num: 2, cat: 'attraction', desc: "Osaka's neon-lit food street" },
        { lat: 34.6686, lng: 135.5014, label: 'Mizuno Okonomiyaki', num: 3, cat: 'food', desc: 'Famous okonomiyaki — seafood, no pork' },
        { lat: 34.6688, lng: 135.5012, label: 'Kani Doraku', num: 4, cat: 'food', desc: 'Giant crab restaurant — all crab, no pork' },
        { lat: 34.6687, lng: 135.5022, label: 'Glico Running Man', num: 5, cat: 'attraction', desc: 'The iconic Osaka neon sign' }
      ]
    },
    {
      num: 7,
      date: '2026-05-21',
      neighborhoods: 'Osaka Bay · Tempozan · Shinsekai',
      title: 'Aquarium, Ferris Wheel & Shinsekai',
      description: "A full day of wonder at one of the world's best aquariums, a giant Ferris wheel with bay views, and the retro-futuristic neighbourhood of Shinsekai for the best kushikatsu (no pork!) in Osaka.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Osaka Aquarium Kaiyukan',
              description: "One of the world's largest aquariums, Kaiyukan is jaw-dropping. A massive whale shark glides through the central tank, and the spiral descent takes you past penguins, dolphins, jellyfish, and sea otters. Toddlers are mesmerized by the jellyfish gallery and the touch pool where they can pet rays and sharks.",
              details: [
                '🐋 The whale shark tank is 9 metres deep — breathtaking',
                '🐧 Penguin feeding time is a highlight — check schedule',
                '✋ Interactive touch pool — toddlers can pet small sharks and rays',
                '🎫 Book online for timed entry — arrive at opening (10am)'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tempozan Ferris Wheel & Harbour Village',
              description: "Right next to Kaiyukan, the Tempozan Giant Ferris Wheel offers panoramic views of Osaka Bay. On a clear day you can see to Kobe and even Awaji Island. The Harbour Village mall below has kid-friendly shops and an indoor playground.",
              details: [
                '🎡 112.5m tall — one of the world\'s largest Ferris wheels',
                '🔭 Clear cabins available for the brave — transparent floor!',
                '🛍️ Tempozan Marketplace has LEGOLAND Discovery Centre'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Naniwa Kuishinbo Yokocho',
              description: "A retro food court inside Tempozan Marketplace recreating 1960s Osaka. Stalls serve takoyaki, yakisoba, and udon. Choose seafood and chicken options — easy to avoid pork. The vintage atmosphere is charming.",
              meta: '💰 $$ · 📍 Tempozan Marketplace · Multiple pork-free options'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shinsekai District',
              description: "Osaka's retro entertainment district feels like stepping into a 1950s Japanese movie set. The Tsutenkaku Tower glows at night, and the streets are lined with kushikatsu restaurants, game arcades, and quirky signage. It's vibrant, safe, and utterly unique.",
              details: [
                '🗼 Tsutenkaku Tower — rub Billiken\'s feet for good luck',
                '🎮 Retro game arcades with crane games — toddlers love trying',
                '🏮 The neon signage and Fugu (blowfish) lanterns are incredible'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Kushikatsu Daruma (Shinsekai)',
              description: "The original Kushikatsu Daruma — Osaka's most famous deep-fried skewer restaurant. Order shrimp, squid, cheese, asparagus, and sweet potato skewers. Simply skip the pork options. The strict 'no double dipping' sauce rule is part of the fun.",
              meta: '💰 $$ · 📍 Shinsekai · Order seafood & veggie skewers — no pork'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6545, lng: 135.4290, label: 'Osaka Aquarium Kaiyukan', num: 1, cat: 'attraction', desc: "World-class aquarium with whale sharks and touch pools" },
        { lat: 34.6530, lng: 135.4310, label: 'Tempozan Ferris Wheel', num: 2, cat: 'attraction', desc: 'Giant Ferris wheel with bay panoramas' },
        { lat: 34.6522, lng: 135.5063, label: 'Shinsekai', num: 3, cat: 'attraction', desc: 'Retro neon district with Tsutenkaku Tower' },
        { lat: 34.6524, lng: 135.5064, label: 'Kushikatsu Daruma', num: 4, cat: 'food', desc: 'Famous deep-fried skewers — shrimp & veggie' }
      ]
    },
    {
      num: 8,
      date: '2026-05-22',
      neighborhoods: 'Nara · Todai-ji · Nara Park',
      title: 'Day Trip to Nara — Bowing Deer & Giant Buddha',
      description: "A magical day trip from Osaka to Nara — where over 1,000 wild deer roam freely and bow for crackers. Toddlers are enchanted. Then visit Todai-ji Temple, housing a 15-metre bronze Buddha so large it takes your breath away.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Train to Nara & Nara Park Deer',
              description: "Take the train from Osaka to Nara (45 min) and walk into Nara Park where over 1,000 sika deer roam freely. Buy deer crackers (shika senbei, ¥200) and watch the deer bow politely before accepting them. Toddlers find this absolutely magical — the deer are gentle and used to children.",
              details: [
                '🦌 Buy deer crackers (¥200) from vendors throughout the park',
                '🙇 The deer have learned to bow — bow back and they\'ll bow again!',
                '👶 Deer are gentle but can be persistent — hold crackers up high',
                '📸 Morning light in the park is beautiful for photos'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Todai-ji Temple & Great Buddha',
              description: "Inside the world's largest wooden building sits a 15-metre bronze Buddha that has inspired awe for over 1,200 years. Toddlers are genuinely amazed by the sheer scale. There's a pillar with a hole the size of the Buddha's nostril — kids can crawl through for good luck.",
              details: [
                '🏛️ The Great Buddha Hall is the world\'s largest wooden structure',
                '👃 Crawl through the nostril pillar for good luck — kids love this!',
                '⛩️ ¥600 adults, free for kids under 6',
                '🌳 The walk from the park entrance through deer-lined paths is lovely'
              ]
            },
            {
              title: 'Isuien Garden',
              description: "A peaceful Meiji-era garden with borrowed scenery from Todai-ji's roof. The pond reflections and manicured paths are stunning. A quiet counterpoint to the deer excitement — good for toddler cooldown time.",
              details: [
                '🍃 Beautiful borrowed scenery (shakkei) technique',
                '🫖 Tea house serves matcha with traditional sweets'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Kakinoha Sushi (Nara specialty)',
              description: "Nara's famous persimmon leaf-wrapped sushi — typically salmon and mackerel pressed sushi wrapped in fragrant kakinoha leaves. Naturally pork-free and unique to Nara. Light, elegant, and toddler-friendly in size.",
              meta: '💰 $$ · 📍 Nara town centre · Nara specialty, no pork'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Osaka',
              description: 'Head back to Osaka on the train (45 min) for dinner and rest. The kids will likely nap on the train after a big day with the deer.',
              details: [
                '🚂 Kintetsu Nara Line back to Osaka-Namba — direct and easy'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Matsusakagyu Yakiniku M (Namba)',
              description: "Premium Matsusaka beef yakiniku (Japanese BBQ). Grill thin-sliced wagyu beef at your table — the marbling melts in your mouth. Entirely beef-focused, naturally pork-free. The interactive grilling keeps kids entertained.",
              meta: '💰 $$$$ · 📍 Namba, Osaka · All beef, no pork · Book ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6851, lng: 135.8048, label: 'Nara Park', num: 1, cat: 'attraction', desc: '1,000+ wild deer that bow for crackers' },
        { lat: 34.6890, lng: 135.8398, label: 'Todai-ji Temple', num: 2, cat: 'attraction', desc: 'Giant Buddha in world\'s largest wooden building' },
        { lat: 34.6876, lng: 135.8388, label: 'Isuien Garden', num: 3, cat: 'attraction', desc: 'Serene Meiji-era garden with Todai-ji views' },
        { lat: 34.6850, lng: 135.8320, label: 'Kakinoha Sushi', num: 4, cat: 'food', desc: 'Persimmon leaf-wrapped sushi — Nara specialty' },
        { lat: 34.6658, lng: 135.5006, label: 'Matsusakagyu Yakiniku M', num: 5, cat: 'food', desc: 'Premium wagyu beef BBQ — no pork' }
      ]
    },
    {
      num: 9,
      date: '2026-05-23',
      neighborhoods: 'Arashiyama · Bamboo Grove · Fushimi Inari',
      title: 'Kyoto Day 1 — Bamboo, Monkeys & Torii Gates',
      description: "Your first Kyoto day trip from Osaka hits two of Japan's most breathtaking sights — the towering Arashiyama Bamboo Grove and the endless vermillion torii gates of Fushimi Inari. Plus, a monkey park where primates roam free and toddlers squeal with delight.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Arashiyama Bamboo Grove',
              description: "Walk through a cathedral of towering bamboo that filters the sunlight into an ethereal green glow. Arrive early (before 9am) and you'll have the path nearly to yourselves. The sound of bamboo creaking in the wind is unforgettable.",
              details: [
                '🎋 Arrive by 8:30am for empty paths — it gets crowded by 10',
                '📸 The light filtering through bamboo is otherworldly',
                '👶 Stroller-friendly paved path through the grove',
                '🌉 Cross the Togetsukyo Bridge afterwards — beautiful river views'
              ]
            },
            {
              title: 'Iwatayama Monkey Park',
              description: "A 15-minute uphill hike (carrier recommended for toddlers) leads to a hilltop park where 120 wild Japanese macaque monkeys roam free. You're in their home — they're not caged. Feed them from inside a shelter while they peer through the wire. Incredible Kyoto panorama from the top.",
              details: [
                '🐒 120 wild monkeys roam freely on the mountain',
                '👶 Use a carrier for the uphill walk — not stroller-friendly',
                '🥜 Buy monkey food (¥100) and feed them through the wire mesh',
                '🏔️ Amazing panoramic views of Kyoto from the summit'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Fushimi Inari Shrine',
              description: "The most iconic sight in all of Japan — thousands of vermillion torii gates creating tunnels up a mountainside. With toddlers, walk the first 30 minutes to the Yotsutsuji intersection viewpoint — no need to do the full 2-hour hike. The gates are mesmerizing at any depth.",
              details: [
                '⛩️ 10,000+ torii gates wind up Mount Inari',
                '🎯 With toddlers, aim for the first viewpoint (30 min up)',
                '🦊 Fox statues everywhere — Inari\'s divine messenger',
                '👶 Carrier recommended — stairs throughout, not stroller-friendly'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Arashiyama Yoshimura',
              description: "Handmade soba noodles with a view of the Togetsukyo Bridge and the Hozu River. The tempura soba set is excellent — shrimp and vegetable tempura with buckwheat noodles. Naturally pork-free.",
              meta: '💰 $$ · 📍 Arashiyama, facing the river · Soba & tempura, no pork'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Fushimi Inari Street Food & Return',
              description: "The approach to Fushimi Inari is lined with food stalls — grilled rice crackers, inari sushi (tofu pocket sushi — named after this very shrine), and soft serve. Grab snacks, then train back to Osaka for dinner.",
              details: [
                '🍘 Grilled senbei (rice crackers) fresh from the grill',
                '🍣 Inari sushi — sweet tofu pockets stuffed with rice',
                '🚂 JR Inari Station → Osaka — about 45 min'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Zuboraya Fugu (Shinsekai)',
              description: "Try fugu (pufferfish) — one of Japan's most unique dining experiences. Despite its reputation, fugu at licensed restaurants is completely safe. Served as sashimi, hot pot, and deep-fried. Entirely seafood, zero pork.",
              meta: '💰 $$$ · 📍 Shinsekai, Osaka · Pufferfish — completely pork-free'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0173, lng: 135.6717, label: 'Arashiyama Bamboo Grove', num: 1, cat: 'attraction', desc: 'Towering bamboo cathedral — arrive early' },
        { lat: 35.0147, lng: 135.6778, label: 'Iwatayama Monkey Park', num: 2, cat: 'attraction', desc: 'Wild monkeys on a hilltop — feed them through wire' },
        { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari Shrine', num: 3, cat: 'attraction', desc: '10,000 vermillion torii gates up a mountainside' },
        { lat: 35.0135, lng: 135.6777, label: 'Arashiyama Yoshimura', num: 4, cat: 'food', desc: 'Handmade soba with river views' },
        { lat: 34.6520, lng: 135.5060, label: 'Zuboraya Fugu', num: 5, cat: 'food', desc: 'Pufferfish dining — unique and pork-free' }
      ]
    },
    {
      num: 10,
      date: '2026-05-24',
      neighborhoods: 'Kinkaku-ji · Gion · Higashiyama',
      title: 'Kyoto Day 2 — Golden Temple, Geisha Streets & Farewell',
      description: "Your final day is pure Kyoto magic — the jaw-dropping Golden Pavilion reflected in its mirror lake, the preserved geisha district of Gion, and the atmospheric lanes of Higashiyama. A fitting farewell to an unforgettable Japan adventure.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kinkaku-ji (Golden Pavilion)',
              description: "Japan's most photographed temple — a three-story pavilion covered entirely in gold leaf, reflecting perfectly in the mirror pond. The garden path loops around the pond, and toddlers love spotting the koi fish and turtles in the water. Arrive at opening (9am) for the calmest experience.",
              details: [
                '✨ The gold leaf gleams even on cloudy days',
                '🐢 Turtles and koi in the pond — toddler magnets',
                '🍵 Matcha and a sweet at the tea garden near the exit',
                '🎫 ¥500 adults, free for preschoolers'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Higashiyama & Ninenzaka Lanes',
              description: "Walk the beautifully preserved lanes of Higashiyama — traditional wooden buildings, incense shops, matcha cafés, and pottery studios. The stone-paved Ninenzaka and Sannenzaka slopes lead up toward Kiyomizu-dera. With toddlers, enjoy the lower lanes without tackling the full temple climb.",
              details: [
                '🏘️ Ninenzaka is one of Japan\'s most photogenic streets',
                '🍡 Matcha soft serve and mitarashi dango (grilled rice dumplings)',
                '🎎 Souvenir shops with handmade crafts, fans, and chopsticks',
                '📸 Spot women in rented kimono — Higashiyama is the kimono rental capital'
              ]
            },
            {
              title: 'Gion Geisha District',
              description: "Kyoto's most famous geisha district — walk along Hanamikoji Street's traditional tea houses and see if you spot a geiko (Kyoto geisha) or maiko (apprentice) heading to an evening engagement. The wooden machiya townhouses are exquisite.",
              details: [
                '👘 Best chance to spot geiko/maiko: around 5-6pm on Hanamikoji',
                '🏡 Shirakawa canal area — willows, stone bridges, stunning photos',
                '📷 Please don\'t chase or block geiko — observe respectfully from a distance'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Omen Udon (Gion)',
              description: "A Kyoto institution serving handmade udon with a rich dipping broth and seasonal vegetables. The signature cold udon with sesame dipping sauce is elegant and refreshing. Naturally pork-free — the broth is kelp and bonito based.",
              meta: '💰 $$ · 📍 Gion area · Handmade udon, no pork'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Farewell Dinner & Return',
              description: "Celebrate 10 incredible days in Japan with a special farewell dinner, then take the train back to Osaka. Tomorrow you'll head to the airport with hearts full of memories — the deer bows, the bamboo whispers, the toddlers' faces at teamLab, and a thousand flavours of this extraordinary country.",
              details: [
                '🎌 What a trip — three cities, zero pork, maximum memories',
                '🚂 Train from Kyoto to Osaka — 30 min',
                '✈️ Kansai International Airport is 50 min from Osaka by train'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Hafuu (Kyoto Wagyu)',
              description: "End the trip with Kyoto's finest wagyu beef — Hafuu serves exquisite steak courses in an intimate setting. Tender, marbled, melt-in-your-mouth Japanese beef. A pure beef restaurant with no pork whatsoever. The perfect farewell meal.",
              meta: '💰 $$$$ · 📍 Central Kyoto · Wagyu steak course, no pork · Book ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0394, lng: 135.7292, label: 'Kinkaku-ji (Golden Pavilion)', num: 1, cat: 'attraction', desc: 'Gold-leaf temple reflected in a mirror pond' },
        { lat: 34.9960, lng: 135.7807, label: 'Ninenzaka', num: 2, cat: 'attraction', desc: 'Preserved stone-paved lanes with traditional shops' },
        { lat: 35.0037, lng: 135.7756, label: 'Gion (Hanamikoji)', num: 3, cat: 'attraction', desc: 'Geisha district — tea houses and kimono' },
        { lat: 35.0055, lng: 135.7780, label: 'Omen Udon', num: 4, cat: 'food', desc: 'Handmade udon — Kyoto institution' },
        { lat: 35.0040, lng: 135.7685, label: 'Hafuu Wagyu', num: 5, cat: 'food', desc: 'Premium Kyoto wagyu steak — farewell dinner' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$100–180/night', midrange: '$200–400/night', luxury: '$400–800/night' },
    { category: 'Meals (family of 5)', budget: '$60–100/day', midrange: '$120–250/day', luxury: '$300–500/day' },
    { category: 'Transport', budget: '$30–50/day', midrange: '$50–100/day', luxury: '$100–200/day' },
    { category: 'Activities', budget: '$20–40/day', midrange: '$50–120/day', luxury: '$120–300/day' },
    { category: 'Japan Rail Pass', budget: '$250pp (7-day)', midrange: '$250pp (7-day)', luxury: '$450pp (Green Car)' },
    { category: '10-Day Total (family)', budget: '$4,000–6,000', midrange: '$7,000–14,000', luxury: '$15,000–30,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Tokyo Narita (NRT) or Haneda (HND) — Haneda is closer to the city', 'Narita Express to Tokyo Station: 60 min. Haneda monorail: 20 min', 'Fly home from Osaka Kansai (KIX) — 50 min train from Osaka Station'] },
    { title: '🏨 Where to Stay', items: ['Tokyo: Shinjuku area — central, great transport links, family hotels', 'Osaka: Namba/Dotonbori area — walkable to street food, close to trains', 'Look for "family rooms" or connecting rooms — many hotels accommodate 5', 'Airbnb apartments give extra space for luggage, strollers, and toddler chaos'] },
    { title: '🌡️ Weather', items: ['Mid-May averages 20-25°C (68-77°F) — comfortable and pleasant', 'Low humidity, occasional rain — pack light rain jackets', 'UV is moderate — sun hats for the kids', 'Perfect season: post-cherry blossom, pre-rainy season'] },
    { title: '💳 Money', items: ['Japan is increasingly cashless but small shops and temples need cash', 'Carry ¥10,000-20,000 in cash — withdraw from 7-Eleven ATMs (international cards)', 'IC cards (Suica/ICOCA) work for transport and convenience stores', 'No tipping anywhere in Japan — it can be considered rude'] },
    { title: '👶 Family Tips', items: ['Kids under 6 ride free on trains and buses', 'Most stations have elevators — look for the wheelchair/stroller signs', 'Konbini (7-Eleven, Lawson, FamilyMart) have diapers, baby food, and wipes 24/7', 'Baby rooms (赤ちゃん休憩室) are in department stores and major stations', 'Rent a pocket WiFi at the airport — essential for maps and translation'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
