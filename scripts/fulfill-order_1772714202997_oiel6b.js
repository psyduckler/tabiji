const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772714202997_oiel6b',
  email: 'galaxycats510@gmail.com',
  destination: 'Sapporo, Hokkaido, Japan',
  startDate: '2026-03-19',
  endDate: '2026-03-25',
  groupSize: '3-4',
  travelStyle: 'Adventure, Cultural, Relaxation, Nightlife',
  dining: 'Casual throughout',
  budget: 'Surprise me',
  requests: 'Ghibli/Spirited Away vibes, snow activities, ice skating, beautiful photos, public transit only, packed but not exhausting',
};

const itineraryData = {
  destination: 'Sapporo, Hokkaido, Japan',
  countryEmoji: '🇯🇵',
  title: 'A Ghibli Winter Escape in Sapporo & Hokkaido',
  subtitle: '7 magical days of powder snow, glowing canal gas lamps, Olympic ice & late-night ramen',
  description: "Sapporo in late March is a winter wonderland on the verge of spring — snow-dusted forests, crystal-clear volcanic lakes, and a city that pulses with some of Japan's best ramen, beer and nightlife. This itinerary keeps your existing framework and fills in every gap with Ghibli-worthy scenery, snow adventures, and the kind of timeless, atmospheric moments that feel straight out of a Miyazaki film. The Otaru Canal at dusk, misty frozen forests, Olympic ice rinks and neon-soaked Susukino nights — Hokkaido winter delivers on every count.",
  duration: '6 nights',
  dates: 'Mar 19 – Mar 25, 2026',
  budget: '$$–$$$',
  pace: 'Moderate',
  bestFor: 'Friends',
  highlights: [
    'Otaru Canal at dusk — gas-lit warehouses & snow create pure Spirited Away magic',
    'Skiing powder at Sapporo Teine with views across Ishikari Bay',
    'Ice skating on the 1972 Olympic rink at Makomanai Arena',
    'Lake Shikotsu\'s otherworldly blue waters framed by snow-covered peaks',
    'Late-night ramen in Susukino\'s legendary neon-lit alleyways',
  ],

  essentials: [
    {
      title: '🧥 Winter Packing',
      text: 'Sapporo in late March averages -2 to 5°C. Pack thermal base layers, a waterproof outer shell, snow boots with good grip (icy sidewalks!), warm gloves and a hat. Ski gear can be rented at Teine. Hand warmers (カイロ) from any convenience store are a game-changer.',
    },
    {
      title: '🚇 Getting Around',
      text: 'Sapporo has an excellent subway network (3 lines, flat ¥210–350 fare). Load an IC card (Kitaca/Suica) at any JR station — tap on/off for buses, subway and JR trains. Airport: take the JR Airport Express (Rapid Airport) from Shin-Chitose Airport → Sapporo Station (37 min, ¥1,150). Always check Hyperdia or Google Maps for transit directions.',
    },
    {
      title: '🍜 Hokkaido Food Musts',
      text: 'Sapporo invented miso ramen — try it at Ramen Yokocho (Ramen Alley). Genghis Khan (lamb BBQ) is Hokkaido\'s signature grill dish. Soup curry is a local specialty. Fresh seafood is exceptional — uni (sea urchin) rice in Otaru, crab at Nijo Market. End any big meal with a Hokkaido milk soft serve or parfait.',
    },
    {
      title: '📸 Photo Hotspots',
      text: 'For Spirited Away vibes: Otaru Canal at dusk when gas lamps glow over the water — arrive at 4:30 PM. Takino Hillside Park\'s snow-covered gorge at mid-morning. Lake Shikotsu\'s impossible blue from the lakeside boardwalk. Sapporo TV Tower from Odori Park looking west along the park at golden hour.',
    },
  ],

  days: [
    {
      num: 1,
      date: '2026-03-19',
      neighborhoods: 'Sapporo City Centre · Odori · Susukino',
      title: 'Arrival Day — Odori Park, Red-Brick Architecture & Susukino Nights',
      description: "Touch down in Sapporo, settle in, and ease into the city with a stroll through Odori Park and the magnificent red-brick Former Hokkaido Government Office building — its snow-dusted grounds look straight out of a Ghibli storybook. The night ends in Susukino, Hokkaido's most famous entertainment district, with legendary miso ramen and bar-hopping under neon lights.",
      timeBlocks: [
        {
          label: 'Morning / Arrival',
          activities: [
            {
              title: 'Arrive at New Chitose Airport → Sapporo',
              description: "Take the JR Airport Express (Rapid Airport) from Shin-Chitose Airport directly to Sapporo Station. Fast, easy, and no stress.",
              details: [
                '🚉 JR Rapid Airport: Shin-Chitose → Sapporo (37 min, ¥1,150)',
                '🪙 Buy an IC card (Kitaca) at the station — use it for all buses, subway & JR',
                '🏨 Hotels near Susukino/Odori Park are ideal — central to everything',
                '📍 Recommended: Cross Hotel Sapporo or JR Inn Sapporo',
              ],
            },
          ],
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Odori Park & Sapporo TV Tower',
              description: "Walk the full length of Odori Park — a 1.5km green corridor right through the city. In late March, snow still dusts the trees and benches, giving it an enchanted winter atmosphere. Climb the Sapporo TV Tower for panoramic views over the city and park below.",
              details: [
                '🗼 TV Tower observation deck: ¥900, open 9AM–10:30PM',
                '📸 Best photo: Stand at the west end of Odori Park looking east — TV Tower + snow-laced park = Ghibli postcard',
                '☕ Grab a coffee at Odori Bisse underground food hall beneath the park',
              ],
            },
            {
              title: 'Former Hokkaido Government Office (Akarenga)',
              description: "A 5-minute walk from Odori Park brings you to the Akarenga — a stunning American neo-baroque red brick building built in 1888, surrounded by manicured snow-covered grounds. The contrast of the deep red brick against white snow is breathtaking and genuinely Ghibli-worthy.",
              details: [
                '🏛️ Free entry to the grounds and interior (closes 5PM)',
                '📸 Shoot from the south path looking north — red brick + snow dome roof',
                '🌳 The surrounding park has gas lamp-style lanterns — especially atmospheric at dusk',
              ],
            },
          ],
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Ramen Yokocho (Sapporo Ramen Alley)',
              description: "Squeeze into a tiny stool at one of the 17 ramen shops crammed into this narrow alley in Susukino — this is where Sapporo miso ramen was born. Order the miso ramen with corn and butter. Steam rising from a bowl in a tiny, shoebox restaurant with lanterns glowing outside = peak Spirited Away atmosphere.",
              details: [
                '📍 Susukino, 5-chome — look for the red lanterns and steam',
                '🍜 Order: Miso ramen with corn & butter (¥900–1,200)',
                '⏰ Best time: 7–9 PM when it\'s buzzing with locals',
                '💡 Most shops seat 10–12 people — expect a short wait, it\'s worth it',
              ],
            },
            {
              title: 'Susukino Bar Hop',
              description: "Sapporo's entertainment district is one of Japan's liveliest — jazz bars, cozy izakayas, and hidden cocktail lounges tucked between neon signs. Try Sapporo Classic draft beer (a local brew only available in Hokkaido) and a plate of grilled seafood skewers.",
              details: [
                '🍺 Sapporo Classic beer on tap — not available outside Hokkaido',
                '🎷 Live jazz bars: Bar Yamatoya or Sapporo Jazz Spot Crawdaddy Club',
                '🦞 Izakaya seafood: fresh crab, scallops and uni (sea urchin) are exceptional',
                '⏰ Susukino runs late — it\'s lively until 2–3AM if you want it',
              ],
            },
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Ramen Yokocho (Ramen Alley)',
              description: 'Legendary narrow alley of 17 ramen shops in Susukino. Sapporo-style miso ramen with corn and butter in a steam-filled, red-lantern-lit setting.',
              meta: '💰 ¥900–1,200 · 📍 Susukino 5-chome · Open daily 11AM–2AM',
            },
          ],
          tips: [
            {
              type: 'tip',
              text: "The Akarenga (red brick office) looks especially magical at dusk when the lanterns glow. Swing by on your way to dinner if you didn't linger in the afternoon.",
            },
          ],
        },
      ],
      mapPins: [
        { lat: 43.0598, lng: 141.3526, label: 'Odori Park', num: 1, cat: 'attraction', desc: '1.5km park through city centre — magical in winter snow' },
        { lat: 43.0611, lng: 141.3573, label: 'Sapporo TV Tower', num: 2, cat: 'attraction', desc: 'Observation deck with panoramic city views, ¥900' },
        { lat: 43.0641, lng: 141.3481, label: 'Former Hokkaido Gov. Office (Akarenga)', num: 3, cat: 'attraction', desc: 'Iconic red-brick Meiji-era building with snowy grounds — pure Ghibli' },
        { lat: 43.0557, lng: 141.3521, label: 'Ramen Yokocho (Ramen Alley)', num: 4, cat: 'food', desc: 'Legendary narrow alley of 17 ramen shops — Sapporo miso ramen' },
        { lat: 43.0544, lng: 141.3529, label: 'Susukino District', num: 5, cat: 'attraction', desc: 'Hokkaido\'s premier nightlife district — neon, izakayas, jazz bars' },
      ],
    },

    {
      num: 2,
      date: '2026-03-20',
      neighborhoods: 'Sapporo Teine · Hokkaido Mountains',
      title: 'Snow Day at Sapporo Teine Ski Resort',
      description: "Strap on skis (or a snowboard, or just boots for the snow fun!) and head to Sapporo Teine — one of Hokkaido's most accessible ski resorts, just 30 minutes from the city centre. Two zones offer runs for every level, and on a clear day you'll see all the way across Ishikari Bay. End the day with a soothing public onsen bath to unknot those ski legs.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'JR Train to Sapporo Teine',
              description: "It's remarkably easy to get to a world-class ski resort by public train. Take the JR from Sapporo Station to Teine Station, then catch the JR bus directly to the resort.",
              details: [
                '🚉 JR Hakodate Line: Sapporo Station → Teine Station (12 min, ¥360)',
                '🚌 JR Bus from Teine Station → Teine Olympia/Highland (15–30 min)',
                '⏰ Leave hotel by 8:30 AM to arrive for lifts opening at 9 AM',
                '🎿 Ski/snowboard rental available at the resort (¥4,000–6,000/day)',
              ],
            },
            {
              title: 'Skiing & Snowboarding at Teine',
              description: "Sapporo Teine has two zones: Olympia (lower, beginner-friendly runs, wide groomed pistes) and Highland (steeper, tree runs, expert terrain). Late March snow is often sun-warmed and forgiving for beginners — perfect conditions. On a clear day, the ocean panorama is stunning.",
              details: [
                '🎿 Olympia Zone: gentle slopes, great for beginners and groups',
                '🏂 Highland Zone: challenging runs, powder stashes in the trees',
                '🌊 Clear-day views across Ishikari Bay — rare winter ocean panorama',
                '📸 Photo opp: group shot on the slopes with the bay in the background',
                '🍜 Lunch at the resort lodge — try their Hokkaido milk soft serve too',
              ],
            },
          ],
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'More Runs + Snow Play',
              description: "Take a few more runs, or just find a snowy slope and go full Ghibli — roll down it, make snow angels, have a snowball fight. There's no wrong way to enjoy Hokkaido powder.",
              details: [
                '❄️ Late March snow is often heavier and wetter — great for building snowballs',
                '☕ Take a warm-up break in the resort lodge with amazake (sweet warm rice wine)',
                '⏰ Head to the bus stop by 3:30 PM for the return journey',
              ],
            },
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Teine Highland Lodge',
              description: 'Resort lodge at the ski area — hot ramen, gyudon (beef bowl) and curry to fuel you back up. Views of the slopes from the windows.',
              meta: '💰 ¥1,000–1,500 · 📍 Inside Teine Highland Zone',
            },
          ],
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Public Sento (Hot Spring Bath) in Sapporo',
              description: "After a day of skiing, nothing restores the body like a Japanese public bath. Find a sento near your hotel and soak those muscles in hot mineral water. Many Sapporo neighbourhoods have old-school neighbourhood bathhouses that feel wonderfully timeless.",
              details: [
                '♨️ Sento (public bathhouse): ¥490–600 entry, towel rental ¥100–200',
                '🔑 Tip: follow the kanji 銭湯 to find local bathhouses',
                '⚠️ Tattoos may be prohibited — call ahead if relevant',
              ],
            },
          ],
          meals: [
            {
              type: '🥩 Dinner',
              name: 'Daruma Genghis Khan (Jingisukan)',
              description: "Hokkaido's signature dish — Genghis Khan lamb BBQ cooked on a dome grill at the table, grilled with vegetables and dipped in a sweet-savory sauce. Daruma in Susukino is the most famous spot. Smoky, fun, and absolutely delicious.",
              meta: '💰 ¥2,000–3,000 pp · 📍 Susukino, Daruma (multiple locations) · Expect queues',
            },
          ],
          tips: [
            {
              type: 'tip',
              text: "Daruma gets packed on weekends — if there's a queue, head to Sapporo Beer Garden (10 min by taxi) which has a huge Genghis Khan hall with no wait.",
            },
          ],
        },
      ],
      mapPins: [
        { lat: 43.1165, lng: 141.1906, label: 'Sapporo Teine Ski Resort', num: 1, cat: 'attraction', desc: '2-zone ski resort accessible by JR train + bus from central Sapporo' },
        { lat: 43.1172, lng: 141.2440, label: 'JR Teine Station', num: 2, cat: 'attraction', desc: 'Transfer point — JR bus to ski resort departs from here' },
        { lat: 43.0575, lng: 141.3519, label: 'Daruma Genghis Khan (Susukino)', num: 3, cat: 'food', desc: 'Iconic Hokkaido lamb BBQ restaurant in Susukino' },
      ],
    },

    {
      num: 3,
      date: '2026-03-21',
      neighborhoods: 'Takino · Makomanai · Sapporo South',
      title: 'Enchanted Forest Park & Olympic Ice Skating',
      description: "Today is for nature and nostalgia. Takino Suzuran Hillside National Government Park is a vast, snow-covered forest wilderness on the edge of the city — think towering trees, ice-fringed rivers and zero crowds. Then head to Makomanai Ice Arena, where Janet Lynn charmed the world at the 1972 Olympics, and take a spin on actual Olympic ice.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Takino Suzuran Hillside National Government Park',
              description: "A 400-hectare national park just outside Sapporo, Takino Hillside Park in winter is a snow-shrouded wonderland of towering Hokkaido forest, frozen streams and misty gorges. It feels remarkably remote and untouched — this is the closest you'll get to wandering into a Hayao Miyazaki forest without a portal.",
              details: [
                '🚌 From Sapporo: Subway to Makomanai Station (Namboku Line) → Jotetsu Bus to Takino Park (30 min)',
                '❄️ The Takino Waterfall Gorge in winter is frozen or half-frozen — ethereal',
                '🌲 Rent snowshoes at the park entrance for ¥500 and explore the forest trails',
                '📸 Best shots: the wooden bridge over the gorge with snow-laden pines',
                '⏰ Open 9AM–5PM. Admission: ¥450 adults',
              ],
            },
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Park Rest House',
              description: 'Simple café inside the park — warm up with hot cocoa, corn soup or a simple set lunch before exploring the trails.',
              meta: '💰 ¥500–1,000 · 📍 Inside Takino Suzuran Park near entrance',
            },
          ],
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: '🛼 Ice Skating at Makomanai Ice Arena (1972 Olympics)',
              description: "A short bus ride from the park brings you to the Makomanai Sekisui Heim Ice Arena — the actual Olympic figure skating venue from the 1972 Sapporo Winter Games. This is where legendary skater Janet Lynn captivated the world. It's still open to the public for recreational skating. Lace up and glide on history.",
              details: [
                '🏟️ Makomanai Sekisui Heim Ice Arena, open Tue–Sun',
                '🛼 Public skating sessions: check schedule at www.sapporoskating.com',
                '👟 Skate rental available on site (¥500–700)',
                '🧤 Gloves required — bring your own or buy at a ¥100 store',
                '📍 Access: walk from Makomanai Subway Station (Namboku Line), ~15 min',
                '💰 Entry + skate rental: approx ¥1,000–1,500 per person',
              ],
            },
          ],
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Soup Curry Dinner',
              description: "Sapporo's own comfort food invention — a light, aromatic curry broth loaded with whole vegetables and your choice of protein. It's warming, photogenic, and incredibly satisfying after a cold outdoorsy day.",
              details: [
                '🍛 Try: Garaku (one of Sapporo\'s most beloved soup curry spots)',
                '🌶️ Spice level: choose your heat level from 1 (mild) to 30+ (fire)',
                '🥦 The vegetables (half an eggplant, a whole drumstick) are cooked until perfect',
                '📍 Garaku: Minami 2-jo Nishi 2-chome, central Sapporo',
              ],
            },
          ],
          meals: [
            {
              type: '🍛 Dinner',
              name: 'Garaku Soup Curry',
              description: "Sapporo's most iconic soup curry restaurant — a cozy, dimly-lit space with the most fragrant curry broth you've ever encountered. Perfect for a cold winter evening.",
              meta: '💰 ¥1,200–1,800 · 📍 Minami 2-jo Nishi, central Sapporo · Arrive by 6PM',
            },
          ],
          tips: [
            {
              type: 'tip',
              text: "Soup curry is a Sapporo specialty you can't find anywhere else in Japan. Don't skip it — it's a top-5 Hokkaido food experience.",
            },
          ],
        },
      ],
      mapPins: [
        { lat: 42.9905, lng: 141.3068, label: 'Takino Suzuran Hillside Park', num: 1, cat: 'attraction', desc: '400ha national park — snow-covered forests, frozen gorge, zero crowds' },
        { lat: 42.9931, lng: 141.3328, label: 'Makomanai Ice Arena (1972 Olympics)', num: 2, cat: 'attraction', desc: 'Olympic figure skating rink, open for public skating — iconic Sapporo experience' },
        { lat: 42.9978, lng: 141.3345, label: 'Makomanai Subway Station', num: 3, cat: 'attraction', desc: 'Namboku Line — gateway to ice arena and Takino Park bus' },
        { lat: 43.0570, lng: 141.3513, label: 'Garaku Soup Curry', num: 4, cat: 'food', desc: 'Sapporo\'s most famous soup curry restaurant — warming and photogenic' },
      ],
    },

    {
      num: 4,
      date: '2026-03-22',
      neighborhoods: 'Lake Toya · Toyako Onsen · Shikotsu-Toya National Park',
      title: 'Lake Toya Day Trip — Volcanic Caldera & Steaming Hot Springs',
      description: "Your Klook day tour takes you to Lake Toya — a perfectly circular volcanic caldera lake surrounded by mountains, with the dramatic Showa Shinzan volcanic dome rising nearby. Steam vents curl up from the hillsides, making the whole landscape feel primordially alive and otherworldly. Volcanic Japan at its most cinematic.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Depart on Klook Day Tour',
              description: "Your Klook tour handles transportation from Sapporo. Sit back and enjoy the 90-minute drive through Hokkaido countryside as the snow-covered volcanic mountains come into view.",
              details: [
                '🚌 Klook day tours typically depart from Sapporo Station at 8:00–9:00 AM',
                '⏰ Confirm departure point and time with your Klook booking',
                '🎒 Pack hand warmers, your camera, and a windproof jacket',
                '🌋 Lake Toya is 80km southwest of Sapporo — a scenic drive through snow-covered hills',
              ],
            },
            {
              title: 'Lake Toya (Toyako) — Caldera Lake Views',
              description: "Lake Toya is one of Hokkaido's most dramatic natural wonders — a nearly perfectly circular caldera formed 110,000 years ago. The lake doesn't freeze in winter (geothermal heat keeps it liquid), giving it an eerily steaming, mystical quality surrounded by snow. This is peak Ghibli-scape.",
              details: [
                '📸 Best photo: stand on the Toyako shore looking towards Nakajima islands with Usu in the background',
                '🌋 Nakajima islands in the centre of the lake — accessible by boat in warmer months',
                '♨️ Geothermal steam rises from the lake surface on cold mornings',
                '🦅 Look for winter eagles and migratory birds around the shoreline',
              ],
            },
          ],
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Showa Shinzan — Japan\'s Youngest Volcano',
              description: "A short drive from the lake brings you to Showa Shinzan — a volcanic lava dome that literally rose out of a wheat field between 1943–1945. It's vivid orange-yellow and steaming, surrounded by pure white snow. Utterly alien and magnificent.",
              details: [
                '🌋 Showa Shinzan is 398m tall and still actively steaming — born in WWII era',
                '📸 The contrast of orange volcanic rock against white snow is incredible',
                '🐻 Bear Ranch Showa Shinzan: a traditional (if controversial) attraction nearby',
                '🚡 Usu Ropeway: cable car up Mt. Usu for panoramic views over lake, volcano and sea',
              ],
            },
            {
              title: 'Toyako Onsen Town',
              description: "The hot spring resort town of Toyako Onsen lines the shore of Lake Toya, its ryokans and hotels billowing steam into the cold air. Even without staying overnight, the lakeside promenade and small shops are worth a stroll.",
              details: [
                '♨️ Day use onsen available at some hotels (¥800–1,500)',
                '🛍️ Pick up Hokkaido souvenir sweets and bear-shaped treats at lakeshore shops',
                '🌅 If your tour allows, the late afternoon light on the lake is extraordinary',
              ],
            },
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Lakeside Restaurant at Toyako',
              description: 'Your Klook tour may include a lunch stop — expect local Hokkaido fare, fresh dairy, and hot comfort food. If not included, the Toyako town restaurants serve simple ramen and set meals.',
              meta: '💰 ¥1,000–2,000 · 📍 Toyako Onsen town — various options along the lake promenade',
            },
          ],
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Sapporo',
              description: "Your Klook tour returns you to Sapporo in the early evening. Freshen up at the hotel, then head out for a relaxed dinner.",
              details: [
                '⏰ Most Klook day tours return to Sapporo around 6–7 PM',
                '🍦 Stop for a Hokkaido soft serve cone on the way back — milk vending machines or convenience store soft serve',
              ],
            },
          ],
          meals: [
            {
              type: '🍣 Dinner',
              name: 'Seafood Izakaya in Susukino',
              description: "Tonight, let the izakayas of Susukino do the work — fresh Hokkaido scallops, hairy crab, and grilled salmon collar with cold Sapporo Classic beer. Relax after a day of sightseeing.",
              meta: '💰 ¥2,500–4,000 pp · 📍 Susukino area — look for 居酒屋 signs',
            },
          ],
        },
      ],
      mapPins: [
        { lat: 42.5983, lng: 140.8025, label: 'Lake Toya (Toyako)', num: 1, cat: 'attraction', desc: 'Perfect circular volcanic caldera lake — steaming, ethereal, Ghibli-esque' },
        { lat: 42.5342, lng: 140.8462, label: 'Mount Usu', num: 2, cat: 'attraction', desc: 'Active volcano with ropeway — panoramic views over lake and sea' },
        { lat: 42.5432, lng: 140.8597, label: 'Showa Shinzan', num: 3, cat: 'attraction', desc: 'Lava dome born 1943–45 — vivid orange volcanic cone, still steaming' },
        { lat: 42.5952, lng: 140.7981, label: 'Toyako Onsen Town', num: 4, cat: 'attraction', desc: 'Hot spring resort town on Lake Toya\'s shore — steam rising everywhere' },
      ],
    },

    {
      num: 5,
      date: '2026-03-23',
      neighborhoods: 'Otaru · Sakaimachi · Canal District',
      title: 'Otaru — The Spirited Away Town 🏮',
      description: "This is the day you've been waiting for. Otaru is a preserved 19th-century port town 35 minutes from Sapporo, and it is, without question, the most Spirited Away place in all of Japan. The old canal lined with stone warehouses converted into restaurants and galleries, gas lamps glowing gold in the evening mist, music boxes chiming in shop windows... it feels like stepping through a portal into the spirit world. Stay for dusk. You'll understand.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'JR Train from Sapporo to Otaru',
              description: "Board the JR train from Sapporo Station and in 35 minutes you'll arrive in another era. The train runs along the coast — if you get a window seat on the left side, you'll catch glimpses of the Sea of Japan.",
              details: [
                '🚉 JR Hakodate or Otaru line: Sapporo Station → Otaru Station (35 min, ¥640)',
                '⏰ Take the 9:00–9:30 AM train to arrive before the day-trippers',
                '🚶 Most Otaru attractions are walkable from the station (10–20 min on foot)',
              ],
            },
            {
              title: 'Otaru Canal — Morning Mist & Stone Warehouses',
              description: "Walk to the canal first thing. In the morning, mist hangs over the water and the stone warehouses cast long reflections. The 1.3km canal is lined with converted merchant warehouses now housing restaurants, bars and galleries. Without crowds, it\'s hauntingly beautiful.",
              details: [
                '🌁 Morning mist + snow + canal reflections = the most atmospheric hour',
                '📸 Best spot: the arched bridge (Asahibashi) at the north end of the canal',
                '🏚️ The red-brick warehouses date to the late 19th-century herring trade era',
                '🦅 Watch for herons and ducks on the canal surface in the morning',
              ],
            },
          ],
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Sakaimachi Street — Glass, Music Boxes & Sweets',
              description: "Otaru\'s main tourist street is packed with incredible artisan workshops. Kitaichi Glass is Hokkaido's most famous glassworks — you can browse hundreds of handcrafted pieces. The Otaru Music Box Museum (Otaru Orgel-do) has over 3,000 music boxes, from pocket-watch sized to elaborate steampunk towers.",
              details: [
                '🫙 Kitaichi Glass: Meiji-era building, gorgeous coloured glasswork, free to browse',
                '🎵 Otaru Music Box Museum (Orgel-do): ¥0 entry, buy a custom music box from ¥1,500',
                '🍫 Rokkatei chocolate café on Sakaimachi — Hokkaido\'s most beloved confectioner',
                '📸 The street itself is lined with snow-laden ornamental street lamps',
              ],
            },
            {
              title: 'LeTAO Patisserie — The Famous Hokkaido Cheesecake',
              description: "LeTAO's double fromage — a featherlight duet of cream cheese and Camembert baked into a cloud of a cake — is one of Hokkaido's most beloved sweet exports. Eat it fresh at the Otaru flagship with a view from the second-floor balcony.",
              details: [
                '🍰 Double Fromage cheesecake: ¥1,940 (whole) or ¥540 slice at café',
                '📍 LeTAO flagship: Sakaimachi street, two floors',
                '☕ Pair with a Hokkaido milk tea or matcha latte',
              ],
            },
          ],
          meals: [
            {
              type: '🍣 Lunch',
              name: 'Masazushi or Canal-side Sushi',
              description: "Otaru is Hokkaido's seafood capital — fresh uni (sea urchin), ikura (salmon roe) and snow crab are served at sushi restaurants that have been operating for decades. Masazushi on Hanazono-dori is a local institution.",
              meta: '💰 ¥2,000–4,000 pp · 📍 Masazushi, Otaru city centre · Cash recommended',
            },
          ],
        },
        {
          label: 'Evening',
          activities: [
            {
              title: '🏮 MUST DO: Otaru Canal at Dusk (Gas Lamps)',
              description: "Return to the canal at 4:30 PM and wait for this. As the winter sun drops, the 167 gas lamps that line the canal path flicker on one by one. The warehouses glow amber, the steam from nearby restaurants drifts across the water, and the whole scene becomes something from another dimension. This is your Spirited Away bath house moment — take your time, soak it in, and shoot as many photos as you want.",
              details: [
                '⏰ Gas lamps turn on around 4:30–5:00 PM in March — arrive by 4:15 PM',
                '📸 Long-exposure phone photos work beautifully with lamp reflections on water',
                '❄️ On snowy evenings, snowflakes caught in the lamp light = magic',
                '🧣 Dress warmly — you\'ll want to linger for at least 30–45 minutes',
                '📍 Walk the full length of the canal once in each direction',
              ],
            },
            {
              title: 'Return to Sapporo by JR',
              description: "Board the JR train back to Sapporo fully enchanted. The journey home through the evening feels appropriately dreamy.",
              details: [
                '🚉 JR Otaru → Sapporo: 35 min, last trains run until ~11 PM',
                '🍜 Late-night ramen back in Susukino is an excellent coda to the day',
              ],
            },
          ],
          tips: [
            {
              type: 'tip',
              text: "If you love the Otaru vibe, consider coming back for a second evening visit. Otaru is only 35 min away and transforms completely after dark.",
            },
          ],
        },
      ],
      mapPins: [
        { lat: 43.1923, lng: 141.0039, label: 'Otaru Canal', num: 1, cat: 'attraction', desc: 'THE Spirited Away canal — 1.3km of stone warehouses & 167 gas lamps' },
        { lat: 43.1832, lng: 141.0048, label: 'Otaru Station', num: 2, cat: 'attraction', desc: 'JR station — walk south 10 min to reach the canal' },
        { lat: 43.1859, lng: 141.0044, label: 'Sakaimachi Street', num: 3, cat: 'attraction', desc: 'Main artisan street — Kitaichi Glass, music box museum, sweets' },
        { lat: 43.1872, lng: 141.0033, label: 'Otaru Music Box Museum (Orgel-do)', num: 4, cat: 'attraction', desc: '3,000+ music boxes, custom orders — chiming, enchanting' },
        { lat: 43.1865, lng: 141.0086, label: 'LeTAO Patisserie', num: 5, cat: 'food', desc: 'Hokkaido\'s legendary double fromage cheesecake — eat fresh here' },
        { lat: 43.1900, lng: 141.0030, label: 'Masazushi Restaurant', num: 6, cat: 'food', desc: 'Otaru seafood sushi institution — uni, ikura, fresh crab' },
      ],
    },

    {
      num: 6,
      date: '2026-03-24',
      neighborhoods: 'Lake Shikotsu · Chitose · Sapporo',
      title: 'Lake Shikotsu — Japan\'s Clearest Lake & Final Susukino Night',
      description: "Lake Shikotsu is one of Japan's deepest and clearest lakes — its water an impossible blue-green that doesn't freeze even in the coldest winters. Surrounded by snow-dusted volcanic mountains and wrapped in near-total silence, it's the most ethereally beautiful place in Hokkaido. It's a meditative counterpoint to city life, and the perfect penultimate day before the flight home. Tonight: final Susukino send-off.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Getting to Lake Shikotsu (via Chitose)',
              description: "Lake Shikotsu doesn't have a direct bus from Sapporo anymore, but the route via Chitose Station is straightforward.",
              details: [
                '🚉 Sapporo Station → JR to Chitose Station (35 min, ¥1,070)',
                '🚌 Hokkaido Chuo Bus: Chitose Station → Shikotsuko Kohan (45 min, ¥1,140)',
                '⏰ Depart Sapporo by 8:30 AM to arrive at the lake by 10:30 AM',
                '🔄 Return: last bus from Shikotsuko Kohan around 5:30 PM (check seasonal schedule)',
              ],
            },
            {
              title: 'Lake Shikotsu Shoreline Walk',
              description: "Arrive at Shikotsuko Kohan (the lake village) and walk to the water's edge. Lake Shikotsu has water clarity so extreme it looks artificially dyed — a deep blue-green that shifts as the light changes. The surrounding mountains (Mt. Tarumae, Mt. Eniwa, Mt. Fuppushi) are snow-covered and perfectly reflected in the water.",
              details: [
                '💎 Lake Shikotsu has water transparency measured at 21+ metres — one of Japan\'s clearest',
                '📸 Best angle: stand at the lakeside pier looking south towards Mt. Tarumae',
                '🌋 Mt. Tarumae (1,041m): active volcano visible from the lake, steaming gently',
                '🦢 White-tailed eagles and winter waterfowl on the lake in March',
              ],
            },
          ],
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shikotsu Lake Visitor Center & Nature Walk',
              description: "The Shikotsu Lake Visitor Center (free entry) explains the lake's volcanic formation and the extraordinary ecosystem it supports. Then lace up and walk the lakeside path — on a quiet winter weekday, you might have the entire trail to yourself.",
              details: [
                '🏛️ Visitor Center: free admission, excellent displays on the volcanic geology',
                '🥾 Lakeside trail: 2–4km flat walk with continuous lake views',
                '❄️ In late March, snow is still on the trails — bring waterproof boots',
                '♨️ Marukoma Onsen (accessible by lakeside path or taxi, 30 min walk): outdoor hot spring overlooking the lake — extraordinary if you have time',
              ],
            },
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Lakeside Restaurant at Shikotsuko Kohan',
              description: "The small village has a handful of restaurants serving simple, hearty Hokkaido fare — venison curry, lake-smelt (wakasagi) tempura, and hot ramen. Eat with the lake in view.",
              meta: '💰 ¥1,000–1,800 · 📍 Shikotsuko Kohan village near bus stop',
            },
          ],
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Sapporo',
              description: "Take the bus back to Chitose and the JR train to Sapporo. Arrive back in the early evening with plenty of time for a final Susukino celebration.",
              details: [
                '🚌 Bus: Shikotsuko Kohan → Chitose Station (~5 PM departure)',
                '🚉 JR: Chitose → Sapporo Station (35 min)',
                '⏰ Back in Sapporo by 6:30 PM',
              ],
            },
            {
              title: '🎉 Final Night in Susukino',
              description: "Your last night in Sapporo calls for a proper celebration. Do it right — a sit-down crab dinner, drinks at a jazz bar, and a late-night bowl of ramen before calling it a trip.",
              details: [
                '🦀 Kani-honke or Kani-doraku: premium Hokkaido hairy crab (kegani) dinner — splurge-worthy farewell',
                '🎷 Jazz club: Sapporo Jazz Spot Crawdaddy Club or Bar El Bohio for live music',
                '🍜 Midnight ramen send-off at Ramen Yokocho (until 2AM) — go full circle from Day 1',
                '📸 Susukino\'s neon signs at night are spectacular — get your group shot under the lights',
              ],
            },
          ],
          meals: [
            {
              type: '🦀 Dinner',
              name: 'Kani-honke (Crab Kaiseki)',
              description: "Hokkaido's premium crab restaurant — hairy crab (kegani) steamed and served in multiple preparations. A special farewell dinner that showcases the finest Hokkaido seafood.",
              meta: '💰 ¥5,000–8,000 pp · 📍 Susukino/city centre location · Reserve ahead',
            },
          ],
          tips: [
            {
              type: 'tip',
              text: "If a crab kaiseki is outside the budget, hit Nijo Market area around 6 PM — several standing seafood bars serve fresh hairy crab and uni rice for ¥2,000–3,000.",
            },
          ],
        },
      ],
      mapPins: [
        { lat: 42.7741, lng: 141.3572, label: 'Lake Shikotsu (Shikotsuko)', num: 1, cat: 'attraction', desc: 'Japan\'s clearest lake — impossible blue-green, volcanic mountains, total silence' },
        { lat: 42.7716, lng: 141.3559, label: 'Shikotsu Visitor Center', num: 2, cat: 'attraction', desc: 'Free museum about lake geology and ecosystem — worth a visit' },
        { lat: 42.7832, lng: 141.3228, label: 'Mt. Tarumae (view from lake)', num: 3, cat: 'attraction', desc: 'Active steaming volcano — reflected in Lake Shikotsu on clear days' },
        { lat: 42.8310, lng: 141.6507, label: 'JR Chitose Station (transit hub)', num: 4, cat: 'attraction', desc: 'Transfer point — buses to Lake Shikotsu depart from here' },
        { lat: 43.0590, lng: 141.3560, label: 'Kani-honke (Crab Restaurant)', num: 5, cat: 'food', desc: 'Premium Hokkaido crab kaiseki — the farewell dinner' },
      ],
    },

    {
      num: 7,
      date: '2026-03-25',
      neighborhoods: 'Sapporo City · Nijo Market · Sapporo Station',
      title: 'Departure Morning — Market Breakfast & Flight to Seoul',
      description: "Your flight back to Seoul departs at 3:55 PM, so you have a leisurely morning in the city. Use it well: a seafood breakfast at the historic Nijo Market, a final wander through the Sapporo underground shopping mall for last-minute Hokkaido souvenirs, and a smooth JR Airport Express ride to see you off in style.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Odori Park at Dawn (Optional)',
              description: "If you\'re up early, Odori Park at first light with fresh snow and zero people is an extraordinary sight. The TV Tower glows gold against the morning sky. A 20-minute wander before breakfast.",
              details: [
                '⏰ Best: 6:30–7:30 AM before the city fully wakes up',
                '📸 TV Tower with empty park and morning light — a quiet, beautiful goodbye',
              ],
            },
            {
              title: 'Nijo Market (Nijo Ichiba) — Seafood Breakfast',
              description: "Nijo Market is one of Sapporo's oldest markets — a covered street of 60+ stalls selling fresh Hokkaido seafood, vegetables and produce. Here you can have the ultimate Hokkaido breakfast: a bowl of fresh sea urchin (uni) rice, salmon roe (ikura) rice, or a steaming hairy crab miso soup. Atmospheric, delicious, and deeply local.",
              details: [
                '📍 Nijo Market: near Susukino, 5 min walk from Odori Park',
                '⏰ Open from 6 AM — best early when produce is freshest',
                '🦞 Try: kaisendon (seafood rice bowl) with fresh morning uni or ikura — ¥1,500–3,000',
                '☕ Several small cafés in the market serve Hokkaido milk coffee and fresh bread',
              ],
            },
          ],
          meals: [
            {
              type: '🍱 Breakfast',
              name: 'Nijo Market Kaisendon',
              description: "A bowl of fresh Hokkaido seafood rice — uni, ikura, crab or scallop — at one of the market stalls. The freshest, most indulgent breakfast possible.",
              meta: '💰 ¥1,500–3,000 · 📍 Nijo Market, near Susukino · Open from 6 AM',
            },
          ],
        },
        {
          label: 'Late Morning',
          activities: [
            {
              title: 'Souvenir Shopping at Sapporo Station Underground',
              description: "Sapporo Station and its underground shopping complex (Paseo, ESTA, Aurora Town) are the best places in all of Hokkaido to buy souvenirs. Everything is here and you can check-in your bags later.",
              details: [
                '🍪 Shiroi Koibito (white lover cookies) — the most famous Hokkaido souvenir',
                '🍫 Royce Chocolate (original Hokkaido brand) — nama chocolate especially',
                '🐄 Hokkaido dairy products: fresh butter, cheese and milk candy',
                '🍬 Jaga Pokkuru (Calbee Hokkaido potato snacks) — hard to find outside Hokkaido',
                '⏰ Shops open from 10 AM — allow 45–60 minutes for souvenir shopping',
              ],
            },
            {
              title: 'Airport Transfer: JR Airport Express',
              description: "Catch the JR Rapid Airport train from Sapporo Station directly to Shin-Chitose Airport. Fast, frequent, no stress.",
              details: [
                '🚉 JR Rapid Airport: Sapporo Station → Shin-Chitose Airport (37 min, ¥1,150)',
                '✈️ Flight at 3:55 PM → check-in by 1:45 PM → leave hotel by 12:00 PM',
                '⏰ Catch the 12:00–12:15 PM train to arrive airport by ~12:52 PM',
                '🛃 International departure: 2F, main terminal',
              ],
            },
          ],
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: '✈️ Flight to Seoul — See You Next Time, Hokkaido',
              description: "Board your flight back to Seoul, hearts full of powder snow, gas-lamp glows, Olympic ice, and the clearest blue lake you've ever seen. Hokkaido has a way of getting into the soul.",
              details: [
                '✈️ Flight: 3:55 PM from Shin-Chitose Airport (CTS) to Seoul',
                '🧳 Keep Hokkaido snacks in your carry-on to share at home',
                '💭 Already planning the next trip? Sapporo\'s cherry blossom season is May — just saying.',
              ],
            },
          ],
        },
      ],
      mapPins: [
        { lat: 43.0587, lng: 141.3591, label: 'Nijo Market (Nijo Ichiba)', num: 1, cat: 'food', desc: 'Historic covered seafood market — fresh uni, ikura and crab for breakfast' },
        { lat: 43.0598, lng: 141.3526, label: 'Odori Park (morning walk)', num: 2, cat: 'attraction', desc: 'Beautiful at dawn — TV Tower gold light, zero crowds, quiet goodbye' },
        { lat: 43.0683, lng: 141.3507, label: 'Sapporo Station (souvenirs + JR)', num: 3, cat: 'attraction', desc: 'Underground mall for Shiroi Koibito, Royce Chocolate — then JR to airport' },
        { lat: 42.7752, lng: 141.6921, label: 'Shin-Chitose Airport (CTS)', num: 4, cat: 'attraction', desc: 'JR Rapid Airport from Sapporo Station (37 min) — international departures 2F' },
      ],
    },
  ],

  budgetTable: [
    { category: 'Accommodation (per room)', budget: '¥8,000–12,000/night', midrange: '¥12,000–20,000/night', luxury: '¥20,000–50,000/night' },
    { category: 'Meals (per person)', budget: '¥2,000–3,500/day', midrange: '¥3,500–6,000/day', luxury: '¥6,000–15,000/day' },
    { category: 'Local Transit', budget: '¥500–1,000/day', midrange: '¥1,000–2,000/day', luxury: '¥2,000–5,000/day (taxi)' },
    { category: 'Ski Day (Teine)', budget: '¥8,000 lift+rental', midrange: '¥10,000–12,000', luxury: '¥15,000+ (lesson)' },
    { category: 'Ice Skating (Makomanai)', budget: '¥1,000–1,500 pp', midrange: '¥1,500', luxury: '¥1,500' },
    { category: 'Otaru Day Trip', budget: '¥1,280 train+spend', midrange: '¥4,000–6,000', luxury: '¥8,000+' },
    { category: '7-Day Estimate (per person)', budget: '¥80,000–120,000', midrange: '¥120,000–200,000', luxury: '¥200,000+' },
  ],

  practicalInfo: [
    {
      title: '✈️ Getting There & Away',
      items: [
        'Arriving: New Chitose Airport (CTS) → JR Rapid Airport → Sapporo Station (37 min, ¥1,150)',
        'Departing: Same route in reverse — allow 2.5 hours before flight for international departure',
        'Your flight: Seoul at 3:55 PM — leave Sapporo by noon at the latest',
        'IC card (Kitaca/Suica): buy at Sapporo Station, covers all subway, bus and JR',
      ],
    },
    {
      title: '🏨 Where to Stay',
      items: [
        'Cross Hotel Sapporo — stylish, central, walking distance from Susukino and Odori',
        'JR Inn Sapporo — great value, attached to Sapporo Station',
        'Mitsui Garden Hotel Sapporo — clean, well-located near Odori',
        'Stay in Susukino/Odori area for best walkability to nightlife and subway',
      ],
    },
    {
      title: '🌡️ March Weather',
      items: [
        'Sapporo late March: -2°C to 5°C — still proper winter with snow on the ground',
        'Snow is likely for all 7 days — pack full winter gear (waterproof layers essential)',
        'Takino Park and Lake Shikotsu will be snowy and cold — dress in layers',
        'By late March, daylight extends to around 6 PM — good for late afternoon shots',
      ],
    },
    {
      title: '💳 Money & Payments',
      items: [
        'Japan is still largely cash-based — carry ¥5,000–10,000 in cash daily',
        '7-Eleven, FamilyMart and Lawson ATMs accept international cards 24/7',
        'Convenience stores (konbini) are lifesavers — hot food, snacks, cash, umbrellas',
        'Tipping is NOT customary in Japan — attempting it can cause embarrassment',
      ],
    },
    {
      title: '📱 Connectivity',
      items: [
        'Buy a pocket WiFi at Chitose Airport or pre-order an eSIM (IIJmio, Ubigi, Airalo)',
        'Google Maps works offline — download the Sapporo region before arrival',
        'HyperDia app: most reliable for Japanese train/bus schedules',
        'Google Translate camera mode: photograph menus, signs — works brilliantly in Japan',
      ],
    },
  ],
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('\n✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('\n❌ Error:', err.message);
  process.exit(1);
}
