const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1773100928740_whin6n',
  email: 'colandroangela@gmail.com',
  destination: 'Japan',
  startDate: '2029-05-14',
  endDate: '2029-05-30',
  groupSize: '5+',
  requests: 'Shibuya, Harajuku, Akihabara, Ginza, Central Tokyo, Asakusa, Poke Park Kanto, Ghibli Park, Shinjuku, Kichijoji, Gotokuji, Izu Peninsula, Mt Fuji, Osaka, Kyoto, Nara, Mie and Toba, Nagoya, Hiroshima'
};

const day1 = {
  num: 1,
  date: '2029-05-14',
  neighborhoods: 'Shibuya · Harajuku · Omotesando',
  title: 'Welcome to Tokyo — Shibuya & Harajuku',
  description: "Touch down in Tokyo and dive straight into its most iconic neighborhoods. Cross the world-famous Shibuya Crossing, explore Harajuku's wild fashion scene, and kick off the trip with an evening izakaya feast.",
  timeBlocks: [
    {
      label: 'Afternoon',
      activities: [
        {
          title: 'Shibuya Crossing & Shibuya Sky',
          description: "After checking in, head to the world's busiest pedestrian crossing. Watch the organized chaos from the Starbucks above, then ascend Shibuya Sky — the open-air observation deck at Shibuya Scramble Square (230m) for 360° Tokyo panoramas.",
          details: [
            '📸 Shibuya Sky is best near sunset — book a timed slot online',
            '🐕 Visit the Hachiko statue outside Shibuya Station for the group photo',
            '🏬 Shibuya 109 is right here for Japanese street fashion shopping'
          ]
        }
      ]
    },
    {
      label: 'Evening',
      activities: [
        {
          title: 'Harajuku & Takeshita Street',
          description: "Walk from Shibuya to Harajuku (15 min) and stroll down Takeshita Street — Tokyo's wildest shopping lane packed with rainbow cotton candy, crepe stands, and kawaii fashion boutiques.",
          details: [
            '🍦 Try a rainbow cotton candy or Japanese crepe from Marion Crêpes',
            '🛍️ Omotesando is Tokyo\'s Champs-Élysées — luxury brands in stunning architecture',
            '⛩️ Meiji Jingu entrance is right here — save the full visit for another day'
          ]
        }
      ],
      meals: [
        {
          type: '🍺 Dinner',
          name: 'Uobei Shibuya (Genki Sushi)',
          description: 'High-speed conveyor belt sushi where you order on a touchscreen and plates zoom to your seat on a mini bullet train. Fun, casual, and incredibly affordable — perfect for a group.',
          meta: '💰 ¥1,000-2,000pp · 📍 Dogenzaka, Shibuya · No reservations, short wait'
        }
      ],
      tips: [
        { type: 'tip', text: "Jet-lagged? Shibuya's neon energy will wake you right up. Konbini (7-Eleven, Lawson) are open 24/7 for late-night snacks — their egg sandwiches are legendary." }
      ]
    }
  ],
  mapPins: [
    { lat: 35.6595, lng: 139.7004, label: 'Shibuya Crossing', num: 1, cat: 'attraction', desc: "World's busiest pedestrian crossing" },
    { lat: 35.6584, lng: 139.7022, label: 'Shibuya Sky', num: 2, cat: 'attraction', desc: '230m open-air observation deck with 360° views' },
    { lat: 35.6590, lng: 139.7006, label: 'Hachiko Statue', num: 3, cat: 'attraction', desc: 'Iconic loyal dog statue at Shibuya Station' },
    { lat: 35.6702, lng: 139.7028, label: 'Takeshita Street', num: 4, cat: 'attraction', desc: "Harajuku's wild fashion and snack street" },
    { lat: 35.6654, lng: 139.7100, label: 'Omotesando', num: 5, cat: 'attraction', desc: "Tokyo's elegant tree-lined shopping boulevard" },
    { lat: 35.6613, lng: 139.6980, label: 'Uobei Shibuya', num: 6, cat: 'food', desc: 'Bullet train conveyor belt sushi' }
  ]
};

const day2 = {
  num: 2,
  date: '2029-05-15',
  neighborhoods: 'Asakusa · Central Tokyo · Ueno',
  title: 'Ancient Asakusa & Imperial Tokyo',
  description: "Step back in time at Senso-ji, Tokyo's oldest temple, then contrast with the wide-open spaces around the Imperial Palace. End the day with a yakitori alley crawl.",
  timeBlocks: [
    {
      label: 'Morning',
      activities: [
        {
          title: 'Senso-ji Temple & Nakamise Street',
          description: "Arrive early at Senso-ji — Tokyo's oldest and most visited Buddhist temple (founded 645 AD). Walk through the massive Kaminarimon (Thunder Gate) and browse Nakamise-dori's 200+ stalls.",
          details: [
            '⛩️ Arrive before 9am to beat crowds — the temple is open 24/7',
            '🍡 Try ningyo-yaki (custard-filled cakes) and age-manju (fried sweet buns)',
            '📸 The five-story pagoda is stunning against blue sky'
          ]
        }
      ],
      meals: [
        {
          type: '☕ Breakfast',
          name: 'Pelican Café',
          description: 'Legendary Tokyo bakery since 1942, famous for their thick-cut milk bread toast. Small and always busy — arrive early.',
          meta: '💰 ¥500-800pp · 📍 Kotobuki, Taito · Closes when bread sells out'
        }
      ]
    },
    {
      label: 'Afternoon',
      activities: [
        {
          title: 'Imperial Palace East Gardens',
          description: 'Explore the Imperial Palace East Gardens — free, peaceful, and beautifully landscaped on the grounds of the former Edo Castle. The stone walls and moats are impressive remnants of the shogunate era.',
          details: [
            '🏯 Free admission · Closed Mon & Fri',
            '🌳 The ninomaru garden is stunning — traditional Japanese landscaping',
            '📸 Nijubashi Bridge with the palace in the background is the classic Tokyo shot'
          ]
        }
      ]
    },
    {
      label: 'Evening',
      activities: [
        {
          title: 'Ameyoko Market & Ueno',
          description: "Head to Ameyoko — the bustling market street under the Yamanote Line tracks near Ueno. Street vendors sell everything from fresh seafood to sneakers.",
          details: [
            '🦑 Fresh seafood stalls selling uni, crab legs, and grilled squid on sticks',
            '🍺 Grab tall boys from the vendors and street-drink like a local'
          ]
        }
      ],
      meals: [
        {
          type: '🍺 Dinner',
          name: 'Hoppy Street (Hoppy-dori)',
          description: 'A rowdy, festive alley of outdoor izakayas where locals gather for cheap yakitori, fried gyoza, and hoppy beer. Perfect for a group — just pick a stall and sit down.',
          meta: '💰 ¥1,500-3,000pp · 📍 Near Senso-ji, Asakusa · No reservations needed'
        }
      ]
    }
  ],
  mapPins: [
    { lat: 35.7148, lng: 139.7967, label: 'Senso-ji Temple', num: 1, cat: 'attraction', desc: "Tokyo's oldest Buddhist temple (645 AD)" },
    { lat: 35.7146, lng: 139.7966, label: 'Nakamise Street', num: 2, cat: 'attraction', desc: 'Traditional shopping street to the temple' },
    { lat: 35.6852, lng: 139.7528, label: 'Imperial Palace East Gardens', num: 3, cat: 'attraction', desc: 'Free gardens on former Edo Castle grounds' },
    { lat: 35.6812, lng: 139.7671, label: 'Tokyo Station', num: 4, cat: 'attraction', desc: 'Beautiful Meiji-era red brick station' },
    { lat: 35.7104, lng: 139.7748, label: 'Ameyoko Market', num: 5, cat: 'attraction', desc: 'Bustling market street under train tracks' },
    { lat: 35.7126, lng: 139.7944, label: 'Hoppy Street', num: 6, cat: 'food', desc: 'Rowdy izakaya alley near Senso-ji' }
  ]
};

