const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1772625956315_u924ah",
  email: "galaxycats510@gmail.com",
  destination: "Sapporo, Hokkaido, Japan",
  start_date: "2026-03-19",
  end_date: "2026-03-25",
  group_size: "3-4",
  travel_style: "Adventure, Cultural, Relaxation, Nightlife",
  dining: "Casual throughout",
  budget: "Surprise me",
  requests: "skiing, snow activities, day trips, beautiful lake scenery similar to Kamikochi, onsen, Ghibli/Spirited Away vibes, photography spots, fun nightlife (Susukino)",
  amount: "0.00",
  timestamp: "2026-03-04T12:05:56.315Z",
  status: "pending"
};

const itineraryData = {
  destination: "Sapporo & Hokkaido",
  countryEmoji: "🇯🇵",
  title: "6 Nights in Sapporo & Hokkaido: Snow, Lakes & Spirited Away Vibes",
  subtitle: "Skiing → Frozen Lakes → Ghibli-esque Canal Towns → Onsen → Susukino Nightlife",
  description: "A winter wonderland week in Japan's northernmost island — where powder snow blankets volcanic mountains, crystalline caldera lakes rival the beauty of Kamikochi, and snow-dusted canal towns look straight out of a Studio Ghibli film. March in Hokkaido is late-season magic: the ski slopes are still covered in legendary Japanese powder, the frozen lakes are thawing into surreal blue-green mirrors, and the onsen (hot springs) hit different when snowflakes melt on your face. Base yourself in Sapporo and radiate outward — skiing at Teine, a Ghibli-perfect day in Otaru, volcanic Lake Shikotsu, the resort shores of Lake Toya, and the neon-soaked nightlife of Susukino. This is Hokkaido at its most cinematic.",
  duration: "6 nights / 7 days",
  dates: "Mar 19 – 25, 2026",
  budget: "Flexible — Hokkaido is well-priced for Japan, especially for food and onsen",
  pace: "Balanced — active adventure days mixed with relaxation and nightlife",
  bestFor: "Groups of friends seeking adventure, culture, stunning scenery & fun nights out",
  highlights: [
    "Sapporo Teine — Olympic-level skiing with panoramic views of the city and ocean",
    "Otaru Canal — snow-dusted stone warehouses and gas lamps straight from Spirited Away",
    "Lake Shikotsu — Japan's second-deepest caldera lake with Kamikochi-like clarity",
    "Lake Toya — volcanic lakeside scenery, onsen resorts, and Mt. Usu views",
    "Jōzankei Onsen — forested hot spring valley 40 minutes from downtown Sapporo",
    "Susukino — Japan's northernmost (and wildest) entertainment district",
    "Hokkaido seafood — the freshest crab, uni, ikura, and sashimi in all of Japan",
    "Shiroi Koibito Park — a fairytale chocolate factory in the snow",
    "Hokkaido University — snow-covered ginkgo-lined campus, perfect for winter photography",
    "Miso ramen — Sapporo invented it, and you'll taste the original"
  ],
  essentials: [
    { title: "✈️ Getting There", text: "New Chitose Airport (CTS) is Hokkaido's main gateway — direct flights from Tokyo (1h45m), Osaka, and several international cities. Airport to Sapporo Station is 37 minutes by JR Rapid Airport train (¥1,150). The train runs every 15 minutes and is by far the most convenient option. Taxis to the city are ¥10,000+." },
    { title: "🚃 Getting Around", text: "Sapporo has excellent public transit — subway (3 lines), buses, and streetcar. For day trips, rent a car (highly recommended for Lake Shikotsu/Toya — roads are well-maintained and winter-ready) or take JR trains. A Sapporo subway day pass is ¥830. IC cards (Kitaca/Suica) work everywhere. For skiing, resort shuttle buses run from Sapporo Station." },
    { title: "💵 Budget Reality", text: "Hokkaido is one of Japan's most affordable regions. Ramen: ¥800-1,200 ($5-8). Izakaya dinner with drinks: ¥3,000-5,000pp ($20-33). Onsen day pass: ¥800-2,000 ($5-13). Ski lift ticket: ¥5,000-7,000 ($33-46). Hotel (3-4 star): ¥8,000-15,000/night ($53-100). The seafood-to-price ratio is absurd — world-class sushi for ¥2,500 ($17). 'Surprise me' budget means you can do everything and eat like royalty." },
    { title: "❄️ March Weather", text: "Late winter in Sapporo: highs around 3-7°C (37-45°F), lows around -3°C (27°F). Still snowy — average 30cm of snow remains on the ground. Ski resorts have excellent late-season coverage. Days are getting longer (sunrise ~5:50am, sunset ~5:50pm). Pack warm layers, waterproof boots, and hand warmers. The dry cold is manageable with proper layering." },
    { title: "🏨 Where to Stay", text: "Sapporo Station area for transit convenience and day trips. Susukino area for nightlife access and food (walkable to everything). Odori area splits the difference — central, near the park, subway access. For groups of 3-4, look at Airbnb apartments or hotel suites — Japanese business hotels are typically tiny singles." },
    { title: "🍜 Food Rules", text: "Hokkaido is Japan's food paradise. The cold climate produces incredible dairy, seafood, and produce. Must-try: miso ramen (Sapporo's invention), soup curry (another Sapporo original), Genghis Khan (grilled lamb), kaisendon (seafood rice bowl), crab (taraba, zuwaigani, kegani — all three species), uni (sea urchin), Yubari melon, Shiroi Koibito cookies, and Hokkaido milk soft serve." },
    { title: "📱 Essentials", text: "Get a Suica/Kitaca IC card at the airport for all transit. Pocket WiFi or eSIM from the airport (¥1,000/day for pocket WiFi). Google Maps works perfectly for transit. Download Google Translate for camera mode (Japanese menus). Most restaurants accept cash only — carry ¥10,000-20,000 at all times. Convenience stores (7-Eleven, Lawson, Seicomart) are lifelines — ATMs, hot food, drinks, and snacks 24/7." }
  ],
  days: [
    {
      num: 1,
      title: "Arrival in Sapporo — Ramen & Susukino",
      neighborhoods: "Sapporo Station · Susukino",
      date: "Mar 19",
      mapPins: [
        { lat: 43.0686, lng: 141.3508, label: "New Chitose Airport", num: 1, cat: "activity", desc: "Hokkaido's main airport" },
        { lat: 43.0687, lng: 141.3508, label: "Sapporo Station", num: 2, cat: "activity", desc: "City center transit hub" },
        { lat: 43.0557, lng: 141.3530, label: "Ramen Alley (Ramen Yokochō)", num: 3, cat: "food", desc: "17 ramen shops in one alley since 1951" },
        { lat: 43.0541, lng: 141.3530, label: "Susukino Entertainment District", num: 4, cat: "activity", desc: "Hokkaido's neon-lit nightlife hub" },
        { lat: 43.0603, lng: 141.3541, label: "Tanukikōji Shopping Arcade", num: 5, cat: "activity", desc: "Covered 1km shopping street" }
      ],
      timeBlocks: [
        {
          label: "Afternoon",
          activities: [
            { title: "Arrive & Settle In", description: "Land at New Chitose Airport and take the JR Rapid Airport train to Sapporo Station (37 minutes, runs every 15 min). Check into your hotel and get oriented. Sapporo is a grid city — easy to navigate, with wide streets designed for snow removal. The cold air hits different after Tokyo — crisp, clean, and smelling of snow. Welcome to Hokkaido.", details: ["📍 JR Rapid Airport → Sapporo Station · ¥1,150 · 37 minutes", "💡 Pick up Kitaca IC cards at the airport for seamless subway/bus/train travel. Load ¥3,000 each to start."] },
            { title: "Tanukikōji Shopping Arcade", description: "Walk through Tanukikōji — a 1km covered shopping arcade that's been Sapporo's main shopping street since 1873. In winter, the covered roof makes it the perfect warm walking route. Browse shops, duck into a Seicomart (Hokkaido's beloved convenience store chain — better than 7-Eleven, locals will fight you on this), and grab Hokkaido milk soft serve from a street vendor.", details: ["📍 Tanukikōji · Free · Runs east-west between Susukino and Ōdōri"] }
          ],
          meals: [
            { type: "🍽️ Late Lunch", name: "Ramen Yokochō (Ramen Alley)", description: "Your first meal in Sapporo MUST be miso ramen — the city literally invented it. Ramen Yokochō is a narrow alley in Susukino with 17 tiny ramen shops, open since 1951. Each seats 8-10 people. The miso ramen here is rich, buttery, and loaded with corn, bean sprouts, and chashu pork. The broth is thick enough to coat your soul. Try Ganso Ramen Yokochō Ramen or Hakusen for the classic experience.", meta: "¥900-1,200 ($6-8) · Minami 5 Nishi 3 · Walk in, expect a short queue" }
          ],
          tips: [{ type: "reddit", text: "Sapporo miso ramen is NOT the same as what you get outside Hokkaido. The local version uses a rich pork/chicken bone broth blended with red or white miso, finished with butter and sweetcorn. It's heavier, warmer, and designed to fight Hokkaido winters. You need this.", cite: "r/JapanTravel" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Susukino Night Walk & Nikka Sign", description: "Welcome to Susukino — Japan's northernmost major entertainment district and one of Asia's great nightlife neighborhoods. Over 4,000 bars, restaurants, clubs, and izakayas packed into a neon-drenched grid. Start with the iconic Nikka Whisky sign — a glowing bearded man that's become Sapporo's unofficial symbol. The streets buzz with energy even in the cold — izakaya lanterns glow orange through frosted windows, yakitori smoke drifts between buildings, and laughter echoes off snow-packed sidewalks.", details: ["📍 The Nikka sign is on Susukino Crossing (Minami 4 Nishi 3) — best photo angle from across the intersection", "💡 Susukino is very safe — Japan in general has extremely low crime. The biggest danger is spending too much on whisky."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Daruma Genghis Khan", description: "Genghis Khan (ジンギスカン, jingisukan) is Hokkaido's signature grilled lamb dish — named after the Mongolian emperor and cooked on a helmet-shaped dome grill. Daruma is the most famous spot in Sapporo — a tiny, smoky joint where you grill tender lamb yourself over charcoal. The meat is marinated in a secret sauce and grilled with onions, peppers, and bean sprouts. Your clothes will smell like smoke for days and you won't care.", meta: "¥1,500-2,500pp ($10-17) · Minami 5 Nishi 4 · Always a queue — go early (5pm) or late (9pm)" }
          ],
          tips: [{ type: "reddit", text: "Daruma has multiple branches in Susukino — the original (4.4 branch) has the most atmosphere but the longest lines. The 6.4 branch is the same food with shorter waits. Pro tip: the all-you-can-eat lamb option is insane value if you're hungry.", cite: "r/JapanTravel" }]
        }
      ]
    },
    {
      num: 2,
      title: "Skiing at Sapporo Teine",
      neighborhoods: "Teine Ski Resort · Sapporo",
      date: "Mar 20",
      mapPins: [
        { lat: 43.1095, lng: 141.2230, label: "Sapporo Teine Highland", num: 1, cat: "activity", desc: "1972 Olympics ski venue with ocean views" },
        { lat: 43.1050, lng: 141.2280, label: "Teine Olympia Zone", num: 2, cat: "activity", desc: "Beginner-friendly slopes" },
        { lat: 43.0557, lng: 141.3530, label: "Susukino", num: 3, cat: "food", desc: "Post-ski dinner district" },
        { lat: 43.0625, lng: 141.3543, label: "Ōdōri Park", num: 4, cat: "activity", desc: "City center park and TV Tower" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Sapporo Teine — Skiing & Snowboarding", description: "Just 40 minutes from downtown Sapporo, Teine is where the 1972 Winter Olympics were held — and the snow is still Olympic-caliber. The Highland zone offers advanced terrain with stunning panoramic views: on a clear day you can see the Sea of Japan, Sapporo city below, and the surrounding Hokkaido mountains all at once. The Olympia zone is gentler — perfect for beginners or anyone who wants cruisy runs through the trees. March means the crowds thin out, lift lines are short, and the spring snow is soft and forgiving. Rental equipment is available on-site.", details: ["📍 Sapporo Teine · Bus from Teine Station (20 min) or drive (40 min from Sapporo Station)", "💡 Full-day lift ticket: ¥5,900 ($39). Rental package (skis/board + boots + poles): ~¥5,500 ($36). First lifts at 9am. The Highland gondola opens incredible above-treeline terrain.", "📍 Shuttle bus runs from Sapporo Station — check the Teine website for the schedule. Runs every 30-60 min."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Hotel Breakfast or Convenience Store", description: "Grab onigiri, hot canned coffee, and nikuman (steamed meat buns) from Seicomart or 7-Eleven before heading to the slopes. Japanese convenience store food is legitimately excellent — don't sleep on it.", meta: "¥500-800 ($3-5) · Any konbini" }
          ],
          tips: [{ type: "reddit", text: "Teine Highland has some seriously steep terrain that surprises people — the Women's Downhill run from the Olympics is genuinely challenging. But the Olympia side is super mellow. Great mountain for a mixed-ability group.", cite: "r/JapanTravel" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Après-Ski & Lodge Lunch", description: "Take a break at the Teine lodge for a hot bowl of curry rice or katsu — classic Japanese ski lodge food. The views from the Highland lodge terrace are breathtaking. Continue skiing until the lifts close (5pm for Highland, 9pm for Olympia night skiing if open) or head back to the city.", details: ["💡 Teine sometimes offers night skiing on the Olympia side — check ahead. Skiing under floodlights with Sapporo's city lights below is surreal."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Teine Lodge Curry Rice", description: "Classic Japanese ski lodge food — katsu curry rice, udon, ramen. Nothing fancy, everything satisfying after a morning on the mountain. The curry rice at Japanese ski resorts is an institution.", meta: "¥900-1,200 · Teine Highland or Olympia lodge" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Sapporo TV Tower & Night Views", description: "Head to Sapporo TV Tower at the east end of Ōdōri Park for panoramic night views. The 90-meter observation deck offers sweeping views of Sapporo's grid lit up in winter — the snowscape city is gorgeous after dark. On a clear night you can see all the way to the mountains.", details: ["📍 Sapporo TV Tower · ¥1,000 admission · Open until 10pm"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Soup Curry at Suage+", description: "Soup curry is Sapporo's OTHER signature dish — invented here in the 1970s. Unlike thick Japanese curry, soup curry is a light, spiced broth loaded with massive vegetables (whole potatoes, half-eggplants, lotus root), tender chicken leg, and served alongside a separate bowl of rice. Suage+ is one of the city's best — the broth is deeply aromatic with 20+ spices and herbs, and you choose your spice level (start at 3-5 unless you're a heat demon).", meta: "¥1,200-1,600 ($8-11) · Multiple locations · Walk-in, expect a wait at dinner" }
          ],
          tips: [{ type: "reddit", text: "Soup curry is a Sapporo invention that hasn't really spread to the rest of Japan. It's COMPLETELY different from regular Japanese curry — think Southeast Asian-influenced spice broth with Japanese ingredients. You'll either become obsessed or confused. Most people become obsessed.", cite: "r/JapanTravel" }]
        }
      ]
    },
    {
      num: 3,
      title: "Otaru — Ghibli Vibes & Canal Magic",
      neighborhoods: "Otaru Canal · Sakaimachi · Otaru Port",
      date: "Mar 21",
      mapPins: [
        { lat: 43.1971, lng: 140.9948, label: "Otaru Canal", num: 1, cat: "activity", desc: "Snow-dusted stone warehouses and gas lamps" },
        { lat: 43.1980, lng: 141.0020, label: "Sakaimachi Street", num: 2, cat: "activity", desc: "Glass workshops, music boxes, and sweets" },
        { lat: 43.1960, lng: 140.9830, label: "Otaru Music Box Museum", num: 3, cat: "activity", desc: "3,000+ music boxes in a Victorian building" },
        { lat: 43.2076, lng: 140.9904, label: "Sankaku Market", num: 4, cat: "food", desc: "Freshest seafood bowls in Hokkaido" },
        { lat: 43.1945, lng: 141.0050, label: "Kitaichi Glass", num: 5, cat: "activity", desc: "Historic glass workshops and oil lamp gallery" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Train to Otaru & Sankaku Market", description: "Take the JR train from Sapporo to Otaru — 35 minutes along the stunning coastline of Ishikari Bay. The train hugs the shore, passing through tunnels carved into seaside cliffs. Arriving in Otaru feels like stepping into another era. Head straight to Sankaku Market near the station — a covered fish market where vendors pile mountains of fresh crab legs, uni (sea urchin), ikura (salmon roe), and scallops. Get a kaisendon — a seafood rice bowl piled impossibly high with raw fish, uni, and ikura. This is Hokkaido seafood at its peak.", details: ["📍 JR Sapporo → Otaru · ¥750 · 35 minutes · Trains every 15-20 min", "💡 Sit on the LEFT side of the train for ocean views on the way to Otaru."] }
          ],
          meals: [
            { type: "🍽️ Brunch", name: "Sankaku Market Kaisendon", description: "Build-your-own seafood bowl at one of the market stalls. Choose from uni, ikura, crab, salmon, scallop, squid, tuna — they pile it on rice. The uni in Hokkaido is sweeter and creamier than anywhere else in Japan. The ikura pops in your mouth like little ocean pearls. This might be the best breakfast of your life.", meta: "¥2,000-3,500 ($13-23) · Otaru Sankaku Market · Walk-in, opens 8am" }
          ],
          tips: [{ type: "reddit", text: "Otaru seafood markets are legit — this isn't tourist-trap fish. Otaru is an active fishing port and the seafood comes off the boats that morning. The kaisendon (seafood bowls) here rival Tsukiji/Toyosu at half the price.", cite: "r/JapanTravel" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Otaru Canal — Spirited Away Vibes", description: "The Otaru Canal is why you're here. Stone warehouses from the 1920s line both banks, their dark slate walls dusted with snow. Gas lamps cast warm orange light over the still water. In March, snow still clings to the rooftops and icicles hang from the eaves. The reflection of the warehouses in the canal water — doubled, dreamlike, silent — is pure Studio Ghibli. Walk slowly. Take photographs. The canal is only 1.1km long but every angle is cinematic. The south section with the stone retaining walls is the most photogenic.", details: ["📍 Otaru Canal · Free · Always open · Best photos: late afternoon when gas lamps are lit", "💡 The canal at dusk (around 5pm in March) is the most magical — gas lamps turn on automatically and the sky turns deep blue behind the warehouses. The reflection shots are extraordinary."] },
            { title: "Sakaimachi Street & Glass Workshops", description: "Sakaimachi Street is Otaru's main attraction street — a charming avenue of converted warehouses now housing glass workshops, music box shops, candy stores, and cafés. Otaru's glass-blowing tradition dates to the herring fishing era when glass fishing floats were made here. Kitaichi Glass has a stunning gallery lit entirely by oil lamps — hundreds of them casting flickering warm light across handblown glass pieces. It feels like walking into a Ghibli scene. The Music Box Museum is another treasure — a Victorian-style building with 3,000+ music boxes, from tiny to room-sized mechanical orchestras.", details: ["📍 Sakaimachi Street · Free to walk · Kitaichi Glass open 9am-6pm · Music Box Museum ¥free (main hall)", "💡 You can make your own music box at the workshop (¥1,500-3,000, 30 min). A beautiful souvenir."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "LeTAO Double Fromage Cheesecake", description: "LeTAO is Otaru's famous patisserie — their double fromage cheesecake (half baked, half rare) is Hokkaido's most celebrated dessert. The top layer is creamy Italian mascarpone, the bottom is rich baked cheesecake made with Hokkaido milk. Eat it at the café or buy a whole cake to bring back. The Hokkaido dairy makes this taste completely different from any cheesecake you've had.", meta: "¥350/slice, ¥1,800/whole · Sakaimachi Street · Multiple locations" }
          ],
          tips: [{ type: "tip", text: "Otaru in winter genuinely looks like a Ghibli film — particularly Spirited Away's bathhouse town vibes. The warm lamplight against dark stone, the snow on slate roofs, the quiet canal reflections. If you love Ghibli aesthetics, this is the real-life version." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Otaru Canal at Dusk & Return", description: "Walk the canal one more time as the gas lamps light up and the sky turns deep indigo. The early evening is when the magic peaks — the warm lamp glow against the cold blue snow. Take your time, take your photos. Then catch the train back to Sapporo. The nighttime coastal train ride is beautiful too — moonlight on Ishikari Bay.", details: ["📍 Return trains run until ~11pm · Same 35-minute ride"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Naruto Wakadon (Otaru)", description: "Before heading back, try Otaru's famous half-fried chicken (zangi) at a local spot, or get fresh sushi at one of the canal-side restaurants. Otaru sushi is legendary — the port city's proximity to fishing boats means the fish is hours old. Tuna, salmon, uni, and hotate (scallop) sushi here is extraordinary.", meta: "¥2,500-4,000pp · Canal area or Sushi Street · Walk-in" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 4,
      title: "Lake Shikotsu — Kamikochi of the North",
      neighborhoods: "Lake Shikotsu · Shikotsu-Toya National Park",
      date: "Mar 22",
      mapPins: [
        { lat: 42.7586, lng: 141.3311, label: "Lake Shikotsu", num: 1, cat: "activity", desc: "Japan's 2nd deepest caldera lake — crystal blue" },
        { lat: 42.7620, lng: 141.3350, label: "Shikotsu Kohan Onsen", num: 2, cat: "activity", desc: "Lakeside hot springs village" },
        { lat: 42.7570, lng: 141.3260, label: "Lake Shikotsu Visitor Center", num: 3, cat: "activity", desc: "Nature exhibits and trailhead" },
        { lat: 42.7550, lng: 141.3400, label: "Marukoma Onsen", num: 4, cat: "activity", desc: "Lakeside rotenburo with mountain views" },
        { lat: 42.7700, lng: 141.3200, label: "Mt. Tarumae Trailhead", num: 5, cat: "activity", desc: "Active volcano with crater hike" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Drive to Lake Shikotsu", description: "Rent a car and drive south from Sapporo to Lake Shikotsu — about 1 hour through snowy Hokkaido forest. As you descend toward the lake, the first glimpse through the trees is jaw-dropping: an impossibly blue caldera lake surrounded by snow-covered volcanic mountains. Lake Shikotsu is Japan's second-deepest lake and holds the record for the clearest freshwater in Japan — in summer the visibility is 20+ meters. In March, the lake's edges may still have ice formations, and the water shifts between deep cobalt blue and emerald green depending on the light. This is the Kamikochi-level scenery you came for.", details: ["📍 Lake Shikotsu · ~60 min drive from Sapporo · Free parking at the lakeside village", "💡 Rent a car for today and tomorrow (Lake Toya). Toyota Rent a Car at Sapporo Station is convenient. ¥8,000-12,000/day ($53-80) including insurance. Roads are well-maintained but may require snow tires (included in winter rentals)."] },
            { title: "Lakeside Walk & Visitor Center", description: "Walk along the shore of Lake Shikotsu. The volcanic peaks of Mt. Tarumae, Mt. Eniwa, and Mt. Fuppushi frame the lake like a painting. The water is surreally clear — you can see the lake bed through blue-tinted water. The visitor center has excellent exhibits on the lake's volcanic geology and the surrounding wildlife (brown bears, Stellar's sea eagles, red foxes). In March, the late-winter light creates dramatic shadows across the snow-covered peaks.", details: ["📍 Lake Shikotsu Visitor Center · Free · Open 9am-5pm"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Seicomart Road Trip Provisions", description: "Load up at Seicomart before leaving Sapporo — onigiri, hot coffee, karaage (fried chicken), and Hokkaido milk. Seicomart's hot food section (Hot Chef) makes fresh bento, croquettes, and katsu sandwiches in-store. The Hokkaido melon cream bread is a must.", meta: "¥500-800pp · Any Seicomart" }
          ],
          tips: [{ type: "tip", text: "Lake Shikotsu is often called the 'Kamikochi of the North' — the same crystal-clear water surrounded by dramatic mountain scenery, but without the crowds. In March you might have the lakeshore practically to yourself." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Marukoma Onsen — Lakeside Hot Spring", description: "The highlight: Marukoma Onsen ryokan has a legendary rotenburo (outdoor bath) literally at the lake's edge. Imagine soaking in steaming hot mineral water while staring at the frozen blue lake and snow-covered volcanic mountains. In March, snowflakes might drift onto your face while your body is submerged in 42°C water. The contrast between the hot water and cold air is sublime. Even if you're not staying overnight, you can visit for a day-use bath.", details: ["📍 Marukoma Onsen · Day-use bath: ¥1,000 ($7) · Open 10am-3pm for day visitors", "💡 The outdoor bath is mixed-gender with swimwear option, or separated indoor baths available. Towels can be rented. Follow onsen etiquette: shower first, no swimsuit in gender-separated baths, tie hair up, no photos in the bath area."] },
            { title: "Snow Activities & Photography", description: "After the onsen, explore more of the lakeshore. In March, there may still be remnants of the famous ice formations (hyōtō) along the shore — natural ice sculptures created by lake spray freezing on contact. Walk toward the quieter sections of the lake for stunning photography opportunities: the volcanic peaks reflected in the impossibly blue water, snow-laden birch trees, and the silence of Hokkaido's wilderness.", details: ["💡 If you're up for it, the trail toward Mt. Tarumae (active volcano) starts nearby. In March, snowshoes may be needed — check conditions at the visitor center."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Shikotsu Kohan Himemasu", description: "Lake Shikotsu's specialty is himemasu — a freshwater salmon unique to this lake. Served as sashimi, grilled, or in a set meal at the lakeside restaurants. The fish is delicate, sweet, and unlike anything you've had. Try it grilled with salt or as sashimi if available.", meta: "¥1,500-2,500 · Lakeside village restaurants · Seasonal, check availability" }
          ],
          tips: [{ type: "reddit", text: "Marukoma Onsen at Lake Shikotsu is one of the most scenic bathhouse experiences in Hokkaido. The rotenburo right at the water's edge with the mountains behind you is absolutely worth the trip. Go on a weekday for fewer people.", cite: "r/JapanTravel" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Return to Sapporo & Izakaya Night", description: "Drive back to Sapporo (1 hour). Tonight, dive into the izakaya scene. Japanese izakayas are the heart of nightlife — small, warm, lively bars serving drinks alongside small plates of food. In Sapporo, the food is next-level because Hokkaido ingredients are Japan's best.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Izakaya Row in Susukino", description: "Find a local izakaya in Susukino and order round after round: edamame, karaage (fried chicken), hokke (grilled Atka mackerel — a Hokkaido classic), potato butter (another Hokkaido staple), sashimi platter, and Sapporo Classic beer (the local brew, only available in Hokkaido). The vibe is warm, loud, and communal — perfect for a group of friends. If you see a tiny place with a noren curtain and steam coming out, go in.", meta: "¥3,000-5,000pp ($20-33) · Susukino area · Walk-in or reservation" }
          ],
          tips: [{ type: "reddit", text: "Sapporo Classic (beer) is only sold in Hokkaido — it's a different brew from regular Sapporo and locals are fiercely proud of it. It's smoother and slightly more malty. Order it everywhere.", cite: "r/JapanTravel" }]
        }
      ]
    },
    {
      num: 5,
      title: "Lake Toya & Noboribetsu Onsen",
      neighborhoods: "Lake Toya · Noboribetsu · Mt. Usu",
      date: "Mar 23",
      mapPins: [
        { lat: 42.6100, lng: 140.8500, label: "Lake Toya", num: 1, cat: "activity", desc: "Stunning caldera lake with island views" },
        { lat: 42.5440, lng: 140.8420, label: "Mt. Usu Ropeway", num: 2, cat: "activity", desc: "Active volcano with crater views" },
        { lat: 42.6150, lng: 140.8530, label: "Toya Onsen Town", num: 3, cat: "activity", desc: "Lakeside hot spring resort town" },
        { lat: 42.4940, lng: 141.1580, label: "Noboribetsu Jigokudani", num: 4, cat: "activity", desc: "Hell Valley — steaming volcanic vents" },
        { lat: 42.4960, lng: 141.1550, label: "Noboribetsu Onsen", num: 5, cat: "activity", desc: "Hokkaido's most famous hot spring town" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Drive to Lake Toya", description: "Drive southwest from Sapporo to Lake Toya — about 2 hours through Hokkaido's volcanic landscape. Lake Toya is a massive caldera lake (11km across) with a forested island in the center — Nakajima — which looks like it floats on the water. The lake never freezes even in winter, earning it the nickname 'the lake that never sleeps.' The scenery is dramatic: the active volcano Mt. Usu looms over the south shore, Showa Shinzan (a lava dome that literally rose out of a wheat field in 1944) steams nearby, and the snow-covered Hokkaido mountains frame everything. This is cinematic, otherworldly landscape.", details: ["📍 Lake Toya · ~2 hours from Sapporo by car · Free parking at the onsen town", "💡 The drive via Route 230 through Nakayama Pass is scenic — stop at the rest area for panoramic views of the mountains."] },
            { title: "Mt. Usu Ropeway", description: "Take the Mt. Usu Ropeway to the top of this active volcano (last eruption: 2000). From the summit observation deck, you'll see the devastation from the eruption — buildings buried under volcanic debris, roads cracked and swallowed — alongside the stunning beauty of Lake Toya and Nakajima island below. Walking trails lead to the Ginuma crater and panoramic viewpoints. The contrast between destruction and beauty is powerful.", details: ["📍 Mt. Usu Ropeway · ¥1,800 round trip · Open 9am-4:15pm (March)", "💡 The 2000 eruption walkthrough trail shows actual destroyed buildings and roads — left as-is for education. It's eerie and fascinating."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Roadside Rest Stop Breakfast", description: "Stop at Nakayama Pass rest area on the drive for fresh Hokkaido milk, melon pan, and hot corn soup from vending machines. The views from the rest area are spectacular — snow-covered peaks in every direction.", meta: "¥300-600 · Nakayama Pass rest area" }
          ],
          tips: [{ type: "tip", text: "Lake Toya hosted the 2008 G8 Summit — The Windsor Hotel Toya on the hilltop above the lake is where world leaders stayed. You can visit the lobby for incredible views even if you're not staying." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Toya Lakeside & Foot Baths", description: "Walk along the Lake Toya promenade — the lakeside path has free foot baths (ashiyu) at several points along the shore. Soak your feet in hot spring water while gazing at the lake, the island, and the mountains. Sculptures dot the shoreline — the Toya Lake Sculpture Park has 58 works by artists from around the world.", details: ["💡 Free ashiyu (foot baths) — no towel needed, just roll up your pants. Several locations along the promenade."] },
            { title: "Noboribetsu Jigokudani (Hell Valley)", description: "Drive 45 minutes east to Noboribetsu — Hokkaido's most famous hot spring town. Jigokudani (Hell Valley) is a volcanic crater valley where steam vents blast sulfurous clouds from orange and yellow earth, hot rivers flow between the rocks, and the smell of sulfur fills the air. In winter, the steam is even more dramatic against the snow. A well-maintained boardwalk lets you walk right through the valley. It feels like walking on another planet — or through a scene from Spirited Away's bathhouse underworld.", details: ["📍 Jigokudani · Free · Always open · Boardwalk ~800m", "💡 The large demon statue at the entrance is a classic photo spot. Noboribetsu's mascot is a red demon (oni)."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Toya Onsen Town Lunch", description: "The lakeside onsen town has several restaurants serving Hokkaido comfort food — try Hokkaido-style ramen (butter corn miso), curry rice, or a set meal with grilled fish. The lakeside views from the restaurant windows make everything taste better.", meta: "¥1,000-1,500 · Toya Onsen Town" }
          ],
          tips: [{ type: "reddit", text: "Noboribetsu's Hell Valley is genuinely impressive — the scale is bigger than photos suggest and the sulfur steam in winter is dramatic. The town itself has a fun demon theme — demon statues everywhere, demon-themed snacks, a demon parade street.", cite: "r/JapanTravel" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Noboribetsu Onsen Experience", description: "Before driving back, visit one of Noboribetsu's legendary bathhouses. Dai-ichi Takimotokan has one of Japan's largest public baths — 35 different pools fed by 7 different hot spring sources, each with different mineral content and temperature. Or try Sagiriyu, a smaller, more local public bath right in the center of town (¥480). The water comes directly from Hell Valley's volcanic vents — rich in sulfur, iron, and minerals. Your skin will feel like silk afterward.", details: ["📍 Dai-ichi Takimotokan · Day-use bath ¥2,250 · Open 9am-6pm for visitors", "📍 Sagiriyu Public Bath · ¥480 · Open 7am-9pm · Small, local, authentic"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Noboribetsu Onsen Street Dining", description: "The main street of Noboribetsu onsen town has casual eateries — try jigoku ramen (hell ramen, very spicy), steamed eggs cooked in the hot spring water, or enma yaki (demon-themed snacks). Then drive back to Sapporo (~90 minutes) with warm onsen skin and full bellies.", meta: "¥800-1,500 · Noboribetsu main street" }
          ],
          tips: [{ type: "tip", text: "Hot spring eggs (onsen tamago) in Noboribetsu are cooked by volcanic heat — the yolk is custard-soft, the white is barely set. Buy them from vendors near Hell Valley. ¥100-200 each." }]
        }
      ]
    },
    {
      num: 6,
      title: "Sapporo Cultural Day & Jōzankei Onsen",
      neighborhoods: "Sapporo City · Jōzankei · Shiroi Koibito Park",
      date: "Mar 24",
      mapPins: [
        { lat: 43.0814, lng: 141.3398, label: "Hokkaido University", num: 1, cat: "activity", desc: "Snow-covered campus and ginkgo avenue" },
        { lat: 43.0523, lng: 141.2913, label: "Shiroi Koibito Park", num: 2, cat: "activity", desc: "Chocolate factory theme park" },
        { lat: 42.9690, lng: 141.1650, label: "Jōzankei Onsen", num: 3, cat: "activity", desc: "Forest hot spring valley" },
        { lat: 43.0603, lng: 141.3464, label: "Nijo Market", num: 4, cat: "food", desc: "Fresh seafood market since 1903" },
        { lat: 43.0541, lng: 141.3530, label: "Susukino", num: 5, cat: "food", desc: "Final night out" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Nijo Market — Seafood Breakfast", description: "Start at Nijo Market — Sapporo's fresh seafood market operating since 1903. Wander through narrow stalls piled with king crab legs, scallops the size of your fist, glistening uni, and rows of grilled seafood on sticks. Get a kaisendon or eat grilled crab legs standing up. The vendors are lively, offering tastings and shouting their prices. In March, the winter crab season is at its peak — Hokkaido's three crab species (taraba/king, zuwaigani/snow, kegani/horsehair) are all in season.", details: ["📍 Nijo Market · Free to enter · Open 7am-6pm · Near Ōdōri", "💡 Horsehair crab (kegani) is Hokkaido's specialty — smaller than king crab but the meat is sweeter and more delicate. Try it at least once."] },
            { title: "Hokkaido University Campus Walk", description: "Walk through the beautiful Hokkaido University campus — one of Japan's oldest and most prestigious universities. In winter, the famous poplar-lined avenue and ginkgo avenue are covered in snow, creating ethereal white corridors. The campus is enormous, green (well, white in March), and free to explore. The original farm buildings from the 1870s are still standing. Clark's 'Boys, be ambitious!' statue is an icon.", details: ["📍 Hokkaido University · Free · Always open · 10 min walk from Sapporo Station", "💡 The Poplar Avenue (Poplar Namiki) is the most photographed spot — tall poplars creating a snow tunnel. Early morning light is best for photography."] }
          ],
          meals: [
            { type: "🍽️ Brunch", name: "Nijo Market Kaisendon", description: "A towering bowl of rice topped with fresh uni, ikura, crab, salmon, and scallop. The vendors will pile it impossibly high. Eat it at the standing counters inside the market, chopsticks in one hand, catching falling ikura with the other. This is Hokkaido in a bowl.", meta: "¥2,000-3,500 · Nijo Market stalls · Walk-in" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Shiroi Koibito Park", description: "Visit the Shiroi Koibito (White Lover) chocolate factory — Hokkaido's most famous souvenir cookie turned into a European fairytale theme park. The factory building looks like a Swiss chalet, surrounded by manicured gardens (snow-covered in March), a clock tower with mechanical dolls, and a miniature train. Inside, watch Shiroi Koibito cookies being made on the production line, learn about chocolate history, and decorate your own cookies. The Ghibli-loving photographer in your group will go wild — the whole complex is painfully photogenic.", details: ["📍 Shiroi Koibito Park · ¥800 admission · Open 10am-5pm · Subway to Miyanosawa then bus", "💡 Buy the fresh Shiroi Koibito cookies here — still warm from the line. They're different from the boxed ones. Also try their exclusive soft serve made with Hokkaido milk and white chocolate."] },
            { title: "Jōzankei Onsen — Forest Hot Spring", description: "Drive or bus 40 minutes south of Sapporo to Jōzankei — a forested hot spring valley tucked between mountains along the Toyohira River. This is Sapporo's onsen retreat: historic ryokan and hotels with outdoor baths overlooking the snow-covered gorge. Hōheikyo Onsen (a bit further up the valley) is a rustic, budget-friendly public bath with a massive outdoor stone pool surrounded by forest. Soaking in hot mineral water while snow covers the trees above — this is the quintessential Hokkaido onsen moment.", details: ["📍 Jōzankei Onsen · Bus from Sapporo Station (~75 min) or drive (~40 min)", "📍 Hōheikyo Onsen · ¥1,100 · Open 8am-9pm · Rustic outdoor bath in the forest", "💡 Jōzankei has free foot baths (ashiyu) along the riverside walkway. The Kappa statues throughout the town reference a local legend about water spirits."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Shiroi Koibito Park Café", description: "The park's café serves chocolate-themed desserts, parfaits, and drinks. Their white chocolate parfait with Hokkaido milk soft serve is decadent. A sweet lunch before the onsen.", meta: "¥800-1,500 · Shiroi Koibito Park" }
          ],
          tips: [{ type: "reddit", text: "Jōzankei is an underrated onsen compared to Noboribetsu — less touristy, more nature, easier to access from Sapporo. Hōheikyo Onsen in particular is a hidden gem — a massive outdoor stone bath in the middle of the forest. In winter with snow on the trees it's magical.", cite: "r/JapanTravel" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Final Night in Susukino", description: "Your last night in Sapporo — make it count. Return to Susukino for one final round. Hit a whisky bar (Sapporo has excellent ones — try Bar Yamazaki or Bar Keller for Japanese whisky flights), a karaoke box (Big Echo or Jankara — private rooms, unlimited drinks, sing until 5am), or a late-night ramen crawl. Susukino doesn't sleep — some bars stay open until dawn. The neon glow, the cold night air, the warmth of a tiny bar — this is Hokkaido nightlife at its finest.", details: ["💡 Karaoke in Japan is private rooms, not public singing. Perfect for groups. Most places offer nomihōdai (all-you-can-drink) packages for ¥1,500-2,500/person for 2 hours."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Sapporo Beer Garden (Kirin Beer En or Sapporo Beer Museum)", description: "For the final dinner, go big: the Sapporo Beer Garden in the historic red-brick Sapporo Beer Museum. All-you-can-eat Genghis Khan grilled lamb + all-you-can-drink Sapporo beer for ¥4,400 ($29) for 100 minutes. You grill the lamb yourself on dome-shaped grills while drinking unlimited fresh Sapporo beer in a massive hall that feels like a beer cathedral. It's loud, smoky, joyful, and peak Hokkaido.", meta: "¥4,400pp all-you-can-eat+drink (100 min) · Sapporo Beer Museum · Reservation recommended" }
          ],
          tips: [{ type: "reddit", text: "Sapporo Beer Garden all-you-can-eat Genghis Khan is one of the best value meals in Japan. ¥4,400 for unlimited lamb + unlimited beer in a gorgeous historic building. Book ahead — it fills up, especially on weekends.", cite: "r/JapanTravel" }]
        }
      ]
    },
    {
      num: 7,
      title: "Departure Day — Last Ramen & Goodbye",
      neighborhoods: "Sapporo Station · New Chitose Airport",
      date: "Mar 25",
      mapPins: [
        { lat: 43.0687, lng: 141.3508, label: "Sapporo Station", num: 1, cat: "food", desc: "Last-minute shopping and ramen" },
        { lat: 43.0603, lng: 141.3541, label: "Tanukikōji", num: 2, cat: "activity", desc: "Souvenir shopping" },
        { lat: 43.0686, lng: 141.3508, label: "New Chitose Airport", num: 3, cat: "activity", desc: "Departure" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Last Morning in Sapporo", description: "Depending on your flight time, squeeze in final experiences. Walk through Ōdōri Park one last time — the wide boulevard stretching from the TV Tower to the mountains is Sapporo's heartline. In March, the snow sculptures from the February festival are gone but the park is still beautifully snow-covered. Pick up last-minute souvenirs at Tanukikōji or the underground shopping malls beneath Sapporo Station — Royce' chocolate, Shiroi Koibito, Hokkaido melon Kit-Kats, and lavender products from Furano.", details: ["📍 Ōdōri Park · Free · Always open", "💡 New Chitose Airport has an incredible shopping area — Royce' Chocolate World (free factory tour + tasting), ramen street, seafood market, and more. Arrive 2+ hours early to shop and eat."] },
            { title: "New Chitose Airport", description: "Take the JR Rapid Airport train from Sapporo Station (37 min). New Chitose Airport is one of Japan's best — it has its own Royce' Chocolate World with a free factory tour, a ramen alley with Hokkaido's best shops, a Doraemon museum, a movie theater, and an onsen (yes, an airport onsen with runway views). Arrive early and make the airport part of the experience.", details: ["📍 JR Sapporo → New Chitose Airport · ¥1,150 · 37 min", "💡 The airport ramen street has excellent Hokkaido ramen — one last bowl for the road. The onsen (New Chitose Airport Onsen) is ¥1,500 and has runway views — soak before you fly."] }
          ],
          meals: [
            { type: "🍽️ Brunch", name: "One Last Miso Ramen", description: "End where you started — with a bowl of Sapporo miso ramen. At the airport's ramen alley or at your favorite spot in town. The rich miso broth, the butter, the corn, the perfectly chewy noodles. You'll dream about this ramen. Sapporo has earned its place in your heart — through your stomach.", meta: "¥900-1,200 · Airport ramen street or Sapporo city" }
          ],
          tips: [{ type: "tip", text: "また来るよ、札幌 — Mata kuru yo, Sapporo. I'll be back. 🇯🇵❄️" }]
        }
      ]
    }
  ],
  budgetTable: [
    { item: "Accommodation (6 nights, hotel/Airbnb for group)", low: "¥48,000", mid: "¥72,000", high: "¥120,000", notes: "Per room/unit — split 3-4 ways" },
    { item: "Transportation (airport + subway + day trips)", low: "¥8,000", mid: "¥15,000", high: "¥25,000", notes: "Per person, including car rental share" },
    { item: "Ski Day (lift + rental)", low: "¥8,000", mid: "¥11,500", high: "¥15,000", notes: "Per person, one day" },
    { item: "Food (per day)", low: "¥3,000", mid: "¥5,500", high: "¥10,000", notes: "Per person — Hokkaido is affordable" },
    { item: "Onsen (3 visits)", low: "¥1,500", mid: "¥3,500", high: "¥7,000", notes: "Per person — from ¥480 to ¥2,250 per visit" },
    { item: "Activities & Attractions", low: "¥3,000", mid: "¥6,000", high: "¥10,000", notes: "Per person — ropeway, museums, parks" },
    { item: "Nightlife & Drinks", low: "¥2,000", mid: "¥5,000", high: "¥12,000", notes: "Per person per night — izakaya, bars, karaoke" }
  ],
  practicalInfo: [
    { title: "🗣️ Language", items: ["English signage is limited outside Sapporo Station and tourist spots — Google Translate's camera mode is essential for menus and signs", "Most Japanese people are incredibly helpful even without shared language — point, gesture, and smile", "Learn a few words: arigatō (thank you), sumimasen (excuse me), oishii (delicious), kanpai (cheers)"] },
    { title: "💴 Cash is King", items: ["Many Sapporo restaurants, especially izakayas and ramen shops, are cash-only", "ATMs at 7-Eleven and Japan Post accept international cards — carry ¥20,000-30,000 ($130-200) at all times", "Credit cards work at hotels, department stores, and chain restaurants, but not at the best small places"] },
    { title: "♨️ Onsen Etiquette", items: ["Onsen are communal — most are gender-separated and require full nudity (no swimsuits)", "Shower thoroughly before entering — small towel goes on your head (not in the water)", "Tattoos: some onsen ban visible tattoos — call ahead or use private baths", "Don't splash or swim — be quiet and respectful. It's one of Japan's most beautiful traditions"] },
    { title: "🚗 Winter Driving", items: ["Hokkaido roads are well-maintained but snow-covered — rental cars come with studded/snow tires", "Drive slowly, brake gently, and watch for black ice — chains are rarely needed", "GPS in rental cars has English option — gas stations (full-service) are easy to find", "Drive on the LEFT"] },
    { title: "📷 Photography Tips", items: ["Hokkaido in March is a photographer's dream — white landscapes, blue lakes, warm orange city lights against snow", "Golden hour is around 5:30-6pm — Otaru Canal at dusk, Lake Shikotsu's blue water, Susukino's neon, Hokudai's snow corridors", "Bring extra batteries (cold drains them fast) and a waterproof bag"] }
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
