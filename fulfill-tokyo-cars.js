const fulfillOrder = require('./functions/fulfill-order');

const order = {
  id: 'order_1771302235452_gr3ds8',
  email: 'fsalinas40@outlook.com',
  destination: 'Tokyo, Japan',
  startDate: '2026-10-23',
  endDate: '2026-11-01',
  groupSize: '5+',
  travelStyle: ['Adventure', 'Cultural', 'Foodie', 'Nightlife'],
  dining: 'Mix of everything',
  budget: '$1,000-2,000',
  requests: 'Would love to see the car scene, nightlife, good food, museums.'
};

const itineraryData = {
  destination: "Tokyo, Japan",
  countryEmoji: "🇯🇵",
  title: "Tokyo: JDM Culture, Late Nights & Street Eats",
  subtitle: "9 days of car meets, neon-lit nightlife, world-class museums, and the best food on earth",
  description: "This Tokyo itinerary is built for a crew that lives for JDM car culture, late-night adventures, and eating everything in sight. From legendary car meets at Daikoku PA to golden hour at Shinjuku's Golden Gai, from go-kart racing through city streets to quiet mornings at world-class museums — this trip balances adrenaline with culture, and every night ends somewhere unforgettable.",
  duration: "10 days / 9 nights",
  dates: "Oct 23 – Nov 1, 2026",
  budget: "$1,000–2,000 per person",
  pace: "Moderate – packed but balanced",
  bestFor: "Car enthusiasts, nightlife lovers, foodies, groups of 5+",
  highlights: [
    "Daikoku PA & Tatsumi PA car meets",
    "Go-kart street racing through Tokyo",
    "Shinjuku Golden Gai & Shibuya nightlife",
    "TeamLab Borderless & Mori Art Museum",
    "Tsukiji Outer Market & ramen deep dives",
    "Akihabara gaming & JDM culture",
    "Tokyo National Museum & Meiji Shrine"
  ],

  essentials: [
    { title: "🚇 Get a Suica/Pasmo Card", text: "Load it at any station. Works on trains, buses, and convenience stores. Essential for a group navigating Tokyo." },
    { title: "🌐 Pocket WiFi", text: "Rent at Narita/Haneda airport. One device per 2-3 people. You'll need maps constantly." },
    { title: "🚗 Car Meets Are Late Night", text: "Daikoku PA and Tatsumi PA peak around 10pm–2am on Friday/Saturday nights. Plan naps accordingly." },
    { title: "🍜 Eat at Counters", text: "Many of Tokyo's best spots seat 6-8 max. Your group may need to split for ramen shops — worth it." },
    { title: "💴 Carry Cash", text: "Many izakayas, small ramen shops, and Golden Gai bars are cash only. 7-Eleven ATMs accept foreign cards." },
    { title: "🎃 Halloween Week!", text: "You're arriving during Tokyo's massive Halloween celebration (Oct 31). Shibuya gets wild — embrace it." }
  ],

  days: [
    {
      num: 1,
      date: "2026-10-23",
      neighborhoods: "Shinjuku · Kabukichō",
      title: "Arrival & Shinjuku Neon Baptism",
      description: "Land in Tokyo, get settled, and dive straight into the sensory overload of Shinjuku. Tonight is about getting your bearings and your first taste of Tokyo nightlife.",
      timeBlocks: [
        {
          label: "Afternoon",
          activities: [
            { title: "Arrive & Check In", description: "Arrive at Narita or Haneda. Take the Narita Express or Limousine Bus to Shinjuku. Check into your hotel and grab Suica cards.", details: ["💡 Book hotel in Shinjuku or Shibuya for easy nightlife access"] }
          ]
        },
        {
          label: "Evening",
          activities: [
            { title: "Omoide Yokocho (Memory Lane)", description: "Squeeze into the narrow alleys of Piss Alley for yakitori, beer, and atmosphere. Tiny stalls seat 4-6 people so split the group and explore.", details: ["📍 Just outside Shinjuku Station west exit", "🍢 Try the chicken skin (kawa) and cartilage (nankotsu)"] }
          ],
          meals: [
            { type: "Dinner", name: "Omoide Yokocho Yakitori Alley", description: "Charcoal-grilled skewers and cold beer in Tokyo's most atmospheric alley.", meta: "¥1,500-2,500/person · Cash only" }
          ]
        },
        {
          label: "Night",
          activities: [
            { title: "Shinjuku Golden Gai – Night 1", description: "200+ tiny bars packed into six narrow alleys. Each seats 5-10 people. Many have cover charges (¥500-1,000) but the vibe is unmatched. Try 2-3 bars minimum.", details: ["🍸 Look for bars with English signs if language is a concern", "💡 Some bars have themes — jazz, punk, cinema, horror"] }
          ],
          tips: [
            { type: "tip", text: "Golden Gai bars often have a ¥500-1,000 cover charge per person. Budget for 3-4 bars at ~¥2,000-3,000 total including drinks." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6938, lng: 139.7005, label: "Omoide Yokocho", num: 1, cat: "food", desc: "Yakitori alley near Shinjuku Station" },
        { lat: 35.6936, lng: 139.7046, label: "Shinjuku Golden Gai", num: 2, cat: "nightlife", desc: "200+ tiny themed bars" },
        { lat: 35.6896, lng: 139.6917, label: "Shinjuku Station", num: 3, cat: "transport", desc: "World's busiest station — your home base" }
      ]
    },
    {
      num: 2,
      date: "2026-10-24",
      neighborhoods: "Shibuya · Harajuku · Omotesandō",
      title: "Shibuya Crossing, Street Style & Saturday Night",
      description: "Explore Tokyo's most iconic neighborhoods by day, then experience Shibuya's legendary Saturday nightlife. This is the day to go-kart through the city streets.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Shibuya Crossing & Hachiko", description: "See the world's busiest pedestrian crossing. Visit the Hachiko statue. Hit up Shibuya Sky observatory for panoramic views if the group is into it.", details: ["📍 Shibuya Sky tickets: ¥2,000 — book online to skip lines"] }
          ],
          meals: [
            { type: "Breakfast", name: "Bills Omotesandō", description: "Famous ricotta pancakes. Perfect fuel for a big day. Popular with groups.", meta: "¥1,800-2,500/person · Reservation recommended" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "🏎️ Street Go-Kart Experience", description: "The legendary Tokyo go-kart experience — dress up in costumes and race real go-karts through city streets. Multiple companies operate from Shibuya. International driving permit required.", details: ["⚠️ You NEED an International Driving Permit (IDP) — get this before you leave home!", "🏎️ Companies: Tokyo Kart, Akiba Kart — book 2+ weeks ahead for groups", "📸 This is a top-5 Tokyo experience. Budget ¥8,000-10,000/person for 2hrs"] }
          ],
          tips: [
            { type: "reddit", text: "The go-kart experience is 100% worth it. Get the costume rental. You will feel like an absolute legend driving through Shibuya in a Mario outfit.", cite: "r/JapanTravel" }
          ]
        },
        {
          label: "Evening",
          meals: [
            { type: "Dinner", name: "Genki Sushi Shibuya", description: "High-speed conveyor belt sushi. Fun for groups, surprisingly good quality.", meta: "¥2,000-3,500/person" }
          ]
        },
        {
          label: "Night",
          activities: [
            { title: "Shibuya Nightlife Crawl", description: "Shibuya has everything — clubs, bars, karaoke. Hit up WOMB or Sound Museum Vision for dancing, or rent a karaoke room at Big Echo for the full group.", details: ["🎤 Karaoke: Big Echo or Joysound — ¥500-800/person/hour with drinks", "🎶 Club WOMB: ¥2,000-3,500 cover, world-class DJs on Saturdays"] }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6595, lng: 139.7004, label: "Shibuya Crossing", num: 1, cat: "attraction", desc: "World's busiest pedestrian crossing" },
        { lat: 35.6652, lng: 139.7103, label: "Harajuku / Takeshita Street", num: 2, cat: "attraction", desc: "Street fashion and crepe shops" },
        { lat: 35.6613, lng: 139.7042, label: "Street Go-Kart Shibuya", num: 3, cat: "activity", desc: "Go-kart through city streets in costume" },
        { lat: 35.6614, lng: 139.6979, label: "Club WOMB", num: 4, cat: "nightlife", desc: "Legendary Shibuya club" },
        { lat: 35.6597, lng: 139.6986, label: "Shibuya Sky", num: 5, cat: "attraction", desc: "Panoramic rooftop observatory" }
      ]
    },
    {
      num: 3,
      date: "2026-10-25",
      neighborhoods: "Odaiba · Daikoku PA",
      title: "🏎️ Car Culture Day — Daikoku PA & Odaiba",
      description: "THE day for car enthusiasts. Explore Odaiba's automotive attractions by day, then make the pilgrimage to Daikoku Parking Area for one of the world's most famous car meets.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "MEGA WEB / Toyota Gazoo Racing Garage", description: "Toyota's massive showroom in Odaiba (or its successor exhibit). Test drive concepts, see racing history, and nerd out on JDM legends.", details: ["📍 Palette Town, Odaiba — take the Yurikamome line", "💡 Free entry to most exhibits"] }
          ],
          meals: [
            { type: "Brunch", name: "Diver City Food Court", description: "Massive food court next to the life-size Gundam statue. Ramen, curry, sushi — something for everyone.", meta: "¥800-1,500/person" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Odaiba Seaside & Gundam", description: "See the life-size Unicorn Gundam at DiverCity. Walk the Rainbow Bridge waterfront. Great photo ops with Tokyo skyline.", details: ["📍 The Gundam transforms at set times — check the schedule"] },
            { title: "MEGA WEB History Garage", description: "Classic car museum with vintage Toyota, Nissan, and other JDM icons. A pilgrimage for car nerds.", details: [] }
          ]
        },
        {
          label: "Evening",
          meals: [
            { type: "Dinner", name: "Odaiba Takoyaki Museum", description: "Multiple takoyaki stalls from Osaka's best. Perfect group food — cheap, delicious, fun.", meta: "¥500-1,000/person" }
          ]
        },
        {
          label: "Late Night",
          activities: [
            { title: "🏎️ Daikoku Parking Area Car Meet", description: "The mecca of Japanese car culture. On weekend nights, hundreds of modified cars gather — Skylines, Supras, RX-7s, bosozoku vans, itasha cars, everything. Free to attend. Take the Bayshore Route expressway or taxi from Odaiba.", details: ["📍 Daikoku PA, Bayshore Route (Wangan), Yokohama", "🕙 Peak time: 10pm–2am on Friday/Saturday nights", "📸 Bring your camera — this is bucket list stuff", "⚠️ Be respectful — don't rev engines, don't touch cars without permission"] }
          ],
          tips: [
            { type: "reddit", text: "Daikoku PA on a Saturday night is genuinely one of the best car experiences in the world. You'll see everything from million-dollar GT-Rs to crazy bosozoku trucks. Get there by 10pm.", cite: "r/JDM" },
            { type: "tip", text: "Getting there: Take a taxi or hire a van. It's on the expressway — no train access. Budget ¥5,000-8,000 for a group taxi from Odaiba." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6249, lng: 139.7756, label: "DiverCity / Gundam", num: 1, cat: "attraction", desc: "Life-size Unicorn Gundam & food court" },
        { lat: 35.6230, lng: 139.7780, label: "MEGA WEB / History Garage", num: 2, cat: "car", desc: "Toyota showroom & classic car museum" },
        { lat: 35.4618, lng: 139.6732, label: "Daikoku Parking Area", num: 3, cat: "car", desc: "Legendary late-night car meet spot" },
        { lat: 35.6290, lng: 139.7746, label: "Odaiba Seaside Park", num: 4, cat: "attraction", desc: "Waterfront views & Rainbow Bridge" }
      ]
    },
    {
      num: 4,
      date: "2026-10-26",
      neighborhoods: "Akihabara · Ueno",
      title: "Akihabara Electric Town & Tokyo National Museum",
      description: "Morning culture at one of the world's great museums, then an afternoon deep-dive into Akihabara's electric sensory overload — arcades, JDM model shops, anime, and everything in between.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Tokyo National Museum", description: "Japan's oldest and largest museum. The Honkan building alone has samurai armor, ukiyo-e prints, swords, and ceramics spanning thousands of years. Allow 2-3 hours.", details: ["📍 Ueno Park — take JR to Ueno Station", "🎟️ ¥1,000 admission", "💡 The Japanese Gallery (Honkan) is the must-see"] }
          ],
          meals: [
            { type: "Breakfast", name: "Kayaba Coffee", description: "Retro kissaten (old-school coffee shop) near Ueno. Famous egg sandwiches and thick-cut toast.", meta: "¥600-900/person" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Akihabara Deep Dive", description: "Electric Town delivers for car nerds and gamers alike. Hit up Super Autobacs for JDM parts, Tamiya model shops, retro game arcades, and figure shops.", details: ["🏎️ Super Autobacs A PIT: JDM parts paradise — even if you're not buying, it's incredible", "🕹️ Super Potato: Retro gaming heaven across 5 floors", "📍 Mandarake Complex: 8 floors of anime, manga, and collectibles"] }
          ],
          tips: [
            { type: "tip", text: "Akihabara's arcades have initial D arcade machines — race your crew on the actual game that defined drift culture." }
          ]
        },
        {
          label: "Evening",
          meals: [
            { type: "Dinner", name: "Kanda Matsuya", description: "Historic soba noodle shop near Akihabara. Been serving handmade buckwheat noodles since 1884.", meta: "¥800-1,200/person · Cash only" }
          ],
          activities: [
            { title: "Akihabara at Night", description: "The neon hits different after dark. Walk the main strip, hit another arcade, or explore the backstreets for hidden figures shops and maid cafés (for the experience).", details: [] }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7189, lng: 139.7766, label: "Tokyo National Museum", num: 1, cat: "museum", desc: "Japan's oldest museum — samurai armor, ukiyo-e, swords" },
        { lat: 35.7021, lng: 139.7715, label: "Akihabara Electric Town", num: 2, cat: "attraction", desc: "Arcades, JDM shops, anime culture" },
        { lat: 35.7147, lng: 139.7713, label: "Kayaba Coffee", num: 3, cat: "food", desc: "Retro coffee shop near Ueno" },
        { lat: 35.6984, lng: 139.7710, label: "Super Potato Retro Games", num: 4, cat: "attraction", desc: "5-floor retro gaming arcade" },
        { lat: 35.7012, lng: 139.7697, label: "Kanda Matsuya", num: 5, cat: "food", desc: "Historic soba since 1884" }
      ]
    },
    {
      num: 5,
      date: "2026-10-27",
      neighborhoods: "Toyosu · Tsukiji · Ginza",
      title: "Fish Market, Food Crawl & Ginza Luxury",
      description: "Start at the crack of dawn at Toyosu fish market, then eat your way through Tsukiji's outer market. Afternoon in upscale Ginza for a change of pace.",
      timeBlocks: [
        {
          label: "Early Morning",
          activities: [
            { title: "Toyosu Fish Market", description: "The world's largest fish market. Watch the tuna auction from the observation deck (arrive by 5:30am for best views). The market restaurants serve the freshest sushi you'll ever eat.", details: ["⏰ Tuna auction viewing: 5:30-6:30am — first come, first served", "📍 Toyosu Market Station on Yurikamome line"] }
          ],
          meals: [
            { type: "Breakfast", name: "Sushi Dai (Toyosu)", description: "Legendary omakase breakfast sushi. The line is long but moves. Expect a 1-2 hour wait — have part of the group wait while others explore.", meta: "¥3,000-5,000/person · Cash preferred" }
          ]
        },
        {
          label: "Late Morning",
          activities: [
            { title: "Tsukiji Outer Market Food Crawl", description: "The outer market is still thriving. Eat your way through — tamagoyaki (egg omelet on a stick), fresh uni, grilled seafood skewers, strawberry mochi.", details: ["🍣 Must-try: Fresh uni (sea urchin) cups, tamagoyaki, tuna skewers", "📍 Open ~5am–2pm, best before noon"] }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Ginza District", description: "Tokyo's upscale shopping district. Window-shop luxury brands, visit the Nissan Crossing showroom (free, showcases concept cars), and explore the iconic architecture.", details: ["🏎️ Nissan Crossing: Free showroom in Ginza 4-chome — concept cars and GT-R displays", "📍 Uniqlo Ginza flagship: 12 floors, Japan-exclusive items"] }
          ]
        },
        {
          label: "Evening",
          meals: [
            { type: "Dinner", name: "Ginza Kagari", description: "Michelin-recognized chicken paitan (creamy chicken broth) ramen. Rich, silky, unforgettable.", meta: "¥1,000-1,500/person · Expect a wait" }
          ],
          activities: [
            { title: "Chill Night / Recovery", description: "After the early morning, take it easy tonight. Explore a local konbini (convenience store) for snacks and Strong Zero — Japan's convenience stores are an experience unto themselves.", details: ["💡 Tomorrow is another big car day — rest up"] }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6455, lng: 139.7818, label: "Toyosu Fish Market", num: 1, cat: "food", desc: "World's largest fish market — tuna auction" },
        { lat: 35.6654, lng: 139.7707, label: "Tsukiji Outer Market", num: 2, cat: "food", desc: "Street food paradise — sushi, tamagoyaki, uni" },
        { lat: 35.6712, lng: 139.7649, label: "Nissan Crossing Ginza", num: 3, cat: "car", desc: "Free Nissan showroom — concept cars & GT-R" },
        { lat: 35.6717, lng: 139.7651, label: "Ginza Kagari Ramen", num: 4, cat: "food", desc: "Michelin chicken paitan ramen" }
      ]
    },
    {
      num: 6,
      date: "2026-10-28",
      neighborhoods: "Tatsumi · Daikanyama · Nakameguro",
      title: "🏎️ Tatsumi PA, Car Shops & Hip Tokyo",
      description: "Another car culture pilgrimage — Tatsumi PA and the JDM tuning shops of Tokyo. Afternoon in trendy Daikanyama and Nakameguro for a stylish counterpoint.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Up Garage & Autobacs Tour", description: "Visit Up Garage (Japan's biggest used car parts chain) and Autobacs for JDM parts shopping. Even if you can't ship parts home, the selection is jaw-dropping — Nismo, TRD, Mugen, Rays wheels.", details: ["📍 Multiple locations — Up Garage Shinagawa or Setagaya recommended", "💡 They ship internationally for larger items"] }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Daikanyama & Nakameguro", description: "Tokyo's most stylish neighborhoods. Daikanyama T-Site (a gorgeous bookstore), vintage clothing shops, and the Meguro River walk — autumn colors should be starting.", details: ["📍 Daikanyama T-Site: architecturally stunning Tsutaya bookstore", "🍂 Late October = early autumn foliage along the Meguro River"] }
          ],
          meals: [
            { type: "Lunch", name: "Afuri Ramen Nakameguro", description: "Famous yuzu shio (citrus salt) ramen. Light, refreshing, and perfect for a group. Multiple seats available.", meta: "¥1,000-1,400/person" }
          ]
        },
        {
          label: "Night",
          activities: [
            { title: "🏎️ Tatsumi Parking Area", description: "Another legendary car meet spot on the Bayshore Route. Smaller and more intimate than Daikoku — you'll see serious builds here. Wangan Midnight vibes.", details: ["📍 Tatsumi PA, Bayshore Route — taxi or hired car", "🕙 Best on weekday nights when Daikoku is quieter", "💡 This is the spot from Wangan Midnight — real heads know"] }
          ],
          tips: [
            { type: "reddit", text: "Tatsumi PA is more underground than Daikoku. Fewer tourists, more serious car people. Wednesday/Thursday nights are surprisingly active.", cite: "r/JDM" }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6280, lng: 139.8080, label: "Tatsumi Parking Area", num: 1, cat: "car", desc: "Underground car meet — Wangan Midnight vibes" },
        { lat: 35.6500, lng: 139.7030, label: "Daikanyama T-Site", num: 2, cat: "attraction", desc: "Stunning bookstore & lifestyle complex" },
        { lat: 35.6441, lng: 139.6988, label: "Nakameguro / Meguro River", num: 3, cat: "attraction", desc: "Trendy neighborhood, autumn foliage" },
        { lat: 35.6443, lng: 139.6985, label: "Afuri Ramen", num: 4, cat: "food", desc: "Famous yuzu shio ramen" },
        { lat: 35.6190, lng: 139.7250, label: "Up Garage Shinagawa", num: 5, cat: "car", desc: "JDM used parts paradise" }
      ]
    },
    {
      num: 7,
      date: "2026-10-29",
      neighborhoods: "Toyosu · Azabudai · Roppongi",
      title: "TeamLab, Mori Art Museum & Roppongi Nightlife",
      description: "Immerse yourselves in digital art at TeamLab, then take in panoramic views and contemporary art at Mori Art Museum. End with Roppongi's international nightlife scene.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "TeamLab Borderless (Azabudai Hills)", description: "The world's most famous digital art museum. Immersive, interactive rooms where art flows around you. Book tickets well in advance — this sells out.", details: ["🎟️ ¥3,800/person — book online 2-4 weeks ahead", "📍 Azabudai Hills, Minato — opened 2024 at new location", "⏱️ Allow 2-3 hours to explore properly"] }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Mori Art Museum & Tokyo City View", description: "Contemporary art museum on the 53rd floor of Mori Tower. The observation deck (Tokyo City View) offers 360° views. Great combo ticket available.", details: ["🎟️ ¥2,000 combo ticket for museum + observation deck", "📍 Roppongi Hills Mori Tower"] }
          ],
          meals: [
            { type: "Lunch", name: "Roppongi Hills Food Court", description: "Diverse options from soba to burgers. Easy for groups with different preferences.", meta: "¥1,000-2,000/person" }
          ]
        },
        {
          label: "Evening",
          meals: [
            { type: "Dinner", name: "Gonpachi Roppongi (Kill Bill Restaurant)", description: "The restaurant that inspired the crazy 88 fight scene in Kill Bill. Multi-level izakaya with soba, yakitori, and tempura. Great for groups.", meta: "¥3,000-5,000/person · Reservations recommended" }
          ]
        },
        {
          label: "Night",
          activities: [
            { title: "Roppongi Nightlife", description: "Tokyo's most international nightlife district. Mix of clubs, bars, and lounges. V2 Tokyo and 1OAK for clubbing, or explore the side streets for chill bars.", details: ["🎶 V2 Tokyo: Upscale club, international crowd", "🍸 Roppongi has more English-friendly bars than anywhere else in Tokyo", "⚠️ Avoid aggressive touts on the main strip — stick to known venues"] }
          ],
          tips: [
            { type: "tip", text: "Roppongi can be touristy on the main drag. The best bars are on side streets. Ask locals or hotel staff for recommendations." }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6596, lng: 139.7387, label: "TeamLab Borderless", num: 1, cat: "museum", desc: "Immersive digital art museum" },
        { lat: 35.6604, lng: 139.7292, label: "Mori Art Museum", num: 2, cat: "museum", desc: "Contemporary art + Tokyo City View" },
        { lat: 35.6624, lng: 139.7318, label: "Gonpachi (Kill Bill)", num: 3, cat: "food", desc: "Iconic izakaya from Kill Bill" },
        { lat: 35.6633, lng: 139.7316, label: "Roppongi Nightlife", num: 4, cat: "nightlife", desc: "International clubs and bars" }
      ]
    },
    {
      num: 8,
      date: "2026-10-30",
      neighborhoods: "Meiji Shrine · Aoyama · Ebisu",
      title: "Temples, Autumn Vibes & Pre-Halloween Night",
      description: "A more balanced day — morning serenity at Meiji Shrine, afternoon exploring Aoyama's car-friendly streets, and pre-Halloween festivities as Tokyo gears up for the big night.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Meiji Shrine (Meiji Jingū)", description: "Tokyo's most famous Shinto shrine, set in a 170-acre forest in the heart of the city. Peaceful morning walk through towering torii gates and ancient trees.", details: ["📍 Short walk from Harajuku Station", "⏱️ Allow 1-1.5 hours", "🍂 Beautiful autumn atmosphere in late October"] }
          ],
          meals: [
            { type: "Breakfast", name: "Commune Aoyama area cafés", description: "Trendy café culture in the Aoyama district. Great coffee and pastries.", meta: "¥800-1,200/person" }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Aoyama & Omotesandō Stroll", description: "Window-shop along Tokyo's Champs-Élysées. Architectural gems by Tadao Ando and Kengo Kuma. The Honda Welcome Plaza near Aoyama is worth a pop-in.", details: ["🏎️ Honda Welcome Plaza Aoyama: Free showroom with latest models and racing heritage", "📍 Omotesandō Hills for luxury shopping and architecture"] }
          ],
          meals: [
            { type: "Lunch", name: "Ichiran Ramen Shibuya", description: "The famous solo-booth ramen experience. Customize everything — noodle firmness, broth richness, spice level. Iconic.", meta: "¥980-1,500/person" }
          ]
        },
        {
          label: "Evening",
          activities: [
            { title: "Ebisu Yokocho & Beer Museum", description: "Ebisu is a chill, upscale neighborhood. Yebisu Beer Museum is free (tastings ¥400). Ebisu Yokocho is an indoor food hall with 20+ stalls — perfect for groups.", details: ["🍺 Yebisu Beer Museum: Free entry, paid tastings", "📍 Ebisu Yokocho: Indoor izakaya food hall"] }
          ]
        },
        {
          label: "Night",
          activities: [
            { title: "Pre-Halloween Night Out", description: "Tokyo's Halloween celebration is building. People start costuming up the night before. Hit Shibuya or Roppongi for the pre-party atmosphere.", details: ["🎃 Costumes are strongly encouraged — Tokyo goes ALL OUT", "💡 Don Quijote (Donki) sells cheap costumes everywhere"] }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6764, lng: 139.6993, label: "Meiji Shrine", num: 1, cat: "attraction", desc: "Tokyo's most famous shrine — 170-acre forest" },
        { lat: 35.6654, lng: 139.7121, label: "Honda Welcome Plaza Aoyama", num: 2, cat: "car", desc: "Free Honda showroom and racing heritage" },
        { lat: 35.6466, lng: 139.7103, label: "Ebisu Yokocho", num: 3, cat: "food", desc: "Indoor food hall — 20+ stalls" },
        { lat: 35.6467, lng: 139.7093, label: "Yebisu Beer Museum", num: 4, cat: "attraction", desc: "Free beer museum with tastings" },
        { lat: 35.6619, lng: 139.7038, label: "Omotesandō", num: 5, cat: "attraction", desc: "Tokyo's Champs-Élysées — architecture & luxury" }
      ]
    },
    {
      num: 9,
      date: "2026-10-31",
      neighborhoods: "Shibuya · Shinjuku",
      title: "🎃 Halloween in Tokyo — The Grand Finale",
      description: "It's Halloween in Tokyo and you're here for it. This is one of the biggest street parties in the world. Shibuya becomes a massive costume parade. This is your final big night — make it legendary.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Sleep In & Prep", description: "You'll need energy for tonight. Sleep in, grab a late breakfast, and start planning costumes. Don Quijote in Shibuya has entire floors of costumes and accessories.", details: ["🎃 Don Quijote (Donki) Shibuya: Open 24hrs, costumes on multiple floors", "💡 Group costumes hit different in Tokyo — go big"] }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Costume Shopping & Prep", description: "Hit up Don Quijote, Daiso, or the costume shops in Harajuku. Get ready early — the streets start filling up by 5-6pm.", details: [] }
          ],
          meals: [
            { type: "Lunch", name: "Fuunji Tsukemen Shinjuku", description: "One of Tokyo's best tsukemen (dipping ramen). Rich, thick dipping broth with firm noodles. The line moves fast.", meta: "¥900-1,100/person" }
          ]
        },
        {
          label: "Evening",
          activities: [
            { title: "🎃 Shibuya Halloween Street Party", description: "Shibuya's streets fill with hundreds of thousands of people in incredible costumes. The energy is insane. Walk around, take photos, soak it in. The area around Shibuya Crossing becomes a massive outdoor party.", details: ["📍 Center-gai and the streets around Shibuya Station", "📸 Some of the best costumes you'll ever see", "⚠️ Stay with your group — it gets PACKED", "💡 Designate a meeting point in case you get separated"] }
          ]
        },
        {
          label: "Night",
          activities: [
            { title: "Final Night Out", description: "After the street party, hit the clubs and bars. Every venue has Halloween events. This is your last big night — go all out.", details: ["🍻 Golden Gai will be extra wild tonight", "🎶 Every club in Shibuya has a Halloween event"] }
          ],
          meals: [
            { type: "Late Night", name: "Ichiran or 24hr Ramen", description: "End the night with a bowl of ramen. Tokyo's 24-hour ramen shops are a godsend after a big night out.", meta: "¥980-1,500/person" }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6595, lng: 139.7004, label: "Shibuya Crossing Halloween", num: 1, cat: "nightlife", desc: "Massive Halloween street party" },
        { lat: 35.6601, lng: 139.6988, label: "Don Quijote Shibuya", num: 2, cat: "attraction", desc: "24hr discount store — costumes galore" },
        { lat: 35.6932, lng: 139.7013, label: "Fuunji Tsukemen", num: 3, cat: "food", desc: "Top-tier dipping ramen in Shinjuku" },
        { lat: 35.6936, lng: 139.7046, label: "Golden Gai Halloween", num: 4, cat: "nightlife", desc: "200+ tiny bars — Halloween edition" }
      ]
    },
    {
      num: 10,
      date: "2026-11-01",
      neighborhoods: "Asakusa · Senso-ji · Narita",
      title: "Last Morning — Senso-ji & Sayonara",
      description: "A gentle final morning at Tokyo's oldest temple before heading to the airport. Pick up last-minute souvenirs and soak in one final Tokyo moment.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Senso-ji Temple & Nakamise Street", description: "Tokyo's oldest temple (built 645 AD). Walk through the iconic Kaminarimon gate, browse Nakamise shopping street for souvenirs — chopsticks, fans, snacks, keychains.", details: ["📍 Asakusa Station — 5 min walk", "🛍️ Nakamise-dori: Traditional souvenirs and street snacks", "⏱️ Allow 1-1.5 hours"] }
          ],
          meals: [
            { type: "Breakfast", name: "Asakusa street food", description: "Melon pan, ningyo-yaki (custard-filled cakes), and matcha soft serve from the stalls on Nakamise-dori.", meta: "¥300-800/person" }
          ]
        },
        {
          label: "Midday",
          activities: [
            { title: "Departure", description: "Head to Narita or Haneda airport. Narita Express from major stations takes ~60-90 minutes. Buy last-minute snacks (Tokyo Banana, KitKat flavors) at the airport.", details: ["🚃 Narita Express: ¥3,070 from Shinjuku/Shibuya", "💡 Airport shops have all the souvenir snacks you need", "✈️ Sayonara, Tokyo. You'll be back."] }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: "Senso-ji Temple", num: 1, cat: "attraction", desc: "Tokyo's oldest temple — 645 AD" },
        { lat: 35.7118, lng: 139.7963, label: "Nakamise Shopping Street", num: 2, cat: "food", desc: "Traditional souvenirs and street snacks" },
        { lat: 35.7720, lng: 140.3929, label: "Narita Airport", num: 3, cat: "transport", desc: "International departure" }
      ]
    }
  ],

  budgetTable: [
    { category: "Accommodation (9 nights)", budget: "$450–900", notes: "Hostel/Airbnb ($50-100/night split 5 ways)" },
    { category: "Food & Drinks", budget: "$250–450", notes: "Mix of street food, ramen, izakaya, konbini" },
    { category: "Transport (local)", budget: "$80–120", notes: "Suica card + taxi rides to car meets" },
    { category: "Activities", budget: "$150–300", notes: "Go-karts, TeamLab, museums, clubs" },
    { category: "Nightlife", budget: "$100–250", notes: "Cover charges, drinks, karaoke" },
    { category: "Shopping & Misc", budget: "$50–150", notes: "Souvenirs, JDM parts, costumes" }
  ],

  practicalInfo: [
    { title: "🚇 Getting Around", items: ["Tokyo's train system is world-class — get a Suica/Pasmo card immediately at any station", "For car meets (Daikoku PA, Tatsumi PA), you'll need taxis or a hired van — these are on expressways with no train access", "Budget ¥5,000-10,000 per car meet trip for group transport", "Google Maps works perfectly for train navigation in Tokyo"] },
    { title: "🚗 International Driving Permit", items: ["REQUIRED for the go-kart experience — Japan does not accept foreign licenses alone", "Apply in your home country before departure — processing takes 1-2 weeks", "Bring both your IDP and your original license"] },
    { title: "🗣️ Language", items: ["English is limited outside tourist areas", "Download Google Translate with Japanese offline pack before you go", "Most restaurants have picture menus or plastic food displays", "Train stations have English signage — you'll be fine navigating"] },
    { title: "💴 Money & Tipping", items: ["Do NOT tip in Japan — it's considered rude", "Carry cash — many izakayas, ramen shops, and Golden Gai bars are cash only", "7-Eleven and Japan Post ATMs reliably accept foreign cards", "Budget ¥3,000-5,000/day for food if eating mostly street food and ramen"] },
    { title: "🌤️ Weather (Late October)", items: ["Expect 15-20°C (60-68°F) — light jacket weather", "Possible rain — pack a compact umbrella", "Early autumn foliage starting, especially along rivers and in parks", "Evenings can be cool — a hoodie or light layer is enough"] },
    { title: "🎃 Halloween (Oct 31)", items: ["Tokyo's Halloween is massive, especially in Shibuya — hundreds of thousands in costume", "Alcohol restrictions may apply around Shibuya — check current rules closer to date", "Don Quijote (open 24hrs) sells costumes everywhere — group costumes hit different", "It's chaotic, fun, and unforgettable — stay with your group"] },
    { title: "👥 Group Size Tips", items: ["Groups of 5+ will need to split for small ramen shops and Golden Gai bars (most seat 6-8 max)", "Book restaurants ahead where possible — use TableLog or Gurunavi", "Izakayas and food halls are your best bet for group dining", "For karaoke, book a large room — most places accommodate groups easily"] }
  ]
};

const result = fulfillOrder(order, itineraryData);
console.log('✅ Order fulfilled!');
console.log('Slug:', result.slug);
console.log('URL:', result.url);
console.log('File:', result.filePath);
console.log('Email sent:', result.emailSent);
