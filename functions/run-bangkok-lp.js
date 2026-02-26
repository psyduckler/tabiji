const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1772114861900_l3cm0s",
  email: "sophieslot@hotmail.com",
  destination: "Bangkok and Luang Prabang",
  start_date: "2026-05-08",
  end_date: "2026-05-17",
  group_size: "2",
  travel_style: "Adventure, Cultural, Foodie, Relaxation",
  dining: "Mix of everything",
  budget: "$1,000-2,000",
  requests: "A 2 days one night boat trip over Mekong from northern Thailand to Luang Prabang. Some time for chill reading.",
  amount: "0.00",
  timestamp: "2026-02-26T14:07:41.900Z",
  status: "pending"
};

const itineraryData = {
  destination: "Bangkok & Luang Prabang",
  countryEmoji: "🇹🇭🇱🇦",
  title: "9 Nights: Bangkok, the Mekong Slow Boat & Luang Prabang",
  subtitle: "Street Food Capital → Northern Thailand → 2-Day Mekong River Journey → UNESCO Heritage Town",
  description: "Two of Southeast Asia's most magnetic destinations connected by its most legendary journey — the Mekong slow boat. Start in Bangkok's sensory overload of temples, markets, and world-class street food. Fly north to Chiang Rai's artistic edge. Then cross into Laos for the iconic 2-day slow boat down the Mekong through pristine jungle and limestone karst to Luang Prabang — a place so serene, so perfectly preserved, that UNESCO protected the entire town. End with three unhurried days of monk processions at dawn, riverside reading, Lao coffee, and waterfall swims. This trip is equal parts adventure and deep relaxation.",
  duration: "9 nights / 10 days",
  dates: "May 8–17, 2026",
  budget: "$1,000–2,000 for two",
  pace: "Balanced — active city days, slow river travel, lazy Luang Prabang afternoons",
  bestFor: "Adventure couples, cultural explorers & food lovers who want to unplug",
  highlights: [
    "Bangkok's Grand Palace, Wat Pho & the reclining Buddha",
    "Chinatown's legendary street food — the best food street in the world",
    "Chatuchak Weekend Market — 15,000+ stalls of organized chaos",
    "The 2-day Mekong slow boat from Huay Xai to Luang Prabang through untouched jungle",
    "Pak Beng — a one-street river town perched on a hillside, your overnight stop",
    "Luang Prabang's morning alms giving ceremony — 600 monks in saffron robes at dawn",
    "Kuang Si Falls — turquoise cascading pools in the jungle",
    "Luang Prabang Night Market — handwoven textiles, Lao silk, and handmade paper",
    "Joma Bakery Café & riverside spots — perfect reading nooks",
    "Lao cuisine — sticky rice, laap, khao piak sen, and Beerlao at sunset"
  ],
  essentials: [
    { title: "✈️ Getting There & Between", text: "Fly into Bangkok's Suvarnabhumi (BKK) or Don Mueang (DMK). After Bangkok, take a domestic flight to Chiang Rai (CEI) — about 1h20m, $30-60 on AirAsia or Nok Air. From Chiang Rai, a bus or minivan to the Thai-Lao border at Chiang Khong takes 1.5 hours. Cross the Friendship Bridge to Huay Xai for the slow boat. Return flight: Luang Prabang (LPQ) has direct flights to Bangkok on Bangkok Airways and Lao Airlines (~1h40m, $80-150)." },
    { title: "💵 Budget Reality", text: "Thailand and Laos are extremely affordable. Bangkok: street food $1-3, nice dinner $10-20, BTS/MRT rides $0.50-1.50, tuk-tuk negotiable $2-5. Laos: even cheaper. Slow boat ticket: ~$25-35/person. Luang Prabang meal: $3-8. Budget hotel: $15-30/night. A couple can comfortably do this entire trip for $1,000-2,000 including internal flights, with plenty of great food and comfortable rooms." },
    { title: "🌧️ May Weather", text: "May is the start of the wet season in both countries. Expect hot and humid days (85-95°F / 30-35°C) with afternoon thunderstorms that usually clear within an hour. Mornings are often sunny and gorgeous. The upside: fewer tourists, lush green landscapes, dramatic skies, and the Mekong is full and flowing beautifully. Pack a light rain jacket and embrace it." },
    { title: "🚢 Slow Boat Essentials", text: "The public slow boat departs Huay Xai around 11am and arrives Pak Beng around 5-6pm (Day 1), then Pak Beng 9am to Luang Prabang ~5pm (Day 2). Buy tickets at the boat landing or through your Chiang Khong guesthouse. Bring snacks, water, a book (essential!), a cushion or scarf to sit on, and sunscreen. The boat has basic wooden seats — some with cushions, some without. Sit on the left side for the best views. There's a small bar selling Beerlao and snacks." },
    { title: "📱 Connectivity", text: "Get a Thai SIM at Bangkok airport (AIS or TrueMove, ~$5-10, 30 days). In Laos, buy a Unitel SIM at the border crossing or in Luang Prabang ($2-5). WiFi is available in most hotels and cafes in Bangkok and Luang Prabang, but expect to be mostly offline during the slow boat — which is the whole point." },
    { title: "💱 Currency", text: "Thailand uses Thai Baht (THB), Laos uses Lao Kip (LAK). In Laos, Thai Baht and USD are widely accepted for larger purchases. ATMs available everywhere in Bangkok and Luang Prabang. Carry some cash for the slow boat, Pak Beng, and Lao markets. Credit cards accepted at upscale places only." },
    { title: "📚 Packing for Reading", text: "You asked for chill reading time — you'll get it. The slow boat (12+ hours of river), Luang Prabang's cafes, and hammocks by the Mekong are perfect reading environments. Load up your Kindle or bring 2-3 paperbacks. Joma Bakery, Le Banneton, and Utopia Bar in Luang Prabang are legendary reading spots with river views." }
  ],
  days: [
    {
      num: 1,
      title: "Arrive in Bangkok",
      neighborhoods: "Rattanakosin · Khao San",
      date: "May 8",
      mapPins: [
        { lat: 13.6900, lng: 100.7501, label: "Suvarnabhumi Airport", num: 1, cat: "transport", desc: "Bangkok's main international airport" },
        { lat: 13.7510, lng: 100.4927, label: "Wat Pho", num: 2, cat: "attraction", desc: "Temple of the Reclining Buddha" },
        { lat: 13.7563, lng: 100.4920, label: "Khao San Road area", num: 3, cat: "activity", desc: "Backpacker hub and street food" },
        { lat: 13.7411, lng: 100.5067, label: "Tha Tien Pier", num: 4, cat: "activity", desc: "Cross-river ferry to Wat Arun" }
      ],
      timeBlocks: [
        {
          label: "Afternoon",
          activities: [
            { title: "Arrive & Settle In", description: "Land at Suvarnabhumi, grab the Airport Rail Link ($1.50) to the city, and check into your hotel. The Rattanakosin/Old City area puts you walking distance from Bangkok's greatest hits. Freshen up and head out — Bangkok rewards the jetlagged with sensory overload that resets your clock.", details: ["💡 Airport Rail Link runs to Phaya Thai station. Transfer to BTS Skytrain for most destinations. Total cost under $2."] },
            { title: "Wat Pho — Temple of the Reclining Buddha", description: "Your first Thai temple should be the best one. Wat Pho is home to the 46-meter gold-leaf reclining Buddha — one of the largest in the world — resting in a hall that barely contains it. Beyond the main attraction, the temple complex is Bangkok's oldest and largest, with over 1,000 Buddha images, beautiful stupas covered in Chinese porcelain, and the birthplace of traditional Thai massage. Late afternoon is the magic hour: golden light, thinner crowds, serene atmosphere.", details: ["📍 2 Sanamchai Rd · 300 THB ($8.50) · Open 8am-6:30pm", "💡 Dress modestly: cover knees and shoulders. Sarongs available for rent at entrance."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Pad Thai Thip Samai", description: "Bangkok's most famous pad Thai — and it earns it. Thip Samai has been wrapping stir-fried rice noodles in a delicate egg crepe since 1966. Order the 'superb' version (pad thai wrapped in egg) and a fresh-squeezed orange juice. There's always a line but it moves fast. This is the meal that sets the tone for your entire Bangkok food experience.", meta: "60-80 THB ($1.70-2.30) · 313 Mahachai Rd · Open 5pm-2am · Expect a line" }
          ],
          tips: [{ type: "tip", text: "Bangkok is a walking city only in specific neighborhoods. Between neighborhoods, use the BTS Skytrain, MRT subway, river boats, or Grab. Never take a tuk-tuk that 'offers you a deal' near tourist temples — it's always a scam that routes through gem shops." }]
        }
      ]
    },
    {
      num: 2,
      title: "Grand Palace, Temples & Chinatown",
      neighborhoods: "Rattanakosin · Yaowarat (Chinatown)",
      date: "May 9",
      mapPins: [
        { lat: 13.7500, lng: 100.4914, label: "Grand Palace", num: 1, cat: "attraction", desc: "Thailand's most sacred site and former royal residence" },
        { lat: 13.7437, lng: 100.4888, label: "Wat Arun", num: 2, cat: "attraction", desc: "Temple of Dawn — iconic riverside spire" },
        { lat: 13.7387, lng: 100.5133, label: "Yaowarat Road (Chinatown)", num: 3, cat: "food", desc: "Bangkok's legendary street food strip" },
        { lat: 13.7466, lng: 100.5098, label: "Pak Khlong Talat (Flower Market)", num: 4, cat: "activity", desc: "24-hour flower market" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "The Grand Palace", description: "Thailand's most dazzling, overwhelming, absolutely must-see attraction. This 218,000 sq meter complex was the home of Thai kings for 150 years. Inside: Wat Phra Kaew (Temple of the Emerald Buddha — the most sacred Buddhist site in Thailand), gilded spires, mirrored mosaics, mythological guardians, and architecture that defies belief. Every surface glitters. Every detail is intentional. Go at 8:30am opening to beat the worst crowds.", details: ["📍 Na Phra Lan Rd · 500 THB ($14) · Open 8:30am-3:30pm · Strict dress code", "💡 Wear long pants, closed-toe shoes, and covered shoulders. They will turn you away. No exceptions."] },
            { title: "Wat Arun — Temple of Dawn", description: "Cross the river by ferry (4 THB / $0.12) from Tha Tien pier to Wat Arun. This riverside temple is Bangkok's most photographed landmark — a 70-meter Khmer-style spire encrusted with thousands of pieces of Chinese porcelain and colored glass that sparkle in the sunlight. Climb the steep stairs partway up for sweeping river views. Despite the name, it's actually more spectacular in the afternoon light.", details: ["📍 158 Wang Doem Rd · 100 THB ($2.85) · Cross-river ferry from Tha Tien pier", "💡 The ferry ride itself is a highlight — 3 minutes across the Chao Phraya with Wat Arun growing larger before you."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Joke (Thai Rice Porridge)", description: "Start your morning like a Thai local: joke (jok) is silky, thick rice porridge topped with a soft-boiled egg, minced pork, ginger, fried garlic, and white pepper. Comforting, warming, and perfect before a morning of temple walking. Any street cart near your hotel will have it.", meta: "35-50 THB ($1-1.50) · Street vendors everywhere · Morning" }
          ],
          tips: [{ type: "tip", text: "The Grand Palace + Wat Pho + Wat Arun triangle is Bangkok's cultural heart. All three are within walking/short ferry distance of each other. Do them in one morning to maximize energy and beat afternoon heat." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Pak Khlong Talat & Afternoon Rest", description: "Walk through Bangkok's 24-hour flower market — mountains of jasmine garlands, roses, orchids, and marigolds used in temple offerings. The colors and fragrance are intoxicating. Then head back to your hotel for a proper Thai massage (300-500 THB / $8.50-14 for a full hour) and cool down during peak heat.", details: ["📍 Chak Phet Rd · Free · Most photogenic pre-dawn but beautiful anytime"] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Nai Mong Hoi Tod", description: "Chinatown's legendary oyster omelette — crispy-edged, eggy, stuffed with fat plump oysters and beansprouts, served with a spicy-sweet chili sauce. This tiny shop on Plaeng Nam Road has been doing one thing perfectly for decades. Pair with a cold Singha.", meta: "80-120 THB ($2.30-3.40) · 539 Plaeng Nam Rd · Lunch-dinner" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Yaowarat Road — Chinatown Street Food", description: "This is it. The main event. Yaowarat Road at night is arguably the greatest street food experience on earth. The neon signs glow red and gold, smoke rises from wok stations, and hundreds of vendors line both sides of the street serving everything: grilled seafood platters on folding tables, roast duck over rice, ba mee noodles, mango sticky rice, rolled ice cream, and dim sum. Walk slowly. Eat everything. This is Bangkok at its most alive.", details: ["📍 Yaowarat Road · Most stalls open 5pm-midnight · Come hungry", "💡 Don't fill up on the first stall. Walk the entire stretch first to scout, then double back to your favorites. Bring cash — no cards accepted."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "T&K Seafood + Yaowarat Grazing", description: "Park yourself at T&K (the one with green-shirted staff) for their famous tom yum goong — huge river prawns in a searingly hot-sour broth — and grilled squid. Then graze: grab pork satay from the cart across the street, duck noodles from the corner stall, and finish with mango sticky rice from any of the fruit vendors. Budget: $10-15 per person for a feast.", meta: "200-500 THB per person ($5.70-14) · Yaowarat Rd · Evening only" }
          ],
          tips: [{ type: "reddit", text: "Yaowarat is peak Bangkok. Go on an empty stomach and just eat your way down the street. The grilled river prawns at T&K are worth the hype. Get there by 6pm before the biggest crowds.", cite: "r/ThailandTourism" }]
        }
      ]
    },
    {
      num: 3,
      title: "Markets, Massage & the River",
      neighborhoods: "Chatuchak · Silom · Riverside",
      date: "May 10",
      mapPins: [
        { lat: 13.7999, lng: 100.5533, label: "Chatuchak Weekend Market", num: 1, cat: "activity", desc: "World's largest outdoor market — 15,000+ stalls" },
        { lat: 13.7284, lng: 100.5347, label: "Silom Area", num: 2, cat: "activity", desc: "Business district with great food and nightlife" },
        { lat: 13.7240, lng: 100.5120, label: "Asiatique the Riverfront", num: 3, cat: "activity", desc: "Night market on the Chao Phraya" },
        { lat: 13.7445, lng: 100.5092, label: "Chao Phraya River", num: 4, cat: "activity", desc: "Express boat service — Bangkok's river highway" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Chatuchak Weekend Market", description: "May 10 is a Sunday — perfect. Chatuchak is the world's largest outdoor market: 15,000 stalls spread across 35 acres, selling everything from vintage clothing and handmade ceramics to fighting fish, coconut ice cream, and antique typewriters. It's organized chaos. Get lost on purpose. The best finds are always in the sections you didn't plan to visit. Come early to beat the heat — by noon it's sweltering.", details: ["📍 Kamphaeng Phet 2 Rd · Free entry · Sat-Sun 9am-6pm · BTS Mo Chit", "💡 Download the Chatuchak Guide app to navigate sections. Section 2-4 for clothes, 7-8 for antiques, 17-19 for ceramics and homewares. The coconut ice cream stall in Section 28 is legendary."] }
          ],
          meals: [
            { type: "☕ Breakfast/Brunch", name: "Chatuchak Market Eats", description: "Eat your way through the market: fresh coconut ice cream served in the shell, pad Thai from tiny wok stations, grilled pork skewers (moo ping) dipped in sticky rice, Thai iced tea, and mango sticky rice. This IS breakfast and lunch. Don't try to plan it — just follow your nose and the longest lines.", meta: "20-60 THB per item · Throughout the market · Morning is best" }
          ],
          tips: [{ type: "tip", text: "Chatuchak is enormous and hot. Wear comfortable shoes, bring water, and don't try to see everything. Pick 3-4 sections and explore deeply rather than rushing through all 27." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Thai Massage & Rest", description: "After the market madness, treat yourselves to a proper Thai massage. Wat Pho's massage school is legendary but any well-reviewed spot will do. A traditional Thai massage is 1-2 hours of full-body stretching, pressure points, and muscle work — it's intense but you'll float out feeling reborn. May heat demands an afternoon break, so lean into it.", details: ["💡 Health Land (multiple locations) offers excellent quality at fair prices: 600 THB ($17) for a 2-hour Thai massage. Book ahead on weekends."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Som Tam Jay So", description: "A tiny street cart near Silom famous for som tam (green papaya salad) — shredded unripe papaya pounded with chilies, garlic, lime, fish sauce, tomato, and peanuts. It's spicy, sour, salty, and sweet all at once. Order it with grilled chicken (gai yang) and sticky rice. This is Isaan food — northeastern Thai cuisine that's become Bangkok's street food backbone.", meta: "40-80 THB ($1.15-2.30) · Silom area · Lunch" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Chao Phraya Dinner Cruise or Asiatique", description: "Two great options for your last Bangkok evening: take a dinner cruise on the Chao Phraya River passing illuminated temples and the Grand Palace, or head to Asiatique — a riverfront night market in a converted warehouse complex with street food, shopping, a Ferris wheel, and a Muay Thai live show. Asiatique is touristy but genuinely fun, especially as a couple. The river breeze is bliss after a hot day.", details: ["📍 Asiatique: 2194 Charoen Krung Rd · Free entry · Shuttle boat from Saphan Taksin BTS · Open 4pm-midnight", "💡 For a more local experience, skip the tourist dinner cruises and just ride the Chao Phraya Express Boat at sunset — same views, $0.50."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Riverside Dining", description: "If you skip the cruise: Supanniga Eating Room (Tha Tien branch) serves refined Thai food with river views — their crab curry is unforgettable. For something more casual, grab noodles and Singha beers at any riverside spot. Bangkok's rivers are gorgeous at night.", meta: "200-600 THB/person ($5.70-17) · Various riverside spots" }
          ],
          tips: [{ type: "tip", text: "Pack your bags tonight — you have an early-ish flight to Chiang Rai tomorrow. Bangkok to Chiang Rai is about 1h20m and flights are cheap if booked ahead ($30-60 on AirAsia or Nok Air)." }]
        }
      ]
    },
    {
      num: 4,
      title: "Fly to Chiang Rai — White Temple & Night Market",
      neighborhoods: "Chiang Rai · Chiang Khong",
      date: "May 11",
      mapPins: [
        { lat: 19.9523, lng: 99.8829, label: "Chiang Rai Airport", num: 1, cat: "transport", desc: "Mae Fah Luang Airport (CEI)" },
        { lat: 19.8244, lng: 99.7631, label: "Wat Rong Khun (White Temple)", num: 2, cat: "attraction", desc: "Stunning contemporary Buddhist temple" },
        { lat: 19.9105, lng: 99.8325, label: "Chiang Rai Clock Tower", num: 3, cat: "attraction", desc: "Golden clock tower with nightly light show" },
        { lat: 19.9117, lng: 99.8318, label: "Chiang Rai Night Bazaar", num: 4, cat: "food", desc: "Night market with hill tribe crafts and street food" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Flight to Chiang Rai", description: "Catch a morning flight from Bangkok to Chiang Rai — about 1 hour 20 minutes. The landscape shift is dramatic: Bangkok's concrete jungle gives way to forested mountains and rice paddies. Chiang Rai is Thailand's northernmost province, bordering both Laos and Myanmar. It's cooler, quieter, and deeply artistic — a perfect transition between Bangkok's chaos and Laos's tranquility.", details: ["💡 AirAsia and Nok Air run multiple daily flights. Book ahead for $30-60. Don Mueang Airport (DMK) serves budget airlines — not Suvarnabhumi."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Airport or In-Flight", description: "Grab a quick breakfast at the airport — iced coffee and a pastry, or eat something more substantial if you have time. Thai airport food courts are surprisingly good and cheap.", meta: "50-100 THB ($1.50-3)" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Wat Rong Khun — The White Temple", description: "One of the most extraordinary buildings in Southeast Asia. Artist Chalermchai Kositpipat has been building this blindingly white, mirrored temple since 1997 — it's part Buddhist temple, part contemporary art installation. The exterior glitters like ice in the sun. The bridge to the main hall crosses a sea of reaching hands (representing desire/hell). Inside, the murals feature Superman, The Matrix, and 9/11 alongside traditional Buddhist imagery. It's weird, beautiful, profound, and unlike anything else you'll ever see.", details: ["📍 Pa O Don Chai Rd · 100 THB ($2.85) · Open 8am-5pm · 13km south of town center", "💡 Hire a Grab or songthaew (red truck taxi) from town. Combine with the Blue Temple (Wat Rong Suea Ten) nearby — similar psychedelic energy, no entrance fee."] },
            { title: "Blue Temple (Wat Rong Suea Ten)", description: "If the White Temple is heaven, the Blue Temple is its mystical counterpart. Deep sapphire blue with gold accents, guarded by serpent dragons, with a massive white Buddha inside a blue hall. It's smaller and less crowded than the White Temple but equally stunning. A different artist, a different vision, but the same fearless creativity that defines Chiang Rai.", details: ["📍 306 Moo 2, Rim Kok · Free entry · Open 7am-8pm · 5 min from White Temple"] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Khao Soi at Pho Chai", description: "Northern Thailand's signature dish: khao soi — egg noodles in a rich, mildly spicy coconut curry broth, topped with crispy fried noodles and pickled mustard greens, served with chicken or beef on the bone. This creamy, crunchy, aromatic bowl is unique to the north and you cannot leave without trying it. Pho Chai in town does a textbook version.", meta: "50-80 THB ($1.40-2.30) · Pho Chai · Lunch" }
          ],
          tips: [{ type: "reddit", text: "The White Temple is worth the hype. Go in the early afternoon when most tour buses have left. The murals inside are insane — Doraemon, Kung Fu Panda, and Captain America alongside traditional Buddhist art. The artist is still working on it and adding new buildings.", cite: "r/ThailandTourism" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Chiang Rai Night Bazaar & Clock Tower", description: "The Night Bazaar is Chiang Rai's social hub — a compact outdoor market with hill tribe handicrafts, street food stalls, and a central food court with live music. At 7pm, 8pm, and 9pm, the golden Clock Tower (designed by the same artist as the White Temple) puts on a dramatic light and sound show that stops traffic. Pick a spot at the food court, order a plate of grilled sausages (sai ua — northern Thai spiced sausage), Singha beer, and enjoy the show.", details: ["📍 Chiang Rai Night Bazaar · Phaholyothin Rd · Free entry · Open 6pm-11pm nightly", "💡 The hill tribe crafts here are more authentic and cheaper than Bangkok. Silver jewelry, hand-woven textiles, and bamboo goods make great souvenirs."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Night Bazaar Food Court", description: "The food court inside the Night Bazaar is local-heavy and excellent: grilled meats on sticks, larb (spicy minced meat salad), sticky rice, green curry, pad see ew, and fresh fruit shakes. Order from multiple stalls and create your own feast. Everything is labeled in English.", meta: "40-100 THB per dish ($1.15-2.85) · Night Bazaar · Evening" }
          ],
          tips: [{ type: "tip", text: "Tomorrow morning you'll take a bus/minivan to Chiang Khong (the Thai border town) — about 2.5 hours. Your guesthouse can arrange this. Alternatively, book a slow boat package from Chiang Rai that includes the transfer, border crossing assistance, and boat ticket." }]
        }
      ]
    },
    {
      num: 5,
      title: "Cross to Laos & Slow Boat Day 1 — Huay Xai to Pak Beng",
      neighborhoods: "Chiang Khong · Huay Xai · Mekong River · Pak Beng",
      date: "May 12",
      mapPins: [
        { lat: 20.2633, lng: 100.4044, label: "Chiang Khong (Thai border)", num: 1, cat: "transport", desc: "Thai border town — departure point" },
        { lat: 20.2610, lng: 100.4170, label: "Fourth Thai-Lao Friendship Bridge", num: 2, cat: "transport", desc: "Cross the Mekong to Laos" },
        { lat: 20.2590, lng: 100.4300, label: "Huay Xai Boat Landing", num: 3, cat: "transport", desc: "Slow boat departure point in Laos" },
        { lat: 19.8917, lng: 101.4075, label: "Pak Beng", num: 4, cat: "activity", desc: "Riverside overnight stop — one-street hill town" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Border Crossing: Thailand → Laos", description: "Early start. Take the bus or arranged transfer from Chiang Rai/Chiang Khong to the Thai border. At Chiang Khong, you'll exit Thailand (passport stamped out), then take a short bus ride across the Fourth Thai-Lao Friendship Bridge over the Mekong to Huay Xai, Laos. Get your Laos visa on arrival at immigration (~$30-42 USD depending on nationality, bring passport photos and exact USD cash). The whole process takes 1-2 hours depending on queues.", details: ["💡 Bring 2 passport photos and USD cash for the Laos visa on arrival. Some nationalities don't need a visa — check beforehand. There's an exchange booth at the border for Lao Kip.", "💡 If you arranged a slow boat package, they'll handle the logistics. If DIY, just follow the crowd from immigration down to the boat landing."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Quick Breakfast in Chiang Khong", description: "Grab noodle soup or toast and coffee at your guesthouse or a roadside shop in Chiang Khong before heading to the border. Eat well — the slow boat has limited food options.", meta: "30-60 THB · Guesthouse or street vendor" }
          ],
          tips: [{ type: "tip", text: "Stock up on snacks and water at the small shops near the Huay Xai boat landing BEFORE boarding. The boat has a small bar but prices are higher and selection is limited. Beerlao, water, chips, fruit, and a baguette sandwich are your best friends." }]
        },
        {
          label: "All Day (11am–5pm)",
          activities: [
            { title: "Slow Boat Day 1: Huay Xai → Pak Beng", description: "This is it — the journey you came for. The public slow boat departs Huay Xai around 11am and glides downstream through 6 hours of pristine Mekong River wilderness. The scenery is staggering: sheer limestone cliffs draped in jungle, remote villages accessible only by river, water buffalo bathing on sandbars, fishermen casting nets from longtail boats, and the vast brown Mekong carving through mountains that haven't changed in centuries. This is Southeast Asia before roads. The boat itself is a long, wooden vessel with rows of car-seat-style chairs facing forward. It's basic but beautiful. Crack open a Beerlao, pull out your book, and watch the world's 12th-longest river unfold. In May, the water is rising and the jungle is explosively green from early rains.", details: ["📍 Huay Xai Boat Landing → Pak Beng · ~6 hours · Departs ~11am", "💡 Sit on the LEFT side for the best jungle views and afternoon shade. Bring a cushion/scarf for the wooden seats. Sunscreen for the glare off the water.", "📚 READING TIME: This is your first major reading window. Six uninterrupted hours with no WiFi, no distractions, just river sounds and turning pages. Bring your book."] }
          ],
          meals: [
            { type: "🍽️ Boat Lunch", name: "Packed Snacks & Boat Bar", description: "The boat has a small bar selling Beerlao ($1.50), water, instant noodles, and basic snacks. Supplement with whatever you bought in Huay Xai — baguette sandwiches, fruit, cookies. Some boats have a vendor selling fried rice or noodle dishes. It's basic but you're not here for the food — you're here for the journey.", meta: "Bring your own snacks + $5-10 for boat bar purchases" }
          ],
          tips: [{ type: "reddit", text: "The slow boat is one of the best travel experiences in Southeast Asia. It's long and the seats aren't comfortable but the scenery is unreal. Bring a book, snacks, and Beerlao. The left side has better views. Don't take the speedboat — it's dangerous and you miss everything.", cite: "r/laos" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Arrive in Pak Beng", description: "The boat pulls into Pak Beng around 5-6pm as the sun begins to set over the Mekong. Pak Beng is a one-street hill town that exists almost entirely because of the slow boat — every passenger spends the night here. Climb the steep path from the boat landing up to the main street, pick a guesthouse with a river view (the touts will find you), and shower off the river dust. Then sit on a balcony overlooking the Mekong as the sky turns orange and pink. This is a moment.", details: ["💡 Guesthouses range from $5-20/night. Hive Bar and Mekong View guesthouses have the best river views. Don't overthink it — you're only here one night.", "💡 Pak Beng has spotty electricity and limited WiFi. Embrace it."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Mekong Riverside Dinner", description: "Walk the main street and pick a restaurant with a terrace overlooking the river. Most serve similar Lao food: laap (minced meat salad with herbs, lime, and roasted rice powder), sticky rice, fried Mekong fish, spring rolls, and papaya salad. Pair it all with Beerlao — Laos's surprisingly excellent national lager. The food is simple, fresh, and exactly right for this moment.", meta: "30,000-60,000 LAK ($1.50-3) per dish · Main street restaurants · Beerlao: 15,000 LAK ($0.75)" }
          ],
          tips: [{ type: "tip", text: "Go to bed early. The boat to Luang Prabang departs around 9am and the boarding process starts at 8am. You'll want a good seat again." }]
        }
      ]
    },
    {
      num: 6,
      title: "Slow Boat Day 2 — Pak Beng to Luang Prabang",
      neighborhoods: "Mekong River · Luang Prabang",
      date: "May 13",
      mapPins: [
        { lat: 19.8917, lng: 101.4075, label: "Pak Beng (departure)", num: 1, cat: "transport", desc: "Morning departure point" },
        { lat: 20.0556, lng: 102.1375, label: "Pak Ou Caves area", num: 2, cat: "attraction", desc: "Thousands of Buddha statues in river caves (visible from boat)" },
        { lat: 19.8856, lng: 102.1347, label: "Luang Prabang Boat Landing", num: 3, cat: "transport", desc: "Arrival point — heart of the old town" },
        { lat: 19.8892, lng: 102.1350, label: "Luang Prabang Old Town", num: 4, cat: "activity", desc: "UNESCO World Heritage town center" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Slow Boat Day 2: Pak Beng → Luang Prabang", description: "Board the boat by 8:30am for the 9am departure. Day 2 is another 7-8 hours on the Mekong, and the scenery arguably gets even better. The river narrows in places, the karst mountains grow taller, and you'll pass the Pak Ou Caves area — dramatic limestone cliffs where the Nam Ou River meets the Mekong, filled with thousands of Buddha statues. You can't stop on the public boat, but you'll see the caves from the water. The rhythm of the boat, the green water, the jungle sounds — it's deeply meditative. More reading time, more Beerlao, more river.", details: ["📍 Pak Beng → Luang Prabang · ~7-8 hours · Departs ~9am, arrives ~4-5pm", "📚 READING TIME: Another 7-8 hours of pure reading/reflection time. By now you'll have found your river rhythm. This is the chill reading time you wanted — the Mekong delivers."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Pak Beng Bakery", description: "Several bakeries on Pak Beng's main street open early to serve slow boat passengers: French-style baguettes (a Lao colonial legacy), banana pancakes, real coffee, and fresh fruit. Fuel up properly — it's another long day on the water.", meta: "10,000-30,000 LAK ($0.50-1.50) · Main street · Early morning" }
          ],
          tips: [{ type: "tip", text: "The final hour of the boat ride, as Luang Prabang appears around the river bend, is magical. Mountains, golden temple spires poking above the treeline, the Nam Khan River flowing in from the right. Have your camera ready." }]
        },
        {
          label: "Late Afternoon / Evening",
          activities: [
            { title: "Arrive in Luang Prabang", description: "The boat lands right in the heart of Luang Prabang's old town around 4-5pm. Walk off the boat and you're immediately in a UNESCO World Heritage Site — a perfectly preserved French colonial and Lao town at the confluence of the Mekong and Nam Khan rivers. Drop your bags at your guesthouse and wander. The golden hour light on the temple roofs, the bougainvillea, the quiet streets lined with palm trees — Luang Prabang is love at first sight.", details: ["💡 Book accommodation in the Old Town (peninsula between the two rivers) for walkability. Plenty of charming guesthouses $15-40/night."] },
            { title: "Sunset at Phousi Hill", description: "Climb the 328 steps to the top of Mount Phousi in the center of town for a 360-degree panorama of Luang Prabang, the Mekong, and the surrounding mountains. At sunset, the whole landscape turns golden. It's the best introduction to a town that will have you considering never leaving.", details: ["📍 Sisavangvong Rd · 20,000 LAK ($1) · Climb takes 15-20 min"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Tamarind Restaurant", description: "Your first proper Lao meal at one of Luang Prabang's best restaurants. Tamarind is dedicated to preserving traditional Lao cuisine: try the tasting platter for an overview — sticky rice, jeow bong (spicy chili paste with buffalo skin), laap, stuffed lemongrass, river weed with sesame (a Luang Prabang specialty), and Mekong fish steamed in banana leaf. Everything is exquisitely flavored. They also run cooking classes if you want to go deeper.", meta: "60,000-120,000 LAK ($3-6) per person · Ban Wat Sene · Reservation recommended" }
          ],
          tips: [{ type: "reddit", text: "Luang Prabang exceeded every expectation. It's one of the most peaceful, beautiful places I've ever been. Stay in the old town, wake up for the alms giving, eat at Tamarind, and swim at Kuang Si. Don't rush — this place rewards slowness.", cite: "r/solotravel" }]
        }
      ]
    },
    {
      num: 7,
      title: "Alms Giving, Temples & the Night Market",
      neighborhoods: "Luang Prabang Old Town",
      date: "May 14",
      mapPins: [
        { lat: 19.8880, lng: 102.1348, label: "Sakkaline Road (Alms Giving)", num: 1, cat: "attraction", desc: "Morning alms ceremony — monks in saffron robes" },
        { lat: 19.8893, lng: 102.1332, label: "Wat Xieng Thong", num: 2, cat: "attraction", desc: "Luang Prabang's most beautiful temple" },
        { lat: 19.8899, lng: 102.1334, label: "Royal Palace Museum", num: 3, cat: "attraction", desc: "Former royal residence, now a museum" },
        { lat: 19.8880, lng: 102.1350, label: "Night Market", num: 4, cat: "activity", desc: "Handicraft night market on Sisavangvong Road" },
        { lat: 19.8883, lng: 102.1380, label: "Joma Bakery Café", num: 5, cat: "food", desc: "Perfect reading café with river views" }
      ],
      timeBlocks: [
        {
          label: "Early Morning",
          activities: [
            { title: "Morning Alms Giving Ceremony (Tak Bat)", description: "Set your alarm for 5:30am. Every morning at dawn, hundreds of saffron-robed monks walk barefoot in silent single file through the streets of Luang Prabang while residents kneel and place sticky rice into their alms bowls. This tradition has continued unbroken for centuries. It's one of the most moving and spiritual rituals in Southeast Asia. Watch quietly from the opposite side of the street. Do not use flash photography. Do not block the monks' path. If you want to participate, buy sticky rice from a local vendor (not the tourist traps) and kneel respectfully.", details: ["📍 Sakkaline Road (main street) · ~6:00-6:30am · Free to observe", "💡 Be a silent observer, not a spectacle. No flash, no selfies with monks. Sit or kneel at a respectful distance. This is a living religious practice, not a show."] }
          ],
          meals: [
            { type: "☕ Morning Coffee", name: "Joma Bakery Café", description: "After the ceremony, walk to Joma — a beloved Luang Prabang institution serving proper espresso, fresh croissants, quiche, and smoothies in a beautiful colonial building. Grab a window seat or the upstairs terrace, order a latte and pastry, and start your morning reading session. This is one of Luang Prabang's perfect reading spots — you could happily spend two hours here.", meta: "25,000-50,000 LAK ($1.25-2.50) · Sisavangvong Rd · Opens early · WiFi" }
          ],
          tips: [{ type: "tip", text: "📚 READING TIME: Joma in the early morning, after the alms ceremony, is perfect. The town is still quiet, the coffee is good, and there's nowhere you need to be. Read for an hour or two before the day heats up." }]
        },
        {
          label: "Morning / Midday",
          activities: [
            { title: "Wat Xieng Thong", description: "Luang Prabang's crown jewel — a masterpiece of Lao temple architecture from 1560, sitting at the tip of the old town peninsula where the two rivers meet. The sweeping, multi-tiered roofs nearly touch the ground. The rear wall features a stunning 'Tree of Life' glass mosaic. Inside, gold stencils on black lacquer walls depict Buddhist and folk stories. The royal funeral chapel houses an elaborate gilded hearse. It's intimate, serene, and unbelievably beautiful.", details: ["📍 Khem Khong Rd · 20,000 LAK ($1) · Open 8am-5pm"] },
            { title: "Royal Palace Museum (Haw Kham)", description: "The former residence of Lao royalty, now a museum housing the Phra Bang (the sacred gold Buddha after which the city is named), royal regalia, diplomatic gifts, and a throne hall. The architecture blends French Beaux-Arts with traditional Lao style. Worth an hour to understand Luang Prabang's royal history and why this tiny town punches so far above its weight.", details: ["📍 Sisavangvong Rd · 30,000 LAK ($1.50) · Open 8am-11:30am & 1:30pm-4pm · No photos inside"] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Khaiphaen Restaurant", description: "Social enterprise restaurant training former street youth in hospitality. The food is excellent: crispy Mekong riverweed (the restaurant's namesake — a local delicacy), buffalo laap, fish in banana leaf, and fresh herbs from their garden. Eat on the airy terrace overlooking the street. You're supporting a great cause and getting one of the best meals in town.", meta: "40,000-80,000 LAK ($2-4) per dish · Sisavangvong Rd · Lunch-dinner" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Riverside Reading & Chill Time", description: "This is your afternoon to do absolutely nothing productive. Walk down to the Mekong waterfront, find a hammock or a shady spot at Utopia Bar — a legendary riverside lounge with floor cushions, hammocks, and views over the Nam Khan River. Order a fruit shake or Beerlao, open your book, and disappear for a few hours. The gentle sound of the river and the afternoon heat make this effortless. This is the chill reading time you asked for.", details: ["📍 Utopia Bar · Downstream from Wat Xieng Thong · Open 8am-11:30pm · Cash only", "📚 READING TIME: Utopia is possibly the best reading spot in Southeast Asia. Floor cushions, river views, cold drinks, no urgency. Stay as long as you want."] }
          ],
          meals: [],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Luang Prabang Night Market", description: "Every evening, the main street transforms into a gorgeous handicraft night market. Hmong and Lao vendors sell hand-woven textiles, silk scarves, mulberry paper lanterns, hand-stitched bags, and silver jewelry. It's tasteful, well-curated, and far more artisanal than most Southeast Asian night markets. Walk slowly, browse, and pick up unique souvenirs. The handwoven silk pieces are particularly special.", details: ["📍 Sisavangvong Road · Open 5pm-10pm nightly · Cash preferred"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Night Market Food Stalls", description: "At the end of the handicraft market, a food alley serves the most affordable dinner in Luang Prabang: vegetarian buffet plates where you fill a bowl for 15,000 LAK ($0.75), plus grilled meats, noodle soups, and coconut pancakes. It's where locals and budget travelers eat. The vegetarian buffet stalls are surprisingly diverse — curries, stir-fries, spring rolls, tofu dishes. Pair with a fresh fruit shake.", meta: "15,000-40,000 LAK ($0.75-2) · End of night market · Evening" }
          ],
          tips: [{ type: "tip", text: "The vegetarian buffet stalls at the night market are one of Luang Prabang's best-kept secrets. For $0.75 you get a heaping plate of diverse, flavorful food. Most items are actually vegan." }]
        }
      ]
    },
    {
      num: 8,
      title: "Kuang Si Falls & Whiskey Village",
      neighborhoods: "Kuang Si · Ban Xang Hai · Luang Prabang",
      date: "May 15",
      mapPins: [
        { lat: 19.7486, lng: 101.9956, label: "Kuang Si Falls", num: 1, cat: "attraction", desc: "Turquoise cascading waterfall — Luang Prabang's crown jewel" },
        { lat: 19.7480, lng: 101.9950, label: "Kuang Si Bear Rescue Centre", num: 2, cat: "attraction", desc: "Rescued Asiatic black bears" },
        { lat: 19.8500, lng: 102.0900, label: "Ban Xang Hai (Whiskey Village)", num: 3, cat: "activity", desc: "Village famous for Lao Lao rice whiskey" },
        { lat: 19.8870, lng: 102.1415, label: "Le Banneton Bakery", num: 4, cat: "food", desc: "French bakery — morning reading spot" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Kuang Si Falls", description: "The most beautiful waterfall in Southeast Asia — and it earns that title. A 60-meter cascade of milky turquoise water pours over limestone tiers into a series of natural swimming pools surrounded by jungle. The water gets its surreal color from dissolved limestone minerals. Swim in the pools, climb to the top of the falls via jungle trails, or just sit on the rocks and stare. In May, water flow is increasing from early rains — the falls will be powerful and the pools full. Bring swimwear, water shoes, and a towel.", details: ["📍 29km south of Luang Prabang · 20,000 LAK ($1) · Open 8am-5pm", "💡 Hire a tuk-tuk ($8-10 return with waiting time) or join a shared minivan ($3-5/person). Go early (8-9am) to get the pools before crowds arrive.", "💡 The bear rescue center at the entrance is free and worth 20 minutes — rescued Asiatic black bears playing in their enclosures."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Le Banneton", description: "French bakery with flaky croissants, pain au chocolat, and strong coffee — a legacy of Laos's French colonial period. Grab breakfast to go or eat on their terrace before heading to the falls. Another perfect reading-with-coffee spot.", meta: "20,000-40,000 LAK ($1-2) · Near old town · Morning" }
          ],
          tips: [{ type: "reddit", text: "Kuang Si is magical. Go EARLY before the tour groups (they arrive 10-11am). The top pool at the base of the main falls is the best swimming spot. Wear water shoes — the rocks are slippery. Easily the highlight of Luang Prabang.", cite: "r/laos" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Ban Xang Hai — Whiskey Village", description: "On the way back from Kuang Si (or by boat), stop at Ban Xang Hai — a riverside village famous for producing Lao Lao, Laos's potent rice whiskey. Sample varieties infused with scorpions, snakes, herbs, and honey. The village women will happily let you taste everything. Buy a bottle for $2-3 as a souvenir. The snake whiskey bottles make incredible gifts (or conversation pieces).", details: ["📍 On the Mekong, 25km upstream from LP · Accessible by boat or road · Free to visit", "💡 If you take a boat tour to Kuang Si, the whiskey village stop is usually included."] },
            { title: "Afternoon Reading by the River", description: "Back in Luang Prabang, find a quiet cafe or your guesthouse balcony for more reading time. The town's pace encourages it — there's no urgency, no rush. Sip iced Lao coffee (dark roast with sweetened condensed milk, poured over ice) and read until golden hour.", details: ["📚 READING TIME: Afternoon in Luang Prabang is made for reading. Try the bamboo bridge area near the confluence of the rivers, or the cafes along the Mekong side of the peninsula."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Picnic at Kuang Si / Light Lunch", description: "Pack sandwiches from Le Banneton for a picnic at Kuang Si, or eat at the small restaurants near the falls entrance. Simple Lao food — fried rice, noodle soup, spring rolls — at fair prices.", meta: "30,000-50,000 LAK ($1.50-2.50) · Near falls entrance" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Cooking Class or Spa Evening", description: "Two great options: take an evening Lao cooking class at Tamarind (learn to make laap, sticky rice, jeow dipping sauces, and more — $30-40/person including a market visit), or treat yourselves to a traditional Lao herbal sauna and massage at the Red Cross Sauna ($3 for sauna, $8-10 for massage). After the active Kuang Si morning, either is a perfect wind-down.", details: ["📍 Tamarind Cooking Class: book through their restaurant · Red Cross Sauna: Wisunalat Rd, open 4:30-8pm"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Dyen Sabai", description: "Cross the bamboo bridge over the Nam Khan to Dyen Sabai — a garden restaurant with cushions under the trees, fairy lights, and a relaxed hippie-chic atmosphere. The Lao fusion food is excellent: try the stuffed Mekong fish, Luang Prabang salad, and their signature cocktails. It's romantic, unhurried, and exactly the kind of place you come to Luang Prabang to discover.", meta: "50,000-100,000 LAK ($2.50-5) per dish · Cross bamboo bridge · Dinner · Cash only" }
          ],
          tips: [{ type: "tip", text: "The bamboo bridge to Dyen Sabai charges a 10,000 LAK ($0.50) toll. These bridges are rebuilt every year after the rainy season washes them away — a beautiful, impermanent tradition." }]
        }
      ]
    },
    {
      num: 9,
      title: "Morning Yoga, Weaving & Final Mekong Sunset",
      neighborhoods: "Luang Prabang Old Town · Ban Xang Khong",
      date: "May 16",
      mapPins: [
        { lat: 19.8900, lng: 102.1310, label: "Mekong Riverside", num: 1, cat: "activity", desc: "Morning walk and reading by the river" },
        { lat: 19.8970, lng: 102.1480, label: "Ban Xang Khong", num: 2, cat: "activity", desc: "Traditional weaving and paper-making village" },
        { lat: 19.8862, lng: 102.1420, label: "Ock Pop Tok Living Crafts Centre", num: 3, cat: "activity", desc: "Textile center with weaving classes and riverside cafe" },
        { lat: 19.8878, lng: 102.1345, label: "Utopia Bar", num: 4, cat: "activity", desc: "Hammock bar overlooking the Nam Khan" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Slow Morning — Coffee & Reading", description: "Your last full day in Luang Prabang. No alarm, no plan. Wake up naturally, walk to your favorite café (Joma, Le Banneton, or one of the small Lao coffee shops on the side streets), and read for as long as you want. This is your chill reading morning. The town is quietest before 9am — just monks, market vendors, and the occasional rooster. Savor it.", details: ["📚 READING TIME: This morning is entirely yours. Two hours of reading with good coffee, no agenda. The trip's pace has been building to this — total relaxation."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Café Mekong or Joma", description: "Linger over breakfast: eggs, fresh bread, tropical fruit, and strong Lao coffee. Or try khao piak sen — Lao chicken noodle soup with hand-rolled rice noodles in a silky, gingery broth. It's Luang Prabang's comfort food and the perfect slow morning dish.", meta: "25,000-50,000 LAK ($1.25-2.50) · Various old town spots" }
          ],
          tips: []
        },
        {
          label: "Midday",
          activities: [
            { title: "Ock Pop Tok Living Crafts Centre", description: "A stunning riverside textile center where you can take a half-day weaving class, watch master weavers at their looms, learn about Lao silk traditions, and browse beautiful handmade textiles. The centre sits on the banks of the Mekong with a gorgeous cafe and gardens. Even if you don't take a class, the cafe alone is worth the visit — river views, good food, hammocks, and the peaceful sound of looms clicking. It's a UNESCO-recognized cultural preservation project.", details: ["📍 Ban Saylom, along the Mekong · Weaving class: $35-65/person (half/full day) · Cafe open to all · Free tuk-tuk from town center", "💡 The half-day weaving class is surprisingly engaging — you'll make a small silk piece to take home. Book ahead."] },
            { title: "Ban Xang Khong Village", description: "A short bike ride from town, this quiet village is famous for traditional sa (mulberry bark) paper making and hand weaving. Watch artisans turn mulberry bark into gorgeous paper embedded with flowers, and see traditional Lao textiles being woven on wooden looms. Buy handmade paper lanterns, journals, or prints directly from the makers. It's authentic, uncommercial, and beautiful.", details: ["📍 3km east of old town · Free to visit · Accessible by bicycle or tuk-tuk"] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Ock Pop Tok Café", description: "Eat at the craft center's riverside cafe — Lao food with a modern touch, served in a beautiful garden setting overlooking the Mekong. The fish laap and herbal teas are excellent. You'll feel like you've stumbled into someone's impossibly chic riverside garden party.", meta: "40,000-70,000 LAK ($2-3.50) · At the craft center · Lunch" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Final Mekong Sunset", description: "Walk down to the Mekong riverbank for your last sunset. The western sky over the mountains turns from gold to pink to deep purple. Local kids play in the shallows. Fishermen head home in longtail boats. This is the moment you'll remember when someone asks about this trip. Find a quiet spot, sit on the riverbank, and just be present.", details: ["💡 The best sunset spot is the riverbank near Wat Xieng Thong — facing west across the Mekong with the mountains behind."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "The Belle Rive Terrace", description: "Splurge on your final night: The Belle Rive boutique hotel's riverside terrace serves excellent Lao-French fusion with the Mekong as your backdrop. Grilled Mekong fish, duck laap, French wine, and crème brûlée under the stars. It's romantic, indulgent, and the perfect farewell dinner to a trip that delivered everything you wanted.", meta: "80,000-150,000 LAK ($4-7.50) per person · Khem Khong Rd · Reservation recommended" }
          ],
          tips: [{ type: "tip", text: "Pack tonight. Tomorrow you fly home from Luang Prabang. Flights to Bangkok are on Bangkok Airways or Lao Airlines — about 1h40m. Book the afternoon flight if you want one more morning in town." }]
        }
      ]
    },
    {
      num: 10,
      title: "Departure — One Last Morning",
      neighborhoods: "Luang Prabang · Luang Prabang Airport",
      date: "May 17",
      mapPins: [
        { lat: 19.8880, lng: 102.1348, label: "Luang Prabang Old Town", num: 1, cat: "activity", desc: "Final morning walk" },
        { lat: 19.8980, lng: 102.1610, label: "Luang Prabang Airport (LPQ)", num: 2, cat: "transport", desc: "Departure airport" },
        { lat: 19.8883, lng: 102.1380, label: "Joma Bakery Café", num: 3, cat: "food", desc: "Last coffee and reading" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Last Morning in Luang Prabang", description: "If your flight is in the afternoon, you have one more golden morning. Watch the alms ceremony one final time (it hits different the second time — you know what to expect and can be fully present). Then walk the quiet streets one last time: past the temples, along the river, through the market. Buy a last bag of Lao coffee beans ($3-5) or a silk scarf from a vendor you've been eyeing. Have your final Lao coffee at Joma. Read one more chapter. Let Luang Prabang imprint itself on you.", details: ["📍 Luang Prabang Airport (LPQ) is just 4km from old town — 10 minutes by tuk-tuk ($3-5)", "📚 READING TIME: Your final reading session. Full circle from the Mekong slow boat to a quiet Luang Prabang cafe."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Final Joma Breakfast", description: "One more breakfast at Joma or Le Banneton. Croissant, coffee, tropical fruit. Soak up the atmosphere one last time. This place has a way of making you plan your next visit before you've even left.", meta: "25,000-50,000 LAK · Old town · Morning" }
          ],
          tips: [{ type: "tip", text: "Luang Prabang's airport is tiny, charming, and efficient. Arrive 1.5 hours before your flight. There's a small café and duty-free shop but not much else — do your souvenir shopping in town." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Fly Home", description: "Tuk-tuk to the airport and fly out. Bangkok Airways and Lao Airlines run direct flights to Bangkok (1h40m). Connect onwards from Bangkok Suvarnabhumi to your final destination. As the plane lifts off and you see the Mekong River winding through the mountains below, you'll understand why people keep coming back to this part of the world.", details: [] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "If you have a long connection in Bangkok, the airport has excellent lounges (Miracle Lounge, ~$30 walk-in) and a great food court in the basement level. One more pad Thai for the road." }]
        }
      ]
    }
  ],
  budgetTable: [
    { item: "Bangkok → Chiang Rai flight", cost: "$30-60/person", notes: "AirAsia or Nok Air, book 2+ weeks ahead" },
    { item: "Bangkok accommodation (3 nights)", cost: "$20-40/night", notes: "Boutique guesthouse in Old City" },
    { item: "Chiang Rai accommodation (1 night)", cost: "$15-25/night", notes: "Guesthouse near Night Bazaar" },
    { item: "Slow boat ticket (Huay Xai → LP)", cost: "$25-35/person", notes: "Buy at boat landing or via guesthouse" },
    { item: "Pak Beng accommodation (1 night)", cost: "$5-20/night", notes: "Basic river-view guesthouse" },
    { item: "Luang Prabang accommodation (3 nights)", cost: "$15-40/night", notes: "Old town guesthouse or boutique hotel" },
    { item: "Luang Prabang → Bangkok flight", cost: "$80-150/person", notes: "Bangkok Airways or Lao Airlines" },
    { item: "Laos visa on arrival", cost: "$30-42/person", notes: "Depends on nationality — bring USD cash + photos" },
    { item: "Food (daily average)", cost: "$10-25/day for two", notes: "Street food to nice restaurants" },
    { item: "Activities & transport", cost: "$5-15/day for two", notes: "Temples, falls, tuk-tuks" },
    { item: "ESTIMATED TOTAL (2 people)", cost: "$1,000-1,800", notes: "Comfortably within your budget" }
  ],
  practicalInfo: [
    { title: "💉 Health & Vaccinations", text: "No mandatory vaccinations, but recommended: Hepatitis A & B, Typhoid, Tetanus. Malaria risk is very low in cities and tourist areas but higher in remote jungle. Mosquito repellent is essential for dengue prevention (present year-round). Drink bottled water only. Travel insurance covering medical evacuation is strongly recommended." },
    { title: "🔌 Power & Plugs", text: "Thailand uses Types A, B, C (220V). Laos uses Types A, B, C, E, F (230V). A universal adapter covers both. Most hotels have USB charging available." },
    { title: "🗣️ Language", text: "Thai in Thailand, Lao in Laos (mutually intelligible to some degree). English is widely spoken in Bangkok tourist areas, less so in Chiang Rai and rural Laos. In Luang Prabang, English and some French are common. Google Translate's camera feature is invaluable for menus." },
    { title: "🙏 Cultural Etiquette", text: "Remove shoes before entering temples and homes. Don't touch people's heads. Don't point your feet at Buddha images or monks. Dress modestly at temples (cover knees and shoulders). In Laos, the traditional greeting is the 'nop' — hands pressed together at chest level. Thai equivalent: the 'wai.' Return it when received." },
    { title: "🔒 Safety", text: "Both Thailand and Laos are very safe for travelers. Petty theft exists in crowded areas — use a money belt or front pocket. The biggest risks: traffic (especially motorbikes), dehydration in May heat, and overenthusiastic street food consumption (pace yourself). The slow boat is safe but can be crowded — guard your belongings." }
  ]
};

// Run fulfillment
try {
  const result = fulfillOrder(order, itineraryData);
  console.log('\n🎉 ORDER FULFILLED SUCCESSFULLY');
  console.log('Slug:', result.slug);
  console.log('URL:', result.url);
  console.log('File:', result.filePath);
} catch (err) {
  console.error('\n❌ FULFILLMENT FAILED:', err.message);
  process.exit(1);
}
