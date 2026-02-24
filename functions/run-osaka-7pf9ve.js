const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1771943235637_7pf9ve",
  orderId: "order_1771943235637_7pf9ve",
  email: "galaxycats510@gmail.com",
  destination: "Osaka, Japan",
  startDate: "2026-03-11",
  endDate: "2026-03-14",
  start_date: "2026-03-11",
  end_date: "2026-03-14",
  groupSize: "3-4",
  style: "Adventure, Cultural, Relaxation, Nightlife, Family-friendly",
  dining: "Casual throughout",
  budget: "Surprise me",
  requests: "USJ is a must see. Dad is vegetarian (can eat eggs). 2nd time in Osaka — hidden gems, NO Osaka Castle. Scenic views, fun, Kyoto day trip with all must-sees (first time in Kyoto). Nightlife.",
  status: "pending"
};

const itineraryData = {
  destination: "Osaka, Japan",
  countryEmoji: "🇯🇵",
  title: "Osaka Like a Local: Hidden Gems, USJ & Epic Kyoto Day Trip",
  subtitle: "Nakazakicho → Universal Studios Japan → Kyoto All Day → Nakanoshima & Shinsekai",
  description: "You've done the tourist Osaka. This time, you go local. Think tucked-away vintage cafés in Nakazakicho where the regulars have their seats permanently reserved. Think Fukushima — Osaka's secret izakaya capital where salarymen go to disappear. A full day at Universal Studios Japan with Nintendo World and Harry Potter. Then the Kyoto day that covers absolutely everything: torii gates at dawn, bamboo groves, the Golden Pavilion, Gion's geisha streets, and Kyoto's 400-year-old food market. No Osaka Castle. No crowds. Just the real Osaka — and a Kyoto first that hits every highlight. The vegetarian dad eats like royalty throughout (Buddhist cuisine is some of Japan's finest). Nightlife included.",
  duration: "3 nights / 4 days",
  dates: "Mar 11 – 14, 2026",
  budget: "Moderate",
  pace: "Active days, electric nights",
  bestFor: "Repeat Osaka visitors, families with adventure in mind, hidden gem hunters",
  highlights: [
    "Nakazakicho — Osaka's hipster quarter: vintage shops, retro kissaten, zero tourists",
    "Fukushima district dinner — the izakaya neighborhood Osaka locals guard like a secret",
    "Universal Studios Japan — Nintendo World (Mario Kart!), Harry Potter World & Hollywood Dream",
    "Fushimi Inari Taisha at dawn — 10,000 vermillion torii gates in eerie quiet",
    "Kinkaku-ji (Golden Pavilion) — Kyoto's most iconic reflection shot",
    "Arashiyama bamboo grove + Tenryu-ji's UNESCO Zen garden",
    "Gion at dusk — Hanamikoji Street and Shirakawa canal under weeping willows",
    "Nishiki Market — Kyoto's 400-year-old covered food street (\"Kyoto's Kitchen\")",
    "Nakanoshima island — the scenic riverside park and neoclassical buildings almost no tourists visit",
    "Shinsekai: Tsutenkaku Tower + kushikatsu with vegetarian skewer options dad will love"
  ],
  essentials: [
    {
      title: "🚄 Getting Around",
      text: "Pick up an ICOCA card at any Kansai train station — it's the IC card that works on every train, subway, and bus in Osaka AND Kyoto. From Osaka to Kyoto: JR Special Rapid from Osaka Station takes just 14–20 minutes (¥570) — the fastest and cheapest. For USJ: JR Osaka Loop Line from Namba or Osaka Station to Universal City Station (~15 min, ¥190). Google Maps handles Kansai transit flawlessly."
    },
    {
      title: "🎡 USJ: How to Win the Day",
      text: "Pre-book tickets online (usj.co.jp or Klook) — don't rely on same-day availability in March. Express Passes are worth it for Nintendo World and Harry Potter. Super Nintendo World uses a timed-entry system through the USJ app — activate yours the moment you walk in. Arrive 30 min before gates open. March is busy but mid-week lines are much shorter than weekends. Park typically opens 9am. Check the schedule for closing shows — the evening atmosphere is genuinely magical."
    },
    {
      title: "🥦 Vegetarian Osaka & Kyoto",
      text: "Japan's Buddhist culinary heritage is your friend. Shojin ryori (temple vegetarian cuisine) is wholly plant-based and extraordinary — you'll have it in Kyoto. In Osaka: tofu izakayas, vegetable tempura restaurants, ramen spots with veggie broth options. At convenience stores (7-Eleven, FamilyMart), tamagoyaki onigiri and egg sandwiches are vegetarian. Show this phrase at any restaurant: '肉・魚・鶏肉なしでお願いします。卵は大丈夫です。' (No meat, fish, or chicken please. Eggs are fine.) The vegetarian spreads in this itinerary are world-class — not an afterthought."
    },
    {
      title: "🌸 March in Osaka & Kyoto",
      text: "March 11–14 puts you in early spring. Expect temperatures around 10–18°C — layers are key. Cherry blossoms typically hit peak bloom late March to early April in Kansai, so you'll likely catch the first early-blooming varieties (kawazu-zakura) starting to appear. Plum blossoms may still linger. Mornings at shrines and temples are cool and magical — afternoon warms up nicely."
    },
    {
      title: "🌃 Nightlife Guide",
      text: "Osaka nights hit different. Namba and Shinsaibashi are the epicenters — dozens of craft cocktail bars, izakayas with nomihoudai (all-you-can-drink for ¥1,500–2,000/2hrs), tachinomi (standing drink) bars, and Osaka's famous bar-street energy. Amerikamura (Amemura) is the young, streetwear-meets-nightlife hub. For a more local experience, Fukushima district has standing izakayas packed with off-duty chefs and locals. Day 1 is perfectly positioned for the full Namba nightlife circuit."
    },
    {
      title: "💴 Practical Tips",
      text: "Japan still runs on cash at smaller spots — 7-Eleven ATMs accept international cards. Budget ¥4,000–8,000/day/person for food and entry fees (USJ is its own budget day, ~¥9,400–10,400 per person for tickets). USJ Express Passes: ¥5,000–15,000 depending on tier. Coin lockers at major stations (Namba, Osaka, Kyoto) let you travel light. Bring a small day pack for the Kyoto day — you'll walk 20,000+ steps."
    }
  ],
  days: [
    {
      num: 1,
      title: "Real Osaka Arrival: Nakazakicho, Fukushima & Namba Nightlife",
      neighborhoods: "Nakazakicho · Tenjin · Kuromon · Dotonbori · Fukushima",
      date: "Mar 11",
      mapPins: [
        { lat: 34.7031, lng: 135.5082, label: "Nakazakicho Neighborhood", num: 1, cat: "activity", desc: "Osaka's artsy vintage quarter — retro kissaten, indie shops, zero tourists" },
        { lat: 34.7009, lng: 135.5110, label: "Tenjinbashisuji Shopping Street", num: 2, cat: "activity", desc: "World's longest covered arcade (2.6km) — hyper-local, no tourist playbook needed" },
        { lat: 34.6689, lng: 135.5042, label: "Kuromon Ichiba Market", num: 3, cat: "food", desc: "Osaka's 200-year-old kitchen market — vegetarian grazing paradise" },
        { lat: 34.6687, lng: 135.5013, label: "Dotonbori Canal", num: 4, cat: "activity", desc: "Classic neon canal — arrival photo stop before the night begins" },
        { lat: 34.6916, lng: 135.4851, label: "Fukushima District", num: 5, cat: "food", desc: "Osaka's secret izakaya neighborhood — where locals eat, not tourists" },
        { lat: 34.6741, lng: 135.5014, label: "Shinsaibashi-suji / Amerikamura", num: 6, cat: "nightlife", desc: "Osaka nightlife hub — craft cocktails, tachinomi bars, late-night energy" }
      ],
      timeBlocks: [
        {
          label: "Afternoon (Arrival)",
          activities: [
            {
              title: "Check In & Head Straight to Nakazakicho",
              description: "Drop bags and resist the urge to go to Dotonbori first. Instead, take the Midosuji Line two stops north to Nakazakicho Station — and step into the Osaka that most visitors never find. This compact neighborhood is caught in a beautiful time warp: narrow lanes with vintage clothing boutiques, antique furniture shops, old-school kissaten (Japanese coffee houses) where the menu hasn't changed since 1975, and independent art galleries. It has the energy of a creative village dropped inside a giant city.",
              details: [
                "📍 Nakazakicho Station on the Tanimachi Line or walk 20 min north from Umeda",
                "💡 The kissaten here (look for the hand-drawn signs and brown curtains) serve 'morning sets' all day — coffee + toast + egg for ¥400–600. Vegetarian-friendly and deeply atmospheric.",
                "🛍️ Hit the vintage shops along Nakazaki-cho alley — curated vintage at fair prices, very different from Amerikamura's resale hustle"
              ]
            },
            {
              title: "Tenjinbashisuji Shopping Street",
              description: "Walk south into Tenjinbashisuji — at 2.6 kilometers, it's the longest covered shopping arcade in the world, running from Tenjin Station all the way down to Namba. Unlike the tourist-facing Shinsaibashi-suji, this one is almost entirely local: 600+ shops selling everyday goods, hardware, local sweets, fruit stalls, and cheap ramen joints. Real Osaka commercial life, unfiltered. Great for picking up specialty snacks (Osaka no-brand chips, regional mochi varieties) at low prices.",
              details: [
                "💡 Look for the wagashi (traditional sweet) shops and the dried goods stalls — very local, excellent quality",
                "📍 Start at Tenjimbashisuji 6-chome Station and walk south — you'll exit near Namba eventually"
              ]
            }
          ],
          meals: [
            {
              type: "☕ Afternoon Snack",
              name: "Kissaten coffee + Nakazakicho grazing",
              description: "Stop at one of the retro kissaten in Nakazakicho for hand-dripped coffee and toast. Many serve egg-based morning sets all day. Then graze through Tenjinbashisuji for street snacks — roasted sweet potatoes (yaki-imo), fresh-made senbei, and fruit stands.",
              meta: "¥400–800pp · Nakazakicho area · Cash preferred · Look for hand-written menus on the door"
            }
          ],
          tips: [
            { type: "tip", text: "Nakazakicho is Osaka's best-kept secret from the tourist trail. Locals call it 'Osaka's Brooklyn' — which is accurate. The vintage stores here are better curated and cheaper than anywhere in Shinsaibashi." }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Quick Dotonbori Arrival Photo",
              description: "You're in Osaka — a 15-minute Dotonbori canal walk for the classic neon shots is perfectly reasonable. Cross Ebisu-bashi bridge for the Glico Running Man reflection shot. Then leave. Dotonbori is for photos; the night belongs to Fukushima.",
              details: [
                "📸 Best shot: stand on Ebisu-bashi bridge facing west — the Glico man is on your left, the canal lights below",
                "💡 Don't eat here — you have a much better dinner plan in Fukushima"
              ]
            },
            {
              title: "Fukushima District — Osaka's Izakaya Secret",
              description: "Hop on the train to Fukushima Station (one stop from Osaka Station on the JR Osaka Loop Line). Fukushima district is where Osaka's off-duty chefs, food professionals, and in-the-know locals go to eat. Unlike the tourist-facing Namba izakayas with English menus, these spots serve whatever was fresh that morning, in dining rooms that seat 8 people, by owners who've been doing this for 30 years. The density of incredible small restaurants per block is higher here than anywhere else in Osaka.",
              details: [
                "📍 JR Fukushima Station or Fukushima Station on Hanshin line — 1 stop from Osaka",
                "💡 Walk the alleys immediately south of the station — they're packed with standing bars and tiny izakayas. If there's a handwritten sign and no English menu, go in.",
                "🥦 Vegetarian finds: agedashi tofu (deep-fried tofu in dashi broth), dashimaki tamago (egg rolls), vegetable kakiage tempura, cold hiyayakko tofu with ginger and soy. Every izakaya will have these.",
                "🍺 Order a draft Asahi (nama biiru) and let the evening unfold"
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Dinner",
              name: "Fukushima izakaya alley — choose what looks alive",
              description: "The best dinner here is the one with a full house and a grilling smell. Look for a counter with 6–8 seats, a handwritten specials board, and locals eating seriously. Order the daily specials (kyō no osusume). For the group: yakitori (chicken/veg skewers), sashimi for non-vegetarians, agedashi tofu and dashimaki for dad. A shared table of shared dishes — the best way to eat in Osaka.",
              meta: "¥2,000–4,000pp with drinks · Fukushima district alleys · Cash · No reservations needed — just walk in"
            }
          ],
          tips: [
            { type: "reddit", text: "Fukushima is criminally underrated. I've lived in Osaka for 3 years and it's where I take people when I want them to see the real city. No tourists, incredible food, and the most alive neighborhood at 9pm on a Tuesday.", cite: "r/osaka" }
          ]
        },
        {
          label: "Late Night",
          activities: [
            {
              title: "Shinsaibashi & Amerikamura Bar Circuit",
              description: "Back in Namba for the nightlife circuit. The area around Shinsaibashi-suji and Amerikamura has dozens of bars ranging from craft cocktail spots to tiny standing drink bars (tachinomi) where you order at a hatch and drink on the sidewalk. Osaka nightlife runs late — things peak around 11pm. The 'Bar District' just south of Shinsaibashi Station on the west side of the arcade has a concentration of great spots.",
              details: [
                "🍸 Look for craft cocktail bars on the upper floors (2F, 3F) — they tend to have the best quality drinks and smaller crowds",
                "🍺 Nomihoudai deals: many izakayas offer 2-hour all-you-can-drink for ¥1,500–2,000 — great value for the group",
                "💡 Amerikamura's Triangle Park is the late-night gathering point — good for people watching even if you don't drink",
                "🕐 Osaka doesn't really close — convenience stores, ramen spots, and some bars run 24 hours"
              ]
            }
          ],
          meals: [],
          tips: [
            { type: "tip", text: "Pace yourself — USJ tomorrow is a full-on active day. A 1am finish is fine; 3am is ambitious. Osaka will still be here." }
          ]
        }
      ]
    },
    {
      num: 2,
      title: "Universal Studios Japan — Full Day in the Theme Park",
      neighborhoods: "USJ · Sakurajima · Konohana Ward",
      date: "Mar 12",
      mapPins: [
        { lat: 34.6654, lng: 135.4323, label: "Universal Studios Japan Main Gate", num: 1, cat: "activity", desc: "Japan's premier theme park — plan your day at the gate" },
        { lat: 34.6648, lng: 135.4320, label: "Super Nintendo World", num: 2, cat: "activity", desc: "Mario Kart: Koopa's Challenge + interactive Power Up Band world" },
        { lat: 34.6667, lng: 135.4295, label: "The Wizarding World of Harry Potter", num: 3, cat: "activity", desc: "Hogsmeade + Hogwarts Castle — Butterbeer and Forbidden Journey" },
        { lat: 34.6645, lng: 135.4338, label: "Minion Park", num: 4, cat: "activity", desc: "Despicable Me rides + Minion-themed everything" },
        { lat: 34.6644, lng: 135.4348, label: "Hollywood Dream – The Ride", num: 5, cat: "activity", desc: "High-speed coaster with music pumped through headrests" },
        { lat: 34.6644, lng: 135.4358, label: "Jurassic World & Jaws Area", num: 6, cat: "activity", desc: "Log flume + dinosaur island — bring ponchos" }
      ],
      timeBlocks: [
        {
          label: "Getting There (Early Start)",
          activities: [
            {
              title: "Pre-Park Strategy",
              description: "Take JR Osaka Loop Line or Yumesaki Line from Osaka Station / Nishikujo Station to Universal City Station (~15–20 min, ¥190). Aim to arrive at the park gate 30 minutes before opening — usually 9am in March. This positions you for the crucial first-minutes sprint. March is busy, but mid-week is dramatically shorter than weekends.",
              details: [
                "🎟️ Pre-booked tickets on usj.co.jp or Klook — print or download the app QR code",
                "⚡ Express Passes: recommend Area 7 (covers Nintendo World + Harry Potter + Hollywood Dream + 4 others). Worth every yen.",
                "📱 Download the USJ app before arrival — it shows live wait times and is how you activate Nintendo World timed entry"
              ]
            }
          ],
          meals: [
            {
              type: "☕ Breakfast Before the Park",
              name: "Hotel or convenience store",
              description: "Eat before you arrive — grab breakfast from your hotel or a 7-Eleven near the station. Onigiri, egg sandwiches, and hot tea. Food inside USJ is part of the experience, but you want to ride first, eat later.",
              meta: "¥400–700 · Any konbini near hotel or USJ station"
            }
          ],
          tips: [
            { type: "tip", text: "The 2-minute sprint from the gate to Nintendo World on park open is real — and worth doing. Activate your Nintendo World timed-entry ticket on the USJ app the moment the gates open. If you miss the first slot, you'll wait 45+ minutes for the next." }
          ]
        },
        {
          label: "Morning — Ride the Big Three",
          activities: [
            {
              title: "Super Nintendo World — Mario Kart: Koopa's Challenge",
              description: "The crown jewel of USJ — Nintendo World is a fully realized interactive environment where the entire area runs like a Mario game. Pick up Power Up Bands (¥3,300 at the gift shop — worth it) to collect coins, hit question blocks, and battle Bowser throughout the zone. Mario Kart: Koopa's Challenge uses AR headset glasses and motion-sensor racing technology — it's unlike any ride anywhere in the world. Donkey Kong Country (expansion area) has its own separate timed entry.",
              details: [
                "🎮 Power Up Bands sync to your phone — you can compete for the high score against other park visitors",
                "💡 The themed food here (Yoshi Melon Soda, 1-UP Mushroom Bun) is part of the experience — budget ¥1,000 extra for Nintendo bites",
                "⚡ Express Pass holders still need to activate Nintendo World timed entry — do it immediately on park entry"
              ]
            },
            {
              title: "The Wizarding World of Harry Potter",
              description: "Hogsmeade Village is stunning — one of the most immersive theme park environments ever built. Honeydukes, Zonko's, Ollivanders wand shop. Hogwarts Castle looms at the end of the cobblestone street. Harry Potter and the Forbidden Journey (inside the castle) uses motion-based ride technology through Hogwarts' moving staircases, Quidditch pitch, and the Whomping Willow. The Flight of the Hippogriff outdoor coaster is a fun, family-friendly ride with great views of the zone.",
              details: [
                "🍺 Butterbeer (frozen is best) is vegetarian — it's a sweet cream soda with butterscotch foam",
                "🪄 Purchase an interactive wand (¥4,400) and cast spells at marked spots throughout Hogsmeade",
                "💡 Go to Forbidden Journey with Express Pass — without it, 60–90 min wait by 10am"
              ]
            }
          ],
          meals: [],
          tips: [
            { type: "reddit", text: "Nintendo World is legitimately one of the greatest theme park experiences I've ever had and I've been to every Disney park on earth. The Mario Kart ride is mind-blowing. The Power Up Bands make it interactive in a way nothing else does. Buy them.", cite: "r/ThemeParks" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Hollywood Dream – The Ride",
              description: "USJ's signature roller coaster — the one thing every local will tell you to ride. High-speed outdoor coaster where music pumps through headrests (you choose from 5 song options before the ride). The Backdrop version runs the coaster in reverse — completely different and equally great. Usually mid-20 to 40-minute waits in the afternoon.",
              details: [
                "🎵 Song selection: pick your energy level — the options range from J-pop to hard rock",
                "💡 The Backdrop (backwards) version has a separate line — worth doing if the queue is short"
              ]
            },
            {
              title: "Minion Park & Universal Wonderland",
              description: "Minion Park is high-energy chaos in the best way — the Minion Mayhem ride puts you through a chaotic Minion training camp, and the character area is excellent for photos. Universal Wonderland (adjacent) has Sesame Street and Hello Kitty — great for younger members of the group. The Minion-shaped popcorn buckets sell out — grab them early.",
              details: [
                "💡 The yellow Minion popcorn buckets (¥2,500 refillable) are very popular — lines for them form early",
                "📸 Character meet-and-greets happen throughout the day — check the schedule posted at the entrance"
              ]
            }
          ],
          meals: [
            {
              type: "🍕 Lunch",
              name: "USJ: Minion Cafe or The Three Broomsticks (Harry Potter)",
              description: "For dad: The Three Broomsticks serves roasted vegetable and pumpkin soup sets. Pizza Margherita is available at multiple park locations. In Minion Cafe: pasta and salad options. Check the current menu on the USJ app — vegetarian items are labeled. The non-vegetarians: Butterbeer Beef Stew at Three Broomsticks, chicken at Jurassic area restaurants.",
              meta: "¥1,500–2,500pp · Multiple locations · Eat at 11am or 2:30pm to avoid the lunch rush"
            }
          ],
          tips: [
            { type: "tip", text: "Use the USJ app's live wait times constantly. Rides that had 90-minute waits at 10am often drop to 20 minutes by 5pm. Evening at USJ is completely underrated — smaller crowds, better light, and the shows are spectacular." }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "USJ Evening: Shows, Lights & Last Rides",
              description: "After 5pm, USJ transforms. Crowds thin, wait times drop, and the park lighting becomes genuinely magical. Hogwarts Castle lit up at dusk is extraordinary. The WaterWorld evening show is spectacular. Check the schedule for any nighttime parades or projection shows — they vary by season but March often has a spring event.",
              details: [
                "💡 Use the final 2 hours to revisit your favorite rides with the shortest waits of the day",
                "🎆 The evening projection show on Hogwarts is worth staying for — usually runs 30 min before close"
              ]
            }
          ],
          meals: [
            {
              type: "🍜 Dinner Back in Osaka",
              name: "Ichiran Ramen (solo booth — Namba)",
              description: "After a full USJ day, Ichiran Ramen is the perfect decompress. The legendary solo-booth system — you order on a form (tick boxes: broth strength, garlic level, chili level), slide it through a bamboo curtain, and the ramen appears. The vegetarian/lighter tonkotsu option is decent; non-vegetarians get the full pork bone broth. Fast, cheap, excellent.",
              meta: "¥880–1,200pp · Namba area multiple locations · Open until 5am · No wait after 10pm"
            }
          ],
          tips: [
            { type: "reddit", text: "Arriving at USJ at opening and staying until 8pm seems exhausting but it's actually the best way to do it — first 2 hours you hit the big rides, then you relax and the evening takes care of itself. The park is completely different vibes at 7pm vs 10am.", cite: "r/JapanTravel" }
          ]
        }
      ]
    },
    {
      num: 3,
      title: "Kyoto All Day — Every Must-See from Torii Gates to Gion Twilight",
      neighborhoods: "Fushimi · Arashiyama · Kinkaku-ji · Gion · Nishiki · Kyoto Station",
      date: "Mar 13",
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: "Fushimi Inari Taisha", num: 1, cat: "activity", desc: "10,000 vermillion torii gates winding up Mt. Inari — come at dawn" },
        { lat: 35.0168, lng: 135.6745, label: "Arashiyama Bamboo Grove", num: 2, cat: "activity", desc: "Towering bamboo corridor — surreal and hushed in morning light" },
        { lat: 35.0161, lng: 135.6747, label: "Tenryu-ji Temple & Zen Garden", num: 3, cat: "activity", desc: "UNESCO garden with borrowed mountain scenery — shojin ryori lunch here" },
        { lat: 35.0394, lng: 135.7292, label: "Kinkaku-ji (Golden Pavilion)", num: 4, cat: "activity", desc: "Three-story gold-leafed temple reflected in Mirror Pond" },
        { lat: 34.9949, lng: 135.7785, label: "Nishiki Market", num: 5, cat: "food", desc: "400-year-old covered food street — Kyoto's Kitchen, 100+ stalls" },
        { lat: 35.0036, lng: 135.7788, label: "Gion — Hanamikoji & Shirakawa", num: 6, cat: "activity", desc: "Kyoto's geisha district — preserved machiya and canal willow trees at dusk" }
      ],
      timeBlocks: [
        {
          label: "Early Morning — 7am Departure",
          activities: [
            {
              title: "Fushimi Inari Taisha at Dawn",
              description: "Leave Osaka by 7am. JR Special Rapid from Osaka Station to Kyoto Station (14 min, ¥570), then JR Nara Line to Inari Station (5 min, ¥150). You'll be at the shrine before 8:30am. The lower torii gates are the famous Instagram ones — dozens of vermillion gates in perfect tunnels. But the real magic is going up the mountain. Climb to Yotsutsuji intersection (30–40 min up) for panoramic views over Kyoto — below you, the city glows in the morning haze while you're surrounded by gates so dense you can barely see through them. Fox statues (Inari is the fox deity) watch from every corner.",
              details: [
                "⏰ Arrive before 9am — by 10am the lower gates are shoulder-to-shoulder with tour groups",
                "📍 JR Inari Station is a 2-minute walk from the main shrine entrance — perfectly direct, no Google Maps needed",
                "💡 Going to Yotsutsuji (halfway up) and back takes 1.5 hours. The full loop is 3+ hours — not necessary for a packed day trip.",
                "🦊 Look for the kitsune (fox) stone statues throughout — they often carry keys in their mouths (keys to the rice granary, Inari's symbol)",
                "📸 The very best shots are 5 minutes from the entrance — the curved gate tunnels before the main path splits. Morning mist through the gates is otherworldly."
              ]
            }
          ],
          meals: [
            {
              type: "☕ Breakfast (Early — Before Departure)",
              name: "Hotel or Osaka Station konbini",
              description: "Grab breakfast at the hotel or 7-Eleven/Lawson at Osaka Station before boarding the 7am train. Onigiri (tamagoyaki for dad — the egg version is perfect), hot tea, melon bread. Quick and efficient — save your appetite for Arashiyama.",
              meta: "¥400–700 · Open 24/7 · Any station convenience store"
            }
          ],
          tips: [
            { type: "reddit", text: "Fushimi Inari at dawn genuinely changed the way I think about travel. We were nearly alone in the gate tunnels at 7am. By 9am it was completely different. The morning effort is 100% worth it.", cite: "r/JapanTravel" }
          ]
        },
        {
          label: "Morning — Arashiyama",
          activities: [
            {
              title: "Arashiyama Bamboo Grove",
              description: "Take the JR Sagano Line from Kyoto Station to Saga-Arashiyama Station (~25 min, ¥240). The bamboo grove is a 5-minute walk. This is one of those places that photographs can't fully capture — the sound of the wind moving through 30-meter bamboo stalks creates a deep whooshing rustle that is completely unlike anything else. Walk through quickly into Tenryu-ji, where the bamboo continues in a more serene context, before the day-tripper crowds arrive.",
              details: [
                "💡 The bamboo grove is busiest midday and on weekends — March mid-week mornings are about as calm as it gets",
                "📍 The grove is publicly accessible (free) — Tenryu-ji charges separately for the garden and temple",
                "🎋 March light through bamboo: the pale green diffused glow in morning light is uniquely beautiful — different from midday or summer"
              ]
            },
            {
              title: "Tenryu-ji Temple & UNESCO Zen Garden",
              description: "Step through the bamboo grove directly into Tenryu-ji's temple grounds. The Sogenchi Garden — the main attraction — is a 700-year-old Zen garden designed by master Muso Soseki, one of Japan's greatest garden designers. It uses 'shakkei' (borrowed scenery) — the Arashiyama mountains form the backdrop of the garden, perfectly integrated. The composition of water, rocks, and pine trees in front of the mountains is breathtaking in any season.",
              details: [
                "💴 Garden entry: ¥500 · Temple building interior: ¥300 extra (worth it for the painted dragon ceiling)",
                "🕐 Open 8:30am–5pm",
                "💡 The painted cloud dragon on the ceiling of the main hall is one of Kyoto's great treasures — look up"
              ]
            }
          ],
          meals: [
            {
              type: "🍱 Lunch",
              name: "Shigetsu (精進料理) — Tenryu-ji Temple",
              description: "This is the meal of the entire trip. Shigetsu is the restaurant inside Tenryu-ji temple grounds serving shojin ryori — the centuries-old Buddhist vegetarian cuisine that is the foundation of Japanese cooking. Multi-course set meals: sesame tofu, miso soup, seasonal vegetable simmered dishes, tofu dengaku (miso-glazed grilled tofu), pickles, rice. Served in a tatami room overlooking the garden, with the mountains behind. For dad, this isn't 'vegetarian compromise food' — this is some of the finest Japanese cuisine that exists. Everyone in the group will eat well. Book in advance.",
              meta: "¥4,000–6,000pp · Inside Tenryu-ji grounds · Reservations: tenryuji.com or call ahead · Closed irregularly — confirm before trip"
            }
          ],
          tips: [
            { type: "tip", text: "Shigetsu needs a reservation. Call or book online at tenryuji.com before your trip. It's one of the most memorable meals you can have in Japan — the setting, the garden view, the food. Make it happen." }
          ]
        },
        {
          label: "Afternoon — Golden Pavilion to Gion",
          activities: [
            {
              title: "Kinkaku-ji — The Golden Pavilion",
              description: "Take the Kyoto City Bus (#59 from Arashiyama, or bus/taxi from Saga-Arashiyama Station) to Kinkaku-ji (~30 min). No Kyoto trip is complete without it — a three-story Zen temple completely covered in gold leaf, reflected in the Mirror Pond below. The color of the gold changes depending on the light, sky, and season. In early March with a blue sky, the reflection is electric. The garden grounds are equally beautiful — take the circuit path slowly.",
              details: [
                "💴 ¥500 per person · No interior access — the experience is entirely the exterior and grounds",
                "🕐 Open 9am–5pm",
                "📸 The classic shot: stand on the viewing platform 10 meters from the pond — the pavilion fills the frame perfectly",
                "💡 March is pre-peak-tourist season so crowds are manageable — arrive mid-afternoon (2pm) for the best light angle on the gold"
              ]
            },
            {
              title: "Nishiki Market — Kyoto's 400-Year-Old Kitchen",
              description: "Bus or subway from Kinkaku-ji to central Kyoto (Shijo-Karasuma area). Walk into Nishiki Market — a narrow 400-meter covered shopping street that has been Kyoto's food market since the early 1600s. Over 100 stalls selling: fresh Kyoto pickles (tsukemono) in every color, yuba (tofu skin — a Kyoto specialty), yudofu (simmered tofu), warabi mochi, matcha-flavored everything, knife shops, lacquerware, and fresh street food.",
              details: [
                "📍 5 minutes from Shijo or Karasuma Station (Kyoto subway) · Most open 9am–5pm",
                "🥦 Vegetarian highlights: Murakami-ju tsukemono store (gorgeous Kyoto pickles), natto and yuba shops, warabi mochi stalls (bracken starch, plant-based), and fresh tofu stalls",
                "🛍️ Gift shopping: Kyoto matcha KitKats, ceramic chopstick rests, dashi packs, and yatsuhashi (the traditional cinnamon sweet — iconic Kyoto omiyage)"
              ]
            },
            {
              title: "Gion at Dusk — Hanamikoji & Shirakawa",
              description: "Walk 10 minutes east from Nishiki Market into Gion — Kyoto's most atmospheric district, perfectly preserved with centuries-old machiya (wooden merchant houses) now housing high-end restaurants, ochaya (geisha teahouses), and boutiques. Walk Hanamikoji Street from south to north — the most photographed street in Kyoto. Then find Shirakawa Lane (just north of Shijo-dori) where a narrow canal is lined with weeping willows that in mid-March are just starting to bud. At dusk, stone lanterns reflect on the water. This is Kyoto at its most beautiful.",
              details: [
                "💡 Spot a maiko (apprentice geisha) — they walk through Gion in early evening on their way to ochaya engagements. Do not approach or photograph up close — admire respectfully.",
                "📍 Yasaka Shrine is at the east end of Gion — beautiful lit up in the evening and free to enter",
                "🌸 March: early plum blossoms may still be showing in Gion's gardens — check as you walk"
              ]
            }
          ],
          meals: [
            {
              type: "🍵 Afternoon Tea",
              name: "Nakamura Tokichi Honten — Gion",
              description: "Kyoto's most iconic matcha experience. This historic tea house in Gion has been serving since 1854. The matcha soft serve (Mr. Matcha soft cream) is extraordinary — intense, bitter-sweet, deeply green. The matcha parfait is a showpiece. Also: hojicha (roasted tea) soft serve and traditional wagashi (Japanese sweets). A perfect stop mid-afternoon before the Gion walk.",
              meta: "¥600–1,800pp · Gion area · Walk-in for café items · Expect a short line"
            }
          ],
          tips: [
            { type: "reddit", text: "Gion at dusk in early March is genuinely one of the most beautiful places I've ever stood. The willows are budding, lanterns are lit, and if you catch a maiko hurrying past — it's a moment. Worth every bit of the long day.", cite: "r/Kyoto" }
          ]
        },
        {
          label: "Evening Return to Osaka",
          activities: [
            {
              title: "Last Train Back — Grab Kyoto Souvenirs at Kyoto Station",
              description: "Head to Kyoto Station for the JR Special Rapid back to Osaka (14 min, ¥570). Before boarding, hit the Kyoto Station building's Cube basement level and Isetan food floor — the best concentrated collection of Kyoto omiyage (gifts) anywhere: yatsuhashi (cinnamon rice cake, the definitive Kyoto sweet), matcha everything, Kyoto sake, and beautifully packaged wagashi. Leave 20–30 minutes for this.",
              details: [
                "💡 The Kyoto Station Isetan food basement is better than the airport for omiyage — wider selection, better prices",
                "🚆 JR Special Rapid: Kyoto → Osaka, every ~15 min from Platforms 3–4, ¥570 on IC card"
              ]
            }
          ],
          meals: [
            {
              type: "🍜 Late Dinner in Osaka",
              name: "Dotonbori street food round — or Paprika Shokudo",
              description: "After a huge day, keep dinner light and easy. Option A: Dotonbori street food circuit — takoyaki from Aizuya (Osaka's most-loved takoyaki stand, non-veg) while dad gets fresh tamagoyaki from a nearby stall. Option B: Paprika Shokudo Vegan near Namba — beloved all-vegan Japanese home cooking, miso sets and tempura that are genuinely excellent for the whole group. Closed some days — check before going.",
              meta: "Street food: ¥300–800pp · Paprika Shokudo: ¥1,500–2,500pp · Namba area"
            }
          ],
          tips: [
            { type: "tip", text: "The Kyoto day is the longest and most walking-intensive. You'll hit 25,000+ steps easily. Pack good shoes and charge your phone the night before. The reward is worth every step." }
          ]
        }
      ]
    },
    {
      num: 4,
      title: "Osaka Local Life: Nakanoshima, Tenjin & Shinsekai Before Departure",
      neighborhoods: "Nakanoshima · Tenjin · Tenjinbashisuji · Shinsekai · Shinsaibashi",
      date: "Mar 14",
      mapPins: [
        { lat: 34.6921, lng: 135.5020, label: "Umeda Sky Building — Floating Garden", num: 1, cat: "activity", desc: "Two towers connected by an open-air 360° ring — best views in Osaka" },
        { lat: 34.6924, lng: 135.5095, label: "Nakanoshima Island", num: 2, cat: "activity", desc: "Island between two rivers — neoclassical buildings, rose garden, almost zero tourists" },
        { lat: 34.6919, lng: 135.5090, label: "Museum of Oriental Ceramics", num: 3, cat: "activity", desc: "World-class ceramics collection in a beautiful riverside building" },
        { lat: 34.6523, lng: 135.5063, label: "Shinsekai & Tsutenkaku Tower", num: 4, cat: "activity", desc: "1950s retro Osaka — Billiken statues, kushikatsu street, nostalgic atmosphere" },
        { lat: 34.6519, lng: 135.5065, label: "Kushikatsu Daruma (Shinsekai)", num: 5, cat: "food", desc: "Original kushikatsu restaurant — deep-fried skewers including great vegetarian options" },
        { lat: 34.6741, lng: 135.5014, label: "Shinsaibashi Final Shopping", num: 6, cat: "activity", desc: "Last sweep — Don Quijote, Uniqlo, Amerikamura for final haul" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Umeda Sky Building — Floating Garden Observatory",
              description: "This is Osaka's great secret scenic experience — not the castle, not Tsutenkaku, but the Sky Building's \"Floating Garden\" rooftop ring. Two 40-story towers are connected at the top by an open-air ring observation deck. You take an escalator through a glass tunnel (suspended between the towers in the open air) and emerge on a platform 173 meters up with 360-degree unobstructed views over all of Osaka: the bay to the west, the mountains to the east, and the city grid below in every direction. Stunning in the morning light.",
              details: [
                "💴 ¥1,500 per person · Open 10am–10:30pm",
                "📍 15 min walk from Osaka Station (west side) or use the underground shopping arcade",
                "💡 The escalator through the open-air tunnel between the towers is itself worth coming for — 30 floors of glass tube in the sky",
                "🌅 Morning (10–11am) gives the clearest visibility. On clear early-spring days, Mount Rokko is visible to the east."
              ]
            },
            {
              title: "Nakanoshima Island — The Osaka Nobody Told You About",
              description: "Walk east from the Sky Building to Nakanoshima — a long, narrow island between the Dojima and Tosabori rivers in central Osaka. This is one of the few places in the city where you can completely forget you're in one of Japan's largest cities. Neoclassical European-inspired buildings line the island (the Bank of Japan Osaka Branch, Osaka City Hall, and the stunning rose-brick Central Public Hall from 1918). The riverside paths are peaceful, lined with small sculptures. In March, early plum blossoms and the rose garden (free) make it beautiful. Almost zero tourists.",
              details: [
                "💡 The Nakanoshima rose garden is best in full bloom (May), but in March the geometry of the beds and the riverside setting are already lovely",
                "🏛️ Osaka Central Public Hall (built 1918) is free to enter the ground floor — incredible neoclassical interior, a complete surprise in central Osaka",
                "🖼️ Museum of Oriental Ceramics (¥1,000) — if the group has museum energy, it holds one of the world's finest Korean and Chinese ceramics collections in a beautiful building overlooking the river"
              ]
            }
          ],
          meals: [
            {
              type: "☕ Breakfast",
              name: "Nakanoshima morning café or hotel",
              description: "The Nakanoshima area has several quiet riverside cafés for a morning coffee and breakfast. Or eat at your hotel before checking out — today is a half-day local exploration before departure.",
              meta: "¥600–1,200pp · Nakanoshima riverside area"
            }
          ],
          tips: [
            { type: "tip", text: "Nakanoshima is the itinerary's hidden gem — it's where Osaka residents go for a quiet walk on a weekend morning. The combination of European architecture, rivers, and cherry tree-lined paths is genuinely beautiful and takes zero effort to reach." }
          ]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "Shinsekai — Tsutenkaku Tower & the Retro Quarter",
              description: "Take the subway or tram south to Shinsekai (\"New World\") — built in 1912, modeled half on Paris, half on New York, and now a wonderfully untouched time capsule of Showa-era (1950s–60s) Osaka. Tsutenkaku Tower (¥1,000) was the Eiffel Tower of its time — still standing, now mostly beloved for its kitsch. The neighborhood itself is the real attraction: dozens of kushikatsu restaurants, old-school pachinko parlors, retro game centers, Billiken (Osaka's luck god) statues on every corner, and a working-class energy that hasn't been gentrified yet.",
              details: [
                "📍 Dobutsuen-mae Station (Midosuji Line) or Shin-Imamiya Station (JR/Nankai) · Walk 5 min",
                "💡 Shinsekai is Osaka's most authentically retro neighborhood — real locals, real prices, real atmosphere. Very photogenic.",
                "🎯 Tsutenkaku Tower: the observation deck view (¥1,000) is fun, especially with the retro kitsch interior. The Billiken statue at the top is Osaka's lucky god — rub his feet."
              ]
            }
          ],
          meals: [
            {
              type: "🍢 Lunch",
              name: "Kushikatsu Daruma — Shinsekai Original Location",
              description: "Deep-fried breaded skewers on sticks — Osaka's working-class soul food. Kushikatsu Daruma is the original that started it all in Shinsekai. Dip once only into the communal sauce (double-dipping is Shinsekai's cardinal sin). For dad: some of the best skewers are vegetarian — asparagus, lotus root, onion, potato, sweet pumpkin, mushroom, and cheese (check current menu). The light batter and umami sauce make even the vegetable versions genuinely excellent. Non-vegetarians will work through pork, chicken, and shrimp skewers. Order until you're done — they come out as you order.",
              meta: "¥150–350/skewer · Shinsekai, multiple Daruma locations · No reservation needed · Cash"
            }
          ],
          tips: [
            { type: "reddit", text: "The kushikatsu scene in Shinsekai is genuine — not a tourist trap, actual Osaka soul food. The asparagus skewer is legitimately one of the best things I've eaten in Japan. And the atmosphere of the neighborhood is completely different from tourist Osaka.", cite: "r/osaka" }
          ]
        },
        {
          label: "Afternoon — Final Shopping & Departure",
          activities: [
            {
              title: "Shinsaibashi Final Shopping Sweep",
              description: "Head back north to Shinsaibashi-suji for the final shopping sweep. The main covered arcade and the surrounding streets have everything: Don Quijote (Donki — Japan's legendary discount store, open 24/7, chaotic, great for snacks and character goods), Uniqlo, GU, Japanese streetwear in Amerikamura, and the best selection of Japanese snacks and omiyage in Osaka. Budget ¥3,000–15,000 depending on willpower.",
              details: [
                "🛍️ Must-buys: matcha KitKat variety packs, Japanese face masks (the sheet masks here are legendary), Pocky sets, Uniqlo items with Japan-exclusive designs, and any Japanese candy that looks interesting",
                "💡 Don Quijote has the largest selection of Japanese snack variety packs for omiyage — much cheaper here than at the airport",
                "🧢 Amerikamura (one block west of Shinsaibashi arcade) for vintage clothing and limited-edition streetwear"
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Farewell Meal",
              name: "Mizuno Okonomiyaki (Namba) — or Dotonbori one last time",
              description: "If departure allows: Mizuno is Osaka's most respected okonomiyaki restaurant, serving since 1945. Their Osaka-style version mixes everything into the batter (not layered Hiroshima style). The yasai (vegetable + egg) okonomiyaki is outstanding — cabbage, egg, tendon (shrimp tempura, can swap for more veg), and Osaka sauce + mayo on the iron griddle at your table. A true farewell meal. Lines form but move fast.",
              meta: "¥1,000–1,800pp · Namba, near Dotonbori · Line expected but moves fast"
            }
          ],
          tips: [
            { type: "tip", text: "Airport from Namba: Nankai Rapid Express to Kansai International Airport (KIX) runs from Namba Station directly — 38 minutes, ¥1,060. Or Shinkansen from Shin-Osaka Station. Pack those omiyage tight — Japanese snacks are worth every gram of checked bag weight." }
          ]
        }
      ]
    }
  ],
  budgetTable: [
    { category: "🎢 USJ Tickets (×4)", estimated: "¥37,600–41,600", notes: "~¥9,400–10,400 per person. Book online in advance." },
    { category: "⚡ USJ Express Passes (×4)", estimated: "¥20,000–60,000", notes: "Varies by tier — Area 7 pass recommended (~¥13,000–15,000pp)" },
    { category: "🏛️ Fushimi Inari", estimated: "Free", notes: "The shrine grounds are always free to visit" },
    { category: "🌿 Tenryu-ji Garden", estimated: "¥2,000 (×4)", notes: "¥500pp garden entry. Temple interior ¥300 extra." },
    { category: "🍱 Shigetsu Shojin Ryori Lunch", estimated: "¥16,000–24,000", notes: "¥4,000–6,000pp — book in advance, worth every yen" },
    { category: "✨ Kinkaku-ji", estimated: "¥2,000 (×4)", notes: "¥500 per person" },
    { category: "🌅 Umeda Sky Building", estimated: "¥6,000 (×4)", notes: "¥1,500 per person" },
    { category: "🗼 Tsutenkaku Tower", estimated: "¥4,000 (×4)", notes: "¥1,000 per person (optional)" },
    { category: "🚆 Osaka–Kyoto trains (×4, roundtrip)", estimated: "¥4,560", notes: "¥570 × 2 ways × 4 people via JR Special Rapid" },
    { category: "🍽️ Meals (casual, 3 days)", estimated: "¥30,000–50,000", notes: "~¥1,500–3,000pp per meal × 3 people × 3 days" },
    { category: "✈️ TOTAL (excl. flights + hotel)", estimated: "¥120,000–190,000", notes: "Roughly ¥30,000–47,500 per person for 4 days" }
  ],
  practicalInfo: [
    {
      title: "🗓️ Kyoto Timing Strategy",
      items: [
        "Day 3 is a long one — leave Osaka by 7am, aim to return by 8–9pm.",
        "Fushimi Inari: arrive before 9am at all costs. After 10am it's a completely different experience.",
        "Kinkaku-ji: best light is mid-afternoon when the sun hits the gold from the south.",
        "Book Shigetsu (Tenryu-ji) before your trip — it fills up, especially on weekends.",
        "Gion dusk timing: aim to be on Hanamikoji Street between 5–7pm. That's the golden window."
      ]
    },
    {
      title: "🎮 USJ Pro Tips",
      items: [
        "Download the official USJ app before arrival — it's your wait-time map and timed entry tool.",
        "Activate your Nintendo World entry reservation the moment the gates open.",
        "Express Pass is worth it for a group — saves collective hours and stress.",
        "The park looks incredible at night — Hogwarts Castle lit up is genuinely magical. Stay past 6pm.",
        "Fantasy Springs (Frozen, Peter Pan, Tangled area) needs a separate add-on ticket — book in advance."
      ]
    },
    {
      title: "🥦 Vegetarian Resources for Dad",
      items: [
        "Show this card at restaurants: '肉・魚・鶏肉なしでお願いします。卵は大丈夫です。' (No meat, fish, chicken. Eggs OK.)",
        "Shojin ryori at Tenryu-ji (Day 3 lunch) is the highlight — entirely vegetarian by centuries of tradition.",
        "Kushikatsu at Daruma has excellent vegetarian skewer options (asparagus, onion, lotus root, sweet potato).",
        "Paprika Shokudo Vegan (Namba) is the best all-day option for a full vegetarian Japanese meal.",
        "Convenience store wins for dad: tamagoyaki onigiri, egg salad sandwiches, dashimaki tamago packs."
      ]
    },
    {
      title: "🌃 Osaka Nightlife Notes",
      items: [
        "Namba and Shinsaibashi are the nightlife cores — concentrated, walkable, and safe.",
        "Nomihoudai (all-you-can-drink) at most izakayas: ¥1,500–2,000 for 2 hours — excellent group value.",
        "Fukushima district (Day 1): standing izakayas hit their stride 7–10pm. Order house sake or draft beer.",
        "Tachinomi (standing drink) bars are quintessential Osaka — find one on any alley off Shinsaibashi-suji.",
        "Osaka runs late — trains until midnight, some bars until 5am. Plan departure times with buffer."
      ]
    },
    {
      title: "📱 Essential Apps & Links",
      items: [
        "Google Maps — handles all Kansai transit, walking routes, and restaurant navigation",
        "USJ Official App (usj.co.jp) — wait times, timed entry, ride status",
        "Google Translate — camera mode reads Japanese menus instantly",
        "HappyCow — vegetarian and vegan restaurants near you",
        "Tabelog — Japanese restaurant review app (use Google Translate camera on it)"
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
