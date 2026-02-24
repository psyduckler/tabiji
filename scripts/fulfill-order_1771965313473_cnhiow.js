const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771965313473_cnhiow',
  email: 'ssgaming187@gmail.com',
  destination: 'Okinawa, Japan',
  startDate: '2026-07-15',
  endDate: '2026-07-22',
  groupSize: '3-4',
  requests: ''
};

const itineraryData = {
  destination: 'Okinawa, Japan',
  countryEmoji: '🇯🇵',
  title: 'Island Time in Okinawa',
  subtitle: '7 days of turquoise seas, ancient kingdoms & soul-warming soba for your crew',
  description: "Okinawa isn't quite Japan and it isn't quite tropical — it's something entirely its own. A former Ryukyu Kingdom with UNESCO castles crumbling into jungle, beaches that rival the Maldives, and a food culture built around longevity and pork. This itinerary takes your group from Naha's buzzing Kokusai Street through sacred groves at Sefa Utaki, snorkeling the Kerama Blue, exploring the massive Churaumi Aquarium, and eating your way through soki soba shops and taco rice joints that only locals know. Summer means peak beach season, vibrant eisa festivals, and sunsets that melt into the East China Sea.",
  duration: '7 nights',
  dates: 'Jul 15 – Jul 22, 2026',
  budget: '$$',
  pace: 'Relaxed–Moderate',
  bestFor: 'Friends · Adventure · Foodies',
  highlights: [
    'Snorkeling the Kerama Islands — "Kerama Blue" is a real thing',
    'Churaumi Aquarium\'s whale shark tank — one of the world\'s largest',
    'Shuri Castle — rebuilt seat of the Ryukyu Kingdom',
    'Sefa Utaki — Okinawa\'s most sacred spiritual site',
    'Kokusai Street food crawl — taco rice, sata andagi, and awamori'
  ],

  essentials: [
    { title: '🌴 Summer Heat', text: 'July in Okinawa averages 30-33°C (86-91°F) with high humidity. Pack reef-safe sunscreen, rash guards for snorkeling, and stay hydrated. Afternoon thunderstorms are common but pass quickly — they cool things down beautifully.' },
    { title: '🚗 Getting Around', text: 'Okinawa has no train system (except the Naha monorail). Rent a car — it\'s essential for exploring beyond Naha. An International Driving Permit is required. Drive on the left. Parking is plentiful and usually free at attractions.' },
    { title: '🍜 Food Culture', text: 'Okinawan cuisine is distinct from mainland Japan. Pork is king (every part of the pig). Try soki soba, goya champuru, taco rice (an Okinawan invention), umibudo (sea grapes), and jimami tofu. Awamori is the local spirit — aged in clay pots.' },
    { title: '💴 Budget Tips', text: 'Okinawa is cheaper than Tokyo/Osaka. ¥1,000-1,500 lunches are everywhere. Convenience store onigiri + soba combos are great. Beach access is mostly free. Biggest costs: car rental (~¥5,000/day), Kerama boat tours (~¥8,000-12,000pp), and Churaumi entry (¥2,180).' }
  ],

  days: [
    {
      num: 1,
      date: '2026-07-15',
      neighborhoods: 'Naha · Kokusai Street · Tsuboya',
      title: 'Welcome to the Ryukyu Kingdom',
      description: "Land in Naha and dive straight into Okinawa's vibrant capital. Kokusai Street is a sensory overload of souvenir shops, street food, and live music. Then duck into the quiet backstreets of Tsuboya pottery village — a world apart, where artisans have been shaping Okinawan ceramics for 300 years.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive & Explore Kokusai Street',
              description: "After landing at Naha Airport, take the Yui Rail monorail to your hotel (Makishi or Kencho-mae station). Drop your bags and hit Kokusai Street — Naha's 1.6km main drag. It's touristy but genuinely fun, with covered arcades branching off into local market alleys.",
              details: [
                '🚝 Yui Rail from airport to Makishi — 15 mins, ¥300',
                '🛍️ Heiwa-dori and Mutsumi-dori arcades branch off Kokusai — that\'s where the real finds are',
                '🍩 Grab sata andagi (Okinawan doughnuts) from any street vendor — crispy outside, fluffy inside'
              ]
            },
            {
              title: 'Makishi Public Market (Nuchi Machi)',
              description: "The rebuilt Makishi Market is Okinawa's kitchen. The ground floor sells everything — pig faces, tropical fish, sea grapes, purple sweet potatoes. Buy seafood downstairs and have the upstairs restaurants cook it for you (¥500 cooking fee). This is the best food experience in Naha.",
              details: [
                '🐟 Point at any fish, shellfish, or lobster — they\'ll prep it upstairs',
                '🐙 Try umibudo (sea grapes) — they pop like caviar, taste like the ocean',
                '🐷 Mimiga (pig ear) is a local snack — crispy and delicious with vinegar'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Makishi Public Market (2F Restaurants)',
              description: 'Have your market-bought seafood cooked upstairs — sashimi, grilled lobster, butter-fried fish. Add a round of Orion beers and you\'ve got Okinawa\'s best first-night dinner.',
              meta: '💰 ¥2,000-4,000pp · 📍 Makishi Market 2F · Cash preferred'
            }
          ],
          tips: [
            { type: 'tip', text: 'The market closes around 8pm. Go by 5-6pm for the best selection and a relaxed cooking experience upstairs. The aunties running the restaurants are characters — enjoy the banter.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Tsuboya Pottery District Stroll',
              description: "Walk 10 minutes from Kokusai Street into a different century. Tsuboya\'s cobblestone Yachimun Street is lined with pottery studios and climbing kilns (noborigama) dating back to the 1600s. Browse shisa lion statues, sake cups, and beautiful plates — many made by Living National Treasures.",
              details: [
                '🏺 Ikutouen and Kamany are excellent shops with working studios',
                '🦁 Shisa (lion-dog guardians) make the perfect Okinawa souvenir',
                '🍵 Stop at Ucharacha for tea served in handmade Tsuboya cups'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 26.3358, lng: 127.6691, label: 'Kokusai Street', num: 1, cat: 'attraction', desc: 'Naha\'s main entertainment and shopping street' },
        { lat: 26.3340, lng: 127.6720, label: 'Makishi Public Market', num: 2, cat: 'food', desc: 'Buy seafood downstairs, cook it upstairs' },
        { lat: 26.3310, lng: 127.6740, label: 'Tsuboya Pottery District', num: 3, cat: 'attraction', desc: '300-year-old pottery village with working kilns' },
        { lat: 26.3362, lng: 127.6640, label: 'Naha Airport (Yui Rail)', num: 4, cat: 'transport', desc: 'Monorail to city center — 15 mins' }
      ]
    },
    {
      num: 2,
      date: '2026-07-16',
      neighborhoods: 'Shuri · Kinjo-cho · Naha',
      title: 'Castles, Sacred Stones & Soba',
      description: "Today you explore the soul of old Okinawa. Shuri Castle was the seat of the Ryukyu Kingdom for 450 years — destroyed and rebuilt multiple times, most recently after the devastating 2019 fire. The reconstruction is ongoing and fascinating. Then walk the ancient Kinjo Stone Path and eat the best soba on the island.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shuri Castle (首里城)',
              description: "Take the Yui Rail to Shuri Station and walk 15 minutes uphill to the castle. Even with ongoing reconstruction after the 2019 fire, Shuri Castle is magnificent — the Shureimon gate, stone walls, and gardens are intact. The castle blends Chinese, Japanese, and uniquely Ryukyuan architecture. The views over Naha are stunning.",
              details: [
                '🏯 Open 8:00am-7:30pm (summer) · Entry ¥400',
                '📸 Shureimon Gate — the iconic symbol of Okinawa, featured on the old ¥2,000 note',
                '🔨 Reconstruction is ongoing — you can watch artisans at work, which is actually fascinating',
                '🌺 The surrounding Shuri district has beautiful old stone walls draped in bougainvillea'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Go early (by 8:30am) before tour buses arrive. The morning light on the red lacquer gates is gorgeous.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kinjo-cho Stone Path (金城町石畳道)',
              description: "Just below Shuri Castle, this 300-meter cobblestone path descends through a canopy of ancient banyan trees. It's the best-preserved section of the old royal road that once connected Shuri to the southern ports. Quiet, atmospheric, and completely free.",
              details: [
                '🌳 The Great Banyan Tree of Akagi is 200+ years old',
                '🚶 Steep descent — wear good shoes. Only 10 mins but feels like time travel',
                '📸 Go slow and look for tiny shrines tucked into stone walls'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Shuri Soba',
              description: 'One of Naha\'s most beloved soba shops, housed in a traditional Okinawan red-tile home near Shuri Castle. The soki soba (spare rib noodles) here is legendary — rich pork bone broth, hand-made noodles, melt-off-the-bone ribs.',
              meta: '💰 ¥700-1,000 · 📍 Near Shuri Castle · Opens 11:30am · Cash only · Expect a line'
            },
            {
              type: '🍺 Dinner',
              name: 'Uchina Ryouri Yuunangi',
              description: 'Classic Okinawan izakaya in Naha serving all the greatest hits — goya champuru, rafute (braised pork belly), jimami tofu, and island fish. The awamori selection is excellent. A perfect group dinner.',
              meta: '💰 ¥2,500-4,000pp · 📍 Kumoji, Naha · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 26.2170, lng: 127.7195, label: 'Shuri Castle', num: 1, cat: 'attraction', desc: 'Rebuilt seat of the Ryukyu Kingdom — UNESCO World Heritage' },
        { lat: 26.2145, lng: 127.7175, label: 'Kinjo Stone Path', num: 2, cat: 'attraction', desc: 'Ancient royal road through banyan trees' },
        { lat: 26.2190, lng: 127.7190, label: 'Shuri Soba', num: 3, cat: 'food', desc: 'Legendary soba in a traditional Okinawan house' },
        { lat: 26.3345, lng: 127.6680, label: 'Yuunangi', num: 4, cat: 'food', desc: 'Beloved Okinawan izakaya — all the greatest hits' }
      ]
    },
    {
      num: 3,
      date: '2026-07-17',
      neighborhoods: 'Kerama Islands · Tokashiki / Zamami',
      title: 'Kerama Blue — Snorkeling Paradise',
      description: "Today is the adventure highlight of the trip. The Kerama Islands sit 30-40 minutes by high-speed ferry from Naha, and the water is so impossibly clear it has its own name: Kerama Blue. Sea turtles, coral gardens, and visibility up to 50 meters. This is world-class snorkeling without needing to be a diver.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'High-Speed Ferry to Zamami Island',
              description: "Catch the Queen Zamami high-speed ferry from Tomari Port in Naha (departs 9:00am or 10:00am, 50 mins). Zamami is the most popular Kerama island with stunning Furuzamami Beach — a crescent of white sand meeting impossibly clear water. Book ferry tickets in advance — summer sells out.",
              details: [
                '🚢 Queen Zamami ferry — ¥3,200 one-way, book at vill.zamami.okinawa.jp',
                '⏰ Arrive at Tomari Port 30 mins early — it\'s a small terminal',
                '🤿 Rent snorkel gear on Zamami for ~¥1,000-2,000 or bring your own',
                '🐢 Sea turtle encounters are almost guaranteed at Furuzamami Beach'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Snorkeling at Furuzamami & Ama Beach',
              description: "Furuzamami Beach has a protected coral reef right offshore — swim out 50 meters and you're surrounded by tropical fish and sea turtles. After lunch, walk or rent a bike to Ama Beach on the other side of the island for a quieter, equally beautiful swim. The water temperature in July is a perfect 28°C.",
              details: [
                '🐠 Furuzamami\'s reef starts just 30m from shore — even beginners can reach it',
                '🐢 Green sea turtles are resident — approach calmly and they\'ll swim right past you',
                '🏖️ Ama Beach is less crowded and has great sunset views',
                '🍱 Pack lunch from Naha or eat at the small restaurants near Zamami port'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Zamami Island Cafés',
              description: 'Small restaurants near the port serve simple but delicious island food — fresh fish, Okinawa soba, and curry rice. Marumiya is a local favorite.',
              meta: '💰 ¥800-1,200 · 📍 Near Zamami Port'
            },
            {
              type: '🍻 Dinner',
              name: 'Helios Pub Craft Beer House',
              description: 'Back in Naha, celebrate your ocean adventure at Helios — Okinawa\'s craft brewery. Great burgers, goya fries, and their signature Goya Dry Pale Ale. Casual and perfect for a tired, salty, happy group.',
              meta: '💰 ¥2,000-3,000pp · 📍 Makishi, Naha · Near Kokusai Street'
            }
          ],
          tips: [
            { type: 'tip', text: 'Book the ferry at least 2 weeks ahead in July — it sells out. If Zamami is full, Tokashiki Island is equally beautiful with a slightly earlier ferry (9:00am, 35 mins). Bring reef-safe sunscreen — it\'s now required in many Okinawa marine areas.' }
          ]
        }
      ],
      mapPins: [
        { lat: 26.2310, lng: 127.6780, label: 'Tomari Port', num: 1, cat: 'transport', desc: 'Ferry terminal for Kerama Islands' },
        { lat: 26.2300, lng: 127.2970, label: 'Zamami Island', num: 2, cat: 'attraction', desc: 'Kerama Islands — stunning snorkeling and sea turtles' },
        { lat: 26.2250, lng: 127.2900, label: 'Furuzamami Beach', num: 3, cat: 'attraction', desc: 'White sand beach with coral reef right offshore' },
        { lat: 26.2360, lng: 127.3020, label: 'Ama Beach', num: 4, cat: 'attraction', desc: 'Quieter beach on Zamami\'s north side' },
        { lat: 26.3355, lng: 127.6715, label: 'Helios Pub', num: 5, cat: 'food', desc: 'Okinawan craft beer house near Kokusai Street' }
      ]
    },
    {
      num: 4,
      date: '2026-07-18',
      neighborhoods: 'Southern Okinawa · Nanjo · Sefa Utaki · Nirai Kanai Bridge',
      title: 'Sacred South — Spiritual Okinawa',
      description: "Southern Okinawa is where the island gets deeply spiritual and profoundly moving. Sefa Utaki is the most sacred site in Okinawan religion — a moss-covered limestone grove where priestesses communed with the gods. Nearby, the Peace Memorial Park commemorates the Battle of Okinawa. End the day at a stunning ocean-view café.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sefa Utaki (斎場御嶽)',
              description: "UNESCO World Heritage site and the holiest place in Okinawa. This isn't a temple — it's a natural limestone forest where triangular rock formations create sacred spaces. Ryukyuan priestesses (noro) performed rituals here for centuries. The triangular rock passage framing the sea and Kudaka Island (the mythical island of creation) is one of the most powerful views in Japan.",
              details: [
                '⛩️ Open 9:00am-6:00pm · Entry ¥300',
                '🙏 This is an active sacred site — be respectful, speak quietly',
                '👟 Rocky, uneven paths — wear closed-toe shoes',
                '🏝️ Through the triangular rock, you can see Kudaka Island — where Okinawan creation mythology begins'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nirai Kanai Bridge Overlook',
              description: "A stunning S-curved bridge carved into cliffsides with panoramic Pacific Ocean views. The overlook point above the bridge is one of Okinawa's best photo spots — especially on a clear summer day when the water glows every shade of blue.",
              details: [
                '📸 The overlook is above the bridge — look for the small parking area on Route 86',
                '🌊 Clear days reveal stunning gradient blues in the water below'
              ]
            },
            {
              title: 'Okinawa Peace Memorial Park',
              description: "The Battle of Okinawa in 1945 was one of the bloodiest in the Pacific War — over 200,000 lives lost, including a third of the civilian population. The Peace Memorial Park is beautiful, solemn, and important. The Cornerstone of Peace lists every name lost, regardless of nationality.",
              details: [
                '🕊️ Free entry to the park grounds · Museum ¥300',
                '📜 The Cornerstone of Peace — 240,000+ names engraved on black granite',
                '⏰ Allow 1-2 hours — the park is large and the museum is excellent'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Café Curcuma',
              description: 'Perched on a cliff overlooking the Pacific, this Thai-Okinawan fusion café has one of the most spectacular lunch views on the island. Great curries, fresh juices, and a terrace that feels like you\'re floating above the sea.',
              meta: '💰 ¥1,200-1,800 · 📍 Chinen, Nanjo · Arrive early — long waits on weekends'
            },
            {
              type: '🍽️ Dinner',
              name: 'Steak House 88 (Kokusai Street)',
              description: 'Okinawa has a surprising steak culture from American military influence. Steak House 88 is a Naha institution — tender steaks at incredible prices. The ¥1,000 steak set is legendary value. Perfect casual group dinner.',
              meta: '💰 ¥1,000-3,000pp · 📍 Kokusai Street, Naha'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 26.1720, lng: 127.8270, label: 'Sefa Utaki', num: 1, cat: 'attraction', desc: 'UNESCO sacred site — Okinawa\'s holiest place' },
        { lat: 26.1650, lng: 127.8100, label: 'Nirai Kanai Bridge', num: 2, cat: 'attraction', desc: 'Dramatic clifftop bridge with ocean panorama' },
        { lat: 26.0900, lng: 127.7230, label: 'Peace Memorial Park', num: 3, cat: 'attraction', desc: 'WWII memorial honoring all who perished' },
        { lat: 26.1620, lng: 127.8180, label: 'Café Curcuma', num: 4, cat: 'food', desc: 'Cliff-top café with Pacific views and Thai-Okinawan fusion' },
        { lat: 26.3370, lng: 127.6690, label: 'Steak House 88', num: 5, cat: 'food', desc: 'Naha institution — ¥1,000 steak sets' }
      ]
    },
    {
      num: 5,
      date: '2026-07-19',
      neighborhoods: 'Central Okinawa · Yomitan · Chatan · American Village',
      title: 'Pottery, Beaches & American Village Sunset',
      description: "Central Okinawa is where traditional craft meets surf culture meets American influence. Start at Yomitan's pottery village — one of Japan's great ceramic destinations — then hit the beaches, and end at the vibrant American Village waterfront for sunset and shopping.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Yachimun no Sato (Yomitan Pottery Village)',
              description: "This artist collective in Yomitan village is home to dozens of potters working in traditional Okinawan styles. The climbing kilns (noborigama) fire together several times a year. Browse studios, meet artisans, and buy directly — bold fish motifs, cobalt blue glazes, and earthy Okinawan forms you won't find anywhere else in Japan.",
              details: [
                '🏺 Free to walk around — studios are open for browsing and buying',
                '🎨 Look for studios of Yonamine Shin and Matsuda Yoneshi — master potters',
                '☕ Gallery & Café Yachimun serves coffee in handmade cups you can purchase',
                '🛒 Prices are 30-50% cheaper than buying the same pieces in Naha shops'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nirai Beach & Zanpa Cape',
              description: "Nirai Beach in Yomitan is a protected natural beach with crystal water — less crowded than resort beaches. Then drive 10 minutes to Cape Zanpa, where a white lighthouse sits atop dramatic 30-meter cliffs. The coastline walk is exhilarating.",
              details: [
                '🏖️ Nirai Beach — natural, undeveloped, beautiful. Bring your own shade',
                '🗼 Zanpa Lighthouse — ¥300 to climb for 360° views',
                '🌊 The cliff formations at Cape Zanpa are dramatic — waves crash against columnar limestone'
              ]
            }
          ],
          meals: [
            {
              type: '🌮 Lunch',
              name: 'King Tacos (Kin Town)',
              description: 'The birthplace of taco rice — Okinawa\'s most famous comfort food. King Tacos has been serving mountains of seasoned beef, cheese, lettuce, and salsa over rice since 1984. The portions are absurdly generous. This is a pilgrimage.',
              meta: '💰 ¥500-800 · 📍 Kin Town (slight detour north, totally worth it) · Cash only'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Chatan American Village Sunset',
              description: "This beachside entertainment complex in Chatan is built on reclaimed US military land. It's colorful, kitschy, and genuinely fun — think a Japanese interpretation of a California boardwalk. The Sunset Beach here is the best place in central Okinawa to watch the sun drop into the East China Sea.",
              details: [
                '🎡 Ferris wheel, shops, arcades — peak group vibes',
                '🌅 Sunset Beach lives up to its name — arrive by 6:30pm in July',
                '🛍️ Great for souvenirs — Okinawan salt, awamori, shisa goods'
              ]
            }
          ],
          meals: [
            {
              type: '🍕 Dinner',
              name: 'Zhyvago Coffee Works / American Village Restaurants',
              description: 'Zhyvago is a gorgeous ocean-view coffee roastery with great food. Or explore the many restaurants in American Village — from Korean BBQ to craft burgers to izakaya. Best to wander and pick what catches your eye.',
              meta: '💰 ¥1,500-3,000pp · 📍 Chatan, American Village'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 26.3960, lng: 127.7360, label: 'Yachimun no Sato', num: 1, cat: 'attraction', desc: 'Yomitan pottery village with master craftsmen studios' },
        { lat: 26.3980, lng: 127.7150, label: 'Nirai Beach', num: 2, cat: 'attraction', desc: 'Natural protected beach with crystal clear water' },
        { lat: 26.4430, lng: 127.7130, label: 'Cape Zanpa', num: 3, cat: 'attraction', desc: 'White lighthouse on dramatic 30m sea cliffs' },
        { lat: 26.4540, lng: 127.7680, label: 'King Tacos', num: 4, cat: 'food', desc: 'Birthplace of taco rice — since 1984' },
        { lat: 26.3260, lng: 127.7630, label: 'American Village', num: 5, cat: 'attraction', desc: 'Colorful beachside entertainment complex with sunset views' },
        { lat: 26.3240, lng: 127.7600, label: 'Sunset Beach Chatan', num: 6, cat: 'attraction', desc: 'Best sunset spot in central Okinawa' }
      ]
    },
    {
      num: 6,
      date: '2026-07-20',
      neighborhoods: 'Northern Okinawa · Motobu · Churaumi · Nago',
      title: 'Whale Sharks & the Wild North',
      description: "Head north to Okinawa's crown jewel — the Churaumi Aquarium. One of the world's best, with a whale shark tank so massive it stops you in your tracks. Then explore the wild, jungle-covered northern peninsula, mangrove kayaking, and the charming town of Nago.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Churaumi Aquarium (美ら海水族館)',
              description: "This is worth the 90-minute drive north. The Kuroshio Sea tank — 7,500 cubic meters of water holding whale sharks, manta rays, and thousands of fish — is a genuine wonder. You'll stand in front of the 8.2m acrylic panel and forget how to speak. The surrounding Ocean Expo Park is free and has a beautiful beach, tropical garden, and reconstructed Okinawan village.",
              details: [
                '🐋 Open 8:30am-6:30pm (summer) · Entry ¥2,180 · Discount after 4pm: ¥1,510',
                '🦈 Feeding time at Kuroshio Sea tank: 9:30am & 3:00pm — arrive 15 mins early for a spot',
                '🏖️ Emerald Beach next door is one of Okinawa\'s most beautiful — and free',
                '🌺 Tropical Dream Center (botanical gardens) is stunning — ¥760'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Bise Fukugi Tree Road',
              description: "Just minutes from the aquarium, this 1km tunnel of 300-year-old fukugi trees in Bise village is pure magic. The trees were planted as windbreaks, creating a canopy so dense it feels like an enchanted forest. Rent a water buffalo cart or just walk slowly. Emerges at a hidden beach.",
              details: [
                '🌳 Free to walk · Water buffalo cart ~¥2,000',
                '📸 The dappled light through the canopy is gorgeous',
                '🏖️ The path ends at a quiet beach with views of Ie Island'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Lunch',
              name: 'Kishimoto Shokudo',
              description: 'Operating since 1905, this is arguably the most famous soba shop in all of Okinawa. The hand-made noodles use wood ash lye water (the traditional method). Simple, perfect, legendary. Lines are long — it\'s worth every minute.',
              meta: '💰 ¥600-900 · 📍 Motobu Town, near Churaumi · Cash only · Closed Wednesdays'
            },
            {
              type: '🍻 Dinner',
              name: 'Orion Happy Park (Nago Brewery)',
              description: 'Free brewery tour of Orion Beer — Okinawa\'s beloved local brew. Tours run every 20 mins and end with free tastings. The attached restaurant serves beer-paired Okinawan food. Great way to end a day in the north.',
              meta: '💰 Free tour + tastings · Restaurant ¥2,000-3,000pp · 📍 Nago · Reserve online'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 26.6940, lng: 127.8775, label: 'Churaumi Aquarium', num: 1, cat: 'attraction', desc: 'World-class aquarium with whale shark tank' },
        { lat: 26.6980, lng: 127.8810, label: 'Emerald Beach', num: 2, cat: 'attraction', desc: 'Beautiful free beach next to the aquarium' },
        { lat: 26.7020, lng: 127.8840, label: 'Bise Fukugi Tree Road', num: 3, cat: 'attraction', desc: '300-year-old tree tunnel to a hidden beach' },
        { lat: 26.6840, lng: 127.8930, label: 'Kishimoto Shokudo', num: 4, cat: 'food', desc: 'Okinawa\'s most famous soba — since 1905' },
        { lat: 26.5920, lng: 127.9770, label: 'Orion Happy Park', num: 5, cat: 'food', desc: 'Free Orion Beer brewery tour with tastings' }
      ]
    },
    {
      num: 7,
      date: '2026-07-21',
      neighborhoods: 'Naha · Shikinaen · Tsuboya · Kokusai Street',
      title: 'Last Day — Royal Gardens, Souvenirs & Farewell Feast',
      description: "Your final full day in Okinawa. Visit the serene Shikinaen Royal Garden — the Ryukyu king's retreat — then spend the afternoon picking up last souvenirs, revisiting favorite spots, and sitting down for a proper farewell dinner with awamori toasts and all the Okinawan dishes you love.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shikinaen Royal Garden (識名園)',
              description: "The second royal residence of the Ryukyu kings, built in 1799. This UNESCO World Heritage garden blends Chinese, Japanese, and Okinawan landscape design — a pine-fringed pond, stone bridges, a wooden royal villa, and tropical plants. It's a peaceful, uncrowded counterpoint to Shuri Castle.",
              details: [
                '🌿 Open 9:00am-5:30pm · Entry ¥400',
                '📸 The view from the hexagonal pavilion across the pond is the money shot',
                '🌺 Much less crowded than Shuri Castle — a local favorite',
                '⏰ Allow 45-60 mins'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Souvenir Shopping & Chill',
              description: "Hit Kokusai Street and the backstreet arcades for souvenirs — chinsuko cookies, Okinawan sea salt, awamori, shisa statues, beni-imo tarts (purple sweet potato). Or revisit Tsuboya for pottery. The afternoon is intentionally relaxed — you've earned it.",
              details: [
                '🍠 Beni-imo tarts from Okashigoten — the #1 Okinawa souvenir',
                '🧂 Okinawan sea salt from Gala Aoi Salt or any Kokusai shop',
                '🍶 Buy aged awamori (kusu) — 3-year minimum, 10+ year for a real treat',
                '🦁 Tsuboya pottery shisa make beautiful, meaningful souvenirs'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Okinawa Soba EIBUN',
              description: 'A modern take on Okinawa soba in a stylish Naha café. Their tsukemen (dipping noodles) Okinawa style is unique and delicious. Great for a lighter lunch on your last day.',
              meta: '💰 ¥900-1,300 · 📍 Tsuboya area, Naha'
            },
            {
              type: '🍶 Dinner',
              name: 'Ukishima Garden',
              description: 'A beautiful Okinawan house converted into a vegetable-forward restaurant — perfect for a farewell meal that celebrates Okinawa\'s longevity food culture. Island vegetables, tofu champuru, and creative dishes in a garden setting. Then walk to Tachikomi for awamori nightcaps.',
              meta: '💰 ¥2,500-4,000pp · 📍 Matsuo, Naha · Reservations recommended'
            }
          ],
          tips: [
            { type: 'tip', text: 'For a nightcap, Tachikomi Bar on Kokusai Street has 200+ varieties of awamori with knowledgeable staff who\'ll guide you through tastings. The perfect end to an Okinawa trip.' }
          ]
        }
      ],
      mapPins: [
        { lat: 26.2080, lng: 127.7150, label: 'Shikinaen Royal Garden', num: 1, cat: 'attraction', desc: 'UNESCO royal garden — serene Ryukyu retreat' },
        { lat: 26.3358, lng: 127.6691, label: 'Kokusai Street Shopping', num: 2, cat: 'attraction', desc: 'Last-day souvenirs — beni-imo tarts, salt, awamori' },
        { lat: 26.3310, lng: 127.6740, label: 'Tsuboya Pottery', num: 3, cat: 'attraction', desc: 'Handmade shisa and pottery souvenirs' },
        { lat: 26.3320, lng: 127.6730, label: 'EIBUN Soba', num: 4, cat: 'food', desc: 'Modern Okinawa soba in a stylish setting' },
        { lat: 26.3340, lng: 127.6660, label: 'Ukishima Garden', num: 5, cat: 'food', desc: 'Vegetable-forward farewell dinner in a garden house' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '¥5,000-8,000/night', midrange: '¥10,000-20,000/night', luxury: '¥25,000-60,000/night' },
    { category: 'Meals (per person)', budget: '¥2,000-3,000/day', midrange: '¥4,000-7,000/day', luxury: '¥10,000-20,000/day' },
    { category: 'Car Rental', budget: '¥4,000-6,000/day', midrange: '¥6,000-10,000/day', luxury: '¥15,000-25,000/day' },
    { category: 'Activities', budget: '¥1,000-2,000/day', midrange: '¥3,000-6,000/day', luxury: '¥10,000-20,000/day' },
    { category: 'Kerama Snorkel Trip', budget: '¥8,000pp (DIY ferry)', midrange: '¥12,000pp (guided)', luxury: '¥25,000pp (private boat)' },
    { category: '7-Day Total (per person)', budget: '¥80,000-120,000', midrange: '¥150,000-250,000', luxury: '¥350,000-600,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Naha Airport (OKA) — direct flights from Tokyo (2.5h), Osaka (2h), and many Asian cities', 'Yui Rail monorail connects the airport to Naha city center (15 mins)', 'Pick up rental car at the airport — many agencies with shuttle buses to nearby lots'] },
    { title: '🏨 Where to Stay', items: ['Naha (Days 1-3, 7): Stay near Kokusai Street — Hyatt Regency Naha, Hotel Anteroom, or Naha Central Hotel', 'Central Okinawa (Days 4-6): Consider a night in Chatan (Hilton, Vessel Hotel) for beach access', 'Budget option: Guest houses and Airbnbs are plentiful and well-run throughout Okinawa'] },
    { title: '🌡️ Weather', items: ['July averages 30-33°C (86-91°F) with 80%+ humidity', 'Rainy season ends late June — July is hot but sunny', 'Typhoon season runs July-October — check forecasts, but most pass quickly', 'UV is intense — reef-safe SPF 50+ is essential'] },
    { title: '💳 Money', items: ['Japan is increasingly cashless, but Okinawa\'s small shops often prefer cash', 'Carry ¥10,000-20,000 in cash for market stalls, soba shops, and small eateries', 'Convenience store ATMs (7-Eleven, Lawson) accept international cards', 'No tipping — it\'s not part of Japanese culture'] },
    { title: '📱 Connectivity', items: ['Buy a travel eSIM before arrival (Ubigi, Airalo) — 5-10GB for ¥1,500-3,000', 'Free WiFi at airports, convenience stores, and most hotels', 'Google Maps works great for driving navigation — set it to Japanese addresses for accuracy', 'Download Google Translate with Japanese offline pack — very useful outside Naha'] }
  ]
};

fulfillOrder(order, itineraryData);
