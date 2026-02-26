const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772114975799_efy6sx',
  email: 'sophieslot@hotmail.com',
  destination: 'Tawang',
  dates: '2026-03-13 to 2026-03-29',
  groupSize: 2,
  style: 'Adventure, Cultural, Foodie',
  dining: 'Mix of everything',
  budget: '$1,000-2,000',
  requests: 'Want to combine hiking and culture, 1-2 beach days as well\nExcited to try local food and night markets\nDon\'t like too touristy places'
};

const itineraryData = {
  destination: 'Tawang, India',
  countryEmoji: '🇮🇳',
  title: 'Tawang: Himalayan Monasteries, High Passes & Monpa Culture',
  subtitle: '16 days of high-altitude adventure, Buddhist heritage & local flavour in Arunachal Pradesh',
  description: "Tawang sits at 3,000 metres in the far northeastern tip of India, hemmed in by Bhutan, Tibet and some of the world's most dramatic Himalayan scenery. This 16-day circuit takes you through ancient monasteries where monks chant at dawn, across the legendary Sela Pass wreathed in cloud, to the Indo-China border at Bumla, and deep into remote Monpa villages that rarely see outsiders. A note on your beach-day request: Tawang is landlocked mountain country — but we've designed two dedicated 'lake days' at Madhuri Lake and Sela Lake that deliver the same serene, reset energy of a beach day, at 4,000 metres with Himalayan peaks reflected in turquoise water. The food scene is genuinely exciting — thukpa, zan, butter tea and smoky pork momos in tiny local dhabas. This trip will surprise you.",
  duration: '16 nights',
  dates: 'Mar 13 – Mar 29, 2026',
  budget: '$',
  pace: 'Moderate',
  bestFor: 'Adventure Couples',
  highlights: [
    'Tawang Monastery — Asia\'s 2nd-largest, 17th-century hilltop citadel with 400 monks',
    'Bumla Pass at 15,200 ft — stand at the Indo-China border',
    'Madhuri Lake day — turquoise high-altitude lake surrounded by snow peaks (your "lake day")',
    'Sela Pass crossing at 13,700 ft through frozen landscapes',
    'Zemithang valley — remote Monpa village with Gorsem Gompa and yak herders',
    'Chumi Gyatse — 108 sacred cascading waterfalls holy to Tibetan Buddhism',
    'Local food immersion: Monpa zan, thukpa, butter tea & smoky momos',
    'Nuranang (Bong Bong) Falls — jungle waterfall made famous by Bollywood'
  ],

  essentials: [
    { title: '📜 Inner Line Permit (ILP)', text: 'All visitors to Arunachal Pradesh require an Inner Line Permit. Apply online at arunachalilp.com or at district offices in Guwahati. Foreign nationals also need a Protected Area Permit (PAP) — apply at least 2 weeks before travel. Bumla Pass additionally requires a separate PAP for foreigners; book via a registered local tour operator. Get permits sorted BEFORE flying to Guwahati.' },
    { title: '🏔️ Altitude & Acclimatisation', text: 'Tawang town sits at 3,048m (10,000 ft); Sela Pass is 4,176m; Bumla is 4,633m. Take the Bomdila → Dirang → Tawang route slowly — 2 nights in Bomdila and 1 in Dirang helps. Drink 3+ litres of water daily, avoid alcohol for the first 3 days, and carry Diamox (consult your doctor). March nights drop to -5°C near passes — pack accordingly.' },
    { title: '🌊 About Your "Beach Days"', text: "Tawang is deep in the Himalayas — there are no beaches within 1,000km. But we've designed two dedicated lake days that hit the same reset-and-refresh notes: Madhuri Lake (Day 7) and Sela Lake (Day 5). Both are high-altitude turquoise lakes with snow peaks, absolute silence, and picnic-worthy shores. Think alpine Switzerland, not Goa. You'll love them." },
    { title: '🚗 Getting Around', text: 'The standard route: fly into Guwahati → shared sumo/taxi or private car via Bhalukpong → Bomdila → Dirang → Sela Pass → Tawang. Hiring a private taxi for the whole circuit costs ~₹18,000-25,000 ($215-300) and is strongly recommended for flexibility. Shared sumos are cheaper (~₹600/seat/day) but less comfortable on mountain roads. Local taxis in Tawang for day trips: ~₹2,000-3,500/day.' },
    { title: '🍽️ Food Culture', text: 'Tawang\'s cuisine is distinctly Monpa — influenced by Tibet and Bhutan. Must-tries: zan (buckwheat porridge with butter and cheese), thukpa (noodle soup), ting momos (steamed dumplings), butter tea (po cha), gyapa khazi (spiced rice), and smoked pork curry. The Main Bazaar area has the best local eateries. Night market stalls open from 7pm near the bus stand. No tipping culture — just honest, simple mountain food.' },
    { title: '💰 Budget Tips', text: 'For $1,000-2,000 total for two over 16 days, budget roughly: accommodation ₹800-2,000/night ($10-24), meals ₹200-400/day per person ($5-10), transport ₹1,500-3,000/day total ($18-36). Hire a shared sumo where possible. Eat at local dhabas (not hotel restaurants). Entry fees are minimal. Permits are free for Indian nationals; ~₹2,000 for foreigners.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-13',
      neighborhoods: 'Guwahati · Bhalukpong',
      title: 'Arrival in Guwahati — Gateway to the Northeast',
      description: 'Fly into Guwahati, collect your Inner Line Permits, and begin the road journey northeast toward Arunachal Pradesh. Tonight you cross the ILP checkpoint at Bhalukpong and sleep at the edge of the foothills — the Himalayan adventure begins.',
      timeBlocks: [
        {
          label: 'Morning / Afternoon',
          activities: [
            {
              title: 'Arrive Guwahati & Collect ILP',
              description: 'Land at Lokpriya Gopinath Bordoloi International Airport (GAU). Head into the city to collect your pre-arranged Inner Line Permits from the Arunachal Bhavan office or confirm your online permit at the checkpoint. Have printed copies + digital backups.',
              details: [
                '📜 Arunachal Bhavan, Guwahati — ILP collection: Mon-Sat, 10am-5pm',
                '🛂 ILP is checked at Bhalukpong entry point — don\'t skip this',
                '🏨 If collecting permits takes time, you may overnight in Guwahati'
              ]
            },
            {
              title: 'Road Trip Begins: Guwahati to Bhalukpong',
              description: 'Hit the road on NH-15. The 182km drive takes ~5 hours through Assam\'s lush tea gardens and Brahmaputra valley plains. At Bhalukpong, cross the ILP checkpoint into Arunachal Pradesh — the landscape shifts immediately.',
              details: [
                '🚗 Hire a private taxi from Guwahati airport or book in advance',
                '🍵 Drive passes through famous Assam tea estate country',
                '🌿 Bhalukpong sits at the confluence of the Kameng river and the hills'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Bhalukpong Town Dhabas',
              description: 'Simple roadside dhabas near the checkpoint serve dal-rice, paratha and basic North Indian food. Eat early — guesthouses here are simple.',
              meta: '💰 $ · 📍 Main Road, Bhalukpong'
            }
          ],
          tips: [
            { type: 'tip', text: 'Book your accommodation in Tawang in advance for March — rooms fill up. Call direct or use MakeMyTrip. Hotel Tawang Heights and Hotel Mon Regency are solid midrange picks.' },
            { type: 'tip', text: 'March weather: days ~12-18°C in the valleys; passes may have snow. Pack thermal layers, a good windproof jacket, and trekking boots.' }
          ]
        }
      ],
      mapPins: [
        { lat: 26.1445, lng: 91.7362, label: 'Guwahati Airport', num: 1, cat: 'attraction', desc: 'Gateway to Northeast India — fly in here' },
        { lat: 27.0049, lng: 92.6478, label: 'Bhalukpong Checkpoint', num: 2, cat: 'attraction', desc: 'ILP checkpoint — entry into Arunachal Pradesh' },
        { lat: 27.0100, lng: 92.6400, label: 'Bhalukpong Guesthouse', num: 3, cat: 'attraction', desc: 'Overnight stop at the foothills of Arunachal' }
      ]
    },
    {
      num: 2,
      date: '2026-03-14',
      neighborhoods: 'Bhalukpong · Bomdila',
      title: 'Into the Hills — Tippi Orchid Centre & Bomdila Arrival',
      description: 'The road climbs from tropical foothills into pine-scented mountain country. Stop at the Tippi Orchid Research Centre, catch the Sessa waterfall, and arrive in Bomdila — a charming hill town with Buddhist monasteries and a lively local market.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tippi Orchid Research Centre',
              description: 'En route to Bomdila, stop at the Tippi Orchid Research Centre — home to over 500 species of orchids. March is orchid season in the foothills. The centre also has a butterfly garden and is largely unknown to mainstream tourists.',
              details: [
                '🌸 500+ orchid species including rare blue vanda and rhynchostylis',
                '🦋 Butterfly garden alongside orchid houses',
                '⏰ Open 9am-4pm · Entry nominal fee'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Sessa Waterfall Photo Stop',
              description: 'A short detour brings you to the Sessa Waterfall — a beautiful jungle cascade surrounded by ferns and mossy rocks. It\'s a refreshing break from the road and often deserted on weekdays.',
              details: [
                '📍 Near Sessa village, ~15 mins off the main road',
                '🌊 Good monsoon flow even in March with snowmelt'
              ]
            },
            {
              title: 'Arrive Bomdila & Evening Wander',
              description: 'Reach Bomdila (2,415m) by afternoon. Walk around the Main Market area — a mix of Tibetan traders, local Aka tribals, and AMA (Arunachal Mahila Association) shops selling handwoven textiles. Visit the Lower Gompa before sunset.',
              details: [
                '🛍️ AMA market for handwoven shawls and tribal textiles at genuine prices',
                '🕌 Lower Gompa — active monastery, prayer wheels and butter lamp hall'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Café La Bomdila (Café/Restaurant near market)',
              description: 'Cozy café in the market area serving Tibetan noodles, thukpa and local rice dishes. A favourite of backpackers and the few travellers who linger in Bomdila.',
              meta: '💰 $ · 📍 Main Market, Bomdila'
            }
          ],
          tips: [
            { type: 'tip', text: 'Bomdila is your first acclimatisation stop at 2,415m. Take it easy tonight — short walks only, no alcohol.' }
          ]
        }
      ],
      mapPins: [
        { lat: 27.1167, lng: 92.4167, label: 'Tippi Orchid Centre', num: 1, cat: 'attraction', desc: '500+ orchid species — stop en route to Bomdila' },
        { lat: 27.2644, lng: 92.4108, label: 'Bomdila', num: 2, cat: 'attraction', desc: 'Charming hill town at 2,415m — first acclimatisation stop' },
        { lat: 27.2630, lng: 92.4090, label: 'Lower Gompa Bomdila', num: 3, cat: 'attraction', desc: 'Active Buddhist monastery with prayer wheels' },
        { lat: 27.2650, lng: 92.4120, label: 'AMA Market Bomdila', num: 4, cat: 'food', desc: 'Handwoven textiles, tribal crafts and local snacks' }
      ]
    },
    {
      num: 3,
      date: '2026-03-15',
      neighborhoods: 'Bomdila',
      title: 'Bomdila — Monasteries, Museums & Mountain Views',
      description: 'A full day to explore Bomdila at a gentle pace. This is your acclimatisation day — a critical investment before the higher passes ahead. Visit three monasteries at different altitudes, learn Arunachal\'s tribal history at the district museum, and browse the bustling Tibetan market.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'GRL Monastery (Upper Gompa)',
              description: 'The Gontse Rabgyel Ling (GRL) Monastery sits above Bomdila with sweeping views of the Himalayan range. Founded in 1965, it houses butter lamp rooms, ancient thangkas and a towering Buddha statue. Arrive early to hear morning prayers.',
              details: [
                '⛩️ Morning prayers 6-7am — sit quietly at the back',
                '🏔️ Terrace views: on clear days, see as far as the Kangto peak (7,090m)',
                '🕯️ Butter lamp hall — the smell alone is meditative'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Hotel Blue Pine Café',
              description: 'Simple guesthouse café with excellent local breakfast: buckwheat pancakes (zan), butter tea and boiled eggs. The view of the mountains from the dining room makes it.',
              meta: '💰 $ · 📍 Bomdila town'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Bomdila Museum & Crafts Emporium',
              description: 'The Bomdila Museum covers the tribal cultures of Arunachal Pradesh — the Aka, Miji, Sherdukpen and Monpa peoples. Small but genuinely informative. Next door, the Crafts Emporium sells authentic cane-and-bamboo crafts, woollen textiles and Monpa masks at fixed government prices.',
              details: [
                '🏛️ Museum: Tue-Sun, 10am-4pm · Free entry',
                '🧶 Crafts Emporium: better prices than market stalls for quality pieces'
              ]
            },
            {
              title: 'Middle Gompa & Tibetan Market',
              description: 'The Middle Gompa is smaller but beautifully painted — look for the murals depicting the life of Buddha. Then explore the Tibetan market: yak butter, dried fruit, medicinal herbs, prayer flags and locally-produced apple wine (Arunachal Pradesh is famous for its apples).',
              details: [
                '🍎 March is not apple season but you\'ll find dried apple products and cider',
                '🧧 Prayer flags and Tibetan silver jewellery at good prices',
                '📍 Tibetan Market is 5 min walk from the Middle Gompa'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Drink 3 litres of water today. Headaches at 2,400m are common — Diamox helps but isn\'t a substitute for hydration and rest.' }
          ]
        }
      ],
      mapPins: [
        { lat: 27.2680, lng: 92.4095, label: 'GRL Upper Monastery', num: 1, cat: 'attraction', desc: 'Hilltop monastery with panoramic Himalayan views' },
        { lat: 27.2644, lng: 92.4108, label: 'Middle Gompa', num: 2, cat: 'attraction', desc: 'Beautiful painted monastery in town centre' },
        { lat: 27.2610, lng: 92.4080, label: 'Bomdila Museum', num: 3, cat: 'attraction', desc: 'Tribal culture and Arunachal heritage exhibits' },
        { lat: 27.2655, lng: 92.4115, label: 'Tibetan Market', num: 4, cat: 'food', desc: 'Yak butter, apple wine, prayer flags and silver' }
      ]
    },
    {
      num: 4,
      date: '2026-03-16',
      neighborhoods: 'Bomdila · Dirang',
      title: 'Drive to Dirang — Dzong, Hot Springs & Apple Orchards',
      description: 'A scenic 96km drive through pine forests and river valleys brings you to Dirang — a gorgeous medieval village with a 500-year-old dzong (fort) and natural hot springs. Dirang is one of the most underrated stops on the Tawang circuit.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive Bomdila to Dirang',
              description: 'The 3-hour drive follows the Dirang Chu river valley — waterfalls cascade from roadside cliffs and kiwi vines grow wild along the verge. Look out for Rufous-necked hornbills in the trees.',
              details: [
                '🚗 96km, ~3 hours on mountain roads',
                '🦜 Excellent birding en route — bring binoculars',
                '🥝 Kiwi and apple orchards line the valley — March is blossom season'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Dirang Dzong',
              description: 'The 500-year-old Dirang Dzong (fort) sits above the village and is one of the most authentic medieval settlements in Arunachal. Walk through narrow stone-paved lanes between whitewashed houses, spot old women spinning yak wool on hand spindles, and find the dzong\'s ancient shrine rooms.',
              details: [
                '🏯 Dzong is still inhabited — be respectful of residents',
                '📸 The stone lanes with prayer flags are photogenic at any time of day',
                '🐄 Yaks and sheep graze freely through the dzong lanes'
              ]
            },
            {
              title: 'Dirang Hot Springs',
              description: 'After days of mountain driving, nothing beats soaking in Dirang\'s natural sulphur hot springs by the river. The springs are modest — concrete tubs built around the natural source — but the mineral water is genuinely therapeutic after acclimatisation.',
              details: [
                '♨️ Water temperature: 40-45°C — genuinely hot',
                '📍 Located 3km from Dirang town, riverside',
                '⏰ Open sunrise to sunset, small fee for entry'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Local Dhaba near Dirang Market',
              description: 'Ask your guesthouse to recommend the best local dhaba — small family-run places serve rice, dal, pork curry and fresh vegetables. The pork dishes in Dirang are particularly good.',
              meta: '💰 $ · 📍 Dirang Market area'
            }
          ],
          tips: [
            { type: 'tip', text: 'Stay in Dirang overnight — don\'t rush through. It\'s the most off-the-beaten-track stop on the circuit and genuinely untouristy. Hotel Pemaling or Circuit House are good options.' }
          ]
        }
      ],
      mapPins: [
        { lat: 27.3477, lng: 92.2481, label: 'Dirang Dzong', num: 1, cat: 'attraction', desc: '500-year-old medieval fort village, still inhabited' },
        { lat: 27.3490, lng: 92.2450, label: 'Dirang Hot Springs', num: 2, cat: 'attraction', desc: 'Natural sulphur hot springs by the Dirang Chu river' },
        { lat: 27.3460, lng: 92.2500, label: 'Dirang Market', num: 3, cat: 'food', desc: 'Local dhabas and small market for fresh produce' }
      ]
    },
    {
      num: 5,
      date: '2026-03-17',
      neighborhoods: 'Dirang · Sela Pass · Tawang',
      title: '🏔️ LAKE DAY 1 — Sela Pass & Sela Lake (Your High-Altitude "Beach Day")',
      description: 'Today is your first designated lake day — Sela Pass at 13,700 ft, with the sacred Sela Lake sitting in a bowl of snow-streaked mountains. We promised you a beach vibe at altitude: pack a picnic, sit by the turquoise water, listen to the silence, and feel the thin air. Then drop down through Jaswant Garh War Memorial and Nuranang Falls to Tawang.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Early Start: Dirang to Sela Pass',
              description: 'Leave Dirang by 7am — the 87km drive to Tawang via Sela Pass takes 5-6 hours with stops. The climb from Dirang to the pass is dramatic: thick rhododendron forests give way to stunted alpine shrubs, then bare rock and ice. The pass itself is often in cloud — arrive before 9am for clear views.',
              details: [
                '⏰ Depart by 7am — passes cloud over by midday',
                '🌸 Rhododendrons bloom blood-red along this route in March-April',
                '❄️ The pass may have snow — keep traction devices in the car just in case'
              ]
            },
            {
              title: 'Sela Lake Picnic — Your Himalayan "Beach Day"',
              description: 'Sela Lake (4,175m) sits right at the top of the pass — a perfectly round glacial lake surrounded by snow-dusted peaks. It\'s utterly serene. Buy momos or snacks from the small stall at the top, find a boulder by the lakeshore, and just sit. The air is thin but the silence is absolute. This is your reset day.',
              details: [
                '🏖️ Bring a picnic — warm food, thermos of chai, chocolate',
                '📸 Reflection shots of the peaks in the lake are stunning',
                '🙏 The lake is considered sacred — Sela herself is said to have sacrificed her life here for an Indian soldier',
                '🥶 Temperature at the pass: 2-8°C in March — full winter layers needed'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Jaswant Garh War Memorial',
              description: 'Just below the pass, Jaswant Garh honours Rifleman Jaswant Singh Rawat who held off Chinese forces for 72 hours alone in 1962. The memorial is maintained with a dignified simplicity. Ask your driver for the full story — it\'s extraordinary.',
              details: [
                '🪖 The memorial includes his original bunker, weapons and personal items',
                '📍 15km below Sela Pass on the Tawang side'
              ]
            },
            {
              title: 'Nuranang (Bong Bong) Falls',
              description: 'One of the most spectacular waterfalls in northeast India — a 100-metre plunge into a gorge, surrounded by dense jungle. The falls became famous after the Bollywood film Koyla (1997) was filmed here. The jungle walk to the viewpoint takes 20 minutes.',
              details: [
                '💧 Best flow in March due to snowmelt — spectacular',
                '🎬 Film location for Koyla (1997)',
                '⏰ Allow 45 mins total including the jungle walk'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Tawang town — First Dinner in the City',
              description: 'Arrive in Tawang as the sun sets over the valley. Dragon Restaurant in the Main Bazaar area is the go-to first-night spot: thukpa, momos, butter tea and a celebratory beer.',
              meta: '💰 $ · 📍 Dragon Restaurant, Main Bazaar, Tawang'
            }
          ],
          tips: [
            { type: 'tip', text: 'Tawang town sits at 3,048m (10,000 ft). After the pass crossing, you\'ll be acclimatised enough to sleep well tonight. Still drink plenty of water.' }
          ]
        }
      ],
      mapPins: [
        { lat: 27.4862, lng: 92.0889, label: 'Sela Pass (4,176m)', num: 1, cat: 'attraction', desc: 'Iconic high mountain pass — gateway to Tawang' },
        { lat: 27.4900, lng: 92.0900, label: 'Sela Lake', num: 2, cat: 'attraction', desc: 'Sacred glacial lake at the pass — your first lake day' },
        { lat: 27.4750, lng: 92.1100, label: 'Jaswant Garh Memorial', num: 3, cat: 'attraction', desc: 'Moving war memorial below the pass' },
        { lat: 27.4383, lng: 92.1158, label: 'Nuranang Falls', num: 4, cat: 'attraction', desc: 'Spectacular 100m jungle waterfall — Bollywood location' },
        { lat: 27.5859, lng: 91.8679, label: 'Tawang Town', num: 5, cat: 'attraction', desc: 'Your base for the next 8 nights — arrive at sunset' }
      ]
    },
    {
      num: 6,
      date: '2026-03-18',
      neighborhoods: 'Tawang',
      title: 'Tawang Monastery — Asia\'s 2nd Largest Buddhist Complex',
      description: 'Dedicate a full day to the Tawang Monastery (Galden Namgey Lhatse) — a 17th-century hilltop fortress-monastery that is the spiritual heart of the entire region. Morning prayers, ancient thankas, a 28-foot golden Buddha, and views over the valley that will stop your breath.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Dawn Prayers at Tawang Monastery',
              description: 'Arrive before 6am to witness the monks\' morning puja. The drone of horns, clash of cymbals and deep chanting reverberates through the cold stone halls. 450 monks live within the monastery walls — this is a living, breathing religious community, not a museum.',
              details: [
                '⏰ Morning prayers: 5:30-7am — arrive by 5:45am',
                '🛕 Monastery built 1681 at 3,300m by Merak Lama Lodre Gyatso',
                '🚫 Remove shoes in the prayer hall; no photography during active prayers',
                '🎺 The radong (long horn trumpets) are unforgettable at dawn'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Monastery Café',
              description: 'A small café near the monastery gate serves butter tea, thukpa and basic Tibetan breakfast. Ideal after the dawn prayers.',
              meta: '💰 $ · 📍 Near monastery entrance'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Monastery Museum & Golden Buddha',
              description: 'The monastery library holds over 400 ancient hand-written manuscripts and tankas (painted silk scrolls). The main shrine houses a 28-foot golden Buddha — the centrepiece of the entire complex. The museum in the prayer hall displays 16th century thankas, weaponry and costumes.',
              details: [
                '📚 Library: rare Buddhist manuscripts in Tibetan script',
                '🖼️ Thankas painted on silk — some 400+ years old',
                '📸 Golden Buddha hall — photography permitted (no flash)',
                '⏰ Museum open 9am-4pm · Small entry fee'
              ]
            },
            {
              title: 'Monastery Ramparts Walk & Valley Views',
              description: 'Walk the outer ramparts of the monastery for panoramic views of the Tawang valley and the surrounding Himalayan peaks. On clear days you can see Tibet. The whitewashed walls glow golden in afternoon light — some of the best photographs you\'ll take on the trip.',
              details: [
                '📸 Best light for photography: 2-4pm as sun drops toward the west',
                '🏔️ On clear days: views of peaks over 6,000m in Tibet',
                '🌀 Spin the prayer wheels as you walk the perimeter'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Hire a monastery guide (₹300-500 for 2 hours) — they explain the thangkas, the Buddha legends and the monastery\'s extraordinary history. Worth every rupee.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Tawang Main Bazaar & Night Market',
              description: 'After the monastery, wander the Main Bazaar as it comes alive in the evening. Street food stalls set up from 6pm — hot momos with chamin sauce, grilled corn, deep-fried puri with potato curry. A few stalls near the bus stand sell local Monpa rice wine (apong). This is your closest equivalent to a night market in Tawang.',
              details: [
                '🥟 Best momos: look for the cart near the main square with the longest queue',
                '🌽 Grilled corn with chilli-lime — classic mountain street food',
                '🍶 Apong (millet/rice wine) — local brew, try it at least once',
                '⏰ Stalls are busiest 6:30-8:30pm'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 27.5843, lng: 91.8659, label: 'Tawang Monastery', num: 1, cat: 'attraction', desc: 'Asia\'s 2nd-largest monastery — 17th century hilltop citadel' },
        { lat: 27.5870, lng: 91.8680, label: 'Tawang Main Bazaar', num: 2, cat: 'food', desc: 'Evening market with momos, street food and local wine' },
        { lat: 27.5860, lng: 91.8670, label: 'Dragon Restaurant', num: 3, cat: 'food', desc: 'Best thukpa and butter tea in town' }
      ]
    },
    {
      num: 7,
      date: '2026-03-19',
      neighborhoods: 'Tawang · Bumla Road',
      title: '🏔️ LAKE DAY 2 — Madhuri Lake & Bumla Pass (Your Himalayan "Beach Day")',
      description: 'Your second lake day — Madhuri Lake (Sangetsar Tso) at 4,200m is the most photographed lake in Arunachal Pradesh. Turquoise water, snow-streaked peaks reflected perfectly, a ring of dead-standing pine trees killed by the 1950 earthquake. Then push on to Bumla Pass at the Indo-China border. This is a full-day excursion that requires an early start.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Early Drive to Madhuri Lake (Sangetsar Tso)',
              description: 'Depart Tawang by 6am on the road toward Bumla Pass. After ~40km of dramatic mountain driving, you reach Madhuri Lake — named after Bollywood actress Madhuri Dixit who danced here in the film Koyla. The setting is surreal: perfectly still turquoise water ringed by ghost trees (killed by earthquake uplift) with Himalayan peaks rising behind.',
              details: [
                '🏖️ THIS IS YOUR LAKE DAY — bring a blanket, snacks, thermos of chai',
                '🐓 The road up passes dozens of high-altitude yak herding camps',
                '📸 Best photos: early morning before clouds roll in (before 10am)',
                '🌡️ Temperature at the lake: 0-5°C in March — full winter gear required',
                '⚠️ Requires PAP permit for foreigners — ensure you have it'
              ]
            }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'PT Tso Lake',
              description: 'A short drive beyond Madhuri brings you to PT Tso (Pankong Tso) — smaller, quieter, and even more reflective. Few tourists make it this far. Sit by the lakeshore and eat your packed lunch in total silence.',
              details: [
                '🤫 Often completely empty — genuine off-the-beaten-path lake',
                '🦢 Migratory bar-headed geese in March',
                '📍 4km beyond Madhuri Lake on the Bumla road'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Bumla Pass — Stand at the Indo-China Border',
              description: 'Bumla Pass (4,633m / 15,200 ft) is the actual Indo-China border in Arunachal Pradesh — Indian and Chinese soldiers stand on either side of a white line. You can see Chinese territory from where you stand. The site is both thrilling and deeply sobering.',
              details: [
                '🛂 PAP permit required — Indian nationals need this too',
                '🏔️ At 4,633m: the altitude hit is real — walk slowly, no exertion',
                '🇨🇳 Chinese soldiers across the line — photography rules apply, follow guides',
                '🌬️ Wind at the pass is extreme — dress for -5°C even in March'
              ]
            },
            {
              title: 'Chumi Gyatse Waterfalls',
              description: 'On the way back to Tawang, stop at Chumi Gyatse — 108 sacred waterfalls cascading in tiers down a cliff face. In Tibetan Buddhism, 108 is a deeply auspicious number. In March, the falls are partly frozen, creating ice curtains alongside the cascades.',
              details: [
                '🕉️ 108 falls = 108 sacred beads on a mala rosary',
                '❄️ In March: waterfall + ice curtain combination is spectacular',
                '📍 On the Tawang-Bumla road, ~10km before Tawang'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Yaksi Café, Old Market',
              description: 'Tawang\'s most beloved local café — famous for pork thukpa and butter tea. Very small, very local, entirely unpretentious. Often has Monpa locals and monks eating alongside tourists.',
              meta: '💰 $ · 📍 Old Market area, Tawang'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 27.6967, lng: 91.9522, label: 'Madhuri Lake (Sangetsar)', num: 1, cat: 'attraction', desc: 'Stunning turquoise lake at 4,200m — Lake Day #2' },
        { lat: 27.6833, lng: 91.9500, label: 'PT Tso Lake', num: 2, cat: 'attraction', desc: 'Quieter lake beyond Madhuri, often empty' },
        { lat: 27.7536, lng: 91.9894, label: 'Bumla Pass (4,633m)', num: 3, cat: 'attraction', desc: 'Indo-China border — stand at the frontier' },
        { lat: 27.6500, lng: 91.9000, label: 'Chumi Gyatse Falls', num: 4, cat: 'attraction', desc: '108 sacred waterfalls — partly frozen in March' },
        { lat: 27.5850, lng: 91.8660, label: 'Yaksi Café', num: 5, cat: 'food', desc: 'Local legend for pork thukpa and butter tea' }
      ]
    },
    {
      num: 8,
      date: '2026-03-20',
      neighborhoods: 'Tawang · Urgelling · Bekhar',
      title: 'Dalai Lama\'s Birthplace & The Giant Buddha',
      description: 'Explore the sacred sites linked to the 6th Dalai Lama, born in this valley in 1683. Visit Urgelling Monastery — his birthplace — and the small house in Bekhar village where he grew up, before standing before Tawang\'s iconic 28-metre Giant Buddha statue overlooking the entire valley.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Urgelling Monastery — Birthplace of the 6th Dalai Lama',
              description: 'Urgelling is one of Arunachal Pradesh\'s most sacred sites — the small monastery where Tsangyang Gyatso, the 6th Dalai Lama, was born in 1683. It\'s much quieter than Tawang Monastery and has a different, more intimate energy. The original structure is ancient; look for the birth-room shrine.',
              details: [
                '🕌 One of the oldest monasteries in Tawang district',
                '🧘 Intimate atmosphere — often just a few monks present',
                '📜 The 6th Dalai Lama later became famous for his romantic poetry (unusual for a Dalai Lama)'
              ]
            },
            {
              title: 'Bekhar Village — The 6th Dalai Lama\'s Home',
              description: 'A short walk from Urgelling, Bekhar village preserves the traditional stone-and-wood home where the young Tsangyang Gyatso grew up. The village itself is beautifully preserved — ask an elder to show you around (they\'ll be delighted). This is as off-the-beaten-track as it gets in Tawang.',
              details: [
                '🏠 Traditional Monpa architecture — stone walls, wooden beams',
                '👴 Village elders often speak some English — great for conversation',
                '📍 5km from Tawang town — short taxi ride or 1.5hr walk'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Giant Buddha Statue (Tawang)',
              description: 'The 28-metre bronze Buddha statue above Tawang sits on a hilltop and can be seen from across the valley. Climb the steps for panoramic views that take in the entire Tawang town, the monastery, and the surrounding peaks. March afternoon light turns everything golden.',
              details: [
                '📸 Best viewpoint in Tawang for the "whole valley" shot',
                '🌅 Afternoon light (2-4pm) is ideal for photography',
                '🏔️ On clear days: snow peaks of Tibet visible on the northern horizon'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Zomsa Restaurant',
              description: 'The name means "place of meeting" in Tibetan — Zomsa lives up to it. Great mix of Tibetan and local Monpa dishes, friendly staff, and a good vantage point in the market area.',
              meta: '💰 $ · 📍 Main Market, Tawang'
            },
            {
              type: '🍽️ Dinner',
              name: 'Hotel Mon Valley Kitchen',
              description: 'Traditional Monpa recipes passed down locally — this is the most authentic dinner experience in Tawang. Order zan (buckwheat porridge) with butter, chura sabji (local cheese with vegetables) and butter tea.',
              meta: '💰 $-$$ · 📍 Hotel Mon Valley, Tawang'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 27.5967, lng: 91.8600, label: 'Urgelling Monastery', num: 1, cat: 'attraction', desc: 'Birthplace of the 6th Dalai Lama — 1683' },
        { lat: 27.5950, lng: 91.8580, label: 'Bekhar Village', num: 2, cat: 'attraction', desc: 'Ancestral home of the 6th Dalai Lama, traditional Monpa village' },
        { lat: 27.5917, lng: 91.8667, label: 'Giant Buddha Statue', num: 3, cat: 'attraction', desc: '28-metre hilltop Buddha with sweeping valley views' },
        { lat: 27.5870, lng: 91.8680, label: 'Zomsa Restaurant', num: 4, cat: 'food', desc: 'Tibetan-Monpa fusion in a welcoming setting' }
      ]
    },
    {
      num: 9,
      date: '2026-03-21',
      neighborhoods: 'Tawang · Zemithang Valley',
      title: 'Zemithang — The Remote Monpa Frontier',
      description: 'Today is the adventure highlight — a 93km drive deep into the Zemithang valley to reach one of the most remote Monpa settlements in India. The valley sits near the Bhutan border with views into Bhutanese territory. Gorsem Gompa is the main monastery here, and the village life is entirely untouched by tourism.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive to Zemithang (Full Day Excursion)',
              description: 'The 93km drive from Tawang to Zemithang takes 3-4 hours on rough mountain roads. The valley opens up dramatically as you descend — terraced fields, yak herds, and traditional Monpa settlements cling to the hillsides. The landscape shifts from alpine to a warmer sub-alpine valley floor.',
              details: [
                '🚗 Start by 6:30am — roads can be slow, return before dark',
                '⚠️ Roads can be rough in places — 4WD/Sumo recommended',
                '🏔️ The drive passes through landscapes with almost zero tourist infrastructure',
                '📸 Every hairpin turn reveals a new valley panorama'
              ]
            },
            {
              title: 'Gorsem Gompa',
              description: 'Gorsem Gompa (Khinmey Nyingma Monastery) sits dramatically at the edge of the valley overlooking the Nyamjang Chu river. Built on a cliff, it dates from the 15th century and is associated with Guru Rinpoche. The murals inside are extraordinary — vivid tantric imagery in original pigment.',
              details: [
                '🎨 Original 15th-century tantric murals — remarkable preservation',
                '🏔️ Cliff-edge position with views into Bhutan',
                '🙏 Active monastery — monks in residence year-round',
                '📍 Ask your driver to call ahead — the caretaker monk may unlock locked rooms'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Zemithang Village & Monpa Community',
              description: 'Walk through Zemithang village — one of the most isolated communities on the Tawang circuit. Monpa families weave wool, tend their fields and herd yaks using centuries-old methods. Very few outside visitors make it this far. Accept any invitation for tea — the hospitality is extraordinary.',
              details: [
                '☕ Po cha (butter tea) offered in homes — always accept',
                '🧶 Watch women weave traditional Monpa woollen fabric',
                '🐄 Yak herds roam freely through the village — don\'t startle them',
                '🛍️ May find hand-woven textiles and yak-wool items for sale directly from weavers'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Packed Lunch',
              name: 'Pack food from Tawang',
              description: 'There are no restaurants in Zemithang. Pack a thermos of chai, momos, bread and fruit from Tawang before departure. Your driver will know a good source.',
              meta: '💰 $ · Bring everything from Tawang'
            }
          ],
          tips: [
            { type: 'tip', text: 'This is the most genuinely untouristy day of the trip. No English menus, no souvenir shops, no crowds. Just mountains, monasteries and real Monpa life. Bring your curiosity.' }
          ]
        }
      ],
      mapPins: [
        { lat: 27.7167, lng: 91.6500, label: 'Zemithang Valley', num: 1, cat: 'attraction', desc: 'Remote Monpa valley 93km from Tawang' },
        { lat: 27.7200, lng: 91.6450, label: 'Gorsem Gompa', num: 2, cat: 'attraction', desc: '15th-century cliff monastery with original tantric murals' },
        { lat: 27.7150, lng: 91.6500, label: 'Zemithang Village', num: 3, cat: 'attraction', desc: 'Isolated Monpa community near Bhutan border' }
      ]
    },
    {
      num: 10,
      date: '2026-03-22',
      neighborhoods: 'Tawang · Mukto Village · Chakzam Bridge',
      title: 'Hidden Tawang — Chain Bridge, Offbeat Villages & Local Life',
      description: 'A relaxed day exploring Tawang\'s most underrated corners: the 600-year-old Chakzam chain bridge, the offbeat Monpa village of Mukto, and an afternoon wandering the Old Market. No tour groups, no crowded viewpoints — just local life.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Chakzam Bridge — 600-Year-Old Chain Bridge',
              description: 'The Chakzam (Chagzam) Bridge is one of the most extraordinary structures in northeast India — an iron chain bridge built in the 15th century, still standing. It spans the Tawang Chu gorge with dramatic drops on either side. Very few tourists know about it.',
              details: [
                '🌉 Iron chain bridge, 15th century — a true engineering marvel for its era',
                '📍 6km from Tawang town along the river gorge',
                '😨 The bridge sways — thrilling for adventurers, terrifying for others',
                '🚗 Take a local taxi or walk the river path (40 min)'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Mukto Village',
              description: 'The small village of Mukto is the closest thing to "old Tawang" left — traditional Monpa houses with carved wooden balconies, spinning women, and community prayer flags stretched between rooftops. Historically significant as a trading hub between India and Tibet.',
              details: [
                '🏘️ Traditional architecture largely intact',
                '📸 Spinning women at doorways — ask permission before photographing',
                '🗺️ About 8km from Tawang — ask your driver or walk via a farm trail'
              ]
            },
            {
              title: 'Old Market Tawang & Shopping',
              description: 'The Old Market (separate from the main bazaar) has the best selection of genuine Monpa crafts: hand-spun yak wool carpets, masks used in Tawang festival dances, traditional chopsticks, prayer beads and incense. Prices are negotiable but fair.',
              details: [
                '🧧 Best souvenirs: Monpa masks (₹500-2,000), woollen shawls (₹300-800)',
                '🪬 Singing bowls, prayer flags and thangka prints available too',
                '🛍️ Fixed prices at government emporium; bargain gently at private stalls'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Tawang Restaurant, Main Bazaar',
              description: 'Homestyle local cooking — no frills, excellent quality. Dal tadka, seasonal greens with garlic, chicken curry and rice. Popular with government workers and monks on lunch break.',
              meta: '💰 $ · 📍 Main Bazaar, Tawang'
            },
            {
              type: '🍽️ Dinner',
              name: 'Evening Momos at Night Market',
              description: 'Return to the Main Bazaar evening stalls for a repeat performance of the night market food — ting momos (soup dumplings), grilled skewers and hot corn. By now you\'ll know which cart is best.',
              meta: '💰 $ · 📍 Main Bazaar area, from 6:30pm'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 27.5800, lng: 91.8900, label: 'Chakzam Chain Bridge', num: 1, cat: 'attraction', desc: '15th-century iron chain bridge over Tawang Chu gorge' },
        { lat: 27.5720, lng: 91.8750, label: 'Mukto Village', num: 2, cat: 'attraction', desc: 'Traditional Monpa village with carved wooden balconies' },
        { lat: 27.5870, lng: 91.8680, label: 'Old Market Tawang', num: 3, cat: 'food', desc: 'Monpa crafts, masks, yak-wool carpets and souvenirs' }
      ]
    },
    {
      num: 11,
      date: '2026-03-23',
      neighborhoods: 'Tawang · Gorichen Base Area',
      title: 'Hiking Day — Gorichen Trek & Alpine Meadows',
      description: 'Today is pure adventure: a mountain hike into the alpine zone above Tawang. The Gorichen region (towards the base of Arunachal\'s highest peak at 6,538m) offers spectacular day hikes through rhododendron forests, past glacial streams and into open meadows with 360-degree Himalayan views.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Trek to Alpine Meadows above Tawang',
              description: 'Start from the road above Tawang Monastery and hike up through rhododendron and silver fir forests. March is the start of rhododendron season — expect flashes of red and pink blooms against the snow. The trail climbs to open alpine meadows at ~4,000m with unobstructed views of the Himalayan peaks.',
              details: [
                '🥾 Moderate difficulty — 8-10km round trip, 600m elevation gain',
                '🌸 March: early rhododendrons blooming, possible light snow at top',
                '🦅 Excellent raptor watching: golden eagles, bearded vultures',
                '⏰ Start by 7am — return before clouds build (usually by 1pm)',
                '🧭 Hire a local guide from Tawang town (₹600-900/day) — worth it'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Picnic in the Meadows & Return',
              description: 'Reach the high meadows by mid-morning, eat your packed lunch above the treeline with 360-degree mountain views, then descend at a relaxed pace. The afternoon return through the rhododendron forest is magical — shafts of light, bird calls and the scent of mountain herbs.',
              details: [
                '🥪 Pack a substantial lunch and extra snacks — hiking at altitude burns calories fast',
                '🔭 Bring binoculars — snowcock, impeyan pheasant and Himalayan monal may be seen',
                '🌿 The meadows have edible wild berries (check with guide before eating)'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Dragon Restaurant — Post-Hike Feast',
              description: 'After a day\'s hiking you deserve a proper spread: large bowl of thukpa (broth noodles), steamed momos, rice with pork curry and — if available — a Kingfisher beer. Dragon Restaurant is consistently the best full-meal experience in Tawang.',
              meta: '💰 $ · 📍 Dragon Restaurant, Main Bazaar'
            }
          ],
          tips: [
            { type: 'tip', text: 'High altitude hiking: pace yourself, don\'t push hard for at least the first hour. Turn back at any sign of serious altitude symptoms (confusion, severe headache, blue lips).' }
          ]
        }
      ],
      mapPins: [
        { lat: 27.6100, lng: 91.8500, label: 'Tawang Alpine Trailhead', num: 1, cat: 'attraction', desc: 'Start of the alpine meadow hike above the monastery' },
        { lat: 27.6300, lng: 91.8300, label: 'Alpine Meadow Viewpoint (~4,000m)', num: 2, cat: 'attraction', desc: 'Open meadow with 360° Himalayan views — lunch spot' },
        { lat: 27.5843, lng: 91.8659, label: 'Tawang Monastery (Below)', num: 3, cat: 'attraction', desc: 'Visible from the trail above' }
      ]
    },
    {
      num: 12,
      date: '2026-03-24',
      neighborhoods: 'Tawang · Shonga-tser Lake Area',
      title: 'Shonga-tser Lake & Buddhist Village Walk',
      description: 'A gentler day exploring Shonga-tser Lake (another beautiful high-altitude lake near Tawang), followed by a walking tour of a small local monastery village that\'s completely off most itineraries. End with a Monpa cooking experience at a local home.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shonga-tser (Madhuri) Lake Morning Walk',
              description: 'Visit Shonga-tser Lake (separate from Madhuri/Sangetsar Lake) in the morning light — this smaller lake near Tawang town rarely appears in guidebooks. Circle the lake on foot, watching for migratory birds and taking in the reflection of the mountains.',
              details: [
                '🦢 Bar-headed geese and Brahminy ducks visit in March',
                '⏰ Best light before 10am',
                '📍 Ask your driver/hotel for the exact location — it\'s local knowledge'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Local Monastery Village Walk',
              description: 'Ask your hotel or local guide to take you to one of the small namgey (monastery villages) outside Tawang town — communities of 20-30 families clustered around a small gompa. These are rarely visited and the welcome is genuine. Look for butter sculptures, hand-printing rooms and the village chorten.',
              details: [
                '🙏 Always accept the butter tea offered — it\'s ceremonially important',
                '📿 Villages often have a single local monk who will explain the monastery',
                '📸 Seek permission before photographing people'
              ]
            },
            {
              title: 'Monpa Home Cooking Experience',
              description: 'Through your guesthouse, arrange to join a local Monpa family for dinner preparation and a shared meal. Learn to make zan (buckwheat dumpling dipped in butter and cheese), thukpa broth and momos from scratch. This is the kind of experience that stays with you for years.',
              details: [
                '🍳 Many guesthouses can arrange this — ask 1-2 days in advance, budget ₹1,500-2,500 for two',
                '🥢 You\'ll cook on a wood-fired stove in a traditional Monpa kitchen',
                '🍶 Ends with homemade apong (rice wine) and conversation'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The Monpa home cooking experience is one of the hardest things to arrange spontaneously. Ask your hotel on Day 6 or 7 to set it up for tonight.' }
          ]
        }
      ],
      mapPins: [
        { lat: 27.5980, lng: 91.8800, label: 'Shonga-tser Lake', num: 1, cat: 'attraction', desc: 'Hidden lake near Tawang, rarely visited by tourists' },
        { lat: 27.5900, lng: 91.8700, label: 'Monastery Village (Local)', num: 2, cat: 'attraction', desc: 'Small namgey village — ask locally for directions' },
        { lat: 27.5859, lng: 91.8679, label: 'Monpa Home Kitchen', num: 3, cat: 'food', desc: 'Arranged cooking experience with a local family' }
      ]
    },
    {
      num: 13,
      date: '2026-03-25',
      neighborhoods: 'Tawang · Dirang',
      title: 'Farewell Tawang — Drive Back to Dirang',
      description: 'Your last morning in Tawang. One final sunrise at the monastery, a wander through the market for last-minute purchases, then begin the long drive back south toward Dirang. The journey retraces the spectacular mountain road but every viewpoint looks different in reverse.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sunrise at Tawang Monastery (Last Morning)',
              description: 'Wake before dawn for a final hour at Tawang Monastery. The monastery glows gold in early morning light, the valley below is filled with mist, and the peaks to the north are lit pink. Sit on the wall. Don\'t rush this.',
              details: [
                '🌅 Sunrise in Tawang in March: approximately 5:45am',
                '🙏 If lucky, morning horn ceremony at 6am from the monastery roof'
              ]
            },
            {
              title: 'Last Market Walk & Purchases',
              description: 'Final sweep of the Old Market and Main Bazaar for any remaining souvenirs. Stock up on Monpa butter tea powder, dried yak cheese (chhurpi), local apricot jam and prayer flags to take home.',
              details: [
                '🎁 Best gifts: Chhurpi (dried yak cheese), prayer flags, Monpa woven scarves',
                '🍵 Tawang butter tea powder — available in sealed packets at grocery stalls'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Drive Tawang to Dirang (Reverse Route)',
              description: 'The 85km drive back to Dirang takes 4-5 hours. You\'ll cross Sela Pass again — this time from north to south. Stop for chai and instant noodles at the Sela Pass army canteen (one of the highest tea stalls in India). Arrive in Dirang before dark.',
              details: [
                '☕ Sela Pass army tea stall: chai and Maggi noodles at 13,700 ft — surreal and perfect',
                '📸 The pass looks completely different in afternoon light',
                '🏔️ Check the rhododendrons again — after 8 days they may be more in bloom'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Dirang Local Dhaba',
              description: 'Back in Dirang at a lower altitude. Celebrate with a proper hot meal — rice and pork curry, fresh salad and a cold beer (easier to drink here at 1,500m).',
              meta: '💰 $ · 📍 Dirang Market'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 27.5843, lng: 91.8659, label: 'Tawang Monastery (Farewell)', num: 1, cat: 'attraction', desc: 'Final sunrise at the monastery' },
        { lat: 27.4900, lng: 92.0900, label: 'Sela Pass (Southbound)', num: 2, cat: 'attraction', desc: 'Army tea stall at the pass — chai at 13,700 ft' },
        { lat: 27.3477, lng: 92.2481, label: 'Dirang', num: 3, cat: 'attraction', desc: 'Overnight — lower altitude relief' }
      ]
    },
    {
      num: 14,
      date: '2026-03-26',
      neighborhoods: 'Dirang · Shergaon · Bomdila',
      title: 'Shergaon Village & Return to Bomdila',
      description: 'A hidden gem day: Shergaon is a tiny Sherdukpen tribal village that won the United Nations\' Best Sustainable Tourism Village award — and almost nobody has heard of it. Cool climate, ancient village monastery, fruit orchards and genuine tribal hospitality. Then move on to Bomdila for the night.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Dirang Hot Springs (Second Visit)',
              description: 'One last soak in the Dirang hot springs before the day\'s drive. After 12 nights at altitude, your muscles will thank you.',
              details: [
                '♨️ Open from 7am — get there early before other travellers',
                '⏰ 45 minutes is enough — you have a full day ahead'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shergaon Village — UN Award-Winning Sustainable Tourism',
              description: 'The Sherdukpen village of Shergaon is unlike anything else on this circuit. Neat wooden houses with carved facades, a community orchard, ancient Lhagyala Gompa, and a community museum. The villagers run the tourism themselves, meaning your money goes directly to the community.',
              details: [
                '🏆 UN Silver Award for Best Sustainable Tourism Village 2023',
                '🌿 The village has no plastic — community enforced',
                '🏛️ Lhagyala Gompa: one of the oldest monasteries in Arunachal Pradesh',
                '🎁 Buy directly from village weavers — prices set by community cooperative'
              ]
            },
            {
              title: 'Arrive Bomdila for Final Night',
              description: 'Drive from Shergaon to Bomdila (40km, 1.5 hours). Bomdila feels almost like a city after Tawang and Zemithang. Walk the market one last time, eat at the best restaurant you found on the way up, and reflect on an extraordinary journey.',
              details: []
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Best Bomdila Restaurant (Your Pick)',
              description: 'Return to your favourite Bomdila eatery from Day 2 or 3. The thukpa and fried rice here tastes better after two weeks in the mountains.',
              meta: '💰 $ · 📍 Bomdila market area'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 27.3490, lng: 92.2450, label: 'Dirang Hot Springs', num: 1, cat: 'attraction', desc: 'Final soak before the long drive home' },
        { lat: 27.1900, lng: 92.4900, label: 'Shergaon Village', num: 2, cat: 'attraction', desc: 'UN award-winning Sherdukpen tribal village' },
        { lat: 27.2644, lng: 92.4108, label: 'Bomdila', num: 3, cat: 'attraction', desc: 'Final night in the hills before the plains' }
      ]
    },
    {
      num: 15,
      date: '2026-03-27',
      neighborhoods: 'Bomdila · Bhalukpong · Tezpur',
      title: 'Descent — Through Assam Tea Country to Tezpur',
      description: 'The final day of driving: drop from the mountains through Arunachal\'s forested foothills and out onto the Assam plains. The landscape shift is dramatic — from alpine Himalayan to tropical Brahmaputra valley in a single afternoon. End the night in Tezpur, Assam\'s most charming river town.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive Bomdila to Bhalukpong',
              description: 'The descent from Bomdila is its own spectacle — the road drops 2,000 metres through progressively lusher forest, from pine to bamboo to full tropical jungle. Exit Arunachal Pradesh at Bhalukpong checkpoint (keep your ILP for stamping out).',
              details: [
                '🌿 Watch the vegetation change with altitude — botanical film in real time',
                '🛂 Exit checkpoint at Bhalukpong — surrender ILP permit copy'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tezpur — Brahmaputra Views & Ancient Temples',
              description: 'Tezpur is a pleasant Assam town on the Brahmaputra river — wide, slow and enormous. Visit the ruins of Da-Parbatia temple (6th century, extraordinary stone carvings), walk the Mahabhairab Temple ghats, and sit on the riverbank watching the world\'s largest riverine island flow by.',
              details: [
                '🏛️ Da-Parbatia ruins: 6th century Gupta-era stone carvings — genuinely stunning',
                '🌊 Brahmaputra river: 10km wide in places — stand on the bank and feel small',
                '🐘 Tezpur is the gateway to Nameri National Park — elephant country'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Tezpur Assamese Restaurant',
              description: 'After two weeks of Monpa/Tibetan food, an Assamese spread is revelatory: masor tenga (sour fish curry), khar (alkaline chicken/pork dish), bamboo shoot pickle and sticky rice. Ask the hotel to recommend the best local Assamese restaurant.',
              meta: '💰 $ · 📍 Tezpur town'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 27.0049, lng: 92.6478, label: 'Bhalukpong Exit Checkpoint', num: 1, cat: 'attraction', desc: 'Exit Arunachal Pradesh — surrender ILP' },
        { lat: 26.6335, lng: 92.7992, label: 'Tezpur', num: 2, cat: 'attraction', desc: 'Assamese river town on the Brahmaputra' },
        { lat: 26.6290, lng: 92.7940, label: 'Da-Parbatia Ruins', num: 3, cat: 'attraction', desc: '6th century Gupta-era stone temple ruins' }
      ]
    },
    {
      num: 16,
      date: '2026-03-28',
      neighborhoods: 'Tezpur · Guwahati',
      title: 'Final Day — Guwahati & Departure',
      description: 'The last morning. Drive back to Guwahati through the tea estates of Assam, stop at a working tea estate for a proper garden tour, then end with a farewell dinner on the Brahmaputra riverfront before your departing flight.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive Through Assam Tea Estates',
              description: 'The 183km drive from Tezpur to Guwahati passes through the heart of Assam\'s tea country. Ask your driver to stop at a working estate — many allow brief visits to the plucking fields and the processing house. The smell of fresh tea leaves is intoxicating.',
              details: [
                '🍵 March is the "first flush" season — premium Assam tea being harvested',
                '📸 The rolling bright-green tea gardens with the Himalayas behind',
                '🛍️ Buy fresh first-flush Assam tea directly from the estate shop'
              ]
            }
          ]
        },
        {
          label: 'Afternoon / Evening',
          activities: [
            {
              title: 'Umananda Island Temple, Guwahati',
              description: 'The world\'s smallest inhabited river island sits in the middle of the Brahmaputra in Guwahati. A short ferry ride deposits you at the ancient Umananda Shiva temple, surrounded by Assam\'s characteristic river light. The ferry trip alone is worth it.',
              details: [
                '⛴️ Ferry from Umananda Ghat — 10 minutes each way',
                '🕌 16th century Shiva temple — colourful, active, atmospheric',
                '🐒 Golden langur monkeys inhabit the island'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Paradise Restaurant or Guwahati Riverfront',
              description: 'Guwahati has a few good restaurants on the riverfront. Paradise Restaurant (a Guwahati institution) serves Assamese and Mughlai cuisine; the fish dishes are exceptional. Raise a glass to sixteen extraordinary days in the Himalayas.',
              meta: '💰 $-$$ · 📍 Guwahati riverfront area'
            }
          ],
          tips: [
            { type: 'tip', text: 'Guwahati Airport (GAU) has flights to Delhi, Mumbai and major Indian cities. Book your onward connection home from Guwahati — flights fill up fast during peak season.' }
          ]
        }
      ],
      mapPins: [
        { lat: 26.1700, lng: 91.7500, label: 'Assam Tea Estate (en route)', num: 1, cat: 'attraction', desc: 'First-flush Assam tea in March — visit the plucking fields' },
        { lat: 26.1855, lng: 91.7524, label: 'Umananda Island Temple', num: 2, cat: 'attraction', desc: 'World\'s smallest inhabited river island with Shiva temple' },
        { lat: 26.1445, lng: 91.7362, label: 'Guwahati Airport', num: 3, cat: 'attraction', desc: 'Departure — your Himalayan adventure complete' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (per night, 2 sharing)', budget: '₹800-1,500 ($10-18)', midrange: '₹1,500-3,000 ($18-36)', luxury: '₹3,000-6,000 ($36-72)' },
    { category: 'Meals (per couple/day)', budget: '₹400-800 ($5-10)', midrange: '₹800-1,500 ($10-18)', luxury: '₹1,500-3,000 ($18-36)' },
    { category: 'Private Car (per day)', budget: '₹2,500 (shared sumo)', midrange: '₹3,000-4,000 (private)', luxury: '₹5,000+ (4WD)' },
    { category: 'Inner Line Permit', budget: 'Free (Indian nationals)', midrange: '₹2,000 ($24) for foreigners', luxury: 'Same' },
    { category: 'Bumla Pass PAP', budget: '₹500-1,000 (via operator)', midrange: 'Same', luxury: 'Same' },
    { category: '16-Day Total (couple)', budget: '$600-900', midrange: '$900-1,600', luxury: '$1,600-2,500' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly to Guwahati (GAU) — hub for all northeast India', 'Nearest airport to Tawang: Tezpur (VETZ) — reduces driving by ~2 hours', 'No direct flights to Tawang; all arrivals by road', 'Alternative: Assam Rail to Rangapara North, then drive'] },
    { title: '📜 Permits', items: ['Inner Line Permit (ILP): apply at arunachalilp.com (free for Indians; ₹100 for foreigners)', 'Foreign nationals: also need Protected Area Permit (PAP) from Ministry of Home Affairs', 'Bumla Pass extra PAP: arrange via registered Arunachal tour operator in advance', 'Keep multiple printed copies + digital photos of all permits'] },
    { title: '🏨 Where to Stay in Tawang', items: ['Hotel Tawang Heights — best midrange option, central', 'Hotel Mon Regency — good value, helpful staff', 'Pemaling Lodge — basic but run by local family', 'Circuit House (government) — advance booking required, basic but comfortable', 'Budget guesthouses in Main Bazaar from ₹500/night ($6)'] },
    { title: '🌡️ March Weather', items: ['Tawang town: 5-18°C days, -2 to -5°C nights', 'Sela Pass: -5 to 8°C, may have snow on road', 'Bumla Pass: -10 to 2°C, always bring full winter gear', 'Lower valleys (Bomdila, Dirang): 10-22°C — much warmer', 'March has occasional snowfall at passes — roads usually passable but check conditions'] },
    { title: '📱 Connectivity', items: ['BSNL is the only network with coverage across most of Arunachal Pradesh — buy a BSNL SIM', 'No signal at passes, Zemithang or remote valleys — inform family before you go off-grid', 'WhatsApp works in Tawang town, Bomdila and Dirang on BSNL', 'Carry an offline map (Maps.me or OsmAnd with Arunachal downloaded)'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
