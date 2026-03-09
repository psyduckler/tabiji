const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772677250986_k86fnz',
  email: 'paulhblasjr@gmail.com',
  destination: 'Tokyo, Osaka, Kyoto',
  startDate: '2026-05-15',
  endDate: '2026-05-24',
  groupSize: 5,
  requests: '3 adults, 2 children ages 3 and 2. No pork. No gundam. Landing NRT May 15 ~1pm. Airbnb in Shinjuku.'
};

const itineraryData = {
  destination: 'Tokyo, Osaka & Kyoto, Japan',
  countryEmoji: '🇯🇵',
  title: 'Japan with Tiny Adventurers',
  subtitle: '10 days of temples, matcha, anime & street food across Tokyo, Osaka & Kyoto — no pork, all heart',
  description: "This itinerary is built for a crew that doesn't slow down just because the kids are small. You'll crush 50+ spots across three cities — matcha every morning, character cafés by day, and late-night yakitori alleys after bedtime. Tokyo's neon energy, Kyoto's ancient calm, Osaka's street food soul, and Nara's friendly deer — all routed for efficiency with stroller-friendly paths and no pork anywhere. Your toddlers will think Japan is a giant playground. They're not wrong.",
  duration: '10 days / 9 nights',
  dates: 'May 15 – May 24, 2026',
  budget: '$$–$$$',
  pace: 'Adventurous',
  bestFor: 'Families with young kids',
  highlights: [
    'teamLab Planets — immersive digital art the kids will lose their minds over',
    'Fushimi Inari — 10,000 vermillion torii gates at golden hour',
    'Nara deer park — toddlers feeding wild deer (supervised chaos)',
    'Kirby Café & Pokémon Center — character overload in Ikebukuro',
    'Late-night Golden Gai & Omoide Yokocho — after the kids crash',
    'Matcha shops every single morning — this is non-negotiable',
    'Sensō-ji, Meiji Jingū & Gōtokuji — temples across Tokyo',
    'Osaka street food crawl — takoyaki, yakitori, kushikatsu (no pork)',
    'Shibuya Sky sunset — the best view in Tokyo'
  ],

  essentials: [
    { title: '🍖 NO PORK Policy', text: "Every restaurant in this itinerary has been selected with your no-pork restriction in mind. In Japan, pork hides everywhere — ramen broth (tonkotsu), gyoza filling, tonkatsu, nikuman. Always say \"buta nashi de onegaishimasu\" (豚なしでお願いします) — no pork please. Cards with your allergy in Japanese are a lifesaver. Print one or save it on your phone." },
    { title: '👶 Toddler Travel Tips', text: "Japan is insanely family-friendly. Most department stores have nursing rooms (akachan rooms) with changing tables, hot water for formula, and even kid-size toilets. Elevators are everywhere in train stations (look for the ♿ signs). Bring a lightweight umbrella stroller — compact enough for trains, tough enough for temple steps. Convenience stores (konbini) have onigiri, fruit cups, and milk anytime." },
    { title: '🚄 Getting Around', text: "Get Suica/PASMO cards for everyone (kids under 6 ride free on trains). For the Tokyo→Osaka leg, book Shinkansen tickets at the station or use SmartEX app. Reserve seats (shitei-seki) for family comfort. In Osaka, the subway + JR covers everything. Taxis are clean and safe — great for tired toddler moments." },
    { title: '🍵 Matcha Morning Ritual', text: "Your mornings start with matcha. Japan takes tea seriously — from ceremonial grade whisked in Kyoto to creamy matcha lattes in Shinjuku. We've routed a matcha stop into every single morning because you asked for it and honestly it's the best way to start a day." }
  ],

  days: [
    {
      num: 1,
      date: '2026-05-15',
      neighborhoods: 'Narita · Shinjuku',
      title: 'Landing Day — Welcome to Tokyo',
      description: "You land at NRT around 1pm. By the time you clear customs, grab bags, and ride the Narita Express into Shinjuku, it'll be late afternoon. Drop bags at your Airbnb, stretch those toddler legs, and ease into Tokyo with an evening walk through Shinjuku's neon wonderland. Tonight is about vibes, not distance.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Narita Express to Shinjuku',
              description: "The N'EX (Narita Express) runs directly to Shinjuku Station in about 80 minutes. Reserved seats, luggage racks, and smooth ride — perfect for jet-lagged toddlers to nap. Buy tickets at the JR counter in the airport arrivals hall.",
              details: [
                '🚆 N\'EX departs roughly every 30 min — no rush through customs',
                '👶 Kids under 6 ride free on your lap (no seat reservation needed)',
                '💳 Get Suica cards at the airport — they work on everything'
              ]
            },
            {
              title: 'Check In & Shinjuku Gyoen Stroll',
              description: "After dropping bags at your Shinjuku Airbnb, walk to Shinjuku Gyoen National Garden — a massive, peaceful park right in your neighbourhood. The kids can run free on the lawns while you decompress. The Japanese garden section is stunning even in a quick visit.",
              details: [
                '🌿 Open until 6pm (last entry 5:30pm) — ¥500 adults, free for kids under 6',
                '🌸 May = iris season in the traditional garden',
                '👶 Wide flat paths, perfect for strollers'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "Shinjuku Gyoen closes at 6pm sharp. If you arrive too late, skip to the evening plan — you're right next to everything." }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shinjuku Station East Exit & 3D Cat',
              description: "Walk past Shinjuku Station East Exit (JJK fans, you know this spot) and look up at the giant 3D cat on the Cross Shinjuku Vision screen. The hyper-realistic calico cat has been Tokyo's unofficial mascot since 2021. Kids will be mesmerized.",
              details: [
                '🐱 Cross Shinjuku Vision — corner of Studio Alta building',
                '📸 The cat animation runs on the hour and half-hour',
                '⚡ Shinjuku Station East Exit — the JJK Shibuya Incident reference point'
              ]
            },
            {
              title: 'Don Quijote Shinjuku & Shopping',
              description: "Don Quijote (Donki) is Japan's legendary discount store — a sensory overload of snacks, toys, cosmetics, and random treasures stacked floor to ceiling. The Shinjuku Kabukicho location is open 24 hours. Stock up on konbini snacks and kid supplies.",
              details: [
                '🏪 Open 24 hours — come back anytime this trip',
                '🍬 Grab Japanese Kit-Kats, mochi, and rice crackers for the Airbnb',
                '🧸 Character goods section is toddler paradise'
              ]
            }
          ],
          meals: [
            {
              type: '🍵 Matcha',
              name: 'Saryo Tsujiri Shinjuku',
              description: "Kyoto's famous matcha house has a Shinjuku branch. Rich matcha lattes, parfaits, and soft-serve to welcome you to Japan. The kids will love the matcha soft-serve.",
              meta: '💰 $ · 📍 Shinjuku 3-chome · No pork on menu'
            },
            {
              type: '🍽️ Dinner',
              name: 'Shinjuku Kabuki Hall / Kabuki Yokocho',
              description: "A retro-themed food hall in the Kabukicho Tower with multiple stalls serving yakitori (chicken), seafood, tempura, and more. Lively atmosphere, easy to find no-pork options, and the kids can wander between stalls. Perfect jet-lag dinner.",
              meta: '💰 $$ · 📍 Kabukicho Tower, Shinjuku · Multiple no-pork stalls'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6846, lng: 139.6903, label: 'Shinjuku Gyoen', num: 1, cat: 'attraction', desc: 'Massive beautiful garden — perfect for jet-lag recovery' },
        { lat: 35.6938, lng: 139.7034, label: 'Shinjuku Station East Exit', num: 2, cat: 'attraction', desc: 'JJK reference point — bustling station exit' },
        { lat: 35.6942, lng: 139.7012, label: '3D Cat Cross Shinjuku', num: 3, cat: 'attraction', desc: 'Giant hyper-realistic 3D cat on LED screen' },
        { lat: 35.6948, lng: 139.7030, label: 'Don Quijote Shinjuku', num: 4, cat: 'shopping', desc: '24-hour discount store — snacks, toys, everything' },
        { lat: 35.6936, lng: 139.7006, label: 'Saryo Tsujiri', num: 5, cat: 'food', desc: 'Kyoto matcha house — lattes and soft-serve' },
        { lat: 35.6946, lng: 139.7019, label: 'Kabuki Hall Yokocho', num: 6, cat: 'food', desc: 'Retro food hall in Kabukicho Tower' }
      ]
    },
    {
      num: 2,
      date: '2026-05-16',
      neighborhoods: 'Harajuku · Meiji Jingū · Shibuya',
      title: 'Temples, Takeshita & Shibuya Sky',
      description: "Today you go from ancient shrine forest to kawaii overload to Tokyo's best skyline view. Start with matcha and the sacred Meiji Jingū, let the kids go wild on Takeshita Street, then catch sunset from Shibuya Sky 230 meters up. This is peak Tokyo in one day.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Matcha & Meiji Jingū Shrine',
              description: "Start the day right — matcha first, then walk through the towering torii gate into Meiji Jingū's ancient forest. This Shinto shrine dedicated to Emperor Meiji feels like stepping out of Tokyo entirely. The gravel paths wind through 170,000 trees. Write a wish on an ema (wooden plaque) and hang it with thousands of others.",
              details: [
                '⛩️ Free admission · Open sunrise to sunset',
                '🌳 The forested approach is stroller-friendly on the main path',
                '📿 Ema plaques: ¥500 — let the kids draw their wishes',
                '🍵 Hit a matcha spot on Omotesando before entering'
              ]
            },
            {
              title: 'Yoyogi Park',
              description: "Right next to Meiji Jingū, Yoyogi Park is Tokyo's Central Park. Wide open lawns, shady trees, and on weekends you might catch rockabilly dancers or street performers. Let the toddlers run while you coffee up.",
              details: [
                '🌿 Free · Open 24 hours',
                '👶 Huge flat grassy areas — toddler dream',
                '🎸 Weekend performers near the Harajuku entrance'
              ]
            }
          ],
          meals: [
            {
              type: '🍵 Matcha',
              name: 'Cha Cha no Ma',
              description: "Intimate matcha café near Omotesando where you sit on the floor and choose your own tea bowl. They serve ceremonial-grade matcha whisked to order. A calm, beautiful start before the Harajuku chaos.",
              meta: '💰 $$ · 📍 Near Meiji-Jingūmae Station · Reservations recommended'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Takeshita Street & Harajuku',
              description: "Dive into Takeshita Street — Harajuku's famous pedestrian lane packed with kawaii shops, crepe stands, character stores, and wild fashion. It's sensory overload in the best way. The kids will point at everything. Get cotton candy the size of their heads.",
              details: [
                '🍦 Marion Crêpes — the original Harajuku crepe stand',
                '🧸 Kiddy Land — 6 floors of character goods and toys',
                '🍭 Totti Candy Factory — giant rainbow cotton candy',
                '👗 Brandy Melville is on the main drag near the entrance'
              ]
            },
            {
              title: 'Café Reissue',
              description: "This Harajuku café is famous for latte art — they'll draw any character on your drink. Get a custom Pikachu or Kirby latte for the kids (or for yourself, no judgment). Instagram gold.",
              details: [
                '☕ Custom latte art to order — ¥700-900',
                '📸 Tell them what character you want and watch the magic',
                '📍 Short walk from Takeshita Street'
              ]
            },
            {
              title: 'Uniqlo Harajuku Global Flagship',
              description: "The massive Uniqlo flagship on Meiji-dori is worth a browse — Japan-exclusive collaborations, UT graphic tees, and the kids' section has adorable stuff you can't get back home.",
              details: [
                '🛍️ Japan-exclusive anime/character collabs',
                '👶 Kids section with unique Japanese designs',
                '📍 Right on Meiji-dori, can\'t miss it'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shibuya Sky Sunset',
              description: "Take the elevator 230 meters up to Shibuya Sky's open-air observation deck for the best sunset view in Tokyo. The city stretches to infinity in every direction. On clear days you can see Mt. Fuji. Book tickets online in advance — sunset slots sell out.",
              details: [
                '🎫 ¥2,000 adults, ¥900 kids 3-5 · Book online for sunset slot',
                '🌅 Sunset in May is around 6:40pm — arrive 30 min early',
                '📸 Open-air deck + glass floor = incredible photos',
                '👶 Strollers must be left at the entrance — bring a carrier'
              ]
            },
            {
              title: 'Shibuya Crossing & Character Store Marathon',
              description: "After Shibuya Sky, descend into the famous Shibuya Crossing — the world's busiest intersection. Then hit the character stores: Nintendo Tokyo, Pokémon Center, Capcom, and more. All within walking distance in the Shibuya/Parco area.",
              details: [
                '🚶 Cross the scramble — stand in the center island for the full experience',
                '📸 Best view of the crossing: Starbucks on the 2nd floor of TSUTAYA building',
                '🎮 Shibuya PARCO 6F: Nintendo Tokyo, Capcom, Pokémon Center'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Uobei Shibuya (Genki Sushi)',
              description: "Conveyor belt sushi where you order on a tablet and plates zoom to your seat on a bullet-train track. Toddlers will be OBSESSED. All seafood, no pork. Fast, fun, delicious, cheap.",
              meta: '💰 $ · 📍 Shibuya · Touchscreen ordering · No pork'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6764, lng: 139.6993, label: 'Meiji Jingū', num: 1, cat: 'attraction', desc: 'Majestic Shinto shrine in an ancient forest' },
        { lat: 35.6715, lng: 139.6948, label: 'Yoyogi Park', num: 2, cat: 'attraction', desc: 'Wide-open lawns — let the toddlers run' },
        { lat: 35.6706, lng: 139.7027, label: 'Takeshita Street', num: 3, cat: 'shopping', desc: 'Harajuku kawaii shopping lane' },
        { lat: 35.6693, lng: 139.7024, label: 'Café Reissue', num: 4, cat: 'food', desc: 'Custom character latte art café' },
        { lat: 35.6686, lng: 139.7010, label: 'Uniqlo Harajuku', num: 5, cat: 'shopping', desc: 'Global flagship — Japan-exclusive collabs' },
        { lat: 35.6684, lng: 139.7010, label: 'Brandy Melville', num: 6, cat: 'shopping', desc: 'On Takeshita Street near the entrance' },
        { lat: 35.6584, lng: 139.7023, label: 'Shibuya Sky', num: 7, cat: 'attraction', desc: '230m observation deck — sunset views of all Tokyo' },
        { lat: 35.6595, lng: 139.7004, label: 'Shibuya Crossing', num: 8, cat: 'attraction', desc: 'World\'s busiest intersection' },
        { lat: 35.6620, lng: 139.6981, label: 'Nintendo/Pokémon Shibuya PARCO', num: 9, cat: 'shopping', desc: 'Character stores in Shibuya PARCO' },
        { lat: 35.6593, lng: 139.6988, label: 'Uobei Shibuya', num: 10, cat: 'food', desc: 'Bullet-train sushi — toddler heaven' },
        { lat: 35.6710, lng: 139.7050, label: 'Cha Cha no Ma', num: 11, cat: 'food', desc: 'Ceremonial matcha café near Omotesando' }
      ]
    },
    {
      num: 3,
      date: '2026-05-17',
      neighborhoods: 'Ikebukuro · Setagaya (Gōtokuji)',
      title: 'Character Cafés, Cat Temple & Sunshine City',
      description: "Today is anime, character, and cat temple day. Start with the cat temple Gōtokuji (thousands of lucky cat figurines), then head to Ikebukuro for Kirby Café, Pokémon Center Mega, Pikachu Sweets, the Ghibli Store, and Sunshine City. This is the day the kids will talk about forever.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Matcha & Gōtokuji Temple (Cat Temple)',
              description: "Take the Odakyu Line to Gōtokuji — the birthplace of the maneki-neko (beckoning cat). Thousands of white lucky cat figurines line the shelves of this serene Buddhist temple. Buy a small one (¥300-3,000), make a wish, and leave it to join the collection. The toddlers will think it's a cat village.",
              details: [
                '🐱 Free admission · Open 6am–6pm',
                '🚂 15 min from Shinjuku on Odakyu Line to Gōtokuji Station',
                '📿 Buy a lucky cat, write your wish, leave it at the temple',
                '👶 Flat grounds, stroller-accessible'
              ]
            }
          ],
          meals: [
            {
              type: '🍵 Matcha',
              name: 'Matcha Stand Maruni (Setagaya)',
              description: "Small, beloved matcha stand near the cat temple area. Thick matcha lattes, hojicha, and matcha-dipped treats. Quick and perfect before temple time.",
              meta: '💰 $ · 📍 Setagaya area · Takeaway-style'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kirby Café Tokyo',
              description: "The permanent Kirby Café in Tokyo Skytree Town (Solamachi) serves adorable Kirby-themed food — pink curry, character pancakes, and Waddle Dee desserts. MUST reserve online in advance — slots open 1 month before. This place books out instantly.",
              details: [
                '🎫 MUST reserve at kirbycafe.jp — opens 1 month prior at noon JST',
                '🍛 No pork items available — chicken curry, seafood pasta, desserts',
                '📍 Tokyo Solamachi 4F, near Skytree',
                '👶 High chairs available, kid-friendly portions'
              ]
            },
            {
              title: 'Pokémon Center Mega Tokyo & Pikachu Sweets',
              description: "The biggest Pokémon Center in Tokyo is in Ikebukuro's Sunshine City. Wall-to-wall plushies, exclusive merch, and game demos. Right next door, Pikachu Sweets café serves Pikachu-shaped desserts and drinks. The kids won't want to leave.",
              details: [
                '🎮 Free entry · Sunshine City Alpa 2F',
                '🧁 Pikachu Sweets: no reservation needed, but expect a short wait',
                '🛍️ Tokyo-exclusive Pokémon merch you can\'t get anywhere else'
              ]
            },
            {
              title: 'Donguri Kyowakoku (Ghibli Store) Ikebukuro',
              description: "The official Studio Ghibli merchandise store — Totoro plushies, Kiki's Delivery Service bags, Spirited Away accessories. The Ikebukuro location in Sunshine City is one of the largest. Stock up on Ghibli souvenirs.",
              details: [
                '🛍️ Sunshine City Alpa · No reservation needed',
                '🧸 Exclusive Japan-only Ghibli merchandise',
                '📍 Same building as Pokémon Center — efficient routing'
              ]
            },
            {
              title: 'Sunshine City & Sunshine Aquarium',
              description: "Sunshine City is a massive entertainment complex. Beyond the character stores, check out the Sunshine Aquarium on the rooftop — penguins swimming in a sky-high tank above your head. Perfect for toddlers.",
              details: [
                '🐧 Sunshine Aquarium: ¥2,600 adults, ¥800 ages 4+ (free under 4)',
                '🎮 Namjatown: indoor theme park with character attractions',
                '🏬 Multiple floors of shopping and entertainment'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'SURUGA-YA & Seria (Shinjuku Marui Annex)',
              description: "Back in Shinjuku, hit SURUGA-YA in the Marui Annex for retro anime figures, manga, and collectibles. Seria (also in Marui Annex) is a ¥100 store with surprisingly cute Japanese stationery, toys, and household goods. Both in the same building.",
              details: [
                '📍 Shinjuku Marui Annex — near Shinjuku Station East Exit',
                '🎌 SURUGA-YA: anime figures, retro games, manga at great prices',
                '💯 Seria: Japan\'s cutest ¥100 store — stationery, toys, crafts'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Afuri Ramen (Shinjuku)',
              description: "Afuri specializes in yuzu shio (citrus salt) ramen — light, refreshing, and completely pork-free. Their chicken or vegan broth options are incredible. The yuzu flavor is unlike any ramen you've had. Counter seating with ticket machine ordering.",
              meta: '💰 $ · 📍 Shinjuku · Chicken/vegan broth · NO PORK'
            }
          ],
          tips: [
            { type: 'tip', text: "Book Kirby Café the moment reservations open (1 month before your date). Set an alarm. It sells out in minutes." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6488, lng: 139.6369, label: 'Gōtokuji Temple', num: 1, cat: 'attraction', desc: 'Cat temple — thousands of lucky cat figurines' },
        { lat: 35.7101, lng: 139.8107, label: 'Kirby Café (Skytree Town)', num: 2, cat: 'food', desc: 'Adorable Kirby-themed food — reserve ahead!' },
        { lat: 35.7294, lng: 139.7189, label: 'Pokémon Center Mega Tokyo', num: 3, cat: 'shopping', desc: 'Biggest Pokémon store in Tokyo — Sunshine City' },
        { lat: 35.7294, lng: 139.7189, label: 'Pikachu Sweets', num: 4, cat: 'food', desc: 'Pikachu-shaped desserts next to Pokémon Center' },
        { lat: 35.7290, lng: 139.7185, label: 'Donguri Kyowakoku (Ghibli Store)', num: 5, cat: 'shopping', desc: 'Official Ghibli merch — Totoro, Kiki, Spirited Away' },
        { lat: 35.7288, lng: 139.7193, label: 'Sunshine City', num: 6, cat: 'attraction', desc: 'Entertainment complex with aquarium and stores' },
        { lat: 35.6930, lng: 139.7032, label: 'SURUGA-YA Marui Annex', num: 7, cat: 'shopping', desc: 'Retro anime figures and manga' },
        { lat: 35.6930, lng: 139.7032, label: 'Seria Marui Annex', num: 8, cat: 'shopping', desc: '¥100 store — cute stationery and toys' },
        { lat: 35.6906, lng: 139.6987, label: 'Afuri Ramen', num: 9, cat: 'food', desc: 'Yuzu citrus ramen — pork-free options' }
      ]
    },
    {
      num: 4,
      date: '2026-05-18',
      neighborhoods: 'Asakusa · Sumida · Toyosu',
      title: 'Ancient Temples, Skytree & Spa Night',
      description: "From Tokyo's oldest temple to its tallest tower. Start at Sensō-ji in Asakusa for incense and ichigo daifuku, cross the river to Tokyo Skytree for views that make Shibuya Sky look short, cruise along Oyokogawa Shinsui Park, then end with a luxurious soak at Toyosu Manyo Club — the 24-hour spa with a view.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sensō-ji Temple & Nakamise-dōri',
              description: "Tokyo's oldest and most visited temple. Walk through the massive Kaminarimon (Thunder Gate), browse the 250m Nakamise shopping street, and enter the incense-filled main hall. Get there early before the crowds. The five-story pagoda is stunning in morning light.",
              details: [
                '⛩️ Free admission · Main hall open 6am–5pm',
                '🛍️ Nakamise-dōri: traditional snacks, fans, chopsticks, toys',
                '🍡 Try ningyo-yaki (custard-filled cakes) fresh from the griddle',
                '👶 Wide paths, stroller-friendly, lots to look at'
              ]
            },
            {
              title: 'Ichigo Daifuku at Asakusa',
              description: "Hunt for ichigo daifuku (strawberry mochi) — plump strawberries wrapped in sweet bean paste and soft mochi. Several shops along Nakamise and surrounding streets sell them. May is the tail end of strawberry season so they're extra sweet.",
              details: [
                '🍓 Look for shops with fresh daifuku in the display case',
                '📍 Umezono (梅園) near Sensō-ji is a classic pick',
                '💰 Usually ¥300-500 per piece'
              ]
            }
          ],
          meals: [
            {
              type: '🍵 Matcha',
              name: 'Suzukien Asakusa',
              description: "Famous for having the world's strongest matcha gelato — 7 levels of intensity from mild to \"premium No. 7\" which is so intense it's almost bitter. The kids will love level 1-2, you'll dare each other to try level 7.",
              meta: '💰 $ · 📍 Asakusa, near Sensō-ji · World\'s strongest matcha gelato'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tokyo Skytree',
              description: "At 634 meters, Tokyo Skytree is the tallest tower in Japan. Take the elevator to the Tembo Deck (350m) or Tembo Galleria (450m) for views that stretch to Mt. Fuji on clear days. The base complex (Solamachi) has shopping, food, and the Kirby Café.",
              details: [
                '🎫 Tembo Deck: ¥2,100 adults, ¥950 ages 4-5, free under 4',
                '⏰ Book combo tickets online for shorter lines',
                '📸 Clear May days = possible Fuji views',
                '🛍️ Solamachi mall at the base has 300+ shops'
              ]
            },
            {
              title: 'Oyokogawa Shinsui Park',
              description: "A peaceful canal-side park in the Sumida area — cherry trees, small bridges, and a walking path along the old Oyoko River. Great for a quiet stroller walk between Skytree and your next stop. The kids can splash near the shallow water features.",
              details: [
                '🌿 Free · Open 24 hours',
                '📍 About 15 min walk south of Skytree',
                '👶 Flat paths, benches, shady trees'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Toyosu Manyo Club (24-Hour Spa)',
              description: "End the day at Toyosu Manyo Club — a massive onsen resort right on Tokyo Bay. Natural hot spring water, multiple bath types, a manga library, rest areas, and restaurants. The outdoor foot bath has Toyosu market and Rainbow Bridge views. Family-friendly with kid bathing areas.",
              details: [
                '♨️ ¥3,850 adults, ¥2,060 kids 4+ · Open 24 hours',
                '👶 Family bathing area available · Kids under 4 free',
                '🌃 Rooftop foot bath with Tokyo Bay night views',
                '📚 Manga library with thousands of volumes',
                '🍽️ Multiple restaurants inside — no need to leave for dinner'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Toyosu Manyo Club Restaurant',
              description: "Dine inside the spa complex — fresh seafood from nearby Toyosu Market, tempura, udon, and set meals. Eat in your yukata (robe) while the kids play. Multiple no-pork options available.",
              meta: '💰 $$ · 📍 Inside Toyosu Manyo Club · Seafood & udon · No pork'
            }
          ],
          tips: [
            { type: 'tip', text: "Toyosu Manyo Club is a great rainy day backup too — you could spend half a day here. The manga library alone is worth it." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: 'Sensō-ji Temple', num: 1, cat: 'attraction', desc: 'Tokyo\'s oldest temple — Thunder Gate & Nakamise' },
        { lat: 35.7140, lng: 139.7966, label: 'Ichigo Daifuku (Asakusa)', num: 2, cat: 'food', desc: 'Strawberry mochi — seasonal perfection' },
        { lat: 35.7148, lng: 139.7963, label: 'Suzukien Matcha Gelato', num: 3, cat: 'food', desc: '7 levels of matcha intensity' },
        { lat: 35.7101, lng: 139.8107, label: 'Tokyo Skytree', num: 4, cat: 'attraction', desc: '634m tower — tallest in Japan' },
        { lat: 35.7000, lng: 139.8080, label: 'Oyokogawa Shinsui Park', num: 5, cat: 'attraction', desc: 'Peaceful canal-side park walk' },
        { lat: 35.6468, lng: 139.7895, label: 'Toyosu Manyo Club', num: 6, cat: 'attraction', desc: '24-hour spa resort with Tokyo Bay views' }
      ]
    },
    {
      num: 5,
      date: '2026-05-19',
      neighborhoods: 'Minato · Toyosu · Shinjuku',
      title: 'Tokyo Tower, teamLab & Golden Gai Farewell',
      description: "Your last full day in Tokyo. Start at Tsukiji's outer market for the freshest breakfast, walk through Prince Shiba Park to Tokyo Tower, then spend the afternoon at teamLab Planets — a barefoot, immersive art experience the whole family will love. End with late-night eating at Golden Gai and Omoide Yokocho after the kids pass out.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tsukiji Outer Market',
              description: "The outer market is still thriving with food stalls and restaurants. Grab fresh tamagoyaki (egg omelette on a stick), grilled seafood skewers, and fruit. Skip the tourist sushi spots and eat what the vendors are eating. Everything is fresh off the boat.",
              details: [
                '🐟 Best time: 7–10am before crowds build',
                '🥚 Tamagoyaki sticks — sweet egg omelette, kids love it',
                '🦐 Grilled scallops, crab legs, tuna skewers — all pork-free',
                '🍓 Fresh fruit stands with perfect Japanese strawberries'
              ]
            },
            {
              title: 'Hie-jinja Shrine',
              description: "A peaceful Shinto shrine near Akasaka with a famous tunnel of red torii gates (smaller version of Fushimi Inari). The hillside staircase through the torii is beautiful and less crowded than most Tokyo shrines.",
              details: [
                '⛩️ Free · Open 6am–5pm',
                '📍 Near Akasaka/Tameike-Sanno Station',
                '📸 Red torii tunnel on the side staircase — stunning photos'
              ]
            }
          ],
          meals: [
            {
              type: '🍵 Matcha',
              name: 'Matcha Stand Maiko (Tsukiji)',
              description: "Grab a thick matcha latte from this popular stand right in the Tsukiji market area. Rich, creamy, and the perfect fuel for a market morning.",
              meta: '💰 $ · 📍 Tsukiji Outer Market area'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Prince Shiba Park & Tokyo Tower',
              description: "Walk through the green lawns of Shiba Park with Tokyo Tower looming above. The park is great for a quick toddler break — open grass, shade trees, and the tower framed perfectly from the north side. Then head up Tokyo Tower itself for 360° views from the classic orange lattice landmark.",
              details: [
                '🗼 Main Deck: ¥1,200 adults, ¥700 ages 4-6, free under 4',
                '🌿 Shiba Park: free, open, lots of running space',
                '📸 Best Tokyo Tower photo spot: from the north side of Shiba Park',
                '🕌 Bonus: Zōjō-ji Temple is right here — beautiful with Tower behind it'
              ]
            },
            {
              title: 'teamLab Planets TOKYO DMM',
              description: "Walk barefoot through water, wade knee-deep through a koi pond of digital fish, and lie back in a room of infinite flowers. teamLab Planets is a full-body immersive experience that toddlers and adults love equally. You WILL get wet — wear shorts or roll up your pants.",
              details: [
                '🎫 ¥3,800 adults, ¥1,500 ages 4-6, free under 4 · BOOK ONLINE',
                '💦 You walk barefoot through water — bring a small towel',
                '👶 Toddlers can be carried or wade — strollers parked at entrance',
                '⏰ Allow 60-90 minutes · Last entry 1 hour before closing',
                '📍 Toyosu area — short walk from Shin-Toyosu Station'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Art Aquarium Museum',
              description: "Goldfish swimming in beautifully illuminated art installations — part aquarium, part art gallery, entirely mesmerizing. The dark rooms with glowing fish tanks are magical for kids. Located in the Ginza area.",
              details: [
                '🐠 ¥2,400 adults, ¥1,000 ages 4+ · Free under 4',
                '📍 Ginza/Nihonbashi area',
                '🌙 The dark rooms are atmospheric — great for evening visits'
              ]
            },
            {
              title: 'Late Night: Omoide Yokocho & Golden Gai',
              description: "After the kids crash at the Airbnb (tag-team babysitting time!), sneak out to Shinjuku's atmospheric drinking alleys. Omoide Yokocho (Memory Lane) is a narrow alley of tiny yakitori joints — get chicken skewers and beer. Golden Gai is 6 narrow lanes of 200+ tiny bars, each seating 6-8 people. This is where Tokyo reveals its soul.",
              details: [
                '🍢 Omoide Yokocho: chicken yakitori (specify no pork — \"buta nashi\")',
                '🍺 Golden Gai: cover charges ¥500-1000, drinks ¥600-900',
                '🌙 Best after 9pm — some bars don\'t open until late',
                '📍 Both are 5-min walk from Shinjuku Station West Exit',
                '⚠️ Some Golden Gai bars are regulars-only — look for \"tourists welcome\" signs'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Toriki (Shinjuku)',
              description: "Outstanding chicken yakitori in Shinjuku — every part of the chicken grilled to perfection over charcoal. No pork on the menu, just incredible chicken. Counter seating, smoky atmosphere, the real deal.",
              meta: '💰 $$ · 📍 Shinjuku · All chicken, NO PORK'
            }
          ],
          tips: [
            { type: 'tip', text: "Golden Gai and Omoide Yokocho are adult-only vibes. Take turns — one adult stays with sleeping kids at the Airbnb while two go explore. You're in Shinjuku, it's a 5-minute walk." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6654, lng: 139.7707, label: 'Tsukiji Outer Market', num: 1, cat: 'food', desc: 'Fresh seafood, tamagoyaki, grilled skewers' },
        { lat: 35.6748, lng: 139.7381, label: 'Hie-jinja Shrine', num: 2, cat: 'attraction', desc: 'Torii tunnel shrine near Akasaka' },
        { lat: 35.6586, lng: 139.7454, label: 'Prince Shiba Park', num: 3, cat: 'attraction', desc: 'Green park with Tokyo Tower framing' },
        { lat: 35.6586, lng: 139.7454, label: 'Tokyo Tower', num: 4, cat: 'attraction', desc: 'Classic orange lattice tower — 333m' },
        { lat: 35.6427, lng: 139.7895, label: 'teamLab Planets', num: 5, cat: 'attraction', desc: 'Immersive barefoot digital art — get wet!' },
        { lat: 35.6676, lng: 139.7710, label: 'Art Aquarium', num: 6, cat: 'attraction', desc: 'Illuminated goldfish art installations' },
        { lat: 35.6946, lng: 139.6987, label: 'Omoide Yokocho', num: 7, cat: 'food', desc: 'Memory Lane — tiny yakitori alley' },
        { lat: 35.6934, lng: 139.7039, label: 'Golden Gai', num: 8, cat: 'nightlife', desc: '200+ tiny bars in 6 narrow lanes' },
        { lat: 35.6925, lng: 139.6996, label: 'Toriki', num: 9, cat: 'food', desc: 'Charcoal chicken yakitori — no pork' }
      ]
    },
    {
      num: 6,
      date: '2026-05-20',
      neighborhoods: 'Shinjuku → Shin-Osaka → Namba · Dōtonbori',
      title: 'Shinkansen to Osaka — Street Food Capital',
      description: "Pack up the Shinjuku Airbnb and bullet train to Osaka! The Shinkansen ride is an experience itself — Mt. Fuji views, bento boxes, and toddlers glued to the window. Arrive in Osaka and dive straight into Dōtonbori — neon signs, takoyaki, and the wildest food street in Japan.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinkansen to Osaka',
              description: "Take the Tokaido Shinkansen from Shinagawa or Tokyo Station to Shin-Osaka. The Nozomi takes about 2 hours 15 minutes. Book reserved seats (shitei-seki) for family comfort — aim for seats on the right side (seats E/D) heading west for Mt. Fuji views around 40 minutes in.",
              details: [
                '🚄 Nozomi: ~2h15m · Book at JR counter or SmartEX app',
                '🗻 Mt. Fuji view: right side, about 40 min after departure',
                '🍱 Buy ekiben (station bento) at the platform kiosks — avoid pork ones',
                '👶 Kids under 6: free on your lap, or buy a seat for comfort'
              ]
            }
          ],
          meals: [
            {
              type: '🍵 Matcha',
              name: 'Tsujiri (Tokyo Station)',
              description: "Quick matcha fix before boarding — Tsujiri has a stand inside Tokyo Station. Grab matcha lattes and a matcha soft-serve for the road.",
              meta: '💰 $ · 📍 Tokyo Station · Quick pre-Shinkansen fuel'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In & Dōtonbori Walk',
              description: "Drop bags at your Osaka accommodation and head straight for Dōtonbori — Osaka's legendary entertainment and food district. The Glico Running Man sign, the mechanical crab, the giant blowfish — it's sensory overload and the toddlers will be transfixed. Walk along the canal and take it all in.",
              details: [
                '📸 Glico Running Man sign — THE Osaka photo spot',
                '🦀 Kani Dōraku mechanical crab — kids love the moving legs',
                '🌊 Dōtonbori canal walk — lit up beautifully at night',
                '🛍️ Don Quijote Dōtonbori — the ferris wheel on the building!'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dōtonbori Street Food Crawl',
              description: "Osaka is Japan's kitchen (kuidaore — eat until you drop). Hit the street food stalls for takoyaki (octopus balls), kushikatsu (deep-fried skewers — get chicken/shrimp/veggie, skip pork), and okonomiyaki (savory pancakes — request no pork). Eat your way down both sides of the canal.",
              details: [
                '🐙 Takoyaki: Kukuru or Wanaka — crispy outside, gooey octopus inside',
                '🍢 Kushikatsu: Daruma — choose chicken, shrimp, veggie skewers (say \"buta nashi\")',
                '🥞 Okonomiyaki: Mizuno — get seafood or mixed veggie version',
                '⚠️ Always specify NO PORK — many places use pork by default'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Dōtonbori Street Food (Multiple Stalls)',
              description: "Don't sit down for dinner tonight — graze your way through Dōtonbori. Takoyaki from Kukuru, kushikatsu from Daruma (chicken/shrimp), and finish with a taiyaki (fish-shaped cake filled with custard or red bean).",
              meta: '💰 $ · 📍 Dōtonbori · Street food · Ask for no pork at each stall'
            }
          ],
          tips: [
            { type: 'tip', text: "Osaka locals eat late. The street food stalls are busiest (and best) from 7-10pm. The neon lights reflect on the canal — magical at night." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6812, lng: 139.7671, label: 'Tokyo Station (Shinkansen)', num: 1, cat: 'transport', desc: 'Bullet train departure to Osaka' },
        { lat: 34.6685, lng: 135.5013, label: 'Dōtonbori', num: 2, cat: 'attraction', desc: 'Osaka\'s legendary food & entertainment street' },
        { lat: 34.6687, lng: 135.5022, label: 'Glico Running Man', num: 3, cat: 'attraction', desc: 'THE iconic Osaka photo spot' },
        { lat: 34.6690, lng: 135.5010, label: 'Takoyaki Kukuru', num: 4, cat: 'food', desc: 'Famous takoyaki — crispy octopus balls' },
        { lat: 34.6680, lng: 135.5018, label: 'Kushikatsu Daruma', num: 5, cat: 'food', desc: 'Deep-fried skewers — get chicken/shrimp, skip pork' },
        { lat: 34.6692, lng: 135.5030, label: 'Don Quijote Dōtonbori', num: 6, cat: 'shopping', desc: 'Donki with a ferris wheel on the building' }
      ]
    },
    {
      num: 7,
      date: '2026-05-21',
      neighborhoods: 'Fushimi · Gion · Higashiyama (Kyoto Day Trip)',
      title: 'Kyoto Day Trip — Fushimi Inari, Gion & Nishiki',
      description: "Day trip to Kyoto — just 15 minutes by Shinkansen from Osaka. Start with the 10,000 torii gates of Fushimi Inari at dawn, sip ceremonial matcha at Rokujuan Tea House, explore the geisha district of Gion, and shop your way through Nishiki Market. This is the Japan of postcards.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Fushimi Inari Taisha',
              description: "The most iconic sight in Japan — thousands of vermillion torii gates winding up Mt. Inari. Go EARLY (before 8am) to have the gates almost to yourself. You don't need to hike the full 2-hour loop — the first 20 minutes to the Yotsutsuji intersection is stunning and toddler-manageable (stroller won't work on the stairs though).",
              details: [
                '⛩️ FREE · Open 24 hours',
                '🌅 Arrive before 8am for empty gates and golden light',
                '👶 First section (to Yotsutsuji) is doable with toddlers in carriers',
                '📸 The tunnel of gates is most photogenic in morning light',
                '🦊 Fox statues everywhere — explain the Inari fox mythology to the kids'
              ]
            },
            {
              title: 'Rokujuan Tea House',
              description: "After Fushimi Inari, walk to Rokujuan — a traditional tea house serving ceremonial matcha and sweets. Sit in the tatami room, watch the tea preparation, and enjoy a moment of calm before the day ramps up. The matcha is whisked by hand, served with a seasonal wagashi sweet.",
              details: [
                '🍵 Matcha set: ~¥1,000',
                '📍 Near Fushimi Inari — short walk',
                '🧘 Traditional tatami seating — toddlers can sit on your lap'
              ]
            }
          ],
          meals: [
            {
              type: '🍵 Matcha',
              name: 'Rokujuan Tea House',
              description: "Ceremonial matcha whisked to order with seasonal wagashi sweet. A peaceful traditional tea experience right near Fushimi Inari.",
              meta: '💰 $$ · 📍 Near Fushimi Inari · Traditional tatami room'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nishiki Market',
              description: "Kyoto's Kitchen — a 400-meter covered shopping street with 100+ stalls selling pickles, mochi, fresh fish, tofu, matcha everything, and seasonal specialties. Graze your way through: try dashimaki tamago (rolled egg omelette), yuba (tofu skin), and matcha warabi mochi.",
              details: [
                '🥚 Dashimaki tamago — fluffy Japanese omelette on a stick',
                '🍡 Matcha warabi mochi — soft, jiggly, dusted in matcha powder',
                '🐟 Fresh sashimi cups and grilled seafood skewers',
                '📍 Nishiki-koji Street between Teramachi and Takakura',
                '👶 Covered arcade = rain-proof and stroller-friendly'
              ]
            },
            {
              title: 'Gion District',
              description: "Walk through Gion — Kyoto's famous geisha (geiko) district. Narrow wooden machiya streets, tea houses, and if you're lucky, a geiko or maiko in full kimono heading to an appointment. Hanami-koji Street is the main drag. Respectful photos only — no chasing or blocking.",
              details: [
                '👘 Hanami-koji Street — traditional wooden architecture',
                '🏮 Evening is best for geiko sightings — around 5-6pm',
                '📸 Yasaka Shrine at the eastern end of Gion — beautiful and free',
                '🍵 Tea houses line the streets but most are appointment-only'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Nishiki Market Grazing',
              description: "Skip a sit-down lunch — eat your way through Nishiki Market. Dashimaki tamago, sashimi cups, matcha treats, and grilled seafood. Way more fun than a restaurant.",
              meta: '💰 $-$$ · 📍 Nishiki Market · No pork stalls available'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Yasaka Shrine & Gion at Dusk',
              description: "Visit Yasaka Shrine at the east end of Gion — beautiful lanterns light up at dusk. The shrine grounds are open and the toddlers can explore. Then walk back through Gion's lantern-lit streets before catching the train back to Osaka.",
              details: [
                '🏮 Free · Lanterns light up at sunset',
                '🚆 JR Nara Line or Keihan Line back to Osaka — 30-45 min',
                '📍 Last Shinkansen from Kyoto to Osaka: around 10pm'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Omen (Gion)',
              description: "Kyoto's beloved udon restaurant in the heart of Gion. Handmade udon served cold with dipping sauce and seasonal vegetables, or hot in a dashi broth. Clean, simple, no pork. The set meals are perfect — noodles, tempura, and pickles.",
              meta: '💰 $$ · 📍 Gion, Kyoto · Handmade udon · No pork'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari Taisha', num: 1, cat: 'attraction', desc: '10,000 vermillion torii gates up Mt. Inari' },
        { lat: 34.9670, lng: 135.7710, label: 'Rokujuan Tea House', num: 2, cat: 'food', desc: 'Ceremonial matcha near Fushimi Inari' },
        { lat: 35.0050, lng: 135.7648, label: 'Nishiki Market', num: 3, cat: 'food', desc: 'Kyoto\'s Kitchen — 100+ food stalls' },
        { lat: 35.0036, lng: 135.7756, label: 'Gion District', num: 4, cat: 'attraction', desc: 'Geisha district — traditional machiya streets' },
        { lat: 35.0036, lng: 135.7785, label: 'Yasaka Shrine', num: 5, cat: 'attraction', desc: 'Lantern-lit shrine at the end of Gion' }
      ]
    },
    {
      num: 8,
      date: '2026-05-22',
      neighborhoods: 'Nara (Day Trip from Osaka)',
      title: 'Nara Day Trip — Deer, Daibutsu & Mochi',
      description: "Today the toddlers meet 1,200 wild deer who bow for crackers. Nara is a 45-minute train ride from Osaka and one of the most magical day trips in Japan. Beyond the deer, there's a 15-meter bronze Buddha, ancient temples, and the best warabi mochi in the country. The kids will be in actual heaven.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Train to Nara & Nara Park',
              description: "Take the Kintetsu Line from Namba to Kintetsu Nara (about 40 minutes, more convenient than JR). Walk 5 minutes from the station and you're in Nara Park — 500 hectares of green space where over 1,200 sika deer roam freely. Buy shika senbei (deer crackers, ¥200) and teach the toddlers to bow to the deer — they bow back!",
              details: [
                '🦌 Deer crackers (shika senbei): ¥200 per bundle',
                '👶 Supervise closely — deer can be pushy when they see crackers!',
                '📍 Kintetsu Nara Station → 5 min walk to park',
                '🌿 Huge flat park — perfect for toddlers and strollers'
              ]
            },
            {
              title: 'Tōdai-ji Temple & Great Buddha',
              description: "Inside Nara Park, Tōdai-ji houses the Daibutsu — a 15-meter-tall bronze Buddha that's been sitting here since 752 AD. The wooden hall that holds it is one of the largest wooden structures in the world. Kids can try to crawl through the pillar hole (said to bring enlightenment).",
              details: [
                '🎫 ¥600 adults, ¥300 ages 6+ (free under 6)',
                '📸 The Great Buddha is jaw-droppingly massive',
                '🕳️ The pillar hole: kids can crawl through for good luck',
                '👶 Stroller-accessible main hall'
              ]
            }
          ],
          meals: [
            {
              type: '🍵 Matcha',
              name: 'Nakatanidou (Nara)',
              description: "Famous for high-speed mochi pounding — the owner pounds mochi at lightning speed in a mesmerizing performance. The matcha mochi (yomogi mochi) is soft, warm, and incredible. The performance alone is worth the stop.",
              meta: '💰 $ · 📍 Near Kintetsu Nara Station · Mochi pounding show'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kasuga Taisha Shrine',
              description: "Walk through the forest to Kasuga Taisha — Nara's most photogenic shrine. The approach is lined with 3,000 stone lanterns, many covered in moss. The vermillion shrine buildings against the forest green is stunning. Deer wander freely among the lanterns.",
              details: [
                '🏮 3,000 stone lanterns lining the approach',
                '⛩️ ¥500 for inner shrine · Grounds are free',
                '🦌 Deer everywhere on the path to the shrine',
                '📸 The moss-covered lanterns are incredibly photogenic'
              ]
            },
            {
              title: 'Naramachi Old Town',
              description: "Wander through Naramachi — the old merchant district with traditional wooden machiya houses, craft shops, and small cafés. Much quieter than the deer park area. Great for souvenir shopping — look for nara-zuke pickles, handmade textiles, and deer-themed everything.",
              details: [
                '🏘️ Traditional wooden townhouses converted to shops and cafés',
                '🛍️ Deer-themed souvenirs — from elegant to adorably kitsch',
                '📍 South of Sarusawa Pond'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Kamaiki (Nara)',
              description: "Traditional kamaage udon (udon served in the hot pot water with dipping sauce). Simple, satisfying, and completely pork-free. Great for families — the kids can eat udon easily.",
              meta: '💰 $$ · 📍 Near Nara Park · Hot pot udon · No pork'
            },
            {
              type: '🍽️ Dinner',
              name: 'Yakiniku M (Namba)',
              description: "Back in Osaka, celebrate with Japanese BBQ — premium wagyu beef grilled at your table. No pork needed when you have A5 wagyu! Kids love the interactive grilling. Order tongue, rib, and sirloin cuts.",
              meta: '💰 $$$ · 📍 Namba, Osaka · All-beef yakiniku · NO PORK'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6851, lng: 135.8390, label: 'Nara Park', num: 1, cat: 'attraction', desc: '1,200 wild deer that bow for crackers' },
        { lat: 34.6890, lng: 135.8399, label: 'Tōdai-ji Temple', num: 2, cat: 'attraction', desc: '15m bronze Buddha in massive wooden hall' },
        { lat: 34.6812, lng: 135.8497, label: 'Kasuga Taisha Shrine', num: 3, cat: 'attraction', desc: '3,000 stone lanterns through ancient forest' },
        { lat: 34.6780, lng: 135.8320, label: 'Naramachi', num: 4, cat: 'attraction', desc: 'Old merchant district with craft shops' },
        { lat: 34.6850, lng: 135.8325, label: 'Nakatanidou', num: 5, cat: 'food', desc: 'High-speed mochi pounding performance' },
        { lat: 34.6660, lng: 135.5020, label: 'Yakiniku M (Namba)', num: 6, cat: 'food', desc: 'Premium wagyu beef BBQ — no pork' }
      ]
    },
    {
      num: 9,
      date: '2026-05-23',
      neighborhoods: 'Osaka Castle · Shinsekai · teamLab Botanical Garden',
      title: 'Osaka Deep Dive — Castle, Shinsekai & teamLab',
      description: "Explore Osaka's own treasures today. Morning at Osaka Castle Park (stroller heaven), afternoon in the retro Shinsekai district for kushikatsu and the Tsūtenkaku Tower, and evening at teamLab Botanical Garden for an illuminated forest walk. Osaka rewards you for staying an extra day.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Osaka Castle Park',
              description: "Osaka Castle is surrounded by a massive park with moats, stone walls, and wide gravel paths perfect for strollers. The castle itself is a museum inside (elevator to the top floor for panoramic views). The park is the real star — cherry blossom trees, plum groves, and open lawns.",
              details: [
                '🏯 Castle museum: ¥600 adults, free for kids under 15',
                '🌿 Park is free and open — great for morning strolls',
                '🛗 Elevator inside the castle — fully accessible',
                '👶 Wide flat paths throughout the park grounds'
              ]
            }
          ],
          meals: [
            {
              type: '🍵 Matcha',
              name: 'Maru Sankaku Shikaku (Osaka)',
              description: "Trendy matcha café near Osaka Castle serving thick matcha lattes, matcha tiramisu, and seasonal matcha desserts. Beautiful interior for photos.",
              meta: '💰 $$ · 📍 Near Osaka Castle · Matcha desserts'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shinsekai District & Tsūtenkaku Tower',
              description: "Shinsekai ('New World') is Osaka's retro entertainment district — neon signs, blowfish lanterns, and the Tsūtenkaku Tower lit up like a beacon. It's kitschy, colorful, and very Osaka. Walk through the covered arcades and soak up the energy.",
              details: [
                '🗼 Tsūtenkaku Tower: ¥900 adults, ¥400 ages 5+',
                '🐡 Giant blowfish and crab signs everywhere',
                '🎮 Retro game arcades and crane game centers',
                '👶 Covered shopping arcades — rain-proof'
              ]
            },
            {
              title: 'Samurai Ninja Museum (Osaka)',
              description: "Interactive museum where you can try on samurai armor, hold replica swords, watch a ninja show, and learn throwing stars. The hands-on exhibits are perfect for kids (and adults who are kids at heart). Located in the Namba area.",
              details: [
                '🎫 ¥3,300 adults, ¥2,200 kids · Includes interactive experience',
                '⚔️ Try on real samurai armor for photos',
                '🥷 Ninja star throwing experience',
                '📍 Namba area — walking distance from Dōtonbori'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Kushikatsu Daruma (Shinsekai Original)',
              description: "The original Kushikatsu Daruma in Shinsekai — the birthplace of Osaka's famous deep-fried skewers. Get chicken, shrimp, asparagus, cheese, and lotus root. Skip the pork ones. The angry-face logo is iconic.",
              meta: '💰 $$ · 📍 Shinsekai · Chicken/shrimp/veggie skewers · No pork available'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'teamLab Botanical Garden Osaka',
              description: "teamLab's Osaka installation transforms the Nagai Botanical Garden into an illuminated digital forest at night. Walk through trees that glow and change color as you approach, wade through projected flower fields, and watch the garden come alive with light. A different vibe from Planets but equally magical.",
              details: [
                '🎫 ¥1,800 adults, ¥500 ages 4+ · Evening entry only',
                '🌳 Outdoor — dress for weather, bring mosquito repellent',
                '👶 Stroller-friendly paths through the garden',
                '📍 Nagai Park — about 25 min by subway from Namba'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Harukoma Sushi (Tennoji)',
              description: "Standing sushi bar famous for massive cuts of fresh fish at incredible prices. The tuna and salmon are legendary. Fast, fresh, no pork. The queue moves quickly.",
              meta: '💰 $$ · 📍 Tennoji/Shinsekai area · Standing sushi · No pork'
            }
          ],
          tips: [
            { type: 'tip', text: "teamLab Botanical Garden is best visited after dark — the installations only light up at night. Combine with an early dinner in Shinsekai." }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6873, lng: 135.5262, label: 'Osaka Castle', num: 1, cat: 'attraction', desc: 'Iconic castle with park, moats, and panoramic views' },
        { lat: 34.6523, lng: 135.5062, label: 'Shinsekai', num: 2, cat: 'attraction', desc: 'Retro neon entertainment district' },
        { lat: 34.6526, lng: 135.5064, label: 'Tsūtenkaku Tower', num: 3, cat: 'attraction', desc: 'Osaka\'s Eiffel Tower — retro and kitschy' },
        { lat: 34.6660, lng: 135.5017, label: 'Samurai Ninja Museum', num: 4, cat: 'attraction', desc: 'Try samurai armor and throw ninja stars' },
        { lat: 34.6210, lng: 135.5180, label: 'teamLab Botanical Garden', num: 5, cat: 'attraction', desc: 'Illuminated forest — digital art outdoors' },
        { lat: 34.6520, lng: 135.5058, label: 'Kushikatsu Daruma (Original)', num: 6, cat: 'food', desc: 'The OG kushikatsu — no pork options' },
        { lat: 34.6540, lng: 135.5132, label: 'Harukoma Sushi', num: 7, cat: 'food', desc: 'Standing sushi — massive fresh cuts, great prices' }
      ]
    },
    {
      num: 10,
      date: '2026-05-24',
      neighborhoods: 'Namba · Shinsaibashi · Kansai Airport',
      title: 'Last Morning — Osaka Souvenirs & Sayonara',
      description: "Your final morning in Japan. Squeeze in one more matcha, grab last-minute souvenirs at Shinsaibashi, hit One Piece and Naruto stores, pick up omiyage (gift snacks) at the station, and head to Kansai Airport. It's not goodbye — it's ittekimasu (I'll be back).",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinsaibashi Shopping & Character Stores',
              description: "Shinsaibashi-suji is Osaka's main shopping arcade — covered, long, and packed with everything from fast fashion to traditional crafts. Hit the One Piece Mugiwara Store and Naruto/Boruto store for anime souvenirs. Let the kids pick their favorite character goods.",
              details: [
                '🏴‍☠️ One Piece Mugiwara Store: official merch, exclusive Osaka items',
                '🍥 Naruto/Boruto store: Konoha headbands, kunai, plushies',
                '🛍️ Shinsaibashi-suji: covered arcade, stroller-friendly',
                '📍 Between Shinsaibashi and Namba stations'
              ]
            },
            {
              title: 'Bokksu Market / Omiyage Shopping',
              description: "Stock up on omiyage — Japanese gift snacks that are expected when you return from a trip. Tokyo Banana, Royce chocolate, regional Kit-Kats, matcha everything. Department store basements (depachika) are the best for this. Also check for Bokksu-featured Japanese snack boxes if available.",
              details: [
                '🎁 Depachika (basement food floors) at Takashimaya or Daimaru',
                '🍫 Regional Kit-Kats make perfect gifts',
                '🍵 Matcha cookies, senbei, and wagashi boxes',
                '📦 Many shops offer beautiful gift wrapping for free'
              ]
            }
          ],
          meals: [
            {
              type: '🍵 Matcha',
              name: 'Tsujiri Namba',
              description: "One last matcha for the road. Tsujiri's Namba shop serves matcha parfaits, lattes, and soft-serve. Savor every sip — you won't get matcha this good at home.",
              meta: '💰 $ · 📍 Namba · Last matcha in Japan'
            },
            {
              type: '☕ Brunch',
              name: 'Rikuro Ojisan no Mise',
              description: "Rikuro's famous jiggly cheesecake — light, fluffy, and wobbly like a cloud. Buy a whole one (¥965) and eat it warm from the oven. The kids will be hypnotized by the jiggle. Completely pork-free — just eggs, cream, and magic.",
              meta: '💰 $ · 📍 Namba · Iconic jiggly cheesecake · No pork'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kansai International Airport (KIX)',
              description: "Take the Nankai Rapi:t limited express from Namba to KIX — the train itself looks like a spaceship (kids will love it). About 40 minutes. Allow extra time with toddlers and luggage. KIX has great shopping and food after security — last chance for Japanese snacks and tax-free goods.",
              details: [
                '🚆 Nankai Rapi:t from Namba: ~40 min, ¥1,450 + seat fee',
                '🛫 Allow 3 hours before international flights with kids',
                '🛍️ Airside shops: more Kit-Kats, matcha, character goods',
                '👶 KIX has family rooms and nursing rooms in all terminals'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "If your flight is in the evening, you have time for a morning adventure. If it's early, simplify — matcha, cheesecake, train. Don't stress the last day." }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6720, lng: 135.5020, label: 'Shinsaibashi-suji', num: 1, cat: 'shopping', desc: 'Main shopping arcade — covered and endless' },
        { lat: 34.6700, lng: 135.5015, label: 'One Piece Mugiwara Store', num: 2, cat: 'shopping', desc: 'Official One Piece merchandise' },
        { lat: 34.6695, lng: 135.5018, label: 'Naruto/Boruto Store', num: 3, cat: 'shopping', desc: 'Konoha headbands, kunai, plushies' },
        { lat: 34.6660, lng: 135.5010, label: 'Rikuro Cheesecake', num: 4, cat: 'food', desc: 'Iconic jiggly cheesecake — eat it warm' },
        { lat: 34.6655, lng: 135.5005, label: 'Tsujiri Namba', num: 5, cat: 'food', desc: 'Last matcha — parfaits and soft-serve' },
        { lat: 34.4347, lng: 135.2440, label: 'Kansai Airport (KIX)', num: 6, cat: 'transport', desc: 'Departure — sayonara Japan' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '¥8,000–15,000/night', midrange: '¥15,000–30,000/night', luxury: '¥30,000–60,000/night' },
    { category: 'Meals (family of 5)', budget: '¥5,000–8,000/day', midrange: '¥10,000–18,000/day', luxury: '¥25,000–40,000/day' },
    { category: 'Transport (local)', budget: '¥2,000–4,000/day', midrange: '¥4,000–8,000/day', luxury: '¥10,000–20,000/day' },
    { category: 'Tokyo→Osaka Shinkansen', budget: '¥13,870/adult', midrange: '¥13,870/adult', luxury: '¥13,870/adult (Green Car: ¥19,040)' },
    { category: 'Activities', budget: '¥2,000–5,000/day', midrange: '¥5,000–12,000/day', luxury: '¥15,000–25,000/day' },
    { category: '10-Day Total (family of 5)', budget: '¥250,000–400,000', midrange: '¥450,000–750,000', luxury: '¥900,000–1,500,000' }
  ],

  practicalInfo: [
    { title: '✈️ Arriving', items: ['NRT (Narita) → Shinjuku: Narita Express (N\'EX) ~80 min or Limousine Bus ~100 min', 'Buy Suica/PASMO IC cards at the airport — works on all trains, buses, and konbini', 'Kids under 6: free on all trains (no seat), or buy a child ticket for a reserved seat'] },
    { title: '🏨 Accommodation', items: ['Tokyo: Shinjuku Airbnb (your booking — great location for everything)', 'Osaka: Book near Namba or Shinsaibashi for food/transit access', 'Look for family rooms or 2-bedroom apartments on Airbnb/Booking.com'] },
    { title: '🍖 NO PORK Guide', items: ['Say: \"buta nashi de onegaishimasu\" (豚なしでお願いします) = No pork please', 'Print/save an allergy card in Japanese explaining no pork', 'Tonkotsu ramen = pork broth. Choose shio (salt), shoyu (soy), or tori (chicken) instead', 'Gyoza usually contains pork — ask before ordering', 'Konbini onigiri: check for 豚 (buta/pork) on the label — salmon, tuna, umeboshi are safe'] },
    { title: '👶 Family Essentials', items: ['Nursing rooms (akachan rooms): in every department store and major station', 'Stroller rental: available at some malls and attractions', 'Konbini (7-11, Lawson, FamilyMart): diapers, wipes, baby food, milk 24/7', 'Most restaurants have high chairs — ask for \"kodomo isu\"', 'Japanese toilets have warm seats and bidets — the kids will be fascinated'] },
    { title: '🌡️ May Weather', items: ['Average 18-24°C (64-75°F) — pleasant spring weather', 'Occasional rain — pack a light rain jacket and stroller rain cover', 'UV is moderate — sunscreen for the outdoor days', 'Comfortable for walking all day — not too hot, not too cold'] },
    { title: '💳 Money & Tips', items: ['IC cards (Suica/PASMO) work for trains and many shops', 'Cash is still king at smaller shops and food stalls — carry ¥10,000-20,000', 'No tipping in Japan — ever. It\'s considered rude', '7-11 and Lawson ATMs accept foreign cards'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
