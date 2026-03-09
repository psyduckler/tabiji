const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772735600899_0jzfj2',
  email: 'paulhblasjr@gmail.com',
  destination: 'Tokyo, Osaka, Kyoto',
  startDate: '2026-05-15',
  endDate: '2026-05-24',
  groupSize: '5+',
  requests: 'Pre-planned family itinerary with 60+ venues across Tokyo, Nara, Kyoto, Osaka'
};

const itineraryData = {
  destination: 'Tokyo, Kyoto & Osaka',
  countryEmoji: '🇯🇵',
  title: 'Tokyo, Kyoto & Osaka — A Family Adventure Through Japan',
  subtitle: '10 days of temples, toddler-friendly fun, anime cafés, street food & iconic sights across three cities',
  description: "This itinerary packs in over 60 hand-picked experiences across Japan's three greatest cities — designed for a family of five with two toddlers who refuse to slow down. From the neon chaos of Shinjuku to the sacred stillness of Fushimi Inari at dawn, from soufflé pancakes in Harajuku to takoyaki in Dotonbori — every day is a curated adventure. The pace is ambitious but realistic, with built-in flexibility for nap breaks, konbini pit stops, and spontaneous detours. No pork anywhere. No Gundam. Just pure Japan magic.",
  duration: '10 days',
  dates: 'May 15–24, 2026',
  budget: '$$–$$$',
  pace: 'Adventurous',
  bestFor: 'Families · Foodies · Culture · Adventure',
  highlights: [
    'teamLab Planets — walk barefoot through immersive digital art installations',
    'Fushimi Inari at dawn — thousands of vermilion torii gates without the crowds',
    'Kirby Café & Pokémon Center — anime/game cafés the whole family will love',
    'Dotonbori street food — takoyaki, okonomiyaki & the iconic Glico sign',
    'Arashiyama Bamboo Forest & Monkey Park — monkeys, bamboo & mountain views',
    'Nara Park — feed the legendary bowing deer with the kids',
    'Shinjuku Golden Gai — tiny bars in neon-lit alleyways after dark',
    'Osaka Aquarium Kaiyukan — whale sharks and rays in a massive tank',
    'Sensō-ji Temple — Tokyo\'s oldest temple at sunrise',
    'Shibuya Sky — sunset over Tokyo from 230 metres up'
  ],

  essentials: [
    { title: '🚆 Getting Around', text: 'Get a Suica or PASMO IC card at Narita — works on all trains, buses, and konbini. For the Tokyo → Kyoto Shinkansen (Day 6) and Osaka → Tokyo return (Day 9), consider a 7-day JR Pass (starts Day 3 or 4). Kyoto → Osaka is only 15 min by train. Nara from Kyoto is ~45 min by JR Nara Line.' },
    { title: '👶 Traveling with Toddlers', text: 'Japan is incredibly toddler-friendly. Most train stations have elevators, department stores have nursing rooms, and konbini stock diapers and baby food. Bring a compact stroller — it fits on trains and most attractions. Many restaurants offer kids\' seats. Coin lockers at major stations store bags so you stay light.' },
    { title: '🍜 No Pork Policy', text: 'Pork is everywhere in Japanese cuisine (ramen broth, gyoza, tonkatsu). Always ask "butaniku nashi de onegaishimasu" (no pork please) or show a written card. Chicken, beef, seafood, and vegetable options are plentiful. The restaurants in this itinerary are chosen with pork-free options available.' },
    { title: '🎫 Book in Advance', text: 'teamLab Planets, Shibuya Sky, Kirby Café, and Pokémon Cafe Osaka all require advance booking and sell out. Book 2-4 weeks ahead. Kimono photoshoots in Kyoto also fill up in May.' },
    { title: '🌤️ May Weather', text: 'May is ideal — warm (20-25°C), low humidity, mostly sunny. Light layers work. Late May can see early rainy season in Kansai. Pack a compact umbrella and rain cover for the stroller.' }
  ],

  days: [
    // ============ DAY 1 — May 15 (Fri) — Arrival ============
    {
      num: 1,
      date: '2026-05-15',
      neighborhoods: 'Narita · Shinjuku',
      title: 'Arrival — Welcome to Tokyo',
      description: "You land at Narita around 1 PM and head straight to your Shinjuku Airbnb. After dropping bags and freshening up, ease into Tokyo with a first-night dinner at Omoide Yokocho's atmospheric yakitori alleys, then explore the legendary tiny bars of Golden Gai. The jet lag won't know what hit it.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive at Narita International Airport (NRT)',
              description: 'Welcome to Japan! After clearing immigration and customs, pick up your Suica/PASMO IC cards and pocket WiFi at the airport. Take the Narita Express (N\'EX) directly to Shinjuku Station — about 80 minutes, smooth and comfortable with luggage space.',
              details: [
                '✈️ Landing ~1:00 PM — allow 45-60 min for immigration',
                '🎫 Buy Suica cards at the JR ticket machines in the arrivals hall',
                '📶 Pick up pocket WiFi or activate eSIM (ordered in advance)',
                '🚃 Narita Express to Shinjuku: ~80 min, ¥3,250/adult'
              ]
            },
            {
              title: 'Check into Shinjuku Airbnb',
              description: 'Drop your bags, get the kids settled, and freshen up. Take a quick walk around the neighborhood to orient yourselves — find the nearest konbini (convenience store) for snacks, drinks, and any essentials.',
              details: [
                '🏠 Shinjuku is your home base for 5 nights',
                '🏪 FamilyMart and 7-Eleven are everywhere — stock up on onigiri, drinks, baby supplies',
                '💤 Let the toddlers rest if needed — tonight is a late one'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Japanese konbini are a revelation — fresh onigiri, egg sandwiches, matcha lattes, diapers, and even decent wine. Your toddlers will love the character-themed snacks.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Omoide Yokocho (Memory Lane)',
              description: 'Your first taste of old Tokyo — narrow alleys packed with tiny yakitori stalls under paper lanterns. The atmosphere is pure magic, especially at dusk when the smoke and lantern light create an almost dreamlike scene. Order chicken skewers (no pork!) and cold beer while the kids marvel at the sizzling grills.',
              details: [
                '📍 Right next to Shinjuku Station West Exit — 2-minute walk',
                '🍗 Stick to chicken (yakitori), beef, and seafood skewers — skip tonkatsu',
                '🕖 Best atmosphere from 6-9 PM',
                '👶 Tight spaces but toddlers in carriers/strollers can manage the wider alleys'
              ]
            },
            {
              title: 'Shinjuku Golden Gai',
              description: 'A labyrinth of over 200 tiny bars crammed into six narrow alleys — each seating 5-10 people. Even if you don\'t drink, walking through the neon-lit passages is an experience. Some bars welcome families in the early evening hours before it gets rowdy.',
              details: [
                '🌃 5-minute walk from Omoide Yokocho',
                '🍺 Some bars charge a cover (¥500-1000) — check the door signs',
                '📸 The alleyways are incredibly photogenic after dark',
                '⏰ Visit early (7-9 PM) with kids — gets more adult-oriented later'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Golden Gai is best experienced as a walk-through with toddlers. The neon signs and tiny doorways are fascinating even from the outside. Save a proper bar crawl for another trip!' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7647, lng: 139.7713, label: 'Narita International Airport', num: 1, cat: 'transport', desc: 'Arrival point — pick up Suica cards and N\'EX tickets' },
        { lat: 35.6938, lng: 139.7034, label: 'Shinjuku Airbnb', num: 2, cat: 'hotel', desc: 'Home base for 5 nights' },
        { lat: 35.6936, lng: 139.6987, label: 'Omoide Yokocho', num: 3, cat: 'food', desc: 'Atmospheric yakitori alleys — first night dinner' },
        { lat: 35.6942, lng: 139.7038, label: 'Shinjuku Golden Gai', num: 4, cat: 'nightlife', desc: '200+ tiny bars in neon alleys' }
      ]
    },

    // ============ DAY 2 — May 16 (Sat) — Shinjuku & Harajuku ============
    {
      num: 2,
      date: '2026-05-16',
      neighborhoods: 'Meiji Jingu · Harajuku · Omotesandō · Shinjuku',
      title: 'Shrines, Soufflé Pancakes & Neon Nights',
      description: "Start with the serene forest paths of Meiji Jingu shrine, then dive into Harajuku's wild fashion scene and Takeshita Street chaos. Refuel with impossibly fluffy soufflé pancakes, stroll through Yoyogi Park, and finish at the stunning Shinjuku Gyoen gardens. Evening brings Don Quijote shopping madness and Kabukicho neon.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Meiji Jingu',
              description: 'Tokyo\'s most important Shinto shrine sits in a 170-acre forest that feels like another world — just minutes from Harajuku\'s chaos. Walk the wide gravel path under towering camphor trees, cleanse your hands at the temizuya, and make a wish at the main hall. The toddlers will love the wide open spaces and forest atmosphere.',
              details: [
                '🕘 Arrive by 9:00 AM for peaceful morning light and thin crowds',
                '⛩️ Free entry — the approach walk takes 10-15 minutes',
                '🌳 The forest was planted 100 years ago with 100,000 donated trees',
                '👶 Stroller-friendly gravel paths (wide and flat)'
              ]
            },
            {
              title: 'Harajuku & Takeshita Street',
              description: 'The epicenter of Tokyo youth culture — a narrow pedestrian street packed with quirky fashion shops, crepe stands, cotton candy bigger than your head, and every color of the rainbow. The kids will be mesmerized by the sensory overload.',
              details: [
                '🛍️ 10:30 AM — starts filling up by midday',
                '🍦 Try a Harajuku crepe — the whipped cream ones are enormous',
                '👗 Brandy Melville is on nearby Cat Street',
                '📍 3-minute walk from Meiji Jingu\'s Harajuku exit'
              ]
            },
            {
              title: 'ONE PIECE Mugiwara Store Harajuku',
              description: 'A haven for One Piece fans — official merchandise, exclusive store-only items, and character displays. Even if you\'re not a mega-fan, the store is fun to browse with its pirate-themed décor.',
              details: [
                '🏴‍☠️ On Takeshita-dori or nearby — check current location',
                '🛒 Exclusive Harajuku-only merchandise available',
                '⏱️ 20-30 minutes to browse'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Hit Meiji Jingu first, then walk straight through to Takeshita Street — they\'re connected. This natural flow avoids backtracking.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'A Happy Pancake Omotesandō',
              description: 'Japan\'s famous soufflé pancakes — impossibly fluffy, jiggly, and topped with whipped butter and syrup. These are nothing like regular pancakes. The kids will be hypnotized watching them wobble. Worth the wait.',
              details: [
                '🥞 Arrive by 1:00 PM — waits can be 30-60 min on weekends',
                '📍 Omotesandō area, short walk from Takeshita Street',
                '🍽️ No pork on the menu — pancakes are the star',
                '💰 ~¥1,500-2,000 per serving'
              ]
            },
            {
              title: 'Yoyogi Park',
              description: 'A massive green space perfect for letting toddlers run free after a morning of structured sightseeing. On weekends you might catch street performers, cosplayers, or musicians. Spread a blanket and breathe.',
              details: [
                '🌳 Free entry — open space right next to Harajuku',
                '👶 Great for toddler energy burn — wide lawns, shaded areas',
                '🎵 Weekend buskers and performers near the entrance',
                '⏱️ 30-60 minutes depending on kids\' energy'
              ]
            },
            {
              title: 'Shinjuku Gyoen National Garden',
              description: 'One of Tokyo\'s finest gardens — 144 acres of Japanese, English, and French landscape gardens. In May, the roses are blooming and the greenhouse tropical plants are lush. A perfect serene contrast to the morning\'s chaos.',
              details: [
                '🌹 ¥500/adult, free for kids — open until 6 PM (last entry 5:30)',
                '🍱 No alcohol allowed — family-friendly atmosphere',
                '📍 10-minute walk from Shinjuku Station',
                '👶 Stroller-friendly paved paths throughout'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Shinjuku Gyoen is a perfect toddler nap spot — the gardens are peaceful and shaded. Time it for post-lunch sleepiness.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Don Quijote Shinjuku',
              description: 'Japan\'s legendary discount store — a multi-floor chaotic wonderland of snacks, beauty products, electronics, toys, costumes, and souvenirs. The "Donki" experience is a rite of passage. Stock up on Kit-Kat flavors and character goods.',
              details: [
                '🏬 Open 24 hours — Shinjuku location is massive',
                '💰 Tax-free shopping for tourists (bring passport)',
                '🎭 Each floor is a different theme of organized chaos',
                '⏱️ Easy to spend 1-2 hours here'
              ]
            },
            {
              title: '3D Cat at Cross Shinjuku Vision',
              description: 'A massive 3D digital billboard featuring a hyper-realistic calico cat that appears to leap out of the screen. The toddlers will lose their minds. Quick stop but absolutely worth it.',
              details: [
                '🐱 Shinjuku Station East Exit — above the Cross Shinjuku building',
                '📸 Cat appears at various intervals — catch it on the hour',
                '⏱️ 5-10 minute photo op'
              ]
            },
            {
              title: 'Kabukicho & Shinjuku Kabuki Yokocho',
              description: 'Tokyo\'s neon entertainment district — transformed from its seedier past into a vibrant food and entertainment zone. Kabuki Yokocho (横丁) is a retro-themed food hall with various stalls. Safe for families in the early evening.',
              details: [
                '🌃 Neon-soaked streets — incredible for photos',
                '🍜 Kabuki Yokocho has ramen, udon, and yakitori stalls (ask for no pork)',
                '👶 Fine with kids before 9 PM — gets rowdier later',
                '📍 5-minute walk from Shinjuku Station East Exit'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The SURUGA-YA Shinjuku Marui Annex (secondhand anime goods) and Seria Shinjuku Marui Annex (100-yen shop) are both in the Marui Annex building near Shinjuku Station East — hit them during the Don Quijote run or save them for Day 9.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6764, lng: 139.6993, label: 'Meiji Jingu', num: 1, cat: 'shrine', desc: 'Serene forest shrine — arrive by 9 AM' },
        { lat: 35.6715, lng: 139.7030, label: 'Takeshita Street', num: 2, cat: 'shopping', desc: 'Harajuku fashion, crepes & quirky shops' },
        { lat: 35.6697, lng: 139.7050, label: 'ONE PIECE Mugiwara Store', num: 3, cat: 'shopping', desc: 'Official One Piece merchandise' },
        { lat: 35.6651, lng: 139.7123, label: 'A Happy Pancake Omotesandō', num: 4, cat: 'food', desc: 'Famous soufflé pancakes' },
        { lat: 35.6717, lng: 139.6949, label: 'Yoyogi Park', num: 5, cat: 'park', desc: 'Green space for toddler energy burn' },
        { lat: 35.6852, lng: 139.7100, label: 'Shinjuku Gyoen', num: 6, cat: 'park', desc: 'Beautiful Japanese, English & French gardens' },
        { lat: 35.6941, lng: 139.7012, label: 'Don Quijote Shinjuku', num: 7, cat: 'shopping', desc: 'Legendary discount store — souvenir heaven' },
        { lat: 35.6940, lng: 139.7039, label: '3D Cat Cross Shinjuku', num: 8, cat: 'attraction', desc: 'Hyper-realistic 3D cat billboard' },
        { lat: 35.6954, lng: 139.7036, label: 'Kabukicho', num: 9, cat: 'food', desc: 'Neon entertainment district & Kabuki Yokocho food hall' }
      ]
    },

    // ============ DAY 3 — May 17 (Sun) — Shibuya & Ginza ============
    {
      num: 3,
      date: '2026-05-17',
      neighborhoods: 'Tsukiji · Ginza · Shibuya',
      title: 'Fish Markets, Art Aquarium & Shibuya Sky at Sunset',
      description: "A day of contrasts — morning street food at the legendary Tsukiji Market, mesmerizing goldfish art in Ginza, matcha everything at a dedicated matcha café, then an afternoon conquering Shibuya's iconic crossing before watching sunset from 230 metres up at Shibuya Sky.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tsukiji Outer Market',
              description: 'The original fish market\'s outer market is still very much alive — dozens of stalls serving the freshest sushi, tamagoyaki (sweet egg omelette), grilled seafood on sticks, and fresh fruit. This is breakfast, Tokyo style. The kids can try tamago on a stick — sweet, warm, and universally loved.',
              details: [
                '🐟 Arrive by 9:30 AM — best selection and freshest food',
                '🍣 Must-try: tamagoyaki, fresh sushi, grilled scallops, melon on a stick',
                '🚫 No pork items — stick to seafood stalls',
                '👶 Stroller-navigable but tight — consider carrier for peak times'
              ]
            },
            {
              title: 'ART AQUARIUM MUSEUM (Ginza)',
              description: 'A stunning fusion of art and aquarium — thousands of goldfish swimming in elaborately designed glass tanks illuminated with ever-changing lights. It\'s like walking through a living painting. The toddlers will be absolutely mesmerized by the colors and movement.',
              details: [
                '🐠 11:00 AM — Ginza Mitsukoshi area',
                '📸 Dark venue with dramatic lighting — incredible photos',
                '💰 ~¥2,300/adult, kids under 3 free',
                '⏱️ Allow 60-90 minutes'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Tsukiji Outer Market and the old Tsukiji site are different from Toyosu Market (where the wholesale auctions moved). You want the Outer Market — it\'s the street food paradise.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Godaime Hanayama Udon (Ginza)',
              description: 'Thick, chewy sanuki-style udon in a stylish Ginza setting. The noodles are hand-cut and the broth is rich without relying on pork. A satisfying, toddler-friendly lunch.',
              details: [
                '🍜 12:30 PM — near Art Aquarium in Ginza',
                '🚫 Ask for chicken or seafood-based broth (no tonkotsu)',
                '👶 Udon is perfect toddler food — soft, fun to slurp'
              ]
            },
            {
              title: 'Matcha Cafe Wabisabi (Higashi-Ginza)',
              description: 'A matcha-dedicated café where everything is matcha — lattes, soft serve, tiramisu, parfaits. The green intensity is photogenic and the flavors are genuinely excellent. Get the matcha soft serve for the kids.',
              details: [
                '🍵 2:00 PM — short walk from lunch',
                '📸 The all-green aesthetic is very Instagram-worthy',
                '💰 Drinks ¥600-900, desserts ¥800-1,200'
              ]
            },
            {
              title: 'Shibuya Crossing',
              description: 'Stand in the middle of the world\'s busiest pedestrian crossing — up to 3,000 people cross at once when the light changes. It\'s organized chaos and an absolute must-experience. The Starbucks overlooking the crossing has a prime viewing spot.',
              details: [
                '🚶 3:30 PM — busiest in afternoon/evening',
                '📸 Best viewing: Starbucks 2F at Shibuya Tsutaya, or Magnet by 109 rooftop',
                '👶 Hold toddlers\' hands or use carrier during the actual crossing'
              ]
            },
            {
              title: 'MAGNET by SHIBUYA109',
              description: 'Head to the rooftop of this Shibuya landmark for a bird\'s-eye view of the scramble crossing below. The building also has shopping floors worth browsing.',
              details: [
                '🏙️ Rooftop observation area — free or cheap entry',
                '📸 Perfect overhead view of Shibuya Crossing',
                '⏱️ 15-20 minutes for photos'
              ]
            },
            {
              title: 'Pokémon Center Shibuya',
              description: 'One of the biggest Pokémon stores in Tokyo — exclusive Shibuya merchandise, plushies galore, and interactive displays. The kids will think they\'ve entered paradise.',
              details: [
                '📍 Inside Shibuya PARCO (5F)',
                '🛒 Shibuya-exclusive merchandise with Mewtwo theme',
                '⏱️ 30-45 minutes to browse and shop'
              ]
            },
            {
              title: 'CAFE REISSUE',
              description: 'A cozy Shibuya café famous for latte art — they\'ll draw any character you request on your coffee. The toddlers will love watching the barista work their magic.',
              details: [
                '☕ Character latte art on request',
                '📸 Very photogenic — popular on social media',
                '💰 Drinks ¥800-1,200'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The Shibuya Character Street Marathon — Pokémon Center, Nintendo Store, and various character shops — are all in or near Shibuya PARCO. Do them in one sweep.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shibuya Sky',
              description: 'Tokyo\'s most dramatic observation deck — an open-air rooftop at 230 metres with 360-degree views. Time your visit for sunset and watch Tokyo transform from a daytime cityscape into an infinite grid of lights. The glass-edged platform and sky-edge hammocks are thrilling.',
              details: [
                '🌅 7:30 PM — book sunset slot in advance (sells out!)',
                '💰 ¥2,000/adult, ¥1,000 ages 3-5, under 3 free',
                '📸 Bring your camera — golden hour views are unreal',
                '🎫 Book at shibuya-sky.tokyo well in advance'
              ]
            },
            {
              title: 'PEANUTS Cafe Sunny Side Kitchen',
              description: 'A charming Snoopy-themed restaurant in Shibuya with character-shaped meals and themed desserts. Perfect family dinner spot — the kids will love eating from Snoopy plates.',
              details: [
                '🐕 9:00 PM dinner — or earlier if the kids are fading',
                '📍 Near Shibuya Station',
                '🍽️ Themed meals and desserts — check for no-pork options',
                '💰 ¥1,500-2,500 per person'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Book Shibuya Sky for 30 minutes before sunset — you get both the golden hour and the night view in one visit. May sunset is around 6:40 PM.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6654, lng: 139.7707, label: 'Tsukiji Outer Market', num: 1, cat: 'food', desc: 'Street food breakfast — sushi, tamagoyaki, grilled seafood' },
        { lat: 35.6693, lng: 139.7639, label: 'Art Aquarium Museum', num: 2, cat: 'museum', desc: 'Goldfish art installation — mesmerizing for kids' },
        { lat: 35.6706, lng: 139.7648, label: 'Godaime Hanayama Udon', num: 3, cat: 'food', desc: 'Thick hand-cut sanuki udon in Ginza' },
        { lat: 35.6694, lng: 139.7677, label: 'Matcha Cafe Wabisabi', num: 4, cat: 'food', desc: 'Matcha everything — lattes, soft serve, parfaits' },
        { lat: 35.6595, lng: 139.7004, label: 'Shibuya Crossing', num: 5, cat: 'attraction', desc: 'World\'s busiest crossing — 3,000 people at once' },
        { lat: 35.6610, lng: 139.6990, label: 'MAGNET by SHIBUYA109', num: 6, cat: 'attraction', desc: 'Rooftop view of Shibuya Crossing' },
        { lat: 35.6620, lng: 139.6983, label: 'Pokémon Center Shibuya', num: 7, cat: 'shopping', desc: 'Huge Pokémon store in PARCO — Mewtwo exclusive' },
        { lat: 35.6601, lng: 139.6969, label: 'CAFE REISSUE', num: 8, cat: 'food', desc: 'Character latte art café' },
        { lat: 35.6584, lng: 139.7023, label: 'Shibuya Sky', num: 9, cat: 'attraction', desc: 'Open-air observation deck at 230m — sunset views' },
        { lat: 35.6610, lng: 139.6961, label: 'PEANUTS Cafe Sunny Side Kitchen', num: 10, cat: 'food', desc: 'Snoopy-themed family dinner' }
      ]
    },

    // ============ DAY 4 — May 18 (Mon) — Asakusa & Ikebukuro ============
    {
      num: 4,
      date: '2026-05-18',
      neighborhoods: 'Asakusa · Akasaka · Ikebukuro',
      title: 'Ancient Temples, Pokémon & the Kirby Café',
      description: "Begin at Tokyo's oldest temple before the crowds arrive, hunt for ichigo daifuku on Nakamise-dori, then head to Ikebukuro for an afternoon of anime shopping at Sunshine City — hitting the Pokémon Center Mega Tokyo, Ghibli Store, and the legendary Kirby Café. End the day soaking at Toyosu Manyo Club.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sensō-ji Temple & Nakamise-dori',
              description: 'Tokyo\'s oldest temple (built 628 AD) is magnificent at any time, but arrive by 8:30 AM and you\'ll have the massive Thunder Gate (Kaminarimon) and five-story pagoda nearly to yourself. Walk Nakamise-dori shopping street for traditional snacks — the ichigo daifuku (strawberry mochi) from the stalls here is legendary.',
              details: [
                '⛩️ 8:30 AM — free entry, always open',
                '🍓 Hunt for ichigo daifuku at Asakusa Ichigo-za or Ginkadō on Nakamise-dori',
                '📸 The massive red lantern at Kaminarimon is THE Tokyo photo',
                '👶 Wide paths, stroller-friendly, lots to see and touch'
              ]
            },
            {
              title: 'Wagyu Ichinoya (near Sensō-ji)',
              description: 'Treat the family to an early wagyu experience — tender, melt-in-your-mouth beef served in various styles. No pork on the menu when you order beef sets. The kids can share a rice bowl.',
              details: [
                '🥩 10:00 AM — near Senso-ji area',
                '💰 ¥2,000-5,000 for lunch wagyu sets',
                '🚫 Order beef only — wagyu doesn\'t need pork accompaniment'
              ]
            },
            {
              title: 'UNIQLO Asakusa',
              description: 'A quick shopping stop — Japan\'s UNIQLO stores carry exclusive items you won\'t find abroad. Stock up on kids\' clothes, character collaborations, and those famous AIRism undershirts.',
              details: [
                '👕 11:00 AM — 20-30 minute browse',
                '🛒 Japan-exclusive UT graphic tees and kids\' line',
                '💰 Generally cheaper than UNIQLO abroad'
              ]
            },
            {
              title: 'Hie-jinja Shrine',
              description: 'A beautiful hilltop shrine with a dramatic tunnel of red torii gates reminiscent of (but much less crowded than) Fushimi Inari. The elevator makes it accessible, and the peaceful grounds are a nice contrast to Asakusa\'s bustle.',
              details: [
                '⛩️ 11:30 AM — en route from Asakusa toward central Tokyo',
                '🔴 Red torii gate tunnel — great photo opportunity',
                '🛗 Elevator available — toddler and stroller friendly',
                '⏱️ 20-30 minutes'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The ichigo daifuku near Senso-ji is seasonal — May is right at the tail end of strawberry season. Get it early before they sell out!' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Sunshine City (Ikebukuro)',
              description: 'A massive entertainment and shopping complex — aquarium, observation deck, Namco arcade, and tons of character shops. It\'s a one-stop afternoon destination, especially with kids who need variety.',
              details: [
                '🏢 1:30 PM — Ikebukuro East Exit area',
                '🎮 Multiple floors of shopping, entertainment, and dining',
                '👶 Indoor and climate-controlled — perfect for any weather'
              ]
            },
            {
              title: 'Pokémon Center Mega Tokyo & Pikachu Sweets',
              description: 'THE flagship Pokémon store — the biggest in Tokyo. Massive plushie walls, exclusive merchandise, and the attached Pikachu Sweets café serves Pokémon-themed desserts and drinks. This is the one to visit.',
              details: [
                '📍 Sunshine City Alpa 2F — in the Ikebukuro complex',
                '🧸 Exclusive Mega Tokyo merchandise',
                '🍰 Pikachu Sweets: character pancakes, drinks, and cakes',
                '⏱️ Allow 45-60 minutes (shopping + café combined)'
              ]
            },
            {
              title: 'KIDDY LAND Ikebukuro',
              description: 'A toy and character goods store that\'s pure joy for kids — Sanrio, Disney, Studio Ghibli, and more. Great for picking up unique toys you won\'t find outside Japan.',
              details: [
                '🧸 3:30 PM — near Sunshine City',
                '🛒 Japanese character toys and exclusive items',
                '⏱️ 20-30 minutes'
              ]
            },
            {
              title: 'Donguri Kyowakoku (Ghibli Store)',
              description: 'The official Studio Ghibli merchandise store — Totoro, Kiki, Spirited Away, and more. Plushies, accessories, home goods, and beautifully crafted items that feel like pieces of the Ghibli universe.',
              details: [
                '🏪 4:00 PM — inside Sunshine City or nearby',
                '🧸 Totoro and No-Face plushies are the top sellers',
                '🎁 Beautiful gift items — high quality, unique to Japan',
                '⏱️ 20-30 minutes'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Ikebukuro is also home to tons of anime shops along Otome Road if you want to explore more character goods beyond Sunshine City.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Kirby Café',
              description: 'A cafe entirely themed around Kirby — the pink puffball from Nintendo. Every dish is shaped like Kirby characters, from pasta to parfaits. The attention to detail is incredible and kids absolutely lose it. Reservations are MANDATORY and book out weeks in advance.',
              details: [
                '🩷 6:00 PM — MUST book at kirbycafe.jp well in advance',
                '📍 Tokyo Solamachi (Tokyo Skytree complex) — plan travel time',
                '🍝 Full themed menu — check for pork-free options when booking',
                '💰 ¥2,500-3,500 per person including mandatory drink order',
                '⏱️ 80-minute dining window (timed reservations)'
              ]
            },
            {
              title: 'Toyosu Manyo Club',
              description: 'The perfect way to end a big day — a 24-hour hot spring resort with indoor and outdoor baths, restaurants, relaxation rooms, and panoramic views. Natural hot spring water is trucked in from Hakone. Kids can use the baths, and there\'s a rest area if the toddlers fall asleep.',
              details: [
                '♨️ 8:00 PM — stay as long as you like (24 hours)',
                '💰 ¥3,850/adult, kids around ¥1,800',
                '🧖 Separate bathing (nude, gender-separated) — family baths available',
                '👶 Toddlers welcome in family bathing areas',
                '📍 Toyosu area — near teamLab (which is Day 5)'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Book Kirby Café the moment reservations open (usually 1st of the month, 2 months ahead). They sell out in minutes. Have someone ready to grab slots at midnight JST.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: 'Sensō-ji Temple', num: 1, cat: 'shrine', desc: 'Tokyo\'s oldest temple — arrive by 8:30 AM' },
        { lat: 35.7130, lng: 139.7959, label: 'Nakamise-dori (Ichigo Daifuku)', num: 2, cat: 'food', desc: 'Strawberry mochi and traditional snacks' },
        { lat: 35.7122, lng: 139.7938, label: 'Wagyu Ichinoya', num: 3, cat: 'food', desc: 'Wagyu beef lunch near Senso-ji' },
        { lat: 35.7108, lng: 139.7960, label: 'UNIQLO Asakusa', num: 4, cat: 'shopping', desc: 'Japan-exclusive items' },
        { lat: 35.6751, lng: 139.7407, label: 'Hie-jinja Shrine', num: 5, cat: 'shrine', desc: 'Hilltop shrine with red torii tunnel' },
        { lat: 35.7292, lng: 139.7191, label: 'Sunshine City', num: 6, cat: 'shopping', desc: 'Entertainment complex in Ikebukuro' },
        { lat: 35.7289, lng: 139.7195, label: 'Pokémon Center Mega Tokyo', num: 7, cat: 'shopping', desc: 'Biggest Pokémon store + Pikachu Sweets café' },
        { lat: 35.7285, lng: 139.7188, label: 'Donguri Kyowakoku (Ghibli Store)', num: 8, cat: 'shopping', desc: 'Official Ghibli merchandise' },
        { lat: 35.6340, lng: 139.8092, label: 'Kirby Café (Tokyo Solamachi)', num: 9, cat: 'food', desc: 'Kirby-themed café — book way in advance' },
        { lat: 35.6465, lng: 139.7942, label: 'Toyosu Manyo Club', num: 10, cat: 'relaxation', desc: '24-hour hot spring resort — Hakone water' }
      ]
    },

    // ============ DAY 5 — May 19 (Tue) — Cat Temple, Skytree & teamLab ============
    {
      num: 5,
      date: '2026-05-19',
      neighborhoods: 'Setagaya · Shiba · Sumida · Toyosu',
      title: 'Lucky Cats, Tokyo Tower & teamLab Planets',
      description: "Your last full day in Tokyo takes you from the enchanting cat temple of Gōtokuji to Tokyo Tower's classic views, then plunges you (literally) into the barefoot wonder of teamLab Planets. Finish with sunset views from Tokyo Skytree and a free nighttime panorama from the Metropolitan Government Building.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Gōtokuji Temple',
              description: 'The birthplace of the maneki-neko (beckoning cat) — thousands of white cat figurines line the temple grounds, left by visitors whose wishes were granted. It\'s magical, quirky, and unlike anything else in Tokyo. The kids will love counting all the cats.',
              details: [
                '🐱 9:30 AM — quiet residential neighborhood in Setagaya',
                '📸 The display of thousands of cat figurines is surreal',
                '🎎 Buy a small maneki-neko to leave as your own offering',
                '⏱️ 30-45 minutes — include the walk through the grounds'
              ]
            },
            {
              title: 'Prince Shiba Park',
              description: 'A pleasant park right next to Tokyo Tower with views of the tower framed by greenery. Perfect for a quick stroll and letting the kids run around before heading up the tower.',
              details: [
                '🌳 11:00 AM — free, open park near Tokyo Tower',
                '📸 Classic Tokyo Tower photo from the park grounds',
                '👶 Open grass areas for toddlers'
              ]
            },
            {
              title: 'Tokyo Tower',
              description: 'The original Tokyo icon — 333 metres of Eiffel-inspired steel painted in international orange. Less crowded than Skytree and arguably more charming. The main observation deck at 150m gives excellent views, and the tower\'s retro aesthetic is pure nostalgia.',
              details: [
                '🗼 12:00 PM — Main Deck ¥1,200/adult, ¥700 ages 4+',
                '🏙️ Great views toward Shibuya and Rainbow Bridge',
                '👶 Elevators to the top — fully accessible',
                '⏱️ 30-45 minutes including observation deck'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Gōtokuji is off the typical tourist trail — the train ride through residential Setagaya is a nice glimpse of everyday Tokyo life.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'teamLab Planets TOKYO DMM',
              description: 'Walk barefoot through rooms of water, digital flowers, and infinite mirror universes. This is immersive art at its absolute best — you wade through knee-deep water with digital koi swimming around your feet, lie in fields of projected flowers, and lose all sense of space in infinity rooms. The toddlers will be in awe (and love splashing).',
              details: [
                '🎨 2:00 PM — MUST book at planets.teamlab.art in advance',
                '👣 You go barefoot — roll up pants above knees for water rooms',
                '👶 Toddlers love the water rooms — bring a change of clothes',
                '💰 ¥3,800/adult, free for ages 3 and under',
                '⏱️ Allow 90-120 minutes',
                '📍 Toyosu area — close to Toyosu Manyo Club from last night'
              ]
            },
            {
              title: 'Tokyo Skytree',
              description: 'At 634 metres, it\'s the tallest structure in Japan and the tallest tower in the world. The observation decks at 350m and 450m offer views up to 70km on clear days — you can see Mt. Fuji. The surrounding Solamachi shopping mall has great stores.',
              details: [
                '🏙️ 4:30 PM — Tembo Deck ¥2,100/adult, ¥950 ages 4-5',
                '📍 Connected to Tokyo Solamachi (where Kirby Café is)',
                '🌅 Good time for pre-sunset golden light',
                '👶 Elevators only — very accessible'
              ]
            },
            {
              title: 'Oyokogawa Shinsui Park',
              description: 'A peaceful riverside park right near Skytree — walking paths along a restored canal. A nice decompression spot after the Skytree visit, and the toddlers can stretch their legs.',
              details: [
                '🌊 Near Skytree — short walk',
                '🌸 Riverside walking path with seasonal plants',
                '⏱️ 15-20 minutes for a quick stroll'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'teamLab Planets provides towels and has lockers for your shoes/bags. Wear shorts or easily rollable pants. The water rooms are the highlight — don\'t rush through them.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dinner — Wagyu or Halal Steak (Harajuku/Shibuya area)',
              description: 'Final Tokyo dinner — go big with wagyu. Several halal-friendly and pork-free wagyu restaurants in the Harajuku/Shibuya area offer premium beef without pork accompaniments.',
              details: [
                '🥩 7:00 PM — book a wagyu restaurant in advance',
                '🚫 Request no pork — wagyu sets typically come with beef, rice, and veggies',
                '💰 ¥4,000-8,000 for quality wagyu dinner sets'
              ]
            },
            {
              title: 'Tokyo Metropolitan Government Building (Free Observation)',
              description: 'A hidden gem — the North Observation Deck is FREE and offers panoramic night views of Tokyo rivaling any paid deck. At 202m, you can see Shinjuku\'s neon grid, Tokyo Tower, and Skytree all at once. Open some evenings until 11 PM.',
              details: [
                '🏢 8:30 PM — FREE entry',
                '📍 Shinjuku — 10-minute walk from your Airbnb',
                '🌃 Night views are spectacular and completely free',
                '⏱️ 20-30 minutes',
                '⚠️ Check operating hours — may close some evenings for maintenance'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The Metropolitan Government Building observation deck is one of Tokyo\'s best-kept secrets. Free, less crowded than Shibuya Sky, and the views are just as good. Perfect for your last night in Shinjuku.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6596, lng: 139.6477, label: 'Gōtokuji Temple', num: 1, cat: 'shrine', desc: 'Cat temple — thousands of maneki-neko figurines' },
        { lat: 35.6578, lng: 139.7478, label: 'Prince Shiba Park', num: 2, cat: 'park', desc: 'Park with Tokyo Tower views' },
        { lat: 35.6586, lng: 139.7454, label: 'Tokyo Tower', num: 3, cat: 'attraction', desc: '333m icon — observation deck at 150m' },
        { lat: 35.6426, lng: 139.7876, label: 'teamLab Planets', num: 4, cat: 'museum', desc: 'Barefoot immersive digital art — book ahead!' },
        { lat: 35.7101, lng: 139.8107, label: 'Tokyo Skytree', num: 5, cat: 'attraction', desc: 'Tallest tower in the world — 634m' },
        { lat: 35.7043, lng: 139.8129, label: 'Oyokogawa Shinsui Park', num: 6, cat: 'park', desc: 'Riverside park near Skytree' },
        { lat: 35.6896, lng: 139.6917, label: 'Tokyo Metropolitan Government Building', num: 7, cat: 'attraction', desc: 'FREE night observation deck — 202m' }
      ]
    },

    // ============ DAY 6 — May 20 (Wed) — Travel to Kansai + Nara Day Trip ============
    {
      num: 6,
      date: '2026-05-20',
      neighborhoods: 'Tokyo Station · Nara · Kyoto · Gion',
      title: 'Bullet Train West — Nara\'s Deer & Kyoto by Night',
      description: "Say goodbye to Tokyo and ride the Shinkansen west to the ancient capital region. Spend the afternoon in Nara feeding the sacred deer, tasting ice cream bouquets at Bōkusui Market, and strolling the botanical gardens. Settle into Osaka in the evening and head to Kyoto's atmospheric Gion district for dinner.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinkansen: Tokyo → Kyoto',
              description: 'Board the Nozomi bullet train at Tokyo Station and watch Japan blur past at 300 km/h. The 2-hour-15-minute ride passes through the countryside with glimpses of Mt. Fuji on clear days (sit on the right side, window seats in rows D/E). Arrive Kyoto Station and store luggage in coin lockers.',
              details: [
                '🚄 7:00 AM departure — arrive Kyoto ~9:15 AM',
                '💰 ¥14,170/adult one-way (or covered by JR Pass if you have one)',
                '🗻 Mt. Fuji visible from right side on clear days (around Shin-Fuji station)',
                '👶 Reserved seats with legroom — kids under 6 ride free on your lap',
                '🍱 Buy ekiben (station bento) at Tokyo Station for breakfast on the train'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Tokyo Station\'s "Gransta" underground mall has incredible ekiben (train bento boxes). Grab different ones for each family member — it\'s part of the bullet train experience.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nara Park & the Sacred Deer',
              description: 'Over 1,000 wild sika deer roam freely through this enormous park — and they bow to you for crackers. It\'s the most magical wildlife experience in Japan for kids. Buy shika senbei (deer crackers, ¥200) from the vendors and watch the toddlers\' faces as deer politely bow and then mob them.',
              details: [
                '🦌 11:00 AM — JR Nara Line from Kyoto, ~45 minutes',
                '🍘 Shika senbei (deer crackers): ¥200 per bundle from park vendors',
                '⚠️ Deer can be pushy — keep toddlers close and supervise feeding',
                '👶 Flat, stroller-friendly paths throughout the park',
                '⏱️ Allow 60-90 minutes in the park'
              ]
            },
            {
              title: 'Bokusui Market (Bōkusui)',
              description: 'A charming market area in Nara known for its ice cream bouquets — scoops of gelato arranged like a flower bouquet. Photogenic, delicious, and absolutely perfect for toddlers who love ice cream (so, all toddlers).',
              details: [
                '🍦 12:30 PM — near Nara Park',
                '📸 The ice cream bouquet is incredibly photogenic',
                '🍨 Various flavors including matcha, strawberry, seasonal fruits',
                '💰 ¥500-800 per bouquet'
              ]
            },
            {
              title: 'Man\'yō Botanical Gardens',
              description: 'A peaceful botanical garden within Nara Park featuring plants mentioned in the ancient Man\'yōshū poetry collection. A serene contrast to the deer chaos — beautiful walking paths through seasonal flowers.',
              details: [
                '🌿 2:00 PM — inside Nara Park grounds',
                '💰 Small entrance fee (~¥500)',
                '⏱️ 30-45 minutes for a peaceful stroll',
                '🌸 May brings irises and other seasonal blooms'
              ]
            },
            {
              title: 'Return to Kyoto / Check into Osaka',
              description: 'Head back from Nara to either Kyoto or Osaka to check in and drop bags. Osaka will be your base camp, but tonight you\'re exploring Kyoto.',
              details: [
                '🚃 4:00 PM — Nara → Osaka: ~50 min by JR or Kintetsu',
                '🏨 Check into your Osaka accommodation',
                '🧳 Drop bags, freshen up, head to Kyoto for dinner'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The deer in Nara are wild animals — teach the toddlers to hold crackers flat-palmed like feeding a horse. If a deer gets too aggressive, raise both hands above your head (showing "no food") and they\'ll lose interest.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Men-ya Inoichi Ramen (Kyoto)',
              description: 'A famous Kyoto-style ramen shop known for rich, flavorful broth. Kyoto ramen tends to be chicken-based (tori paitan) rather than pork, making it perfect for your no-pork policy. The thick, creamy chicken broth is outstanding.',
              details: [
                '🍜 6:30 PM — check for chicken broth options (no tonkotsu)',
                '📍 Central Kyoto area',
                '💰 ¥900-1,200 per bowl',
                '👶 Ramen is great toddler food — order plain noodles for kids'
              ]
            },
            {
              title: 'Gion District Evening Stroll',
              description: 'Kyoto\'s most atmospheric neighborhood — traditional wooden machiya townhouses line narrow streets lit by paper lanterns. You might spot a maiko (apprentice geisha) heading to an evening appointment. The stone-paved streets of Hanamikoji-dōri are especially beautiful after dark.',
              details: [
                '🏮 8:00 PM — magical after dark with lantern lighting',
                '👘 Look for maiko (apprentice geisha) heading to engagements',
                '📸 Hanamikoji-dōri is the most photogenic street',
                '🚫 Don\'t photograph maiko without permission — it\'s considered rude',
                '⏱️ 30-60 minutes of wandering'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Kyoto → Osaka is only 15 minutes by Shinkansen or 30 min by regular train. Using Osaka as your base for both Kyoto and Nara day trips is efficient and saves packing/unpacking.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6812, lng: 139.7671, label: 'Tokyo Station', num: 1, cat: 'transport', desc: 'Shinkansen departure — buy ekiben for breakfast' },
        { lat: 34.6851, lng: 135.8430, label: 'Nara Park', num: 2, cat: 'park', desc: '1,000+ sacred deer — buy crackers and watch them bow' },
        { lat: 34.6840, lng: 135.8380, label: 'Bokusui Market', num: 3, cat: 'food', desc: 'Ice cream bouquets — photogenic and delicious' },
        { lat: 34.6820, lng: 135.8460, label: 'Man\'yō Botanical Gardens', num: 4, cat: 'park', desc: 'Peaceful botanical walk with seasonal flowers' },
        { lat: 35.0045, lng: 135.7694, label: 'Men-ya Inoichi Ramen', num: 5, cat: 'food', desc: 'Famous Kyoto ramen — chicken-based broth' },
        { lat: 35.0037, lng: 135.7756, label: 'Gion District', num: 6, cat: 'attraction', desc: 'Lantern-lit geisha district — evening stroll' }
      ]
    },

    // ============ DAY 7 — May 21 (Thu) — Kyoto Full Day ============
    {
      num: 7,
      date: '2026-05-21',
      neighborhoods: 'Fushimi · Arashiyama · Okazaki · Gion',
      title: 'Fushimi Inari at Dawn, Bamboo & Monkeys',
      description: "Kyoto's greatest hits in one unforgettable day — start before dawn at the endless vermilion torii gates of Fushimi Inari, sip matcha at a traditional tea house, then head to Arashiyama for the iconic bamboo forest, a Miffy-themed lunch, quirky stone statues, and monkeys on a mountaintop. Finish with a kimono photoshoot through Gion's lantern-lit streets.",
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            {
              title: 'Fushimi Inari Taisha',
              description: 'Thousands of vermilion torii gates snaking up a mountain — Japan\'s most iconic image. Arrive at dawn (the shrine never closes) and you\'ll have the famous gate tunnels nearly to yourself. Walk as far up as the toddlers allow — even the first 15 minutes is breathtaking. The full loop is 2-3 hours but you can turn back anywhere.',
              details: [
                '⛩️ 7:30 AM — open 24 hours, free entry',
                '🏔️ Full hike: 2-3 hours round trip, 233m elevation',
                '👶 First section is paved and manageable — turn back when kids tire',
                '📸 Best photos: early morning light through the torii gates',
                '🦊 Dedicated to Inari, the fox deity — look for fox statues everywhere'
              ]
            },
            {
              title: 'Rokujūan Tea House',
              description: 'A traditional tea house near Fushimi Inari where you can experience matcha tea the way it was meant to be — whisked by hand and served with a seasonal wagashi sweet. A serene, contemplative experience after the energy of the shrine.',
              details: [
                '🍵 9:30 AM — near Fushimi Inari area',
                '🍡 Matcha + wagashi set: ~¥800-1,200',
                '🧘 Sit on tatami mats — toddlers might find this interesting or squirmy',
                '⏱️ 20-30 minutes'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The torii gates are most photogenic in the first 30 minutes of your visit. After the initial dense tunnel, the gates space out and the path gets steeper. With toddlers, the sweet spot is the first 30-45 minutes.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arashiyama Bamboo Grove',
              description: 'Walk through a cathedral of towering bamboo stalks — they creak and sway in the wind above you, filtering the sunlight into an ethereal green glow. It\'s one of those places that looks exactly like the photos. Midday is busier but still magical.',
              details: [
                '🎋 11:30 AM — from Fushimi, take JR + bus/walk to Arashiyama',
                '📸 Best photos looking up through the bamboo canopy',
                '👶 Paved path, stroller-friendly, about 500m long',
                '⏱️ 15-20 minutes to walk through'
              ]
            },
            {
              title: 'Arashiyama Miffy Sakura Kitchen',
              description: 'A Miffy (Nijntje) themed café in Arashiyama serving adorable character-shaped food — Miffy-shaped bread, themed drinks, and seasonal items. The kids will love it, and the sakura (cherry blossom) theme is extra charming.',
              details: [
                '🐰 12:30 PM — lunch in Arashiyama main street area',
                '🍞 Miffy-shaped bread and character drinks',
                '💰 ¥800-1,500 per person',
                '📸 Extremely cute and photogenic'
              ]
            },
            {
              title: 'Kimono Forest',
              description: 'Right at Arashiyama Station — 600 pillars wrapped in colorful kimono fabric that glow beautifully when lit. It\'s a free, open-air art installation that\'s particularly stunning in the afternoon light.',
              details: [
                '👘 1:30 PM — Randen Arashiyama Station, free',
                '📸 600 illuminated kimono fabric pillars',
                '⏱️ 10-15 minutes for photos'
              ]
            },
            {
              title: 'Otagi Nenbutsu-ji',
              description: 'A hidden gem temple with over 1,200 unique stone statues (rakan) — each carved by a different amateur sculptor, so they have wildly different expressions: laughing, crying, meditating, playing instruments, holding cats. It\'s whimsical, quirky, and kids LOVE finding their favorite faces.',
              details: [
                '🗿 2:00 PM — 20-minute walk from bamboo grove (or short taxi)',
                '💰 ¥300 entry',
                '📸 Every statue is unique — some are hilarious',
                '👶 Uneven stone paths — carrier better than stroller here',
                '⏱️ 30-45 minutes exploring and statue-hunting'
              ]
            },
            {
              title: 'Arashiyama Monkey Park Iwatayama',
              description: 'Hike up a short trail (about 20 minutes) to a mountainside park where wild Japanese macaques roam free. You get panoramic views of Kyoto and can feed the monkeys from inside a fenced shelter (so you\'re in the cage, not them). The toddlers will go bananas.',
              details: [
                '🐒 3:30 PM — entrance near Togetsukyo Bridge',
                '💰 ¥550/adult, ¥250/child',
                '🏔️ 20-minute uphill walk — consider carrier for toddlers',
                '🌆 Amazing panoramic views of Kyoto from the top',
                '🍎 Buy monkey food (¥100) at the shelter to feed them'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Otagi Nenbutsu-ji is often missed by tourists — it\'s a 20-min walk further from the bamboo grove, but it\'s one of Kyoto\'s most unique experiences. The quirky statues are perfect for a game of "find the funniest face" with kids.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Okazaki Sakura Corridor (Canal Walk)',
              description: 'A scenic canal walk near Heian Shrine lined with cherry trees. In May the trees are fully leafed in fresh green — beautiful reflections in the canal water. Take a boat ride if available.',
              details: [
                '🌿 5:30 PM — Okazaki area, near Heian Shrine',
                '🚣 Canal boat rides available seasonally',
                '📸 Beautiful reflections in the water',
                '⏱️ 20-30 minutes'
              ]
            },
            {
              title: 'Kimono Rental & Gion Photoshoot',
              description: 'Dress the whole family in traditional kimono or yukata and walk through Gion\'s atmospheric streets for photos. Many rental shops near Gion offer family sets including kids\' sizes. Book in advance for May — it\'s popular season.',
              details: [
                '👘 7:00 PM — book rental + optional professional photographer',
                '📍 Several rental shops near Gion: Yumeyakata, Wargo, etc.',
                '👶 Toddler-sized kimono available and adorable',
                '💰 ¥3,000-5,000 per person for rental; photographer extra',
                '🌃 Evening Gion is magical in kimono — lantern-lit streets'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The Nishiki Market mentioned in your list is also worth a visit if you have time — it\'s Kyoto\'s kitchen, full of food stalls and local specialties. Could swap for the canal walk if preferred.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari Taisha', num: 1, cat: 'shrine', desc: 'Thousands of vermilion torii gates — arrive at dawn' },
        { lat: 34.9665, lng: 135.7741, label: 'Rokujūan Tea House', num: 2, cat: 'food', desc: 'Traditional matcha + wagashi near Fushimi' },
        { lat: 35.0173, lng: 135.6717, label: 'Arashiyama Bamboo Grove', num: 3, cat: 'attraction', desc: 'Cathedral of towering bamboo' },
        { lat: 35.0155, lng: 135.6730, label: 'Miffy Sakura Kitchen', num: 4, cat: 'food', desc: 'Miffy-themed lunch in Arashiyama' },
        { lat: 35.0141, lng: 135.6745, label: 'Kimono Forest', num: 5, cat: 'attraction', desc: '600 illuminated kimono fabric pillars — free' },
        { lat: 35.0274, lng: 135.6627, label: 'Otagi Nenbutsu-ji', num: 6, cat: 'shrine', desc: '1,200 unique stone statues — hidden gem' },
        { lat: 35.0114, lng: 135.6773, label: 'Monkey Park Iwatayama', num: 7, cat: 'attraction', desc: 'Wild macaques + Kyoto panoramic views' },
        { lat: 35.0126, lng: 135.7845, label: 'Okazaki Sakura Corridor', num: 8, cat: 'park', desc: 'Scenic canal walk near Heian Shrine' },
        { lat: 35.0037, lng: 135.7756, label: 'Gion Kimono Photoshoot', num: 9, cat: 'attraction', desc: 'Kimono rental + lantern-lit Gion streets' }
      ]
    },

    // ============ DAY 8 — May 22 (Fri) — Osaka ============
    {
      num: 8,
      date: '2026-05-22',
      neighborhoods: 'Shinsaibashi · Namba · Dotonbori',
      title: 'Osaka — Pokémon Café, Aquarium & Dotonbori Feast',
      description: "Japan's kitchen city — Osaka is all about eating, and today delivers. Start with Onitsuka Tiger shopping, have the most adorable lunch of your life at Pokémon Cafe, marvel at whale sharks at Kaiyukan Aquarium, then spend the evening in the sensory overload of Dotonbori's neon-lit food stalls.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Arrive & Settle in Osaka',
              description: 'If you stayed in Kyoto, the train to Osaka is only 15-30 minutes. Drop any bags at your accommodation and get ready for a full day of Osaka goodness.',
              details: [
                '🚃 Kyoto → Osaka: 15 min by Shinkansen, 30 min by regular train',
                '📍 Shinsaibashi/Namba area is ideal — walking distance to everything today'
              ]
            },
            {
              title: 'Onitsuka Tiger Store (Shinsaibashi)',
              description: 'The birthplace brand of ASICS — Onitsuka Tiger\'s flagship stores in Japan carry exclusive colorways and Japan-only models. The retro sneakers are beautiful and make great souvenirs.',
              details: [
                '👟 11:00 AM — Shinsaibashi shopping arcade',
                '🛒 Japan-exclusive colorways and models',
                '💰 Generally ¥8,000-15,000 per pair',
                '⏱️ 20-30 minutes'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Shinsaibashi-suji is one of Japan\'s longest shopping arcades — covered and climate-controlled. Perfect for stroller-pushing shopping with toddlers.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Pokémon Cafe Osaka Shinsaibashi',
              description: 'The ultimate Pokémon dining experience — every dish is shaped like a different Pokémon, from Pikachu curry rice to Eevee parfaits. A Pikachu character visits your table for photos. Reservations are MANDATORY and open one month in advance — set an alarm.',
              details: [
                '🐾 12:30 PM — MUST book at pokemoncafe-reservation.com',
                '📍 Shinsaibashi area, Osaka',
                '🍛 Pikachu omurice, character-shaped desserts, themed drinks',
                '💰 ¥1,800-2,500 per person (food + mandatory drink order)',
                '👶 Kids\' menu available — Pokémon plates they can keep',
                '⏱️ 90-minute dining window (strictly timed)',
                '🚫 Check for pork-free options — many dishes use chicken or seafood'
              ]
            },
            {
              title: 'Osaka Aquarium Kaiyukan',
              description: 'One of the world\'s largest aquariums — the centerpiece is a massive tank with whale sharks, manta rays, and thousands of fish that you spiral down around over 8 floors. The scale is jaw-dropping for adults and kids alike. The touch pools let kids pet rays and sharks.',
              details: [
                '🐋 2:00 PM — Tempozan area (15-20 min from Shinsaibashi)',
                '💰 ¥2,700/adult, ¥1,400 ages 4-6, free under 3',
                '🦈 Touch pool: pet bamboo sharks and rays',
                '👶 Stroller-friendly ramps throughout',
                '⏱️ Allow 2-2.5 hours'
              ]
            },
            {
              title: 'Shopping — Shinsaibashi',
              description: 'Browse the shops of Shinsaibashi-suji arcade on your way from the aquarium back toward Dotonbori. Electronics, fashion, souvenirs, and more under a covered arcade.',
              details: [
                '🛍️ 4:30 PM — covered shopping arcade',
                '📍 Connects Shinsaibashi to Namba/Dotonbori',
                '⏱️ 30-60 minutes of browsing'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Pokémon Cafe reservations open on the 1st of each month at 6 PM JST for the following month. They sell out in minutes. Have the booking page loaded and ready.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dotonbori — Glico Sign & Food Stalls',
              description: 'Osaka\'s most iconic street — a canal-side neon strip anchored by the famous Glico Running Man sign. This is where Osaka\'s "eat till you drop" (kuidaore) culture comes alive. The neon reflections in the canal water at night are unforgettable.',
              details: [
                '🌃 6:00 PM — peak atmosphere after dark',
                '📸 THE classic Osaka photo: Glico Running Man sign reflected in the canal',
                '👶 Wide pedestrian streets — stroller-friendly',
                '🎭 Street performers, giant crab signs, and sensory overload'
              ]
            },
            {
              title: 'Immo Pipi Sweet Potato',
              description: 'A wildly popular street stall selling sweet potato desserts — whole baked sweet potatoes with soft serve, sweet potato tarts, and candied sweet potato sticks. The toddlers will devour these.',
              details: [
                '🍠 6:30 PM — Dotonbori area',
                '📸 Purple sweet potato soft serve is the signature',
                '💰 ¥500-800'
              ]
            },
            {
              title: 'Dotonbori Food Crawl',
              description: 'This is what Osaka lives for — eat your way through the stalls. Takoyaki (octopus balls), okonomiyaki (savory pancakes with seafood), kushikatsu (deep-fried skewers — get chicken/seafood/veggie, skip pork), and whatever else catches your eye.',
              details: [
                '🐙 Takoyaki: crispy outside, molten inside — the kids will love them',
                '🥞 Okonomiyaki: ask for seafood version (no pork)',
                '🍢 Kushikatsu: deep-fried skewers — chicken, shrimp, veggie',
                '🚫 Skip tonkatsu (pork cutlet) — plenty of alternatives',
                '💰 Most street food is ¥500-1,000 per item'
              ]
            },
            {
              title: 'FamilyMart / 7-Eleven Run',
              description: 'The Japanese konbini experience is legendary — grab seasonal snacks, limited-edition Kit-Kats, Rilakkuma goods, fried chicken (karaage), and fluffy Japanese milk bread. Stock up for the train ride tomorrow.',
              details: [
                '🏪 9:00 PM — they\'re everywhere and open 24 hours',
                '🍙 Must-try: onigiri, egg sandwich, famichiki, matcha desserts',
                '🍫 Seasonal Kit-Kat flavors only in Japan'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Osaka\'s rule: "kuidaore" — eat until you drop. Pace yourselves through Dotonbori, eat small portions at many stalls, and save room for dessert. The sweet potato at Immo Pipi is not optional.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6745, lng: 135.5020, label: 'Onitsuka Tiger Shinsaibashi', num: 1, cat: 'shopping', desc: 'Japan-exclusive sneakers' },
        { lat: 34.6720, lng: 135.5015, label: 'Pokémon Cafe Osaka', num: 2, cat: 'food', desc: 'Pokémon-themed dining — book in advance!' },
        { lat: 34.6545, lng: 135.4290, label: 'Osaka Aquarium Kaiyukan', num: 3, cat: 'attraction', desc: 'World-class aquarium — whale sharks & touch pools' },
        { lat: 34.6690, lng: 135.5020, label: 'Shinsaibashi Shopping', num: 4, cat: 'shopping', desc: 'Covered arcade — fashion, souvenirs, electronics' },
        { lat: 34.6687, lng: 135.5013, label: 'Dotonbori & Glico Sign', num: 5, cat: 'attraction', desc: 'Iconic neon strip — the heart of Osaka' },
        { lat: 34.6683, lng: 135.5031, label: 'Immo Pipi Sweet Potato', num: 6, cat: 'food', desc: 'Sweet potato soft serve & desserts' },
        { lat: 34.6685, lng: 135.5008, label: 'Dotonbori Food Stalls', num: 7, cat: 'food', desc: 'Takoyaki, okonomiyaki, kushikatsu — eat till you drop' }
      ]
    },

    // ============ DAY 9 — May 23 (Sat) — Return to Tokyo, Final Day ============
    {
      num: 9,
      date: '2026-05-23',
      neighborhoods: 'Osaka · Shinjuku · Marunouchi · Shibuya',
      title: 'Shinkansen Home — Last Shopping & Farewell Dinner',
      description: "Board the bullet train back to Tokyo for one final afternoon of shopping and sightseeing. Hit the anime treasure trove at SURUGA-YA, fill bags at the 100-yen Seria shop, enjoy a fancy farewell lunch in Marunouchi, and make your JJK pilgrimage to Shibuya and Shinjuku Stations.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinkansen: Osaka → Tokyo',
              description: 'Board the Nozomi for the 2.5-hour ride back to Tokyo. Grab ekiben at Shin-Osaka Station and enjoy the views one last time.',
              details: [
                '🚄 Depart Shin-Osaka ~8:00 AM → arrive Tokyo ~10:30 AM',
                '🍱 Osaka ekiben specialties: takoyaki bento, kitsune udon bento',
                '👶 Kids under 6 free on lap — grab window seats'
              ]
            },
            {
              title: 'SURUGA-YA Shinjuku Marui Annex',
              description: 'A paradise for anime, manga, and retro game collectors — secondhand figures, rare manga volumes, vintage game cartridges, trading cards, and exclusive merchandise at reasonable prices. Way better organized than most secondhand shops.',
              details: [
                '🎮 Morning — Shinjuku Marui Annex building',
                '🛒 Secondhand anime figures, manga, games, trading cards',
                '💰 Great prices on pre-owned goods',
                '⏱️ 30-60 minutes — easy to lose track of time'
              ]
            },
            {
              title: 'Seria Shinjuku Marui Annex',
              description: 'Japan\'s stylish 100-yen shop — everything costs ¥100 (about $0.65). Kitchen goods, stationery, craft supplies, organization items, and seasonal goods that look way more expensive than they are. Stock up on souvenirs here.',
              details: [
                '💯 Same building as SURUGA-YA — Marui Annex',
                '🛒 Everything ¥100 — incredible value',
                '🎁 Perfect for small souvenirs and gifts',
                '⏱️ 20-30 minutes'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'SURUGA-YA and Seria are in the same building (Marui Annex near Shinjuku Station East Exit) — knock them both out in one stop.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'The Front Room Deli Restaurant (Marunouchi)',
              description: 'An elegant restaurant in Tokyo\'s upscale Marunouchi district — perfect for a fancy farewell lunch. The area around Tokyo Station has beautiful red-brick architecture and tree-lined boulevards that feel almost European.',
              details: [
                '🍽️ Afternoon — Marunouchi area near Tokyo Station',
                '💰 ¥2,000-4,000 for lunch sets',
                '🏙️ Beautiful Marunouchi streetscape for post-lunch stroll'
              ]
            },
            {
              title: 'Shibuya Station (JJK Reference)',
              description: 'For Jujutsu Kaisen fans — Shibuya Station was the setting for the devastating Shibuya Incident arc. Stand in the real station that was ground zero for one of anime\'s most intense battle sequences. Take photos at the exits featured in the manga.',
              details: [
                '📍 Afternoon — Shibuya Station various exits',
                '📸 Spot locations from the Shibuya Incident arc',
                '⏱️ 15-20 minutes for photos and appreciation'
              ]
            },
            {
              title: 'Shinjuku Station East Exit (JJK Reference)',
              description: 'Another key JJK location — Shinjuku Station\'s East Exit area. The neon-lit streets of Kabukicho visible from here were backdrop to major scenes. Complete your JJK pilgrimage.',
              details: [
                '📍 Shinjuku Station East Exit',
                '📸 The iconic East Exit view toward Kabukicho',
                '⏱️ 10-15 minutes'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Use this afternoon for any last-minute shopping you missed — Don Quijote for snacks and souvenirs, or revisit a favorite spot. The kids might enjoy one more playground visit at Yoyogi or Shinjuku Gyoen.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Tokyo Dinner',
              description: 'Choose your farewell meal — revisit a favorite restaurant, try something new, or do one last ramen/udon run. This is your sayonara dinner, so make it count.',
              details: [
                '🍽️ Pick your highlight cuisine: wagyu, sushi, udon, curry',
                '📍 Shinjuku area — easy walk home after',
                '🍺 Toast to an incredible 10 days'
              ]
            },
            {
              title: 'Last Konbini Run & Pack',
              description: 'Final convenience store sweep for snacks, drinks, and any forgotten souvenirs. Then head back to pack up. You\'ve earned an early night — tomorrow is departure day.',
              details: [
                '🏪 Stock up on Japan-only snacks for the flight home',
                '🧳 Pack tonight — morning departures are smoother when bags are ready',
                '😴 Early to bed — airport mornings come fast'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Buy a bag of Tokyo Banana, Shiroi Koibito, or regional Kit-Kats at the konbini tonight — they make perfect omiyage (gifts) for friends and family back home.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.7334, lng: 135.5001, label: 'Shin-Osaka Station', num: 1, cat: 'transport', desc: 'Shinkansen departure back to Tokyo' },
        { lat: 35.6926, lng: 139.7046, label: 'SURUGA-YA Marui Annex', num: 2, cat: 'shopping', desc: 'Secondhand anime, manga & games' },
        { lat: 35.6926, lng: 139.7046, label: 'Seria Marui Annex', num: 3, cat: 'shopping', desc: '100-yen shop — incredible souvenirs' },
        { lat: 35.6812, lng: 139.7671, label: 'The Front Room (Marunouchi)', num: 4, cat: 'food', desc: 'Fancy farewell lunch near Tokyo Station' },
        { lat: 35.6580, lng: 139.7016, label: 'Shibuya Station (JJK)', num: 5, cat: 'attraction', desc: 'Jujutsu Kaisen Shibuya Incident location' },
        { lat: 35.6896, lng: 139.7006, label: 'Shinjuku East Exit (JJK)', num: 6, cat: 'attraction', desc: 'JJK pilgrimage — neon Kabukicho backdrop' }
      ]
    },

    // ============ DAY 10 — May 24 (Sun) — Departure ============
    {
      num: 10,
      date: '2026-05-24',
      neighborhoods: 'Shinjuku · Narita',
      title: 'Sayonara Japan — Departure Day ✈️',
      description: "All good things come to an end. Pack up, grab one last konbini breakfast, and head to Narita Airport. Allow plenty of time for check-in, tax-free shopping in the terminal, and a final bowl of ramen before boarding.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Final Morning in Tokyo',
              description: 'Wake up, enjoy one last Japanese breakfast (konbini onigiri and matcha, or find a local café), and do a final luggage check. Make sure all those souvenirs actually fit in your bags.',
              details: [
                '☀️ Wake up with time to spare — no rushing today',
                '🍙 Konbini breakfast: onigiri, tamago sando, matcha latte',
                '🧳 Final bag check — you probably bought more than expected',
                '📦 If bags are overstuffed, you can ship a box from a konbini (Yamato Transport)'
              ]
            },
            {
              title: 'Head to Narita Airport',
              description: 'Take the Narita Express from Shinjuku Station — the same smooth 80-minute ride you took on Day 1, but this time going the other direction with a heart full of memories.',
              details: [
                '🚃 N\'EX from Shinjuku to Narita: ~80 minutes, ¥3,250/adult',
                '⏰ Arrive at airport 3 hours before international flights',
                '🛒 Narita has excellent tax-free shopping in the terminal',
                '🍜 Airport ramen shops serve one last great bowl'
              ]
            },
            {
              title: 'Narita Airport — Tax-Free Shopping & Departure',
              description: 'Narita\'s terminals have incredible shopping — last chance for Japanese snacks, cosmetics, electronics, and character goods. Many prices are competitive with city shops, and everything is tax-free. Grab a final meal at the airport restaurants before boarding.',
              details: [
                '🛍️ Don\'t miss the character shops in the departure terminal',
                '🍫 Last chance for limited-edition snacks and sweets',
                '🍜 Airport ramen is surprisingly good — one final slurp',
                '✈️ Sayonara Japan! またね (mata ne — see you again!) 🇯🇵'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Return your Suica/PASMO cards at the JR counter in the airport for a ¥500 deposit refund per card (or keep them as souvenirs — they work forever and you can reload them on your next trip).' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6938, lng: 139.7034, label: 'Shinjuku (Departure)', num: 1, cat: 'hotel', desc: 'Final morning — pack up and head out' },
        { lat: 35.7647, lng: 139.7713, label: 'Narita International Airport', num: 2, cat: 'transport', desc: 'Sayonara Japan! またね 🇯🇵' }
      ]
    }
  ],

  // Google Maps API key
  mapsApiKey: 'AIzaSyBP0yidMjJEECgkIiZz2lw1NLsQ7jdASYc'
};

// Run fulfillment
try {
  const result = fulfillOrder(order, itineraryData);
  console.log('\n✅ FULFILLMENT COMPLETE');
  console.log('Slug:', result.slug);
  console.log('URL:', result.url);
  console.log('File:', result.filePath);
} catch (err) {
  console.error('\n❌ FULFILLMENT FAILED:', err.message);
  process.exit(1);
}
