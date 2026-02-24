const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771925457294_4zd7dh',
  email: 'chtnphani@gmail.com',
  destination: 'Tokyo, Japan',
  startDate: '2026-03-13',
  endDate: '2026-03-18',
  groupSize: '3-4',
  travelStyle: 'Family-friendly',
  dining: 'Mix of everything',
  budget: '',
  requests: ''
};

const itineraryData = {
  destination: 'Tokyo, Japan',
  countryEmoji: '🇯🇵',
  title: 'Tokyo with Kids — Sakura Season & Big City Magic',
  subtitle: '6 days of cherry blossoms, ramen, anime, temples & teamLab wonders for the whole family',
  description: "Tokyo is one of the world's great family destinations — and you've landed at the most magical time of year. Mid-March in Tokyo means the first sakura blossoms are beginning to open across the city, filling parks and canal paths with soft pink clouds. For families, Tokyo is surprisingly gentle: trains run on time, streets are safe and clean, kids are welcomed everywhere, and the city effortlessly balances ancient shrines with robot restaurants and glowing digital art museums. This itinerary moves at a sustainable pace — big highlights with breathing room — covering Asakusa's temples, Harajuku's playful energy, teamLab's immersive digital worlds, Akihabara's pop culture explosion, and the best ramen, sushi, and street food Tokyo has to offer. Buckle up: Tokyo is going to earn permanent residence in your family's collective memory.",
  duration: '5 nights',
  dates: 'Mar 13 – Mar 18, 2026',
  budget: '$$–$$$',
  pace: 'Moderate',
  bestFor: 'Families with kids',

  highlights: [
    'Cherry blossom season begins — early blooms at Ueno Park, Chidorigafuchi & Shinjuku Gyoen',
    'teamLab Planets: walk through shimmering digital waterfalls and floating flowers (kids go crazy for it)',
    'Senso-ji Temple complex — ancient Asakusa in the golden morning light',
    'Meiji Shrine forest walk + Harajuku\'s Takeshita Street rainbow crepes and kawaii culture',
    'Akihabara electronics paradise & Shibuya\'s legendary 150-person pedestrian scramble crossing',
    'Fresh tuna breakfast at Tsukiji Outer Market followed by the best sushi of your life'
  ],

  essentials: [
    {
      title: '🌸 Cherry Blossom Timing',
      text: 'Mid-March is the very start of sakura season — you\'ll likely catch early blooms rather than full peak bloom (which typically hits late March/early April). Ueno Park, Chidorigafuchi moat, Shinjuku Gyoen, and Nakameguro Canal are top spots. Check the Japan Meteorological Corporation\'s official forecast close to your trip. Even partial blooms are breathtaking.'
    },
    {
      title: '🚇 Getting Around',
      text: 'Tokyo\'s subway is the backbone of the city. Get a Suica or Pasmo IC card at the airport — tap in and out of every train and bus, works at convenience stores too. The JR Yamanote Line loops the city\'s main hubs (Shinjuku, Harajuku, Shibuya, Akihabara, Ueno, Tokyo). For a family of 4, cabs are reasonable for short hops after 9pm. Google Maps is perfect for navigation.'
    },
    {
      title: '🌡️ March Weather',
      text: 'March in Tokyo means mild but unpredictable weather: daytime 10–17°C (50–63°F), cooler at night. Pack layers — a light jacket, comfortable walking shoes, and a compact umbrella. March can have rainy spells. If it rains during cherry blossom time, it\'s called "sakura nagashi" (the petals fall like rain). Beautiful in its own way.'
    },
    {
      title: '💴 Money & Practicalities',
      text: 'Japan remains largely cash-preferring. Hit a 7-Eleven or Japan Post ATM on arrival — they reliably accept foreign cards. Budget ¥2,000–3,000 per person per meal at mid-range restaurants. 7-Eleven, FamilyMart, and Lawson convenience stores (コンビニ) are incredible for onigiri, sandwiches, hot food, and snacks at any hour. Get a pocket WiFi or local SIM at the airport.'
    }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-13',
      neighborhoods: 'Shinjuku · Shinjuku Gyoen · Kabukicho',
      title: 'Arrive in Tokyo — Shinjuku First Night',
      description: "Touch down at Narita or Haneda and ride the train straight into one of the world's greatest cities. Shinjuku is the perfect base for a family — central, full of food options, with the stunning Shinjuku Gyoen garden just a short walk away. Tonight, ease in: find your rhythm, explore the neighborhood, and let Tokyo begin working its magic.",
      timeBlocks: [
        {
          label: 'Arrival & Afternoon',
          activities: [
            {
              title: 'Arrive & Transfer to Shinjuku',
              description: "From Narita Airport, take the Narita Express (N'EX) to Shinjuku — about 90 minutes, clean and comfortable. From Haneda, take the Tokyo Monorail to Hamamatsucho then the Yamanote Line to Shinjuku (about 40 minutes). Check in, drop your bags, and take your first steps in Tokyo.",
              details: [
                '✈️ Narita → Shinjuku: N\'EX Limited Express — ¥3,250 per adult, ¥1,630 per child',
                '✈️ Haneda → Shinjuku: Tokyo Monorail + Yamanote Line — ¥700 per person',
                '🏨 Recommended areas: Shinjuku (central), Asakusa (traditional) — both great for families',
                '🎒 Store large luggage at your hotel; most allow early check-in luggage drop',
                '💴 Get Suica/Pasmo IC cards at the airport — use for all trains, buses & 7-Eleven'
              ]
            },
            {
              title: 'Shinjuku Gyoen National Garden',
              description: "If the timing works, stop at Shinjuku Gyoen on your first afternoon. This 144-acre garden is one of Japan's finest — a serene mix of French formal garden, English landscape garden, and Japanese traditional garden. In mid-March, early-blooming cherry trees (kanzakura, kawazu-zakura) may already be showing color while the famous somei yoshino varieties are still budding. A gentle, beautiful way to arrive in Tokyo.",
              details: [
                '🌸 Entry: ¥500 adults, ¥250 children · Open 9am–4:30pm (closed Monday)',
                '🌳 The hothouse greenhouse is great for kids — tropical plants, giant water lilies',
                '📍 5-minute walk from Shinjuku Gyoenmae subway station',
                '☀️ The French garden\'s central lawns are perfect for a first-day picnic rest'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Your first evening, resist the urge to plan too much. A stroll through Shinjuku\'s backstreets and a bowl of ramen is the perfect jet-lag cure. The body needs food and movement, not a packed schedule.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Kabukicho Night Walk (Family-Friendly)',
              description: "Kabukicho is Shinjuku's famous entertainment district — and the neon-lit Kabukicho Tower and Robot Restaurant area are genuinely spectacular for kids at night, even if you don't dine there. Walk to Omoide Yokocho (Memory Lane) — a tiny alley of yakitori stalls where smoke curls into the neon sky. It looks exactly like a Studio Ghibli film.",
              details: [
                '🍢 Omoide Yokocho: grilled skewers from ¥200–400 each — point and order',
                '🤖 Kabukicho Tower\'s exterior and Godzilla Hotel sign make great first Tokyo photos',
                '🌃 Shinjuku at night is all sensory overload — let kids take it in at their pace',
                '⚠️ Stick to well-lit main streets in Kabukicho — it\'s safe for families but lively'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Ichiran Ramen, Shinjuku',
              description: 'The perfect first dinner in Tokyo. Ichiran is famous for its solo dining booths and deeply customizable tonkotsu ramen — you fill out a flavor sheet (spice level, richness, noodle firmness), push it under the curtain, and a perfect bowl appears. Kids absolutely love the "secret booth" experience. The broth is deeply savory and rich.',
              meta: '💰 ¥1,000–1,400 per person · 📍 Multiple locations around Shinjuku · Open 24 hours'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6938, lng: 139.7036, label: 'Shinjuku Station', num: 1, cat: 'attraction', desc: 'Your main hub — world\'s busiest train station, surrounded by shops, food & hotels' },
        { lat: 35.6851, lng: 139.7103, label: 'Shinjuku Gyoen National Garden', num: 2, cat: 'attraction', desc: 'Magnificent 144-acre garden — early cherry blossoms possible in mid-March' },
        { lat: 35.6960, lng: 139.7036, label: 'Kabukicho Entertainment District', num: 3, cat: 'attraction', desc: 'Neon-lit streets, Godzilla Hotel, Robot Restaurant — spectacular for kids at night' },
        { lat: 35.6940, lng: 139.7003, label: 'Omoide Yokocho (Memory Lane)', num: 4, cat: 'food', desc: 'Tiny Ghibli-like alley of yakitori smoke and neon — Tokyo at its most atmospheric' },
        { lat: 35.6916, lng: 139.7001, label: 'Ichiran Ramen Shinjuku', num: 5, cat: 'food', desc: 'First night ramen ritual — customizable tonkotsu in a solo booth, kids love it' }
      ]
    },
    {
      num: 2,
      date: '2026-03-14',
      neighborhoods: 'Asakusa · Nakamise · Ueno Park · Yanaka',
      title: 'Old Tokyo — Senso-ji, Ueno & First Sakura',
      description: "Asakusa is where old Edo-era Tokyo breathes. Wander through the great Senso-ji Temple complex early in the morning before the crowds arrive, browse Nakamise shopping street for ninja headbands and mochi, then head to Ueno Park where the cherry trees are beginning to wake up. Finish in the charming, cat-filled backstreets of Yanaka — one of the neighborhoods that survived the WWII bombing raids and still looks like 1960s Tokyo.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Senso-ji Temple Complex — Asakusa',
              description: "Tokyo's oldest and most famous temple complex. Enter through the Kaminarimon (Thunder Gate) with its enormous red lantern, walk Nakamise shopping street, and arrive at the main temple hall where incense smoke curls toward the sky. Kids can try fortune sticks (omikuji) for ¥100 — they shake a metal cylinder and a numbered stick falls out, then find the matching fortune drawer. Even before full cherry bloom, the gardens around Senso-ji have early-blooming varieties.",
              details: [
                '⛩️ Free to enter · Open 24 hours (temple grounds) · Main hall 6am–5pm',
                '👺 Nakamise Street: 200m corridor of traditional shops — snacks, toys, ninja goods, fans',
                '🎋 Omikuji fortune sticks: ¥100 per draw — if you get a bad fortune, tie it to the rack',
                '🕕 Arrive before 8am to have the temple largely to yourselves — magical atmosphere'
              ]
            },
            {
              title: 'Nakamise Shopping Street',
              description: "The covered shopping arcade leading to Senso-ji is lined with 89 small shops selling traditional crafts, snacks, and souvenirs. Excellent for first-day souvenir hunting. Try ningyo-yaki (small sponge cakes stuffed with red bean paste shaped like Senso-ji landmarks), get matching happi coats for the family, or pick up folding fans. Budget ¥1,000–2,000 per person for fun shopping.",
              details: [
                '🎎 Best souvenir spots: traditional fans, tenugui (hand towels), lucky cats, ninja sets',
                '🧁 Must try: ningyo-yaki (red bean cakes, ¥200–300), melonpan from street stalls',
                '📸 The view back through Kaminarimon gate from inside Nakamise is a perfect photo',
                '⏰ Open from ~9am, shops busiest mid-morning and afternoon'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Pelican Café, Asakusa',
              description: 'A beloved local bakery in Asakusa with thick toast, warm coffee, and a neighborhood vibe completely free of tourist crowds. Their pain de mie toast is legendary — thick, pillowy slices served with butter and jam. Opens early and fills with locals before 9am.',
              meta: '💰 ¥400–800 · 📍 Kuramae, 5-min taxi from Senso-ji · Open 9am–5pm, closed Sunday'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ueno Park — Cherry Blossoms Begin',
              description: "A 10-minute walk from Asakusa, Ueno Park is one of Tokyo's most famous hanami (flower-viewing) spots, lined with 1,000+ cherry trees. In mid-March, the somei yoshino trees are typically budding and the early varieties may be showing color — you might catch the very beginning of the bloom. The park also contains the Tokyo National Museum, Ueno Zoo, Shinobazu Pond, and multiple smaller shrines.",
              details: [
                '🌸 Even early-season, the park atmosphere is festive — vendors sell sakura snacks and beer',
                '🦒 Ueno Zoo: ¥600 adults, ¥300 under 12 · Home to Japan\'s giant pandas',
                '🏛️ Tokyo National Museum: ¥1,000 adults, free under 18 — incredible samurai armor and Buddhist art',
                '🦢 Shinobazu Pond: row a swan paddle boat (¥700 for 30 min) — kids love it'
              ]
            },
            {
              title: 'Yanaka Ginza — Old Tokyo Backstreets',
              description: "A 15-minute walk north from Ueno, Yanaka Ginza is a shopping street frozen in time — a covered shotengai (old-style arcade) with local butchers, pickle shops, cat-themed cafes, and handmade sembei rice crackers. The surrounding Yanaka neighborhood has wooden temple alleys and a historic cemetery that feels like stepping into 1960s Japan. Cats are everywhere and they're friendly.",
              details: [
                '🐱 Yanaka is famous for its community cats — stop for photos freely',
                '🍡 Try menchi-katsu (fried meat patty), croquettes, or fresh dango on a stick from stalls',
                '⛩️ Yanaka Cemetery: peaceful walk through old Tokyo — cherry trees line the main path',
                '📍 Access via Nippori Station (JR Yamanote Line)'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Otafuku, Asakusa',
              description: 'A 100-year-old oden shop in Asakusa — Japan\'s ultimate comfort food. Oden is a slow-simmered broth filled with daikon radish, tofu, fish cake, and soft-boiled eggs. Perfect for a chilly March afternoon. A totally authentic, non-touristy experience in the middle of tourist central.',
              meta: '💰 ¥1,200–1,800 · 📍 Senso-ji area, Asakusa · Open 11am, closed some weekdays'
            },
            {
              type: '🍽️ Dinner',
              name: 'Kappabashi Dori → Unatoto Unagi, Ueno',
              description: 'After Yanaka, head back toward Ueno for unagi (freshwater eel) dinner — a Japanese family classic. Unatoto is an affordable chain with excellent donburi (eel over rice bowls). Unagi is considered a stamina food in Japan — perfect fuel for a day of walking.',
              meta: '💰 ¥1,500–2,500 per person · 📍 Multiple locations near Ueno · No reservation needed'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: 'Senso-ji Temple', num: 1, cat: 'attraction', desc: 'Tokyo\'s most iconic temple — Kaminarimon gate, incense smoke, fortune sticks' },
        { lat: 35.7143, lng: 139.7964, label: 'Nakamise Shopping Street', num: 2, cat: 'attraction', desc: 'Traditional souvenir lane leading to Senso-ji — ninja gear, rice crackers, fans' },
        { lat: 35.7139, lng: 139.7732, label: 'Ueno Park', num: 3, cat: 'attraction', desc: 'Famous hanami spot — 1,000+ cherry trees, Ueno Zoo, Tokyo National Museum' },
        { lat: 35.7188, lng: 139.7767, label: 'Tokyo National Museum', num: 4, cat: 'attraction', desc: 'World-class samurai armor, Buddhist sculpture — free for under 18' },
        { lat: 35.7129, lng: 139.7755, label: 'Ueno Zoo', num: 5, cat: 'attraction', desc: 'Giant pandas + 400 species — a must for families with young kids' },
        { lat: 35.7267, lng: 139.7663, label: 'Yanaka Ginza', num: 6, cat: 'attraction', desc: 'Old-Tokyo shopping street with cats, croquettes, and zero tourists' },
        { lat: 35.7081, lng: 139.7943, label: 'Otafuku Oden, Asakusa', num: 7, cat: 'food', desc: '100-year-old oden restaurant — warm broth, daikon, tofu, fish cake' }
      ]
    },
    {
      num: 3,
      date: '2026-03-15',
      neighborhoods: 'Toyosu · Odaiba · teamLab Planets · Shinonome',
      title: 'Digital Wonders — teamLab Planets & Odaiba',
      description: "This is the day the kids will talk about for years. teamLab Planets in Toyosu is one of the world's most extraordinary art experiences — a series of large-scale, fully immersive digital rooms where you walk barefoot through shallow water while the walls, floor, and ceiling become shimmering galaxies, flowing flowers, and pulsing creatures. Afterward, the Odaiba waterfront offers a full afternoon of family fun: a giant Gundam robot, a Tokyo skyline backdrop, and the best views of Rainbow Bridge at sunset.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'teamLab Planets, Toyosu',
              description: "Book tickets in advance online — this is the single most popular attraction with families in Tokyo and timed slots sell out weeks ahead. You enter barefoot and wade through shallow water into rooms where the digital art surrounds you completely: a room of ten thousand falling flowers, a universe of floating lights you can bat with your hands, a mirrored space filled with watermelons that glow as you walk past them. Children lose their minds. Adults cry. It's one of those experiences.",
              details: [
                '🎟️ BOOK ONLINE BEFORE YOUR TRIP: teamlab.art/e/planets — Timed entry, sells out',
                '💰 ¥3,200 adults (¥2,200 discount if booked in advance) · ¥1,000 under 15 · Free under 3',
                '🦶 Go barefoot — you will wade through water! Wear easy-to-remove shoes, no socks with holes',
                '📍 Toyosu Station on the Yurikamome Line (20 min from Shinjuku area)',
                '⏰ Mornings are least crowded — aim for the 10am slot if available',
                '📵 Photography is allowed and encouraged — phones stay in pockets during water rooms though'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Odaiba Waterfront & DiverCity Tokyo',
              description: "Take the futuristic Yurikamome monorail from Toyosu over Rainbow Bridge to Odaiba — the artificial island in Tokyo Bay with sweeping views of the city skyline. The crown jewel is the life-size (18m tall) RX-78-2 Gundam statue at DiverCity Tokyo Plaza, which lights up and moves its head. For gaming and anime fans of any age, the Gundam Base inside is incredible. The waterfront promenade has a perfect view of Tokyo Tower and Rainbow Bridge.",
              details: [
                '🤖 Gundam Statue: Free to view outside DiverCity · Open plaza hours until 9pm',
                '🏪 DiverCity Tokyo Mall: Gundam Base, anime shops, Joypolis indoor theme park',
                '🌉 Rainbow Bridge: walk or take the free shuttle bus across for bay views',
                '🗼 Best spot to photograph Rainbow Bridge + Tokyo Tower together: Odaiba seaside park',
                '🎮 SEGA Joypolis: indoor theme park for older kids — ¥800 entry + ride tickets'
              ]
            },
            {
              title: 'Odaiba Seaside Park & Aqua City',
              description: "Walk south along Odaiba's waterfront park for the best views of Rainbow Bridge and the Tokyo skyline. Aqua City Odaiba is a large mall with a rooftop terrace that gives a spectacular view of the bay. The fake Statue of Liberty (a 1/7 replica gifted by France in 1998) is right here — great for photos with a backdrop of the real Tokyo Tower across the water.",
              details: [
                '🗽 Statue of Liberty replica: free to visit, great photo prop',
                '🛍️ Aqua City Odaiba: rooftop observation deck (free) with bay views — go at sunset',
                '🍜 Decks Tokyo Beach mall: excellent food court with ramen, sushi, and takoyaki options',
                '⛵ Tokyo Water Bus: scenic boat back to central Tokyo (Hinode Pier → Asakusa route)'
              ]
            }
          ],
          meals: [
            {
              type: '🍡 Lunch',
              name: 'Tsukishima Monja Street (en route)',
              description: 'If you\'re heading to Odaiba via Tsukishima, stop for monjayaki — Tokyo\'s answer to okonomiyaki (savory pancake). The fun part: you cook it yourself on a teppan griddle at your table. Kids love it. Tsukishima is famous for monja and the whole street is dedicated to it.',
              meta: '💰 ¥1,500–2,000 per person · 📍 Tsukishima Station (Yurakucho/Oedo lines) · Lunchtime not crowded'
            },
            {
              type: '🍽️ Dinner',
              name: 'Sushi at Conveyor Belt — Hamazushi or Kura Sushi, Odaiba',
              description: 'Kaitenzushi (conveyor belt sushi) is a quintessential Tokyo family meal. Plates circle on a belt, you grab what you want, and pay per plate at the end. Both Hamazushi and Kura Sushi use tablet ordering for anything not on the belt. Kids go berserk for it. Each plate is typically ¥130–220. Order maguro (tuna), salmon, and for the brave, uni (sea urchin).',
              meta: '💰 ¥1,000–2,000 per person · 📍 Multiple chains in DiverCity and Aqua City Odaiba'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6541, lng: 139.7944, label: 'teamLab Planets, Toyosu', num: 1, cat: 'attraction', desc: 'World\'s greatest immersive digital art experience — MUST book tickets in advance' },
        { lat: 35.6272, lng: 139.7773, label: 'DiverCity Tokyo Plaza', num: 2, cat: 'attraction', desc: '18m life-size Gundam statue + Gundam Base store — anime paradise for the family' },
        { lat: 35.6244, lng: 139.7756, label: 'Odaiba Seaside Park', num: 3, cat: 'attraction', desc: 'Best views of Rainbow Bridge and Tokyo skyline — sunset golden hour perfection' },
        { lat: 35.6268, lng: 139.7766, label: 'Aqua City Odaiba', num: 4, cat: 'attraction', desc: 'Waterfront mall with rooftop terrace, Statue of Liberty replica, and great food' },
        { lat: 35.6327, lng: 139.7781, label: 'Rainbow Bridge', num: 5, cat: 'attraction', desc: 'Iconic suspension bridge connecting Odaiba to central Tokyo — walk or take the bus' },
        { lat: 35.6644, lng: 139.7835, label: 'Tsukishima Monja Street', num: 6, cat: 'food', desc: 'Tokyo\'s monjayaki district — cook your own savory pancake on a teppan table' }
      ]
    },
    {
      num: 4,
      date: '2026-03-16',
      neighborhoods: 'Harajuku · Meiji Shrine · Shibuya · Daikanyama',
      title: 'Meiji Shrine, Harajuku Kawaii & Shibuya Scramble',
      description: "Today covers Tokyo's most photogenic and culturally rich pocket: the ancient Meiji Shrine forest, the exuberantly weird Harajuku Takeshita Street, the leafy boutique lanes of Omotesando, and the sensory overload of Shibuya — culminating in standing at the center of the world's most famous pedestrian crossing. A day that manages to be serene, silly, and spectacular all at once.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Meiji Jingu Shrine — Forest Walk',
              description: "One of Tokyo's most peaceful experiences: a walk through the towering forest surrounding Meiji Shrine, dedicated to Emperor Meiji and Empress Shoken. The forest — 70,000 trees donated from across Japan — feels impossibly vast and silent given that Shinjuku's skyscrapers are minutes away. Walk the gravel path, pass through the massive torii gate, and reach the main shrine. If timing is right, you may witness a traditional wedding procession in white kimono.",
              details: [
                '⛩️ Free to enter · Open sunrise to sunset (approx 5:40am–5:30pm in March)',
                '🌲 The 700m walk from the outer torii gate to the main shrine through forest is the whole point',
                '🎋 Sake barrel display at the entrance: 300+ barrels of sake donated to the shrine — great photo',
                '👰 Traditional Shinto weddings often happen mid-morning on weekends — look for the procession',
                '📍 Harajuku Station (JR Yamanote Line) — shrine entrance is right outside'
              ]
            },
            {
              title: 'Yoyogi Park Stroll',
              description: "Adjacent to Meiji Shrine, Yoyogi Park is Tokyo's most relaxed public park — the city's answer to Central Park. In mid-March, early cherry blossoms may dot the park edges. Locals jog, cyclists loop, and families spread picnic sheets. A nice 20-minute walk before the energy of Harajuku.",
              details: [
                '🌸 West side of the park has a grove of early-blooming cherry trees',
                '🎸 On weekends, buskers and dance groups often perform near the south entrance',
                '🌳 The park connects directly to Harajuku\'s main streets — walk south to exit near Takeshita St'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Little Nap Coffee Stand, Yoyogi',
              description: 'A beloved Tokyo specialty coffee micro-stand near Yoyogi Park. Single-origin pour-overs in a tiny space beloved by designers and architects. Pair with a croissant from the neighboring bakery. A refined morning fuel-up before the Meiji Shrine walk.',
              meta: '💰 ¥500–700 · 📍 5-6 Motoyoyogi-cho, Shibuya · Opens 9am · Standing-only space, quick stop'
            }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Takeshita Street, Harajuku — Kawaii Central',
              description: "Welcome to the most concentrated dose of Japanese pop culture anywhere on earth. Takeshita Street (竹下通り) is a 350-meter pedestrian lane crammed with crepe stands, rainbow cotton candy, unicorn-printed everything, and fashion that defies description. Kids absolutely love it and the energy is genuinely joyful. The street is busiest on weekends but always vibrant. Budget ¥1,500–2,000 per person for the inevitable crepe-and-trinket budget.",
              details: [
                '🌈 Crepe stands: Harajuku is famous for them — try strawberry cream with Nutella',
                '🍬 Rainbow candy floss (cotton candy on a stick in pastel swirls): ¥600–800',
                '👾 Marion Crepes: the original Harajuku crepe since 1976 — try the classic banana/chocolate',
                '👗 6%DOKIDOKI: the flagship kawaii fashion boutique (upstairs) — window displays are art',
                '⏰ Even in March, this lane is packed by 11am — arrive by 10:30 for easier navigation'
              ]
            },
            {
              title: 'Omotesando — Luxury Lane Walk',
              description: "A 5-minute walk from Takeshita, Omotesando is Tokyo's answer to the Champs-Élysées — tree-lined, wide, and flanked by flagship stores designed by the world's top architects. Even if you\'re not buying, the buildings alone are worth walking past: Prada by Herzog & de Meuron, Dior by SANAA, Tod's designed like a tree. At the end, Omotesando Hills shopping complex is built into the hillside.",
              details: [
                '🏛️ Architecture walk: spot the LVMH building, Prada\'s glass mesh facade, and the Gyre complex',
                '🍦ソフトクリーム: Japanese soft serve ice cream stands are scattered throughout — flavors include matcha, black sesame, strawberry',
                '🛍️ Kiddy Land toy store on the side street is a Tokyo institution — Pokemon, Ghibli, Hello Kitty'
              ]
            }
          ]
        },
        {
          label: 'Afternoon & Evening',
          activities: [
            {
              title: 'Shibuya Crossing & Scramble Square',
              description: "The Shibuya Scramble Crossing is the most famous intersection on earth — up to 3,000 people cross from all directions simultaneously when the lights change. Walk it first, then head up to Shibuya Sky (Scramble Square skyscraper observatory) for the best aerial view of the crossing and the entire Tokyo skyline. The outdoor rooftop at 230m is truly breathtaking — especially at sunset.",
              details: [
                '🚦 Cross the scramble yourself first — it\'s gentler than it looks, everyone flows',
                '🏙️ Shibuya Sky: ¥2,000 adults, ¥1,200 children (under 12) — BOOK ONLINE to guarantee entry',
                '🌇 The hour before sunset gives you golden hour AND the neon turning on — perfect timing',
                '📸 The outdoor rooftop has clear glass railings — incredible for photos',
                '⏰ Sunset in mid-March: around 5:45pm JST — arrive Shibuya Sky by 4:30pm'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Afuri Ramen, Harajuku',
              description: 'Harajuku\'s best ramen spot — Afuri is famous for its yuzu shio (citrus salt) broth, lighter and more fragrant than the rich Hokkaido-style tonkotsu. The broth is almost clear with a gorgeous yuzu aroma. Excellent vegan options too. The minimalist interior makes it feel like eating in a design studio.',
              meta: '💰 ¥1,200–1,600 · 📍 1-1-7 Jingumae, Harajuku · Usually a queue — aim for 11:30am'
            },
            {
              type: '🍽️ Dinner',
              name: 'Genki Sushi Shibuya / Shabusen Shibuya',
              description: 'For a family group, Shabusen in Shibuya is a fantastic shabu-shabu experience — you cook thin-sliced beef and vegetables in bubbling broth at your table and dip in ponzu or sesame sauce. All-you-can-eat sets available (¥2,500–3,500 per person). A sociable, interactive dinner perfect for families. Kids love cooking their own food.',
              meta: '💰 ¥2,500–3,500 per person · 📍 Shibuya Scramble Square B1 and Shibuya 109 building · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6763, lng: 139.6993, label: 'Meiji Jingu Shrine', num: 1, cat: 'attraction', desc: 'Ancient forested shrine — 700m walk through towering trees, Shinto ceremonies' },
        { lat: 35.6713, lng: 139.6942, label: 'Yoyogi Park', num: 2, cat: 'attraction', desc: 'Tokyo\'s Central Park — early cherry blossoms possible, weekend buskers and cyclists' },
        { lat: 35.6710, lng: 139.7034, label: 'Takeshita Street, Harajuku', num: 3, cat: 'attraction', desc: 'Kawaii culture explosion — rainbow crepes, cotton candy, pop fashion, pure joy' },
        { lat: 35.6656, lng: 139.7077, label: 'Omotesando Boulevard', num: 4, cat: 'attraction', desc: 'Tokyo\'s luxury tree-lined avenue — designer flagship stores in architectural masterpieces' },
        { lat: 35.6591, lng: 139.7006, label: 'Shibuya Scramble Crossing', num: 5, cat: 'attraction', desc: 'World\'s most famous pedestrian crossing — 3,000 people surge from all directions' },
        { lat: 35.6583, lng: 139.7025, label: 'Shibuya Sky Observatory', num: 6, cat: 'attraction', desc: 'Rooftop at 230m — aerial view of the crossing and entire Tokyo skyline at sunset' },
        { lat: 35.6692, lng: 139.7049, label: 'Afuri Ramen Harajuku', num: 7, cat: 'food', desc: 'Light yuzu shio broth ramen — a Tokyo classic in minimalist Harajuku setting' }
      ]
    },
    {
      num: 5,
      date: '2026-03-17',
      neighborhoods: 'Tsukiji · Ginza · Akihabara · Chidorigafuchi',
      title: 'Tsukiji Market, Akihabara & Cherry Blossom Moat',
      description: "Start with the freshest fish breakfast you\'ve ever eaten at the legendary Tsukiji Outer Market, then walk to Ginza for some urban browsing. The afternoon belongs to Akihabara — Tokyo\'s electric town where anime, manga, retro video games, and robot figurines compete for your attention on six floors of joyful chaos. Then, as the sun drops, make your way to Chidorigafuchi for what may be your first magical sakura evening — the moat path lined with cherry trees reflects shimmering blossoms in the green water below.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tsukiji Outer Market — Breakfast',
              description: "The famous Tsukiji Inner Market moved to Toyosu in 2018, but the Outer Market remains very much alive — a labyrinth of stalls selling fresh seafood, tamagoyaki (sweet rolled omelette), pickles, dashi, knives, and of course sushi and sashimi from tiny counters. Come hungry at 8-9am when it\'s freshest. The best activity: buy fresh seafood at the stalls and eat it standing at the counter. Tamago on a stick, fresh uni spoons, grilled scallops with butter.",
              details: [
                '🐟 Best for: fresh oysters, tamago sushi, grilled scallops, uni (sea urchin) on crackers',
                '⏰ Arrive 8-9:30am for the best selection and freshest stock',
                '💴 Budget ¥2,000-3,500 per person for a full street breakfast grazing experience',
                '📍 Tsukiji Station (Hibiya Line) or 10-min walk from Ginza',
                '🍣 Sushi Dai and Daiwa Sushi in the outer market area still have lines — arrive early or skip lines at smaller counters'
              ]
            }
          ],
          meals: [
            {
              type: '🍣 Breakfast',
              name: 'Tsukiji Outer Market Stalls',
              description: 'The ultimate Tokyo food experience — graze through the market stalls eating things on sticks. Must-tries: tamagoyaki (sweet rolled egg on a stick, ¥100), fresh oysters with lemon (¥200-300 each), grilled scallop with soy butter (¥500), and if the queue is short, a sushi breakfast set at one of the small sushi counters.',
              meta: '💰 ¥1,500–3,000 per person · 📍 Tsukiji (Chuo-ku) · Best 8–10am'
            }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Ginza Walk & Itoya Stationery',
              description: "A 10-minute walk from Tsukiji, Ginza is Tokyo's most prestigious shopping district — the Fifth Avenue of Japan. You don't need to shop to enjoy the architecture and energy. The one essential stop: Itoya (伊東屋), a 12-floor stationery and art supply store at the corner of Ginza Chome. Even non-stationery people find it magical. Kids love the craft supplies floor.",
              details: [
                '📝 Itoya: the world\'s finest stationery store — 12 floors of pens, paper, notebooks, and craft supplies',
                '🏛️ Ginza Six: enormous luxury mall with a rooftop garden — free to access',
                '🌆 The main Ginza street (Chuo-dori) goes car-free on weekend afternoons — very pleasant walk',
                '☕ Café de l\'Ambre: legendary Tokyo coffee shop since 1948 — aged single-origin brews'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Akihabara — Electric Town Explosion',
              description: "Akihabara (秋葉原) is a full sensory experience unlike anything else on earth. Buildings stacked floor to floor with electronics, anime merchandise, manga, retro game cartridges, Gundam model kits, and themed cafés. The streets have multi-story arcades where Japanese salaryman and teenagers compete at rhythm games. For kids: this is heaven. For adults: bewildering and totally compelling. Yodobashi Camera and Bic Camera are the anchor electronics stores; the narrow side streets have the real treasures.",
              details: [
                '🎮 Super Potato: legendary retro gaming shop — original Famicom cartridges, Super Nintendo, rare gems',
                '🤖 Kotobukiya: premium anime model kits and figures — better quality than most souvenir shops',
                '🎰 SEGA Akihabara: multi-floor arcade with crane games (UFO catchers), rhythm games, racing simulators',
                '⚡ Yodobashi Camera: 8-floor electronics megastore — great for gadgets, cameras, and tech accessories',
                '🍱 Maid Café: touristy but uniquely Tokyo — servers in maid costumes, omurice with ketchup drawings'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Kanda Yabu Soba — Near Akihabara',
              description: 'One of Tokyo\'s most historic soba restaurants, open since 1880 near Akihabara. Buckwheat soba noodles served cold in a bamboo basket with dipping broth — pure, delicate, and delicious. A wonderful counterpoint to the sensory overload of Akihabara. Beloved by Tokyo locals for generations.',
              meta: '💰 ¥1,000–1,500 · 📍 Awajichō, 10-min walk from Akihabara Station · Open for lunch, closed Tuesday'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Chidorigafuchi Cherry Blossom Moat — Evening Walk',
              description: "This is the defining Tokyo sakura experience. Chidorigafuchi is a moat around the Imperial Palace whose path is lined with hundreds of cherry trees — when they bloom, the branches arch over the water and petals drift onto the surface. At dusk, the path is illuminated and the reflection of pale pink blossoms in the dark water is heartbreakingly beautiful. In mid-March, you may catch early blooms or vivid buds just breaking open — either way, the evening atmosphere is magical. Rent a rowboat (¥800 for 30 min) to paddle under the branches.",
              details: [
                '🌸 Even early-season, the moat path itself is beautiful — 700m under arching trees',
                '🚣 Boat rental: ¥800 per 30 min (queue can be long on weekends — arrive before 5pm)',
                '🏮 Light-up illumination: sakura illumination typically runs 6–10pm during bloom season',
                '📍 Kudanshita Station (Tozai/Hanzomon/Shinjuku lines) · Free to walk the path',
                '🌅 Sunset + early bloom timing is stunning — bring a jacket, evenings are cool in March'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Kagurazaka — French-Japanese Neighborhood',
              description: 'End the evening in Kagurazaka, a neighborhood with cobblestone alleys and a unique French-Japanese identity (a large French community has lived here for decades). The narrow ishidatami (stone-paved) side streets are lined with excellent French bistros, kaiseki restaurants, and atmospheric izakayas. Walk the backstreet alleys before dinner — they\'re impossibly charming.',
              meta: '💰 ¥2,000–4,000 per person · 📍 Kagurazaka Station (Tozai Line) · Try Brasserie Viron or any izakaya alley you like the look of'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6654, lng: 139.7708, label: 'Tsukiji Outer Market', num: 1, cat: 'food', desc: 'Tokyo\'s legendary market — fresh oysters, tamagoyaki on a stick, sushi breakfast' },
        { lat: 35.6717, lng: 139.7646, label: 'Ginza District', num: 2, cat: 'attraction', desc: 'Tokyo\'s luxury shopping boulevard — Itoya stationery, Ginza Six rooftop garden' },
        { lat: 35.6979, lng: 139.7716, label: 'Itoya Stationery, Ginza', num: 3, cat: 'attraction', desc: '12-floor stationery paradise — pens, notebooks, craft supplies, Japanese paper' },
        { lat: 35.7000, lng: 139.7733, label: 'Akihabara Electric Town', num: 4, cat: 'attraction', desc: 'Anime, retro games, electronics, arcades — the world\'s most dazzling shopping district' },
        { lat: 35.6948, lng: 139.7464, label: 'Chidorigafuchi Cherry Blossom Moat', num: 5, cat: 'attraction', desc: 'Tokyo\'s most romantic sakura spot — row a boat under blooming cherry trees over the moat' },
        { lat: 35.7022, lng: 139.7409, label: 'Kagurazaka', num: 6, cat: 'food', desc: 'Cobblestone French-Japanese neighborhood — charming backstreet alleys and superb restaurants' }
      ]
    },
    {
      num: 6,
      date: '2026-03-18',
      neighborhoods: 'Nakameguro · Daikanyama · Departure',
      title: 'Farewell Sakura Morning — Nakameguro Canal Walk',
      description: "Your last morning in Tokyo. Check out, store your bags, and head to Nakameguro for what may be the most beautiful farewell walk in travel. The Meguro River is a narrow urban canal whose banks are lined with hundreds of cherry trees — when blooming, the branches form a pink tunnel over the water while petals drift downstream. Coffee shops and cafés line both sides with seats overlooking the canal. A perfect, unhurried goodbye to Tokyo.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Nakameguro Canal — Cherry Blossom Walk',
              description: "The Meguro River in Nakameguro is arguably Tokyo's most photographed sakura spot — the canal is narrow enough that the cherry branches from both sides meet overhead, creating a soft pink tunnel reflected in the water below. The walk from Nakameguro Station south to Daikanyama is about 1.5km and lined with excellent coffee shops. In mid-March, early bloomers are possible and the environment itself is beautiful.",
              details: [
                '🌸 Best section: from Nakameguro Station to Daikanyama (1.5km, flat, easy)',
                '☕ Excellent café strip: Onibus Coffee, Log Road cafés, Starbucks Reserve (Nakameguro flagship)',
                '📍 Nakameguro Station (Tokyu Toyoko Line / Tokyo Metro Hibiya Line)',
                '🕐 Walk takes 45 min at a leisurely pace with coffee stops — aim to finish by 11am',
                '🌸 If blossoms haven\'t fully opened yet, the canal banks are still lovely and peaceful'
              ]
            },
            {
              title: 'Daikanyama T-Site — Tokyo\'s Most Beautiful Bookshop',
              description: "A 10-minute walk from Nakameguro, Tsutaya Books Daikanyama is one of the world's most beautiful bookstores — a sprawling garden campus with three connected buildings housing books, music, a café, and curated design products. The gardening section is famously beloved, with staff picks in multiple languages. The attached Anjin café (vintage magazine library) is perfect for a final Tokyo coffee.",
              details: [
                '📚 Open 7am–2am (café) · Bookstore 9am–11pm',
                '☕ Anjin café: vintage international magazine library — coffee while surrounded by decades of Vogue, National Geographic, and Life',
                '🌿 The garden between the buildings has mature trees and outdoor seating',
                '🎵 The music vinyl section is well-curated — great for music lovers'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Final Breakfast',
              name: 'Starbucks Reserve Roastery Nakameguro',
              description: 'Not just a Starbucks — the Tokyo Starbucks Reserve Roastery is one of only 6 in the world, housed in a stunning 4-floor building right on the Nakameguro canal. The specialty coffee is excellent, the pastries are Japanese-influenced, and the canal view from the upper terrace with cherry blossom branches overhead is the perfect final Tokyo memory.',
              meta: '💰 ¥600–1,200 · 📍 2-19-23 Aobadai, Meguro, right on the canal · Can have a queue on weekends — arrive when it opens at 7am'
            }
          ]
        },
        {
          label: 'Departure',
          activities: [
            {
              title: 'Head to Airport — Haneda or Narita',
              description: "Collect your bags, take one last look at the Tokyo skyline, and head to the airport. Give yourself ample time — Tokyo's airports are efficient but distance matters.",
              details: [
                '✈️ Haneda Airport (HND): 35–40 min by Keikyu Line from Shinagawa, or by Tokyo Monorail from Hamamatsucho',
                '✈️ Narita Airport (NRT): 60–90 min via N\'EX from Shinjuku/Tokyo station (¥3,250 adult, ¥1,630 child)',
                '🛄 Store bags at hotel until departure · Most Tokyo hotels allow late luggage storage',
                '🛍️ Last-minute gift buying: Tokyo Station\'s basement (Gransta) is excellent for omiyage (souvenir gifts) — Tokyo Banana, Shiroi Koibito cookies, matcha KitKats'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6413, lng: 139.6986, label: 'Nakameguro Canal', num: 1, cat: 'attraction', desc: 'Tokyo\'s most beautiful sakura walk — cherry branches arch over the narrow canal' },
        { lat: 35.6481, lng: 139.7029, label: 'Starbucks Reserve Roastery Nakameguro', num: 2, cat: 'food', desc: 'One of 6 Reserve Roasteries in the world — canal-side cherry blossom coffee farewell' },
        { lat: 35.6484, lng: 139.7003, label: 'Daikanyama T-Site Tsutaya Books', num: 3, cat: 'attraction', desc: 'One of the world\'s most beautiful bookstores — garden campus, café, vinyl records' },
        { lat: 35.6812, lng: 139.7671, label: 'Tokyo Station Gransta', num: 4, cat: 'food', desc: 'Best last-minute omiyage: Tokyo Banana, matcha KitKat, Shiroi Koibito cookies' },
        { lat: 35.5494, lng: 139.7798, label: 'Haneda Airport (HND)', num: 5, cat: 'attraction', desc: 'Tokyo\'s closest airport — 35 min from Shinagawa by Keikyu Line' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '¥10,000–15,000/night', midrange: '¥20,000–40,000/night', luxury: '¥50,000–120,000/night' },
    { category: 'Meals', budget: '¥3,000–5,000/person/day', midrange: '¥6,000–10,000/person/day', luxury: '¥15,000–30,000/person/day' },
    { category: 'Attractions', budget: '¥1,000–3,000/day/family', midrange: '¥5,000–12,000/day/family', luxury: '¥15,000+/day/family' },
    { category: 'Transport (subway)', budget: '¥500–1,000/person/day', midrange: '¥800–1,500/person/day', luxury: '¥2,000+ (taxi/private)' },
    { category: '6-Day Total (family of 4)', budget: '¥200,000–280,000 (~$1,300–1,900)', midrange: '¥350,000–600,000 (~$2,400–4,100)', luxury: '¥800,000+ (~$5,400+)' }
  ],

  practicalInfo: [
    {
      title: '✈️ Getting There',
      items: [
        'Haneda Airport (HND) is closest to central Tokyo — 35 min to Shinagawa by Keikyu Line',
        'Narita Airport (NRT) is 60–90 min by N\'EX express — ¥3,250 adult, ¥1,630 child to Shinjuku/Tokyo Station',
        'IC Card (Suica/Pasmo) setup at airport: add ¥5,000 per person to start — covers all trains, buses, and convenience stores'
      ]
    },
    {
      title: '🏨 Where to Stay',
      items: [
        'Best neighborhoods for families: Shinjuku (central, food-rich), Asakusa (traditional, near temple), Shibuya (trendy, central)',
        'Budget: Dormy Inn chain — business hotel but excellent onsen baths and free late-night ramen service',
        'Mid-range: Citadines Shinjuku, Hotel Gracery Shinjuku (Godzilla head on the roof!), Via Inn Asakusa',
        'Splurge: Park Hyatt Tokyo (Lost in Translation hotel), Aman Tokyo (ultra-luxury in Otemachi)'
      ]
    },
    {
      title: '🌸 Cherry Blossom Forecast',
      items: [
        'Peak sakura in Tokyo is typically late March to early April — mid-March may see early blooms',
        'Best early-bloom spots: Shinjuku Gyoen (early varieties), Ueno Park (some kanzakura), Chidorigafuchi',
        'Check the JMC official forecast (jma.go.jp) or Japan-Guide.com\'s sakura tracker the week before you travel',
        'Even 30% bloom is beautiful — the atmosphere in Tokyo during sakura season is joyful regardless'
      ]
    },
    {
      title: '👨‍👩‍👧‍👦 Family Tips',
      items: [
        'Japan is one of the safest countries on earth — kids can wander and explore with minimal worry',
        'Konbini (convenience stores) are lifesavers: open 24/7, hot food, affordable snacks, clean restrooms everywhere',
        'Book teamLab Planets in advance — it sells out weeks ahead. Do this NOW at teamlab.art/e/planets',
        'If kids get tired, Tokyo has world-class parks (Yoyogi, Ueno, Shinjuku Gyoen) for rest breaks',
        'Escalators: stand on the left in Tokyo (unlike Osaka where it\'s the right) — a subtle but important rule',
        'Kids eat free or cheap at most family restaurants (ファミレス) — look for "お子様ランチ" (Okosama Lunch) kids menus'
      ]
    }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('\n✅ Fulfillment complete!');
  console.log('Slug:', result.slug);
  console.log('URL:', result.url);
  console.log('File:', result.filePath);
  console.log('Email sent:', result.emailSent);
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
