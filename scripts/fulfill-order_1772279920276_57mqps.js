const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772279920276_57mqps',
  email: 'angelbmw2003@yahoo.com',
  destination: 'Puerto Vallarta, Jalisco, Mexico',
  startDate: '2026-05-28',
  endDate: '2026-06-04',
  groupSize: '3-4',
  requests: ''
};

const itineraryData = {
  destination: 'Puerto Vallarta, Mexico',
  countryEmoji: '🇲🇽',
  title: 'Adventure, Flavor & Ocean Bliss in Puerto Vallarta',
  subtitle: '7 days of jungle thrills, street tacos & Pacific sunsets for your crew',
  description: "Puerto Vallarta is where the Sierra Madre jungle tumbles into the Pacific — a place where you can zipline through tropical canopy in the morning, feast on fresh ceviche at a beachfront palapa by noon, and sink into a sunset cocktail on the Malecón by evening. This itinerary balances adrenaline-pumping adventures with the best food scene on Mexico's Pacific coast and plenty of hammock time on golden sand beaches. Budget-friendly, endlessly delicious, and absolutely unforgettable.",
  duration: '7 nights',
  dates: 'May 28 – Jun 4, 2026',
  budget: '$–$$',
  pace: 'Balanced',
  bestFor: 'Friend Groups',
  highlights: [
    'Zipline & ATV through the Sierra Madre jungle',
    'Vallarta food tour through hidden taco stands & markets',
    'Boat trip to the secret beach at Marietas Islands',
    'Snorkeling at Los Arcos marine park',
    'Sunset cocktails on the iconic Malecón',
    'Day trip to the charming beach village of Sayulita'
  ],

  essentials: [
    { title: '🌴 Tropical Weather', text: 'Late May/early June is the start of rainy season — expect warm 28-32°C days with brief afternoon showers. Mornings are usually sunny and perfect for activities. Pack light clothes, reef-safe sunscreen, and a light rain jacket.' },
    { title: '💰 Budget-Friendly', text: 'Puerto Vallarta is incredibly affordable. Street tacos are 15-25 pesos each, local buses cost 10 pesos, and many beaches and attractions are free. Your biggest expenses will be organized tours and sit-down restaurants.' },
    { title: '🚐 Getting Around', text: 'Local buses run everywhere for 10 pesos. Uber works great and is very cheap. For day trips, book tours with transport included. The Zona Romántica, Malecón, and downtown are all walkable.' },
    { title: '🌊 Ocean Safety', text: 'The Pacific can have strong currents — swim at lifeguarded beaches like Playa de los Muertos. For snorkeling, calm mornings are best. Respect marine park rules at Los Arcos and Marietas Islands.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-05-28',
      neighborhoods: 'Zona Romántica · Malecón · Old Town',
      title: 'Arrival — Malecón Magic & First Tacos',
      description: "Touch down in paradise and dive straight into PV's vibrant heart. Stroll the famous Malecón seaside promenade with its sculptures and street performers, then explore the Zona Romántica — the city's most charming neighborhood packed with restaurants, bars, and character.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Malecón Boardwalk Stroll',
              description: "Walk the mile-long Malecón oceanfront promenade lined with whimsical bronze sculptures, street art, and vendors. Stop at the iconic Caballero del Mar (Seahorse) sculpture — it's the unofficial symbol of PV and your first great group photo op.",
              details: [
                '📸 Don\'t miss "Rotunda of the Sea" sculpture — surreal and photogenic',
                '🎭 Street performers and live music most evenings',
                '🌅 The north end has the best sunset views'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Hit the Malecón around 5-6pm when the heat eases and the golden hour light makes everything glow. Street performers come out and the vibe is electric.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Zona Romántica Bar & Taco Crawl',
              description: "The Zona Romántica comes alive at night. Hit up the taco stands on Basilio Badillo street — every block has legendary spots. Follow the smoke from the grills and order whatever the locals are eating.",
              details: [
                '🌮 Pancho\'s Takos — iconic late-night spot on Constitución',
                '🍺 Los Muertos Brewing — craft beer with a local twist',
                '🎶 Live music spills from every other doorway'
              ]
            }
          ],
          meals: [
            {
              type: '🌮 Dinner',
              name: 'Mariscos Cisneros',
              description: 'No-frills beachfront seafood shack on Playa de los Muertos serving the freshest ceviche, aguachile, and whole grilled fish. Cold beers, plastic chairs, and ocean views — this is the real PV.',
              meta: '💰 $ · 📍 Playa de los Muertos beach · Cash preferred'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.6110, lng: -105.2353, label: 'Malecón Boardwalk', num: 1, cat: 'attraction', desc: 'Iconic oceanfront promenade with sculptures and sunset views' },
        { lat: 20.6044, lng: -105.2310, label: 'Zona Romántica', num: 2, cat: 'attraction', desc: 'PV\'s most charming neighborhood — restaurants, bars, and character' },
        { lat: 20.6035, lng: -105.2330, label: 'Playa de los Muertos', num: 3, cat: 'attraction', desc: 'Popular beach with pier, vendors, and beachfront restaurants' },
        { lat: 20.6050, lng: -105.2305, label: 'Mariscos Cisneros', num: 4, cat: 'food', desc: 'Fresh ceviche and grilled fish on the beach' },
        { lat: 20.6055, lng: -105.2295, label: 'Pancho\'s Takos', num: 5, cat: 'food', desc: 'Legendary late-night taco stand' }
      ]
    },
    {
      num: 2,
      date: '2026-05-29',
      neighborhoods: 'Sierra Madre · Canopy River · Jungle',
      title: 'Jungle Adventure — Ziplines, ATVs & River Swims',
      description: "Today is pure adrenaline. Head into the Sierra Madre mountains for a day of zipline canopy tours, ATV rides through jungle trails, and swimming in crystal-clear river pools. This is the adventure highlight of the trip.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Canopy Zipline & ATV Tour',
              description: "Get picked up from your hotel and head into the lush Sierra Madre jungle for an action-packed morning. Soar over the jungle canopy on 10+ ziplines (including one of the longest in Mexico), then hop on ATVs to tear through muddy jungle trails to a hidden river.",
              details: [
                '🏔️ Canopy River or Vallarta Adventures are top-rated operators',
                '🤸 The longest zipline is over 1km — absolutely thrilling',
                '🏍️ ATV trails wind through tropical forest and small villages',
                '💦 End at a pristine river pool — bring your swimsuit!'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Book the morning slot (8-9am pickup) — it\'s cooler, less crowded, and you avoid afternoon rain. Wear closed-toe shoes and clothes you don\'t mind getting muddy.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Jungle River Swimming & Relaxation',
              description: "After the adrenaline rush, unwind at the river pools. Most tour operators include lunch at a riverside palapa — fresh grilled fish, guacamole, and cold drinks in the middle of the jungle. It's paradise.",
              details: [
                '🏊 Crystal-clear natural pools surrounded by jungle',
                '🍽️ Tour usually includes a traditional Mexican lunch',
                '🌿 Keep eyes peeled for iguanas, toucans, and butterflies'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Included Jungle Lunch',
              description: 'Traditional Mexican lunch at the tour\'s riverside palapa — grilled fish, fresh guacamole, tortillas, and cold beverages surrounded by jungle.',
              meta: '💰 Included with tour · 📍 Sierra Madre riverside'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Café des Artistes',
              description: 'One of PV\'s most acclaimed restaurants. Chef Thierry Blouet serves creative Mexican-French fusion in a gorgeous garden setting. A splurge-worthy dinner after your adventure day.',
              meta: '💰 $$$ · 📍 Guadalupe Sánchez 740, Centro · Reservations essential'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.6730, lng: -105.2100, label: 'Canopy River Ziplines', num: 1, cat: 'attraction', desc: 'World-class zipline and ATV tour through Sierra Madre jungle' },
        { lat: 20.6750, lng: -105.2050, label: 'Jungle River Pools', num: 2, cat: 'attraction', desc: 'Natural swimming pools in the heart of the jungle' },
        { lat: 20.6145, lng: -105.2340, label: 'Café des Artistes', num: 3, cat: 'food', desc: 'Acclaimed Mexican-French fusion in a garden setting' }
      ]
    },
    {
      num: 3,
      date: '2026-05-30',
      neighborhoods: 'Banderas Bay · Los Arcos · Yelapa',
      title: 'Ocean Day — Snorkeling, Hidden Beaches & Yelapa',
      description: "Take to the water today. A boat trip around Banderas Bay hits the best snorkeling at Los Arcos marine park, stops at secluded beaches only reachable by water, and ends at the dreamy fishing village of Yelapa with its waterfall and hammock-strung palapas.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Snorkeling at Los Arcos Marine Park',
              description: "Board a boat from the Los Muertos pier and head south to Los Arcos — dramatic granite rock formations jutting from the sea that shelter an incredible underwater world. Snorkel among tropical fish, sea turtles, and rays in crystal-clear water.",
              details: [
                '🐢 Sea turtles are commonly spotted here',
                '🪨 Swim through natural rock arches and tunnels',
                '🐟 Bring an underwater camera — the colors are spectacular',
                '🚤 Book a panga (small boat) tour for a more intimate experience'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Yelapa Beach Village',
              description: "Continue by boat to Yelapa — a tiny fishing village with no roads in or out, only accessible by water. Swim in the warm bay, hike 20 minutes to a jungle waterfall, and eat fresh fish at a beachside palapa. Time feels different here.",
              details: [
                '🏝️ No cars, no roads — just boats, beach, and jungle',
                '💧 The waterfall is a short hike through the village — totally worth it',
                '🦎 Traditional pie ladies sell homemade coconut and chocolate pies on the beach'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Beachside Palapa in Yelapa',
              description: 'Fresh whole grilled fish (pescado zarandeado), ceviche, and cold Pacíficos at a no-name beachside palapa. Feet in the sand, waves lapping. Perfection.',
              meta: '💰 $ · 📍 Yelapa beach · Cash only'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🌮 Dinner',
              name: 'El Barracuda',
              description: 'Hip, modern seafood restaurant in the Zona Romántica. Creative ceviches, octopus tacos, and mezcal cocktails. Perfect post-ocean-day dinner.',
              meta: '💰 $$ · 📍 Zona Romántica'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.5483, lng: -105.2917, label: 'Los Arcos Marine Park', num: 1, cat: 'attraction', desc: 'Dramatic rock formations with incredible snorkeling' },
        { lat: 20.5033, lng: -105.3367, label: 'Yelapa', num: 2, cat: 'attraction', desc: 'Remote fishing village accessible only by boat' },
        { lat: 20.5050, lng: -105.3350, label: 'Yelapa Waterfall', num: 3, cat: 'attraction', desc: 'Jungle waterfall a short hike from the beach' },
        { lat: 20.6035, lng: -105.2330, label: 'Los Muertos Pier', num: 4, cat: 'attraction', desc: 'Departure point for boat tours' },
        { lat: 20.6048, lng: -105.2300, label: 'El Barracuda', num: 5, cat: 'food', desc: 'Creative seafood and mezcal cocktails' }
      ]
    },
    {
      num: 4,
      date: '2026-05-31',
      neighborhoods: 'Centro · Isla Cuale · Gringo Gulch',
      title: 'Culture & Food — Markets, Murals & a Food Tour',
      description: "Dive deep into PV's culinary and cultural soul. Join a walking food tour through the markets and taco stands that tourists never find, explore the river island of Isla Cuale, and discover the hillside neighborhood of Gringo Gulch with its Elizabeth Taylor history.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Vallarta Food Tour',
              description: "Join Vallarta Eats Food Tours for a 3-hour guided crawl through PV's best street food and markets. You'll hit 8-10 stops — from birria tacos and fresh churros to ceviche carts and mezcal tastings. Your guide explains the history and technique behind each dish.",
              details: [
                '🌮 Stops include: birria, al pastor, ceviche, churros, mezcal',
                '🏪 Mercado Municipal Isla Cuale — the local market few tourists visit',
                '🧑‍🍳 Small group size means personal attention and extra samples',
                '⏰ Morning tours start around 10am — book online in advance'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Isla Cuale & Street Art Walk',
              description: "Cross the bridges to Isla Cuale — a river island in the center of town with a small museum, art galleries, and shady pathways. Then head uphill to Gringo Gulch, the hillside neighborhood where Elizabeth Taylor and Richard Burton had their famous love affair.",
              details: [
                '🌉 The island sits in the middle of the Río Cuale',
                '🎨 Street art and murals throughout the centro streets',
                '🏠 Casa Kimberly — Liz Taylor\'s former home, now a boutique hotel you can tour'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The food tour will fill you up — skip breakfast and come hungry. Afternoon is perfect for a slow stroll and ice cream from one of the many neverías (ice cream shops) downtown.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍷 Dinner',
              name: 'La Palapa',
              description: 'Iconic beachfront restaurant on Playa de los Muertos. Toes-in-the-sand dining with torchlit tables, fresh seafood, and Mexican specialties. The most romantic dinner spot in PV.',
              meta: '💰 $$–$$$ · 📍 Playa de los Muertos · Reservations recommended for sunset tables'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.6085, lng: -105.2340, label: 'Mercado Municipal', num: 1, cat: 'food', desc: 'Bustling local market — the heart of PV food culture' },
        { lat: 20.6100, lng: -105.2345, label: 'Isla Cuale', num: 2, cat: 'attraction', desc: 'River island with galleries, museum, and shady paths' },
        { lat: 20.6120, lng: -105.2330, label: 'Gringo Gulch', num: 3, cat: 'attraction', desc: 'Historic hillside neighborhood — Liz Taylor\'s old haunt' },
        { lat: 20.6125, lng: -105.2325, label: 'Casa Kimberly', num: 4, cat: 'attraction', desc: 'Elizabeth Taylor\'s former home, now a boutique hotel' },
        { lat: 20.6030, lng: -105.2335, label: 'La Palapa', num: 5, cat: 'food', desc: 'Toes-in-the-sand beachfront fine dining' }
      ]
    },
    {
      num: 5,
      date: '2026-06-01',
      neighborhoods: 'Sayulita · San Pancho · Riviera Nayarit',
      title: 'Day Trip — Sayulita Surf Town & San Pancho',
      description: "Escape to the bohemian surf towns of Sayulita and San Pancho, about an hour north of PV. Sayulita is a colorful, vibrant village with surfing, shopping, and incredible food. San Pancho (San Francisco) is its quieter, artsy neighbor — equally charming.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sayulita Beach & Surf Lesson',
              description: "Arrive in Sayulita and head straight to the beach. The beginner-friendly waves are perfect for a first surf lesson (or just bodysurf in the warm water). The town's colorful streets, papel picado decorations, and laid-back energy are infectious.",
              details: [
                '🏄 Surf lessons run about $40 USD per person — no experience needed',
                '🎨 The streets are covered in colorful murals and papel picado banners',
                '🛍️ Browse the Huichol art galleries and bohemian boutiques',
                '🚐 Take a bus from PV (1 hour, ~$3 USD) or book a shared shuttle'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'ChocoBanana',
              description: 'Sayulita institution famous for smoothie bowls, fresh juices, and epic breakfast burritos. Covered in plants and good vibes.',
              meta: '💰 $ · 📍 Calle Delfín, Sayulita'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'San Pancho Art Walk & Beach',
              description: "Hop over to neighboring San Pancho (15 minutes north) for a totally different vibe. This small town has an artistic soul — galleries, organic cafés, and a wide, uncrowded beach backed by jungle. It's the chill counterbalance to Sayulita's energy.",
              details: [
                '🎨 Entreamigos community center often has art exhibitions',
                '🏖️ The beach is wide, golden, and blissfully uncrowded',
                '🐊 Jungle-lined creek at the south end has crocodiles (keep your distance!)'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Mary\'s Restaurant',
              description: 'Legendary Sayulita seafood spot. The fish tacos are the stuff of travel legend — perfectly battered, topped with pickled cabbage and creamy chipotle. Grab a cold Pacífico and savor it.',
              meta: '💰 $ · 📍 Calle Marlin, Sayulita · Cash only'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset Back in PV',
              description: "Head back to Puerto Vallarta in time for sunset. Hit the rooftop at La Santa for cocktails with panoramic bay views as the sun drops behind the Sierra Madre. The perfect golden hour spot.",
              details: [
                '🌅 La Santa rooftop opens at 5pm — get there early for the best seats',
                '🍹 Their mezcal margaritas are famous'
              ]
            }
          ],
          meals: [
            {
              type: '🌮 Dinner',
              name: 'Taquería El Cunao',
              description: 'The taco stand that locals obsess over. Carne asada and al pastor tacos that are simply perfect — paper plates, street-side seating, unforgettable flavor. Under $3 per person.',
              meta: '💰 $ · 📍 Centro, near the Malecón'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.8685, lng: -105.4410, label: 'Sayulita Beach', num: 1, cat: 'attraction', desc: 'Bohemian surf town with colorful streets and great waves' },
        { lat: 20.8700, lng: -105.4400, label: 'ChocoBanana', num: 2, cat: 'food', desc: 'Iconic Sayulita café — smoothie bowls and breakfast burritos' },
        { lat: 20.8680, lng: -105.4415, label: 'Mary\'s Restaurant', num: 3, cat: 'food', desc: 'Legendary fish tacos in Sayulita' },
        { lat: 20.9050, lng: -105.4550, label: 'San Pancho Beach', num: 4, cat: 'attraction', desc: 'Quiet, artsy beach town just north of Sayulita' },
        { lat: 20.6140, lng: -105.2360, label: 'La Santa Rooftop', num: 5, cat: 'food', desc: 'Rooftop mezcal cocktails with panoramic bay views' }
      ]
    },
    {
      num: 6,
      date: '2026-06-02',
      neighborhoods: 'Marina Vallarta · Nuevo Vallarta · Banderas Bay',
      title: 'Beach & Relaxation — Pool Day, Spa & Sunset Sail',
      description: "After days of adventure, today is all about unwinding. Sleep in, lounge by the pool or on a quiet beach, book a spa treatment, and cap it off with a sunset sailing cruise across Banderas Bay — drinks in hand, wind in your hair.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sleep In & Beach Club Morning',
              description: "You've earned a slow morning. Head to a beach club on the quieter north side of the bay — Playa Palmares or a day pass at a resort pool. Order fresh fruit, cold drinks, and just exist. No schedule, no rush.",
              details: [
                '🏖️ Beach clubs offer day passes ($20-40 USD) with pool, towels, and food service',
                '☀️ The morning sun hits the north-facing beaches perfectly',
                '📖 Bring a book or just nap under a palapa'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Spa & Temazcal Experience',
              description: "Try a traditional Mexican temazcal — a pre-Hispanic sweat lodge ritual led by a shaman. It's part spa, part spiritual experience. Alternatively, book a more conventional spa treatment — Thai massage and hot stone options are popular in PV.",
              details: [
                '🧖 Terra Noble spa in the hills offers temazcal with valley views',
                '💆 Budget option: massages on Playa de los Muertos from ~$30 USD/hour',
                '🌿 The temazcal ceremony takes about 2 hours — deeply relaxing'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Lázaro Cárdenas Taco Row',
              description: 'A strip of taco stands along Calle Lázaro Cárdenas — each one specializing in something different. Al pastor from one stand, birria from the next, seafood from another. Build your own taco crawl for under $5.',
              meta: '💰 $ · 📍 Calle Lázaro Cárdenas, near Insurgentes'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset Sailing Cruise',
              description: "Board a catamaran or sailboat for a sunset cruise across Banderas Bay. Watch the sun sink behind the mountains while sipping cocktails on deck. Many cruises include open bar, appetizers, and sometimes even whale-watching (seasonal).",
              details: [
                '⛵ Departures from Marina Vallarta around 5-6pm',
                '🍹 Most cruises include open bar and snacks (~$60-80 USD)',
                '🌅 The sunset over the bay from the water is absolutely magical',
                '🐋 Humpback whales are in the bay Dec-March (not this time, but dolphins are year-round)'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Tintoque',
              description: 'Chef Joel Ornelas\' modern Mexican tasting menu — one of the best fine dining experiences in PV. Inventive courses using local ingredients, beautiful plating, and a relaxed atmosphere.',
              meta: '💰 $$$ · 📍 Zona Romántica · Tasting menu ~$65 USD pp'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.6520, lng: -105.2530, label: 'Marina Vallarta', num: 1, cat: 'attraction', desc: 'Marina district — departure point for sailing cruises' },
        { lat: 20.6400, lng: -105.2350, label: 'Terra Noble Spa', num: 2, cat: 'attraction', desc: 'Hilltop spa with temazcal ceremonies and valley views' },
        { lat: 20.6065, lng: -105.2310, label: 'Lázaro Cárdenas Taco Row', num: 3, cat: 'food', desc: 'Strip of legendary taco stands — build your own crawl' },
        { lat: 20.6042, lng: -105.2298, label: 'Tintoque', num: 4, cat: 'food', desc: 'Modern Mexican tasting menu — PV\'s fine dining gem' }
      ]
    },
    {
      num: 7,
      date: '2026-06-03',
      neighborhoods: 'Conchas Chinas · Mismaloya · South Shore',
      title: 'Hidden Beaches, Mezcal & One Last Sunset',
      description: "Your final full day explores PV's quieter south shore — the secluded coves of Conchas Chinas, the movie-famous beach of Mismaloya, and a mezcal tasting to bring home the flavors of Mexico. End with a farewell dinner watching the sun melt into the Pacific.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Conchas Chinas & Mismaloya',
              description: "Head south along the coast to discover PV's hidden beaches. Conchas Chinas is a series of small, rocky coves with clear turquoise water — each one feels like your private beach. Continue to Mismaloya, where \"Night of the Iguana\" was filmed and the jungle meets the sea.",
              details: [
                '🏖️ Conchas Chinas has no facilities — bring water and snacks',
                '🎬 Mismaloya\'s "Night of the Iguana" set ruins are in the jungle above the beach',
                '🚕 Quick Uber ride south from Zona Romántica (~10 min)'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Mezcal Tasting Experience',
              description: "No trip to Mexico is complete without understanding mezcal. Visit a mezcal bar or tasting room to learn about the different agave varieties, production methods, and flavor profiles. PV has some excellent mezcalerías with knowledgeable staff.",
              details: [
                '🥃 La Mezcalera — intimate bar with 100+ mezcals and expert-guided tastings',
                '🌵 Learn the difference between espadín, tobalá, and cuishe agave',
                '🎓 Tastings usually include 4-5 pours with food pairings (~$25 USD)'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Joe Jack\'s Fish Shack',
              description: 'Funky, colorful seafood spot on Basilio Badillo. Famous for their fish & chips, shrimp burgers, and creative seafood tacos. Great cocktails and a fun, casual atmosphere.',
              meta: '💰 $$ · 📍 Basilio Badillo 212, Zona Romántica'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Farewell Sunset at Playa de los Muertos Pier',
              description: "Gather at the iconic Los Muertos Pier — the sail-shaped structure is PV's most recognizable landmark. Watch the sun set over Banderas Bay one last time, then walk along the beach to your farewell dinner.",
              details: [
                '🌅 The pier faces due west — perfect sunset alignment',
                '📸 The lit-up pier at dusk is spectacular',
                '🎸 Often live music and performers near the pier at sunset'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Hacienda San Angel',
              description: 'Stunning hilltop restaurant with panoramic views of the bay and the city lights below. Upscale Mexican cuisine, live music, and a magical atmosphere. The perfect farewell dinner — book a terrace table.',
              meta: '💰 $$$–$$$$ · 📍 Miramar 336, Centro · Reservations essential'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.5950, lng: -105.2420, label: 'Conchas Chinas', num: 1, cat: 'attraction', desc: 'Secluded rocky coves with turquoise water' },
        { lat: 20.5550, lng: -105.2830, label: 'Mismaloya Beach', num: 2, cat: 'attraction', desc: 'Movie-famous beach where jungle meets the sea' },
        { lat: 20.6060, lng: -105.2290, label: 'La Mezcalera', num: 3, cat: 'food', desc: 'Expert mezcal tastings with 100+ varieties' },
        { lat: 20.6050, lng: -105.2300, label: 'Joe Jack\'s Fish Shack', num: 4, cat: 'food', desc: 'Funky seafood spot on Basilio Badillo' },
        { lat: 20.6035, lng: -105.2330, label: 'Los Muertos Pier', num: 5, cat: 'attraction', desc: 'Iconic sail-shaped pier — PV\'s sunset landmark' },
        { lat: 20.6140, lng: -105.2380, label: 'Hacienda San Angel', num: 6, cat: 'food', desc: 'Hilltop fine dining with panoramic bay views' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$30–60/night', midrange: '$80–150/night', luxury: '$200–500/night' },
    { category: 'Meals (per person)', budget: '$10–20/day', midrange: '$25–50/day', luxury: '$60–120/day' },
    { category: 'Transport', budget: '$3–10/day', midrange: '$15–30/day', luxury: '$50–100/day (private)' },
    { category: 'Activities', budget: '$0–30/day', midrange: '$40–80/day', luxury: '$100–250/day' },
    { category: 'Sunset Cruise', budget: '$50–70pp', midrange: '$80–120pp', luxury: '$150–300pp' },
    { category: '7-Day Total (per person)', budget: '$400–700', midrange: '$800–1,500', luxury: '$2,000–4,500' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Gustavo Díaz Ordaz International Airport (PVR) has direct flights from most US cities', 'Airport is 15 minutes from the hotel zone, 25 minutes from Zona Romántica', 'Uber from airport is ~$8-12 USD (much cheaper than airport taxis)', 'ATM in the airport — withdraw pesos for better exchange rates than USD'] },
    { title: '🏨 Where to Stay', items: ['Zona Romántica — walkable, lively, best restaurant density (recommended)', 'Centro/Old Town — charming, affordable, near the Malecón', 'Marina Vallarta — quieter, resort-style, good for families', 'Airbnbs and hostels are plentiful and very affordable'] },
    { title: '🌡️ Weather', items: ['Late May/early June: 28-32°C (82-90°F), humidity rising', 'Start of rainy season — expect brief afternoon/evening showers', 'Mornings are typically sunny and perfect for activities', 'Ocean temperature is warm — 27-28°C (80-82°F)'] },
    { title: '💳 Money', items: ['Mexican peso (MXN) — $1 USD ≈ 17-18 pesos', 'Most restaurants accept cards, but carry cash for street food and markets', 'ATMs (cajeros) are everywhere — use bank ATMs to avoid fees', 'Tipping: 10-15% at restaurants, 50-100 pesos for tour guides'] },
    { title: '📱 Safety & Tips', items: ['PV is one of Mexico\'s safest tourist cities', 'Stick to well-traveled areas at night — Zona Romántica and Malecón are very safe', 'Drink bottled water (ice in restaurants is purified and safe)', 'Uber is safe, reliable, and very cheap throughout PV'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
