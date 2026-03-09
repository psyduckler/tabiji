const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772481601812_ul6yqi',
  email: 'paulhblasjr@gmail.com',
  destination: 'Tokyo, Osaka, Kyoto & Nara, Japan',
  startDate: '2026-05-15',
  endDate: '2026-05-24',
  groupSize: '5+',
  requests: 'NO PORK, NO GUNDAM. 3 adults, 2 children (ages 2 and 3). Family-friendly pace.'
};

const itineraryData = {
  destination: 'Tokyo, Osaka, Kyoto & Nara',
  countryEmoji: '🇯🇵',
  title: 'Japan with Little Ones — Tokyo to Kansai',
  subtitle: '10 days across Tokyo, Osaka, Kyoto & Nara for a family of 5 with toddlers',
  description: "A carefully paced family adventure through Japan's greatest cities — designed for two toddlers, three adults, and a whole lot of character cafés. Tokyo's electric energy meets Kyoto's ancient calm, with Osaka as your Kansai base camp. Every day is built around your specific must-visit spots, grouped by neighborhood to minimize transit with little legs. Stroller-friendly routes, nap-time breaks, and zero pork — guaranteed.",
  duration: '10 days / 9 nights',
  dates: 'May 15 – May 24, 2026',
  budget: '$$–$$$',
  pace: 'Family-Friendly (built-in rest breaks)',
  bestFor: 'Families with Toddlers',
  highlights: [
    'teamLab Planets — an immersive sensory wonderland kids will lose their minds over',
    'Pokémon Centers, Kirby Café, and Pikachu Sweets — character overload in the best way',
    'Fushimi Inari Taisha — the iconic red gates, stroller-friendly on the lower paths',
    'Nara Park — toddlers feeding friendly deer (with supervision!)',
    'Arashiyama Bamboo Forest & Monkey Park — nature meets adventure',
    'Osaka\'s Dotonbori at night — glowing signs, street food, pure energy'
  ],

  essentials: [
    { title: '🚅 Getting Between Cities', text: 'Activate a 7-Day Japan Rail Pass on May 18 (covering your last Tokyo day through all Kansai travel). Tokyo to Osaka is ~2.5 hours on the Shinkansen. Reserve seats in advance — Green Car is worth it with toddlers for extra space and quiet. IC cards (Suica/PASMO) for local trains and convenience stores.' },
    { title: '👶 Traveling with Toddlers', text: 'Japan is incredibly toddler-friendly. Most train stations have elevators, department stores have nursing rooms (赤ちゃん休憩室), and convenience stores stock diapers and baby food. Bring a lightweight umbrella stroller — it fits on trains and most temples are accessible on main paths. Coin lockers at major stations hold luggage while you explore.' },
    { title: '🚫 No Pork Guide', text: 'Japan\'s cuisine is deeply pork-centric, but halal and pork-free options exist. We\'ve flagged pork-free restaurants throughout. Key phrases: "Buta nashi de onegaishimasu" (no pork please) and "Buta wa taberaremasen" (I can\'t eat pork). Many ramen shops offer chicken (tori) or seafood (gyokai) broth — always confirm. Beef, chicken, and seafood are your best friends.' },
    { title: '🏨 Accommodation Strategy', text: 'Tokyo (May 15-19): Stay in Shinjuku for central access to all neighborhoods. Osaka (May 20-24): Stay near Namba/Shinsaibashi for Dotonbori access and easy day-trip trains. Look for family rooms or adjoining rooms — Japanese hotels often have family-sized rooms with extra futons.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-05-15',
      neighborhoods: 'Shinjuku · Shibuya · Harajuku',
      title: 'Arrival Day — Shinjuku, Shibuya & Harajuku',
      description: "Welcome to Tokyo! After settling in, ease into the city with Shinjuku's iconic streetscapes, the famous Shibuya Crossing, and Harajuku's colorful Takeshita Street. Today is about soaking in the energy without overdoing it — you just flew across the world with two toddlers.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shinjuku Gyoen National Garden',
              description: 'Start gently with one of Tokyo\'s most beautiful parks. The wide lawns and flat paths are perfect for toddlers to run free after a long flight. The greenhouse is a hit with little ones.',
              details: [
                '🌿 ¥500 adults, free for kids under 6',
                '🚶 Completely stroller-friendly on main paths',
                '📸 Stunning Japanese garden, English garden, and French formal garden',
                '⏰ Open until 6pm (last entry 5:30pm)'
              ]
            },
            {
              title: '3D Cat at Cross Shinjuku Vision',
              description: 'Walk to the east exit of Shinjuku Station to see the famous giant 3D calico cat on the curved LED screen above Cross Shinjuku. Kids will be mesmerized.',
              details: [
                '🐱 Free to watch — the cat "wakes up" at various times',
                '📍 Cross Shinjuku Vision building, above Shinjuku Station East Exit',
                '📸 Great photo op — the 3D effect is genuinely impressive'
              ]
            },
            {
              title: 'Shibuya Crossing & Shibuya Sky',
              description: 'Take the train one stop to Shibuya for the world\'s most famous intersection. Then head up to Shibuya Sky for panoramic views of the city from the rooftop observation deck.',
              details: [
                '🏙️ Shibuya Sky — book tickets online in advance (¥2,000 adults, ¥1,000 kids 6+, free under 6)',
                '📍 Shibuya Station — anime fans will recognize this as a JJK reference point',
                '📸 The crossing is best viewed from Shibuya Sky or the Starbucks above'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Jet lag hack: Keep the kids awake until at least 7pm local time. A park visit helps burn energy and reset body clocks. Don\'t fight it if they nap in the stroller though — flexibility is key with toddlers.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Harajuku — Takeshita Street & Yoyogi Park',
              description: 'Stroll through the iconic Takeshita Street for crepes, colorful shops, and sensory overload. If the kids need a breather, duck into Yoyogi Park right next door — it\'s a massive green space perfect for winding down.',
              details: [
                '🍦 Takeshita Street crepes — get the strawberry and cream ones',
                '🌳 Yoyogi Park — free, wide open, stroller paradise',
                '🛍️ KIDDY LAND Harajuku branch for character toys'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'A Happy Pancake Omotesando',
              description: 'Fluffy Japanese soufflé pancakes that melt in your mouth — and toddlers absolutely demolish them. The Omotesando location has a calm atmosphere. No pork on the menu.',
              meta: '💰 $$ · 📍 Omotesando · Kid-friendly'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6852, lng: 139.7100, label: 'Shinjuku Gyoen', num: 1, cat: 'attraction', desc: 'Beautiful park — perfect for jet-lagged toddlers' },
        { lat: 35.6896, lng: 139.7006, label: '3D Cat Cross Shinjuku', num: 2, cat: 'attraction', desc: 'Giant 3D cat LED screen' },
        { lat: 35.6580, lng: 139.7016, label: 'Shibuya Crossing', num: 3, cat: 'attraction', desc: 'World\'s most famous intersection + JJK reference' },
        { lat: 35.6584, lng: 139.7023, label: 'Shibuya Sky', num: 4, cat: 'attraction', desc: 'Rooftop observation deck with 360° views' },
        { lat: 35.6707, lng: 139.7027, label: 'Takeshita Street', num: 5, cat: 'attraction', desc: 'Harajuku\'s colorful pedestrian shopping street' },
        { lat: 35.6717, lng: 139.6949, label: 'Yoyogi Park', num: 6, cat: 'attraction', desc: 'Huge park next to Harajuku' },
        { lat: 35.6652, lng: 139.7098, label: 'A Happy Pancake Omotesando', num: 7, cat: 'food', desc: 'Fluffy soufflé pancakes — toddler heaven' }
      ]
    },
    {
      num: 2,
      date: '2026-05-16',
      neighborhoods: 'Asakusa · Skytree · Sumida',
      title: 'Asakusa, Sensō-ji & Tokyo Skytree',
      description: "Tokyo's historic heart meets its modern skyline. Start at the ancient Sensō-ji temple, explore Nakamise-dori's shops, then head to Tokyo Skytree for views that stretch to Mount Fuji on a clear day. The Sumida area is flat, stroller-friendly, and packed with charm.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sensō-ji Temple & Nakamise-dori',
              description: 'Tokyo\'s oldest temple (built 628 AD) is stunning in the morning light before the crowds. Walk through the massive Kaminarimon gate, browse the Nakamise-dori shopping street, and explore the temple grounds.',
              details: [
                '⛩️ Free entry — the temple grounds are open 24/7',
                '🛍️ Nakamise-dori shops: Asakusa Ichigo-za (strawberry sweets), Ginkado (traditional crafts)',
                '🍓 Ichigo daifuku (strawberry mochi) — find it at stalls along Nakamise-dori',
                '🚶 Flat and stroller-friendly throughout',
                '📸 The five-story pagoda is gorgeous with kids in front'
              ]
            },
            {
              title: 'UNIQLO Asakusa',
              description: 'The massive Asakusa UNIQLO is right near Sensō-ji. Stock up on affordable, comfortable clothes for the trip — their kids\' line is excellent for travel.',
              details: [
                '👕 Great for picking up extra layers, UV protection shirts, and comfy basics',
                '📍 Right on the main street near Sensō-ji'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Ichinoya — Wagyu Steak',
              description: 'Premium wagyu beef in Asakusa — tender, melt-in-your-mouth steak served in a traditional setting. Completely pork-free. Kids can share adult portions or order smaller rice bowl sets.',
              meta: '💰 $$$ · 📍 Asakusa · No pork on menu'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tokyo Skytree & Solamachi',
              description: 'At 634 meters, Skytree is the tallest structure in Japan. The Tembo Deck (350m) offers incredible views, and the shopping complex at its base — Tokyo Solamachi — has a massive Pokémon Center, a studio Ghibli shop, and tons of kid-friendly stores.',
              details: [
                '🗼 Book tickets online to skip the line — ¥2,100 adults, ¥950 ages 4-11, free under 4',
                '🎮 Pokémon Center Skytree Town in the Solamachi mall',
                '📸 On clear days you can see Mount Fuji from the top',
                '👶 Stroller-friendly — elevators to all observation decks'
              ]
            },
            {
              title: 'Oyokogawa Shinsui Park',
              description: 'A lovely canal-side walking path near Skytree with greenery and water features. Perfect for a toddler break — let them splash near the shallow waterways and burn energy on the flat paths.',
              details: [
                '🌊 Free, open public park along the canal',
                '🚶 Flat, paved paths perfect for strollers',
                '🌸 Beautiful with seasonal flowers'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Nap strategy: After Skytree, if the kids are fading, put them in the stroller and walk the peaceful Oyokogawa park. The gentle movement usually does the trick.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Convenience Store Dinner Run',
              description: 'Hear us out — Japanese convenience stores are a genuine food experience. FamilyMart and 7-Eleven have incredible onigiri, chicken karaage, egg sandwiches, fresh fruit, and desserts. Perfect for a low-key evening with tired toddlers back at the hotel.',
              details: [
                '🏪 FamilyMart fried chicken (Famichiki) — no pork, incredibly good',
                '🍙 Onigiri (rice balls) — salmon, tuna, or kelp varieties are pork-free',
                '🍮 Puddings, fruit cups, and matcha desserts galore',
                '💡 Ask for "buta nashi" items if unsure — staff are helpful'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: 'Sensō-ji Temple', num: 1, cat: 'attraction', desc: 'Tokyo\'s oldest temple — stunning Kaminarimon gate' },
        { lat: 35.7120, lng: 139.7960, label: 'Nakamise-dori', num: 2, cat: 'shopping', desc: 'Traditional shopping street — ichigo daifuku & crafts' },
        { lat: 35.7121, lng: 139.7946, label: 'UNIQLO Asakusa', num: 3, cat: 'shopping', desc: 'Massive UNIQLO near Sensō-ji' },
        { lat: 35.7101, lng: 139.8107, label: 'Tokyo Skytree', num: 4, cat: 'attraction', desc: '634m tower — Japan\'s tallest structure' },
        { lat: 35.7063, lng: 139.8136, label: 'Oyokogawa Shinsui Park', num: 5, cat: 'attraction', desc: 'Canal-side park for a toddler break' },
        { lat: 35.7130, lng: 139.7970, label: 'Ichinoya', num: 6, cat: 'food', desc: 'Premium wagyu steak in Asakusa — pork-free' }
      ]
    },
    {
      num: 3,
      date: '2026-05-17',
      neighborhoods: 'Shibuya · Omotesando · Meiji Jingu',
      title: 'Meiji Jingu, Shibuya Shopping & Character Stores',
      description: "A day of contrast — ancient forest shrine in the morning, then Shibuya's buzzing character stores and cafés in the afternoon. This is the anime/character day your family has been waiting for.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Meiji Jingu Shrine',
              description: 'Walk through the towering torii gate into a tranquil forest in the heart of Tokyo. Meiji Jingu is a Shinto shrine surrounded by 170 acres of woodland — it feels like stepping into another world. The wide gravel paths are manageable with strollers.',
              details: [
                '⛩️ Free entry — open sunrise to sunset',
                '🌳 The forest walk from the entrance to the shrine is ~10 minutes',
                '🚶 Main path is wide gravel — stroller-doable but bumpy in spots',
                '📸 The massive wooden torii gate is one of Tokyo\'s most iconic sights'
              ]
            },
            {
              title: 'PEANUTS Cafe Harajuku',
              description: 'A charming Snoopy-themed café near Meiji Jingu with adorable Peanuts latte art, themed desserts, and a gift shop. The calm vibe makes it a great mid-morning stop with kids.',
              details: [
                '🥜 Cute Snoopy latte art and themed treats',
                '📍 Near the Meiji Jingu entrance in the Harajuku area',
                '👶 Kid-friendly atmosphere with character appeal'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shibuya Character Stores Marathon',
              description: 'Time for the main event — a crawl through Shibuya\'s incredible character stores. Start at Pokémon Center Shibuya, hit the MAGNET by SHIBUYA109 building, and browse to your heart\'s content.',
              details: [
                '🎮 Pokémon Center Shibuya — massive store with exclusive Shibuya Pikachu merch',
                '🏪 MAGNET by SHIBUYA109 — multi-floor shopping with rooftop views',
                '👕 Brandy Melville Japan — in the Shibuya/Harajuku area'
              ]
            },
            {
              title: 'ONE PIECE Mugiwara Store',
              description: 'Located in the Harajuku/Shibuya area, this official One Piece merchandise store has exclusive figures, clothing, and collectibles. A must for any One Piece fan in the family.',
              details: [
                '🏴‍☠️ Exclusive Mugiwara Store merchandise',
                '📍 Harajuku area — walkable from Shibuya',
                '📸 Photo ops with life-size character displays'
              ]
            },
            {
              title: 'CAFE REISSUE',
              description: 'Famous for their incredible latte art — they\'ll draw any character on your coffee. Kids love watching the artist work. The café also serves kid-friendly drinks and light food.',
              details: [
                '☕ Custom latte art — request any character!',
                '📍 Shibuya area',
                '📸 Instagram-worthy drinks'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Wagyu Halal Steak HamBurger & Ramen 5W-Tokyo 1962',
              description: 'Halal-certified wagyu burgers and chicken ramen — completely pork-free with halal certification. Perfect for your dietary needs with incredible quality.',
              meta: '💰 $$ · 📍 Central Tokyo · Halal certified, no pork'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Don Quijote Shibuya',
              description: 'The legendary discount store — a chaotic wonderland of snacks, toys, electronics, costumes, and souvenirs across multiple floors. Kids will love the toy sections and the sheer sensory overload.',
              details: [
                '🏪 Open until late (some 24hr)',
                '🍬 Stock up on Japanese snacks and Kit-Kat flavors',
                '🎎 Great for souvenirs — tax-free for tourists over ¥5,000'
              ]
            }
          ],
          meals: [
            {
              type: '🍕 Dinner',
              name: 'Immo Pipi — Sweet Potato Treats',
              description: 'A sweet potato dessert shop with gorgeous purple and golden sweet potato parfaits, soft serve, and baked treats. Naturally pork-free and kids go crazy for the colorful sweets.',
              meta: '💰 $ · 📍 Shibuya/Harajuku area · Pork-free'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6764, lng: 139.6993, label: 'Meiji Jingu Shrine', num: 1, cat: 'attraction', desc: 'Ancient Shinto shrine in a 170-acre forest' },
        { lat: 35.6688, lng: 139.7024, label: 'PEANUTS Cafe', num: 2, cat: 'food', desc: 'Snoopy-themed café with latte art' },
        { lat: 35.6611, lng: 139.6988, label: 'Pokémon Center Shibuya', num: 3, cat: 'shopping', desc: 'Massive Pokémon store with Shibuya exclusives' },
        { lat: 35.6607, lng: 139.6984, label: 'MAGNET by SHIBUYA109', num: 4, cat: 'shopping', desc: 'Multi-floor shopping with rooftop views' },
        { lat: 35.6699, lng: 139.7032, label: 'ONE PIECE Mugiwara Store', num: 5, cat: 'shopping', desc: 'Official One Piece merchandise store' },
        { lat: 35.6618, lng: 139.7002, label: 'CAFE REISSUE', num: 6, cat: 'food', desc: 'Famous custom latte art café' },
        { lat: 35.6622, lng: 139.6998, label: 'Don Quijote Shibuya', num: 7, cat: 'shopping', desc: 'Legendary discount store — open late' },
        { lat: 35.6596, lng: 139.7005, label: 'Brandy Melville Japan', num: 8, cat: 'shopping', desc: 'Trendy fashion store' },
        { lat: 35.6630, lng: 139.7010, label: 'Immo Pipi', num: 9, cat: 'food', desc: 'Sweet potato desserts — colorful and kid-friendly' }
      ]
    },
    {
      num: 4,
      date: '2026-05-18',
      neighborhoods: 'Ikebukuro · Shinjuku · Ginza',
      title: 'Ikebukuro Characters, Shinjuku Nightlife Streets & Ginza Culture',
      description: "A packed day spanning three of Tokyo's most exciting neighborhoods. Morning at Ikebukuro's character paradise, afternoon in sophisticated Ginza, and evening exploring Shinjuku's atmospheric alleyways (kid-friendly, we promise).",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sunshine City Ikebukuro',
              description: 'A massive entertainment complex with an aquarium, Pokémon Center, Ghibli store, and Namco game center all under one roof. You could spend the whole morning here easily.',
              details: [
                '🐠 Sunshine Aquarium on the rooftop — penguins "fly" through a sky pool',
                '🎮 Pokémon Center Mega Tokyo — the largest Pokémon store in Tokyo',
                '🧁 Pikachu Sweets — Pokémon-themed desserts and drinks right next door',
                '🏪 Tons of character stores and kids\' entertainment'
              ]
            },
            {
              title: 'Donguri Kyowakoku (Ghibli Store) Ikebukuro',
              description: 'The official Studio Ghibli merchandise store — Totoro plushies, Kiki\'s Delivery Service bags, Spirited Away figurines, and more. Located in the Sunshine City area.',
              details: [
                '🌿 Official Ghibli merch — quality is outstanding',
                '🧸 Totoro plushies in all sizes — perfect souvenir for kids',
                '📍 Inside Sunshine City, Ikebukuro'
              ]
            },
            {
              title: 'KIDDY LAND',
              description: 'A multi-floor toy store paradise with character goods from every franchise imaginable. Sanrio, Disney, Pokémon, Ghibli, and more.',
              details: [
                '🧸 Multiple floors of toys and character merchandise',
                '📍 Ikebukuro area',
                '👶 Toddlers will want everything — budget warning!'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ginza — Art Aquarium & Matcha',
              description: 'Head to the upscale Ginza district for the mesmerizing ART AQUARIUM MUSEUM — goldfish swimming in illuminated artistic tanks that captivate kids and adults alike. Then stop at Matcha café Wabisabi for beautiful matcha drinks.',
              details: [
                '🐟 ART AQUARIUM MUSEUM — stunning light and water art with thousands of goldfish',
                '🍵 Matcha café Wabisabi — gorgeous matcha lattes and desserts',
                '📍 Ginza is stroller-friendly with wide sidewalks'
              ]
            },
            {
              title: 'Godaime Hanayama Udon — Ginza',
              description: 'Famous for thick, chewy udon noodles — a pork-free lunch option where you can watch the noodles being made. Kids love the texture and the interactive experience.',
              details: [
                '🍜 Thick sanuki-style udon — choose chicken or veggie tempura toppings',
                '🚫 Pork-free options available — ask for tori (chicken) or yasai (vegetable) broth',
                '📍 Ginza district'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Godaime Hanayama Udon',
              description: 'Thick, handmade udon noodles in Ginza. Get the chicken tempura udon for a hearty, pork-free meal. The noodle-making performance is mesmerizing for kids.',
              meta: '💰 $$ · 📍 Ginza · Pork-free options'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shinjuku Evening — Omoide Yokocho & Golden Gai',
              description: 'Walk through the atmospheric narrow alleys of Omoide Yokocho (Memory Lane) and Golden Gai — they\'re safe, well-lit, and fascinating to walk through even with kids. The tiny bars and lantern-lit alleys are like stepping into a movie set. For food, stick to the yakitori (chicken skewer) stalls.',
              details: [
                '🏮 Omoide Yokocho — atmospheric alley of tiny restaurants under the train tracks',
                '🍢 Yakitori (chicken skewers) — completely pork-free, order "torikawa" (chicken skin) and "negima" (chicken & leek)',
                '📸 Golden Gai — 6 narrow alleys with 200+ tiny bars, incredible for photos even if you don\'t drink',
                '🎭 Kabukicho & Kabuki Hall/Yokocho — the neon entertainment district, fun to walk through'
              ]
            },
            {
              title: 'Shinjuku Station East Exit (JJK Reference)',
              description: 'For the anime fans — Shinjuku Station\'s east exit is a key location in Jujutsu Kaisen. Snap your photos at this iconic spot.',
              details: [
                '📸 JJK fans will recognize this immediately',
                '📍 Shinjuku Station East Exit area',
                '🎌 Also near SURUGA-YA (anime collectibles) and Seria (100-yen shop)'
              ]
            }
          ],
          meals: [
            {
              type: '🍕 Dinner',
              name: 'Yakitori at Omoide Yokocho',
              description: 'Chicken skewers grilled over charcoal in the atmospheric alleyways under the Shinjuku train tracks. Stick to chicken (tori) skewers — they\'re everywhere and delicious. Ask for "tori" only.',
              meta: '💰 $ · 📍 Omoide Yokocho, Shinjuku · Chicken-only options available'
            }
          ],
          tips: [
            { type: 'tip', text: 'Golden Gai and Omoide Yokocho are perfectly safe to walk through with kids — especially in the early evening (5-7pm). Many tiny bars don\'t allow children inside, but the alleyways themselves are a photographer\'s dream.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7292, lng: 139.7193, label: 'Sunshine City', num: 1, cat: 'attraction', desc: 'Pokémon Center Mega, Aquarium, Ghibli Store' },
        { lat: 35.7294, lng: 139.7195, label: 'Pokémon Center Mega Tokyo', num: 2, cat: 'shopping', desc: 'Tokyo\'s biggest Pokémon store + Pikachu Sweets' },
        { lat: 35.7290, lng: 139.7191, label: 'Donguri Kyowakoku', num: 3, cat: 'shopping', desc: 'Official Studio Ghibli merchandise store' },
        { lat: 35.7280, lng: 139.7185, label: 'KIDDY LAND', num: 4, cat: 'shopping', desc: 'Multi-floor toy store paradise' },
        { lat: 35.6693, lng: 139.7639, label: 'ART AQUARIUM MUSEUM', num: 5, cat: 'attraction', desc: 'Illuminated goldfish art museum' },
        { lat: 35.6710, lng: 139.7650, label: 'Matcha café Wabisabi', num: 6, cat: 'food', desc: 'Beautiful matcha drinks and desserts' },
        { lat: 35.6705, lng: 139.7636, label: 'Godaime Hanayama Udon', num: 7, cat: 'food', desc: 'Famous thick udon noodles — pork-free' },
        { lat: 35.6938, lng: 139.6987, label: 'Omoide Yokocho', num: 8, cat: 'food', desc: 'Atmospheric alley of tiny restaurants under the tracks' },
        { lat: 35.6941, lng: 139.7037, label: 'Golden Gai', num: 9, cat: 'attraction', desc: '200+ tiny bars in 6 narrow alleys' },
        { lat: 35.6945, lng: 139.7043, label: 'Kabukicho', num: 10, cat: 'attraction', desc: 'Neon entertainment district' },
        { lat: 35.6910, lng: 139.7005, label: 'SURUGA-YA', num: 11, cat: 'shopping', desc: 'Anime collectibles and retro goods' },
        { lat: 35.6905, lng: 139.7008, label: 'Seria', num: 12, cat: 'shopping', desc: '100-yen shop — great for souvenirs' },
        { lat: 35.6896, lng: 139.7020, label: 'Shinjuku Station East Exit', num: 13, cat: 'attraction', desc: 'JJK reference point' }
      ]
    },
    {
      num: 5,
      date: '2026-05-19',
      neighborhoods: 'Odaiba · Toyosu · Tsukiji · Shiba Park',
      title: 'teamLab, Tsukiji, Tokyo Tower & Farewell Tokyo',
      description: "Your final Tokyo day hits some bucket-list experiences — the mind-bending teamLab Planets, the legendary Tsukiji Fish Market, Tokyo Tower, and a relaxing evening before the Shinkansen tomorrow. Pack it in but keep the pace toddler-friendly.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'teamLab Planets',
              description: 'An immersive digital art museum where you wade through water, walk barefoot through light installations, and lose yourself in infinity rooms. Toddlers are mesmerized by the colors and textures. You MUST book tickets in advance.',
              details: [
                '🎨 Book online at teamlab.art — ¥3,800 adults, ¥1,500 ages 4-12, free under 4',
                '👣 You go barefoot — they provide lockers for shoes and bags',
                '💧 Some rooms have knee-deep water — carry toddlers or let them wade',
                '📸 Incredibly photogenic — every room is a different world',
                '⏰ Go at opening (9 or 10am) for smaller crowds'
              ]
            },
            {
              title: 'Tsukiji Outer Market',
              description: 'The inner wholesale market moved to Toyosu, but the outer market is alive and thriving — hundreds of food stalls, fresh seafood, tamagoyaki (egg omelette), and street food. This is where locals eat.',
              details: [
                '🐟 Try fresh sashimi, grilled scallops, and tamagoyaki on a stick',
                '🍳 Tamagoyaki (sweet egg omelette) — kids love it, zero pork',
                '🦐 Grilled seafood stalls — shrimp, scallops, and uni',
                '🚶 Narrow aisles — stroller is manageable but tight in peak hours'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Brunch',
              name: 'Tsukiji Outer Market Street Food',
              description: 'Graze through the stalls — fresh sashimi bowls, grilled seafood skewers, tamagoyaki, and matcha desserts. All pork-free seafood options.',
              meta: '💰 $–$$ · 📍 Tsukiji Outer Market · Pork-free seafood everywhere'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Prince Shiba Park & Tokyo Tower',
              description: 'A peaceful green space with direct views of Tokyo Tower — let the kids run around the park, then head up Tokyo Tower for panoramic views. Less crowded than Skytree and more iconic.',
              details: [
                '🗼 Tokyo Tower — Main Deck ¥1,200 adults, ¥700 ages 4-15, free under 4',
                '🌿 Prince Shiba Park — free, grassy, perfect for a break',
                '📸 The tower lit up at sunset is magical — time your visit for late afternoon'
              ]
            },
            {
              title: 'Hie-jinja Shrine',
              description: 'A beautiful shrine near Akasaka with a stunning tunnel of red torii gates (smaller than Fushimi Inari but with zero crowds). The escalator entrance makes it uniquely stroller-accessible.',
              details: [
                '⛩️ Free entry — beautiful tunnel of red torii gates',
                '♿ Has an escalator — rare for a shrine!',
                '📸 The torii tunnel is stunning and usually empty'
              ]
            },
            {
              title: 'Kirby Café Tokyo',
              description: 'An adorable Kirby-themed café with character-shaped food, Kirby desserts, and exclusive merchandise. Reservations are essential — book online well in advance.',
              details: [
                '🌟 Book at kirbycafe.jp — reservations open ~1 month ahead',
                '🍰 Every dish is Kirby-shaped — the attention to detail is incredible',
                '📍 Tokyo Solamachi (Skytree area) — but reachable from Shiba Park by train',
                '👶 Extremely kid-friendly — they even have Kirby bibs!'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Late Lunch',
              name: 'Kirby Café',
              description: 'Character-shaped curry, pasta, and desserts in the cutest café you\'ve ever seen. Book well in advance — it\'s insanely popular. Chicken and seafood options available (no pork).',
              meta: '💰 $$$ · 📍 Tokyo Solamachi · Reservations required, pork-free options'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'The Front Room Deli Marunouchi',
              description: 'A relaxed deli-style restaurant near Tokyo Station — perfect for a calm farewell dinner before your Shinkansen tomorrow. Quality sandwiches, salads, and pastries.',
              details: [
                '📍 Marunouchi area, near Tokyo Station',
                '🥪 Quality deli food — great for families who want a chill dinner',
                '🚉 Close to Tokyo Station for easy hotel access'
              ]
            },
            {
              title: 'Gōtokuji Temple (Cat Temple)',
              description: 'If energy permits — a charming temple covered in thousands of maneki-neko (beckoning cat) figurines. It\'s the birthplace of the lucky cat tradition. A unique, photo-worthy stop.',
              details: [
                '🐱 Thousands of lucky cat figurines covering every surface',
                '📍 In Setagaya — about 20 min from Shinjuku by train',
                '📸 One of Tokyo\'s most unique photo spots',
                '⚡ Optional — only if the family has energy left!'
              ]
            }
          ],
          meals: [
            {
              type: '🍕 Dinner',
              name: 'The Front Room Deli Marunouchi',
              description: 'Casual, high-quality deli near Tokyo Station. Sandwiches, grain bowls, and pastries — a relaxed end to your Tokyo days before the Shinkansen south tomorrow.',
              meta: '💰 $$ · 📍 Marunouchi, near Tokyo Station'
            }
          ],
          tips: [
            { type: 'tip', text: 'Tonight: pack your bags and organize luggage. Tomorrow you take the Shinkansen to Osaka. Ship large luggage ahead via "takkyubin" (hotel front desk can arrange Yamato Transport) — travel light with kids on the bullet train.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6426, lng: 139.7777, label: 'teamLab Planets', num: 1, cat: 'attraction', desc: 'Immersive barefoot digital art museum' },
        { lat: 35.6654, lng: 139.7707, label: 'Tsukiji Outer Market', num: 2, cat: 'food', desc: 'Legendary food market — fresh seafood & tamagoyaki' },
        { lat: 35.6586, lng: 139.7454, label: 'Tokyo Tower', num: 3, cat: 'attraction', desc: 'Iconic tower with panoramic views' },
        { lat: 35.6577, lng: 139.7480, label: 'Prince Shiba Park', num: 4, cat: 'attraction', desc: 'Green park with Tokyo Tower views' },
        { lat: 35.6756, lng: 139.7399, label: 'Hie-jinja Shrine', num: 5, cat: 'attraction', desc: 'Red torii tunnel — has an escalator!' },
        { lat: 35.7101, lng: 139.8107, label: 'Kirby Café', num: 6, cat: 'food', desc: 'Adorable character-shaped food — book ahead!' },
        { lat: 35.6812, lng: 139.7671, label: 'The Front Room Deli', num: 7, cat: 'food', desc: 'Casual deli near Tokyo Station' },
        { lat: 35.6530, lng: 139.6376, label: 'Gōtokuji Temple', num: 8, cat: 'attraction', desc: 'Cat temple — thousands of lucky cat figurines' }
      ]
    },
    {
      num: 6,
      date: '2026-05-20',
      neighborhoods: 'Tokyo → Osaka · Dotonbori · Shinsaibashi · Namba',
      title: 'Shinkansen to Osaka — Dotonbori & Pokémon Café',
      description: "Bullet train day! Ride the Shinkansen to Osaka, check into your Kansai base camp, then dive into the electric energy of Dotonbori. Tonight is all about glowing neon signs, street food, and one of Japan's most photogenic streets.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinkansen: Tokyo → Shin-Osaka',
              description: 'Take the Tokaido Shinkansen from Tokyo Station to Shin-Osaka (~2.5 hours). Reserve seats in advance — get a window seat on the right side (seats A/B) for Mount Fuji views around Shin-Fuji station.',
              details: [
                '🚅 Nozomi is fastest (~2h15m) but NOT covered by JR Pass. Take Hikari (~2h40m) with JR Pass.',
                '🗻 Mount Fuji views: right side, ~40 min after departure',
                '🍱 Buy ekiben (station bento) at Tokyo Station — incredible variety, mostly pork-free options available',
                '👶 Kids love watching the landscape zoom by at 300 km/h'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'JR Pass tip: If you have a 7-day pass activated on May 18, it covers today\'s Shinkansen and all Kansai local JR trains through May 24. The Hikari Shinkansen (covered by JR Pass) is only 15 min slower than Nozomi.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In & Rest',
              description: 'Settle into your Osaka hotel (Namba/Shinsaibashi area recommended). Let the kids decompress and nap. The travel day warrants a break.',
              details: [
                '🏨 Namba/Shinsaibashi hotels put you walking distance from Dotonbori',
                '😴 Toddler nap time — seriously, take the break',
                '📍 You\'ll use Osaka as base for 5 days of Kansai exploration'
              ]
            },
            {
              title: 'Pokémon Café Osaka Shinsaibashi',
              description: 'A themed Pokémon café with character-shaped food, drinks served in Pokémon mugs (you can buy them!), and adorable details everywhere. Reservations are mandatory — book online at pokemoncafe-reservation.com.',
              details: [
                '🎮 Book 31 days in advance at pokemoncafe-reservation.com',
                '🍰 Pikachu curry, Eevee pancakes, and character drinks',
                '🛍️ Exclusive Pokémon Café merchandise',
                '👶 Incredibly kid-friendly — high chairs available'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Late Lunch',
              name: 'Pokémon Café Osaka',
              description: 'Character-shaped curry, pancakes, and drinks in an adorable themed café. Your kids will be in Pokémon heaven. Chicken and veggie options (no pork). Book 31 days ahead!',
              meta: '💰 $$$ · 📍 Shinsaibashi · Reservations mandatory'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dotonbori Night Walk',
              description: 'Osaka\'s most iconic street comes alive at night — the massive Glico Running Man sign, neon-lit canal, and endless street food stalls. This is Osaka at its most electric.',
              details: [
                '📸 The Glico Sign — the most photographed spot in Osaka, take your family photo here',
                '🦐 Street food: takoyaki (octopus balls), kushikatsu (fried skewers — confirm no pork), yakitori (chicken)',
                '🌊 Dotonbori Canal — the reflections at night are magical',
                '🚶 Flat, wide streets — very stroller-friendly'
              ]
            },
            {
              title: 'Onitsuka Tiger Store',
              description: 'Pick up authentic Onitsuka Tiger sneakers at the Shinsaibashi store — Japan-exclusive colorways and limited editions at better prices than abroad.',
              details: [
                '👟 Japan-exclusive designs and colorways',
                '📍 Shinsaibashi shopping arcade, near Dotonbori',
                '💰 Often cheaper than overseas — especially limited editions'
              ]
            }
          ],
          meals: [
            {
              type: '🍕 Dinner',
              name: 'Dotonbori Street Food',
              description: 'Graze the stalls — takoyaki (octopus balls, no pork), yakitori, grilled seafood, and the famous cheesecake shops. Osaka is the street food capital of Japan.',
              meta: '💰 $ · 📍 Dotonbori · Pork-free options everywhere'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6812, lng: 139.7671, label: 'Tokyo Station', num: 1, cat: 'transport', desc: 'Shinkansen departure — buy ekiben here' },
        { lat: 34.7336, lng: 135.5001, label: 'Shin-Osaka Station', num: 2, cat: 'transport', desc: 'Shinkansen arrival in Osaka' },
        { lat: 34.6687, lng: 135.5031, label: 'Pokémon Café Osaka', num: 3, cat: 'food', desc: 'Character-shaped food — reservations required' },
        { lat: 34.6687, lng: 135.5024, label: 'Glico Sign Dotonbori', num: 4, cat: 'attraction', desc: 'Osaka\'s most iconic photo spot' },
        { lat: 34.6690, lng: 135.5020, label: 'Dotonbori', num: 5, cat: 'food', desc: 'Street food paradise — takoyaki, yakitori, seafood' },
        { lat: 34.6720, lng: 135.5021, label: 'Onitsuka Tiger Store', num: 6, cat: 'shopping', desc: 'Japan-exclusive sneakers' }
      ]
    },
    {
      num: 7,
      date: '2026-05-21',
      neighborhoods: 'Kyoto — Arashiyama · Sagano',
      title: 'Kyoto Day Trip #1 — Arashiyama & Bamboo Forest',
      description: "Take the train from Osaka to Arashiyama, Kyoto's most enchanting district. Towering bamboo groves, a monkey park on a mountain, the Kimono Forest installation, and one of the quirkiest temples in Japan — all in a compact, walkable area.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Train: Osaka → Arashiyama',
              description: 'Take the JR line from Osaka to Saga-Arashiyama station (~45 min, covered by JR Pass). Arrive early to beat the crowds at the bamboo grove.',
              details: [
                '🚃 JR Osaka → Saga-Arashiyama, ~45 min',
                '⏰ Aim to arrive by 9am — the bamboo grove is magical when empty',
                '🎫 Covered by JR Pass'
              ]
            },
            {
              title: 'Arashiyama Bamboo Grove',
              description: 'Walk through a cathedral of soaring bamboo stalks — one of the most iconic sights in all of Japan. The path is paved and stroller-friendly. Go early morning for the best experience with minimal crowds.',
              details: [
                '🎋 Free — the path is public',
                '🚶 Paved, flat, stroller-friendly',
                '📸 Early morning light through the bamboo is otherworldly',
                '⏰ Best before 10am — it gets extremely crowded midday'
              ]
            },
            {
              title: 'Kimono Forest',
              description: 'Right at Arashiyama station — hundreds of colorful kimono-fabric cylinders lit from within, lining the path. Beautiful by day, magical at dusk. Kids love running between the pillars.',
              details: [
                '🎌 600 kimono fabric poles — each unique',
                '📍 Randen Arashiyama Station',
                '📸 Incredible photo spot — especially with kimono rental'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Monkey Park Iwatayama',
              description: 'Hike up the mountain (about 20 min uphill) to a park where wild Japanese macaques roam free. You feed them from inside a shelter while they hang out right next to you. Kids are OBSESSED.',
              details: [
                '🐒 ¥550 adults, ¥250 ages 4-15',
                '⛰️ 20-min uphill walk — leave the stroller at the bottom',
                '🥜 Buy monkey food (¥100) at the top — feed them through the mesh!',
                '👶 Carry the toddlers up — the path is well-maintained but steep',
                '📸 Panoramic views of Kyoto from the top'
              ]
            },
            {
              title: 'Miffy Sakura Kitchen',
              description: 'A Miffy-themed bakery and café in Arashiyama serving adorable Miffy-shaped bread, cookies, and drinks. The perfect mid-afternoon treat stop.',
              details: [
                '🐰 Miffy-shaped melon bread and cookies',
                '📍 Main Arashiyama shopping street',
                '👶 Quick stop — great for a snack break'
              ]
            },
            {
              title: 'Otagi Nenbutsu-ji Temple',
              description: 'A hidden gem with 1,200 stone rakan (Buddhist disciple) statues — each carved with a unique, expressive face. Some are laughing, some hold cats, some play sports. Kids love finding funny faces among the statues.',
              details: [
                '🗿 1,200 unique stone statues — no two alike',
                '¥300 entry',
                '📍 A 15-min walk from the bamboo grove — away from crowds',
                '📸 One of the most unique photo spots in all of Kyoto'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Miffy Sakura Kitchen + Arashiyama street food',
              description: 'Grab Miffy bread at the bakery, then snack along the main Arashiyama shopping street — matcha soft serve, dango (rice dumplings), and grilled mochi. All naturally pork-free.',
              meta: '💰 $ · 📍 Arashiyama · Pork-free snacks'
            }
          ],
          tips: [
            { type: 'tip', text: 'Kimono Rental: Consider renting kimonos in Arashiyama for the family — many shops offer kids\' sizes. Photos in the bamboo grove in kimonos are unforgettable. Rent near the station and return before your train back.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Osaka & Rest',
              description: 'Head back to Osaka by late afternoon. After a big day of exploring Arashiyama, keep the evening low-key. Pick up convenience store food or find a local restaurant near your hotel.',
              details: [
                '🚃 JR Saga-Arashiyama → Osaka, ~45 min',
                '😴 Kids will likely nap on the train — let them',
                '🏨 Low-key evening at the hotel'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0168, lng: 135.6713, label: 'Arashiyama Bamboo Grove', num: 1, cat: 'attraction', desc: 'Iconic towering bamboo forest — go early!' },
        { lat: 35.0142, lng: 135.6738, label: 'Kimono Forest', num: 2, cat: 'attraction', desc: '600 illuminated kimono fabric pillars' },
        { lat: 35.0097, lng: 135.6769, label: 'Monkey Park Iwatayama', num: 3, cat: 'attraction', desc: 'Wild macaques on a mountain with panoramic views' },
        { lat: 35.0170, lng: 135.6720, label: 'Miffy Sakura Kitchen', num: 4, cat: 'food', desc: 'Adorable Miffy-themed bakery' },
        { lat: 35.0293, lng: 135.6588, label: 'Otagi Nenbutsu-ji', num: 5, cat: 'attraction', desc: '1,200 uniquely carved stone statues' }
      ]
    },
    {
      num: 8,
      date: '2026-05-22',
      neighborhoods: 'Kyoto — Fushimi · Gion · Okazaki',
      title: 'Kyoto Day Trip #2 — Red Gates, Gion & Kimono Experience',
      description: "Today hits Kyoto's other iconic sights — the endless red torii gates of Fushimi Inari, the geisha district of Gion, the beautiful Okazaki area, and a kimono rental experience that'll produce photos you'll treasure forever.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Fushimi Inari Taisha',
              description: 'The most visited shrine in Japan — thousands of vermillion torii gates wind up the mountain in a seemingly endless tunnel of red. You don\'t need to hike the full mountain; the lower paths (first 15-20 minutes) are the most photographed and stroller-possible.',
              details: [
                '⛩️ Free entry — open 24/7',
                '🚶 Lower paths are paved — manageable with a stroller for the first section',
                '📸 Best photos: the dense gate tunnels on the lower mountain',
                '⏰ Arrive by 9am to avoid the worst crowds',
                '🦊 Fox statues everywhere — kids love spotting them all',
                '⛰️ Full hike is 2-3 hours — with toddlers, stick to the lower 30 min'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kimono Rental Experience',
              description: 'Rent traditional kimonos for the whole family (yes, they have toddler sizes!). Wear them through Gion and Okazaki for stunning photos. Most rental shops handle the full dressing — it takes about 30 minutes.',
              details: [
                '👘 Many shops near Gion/Higashiyama — book ahead online',
                '👶 Kids\' kimonos available from age 1 — incredibly cute',
                '⏰ Rent morning, return by 5-6pm (varies by shop)',
                '💰 ~¥3,000-5,000 per person, kids ~¥2,000-3,000'
              ]
            },
            {
              title: 'Gion District',
              description: 'Kyoto\'s famous geisha district — wooden machiya townhouses, tea houses, and stone-paved streets. Walk along Hanami-koji and Shirakawa canal for the most atmospheric stroll in Kyoto.',
              details: [
                '🎭 You might spot a geiko (geisha) or maiko (apprentice) heading to appointments',
                '📸 Hanami-koji street and Shirakawa canal are the most photogenic spots',
                '🚶 Flat, stroller-friendly streets',
                '🍵 Many tea houses for matcha and wagashi (traditional sweets)'
              ]
            },
            {
              title: 'Okazaki Sakura Corridor',
              description: 'A beautiful canal-side walkway in the Okazaki area. While the cherry blossoms will be past by May, the tree-lined canal is still lovely and peaceful — a great stroller walk.',
              details: [
                '🌊 Beautiful canal with tree-lined banks',
                '📍 Near Heian Shrine in the Okazaki area',
                '🚶 Flat, peaceful, stroller-perfect'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Men-ya Inoichi Ramen',
              description: 'A Kyoto ramen shop known for their rich chicken (tori) broth ramen — completely pork-free. The chicken paitan broth is creamy and delicious. One of the best pork-free ramen experiences in Kyoto.',
              meta: '💰 $$ · 📍 Central Kyoto · Chicken broth — no pork'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Osaka',
              description: 'Train back to Osaka (~30-40 min from central Kyoto). Another fulfilling day exploring Kyoto\'s cultural treasures.',
              details: [
                '🚃 JR or Keihan line back to Osaka',
                '🌆 If kids have energy, grab dinner in Dotonbori again',
                '😴 Otherwise, convenience store dinner and early bedtime'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari Taisha', num: 1, cat: 'attraction', desc: 'Thousands of red torii gates winding up the mountain' },
        { lat: 35.0037, lng: 135.7747, label: 'Gion District', num: 2, cat: 'attraction', desc: 'Geisha district — wooden townhouses & tea rooms' },
        { lat: 35.0132, lng: 135.7837, label: 'Okazaki Sakura Corridor', num: 3, cat: 'attraction', desc: 'Tree-lined canal walkway' },
        { lat: 35.0052, lng: 135.7684, label: 'Men-ya Inoichi Ramen', num: 4, cat: 'food', desc: 'Chicken broth ramen — no pork' },
        { lat: 35.0040, lng: 135.7760, label: 'Kimono Rental', num: 5, cat: 'attraction', desc: 'Family kimono rental — toddler sizes available' }
      ]
    },
    {
      num: 9,
      date: '2026-05-23',
      neighborhoods: 'Nara — Nara Park · Todai-ji · Gardens',
      title: 'Nara Day Trip — Deer, Gardens & Tea',
      description: "A magical day trip to Nara — where over 1,000 friendly deer roam freely through parks and temple grounds. Toddlers feeding deer, stunning botanical gardens, ice cream bouquets, and a peaceful tea house. This might be the kids' favorite day of the entire trip.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Train: Osaka → Nara',
              description: 'Take the Kintetsu line from Namba to Kintetsu-Nara (~35 min) or JR from Osaka to JR Nara (~45 min, covered by JR Pass). Both stations are walking distance from Nara Park.',
              details: [
                '🚃 Kintetsu is faster and closer to the park; JR is covered by JR Pass',
                '⏰ Arrive by 9:30am for a full day',
                '👶 Easy, flat walk from either station to the park'
              ]
            },
            {
              title: 'Nara Park — Deer Feeding',
              description: 'Over 1,000 sika deer roam freely through Nara Park. Buy deer crackers (shika senbei, ¥200) and feed them. The deer bow to you before eating — it\'s incredibly charming. Supervise toddlers closely as deer can be enthusiastic.',
              details: [
                '🦌 Buy shika senbei (deer crackers) from vendors — ¥200 per pack',
                '🦌 The deer BOW before you feed them — genuinely magical',
                '👶 Hold toddlers while feeding — deer are gentle but persistent when they see food',
                '📸 Deer + toddler photos will be the trip highlight, guaranteed',
                '🚶 Flat, wide paths — very stroller-friendly'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Manyo Botanical Gardens',
              description: 'A serene botanical garden within Nara Park featuring plants referenced in ancient Japanese poetry. Peaceful paths through flowers and greenery — a wonderful contrast to the energetic deer park.',
              details: [
                '🌺 Seasonal flowers and ancient plant varieties',
                '🚶 Gentle paths through themed gardens',
                '😌 Calm and uncrowded — a nice toddler pace'
              ]
            },
            {
              title: 'Boksburg Market — Ice Cream Bouquet',
              description: 'A charming café/market known for their stunning ice cream bouquets — scoops arranged like a flower bouquet. Incredibly photogenic and delicious.',
              details: [
                '🍦 Ice cream bouquet — multiple flavors arranged like flowers',
                '📸 One of the most Instagram-worthy treats in Nara',
                '👶 Kids will love picking their own flavors'
              ]
            },
            {
              title: 'Rokujuan Tea House',
              description: 'A traditional Japanese tea house where you can enjoy matcha and wagashi (traditional sweets) in a serene setting. A calming afternoon experience.',
              details: [
                '🍵 Matcha and traditional Japanese sweets',
                '🏯 Traditional tatami room setting',
                '😌 Peaceful break — let the kids explore the garden'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Nara area restaurants',
              description: 'Try kakinoha-zushi (persimmon leaf sushi) — Nara\'s famous specialty. Pressed sushi wrapped in persimmon leaves with salmon or mackerel (no pork). Available at many restaurants near the park.',
              meta: '💰 $$ · 📍 Nara Park area · Pork-free sushi'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Nishiki Robe Photoshoot',
              description: 'If you arranged a nishiki (traditional Japanese robe) photoshoot, late afternoon golden hour in Nara Park with the deer makes for absolutely magical family photos.',
              details: [
                '📸 Golden hour light + deer + traditional robes = perfection',
                '📍 Book with a local Nara photographer for professional shots',
                '👶 Toddlers in tiny robes are the cutest thing you\'ll ever see'
              ]
            },
            {
              title: 'Return to Osaka',
              description: 'Train back to Osaka for your last evening in Kansai.',
              details: [
                '🚃 Kintetsu-Nara → Namba, ~35 min',
                '🌃 Last night — maybe revisit a favorite Dotonbori stall'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6851, lng: 135.8430, label: 'Nara Park', num: 1, cat: 'attraction', desc: 'Friendly deer roaming free — buy deer crackers!' },
        { lat: 34.6890, lng: 135.8399, label: 'Manyo Botanical Gardens', num: 2, cat: 'attraction', desc: 'Serene gardens with ancient plant varieties' },
        { lat: 34.6820, lng: 135.8300, label: 'Boksburg Market', num: 3, cat: 'food', desc: 'Famous ice cream bouquets' },
        { lat: 34.6845, lng: 135.8420, label: 'Rokujuan Tea House', num: 4, cat: 'food', desc: 'Traditional matcha and wagashi' },
        { lat: 34.6860, lng: 135.8410, label: 'Nishiki Robe Photoshoot', num: 5, cat: 'attraction', desc: 'Golden hour photos in traditional robes with deer' }
      ]
    },
    {
      num: 10,
      date: '2026-05-24',
      neighborhoods: 'Osaka — Tempozan · Kaiyukan · Departure',
      title: 'Osaka Aquarium & Farewell Japan',
      description: "Your final day in Japan — make it count with the spectacular Osaka Aquarium Kaiyukan, one of the world's largest aquariums. Then soak in your last moments before heading to the airport. What a trip.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Osaka Aquarium Kaiyukan',
              description: 'One of the world\'s largest aquariums — home to whale sharks, manta rays, penguins, and an incredible Pacific Rim exhibit. The spiral walkway takes you from the top to the bottom of massive tanks. Toddlers are absolutely captivated.',
              details: [
                '🐋 Whale sharks in a 5,400 ton tank — the centerpiece is jaw-dropping',
                '🎫 ¥2,700 adults, ¥1,200 ages 4-6, free under 4 — book online',
                '🐧 Touch pool at the end — kids can touch rays and sharks',
                '⏰ Opens at 10am — arrive at opening for smallest crowds',
                '🚶 Stroller-friendly — elevators available',
                '📍 Tempozan Harbor area — about 30 min from Namba by subway'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tempozan Harbor Village',
              description: 'Explore the area around the aquarium — there\'s a giant Ferris wheel (Tempozan Giant Ferris Wheel) with views of the bay, a shopping mall, and waterfront restaurants.',
              details: [
                '🎡 Tempozan Ferris Wheel — ¥800, stunning bay views',
                '🛍️ Tempozan Marketplace — shops and restaurants',
                '📸 Beautiful waterfront area for final Japan photos'
              ]
            },
            {
              title: 'Last-Minute Shopping & Souvenir Run',
              description: 'Head back to Shinsaibashi or Dotonbori for any last souvenirs, snacks, and gifts. Don Quijote in Dotonbori is open late and has everything.',
              details: [
                '🍬 Japanese Kit-Kats, Tokyo Banana, matcha everything — stock up',
                '🏪 Don Quijote Dotonbori — tax-free for tourists over ¥5,000',
                '📍 Drug stores (Matsumoto Kiyoshi) for Japanese beauty products'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Lunch',
              name: 'Dotonbori favorites — one last round',
              description: 'Hit your favorite Dotonbori stalls one more time. Last chance for takoyaki, grilled seafood, and matcha soft serve. Eat everything.',
              meta: '💰 $–$$ · 📍 Dotonbori · Your last Osaka meal — make it count'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Departure',
              description: 'Head to Kansai International Airport (KIX). Take the Nankai Rapi:t from Namba (~38 min) or JR Haruka from Tennoji/Shin-Osaka (~45-50 min, covered by JR Pass if still valid).',
              details: [
                '✈️ Nankai Rapi:t from Namba — ¥1,450, stylish blue train',
                '🚃 JR Haruka — covered by JR Pass if valid, from Tennoji or Shin-Osaka',
                '⏰ Arrive at KIX 3 hours before international flights with kids',
                '🍬 Airport has excellent last-minute souvenir shops after security'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Ship souvenirs home! Japan Post EMS or Yamato Transport can ship boxes of souvenirs to your home address — much easier than stuffing them in luggage. Ask your hotel front desk to arrange it.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6545, lng: 135.4290, label: 'Osaka Aquarium Kaiyukan', num: 1, cat: 'attraction', desc: 'World-class aquarium — whale sharks & touch pool' },
        { lat: 34.6530, lng: 135.4280, label: 'Tempozan Ferris Wheel', num: 2, cat: 'attraction', desc: 'Giant Ferris wheel with bay views' },
        { lat: 34.6690, lng: 135.5020, label: 'Dotonbori', num: 3, cat: 'food', desc: 'Last chance for Osaka street food' },
        { lat: 34.4347, lng: 135.2441, label: 'Kansai International Airport', num: 4, cat: 'transport', desc: 'KIX — your departure point' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Flights (3 adults, roundtrip)', budget: '$2,400–3,600', midrange: '$3,600–5,400', luxury: '$6,000–12,000' },
    { category: '7-Day JR Pass (per adult)', budget: '¥50,000 (~$330)', midrange: '¥50,000 Ordinary', luxury: '¥70,000 Green Car' },
    { category: 'Accommodation (9 nights)', budget: '$1,200–1,800', midrange: '$2,000–3,500', luxury: '$4,000–8,000' },
    { category: 'Meals (family/day)', budget: '$60–100', midrange: '$120–200', luxury: '$250–400' },
    { category: 'Activities & Entry Fees', budget: '$200–400', midrange: '$400–600', luxury: '$600–1,000' },
    { category: 'Character Cafés (Kirby, Pokémon)', budget: '$80–120 total', midrange: '$120–180 total', luxury: '$180–250 total' },
    { category: '10-Day Total (family of 5)', budget: '$5,500–8,000', midrange: '$9,000–14,000', luxury: '$16,000–25,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Narita (NRT) or Haneda (HND) for Tokyo — Haneda is closer to the city', 'Depart from Kansai International (KIX) for a one-way trip flow', 'Book open-jaw tickets: arrive Tokyo, depart Osaka — avoid backtracking'] },
    { title: '🚅 JR Pass Strategy', items: ['7-Day JR Pass covers: Shinkansen (Tokyo→Osaka), JR local trains in both cities, JR to Nara', 'Activate on Day 4 (May 18) to cover May 18-24 — your Shinkansen day + all Kansai travel', 'NOT covered: Nankai Rapi:t to KIX airport, Kintetsu trains, Tokyo Metro/subway'] },
    { title: '👶 Toddler Survival Guide', items: ['Bring a lightweight umbrella stroller — it fits everywhere', 'Nursing rooms (赤ちゃん休憩室) in every department store and most stations', 'Convenience stores stock diapers, wet wipes, and baby food 24/7', 'Most restaurants have high chairs — say "kodomo isu arimasu ka?"', 'Trains: priority seats near doors, elevators at every station', 'Plan for 1-2 nap breaks per day — don\'t overschedule'] },
    { title: '🚫 No Pork Phrases', items: ['"Buta nashi de onegaishimasu" — No pork please', '"Buta wa taberaremasen" — I can\'t eat pork', '"Tori" = chicken, "Gyu" = beef, "Sakana" = fish, "Yasai" = vegetables', 'Many broths use pork (tonkotsu) — always ask about the soup base', 'Halal-certified restaurants: search "Halal Navi" app for nearby options'] },
    { title: '🌡️ Weather (Late May)', items: ['Expect 20–27°C (68–81°F) — warm and pleasant', 'Humidity starts to build — light, breathable clothing recommended', 'Rainy season (tsuyu) usually starts early-to-mid June — you should be fine', 'Bring a light rain jacket just in case — Japan\'s weather can surprise', 'Sunscreen and hats for the kids — the sun is strong even on cloudy days'] },
    { title: '📱 Essential Apps', items: ['Google Maps — works perfectly in Japan, shows train routes and times', 'Suica/PASMO (Apple Wallet) — tap-to-pay on trains and in stores', 'Google Translate — camera mode reads Japanese menus in real-time', 'Halal Navi — find pork-free/halal restaurants', 'Navitime — Japanese train schedules and route planning'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
