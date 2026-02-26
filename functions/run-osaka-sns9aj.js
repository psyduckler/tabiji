const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1772072806020_sns9aj",
  orderId: "order_1772072806020_sns9aj",
  email: "psyduckler@gmail.com",
  destination: "Osaka, Japan",
  startDate: "2026-02-27",
  endDate: "2026-03-02",
  start_date: "2026-02-27",
  end_date: "2026-03-02",
  groupSize: "1",
  travel_style: "",
  dining: "",
  budget: "",
  requests: "",
  amount: "0.00",
  status: "pending"
};

const itineraryData = {
  destination: "Osaka, Japan",
  countryEmoji: "🇯🇵",
  title: "Solo Osaka: The Real City, Unfiltered",
  subtitle: "Dotonbori → Nakazakicho → Shinsekai → Kyoto → Farwell in Namba",
  description: "Osaka alone is Osaka at its best. No consensus dinner decisions. No group pace. Just you and Japan's most charismatic city — the one built on street food, blunt opinions, and the philosophy that eating well is a civic duty. This 4-day solo itinerary skips the obligatory tourist checklist and goes deep: vintage-kissaten mornings in Nakazakicho, a Kyoto deep-dive built around dawn at Fushimi Inari, late-night standing bars in Fukushima where the regulars have been drinking there since the Showa era, and a farewell bowl of ramen eaten alone in a solo booth at 1am. Solo Osaka is freedom. Use it.",
  duration: "3 nights / 4 days",
  dates: "Feb 27 – Mar 2, 2026",
  budget: "Moderate",
  pace: "Fast days, self-directed nights",
  bestFor: "Solo travelers, urban explorers, first-timers who want depth over landmarks",
  highlights: [
    "Dotonbori at night — neon canal walk the right way (quickly, then leave)",
    "Nakazakicho — Osaka's artistic village: retro kissaten, vintage shops, zero tour groups",
    "Kuromon Ichiba Market — Osaka's 200-year-old kitchen, best solo grazing on earth",
    "Shinsekai deep dive — the 1950s Osaka time capsule, kushikatsu skewers with the locals",
    "Fushimi Inari at dawn alone — 10,000 torii gates before the crowds arrive",
    "Tenryu-ji Zen garden and the bamboo grove — Arashiyama at its most serene",
    "Fukushima izakaya district — where Osaka locals actually eat and drink",
    "Ichiran Ramen solo booth — the loneliest and most perfect bowl of ramen",
    "Namba late-night circuit — tachinomi bars, craft cocktails, and Osaka's 24-hour energy"
  ],
  essentials: [
    {
      title: "🚄 Getting Around Osaka",
      text: "Grab an ICOCA card at Kansai International Airport (KIX) or any major station — it works on every train, subway, and bus in Osaka and Kyoto. The Osaka Metro network is excellent and covers almost everywhere you'll want to go. For Kyoto day trip: JR Special Rapid from Osaka Station to Kyoto Station takes 14–20 min (¥570) — the fastest and cheapest option. Google Maps handles Kansai transit flawlessly. Taxis are easy but pricey; use them only when the train doesn't make sense."
    },
    {
      title: "🌡️ Late February / Early March in Osaka",
      text: "Expect cool to mild temperatures — 7°C at night, up to 15°C during the day. Pack layers: a light down jacket for mornings and evenings, with a lighter layer underneath for when you're walking hard. No cherry blossoms yet (peak is late March–April in Kansai), but plum blossoms may be finishing at shrines and gardens — still beautiful. Days are getting noticeably longer. Morning fog over the rivers and canals in Nakanoshima and Dotonbori is atmospheric. Pack a compact umbrella; February in Osaka can bring rain."
    },
    {
      title: "🍜 Solo Eating in Japan",
      text: "Solo dining in Osaka is genuinely comfortable — Japan is culturally very accommodating of solo diners. Ichiran Ramen's individual booths were literally invented for solo eating. Counter seats at izakayas are normal and social (you end up talking to the person next to you). Standing ramen, soba, and noodle shops are perfect: fast, cheap, no awkwardness. Markets like Kuromon Ichiba and Nishiki Market are essentially designed for solo grazing — buy one of everything and keep moving. Being solo here is an advantage."
    },
    {
      title: "🌃 Osaka Nights — Going Solo",
      text: "Osaka nightlife as a solo traveler is actually great. Standing bars (tachinomi) are inherently social — you're elbow-to-elbow with strangers. Counter seats at izakayas invite conversation (even with minimal Japanese — a nod and a raised glass goes far). Amerikamura and Shinsaibashi have the energy. Fukushima district is more local and intimate. Don't skip late-night Osaka — this is one of the world's great night cities, and a solo wanderer can go wherever the evening pulls them without compromise."
    },
    {
      title: "💴 Money & Practical Tips",
      text: "Japan still runs heavily on cash — especially at smaller restaurants, temples, and standing bars. Get cash from a 7-Eleven ATM (accepts international cards without drama). Budget ¥4,000–8,000/day for food, transit, and entry fees as a solo traveler. Coin lockers at Namba, Osaka, and Kyoto Stations let you stash bags when exploring all day. Download Google Translate and point the camera at menus — it reads Japanese instantly. Download the Osaka Metro app for live train status. Tipping is not a thing in Japan — don't do it."
    }
  ],
  days: [
    {
      num: 1,
      title: "Arrival: Dotonbori, Kuromon & First Night in Osaka",
      neighborhoods: "Namba · Dotonbori · Kuromon · Shinsaibashi",
      date: "Feb 27",
      mapPins: [
        { lat: 34.6687, lng: 135.5013, label: "Dotonbori Canal", num: 1, cat: "activity", desc: "Osaka's famous neon canal — the arrival photo, then move on" },
        { lat: 34.6689, lng: 135.5042, label: "Kuromon Ichiba Market", num: 2, cat: "food", desc: "200-year-old covered market — fresh sashimi, grilled skewers, Japanese street food" },
        { lat: 34.6695, lng: 135.5063, label: "Namba Grand Kagetsu", num: 3, cat: "activity", desc: "Osaka's most famous comedy theater — manzai and rakugo in the city of comedy" },
        { lat: 34.6741, lng: 135.5014, label: "Shinsaibashi-suji Arcade", num: 4, cat: "activity", desc: "Osaka's main shopping strip — 600m of shops, restaurants, and energy" },
        { lat: 34.6741, lng: 135.5003, label: "Amerikamura Triangle Park", num: 5, cat: "nightlife", desc: "Heart of Osaka's youth culture and nightlife district" },
        { lat: 34.6702, lng: 135.4999, label: "Ichiran Ramen Namba", num: 6, cat: "food", desc: "Solo ramen booth — the perfect solo traveler first meal in Japan" }
      ],
      timeBlocks: [
        {
          label: "Afternoon (Arrival)",
          activities: [
            {
              title: "Land, Orient, and Get to Namba",
              description: "From KIX (Kansai International Airport): take the Nankai Rapid Express directly to Namba Station — 38 minutes, ¥1,060. No transfer, no drama. If you're on a late arrival, the Nankai runs until midnight. Check in, drop your bags, and don't let jet lag win — Osaka rewards the traveler who pushes through the first afternoon. Grab an ICOCA card at KIX or Namba Station before anything else.",
              details: [
                "🛬 Nankai Rapid Express: KIX → Namba, every 30 min, ¥1,060, 38 min — the simplest airport transfer in Japan",
                "💡 ICOCA card: buy at any ticket machine at KIX or Namba (¥2,000 deposit included) — it loads instantly and works everywhere",
                "🗄️ Coin lockers at Namba Station if your accommodation isn't checking in yet — ¥300–700 depending on size"
              ]
            },
            {
              title: "Kuromon Ichiba Market — Osaka's Kitchen",
              description: "Head straight to Kuromon Ichiba — the 200-year-old covered market that's been feeding Osaka since before modern Japan existed. Solo grazing at its finest: dozens of stalls selling fresh sashimi on skewers, grilled wagyu beef bites, takoyaki (octopus balls), fresh oysters, and Japanese street snacks. Walk the length, buy what looks good, eat immediately. Unlike Tokyo's Tsukiji market, Kuromon is compact, intimate, and barely touristy before 3pm. Go hungry.",
              details: [
                "📍 5 min walk from Namba Station or Nipponbashi Station (Sakaisuji Line)",
                "🦪 The raw oyster stall near the entrance — ¥300/each, opened right in front of you. Solo traveler's perfect snack.",
                "🐟 Fresh sashimi on skewers: yellowtail, tuna, sea urchin — market-fresh and far cheaper than any restaurant",
                "💡 The market closes early (5–6pm) — hit it now, not later. Graze as your arrival meal."
              ]
            }
          ],
          meals: [
            {
              type: "🦪 Arrival Grazing",
              name: "Kuromon Ichiba Market — eat your way through",
              description: "This IS your first meal in Osaka. Pick up fresh sashimi skewers, grilled wagyu bites, takoyaki from the oldest stall you can find, and end with a fresh uni (sea urchin) on rice if it's available. Budget ¥1,500–2,500 and walk the length twice.",
              meta: "¥1,500–2,500 total · Kuromon Ichiba · Market closes ~5–6pm · Cash preferred"
            }
          ],
          tips: [
            { type: "tip", text: "Kuromon Ichiba is best experienced by walking the entire length first without buying anything — see what's there, note what looks good, then go back for the best of each. Solo travel means you can stop for exactly the three things you want, in exactly the order you want." }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Dotonbori: The Canal Shot, Then Get Out",
              description: "You're obligated to walk Dotonbori — it's Osaka's most famous street and the neon canal is genuinely spectacular at night. Do the classic Ebisu-bashi bridge shot with the Glico Running Man. Walk the canal. See the giant Kani Doraku moving crab. Acknowledge that you're in one of the world's great cities. Then leave. Dotonbori is for the photo. The rest of your evening is for the real Osaka.",
              details: [
                "📸 Best shot: stand on Ebisu-bashi bridge facing east — the neon reflections on the canal at night are exactly what you came for",
                "💡 Nighttime is when Dotonbori really fires — the neon, the canal, the movement. 10 minutes is enough.",
                "🦀 The Kani Doraku crab sign (giant moving mechanical crab) has been there since 1960 — photograph it, it's genuinely great"
              ]
            },
            {
              title: "Shinsaibashi Night Walk",
              description: "Walk north from Dotonbori into Shinsaibashi-suji arcade — Japan's most lively covered shopping street at night. The shops run until 8–9pm, and the streets fill with people after. Walk west one block into Amerikamura — the youth culture and nightlife district centered on Triangle Park. The concentration of bars, vintage stores, and food options in a two-block radius is overwhelming in the best way.",
              details: [
                "🛍️ The arcade itself is worth the walk even at night — people-watching in Shinsaibashi is world-class",
                "🎨 Amerikamura has the best street art in Osaka scattered on walls through the district — keep your eyes up",
                "🍸 Start your evening here — dozens of options from craft beer to izakaya to cocktail bars"
              ]
            }
          ],
          meals: [
            {
              type: "🍜 Dinner",
              name: "Ichiran Ramen — solo booth experience",
              description: "Ichiran Ramen Namba: the legendary solo-booth ramen designed specifically for solo diners. You fill out a customization form (broth richness, garlic level, chili level, extra toppings), slide it through a bamboo curtain, and a perfect bowl of tonkotsu ramen appears. You eat alone in your little booth. It's meditative and delicious. This is the perfect first dinner in Japan as a solo traveler — a small ritual that says you've arrived.",
              meta: "¥880–1,300 · Namba, multiple locations · Open until 5am · Zero wait after 10pm"
            }
          ],
          tips: [
            { type: "reddit", text: "Ichiran as a solo traveler is something else. You're in your own little world — you can read, think, just exist. And the ramen is genuinely excellent. It's not even ironic — it's legitimately the best tonkotsu I've had in Osaka.", cite: "r/JapanTravel" }
          ]
        }
      ]
    },
    {
      num: 2,
      title: "Osaka Deep: Nakazakicho, Shinsekai & Fukushima Nights",
      neighborhoods: "Nakazakicho · Tenjinbashisuji · Shinsekai · Fukushima",
      date: "Feb 28",
      mapPins: [
        { lat: 34.7031, lng: 135.5082, label: "Nakazakicho Neighborhood", num: 1, cat: "activity", desc: "Osaka's artistic vintage quarter — retro kissaten, indie galleries, no tour groups" },
        { lat: 34.7009, lng: 135.5110, label: "Tenjinbashisuji Shopping Street", num: 2, cat: "activity", desc: "World's longest covered arcade — 2.6km of local shops and real Osaka life" },
        { lat: 34.6921, lng: 135.5020, label: "Umeda Sky Building", num: 3, cat: "activity", desc: "Osaka's most spectacular viewpoint — open-air ring 173m up between two towers" },
        { lat: 34.6924, lng: 135.5095, label: "Nakanoshima Island", num: 4, cat: "activity", desc: "Neoclassical island between two rivers — Osaka's best-kept secret" },
        { lat: 34.6523, lng: 135.5063, label: "Shinsekai & Tsutenkaku", num: 5, cat: "activity", desc: "Osaka's 1950s retro neighborhood — kushikatsu alley and the Billiken tower" },
        { lat: 34.6916, lng: 135.4851, label: "Fukushima Izakaya District", num: 6, cat: "nightlife", desc: "Where Osaka's off-duty chefs eat — standing bars and tiny izakayas" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Nakazakicho: The Osaka Nobody Talks About",
              description: "Take the Tanimachi Line two stops north of Namba to Nakazakicho Station. Step out into a neighborhood that exists in a completely different Osaka from Dotonbori. Nakazakicho is where Osaka's artists, designers, and creative people have been quietly building something for 40 years: narrow lanes with vintage clothing boutiques, antique furniture, indie bookshops, and old-school kissaten (Japanese coffee houses) where the menu hasn't changed since 1975. The atmosphere is almost aggressively unhurried. Perfect solo morning.",
              details: [
                "☕ The kissaten here are the real thing — hand-dripped coffee, thick toast, boiled egg, ¥400–600. Many serve this all day.",
                "🛍️ The vintage clothing stores are better curated and cheaper than Harajuku or Shimokitazawa — look for the ones with hand-lettered signs",
                "💡 Walk the small alleys north of the main street — that's where the most interesting spots hide"
              ]
            },
            {
              title: "Tenjinbashisuji: Real Osaka Commerce",
              description: "Walk south from Nakazakicho into Tenjinbashisuji — the world's longest covered shopping arcade at 2.6 kilometers. Unlike tourist-facing Shinsaibashi, this is where Osaka actually shops: 600+ stores selling everyday goods, local sweets, hardware, fruit stalls, cheap ramen joints, and neighborhood pharmacies. The quality of people-watching is exceptional. Great for picking up specialty Osaka snacks at local prices.",
              details: [
                "📍 Walk from Nakazakicho Station south — you exit near Namba eventually",
                "🍡 Try the wagashi (traditional sweet) shops along the way — especially handmade mochi from stalls with long lines",
                "💡 The arcade is partially covered — bring layers for the open sections"
              ]
            }
          ],
          meals: [
            {
              type: "☕ Breakfast",
              name: "Kissaten in Nakazakicho — hand-dripped coffee and morning set",
              description: "Find a kissaten (old-school Japanese coffee house) in Nakazakicho with a hand-written menu and brown curtains. Order the morning set: hand-dripped coffee and thick toast, often with a boiled egg or jam. This is a distinctly Japanese solo breakfast ritual — quiet, unhurried, excellent coffee. The ones with locals in them at 9am are the right ones.",
              meta: "¥400–700 · Nakazakicho neighborhood · Look for handwritten signs · Cash"
            }
          ],
          tips: [
            { type: "tip", text: "Nakazakicho has a 'hidden bakery' vibe — the best kissaten don't have signs you can read from the street. Follow the smell of fresh coffee. Solo travel means you can duck into any door that looks interesting without consulting anyone." }
          ]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "Umeda Sky Building — The Best View in Osaka",
              description: "Walk west from Osaka Station to the Umeda Sky Building — two 40-story towers connected at the top by an open-air ring observatory called the Floating Garden. The observation deck is the best view in Osaka: 360 degrees at 173 meters, no obstructions. The 10-story escalator ride through a glass tube between the towers, suspended in open air, is itself extraordinary. Morning light on the city grid is spectacular. On clear late-February days, you can see the mountains to the east and the bay to the west.",
              details: [
                "💴 ¥1,500 · Open 10am–10:30pm",
                "📍 15 min walk west from Osaka Station (or through the underground shopping mall)",
                "💡 The glass escalator between the towers is one of the great individual moments in any building in the world — stop mid-ride and look down"
              ]
            },
            {
              title: "Nakanoshima Island — Osaka's European Secret",
              description: "Walk 15 minutes east from the Sky Building to Nakanoshima — a long island between the Dojima and Tosabori rivers in the center of the city. This is one of the few places in Osaka where you completely forget you're in a major city. Neoclassical European-inspired buildings line both shores: the Bank of Japan Osaka Branch (1903), the gorgeous rose-brick Osaka City Central Public Hall (1918, free to enter), and the Museum of Oriental Ceramics. Riverside walking paths. Almost no tourists.",
              details: [
                "🏛️ The Osaka City Central Public Hall entrance hall is free — walk in for the neoclassical interior, then walk the riverside",
                "🖼️ Museum of Oriental Ceramics (¥1,000) — world-class Korean and Chinese ceramics in a serene riverside building. Worth it if you have museum energy.",
                "💡 The island in late February: river mist in the mornings, occasional plum blossoms in the small gardens"
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Lunch",
              name: "Nakanoshima riverside café or ramen spot near Umeda",
              description: "After the Sky Building, grab lunch near Umeda or Nakanoshima. The Umeda underground mall has dozens of ramen, soba, and set-meal restaurants — full lunch for ¥800–1,200. For a sit-down experience, the Nakanoshima area has quiet riverside restaurants with ¥1,000–1,500 set lunch deals.",
              meta: "¥800–1,500 · Umeda/Nakanoshima area · Weekday lunch sets are excellent value"
            }
          ],
          tips: [
            { type: "tip", text: "Nakanoshima is where Osaka residents take their quiet weekend walks. A solo traveler here blends right in — bring a book for the riverside bench." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Shinsekai: 1950s Osaka Frozen in Time",
              description: "Take the subway south to Dobutsuen-mae Station and walk into Shinsekai — \"New World,\" built in 1912, modeled half on Paris and half on New York, and now a perfectly preserved 1950s time capsule. Tsutenkaku Tower watches over a neighborhood of kushikatsu restaurants, old pachinko parlors, retro game centers, and dozens of Billiken (Osaka's luck god) statues. It's gloriously kitsch and completely authentic — working-class Osaka with no pretense of being anything else. Walk the main kushikatsu street slowly.",
              details: [
                "📍 Dobutsuen-mae Station (Midosuji Line) · 5 min walk to Shinsekai main street",
                "🗼 Tsutenkaku Tower (¥1,000) — the observation deck is fun; the Billiken statue at the top is Osaka's lucky god. Rub his feet for luck.",
                "💡 Walk the alleys south of the tower — the old-school coffee shops, senbei stalls, and 3-seat barbers are the best part of Shinsekai"
              ]
            }
          ],
          meals: [
            {
              type: "🍢 Late Afternoon Snack / Early Dinner",
              name: "Kushikatsu at Shinsekai — breaded skewers, Osaka's soul food",
              description: "Kushikatsu (deep-fried breaded skewers on sticks) originated in Shinsekai. Order at any counter — the rule is dip once only into the communal sauce (double-dipping is the neighborhood's cardinal sin, and they will tell you). Order: pork, asparagus, lotus root, cheese, onion, shrimp — whatever looks best. Solo is ideal: you sit at the counter, order one at a time, the chef hands them to you fresh. Most places: ¥150–350 per skewer. Eat until done.",
              meta: "¥800–1,500 total · Shinsekai main street, multiple restaurants · No reservations · Cash"
            }
          ],
          tips: [
            { type: "reddit", text: "Shinsekai feels like Osaka before it became Instagram. The kushikatsu is the real thing — not tourist food. Sitting at the counter alone with a beer and a pile of skewers while the owner chats at you in Osaka dialect is one of my top travel memories.", cite: "r/osaka" }
          ]
        },
        {
          label: "Evening — Fukushima Izakaya Night",
          activities: [
            {
              title: "Fukushima District: Where Osaka Actually Drinks",
              description: "Head north on the subway to Fukushima Station — one stop from JR Osaka. This neighborhood is where Osaka's professional chefs, food journalists, and serious drinkers go when they want to eat without the tourist theater of Namba. The standing izakayas and tiny counter restaurants on the alleys immediately south of the station serve whatever was freshest that morning, in rooms that seat 6–10 people, run by owners who've been doing this for 30+ years. As a solo traveler you'll get counter seats immediately, you'll be next to locals, and drinks will arrive fast.",
              details: [
                "📍 JR Fukushima Station or Hanshin Fukushima Station · Walk south into the alleys",
                "💡 If there's a handwritten specials board (kyō no osusume) and no English menu, that's the place to go in",
                "🍶 Solo drinks: order a draft Asahi (nama biiru) or house sake — the counter culture here means you'll likely end up in conversation",
                "🕐 Fukushima gets lively 7–10pm — arrive early for a seat, or arrive at 9pm when second-round seats open up"
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Dinner",
              name: "Fukushima standing izakaya — order the daily specials",
              description: "Walk the Fukushima alleys until you find a counter with people in it, a charcoal grill smell, and a handwritten menu. Sit at the counter. Order whatever the person next to you is having if you can't read the menu — point and nod. The daily specials (kyō no osusume) will involve whatever was freshest at the market that morning. Yakitori skewers, grilled fish, small cold dishes, house sake. Solo counter dining in Fukushima is one of the great experiences Osaka offers.",
              meta: "¥2,000–4,000 with drinks · Fukushima alleys south of the station · Walk-in, no English, bring cash"
            }
          ],
          tips: [
            { type: "tip", text: "Fukushima is where the real Osaka drink scene is. Skip Namba's nomihoudai bars tonight — save those for tomorrow's final night. Fukushima rewards the solo traveler who walks in without a plan and just orders something." }
          ]
        }
      ]
    },
    {
      num: 3,
      title: "Kyoto Day Trip: Fushimi Inari at Dawn, Arashiyama & Gion at Dusk",
      neighborhoods: "Fushimi · Arashiyama · Kinkaku-ji · Gion · Nishiki · Kyoto Station",
      date: "Mar 1",
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: "Fushimi Inari Taisha", num: 1, cat: "activity", desc: "10,000 vermillion torii gates up Mt. Inari — arrive at dawn for the gates alone" },
        { lat: 35.0168, lng: 135.6745, label: "Arashiyama Bamboo Grove", num: 2, cat: "activity", desc: "Towering bamboo — surreal sound and light in the morning" },
        { lat: 35.0161, lng: 135.6747, label: "Tenryu-ji Zen Garden", num: 3, cat: "activity", desc: "UNESCO garden using the mountains as borrowed scenery — one of Japan's finest" },
        { lat: 35.0394, lng: 135.7292, label: "Kinkaku-ji — Golden Pavilion", num: 4, cat: "activity", desc: "Three-story gold-leafed temple reflected in Mirror Pond" },
        { lat: 34.9949, lng: 135.7785, label: "Nishiki Market", num: 5, cat: "food", desc: "Kyoto's 400-year-old covered food street — solo grazing paradise" },
        { lat: 35.0036, lng: 135.7788, label: "Gion — Hanamikoji & Shirakawa", num: 6, cat: "activity", desc: "Kyoto's geisha district — stone lanterns, canal willows, preserved machiya" }
      ],
      timeBlocks: [
        {
          label: "Early Morning — 6:30am Departure",
          activities: [
            {
              title: "Fushimi Inari Taisha at Dawn — Gates Alone",
              description: "Leave Osaka by 6:30am. JR Special Rapid from Osaka Station to Kyoto Station (14 min, ¥570), then JR Nara Line two stops to Inari Station (5 min, ¥150). Arrive before 8am. This is the reward for the early alarm: the lower torii gate tunnels — the most photographed spot in Japan — with almost no one in them. The vermillion columns glow orange in the morning light. Climb to the Yotsutsuji intersection (30–40 min up) for panoramic views over Kyoto in the morning haze. This is what solo travel was invented for: being somewhere extraordinary, alone, before the world wakes up.",
              details: [
                "⏰ Aim to reach the gate by 8am — by 9:30am it's completely different",
                "📍 JR Inari Station is literally at the shrine entrance — 2 minutes on foot",
                "🦊 The kitsune (fox) statues holding keys in their mouths throughout the mountain — guardians of Inari, the rice and commerce deity",
                "💡 The Yotsutsuji viewpoint (halfway up, 30–40 min) is the right turn-around for a packed day — gives you the mountain experience without the full 4-hour loop",
                "🌫️ Late February morning mist through the gates: atmospheric beyond description"
              ]
            }
          ],
          meals: [
            {
              type: "☕ Pre-Departure Breakfast",
              name: "Hotel or Osaka Station convenience store",
              description: "Grab breakfast before you leave. 7-Eleven at Osaka Station: onigiri, hot tea, maybe a sandwich. Eat on the train. Save your appetite for Arashiyama — you'll want to be hungry for the Tenryu-ji shojin ryori lunch.",
              meta: "¥400–700 · Any konbini · 24/7 · Eat on the platform or train"
            }
          ],
          tips: [
            { type: "reddit", text: "Fushimi Inari alone at dawn is one of those travel moments you genuinely remember for years. I was there by 7:30am and had the middle gate tunnels almost to myself for 20 minutes. By 9am it was four abreast. The alarm is worth it.", cite: "r/JapanTravel" }
          ]
        },
        {
          label: "Morning — Arashiyama",
          activities: [
            {
              title: "Arashiyama Bamboo Grove",
              description: "Take the JR Sagano Line from Kyoto Station to Saga-Arashiyama Station (~25 min, ¥240). The bamboo grove is a 5-minute walk — free to enter, always accessible. Walking through 30-meter bamboo that blocks out the sky creates a sound unlike anything else in the world: a deep, resonant rustling. Go in the morning. Exit through Tenryu-ji's bamboo section (the continuation of the grove inside the temple grounds) into the Zen garden. In late February, the bamboo is green against a pale winter sky.",
              details: [
                "🎋 The bamboo is best experienced by pausing and listening — the wind creates waves of sound through the entire grove",
                "💡 Continue straight from the grove into Tenryu-ji — the transition is seamless and the garden is the real destination",
                "📸 Early morning in the grove: pale green diffused light and almost empty paths — March on a weekday is ideal"
              ]
            },
            {
              title: "Tenryu-ji Zen Garden — 700 Years of Garden Design",
              description: "Tenryu-ji's Sogenchi Garden was designed in the 14th century by Muso Soseki, one of Japan's greatest garden masters. It uses 'shakkei' — borrowed scenery — so the Arashiyama mountains beyond the garden wall become part of the composition. Water, rocks, moss, and pine trees in the foreground; mountain ridges behind. A garden designed to look exactly right from one specific spot. From there, it's perfect. Also: the painted cloud dragon on the ceiling of the main hall is one of Kyoto's great artworks — look up.",
              details: [
                "💴 ¥500 garden entry, ¥300 extra for temple interior (worth it for the dragon ceiling)",
                "🕐 Open 8:30am–5pm",
                "💡 Walk the full garden circuit path — it takes 20 minutes and every angle is thoughtfully composed"
              ]
            }
          ],
          meals: [
            {
              type: "🍱 Lunch",
              name: "Arashiyama café or Tenryu-ji shojin ryori — Buddhist vegetarian cuisine",
              description: "If you book ahead: Shigetsu, the restaurant inside Tenryu-ji temple grounds, serves shojin ryori — centuries-old Japanese Buddhist vegetarian cuisine. Multi-course set meals with sesame tofu, simmered seasonal vegetables, miso soup, tofu dengaku, pickles, and rice. Served in a tatami room overlooking the garden with mountains behind. One of Japan's finest dining experiences. Reservations: tenryuji.com. If not pre-booked: the Arashiyama main street has cafés and soba restaurants with garden views.",
              meta: "Shigetsu: ¥4,000–6,000 · Reservations essential · Inside Tenryu-ji grounds | Casual alternative: ¥800–1,500 · Arashiyama main street"
            }
          ],
          tips: [
            { type: "tip", text: "If you want to book Shigetsu, do it before your trip at tenryuji.com. Solo seat is usually easier to get than a group. The experience of eating shojin ryori while looking at a Zen garden is legitimately one of Japan's finest lunch experiences." }
          ]
        },
        {
          label: "Afternoon — Golden Pavilion to Gion",
          activities: [
            {
              title: "Kinkaku-ji — The Gold Pavilion",
              description: "Bus from Arashiyama (City Bus #59 or a taxi) to Kinkaku-ji — a three-story temple completely covered in gold leaf, reflected in Mirror Pond. You've seen it in every photo of Japan. In person, on a clear late-February day, the gold and the reflection are electric. The grounds are a short circuit walk — thoughtfully designed to frame the pavilion from multiple angles. The tea house at the end of the path has been here since 1670.",
              details: [
                "💴 ¥500 · Open 9am–5pm",
                "📸 Classic shot: the main viewing platform right at the pond edge — the pavilion fills the frame perfectly. Afternoon light from the south hits the gold beautifully.",
                "💡 Mid-afternoon is less crowded than morning — and the gold reflects the afternoon sun differently (warmer, more saturated)"
              ]
            },
            {
              title: "Nishiki Market — Solo Food Street",
              description: "Bus or subway from Kinkaku-ji to central Kyoto (Shijo-Karasuma area). Nishiki Market: 400 meters of covered food street that has been Kyoto's kitchen since the early 1600s. Over 100 stalls. Solo grazing at its finest: yuba (tofu skin, Kyoto specialty), fresh pickles in every color, matcha-flavored everything, warabi mochi, hot sesame tofu on a stick, fresh sashimi samples, and the best selection of Kyoto omiyage (gifts) in the city.",
              details: [
                "📍 5 min from Shijo or Karasuma Station · Most stalls open 9am–5pm",
                "🍡 Get: a stick of grilled tofu with miso glaze (dengaku), the fresh handmade pickles from Murakami-ju, and warabi mochi from any stall with a line",
                "🛍️ Kyoto omiyage: yatsuhashi (cinnamon rice cake in various flavors) and matcha KitKats are the right call"
              ]
            },
            {
              title: "Gion at Dusk — Kyoto's Most Beautiful Hour",
              description: "Walk 10 minutes east from Nishiki into Gion — Kyoto's most atmospheric district. Walk Hanamikoji Street from south to north as the stone lanterns light up and the machiya (wooden merchant townhouses) glow warm. Then find Shirakawa Lane: a narrow canal lined with weeping willows that in early March are beginning to bud, with stone lanterns reflecting in the water. This is Kyoto at its most beautiful. Solo: you can linger exactly as long as you want without anyone needing to be somewhere.",
              details: [
                "💡 Dusk to early evening (5–7pm) is the golden window — lanterns light up, tour groups thin out",
                "📸 Shirakawa Lane with lantern reflections on the water is the shot — it's 2 minutes north of Shijo on Shirakawa-dori",
                "🏮 Yasaka Shrine at the east end of Gion is beautiful lit up at night — free to enter anytime"
              ]
            }
          ],
          meals: [
            {
              type: "🍵 Afternoon Tea",
              name: "Nakamura Tokichi Honten — Gion matcha experience",
              description: "This tea house in Gion has served matcha since 1854. The matcha soft serve (Mr. Matcha soft cream) is one of the best things you'll eat in Japan — intensely bitter-sweet, deeply green. Also: matcha parfait, hojicha (roasted tea) soft serve, and traditional wagashi (Japanese sweets). Perfect Gion afternoon stop.",
              meta: "¥600–1,800 · Gion area · Walk-in · Short line expected"
            }
          ],
          tips: [
            { type: "reddit", text: "Gion on a quiet weekday evening in early March — after the tour groups leave and before the peak tourist season — is genuinely one of the most beautiful places I've ever been. Hanamikoji Street with the lanterns on, almost to yourself. It's worth the whole trip.", cite: "r/Kyoto" }
          ]
        },
        {
          label: "Evening — Return to Osaka",
          activities: [
            {
              title: "Kyoto Station → Osaka — Last Train, Omiyage Run",
              description: "Head to Kyoto Station for the JR Special Rapid back to Osaka (14 min, ¥570, every 15 min from Platforms 3–4). Before boarding, do a quick run through the Kyoto Station Isetan food basement — the best concentrated selection of Kyoto omiyage in one place: yatsuhashi (cinnamon rice cake, the definitive Kyoto sweet), matcha everything, Kyoto sake, beautifully packaged wagashi. 20 minutes, maximum efficiency.",
              details: [
                "🛍️ The Kyoto Station Isetan basement is better for omiyage than the airport — wider selection, lower prices",
                "🚆 Special Rapid: Kyoto → Osaka, ¥570 on IC card, 14 min"
              ]
            }
          ],
          meals: [
            {
              type: "🍜 Late Dinner in Osaka",
              name: "Namba street food or late ramen — keep it simple",
              description: "After a massive day, keep dinner easy. Option A: Dotonbori street food — takoyaki from Aizuya (Osaka's most beloved takoyaki stall, cash only, walk-up) + a cold Asahi from a 7-Eleven. Option B: Back to Ichiran for a late-night solo ramen ritual — the solo booth at midnight hits different after a Kyoto day. Option C: find a Namba izakaya still serving and order one or two things. You've been walking 25,000+ steps. Eat, sleep.",
              meta: "Street food: ¥300–800 · Namba/Dotonbori · Ichiran: ¥880–1,300, open until 5am"
            }
          ],
          tips: [
            { type: "tip", text: "The Kyoto day will wreck your legs in the best way. Pack good shoes and a small day pack. The reward is worth every step — but don't fight the tiredness tonight. Tomorrow is your last morning in Osaka." }
          ]
        }
      ]
    },
    {
      num: 4,
      title: "Last Morning: Namba, Markets & Farewell Osaka",
      neighborhoods: "Namba · Shinsaibashi · Dotonbori",
      date: "Mar 2",
      mapPins: [
        { lat: 34.6689, lng: 135.5042, label: "Kuromon Ichiba Morning", num: 1, cat: "food", desc: "Return to the market for a final morning graze — different vendors, same energy" },
        { lat: 34.6687, lng: 135.5013, label: "Dotonbori Farewell Walk", num: 2, cat: "activity", desc: "Morning Dotonbori — completely different from the neon-night version" },
        { lat: 34.6695, lng: 135.5034, label: "Namba Parks & Hōzen-ji Yokochō", num: 3, cat: "activity", desc: "Osaka's hidden moss-covered alley — quiet, atmospheric, tiny" },
        { lat: 34.6741, lng: 135.5014, label: "Shinsaibashi Last Shopping", num: 4, cat: "activity", desc: "Don Quijote, Uniqlo Japan-exclusive items, and final omiyage run" },
        { lat: 34.6734, lng: 135.5015, label: "Don Quijote Shinsaibashi", num: 5, cat: "activity", desc: "Japan's legendary discount store — snacks, character goods, chaos" },
        { lat: 34.6650, lng: 135.5010, label: "Namba Station — Nankai to KIX", num: 6, cat: "activity", desc: "Nankai Express to Kansai Airport — 38 min, ¥1,060" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Hōzen-ji Yokochō — Osaka's Hidden Moss Alley",
              description: "Walk to Hōzen-ji Yokochō — a tiny cobblestone alley near Dotonbori lined with moss-covered stone lanterns, small traditional restaurants, and the moss-covered Fudō-son statue at the end (people pour water on it for good luck — hence the moss). It's been here since 1637. 100 meters long. Completely serene compared to the Dotonbori chaos 30 meters away. Go in the morning when the alley is quiet. This is the Osaka that survived — narrow, personal, weathered.",
              details: [
                "📍 5 min walk from Dotonbori canal — look for the entrance near Namba Grand Kagetsu theater",
                "🗿 The moss-covered Fudō-son statue: pour a ladle of water over it. The accumulated water has grown that moss over decades.",
                "💡 The small restaurants here (kaiseki, traditional Japanese) are some of Osaka's most respected — worth a reservation on a future trip"
              ]
            },
            {
              title: "Kuromon Ichiba: Final Morning Market Run",
              description: "Return to Kuromon Ichiba for one last graze — the morning vendors are different from the afternoon crowd, and some of the best fresh sashimi stalls are set up by 9am. Get whatever you didn't try on Day 1. The fresh uni (sea urchin) and live scallops are best in the morning. Eat standing at the stall — Osaka's best eating is standing.",
              details: [
                "🦪 Morning highlight: grilled scallops with butter and soy — multiple stalls, ¥200–400 each",
                "🐡 Fugu (blowfish) season runs through February — if a stall has it, try it",
                "⏰ Market opens ~8–9am · Best selection before 11am"
              ]
            }
          ],
          meals: [
            {
              type: "🍳 Final Breakfast",
              name: "Dotonbori morning walk + Kuromon market graze",
              description: "Morning Dotonbori is a completely different experience from the neon-night version — quiet, a few vendors setting up, the canal reflecting pale morning sky. Walk it once, then head to Kuromon Ichiba for your actual breakfast: fresh grilled scallops, uni on rice, tamagoyaki, or whatever looks best. This is how Osaka eats in the morning.",
              meta: "¥800–1,500 total · Kuromon Ichiba · Cash · Arrive before 10am for freshest selection"
            }
          ],
          tips: [
            { type: "reddit", text: "I went back to Kuromon on my last morning just for one more scallop and ended up staying 90 minutes. Morning Osaka market grazing is somehow even better than afternoon — fewer people, everything is fresh, you feel like the city hasn't woken up yet and you're in on a secret.", cite: "r/osaka" }
          ]
        },
        {
          label: "Midday — Final Shopping & Departure",
          activities: [
            {
              title: "Shinsaibashi: The Last Shopping Sweep",
              description: "Final run through Shinsaibashi-suji and Amerikamura. The priorities: Don Quijote (Donki — 5 floors of barely organized discount goods, best place in Japan for variety snacks and character goods), Uniqlo for Japan-exclusive items that aren't available internationally, and any last-minute omiyage. Give yourself an hour. Japanese airport prices are notably higher than city prices for snacks — buy here, not at KIX.",
              details: [
                "🛍️ Don Quijote: best snack variety packs for omiyage — one-stop for all regional Japanese snacks, cheaper than Namba tourist shops",
                "👕 Uniqlo Shinsaibashi: 3 floors, Japan-exclusive UTme print designs and Japan-only colorways. Bring your size.",
                "💡 Set a hard stop time — allow 1.5 hours minimum to get to KIX from Namba Station"
              ]
            }
          ],
          meals: [
            {
              type: "🥞 Farewell Lunch or Early Airport Meal",
              name: "Okonomiyaki at Mizuno — Osaka's definitive farewell meal",
              description: "If time allows before heading to the airport: Mizuno in Namba has been making Osaka-style okonomiyaki since 1945. The yasai okonomiyaki (vegetable + egg + cabbage + batter, cooked on an iron griddle at your table, topped with Osaka sauce and mayo) is the city's most satisfying farewell meal. Lines form but move quickly. Otherwise: get an ekiben (station bento) at Namba Station for the airport express — often better food than the airport.",
              meta: "Mizuno: ¥1,000–1,800 · Namba, Dotonbori area · No reservation, line expected, moves fast | Ekiben: ¥800–1,200 · Namba Station convenience shops"
            }
          ],
          tips: [
            { type: "tip", text: "Nankai Rapid Express from Namba Station to Kansai International Airport (KIX): 38 minutes, ¥1,060 on ICOCA. Runs every 30 minutes. Allow 2 hours from Namba to your gate — KIX is large and international departures have long security queues. The city was good to you. Osaka always is." }
          ]
        }
      ]
    }
  ],
  budgetTable: [
    { category: "🚄 Osaka Metro / Transit (4 days)", estimated: "¥3,000–5,000", notes: "ICOCA card covers all trains and subways across Osaka + Kyoto day trip" },
    { category: "🛬 KIX → Namba Airport Express", estimated: "¥1,060 × 2", notes: "Nankai Rapid Express both ways" },
    { category: "🌅 Umeda Sky Building", estimated: "¥1,500", notes: "Open-air ring observatory at 173m" },
    { category: "🦊 Fushimi Inari Taisha", estimated: "Free", notes: "Always free, always open" },
    { category: "🌿 Tenryu-ji Zen Garden", estimated: "¥500–800", notes: "Garden entry ¥500, temple interior ¥300 extra" },
    { category: "✨ Kinkaku-ji", estimated: "¥500", notes: "Per person" },
    { category: "🗼 Tsutenkaku Tower (optional)", estimated: "¥1,000", notes: "Observation deck — optional, neighborhood is the real draw" },
    { category: "🍜 Meals — 4 days", estimated: "¥15,000–25,000", notes: "Solo eating in Osaka is remarkably affordable: ¥800–2,500 per meal" },
    { category: "🛍️ Omiyage / Shopping", estimated: "Varies", notes: "Budget ¥3,000–15,000 depending on willpower at Don Quijote" },
    { category: "✈️ TOTAL (excl. flights + hotel)", estimated: "¥25,000–40,000", notes: "Solo Osaka trip — roughly $165–265 USD for 4 days, excl. accommodations" }
  ],
  practicalInfo: [
    {
      title: "🗺️ Solo Navigation in Osaka",
      items: [
        "Google Maps handles Kansai transit perfectly — it knows every bus, subway, and JR line",
        "ICOCA card loaded with ¥5,000 covers all transit for the trip + initial load",
        "Coin lockers at Namba and Osaka Station: ¥300–700/day — use them on the Kyoto day trip",
        "7-Eleven ATMs: accept all international cards, no drama, 24 hours",
        "Osaka Namba and Shinsaibashi are 15-minute walking radius — most evenings you won't need transit"
      ]
    },
    {
      title: "🌡️ Late February / Early March Packing",
      items: [
        "Temperature range: 7–16°C · Layers are essential — cold mornings, warm afternoons",
        "Compact umbrella — February can bring rain without warning",
        "Good walking shoes — you'll do 20,000+ steps on the Kyoto day",
        "Small daypack for the Kyoto trip: water bottle, camera, light jacket to shed",
        "Cherry blossoms won't be out yet (peak: late March–early April) but plum blossoms are possible"
      ]
    },
    {
      title: "🍜 Solo Dining Tips for Osaka",
      items: [
        "Counter seats at any izakaya are normal and excellent for solo travelers",
        "Ichiran Ramen solo booths: literally designed for solo eating — order forms, bamboo curtains, bowls appear",
        "Standing ramen and soba shops: fastest, cheapest, most authentic solo lunch",
        "Kuromon Ichiba: designed for walking and eating — buy one, eat, walk, repeat",
        "Kombini (7-Eleven, Lawson, FamilyMart) are legitimate meal solutions — Japan's is exceptional"
      ]
    },
    {
      title: "🌃 Solo Nightlife Approach",
      items: [
        "Tachinomi bars (standing drink shops): inherently social — order at the window, stand with strangers",
        "Counter seats at izakayas = automatic neighbors. A nod and a raised glass requires no Japanese.",
        "Fukushima district (Day 2): most local, most intimate, best for solo drinkers who want neighborhood energy",
        "Amerikamura area (Days 1 & 3): higher energy, more English-friendly, better for bar-hopping",
        "Osaka nightlife peaks 9pm–midnight — this is a city that comes alive after dinner"
      ]
    },
    {
      title: "📱 Essential Apps",
      items: [
        "Google Maps — transit, walking, restaurant search. Works offline if you download Osaka/Kyoto maps.",
        "Google Translate — camera mode reads Japanese menus instantly",
        "HappyCow — if you want vegetarian options (very useful in Kyoto)",
        "Tabelog — Japanese restaurant reviews (use Google Translate camera to read it)",
        "USJ App — only needed if you add Universal Studios Japan to the trip"
      ]
    }
  ]
};

// Run fulfillment
(async () => {
  try {
    const result = fulfillOrder(order, itineraryData);
    console.log('✅ Fulfillment complete:', JSON.stringify(result, null, 2));
  } catch (err) {
    console.error('❌ Fulfillment failed:', err.message);
    process.exit(1);
  }
})();
