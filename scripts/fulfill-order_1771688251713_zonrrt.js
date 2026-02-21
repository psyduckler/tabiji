const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771688251713_zonrrt',
  email: 'colzeri.uk@gmail.com',
  destination: 'Japan',
  startDate: '2026-04-03',
  endDate: '2026-04-17',
  groupSize: 2,
  requests: 'Mix of touristic and real Japan, public transport accessible, lots of typical food, some high-end real experiences (no tourist traps), spa/onsen, balance of busy and relaxing days'
};

const itineraryData = {
  destination: 'Japan',
  countryEmoji: '🇯🇵',
  title: 'Cherry Blossoms & Hidden Japan',
  subtitle: '14 days from neon-lit Tokyo to ancient temples, steaming onsen & Osaka street food for two',
  description: "Japan in early April is a dream — the cherry blossoms are at their peak, turning parks and canal-sides into tunnels of pink and white. This itinerary balances the electric energy of Tokyo with the meditative calm of Kyoto's temples, the volcanic steam of Hakone's onsen, and the unrestrained foodie paradise of Osaka. You'll eat at tiny 6-seat ramen counters, soak in outdoor hot springs overlooking misty mountains, wander bamboo groves at dawn, and discover neighborhoods most tourists never find. This is both the Japan of postcards and the Japan that locals love.",
  duration: '14 nights',
  dates: 'Apr 3 – Apr 17, 2026',
  budget: '$$–$$$$',
  pace: 'Balanced',
  bestFor: 'Couples · Foodies · Culture Lovers',
  highlights: [
    'Cherry blossom season along the Philosopher\'s Path in Kyoto',
    'Private onsen ryokan stay in Hakone with Mt. Fuji views',
    'Tsukiji Outer Market tuna & tamagoyaki breakfast',
    'Fushimi Inari\'s 10,000 vermillion torii gates at sunrise',
    'Osaka\'s Dotonbori street food crawl — takoyaki, okonomiyaki, kushikatsu',
    'Arashiyama bamboo grove before the crowds',
    'Nara\'s friendly deer and ancient Todai-ji temple',
    'Hiroshima Peace Memorial & Miyajima\'s floating torii',
    'Traditional tea ceremony in a Kyoto machiya townhouse',
    'Shinjuku Golden Gai — tiny bars, big personality'
  ],

  essentials: [
    { title: '🌸 Cherry Blossom Season', text: 'Early April is peak sakura in Tokyo and Kyoto. Check real-time forecasts on japan-guide.com/sakura. Parks fill up for hanami picnics — join in with convenience store bento and beer. The blossoms last about 7-10 days per area.' },
    { title: '🚄 Japan Rail Pass', text: 'A 14-day JR Pass (¥50,000/~€310pp) covers all shinkansen (except Nozomi/Mizuho), JR local trains, and many buses. Activate on Day 5 (Hakone→Kyoto) to cover your longest journeys. Tokyo days use metro/Suica instead.' },
    { title: '💴 Cash & Cards', text: 'Japan is increasingly card-friendly, but many small restaurants, temples, and ryokan are cash-only. Withdraw yen at 7-Eleven ATMs (no fees with most international cards). Budget ¥5,000-10,000/day cash per person.' },
    { title: '🚇 Getting Around Cities', text: 'Get a Suica or Pasmo IC card at any station — tap on/off for trains, buses, even convenience stores. Tokyo Metro + JR lines cover everything. In Kyoto, buses are king (day pass ¥700). Google Maps works perfectly for transit routing.' },
    { title: '🏨 Accommodation Mix', text: 'We recommend: modern hotel in Tokyo (Shinjuku area), traditional ryokan in Hakone (one night), boutique hotel or machiya in Kyoto, and hotel near Namba in Osaka. Book the ryokan early — popular ones sell out months ahead.' },
    { title: '🍜 Food Culture Tips', text: 'Slurping noodles is polite. No tipping ever. Many restaurants use ticket vending machines — press the button with the photo you want, hand the ticket to staff. Lunch sets (teishoku) are incredible value. Convenience store food (konbini) is genuinely excellent.' }
  ],

  days: [
    // ========== DAY 1 ==========
    {
      num: 1,
      date: '2026-04-03',
      neighborhoods: 'Shinjuku · Kabukichō · Golden Gai',
      title: 'Welcome to Tokyo — Neon, Ramen & Golden Gai',
      description: "Land in Tokyo and dive straight into sensory overload. Check into Shinjuku — Tokyo's buzzing heart — grab your first bowl of proper ramen, watch the famous Shibuya scramble crossing, and end the night bar-hopping through the tiny wonderland of Golden Gai.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive & Check In — Shinjuku',
              description: 'Take the Narita Express (N\'EX) or Limousine Bus to Shinjuku. Drop your bags, pick up a Suica card at the station, and orient yourself. Shinjuku Station is the world\'s busiest — embrace the chaos.',
              details: [
                '✈️ Narita Express: 80 min to Shinjuku, ¥3,250 (or free with JR Pass if activated)',
                '💳 Get Suica/Pasmo IC card at any JR ticket machine',
                '🏨 Stay near Shinjuku Station for maximum transport convenience'
              ]
            },
            {
              title: 'Shibuya Scramble & Hachiko',
              description: 'Take the JR line one stop to Shibuya. Stand at the Shibuya Sky observation deck or the Starbucks window to watch the world\'s most famous pedestrian crossing. Pay respects to Hachiko, the loyal dog statue.',
              details: [
                '📸 Best scramble views: Shibuya Sky rooftop (¥2,000) or Mag\'s Park rooftop (free)',
                '🐕 Hachiko statue is right outside Shibuya Station\'s Hachiko Exit'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Fuunji Tsukemen',
              description: 'Iconic tsukemen (dipping ramen) shop in Shinjuku. Thick, rich broth with perfectly chewy noodles. There\'s always a queue — it\'s worth every minute. Order from the vending machine.',
              meta: '💰 $ · 📍 Yoyogi, 2 min from Shinjuku South Exit · Cash only'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Golden Gai Bar Hopping',
              description: 'Shinjuku\'s Golden Gai is a labyrinth of 200+ tiny bars crammed into six narrow alleys. Each seats 4-8 people and has its own bizarre theme — jazz, punk, horror movies, cats. Cover charges are typically ¥500-1,000. Just pick a door and walk in.',
              details: [
                '🍺 Start at bars with English menus if nervous — many welcome tourists',
                '💴 Cash only everywhere. Some bars charge a cover (¥300-1,000)',
                '📸 The alleys themselves are incredibly photogenic'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Jet lag is real. Don\'t fight it — Golden Gai is perfect for a late night. But try to sleep by midnight to reset your clock for tomorrow\'s early start.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6896, lng: 139.7006, label: 'Shinjuku Station', num: 1, cat: 'transport', desc: 'World\'s busiest station — your home base' },
        { lat: 35.6595, lng: 139.7004, label: 'Shibuya Crossing', num: 2, cat: 'attraction', desc: 'The famous scramble crossing' },
        { lat: 35.6887, lng: 139.6975, label: 'Fuunji Tsukemen', num: 3, cat: 'food', desc: 'Legendary tsukemen dipping ramen' },
        { lat: 35.6938, lng: 139.7036, label: 'Golden Gai', num: 4, cat: 'attraction', desc: '200+ tiny themed bars in narrow alleys' },
        { lat: 35.6585, lng: 139.6984, label: 'Shibuya Sky', num: 5, cat: 'attraction', desc: 'Rooftop observation deck over the crossing' }
      ]
    },

    // ========== DAY 2 ==========
    {
      num: 2,
      date: '2026-04-04',
      neighborhoods: 'Tsukiji · Asakusa · Ueno · Yanaka',
      title: 'Old Tokyo — Markets, Temples & Cherry Blossoms',
      description: "Discover Tokyo's traditional soul. Start with a legendary market breakfast at Tsukiji, explore the ancient Senso-ji temple in Asakusa, then chase cherry blossoms through Ueno Park and the charmingly retro neighborhood of Yanaka — Tokyo's last old-town quarter.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tsukiji Outer Market Breakfast',
              description: 'While the inner wholesale market moved to Toyosu, the Tsukiji Outer Market remains a foodie paradise. Wander the stalls eating tamagoyaki (sweet omelette on a stick), fresh sashimi, grilled seafood skewers, and Japanese street snacks. Come hungry.',
              details: [
                '🐟 Must-try: tamagoyaki, unagi skewers, fresh oysters, mochi',
                '⏰ Best before 10am — stalls close by early afternoon',
                '💴 Mostly cash only'
              ]
            },
            {
              title: 'Senso-ji Temple, Asakusa',
              description: 'Tokyo\'s oldest temple (built 645 AD) is spectacular — approach through the iconic Kaminarimon thunder gate, walk the bustling Nakamise shopping street, and admire the five-story pagoda. The incense smoke is said to heal whatever body part you waft it toward.',
              details: [
                '⛩️ Free entry · Open 24 hours (main hall 6am-5pm)',
                '🛍️ Nakamise-dori has traditional snacks and souvenirs — try ningyo-yaki (filled cakes)',
                '📸 Come early or the crowds can be intense'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Cherry Blossoms at Ueno Park',
              description: 'Ueno Park is one of Tokyo\'s top hanami (cherry blossom viewing) spots with over 1,000 trees lining the main path. In early April, the park transforms into a sea of pink with picnicking locals spread out under the trees. Grab a bento and join them.',
              details: [
                '🌸 Over 1,000 cherry trees — peak bloom usually late March to early April',
                '🍱 Buy a bento + beer from a nearby konbini for instant hanami',
                '🏛️ Tokyo National Museum is here if you want world-class Japanese art'
              ]
            },
            {
              title: 'Yanaka — Old Tokyo\'s Hidden Gem',
              description: 'Yanaka survived the bombings and earthquakes that flattened most of Tokyo. Narrow lanes, wooden houses, tiny temples, independent craft shops, and resident cats. Yanaka Ginza shopping street feels like 1960s Japan. This is the \"real Tokyo\" tourists miss.',
              details: [
                '🐱 Yanaka is famous for its stray cats — look for cat-themed shops',
                '🏘️ Yanaka Cemetery has some of Tokyo\'s best cherry blossom canopies',
                '🍡 Try menchi-katsu (fried meat croquette) from the Yanaka Ginza street vendors'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Sometaro Okonomiyaki',
              description: 'Cook-your-own okonomiyaki (savory pancake) in a charming old Asakusa house. The tatami seating and DIY griddle make this a fun, authentic experience.',
              meta: '💰 $$ · 📍 Asakusa, Taito · Cash preferred'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Asakusa by Night',
              description: 'Return to Senso-ji after dark — the pagoda and Kaminarimon gate are beautifully illuminated with almost no one around. Stroll along the Sumida River to see Tokyo Skytree lit up reflecting on the water.',
              details: [
                '🌙 Senso-ji at night is hauntingly beautiful and nearly empty',
                '📸 Skytree reflection on Sumida River — stunning nighttime photo'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Hoppy Street (Hoppy-dori)',
              description: 'Asakusa\'s lively outdoor drinking street lined with izakaya. Sit on plastic stools, order nikomi (beef tendon stew), yakitori skewers, and Hoppy (a beer-like drink). This is how Tokyo locals eat and drink.',
              meta: '💰 $ · 📍 Asakusa, near Senso-ji · Super casual, super fun'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6654, lng: 139.7707, label: 'Tsukiji Outer Market', num: 1, cat: 'food', desc: 'Legendary food market — breakfast paradise' },
        { lat: 35.7148, lng: 139.7967, label: 'Senso-ji Temple', num: 2, cat: 'attraction', desc: 'Tokyo\'s oldest and most famous temple' },
        { lat: 35.7146, lng: 139.7750, label: 'Ueno Park', num: 3, cat: 'attraction', desc: '1,000+ cherry trees — top hanami spot' },
        { lat: 35.7269, lng: 139.7677, label: 'Yanaka Ginza', num: 4, cat: 'attraction', desc: 'Old-town shopping street with retro charm' },
        { lat: 35.7116, lng: 139.7965, label: 'Sometaro', num: 5, cat: 'food', desc: 'DIY okonomiyaki in a traditional Asakusa house' },
        { lat: 35.7126, lng: 139.7940, label: 'Hoppy Street', num: 6, cat: 'food', desc: 'Outdoor izakaya street — local drinking culture' }
      ]
    },

    // ========== DAY 3 ==========
    {
      num: 3,
      date: '2026-04-05',
      neighborhoods: 'Meiji Shrine · Harajuku · Omotesando · Roppongi',
      title: 'Shrines, Fashion & Tokyo\'s Creative Side',
      description: "From the serene forest of Meiji Shrine to the kaleidoscopic fashion of Harajuku and the sophistication of Omotesando, today explores Tokyo\'s creative spectrum. End with sunset views from Roppongi Hills and a kaiseki dinner that\'s edible art.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Meiji Shrine (Meiji Jingū)',
              description: 'Enter through the towering torii gate into 170 acres of forested serenity in the heart of Tokyo. Meiji Shrine is dedicated to Emperor Meiji and Empress Shōken. Walk the gravel paths under a canopy of 100,000 trees, write a wish on an ema (wooden plaque), and witness a traditional Shinto ceremony if you\'re lucky.',
              details: [
                '⛩️ Free entry · Open sunrise to sunset',
                '🌳 The forest was planted in 1920 — 100,000 trees from all over Japan',
                '📿 Write a wish on an ema plaque (¥500) and hang it at the shrine'
              ]
            },
            {
              title: 'Harajuku & Takeshita Street',
              description: 'Step from sacred to surreal. Harajuku is Tokyo\'s youth culture epicenter — Takeshita Street bursts with cotton candy crepes, wild fashion boutiques, and cosplayers. Love it or find it overwhelming — it\'s a quintessential Tokyo experience.',
              details: [
                '🍦 Giant cotton candy, rainbow crepes, and themed cafés',
                '👗 Cat Street (one block over) has cooler, indie fashion',
                '📸 Takeshita-dori is tiny — go before 11am to actually walk'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Bills Omotesando',
              description: 'The restaurant that made ricotta hotcakes famous worldwide. Light, fluffy, and served with honeycomb butter and banana. Beautiful airy space on Omotesando.',
              meta: '💰 $$ · 📍 Omotesando · Book ahead on weekends'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Omotesando — Tokyo\'s Champs-Élysées',
              description: 'The tree-lined boulevard of Omotesando is Tokyo\'s most architecturally stunning shopping street. Even if you don\'t shop, admire the buildings: Tadao Ando\'s Omotesando Hills, Toyo Ito\'s Tod\'s building, and Herzog & de Meuron\'s Prada flagship. Each is a masterpiece.',
              details: [
                '🏛️ It\'s an open-air architecture gallery — bring a camera',
                '🛍️ Side streets hide vintage shops and independent designers'
              ]
            },
            {
              title: 'Nezu Museum',
              description: 'A hidden oasis in Omotesando — the Nezu Museum houses a stunning collection of pre-modern Japanese and East Asian art in a building designed by Kengo Kuma. The real star is the lush garden with ponds, stone paths, and tea houses.',
              details: [
                '🎋 The garden is magical — especially beautiful in spring',
                '🎟️ ¥1,300 admission · Closed Mondays'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Roppongi Hills Observation Deck',
              description: 'Head to the Tokyo City View observation deck at Roppongi Hills for a 360° panorama at sunset. On a clear day, Mt. Fuji glows pink. At night, the city becomes an infinite grid of lights.',
              details: [
                '🌅 Time for sunset — check sunset time (around 6:10pm in early April)',
                '🎟️ ¥2,000 · Open-air Sky Deck on the rooftop is extra ¥500 but worth it'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Kaiseki at Kikunoi Akasaka',
              description: 'Three-Michelin-starred kaiseki (traditional multi-course Japanese cuisine) at one of Tokyo\'s most revered restaurants. Every dish is a seasonal work of art — cherry blossom motifs will feature heavily in April. This is the high-end Japanese dining experience at its finest.',
              meta: '💰 $$$$ · 📍 Akasaka · ¥15,000-25,000 per person · Book weeks ahead'
            }
          ],
          tips: [
            { type: 'tip', text: 'Kaiseki is a slow, meditative experience — expect 2+ hours and 8-12 courses. Tell them any dietary restrictions when booking. Dress smart casual.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6764, lng: 139.6993, label: 'Meiji Shrine', num: 1, cat: 'attraction', desc: 'Serene Shinto shrine in a vast urban forest' },
        { lat: 35.6702, lng: 139.7026, label: 'Takeshita Street', num: 2, cat: 'attraction', desc: 'Harajuku\'s wild youth fashion street' },
        { lat: 35.6653, lng: 139.7122, label: 'Omotesando', num: 3, cat: 'attraction', desc: 'Tree-lined boulevard of architectural marvels' },
        { lat: 35.6624, lng: 139.7180, label: 'Nezu Museum', num: 4, cat: 'attraction', desc: 'Art museum with stunning traditional garden' },
        { lat: 35.6604, lng: 139.7292, label: 'Roppongi Hills', num: 5, cat: 'attraction', desc: '360° Tokyo views from the observation deck' },
        { lat: 35.6714, lng: 139.7370, label: 'Kikunoi Akasaka', num: 6, cat: 'food', desc: 'Three-star kaiseki — edible art' }
      ]
    },

    // ========== DAY 4 ==========
    {
      num: 4,
      date: '2026-04-06',
      neighborhoods: 'Shimokitazawa · Nakameguro · Daikanyama',
      title: 'Local Tokyo — Hip Neighborhoods & Canal Blossoms',
      description: "Skip the tourist trail today and explore Tokyo like a local. Vintage shopping in bohemian Shimokitazawa, cherry blossoms along Nakameguro\'s canal (one of Tokyo\'s most stunning sakura spots), and laid-back cafés in leafy Daikanyama. A slow, beautiful day.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shimokitazawa — Tokyo\'s Bohemian Quarter',
              description: 'This is the Tokyo that guidebooks are only starting to mention. Narrow lanes packed with vintage clothing shops, tiny record stores, independent cafés, and live music venues. It feels like a creative small town transplanted into the megalopolis.',
              details: [
                '👕 Amazing vintage — expect ¥500-3,000 for unique pieces',
                '☕ Bear Pond Espresso is legendary but temperamental (no photos allowed)',
                '🎵 Dozens of tiny live music venues — check what\'s on tonight'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Ballon d\'Essai',
              description: 'A charming French-Japanese bakery café in Shimokitazawa. Exquisite croissants and pain au chocolat — the Japanese take on French patisserie is world-class.',
              meta: '💰 $ · 📍 Shimokitazawa · Opens 8am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nakameguro Cherry Blossoms',
              description: 'The Meguro River in Nakameguro is one of Tokyo\'s most magical sakura spots. Over 800 cherry trees line both banks, their branches forming a pink tunnel over the water. In peak bloom, petals drift down like snow. Canal-side cafés and wine bars make it perfect for lingering.',
              details: [
                '🌸 800+ cherry trees over 3.8km of canal — peak early April',
                '🍷 Grab a drink from a canal-side stand and stroll',
                '📸 The pink tunnel effect is most intense near Nakameguro Station',
                '🌙 Come back at night — some sections are illuminated'
              ]
            },
            {
              title: 'Daikanyama & Tsutaya Books',
              description: 'Daikanyama is Tokyo\'s most sophisticated residential neighborhood — quiet tree-lined streets with design boutiques and architecture. The Tsutaya T-Site bookstore is a stunning space: three glass pavilions connected by a magazine-lined corridor. Perfect for browsing.',
              details: [
                '📚 Tsutaya T-Site — one of the world\'s most beautiful bookstores',
                '🌿 The whole neighborhood feels like a different city — calm and curated'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Onigiri Bongo',
              description: 'Cult-favorite onigiri (rice ball) shop near Otsuka Station. Made fresh to order with over 50 filling options — salmon, mentaiko, pickled plum, tuna mayo. Massive, hand-formed, and impossibly delicious. The queue is part of the experience.',
              meta: '💰 $ · 📍 Otsuka (10 min detour) · ¥200-350 per onigiri · Cash only'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Nakameguro Evening Stroll & Dinner',
              description: 'Return to Nakameguro as the sun sets. Some sections of the cherry tree canal are illuminated in the evenings, creating a dreamlike reflection on the water. The neighborhood has excellent izakaya and wine bars.',
              details: [
                '🌸 Illuminated cherry blossoms reflecting on the canal — unreal',
                '🍷 The neighborhood transforms into a sophisticated evening scene'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Yakitori Hachibei',
              description: 'Outstanding yakitori (grilled chicken skewers) in Nakameguro. Each part of the bird prepared differently — from juicy thigh to crispy skin to heart. Paired with cold sake, this is quintessential Japanese drinking food done at an exceptional level.',
              meta: '💰 $$ · 📍 Nakameguro · Counter seating, intimate vibe'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6610, lng: 139.6687, label: 'Shimokitazawa', num: 1, cat: 'attraction', desc: 'Bohemian quarter — vintage shops and indie cafés' },
        { lat: 35.6441, lng: 139.6987, label: 'Nakameguro Canal', num: 2, cat: 'attraction', desc: '800+ cherry trees forming a pink tunnel over the river' },
        { lat: 35.6494, lng: 139.7010, label: 'Daikanyama T-Site', num: 3, cat: 'attraction', desc: 'One of the world\'s most beautiful bookstores' },
        { lat: 35.7316, lng: 139.7280, label: 'Onigiri Bongo', num: 4, cat: 'food', desc: 'Cult onigiri shop — 50+ fillings made to order' },
        { lat: 35.6438, lng: 139.6980, label: 'Yakitori Hachibei', num: 5, cat: 'food', desc: 'Exceptional yakitori with cold sake' }
      ]
    },

    // ========== DAY 5 ==========
    {
      num: 5,
      date: '2026-04-07',
      neighborhoods: 'Hakone · Owakudani · Lake Ashi',
      title: 'Hakone — Volcanic Valleys, Lake & Onsen Ryokan',
      description: "Leave Tokyo behind for the mountains of Hakone. Ride the famous mountain railway through switchbacks, take a cable car over steaming volcanic vents, cruise Lake Ashi with Mt. Fuji reflected in the water, and check into a traditional ryokan for your first onsen experience — hot mineral springs overlooking misty forests.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Romance Car to Hakone',
              description: 'Board the Odakyu Romance Car from Shinjuku — a sleek limited express with panoramic windows. The 90-minute ride takes you from the urban sprawl into lush mountain scenery. Reserve front-row seats in the observation car for the best views.',
              details: [
                '🚂 Odakyu Romance Car: Shinjuku → Hakone-Yumoto, 85 min, ¥2,330',
                '💺 Book front observation seats online at odakyu.jp — sells out fast',
                '🎫 Buy the Hakone Free Pass (¥6,100) — covers all transport loops within Hakone'
              ]
            },
            {
              title: 'Hakone Loop — Railway, Cable Car & Ropeway',
              description: 'The Hakone loop is an engineering marvel: switchback mountain railway → cable car up through sulfur-steaming Owakudani valley → ropeway with aerial views of Lake Ashi and (weather permitting) Mt. Fuji. Each segment reveals dramatically different landscape.',
              details: [
                '🚡 Owakudani: active volcanic area — eat a black egg (kuro-tamago) for 7 extra years of life',
                '🗻 Mt. Fuji views from the ropeway are weather-dependent — cross fingers for a clear day',
                '🥚 Black eggs boiled in volcanic sulfur — ¥500 for 5'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Lake Ashi Pirate Ship Cruise',
              description: 'Board the kitsch-but-fun pirate ship replica across Lake Ashi. On clear days, Mt. Fuji presides over the lake with the red torii gate of Hakone Shrine rising from the shoreline. It\'s absurdly picturesque.',
              details: [
                '🚢 Included in Hakone Free Pass',
                '⛩️ Hakone Shrine\'s lakeside torii — one of Japan\'s most photographed spots',
                '📸 Mt. Fuji reflection on calm mornings'
              ]
            },
            {
              title: 'Hakone Shrine',
              description: 'A Shinto shrine set in a dense cryptomeria forest along the lake shore. The vermillion torii gate standing in the water is iconic. The path through the ancient trees feels otherworldly.',
              details: [
                '⛩️ The lakeside torii is the classic photo — arrive by boat for the best approach',
                '🌲 The cedar forest path is atmospheric and cool'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Soba Noodles at Hatsuhana',
              description: 'Hakone is famous for soba (buckwheat noodles) made with pure mountain spring water. Hatsuhana is the most celebrated shop — hand-cut noodles with a clean, nutty flavor served on bamboo trays.',
              meta: '💰 $$ · 📍 Hakone-Yumoto · Queue likely · Cash only'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Check In to Ryokan & Onsen',
              description: 'This is the highlight of Hakone — checking into a traditional ryokan (Japanese inn). Change into your yukata (cotton robe), explore the onsen (hot spring baths), and surrender to total relaxation. Most ryokan have both indoor and rotenburo (outdoor) baths overlooking forests or mountains. Dinner is a multi-course kaiseki feast served in your room.',
              details: [
                '♨️ Onsen etiquette: wash thoroughly before entering, no swimwear, towels stay out of the water',
                '👘 Your yukata is provided — wear it everywhere in the ryokan',
                '🍽️ Kaiseki dinner included — expect 10+ exquisite courses',
                '🏨 Recommended: Gora Kadan, Hakone Ginyu, or Yama no Chaya for the full experience'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Japanese onsen require bathing nude. There are separate male and female baths. If you have tattoos, some ryokan offer private baths (kashikiri) — ask when booking. This is an unmissable experience.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.2328, lng: 139.1060, label: 'Hakone-Yumoto Station', num: 1, cat: 'transport', desc: 'Gateway to Hakone — Romance Car terminal' },
        { lat: 35.2440, lng: 139.0210, label: 'Owakudani', num: 2, cat: 'attraction', desc: 'Volcanic valley with black eggs and sulfur vents' },
        { lat: 35.2040, lng: 139.0310, label: 'Lake Ashi', num: 3, cat: 'attraction', desc: 'Scenic lake with Mt. Fuji views and pirate ship cruise' },
        { lat: 35.2038, lng: 139.0274, label: 'Hakone Shrine', num: 4, cat: 'attraction', desc: 'Forest shrine with iconic lakeside torii gate' },
        { lat: 35.2322, lng: 139.1045, label: 'Hatsuhana Soba', num: 5, cat: 'food', desc: 'Legendary handmade soba noodles' },
        { lat: 35.2473, lng: 139.0458, label: 'Ryokan & Onsen', num: 6, cat: 'attraction', desc: 'Traditional inn with hot spring baths and kaiseki dinner' }
      ]
    },

    // ========== DAY 6 ==========
    {
      num: 6,
      date: '2026-04-08',
      neighborhoods: 'Hakone · Shinkansen · Kyoto — Higashiyama',
      title: 'Hakone Morning → Bullet Train to Kyoto',
      description: "Wake early for a sunrise onsen soak, savor a traditional Japanese breakfast, then bid Hakone farewell. Board the shinkansen (bullet train) and watch Japan blur past your window at 285 km/h. Arrive in Kyoto — the ancient capital — and explore the atmospheric Higashiyama district as evening falls.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sunrise Onsen & Japanese Breakfast',
              description: 'Rise early and soak in the outdoor onsen as morning mist drifts through the valley. Ryokan breakfasts are an experience: grilled fish, miso soup, rice, pickles, tamagoyaki, natto (if you\'re brave), and green tea. It\'s elaborate and beautiful.',
              details: [
                '♨️ The outdoor bath at dawn — steam rising, birds singing — is pure magic',
                '🍳 Japanese breakfast looks like a lot of small dishes — try everything',
                '🧳 Pack up and check out by 10am'
              ]
            },
            {
              title: 'Shinkansen to Kyoto',
              description: 'Take a bus or Romancecar back to Odawara Station, then board the Hikari shinkansen to Kyoto. The ride is about 2 hours — grab an ekiben (train station bento box) and watch the landscape transform from coastal mountains to rice paddies.',
              details: [
                '🚄 Odawara → Kyoto: Hikari shinkansen, ~2 hours (covered by JR Pass)',
                '🍱 Buy an ekiben (station bento) at Odawara — they\'re works of art',
                '💺 Sit on the right side (seats D/E) for Mt. Fuji views on a clear day'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In & Explore Higashiyama',
              description: 'Drop your bags at your Kyoto accommodation and head to the Higashiyama district — Kyoto\'s most atmospheric area. Wander the steep cobblestone lanes of Ninenzaka and Sannenzaka, lined with traditional wooden buildings, tea shops, and pottery stores.',
              details: [
                '🏘️ Ninenzaka & Sannenzaka — photogenic stone-paved lanes',
                '🍵 Stop for matcha and a sweet at a traditional tea house',
                '👘 This area has kimono rental shops — wearing one enhances the experience'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Ekiben on the Shinkansen',
              description: 'Train station bento boxes are a beloved Japanese tradition. Each region has specialties — Odawara\'s feature local seafood and kamaboko (fish cake). Eating while watching the countryside fly by is peak Japan.',
              meta: '💰 $ · 📍 Odawara Station · ¥1,000-1,500'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Gion District at Dusk',
              description: 'As the lanterns come on, Gion transforms. This is Kyoto\'s famed geisha district — wooden machiya townhouses line the Shirakawa canal, their windows glowing warm. You might spot a maiko (apprentice geisha) hurrying to an appointment in full regalia.',
              details: [
                '🏮 Hanamikoji Street is the main artery — beautifully preserved',
                '👘 If you see a geiko/maiko, be respectful — no blocking, chasing, or touching',
                '🌸 The Shirakawa canal area in Gion has some beautiful weeping cherry trees'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Pontocho Alley Dining',
              description: 'Pontocho is a narrow alley running along the Kamogawa River, packed with restaurants ranging from casual yakitori to upscale kaiseki. In warm weather, many have riverside terraces (kawadoko). Pick one that appeals and settle in — you can\'t really go wrong here.',
              meta: '💰 $$–$$$ · 📍 Pontocho, between Shijo and Sanjo · Riverside terraces from May'
            }
          ],
          tips: [
            { type: 'tip', text: 'Kyoto is compact enough to bike around. Rent bikes from your hotel or a local shop — it\'s the best way to explore the canal-side neighborhoods and temple approaches.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.2328, lng: 139.1060, label: 'Hakone → Odawara', num: 1, cat: 'transport', desc: 'Bus/train to Odawara for shinkansen' },
        { lat: 34.9858, lng: 135.7588, label: 'Kyoto Station', num: 2, cat: 'transport', desc: 'Arrive via Hikari shinkansen' },
        { lat: 34.9981, lng: 135.7810, label: 'Ninenzaka & Sannenzaka', num: 3, cat: 'attraction', desc: 'Atmospheric stone-paved lanes in Higashiyama' },
        { lat: 34.9997, lng: 135.7748, label: 'Gion District', num: 4, cat: 'attraction', desc: 'Kyoto\'s geisha district with lantern-lit lanes' },
        { lat: 35.0050, lng: 135.7706, label: 'Pontocho Alley', num: 5, cat: 'food', desc: 'Narrow restaurant alley along the river' }
      ]
    },

    // ========== DAY 7 ==========
    {
      num: 7,
      date: '2026-04-09',
      neighborhoods: 'Fushimi · Kiyomizu-dera · Higashiyama · Gion',
      title: 'Kyoto Icons — Torii Gates, Temples & Tea',
      description: "Today is peak Kyoto. Rise before dawn to walk through Fushimi Inari\'s endless vermillion torii gates in blissful solitude, visit the cliff-hanging Kiyomizu-dera temple overlooking the city, and experience a traditional tea ceremony in a centuries-old machiya townhouse.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Fushimi Inari Shrine at Sunrise',
              description: 'The most visited place in Japan — but arrive at 6am and it\'s practically yours. Over 10,000 vermillion torii gates snake up Mt. Inari, creating mesmerizing tunnels of orange light. The full hike to the summit takes 2-3 hours; most visitors only do the first section. Push further for quiet forest paths and hidden sub-shrines.',
              details: [
                '⛩️ Free · Open 24 hours — arrive by 6am for emptiness',
                '🥾 Full loop to summit: ~2-3 hours, moderate hiking',
                '🦊 Dedicated to Inari, the fox deity of rice and business — fox statues everywhere',
                '📸 The deeper you go, the more magical (and empty) it gets'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Vermillion Café',
              description: 'Charming café just outside Fushimi Inari, perfect for post-hike coffee and a light breakfast. Sit on the terrace overlooking a small garden.',
              meta: '💰 $ · 📍 Right at Fushimi Inari\'s entrance · Opens 9am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kiyomizu-dera Temple',
              description: 'This UNESCO World Heritage temple perches on a hillside with a massive wooden stage jutting out over the valley. In cherry blossom season, the view from the stage — Kyoto\'s rooftops framed by pink trees — is one of Japan\'s most celebrated vistas. The wooden structure was built without a single nail.',
              details: [
                '🎟️ ¥400 · Open 6am-6pm',
                '🌸 Cherry blossom season here is extraordinary — pink trees below the wooden stage',
                '💧 Otowa Waterfall at the base — drink from three streams for longevity, love, or success (choose wisely)'
              ]
            },
            {
              title: 'Traditional Tea Ceremony',
              description: 'Experience chado — the Japanese Way of Tea — in a traditional machiya townhouse. A tea master guides you through the meditative preparation and drinking of matcha in a serene tatami room. It\'s not about the tea; it\'s about presence, aesthetics, and connection.',
              details: [
                '🍵 Book via Camellia or En tea ceremony for intimate, English-friendly experiences',
                '⏱️ Sessions last about 45-60 minutes',
                '📍 Many are in beautifully restored Gion-area machiya'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Omen Kodai-ji',
              description: 'Beautiful udon restaurant near Kodai-ji temple. Their signature cold udon with seasonal dipping vegetables is simple perfection — handmade noodles with clean, pure flavors. The garden courtyard is lovely.',
              meta: '💰 $$ · 📍 Kodai-ji area, Higashiyama'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Philosopher\'s Path Evening Stroll',
              description: 'This 2km stone path follows a cherry-tree-lined canal from Ginkaku-ji to Nanzen-ji. Named after the philosopher Nishida Kitaro who meditated while walking here. In early April, cherry blossoms form a complete canopy over the path — petals float on the canal water.',
              details: [
                '🌸 2km canal path — one of Japan\'s most famous cherry blossom spots',
                '🚶 Walk south toward Nanzen-ji for a quieter, more contemplative experience',
                '🐱 Look for the neighborhood cats along the path'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Gion Nishi',
              description: 'Intimate omakase sushi in the heart of Gion. The chef serves seasonal Kyoto-style sushi — lighter vinegar, delicate fish, with spring vegetables. Counter seating only, watching the master at work.',
              meta: '💰 $$$ · 📍 Gion · Counter seating · Reservation essential'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari Shrine', num: 1, cat: 'attraction', desc: '10,000 vermillion torii gates up Mt. Inari' },
        { lat: 34.9949, lng: 135.7850, label: 'Kiyomizu-dera', num: 2, cat: 'attraction', desc: 'Cliff-hanging temple with panoramic Kyoto views' },
        { lat: 35.0000, lng: 135.7750, label: 'Tea Ceremony (Gion)', num: 3, cat: 'attraction', desc: 'Traditional matcha ceremony in a machiya' },
        { lat: 35.0272, lng: 135.7943, label: 'Philosopher\'s Path', num: 4, cat: 'attraction', desc: 'Cherry blossom canopy over a canal-side walk' },
        { lat: 34.9963, lng: 135.7800, label: 'Omen Kodai-ji', num: 5, cat: 'food', desc: 'Handmade udon in a garden courtyard' },
        { lat: 35.0020, lng: 135.7760, label: 'Gion Nishi', num: 6, cat: 'food', desc: 'Intimate omakase sushi counter in Gion' }
      ]
    },

    // ========== DAY 8 ==========
    {
      num: 8,
      date: '2026-04-10',
      neighborhoods: 'Arashiyama · Sagano · Tenryū-ji',
      title: 'Arashiyama — Bamboo, Monkeys & River Bliss',
      description: "Head west to Arashiyama for a day of natural wonder. Walk through the otherworldly bamboo grove before the crowds arrive, visit the zen gardens of Tenryū-ji, climb to the monkey park for views and friendly macaques, and relax by the gentle Hozu River as cherry petals drift past.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Arashiyama Bamboo Grove at Dawn',
              description: 'Be here by 7am and you\'ll have this surreal landscape nearly to yourself. Towering bamboo stalks form a green cathedral above you, creaking and swaying in the breeze. The light filtering through is magical. By 9am, tour groups arrive and the magic fades — early birds win.',
              details: [
                '🎋 Free · Open 24 hours — 7am is the sweet spot',
                '📸 The path is about 500m — walk slowly and listen to the bamboo',
                '🚶 Continue through to Okochi Sanso villa garden for even more serenity'
              ]
            },
            {
              title: 'Tenryū-ji Temple & Garden',
              description: 'A UNESCO World Heritage Zen temple with one of Japan\'s oldest landscape gardens. The Sōgenchi pond garden, designed in 1339, perfectly frames the Arashiyama mountains as \"borrowed scenery.\" Sit on the veranda and just... breathe.',
              details: [
                '🎟️ ¥500 garden / ¥800 with temple buildings',
                '🌸 The garden is spectacular in cherry blossom season',
                '🧘 This is living Zen — find a spot on the veranda and sit quietly'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Iwatayama Monkey Park',
              description: 'A 20-minute uphill walk from the river leads to a hilltop park where over 100 Japanese macaques roam free. You\'re in their space — they ignore you completely while you enjoy panoramic views over Kyoto. You can feed them from inside a netted shelter (the humans are caged, the monkeys are free).',
              details: [
                '🐒 ¥550 · Open 9am-4pm · 20 min hike up',
                '📸 Views of Kyoto from the top are incredible',
                '🍎 Buy apple slices to feed the monkeys from inside the shelter'
              ]
            },
            {
              title: 'Togetsukyo Bridge & Riverside Relaxation',
              description: 'The iconic Moon Crossing Bridge spans the Hozu River with mountains rising behind it. In cherry blossom season, the riverbanks are lined with pink trees. Rent a small boat, walk along the river, or just sit on the banks and watch the water.',
              details: [
                '🌸 The riverside cherry blossoms are stunning in early April',
                '🛶 Rowboats available for rent — romantic on the gentle river'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Yudofu at Sagano',
              description: 'Arashiyama\'s specialty is yudofu — silken tofu simmered in kombu broth. Sounds simple, tastes transcendent. Sagano serves it in a stunning garden setting with river views. A zen meal in a zen place.',
              meta: '💰 $$ · 📍 Arashiyama, near Tenryū-ji · Tatami seating with garden views'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Relaxed Evening in Kyoto',
              description: 'Head back to central Kyoto at a leisurely pace. Tonight is a free evening — walk along the Kamogawa River (locals sit in couples on the riverbanks at sunset, perfectly spaced apart), browse the Nishiki Market if it\'s still open, or find a quiet neighborhood bar.',
              details: [
                '🌊 Kamogawa River couples are a Kyoto tradition — join them on the banks',
                '🏮 Nishiki Market closes around 5-6pm — catch the tail end for discounts'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Nishiki Warai Izakaya',
              description: 'Lively Kyoto-style izakaya near Nishiki Market. Try obanzai — Kyoto\'s home-style cooking: small plates of seasonal vegetables, tofu dishes, grilled fish, and pickles. Pair with local Fushimi sake.',
              meta: '💰 $$ · 📍 Near Nishiki Market · Casual and fun'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0173, lng: 135.6717, label: 'Bamboo Grove', num: 1, cat: 'attraction', desc: 'Otherworldly bamboo cathedral — arrive at dawn' },
        { lat: 35.0155, lng: 135.6744, label: 'Tenryū-ji Temple', num: 2, cat: 'attraction', desc: 'UNESCO Zen temple with 700-year-old garden' },
        { lat: 35.0101, lng: 135.6773, label: 'Monkey Park Iwatayama', num: 3, cat: 'attraction', desc: 'Wild macaques with panoramic Kyoto views' },
        { lat: 35.0114, lng: 135.6778, label: 'Togetsukyo Bridge', num: 4, cat: 'attraction', desc: 'Iconic bridge over the Hozu River' },
        { lat: 35.0175, lng: 135.6730, label: 'Sagano Yudofu', num: 5, cat: 'food', desc: 'Zen tofu cuisine in a garden setting' },
        { lat: 35.0050, lng: 135.7640, label: 'Nishiki Market', num: 6, cat: 'food', desc: 'Kyoto\'s kitchen — 400 years of food stalls' }
      ]
    },

    // ========== DAY 9 ==========
    {
      num: 9,
      date: '2026-04-11',
      neighborhoods: 'Nara · Nara Park · Todai-ji · Naramachi',
      title: 'Day Trip to Nara — Deer, Giant Buddha & Old Town',
      description: "A short train ride from Kyoto brings you to Nara, Japan\'s first permanent capital. Over 1,200 wild deer roam freely through the park and streets, bowing for crackers. The massive bronze Buddha inside Todai-ji temple will leave you speechless. Then explore the charming old merchant quarter of Naramachi.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Nara Park & the Sacred Deer',
              description: 'Step off the train and within minutes you\'re surrounded by over 1,200 wild sika deer. They roam the park, streets, and temple grounds freely — bowing to tourists for shika-senbei (deer crackers, ¥200). They\'re adorable but assertive — guard your maps and bags.',
              details: [
                '🦌 The deer bow to you if you bow first — it\'s a learned behavior!',
                '🍘 Buy shika-senbei (¥200) from park vendors — the deer will mob you',
                '📸 In April, deer among cherry blossoms = peak Japan photography'
              ]
            },
            {
              title: 'Todai-ji Temple & The Great Buddha',
              description: 'Todai-ji houses the world\'s largest bronze Buddha (15m tall) inside the world\'s largest wooden building. Walking through the enormous Nandaimon gate flanked by fierce guardian statues and then seeing the Buddha for the first time is genuinely jaw-dropping.',
              details: [
                '🎟️ ¥600 · Open 7:30am-5:30pm (Apr)',
                '🏛️ The wooden hall is the largest in the world — it\'s actually a REBUILT smaller version',
                '🕳️ Try squeezing through the pillar hole (same size as the Buddha\'s nostril) — said to grant enlightenment'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Nakatanidou Mochi',
              description: 'Watch the famous mochi-pounding performance at this tiny shop near Kintetsu Nara Station. Two men pound steaming rice at incredible speed, then hand you the freshest, softest mochi you\'ve ever tasted. It\'s an edible show.',
              meta: '💰 $ · 📍 Near Kintetsu Nara Station · Yomogi (mugwort) mochi is the signature'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kasuga Taisha Shrine',
              description: 'Follow a path through the forest lined with 3,000 stone lanterns to reach Kasuga Taisha, Nara\'s most important shrine. The lanterns, covered in moss, create an ethereal atmosphere. Twice a year they\'re all lit — but even unlit, the approach is magical.',
              details: [
                '⛩️ ¥500 for inner sanctuary · Path is free',
                '🪔 3,000 stone lanterns line the forest approach',
                '🦌 Deer wander through the shrine grounds — they\'re considered divine messengers here'
              ]
            },
            {
              title: 'Naramachi — Old Merchant Quarter',
              description: 'Wander the narrow lanes of Naramachi, a beautifully preserved Edo-period merchant district. Traditional machiya townhouses now house craft shops, small museums, sake breweries, and cafés. It\'s Nara\'s quiet, local side — perfect for slow exploration.',
              details: [
                '🏘️ Look for migawari-zaru (red cloth monkeys) hanging outside houses — protective charms',
                '🍶 Several small sake breweries offer tastings',
                '📸 The narrow streets are wonderfully photogenic'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Kakinoha Sushi at Hiraso',
              description: 'Nara\'s iconic dish: pressed sushi wrapped in persimmon leaves (kakinoha-zushi). The leaf imparts a subtle fragrance and acts as a natural preservative. Hiraso has been making them for over 150 years.',
              meta: '💰 $$ · 📍 Naramachi · A unique, only-in-Nara experience'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Kyoto — Evening at Leisure',
              description: 'Take the train back to Kyoto (45 min) and enjoy a relaxed evening. Visit a neighborhood sento (public bathhouse) for a soak, or walk along the Kamogawa River as the cherry trees are illuminated.',
              details: [
                '🚂 Kintetsu Nara → Kyoto: ~45 minutes, direct',
                '♨️ Try a local sento (public bath) — less fancy than onsen but very local (¥490)'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Ramen at Ippudo Kyoto',
              description: 'After a long day of walking, nothing beats a rich bowl of tonkotsu ramen. Ippudo\'s Kyoto branch serves their signature creamy pork broth with perfectly thin noodles. Order extra chashu (pork) — you\'ve earned it.',
              meta: '💰 $ · 📍 Central Kyoto · Fast and satisfying'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6851, lng: 135.8048, label: 'Nara Park', num: 1, cat: 'attraction', desc: '1,200+ wild deer roaming freely' },
        { lat: 34.6890, lng: 135.8398, label: 'Todai-ji Temple', num: 2, cat: 'attraction', desc: 'World\'s largest bronze Buddha and wooden building' },
        { lat: 34.6813, lng: 135.8497, label: 'Kasuga Taisha', num: 3, cat: 'attraction', desc: '3,000 stone lanterns in a mystical forest' },
        { lat: 34.6763, lng: 135.8309, label: 'Naramachi', num: 4, cat: 'attraction', desc: 'Preserved Edo-period merchant quarter' },
        { lat: 34.6818, lng: 135.8288, label: 'Hiraso Kakinoha Sushi', num: 5, cat: 'food', desc: 'Persimmon leaf sushi — 150-year tradition' },
        { lat: 34.6843, lng: 135.8010, label: 'Nakatanidou Mochi', num: 6, cat: 'food', desc: 'Famous high-speed mochi pounding show' }
      ]
    },

    // ========== DAY 10 ==========
    {
      num: 10,
      date: '2026-04-12',
      neighborhoods: 'Kinkaku-ji · Ryōan-ji · Kitano · Kyoto Imperial Palace',
      title: 'Golden Temples, Zen Gardens & Slow Kyoto',
      description: "A more relaxed Kyoto day visiting the dazzling Golden Pavilion, the mysteriously minimalist rock garden at Ryōan-ji, and the peaceful grounds of the Imperial Palace. Afternoon is deliberately unstructured — rent bikes, explore side streets, shop for ceramics, or find a quiet café.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kinkaku-ji — The Golden Pavilion',
              description: 'Japan\'s most famous image in person: a three-story pavilion covered entirely in gold leaf, reflected perfectly in the mirror-still pond. Arrive when the gates open at 9am for the best light and smallest crowds. It\'s smaller than you expect and more beautiful than you imagine.',
              details: [
                '🎟️ ¥500 · Opens 9am · No interior access',
                '📸 The reflection shot is from the first viewing area — don\'t rush past it',
                '🍵 There\'s a tea garden inside where you can drink matcha with a view'
              ]
            },
            {
              title: 'Ryōan-ji — Zen Rock Garden',
              description: 'Fifteen rocks on raked white gravel — the most famous Zen garden in the world. Sit on the wooden veranda and contemplate. The garden is designed so you can never see all 15 stones from any single angle. No one fully agrees what it means. That\'s the point.',
              details: [
                '🎟️ ¥500 · 20 min walk from Kinkaku-ji (or bus)',
                '🧘 Sit quietly and just look. Let the garden work on you.',
                '🌿 The temple grounds also have a beautiful pond garden'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kyoto Imperial Palace & Park',
              description: 'The former residence of Japan\'s Emperor sits in a vast, peaceful park. Free self-guided tours let you explore the elegant buildings and gardens. The surrounding park is a local favorite for cherry blossom picnics — grab a konbini bento and join them.',
              details: [
                '🏯 Free admission · No reservation needed for self-guided tour',
                '🌸 The park has weeping cherry trees that are often at peak when others are done',
                '🚲 Bike through the park — it\'s massive and beautifully quiet'
              ]
            },
            {
              title: 'Free Time — Explore at Your Own Pace',
              description: 'This afternoon is deliberately open. Kyoto rewards slow wandering: cycle along canal-side paths, browse ceramics on Teapot Lane (Chawanzaka), visit a kimono fabric shop, or simply find a quiet temple garden and sit. Not every hour needs to be scheduled.',
              details: [
                '🍵 Ippodo Tea — Kyoto\'s finest tea shop since 1717, with a tasting room',
                '🏺 Chawanzaka (Teapot Lane) near Kiyomizu has stunning pottery',
                '📖 Kyoto is also a great city for coffee — try % Arabica or Weekenders'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Nishiki Market Grazing',
              description: 'Kyoto\'s 400-year-old "Kitchen" — a narrow covered arcade with over 100 food stalls. Graze on dashimaki tamago (rolled omelette), pickles, mochi, matcha sweets, fresh tofu, and skewered octopus. This is lunch as an adventure.',
              meta: '💰 $–$$ · 📍 Nishiki Market, central Kyoto · Most stalls close by 5pm'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Kyoto Craft Beer & Kushikatsu',
              description: 'Try Kyoto\'s emerging craft beer scene paired with kushikatsu (deep-fried skewers). Bungalow is a great spot with local brews on tap and a relaxed, modern atmosphere. A nice break from traditional dining.',
              meta: '💰 $$ · 📍 Central Kyoto · Casual and fun'
            }
          ],
          tips: [
            { type: 'tip', text: 'If you have energy, the Philosopher\'s Path is illuminated at night during cherry blossom season in some years. Check locally — it\'s magical if it\'s happening.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0394, lng: 135.7292, label: 'Kinkaku-ji (Golden Pavilion)', num: 1, cat: 'attraction', desc: 'Gold-leaf pavilion reflected in a mirror pond' },
        { lat: 35.0345, lng: 135.7183, label: 'Ryōan-ji', num: 2, cat: 'attraction', desc: 'World\'s most famous Zen rock garden' },
        { lat: 35.0254, lng: 135.7620, label: 'Kyoto Imperial Palace', num: 3, cat: 'attraction', desc: 'Former Emperor\'s residence in a vast park' },
        { lat: 35.0050, lng: 135.7640, label: 'Nishiki Market', num: 4, cat: 'food', desc: '400-year-old food arcade — Kyoto\'s kitchen' },
        { lat: 35.0084, lng: 135.7685, label: 'Ippodo Tea', num: 5, cat: 'food', desc: 'Kyoto\'s premier tea shop since 1717' }
      ]
    },

    // ========== DAY 11 ==========
    {
      num: 11,
      date: '2026-04-13',
      neighborhoods: 'Kyoto → Osaka · Dōtonbori · Shinsekai',
      title: 'Kyoto to Osaka — Street Food Capital of Japan',
      description: "Bid Kyoto farewell and ride 15 minutes to Osaka — Japan\'s food-obsessed, no-pretense, laugh-out-loud city. Osaka\'s motto is kuidaore (eat until you drop) and today you\'ll test that theory. From the neon chaos of Dotonbori to the retro charm of Shinsekai, prepare for the best street food of your life.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinkansen to Osaka & Check In',
              description: 'Kyoto to Osaka is just 15 minutes by shinkansen (or 30 min by regular train). Check into your hotel near Namba — this puts you within walking distance of Dotonbori, Shinsekai, and the best food streets.',
              details: [
                '🚂 JR Special Rapid: Kyoto → Osaka, 29 min (JR Pass), or Hankyu line 43 min',
                '🏨 Stay near Namba or Shinsaibashi for the best food access',
                '🎒 Drop bags at the hotel or use station coin lockers'
              ]
            },
            {
              title: 'Kuromon Market — Osaka\'s Kitchen',
              description: 'Osaka\'s answer to Tsukiji: a covered market bursting with fresh seafood, street food, and local energy. Eat grilled scallops, tuna sashimi, sea urchin, tamagoyaki, and fresh strawberries as you walk. Come hungry — very hungry.',
              details: [
                '🐟 Must-try: uni (sea urchin), grilled king crab legs, fresh mochi',
                '⏰ Best before noon — stalls start closing by 4pm',
                '💴 Mostly cash only'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Dōtonbori — Neon Food Paradise',
              description: 'The beating heart of Osaka nightlife and street food. The canal is lined with enormous neon signs (the running Glico Man, the mechanical crab), and every restaurant competes with theatrical signage. This is where you eat takoyaki (octopus balls), okonomiyaki (savory pancakes), and kushikatsu (fried skewers).',
              details: [
                '🐙 Takoyaki: try Creo-Ru or Wanaka — crispy outside, molten inside',
                '🥞 Okonomiyaki: Mizuno is legendary (expect a queue)',
                '📸 The Glico Running Man sign — Osaka\'s Shibuya crossing equivalent'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Takoyaki at Creo-Ru',
              description: 'Dotonbori\'s best takoyaki — spheres of battered octopus, crispy on the outside, gooey on the inside, topped with sauce, mayo, and bonito flakes that dance in the heat. Eat them immediately (warning: molten interior).',
              meta: '💰 $ · 📍 Dōtonbori · ¥500-700 for 8 pieces'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shinsekai — Retro Osaka',
              description: 'This neighborhood was built in 1912 to be \"the new world\" — modeled on New York and Paris. Today it\'s a wonderfully retro, slightly gritty area packed with kushikatsu shops and cheap beer joints. Tsūtenkaku Tower (Osaka\'s Eiffel Tower) presides over neon-drenched streets of pure character.',
              details: [
                '🗼 Tsūtenkaku Tower observation deck: ¥900',
                '🍢 Kushikatsu rule: NEVER double-dip in the communal sauce',
                '🎮 Game arcades, pachinko parlors, and retro vibes everywhere'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Daruma Kushikatsu',
              description: 'Shinsekai\'s most famous kushikatsu restaurant. Deep-fried skewers of everything — pork, shrimp, lotus root, quail egg, mochi — dipped once in the communal tangy sauce. Wash it down with ice-cold beer. Pure Osaka soul food.',
              meta: '💰 $$ · 📍 Shinsekai · Counter and table seating · No double dipping!'
            }
          ],
          tips: [
            { type: 'tip', text: 'Osaka at night is incredibly safe. Wander the neon streets of Dotonbori and Shinsekai after dinner — the energy is infectious and the photo opportunities are endless.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6690, lng: 135.5060, label: 'Kuromon Market', num: 1, cat: 'food', desc: 'Osaka\'s kitchen — fresh seafood and street food' },
        { lat: 34.6687, lng: 135.5013, label: 'Dōtonbori', num: 2, cat: 'attraction', desc: 'Neon-lit canal of food and entertainment' },
        { lat: 34.6524, lng: 135.5062, label: 'Shinsekai', num: 3, cat: 'attraction', desc: 'Retro neighborhood with kushikatsu and character' },
        { lat: 34.6525, lng: 135.5063, label: 'Tsūtenkaku Tower', num: 4, cat: 'attraction', desc: 'Osaka\'s quirky 1912 observation tower' },
        { lat: 34.6687, lng: 135.5020, label: 'Creo-Ru Takoyaki', num: 5, cat: 'food', desc: 'Dotonbori\'s best takoyaki' },
        { lat: 34.6519, lng: 135.5056, label: 'Daruma Kushikatsu', num: 6, cat: 'food', desc: 'Legendary deep-fried skewers in Shinsekai' }
      ]
    },

    // ========== DAY 12 ==========
    {
      num: 12,
      date: '2026-04-14',
      neighborhoods: 'Hiroshima · Peace Memorial · Miyajima Island',
      title: 'Day Trip — Hiroshima & Miyajima\'s Floating Torii',
      description: "A powerful and beautiful day trip by bullet train. Start at Hiroshima\'s Peace Memorial Park — sobering, essential, and ultimately hopeful. Then ferry to the sacred island of Miyajima, where the famous floating torii gate rises from the sea and wild deer roam among ancient temples.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinkansen to Hiroshima',
              description: 'Board the Sakura shinkansen from Shin-Osaka to Hiroshima (80 min). The speed and efficiency of the bullet train make this day trip perfectly doable.',
              details: [
                '🚄 Shin-Osaka → Hiroshima: Sakura shinkansen, 80 min (JR Pass)',
                '⏰ Depart by 7:30am to maximize your day'
              ]
            },
            {
              title: 'Hiroshima Peace Memorial Park',
              description: 'The Peace Memorial Park and Museum is one of the world\'s most important historical sites. The A-Bomb Dome — the skeletal remains of the only building to survive near ground zero — is hauntingly powerful. The museum tells the stories of survivors with unflinching honesty and a message of hope for peace.',
              details: [
                '🕊️ Museum: ¥200 · Allow 1-2 hours — it\'s deeply moving',
                '🏛️ A-Bomb Dome is visible from outside the museum — a UNESCO World Heritage site',
                '🌸 The park itself is peaceful and beautiful, lined with cherry trees and memorials',
                '📿 The Children\'s Peace Monument with its paper cranes is particularly moving'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast/Snack',
              name: 'Hiroshima Okonomiyaki',
              description: 'Hiroshima-style okonomiyaki is completely different from Osaka\'s — layers of batter, cabbage, bean sprouts, noodles, pork, and egg pressed together on the griddle. It\'s heartier and more complex. Okonomi-mura (Okonomiyaki Village) has dozens of stalls on multiple floors.',
              meta: '💰 $ · 📍 Okonomi-mura, central Hiroshima · ¥800-1,200'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ferry to Miyajima Island',
              description: 'Take the JR ferry (free with JR Pass) from Miyajimaguchi to Miyajima Island. As you approach, the famous red torii gate of Itsukushima Shrine gradually appears, seemingly floating on the water. The island is considered so sacred that no births or deaths have been permitted here for centuries.',
              details: [
                '🚢 JR Miyajima Ferry: free with JR Pass, 10 min crossing',
                '🚂 JR train from Hiroshima to Miyajimaguchi: 27 min',
                '🦌 More friendly deer on the island — they roam everywhere'
              ]
            },
            {
              title: 'Itsukushima Shrine & Floating Torii',
              description: 'The UNESCO World Heritage shrine appears to float on water at high tide — one of Japan\'s three most celebrated views. At low tide, you can walk out to the massive torii gate and stand beneath it. Check tide times and plan accordingly — both experiences are incredible.',
              details: [
                '⛩️ ¥300 · The torii gate is 16m tall and recently restored',
                '🌊 High tide: shrine and torii float. Low tide: walk to the torii base.',
                '📸 Sunset over the torii is legendary if you can time it'
              ]
            },
            {
              title: 'Mt. Misen Hike or Ropeway',
              description: 'If energy permits, take the ropeway (or hike) up Mt. Misen — the island\'s highest peak with panoramic views over the Inland Sea. The summit has ancient boulders, monkeys, and a \"eternal flame\" that\'s burned for 1,200 years.',
              details: [
                '🚡 Ropeway: ¥1,840 return · 15 min ride + 30 min walk to summit',
                '🔥 The Reikado Hall has a flame that\'s burned since 806 AD'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Momiji Manju & Grilled Oysters',
              description: 'Miyajima\'s two must-eats: momiji manju (maple-leaf-shaped cakes filled with red bean, custard, or chocolate) and enormous grilled oysters from the island\'s many street stalls. The oysters here are some of the best in Japan.',
              meta: '💰 $ · 📍 Miyajima Omotesando shopping street'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Osaka',
              description: 'Ferry back to the mainland and take the shinkansen back to Osaka. You\'ll be back by early evening with time for a light dinner near your hotel.',
              details: [
                '🚄 Last ferries around 5-6pm. Miyajimaguchi → Shin-Osaka: ~2 hours total',
                '🍻 Grab a beer and ekiben for the shinkansen ride back'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Yakiniku at Matsusaka (Osaka)',
              description: 'After a big day, treat yourselves to yakiniku (Japanese BBQ). Grill premium wagyu beef at your table — the marbling melts on the griddle. Osaka has some of the best yakiniku in Japan at reasonable prices.',
              meta: '💰 $$$ · 📍 Namba area, Osaka · Wagyu sets from ¥5,000pp'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.3955, lng: 132.4536, label: 'Peace Memorial Park', num: 1, cat: 'attraction', desc: 'Hiroshima\'s moving memorial to atomic bomb victims' },
        { lat: 34.3966, lng: 132.4525, label: 'A-Bomb Dome', num: 2, cat: 'attraction', desc: 'UNESCO skeletal ruins near ground zero' },
        { lat: 34.3956, lng: 132.4579, label: 'Okonomi-mura', num: 3, cat: 'food', desc: 'Multi-floor okonomiyaki food hall' },
        { lat: 34.2961, lng: 132.3196, label: 'Itsukushima Shrine', num: 4, cat: 'attraction', desc: 'Floating shrine and iconic torii gate' },
        { lat: 34.2812, lng: 132.3183, label: 'Mt. Misen', num: 5, cat: 'attraction', desc: 'Island summit with panoramic Inland Sea views' },
        { lat: 34.2978, lng: 132.3193, label: 'Miyajima Town', num: 6, cat: 'food', desc: 'Grilled oysters and momiji manju' }
      ]
    },

    // ========== DAY 13 ==========
    {
      num: 13,
      date: '2026-04-15',
      neighborhoods: 'Osaka Castle · Tenmabashi · Umeda · Nakazakicho',
      title: 'Osaka Exploration — Castle, Culture & Hidden Bars',
      description: "A relaxed day to soak in Osaka\'s energy. Visit the impressive Osaka Castle surrounded by cherry blossoms, explore the quirky retro neighborhood of Nakazakicho, and end with Osaka\'s legendary nightlife — from tiny standing bars to rooftop cocktails.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Osaka Castle & Nishinomaru Garden',
              description: 'Osaka Castle is a stunning sight — the white-and-gold tower rising above massive stone walls and a moat. The Nishinomaru Garden at its base is one of Osaka\'s best cherry blossom spots, with 300 trees framing the castle perfectly. The interior museum is fine, but the park is the real star.',
              details: [
                '🏯 Castle museum: ¥600 · Nishinomaru Garden: ¥200 (cherry blossom season)',
                '🌸 300 cherry trees in Nishinomaru Garden — stunning with the castle backdrop',
                '🚇 Tanimachi 4-chome or Morinomiya Station'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Brooklyn Roasting Company Kitahama',
              description: 'Excellent specialty coffee in a beautifully restored building on the river. A calm, modern start before the Osaka energy kicks in.',
              meta: '💰 $$ · 📍 Kitahama, near Osaka Castle area'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nakazakicho — Osaka\'s Hidden Creative Quarter',
              description: 'This tiny neighborhood near Umeda is Osaka\'s best-kept secret. Crumbling pre-war buildings have been transformed into indie cafés, vintage clothing shops, record stores, and art galleries. It feels like a village inside the city — the anti-Dotonbori. Most tourists have never heard of it.',
              details: [
                '☕ Salon de AManTO is a legendary café in a 100-year-old building',
                '🎵 Tiny vinyl shops and art spaces around every corner',
                '📸 The contrast of old architecture and modern creativity is wonderful'
              ]
            },
            {
              title: 'Spa World — Japanese Super Bathhouse',
              description: 'If you want another onsen experience (or missed Hakone), Spa World in Shinsekai is a massive hot spring complex with baths themed around different countries and regions. It\'s kitsch, fun, and genuinely relaxing. Floors alternate between male/female monthly.',
              details: [
                '♨️ ¥1,500 · Open 24 hours (can even stay overnight)',
                '🌍 Asian-themed floor and European-themed floor — both have unique baths',
                '🧖 Includes saunas, outdoor baths, and relaxation areas'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Chibo Okonomiyaki',
              description: 'High-end okonomiyaki in the Dotonbori area. Their tokubetsu (special) mix loaded with seafood, pork, and cheese is outrageously good. Teppan-grilled right in front of you.',
              meta: '💰 $$ · 📍 Dōtonbori · Multiple floors with canal views'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Osaka Nightlife — Bars & Drinks',
              description: 'Osaka\'s nightlife is warmer and more welcoming than Tokyo\'s. The Ura-Namba (backstreet Namba) area has hundreds of tiny standing bars (tachinomi), each with character. Try nihonshu (sake) at a specialized bar, or head to the Americamura area for cocktails and live music.',
              details: [
                '🍶 Ura-Namba — the narrow back-alleys behind Namba are full of tiny bars',
                '🍸 Americamura (Ame-Mura) — Osaka\'s youth culture hub with cocktail bars',
                '🎵 Osaka people are famously friendly — conversations happen easily at bar counters'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Ajinoya Okonomiyaki & Drinks',
              description: 'Another Osaka okonomiyaki institution — Ajinoya has been grilling since 1945. Their mixed seafood okonomiyaki is legendary. Pair with highballs (Japanese whisky and soda) — the Osaka way.',
              meta: '💰 $$ · 📍 Namba · Since 1945 · Counter seating available'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6873, lng: 135.5262, label: 'Osaka Castle', num: 1, cat: 'attraction', desc: 'Iconic castle surrounded by cherry blossom gardens' },
        { lat: 34.7069, lng: 135.5029, label: 'Nakazakicho', num: 2, cat: 'attraction', desc: 'Hidden creative quarter — cafés, art, vintage' },
        { lat: 34.6520, lng: 135.5065, label: 'Spa World', num: 3, cat: 'attraction', desc: 'Massive themed hot spring complex' },
        { lat: 34.6680, lng: 135.5020, label: 'Ura-Namba Bars', num: 4, cat: 'food', desc: 'Backstreet standing bars and izakaya' },
        { lat: 34.6715, lng: 135.4970, label: 'Americamura', num: 5, cat: 'attraction', desc: 'Youth culture hub with bars and live music' },
        { lat: 34.6688, lng: 135.5028, label: 'Chibo Okonomiyaki', num: 6, cat: 'food', desc: 'High-end okonomiyaki with canal views' }
      ]
    },

    // ========== DAY 14 ==========
    {
      num: 14,
      date: '2026-04-16',
      neighborhoods: 'Osaka → Tokyo · Ginza · Tokyo Station',
      title: 'Last Day — Osaka Morning, Tokyo Farewell',
      description: "Your final day in Japan. Enjoy a last Osaka morning — pick up souvenirs, have one more food adventure — then take the shinkansen back to Tokyo for a farewell evening. A final stroll through Ginza, last-minute gift shopping at Tokyo Station, and a quiet, grateful dinner to close your Japanese journey.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Last Osaka Morning',
              description: 'Sleep in or revisit your favorite spots. Hit Kuromon Market one more time, stock up on Japanese snacks and souvenirs at Don Quijote (open 24 hours), or simply enjoy a slow breakfast at a Namba café.',
              details: [
                '🛍️ Don Quijote (Donki) — the chaotic everything-store. Great for snacks, cosmetics, souvenirs',
                '🍫 Buy: KitKat flavors (matcha, sake, strawberry), rice crackers, instant ramen as gifts',
                '🧳 Pack carefully — Japan\'s souvenirs and snacks multiply'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Shinsekai Morning Set',
              description: 'Many Shinsekai kissaten (retro cafés) offer morning sets — toast, hard-boiled egg, and coffee for just ¥400-500. It\'s a charming old-school Japanese morning ritual.',
              meta: '💰 $ · 📍 Shinsekai · The most Japanese breakfast you can have'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shinkansen Back to Tokyo',
              description: 'Board the Nozomi or Hikari shinkansen from Shin-Osaka to Tokyo (2.5 hours). Enjoy the views one last time — on a clear day, Mt. Fuji will say goodbye from the right-side windows.',
              details: [
                '🚄 Shin-Osaka → Tokyo: 2.5 hours by Hikari (JR Pass) or 2h15 by Nozomi',
                '🍱 Grab a farewell ekiben from the station',
                '🗻 Right-side window for Mt. Fuji views'
              ]
            },
            {
              title: 'Ginza — Elegant Tokyo',
              description: 'Spend your last afternoon in Ginza — Tokyo\'s most elegant shopping district. Even if you don\'t buy anything, the architecture and window displays are stunning. The backstreets hide art galleries, vintage shops, and tiny specialty stores.',
              details: [
                '🛍️ Ginza Six — stunning department store with art installations',
                '🍰 Ginza has incredible patisseries — try Hidemi Sugino or Henri Charpentier',
                '🖼️ Backstreet galleries are free and world-class'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Tokyo Station Gift Shopping',
              description: 'Tokyo Station\'s underground shopping streets (Character Street, Ramen Street, First Avenue) are an attraction in themselves. This is the best place for last-minute omiyage (gifts) — every region of Japan has a specialty shop here.',
              details: [
                '🎁 Tokyo Banana, Shiroihito Koibito, regional mochi — perfect gifts',
                '🍜 Tokyo Ramen Street has 8 top ramen shops if you want one last bowl',
                '🛒 GRANSTA underground shopping is massive'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Farewell Dinner',
              name: 'Sushi Saito or Omakase at Sushi Dai',
              description: 'End your Japan journey the way it deserves — with the finest sushi. For a splurge, Ginza has world-class omakase counters. For something more accessible, find a mid-range sushi counter where the chef selects seasonal fish and tells you the story of each piece. Let the chef guide you.',
              meta: '💰 $$$–$$$$ · 📍 Ginza · Counter omakase is the quintessential farewell meal'
            }
          ],
          tips: [
            { type: 'tip', text: 'If flying out early tomorrow, stay near Tokyo or Shinagawa Station for easy Narita/Haneda Express access. Pack tonight and leave your last morning stress-free. You\'ll be back — Japan has that effect on people.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6687, lng: 135.5013, label: 'Dōtonbori (Last Visit)', num: 1, cat: 'attraction', desc: 'One more Osaka food farewell' },
        { lat: 34.6656, lng: 135.5040, label: 'Don Quijote Namba', num: 2, cat: 'attraction', desc: 'Chaotic everything-store for souvenirs' },
        { lat: 35.6812, lng: 139.7671, label: 'Tokyo Station', num: 3, cat: 'transport', desc: 'Last-minute gifts at underground shopping' },
        { lat: 35.6717, lng: 139.7649, label: 'Ginza', num: 4, cat: 'attraction', desc: 'Tokyo\'s most elegant shopping district' },
        { lat: 35.6751, lng: 139.7630, label: 'Ginza Sushi', num: 5, cat: 'food', desc: 'Farewell omakase sushi counter' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (per night)', budget: '¥8,000–15,000', midrange: '¥15,000–35,000', luxury: '¥35,000–80,000+' },
    { category: 'Ryokan Night (Hakone)', budget: '¥25,000pp', midrange: '¥40,000–60,000pp', luxury: '¥80,000–150,000pp' },
    { category: 'Meals (per couple/day)', budget: '¥5,000–8,000', midrange: '¥10,000–20,000', luxury: '¥30,000–60,000' },
    { category: 'Transport (JR Pass 14-day)', budget: '¥50,000pp', midrange: '¥50,000pp + metro', luxury: '¥50,000pp + taxis' },
    { category: 'Activities & Entry Fees', budget: '¥1,000–2,000/day', midrange: '¥3,000–5,000/day', luxury: '¥5,000–15,000/day' },
    { category: '14-Day Total (couple)', budget: '¥400,000–600,000 (~€2,500–3,700)', midrange: '¥700,000–1,200,000 (~€4,300–7,400)', luxury: '¥1,500,000–3,000,000 (~€9,300–18,500)' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Narita (NRT) or Haneda (HND) — Haneda is closer to central Tokyo', 'Narita Express to Shinjuku: 80 min (¥3,250)', 'Haneda monorail/Keikyu to central Tokyo: 20-30 min', 'Buy JR Pass before arrival or at major JR stations'] },
    { title: '🏨 Where to Stay', items: ['Tokyo: Shinjuku (transport hub) or Shibuya (trendy)', 'Hakone: Traditional ryokan with onsen (book early)', 'Kyoto: Gion area (atmospheric) or near Kyoto Station (convenient)', 'Osaka: Namba (food) or Shinsaibashi (shopping + food)'] },
    { title: '🌡️ Weather (Early April)', items: ['Temperatures: 10-18°C (50-65°F)', 'Cherry blossom peak — magical but popular', 'Light rain possible — pack a compact umbrella', 'Layers recommended — warm days, cool evenings'] },
    { title: '💳 Money & Tipping', items: ['No tipping in Japan — ever. It can be considered rude.', '7-Eleven ATMs accept international cards', 'IC card (Suica/Pasmo) works for transit + konbini', 'Many small restaurants are cash only — carry ¥10,000-20,000'] },
    { title: '📱 Connectivity', items: ['Rent a pocket WiFi at the airport (¥800-1,000/day)', 'Or buy an eSIM (Ubigi, Airalo) before departure', 'Google Maps transit directions work perfectly in Japan', 'Download Google Translate with Japanese offline pack'] },
    { title: '🗣️ Language', items: ['English signage is common in stations and tourist areas', 'Learn: sumimasen (excuse me), arigatou (thanks), kudasai (please)', 'Google Translate camera mode reads Japanese menus instantly', 'Japanese people are incredibly helpful — don\'t hesitate to ask'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
