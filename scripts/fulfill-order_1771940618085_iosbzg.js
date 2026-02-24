const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771940618085_iosbzg',
  email: 'galaxycats510@gmail.com',
  destination: 'Tokyo, Japan',
  startDate: '2026-03-14',
  endDate: '2026-03-19',
  groupSize: '3-4',
  requests: 'Father is vegetarian (can eat eggs). DisneySea is a must. Shopping, scenery, fun activities. Open to day trips near Tokyo.'
};

const itineraryData = {
  destination: 'Tokyo, Japan',
  countryEmoji: '🇯🇵',
  title: 'Tokyo Adventure: Theme Parks, Temples & Cherry Blossoms',
  subtitle: '5 nights of culture, fun & flavour for the whole family',
  description: "Tokyo in mid-March is electric — the first cherry blossoms are appearing, the streets buzz with energy, and there's magic around every corner. This itinerary balances iconic experiences (DisneySea! Shibuya! Senso-ji!) with hidden gems, vegetarian-friendly dining for Dad, and enough shopping and scenery to fill everyone's camera roll. From the futuristic streets of Akihabara to the serene bamboo of Kamakura, this is Tokyo at its best.",
  duration: '5 nights',
  dates: 'Mar 14 – Mar 19, 2026',
  budget: '$',
  pace: 'Moderate',
  bestFor: 'Families & Groups',
  highlights: [
    'Full day at Tokyo DisneySea with Fantasy Springs',
    'Day trip to Kamakura — Great Buddha & coastal scenery',
    'Shibuya Crossing, Harajuku & Meiji Shrine',
    'Senso-ji Temple & Nakamise shopping street',
    'Akihabara arcades & Shimokitazawa vintage shopping'
  ],

  essentials: [
    { title: '🌸 Early Cherry Blossoms', text: "Mid-March is the very start of cherry blossom season in Tokyo. Early-blooming varieties may be out — check Shinjuku Gyoen and Ueno Park. Full bloom is typically late March to early April." },
    { title: '🚇 Getting Around', text: "Get a Suica or Pasmo IC card (or use Apple Wallet) for seamless travel on all trains, subways, and buses. A 72-hour Tokyo Subway Ticket (¥1,500) is great value. Google Maps handles all transit perfectly." },
    { title: '🥬 Vegetarian in Tokyo', text: "Japan can be tricky for vegetarians due to hidden dashi (fish stock). Look for shojin ryori (Buddhist temple cuisine), Indian restaurants, and chains like Afuri (yuzu shio ramen has a vegan option). Always say 'watashi wa bejitarian desu' (I'm vegetarian). Eggs (tamago) are widely available." },
    { title: '💴 Budget Tips', text: "Convenience stores (7-Eleven, Lawson, FamilyMart) have amazing, cheap food — onigiri, egg sandwiches, salads. Department store basement floors (depachika) have incredible takeaway meals. Many temples and parks are free." }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-14',
      neighborhoods: 'Asakusa · Ueno · Akihabara',
      title: 'Temples, Traditions & Electric Town',
      description: "Hit the ground running with Tokyo's most iconic temple, a stroll through Ueno's cultural corridor, and an evening in the neon-lit wonderland of Akihabara. This day is all about first impressions — and Tokyo delivers.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Senso-ji Temple & Nakamise Street',
              description: "Tokyo's oldest and most visited temple is stunning in any season. Walk through the iconic Kaminarimon (Thunder Gate), browse the Nakamise shopping street for traditional snacks and souvenirs, and explore the temple grounds. Arrive early for fewer crowds.",
              details: [
                '⛩️ Free entry · Open 24 hours (main hall 6am–5pm)',
                '🛍️ Nakamise has 90+ shops — try melon pan, senbei crackers, and ningyo-yaki',
                '🥬 Dad tip: many Nakamise snacks are naturally vegetarian (rice crackers, sweet potato treats, dango)'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Pelican Café',
              description: 'Famous Tokyo bakery near Asakusa serving incredible thick-cut toast and egg sandwiches. Simple, delicious, and veggie-friendly.',
              meta: '💰 $ · 📍 Taito, near Asakusa · Cash only'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ueno Park & Ameyoko Market',
              description: "Walk south to Ueno Park — a huge green space with museums, shrines, and a lake. Check for early cherry blossoms at Shinobazu Pond. Then dive into Ameyoko, the bustling outdoor market street for cheap street food, snacks, and bargains.",
              details: [
                '🌸 Ueno Park is one of Tokyo\'s top hanami (blossom viewing) spots',
                '🏛️ Tokyo National Museum is here if you want world-class Japanese art',
                '🛒 Ameyoko is chaotic and fun — great for dried fruits, snacks, and clothes'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Afuri Ramen (Ueno)',
              description: 'Famous for their yuzu shio (citrus salt) ramen. They offer a vegan/vegetarian version that\'s light, fragrant, and absolutely delicious — one of the best veggie ramen options in Tokyo.',
              meta: '💰 $ · 📍 Multiple locations · 🥬 Vegan ramen available'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Akihabara Electric Town',
              description: "Tokyo's famous electronics and anime district is sensory overload in the best way. Explore multi-floor arcades (try the crane games!), retro game shops, anime stores, and quirky themed cafés. Even non-gamers love the energy here.",
              details: [
                '🕹️ SEGA and Taito arcades — crane games, rhythm games, photo booths',
                '🎮 Super Potato for retro game shopping',
                '📸 The neon-lit streets are incredible at night'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'CoCo Ichibanya Curry House',
              description: 'Japan\'s beloved curry chain lets you fully customize your order. Vegetable curry with egg topping is perfect for Dad, and everyone else can load up on katsu or seafood versions.',
              meta: '💰 $ · 📍 Akihabara branch · 🥬 Vegetable curry + egg option'
            }
          ],
          tips: [
            { type: 'tip', text: 'If jet lag hits, the bright lights and arcade energy of Akihabara will keep you going. Grab a matcha Kit-Kat from a convenience store for fuel!' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: 'Senso-ji Temple', num: 1, cat: 'attraction', desc: "Tokyo's oldest temple with iconic Thunder Gate" },
        { lat: 35.7146, lng: 139.7966, label: 'Nakamise Shopping Street', num: 2, cat: 'shopping', desc: 'Traditional souvenir and snack street' },
        { lat: 35.7141, lng: 139.7774, label: 'Ueno Park', num: 3, cat: 'attraction', desc: 'Huge park with museums, shrines, and cherry blossoms' },
        { lat: 35.7082, lng: 139.7745, label: 'Ameyoko Market', num: 4, cat: 'shopping', desc: 'Bustling outdoor market street' },
        { lat: 35.6984, lng: 139.7731, label: 'Akihabara', num: 5, cat: 'attraction', desc: 'Electric Town — arcades, anime, and neon lights' },
        { lat: 35.7100, lng: 139.7823, label: 'Afuri Ramen', num: 6, cat: 'food', desc: 'Famous yuzu ramen with vegan option' }
      ]
    },
    {
      num: 2,
      date: '2026-03-15',
      neighborhoods: 'Harajuku · Shibuya · Shinjuku',
      title: 'Fashion, Scramble & City Lights',
      description: "Today is all about Tokyo's iconic pop culture and urban energy. From the quirky fashion of Harajuku to the world-famous Shibuya Crossing, and ending with the dazzling skyline views of Shinjuku — this is the Tokyo you've seen in movies, and it's even better in person.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Meiji Shrine & Harajuku',
              description: "Start with the serene forested walk to Meiji Shrine — a peaceful Shinto shrine dedicated to Emperor Meiji, surrounded by 170,000 trees. Then emerge onto Takeshita Street for a total vibe shift: kawaii fashion, crêpes, and wild energy.",
              details: [
                '⛩️ Free entry · The forested approach is magical — feels like leaving Tokyo',
                '🛍️ Takeshita Street is short but packed — rainbow cotton candy, crêpes, quirky shops',
                '👗 Harajuku side streets have vintage and designer shops'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Bills Omotesando',
              description: "The famous Australian café known for 'the world's best ricotta pancakes.' Light, fluffy, and they have great egg dishes too. A perfect start to a big day.",
              meta: '💰 $$ · 📍 Omotesando · 🥬 Ricotta pancakes & egg dishes for Dad'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shibuya Crossing & Shopping',
              description: "The world's busiest pedestrian crossing is mesmerizing. Watch from the Starbucks above, then join the flow. Explore Shibuya 109 for Japanese fashion, Center-gai for street food, and the new Shibuya Sky observation deck for panoramic views.",
              details: [
                '📸 Best viewing: Starbucks 2F at Tsutaya or the new Shibuya Sky (¥2,000)',
                '🐕 Hachiko statue — the famous loyal dog, right outside the station',
                '🛍️ Shibuya 109 for J-fashion, Mega Don Quijote for wild souvenirs'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Nagi Shokudo',
              description: 'A fully vegetarian/vegan café in Shibuya serving Japanese home-style set meals. The veggie plate lunch is hearty, balanced, and changes daily. Perfect for Dad!',
              meta: '💰 $ · 📍 Shibuya · 🥬 100% vegetarian restaurant'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shinjuku Gyoen & Kabukicho',
              description: "If time permits, catch the last light at Shinjuku Gyoen (closes 4:30pm in March — check schedule). Then head to Kabukicho and the neon-drenched streets of east Shinjuku. Omoide Yokocho (Memory Lane) is an atmospheric alley of tiny eateries.",
              details: [
                '🌸 Shinjuku Gyoen has 1,000+ cherry trees — check early blooms',
                '🏮 Omoide Yokocho — tiny atmospheric alley bars (some veggie-friendly yakitori alternatives)',
                '🌃 Kabukicho\'s new Kabukicho Tower has entertainment and dining'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Shinjuku Gyoen Ramen Ouka',
              description: 'Near Shinjuku Gyoen, this spot offers excellent tonkotsu ramen. For Dad, nearby Ain Soph Journey in Shinjuku has incredible vegan burgers and set meals.',
              meta: '💰 $–$$ · 📍 Shinjuku · 🥬 Ain Soph Journey (vegan) is 5 min walk'
            }
          ],
          tips: [
            { type: 'tip', text: "Don Quijote (Donki) in Shibuya is open 24 hours — it's the ultimate souvenir shop. Japanese snacks, quirky gadgets, cosmetics, and tax-free shopping. Go wild." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6764, lng: 139.6993, label: 'Meiji Shrine', num: 1, cat: 'attraction', desc: 'Serene Shinto shrine in a forested grove' },
        { lat: 35.6702, lng: 139.7026, label: 'Takeshita Street', num: 2, cat: 'shopping', desc: 'Harajuku\'s famous kawaii fashion street' },
        { lat: 35.6595, lng: 139.7004, label: 'Shibuya Crossing', num: 3, cat: 'attraction', desc: 'World\'s busiest pedestrian crossing' },
        { lat: 35.6584, lng: 139.7022, label: 'Hachiko Statue', num: 4, cat: 'attraction', desc: 'Famous loyal dog statue at Shibuya Station' },
        { lat: 35.6852, lng: 139.7100, label: 'Shinjuku Gyoen', num: 5, cat: 'attraction', desc: 'Beautiful national garden — early cherry blossoms' },
        { lat: 35.6612, lng: 139.7038, label: 'Nagi Shokudo', num: 6, cat: 'food', desc: '100% vegetarian Japanese café in Shibuya' },
        { lat: 35.6938, lng: 139.7034, label: 'Omoide Yokocho', num: 7, cat: 'food', desc: 'Atmospheric alley of tiny bars and eateries' }
      ]
    },
    {
      num: 3,
      date: '2026-03-16',
      neighborhoods: 'Tokyo DisneySea · Maihama',
      title: 'A Magical Day at Tokyo DisneySea',
      description: "The day you've been waiting for! Tokyo DisneySea is widely considered the most beautiful theme park in the world. From the stunning Mediterranean Harbour entrance to the brand-new Fantasy Springs area, this is a full day of rides, shows, incredible themed food, and pure magic.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Arrive Early & Fantasy Springs',
              description: "Get to the park gates 30–45 minutes before opening. Head straight to Fantasy Springs — the newest area featuring Frozen, Tangled, and Peter Pan attractions. Anna & Elsa's Frozen Journey and Peter Pan's Never Land Adventure are the top rides with the longest waits.",
              details: [
                '🎟️ Buy tickets online in advance at the Tokyo Disney Resort website (¥7,900–9,400/adult)',
                '⏰ Park opens at 9am most days — be there by 8:15am',
                '📱 Download the Tokyo Disney Resort app for wait times and Disney Premier Access (paid FastPass)',
                '❄️ Fantasy Springs DPA (¥2,000) is worth it to skip the 90+ min queues'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Mamma Biscotti\'s Bakery',
              description: 'Right near the park entrance in Mediterranean Harbour. Fresh pastries, pizza bread, and coffee to fuel your morning rush. Grab and go!',
              meta: '💰 $ · 📍 Mediterranean Harbour · 🥬 Pastries & bread are veggie-friendly'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Classic Attractions & Themed Lands',
              description: "Explore the park's seven themed ports. Don't miss: Journey to the Center of the Earth (thrilling volcano ride), 20,000 Leagues Under the Sea (submarine dark ride), Tower of Terror, Indiana Jones Adventure, and Soaring: Fantastic Flight. The theming and attention to detail is on another level.",
              details: [
                '🌋 Journey to the Center of the Earth — DisneySea\'s signature ride, inside the volcano',
                '🗼 Tower of Terror — different storyline than other parks',
                '🦅 Soaring: Fantastic Flight — stunning hang-glider simulation',
                '🧜 Mermaid Lagoon — indoor area great for a break from crowds'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Casbah Food Court',
              description: 'In the Arabian Coast area, this restaurant serves excellent curries — including vegetable curry options that are perfect for Dad. The theming feels like stepping into Aladdin\'s palace.',
              meta: '💰 $ · 📍 Arabian Coast · 🥬 Vegetable curry available'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Believe! Sea of Dreams Night Show',
              description: "Stay for DisneySea's spectacular nighttime show on Mediterranean Harbour. Water fountains, fireworks, projections, and fire effects create a breathtaking 30-minute show. Stake out a spot 30–45 minutes early along the harbour waterfront.",
              details: [
                '🎆 Show is usually at 8:30pm — check the app for the day\'s schedule',
                '📍 Best viewing: near the Fortress or the bridge by Mysterious Island',
                '🛍️ Hit the shops after the show (they stay open 30 min after park close)'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Vulcania Restaurant',
              description: 'Inside the Mysterious Island volcano, this restaurant serves Chinese-inspired dishes in a Jules Verne steampunk setting. Fried rice and gyoza options available.',
              meta: '💰 $$ · 📍 Mysterious Island · 🥬 Fried rice & vegetable options'
            }
          ],
          tips: [
            { type: 'tip', text: "DisneySea's popcorn comes in unique flavours by area — curry, milk chocolate, strawberry, and more. The collectible popcorn buckets are iconic souvenirs. Grab one early before they sell out!" }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6267, lng: 139.8851, label: 'Tokyo DisneySea Entrance', num: 1, cat: 'attraction', desc: 'Park entrance at Mediterranean Harbour' },
        { lat: 35.6255, lng: 139.8870, label: 'Fantasy Springs', num: 2, cat: 'attraction', desc: 'Newest area — Frozen, Tangled, Peter Pan' },
        { lat: 35.6260, lng: 139.8835, label: 'Journey to the Center of the Earth', num: 3, cat: 'attraction', desc: 'Signature volcano thrill ride' },
        { lat: 35.6275, lng: 139.8810, label: 'Arabian Coast', num: 4, cat: 'attraction', desc: 'Aladdin-themed area with Casbah Food Court' },
        { lat: 35.6248, lng: 139.8855, label: 'Mysterious Island', num: 5, cat: 'attraction', desc: 'Jules Verne-themed volcanic crater' },
        { lat: 35.6280, lng: 139.8860, label: "Mamma Biscotti's Bakery", num: 6, cat: 'food', desc: 'Bakery near park entrance — pastries and coffee' }
      ]
    },
    {
      num: 4,
      date: '2026-03-17',
      neighborhoods: 'Kamakura · Enoshima',
      title: 'Day Trip: Kamakura — Great Buddha & Coastal Charm',
      description: "Escape Tokyo for a day and head south to Kamakura, the ancient capital filled with temples, hiking trails, and the iconic Great Buddha statue. Continue to the coastal island of Enoshima for ocean views, seafood, and a relaxed beach-town vibe. It's nature, history, and scenery rolled into one perfect day.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kamakura Great Buddha & Hase-dera Temple',
              description: "Take the JR Yokosuka Line from Tokyo Station to Kamakura (about 1 hour). Start at Kotoku-in to see the Great Buddha (Daibutsu) — a 13-meter bronze statue that's been sitting serenely since 1252. Then walk to nearby Hase-dera Temple for stunning ocean views and thousands of small Jizo statues.",
              details: [
                '🚂 JR Yokosuka Line from Tokyo → Kamakura (¥940, ~60 min)',
                '🗿 Great Buddha entry: ¥300 · You can go inside the statue for ¥50',
                '⛩️ Hase-dera has beautiful gardens and a panoramic ocean viewpoint',
                '📸 The Great Buddha is one of Japan\'s most iconic photos'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Onigiri & Coffee at Kamakura Station',
              description: 'Grab onigiri (rice balls) and canned coffee from the convenience store at Kamakura Station. Quick, cheap, and the perfect fuel for temple-hopping.',
              meta: '💰 $ · 📍 Kamakura Station · 🥬 Vegetable and egg onigiri available'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Komachi-dori Shopping Street & Bamboo Temple',
              description: "Head to Komachi-dori, Kamakura's charming pedestrian shopping street, for souvenirs, matcha treats, and snacks. Then visit Hokoku-ji — the famous Bamboo Temple — where you can sip matcha tea in a tranquil bamboo grove with over 2,000 towering stalks.",
              details: [
                '🛍️ Komachi-dori has cute shops, matcha soft serve, and fresh senbei',
                '🎋 Hokoku-ji entry: ¥300 (+¥600 for matcha in the bamboo garden)',
                '🍵 The matcha experience in the bamboo grove is unforgettable'
              ]
            },
            {
              title: 'Enoshima Island',
              description: "Take the Enoden tram (a charming coastal train) from Kamakura to Enoshima. Walk across the bridge to this small island for shrine visits, cave explorations, and panoramic views from the Sea Candle observation tower. On a clear day, you can see Mt. Fuji!",
              details: [
                '🚃 Enoden tram from Kamakura → Enoshima (¥260, 25 min) — sit on the right for ocean views',
                '🗼 Sea Candle tower: ¥500 · Mt. Fuji views on clear days',
                '🌊 Enoshima Iwaya caves are worth exploring'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Bowls Kamakura',
              description: 'Popular vegetarian-friendly café on Komachi-dori serving açaí bowls, smoothie bowls, and veggie plates. Light, fresh, and healthy.',
              meta: '💰 $ · 📍 Komachi-dori, Kamakura · 🥬 Fully veggie-friendly'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset at Enoshima & Return',
              description: "Watch the sunset from Enoshima's western shore — if it's clear, you'll see the sun set behind Mt. Fuji. Then take the train back to Tokyo, tired but happy. The Enoden to Fujisawa, then JR back to Tokyo, takes about 90 minutes.",
              details: [
                '🌅 Samuel Cocking Garden on Enoshima has great sunset viewpoints',
                '🚂 Return: Enoden → Fujisawa → JR Tokaido Line → Tokyo (about 90 min)'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ain Soph Ripple (Shinjuku)',
              description: 'Back in Tokyo, head to this popular vegan burger restaurant. Their fluffy vegan pancakes and burgers are legendary. Dad will love it — and everyone else will too. The burgers are that good.',
              meta: '💰 $$ · 📍 Shinjuku · 🥬 100% vegan restaurant — burgers, pancakes, pasta'
            }
          ],
          tips: [
            { type: 'tip', text: "The Enoden tram is a highlight in itself — it runs through residential streets so close to houses you could reach out and touch them. Sit by the window and enjoy the ride!" }
          ]
        }
      ],
      mapPins: [
        { lat: 35.3167, lng: 139.5357, label: 'Great Buddha (Kotoku-in)', num: 1, cat: 'attraction', desc: '13-meter bronze Buddha statue from 1252' },
        { lat: 35.3119, lng: 139.5320, label: 'Hase-dera Temple', num: 2, cat: 'attraction', desc: 'Beautiful temple with ocean views and Jizo statues' },
        { lat: 35.3221, lng: 139.5504, label: 'Komachi-dori', num: 3, cat: 'shopping', desc: 'Charming pedestrian shopping and snack street' },
        { lat: 35.3280, lng: 139.5670, label: 'Hokoku-ji Bamboo Temple', num: 4, cat: 'attraction', desc: 'Tranquil bamboo grove with matcha tea experience' },
        { lat: 35.2997, lng: 139.4797, label: 'Enoshima Island', num: 5, cat: 'attraction', desc: 'Coastal island with shrines, caves, and ocean views' },
        { lat: 35.2985, lng: 139.4780, label: 'Enoshima Sea Candle', num: 6, cat: 'attraction', desc: 'Observation tower — Mt. Fuji views on clear days' }
      ]
    },
    {
      num: 5,
      date: '2026-03-18',
      neighborhoods: 'Shimokitazawa · Yanaka · Tokyo Tower',
      title: 'Hidden Tokyo: Vintage Vibes, Old-Town Charm & Skyline Views',
      description: "Your last full day explores the Tokyo most tourists miss. Morning in Shimokitazawa — Tokyo's coolest neighbourhood for vintage shopping and indie cafés. Afternoon in Yanaka — a wonderfully preserved old-town district. End with sunset from Tokyo Tower and a farewell dinner.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shimokitazawa Vintage Shopping',
              description: "Take the Keio Line to Shimokitazawa — Tokyo's answer to Brooklyn or Shoreditch. This bohemian neighbourhood is packed with vintage clothing shops, record stores, independent cafés, and small theatres. Wander the narrow streets and discover hidden gems.",
              details: [
                '👕 Flamingo, Chicago, and Haight & Ashbury for vintage clothes',
                '💿 Flash Disc Ranch and Disk Union for vinyl records',
                '☕ Bear Pond Espresso is legendary (small, cash only, worth the wait)'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'City Country City',
              description: 'A cozy café above a vintage shop in Shimokitazawa. Great coffee, toast sets, and a relaxed atmosphere. Feels like hanging out at a friend\'s cool apartment.',
              meta: '💰 $ · 📍 Shimokitazawa · 🥬 Toast and egg sets available'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Yanaka Old Town & Yanesen Area',
              description: "Head to Yanaka — one of the few Tokyo neighbourhoods that survived WWII bombing. It feels like stepping back in time: narrow lanes, wooden houses, traditional craft shops, and friendly cats everywhere. Yanaka Ginza shopping street is a delightful strip of old-school Tokyo.",
              details: [
                '🐱 Yanaka is famous for its stray cats — look for cat-themed shops and statues',
                '🏘️ Yanaka Cemetery is peaceful and beautiful — look for cherry trees',
                '🛍️ Yanaka Ginza has traditional crafts, croquettes, and coffee'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Kayaba Coffee',
              description: 'A beautifully restored 1938 building in Yanaka serving excellent coffee and tamago sando (Japanese egg sandwiches). The upstairs tatami seating is charming.',
              meta: '💰 $ · 📍 Yanaka · 🥬 Egg sandwiches and toast for Dad'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Tokyo Tower at Sunset',
              description: "End your trip with a sunset visit to Tokyo Tower — the iconic 333-meter red-and-white tower. The main observation deck (150m) gives you sweeping views of the city lighting up as dusk falls. It's nostalgic, romantic, and the perfect farewell to Tokyo.",
              details: [
                '🗼 Main deck: ¥1,200 · Top deck tour: ¥2,800 (reserve online)',
                '🌅 Arrive 30 min before sunset for the golden hour transition',
                '📸 On clear days you can see Mt. Fuji from the top deck'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'T\'s TanTan (Tokyo Station)',
              description: "A vegan ramen restaurant inside Tokyo Station — perfect for a farewell meal before heading back to your hotel. Their tantan (sesame) ramen is rich, creamy, and 100% plant-based. Everyone at the table will love it, veggie or not.",
              meta: '💰 $ · 📍 Tokyo Station (Keiyo Street) · 🥬 100% vegan — famous tantan ramen'
            }
          ],
          tips: [
            { type: 'tip', text: "Pack your bags tonight! If you're heading to the airport tomorrow, get a Suica refund at any JR station. For last-minute souvenirs, Tokyo Station's underground shops (Character Street and Ramen Street) are incredible." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6613, lng: 139.6680, label: 'Shimokitazawa', num: 1, cat: 'shopping', desc: "Tokyo's coolest vintage and indie neighbourhood" },
        { lat: 35.7264, lng: 139.7676, label: 'Yanaka Ginza', num: 2, cat: 'shopping', desc: 'Old-town shopping street with traditional crafts' },
        { lat: 35.7240, lng: 139.7700, label: 'Yanaka Cemetery', num: 3, cat: 'attraction', desc: 'Peaceful cemetery with cherry trees and cat sculptures' },
        { lat: 35.6586, lng: 139.7454, label: 'Tokyo Tower', num: 4, cat: 'attraction', desc: 'Iconic 333m tower with sunset observation deck' },
        { lat: 35.7250, lng: 139.7690, label: 'Kayaba Coffee', num: 5, cat: 'food', desc: 'Restored 1938 café — egg sandwiches and pour-over coffee' },
        { lat: 35.6812, lng: 139.7671, label: "T's TanTan", num: 6, cat: 'food', desc: 'Vegan ramen in Tokyo Station — famous tantan ramen' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '¥5,000–10,000/night', midrange: '¥12,000–25,000/night', luxury: '¥30,000–80,000/night' },
    { category: 'Meals (per person)', budget: '¥1,500–3,000/day', midrange: '¥4,000–8,000/day', luxury: '¥10,000–25,000/day' },
    { category: 'Transport', budget: '¥800–1,500/day', midrange: '¥1,500–3,000/day', luxury: '¥5,000–10,000/day' },
    { category: 'Activities', budget: '¥0–1,000/day', midrange: '¥1,500–4,000/day', luxury: '¥5,000–15,000/day' },
    { category: 'DisneySea Ticket', budget: '¥7,900pp', midrange: '¥7,900pp + DPA ¥2,000', luxury: '¥9,400pp (peak) + DPA' },
    { category: '5-Night Total (per person)', budget: '¥50,000–80,000', midrange: '¥100,000–180,000', luxury: '¥250,000–450,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Narita Airport (NRT): 60–90 min to central Tokyo via Narita Express (¥3,070) or Skyliner (¥2,520)', 'Haneda Airport (HND): 20–40 min via Tokyo Monorail or Keikyu Line — much more convenient', 'Pocket WiFi or eSIM is essential — rent at the airport or order in advance'] },
    { title: '🏨 Where to Stay', items: ['Shinjuku — central hub, great transit, lively nightlife', 'Shibuya — trendy, walkable, close to Harajuku', 'Asakusa — traditional atmosphere, budget-friendly, near Senso-ji', 'For a group of 3-4: consider an Airbnb apartment or family rooms at Tokyu Stay or Mitsui Garden'] },
    { title: '🌡️ Weather', items: ['Mid-March averages 10–16°C (50–61°F)', 'Layers are key — warm mornings, pleasant afternoons', 'Rain is possible — pack a compact umbrella', 'Early cherry blossoms possible at Shinjuku Gyoen and Ueno Park'] },
    { title: '💳 Money', items: ['Japan is still fairly cash-heavy — carry ¥10,000–20,000 at a time', 'ATMs: 7-Eleven and Japan Post ATMs accept international cards', 'IC cards (Suica/Pasmo) work at convenience stores and vending machines too', 'Tax-free shopping available at department stores (bring your passport)'] },
    { title: '📱 Connectivity', items: ['Pocket WiFi: rent from Japan Wireless or Global WiFi (¥500–900/day)', 'eSIM: Ubigi, Airalo, or IIJmio — activate before you land', 'Free WiFi is spotty — don\'t rely on it', 'Download Google Maps offline + Tokyo Metro app'] }
  ]
};

fulfillOrder(order, itineraryData);
