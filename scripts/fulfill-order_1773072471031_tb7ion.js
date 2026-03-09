const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1773072471031_tb7ion',
  email: 'abc@yahoo.com',
  destination: 'Osaka, Japan',
  startDate: '2026-04-03',
  endDate: '2026-04-06',
  groupSize: 1,
  style: 'Cultural, Foodie, Relaxation, Nightlife',
  dining: 'Mix of everything',
  budget: 'Under $1,000',
  requests: ''
};

const itineraryData = {
  destination: 'Osaka, Japan',
  countryEmoji: '🇯🇵',
  title: "Osaka: Japan's Kitchen, Neon & Soul",
  subtitle: '4 days of street food feasts, ancient castles, onsen soaks & electric nightlife — solo style',
  description: "Osaka punches harder than any city its size. Known as \"tenka no daidokoro\" — the nation's kitchen — it feeds you from morning street stalls to midnight ramen counters without pause. This solo itinerary moves through glowing Dotonbori canals, samurai castle grounds dusted with late cherry blossoms, crammed izakaya alleys, and throbbing nightlife districts where the drinks flow and strangers become friends. April is the sweet spot: spring warmth, lingering sakura, and a city fully awake after winter.",
  duration: '3 nights',
  dates: 'Apr 3 – Apr 6, 2026',
  budget: '$',
  pace: 'Moderate',
  bestFor: 'Solo Travelers',
  highlights: [
    'Late-night street food crawl through Dotonbori — takoyaki, okonomiyaki, kushikatsu',
    'Osaka Castle with the last cherry blossoms of the season',
    'Kuromon Ichiba Market — Osaka\'s 200-year-old kitchen at its finest',
    'Kushikatsu dinner in Shinsekai under Tsutenkaku Tower',
    'Namba nightlife: jazz bars, izakayas, karaoke at 2am',
    'Amerika-mura vintage shopping and hidden cafe culture',
    'Spa World soak — Osaka\'s legendary onsen complex'
  ],

  essentials: [
    { title: '🌸 April in Osaka', text: 'Early April brings the tail end of cherry blossom season — Osaka Castle Park is spectacular. Expect 15–20°C days, light jacket evenings. Crowds thin mid-week but Dotonbori is always buzzing.' },
    { title: '🚇 Getting Around', text: 'The Osaka Metro is fast, cheap, and covers everything. Get an IC card (Suica or ICOCA) at the airport or any metro station — tap on/off everywhere. Day passes available. Most key spots in Namba/Shinsaibashi are walkable from each other.' },
    { title: '💴 Cash vs Card', text: 'Japan is still cash-heavy. Withdraw yen from 7-Eleven or Japan Post ATMs (international cards accepted). Street food and small izakayas are cash-only. Budget ¥5,000–8,000/day for food + activities as a solo traveler.' },
    { title: '🍣 Osaka Food Rules', text: 'Eat where the locals eat: countertop ramen bars, standing sushi, basement food halls (depachika). The golden rule: if there\'s a queue of salarymen at lunch, join it. Never turn down a free sample at Kuromon Market.' },
    { title: '🌙 Solo Nightlife Tips', text: 'Osaka\'s nightlife is incredibly welcoming to solos. Counter seating at izakayas means you\'ll chat with neighbors easily. Namba and Shinsaibashi stay alive until 4–5am on weekends. For the brave: Golden-Gai style tiny bars in Namba Parks area.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-04-03',
      neighborhoods: 'Namba · Dotonbori · Hozenji Yokocho',
      title: 'Arrive & Eat Everything in Sight',
      description: "Your introduction to Osaka is served on a stick. Drop your bags and dive straight into Dotonbori — the world's most photogenic food street. Tonight is for wandering, grazing, and letting the city hit you with its full neon-and-aroma assault.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In & First Walk',
              description: "Check into your accommodation in the Namba area — ground zero for everything. Do a first walk down Dotonbori canal to get your bearings: the giant Glico Running Man sign, the mechanical crab of Kani Doraku, and the wall of smells from a hundred food stalls.",
              details: [
                '🏨 Stay in Namba or Shinsaibashi for maximum walkability',
                '📍 Dotonbori starts right at Ebisubashi Bridge — begin here',
                '🦀 Kani Doraku (giant moving crab sign) — the ultimate Osaka photo op',
                '🌸 Walk the canal — the cherry trees may still have late blossoms'
              ]
            },
            {
              title: 'Kuromon Ichiba Market',
              description: "Osaka's 200-year-old covered market is an afternoon must-do. The stalls sell fresh tuna, live shellfish, Kobe beef skewers, king crab legs, tamagoyaki, and every Osaka specialty you can name. Graze your way through — this is not a shopping trip, it's a tasting menu.",
              details: [
                '🦞 Try: fresh uni (sea urchin) on rice, grilled scallops, tuna sashimi skewers',
                '🥩 Kobe beef skewer stalls — expensive but worth it (¥2,000–3,000)',
                '🍳 Tamagoyaki (sweet rolled egg) shops — buy one to snack on',
                '⏰ Opens 8am–6pm, best visited 11am–3pm',
                '📍 Kuromon Ichiba, Nipponbashi — 5 min walk from Namba'
              ]
            }
          ],
          meals: [
            {
              type: '🍢 Afternoon Snack',
              name: 'Kuromon Market Stalls',
              description: 'Graze through market stalls — fresh seafood on skewers, oysters, tamagoyaki. Budget ¥1,500–2,500 for a generous snack crawl.',
              meta: '💰 ¥500–800/item · 📍 Kuromon Ichiba Market, Nipponbashi'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dotonbori Street Food Crawl',
              description: "The essential Osaka experience. Start at Ebisubashi Bridge and work your way west, tasting from every vendor that catches your eye. Takoyaki at Wanaka, crispy okonomiyaki at Fukutaro, fresh crab at a street stall. The crowds thin slightly after 9pm — but the food keeps coming till midnight.",
              details: [
                '🐙 Takoyaki: Wanaka (長堀橋店) — the gold standard, ¥600 for 8 balls',
                '🥞 Okonomiyaki: Mizuno (道頓堀) — savory pancake legend since 1945',
                '🍡 Ikayaki (grilled squid): look for the smoky grills on Dotonbori itself',
                '📸 Best photo: facing the Glico sign from Ebisubashi Bridge at night'
              ]
            },
            {
              title: 'Hozenji Yokocho Alley',
              description: "Duck off Dotonbori into Hozenji Yokocho — a narrow stone alley with moss-covered Fudo-Myoo shrine and tiny old-school restaurants packed with locals. One of Osaka's most atmospheric spots. Buy incense, pray, then eat next door.",
              details: [
                '⛩️ Hozenji Temple — wash the mossy Fudo-Myoo statue for good luck',
                '🍶 The alley has 50+ tiny restaurants in just 80 meters',
                '📍 Behind the main Dotonbori strip, near Namba Grand Kagetsu theater'
              ]
            }
          ],
          meals: [
            {
              type: '🍺 Dinner',
              name: 'Kuidaore Taro Building Area',
              description: "Eat like an Osakan: no single restaurant, just move from stall to bar to counter. Land eventually at a ramen counter — Kinryu Ramen on Dotonbori is open 24 hours. Dragon statues outside, tonkotsu inside.",
              meta: '💰 ¥800–1,500/dish · 📍 Dotonbori / Hozenji Yokocho strip'
            }
          ],
          tips: [
            { type: 'tip', text: 'Osaka has a concept called "kuidaore" — eat until you drop. Lean into it. No one judges you for eating from 5 different stalls in 30 minutes.' }
          ]
        },
        {
          label: 'Night',
          activities: [
            {
              title: 'First Night in Namba',
              description: "After dinner, wander the covered Namba arcade streets — Shinsaibashi-suji is open late. For drinks, head to the izakaya alleys near Namba Station. Solo tip: sit at the counter and the chef or neighbors will often start chatting.",
              details: [
                '🍻 Izakaya row near Dotonbori: try anywhere with a red lantern (aka-chochin)',
                '🎤 Karaoke: Big Echo Namba — private rooms, cheap drinks, open till 5am',
                '🌃 Night walk: south end of Dotonbori canal for neon reflections'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6687, lng: 135.5014, label: 'Dotonbori Canal', num: 1, cat: 'attraction', desc: 'Osaka\'s neon food strip — Glico Man sign, canal walk, street stalls' },
        { lat: 34.6688, lng: 135.5014, label: 'Kani Doraku', num: 2, cat: 'attraction', desc: 'Iconic giant mechanical crab sign — Dotonbori landmark' },
        { lat: 34.6667, lng: 135.5083, label: 'Kuromon Ichiba Market', num: 3, cat: 'food', desc: 'Osaka\'s 200-year-old kitchen market — fresh seafood, Kobe beef skewers' },
        { lat: 34.6692, lng: 135.5024, label: 'Hozenji Temple & Yokocho', num: 4, cat: 'attraction', desc: 'Moss-covered shrine and atmospheric restaurant alley' },
        { lat: 34.6685, lng: 135.5012, label: 'Kinryu Ramen', num: 5, cat: 'food', desc: '24-hour ramen counter with dragon statues — Osaka midnight classic' },
        { lat: 34.6685, lng: 135.5009, label: 'Wanaka Takoyaki', num: 6, cat: 'food', desc: 'The definitive takoyaki — crispy outside, molten octopus inside' }
      ]
    },
    {
      num: 2,
      date: '2026-04-04',
      neighborhoods: 'Osaka Castle · Tenjimbashi · Shinsekai · Tennoji',
      title: 'Castles, Markets & Kushikatsu Under the Tower',
      description: "The cultural heart of Osaka. Morning at the majestic castle with late cherry blossoms still hanging on. Midday at Japan's longest shopping street for local flavor. Evening deep in Shinsekai — the retro working-class district that time forgot — for the best kushikatsu in the city.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Osaka Castle & Castle Park',
              description: "Osaka Castle is the city's defining icon — the white-walled castle towering above a moat with stone ramparts. In early April, the castle park's 3,000 cherry trees are at or just past peak bloom, creating a stunning backdrop. Go early to beat tour groups.",
              details: [
                '🏯 Castle interior has 8 floors of Toyotomi Hideyoshi history — worth the climb for the top-floor panorama',
                '🌸 Nishinomaru Garden (¥200 entry) — best cherry blossom views with castle backdrop',
                '⏰ Open 9am–5pm; arrive by 9am to beat the crowds',
                '🎫 Admission: ¥600 adults · 📍 1-1 Osakajo, Chuo Ward'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Castle Park Convenience Store Picnic',
              description: 'Grab an onigiri, tamagoyaki sandwich, or hot coffee from the 7-Eleven near Tanimachi 4-chome Station. Eat in the castle park under the last cherry blossoms — peak Osaka spring morning.',
              meta: '💰 ¥400–700 · 📍 7-Eleven near Osaka Castle, Tanimachi 4-chome'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: "Tenjimbashi-suji Shopping Street",
              description: "At 2.6 kilometers, Tenjimbashi-suji is Japan's longest covered shopping street. It's gloriously un-touristy — locals buy groceries, clothes, daily goods, and eat at the tiny restaurants lining the covered arcade. Walk south to north and duck into everything that looks interesting.",
              details: [
                '🛍️ Starts at Tenjimbashi 1-chome, runs north past Ogimachi Park',
                '🍡 Look for: traditional wagashi (Japanese sweets), cheap ramen shops, vintage stores',
                '🎭 Osaka Tenmangu Shrine at the south end — worth a detour',
                '📸 The covered arcade with local shop signs is great street photography'
              ]
            },
            {
              title: 'Spa World — Osaka\'s Temple of Relaxation',
              description: "Swap the castle rush for an afternoon soak. Spa World is a massive multi-floor onsen complex in Shinsekai with themed bath zones: Roman baths, Finnish saunas, Japanese rotenburo (outdoor baths), and more. The ultimate reset between two nights of food and drink.",
              details: [
                '♨️ European and Asian themed bath zones rotate monthly between genders',
                '💴 Entry: ¥1,200–1,500 depending on time/day · Towels available for purchase',
                '🌆 Open 10am–8:45am next day (yes, you can sleep there)',
                '📍 3-4-24 Ebisuhigashi, Naniwa Ward — short walk from Tsutenkaku Tower'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shinsekai & Tsutenkaku Tower at Sunset',
              description: "Shinsekai means 'New World' — which is ironic since this retro district hasn't changed much since the 1920s. Walk under Tsutenkaku Tower as it lights up at dusk. This is Osaka's most authentic neighborhood: old billiard halls, pachinko parlors, chess players on benches.",
              details: [
                '🗼 Tsutenkaku Tower — climb to the observation deck for panoramic Osaka views',
                '📸 The tower lit up against the sunset is a stunning shot',
                '🎮 The neighborhood has old-school game centers and billiard halls from a different era',
                '🐡 Look for Billiken statues (the God of Things as They Ought to Be) — rub his feet for luck'
              ]
            }
          ],
          meals: [
            {
              type: '🍢 Dinner',
              name: 'Kushikatsu Daruma — Shinsekai Original',
              description: "Kushikatsu (deep-fried skewers) was invented in Shinsekai, and Daruma is the undisputed classic. Beef, prawn, lotus root, asparagus — each dipped once (!) in the communal sauce. The \"no double dipping\" rule is sacred. Sit at the counter, order rounds of skewers and cold Asahi.",
              meta: '💰 ¥1,500–2,500 · 📍 2-3-9 Ebisuhigashi, Naniwa Ward · The OG Shinsekai location'
            }
          ],
          tips: [
            { type: 'tip', text: 'In Shinsekai kushikatsu restaurants, the communal sauce pot sits on the counter. You can dip once, never twice — it\'s both the law and religion here.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6873, lng: 135.5262, label: 'Osaka Castle', num: 1, cat: 'attraction', desc: 'Iconic 16th-century castle with panoramic city views and cherry blossom park' },
        { lat: 34.6878, lng: 135.5246, label: 'Nishinomaru Garden', num: 2, cat: 'attraction', desc: 'Best cherry blossom viewing with castle backdrop — ¥200 entry' },
        { lat: 34.7009, lng: 135.5100, label: 'Tenjimbashi-suji Shopping Street', num: 3, cat: 'attraction', desc: "Japan's longest covered shopping street — 2.6km of local shops" },
        { lat: 34.6524, lng: 135.5063, label: 'Tsutenkaku Tower', num: 4, cat: 'attraction', desc: 'Retro Shinsekai tower — observation deck + neighborhood icon' },
        { lat: 34.6517, lng: 135.5047, label: 'Spa World', num: 5, cat: 'attraction', desc: 'Massive themed onsen complex — Roman baths, Finnish saunas, Japanese rotenburo' },
        { lat: 34.6523, lng: 135.5069, label: 'Kushikatsu Daruma', num: 6, cat: 'food', desc: 'The original kushikatsu restaurant — birthplace of deep-fried skewers' },
        { lat: 34.6528, lng: 135.5064, label: 'Shinsekai District', num: 7, cat: 'attraction', desc: 'Retro 1920s working-class neighborhood, pachinko, billiards, authentic Osaka soul' }
      ]
    },
    {
      num: 3,
      date: '2026-04-05',
      neighborhoods: 'Shinsaibashi · Amerika-mura · Kitahorie · Namba',
      title: 'Vintage Alley Days & Electric Nights',
      description: "Daytime is for wandering Shinsaibashi and the hidden streets of Amerika-mura, where vintage shops and independent cafés fill converted buildings. Evenings escalate through izakayas, jazz bars, and the controlled chaos of Namba after midnight — Osaka's nightlife is legendary and you should experience all of it.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinsaibashi-suji Covered Arcade',
              description: "Osaka's most famous shopping street runs for 600 meters under a glass-roofed arcade. Brands mix with local shops and coffee spots. It's best in the morning before crowds peak — drift south toward Amerika-mura as you go.",
              details: [
                '🛍️ Mix of Japanese fashion brands, shoe shops, souvenirs, and food stalls',
                '📍 Starts near Shinsaibashi Station, runs south toward Namba',
                '🕘 Morning is the sweet spot — open from ~10am, quieter than afternoons'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Arabica Coffee (% Arabica) — Shinsaibashi',
              description: "Osaka's most Instagrammed coffee. The minimalist white kiosk near Shinsaibashi does the best cortado in the city. Grab one and walk.",
              meta: '💰 ¥600–800 · 📍 Shinsaibashi area · Look for the % sign'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Amerika-mura (Amemura) — Osaka\'s Counterculture Village',
              description: "Turn west off Shinsaibashi into Amerika-mura — Osaka's answer to Harajuku but grittier, more genuinely weird, and less polished. Vintage American clothes shops crowd narrow streets. Triangle Park in the center is where teens hang out in elaborate fashion. Hidden above the shops: jazz cafés, record stores, and independent art spaces.",
              details: [
                '👗 Vintage shopping: Chicago Osaka, New York Joe Exchange, and dozens of indie shops',
                '🎵 Big Step building on Triangle Park has indie shops and a rooftop',
                '📸 Triangle Park: street fashion photo opportunities all afternoon',
                '☕ Duck into any staircase with a handwritten sign — that\'s where the good cafés hide'
              ]
            },
            {
              title: 'Kitahorie Neighborhood & Horie Walk',
              description: "Continue west into Kitahorie / Horie — Osaka's hipper, more adult version of Amerika-mura. Boutique furniture stores, concept shops, and the kind of understated coffee bars that Japanese cities do better than anywhere. Walk along the Nagahori canal.",
              details: [
                '🌿 Nagahori Tsurumi-ryokuchi Park canal walk — a peaceful break',
                '☕ Café culture is strong here — look for independent third-wave spots',
                '🏮 This area is much less touristy — proper Osaka living'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Menya Inoichi — Shinsaibashi',
              description: "Award-winning yuzu shio ramen hidden in the backstreets near Shinsaibashi. The bowl is delicate, complex, and utterly unlike the tonkotsu you've been seeing everywhere. Counter seating, lunch only.",
              meta: '💰 ¥900–1,200 · 📍 Near Shinsaibashi · Lines form by noon — arrive early'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Izakaya Crawl — Namba\'s Backstreets',
              description: "Osaka's izakaya culture is the best in Japan. Skip the tourist-facing spots and head one block back from Dotonbori — the parallel streets are packed with tiny bars serving excellent yakitori, edamame, and cold drafts to salarymen. Sit at counters and you will make friends.",
              details: [
                '🍶 Order: cold Kirin draft, edamame, yakitori assortment — then see what they recommend',
                '🎯 Target: red lantern (aka-chochin) izakayas with no English menu — these are the real ones',
                '🍣 Nearby: standing sushi bars in Namba are excellent and cheap (¥100-200/piece)'
              ]
            }
          ],
          meals: [
            {
              type: '🍺 Dinner',
              name: 'Izakaya Crawl + Yakitori Counter',
              description: "Don't eat at one place — do 2-3 small izakayas. Yakitori counter for skewers, then a standing ramen bar to finish. Each stop: 45-60 minutes, one order of food + 1-2 drinks. Total bill: ¥3,000–5,000 for the full evening.",
              meta: '💰 ¥1,000–2,000 per stop · 📍 Side streets behind Dotonbori, Namba area'
            }
          ]
        },
        {
          label: 'Night',
          activities: [
            {
              title: 'Osaka Nightlife — Jazz, Karaoke & Late Bars',
              description: "Osaka at 11pm is just warming up. Options: Sam & Dave Jazz Club (no cover, incredible musicians), karaoke at Big Echo (private rooms, all-you-can-drink options), or the tiny basement bars near Namba Parks area. The city runs until 4-5am on weekends.",
              details: [
                '🎷 Jazz: Osaka has an incredible jazz scene — Sam & Dave, Club Metro, Cotton Club',
                '🎤 Karaoke: Big Echo Dotonbori — ¥1,500/hour, drinks included',
                '🍸 Late bars: the alleys north of Namba Station have venues open until 5am',
                '🌃 Walk the canal one last time after midnight when the neon is doubled in the reflections'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "Osaka people are famously friendly — Osaka-ites (Osaka-jin) have a reputation for talking to strangers. Don't be surprised if someone buys you a drink and wants to know your life story in broken English." }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6745, lng: 135.5025, label: 'Shinsaibashi-suji Arcade', num: 1, cat: 'attraction', desc: '600m covered shopping street — brands, local shops, coffee' },
        { lat: 34.6724, lng: 135.4997, label: 'Amerika-mura (Triangle Park)', num: 2, cat: 'attraction', desc: 'Osaka\'s counterculture hub — vintage shops, street fashion, indie cafés' },
        { lat: 34.6718, lng: 135.4975, label: 'Kitahorie / Horie District', num: 3, cat: 'attraction', desc: 'Upscale local neighborhood, boutiques, canal walk, third-wave coffee' },
        { lat: 34.6730, lng: 135.5000, label: '% Arabica Shinsaibashi', num: 4, cat: 'food', desc: 'Osaka\'s most iconic coffee kiosk — minimalist, exceptional cortado' },
        { lat: 34.6742, lng: 135.5010, label: 'Menya Inoichi', num: 5, cat: 'food', desc: 'Award-winning yuzu shio ramen — counter seating, lunch only' },
        { lat: 34.6659, lng: 135.5013, label: 'Namba Izakaya District', num: 6, cat: 'food', desc: 'Red lantern izakayas — yakitori, cold beer, late-night salaryman culture' },
        { lat: 34.6670, lng: 135.5020, label: 'Dotonbori Canal Night Walk', num: 7, cat: 'attraction', desc: 'Midnight canal stroll — neon doubled in the water reflections' }
      ]
    },
    {
      num: 4,
      date: '2026-04-06',
      neighborhoods: 'Umeda · Nakanoshima · Osaka Station',
      title: 'North Osaka, Department Store Feasts & Farewell',
      description: "The north side of Osaka — centered on Umeda and Osaka Station — has a different character: Hankyu and Hanshin department store food halls that rival Tokyo for quality, the futuristic Umeda Sky Building, and the elegant Nakanoshima island with its rose gardens and museums. A final morning in Japan's kitchen before you go.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Nakanoshima Island Morning Walk',
              description: "Nakanoshima is a sliver of land between two rivers in central Osaka, with Meiji-era buildings, the Bank of Japan Osaka branch, and the Museum of Oriental Ceramics. The rose garden blooms alongside spring flowers in April. Quiet, elegant, and completely unlike the chaos of Namba.",
              details: [
                '🌹 Nakanoshima Park rose garden — spring flowers in early April',
                '🏛️ Museum of Oriental Ceramics (MOCA) — one of Asia\'s finest ceramics collections, ¥1,500',
                '🌊 Walk along the Okawa River — there may be a boat passing under cherry trees',
                '📍 Accessible from Yodoyabashi or Naniwabashi Station'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Coffee Baum — Nakanoshima',
              description: 'A beloved local kissaten (old-school coffee shop) near Nakanoshima with a morning set: coffee + toast + egg. The Japanese morning ritual at its finest.',
              meta: '💰 ¥600–900 · 📍 Nakanoshima area · Morning set served until 11am'
            }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Umeda Sky Building',
              description: "Two towers connected by a floating garden observatory 170 meters up. The view takes in all of Osaka in every direction. Below ground is Takimi-koji — a nostalgic 1920s-recreation food alley with some of Osaka's best restaurants for a farewell lunch.",
              details: [
                '🏙️ Floating Garden Observatory: ¥1,500, open 9:30am–10:30pm',
                '🌃 360° view of Osaka, Kobe mountains, and clear days to Awaji Island',
                '🍜 Takimi Koji underground — a curated food street with top restaurants',
                '📍 1-1-88 Oyodonaka, Kita Ward — 10 min walk from Osaka Station'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Farewell Lunch',
              name: 'Takimi Koji (Umeda Sky Building Basement)',
              description: "The underground food alley beneath the Sky Building recreates an Osaka shopping street from the Taisho era. Excellent tonkotsu ramen, fresh sushi, and regional bento options. Perfect last meal — choose what you didn't manage to eat yet.",
              meta: '💰 ¥1,000–2,500 · 📍 B1F, Umeda Sky Building basement'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Hanshin / Hankyu Department Store Depachika',
              description: "Your last Osaka ritual: the basement food halls (depachika) of Hanshin or Hankyu department stores near Osaka Station. These are temples of Japanese food culture — artisan wagashi, Kobe beef bentos, world-class pastry, fresh sushi, and every regional specialty beautifully packaged. Load up on omiyage (souvenirs) here.",
              details: [
                '🍰 Hanshin Umeda B1: best food hall for casual eating and grazing',
                '🎂 Hankyu B1: more premium, excellent wagashi and cakes',
                '🛍️ Souvenirs: Osaka rock candy, Glico Pocky sets, Osaka-designed goods',
                '📦 Pre-packaged omiyage for home — seal-fresh packaging holds up on the flight'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "The depachika closes around 8pm, but the buying rush happens 5-7pm when salarymen grab dinner bentos. Go earlier for relaxed browsing and full selection." }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6929, lng: 135.5017, label: 'Nakanoshima Island', num: 1, cat: 'attraction', desc: 'Elegant river island with rose garden, Meiji buildings, and art museum' },
        { lat: 34.6930, lng: 135.5005, label: 'Museum of Oriental Ceramics', num: 2, cat: 'attraction', desc: 'World-class ceramics collection — Tang dynasty to modern Japan' },
        { lat: 34.7024, lng: 135.4959, label: 'Umeda Sky Building', num: 3, cat: 'attraction', desc: '170m floating garden observatory with 360° city views' },
        { lat: 34.7024, lng: 135.4959, label: 'Takimi Koji', num: 4, cat: 'food', desc: 'Taisho-era replica food street in the Sky Building basement' },
        { lat: 34.7019, lng: 135.4985, label: 'Hanshin Department Store', num: 5, cat: 'food', desc: 'Best depachika (basement food hall) in Osaka — graze and stock up' },
        { lat: 34.7025, lng: 135.4978, label: 'Hankyu Department Store', num: 6, cat: 'food', desc: 'Premium food hall — wagashi, Kobe beef bentos, artisan pastry' },
        { lat: 34.7024, lng: 135.4959, label: 'Osaka/Umeda Station', num: 7, cat: 'attraction', desc: 'Hub for departures — Haruka Express to KIX, shinkansen to Tokyo' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (solo)', budget: '¥3,000–6,000/night', midrange: '¥8,000–15,000/night', luxury: '¥20,000–40,000/night' },
    { category: 'Food (per day)', budget: '¥3,000–5,000/day', midrange: '¥6,000–10,000/day', luxury: '¥15,000+/day' },
    { category: 'Transport (Osaka Metro)', budget: '¥600–1,000/day', midrange: '¥1,200–2,000/day', luxury: '¥3,000+/day (taxi)' },
    { category: 'Activities', budget: '¥0–1,500/day', midrange: '¥2,000–4,000/day', luxury: '¥5,000+/day' },
    { category: 'Spa World', budget: '¥1,200–1,500', midrange: '¥1,500', luxury: '—' },
    { category: '4-Day Total (solo)', budget: '¥40,000–60,000 (~$270–400)', midrange: '¥80,000–120,000 (~$530–800)', luxury: '¥200,000+' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Kansai International Airport (KIX) — main gateway for Osaka', 'Haruka Limited Express to Osaka/Umeda: ~75 min, ¥3,060', 'Limousine bus to Namba: ~60 min, ¥1,600 — easier with luggage', 'Shin-Osaka Station for shinkansen connections (bullet train from Tokyo ~2.5hr)'] },
    { title: '🏨 Where to Stay', items: ['Namba area — best for nightlife and food access', 'Shinsaibashi area — midpoint between Namba and Umeda', 'Budget: capsule hotels from ¥3,000/night (Book and Bed Osaka is excellent)', 'Midrange: APA Hotel Namba, Cross Hotel Osaka (¥8,000–15,000)'] },
    { title: '🌸 April Specifics', items: ['Cherry blossom season typically late March – early April — you may catch the tail end', 'Osaka Castle Park: best blossom spot in the city', 'Spring weather: 14–20°C, light rain possible — pack a layer and compact umbrella', 'Golden Week begins April 29 — leave before or expect extreme crowds'] },
    { title: '📱 Connectivity', items: ['Buy a data SIM at KIX or convenience stores (IIJmio, Sakura Mobile)', 'Pocket WiFi rental available at KIX — convenient if sharing', 'Google Maps works perfectly on Japan subway — essential tool', '7-Eleven ATMs accept international cards — withdraw yen there'] },
    { title: '🗣️ Language Tips', items: ['Google Translate camera mode — point at menus for instant translation', 'Most transport staff speak some English; station signs have English', '"Eigo no menu wa arimasu ka?" = "Do you have an English menu?"', '"Kore wo kudasai" + pointing = universal ordering technique'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
