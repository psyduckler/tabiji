const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772555759586_b7ijpe',
  email: 'paulhblasjr@gmail.com',
  destination: 'Tokyo, Osaka, Kyoto',
  startDate: '2026-05-15',
  endDate: '2026-05-24',
  groupSize: 5,
  requests: 'NO PORK. No Gundam. 3 adults, 2 children (ages 3 and 2). Land at NRT May 15 ~1300. Shibuya Airbnb May 15-19, Tokyo until May 20, Osaka base for Kyoto/Nara day trips. Flying out of Osaka KIX. Matcha shops mornings, late-night eating/shopping after dinner. Adventure pace even with toddlers.'
};

const itineraryData = {
  destination: 'Tokyo, Osaka & Kyoto, Japan',
  countryEmoji: '🇯🇵',
  title: 'Tokyo to Osaka: A Family Adventure Across Japan',
  subtitle: '10 days of temples, teamLab, toddler-friendly eats & late-night ramen for 3 adults and 2 tiny explorers',
  description: "This itinerary packs Japan's three greatest cities into one epic family trip — from Shibuya's neon canyons and Asakusa's ancient temples to Kyoto's bamboo groves and Osaka's street food paradise. Every day is designed around toddler-friendly pacing with matcha mornings, big adventures by midday, and late-night eating and shopping after the kids' bedtime wind-down. All meals are pork-free, every route is stroller-tested, and every neighborhood is grouped for maximum efficiency with minimum meltdowns.",
  duration: '10 days',
  dates: 'May 15 – May 24, 2026',
  budget: '$$–$$$',
  pace: 'Adventurous',
  bestFor: 'Families with Toddlers',
  highlights: [
    'teamLab Planets — barefoot immersive art the whole family will love',
    'Sensō-ji Temple at golden hour with Skytree glowing in the background',
    'Character café marathon: Kirby, Miffy, Pokémon & Pikachu Sweets',
    'Fushimi Inari\'s thousand vermillion torii gates at sunrise',
    'Nara\'s friendly bowing deer in the park',
    'Late-night exploration of Golden Gai & Omoide Yokocho (pork-free!)',
    'Shibuya Sky sunset views over the Tokyo skyline',
    'Matcha-everything mornings across three cities'
  ],

  essentials: [
    { title: '🍜 No Pork, No Problem', text: 'Japan loves pork, but this itinerary is 100% pork-free. We\'ve selected restaurants with chicken, beef, seafood, and vegetable options. Key phrase to know: "Butaniku nashi de onegaishimasu" (ブタ肉なしでお願いします) — "No pork please." Also useful: "Buta wa taberaremasen" (豚は食べられません) — "I cannot eat pork." Many ramen shops offer chicken (tori) or seafood (gyokai) broths — just ask!' },
    { title: '👶 Stroller Strategy', text: 'Japan is surprisingly stroller-friendly. Train stations have elevators (look for エレベーター signs), and most major attractions are accessible. Bring a compact folding stroller — you\'ll fold it on trains during rush hour. Temples often have gravel paths so a lightweight stroller with bigger wheels helps. Baby changing stations are everywhere — even convenience stores.' },
    { title: '🚅 IC Cards & Trains', text: 'Get Suica or PASMO IC cards at any train station — they work on ALL trains, subways, and buses across Tokyo and Osaka. Tap-on, tap-off. Kids under 6 ride free. For the Tokyo→Osaka Shinkansen (bullet train), book reserved seats for space and comfort with the stroller.' },
    { title: '🌤️ May Weather', text: 'Mid-May is one of the best times to visit Japan — warm (20-25°C), low humidity, occasional rain. Cherry blossom season is over but everything is lush and green. Pack layers for temple visits and a compact rain jacket.' },
    { title: '🏪 Konbini Are Your Best Friend', text: 'Japanese convenience stores (7-Eleven, Lawson, FamilyMart) are incredible — fresh onigiri, bento boxes, snacks, diapers, drinks, ATMs, and even decent coffee. They\'re on every corner and open 24/7. Perfect for toddler emergencies.' },
    { title: '⏰ Matcha Mornings & Late Nights', text: 'This itinerary starts each morning with a matcha café or tea house, and ends with late-night shopping and eating options. Japan\'s cities are incredibly safe at night — Don Quijote stores are open until 2-5am, and many restaurants serve until midnight.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-05-15',
      neighborhoods: 'Narita · Shibuya · Ebisu',
      title: 'Touchdown Tokyo — Shibuya by Sunset',
      description: "Land at Narita around 1pm, grab your pocket WiFi, load up Suica cards, and take the Narita Express to Shibuya. Check into your Airbnb, shake off the jet lag with a walk through Shibuya Crossing, and catch sunset from Shibuya Sky. Ease into Tokyo with a gentle evening of convenience store snacks and neon-lit streets.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive at Narita & Travel to Shibuya',
              description: 'Clear immigration, pick up your pocket WiFi (reserve in advance from Global WiFi or Ninja WiFi), and buy Suica cards at the JR ticket machines. Take the Narita Express (N\'EX) direct to Shibuya Station — about 80 minutes.',
              details: [
                '✈️ Landing ~1:00pm, expect to clear customs by 2:00pm',
                '🚃 Narita Express to Shibuya — reserved seats, spacious, stroller-friendly',
                '💳 Suica cards: tap machines in English, load ¥3,000-5,000 each to start',
                '👶 Kids under 6 ride free on all trains!'
              ]
            },
            {
              title: 'Check Into Shibuya Airbnb & Settle In',
              description: 'Drop your bags, get oriented in the neighborhood. Hit a nearby konbini (convenience store) for water, snacks, and any toddler essentials you forgot to pack.',
              details: [
                '🏠 Shibuya Airbnb is your base for 4 nights (May 15-19)',
                '🏪 Lawson or FamilyMart — grab onigiri, milk, baby snacks',
                '💡 Pro tip: Japanese convenience stores have hot water for instant formula/meals'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Fight jet lag by staying awake until sunset. The neon lights of Shibuya will help keep everyone alert — even the toddlers will be mesmerized.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shibuya Crossing & Center-Gai',
              description: 'Walk to the world\'s busiest pedestrian crossing — Shibuya Scramble. Cross it with the kids (they\'ll love the chaos), then wander up Center-Gai street for your first taste of Tokyo\'s energy.',
              details: [
                '📸 Best photo spot: Shibuya Sky is even better, but the Starbucks overlooking the crossing works too',
                '🛍️ Center-Gai has character stores, arcades, and Don Quijote (open super late)'
              ]
            },
            {
              title: 'Shibuya Sky at Sunset',
              description: 'Take the elevator up 47 floors to Shibuya Sky — the open-air rooftop observation deck with 360° views of Tokyo. On a clear May evening, you can see Mt. Fuji. The sunset here is absolutely stunning.',
              details: [
                '🎫 Book tickets online in advance — ¥2,000/adult, free for kids under 3',
                '🌅 May sunset is around 6:30pm — arrive by 6pm',
                '📸 The edge seating area is Instagram gold',
                '👶 Stroller-friendly — elevator access to the top'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Afuri Ramen (Shibuya)',
              description: 'Famous yuzu shio (citrus salt) ramen — light, refreshing, and completely pork-free. Their chicken-based broth is one of Tokyo\'s best. Kids\' portions available.',
              meta: '💰 $$ · 📍 Shibuya · 🚫 Pork-free: chicken broth base · 👶 Kid-friendly'
            }
          ],
          tips: [
            { type: 'tip', text: 'Don Quijote in Shibuya (open until 2am) is perfect for late-night shopping after the kids fall asleep — one adult stays back while others explore. Snacks, souvenirs, weird gadgets, everything.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6595, lng: 139.7004, label: 'Shibuya Crossing', num: 1, cat: 'attraction', desc: 'World\'s busiest pedestrian crossing' },
        { lat: 35.6584, lng: 139.7022, label: 'Shibuya Sky', num: 2, cat: 'attraction', desc: '360° rooftop observation deck — sunset views' },
        { lat: 35.6609, lng: 139.6988, label: 'Don Quijote Shibuya', num: 3, cat: 'shopping', desc: 'Mega discount store open until 2am' },
        { lat: 35.6614, lng: 139.6989, label: 'Afuri Ramen', num: 4, cat: 'food', desc: 'Yuzu shio chicken ramen — no pork' }
      ]
    },
    {
      num: 2,
      date: '2026-05-16',
      neighborhoods: 'Harajuku · Meiji Jingu · Omotesando · Yoyogi Park',
      title: 'Matcha, Meiji Shrine & Harajuku\'s Kawaii Kingdom',
      description: "Start with matcha at a serene café near Meiji Jingu, then walk through the towering torii gate into one of Tokyo's most peaceful forests. Emerge into Harajuku's explosion of kawaii culture — Takeshita Street, character cafés, and Yoyogi Park for the kids to run free.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Matcha Morning at Café Reissue',
              description: 'Start the day right with matcha lattes and adorable latte art at Café Reissue in Harajuku. They\'ll draw cute characters on your drinks — the kids will be obsessed.',
              details: [
                '🍵 Known for their cute latte art — request characters!',
                '📍 Short walk from Harajuku Station',
                '👶 High chairs available, relaxed atmosphere'
              ]
            },
            {
              title: 'Meiji Jingu Shrine',
              description: 'Walk through the massive torii gate into the forested grounds of Meiji Jingu — Tokyo\'s most important Shinto shrine. The 70-hectare forest feels worlds away from the city. Write a wish on an ema (wooden plaque) and watch the kids marvel at the towering cypress trees.',
              details: [
                '⛩️ Free admission · Open sunrise to sunset',
                '🌳 The forest path is stroller-accessible (gravel but manageable)',
                '🙏 Cleanse hands at the temizuya (water fountain) — toddlers love this',
                '📸 The main torii gate is 12 meters tall — stunning photo op'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Meiji Jingu is best early morning when it\'s quiet and the light filters through the trees. Go before 10am to avoid crowds.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Yoyogi Park',
              description: 'Right next to Meiji Jingu, Yoyogi Park is Tokyo\'s best park for families. Let the toddlers run free on the grass, watch street performers, and enjoy a picnic under the trees. In May, the park is lush and green.',
              details: [
                '🌿 Huge open lawns — perfect for toddler energy burning',
                '🎵 Weekend street performers near the entrance',
                '🧸 Bring a blanket and snacks from the konbini'
              ]
            },
            {
              title: 'Takeshita Street & Harajuku Shopping',
              description: 'Dive into Harajuku\'s famous Takeshita Street — a narrow lane bursting with kawaii fashion, crêpe stands, character goods, and cotton candy bigger than your head. It\'s sensory overload in the best way.',
              details: [
                '🛍️ Brandy Melville — trendy fashion shop on this strip',
                '🍦 Giant rainbow cotton candy and crêpes everywhere',
                '📸 The entire street is an Instagram playground',
                '👶 Note: very crowded on weekends — stroller navigation is tight. Weekday is better. Consider a baby carrier.'
              ]
            },
            {
              title: 'Sakura Miffy Café',
              description: 'A few minutes from Takeshita Street, this adorable Miffy-themed café serves matcha and sakura-flavored treats shaped like the beloved bunny character. The kids will lose their minds.',
              details: [
                '🐰 Miffy-shaped pancakes, drinks, and desserts',
                '📍 Near Harajuku/Omotesando area',
                '📷 Everything is photogenic — even the bathroom'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Harajuku Gyoza-ro (Chicken Gyoza)',
              description: 'This popular gyoza shop has a chicken gyoza option that\'s crispy, juicy, and kid-approved. Quick, casual, and right off Takeshita Street.',
              meta: '💰 $ · 📍 Harajuku · 🚫 Order chicken (tori) gyoza — not pork · 👶 Fast and easy with kids'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Omotesando Avenue Stroll',
              description: 'Walk down Omotesando — Tokyo\'s Champs-Élysées. Tree-lined boulevard with luxury boutiques and stunning architecture. The Uniqlo flagship here is massive and has great kids\' clothing.',
              details: [
                '👕 Uniqlo Harajuku flagship — affordable Japanese fashion for the whole family',
                '🏛️ Gorgeous architecture: Tadao Ando\'s Omotesando Hills',
                '🌳 Wide sidewalks — very stroller-friendly'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Maisen Tonkatsu (Chicken Katsu)',
              description: 'Famous tonkatsu restaurant in a beautiful converted bathhouse. Order the chicken katsu (chikin katsu) instead of pork — it\'s crispy, tender perfection. Kids love the crunch.',
              meta: '💰 $$ · 📍 Omotesando · 🚫 Order CHICKEN katsu only — they have both · 👶 Set meals with rice and cabbage'
            }
          ],
          tips: [
            { type: 'tip', text: 'After dinner, the Omotesando tree-lined streets are beautifully lit at night and nearly empty. Great for a peaceful evening stroll with sleeping toddlers in the stroller.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6764, lng: 139.6993, label: 'Meiji Jingu', num: 1, cat: 'attraction', desc: 'Tokyo\'s most important Shinto shrine in a forested grove' },
        { lat: 35.6719, lng: 139.6947, label: 'Yoyogi Park', num: 2, cat: 'attraction', desc: 'Huge park — perfect for toddlers to run free' },
        { lat: 35.6706, lng: 139.7032, label: 'Takeshita Street', num: 3, cat: 'attraction', desc: 'Harajuku\'s iconic kawaii shopping street' },
        { lat: 35.6685, lng: 139.7069, label: 'Café Reissue', num: 4, cat: 'food', desc: 'Cute latte art café in Harajuku' },
        { lat: 35.6693, lng: 139.7043, label: 'Sakura Miffy Café', num: 5, cat: 'food', desc: 'Miffy-themed café with character treats' },
        { lat: 35.6652, lng: 139.7096, label: 'Omotesando', num: 6, cat: 'shopping', desc: 'Tokyo\'s luxury tree-lined boulevard' },
        { lat: 35.6655, lng: 139.7088, label: 'Uniqlo Harajuku', num: 7, cat: 'shopping', desc: 'Flagship store with great kids\' section' },
        { lat: 35.6688, lng: 139.7058, label: 'Brandy Melville', num: 8, cat: 'shopping', desc: 'Trendy fashion on Takeshita Street' },
        { lat: 35.6665, lng: 139.7101, label: 'Maisen', num: 9, cat: 'food', desc: 'Chicken katsu in a converted bathhouse' }
      ]
    },
    {
      num: 3,
      date: '2026-05-17',
      neighborhoods: 'Shinjuku · Shinjuku Gyoen · Kabukicho · Golden Gai',
      title: 'Shinjuku — Gardens, Godzilla & Golden Gai',
      description: "Today is all Shinjuku — one of Tokyo's most electrifying districts. Start with matcha in serene Shinjuku Gyoen garden, hunt for treasures at vintage shops and Don Quijote, see the famous 3D cat, then explore Kabukicho and Golden Gai after dark (yes, with kids — it's safe!).",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Matcha at Shinjuku Gyoen Tea House',
              description: 'Enter the tranquil Shinjuku Gyoen National Garden and head to the traditional Japanese tea house for ceremonial matcha and wagashi (Japanese sweets). The garden is enormous — 58 hectares of Japanese, English, and French gardens.',
              details: [
                '🍵 ¥500 entry + ¥700 for matcha set at the tea house',
                '🌿 Three distinct garden styles — the Japanese garden with koi pond is magical',
                '👶 Wide paths are very stroller-friendly',
                '⏰ Opens 9am — get there early for near-empty beauty'
              ]
            },
            {
              title: 'Shinjuku Gyoen Garden Exploration',
              description: 'After tea, explore the garden at your own pace. The greenhouse has tropical plants, there\'s a vast lawn for toddlers, and the Japanese pond garden is postcard-perfect. In May, the roses are in bloom.',
              details: [
                '🌹 Rose garden in peak bloom in May',
                '🌺 Greenhouse with tropical plants — great on a rainy day',
                '🦆 Koi fish in the pond — toddlers will be transfixed'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: '3D Cat Billboard at Cross Shinjuku Space',
              description: 'Head to Shinjuku Station East Exit to see the famous giant 3D calico cat on the Cross Shinjuku Space billboard. It meows, stretches, and looks incredibly real. The toddlers will go wild.',
              details: [
                '🐱 Best viewing: stand at the Shinjuku East Exit square',
                '📸 The cat appears on a loop — you\'ll catch it easily',
                '⏰ Runs throughout the day — best viewed from straight-on'
              ]
            },
            {
              title: 'SURUGA-YA & Seria (Shinjuku Marui Annex)',
              description: 'SURUGA-YA is a treasure trove of vintage anime figures, retro games, and collectibles. Seria (100-yen shop) in the same building is perfect for cheap souvenirs and adorable Japanese stationery.',
              details: [
                '🎮 SURUGA-YA: vintage games, anime figures, trading cards',
                '💯 Seria: everything ¥100 — great souvenirs, cute stationery, toys for kids',
                '📍 Both in Shinjuku Marui Annex building'
              ]
            },
            {
              title: 'Don Quijote Shinjuku',
              description: 'The flagship Don Quijote in Shinjuku is a multi-floor maze of everything — snacks, cosmetics, electronics, costumes, toys. Budget at least an hour because you WILL get lost in the best way.',
              details: [
                '🏬 Tax-free shopping with passport',
                '🍬 Entire floor of Japanese snacks and candy',
                '🧸 Kids\' toy section is enormous',
                '⏰ Open until 5am — perfect for late-night return trips'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Fuunji Tsukemen',
              description: 'Legendary tsukemen (dipping noodles) near Shinjuku Station. Rich seafood-based dipping broth with thick, chewy noodles. One of Shinjuku\'s most famous bowls.',
              meta: '💰 $ · 📍 Near Shinjuku South Exit · 🚫 Gyokai (fish) broth — no pork · 👶 Counter seating — may need to hold smaller kids'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Tokyo Metropolitan Government Building Observation Deck',
              description: 'FREE observation deck on the 45th floor with panoramic views of Tokyo. On clear May evenings, Mt. Fuji glows pink at sunset. The North Observation Deck is the one to visit.',
              details: [
                '🆓 Completely free admission',
                '🌅 Open until 11pm — perfect for sunset and night views',
                '📸 On a clear day, Mt. Fuji is visible to the west',
                '👶 Elevator up, stroller-friendly'
              ]
            },
            {
              title: 'Omoide Yokocho & Kabukicho',
              description: 'Walk through Omoide Yokocho ("Memory Lane") — narrow alleys of tiny yakitori stalls. Many have chicken (tori) skewers. Then head to Kabukicho, Tokyo\'s entertainment district, for the neon spectacle. The giant 3D screen and Godzilla head on the Hotel Gracery are unmissable.',
              details: [
                '🍢 Omoide Yokocho: order yakitori (chicken) skewers — specify "tori" (鳥)',
                '🦖 Godzilla head on Hotel Gracery Shinjuku — the kids will flip',
                '🎪 Kabuki Yokocho: themed food hall great for families',
                '🌃 The neon signs of Kabukicho are incredible at night — very safe area'
              ]
            },
            {
              title: 'Golden Gai (Quick Walk-Through)',
              description: 'A labyrinth of 200+ tiny bars in converted shacks, each seating 5-8 people. Walk through the alleys to soak in the atmosphere — it\'s like a movie set. Most bars welcome visitors; some charge a small seating fee.',
              details: [
                '🍸 Most bars open after 8pm',
                '📸 The alleys are incredibly photogenic',
                '👶 Walk through with kids for the atmosphere — the alleys are fascinating',
                '🌙 Come back later (adults only) for a proper drink at a bar'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Kabuki Yokocho Food Hall',
              description: 'Themed food hall in Kabukicho with multiple stalls — find chicken yakitori, seafood, udon, and more. Each stall is decorated in edo-period style. Great for families because everyone picks what they want.',
              meta: '💰 $$ · 📍 Kabukicho, Shinjuku · 🚫 Multiple stalls — easy to avoid pork · 👶 Casual, no-pressure family dining'
            }
          ],
          tips: [
            { type: 'tip', text: 'After dinner, one adult can head back to the Airbnb with the kids while others explore Golden Gai properly — tiny bars with fascinating themes (horror, jazz, 80s music, etc.). Cover charge is usually ¥500-1000.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6852, lng: 139.7100, label: 'Shinjuku Gyoen', num: 1, cat: 'attraction', desc: '58-hectare garden with tea house — matcha morning' },
        { lat: 35.6896, lng: 139.7006, label: 'Tokyo Metro Gov\'t Building', num: 2, cat: 'attraction', desc: 'FREE 45th-floor observation deck' },
        { lat: 35.6938, lng: 139.7035, label: '3D Cat Billboard', num: 3, cat: 'attraction', desc: 'Famous giant 3D cat at Cross Shinjuku Space' },
        { lat: 35.6929, lng: 139.7020, label: 'SURUGA-YA / Seria', num: 4, cat: 'shopping', desc: 'Vintage anime goods + ¥100 shop in Marui Annex' },
        { lat: 35.6944, lng: 139.7004, label: 'Don Quijote Shinjuku', num: 5, cat: 'shopping', desc: 'Multi-floor discount mega store' },
        { lat: 35.6926, lng: 139.6996, label: 'Omoide Yokocho', num: 6, cat: 'food', desc: 'Tiny alley of yakitori stalls — get chicken skewers' },
        { lat: 35.6942, lng: 139.7036, label: 'Golden Gai', num: 7, cat: 'attraction', desc: '200+ tiny themed bars in narrow alleys' },
        { lat: 35.6945, lng: 139.7028, label: 'Kabukicho', num: 8, cat: 'attraction', desc: 'Neon entertainment district with Godzilla head' },
        { lat: 35.6933, lng: 139.7028, label: 'Kabuki Yokocho', num: 9, cat: 'food', desc: 'Edo-themed food hall in Kabukicho' },
        { lat: 35.6889, lng: 139.6992, label: 'Fuunji', num: 10, cat: 'food', desc: 'Legendary seafood tsukemen — no pork' }
      ]
    },
    {
      num: 4,
      date: '2026-05-18',
      neighborhoods: 'Asakusa · Sumida · Tokyo Skytree · Oyokogawa',
      title: 'Ancient Temples, Skytree & River Park',
      description: "Step back in time at Sensō-ji — Tokyo's oldest temple — then rocket to the future at Tokyo Skytree. This east-Tokyo day combines the spiritual with the spectacular, with a peaceful riverside park for the toddlers to stretch their legs.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Matcha & Ichigo Daifuku at Asakusa',
              description: 'Start with matcha and the iconic ichigo daifuku (strawberry mochi) from one of the traditional sweet shops along Nakamise-dori. Funawa or Umezono are excellent choices near the temple.',
              details: [
                '🍓 Ichigo daifuku: fresh strawberry wrapped in mochi and red bean paste',
                '🍵 Matcha sets available at traditional tea shops along the approach',
                '⏰ Get to Asakusa by 8:30am — Sensō-ji is magical before the crowds'
              ]
            },
            {
              title: 'Sensō-ji Temple',
              description: 'Tokyo\'s oldest and most visited temple (built 645 AD). Walk through the massive Kaminarimon ("Thunder Gate") with its iconic red lantern, browse Nakamise-dori shopping street, and explore the main hall. The incense burner is said to bring good health — waft the smoke over the kids!',
              details: [
                '⛩️ Kaminarimon gate → Nakamise-dori → Hōzōmon gate → Main Hall',
                '🛍️ Nakamise-dori: 90 shops selling traditional snacks, toys, fans, and souvenirs',
                '👶 Wide approach is stroller-friendly; main hall has steps but you can view from below',
                '📸 Best photo: the pagoda with Skytree behind it'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tokyo Skytree',
              description: 'The world\'s tallest tower (634m) is a short walk from Asakusa across the Sumida River. Take the elevator to the Tembo Deck (350m) or Tembo Gallery (450m) for staggering views of Tokyo stretching to the horizon.',
              details: [
                '🗼 ¥2,100/adult for Tembo Deck, ¥3,100 combo with Gallery',
                '👶 Kids under 3 free! Stroller-friendly with elevators',
                '📸 On a clear day you can see Mt. Fuji',
                '🛍️ Tokyo Solamachi mall at the base has great shopping and restaurants'
              ]
            },
            {
              title: 'Oyokogawa Shinsui Park',
              description: 'A hidden gem — this restored waterway park near Skytree has shallow wading areas, little bridges, and cherry trees along a peaceful canal path. Perfect for toddlers to splash and play.',
              details: [
                '💧 Shallow water areas safe for toddlers to wade in',
                '🌳 Shaded walking path along the canal',
                '🆓 Free and rarely crowded — a locals\' secret',
                '👶 Bring a change of clothes for the kids — they WILL get wet'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Sometaro Okonomiyaki',
              description: 'Cook your own okonomiyaki (savory Japanese pancake) on a tabletop grill at this charming 1937-era house in Asakusa. Get the seafood or mixed vegetable version — the kids will love watching the cooking.',
              meta: '💰 $ · 📍 Asakusa · 🚫 Order seafood (gyokai) or veggie — skip the pork options · 👶 Fun interactive dining for families'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Asakusa at Night & Sensō-ji Illuminated',
              description: 'Return to Sensō-ji at night — the temple is beautifully illuminated and almost empty compared to daytime. The five-story pagoda glows against the night sky. Walk along the Sumida River for Skytree\'s changing LED colors reflected in the water.',
              details: [
                '🌙 Temple grounds are open 24/7 — the main hall closes but the grounds are peaceful',
                '💡 Skytree changes color nightly — beautiful from the Sumida River banks',
                '📸 Night photos of the illuminated temple + Skytree are spectacular'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Tsukishima Monja Street',
              description: 'Take the subway to Tsukishima for monjayaki — Tokyo\'s signature griddle dish. It\'s like a runny, crispy savory pancake you scrape off the grill with tiny spatulas. Completely unique and fun for families.',
              meta: '💰 $$ · 📍 Tsukishima · 🚫 Seafood and veggie options — specify no pork · 👶 Interactive cooking — kids love scraping the grill'
            }
          ],
          tips: [
            { type: 'tip', text: 'Tsukiji Fish Market outer market area (just one stop from Tsukishima) is also great for late snacks — tamagoyaki (sweet egg) on a stick, fresh fruit, and seafood skewers.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: 'Sensō-ji Temple', num: 1, cat: 'attraction', desc: 'Tokyo\'s oldest temple — 645 AD' },
        { lat: 35.7101, lng: 139.8107, label: 'Tokyo Skytree', num: 2, cat: 'attraction', desc: 'World\'s tallest tower — 634m views' },
        { lat: 35.7147, lng: 139.7945, label: 'Kaminarimon Gate', num: 3, cat: 'attraction', desc: 'Iconic Thunder Gate at Sensō-ji entrance' },
        { lat: 35.7060, lng: 139.8150, label: 'Oyokogawa Shinsui Park', num: 4, cat: 'attraction', desc: 'Canal park with wading areas for toddlers' },
        { lat: 35.7139, lng: 139.7969, label: 'Nakamise-dori', num: 5, cat: 'shopping', desc: '90 traditional souvenir shops to the temple' },
        { lat: 35.7125, lng: 139.7946, label: 'Sometaro', num: 6, cat: 'food', desc: 'DIY okonomiyaki in a 1937 house' },
        { lat: 35.6625, lng: 139.7767, label: 'Tsukishima Monja Street', num: 7, cat: 'food', desc: 'Tokyo\'s monjayaki griddle district' }
      ]
    },
    {
      num: 5,
      date: '2026-05-19',
      neighborhoods: 'Ikebukuro · Sunshine City · Toyosu · Odaiba',
      title: 'Pokémon, Kirby & teamLab Planets',
      description: "Today is pure fun — character cafés and stores in Ikebukuro, then the immersive wonder of teamLab Planets. This is the day the kids (and adults) will talk about forever. End with a soak at Toyosu Manyo Club onsen if energy remains.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Matcha & Donguri Kyowakoku (Ghibli Store)',
              description: 'Head to Ikebukuro\'s Donguri Kyowakoku — the official Studio Ghibli merchandise store. Totoro plushies, Kiki\'s Delivery Service bags, Spirited Away chopstick sets. Grab a matcha from a nearby café while browsing.',
              details: [
                '🍵 Grab matcha at any nearby café or Starbucks Reserve in Ikebukuro',
                '🧸 Donguri Kyowakoku has Ghibli goods you can\'t find outside Japan',
                '📍 Located in Sunshine City Alpa or nearby — check location',
                '👶 Totoro plushies are irresistible — budget for souvenirs here'
              ]
            },
            {
              title: 'Sunshine City Complex',
              description: 'Sunshine City is a massive entertainment/shopping complex in Ikebukuro with an aquarium, observatory, and tons of shops. The Sunshine Aquarium on the roof is particularly fun for toddlers — penguins appear to fly through the sky!',
              details: [
                '🐧 Sunshine Aquarium: rooftop marine park with sky penguins',
                '🛍️ Shopping mall with kids\' stores and food court',
                '🎮 Namco amusement area for older kids',
                '👶 Indoor and stroller-friendly throughout'
              ]
            },
            {
              title: 'Pokémon Center Mega Tokyo & Pikachu Sweets',
              description: 'The biggest Pokémon Center in Tokyo is in Sunshine City. Plus the adjacent Pikachu Sweets café serves Pikachu-shaped pastries and desserts. This is Pokémon paradise.',
              details: [
                '⚡ Exclusive Tokyo Pokémon merch not sold elsewhere',
                '🧁 Pikachu Sweets: character-shaped cakes, cookies, and drinks',
                '📍 Sunshine City, Ikebukuro',
                '👶 Very family-friendly — expect to spend 30-60 mins browsing'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Kirby Café Tokyo',
              description: 'A must-visit character café where every dish is Kirby-themed. Reserve online (reservations required!) for adorable Kirby-shaped curry, pasta, and desserts. The attention to detail is unreal.',
              meta: '💰 $$$ · 📍 Tokyo Solamachi (near Skytree) · ⚠️ MUST reserve online in advance · 🚫 Multiple non-pork options on menu · 👶 Dream come true for kids'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Character Store Marathon: One Piece & Naruto',
              description: 'Ikebukuro\'s Sunshine City area has the official One Piece Mugiwara Store and Naruto/Boruto store nearby. Browse exclusive merchandise, take photos with character statues, and pick up souvenirs.',
              details: [
                '🏴‍☠️ One Piece Store: Mugiwara Store in Shibuya PARCO or Sunshine City',
                '🍥 Naruto Store: exclusive shuriken keychains, Akatsuki cloaks',
                '📍 Both in or near Sunshine City / Ikebukuro area',
                '🛍️ Great for older anime fans in the group'
              ]
            },
            {
              title: 'teamLab Planets TOKYO DMM',
              description: 'The highlight of the trip. teamLab Planets is an immersive barefoot walk through water, flowers, light, and infinity. You wade knee-deep through warm water, walk through waterfalls of light, and float in an infinite universe. It\'s mind-blowing for all ages.',
              details: [
                '🎫 Book online in advance — sells out! ¥3,800/adult, kids under 3 free',
                '👣 Barefoot experience — roll up pants, leave shoes in lockers',
                '💧 You walk through knee-deep warm water (towels provided)',
                '👶 Toddlers LOVE the water rooms and light installations',
                '📸 Some of the most incredible photos you\'ll ever take',
                '⏰ Allow 2-3 hours for the full experience',
                '📍 Toyosu area — take the Yurikamome line'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Bring a change of pants for teamLab — you WILL get wet up to the knees. Shorts or rolled-up pants work best. They provide towels but not clothes. Kids will want to splash everything.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Toyosu Manyo Club (Optional Onsen)',
              description: 'A 24-hour onsen (hot spring) spa right near teamLab Planets. If the kids are still going, the foot baths and family-friendly areas are great. Otherwise, head back to Shibuya for last-night shopping.',
              details: [
                '♨️ Natural hot spring water from Hakone',
                '👶 Family-friendly areas available',
                '🌙 Open 24 hours — could even go super late',
                '💡 Alternative: head back to Shibuya for last-night Don Quijote run'
              ]
            },
            {
              title: 'Shibuya Last Night — Character Store Marathon',
              description: 'Your last night in Shibuya! Hit up any character stores you missed — Shibuya has clusters of anime, Ghibli, and character shops. Shibuya 109 and the surrounding streets are packed with options.',
              details: [
                '🛍️ Shibuya PARCO: Nintendo Store, Pokémon Center, Capcom Store',
                '🏬 Shibuya 109: trendy fashion and character goods',
                '📍 All within walking distance of your Airbnb',
                '🌙 Many shops open until 9-10pm, Don Quijote until 2am'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Nabezo Shibuya (Shabu-Shabu)',
              description: 'All-you-can-eat shabu-shabu (Japanese hot pot) — choose beef, chicken, or seafood with fresh vegetables. Perfect family meal: everyone cooks together at the table. Kids love dipping ingredients in the bubbling broth.',
              meta: '💰 $$ · 📍 Shibuya · 🚫 Beef & chicken options — no pork needed · 👶 Interactive cooking kids love + private booth seating'
            }
          ],
          tips: [
            { type: 'tip', text: 'This is your last night at the Shibuya Airbnb — pack what you can tonight. Tomorrow you\'ll move to another Tokyo hotel briefly before heading to Osaka on the 20th.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7295, lng: 139.7190, label: 'Sunshine City', num: 1, cat: 'attraction', desc: 'Massive complex — aquarium, shops, Pokémon Center' },
        { lat: 35.7295, lng: 139.7190, label: 'Pokémon Center Mega Tokyo', num: 2, cat: 'shopping', desc: 'Biggest Pokémon store in Tokyo' },
        { lat: 35.7290, lng: 139.7188, label: 'Donguri Kyowakoku', num: 3, cat: 'shopping', desc: 'Official Studio Ghibli merchandise store' },
        { lat: 35.7290, lng: 139.7195, label: 'One Piece Store', num: 4, cat: 'shopping', desc: 'Official Mugiwara Store' },
        { lat: 35.7290, lng: 139.7200, label: 'Naruto Store', num: 5, cat: 'shopping', desc: 'Official Naruto/Boruto merchandise' },
        { lat: 35.6499, lng: 139.7880, label: 'teamLab Planets', num: 6, cat: 'attraction', desc: 'Immersive barefoot art — walk through water and light' },
        { lat: 35.6465, lng: 139.7905, label: 'Toyosu Manyo Club', num: 7, cat: 'attraction', desc: '24-hour onsen spa near teamLab' },
        { lat: 35.7101, lng: 139.8107, label: 'Kirby Café', num: 8, cat: 'food', desc: 'Kirby-themed café — must reserve ahead' },
        { lat: 35.6595, lng: 139.7004, label: 'Nabezo Shibuya', num: 9, cat: 'food', desc: 'All-you-can-eat shabu-shabu hot pot' }
      ]
    },
    {
      num: 6,
      date: '2026-05-20',
      neighborhoods: 'Tsukiji · Hie-jinja · Gōtokuji · Osaka (Shin-Osaka)',
      title: 'Last Tokyo Bites & Bullet Train to Osaka',
      description: "Cram in the final Tokyo must-sees: Tsukiji Fish Market for breakfast, the cat temple Gōtokuji, and the hidden Hie-jinja shrine. Then board the Shinkansen bullet train and rocket to Osaka at 300km/h — the kids will love it.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tsukiji Outer Market Breakfast',
              description: 'The legendary Tsukiji outer market is still thriving with 400+ stalls selling the freshest seafood, tamagoyaki (sweet egg omelette), fresh fruit, and street food. This is Tokyo\'s greatest food adventure.',
              details: [
                '🐟 Must-try: fresh sashimi, tamagoyaki on a stick, grilled scallops',
                '🍣 Sushi Dai-style fresh sushi for breakfast — no pork anywhere here',
                '🍓 Fresh fruit skewers and melon slices — toddler favorites',
                '⏰ Best 7-10am — get there early for the best stalls',
                '👶 Stroller works on main streets, carry kids in narrow alleys'
              ]
            },
            {
              title: 'Hie-jinja Shrine',
              description: 'A beautiful hilltop shrine in Akasaka with a stunning tunnel of vermillion torii gates (like a mini Fushimi Inari!). Less crowded and more intimate than the big shrines.',
              details: [
                '⛩️ Row of torii gates along the hillside staircase — very photogenic',
                '🐒 Sacred monkey statues — the kids will love them',
                '📍 Near Akasaka-Mitsuke Station',
                '👶 Main shrine area is stroller-accessible via a side path (skip the stairs)'
              ]
            }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Gōtokuji Temple (Cat Temple)',
              description: 'The "cat temple" is covered in thousands of maneki-neko (beckoning cat) figurines — shelves upon shelves of white lucky cats with raised paws. It\'s surreal, beautiful, and toddlers will be obsessed with finding the biggest and smallest cats.',
              details: [
                '🐱 Buy a small maneki-neko (¥300-3000) and leave it as an offering, or take it home',
                '📍 Setagaya area — a bit out of the way but absolutely worth it',
                '📸 Thousands of cat figurines on shelves — incredible photo opportunity',
                '👶 Peaceful temple grounds, easy to walk with strollers'
              ]
            },
            {
              title: 'Bokksu Market (If Time Permits)',
              description: 'If time allows before your train, swing by for curated Japanese snack boxes and artisan treats — great souvenirs to take home.',
              details: [
                '📦 Curated boxes of Japanese snacks from small makers',
                '🛍️ Pre-packaged and easy to travel with'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Ekiben (Train Bento) from Tokyo Station',
              description: 'Buy beautiful ekiben (train station bento boxes) from the shops in Tokyo Station before boarding the Shinkansen. The variety is incredible — choose from seafood, chicken, and mixed bento. Eating a fancy bento on the bullet train is a quintessential Japanese experience.',
              meta: '💰 $$ · 📍 Tokyo Station · 🚫 Look for tori (chicken), sake (salmon), or ebi (shrimp) bento — avoid tonkatsu · 👶 Kids love picking from a colorful bento box'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shinkansen to Osaka!',
              description: 'Board the Tokaido Shinkansen at Tokyo Station heading to Shin-Osaka. The Nozomi is the fastest (2 hours 15 minutes). Book reserved seats for space — the kids will be glued to the window watching Japan blur past at 300km/h. Mt. Fuji appears on the right side about 40 minutes in!',
              details: [
                '🚅 Nozomi: 2h15m Tokyo→Shin-Osaka · Book reserved seats (Green Car for luxury)',
                '🗻 Sit on the RIGHT side (seats D/E) for Mt. Fuji views around Shin-Fuji Station',
                '👶 Reserved seats have more legroom for strollers; Green Car has extra space',
                '🍱 Eat your ekiben on the train — it\'s a tradition!'
              ]
            },
            {
              title: 'Check Into Osaka Hotel & Explore Namba',
              description: 'Arrive at Shin-Osaka, take the subway to your Osaka hotel (Namba or Shinsaibashi area recommended). Drop bags and head out to explore the immediate neighborhood.',
              details: [
                '🏨 Osaka is your base for 4 nights (May 20-24)',
                '📍 Namba/Shinsaibashi area: central, walkable, tons of food and shopping',
                '🌃 Dotonbori is within walking distance — save it for tonight!'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dotonbori Night Walk',
              description: 'Welcome to Osaka! Dotonbori is the city\'s iconic entertainment and street food strip along the canal. Neon signs, the famous Glico Running Man, and the most incredible street food in Japan. Just walk, eat, and soak it all in.',
              details: [
                '🏃 The Glico Running Man sign — Osaka\'s most famous photo spot',
                '🦀 Giant moving crab sign, blowfish lanterns, dragon sculptures',
                '🌊 Canal-side walking is stroller-friendly and gorgeous at night',
                '📸 The neon reflections on the canal water are magical'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Dotonbori Street Food Crawl',
              description: 'Osaka is Japan\'s street food capital. Graze your way through Dotonbori: takoyaki (octopus balls), chicken karaage, yakitori, kushikatsu (deep-fried skewers — get chicken/shrimp/veggie), and finish with a crepe. Pure deliciousness.',
              meta: '💰 $ · 📍 Dotonbori · 🚫 Takoyaki, chicken karaage, ebi kushikatsu — all pork-free · 👶 Street food is perfect for picky toddlers — try a little of everything'
            }
          ],
          tips: [
            { type: 'tip', text: 'Osaka people say "kuidaore" — eat until you drop. This city is about food above all else. Let the street food crawl be dinner — no need for a sit-down restaurant tonight.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6654, lng: 139.7707, label: 'Tsukiji Outer Market', num: 1, cat: 'food', desc: '400+ stalls of fresh seafood and street food' },
        { lat: 35.6762, lng: 139.7408, label: 'Hie-jinja Shrine', num: 2, cat: 'attraction', desc: 'Hilltop shrine with torii gate tunnel' },
        { lat: 35.6458, lng: 139.6373, label: 'Gōtokuji Temple', num: 3, cat: 'attraction', desc: 'Cat temple — thousands of maneki-neko figurines' },
        { lat: 35.6812, lng: 139.7671, label: 'Tokyo Station', num: 4, cat: 'transport', desc: 'Shinkansen departure + ekiben bento shops' },
        { lat: 34.6685, lng: 135.5013, label: 'Dotonbori', num: 5, cat: 'attraction', desc: 'Osaka\'s iconic neon-lit street food strip' },
        { lat: 34.6687, lng: 135.5020, label: 'Glico Running Man', num: 6, cat: 'attraction', desc: 'Osaka\'s most famous photo spot' }
      ]
    },
    {
      num: 7,
      date: '2026-05-21',
      neighborhoods: 'Kyoto: Fushimi · Gion · Nishiki Market · Higashiyama',
      title: 'Kyoto Day Trip — Torii Gates, Geisha Streets & Tea',
      description: "Take the train from Osaka to Kyoto (30 min) for a day of ancient beauty. Start with the otherworldly Fushimi Inari torii gates, sip ceremonial matcha at a traditional tea house, explore Gion's geisha district, and graze through Nishiki Market.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Train to Kyoto & Fushimi Inari Taisha',
              description: 'Take the JR Special Rapid from Osaka to Kyoto (30 min), then one stop on the JR Nara Line to Inari Station. Fushimi Inari\'s thousands of vermillion torii gates climbing up Mt. Inari are Japan\'s most iconic image. Go early to beat the crowds.',
              details: [
                '⛩️ Free admission, open 24 hours',
                '🏔️ Full hike to the top: 2-3 hours. With toddlers: do the first 20-30 min section — still spectacular',
                '📸 The tunnel of gates is most photogenic in the lower section',
                '👶 Stroller works for the flat lower section; carrier recommended for the uphill parts',
                '⏰ Arrive by 8:30am — the morning light through the gates is ethereal'
              ]
            },
            {
              title: 'Rokujuan Tea House',
              description: 'After the shrine, visit Rokujuan (or a nearby traditional tea house) for ceremonial matcha and Japanese sweets. Sit on tatami mats and watch the tea ceremony — a moment of pure zen after the hike.',
              details: [
                '🍵 Ceremonial matcha with seasonal wagashi',
                '📍 Near Fushimi Inari area',
                '👶 Tatami seating — toddlers can sit on the floor (they\'ll love it)'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nishiki Market',
              description: 'Kyoto\'s 400-year-old "Kitchen of Kyoto" — a narrow covered market stretching 5 blocks with 100+ stalls selling pickles, mochi, matcha everything, fresh tofu, dango, and seasonal delicacies. The best food market in Japan.',
              details: [
                '🛒 5 blocks long — take your time browsing and tasting',
                '🍡 Must-try: fresh dango (rice dumplings), matcha soft serve, pickled vegetables',
                '🐟 Fresh sashimi, grilled seafood skewers, tamagoyaki',
                '👶 Narrow aisles — consider a baby carrier over stroller here',
                '📍 Between Shijo and Nishikikoji streets'
              ]
            },
            {
              title: 'Gion District Walk',
              description: 'Kyoto\'s famous geisha (geiko) district. Walk along Hanami-koji — the photogenic stone-paved street lined with traditional wooden machiya houses, tea houses, and restaurants. You might spot a maiko (apprentice geisha) heading to an evening appointment.',
              details: [
                '👘 Best chance to see maiko: late afternoon (4-6pm) as they head to engagements',
                '📸 Hanami-koji is the most photographed street in Kyoto',
                '🏘️ The side streets are even more atmospheric and less crowded',
                '👶 Flat stone-paved streets are stroller-accessible'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Nishiki Market Grazing',
              description: 'Skip a sit-down lunch — just graze your way through Nishiki Market. Fresh dango, grilled mochi, seafood skewers, and matcha treats. This IS lunch, and it\'s better than any restaurant.',
              meta: '💰 $ · 📍 Nishiki Market · 🚫 Almost everything here is pork-free — seafood and veggie dominant · 👶 Perfect for toddlers — constant small bites'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Yasaka Shrine & Maruyama Park',
              description: 'At the east end of Gion, Yasaka Shrine leads into Maruyama Park — Kyoto\'s most popular park. In May it\'s lush and green with a beautiful pond. Let the kids run around before heading back to Osaka.',
              details: [
                '⛩️ Yasaka Shrine is free and beautifully lit at night',
                '🌳 Maruyama Park has open lawns — great for toddler energy release',
                '🚃 Head back to Osaka from Gion-Shijo Station (Keihan Line) — 50 min'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Gion Owatari',
              description: 'Elegant kaiseki-inspired dinner in Gion — seasonal Kyoto cuisine with beautiful presentation. They offer chicken and fish courses. The atmosphere in a traditional machiya is unforgettable.',
              meta: '💰 $$$ · 📍 Gion, Kyoto · 🚫 Request no-pork kaiseki — fish and chicken courses available · 👶 Tatami room seating — reserve a private room for the family'
            }
          ],
          tips: [
            { type: 'tip', text: 'Alternative dinner: head back to Osaka and hit up Shinsekai district for kushikatsu (deep-fried skewers). Get chicken, shrimp, and veggie skewers — it\'s Osaka\'s signature dish and very kid-friendly.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari Taisha', num: 1, cat: 'attraction', desc: 'Thousands of vermillion torii gates up Mt. Inari' },
        { lat: 34.9668, lng: 135.7718, label: 'Rokujuan Tea House', num: 2, cat: 'food', desc: 'Ceremonial matcha near Fushimi Inari' },
        { lat: 35.0050, lng: 135.7650, label: 'Nishiki Market', num: 3, cat: 'food', desc: 'Kyoto\'s 400-year-old covered food market' },
        { lat: 35.0037, lng: 135.7756, label: 'Gion District', num: 4, cat: 'attraction', desc: 'Historic geisha district with traditional machiya' },
        { lat: 35.0036, lng: 135.7786, label: 'Yasaka Shrine', num: 5, cat: 'attraction', desc: 'Beautiful shrine at the entrance to Maruyama Park' },
        { lat: 35.0039, lng: 135.7807, label: 'Maruyama Park', num: 6, cat: 'attraction', desc: 'Kyoto\'s most popular park — let the kids run' },
        { lat: 35.0034, lng: 135.7758, label: 'Gion Owatari', num: 7, cat: 'food', desc: 'Kaiseki dinner in a traditional machiya' }
      ]
    },
    {
      num: 8,
      date: '2026-05-22',
      neighborhoods: 'Nara · Osaka: Shinsekai · Tennoji',
      title: 'Nara\'s Bowing Deer & Osaka\'s Retro Soul',
      description: "Day trip to Nara — where over 1,000 sacred deer roam free and bow to you for crackers. The kids will be in absolute heaven. Return to Osaka for the retro charm of Shinsekai and Tsutenkaku Tower.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Train to Nara & Nara Park',
              description: 'Take the Kintetsu Railway from Namba to Nara (35 min). Walk from Kintetsu Nara Station into Nara Park — within minutes you\'ll be surrounded by friendly deer. Buy shika senbei (deer crackers, ¥200) and watch the deer literally bow to you before eating. This is the highlight of the trip for most kids.',
              details: [
                '🦌 Over 1,000 free-roaming deer — they bow when you hold up a cracker!',
                '🍘 Shika senbei (deer crackers) sold by vendors throughout the park — ¥200/pack',
                '👶 IMPORTANT: Hold crackers high — deer can be pushy. Keep toddlers close and feed deer together',
                '📸 The deer are very photogenic — they\'ll pose with the kids',
                '⏰ Arrive by 9:30am for calmer deer (they get more aggressive as the day goes on)'
              ]
            },
            {
              title: 'Todai-ji Temple',
              description: 'Home to the world\'s largest bronze Buddha (15 meters tall!) inside the world\'s largest wooden building. Walking through the main gate and seeing the Daibutsu for the first time is jaw-dropping. The kids can try to squeeze through the "Buddha\'s nostril" pillar hole for good luck.',
              details: [
                '🏛️ ¥600/adult, ¥300/child · Kids under 6 free',
                '🗿 The Great Buddha (Daibutsu) is 15m tall and 500 tons of bronze',
                '🕳️ Pillar hole challenge: squeeze through for enlightenment in your next life!',
                '👶 Flat grounds are stroller-accessible'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Kakinoha Sushi (Nara Specialty)',
              description: 'Nara\'s signature dish: pressed sushi wrapped in persimmon leaves. The leaves add a subtle, sweet fragrance. Typically made with mackerel or salmon — delicate, beautiful, and unique to this region.',
              meta: '💰 $$ · 📍 Nara · 🚫 Fish-based — no pork · 👶 Mild flavors kids tend to like'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nara\'s Side Streets & Mochi Shops',
              description: 'Walk through Naramachi — the old merchant quarter with traditional machiya houses, craft shops, and mochi tea houses. Pick up freshly made warabi mochi or yomogi mochi (mugwort rice cake) as an afternoon treat.',
              details: [
                '🍡 Fresh mochi shops everywhere — try different flavors',
                '🏘️ Naramachi has beautiful preserved merchant houses',
                '🛍️ Deer-themed souvenirs: deer plushies, deer socks, deer cookies',
                '👶 Flat streets, easy strolling'
              ]
            },
            {
              title: 'Return to Osaka & Shinsekai',
              description: 'Head back to Osaka and explore Shinsekai — Osaka\'s retro entertainment district modeled after Paris and New York in the early 1900s. The Tsutenkaku Tower has an observation deck, and the streets below are filled with kushikatsu restaurants and vintage game arcades.',
              details: [
                '🗼 Tsutenkaku Tower: ¥900/adult — panoramic Osaka views',
                '🎮 Retro arcade games in the streets below',
                '🏮 The neon-lit streets at night are incredibly atmospheric',
                '👶 Flat, walkable area — stroller-friendly'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Don Quijote Osaka & Late-Night Shopping',
              description: 'Hit up Don Quijote in Dotonbori for more snack shopping and souvenirs. Osaka\'s Don Quijote has the famous Ferris wheel on the building — ride it for canal views at night!',
              details: [
                '🎡 Don Quijote Dotonbori has a Ferris wheel ON the building!',
                '🛍️ Tax-free shopping with passport',
                '🌙 Open until 5am',
                '👶 The Ferris wheel is gentle — toddlers will enjoy the lights'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Daruma Kushikatsu (Shinsekai)',
              description: 'Shinsekai is the birthplace of kushikatsu — deep-fried skewers. Daruma is the most famous shop. Get chicken, shrimp, asparagus, lotus root, and cheese skewers. Dip once in the communal sauce (no double-dipping! It\'s the rule).',
              meta: '💰 $ · 📍 Shinsekai · 🚫 Chicken, shrimp, veggie skewers — specify no pork · 👶 Fun finger food for kids — easy to share'
            }
          ],
          tips: [
            { type: 'tip', text: 'Surugaya (vintage anime/game shop) has a branch in Osaka — check Nipponbashi/Den Den Town area if you want more anime shopping. It\'s Osaka\'s answer to Akihabara.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6851, lng: 135.8430, label: 'Nara Park', num: 1, cat: 'attraction', desc: '1,000+ free-roaming deer that bow for crackers' },
        { lat: 34.6890, lng: 135.8399, label: 'Todai-ji Temple', num: 2, cat: 'attraction', desc: 'World\'s largest bronze Buddha in world\'s largest wooden building' },
        { lat: 34.6783, lng: 135.8310, label: 'Naramachi', num: 3, cat: 'attraction', desc: 'Old merchant quarter with mochi shops and crafts' },
        { lat: 34.6523, lng: 135.5063, label: 'Shinsekai', num: 4, cat: 'attraction', desc: 'Retro entertainment district — kushikatsu capital' },
        { lat: 34.6525, lng: 135.5063, label: 'Tsutenkaku Tower', num: 5, cat: 'attraction', desc: 'Osaka\'s retro tower with observation deck' },
        { lat: 34.6520, lng: 135.5058, label: 'Daruma Kushikatsu', num: 6, cat: 'food', desc: 'Shinsekai\'s most famous deep-fried skewers' },
        { lat: 34.6688, lng: 135.5015, label: 'Don Quijote Dotonbori', num: 7, cat: 'shopping', desc: 'Mega store with Ferris wheel on the building' }
      ]
    },
    {
      num: 9,
      date: '2026-05-23',
      neighborhoods: 'Osaka: Osaka Castle · Umeda · Amerikamura',
      title: 'Osaka Castle, Shopping & Final Feast',
      description: "Your last full day! Explore Osaka Castle and its beautiful park, check out teamLab if available, do final shopping in Umeda or Amerikamura, and have one last incredible Osaka dinner. Make it count!",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Matcha Morning near Osaka Castle',
              description: 'Start with matcha at a café near Osaka Castle before exploring the grounds. The castle park is gorgeous in May — green lawns, moats with turtles, and plum groves.',
              details: [
                '🍵 Several cafés in Osaka Business Park near the castle',
                '🌿 The castle grounds are massive — great morning walk'
              ]
            },
            {
              title: 'Osaka Castle & Park',
              description: 'Osaka\'s most famous landmark — a towering white and gold castle surrounded by huge stone walls and moats. The interior is a museum about Toyotomi Hideyoshi and Osaka\'s history. The top floor observation deck has panoramic city views.',
              details: [
                '🏯 ¥600/adult, kids free · Opens 9am',
                '📸 Best photo from the southwest corner with the moat reflection',
                '🐢 The moat has turtles — toddlers will be mesmerized',
                '👶 Elevator inside to the top floor (stroller-friendly)',
                '🌳 The park around the castle is perfect for the kids to run'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'teamLab Botanical Garden Osaka (If Available)',
              description: 'If teamLab\'s Osaka installation is running, it\'s a nighttime botanical garden experience. Check availability — it\'s different from teamLab Planets in Tokyo and equally stunning.',
              details: [
                '🌺 Interactive light installations in a real botanical garden',
                '🎫 Check teamlab.art for current Osaka exhibitions',
                '👶 Outdoor, stroller-friendly paths',
                '💡 Alternative if not available: Osaka Aquarium Kaiyukan — massive aquarium the kids will love'
              ]
            },
            {
              title: 'Amerikamura & Shinsaibashi Shopping',
              description: 'Osaka\'s answer to Harajuku — Amerikamura (American Village) is a trendy shopping district with vintage clothes, street art, and great cafés. Shinsaibashi-suji shopping arcade runs from here all the way to Namba.',
              details: [
                '🛍️ Shinsaibashi-suji: covered arcade stretching 600m — rain or shine shopping',
                '👕 Vintage shops, sneaker stores, Japanese streetwear',
                '🍦 Try the famous giant melonpan ice cream sandwiches',
                '📍 Surugaya Osaka: check Den Den Town for anime/vintage goods'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Rikuro\'s Cheesecake + Okonomiyaki',
              description: 'Grab Osaka\'s famous Rikuro\'s jiggly cheesecake (you\'ll see the queue — it\'s worth it), then sit down for proper Osaka-style okonomiyaki. The ultimate Osaka comfort food combo.',
              meta: '💰 $$ · 📍 Namba area · 🚫 Seafood okonomiyaki — specify no pork (buta nashi) · 👶 Jiggly cheesecake is toddler-approved'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Dotonbori Walk & Souvenirs',
              description: 'One last walk through Dotonbori — pick up any final souvenirs, street food, and photos. Hit the Don Quijote for last-minute gifts.',
              details: [
                '📸 Final Glico Running Man photo!',
                '🛍️ Last chance for souvenirs and snacks to bring home',
                '🌙 The canal at night is pure Osaka magic'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Yakiniku (Japanese BBQ)',
              description: 'End the trip with a proper yakiniku feast — grill premium wagyu beef, chicken, and seafood at your table. It\'s interactive, delicious, and the perfect celebration dinner. Osaka has incredible yakiniku restaurants.',
              meta: '💰 $$$ · 📍 Namba/Dotonbori area · 🚫 All beef, chicken, seafood — no pork · 👶 Interactive grilling is fun for families + private booth seating available'
            }
          ],
          tips: [
            { type: 'tip', text: 'Pack tonight! Tomorrow is departure day. Have the hotel store your luggage if you want to explore in the morning before heading to KIX.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6873, lng: 135.5262, label: 'Osaka Castle', num: 1, cat: 'attraction', desc: 'Iconic white and gold castle with park and moats' },
        { lat: 34.6727, lng: 135.4980, label: 'Amerikamura', num: 2, cat: 'shopping', desc: 'Osaka\'s trendy vintage and street fashion district' },
        { lat: 34.6745, lng: 135.5014, label: 'Shinsaibashi', num: 3, cat: 'shopping', desc: '600m covered shopping arcade' },
        { lat: 34.6685, lng: 135.5013, label: 'Dotonbori', num: 4, cat: 'attraction', desc: 'Final night walk along the iconic canal' },
        { lat: 34.6688, lng: 135.5008, label: 'Rikuro\'s', num: 5, cat: 'food', desc: 'Famous jiggly cheesecake — the queue is worth it' },
        { lat: 34.6600, lng: 135.5050, label: 'Surugaya Osaka', num: 6, cat: 'shopping', desc: 'Vintage anime and game shop in Den Den Town' }
      ]
    },
    {
      num: 10,
      date: '2026-05-24',
      neighborhoods: 'Osaka · Kansai International Airport (KIX)',
      title: 'Sayonara Japan — Final Morning & Flight Home',
      description: "Your last morning in Japan. Enjoy one final matcha, pick up omiyage (souvenirs/gifts) at the airport, and say goodbye to this incredible country. You'll be back — Japan has a way of pulling you back.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Last Matcha & Konbini Run',
              description: 'One final matcha at a café near your hotel, then hit up a konbini for last-minute snacks to bring home — Kit Kats in every flavor, rice crackers, and those amazing onigiri.',
              details: [
                '🍵 Final matcha — savor it!',
                '🏪 7-Eleven/Lawson: stock up on Japanese Kit Kats, snacks, and treats for home',
                '🍙 Grab onigiri and drinks for the airport journey'
              ]
            },
            {
              title: 'Travel to KIX Airport',
              description: 'Take the Nankai Rapi:t limited express from Namba to Kansai International Airport (34 min) — the retro-futuristic blue train is an attraction in itself. Or take the JR Haruka express from Tennoji.',
              details: [
                '🚃 Nankai Rapi:t from Namba: 34 min, ¥1,450',
                '🤖 The Rapi:t train looks like a spaceship — kids love it',
                '⏰ Arrive at airport 3 hours before international flights',
                '👶 Elevator access at all stations'
              ]
            }
          ]
        },
        {
          label: 'At the Airport',
          activities: [
            {
              title: 'KIX Airport Shopping & Last Bites',
              description: 'Kansai Airport has excellent shopping — pick up beautifully packaged omiyage (gift sweets), last-minute Japanese souvenirs, and even tax-free electronics. The food court has great ramen, sushi, and udon options.',
              details: [
                '🎁 Omiyage shops: Tokyo Banana, Royce chocolate, regional sweets',
                '🛍️ Uniqlo, duty-free electronics, character goods',
                '🍜 Airport ramen: try chicken-based Ippudo or seafood options',
                '👶 KIX has great kids\' play areas near the gates'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'KIX Airport Last Meal',
              description: 'One final Japanese meal before you fly — the airport food court has surprisingly excellent sushi, udon, and curry. Get the katsu curry with CHICKEN katsu for one last crunch.',
              meta: '💰 $$ · 📍 KIX Terminal 1 · 🚫 Chicken katsu curry or seafood — many options · 👶 Food court is easy with kids'
            }
          ],
          tips: [
            { type: 'tip', text: 'Tax-free shopping at the airport is actually good value for last-minute electronics and cosmetics. Keep your receipts organized — you\'ll show them at customs on the way out.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6639, lng: 135.5000, label: 'Namba Station', num: 1, cat: 'transport', desc: 'Nankai Rapi:t departure to KIX airport' },
        { lat: 34.4347, lng: 135.2441, label: 'Kansai International Airport', num: 2, cat: 'transport', desc: 'KIX — departure airport on man-made island' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '¥10,000-15,000/night', midrange: '¥20,000-35,000/night', luxury: '¥40,000-80,000/night' },
    { category: 'Meals (family of 5)', budget: '¥5,000-8,000/day', midrange: '¥10,000-20,000/day', luxury: '¥25,000-50,000/day' },
    { category: 'Transport (IC cards)', budget: '¥3,000-5,000/day', midrange: '¥5,000-8,000/day', luxury: '¥10,000-20,000/day (taxi)' },
    { category: 'Activities', budget: '¥0-3,000/day', midrange: '¥3,000-8,000/day', luxury: '¥8,000-20,000/day' },
    { category: 'Shinkansen (Tokyo→Osaka)', budget: '¥13,870/adult one-way', midrange: '¥13,870/adult', luxury: '¥19,590/adult (Green Car)' },
    { category: '10-Day Total (family of 5)', budget: '¥350,000-500,000', midrange: '¥500,000-900,000', luxury: '¥1,000,000-2,000,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There & Away', items: ['Arrive: Narita Airport (NRT) → Narita Express to Shibuya (80 min)', 'Depart: Kansai International Airport (KIX) — Nankai Rapi:t from Namba (34 min)', 'Shinkansen Tokyo→Osaka: Nozomi 2h15m, ¥13,870/adult, kids under 6 free'] },
    { title: '🏨 Where You\'re Staying', items: ['May 15-19: Shibuya Airbnb (4 nights) — central Tokyo base', 'May 19-20: Tokyo hotel (1 night) — near Tokyo Station for easy Shinkansen access', 'May 20-24: Osaka hotel (4 nights) — Namba/Shinsaibashi area recommended for food and transit'] },
    { title: '🚇 Getting Around', items: ['Suica/PASMO IC cards work on ALL trains, subways, buses across Japan', 'Kids under 6 ride free on all public transit', 'Google Maps works perfectly for transit directions in Japan', 'Elevators at all major stations — look for エレベーター signs'] },
    { title: '👶 Toddler Tips', items: ['Baby changing stations in every station, mall, and most restaurants', 'Convenience stores carry diapers, wipes, baby food, and formula', 'Many restaurants have kids\' menus (okosama set/お子様セット)', 'Strollers fold on crowded trains — consider a carrier for temples and markets', 'Japan is incredibly safe — don\'t worry about the kids exploring a bit'] },
    { title: '🚫 No-Pork Phrases', items: ['ブタ肉なしでお願いします (Butaniku nashi de onegaishimasu) — No pork please', '豚は食べられません (Buta wa taberaremasen) — I cannot eat pork', 'アレルギーカードを見せる — Show an allergy card (print one in advance!)', 'Safe options: tori (chicken), gyū (beef), sakana (fish), yasai (vegetable)', 'Watch for: tonkotsu (pork bone broth), chashu (pork slices), katsudon (pork cutlet)'] },
    { title: '💳 Money & Tips', items: ['IC cards and credit cards accepted almost everywhere', 'Some small shops and shrines are cash-only — carry ¥10,000-20,000', '7-Eleven ATMs accept international cards', 'No tipping in Japan — it can even be considered rude'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
