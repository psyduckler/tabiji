const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772625956315_u924ah',
  email: 'galaxycats510@gmail.com',
  destination: 'Sapporo, Hokkaido, Japan',
  startDate: '2026-03-19',
  endDate: '2026-03-25',
  groupSize: '3-4',
  requests: 'Would love to have lots of fun. Go skiing, see snow and play with snow. Wouldn\'t mind taking day trips. I want to go somewhere SIMILAR to kamikochi, so beautiful lake sceneries. I don\'t mind taking day trips. Would love beautiful scenery. Would love some onsen and I love spirited away vibes or Ghibli vibes in general. I love taking pictures too.'
};

const itineraryData = {
  destination: 'Sapporo, Hokkaido, Japan',
  countryEmoji: '🇯🇵',
  title: 'Snow, Onsens & Ghibli Magic in Sapporo',
  subtitle: '7 days of powder skiing, fairytale lake sceneries, steaming hot springs & Susukino nights',
  description: 'Hokkaido in March is a winter dream — deep powder snow still blankets the mountains, onsens steam under crystal skies, and the landscapes look lifted straight from a Studio Ghibli film. This itinerary balances thrilling days on the slopes of Sapporo Teine with soul-stirring scenery at Lake Shikotsu and Lake Toya (your Kamikochi-style lake fix), enchanting day trips to the historic Otaru canal, and steaming hell-valley onsens at Noboribetsu that are pure Spirited Away magic. Nights end in Susukino — Sapporo\'s vibrant entertainment district — with ramen, izakayas, and neon reflecting off the snow.',
  duration: '6 nights',
  dates: 'Mar 19 – Mar 25, 2026',
  budget: '$$–$$$',
  pace: 'Active',
  bestFor: 'Adventure Seekers, Photographers, Onsen Lovers',

  highlights: [
    'Powder skiing at Sapporo Teine with Mt. Yotei panoramas',
    'Lake Toya — a stunning caldera lake with island reflections (your Kamikochi moment)',
    'Noboribetsu\'s Jigokudani (Hell Valley) — pure Spirited Away energy',
    'Otaru Canal lit by gas lanterns in the snow — impossibly photogenic',
    'Jozankei Onsen: soak in an outdoor rotenburo surrounded by snowy forest',
    'Susukino nightlife — ramen, sake bars, and Hokkaido craft beer under neon lights'
  ],

  essentials: [
    { title: '❄️ March Snow Conditions', text: 'Late March is still excellent for skiing in Hokkaido — Teine typically stays open through late March or early April. Temperatures in Sapporo average -3°C to 4°C. Pack warm layers, waterproof outerwear, and snow boots. The landscapes are still beautifully snow-covered.' },
    { title: '🚃 Getting Around', text: 'Sapporo has a great subway (3 lines). Day trips to Otaru use JR trains (40 min, very frequent). For Lake Shikotsu, Lake Toya, and Noboribetsu, rent a car or book a day-tour van from Sapporo — car rentals are easy and affordable at Sapporo Station. IC card (Kitaca/Suica) covers trains, subways, and buses.' },
    { title: '🏔️ Ski Gear Tips', text: 'Sapporo Teine has full ski rental shops on-site — boards, skis, helmets, boots all available. Niseko is 2.5h from Sapporo for a premium upgrade. Buy a multi-day lift pass in advance for savings. Lessons available in English.' },
    { title: '♨️ Onsen Etiquette', text: 'Tattoos are a consideration — some traditional onsen in Noboribetsu are private-bath (kashi-buro) which welcome everyone. Remove all clothing, shower and rinse before entering the baths. No phones or cameras in the bathing areas. Most provide towels and yukata.' },
    { title: '🍜 Food & Dining', text: 'Sapporo is famous for miso ramen, Genghis Khan (grilled lamb), fresh seafood (sea urchin, crab, salmon), and Sapporo Beer. Susukino\'s izakayas are affordable and lively. Most restaurants have picture menus — pointing and smiling works great.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-19',
      neighborhoods: 'Sapporo Station · Odori Park · Susukino',
      title: 'Arrive in Sapporo — Snow City First Impressions',
      description: 'Touch down in Hokkaido and feel that crisp northern air. Sapporo greets you with wide snowy boulevards, historic red-brick buildings, and the excitement of a city that knows how to do winter right. Your first evening ends in the glowing neon of Susukino.',
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In & Odori Park Snow Walk',
              description: 'Drop your bags and head to Odori Park — the green spine of Sapporo, running 13 blocks through the city center. In March, it\'s still blanketed in snow and the TV Tower at the east end makes for a great orientation photo.',
              details: [
                '🏨 Stay in Susukino or near Sapporo Station — central for all day trips',
                '📸 Odori Park + Sapporo TV Tower: your first Sapporo skyline shot',
                '🏛️ Old Hokkaido Government Building (Red Brick) is a 5-minute walk — free entry, stunning architecture',
                '🎪 Sapporo Clock Tower nearby — Meiji-era wooden building, very photogenic in snow'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The Red Brick Building (Akarenga) is surrounded by snow-covered lawns — incredible for photos. Go inside to see Hokkaido\'s history told through beautiful exhibitions. Free entry.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Tanuki Koji Shopping Arcade & Susukino Exploration',
              description: 'Warm up in Tanuki Koji — an 800-meter covered shopping arcade packed with souvenir shops, cafés, and snack bars that\'s been here since the 1800s. Then venture into Susukino, Hokkaido\'s biggest entertainment district, and take in the neon spectacle.',
              details: [
                '🛍️ Tanuki Koji runs between 1-chome and 7-chome south of Odori Park',
                '📸 Susukino intersection at night — neon reflections on snowy streets = iconic shot',
                '🍺 Grab a Sapporo Classic draft at any izakaya — it\'s only available in Hokkaido'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Sapporo Miso Ramen in Ramen Yokocho',
              description: 'Sapporo\'s famous Ramen Alley (Ramen Yokocho) near Susukino — 17 tiny ramen shops packed into a narrow alley. The Sapporo miso ramen with butter and corn is legendary, perfect for a cold first night.',
              meta: '💰 ¥900–1,200 per bowl · 📍 Susukino, near the intersection · Look for the retro lantern sign'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 43.0603, lng: 141.3530, label: 'Odori Park', num: 1, cat: 'attraction', desc: 'Snow-covered 13-block park — Sapporo\'s heart' },
        { lat: 43.0619, lng: 141.3543, label: 'Sapporo Clock Tower', num: 2, cat: 'attraction', desc: 'Meiji-era wooden clock tower, iconic in snow' },
        { lat: 43.0639, lng: 141.3484, label: 'Red Brick Building (Akarenga)', num: 3, cat: 'attraction', desc: 'Historic Hokkaido Government Building, free entry' },
        { lat: 43.0583, lng: 141.3521, label: 'Tanuki Koji Arcade', num: 4, cat: 'attraction', desc: '800m covered shopping arcade since 1800s' },
        { lat: 43.0535, lng: 141.3540, label: 'Susukino / Ramen Yokocho', num: 5, cat: 'food', desc: 'Neon nightlife district + famous ramen alley' }
      ]
    },
    {
      num: 2,
      date: '2026-03-20',
      neighborhoods: 'Sapporo Teine Ski Resort · Otaru Coast',
      title: 'Powder Day — Skiing & Snow Play at Teine',
      description: 'Today is your ultimate Hokkaido snow day. Sapporo Teine ski resort is only 30 minutes from the city and offers incredible powder runs with panoramic views of the Sea of Japan. Ski, snowboard, sled — or just run out into a snowy field and throw snowballs. This is exactly what you came for.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sapporo Teine Ski Resort',
              description: 'Board a direct shuttle or taxi from Sapporo Station to Sapporo Teine — just 30 minutes away. Teine has two zones: Highland (for intermediate/advanced) and Olympia (beginner-friendly, site of the 1972 Olympic bobsled). The views from the top are breathtaking — Sea of Japan on one side, snow-capped Hokkaido on the other.',
              details: [
                '🎿 Full rental packages available: skis/snowboard + boots + helmet = ~¥5,000–7,000',
                '🚌 Shuttle bus from Sapporo Station to Teine (check Teine website for schedule)',
                '⛷️ Beginner area at Olympia Zone is excellent for first-timers in the group',
                '📸 Top of Highland Zone: panoramic views of the Sea of Japan on a clear day',
                '🏔️ 1972 Winter Olympics was held here — ski the Olympic courses!'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'March at Teine: the snow is still great but slightly spring-like (softer in afternoon). Go early for the best powder. Buy lift tickets online in advance for a discount.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Snow Play & Après-Ski on the Mountain',
              description: 'Between runs, find a gentle slope off the main runs and go wild — make a snowman, have a snowball fight, make snow angels. Hokkaido powder is the best in the world for this. The resort has warming lodges with hot cocoa and Japanese curry.',
              details: [
                '☃️ The deep powder banks beside the runs are perfect for snow play',
                '🍛 Teine\'s restaurant serves hearty Japanese curry and ramen to fuel up',
                '🎿 Last lifts run around 4-4:30pm — check the daily schedule'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Sapporo & Recovery Ramen',
              description: 'Tired muscles and glowing faces — head back to Sapporo and settle in for a big, warming bowl of soup curry (a Sapporo specialty unique to Hokkaido). Your legs will thank you for the early night.',
              details: [
                '🚌 Shuttle back to Sapporo Station',
                '🛁 Your hotel bath or Susukino foot-bath cafés are great for post-ski recovery'
              ]
            }
          ],
          meals: [
            {
              type: '🍲 Dinner',
              name: 'Soup Curry at Garaku',
              description: 'Sapporo\'s most beloved soup curry restaurant — a Hokkaido invention and must-try. Rich broth loaded with huge vegetables and tender chicken or lamb. The wait is worth it.',
              meta: '💰 ¥1,200–1,800 · 📍 Susukino area · May have a queue — arrive early'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 43.1195, lng: 141.1995, label: 'Sapporo Teine Ski Resort', num: 1, cat: 'attraction', desc: '1972 Olympic venue — 2 zones, incredible powder skiing' },
        { lat: 43.1150, lng: 141.2100, label: 'Teine Highland Zone', num: 2, cat: 'attraction', desc: 'Advanced runs with Sea of Japan views' },
        { lat: 43.1230, lng: 141.1960, label: 'Teine Olympia Zone', num: 3, cat: 'attraction', desc: 'Beginner-friendly slopes, former Olympic bobsled site' },
        { lat: 43.0535, lng: 141.3540, label: 'Susukino / Garaku Soup Curry', num: 4, cat: 'food', desc: 'Best soup curry in Sapporo — Hokkaido specialty' }
      ]
    },
    {
      num: 3,
      date: '2026-03-21',
      neighborhoods: 'Otaru Canal District · Sakaimachi Street · Otaru Port',
      title: 'Otaru — The Ghibli Canal Town',
      description: 'A 40-minute train ride delivers you to Otaru — one of the most photographically beautiful towns in Japan. Snow-dusted Meiji-era stone warehouses line a romantic canal lit by antique gas lanterns. Glassblowing workshops, sake breweries, music boxes, and the freshest sushi you\'ll ever eat. This is your Ghibli day.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'JR Train to Otaru & Canal Morning Walk',
              description: 'Catch the JR Hakodate Line from Sapporo Station to Otaru (35-45 min, ¥640). The Otaru Canal is a 10-minute walk from the station. In morning light, the snow-covered stone warehouses reflected in the still canal water are extraordinary. Gas lanterns still glow. You\'ll shoot hundreds of photos.',
              details: [
                '🚂 JR trains run frequently — first one around 6am, then every 15-30 min',
                '📸 The canal is most magical at golden hour (early morning) before crowds arrive',
                '🏚️ AsaRI Canal area is slightly less crowded than the main stretch — equally beautiful',
                '🕯️ Gas lanterns line both sides of the canal — they glow even in daytime for atmosphere'
              ]
            }
          ],
          meals: [
            {
              type: '🦞 Brunch/Lunch',
              name: 'Sushi on Sushiya-dori (Sushi Street)',
              description: 'Otaru\'s famous Sushi Street is a short walk from the canal. Ultra-fresh Hokkaido seafood — sea urchin (uni), crab (kani), salmon, and ikura (salmon roe) at market prices. The sets are incredible value for the quality.',
              meta: '💰 ¥1,500–4,000 per set · 📍 Sakaimachi/Sushiya-dori · Opens from 11am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kitaichi Glass & Music Box Museum',
              description: 'Otaru has been famous for hand-blown glasswork since the Meiji period when glass floats were made for fishing nets. Kitaichi Glass on Sakaimachi Street has beautiful hand-crafted pieces. Next door, the Otaru Music Box Museum (Otaru Orgel-do) has thousands of intricate music boxes — very Ghibli.',
              details: [
                '🎵 Otaru Orgel-do: largest music box museum in Japan — free to browse, buy as souvenirs',
                '🫧 Kitaichi Glass: watch artisans at work and buy unique hand-blown pieces',
                '🏛️ Sakaimachi Street: 400m of Meiji stone buildings converted to shops and cafés',
                '📸 Entire street looks like a Ghibli background — every corner is a photo'
              ]
            },
            {
              title: 'Sake Tasting & Otaru Old Brewery',
              description: 'Otaru has several sake breweries and a beautiful old brewery building (Otaru Beer Brewery in a former warehouse). Sample local sake or Otaru craft beer while sheltered from the cold.',
              details: [
                '🍶 Tanaka Sake Brewery: guided tastings available, beautiful old warehouse setting',
                '🍺 Otaru Beer (Otaru Brewery): German-style craft beers in a stunning red-brick building'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Otaru Orgel-do (Music Box Museum) has an amazing "Custom Music Box" workshop — choose a box and melody and they assemble it for you on the spot. Takes 20 minutes and makes a perfect Ghibli-style keepsake.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset Canal & Return to Sapporo',
              description: 'As the light fades, the gas lanterns along the Otaru Canal glow more intensely. Spend 30 minutes just walking the canal at dusk — it\'s one of the most beautiful scenes in Japan. Then catch a train back to Sapporo.',
              details: [
                '🌅 Sunset in Otaru in March: around 6:00pm — canal lanterns + golden light = magic',
                '📸 The canal bridge (Chuo-bashi) at dusk is one of Japan\'s top photo spots',
                '🚂 Trains back to Sapporo run until around midnight'
              ]
            }
          ],
          meals: [
            {
              type: '🍶 Dinner',
              name: 'Izakaya in Sapporo Susukino',
              description: 'Back in Sapporo, dive into a proper izakaya night — small plates of grilled yakitori, edamame, and fried chicken with cold Sapporo Classic draft beer. The lively group atmosphere is perfect.',
              meta: '💰 ¥2,000–3,500pp with drinks · 📍 Susukino streets'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 43.1987, lng: 140.9937, label: 'Otaru Canal', num: 1, cat: 'attraction', desc: 'Snow-lined canal with gas lanterns — pure Ghibli magic' },
        { lat: 43.1966, lng: 140.9946, label: 'Otaru Canal Bridge (Chuo-bashi)', num: 2, cat: 'attraction', desc: 'Best photo spot — canal reflections and old warehouses' },
        { lat: 43.1951, lng: 140.9952, label: 'Otaru Orgel-do Music Box Museum', num: 3, cat: 'attraction', desc: 'Thousands of music boxes + custom workshop' },
        { lat: 43.1958, lng: 140.9948, label: 'Kitaichi Glass', num: 4, cat: 'attraction', desc: 'Famous Otaru hand-blown glasswork on Sakaimachi St' },
        { lat: 43.1990, lng: 140.9962, label: 'Sushiya-dori (Sushi Street)', num: 5, cat: 'food', desc: 'Otaru\'s famous fresh Hokkaido sushi street' },
        { lat: 43.2001, lng: 140.9995, label: 'Otaru Beer Brewery', num: 6, cat: 'food', desc: 'Craft beer in a stunning old warehouse building' }
      ]
    },
    {
      num: 4,
      date: '2026-03-22',
      neighborhoods: 'Lake Shikotsu · Noboribetsu Hell Valley · Noboribetsu Onsen',
      title: 'Hell Valley & Shikotsu — Spirited Away Day',
      description: 'This is your most immersive Ghibli day. Drive to Lake Shikotsu — a breathtaking caldera lake that never freezes, ringed by snow-capped volcanoes — then continue to Noboribetsu\'s Jigokudani (Hell Valley), a steaming otherworldly landscape straight from Spirited Away. End the day soaking in a centuries-old onsen.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive to Lake Shikotsu',
              description: 'Rent a car from Sapporo Station (or book a private day-tour) and drive 1 hour south to Lake Shikotsu. This deep caldera lake is one of Japan\'s clearest — the water stays impossibly blue-green even in winter because it never freezes. The surrounding snow-capped peaks create mirror reflections that look exactly like the mountain lake scenery you were dreaming of.',
              details: [
                '🚗 Drive: ~1 hour from Sapporo via Route 453 (scenic mountain road)',
                '🏔️ Tarumae-zan volcano looms over the lake — perfectly conical, very photogenic',
                '💙 The lake water is a supernatural shade of blue-green year-round',
                '❄️ In March, ice formations and frost-covered shoreline create magical photo conditions',
                '🎿 Skidoo snowmobile tours available on the lake shore in winter'
              ]
            }
          ],
          meals: [
            {
              type: '🦀 Lunch',
              name: 'Poropinai Restaurant at Lake Shikotsu',
              description: 'Rustic lakeshore restaurant serving Hokkaido crab ramen, fresh trout, and warming soups while gazing directly at the lake. Simple but perfect fuel for an adventure day.',
              meta: '💰 ¥1,000–2,000 · 📍 Lake Shikotsu Onsen village'
            }
          ],
          tips: [
            { type: 'tip', text: 'Lake Shikotsu Onsen village is right on the lake shore — a handful of traditional ryokan and a visitor center. Walk the snow-covered shoreline path for the best lake-and-volcano reflection shots.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Noboribetsu Jigokudani — Hell Valley',
              description: 'Drive 45 minutes from Lake Shikotsu to Noboribetsu and walk into Jigokudani (Hell Valley) — a volcanic crater vent belching sulfurous steam, blood-red earth, and bubbling mud pools. The demon statues and steaming landscape feel like a real-life Spirited Away bathhouse. In winter, the steam against snow creates an extraordinarily atmospheric scene.',
              details: [
                '😈 Oni (demon) statues everywhere — Noboribetsu\'s mascot characters',
                '♨️ The steam vents smell of sulfur but the landscape is absolutely surreal',
                '🌡️ The Oyunuma natural hot spring pond bubbles at 50°C — you can see it boiling',
                '📸 The steaming valley against snow-covered hills = pure Ghibli concept art come to life',
                '🥾 Walking path through the valley: 1.3km loop, easy terrain, 30-40 min'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Noboribetsu Onsen Ryokan Soak',
              description: 'Noboribetsu has some of Japan\'s most celebrated onsen — 11 different types of hot spring water naturally occurring in the same small area. Check into a ryokan\'s day-use bath (hitachi-buro) or book a private bath (kashi-buro) if the group prefers privacy. Soak in milky white sulfur waters while snow falls outside.',
              details: [
                '♨️ Daiichi Takimotokan: massive onsen complex with 35 types of baths — day-use available',
                '♨️ Noboribetsu Grand Hotel: beautiful rotenburo outdoor baths with garden views',
                '🔒 Kashi-buro (private baths) at most hotels — tattoo-friendly, book ahead',
                '🌨️ Soaking in outdoor rotenburo while snow falls is a peak Japanese winter experience',
                '🚗 Drive back to Sapporo: ~1.5 hours'
              ]
            }
          ],
          meals: [
            {
              type: '🍣 Dinner',
              name: 'Genghis Khan (Jingisukan) at Daruma',
              description: 'Back in Sapporo, try Genghis Khan — Hokkaido\'s beloved lamb BBQ grilled at the table. Daruma in Susukino is the famous original. The smoky, fun atmosphere is incredible.',
              meta: '💰 ¥2,500–3,500pp · 📍 Susukino · Often has queues — arrive by 6:30pm'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 42.7500, lng: 141.3667, label: 'Lake Shikotsu', num: 1, cat: 'attraction', desc: 'Never-freezing caldera lake with volcano reflections' },
        { lat: 42.7470, lng: 141.3520, label: 'Lake Shikotsu Shoreline Walk', num: 2, cat: 'attraction', desc: 'Snow-covered path with the best lake-and-mountain views' },
        { lat: 42.7556, lng: 141.3575, label: 'Shikotsu Onsen Village', num: 3, cat: 'attraction', desc: 'Small hot-spring village right on the lake shore' },
        { lat: 42.4897, lng: 141.1024, label: 'Jigokudani Hell Valley', num: 4, cat: 'attraction', desc: 'Volcanic steaming valley — Spirited Away come to life' },
        { lat: 42.4920, lng: 141.1035, label: 'Oyunuma Pond', num: 5, cat: 'attraction', desc: '50°C naturally boiling hot spring pond in the valley' },
        { lat: 42.4872, lng: 141.1039, label: 'Noboribetsu Onsen', num: 6, cat: 'attraction', desc: 'Japan\'s premier onsen town — 11 types of hot spring water' },
        { lat: 43.0530, lng: 141.3545, label: 'Daruma Jingisukan', num: 7, cat: 'food', desc: 'Legendary Hokkaido lamb BBQ in Susukino' }
      ]
    },
    {
      num: 5,
      date: '2026-03-23',
      neighborhoods: 'Lake Toya · Showa Shinzan · Toyako Onsen',
      title: 'Lake Toya — Your Kamikochi Moment',
      description: 'Drive to Lake Toya — a vast caldera lake ringed by perfect volcanic peaks with a wooded island at its center. In winter, the snow-dusted mountain reflections in the glassy water create exactly the serene, magical lake scenery you were after. This is Hokkaido at its most breathtaking.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Drive to Lake Toya — Panoramic Arrival',
              description: 'Drive 2 hours south from Sapporo (or take an express bus) to Lake Toya, a massive caldera lake formed 110,000 years ago. As you crest the hill above Toyako Onsen town, you\'ll suddenly see the whole lake spread below you with Mt. Usu and Showa Shinzan behind — one of the most dramatic natural reveals in Japan.',
              details: [
                '🚗 Drive: 2 hours from Sapporo via Expressway (free with ETC card)',
                '🚌 Donan Bus from Sapporo to Toyako: ~2h 40min, ¥1,970',
                '🏔️ Mt. Usu loomed ominously — it last erupted in 2000, leaving scorch marks visible today',
                '🌊 Nakajima (Middle Island) in the lake center creates perfect reflection symmetry',
                '📸 The panoramic rest stop on Route 453 before descending to the lake: STOP HERE for the best wide shot'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'In March, Lake Toya has almost no tourists — you\'ll often have the shoreline entirely to yourselves. The silence, the mountain reflections, and the snow is Kamikochi-level stunning without any crowds.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Lake Toya Shoreline & Nakajima Island',
              description: 'Walk the lake shoreline path through Toyako Onsen town. In winter, the path is snow-covered and quiet, with perfect mountain reflections. In spring-shoulder season (late March), ducks and swans appear on the lake edge. A ferry to Nakajima Island runs from spring — check if running in late March.',
              details: [
                '🦢 Waterbirds gather at the lake edge in late March',
                '⛵ Nakajima Island ferry: check seasonal schedule at Toyako visitor center',
                '📸 Walk east of the town for the clearest Mt. Usu reflection shots',
                '🌋 Mt. Usu crater path: if snow has melted enough, a short hike offers aerial lake views'
              ]
            },
            {
              title: 'Showa Shinzan & Usu Ropeway',
              description: 'Drive 10 minutes from the lake to Showa Shinzan — a 402m lava dome that literally rose from a wheat field between 1943-1945 due to volcanic activity. Take the Usu Ropeway (if conditions allow) up Mt. Usu for an aerial view of the entire Lake Toya caldera.',
              details: [
                '🌋 Showa Shinzan: one of Japan\'s newest mountains — watch it steam gently',
                '🚡 Usu Ropeway: 6-minute ride, ~¥1,800 return, panoramic caldera views',
                '📸 From the ropeway top: Lake Toya spread below you surrounded by peaks'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Marimite Restaurant at Toyako Onsen',
              description: 'Lakeside restaurant in Toyako Onsen town with window views directly across the lake. Fresh Hokkaido scallops, lake trout, and warming noodles. Very casual, very good.',
              meta: '💰 ¥1,000–2,000 · 📍 Toyako Onsen town center'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Toyako Onsen Lakeside Soak & Return',
              description: 'Toyako Onsen town has ryokan with rotenburo (outdoor baths) facing directly across the lake. Many offer day-use bathing. Soak in steaming water with Lake Toya panoramas stretching before you as the winter sun sets behind the mountains — one of Hokkaido\'s most beautiful onsen experiences.',
              details: [
                '♨️ Windsor Hotel Toya: rooftop onsen with lake views, luxury day-use ¥2,000',
                '♨️ Toyako Manseikaku Hotel: lake-view baths, day-use available',
                '🌅 Sunset over the lake from the rotenburo: allow 2 hours before returning',
                '🚗 Return to Sapporo: ~2 hours'
              ]
            }
          ],
          meals: [
            {
              type: '🍶 Dinner',
              name: 'Susukino Night: Craft Beer at Sapporo Beer Kan',
              description: 'Return to Susukino and celebrate a perfect day at Sapporo Beer Kan — the original Sapporo Beer Hall, a grand 1920s red-brick building. Order the Jingisukan lamb BBQ with draft Sapporo Black Label.',
              meta: '💰 ¥2,000–3,000pp · 📍 Higashi-ku near Sapporo Station · Iconic building'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 42.5970, lng: 140.8382, label: 'Lake Toya', num: 1, cat: 'attraction', desc: 'Vast caldera lake with volcanic mountain reflections' },
        { lat: 42.5898, lng: 140.8254, label: 'Toyako Onsen Town', num: 2, cat: 'attraction', desc: 'Lakeside hot-spring village with panoramic rotenburo' },
        { lat: 42.6050, lng: 140.8400, label: 'Lake Toya Panorama Point', num: 3, cat: 'attraction', desc: 'Best overview of entire caldera before descending' },
        { lat: 42.5338, lng: 140.8587, label: 'Showa Shinzan', num: 4, cat: 'attraction', desc: 'Active lava dome that rose from a wheat field in 1943' },
        { lat: 42.5390, lng: 140.8430, label: 'Usu Ropeway', num: 5, cat: 'attraction', desc: 'Aerial tram with bird\'s-eye caldera views' },
        { lat: 42.5898, lng: 140.8254, label: 'Toyako Onsen Rotenburo', num: 6, cat: 'attraction', desc: 'Outdoor hot springs facing Lake Toya at sunset' }
      ]
    },
    {
      num: 6,
      date: '2026-03-24',
      neighborhoods: 'Jozankei · Moerenuma Park · Shiroi Koibito Park · Susukino',
      title: 'Forest Onsens, Snow Sculptures & Sapporo Nights',
      description: 'Your penultimate day mixes the tranquil and the electric. Morning in Jozankei — a remote mountain onsen village 30 minutes from Sapporo where steam rises from the Toyohira River and the forest feels enchanted. Afternoon at Moerenuma Park (Noguchi\'s snow-covered art landscape) and Shiroi Koibito Park. Then your biggest Susukino night.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Jozankei Onsen — Mountain River Baths',
              description: 'Drive 30 minutes into the mountains south of Sapporo to Jozankei, a hot spring village nestled deep in a forested gorge. The Toyohira River steams in winter — the mineral-rich water is pumped into beautiful ryokan baths. The snow-draped forest and misty river scene is pure Spirited Away.',
              details: [
                '🚌 Bus from Sapporo Chuo Bus Terminal to Jozankei: ~70 min, very scenic',
                '🚗 Or drive 30 minutes via Route 230',
                '♨️ Hoheikyo Onsen: beautiful large baths, day-use ¥600 — extremely popular for good reason',
                '♨️ Jozankei Tsuruga Resort: luxury rotenburo in the treetops above the river',
                '🌊 Futami Suspension Bridge: walk over the steaming Toyohira River gorge in snow'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Onsen Ryokan Breakfast at Jozankei',
              description: 'Many Jozankei ryokan offer day-use breakfast packages — traditional Japanese breakfast (grilled fish, rice, miso, pickles, tofu) in a tatami room overlooking the snowy garden.',
              meta: '💰 ¥1,500–2,000 · 📍 Various ryokan in Jozankei'
            }
          ],
          tips: [
            { type: 'tip', text: 'The Futami Koen suspension bridge over the gorge is only a 5-minute walk from Jozankei\'s main street. The view of steam rising from the river between snow-covered cliffs is unforgettable. Don\'t miss it.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Moerenuma Park — Noguchi\'s Snow Sculpture Garden',
              description: 'Drive back toward Sapporo and visit Moerenuma Park — designed by legendary sculptor Isamu Noguchi as a massive outdoor art installation. In winter, the geometric grass mounds and pyramids are blanketed in white snow, creating a surreal minimalist landscape. Slide down the giant Pyramid hill on a sled for the best ride of the trip.',
              details: [
                '🗿 Isamu Noguchi designed the entire park as one cohesive artwork',
                '⛷️ Snow sledding on the Play Mountain hill — rent sleds at the park entrance',
                '📐 The glass pyramid (Hidamari) is the park centerpiece — free entry',
                '📸 The snow-covered geometric landscape is extraordinary for photography',
                '🚋 Take the subway to Kanjodori Higashi, then taxi or bus 69/79'
              ]
            },
            {
              title: 'Shiroi Koibito Park — Chocolate Wonderland',
              description: 'Hokkaido\'s most beloved souvenir cookie — Shiroi Koibito (White Lover) — is made at this whimsical European-castle themed park in western Sapporo. Tour the factory, sample fresh cookies, and explore the themed gardens. Very fairy-tale, very Ghibli.',
              details: [
                '🍫 Factory tour: watch Shiroi Koibito being made, ¥600',
                '🏰 The building is designed like a European castle with formal gardens',
                '🛍️ Buy fresh cookies and limited Hokkaido-only flavors to take home',
                '🚃 Easy access: Miyanosawa Station (Tozai Subway Line)'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Grand Susukino Night Out',
              description: 'This is your big night in Japan\'s most exciting northern entertainment district. Susukino has 4,000+ establishments — start with cocktails at a rooftop bar, then wander between izakayas and karaoke. The neon-lit streets are electric and the energy is infectious.',
              details: [
                '🎤 Karaoke at Joysound or Big Echo — private rooms for groups, ~¥500/hr per person',
                '🍺 Craft sake bar: Sapporo has excellent junmai sake bars in Susukino',
                '🌃 The Susukino intersection at midnight: neon, snow, crowds — photograph it',
                '🍜 End the night with a 3am bowl of miso ramen at Ramen Yokocho — Sapporo tradition'
              ]
            }
          ],
          meals: [
            {
              type: '🍻 Dinner',
              name: 'Izakaya Hop in Susukino',
              description: 'Do an izakaya crawl — start with fresh Hokkaido oysters and sea urchin at a seafood izakaya, move to yakitori skewers and sake, end at a standing bar for nightcaps. Every place has plastic food displays outside so ordering is easy.',
              meta: '💰 ¥3,000–5,000pp with drinks · 📍 Susukino any direction'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 42.9773, lng: 141.1547, label: 'Jozankei Onsen', num: 1, cat: 'attraction', desc: 'Mountain gorge onsen village — pure Spirited Away steam' },
        { lat: 42.9810, lng: 141.1580, label: 'Futami Suspension Bridge', num: 2, cat: 'attraction', desc: 'Gorge bridge with steaming river views in winter' },
        { lat: 42.9760, lng: 141.1510, label: 'Hoheikyo Onsen', num: 3, cat: 'attraction', desc: 'Best day-use onsen in Jozankei, ¥600' },
        { lat: 43.1247, lng: 141.4185, label: 'Moerenuma Park', num: 4, cat: 'attraction', desc: 'Noguchi\'s snow sculpture garden — sled the pyramids' },
        { lat: 43.0879, lng: 141.2936, label: 'Shiroi Koibito Park', num: 5, cat: 'attraction', desc: 'Fairy-tale chocolate factory park, Hokkaido\'s best souvenir' },
        { lat: 43.0535, lng: 141.3540, label: 'Susukino Entertainment District', num: 6, cat: 'food', desc: 'Sapporo\'s legendary neon nightlife — 4000+ venues' }
      ]
    },
    {
      num: 7,
      date: '2026-03-25',
      neighborhoods: 'Sapporo Beer Museum · Hokkaido Jingu · Airport',
      title: 'Final Morning — Beer, Shrines & Sayonara',
      description: 'Your last morning in Hokkaido. Spend it savoring the places you haven\'t hit yet — the historic Sapporo Beer Museum, the snow-covered gardens of Hokkaido Jingu shrine, and one last miso ramen before heading to the airport. Sapporo will pull at your heart.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sapporo Beer Museum & Garden',
              description: 'Sapporo Beer is Japan\'s oldest beer brand (est. 1876) and the original brewery — a grand red-brick Victorian factory — is now a museum and restaurant. The museum is free and fascinating. A Sapporo Classic draft here, at the source, is mandatory.',
              details: [
                '🍺 Museum free, premium tasting tour ¥500',
                '🏭 The building is a Meiji-era brick masterpiece — stunning in winter light',
                '🐑 Beer Garden Bier Grill: open for lunch — Jingisukan lamb BBQ + draft beer',
                '🚋 Tram stop: Sapporo Beer En-mae or taxi from Sapporo Station (10 min)'
              ]
            },
            {
              title: 'Hokkaido Jingu Shrine',
              description: 'A calm, forested Shinto shrine in Maruyama Park — one of Sapporo\'s most sacred spaces. In winter, the stone pathway through the ancient trees is flanked by deep snow and absolute silence. A beautiful, meditative final morning.',
              details: [
                '⛩️ Founded in 1869 when Hokkaido was being settled by Japan',
                '🌲 The approach path through Maruyama Forest is breathtaking in snow',
                '🙏 Draw an omikuji (fortune) for your travels ahead',
                '🚇 Maruyama Koen Station (Tozai Line) — 10 minute walk to the shrine'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Final Ramen',
              name: 'One Last Miso Ramen — Menya Saimi',
              description: 'Sapporo\'s most awarded miso ramen shop — rich, umami-deep broth with thick noodles and roasted pork. A perfect final meal before the airport.',
              meta: '💰 ¥1,100–1,400 · 📍 Near Sapporo Station · Opens 11am · May have a short queue'
            }
          ],
          tips: [
            { type: 'tip', text: 'Leave for New Chitose Airport (CTS) at least 90 minutes before departure. Airport is 35-40 minutes by express train from Sapporo Station (¥1,150). The airport has fantastic last-minute shopping — ramen, Shiroi Koibito, crab-flavored chips, and Hokkaido dairy products.' }
          ]
        }
      ],
      mapPins: [
        { lat: 43.0726, lng: 141.3678, label: 'Sapporo Beer Museum', num: 1, cat: 'attraction', desc: 'Japan\'s oldest beer brand — Meiji red-brick brewery museum' },
        { lat: 43.0543, lng: 141.3195, label: 'Hokkaido Jingu Shrine', num: 2, cat: 'attraction', desc: 'Sacred Shinto shrine in snowy forest of Maruyama' },
        { lat: 43.0560, lng: 141.3215, label: 'Maruyama Park', num: 3, cat: 'attraction', desc: 'Ancient forest surrounding the shrine — peaceful in snow' },
        { lat: 43.0640, lng: 141.3498, label: 'Menya Saimi', num: 4, cat: 'food', desc: 'Award-winning miso ramen — the perfect final Sapporo meal' },
        { lat: 42.7760, lng: 141.6923, label: 'New Chitose Airport (CTS)', num: 5, cat: 'attraction', desc: '35 min express train from Sapporo — excellent last-minute shopping' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '¥8,000–12,000/night', midrange: '¥12,000–20,000/night', luxury: '¥25,000–60,000/night' },
    { category: 'Meals (per person)', budget: '¥2,500–4,000/day', midrange: '¥4,000–8,000/day', luxury: '¥10,000+/day' },
    { category: 'Ski Day (Teine)', budget: '¥6,000–8,000pp', midrange: '¥10,000–12,000pp', luxury: '¥15,000+ (Niseko)' },
    { category: 'Day Trip Transport', budget: '¥1,500–3,000pp (bus)', midrange: '¥4,000–7,000 (car rental)', luxury: '¥15,000+ (private van)' },
    { category: 'Onsen Day-Use', budget: '¥600–1,500pp', midrange: '¥2,000–3,500pp', luxury: '¥5,000+ (private bath)' },
    { category: '7-Day Total (group of 3)', budget: '¥300,000–450,000', midrange: '¥500,000–750,000', luxury: '¥900,000+' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['New Chitose Airport (CTS) serves Sapporo — Japan\'s 4th busiest airport', 'Express train (Airport Limited Express) to Sapporo Station: 35-40 min, ¥1,150', 'International flights from Tokyo (Haneda/Narita): 1.5 hours', 'Bus from airport to Sapporo: ¥1,100, 70 min'] },
    { title: '🏨 Where to Stay', items: ['JR Tower Hotel Nikko Sapporo: luxury on top of Sapporo Station — unbeatable convenience', 'Cross Hotel Sapporo: boutique mid-range near Susukino, great value', 'Daiwa Roynet Hotel: reliable business hotel near subway, affordable', 'For onsen immersion: splurge one night at Jozankei ryokan'] },
    { title: '🌡️ March Weather', items: ['Sapporo averages -3°C to 4°C in late March — still feels like real winter', 'Snow is melting in the city but mountains still have excellent coverage', 'Pack: warm parka, thermal layers, waterproof boots, gloves, hat', 'Days are getting longer — sunset around 6pm by late March', 'March has fewer tourists than February (no Snow Festival crowds)'] },
    { title: '💴 Money & Payments', items: ['Japan is still heavily cash-based — carry ¥10,000–15,000/day', '7-Eleven and convenience store ATMs accept foreign cards reliably', 'IC card (Suica or Kitaca) for all trains, subways, buses — load ¥3,000–5,000', 'No tipping in Japan — it can cause embarrassment'] },
    { title: '📱 Connectivity', items: ['Buy a pocket WiFi at the airport or get an eSIM before departure', 'Google Translate camera mode works well for menus — download Japanese offline', 'Google Maps works perfectly in Japan — download Sapporo/Hokkaido offline', 'Hokkaido Free WiFi at many tourist spots (register once)'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
