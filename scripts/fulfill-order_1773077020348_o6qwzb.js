const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1773077020348_o6qwzb',
  email: 'kialogy@gmail.com',
  destination: 'Kihei, HI, USA',
  startDate: '2026-04-13',
  endDate: '2026-04-19',
  groupSize: 2,
  requests: 'Would like a mix of beach, surfing, relaxation, and activities. Have a baby so want to accommodate him.'
};

const itineraryData = {
  destination: 'Kihei, Maui',
  countryEmoji: '🇺🇸',
  title: 'Sand, Surf & Baby Toes on Maui\'s South Shore',
  subtitle: '6 days of gentle beaches, family surf sessions & island flavors in Kihei',
  description: "Kihei is the sweet spot of Maui — sunny almost every day, calm baby-friendly beaches just steps away, and enough adventure to keep parents stoked between nap times. This itinerary balances surf lessons at The Cove with lazy mornings on Kamaole III, a baby-safe Haleakalā visit (no 3am alarm needed), snorkeling at Turtle Town, and some of the island's best poke and plate lunches. Designed for a family with a baby who wants real Maui experiences without the stress.",
  duration: '6 nights',
  dates: 'Apr 13 – Apr 19, 2026',
  budget: '$$–$$$',
  pace: 'Relaxed',
  bestFor: 'Families with Baby',
  highlights: [
    'Surf lessons at The Cove in Kihei — Maui\'s friendliest beginner break',
    'Kamaole Beach III — the island\'s best family beach with grass park and shade',
    'Snorkeling with sea turtles at Turtle Town',
    'Haleakalā at your own pace — no sunrise alarm, just sunset views above the clouds',
    'Poke bowls, shave ice & plate lunches from Kihei\'s best local spots'
  ],

  essentials: [
    { title: '👶 Traveling with Baby', text: 'Kihei is ideal for babies — flat terrain, calm beaches, and easy parking everywhere. Bring or rent a pop-up beach shade tent (available at Snorkel Bob\'s or Boss Frog\'s). Kamaole III has the gentlest shore break and grassy areas perfect for crawlers. Most restaurants are casual and baby-welcoming.' },
    { title: '☀️ April Weather', text: 'April is shoulder season — less crowded than winter, still warm (78-84°F / 25-29°C). Trade winds keep it comfortable. South Maui gets 300+ days of sunshine per year. UV is intense — SPF 50+ for everyone, rash guard for baby in the water.' },
    { title: '🚗 Getting Around', text: 'Rent a car — it\'s essential on Maui. Car seats can be rented with most rental companies. Kihei is a 25-minute drive from Kahului Airport (OGG). Most of your activities are within 10-15 minutes of your accommodation.' },
    { title: '🏖️ Beach Gear', text: 'Rent snorkel gear, beach chairs, coolers, and pop-up tents from Snorkel Bob\'s or Boss Frog\'s in Kihei. They also rent baby beach gear. Buy reef-safe sunscreen — it\'s the law in Hawaii (no oxybenzone or octinoxate).' }
  ],

  days: [
    {
      num: 1,
      date: '2026-04-13',
      neighborhoods: 'Kihei · Kamaole Beach III',
      title: 'Arrival Day — Settle In & First Beach Dip',
      description: "Land on Maui, grab your rental car, and drive straight to Kihei. No agenda — just get your toes in the sand at Kamaole III, the most baby-friendly beach on the island. Gentle waves, soft sand, lifeguards on duty, and a grassy park with shade trees right behind the beach.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive & Settle In',
              description: 'Pick up your rental car at Kahului Airport (OGG) and make a quick stop at Foodland Farms in Kihei for essentials — reef-safe sunscreen, snacks, baby supplies, and the best poke counter on the island.',
              details: [
                '🚗 25-minute drive from OGG to Kihei via Pi\'ilani Highway',
                '🛒 Foodland Farms Kihei — their poke is legendary, grab a bowl for your first lunch',
                '👶 Pick up baby beach essentials if needed — rash guards, swim diapers, shade tent'
              ]
            },
            {
              title: 'First Dip at Kamaole Beach III',
              description: 'This is your home beach for the week. Kam III (as locals call it) has the gentlest shore break of the three Kamaole beaches, a wide grassy park with BBQ grills and shade trees, and a rocky point on the south end where sea turtles often rest.',
              details: [
                '🏖️ Park in the lot off S Kihei Rd — free parking, fills up by 10am on busy days',
                '🐢 Walk to the south rocky point at low tide to spot Hawaiian green sea turtles',
                '👶 The grassy park behind the beach is perfect for baby to play and crawl',
                '🌅 Face west for incredible sunsets — every single night'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Don\'t fight jet lag — let the ocean reset your clock. An early sunset beach session and early bedtime sets you up perfectly for the week.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Nalu\'s South Shore Grill',
              description: 'Casual, family-friendly spot right in the Kihei action. Great fish tacos, burgers, and a solid kids\' menu. Outdoor patio with ocean breezes — relaxed enough for a baby in a high chair.',
              meta: '💰 $$ · 📍 1280 S Kihei Rd · Outdoor patio, high chairs available'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.7644, lng: -156.4450, label: 'Kahului Airport (OGG)', num: 1, cat: 'transport', desc: 'Maui\'s main airport — 25 min to Kihei' },
        { lat: 20.7257, lng: -156.4530, label: 'Foodland Farms Kihei', num: 2, cat: 'food', desc: 'Best poke counter on Maui + grocery essentials' },
        { lat: 20.7140, lng: -156.4495, label: 'Kamaole Beach III', num: 3, cat: 'attraction', desc: 'Baby-friendly beach with grass park and sea turtles' },
        { lat: 20.7330, lng: -156.4530, label: 'Nalu\'s South Shore Grill', num: 4, cat: 'food', desc: 'Casual fish tacos and burgers with outdoor patio' }
      ]
    },
    {
      num: 2,
      date: '2026-04-14',
      neighborhoods: 'The Cove · Kalama Park · Kihei',
      title: 'Surf Day — Catch Your First Wave',
      description: "One of you hits the water for a beginner surf lesson at The Cove — Kihei's mellowest break — while the other hangs with baby on the beach at Kalama Park. Then swap or just celebrate with shave ice. Afternoon is all about slow beach time and the best poke on the island.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Surf Lesson at The Cove',
              description: 'The Cove at the south end of Kalama Park is where every local learned to surf. Gentle, consistent whitewash over a sandy bottom — perfect for beginners. Book a 2-hour group or private lesson with Maui Wave Riders or Surf Club Maui. One parent surfs while the other watches baby from the grassy park just steps away.',
              details: [
                '🏄 2-hour lessons run ~$85-120pp — book ahead for morning slots',
                '🌊 The Cove is the safest beginner break in Kihei — sandy bottom, no reef',
                '👶 Kalama Park is right there with shade, grass, and restrooms',
                '📸 The non-surfing parent gets epic photo duty from the park'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Kihei Caffe',
              description: 'The go-to Kihei breakfast spot. No-frills, massive portions, always a line (worth it). Their loco moco and banana macadamia nut pancakes are iconic.',
              meta: '💰 $ · 📍 1945 S Kihei Rd · Cash only, opens 6am · Get there early'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kalama Park Beach Hang',
              description: 'After surfing, spend the afternoon at Kalama Park. This local-favorite park has a huge grassy area, skate park, basketball courts, and a calm beach. Great for baby to nap under a shade tent while you decompress.',
              details: [
                '🌴 Large banyan trees provide natural shade',
                '🧊 Ululani\'s Hawaiian Shave Ice is across the street — best on the island',
                '👶 Flat, grassy areas perfect for baby to play'
              ]
            }
          ],
          meals: [
            {
              type: '🍧 Snack',
              name: 'Ululani\'s Hawaiian Shave Ice',
              description: 'Not your mainland snow cone. Ultra-fine shave ice with real fruit syrups, haupia cream, and mochi balls. Get the "No Ka Oi" combo. Life-changing.',
              meta: '💰 $ · 📍 Kihei (multiple locations) · Try the li hing mui flavor'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'South Maui Fish Company',
              description: 'Featured on Diners, Drive-Ins and Dives. Tiny spot, massive flavor. Fresh-caught poke by the pound, fish tacos with coconut slaw, and grilled mahi plates. Get there before they sell out — the fish is never frozen.',
              meta: '💰 $$ · 📍 1913 S Kihei Rd · Opens 11am, often sells out by 5pm · CASH ONLY'
            }
          ],
          tips: [
            { type: 'tip', text: 'South Maui Fish Co sells out fast. Go for an early dinner (4pm) or grab takeout for a sunset beach dinner at Kam III. The poke by the pound is the move.' }
          ]
        }
      ],
      mapPins: [
        { lat: 20.7295, lng: -156.4555, label: 'The Cove (Surf Break)', num: 1, cat: 'attraction', desc: 'Kihei\'s gentlest beginner surf spot — sandy bottom' },
        { lat: 20.7310, lng: -156.4540, label: 'Kalama Park', num: 2, cat: 'attraction', desc: 'Large beach park with grass, shade, and restrooms' },
        { lat: 20.7340, lng: -156.4530, label: 'Kihei Caffe', num: 3, cat: 'food', desc: 'Iconic breakfast spot — loco moco and pancakes' },
        { lat: 20.7320, lng: -156.4535, label: 'Ululani\'s Shave Ice', num: 4, cat: 'food', desc: 'Best shave ice on Maui — real fruit syrups' },
        { lat: 20.7260, lng: -156.4520, label: 'South Maui Fish Company', num: 5, cat: 'food', desc: 'Famous poke and fish tacos — sells out daily' }
      ]
    },
    {
      num: 3,
      date: '2026-04-15',
      neighborhoods: 'Ma\'alaea · Wailea · Makena',
      title: 'Ocean Explorer Day — Turtles, Tidepools & Sunset Luau',
      description: "Start at the Maui Ocean Center — one of the best aquariums in Hawaii and a hit with babies. Afternoon snorkeling at Turtle Town (take turns with baby). End the day with a traditional luau at the Wailea Beach Resort.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Maui Ocean Center',
              description: 'Hawaii\'s largest aquarium and a perfect baby-friendly activity. Walk through the 750,000-gallon open-ocean exhibit with sharks, rays, and tropical fish. The outdoor turtle lagoon and touch pools are mesmerizing for little ones. Plan about 2-3 hours.',
              details: [
                '🐠 Open 9am-5pm · ~$40/adult, free for ages 0-2',
                '🦈 The 54-foot-long acrylic tunnel through the shark tank is incredible',
                '🐢 Outdoor Hawaiian green sea turtle lagoon — babies love watching them',
                '👶 Stroller-friendly, air-conditioned, restrooms with changing stations'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Snorkeling at Turtle Town',
              description: 'Drive to Maluaka Beach in Makena — the gateway to Turtle Town. One parent snorkels with sea turtles while the other relaxes with baby on this beautiful, relatively uncrowded beach. The water is calm and clear, and turtles are almost guaranteed.',
              details: [
                '🐢 Hawaiian green sea turtles feed on the reef here — nearly 100% sighting rate',
                '🤿 Bring your own gear or rent from Snorkel Bob\'s in Kihei',
                '📏 Stay 10 feet from all sea turtles — it\'s federal law',
                '🏖️ Maluaka Beach has shade trees, calm water, and is baby-friendly on the sand'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Turtle Town is best in the morning when water is calmest and clearest. If you go afternoon, aim for before 2pm. Take turns — one snorkels, one watches baby. Swap and repeat.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Te Au Moana Luau at Wailea Beach Resort',
              description: 'A proper Hawaiian luau with fire dancing, hula, live music, and a traditional feast. This is one of the more intimate luaus on Maui and wraps up earlier than most — great for families with babies. Beachfront setting with sunset views.',
              details: [
                '🔥 Fire knife dancing, Polynesian performances, and live Hawaiian music',
                '🍖 Kalua pork, lomi salmon, poi, haupia — full traditional spread',
                '🌅 Starts around 5pm, wraps by 8:30pm — baby-friendly timing',
                '💰 ~$150-180/adult · Book in advance — sells out in peak season'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.7930, lng: -156.5090, label: 'Maui Ocean Center', num: 1, cat: 'attraction', desc: 'Hawaii\'s best aquarium — sharks, rays, sea turtles' },
        { lat: 20.6620, lng: -156.4415, label: 'Maluaka Beach / Turtle Town', num: 2, cat: 'attraction', desc: 'Calm beach with guaranteed sea turtle snorkeling' },
        { lat: 20.6870, lng: -156.4430, label: 'Wailea Beach Resort', num: 3, cat: 'attraction', desc: 'Te Au Moana Luau — fire dancing and traditional feast' }
      ]
    },
    {
      num: 4,
      date: '2026-04-16',
      neighborhoods: 'Haleakalā · Upcountry Maui · Kula',
      title: 'Above the Clouds — Haleakalā Without the 3am Alarm',
      description: "You don't need the 3am sunrise slot to experience Haleakalā. Drive up mid-morning when baby is happy, explore the crater views in warm daylight, then wind through Upcountry Maui's lavender farms and cowboy town of Makawao. Return for sunset at the summit if energy allows.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive Up Haleakalā (Late Morning)',
              description: 'Skip the brutal 3am sunrise drive — with a baby, the mid-morning approach is way better. The crater views are just as spectacular in daylight, there are no crowds, and baby won\'t be miserable in 40°F darkness. The drive from Kihei to the summit takes about 90 minutes.',
              details: [
                '🌋 Summit elevation: 10,023 feet — dress in layers, it\'s 30-40°F colder than the beach',
                '🚗 No reservation needed outside of sunrise hours (before 7am)',
                '👶 Bundle baby in warm layers — hoodies, blankets, socks',
                '🅿️ $30 park entry fee per vehicle (valid 3 days)',
                '⚠️ Watch baby for altitude — if fussy, head down. Most babies do fine.'
              ]
            },
            {
              title: 'Haleakalā Crater Overlooks',
              description: 'Walk to the main overlooks — Pu\'u \'Ula\'ula (Summit), Kalahaku, and Leleiwi. The volcanic landscape looks like the surface of Mars. On clear days you can see the Big Island, Moloka\'i, and Lana\'i.',
              details: [
                '📸 The colors shift dramatically with the light — reds, purples, silvers',
                '🌌 If you return for sunset, the crater fills with golden light — transcendent',
                '🦅 Look for the nēnē (Hawaiian goose) — Hawaii\'s state bird lives here'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ali\'i Kula Lavender Farm',
              description: 'On the way down from Haleakalā, stop at this fragrant hillside farm at 4,000 feet elevation. Gorgeous gardens with lavender and native plants, incredible views of the central valley and ocean. Baby will love the colors and smells.',
              details: [
                '💜 Walking garden tour — stroller-friendly paths',
                '📸 Photo ops everywhere — lavender rows with ocean backdrop',
                '🛍️ Gift shop with lavender scones, honey, and sachets'
              ]
            },
            {
              title: 'Makawao Town',
              description: 'This former paniolo (Hawaiian cowboy) town is now an artsy, laid-back village with boutiques, galleries, and one of the best bakeries on Maui. Stroll the main street and soak up the Upcountry vibe.',
              details: [
                '🍩 Komoda Store & Bakery — legendary cream puffs and stick doughnuts (get there early, they sell out)',
                '🎨 Small galleries and surf shops along Baldwin Avenue',
                '🤠 Paniolo (cowboy) heritage — Maui\'s ranch country'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Grandma\'s Coffee House',
              description: 'Charming café on the slopes of Haleakalā in tiny Keokea. Home-roasted 100% Maui coffee, generous sandwiches, and homemade pies. The lanai has sweeping views of the south coast.',
              meta: '💰 $ · 📍 9232 Kula Hwy, Keokea · Cash preferred'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Monkeypod Kitchen',
              description: 'Locally-sourced craft cuisine in Wailea. Famous for their mai tais (36 flavors of ice cream for the pie!) and wood-fired pizzas. Live music nightly. Great high chairs and a family-friendly vibe.',
              meta: '💰 $$$ · 📍 10 Wailea Gateway Pl · Happy hour 3-5:30pm is the move'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.7097, lng: -156.2500, label: 'Haleakalā Summit', num: 1, cat: 'attraction', desc: '10,023ft volcano crater — above the clouds' },
        { lat: 20.7580, lng: -156.3280, label: 'Ali\'i Kula Lavender Farm', num: 2, cat: 'attraction', desc: 'Fragrant hillside gardens with ocean views' },
        { lat: 20.7660, lng: -156.3430, label: 'Grandma\'s Coffee House', num: 3, cat: 'food', desc: '100% Maui coffee on the slopes of Haleakalā' },
        { lat: 20.9210, lng: -156.3380, label: 'Makawao Town', num: 4, cat: 'attraction', desc: 'Artsy cowboy town with legendary bakery' },
        { lat: 20.6880, lng: -156.4430, label: 'Monkeypod Kitchen', num: 5, cat: 'food', desc: 'Craft cocktails, wood-fired pizza, live music' }
      ]
    },
    {
      num: 5,
      date: '2026-04-17',
      neighborhoods: 'Wailea · Ulua Beach · Shops at Wailea',
      title: 'Wailea Day — Luxury Beach, Coastal Trail & Spa Vibes',
      description: "Today is pure relaxation. Walk the paved Wailea Beach Path along some of the most beautiful coastline in Hawaii, snorkel at calm Ulua Beach, and browse the high-end Shops at Wailea. This is the resort side of Maui — polished, gorgeous, and surprisingly baby-friendly.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Wailea Beach Path',
              description: 'A beautiful 1.5-mile paved coastal path connecting five crescent beaches and some of Maui\'s best resorts. Completely stroller-friendly — smooth pavement, gorgeous views, and beach access points every few minutes. Morning light is magic here.',
              details: [
                '🚶 1.5 miles, paved, flat — perfect for strollers and baby carriers',
                '🏖️ Five beaches along the walk: Mokapu, Ulua, Wailea, Polo, and Makena',
                '🐋 April is the tail end of whale season — watch for spouts offshore',
                '📸 The path passes through resort gardens — great photo ops'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Lineage at the Shops at Wailea',
              description: 'Chef Sheldon Simeon\'s (Top Chef) celebration of local Hawaiian flavors. His breakfast dishes — like the chili pepper fried rice and spam musubi — are incredible. One of the best chefs on the island.',
              meta: '💰 $$$ · 📍 3750 Wailea Alanui Dr · Reservations recommended'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Snorkel at Ulua Beach',
              description: 'Ulua Beach has some of the best shore snorkeling in Wailea. The reef on the right side is loaded with tropical fish, and the beach itself has calm, clear water. One parent snorkels, the other beach-hangs with baby under the shade trees.',
              details: [
                '🤿 Enter at the right side of the beach — the reef starts just offshore',
                '🐠 Look for humuhumunukunukuāpua\'a (reef triggerfish) — Hawaii\'s state fish',
                '🏖️ Shade trees at the back of the beach — claim a spot early',
                '🚿 Showers and restrooms in the parking lot'
              ]
            },
            {
              title: 'Shops at Wailea',
              description: 'Upscale open-air shopping center with restaurants, boutiques, and a free Tuesday evening hula show. Air-conditioned shops are a nice baby cool-down break. Browse local art, pick up koa wood jewelry, or just get gelato.',
              details: [
                '💃 Free hula show — check schedule (usually Tuesdays)',
                '🍦 Lappert\'s Hawaii ice cream — Kona coffee flavor is incredible',
                '🛍️ Mix of luxury brands and local Maui boutiques'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset at Keawakapu Beach',
              description: 'This is the secret sunset beach between Kihei and Wailea. Less crowded than Kamaole, stunning views of Molokini and Kaho\'olawe, and the sand is like powdered sugar. Bring a blanket and a bottle of wine.',
              details: [
                '🌅 One of the best sunset beaches on Maui — wide open western view',
                '🏖️ Parking at the south end off Kilohana Dr',
                '🐢 Turtles sometimes come ashore here at dusk'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Eskimo Candy Seafood Market & Café',
              description: 'Local institution since 1989. Part fish market, part café — the freshest seafood on the island. Their fish and chips use today\'s catch, and the smoked marlin spread is legendary. No-frills, all flavor.',
              meta: '💰 $$ · 📍 2665 Wai Wai Pl, Kihei · Lunch/early dinner — closes 5-6pm'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.6880, lng: -156.4430, label: 'Wailea Beach Path', num: 1, cat: 'attraction', desc: 'Paved 1.5-mile coastal walk — stroller-friendly' },
        { lat: 20.6940, lng: -156.4430, label: 'Ulua Beach', num: 2, cat: 'attraction', desc: 'Calm snorkeling beach with shade trees' },
        { lat: 20.6895, lng: -156.4430, label: 'Shops at Wailea', num: 3, cat: 'attraction', desc: 'Upscale shopping, dining, and hula shows' },
        { lat: 20.6995, lng: -156.4485, label: 'Keawakapu Beach', num: 4, cat: 'attraction', desc: 'Secret sunset beach with powdered-sugar sand' },
        { lat: 20.7160, lng: -156.4500, label: 'Eskimo Candy', num: 5, cat: 'food', desc: 'Legendary local seafood market and café' },
        { lat: 20.6895, lng: -156.4430, label: 'Lineage', num: 6, cat: 'food', desc: 'Top Chef Sheldon Simeon\'s Hawaiian cuisine' }
      ]
    },
    {
      num: 6,
      date: '2026-04-18',
      neighborhoods: 'North Shore · Pa\'ia · Ho\'okipa · Kihei',
      title: 'North Shore Adventure & Aloha Sunset',
      description: "Your last full day — cruise up to Maui's funky North Shore. Browse Pa'ia's surf shops and galleries, watch pro surfers and sea turtles at Ho'okipa Beach, grab the island's most famous fish tacos, and end with a final sunset at your home beach.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Pa\'ia Town Stroll',
              description: 'This colorful surf town on the North Shore is Maui\'s bohemian heart. Rainbow-painted storefronts, surf shops, yoga studios, and the best fish tacos you\'ll ever eat. It\'s a quick 30-minute drive from Kihei and feels like a different world.',
              details: [
                '🏄 Pa\'ia is where pro surfers, hippies, and artists collide',
                '🛍️ Browse Maui Crafts Guild for local art and jewelry',
                '📸 The colorful storefronts make great family photos',
                '🅿️ Street parking can be tight — arrive before 10am'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast/Brunch',
              name: 'Pa\'ia Fish Market',
              description: 'Island institution. Their fish tacos and fish burgers are made with whatever was caught that morning. No-frills — order at the counter, grab a picnic table. This is the real deal.',
              meta: '💰 $$ · 📍 100 Hana Hwy, Pa\'ia · Opens 11am · Always packed, worth the wait'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ho\'okipa Beach Park — Turtles & Surf Watching',
              description: 'Just past Pa\'ia, Ho\'okipa is one of the best spots on earth to watch world-class windsurfing and kiteboarding. The lookout above the beach gives you a bird\'s-eye view. In the afternoon, Hawaiian green sea turtles haul out on the sand to rest — you can watch from the designated viewing area.',
              details: [
                '🐢 Turtles come ashore in the afternoon — the viewing area is roped off and stroller-accessible',
                '🏄 The surf here is serious — just watch, don\'t swim (strong currents)',
                '📸 The lookout parking lot is the best vantage point',
                '👶 Short stop — 30-45 minutes is perfect with a baby'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Ho\'okipa turtles usually arrive after 2pm. The viewing ropes keep you at a safe distance. Rangers are sometimes present — they\'re friendly and full of turtle facts.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Sunset at Kamaole Beach III',
              description: 'Come full circle. Return to your home beach for one last Maui sunset. Spread out a blanket, crack open some poke from Foodland, and watch the sky turn orange and pink over the Pacific. This is the moment you\'ll remember.',
              details: [
                '🌅 Sunsets in April are around 6:45pm — arrive by 6pm',
                '🍱 Grab poke and snacks from Foodland Farms on the way',
                '👶 Grassy park is perfect for baby\'s last Maui crawl',
                '📸 The green flash is real — watch for it as the sun dips below the horizon'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Maui Brewing Company',
              description: 'End the trip at Maui\'s biggest craft brewery. Big outdoor dining area where kids can run around (or crawl). Great burgers, tacos, and fresh-brewed Bikini Blonde ale. Live music some nights.',
              meta: '💰 $$ · 📍 605 Lipoa Pkwy, Kihei · Outdoor seating, very family-friendly'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.9375, lng: -156.3560, label: 'Pa\'ia Town', num: 1, cat: 'attraction', desc: 'Bohemian surf town with galleries and shops' },
        { lat: 20.9375, lng: -156.3560, label: 'Pa\'ia Fish Market', num: 2, cat: 'food', desc: 'Legendary fish tacos — Maui institution' },
        { lat: 20.9360, lng: -156.3290, label: 'Ho\'okipa Beach Park', num: 3, cat: 'attraction', desc: 'World-class surf watching and turtle beach' },
        { lat: 20.7140, lng: -156.4495, label: 'Kamaole Beach III', num: 4, cat: 'attraction', desc: 'Your home beach — one last sunset' },
        { lat: 20.7175, lng: -156.4460, label: 'Maui Brewing Company', num: 5, cat: 'food', desc: 'Craft brewery with outdoor family dining' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$200–350/night', midrange: '$350–550/night', luxury: '$600–1200/night' },
    { category: 'Meals (per couple + baby)', budget: '$60–100/day', midrange: '$120–200/day', luxury: '$250–400/day' },
    { category: 'Rental Car', budget: '$70–100/day', midrange: '$100–150/day', luxury: '$150–250/day' },
    { category: 'Activities', budget: '$0–50/day', midrange: '$50–150/day', luxury: '$150–300/day' },
    { category: 'Luau (2 adults)', budget: '—', midrange: '$300–360', luxury: '$400–600 (premium seating)' },
    { category: '6-Day Total', budget: '$3,000–5,000', midrange: '$5,000–8,000', luxury: '$8,000–15,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Kahului Airport (OGG) — most mainland flights are direct from west coast cities', 'Kihei is a 25-minute drive south via Pi\'ilani Highway (Hwy 31)', 'Rent a car at the airport — you need one on Maui, period', 'Car seat can be rented with most companies or bring your own'] },
    { title: '🏨 Where to Stay', items: ['Kihei condo rentals are the best value — full kitchen, washer/dryer, pool (VRBO/Airbnb)', 'Kamaole Sands — directly across from Kam III, pools + hot tubs, baby-friendly', 'Wailea resorts if you want luxury — Four Seasons, Grand Wailea, Fairmont Kea Lani', 'Look for ground-floor units for stroller access and late-night walks'] },
    { title: '👶 Baby Essentials', items: ['Rent cribs, strollers, car seats, beach gear from Baby\'s Away Maui or Maui Baby Rentals', 'Most Kihei condos have full kitchens — great for baby food prep', 'Pack swim diapers, rash guards, and a pop-up beach shade tent', 'Bring a baby carrier (Ergobaby, etc.) for hikes and town strolling'] },
    { title: '🌡️ Weather', items: ['April averages 78-84°F (25-29°C) — perfect beach weather', 'Trade winds keep humidity comfortable on the south shore', 'UV is extreme — reef-safe SPF 50+ is mandatory (and the law)', 'Occasional brief afternoon showers, mostly sunny'] },
    { title: '💳 Money & Tips', items: ['Card accepted everywhere — but some spots are cash only (Kihei Caffe, South Maui Fish Co)', 'Tipping: 18-20% at restaurants, $5-10/person for surf lessons', 'Grocery prices are 20-30% higher than mainland — stock up at Costco near the airport', 'Happy hours are your friend — Monkeypod 3-5:30pm is legendary'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}