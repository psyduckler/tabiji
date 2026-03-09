const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772711881472_k9fn99',
  email: 'galaxycats510@gmail.com',
  destination: 'Kamakura & Enoshima, Japan',
  startDate: '2026-03-15',
  endDate: '2026-03-15',
  groupSize: '3-4',
  requests: 'Day trip from Shibamata, Tokyo. Kamakurakokomae (Slam Dunk crossing), Mt Fuji view from Enoshima, catch sunset in Enoshima.'
};

const itineraryData = {
  destination: 'Kamakura & Enoshima, Japan',
  countryEmoji: '🇯🇵',
  title: 'Samurai Coast & Island Sunsets',
  subtitle: 'A perfect day trip from Shibamata — ancient temples, the Slam Dunk crossing & a golden sunset over Mt Fuji',
  description: "This is one of Japan's greatest day trips. You'll leave the quiet streets of Shibamata early, ride into Kamakura to stand before the Great Buddha and wander sacred temple paths, then board the legendary Enoden coastal tram to Kamakurakokomae — where the sea, the crossing gate, and Enoshima Island frame the most iconic train-station photo in Japan. From there, the road leads to Enoshima itself: a small island packed with shrines, sea caves, and — on a clear March day — a perfect silhouette of Mt Fuji floating above the Pacific. Time it right and you'll watch the sun set directly behind the mountain. Pure magic.",
  duration: '1 day',
  dates: 'Mar 15, 2026',
  budget: '$$',
  pace: 'Active',
  bestFor: 'Groups of 3–4',
  highlights: [
    'The Great Buddha of Kamakura — 13.35 metres of serene bronze majesty',
    'Tsurugaoka Hachimangu — Kamakura\'s grand hilltop shrine with cherry blossom approach',
    'Kamakurakokomae Station — the iconic Slam Dunk anime crossing with ocean backdrop',
    'Sea Candle observation deck — Mt Fuji silhouetted against the Pacific on a clear day',
    'Sunset over the sea at Enoshima — one of Japan\'s Three Views of the Moon',
    'Shirasu (whitebait) bowls — the fresh local speciality you can only get here'
  ],

  essentials: [
    {
      title: '🚆 Getting There from Shibamata',
      text: 'From Shibamata Station (Keisei Kanamachi Line), take the train one stop to Keisei-Kanamachi, then transfer to the JR Joban Line to Shin-Koiwa or Tokyo Station. From Tokyo Station, board the JR Yokosuka Line directly to Kamakura (about 55 min). Total journey: roughly 1h 45min. IC card (Suica/Pasmo) covers the whole route — no need for separate tickets. Depart by 7:00 AM to maximize your day.'
    },
    {
      title: '🚋 The Enoden — Japan\'s Coastal Tram',
      text: 'The Enoshima Electric Railway (Enoden) is a single-track tram that winds between Kamakura and Fujisawa along the coast. It\'s slow by design — 34 minutes end to end — and utterly charming. Sit on the left (sea-side) between Kamakura and Kamakurakokomae for ocean views. A one-day Enoden pass (¥700) is worth it if you ride more than twice. Buy from vending machines at any Enoden station.'
    },
    {
      title: '🗻 Mt Fuji Viewing Conditions',
      text: 'Mid-March is prime Fuji-viewing season: the air is still cool and crisp, humidity is low, and Fuji is fully snow-capped. Best visibility is in the morning and again around sunset. From the Sea Candle observation deck (Enoshima Tower), you\'ll see Fuji to the northwest on a clear day — a breathtaking sight across the water. The view from Chigogafuchi (the rocky shore on Enoshima\'s west side) is equally spectacular. Check conditions the morning of your visit via Yahoo! Japan Weather.'
    },
    {
      title: '🌅 Sunset & Timing',
      text: 'Sunset on March 15 in Kamakura/Enoshima is at approximately 5:50 PM. Plan to be at Chigogafuchi or on the western shore of Enoshima by 5:20 PM. In mid-March, Mt Fuji and the setting sun align nearly perfectly when viewed from Enoshima\'s western shore — this is called "Diamond Fuji" and while the exact date shifts yearly, mid-March often comes close. Check the Enoshima Tourism Board for the exact date near your visit.'
    },
    {
      title: '🍜 Shirasu — The Local Obsession',
      text: 'Shirasu are tiny whitebait (baby anchovies) harvested fresh from Sagami Bay. Kamakura and Enoshima are the best places in Japan to eat them. In spring, fresh (nama) shirasu are served atop bowls of rice — slightly translucent, lightly briny, and delicious. Elsewhere you\'ll get kama-age (briefly blanched) or dried shirasu. Either way, have at least one shirasu don (bowl) during the day.'
    },
    {
      title: '💴 Money & Budget',
      text: 'Most shops and restaurants accept IC cards and credit cards now, but carry ¥2,000–3,000 cash for smaller spots, the cave entry fees, and any street food. A comfortable day budget per person: ¥4,000–6,000 (transport + meals + Sea Candle entry). The Sea Candle tower (Samuel Cocking Garden entry included) costs ¥500 for the garden + ¥500 for the observation deck.'
    }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-15',
      neighborhoods: 'Shibamata → Kamakura → Kamakurakokomae → Enoshima',
      title: 'Kamakura Temples, the Slam Dunk Crossing & Enoshima Sunset',
      description: 'A full day along Japan\'s samurai coast — starting before the crowds arrive in Kamakura, riding the legendary Enoden tram, pausing at the Slam Dunk crossing, and ending with Mt Fuji painted gold by the setting sun from Enoshima island.',
      timeBlocks: [
        {
          label: '7:00 AM — Depart Shibamata',
          activities: [
            {
              title: 'Early Departure from Shibamata',
              description: 'Leave Shibamata Station by 7:00 AM sharp. The Keisei Kanamachi Line takes you one stop to Keisei-Kanamachi. Transfer to JR Joban Line → Tokyo Station, then board the JR Yokosuka Line bound for Kurihama or Zushi. Stay on until Kamakura Station. The trains are comfortable and early departures are quiet.',
              details: [
                '🚆 Shibamata → Keisei-Kanamachi (Keisei Kanamachi Line, 1 stop)',
                '🚆 Keisei-Kanamachi → Tokyo (JR Joban Line, ~30 min)',
                '🚆 Tokyo → Kamakura (JR Yokosuka Line, ~55 min)',
                '💳 Use Suica/Pasmo IC card throughout — no need to buy separate tickets',
                '⏱️ Total journey: approximately 1h 45min',
                '🛍️ Grab a convenience store onigiri or coffee at Tokyo Station for the ride'
              ]
            }
          ]
        },
        {
          label: '8:50 AM — Kamakura Arrival & Tsurugaoka Hachimangu',
          activities: [
            {
              title: 'Tsurugaoka Hachimangu Shrine',
              description: 'Kamakura\'s most important shrine sits at the end of the Wakamiya Oji approach — a grand boulevard lined with cherry trees (in early bloom in mid-March). Walk the entire approach from Dankazura (the raised central path flanked by ponds) to the main hall at the top of the stone steps. In early morning you\'ll have it nearly to yourself.',
              details: [
                '📍 5-minute walk from Kamakura Station (east exit)',
                '⛩️ Founded in 1063 — the spiritual heart of Kamakura',
                '🌸 Mid-March: early cherry blossoms often visible along the approach',
                '🕗 Open from 6:00 AM — best before 9:30 AM while crowds are thin',
                '💰 Free entry to the main shrine grounds'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Look back from the top of the main shrine steps for a magnificent view down the Dankazura approach toward Kamakura Station. Spectacular framing for photos.' }
          ]
        },
        {
          label: '9:45 AM — Komachi-dori Street',
          activities: [
            {
              title: 'Komachi-dori — Kamakura\'s Beloved Shopping Street',
              description: 'Walk back toward the station along Komachi-dori, Kamakura\'s lively covered shopping street. It\'s lined with pottery shops, matcha soft-serve stalls, sembei (rice cracker) shops, and local confectioneries. Perfect for picking up a morning snack and some gifts to take home.',
              details: [
                '📍 Runs west from Tsurugaoka Hachimangu toward Kamakura Station',
                '🍡 Try: kuzu-mochi (chewy starch cakes with black syrup), or matcha soft-serve',
                '🎁 Great for pottery, tenugui (printed cotton cloths), and local sweets',
                '⏱️ Allow 20–30 minutes to browse at leisure'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Coffee & Snack',
              name: 'Kamakura Station Area',
              description: 'Grab a light snack on Komachi-dori before heading to the Great Buddha. Many shops open by 9:30 AM. Look for hot mitarashi dango (rice dumplings with sweet soy glaze) — fresh, warm, and filling.',
              meta: '💰 ¥200–400 · 📍 Komachi-dori, Kamakura'
            }
          ]
        },
        {
          label: '10:15 AM — Great Buddha (Kotoku-in)',
          activities: [
            {
              title: 'Kotoku-in Daibutsu — The Great Buddha of Kamakura',
              description: 'Take bus #4 from Kamakura Station (Hase stop, ~15 min) to reach Kotoku-in, home of the Kamakura Daibutsu — the second-largest bronze Buddha statue in Japan at 13.35 metres tall. Cast in 1252, the Buddha sits in the open air after his temple hall was swept away by a tsunami in 1498, and the serene expression on his face is genuinely moving. You can go inside the statue for an extra ¥20.',
              details: [
                '🚌 Bus #4 or #7 from Kamakura Station (platform 1), get off at Daibutsu-mae (~15 min)',
                '⏱️ Or walk the scenic Daibutsu Hiking Trail (~50 min) if energy allows',
                '💰 Entry: ¥300 per person; inside the statue: additional ¥20',
                '🕙 Open 8:00 AM – 5:30 PM (last entry 5:00 PM)',
                '📸 Best photos: arrive early before tour groups arrive',
                '👜 No backpacks allowed inside the statue (lockers available)'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The Buddha\'s ears are 1.9 metres long. Stand close and look up — the scale is genuinely humbling in a way photos don\'t convey.' }
          ]
        },
        {
          label: '11:30 AM — Hase-dera Temple',
          activities: [
            {
              title: 'Hase-dera — Gardens, Ocean Views & Kannon',
              description: 'Just a 10-minute walk from the Great Buddha, Hase-dera is one of Kamakura\'s most beautiful temples. The complex climbs a hillside with a carved 9.18-metre Kannon (Goddess of Mercy) as its centrepiece, surrounded by blooming plum and early cherry trees in March. The upper terrace offers one of the finest views of Kamakura and the Pacific.',
              details: [
                '📍 2-3 min walk from Daibutsu-mae bus stop (or 10 min walk from Kotoku-in)',
                '💰 Entry: ¥400 per person',
                '🕙 Open 8:00 AM – 5:30 PM',
                '🌸 Mid-March: plum blossoms at peak, early cherry blossoms beginning',
                '📸 View from the upper terrace: ocean, town, and hills — stunning framing'
              ]
            }
          ]
        },
        {
          label: '12:30 PM — Lunch in Hase',
          activities: [],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Shirasu Hut (Komachi-dori or Hase area)',
              description: 'Head back toward Kamakura or stay in the Hase area for a proper shirasu don (whitebait rice bowl). In spring, look for fresh "nama shirasu" — barely-blanched whitebait that\'s almost translucent and briny-sweet. Many small restaurants on Komachi-dori and around Hase station serve this. Pairs perfectly with miso soup and pickles.',
              meta: '💰 ¥800–1,500 · 📍 Komachi-dori or near Hase Station (Enoden)'
            }
          ],
          tips: [
            { type: 'tip', text: 'Shirasu availability depends on fishing season. Mid-March often still has fresh (nama) shirasu — ask before ordering. If unavailable, kama-age (hot blanched) is equally delicious.' }
          ]
        },
        {
          label: '1:15 PM — Board Enoden to Kamakurakokomae',
          activities: [
            {
              title: 'Enoshima Electric Railway (Enoden)',
              description: 'Board the Enoden from Kamakura Station (or Hase Station) heading toward Fujisawa. This charming single-track tram threads through residential streets, past gardens, and along the Pacific coast. Sit on the left side of the car heading west for the ocean views.',
              details: [
                '🚋 Board at Kamakura Station (Enoden platform) or Hase Station',
                '🎫 Buy an Enoden day pass (¥700) at the ticket machine — valid all day',
                '⏱️ Kamakura → Kamakurakokomae: ~25 minutes',
                '🌊 Look left after Shichirigahama station — the open Pacific appears',
                '📸 The moment the tram rounds the curve and the coast appears is pure joy'
              ]
            }
          ]
        },
        {
          label: '1:40 PM — Kamakurakokomae (Slam Dunk Crossing)',
          activities: [
            {
              title: 'The Slam Dunk Crossing — Kamakurakokomae Station',
              description: 'This is THE photo stop of the trip. Kamakurakokomae Station became a pilgrimage site for anime fans worldwide after the Slam Dunk manga/film used its level crossing as a recurring backdrop — Enoshima island visible in the distance across the sea. But even non-anime fans are blown away: stand at the crossing gate as the Enoden tram passes, Enoshima floating on the horizon, and Sagami Bay stretching endlessly. It\'s legitimately one of the most beautiful train-station views in the world.',
              details: [
                '📍 Exit Kamakurakokomae Station, cross to the level crossing immediately outside',
                '📸 Frame the shot: crossing gate + Enoden tram (approaching from Kamakura) + sea + Enoshima island in distance',
                '⏱️ Enoden comes every 10–12 minutes — time it for the tram passing the crossing',
                '🎌 Slam Dunk fans: the exact spot from the OP/film is right at the crossing',
                '🌊 The beach right below the station is Shichiri-ga-hama — great for a quick walk'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'To get the tram-in-frame shot, stand on the sea side of the crossing and face northeast (toward Kamakura). The tram will approach from that direction. Trains run approximately every 10 minutes — you won\'t wait long.' }
          ]
        },
        {
          label: '2:15 PM — Enoden to Enoshima Station & Island Entry',
          activities: [
            {
              title: 'Board Enoden to Enoshima',
              description: 'Re-board the Enoden from Kamakurakokomae and ride three more stops to Enoshima Station (or continue to Katase-Enoshima on the Odakyu Line — same island). From the station, it\'s a 10-minute walk across the Benten Bridge causeway to Enoshima island.',
              details: [
                '🚋 Kamakurakokomae → Enoshima Station: ~12 minutes',
                '🚶 Walk from station to island entrance: ~10 min along Benten Bridge',
                '🌊 The bridge walk gives you a great view of Enoshima island ahead and Mt Fuji behind (look northwest on a clear day)',
                '📍 Enoshima is connected to the mainland by a 600-metre causeway — walkable'
              ]
            },
            {
              title: 'Enoshima Shrine (Enoshima Jinja)',
              description: 'The island\'s main shrine complex is dedicated to Benzaiten (goddess of music, art, and the sea). A covered shopping street called Nakamise-dori leads uphill from the island\'s gate, lined with shirasu shops and seafood restaurants. The shrines are nestled in three connected pavilions as you climb — each with beautiful details and ocean views.',
              details: [
                '⛩️ Three shrines: Hetsunomiya, Nakatsunomiya, and Okutsunomiya',
                '💰 Shrine grounds: free; inner sanctuary (Benzaiten Hall): ¥200',
                '🚡 Enoshima Escar (outdoor escalator): ¥360 up / free down — skip the steep stairs',
                '🐢 Look for the giant sea turtle tank near the shrine approach',
                '📸 The torii gates framing the ocean as you look back are beautiful'
              ]
            }
          ]
        },
        {
          label: '3:30 PM — Sea Candle & Mt Fuji View',
          activities: [
            {
              title: 'Samuel Cocking Garden & Sea Candle Lighthouse Tower',
              description: 'The Samuel Cocking Garden is a beautifully maintained botanical garden near the island\'s summit, surrounding the Sea Candle — a 59.8-metre lighthouse tower with an observation deck. On a clear March day, the view from the top is extraordinary: Sagami Bay spread below, the Izu Peninsula to the south, the Boso Peninsula to the east, and — most dramatically — the perfect snow-capped cone of Mt Fuji to the northwest. This is your prime Mt Fuji viewing moment.',
              details: [
                '🗼 Sea Candle Tower: observation deck at ~100m elevation above sea level',
                '💰 Garden + Tower combo: ¥500 (garden) + ¥500 (tower observation) = ¥1,000 per person',
                '🕙 Open until 8:00 PM (last entry 7:30 PM) — good for sunset too',
                '🗻 Mt Fuji view: look northwest from the observation deck — clearest before 5 PM',
                '📸 Best Mt Fuji shot: zoom toward the northwest quadrant, Fuji floats above the hills of Hakone',
                '🌸 Mid-March: early cherry blossoms and winter flowers in the garden below'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'If Mt Fuji is visible, take the photo from the northwest-facing side of the observation deck. In the late afternoon, the snow cap catches warm light. After sunset the tower illuminates — beautiful but Fuji will be less visible. Prioritize the Fuji shot before sunset.' }
          ]
        },
        {
          label: '4:30 PM — Iwaya Caves & West Shore Walk',
          activities: [
            {
              title: 'Iwaya Sea Caves',
              description: 'Descend from the Sea Candle to the island\'s western tip, where the Iwaya caves cut deep into the volcanic rock. These natural sea caves have been sacred for over 1,000 years — candles illuminate the passage, stone Buddhas line the walls, and the sound of the sea echoes through the tunnels. The cave path loops through two chambers connected by narrow passages.',
              details: [
                '💰 Entry: ¥500 per person; includes a candle',
                '🕙 Open 9:00 AM – 5:00 PM (last entry 4:30 PM) — arrive by 4:15 PM',
                '⚠️ Tight passages — not suitable for those with severe claustrophobia',
                '📿 Over 150 small stone statues line the cave walls',
                '⏱️ Allow 30–40 minutes for the full cave loop'
              ]
            },
            {
              title: 'Chigogafuchi — West Shore Sunset Spot',
              description: 'After the caves, make your way to Chigogafuchi — the rocky coastline on Enoshima\'s western shore. This is the best sunset viewing spot on the island: low rock platforms extend into the sea, the horizon is wide open to the west, and on clear days Mt Fuji looms large to the northwest as the sky turns orange and pink. Find your spot on the rocks early — others will have the same idea.',
              details: [
                '📍 On the western side of the island, below and beyond Okutsunomiya shrine',
                '🗻 Mt Fuji visible to the northwest — the low horizon angle makes it dramatic',
                '🌅 March 15 sunset: approximately 5:50 PM',
                '⚠️ The rocks can be slippery — wear shoes with grip, watch the tide',
                '📸 Best sunset composition: low angle on the rocks with Fuji silhouetted to the right of the sun'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The timing here matters: finish the caves by 4:50 PM, then walk directly to Chigogafuchi. Arrive 30+ minutes before sunset (5:20 PM latest) to find a good spot before it fills up.' }
          ]
        },
        {
          label: '5:20 PM — Sunset at Chigogafuchi',
          activities: [
            {
              title: 'Watching the Sun Set Over Sagami Bay',
              description: 'This is what you came for. Settle onto the rocks at Chigogafuchi as the sky begins to change. The Pacific stretches to the southwest, the hills of the Miura Peninsula frame the right, and Mt Fuji — snow-white and massive — stands sentinel to the northwest. As the sun drops, the mountain turns from white to pale rose to deep purple. On the clearest evenings, the last light catches the summit snow in shades of red and gold.',
              details: [
                '🌅 Sunset: ~5:50 PM on March 15',
                '🗻 Best Fuji light: 20–30 minutes before sunset when the snow cap turns pink',
                '📸 Shoot in burst mode as the light changes rapidly in the final 15 minutes',
                '🌊 The waves on the rocks add natural foreground texture and sound',
                '🥶 March evenings cool quickly — have a layer ready for after sunset'
              ]
            }
          ]
        },
        {
          label: '6:15 PM — Dinner on the Island',
          activities: [],
          meals: [
            {
              type: '🍣 Dinner',
              name: 'Nakamise-dori Seafood Restaurant (Enoshima)',
              description: 'Enoshima\'s covered shopping street (Nakamise-dori) has several casual seafood restaurants that stay open into the evening. Order the local speciality: seafood grilled on the spot (sazae/turban shell with butter, shrimp, squid) with rice, miso soup, and of course a shirasu dish. Casual, delicious, and you\'re eating fresh Sagami Bay seafood minutes after sunset.',
              meta: '💰 ¥1,500–2,500 per person · 📍 Nakamise-dori, Enoshima'
            }
          ],
          tips: [
            { type: 'tip', text: 'Look for restaurants displaying fresh sazae (turban shells) — these are filled with butter, sake, and soy sauce then grilled on a little grill at the table. One of the great simple pleasures of Enoshima.' }
          ]
        },
        {
          label: '7:30 PM — Return to Shibamata',
          activities: [
            {
              title: 'Return Journey to Shibamata',
              description: 'From Enoshima Station (Enoden), take the tram back to Kamakura Station, then reverse the morning route: JR Yokosuka Line to Tokyo Station, then JR Joban Line to Keisei-Kanamachi, and one stop to Shibamata. It\'s a relaxed train ride — you\'ll be tired but deeply satisfied.',
              details: [
                '🚋 Enoshima → Kamakura (Enoden): ~34 minutes',
                '🚆 Kamakura → Tokyo (JR Yokosuka Line): ~55 minutes',
                '🚆 Tokyo → Keisei-Kanamachi → Shibamata: ~35 minutes',
                '⏱️ Total return journey: approximately 2h',
                '🏠 Expected arrival in Shibamata: ~9:30–10:00 PM depending on connections',
                '💤 Sleep well — you earned it'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7740, lng: 139.8685, label: 'Shibamata Station', num: 1, cat: 'attraction', desc: 'Departure point — Keisei Kanamachi Line' },
        { lat: 35.3197, lng: 139.5509, label: 'Kamakura Station', num: 2, cat: 'attraction', desc: 'JR Yokosuka Line arrival — start of the day' },
        { lat: 35.3263, lng: 139.5560, label: 'Tsurugaoka Hachimangu', num: 3, cat: 'attraction', desc: 'Kamakura\'s grand Shinto shrine, founded 1063' },
        { lat: 35.3277, lng: 139.5543, label: 'Komachi-dori', num: 4, cat: 'attraction', desc: 'Kamakura\'s beloved shopping and food street' },
        { lat: 35.3167, lng: 139.5353, label: 'Kotoku-in (Great Buddha)', num: 5, cat: 'attraction', desc: 'The iconic 13.35m bronze Great Buddha, cast 1252' },
        { lat: 35.3180, lng: 139.5342, label: 'Hase-dera Temple', num: 6, cat: 'attraction', desc: 'Hilltop temple with giant Kannon and Pacific views' },
        { lat: 35.3183, lng: 139.5255, label: 'Hase Station (Enoden)', num: 7, cat: 'attraction', desc: 'Board the Enoden tram toward Kamakurakokomae' },
        { lat: 35.3103, lng: 139.4952, label: 'Kamakurakokomae Station', num: 8, cat: 'attraction', desc: 'The Slam Dunk anime crossing — Enoshima on the horizon' },
        { lat: 35.3010, lng: 139.4845, label: 'Shichirigahama Beach', num: 9, cat: 'attraction', desc: 'Stretch of coast below Kamakurakokomae with ocean views' },
        { lat: 35.2997, lng: 139.4838, label: 'Enoshima Station (Enoden)', num: 10, cat: 'attraction', desc: 'Enoden terminus, 10-min walk to island entrance' },
        { lat: 35.3013, lng: 139.4797, label: 'Enoshima Island Entrance', num: 11, cat: 'attraction', desc: 'Benten Bridge causeway — start of the island walk' },
        { lat: 35.3002, lng: 139.4782, label: 'Enoshima Jinja (Shrine)', num: 12, cat: 'attraction', desc: 'Three-pavilion shrine to Benzaiten, goddess of the sea' },
        { lat: 35.2993, lng: 139.4780, label: 'Samuel Cocking Garden & Sea Candle', num: 13, cat: 'attraction', desc: 'Observation tower — best Mt Fuji views from Enoshima' },
        { lat: 35.2980, lng: 139.4760, label: 'Iwaya Sea Caves', num: 14, cat: 'attraction', desc: '1,000-year-old sacred sea caves lit by candlelight' },
        { lat: 35.2975, lng: 139.4748, label: 'Chigogafuchi (Sunset Spot)', num: 15, cat: 'attraction', desc: 'Rocky west shore — best sunset & Mt Fuji silhouette view' },
        { lat: 35.3005, lng: 139.4790, label: 'Nakamise-dori Seafood Restaurants', num: 16, cat: 'food', desc: 'Casual grilled seafood & shirasu bowls on the island' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Transport (round trip)', budget: '¥2,200–2,800', midrange: '¥2,500–3,200', luxury: '¥5,000+ (taxi)' },
    { category: 'Kamakura entries', budget: '¥700 (Buddha + Hase-dera)', midrange: '¥700', luxury: '¥700' },
    { category: 'Enoshima entries', budget: '¥1,500 (Sea Candle + caves)', midrange: '¥1,500', luxury: '¥1,500' },
    { category: 'Meals (all day)', budget: '¥2,000–3,000', midrange: '¥3,000–5,000', luxury: '¥6,000+' },
    { category: 'Day total per person', budget: '¥6,400–8,000', midrange: '¥7,700–10,400', luxury: '¥13,000+' }
  ],

  practicalInfo: [
    {
      title: '📍 Getting to Shibamata',
      items: [
        'Shibamata Station is on the Keisei Kanamachi Line (eastern Tokyo)',
        'Known for Taishakuten Temple and the Tora-san film series',
        'From central Tokyo (Shinjuku/Tokyo), reach via subway + transfer'
      ]
    },
    {
      title: '🗓️ Best Season',
      items: [
        'Mid-March: cherry blossoms just beginning (Kamakura is excellent for early sakura)',
        'Mt Fuji still fully snow-capped — prime viewing season',
        'Cool and crisp: ideal for long walking days',
        'Avoid Golden Week (late April–May) — extremely crowded'
      ]
    },
    {
      title: '👟 What to Wear',
      items: [
        'Comfortable walking shoes — you\'ll cover 10–15km on foot',
        'Layers: morning is cool (~8°C), afternoon warms to 13–16°C, evenings cool fast',
        'Light jacket for the Enoshima cliffs at sunset',
        'Waterproof shoes helpful — sea spray at Chigogafuchi'
      ]
    },
    {
      title: '📱 Useful Apps',
      items: [
        'Google Maps / Yahoo! Japan乗換 for train transfers',
        'Yahoo! Japan Weather for Mt Fuji visibility forecast',
        'Tabelog for restaurant reviews',
        'Enoden app for tram schedules (search: 江ノ電)'
      ]
    },
    {
      title: '⚠️ Watch Out For',
      items: [
        'Enoden is often crowded on weekends — Mon–Fri is much calmer',
        'The crossing at Kamakurakokomae draws crowds — be patient and respectful',
        'Iwaya caves close at 4:30 PM for last entry — don\'t linger too long at the Sea Candle',
        'Enoshima can be foggy in the morning — Mt Fuji views improve through the day',
        'Chigogafuchi rocks are slippery — no running or going beyond the barriers'
      ]
    }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
