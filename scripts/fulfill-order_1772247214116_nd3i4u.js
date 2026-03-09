const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772247214116_nd3i4u',
  email: 'chadwick.chambers@gmail.com',
  destination: 'Luang Prabang, Laos',
  startDate: '2026-03-03',
  endDate: '2026-03-10',
  groupSize: 1,
  requests: 'Adventure, Cultural, Relaxation — Beautiful viewpoints and landscapes, exploring on my own, off the tourist track, kayaking and caves, creativity and art, history and legacy. Casual dining throughout.'
};

const itineraryData = {
  destination: 'Luang Prabang, Laos',
  countryEmoji: '🇱🇦',
  title: 'The Solo Explorer\'s Luang Prabang',
  subtitle: '7 days of karst viewpoints, river caves, hidden temples & quiet artisan villages',
  description: "Luang Prabang sits at the confluence of the Mekong and Nam Khan rivers, wrapped in mist-covered mountains and dotted with saffron-robed monks moving through dawn-lit streets. This UNESCO World Heritage town is one of Southeast Asia's most quietly magical places — but the real treasures lie beyond the tourist core. This itinerary is designed for a solo adventurer who wants to kayak through limestone gorges, explore caves filled with centuries of Buddha statues, wander off-trail to hilltop viewpoints, discover traditional weaving and paper-making villages, and feel the deep spiritual legacy of Laos at a pace that invites genuine connection.",
  duration: '7 nights',
  dates: 'Mar 3 – Mar 10, 2026',
  budget: '$$',
  pace: 'Moderate–Adventurous',
  bestFor: 'Solo Adventurers · Off-Track Explorers · Culture & Art Lovers',
  highlights: [
    'Sunrise alms-giving ceremony on the main street of Luang Prabang',
    'Kayaking the Nam Ou River through limestone karst valleys',
    'Pak Ou Caves — thousands of Buddha statues in riverside cliff grottoes',
    'Kuang Si Waterfall — turquoise cascades in the jungle',
    'Mount Phousi sunset — 360° panorama over rivers and mountains',
    'Ban Xang Khong — traditional Lao paper-making and silk-weaving village',
    'Nong Khiaw — dramatic viewpoint hikes and hidden caves off the tourist trail'
  ],

  essentials: [
    { title: '🌤️ March Weather', text: 'March is dry season — warm days (28–33°C), cool mornings (15–20°C), and virtually no rain. Perfect conditions for hiking, kayaking, and outdoor exploration. Evenings can be cool by the river — pack a light layer.' },
    { title: '💰 Money', text: 'Lao Kip (LAK). ATMs available in town but charge fees — withdraw larger amounts. Thai Baht and USD widely accepted. Budget ~$30–50/day for food, transport, and activities. Cash is king outside the town center.' },
    { title: '🛵 Getting Around', text: 'Luang Prabang is walkable and bikeable. Rent a bicycle (~30,000 LAK/day) for the Old Town. For day trips (Kuang Si, Pak Ou), hire a tuk-tuk or join a minivan. For Nong Khiaw, take the public minivan (3 hours, ~80,000 LAK). Slow boats on the Mekong are the classic Lao transport experience.' },
    { title: '🍜 Food Culture', text: 'Lao food is fresh, herbaceous, and built around sticky rice (khao niao) — eaten with your hands. Night markets and morning markets are the best places to eat. Try laap (spiced minced meat salad), tam mak hoong (spicy papaya salad), and or lam (a rich stew of herbs, eggplant, and buffalo). Beer Lao is excellent and everywhere.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-03',
      neighborhoods: 'Luang Prabang · Old Town Peninsula',
      title: 'Arrive at the Confluence — Rivers, Temples & First Light',
      description: 'Touch down in the jewel of northern Laos. Settle into the Old Town peninsula between the Mekong and Nam Khan rivers, climb Mount Phousi for your first panoramic sunset, and let the pace of this gentle town wash over you.',
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive & Settle In',
              description: 'Luang Prabang International Airport (LPQ) is 4km from town. A tuk-tuk or shared van will drop you in the heart of the Old Town within 15 minutes. Check into a guesthouse on the peninsula — the strip between the Mekong and the Nam Khan — and start exploring on foot.',
              details: [
                '🚕 Tuk-tuk from airport: ~50,000 LAK (~$2.50)',
                '🏨 Stay on the peninsula for walkable access to everything',
                '💡 Buy a Lao SIM at the airport (Unitel — ~$3 for 5GB)'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The Old Town peninsula is barely 1km long — you can walk end to end in 15 minutes. Everything important is within this strip: temples, the night market, the Royal Palace, and the Mekong riverfront cafés.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Mount Phousi Sunset',
              description: 'Climb the 328 steps up Mount Phousi — the sacred hill at the center of the Old Town — for a 360° sunset panorama over the Mekong, the Nam Khan, the mountains, and the golden temple rooftops below. This is the defining view of Luang Prabang.',
              details: [
                '⛰️ Entry: 20,000 LAK (~$1)',
                '🌅 Arrive by 5pm to secure a good spot — it gets popular at sunset',
                '📸 The view north over the Mekong bend is extraordinary',
                '🛕 Wat Chomsi sits at the summit — a small golden stupa'
              ]
            },
            {
              title: 'Night Market Stroll',
              description: 'After sunset, descend into the Luang Prabang Night Market — the entire main street (Sisavangvong Road) transforms into a vibrant market of handwoven textiles, mulberry paper, and Lao street food. Browse slowly, try the grilled skewers and fruit shakes.',
              details: [
                '🛍️ The night market runs every evening from ~5pm–10pm',
                '🧵 Look for handwoven Lao silk scarves — each pattern has cultural meaning',
                '🍢 Grilled meat skewers and coconut pancakes from the food stalls'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Night Market Food Stalls (Sisavangvong Road)',
              description: 'The food alley behind the textile market is the best casual dinner in town. For 15,000 LAK (~$0.75), fill a plate from the buffet tables — laap, sticky rice, grilled fish, papaya salad, and Mekong river weed (a crispy local delicacy).',
              meta: '💰 $ · 📍 Side street off Sisavangvong Road · Open nightly'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 19.8856, lng: 102.1350, label: 'Mount Phousi', num: 1, cat: 'attraction', desc: '328 steps to the best 360° panorama in Luang Prabang' },
        { lat: 19.8878, lng: 102.1340, label: 'Night Market', num: 2, cat: 'food', desc: 'Nightly textile and food market on the main street' },
        { lat: 19.8895, lng: 102.1355, label: 'Old Town Peninsula', num: 3, cat: 'attraction', desc: 'UNESCO World Heritage zone between two rivers' }
      ]
    },
    {
      num: 2,
      date: '2026-03-04',
      neighborhoods: 'Luang Prabang · Old Town · Mekong Riverside',
      title: 'Dawn Alms, Ancient Temples & the Royal Legacy',
      description: 'Wake before dawn for the sacred alms-giving ceremony, then spend the day exploring Luang Prabang\'s most important temples and the Royal Palace Museum — the spiritual and historical heart of the Lao kingdom.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Alms-Giving Ceremony (Tak Bat)',
              description: 'At 5:30am, hundreds of saffron-robed monks walk silently through the streets collecting rice from kneeling residents. This centuries-old Theravada Buddhist tradition is one of the most profound cultural experiences in Southeast Asia. Observe quietly from a respectful distance — this is not a photo opportunity, it\'s a living practice.',
              details: [
                '🙏 Observe from across the street — do not block the monks\' path',
                '📵 Flash photography is strictly discouraged — the monks are not performers',
                '🍚 If offering rice, buy from local vendors (not tour operators) and kneel quietly',
                '⏰ Starts ~5:30am — position yourself on Sakkaline Road by 5:15am'
              ]
            },
            {
              title: 'Wat Xieng Thong',
              description: 'The crown jewel of Luang Prabang\'s temples — a 16th-century masterpiece of Lao architecture with sweeping, layered roofs that nearly touch the ground. The rear wall features a stunning mosaic Tree of Life in coloured glass. The royal funeral chapel houses a gilded hearse shaped like a multi-headed serpent.',
              details: [
                '🛕 Entry: 20,000 LAK · Open 8am–5pm',
                '🎨 The Tree of Life mosaic on the rear wall is the most photographed artwork in Laos',
                '👑 The gilded funeral carriage chapel is extraordinary — don\'t miss it',
                '📍 Located at the tip of the peninsula where the rivers meet'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Joma Bakery Café',
              description: 'Popular café in a colonial building on the main street. Excellent coffee, fresh pastries, and Lao-style baguettes — a legacy of French colonial influence. A good base to warm up after the early morning alms ceremony.',
              meta: '💰 $ · 📍 Sisavangvong Road, Old Town'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Royal Palace Museum (Haw Kham)',
              description: 'The former residence of the Lao royal family, now a museum housing the Phra Bang — the sacred gold Buddha image that gives the city its name. The throne room, royal bedchambers, and the reception hall with murals by French-trained Lao artist Alix de Fautereau are fascinating.',
              details: [
                '🏛️ Entry: 30,000 LAK · Open 8am–11:30am, 1:30pm–4pm · Closed Tuesdays',
                '👗 Dress modestly — no shorts or tank tops',
                '📵 No photography inside the museum',
                '🌺 The palace gardens are beautiful and free to walk through'
              ]
            },
            {
              title: 'Wat Visounnarath & That Makmo',
              description: 'The oldest operating temple in Luang Prabang (1513), housing a collection of ancient wooden Buddha images. Next to it stands That Makmo — the "watermelon stupa" — a rounded dome shape unique in Lao Buddhist architecture.',
              details: [
                '🛕 Entry: 20,000 LAK',
                '📸 The wooden Buddhas inside are carved in styles spanning centuries',
                '🍉 That Makmo\'s rounded shape is unique — it looks nothing like a typical stupa'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Mekong Riverside Sunset',
              description: 'Walk down to the Mekong riverbank below the Old Town. Find a spot on the bamboo platforms that jut out over the water and watch the sun set behind the mountains across the river. The light on the Mekong at golden hour is liquid gold.',
              details: [
                '🌅 The bamboo platforms below the Royal Palace are the best spots',
                '🍺 Beer Lao on the riverbank: ~15,000 LAK (~$0.75)',
                '📸 The Mekong glows copper and gold in March — extraordinary light'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Tamarind Restaurant',
              description: 'The best Lao restaurant in town — specializing in traditional dishes with explanations for each. Try the tasting platter: laap, or lam, stuffed lemongrass, Mekong river weed, and jeow bong (spicy chili paste with buffalo skin). Everything served with sticky rice.',
              meta: '💰 $$ · 📍 Ban Wat Sene, near Nam Khan bridge · Book ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 19.8910, lng: 102.1370, label: 'Wat Xieng Thong', num: 1, cat: 'attraction', desc: '16th-century masterpiece — Tree of Life mosaic and royal chapel' },
        { lat: 19.8880, lng: 102.1335, label: 'Royal Palace Museum', num: 2, cat: 'attraction', desc: 'Former royal residence housing the sacred Phra Bang Buddha' },
        { lat: 19.8840, lng: 102.1310, label: 'Wat Visounnarath', num: 3, cat: 'attraction', desc: 'Oldest operating temple (1513) with ancient wooden Buddhas' },
        { lat: 19.8870, lng: 102.1320, label: 'Tamarind Restaurant', num: 4, cat: 'food', desc: 'Best traditional Lao cuisine in Luang Prabang' },
        { lat: 19.8875, lng: 102.1345, label: 'Mekong Riverbank', num: 5, cat: 'attraction', desc: 'Bamboo platforms for golden-hour river watching' }
      ]
    },
    {
      num: 3,
      date: '2026-03-05',
      neighborhoods: 'Kuang Si · Ban Na Ouane · Jungle Trails',
      title: 'Kuang Si Falls — Turquoise Cascades & Bear Rescue',
      description: 'A full day at Kuang Si — Luang Prabang\'s most spectacular natural attraction. Hike the jungle trails above the falls for a viewpoint most tourists never reach, visit the Asiatic black bear rescue center, and swim in turquoise pools under the canopy.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive to Kuang Si Waterfall',
              description: 'Hire a tuk-tuk or motorbike for the 30km journey south through rural Lao villages and rice paddies. Arrive early (before 9am) to have the falls nearly to yourself — the tour groups arrive around 10am.',
              details: [
                '🛵 Rent a motorbike (~100,000 LAK/day) or tuk-tuk (~200,000 LAK return with wait)',
                '⏰ Leave by 8am to beat the crowds — the road is scenic and easy',
                '💰 Entry: 20,000 LAK',
                '🐻 Stop at the Tat Kuang Si Bear Rescue Centre at the entrance — free with park entry'
              ]
            },
            {
              title: 'Bear Rescue Centre',
              description: 'At the park entrance, the Free the Bears rescue center houses Asiatic black bears saved from illegal wildlife trade and traditional medicine. Watch them play in their forested enclosures from elevated walkways — a moving introduction to Lao conservation efforts.',
              details: [
                '🐻 The bears are most active in the morning — feeding time is before 10am',
                '🌿 The enclosures are spacious and forested — well-run facility',
                '💛 Free the Bears is an Australian-Lao nonprofit — donations appreciated'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Swim in the Turquoise Pools',
              description: 'The mineral-rich water creates a series of turquoise-blue pools cascading down the hillside, surrounded by jungle. The lower pools are perfect for swimming — cool, clear, and otherworldly in colour. Change into swimwear and spend an hour floating beneath the canopy.',
              details: [
                '🏊 The lower pools are swimmable — rope swings hang from trees overhead',
                '💧 The turquoise colour comes from dissolved limestone minerals',
                '📸 The main cascade is 60m tall — spectacular from the viewing platform'
              ]
            },
            {
              title: 'Hike to the Upper Falls Viewpoint',
              description: 'Most visitors stay at the lower pools. Take the trail that climbs steeply behind and above the main cascade — a 30-minute jungle hike that leads to the top of the waterfall and a hidden viewpoint looking down over the entire falls system. You\'ll likely be alone up here.',
              details: [
                '🥾 The trail is steep but manageable — wear shoes with grip',
                '📸 The view from above the falls is dramatically different from below',
                '🌿 The upper trail continues through dense jungle — excellent for birdwatching',
                '⚠️ The rocks near the top can be slippery — take care'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Picnic at Kuang Si',
              description: 'Pack sticky rice, grilled chicken, and papaya salad from the Luang Prabang morning market before you leave. Eat on the rocks beside the turquoise pools — the best picnic spot in Laos.',
              meta: '💰 $ · 📍 Pack from Phousi Market before departing'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return via Ban Na Ouane Village',
              description: 'On the drive back, stop at Ban Na Ouane — a small Khmu ethnic village along the road. The Khmu are one of Laos\' oldest indigenous groups. Walk through the village to see traditional bamboo houses, rice granaries, and community life that has changed very little in centuries.',
              details: [
                '🏡 The village is small — a 20-minute walk through is respectful and welcomed',
                '🎋 Bamboo is the primary building material — beautiful stilted houses',
                '🍚 If invited to share rice, accepting is a gesture of goodwill'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Dyen Sabai Restaurant',
              description: 'Cross the Nam Khan river on a bamboo footbridge to reach this open-air restaurant built into the riverbank. Cushions on bamboo platforms over the water, Lao cuisine, and the sound of the river below. A truly magical setting for solo dining.',
              meta: '💰 $$ · 📍 Across the bamboo bridge over the Nam Khan · Cash only'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 19.7483, lng: 101.9936, label: 'Kuang Si Waterfall', num: 1, cat: 'attraction', desc: '60m turquoise cascade with swimmable pools and jungle trails' },
        { lat: 19.7485, lng: 101.9940, label: 'Bear Rescue Centre', num: 2, cat: 'attraction', desc: 'Asiatic black bear sanctuary at the falls entrance' },
        { lat: 19.8200, lng: 102.0500, label: 'Ban Na Ouane', num: 3, cat: 'attraction', desc: 'Traditional Khmu ethnic village on the Kuang Si road' },
        { lat: 19.8890, lng: 102.1400, label: 'Dyen Sabai', num: 4, cat: 'food', desc: 'Bamboo-platform restaurant over the Nam Khan river' }
      ]
    },
    {
      num: 4,
      date: '2026-03-06',
      neighborhoods: 'Pak Ou · Mekong River · Ban Xang Hai',
      title: 'Mekong Journey — Pak Ou Caves & Whiskey Village',
      description: 'Boat up the Mekong to the Pak Ou Caves — cliff grottoes stuffed with thousands of Buddha statues accumulated over centuries. Stop at Ban Xang Hai village for local rice whiskey and weaving, then drift back downstream as the sun turns the river to bronze.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Slow Boat Up the Mekong',
              description: 'Board a traditional wooden slow boat at the Luang Prabang pier for the 2-hour journey upstream to Pak Ou. The trip itself is the experience — drifting past limestone karsts, bamboo-fringed banks, riverside villages, and fishermen casting nets. The Mekong is wide, brown, and deeply peaceful.',
              details: [
                '⛵ Hire a private boat (~250,000 LAK) or join a shared tour (~100,000 LAK/person)',
                '⏰ Depart around 8:30am from the pier below the Royal Palace',
                '📸 The karst cliffs along the Mekong between Luang Prabang and Pak Ou are spectacular',
                '☕ Bring coffee and snacks for the ride — there\'s nothing but river and sky'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Pak Ou Caves (Tham Ting & Tham Phum)',
              description: 'At the confluence of the Mekong and Nam Ou rivers, two caves in a limestone cliff face house thousands of Buddha statues — accumulated over centuries by pilgrims and locals. Tham Ting (the lower cave) is open and airy, with hundreds of Buddhas of every size silhouetted against the river light. Tham Phum (the upper cave) is darker, deeper, and more atmospheric.',
              details: [
                '🛕 Entry: 20,000 LAK',
                '🔦 Bring a flashlight for Tham Phum (upper cave) — it goes deep and dark',
                '🙏 The statues range from tiny palm-sized to life-sized — extraordinary accumulation',
                '📸 The view from the cave mouth over the river confluence is stunning'
              ]
            },
            {
              title: 'Ban Xang Hai — Whiskey Village',
              description: 'On the return downstream, stop at Ban Xang Hai — known as "Whiskey Village" for its production of lao-lao, the local rice whiskey. Watch the distillation process, sample whiskeys infused with scorpions, snakes, and herbs, and browse handwoven textiles.',
              details: [
                '🥃 Lao-lao tastings are free — bottles from 20,000 LAK',
                '🐍 The snake and scorpion whiskeys are more tourist spectacle than local tradition — try the plain lao-lao',
                '🧵 The village also produces beautiful handwoven scarves'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Riverside Lunch at Ban Xang Hai',
              description: 'Simple Lao lunch at one of the village\'s riverside restaurants — grilled fish from the Mekong, sticky rice, and fresh herbs. Eating beside the river with the karsts rising behind you.',
              meta: '💰 $ · 📍 Ban Xang Hai village restaurants'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Drift Back to Luang Prabang',
              description: 'The return downstream is faster (1 hour with the current). Watch the light change on the river as afternoon deepens into golden hour. Arrive back at the Luang Prabang pier with the town glowing in late light.',
              details: [
                '🌅 The downstream return catches beautiful late afternoon light on the karsts',
                '📸 The approach back to Luang Prabang from the river is one of the great arrivals'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'L\'Éléphant Restaurant',
              description: 'French-Lao fine dining in a restored colonial villa. The tasting menu blends Gallic technique with Lao ingredients — Mekong fish in banana leaf, buffalo tartare, and frangipane desserts. A legacy of French Indochina, refined and romantic.',
              meta: '💰 $$$ · 📍 Ban Wat Nong, Luang Prabang'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.0531, lng: 102.2175, label: 'Pak Ou Caves', num: 1, cat: 'attraction', desc: 'Cliff grottoes with thousands of Buddha statues at the river confluence' },
        { lat: 19.9500, lng: 102.1700, label: 'Ban Xang Hai', num: 2, cat: 'attraction', desc: 'Whiskey Village — lao-lao distillation and handwoven textiles' },
        { lat: 19.8885, lng: 102.1330, label: 'Luang Prabang Pier', num: 3, cat: 'attraction', desc: 'Departure point for Mekong slow boat journeys' },
        { lat: 19.8865, lng: 102.1315, label: 'L\'Éléphant Restaurant', num: 4, cat: 'food', desc: 'French-Lao colonial fine dining' }
      ]
    },
    {
      num: 5,
      date: '2026-03-07',
      neighborhoods: 'Ban Xang Khong · Ban Xieng Lek · Countryside',
      title: 'Art, Craft & Hidden Temples — The Creative Side of Luang Prabang',
      description: 'Explore the artisan villages on the outskirts of town — traditional mulberry paper-making, silk weaving, and temple murals that few tourists ever see. This is the creative, quiet Luang Prabang that rewards those who wander off the main street.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Ban Xang Khong — Paper & Weaving Village',
              description: 'Cycle 4km east along the Mekong to Ban Xang Khong — a village famous for handmade sa (mulberry bark) paper and traditional Lao silk weaving. Watch artisans pound bark into pulp, press sheets embedded with flowers and leaves, and weave intricate patterns on wooden looms. This is living heritage.',
              details: [
                '🚲 Easy 15-minute bicycle ride along the river road from the Old Town',
                '📜 Sa paper workshops welcome visitors — free to watch, products available to buy',
                '🧵 The silk weaving is done on traditional floor looms — patterns are passed down through generations',
                '🎨 Some workshops create paper with embedded flower petals — beautiful as artwork or lampshades'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Le Banneton Café',
              description: 'French-style bakery with outstanding croissants, pain au chocolat, and Vietnamese-style coffee. The French colonial influence is still alive in Luang Prabang\'s morning pastry culture.',
              meta: '💰 $ · 📍 Sakkaline Road, Old Town'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Hidden Temples Walk — West Bank of the Mekong',
              description: 'Cross the Mekong by the local ferry to the west bank — the "other side" that almost no tourists visit. Walk south along the river through small villages and discover a string of quiet temples (Wat Long Khoun, Wat Tham Xieng Maen) and overgrown shrines in the forest. The old royal retreat Wat Long Khoun has faded murals and a meditation cave.',
              details: [
                '⛴️ Local ferry across the Mekong: 10,000 LAK per crossing',
                '🛕 Wat Long Khoun — former royal meditation retreat, crumbling and atmospheric',
                '🕳️ Tham Xieng Maen — a cave temple with Buddha statues, rarely visited',
                '🌿 The walk is about 3km along a dirt path — peaceful and shaded'
              ]
            },
            {
              title: 'Traditional Arts & Ethnology Centre (TAEC)',
              description: 'Back in town, visit this small but exceptional museum dedicated to the ethnic minorities of Laos — Hmong, Khmu, Akha, and Tai Dam. Displays of traditional clothing, tools, spiritual objects, and photography explain the incredible diversity of cultures within this small country.',
              details: [
                '🏛️ Entry: 25,000 LAK · Open 9am–6pm · Closed Mondays',
                '📚 The textile collection is outstanding — each pattern tells a story',
                '🎨 The museum shop sells fair-trade crafts directly supporting artisan communities'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Phousi Market Morning Goods at Dusk',
              description: 'The Phousi Market (main day market) winds down in the late afternoon but the surrounding streets come alive with local food vendors — grilled Mekong fish, khao piak sen (Lao chicken noodle soup), and fresh fruit smoothies. This is where locals eat, not tourists.',
              details: [
                '🍲 Khao piak sen (hand-rolled rice noodle soup) is pure comfort food',
                '🐟 Grilled Mekong fish wrapped in banana leaves: ~30,000 LAK',
                '📍 The market is near the bus station — away from the tourist strip'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Khaiphaen Restaurant',
              description: 'Social enterprise restaurant training former street youth in hospitality. Named after Mekong river weed (khaiphaen), the menu highlights traditional Lao dishes with a modern twist. Excellent laap, stuffed lemongrass, and creative cocktails using local herbs.',
              meta: '💰 $$ · 📍 100m from the Night Market, Sisavangvong Road'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 19.8980, lng: 102.1530, label: 'Ban Xang Khong', num: 1, cat: 'attraction', desc: 'Traditional mulberry paper-making and silk weaving village' },
        { lat: 19.8850, lng: 102.1250, label: 'Wat Long Khoun', num: 2, cat: 'attraction', desc: 'Crumbling royal meditation retreat on the Mekong\'s west bank' },
        { lat: 19.8840, lng: 102.1230, label: 'Tham Xieng Maen', num: 3, cat: 'attraction', desc: 'Cave temple with Buddha statues — rarely visited' },
        { lat: 19.8870, lng: 102.1355, label: 'TAEC Museum', num: 4, cat: 'attraction', desc: 'Ethnic minority arts and culture museum' },
        { lat: 19.8875, lng: 102.1340, label: 'Khaiphaen Restaurant', num: 5, cat: 'food', desc: 'Social enterprise Lao restaurant — creative traditional food' }
      ]
    },
    {
      num: 6,
      date: '2026-03-08',
      neighborhoods: 'Nong Khiaw · Nam Ou River Valley',
      title: 'Nong Khiaw — Karst Peaks, Hidden Caves & River Kayaking',
      description: 'Leave the tourist trail behind entirely. Travel 3 hours north to Nong Khiaw — a tiny riverside town surrounded by some of the most dramatic limestone karst scenery in Southeast Asia. Hike to a viewpoint, explore wartime caves, and kayak the Nam Ou River.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive to Nong Khiaw',
              description: 'Take the public minivan from Luang Prabang\'s northern bus station (3 hours, ~80,000 LAK) through winding mountain roads. The drive itself is an adventure — green valleys, stilted villages, and mist-wrapped peaks. Nong Khiaw appears suddenly, a cluster of wooden buildings at the base of sheer limestone walls on the Nam Ou River.',
              details: [
                '🚌 Minivan departs ~9am from the northern bus station — buy tickets day before',
                '🏔️ The scenery on the drive gets progressively more dramatic',
                '🏨 Book a riverside guesthouse in Nong Khiaw — Nong Kiau Riverside or Mandala Ou',
                '💰 Accommodation: $10–25/night for riverside bungalows'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Pha Daeng Viewpoint Hike',
              description: 'The Pha Daeng (or "Viewpoint 1") hike is a steep 1-hour climb through forest to a jaw-dropping panorama over the Nam Ou River valley, the bridge, and the surrounding karst peaks. This is one of the most spectacular viewpoints in all of Laos — and on a weekday, you might be alone at the top.',
              details: [
                '🥾 Trailhead is just across the bridge — entry 20,000 LAK',
                '⏱️ Allow 1 hour up, 45 minutes down — steep but well-marked',
                '📸 The view over the river bending through the karsts is extraordinary',
                '💧 Bring water — there\'s no shade on the final approach'
              ]
            },
            {
              title: 'Pha Kuang Cave (Tham Pha Kuang)',
              description: 'A short walk from Nong Khiaw leads to Pha Kuang Cave — a massive cavern used by villagers as shelter during the Vietnam War-era bombings. The cave is enormous, with stalactites and war-era artifacts still visible. Barely visited, deeply atmospheric.',
              details: [
                '🔦 Bring a headlamp — the cave goes deep and has no lighting',
                '💰 Entry: 10,000 LAK · Guide available at the trailhead for 50,000 LAK',
                '🕳️ The cave is large enough that hundreds of people sheltered here during the Secret War',
                '📍 20-minute walk from town — follow signs from the bridge'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Coco Home Bar & Restaurant',
              description: 'Laid-back riverside restaurant with wooden decks over the Nam Ou. Excellent fried rice, Lao salads, and fruit shakes with views of the karst mountains directly behind the kitchen.',
              meta: '💰 $ · 📍 Nong Khiaw riverside'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset from the Nong Khiaw Bridge',
              description: 'The bridge spanning the Nam Ou is the perfect sunset viewpoint — the light hits the limestone cliffs and turns them gold and pink while the river mirrors everything below. Stand on the bridge as the town goes quiet and the bats emerge.',
              details: [
                '🌅 Sunset around 6pm in March — position on the bridge by 5:30pm',
                '🦇 Bats emerge from the caves at dusk — watch them stream across the sky',
                '📸 The bridge view with karsts on both sides is uniquely dramatic'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Delilah\'s Place',
              description: 'Backpacker-friendly but excellent — this riverside spot serves the best food in Nong Khiaw. Try the Lao-style grilled fish and the buffalo laap. The atmosphere is relaxed and the owners are a wealth of local trail information.',
              meta: '💰 $ · 📍 Nong Khiaw main road, riverside'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.5720, lng: 102.6110, label: 'Nong Khiaw', num: 1, cat: 'attraction', desc: 'Tiny riverside town beneath dramatic limestone karsts' },
        { lat: 20.5740, lng: 102.6130, label: 'Pha Daeng Viewpoint', num: 2, cat: 'attraction', desc: 'Jaw-dropping panorama over the Nam Ou valley — 1-hour hike' },
        { lat: 20.5700, lng: 102.6080, label: 'Pha Kuang Cave', num: 3, cat: 'attraction', desc: 'Massive wartime shelter cave with stalactites' },
        { lat: 20.5725, lng: 102.6115, label: 'Nong Khiaw Bridge', num: 4, cat: 'attraction', desc: 'Sunset viewpoint over the Nam Ou and karst peaks' },
        { lat: 20.5718, lng: 102.6105, label: 'Delilah\'s Place', num: 5, cat: 'food', desc: 'Best food in Nong Khiaw — riverside grilled fish and laap' }
      ]
    },
    {
      num: 7,
      date: '2026-03-09',
      neighborhoods: 'Nong Khiaw · Nam Ou River · Return to Luang Prabang',
      title: 'Kayak the Nam Ou & Return to Luang Prabang',
      description: 'Your most adventurous day — kayak downstream on the Nam Ou River through limestone gorges, past riverside villages, and into the Mekong current. Then return to Luang Prabang for a final evening of temple-lit streets and river reflections.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kayak the Nam Ou River',
              description: 'Arrange a half-day kayaking trip from Nong Khiaw downstream on the Nam Ou. Paddle through a landscape of towering karst cliffs, past fishing villages, and through gentle rapids. The river is calm in March (dry season) and the scenery is like paddling through a Chinese ink painting.',
              details: [
                '🛶 Book through Tiger Trail or Green Discovery in Nong Khiaw (~$25–40/person)',
                '⏱️ Half-day trip: ~3–4 hours on the water',
                '🏔️ The karst scenery from water level is completely different from above — immersive',
                '🐟 Fishermen cast nets from bamboo rafts along the river — beautiful to watch',
                '💧 The river is gentle in March — suitable for beginners'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Sunrise at Nong Khiaw',
              description: 'Wake early for one of the most spectacular sunrises in Laos — mist rising off the Nam Ou, the karst cliffs emerging from the fog. Grab coffee and khao jee (Lao baguette with condensed milk) from a street vendor.',
              meta: '💰 $ · 📍 Any riverside vendor, Nong Khiaw'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Return to Luang Prabang',
              description: 'Take the afternoon minivan back to Luang Prabang (3 hours). Arrive in the late afternoon with time for a final temple visit or a quiet Mekong-side coffee.',
              details: [
                '🚌 Minivans depart Nong Khiaw around 1pm — buy ticket in the morning',
                '⏱️ Arrive Luang Prabang ~4pm',
                '🌅 Time for one last Mount Phousi sunset if you want a bookend to day 1'
              ]
            },
            {
              title: 'Wat Sibounheuang — A Quiet Temple',
              description: 'Skip the famous temples and find Wat Sibounheuang — a small, beautifully maintained temple on a quiet side street that most tourists walk past. The monks here are friendly and often happy to chat in the late afternoon. The murals inside are exquisite.',
              details: [
                '🛕 Free entry — on a side street between Sakkaline and the Mekong',
                '🙏 If a monk invites you to sit, accept — temple conversations are a privilege in Laos',
                '🎨 The interior murals depict Jataka tales — stories of the Buddha\'s past lives'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Evening — Bamboo Bridge & Nam Khan',
              description: 'Walk across the seasonal bamboo bridge spanning the Nam Khan river (rebuilt each dry season by hand). On the far side, find a quiet spot on the riverbank and watch Luang Prabang\'s temple spires and Mount Phousi glow in the last light. This is the image that stays.',
              details: [
                '🌉 Bamboo bridge toll: 10,000 LAK — it sways gently as you walk',
                '🌅 The view back toward Mount Phousi from across the Nam Khan is the classic farewell image',
                '📸 The bridge is rebuilt each October after the monsoon destroys it — a beautiful impermanence'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Manda de Laos',
              description: 'Set in a garden with restored colonial-era fish ponds and lotus flowers, Manda de Laos serves refined Lao cuisine in one of the most beautiful settings in town. Grilled Mekong fish in banana leaf, or lam stew, and coconut sticky rice dessert. A perfect farewell meal.',
              meta: '💰 $$$ · 📍 Phouvao Road, south of the Old Town · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.5720, lng: 102.6110, label: 'Nam Ou Kayak Start', num: 1, cat: 'attraction', desc: 'Half-day kayak through karst gorges on the Nam Ou' },
        { lat: 19.8860, lng: 102.1325, label: 'Wat Sibounheuang', num: 2, cat: 'attraction', desc: 'Quiet temple with exquisite murals — hidden in plain sight' },
        { lat: 19.8870, lng: 102.1380, label: 'Bamboo Bridge', num: 3, cat: 'attraction', desc: 'Seasonal handmade bridge over the Nam Khan — rebuilt each year' },
        { lat: 19.8830, lng: 102.1310, label: 'Manda de Laos', num: 4, cat: 'food', desc: 'Refined Lao dining in lotus-pond gardens' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$8–15/night', midrange: '$25–60/night', luxury: '$80–200/night' },
    { category: 'Meals', budget: '$5–10/day', midrange: '$15–30/day', luxury: '$40–80/day' },
    { category: 'Activities & Tours', budget: '$5–15/day', midrange: '$20–50/day', luxury: '$60–120/day' },
    { category: 'Transport (local)', budget: '$3–8/day', midrange: '$10–25/day', luxury: '$30–60/day' },
    { category: '7-Day Total (solo)', budget: '$200–400', midrange: '$500–1,200', luxury: '$1,500–3,500' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Luang Prabang International Airport (LPQ) — direct flights from Bangkok (BKK/DMK), Hanoi, Vientiane, Chiang Mai, and Siem Reap', 'Bangkok to Luang Prabang is 2 hours (Bangkok Airways, Lao Airlines, AirAsia)', 'Alternatively, the slow boat from Huay Xai (Thai border) takes 2 days down the Mekong — one of SE Asia\'s great journeys'] },
    { title: '📋 Visa', items: ['Most nationalities get visa on arrival at the airport ($30–42 USD depending on nationality)', 'Bring 2 passport photos and USD cash for the visa fee', 'E-visa available in advance at laoevisa.gov.la — saves queuing'] },
    { title: '🏨 Where to Stay', items: ['Old Town peninsula for walkable access to everything — guesthouses from $10/night', 'Sayo River Guest House — quiet, riverside, excellent value ($15–25)', 'Sofitel Luang Prabang — if you want luxury in a UNESCO setting ($200+)', 'Nong Khiaw: Nong Kiau Riverside Bungalows — karst views from your balcony ($15–30)'] },
    { title: '🌡️ March Weather', items: ['Dry season — virtually no rain, warm days (28–33°C), cool mornings (15–20°C)', 'The driest, sunniest month — perfect for outdoor adventures', 'Rivers are lower in March — excellent for kayaking with exposed sandbars and clear water', 'Evenings by the river can be cool — bring a light jacket'] },
    { title: '🛡️ Solo Travel Safety', items: ['Laos is one of the safest countries in SE Asia for solo travelers', 'Luang Prabang feels remarkably safe even at night — locals are genuinely friendly', 'Petty theft is rare but use common sense with valuables', 'The biggest risk is motorbike accidents — wear a helmet and drive slowly on mountain roads'] },
    { title: '🌐 Connectivity', items: ['Buy a Unitel SIM at the airport (~$3 for 5GB) — good coverage in Luang Prabang', 'WiFi available in most cafés and guesthouses in town', 'Nong Khiaw has patchy signal — embrace the disconnection'] }
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
