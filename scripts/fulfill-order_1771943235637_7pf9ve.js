const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771943235637_7pf9ve',
  email: 'galaxycats510@gmail.com',
  destination: 'Osaka, Japan',
  startDate: '2026-03-11',
  endDate: '2026-03-14',
  groupSize: '3-4',
  requests: 'USJ is a must see. Dad is vegetarian (can eat eggs). 2nd time visiting — wants scenic views, fun, hidden gems, NO Osaka Castle. Day trip to Kyoto with all must-sees (first time).'
};

const itineraryData = {
  destination: 'Osaka, Japan',
  countryEmoji: '🇯🇵',
  title: 'Osaka Hidden Gems, USJ Thrills & a Kyoto Day Trip',
  subtitle: '4 days of theme parks, temple trails, retro neighborhoods & neon-lit nights for the family',
  description: "Your second time in Osaka means skipping the obvious and diving deep into the city's soul. This itinerary packs a full day of Universal Studios Japan thrills (with vegetarian-friendly picks for Dad), a whirlwind Kyoto day hitting every must-see temple and shrine, and a day exploring Osaka's coolest hidden neighborhoods — from the retro charm of Shinsekai to the café-lined alleys of Nakazakicho. Evenings bring Dotonbori's neon glow and the best street food in Japan. No Osaka Castle. Just the good stuff.",
  duration: '3 nights',
  dates: 'Mar 11 – Mar 14, 2026',
  budget: '$$–$$$',
  pace: 'Active',
  bestFor: 'Families & Groups',
  highlights: [
    'Full day at Universal Studios Japan — Super Nintendo World & Harry Potter',
    'Kyoto day trip: Fushimi Inari, Kinkaku-ji, Arashiyama & Kiyomizu-dera',
    'Osaka hidden gems — Nakazakicho cafés, Shinsekai retro streets',
    'Umeda Sky Building sunset panorama',
    'Dotonbori nightlife & neon-lit street food crawl'
  ],

  essentials: [
    { title: '🎢 USJ Tips', text: 'Buy tickets and Express Pass online in advance — March is spring break season and gets crowded. Arrive 30 min before gates open for early entry. Download the USJ app for real-time wait times.' },
    { title: '🚆 Getting Around', text: 'Get an ICOCA card for all trains, subways, and buses. Osaka Metro covers the city; JR lines reach USJ and Kyoto. A day trip to Kyoto is just 15 min by shinkansen or 30 min by JR Special Rapid (covered by some rail passes).' },
    { title: '🥬 Vegetarian in Japan', text: "Japanese cuisine relies heavily on dashi (fish stock), so always ask about broth ingredients. Look for shojin ryori (Buddhist temple cuisine — fully vegan). Egg dishes (tamagoyaki, omurice) are widely available. Indian restaurants are a reliable backup. We've flagged veggie options for Dad throughout." },
    { title: '🌸 March Weather', text: 'Early-to-mid March averages 8-14°C (46-57°F). Layers are key — mornings are chilly but afternoons warm up. Cherry blossoms may start appearing late March. Rain is possible; pack a compact umbrella.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-11',
      neighborhoods: 'Universal City · Konohana',
      title: 'Universal Studios Japan — Full Send',
      description: "An all-day theme park adventure at one of Japan's most popular attractions. From the magic of Super Nintendo World to the wizardry of Hogwarts, this day is pure fun for the whole family. We've mapped out the must-do rides and flagged every vegetarian-friendly food spot for Dad.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Gates Open — Hit Super Nintendo World First',
              description: "Arrive 30 minutes before opening and head straight to Super Nintendo World. This area has timed entry and fills up fast. Ride Mario Kart: Koopa's Challenge (the star attraction) and Yoshi's Adventure. Grab Power-Up Bands to play the interactive coin games throughout the land.",
              details: [
                '🎮 Mario Kart: Koopa\'s Challenge — AR racing, the park\'s #1 ride',
                '🦕 Yoshi\'s Adventure — gentler ride, great for all ages',
                '⌚ Power-Up Band (¥3,800) — activates interactive games in the area',
                '📱 Download USJ app for live wait times and show schedules'
              ]
            },
            {
              title: 'Donkey Kong Country (New Area)',
              description: "The newest expansion brings Donkey Kong's jungle to life. Ride the mine cart coaster and explore the immersive tropical environment. A must-do for Nintendo fans.",
              details: [
                '🦍 Mine Cart Madness — thrilling family coaster through DK\'s jungle',
                '🍌 Interactive barrel and vine challenges throughout the area'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Grab & Go Before Entry',
              description: "Eat at your hotel or grab onigiri from a nearby Lawson/FamilyMart before entering the park. 🥬 Dad: egg salad sandwich (tamago sando) from any konbini — eggs OK, fully vegetarian.",
              meta: '💰 $ · 📍 Universal City Walk or konbini near hotel'
            }
          ],
          tips: [
            { type: 'tip', text: 'Express Pass is highly recommended for March (spring break crowds). It lets you skip lines on top rides. Book online at usj.co.jp weeks in advance — they sell out.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'The Wizarding World of Harry Potter',
              description: "Step into Hogsmeade village and ride Harry Potter and the Forbidden Journey — a stunning motion-based dark ride through Hogwarts. Explore Ollivanders wand shop, drink Butterbeer, and admire the incredible Hogwarts Castle recreation.",
              details: [
                '🧙 Forbidden Journey — indoor motion ride, one of the world\'s best themed rides',
                '🍺 Butterbeer (non-alcoholic) — the frozen version is amazing',
                '🏰 Hogwarts Castle walkthrough is free and beautifully detailed',
                '🪄 Ollivanders wand experience — interactive and magical for kids'
              ]
            },
            {
              title: 'Hollywood Area & Thrill Rides',
              description: "Hit the big coasters: Hollywood Dream (front-facing) and Backdrop (reverse). If the group is up for it, Space Fantasy is a spinning indoor coaster that's uniquely fun. Jaws boat ride is a classic USJ original worth doing.",
              details: [
                '🎢 Hollywood Dream: The Ride — smooth, music-playing coaster with great views',
                '🦈 Jaws — fun boat ride through Amity Village',
                '🌀 Space Fantasy — spinning indoor coaster, unique to USJ'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Kinopio\'s Café (Super Nintendo World)',
              description: "Themed Mario restaurant inside Nintendo World. The mushroom-shaped interior is incredible. 🥬 Dad: Vegetable soup set and the Super Mushroom pizza bowl (request no meat) — check current menu for egg-based options.",
              meta: '💰 $$ · 📍 Super Nintendo World · Expect 30+ min wait at peak times'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Parade, Shows & Final Rides',
              description: "Catch the evening parade (seasonal) and any remaining rides. As crowds thin after 5pm, re-ride favorites with shorter waits. The park often stays open until 8-9pm.",
              details: [
                '🎆 Check USJ app for parade times — usually late afternoon',
                '🌙 Wait times drop significantly in the last 2 hours',
                '📸 Hogwarts Castle is beautifully lit at night — great photo op'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Ganko Sushi (Universal City Walk)',
              description: "After exiting the park, grab dinner at this reliable sushi chain in Universal City Walk. 🥬 Dad: tamago (egg) sushi, inari sushi (tofu pouches), kappa maki (cucumber rolls), and edamame — all vegetarian with eggs OK.",
              meta: '💰 $$ · 📍 Universal City Walk Osaka · Open late'
            }
          ],
          tips: [
            { type: 'tip', text: "Stay hydrated and wear comfortable shoes — you'll walk 15,000+ steps. March can be chilly in the evening, so bring a light jacket for the outdoor rides and parades." }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6654, lng: 135.4323, label: 'Universal Studios Japan', num: 1, cat: 'attraction', desc: 'Full-day theme park — Super Nintendo World, Harry Potter & more' },
        { lat: 34.6660, lng: 135.4340, label: 'Super Nintendo World', num: 2, cat: 'attraction', desc: 'Mario Kart, Yoshi\'s Adventure & Donkey Kong Country' },
        { lat: 34.6652, lng: 135.4305, label: 'Wizarding World of Harry Potter', num: 3, cat: 'attraction', desc: 'Hogwarts Castle, Forbidden Journey & Butterbeer' },
        { lat: 34.6658, lng: 135.4350, label: 'Kinopio\'s Café', num: 4, cat: 'food', desc: 'Mario-themed restaurant in Nintendo World' },
        { lat: 34.6670, lng: 135.4365, label: 'Universal City Walk', num: 5, cat: 'food', desc: 'Restaurants and shops outside the park gates' }
      ]
    },
    {
      num: 2,
      date: '2026-03-12',
      neighborhoods: 'Fushimi · Kinkaku-ji · Arashiyama · Higashiyama · Gion',
      title: 'Kyoto Day Trip — Temples, Bamboo & Geisha Streets',
      description: "Your one and only Kyoto day, so we're packing it full. Start early at the mesmerizing Fushimi Inari gates, hit the golden pavilion, wander through a bamboo cathedral, marvel at Kiyomizu-dera's wooden stage, browse Nishiki Market, and end in the geisha district of Gion as lanterns flicker on. It's ambitious but absolutely doable with early starts and smart routing.",
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            {
              title: 'Fushimi Inari Taisha — Thousand Torii Gates',
              description: "Take the first JR train to Kyoto and head straight to Fushimi Inari. Arriving by 7:30-8am means you'll have the iconic orange torii gates nearly to yourselves. Walk at least to the Yotsutsuji intersection (30-40 min up) for panoramic views of Kyoto. The full hike to the summit takes 2-3 hours, but the first section is the most photogenic.",
              details: [
                '⛩️ Over 10,000 vermillion torii gates winding up Mt. Inari',
                '📸 Best photos: early morning light filtering through the gates',
                '🏔️ Yotsutsuji intersection — stunning city views, good turnaround point',
                '⏰ Arrive by 8am to beat tour groups — the shrine is open 24/7'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Take JR Special Rapid from Osaka Station to Kyoto Station (30 min), then JR Nara Line to Inari Station (5 min). Total: ~40 min, covered by ICOCA. No rail pass needed for this route.' }
          ]
        },
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kinkaku-ji — The Golden Pavilion',
              description: "Take a bus or taxi from Fushimi to Kinkaku-ji. The gold-leaf temple reflecting in its mirror pond is one of Japan's most iconic images. The surrounding gardens are serene and beautiful even in early spring.",
              details: [
                '✨ The top two floors are covered entirely in gold leaf',
                '📸 The reflection shot from across the pond is the classic photo',
                '🎫 ¥500 admission — you receive a blessing charm as your ticket',
                '🚌 Bus #101 or #205 from Kyoto Station, or taxi (~¥2,500 from Fushimi Inari)'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast/Brunch',
              name: 'Falafel Garden (near Kinkaku-ji)',
              description: "A surprisingly excellent Middle Eastern restaurant near Kinkaku-ji. 🥬 Dad: Completely vegetarian-friendly — falafel wraps, hummus plates, and fresh salads. A lifesaver for vegetarians in Kyoto.",
              meta: '💰 $ · 📍 Near Kinkaku-ji bus stop · Casual and quick'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arashiyama Bamboo Grove',
              description: "Head west to Arashiyama and walk through the towering bamboo forest. The light filtering through the endless green stalks is otherworldly. Combine with a stroll across Togetsukyo Bridge with mountain views.",
              details: [
                '🎋 The bamboo grove is free and always open — best light in early afternoon',
                '🌉 Togetsukyo Bridge — iconic Arashiyama landmark with mountain backdrop',
                '🐒 Iwatayama Monkey Park nearby (15 min hike) — wild monkeys with city views',
                '🚂 JR Sagano Line from Kyoto Station to Saga-Arashiyama (15 min)'
              ]
            },
            {
              title: 'Kiyomizu-dera — The Temple on Stilts',
              description: "Cross the city to Kiyomizu-dera, perched on a hillside with a massive wooden stage offering sweeping views of Kyoto. Walk the charming Ninenzaka and Sannenzaka lanes on the approach — traditional Kyoto streetscapes with tea houses and souvenir shops.",
              details: [
                '🏛️ The wooden stage juts out 13 meters over the hillside — breathtaking views',
                '🏮 Ninenzaka & Sannenzaka — photogenic stone-paved lanes with traditional shops',
                '🎫 ¥400 admission · Open until 6pm (extended hours during special illuminations)',
                '🚌 Bus from Arashiyama to Kiyomizu-michi (~45 min) or taxi'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Arabica Coffee + Yudofu at Arashiyama',
              description: "Grab a famous % Arabica coffee by the river, then try yudofu (tofu hot pot) — Arashiyama's specialty. 🥬 Dad: Yudofu is a traditional Kyoto vegetarian dish — soft tofu simmered in kombu broth. Perfect and authentic.",
              meta: '💰 $$ · 📍 Arashiyama riverside area'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Nishiki Market — Kyoto\'s Kitchen',
              description: "A 400-meter covered market with over 100 stalls selling Kyoto specialties. Sample pickles, matcha sweets, mochi, and fresh produce. Great for snacking and souvenir shopping.",
              details: [
                '🍡 Try: yuba (tofu skin), matcha dango, tsukemono (pickles), tamagoyaki',
                '🥬 Dad: yuba skewers, grilled mochi, tamago stands, and sweet potato treats — lots of veggie options',
                '⏰ Shops close around 5-6pm — arrive by 4pm at the latest'
              ]
            },
            {
              title: 'Gion — The Geisha District at Dusk',
              description: "End your Kyoto day in Gion, the historic geisha (geiko) district. Walk Hanami-koji street lined with wooden machiya tea houses. If lucky, you'll spot a maiko (apprentice geisha) hurrying to an evening engagement. The lantern-lit streets at dusk are magical.",
              details: [
                '🏮 Hanami-koji — the main street, most atmospheric after 5pm',
                '👘 Best chance to spot maiko: 5:30-6:30pm heading to engagements',
                '🌸 Shirakawa canal — willow-lined canal with stone bridges, gorgeous at dusk',
                '📷 Please don\'t chase or block geiko/maiko for photos — observe respectfully'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Gion Kappa Restaurant',
              description: "Traditional Kyoto cuisine in the heart of Gion. 🥬 Dad: They offer shojin ryori (Buddhist vegetarian cuisine) sets — tofu, seasonal vegetables, and rice. An authentic Kyoto dining experience.",
              meta: '💰 $$$ · 📍 Gion district · Reservations recommended'
            }
          ],
          tips: [
            { type: 'tip', text: 'Last JR Special Rapid from Kyoto to Osaka runs around 11pm. Take the train back from Kyoto Station after dinner — you\'ll be exhausted but happy. About 30 min ride.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari Taisha', num: 1, cat: 'attraction', desc: '10,000 orange torii gates winding up Mt. Inari' },
        { lat: 35.0394, lng: 135.7292, label: 'Kinkaku-ji (Golden Pavilion)', num: 2, cat: 'attraction', desc: 'Gold-leaf temple reflected in a mirror pond' },
        { lat: 35.0173, lng: 135.6717, label: 'Arashiyama Bamboo Grove', num: 3, cat: 'attraction', desc: 'Towering bamboo forest with ethereal light' },
        { lat: 35.0149, lng: 135.6811, label: 'Togetsukyo Bridge', num: 4, cat: 'attraction', desc: 'Iconic bridge with mountain backdrop' },
        { lat: 34.9948, lng: 135.7850, label: 'Kiyomizu-dera', num: 5, cat: 'attraction', desc: 'Hillside temple with wooden stage and city views' },
        { lat: 35.0050, lng: 135.7649, label: 'Nishiki Market', num: 6, cat: 'food', desc: "Kyoto's 400m covered food market" },
        { lat: 35.0037, lng: 135.7745, label: 'Gion District', num: 7, cat: 'attraction', desc: 'Historic geisha district with lantern-lit machiya streets' }
      ]
    },
    {
      num: 3,
      date: '2026-03-13',
      neighborhoods: 'Nakazakicho · Umeda · Shinsekai · Sumiyoshi · Namba · Dotonbori',
      title: 'Osaka\'s Soul — Hidden Gems, Scenic Views & Neon Nights',
      description: "Today you discover the Osaka that most tourists miss. Morning in the retro-chic cafés of Nakazakicho, afternoon exploring the wonderfully weird Shinsekai district and the ancient Sumiyoshi Taisha shrine, a sunset panorama from the Umeda Sky Building, and a legendary Dotonbori nightlife crawl. This is Osaka at its most authentic and electric.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Nakazakicho — Osaka\'s Retro Creative Quarter',
              description: "A hidden neighborhood of converted pre-war wooden houses turned into indie cafés, vintage shops, and art galleries. Wander the narrow alleys and discover places that feel frozen in time — each doorway hides something unique. It's the anti-Dotonbori: quiet, charming, and deeply local.",
              details: [
                '☕ Café Tabi-no-Ne — vintage café in a converted Showa-era house, famous for hand-drip coffee',
                '🏚️ Every alley has surprises — letterpress studios, zakka shops, tiny galleries',
                '📍 10-15 min walk south from Umeda/Osaka Station',
                '📸 The crumbling facades with vines and hand-painted signs are incredibly photogenic'
              ]
            },
            {
              title: 'Tenjinbashisuji Shopping Street',
              description: "Japan's longest shopping street at 2.6km. Browse the northern end near Nakazakicho for vintage finds, local sweets, and old-school Osaka vibes without the tourist crowds.",
              details: [
                '🛍️ 2.6km covered arcade — Japan\'s longest shotengai',
                '🍘 Street snacks: taiyaki, korokke, and cheap eats galore',
                '🥬 Dad: look for imagawayaki (red bean or custard-filled cakes, egg-based batter) and fried sweet potato chips'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Salon de AManTO (Nakazakicho)',
              description: "A beloved Nakazakicho café known for being fully vegetarian-friendly. 🥬 Dad: The entire menu is veggie! Organic coffee, veggie curry, and homemade cakes in a cozy converted house. A perfect start.",
              meta: '💰 $ · 📍 Nakazakicho · Laid-back vintage vibes'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shinsekai — Retro Osaka at Its Most Colorful',
              description: "Step into a neighborhood that feels like 1960s Osaka — Tsutenkaku Tower looming over neon-signed kushikatsu joints, shogi parlors, and retro game arcades. It's wonderfully loud, unapologetically kitsch, and bursting with character. The Billiken statue at Tsutenkaku is said to bring good luck if you rub its feet.",
              details: [
                '🗼 Tsutenkaku Tower — ride to the observation deck for 360° city views',
                '🎮 Jan Jan Yokocho arcade alley — retro game centers and old-school atmosphere',
                '🍢 Kushikatsu (deep-fried skewers) originated here — DON\'T double-dip the sauce!',
                '🥬 Dad: kushikatsu places usually offer veggie skewers — egg, lotus root, shiso, sweet potato, mushroom. Ask for "yasai" (vegetable) skewers'
              ]
            },
            {
              title: 'Sumiyoshi Taisha — Ancient Osaka Shrine',
              description: "One of Japan's oldest shrines (founded 211 AD), far off the tourist trail. The striking vermillion buildings use a unique architectural style predating Chinese influence — you won't see this design anywhere else. The iconic arched Sorihashi Bridge is stunningly photogenic.",
              details: [
                '⛩️ Unique Sumiyoshi-zukuri architecture — Japan\'s oldest shrine style',
                '🌉 Sorihashi (Drum Bridge) — dramatically arched, great for photos',
                '🐇 Draw a fortune (omikuji) from the rabbit-shaped fortune holders',
                '🚃 Hankai Tramway from Shinsekai — ride Osaka\'s last remaining streetcar line'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Kushikatsu Daruma (Shinsekai)',
              description: "The most famous kushikatsu restaurant in the district that invented it. 🥬 Dad: Order the yasai (vegetable) set — includes lotus root, onion, sweet potato, shiso leaf, and mushroom skewers. Eggs used in batter, so it's fine.",
              meta: '💰 $$ · 📍 Shinsekai main street · Expect a short queue'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Umeda Sky Building — Floating Garden Sunset',
              description: "Head to the futuristic Umeda Sky Building for sunset. The open-air Floating Garden Observatory on the 40th floor offers 360° panoramic views of Osaka as the city lights switch on. The architecture itself is stunning — two towers connected by a circular sky bridge. One of the best sunset spots in all of Japan.",
              details: [
                '🌅 Arrive 30-45 min before sunset for the full golden hour experience',
                '🏙️ 360° views — mountains, city, harbour, and on clear days, even Awaji Island',
                '🎫 ¥1,500 admission · Open until 10:30pm',
                '📸 The escalator ride up through the glass tube between towers is thrilling'
              ]
            },
            {
              title: 'Dotonbori & Namba Nightlife Crawl',
              description: "Osaka's most famous street comes alive at night. Walk along the Dotonbori canal with its giant neon signs (Glico Running Man, the crab, the octopus), then dive into the backstreets. Hozenji Yokocho is a hidden moss-covered shrine alley with intimate bars. Ura Namba has craft cocktail spots and standing bars.",
              details: [
                '🏮 Hozenji Yokocho — atmospheric narrow alley with a moss-covered shrine and izakayas',
                '🍸 Ura Namba — Osaka\'s craft cocktail and standing bar scene, south of Dotonbori',
                '🛍️ Shinsaibashi-suji — covered shopping arcade leading to Dotonbori',
                '📸 Glico Running Man sign + canal reflection — THE iconic Osaka photo',
                '🎵 For nightlife: Bar Nayuta (craft cocktails), Misono Building 2F (retro bar alley)'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Okonomiyaki Mizuno (Dotonbori)',
              description: "Michelin-recognized okonomiyaki right on Dotonbori. Watch the chef make your savory pancake on the griddle in front of you. 🥬 Dad: Order the yama-imo (mountain yam) okonomiyaki without meat — specify 'niku nashi, tamago ari' (no meat, egg OK). They can make a vegetable + egg version.",
              meta: '💰 $$ · 📍 Dotonbori · Queue moves fast, worth the wait'
            }
          ],
          tips: [
            { type: 'tip', text: "Dotonbori is sensory overload in the best way. Budget at least 2-3 hours for the evening stroll. Street food is half the fun — Dad can enjoy takoyaki-style snacks made with egg batter, grilled corn, and yakiimo (roasted sweet potato) from street vendors." }
          ]
        }
      ],
      mapPins: [
        { lat: 34.7100, lng: 135.5050, label: 'Nakazakicho', num: 1, cat: 'attraction', desc: 'Retro creative quarter with indie cafés in pre-war houses' },
        { lat: 34.7055, lng: 135.5113, label: 'Tenjinbashisuji Shopping Street', num: 2, cat: 'attraction', desc: "Japan's longest covered shopping street (2.6km)" },
        { lat: 34.6524, lng: 135.5063, label: 'Shinsekai', num: 3, cat: 'attraction', desc: 'Retro entertainment district with Tsutenkaku Tower' },
        { lat: 34.6126, lng: 135.4929, label: 'Sumiyoshi Taisha', num: 4, cat: 'attraction', desc: "One of Japan's oldest shrines (211 AD) with iconic arched bridge" },
        { lat: 34.7052, lng: 135.4905, label: 'Umeda Sky Building', num: 5, cat: 'attraction', desc: 'Floating Garden Observatory with 360° sunset panorama' },
        { lat: 34.6687, lng: 135.5027, label: 'Dotonbori', num: 6, cat: 'attraction', desc: 'Neon-lit canal street — Osaka\'s iconic entertainment hub' },
        { lat: 34.6697, lng: 135.5048, label: 'Hozenji Yokocho', num: 7, cat: 'attraction', desc: 'Hidden shrine alley with moss-covered Buddha and intimate bars' },
        { lat: 34.6680, lng: 135.5020, label: 'Okonomiyaki Mizuno', num: 8, cat: 'food', desc: 'Michelin-recognized okonomiyaki on Dotonbori' }
      ]
    },
    {
      num: 4,
      date: '2026-03-14',
      neighborhoods: 'Namba · Kuromon Market',
      title: 'Morning Market & Sayonara Osaka',
      description: "A relaxed departure day with one final Osaka experience. Wander through Kuromon Market for a leisurely farewell breakfast, pick up last-minute souvenirs, and soak in the city one more time before heading to the airport.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kuromon Market — Osaka\'s Kitchen',
              description: "A 600-meter covered market known as 'Osaka's Kitchen' for over 190 years. Stroll through stalls piled with fresh seafood, seasonal fruits, tamago (egg) dishes, and Osaka specialties. A perfect final taste of the city.",
              details: [
                '🐟 Fresh seafood stalls — giant grilled scallops, sashimi, and uni',
                '🍓 Seasonal fruit stands — Japanese strawberries in March are incredible',
                '🥬 Dad: tamago-yaki stands (grilled egg omelettes), fresh fruit, mochi, and grilled corn',
                '⏰ Best before 11am — stalls start closing early afternoon'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Kuromon Market Grazing',
              description: "Skip a sit-down breakfast and graze through the market. 🥬 Dad: tamagoyaki (sweet grilled egg), seasonal fruit skewers, fresh mochi, and matcha from the many stalls. Everyone else: try the grilled seafood and street food.",
              meta: '💰 $–$$ · 📍 Kuromon Market, Namba · Open from 8am'
            }
          ],
          tips: [
            { type: 'tip', text: 'Kansai International Airport (KIX) is about 50-70 min from central Osaka via Nankai Rapi:t or JR Haruka express. If flying from Itami (domestic), it\'s 30 min by bus from Namba.' }
          ]
        },
        {
          label: 'Late Morning',
          activities: [
            {
              title: 'Last Souvenirs & Departure',
              description: "Pick up omiyage (souvenirs) at the market or nearby shops. Osaka favorites: Rikuro's cheesecake (jiggly and delicious), 551 Horai pork buns (famous Osaka brand), and matcha Kit Kats. Then head to the airport with amazing memories.",
              details: [
                '🎁 Rikuro\'s cheesecake — the signature Osaka souvenir, available at Namba',
                '🥟 551 Horai — iconic Osaka pork buns (grab a box at the station or airport)',
                '🍵 Don Quijote (Dotonbori) for last-minute snack souvenirs',
                '🥬 Dad souvenir idea: matcha sweets, rice crackers (senbei), or Japanese tea'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6688, lng: 135.5074, label: 'Kuromon Market', num: 1, cat: 'food', desc: "Osaka's Kitchen — 190-year-old covered food market" },
        { lat: 34.6659, lng: 135.5013, label: "Rikuro's Cheesecake (Namba)", num: 2, cat: 'food', desc: 'Famous jiggly cheesecake — top Osaka souvenir' },
        { lat: 34.6685, lng: 135.5023, label: 'Namba Station', num: 3, cat: 'transport', desc: 'Hub for Nankai line to KIX airport' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (per night)', budget: '¥8,000–15,000', midrange: '¥15,000–30,000', luxury: '¥30,000–60,000' },
    { category: 'Meals (per person/day)', budget: '¥2,000–4,000', midrange: '¥4,000–8,000', luxury: '¥8,000–15,000' },
    { category: 'Transport', budget: '¥1,000–2,000/day', midrange: '¥2,000–4,000/day', luxury: '¥5,000+ (taxi/private)' },
    { category: 'USJ Ticket + Express', budget: '¥8,600 (ticket only)', midrange: '¥16,000–22,000', luxury: '¥25,000+ (VIP)' },
    { category: 'Activities & Temples', budget: '¥1,000–2,000/day', midrange: '¥2,000–4,000/day', luxury: '¥5,000+/day' },
    { category: '4-Day Total (per person)', budget: '¥50,000–80,000', midrange: '¥80,000–140,000', luxury: '¥150,000–250,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Kansai International Airport (KIX) — international flights, 50–70 min to central Osaka', 'Osaka Itami Airport (ITM) — domestic flights, 30 min to Namba by bus', 'Nankai Rapi:t express from KIX to Namba — fast and scenic (¥1,450, 40 min)', 'JR Haruka from KIX to Shin-Osaka/Tennoji — connects to JR network'] },
    { title: '🏨 Where to Stay', items: ['Namba/Dotonbori area — central, walkable to everything, great nightlife', 'Shinsaibashi — shopping district, slightly calmer than Namba', 'Umeda/Osaka Station — convenient for JR lines to USJ and Kyoto', 'Universal City — if prioritizing USJ, stay at a partner hotel for early entry'] },
    { title: '🌡️ March Weather', items: ['Average highs: 12-15°C (54-59°F), lows: 4-8°C (39-46°F)', 'Layers are essential — chilly mornings, pleasant afternoons', 'Cherry blossom season may start late March (check forecasts!)', 'Occasional rain — pack a compact umbrella'] },
    { title: '💳 Money', items: ['Japan is increasingly cashless but many small shops are cash-only', 'Carry ¥10,000–20,000 in cash for markets, temples, and small eateries', 'IC cards (ICOCA) work for transit and many konbini/vending machines', '7-Eleven and Lawson ATMs accept international cards'] },
    { title: '🥬 Vegetarian Survival Guide', items: ['Always ask: "Niku nashi, sakana nashi de onegaishimasu" (no meat, no fish please)', 'Dashi (fish stock) is in almost everything — specify "katsuo dashi nashi" if concerned', 'Safe bets: Indian restaurants, shojin ryori, tempura veggies, inari sushi, edamame', 'Konbini egg sandwiches (tamago sando), onigiri with kelp/plum filling, and banana are easy grabs', 'HappyCow app shows vegetarian restaurants — download before the trip'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