const day3 = {
  num: 3,
  date: '2029-05-16',
  neighborhoods: 'Akihabara · Ginza · Tsukiji Outer Market',
  title: 'Otaku Paradise & Glamorous Ginza',
  description: "Morning in Akihabara's electric wonderland of anime, gaming, and gadgets. Afternoon, shift gears to the sophistication of Ginza. End with fresh sushi near the old Tsukiji market.",
  timeBlocks: [
    {
      label: 'Morning',
      activities: [
        {
          title: 'Akihabara Electric Town',
          description: "Dive into the sensory overload of Akihabara — Tokyo's otaku capital. Multi-story arcades, retro game shops, anime mega-stores, and themed cafés.",
          details: [
            '🎮 Super Potato — legendary retro game shop across 5 floors',
            '🕹️ SEGA and Taito Station arcades — UFO catchers, rhythm games, purikura',
            '📚 Mandarake — massive secondhand anime/manga store'
          ]
        }
      ],
      meals: [
        {
          type: '☕ Lunch',
          name: 'Kanda Matsuya',
          description: 'Historic soba noodle shop serving handmade buckwheat noodles since 1884. The cold soba with dipping sauce is sublime — a true Tokyo institution.',
          meta: '💰 ¥800-1,200pp · 📍 Kanda Sudacho, Chiyoda · Lunch rush 11:30-1pm'
        }
      ]
    },
    {
      label: 'Afternoon',
      activities: [
        {
          title: 'Ginza District',
          description: "Tokyo's most glamorous neighborhood — broad boulevards lined with flagship stores, art galleries, and department stores. Architecture from the futuristic Mikimoto building to the classic Wako clock tower.",
          details: [
            '🏬 Ginza Six — luxury mall with rooftop garden and Tsutaya bookshop',
            '🎨 Ginza galleries are free — check Shiseido Gallery or Pola Museum Annex',
            '📸 On weekends, Chuo-dori becomes a pedestrian-only promenade'
          ]
        }
      ]
    },
    {
      label: 'Evening',
      activities: [
        {
          title: 'Tsukiji Outer Market Area',
          description: "The outer market still thrives with dozens of stalls and small restaurants serving the freshest sushi, tamagoyaki, and wagyu skewers. Visit for the atmosphere and late-afternoon bites.",
          details: [
            '🥚 Yamacho — famous tamagoyaki (sweet egg omelet on a stick)',
            '🐟 Sushi Zanmai for great quality without insane waits'
          ]
        }
      ],
      meals: [
        {
          type: '🍷 Dinner',
          name: 'Uoshin Nihonbashi',
          description: 'Fresh-from-market seafood izakaya with excellent sashimi platters perfect for sharing. Cold sake and a lively group atmosphere.',
          meta: '💰 ¥3,000-5,000pp · 📍 Nihonbashi area · Reservations recommended for 5+'
        }
      ],
      tips: [
        { type: 'tip', text: "Ginza can be pricey, but window shopping is free and the architecture is incredible. Save your yen for the food — that's where it really shines." }
      ]
    }
  ],
  mapPins: [
    { lat: 35.6984, lng: 139.7712, label: 'Akihabara Electric Town', num: 1, cat: 'attraction', desc: 'Otaku paradise — anime, gaming, electronics' },
    { lat: 35.6997, lng: 139.7710, label: 'Super Potato', num: 2, cat: 'attraction', desc: 'Legendary retro game shop' },
    { lat: 35.6953, lng: 139.7649, label: 'Kanda Matsuya', num: 3, cat: 'food', desc: 'Historic soba noodles since 1884' },
    { lat: 35.6717, lng: 139.7649, label: 'Ginza District', num: 4, cat: 'attraction', desc: "Tokyo's most glamorous shopping boulevard" },
    { lat: 35.6654, lng: 139.7707, label: 'Ginza Six', num: 5, cat: 'attraction', desc: 'Luxury mall with rooftop garden' },
    { lat: 35.6655, lng: 139.7706, label: 'Tsukiji Outer Market', num: 6, cat: 'food', desc: 'Fresh sushi, tamagoyaki & street food stalls' }
  ]
};

const day4 = {
  num: 4,
  date: '2029-05-17',
  neighborhoods: 'Shinjuku · Kabukicho · Golden Gai',
  title: 'Shinjuku — Gardens, Neon & Legendary Nightlife',
  description: "Explore Tokyo's vibrant Shinjuku — morning in the serene Gyoen gardens, afternoon skyscraper views, then the main event: Golden Gai and Kabukicho after dark.",
  timeBlocks: [
    {
      label: 'Morning',
      activities: [
        {
          title: 'Shinjuku Gyoen National Garden',
          description: "One of Tokyo's most beautiful parks — 144 acres of French formal, English landscape, and Japanese traditional gardens. In late May, the iris and rose gardens are in full bloom.",
          details: [
            '🌹 Rose garden peaks mid-May — over 100 varieties',
            '🍱 No alcohol allowed, but picnics welcome — grab bento from a konbini',
            '💰 ¥500 admission · Open 9am-6pm'
          ]
        }
      ]
    },
    {
      label: 'Afternoon',
      activities: [
        {
          title: 'Tokyo Metropolitan Government Building',
          description: 'Free 202m observation decks with panoramic city views. On clear days you can see Mt Fuji to the west.',
          details: [
            '🏙️ North & South observation decks — both free, North less crowded',
            '🛍️ Don Quijote Shinjuku nearby — chaotic discount shopping for souvenirs'
          ]
        }
      ],
      meals: [
        {
          type: '☕ Lunch',
          name: 'Fuunji Ramen',
          description: 'Legendary tsukemen (dipping ramen) shop — rich, thick, intensely flavored fish and pork broth with springy noodles. Always a line, always worth it.',
          meta: '💰 ¥900-1,200pp · 📍 Near Shinjuku South Exit · Expect 20-40 min wait'
        }
      ]
    },
    {
      label: 'Night',
      activities: [
        {
          title: 'Golden Gai Bar Hopping',
          description: "Tokyo's legendary nightlife district — six narrow alleys packed with over 200 tiny bars, each seating just 5-10 people. Every bar has its own theme, music, and personality.",
          details: [
            '🍸 Most bars charge a ¥500-1,000 seating charge — totally normal',
            '🎵 Try Albatross (chandelier bar), Deathmatch in Hell (horror), or Champion',
            '👥 Group of 5+ will need to split up — bars are TINY. Part of the charm.'
          ]
        },
        {
          title: 'Kabukicho & Godzilla Head',
          description: "Walk through the neon-drenched streets of Kabukicho. The giant Godzilla head atop Shinjuku Toho Building is an iconic photo op.",
          details: [
            '🦎 Godzilla head best seen from below at night',
            '⚠️ Area is safe but avoid touts offering "free drinks"'
          ]
        }
      ],
      meals: [
        {
          type: '🍺 Dinner',
          name: 'Omoide Yokocho (Memory Lane)',
          description: 'Smoky alley of tiny yakitori joints feeding Shinjuku since the 1940s. Squeeze onto a stool, order chicken skewers and beer, and soak up old Tokyo.',
          meta: '💰 ¥1,500-3,000pp · 📍 West side of Shinjuku Station · Best after 6pm'
        }
      ]
    }
  ],
  mapPins: [
    { lat: 35.6852, lng: 139.7100, label: 'Shinjuku Gyoen', num: 1, cat: 'attraction', desc: '144-acre garden with Japanese, French & English sections' },
    { lat: 35.6896, lng: 139.6917, label: 'Tokyo Metropolitan Government Bldg', num: 2, cat: 'attraction', desc: 'Free 202m observation decks' },
    { lat: 35.6880, lng: 139.6999, label: 'Fuunji Ramen', num: 3, cat: 'food', desc: 'Legendary tsukemen dipping ramen' },
    { lat: 35.6938, lng: 139.7040, label: 'Golden Gai', num: 4, cat: 'nightlife', desc: '200+ tiny themed bars in narrow alleys' },
    { lat: 35.6955, lng: 139.7015, label: 'Omoide Yokocho', num: 5, cat: 'food', desc: 'Smoky yakitori alley since the 1940s' },
    { lat: 35.6945, lng: 139.7013, label: 'Kabukicho / Godzilla Head', num: 6, cat: 'attraction', desc: 'Neon entertainment district' }
  ]
};

const day5 = {
  num: 5,
  date: '2029-05-18',
  neighborhoods: 'Gotokuji · Kichijoji · Shimokitazawa',
  title: 'Local Tokyo — Lucky Cats, Parks & Vintage Vibes',
  description: "Escape the tourist trail into Tokyo's beloved local neighborhoods. Morning at the charming cat temple of Gotokuji, afternoon in Kichijoji's parks and markets, evening in bohemian Shimokitazawa.",
  timeBlocks: [
    {
      label: 'Morning',
      activities: [
        {
          title: 'Gotokuji Temple — The Lucky Cat Temple',
          description: "This serene Buddhist temple is the birthplace of the maneki-neko (beckoning cat). Hundreds of white lucky cat figurines line shelves and altars, left by visitors whose wishes came true.",
          details: [
            '🐱 Buy a small maneki-neko (from ¥300) and make a wish',
            '📸 The shelves overflowing with cat figurines are incredibly photogenic',
            '🚃 Take Odakyu Line to Gotokuji Station — 5 min walk',
            '⏰ Free admission · Best visited morning for quiet'
          ]
        }
      ]
    },
    {
      label: 'Afternoon',
      activities: [
        {
          title: 'Kichijoji & Inokashira Park',
          description: "Consistently voted Tokyo's most desirable neighborhood. Stroll through Inokashira Park, rent swan boats on the lake, and explore the Harmonica Yokocho alley of tiny bars and eateries.",
          details: [
            '🦢 Swan boat rentals on Inokashira Pond — ¥700/30 min',
            '🛍️ Harmonica Yokocho — maze of yakitori bars, craft shops, and vintage stores',
            '🍖 Satou — famous butcher with legendary ¥240 menchi katsu (meat croquettes)'
          ]
        }
      ],
      meals: [
        {
          type: '☕ Lunch',
          name: 'Satou Menchi Katsu + Harmonica Yokocho',
          description: 'Grab the famous ¥240 menchi katsu from the legendary Satou butcher, then find a Harmonica Yokocho spot for cold beer and yakitori.',
          meta: '💰 ¥1,000-2,000pp · 📍 Kichijoji · Satou line moves fast'
        }
      ]
    },
    {
      label: 'Evening',
      activities: [
        {
          title: 'Shimokitazawa — Vintage, Cafés & Live Music',
          description: "Tokyo's bohemian heart. Narrow streets packed with vintage clothing stores, record shops, indie cafés, and live music venues. Like Williamsburg meets Harajuku.",
          details: [
            '👗 New York Joe Exchange and Flamingo are top vintage shops',
            '🎵 Check live music at Shelter or THREE',
            '🍺 Shimokita Taproom for excellent craft beer'
          ]
        }
      ],
      meals: [
        {
          type: '🍺 Dinner',
          name: 'Shirube Shimokitazawa',
          description: 'Cozy izakaya serving creative Japanese small plates and excellent sake. Warm and inviting — perfect for a group dinner after vintage shopping.',
          meta: '💰 ¥2,500-4,000pp · 📍 Shimokitazawa · Reservations recommended'
        }
      ]
    }
  ],
  mapPins: [
    { lat: 35.6593, lng: 139.6491, label: 'Gotokuji Temple', num: 1, cat: 'attraction', desc: 'Birthplace of the lucky cat — hundreds of maneki-neko' },
    { lat: 35.7032, lng: 139.5796, label: 'Inokashira Park', num: 2, cat: 'attraction', desc: 'Beautiful park with swan boats' },
    { lat: 35.7034, lng: 139.5800, label: 'Harmonica Yokocho', num: 3, cat: 'food', desc: 'Maze of tiny yakitori bars in Kichijoji' },
    { lat: 35.7038, lng: 139.5804, label: 'Satou Menchi Katsu', num: 4, cat: 'food', desc: 'Legendary ¥240 meat croquettes' },
    { lat: 35.6609, lng: 139.6687, label: 'Shimokitazawa', num: 5, cat: 'attraction', desc: "Tokyo's bohemian vintage quarter" },
    { lat: 35.6612, lng: 139.6690, label: 'Shirube Izakaya', num: 6, cat: 'food', desc: 'Creative small plates & sake' }
  ]
};


