const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1771686068692_81hnmo",
  email: "psyduckler@gmail.com",
  destination: "Tulum",
  start_date: "2026-02-21",
  end_date: "2026-02-24",
  group_size: "1",
  travel_style: "",
  dining: "",
  budget: "",
  requests: "",
  amount: "0.00",
  timestamp: "2026-02-21T15:01:08.692Z",
  status: "pending"
};

const itineraryData = {
  destination: "Tulum, Mexico",
  countryEmoji: "🇲🇽",
  title: "Tulum in 3 Nights: Ruins, Cenotes & Caribbean Magic",
  subtitle: "Beach Zone → Pueblo → Cenote Country → Sian Ka'an",
  description: "A solo traveler's guide to Tulum in late February — the sweet spot between high season crowds and oppressive heat. Expect warm days (80-85°F), turquoise Caribbean water, ancient Mayan ruins perched on sea cliffs, otherworldly cenotes hidden in the jungle, and some of the most creative restaurants in Mexico. Tulum rewards the curious and the unhurried.",
  duration: "3 nights / 4 days",
  dates: "Feb 21 – 24, 2026",
  budget: "Moderate",
  pace: "Relaxed — morning adventures, afternoon cenotes & beach, evening dining",
  bestFor: "Solo travelers, nature lovers & foodies",
  highlights: [
    "Tulum Archaeological Zone — Mayan ruins on Caribbean sea cliffs",
    "Gran Cenote — crystal-clear underground swimming with turtles",
    "Cenote Dos Ojos — stunning twin cave system for snorkeling",
    "Tulum Beach — powdery white sand, turquoise water, no crowds in Feb",
    "Sian Ka'an Biosphere Reserve — UNESCO World Heritage jungle & lagoons",
    "Hartwood — legendary open-fire restaurant in the jungle",
    "Pueblo vibes — taco stands, mezcal bars & local life",
    "Cenote Calavera — cliff jumps into a skull-shaped cave",
    "Ahau Tulum beach club — boho chic with the iconic Ven a la Luz sculpture",
    "Matcha Mama & raw food scene — Tulum's wellness culture"
  ],
  essentials: [
    { title: "🚗 Getting Around", text: "Fly into Cancún (CUN), then it's 1.5–2 hours south. Book a private transfer ($80-120 USD) or take an ADO bus ($15 USD, comfortable). In Tulum, rent a bicycle ($8-10/day) for the beach zone, or a scooter ($25-30/day) for cenotes. Taxis exist but overcharge tourists — agree on price before getting in. The beach road is one long strip; the pueblo (town) is 3km inland." },
    { title: "💵 Budget Tips", text: "Tulum has two economies: the Instagram-famous beach zone ($$$$) and the pueblo ($$). Eat lunch at taco stands in town ($3-5), splurge on one jungle dinner ($40-70pp). Cenotes cost $10-25 USD entry. Beach clubs charge $20-50 minimum spend. February is high season — book restaurants 2-3 days ahead. Pesos get better prices than USD at local spots." },
    { title: "☀️ February Weather", text: "Perfect timing. 80-85°F (27-30°C) during the day, 68-72°F (20-22°C) at night. Low humidity, rare rain, and the Caribbean is warm enough for swimming. UV is intense — SPF 50 and reef-safe sunscreen are mandatory (regular sunscreen is banned at cenotes). Bring a light layer for evenings and jungle mosquito protection." },
    { title: "🏨 Where to Stay", text: "Beach Zone for the classic Tulum experience — boutique hotels, jungle-meets-ocean vibes, but pricey ($150-400/night). Pueblo (town) for budget-friendly stays with local character ($30-80/night), a 10-min bike ride to the beach. La Veleta neighborhood (between pueblo and beach) is a great middle ground — newer, quieter, walkable to both zones." },
    { title: "🤿 Cenote Tips", text: "Tulum has 6,000+ cenotes within an hour's drive. Go early (8-9am) to beat crowds and get the magical light. Bring a waterproof phone case. No chemical sunscreen allowed — rinse off before entering. Some cenotes require cash (pesos). Snorkel gear is usually included in entry or rentable for $5. If you only visit one: Gran Cenote." },
    { title: "📱 Useful Apps", text: "Google Maps (works well in Tulum), WhatsApp (how Mexico communicates — restaurants and tours book via WhatsApp), Uber (works from CUN airport but not in Tulum itself), Wise or Revolut (best exchange rates), iNaturalist (identify jungle wildlife and plants at Sian Ka'an)." }
  ],
  days: [
    {
      num: 1,
      title: "Tulum Ruins, Beach Zone & Sunset",
      neighborhoods: "Archaeological Zone · Beach Zone · Playa Paraíso",
      date: "Feb 21",
      mapPins: [
        { lat: 20.2145, lng: -87.4291, label: "Tulum Ruins", num: 1, cat: "activity", desc: "Mayan clifftop ruins overlooking the Caribbean" },
        { lat: 20.2082, lng: -87.4350, label: "Playa Ruinas", num: 2, cat: "activity", desc: "Beach below the ruins — stunning turquoise water" },
        { lat: 20.2020, lng: -87.4370, label: "Playa Paraíso", num: 3, cat: "activity", desc: "Tulum's most iconic beach" },
        { lat: 20.1930, lng: -87.4410, label: "Ahau Tulum", num: 4, cat: "activity", desc: "Ven a la Luz sculpture & beach club" },
        { lat: 20.1990, lng: -87.4390, label: "Matcha Mama", num: 5, cat: "food", desc: "Famous smoothie shack on the beach road" },
        { lat: 20.2115, lng: -87.4620, label: "Tulum Pueblo", num: 6, cat: "food", desc: "Local taco stands and mezcal bars" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Tulum Archaeological Zone", description: "Arrive at the ruins right at opening (8am) to beat the tour bus crowds. The Tulum ruins are the only major Mayan site built on a Caribbean sea cliff — El Castillo perched above turquoise water is one of Mexico's most iconic images. The walled city was a major trading port for Cobá, occupied from the 13th-15th century. Walking through the compact site takes about an hour. The views from the cliff edge are absolutely unreal — endless shades of blue stretching to the horizon.", details: ["📍 Carretera Federal 307, Km 230 · $85 MXN (~$5 USD) entry · Opens 8am", "💡 Go at 8am sharp. By 10am, tour buses from Cancún arrive and it gets packed. Hire a guide at the entrance ($40 USD) for context — they're excellent and the history is fascinating."] },
            { title: "Playa Ruinas", description: "After exploring the ruins, take the wooden staircase down to Playa Ruinas — the small beach directly below the archaeological site. Swimming here with ancient Mayan temples on the cliff above you is surreal. The water is impossibly clear and warm. This beach is small and fills up fast, so enjoy it early.", details: ["💡 Bring your swimsuit and a towel. There are no facilities on Playa Ruinas — just sand, sea, and ruins above. Magical."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Burrito Amor (Pueblo)", description: "The best breakfast in Tulum Pueblo. Fresh-pressed juices, chilaquiles that'll change your life, and breakfast burritos stuffed with local ingredients. Colorful, casual, and packed with locals and in-the-know travelers. The café de olla (traditional cinnamon-spiced Mexican coffee) is perfect.", meta: "$8-14 USD · Tulum Pueblo, Av. Satelite · Walk-in, opens 8am" }
          ],
          tips: [{ type: "tip", text: "Tulum ruins are compact — 1-1.5 hours is plenty. Wear comfortable shoes, bring water, and don't forget sunscreen. The site has little shade. The path from the entrance to the ruins is about a 10-minute walk (or $2 for a tram ride)." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Beach Zone Exploration", description: "Bike or taxi down the Tulum beach road — a sandy, jungled strip lined with boutique hotels, beach clubs, yoga studios, and restaurants. Stop at Playa Paraíso, consistently rated one of Mexico's most beautiful beaches: powdery white sand, shallow turquoise water, palm trees swaying. In February, it's warm but not scorching — perfect for a long afternoon of swimming and reading.", details: ["📍 Playa Paraíso is at the north end of the beach zone, closest to the ruins", "💡 Bring cash for beach chairs ($10-15 USD) or skip them and lay out a towel. The water is shallow and warm — you can wade out 50 meters and it's still waist-deep."] },
            { title: "Ahau Tulum & Ven a la Luz", description: "Walk south along the beach road to Ahau Tulum, home of the iconic Ven a la Luz ('Come to the Light') sculpture by Daniel Popper — a towering 10-meter figure with a portal through its chest, covered in climbing plants. It's Tulum's most photographed landmark. The beach club is mellow — grab a daybed, order a mezcal cocktail, and watch the afternoon unfold.", details: ["📍 Beach Road Km 7.5 · Minimum spend ~$30-50 USD for a daybed", "💡 Best light for Ven a la Luz photos is late afternoon when the sun filters through the sculpture's opening."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Matcha Mama", description: "The most Instagrammed spot on the beach road — and it actually delivers. Acai bowls, matcha lattes, smoothies loaded with tropical fruit. The wooden treehouse-style structure is adorable. A perfect light lunch between beach sessions. Solo travelers love the communal picnic-table vibe.", meta: "$10-15 USD · Beach Road · Walk-in, expect a short line" }
          ],
          tips: [{ type: "reddit", text: "The beach zone in February is peak season but not crazy packed like December. You can still find open spots on Playa Paraíso. The beach clubs south of the ruins are where the Instagram crowd goes; north of the ruins is way more chill and local.", cite: "r/tulum" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Tulum Pueblo Sunset Stroll", description: "Head into Tulum Pueblo for the evening. The town has transformed from a dusty highway stop into a vibrant food scene. Walk down Avenida Tulum — the main strip lined with taco stands, mezcalerías, and local shops. The energy is completely different from the beach zone: more Mexican, more real, more affordable. Perfect for a solo wanderer.", details: ["💡 The pueblo is where locals eat and drink. Prices are 50-70% less than the beach zone for comparable quality."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Taquería La Eufemia (Pueblo)", description: "No-frills taquería that's become legendary among travelers. Al pastor tacos with fresh pineapple, handmade tortillas, grilled onions, and every salsa you can imagine. Sit at plastic tables under string lights and eat some of the best tacos of your life. Cold Modelo or michelada to wash it down. This is the real Tulum.", meta: "$5-10 USD · Pueblo · Walk-in, cash preferred" }
          ],
          tips: [{ type: "reddit", text: "Skip the $25 tacos on the beach road. Go to the pueblo and eat at the stands on the main street. La Eufemia, Antojitos La Chiapaneca, or any stand with a crowd of locals — that's where the real food is. You'll eat like a king for $10.", cite: "r/tulum" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Mezcal at Batey", description: "End the night at Batey — a mezcal bar in the pueblo built around a vintage VW Beetle. Live music most nights, incredible mezcal cocktails (try the mezcal mojito or the smoke old fashioned), and a crowd that's equal parts local and traveler. The outdoor courtyard string-light vibe is exactly what a Tulum night should feel like. Solo travelers fit right in at the bar.", details: ["📍 Centauro Sur, between Av. Tulum and the highway · Open until late", "💡 Order a mezcal flight to try different agave varieties. The bartenders are passionate and love explaining the differences."] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 2,
      title: "Cenote Day: Gran Cenote, Dos Ojos & Calavera",
      neighborhoods: "Cenote Country · Jungle Roads · Beach Zone",
      date: "Feb 22",
      mapPins: [
        { lat: 20.2469, lng: -87.4640, label: "Gran Cenote", num: 1, cat: "activity", desc: "Crystal-clear open cenote with turtles" },
        { lat: 20.2427, lng: -87.3937, label: "Cenote Dos Ojos", num: 2, cat: "activity", desc: "Twin-cave cenote system, incredible snorkeling" },
        { lat: 20.2310, lng: -87.4540, label: "Cenote Calavera", num: 3, cat: "activity", desc: "Skull-shaped cave with cliff jumps" },
        { lat: 20.2080, lng: -87.4605, label: "La Zebra Beach", num: 4, cat: "food", desc: "Beach restaurant with live music Saturdays" },
        { lat: 20.2050, lng: -87.4400, label: "Hartwood", num: 5, cat: "food", desc: "Legendary open-fire jungle restaurant" },
        { lat: 20.2116, lng: -87.4618, label: "Tulum Pueblo Center", num: 6, cat: "food", desc: "Morning coffee and provisions" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Gran Cenote", description: "Start early at Gran Cenote — Tulum's most famous cenote, and for good reason. A half-open limestone cave with crystal-clear turquoise water so transparent you can see 30 meters to the bottom. Swim through a cavern opening into an open-air pool surrounded by jungle. Freshwater turtles glide beneath you. Stalactites hang from the cave ceiling. The morning light filtering into the cave is genuinely otherworldly. Arrive right at 8am opening — by 10am it's crowded.", details: ["📍 4km west of Tulum on the road to Cobá · $300 MXN (~$18 USD) entry", "💡 Rinse off all sunscreen before entering (required). Bring a waterproof phone case. Snorkel gear included in entry. The early morning light creates beams through the cave opening — photographers, you want to be here at 8am."] },
            { title: "Cenote Calavera", description: "A 5-minute drive from Gran Cenote. Cenote Calavera ('Skull Cenote') is a collapsed cave with three holes in the top that look like a skull's eyes and mouth from above. You climb down a ladder (or jump 3-5 meters through the holes, if brave). Inside is a cathedral-sized cave with deep blue water. Far less crowded than Gran Cenote — you might have it to yourself on a weekday morning.", details: ["📍 On the Cobá road, 1km past Gran Cenote · $250 MXN (~$15 USD)", "💡 The cliff jumps are 3m and 5m. The water is deep (10m+) and safe to jump into. But always check the entry point — don't be the person who slips on the wet rock. Lockers available."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Ki'BOK Coffee & Bakery (Pueblo)", description: "Locally roasted coffee from Chiapas beans, house-baked pastries, and healthy bowls. A calm, aesthetic café that's perfect for a solo morning before cenote adventures. The cold brew is excellent and they have good WiFi if you need to plan your route.", meta: "$6-10 USD · Tulum Pueblo · Walk-in, opens 7am" }
          ],
          tips: [{ type: "reddit", text: "Do Gran Cenote first thing in the morning. I went at 8am and had maybe 10 people there. Went back at noon another day and it was a zoo. The turtles are more active in the morning too. Bring your own snorkel if you have one — the rental ones fog up.", cite: "r/tulum" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Cenote Dos Ojos", description: "Drive 20 minutes north to Cenote Dos Ojos ('Two Eyes') — part of one of the world's longest underwater cave systems (Sac Actun, 380+ km). Two connected cenotes: the first eye is wide open with stunning stalactites and shallow turquoise water perfect for snorkeling; the second eye is darker, deeper, and more adventurous. The underground cathedral formations are millions of years old. This is the cenote that makes you understand why the Maya considered them sacred portals to the underworld.", details: ["📍 Off Highway 307, north of Tulum · $400 MXN (~$24 USD) entry with snorkel", "💡 Do both eyes — they're different experiences. The first is bright and photogenic, the second is moody and cave-like. Diving is available ($60-80 USD) for certified divers — the cave system is world-class."] },
            { title: "Beach Afternoon", description: "After three cenotes, you've earned a lazy beach afternoon. Head to the quieter southern end of the beach zone — fewer crowds, same stunning water. Rent a lounger, swim in the Caribbean, read a book, decompress. February's golden afternoon light on the turquoise water is pure therapy.", details: ["💡 The beach south of the main hotel strip (past Ahau, toward Sian Ka'an) is wider, quieter, and just as beautiful. Some stretches are nearly empty in February."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Cenote Dos Ojos Restaurant", description: "Simple Mexican food at the cenote park — tacos, quesadillas, fresh fruit, cold drinks. Nothing fancy but exactly what you need between swims. Eat under a palapa roof surrounded by jungle. Fresh-squeezed orange juice is mandatory.", meta: "$8-12 USD · At the cenote park · Cash preferred" }
          ],
          tips: [{ type: "tip", text: "Cenote circuit plan: Gran Cenote (8am) → Calavera (9:30am) → Dos Ojos (11:30am). All three in one morning is doable. Drive or take a colectivo. If you rent a scooter, the jungle roads between cenotes are beautiful but watch for potholes." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Hartwood Dinner", description: "Tonight is the night for Hartwood — Tulum's most legendary restaurant and a defining experience of the Riviera Maya food scene. Chef Eric Werner cooks entirely over open fire and wood, with no gas, no electricity in the kitchen. The menu changes daily based on what's available from local fishermen, farmers, and foragers. Expect wood-roasted octopus, jungle-herb salads, whole grilled fish, and smoky mezcal cocktails. The open-air jungle setting, fire crackling, stars above — it's unforgettable.", details: ["📍 Beach Road Km 7.6 · Book on Instagram DM or WhatsApp weeks in advance", "💡 Hartwood books up fast. Message their Instagram at least 1-2 weeks ahead. If you can't get a reservation, show up at 5:30pm and put your name on the walk-in list. Solo diners often get seated at the bar — which is actually the best seat in the house."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Hartwood", description: "Open-fire cooking in the jungle. Daily changing menu sourced from local fishermen and farmers. The octopus, whatever fish they have, and the wood-roasted vegetables are always extraordinary. Mezcal cocktails are outstanding. The experience — eating fire-cooked food under the stars in the Yucatán jungle — is as important as the food itself. One of the most memorable meals you'll have anywhere.", meta: "$45-70 USD · Beach Road · Reservations essential (Instagram/WhatsApp)" }
          ],
          tips: [{ type: "reddit", text: "Hartwood is not overhyped. It's genuinely one of the best dining experiences in Mexico. Book ahead or go for the walk-in list. Solo at the bar is actually ideal — you can watch them cook over the fire. The mezcal negroni is insane.", cite: "r/foodie" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Beach Road Night Stroll", description: "Walk the beach road at night — it transforms after dark. Fairy lights in the jungle, the sound of waves, live music drifting from restaurants. Some hotels and bars have bonfires on the beach. Tulum's beach road at night is one of the most atmospheric walks in Mexico. Bioluminescence is sometimes visible in the waves in February — look for a blue-green glow in the surf.", details: ["💡 Papaya Playa Project often has DJ nights and beach parties on weekends. Check their Instagram for the schedule."] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 3,
      title: "Sian Ka'an Biosphere & Southern Tulum",
      neighborhoods: "Sian Ka'an · Muyil · Southern Beach Zone",
      date: "Feb 23",
      mapPins: [
        { lat: 20.1320, lng: -87.4685, label: "Sian Ka'an Entrance", num: 1, cat: "activity", desc: "UNESCO Biosphere Reserve entrance" },
        { lat: 20.0800, lng: -87.6100, label: "Muyil Ruins & Lagoon", num: 2, cat: "activity", desc: "Mayan ruins + floating canal to lagoon" },
        { lat: 20.1100, lng: -87.4800, label: "Sian Ka'an Lagoon", num: 3, cat: "activity", desc: "Float through mangrove channels" },
        { lat: 20.1500, lng: -87.4600, label: "Punta Allen Road", num: 4, cat: "activity", desc: "Scenic dirt road through the reserve" },
        { lat: 20.1950, lng: -87.4420, label: "Casa Jaguar", num: 5, cat: "food", desc: "Jungle restaurant with a cenote" },
        { lat: 20.2000, lng: -87.4400, label: "Arca", num: 6, cat: "food", desc: "Modern Mexican tasting menu" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Sian Ka'an Biosphere Reserve", description: "Today is for Tulum's crown jewel: the Sian Ka'an Biosphere Reserve — a 1.3 million-acre UNESCO World Heritage site of jungle, wetlands, mangroves, and Caribbean coast that starts right where Tulum's beach zone ends. Book a guided tour (essential — the reserve is vast and guides know where to find wildlife). You'll drive down a bumpy dirt road through the reserve, stopping at ancient Mayan canals, floating through mangrove channels in the current, and spotting dolphins, manatees, crocodiles, and hundreds of bird species.", details: ["📍 Entrance at the south end of Tulum Beach Road · Tours $80-120 USD pp", "💡 Book with Community Tours Sian Ka'an — a local cooperative that employs Mayan community members as guides. They're the most knowledgeable and ethical operator. Book via WhatsApp at least 2-3 days ahead."] },
            { title: "Muyil Ruins & Floating Canals", description: "An alternative (or addition) to the coastal Sian Ka'an tour: drive 25 minutes south to Muyil — a small, uncrowded Mayan site surrounded by jungle. After exploring the ruins (look for the tall pyramid peeking above the canopy), take the boardwalk to Muyil Lagoon and float 1km down an ancient Mayan canal through the mangroves. The current carries you gently — no swimming required. It's peaceful, surreal, and a fraction of the cost of the main Sian Ka'an tour.", details: ["📍 Muyil ruins: Highway 307, 25 min south of Tulum · $85 MXN ruins + ~$500 MXN float", "💡 This can be done independently (no tour needed). The float through the mangrove canal is one of Tulum's most underrated experiences."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Chamico's (Pueblo)", description: "Local breakfast spot where construction workers and fishermen eat alongside travelers. Huevos motuleños (eggs on tortilla with black beans, plantain, ham, and tomato sauce — a Yucatecan classic), fresh-squeezed juices, and café de olla. Authentic, filling, and under $6.", meta: "$4-7 USD · Pueblo · Walk-in, opens early" }
          ],
          tips: [{ type: "reddit", text: "Sian Ka'an is the #1 thing to do in Tulum that most tourists skip. The floating through Mayan canals surrounded by mangroves with zero people around is otherworldly. Book Community Tours Sian Ka'an — they're the best. Muyil is the budget-friendly alternative and equally magical.", cite: "r/tulum" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Last Beach Afternoon", description: "Return from Sian Ka'an in the early afternoon and soak up your last full beach session. The southern end of the beach zone, closest to Sian Ka'an, is the most pristine and least developed stretch. Caribbean water, white sand, palm trees, maybe a coconut from a beach vendor. This is the Tulum that everyone comes for. Soak it in.", details: ["💡 If the sargassum (seaweed) is minimal (February is usually good), this stretch of beach is absolutely world-class. If there is sargassum, head slightly north — hotels clear their sections daily."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Casa Jaguar", description: "A jungle restaurant built around a cenote. Yes, a cenote inside a restaurant. Swim in the private cenote before lunch, then sit under the palapa roof and eat wood-fired seafood, ceviche, and guacamole made tableside. The setting is absolutely ridiculous — jungle, cenote, fire, food. One of those only-in-Tulum experiences.", meta: "$25-40 USD · Beach Road Km 7.5 · Reservations recommended, walk-ins sometimes possible" }
          ],
          tips: [{ type: "tip", text: "February is one of the best months for sargassum-free beaches in Tulum. The heavy seaweed season is typically May-September. You should have clear, turquoise water." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Farewell Dinner at Arca", description: "For your last Tulum dinner, treat yourself to Arca — one of the most exciting restaurants in Mexico right now. Chef José Luis Hinostroza creates modern Mexican tasting menus using Yucatecan ingredients cooked over wood and fire. The space is stunning: an open-air concrete structure in the jungle with a dramatic central fire pit. Expect dishes like wood-roasted cacao-glazed pork, smoked fish tostadas, and corn in ways you've never imagined. A fitting finale.", details: ["📍 Beach Road · Tasting menu ~$70-90 USD · Reservations essential (Resy or WhatsApp)", "💡 The cocktail program is incredible — the mezcal-based drinks with local citrus and herbs are some of the best in Tulum. Solo diners get excellent treatment at the bar."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Arca", description: "Modern Mexican tasting menu in a dramatic jungle setting. Wood-fire cooking, Yucatecan ingredients, creative and beautiful plates. The atmosphere alone — fire, concrete, jungle — is worth the visit. One of the defining restaurants of the Riviera Maya's current golden age.", meta: "$70-90 USD tasting menu · Beach Road · Reservations essential" }
          ],
          tips: [{ type: "reddit", text: "Arca blew my mind. The tasting menu is a journey. Every course tells a story about Yucatecan ingredients. If Hartwood is the classic Tulum restaurant experience, Arca is the next generation. Don't skip the cocktails.", cite: "r/mexicofood" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Beach Bonfire & Stars", description: "Your last Tulum night. Walk down to the beach. Many hotels leave bonfire pits burning, and the beach is public. Sit by the fire, listen to the waves, look up at the Milky Way (Tulum's beach zone has relatively low light pollution, especially toward Sian Ka'an). The Maya called this coast Zamá — 'Place of the Dawn.' Tomorrow you'll understand why.", details: ["💡 Bring a mezcal from the pueblo ($15-20 for a good bottle) and enjoy it on the beach. The southern end near Sian Ka'an has the darkest skies and best stargazing."] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 4,
      title: "Sunrise, Last Swim & Departure",
      neighborhoods: "Beach Zone · Pueblo · Highway 307",
      date: "Feb 24",
      mapPins: [
        { lat: 20.2020, lng: -87.4370, label: "Sunrise Beach", num: 1, cat: "activity", desc: "Caribbean sunrise — the Place of the Dawn" },
        { lat: 20.2116, lng: -87.4618, label: "Tulum Pueblo", num: 2, cat: "food", desc: "Final breakfast in town" },
        { lat: 20.2145, lng: -87.4291, label: "Beach near Ruins", num: 3, cat: "activity", desc: "One last swim in the Caribbean" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Caribbean Sunrise", description: "Wake up early for a Tulum sunrise. The ancient Maya chose this coast because it faces east — directly into the rising sun. The sunrise over the Caribbean is spectacular: the sky goes from deep purple to pink to gold, and the first light hits the turquoise water like a switch being flipped. Walk to the beach, sit in the sand, and watch the Place of the Dawn do its thing. This is the moment that stays with you long after you leave.", details: ["💡 Sunrise in late February is around 6:45am. The beach is nearly empty at this hour. Bring your coffee."] },
            { title: "Last Swim & Farewell", description: "Take a final swim in the Caribbean. The morning water is calm, warm, and impossibly clear. Float on your back, look at the sky, and mentally bookmark this moment. Then head into the pueblo for a last breakfast before your transfer to the airport.", details: [] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Burrito Amor (Pueblo)", description: "Come full circle — end where you started. The chilaquiles, the café de olla, the colorful murals. Pick up a couple of tamales for the road. A final taste of Tulum before the ride north to Cancún.", meta: "$8-14 USD · Pueblo · Walk-in" }
          ],
          tips: [{ type: "tip", text: "Allow 2-2.5 hours for the drive to Cancún airport. ADO buses depart regularly from the Tulum bus station ($15 USD, comfortable, WiFi). Private transfers are $80-120 and more convenient. Book the night before via WhatsApp with your hotel or a local driver." }]
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
