const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771948962559_urwshj',
  email: 'zhaoqian94@gmail.com',
  destination: 'Osaka & Kyoto, Japan',
  startDate: '2026-04-04',
  endDate: '2026-04-14',
  groupSize: 2,
  requests: 'Cultural, Foodie, Relaxation trip for couple (Terrence and Pey). Pey does NOT eat beef.'
};

const itineraryData = {
  destination: 'Osaka & Kyoto, Japan',
  countryEmoji: '🇯🇵',
  title: 'Cherry Blossoms, Street Food & Temple Magic',
  subtitle: '11 days through Osaka and Kyoto for Terrence & Pey — sakura season at its peak',
  description: "This trip is built around the two of you — Terrence\'s love of great food and Pey\'s need for beauty, culture, and zero beef. You\'ll eat your way through Osaka\'s neon-lit streets (kushikatsu, takoyaki, tonkotsu ramen), chase cherry blossoms from Osaka Castle to Arashiyama, and slow down in Kyoto\'s temple gardens. Every restaurant is chosen so Pey has excellent non-beef options and Terrence can still get his wagyu fix in Kobe. From the electric energy of Shinsekai to the stone paths of Ninenzaka at dusk — this is Japan at its most magical.",
  duration: '10 nights',
  dates: 'Apr 4 – Apr 14, 2026',
  budget: '$$–$$$',
  pace: 'Moderate',
  bestFor: 'Couples · Foodies · Culture Lovers',
  highlights: [
    'Osaka Castle cherry blossoms in full bloom',
    'Kushikatsu & takoyaki crawl through Shinsekai',
    'Kobe teppanyaki — wagyu for Terrence, lobster for Pey',
    'Fushimi Inari at sunrise with empty torii gates',
    'Arashiyama bamboo grove in the early morning mist',
    'Nishiki Market tasting tour in Kyoto',
    'Nara deer park among the cherry trees',
    'Gion at twilight — geisha district magic'
  ],

  essentials: [
    { title: '🌸 Cherry Blossom Season', text: "Early April is peak sakura in Osaka and Kyoto. Blossoms typically hit full bloom (mankai) around April 2-7 in Osaka and April 5-10 in Kyoto. You\'re arriving at the perfect time. Bring a picnic blanket for hanami under the trees." },
    { title: '🚇 Getting Around', text: "Use a Suica or ICOCA card (tap-on/tap-off) for all trains and buses. From your Osaka hotel, Shinsaibashi Station (Midosuji Line) is a 5-minute walk. In Kyoto, Gojo Station (Karasuma Line) is 5 minutes from your hotel. Get a Kansai One Pass at KIX for the IC card + tourist discounts." },
    { title: '🍽️ Dining Note for Pey', text: "Most Japanese restaurants are very accommodating. Pey — when in doubt, say 'gyū niku nashi de onegaishimasu' (牛肉なしでお願いします) which means 'without beef please.' We\'ve picked restaurants where chicken, pork, seafood, and vegetable options are abundant. Terrence — your Kobe beef moment is Day 6." },
    { title: '💴 Cash Budget', text: "Your ¥230,000 cash budget covers food, transit, and activities for 11 days. That\'s roughly ¥21,000/day for two. Breakdown: ~¥6,000-8,000/day meals, ~¥3,000-4,000/day transit, ~¥3,000-5,000/day activities. Many smaller restaurants and market stalls are cash-only. Hit a 7-Eleven ATM on arrival." }
  ],

  days: [
    {
      num: 1,
      date: '2026-04-04',
      neighborhoods: 'Kansai Airport · Shinsaibashi · Nagahori',
      title: 'Landing in Osaka — Late Night Ramen Run',
      description: "You're landing at KIX around 9pm — by the time you clear customs and ride the Nankai Rapi:t or JR Haruka into the city, it'll be late. Drop your bags at the Hearton Hotel and head straight out for a proper Osaka welcome: a steaming bowl of ramen in the neon glow of Shinsaibashi.",
      timeBlocks: [
        {
          label: 'Evening',
          activities: [
            {
              title: 'Arrive at Kansai International Airport',
              description: "Clear immigration, grab your bags, and pick up your ICOCA cards at the JR ticket office in the arrivals hall. Take the Nankai Rapi:t limited express to Namba Station (34 min, ¥1,290/person), then walk or take one stop on the Midosuji Line to Shinsaibashi.",
              details: [
                '✈️ KIX Terminal 1 arrivals → Nankai Railway platform (follow signs)',
                '💳 Get ICOCA cards at the JR West ticket counter — load ¥3,000 each to start',
                '🚃 Nankai Rapi:t to Namba: 34 min, ¥1,290. Last train ~10:30pm',
                '🏨 Namba → Shinsaibashi: 1 stop Midosuji Line or 10-min walk north'
              ]
            },
            {
              title: 'Check In: Hearton Hotel Shinsaibashi Nagahoridori',
              description: "Your home for the next 6 nights. The hotel is perfectly located — 5 minutes from Shinsaibashi Station, walking distance to Dotonbori, and surrounded by konbini and restaurants open late.",
              details: [
                '🏨 5-min walk from Shinsaibashi Station Exit 2 (Midosuji Line)',
                '🏪 FamilyMart and Lawson within 2 minutes for late-night snacks',
                '📍 Address: 1-4-10 Minamisenba, Chuo-ku, Osaka'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Late Dinner',
              name: 'Ichiran Ramen (Dotonbori)',
              description: "Perfect for a jet-lagged late arrival — Ichiran is open until 6am and serves rich tonkotsu ramen in private booths (no beef in the broth — it's pork-based). Customize your noodle firmness, richness, and garlic level on the order sheet. A warm, comforting welcome to Osaka.",
              meta: '💰 ¥1,000-1,500pp · 📍 7-18 Soemoncho, Chuo-ku · Open until 6am · 8-min walk from hotel'
            }
          ],
          tips: [
            { type: 'tip', text: "If you arrive too late for sit-down ramen, every konbini (7-Eleven, Lawson, FamilyMart) has surprisingly good onigiri, sandwiches, and hot foods. Don't sleep on konbini egg sandwiches — they're legendary." }
          ]
        }
      ],
      mapPins: [
        { lat: 34.4320, lng: 135.2441, label: 'Kansai International Airport', num: 1, cat: 'transport', desc: 'Arrival — take Nankai Rapi:t to Namba' },
        { lat: 34.6723, lng: 135.5013, label: 'Namba Station', num: 2, cat: 'transport', desc: 'Transfer point — walk north to hotel' },
        { lat: 34.6756, lng: 135.5042, label: 'Hearton Hotel Shinsaibashi', num: 3, cat: 'hotel', desc: 'Your Osaka home for 6 nights' },
        { lat: 34.6687, lng: 135.5013, label: 'Ichiran Ramen Dotonbori', num: 4, cat: 'food', desc: 'Late-night tonkotsu ramen — open until 6am' }
      ]
    },
    {
      num: 2,
      date: '2026-04-05',
      neighborhoods: 'Shinsekai · Den Den Town · Amerikamura',
      title: 'Retro Osaka — Towers, Arcades & Street Style',
      description: "Today is pure Osaka energy. Start in Shinsekai, the wonderfully retro entertainment district under Tsutenkaku Tower, where kushikatsu (deep-fried skewers) is king. Then head to Den Den Town for anime, vintage games, and electronics. End the day in Amerikamura — Osaka's Harajuku — for streetwear shopping and people-watching.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinsekai & Tsutenkaku Tower',
              description: "Take the Midosuji Line from Shinsaibashi to Dobutsuen-mae Station (2 stops, 5 min). Emerge into Shinsekai — a retro wonderland of neon signs, puffer fish lanterns, and deep-fried everything. Climb Tsutenkaku Tower for panoramic city views and rub the Billiken statue's feet for good luck.",
              details: [
                '🚇 Midosuji Line: Shinsaibashi → Dobutsuen-mae (2 stops, ¥230)',
                '🗼 Tsutenkaku Tower: ¥900/person, opens 10am',
                '📸 The neon-lit alley under the tower is incredibly photogenic',
                '🐡 The giant puffer fish signs are Shinsekai\'s signature'
              ]
            }
          ],
          meals: [
            {
              type: '🍢 Brunch',
              name: 'Kushikatsu Daruma (Shinsekai Main Branch)',
              description: "The most famous kushikatsu spot in Osaka. Deep-fried skewers of shrimp, pork, vegetables, lotus root, quail eggs — massive variety beyond beef. Pey can easily fill up on seafood and veggie skewers. Terrence, try the beef tongue. The rule: NO double-dipping in the communal sauce!",
              meta: '💰 ¥1,500-2,500pp · 📍 2-3-9 Ebisuhigashi, Naniwa-ku · 2-min walk from Tsutenkaku'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Den Den Town — Osaka\'s Electric Town',
              description: "Walk 10 minutes north from Shinsekai to Den Den Town (Nipponbashi), Osaka's answer to Akihabara. Browse retro game shops, anime figure stores, manga floors, and electronics. Super Potato for retro games, Mandarake for rare collectibles.",
              details: [
                '🎮 Super Potato: 3 floors of retro games — play vintage arcade cabinets on the top floor',
                '📚 Mandarake: rare manga, figures, and cosplay gear',
                '🕹️ Retro game carts from ¥100 — great souvenirs',
                '🚶 Walkable from Shinsekai — head north along Sakasuji'
              ]
            },
            {
              title: 'Amerikamura (American Village)',
              description: "Head back up to Shinsaibashi area and explore Amerikamura — Osaka\'s youth fashion district. Vintage shops, streetwear boutiques, record stores, and quirky cafés cluster around Triangle Park. It\'s Osaka\'s creative heartbeat.",
              details: [
                '👟 Village Vanguard, WEGO, and dozens of vintage shops',
                '🍦 Long line for the famous giant cream puffs at Pablo',
                '📍 Triangle Park — the social hub, great for people-watching',
                '🚇 Walk north from Den Den Town or Midosuji Line back to Shinsaibashi'
              ]
            }
          ],
          meals: [
            {
              type: '🐙 Snack',
              name: 'Takoyaki Wanaka (Amerikamura)',
              description: "Some of the best takoyaki (octopus balls) in Osaka. Crispy outside, molten inside, topped with special sauce and dancing bonito flakes. No beef involved — pure Osaka street food perfection.",
              meta: '💰 ¥500-700 · 📍 Amerikamura, near Triangle Park'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dotonbori Night Walk',
              description: "As the sun sets, Dotonbori comes alive. Walk along the canal and take in the iconic Glico Running Man sign, the giant crab at Kani Doraku, and the kinetic energy of thousands of people on a Saturday night. This is Osaka at its most electric.",
              details: [
                '📸 The Glico Running Man sign — get your running pose photo on the Ebisubashi Bridge',
                '🦀 Kani Doraku\'s mechanical crab is mesmerizing',
                '🌊 Walk along both sides of the Dotonbori canal'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Okonomiyaki Mizuno',
              description: "One of Osaka's most beloved okonomiyaki restaurants — expect a short wait but it's worth it. The yamaimoyaki (with mountain yam) is their signature. Pey, order the seafood mix or pork; Terrence, try the mixed deluxe. Grilled right on the teppan in front of you.",
              meta: '💰 ¥1,500-2,000pp · 📍 1-4-15 Dotonbori, Chuo-ku · Expect 20-30 min wait'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6523, lng: 135.5063, label: 'Shinsekai', num: 1, cat: 'attraction', desc: 'Retro entertainment district under Tsutenkaku Tower' },
        { lat: 34.6531, lng: 135.5058, label: 'Kushikatsu Daruma', num: 2, cat: 'food', desc: 'Osaka\'s most famous deep-fried skewers' },
        { lat: 34.6598, lng: 135.5058, label: 'Den Den Town', num: 3, cat: 'attraction', desc: 'Anime, retro games, and electronics district' },
        { lat: 34.6726, lng: 135.4977, label: 'Amerikamura', num: 4, cat: 'attraction', desc: 'Youth fashion and streetwear district' },
        { lat: 34.6686, lng: 135.5012, label: 'Dotonbori', num: 5, cat: 'attraction', desc: 'Iconic canal street — Glico sign and night food' },
        { lat: 34.6687, lng: 135.5024, label: 'Okonomiyaki Mizuno', num: 6, cat: 'food', desc: 'Top okonomiyaki — must-wait, must-eat' }
      ]
    },
    {
      num: 3,
      date: '2026-04-06',
      neighborhoods: 'Osaka Castle Park · Tenmabashi · Shinsaibashi',
      title: 'Sakura at Osaka Castle & Shinsaibashi Shopping',
      description: "Today is about cherry blossoms and retail therapy. Osaka Castle Park has over 3,000 cherry trees, and early April is prime time. Spend the morning wandering through clouds of pink petals, then head south for serious shopping along Shinsaibashi-suji, one of Osaka's longest covered shopping streets.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Osaka Castle & Nishinomaru Garden',
              description: "Take the Nagahori Tsurumi-ryokuchi Line from Nagahoribashi Station (3 min walk from hotel) to Morinomiya Station (4 stops). Enter from the east and walk through the outer moat lined with cherry trees. The Nishinomaru Garden (¥350) is the premium sakura spot — 300 cherry trees framing the castle.",
              details: [
                '🚇 Nagahori-Tsurumi Line: Nagahoribashi → Morinomiya (4 stops, ¥280)',
                '🌸 Nishinomaru Garden: ¥350 entry, opens 9am — the best sakura viewpoint',
                '🏯 Castle tower entry: ¥600 — 8 floors of history + panoramic views from the top',
                '📸 Best photo: cherry blossoms with castle from the south side of Nishinomaru'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Morning Coffee',
              name: 'Takamura Coffee Roasters',
              description: "Before heading to the castle, grab specialty coffee at this acclaimed roaster near your hotel. Single-origin pour-overs in a minimalist Japanese space.",
              meta: '💰 ¥600-900 · 📍 1-1-8 Nishi-Shinsaibashi · 7-min walk from hotel · Opens 9am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shinsaibashi-suji Shopping Arcade',
              description: "Walk from your hotel right into Shinsaibashi-suji — a 600-meter covered shopping street with everything from Uniqlo and H&M to Japanese boutiques, drug stores (stock up on Japanese skincare!), and quirky shops. Daimaru department store is at the north end for premium shopping.",
              details: [
                '🛍️ Daimaru Shinsaibashi: luxury brands + excellent depachika (basement food hall)',
                '💊 Matsumoto Kiyoshi or Daikoku Drug for Japanese skincare and beauty',
                '👗 The arcade stretches from Shinsaibashi to Namba — explore both sides',
                '🚶 Literally steps from your hotel'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "Tax-free shopping: Spend over ¥5,000 at a single store and show your passport for duty-free. Most major shops have a tax-free counter. Daimaru has a dedicated one." }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Hanami Night Walk at Osaka Castle',
              description: "Return to Osaka Castle Park in the evening for yozakura — nighttime cherry blossom viewing. The trees along the moat are illuminated, creating a magical tunnel of soft pink light reflecting in the water. Much less crowded than daytime.",
              details: [
                '🌸 Illumination typically runs until 9pm during sakura season',
                '📍 Walk along the outer moat on the south and west sides',
                '🍻 Pick up drinks and snacks from a konbini for a casual hanami'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Harukoma Sushi (Tenma)',
              description: "Take a short detour to Tenjinbashi for some of Osaka's best and most affordable sushi. Harukoma is a standing sushi bar where the fish is impeccable and the prices are shockingly low. Pey — all seafood, no beef in sight. Terrence, try the otoro.",
              meta: '💰 ¥2,000-3,500pp · 📍 5-5-2 Tenjinbashi, Kita-ku · Expect a queue — moves fast'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6873, lng: 135.5262, label: 'Osaka Castle', num: 1, cat: 'attraction', desc: '3,000+ cherry trees — peak bloom early April' },
        { lat: 34.6860, lng: 135.5230, label: 'Nishinomaru Garden', num: 2, cat: 'attraction', desc: 'Premium sakura garden with castle backdrop (¥350)' },
        { lat: 34.6751, lng: 135.5023, label: 'Shinsaibashi-suji', num: 3, cat: 'attraction', desc: '600m covered shopping arcade from hotel' },
        { lat: 34.6780, lng: 135.5035, label: 'Daimaru Shinsaibashi', num: 4, cat: 'attraction', desc: 'Department store with depachika food hall' },
        { lat: 34.7046, lng: 135.5108, label: 'Harukoma Sushi', num: 5, cat: 'food', desc: 'Standing sushi bar — incredible value, all seafood' }
      ]
    },
    {
      num: 4,
      date: '2026-04-07',
      neighborhoods: 'Nara Park · Todai-ji · Kasuga Taisha · Naramachi',
      title: 'Nara Day Trip — Deer, Giant Buddhas & Sakura',
      description: "An early start for one of the trip's most magical days. Nara's friendly deer roam freely among ancient temples and cherry trees in full bloom. You'll see the world's largest bronze Buddha at Todai-ji, walk through hundreds of stone lanterns at Kasuga Taisha, and explore the charming old merchant quarter of Naramachi.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Early Train to Nara',
              description: "Take the Kintetsu Nara Line from Osaka-Namba Station at 7:30am. The rapid express takes just 40 minutes and drops you at Kintetsu Nara Station, a short walk from the park. Early arrival means fewer crowds and calm deer.",
              details: [
                '🚃 Kintetsu Nara Line: Osaka-Namba → Kintetsu Nara (40 min, ¥680)',
                '⏰ Depart 7:30am to arrive by 8:10am — the park is peaceful before 9am',
                '🚶 Hotel to Osaka-Namba Station: 10-min walk south',
                '🦌 Buy shika senbei (deer crackers, ¥200) at park entrance — the deer know the drill'
              ]
            },
            {
              title: 'Nara Park & Todai-ji Temple',
              description: "Walk from the station through the park, bowing to deer along the way (they bow back!). Todai-ji houses a 15-meter bronze Buddha — it's genuinely awe-inspiring. The wooden hall itself is the world's largest wooden structure.",
              details: [
                '🦌 Over 1,200 free-roaming deer — they\'re sacred messengers of the gods',
                '🏛️ Todai-ji: ¥600/person · The Great Buddha Hall is staggering',
                '🌸 Cherry trees throughout Nara Park — beautiful mid-bloom',
                '📸 Deer + cherry blossoms = ultimate Japan photo'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Grab-and-Go at Kintetsu Nara Station',
              description: "Pick up fresh pastries, onigiri, or a bento box at the shops in Kintetsu Nara Station before heading to the park. The station bakery has excellent melon pan.",
              meta: '💰 ¥500-800pp · 📍 Kintetsu Nara Station ground floor'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kasuga Taisha Shrine',
              description: "Walk south through the park to Kasuga Taisha, a Shinto shrine famous for its thousands of stone lanterns draped in moss. The path through the primeval forest is otherworldly — giant cedars, filtered light, and the sound of deer crackling through leaves.",
              details: [
                '⛩️ Kasuga Taisha: free outer area, ¥500 for inner sanctuary',
                '🏮 3,000 stone and bronze lanterns — some over 800 years old',
                '🌳 The surrounding forest is a UNESCO site'
              ]
            },
            {
              title: 'Naramachi Old Town',
              description: "Head south to Naramachi, Nara's preserved merchant quarter. Narrow streets lined with Edo-period machiya houses, now home to craft shops, tea houses, and galleries. Look for the red monkey charms (migawari-zaru) hanging from the eaves.",
              details: [
                '🏘️ Free to wander — peek into open machiya houses',
                '🐒 Red monkey charms ward off bad luck',
                '🍵 Stop at a tea house for matcha and wagashi (traditional sweets)'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Kamaiki Udon',
              description: "Thick, chewy Nara-style udon in a rich dashi broth. The kama-age (served in the pot with dipping sauce) is their specialty. No beef — the broth is dashi-based. Simple, warming, and deeply satisfying.",
              meta: '💰 ¥1,000-1,500pp · 📍 Naramachi area · Cash only'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Osaka',
              description: "Catch the Kintetsu rapid express back to Namba (same route, 40 min). You'll be back in Osaka by early evening with time to rest or explore more.",
              details: [
                '🚃 Last rapid express around 9:30pm — no rush',
                '🌆 Arrive Namba → 10-min walk back to hotel'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Kinryu Ramen (Dotonbori)',
              description: "For a quick, cheap, and satisfying dinner after Nara, hit Kinryu Ramen on Dotonbori — look for the giant dragon sign. Tonkotsu pork broth, no beef. Open late, fast service, and absolutely delicious for the price.",
              meta: '💰 ¥700-1,000pp · 📍 Dotonbori, Chuo-ku · 8-min walk from hotel · Open late'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6851, lng: 135.7998, label: 'Kintetsu Nara Station', num: 1, cat: 'transport', desc: 'Arrive from Osaka-Namba in 40 min' },
        { lat: 34.6890, lng: 135.8399, label: 'Todai-ji Temple', num: 2, cat: 'attraction', desc: "World\'s largest bronze Buddha and wooden hall" },
        { lat: 34.6812, lng: 135.8498, label: 'Kasuga Taisha', num: 3, cat: 'attraction', desc: '3,000 stone lanterns in an ancient forest' },
        { lat: 34.6800, lng: 135.8300, label: 'Nara Park', num: 4, cat: 'attraction', desc: '1,200 free-roaming sacred deer' },
        { lat: 34.6755, lng: 135.8311, label: 'Naramachi', num: 5, cat: 'attraction', desc: 'Preserved Edo-period merchant quarter' },
        { lat: 34.6687, lng: 135.5013, label: 'Kinryu Ramen', num: 6, cat: 'food', desc: 'Quick tonkotsu ramen under the dragon sign' }
      ]
    },
    {
      num: 5,
      date: '2026-04-08',
      neighborhoods: 'Universal Studios Japan · Osaka Bay',
      title: 'Universal Studios Japan — Full Theme Park Day',
      description: "A full day at USJ! The Wizarding World of Harry Potter is the crown jewel, but Super Nintendo World, the new Donkey Kong Country, and the Hollywood rides are all excellent. Buy Express Passes to skip the worst lines and maximize your time.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Early Arrival at USJ',
              description: "Get there before gates open (usually 30 min before posted time). Take the JR from Nishikujo to Universal City Station. Head straight to Super Nintendo World or Wizarding World of Harry Potter — whichever has shorter initial lines.",
              details: [
                '🚃 Shinsaibashi → Namba (walk) → JR Namba → Nishikujo → Universal City (30 min total, ~¥400)',
                '🎟️ Buy tickets online in advance at usj.co.jp — ¥8,600/person for 1-Day Pass',
                '⚡ Express Pass 4 or 7 strongly recommended (¥7,800-13,800) — saves hours of waiting',
                '🕐 Arrive by 8:30am — gates often open early during cherry blossom season'
              ]
            },
            {
              title: 'Super Nintendo World & Donkey Kong Country',
              description: "Mario Kart: Koopa's Challenge uses AR goggles for an immersive ride. The new Donkey Kong Country expansion has a mine cart coaster. Collect coins, punch ? blocks, and live inside a Nintendo game. It's genuinely magical even as adults.",
              details: [
                '🍄 Get a Power-Up Band (¥4,800) to punch blocks and collect coins throughout the land',
                '🎢 Mario Kart ride uses AR — absolutely next-level',
                '🦍 Donkey Kong mine cart coaster — thrilling but not too intense'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Wizarding World of Harry Potter',
              description: "Enter through the Hogwarts gates and you're IN the movies. Explore Hogsmeade village, ride Harry Potter and the Forbidden Journey (incredible motion ride inside Hogwarts), and try frozen butterbeer. The attention to detail is astonishing.",
              details: [
                '🏰 Hogwarts Castle ride: flight simulator through the castle — top tier',
                '🍺 Frozen Butterbeer at the Three Broomsticks (¥750)',
                '🪄 Ollivanders wand experience — interactive show (10-15 min wait)',
                '📸 Hogwarts Castle at the golden hour is stunning'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Three Broomsticks (Wizarding World)',
              description: "Themed British pub food inside Hogsmeade. Fish & chips, roast chicken, shepherd's pie. Pey — the fish & chips or chicken are great options. Terrence — the ribs are solid. Butterbeer is a must.",
              meta: '💰 ¥1,500-2,500pp · 📍 Inside Wizarding World of Harry Potter'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Evening Rides & Light Show',
              description: "Hit any remaining rides — Hollywood Dream (roller coaster with music), Jurassic Park splash ride, or re-ride favorites. Stay for the evening projection show on Hogwarts Castle if running during your visit.",
              details: [
                '🎢 Hollywood Dream: The Ride — forward or BACKWARD (choose the back!)',
                '🌊 Jurassic Park: The Ride — you WILL get wet',
                '🎆 Check USJ website for evening entertainment schedule'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Yakiniku-M Namba (Post-Park)',
              description: "After USJ, head back to Namba for yakiniku. This is Terrence's treat — premium wagyu at the table grill. Pey, they have excellent seafood platters (scallops, shrimp, squid) plus pork and chicken options. A fun, interactive dinner to end a big day.",
              meta: '💰 ¥3,000-5,000pp · 📍 Namba area · 🥩 Terrence: A5 wagyu set / 🦐 Pey: seafood platter'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6656, lng: 135.4323, label: 'Universal Studios Japan', num: 1, cat: 'attraction', desc: 'Full day theme park — Harry Potter, Nintendo World' },
        { lat: 34.6656, lng: 135.4330, label: 'Super Nintendo World', num: 2, cat: 'attraction', desc: 'Mario Kart, Donkey Kong — gaming paradise' },
        { lat: 34.6650, lng: 135.4315, label: 'Wizarding World of Harry Potter', num: 3, cat: 'attraction', desc: 'Hogwarts, Hogsmeade, and frozen Butterbeer' },
        { lat: 34.6653, lng: 135.4337, label: 'Universal City Station', num: 4, cat: 'transport', desc: 'JR station — direct from Nishikujo' }
      ]
    },
    {
      num: 6,
      date: '2026-04-09',
      neighborhoods: 'Kobe · Kitano · Sannomiya · Harborland',
      title: 'Kobe Half-Day — Harbor Views & Teppanyaki Feast',
      description: "A relaxed half-day trip to Kobe — just 25 minutes from Osaka. Morning in the European-style Kitano district, waterfront stroll at Kobe Harborland, and the meal of the trip: teppanyaki dinner where Terrence gets his A5 Kobe wagyu and Pey feasts on lobster and seasonal seafood, all cooked theatrically on the iron plate right in front of you.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Train to Kobe & Kitano-cho',
              description: "Take the Hanshin Railway from Osaka-Namba to Kobe-Sannomiya (40 min, ¥420, or JR from Osaka Station 25 min, ¥420). Walk uphill to Kitano-cho, a hillside neighborhood of Western-style mansions from the Meiji era when foreign merchants settled here.",
              details: [
                '🚃 Hanshin Namba Line: Osaka-Namba → Kobe-Sannomiya (40 min, ¥420)',
                '🏠 Kitano Ijinkan (foreign houses): ¥550-750 each or combination tickets',
                '⛪ Kobe Kitano Church and Weathercock House are the most photogenic',
                '☕ Starbucks Kitano branch is inside a beautiful 1907 Western mansion'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kobe Harborland & Meriken Park',
              description: "Walk down to the waterfront for views of Kobe's modern harbor. The BE KOBE monument, Kobe Port Tower (¥700, reopened 2024), and the Maritime Museum make for a pleasant afternoon. Grab Kobe's famous cream bread at a local bakery.",
              details: [
                '📸 BE KOBE monument at Meriken Park — the Instagram spot',
                '🗼 Port Tower observation deck for harbor panorama',
                '🍞 Kobe is famous for bakeries — try Isuzu Bakery for cream pan',
                '🚶 Harborland to Sannomiya: pleasant 15-min waterfront walk'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Kobe Gyoza En (Sannomiya)',
              description: "Light lunch of Kobe-style gyoza — crispy pan-fried dumplings with pork and vegetable filling. No beef, plenty of flavor. Save room for the teppanyaki tonight!",
              meta: '💰 ¥800-1,200pp · 📍 Sannomiya area'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: '🥩 THE Meal: Kobe Teppanyaki Dinner',
              description: "This is the dinner of the trip. At a premium Kobe teppanyaki restaurant, a chef prepares your meal on a steel griddle right before your eyes. Terrence — you're getting A5 Kobe wagyu, seared to perfection, melting on contact with your tongue. Pey — the lobster and seasonal seafood course with abalone, scallops, and prawns. Both courses come with grilled vegetables, garlic rice, and miso soup.",
              details: [
                '🥩 Terrence: A5 Kobe Beef Course (~¥12,000-15,000)',
                '🦞 Pey: Seafood Teppanyaki Course (~¥10,000-13,000) — lobster, abalone, scallops',
                '👨‍🍳 The chef performance is part of the experience — watch the knife skills',
                '🍷 Add a glass of Japanese wine or Kirin draft',
                '💰 Budget: ¥22,000-28,000 total for two (this IS the splurge meal)'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Kobe Beef Steak Mouriya (Sannomiya Main Branch)',
              description: "A Kobe institution since 1885. Mouriya is one of the most respected teppanyaki restaurants in Kobe, certified to serve genuine Kobe beef. The chef grills everything to your exact preference on the iron plate. They offer separate beef and seafood courses — perfect for you two.",
              meta: '💰 ¥10,000-15,000pp · 📍 2-1-12 Shimoyamatedori, Chuo-ku, Kobe · ⚠️ Book ahead online at mouriya.co.jp'
            }
          ],
          tips: [
            { type: 'tip', text: "Book Mouriya at least 2-3 weeks ahead online. Request counter seats for the best view of the chef\'s teppan performance. Mention dietary needs when booking — they\'ll prepare Pey\'s seafood course perfectly." }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6992, lng: 135.1903, label: 'Kobe Sannomiya Station', num: 1, cat: 'transport', desc: '40 min from Osaka-Namba by Hanshin Railway' },
        { lat: 34.7022, lng: 135.1898, label: 'Kitano-cho', num: 2, cat: 'attraction', desc: 'European-style hillside mansions and cafés' },
        { lat: 34.6847, lng: 135.1893, label: 'Meriken Park', num: 3, cat: 'attraction', desc: 'BE KOBE monument and harbor views' },
        { lat: 34.6868, lng: 135.1848, label: 'Kobe Port Tower', num: 4, cat: 'attraction', desc: 'Observation deck overlooking the harbor' },
        { lat: 34.6953, lng: 135.1928, label: 'Mouriya Teppanyaki', num: 5, cat: 'food', desc: 'A5 Kobe wagyu for Terrence, lobster for Pey' }
      ]
    },
    {
      num: 7,
      date: '2026-04-10',
      neighborhoods: 'Kyoto · Nishiki Market · Teramachi · Pontocho',
      title: 'Transfer to Kyoto — Markets, Temples & River Dining',
      description: "Check out of Osaka and take the JR Special Rapid to Kyoto (30 min). Drop bags at Hotel Amanek near Gojo, then dive into Kyoto's food and shopping heart: Nishiki Market for tastings, Teramachi for souvenirs, and Pontocho alley for a magical riverside dinner.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Transfer: Osaka → Kyoto',
              description: "Check out of the Hearton Hotel. Walk to Shinsaibashi Station, take Midosuji Line to Umeda/Osaka Station (3 stops), then JR Special Rapid to Kyoto Station (30 min, ¥580). From Kyoto Station, take the Karasuma Line 2 stops to Gojo Station — your hotel is a 5-minute walk.",
              details: [
                '🚃 Midosuji Line: Shinsaibashi → Umeda (3 stops, ¥280)',
                '🚄 JR Special Rapid: Osaka → Kyoto (30 min, ¥580)',
                '🚇 Karasuma Line: Kyoto Station → Gojo (2 stops, ¥220)',
                '🏨 Hotel Amanek Kawaramachi Gojo — 5-min walk from Gojo Station Exit 1',
                '⏰ Total transit: ~50-60 min door to door'
              ]
            },
            {
              title: 'Check In: Hotel Amanek Kawaramachi Gojo',
              description: "Your Kyoto home for 4 nights. Perfectly positioned between Gion and Kyoto Station, on the Kawaramachi shopping street. The Kamo River is a 3-minute walk east — evening strolls along the river are beautiful.",
              details: [
                '📍 Near Gojo Station (Karasuma Line) — 5-min walk',
                '🏪 Konbini, restaurants, and cafés all within walking distance',
                '🌸 Kamo River walking path is right there for morning/evening strolls'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Nishiki Market Food Crawl',
              description: "A 5-block covered market street packed with over 100 food stalls and shops. Taste your way through: grilled mochi, fresh yuba (tofu skin), tamagoyaki (sweet omelet on a stick), pickles, matcha everything, and seasonal treats. This is Kyoto's kitchen.",
              details: [
                '🚶 15-min walk north from hotel along Kawaramachi-dori',
                '🦑 Must-try: grilled squid skewers, yuba cream croquette, matcha warabi mochi',
                '🍡 Aritsugu — legendary knife shop (great souvenir if you cook)',
                '📸 Go midday when all stalls are open — it gets quieter after 4pm'
              ]
            },
            {
              title: 'Teramachi & Shinkyogoku Shopping Streets',
              description: "Connected covered arcades running parallel to Nishiki. More touristy but great for souvenirs: Japanese fans, incense, ceramics, washi paper, and snack shops. Shinkyogoku has more trendy shops; Teramachi is traditional.",
              details: [
                '🎋 Japanese fans (sensu) make beautiful gifts — many hand-painted',
                '🍵 Ippodo Tea — Kyoto\'s finest matcha and hojicha since 1717',
                '🛍️ Connected directly to the south end of Nishiki Market'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Nishiki Market Grazing',
              description: "Don't sit down — just graze your way through the market. Budget ¥2,000-3,000 between the two of you for multiple tastings: tamagoyaki (¥200), grilled mochi (¥300), yuba croquette (¥350), octopus skewer (¥500), matcha soft serve (¥400).",
              meta: '💰 ¥2,000-3,000 for two · 📍 Nishiki Market · Cash recommended for stalls'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Pontocho Alley',
              description: "As the lanterns flicker on along Pontocho, one of Kyoto's most atmospheric dining alleys, find your dinner spot. This narrow stone lane runs parallel to the Kamo River, packed with tiny restaurants — many with riverside patios (kawadoko) in warmer months.",
              details: [
                '🏮 Pontocho is just north of Gojo — 10-min walk from hotel along the river',
                '🌸 Early April — some restaurants may have started kawadoko (riverside platforms)',
                '📸 The alley itself is incredibly photogenic — especially at dusk'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Hafuu (Pontocho)',
              description: "A refined Pontocho restaurant specializing in Kyoto-style cuisine with excellent chicken and seafood options. Pey can enjoy seasonal fish and tofu dishes; Terrence, their duck or chicken courses are excellent. The intimate setting overlooking the Kamo River makes it feel quintessentially Kyoto.",
              meta: '💰 ¥4,000-6,000pp · 📍 Pontocho alley · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9981, lng: 135.7592, label: 'Gojo Station', num: 1, cat: 'transport', desc: 'Karasuma Line — nearest to hotel' },
        { lat: 34.9975, lng: 135.7632, label: 'Hotel Amanek Kawaramachi Gojo', num: 2, cat: 'hotel', desc: 'Your Kyoto home for 4 nights' },
        { lat: 35.0050, lng: 135.7650, label: 'Nishiki Market', num: 3, cat: 'food', desc: "Kyoto\'s kitchen — 100+ food stalls and shops" },
        { lat: 35.0060, lng: 135.7680, label: 'Teramachi Shopping Street', num: 4, cat: 'attraction', desc: 'Souvenirs, fans, incense, and washi paper' },
        { lat: 35.0040, lng: 135.7705, label: 'Pontocho Alley', num: 5, cat: 'food', desc: 'Atmospheric lantern-lit dining alley by the Kamo River' }
      ]
    },
    {
      num: 8,
      date: '2026-04-11',
      neighborhoods: 'Fushimi Inari · Uji',
      title: 'Sunrise Torii Gates & Uji Tea Country',
      description: "The early bird gets the empty torii gates. Arrive at Fushimi Inari by 7am to walk through thousands of vermillion gates in near-solitude. Then hop a train south to Uji — the birthplace of Japanese green tea — for temple visits, matcha tastings, and a peaceful riverside afternoon.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Fushimi Inari Taisha at Sunrise',
              description: "Take the JR Nara Line from Tofukuji Station (one stop from your area) to Inari Station. The shrine is open 24/7 and free. At 7am, the thousands of vermillion torii gates are nearly empty — you'll have those iconic tunnel shots to yourselves. Walk at least to the Yotsutsuji intersection (45 min up) for stunning city views.",
              details: [
                '🚃 Walk to Gojo-Kawaramachi bus stop → Bus 202 to Tofukuji → JR to Inari (20 min total)',
                '⛩️ Free entry, open 24/7 — 7am arrival is ideal',
                '🥾 Full summit hike: 2-3 hours round trip. Yotsutsuji halfway point: 45 min up',
                '📸 The torii tunnel photos are best between the first and second gates — fewer people, better light',
                '🦊 Fox statues everywhere — Inari is the god of rice and prosperity'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Train to Uji',
              description: "From Inari, continue south on the JR Nara Line to Uji Station (17 min, ¥250). Uji is a peaceful riverside town famous as the birthplace of Japanese green tea and home to the stunning Byodo-in Temple (the one on the ¥10 coin!).",
              details: [
                '🚃 JR Nara Line: Inari → Uji (17 min, ¥250)',
                '🍵 Uji has been growing tea since the 1200s',
                '💴 Byodo-in is on the ¥10 coin — check your change!'
              ]
            },
            {
              title: 'Byodo-in Temple & Tea District',
              description: "Walk along the Uji River to Byodo-in, a UNESCO World Heritage Site. The Phoenix Hall seems to float on its reflection pond. Then explore the tea shops along Byodo-in Omotesando — the street of matcha everything.",
              details: [
                '🏛️ Byodo-in: ¥700/person · Phoenix Hall interior tours run every 20 min (separate ¥300)',
                '🍵 Nakamura Tokichi — historic tea house, try their matcha parfait or matcha soba',
                '🌸 Cherry trees line the Uji River — beautiful in early April',
                '🛍️ Buy premium matcha to take home — Uji matcha is the gold standard'
              ]
            }
          ],
          meals: [
            {
              type: '🍵 Lunch',
              name: 'Nakamura Tokichi (Uji Main Branch)',
              description: "Tea house since 1854. Their matcha parfait is legendary, but for lunch try the matcha soba set — buckwheat noodles with a matcha dipping sauce, plus seasonal sides. Pey and Terrence — entirely beef-free menu focused on tea-infused cuisine.",
              meta: '💰 ¥1,500-2,500pp · 📍 Uji-Ichiban, Uji · Expect 20-30 min wait'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Kyoto & Kamo River Walk',
              description: "Train back to Kyoto and spend a relaxed evening walking along the Kamo River near your hotel. The cherry trees along the riverbanks may still be in bloom, and the river path is magical at dusk with couples picnicking on the stone banks.",
              details: [
                '🚃 JR Uji → Kyoto Station → Gojo (30 min total)',
                '🌸 Kamo River cherry blossoms between Gojo and Shijo bridges',
                '🌆 The river is beautiful at golden hour'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Omen Kodaiji (Udon)',
              description: "One of Kyoto's most famous udon restaurants. Their signature is cold udon with a sesame dipping sauce and a plate of fresh vegetables — seasonal, light, and entirely beef-free. The atmosphere is warm, woody, and very Kyoto.",
              meta: '💰 ¥1,500-2,000pp · 📍 Kodaiji area, 15-min walk from hotel · Closes 9pm'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari Taisha', num: 1, cat: 'attraction', desc: '10,000 vermillion torii gates — arrive 7am for solitude' },
        { lat: 34.8890, lng: 135.8077, label: 'Byodo-in Temple', num: 2, cat: 'attraction', desc: 'UNESCO Phoenix Hall — the ¥10 coin temple' },
        { lat: 34.8900, lng: 135.8060, label: 'Nakamura Tokichi', num: 3, cat: 'food', desc: 'Historic tea house — matcha soba and parfaits since 1854' },
        { lat: 34.8912, lng: 135.8050, label: 'Uji Tea District', num: 4, cat: 'attraction', desc: 'Birthplace of Japanese green tea — shops and tastings' },
        { lat: 35.0010, lng: 135.7700, label: 'Kamo River (Gojo area)', num: 5, cat: 'attraction', desc: 'Evening cherry blossom walk along the riverbank' }
      ]
    },
    {
      num: 9,
      date: '2026-04-12',
      neighborhoods: 'Arashiyama · Sagano · Tenryu-ji',
      title: 'Arashiyama — Bamboo, Monkeys & River Beauty',
      description: "An early morning in Arashiyama to experience the bamboo grove before the crowds arrive. The towering green stalks swaying overhead feel like another planet. Add Tenryu-ji's stunning garden, the Monkey Park overlooking all of Kyoto, and the iconic Togetsukyo Bridge framed by cherry blossoms.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Arashiyama Bamboo Grove at Dawn',
              description: "Arrive early — by 7:30-8am the bamboo grove is peaceful and empty. Take Bus 28 from Gojo to Arashiyama (30 min) or the JR Sagano Line from Kyoto Station. Walk north from Togetsukyo Bridge through the bamboo path. The filtered green light through thousands of towering stalks is breathtaking.",
              details: [
                '🚌 Bus 28: Gojo-Kawaramachi → Arashiyama (30 min, ¥230)',
                '🎋 The grove is free and open 24/7 — early morning = no crowds',
                '📸 The best photos are in the main path between Tenryu-ji north gate and Okochi Sanso',
                '🌿 Walk slowly — listen to the wind through the bamboo'
              ]
            },
            {
              title: 'Tenryu-ji Temple & Garden',
              description: "One of Kyoto's five great Zen temples. The Sogenchi Garden, with its borrowed scenery of the Arashiyama mountains, is a masterpiece of Japanese garden design. Cherry blossoms frame the pond in April.",
              details: [
                '🏛️ Garden entry: ¥500/person · Inside temple additional ¥300',
                '🌸 Cherry blossoms + mountain backdrop + mirror pond = perfection',
                '⏰ Opens 8:30am — enter from the bamboo grove side'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: '% Arabica Arashiyama',
              description: "Iconic minimalist coffee shop right on the Katsura River. World-class latte with one of the best views in Kyoto — the Togetsukyo Bridge and mountains reflected in the water. Get here before the line builds.",
              meta: '💰 ¥500-700 · 📍 3-47 Sagatenryuji Susukinobabacho · Opens 8am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Iwatayama Monkey Park',
              description: "Cross Togetsukyo Bridge and climb 15 minutes up to the monkey park. 120 wild Japanese macaques roam freely on the mountaintop while you get panoramic views of Kyoto stretching to the horizon. You can feed them from inside a cage (yes, you're in the cage).",
              details: [
                '🐒 Entry: ¥550/person · Open 9am-4:30pm',
                '🥾 15-min uphill walk from the base — moderate effort',
                '📸 The view from the top is one of Kyoto\'s best-kept secrets',
                '🍎 Buy apple slices (¥100) to feed monkeys through the cage fence'
              ]
            },
            {
              title: 'Togetsukyo Bridge & River Walk',
              description: "The iconic bridge with mountains rising behind it is one of Kyoto's most photographed scenes — even more stunning during cherry blossom season. Rent a boat (¥1,500 for 30 min) for a peaceful float on the Katsura River.",
              details: [
                '🌸 Cherry trees line both banks of the river',
                '🚣 Rowboat rental near the bridge — romantic on the water',
                '📸 Best bridge photos from the south bank'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Yudofu Sagano (Tofu Restaurant)',
              description: "Arashiyama is famous for yudofu — silky tofu simmered in kombu broth. This traditional restaurant serves a multi-course tofu meal in a garden setting. Entirely plant-based, incredibly delicate, and deeply Kyoto. Pey will love this.",
              meta: '💰 ¥2,500-3,500pp · 📍 Sagano area, near bamboo grove · Lunch only'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Kyoto — Relaxed Evening',
              description: "Head back to the hotel by mid-afternoon. Spend the evening at a sento (public bath) to soak tired legs, or browse the shops along Kawaramachi-dori near your hotel. A relaxed evening before the last two big days.",
              details: [
                '🚌 Bus 28 back to Gojo (30 min)',
                '♨️ Goko-yu Sento near Gojo — traditional public bath (¥490)',
                '🛍️ Kawaramachi-dori has great evening window shopping'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Gion Kappa Restaurant',
              description: "Casual and charming izakaya near Gion. Great variety: yakitori skewers, grilled fish, tempura, edamame, Japanese pickles. Perfect for a relaxed dinner where both of you can order freely — extensive non-beef menu. Terrence, try the chicken nanban.",
              meta: '💰 ¥2,500-4,000pp · 📍 Near Gion, 15-min walk from hotel'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0173, lng: 135.6716, label: 'Arashiyama Bamboo Grove', num: 1, cat: 'attraction', desc: 'Towering bamboo forest — arrive before 8am' },
        { lat: 35.0154, lng: 135.6745, label: 'Tenryu-ji Temple', num: 2, cat: 'attraction', desc: 'Zen temple with one of Japan\'s finest gardens' },
        { lat: 35.0135, lng: 135.6764, label: '% Arabica Arashiyama', num: 3, cat: 'food', desc: 'Iconic coffee shop overlooking Togetsukyo Bridge' },
        { lat: 35.0096, lng: 135.6771, label: 'Iwatayama Monkey Park', num: 4, cat: 'attraction', desc: 'Wild macaques with panoramic Kyoto views' },
        { lat: 35.0115, lng: 135.6780, label: 'Togetsukyo Bridge', num: 5, cat: 'attraction', desc: 'Iconic bridge with mountain and cherry blossom views' }
      ]
    },
    {
      num: 10,
      date: '2026-04-13',
      neighborhoods: 'Higashiyama · Kiyomizu-dera · Gion',
      title: 'Temple Trails & Gion at Twilight',
      description: "Your last full day is Kyoto at its most beautiful. Start with the iconic Kiyomizu-dera veranda overlooking a sea of cherry blossoms, wind down the stone-paved lanes of Sannenzaka and Ninenzaka, then spend the golden hours in Gion — Kyoto's geisha district — where you might spot a maiko gliding between teahouses.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kiyomizu-dera Temple',
              description: "Walk east from your hotel (20 min uphill, or bus 207 to Kiyomizu-michi). Kiyomizu-dera\'s massive wooden stage juts out over a hillside of cherry and maple trees — in April, it\'s a sea of pink and green. The view from the stage is one of Japan\'s most iconic.",
              details: [
                '🚶 Walk from hotel: 20 min east and uphill through Gojo-zaka',
                '🏛️ Entry: ¥400/person · Opens 6am (go early!)',
                '🌸 The cherry trees below the main stage are peak bloom in early April',
                '💧 Otowa Waterfall: drink from one of three streams for love, success, or longevity',
                '📸 The classic photo: main hall with cherry blossoms from the viewing platform'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Sannenzaka & Ninenzaka',
              description: "Descend from Kiyomizu-dera along these beautiful preserved stone-paved lanes. Lined with traditional wooden shops, tea houses, and craft stores, they feel like stepping back 200 years. Browse ceramics, pick up incense, try yatsuhashi (cinnamon rice cake sweets).",
              details: [
                '🏘️ Sannenzaka (three-year slope) → Ninenzaka (two-year slope)',
                '🍡 Yatsuhashi sweets — Kyoto\'s signature souvenir',
                '📸 Early morning or late afternoon for fewer people',
                '☕ % Arabica Kyoto Higashiyama — another branch, shorter line than Arashiyama'
              ]
            },
            {
              title: 'Yasaka Pagoda & Hokan-ji',
              description: "The five-story pagoda visible from Ninenzaka is one of Kyoto's most photographed scenes. Walk around it, find the classic angle with the stone steps leading up, and continue north toward Yasaka Shrine.",
              details: [
                '📸 The pagoda framed by traditional houses and cherry blossoms — THE Kyoto shot',
                '⛩️ Yasaka Shrine at the end of Shijo-dori — marks the entrance to Gion'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Junsei (Yudofu near Nanzen-ji)',
              description: "Another beautiful yudofu experience — this one in a stunning garden setting near the Nanzen-ji Temple area. Multi-course tofu kaiseki: yuba sashimi, agedashi tofu, sesame tofu, and silky yudofu. Completely beef-free and deeply elegant.",
              meta: '💰 ¥3,000-4,500pp · 📍 Nanzen-ji area · Slight detour north but very worth it'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Gion at Twilight',
              description: "As the light turns golden, wander through Gion — Kyoto's famous geisha (geiko) and apprentice (maiko) district. Walk along Hanamikoji Street, the stone-paved main avenue lined with ochaya (teahouses). If you're lucky, you might spot a maiko hurrying to an evening engagement in her full regalia.",
              details: [
                '🏮 Hanamikoji Street — the heart of Gion, wooden machiya and stone paths',
                '👘 Best time to spot maiko: around 5:30-6:30pm as they head to engagements',
                '📸 Please be respectful — do not block, chase, or touch geiko/maiko',
                '🌸 Shirakawa Canal — willow trees and cherry blossoms over the narrow waterway'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Gion Owatari',
              description: "A special kaiseki dinner for your last evening in Japan. Gion Owatari serves refined Kyoto cuisine in an intimate machiya setting. Multi-course seasonal menu featuring fish, tofu, seasonal vegetables, and delicate preparations. Entirely beef-free. A beautiful way to say goodbye to Kyoto.",
              meta: '💰 ¥6,000-10,000pp · 📍 Gion area · Reservations essential'
            }
          ],
          tips: [
            { type: 'tip', text: "After dinner, walk along the Shirakawa Canal in Gion — the cherry blossoms, willow trees, and stone bridges lit by soft lanterns are pure magic. One of the most romantic spots in all of Japan." }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9949, lng: 135.7850, label: 'Kiyomizu-dera', num: 1, cat: 'attraction', desc: 'Iconic wooden stage over cherry blossom valley' },
        { lat: 34.9976, lng: 135.7803, label: 'Sannenzaka & Ninenzaka', num: 2, cat: 'attraction', desc: 'Preserved stone-paved lanes with traditional shops' },
        { lat: 34.9983, lng: 135.7811, label: 'Yasaka Pagoda', num: 3, cat: 'attraction', desc: 'Five-story pagoda — THE Kyoto photo' },
        { lat: 35.0036, lng: 135.7786, label: 'Gion (Hanamikoji)', num: 4, cat: 'attraction', desc: 'Geisha district — machiya teahouses and stone paths' },
        { lat: 35.0040, lng: 135.7758, label: 'Shirakawa Canal', num: 5, cat: 'attraction', desc: 'Willows, cherry blossoms, and lantern-lit bridges' },
        { lat: 35.0030, lng: 135.7790, label: 'Gion Owatari', num: 6, cat: 'food', desc: 'Farewell kaiseki dinner in a Gion machiya' }
      ]
    },
    {
      num: 11,
      date: '2026-04-14',
      neighborhoods: 'Kyoto Station · Departure',
      title: 'Sayonara — Last Shopping & Haruka to KIX',
      description: "Your last morning in Japan. Pack up, check out, and head to Kyoto Station for final souvenir shopping in the massive station complex. Grab an ekiben (train bento) and catch the Haruka Express to Kansai Airport. Sayonara, Japan. You'll be back.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Check Out & Head to Kyoto Station',
              description: "Check out of Hotel Amanek and take the Karasuma Line from Gojo to Kyoto Station (2 stops, 4 min). The station complex is massive — use the morning to explore The Cube and Porta underground malls for last-minute shopping.",
              details: [
                '🚇 Karasuma Line: Gojo → Kyoto Station (2 stops, ¥220)',
                '🧳 Leave luggage in station coin lockers (¥500-700) while you shop',
                '🕐 Aim to finish shopping by 12:30pm for a 1:00pm Haruka'
              ]
            },
            {
              title: 'Kyoto Station Shopping',
              description: "The Cube (basement mall) and Porta (underground shopping street) have everything: matcha sweets, yatsuhashi, Japanese ceramics, Kyoto cosmetics, and snacks. The 10th floor has a restaurant street with views of Kyoto Tower. Isetan department store is also connected.",
              details: [
                '🍵 Tsujiri or Malebranche for premium matcha sweets to take home',
                '🎁 Yatsuhashi varieties (cinnamon rice cakes) — Kyoto\'s #1 souvenir',
                '🍱 Grab an ekiben (train bento box) for the Haruka ride — the station has dozens of options',
                '📸 Kyoto Tower is visible from the station — last photo op'
              ]
            }
          ],
          meals: [
            {
              type: '🍱 Lunch',
              name: 'Ekiben from Kyoto Station',
              description: "A proper Japanese send-off: pick up a beautiful ekiben (train bento box) from the ground floor shops. The seasonal Kyoto-style bento with pickled vegetables, grilled fish, and rice is the perfect last meal. Eat it on the Haruka Express as Japan rushes past the window.",
              meta: '💰 ¥1,000-1,500pp · 📍 Kyoto Station ground floor · Buy before boarding'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Haruka Express to Kansai Airport',
              description: "Board the JR Haruka Limited Express from Kyoto Station to Kansai Airport. The train takes 75 minutes and runs every 30 minutes. Book reserved seats for guaranteed comfort with your luggage. Aim for the 1:00pm or 1:30pm departure depending on your flight time.",
              details: [
                '🚄 JR Haruka: Kyoto → KIX (75 min, ¥3,640 reserved seat)',
                '⏰ Board by 1:30pm for comfortable check-in time',
                '💳 Use your ICOCA card + Haruka discount ticket if available',
                '✈️ Arrive KIX 2:45pm → plenty of time for international departure'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "Terrence and Pey — use any remaining yen at Kyoto Station or the KIX duty-free. Don't exchange coins back (most places won't take them). Spend them on snacks, vending machine drinks, or gacha capsule machines at the station. 🎰" }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9858, lng: 135.7588, label: 'Kyoto Station', num: 1, cat: 'transport', desc: 'Shopping complex + Haruka Express departure' },
        { lat: 34.9870, lng: 135.7590, label: 'The Cube / Porta Mall', num: 2, cat: 'attraction', desc: 'Underground shopping — souvenirs and matcha sweets' },
        { lat: 34.4320, lng: 135.2441, label: 'Kansai International Airport', num: 3, cat: 'transport', desc: '75 min on Haruka Express — sayonara Japan!' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: 'Pre-booked', midrange: 'Pre-booked', luxury: 'Pre-booked' },
    { category: 'Meals (per couple/day)', budget: '¥4,000-6,000', midrange: '¥6,000-10,000', luxury: '¥10,000-20,000' },
    { category: 'Transit (per couple/day)', budget: '¥1,500-2,500', midrange: '¥2,500-4,000', luxury: '¥4,000+ (taxi)' },
    { category: 'Activities (per couple/day)', budget: '¥1,000-2,000', midrange: '¥2,000-5,000', luxury: '¥5,000-10,000' },
    { category: 'USJ (Day 5, per couple)', budget: '¥17,200 (tickets)', midrange: '¥33,000 (+ Express)', luxury: '¥45,000 (+ Express 7)' },
    { category: 'Kobe Teppanyaki (Day 6)', budget: '—', midrange: '¥22,000-28,000', luxury: '¥35,000-50,000' },
    { category: '11-Day Total (couple)', budget: '¥130,000-160,000', midrange: '¥180,000-230,000', luxury: '¥300,000-400,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Kansai International Airport (KIX) serves Osaka, Kyoto, and Kobe', 'Nankai Rapi:t to Namba: 34 min, ¥1,290', 'JR Haruka Express to Shin-Osaka/Kyoto: 50-75 min', 'Get ICOCA cards at the JR counter in arrivals'] },
    { title: '🏨 Your Hotels', items: ['Apr 4-10: Hearton Hotel Shinsaibashi Nagahoridori (Osaka) — 5 min from Shinsaibashi Stn', 'Apr 10-14: Hotel Amanek Kawaramachi Gojo (Kyoto) — 5 min from Gojo Stn', 'Both are centrally located with easy transit access'] },
    { title: '🌡️ April Weather', items: ['Osaka/Kyoto average: 12-20°C (54-68°F)', 'Cherry blossom peak: early to mid April', 'Occasional rain — pack a compact umbrella', 'Layers recommended: warm days, cool evenings'] },
    { title: '💴 Money & Budget', items: ['¥230,000 cash budget for food/transit/activities over 11 days', 'Many small restaurants and market stalls are cash-only', '7-Eleven and JP Post ATMs accept international cards', 'IC card (ICOCA/Suica) for all transit — load ¥3,000 to start, top up as needed'] },
    { title: '📱 Connectivity', items: ['Buy an eSIM before departure or pocket WiFi at KIX', 'Google Maps works perfectly in Japan for train routes', 'Download Google Translate with Japanese offline pack', 'Most konbini and stations have free WiFi'] },
    { title: '🍽️ Pey\'s Dining Guide', items: ["Say: 'Gyū niku nashi de onegaishimasu' (without beef please)", 'Japanese cuisine naturally emphasizes seafood, chicken, pork, and tofu', 'Ramen broths are typically pork (tonkotsu) or chicken (tori) based', 'Every restaurant in this itinerary has been chosen with beef-free options'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
