const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771297030921_7urivo',
  email: 'bernard.j.huang@gmail.com',
  destination: 'Sapporo, Hokkaido, Japan',
};

const itineraryData = {
  destination: 'Sapporo, Hokkaido, Japan',
  countryEmoji: '🇯🇵',
  title: 'Sapporo Solo: Powder, Ramen & Frozen Nights',
  subtitle: '4 nights of Hokkaido winter — world-class powder skiing, steaming ramen counters, frozen canal towns, and onsen soaks under falling snow',
  description: 'January in Hokkaido is a different planet. Sapporo sits at the crossroads of Siberian powder dumps and Japanese hospitality — meaning you get some of the best skiing on Earth, then warm up with a bowl of rich miso ramen at a counter seat built for one. This itinerary is designed for the solo adventurer: ski the legendary dry powder at Sapporo Teine and Kiroro, wander the nostalgic canal streets of Otaru, soak in a mountainside onsen while snow falls on your shoulders, and eat your way through Hokkaido\'s greatest hits — soup curry, Genghis Khan lamb, fresh uni at Nijo Market, and late-night ramen in Susukino. No group coordination needed. Just you, the snow, and the city.',
  duration: '4 nights',
  dates: 'Jan 6 – Jan 10, 2027',
  budget: '¥12,000 – ¥20,000 per day (~$80–$135 USD)',
  pace: 'Active',
  bestFor: 'Solo travelers, Skiers & snowboarders, Food lovers, Winter adventurers',
  highlights: [
    'Powder skiing at Sapporo Teine & Kiroro Resort',
    'Otaru canal town day trip — sushi, glasswork & snow-lit streets',
    'Miso ramen crawl through Ramen Alley & Susukino',
    'Nijo Market fresh seafood breakfast — uni, crab, ikura',
    'Outdoor onsen soak in falling snow',
    'Sapporo Beer Museum & fresh Genghis Khan lamb BBQ',
    'Susukino neon nightlife & late-night ramen'
  ],

  essentials: [
    { title: '🛬 Getting There', text: 'Fly into New Chitose Airport (CTS), 40 min south of Sapporo by JR Rapid Airport train (¥1,150). Direct flights from Tokyo (Haneda/Narita), Osaka, and many Asian hubs. The airport train runs every 15 min and drops you at Sapporo Station. IC cards (Kitaca/Suica) work on all trains and buses.' },
    { title: '💵 Money', text: 'Japanese Yen (¥). Japan is still cash-heavy — many ramen shops, small restaurants, and onsen are cash-only. Withdraw from 7-Eleven ATMs (international cards accepted, no fees from their side). Budget ¥12,000-20,000/day for meals, transport, and activities. Ski lift tickets are extra (¥4,000-5,500/day).' },
    { title: '🌨️ January Weather', text: 'Cold and snowy. Avg highs -1°C (30°F), lows -8°C (18°F). Sapporo gets 5+ meters of snow annually — January is peak powder season. Pack: insulated waterproof jacket, thermal layers, waterproof boots with good traction (ice!), hand warmers, and ski gear or rent on-mountain. The dry Hokkaido powder is legendarily light.' },
    { title: '🚇 Getting Around', text: 'Sapporo has an efficient subway (3 lines), streetcar (tram), and bus network. Get a Kitaca IC card at the airport for tap-and-go transit. For ski resorts, use resort shuttle buses (bookable online) or local bus routes. Otaru is 30-50 min by JR train from Sapporo Station. No car needed.' },
    { title: '♨️ Onsen Etiquette', text: 'Wash thoroughly before entering the bath. No swimsuits. Small towels OK but keep them out of the water (fold on your head). Tattoos: some onsen ban them, but many Hokkaido spots are tattoo-friendly — check ahead or use private baths. Solo onsen soaking is one of Japan\'s greatest pleasures.' },
    { title: '🏨 Where to Stay', text: 'Stay near Susukino or Odori for walkability to food and nightlife. Budget: Dormy Inn Sapporo (¥6,000-9,000/night, free onsen on top floor!). Mid-range: Mercure Sapporo or Cross Hotel Sapporo. Solo travelers thrive at business hotels — clean, compact, often with onsen facilities.' }
  ],

  days: [
    // DAY 1 — Arrival, Nijo Market, Beer Museum, Susukino
    {
      num: 1,
      title: 'Arrival & Sapporo City Deep Dive',
      description: 'Land in Sapporo, fuel up on fresh seafood at Nijo Market, explore the Sapporo Beer Museum with a Genghis Khan lamb BBQ, then hit Susukino\'s neon streets for your first bowl of Hokkaido miso ramen.',
      neighborhoods: 'Nijo Market · Sapporo Beer Garden · Susukino · Tanuki Koji',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Arrive at New Chitose Airport → Sapporo',
              description: 'Take the JR Rapid Airport train from New Chitose to Sapporo Station (37 min, ¥1,150). Drop your bags at the hotel — most places offer luggage storage before check-in. Grab a Kitaca IC card at the station for seamless transit.',
              details: [
                '📍 JR Sapporo Station',
                '💡 Trains run every 15 min from 7am. Buy tickets at the JR counter or use IC card.'
              ]
            }
          ],
          meals: [],
          tips: []
        },
        {
          label: 'Late Morning',
          activities: [
            {
              title: 'Nijo Market (二条市場) — Seafood Breakfast',
              description: 'Sapporo\'s historic fish market since 1903. Walk the narrow aisles past mountains of king crab legs, glistening uni (sea urchin), and salmon roe. Sit at a counter and order a kaisendon (seafood rice bowl) loaded with uni, ikura, and fresh sashimi. This is the Hokkaido breakfast experience — standing at a tiny counter, eating the freshest seafood of your life.',
              details: [
                '📍 Nijo Market, Chuo-ku (10 min walk from Sapporo Station)',
                '💰 ¥2,000-3,500 for a loaded kaisendon',
                '💡 Ohiso (大磯) and Donburi Chaya are the top stalls — expect short lines, worth it'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Brunch',
              name: 'Kaisendon at Nijo Market',
              description: 'A heaping bowl of rice topped with fresh uni, ikura (salmon roe), crab, and seasonal sashimi. Eaten at a 6-seat counter in a bustling market stall — peak solo dining.',
              meta: '📍 Nijo Market, Chuo-ku · 💰 ¥2,000-3,500 · 🕐 Open from 7am'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Go before 11am to avoid tour groups. Point at what looks good — the vendors are used to tourists and many have picture menus.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Sapporo Beer Museum & Genghis Khan BBQ 🍺',
              description: 'Hokkaido is the birthplace of Japanese beer. The Sapporo Beer Museum (free entry, ¥500 for tasting set) is housed in a gorgeous red-brick former brewery from 1890. Tour the history of Japanese brewing, then head next door to the Sapporo Beer Garden for Genghis Khan — Hokkaido\'s signature dome-grilled lamb BBQ, all-you-can-eat style with unlimited draft beer.',
              details: [
                '📍 Sapporo Beer Museum, Kita 7-jo, Higashi-ku',
                '💰 Museum free, tasting ¥500. Genghis Khan all-you-can-eat: ¥3,500-4,200 (100 min, includes beer)',
                '🕐 Museum 11am-8pm. Beer Garden lunch from 11:30am.',
                '💡 The Kessel Hall (ケッセルホール) room is the most atmospheric — massive copper kettles, beer hall vibes'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Genghis Khan Lamb BBQ at Sapporo Beer Garden',
              description: 'Grill thin-sliced lamb and vegetables on a dome-shaped iron plate (shaped like a Mongolian helmet). Dip in sweet soy-based tare sauce. All-you-can-eat with unlimited Sapporo draft beer. Solo diners sit at shared tables — it\'s social and fun.',
              meta: '📍 Sapporo Beer Garden · 💰 ¥3,500-4,200 all-you-can-eat+drink · 🍺 Unlimited draft beer'
            }
          ],
          tips: [
            { type: 'reddit', text: 'Sapporo Beer Garden Genghis Khan is a must-do, even solo. You sit at big communal tables grilling your own lamb. The all-you-can-eat deal with beer is an incredible value. Go for lunch to avoid the dinner rush.', cite: 'r/JapanTravel' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Susukino Neon Walk & Ramen Alley 🍜',
              description: 'Susukino is Sapporo\'s entertainment district — a dazzling grid of neon signs, izakayas, bars, and ramen shops. Walk south from Odori along Ekimae-dori to take in the lights. Then find Ramen Alley (Ramen Yokocho) — a narrow lane of 17 tiny ramen shops, each with about 10 counter seats. Pick one, order Sapporo-style miso ramen with butter and corn, and slurp in shoulder-to-shoulder bliss.',
              details: [
                '📍 Ganso Sapporo Ramen Yokocho, Minami 5-jo, Nishi 3',
                '💰 ¥800-1,100 per bowl',
                '💡 Hachiya (蜂屋) for classic rich miso. Shirakaba Sansou for the cult following.',
                '💡 Ramen Yokocho is tiny — just pick whichever has a short line and dive in'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Miso Ramen at Ramen Yokocho',
              description: 'Sapporo invented miso ramen. Rich pork-based broth blended with red miso, topped with bean sprouts, ground pork, butter, and sweet corn. Eaten at a counter barely wider than your elbows. This is the ramen experience.',
              meta: '📍 Ramen Yokocho, Susukino · 💰 ¥800-1,100 · 🕐 Open until 2am'
            }
          ],
          tips: []
        }
      ],
      mapPins: [
        { lat: 43.0687, lng: 141.3508, label: 'JR Sapporo Station', num: 1, cat: 'transport', desc: 'Main transit hub — airport train arrives here' },
        { lat: 43.0571, lng: 141.3559, label: 'Nijo Market', num: 2, cat: 'food', desc: 'Historic seafood market — fresh uni and kaisendon' },
        { lat: 43.0709, lng: 141.3688, label: 'Sapporo Beer Museum', num: 3, cat: 'attraction', desc: 'Red-brick brewery museum with beer tastings' },
        { lat: 43.0709, lng: 141.3695, label: 'Sapporo Beer Garden', num: 4, cat: 'restaurant', desc: 'Genghis Khan lamb BBQ & unlimited beer' },
        { lat: 43.0520, lng: 141.3531, label: 'Ramen Yokocho (Ramen Alley)', num: 5, cat: 'food', desc: '17 tiny ramen shops in one lane — miso ramen heaven' },
        { lat: 43.0500, lng: 141.3531, label: 'Susukino', num: 6, cat: 'nightlife', desc: 'Sapporo\'s neon-lit entertainment district' }
      ]
    },

    // DAY 2 — Ski Day at Sapporo Teine
    {
      num: 2,
      title: 'Powder Day at Sapporo Teine',
      description: 'Hit the slopes at Sapporo Teine — the mountain that hosted the 1972 Winter Olympics, just 40 minutes from downtown. Legendary dry Hokkaido powder, panoramic views of the city and sea, then warm up with soup curry back in town.',
      neighborhoods: 'Sapporo Teine · Odori · Soup Curry District',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sapporo Teine — Highland Zone ⛷️',
              description: 'Bus from Sapporo to Teine Highland (40 min, ¥590). This is where the 1972 Olympic downhill and giant slalom were held. The Highland zone has steeper, more challenging terrain and the best powder — ungroomed tree runs through birch forests with Hokkaido\'s famously light, dry snow (nicknamed "Japow"). On a clear day, you can see the Sea of Japan and Sapporo\'s skyline simultaneously.',
              details: [
                '📍 Sapporo Teine, Teine-ku (bus from JR Teine Station or direct bus from Sapporo)',
                '💰 Lift ticket: ¥5,200/day. Rental gear: ¥5,000-7,000/day',
                '🕐 Lifts open 9am-5pm (Highland), 9am-9pm (Olympia night skiing)',
                '💡 Take JR train to Teine Station (15 min, ¥340), then free shuttle bus to resort (15 min)',
                '💡 Highland gets less crowded than Niseko — same quality powder, fraction of the people'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Mountain Lodge Lunch at Teine',
              description: 'Refuel on the mountain with katsu curry, udon, or ramen at the Highland lodge cafeteria. Cheap, hot, and exactly what you need mid-powder day.',
              meta: '📍 Teine Highland Lodge · 💰 ¥800-1,200'
            }
          ],
          tips: [
            { type: 'reddit', text: 'Teine Highland is severely underrated. I skied there on a powder day and had fresh tracks at 10am while everyone else was fighting crowds at Niseko. The tree skiing in the Highland zone is incredible.', cite: 'r/skiing' },
            { type: 'tip', text: '💡 Rent gear in Sapporo the night before at Rhythm Japan or a shop near the station — saves time in the morning. Boot fitting matters for powder days.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ski Until Legs Give Out',
              description: 'Keep riding the Highland lifts for afternoon powder stashes, or head down to the Olympia zone for wider groomed cruisers with city views. If you still have energy, Teine offers night skiing on the Olympia side until 9pm — skiing under lights with Sapporo\'s city glow in the distance is surreal.',
              details: [
                '💡 Olympia night skiing (5pm-9pm) is ¥2,100 extra — worth it for the experience'
              ]
            }
          ],
          meals: [],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Soup Curry — Hokkaido\'s Signature Comfort Food 🍛',
              description: 'Back in Sapporo, warm your frozen bones with soup curry — a Sapporo invention. Unlike thick Japanese curry, this is a fragrant, spiced broth loaded with massive chunks of vegetables (whole potato, half an onion, huge carrots) and your choice of chicken leg, pork, or cheese Hamburg steak. It\'s Sapporo\'s ultimate après-ski food.',
              details: [
                '📍 Suage+ (Susukino area) or Garaku (near Sapporo Station)',
                '💰 ¥1,200-1,600',
                '💡 Suage+ is famous for crispy fried chicken in soup curry. Garaku for rich, complex spice blends.',
                '💡 Pick your spice level 1-40. Start at 5 unless you know your tolerance.'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Soup Curry at Suage+',
              description: 'Sapporo\'s iconic soup curry — a thin, aromatic, impossibly flavorful broth with a whole chicken leg, roasted vegetables, and your choice of spice level. The perfect post-ski meal.',
              meta: '📍 Suage+, Susukino · 💰 ¥1,200-1,600 · 🌶️ Choose spice level 1-40'
            }
          ],
          tips: []
        }
      ],
      mapPins: [
        { lat: 43.0789, lng: 141.1958, label: 'Sapporo Teine Highland', num: 1, cat: 'adventure', desc: '1972 Olympic ski area — steep terrain and deep powder' },
        { lat: 43.0833, lng: 141.2028, label: 'Sapporo Teine Olympia', num: 2, cat: 'adventure', desc: 'Beginner-intermediate zone with night skiing' },
        { lat: 43.0554, lng: 141.3489, label: 'Suage+ Soup Curry', num: 3, cat: 'restaurant', desc: 'Sapporo\'s famous crispy chicken soup curry' },
        { lat: 43.0633, lng: 141.3533, label: 'Garaku Soup Curry', num: 4, cat: 'restaurant', desc: 'Rich, complex spice blends — cult following' }
      ]
    },

    // DAY 3 — Otaru Day Trip
    {
      num: 3,
      title: 'Otaru Canal Town — Snow, Sushi & Glasswork',
      description: 'Day trip to Otaru — a nostalgic port city 40 minutes from Sapporo. Snow-draped canal warehouses, the freshest sushi in Hokkaido, handblown glass shops, and a legendary music box museum. Return for a hot onsen soak.',
      neighborhoods: 'Otaru Canal · Sushi Street · Sakaimachi · Asarigawa Onsen',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'JR Train to Otaru 🚃',
              description: 'Catch the JR train from Sapporo Station to Otaru (32-50 min depending on express/local, ¥750). The train hugs the coastline — watch for dramatic winter sea views on the left side. Arrive in Otaru and walk 10 minutes downhill to the canal district.',
              details: [
                '📍 JR Otaru Station → Otaru Canal (10 min walk downhill)',
                '💡 Sit on the left side of the train for ocean views. The coastal stretch is stunning in winter.'
              ]
            },
            {
              title: 'Otaru Canal Walk ❄️',
              description: 'The iconic Otaru Canal lined with 19th-century stone warehouses, now blanketed in snow. In winter, the gas lamps and snow create a dreamy atmosphere even in daylight. Walk along the canal path, cross the bridges, and photograph the warehouses reflected in the still water. If you visit in early February, the Otaru Snow Light Path festival fills the canal with floating candles.',
              details: [
                '📍 Otaru Canal, central Otaru',
                '💡 Walk the full length — the south end near the canal plaza has the best photo angles'
              ]
            }
          ],
          meals: [],
          tips: []
        },
        {
          label: 'Late Morning',
          activities: [
            {
              title: 'Otaru Sushi Street (寿司屋通り) 🍣',
              description: 'Otaru was once Hokkaido\'s busiest herring port, and that fishing heritage means some of Japan\'s best sushi. Sushi-ya Dori (Sushi Street) has over a dozen sushi restaurants — sit at a counter and order omakase. The uni here comes straight from Shakotan Peninsula, and the squid is so fresh it\'s translucent. Solo counter dining at its absolute finest.',
              details: [
                '📍 Sushi-ya Dori, central Otaru (5 min from canal)',
                '💰 ¥2,500-4,000 for omakase lunch set',
                '💡 Masazushi or Otaru Takeda are top picks. Lunch sets are significantly cheaper than dinner.',
                '💡 Counter seats only — perfect for solo. Watch the chef work inches from your plate.'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Omakase Sushi on Sushi Street',
              description: 'Chef\'s choice sushi at a 10-seat counter in Otaru\'s famous sushi district. Expect ultra-fresh uni, translucent squid, fatty tuna, and Hokkaido salmon. Quiet, focused, and transcendent.',
              meta: '📍 Sushi-ya Dori, Otaru · 💰 ¥2,500-4,000 lunch set · 🕐 Go before noon'
            }
          ],
          tips: [
            { type: 'reddit', text: 'Skip the tourist-trap sushi places on the main drag. Walk one block off Sushi Street and you\'ll find places with half the price and the same fish. Masazushi is worth the premium though — their uni is otherworldly.', cite: 'r/JapanTravel' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Sakaimachi Street — Glass, Music Boxes & Sweets',
              description: 'Otaru\'s main shopping street is a charming stretch of repurposed stone warehouses filled with handblown glass studios (Kitaichi Glass is the most famous), music box shops (the Otaru Music Box Museum is mesmerizing — 25,000+ music boxes), and LeTAO\'s original cheesecake shop. Warm up with a fresh LeTAO double fromage cheesecake and hot cocoa.',
              details: [
                '📍 Sakaimachi-dori, Otaru',
                '💡 Kitaichi Glass Hall No. 3 — beautiful oil-lamp-lit interior, great for browsing',
                '💡 LeTAO cheesecake is Hokkaido-famous. Try the fresh double fromage (¥800) — you can only get it here'
              ]
            },
            {
              title: 'Otaru Snow Walk & Return',
              description: 'Wander back toward the station through snowy side streets. Otaru feels frozen in time — Meiji-era banks, old rail lines, and quiet residential streets under heavy snow. Catch the JR train back to Sapporo.',
              details: []
            }
          ],
          meals: [],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Onsen Soak — Snow Falling on Hot Water ♨️',
              description: 'End the day with the quintessential Hokkaido experience: an outdoor onsen (rotenburo) while snow falls around you. If your hotel has an onsen (Dormy Inn does — rooftop!), use it. For a more dramatic experience, take a short bus to Jozankei Onsen (60 min from Sapporo) or try Tsukimiru Kimi Omofu in Susukino — a modern day-spa onsen with open-air baths.',
              details: [
                '📍 Dormy Inn Premium Sapporo (rooftop onsen, guests only) or Tsukimiru Kimi Omofu (day use)',
                '💰 Day-use onsen: ¥1,500-3,000. Hotel onsen: free for guests.',
                '💡 The feeling of hot water + cold snow on your face is indescribable. Go after dark for maximum atmosphere.'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ebikani Gassen (Crab & Shrimp Battle)',
              description: 'Splurge night. All-you-can-eat crab restaurant near Susukino — king crab legs, snow crab, and grilled shrimp. Hokkaido crab in January is at peak sweetness. Solo counter available.',
              meta: '📍 Ebikani Gassen, Susukino · 💰 ¥4,000-6,000 all-you-can-eat'
            }
          ],
          tips: [
            { type: 'tip', text: '♨️ If you only do one onsen, make it a rotenburo (outdoor bath) during snowfall. It\'s a bucket-list moment. Check your hotel first — many business hotels in Sapporo have surprise rooftop baths.' }
          ]
        }
      ],
      mapPins: [
        { lat: 43.1975, lng: 140.9945, label: 'Otaru Canal', num: 1, cat: 'attraction', desc: 'Snow-draped historic canal with stone warehouses' },
        { lat: 43.1948, lng: 140.9970, label: 'Otaru Sushi Street', num: 2, cat: 'food', desc: 'Dozen+ sushi restaurants — best uni in Hokkaido' },
        { lat: 43.1970, lng: 140.9988, label: 'Sakaimachi Street', num: 3, cat: 'shopping', desc: 'Glass studios, music boxes & LeTAO cheesecake' },
        { lat: 43.1988, lng: 140.9999, label: 'Otaru Music Box Museum', num: 4, cat: 'attraction', desc: '25,000+ music boxes in a stone warehouse' },
        { lat: 43.0500, lng: 141.3520, label: 'Susukino Onsen District', num: 5, cat: 'onsen', desc: 'Day-use onsen & late-night soaking options' },
        { lat: 43.0510, lng: 141.3545, label: 'Ebikani Gassen', num: 6, cat: 'restaurant', desc: 'All-you-can-eat king crab & snow crab' }
      ]
    },

    // DAY 4 — Kiroro Ski Resort + Farewell Ramen
    {
      num: 4,
      title: 'Kiroro Deep Powder & Farewell Feast',
      description: 'Chase the deepest powder at Kiroro Resort — Hokkaido\'s snowiest ski area, buried under 21 meters of annual snowfall. Return to Sapporo for a final ramen pilgrimage and late-night Susukino walk.',
      neighborhoods: 'Kiroro Resort · Sapporo Station · Susukino',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kiroro Resort — The Snow Monster ⛷️',
              description: 'Bus to Kiroro Resort (90 min from Sapporo, shuttle available). Kiroro averages 21 METERS of snowfall per season — one of the snowiest resorts on Earth. The terrain is intermediate-friendly with incredible tree skiing and wide-open powder bowls. Far fewer crowds than Niseko, and the snow is somehow even lighter and drier. This is the Hokkaido powder day.',
              details: [
                '📍 Kiroro Resort, Akaigawa Village (90 min bus from Sapporo)',
                '💰 Lift ticket: ¥5,500/day. Bus: ¥1,500-2,000 round trip.',
                '🕐 First lift 9am. Bus departs Sapporo ~7:30am.',
                '💡 Book the Chuo Bus Kiroro shuttle from Sapporo Station Bus Terminal — reserve online the day before',
                '💡 Kiroro gets 2-3x the snow of Sapporo city. Even on a "bad" day, there\'s powder here.'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Kiroro Mountain Cafeteria',
              description: 'Classic Japanese ski lodge food — katsu curry rice, miso ramen, or hot udon. Cheap, filling, and delicious after a morning of powder laps.',
              meta: '📍 Kiroro Resort Center · 💰 ¥900-1,300'
            }
          ],
          tips: [
            { type: 'reddit', text: 'Kiroro is the move if you want untouched powder. We went on a weekday in January and had entire runs to ourselves. The tree skiing off the Asari Gondola is absolutely bonkers — waist-deep on a good day.', cite: 'r/JapanTravel' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Last Runs & Return to Sapporo',
              description: 'Squeeze in afternoon laps until your legs are done, then catch the shuttle bus back to Sapporo (arrives ~5-6pm). Head to the hotel, drop off gear, and prep for a final farewell dinner tour.',
              details: [
                '💡 Last bus back is usually around 4-4:30pm — check the schedule when you arrive'
              ]
            }
          ],
          meals: [],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Farewell Ramen: Sumire (すみれ) — The GOAT 🍜',
              description: 'For your last night, go to the source. Sumire in Nakanoshima is widely considered the birthplace of modern Sapporo miso ramen — rich, lard-topped, intensely savory broth with a thin layer of oil that keeps it screaming hot. There\'s always a line, but it moves fast. This is the bowl you\'ll dream about when you get home.',
              details: [
                '📍 Sumire, Nakanoshima (or Susukino branch)',
                '💰 ¥900-1,100',
                '💡 The original Nakanoshima location is a trek but worth it for purists. The Susukino branch (in ESTA/Ramen Republic) is more convenient.',
                '💡 Order the classic miso ramen. Add butter if you want peak Hokkaido decadence.'
              ]
            },
            {
              title: 'Final Susukino Night Walk',
              description: 'One last walk through Susukino\'s neon canyons. Pop into a standing bar (tachinomi) for a highball, browse the late-night don quijote for souvenirs (Royce\' chocolate, Shiroi Koibito cookies, dried scallops), and soak in the winter city one final time.',
              details: [
                '📍 Susukino / Tanuki Koji covered arcade',
                '💡 Royce\' Chocolate and Shiroi Koibito are the quintessential Hokkaido souvenirs — cheaper here than at the airport'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Miso Ramen at Sumire',
              description: 'The godfather of Sapporo miso ramen. Thick, rich pork-miso broth sealed under a layer of hot lard, curly noodles, ground pork, and bean sprouts. The bowl that launched a thousand imitators. A perfect final meal.',
              meta: '📍 Sumire, Nakanoshima/Susukino · 💰 ¥900-1,100 · 🕐 Expect a 15-30 min wait'
            }
          ],
          tips: [
            { type: 'tip', text: '🎁 Stock up on Hokkaido souvenirs at Don Quijote in Susukino (open 24h) or the underground shopping mall at Sapporo Station. Royce\' nama chocolate and Shiroi Koibito are crowd-pleasers back home.' }
          ]
        }
      ],
      mapPins: [
        { lat: 43.0759, lng: 140.6863, label: 'Kiroro Resort', num: 1, cat: 'adventure', desc: '21m annual snowfall — Hokkaido\'s powder paradise' },
        { lat: 43.0480, lng: 141.3790, label: 'Sumire Ramen (Nakanoshima)', num: 2, cat: 'food', desc: 'Birthplace of modern Sapporo miso ramen' },
        { lat: 43.0520, lng: 141.3531, label: 'Susukino Neon District', num: 3, cat: 'nightlife', desc: 'Final night walk through Sapporo\'s glowing heart' },
        { lat: 43.0540, lng: 141.3485, label: 'Tanuki Koji Arcade', num: 4, cat: 'shopping', desc: 'Covered shopping arcade — souvenirs and late-night snacks' },
        { lat: 43.0507, lng: 141.3530, label: 'Don Quijote Susukino', num: 5, cat: 'shopping', desc: '24h mega-store for souvenirs, snacks & weird finds' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '¥6,000-9,000/night', mid: '¥10,000-15,000/night', premium: '¥20,000+/night' },
    { category: 'Ski Lift Ticket', budget: '¥4,200 (half-day)', mid: '¥5,200-5,500 (full day)', premium: '¥12,000+ (multi-resort)' },
    { category: 'Ski Rental', budget: '¥3,500/day', mid: '¥5,000-7,000/day', premium: '¥10,000+/day (demo)' },
    { category: 'Meals', budget: '¥2,500-4,000/day', mid: '¥5,000-8,000/day', premium: '¥10,000+/day' },
    { category: 'Transport', budget: '¥1,000-2,000/day', mid: '¥2,000-3,000/day', premium: '¥5,000+/day (taxi)' },
    { category: 'Activities', budget: '¥500-1,500/day', mid: '¥2,000-4,000/day', premium: '¥8,000+/day' }
  ],

  practicalInfo: [
    { title: '🛂 Visa', items: ['Most Western passport holders get 90-day visa-free entry to Japan', 'Check your country\'s specific requirements before travel', 'No visa application needed for US, EU, UK, AU, CA citizens'] },
    { title: '📱 Connectivity', items: ['Rent a pocket WiFi at New Chitose Airport (¥500-800/day)', 'eSIM options: Ubigi, Airalo — set up before departure', 'Free WiFi at stations and convenience stores but unreliable for navigation'] },
    { title: '🏧 Cash', items: ['Japan is still cash-dependent — many ramen shops and small eateries are cash-only', '7-Eleven and Japan Post ATMs accept international cards', 'Withdraw ¥20,000-30,000 at a time to avoid multiple fees'] },
    { title: '⏰ Timing', items: ['January 6-10 is right after New Year holidays — crowds thin out, prices normalize', 'Peak powder season — consistent snowfall throughout January', 'Sapporo Snow Festival starts early February (just after your trip)'] },
    { title: '🎿 Ski Gear', items: ['Rent in Sapporo city (Rhythm Japan, SPICY Rental) — cheaper than on-mountain', 'Pick up gear the night before to save morning time', 'Bring your own goggles and gloves if particular about fit'] },
    { title: '🚨 Safety', items: ['Sapporo is extremely safe — biggest hazard is icy sidewalks', 'Wear boots with good tread or buy clip-on ice grips (¥500 at any konbini)', 'Ski within marked boundaries — backcountry requires avalanche gear and a guide'] }
  ]
};

// Run fulfillment
const result = fulfillOrder(order, itineraryData);
console.log('\n✅ ITINERARY FULFILLED');
console.log('Slug:', result.slug);
console.log('URL:', result.url);
console.log('File:', result.filePath);
console.log('Email sent:', result.emailSent);
