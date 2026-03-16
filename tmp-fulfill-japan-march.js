const fulfillOrder = require('./functions/fulfill-order');

const order = {
  id: 'order_1773640104252_xih28b',
  orderId: 'order_1773640104252_xih28b',
  email: 'paudcll4@gmail.com',
  startDate: '2026-03-17',
  customerName: null,
};

const itineraryData = {
  destination: "Japan",
  countryEmoji: "🇯🇵",
  title: "Spring Awakening: Late March Across Japan",
  subtitle: "Cherry blossoms, mountain onsen, temple stays & hidden traditions — 9 days through Hida, Kansai & Koyasan",
  description: "A season-optimized journey through central and western Japan, timed for early cherry blossoms, the Spring Equinox, and the transition from alpine winter to Kansai spring. From Takayama's Edo-period streets to overnight meditation at a mountaintop monastery, every day is planned around what's uniquely special in late March.",
  duration: "9 days",
  dates: "March 17 – 25, 2026",
  budget: "¥12,000–18,000/day (~$80–120 USD)",
  pace: "Active",
  bestFor: "Solo · Seasonal experiences · Off-the-beaten-path · Cultural immersion",

  highlights: [
    "Early cherry blossoms along Kyoto's Philosopher's Path and Maruyama Park",
    "Spring Equinox temple ceremonies at Kyoto's ancient shrines",
    "Overnight stay in a Buddhist temple on sacred Mt. Koya",
    "Hida beef and sake in Takayama's preserved Edo-period streets",
    "Open-air onsen in Gero — one of Japan's legendary top 3 hot spring towns"
  ],

  essentials: [
    { title: "🚄 Getting Around", text: "JR Pass is NOT cost-effective for this route (too many non-JR segments). Instead, buy individual tickets: Takayama–Gero (JR Takayama Line, ¥990), Gero–Kyoto (JR via Nagoya, ~¥7,500), Kyoto–Nara (Kintetsu, ¥640), Kyoto–Osaka (Hankyu Railway, ¥400), Osaka–Koyasan (Nankai Railway, ~¥1,650). IC card (Suica/ICOCA) works on local transport everywhere." },
    { title: "🏨 Accommodation Style", text: "Mix of budget hostels, capsule hotels, one ryokan night in Gero, and a temple lodging (shukubo) on Koyasan. Single rooms at ¥3,500–6,000/night in hostels, ¥8,000–12,000 for the ryokan, ¥10,000–13,000 for the temple stay." },
    { title: "🌸 Cherry Blossom Status", text: "Late March is the START of sakura season in Kansai. Kyoto's earliest bloomers (Toji, Maruyama Park weeping cherry) typically open March 20–25. Full bloom is usually late March to early April. You'll catch the magical 'opening' phase — less crowded than peak." },
    { title: "🗓️ Spring Equinox (Mar 20)", text: "Shunbun no Hi is a national holiday. Temples hold special higan ceremonies honoring ancestors. Expect larger crowds at major temples but also unique rituals you won't see other times of year." },
    { title: "💴 Budget Tips", text: "Konbini (7-Eleven, Lawson, FamilyMart) for cheap onigiri breakfasts (¥120–200). Lunch sets (ランチセット) at restaurants are 30–50% cheaper than dinner. Supermarket bento after 7pm are discounted 20–50%. Free temple grounds are often as beautiful as paid ones." },
    { title: "🌐 Language", text: "Google Translate camera mode works well for menus. Download Japanese offline pack before departure. Most train stations have English signage. In Takayama/Gero, English is less common — a few key phrases help." }
  ],

  days: [
    {
      num: 1,
      title: "Alpine Exit to Hida Heritage",
      neighborhoods: "Takayama · Sanmachi Suji · Hida Region",
      description: "Leave the snow behind and descend into Takayama's beautifully preserved Edo-period old town, where spring is just beginning to stir in the mountain valleys.",
      timeBlocks: [
        {
          label: "Morning — Travel & Arrival",
          activities: [
            {
              title: "Hakuba to Takayama",
              description: "Take the highway bus from Hakuba to Takayama (approximately 3 hours via Matsumoto transfer, or direct Nohi Bus seasonal route). Arrive by early afternoon.",
              details: [
                "🚌 Nohi Bus Hakuba–Takayama: check schedule at nouhibus.co.jp — if no direct, route via Matsumoto (Alpico Bus to Matsumoto, then JR Wide View Hida to Takayama)",
                "💰 Budget: ~¥4,500–5,500 total depending on route"
              ]
            }
          ],
          tips: [
            { type: "tip", text: "Grab an ekiben (station bento) at Matsumoto station if transferring — the Shinano-branded ones are excellent." }
          ]
        },
        {
          label: "Afternoon — Old Town Exploration",
          activities: [
            {
              title: "Sanmachi Suji Historic District",
              description: "Wander through the three streets of beautifully preserved Edo-era merchant houses. Dark wooden lattice facades, small sake breweries with cedar ball signs (sugidama), and craft shops line the canals.",
              details: [
                "🏠 Free to walk — open 24 hours",
                "📍 Best photo spots: the canal bridges with willow trees",
                "🍶 Look for the green sugidama (cedar balls) hanging outside — they indicate sake breweries offering tastings"
              ]
            },
            {
              title: "Sake Brewery Tasting Tour",
              description: "Takayama has 7 sake breweries clustered in the old town, most offering free or ¥100–300 tastings. In March, many are finishing their winter brewing season — the freshest sake of the year.",
              details: [
                "🍶 Funasaka Sake Brewery — oldest in town, try their seasonal namazake (unpasteurized)",
                "🍶 Harada Sake Brewery — small family operation, excellent junmai daiginjo",
                "⏰ Most close by 5pm — start by 3pm to visit 2–3"
              ]
            }
          ],
          meals: [
            { type: "🥩 Late Lunch", name: "Kyoya", description: "A5 Hida beef at an old-town restaurant. The lunch set (¥2,200) includes Hida beef steak with rice, miso soup, and pickles — a fraction of dinner prices.", meta: "📍 Sanmachi Suji area · ¥2,200–3,500" },
            { type: "🍜 Dinner", name: "Tsuzumi Soba", description: "Handmade buckwheat soba in a 100-year-old house. The wild mountain vegetable tempura (sansai tempura) is a Hida specialty available only in early spring.", meta: "📍 Near Miyagawa River · ¥1,200–1,800" }
          ]
        },
        {
          label: "Evening — Riverside Walk",
          activities: [
            {
              title: "Miyagawa River Evening Stroll",
              description: "Walk along the Miyagawa River as the streetlights reflect on the water. The eastern bank has a beautiful path with mountain views. In late March, look for the first plum blossoms along the riverbanks.",
              details: [
                "🏮 The Nakabashi Bridge is lit up at night — iconic red arch over the river",
                "♨️ Stop at one of the free ashiyu (foot baths) near the station area"
              ]
            }
          ],
          tips: [
            { type: "tip", text: "Takayama's morning markets (asaichi) start at 7am — set an alarm for tomorrow. They're one of the most authentic market experiences in Japan." }
          ]
        }
      ],
      mapPins: [
        { lat: 36.1408, lng: 137.2523, label: "Sanmachi Suji", num: 1, cat: "attraction", desc: "Edo-period merchant street district" },
        { lat: 36.1412, lng: 137.2535, label: "Funasaka Sake Brewery", num: 2, cat: "bar", desc: "Historic sake brewery with tastings" },
        { lat: 36.1395, lng: 137.2515, label: "Kyoya", num: 3, cat: "food", desc: "Hida beef lunch sets" },
        { lat: 36.1430, lng: 137.2510, label: "Nakabashi Bridge", num: 4, cat: "attraction", desc: "Iconic red bridge over Miyagawa River" },
        { lat: 36.1420, lng: 137.2505, label: "Tsuzumi Soba", num: 5, cat: "food", desc: "Handmade soba in 100-year-old house" }
      ]
    },

    {
      num: 2,
      title: "Morning Markets & Mountain Hot Springs",
      neighborhoods: "Takayama Markets · Gero Onsen",
      description: "Experience Takayama's famous morning markets at dawn, then ride the scenic JR Takayama Line south through dramatic gorges to one of Japan's legendary top 3 onsen towns.",
      timeBlocks: [
        {
          label: "Early Morning — Markets",
          activities: [
            {
              title: "Miyagawa Morning Market (Asaichi)",
              description: "One of Japan's three great morning markets, running along the Miyagawa River since the Edo period. Local farmers sell mountain vegetables, homemade pickles, miso paste, handcrafts, and seasonal specialties. In March, look for fukujuso (spring wildflowers) and fresh wasabi.",
              details: [
                "⏰ 7:00am–12:00pm (opens early, best before 9am)",
                "📍 Eastern bank of Miyagawa River, ~700m of stalls",
                "🛒 Try: sarubobo charms (lucky dolls), mitarashi dango (grilled rice dumplings, ¥100), fresh apple juice"
              ]
            },
            {
              title: "Jinya-mae Morning Market",
              description: "The smaller, more intimate market in front of the Takayama Jinya (historic government building). More focused on local crafts and pickled vegetables.",
              details: [
                "⏰ 7:00am–12:00pm",
                "🏯 Peek into the Takayama Jinya courtyard (¥440 entry) — the only remaining Edo-era provincial government building in Japan"
              ]
            }
          ],
          meals: [
            { type: "🍡 Breakfast", name: "Market stalls", description: "Mitarashi dango (sweet soy-glazed rice dumplings, ¥100), gohei mochi (walnut-miso glazed rice cakes), and hot amazake (sweet rice drink) — the perfect cold morning market breakfast.", meta: "📍 Miyagawa River market stalls · ¥300–500 total" }
          ]
        },
        {
          label: "Midday — Scenic Train to Gero",
          activities: [
            {
              title: "JR Takayama Line to Gero Onsen",
              description: "One of Japan's most scenic rail journeys. The single-track train winds through the Hida River gorge, past steep forested mountains and tiny villages. The 50-minute ride feels like traveling back in time.",
              details: [
                "🚂 JR Takayama Line: ~50 min, ¥990",
                "💺 Sit on the LEFT side for the best river gorge views",
                "📷 Best photo spot: the stretch between Hida-Kanayama and Gero where the train hugs the cliff"
              ]
            }
          ]
        },
        {
          label: "Afternoon — Gero Onsen Town",
          activities: [
            {
              title: "Explore Gero Onsen",
              description: "One of Japan's top 3 onsen towns (alongside Kusatsu and Arima). The town is compact and walkable along the Hida River. The water is uniquely silky-smooth (alkaline simple spring, pH 9.18) — called 'bijin no yu' (beauty's bath) because it makes skin incredibly soft.",
              details: [
                "🎫 Buy a Yumeguri Tegata pass (¥1,300) — access 3 different ryokan baths in town",
                "♨️ Free foot baths along the river at Bi no Ashiyu and near Gero Station",
                "🐸 The town mascot is a frog (gero = frog sound in Japanese) — frog statues everywhere"
              ]
            },
            {
              title: "Onsen Hopping",
              description: "With your Yumeguri pass, visit different ryokan baths with distinct characters. Each has a different view and atmosphere — riverside, garden, or mountain-facing.",
              details: [
                "♨️ Suimeikan — grand riverside bath with outdoor rotenburo overlooking the river",
                "♨️ Ogawaya — intimate wooden bath with garden views",
                "⏰ Most baths open 12pm–3pm for day visitors"
              ]
            }
          ],
          meals: [
            { type: "🍖 Lunch", name: "Senri Restaurant", description: "Tomato-based Hida beef stew (Gero's unique local dish) or keichan — miso-marinated chicken grilled at your table, a Hida specialty.", meta: "📍 Near Gero Station · ¥1,000–1,500" },
            { type: "🍱 Dinner", name: "Ryokan Kaiseki", description: "Let your ryokan serve a multi-course kaiseki dinner featuring local river fish (ayu), Hida beef, mountain vegetables, and seasonal spring dishes. This is included in most ryokan stays.", meta: "📍 Your ryokan · Included with stay" }
          ],
          tips: [
            { type: "tip", text: "Budget ryokan option: Gero Onsen Mutsumikan offers single rooms from ¥8,000 including dinner and breakfast. Book on Jalan.net for best prices." }
          ]
        },
        {
          label: "Evening — Riverside Rotenburo",
          activities: [
            {
              title: "Funsenchi Open-Air Bath",
              description: "A legendary free mixed-gender open-air bath right on the riverbank in the center of town. Bathing under the stars with the sound of the Hida River is unforgettable. In March, the night air is crisp — perfect contrast with the hot water.",
              details: [
                "♨️ Free, open 24 hours — swimsuits allowed (unusual for Japan)",
                "📍 Right next to Gero Ohashi bridge, center of town",
                "⚠️ Very open/public — if you're shy, the foot baths nearby are a good alternative"
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 36.1425, lng: 137.2520, label: "Miyagawa Morning Market", num: 1, cat: "shopping", desc: "Famous Edo-period morning market" },
        { lat: 36.1390, lng: 137.2530, label: "Jinya-mae Market", num: 2, cat: "shopping", desc: "Market by historic government building" },
        { lat: 35.8051, lng: 137.2437, label: "Gero Station", num: 3, cat: "transport", desc: "Gateway to Gero Onsen" },
        { lat: 35.8025, lng: 137.2455, label: "Suimeikan", num: 4, cat: "attraction", desc: "Grand riverside onsen" },
        { lat: 35.8037, lng: 137.2445, label: "Funsenchi Open-Air Bath", num: 5, cat: "attraction", desc: "Free riverside rotenburo" }
      ]
    },

    {
      num: 3,
      title: "Into the Cherry Blossom Belt",
      neighborhoods: "Gero · Nagoya Transfer · Higashiyama · Gion",
      description: "Travel south from the mountains into Kyoto — where the first cherry blossoms of the season are just beginning to open. The temperature shift from Hida's alpine chill to Kansai's milder spring feels like fast-forwarding through seasons.",
      timeBlocks: [
        {
          label: "Morning — Departure from Gero",
          activities: [
            {
              title: "Ryokan Breakfast & Check-out",
              description: "Enjoy a traditional Japanese breakfast at the ryokan — grilled fish, miso soup, pickled vegetables, rice, and tamago (egg). Check out and catch the JR Wide View Hida toward Nagoya.",
              details: [
                "🚂 JR Gero → Nagoya (~1h40), then Shinkansen Nagoya → Kyoto (~35min)",
                "💰 Total: ~¥7,500 (or use Hida–Kyoto discount ticket if available)",
                "📦 Use takkyubin luggage forwarding from your ryokan to your Kyoto hotel (~¥2,000) to travel light"
              ]
            }
          ]
        },
        {
          label: "Afternoon — First Steps in Kyoto",
          activities: [
            {
              title: "Philosopher's Path (Tetsugaku no Michi)",
              description: "A 2km stone path along a canal lined with hundreds of cherry trees. In late March, the earliest varieties will be showing pink buds or first blossoms. Even before full bloom, the atmosphere is magical — anticipation fills the air.",
              details: [
                "🌸 Somei Yoshino trees here typically start opening March 22–28",
                "📍 Walk south to north: start near Nanzenji, end near Ginkaku-ji",
                "🕐 ~45 minutes to walk, longer with photo stops and temple detours",
                "🆓 Free to walk anytime"
              ]
            },
            {
              title: "Nanzen-ji Temple",
              description: "A grand Zen temple at the southern end of the Philosopher's Path. The massive sanmon gate offers views over the city (¥600). The aqueduct behind the main hall — a Meiji-era brick structure cutting through the ancient temple — is one of Kyoto's most striking photo spots.",
              details: [
                "⏰ 8:40am–5:00pm, grounds free, sanmon gate ¥600",
                "📷 The brick aqueduct is free to see and incredibly photogenic",
                "🌸 Early-blooming cherry trees in the grounds"
              ]
            }
          ],
          meals: [
            { type: "🍜 Lunch", name: "Omen Nippon", description: "Famous udon noodle restaurant near the Philosopher's Path. Their signature dish is thick handmade udon with seasonal dipping sauce and a plate of fresh vegetables and condiments you add yourself.", meta: "📍 Near Ginkaku-ji · ¥1,200–1,600" }
          ]
        },
        {
          label: "Evening — Gion at Dusk",
          activities: [
            {
              title: "Gion District Evening Walk",
              description: "Kyoto's most atmospheric neighborhood at its best hour. Wooden machiya townhouses, paper lanterns, and the occasional glimpse of a maiko (apprentice geisha) heading to an evening engagement. Hanami-koji is the main street, but the side alleys (especially Shinbashi-dori) are more atmospheric.",
              details: [
                "📍 Start at Shijo-dori and walk south through Hanami-koji",
                "📍 Shinbashi-dori — the most photographed street in Kyoto, with willow trees and traditional facades",
                "🌸 The Shirakawa Canal area near Gion has early-blooming weeping cherries (shidare-zakura) that open before Somei Yoshino",
                "⚠️ No photography of geiko/maiko without permission — observe respectfully"
              ]
            }
          ],
          meals: [
            { type: "🍣 Dinner", name: "Gion Kappa", description: "A tiny counter-style restaurant in Gion serving excellent sushi at reasonable prices. The master serves seasonal fish — in March, look for sayori (halfbeak) and hotaru ika (firefly squid), both spring specialties.", meta: "📍 Gion, Higashiyama · ¥2,500–4,000" }
          ],
          tips: [
            { type: "tip", text: "Accommodation: Hotel Ethnography Gion Shinmonzen — beautiful machiya-style boutique hotel from ¥5,500/night for singles. Or Piece Hostel Sanjo for budget (¥3,200/night) with great location." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0158, lng: 135.7942, label: "Philosopher's Path", num: 1, cat: "attraction", desc: "Cherry blossom-lined canal walk" },
        { lat: 35.0112, lng: 135.7933, label: "Nanzen-ji", num: 2, cat: "attraction", desc: "Grand Zen temple with aqueduct" },
        { lat: 35.0267, lng: 135.7842, label: "Omen Nippon", num: 3, cat: "food", desc: "Famous handmade udon" },
        { lat: 35.0038, lng: 135.7755, label: "Gion Hanami-koji", num: 4, cat: "attraction", desc: "Geisha district main street" },
        { lat: 35.0050, lng: 135.7745, label: "Shinbashi-dori", num: 5, cat: "attraction", desc: "Most photogenic street in Kyoto" },
        { lat: 35.0042, lng: 135.7760, label: "Gion Kappa", num: 6, cat: "food", desc: "Counter sushi with seasonal fish" }
      ]
    },

    {
      num: 4,
      title: "Spring Equinox & Sacred Mountains",
      neighborhoods: "Fushimi · Arashiyama · Nishiki Market",
      description: "March 20 is Shunbun no Hi — the Spring Equinox, a national holiday when Japanese families visit temples for ancestral ceremonies. Experience Kyoto's greatest hits at a profound seasonal moment.",
      timeBlocks: [
        {
          label: "Early Morning — Fushimi Inari",
          activities: [
            {
              title: "Fushimi Inari Taisha at Sunrise",
              description: "The famous 10,000 vermillion torii gates winding up Mt. Inari. At sunrise (around 6:00am in late March), you'll have the lower gates almost to yourself. The full hike to the summit takes about 2 hours and rewards with panoramic views over Kyoto.",
              details: [
                "⏰ Open 24 hours, arrive by 6:00am for empty gates",
                "🆓 Completely free",
                "⛰️ Full summit hike: ~2 hours round trip, 233m elevation",
                "📷 The 'tunnel of gates' effect is strongest on the Senbon Torii section (first 20 minutes)"
              ]
            }
          ],
          meals: [
            { type: "🍙 Breakfast", name: "Vermillion Café", description: "Espresso and a light breakfast right near the shrine entrance. Or grab inari-zushi (sweet tofu pocket sushi — named after this very shrine) from the stalls on the approach path.", meta: "📍 Fushimi Inari approach · ¥400–800" }
          ]
        },
        {
          label: "Late Morning — Arashiyama",
          activities: [
            {
              title: "Arashiyama Bamboo Grove",
              description: "Walk through the towering bamboo stalks of Sagano. The grove is most atmospheric in the morning light when sunbeams filter through. Continue past to Okochi Sanso villa garden (¥1,000 incl. matcha) for stunning mountain views.",
              details: [
                "📍 JR Saga-Arashiyama station or Hankyu Arashiyama — 20 min from central Kyoto",
                "🆓 Bamboo grove is free, Okochi Sanso ¥1,000",
                "🌸 The area around Togetsukyo Bridge has early cherry trees"
              ]
            },
            {
              title: "Tenryu-ji Temple",
              description: "A UNESCO World Heritage Zen temple with one of Japan's oldest and finest landscape gardens. The garden was designed in the 14th century to 'borrow' the Arashiyama mountains as backdrop — stunning in any season.",
              details: [
                "⏰ 8:30am–5:00pm, garden ¥500",
                "🌸 Several early-blooming cherry trees in the garden"
              ]
            }
          ],
          meals: [
            { type: "🍜 Lunch", name: "Yoshimura Soba", description: "Handmade soba with a window seat overlooking the Togetsukyo Bridge and Arashiyama mountains. Their tempura soba with seasonal mountain vegetables is perfect for March.", meta: "📍 Right by Togetsukyo Bridge · ¥1,200–1,800" }
          ]
        },
        {
          label: "Afternoon — Spring Equinox Traditions",
          activities: [
            {
              title: "Nishiki Market",
              description: "Kyoto's 400-year-old 'kitchen' — a narrow covered market stretching five blocks with over 100 vendors. Sample seasonal specialties: yomogi mochi (mugwort rice cakes, a spring tradition), tsukemono (Kyoto pickles), and dashimaki tamago (rolled omelette).",
              details: [
                "📍 Nishiki-koji, between Teramachi and Takakura streets",
                "⏰ Most shops 9:00am–5:00pm, some close by 4pm",
                "💰 Budget ¥1,000–2,000 for snacking through the market",
                "🎌 Being a holiday, it'll be lively with Japanese families"
              ]
            },
            {
              title: "Higashi Hongan-ji — Equinox Ceremony",
              description: "One of Kyoto's largest temples holds special Higan services during the equinox week. The massive main hall (the largest wooden structure in Kyoto) hosts chanting ceremonies that are deeply moving even if you don't understand the words.",
              details: [
                "🆓 Free entry, ceremonies throughout the day",
                "📍 5-minute walk from Kyoto Station",
                "🙏 Higan = 'other shore' — the Buddhist concept of reaching enlightenment, celebrated during equinox when day and night are balanced"
              ]
            }
          ],
          tips: [
            { type: "reddit", text: "The Spring Equinox temple ceremonies are something most tourists miss entirely. The chanting at the big Higashi Honganji is genuinely spiritual even for non-Buddhists.", cite: "r/JapanTravel" }
          ]
        },
        {
          label: "Evening — Maruyama Park Illuminations",
          activities: [
            {
              title: "Maruyama Park Night Cherry Blossoms",
              description: "Kyoto's most famous hanami spot. The iconic weeping cherry tree (shidare-zakura) in the center of the park is illuminated at night and is often one of the first trees to bloom in Kyoto. Even if it's not fully open yet, the lighting and atmosphere are extraordinary.",
              details: [
                "🌸 The weeping cherry here typically blooms March 20–28 (before Somei Yoshino)",
                "🏮 Illumination runs sunset to midnight during blossom season",
                "📍 Adjacent to Yasaka Shrine (free, always open)",
                "🆓 Free — bring a convenience store snack and find a spot to sit"
              ]
            }
          ],
          meals: [
            { type: "🍢 Dinner", name: "Yatai Food Stalls at Maruyama Park", description: "During cherry blossom season, dozens of yatai (food stalls) set up in the park. Takoyaki, yakitori, okonomiyaki, warm sake — eat dinner under the illuminated trees like the locals.", meta: "📍 Maruyama Park · ¥1,000–2,000 for a full meal from stalls" }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: "Fushimi Inari Taisha", num: 1, cat: "attraction", desc: "10,000 vermillion torii gates" },
        { lat: 35.0165, lng: 135.6717, label: "Arashiyama Bamboo Grove", num: 2, cat: "attraction", desc: "Towering bamboo forest" },
        { lat: 35.0155, lng: 135.6740, label: "Tenryu-ji Temple", num: 3, cat: "attraction", desc: "UNESCO World Heritage Zen garden" },
        { lat: 35.0050, lng: 135.7650, label: "Nishiki Market", num: 4, cat: "food", desc: "400-year-old covered food market" },
        { lat: 34.9914, lng: 135.7520, label: "Higashi Hongan-ji", num: 5, cat: "attraction", desc: "Equinox ceremonies" },
        { lat: 35.0035, lng: 135.7810, label: "Maruyama Park", num: 6, cat: "attraction", desc: "Night cherry blossom illuminations" },
        { lat: 35.0160, lng: 135.6697, label: "Yoshimura Soba", num: 7, cat: "food", desc: "Soba with Togetsukyo Bridge views" }
      ]
    },

    {
      num: 5,
      title: "Deer, Giants & Ancient Capital",
      neighborhoods: "Nara · Nara Park · Naramachi",
      description: "A full day in Japan's first permanent capital, where sacred deer roam freely among some of the largest and oldest wooden structures on Earth. In late March, the park's plum gardens are in their final bloom and cherry trees are budding.",
      timeBlocks: [
        {
          label: "Morning — Sacred Deer & Great Buddha",
          activities: [
            {
              title: "Nara Park at Dawn",
              description: "Over 1,200 wild Sika deer roam freely through the park — they're considered divine messengers of the gods in Shinto tradition. In the morning, they're calm and approachable. Buy shika senbei (deer crackers, ¥200) to make friends.",
              details: [
                "🦌 Free to enter, always open",
                "📍 ~45 min from Kyoto via Kintetsu Railway (¥640)",
                "🌸 The park has early-blooming cherry trees near Ukimido Pavilion and along Sagi-ike pond"
              ]
            },
            {
              title: "Todai-ji & the Great Buddha",
              description: "The world's largest wooden building houses a 15-meter bronze Buddha cast in 752 AD. The scale is genuinely awe-inspiring — this is NOT a 20-minute castle experience. Between the deer park approach, the Nandaimon gate guardians, and the Daibutsuden hall, plan at least 90 minutes.",
              details: [
                "⏰ 8:00am–5:00pm, ¥600",
                "📷 The Nandaimon gate guardians (Nio statues) are 8.4m tall masterpieces from 1203",
                "🤏 Try the famous 'nostril pillar' — a column with a hole the same size as the Great Buddha's nostril. Crawling through supposedly brings enlightenment"
              ]
            }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Kuruminotaki Café", description: "A hidden café near Nara Park serving excellent coffee and toast sets in a renovated machiya. Peaceful morning start before the crowds arrive.", meta: "📍 Near Nara Park entrance · ¥600–900" }
          ]
        },
        {
          label: "Midday — Ancient Temple Circuit",
          activities: [
            {
              title: "Kasuga Taisha Grand Shrine",
              description: "A Shinto shrine famous for its 3,000 stone and bronze lanterns, many moss-covered and centuries old. The approach through a primeval forest is otherworldly. The shrine holds special Higan ceremonies in the equinox period.",
              details: [
                "⏰ 7:00am–5:00pm, inner sanctuary ¥500",
                "🏮 The lantern-lit festivals (Mantoro) happen in Feb and Aug, but even normally the hundreds of stone lanterns along the path are incredible",
                "🌿 The surrounding Kasugayama Primeval Forest is a UNESCO site — untouched for 1,000 years"
              ]
            },
            {
              title: "Nigatsu-do Hall",
              description: "Part of the Todai-ji complex but often missed. This hillside hall has a balcony with the best panoramic view in Nara — overlooking the entire city and Nara Park. The Omizutori fire ceremony runs through March 14, but the venue itself is stunning year-round.",
              details: [
                "🆓 Free, always open",
                "📷 Best view in Nara — sunset from this balcony is unforgettable",
                "🔥 Even after Omizutori, you can see the charred balcony railings from the fire torches"
              ]
            }
          ],
          meals: [
            { type: "🍜 Lunch", name: "Kakinoha Sushi at Tanaka", description: "Nara's signature dish: sushi wrapped in persimmon leaves (kakinoha-zushi). The leaves impart a subtle fragrance and act as natural preservation — an Edo-era innovation. Tanaka makes them fresh daily.", meta: "📍 Naramachi area · ¥900–1,500" }
          ]
        },
        {
          label: "Afternoon — Naramachi",
          activities: [
            {
              title: "Naramachi Traditional District",
              description: "Nara's old merchant quarter with narrow machiya townhouses, small museums, and artisan shops. Much less touristed than Kyoto's old districts. Look for the migawari-zaru (protective monkey charms) hanging from eaves — a Naramachi tradition.",
              details: [
                "🏠 Free to wander, several free small museums",
                "🐒 Migawari-zaru (red cloth monkey charms) protect households from evil — unique to Naramachi",
                "🍵 Stop at Nakatanidou for freshly pounded mochi — the owner does a famous rapid mochi-pounding performance"
              ]
            }
          ],
          meals: [
            { type: "🍱 Dinner", name: "Harise", description: "A 200-year-old restaurant in Naramachi famous for kamameshi (rice cooked in an iron pot with seasonal ingredients). The spring version has bamboo shoots, mountain vegetables, and shrimp.", meta: "📍 Naramachi · ¥1,800–2,500" }
          ],
          tips: [
            { type: "tip", text: "Return to Kyoto via Kintetsu (¥640, 45 min). If you want to continue to Osaka tomorrow instead, you could stay overnight in Nara — Sun Hotel Nara has singles from ¥3,800." }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6892, lng: 135.8399, label: "Nara Park", num: 1, cat: "attraction", desc: "1,200 sacred deer roam freely" },
        { lat: 34.6890, lng: 135.8398, label: "Todai-ji", num: 2, cat: "attraction", desc: "World's largest wooden building, Great Buddha" },
        { lat: 34.6812, lng: 135.8489, label: "Kasuga Taisha", num: 3, cat: "attraction", desc: "3,000 stone lanterns in ancient forest" },
        { lat: 34.6907, lng: 135.8415, label: "Nigatsu-do", num: 4, cat: "attraction", desc: "Best panoramic view in Nara" },
        { lat: 34.6780, lng: 135.8310, label: "Naramachi", num: 5, cat: "attraction", desc: "Traditional merchant quarter" },
        { lat: 34.6785, lng: 135.8315, label: "Harise", num: 6, cat: "food", desc: "200-year-old kamameshi restaurant" }
      ]
    },

    {
      num: 6,
      title: "Street Food Capital of the World",
      neighborhoods: "Osaka · Dotonbori · Shinsekai · Namba",
      description: "Swap Kyoto's refined elegance for Osaka's raw, neon-lit, unapologetically loud food culture. This city eats harder than anywhere else in Japan — kuidaore (eat until you drop) is the local motto.",
      timeBlocks: [
        {
          label: "Morning — Travel & Tenma Food Market",
          activities: [
            {
              title: "Kyoto to Osaka",
              description: "Quick transfer via Hankyu Railway (¥400, 45 min to Umeda) or JR (¥570, 30 min to Osaka Station).",
              details: [
                "📦 Drop bags at hotel or use coin lockers at Osaka/Umeda Station (¥400–700)"
              ]
            },
            {
              title: "Tenjinbashisuji Shopping Street & Tenma Market",
              description: "Japan's longest covered shopping street (2.6km!) plus the adjacent Tenma market — where Osaka's restaurant owners buy their ingredients. Much more local than Kuromon. Browse dried fish, tofu stalls, knife shops, and hole-in-the-wall udon joints.",
              details: [
                "📍 Tenjinbashisuji station (Sakaisuji Line)",
                "🆓 Free to walk, plan 1–1.5 hours",
                "🍢 Try korokke (croquettes) from the street stalls — ¥100–150 each"
              ]
            }
          ],
          meals: [
            { type: "🍜 Brunch", name: "Daruma Kushi-katsu (Tenma branch)", description: "Deep-fried skewered everything — from pork and shrimp to lotus root, mochi, and even cheese. The legendary no-double-dipping sauce rule applies. A Shinsekai original with a branch near Tenma.", meta: "📍 Near Tenjinbashi · ¥1,000–1,500 for 8–10 skewers" }
          ]
        },
        {
          label: "Afternoon — Dotonbori & Namba",
          activities: [
            {
              title: "Dotonbori Canal Walk",
              description: "Osaka's iconic neon strip along the canal — giant mechanical crabs, the Glico Running Man sign, and an overwhelming density of restaurants. It's tacky and loud and absolutely wonderful.",
              details: [
                "📍 Namba Station, 5-minute walk east",
                "📷 Best photos from the Ebisu Bridge at night, but afternoon lets you eat without insane queues",
                "🛍️ Side streets (especially Hozenji Yokocho — a stone-paved alley with a moss-covered Buddha) are more atmospheric"
              ]
            },
            {
              title: "Hozenji Yokocho",
              description: "A tiny stone alley hidden behind Dotonbori's chaos. The Hozenji temple's moss-covered Fudo Myoo statue is beloved — splash water on it and make a wish. Lined with intimate bars and traditional restaurants.",
              details: [
                "🆓 Free, always open",
                "🌿 The moss grows from all the water visitors splash — it's thick and green, almost surreal next to the neon",
                "🍶 Several tiny standing bars here for afternoon sake"
              ]
            }
          ],
          meals: [
            { type: "🐙 Snack", name: "Takoyaki at Kukuru", description: "Osaka's soul food: crispy-outside, molten-inside octopus balls. Kukuru at Dotonbori is consistent and uses whole octopus legs. Eat them fresh — the inside is lava.", meta: "📍 Dotonbori canal · ¥600 for 8 pieces" },
            { type: "🥞 Snack", name: "Okonomiyaki at Mizuno", description: "Osaka-style savory pancake loaded with cabbage, pork, seafood, and topped with sweet sauce, mayo, bonito flakes, and seaweed. Mizuno has been doing this since 1945 — queues but worth it.", meta: "📍 Dotonbori · ¥1,200–1,800" }
          ]
        },
        {
          label: "Evening — Shinsekai & Night Culture",
          activities: [
            {
              title: "Shinsekai District",
              description: "Osaka's retro entertainment district built in 1912, modeled after New York (north) and Paris (south). Today it's gloriously run-down and authentic — puffer fish lanterns, shogi (chess) cafes, and the best kushikatsu joints in the city. Tsutenkaku Tower glows above it all.",
              details: [
                "📍 Dobutsuen-mae Station (Midosuji Line)",
                "🗼 Tsutenkaku Tower: ¥900 for observation deck (optional — views are decent but Umeda Sky Building is better)",
                "🎮 Retro arcade games in the Jan Jan Yokocho alley"
              ]
            },
            {
              title: "Tobita Shinchi (Walk Through Only)",
              description: "Japan's most visually striking historic red-light area (operating since the Taisho era). The architecture — ornate facades with elaborate lighting — is extraordinary to walk past. Respectful observation only; no photos of people.",
              details: [
                "📍 2 blocks south of Shinsekai",
                "⚠️ Walk through, observe architecture only, no photography of people. Respectful curiosity."
              ]
            }
          ],
          meals: [
            { type: "🍺 Dinner", name: "Toyo (Standing Sashimi Bar)", description: "A legendary standing counter in Shinsekai serving massive portions of fresh sashimi, grilled seafood, and tuna cheek at absurdly low prices. The owner shouts your order theatrically. Pure Osaka.", meta: "📍 Shinsekai · ¥1,500–2,500 for a feast" }
          ],
          tips: [
            { type: "tip", text: "Accommodation: Hostel 64 Osaka in Namba has single capsules from ¥2,800 with great common space. Or Book and Bed Shinsaibashi — sleep inside a bookshelf (¥3,500)." }
          ]
        }
      ],
      mapPins: [
        { lat: 34.7055, lng: 135.5120, label: "Tenjinbashisuji Street", num: 1, cat: "shopping", desc: "Japan's longest covered shopping street" },
        { lat: 34.6687, lng: 135.5014, label: "Dotonbori", num: 2, cat: "attraction", desc: "Iconic neon canal strip" },
        { lat: 34.6680, lng: 135.5010, label: "Hozenji Yokocho", num: 3, cat: "attraction", desc: "Hidden stone alley with moss Buddha" },
        { lat: 34.6525, lng: 135.5063, label: "Shinsekai", num: 4, cat: "attraction", desc: "Retro entertainment district" },
        { lat: 34.6523, lng: 135.5065, label: "Toyo Sashimi Bar", num: 5, cat: "food", desc: "Standing counter sashimi legend" },
        { lat: 34.6690, lng: 135.5020, label: "Kukuru Takoyaki", num: 6, cat: "food", desc: "Osaka soul food" }
      ]
    },

    {
      num: 7,
      title: "Castle Gardens & Sky Views",
      neighborhoods: "Osaka Castle · Kuromon · Umeda",
      description: "Explore Osaka's green spaces and elevated perspectives — from the castle's plum and cherry gardens to one of the most spectacular observation decks in all of Japan.",
      timeBlocks: [
        {
          label: "Morning — Osaka Castle Park",
          activities: [
            {
              title: "Osaka Castle & Nishinomaru Garden",
              description: "The castle itself is a concrete reconstruction (1931), but the surrounding park is one of Osaka's best spring spots. Nishinomaru Garden (¥200) has 300 cherry trees — in late March, the earliest varieties should be opening. The plum grove (bairin) behind the castle will be in its final bloom.",
              details: [
                "⏰ Park: always open. Castle tower: 9am–5pm (¥600). Nishinomaru Garden: 9am–5pm (¥200)",
                "🌸 Nishinomaru cherry trees + castle tower = quintessential Japan photo",
                "📍 Morinomiya or Osakajokoen Station",
                "🏯 Skip the castle interior if short on time — it's a museum, not authentic rooms"
              ]
            }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Moto Coffee", description: "Specialty coffee in a beautiful industrial space near Osaka Castle. Excellent pour-overs and toast sets. A morning ritual for local creatives.", meta: "📍 Tanimachi 4-chome · ¥500–800" }
          ]
        },
        {
          label: "Midday — Kuromon Market",
          activities: [
            {
              title: "Kuromon Ichiba Market",
              description: "Osaka's 'Kitchen' — 170+ stalls of impossibly fresh seafood, seasonal fruits, and street food. More tourist-oriented than Tenma but the quality is undeniable. The giant grilled scallops and uni (sea urchin) are irresistible.",
              details: [
                "⏰ 9am–5pm (many stalls close by 4pm)",
                "📍 Nippombashi Station",
                "💰 Budget ¥1,500–3,000 for a market lunch",
                "🦐 Must try: grilled king crab leg (¥1,000–1,500), fresh uni (¥500–800), tamagoyaki (¥200)"
              ]
            }
          ],
          meals: [
            { type: "🐟 Lunch", name: "Kuromon Market Grazing", description: "Eat your way through — fresh uni, grilled scallops, A5 wagyu skewers, seasonal fruit mochi. Buy from multiple stalls and eat standing or at their counters.", meta: "📍 Kuromon Market · ¥2,000–3,000" }
          ]
        },
        {
          label: "Afternoon — Den Den Town",
          activities: [
            {
              title: "Den Den Town (Osaka's Akihabara)",
              description: "Osaka's electronics and otaku district — retro game shops, vintage synthesizer stores, manga cafes, and figure shops. More compact and less overwhelming than Akihabara. Great for browsing even if you're not buying.",
              details: [
                "📍 Between Nippombashi and Ebisucho stations",
                "🎮 Super Potato: multi-floor retro game paradise — play old arcade cabinets for ¥100",
                "🎵 Look for the vintage audio/synth shops if you're into music gear"
              ]
            }
          ]
        },
        {
          label: "Evening — Umeda Sky Building",
          activities: [
            {
              title: "Umeda Sky Building Floating Garden",
              description: "One of the most extraordinary building designs in Japan — two towers connected by a 'floating' circular observation deck 173m above the ground. The open-air rooftop is especially magical at sunset, with luminous floor panels that glow in the dark.",
              details: [
                "⏰ 9:30am–10:30pm (last entry 10pm), ¥1,500",
                "📷 Time for sunset (~6:15pm in late March) — arrive 30 min before",
                "🌃 The underground Takimi-koji alley recreates 1920s Osaka with retro restaurants"
              ]
            }
          ],
          meals: [
            { type: "🍜 Dinner", name: "Takimi-koji Retro Alley", description: "The basement of the Sky Building recreates a 1920s Osaka street with lanterns, wooden facades, and nostalgic restaurants. Several excellent ramen, udon, and izakaya options in a time-warp setting.", meta: "📍 Umeda Sky Building B1 · ¥1,000–1,800" }
          ],
          tips: [
            { type: "reddit", text: "Umeda Sky Building at sunset is better than any Tokyo observation deck. The open-air design means no glass reflections in your photos. Go 30 min before sunset for the golden hour transition.", cite: "r/JapanTravel" }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6873, lng: 135.5262, label: "Osaka Castle", num: 1, cat: "attraction", desc: "Castle + cherry blossom gardens" },
        { lat: 34.6686, lng: 135.5069, label: "Kuromon Market", num: 2, cat: "food", desc: "Osaka's Kitchen — fresh seafood" },
        { lat: 34.6600, lng: 135.5058, label: "Den Den Town", num: 3, cat: "shopping", desc: "Retro games and otaku culture" },
        { lat: 34.7052, lng: 135.4902, label: "Umeda Sky Building", num: 4, cat: "attraction", desc: "Floating Garden observation deck" },
        { lat: 34.6880, lng: 135.5240, label: "Moto Coffee", num: 5, cat: "food", desc: "Specialty coffee near the castle" }
      ]
    },

    {
      num: 8,
      title: "The Sacred Mountain",
      neighborhoods: "Osaka · Koyasan · Okunoin Cemetery",
      description: "Leave the urban energy behind for one of Japan's most profound spiritual experiences — an overnight stay in a Buddhist temple on the sacred mountain of Koya, headquarters of Shingon Buddhism for 1,200 years.",
      timeBlocks: [
        {
          label: "Morning — Journey to Koyasan",
          activities: [
            {
              title: "Osaka to Koyasan",
              description: "Take the Nankai Railway from Namba to Gokurakubashi (end of the line), then the steep cable car up to the mountaintop plateau. The journey itself is part of the experience — you're ascending from modern Japan into a sacred world of 117 temples surrounded by cedar forests.",
              details: [
                "🚂 Nankai Railway + cable car: ~2 hours, ¥1,650 (buy Koyasan World Heritage Ticket for ¥3,400 — includes round trip + unlimited Koyasan bus)",
                "📍 Depart from Nankai Namba Station (NOT JR Namba)",
                "🚌 From Koyasan cable car station, take the bus to your temple or Senjuinbashi (central stop)"
              ]
            }
          ]
        },
        {
          label: "Midday — Temple Town Exploration",
          activities: [
            {
              title: "Danjo Garan Sacred Precinct",
              description: "The religious heart of Koyasan where Kobo Daishi (Kukai) established Shingon Buddhism in 816 AD. The vermillion Konpon Daito pagoda is stunning — inside, a 3D mandala with Buddha figures creates an immersive sacred space unlike anything else in Japan.",
              details: [
                "⏰ Grounds open 24hrs, Konpon Daito interior 8:30am–5pm (¥500)",
                "📍 15 min walk west from central Koyasan",
                "🌲 The centuries-old cedar trees surrounding the precinct create cathedral-like atmospheres"
              ]
            },
            {
              title: "Kongobu-ji Head Temple",
              description: "The administrative headquarters of Shingon Buddhism with Japan's largest Zen rock garden — the Banryutei, representing two dragons emerging from clouds. The interior rooms have painted fusuma sliding doors by Kano school artists.",
              details: [
                "⏰ 8:30am–5pm, ¥1,000 (includes matcha in a tatami room overlooking a garden)",
                "📍 Central Koyasan, 5 min from main intersection"
              ]
            }
          ],
          meals: [
            { type: "🍜 Lunch", name: "Bon On Sha Café", description: "A surprisingly modern café on the mountain serving excellent curry, sandwiches, and specialty coffee. A nice contrast to the ancient surroundings.", meta: "📍 Central Koyasan · ¥800–1,200" }
          ]
        },
        {
          label: "Afternoon — Temple Check-in & Shojin Ryori",
          activities: [
            {
              title: "Shukubo (Temple Lodging) Check-in",
              description: "Check into your temple stay. You'll sleep on futons on tatami mats in a traditional temple room, often with a garden view. The evening meal is shojin ryori — Buddhist vegetarian cuisine that's been perfected over 1,200 years here.",
              details: [
                "🏯 Recommended: Eko-in (popular, great cemetery tour) or Fukuchi-in (beautiful garden, slightly quieter) or Shojoshin-in (budget, from ¥10,000 with meals)",
                "⏰ Check-in usually 3pm–5pm",
                "🍽️ Dinner served in your room or a communal hall — multi-course vegetarian feast",
                "📵 Rooms typically don't have TV — embrace the digital detox"
              ]
            }
          ],
          meals: [
            { type: "🥢 Dinner", name: "Shojin Ryori (Temple Cuisine)", description: "A multi-course Buddhist vegetarian dinner: sesame tofu (goma-dofu), tempura of seasonal vegetables, pickled mountain plants, miso soup with fu (wheat gluten), and rice. Every dish prepared as a form of spiritual practice. Absolutely beautiful and surprisingly filling.", meta: "📍 Your temple · Included with stay" }
          ]
        },
        {
          label: "Evening — Cemetery Night Walk",
          activities: [
            {
              title: "Okunoin Cemetery After Dark",
              description: "The most otherworldly experience in Japan. Walk 2km through a forest of 200,000+ moss-covered tombstones and memorial stones — from feudal lords to modern corporations — lit by stone lanterns. At the end, the Torodo Hall of Lamps glows with 10,000 lanterns, two of which have burned for over 1,000 years continuously.",
              details: [
                "🆓 Free, open 24 hours",
                "📍 Enter from Ichinohashi bridge (traditional route) or Okunoin-mae bus stop (shorter path)",
                "🌙 Go between 7–9pm — it's darkest and most atmospheric",
                "🕯️ The Torodo Hall's Kiezu no Hi ('never-extinguished fire') has burned since the 11th century",
                "⚠️ Respectful silence — this is still an active sacred cemetery"
              ]
            }
          ],
          tips: [
            { type: "reddit", text: "Walking through Okunoin at night was the single most incredible experience of my entire Japan trip. The giant cedars, the thousands of graves disappearing into darkness, the silence... nothing prepares you for it.", cite: "r/JapanTravel" },
            { type: "tip", text: "Some temples offer guided night tours (Eko-in's is well known, ~¥500). Worth it for the historical context, but going alone is more atmospheric." }
          ]
        }
      ],
      mapPins: [
        { lat: 34.2138, lng: 135.5833, label: "Danjo Garan", num: 1, cat: "attraction", desc: "Sacred precinct with Konpon Daito pagoda" },
        { lat: 34.2150, lng: 135.5865, label: "Kongobu-ji", num: 2, cat: "attraction", desc: "Head temple of Shingon Buddhism" },
        { lat: 34.2175, lng: 135.6048, label: "Okunoin Cemetery", num: 3, cat: "attraction", desc: "200,000+ tombstones and eternal flame" },
        { lat: 34.2155, lng: 135.5880, label: "Eko-in Temple", num: 4, cat: "hotel", desc: "Popular temple lodging" },
        { lat: 34.2145, lng: 135.5850, label: "Bon On Sha Café", num: 5, cat: "food", desc: "Modern café on the sacred mountain" }
      ]
    },

    {
      num: 9,
      title: "Descend & Arrive Home",
      neighborhoods: "Koyasan · Osaka · Naka-Meguro, Tokyo",
      description: "Morning prayer ceremony on the mountain, then descend back to the modern world and travel to your new home in Naka-Meguro — arriving just in time for the Meguro River's famous cherry blossom season beginning.",
      timeBlocks: [
        {
          label: "Early Morning — Temple Ceremony",
          activities: [
            {
              title: "Morning Prayer Service (Gongyo)",
              description: "Wake at 6:00am for the temple's morning prayer ceremony — monks chanting sutras, incense smoke curling through the dark hall, the deep resonance of the temple bell. Even as a non-Buddhist, it's deeply meditative. Most guests find it the highlight of the stay.",
              details: [
                "⏰ Usually 6:00–6:30am (your temple will inform you at check-in)",
                "🙏 Attendance is optional but strongly recommended — sit on zabuton cushions",
                "📵 No photography during the ceremony",
                "🔥 Some temples include a fire ritual (goma) — mesmerizing"
              ]
            },
            {
              title: "Okunoin Morning Walk",
              description: "If you walked Okunoin at night, return in the morning for a completely different experience. Morning light filtering through ancient cedars, birdsong, and the quiet devotion of monks making their rounds creates a sense of profound peace.",
              details: [
                "🌅 Best light: 7:00–8:30am",
                "🆓 Free, always open"
              ]
            }
          ],
          meals: [
            { type: "🍚 Breakfast", name: "Temple Breakfast", description: "Simple, beautiful shojin ryori breakfast: rice porridge (okayu) or plain rice, miso soup, pickles, seasoned nori, and simmered vegetables. Eaten in silence — the monks' way of turning a meal into meditation.", meta: "📍 Your temple · Included with stay" }
          ]
        },
        {
          label: "Midday — Travel to Tokyo",
          activities: [
            {
              title: "Koyasan → Namba → Shin-Osaka → Tokyo",
              description: "Cable car and Nankai Railway back to Osaka Namba (~2 hours), then metro to Shin-Osaka. Shinkansen to Tokyo (~2.5 hours). From Tokyo Station or Shinagawa, take the JR Yamanote Line to Ebisu, then Hibiya Line one stop to Naka-Meguro. Welcome home.",
              details: [
                "🚂 Total travel: ~5–6 hours including transfers",
                "💰 Shinkansen Shin-Osaka → Tokyo: ~¥13,870 (unreserved) or ~¥14,720 (reserved)",
                "🗼 Arrive Naka-Meguro station by mid-afternoon"
              ]
            }
          ],
          tips: [
            { type: "tip", text: "Buy an ekiben at Shin-Osaka station — the tako-meshi (octopus rice) is a classic Osaka souvenir bento." }
          ]
        },
        {
          label: "Evening — New Home, New Season",
          activities: [
            {
              title: "Meguro River Cherry Blossom Preview",
              description: "Your new neighborhood is famous for one of Tokyo's most spectacular cherry blossom spots. 800+ cherry trees line the Meguro River for nearly 4km. In late March, the trees will be budding or just starting to bloom — you'll have front-row seats for the full show in the coming weeks.",
              details: [
                "🌸 Full bloom usually hits Naka-Meguro in late March to early April",
                "📍 Walk from Naka-Meguro Station along the river in either direction",
                "🏮 During hanami season, pink lanterns illuminate the river at night",
                "🍷 Explore your new neighborhood: Naka-Meguro has excellent independent cafés, bookshops, and restaurants along the river"
              ]
            }
          ],
          meals: [
            { type: "🍜 Dinner", name: "Afuri (Naka-Meguro)", description: "Celebrate arriving at your new home with a bowl at Afuri — famous for their yuzu shio (citrus salt) ramen. Light, refreshing, and the perfect end to 9 days of incredible eating.", meta: "📍 Naka-Meguro · ¥1,050–1,400" }
          ],
          tips: [
            { type: "tip", text: "Welcome to Naka-Meguro! You'll have all year to explore Tokyo, so tonight just settle in. The cherry blossoms are about to explode — you're in the best spot in Tokyo for it. 🌸" }
          ]
        }
      ],
      mapPins: [
        { lat: 34.2175, lng: 135.6048, label: "Okunoin Morning Walk", num: 1, cat: "attraction", desc: "Morning light through ancient cedars" },
        { lat: 34.2138, lng: 135.5833, label: "Koyasan Cable Car", num: 2, cat: "transport", desc: "Descend from the sacred mountain" },
        { lat: 35.6440, lng: 139.6988, label: "Naka-Meguro Station", num: 3, cat: "transport", desc: "Your new home station" },
        { lat: 35.6435, lng: 139.6975, label: "Meguro River Cherry Trees", num: 4, cat: "attraction", desc: "800+ cherry trees, Tokyo's best hanami" },
        { lat: 35.6432, lng: 139.6980, label: "Afuri Ramen", num: 5, cat: "food", desc: "Famous yuzu shio ramen" }
      ]
    }
  ],

  budgetTable: [
    { category: "Transport", budget: "¥35,000 ($235)", notes: "Buses, JR trains, Nankai, Shinkansen on Day 9" },
    { category: "Accommodation (8 nights)", budget: "¥48,000 ($320)", notes: "Hostels ¥3,500–5,000, Gero ryokan ¥10,000, Koyasan temple ¥12,000" },
    { category: "Food", budget: "¥45,000 ($300)", notes: "¥5,000/day avg — mix of markets, street food, sit-down" },
    { category: "Activities & Entry Fees", budget: "¥8,000 ($55)", notes: "Temples, gardens, onsen passes, Sky Building" },
    { category: "9-Day Total", budget: "¥136,000 (~$910)", notes: "Comfortable budget without luxury — could go lower with more konbini meals" }
  ],

  practicalInfo: [
    { title: "Getting Around", items: [
      "Get a Suica or ICOCA card at any JR station — works on virtually all trains, buses, and convenience stores nationwide. Load ¥3,000 to start.",
      "JR Pass is NOT cost-effective for this route. Buy individual tickets for each segment.",
      "Download Navitime or use Google Maps for train schedules — essential for rural connections."
    ]},
    { title: "Money & Connectivity", items: [
      "Japan is increasingly cashless but many small restaurants, temples, and market stalls are cash-only. Carry ¥10,000–15,000 at all times.",
      "7-Eleven ATMs accept all international cards with no issues.",
      "Pick up a travel eSIM (Ubigi, Airalo) or pocket WiFi for Google Maps, Translate camera mode, and train apps."
    ]},
    { title: "Daily Life Tips", items: [
      "Most hostels have coin laundry. Standalone coin laundromats (コインランドリー) are everywhere — ¥300–500 per wash + dry.",
      "Don't eat while walking (except at markets/festivals). Don't tip — it's confusing and sometimes offensive.",
      "Bow slightly as a greeting. Take off shoes when entering temples, ryokan, and some restaurants. Be quiet on trains.",
      "Convenience store breakfasts (onigiri ¥120, coffee ¥100) save money and are genuinely good."
    ]},
    { title: "Emergency Contacts", items: [
      "Police: 110 · Ambulance/Fire: 119",
      "JNTO Tourist Hotline: 050-3816-2787 (English, 24/7)",
      "Your embassy if needed for passport/visa issues."
    ]}
  ]
};

// Run fulfillment
try {
  const result = fulfillOrder(order, itineraryData);
  console.log('\n🎉 FULFILLMENT COMPLETE!');
  console.log('Slug:', result.slug);
  console.log('URL:', result.url);
  console.log('Email sent:', result.emailSent);
} catch (err) {
  console.error('\n❌ FULFILLMENT FAILED:', err.message);
  process.exit(1);
}
