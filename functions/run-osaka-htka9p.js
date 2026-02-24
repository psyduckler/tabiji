const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1771940508603_htka9p",
  orderId: "order_1771940508603_htka9p",
  email: "galaxycats510@gmail.com",
  destination: "Osaka, Japan",
  startDate: "2026-03-11",
  endDate: "2026-03-14",
  start_date: "2026-03-11",
  end_date: "2026-03-14",
  groupSize: "3-4",
  style: "Adventure, Cultural, Relaxation",
  dining: "Casual throughout",
  budget: "Surprise me",
  requests: "Father is vegetarian. USJ is a must see. Day trip to Kyoto planned. Enjoy scenic views, shopping, city vibes.",
  status: "in-progress"
};

const itineraryData = {
  destination: "Osaka, Japan",
  countryEmoji: "🇯🇵",
  title: "Osaka in 4 Days: Neon Lights, Universal & a Kyoto Escape",
  subtitle: "Dotonbori → Universal Studios Japan → Kyoto Day Trip → Osaka Castle & Shopping",
  description: "Osaka is Japan at its most electric — neon-lit canals, street food culture so deep it has its own philosophy (kuidaore: \"eat until you drop\"), theme park thrills, and the cultural depth of ancient Japan just 15 minutes away in Kyoto. This itinerary balances the must-sees with room to breathe: Universal Studios for the full-day adventure fix, a Kyoto day trip for temples and bamboo groves, and plenty of time for Osaka's legendary shopping and city vibes. The vegetarian father is fully covered — Japan's Buddhist culinary tradition means incredible plant-based eating at every stop.",
  duration: "3 nights / 4 days",
  dates: "Mar 11 – 14, 2026",
  budget: "Moderate",
  pace: "Active days, relaxed evenings",
  bestFor: "Families & groups craving adventure, culture & incredible food",
  highlights: [
    "Universal Studios Japan — Harry Potter, Nintendo World & Minion Park",
    "Dotonbori Canal at night — neon reflections & street food paradise",
    "Kyoto day trip: Fushimi Inari's 10,000 torii gates at dawn",
    "Arashiyama bamboo grove & Tenryu-ji's shojin ryori (Buddhist vegetarian cuisine)",
    "Osaka Castle & its panoramic cherry blossom gardens",
    "Umeda Sky Building's Floating Garden Observatory",
    "Shinsaibashi-suji & Amerikamura for world-class shopping",
    "Shinsekai & Tsutenkaku Tower — retro Osaka at its quirkiest",
    "Nishiki Market in Kyoto — 400-year-old \"Kitchen of Kyoto\"",
    "Vegetarian-friendly restaurants at every stop — Japan's tofu game is legendary"
  ],
  essentials: [
    {
      title: "🚄 Getting Around",
      text: "Get an IC card (ICOCA in Kansai) at any train station — works on trains, subways, and buses across Osaka and Kyoto. From Osaka to Kyoto: JR Special Rapid takes ~14 minutes from Osaka Station, or the Hankyu/Keihan lines are cheaper (~30 min). Taxis exist but trains are faster and cheaper. Google Maps works perfectly for transit navigation in Japan."
    },
    {
      title: "🎡 USJ Booking Tips",
      text: "Book Universal Studios Japan tickets and Express Passes in advance online (usj.co.jp or Klook). Express Passes skip the lines — worth every yen on busy days. Nintendo World and Harry Potter have separate timed entry reservations (book when tickets open). March is a busy season — go mid-week (Day 2, Thursday) for shorter queues. Gates open at 9am; arrive 30 min early."
    },
    {
      title: "🥦 Vegetarian in Japan",
      text: "Japan is incredibly accommodating for vegetarians when you know where to look. Shojin ryori (Buddhist temple cuisine) is 100% vegan/vegetarian and sublime. Look for tofu restaurants, tempura-ya (vegetable tempura), and soba shops (many have vegetarian dashi). Convenience stores (7-Eleven, FamilyMart) always have onigiri labeled for vegetarians. Key phrase: 'Niku to sakana nashi de' (no meat or fish, please)."
    },
    {
      title: "🌸 March in Osaka",
      text: "Early March means mild weather (10-18°C) and the very beginning of cherry blossom season — you may catch early blooms at Osaka Castle Park. The full bloom typically peaks late March to early April, but the city is beautiful and far less crowded than peak sakura weeks. Pack layers — mornings are cool but afternoons warm up."
    },
    {
      title: "💴 Money & Practical Tips",
      text: "Japan is still largely cash-driven at smaller restaurants and temples. Get yen at 7-Eleven ATMs (the most reliable for foreign cards). Budget ¥4,000-8,000/day per person for food (minus USJ). USJ runs ¥9,400-10,400 per adult for general admission; Express Passes ¥5,000-15,000+ depending on tier. Coin lockers at major stations let you store luggage while exploring."
    },
    {
      title: "📱 Apps to Download",
      text: "Google Maps (transit), Google Translate (camera mode for menus), Klook (USJ tickets), IC Card — SUICA app or physical ICOCA card. Japan Official Travel App for tourist info. Tabelog for restaurant reviews (use Google Translate on it)."
    }
  ],
  days: [
    {
      num: 1,
      title: "Arrival, Dotonbori Nights & the Namba Experience",
      neighborhoods: "Namba · Dotonbori · Shinsaibashi · Minami",
      date: "Mar 11",
      mapPins: [
        { lat: 34.6687, lng: 135.5013, label: "Dotonbori Canal", num: 1, cat: "activity", desc: "Osaka's neon heart — canal walkway lined with giant signs" },
        { lat: 34.6628, lng: 135.5017, label: "Namba Station", num: 2, cat: "activity", desc: "Southern Osaka hub — great transport connections" },
        { lat: 34.6689, lng: 135.5042, label: "Kuromon Ichiba Market", num: 3, cat: "food", desc: "Osaka's 200-year-old kitchen market — street food paradise" },
        { lat: 34.6741, lng: 135.5014, label: "Shinsaibashi-suji", num: 4, cat: "activity", desc: "Japan's longest covered shopping arcade" },
        { lat: 34.6720, lng: 135.4999, label: "Amerikamura (Amemura)", num: 5, cat: "activity", desc: "Trendy streetwear and vintage shopping district" },
        { lat: 34.6670, lng: 135.5044, label: "Hozenji Yokocho", num: 6, cat: "activity", desc: "Ancient laneway with mossy Fudo Myo statue — magical at night" }
      ],
      timeBlocks: [
        {
          label: "Afternoon (Arrival)",
          activities: [
            {
              title: "Check In & First Impressions",
              description: "Drop bags, grab an ICOCA card from the station, and head straight for Dotonbori. The canal area hits differently in the afternoon — you get a full sense of scale before the neon lights take over at sunset. Walk the canal walkway from end to end.",
              details: [
                "📍 Dotonbori is a 10-minute walk from Namba Station",
                "💡 The iconic Glico Running Man sign is the classic photo spot. Find it on the east bank of the canal near the Ebisu-bashi bridge.",
                "🧳 Coin lockers at Namba Station if you need to store bags before check-in"
              ]
            },
            {
              title: "Kuromon Ichiba Market",
              description: "Called 'Osaka's Kitchen,' this 200-year-old covered market has nearly 200 stalls. Go in the afternoon when everything is freshest and vendors are most interactive. Perfect for snacking your way through: fresh sashimi, grilled scallops, tamagoyaki (sweet omelette rolls), and seasonal produce.",
              details: [
                "📍 2-minute walk east of Dotonbori · Open 9am-6pm",
                "🥦 Vegetarian finds: fresh tofu stalls, roasted sweet potato, tamagoyaki (egg-based, no meat), seasonal fruit, and wagashi (Japanese sweets)"
              ]
            }
          ],
          meals: [
            {
              type: "🍜 Late Lunch / Snack",
              name: "Kuromon Market Stalls",
              description: "Graze the market stalls for an informal first meal. Look for the tofu shop (fresh cold tofu with soy sauce and ginger), the tamagoyaki stand, and roasted chestnuts if in season. For the non-vegetarians: the fresh scallop and sea urchin stalls are unmissable.",
              meta: "¥1,000-2,000pp · Kuromon Ichiba · Cash preferred"
            }
          ],
          tips: [
            { type: "tip", text: "Osaka's street food philosophy is kuidaore — 'eat until you drop.' Embrace it. Small bites at multiple stalls beats one big restaurant at this market." }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Dotonbori at Dusk & Neon Hour",
              description: "Dotonbori transforms at sunset. The giant Kani Doraku crab, the Glico man, the Dragon Ramen sign — they all come alive in neon. Walk the canal boardwalk both sides, cross Ebisu-bashi bridge for the classic photo, and soak in what is one of Asia's most visually electric urban environments.",
              details: [
                "💡 The best reflections on the canal happen just after dark (6:30-7pm in March). The neon lights mirror perfectly on still water.",
                "📸 Ebisu-bashi bridge has the iconic Glico Running Man — plan your group shot here"
              ]
            },
            {
              title: "Hozenji Yokocho",
              description: "Just steps from Dotonbori, this ancient stone laneway feels like another century. The mossy Fudo Myo'o statue at Hozenji Temple is Osaka's most beloved icon — locals splash water on it for good luck, giving it its distinctive green moss. Atmospheric izakayas line both sides of the narrow lane.",
              details: [
                "📍 Off Dotonbori, behind the Shochikuza theatre — look for the narrow stone entrance",
                "💡 Visit after 7pm when the lantern light is most magical"
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Dinner",
              name: "Paprika Shokudo Vegan",
              description: "Osaka's most beloved vegetarian/vegan restaurant — and a genuinely great meal for everyone in the group, not just the vegetarian. Warm, cozy space in Namba serving Japanese-style vegan cuisine: miso soup, vegetable tempura, tofu dishes, brown rice sets. The daily set menu is always excellent.",
              meta: "¥1,500-2,500pp · Near Namba · Small space, arrive early or expect a short wait · Closed Tuesdays"
            }
          ],
          tips: [
            { type: "reddit", text: "Paprika Shokudo is incredible even if you eat meat. The food is just delicious Japanese home cooking that happens to be vegan. Don't skip it.", cite: "r/osaka" }
          ]
        },
        {
          label: "Late Night",
          activities: [
            {
              title: "Shinsaibashi Stroll & First Night Drinks",
              description: "Walk north through Shinsaibashi-suji covered arcade — even at night, many shops stay open. Peek into Amerikamura (Amemura) for streetwear and the young Osaka crowd. For drinks: the bars around Namba and Shinsaibashi are some of Japan's best. Look for standing bars (tachinomi) for an authentic local experience.",
              details: [
                "💡 Many izakayas have 2-hour all-you-can-drink (nomihoudai) deals for ¥1,500-2,000. Great value for the group."
              ]
            }
          ],
          meals: [],
          tips: [{ type: "tip", text: "Day 1 is meant to be loose. Wander, eat small things, let Osaka wash over you. Don't over-plan the first night — the city reveals itself best on foot." }]
        }
      ]
    },
    {
      num: 2,
      title: "Universal Studios Japan — Full Day Adventure",
      neighborhoods: "USJ · Sakurajima · Konohana Ward",
      date: "Mar 12",
      mapPins: [
        { lat: 34.6654, lng: 135.4323, label: "Universal Studios Japan", num: 1, cat: "activity", desc: "Japan's premier theme park — Harry Potter, Nintendo World & more" },
        { lat: 34.6667, lng: 135.4295, label: "The Wizarding World of Harry Potter", num: 2, cat: "activity", desc: "Hogsmeade Village — butterbeer & Hogwarts castle" },
        { lat: 34.6648, lng: 135.4320, label: "Super Nintendo World", num: 3, cat: "activity", desc: "Mario Kart: Koopa's Challenge & interactive wristband world" },
        { lat: 34.6645, lng: 135.4338, label: "Minion Park", num: 4, cat: "activity", desc: "Despicable Me rides and Minion-themed food" },
        { lat: 34.6661, lng: 135.4310, label: "Universal Wonderland", num: 5, cat: "activity", desc: "Sesame Street and Hello Kitty area — perfect for younger visitors" },
        { lat: 34.6644, lng: 135.4348, label: "Hollywood Dream – The Ride", num: 6, cat: "activity", desc: "High-speed roller coaster with music pumped through headrests" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Early Entry & Nintendo World",
              description: "Arrive at gates 30 minutes before opening (8:30am if 9am open). Head straight to Super Nintendo World — it has limited timed entry via the USJ app, so activate your Nintendo World entry ticket immediately on arrival. Mario Kart: Koopa's Challenge is the must-ride. Buy wristbands (Power Up Bands, ~¥3,300) to collect coins and battle Bowser interactively throughout the zone.",
              details: [
                "🎮 Power Up Bands unlock interactive features across the entire Nintendo World area",
                "⚡ Express Pass holders: still get Nintendo World timed entry separate from Express Pass",
                "💡 Do the hardest-to-access rides first (Nintendo World, Forbidden Journey, Hagrids) before crowds build"
              ]
            },
            {
              title: "The Wizarding World of Harry Potter",
              description: "The attention to detail here is extraordinary — Hogsmeade Village, Honeydukes, Zonko's, and Hogwarts Castle looming at the end of the street. Harry Potter and the Forbidden Journey (inside the castle) is a must-ride. The Flight of the Hippogriff is a fun family coaster. Buy Butterbeer (frozen is best) and wizard wands for the interactive wand experience zones.",
              details: [
                "🧙 Butterbeer is vegetarian-friendly (it's a sweet cream soda drink)",
                "💡 The queue for Forbidden Journey can be 60-90 min without Express Pass — plan accordingly",
                "📍 Wand interaction spots are marked on the ground with footprint markers throughout Hogsmeade"
              ]
            }
          ],
          meals: [
            {
              type: "☕ Breakfast",
              name: "Three Broomsticks (Harry Potter area)",
              description: "Eat breakfast inside the Great Hall of Hogsmeade. The set meals include roasted chicken, corn soup, and pumpkin juice. Arrive right when the park opens for shortest wait and most atmospheric setting.",
              meta: "¥1,500-2,500pp · Wizarding World area · Opens with the park"
            }
          ],
          tips: [
            { type: "tip", text: "The Harry Potter area is magical even for non-fans. The design and attention to detail is genuinely extraordinary. Budget at least 2.5 hours here." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Minion Park & Despicable Me Ride",
              description: "Minion Park is extremely popular with families — Minion Mayhem (ride) and Minion Mischief (attraction) are both fun. The Minion-shaped churros and popcorn are Instagram gold. Universal's Lil Minion plushies are the best souvenir from USJ.",
              details: [
                "💡 The yellow popcorn buckets shaped like Minions are very popular and often sell out by afternoon"
              ]
            },
            {
              title: "Hollywood Dream & Jurassic World",
              description: "Hollywood Dream — The Ride is an outdoor roller coaster with music playing through headrests (you choose your playlist). The Jurassic World area has a log-flume ride — you WILL get wet, so plan accordingly for March weather.",
              details: [
                "💡 Water Shield ponchos (¥150) available throughout the park if you want to brave the water ride",
                "🦕 The Jurassic Park area redesigned as Jurassic World is spectacular — great theming and photo ops"
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Lunch",
              name: "Minion Cafe / Park-wide dining",
              description: "USJ has decent vegetarian options: pizza margherita, pasta dishes, vegetable curry, and salads at multiple locations. The character-themed food (Minion-shaped bread, Harry Potter themed items) is part of the fun. The vegetarian father can easily eat well — curry rice and pizza are everywhere.",
              meta: "¥1,500-3,000pp · Multiple USJ locations · Best to eat at 11am or 2pm to miss lunch rush"
            }
          ],
          tips: [
            { type: "reddit", text: "Get USJ's app before you go — it shows live wait times for all rides. Check it constantly. A 90-minute queue can drop to 20 min after 5pm. The evening golden hour at USJ is underrated — far fewer crowds.", cite: "r/JapanTravel" }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "USJ Nighttime — Less Crowds, Full Magic",
              description: "After 5pm, crowds thin out dramatically. This is the time to re-ride favorites with shorter queues, catch the evening light shows, and do the attractions you missed. The park often stays open until 9pm — the evening atmosphere with lights and fewer people is genuinely special.",
              details: [
                "💡 The Wizarding World at night with Hogwarts lit up is absolutely magical — worth staying for",
                "🎆 Check the daily schedule for nighttime shows and parades"
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Dinner",
              name: "Back in Osaka: Matsuri (居酒屋)",
              description: "After the park, head back to Namba for a proper izakaya dinner. Matsuri near Dotonbori is excellent — great vegetarian options (agedashi tofu, edamame, vegetable yakitori, cold tofu dishes) alongside dishes for the whole group. The lively atmosphere is perfect after a full USJ day.",
              meta: "¥2,000-3,500pp · Dotonbori area · Walk-in, nomihoudai available"
            }
          ],
          tips: [
            { type: "tip", text: "USJ to Namba: take the JR Osaka Loop Line from Universal City Station to Namba Station (~25 min, ¥190). Easy and direct." }
          ]
        }
      ]
    },
    {
      num: 3,
      title: "Kyoto Day Trip — Torii Gates, Bamboo & Zen Gardens",
      neighborhoods: "Fushimi · Arashiyama · Gion · Kyoto Station",
      date: "Mar 13",
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: "Fushimi Inari Taisha", num: 1, cat: "activity", desc: "10,000 vermillion torii gates winding up Mt. Inari" },
        { lat: 35.0168, lng: 135.6745, label: "Arashiyama Bamboo Grove", num: 2, cat: "activity", desc: "Surreal walking path through towering bamboo" },
        { lat: 35.0161, lng: 135.6747, label: "Tenryu-ji Temple & Garden", num: 3, cat: "activity", desc: "UNESCO World Heritage garden + Shigetsu shojin ryori restaurant" },
        { lat: 35.0050, lng: 135.7652, label: "Nishiki Market", num: 4, cat: "food", desc: "Kyoto's 400-year-old covered market — 'Kitchen of Kyoto'" },
        { lat: 35.0036, lng: 135.7788, label: "Gion District", num: 5, cat: "activity", desc: "Kyoto's geisha district — traditional machiya townhouses" },
        { lat: 34.9855, lng: 135.7588, label: "Kyoto Station", num: 6, cat: "activity", desc: "Return point — grab Kyoto snacks for the journey back" }
      ],
      timeBlocks: [
        {
          label: "Early Morning",
          activities: [
            {
              title: "Fushimi Inari at Dawn — Beat the Crowds",
              description: "Take the 7:30am train from Osaka to Kyoto (JR Special Rapid, ~14 min to Kyoto Station, then JR Nara Line 5 min to Inari Station). Arrive at Fushimi Inari by 8:15am — you'll have the lower torii gates nearly to yourself. Walk through the famous vermillion tunnels and climb at least to Yotsutsuji intersection (about 30-40 min up) for panoramic views over Kyoto. The gates thin out as you go higher — the upper mountain is serene.",
              details: [
                "📍 JR Inari Station is 2 min walk from the shrine entrance — perfectly direct",
                "⏰ Come before 9am to avoid tour groups. By 10am it can be shoulder-to-shoulder.",
                "💡 The full loop takes 2-3 hours. Going to Yotsutsuji (halfway) and back is ~1.5 hours and perfectly satisfying.",
                "🦊 Fushimi Inari is a shrine to Inari, god of foxes and rice — spot the fox statues throughout"
              ]
            }
          ],
          meals: [
            {
              type: "☕ Early Breakfast",
              name: "Convenience Store (Osaka Station)",
              description: "Grab breakfast from 7-Eleven or FamilyMart at Osaka Station before boarding — onigiri, hot tea, and pastries. Fast, delicious, and very Japanese. The egg salad sandwiches are legendary.",
              meta: "¥500-800pp · Any convenience store · Open 24/7"
            }
          ],
          tips: [
            { type: "reddit", text: "Fushimi Inari early morning is genuinely one of the most beautiful experiences in Japan. Even with other people around, the gates create a tunnel of orange that feels otherworldly.", cite: "r/JapanTravel" }
          ]
        },
        {
          label: "Morning–Midday",
          activities: [
            {
              title: "Arashiyama: Bamboo Grove & Tenryu-ji",
              description: "Take the JR Sagano Line from Kyoto Station to Saga-Arashiyama Station (about 25 min). Walk 5 minutes to the bamboo grove — the sound of bamboo swaying in the wind is meditative. Walk through to Tenryu-ji Temple, a UNESCO World Heritage site with one of Japan's finest Zen gardens: the famous 'borrowed scenery' garden uses the mountains behind as its backdrop.",
              details: [
                "📍 Tenryu-ji garden entry: ¥500 · The temple interior is separate (¥300 extra)",
                "💡 The bamboo grove is stunning early and late — midday is busiest. Move quickly through to Tenryu-ji to escape crowds.",
                "🌿 March has fresh green bamboo — beautiful contrast with early plum blossoms still lingering"
              ]
            }
          ],
          meals: [
            {
              type: "🍱 Lunch",
              name: "Shigetsu (精進料理) at Tenryu-ji",
              description: "This is the lunch highlight of the trip. Shigetsu serves shojin ryori — traditional Zen Buddhist cuisine that is entirely vegetarian/vegan. It's served in a beautiful tatami room overlooking the temple garden. Multi-course set menus feature tofu, seasonal vegetables, miso, and pickles — refined, subtle, and deeply Japanese. Book ahead — it fills up. Non-vegetarians: you'll love it too. It's simply great food.",
              meta: "¥3,500-5,500pp · Inside Tenryu-ji temple grounds · Reservations strongly recommended: tenryuji.com"
            }
          ],
          tips: [
            { type: "tip", text: "Shigetsu is one of the best vegetarian meals in Japan — a genuinely special experience. The father will love it. Book this 1-2 weeks in advance." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Nishiki Market — Kyoto's Kitchen",
              description: "Take the Hankyu line or bus back to central Kyoto and walk Nishiki Market — a narrow 400-meter covered shopping arcade lined with 100+ stalls selling Kyoto specialties. Try yudofu (simmered tofu), fresh pickles (tsukemono), warabi mochi, and grilled skewers. The fishmongers, tofu shops, and pickle stalls are incredible.",
              details: [
                "📍 Off Shijo-dori · Most stalls open 9am-5pm · Gets crowded from noon",
                "🥦 Vegetarian gems: Murakami-ju for tsukemono (pickles), Nishiki Warai for yuba (tofu skin), warabi mochi stalls",
                "🛍️ Great souvenir shopping: Kyoto matcha products, pickles, Japanese ceramics at adjoining Teramachi arcade"
              ]
            },
            {
              title: "Gion at Dusk",
              description: "Walk east to Gion — Kyoto's most atmospheric preserved district. Hanamikoji Street has perfectly preserved machiya (wooden merchant townhouses) that now house high-end restaurants and ochaya (geisha teahouses). Walk Shirakawa Lane (a canal lined with willows) as the light fades. Spotting a maiko (apprentice geisha) in the early evening is genuinely possible here.",
              details: [
                "💡 Do not approach or photograph geisha up-close — it's considered very rude. Admire respectfully from a distance.",
                "📍 Yasaka Shrine at the east end of Gion is free and beautiful in the evening light"
              ]
            }
          ],
          meals: [
            {
              type: "🍵 Afternoon Tea",
              name: "Nakamura Tokichi (Gion)",
              description: "Kyoto's most famous matcha experience — sencha, matcha, matcha parfaits, and hojicha desserts in a traditional townhouse. The matcha soft serve is extraordinary. A perfect afternoon stop in Gion.",
              meta: "¥800-1,800pp · Gion area · Walk-in for café items"
            }
          ],
          tips: [
            { type: "reddit", text: "Gion at dusk in early March is genuinely beautiful. The willow trees are starting to bud, it's cool but not cold, and the crowds are manageable compared to cherry blossom season.", cite: "r/kyoto" }
          ]
        },
        {
          label: "Evening Return",
          activities: [
            {
              title: "Back to Osaka — Namba Ramen",
              description: "JR Special Rapid from Kyoto to Osaka Station takes ~14 minutes (¥570). Back in Osaka for a relaxed evening. The group will be well-walked — dinner near the hotel, early night before the final day.",
              details: [
                "💡 Grab Kyoto omiyage (souvenirs) at Kyoto Station Cube basement before boarding — matcha KitKats, yatsuhashi sweets, and Kyoto pickles"
              ]
            }
          ],
          meals: [
            {
              type: "🍜 Dinner",
              name: "Kinryu Ramen (Dotonbori)",
              description: "The famous 24-hour ramen stand with a giant golden dragon on the roof. Tonkotsu ramen at ¥750 — one of the great Osaka late-night traditions. Vegetarians: opt for the Ichiran ramen nearby which has a vegetarian broth option. Quick, cheap, perfect after a long day.",
              meta: "¥750-1,200pp · Dotonbori · Open 24 hours"
            }
          ],
          tips: [
            { type: "tip", text: "Keep energy for Day 4 — it's the final shopping and sightseeing day, and Osaka Castle in the morning is beautiful when you're fresh." }
          ]
        }
      ]
    },
    {
      num: 4,
      title: "Osaka Castle, Scenic Views & Final Shopping",
      neighborhoods: "Osaka Castle · Umeda · Shinsekai · Shinsaibashi",
      date: "Mar 14",
      mapPins: [
        { lat: 34.6873, lng: 135.5262, label: "Osaka Castle", num: 1, cat: "activity", desc: "Japan's most iconic castle with panoramic views" },
        { lat: 34.6873, lng: 135.5200, label: "Osaka Castle Park", num: 2, cat: "activity", desc: "Vast park with early cherry blossoms and moats" },
        { lat: 34.7036, lng: 135.4903, label: "Umeda Sky Building", num: 3, cat: "activity", desc: "Floating Garden Observatory — breathtaking 360° city views" },
        { lat: 34.6523, lng: 135.5063, label: "Tsutenkaku Tower & Shinsekai", num: 4, cat: "activity", desc: "Osaka's retro tower and 1950s-era entertainment district" },
        { lat: 34.6519, lng: 135.5065, label: "Shinsekai Kushikatsu Alley", num: 5, cat: "food", desc: "Deep-fried skewers — Osaka's most iconic working-class food" },
        { lat: 34.6741, lng: 135.5014, label: "Shinsaibashi Final Shopping", num: 6, cat: "activity", desc: "Last sweep of Japan's best covered shopping arcade" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Osaka Castle & the Park",
              description: "Head to Osaka Castle early for the best experience. The castle itself (¥600 entry) has a fascinating museum inside with samurai armor, swords, and Toyotomi Hideyoshi's story. Climb to the 8th floor observation deck for panoramic views over Osaka — on clear days you can see the mountains beyond. The surrounding park is enormous and beautiful, with early March plum blossoms possibly still in bloom.",
              details: [
                "📍 Osaka Castle Museum: ¥600 adults, open 9am-5pm",
                "🌸 The castle park has 600 cherry trees — by mid-March you may catch the very earliest blooms",
                "💡 View from the castle observation deck on a clear morning: the city skyline surrounded by green moats is genuinely spectacular",
                "⏰ Arrive by 9am — it fills with tour groups by 10:30am"
              ]
            }
          ],
          meals: [
            {
              type: "☕ Breakfast",
              name: "Café in Osaka Castle Park",
              description: "The park has several cafés near the main gate. Simple Japanese breakfast sets (toast, eggs, salad) or grab coffee and walk the moat paths. Starting the day outdoors in the park is a lovely way to see Osaka's green side.",
              meta: "¥800-1,500pp · Osaka Castle Park"
            }
          ],
          tips: [
            { type: "tip", text: "The castle grounds are free to walk — only the museum inside costs money. Even if you skip the interior, walking the stone walls and moats is impressive." }
          ]
        },
        {
          label: "Late Morning",
          activities: [
            {
              title: "Umeda Sky Building — Floating Garden Observatory",
              description: "One of Osaka's most architecturally dramatic experiences: two towers connected by a floating ring at the top with a 360° open-air observation deck. The view is stunning — Osaka's urban sprawl to every horizon, the bay to the west. The escalator ride through the glass tunnel between towers is itself a sight. Worth every yen.",
              details: [
                "📍 15-min walk from Osaka Station · ¥1,500 adults · Open 10am-10pm",
                "💡 The escalator from the 35th to 39th floor is suspended in the open air — impressive engineering",
                "🌅 The view from the open-air ring in the morning is beautiful — different quality of light than evening",
                "🛍️ The basement Takimi-koji has vintage Showa-era food stalls — great for lunch"
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Lunch",
              name: "Takimi-koji (Umeda Sky Building Basement)",
              description: "A recreated 1920s Osaka street market in the basement of the Sky Building. Atmospheric ramen, izakaya, and Japanese comfort food. Look for the tofu-based sets and vegetable tempura for the vegetarian father — the shokudo-style spots always have options. A unique and fun Osaka experience.",
              meta: "¥1,200-2,000pp · Umeda Sky Building B2 · Open from 11am"
            }
          ],
          tips: [
            { type: "reddit", text: "The Umeda Sky Building is one of those places that looks just okay in photos but is absolutely mind-blowing in person. The open-air 360° ring at the top is genuinely special.", cite: "r/osaka" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Shinsekai & Tsutenkaku Tower",
              description: "Shinsekai ('New World') was built in 1912 as Osaka's entertainment district — modeled half on Paris, half on New York. It's now a wonderfully retro, slightly gritty neighborhood full of kushikatsu (deep-fried skewer) restaurants, old-school pachinko parlors, and Billiken (Osaka's lucky god) statues. Tsutenkaku Tower (¥1,000) has observation decks and is Shinsekai's defining landmark.",
              details: [
                "📍 Tram or subway from Umeda to Shinsekai (~25 min)",
                "💡 Shinsekai has a nostalgic, Showa-era energy unlike anywhere else in Japan — embrace the kitsch",
                "🥢 Kushikatsu etiquette: dip once only into the communal sauce, never double-dip"
              ]
            },
            {
              title: "Final Shinsaibashi Shopping Sweep",
              description: "Return to Shinsaibashi-suji for final shopping. The 580-meter covered arcade has everything from Don Quijote (the famous discount store open 24/7 — great for snacks, cosmetics, character goods), to Uniqlo, to Japanese streetwear. Amerikamura one block west has vintage clothing and limited-edition sneakers. Budget 1-2 hours and bring ¥5,000-20,000 depending on willpower.",
              details: [
                "🛍️ Must-buys: Pocky variety packs, Japanese snacks, face masks (the Japanese ones are legendary), Uniqlo Osaka exclusives",
                "💡 Don Quijote (Donki) is a controlled chaos of a discount store — floor-to-ceiling everything at great prices. An Osaka institution.",
                "🧢 Amerikamura has great vintage finds and the Triangle Park is the social hub of young Osaka"
              ]
            }
          ],
          meals: [
            {
              type: "🍢 Snack",
              name: "Kushikatsu Daruma (Shinsekai)",
              description: "The original kushikatsu restaurant in Shinsekai — the place that put deep-fried skewers on the map. The vegetarian skewers are genuinely delicious: asparagus, onion, lotus root, mushroom, sweet potato, and cheese. Non-vegetarians will go through 15+ skewers each. Order at the counter and keep pointing.",
              meta: "¥150-300/skewer · Shinsekai · Multiple locations, look for the Daruma logo"
            }
          ],
          tips: [
            { type: "tip", text: "The vegetarian kushikatsu options at Daruma are honestly excellent — asparagus, pumpkin, lotus root, and mushroom skewers are some of the best on the menu. The batter is light and the sauce is addictive." }
          ]
        },
        {
          label: "Evening / Departure",
          activities: [
            {
              title: "Dotonbori Farewell",
              description: "One last walk through Dotonbori before heading to the airport or train station. Grab fresh takoyaki (octopus balls — a Osaka invention) from Aizuya or Osaka Ohsho for gyoza. Stop at a convenience store for last-minute snacks and drinks for the journey. Say goodbye to the neon crab.",
              details: [
                "✈️ Kansai International Airport (KIX): Nankai Rapid from Namba Station (~38 min, ¥1,060) or Haruka Limited Express from Osaka Station (~65 min, ¥2,270)",
                "🚄 Shinkansen departures: from Shin-Osaka Station (subway from Namba ~15 min)"
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Farewell Dinner",
              name: "Mizuno Restaurant (Namba)",
              description: "If you have time before departure, Mizuno is the best okonomiyaki (Osaka savory pancake) in the city — their Osaka-style (toppings mixed in, not layered) has a 60+ year history. The yasai (vegetable) version is perfect for the father. Watch it cooked on the iron griddle at your table. A true Osaka goodbye.",
              meta: "¥1,000-1,800pp · Namba, near Dotonbori · Line possible but moves fast"
            }
          ],
          tips: [
            { type: "tip", text: "Buy extra Japanese snacks, matcha KitKats, and Pocky at Don Quijote before leaving — they're cheaper and better here than at the airport. Load up your suitcase." }
          ]
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
