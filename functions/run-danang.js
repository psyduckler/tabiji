const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1771490222563_k6eut6",
  email: "biz@localhotels.com",
  destination: "Da Nang, Vietnam",
  start_date: "2026-02-19",
  end_date: "2026-03-14",
  group_size: "1",
  travel_style: "Cultural, Foodie, Relaxation",
  dining: "Casual throughout",
  budget: "Surprise me",
  requests: "",
  amount: "0.00",
  timestamp: "2026-02-19T08:37:02.563Z",
  status: "pending"
};

const itineraryData = {
  destination: "Da Nang & Central Vietnam",
  countryEmoji: "🇻🇳",
  title: "23 Nights in Central Vietnam: Da Nang, Hoi An & Huế",
  subtitle: "Beaches → Ancient Towns → Imperial Citadels → Mountain Temples → Street Food Heaven",
  description: "A solo deep-dive into Central Vietnam — the country's cultural and culinary heartland. Base yourself in Da Nang's beachfront energy, wander Hoi An's lantern-lit ancient streets, explore Huế's imperial grandeur, and eat your way through some of the best food on earth. February–March is dry season perfection: warm days, clear skies, and the South China Sea at its calmest. Three weeks means you can actually slow down and live here.",
  duration: "23 nights / 24 days",
  dates: "Feb 19 – Mar 14, 2026",
  budget: "Flexible — Vietnam is extraordinarily affordable",
  pace: "Slow and intentional — deep neighborhood exploration, long meals, beach days, spa afternoons",
  bestFor: "Solo cultural explorers, food obsessives & relaxation seekers",
  highlights: [
    "My Khe Beach — consistently ranked among Asia's finest beaches",
    "Hoi An Ancient Town — UNESCO lantern-lit streets, tailors & cooking classes",
    "Huế Imperial City — Vietnam's former capital and culinary capital",
    "Bà Nà Hills & Golden Bridge — iconic hilltop French village",
    "Marble Mountains — cave temples carved into limestone karst",
    "Mỹ Sơn Sanctuary — Champa kingdom Hindu temple ruins (UNESCO)",
    "Cù Lao Chàm — pristine island marine park off Hoi An",
    "Hai Van Pass — one of the world's most scenic coastal roads",
    "Bánh mì, bún bò Huế, mì Quảng, cao lầu — iconic Central Vietnamese dishes",
    "Vietnamese coffee culture — cà phê sữa đá perfection"
  ],
  essentials: [
    { title: "✈️ Getting There", text: "Da Nang International Airport (DAD) has direct flights from most Asian hubs. A taxi/Grab to the beach hotel area is 15 minutes (~80,000 VND / $3). The airport is incredibly close to the city center — one of Vietnam's most convenient airports." },
    { title: "🛵 Getting Around", text: "Grab (Southeast Asia's Uber) is the easiest option — bikes and cars available. A Grab bike across Da Nang costs $1-2. For Hoi An/Huế trips, hire a private driver ($40-60/day) or take local buses. Renting a motorbike ($5-7/day) is common but requires confidence in Vietnamese traffic. Da Nang is very bikeable along the beachfront." },
    { title: "💵 Budget Reality", text: "Vietnam is incredibly affordable. Street food meals: $1-3. Nice restaurant dinner: $8-15. Craft cocktail: $4-6. Hotel (boutique 4-star): $30-60/night. Spa massage (60 min): $10-15. You can live extremely well on $50-80/day including accommodation. 'Surprise me' budget here means you can do everything without thinking twice." },
    { title: "☀️ February–March Weather", text: "Dry season in Central Vietnam. Expect 75-85°F (24-29°C), low humidity, mostly sunny. Occasional light rain possible but rare. The sea is calm — perfect for swimming. This is the ideal time to visit. Evenings are pleasantly warm (70°F)." },
    { title: "🏨 Where to Stay", text: "Da Nang: My Khe Beach area for convenience and ocean views. Sơn Trà peninsula for luxury seclusion. An Thượng neighborhood for backpacker-chic cafes and nightlife. Hoi An: stay inside or just outside the Ancient Town for walkability. Huế: south bank of the Perfume River near the Citadel." },
    { title: "🍜 Food Rules", text: "Central Vietnam has its own distinct cuisine — different from Hanoi and Saigon. Must-try: mì Quảng (turmeric noodles, Da Nang's signature), bánh xèo (crispy crepes), bún chả cá (fish cake noodle soup), bánh mì (the original!), cao lầu (Hoi An-only noodles), bún bò Huế (spicy beef noodle soup from Huế). Eat where locals eat. Plastic stools = good sign." },
    { title: "📱 Useful Apps", text: "Grab (transport & food delivery), Google Maps (works well here), Google Translate (camera mode for Vietnamese menus), Agoda/Booking.com (hotels), Klook (tours/activities). Get a local SIM at the airport — Viettel or Mobifone, $5-10 for 30 days of data." }
  ],
  days: [
    {
      num: 1,
      title: "Arrival & My Khe Beach",
      neighborhoods: "My Khe Beach · An Thượng",
      date: "Feb 19",
      mapPins: [
        { lat: 16.0544, lng: 108.2022, label: "Da Nang Airport", num: 1, cat: "activity", desc: "International airport, 15 min to beach" },
        { lat: 16.0471, lng: 108.2462, label: "My Khe Beach", num: 2, cat: "activity", desc: "Iconic white sand beach" },
        { lat: 16.0502, lng: 108.2418, label: "An Thượng Street", num: 3, cat: "food", desc: "Backpacker-chic café and bar strip" },
        { lat: 16.0611, lng: 108.2275, label: "Dragon Bridge", num: 4, cat: "activity", desc: "Iconic dragon-shaped bridge, fire show Sat/Sun" }
      ],
      timeBlocks: [
        {
          label: "Afternoon",
          activities: [
            { title: "Check In & Beach Time", description: "Arrive, check into your beachfront hotel, and head straight to My Khe Beach. Named by Forbes as one of the most luxurious beaches on the planet, My Khe stretches for miles with powdery white sand and warm turquoise water. In February, conditions are perfect — calm seas, clear skies, 80°F. Grab a beach chair, order a fresh coconut, and decompress.", details: ["📍 My Khe Beach stretches from Sơn Trà to Ngũ Hành Sơn — the best section is between Phạm Văn Đồng and Võ Nguyên Giáp bridges", "💡 Beach chairs are free if you order a drink from the vendors. Fresh coconut: 20,000 VND ($0.80)."] }
          ],
          meals: [
            { type: "🍽️ Late Lunch", name: "Bún Chả Cá 109", description: "Your first meal in Da Nang should be the city's signature dish: bún chả cá — rice noodle soup with handmade fish cakes, tomato, dill, and a light but deeply savory broth. This no-frills spot on Nguyễn Chí Thanh is where locals go. Sit on a plastic stool, slurp loudly, and welcome to Vietnam.", meta: "25,000 VND ($1) · 109 Nguyễn Chí Thanh · Walk-in, always" }
          ],
          tips: [{ type: "tip", text: "Get a Vietnamese SIM card at the airport before leaving — Viettel has the best coverage. 30 days unlimited data for about $5-10. You'll need it for Grab, maps, and translating menus." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Dragon Bridge & Riverside Walk", description: "Walk along the Hàn River to see the Dragon Bridge — a 2,000-foot bridge shaped like a golden dragon. It's illuminated at night in shifting colors and breathes actual fire and water on weekend evenings (9pm Sat & Sun). Even on weekdays, the bridge and riverside promenade are gorgeous after dark. The city comes alive at night.", details: ["📍 Dragon Bridge · Free to walk/watch · Fire show at 9pm Sat & Sun only", "💡 Thursday is your arrival — catch the fire show this weekend if you're still in Da Nang."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Mì Quảng Bà Vị", description: "Da Nang's other signature: mì Quảng — wide turmeric-tinted noodles in a small amount of rich, savory broth with shrimp, pork, herbs, peanuts, and crispy rice crackers. This is THE dish of Da Nang. Bà Vị's version is legendary — the broth is deeply flavorful and the textures are perfect.", meta: "35,000 VND ($1.40) · 166 Lê Đình Dương · Lunch is better but dinner works" }
          ],
          tips: [{ type: "reddit", text: "Mì Quảng is not a soup — it's a noodle dish with just a little broth at the bottom. Mix everything together including the rice crackers. The peanuts and herbs are essential. Don't skip them.", cite: "r/VietNam" }]
        }
      ]
    },
    {
      num: 2,
      title: "Marble Mountains & Beachfront Life",
      neighborhoods: "Ngũ Hành Sơn · Non Nước Beach",
      date: "Feb 20",
      mapPins: [
        { lat: 16.0039, lng: 108.2627, label: "Marble Mountains", num: 1, cat: "activity", desc: "Five limestone karst hills with cave temples" },
        { lat: 16.0012, lng: 108.2651, label: "Thủy Sơn (Water Mountain)", num: 2, cat: "activity", desc: "Main mountain with caves and pagodas" },
        { lat: 15.9950, lng: 108.2690, label: "Non Nước Beach", num: 3, cat: "activity", desc: "Quiet beach at the foot of the mountains" },
        { lat: 16.0060, lng: 108.2610, label: "Stone Carving Village", num: 4, cat: "activity", desc: "Centuries-old marble sculpting tradition" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Marble Mountains (Ngũ Hành Sơn)", description: "Five towering limestone and marble hills rising dramatically from the coastal plain — each named after an element (water, fire, earth, metal, wood). Thủy Sơn (Water Mountain) is the largest and most spectacular: climb the stone steps (or take the elevator) to find Buddhist pagodas, Hindu cave shrines, and a massive cavern with sunlight streaming through a hole in the ceiling. During the Vietnam War, the Viet Cong used the caves as a field hospital. History, spirituality, and jaw-dropping geology in one place.", details: ["📍 52 Huyền Trân Công Chúa · 40,000 VND ($1.60) entrance · Elevator: 15,000 VND", "💡 Go early (7-8am) to beat tour groups. Wear shoes with grip — the steps can be slippery. Bring a flashlight for the deeper caves."] },
            { title: "Stone Carving Village", description: "At the base of the Marble Mountains sits a centuries-old stone carving village. Artisans have been sculpting Buddha statues, dragons, and decorative pieces from local marble for generations. Watch them work, browse the workshops, and pick up a small piece if you want a meaningful souvenir.", details: [] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Bánh Mì Bà Lan", description: "Proper Vietnamese bánh mì from a street cart — crispy baguette stuffed with pâté, cold cuts, pickled daikon and carrot, cilantro, chili, and a drizzle of soy sauce. Central Vietnam's bánh mì is distinct from Saigon's — lighter bread, more herbs. Perfection for $1.", meta: "15,000-25,000 VND ($0.60-1) · Near Marble Mountains · Morning only" }
          ],
          tips: [{ type: "tip", text: "The view from the top of Marble Mountains toward the coastline is one of the best in Da Nang. On a clear February day you can see from Sơn Trà peninsula all the way down to Hoi An." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Non Nước Beach", description: "After the mountains, walk down to Non Nước Beach — a quieter, less developed stretch of sand at the southern end of Da Nang's coastline. The water is calm, the sand is soft, and you'll likely have long stretches to yourself. Beach chairs, cold beers from wandering vendors, and the Marble Mountains rising behind you. Pure relaxation.", details: ["💡 Non Nước is popular with surfers in winter months. Even in February the waves can be fun for beginners."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Quán Cơm Nhà", description: "Cơm bình dân — Vietnam's beloved 'commoner's rice.' Point at whatever looks good behind the glass: braised pork belly, stir-fried morning glory, fried fish, egg omelette, pickled vegetables. They pile rice on a plate and you choose 2-3 dishes. A full, delicious lunch for $1.50.", meta: "25,000-40,000 VND · Various locations · Point-and-choose" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Sunset at My Khe", description: "Head back to My Khe for sunset — the beach faces east, but the sky behind the city and mountains turns golden and pink. The beachfront restaurants light up, the promenade fills with joggers and families. This is Da Nang's golden hour.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Hải Sản Bé Mặn", description: "Seafood is Da Nang's other obsession. This popular local joint serves incredibly fresh crab, prawns, clams, and squid — grilled, steamed, or stir-fried with tamarind, garlic butter, or chili salt. Pick your seafood from the tanks, choose your cooking style, and watch it come out minutes later. A full seafood feast for $10-15.", meta: "$10-15pp · 252 Võ Nguyên Giáp · Reservations helpful on weekends" }
          ],
          tips: [{ type: "reddit", text: "Da Nang seafood restaurants: the ones on the beach road (Võ Nguyên Giáp) are slightly pricier but still absurdly cheap by Western standards. Always check the price per kilo before ordering — it's displayed on the tanks.", cite: "r/VietNam" }]
        }
      ]
    },
    {
      num: 3,
      title: "Sơn Trà Peninsula & Linh Ứng Pagoda",
      neighborhoods: "Sơn Trà · Thọ Quang",
      date: "Feb 21",
      mapPins: [
        { lat: 16.1185, lng: 108.2777, label: "Linh Ứng Pagoda", num: 1, cat: "activity", desc: "67-meter Lady Buddha statue overlooking the sea" },
        { lat: 16.1250, lng: 108.3050, label: "Sơn Trà Summit", num: 2, cat: "activity", desc: "Jungle-covered peninsula with ocean views" },
        { lat: 16.1100, lng: 108.2600, label: "Tiên Sa Beach", num: 3, cat: "activity", desc: "Secluded beach on the peninsula" },
        { lat: 16.0720, lng: 108.2220, label: "Thọ Quang Fish Market", num: 4, cat: "food", desc: "Bustling wholesale fish market at dawn" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Thọ Quang Fish Market", description: "Wake up early and head to Thọ Quang — Da Nang's wholesale fish market. By 5-6am it's in full chaos: boats unloading the night's catch, vendors sorting mountains of fish, shrimp, squid, and crab under harsh lights. It's raw, real, and fascinating. The energy is incredible. Grab a Vietnamese iced coffee from a nearby stall and watch the commerce.", details: ["📍 Thọ Quang port · Free to walk around · Best before 7am", "💡 Wear shoes you don't mind getting wet. The ground is perpetually damp with fish water."] },
            { title: "Linh Ứng Pagoda", description: "Drive up the Sơn Trà Peninsula to Linh Ứng Pagoda, home to Vietnam's tallest Lady Buddha statue — 67 meters of white marble gazing serenely over the South China Sea. The temple complex is grand and peaceful, with bonsai gardens, ornate dragon pillars, and sweeping views of Da Nang's coastline. The scale of the Buddha against the ocean is breathtaking.", details: ["📍 Sơn Trà Peninsula · Free · Open 8am-8pm", "💡 The panoramic view from behind the Lady Buddha is one of the best photo spots in all of Vietnam. On a clear day you can see the Marble Mountains, Cù Lao Chàm island, and the entire coastline."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Bánh Cuốn Bà Tâm", description: "Bánh cuốn — steamed rice paper rolls filled with minced pork and wood ear mushrooms, served with fried shallots, herbs, and nước chấm dipping sauce. Delicate, light, and deeply satisfying. Bà Tâm's version has the perfect texture — silky thin sheets with a savory filling.", meta: "25,000 VND ($1) · 289 Trưng Nữ Vương · Morning only" }
          ],
          tips: [{ type: "tip", text: "Sơn Trà Peninsula is home to the endangered red-shanked douc langur — one of the world's most beautiful primates with striking red, gray, and white coloring. If you're lucky (and quiet), you might spot them in the trees along the road." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Sơn Trà Exploration", description: "Continue up the winding road through Sơn Trà's tropical jungle. The peninsula is a protected nature reserve — lush, wild, and home to rare wildlife. Stop at various viewpoints for panoramic ocean views. The road to the summit (Ban Co Peak) offers increasingly dramatic vistas. On a clear February day, the blues of the ocean are almost unreal.", details: ["💡 Hire a Grab bike or rent a motorbike for the peninsula loop. The roads are good but winding. Budget 2-3 hours to explore properly."] },
            { title: "Tiên Sa Beach", description: "Find your way to one of Sơn Trà's hidden beaches. Tiên Sa is the most accessible — a quiet crescent of sand backed by jungle. In February the water is calm and clear. You might have it entirely to yourself on a weekday.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Nhà Hàng Mân", description: "A beloved local seafood spot near Sơn Trà. Known for grilled squid with chili lime, garlic butter clams, and tamarind prawns. Simple setting, ocean views, incredible freshness. The owner's family has been fishing these waters for generations.", meta: "$8-12pp · Near Sơn Trà · Walk-in" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "An Thượng Nightlife", description: "Spend the evening in An Thượng — Da Nang's buzzing backpacker-chic neighborhood. A few blocks of cafés, craft beer bars, cocktail spots, and cheap eats. It's where expats, digital nomads, and young Vietnamese hang out. Low-key but social.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Nhà Hàng Trần", description: "Outstanding Vietnamese home cooking in a family-run restaurant. The bò kho (Vietnamese beef stew with French bread), gỏi cuốn (fresh spring rolls), and cá kho tộ (caramelized fish in clay pot) are all excellent. The kind of food Vietnamese grandmothers make.", meta: "$5-8pp · An Thượng area · Walk-in" }
          ],
          tips: [{ type: "reddit", text: "An Thượng is basically Vietnam's answer to a hipster neighborhood. Great craft beer at 7 Bridges, excellent cocktails at Luna Pub, and some surprisingly good Western food if you need a break from Vietnamese.", cite: "r/VietNam" }]
        }
      ]
    },
    {
      num: 4,
      title: "Da Nang Food Deep Dive & Spa Day",
      neighborhoods: "Hải Châu District · Central Da Nang",
      date: "Feb 22",
      mapPins: [
        { lat: 16.0678, lng: 108.2208, label: "Hàn Market", num: 1, cat: "food", desc: "Bustling central market with street food" },
        { lat: 16.0710, lng: 108.2230, label: "Cồn Market", num: 2, cat: "food", desc: "Largest local market in Da Nang" },
        { lat: 16.0550, lng: 108.2150, label: "Museum of Cham Sculpture", num: 3, cat: "activity", desc: "World's largest collection of Cham art" },
        { lat: 16.0490, lng: 108.2400, label: "Spa Area", num: 4, cat: "activity", desc: "Vietnamese massage and wellness" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Hàn & Cồn Markets", description: "Spend the morning at Da Nang's two main markets. Hàn Market is the tourist-friendly one — three floors of dried goods, fabrics, souvenirs, and food stalls. Cồn Market is the real deal — larger, noisier, and packed with local vendors selling everything from live chickens to tropical fruit to knock-off sneakers. The ground floor food section at Cồn is phenomenal — grandmas cooking bánh bèo, bánh nậm, and bánh bột lọc (Central Vietnamese rice cakes) over charcoal.", details: ["📍 Hàn Market: 119 Trần Phú · Cồn Market: 290 Hùng Vương · Both open early morning", "💡 The rice cake trio (bánh bèo, bánh nậm, bánh bột lọc) at Cồn Market is a must — three distinct textures and flavors, all involving rice flour in different forms. About $1 for all three."] },
            { title: "Museum of Cham Sculpture", description: "The world's largest collection of Cham sculpture — artifacts from the Champa kingdom that ruled Central Vietnam from the 2nd to 17th centuries. Hindu and Buddhist sculptures, altar pieces, and architectural fragments. It's small but remarkable — the sandstone carvings are exquisite. Opens a window into Vietnam's pre-Vietnamese history.", details: ["📍 02 2 Tháng 9 · 60,000 VND ($2.40) · Open 7am-5pm"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Cồn Market Food Stalls", description: "Graze through Cồn Market's ground-floor food section. Try bánh bèo (steamed rice cakes with shrimp floss), bánh nậm (flat rice dumplings in banana leaf), and chè (Vietnamese sweet dessert soup). Each vendor specializes in one dish and has been making it for decades.", meta: "5,000-15,000 VND per dish · Cồn Market ground floor" }
          ],
          tips: [{ type: "tip", text: "The Cham Museum is often overlooked but it's genuinely world-class. The Champa civilization left incredible art across Central Vietnam — understanding their history makes visits to Mỹ Sơn and Hoi An much richer." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Vietnamese Spa Afternoon", description: "Book a full afternoon at a Vietnamese spa. A 90-minute traditional massage, followed by a body scrub and a soak. Vietnamese massage is firm, effective, and absurdly affordable. Many spas also offer herbal steam baths and hot stone treatments. This is self-care on a budget that would cost 10x in the West.", details: ["💡 Recommended: Hera Spa, Herbal Spa, or Lá Spa in Da Nang. Book a 2-3 hour package for $20-35 including massage, scrub, and facial."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Bún Mắm Nêm Bà Duyên", description: "Bún mắm — fermented fish sauce noodle soup. Sounds intense, tastes incredible. The fermented anchovy broth is pungent, savory, and deeply umami. Topped with grilled pork, herbs, green mango, and a squeeze of lime. One of Da Nang's most distinctive dishes — an acquired taste that rewards the adventurous.", meta: "30,000 VND ($1.20) · Hải Châu District · Lunch only" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Dragon Bridge Fire Show", description: "If it's Saturday or Sunday evening, head to the Dragon Bridge for the fire and water show at 9pm. The massive dragon head breathes actual fire and then sprays water over the crowd. Thousands of locals gather on both sides of the bridge. It's loud, wet, chaotic, and absolutely joyful. Get there early for a good spot.", details: ["📍 Dragon Bridge · 9pm Sat & Sun · Free · Bring a poncho or accept you'll get wet"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Bánh Tráng Thịt Heo Trần", description: "Da Nang's famous bánh tráng thịt heo — boiled pork belly and herbs wrapped in rice paper with dipping sauce. Simple ingredients, extraordinary when fresh. The pork is silky, the herbs are aromatic, and the act of wrapping your own rolls is meditative. A communal-feeling meal even when dining solo.", meta: "$4-6pp · 54 Lê Hồng Phong · Walk-in" }
          ],
          tips: [{ type: "reddit", text: "The Dragon Bridge fire show is genuinely cool but GET AWAY from the dragon's mouth unless you want to be soaked. Locals bring umbrellas. The water spray reaches surprisingly far.", cite: "r/VietNam" }]
        }
      ]
    },
    {
      num: 5,
      title: "Transfer to Hoi An — Ancient Town",
      neighborhoods: "Hoi An Ancient Town",
      date: "Feb 23",
      mapPins: [
        { lat: 15.8801, lng: 108.3380, label: "Hoi An Ancient Town", num: 1, cat: "activity", desc: "UNESCO World Heritage lantern-lit streets" },
        { lat: 15.8773, lng: 108.3385, label: "Japanese Covered Bridge", num: 2, cat: "activity", desc: "400-year-old iconic bridge" },
        { lat: 15.8796, lng: 108.3396, label: "Phúc Kiến Assembly Hall", num: 3, cat: "activity", desc: "Ornate 17th-century Chinese temple" },
        { lat: 15.8815, lng: 108.3350, label: "Central Market", num: 4, cat: "food", desc: "Riverside market with incredible street food" },
        { lat: 15.8835, lng: 108.3370, label: "Thu Bồn River", num: 5, cat: "activity", desc: "Lantern-lit river at dusk" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Transfer to Hoi An", description: "Take a Grab or private car from Da Nang to Hoi An — about 30-40 minutes along the beautiful coastal road. Check into your hotel (stay inside or near the Ancient Town for walkability). Hoi An is small, flat, and best explored on foot or bicycle.", details: ["💡 Grab car from Da Nang to Hoi An: about 200,000-250,000 VND ($8-10). Or arrange hotel pickup."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "The Espresso Station", description: "Excellent Vietnamese egg coffee (cà phê trứng) and pastries in a beautifully designed café. The egg coffee is a Hanoi invention — whipped egg yolk, condensed milk, and strong Vietnamese coffee creating something between a dessert and a drink. Rich, warm, and addictive.", meta: "$2-4 · Hoi An · Walk-in" }
          ],
          tips: [{ type: "tip", text: "Buy the Hoi An Old Town ticket (120,000 VND / $5) — it grants entry to 5 of 21 heritage sites including the Japanese Bridge, assembly halls, and old houses. Worth it for the cultural context." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Hoi An Ancient Town Walk", description: "Lose yourself in Hoi An's Ancient Town — a UNESCO World Heritage site that was a major trading port from the 15th to 19th centuries. Japanese, Chinese, French, and Vietnamese architecture mingles on narrow streets. Yellow-walled buildings, ceramic-tiled roofs, Chinese assembly halls, and the iconic Japanese Covered Bridge (built in 1593). In the afternoon light, the colors are extraordinary.", details: ["📍 Hoi An Ancient Town · 120,000 VND ticket for heritage sites", "💡 The Ancient Town is car-free — explore on foot. The best streets for wandering: Trần Phú, Nguyễn Thái Học, and Bạch Đằng (riverside)."] },
            { title: "Phúc Kiến Assembly Hall", description: "The most ornate of Hoi An's Chinese assembly halls — built by Fujian Chinese merchants in 1697. Intricate dragon carvings, a spectacular main altar, beautiful courtyard gardens, and hundreds of hanging spiral incense coils. The smoke and light filtering through create an almost mystical atmosphere.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Cao Lầu Bà Bé", description: "Cao lầu — Hoi An's signature dish found nowhere else. Thick, chewy noodles (made with water from a specific local well and lye from Cham Island ash), topped with sliced pork, greens, crispy croutons, and a small amount of savory broth. The noodle texture is unique — dense and slightly smoky. This is THE Hoi An eat.", meta: "35,000 VND ($1.40) · 26 Bạch Đằng (by the river) · Walk-in" }
          ],
          tips: [{ type: "reddit", text: "Cao lầu is ONLY authentic in Hoi An — the noodles require specific well water and ash from Cù Lao Chàm island. Anyone serving it elsewhere is faking it. Eat it here multiple times.", cite: "r/VietNam" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Lantern-Lit Evening", description: "As dusk falls, Hoi An transforms. Hundreds of silk lanterns light up the Ancient Town — hanging from every building, reflected in the Thu Bồn River, casting warm colors across the stone streets. Buy a paper lantern from a riverside vendor, light it, and set it floating on the river. The full moon festival (14th day of lunar month) is the most magical night, but every evening in Hoi An feels enchanted.", details: ["💡 The best spot for the lantern reflection is the bridge connecting the Ancient Town to An Hoi island — stand in the middle and look both ways."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Morning Glory Restaurant", description: "Owned by celebrity chef Ms. Vỹ, Morning Glory is Hoi An's most famous restaurant — and it earns it. The white rose dumplings (another Hoi An-only specialty), the bánh xèo (crispy turmeric crepes), and the whole fried fish are all outstanding. Beautiful setting overlooking the Ancient Town.", meta: "$8-15pp · 106 Nguyễn Thái Học · Reservations recommended" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 6,
      title: "Hoi An Cooking Class & Countryside",
      neighborhoods: "Trà Quế Village · Hoi An Countryside",
      date: "Feb 24",
      mapPins: [
        { lat: 15.8920, lng: 108.3500, label: "Trà Quế Herb Village", num: 1, cat: "activity", desc: "Traditional herb farming village" },
        { lat: 15.8850, lng: 108.3420, label: "Cooking Class", num: 2, cat: "activity", desc: "Market visit + hands-on Vietnamese cooking" },
        { lat: 15.8700, lng: 108.3300, label: "Rice Paddies", num: 3, cat: "activity", desc: "Cycling through emerald green paddies" },
        { lat: 15.8780, lng: 108.3400, label: "Hoi An Market", num: 4, cat: "food", desc: "Morning market ingredient shopping" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Market Visit & Cooking Class", description: "Join a morning cooking class — one of Hoi An's best experiences. Start at the central market with your chef guide, learning to identify Vietnamese herbs, selecting ingredients, and understanding the food culture. Then head to the cooking school's countryside kitchen. You'll make 4-5 dishes: fresh spring rolls, bánh xèo, mì Quảng, and more. You eat everything you cook. Most classes include a basket boat ride through coconut palms.", details: ["💡 Recommended: Red Bridge Cooking School, Tra Que Water Wheel, or Thuan Tinh Island. Book ahead — $25-35pp including market visit, transport, and lunch.", "📍 Classes run 8am-1pm typically. Some offer afternoon sessions too."] }
          ],
          meals: [
            { type: "🍽️ Cooking Class Lunch", name: "Your Own Cooking", description: "You'll eat 4-5 dishes you prepared yourself — spring rolls, crispy pancakes, local noodles, and more. It's a feast.", meta: "Included in class fee ($25-35)" }
          ],
          tips: [{ type: "tip", text: "Cooking classes in Hoi An are legitimately one of the best food experiences in Southeast Asia. You'll learn techniques you'll use at home forever. The market tour alone is worth it for understanding Vietnamese ingredients." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Trà Quế Herb Village & Bicycle Ride", description: "Rent a bicycle and ride through Hoi An's countryside. Trà Quế is a 400-year-old herb farming village where families grow Vietnamese mint, basil, coriander, and dozens of other herbs using traditional methods. Ride through emerald rice paddies, past water buffalo, over small bridges. The flat terrain and quiet roads make it perfect for cycling. Stop at a village house for herbal tea.", details: ["💡 Bicycle rental from your hotel: 20,000-30,000 VND/day ($1). The Trà Quế loop is about 8km round trip from the Ancient Town."] }
          ],
          meals: [],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Riverside Dining", description: "Find a quiet spot along the Thu Bồn River for dinner. The Ancient Town's riverside restaurants offer beautiful views of the water, the lanterns, and the boats.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Cơm Gà Bà Buội", description: "Hoi An chicken rice — cơm gà — is the town's most beloved casual dish. Turmeric-yellow rice cooked in chicken broth, topped with hand-shredded poached chicken, fresh herbs, pickled onion, and chili sauce. Bà Buội's version has been perfecting this for decades. Simple and soul-satisfying.", meta: "30,000 VND ($1.20) · 22 Phan Chu Trinh · Walk-in" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 7,
      title: "Hoi An Tailoring & Beach Day",
      neighborhoods: "Ancient Town · An Bàng Beach",
      date: "Feb 25",
      mapPins: [
        { lat: 15.8800, lng: 108.3370, label: "Tailor Shops", num: 1, cat: "activity", desc: "World-famous custom tailoring" },
        { lat: 15.9020, lng: 108.3600, label: "An Bàng Beach", num: 2, cat: "activity", desc: "Best beach near Hoi An" },
        { lat: 15.8810, lng: 108.3360, label: "Cloth Market", num: 3, cat: "activity", desc: "Silk and fabric shopping" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Custom Tailoring", description: "Hoi An is famous worldwide for its custom tailoring — 400+ tailors who can make anything from a bespoke suit to a silk dress in 24-48 hours. Browse fabric at the cloth market, pick your designs, and get measured. A custom suit costs $80-200 depending on fabric. Dresses, shirts, coats — all ridiculously affordable. The quality ranges from average to genuinely excellent — stick to recommended shops.", details: ["💡 Top recommended tailors: Bé (Mr. Xe), Yaly Couture, A Dong Silk. Get your first fitting done in the morning — they'll have a draft ready by evening for adjustments. Plan 2-3 fittings over a couple days for the best result."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Bánh Mì Phượng", description: "Anthony Bourdain called this 'a symphony in a sandwich.' Possibly the most famous bánh mì in Vietnam. The baguette is crispy-soft perfection, stuffed with combinations like grilled pork, pâté, egg, herbs, and chili. There's always a queue — it moves fast. Order #1 (the special) if in doubt.", meta: "25,000 VND ($1) · 2B Phan Châu Trinh · Walk-in, expect a queue" }
          ],
          tips: [{ type: "reddit", text: "Bánh Mì Phượng is famous for a reason but the queue can be long. Bánh Mì Madame Khánh (The Bánh Mì Queen) at 115 Trần Cao Vân is equally good with a shorter wait. Both are legendary.", cite: "r/VietNam" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "An Bàng Beach", description: "Cycle or Grab to An Bàng Beach — a beautiful stretch of sand about 4km from the Ancient Town. Beach bars, palm trees, loungers, and warm clear water. More developed than Non Nước but with a laid-back boho vibe. Perfect for an afternoon of swimming, reading, and cold Bia Hoi (local draft beer).", details: ["📍 4km from Ancient Town · Grab or bicycle · Lounger rental free with drink order"] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Soul Kitchen (An Bàng Beach)", description: "Beachfront restaurant with Vietnamese and Western options. The grilled fish with lemongrass, fried wonton in creamy sauce, and fresh fruit smoothies are highlights. Eat with sand between your toes and the sound of waves.", meta: "$5-10pp · An Bàng Beach · Walk-in" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Tailor Fitting & Evening Stroll", description: "Return to your tailor for the first fitting. Walk the Ancient Town as it lights up. Each evening in Hoi An feels different — discover new alleys, new lantern configurations, new food stalls.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Mót Hoi An", description: "Elegant Vietnamese fusion in a beautifully restored heritage building. The chef reinterprets Central Vietnamese classics with modern technique — think deconstructed cao lầu, perfectly seared tuna with Vietnamese herbs, and artful desserts. Best upscale meal in Hoi An.", meta: "$15-25pp · Nguyễn Thái Học · Reservations recommended" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 8,
      title: "Cù Lao Chàm Island Day Trip",
      neighborhoods: "Cù Lao Chàm Marine Park",
      date: "Feb 26",
      mapPins: [
        { lat: 15.9450, lng: 108.5150, label: "Cù Lao Chàm", num: 1, cat: "activity", desc: "UNESCO marine park island" },
        { lat: 15.9470, lng: 108.5200, label: "Bãi Chồng Beach", num: 2, cat: "activity", desc: "Clear snorkeling waters" },
        { lat: 15.9420, lng: 108.5100, label: "Cù Lao Chàm Village", num: 3, cat: "food", desc: "Fishing village with seafood lunch" }
      ],
      timeBlocks: [
        {
          label: "Full Day",
          activities: [
            { title: "Cù Lao Chàm Island", description: "Take a speedboat (20 min) or slow boat (1.5 hours) from Cửa Đại port to Cù Lao Chàm — a UNESCO Biosphere Reserve archipelago. The main island has pristine beaches, coral reefs for snorkeling, a small fishing village, and jungle hiking trails. The water clarity is remarkable. Snorkel among coral gardens, explore the village's Cham-era ruins and temples, and feast on fresh seafood cooked by island families.", details: ["📍 Boats depart from Cửa Đại port, 5km east of Hoi An · Speedboat: 350,000 VND ($14) round trip", "💡 February is excellent for Cù Lao Chàm — calm seas, good visibility. Book through your hotel or a tour office in Hoi An. Full-day tours including snorkeling and lunch run $20-30."] },
            { title: "Snorkeling & Beach Time", description: "The snorkeling around Cù Lao Chàm is Central Vietnam's best — coral gardens, tropical fish, and clear warm water. Bãi Chồng and Bãi Bắc beaches have the best underwater life. Equipment is provided on tours. Between snorkeling sessions, relax on the beach or explore the island's trails.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Island Seafood Feast", description: "Lunch on the island is typically a multi-course seafood spread cooked by local families: grilled fish, steamed clams, shrimp in tamarind sauce, crab, and fresh fruit. Eaten at communal tables on the beach or in a family home. Some of the freshest seafood you'll ever have — literally caught that morning.", meta: "Included in most day tours · Or buy directly from village vendors $5-10" }
          ],
          tips: [{ type: "tip", text: "Cù Lao Chàm is plastic-free — no plastic bags or single-use plastics allowed on the island. Bring a reusable water bottle. The conservation efforts here are genuine and impressive." }]
        }
      ]
    },
    {
      num: 9,
      title: "Mỹ Sơn Sanctuary — Champa Ruins",
      neighborhoods: "Mỹ Sơn · Duy Xuyên",
      date: "Feb 27",
      mapPins: [
        { lat: 15.7643, lng: 108.1272, label: "Mỹ Sơn Sanctuary", num: 1, cat: "activity", desc: "UNESCO Champa Hindu temple ruins" },
        { lat: 15.7650, lng: 108.1280, label: "Group B/C Temples", num: 2, cat: "activity", desc: "Best-preserved temple cluster" },
        { lat: 15.8800, lng: 108.3380, label: "Hoi An Ancient Town", num: 3, cat: "food", desc: "Return for evening" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Mỹ Sơn Sanctuary", description: "A 1.5-hour drive inland from Hoi An through lush countryside to Mỹ Sơn — the spiritual capital of the Champa kingdom and Vietnam's most important Hindu temple complex. Built between the 4th and 13th centuries, these brick towers were dedicated to Shiva and stand in a jungle-clad valley surrounded by mountains. Many were damaged by US bombing in 1969, but the surviving structures are hauntingly beautiful. The brickwork is extraordinary — no mortar was used, and the construction technique remains partially unexplained.", details: ["📍 Mỹ Sơn, Duy Xuyên · 150,000 VND ($6) · Open 6:30am-5pm", "💡 Go early (arrive by 7am) to beat tour buses. The morning mist through the jungle valleys is atmospheric. A traditional Apsara dance performance happens at 9:30am and 10:30am at the site — worth catching."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Hotel Breakfast or Packed", description: "Most tours depart early (5:30-6am). Grab breakfast at your hotel or pack something. Coffee is essential.", meta: "" }
          ],
          tips: [{ type: "reddit", text: "Mỹ Sơn isn't Angkor Wat — temper expectations. But if you appreciate the history (1,000 years of Cham civilization) and the jungle setting, it's magical. The Apsara dance is surprisingly moving. Go early, take your time, read the info boards.", cite: "r/VietNam" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Countryside Return & Relaxation", description: "Return to Hoi An via the scenic route through rice paddies and villages. The afternoon is yours — revisit the Ancient Town, pick up your tailoring, or simply relax. After an early morning, an afternoon nap and pool time is well-earned.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Hoi An Central Market", description: "Graze through the Central Market's food stalls. Try bánh bao bánh vạc (white rose dumplings — translucent shrimp dumplings shaped like roses, unique to Hoi An), wonton soups, and fresh fruit. Each stall specializes in one thing and does it perfectly.", meta: "$1-3 for multiple dishes · Central Market · Until early afternoon" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Ancient Town Evening", description: "Pick up your tailored clothes for final fitting. Then spend the evening wandering — Hoi An rewards repeated visits to the same streets as you notice new details each time.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Ông Hai (Mr. Hai)", description: "Legendary hole-in-the-wall known for cơm gà (chicken rice) and cao lầu. Mr. Hai himself often serves you. The dining room is tiny, the food is incredible, and the authenticity is unmatched.", meta: "30,000-45,000 VND ($1.20-1.80) · 46A Trần Hưng Đạo · Walk-in" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 10,
      title: "Hoi An Slow Day — Art, Coffee & Craft",
      neighborhoods: "Ancient Town · An Hoi Island",
      date: "Feb 28",
      mapPins: [
        { lat: 15.8790, lng: 108.3395, label: "Art Galleries", num: 1, cat: "activity", desc: "Traditional and contemporary Vietnamese art" },
        { lat: 15.8770, lng: 108.3360, label: "An Hoi Island", num: 2, cat: "activity", desc: "Lantern workshops and craft market" },
        { lat: 15.8805, lng: 108.3355, label: "Reaching Out Tea House", num: 3, cat: "food", desc: "Silent tea house run by deaf artisans" },
        { lat: 15.8810, lng: 108.3375, label: "Precious Heritage Museum", num: 4, cat: "activity", desc: "Free photography museum on ethnic minorities" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Reaching Out Tea House", description: "Start at Reaching Out — a silent tea house run by deaf and mute artisans. Communication is done via wooden blocks with written requests. You order by pointing, and tea is served in beautiful handmade ceramics. The silence is profound and meditative. Vietnamese tea, drip coffee, and pastries. A genuinely moving experience.", details: ["📍 131 Trần Phú · Open 8am-9pm · Prices slightly above average but support an incredible social enterprise"] },
            { title: "Precious Heritage Museum", description: "Réhahn's free photography museum showcasing Vietnam's 54 ethnic minority groups. Stunning large-format portraits, traditional costumes on display, and detailed cultural context. One of the best free museums in Southeast Asia.", details: ["📍 26 Phan Bội Châu · Free · Open 8am-6pm"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Reaching Out Tea House", description: "Vietnamese drip coffee and bánh bao (steamed buns) in silence. The handmade ceramics the tea is served in are beautiful.", meta: "$3-5 · 131 Trần Phú" }
          ],
          tips: [{ type: "tip", text: "Reaching Out also has a gift shop selling handmade crafts by their artisans — beautiful lanterns, ceramics, and textiles. Meaningful souvenirs that support the deaf community." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "An Hoi Island & Lantern Workshops", description: "Cross the bridge to An Hoi — the island across from the Ancient Town. Less touristy, with lantern-making workshops, art studios, and the night market area. Take a lantern-making class ($5-10) and create your own silk lantern to bring home. The artisans teach you to build the bamboo frame and wrap the silk.", details: [] },
            { title: "Vietnamese Coffee Culture", description: "Hoi An has an exceptional café scene. Try Hoi An Roastery (excellent single-origin Vietnamese coffee), Faifo Coffee (rooftop views over the Ancient Town), or The Espresso Station. Vietnamese coffee culture is unique — strong, dark-roasted robusta, drip-filtered through a phin, often with condensed milk. Sit, watch the world pass, and savor.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Khôi Bánh Xèo", description: "Bánh xèo — massive crispy turmeric crepes stuffed with shrimp, pork, bean sprouts, and herbs. You tear off pieces and wrap them in rice paper with lettuce and herbs, dipping in nước chấm. The sizzle as the batter hits the pan is the dish's namesake (xèo = sizzle). Addictive.", meta: "20,000-30,000 VND · Multiple locations · Walk-in" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Night Market & River Walk", description: "Stroll the An Hoi Night Market — lanterns, souvenirs, street food, and floating candle boats. The atmosphere is magical but touristy. The real experience is the walk back through the Ancient Town as the shops close and the lanterns dim.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Secret Garden", description: "A hidden courtyard restaurant serving traditional Vietnamese home cooking. The lemongrass chicken, clay pot fish, and green papaya salad are stellar. The garden setting — string lights, potted plants, old walls — is pure Hoi An romance.", meta: "$6-10pp · Off Trần Phú · Walk-in" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 11,
      title: "Transfer to Huế — Imperial City",
      neighborhoods: "Huế Citadel · South Bank",
      date: "Mar 1",
      mapPins: [
        { lat: 16.4698, lng: 107.5770, label: "Huế Imperial Citadel", num: 1, cat: "activity", desc: "Massive walled fortress of the Nguyễn dynasty" },
        { lat: 16.4700, lng: 107.5795, label: "Forbidden Purple City", num: 2, cat: "activity", desc: "Inner sanctum of the emperor" },
        { lat: 16.4635, lng: 107.5852, label: "Đông Ba Market", num: 3, cat: "food", desc: "Huế's main market and food haven" },
        { lat: 16.4580, lng: 107.5900, label: "Perfume River", num: 4, cat: "activity", desc: "Scenic river flowing through Huế" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Scenic Transfer to Huế", description: "Drive from Hoi An to Huế — about 3-4 hours via the coastal route, passing through the legendary Hải Vân Pass (sea cloud pass). This stretch of road is one of the most beautiful in the world — clinging to cliff faces above the South China Sea with jaw-dropping views. Stop at the pass summit for photos. The old French-built road (not the tunnel) is the scenic route.", details: ["💡 Hire a private car/driver for the Hai Van Pass route ($40-50 one way). Worth every penny vs. the bus that takes the tunnel. Stop at Lăng Cô fishing village for coffee."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Quick Hoi An Send-Off", description: "Grab a final bánh mì from Phượng or Madame Khánh for the road. You'll miss them.", meta: "25,000 VND" }
          ],
          tips: [{ type: "reddit", text: "The Hai Van Pass is genuinely one of the most scenic drives in the world. Top Gear called it the best coast road they've ever driven. Don't take the tunnel — take the old road over the top. The views will blow your mind.", cite: "r/VietNam" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Huế Imperial Citadel", description: "Arrive in Huế and head straight to the Imperial Citadel — a massive walled fortress that was the capital of Vietnam's Nguyễn dynasty from 1802 to 1945. Within its walls lies the Imperial City, and within that, the Forbidden Purple City — once reserved exclusively for the emperor. Much was destroyed during the Vietnam War (1968 Battle of Huế), but the restoration is ongoing and what remains is magnificent: ornate gates, throne rooms, temples, gardens, and dragon-carved pathways.", details: ["📍 Citadel, Phú Hậu · 200,000 VND ($8) · Open 7am-5:30pm", "💡 Budget 2-3 hours minimum. The Citadel is enormous. The main gate (Ngọ Môn) and the Thai Hoa Palace throne room are the highlights. Audio guides available."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Bún Bò Huế Bà Tuyết", description: "Huế's most famous dish: bún bò Huế — spicy beef and pork noodle soup. The broth is complex — lemongrass, shrimp paste, chili oil — with round rice noodles, tender beef shank, pork knuckle, and blood cake (optional). Bà Tuyết's version is fiery, aromatic, and deeply satisfying. This is why Huế is Vietnam's culinary capital.", meta: "30,000 VND ($1.20) · 47 Nguyễn Công Trứ · Walk-in" }
          ],
          tips: [{ type: "tip", text: "Huế is Vietnam's food capital — its royal cuisine tradition (cơm cung đình) and street food are both exceptional. The city has more unique dishes than any other in Vietnam. Eat everything." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Perfume River Sunset", description: "Walk along the Perfume River as the sun sets behind the Citadel walls. The river earned its name from the flowers that fall into it from orchards upstream. In the evening light, the old bridges, pagodas, and royal tombs along the banks create a timeless scene.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Quán Hành Cung", description: "Royal Huế cuisine — the cooking tradition of the Nguyễn emperors. Elaborately presented small dishes: lotus stem salad, steamed rice flower dumplings, grilled pork in lá lốt leaves, banana flower salad. The portions are delicate, the flavors refined. This style of eating — many small beautiful plates — is uniquely Huế.", meta: "$10-15pp · Citadel area · Reservations recommended" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 12,
      title: "Huế Royal Tombs & Pagodas",
      neighborhoods: "South Bank · Tomb Complex Area",
      date: "Mar 2",
      mapPins: [
        { lat: 16.4588, lng: 107.5453, label: "Thiên Mụ Pagoda", num: 1, cat: "activity", desc: "Iconic 7-story pagoda on the Perfume River" },
        { lat: 16.4058, lng: 107.5453, label: "Tomb of Tự Đức", num: 2, cat: "activity", desc: "Most beautiful royal tomb in Huế" },
        { lat: 16.3973, lng: 107.5757, label: "Tomb of Khải Định", num: 3, cat: "activity", desc: "Ornate fusion of Eastern and Western styles" },
        { lat: 16.4150, lng: 107.5250, label: "Tomb of Minh Mạng", num: 4, cat: "activity", desc: "Harmonious gardens and pavilions" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Thiên Mụ Pagoda", description: "Vietnam's most iconic pagoda — the 7-story octagonal tower rises from the banks of the Perfume River and has been Huế's symbol since 1601. The monastery is still active — monks in saffron robes, incense smoke, bonsai gardens. The famous car that carried monk Thích Quảng Đức to his self-immolation protest in 1963 is preserved here.", details: ["📍 Kim Long, Huế · Free · Open 8am-5pm", "💡 Arrive by boat on the Perfume River for the most dramatic approach. Dragon boats depart from the dock near Tòa Khâm, 100,000 VND round trip."] },
            { title: "Tomb of Tự Đức", description: "The most beautiful of Huế's royal tombs — Emperor Tự Đức designed it himself as a place of poetry and contemplation. Pine-shaded pavilions, lotus lakes, and ornate temples set in a peaceful forest. Tự Đức used it as a retreat during his lifetime, writing poetry by the lake. The romantic, melancholy atmosphere is palpable.", details: ["📍 Thủy Xuân · 150,000 VND ($6) · Open 7am-5:30pm"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Bánh Canh Cua", description: "Thick tapioca-rice noodles in crab broth with crab meat, quail eggs, and herbs. Huế's answer to comfort food. The broth is rich and slightly sweet from the crab. Found at street stalls near the Citadel.", meta: "25,000-35,000 VND · Street stalls near Citadel" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Tomb of Khải Định", description: "The most visually striking tomb — Emperor Khải Định built an extravagant mausoleum blending Vietnamese, Chinese, and European styles. The interior is completely covered in glass and ceramic mosaic — walls, columns, ceiling — creating a dazzling, almost psychedelic effect. The craftsmanship is extraordinary.", details: ["📍 Chau Chu · 150,000 VND ($6)"] },
            { title: "Tomb of Minh Mạng", description: "The most architecturally harmonious tomb complex. Set around a series of lakes and gardens, the layout follows perfect feng shui principles — gates, bridges, pavilions, and the burial mound aligned on a single axis. Peaceful and grand in equal measure.", details: ["📍 Hương Thọ · 150,000 VND ($6)"] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Cơm Hến", description: "Tiny clams from the Perfume River served over cold rice with peanuts, chili oil, herbs, and crispy pork rinds. A uniquely Huế dish — the clams are minuscule but packed with flavor. Eat at the riverside stalls near Đông Ba Market. Strange, beautiful, delicious.", meta: "15,000-25,000 VND · Đông Ba Market area" }
          ],
          tips: [{ type: "tip", text: "A combo ticket for the Citadel + 2 tombs is 360,000 VND ($14.40) — slight savings over individual tickets. Available at any tomb or the Citadel entrance." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Huế Night Food Tour", description: "Explore Huế's incredible street food scene after dark. The streets around Đông Ba Market and the south bank come alive with vendors. Must-try: bánh bèo (steamed rice cakes), nem lụi (lemongrass pork skewers), bánh lọc (translucent tapioca dumplings).", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Hàng Me Street Food", description: "Hàng Me is Huế's street food alley. Vendor after vendor selling dishes you won't find anywhere else: bánh ram ít (crispy and soft rice cakes together), bánh ướt (steamed rice sheets), and nem lụi (pork on lemongrass sticks, wrapped in rice paper with dipping sauce). Walk, eat, repeat.", meta: "$2-5 for a full feast · Hàng Me / Kim Long area" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 13,
      title: "Huế Countryside & Gardens",
      neighborhoods: "Thủy Biều · Kim Long",
      date: "Mar 3",
      mapPins: [
        { lat: 16.4500, lng: 107.5500, label: "Thủy Biều Village", num: 1, cat: "activity", desc: "Pomelo gardens and traditional houses" },
        { lat: 16.4700, lng: 107.5550, label: "Kim Long Village", num: 2, cat: "activity", desc: "Garden houses of Huế nobles" },
        { lat: 16.4638, lng: 107.5870, label: "Đông Ba Market", num: 3, cat: "food", desc: "Main market for local Huế specialties" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Thủy Biều Garden Village", description: "Rent a bicycle and ride to Thủy Biều — a peaceful village along the Perfume River famous for its pomelo orchards and traditional garden houses. These houses — surrounded by tropical gardens, fish ponds, and fruit trees — represent a uniquely Huế way of living that's been maintained for centuries. Some families open their homes for visits and serve herbal tea.", details: ["💡 The ride from central Huế is about 5km along the river — flat and scenic. Ask at your hotel for a bicycle ($1-2/day)."] },
            { title: "Kim Long Garden Houses", description: "Continue to Kim Long village to see more of Huế's famous garden houses — these were built by mandarins and nobles of the Nguyễn court. Each house follows feng shui principles with specific gardens, gates, and screen walls. An Hiên Garden House is the most famous and best-preserved.", details: [] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Bánh Bèo Nậm Lọc", description: "The Huế rice cake trio: bánh bèo (tiny steamed rice cakes with shrimp floss), bánh nậm (flat steamed rice dumplings), and bánh lọc (translucent tapioca dumplings with shrimp). Served together on a platter with nước chấm. Delicate, refined, and beautiful — this is Huế's culinary elegance.", meta: "25,000-40,000 VND for all three · Street stalls" }
          ],
          tips: [{ type: "tip", text: "Huế's garden house culture is unique in Vietnam — it reflects the city's intellectual and aesthetic traditions as the imperial capital. These aren't palaces but refined family homes where poetry, music, and gardening were arts of daily life." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Đông Ba Market Deep Dive", description: "Spend the afternoon at Đông Ba — Huế's largest and most authentic market. Three levels of food, fabric, flowers, and daily life. The ground floor food section is a treasure: fresh herbs stacked in artistic piles, hand-made noodles drying on racks, and vendors cooking dishes that haven't changed in generations.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Lạc Thiện Vegetarian", description: "Huế has Vietnam's strongest vegetarian tradition — tied to its Buddhist heritage. Lạc Thiện serves incredible vegetarian versions of Vietnamese classics: mock-meat phở, vegetable spring rolls, tofu in lemongrass. Run by a deaf family, order by pointing at the menu. A beautiful, delicious experience.", meta: "30,000-50,000 VND · 6 Đinh Công Tráng · Walk-in" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Final Huế Evening", description: "Walk the Perfume River one last time. The bridge over to the Citadel is beautifully lit at night. Reflect on three days of imperial history, extraordinary food, and gentle beauty.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Risotto Restaurant", description: "Surprisingly excellent Italian-Vietnamese fusion on the south bank. The owner-chef trained in Italy and creates dishes that merge both cuisines — risotto with Vietnamese herbs, pasta with local seafood. A nice change of pace for your last Huế evening.", meta: "$8-12pp · South bank · Walk-in" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 14,
      title: "Return to Da Nang — Beach Reset",
      neighborhoods: "My Khe Beach · An Thượng",
      date: "Mar 4",
      mapPins: [
        { lat: 16.4700, lng: 107.5770, label: "Huế Departure", num: 1, cat: "activity", desc: "Morning departure via Hai Van Pass" },
        { lat: 16.2100, lng: 108.0200, label: "Hải Vân Pass Summit", num: 2, cat: "activity", desc: "Scenic stop on the return drive" },
        { lat: 16.0471, lng: 108.2462, label: "My Khe Beach", num: 3, cat: "activity", desc: "Welcome-back beach session" },
        { lat: 16.0500, lng: 108.2420, label: "An Thượng", num: 4, cat: "food", desc: "Evening in the café neighborhood" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Drive Back via Hải Vân Pass", description: "Take the scenic road back through Hải Vân Pass — equally stunning in the southbound direction. Stop at the summit and at Lăng Cô, a beautiful lagoon fishing village between the mountains and the sea.", details: [] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Bún Bò Huế (One Last Time)", description: "You can't leave Huế without one more bowl. The early-morning versions at street stalls are the best — the broth has been simmering all night.", meta: "30,000 VND" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Beach Reset", description: "Back in Da Nang. Check into your hotel (same area or try somewhere new) and head straight to My Khe Beach. After temples, tombs, and history, the beach feels like a reward. Swim, sunbathe, and recalibrate.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Quán Bé", description: "Simple beachside spot for fresh seafood. Grilled shrimp, steamed clams in lemongrass, fried rice. Perfect post-drive fuel.", meta: "$6-10pp · Near My Khe Beach" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "An Thượng Evening", description: "Settle back into Da Nang's rhythm in the An Thượng neighborhood. Craft beer, rooftop bars, and cheap street food.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Ốc Đào", description: "Vietnamese snail restaurant — yes, snails. A beloved genre of Vietnamese street food. Dozens of snail species prepared in every way: grilled with chili salt, steamed in coconut, stir-fried with tamarind. Order a spread and try everything. Best experienced with Bia Hoi (fresh draft beer, 5,000 VND / $0.20).", meta: "$5-8pp · Hải Châu area · Walk-in, evening only" }
          ],
          tips: [{ type: "reddit", text: "Snail restaurants are a huge part of Vietnamese food culture that most tourists miss. Go with an open mind — the flavors are incredible and it's incredibly social. Order Bia Hoi (fresh keg beer) at 5,000 VND per glass.", cite: "r/VietNam" }]
        }
      ]
    },
    {
      num: 15,
      title: "Bà Nà Hills & Golden Bridge",
      neighborhoods: "Bà Nà Hills",
      date: "Mar 5",
      mapPins: [
        { lat: 15.9974, lng: 107.9945, label: "Bà Nà Hills", num: 1, cat: "activity", desc: "Mountaintop French village and theme park" },
        { lat: 15.9980, lng: 107.9950, label: "Golden Bridge", num: 2, cat: "activity", desc: "Iconic bridge held by giant stone hands" },
        { lat: 15.9970, lng: 107.9940, label: "French Village", num: 3, cat: "activity", desc: "European-style mountaintop village" },
        { lat: 15.9960, lng: 107.9930, label: "Cable Car Station", num: 4, cat: "activity", desc: "World-record-holding cable car" }
      ],
      timeBlocks: [
        {
          label: "Full Day",
          activities: [
            { title: "Bà Nà Hills", description: "Take the record-holding cable car (5,801 meters, one of the longest in the world) up to Bà Nà Hills — a mountaintop entertainment complex at 1,489 meters elevation. The centerpiece is the Golden Bridge — a pedestrian walkway held up by two enormous stone hands emerging from the mountainside. It's become one of Vietnam's most iconic images. Beyond the bridge, there's a recreated French village, gardens, temples, and amusement rides. The temperature is 10-15°F cooler than the coast — refreshing on a warm day.", details: ["📍 Bà Nà Hills · 900,000 VND ($36) including cable car, all attractions · Open 7am-9pm", "💡 Go early (arrive by 8am opening) to get the Golden Bridge without crowds. The morning mist adds drama. Weekdays are much less crowded than weekends. Bring a light jacket — it's noticeably cooler at altitude."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Bà Nà Hills Restaurants", description: "Multiple restaurants at the summit — Vietnamese, Asian fusion, and Western. The beer garden is fun. Food is theme-park quality but the setting (eating in the clouds above the coast) makes up for it.", meta: "$8-15pp · Various options at summit" }
          ],
          tips: [{ type: "reddit", text: "Bà Nà Hills is touristy and kitschy — go in with that expectation and you'll enjoy it. The Golden Bridge IS genuinely impressive. The cable car ride is spectacular. If you go early on a weekday, you can get photos without 500 people in them.", cite: "r/VietNam" }]
        }
      ]
    },
    {
      num: 16,
      title: "Full Beach & Spa Day",
      neighborhoods: "My Khe · Sơn Trà",
      date: "Mar 6",
      mapPins: [
        { lat: 16.0471, lng: 108.2462, label: "My Khe Beach", num: 1, cat: "activity", desc: "Full day of beach relaxation" },
        { lat: 16.0490, lng: 108.2400, label: "Spa", num: 2, cat: "activity", desc: "Afternoon spa treatment" },
        { lat: 16.0550, lng: 108.2150, label: "Riverside Walk", num: 3, cat: "activity", desc: "Evening stroll along the Hàn River" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Beach Morning", description: "Pure relaxation. My Khe Beach at dawn — the sand is cool, the water is warm, and local Vietnamese do their morning exercises on the shore: tai chi, badminton, swimming. Join them or just watch with coffee. The early morning light on the South China Sea is extraordinary.", details: [] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Xèo & Bánh Beach Breakfast", description: "Walk to one of the beachfront restaurants for a lazy breakfast. Eggs, bánh mì, tropical fruit, Vietnamese coffee. Take your time.", meta: "$3-5pp" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Spa Afternoon", description: "Book a multi-treatment spa session. Vietnamese herbal massage, hot stone therapy, body wrap, facial. Three hours of pampering for $30-50. This is the slow-travel luxury that three weeks allows — no rush, no FOMO, just deep relaxation.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Phở Lý Quốc Sư", description: "Yes, phở exists in Central Vietnam too — but the local versions differ from Hanoi's. Lighter broth, different herbs, sometimes with a hint of chili. Simple, nourishing, perfect for a lazy beach day.", meta: "35,000-45,000 VND · Various locations" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Riverside Walk & Bridge Lights", description: "Walk the Hàn River promenade. Da Nang's bridges light up spectacularly at night — Dragon Bridge, Trần Thị Lý Bridge (sail-shaped), and the Love Bridge. The whole waterfront is a light show.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Fatfish", description: "Modern Vietnamese restaurant with a focus on fresh seafood and creative presentation. The tuna tataki with Vietnamese herbs, the soft-shell crab, and the passion fruit cocktails are excellent. One of Da Nang's best contemporary dining spots.", meta: "$12-20pp · Sơn Trà area · Reservations recommended" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 17,
      title: "Da Nang Hidden Gems & Local Life",
      neighborhoods: "Thanh Khê · Liên Chiểu",
      date: "Mar 7",
      mapPins: [
        { lat: 16.0750, lng: 108.2000, label: "Local Neighborhoods", num: 1, cat: "activity", desc: "Off-the-beaten-path Da Nang" },
        { lat: 16.0800, lng: 108.1900, label: "Thanh Khê Market", num: 2, cat: "food", desc: "Neighborhood market without tourists" },
        { lat: 16.0550, lng: 108.2350, label: "APEC Park", num: 3, cat: "activity", desc: "Waterfront sculpture park" },
        { lat: 16.0680, lng: 108.2200, label: "Da Nang Cathedral", num: 4, cat: "activity", desc: "Pink French colonial church" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Local Neighborhood Exploration", description: "Spend the morning in the neighborhoods tourists never visit. Thanh Khê and Liên Chiểu are residential areas with incredible local markets, neighborhood temples, and authentic street food. Walk or Grab to a local market — no English signs, no tourists, just Vietnamese daily life. Point at food, smile, eat. This is the real Da Nang.", details: [] },
            { title: "Da Nang Cathedral (Pink Church)", description: "Built by the French in 1923, this cotton-candy-pink cathedral is unexpectedly charming. The rooster weathervane on top earned it the local nickname 'Rooster Church.' Worth a quick visit for the architecture and photos.", details: ["📍 156 Trần Phú · Free · Open for mass, otherwise view from outside"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Street Xôi (Sticky Rice)", description: "Xôi — Vietnamese sticky rice with toppings. Xôi gà (chicken), xôi thịt (pork), xôi đậu (mung bean). Sold from carts and baskets by women in conical hats every morning across Vietnam. Filling, cheap, and genuinely delicious. Buy from any street vendor — they're all good.", meta: "10,000-20,000 VND · Any street vendor, morning only" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "APEC Park & Waterfront", description: "Stroll APEC Sculpture Park along the Hàn River — a collection of sculptures donated by the 21 APEC nations when Da Nang hosted the 2017 summit. Nice for a shaded walk. Then cross the river to explore the east bank.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Bún Riêu Ông Tạ", description: "Bún riêu — crab and tomato noodle soup. The broth is tangy from tomatoes, rich from crab paste, and topped with fried tofu, blood cake, and herbs. It's sour, savory, and refreshing. A perfect lunch dish.", meta: "30,000 VND · Central Da Nang · Walk-in" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Evening Food Crawl", description: "Da Nang's evening street food scene is legendary. Walk along Nguyễn Chí Thanh, Hoàng Diệu, or Hải Phòng streets after dark — grilled skewers, bánh tráng nướng (Vietnamese pizza — grilled rice paper with egg, dried shrimp, scallions), chè carts, and more.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Bánh Tráng Nướng Street Stall", description: "Vietnamese pizza — grilled rice paper topped with egg, dried shrimp, scallion oil, chili sauce, and crispy shallots. Cooked over charcoal on the street. Crunchy, savory, smoky. The best street snack in Vietnam. Costs almost nothing.", meta: "15,000 VND ($0.60) · Street stalls · Evening only" }
          ],
          tips: [{ type: "reddit", text: "Bánh tráng nướng (grilled rice paper) is Da Nang's best street snack and it costs like 60 cents. Look for the ladies with charcoal grills on the sidewalk. Don't overthink it — just eat.", cite: "r/VietNam" }]
        }
      ]
    },
    {
      num: 18,
      title: "Day Trip to Hoi An — Revisit & Tailor Pickup",
      neighborhoods: "Hoi An Ancient Town · An Bàng Beach",
      date: "Mar 8",
      mapPins: [
        { lat: 15.8801, lng: 108.3380, label: "Hoi An Ancient Town", num: 1, cat: "activity", desc: "Return visit — new discoveries" },
        { lat: 15.8800, lng: 108.3370, label: "Tailor Shops", num: 2, cat: "activity", desc: "Final fittings and pickup" },
        { lat: 15.9020, lng: 108.3600, label: "An Bàng Beach", num: 3, cat: "activity", desc: "Afternoon beach time" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Return to Hoi An", description: "Day trip back to Hoi An for final tailor pickups and a revisit with fresh eyes. You'll see things you missed the first time — a hidden courtyard, a new food stall, a different angle of light on the lanterns.", details: [] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Hoi An Market Graze", description: "Return to the Central Market for more bánh bèo, white rose dumplings, and cà phê sữa đá. The market vendors will recognize you.", meta: "$2-3" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "An Bàng Beach", description: "Spend the afternoon at An Bàng — beach chairs, cold beers, swimming. You know the drill by now.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Cargo Club", description: "Riverside restaurant with French-Vietnamese cuisine and the best patisserie in Hoi An. The river view tables at lunch are gorgeous. The crème brûlée is legitimately excellent.", meta: "$8-15pp · 107 Nguyễn Thái Học · Walk-in" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Hoi An Sunset & Return", description: "Catch the lanterns lighting up one more time before heading back to Da Nang.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Cao Lầu — One More Time", description: "One final bowl of cao lầu before leaving Hoi An. You can't get it anywhere else.", meta: "35,000 VND" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 19,
      title: "Vietnamese Coffee Culture & Photography",
      neighborhoods: "Various Da Nang",
      date: "Mar 9",
      mapPins: [
        { lat: 16.0550, lng: 108.2200, label: "43 Factory Coffee", num: 1, cat: "food", desc: "Award-winning specialty coffee roaster" },
        { lat: 16.0610, lng: 108.2275, label: "Dragon Bridge", num: 2, cat: "activity", desc: "Daytime photography" },
        { lat: 16.0500, lng: 108.2400, label: "An Thượng Cafés", num: 3, cat: "food", desc: "Café hopping district" },
        { lat: 16.0471, lng: 108.2462, label: "Beach Sunset", num: 4, cat: "activity", desc: "Golden hour photography" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "43 Factory Coffee Roasters", description: "Vietnam's most award-winning specialty coffee roaster — a stunning minimalist space serving single-origin Vietnamese coffees. Vietnam is the world's second-largest coffee producer, and 43 Factory showcases the best of it: Arabica from Đà Lạt, Robusta from the Central Highlands, honey-processed, washed, natural. A coffee education and a beautiful experience.", details: ["📍 43 Factory Coffee · Sơn Trà · Open 7am-10pm", "💡 Try a Vietnamese coffee flight — different regions and processing methods side by side. The baristas are knowledgeable and passionate."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "43 Factory Coffee + Pastry", description: "World-class coffee and simple pastries. This is a coffee-first experience — the drinks are the stars.", meta: "$3-5 · 43 Factory" }
          ],
          tips: [{ type: "tip", text: "Vietnamese coffee culture is distinct from Western third-wave coffee. The traditional phin filter (slow drip) produces a strong, thick brew. Paired with condensed milk (cà phê sữa đá), it's a perfect drink. Both traditions — traditional and specialty — coexist beautifully here." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Photography Walk", description: "With two weeks of visual memories, spend an afternoon on a dedicated photography walk. The Dragon Bridge from various angles, the fish market boats, the colorful buildings, street food vendors in action, the An Thượng neighborhood's murals and café culture. Da Nang is incredibly photogenic.", details: [] },
            { title: "Café Hopping", description: "Hit 2-3 more cafés across the city. Vietnamese café culture is endlessly creative — each place has its own aesthetic and specialty drinks. Try egg coffee, coconut coffee, salt coffee (cà phê muối — a Da Nang/Huế invention with whipped salted cream), and avocado coffee.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Cơm Tấm", description: "Broken rice with grilled pork chop, egg cake, and fish sauce — cơm tấm is a Southern Vietnamese staple that's beloved everywhere. The pork is marinated and grilled until caramelized, the broken rice grains have a unique chewy texture, and the fish sauce ties it all together.", meta: "35,000-50,000 VND · Various locations" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Sunset Photography", description: "End the day at My Khe for golden hour. The clouds, the waves, the silhouettes of fishing boats — February light in Central Vietnam is extraordinary.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Madame Lân", description: "Beautiful Vietnamese restaurant in a renovated heritage building. The presentation is stunning — lotus-wrapped rice, whole roasted duck, seafood hotpot. One of Da Nang's most atmospheric dining rooms.", meta: "$10-20pp · Central Da Nang · Reservations helpful" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 20,
      title: "Yoga, Wellness & Slow Living",
      neighborhoods: "My Khe · An Thượng",
      date: "Mar 10",
      mapPins: [
        { lat: 16.0500, lng: 108.2440, label: "Yoga Studio", num: 1, cat: "activity", desc: "Morning yoga class" },
        { lat: 16.0471, lng: 108.2462, label: "My Khe Beach", num: 2, cat: "activity", desc: "Meditation and swimming" },
        { lat: 16.0490, lng: 108.2400, label: "Spa", num: 3, cat: "activity", desc: "Afternoon wellness" },
        { lat: 16.0520, lng: 108.2430, label: "Healthy Café", num: 4, cat: "food", desc: "Wellness-focused dining" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Morning Yoga & Meditation", description: "Da Nang has a growing wellness scene. Join a morning yoga class at one of the beachfront studios — many offer drop-in classes for $5-10. Some do beach yoga at sunrise. Follow with a meditation session or simply sit on the beach in silence as the waves roll in.", details: ["💡 Nomad Yoga, Zenith Yoga, and Da Nang Yoga are all well-reviewed for drop-in classes."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Healthy Smoothie Bowl", description: "Da Nang's café scene includes excellent healthy options — açaí bowls, smoothie bowls with dragon fruit and granola, fresh juices. A refreshing start after yoga.", meta: "$3-5 · Various cafés in An Thượng" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Deep Spa Session", description: "Book a longer spa treatment today — 2-3 hours of massage, body scrub, herbal steam, and facial. Vietnamese herbal medicine traditions inform many spa treatments here — lemongrass, turmeric, and local herbs are used in wraps and scrubs.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Chay Garden (Vegetarian)", description: "Vietnamese vegetarian restaurants are extraordinary — they create convincing 'meat' dishes from tofu, mushrooms, and soy. Chay restaurants serve mock-meat phở, 'chicken' rice, spring rolls — all plant-based. Try it even if you're not vegetarian. The creativity is impressive.", meta: "$2-4pp · Various chay restaurants" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Sunset & Quiet Evening", description: "Watch the sunset from the beach. Tonight is a quiet one — read, journal, reflect on three weeks of extraordinary experiences. Maybe one more Vietnamese iced coffee.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "La Maison 1888", description: "If you want one splurge dinner — La Maison 1888 at the InterContinental Sun Peninsula is a Pierre Gagnaire restaurant in a stunning French colonial villa on Sơn Trà. Michelin-level French-Vietnamese cuisine with jaw-dropping views. Dress up, get a Grab, and enjoy.", meta: "$80-150pp · InterContinental Sun Peninsula · Reservations essential" }
          ],
          tips: [{ type: "tip", text: "La Maison 1888 is genuinely world-class and would cost 3-4x this price in Europe. If you're going to splurge once on this trip, this is the place." }]
        }
      ]
    },
    {
      num: 21,
      title: "Sơn Trà Sunrise & Market Morning",
      neighborhoods: "Sơn Trà · Central Da Nang",
      date: "Mar 11",
      mapPins: [
        { lat: 16.1250, lng: 108.3050, label: "Sơn Trà Summit", num: 1, cat: "activity", desc: "Sunrise viewpoint" },
        { lat: 16.0678, lng: 108.2208, label: "Cồn Market", num: 2, cat: "food", desc: "Morning market return" },
        { lat: 16.0471, lng: 108.2462, label: "My Khe Beach", num: 3, cat: "activity", desc: "Afternoon relaxation" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Sơn Trà Sunrise", description: "Wake early and drive up Sơn Trà Peninsula for sunrise. From Ban Co Peak, you'll see the sun rise over the South China Sea while Da Nang's coastline glitters below. The early morning light through the jungle canopy is magical. Keep your eyes open for the red-shanked douc langurs — they're most active at dawn.", details: ["💡 Leave by 5am to make it to the top before sunrise. Grab or rent a motorbike."] },
            { title: "Cồn Market Return", description: "Head to Cồn Market for a final market morning. By now you know what to order — bánh bèo, chè, fresh fruit. The vendors might recognize you.", details: [] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Cồn Market Feast", description: "The full spread: rice cakes, steamed dumplings, tropical fruit, Vietnamese coffee. Your last market breakfast — make it count.", meta: "$2-3" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Beach Time", description: "Your second-to-last full day. Spend it where you've spent many — on the beach. My Khe has become familiar now: you know which spot gets the best shade, which vendor has the coldest coconuts, which time the waves are best.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Nem Nướng Bà Hường", description: "Nem nướng — grilled pork sausage rolls. Minced pork is seasoned, wrapped around skewers, grilled until caramelized, then wrapped in rice paper with herbs, pickled vegetables, and a special fermented soybean dipping sauce. Interactive, fun, and delicious.", meta: "40,000-50,000 VND · Central Da Nang · Walk-in" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Farewell Walk", description: "Walk the entire Hàn River promenade one last time. Cross each bridge. Take in the lights, the families, the energy of a city that's growing and thriving.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Hải Sản Bé Mặn (Return)", description: "End where the seafood is — one final feast of grilled prawns, garlic butter clams, and salt-and-pepper crab. With Bia Hoi and the ocean breeze.", meta: "$10-15pp · Võ Nguyên Giáp" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 22,
      title: "Final Beach Day & Souvenir Shopping",
      neighborhoods: "My Khe · Hải Châu",
      date: "Mar 12",
      mapPins: [
        { lat: 16.0471, lng: 108.2462, label: "My Khe Beach", num: 1, cat: "activity", desc: "Final morning swim" },
        { lat: 16.0678, lng: 108.2208, label: "Shopping Area", num: 2, cat: "activity", desc: "Souvenirs and gifts" },
        { lat: 16.0550, lng: 108.2350, label: "Riverside", num: 3, cat: "food", desc: "Farewell dinner area" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Final Beach Morning", description: "One last swim in the South China Sea. One last Vietnamese iced coffee on the sand. The water is warm, the sky is blue, and you've spent 22 days learning to live at Vietnam's pace.", details: [] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Beach Café Breakfast", description: "Leisurely breakfast at your favorite beachfront spot. You have one by now.", meta: "$3-5" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Souvenir Shopping", description: "Pick up final gifts and souvenirs: Vietnamese coffee (buy whole beans at Cồn Market or 43 Factory), silk, lacquerware, conical hats, spices, and artwork. Da Nang's markets are the best value — Hoi An is slightly pricier for the same items.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Mì Quảng — Last Bowl", description: "One final bowl of Da Nang's signature dish. The turmeric noodles, the rich broth, the peanuts and rice crackers. You'll dream about this.", meta: "35,000 VND" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Farewell Dinner", description: "Treat yourself to a special farewell dinner. Reflect on 23 nights of temples, beaches, food, and the gentle kindness of Vietnamese people.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Brilliant Seafood Restaurant", description: "Upscale seafood on the river — whole steamed grouper, butter garlic lobster, seafood hotpot for one. Beautiful setting with bridge views. A fitting finale.", meta: "$20-30pp · Riverside · Reservations helpful" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 23,
      title: "Last Morning & Departure Prep",
      neighborhoods: "My Khe · Airport Area",
      date: "Mar 13",
      mapPins: [
        { lat: 16.0471, lng: 108.2462, label: "My Khe Beach", num: 1, cat: "activity", desc: "Sunrise walk" },
        { lat: 16.0500, lng: 108.2418, label: "An Thượng", num: 2, cat: "food", desc: "Final coffee and breakfast" },
        { lat: 16.0490, lng: 108.2400, label: "Spa", num: 3, cat: "activity", desc: "Pre-flight massage" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Sunrise Beach Walk", description: "Wake up early one final time for a sunrise walk on My Khe. The beach that welcomed you 23 days ago sends you off. The sunrise over the South China Sea is the same view — but you're different now.", details: [] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Favorite Breakfast Spot", description: "Return to whichever breakfast spot became your regular — the bánh mì cart, the phở stall, the café. By now you're a regular and they know your order.", meta: "" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Pre-Flight Massage", description: "One final Vietnamese massage before the long flight home. An hour of relaxation for $10. You'll miss this.", details: [] },
            { title: "Pack & Prepare", description: "Pack up your tailored clothes, souvenirs, coffee beans, and memories. The airport is 15 minutes away — no stress.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Bún Chả Cá — Full Circle", description: "End where you began — with a bowl of bún chả cá, Da Nang's fish cake noodle soup. The same dish from Day 1. The broth tastes different now — richer, more familiar. You know this city.", meta: "25,000 VND ($1) · 109 Nguyễn Chí Thanh" }
          ],
          tips: [{ type: "tip", text: "Da Nang Airport is one of Vietnam's easiest — small, efficient, and close to everything. 1.5 hours before a domestic flight, 2.5 hours for international. Grab to the airport: ~50,000 VND ($2)." }]
        }
      ]
    },
    {
      num: 24,
      title: "Departure Day",
      neighborhoods: "Da Nang Airport",
      date: "Mar 14",
      mapPins: [
        { lat: 16.0544, lng: 108.2022, label: "Da Nang Airport", num: 1, cat: "activity", desc: "Departure" },
        { lat: 16.0471, lng: 108.2462, label: "My Khe Beach", num: 2, cat: "activity", desc: "One last look" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Departure", description: "Check out and head to Da Nang International Airport. If your flight is in the afternoon, squeeze in one more beach walk or market visit. The airport has decent coffee and a few last-chance souvenir shops. You'll be back — 23 days isn't enough when you've fallen in love with a place.", details: ["💡 Grab to airport: 50,000 VND ($2), 15 minutes. Buy duty-free Vietnamese coffee at the airport — Golden Weasel and Trung Nguyên are good brands."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Airport Coffee", description: "One final cà phê sữa đá at the airport. The taste of Vietnam to take with you.", meta: "$2-3 · Airport cafés" }
          ],
          tips: [{ type: "tip", text: "Hẹn gặp lại, Đà Nẵng — see you again. 🇻🇳" }]
        }
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
