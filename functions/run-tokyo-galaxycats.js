const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1771940618085_iosbzg",
  email: "galaxycats510@gmail.com",
  destination: "Tokyo, Japan",
  start_date: "2026-03-14",
  end_date: "2026-03-19",
  group_size: "3-4",
  travel_style: "Adventure, Cultural, Relaxation",
  dining: "Casual throughout",
  budget: "Under $1,000",
  requests: "Father is vegetarian (can eat eggs). DisneySea is a must. Shopping, scenery, fun activities. Open to day trips near Tokyo.",
  timestamp: "2026-02-24T13:43:38.085Z",
  status: "pending"
};

const itineraryData = {
  destination: "Tokyo, Japan",
  countryEmoji: "🇯🇵",
  title: "Tokyo in 6 Days: Cherry Blossoms, DisneySea & Family Adventure",
  subtitle: "Shinjuku → DisneySea → Kamakura → Shibuya → Asakusa → Ginza",
  description: "A perfect Tokyo adventure for a group of 3–4, timed with the start of cherry blossom season. DisneySea is your anchor day, a day trip to Kamakura breaks up the city pace, and each Tokyo neighborhood delivers its own flavor — from neon-lit Shinjuku to serene temple gardens in Asakusa. Vegetarian-friendly throughout, with specific restaurants that are happy to accommodate dad.",
  duration: "6 days",
  dates: "Mar 14 – 19, 2026",
  budget: "Moderate (Under $1,000)",
  pace: "Active — full days with mix of adventure, culture, and shopping",
  bestFor: "Families, first-timers, cherry blossom season, theme park fans",
  highlights: [
    "Tokyo DisneySea — a full day at Japan's most immersive theme park",
    "Cherry blossom season begins — Ueno Park and Shinjuku Gyoen at their most magical",
    "Kamakura day trip — Great Buddha, coastal temples, and hillside hiking trails",
    "Shibuya Crossing — the world's busiest pedestrian scramble, live",
    "Senso-ji Temple at sunrise in Asakusa — Tokyo's most iconic shrine",
    "teamLab Planets — digital art you walk through barefoot",
    "Vegetarian ramen, curry, and temple food — dad eats like a king",
    "Shopping from Takeshita Street to Omotesando to Ginza",
    "Tokyo Skytree — 634m views over the city",
    "Tsukiji Outer Market breakfast — the freshest food in Tokyo"
  ],
  essentials: [
    {
      title: "🚇 Getting Around",
      text: "Get a Suica or Pasmo IC card at the airport — tap on/off trains, subways, and buses everywhere. For day 1, take the Narita Express (N'EX) or Limousine Bus from the airport. Day-trip to Kamakura: Shonan Shinjuku Line from Shinjuku (55 min, no transfer). DisneySea: JR Keiyō Line to Maihama Station, then Disney Resort Monorail (30–40 min from Tokyo Station). Taxis are expensive — stick to trains."
    },
    {
      title: "🌸 Cherry Blossom Alert",
      text: "Mid-March 2026 lands right at the start of cherry blossom season (sakura). Forecasts typically show Tokyo's first blooms around March 20–25, so you might catch early blossoms or full bloom depending on the year. Check the Japan Meteorological Corporation forecast closer to your trip. Ueno Park and Shinjuku Gyoen are the best spots."
    },
    {
      title: "🌿 Vegetarian Tips for Dad",
      text: "Tokyo is increasingly vegetarian-friendly. Look for 'shojin ryori' (Buddhist temple cuisine — always vegan) and restaurants marked 'yasai' (vegetable). The restaurants in this itinerary are specifically chosen for strong vegetarian menus. In a pinch, convenience stores (7-Eleven, Lawson) have egg sandwiches and onigiri. At regular restaurants, show the staff our vegetarian card: '私は菜食主義者です。卵は食べられます。肉、魚、鶏肉は食べられません。' (I am vegetarian. I can eat eggs. No meat, fish, or chicken.)"
    },
    {
      title: "🎢 DisneySea Advance Planning",
      text: "Book Tokyo DisneySea tickets at least 2–3 weeks in advance via the Tokyo Disney Resort app (disneytokyo.com). The app also lets you book Priority Passes for popular attractions. Must-dos: Journey to the Center of the Earth, Tower of Terror, Sindbad's Storybook Voyage, 20,000 Leagues Under the Sea, and the new Fantasy Springs area. Arrive at park open (usually 9am). For dad's meals: Zambini Brothers' Ristorante has a vegetarian pizza option, Plazma Ray's Diner has vegetable curry with egg, and Blue Bayou Restaurant has a vegetarian quiche set — this one requires a reservation on the app."
    },
    {
      title: "💴 Money & Budget",
      text: "Under $1,000 for 3–4 people is very doable in Tokyo. Biggest expenses: DisneySea tickets (~$80–95 per person), Tokyo Skytree (~$20–25 per person), teamLab Planets (~$30–35 per person). Meals at casual restaurants: $8–15 per person. Convenience store meals: $3–6. Tokyo is extremely cash-friendly — many smaller restaurants are cash only, so keep some yen on hand. 7-Eleven ATMs accept international cards."
    },
    {
      title: "📱 Essential Apps",
      text: "Google Maps (Japan transit is excellent), Tokyo Disney Resort (tickets + reservations), HappyCow (veg restaurants), Google Translate (camera mode for menus), Hyperdia (train schedules), Tabelog (restaurant reviews)."
    }
  ],
  days: [
    {
      num: 1,
      title: "Arrival, Shinjuku & First Night in Tokyo",
      neighborhoods: "Shinjuku · Kabukicho · Omoide Yokocho",
      date: "Mar 14",
      mapPins: [
        { lat: 35.6896, lng: 139.7006, label: "Shinjuku Station", num: 1, cat: "transport", desc: "Largest train station in the world — your Tokyo base" },
        { lat: 35.6851, lng: 139.7100, label: "Shinjuku Gyoen", num: 2, cat: "activity", desc: "National garden — best cherry blossom viewing spot in Shinjuku" },
        { lat: 35.6938, lng: 139.7034, label: "Omoide Yokocho (Memory Lane)", num: 3, cat: "food", desc: "Narrow alley of tiny yakitori stalls, thick with atmosphere" },
        { lat: 35.6880, lng: 139.6953, label: "Tokyo Metropolitan Government Building", num: 4, cat: "activity", desc: "Free observation deck — panoramic Tokyo skyline view" },
        { lat: 35.6956, lng: 139.6917, label: "Ain Soph Journey Shinjuku", num: 5, cat: "food", desc: "100% vegan restaurant — great for the vegetarian in your group" },
        { lat: 35.6989, lng: 139.7037, label: "Golden Gai", num: 6, cat: "nightlife", desc: "200+ tiny bars packed into a couple of narrow alleys" }
      ],
      timeBlocks: [
        {
          label: "Afternoon (Arrival)",
          activities: [
            {
              title: "Arrive & Check In",
              description: "Take the Narita Express (N'EX) directly to Shinjuku Station (~80 min, ¥3,070) or the Limousine Bus. Get Suica IC cards at the airport for seamless train travel throughout your stay. Check into your hotel and drop your bags.",
              details: [
                "💡 Suica cards loaded with ¥5,000–10,000 per person should last the whole trip for trains",
                "📍 Recommended base: Shinjuku or Shibuya — central, good transport links"
              ]
            },
            {
              title: "Shinjuku Gyoen National Garden",
              description: "Walk off the jet lag in this stunning 58-hectare national garden. In mid-March you may catch the very first cherry blossoms appearing on the early-blooming Kanzan trees. Even without full bloom, the garden is beautiful — manicured lawns, traditional Japanese and French garden sections.",
              details: [
                "🕐 Open Tue–Sun, 9am–4:30pm (last entry 4pm)",
                "💴 ¥500 per person · No alcohol allowed in the garden",
                "📍 5 min walk from Shinjuku-Gyoenmae Station"
              ]
            }
          ],
          meals: [
            {
              type: "☕ Arrival Coffee",
              name: "Starbucks Reserve Roastery Tokyo (Nakameguro) or any local café",
              description: "Grab a coffee and konbini snack to settle in. Japanese convenience stores (7-Eleven, Lawson, FamilyMart) are extraordinary — egg sandwiches, onigiri, fresh pastries. Dad can easily find egg salad sandwiches.",
              meta: "¥300–700 · Open 24 hours"
            }
          ],
          tips: [
            { type: "tip", text: "Don't fight the jet lag — stay active until 9pm local time and you'll reset faster. Tokyo's evening energy helps." }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Tokyo Metropolitan Government Building — Free Observation Deck",
              description: "Take the free elevator to the 45th floor (202m) for sweeping views over Tokyo, including Mount Fuji on clear days. North and South towers both have decks open in the evening. One of the best free views in the city.",
              details: [
                "🕐 North Observatory: Tue–Sun 9am–10:30pm. South: Tue–Sun 9am–5:30pm",
                "💴 FREE · No reservation needed",
                "📍 5 min walk from Shinjuku Station West Exit"
              ]
            },
            {
              title: "Omoide Yokocho (Memory Lane)",
              description: "Wander the famous narrow alley packed with tiny yakitori stalls, their smoke billowing into the night. Even if you're not eating here (limited veggie options), the atmosphere is pure Tokyo magic — tiny stools, grilling skewers, locals and travelers shoulder-to-shoulder.",
              details: [
                "📍 Right outside Shinjuku Station East Exit",
                "💡 Great for photos and atmosphere. Grab a Sapporo beer and soak it in."
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Dinner",
              name: "Ain Soph Journey (Shinjuku)",
              description: "Tokyo's most beloved vegan restaurant chain. The Shinjuku location serves creative plant-based Japanese-Western fusion — their fluffy pancakes (at brunch) are legendary, and their dinner set menus are excellent. Dad will eat extremely well here, with plenty of egg-based options. Non-vegetarians are always happy too.",
              meta: "¥1,500–2,500pp · 3F, 2-6-10 Shinjuku · Reservations recommended"
            }
          ],
          tips: [
            { type: "reddit", text: "Ain Soph Journey is genuinely great food, not 'health food.' The mushroom steak and the pancakes are unreal. Non-vegans love it too.", cite: "r/JapanTravel" }
          ]
        },
        {
          label: "Late Night",
          activities: [
            {
              title: "Golden Gai — Tokyo's Most Unique Bar Scene",
              description: "Explore this UNESCO-listed cluster of ~200 tiny bars, each holding 5–10 people. Every bar has its own theme — music bars, movie bars, anime bars, sake bars. Most welcome tourists. Just push open a door that looks interesting. This is Tokyo unlike anywhere else on Earth.",
              details: [
                "💡 Budget ¥1,000–2,000 per bar (cover charge + one drink)",
                "📍 Kabukicho area, very close to Shinjuku Station"
              ]
            }
          ],
          meals: [],
          tips: [{ type: "tip", text: "Golden Gai bars often have a small cover charge (¥500–1,000) — totally worth it. If the door looks interesting, go in. That's the game." }]
        }
      ]
    },
    {
      num: 2,
      title: "TOKYO DISNEYSEA — Full Day",
      neighborhoods: "Urayasu · DisneySea · Maihama",
      date: "Mar 15",
      mapPins: [
        { lat: 35.6267, lng: 139.8853, label: "Tokyo DisneySea", num: 1, cat: "activity", desc: "The world's most beautifully themed theme park" },
        { lat: 35.6350, lng: 139.8804, label: "Maihama Station", num: 2, cat: "transport", desc: "JR station — gateway to Disney Resort" },
        { lat: 35.6303, lng: 139.8822, label: "Mediterranean Harbor", num: 3, cat: "activity", desc: "DisneySea's stunning entrance port — photo-worthy" },
        { lat: 35.6255, lng: 139.8880, label: "Mount Prometheus", num: 4, cat: "activity", desc: "Journey to the Center of the Earth + Tower of Terror area" },
        { lat: 35.6281, lng: 139.8832, label: "Zambini Brothers' Ristorante", num: 5, cat: "food", desc: "Best vegetarian option at DisneySea — vegetarian long pizza" },
        { lat: 35.6249, lng: 139.8899, label: "Fantasy Springs (new 2024)", num: 6, cat: "activity", desc: "Frozen, Tangled & Peter Pan themed new area" }
      ],
      timeBlocks: [
        {
          label: "Getting There (Early!)",
          activities: [
            {
              title: "Early Start to DisneySea",
              description: "Take the JR Keiyō Line from Tokyo Station to Maihama Station (15 min, ¥240). Then ride the Disney Resort Line monorail to DisneySea (10 min). Aim to arrive 30 minutes before park open (usually 9am) to get a great position at the gates.",
              details: [
                "🚉 Tokyo Station → Maihama Station: JR Keiyō Line, ~15 min",
                "🚝 Maihama → DisneySea: Disney Resort Line monorail, ~10 min",
                "🎟️ Pre-book tickets on Tokyo Disney Resort app! Same-day tickets often sell out"
              ]
            }
          ],
          meals: [
            {
              type: "☕ Breakfast",
              name: "Grab breakfast before the park or at the hotel",
              description: "Eat at your hotel or grab a 7-Eleven breakfast — food lines inside DisneySea get long early. You'll want to hit rides first.",
              meta: "¥400–800 at convenience store"
            }
          ],
          tips: [{ type: "tip", text: "The most strategic move: rush straight to Journey to the Center of the Earth or Fantasy Springs at park open — these have the longest waits (60–120 min by 10am)." }]
        },
        {
          label: "Morning — Rides First",
          activities: [
            {
              title: "Journey to the Center of the Earth",
              description: "DisneySea's most iconic ride. A volcanic rock drill vehicle plunges through glowing crystals and prehistoric creatures before bursting into the lava zone — the final drop is incredible. Inside Mount Prometheus, the park's centerpiece volcano.",
              details: ["⚡ Priority Pass recommended — grab it on the app ASAP at park open", "📏 No height restriction"]
            },
            {
              title: "Tower of Terror",
              description: "The DisneySea version is uniquely themed around a cursed 13th floor of the Hotel Hightower — completely different story from the US parks and widely considered more atmospheric. The drop is terrifying in the best way.",
              details: ["⚡ Grab a Priority Pass for this one too", "📏 No height minimum (based on sensation, not height)"]
            },
            {
              title: "20,000 Leagues Under the Sea",
              description: "A slow, atmospheric submarine journey through an underwater world — beautiful for all ages. No scares, great theming, often has shorter waits than other headliners.",
              details: []
            }
          ],
          meals: [],
          tips: [{ type: "reddit", text: "The key to DisneySea is being strategic with Priority Passes. Get them immediately at park open for Journey to the Center of the Earth — waits hit 90 min by 10:30am. Everything else can be done standby after lunch.", cite: "r/TokyoDisneySea" }]
        },
        {
          label: "Afternoon — Shows, Food & More Rides",
          activities: [
            {
              title: "Sindbad's Storybook Voyage",
              description: "A classic slow boat ride through vibrant storybook worlds — surprisingly charming and relaxing after the thrill rides. The Compass of Your Heart song will be stuck in your head for days.",
              details: []
            },
            {
              title: "Fantasy Springs (New 2024 Area)",
              description: "DisneySea's brand new themed area featuring Frozen, Rapunzel/Tangled, and Peter Pan. Stunning theming and three new rides (Frozen Ever After, Rapunzel's Lantern Festival, Peter Pan's Never Land Adventure). A separate ticket area — book ahead.",
              details: [
                "💡 Fantasy Springs requires an add-on ticket booked in advance",
                "⚡ Buy Fantasy Springs tickets on the app before your trip"
              ]
            },
            {
              title: "Indiana Jones Adventure",
              description: "A jeep adventure through an ancient temple in the Mysterious Island area — great physical ride with fun story. Usually has manageable waits mid-afternoon.",
              details: []
            }
          ],
          meals: [
            {
              type: "🍕 Lunch",
              name: "Zambini Brothers' Ristorante",
              description: "Counter-service Italian in the Mediterranean Harbor area — and the best vegetarian option at DisneySea. Their 'Vegetarian Long Pizza' is actually a calzone stuffed with cheese, tomatoes, and pesto. Delicious and filling. The rest of the group can get pasta and grilled meats.",
              meta: "¥1,200–1,800 · Mediterranean Harbor area · Counter service"
            }
          ],
          tips: [
            {
              type: "tip",
              text: "For additional veggie options: Plazma Ray's Diner has a vegetable curry rice bowl with egg (¥780). Blue Bayou Restaurant inside the Pirates ride has a vegetarian quiche set — requires reservation on the app but worth it for the atmosphere."
            }
          ]
        },
        {
          label: "Evening — Shows & Goodbye",
          activities: [
            {
              title: "Fantasmic! Evening Show",
              description: "DisneySea's nighttime water spectacular — a water screen light show in the Mediterranean Harbor that uses projection mapping, water jets, and live performers. Absolutely stunning. Check the park schedule and get a spot 30 min early.",
              details: ["📅 Usually runs at 8pm — check the Tokyo Disney Resort app for showtimes on your day"]
            }
          ],
          meals: [
            {
              type: "🍦 Park Snacks",
              name: "DisneySea Churros & Specialty Snacks",
              description: "DisneySea has amazing seasonal snacks — look for themed popcorn buckets, churros with unique flavors, and limited-edition treats. A DisneySea snack haul is a tradition.",
              meta: "¥500–1,000 per snack item"
            }
          ],
          tips: [{ type: "reddit", text: "DisneySea is genuinely on another level compared to other Disney parks — the theming, the food quality, the shows. It's not a kids theme park, it's a world-class experience. The Fantasmic show is worth staying late for.", cite: "r/travel" }]
        }
      ]
    },
    {
      num: 3,
      title: "Day Trip to Kamakura — Temples, the Great Buddha & the Coast",
      neighborhoods: "Kamakura · Hase · Enoshima (optional)",
      date: "Mar 16",
      mapPins: [
        { lat: 35.3167, lng: 139.5353, label: "Kotoku-in (Great Buddha)", num: 1, cat: "activity", desc: "The iconic 13.4m bronze Great Buddha — outdoor and serene" },
        { lat: 35.3167, lng: 139.5305, label: "Hase-dera Temple", num: 2, cat: "activity", desc: "Beautiful hillside temple with coastal views and a thousand-year-old Kannon statue" },
        { lat: 35.3119, lng: 139.5517, label: "Komachi-dori Street", num: 3, cat: "activity", desc: "Kamakura's main shopping street — street food, souvenirs, cafés" },
        { lat: 35.3227, lng: 139.5466, label: "Tsurugaoka Hachimangu Shrine", num: 4, cat: "activity", desc: "Kamakura's most famous shrine — grand and historic" },
        { lat: 35.2998, lng: 139.4843, label: "Enoshima Island", num: 5, cat: "activity", desc: "Optional extension — sea caves, shrine, ocean views" },
        { lat: 35.3197, lng: 139.5485, label: "Komaki Shokudo Kamakura", num: 6, cat: "food", desc: "Vegan Japanese lunch sets in a traditional building near the station" }
      ],
      timeBlocks: [
        {
          label: "Morning — Train to Kamakura",
          activities: [
            {
              title: "Take the Shonan Shinjuku Line to Kamakura",
              description: "Board the Shonan Shinjuku Line from Shinjuku Station directly to Kamakura (~55 minutes, ¥940 each way). No transfers needed. Sit on the right side of the train for ocean glimpses near the coast. Aim to leave Shinjuku by 8:30–9am.",
              details: [
                "🚉 Shinjuku → Kamakura: Shonan Shinjuku Line, ~55 min direct",
                "💴 ¥940 per person each way — use your Suica card"
              ]
            },
            {
              title: "Tsurugaoka Hachimangu Shrine",
              description: "Start at Kamakura's most celebrated shrine at the end of the grand Wakamiya-oji boulevard. The approach with its stone torii gates, ponds, and lotus flowers is stunning — especially if early cherry blossoms are starting. Climb the central staircase for views over the shrine grounds.",
              details: [
                "📍 10 min walk from Kamakura Station",
                "💴 Free admission to main grounds"
              ]
            }
          ],
          meals: [],
          tips: [{ type: "tip", text: "The walk from Kamakura Station to the Great Buddha via Hase is scenic — consider renting bikes (¥300/hr at the station) to cover more ground and enjoy the coastal paths." }]
        },
        {
          label: "Midday — Temples & the Great Buddha",
          activities: [
            {
              title: "Hase-dera Temple",
              description: "One of the most beautiful temples in the Kanto region — perched on a hillside with sweeping views of the Kamakura coastline and, on clear days, the Pacific Ocean. Inside: a massive 9.18m wooden Kannon statue carved from a single camphor tree over 1,200 years ago. The garden and koi pond are stunning.",
              details: [
                "💴 ¥400 per person",
                "🕐 Open 8am–5pm (last entry 4:30pm)",
                "💡 The hydrangea garden here is famous — mid-March you'll see early blooms"
              ]
            },
            {
              title: "Kotoku-in — The Great Buddha (Daibutsu)",
              description: "The 13.4m bronze Great Buddha is one of Japan's most iconic images — serene, enormous, and 700+ years old. You can pay extra to go inside (yes, inside the statue). The surrounding grounds are peaceful and beautiful. The statue sits outside in the open air — its indoor home was destroyed by a tsunami in the 1300s.",
              details: [
                "💴 ¥300 per person (¥50 extra to enter the statue)",
                "🕐 Open 8am–5:30pm",
                "📍 5 min walk from Hase-dera"
              ]
            }
          ],
          meals: [
            {
              type: "🍱 Lunch",
              name: "Komaki Shokudo Kamakura",
              description: "A beloved fully plant-based Japanese restaurant near Kamakura Station — set menus with seasonal vegetable dishes, miso soup, rice, and pickles. Deeply traditional Japanese flavors in a beautiful old wooden building. One of the best vegetarian lunches in all of Japan. The rest of the group will love it too.",
              meta: "¥1,200–1,800 set lunch · Near Kamakura Station · Reservations recommended"
            }
          ],
          tips: [{ type: "reddit", text: "Komaki Shokudo is a gem — real shojin-inspired cooking, not sad health food. The seasonal set changes daily and everything is impeccably made. Show up hungry.", cite: "r/JapanTravel" }]
        },
        {
          label: "Afternoon — Komachi Street & Optional Enoshima",
          activities: [
            {
              title: "Komachi-dori Shopping Street",
              description: "The pedestrian street leading from Kamakura Station to the shrine is lined with cafés, craft shops, street food stalls, and souvenir shops. Great for matcha ice cream (¥350), handmade accessories, and picking up Japanese ceramics or bamboo crafts.",
              details: [
                "💡 Try the fresh-made senbei (rice crackers) from the shops — they grill them in front of you"
              ]
            },
            {
              title: "Enoshima Island (Optional Extension)",
              description: "If energy allows, hop on the Enoden tram from Kamakura Station to Enoshima (20 min, ¥260) for sea caves, a hilltop shrine with ocean panoramas, and some of the best views of Mount Fuji on clear days. The island's narrow shopping street has excellent seafood and snacks.",
              details: [
                "⏱️ Add 2 hours for Enoshima",
                "💡 The Enoden tram ride itself is scenic — it runs through narrow Kamakura streets close to houses"
              ]
            }
          ],
          meals: [
            {
              type: "🍵 Afternoon Tea",
              name: "Café on Komachi Street",
              description: "Stop for matcha soft cream (soft serve) or a warabi mochi (bracken starch mochi) at one of the street stalls. Kamakura has great matcha everything — sweets, lattes, ice cream.",
              meta: "¥300–600"
            }
          ],
          tips: []
        },
        {
          label: "Evening — Return to Tokyo",
          activities: [
            {
              title: "Scenic Train Ride Back",
              description: "Head back to Tokyo in time for dinner. The Shonan Shinjuku Line gets you back to Shinjuku by 6–7pm if you leave Kamakura around 5pm. The sunset over the ocean near Zushi is beautiful from the train.",
              details: []
            }
          ],
          meals: [
            {
              type: "🍜 Dinner",
              name: "T's TanTan (Tokyo Station / Ueno Station)",
              description: "Tokyo's most famous vegan ramen shop, located inside Tokyo Station (in the JR gate area). 100% plant-based ramen — the sesame dan dan noodles and the spicy sesame ramen are incredible. Perfect post-Kamakura dinner before heading back to Shinjuku.",
              meta: "¥900–1,200 · Tokyo Station, JR Keiyo Street area · No reservation needed"
            }
          ],
          tips: [{ type: "reddit", text: "T's TanTan is my secret weapon when traveling with vegetarians in Japan. The dan dan noodles are genuinely one of the best ramens I've had. Non-vegans have no idea it's vegan until you tell them.", cite: "r/Tokyo" }]
        }
      ]
    },
    {
      num: 4,
      title: "Harajuku, Shibuya & Shopping Day",
      neighborhoods: "Harajuku · Omotesando · Shibuya · Daikanyama",
      date: "Mar 17",
      mapPins: [
        { lat: 35.6764, lng: 139.6993, label: "Meiji Shrine", num: 1, cat: "activity", desc: "Serene forest shrine dedicated to Emperor Meiji — a peaceful start to the day" },
        { lat: 35.6703, lng: 139.7027, label: "Takeshita Street (Harajuku)", num: 2, cat: "activity", desc: "Quirky, colorful youth fashion street — Japanese pop culture at its wildest" },
        { lat: 35.6625, lng: 139.7143, label: "Omotesando Hills", num: 3, cat: "activity", desc: "Architecturally stunning upscale mall — Tadao Ando designed" },
        { lat: 35.6592, lng: 139.7006, label: "Shibuya Crossing", num: 4, cat: "activity", desc: "The world's busiest pedestrian crossing — cross it and watch it from above" },
        { lat: 35.6581, lng: 139.7016, label: "Shibuya Sky (Scramble Square)", num: 5, cat: "activity", desc: "Open-air rooftop observation deck — stunning 360° views from 229m" },
        { lat: 35.6655, lng: 139.6993, label: "Muse (Shibuya Vegan)", num: 6, cat: "food", desc: "Excellent plant-based Japanese restaurant in Shibuya" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Meiji Shrine — Peaceful Forest Start",
              description: "Step into the forested grounds surrounding Tokyo's most famous Shinto shrine, dedicated to Emperor and Empress Meiji. The 70-hectare forest in the middle of the city is stunning — 120,000 trees from across Japan, donated at the shrine's founding. Write a wish on an ema (wooden board) and hang it with thousands of others.",
              details: [
                "💴 Free admission",
                "🕐 Open sunrise to sunset",
                "📍 Harajuku Station, 1 min walk"
              ]
            },
            {
              title: "Takeshita Street — Harajuku Pop Culture",
              description: "Walk through this 350m pedestrian street that's ground zero for Japanese youth fashion, kawaii culture, and creative street food. Crepes with enormous fillings, rainbow cotton candy, gothic lolita shops, anime goods — it's wonderfully chaotic and unlike anywhere else. Great for photos.",
              details: [
                "💡 Busiest on weekends (Saturday = chaos). Go early morning for less crowds",
                "🥞 Must try: a Harajuku crepe (¥600–900) — these are different from French crepes, they're wrapped in a cone"
              ]
            }
          ],
          meals: [
            {
              type: "☕ Breakfast",
              name: "Little Nap Coffee Stand (Yoyogi) or any Harajuku café",
              description: "Tokyo's café scene is world-class. Look for any of the independent coffee shops along Omotesando or in the Harajuku back streets. Japan takes coffee very seriously.",
              meta: "¥500–800"
            }
          ],
          tips: [{ type: "tip", text: "The Harajuku back streets (Ura-Harajuku) between Takeshita Street and Omotesando are where the real treasure is — independent fashion boutiques, vintage shops, tiny cafés. Get lost in there." }]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Omotesando — Tokyo's Most Beautiful Shopping Boulevard",
              description: "A tree-lined avenue with zelkova trees (beautiful in any season), housing both luxury brands (Louis Vuitton, Prada, Dior with stunning architecture) and great mid-range shops. Omotesando Hills mall — designed by Tadao Ando — has a spiraling interior atrium that's worth seeing even if you don't buy anything.",
              details: [
                "💡 The side streets off Omotesando (Cat Street) have more accessible, local shops",
                "🏬 Omotesando Hills has good food options for the group"
              ]
            },
            {
              title: "Shibuya Crossing — Live the Moment",
              description: "At street level, you'll join hundreds of people crossing from all directions simultaneously — electric, exhilarating, and uniquely Tokyo. Then go up to Starbucks or Mag's Park above the crossing to watch the spectacle from above. Peak rush hour (5–6pm) is when it's most dramatic.",
              details: ["📍 Shibuya Station Hachiko Exit — Hachiko statue is right at the exit (the famous loyal dog)"]
            },
            {
              title: "Shibuya Sky — Open-Air Rooftop",
              description: "Tokyo's most thrilling observation deck on top of Scramble Square — a large open-air rooftop at 229m with no glass barriers (there's netting), 360° views including DisneySea on the horizon and Mount Fuji on clear days. Way more exciting than a closed observation deck.",
              details: [
                "💴 ¥2,000 per person (¥1,600 if pre-booked online)",
                "🕐 Open daily 10am–10:30pm (last entry 9:30pm)",
                "💡 Pre-book timed entry tickets online — they sell out on busy days"
              ]
            }
          ],
          meals: [
            {
              type: "🍱 Lunch",
              name: "Brown Rice by Neal's Yard (Omotesando)",
              description: "A long-established vegetarian and vegan café on a quiet back street off Omotesando. Organic Japanese and international dishes — brown rice bowls, miso soups, seasonal vegetable sets. The group can eat outside in the small courtyard when weather allows. A great vegetarian-friendly lunch in a prime location.",
              meta: "¥1,200–1,800pp · 5-1-8 Minami-Aoyama · Closed Mondays"
            }
          ],
          tips: [{ type: "reddit", text: "Shibuya Sky beats Skytree for pure excitement — the open-air aspect and the night views of Shibuya below you are incredible. Do it at sunset if possible.", cite: "r/JapanTravel" }]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Daikanyama & Nakameguro Evening Stroll",
              description: "A 10-minute walk from Shibuya leads to Daikanyama — Tokyo's most stylish neighborhood, full of boutiques, concept stores, and cafés. Then follow the Meguro River to Nakameguro — the canal banks are lined with cherry trees, and in mid-March you might catch early blossoms lit up in the evening. Magical if the timing works.",
              details: ["🌸 The Nakameguro cherry blossom canal walk is one of Tokyo's most beautiful scenes — worth checking even if just early buds"]
            }
          ],
          meals: [
            {
              type: "🍽️ Dinner",
              name: "Muse (Daikanyama/Nakameguro area)",
              description: "A cozy, relaxed plant-based Japanese restaurant. Seasonal vegetable dishes, tofu-based proteins, and beautiful presentation. Dad will love the variety — non-vegetarians are equally satisfied. Casual, great value, and thoroughly Japanese in flavor.",
              meta: "¥1,500–2,500pp · Daikanyama area"
            }
          ],
          tips: []
        }
      ]
    },
    {
      num: 5,
      title: "Asakusa, Ueno Cherry Blossoms & teamLab Planets",
      neighborhoods: "Asakusa · Ueno · Akihabara · Toyosu",
      date: "Mar 18",
      mapPins: [
        { lat: 35.7147, lng: 139.7967, label: "Senso-ji Temple (Asakusa)", num: 1, cat: "activity", desc: "Tokyo's oldest and most visited temple — stunning Thunder Gate" },
        { lat: 35.7163, lng: 139.7711, label: "Ueno Park", num: 2, cat: "activity", desc: "Japan's most famous cherry blossom park — possibly blooming!" },
        { lat: 35.7178, lng: 139.7745, label: "Tokyo National Museum (Ueno)", num: 3, cat: "activity", desc: "Japan's largest and most important art museum" },
        { lat: 35.6984, lng: 139.7731, label: "Akihabara Electric Town", num: 4, cat: "activity", desc: "Anime, electronics, gaming, and all things otaku culture" },
        { lat: 35.6478, lng: 139.7894, label: "teamLab Planets (Toyosu)", num: 5, cat: "activity", desc: "Immersive digital art experience — walk through living artworks barefoot" },
        { lat: 35.7100, lng: 139.7993, label: "Tokyo Skytree", num: 6, cat: "activity", desc: "634m tall — Japan's tallest structure with observation decks" }
      ],
      timeBlocks: [
        {
          label: "Early Morning",
          activities: [
            {
              title: "Senso-ji Temple at Dawn — Beat the Crowds",
              description: "Tokyo's oldest Buddhist temple (645 AD) is best experienced early morning — the fog, the incense smoke, and the silence are magical before tour groups arrive. Walk through the massive Kaminarimon (Thunder Gate) with its iconic red lantern, through Nakamise shopping arcade, into the main temple hall. Toss a coin, bow twice, clap twice, bow once — join the ritual.",
              details: [
                "🕐 Grounds open 24/7 · Temple hall opens 6am",
                "💴 Free admission",
                "📍 Asakusa Station (Ginza Line or Asakusa Line)",
                "💡 Go before 8am for best atmosphere. After 10am it's completely packed."
              ]
            },
            {
              title: "Nakamise Dori — Traditional Souvenir Shopping",
              description: "The 250m approach to Senso-ji is lined with 90 traditional stalls selling senbei (rice crackers), ningyo-yaki (sweet cakes), fans, tenugui (hand towels), and every Japanese souvenir imaginable. The shops open around 9–10am — great for picking up gifts.",
              details: []
            }
          ],
          meals: [
            {
              type: "☕ Breakfast",
              name: "Hatsuogawa Asakusa or any Asakusa café",
              description: "Grab a coffee and fresh ningyo-yaki (sweet bean paste cakes, traditionally shaped, always egg-based — great for dad) from the stalls as they open. Or find a quiet kissaten (traditional Japanese coffee shop) for a morning set.",
              meta: "¥300–700"
            }
          ],
          tips: [{ type: "reddit", text: "Going to Senso-ji at 6am is one of the best Tokyo experiences — incense burning, monks walking through, almost no tourists. By 9am it's chaos. The early morning is worth the effort.", cite: "r/JapanTravel" }]
        },
        {
          label: "Morning",
          activities: [
            {
              title: "Tokyo Skytree — Tallest Tower in Japan",
              description: "Visible from Asakusa (just walk toward it — it's massive), the Skytree offers two observation decks at 350m and 450m. On a clear day you can see all the way to Mount Fuji. The glass floor section at 450m (Tembo Galleria) is thrilling. The base has a huge shopping mall (Solamachi) with great food.",
              details: [
                "💴 ¥2,100 to Tembo Deck (350m) + ¥1,000 to Tembo Galleria (450m)",
                "🕐 Open daily 10am–9pm (last entry 8pm)",
                "💡 Pre-book to avoid queues, especially on weekends"
              ]
            }
          ],
          meals: [],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Ueno Park & Museums",
              description: "Walk or train to Ueno Park — one of Japan's most famous hanami (flower viewing) sites. In mid-March you may see the very first cherry blossoms opening on the 1,200 trees here. Stroll the main avenue and pond area, and visit the National Museum of Nature and Science (excellent English signage, very hands-on). The Tokyo National Museum has Japan's largest collection of Japanese art and artifacts.",
              details: [
                "🌸 Ueno has ~1,200 sakura trees — check forecasts for bloom status",
                "💴 Park is free · National Museum ¥1,000 · Science Museum ¥630",
                "📍 Ueno Station (Yamanote Line)"
              ]
            },
            {
              title: "Akihabara — Electric Town (Optional)",
              description: "If anyone in the group is into anime, gaming, or electronics (or even if they're not), Akihabara is a uniquely Tokyo experience. Multi-story arcades (Round One), retro game shops, anime merchandise floors, maid cafés, and electronics at Japan prices. Great fun for 90 minutes.",
              details: ["📍 Akihabara Station (JR Yamanote or Chūō-Sōbu Line)"]
            }
          ],
          meals: [
            {
              type: "🍱 Lunch",
              name: "Ueno Seiyoken (inside Ueno Park)",
              description: "A historic Western-style restaurant inside Ueno Park, serving since 1876. Classic Japanese-Western cuisine (yoshoku) — great for the group with diverse tastes. Vegetarian options available. Beautiful old-school atmosphere.",
              meta: "¥1,500–2,500pp · Ueno Park (inside Shinobazu Pond entrance)"
            }
          ],
          tips: []
        },
        {
          label: "Evening — teamLab Planets",
          activities: [
            {
              title: "teamLab Planets — Immersive Digital Art",
              description: "One of Tokyo's unmissable experiences. You walk barefoot through rooms that become living artworks — wade through knee-deep water surrounded by holographic koi fish, step into infinite flower installations, lie under pulsing digital universes. It's breathtaking, otherworldly, and works for all ages. Allow 90 minutes.",
              details: [
                "💴 ¥3,200 per person (adults) · ¥1,000 (children 4–12)",
                "🕐 Open daily 9am–10pm · Pre-book timed entry tickets online (sells out!)",
                "📍 Toyosu Station (Yurikamome Line) — 20 min from Akihabara",
                "⚠️ Book well in advance at teamlab.art — this sells out weeks ahead"
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Dinner",
              name: "Toyosu or Odaiba waterfront restaurants",
              description: "After teamLab, head to the Toyosu or Odaiba waterfront for dinner with Rainbow Bridge views. Many shopping malls here (Aqua City, DiverCity) have good food courts with varied Japanese options for the whole group.",
              meta: "¥1,200–2,000pp"
            }
          ],
          tips: [{ type: "reddit", text: "teamLab Planets is genuinely one of the most extraordinary things I've done in any city. The koi fish room alone is worth it. It's not just an 'Instagram thing' — it's actually mind-blowing.", cite: "r/JapanTravel" }]
        }
      ]
    },
    {
      num: 6,
      title: "Ginza, Tsukiji & Tokyo Farewell",
      neighborhoods: "Tsukiji · Ginza · Tokyo Station · Departure",
      date: "Mar 19",
      mapPins: [
        { lat: 35.6654, lng: 139.7707, label: "Tsukiji Outer Market", num: 1, cat: "food", desc: "Famous food market for breakfast — tamagoyaki, fresh produce, street food" },
        { lat: 35.6721, lng: 139.7652, label: "Ginza", num: 2, cat: "activity", desc: "Tokyo's most upscale shopping district — world-class stores and architecture" },
        { lat: 35.6812, lng: 139.7671, label: "Tokyo Station", num: 3, cat: "transport", desc: "Iconic 1914 red-brick station — also a world-class food destination (Gransta mall)" },
        { lat: 35.6628, lng: 139.7650, label: "Itoya Ginza (stationery)", num: 4, cat: "activity", desc: "12-floor stationery store — uniquely Japanese gift shopping" },
        { lat: 35.6679, lng: 139.7616, label: "Kabuki-za Theatre", num: 5, cat: "activity", desc: "Grand traditional kabuki theatre — stunning architecture even from outside" },
        { lat: 35.6734, lng: 139.7599, label: "Nihonbashi", num: 6, cat: "activity", desc: "Historic bridge and district — Japan's 'kilometer zero'" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Tsukiji Outer Market — Final Tokyo Breakfast",
              description: "The outer market (free, public) is still one of the greatest food markets in the world despite the inner wholesale market moving to Toyosu. Arrive by 8am for the best stalls. Dad can enjoy fresh tamagoyaki (egg omelette cooked in sweet layers — vegetarian and perfect), dashimaki tamago, fresh produce, and Japanese sweets. Others can try tuna, oysters, or sashimi.",
              details: [
                "🕐 Best 7am–11am · Most stalls close early afternoon",
                "💴 Free entry — pay per item",
                "💡 Tamagoyaki vendors let you taste for free — must eat the warm one fresh"
              ]
            }
          ],
          meals: [
            {
              type: "🍳 Breakfast",
              name: "Tsukiji Outer Market Stalls",
              description: "Graze through the stalls — tamagoyaki for dad (egg omelette on a stick, perfectly seasoned, ¥300–400), fresh-cut fruit, tamago sando (egg sandwich) from the little shops, matcha-anything. The market is an experience, not just a meal.",
              meta: "¥500–1,500 total · 4-16-2 Tsukiji"
            }
          ],
          tips: [{ type: "tip", text: "The tamagoyaki at Tsukiji is one of Tokyo's great eating experiences — perfectly sweet, custardy layers on a stick. Dad will love it and it's 100% vegetarian." }]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "Ginza — Last Shopping & Strolling",
              description: "Walk through Ginza — Tokyo's equivalent of 5th Avenue. On weekends the main boulevard (Chuo-dori) becomes a pedestrian street (10am–6pm in spring) — people stroll, street performers appear, and the atmosphere is festive. Window shop at flagship stores: Uniqlo's global flagship (8 floors), Muji flagship, Dover Street Market.",
              details: [
                "🏬 Itoya — 12-floor stationery store is a Tokyo institution. Incredible for unique Japanese gifts — washi tape, writing tools, notebooks",
                "🏛️ Kabuki-za Theatre exterior is worth a photo — grand, traditional architecture in the middle of Ginza"
              ]
            },
            {
              title: "Tokyo Station Gransta Mall — Last Shopping",
              description: "Tokyo Station itself is a destination — the beautiful 1914 red-brick building (restored after earthquake damage) houses an underground mall (Gransta) with the best ekiben (train station bento) selection in Japan, dozens of regional food stalls, and the world's best department store food basement. Perfect for buying gifts, snacks, and pickups before departure.",
              details: [
                "🎁 Best for last-minute gifts: Japanese sweets, regional snacks, wagashi, sake/whisky",
                "💡 The Character Street in Tokyo Station has every Nintendo, Pokémon, and Ghibli item imaginable"
              ]
            }
          ],
          meals: [
            {
              type: "🍱 Farewell Lunch",
              name: "Saido (Ginza/Tsukiji area) — Vegan Japanese",
              description: "A dedicated vegetarian Japanese restaurant near Tsukiji with beautiful lunch sets — the Japanese vegetarian multi-course lunch (shojin-inspired) is an elegant finale. Traditional lacquerware presentation, seasonal vegetables, tofu, and rice. A dignified farewell for dad's final Tokyo meal.",
              meta: "¥1,500–2,500 · Tsukiji area · Book ahead"
            }
          ],
          tips: [{ type: "reddit", text: "The Gransta underground mall in Tokyo Station is the best place in Japan to buy gifts — you can find every famous regional food item from across Japan in one place, perfectly packaged. Budget 30 minutes minimum.", cite: "r/JapanTravelTips" }]
        },
        {
          label: "Departure",
          activities: [
            {
              title: "Head to the Airport",
              description: "From Tokyo Station, the Narita Express (N'EX) takes you directly to Narita Airport (~50 min, ¥3,070). Or take the Limousine Bus from major hotels and Shinjuku. Allow at least 3 hours before your flight for international departures.",
              details: [
                "🚉 Tokyo Station → Narita Airport: N'EX, ~50 min",
                "🚌 Limousine Bus from Tokyo City Air Terminal (TCAT): ~60–90 min depending on traffic",
                "✈️ Tip: Check in any luggage the night before (airport check-in counters) to travel light on your last morning"
              ]
            }
          ],
          meals: [
            {
              type: "✈️ Airport Food",
              name: "Narita Airport Terminal Restaurants",
              description: "Narita has excellent restaurants — grab ramen at Fuunji or a soba set at one of the airport soba shops for your last taste of Japan before departure.",
              meta: "¥1,000–1,800"
            }
          ],
          tips: [{ type: "tip", text: "Japan airports are relaxed and efficient — international security and immigration is faster than most airports. 2.5 hours before flight is comfortable; 2 hours is fine if you're not checking bags." }]
        }
      ]
    }
  ],
  budgetTable: [
    { category: "🎢 DisneySea Tickets (×4)", estimated: "$320–380", notes: "~¥7,500–9,000 per person. Book on app." },
    { category: "🔭 Skytree Tembo Deck (×4)", estimated: "$55–65", notes: "¥2,100 per person + ¥1,000 upper deck" },
    { category: "🎨 teamLab Planets (×4)", estimated: "$100–110", notes: "¥3,200 per adult, pre-book online" },
    { category: "🌅 Shibuya Sky (×4)", estimated: "$45–55", notes: "¥1,600 pre-booked or ¥2,000 walk-up" },
    { category: "🚉 Transit (×4 for 6 days)", estimated: "$80–100", notes: "~¥2,500 per person total on Suica" },
    { category: "🍱 Meals (casual, 3 per day)", estimated: "$300–400", notes: "~¥800–1,500 per person per meal" },
    { category: "🎋 Kamakura Day Trip (×4)", estimated: "$30–40", notes: "Train + Hase-dera + Great Buddha" },
    { category: "🏠 Accommodation (5 nights)", estimated: "Varies", notes: "Budget ~$80–150/night; not included in $1,000 estimate" },
    { category: "✈️ TOTAL (excl. flights + hotel)", estimated: "$930–1,150", notes: "Tight for 4; very doable for 3" }
  ],
  practicalInfo: [
    {
      title: "🌸 Cherry Blossom Forecast",
      items: [
        "Tokyo's sakura typically blooms around March 22–28 — your trip (Mar 14–19) catches the very start of the season.",
        "Early-blooming varieties (Kawazu, Kanzan) may show first blossoms by your last couple of days.",
        "Best spots: Ueno Park (1,200 trees), Shinjuku Gyoen, and Nakameguro canal.",
        "Check the Japan Meteorological Corporation sakura forecast closer to your trip for exact timing."
      ]
    },
    {
      title: "📶 SIM Card & Data",
      items: [
        "Get a pocket WiFi rental or data SIM at the airport arrivals hall.",
        "IIJmio, Sakura Mobile, or any airport kiosk all work well — 15GB covers 3–4 people sharing a WiFi.",
        "Google Maps with downloaded offline maps is your essential tool.",
        "Japan's mobile signals are strong everywhere, including trains and subways."
      ]
    },
    {
      title: "🗣️ Language & Vegetarian Card",
      items: [
        "Google Translate camera mode reads kanji menus instantly — game changer.",
        "Show this card for dad at restaurants: '私は菜食主義者です。卵は食べられます。肉、魚、鶏肉は食べられません。'",
        "(Translation: I am vegetarian. I can eat eggs. No meat, fish, or chicken.)",
        "The phrase 'Sumimasen' (sue-me-mah-sen) = excuse me / sorry — gets you everywhere."
      ]
    },
    {
      title: "🏨 Accommodation Tips",
      items: [
        "Base: Shinjuku or Shibuya — best transport links for this itinerary.",
        "Group of 3–4: consider Airbnb apartments (more space, kitchen for breakfast) or Dormy Inn / APA Hotel chains.",
        "Book well ahead — March is peak sakura season and hotels fill up fast.",
        "Many Tokyo hotels offer luggage forwarding services (yamato transport) — ship bags to airport the night before."
      ]
    },
    {
      title: "🧳 Packing & Practical",
      items: [
        "March weather: 8–15°C — pack layers and a light waterproof jacket.",
        "Comfortable walking shoes are non-negotiable — Tokyo days easily reach 15,000+ steps.",
        "Keep some yen cash: many smaller restaurants and shrines are cash only.",
        "7-Eleven ATMs accept all international cards — convenient everywhere."
      ]
    }
  ]
};

// Run fulfillment
try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfillment complete:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Fulfillment failed:', err.message);
  process.exit(1);
}
