const fs = require('fs');
const path = require('path');

// Monkey-patch generateSlug to always return "ruby-kite"
const origRequire = module.constructor.prototype.require;
const slugPath = require.resolve('./generate-slug');
require.cache[slugPath] = { id: slugPath, filename: slugPath, loaded: true, exports: () => 'ruby-kite' };

const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1771169931515_hsq4o9",
  email: "bokasev328@2insp.com",
  destination: "Japan",
  start_date: "2026-05-10",
  end_date: "2026-05-30",
  group_size: "2",
  travel_style: "Adventure, Cultural, Foodie",
  dining: "Mix of everything",
  budget: "Surprise me",
  requests: "",
  amount: "0.00",
  timestamp: "2026-02-15T15:38:51.515Z",
  status: "pending"
};

const itineraryData = {
  destination: "Japan",
  countryEmoji: "🇯🇵",
  title: "Japan: 20 Days of Adventure, Culture & Flavor",
  subtitle: "Tokyo → Hakone → Kanazawa → Takayama → Kyoto → Nara → Osaka → Hiroshima → Miyajima → Osaka",
  description: "An epic 20-day journey through Japan's iconic cities and hidden gems. From Tokyo's neon-lit streets to Kyoto's serene temples, Osaka's legendary street food, and Hiroshima's powerful history — this itinerary covers it all with the perfect balance of adventure, culture, and food.",
  duration: "20 days",
  dates: "May 10 – 30, 2026",
  budget: "Surprise me",
  pace: "Balanced",
  bestFor: "Adventure seekers, culture lovers & foodies",
  highlights: [
    "Tokyo's hidden izakayas and Tsukiji Outer Market",
    "Hakone hot springs with Mt. Fuji views",
    "Kanazawa's stunning Kenroku-en Garden",
    "Takayama's Edo-period old town",
    "Kyoto's bamboo groves and Fushimi Inari at dawn",
    "Nara's friendly deer and ancient temples",
    "Osaka's Dotonbori street food marathon",
    "Hiroshima's Peace Memorial and Miyajima Island",
    "Day trips, cooking classes, and sake tastings"
  ],
  essentials: [
    { title: "🚄 Japan Rail Pass", text: "Get a 21-day JR Pass (~¥60,000). Covers shinkansen between cities, local JR trains, and airport transfers. Activate it on Day 1 at any JR ticket office." },
    { title: "💳 IC Card (Suica/Pasmo)", text: "Load up an IC card for subway, buses, and convenience store purchases. Available at any station kiosk or now via Apple Wallet." },
    { title: "🌐 Pocket WiFi / eSIM", text: "Grab an eSIM (Ubigi or Airalo) before departure or rent a pocket WiFi at the airport. Data is essential for Google Maps and translation apps." },
    { title: "🏧 Cash is King", text: "Many restaurants and small shops are cash-only. 7-Eleven ATMs accept foreign cards. Carry ¥10,000-20,000 at all times." },
    { title: "🗣️ Key Phrases", text: "Sumimasen (excuse me), Arigatou gozaimasu (thank you), Oishii (delicious), Kanpai (cheers). Locals deeply appreciate the effort." },
    { title: "👟 Comfortable Shoes", text: "You'll walk 15,000-25,000 steps daily. Bring shoes you can slip on/off easily — you'll be removing them constantly at temples and restaurants." }
  ],
  days: [
    // DAY 1 — Tokyo Arrival
    {
      num: 1,
      title: "Arrival & Shinjuku Exploration",
      neighborhoods: "Shinjuku · Omoide Yokocho",
      date: "May 10",
      mapPins: [
        { lat: 35.7648, lng: 139.7380, label: "Shinjuku Station", num: 1, cat: "transport", desc: "Arrive via Narita Express to Shinjuku" },
        { lat: 35.6938, lng: 139.7035, label: "Hotel Gracery Shinjuku", num: 2, cat: "lodging", desc: "Check into hotel in the heart of Shinjuku" },
        { lat: 35.6933, lng: 139.6998, label: "Omoide Yokocho", num: 3, cat: "food", desc: "Smoky alley of tiny yakitori stalls from the 1940s" },
        { lat: 35.6896, lng: 139.6922, label: "Tokyo Metropolitan Government Building", num: 4, cat: "activity", desc: "Free observation deck with panoramic city views" },
        { lat: 35.6940, lng: 139.7036, label: "Golden Gai", num: 5, cat: "food", desc: "Iconic cluster of 200+ tiny bars, each seating 5-10 people" }
      ],
      timeBlocks: [
        {
          label: "Afternoon",
          activities: [
            { title: "Arrive at Narita/Haneda → Shinjuku", description: "Take the Narita Express (NEX) or Limousine Bus to Shinjuku. Activate your JR Pass at the airport.", details: ["💡 NEX takes ~80 min from Narita, covered by JR Pass"] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "Drop bags at your hotel and explore — don't waste your first afternoon sleeping off jet lag." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Omoide Yokocho (Memory Lane)", description: "Wander this atmospheric alley of tiny yakitori joints. Pull up a stool, order some skewers and a beer.", details: ["📍 West exit of Shinjuku Station"] },
            { title: "Tokyo Metropolitan Government Building", description: "Free observation decks on the 45th floor. Open until 11pm — stunning night views of the city.", details: [] }
          ],
          meals: [
            { type: "🍢 Dinner", name: "Omoide Yokocho Yakitori Stalls", description: "Try chicken skin (kawa), heart (hatsu), and cartilage (nankotsu). Point and order — no Japanese needed.", meta: "¥1,500-3,000/person · Cash only" }
          ],
          tips: [{ type: "reddit", text: "Omoide Yokocho is tourist-heavy but still worth it. Go to the back alleys for the more local spots.", cite: "r/JapanTravel" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Golden Gai Bar Crawl", description: "Pick 2-3 tiny bars to hop between. Each has a unique theme — from jazz to horror to anime. Look for bars without cover charges (check the signs).", details: ["💡 Some bars charge ¥500-1000 cover. Ask before sitting."] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    // DAY 2 — Tsukiji, Asakusa, Akihabara
    {
      num: 2,
      title: "Classic Tokyo: Markets, Temples & Neon",
      neighborhoods: "Tsukiji · Asakusa · Akihabara",
      date: "May 11",
      mapPins: [
        { lat: 35.6654, lng: 139.7707, label: "Tsukiji Outer Market", num: 1, cat: "food", desc: "World-famous fish market with incredible street food" },
        { lat: 35.7148, lng: 139.7967, label: "Senso-ji Temple", num: 2, cat: "activity", desc: "Tokyo's oldest temple with iconic Thunder Gate" },
        { lat: 35.7100, lng: 139.7963, label: "Nakamise-dori", num: 3, cat: "food", desc: "Traditional shopping street leading to Senso-ji" },
        { lat: 35.7023, lng: 139.7745, label: "Akihabara", num: 4, cat: "activity", desc: "Electric Town — anime, manga, and retro gaming" },
        { lat: 35.6595, lng: 139.7005, label: "Shibuya Crossing", num: 5, cat: "activity", desc: "The world's busiest intersection" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Tsukiji Outer Market", description: "Arrive early (8am) for the freshest sushi, tamagoyaki, and uni. Walk the narrow aisles sampling everything.", details: ["📍 4-16-2 Tsukiji, Chuo City"] }
          ],
          meals: [
            { type: "🍣 Breakfast", name: "Sushi Dai or Daiwa Sushi", description: "Omakase breakfast at the counter. Some of the freshest sushi you'll ever eat.", meta: "¥3,000-5,000 · Arrive by 7:30am to avoid 2hr wait" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Senso-ji Temple & Asakusa", description: "Walk through Kaminarimon (Thunder Gate), browse Nakamise-dori for traditional snacks and souvenirs, then explore the temple grounds.", details: [] },
            { title: "Akihabara Electric Town", description: "Multi-floor arcades, retro game shops, and anime stores. Visit Super Potato for vintage gaming or a maid café for the full experience.", details: [] }
          ],
          meals: [
            { type: "🍜 Lunch", name: "Ramen at Fuunji", description: "Legendary tsukemen (dipping ramen) with rich fish-pork broth. Usually a 30-min wait but moves fast.", meta: "📍 Yoyogi · ¥1,000 · Cash only" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Shibuya Crossing & Shibuya Sky", description: "Experience the iconic crossing, then head up to Shibuya Sky for 360° rooftop views.", details: ["💡 Book Shibuya Sky tickets online in advance — ¥2,000"] }
          ],
          meals: [
            { type: "🍖 Dinner", name: "Uobei Sushi (Genki Sushi)", description: "Fun conveyor-belt sushi where you order on a tablet and plates zoom to your seat on a mini highway.", meta: "📍 Shibuya · ¥2,000-3,000/person" }
          ],
          tips: [{ type: "reddit", text: "Shibuya Sky at sunset is absolutely magical. Book the earliest sunset slot.", cite: "r/JapanTravel" }]
        }
      ]
    },
    // DAY 3 — Harajuku, Meiji, Roppongi
    {
      num: 3,
      title: "Harajuku, Meiji Shrine & Roppongi Art",
      neighborhoods: "Harajuku · Omotesando · Roppongi",
      date: "May 12",
      mapPins: [
        { lat: 35.6764, lng: 139.6993, label: "Meiji Jingu Shrine", num: 1, cat: "activity", desc: "Serene Shinto shrine in a lush forest" },
        { lat: 35.6702, lng: 139.7027, label: "Takeshita Street", num: 2, cat: "activity", desc: "Harajuku's kawaii fashion and crepe street" },
        { lat: 35.6654, lng: 139.7123, label: "Omotesando", num: 3, cat: "activity", desc: "Tokyo's Champs-Élysées — luxury boutiques and architecture" },
        { lat: 35.6604, lng: 139.7292, label: "Roppongi Hills Mori Art Museum", num: 4, cat: "activity", desc: "Contemporary art museum with city view observation deck" },
        { lat: 35.6627, lng: 139.7318, label: "Gonpachi Nishi-Azabu", num: 5, cat: "food", desc: "The restaurant that inspired Kill Bill's fight scene" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Meiji Jingu Shrine", description: "Walk through the towering torii gate into this peaceful forest shrine dedicated to Emperor Meiji. Arrive early for a serene experience.", details: ["📍 1-1 Yoyogikamizonocho, Shibuya"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Bills Omotesando", description: "Famous ricotta hotcakes that are fluffy as clouds. Worth the hype.", meta: "📍 Omotesando · ¥2,000-3,000" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Takeshita Street & Harajuku", description: "Kawaii culture epicenter — wild fashion, themed cafés, and the best crepes in Tokyo.", details: [] },
            { title: "Omotesando Architecture Walk", description: "Stroll this tree-lined boulevard and admire buildings by Tadao Ando, SANAA, and Toyo Ito.", details: [] }
          ],
          meals: [
            { type: "🍜 Lunch", name: "Afuri Ramen (Harajuku)", description: "Light, citrusy yuzu shio ramen. A refreshing change from heavy tonkotsu.", meta: "📍 Harajuku · ¥1,200" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Mori Art Museum & Tokyo City View", description: "Contemporary art exhibitions plus a stunning open-air observation deck on the 52nd floor.", details: ["💡 Open until 10pm — combine art and night views"] }
          ],
          meals: [
            { type: "🍣 Dinner", name: "Gonpachi Nishi-Azabu", description: "The 'Kill Bill restaurant' — great atmosphere, solid izakaya food, and soba noodles.", meta: "📍 Roppongi · ¥4,000-6,000/person" }
          ],
          tips: []
        }
      ]
    },
    // DAY 4 — Toyosu, Teamlab, Odaiba
    {
      num: 4,
      title: "Toyosu Market, teamLab & Tokyo Bay",
      neighborhoods: "Toyosu · Odaiba · Ginza",
      date: "May 13",
      mapPins: [
        { lat: 35.6457, lng: 139.7814, label: "Toyosu Fish Market", num: 1, cat: "food", desc: "Watch the tuna auction and eat the freshest sushi" },
        { lat: 35.6167, lng: 139.7839, label: "teamLab Planets", num: 2, cat: "activity", desc: "Immersive barefoot digital art museum" },
        { lat: 35.6269, lng: 139.7751, label: "Odaiba", num: 3, cat: "activity", desc: "Futuristic waterfront entertainment district" },
        { lat: 35.6717, lng: 139.7649, label: "Ginza", num: 4, cat: "activity", desc: "Tokyo's upscale shopping district" },
        { lat: 35.6710, lng: 139.7656, label: "Kyubey Ginza", num: 5, cat: "food", desc: "Legendary Ginza sushi counter since 1935" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Toyosu Fish Market", description: "Watch the famous tuna auction from the observation deck (arrive by 5:30am), then eat sushi breakfast at the market restaurants.", details: ["💡 Book tuna auction viewing online — limited to 120 visitors/day"] }
          ],
          meals: [
            { type: "🍣 Breakfast", name: "Sushi Dai (Toyosu)", description: "Omakase at the counter inside the market. The chefs slice it right in front of you.", meta: "¥4,000 · Arrive early for shorter wait" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "teamLab Planets", description: "Walk barefoot through stunning immersive digital art installations. You'll wade through water, walk through flowers, and lose yourself in infinity rooms.", details: ["💡 Book tickets online — sells out! Wear pants you can roll up."] }
          ],
          meals: [
            { type: "🍱 Lunch", name: "Odaiba Decks Food Court", description: "Takoyaki, okonomiyaki, and ramen with a waterfront view of Rainbow Bridge.", meta: "¥1,000-2,000" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Ginza Evening Stroll", description: "Window-shop along Chuo-dori (closed to traffic on weekends). Visit the stunning Ginza Six department store.", details: [] }
          ],
          meals: [
            { type: "🍣 Dinner", name: "Kyubey Ginza", description: "One of Tokyo's most celebrated sushi counters. Intimate omakase experience since 1935.", meta: "📍 Ginza · ¥15,000-20,000/person · Reservations essential" }
          ],
          tips: [{ type: "tip", text: "Splurge night! This is your fancy Tokyo dinner. Book well in advance." }]
        }
      ]
    },
    // DAY 5 — Ueno, Yanaka, Sumo
    {
      num: 5,
      title: "Old Tokyo: Yanaka, Ueno & Sumo Culture",
      neighborhoods: "Ueno · Yanaka · Ryogoku",
      date: "May 14",
      mapPins: [
        { lat: 35.7146, lng: 139.7744, label: "Ueno Park", num: 1, cat: "activity", desc: "Sprawling park with museums, temples, and a zoo" },
        { lat: 35.7230, lng: 139.7670, label: "Yanaka Ginza", num: 2, cat: "food", desc: "Charming retro shopping street — old-school Tokyo vibes" },
        { lat: 35.7264, lng: 139.7629, label: "Yanaka Cemetery", num: 3, cat: "activity", desc: "Peaceful cherry tree-lined paths through historic cemetery" },
        { lat: 35.6966, lng: 139.7934, label: "Ryogoku Kokugikan", num: 4, cat: "activity", desc: "National Sumo Stadium — May tournament in session!" },
        { lat: 35.6959, lng: 139.7931, label: "Chanko Nabe Restaurant", num: 5, cat: "food", desc: "Eat the hearty hot pot that sumo wrestlers eat" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Ueno Park & Tokyo National Museum", description: "Japan's oldest and most comprehensive museum. The Japanese Gallery alone is worth 2 hours.", details: ["💡 ¥1,000 entry — JR Pass doesn't cover this"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Kayaba Coffee", description: "100-year-old renovated coffee house in Yanaka. Famous for their egg sandwich and drip coffee.", meta: "📍 Yanaka · ¥800-1,200" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Yanaka District Walk", description: "Tokyo's best-preserved old neighborhood. Wander past wooden houses, tiny temples, and cat statues. Yanaka Ginza street has great snacks.", details: [] },
            { title: "May Grand Sumo Tournament 🏆", description: "The May Basho runs May 10-24 at Ryogoku Kokugikan! Watch live sumo — one of Japan's most thrilling cultural experiences.", details: ["💡 Book tickets at sumo.or.jp as soon as they open. Upper seats ~¥3,800, box seats ~¥11,000"] }
          ],
          meals: [
            { type: "🍲 Lunch", name: "Yanaka Ginza Street Food", description: "Menchi-katsu (fried meat patties), croquettes, and melon-pan from the various stalls.", meta: "¥500-1,000 · Cash only" }
          ],
          tips: [{ type: "reddit", text: "May tournament is perfect timing! Get same-day tickets — line up at Ryogoku by 7am for unreserved seats.", cite: "r/JapanTravel" }]
        },
        {
          label: "Evening",
          activities: [],
          meals: [
            { type: "🍲 Dinner", name: "Tomoegata Chanko Nabe", description: "Authentic sumo hot pot in the sumo district. Rich, protein-packed broth with chicken, tofu, and vegetables.", meta: "📍 Ryogoku · ¥3,000-4,000/person" }
          ],
          tips: []
        }
      ]
    },
    // DAY 6 — Day trip to Kamakura
    {
      num: 6,
      title: "Day Trip: Kamakura's Great Buddha & Coast",
      neighborhoods: "Kamakura · Enoshima",
      date: "May 15",
      mapPins: [
        { lat: 35.3167, lng: 139.5356, label: "Kamakura Station", num: 1, cat: "transport", desc: "1 hour from Shinjuku via JR Shonan-Shinjuku Line" },
        { lat: 35.3168, lng: 139.5360, label: "Komachi-dori Street", num: 2, cat: "food", desc: "Charming shopping street with cafés and snacks" },
        { lat: 35.3167, lng: 139.5356, label: "Tsurugaoka Hachimangu", num: 3, cat: "activity", desc: "Kamakura's most important Shinto shrine" },
        { lat: 35.3117, lng: 139.5357, label: "Great Buddha (Kotoku-in)", num: 4, cat: "activity", desc: "Iconic 13m bronze Buddha statue from 1252" },
        { lat: 35.3003, lng: 139.4800, label: "Enoshima Island", num: 5, cat: "activity", desc: "Scenic island with shrines, caves, and ocean views" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Train to Kamakura", description: "Take JR Shonan-Shinjuku Line from Shinjuku (~1hr, covered by JR Pass).", details: [] },
            { title: "Tsurugaoka Hachimangu Shrine", description: "Kamakura's grandest shrine, set at the end of a beautiful tree-lined approach.", details: [] }
          ],
          meals: [
            { type: "🍡 Breakfast", name: "Komachi-dori Street Snacks", description: "Browse this cute pedestrian street for matcha soft serve, dango, and fresh senbei crackers.", meta: "¥500-1,000" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Great Buddha of Kamakura", description: "Stand before the serene 13-meter bronze Buddha, cast in 1252. You can go inside the hollow statue for ¥50.", details: ["📍 Kotoku-in Temple · ¥300 entry"] },
            { title: "Hase-dera Temple", description: "Beautiful temple with thousands of small Jizo statues and a stunning ocean view from the terrace.", details: [] }
          ],
          meals: [
            { type: "🐟 Lunch", name: "Shirasu-ya", description: "Kamakura's famous raw whitebait (shirasu) rice bowl. Only available fresh here.", meta: "📍 Near Hase Station · ¥1,200-1,800" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Enoshima Island Sunset", description: "Take the Enoden tram to this small island. Climb to the top for panoramic Pacific views. Watch the sunset over Sagami Bay with Mt. Fuji in the background.", details: ["💡 Enoden tram is not covered by JR Pass — ¥260 from Kamakura"] }
          ],
          meals: [
            { type: "🍺 Dinner", name: "Tobiccho", description: "Famous for shirasu pizza and local craft beers with an ocean view.", meta: "📍 Enoshima · ¥2,000-3,000" }
          ],
          tips: [{ type: "reddit", text: "The Enoden tram ride itself is beautiful — it runs right along the coast. Sit on the left side.", cite: "r/JapanTravel" }]
        }
      ]
    },
    // DAY 7 — Hakone
    {
      num: 7,
      title: "Hakone: Hot Springs & Mt. Fuji Views",
      neighborhoods: "Hakone · Owakudani · Lake Ashi",
      date: "May 16",
      mapPins: [
        { lat: 35.2326, lng: 139.1070, label: "Hakone-Yumoto Station", num: 1, cat: "transport", desc: "Gateway to Hakone, 90 min from Shinjuku" },
        { lat: 35.2431, lng: 139.0218, label: "Owakudani Valley", num: 2, cat: "activity", desc: "Volcanic valley with sulfur vents and black eggs" },
        { lat: 35.2040, lng: 139.0274, label: "Lake Ashi", num: 3, cat: "activity", desc: "Scenic lake with pirate ship cruises and Fuji views" },
        { lat: 35.2333, lng: 139.0643, label: "Hakone Open-Air Museum", num: 4, cat: "activity", desc: "Outdoor sculpture park with Picasso gallery" },
        { lat: 35.2326, lng: 139.1070, label: "Ryokan Onsen", num: 5, cat: "lodging", desc: "Stay at a traditional Japanese inn with hot spring baths" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Romance Car to Hakone", description: "Take the iconic Odakyu Romance Car from Shinjuku — reserved seats, big windows, Fuji views.", details: ["💡 ¥2,330 one-way, not covered by JR Pass but worth it"] },
            { title: "Hakone Open-Air Museum", description: "Stunning outdoor sculpture garden with over 120 works set against mountain scenery. Don't miss the Picasso Pavilion.", details: ["¥1,600 entry"] }
          ],
          meals: [],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Hakone Loop: Ropeway → Owakudani → Lake Ashi", description: "Ride the ropeway over volcanic terrain to Owakudani. Eat the famous black eggs (said to add 7 years to your life!), then take the pirate ship across Lake Ashi.", details: ["💡 Hakone Free Pass covers all transport in the loop — ¥6,100 from Shinjuku including Romance Car"] }
          ],
          meals: [
            { type: "🥚 Lunch", name: "Owakudani Black Eggs", description: "Eggs boiled in volcanic sulfur springs — turned black outside, perfect inside. A Hakone must-eat.", meta: "¥500 for 5 eggs" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Ryokan & Onsen Experience", description: "Check into a traditional ryokan. Soak in the natural hot springs (onsen), wear a yukata, and enjoy a kaiseki dinner course.", details: ["💡 Budget ~¥20,000-40,000/person including dinner and breakfast"] }
          ],
          meals: [
            { type: "🍱 Dinner", name: "Ryokan Kaiseki Course", description: "Multi-course traditional dinner served in your room — seasonal dishes, sashimi, grilled fish, pickles, and rice.", meta: "Included with ryokan stay" }
          ],
          tips: [{ type: "reddit", text: "Splurging on one ryokan night is 100% worth it. It's a core Japanese experience you can't replicate anywhere else.", cite: "r/JapanTravel" }]
        }
      ]
    },
    // DAY 8 — Travel to Kanazawa
    {
      num: 8,
      title: "Shinkansen to Kanazawa: Japan's Hidden Gem",
      neighborhoods: "Kanazawa Station · Higashi Chaya · Omicho Market",
      date: "May 17",
      mapPins: [
        { lat: 36.5781, lng: 136.6484, label: "Kanazawa Station", num: 1, cat: "transport", desc: "Stunning wooden drum gate — one of the world's most beautiful stations" },
        { lat: 36.5723, lng: 136.6621, label: "Omicho Market", num: 2, cat: "food", desc: "Kanazawa's 300-year-old 'Kitchen' — fresh seafood and local produce" },
        { lat: 36.5725, lng: 136.6680, label: "Higashi Chaya District", num: 3, cat: "activity", desc: "Beautifully preserved geisha district with teahouses" },
        { lat: 36.5614, lng: 136.6622, label: "Kenroku-en Garden", num: 4, cat: "activity", desc: "One of Japan's Top 3 gardens — stunning in every season" },
        { lat: 36.5600, lng: 136.6570, label: "Kanazawa Castle Park", num: 5, cat: "activity", desc: "Reconstructed castle with beautiful stone walls and gardens" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Shinkansen to Kanazawa", description: "Take the Hokuriku Shinkansen from Tokyo Station (~2.5 hours). The route passes through mountains and tunnels.", details: ["💡 Covered by JR Pass. Reserve seats in advance at a JR ticket office."] }
          ],
          meals: [
            { type: "🍱 Breakfast", name: "Ekiben (Station Bento)", description: "Grab a beautifully packaged train bento at Tokyo Station — it's a Japanese ritual.", meta: "📍 Tokyo Station · ¥1,000-1,500" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Omicho Market", description: "Kanazawa's 'kitchen' since 1721. Try fresh crab, uni, and the famous kaisendon (seafood rice bowl).", details: ["📍 Open 9am-5pm, some stalls close early"] },
            { title: "Higashi Chaya District", description: "Wander the wooden-latticed teahouses of this Edo-era geisha district. Visit Kaikaro teahouse for gold-leaf tea.", details: [] }
          ],
          meals: [
            { type: "🦀 Lunch", name: "Omicho Market Kaisendon", description: "Massive bowl of rice topped with the day's freshest seafood — uni, ikura, crab, and more.", meta: "¥2,000-3,500 · Various stalls" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Kenroku-en Garden Evening", description: "One of Japan's three most beautiful gardens. May brings irises and fresh green foliage. Wander the bridges, streams, and historic teahouses.", details: ["¥320 entry · Open until 6pm in May"] }
          ],
          meals: [
            { type: "🍣 Dinner", name: "Mori Mori Sushi (Kanazawa)", description: "Popular revolving sushi featuring Kanazawa's exceptional Japan Sea fish. Nodoguro (blackthroat seaperch) is the local specialty.", meta: "📍 Near Kanazawa Station · ¥2,500-4,000" }
          ],
          tips: [{ type: "reddit", text: "Kanazawa has arguably better sushi than Tokyo because of direct access to Japan Sea fish. Don't skip nodoguro!", cite: "r/JapanTravel" }]
        }
      ]
    },
    // DAY 9 — Kanazawa Day 2
    {
      num: 9,
      title: "Kanazawa: Samurai, Gold Leaf & Craft",
      neighborhoods: "Nagamachi · 21st Century Museum · Kazuemachi",
      date: "May 18",
      mapPins: [
        { lat: 36.5624, lng: 136.6522, label: "Nagamachi Samurai District", num: 1, cat: "activity", desc: "Atmospheric samurai residential quarter with earthen walls" },
        { lat: 36.5607, lng: 136.6587, label: "21st Century Museum of Contemporary Art", num: 2, cat: "activity", desc: "Free-form circular building with incredible installations" },
        { lat: 36.5709, lng: 136.6607, label: "Hakuza Gold Leaf Shop", num: 3, cat: "activity", desc: "Try gold leaf ice cream and watch artisans at work" },
        { lat: 36.5695, lng: 136.6627, label: "Kazuemachi Chaya", num: 4, cat: "activity", desc: "Quieter geisha district along the Asano River" },
        { lat: 36.5615, lng: 136.6550, label: "Tamazushi", num: 5, cat: "food", desc: "Top-rated local sushi spot loved by Kanazawa residents" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Nagamachi Samurai District", description: "Walk the atmospheric earthen-walled lanes where samurai once lived. Visit the Nomura Samurai House for a peek inside.", details: ["Nomura House: ¥550 · Beautiful tiny garden rated in top Japanese gardens"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Fumuroya Café", description: "Traditional Kanazawa confections with matcha in a beautifully restored merchant house.", meta: "📍 Nagamachi · ¥1,000-1,500" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "21st Century Museum of Contemporary Art", description: "Leandro Erlich's Swimming Pool (you can look down into a room through 'water') is the star, but the whole museum is fantastic. Free areas + paid exhibitions.", details: ["💡 Free zones open until 10pm. Paid exhibitions ¥1,200."] },
            { title: "Gold Leaf Experience", description: "Kanazawa produces 99% of Japan's gold leaf. Visit Hakuza to see artisans hammer gold into impossibly thin sheets, then eat gold-leaf ice cream.", details: [] }
          ],
          meals: [
            { type: "🍱 Lunch", name: "Ippuku (Higashi Chaya)", description: "Matcha and traditional wagashi sweets in a converted Edo-era teahouse.", meta: "¥800-1,200" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Kazuemachi Evening Walk", description: "The quieter geisha district comes alive at dusk. Stroll along the Asano River and listen for shamisen music drifting from teahouses.", details: [] }
          ],
          meals: [
            { type: "🍣 Dinner", name: "Tamazushi", description: "Intimate counter sushi where the chef selects the best catches. A local favorite, not touristy at all.", meta: "📍 Kanazawa · ¥5,000-8,000/person · Reservations recommended" }
          ],
          tips: []
        }
      ]
    },
    // DAY 10 — Takayama
    {
      num: 10,
      title: "Takayama: Edo Streets & Mountain Culture",
      neighborhoods: "Takayama Old Town · Miyagawa Morning Market",
      date: "May 19",
      mapPins: [
        { lat: 36.1408, lng: 137.2521, label: "Takayama Station", num: 1, cat: "transport", desc: "Scenic train ride through Japanese Alps from Kanazawa" },
        { lat: 36.1399, lng: 137.2584, label: "Sanmachi Suji (Old Town)", num: 2, cat: "activity", desc: "Perfectly preserved Edo-period merchant streets" },
        { lat: 36.1420, lng: 137.2560, label: "Miyagawa Morning Market", num: 3, cat: "food", desc: "Riverside market with local produce, pickles, and crafts" },
        { lat: 36.1476, lng: 137.2528, label: "Takayama Jinya", num: 4, cat: "activity", desc: "Only surviving Edo-era government building in Japan" },
        { lat: 36.1388, lng: 137.2599, label: "Hida Beef Restaurant", num: 5, cat: "food", desc: "Takayama is famous for Hida beef — rivals Kobe" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Train to Takayama", description: "Take the Wide View Hida limited express through the spectacular Japanese Alps. One of Japan's most scenic train rides.", details: ["💡 ~2.5 hours from Kanazawa (transfer at Toyama). JR Pass covers it."] },
            { title: "Miyagawa Morning Market", description: "Stroll the riverside market for local pickles, miso, crafts, and fresh produce from the surrounding mountains.", details: ["Open 6am-noon daily"] }
          ],
          meals: [
            { type: "🍡 Breakfast", name: "Miyagawa Market Stalls", description: "Mitarashi dango (grilled rice dumplings with soy glaze) and apple juice from local orchards.", meta: "¥300-800" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Sanmachi Suji (Old Town)", description: "Three streets of dark-wood merchant houses from the Edo period. Sake breweries marked by sugidama (cedar balls) above the door — duck in for tastings.", details: [] },
            { title: "Sake Brewery Hopping", description: "Visit 2-3 of the six breweries on Sanmachi Suji. Look for the cedar ball signs. ¥200-500 gets you a tasting flight.", details: [] }
          ],
          meals: [
            { type: "🥩 Lunch", name: "Center4 Hamburgers", description: "Cult-favorite spot serving Hida beef burgers. Sounds weird for Japan but it's legendary.", meta: "📍 Old Town · ¥1,500-2,500" }
          ],
          tips: [{ type: "reddit", text: "Walk into every sake brewery you see in Takayama. The tastings are cheap and the quality is incredible.", cite: "r/JapanTravel" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Takayama Jinya", description: "The only surviving Edo-era government office. Beautiful tatami rooms and a torture chamber (yes, really).", details: ["¥440 entry"] }
          ],
          meals: [
            { type: "🥩 Dinner", name: "Maruaki (Hida Beef)", description: "A5 Hida beef — Takayama's answer to Kobe. Try the sukiyaki or grilled steak set. Melt-in-your-mouth marbling.", meta: "📍 Takayama · ¥5,000-10,000/person" }
          ],
          tips: []
        }
      ]
    },
    // DAY 11 — Shirakawa-go Day Trip + Travel to Kyoto
    {
      num: 11,
      title: "Shirakawa-go & Journey to Kyoto",
      neighborhoods: "Shirakawa-go · Kyoto Station",
      date: "May 20",
      mapPins: [
        { lat: 36.2578, lng: 136.9060, label: "Shirakawa-go Village", num: 1, cat: "activity", desc: "UNESCO World Heritage thatched-roof village" },
        { lat: 36.2612, lng: 136.9063, label: "Shiroyama Viewpoint", num: 2, cat: "activity", desc: "Panoramic viewpoint overlooking the entire village" },
        { lat: 36.2575, lng: 136.9055, label: "Wada House", num: 3, cat: "activity", desc: "Largest and oldest gassho-zukuri farmhouse, now a museum" },
        { lat: 34.9856, lng: 135.7584, label: "Kyoto Station", num: 4, cat: "transport", desc: "Arrive in Kyoto — your base for the next 5 nights" },
        { lat: 35.0037, lng: 135.7785, label: "Pontocho Alley", num: 5, cat: "food", desc: "Atmospheric narrow alley of restaurants along the Kamo River" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Bus to Shirakawa-go", description: "Take the Nohi Bus from Takayama (50 min, ~¥2,600). Arrive at the UNESCO village of steep thatched-roof farmhouses nestled in the mountains.", details: ["💡 Not covered by JR Pass. Book bus tickets in advance at Takayama Bus Center."] },
            { title: "Shirakawa-go Village Exploration", description: "Walk among 114 traditional gassho-zukuri houses (named for the 'praying hands' roof shape). Visit Wada House museum and climb to Shiroyama Viewpoint.", details: [] }
          ],
          meals: [
            { type: "🍲 Lunch", name: "Irori (Shirakawa-go)", description: "Eat around a traditional sunken hearth. Try hoba miso (miso grilled on magnolia leaf) — a Hida specialty.", meta: "¥1,500-2,500" }
          ],
          tips: [{ type: "reddit", text: "Shirakawa-go is magical but gets crowded by 10am. Take the first bus from Takayama.", cite: "r/JapanTravel" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Bus back to Takayama → Shinkansen to Kyoto", description: "Return to Takayama, then take the Wide View Hida to Nagoya and transfer to the Tokaido Shinkansen to Kyoto. Total ~4 hours.", details: ["💡 All covered by JR Pass except Takayama-Shirakawa bus"] }
          ],
          meals: [],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Arrive in Kyoto & Pontocho Alley", description: "Check into your hotel and stroll Pontocho — a narrow lantern-lit alley along the Kamo River packed with intimate restaurants.", details: [] }
          ],
          meals: [
            { type: "🍶 Dinner", name: "Pontocho Izakaya", description: "Pick any spot with a kawadoko (river terrace). In May the terraces are open — eat above the river!", meta: "📍 Pontocho · ¥3,000-5,000/person" }
          ],
          tips: [{ type: "tip", text: "Kawadoko (riverside dining terraces) open in May. Request a terrace seat — it's magical at night." }]
        }
      ]
    },
    // DAY 12 — Kyoto East
    {
      num: 12,
      title: "Eastern Kyoto: Fushimi Inari & Kiyomizu",
      neighborhoods: "Fushimi · Higashiyama · Gion",
      date: "May 21",
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: "Fushimi Inari Shrine", num: 1, cat: "activity", desc: "10,000 vermillion torii gates winding up the mountain" },
        { lat: 34.9949, lng: 135.7850, label: "Kiyomizu-dera Temple", num: 2, cat: "activity", desc: "Iconic hilltop temple with stunning wooden stage" },
        { lat: 34.9986, lng: 135.7753, label: "Ninenzaka & Sannenzaka", num: 3, cat: "activity", desc: "Photogenic preserved streets with traditional shops" },
        { lat: 35.0036, lng: 135.7748, label: "Gion District", num: 4, cat: "activity", desc: "Historic geisha district — spot maiko at dusk" },
        { lat: 35.0048, lng: 135.7724, label: "Nishiki Market", num: 5, cat: "food", desc: "Kyoto's 400-year-old 'Kitchen' — 5 blocks of food stalls" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Fushimi Inari at Dawn", description: "Arrive by 6am for the famous torii gate tunnels almost to yourself. Hike partway up the mountain (30-60 min) for incredible views.", details: ["💡 Free entry, open 24/7. Early morning = no crowds."] }
          ],
          meals: [
            { type: "🍡 Breakfast", name: "Fushimi Inari Street Stalls", description: "Inari sushi (named after this shrine!), kitsune udon, and grilled sparrow (adventurous!) at the shrine approach.", meta: "¥500-1,000" }
          ],
          tips: [{ type: "reddit", text: "Go to Fushimi Inari at 5:30am. Seriously. By 9am it's a zoo. The sunrise through the gates is otherworldly.", cite: "r/JapanTravel" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Nishiki Market", description: "Five blocks of Kyoto's culinary soul. Try yuba (tofu skin), tsukemono (pickles), matcha everything, and mochi.", details: ["📍 Nishiki-koji Dori · Most stalls close by 5pm"] },
            { title: "Kiyomizu-dera Temple", description: "Perched on a hillside, this temple's massive wooden stage offers sweeping views of Kyoto. Walk the charming Ninenzaka and Sannenzaka lanes to get there.", details: ["¥400 entry · Open 6am-6pm"] }
          ],
          meals: [
            { type: "🍜 Lunch", name: "Nishiki Market Grazing", description: "Eat your way through — tamagoyaki on a stick, grilled mochi, soy milk donuts, and fresh dashi.", meta: "¥1,500-2,500 total" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Gion District at Dusk", description: "Walk Hanamikoji-dori and the back streets of Gion. If you're lucky, you'll spot a maiko (apprentice geisha) hurrying to an evening engagement.", details: ["💡 Be respectful — don't chase or block geiko/maiko for photos"] }
          ],
          meals: [
            { type: "🍱 Dinner", name: "Gion Kappa (Kappo Cuisine)", description: "Refined Kyoto-style kappo cooking at the counter. Seasonal dishes prepared right in front of you.", meta: "📍 Gion · ¥6,000-10,000/person" }
          ],
          tips: []
        }
      ]
    },
    // DAY 13 — Kyoto West (Arashiyama)
    {
      num: 13,
      title: "Arashiyama: Bamboo, Monkeys & River",
      neighborhoods: "Arashiyama · Sagano",
      date: "May 22",
      mapPins: [
        { lat: 35.0094, lng: 135.6722, label: "Arashiyama Bamboo Grove", num: 1, cat: "activity", desc: "Towering bamboo forest — one of Japan's most iconic sights" },
        { lat: 35.0155, lng: 135.6748, label: "Tenryu-ji Temple", num: 2, cat: "activity", desc: "UNESCO World Heritage Zen temple with stunning garden" },
        { lat: 35.0106, lng: 135.6662, label: "Togetsukyo Bridge", num: 3, cat: "activity", desc: "Iconic bridge crossing the Hozu River" },
        { lat: 35.0084, lng: 135.6791, label: "Iwatayama Monkey Park", num: 4, cat: "activity", desc: "Hilltop park with 120 wild Japanese macaques and Kyoto views" },
        { lat: 35.0283, lng: 135.6656, label: "Otagi Nenbutsu-ji", num: 5, cat: "activity", desc: "Hidden temple with 1,200 unique moss-covered stone statues" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Arashiyama Bamboo Grove", description: "Get here by 7am to experience the soaring bamboo without crowds. The morning light filtering through is magical.", details: ["💡 Free · Take JR Sagano Line from Kyoto Station (15 min)"] },
            { title: "Tenryu-ji Temple & Garden", description: "UNESCO site with one of Kyoto's finest Zen gardens designed in the 14th century. The garden is the star — skip the interior.", details: ["Garden ¥500 · Opens 8:30am"] }
          ],
          meals: [
            { type: "🍵 Breakfast", name: "% Arabica Arashiyama", description: "The famous single-origin coffee shop right on the river. Beautiful setting, excellent espresso.", meta: "📍 Togetsukyo area · ¥500-800" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Iwatayama Monkey Park", description: "Climb 20 min up the hill to hang out with 120 wild macaques. You feed them — they don't feed on you. Incredible city views from the top.", details: ["¥550 entry"] },
            { title: "Otagi Nenbutsu-ji (Hidden Gem!)", description: "20-minute walk from the bamboo grove through quiet Sagano. 1,200 unique stone Buddhist statues covered in moss — each with a different expression. Few tourists make it here.", details: ["¥300 entry · One of Kyoto's best-kept secrets"] }
          ],
          meals: [
            { type: "🍜 Lunch", name: "Yoshimura Soba", description: "Handmade buckwheat soba with a view of Togetsukyo Bridge and the Hozu River.", meta: "📍 Arashiyama · ¥1,200-1,800" }
          ],
          tips: [{ type: "reddit", text: "Otagi Nenbutsu-ji is the single best hidden gem in Kyoto. Almost no tourists. The statues are incredible.", cite: "r/JapanTravel" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Sagano Scenic Railway", description: "Take the romantic open-air train along the Hozu River gorge. 25 minutes of beautiful scenery.", details: ["¥880 · Runs from Saga-Torokko Station"] }
          ],
          meals: [
            { type: "🍶 Dinner", name: "Musubi Cafe (Arashiyama)", description: "Creative obanzai (Kyoto home-style cooking) — seasonal small plates with local sake.", meta: "📍 Arashiyama · ¥3,000-4,000/person" }
          ],
          tips: []
        }
      ]
    },
    // DAY 14 — Kyoto: Kinkaku-ji, Ryoan-ji, Cooking Class
    {
      num: 14,
      title: "Golden Temple, Zen Gardens & Cooking Class",
      neighborhoods: "Kinkaku-ji · Ryoan-ji · Central Kyoto",
      date: "May 23",
      mapPins: [
        { lat: 35.0394, lng: 135.7292, label: "Kinkaku-ji (Golden Pavilion)", num: 1, cat: "activity", desc: "The iconic gold-leaf temple reflected in its mirror pond" },
        { lat: 35.0345, lng: 135.7184, label: "Ryoan-ji Temple", num: 2, cat: "activity", desc: "Japan's most famous rock garden — 15 stones in raked gravel" },
        { lat: 35.0264, lng: 135.7136, label: "Ninna-ji Temple", num: 3, cat: "activity", desc: "UNESCO temple with late-blooming cherry trees" },
        { lat: 35.0093, lng: 135.7688, label: "Hana Cooking Class", num: 4, cat: "activity", desc: "Hands-on Japanese cooking class — make ramen, gyoza, or sushi" },
        { lat: 35.0040, lng: 135.7690, label: "Kichi Kichi Omurice", num: 5, cat: "food", desc: "Viral omurice performance — must-book restaurant" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Kinkaku-ji (Golden Pavilion)", description: "Arrive at opening (9am) for the best photos. The gold-leaf covered pavilion reflecting in the pond is surreal.", details: ["¥500 entry · Your 'ticket' is a lucky charm"] },
            { title: "Ryoan-ji Rock Garden", description: "The enigmatic 15-stone rock garden — you can never see all 15 from any single vantage point. Sit and contemplate.", details: ["¥500 entry · 10-minute walk from Kinkaku-ji"] }
          ],
          meals: [
            { type: "🍵 Breakfast", name: "Sarasa Nishijin", description: "Café in a converted 1930s bathhouse. Beautiful tiles, great breakfast sets, strong coffee.", meta: "📍 Nishijin · ¥1,000-1,500" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Japanese Cooking Class", description: "Hands-on class making dashi, sushi rolls, tempura, and miso soup. Learn techniques you'll use at home forever.", details: ["💡 Book via Airbnb Experiences or WAK Japan · ~¥6,000-8,000/person"] }
          ],
          meals: [
            { type: "🍣 Lunch", name: "Your Own Cooking!", description: "Eat what you made in the class — it's always delicious and satisfying.", meta: "Included in class fee" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [],
          meals: [
            { type: "🍳 Dinner", name: "Kichi Kichi Omurice", description: "The famous theatrical omurice — Chef Motokichi flips the egg dramatically onto your rice. A viral sensation for a reason.", meta: "📍 Pontocho · ¥1,500-2,000 · Book via Instagram DM weeks ahead" }
          ],
          tips: [{ type: "reddit", text: "Book Kichi Kichi ASAP via their Instagram. Tables for 2 are easiest to get. It's a 10-minute show + meal.", cite: "r/JapanTravel" }]
        }
      ]
    },
    // DAY 15 — Day trip to Nara
    {
      num: 15,
      title: "Day Trip: Nara's Deer & Ancient Temples",
      neighborhoods: "Nara Park · Naramachi",
      date: "May 24",
      mapPins: [
        { lat: 34.6851, lng: 135.8048, label: "Nara Station", num: 1, cat: "transport", desc: "45 min from Kyoto via JR Nara Line" },
        { lat: 34.6851, lng: 135.8398, label: "Nara Park", num: 2, cat: "activity", desc: "1,200+ wild deer roam freely — buy shika senbei to feed them" },
        { lat: 34.6890, lng: 135.8398, label: "Todai-ji Temple", num: 3, cat: "activity", desc: "World's largest wooden building housing a 15m bronze Buddha" },
        { lat: 34.6812, lng: 135.8432, label: "Kasuga-taisha Shrine", num: 4, cat: "activity", desc: "Ancient shrine with 3,000 stone and bronze lanterns" },
        { lat: 34.6750, lng: 135.8300, label: "Naramachi", num: 5, cat: "food", desc: "Charming old merchant quarter with cafés and craft shops" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "JR to Nara + Nara Park", description: "45-min train from Kyoto (JR Pass). Deer greet you almost immediately. Buy shika senbei (¥200) and bow to the deer — they bow back!", details: ["💡 Be careful — the deer can be aggressive for crackers. Raise your hands empty to show you're out."] }
          ],
          meals: [
            { type: "🍡 Breakfast", name: "Nakatanidou Mochi Shop", description: "Watch the famous mochi pounding performance — two men pound rice at lightning speed. Fresh mochi is heavenly.", meta: "📍 Near Kintetsu Nara Station · ¥400" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Todai-ji Temple", description: "Home to the Great Buddha (Daibutsu) — a 15-meter bronze statue inside the world's largest wooden building. The scale is breathtaking.", details: ["¥600 entry"] },
            { title: "Kasuga-taisha Shrine", description: "Walk through the forest to this shrine famous for its 3,000 stone and bronze lanterns. In the inner sanctum, all lanterns are lit in the darkness.", details: ["¥500 for inner sanctum"] }
          ],
          meals: [
            { type: "🍜 Lunch", name: "Kakinoha Sushi (Tanaka)", description: "Nara's signature dish — sushi wrapped in persimmon leaves. Delicate, slightly fermented, unique.", meta: "📍 Naramachi · ¥1,000-1,500" }
          ],
          tips: [{ type: "reddit", text: "Todai-ji is genuinely awe-inspiring — photos don't capture the scale. Even the 'small' side buildings dwarf normal temples.", cite: "r/JapanTravel" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Naramachi Stroll", description: "Wander the old merchant quarter. Traditional machiya townhouses now house cafés, galleries, and craft shops.", details: [] }
          ],
          meals: [
            { type: "🍺 Dinner", name: "Harushika Sake Brewery", description: "Nara's oldest sake brewery (est. 1884). Tour and tasting, then dinner at their attached restaurant.", meta: "📍 Naramachi · ¥3,000-5,000" }
          ],
          tips: []
        }
      ]
    },
    // DAY 16 — Kyoto Final Day: Tea Ceremony & Shopping
    {
      num: 16,
      title: "Kyoto: Tea Ceremony, Philosophy Path & Farewell",
      neighborhoods: "Nanzen-ji · Philosopher's Path · Downtown",
      date: "May 25",
      mapPins: [
        { lat: 35.0112, lng: 135.7923, label: "Nanzen-ji Temple", num: 1, cat: "activity", desc: "Massive Zen temple complex with iconic brick aqueduct" },
        { lat: 35.0214, lng: 135.7942, label: "Philosopher's Path", num: 2, cat: "activity", desc: "2km canal-side path between Nanzen-ji and Ginkaku-ji" },
        { lat: 35.0268, lng: 135.7982, label: "Ginkaku-ji (Silver Pavilion)", num: 3, cat: "activity", desc: "Wabi-sabi masterpiece with zen sand garden" },
        { lat: 35.0050, lng: 135.7780, label: "Camellia Tea Ceremony", num: 4, cat: "activity", desc: "Traditional tea ceremony experience in a tatami room" },
        { lat: 35.0046, lng: 135.7682, label: "Ippodo Tea Co.", num: 5, cat: "food", desc: "Kyoto's finest tea shop since 1717 — matcha tasting room" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Nanzen-ji Temple", description: "One of Kyoto's most impressive temples. Walk through the massive Sanmon gate and discover the surprising brick aqueduct — a relic of Japan's Meiji modernization.", details: ["¥600 for Sanmon gate · Grounds free"] },
            { title: "Philosopher's Path", description: "2km stone path along a cherry-tree-lined canal connecting Nanzen-ji to Ginkaku-ji. In May, lush green replaces the famous blossoms.", details: ["Free · Allow 45-60 min"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Blue Bottle Coffee Kyoto", description: "Set in a beautiful 100-year-old machiya townhouse. Kyoto meets third-wave coffee.", meta: "📍 Nanzenji area · ¥600-1,000" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Tea Ceremony Experience", description: "Participate in a traditional matcha tea ceremony. A tea master guides you through every movement — it's meditative and deeply cultural.", details: ["💡 Camellia Tea Ceremony near Gion — ¥3,000/person, English-speaking host"] },
            { title: "Ippodo Tea Co.", description: "Buy exceptional matcha, sencha, and gyokuro to take home. Their tasting room lets you prepare and compare teas.", details: ["📍 Teramachi-dori · Since 1717"] }
          ],
          meals: [
            { type: "🍱 Lunch", name: "Omen (Ginkaku-ji)", description: "Handmade udon with seasonal vegetables in a beautiful wooden restaurant near the Silver Pavilion.", meta: "📍 Philosopher's Path · ¥1,200-1,800" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Kyoto Farewell at Kamo River", description: "Grab drinks and snacks and sit along the Kamo River banks. Locals gather here at sunset — it's Kyoto at its most relaxed.", details: [] }
          ],
          meals: [
            { type: "🍖 Dinner", name: "Hafuu (Kyoto Wagyu)", description: "Refined wagyu steak house. Their course menu lets you try different cuts and preparations.", meta: "📍 Kawaramachi · ¥8,000-15,000/person" }
          ],
          tips: [{ type: "tip", text: "Last night in Kyoto. Take a moment at the Kamo River to reflect on the journey so far." }]
        }
      ]
    },
    // DAY 17 — Osaka
    {
      num: 17,
      title: "Osaka: Street Food Capital of Japan",
      neighborhoods: "Dotonbori · Shinsekai · Namba",
      date: "May 26",
      mapPins: [
        { lat: 34.6687, lng: 135.5013, label: "Osaka Station", num: 1, cat: "transport", desc: "15 min shinkansen from Kyoto" },
        { lat: 34.6686, lng: 135.5024, label: "Dotonbori", num: 2, cat: "food", desc: "Neon-lit canal street — Japan's street food mecca" },
        { lat: 34.6523, lng: 135.5062, label: "Shinsekai", num: 3, cat: "food", desc: "Retro district famous for kushikatsu (fried skewers)" },
        { lat: 34.6873, lng: 135.5262, label: "Osaka Castle", num: 4, cat: "activity", desc: "Iconic 16th-century castle surrounded by beautiful park" },
        { lat: 34.6544, lng: 135.5065, label: "Tsutenkaku Tower", num: 5, cat: "activity", desc: "Retro observation tower — symbol of Shinsekai" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Train to Osaka + Osaka Castle", description: "Quick 15-min shinkansen from Kyoto (JR Pass). Drop bags, then visit the impressive castle and its expansive park.", details: ["¥600 entry to main tower · Park is free"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "LiLo Coffee Roasters", description: "Specialty coffee in a tiny Osaka shop. Their pour-over is exceptional.", meta: "📍 Shinsaibashi · ¥500-800" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Shinsekai District", description: "This retro neighborhood feels like 1960s Japan. Colorful signs, pachinko parlors, and the best kushikatsu (deep-fried skewers) in the country.", details: [] }
          ],
          meals: [
            { type: "🍢 Lunch", name: "Daruma Kushikatsu (Shinsekai)", description: "The most famous kushikatsu spot. Dip each skewer once in the communal sauce — NEVER double dip!", meta: "📍 Shinsekai · ¥1,500-2,500 · Look for the angry chef statue" }
          ],
          tips: [{ type: "reddit", text: "Osaka's food motto is kuidaore — eat until you drop. Pace yourself because Dotonbori at night is non-negotiable.", cite: "r/JapanTravel" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Dotonbori Street Food Marathon", description: "THE iconic Osaka experience. Neon signs reflecting in the canal, giant mechanical crabs, and endless food stalls. This is Japan's food capital.", details: ["📍 Along Dotonbori Canal · Best after dark"] }
          ],
          meals: [
            { type: "🐙 Dinner", name: "Dotonbori Crawl", description: "Takoyaki at Wanaka, okonomiyaki at Mizuno, gyoza at Chao Chao, crab at Kani Doraku. Eat everything.", meta: "📍 Dotonbori · ¥3,000-5,000 total for all the hits" }
          ],
          tips: [{ type: "reddit", text: "Mizuno okonomiyaki > Chibo. The yam-based batter is next level. Get the mixed seafood.", cite: "r/JapanTravel" }]
        }
      ]
    },
    // DAY 18 — Osaka Day 2 + Kuromon Market
    {
      num: 18,
      title: "Osaka: Kuromon Market, Umeda & Nightlife",
      neighborhoods: "Kuromon · Umeda · Amerikamura",
      date: "May 27",
      mapPins: [
        { lat: 34.6627, lng: 135.5067, label: "Kuromon Market", num: 1, cat: "food", desc: "Osaka's Kitchen — 170+ stalls of seafood, fruit, and street food" },
        { lat: 34.7055, lng: 135.5002, label: "Umeda Sky Building", num: 2, cat: "activity", desc: "Floating Garden Observatory — futuristic rooftop with 360° views" },
        { lat: 34.6724, lng: 135.4987, label: "Amerikamura", num: 3, cat: "activity", desc: "Osaka's youth culture hub — vintage shops, street art, cafés" },
        { lat: 34.6694, lng: 135.5012, label: "Hozenji Yokocho", num: 4, cat: "food", desc: "Atmospheric narrow alley with a moss-covered Buddha" },
        { lat: 34.6930, lng: 135.5022, label: "Tenjinbashisuji Shopping Street", num: 5, cat: "activity", desc: "Japan's longest shopping arcade — 2.6km of shops and food" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Kuromon Market", description: "Osaka's 'Kitchen' — 170+ stalls selling everything from ¥1,000 tuna sashimi to ¥5,000 A5 wagyu on a stick, torched right in front of you.", details: ["📍 Opens 9am · Best before noon"] }
          ],
          meals: [
            { type: "🍣 Breakfast", name: "Kuromon Market Grazing", description: "Fresh uni, king crab legs, wagyu skewers, tamagoyaki, and seasonal fruit. Eat your way through.", meta: "¥3,000-5,000 · Cash helpful" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Amerikamura & Vintage Shopping", description: "Osaka's Harajuku — thrift shops, street art, and the famous Triangle Park people-watching scene.", details: [] },
            { title: "Umeda Sky Building", description: "Two towers connected by a rooftop 'Floating Garden' observatory. The escalator ride up through the void between towers is thrilling.", details: ["¥1,500 entry · Open until 10:30pm"] }
          ],
          meals: [
            { type: "🍜 Lunch", name: "Kinryu Ramen (Dotonbori)", description: "Iconic 24hr ramen joint with the dragon sign. Tonkotsu ramen for ¥600. No frills, all flavor.", meta: "📍 Dotonbori · ¥600-900 · Cash only" }
          ],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Hozenji Yokocho", description: "Atmospheric narrow alley hidden behind Dotonbori. Splash water on the moss-covered Fudo Myo-o statue for good luck, then duck into a tiny bar.", details: [] }
          ],
          meals: [
            { type: "🍖 Dinner", name: "Yakiniku M (Namba)", description: "Premium yakiniku (Japanese BBQ) — grill A5 wagyu at your table. The tongue and kalbi are exceptional.", meta: "📍 Namba · ¥5,000-8,000/person" }
          ],
          tips: [{ type: "tip", text: "Osaka nightlife is legendary. Check out the bars around Ura-Namba for the local scene." }]
        }
      ]
    },
    // DAY 19 — Day trip to Hiroshima & Miyajima
    {
      num: 19,
      title: "Day Trip: Hiroshima & Miyajima Island",
      neighborhoods: "Hiroshima Peace Park · Miyajima Island",
      date: "May 28",
      mapPins: [
        { lat: 34.3955, lng: 132.4536, label: "Hiroshima Peace Memorial Park", num: 1, cat: "activity", desc: "Powerful memorial and museum dedicated to the atomic bombing" },
        { lat: 34.3955, lng: 132.4534, label: "Atomic Bomb Dome", num: 2, cat: "activity", desc: "UNESCO World Heritage — only structure left standing near the hypocenter" },
        { lat: 34.2965, lng: 132.3197, label: "Miyajima Island", num: 3, cat: "activity", desc: "Sacred island with the famous floating torii gate" },
        { lat: 34.2961, lng: 132.3198, label: "Itsukushima Shrine", num: 4, cat: "activity", desc: "Iconic shrine with torii gate that appears to float at high tide" },
        { lat: 34.3953, lng: 132.4594, label: "Okonomimura", num: 5, cat: "food", desc: "3-floor building packed with Hiroshima-style okonomiyaki stalls" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Shinkansen to Hiroshima", description: "1.5 hours from Osaka via Nozomi (or Sakura/Hikari with JR Pass). Arrive by 9am.", details: ["💡 JR Pass covers Sakura/Hikari shinkansen. Nozomi requires a supplement."] },
            { title: "Hiroshima Peace Memorial Park & Museum", description: "Walk through the park, see the Atomic Bomb Dome, visit the deeply moving museum. Allow 2 hours for the museum.", details: ["¥200 museum entry · Profoundly impactful experience"] }
          ],
          meals: [
            { type: "🥞 Lunch", name: "Okonomimura", description: "3-floor building with 24 okonomiyaki stalls. Hiroshima-style layers noodles into the pancake — totally different from Osaka style.", meta: "📍 Shintenchi · ¥1,000-1,500" }
          ],
          tips: [{ type: "tip", text: "The Peace Museum is emotionally heavy. Take your time and be respectful. It's one of the most important places in the world." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Ferry to Miyajima Island", description: "JR Ferry from Miyajimaguchi (15 min, covered by JR Pass). Spot the floating torii gate from the ferry!", details: ["💡 Check tide times — torii gate is 'floating' at high tide, walkable at low tide. Both are special."] },
            { title: "Itsukushima Shrine & Torii Gate", description: "The iconic vermillion torii gate appears to float on water at high tide. Walk out to touch it at low tide. The shrine itself is built on stilts over the water.", details: ["¥300 shrine entry"] }
          ],
          meals: [],
          tips: []
        },
        {
          label: "Evening",
          activities: [
            { title: "Miyajima at Dusk", description: "After the day-trippers leave, Miyajima becomes magical. Deer roam the quiet streets, lanterns light up, and the torii gate glows.", details: ["💡 If you have time, hike up Mt. Misen (1.5hrs) or take the ropeway for island panoramas"] }
          ],
          meals: [
            { type: "🦪 Dinner", name: "Miyajima Grilled Oysters", description: "Miyajima is famous for giant grilled oysters. Stalls line the main shopping street — ¥200-400 per oyster.", meta: "📍 Miyajima Omotesando · ¥1,500-3,000" }
          ],
          tips: [{ type: "reddit", text: "If you can time it, Miyajima at sunset with the torii gate lit up is the single most beautiful thing in Japan.", cite: "r/JapanTravel" }]
        }
      ]
    },
    // DAY 20 — Osaka Final Day & Departure
    {
      num: 20,
      title: "Final Day: Last Bites & Sayonara",
      neighborhoods: "Namba · Shinsaibashi · Kansai Airport",
      date: "May 29",
      mapPins: [
        { lat: 34.6659, lng: 135.5013, label: "Namba Yasaka Shrine", num: 1, cat: "activity", desc: "Unique shrine with a giant lion head stage" },
        { lat: 34.6746, lng: 135.5019, label: "Shinsaibashi-suji", num: 2, cat: "activity", desc: "Covered shopping arcade — last-minute souvenirs" },
        { lat: 34.6628, lng: 135.5008, label: "Rikuro's Cheesecake", num: 3, cat: "food", desc: "Osaka's famous jiggly cheesecake — watch them wobble" },
        { lat: 34.6686, lng: 135.5024, label: "Dotonbori (One Last Time)", num: 4, cat: "food", desc: "Final takoyaki and photo with the Glico Running Man" },
        { lat: 34.4349, lng: 135.2441, label: "Kansai International Airport", num: 5, cat: "transport", desc: "Fly home from KIX — 50 min by Nankai Rapi:t from Namba" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Namba Yasaka Shrine", description: "A unique shrine featuring a giant lion head stage (Ema-den). It's said to swallow evil spirits and bring good luck.", details: ["Free · 5 min walk from Namba Station"] },
            { title: "Last Shopping at Shinsaibashi", description: "Pick up last-minute souvenirs — Japanese snacks, matcha KitKats, and ceramics.", details: [] }
          ],
          meals: [
            { type: "🍰 Breakfast", name: "Rikuro's Cheesecake (Namba)", description: "Watch the famous jiggly cheesecakes come out of the oven. They brand each one and the whole shop smells incredible. ¥965 for a whole cake.", meta: "📍 Namba · ¥965" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Dotonbori — One Last Time", description: "Take your final photo with the Glico Running Man sign. Get one last round of takoyaki. Say goodbye to Osaka.", details: [] }
          ],
          meals: [
            { type: "🐙 Lunch", name: "Final Takoyaki at Wanaka", description: "Perfectly crispy outside, molten inside. The ultimate Osaka farewell bite.", meta: "📍 Dotonbori · ¥600" }
          ],
          tips: [{ type: "tip", text: "Grab airport snacks at Don Quijote — tax-free shopping for tourists." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Nankai Rapi:t to Kansai Airport", description: "Take the retro-futuristic Rapi:t express from Namba to KIX (50 min, ¥1,290). Or take the JR Haruka (covered by JR Pass) from Tennoji.", details: ["💡 JR Haruka from Tennoji is covered by JR Pass if it's still active"] }
          ],
          meals: [
            { type: "✈️ Dinner", name: "Airport Ramen at KIX", description: "Kansai Airport has surprisingly great food. Hit up the ramen street on the 3rd floor for one final bowl.", meta: "📍 KIX Terminal 1 · ¥900-1,200" }
          ],
          tips: [{ type: "tip", text: "Sayonara, Japan! You've earned those 400,000 steps. Until next time. ✈️🇯🇵" }]
        }
      ]
    }
  ],
  budgetTable: [
    { category: "JR Rail Pass (21 days)", cost: "¥60,000 (~$400)", note: "Covers shinkansen, JR trains, some ferries" },
    { category: "Accommodation (19 nights)", cost: "¥300,000-500,000 (~$2,000-3,300)", note: "Mix of hotels, one ryokan night" },
    { category: "Food & Drink", cost: "¥200,000-300,000 (~$1,300-2,000)", note: "Mix of street food, casual, and splurge meals" },
    { category: "Activities & Entrance Fees", cost: "¥50,000-80,000 (~$330-530)", note: "Temples, museums, cooking class, teamLab" },
    { category: "Local Transport (non-JR)", cost: "¥30,000-50,000 (~$200-330)", note: "Subway, bus, Hakone Pass, Enoden" },
    { category: "Pocket WiFi / eSIM", cost: "¥5,000-8,000 (~$35-55)", note: "Essential for navigation and translation" },
    { category: "TOTAL (per person)", cost: "¥645,000-998,000", note: "~$4,300-6,650 USD" }
  ],
  practicalInfo: [
    { title: "🗓️ Best Time & Weather", items: ["May is perfect — warm (18-25°C), minimal rain before tsuyu (rainy season starts late June), and fewer tourists than cherry blossom season.", "The Grand Sumo Tournament (Natsu Basho) runs May 10-24 at Ryogoku Kokugikan in Tokyo. Try to attend!"] },
    { title: "🧳 Luggage & Transport Tips", items: ["Use Kuroneko Yamato (ta-Q-bin) to ship bags between cities. ¥2,000-3,000 per bag, next-day delivery. Hotels and convenience stores can help.", "JR Pass covers most intercity travel. Activate at the airport on Day 1.", "IC cards (Suica/Pasmo) work for subway, buses, and convenience store payments."] },
    { title: "🎌 Etiquette & Daily Life", items: ["Don't tip — it's considered rude.", "Don't eat while walking. Don't talk on phones in trains.", "Bow when greeting. Remove shoes when entering homes, temples, and ryokans.", "7-Eleven, Lawson, and FamilyMart are incredible — fresh onigiri, egg sandwiches, and decent sushi at 2am."] },
    { title: "🛍️ Shopping & Money", items: ["Cash is king — many restaurants are cash-only. 7-Eleven ATMs accept foreign cards.", "Spend ¥5,000+ at one store and show your passport for tax-free shopping (10% savings).", "Don Quijote, BIC Camera, and department stores all participate in tax-free."] }
  ]
};

// Add description to each day if missing
const dayDescs = [
  "Touch down in Tokyo and dive straight into the neon-lit energy of Shinjuku.",
  "Hit Tokyo's iconic trio: the bustling Tsukiji market, ancient Senso-ji, and the electric streets of Akihabara.",
  "From Meiji Shrine's forest calm to Harajuku's kawaii chaos to Roppongi's art scene.",
  "Tuna auctions at dawn, barefoot digital art at teamLab, and a splurge sushi dinner in Ginza.",
  "Explore old-school Tokyo in Yanaka, then catch the May Grand Sumo Tournament live!",
  "Escape to Kamakura's Great Buddha, coastal temples, and sunset on Enoshima Island.",
  "Hot springs, volcanic eggs, and Mt. Fuji views — Hakone is pure magic.",
  "Bullet train to Kanazawa — Japan's best-kept secret for sushi, gardens, and geisha culture.",
  "Samurai houses, gold leaf ice cream, and world-class contemporary art.",
  "Journey through the Japanese Alps to Takayama's perfectly preserved Edo streets.",
  "UNESCO village of Shirakawa-go, then an evening arrival in ancient Kyoto.",
  "Fushimi Inari's 10,000 gates at dawn, Kiyomizu-dera, and geisha-spotting in Gion.",
  "Bamboo groves, wild monkeys, and a hidden temple with 1,200 moss-covered statues.",
  "Golden Pavilion, zen rock gardens, and a hands-on Japanese cooking class.",
  "Day trip to Nara — friendly deer, the Great Buddha, and persimmon-leaf sushi.",
  "Tea ceremony, Philosopher's Path, and a farewell evening on the Kamo River.",
  "Welcome to Osaka — Japan's street food capital. Kushikatsu, takoyaki, and Dotonbori at night.",
  "Kuromon Market grazing, vintage shopping, and Osaka's legendary nightlife scene.",
  "A powerful day: Hiroshima's Peace Memorial and the floating torii gate of Miyajima Island.",
  "Final takoyaki, last-minute shopping, and sayonara Japan."
];
itineraryData.days.forEach((d, i) => { if (!d.description) d.description = dayDescs[i] || ''; });

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