const day6 = {
  num: 6,
  date: '2029-05-19',
  neighborhoods: 'Meiji Jingu · Yoyogi Park · Roppongi',
  title: 'Meiji Shrine, Yoyogi Park & Roppongi Night Out',
  description: "Start with a peaceful morning at Tokyo's grandest Shinto shrine, spend the afternoon people-watching in Yoyogi Park, then hit Roppongi for rooftop views and the city's most international nightlife scene.",
  timeBlocks: [
    {
      label: 'Morning',
      activities: [
        {
          title: 'Meiji Jingu Shrine',
          description: "Tokyo's most important Shinto shrine, set in 170 acres of forested parkland. The towering torii gate and gravel path through ancient trees feels like entering another world — right in the middle of the city.",
          details: [
            '⛩️ The massive cypress wood torii gate at the entrance is 12m tall',
            '🌳 The forest was planted in 1920 with 100,000 donated trees from across Japan',
            '🍶 Write a wish on an ema (wooden plaque) and hang it at the shrine',
            '⏰ Free admission · Opens at sunrise, closes at sunset'
          ]
        }
      ]
    },
    {
      label: 'Afternoon',
      activities: [
        {
          title: 'Yoyogi Park',
          description: "Tokyo's Central Park. On weekends, the park comes alive with street performers, rockabilly dancers, cosplayers, and picnicking families. Rent a blanket and people-watch.",
          details: [
            '🎸 The rockabilly dancers at Harajuku entrance are a Tokyo institution',
            '🌸 Beautiful in any season — green and lush in May',
            '🍺 Pick up drinks and snacks from the konbini for a park session'
          ]
        }
      ],
      meals: [
        {
          type: '☕ Lunch',
          name: 'Afuri Ramen (Harajuku)',
          description: 'Famous yuzu shio (citrus salt) ramen — lighter and more refreshing than typical heavy tonkotsu. Beautiful modern space with an open kitchen.',
          meta: '💰 ¥1,000-1,500pp · 📍 Harajuku/Omotesando area · Quick-casual'
        }
      ]
    },
    {
      label: 'Night',
      activities: [
        {
          title: 'Roppongi Hills & Mori Art Museum',
          description: "Head to Roppongi Hills for the Mori Art Museum (52nd floor) and the Sky Deck rooftop — an open-air helipad turned observation platform. The night views are breathtaking.",
          details: [
            '🎨 Mori Art Museum stays open until 10pm — contemporary art with views',
            '🌃 Sky Deck (rooftop) costs extra but has unobstructed 360° night views',
            '📸 Tokyo Tower lit up against the cityscape is magical from here'
          ]
        },
        {
          title: 'Roppongi Nightlife',
          description: "Roppongi is Tokyo's most international party district. From upscale cocktail bars to massive clubs, this is where the night never ends.",
          details: [
            '🍸 Try Two Rooms — sophisticated rooftop bar with skyline views',
            '🎶 If you want to dance, V2 Tokyo or 1OAK are the big clubs',
            '🍻 For casual vibes, the alleys behind Roppongi Crossing have small bars'
          ]
        }
      ],
      meals: [
        {
          type: '🍷 Dinner',
          name: 'Gonpachi Nishi-Azabu',
          description: "The restaurant that inspired the iconic fight scene in Kill Bill. Multi-level wooden interior, excellent yakitori, soba, and tempura. A fun group dining experience with theatrical atmosphere.",
          meta: '💰 ¥3,000-5,000pp · 📍 Nishi-Azabu · Reservations recommended for 5+'
        }
      ]
    }
  ],
  mapPins: [
    { lat: 35.6764, lng: 139.6993, label: 'Meiji Jingu Shrine', num: 1, cat: 'attraction', desc: "Tokyo's grandest Shinto shrine in 170 acres of forest" },
    { lat: 35.6717, lng: 139.6949, label: 'Yoyogi Park', num: 2, cat: 'attraction', desc: "Tokyo's Central Park — street performers & picnics" },
    { lat: 35.6656, lng: 139.7078, label: 'Afuri Ramen', num: 3, cat: 'food', desc: 'Famous yuzu citrus salt ramen' },
    { lat: 35.6604, lng: 139.7292, label: 'Roppongi Hills / Mori Art Museum', num: 4, cat: 'attraction', desc: '52nd floor art museum with night city views' },
    { lat: 35.6627, lng: 139.7261, label: 'Gonpachi Nishi-Azabu', num: 5, cat: 'food', desc: 'Kill Bill restaurant — yakitori & soba' },
    { lat: 35.6627, lng: 139.7316, label: 'Roppongi Nightlife', num: 6, cat: 'nightlife', desc: "Tokyo's international party district" }
  ]
};

const day7 = {
  num: 7,
  date: '2029-05-20',
  neighborhoods: 'Yomiuriland · PokéPark KANTO',
  title: 'PokéPark KANTO — Gotta Catch \'Em All!',
  description: "Dedicate a full day to PokéPark KANTO at Yomiuriland — Tokyo's massive Pokémon theme park. Ride the gondola up, explore themed zones, watch live shows, and collect exclusive Pokémon merch. A must for any fan.",
  timeBlocks: [
    {
      label: 'Morning',
      activities: [
        {
          title: 'Travel to PokéPark KANTO',
          description: "Take the Keio Line to Keio-Yomiuriland Station, then ride the Sky Shuttle gondola up to the park — the aerial views of the surrounding hills are beautiful. Download the official PokéPark app before you go!",
          details: [
            '📱 DOWNLOAD THE APP BEFOREHAND — you need it for show lotteries and reservations',
            '🚡 The gondola ride is part of the experience — great views',
            '⏰ Arrive by 9:30am — gates open at 10am and popular attractions fill up fast',
            '🎫 Book tickets well in advance online — they sell out'
          ]
        }
      ]
    },
    {
      label: 'Afternoon',
      activities: [
        {
          title: 'PokéPark KANTO Exploration',
          description: "Explore the themed zones featuring life-size Pokémon encounters, interactive experiences, and photo ops galore. The Kanto region comes alive with themed rides, shows, and activities.",
          details: [
            '📸 Life-size Pokémon statues and encounter zones throughout',
            '🎭 Enter the show lottery via the app for live performances',
            '🛍️ The gift shop has park-exclusive merch you can\'t get anywhere else',
            '🍦 Pokémon-themed food stalls — Pikachu curry, Pokéball onigiri, character drinks'
          ]
        }
      ],
      meals: [
        {
          type: '☕ Lunch',
          name: 'PokéPark Food Court',
          description: 'Character-themed meals inside the park — Pikachu curry, Eevee parfaits, and Pokéball-shaped rice balls. Half the fun is eating food that looks like Pokémon.',
          meta: '💰 ¥1,000-2,000pp · 📍 Inside PokéPark · Multiple stalls'
        }
      ]
    },
    {
      label: 'Evening',
      activities: [
        {
          title: 'Yomiuriland Evening & Return',
          description: "If you still have energy, explore the rest of Yomiuriland amusement park (separate tickets). Take the gondola back down as the sun sets — the views of Tokyo's skyline are gorgeous.",
          details: [
            '🎢 Yomiuriland has roller coasters and rides if the group wants more thrills',
            '🌅 Evening gondola ride back is beautiful at golden hour'
          ]
        }
      ],
      meals: [
        {
          type: '🍺 Dinner',
          name: 'Ichiran Ramen (Shinjuku)',
          description: "End the day with Japan's most famous solo-dining ramen chain. Individual booths with customizable broth — choose richness, spice level, garlic, and noodle firmness.",
          meta: '💰 ¥1,000-1,500pp · 📍 Shinjuku · Open late, no reservations'
        }
      ],
      tips: [
        { type: 'tip', text: "PokéPark can easily fill a full day. Battery packs are essential — the app drains your phone. Bring rain gear just in case (late May can be unpredictable)." }
      ]
    }
  ],
  mapPins: [
    { lat: 35.6256, lng: 139.5175, label: 'Keio-Yomiuriland Station', num: 1, cat: 'transport', desc: 'Starting point — take the gondola up' },
    { lat: 35.6285, lng: 139.5178, label: 'PokéPark KANTO', num: 2, cat: 'attraction', desc: 'Massive Pokémon theme park at Yomiuriland' },
    { lat: 35.6280, lng: 139.5180, label: 'PokéPark Food Court', num: 3, cat: 'food', desc: 'Character-themed Pokémon meals' },
    { lat: 35.6275, lng: 139.5183, label: 'Yomiuriland', num: 4, cat: 'attraction', desc: 'Amusement park with rides & evening views' },
    { lat: 35.6938, lng: 139.7035, label: 'Ichiran Ramen Shinjuku', num: 5, cat: 'food', desc: 'Famous customizable ramen booths' }
  ]
};

