const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771710280734_1e13y5',
  email: 'bernard.j.huang@gmail.com',
  destination: 'Kingdom of Tonga',
  startDate: '2026-06-02',
  endDate: '2026-06-07',
  groupSize: 1,
  requests: ''
};

const itineraryData = {
  destination: 'Tongatapu, Kingdom of Tonga',
  countryEmoji: '🇹🇴',
  title: 'Where the Sun Rises First — Tonga Solo',
  subtitle: '6 days on Tongatapu: humpback whales, blowholes, ancient ruins, and the warmth of the Pacific',
  description: "Tonga is the last Polynesian kingdom — a place where Sunday church hymns shake the walls, kava circles run past midnight, and humpback whales arrive each June to birth their calves in warm turquoise waters. Tongatapu, the main island, is flat, coral-fringed, and deeply cultural. In early June you'll catch the very start of whale season, snorkel pristine reefs off uninhabited islands, stand at a 1,200-year-old stone trilithon that rivals Stonehenge, and eat some of the most honest, generous food in the Pacific — roasted suckling pig, raw fish in coconut cream, and cassava chips from a roadside stand. This isn't resort tourism. This is the real Pacific, at a pace that makes you wonder why you ever rushed anywhere.",
  duration: '5 nights',
  dates: 'Jun 2 – Jun 7, 2026',
  budget: '$',
  pace: 'Relaxed',
  bestFor: 'Solo Travelers',
  highlights: [
    'Swimming with humpback whales — early June marks the start of migration season',
    'Mapu\'a \'a Vaea Blowholes — hundreds of ocean geysers erupting through coral rock',
    'Ha\'amonga \'a Maui Trilithon — Tonga\'s 1,200-year-old "Stonehenge of the Pacific"',
    'Snorkeling the pristine reef off \'Atata Island — a short boat ride from Nuku\'alofa',
    'Sunday church service with full Tongan choir harmonies that will move you to tears',
    'Talamahu Market — tapa cloth, woven baskets, tropical fruit, and Tongan street food'
  ],

  essentials: [
    { title: '🌤️ June Weather', text: 'Early June is dry season in Tonga — expect pleasant 24°C days, cooler 18°C nights, and minimal rain. Water temperature is around 25°C, perfect for snorkeling and whale swimming. Pack light layers for evenings, reef shoes, and strong sunscreen.' },
    { title: '✈️ Getting There', text: 'Fly into Fua\'amotu International Airport (TBU) on Tongatapu. Fiji Airways connects via Nadi (2hr flight), Air New Zealand via Auckland. From the airport, taxis to Nuku\'alofa cost about TOP $30–40 (~$13–17 USD). Book flights early — limited frequency.' },
    { title: '💰 Budget Tips', text: 'Tonga is affordable for the Pacific. Guesthouses run $30–60 USD/night, local meals $5–10. The Tongan Pa\'anga (TOP) trades at roughly 2.3:1 USD. ATMs exist in Nuku\'alofa but carry cash — cards aren\'t widely accepted outside town. Budget $100–150/day all-in.' },
    { title: '🐋 Whale Season', text: 'Humpback whales migrate to Tonga from June through October. Early June is the very beginning — fewer boats, smaller crowds, but sightings are possible. Tongatapu operators run half-day trips ($150–200 USD). Vava\'u to the north is the whale capital, but Tongatapu works for a taste.' },
    { title: '🙏 Sunday Culture', text: 'Tonga shuts down on Sunday — almost everything is closed. This is deeply cultural, not inconvenient. Attend a church service (visitors are warmly welcome), then enjoy a traditional Sunday feast (\'umu) if your guesthouse offers one. Plan accordingly: buy supplies Saturday.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-06-02',
      neighborhoods: 'Nuku\'alofa City Centre · Waterfront',
      title: 'Arrival in the Last Kingdom',
      description: "Land at Fua'amotu Airport and feel the warm Pacific air hit you as you step off the plane. Tonga moves at its own pace — settle into Nuku'alofa, the tiny capital, explore the waterfront, visit the Royal Palace grounds, and get your bearings at Talamahu Market before a sunset walk along Vuna Road.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Royal Palace & Waterfront Stroll',
              description: "The Royal Palace is a white Victorian-era wooden building surrounded by Norfolk pines, sitting right on the waterfront. You can't enter, but the grounds and the view across the harbour are beautiful. Walk along Vuna Road past the old Treasury Building and small boat harbour.",
              details: [
                '🏛️ Royal Palace is viewable from outside only — respect the fence line',
                '📸 Best photos from the waterfront road looking back at the palace with palms',
                '🌅 Late afternoon light is gorgeous along the harbour'
              ]
            },
            {
              title: 'Talamahu Market',
              description: "Nuku'alofa's central market is a feast for the senses — piles of taro, yams, breadfruit, coconuts, and tropical fruit alongside handmade tapa cloth, woven pandanus baskets, and Tongan crafts. Saturday is the biggest day, but weekday afternoons still buzz with vendors.",
              details: [
                '🛒 Open Mon–Sat, busiest mornings and Saturdays',
                '🥥 Try fresh coconut water — vendors crack them open for TOP $2',
                '🎨 Tapa cloth paintings make incredible souvenirs — $10–30 for small pieces',
                '📍 Salote Road, central Nuku\'alofa — impossible to miss'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Coffee & Lunch',
              name: 'Friends Cafe',
              description: 'The most popular cafe in Nuku\'alofa. Fresh juices, excellent coffee, fish tacos, and big salads. Great Wi-Fi and a welcoming vibe for solo travelers. A perfect landing spot.',
              meta: '💰 $ · 📍 Taufa\'ahau Road, Nuku\'alofa centre'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Vuna Road Sunset Walk',
              description: "Stroll the waterfront road as the sun sets over the harbour. Local families gather, kids play rugby on the grass, and the pace of life is exactly what you came for. This is Tonga at its most authentic — no tourists, no rush, just warm evening light and the sound of the sea.",
              details: [
                '🌅 Sunset around 5:30pm in June — golden light over the water',
                '🏉 You\'ll see impromptu rugby games everywhere — Tonga\'s national obsession'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Waterfront Restaurant & Lodge',
              description: 'The best sit-down restaurant in Nuku\'alofa. Fresh grilled fish, coconut curry, and cold Ikale beer on a verandah overlooking the water. Carved Tongan pillars give it local character.',
              meta: '💰 $$ · 📍 Vuna Road, Nuku\'alofa waterfront'
            }
          ],
          tips: [
            { type: 'tip', text: 'Exchange money at the BSP or TDB bank in Nuku\'alofa — better rates than the airport. Withdraw cash from ATMs here; cards are unreliable elsewhere on the island.' }
          ]
        }
      ],
      mapPins: [
        { lat: -21.1333, lng: -175.2000, label: 'Royal Palace', num: 1, cat: 'attraction', desc: 'Victorian-era royal residence on the Nuku\'alofa waterfront' },
        { lat: -21.1360, lng: -175.1985, label: 'Talamahu Market', num: 2, cat: 'attraction', desc: 'Central market — tapa cloth, produce, and Tongan crafts' },
        { lat: -21.1345, lng: -175.2010, label: 'Friends Cafe', num: 3, cat: 'food', desc: 'Best cafe in town — coffee, fish tacos, great Wi-Fi' },
        { lat: -21.1330, lng: -175.2040, label: 'Waterfront Restaurant', num: 4, cat: 'food', desc: 'Fresh grilled fish and coconut curry on the verandah' }
      ]
    },
    {
      num: 2,
      date: '2026-06-03',
      neighborhoods: 'Eastern Tongatapu · Ha\'amonga · Hufangalupe · Anahulu Cave',
      title: 'Ancient Stones & Hidden Caves — Eastern Tongatapu',
      description: "Rent a car or hire a driver ($40–60 for the day) and explore eastern Tongatapu — home to Tonga's most impressive archaeological site, a stunning natural rock bridge, and a freshwater cave where you can swim underground by torchlight. The east coast is wild, windswept, and virtually untouched.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Ha\'amonga \'a Maui Trilithon',
              description: "Tonga's most important archaeological monument — a massive coral limestone trilithon (two uprights and a lintel) built around 1200 AD. Weighing roughly 40 tonnes, it's often called the 'Stonehenge of the Pacific.' The late King Taufa'ahau Tupou IV theorised it was used as a seasonal calendar, with a notch aligned to the solstice sunrise.",
              details: [
                '🏛️ Free entry · Open site, visit anytime',
                '📏 Each stone is about 5m tall and weighs ~12 tonnes',
                '🔭 Look for the small notch on the lintel — aligned to the June solstice',
                '📍 Eastern tip of Tongatapu, about 30min drive from Nuku\'alofa'
              ]
            },
            {
              title: 'Hufangalupe Natural Rock Bridge',
              description: "A dramatic coral rock arch spanning a churning turquoise cove on the southeast coast. Walk carefully to the edge (no railings) and look down into the surge channel where waves crash through the arch. One of the most spectacular natural formations in the Pacific.",
              details: [
                '⚠️ No barriers — be very careful near the edge, especially if windy',
                '📸 Best light in the morning when the sun illuminates the cove',
                '🆓 Free, always open · Short walk from the road'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Tupu\'anga Cafe',
              description: 'Worth the early start — home-roasted Tongan coffee, cassava cakes, lu pies (taro leaves in coconut cream), and lesi scones. Ask about their coffee roastery tour.',
              meta: '💰 $ · 📍 Vuna Road, Kolomotu\'a — just outside Nuku\'alofa'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Anahulu Cave',
              description: "A freshwater limestone cave with a crystal-clear underground pool perfect for swimming. Descend stone steps into the cool darkness, then slip into the water beneath stalactites and stalagmites. Bring a waterproof torch — the cave extends deeper than most visitors venture.",
              details: [
                '🏊 Bring a torch/flashlight and swimsuit',
                '💰 Small entry fee (TOP $10 / ~$4 USD)',
                '🌡️ Water is cool and refreshing — about 22°C year-round',
                '📍 Near the village of Haveluliku, eastern Tongatapu'
              ]
            },
            {
              title: 'Captain Cook\'s Landing Place',
              description: "A small monument marking where Captain James Cook first landed on Tongatapu in 1773. The setting — a quiet beach with pandanus trees — hasn't changed much in 250 years. A contemplative stop on the drive back.",
              details: [
                '📍 North shore, near the village of Mu\'a',
                '🆓 Free · Quiet spot, rarely other visitors'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Hiring a local driver for the day ($40–60 USD) is the best way to see eastern Tongatapu. They know the unmarked turnoffs and will share stories you won\'t find in any guidebook. Ask your guesthouse to arrange one.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Chef Zero Restaurant',
              description: 'Small, family-run restaurant near the waterfront serving generous plates of grilled fish, lobster (in season), and the best \'ota ika (Tongan raw fish in coconut cream) on the island. Arrive hungry.',
              meta: '💰 $ · 📍 Vuna Road, Nuku\'alofa'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -21.1543, lng: -175.0565, label: 'Ha\'amonga \'a Maui Trilithon', num: 1, cat: 'attraction', desc: '1,200-year-old stone trilithon — Stonehenge of the Pacific' },
        { lat: -21.1960, lng: -175.0580, label: 'Hufangalupe Rock Bridge', num: 2, cat: 'attraction', desc: 'Dramatic natural coral arch over churning turquoise cove' },
        { lat: -21.1675, lng: -175.0710, label: 'Anahulu Cave', num: 3, cat: 'attraction', desc: 'Underground freshwater cave for swimming beneath stalactites' },
        { lat: -21.1425, lng: -175.1035, label: 'Captain Cook Landing Place', num: 4, cat: 'attraction', desc: 'Monument marking Cook\'s 1773 landing — quiet historic beach' },
        { lat: -21.1290, lng: -175.2180, label: 'Tupu\'anga Cafe', num: 5, cat: 'food', desc: 'Home-roasted Tongan coffee and cassava cakes' },
        { lat: -21.1340, lng: -175.2020, label: 'Chef Zero Restaurant', num: 6, cat: 'food', desc: 'Best \'ota ika on the island — generous home-style plates' }
      ]
    },
    {
      num: 3,
      date: '2026-06-04',
      neighborhoods: '\'Atata Island · Offshore Reefs',
      title: 'Island Escape — Snorkeling \'Atata\'s Pristine Reef',
      description: "Take a boat to 'Atata Island, a tiny coral island about 30 minutes north of Nuku'alofa. The snorkeling here is world-class — pristine coral gardens, parrotfish, sea turtles, and visibility that stretches forever. Spend the day in the water, eat fresh fish on the beach, and forget that the rest of the world exists.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Boat to \'Atata Island',
              description: "Catch a morning boat from Faua Wharf to 'Atata Island — one of the closest and most beautiful offshore islands from Tongatapu. The Royal Sunset Island Resort operates transfers, or arrange a local boat through your guesthouse. The crossing takes 20–30 minutes through calm, turquoise water.",
              details: [
                '🚤 Boats from Faua Wharf, Vuna Road · Depart ~9am',
                '💰 Return transfer ~TOP $80–100 (~$35–45 USD) via local boat',
                '📍 Royal Sunset Resort on \'Atata can arrange day visits including snorkel gear',
                '🎒 Bring: sunscreen, water, snorkel gear (or rent on island), towel'
              ]
            }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Reef Snorkeling',
              description: "The reef off 'Atata's western shore is some of the best snorkeling in Tongatapu. Healthy hard corals, giant clams, schools of butterfly fish, parrotfish, and often green sea turtles. The water is warm (25°C), calm, and visibility can exceed 20 metres.",
              details: [
                '🐢 Green sea turtles are regularly spotted on the reef',
                '🪸 Healthy coral — Tonga\'s reefs are among the least degraded in the Pacific',
                '🌊 Calm conditions on the western side — perfect for beginners',
                '⚠️ Wear reef shoes and apply reef-safe sunscreen'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Beach Lunch',
              name: 'Fresh Fish BBQ on \'Atata',
              description: 'If arranged through your boat operator or the resort, lunch is fresh-caught fish grilled over coconut husks on the beach with taro, breadfruit, and coconut cream. This is Pacific Island eating at its purest.',
              meta: '💰 $ · 📍 \'Atata Island beachfront'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Beach Walk & Island Exploration',
              description: "'Atata is tiny — you can walk the entire coastline in under an hour. White sand, pandanus trees, and absolute silence except for waves and birdsong. Find a hammock, read a book, or just lie in the shallows and stare at the sky.",
              details: [
                '🏖️ The south beach is the most beautiful — white sand, no footprints',
                '🐚 Look for cowrie shells and sea glass along the tide line',
                '🌴 The island has fewer than 100 residents — it\'s deeply peaceful'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'If whale season has started early, ask your boat operator to keep an eye out on the crossing — humpbacks sometimes pass through the channel between Tongatapu and \'Atata.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Reload Bar & Restaurant',
              description: 'Back in Nuku\'alofa, unwind at this casual waterfront spot popular with locals and expats. Cold beer, grilled chicken, and surprisingly good pizza. Great place to meet other travelers.',
              meta: '💰 $ · 📍 Vuna Road, Nuku\'alofa'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -21.1185, lng: -175.2050, label: 'Faua Wharf', num: 1, cat: 'attraction', desc: 'Departure point for island boat trips — catch morning boat here' },
        { lat: -21.0567, lng: -175.2500, label: '\'Atata Island', num: 2, cat: 'attraction', desc: 'Pristine coral island — world-class snorkeling and white sand' },
        { lat: -21.0540, lng: -175.2520, label: '\'Atata Reef Snorkeling', num: 3, cat: 'attraction', desc: 'Healthy coral gardens with turtles, parrotfish, giant clams' },
        { lat: -21.1340, lng: -175.2015, label: 'Reload Bar & Restaurant', num: 4, cat: 'food', desc: 'Casual waterfront spot — cold beers and grilled chicken' }
      ]
    },
    {
      num: 4,
      date: '2026-06-05',
      neighborhoods: 'Western Tongatapu · Blowholes · Flying Foxes · Keleti Beach',
      title: 'Blowholes, Bats & the Wild West Coast',
      description: "Head west along Tongatapu's southern coast to the island's most dramatic natural attraction — the Mapu'a 'a Vaea blowholes, where the ocean erupts through hundreds of holes in the coral shelf. Continue to the village of Kolovai to see thousands of flying foxes hanging from casuarina trees, then end at Keleti Beach for a quiet swim on the west coast.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Mapu\'a \'a Vaea Blowholes',
              description: "Tongatapu's most spectacular natural sight. Along the southern coral coast, the ocean forces through hundreds of natural channels in the limestone shelf, creating geysers that shoot 10–20 metres into the air. On a big swell day, the entire coastline erupts. Throw coconut husks into the holes and watch them launch skyward.",
              details: [
                '🌊 Best with a southern swell — check conditions with your driver/guesthouse',
                '🥥 Local kids sell coconuts and demonstrate the blowhole launches — tip them',
                '💰 Small village donation (TOP $5–10) expected',
                '📍 Houma village, south coast — about 25min drive from Nuku\'alofa',
                '⚠️ Stay back from holes on big days — the pressure is genuinely dangerous'
              ]
            }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Kolovai Flying Fox Colony',
              description: "Thousands of Tongan flying foxes (fruit bats) roost in the casuarina trees near Kolovai village on the western tip of Tongatapu. They're considered sacred — protected by the royal family — and have lived here for centuries. Walking beneath the trees as thousands of bats hang overhead is surreal and unforgettable.",
              details: [
                '🦇 Best viewed midday when bats are roosting — they fly out at dusk',
                '📸 Bring a zoom lens — they hang 10–20m above in dense clusters',
                '🙏 Sacred to the royal family — treat the area with respect',
                '📍 Kolovai village, western Tongatapu — about 30min from the blowholes'
              ]
            }
          ],
          meals: [
            {
              type: '🥪 Lunch',
              name: 'Roadside Stall in Kolovai',
              description: 'Look for roadside stalls selling lu sipi (lamb and taro leaves in coconut cream baked in foil), fresh coconuts, and manioke chips. This is real Tongan food at real Tongan prices — TOP $5–10 for a full meal.',
              meta: '💰 $ · 📍 Kolovai village area'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Keleti Beach & Good Samaritan Inn',
              description: "End the day at Keleti Beach on the western coast — a quiet, palm-lined beach with calm water and barely another soul. The Good Samaritan Inn nearby has basic beach fales (huts) and cold drinks. Float in the warm Pacific and watch the afternoon light shift.",
              details: [
                '🏖️ Calm, shallow water — safe for swimming',
                '🍺 Cold Ikale beer at Good Samaritan Inn — TOP $5',
                '📍 Ha\'atafu area, western Tongatapu'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Kava Circle Experience',
              description: "Ask your guesthouse or driver to take you to a local kava circle tonight. Kava — a mildly sedative drink made from ground pepper root — is central to Tongan social life. The taste is earthy and numbing; the experience is profoundly communal. Visitors are always welcomed with warmth.",
              details: [
                '🥥 Kava is served in coconut shell cups — clap once before drinking, say "mālō" after',
                '🌙 Sessions often go past midnight — pace yourself',
                '🤝 This is where real conversations happen — Tongans are incredibly welcoming to solo visitors',
                '💰 Usually free or small contribution (TOP $10–20)'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'The Waterfront Cafe',
              description: 'Slightly different from the Waterfront Restaurant — this spot on the harbour does excellent wood-fired pizzas and fresh sashimi alongside Tongan favourites. Popular with the expat community.',
              meta: '💰 $$ · 📍 Vuna Road, Nuku\'alofa waterfront'
            }
          ],
          tips: [
            { type: 'tip', text: 'Don\'t eat a heavy dinner before kava — it\'s traditionally drunk on a relatively empty stomach. The numbing effect on your lips is completely normal and wears off quickly.' }
          ]
        }
      ],
      mapPins: [
        { lat: -21.2080, lng: -175.3180, label: 'Mapu\'a \'a Vaea Blowholes', num: 1, cat: 'attraction', desc: 'Hundreds of ocean geysers erupting through coral limestone' },
        { lat: -21.1890, lng: -175.3560, label: 'Kolovai Flying Fox Colony', num: 2, cat: 'attraction', desc: 'Thousands of sacred fruit bats roosting in casuarina trees' },
        { lat: -21.1750, lng: -175.3450, label: 'Keleti Beach', num: 3, cat: 'attraction', desc: 'Quiet western beach — palm trees, calm water, total peace' },
        { lat: -21.1340, lng: -175.2025, label: 'The Waterfront Cafe', num: 4, cat: 'food', desc: 'Wood-fired pizza and fresh sashimi on the harbour' }
      ]
    },
    {
      num: 5,
      date: '2026-06-06',
      neighborhoods: 'Nuku\'alofa · Offshore Waters',
      title: 'Whale Watching & Tongan Feast',
      description: "Today is the day you've been waiting for — a half-day whale watching trip to search for humpback whales in the waters off Tongatapu. Early June is the very start of season, so sightings aren't guaranteed, but the thrill of being on the water scanning for blows is unforgettable. Spend the afternoon at the Tongan National Centre, then cap the trip with a traditional 'umu feast.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Humpback Whale Watching Trip',
              description: "Board a small boat from Faua Wharf for a half-day whale watching expedition. Humpback whales migrate to Tonga from June to October to breed and calve in the warm waters. Early June means you're at the frontier — mothers with newborn calves are arriving, and the water is uncrowded. If conditions allow, you may get to swim with them.",
              details: [
                '🐋 Operators: Whale Time Tonga, Deep Blue Diving — book 1–2 days ahead',
                '💰 Half-day trip: ~$150–200 USD including gear and guide',
                '⏰ Depart ~7:30am, return ~12:30pm',
                '📸 Waterproof camera essential — GoPro rentals sometimes available',
                '⚠️ Early June = start of season. Sightings likely but not 100% guaranteed',
                '🤿 If whales are calm and conditions right, in-water swimming is possible (Tonga is one of the few places in the world this is legal)'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tongan National Centre',
              description: "A cultural complex just south of Nuku'alofa showcasing traditional Tongan life — tapa cloth making, wood carving, mat weaving, and dance performances. The guided tour explains Tongan social structure, the role of the monarchy, and how ancient Polynesian navigation worked.",
              details: [
                '🏛️ Guided tours available — about 1.5 hours',
                '💰 Entry ~TOP $25 (~$11 USD) · Cultural show extra',
                '🎭 Traditional dance performances on some days — check schedule',
                '📍 South of Nuku\'alofa, near the airport road'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Post-Whale Brunch',
              name: 'Friends Cafe',
              description: 'Return to the best cafe in town for a celebratory post-whale brunch. Big coffee, fresh juice, and fish tacos to refuel after a morning on the water.',
              meta: '💰 $ · 📍 Taufa\'ahau Road, Nuku\'alofa centre'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Traditional \'Umu Feast',
              description: "An 'umu is an underground earth oven — the Tongan way of cooking for centuries. Meats, root vegetables, and lu (taro leaves wrapped around fillings) are layered over hot stones, covered with banana leaves and earth, and slow-cooked for hours. Many guesthouses arrange 'umu nights, or ask at the Tongan National Centre. This is the meal of the trip.",
              details: [
                '🍖 Expect: suckling pig, chicken, fish, taro, yam, breadfruit, lu pulu (corned beef in taro leaves)',
                '🌿 Everything cooked underground in banana leaf wrappings',
                '💰 Guesthouse \'umu dinner: ~TOP $40–60 (~$17–26 USD)',
                '🤝 Often communal — sit on woven mats, eat with your hands, share food'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: '\'Umu Feast (Guesthouse or Cultural Centre)',
              description: 'The ultimate Tongan dining experience — earth-oven cooked suckling pig, root vegetables, and lu pulu. Communal, generous, unforgettable.',
              meta: '💰 $ · 📍 Arrange through your guesthouse'
            }
          ],
          tips: [
            { type: 'tip', text: 'Book the whale trip 1–2 days in advance — operators are small and fill up. If no whales are spotted, most operators offer a partial refund or free rebooking.' }
          ]
        }
      ],
      mapPins: [
        { lat: -21.1185, lng: -175.2050, label: 'Faua Wharf — Whale Trip Departure', num: 1, cat: 'attraction', desc: 'Board whale watching boat here at 7:30am' },
        { lat: -21.0500, lng: -175.1500, label: 'Whale Watching Area', num: 2, cat: 'attraction', desc: 'Offshore waters where humpbacks gather — early season' },
        { lat: -21.1580, lng: -175.2200, label: 'Tongan National Centre', num: 3, cat: 'attraction', desc: 'Cultural complex — tapa making, carving, dance performances' },
        { lat: -21.1345, lng: -175.2010, label: 'Friends Cafe', num: 4, cat: 'food', desc: 'Post-whale brunch — fish tacos and strong coffee' }
      ]
    },
    {
      num: 6,
      date: '2026-06-07',
      neighborhoods: 'Nuku\'alofa · Fua\'amotu',
      title: 'Final Morning — Market, Church & Farewell',
      description: "Your last morning in Tonga. If it's a Sunday, attend a church service — Tongan church choirs are genuinely world-class, and visitors are welcomed with enormous warmth. If not, revisit Talamahu Market for last-minute souvenirs, grab a final coffee, and head to the airport carrying the kind of peace that only the Pacific can give you.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sunday Church Service (if Sunday) or Market Visit',
              description: "June 7, 2026 is a Sunday! Tonga shuts down completely — shops, restaurants, everything. But this is a gift, not a problem. Attend a church service at the Free Wesleyan Church or the Catholic Basilica in Nuku'alofa. The multi-part harmonies of Tongan church choirs are among the most beautiful sounds on Earth. Dress modestly (long pants/skirt, covered shoulders) — visitors sit in the back and are always warmly received.",
              details: [
                '⛪ Free Wesleyan Church of Tonga — largest denomination, most impressive choirs',
                '🎵 Services typically 10am–12pm · Arrive 15min early for a seat',
                '👔 Dress code: modest. Long pants or skirt, covered shoulders',
                '📸 Photography usually OK but ask first — be respectful',
                '🙏 You will be welcomed. Tongans are deeply proud of their faith and happy to share it'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Guesthouse Breakfast',
              description: 'Most guesthouses serve breakfast on Sundays even when everything else is closed. Expect fresh tropical fruit, toast, eggs, and instant coffee. Simple and perfect.',
              meta: '💰 Included · 📍 Your accommodation'
            }
          ],
          tips: [
            { type: 'tip', text: 'Sunday in Tonga is sacred — plan accordingly! Buy snacks and water on Saturday. Your guesthouse will feed you but nothing else will be open. The church experience alone makes it worthwhile.' },
            { type: 'tip', text: 'The airport is 35min south of Nuku\'alofa. Taxis run even on Sundays (arrange through your guesthouse). Allow extra time — Tonga operates on "Tongan time."' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Transfer to Fua\'amotu Airport',
              description: "Say goodbye to the last kingdom. The drive to the airport passes through villages, past taro fields, and under coconut palms. Check in early — Fua'amotu is tiny but relaxed. Carry your memories, your tapa cloth, and the deep calm that Tonga leaves in everyone who visits.",
              details: [
                '✈️ Fua\'amotu International Airport (TBU) · 35min from Nuku\'alofa',
                '🚕 Taxi: TOP $30–40 (~$13–17 USD) · Arrange through guesthouse',
                '🛍️ Small duty-free shop at the airport for last-minute vanilla and handicrafts'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: -21.1365, lng: -175.2005, label: 'Free Wesleyan Church', num: 1, cat: 'attraction', desc: 'Sunday service with world-class Tongan choir harmonies' },
        { lat: -21.2410, lng: -175.1500, label: 'Fua\'amotu Airport (TBU)', num: 2, cat: 'attraction', desc: 'International airport — 35min south of Nuku\'alofa' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$30–60/night', midrange: '$60–120/night', luxury: '$120–250/night' },
    { category: 'Meals (solo)', budget: '$10–20/day', midrange: '$25–45/day', luxury: '$50–80/day' },
    { category: 'Transport (car/driver)', budget: '$15–25/day', midrange: '$40–60/day', luxury: '$80–120/day' },
    { category: 'Whale Watching', budget: '$150 (half-day)', midrange: '$200 (full-day)', luxury: '$350 (private boat)' },
    { category: '\'Atata Island Day Trip', budget: '$40 (local boat)', midrange: '$80 (resort transfer)', luxury: '$150 (private charter)' },
    { category: '6-Day Total (solo)', budget: '$550–750', midrange: '$800–1,200', luxury: '$1,500–2,500' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Fua\'amotu International Airport (TBU) on Tongatapu', 'Fiji Airways via Nadi (2hr) or Air New Zealand via Auckland (3hr)', 'Limited flight frequency — book well in advance', 'Airport taxi to Nuku\'alofa: TOP $30–40 (~$15 USD)'] },
    { title: '🏨 Where to Stay', items: ['Toni\'s Guest House — clean, central, friendly ($30–40/night)', 'Seaview Lodge — harbour views, good breakfast ($50–70/night)', 'Tanoa International Dateline Hotel — most upscale in town ($100–150/night)', 'Stay in central Nuku\'alofa for walkability — the town is tiny'] },
    { title: '🌡️ June Weather', items: ['Dry season — pleasant 24°C days, 18°C nights', 'Water temperature ~25°C — no wetsuit needed for snorkeling', 'Occasional brief showers but mostly sunny', 'UV is strong even in winter — sunscreen and hat essential'] },
    { title: '💳 Money & Logistics', items: ['Currency: Tongan Pa\'anga (TOP) — roughly 2.3 TOP = 1 USD', 'ATMs at BSP and TDB banks in Nuku\'alofa — withdraw cash here', 'Cards accepted at hotels and some restaurants but carry cash for everything else', 'Tipping not expected but appreciated for guides and boat operators'] },
    { title: '📱 Connectivity', items: ['Buy a Digicel SIM at the airport or in town — cheap data, decent coverage on Tongatapu', 'Wi-Fi available at most guesthouses and cafes', 'Coverage drops off quickly once you leave Nuku\'alofa — download offline maps', 'WhatsApp is the primary communication method in Tonga'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}