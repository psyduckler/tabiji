const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772554579651_k3few6',
  email: 'paulhblasjr@gmail.com',
  destination: 'tokyo, osaka, kyoto',
  dates: '2026-05-15 to 2026-05-24',
  groupSize: '5+',
  style: 'Adventure, Cultural, Foodie, Family-friendly',
  dining: 'Mix of everything',
  budget: 'Surprise me',
  requests: '3 adults, 2 children ages 3 and 2. No pork. No gundam. Landing NRT May 15 ~1300. Shibuya Airbnb May 15-19. Osaka base camp with Kyoto day trips. Adventurous pace with toddlers. Matcha mornings, late-night eating/shopping.',
  amount: 0
};

const itineraryData = {
  destination: 'Tokyo, Osaka & Kyoto',
  countryEmoji: '🇯🇵',
  title: 'Matcha, Manga & Mochi: A Family Japan Adventure',
  subtitle: '10 days across Tokyo, Osaka & Kyoto — toddler-tested, no-pork, all heart',
  description: "Three adults, two tiny adventurers, zero pork, and an absolutely packed itinerary through Japan's greatest cities. You'll wake up to matcha lattes in Shibuya, sprint through character stores with the kids, watch the sunset from Shibuya Sky, then hit Golden Gai after bedtime. From the neon chaos of Shinjuku to the silent torii gates of Fushimi Inari at dawn, this trip balances toddler naps with late-night ramen runs, temple mornings with anime shopping marathons, and big-city energy with moments of genuine wonder. Your Shibuya base gives you Tokyo for 4 nights, then the Shinkansen whisks you to Osaka for 5 more nights of street food, deer encounters, and Kyoto day trips.",
  duration: '10 nights',
  dates: 'May 15 – May 24, 2026',
  budget: '$$$',
  pace: 'Adventurous',
  bestFor: 'Families with Toddlers',
  highlights: [
    'teamLab Planets — barefoot immersive art the whole family will love',
    'Shibuya Sky sunset views over the Tokyo skyline',
    'Sensō-ji, Meiji Jingu & Fushimi Inari — Japan\'s most iconic temples',
    'Character store marathon: Pokémon, Kirby, One Piece, Naruto, Ghibli & Miffy',
    'Shinjuku Golden Gai & Omoide Yokocho — late-night Tokyo magic',
    'Nara deer park — toddlers hand-feeding wild deer',
    'Fushimi Inari at sunrise — thousands of vermillion torii gates',
    'Osaka street food crawl: takoyaki, yakitori & late-night Dotonbori'
  ],

  essentials: [
    { title: '🍼 Traveling with Toddlers (2 & 3)', text: 'Japan is incredibly toddler-friendly. Most stations have elevators, convenience stores sell baby food and diapers (Merries/Moony brands are excellent), and restaurants often have kids\' chairs. Bring a lightweight stroller — you\'ll need it for long walking days. Many attractions are free for under-6. Nap time is real: plan a midday break at the Airbnb or a park.' },
    { title: '🚫 No Pork Guide', text: 'Pork is everywhere in Japanese cuisine (ramen broth, gyoza, tonkatsu, many curries). For ramen, seek chicken (tori paitan) or seafood (shio/shoyu) broths — we\'ve marked safe spots throughout. Yakitori (chicken skewers) is your best friend. At conveyor belt sushi, stick to fish/veggie plates. When in doubt, say "butaniku nashi de onegaishimasu" (no pork please) or show the phrase on your phone.' },
    { title: '🚄 Getting Around', text: 'Get a 7-day Japan Rail Pass (covers Shinkansen Tokyo→Osaka + local JR lines). Activate it May 18 to cover your Shinkansen on May 19 and Osaka/Kyoto/Nara trains through May 24. For Tokyo days 1-3, use a Suica/Pasmo IC card (works on all trains/buses/vending machines). Strollers fit on trains but avoid rush hour (7:30-9:30am).' },
    { title: '🍵 Matcha Morning Ritual', text: 'Japan takes matcha seriously and so do you. We\'ve planned matcha stops every morning — from ceremonial tea at Meiji Jingu to matcha lattes in Shibuya to Rokujuan in Kyoto. Most matcha cafés open by 9-10am. Ichigo daifuku (strawberry mochi) pairs perfectly.' },
    { title: '🌙 Late-Night Tokyo & Osaka', text: 'After the kids crash, the adults can take turns exploring. Golden Gai and Omoide Yokocho in Shinjuku are walking distance from many hotels. In Osaka, Dotonbori stays alive until 2am. Convenience store (konbini) runs at midnight are a Japan rite of passage — 7-Eleven onigiri and Lawson karaage are elite.' },
    { title: '💰 Budget Notes', text: 'Japan can be surprisingly affordable with kids. Konbini meals are $3-5pp, sit-down lunches $8-15, nice dinners $20-40pp. Train passes save hundreds. Don Quijote is discount shopping paradise. Budget about $150-250/day for the family of 5 (excluding accommodation), more on big activity days.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-05-15',
      neighborhoods: 'Narita · Shibuya · Shinjuku',
      title: 'Landing in Tokyo — Shibuya First Night',
      description: "You land at Narita around 1pm. Clear immigration (budget 45-60min with kids), grab your Suica cards, and take the Narita Express to Shibuya (~90min). Check into your Airbnb, freshen up, then hit Shibuya Crossing at golden hour. Tonight is about soaking in the neon, grabbing your first incredible meal, and fighting jet lag with pure adrenaline.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Narita Express → Shibuya Airbnb',
              description: 'The Narita Express (N\'EX) runs directly to Shibuya Station (~90 min). Buy tickets at the JR counter in the airport. The train is spacious with luggage areas — perfect for strollers and bags. Kids ride free under 6.',
              details: [
                '🚃 N\'EX departs every 30-60 min from Narita — catch the ~2:30pm departure',
                '💳 Buy Suica IC cards at the airport for tap-and-go on all Tokyo trains',
                '🍼 Change diapers at the airport before boarding — train bathrooms are tiny'
              ]
            },
            {
              title: 'Shibuya Crossing & Hachiko Statue',
              description: 'Drop bags at the Airbnb and walk to the world\'s busiest intersection. Watch the scramble from the Shibuya Station overpass, snap a photo with the Hachiko statue, and let the kids be amazed by the wall of neon and people.',
              details: [
                '📸 Best view: Shibuya Station 2F open-air corridor (free)',
                '🐕 Hachiko statue is right outside Shibuya Station\'s Hachiko Exit',
                '🌆 Golden hour (5-6pm in May) makes the crossing magical'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Fuunji (Shinjuku)',
              description: 'Famous tsukemen (dipping ramen) spot with rich fish-based broth — NO PORK in the base. Thick noodles you dip into an intensely flavorful soup. The line moves fast. One of Tokyo\'s most iconic bowls.',
              meta: '💰 $ · 📍 Shinjuku (5 min from station) · 🚫 Pork-free fish broth option available'
            }
          ],
          tips: [
            { type: 'tip', text: 'Jet lag hack: stay up until 8-9pm local time even if you\'re dying. A big dinner and a walk through neon Shibuya will keep you going. The kids will crash hard — that\'s fine, let them reset.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shibuya Night Walk',
              description: 'Stroll through Center-gai, peek into Don Quijote Shibuya (the discount store wonderland), and let the toddlers point at every flashing screen. If the kids are still awake, grab soft-serve from a convenience store. If they\'re asleep in the stroller, enjoy the neon glow.',
              details: [
                '🏪 Don Quijote Shibuya is open 24hrs — snacks, toys, everything',
                '🍦 Lawson or 7-Eleven soft-serve is surprisingly good',
                '🌃 Shibuya at night with toddlers in a stroller is a vibe'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6580, lng: 139.7016, label: 'Shibuya Crossing', num: 1, cat: 'attraction', desc: 'World\'s busiest intersection — iconic Tokyo moment' },
        { lat: 35.6590, lng: 139.7006, label: 'Hachiko Statue', num: 2, cat: 'attraction', desc: 'The faithful dog statue outside Shibuya Station' },
        { lat: 35.6932, lng: 139.7004, label: 'Fuunji', num: 3, cat: 'food', desc: 'Famous tsukemen with pork-free fish broth' },
        { lat: 35.6600, lng: 139.6985, label: 'Don Quijote Shibuya', num: 4, cat: 'shopping', desc: 'Discount store wonderland — open 24hrs' }
      ]
    },
    {
      num: 2,
      date: '2026-05-16',
      neighborhoods: 'Shibuya · Harajuku · Meiji Jingu · Shinjuku',
      title: 'Shrines, Harajuku & Shinjuku After Dark',
      description: "Your first full Tokyo day starts with matcha at Meiji Jingu, then dives into the colorful chaos of Harajuku's Takeshita Street. Afternoon in Yoyogi Park for the kids to run wild, then Shinjuku Gyoen gardens. Evening: adults take turns exploring Golden Gai and Omoide Yokocho while kids sleep at the Airbnb.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Meiji Jingu Shrine',
              description: 'Walk through the towering torii gate into the forested grounds of Tokyo\'s most important Shinto shrine. The gravel paths through ancient trees feel like another world — steps from Harajuku\'s chaos. Write a wish on an ema (wooden prayer plaque). The inner garden has an iris garden blooming in mid-May.',
              details: [
                '⛩️ Free entry · Opens at sunrise (~4:30am May) but 9am is perfect',
                '🍵 Matcha & wagashi at the shrine\'s tea house (Kaguraden rest area)',
                '✏️ Ema plaques ¥500 — kids love writing wishes',
                '🌸 The iris garden (Meiji Jingu Gyoen, ¥500) blooms beautifully in May'
              ]
            },
            {
              title: 'Takeshita Street & Harajuku',
              description: 'The technicolor epicenter of Japanese youth culture. Crêpe shops, character goods stores, wild fashion boutiques, and cotton candy taller than your toddlers. Walk slowly — there\'s something insane in every window.',
              details: [
                '🍓 Get a Harajuku crêpe — strawberry + cream is the classic',
                '👕 Brandy Melville Harajuku is on Cat Street nearby',
                '🧸 Character shops everywhere — Sanrio, Kirby, etc.',
                '📸 The street is most fun 10am-noon before peak crowds'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Matcha Stop',
              name: 'Sakura Miffy Café (Harajuku)',
              description: 'The most adorable café in Tokyo. Miffy-themed lattes, matcha drinks, and pastries in a pink-and-white wonderland. The toddlers will lose their minds. Get the matcha Miffy latte.',
              meta: '💰 $$ · 📍 Harajuku/Omotesando · Reservations recommended'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Yoyogi Park',
              description: 'Right next to Meiji Jingu, this is Tokyo\'s Central Park. Let the toddlers run free on the grass, watch street performers, and enjoy the shade of massive zelkova trees. On weekends you might catch cosplayers near the Harajuku entrance.',
              details: [
                '🌳 Huge open grass areas — perfect for toddler energy release',
                '🎭 Street performers and cosplayers on weekends near Harajuku gate',
                '🧃 Vending machines everywhere for drinks'
              ]
            },
            {
              title: 'Shinjuku Gyoen National Garden',
              description: 'One of Tokyo\'s most beautiful gardens — English, French, and Japanese landscape styles across 144 acres. The greenhouse is toddler-friendly and the wide lawns are perfect for a break. Late roses and early hydrangeas bloom in May.',
              details: [
                '🌹 May flowers: roses in the formal garden, wisteria fading, hydrangeas starting',
                '💰 ¥500 adults, free under 6 · Closed Mondays',
                '🍱 Picnic-friendly — grab onigiri from a konbini beforehand',
                '📍 Use Shinjuku Gyoen-mae entrance (closest to Shinjuku Station)'
              ]
            },
            {
              title: 'Shinjuku Landmarks Walk',
              description: 'Walk from the garden toward Shinjuku Station. Hit the 3D Cat billboard at Cross Shinjuku (the giant calico cat on the screen — kids will LOVE it), check out Shinjuku Station East Exit (JJK fans know), and browse SURUGA-YA and Seria in the Marui Annex.',
              details: [
                '🐱 3D Cat Cross Shinjuku — the viral 3D billboard at Studio Alta building, plays every ~15 min',
                '📍 JJK reference: Shinjuku Station East Exit — where Gojo fought Sukuna',
                '🏪 SURUGA-YA Shinjuku Marui Annex — retro games, figures, manga',
                '🏪 Seria Shinjuku Marui Annex — Japan\'s best ¥100 shop (like Dollar Tree but actually good)'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Afuri (Harajuku)',
              description: 'Light, refreshing yuzu shio ramen with a clear chicken broth — one of the best pork-free ramen options in Tokyo. The citrusy, clean flavor is perfect for a warm May day.',
              meta: '💰 $$ · 📍 Harajuku/Omotesando · 🚫 Pork-free yuzu chicken broth'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Omoide Yokocho ("Memory Lane")',
              description: 'Narrow alleyways packed with tiny yakitori joints, each seating 6-8 people. Smoke, lanterns, cold beer, and the best chicken skewers in Tokyo. This is old-school Shinjuku at its finest. Come after 7pm for the full atmosphere.',
              details: [
                '🍗 Stick to yakitori (chicken) — it\'s the specialty and naturally pork-free',
                '🍺 Grab a beer and skewers standing at a counter',
                '📸 The narrow alleys are incredibly atmospheric at night',
                '⚠️ Some stalls use pork — ask "tori dake?" (chicken only?)'
              ]
            },
            {
              title: 'Golden Gai (Adults Only — Take Turns)',
              description: 'Six narrow alleys with 200+ tiny bars, each seating 4-8 people. Every bar has a theme — jazz, punk, cinema, cats. Cover charges ¥500-1000. This is where Tokyo gets weird and wonderful. Not for kids — adults take turns after bedtime.',
              details: [
                '🍸 Most bars have a ¥500-1000 cover charge + drinks',
                '🎵 Each bar has a unique vibe — peek in before committing',
                '🚫 No kids — this is adults-after-bedtime territory',
                '📍 Enter from Hanazono Shrine side for the best first impression'
              ]
            },
            {
              title: 'Kabukicho & Don Quijote Shinjuku',
              description: 'Walk through the neon canyon of Kabukicho (Tokyo\'s entertainment district — totally safe, just bright), and hit Don Quijote for late-night souvenir shopping. The massive store is open 24hrs and has everything from snacks to electronics to costumes.',
              details: [
                '🏮 The Kabukicho gate is iconic — great photo spot',
                '🏪 Don Quijote Shinjuku — multi-floor discount paradise, open 24hrs',
                '🎮 SURUGA-YA nearby for retro game shopping'
              ]
            }
          ],
          meals: [
            {
              type: '🌙 Late Night',
              name: 'Kabuki Yokocho (Shinjuku)',
              description: 'A food hall inside Kabukicho featuring regional Japanese cuisine stalls. Stay late, try different stalls. Chicken karaage, seafood, yakitori — plenty of pork-free options. Open until 4am on weekends.',
              meta: '💰 $$ · 📍 Kabukicho, Shinjuku · Open late · Multiple pork-free stalls'
            }
          ],
          tips: [
            { type: 'tip', text: 'Tag-team parenting tonight! One adult stays with sleeping kids at the Airbnb, two adults explore Golden Gai/Omoide Yokocho. Swap the next night. Shibuya to Shinjuku is just 5 min by train.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6764, lng: 139.6993, label: 'Meiji Jingu', num: 1, cat: 'attraction', desc: 'Tokyo\'s most important Shinto shrine in a forest' },
        { lat: 35.6715, lng: 139.7030, label: 'Takeshita Street', num: 2, cat: 'attraction', desc: 'Harajuku\'s colorful youth culture street' },
        { lat: 35.6717, lng: 139.6951, label: 'Yoyogi Park', num: 3, cat: 'attraction', desc: 'Tokyo\'s Central Park — great for toddlers' },
        { lat: 35.6852, lng: 139.7100, label: 'Shinjuku Gyoen', num: 4, cat: 'attraction', desc: 'Beautiful 144-acre garden with three styles' },
        { lat: 35.6938, lng: 139.7034, label: '3D Cat Cross Shinjuku', num: 5, cat: 'attraction', desc: 'Viral 3D cat billboard — kids love it' },
        { lat: 35.6940, lng: 139.7005, label: 'Omoide Yokocho', num: 6, cat: 'food', desc: 'Atmospheric yakitori alley — old-school Shinjuku' },
        { lat: 35.6942, lng: 139.7030, label: 'Golden Gai', num: 7, cat: 'food', desc: '200+ tiny themed bars in narrow alleys' },
        { lat: 35.6948, lng: 139.7030, label: 'Don Quijote Shinjuku', num: 8, cat: 'shopping', desc: 'Multi-floor discount shopping, open 24hrs' },
        { lat: 35.6944, lng: 139.7043, label: 'Kabuki Yokocho', num: 9, cat: 'food', desc: 'Late-night food hall in Kabukicho' },
        { lat: 35.6708, lng: 139.7063, label: 'Sakura Miffy Café', num: 10, cat: 'food', desc: 'Adorable Miffy-themed café with matcha lattes' },
        { lat: 35.6693, lng: 139.7007, label: 'Brandy Melville Harajuku', num: 11, cat: 'shopping', desc: 'Brandy Melville on Cat Street' },
        { lat: 35.6720, lng: 139.7095, label: 'Afuri Ramen', num: 12, cat: 'food', desc: 'Yuzu shio chicken ramen — pork-free' },
        { lat: 35.6936, lng: 139.7044, label: 'SURUGA-YA Shinjuku', num: 13, cat: 'shopping', desc: 'Retro games, figures, manga' },
        { lat: 35.6936, lng: 139.7046, label: 'Seria Shinjuku', num: 14, cat: 'shopping', desc: 'Japan\'s best ¥100 shop' },
        { lat: 35.6896, lng: 139.7006, label: 'Shinjuku Station East Exit', num: 15, cat: 'attraction', desc: 'JJK reference — Gojo vs Sukuna battle site' }
      ]
    },
    {
      num: 3,
      date: '2026-05-17',
      neighborhoods: 'Toyosu · Odaiba · Ikebukuro',
      title: 'teamLab, Ghibli Store & Ikebukuro Anime District',
      description: "Today is pure wonder. Start with the mind-blowing immersive art of teamLab Planets (barefoot in water — the toddlers will go feral), then head to Ikebukuro for the Ghibli store, Sunshine City, Pokémon Center, and the Kirby Café. This is the character store marathon day.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'teamLab Planets TOKYO DMM',
              description: 'Walk barefoot through water, light, and digital art installations. You wade knee-deep through rooms of koi fish made of light, lie in fields of infinite flowers, and float in darkness. The toddlers will be MESMERIZED. One of the best family experiences in Tokyo.',
              details: [
                '🦶 Barefoot experience — wear shorts/roll-up pants (water rooms are knee-deep for adults)',
                '🎟️ Book online in advance — sells out! ¥3,200 adults, free under 3, ¥1,000 ages 4-12',
                '👶 Toddler tip: the dark rooms might startle some kids. The water rooms and flower rooms are universally loved.',
                '⏰ Go at opening (9 or 10am) for shortest waits between rooms',
                '📍 Toyosu area — take Yurikamome line to Shin-Toyosu Station'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Matcha Stop',
              name: 'Matcha Stand Maruni (Toyosu area)',
              description: 'Grab a matcha latte from one of the trendy matcha stands near teamLab before your visit. Rich, creamy, and the perfect morning ritual.',
              meta: '💰 $ · 📍 Near Shin-Toyosu · Quick matcha fix'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Donguri Kyowakoku (Ghibli Store) — Ikebukuro',
              description: 'The official Studio Ghibli merchandise store. Totoro plushies, Kiki\'s Delivery Service bags, Spirited Away figurines — the whole magical world. This Ikebukuro location inside Sunshine City is one of the largest.',
              details: [
                '🏪 Inside Sunshine City Alpa, 3F',
                '🧸 Totoro, Catbus, No-Face, Ponyo — all the plush friends',
                '🎁 Exclusive Japan-only Ghibli merch you can\'t get elsewhere'
              ]
            },
            {
              title: 'Sunshine City — Ikebukuro',
              description: 'A massive entertainment complex with an aquarium, shopping mall, and character stores. The Sunshine Aquarium on the rooftop has a penguin sky walkway — toddler heaven. Browse the anime floors below.',
              details: [
                '🐧 Sunshine Aquarium — penguins swimming overhead in a sky tunnel, ¥2,600 adults',
                '🛍️ Multiple anime/character shops throughout',
                '🍼 Family facilities: nursing rooms, stroller-friendly elevators'
              ]
            },
            {
              title: 'Pokémon Center Mega Tokyo & Pikachu Sweets',
              description: 'The MEGA Pokémon Center in Sunshine City is the biggest in Tokyo. Exclusive plushies, cards, clothing, and snacks. Next door, Pikachu Sweets by Pokémon Café serves Pikachu-shaped desserts and drinks.',
              details: [
                '⚡ Pokémon Center Mega — exclusive Tokyo merch and giant Pikachu displays',
                '🍰 Pikachu Sweets — adorable character desserts (pork-free pastries and drinks)',
                '🎮 Kids can play at the demo stations'
              ]
            },
            {
              title: 'Kirby Café Tokyo',
              description: 'Everything is Kirby-shaped. The pancakes are Kirby. The curry is Kirby. The latte art is Kirby. Reserve ahead — this place sells out. The food is legitimately good AND adorable.',
              details: [
                '🎟️ MUST book online at kirby-cafe.jp — often books out weeks ahead',
                '⏰ 80-minute time limit per seating',
                '🍽️ Try the Kirby chicken curry (pork-free!) and the Waddle Dee dessert',
                '📍 Tokyo Solamachi (near Skytree) — but book your slot for after Ikebukuro'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Kirby Café (reservation)',
              description: 'Your lunch IS the activity. Kirby-shaped everything in the cutest café in Tokyo. Book well in advance. The chicken curry plate and desserts are pork-free and delicious.',
              meta: '💰 $$$ · 📍 Tokyo Solamachi (Skytree area) · 🚫 Pork-free options available · Book ahead!'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Tokyo Skytree',
              description: 'At 634m, it\'s the tallest tower in the world. The observation deck views at sunset are insane — you can see Mt. Fuji on clear days. The Solamachi shopping complex at the base has tons of shops and snacks. Since Kirby Café is here, combine the visit.',
              details: [
                '🗼 Tembo Deck (350m): ¥2,100 adults, ¥950 ages 4-11, free under 4',
                '🌅 Sunset timing in May: ~6:30pm — book the 6pm slot for golden light',
                '📸 Clear May evenings give stunning views toward Mt. Fuji',
                '🛍️ Solamachi has 300+ shops including character stores'
              ]
            }
          ],
          meals: [
            {
              type: '🌙 Dinner',
              name: 'Toraji (Skytree Solamachi)',
              description: 'Premium yakiniku (Japanese BBQ) with spectacular Skytree views. Grill your own wagyu beef and chicken at the table — no pork needed when the beef is this good. Kids love the interactive grilling.',
              meta: '💰 $$$ · 📍 Tokyo Solamachi 6F · 🚫 Order beef & chicken only — easy to avoid pork'
            }
          ],
          tips: [
            { type: 'tip', text: 'Book Kirby Café the moment reservations open (usually 1 month ahead at kirby-cafe.jp). Also pre-book teamLab Planets and Skytree online. May is peak season — walk-ups are risky.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6431, lng: 139.7895, label: 'teamLab Planets', num: 1, cat: 'attraction', desc: 'Barefoot immersive art — mind-blowing for all ages' },
        { lat: 35.7295, lng: 139.7190, label: 'Donguri Kyowakoku (Ghibli Store)', num: 2, cat: 'shopping', desc: 'Official Ghibli store in Sunshine City' },
        { lat: 35.7294, lng: 139.7185, label: 'Sunshine City', num: 3, cat: 'attraction', desc: 'Entertainment complex with aquarium and anime shops' },
        { lat: 35.7290, lng: 139.7188, label: 'Pokémon Center Mega Tokyo', num: 4, cat: 'shopping', desc: 'Biggest Pokémon store in Tokyo + Pikachu Sweets' },
        { lat: 35.7101, lng: 139.8107, label: 'Kirby Café Tokyo', num: 5, cat: 'food', desc: 'Kirby-shaped food in the cutest café ever' },
        { lat: 35.7101, lng: 139.8085, label: 'Tokyo Skytree', num: 6, cat: 'attraction', desc: 'World\'s tallest tower — 634m observation deck' },
        { lat: 35.7103, lng: 139.8095, label: 'Toraji Yakiniku', num: 7, cat: 'food', desc: 'Premium wagyu BBQ with Skytree views' }
      ]
    },
    {
      num: 4,
      date: '2026-05-18',
      neighborhoods: 'Shibuya · Asakusa · Shiba Park · Setagaya',
      title: 'Temples, Towers & Tokyo\'s Hidden Gems',
      description: "Start with matcha and Shibuya Sky views, then explore three of Tokyo's most iconic spots: Sensō-ji temple in Asakusa, the cat temple Gōtokuji, and Tokyo Tower from Shiba Park. Pack in Hie-jinja Shrine, ichigo daifuku shopping, and end with a soak at Toyosu Manyo Club.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shibuya Sky',
              description: 'The rooftop observation deck at Shibuya Scramble Square — 230m up with 360° views of Tokyo. The open-air rooftop (SHIBUYA SKY) is incredible at morning golden hour. Glass floor edges, a net hammock area, and views from Rainbow Bridge to Mt. Fuji.',
              details: [
                '🎟️ ¥2,000 adults, ¥1,000 ages 6-12, free under 6 · Book online!',
                '⏰ First entry at 10am — go early for thin crowds and clear morning views',
                '📸 The rooftop "sky edge" glass area is the money shot',
                '☕ Grab a coffee at the observation deck café'
              ]
            },
            {
              title: 'Shibuya Character Stores Marathon',
              description: 'Before leaving Shibuya, blitz through the character stores near the station. One Piece Mugiwara Store, Naruto/Boruto store, and various anime shops are clustered around Shibuya Parco and nearby buildings.',
              details: [
                '🏴‍☠️ One Piece Mugiwara Store — Shibuya Parco 6F',
                '🍥 Naruto/Boruto Official Store — Shibuya Parco 6F (same floor!)',
                '🎮 Nintendo Tokyo is also in Shibuya Parco 6F',
                '🛍️ Shibuya Parco 6F is basically character store heaven'
              ]
            },
            {
              title: 'Cafe Reissue (Latte Art)',
              description: 'Famous for incredible 3D latte art — the barista sculpts characters out of foam on your drink. Get a matcha latte with a custom foam art creation. Instagram gold and the kids will be obsessed watching them make it.',
              details: [
                '☕ 3D latte art made to order — you can request characters',
                '🍵 Matcha lattes available with art',
                '📍 Shibuya area, small café — can wait 15-20 min'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Matcha + Mochi',
              name: 'Ichigo Daifuku Shopping',
              description: 'Hunt for ichigo daifuku (strawberry mochi) from one of Tokyo\'s famous wagashi shops. Try Iseya near Shibuya or hit depachika (department store basement food halls) for the prettiest seasonal mochi. May = peak strawberry season ending, so the daifuku are extra special.',
              meta: '💰 $ · 📍 Various Shibuya depachika · Seasonal strawberry mochi'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Sensō-ji Temple — Asakusa',
              description: 'Tokyo\'s oldest and most visited temple. Walk through the massive Kaminarimon (Thunder Gate) with its giant red lantern, browse Nakamise-dōri shopping street for snacks and souvenirs, then reach the main hall. The incense cauldron — fan the smoke toward you for good health — is a fun ritual for kids.',
              details: [
                '⛩️ Free entry · Always open, but shops close ~5pm',
                '🛍️ Nakamise-dōri: senbe crackers, ningyo-yaki cakes, chopsticks, fans',
                '🍘 Try melon pan (melon-flavored bread) and age-manju (fried dumplings — check for pork)',
                '👶 The wide paths are stroller-friendly'
              ]
            },
            {
              title: 'Gōtokuji Temple (Cat Temple) — Setagaya',
              description: 'The temple of a thousand beckoning cats (maneki-neko). Shelves and shelves of white lucky cat figurines left as offerings — it\'s surreal and beautiful. Buy your own maneki-neko (from ¥300) and add it to the collection. The toddlers will be cat-crazy.',
              details: [
                '🐱 Thousands of maneki-neko figurines on display shelves',
                '💰 Free entry · Buy a lucky cat from ¥300 to leave or take home',
                '📍 Setagaya area — take Tokyu/Odakyu lines from Shibuya (~25 min)',
                '📸 The cat figurine shelves are one of Tokyo\'s most unique photo spots'
              ]
            },
            {
              title: 'Hie-jinja Shrine',
              description: 'A beautiful Shinto shrine near Akasaka with a stunning tunnel of red torii gates (mini Fushimi Inari vibes!) and a unique monkey motif. The torii tunnel staircase is incredibly photogenic and less crowded than the famous spots.',
              details: [
                '⛩️ Free entry · The torii gate tunnel staircase is on the west side',
                '🐒 Monkey sculptures — the shrine\'s guardian animal',
                '📍 Near Akasaka — between Shibuya and Asakusa routes'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Asakusa Gyukatsu (Beef Cutlet)',
              description: 'Instead of tonkatsu (pork cutlet), try gyukatsu — deep-fried wagyu beef cutlet that you grill on a hot stone at your table. It\'s the perfect pork-free alternative to Japan\'s cutlet obsession. Crispy outside, pink inside.',
              meta: '💰 $$ · 📍 Asakusa area · 🚫 100% beef — pork-free katsu!'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Prince Shiba Park & Tokyo Tower',
              description: 'End the day at Shiba Park with Tokyo Tower glowing orange against the twilight sky. The park is beautiful, the kids can run around, and the tower view from below is more impressive than going up it. (If you want to go up: ¥1,200 adults.)',
              details: [
                '🗼 Tokyo Tower is most beautiful from outside at night — lit up orange',
                '🌳 Shiba Park has wide paths and grass — great for evening toddler energy burn',
                '📸 Classic Tokyo Tower photo from the park\'s temple gate',
                '🏯 Zojo-ji Temple is right there — beautiful lit up at night'
              ]
            },
            {
              title: 'Toyosu Manyo Club (24hr Onsen Spa)',
              description: 'End this packed day with a family soak at Toyosu Manyo Club — a 24-hour hot spring resort with indoor/outdoor baths, relaxation rooms, and restaurants. Kids are welcome in most areas. The warm water will knock everyone out for a great night\'s sleep.',
              details: [
                '♨️ Multiple bath types: indoor, outdoor, jet, silk, carbonated',
                '👶 Kids allowed in most baths (check their current policy for toddlers)',
                '🍽️ Full restaurant inside — eat dinner in your yukata (robe)',
                '💰 ¥3,850 adults, ¥1,980 kids · Open 24hrs',
                '📍 Toyosu area — combine with evening wind-down'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Toyosu Manyo Club Restaurant',
              description: 'Eat in your yukata at the onsen\'s restaurant. Sashimi, udon, chicken karaage, tempura — plenty of pork-free Japanese comfort food. The kids will be in robes and blissed out from the warm water.',
              meta: '💰 $$ · 📍 Inside Toyosu Manyo Club · 🚫 Many pork-free options'
            }
          ],
          tips: [
            { type: 'tip', text: 'Gōtokuji is slightly out of the way but 1000% worth it. Take the Tokyu Setagaya Line from Sangenjaya (easily reached from Shibuya). The quiet residential area around the temple is charming — real neighborhood Tokyo.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6584, lng: 139.7022, label: 'Shibuya Sky', num: 1, cat: 'attraction', desc: '230m rooftop views — 360° Tokyo panorama' },
        { lat: 35.6601, lng: 139.6982, label: 'Shibuya Parco (One Piece/Naruto/Nintendo)', num: 2, cat: 'shopping', desc: 'Character store heaven on 6F' },
        { lat: 35.6612, lng: 139.6988, label: 'Cafe Reissue', num: 3, cat: 'food', desc: 'Famous 3D latte art café' },
        { lat: 35.7148, lng: 139.7967, label: 'Sensō-ji Temple', num: 4, cat: 'attraction', desc: 'Tokyo\'s oldest temple with Nakamise shopping street' },
        { lat: 35.6497, lng: 139.6381, label: 'Gōtokuji (Cat Temple)', num: 5, cat: 'attraction', desc: 'Thousands of lucky cat figurines — surreal and beautiful' },
        { lat: 35.6757, lng: 139.7399, label: 'Hie-jinja Shrine', num: 6, cat: 'attraction', desc: 'Torii gate tunnel staircase and monkey guardians' },
        { lat: 35.6586, lng: 139.7454, label: 'Tokyo Tower from Shiba Park', num: 7, cat: 'attraction', desc: 'Iconic tower glowing orange against twilight' },
        { lat: 35.6564, lng: 139.7468, label: 'Prince Shiba Park', num: 8, cat: 'attraction', desc: 'Beautiful park at the foot of Tokyo Tower' },
        { lat: 35.6430, lng: 139.7900, label: 'Toyosu Manyo Club', num: 9, cat: 'attraction', desc: '24hr onsen spa resort — family soak' },
        { lat: 35.7119, lng: 139.7967, label: 'Asakusa Gyukatsu', num: 10, cat: 'food', desc: 'Wagyu beef cutlet — pork-free katsu alternative' }
      ]
    },
    {
      num: 5,
      date: '2026-05-19',
      neighborhoods: 'Shibuya · Tsukiji · Shinjuku · Shinkansen to Osaka',
      title: 'Final Tokyo Hits & Shinkansen to Osaka',
      description: "Morning rush to hit the remaining Tokyo spots: Tsukiji outer market for breakfast, Uniqlo Ginza flagship, Bokksu Market, and the Tokyo Metropolitan Government Building for free observation deck views. Then grab your bags, board the Shinkansen, and rocket to Osaka in 2.5 hours.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tsukiji Fish Market (Outer Market)',
              description: 'The original fish market\'s outer market is still thriving — a maze of food stalls serving the freshest seafood in the world. Grab tamagoyaki (sweet egg omelette on a stick — kids love it), fresh sashimi, grilled scallops, and strawberry daifuku from the street vendors.',
              details: [
                '🐟 Best stalls open 7-8am — go early for the full experience',
                '🍳 Tamagoyaki (egg omelette) sticks are the kid-friendly MVP',
                '🍓 Ichigo daifuku stalls here are some of Tokyo\'s best',
                '🦑 Grilled squid, scallops, and wagyu beef skewers — all pork-free',
                '🚫 Skip the tuna auctions (moved to Toyosu) — outer market is the food paradise'
              ]
            },
            {
              title: 'Tokyo Metropolitan Government Building — North Observation Deck',
              description: 'FREE panoramic views from 202m up in Shinjuku. On clear days you can see Mt. Fuji. The North Observatory is generally less crowded than the South. Zero reason not to come here — it\'s free and the views rival paid decks.',
              details: [
                '💰 FREE entry — one of Tokyo\'s best-kept secrets',
                '⏰ Opens 10am · North Observatory is usually quieter',
                '🗻 May mornings have the best chance of clear Fuji views',
                '📍 Shinjuku West Exit, 10-min walk from station'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Tsukiji Outer Market Street Food',
              description: 'Your breakfast IS the market. Graze through: tamagoyaki sticks, fresh uni (sea urchin) shooters, grilled seafood, fruit mochi, and matcha soft-serve. Budget ¥2,000-3,000 per person for a feast.',
              meta: '💰 $$ · 📍 Tsukiji Outer Market · 🚫 Naturally pork-free (seafood focus)'
            }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Uniqlo Ginza Flagship',
              description: 'The world\'s largest Uniqlo — 12 floors of Japanese basics done perfectly. Grab AIRism underlayers for the Osaka heat, kids\' clothes, and Japan-exclusive designs. Way cheaper than US Uniqlo.',
              details: [
                '👕 12 floors — Japan exclusives on upper floors',
                '👶 Great kids section with adorable Japan-only prints',
                '🎨 UT graphic tee floor has anime/artist collabs',
                '📍 Ginza, 5-min walk from Tsukiji'
              ]
            },
            {
              title: 'Bokksu Market',
              description: 'Japanese snack and pantry store — curated artisanal Japanese snacks, teas, and ingredients. Pick up matcha, unique Kit-Kats, rice crackers, and mochi to take home. Great for omiyage (souvenirs/gifts).',
              details: [
                '🍵 Premium matcha, hojicha, and Japanese teas',
                '🍫 Unique Kit-Kat flavors and artisanal snacks',
                '🎁 Beautiful packaging — ready-to-gift'
              ]
            },
            {
              title: 'Oyokogawa Shinsui Park',
              description: 'A hidden gem — a narrow waterside park following an old canal in eastern Tokyo. Cherry trees line the banks (blossoms gone by May, but the green canopy is lovely), small playgrounds dot the path, and it\'s blissfully tourist-free. Let the toddlers play.',
              details: [
                '🌳 Peaceful canal-side walking path with playgrounds',
                '👶 Multiple small playground areas along the park',
                '📍 Near Kiyosumi-Shirakawa or Morishita stations'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shinkansen to Osaka',
              description: 'Head back to the Airbnb, grab bags, and take the train to Tokyo Station. Board the Tokaido Shinkansen (Nozomi or Hikari) to Shin-Osaka — 2.5 hours of smooth bullet train magic. The kids will be glued to the window watching Japan blur by at 300km/h.',
              details: [
                '🚄 Nozomi: 2h15m, Hikari: 2h45m to Shin-Osaka',
                '🎟️ If using JR Pass (activate today!), take Hikari (Nozomi not covered)',
                '🍱 Buy ekiben (train station bento) at Tokyo Station — massive selection!',
                '🍼 Change/feed kids before boarding — Shinkansen has small bathrooms',
                '⏰ Aim for the 2-3pm departure to arrive by 5pm'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Shinkansen Lunch',
              name: 'Ekiben at Tokyo Station (Gransta)',
              description: 'Tokyo Station has 200+ ekiben (train bento) options. Get a salmon ikura bento, chicken teriyaki box, or wagyu beef bento. Eating on the Shinkansen is a Japanese tradition — don\'t skip it!',
              meta: '💰 $$ · 📍 Tokyo Station Gransta · 🚫 Many pork-free bentos — check labels (豚 = pork)'
            }
          ],
          tips: [
            { type: 'tip', text: 'Activate your 7-day JR Pass today (May 19) to cover: Shinkansen to Osaka + JR lines in Osaka/Kyoto/Nara through May 24. Pro move: reserve Shinkansen seats at the JR ticket counter before boarding.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Check into Osaka & Dotonbori Night Walk',
              description: 'Arrive in Osaka, check into your accommodation, then head straight for Dotonbori — Osaka\'s neon-lit food paradise along the canal. The Glico Running Man sign, the giant crab and pufferfish signs, and the energy of Namba at night. This is Osaka\'s beating heart.',
              details: [
                '🦀 The Kani Doraku (giant crab) and fugu (pufferfish) signs are iconic',
                '🏃 Glico Running Man — THE Osaka photo spot',
                '🌊 Walk along the canal for the best neon reflections',
                '🛍️ Don Quijote Dotonbori is right here — open 24hrs'
              ]
            }
          ],
          meals: [
            {
              type: '🌙 Dinner',
              name: 'Dotonbori Street Food Crawl',
              description: 'Osaka is the street food capital of Japan. Start with takoyaki (octopus balls) from a street vendor, then yakitori skewers, then okonomiyaki (savory pancake — ask for no pork/seafood version). Wash it down with melon soda.',
              meta: '💰 $ · 📍 Dotonbori · 🚫 Takoyaki & yakitori are naturally pork-free. For okonomiyaki, request "buta nashi" (no pork) — get seafood or chicken version'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6654, lng: 139.7707, label: 'Tsukiji Outer Market', num: 1, cat: 'food', desc: 'Seafood breakfast paradise — freshest in the world' },
        { lat: 35.6897, lng: 139.6917, label: 'Tokyo Metro Government Bldg', num: 2, cat: 'attraction', desc: 'FREE 202m observation deck — Fuji views' },
        { lat: 35.6711, lng: 139.7640, label: 'Uniqlo Ginza Flagship', num: 3, cat: 'shopping', desc: 'World\'s largest Uniqlo — 12 floors' },
        { lat: 35.6822, lng: 139.7956, label: 'Oyokogawa Shinsui Park', num: 4, cat: 'attraction', desc: 'Hidden canal park with playgrounds' },
        { lat: 34.6687, lng: 135.5013, label: 'Dotonbori', num: 5, cat: 'food', desc: 'Osaka\'s neon-lit street food paradise' },
        { lat: 34.6685, lng: 135.5025, label: 'Don Quijote Dotonbori', num: 6, cat: 'shopping', desc: 'Discount shopping — Osaka edition' },
        { lat: 34.6688, lng: 135.5010, label: 'Glico Running Man', num: 7, cat: 'attraction', desc: 'THE iconic Osaka photo spot' }
      ]
    },
    {
      num: 6,
      date: '2026-05-20',
      neighborhoods: 'Osaka · Nara Day Trip',
      title: 'Nara Day Trip — Deer, Buddha & Mochi',
      description: "Train to Nara (45 min from Osaka) for one of the trip's most magical days. Hundreds of wild deer roam freely through the park and temple grounds — they'll bow to you for crackers. The toddlers will absolutely lose it. Plus the Great Buddha at Todai-ji and beautiful Nara Park.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Train to Nara & Nara Park',
              description: 'Take the JR Yamatoji Rapid from Osaka\'s Namba/Tennoji to Nara (~45 min, covered by JR Pass). Walk from the station through the shopping arcade to Nara Park, where over 1,000 wild deer roam free. Buy shika senbei (deer crackers, ¥200) and let the toddlers hand-feed the deer.',
              details: [
                '🦌 Over 1,000 wild deer roam the park — they bow for crackers!',
                '🍘 Shika senbei ¥200 — the deer will come RIGHT to you',
                '👶 Toddler tip: some deer can be pushy. Hold the cracker flat-palmed.',
                '⏰ Go early (arrive 9-9:30am) before tour buses flood in'
              ]
            },
            {
              title: 'Todai-ji Temple & Great Buddha',
              description: 'The world\'s largest wooden building houses a 15m bronze Buddha that\'s been sitting here since 752 AD. Walk through the massive Nandaimon gate with its fierce guardian statues. Inside, there\'s a pillar with a hole the same size as Buddha\'s nostril — if you fit through, you get good luck (kids fit easily!).',
              details: [
                '🏯 ¥600 adults, ¥300 kids · One of Japan\'s most impressive sights',
                '🕳️ The nostril pillar — kids squeeze through for good luck!',
                '⛩️ Nandaimon Gate guardian statues are 8m tall and terrifyingly cool',
                '📸 The scale is jaw-dropping — photos don\'t do it justice'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Matcha Stop',
              name: 'Yosano Matcha House (Nara Park area)',
              description: 'Stop for matcha and warabi mochi (bracken starch mochi with kinako powder) near the park. Nara\'s matcha culture is more relaxed than Kyoto — sit outside with a view of the deer.',
              meta: '💰 $ · 📍 Near Nara Park · Matcha + warabi mochi'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kasuga Taisha Shrine',
              description: 'A Shinto shrine famous for its thousands of stone and bronze lanterns lining the paths through the forest. Deer wander through the shrine grounds. The moss-covered stone lanterns in the ancient forest are otherworldly.',
              details: [
                '🏮 3,000+ lanterns — stone lanterns line the approach, bronze lanterns inside',
                '🦌 Deer wander the shrine grounds freely',
                '🌳 The primeval forest behind the shrine is a UNESCO World Heritage site',
                '💰 Grounds free · Inner shrine ¥500'
              ]
            },
            {
              title: 'Naramachi Old Town',
              description: 'Wander the preserved merchant district south of Nara Park. Traditional machiya (townhouses) converted into cafés, craft shops, and galleries. Much quieter than Kyoto\'s tourist areas — genuine old Japan vibes.',
              details: [
                '🏘️ Traditional wooden architecture from the Edo period',
                '☕ Cute cafés in converted machiya townhouses',
                '🎁 Craft shops with Nara-specific souvenirs'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Kakinoha Sushi (Nara specialty)',
              description: 'Nara\'s signature dish: sushi wrapped in persimmon leaves. The leaves gently flavor and preserve the fish. Tanaka is a famous spot near Kintetsu Nara Station. Completely pork-free — it\'s all fish.',
              meta: '💰 $$ · 📍 Naramachi area · 🚫 Naturally pork-free (fish sushi)'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Osaka & Shinsekai District',
              description: 'Train back to Osaka and explore Shinsekai (New World) — a retro entertainment district with the iconic Tsutenkaku Tower. The area has a nostalgic, slightly gritty vibe with amazing kushikatsu (deep-fried skewers) shops and game arcades.',
              details: [
                '🗼 Tsutenkaku Tower — Osaka\'s mini Eiffel Tower (¥900 to go up)',
                '🎮 Retro game arcades with crane games — toddler magnets',
                '🏮 The neon-lit streets have serious Blade Runner energy at night'
              ]
            }
          ],
          meals: [
            {
              type: '🌙 Dinner',
              name: 'Kushikatsu Daruma (Shinsekai)',
              description: 'Osaka\'s famous deep-fried skewer restaurant. Get the chicken, shrimp, cheese, and veggie skewers — skip the pork ones. The rule: NEVER double-dip in the communal sauce. Crispy, hot, and ridiculously satisfying.',
              meta: '💰 $ · 📍 Shinsekai · 🚫 Order chicken/seafood/veggie skewers — easy to avoid pork'
            }
          ],
          tips: [
            { type: 'tip', text: 'The deer are sacred messengers of the gods in Shinto tradition. They\'ve been protected in Nara for over 1,000 years. They\'ll bow to you — bow back! It\'s polite (and adorable).' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6851, lng: 135.8398, label: 'Nara Park', num: 1, cat: 'attraction', desc: '1,000+ wild deer roaming free — feed them crackers' },
        { lat: 34.6890, lng: 135.8398, label: 'Todai-ji Temple', num: 2, cat: 'attraction', desc: 'World\'s largest wooden building with 15m bronze Buddha' },
        { lat: 34.6812, lng: 135.8499, label: 'Kasuga Taisha Shrine', num: 3, cat: 'attraction', desc: '3,000 lanterns in an ancient forest' },
        { lat: 34.6780, lng: 135.8310, label: 'Naramachi Old Town', num: 4, cat: 'attraction', desc: 'Preserved Edo-period merchant district' },
        { lat: 34.6524, lng: 135.5063, label: 'Shinsekai', num: 5, cat: 'attraction', desc: 'Retro entertainment district with Tsutenkaku Tower' },
        { lat: 34.6524, lng: 135.5060, label: 'Kushikatsu Daruma', num: 6, cat: 'food', desc: 'Famous deep-fried skewers — never double dip!' }
      ]
    },
    {
      num: 7,
      date: '2026-05-21',
      neighborhoods: 'Kyoto · Fushimi Inari · Gion · Nishiki Market',
      title: 'Kyoto Day 1 — Fushimi Inari, Gion & Nishiki Market',
      description: "The Kyoto day you've been dreaming about. Start before dawn at Fushimi Inari for the surreal experience of thousands of vermillion torii gates with almost no one around. Then matcha at Rokujuan, the geisha district of Gion, and Nishiki Market for the best food corridor in Japan.",
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            {
              title: 'Fushimi Inari Taisha — Sunrise Visit',
              description: 'THE iconic Japanese image: thousands of bright vermillion torii gates winding up a mountainside. At sunrise (5am-ish in May), you\'ll have the gates nearly to yourself for stunning photos. You don\'t need to hike the full 2-hour loop — the first 15-20 minutes of gates are the most photogenic.',
              details: [
                '⛩️ Free, open 24/7 — sunrise is the magic hour',
                '📸 The tunnel of gates is most dense in the first section (Senbon Torii)',
                '👶 With toddlers, do the first 20-30 min of the path then turn back',
                '⏰ Take the first JR Nara Line train from Osaka (~40 min) to arrive by 6am',
                '🚫 Stroller won\'t work on the mountain path — bring a carrier for the little ones'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'This is worth the early wake-up. By 8-9am the gates are packed with tour groups and the magic is gone. At 6am it\'s just you, the torii, and the foxes. One adult can stay with sleeping kids if needed — the other two adults go.' }
          ]
        },
        {
          label: 'Morning',
          activities: [
            {
              title: 'Rokujuan Tea House — Uji Matcha Experience',
              description: 'After Fushimi Inari, head to Rokujuan (六条庵) for a proper matcha experience. This tea house serves premium Uji matcha (Kyoto region is matcha\'s birthplace) with traditional wagashi sweets. Sit on tatami, watch the ceremonial preparation, and taste the difference real ceremonial-grade matcha makes.',
              details: [
                '🍵 Ceremonial matcha set with wagashi ~¥1,000-1,500',
                '🏠 Traditional tatami seating — kids sit on cushions',
                '📍 Near Fushimi area — walkable from Fushimi Inari'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Matcha Ceremony',
              name: 'Rokujuan Tea House',
              description: 'Premium Uji matcha in a traditional setting. This is THE matcha morning you\'ve been waiting for. Kyoto\'s Uji region produces the finest matcha in the world — this is where it all comes from.',
              meta: '💰 $$ · 📍 Near Fushimi · Traditional matcha ceremony'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nishiki Market ("Kyoto\'s Kitchen")',
              description: 'A narrow, covered shopping street with 130+ vendors selling Kyoto specialties. Pickles, mochi, fresh tofu, matcha everything, grilled seafood on sticks, and beautiful ceramics. Walk slowly and graze — this is lunch, shopping, and sightseeing combined.',
              details: [
                '🍡 Must-try: yuba (tofu skin), tsukemono (pickles), matcha mochi, grilled squid',
                '🍵 Matcha soft-serve and matcha everything at multiple stalls',
                '🔪 Beautiful Kyoto knives and ceramics for souvenirs',
                '👶 The narrow covered arcade is stroller-passable but tight at peak hours'
              ]
            },
            {
              title: 'Gion District — Geisha Quarter',
              description: 'Wander the historic streets of Gion with its traditional wooden machiya tea houses. Hanami-koji Street is the main artery — if you\'re lucky, you\'ll spot a geiko (Kyoto\'s word for geisha) or maiko (apprentice) hurrying to an evening appointment. The stone-paved streets and lantern light are pure old Kyoto.',
              details: [
                '🎭 Best geiko/maiko sighting: 5-6pm when they walk to evening engagements',
                '📸 Hanami-koji dori is the most photogenic street',
                '🏯 Yasaka Shrine at the end of Shijo-dori is beautiful and free',
                '⚠️ Don\'t chase or grab geiko/maiko for photos — it\'s considered rude'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Nishiki Market Grazing',
              description: 'Your lunch is the market itself. Graze through: grilled squid on a stick, freshly made yuba, pickled vegetables, mochi from Funahashiya, and matcha soft-serve. Budget ¥2,000-3,000pp for a feast.',
              meta: '💰 $$ · 📍 Nishiki Market · 🚫 Mostly pork-free (seafood/tofu focus) — just skip the nikuman'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Pontocho Alley',
              description: 'A narrow, atmospheric alley along the Kamo River lined with restaurants and bars. In May, many restaurants set up kawadoko (riverside dining platforms) over the water. Walking through the lantern-lit alley at dusk is peak Kyoto atmosphere.',
              details: [
                '🏮 One of Kyoto\'s most atmospheric streets at night',
                '🍽️ Kawadoko (river terrace dining) starts in May — magical',
                '📍 Parallel to Kamo River between Shijo and Sanjo bridges'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Hafuu (Pontocho)',
              description: 'Excellent Kyoto-style kushikatsu and yakitori in Pontocho. High-quality chicken skewers, seasonal vegetable tempura, and cold beer on the river terrace if weather allows. Refined Kyoto dining without the pretension.',
              meta: '💰 $$$ · 📍 Pontocho Alley · 🚫 Chicken/seafood/veggie focused — pork-free ordering easy'
            }
          ],
          tips: [
            { type: 'tip', text: 'Train back to Osaka takes 45 min on JR Special Rapid (covered by JR Pass). Last trains run until ~midnight. Don\'t stress about timing — you have plenty of evening to enjoy Kyoto.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari Taisha', num: 1, cat: 'attraction', desc: 'Thousands of vermillion torii gates — go at sunrise!' },
        { lat: 34.9650, lng: 135.7720, label: 'Rokujuan Tea House', num: 2, cat: 'food', desc: 'Premium Uji matcha ceremony near Fushimi Inari' },
        { lat: 35.0050, lng: 135.7649, label: 'Nishiki Market', num: 3, cat: 'food', desc: 'Kyoto\'s Kitchen — 130+ food and craft vendors' },
        { lat: 35.0037, lng: 135.7750, label: 'Gion District', num: 4, cat: 'attraction', desc: 'Historic geisha quarter with wooden tea houses' },
        { lat: 35.0037, lng: 135.7700, label: 'Pontocho Alley', num: 5, cat: 'food', desc: 'Atmospheric dining alley along the Kamo River' },
        { lat: 35.0036, lng: 135.7786, label: 'Yasaka Shrine', num: 6, cat: 'attraction', desc: 'Beautiful Shinto shrine at Gion\'s edge' }
      ]
    },
    {
      num: 8,
      date: '2026-05-22',
      neighborhoods: 'Osaka · Namba · Amerikamura · Tennoji',
      title: 'Osaka Deep Dive — Street Food, Shopping & teamLab',
      description: "A full Osaka day. Morning at Kuromon Market (Osaka's kitchen), afternoon shopping at Don Quijote and Surugaya, and evening at teamLab Botanical Garden in Nagai Park. This is the day you fall in love with Osaka's unapologetic food-obsessed culture.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kuromon Market ("Osaka\'s Kitchen")',
              description: 'Osaka\'s answer to Tsukiji — a 600m covered market street with 170+ stalls. Fresh sashimi, grilled seafood, uni, tamagoyaki, and the most incredible fruit you\'ve ever tasted (Japanese strawberries are next-level). Eat your way through for breakfast.',
              details: [
                '🐟 Must-try: fresh uni, grilled king crab legs, scallops',
                '🍓 Japanese strawberries and melons — expensive but transcendent',
                '🍳 Tamagoyaki stalls — egg omelette on a stick for kids',
                '⏰ Opens 8-9am · Go before 10am for best selection'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Kuromon Market Grazing',
              description: 'Breakfast of champions. Uni, sashimi, grilled scallops, tamagoyaki, and Japanese strawberries. Graze through the market stalls — each one is a tiny temple to a single ingredient.',
              meta: '💰 $$ · 📍 Kuromon Market · 🚫 Naturally pork-free (seafood focus)'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Don Quijote (Dotonbori) Shopping',
              description: 'The Osaka flagship — towering over Dotonbori with its Ferris wheel on the building (yes, really). Stock up on Japanese snacks, beauty products, souvenirs, toys, electronics, and random weirdness. Tax-free for tourists spending over ¥5,000.',
              details: [
                '🎡 The building has a Ferris wheel on its exterior (¥600)',
                '🛍️ Tax-free counter on upper floors — bring your passport',
                '🍬 Japanese snack aisle is DANGEROUS — buy everything',
                '🧴 Japanese beauty products (Shiseido, Canmake) at discount prices'
              ]
            },
            {
              title: 'Surugaya Osaka (Namba)',
              description: 'Vintage anime, manga, retro video games, figures, and collectibles. The Osaka branch has multiple floors of nostalgic treasures. Great for finding rare figures and old-school Japanese toys.',
              details: [
                '🎮 Retro Famicom/Super Famicom games',
                '📚 Vintage manga, trading cards, and figures',
                '📍 Multiple locations in Namba/Den-Den Town area'
              ]
            },
            {
              title: 'Amerikamura (American Village)',
              description: 'Osaka\'s youth fashion district — think Harajuku but grittier and more hip-hop influenced. Vintage clothing stores, street art, and Triangle Park where Osaka\'s cool kids hang out. Fun to walk through even with strollers.',
              details: [
                '👕 Vintage and streetwear shops everywhere',
                '🍦 Famous for "long softcream" — extra-tall soft-serve cones',
                '📍 Between Shinsaibashi and Namba — walkable from Dotonbori'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Mizuno Okonomiyaki (Dotonbori)',
              description: 'The most famous okonomiyaki restaurant in Osaka. Watch them make the savory pancake on a griddle in front of you. Order the seafood mix (no pork!) — squid, shrimp, and vegetables in a crispy batter with special sauce, mayo, and bonito flakes.',
              meta: '💰 $$ · 📍 Dotonbori · 🚫 Order seafood mix — "buta nashi de" (no pork)'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'teamLab Botanical Garden Osaka',
              description: 'teamLab has a permanent installation at Nagai Botanical Garden in Osaka! Walk through a digitally-transformed botanical garden at night — trees, flowers, and water features illuminated with interactive digital art. Different from teamLab Planets but equally magical.',
              details: [
                '🌿 Located in Nagai Park Botanical Garden',
                '🎟️ ¥1,600 adults, ¥500 ages 4-12 · Opens at sunset (~6:30pm May)',
                '🌙 The nighttime botanical garden is magical — different from Tokyo teamLab',
                '👶 Stroller-friendly outdoor paths',
                '📍 Nagai Station on Midosuji Line (~15 min from Namba)'
              ]
            }
          ],
          meals: [
            {
              type: '🌙 Late Night',
              name: 'Dotonbori Late-Night Street Food',
              description: 'Osaka never sleeps. After teamLab, hit Dotonbori again for takoyaki (octopus balls), yakitori, and taiyaki (fish-shaped waffle with custard or red bean). The neon is even more magical late at night.',
              meta: '💰 $ · 📍 Dotonbori · Open until 2-3am · 🚫 Takoyaki & yakitori are pork-free'
            }
          ],
          tips: [
            { type: 'tip', text: 'Osaka locals say "kuidaore" — "eat until you drop." This city is not joking about food. You will eat more today than any other day of the trip. Embrace it.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6690, lng: 135.5095, label: 'Kuromon Market', num: 1, cat: 'food', desc: 'Osaka\'s Kitchen — 170+ stalls of seafood heaven' },
        { lat: 34.6685, lng: 135.5020, label: 'Don Quijote Dotonbori', num: 2, cat: 'shopping', desc: 'Mega discount store with a Ferris wheel on the building' },
        { lat: 34.6700, lng: 135.5010, label: 'Surugaya Osaka', num: 3, cat: 'shopping', desc: 'Vintage anime, games, and collectibles' },
        { lat: 34.6726, lng: 135.4984, label: 'Amerikamura', num: 4, cat: 'attraction', desc: 'Osaka\'s youth fashion district' },
        { lat: 34.6313, lng: 135.5177, label: 'teamLab Botanical Garden', num: 5, cat: 'attraction', desc: 'Digital art in a nighttime botanical garden' },
        { lat: 34.6688, lng: 135.5015, label: 'Mizuno Okonomiyaki', num: 6, cat: 'food', desc: 'Osaka\'s most famous okonomiyaki — get seafood mix' }
      ]
    },
    {
      num: 9,
      date: '2026-05-23',
      neighborhoods: 'Kyoto · Arashiyama · Kinkaku-ji',
      title: 'Kyoto Day 2 — Bamboo Grove, Golden Temple & Tea',
      description: "Second Kyoto day trip — this time heading west to Arashiyama's famous bamboo grove and the Golden Pavilion (Kinkaku-ji). These are two of Japan's most photographed spots, and for good reason. The bamboo grove is otherworldly and the Golden Temple floating on its mirror lake will stop you in your tracks.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Arashiyama Bamboo Grove',
              description: 'Walk through a towering tunnel of bamboo that sways and creaks in the wind. The light filtering through thousands of bamboo stalks creates an ethereal green glow. Go early to beat the crowds — by 10am it\'s shoulder-to-shoulder.',
              details: [
                '🎋 Free, open 24/7 — go by 8am for the best experience',
                '📸 The iconic bamboo path is about 500m long',
                '👶 Stroller works on the main path but carriers are easier in crowds',
                '🐒 Iwatayama Monkey Park is nearby — 120 wild monkeys on a hilltop (20-min hike up, might be tough with toddlers)'
              ]
            },
            {
              title: 'Tenryu-ji Temple & Garden',
              description: 'A UNESCO World Heritage Zen temple right at the entrance to the bamboo grove. The garden is one of Kyoto\'s finest — a pond garden designed in 1339 that\'s barely changed. The borrowed scenery of Arashiyama mountains behind makes it breathtaking.',
              details: [
                '🏯 ¥500 garden only, ¥800 with temple buildings',
                '🌳 The Sogenchi Pond garden is a masterpiece of borrowed scenery',
                '🧘 Zen Buddhist temple — peaceful atmosphere'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Matcha Stop',
              name: '% Arabica Kyoto (Arashiyama)',
              description: 'The original % Arabica coffee shop, perched on the Arashiyama riverbank with views of the Togetsukyo Bridge and mountains. Their matcha latte is excellent, and the setting is unbeatable.',
              meta: '💰 $$ · 📍 Arashiyama riverbank · Matcha or coffee with mountain views'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kinkaku-ji (Golden Pavilion)',
              description: 'A Zen temple covered entirely in gold leaf, reflected perfectly in a mirror-like pond. It\'s as stunning as every photo you\'ve seen — more so in person. The walk-through garden takes about 30-45 minutes. One of those "we\'re really in Japan" moments.',
              details: [
                '✨ ¥500 adults, ¥300 kids · Your "ticket" is a beautiful calligraphy charm',
                '📸 The money shot: golden pavilion reflected in the pond from the main viewpoint',
                '⏰ Afternoon light (2-4pm) is beautiful on the gold leaf',
                '🍵 Matcha and sweets available at the exit tea garden'
              ]
            },
            {
              title: 'Togetsukyo Bridge & Arashiyama River',
              description: 'The iconic wooden bridge spanning the Oi River with mountains behind. In May the surrounding hills are lush green. Walk across, enjoy the views, and let the toddlers watch the boats on the river.',
              details: [
                '🌉 The bridge itself is the attraction — mountains and river views',
                '🚣 Tourist boats cruise the river — scenic from the bridge',
                '📸 Best photos from the south bank looking north toward the mountains'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Arashiyama Yoshimura (Soba)',
              description: 'Handmade soba noodles with a view of the Togetsukyo Bridge and mountains. The cold soba with tempura is perfect for a May afternoon. Buckwheat soba is naturally pork-free and one of Kyoto\'s specialties.',
              meta: '💰 $$ · 📍 Arashiyama · 🚫 Soba & tempura are pork-free'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Kyoto Station Ramen Street',
              description: 'Before catching the train back to Osaka, hit the ramen street on the 10th floor of Kyoto Station. Multiple shops including places with chicken and seafood broths. A warm bowl before the ride home.',
              details: [
                '🍜 10th floor of Kyoto Station — Kyoto Ramen Koji',
                '📍 Multiple shops — look for tori (chicken) or shoyu base',
                '🚫 Ask about broth base: "butaniku/tonkotsu nashi?" (no pork/pork broth?)'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Kyoto Ramen Street (chicken-broth shop)',
              description: 'End the Kyoto day with a steaming bowl of ramen. Menya Inoichi on Ramen Street offers a rich chicken paitan broth — no pork. Get the kids a small bowl and watch them slurp.',
              meta: '💰 $ · 📍 Kyoto Station 10F · 🚫 Choose chicken broth shops'
            }
          ],
          tips: [
            { type: 'tip', text: 'Arashiyama is west Kyoto, Kinkaku-ji is northwest. Bus #11 connects them in ~40 min, or take a taxi (~¥2,000). Combine both in one day to avoid extra Kyoto trips.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0170, lng: 135.6713, label: 'Arashiyama Bamboo Grove', num: 1, cat: 'attraction', desc: 'Towering bamboo tunnel — ethereal and iconic' },
        { lat: 35.0158, lng: 135.6745, label: 'Tenryu-ji Temple', num: 2, cat: 'attraction', desc: 'UNESCO Zen temple with stunning pond garden' },
        { lat: 35.0394, lng: 135.7292, label: 'Kinkaku-ji (Golden Pavilion)', num: 3, cat: 'attraction', desc: 'Gold-leaf temple reflected in a mirror pond' },
        { lat: 35.0115, lng: 135.6780, label: 'Togetsukyo Bridge', num: 4, cat: 'attraction', desc: 'Iconic wooden bridge spanning the Oi River' },
        { lat: 35.0120, lng: 135.6776, label: '% Arabica Kyoto', num: 5, cat: 'food', desc: 'Famous café with matcha lattes and river views' },
        { lat: 35.0125, lng: 135.6774, label: 'Arashiyama Yoshimura', num: 6, cat: 'food', desc: 'Handmade soba with bridge views' },
        { lat: 34.9858, lng: 135.7588, label: 'Kyoto Ramen Street', num: 7, cat: 'food', desc: 'Ramen alley on Kyoto Station 10F' }
      ]
    },
    {
      num: 10,
      date: '2026-05-24',
      neighborhoods: 'Osaka · Osaka Castle · Departure Prep',
      title: 'Final Day — Osaka Castle, Last Bites & Sayonara',
      description: "Your last full day in Japan. Morning at Osaka Castle (the kids will love running around the castle grounds), final shopping runs, and a farewell feast. Soak it all in — from the castle\'s park to one last round of takoyaki. Pack tonight and prep for departure tomorrow.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Osaka Castle & Castle Park',
              description: 'Osaka\'s iconic castle sits in a huge park with moats, stone walls, and open lawns. The castle museum inside tells Osaka\'s samurai history (8 floors, elevator available). The park grounds are perfect for a final morning — toddlers can run on the massive lawn while adults take in the views.',
              details: [
                '🏯 Castle museum: ¥600 adults, free under 15 · Opens 9am',
                '🌳 Castle Park is huge — lawns, moats, cherry trees (green in May)',
                '🛷 Playground near the southeast corner — great for toddlers',
                '📸 Best castle photo from the southwest angle across the inner moat'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Matcha Stop',
              name: 'Maru Sankaku Shikaku (Castle area)',
              description: 'A stylish matcha café near Osaka Castle serving thick Uji matcha, houjicha lattes, and beautiful Japanese sweets. One last matcha morning ritual before you leave Japan.',
              meta: '💰 $$ · 📍 Near Osaka Castle · Final matcha morning'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Last-Minute Shopping & Packing',
              description: 'Hit any stores you missed. Grab last-minute omiyage (souvenirs) from department store basements (depachika), pick up Japanese snacks for the flight home, and do a final Don Quijote run for anything forgotten.',
              details: [
                '🎁 Depachika (department store food basement) for beautiful packaged sweets',
                '🍬 Tokyo Banana, Royce chocolate, and matcha Kit-Kats make great gifts',
                '📦 Pack one bag of snacks for the plane — you\'ll thank yourself later'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Lunch',
              name: 'Harukoma Sushi (Tennoji)',
              description: 'A legendary standing sushi bar where pieces come at you fast across a counter. Ultra-fresh, no-frills nigiri at great prices. The perfect final Japanese meal — simple, fresh, and unforgettable. 100% pork-free.',
              meta: '💰 $$ · 📍 Tennoji area · 🚫 All fish — naturally pork-free'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Farewell Walk — Dotonbori One Last Time',
              description: 'Take one final walk down Dotonbori. Get one more round of takoyaki. Let the neon wash over you. Say goodbye to the running man. Japan will miss you and you will absolutely miss Japan.',
              details: [
                '🌃 The neon at night is the lasting image of Osaka',
                '📸 Final family photo at the Glico Running Man',
                '🐙 One last takoyaki — you deserve it'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Farewell Dinner',
              name: 'Yakiniku Rokka (Namba)',
              description: 'Go out with a bang at a premium yakiniku (Japanese BBQ) restaurant. Grill wagyu beef, chicken, and seafood at your table. Let the kids play with the tongs. Toast to an incredible trip over sizzling A5 beef.',
              meta: '💰 $$$ · 📍 Namba area · 🚫 Order beef/chicken/seafood — skip pork menu items'
            }
          ],
          tips: [
            { type: 'tip', text: 'If flying from KIX (Kansai Airport), the Haruka Express from Tennoji takes 35 min. Book your airport train tickets today. Give yourself 3 hours before an international flight with two toddlers — you\'ll need the buffer for diaper changes and terminal exploring.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6873, lng: 135.5262, label: 'Osaka Castle', num: 1, cat: 'attraction', desc: 'Iconic castle with museum and huge park' },
        { lat: 34.6687, lng: 135.5013, label: 'Dotonbori (Farewell Walk)', num: 2, cat: 'attraction', desc: 'One last neon-lit stroll and takoyaki' },
        { lat: 34.6515, lng: 135.5185, label: 'Harukoma Sushi', num: 3, cat: 'food', desc: 'Legendary standing sushi — fast, fresh, unforgettable' },
        { lat: 34.6680, lng: 135.5030, label: 'Yakiniku Rokka', num: 4, cat: 'food', desc: 'Premium wagyu BBQ — farewell feast' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$80–120/night', midrange: '$120–200/night', luxury: '$200–400/night' },
    { category: 'Meals (family of 5)', budget: '$50–80/day', midrange: '$80–150/day', luxury: '$150–300/day' },
    { category: 'Transport (JR Pass + IC)', budget: '$300 total', midrange: '$400 total', luxury: '$600 total (taxis)' },
    { category: 'Activities & Attractions', budget: '$20–40/day', midrange: '$40–80/day', luxury: '$80–150/day' },
    { category: 'Shopping & Souvenirs', budget: '$30/day', midrange: '$60/day', luxury: '$150/day' },
    { category: '10-Day Total (family)', budget: '$2,500–3,500', midrange: '$4,000–6,500', luxury: '$7,000–12,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There & Away', items: ['Arrive: Narita (NRT) → Narita Express to Shibuya (~90 min, ¥3,250)', 'Depart: Kansai International (KIX) → Haruka Express from Tennoji (~35 min, ¥1,800)', 'Shinkansen Tokyo→Osaka: 2h15m on Nozomi, 2h45m on Hikari (JR Pass covers Hikari only)', 'Activate 7-day JR Pass on May 18 or 19 for maximum Osaka/Kyoto/Nara coverage'] },
    { title: '🏨 Accommodation', items: ['Tokyo (May 15-19): Shibuya Airbnb — central, walkable to everything', 'Osaka (May 19-24): Stay in Namba/Shinsaibashi area for Dotonbori access', 'Family rooms are standard in Japan — many hotels have triple rooms', 'Airbnbs often have washing machines — essential for 10-day family trips'] },
    { title: '🍼 Toddler Essentials', items: ['Diapers: Merries or Moony brand at any drug store (Matsumoto Kiyoshi) or Don Quijote', 'Baby food: 7-Eleven and Lawson carry pouches; drug stores have Japanese baby food', 'Stroller: Bring a lightweight umbrella stroller — you\'ll walk 15-20k steps/day', 'Nursing rooms: Department stores, train stations, and malls have excellent nursing rooms'] },
    { title: '🚫 No-Pork Survival Guide', items: ['Learn: 豚 (buta) = pork, 豚骨 (tonkotsu) = pork bone broth', 'Safe bets: yakitori (chicken), sashimi/sushi, gyukatsu (beef cutlet), tempura, soba', 'Risky: ramen (check broth), gyoza (usually pork), curry (often pork), nikuman (pork bun)', 'Magic phrase: "Butaniku nashi de onegaishimasu" = "Without pork, please"', 'Show your phone: keep a note in Japanese explaining your dietary restriction'] },
    { title: '📱 Connectivity & Apps', items: ['Get a pocket WiFi or eSIM (Ubigi, Airalo) before arriving', 'Google Maps works perfectly in Japan for transit directions', 'Download: Suica app (IC card), Google Translate (offline Japanese), Tabelog (restaurant reviews)', 'Line Pay and PayPay are common mobile payment apps'] }
  ]
};

fulfillOrder(order, itineraryData)
  .then(result => {
    console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
  })
  .catch(err => {
    console.error('❌ Error:', err.message);
    process.exit(1);
  });
