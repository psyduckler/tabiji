const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771940674699_glqdtz',
  email: 'galaxycats510@gmail.com',
  destination: 'Sapporo, Hokkaido, Japan',
  startDate: '2026-03-19',
  endDate: '2026-03-25',
  groupSize: '3-4',
  travelStyle: 'Adventure, Cultural, Relaxation',
  dining: 'Casual throughout',
  budget: 'Surprise me',
  requests: 'We really want to try skiing'
};

const itineraryData = {
  destination: 'Sapporo, Hokkaido, Japan',
  countryEmoji: '🇯🇵',
  title: 'Powder, Ramen & Hot Springs in Hokkaido',
  subtitle: '6 days of skiing, seafood feasts, onsen soaks & cultural gems in Japan\'s snowy north',
  description: "Sapporo in late March is the sweet spot of Hokkaido winter travel — the powder is still falling, the ski resorts are wide open, the ramen is steaming, and the onsen baths have never felt more deserved. Japan's fifth-largest city punches well above its weight: legendary miso ramen born right here, one of Asia's best seafood markets, the world-famous Sapporo Beer, and ski slopes just 30 minutes from downtown. Pair it with a day trip to storybook Otaru and a soak at Jozankei's mountain onsen, and you have the ultimate cold-weather adventure for a group ready to eat, ski, and explore.",
  duration: '6 nights',
  dates: 'Mar 19 – Mar 25, 2026',
  budget: '$$–$$$',
  pace: 'Active',
  bestFor: 'Adventure groups, first-time Hokkaido visitors',

  highlights: [
    'Full ski day at Sapporo Teine — the Olympic resort 30 minutes from downtown',
    'Day trip to Niseko for legendary Hokkaido powder slopes',
    'Charming Otaru canal town with fresh seafood and artisan glassware',
    'Soak in the snow-draped outdoor baths at Jozankei Onsen',
    'Sapporo miso ramen at the iconic Susukino Ramen Alley',
    'Genghis Khan lamb BBQ with cold Sapporo draft at the Beer Garden',
    'Fresh sea urchin and crab at Nijo Morning Market'
  ],

  essentials: [
    { title: '❄️ Late-Season Snow', text: 'Late March means spring skiing conditions — packed powder and corn snow at lower elevations, potentially fresh dumps at higher runs. Sapporo Teine\'s Olympia Zone closes March 29, Highland Zone stays open into May. Niseko is typically open through late March.' },
    { title: '🚆 Getting Around', text: 'The Sapporo subway (Namboku, Tozai, Toho lines) is clean and fast. Taxis are affordable by Japanese standards. For Teine, take the JR Line to Teine Station + taxi up. For Otaru, the JR Hakodate Line runs every 20-30 min (~35 min, ¥640). For Niseko, book a direct bus from Sapporo Station (Donan Bus, ~2hrs, ¥2,500).' },
    { title: '🍜 Food Culture', text: 'Sapporo invented miso ramen. Soup curry is a local creation you can\'t find this good elsewhere. Hokkaido dairy means incredible soft-serve, butter, and cheese everywhere. At Nijo Market, point at what you want — the vendors are friendly and most have picture menus.' },
    { title: '⛷️ Ski Essentials', text: 'Rentals available at both Teine and Niseko — full kit (skis/board, boots, poles, helmet) is ~¥5,000-8,000/day. Lift passes: Teine day pass ~¥8,200/person, Niseko United ~¥8,800/person. Book Niseko bus in advance during peak season.' },
    { title: '🛁 Onsen Etiquette', text: 'Tattoos are commonly prohibited at public baths — check each venue\'s policy. Rinse thoroughly before entering. No swimwear in traditional rotenburo (outdoor baths). Most ryokan onsen are single-use or split by gender. Jozankei\'s private baths (kashikiriburo) can be rented for groups.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-19',
      neighborhoods: 'Odori · Susukino · Tanuki Koji',
      title: 'Welcome to Sapporo — Ramen, Markets & Nightlife',
      description: "Land in Hokkaido and dive straight into Sapporo's soul: a brisk walk through the iconic Odori Park, fresh seafood at the nearby Nijo Market, and an evening in Susukino — one of Japan's most vibrant entertainment districts — culminating in a steaming bowl of miso ramen at the legendary Ramen Alley.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Odori Park & Sapporo TV Tower',
              description: "Sapporo's green heart stretches 12 city blocks through the center of downtown. In late March you'll find the last of the snow sculptures and the first hints of spring. Climb the TV Tower for a panoramic view of the grid-patterned city backed by snow-capped mountains — it orients you perfectly for the days ahead.",
              details: [
                '📍 Odori Station (Namboku/Tozai/Toho lines) — exit right onto the park',
                '🗼 TV Tower observation deck: ¥1,000/adult · Open 9am–10pm',
                '📸 The view down the park boulevard from the tower is quintessential Sapporo',
                '❄️ Late March often still has snow on the ground — great winter atmosphere'
              ]
            },
            {
              title: 'Tanuki Koji Shopping Arcade',
              description: "Duck into Tanuki Koji — Sapporo's covered shopping street dating to 1869. Seven blocks of local shops, drugstores, vintage clothing, and snack stalls. Perfect for grabbing ski layers, Hokkaido souvenirs, and warming up with a taiyaki or soft-serve.",
              details: [
                '🛍️ Stretches from 1-chome to 7-chome (7 blocks)',
                '🍦 Try Hokkaido soft-serve — the milk is unbelievably rich',
                '🧤 Pick up ski base layers or gloves if you\'re missing any'
              ]
            }
          ],
          meals: [
            {
              type: '🦀 Late Lunch / Snack',
              name: 'Nijo Market (二条市場)',
              description: 'Sapporo\'s beloved downtown seafood market with dozens of stalls selling fresh Hokkaido crab (kegani, tarabagani), sea urchin, salmon, and scallops. Grab a "kaisendon" (fresh seafood rice bowl) at one of the market restaurants — this is your Hokkaido welcome meal.',
              meta: '💰 ¥1,500–3,500 · 📍 2-chome, Minami, Chuo-ku · Open 6am–6pm'
            }
          ],
          tips: [
            { type: 'tip', text: 'Nijo Market is walking distance from Odori Park (10 min south). Vendors are friendly and many speak basic English. Point at what looks good — you won\'t be disappointed.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Susukino — Sapporo\'s Neon District',
              description: "Susukino is one of Japan's three great entertainment districts (alongside Shinjuku and Nakasu). By night, the neon signs stack up like a video game city — izakayas, cocktail bars, karaoke, and ramen joints shoulder-to-shoulder for blocks. Wander, explore, and let your group find its rhythm.",
              details: [
                '🌃 Most vibrant after 8pm',
                '🍻 Sapporo draft beer tastes best poured in its home city',
                '🎤 Karaoke: Joysound or Big Echo for group sessions',
                '🍢 Kushiyaki skewers at any standing izakaya — order by pointing'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Susukino Ramen Yokocho (ラーメン横丁)',
              description: 'The most atmospheric place to eat ramen in all of Japan — a narrow alley lined with 17 tiny ramen shops, each with just a handful of seats. Sapporo invented miso ramen, and you\'ll taste exactly why here. Go for the rich, buttery miso broth with corn and a pat of Hokkaido butter.',
              meta: '💰 ¥900–1,200 · 📍 Minami 5-jo Nishi 3-chome, Susukino · Open until midnight or later'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 43.0606, lng: 141.3564, label: 'Odori Park', num: 1, cat: 'attraction', desc: '12-block central park and Sapporo landmark' },
        { lat: 43.0610, lng: 141.3577, label: 'Sapporo TV Tower', num: 2, cat: 'attraction', desc: 'Observation deck with panoramic city and mountain views' },
        { lat: 43.0577, lng: 141.3499, label: 'Tanuki Koji Shopping Arcade', num: 3, cat: 'attraction', desc: 'Historic covered shopping street — 7 blocks of local shops' },
        { lat: 43.0580, lng: 141.3530, label: 'Nijo Market', num: 4, cat: 'food', desc: 'Sapporo\'s downtown seafood market — fresh crab, uni, kaisendon' },
        { lat: 43.0550, lng: 141.3540, label: 'Susukino Entertainment District', num: 5, cat: 'attraction', desc: 'Neon-lit nightlife hub with izakayas, karaoke, and ramen' },
        { lat: 43.0527, lng: 141.3558, label: 'Susukino Ramen Yokocho', num: 6, cat: 'food', desc: 'Famous ramen alley with 17 tiny shops — Sapporo miso birthplace' }
      ]
    },
    {
      num: 2,
      date: '2026-03-20',
      neighborhoods: 'Teine · Okurayama · Nakajima Park',
      title: 'Ski Day at Sapporo Teine — Olympic Slopes 30 Min from Downtown',
      description: "Today you ski the mountain that hosted the 1972 Winter Olympics — right on Sapporo's doorstep. Teine has two distinct zones: the beginner-friendly Olympia and the steeper, more challenging Highland. Late March means the slopes are quiet, the snow is firmly packed, and the mountain views over the Pacific are spectacular. End the day with a long soak in a hot spring.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sapporo Teine Ski Resort — All Day',
              description: "Catch the JR Line from Sapporo Station to Teine Station (18 min, ¥330), then taxi up to the resort (~¥1,200). Or grab one of the resort shuttle buses. The Olympia Zone is great for warm-ups and beginners; take the gondola up to Highland for stunning runs with ocean views on clear days.",
              details: [
                '⛷️ Highland Zone: mostly intermediate and advanced runs (780m vertical)',
                '🎿 Olympia Zone: wider, gentler — perfect for getting legs under you early',
                '🎫 1-day pass: ¥8,200/adult (Highland) or ¥5,700 (Olympia only)',
                '🏂 Rental shop at base — full kit ~¥6,500/day',
                '🚡 Gondola + 9 lifts — rarely queues in late March',
                '🌊 On clear days you can see the Pacific Ocean from the Highland summit'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Teine Kogen Restaurant (base lodge)',
              description: 'Ski lodge ramen and curry rice at the base of the Highland gondola. Classic mountain lodge fare — hot, filling, and exactly what you need mid-ski-day.',
              meta: '💰 ¥800–1,500 · 📍 Highland Zone base lodge'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Okurayama Ski Jump Stadium',
              description: "After skiing, swing by the Okurayama jump stadium on the way back to the city — it hosted the 1972 Olympic ski jump. You can ride a chairlift to the top of the 90-meter jump ramp for a terrifying-yet-thrilling view straight down. The Olympic Museum at the base is excellent and only ¥600.",
              details: [
                '📍 Okurayama Jump Stadium — 15-min taxi from Teine or bus from Maruyama',
                '🎿 Chairlift to jump ramp top: ¥1,000 — the view down will make your stomach drop',
                '🏅 Olympic Museum open 9am–5pm, ¥600 adults',
                '📸 Great group photo at the summit with the city spread below'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Onsen Recovery Soak at Nakajima Park',
              description: "Your legs will know you skied. The best cure: a long hot bath at one of the traditional bathhouses near Nakajima Park in central Sapporo. Houheikan Onsen or the ryokan-style Sapporo Grand Hotel's bath are great options. Let the mineral water do its work.",
              details: [
                '🛁 Houheikan: traditional Hokkaido architecture, open baths, ¥490',
                '⏰ Onsen typically 10am–10pm',
                '🧴 Bring a small towel or rent one at the entrance (¥100–300)'
              ]
            }
          ],
          meals: [
            {
              type: '🥩 Dinner',
              name: 'Jingisukan Daruma (だるま) — Genghis Khan BBQ',
              description: "The most Sapporo thing you can possibly eat: Genghis Khan (Jingisukan). Thin-sliced lamb grilled on a domed iron brazier with vegetables, dipped in a savory tare sauce. Daruma is the original, the iconic, the legendary — in business since 1954. Order the draft Sapporo to wash it down.",
              meta: '💰 ¥2,000–3,500/person · 📍 Susukino, multiple locations · Often a queue — worth it'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 43.1100, lng: 141.2175, label: 'Sapporo Teine Ski Resort', num: 1, cat: 'attraction', desc: '1972 Olympic ski resort — Highland and Olympia zones, 30 min from downtown' },
        { lat: 43.0557, lng: 141.2792, label: 'Okurayama Ski Jump Stadium', num: 2, cat: 'attraction', desc: 'Olympic ski jump venue with chairlift ride to summit viewpoint' },
        { lat: 43.0555, lng: 141.2800, label: 'Okurayama Olympic Museum', num: 3, cat: 'attraction', desc: '1972 Winter Olympics memorabilia and interactive exhibits' },
        { lat: 43.0437, lng: 141.3562, label: 'Nakajima Park Onsen Area', num: 4, cat: 'attraction', desc: 'Central park with nearby traditional bathhouses for post-ski recovery' },
        { lat: 43.0544, lng: 141.3548, label: 'Daruma Jingisukan', num: 5, cat: 'food', desc: 'Legendary Genghis Khan BBQ restaurant — since 1954' }
      ]
    },
    {
      num: 3,
      date: '2026-03-21',
      neighborhoods: 'Niseko · Grand Hirafu · Sapporo Susukino',
      title: 'Niseko Day Trip — Hokkaido\'s World-Famous Powder',
      description: "Today you make the pilgrimage to Niseko — arguably the best ski resort in Asia and famous worldwide for its ultra-light, ultra-deep Hokkaido powder snow. Even in late March you'll find the runs in great shape with smaller crowds than peak January. The two-hour journey from Sapporo is half the adventure, winding through snow-plastered Hokkaido farmland with Mount Yotei (Hokkaido's Fuji) guiding you the whole way.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Early Bus to Niseko Grand Hirafu',
              description: "Catch the Donan Bus from Sapporo Station (Bus Terminal, South exit) to Niseko Grand Hirafu — the biggest and most varied of the four interconnected Niseko United resorts. The bus takes about 2 hours and drops you right at the base. Book tickets in advance online or at the station.",
              details: [
                '🚌 Donan Bus: departs Sapporo Station ~7:30am, arrives Hirafu ~9:40am · ¥2,500 one-way',
                '🎫 Book at the Donan Bus counter (South exit, Bus Terminal) or online',
                '🗻 Mount Yotei visible the entire drive — an almost perfect volcanic cone',
                '⛷️ Niseko United lift pass: ¥8,800/day (links Grand Hirafu, Annupuri, Hanazono, Niseko Village)'
              ]
            },
            {
              title: 'Skiing Niseko Grand Hirafu',
              description: "Niseko Grand Hirafu has 42 runs across 476 hectares — from gentle groomed blues to challenging off-piste powder fields. In late March the lower mountain is often groomed spring snow while upper runs can still get fresh snowfall. The back bowls are magical on a clear day.",
              details: [
                '🎿 Green/blue runs dominate the lower mountain — great for mixed ability groups',
                '🌨️ King gondola whisks you to 1,080m — the real Niseko experience starts here',
                '🏂 Advanced riders: Gate 1 off-piste on a powder day is unforgettable',
                '🌡️ Late March temps: -5°C to +3°C — dress in layers, waterproof outer essential'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Niseko Ramen Bar (Upper Hirafu Village)',
              description: 'Ski boot-friendly ramen right in Hirafu Village — steaming bowls of shio (salt) and miso ramen to refuel. The ski-in/ski-out convenience is unbeatable on a long powder day.',
              meta: '💰 ¥1,200–1,800 · 📍 Hirafu Village, walking distance from gondola base'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'More Skiing + Hirafu Village Explore',
              description: "Keep the turns going through the afternoon. As the sun drops, the light on Yotei turns extraordinary — stop on an upper run for the view before heading down. With an hour before your return bus, explore Hirafu Village: browse ski shops, pick up Hokkaido cheese, or warm up at a café.",
              details: [
                '☕ Hirafu has excellent coffee — Café Hip and Bang2 Café are popular stops',
                '🧀 Hokkaido dairy products at any village shop are extraordinary',
                '🚌 Return bus to Sapporo departs ~5:00-5:30pm — confirm your return ticket time'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍛 Dinner',
              name: 'Soup Curry at Garaku (ガラク)',
              description: "Sapporo's signature dish is the perfect post-ski recovery meal. Soup curry is a Sapporo invention: a thin, deeply spiced broth with a whole roasted chicken leg or vegetables, served with fluffy Hokkaido rice. Garaku is consistently Sapporo's most popular soup curry shop — expect a short queue, but it moves fast.",
              meta: '💰 ¥1,000–1,600 · 📍 South 1, West 4, Chuo-ku · Opens 11:30am, closes when sold out'
            }
          ],
          tips: [
            { type: 'tip', text: 'Arrive at Garaku right at opening or budget 30 min queue time — it\'s worth every minute. You can customize heat level from 1 (mild) to 40 (face-melting). Level 5-10 is a great starting point.' }
          ]
        }
      ],
      mapPins: [
        { lat: 43.0686, lng: 141.3509, label: 'Sapporo Station Bus Terminal', num: 1, cat: 'attraction', desc: 'Donan Bus departure for Niseko — south exit, arrive 30 min early' },
        { lat: 42.8461, lng: 140.6870, label: 'Niseko Grand Hirafu', num: 2, cat: 'attraction', desc: 'Asia\'s most famous ski resort — powder runs, Mount Yotei views' },
        { lat: 42.8350, lng: 140.6875, label: 'Hirafu Village', num: 3, cat: 'attraction', desc: 'Ski village base — rentals, restaurants, après-ski cafés' },
        { lat: 42.8295, lng: 140.6882, label: 'Mount Yotei Viewpoint', num: 4, cat: 'attraction', desc: 'Hokkaido\'s perfect volcanic cone — views from upper Niseko runs' },
        { lat: 43.0567, lng: 141.3498, label: 'Soup Curry Garaku', num: 5, cat: 'food', desc: 'Sapporo\'s most beloved soup curry restaurant — arrive early or queue' }
      ]
    },
    {
      num: 4,
      date: '2026-03-22',
      neighborhoods: 'Otaru · Sakaimachi · Otaru Canal',
      title: 'Otaru Day Trip — Canals, Glasswork & Sea Urchin',
      description: "Just 35 minutes from Sapporo by train, Otaru is one of Hokkaido's most charming towns — a former Meiji-era trading port with tree-lined canals, stone warehouses, artisan glass studios, and some of the best seafood in Japan. In late March you'll find the canal still partially snow-dusted, the seafood market bursting with spring crab and freshly caught scallops, and the famous LeTAO patisserie ready to undo all your ski fitness.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'JR Train to Otaru',
              description: "The JR Hakodate Line from Sapporo Station to Otaru runs every 20-30 minutes and takes about 35 minutes — a pleasant ride through snow-covered Hokkaido suburbs. Arrive early to beat day-trippers from the city.",
              details: [
                '🚆 JR Hakodate Line: Sapporo → Otaru · 35 min · ¥640 one-way',
                '⏰ Aim to arrive by 9:30am for the morning market energy',
                '📍 Otaru Station is walking distance from the canal and Sakaimachi Street'
              ]
            },
            {
              title: 'Otaru Canal & Stone Warehouse District',
              description: "The 1.1km Otaru Canal is Japan's most photographed winter scene for good reason — old stone warehouses reflected in dark still water, with snowflakes or cherry blossoms (early petals in late March) overhead. Walk the canal path, cross the footbridges, and explore the converted warehouses now housing restaurants, shops, and galleries.",
              details: [
                '📸 Best photos: early morning when mist rises from the canal',
                '🏛️ Otaru Canal Cruise: 60-min boat tour, ~¥1,500 (check late March availability)',
                '⏰ Canal Plaza (former warehouse complex): open shops and exhibitions'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Sakaimachi Street — Glasswork, Sweets & Music Boxes',
              description: "Sakaimachi is Otaru's most beloved shopping street — a historic stone-paved lane lined with Meiji-era brick buildings housing glass studios, music box workshops, and artisan sweet shops. Kitaichi Glass is the most famous, with hand-blown pieces you won't find elsewhere. Don't miss the Otaru Music Box Museum.",
              details: [
                '🎵 Otaru Music Box Museum (オルゴール堂): thousands of music boxes, free entry to browse',
                '🔮 Kitaichi Glass: hand-blown Hokkaido glass — beautiful gifts',
                '🎶 Watch live glassblowing demonstrations at multiple studios',
                '⏰ Shops open 9am–5pm (some until 6pm)'
              ]
            },
            {
              title: 'Otaru Sankaku Market (三角市場)',
              description: "Squeeze into Otaru's famous triangular market, packed with fresh seafood vendors. This is the spot for a morning seafood experience — grilled scallops, fresh uni (sea urchin) over rice, and live snow crab. Vendors grill right in front of you and it's incredibly good value.",
              details: [
                '🦀 Live snow crab (zuwaigani) and hairy crab (kegani) in season',
                '🦔 Fresh uni over rice: ¥1,500–2,500 — often better here than Tokyo',
                '🐚 Grilled scallops: order directly from vendors, eat on the spot'
              ]
            }
          ],
          meals: [
            {
              type: '🦞 Lunch',
              name: 'Otaru Sankaku Market or Masazushi',
              description: 'Either eat at the market\'s counter restaurants for an informal seafood bowl experience, or splurge at Masazushi — Otaru\'s legendary sushi counter that has been crafting Hokkaido-topped sushi since 1948. The omakase here is exceptional value compared to Tokyo.',
              meta: '💰 ¥2,000–5,000 · 📍 Masazushi: 1-1 Hanazono, Otaru · Book ahead for peak times'
            }
          ],
          tips: [
            { type: 'tip', text: 'LeTAO\'s flagship patisserie is 2 min from the canal — their "Double Fromage" two-layer cheesecake is the thing Otaru is famous for. Buy a box for the train ride back. They ship across Japan too.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Sapporo + LeTAO Detour',
              description: "Head back to Sapporo in the evening. Before leaving, stop at LeTAO's main shop at the bottom of Sakaimachi Street for their famous cheesecake. Then catch the JR train back to Sapporo for a relaxed dinner in Susukino.",
              details: [
                '🍰 LeTAO flagship: corner of Sakaimachi Street and the canal · closes 6pm',
                '🚆 Last convenient train to Sapporo: aim for the 6-7pm window'
              ]
            }
          ],
          meals: [
            {
              type: '🍣 Dinner',
              name: 'Toriton — Hokkaido Kaiten Sushi',
              description: "Back in Sapporo, cap an incredible seafood day with a conveyor belt sushi dinner at Toriton — a Hokkaido-born chain that has earned an almost cult-like following for its extra-thick, ultra-fresh toppings. Plates are ¥130–280 and the quality is extraordinary for the price.",
              meta: '💰 ¥1,500–2,500/person · 📍 Multiple Sapporo locations · Often queues at dinner — put your name in and grab a drink nearby'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 43.1940, lng: 141.0017, label: 'Otaru Station', num: 1, cat: 'attraction', desc: 'JR Hakodate Line arrival — canal and Sakaimachi within walking distance' },
        { lat: 43.1983, lng: 140.9982, label: 'Otaru Canal', num: 2, cat: 'attraction', desc: 'Historic stone warehouse canal — one of Hokkaido\'s most iconic sights' },
        { lat: 43.1954, lng: 141.0014, label: 'Sakaimachi Street', num: 3, cat: 'attraction', desc: 'Stone-paved shopping street — glasswork, music boxes, and Meiji architecture' },
        { lat: 43.1948, lng: 141.0011, label: 'Kitaichi Glass', num: 4, cat: 'attraction', desc: 'Otaru\'s most famous hand-blown glass studio' },
        { lat: 43.1961, lng: 140.9988, label: 'Otaru Sankaku Market', num: 5, cat: 'food', desc: 'Tight little seafood market — grilled scallops, uni, live crab vendors' },
        { lat: 43.1952, lng: 141.0009, label: 'LeTAO Flagship Patisserie', num: 6, cat: 'food', desc: 'Otaru\'s famous cheesecake — the "Double Fromage" is unmissable' }
      ]
    },
    {
      num: 5,
      date: '2026-03-23',
      neighborhoods: 'Maruyama · Hokkaido Shrine · Sapporo Beer District',
      title: 'Shrines, Brews & Sapporo Classics',
      description: "A day to sink deep into the city itself — morning at Hokkaido's most sacred Shinto shrine in snowy Maruyama Park, afternoon tasting the beer that made this city famous, and an evening dive into Sapporo's local izakaya scene with Genghis Khan lamb and cold malt on tap at the legendary Beer Garden.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Maruyama Park & Hokkaido Shrine',
              description: "Maruyama Park is Sapporo's most beloved urban forest — 600 ancient trees, walking paths, and the grandest shrine in all of Hokkaido at its heart. In late March, the park is transitioning between winter and early spring — pristine snow still covers the grounds, and the shrine's orange torii gates glow against the white. The pre-cherry blossom calm is magical.",
              details: [
                '⛩️ Hokkaido Shrine (北海道神宮): free entry, founded 1869 — one of Japan\'s great shrines',
                '🌳 The forest walk through Maruyama takes 30-45 min at a gentle pace',
                '🐿️ Look for Ezo squirrels (Ezorisu) in the trees — they\'re everywhere in winter',
                '📍 15-min subway ride from Odori: Tozai Line to Maruyama Koen Station'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast / Late Brunch',
              name: 'Maruyama Café Area (around Maruyama Koen Station)',
              description: 'The cafés clustered around Maruyama Koen Station are among Sapporo\'s most beloved morning spots — independent coffee shops with excellent Hokkaido pastries and eggs. It\'s the city\'s "cool neighborhood" equivalent.',
              meta: '💰 ¥600–1,200 · 📍 Maruyama Koen Station area, Chuo-ku'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Sapporo Beer Museum',
              description: "This gorgeous red-brick building — a functioning brewery from 1876 — is a piece of living Japanese history. The free museum section walks you through the Meiji-era birth of Japan's beer industry, while the paid tasting room lets you sample brews only available here, including museum-exclusive limited editions. The adjacent Bier Garten is one of Sapporo's most fun dinner venues.",
              details: [
                '🍺 Museum: Free admission · Open 11am–8pm',
                '🍻 Premium Tasting Room: ~¥800 for 3-beer flight including museum exclusives',
                '🏛️ Architecture alone is worth visiting — red brick Meiji-era industrial',
                '📍 5-min walk from Sapporo Station (North Exit) or Hokkaido University area'
              ]
            },
            {
              title: 'Hokkaido University Campus & Poplar Grove',
              description: "A 15-minute walk from the Beer Museum takes you into the Hokkaido University campus — one of Japan's most beautiful, with a famous poplar-lined avenue and a working experimental farm. In late March, the snow-draped trees and open fields feel vast and meditative.",
              details: [
                '🌲 The famous poplar avenue (ポプラ並木) is best in late afternoon light',
                '🐄 The university farm still has grazing animals even in late winter',
                '📸 Free to enter — the clock tower and gingko avenue are Sapporo icons'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sapporo Beer Garden — Genghis Khan Night',
              description: "The Sapporo Beer Garden complex is the most iconic place in all of Japan to drink the city's namesake beer. The main hall (Kessel Hall) is set inside the original 1890 brick brewery with soaring ceilings, copper kettles, and long communal tables. Order the all-you-can-eat Genghis Khan lamb set with unlimited draft Sapporo — a group feast for the ages.",
              details: [
                '🐑 Jingisukan all-you-can-eat sets: ~¥3,800–5,500/person (includes 90 min unlimited beer)',
                '🏛️ Kessel Hall is the main hall — the most atmospheric setting',
                '⏰ Dinner from 5pm · Book ahead for groups — very popular',
                '🍺 The draft Sapporo here is served fresh from the on-site brewery'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Book the Sapporo Beer Garden for groups via their website or phone ahead. Friday and Saturday evenings fill up fast. They also have a famous cheese fondue set during winter months.' }
          ]
        }
      ],
      mapPins: [
        { lat: 43.0572, lng: 141.3212, label: 'Hokkaido Shrine (Hokkaido Jingu)', num: 1, cat: 'attraction', desc: 'Hokkaido\'s most sacred Shinto shrine — stunning in late-winter snow' },
        { lat: 43.0568, lng: 141.3252, label: 'Maruyama Park', num: 2, cat: 'attraction', desc: 'Ancient forest park with squirrels, walking paths, and winter charm' },
        { lat: 43.0694, lng: 141.3718, label: 'Sapporo Beer Museum', num: 3, cat: 'attraction', desc: 'Historic 1876 red-brick brewery — free museum and premium tasting room' },
        { lat: 43.0765, lng: 141.3417, label: 'Hokkaido University Campus', num: 4, cat: 'attraction', desc: 'Beautiful campus with poplar avenues and snow-covered fields' },
        { lat: 43.0694, lng: 141.3718, label: 'Sapporo Beer Garden (Kessel Hall)', num: 5, cat: 'food', desc: 'All-you-can-eat Genghis Khan BBQ in the original copper-kettled brewery hall' }
      ]
    },
    {
      num: 6,
      date: '2026-03-24',
      neighborhoods: 'Jozankei Onsen · Nakajima Park · Susukino',
      title: 'Jozankei Onsen & Farewell Sapporo Feast',
      description: "Your final full day is pure rest, reward, and indulgence — a morning soak in the mountain hot springs of Jozankei, where the Toyohira River carves through snow-capped valley walls and outdoor rotenburo baths steam against the cold sky. Return to Sapporo for one last afternoon of exploration, then go out in style with a legendary Sapporo farewell dinner: fresh king crab, a final bowl of miso ramen, or whatever the group decides is their white whale of the trip.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Jozankei Onsen Valley',
              description: "Jozankei is Hokkaido's most accessible mountain hot spring resort, just 45 minutes from central Sapporo by bus. The valley town sits where the Toyohira River meets forested mountains, with over a dozen ryokan and spa facilities. In late March, snow still blankets the valley walls and the outdoor baths (rotenburo) are steaming perfection.",
              details: [
                '🚌 Jozankei Liner bus from Sapporo Odori Station: ~45 min, ¥780 one-way',
                '♨️ Hoheikyo Onsen Day Spa: the largest facility, great outdoor baths, ¥1,000 entry',
                '🛁 Daiichi Takimotokan: elegant ryokan with multiple indoor/outdoor pools, day use available',
                '🌊 The Futami Bridge over the Toyohira River has excellent valley views',
                '⏰ Most day-use baths: 10am–3pm window for non-guests'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Ryokan Lunch Set at Jozankei',
              description: 'Many Jozankei ryokan offer kaiseki-style lunch sets for day visitors alongside their onsen access. The Hokkaido set meals feature local venison, mountain vegetables, miso-pickled fish, and extraordinary Hokkaido dairy desserts.',
              meta: '💰 ¥2,500–4,500 · 📍 Various ryokan at Jozankei — Daiichi Takimotokan or Manseikaku'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Return to Sapporo — JR Tower Observation Deck',
              description: "Back in the city, ride the elevator up to the JR Tower T38 observation deck on the 38th floor of the Stellar Place tower above Sapporo Station. On a clear late-March afternoon, you can see the full sweep of Hokkaido: the city grid below, the ski mountains to the west, and on the clearest days, even the distant Pacific.",
              details: [
                '🏙️ JR Tower T38: ¥740/adult · Open 10am–10:30pm',
                '📍 Above JR Sapporo Station — directly accessible from the station',
                '📸 North-facing windows show the full city with mountains behind',
                '🛍️ Stellar Place shopping mall below — excellent Hokkaido souvenir selection'
              ]
            },
            {
              title: 'Last Wander Through Odori Park',
              description: "Take a final stroll through Odori Park as the late afternoon sun turns the snow golden. In late March you\'re right at the edge of spring — sometimes you\'ll spot the first plum blossoms. Buy a warm corn from a street vendor and soak in the city one last time.",
              details: [
                '🌸 Late March sometimes brings first plum blossom (ume) sightings',
                '🌽 Roasted corn and Hokkaido butter — the quintessential Sapporo street snack',
                '📸 The TV Tower at sunset with mountain silhouettes — your final Sapporo shot'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Susukino Exploration',
              description: "Susukino never gets old. Spend your last evening in Japan\'s greatest northern entertainment district — hop between izakayas, share plates of yakitori, and raise one final Sapporo draft to an extraordinary trip.",
              details: [
                '🍻 One last Sapporo draft, poured in its hometown',
                '🍢 Izakaya crawl: order different dishes at 2-3 bars for the full experience',
                '🎤 Karaoke is obligatory for a proper Sapporo farewell'
              ]
            }
          ],
          meals: [
            {
              type: '🦀 Farewell Dinner',
              name: 'Kani Honke (かに本家) — King Crab Kaiseki',
              description: "Go out in the grandest Hokkaido style: Kani Honke specializes in Hokkaido king crab and snow crab in every imaginable preparation — grilled, steamed, sashimi, shabu-shabu, crab rice. The set courses are generous and the quality extraordinary. This is the meal you'll be telling people about for years.",
              meta: '💰 ¥8,000–15,000/person · 📍 South 3, West 3, Chuo-ku · Reservations strongly recommended'
            }
          ],
          tips: [
            { type: 'tip', text: 'If Kani Honke is over budget, Nijo Market\'s evening counters serve excellent crab at casual prices. Alternatively, Sapporo Kani Club near Susukino does great crab at more accessible price points.' }
          ]
        }
      ],
      mapPins: [
        { lat: 42.9761, lng: 141.1219, label: 'Jozankei Onsen', num: 1, cat: 'attraction', desc: 'Mountain hot spring valley — outdoor baths steaming against snow-covered peaks' },
        { lat: 42.9748, lng: 141.1205, label: 'Hoheikyo Onsen Day Spa', num: 2, cat: 'attraction', desc: 'Largest day-use onsen facility at Jozankei — indoor and outdoor pools' },
        { lat: 43.0686, lng: 141.3509, label: 'JR Tower T38 Observation Deck', num: 3, cat: 'attraction', desc: '38th floor panoramic views over Sapporo and Hokkaido mountains' },
        { lat: 43.0606, lng: 141.3564, label: 'Odori Park (Final Walk)', num: 4, cat: 'attraction', desc: 'Farewell sunset stroll — roasted corn vendors and golden light' },
        { lat: 43.0542, lng: 141.3565, label: 'Kani Honke', num: 5, cat: 'food', desc: 'Legendary crab kaiseki restaurant — the ultimate Hokkaido farewell feast' },
        { lat: 43.0550, lng: 141.3540, label: 'Susukino Final Night', num: 6, cat: 'food', desc: 'Izakaya crawl and karaoke for the perfect Sapporo send-off' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '¥8,000–15,000/night', midrange: '¥15,000–30,000/night', luxury: '¥30,000–80,000/night' },
    { category: 'Meals (per person)', budget: '¥2,000–3,500/day', midrange: '¥4,000–8,000/day', luxury: '¥10,000–20,000/day' },
    { category: 'Ski Day (Teine)', budget: '¥5,700 (Olympia)', midrange: '¥8,200 (Highland)', luxury: '¥12,000+ (private guide)' },
    { category: 'Ski Day (Niseko)', budget: '¥8,800 (lift pass)', midrange: '¥14,000 (pass + rentals)', luxury: '¥25,000+ (guide + premium)' },
    { category: 'Onsen (Jozankei)', budget: '¥1,000 (day use)', midrange: '¥3,000–5,000 (lunch set)', luxury: '¥15,000+ (overnight stay)' },
    { category: '6-Day Total (group of 4)', budget: '¥200,000–280,000', midrange: '¥350,000–500,000', luxury: '¥600,000–1,000,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['New Chitose Airport (CTS) is 40 km southeast of Sapporo', 'JR Rapid Airport train: 37 min to Sapporo Station, ¥1,150', 'Direct flights from Tokyo (55 min), Osaka (90 min), and many international hubs via Tokyo connection'] },
    { title: '🏨 Where to Stay', items: ['Sapporo Susukino / Odori area: best location for all activities', 'JR Inn Sapporo: excellent value near the station', 'Sapporo Grand Hotel: classic historic hotel in central Odori', 'Nakajima Park area: quieter, ryokan-style options', 'Book well ahead — late March sees solid demand from skiers'] },
    { title: '🌡️ Weather', items: ['Late March averages: -3°C to +5°C (27–41°F)', 'Snow still on the ground in the city; mountain resorts in full swing', 'Days are lengthening — about 12 hours of daylight by late March', 'Pack proper ski layers, waterproof outer jacket, and thermal base layers', 'Bring proper winter boots — icy sidewalks are common'] },
    { title: '💴 Money', items: ['Japan remains cash-friendly — carry ¥20,000–30,000/person/day for market visits and cash-only spots', 'IC card (Suica or Sapica): load at the station for seamless subway/bus travel', '7-Eleven and Japan Post ATMs accept international cards reliably', 'Restaurant bills are typically paid at the register, not tableside'] },
    { title: '📱 Connectivity', items: ['Buy a data SIM or eSIM at New Chitose Airport arrivals hall (IIJ, HISMobile)', 'Pocket WiFi rentals available at airport counters if your group prefers sharing', 'Google Maps works excellently throughout Hokkaido', 'Line app for messaging; Google Translate camera mode for menus'] },
    { title: '🗣️ Language Tips', items: ['Sapporo is more tourist-savvy than most Japanese cities due to ski tourism', 'A few key phrases: Sumimasen (excuse me), Kore kudasai (this one please), Ikura desu ka? (how much?)', 'Most ski resort staff and tourist district restaurants have some English', 'Download Google Translate offline Japanese pack before you fly'] }
  ]
};

try {
  fulfillOrder(order, itineraryData);
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