const day8 = {
  num: 8,
  date: '2029-05-21',
  neighborhoods: 'Izu Peninsula · Atami · Jogasaki Coast',
  title: 'Izu Peninsula — Coastal Cliffs & Hot Springs',
  description: "Leave Tokyo behind and head south to the Izu Peninsula. Take the bullet train to Atami, explore dramatic coastal cliffs on the Jogasaki Coast trail, and soak in natural onsen overlooking the Pacific Ocean. Adventure and relaxation in one day.",
  timeBlocks: [
    {
      label: 'Morning',
      activities: [
        {
          title: 'Shinkansen to Atami & Izu Coast',
          description: "Take the Tokaido Shinkansen from Tokyo to Atami (45 minutes), then connect to local trains along the eastern Izu coast. The scenery shifts from cityscape to ocean views and lush green mountains.",
          details: [
            '🚅 Shinkansen Kodama to Atami — about 45 min from Tokyo Station',
            '🌊 Sit on the left side for ocean views along the coast',
            '🏨 Consider staying overnight in a ryokan for the full experience'
          ]
        }
      ]
    },
    {
      label: 'Afternoon',
      activities: [
        {
          title: 'Jogasaki Coast Hiking Trail',
          description: "One of Japan's most spectacular coastal walks. Follow clifftop paths past dramatic rock formations, cross a suspension bridge 48m above the ocean, and pass a lighthouse with panoramic views. The adventure highlight of the trip.",
          details: [
            '🌉 The Kadowaki Suspension Bridge (48m high, 60m long) is thrilling',
            '🥾 Full trail is 9km but the best section (bridge to lighthouse) is about 3km',
            '🌊 Waves crash against volcanic rock formations below — incredible sounds',
            '📸 Jogasaki Lighthouse has 360° views — don\'t miss the stairs up'
          ]
        }
      ],
      meals: [
        {
          type: '☕ Lunch',
          name: 'Local Seafood Shokudo',
          description: 'Stop at a local shokudo (cafeteria) near Izu-Kogen Station for fresh-caught kinmedai (golden-eye snapper) — the regional specialty. Simple, fresh, incredible.',
          meta: '💰 ¥1,200-2,000pp · 📍 Near Izu-Kogen Station · Cash preferred'
        }
      ]
    },
    {
      label: 'Evening',
      activities: [
        {
          title: 'Onsen & Relaxation',
          description: "Check into a ryokan (traditional Japanese inn) with natural hot spring baths. Soak in an outdoor rotenburo overlooking the ocean as the sun sets. This is the relaxation the trip was built for.",
          details: [
            '♨️ Most ryokans include kaiseki dinner and breakfast in the rate',
            '🧖 Onsen etiquette: wash thoroughly before entering, no swimwear, towels stay outside the water',
            '👘 Wear the provided yukata (light kimono) around the inn — it\'s expected and comfortable',
            '🌅 Request an ocean-view room for sunset from the bath'
          ]
        }
      ],
      meals: [
        {
          type: '🍷 Dinner',
          name: 'Ryokan Kaiseki Dinner',
          description: 'Multi-course traditional Japanese dinner served in your room — local seafood, seasonal vegetables, delicate preparations. Usually 8-12 courses. An unforgettable culinary experience.',
          meta: '💰 Included with ryokan stay · 📍 In-room dining'
        }
      ]
    }
  ],
  mapPins: [
    { lat: 35.1040, lng: 139.0742, label: 'Atami Station', num: 1, cat: 'transport', desc: 'Gateway to Izu — 45 min from Tokyo by Shinkansen' },
    { lat: 34.9000, lng: 139.1300, label: 'Jogasaki Coast', num: 2, cat: 'attraction', desc: 'Dramatic clifftop hiking trail above the Pacific' },
    { lat: 34.9015, lng: 139.1310, label: 'Kadowaki Suspension Bridge', num: 3, cat: 'attraction', desc: '48m-high bridge over crashing waves' },
    { lat: 34.8950, lng: 139.1350, label: 'Jogasaki Lighthouse', num: 4, cat: 'attraction', desc: '360° coastal panoramas' },
    { lat: 34.9100, lng: 139.1050, label: 'Izu-Kogen Area', num: 5, cat: 'attraction', desc: 'Highland resort area with ryokans & onsen' }
  ]
};


const day9 = {
  num: 9,
  date: '2029-05-22',
  neighborhoods: 'Mt Fuji · Kawaguchiko · Fuji Five Lakes',
  title: 'Mt Fuji — Japan\'s Sacred Peak',
  description: "Travel from Izu to the Fuji Five Lakes region for jaw-dropping views of Japan's most iconic mountain. Cycle around Lake Kawaguchi, visit the Chureito Pagoda, and feel the spiritual power of Fuji-san up close.",
  timeBlocks: [
    {
      label: 'Morning',
      activities: [
        {
          title: 'Travel to Kawaguchiko',
          description: "Head north from Izu through scenic mountain roads to the Fuji Five Lakes region. The first glimpse of Mt Fuji emerging above the treeline is unforgettable — especially with the snow-capped peak against clear May skies.",
          details: [
            '🚌 Bus from Mishima or train connections via Kofu — about 2-3 hours from Izu',
            '🗻 Mt Fuji still has snow on the summit in May — perfect for photos',
            '📸 Clear mornings offer the best views — cloud cover often builds by afternoon'
          ]
        },
        {
          title: 'Chureito Pagoda',
          description: "Climb 398 steps to this five-story pagoda for the most famous view in Japan — the bright red pagoda framing Mt Fuji with cherry trees in the foreground (though by May, it's green and lush instead of pink).",
          details: [
            '📸 THE classic Japan postcard shot — red pagoda + Fuji',
            '🥾 398 steps up — moderate effort, huge reward',
            '⏰ Go early morning for fewest crowds and best light'
          ]
        }
      ]
    },
    {
      label: 'Afternoon',
      activities: [
        {
          title: 'Lake Kawaguchiko Cycling',
          description: "Rent bikes and cycle the scenic path around Lake Kawaguchi — the reflections of Mt Fuji in the calm lake water are mesmerizing. Stop at lakeside cafés, art museums, and photo spots along the 20km circuit.",
          details: [
            '🚲 Bike rentals available at Kawaguchiko Station — about ¥1,000/day',
            '📸 Ubuyagasaki cape has the best Fuji reflection photo spot',
            '☕ Kachi Kachi Ropeway takes you to Mt Tenjo for aerial views',
            '🌊 Lake is calm in the morning — best for mirror-like Fuji reflections'
          ]
        }
      ],
      meals: [
        {
          type: '☕ Lunch',
          name: 'Houtou Fudou',
          description: "Kawaguchiko's most famous restaurant serving houtou — flat udon noodles in a thick miso-based soup with pumpkin and vegetables. The regional specialty, perfect fuel for cycling.",
          meta: '💰 ¥1,200-1,800pp · 📍 Kawaguchiko · Expect a wait on weekends'
        }
      ]
    },
    {
      label: 'Evening',
      activities: [
        {
          title: 'Fujisan Onsen & Sunset Views',
          description: "Soak in a hot spring with Mt Fuji views as the sun sets behind the mountain. Several public onsen and hotel baths in the area offer stunning Fuji panoramas.",
          details: [
            '♨️ Fujiyama Onsen is a large public facility near Kawaguchiko Station',
            '🌅 Golden hour on Fuji is spectacular — the alpenglow effect turns the peak pink',
            '🏨 Many lakeside hotels have Fuji-view baths'
          ]
        }
      ],
      meals: [
        {
          type: '🍷 Dinner',
          name: 'Local Izakaya near Kawaguchiko',
          description: 'Casual izakaya dinner featuring local specialties — venison, horse sashimi (basashi), and fresh river fish. The Fuji area has a distinctive mountain cuisine quite different from coastal cities.',
          meta: '💰 ¥2,500-4,000pp · 📍 Kawaguchiko town'
        }
      ]
    }
  ],
  mapPins: [
    { lat: 35.4960, lng: 138.7620, label: 'Chureito Pagoda', num: 1, cat: 'attraction', desc: 'Famous red pagoda with Mt Fuji backdrop' },
    { lat: 35.5104, lng: 138.7530, label: 'Lake Kawaguchiko', num: 2, cat: 'attraction', desc: 'Scenic lake with Mt Fuji reflections' },
    { lat: 35.5070, lng: 138.7550, label: 'Kawaguchiko Station', num: 3, cat: 'transport', desc: 'Hub for Fuji Five Lakes — bike rentals here' },
    { lat: 35.5120, lng: 138.7470, label: 'Houtou Fudou', num: 4, cat: 'food', desc: 'Famous thick miso udon with pumpkin' },
    { lat: 35.5108, lng: 138.7610, label: 'Kachi Kachi Ropeway', num: 5, cat: 'attraction', desc: 'Aerial ropeway to Mt Tenjo viewpoint' }
  ]
};

const day10 = {
  num: 10,
  date: '2029-05-23',
  neighborhoods: 'Nagoya · Ghibli Park · Aichi',
  title: 'Ghibli Park — Walking Through Miyazaki\'s Dreams',
  description: "Travel to Nagoya and spend the day at Ghibli Park — Studio Ghibli's magical theme park set within the Aichi Commemorative Park. Walk through recreations of scenes from Totoro, Spirited Away, Howl's Moving Castle, and more.",
  timeBlocks: [
    {
      label: 'Morning',
      activities: [
        {
          title: 'Travel to Nagoya & Ghibli Park',
          description: "Take the Shinkansen from Mishima (near Fuji) to Nagoya (about 1.5 hours), then the Linimo monorail to Ai-chikyuhaku-kinen-koen Station. Ghibli Park is spread across five areas within the larger commemorative park.",
          details: [
            '🚅 Tokaido Shinkansen to Nagoya — about 1.5 hours',
            '🚝 Linimo monorail from Fujigaoka to the park entrance',
            '🎫 TICKETS MUST BE PRE-BOOKED — they sell out months ahead. Use Boo-Woo Ticket or Lawson',
            '📱 The O-Sanpo Day Pass covers all 5 areas (morning or afternoon slot)'
          ]
        },
        {
          title: 'Ghibli\'s Grand Warehouse',
          description: "An indoor area recreating scenes from across Ghibli's filmography. Walk through the fantastical food stalls from Spirited Away, sit in Catbus, explore a 1:1 recreation of the Boiler Room, and discover hidden Ghibli characters throughout.",
          details: [
            '📸 No-Face train from Spirited Away — sit next to the spirit for photos',
            '🐱 The life-size Catbus is a highlight — kids and adults love it equally',
            '🎬 Mini-theater shows exclusive Ghibli short films (included with ticket)'
          ]
        }
      ]
    },
    {
      label: 'Afternoon',
      activities: [
        {
          title: 'Hill of Youth & Dondoko Forest',
          description: "Explore the outdoor areas — the Hill of Youth features a recreation of the antique shop from Whisper of the Heart, while Dondoko Forest has Satsuki and Mei's house from My Neighbor Totoro in a beautiful woodland setting.",
          details: [
            '🏡 Satsuki and Mei\'s House — meticulously recreated with period-accurate furnishings',
            '🌳 Dondoko Forest walk — giant Totoro statue at the top of the trail',
            '🏰 Valley of Witches features Howl\'s Moving Castle and Witch\'s House',
            '🚶 The park is spread out — wear comfortable shoes, expect lots of walking'
          ]
        }
      ],
      meals: [
        {
          type: '☕ Lunch',
          name: 'Ghibli Park Café / Lawn Picnic',
          description: 'The park has food stalls and the surrounding Aichi Park has picnic areas. Alternatively, grab bento from Nagoya Station konbini before arriving.',
          meta: '💰 ¥800-1,500pp · 📍 Inside park or surrounding green areas'
        }
      ]
    },
    {
      label: 'Evening',
      activities: [
        {
          title: 'Nagoya Evening — Osu & Sakae',
          description: "Head back to central Nagoya. Explore the Osu shopping arcade — a vibrant covered market street with vintage shops, electronics, and street food. Then head to Sakae for Nagoya's nightlife scene.",
          details: [
            '🛍️ Osu Kannon shopping district — 1,200 shops in covered arcades',
            '🏯 Nagoya Castle is nearby if you want a quick evening photo of the illuminated castle',
            '🍺 Sakae district has Nagoya\'s best bars and clubs'
          ]
        }
      ],
      meals: [
        {
          type: '🍺 Dinner',
          name: 'Yamamotoya Honten — Miso Nikomi Udon',
          description: 'Nagoya\'s signature dish: thick udon noodles simmered in rich red miso broth in a clay pot. Yamamotoya is the most famous purveyor — hearty, warming, and uniquely Nagoya.',
          meta: '💰 ¥1,000-1,800pp · 📍 Multiple locations in Nagoya · No reservations needed'
        }
      ],
      tips: [
        { type: 'tip', text: 'Ghibli Park tickets sell out months in advance! Book as early as possible. The park is not an amusement park — it is a walking experience. There are no rides, just beautifully crafted worlds to explore.' }
      ]
    }
  ],
  mapPins: [
    { lat: 35.1709, lng: 137.0864, label: 'Nagoya Station', num: 1, cat: 'transport', desc: 'Shinkansen hub — transfer to Linimo here' },
    { lat: 35.1815, lng: 137.0903, label: 'Ghibli Park', num: 2, cat: 'attraction', desc: "Studio Ghibli's magical theme park" },
    { lat: 35.1820, lng: 137.0900, label: "Grand Warehouse", num: 3, cat: 'attraction', desc: 'Indoor Ghibli film recreations' },
    { lat: 35.1810, lng: 137.0910, label: 'Dondoko Forest', num: 4, cat: 'attraction', desc: "Satsuki & Mei's house from Totoro" },
    { lat: 35.1700, lng: 137.0850, label: 'Yamamotoya Honten', num: 5, cat: 'food', desc: "Nagoya's famous miso nikomi udon" },
    { lat: 35.1590, lng: 136.9025, label: 'Osu Shopping Arcade', num: 6, cat: 'attraction', desc: '1,200 shops in covered arcades' }
  ]
};

const day11 = {
  num: 11,
  date: '2029-05-24',
  neighborhoods: 'Ise · Toba · Mie Prefecture',
  title: 'Ise Grand Shrine & Toba Pearl Divers',
  description: "Journey to Mie Prefecture for Japan's most sacred Shinto shrine — Ise Jingu — then to the coastal town of Toba to meet ama pearl divers and feast on the freshest seafood in the country.",
  timeBlocks: [
    {
      label: 'Morning',
      activities: [
        {
          title: 'Ise Grand Shrine (Ise Jingu)',
          description: "Japan's holiest shrine, rebuilt every 20 years for over 1,300 years. The Inner Shrine (Naiku) is set deep within an ancient cypress forest — the spiritual atmosphere is overwhelming. This is the heart of Japanese Shinto.",
          details: [
            '⛩️ Visit the Inner Shrine (Naiku) — the most important of the 125 shrines',
            '🌲 Walk across the Uji Bridge into the sacred forest — the air changes',
            '🙏 Photography is restricted near the main hall — respect the sacred space',
            '📿 The shrine has been rebuilt every 20 years since 690 AD — next rebuild: 2033'
          ]
        }
      ],
      meals: [
        {
          type: '☕ Lunch',
          name: 'Okage Yokocho',
          description: "Traditional shopping street near the Inner Shrine recreating Edo-period architecture. Famous for Ise udon (thick, soft noodles in dark sauce) and akafuku mochi (sweet rice cakes). A foodie paradise.",
          meta: '💰 ¥800-1,500pp · 📍 Adjacent to Naiku shrine · Many stalls and restaurants'
        }
      ]
    },
    {
      label: 'Afternoon',
      activities: [
        {
          title: 'Toba — Mikimoto Pearl Island & Ama Divers',
          description: "Head to Toba to visit Mikimoto Pearl Island — where cultured pearl farming was invented. Watch ama (women free divers) demonstrate their ancient diving technique, and learn about Japan's fascinating pearl industry.",
          details: [
            '🦪 Mikimoto Pearl Island — museum + live ama diving demonstrations',
            '🤿 Ama divers have been harvesting seafood for 2,000+ years',
            '💎 The pearl museum shows how cultured pearls are made — fascinating process'
          ]
        },
        {
          title: 'Meoto Iwa (Married Couple Rocks)',
          description: "Visit the sacred Meoto Iwa — two rocks in the ocean connected by a shimenawa rope, representing the union of the creator gods. One of Japan's most iconic spiritual sights.",
          details: [
            '📸 Best photographed at sunrise, but impressive any time',
            '⛩️ Futami Okitama Shrine nearby has adorable frog statues everywhere'
          ]
        }
      ]
    },
    {
      label: 'Evening',
      activities: [
        {
          title: 'Toba Seafood Feast',
          description: "Toba is one of Japan's premier seafood destinations. The waters here produce incredible Ise-ebi (spiny lobster), oysters, abalone, and turban shells. Treat the group to an unforgettable seafood dinner.",
          details: [
            '🦞 Ise-ebi season peaks in fall, but the local seafood is outstanding year-round',
            '🦪 Toba oysters are farmed in the nutrient-rich bay — plump and sweet',
            '🏨 Many ryokans in Toba include spectacular seafood kaiseki dinners'
          ]
        }
      ],
      meals: [
        {
          type: '🍷 Dinner',
          name: 'Ama Hut Seafood BBQ (Osatsu Kamado)',
          description: "Eat grilled seafood over an open fire, served in a seaside hut by women dressed as traditional ama divers. Abalone, turban shells, oysters, and clams cooked right in front of you — absolutely unique.",
          meta: '💰 ¥3,000-5,000pp · 📍 Osatsu area, Toba · Reservations required'
        }
      ]
    }
  ],
  mapPins: [
    { lat: 34.4550, lng: 136.7256, label: 'Ise Grand Shrine (Naiku)', num: 1, cat: 'attraction', desc: "Japan's holiest Shinto shrine — 1,300 years old" },
    { lat: 34.4533, lng: 136.7280, label: 'Okage Yokocho', num: 2, cat: 'food', desc: 'Edo-style food street — Ise udon & akafuku mochi' },
    { lat: 34.4809, lng: 136.8422, label: 'Mikimoto Pearl Island', num: 3, cat: 'attraction', desc: 'Birthplace of cultured pearl farming' },
    { lat: 34.5066, lng: 136.7932, label: 'Meoto Iwa (Married Rocks)', num: 4, cat: 'attraction', desc: 'Sacred rocks connected by shimenawa rope' },
    { lat: 34.4820, lng: 136.8430, label: 'Toba Bay', num: 5, cat: 'attraction', desc: 'Pearl cultivation bay with ama diving' },
    { lat: 34.4500, lng: 136.8500, label: 'Osatsu Ama Hut', num: 6, cat: 'food', desc: 'Grilled seafood served by traditional divers' }
  ]
};


const day12 = {
  num: 12,
  date: '2029-05-25',
  neighborhoods: 'Osaka · Dotonbori · Shinsekai · Namba',
  title: 'Osaka — The Kitchen of Japan',
  description: "Welcome to Osaka — Japan's street food capital, comedy hub, and nightlife powerhouse. Spend the day eating your way through Dotonbori, explore the retro charm of Shinsekai, and end with Osaka's legendary nightlife.",
  timeBlocks: [
    {
      label: 'Morning',
      activities: [
        {
          title: 'Travel to Osaka & Osaka Castle',
          description: "Take the train from Toba/Ise to Osaka (about 2 hours). Drop your bags and head to Osaka Castle — the dramatic five-story tower sits atop a stone-walled hilltop surrounded by moats and parkland.",
          details: [
            '🏯 Osaka Castle is a reconstruction but the museum inside is worthwhile',
            '🌳 The surrounding Nishinomaru Garden is beautiful in late spring',
            '📸 Best photo angles from across the moat on the south side'
          ]
        }
      ]
    },
    {
      label: 'Afternoon',
      activities: [
        {
          title: 'Dotonbori Street Food Crawl',
          description: "Osaka's motto is kuidaore — 'eat till you drop.' Dotonbori is ground zero for this philosophy. Walk the canal-side street and eat everything: takoyaki, okonomiyaki, gyoza, kushikatsu, and more.",
          details: [
            '🐙 Takoyaki (octopus balls) — try Creo-Ru or Kukuru for the best',
            '🥞 Okonomiyaki (savory pancake) — Mizuno is legendary, expect a line',
            '🍢 Kushikatsu (deep-fried skewers) — Daruma is the iconic spot',
            '📸 The Glico Running Man sign is Osaka\'s most famous photo spot'
          ]
        },
        {
          title: 'Shinsekai District',
          description: "Walk south to Shinsekai — Osaka's retro entertainment district. Built in 1912 to blend Paris and New York, it now has a wonderfully faded charm. The Tsutenkaku Tower overlooks streets lined with kushikatsu shops and game parlors.",
          details: [
            '🗼 Tsutenkaku Tower — modest views but great retro vibes',
            '🍢 Shinsekai is THE kushikatsu district — try Jan Jan Yokocho alley',
            '🎰 Retro game centers and pachinko parlors everywhere'
          ]
        }
      ],
      meals: [
        {
          type: '☕ Lunch',
          name: 'Dotonbori Street Food',
          description: 'Skip the sit-down and graze! Takoyaki from Creo-Ru, gyoza from Chao Chao, and kushikatsu from Daruma. Budget about ¥2,000-3,000 total for a full street food lunch.',
          meta: '💰 ¥2,000-3,000pp · 📍 Dotonbori · Walk and eat'
        }
      ]
    },
    {
      label: 'Night',
      activities: [
        {
          title: 'Namba & Osaka Nightlife',
          description: "Osaka's nightlife rivals Tokyo but with a friendlier, more outgoing energy. Start with drinks on the Dotonbori canal, then head to the bars around Namba and Shinsaibashi. Osakans are famous for their warmth and humor.",
          details: [
            '🍸 Bar Nayuta — intimate cocktail bar with legendary bartender',
            '🎤 Karaoke is a MUST in Osaka — try Jankara for cheap group rooms',
            '🎶 AMMONA in Shinsaibashi for clubbing till dawn',
            '🍺 Ura-Namba (back streets of Namba) has excellent standing bars and izakayas'
          ]
        }
      ],
      meals: [
        {
          type: '🍺 Dinner',
          name: 'Toyo (Standing Sashimi Bar)',
          description: "Legendary standing sushi/sashimi bar in Kuromon Market area. The tuna is butchered right in front of you and served on the spot. Casual, chaotic, and absolutely delicious. Cash only.",
          meta: '💰 ¥2,000-4,000pp · 📍 Near Kuromon Market, Namba · No reservations, stand and eat'
        }
      ]
    }
  ],
  mapPins: [
    { lat: 34.6873, lng: 135.5262, label: 'Osaka Castle', num: 1, cat: 'attraction', desc: 'Dramatic five-story castle on a hilltop' },
    { lat: 34.6687, lng: 135.5012, label: 'Dotonbori', num: 2, cat: 'food', desc: "Osaka's iconic street food canal district" },
    { lat: 34.6688, lng: 135.5015, label: 'Glico Running Man', num: 3, cat: 'attraction', desc: "Osaka's most famous neon sign" },
    { lat: 34.6523, lng: 135.5064, label: 'Shinsekai', num: 4, cat: 'attraction', desc: 'Retro entertainment district with Tsutenkaku Tower' },
    { lat: 34.6654, lng: 135.5058, label: 'Toyo Sashimi Bar', num: 5, cat: 'food', desc: 'Legendary standing sushi near Kuromon Market' },
    { lat: 34.6690, lng: 135.5005, label: 'Namba Nightlife', num: 6, cat: 'nightlife', desc: "Osaka's warm and wild nightlife scene" }
  ]
};

const day13 = {
  num: 13,
  date: '2029-05-26',
  neighborhoods: 'Kyoto · Fushimi Inari · Arashiyama · Gion',
  title: 'Kyoto — Temples, Bamboo & Geisha District',
  description: "Day trip to Kyoto — just 15 minutes from Osaka by Shinkansen. Experience the jaw-dropping 10,000 vermillion torii gates of Fushimi Inari, the ethereal bamboo groves of Arashiyama, and the mysterious geisha district of Gion.",
  timeBlocks: [
    {
      label: 'Morning',
      activities: [
        {
          title: 'Fushimi Inari Shrine',
          description: "Arrive at dawn for the most magical experience in all of Japan — thousands of bright orange torii gates snaking up a mountainside through dense forest. The full hike to the summit takes 2 hours, but even 30 minutes is unforgettable.",
          details: [
            '⛩️ Start EARLY (before 7am) to have the gates almost to yourself',
            '🥾 Full summit hike: 4km, 2 hours. The mini summit at 30 min is also rewarding.',
            '🦊 Fox statues throughout — the fox is Inari\'s messenger',
            '📸 The dense tunnel sections are the most photogenic — fewer people = better shots'
          ]
        }
      ],
      meals: [
        {
          type: '☕ Breakfast',
          name: 'Vermillion Café',
          description: 'Charming café right at the base of Fushimi Inari, perfect for post-hike coffee and pastries with a view of the shrine entrance.',
          meta: '💰 ¥500-1,000pp · 📍 Next to Fushimi Inari station · Opens early'
        }
      ]
    },
    {
      label: 'Afternoon',
      activities: [
        {
          title: 'Arashiyama Bamboo Grove',
          description: "Walk through the towering bamboo forest of Arashiyama — the light filtering through thousands of bamboo stalks creates an otherworldly atmosphere. Continue to the scenic Togetsukyo Bridge spanning the Katsura River.",
          details: [
            '🎋 Arrive before 9am or after 4pm for fewer crowds',
            '🐒 Iwatayama Monkey Park is a 20-min climb — wild macaques with city views',
            '🌉 Togetsukyo Bridge is especially beautiful with mountains in the background'
          ]
        },
        {
          title: 'Kinkaku-ji (Golden Pavilion)',
          description: "One of Kyoto's most iconic sights — a three-story pavilion covered in gold leaf reflecting perfectly in the mirror pond. The surrounding strolling garden is immaculate.",
          details: [
            '✨ The reflection in the pond is the money shot — arrive when it\'s calm',
            '💰 ¥500 admission · Your ticket is a beautiful calligraphic charm',
            '🍵 Grab matcha and wagashi at the tea garden inside the grounds'
          ]
        }
      ],
      meals: [
        {
          type: '☕ Lunch',
          name: 'Arashiyama Yoshimura Soba',
          description: 'Handmade soba noodles with a view of the Togetsukyo Bridge and Katsura River. The tempura soba set is excellent. Tatami seating with river views.',
          meta: '💰 ¥1,200-1,800pp · 📍 Arashiyama · River-view seating'
        }
      ]
    },
    {
      label: 'Evening',
      activities: [
        {
          title: 'Gion District — Geisha Quarter',
          description: "Wander the atmospheric streets of Gion as dusk falls. The wooden machiya townhouses, stone-paved lanes, and soft lantern light create an enchanting atmosphere. You might spot a maiko (apprentice geisha) hurrying to an engagement.",
          details: [
            '👘 Hanami-koji is the main geisha street — respect their privacy, no chasing for photos',
            '🏮 Shirakawa canal with its weeping willows and stone bridges is magical at dusk',
            '⛩️ Yasaka Shrine at the eastern end is beautiful lit up at night',
            '🍵 Consider a traditional tea ceremony experience in Gion — about ¥2,000-4,000pp'
          ]
        }
      ],
      meals: [
        {
          type: '🍷 Dinner',
          name: 'Pontocho Alley Dining',
          description: "Narrow alley running along the Kamogawa River, packed with restaurants from high-end kaiseki to casual izakayas. In summer, restaurants extend seating onto kawadoko (riverside platforms). Choose any spot — they're all atmospheric.",
          meta: '💰 ¥2,500-5,000pp · 📍 Pontocho, Kyoto · Riverfront spots book up fast'
        }
      ],
      tips: [
        { type: 'tip', text: 'Kyoto is a day trip from Osaka — just 15 min by Shinkansen or 30 min by regular train. Return to your Osaka hotel for the night.' }
      ]
    }
  ],
  mapPins: [
    { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari Shrine', num: 1, cat: 'attraction', desc: '10,000 vermillion torii gates up a mountain' },
    { lat: 35.0175, lng: 135.6716, label: 'Arashiyama Bamboo Grove', num: 2, cat: 'attraction', desc: 'Towering bamboo forest — ethereal atmosphere' },
    { lat: 35.0127, lng: 135.6779, label: 'Togetsukyo Bridge', num: 3, cat: 'attraction', desc: 'Scenic bridge over the Katsura River' },
    { lat: 35.0394, lng: 135.7292, label: 'Kinkaku-ji (Golden Pavilion)', num: 4, cat: 'attraction', desc: 'Gold-leaf pavilion with mirror pond reflection' },
    { lat: 35.0037, lng: 135.7746, label: 'Gion District', num: 5, cat: 'attraction', desc: 'Historic geisha quarter with lantern-lit streets' },
    { lat: 35.0050, lng: 135.7700, label: 'Pontocho Alley', num: 6, cat: 'food', desc: 'Atmospheric riverside dining alley' }
  ]
};


const day14 = {
  num: 14,
  date: '2029-05-27',
  neighborhoods: 'Nara · Southern Kyoto Temples',
  title: 'Nara\'s Ancient Deer & Kyoto\'s Hidden Temples',
  description: "Morning with Nara's famously friendly deer and the colossal Great Buddha, then afternoon exploring Kyoto's lesser-known southern temples — Tofuku-ji's zen gardens and the stunning Byodo-in (the temple on the ¥10 coin).",
  timeBlocks: [
    {
      label: 'Morning',
      activities: [
        {
          title: 'Nara Park & Todai-ji Temple',
          description: "Train to Nara (45 min from Osaka) and enter Nara Park — home to 1,200 free-roaming deer considered sacred messengers. They'll bow to you for deer crackers! Then visit Todai-ji — the enormous wooden temple housing a 15-meter bronze Buddha.",
          details: [
            '🦌 Buy shika senbei (deer crackers, ¥200) and the deer will bow to you',
            '🙏 Todai-ji\'s Great Buddha Hall is the world\'s largest wooden building',
            '📸 The deer are adorable but can be pushy — hide your crackers!',
            '⏰ Arrive early to beat tour groups — the deer are friendliest in the morning'
          ]
        },
        {
          title: 'Kasuga Taisha Shrine',
          description: "Walk through Nara Park's ancient forest to Kasuga Grand Shrine — famous for its 3,000 stone and bronze lanterns. The approach through the primeval forest with deer grazing alongside is enchanting.",
          details: [
            '🏮 3,000 lanterns line the paths and hang in the corridors',
            '🌳 The surrounding Kasugayama Primeval Forest is a UNESCO site',
            '⛩️ ¥500 for the inner sanctuary — the lantern-filled corridors are worth it'
          ]
        }
      ],
      meals: [
        {
          type: '☕ Lunch',
          name: 'Kakinoha Sushi (Persimmon Leaf Sushi)',
          description: 'Nara\'s famous local specialty — pressed sushi wrapped in fragrant persimmon leaves. Try Tanaka at Kintetsu Nara Station or any shop along the approach to Todai-ji.',
          meta: '💰 ¥800-1,200pp · 📍 Near Todai-ji or Kintetsu Nara Station'
        }
      ]
    },
    {
      label: 'Afternoon',
      activities: [
        {
          title: 'Tofuku-ji Temple',
          description: "Head to Kyoto's Tofuku-ji — one of the great Zen temples, famous for its stunning gardens. The Hojo garden (designed in 1939) is a masterpiece of modern zen garden design with moss, stone, and raked gravel.",
          details: [
            '🌿 The moss and checkered stone garden is unlike anything else in Kyoto',
            '🍁 Famous for autumn leaves, but the gardens are beautiful year-round',
            '📸 The Tsutenkyo (bridge) corridor offers unique elevated garden views'
          ]
        }
      ]
    },
    {
      label: 'Evening',
      activities: [
        {
          title: 'Return to Osaka & Ura-Namba',
          description: "Head back to Osaka for your last night in the city. Explore Ura-Namba (back streets of Namba) — a maze of tiny standing bars, yakitori joints, and local izakayas where Osakans actually hang out.",
          details: [
            '🍺 Ura-Namba standing bars — ¥300-500 beers and cheap snacks',
            '🎤 One last karaoke session with the group — Jankara or Big Echo',
            '🌙 Take a final walk along the Dotonbori canal at night for the neon reflections'
          ]
        }
      ],
      meals: [
        {
          type: '🍺 Dinner',
          name: 'Ajinoya Okonomiyaki',
          description: 'One of Osaka\'s best okonomiyaki restaurants — watch them make your savory pancake on the teppan right in front of you. The pork and squid mix is incredible. Perfect casual group dinner.',
          meta: '💰 ¥1,200-2,000pp · 📍 Namba · May have a queue but moves fast'
        }
      ]
    }
  ],
  mapPins: [
    { lat: 34.6890, lng: 135.8398, label: 'Nara Park', num: 1, cat: 'attraction', desc: '1,200 free-roaming sacred deer' },
    { lat: 34.6890, lng: 135.8400, label: 'Todai-ji Temple', num: 2, cat: 'attraction', desc: 'World\'s largest wooden building with 15m Buddha' },
    { lat: 34.6811, lng: 135.8499, label: 'Kasuga Taisha Shrine', num: 3, cat: 'attraction', desc: '3,000 stone and bronze lanterns' },
    { lat: 34.9765, lng: 135.7747, label: 'Tofuku-ji Temple', num: 4, cat: 'attraction', desc: 'Zen temple with masterpiece modern gardens' },
    { lat: 34.6660, lng: 135.5020, label: 'Ura-Namba', num: 5, cat: 'nightlife', desc: 'Back-street standing bars & local izakayas' },
    { lat: 34.6685, lng: 135.5030, label: 'Ajinoya Okonomiyaki', num: 6, cat: 'food', desc: 'Top-tier Osaka okonomiyaki on the teppan' }
  ]
};

const day15 = {
  num: 15,
  date: '2029-05-28',
  neighborhoods: 'Hiroshima · Miyajima Island',
  title: 'Hiroshima — Peace, History & Miyajima\'s Floating Torii',
  description: "A powerful and moving day trip from Osaka. Visit the Hiroshima Peace Memorial and Museum, then ferry to Miyajima Island to see the iconic floating torii gate of Itsukushima Shrine — one of Japan's most beautiful sights.",
  timeBlocks: [
    {
      label: 'Morning',
      activities: [
        {
          title: 'Shinkansen to Hiroshima & Peace Memorial Park',
          description: "Take the early Shinkansen from Shin-Osaka to Hiroshima (80 minutes). Walk to the Peace Memorial Park — a solemn, beautifully designed park centered on the A-Bomb Dome, the only structure left standing near the bomb's hypocenter.",
          details: [
            '🕊️ The A-Bomb Dome is a UNESCO World Heritage Site — preserved as it stood after the blast',
            '🕯️ The Children\'s Peace Monument with its paper cranes is deeply moving',
            '🏛️ The Peace Memorial Museum was renovated in 2019 — deeply impactful exhibits',
            '⏰ Museum opens at 8:30am — arrive early, allow 1-1.5 hours'
          ]
        }
      ]
    },
    {
      label: 'Afternoon',
      activities: [
        {
          title: 'Miyajima Island & Itsukushima Shrine',
          description: "Ferry from Hiroshima to Miyajima Island (about 1 hour total including tram to port). The iconic floating torii gate of Itsukushima Shrine appears to hover over the water at high tide — one of Japan's Three Most Scenic Views.",
          details: [
            '⛩️ The vermillion torii gate \"floats\" at high tide and is walkable at low tide — check tide times!',
            '🦌 Wild deer roam Miyajima too — smaller and more relaxed than Nara\'s',
            '🏯 Explore Senjokaku (Hall of 1,000 Tatami Mats) and the five-story pagoda',
            '🚡 Miyajima Ropeway to Mt Misen summit for panoramic inland sea views (if time allows)'
          ]
        }
      ],
      meals: [
        {
          type: '☕ Lunch',
          name: 'Hiroshima Okonomiyaki',
          description: "Hiroshima-style okonomiyaki is layered (not mixed like Osaka's) with noodles, cabbage, egg, and toppings stacked on the griddle. Try Nagata-ya or Hassei near the Peace Park for the best.",
          meta: '💰 ¥900-1,500pp · 📍 Near Peace Park, Hiroshima · Nagata-ya has a line — worth it'
        },
        {
          type: '🍺 Snack',
          name: 'Miyajima Grilled Oysters & Momiji Manju',
          description: 'Miyajima is famous for two things: massive grilled oysters from the Seto Inland Sea (¥200-400 each) and momiji manju — maple-leaf-shaped cakes filled with sweet bean paste, custard, or chocolate.',
          meta: '💰 ¥500-1,000pp · 📍 Miyajima shopping street'
        }
      ]
    },
    {
      label: 'Evening',
      activities: [
        {
          title: 'Return to Osaka',
          description: "Take the Shinkansen back to Shin-Osaka (80 min). Reflect on a powerful, moving day. If you have energy, grab a nightcap in Namba or near your hotel.",
          details: [
            '🚅 Last Shinkansen back is around 9pm — don\'t miss it!',
            '🍺 Grab ekiben (station bento) and a beer for the ride back — a Japanese train tradition'
          ]
        }
      ],
      meals: [
        {
          type: '🍷 Dinner',
          name: 'Ekiben on the Shinkansen',
          description: 'Buy a Hiroshima-specialty ekiben (station bento) at Hiroshima Station for the ride back. The anagomeshi (grilled conger eel on rice) bento is a Hiroshima classic.',
          meta: '💰 ¥1,000-1,500pp · 📍 Hiroshima Station shops'
        }
      ],
      tips: [
        { type: 'tip', text: 'This is a long day but absolutely doable as a day trip. Leave Osaka by 7am Shinkansen, spend morning in Hiroshima, afternoon on Miyajima, return by 9pm. JR Pass covers everything.' }
      ]
    }
  ],
  mapPins: [
    { lat: 34.3955, lng: 132.4536, label: 'A-Bomb Dome', num: 1, cat: 'attraction', desc: 'UNESCO site — preserved blast structure' },
    { lat: 34.3915, lng: 132.4531, label: 'Peace Memorial Museum', num: 2, cat: 'attraction', desc: 'Deeply impactful museum on atomic bombing' },
    { lat: 34.3932, lng: 132.4534, label: 'Children\'s Peace Monument', num: 3, cat: 'attraction', desc: 'Memorial with paper cranes' },
    { lat: 34.2961, lng: 132.3198, label: 'Itsukushima Floating Torii', num: 4, cat: 'attraction', desc: 'Iconic floating vermillion gate' },
    { lat: 34.2970, lng: 132.3195, label: 'Itsukushima Shrine', num: 5, cat: 'attraction', desc: 'Seaside shrine — one of Japan\'s Three Views' },
    { lat: 34.3962, lng: 132.4590, label: 'Nagata-ya Okonomiyaki', num: 6, cat: 'food', desc: 'Best Hiroshima-style layered okonomiyaki' }
  ]
};

const day16 = {
  num: 16,
  date: '2029-05-29',
  neighborhoods: 'Osaka · Kuromon Market · Umeda · Departure',
  title: 'Final Day — Osaka\'s Last Bites & Sayonara',
  description: "Your final day in Japan. Make the most of the morning with Osaka's incredible Kuromon Market, explore the skyline from Umeda Sky Building, pick up last-minute souvenirs, and say sayonara to an unforgettable 16-day adventure.",
  timeBlocks: [
    {
      label: 'Morning',
      activities: [
        {
          title: 'Kuromon Market — Osaka\'s Kitchen',
          description: "Osaka's 190-year-old \"Kitchen\" — a covered market stretching 580 meters with 150+ stalls selling the freshest seafood, fruit, and street food. This is your breakfast and lunch in one glorious grazing session.",
          details: [
            '🐟 Giant grilled scallops, king crab legs, uni (sea urchin), and fatty tuna sashimi — all eaten standing',
            '🍓 Japanese strawberries and perfectly cubed fruit — worth the splurge',
            '🐡 Some stalls serve fugu (pufferfish) if you\'re feeling adventurous',
            '⏰ Stalls open around 9am — busiest 10am-noon'
          ]
        }
      ],
      meals: [
        {
          type: '☕ Breakfast/Brunch',
          name: 'Kuromon Market Grazing',
          description: 'This IS your meal — graze through the market eating fresh sashimi, grilled seafood, tamagoyaki, and seasonal fruit. Budget ¥3,000-5,000 for a full market breakfast.',
          meta: '💰 ¥3,000-5,000pp · 📍 Kuromon Market, Namba · Best 9am-noon'
        }
      ]
    },
    {
      label: 'Afternoon',
      activities: [
        {
          title: 'Umeda Sky Building & Souvenir Shopping',
          description: "Head to Umeda for the futuristic Sky Building — two towers connected by a floating garden observatory at 173m. The escalator through the open air between towers is thrilling. Then hit the underground shopping streets for last-minute souvenirs.",
          details: [
            '🏙️ The Floating Garden Observatory has 360° open-air views',
            '🛍️ Buy Japanese snack boxes, Kit Kat flavors, and matcha sweets at Don Quijote or department store basements (depachika)',
            '📦 Osaka Station has excellent souvenir shops — 551 Horai\'s pork buns are the classic Osaka omiyage',
            '🧳 Pack or ship — Japan Post and Yamato offer affordable international shipping'
          ]
        }
      ]
    },
    {
      label: 'Evening',
      activities: [
        {
          title: 'Final Walk & Departure',
          description: "Take one last stroll through your favorite Osaka neighborhood. If departing from Kansai International Airport (KIX), take the Nankai Rapit express train from Namba (38 min) or JR Haruka from Tennoji/Shin-Osaka.",
          details: [
            '✈️ KIX: Nankai Rapit from Namba (38 min) or JR Haruka from Shin-Osaka (50 min)',
            '✈️ ITM (Itami/Osaka domestic): Airport bus from major stations',
            '🎌 Sayonara, Japan! You\'ve covered 16 incredible days across the entire country'
          ]
        }
      ],
      meals: [
        {
          type: '🍺 Lunch/Farewell',
          name: '551 Horai Butaman (Pork Buns)',
          description: "Osaka's most beloved takeaway — juicy steamed pork buns from 551 Horai. Every Osakan knows the smell. Grab a box at any station shop for the journey to the airport.",
          meta: '💰 ¥500-800 for a box · 📍 Every major station · THE Osaka souvenir'
        }
      ],
      tips: [
        { type: 'tip', text: 'Tax-free shopping: spend ¥5,000+ at participating stores and show your passport for 10% tax refund. Department stores have dedicated tax-free counters.' }
      ]
    }
  ],
  mapPins: [
    { lat: 34.6690, lng: 135.5075, label: 'Kuromon Market', num: 1, cat: 'food', desc: "Osaka's 190-year-old kitchen — 150+ stalls" },
    { lat: 34.7055, lng: 135.4906, label: 'Umeda Sky Building', num: 2, cat: 'attraction', desc: 'Floating garden observatory at 173m' },
    { lat: 34.7024, lng: 135.4959, label: 'Osaka/Umeda Station', num: 3, cat: 'transport', desc: 'Major station with souvenir shops' },
    { lat: 34.6647, lng: 135.5020, label: '551 Horai (Namba)', num: 4, cat: 'food', desc: "Osaka's famous steamed pork buns" },
    { lat: 34.4350, lng: 135.2440, label: 'Kansai International Airport', num: 5, cat: 'transport', desc: 'International departure — KIX' }
  ]
};


const itineraryData = {
  destination: 'Japan',
  countryEmoji: '🇯🇵',
  title: 'The Ultimate Japan Adventure: Tokyo to Hiroshima',
  subtitle: '16 days of neon nights, sacred temples, coastal hot springs & unforgettable feasts for your crew',
  description: "This epic 16-day journey spans the full breadth of Japan — from Tokyo's electric neighborhoods and Pokémon theme parks to the serene onsen of the Izu Peninsula, the artistic wonder of Ghibli Park, sacred shrines of Ise, street food legends of Osaka, ancient temples of Kyoto and Nara, and the powerful memorials of Hiroshima. Designed for a group of five or more who crave adventure by day and nightlife after dark, with casual dining woven throughout. Late May brings warm weather, blooming hydrangeas, and the very edge of rainy season — pack a light rain jacket and your sense of wonder.",
  duration: '16 nights',
  dates: 'May 14 – May 30, 2029',
  budget: '$$–$$$',
  pace: 'Moderate',
  bestFor: 'Groups & Friends',
  highlights: [
    'Shibuya Crossing at night & Golden Gai bar-hopping in Shinjuku',
    'PokéPark KANTO at Yomiuriland — full day of Pokémon immersion',
    "Ghibli Park in Nagoya — walk through Miyazaki's worlds",
    'Izu Peninsula onsen & Jogasaki Coast cliff hiking',
    'Mt Fuji views from Kawaguchiko with lakeside cycling',
    "Ise Grand Shrine & Ama pearl diver huts in Toba",
    'Osaka street food crawl — takoyaki, okonomiyaki & kushikatsu',
    "Fushimi Inari's 10,000 torii gates at dawn in Kyoto",
    "Nara's friendly deer & ancient Great Buddha",
    "Hiroshima Peace Memorial & Miyajima Island's floating torii"
  ],

  essentials: [
    { title: '🚅 Japan Rail Pass', text: 'A 14 or 21-day JR Pass is essential for this trip. It covers bullet trains (Shinkansen) between Tokyo, Nagoya, Osaka, Kyoto, and Hiroshima, plus many local JR lines. Activate it on Day 8 when you leave Tokyo — use IC cards (Suica/Pasmo) for Tokyo metro.' },
    { title: '🌧️ Late May Weather', text: 'Expect 20-28°C across Japan. Late May is the very start of tsuyu (rainy season) in western Japan — Osaka and Kyoto may see afternoon showers. Pack a compact umbrella and light rain jacket. Tokyo will be warm and pleasant.' },
    { title: '💴 Budget Tips', text: "Konbini (convenience stores) like 7-Eleven and Lawson have incredible cheap meals — onigiri, bento, sandwiches. Lunch sets at restaurants are 30-50% cheaper than dinner. Many temples and shrines are free. Group izakaya courses offer great value for 5+." },
    { title: '📱 Staying Connected', text: "Rent a pocket WiFi at the airport or get eSIMs for everyone. Coverage is excellent nationwide. Download the Navitime or Google Maps transit app — Japan's train system is complex but these make it easy." },
    { title: '🎫 Book Ahead', text: 'Ghibli Park and PokéPark KANTO require advance tickets (often months ahead). Book Ghibli Park via Boo-Woo Ticket or Lawson. PokéPark tickets via the official app. Some popular restaurants need reservations too.' }
  ],

  days: [day1, day2, day3, day4, day5, day6, day7, day8, day9, day10, day11, day12, day13, day14, day15, day16],

  budgetTable: [
    { category: 'Accommodation', budget: '¥5,000-8,000/night', midrange: '¥10,000-20,000/night', luxury: '¥25,000-50,000/night' },
    { category: 'Meals (per person)', budget: '¥2,000-3,500/day', midrange: '¥4,000-7,000/day', luxury: '¥8,000-15,000/day' },
    { category: 'Transport (JR Pass)', budget: '¥50,000 (14-day)', midrange: '¥50,000 + IC card', luxury: '¥70,000 (Green Car)' },
    { category: 'Activities', budget: '¥1,000-3,000/day', midrange: '¥3,000-6,000/day', luxury: '¥5,000-15,000/day' },
    { category: 'Nightlife', budget: '¥2,000-4,000/night', midrange: '¥4,000-8,000/night', luxury: '¥8,000-20,000/night' },
    { category: '16-Day Total (per person)', budget: '¥250,000-400,000', midrange: '¥400,000-700,000', luxury: '¥700,000-1,200,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Tokyo Narita (NRT) or Haneda (HND) — Haneda is closer to the city', 'Depart from Osaka Kansai (KIX) for a one-way route — no backtracking', 'Book open-jaw flights (into Tokyo, out of Osaka) to save time and money'] },
    { title: '🏨 Where to Stay', items: ['Tokyo: Shinjuku or Shibuya for nightlife access and train connections', 'Izu: Book a ryokan with onsen for the full experience', 'Kawaguchiko: Lakeside hotel with Fuji views', 'Nagoya: Near Nagoya Station for easy Shinkansen access', 'Osaka: Namba or Shinsaibashi for food and nightlife'] },
    { title: '🌡️ Weather', items: ['Mid-May: 20-26°C, mostly sunny with occasional rain', 'Late May: 22-28°C, tsuyu (rainy season) may begin in western Japan', 'Humidity increases throughout May — carry a handkerchief and stay hydrated', 'UV is strong — sunscreen and hats recommended for outdoor days'] },
    { title: '💳 Money & Tipping', items: ['Japan is increasingly cashless but carry some yen — small shops and shrines are cash-only', 'NO TIPPING in Japan — it can actually be considered rude', '7-Eleven and Japan Post ATMs accept international cards', 'Tax-free shopping at ¥5,000+ — show passport at participating stores'] },
    { title: '📱 Etiquette Tips', items: ['Remove shoes when entering temples, ryokans, and many restaurants (look for the raised floor)', 'No eating or drinking while walking (except festival areas)', 'Phones on silent (manner mode) on public transport — no calls', 'Bow slightly when greeting — it goes a long way', 'Queue patiently — Japan has amazing queue culture'] }
  ]
};

// Run fulfillment
try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
