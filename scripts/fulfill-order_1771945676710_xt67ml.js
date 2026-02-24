const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771945676710_xt67ml',
  email: 'zhaoqian94@gmail.com',
  destination: 'Osaka and Kyoto, Japan',
  startDate: '2026-04-04',
  endDate: '2026-04-14',
  groupSize: 2,
  requests: 'Base in Osaka 5 nights then Kyoto. USJ Apr 8, Nara day trip Apr 7, Uji day trip, Kobe day trip. Weekends casual/exploratory. Partner cannot eat beef.'
};

const itineraryData = {
  destination: 'Osaka & Kyoto, Japan',
  countryEmoji: '🇯🇵',
  title: 'Cherry Blossom Romance: Osaka & Kyoto',
  subtitle: '11 days of sakura, street food, temples & neighborhood wandering for two',
  description: "April in Kansai is pure magic — cherry blossoms canopy every canal, castle, and shrine in soft pink. This itinerary splits between Osaka's electric food scene and Kyoto's timeless beauty, weaving in day trips to Nara's deer-filled parks, Uji's matcha temples, and Kobe's harbour. Weekends stay casual with neighborhood exploration, food tours, and romantic evening strolls through lantern-lit alleyways. Every meal is chosen with care — no beef, all delicious.",
  duration: '10 nights',
  dates: 'Apr 4 – Apr 14, 2026',
  budget: '$$–$$$',
  pace: 'Relaxed',
  bestFor: 'Couples · Foodies · Culture Lovers',
  highlights: [
    'Cherry blossoms at Osaka Castle and along the Kema Sakuranomiya riverbank',
    'Nara day trip — deer, ancient temples & sakura in Nara Park',
    'Universal Studios Japan on a weekday',
    'Hozenji Yokocho evening stroll with yakitori & sake',
    'Fushimi Inari at sunrise — thousands of vermillion torii gates',
    'Uji day trip — matcha everything at the birthplace of Japanese tea',
    'Arashiyama bamboo grove & riverside cherry blossoms',
    'Kobe harbour sunset & world-class seafood dinner'
  ],

  essentials: [
    { title: '🌸 Cherry Blossom Season', text: 'Early April is peak sakura in Osaka and Kyoto. Expect full bloom around April 3-8 for Somei-Yoshino varieties, with late-blooming yaezakura lasting through mid-April. Pack layers — temps range 10-20°C with occasional rain.' },
    { title: '🚇 Getting Around', text: 'Use an IC card (ICOCA) for trains, subways, and buses across Kansai. Kintetsu and JR lines connect Osaka, Kyoto, Nara, and Kobe. The Hankyu line is great for Osaka-Kyoto. Buy day passes for heavy travel days.' },
    { title: '🍜 No-Beef Dining', text: "This itinerary avoids beef entirely. Kansai is paradise for non-beef eaters: yakitori (chicken), takoyaki (octopus), seafood izakaya, tofu kaiseki, ramen (pork/chicken broth), okonomiyaki (pork or seafood), and incredible sushi. Just say 'gyūniku nashi de' (no beef) when ordering." },
    { title: '💑 Weekend Strategy', text: 'Per your request, weekends avoid crowded temples and parks. Instead: neighborhood walks, shopping arcades, food tours, and romantic evening strolls. Weekday mornings are best for major sights.' }
  ],

  days: [
    // ===== DAY 1: Saturday April 4 — Arrival in Osaka (Weekend: casual) =====
    {
      num: 1,
      date: '2026-04-04',
      neighborhoods: 'Namba · Shinsaibashi · Dotonbori',
      title: 'Arrive in Osaka — Neon Lights & Street Food',
      description: "Land in Osaka and dive straight into the city's electric food scene. Saturday evening is perfect for exploring Dotonbori's neon-lit canals and grazing on takoyaki, kushikatsu, and gyoza without any agenda.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In & Shinsaibashi Stroll',
              description: "Settle into your hotel near Namba and wander the covered Shinsaibashi-suji shopping arcade. It stretches 600 meters and is perfect for first impressions — fashion boutiques, drugstores, and snack shops line both sides.",
              details: [
                '🏨 Stay near Namba or Shinsaibashi for walkable access to everything',
                '🛍️ Shinsaibashi-suji arcade — covered, so great rain or shine',
                '📸 The Glico Running Man sign marks the heart of Dotonbori'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "If arriving from KIX, take the Nankai Rapi:t express to Namba (34 min, ¥1,450). It's a beautiful retro-futuristic train." }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dotonbori Street Food Crawl',
              description: "Osaka is Japan's kitchen, and Dotonbori is the heart of it. Walk along the canal and graze: takoyaki from Wanaka, kushikatsu (deep-fried skewers) from Daruma, and finish with a creamy gyoza from Chao Chao. No reservations needed — just follow the crowds and your nose.",
              details: [
                '🐙 Takoyaki Wanaka — crispy outside, molten octopus inside',
                '🍢 Kushikatsu Daruma — the original since 1929 (pork, shrimp, veggie options)',
                '🥟 Chao Chao Gyoza — juicy pork & shrimp dumplings'
              ]
            }
          ],
          meals: [
            {
              type: '🍻 Dinner',
              name: 'Dotonbori Street Food Crawl',
              description: 'Graze your way through Osaka\'s most famous food street — takoyaki, kushikatsu, gyoza, and more. No beef needed when the seafood and pork options are this good.',
              meta: '💰 $ · 📍 Dotonbori Canal area · No reservations needed'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6687, lng: 135.5013, label: 'Dotonbori', num: 1, cat: 'attraction', desc: 'Neon-lit canal street — Osaka\'s iconic food district' },
        { lat: 34.6722, lng: 135.5010, label: 'Shinsaibashi-suji', num: 2, cat: 'attraction', desc: '600m covered shopping arcade' },
        { lat: 34.6686, lng: 135.5027, label: 'Takoyaki Wanaka', num: 3, cat: 'food', desc: 'Legendary takoyaki stand on Dotonbori' },
        { lat: 34.6684, lng: 135.5030, label: 'Kushikatsu Daruma', num: 4, cat: 'food', desc: 'Original kushikatsu since 1929 — no double dipping!' },
        { lat: 34.6693, lng: 135.5023, label: 'Glico Running Man Sign', num: 5, cat: 'attraction', desc: 'Osaka\'s most photographed landmark' }
      ]
    },

    // ===== DAY 2: Sunday April 5 — Weekend: Casual Exploration =====
    {
      num: 2,
      date: '2026-04-05',
      neighborhoods: 'Shinsekai · Tennoji · Amerikamura',
      title: 'Sunday Slow — Retro Neighborhoods & Hidden Gems',
      description: "Sunday is for wandering. Skip the temples and explore Osaka's retro Shinsekai district with its Tsutenkaku Tower, then hop to Amerikamura for vintage shopping and café culture. Evening: a romantic stroll through the lantern-lit Hozenji Yokocho alley.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinsekai Neighborhood Walk',
              description: "Shinsekai ('New World') is Osaka's retro wonderland — built in 1912 as a futuristic district, it now has a nostalgic, slightly gritty charm. Tsutenkaku Tower rises above streets lined with colorful kushikatsu shops, game arcades, and friendly locals.",
              details: [
                '🗼 Tsutenkaku Tower — climb for 360° city views (¥900)',
                '🎮 Jan Jan Yokocho alley — old-school game arcades and shogi parlors',
                '🍢 Kushikatsu heaven — try Yaekatsu for shrimp and vegetable skewers'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Tennoji Cha Cha',
              description: 'Cozy café near Tennoji Park serving thick Japanese-style pancakes and excellent pour-over coffee. A calm start to a lazy Sunday.',
              meta: '💰 $ · 📍 Near Tennoji Station'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Amerikamura (American Village)',
              description: "Osaka's youth culture hub — think vintage clothing shops, street art, indie record stores, and trendy cafés. Much less crowded on a Sunday afternoon than Dotonbori. Great for picking up unique souvenirs.",
              details: [
                '👕 Big Step mall — vintage shops and indie boutiques',
                '🍦 Long Softcream — famous for 40cm-tall soft serve',
                '🎨 Street art around Triangle Park'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Hozenji Yokocho Evening Stroll',
              description: "This tiny stone-paved alley near Dotonbori is pure old Osaka romance. Lanterns glow, water drips over the moss-covered Hozenji temple statue, and intimate restaurants line both sides. Splash water on the Fudo Myoo statue for good luck in love.",
              details: [
                '⛩️ Hozenji Temple — the moss-covered water-splashing ritual is charming',
                '🏮 The alley is only 2.7m wide — impossibly atmospheric at night',
                '📸 One of the most romantic spots in all of Osaka'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Seitaro (Hozenji Yokocho)',
              description: "Fresh sushi and seafood in the heart of Hozenji Yokocho. Run by a fish dealer's son, the seafood is impeccable. Try the ika naruto-maki (squid sashimi roll) and seasonal nigiri. Intimate and romantic.",
              meta: '💰 $$$ · 📍 Hozenji Yokocho alley · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6526, lng: 135.5063, label: 'Shinsekai', num: 1, cat: 'attraction', desc: 'Retro 1912 entertainment district with kushikatsu & arcades' },
        { lat: 34.6524, lng: 135.5064, label: 'Tsutenkaku Tower', num: 2, cat: 'attraction', desc: 'Iconic tower with panoramic city views' },
        { lat: 34.6725, lng: 135.4980, label: 'Amerikamura', num: 3, cat: 'attraction', desc: 'Youth culture hub — vintage shops, street art, cafés' },
        { lat: 34.6690, lng: 135.5043, label: 'Hozenji Yokocho', num: 4, cat: 'attraction', desc: 'Atmospheric lantern-lit alley with temples and restaurants' },
        { lat: 34.6690, lng: 135.5045, label: 'Seitaro', num: 5, cat: 'food', desc: 'Fresh sushi by a fish dealer\'s son in Hozenji Yokocho' }
      ]
    },

    // ===== DAY 3: Monday April 6 — Osaka Castle & Sakura =====
    {
      num: 3,
      date: '2026-04-06',
      neighborhoods: 'Osaka Castle · Kema Sakuranomiya · Tenmabashi',
      title: 'Cherry Blossoms & Castle Magic',
      description: "Monday morning means fewer crowds at Osaka's best sakura spots. Start with cherry blossoms framing the magnificent castle, then walk the Kema Sakuranomiya riverside — a 4.2km tunnel of pink petals along the Okawa River.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Osaka Castle Park — Sakura Season',
              description: "With over 3,000 cherry trees, Osaka Castle Park is one of Kansai's premier hanami spots. The massive stone walls and moat reflect the pink blossoms beautifully. Enter from Tanimachi Yonchome and walk through Nishinomaru Garden for the best castle-and-sakura photo ops.",
              details: [
                '🌸 Nishinomaru Garden (¥350) — the iconic cherry blossom + castle view',
                '🏯 Castle tower entry ¥600 — exhibits on Toyotomi Hideyoshi\'s history',
                '📸 Best photo: from the south side of Nishinomaru Garden looking north'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kema Sakuranomiya Riverside Walk',
              description: "Walk north from the castle along the Okawa River to Kema Sakuranomiya Park. This 4.2km stretch has over 4,500 cherry trees forming a pink tunnel over the river path. It's one of Osaka's most magical sakura experiences — especially stunning when petals fall on the water.",
              details: [
                '🌸 4,500+ cherry trees lining 4.2km of riverbank',
                '🚣 River cruise boats pass under the blossoms — wave!',
                '🍱 Grab a bento from a konbini and have an impromptu hanami picnic'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Garb Weeks (Osaka Castle Park)',
              description: 'Casual Italian-Japanese café right in the castle park grounds. Terrace seating under the cherry blossoms with pasta, pizza, and seasonal salads.',
              meta: '💰 $$ · 📍 Osaka Castle Park · Terrace with sakura views'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Tenmabashi & Osaka Mint Area',
              description: "If the Osaka Mint Bureau's cherry blossom viewing is open (usually early-mid April), it's a spectacular evening walk with over 300 trees of 100+ rare varieties, many illuminated. Otherwise, enjoy the Tenmabashi area's riverside restaurants.",
              details: [
                '🌸 Osaka Mint — advance reservations usually required',
                '🏮 Evening illumination makes the late-blooming varieties glow'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Torikizoku',
              description: 'Popular yakitori chain beloved by locals — all skewers and drinks at amazing value. Chicken thigh, tsukune (chicken meatball), and negima (chicken & green onion) are highlights. Fun, casual, and totally beef-free.',
              meta: '💰 $ · 📍 Multiple Osaka locations · No reservations needed'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6873, lng: 135.5262, label: 'Osaka Castle', num: 1, cat: 'attraction', desc: 'Magnificent castle surrounded by 3,000 cherry trees' },
        { lat: 34.6865, lng: 135.5240, label: 'Nishinomaru Garden', num: 2, cat: 'attraction', desc: 'Best cherry blossom + castle photo spot' },
        { lat: 34.7012, lng: 135.5190, label: 'Kema Sakuranomiya Park', num: 3, cat: 'attraction', desc: '4.2km riverside cherry blossom tunnel' },
        { lat: 34.6940, lng: 135.5178, label: 'Osaka Mint Bureau', num: 4, cat: 'attraction', desc: '300+ rare cherry trees — special April opening' },
        { lat: 34.6875, lng: 135.5250, label: 'Garb Weeks', num: 5, cat: 'food', desc: 'Casual café with terrace in Osaka Castle Park' }
      ]
    },

    // ===== DAY 4: Tuesday April 7 — Nara Day Trip =====
    {
      num: 4,
      date: '2026-04-07',
      neighborhoods: 'Nara Park · Todaiji · Kasuga Taisha',
      title: 'Nara Day Trip — Deer, Temples & Sakura',
      description: "Early start on the Kintetsu-Nara line (~7:30 AM as planned). Nara in April is enchanting — over 1,000 friendly deer roam freely under cherry blossom canopies, and the ancient temples are jaw-dropping. Back to Osaka for dinner.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kintetsu-Nara Express & Nara Park',
              description: "Catch the Kintetsu limited express from Osaka-Namba to Kintetsu-Nara (~40 min). The station drops you right near Nara Park, where over 1,000 wild deer bow for shika-senbei crackers. In early April, the park is blanketed in cherry blossoms — deer posing under sakura is peak Japan.",
              details: [
                '🚃 Kintetsu-Nara line from Osaka-Namba — depart ~7:30 AM',
                '🦌 Buy shika-senbei (deer crackers, ¥200) from vendors in the park',
                '🌸 Mt. Wakakusa hillside behind the park has panoramic sakura views',
                '📸 Deer bowing under cherry trees = your best photo of the trip'
              ]
            },
            {
              title: 'Todaiji Temple — Great Buddha',
              description: "The world's largest wooden building houses a 15-meter bronze Buddha that has to be seen to be believed. Walk through the massive Nandaimon Gate guarded by fierce Nio guardians. Try squeezing through the pillar hole for good luck.",
              details: [
                '🏛️ Entry ¥600 · Opens 7:30 AM in April',
                '🕳️ The pillar hole is said to grant enlightenment — if you fit through!',
                '📸 The Great Buddha Hall against cherry blossoms is unforgettable'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kasuga Taisha Shrine',
              description: "Walk through the ancient forest path lined with 3,000 stone lanterns to reach Kasuga Taisha, Nara's most famous Shinto shrine. The vermillion buildings nestled in primeval forest with hanging wisteria (if you're lucky) are magical. Deer wander freely here too.",
              details: [
                '🏮 3,000 stone lanterns line the approach — donated over centuries',
                '⛩️ Vermillion shrine buildings date to 768 AD',
                '🌿 The surrounding forest is a UNESCO World Heritage Site'
              ]
            },
            {
              title: 'Naramachi — Old Merchant Quarter',
              description: "The historic merchant district south of Nara Park has beautifully preserved machiya (wooden townhouses), craft shops, and cozy cafés. Much quieter than the deer park area and great for a post-temple wind-down.",
              details: [
                '🏘️ Traditional machiya converted to shops and galleries',
                '🍵 Stop for matcha and wagashi at Nakatanidou (famous mochi-pounding shop)'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Kamaiki Udon',
              description: 'Hand-pulled udon noodles in a traditional Nara setting. Their kamaage udon (served in hot water with dipping sauce) and tempura set is a comforting, filling lunch after temple-hopping.',
              meta: '💰 $ · 📍 Near Kintetsu-Nara Station · Cash preferred'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Osaka',
              description: "Take the Kintetsu back to Namba and have a relaxed dinner in the Namba area. You'll have walked 15,000+ steps today — you've earned a good meal.",
              details: [
                '🚃 Last Kintetsu express back around 9:30 PM',
                '🦶 Expect 15-20k steps today — wear comfortable shoes'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Mizuno Okonomiyaki',
              description: "Osaka's most famous okonomiyaki restaurant, right on Dotonbori. Get the seafood mix (ika, ebi, pork) cooked on the iron griddle in front of you. Fluffy, savory, and utterly satisfying after a long day.",
              meta: '💰 $$ · 📍 Dotonbori · Queue expected, worth the wait'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6851, lng: 135.8310, label: 'Nara Park', num: 1, cat: 'attraction', desc: '1,000+ wild deer roaming under cherry blossoms' },
        { lat: 34.6890, lng: 135.8398, label: 'Todaiji Temple', num: 2, cat: 'attraction', desc: 'World\'s largest wooden building with Great Buddha' },
        { lat: 34.6812, lng: 135.8499, label: 'Kasuga Taisha Shrine', num: 3, cat: 'attraction', desc: '3,000 stone lanterns in primeval forest' },
        { lat: 34.6770, lng: 135.8325, label: 'Naramachi', num: 4, cat: 'attraction', desc: 'Historic merchant quarter with machiya townhouses' },
        { lat: 34.6687, lng: 135.5013, label: 'Mizuno Okonomiyaki', num: 5, cat: 'food', desc: 'Osaka\'s most famous okonomiyaki on Dotonbori' }
      ]
    },

    // ===== DAY 5: Wednesday April 8 — USJ =====
    {
      num: 5,
      date: '2026-04-08',
      neighborhoods: 'Universal Studios Japan · Bay Area',
      title: 'Universal Studios Japan — Full Day Adventure',
      description: "Wednesday at USJ means shorter weekday queues. Spend the full day exploring Super Nintendo World, the Wizarding World of Harry Potter, and thrilling rides. Express passes recommended for maximum fun.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Early Entry & Super Nintendo World',
              description: "Arrive before gates open (usually 8:30-9:00 AM). Head straight to Super Nintendo World — the timed entry fills up fast. Wear the Power-Up Band (¥4,800) to punch ? blocks and collect virtual coins. The Mario Kart ride is mind-blowing augmented reality.",
              details: [
                '🎮 Buy Express Pass in advance online — sells out for peak sakura season!',
                '⭐ Super Nintendo World timed entry — go first thing',
                '🏎️ Mario Kart: Koopa\'s Challenge — the marquee ride',
                '🍄 Toadstool Café — themed food, book via the USJ app'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Wizarding World of Harry Potter & Rides',
              description: "Hogwarts Castle looms over an incredibly detailed Hogsmeade village. The Forbidden Journey ride inside the castle is spectacular. Then hit the big rides: Hollywood Dream roller coaster, Jurassic World, and the Jaws boat ride.",
              details: [
                '🧙 Butterbeer (non-alcoholic) — ¥650, surprisingly delicious',
                '🎢 Hollywood Dream — ride it backwards for extra thrill',
                '🦕 Jurassic World — you will get wet'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Toadstool Café (Super Nintendo World)',
              description: 'Themed restaurant inside Super Nintendo World. Mario-themed dishes including mushroom soup in a ? block bowl, Peach\'s cake, and character-themed bento boxes.',
              meta: '💰 $$ · 📍 Super Nintendo World · Book via USJ app'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Night Parade & Final Rides',
              description: "If there's an evening parade or projection show, stay for it — USJ's nighttime entertainment is spectacular. Grab some last-minute rides with shorter evening queues before heading back to Namba.",
              details: [
                '🎆 Check USJ app for show times',
                '🚃 JR Yumesaki Line from Universal City to Nishi-Kujo, then Osaka Loop Line back'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ichiran Ramen (Dotonbori)',
              description: "After a long day of rides, nothing beats a steaming bowl of Ichiran's tonkotsu (pork bone) ramen. Order from the vending machine, customize your spice level, and slurp in your private booth. Zero beef, pure comfort.",
              meta: '💰 $ · 📍 Dotonbori · Open late · No reservations'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6654, lng: 135.4323, label: 'Universal Studios Japan', num: 1, cat: 'attraction', desc: 'Full day of rides, Super Nintendo World & Harry Potter' },
        { lat: 34.6656, lng: 135.4320, label: 'Super Nintendo World', num: 2, cat: 'attraction', desc: 'Mario Kart ride, ? blocks, and Toadstool Café' },
        { lat: 34.6652, lng: 135.4318, label: 'Wizarding World', num: 3, cat: 'attraction', desc: 'Hogwarts Castle and Hogsmeade Village' },
        { lat: 34.6687, lng: 135.5013, label: 'Ichiran Ramen', num: 4, cat: 'food', desc: 'Iconic tonkotsu ramen with private booths' }
      ]
    },

    // ===== DAY 6: Thursday April 9 — Transfer to Kyoto =====
    {
      num: 6,
      date: '2026-04-09',
      neighborhoods: 'Higashiyama · Gion · Kiyomizu',
      title: 'Move to Kyoto — Higashiyama & Gion at Golden Hour',
      description: "Check out of Osaka and take the 30-minute train to Kyoto. Drop bags at your hotel and spend the afternoon exploring Higashiyama's preserved streets and Gion's geisha district as the light turns golden. Cherry blossoms frame every temple.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Transfer to Kyoto',
              description: "Take the Hankyu Line from Umeda to Kawaramachi (¥410, 45 min) or JR Special Rapid from Osaka to Kyoto Station (¥580, 30 min). Check into your Kyoto hotel — ideally in the Gion/Higashiyama area for walkability.",
              details: [
                '🚃 JR Special Rapid is fastest; Hankyu drops you in central Kyoto',
                '🏨 Gion or Higashiyama area = walking distance to temples and restaurants',
                '🧳 Use coin lockers at Kyoto Station if hotel check-in is later'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kiyomizu-dera Temple',
              description: "Start with Kyoto's most iconic temple. The massive wooden stage juts out over the hillside with panoramic views of the city. In early April, cherry blossoms cascade down the valley below. Walk down through Sannen-zaka and Ninen-zaka — beautifully preserved cobblestone lanes with tea houses and craft shops.",
              details: [
                '⛩️ Entry ¥400 · Best light in afternoon',
                '🌸 Cherry blossoms frame the famous wooden stage perfectly',
                '🏮 Sannen-zaka & Ninen-zaka — Kyoto\'s most photogenic streets'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Omen Kodaiji',
              description: 'Beautiful udon restaurant near Kodaiji Temple. Their signature cold udon with seasonal vegetables and dipping broth is light and perfect for a temple-hopping day. Traditional wooden interior.',
              meta: '💰 $$ · 📍 Near Kodaiji Temple, Higashiyama'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Gion District Evening Walk',
              description: "As the light fades, Gion transforms. Paper lanterns illuminate the traditional machiya facades along Hanami-koji street. You might spot a maiko (apprentice geisha) hurrying to an engagement. Shirakawa Canal nearby is lined with weeping cherry blossoms and willow trees — heart-stoppingly romantic at night.",
              details: [
                '🏮 Hanami-koji — Gion\'s main street, lined with exclusive teahouses',
                '🌸 Shirakawa Canal — weeping cherries lit up at night',
                '📸 Be respectful — photos of geiko/maiko from a distance only'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Gion Kappa Restaurant',
              description: 'Welcoming izakaya in Gion serving excellent tofu dishes, grilled chicken, and seasonal Kyoto vegetables. Known for their yudofu (hot tofu) and chicken nanban. Intimate atmosphere with counter seating.',
              meta: '💰 $$ · 📍 Gion, near Hanami-koji · Reservations helpful'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9949, lng: 135.7850, label: 'Kiyomizu-dera', num: 1, cat: 'attraction', desc: 'Iconic temple with wooden stage and sakura valley views' },
        { lat: 34.9982, lng: 135.7808, label: 'Sannen-zaka & Ninen-zaka', num: 2, cat: 'attraction', desc: 'Preserved cobblestone lanes with tea houses' },
        { lat: 35.0037, lng: 135.7748, label: 'Gion (Hanami-koji)', num: 3, cat: 'attraction', desc: 'Geisha district with traditional teahouses' },
        { lat: 35.0045, lng: 135.7755, label: 'Shirakawa Canal', num: 4, cat: 'attraction', desc: 'Weeping cherries and willows — magical at night' },
        { lat: 35.0020, lng: 135.7790, label: 'Omen Kodaiji', num: 5, cat: 'food', desc: 'Beautiful udon near Kodaiji Temple' },
        { lat: 35.0040, lng: 135.7740, label: 'Gion Kappa', num: 6, cat: 'food', desc: 'Welcoming izakaya with tofu and chicken dishes' }
      ]
    },

    // ===== DAY 7: Friday April 10 — Fushimi Inari & South Kyoto =====
    {
      num: 7,
      date: '2026-04-10',
      neighborhoods: 'Fushimi Inari · Fushimi · Tofukuji',
      title: 'Vermillion Gates & Sake District',
      description: "Beat the crowds with an early visit to Fushimi Inari's thousands of torii gates, then explore the Fushimi sake district for tastings. Afternoon at the serene Tofukuji Temple gardens.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Fushimi Inari Taisha — Sunrise Visit',
              description: "Arrive by 7 AM to walk the 10,000 vermillion torii gates in near-solitude. The trail winds up Mt. Inari for about 2 hours (full loop). The early sections are the most photogenic — the light filtering through the orange gates is ethereal. You don't need to summit; the Yotsutsuji intersection halfway up has amazing city views.",
              details: [
                '⛩️ Free entry · Open 24 hours · Best before 8 AM',
                '🦊 Fox statues everywhere — Inari\'s divine messengers',
                '📸 The tunnel of gates is most dramatic in the first 20 minutes of walking',
                '🥾 Full loop: ~4km, ~2 hours. Halfway point has the best view.'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Fushimi Sake District',
              description: "Kyoto's Fushimi ward is one of Japan's great sake-brewing regions. Visit Gekkeikan Okura Sake Museum (¥600, includes tasting) and walk the picturesque canal lined with sake breweries and willow trees. Several breweries offer free tastings.",
              details: [
                '🍶 Gekkeikan Okura Museum — sake history + 3 tastings included',
                '🚣 The canal area is beautiful — weeping willows and stone bridges',
                '🍶 Kizakura Kappa Country — brewery, restaurant, and beer garden'
              ]
            },
            {
              title: 'Tofukuji Temple Gardens',
              description: "Often overlooked in favor of more famous temples, Tofukuji has some of Kyoto's finest Zen gardens. The Hojo garden by Mirei Shigemori is a modernist masterpiece of moss and stone. Much quieter than Kiyomizu-dera.",
              details: [
                '🏛️ Entry ¥500 for gardens · The bridge walkway is stunning',
                '🌿 Four gardens representing the four seasons',
                '📸 The moss checkerboard garden is Instagram-famous for good reason'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Torisei (Fushimi)',
              description: 'Yakitori and sake pairing in the heart of the brewery district. They brew their own sake on-site. Grilled chicken thigh, chicken skin, and seasonal vegetable skewers pair perfectly with fresh junmai sake.',
              meta: '💰 $$ · 📍 Fushimi sake district · Try the sake flight'
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Menbakaichidai Fire Ramen',
              description: "Kyoto's famous fire ramen — the chef literally sets your bowl of green onion ramen ablaze before serving. The spectacle is thrilling and the ramen (chicken/pork broth) is genuinely delicious. A unique and unforgettable dinner.",
              meta: '💰 $ · 📍 Near Kitaoji Station · Queue from 5 PM'
            }
          ],
          tips: [
            { type: 'tip', text: 'The fire ramen show happens with every bowl — sit at the counter for the best view. They drape a protective cape over you. It\'s hilarious and delicious.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari Taisha', num: 1, cat: 'attraction', desc: '10,000 vermillion torii gates winding up Mt. Inari' },
        { lat: 34.9290, lng: 135.7570, label: 'Gekkeikan Sake Museum', num: 2, cat: 'attraction', desc: 'Sake history museum with tastings in Fushimi' },
        { lat: 34.9764, lng: 135.7740, label: 'Tofukuji Temple', num: 3, cat: 'attraction', desc: 'Stunning Zen gardens and bridge walkway' },
        { lat: 34.9300, lng: 135.7575, label: 'Torisei', num: 4, cat: 'food', desc: 'Yakitori and house-brewed sake in Fushimi' },
        { lat: 35.0445, lng: 135.7585, label: 'Menbakaichidai', num: 5, cat: 'food', desc: 'Famous fire ramen — chef sets your bowl ablaze' }
      ]
    },

    // ===== DAY 8: Saturday April 11 — Weekend: Casual Kyoto =====
    {
      num: 8,
      date: '2026-04-11',
      neighborhoods: 'Nishiki Market · Teramachi · Pontocho',
      title: 'Saturday Slow — Markets, Shopping & Pontocho',
      description: "Weekend means neighborhood mode. Skip the tourist temples and dive into Kyoto's local life — Nishiki Market for breakfast grazing, Teramachi arcade for shopping, and Pontocho alley for a romantic riverside dinner as the Kamo River sparkles.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Nishiki Market — Kyoto\'s Kitchen',
              description: "This 400-year-old covered market stretches five blocks and is packed with over 100 vendors selling pickles, tofu, mochi, grilled seafood, matcha sweets, and Kyoto specialties. Graze your way through — it's the best breakfast in Kyoto.",
              details: [
                '🐟 Try grilled unagi (eel) on a stick',
                '🍡 Mochi and dango stands everywhere',
                '🥒 Kyoto tsukemono (pickles) — try the shibazuke',
                '🍵 Fresh matcha soft serve from Nishiki\'s tea shops'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Teramachi & Shinkyogoku Shopping',
              description: "Two parallel covered arcades running north-south through central Kyoto. Teramachi is more traditional (incense shops, washi paper, antique bookstores), while Shinkyogoku is younger (fashion, souvenirs, crêpes). Perfect for a rainy afternoon too.",
              details: [
                '🎋 Kyukyodo — famous incense and stationery shop since 1663',
                '📿 Nishiki Tenmangu Shrine — hidden between the shops',
                '🍧 Daifuku-ya — fresh daifuku mochi made before your eyes'
              ]
            },
            {
              title: 'Kamo River Walk',
              description: "The Kamo River is the heart of Kyoto. Couples sit along the riverbanks in evenly spaced pairs (it's a real tradition!). Walk along the path from Sanjo to Shijo, watching herons fish and the light change. In April, cherry trees line sections of the river.",
              details: [
                '🌸 Cherry trees along the river between Kitaoji and Marutamachi',
                '💑 The couple-spacing tradition is called "Kamo River equal spacing law"',
                '🦢 Great blue herons are a common sight'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Tsukimochiya Naomasa',
              description: 'Tiny traditional sweets shop near Nishiki Market. Their tsukimi dango and seasonal wagashi with matcha are the perfect mid-shopping treat.',
              meta: '💰 $ · 📍 Near Nishiki Market'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Pontocho Alley',
              description: "Pontocho is Kyoto's most atmospheric dining alley — a single narrow lane running parallel to the Kamo River, lined with traditional restaurants and bars. In warm April evenings, many restaurants open their riverside terraces (kawadoko/kawayuka). The lanterns, the river sounds, the cherry petals — it's peak romance.",
              details: [
                '🏮 One of Kyoto\'s most beautiful streets — especially at dusk',
                '🍷 Many restaurants have Kamo River terraces in April',
                '📸 Walk the full length before choosing a restaurant'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Hafuu Honten',
              description: "Beloved Kyoto yoshoku (Western-Japanese fusion) restaurant. Their pork cutlet (tonkatsu) is legendary, and they also serve excellent seafood gratin and cream croquettes. Cozy, unpretentious, and completely beef-free.",
              meta: '💰 $$ · 📍 Near Pontocho · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0050, lng: 135.7650, label: 'Nishiki Market', num: 1, cat: 'food', desc: 'Kyoto\'s 400-year-old kitchen — 100+ food vendors' },
        { lat: 35.0060, lng: 135.7640, label: 'Teramachi Arcade', num: 2, cat: 'attraction', desc: 'Traditional shopping arcade — incense, paper, antiques' },
        { lat: 35.0055, lng: 135.7695, label: 'Kamo River', num: 3, cat: 'attraction', desc: 'Kyoto\'s heart — couples, herons, cherry trees' },
        { lat: 35.0060, lng: 135.7700, label: 'Pontocho Alley', num: 4, cat: 'attraction', desc: 'Atmospheric dining alley with riverside terraces' },
        { lat: 35.0040, lng: 135.7690, label: 'Hafuu Honten', num: 5, cat: 'food', desc: 'Legendary tonkatsu and yoshoku in Kyoto' }
      ]
    },

    // ===== DAY 9: Sunday April 12 — Weekend: Arashiyama (casual) + Kobe =====
    {
      num: 9,
      date: '2026-04-12',
      neighborhoods: 'Arashiyama · Sagano · Kobe Harbour',
      title: 'Bamboo Grove Morning & Kobe Sunset',
      description: "Early morning at Arashiyama's bamboo grove before it gets crowded (it's Sunday, so this is key). Then afternoon train to Kobe for harbour views and an incredible seafood dinner — your extra day trip, beef-free and beautiful.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Arashiyama Bamboo Grove — Early Visit',
              description: "Arrive by 7:30 AM to experience the bamboo grove in near-silence. The towering stalks creak and sway overhead, filtering the light into an ethereal green glow. Walk through to Okochi Sanso villa garden (¥1,000, includes matcha) for stunning views over the valley and cherry blossoms.",
              details: [
                '🎋 Before 8 AM is essential for crowd-free photos',
                '🍵 Okochi Sanso — matcha served with the mountain view',
                '🌸 Togetsukyo Bridge with cherry blossoms — Arashiyama\'s signature view'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: '% Arabica Arashiyama',
              description: 'Famous specialty coffee shop right by the Togetsukyo Bridge. Their latte with Arashiyama mountain views is one of Kyoto\'s most Instagrammed moments.',
              meta: '💰 $ · 📍 Togetsukyo Bridge area · Queue expected'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Train to Kobe',
              description: "From Kyoto, take the JR Special Rapid to Sannomiya Station (about 50 min, ¥1,110). Kobe is a cosmopolitan port city sandwiched between mountains and sea. Walk along the harbour, visit Meriken Park, and enjoy the waterfront atmosphere.",
              details: [
                '🚃 JR Special Rapid from Kyoto to Kobe-Sannomiya — ~50 min',
                '⛵ Meriken Park & Kobe Port Tower — great harbour walk',
                '🏙️ Kobe\'s Chinatown (Nankinmachi) is fun for afternoon snacking'
              ]
            },
            {
              title: 'Kobe Harbour & Nankinmachi',
              description: "Walk along Kobe's beautiful waterfront — Meriken Park has the iconic Kobe Port Tower and the earthquake memorial. Then duck into Nankinmachi (Chinatown) for pork buns, dumplings, and bubble tea. It's compact and lively.",
              details: [
                '🏮 Nankinmachi — Kobe\'s Chinatown, great for pork buns and dumplings',
                '📸 Kobe Port Tower and the BE KOBE sign — photo ops',
                '🌅 The harbour faces west — perfect for sunset'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Kobe Harbour Sunset',
              description: "Watch the sun set over the harbour from Meriken Park or the Mosaic mall waterfront. The sky turns pink and orange over the water — a perfect romantic moment before dinner.",
              details: [
                '🌅 Sunset around 6:15 PM in mid-April',
                '📸 Harbour at Night is also spectacular — stay for the lights'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Kobe Plaisir',
              description: "While Kobe is famous for beef, Kobe Plaisir also serves excellent seafood courses — fresh sashimi, grilled lobster, and Akashi sea bream. Your partner can enjoy premium seafood while you can try their chicken or pork options. Harbour views.",
              meta: '💰 $$$ · 📍 Kobe Harbour area · Reservations recommended'
            }
          ],
          tips: [
            { type: 'tip', text: "Kobe has incredible non-beef options: try Akashi-yaki (egg-based octopus dumplings, Kobe's local specialty), fresh sashimi from the Akashi Strait, or Chinese food in Nankinmachi. You won't miss the beef!" }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0154, lng: 135.6780, label: 'Arashiyama Bamboo Grove', num: 1, cat: 'attraction', desc: 'Towering bamboo forest — ethereal early morning' },
        { lat: 35.0144, lng: 135.6772, label: 'Togetsukyo Bridge', num: 2, cat: 'attraction', desc: 'Arashiyama\'s iconic bridge with cherry blossoms' },
        { lat: 34.6850, lng: 135.1894, label: 'Meriken Park', num: 3, cat: 'attraction', desc: 'Kobe\'s waterfront with Port Tower and earthquake memorial' },
        { lat: 34.6868, lng: 135.1835, label: 'Nankinmachi (Chinatown)', num: 4, cat: 'food', desc: 'Kobe\'s Chinatown — pork buns, dumplings, Akashi-yaki' },
        { lat: 34.6855, lng: 135.1900, label: 'Kobe Plaisir', num: 5, cat: 'food', desc: 'Harbour restaurant with seafood and non-beef courses' }
      ]
    },

    // ===== DAY 10: Monday April 13 — Uji Day Trip =====
    {
      num: 10,
      date: '2026-04-13',
      neighborhoods: 'Uji · Byodoin · Ujigawa River',
      title: 'Uji — Matcha, Temples & Tea Country',
      description: "A serene day trip to Uji, the birthplace of Japanese tea culture. Visit the stunning Byodoin Temple (it's on the ¥10 coin!), stroll the Uji River with its cherry blossoms, and taste the finest matcha in the world. Back to Kyoto for a farewell dinner.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Train to Uji & Byodoin Temple',
              description: "Take the JR Nara Line from Kyoto to Uji (17 min, ¥240). Walk straight to Byodoin Temple before the crowds — the Phoenix Hall floating on its pond is one of Japan's most serene and beautiful sights. It's the image on the ¥10 coin and the ¥10,000 bill.",
              details: [
                '🏛️ Byodoin entry ¥700 · Phoenix Hall interior tour ¥300 extra (limited tickets)',
                '📸 The reflection of Phoenix Hall in the pond = perfect symmetry',
                '🌸 Cherry trees frame the temple beautifully in April',
                '💴 Compare the real thing to your ¥10 coin!'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Uji Tea Street & Matcha Tasting',
              description: "Omotesando street leading to Byodoin is lined with centuries-old tea shops. Uji matcha is considered Japan's finest — taste the difference in a traditional tea ceremony or simply at a tea house. Try matcha everything: soft serve, soba, mochi, parfaits.",
              details: [
                '🍵 Nakamura Tokichi Honten — matcha tea house since 1859, try the matcha jelly',
                '🍦 Matcha soft serve from Tsuen Tea — Japan\'s oldest tea shop (1160 AD!)',
                '🍡 Matcha dango and warabi mochi from street vendors'
              ]
            },
            {
              title: 'Ujigami Shrine & Uji River Walk',
              description: "Cross the Uji River to Ujigami Shrine — the oldest surviving Shinto shrine building in Japan (11th century). Then walk along the Uji River path, watching cormorant fishermen and enjoying the cherry blossoms reflected in the water.",
              details: [
                '⛩️ Ujigami Shrine — UNESCO World Heritage Site, remarkably modest',
                '🎣 Uji is famous for cormorant fishing (ukai) in summer',
                '🌸 The river walk is beautifully lined with cherry trees'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Nakamura Tokichi Honten',
              description: "Uji's most famous tea house, operating since 1859. Their matcha jelly parfait is legendary — layers of matcha jelly, red bean, shiratama dango, and matcha ice cream. Also serves excellent matcha soba and udon.",
              meta: '💰 $$ · 📍 Uji Omotesando · Queue expected, worth it'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Kyoto — Final Evening',
              description: "Head back to Kyoto for your last evening. Take a final stroll along the Kamo River or through Gion. Tomorrow is departure day, so soak in the atmosphere one more time.",
              details: [
                '🚃 JR back to Kyoto — 17 min',
                '🌸 If cherry blossoms are still going, Maruyama Park has beautiful night illumination'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Kyoto Gogyo',
              description: "Celebrated ramen restaurant known for their kogashi (burnt) miso ramen — the miso is charred in a wok to create a deep, smoky flavor. Rich chicken and pork broth, no beef. A perfect farewell bowl.",
              meta: '💰 $$ · 📍 Nishikikoji, central Kyoto · Open until late'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.8893, lng: 135.8078, label: 'Byodoin Temple', num: 1, cat: 'attraction', desc: 'Phoenix Hall — on the ¥10 coin, floating on a pond' },
        { lat: 34.8908, lng: 135.8088, label: 'Uji Omotesando (Tea Street)', num: 2, cat: 'food', desc: 'Centuries-old tea shops and matcha everything' },
        { lat: 34.8930, lng: 135.8110, label: 'Ujigami Shrine', num: 3, cat: 'attraction', desc: 'Oldest surviving Shinto shrine building (11th century)' },
        { lat: 34.8900, lng: 135.8085, label: 'Nakamura Tokichi', num: 4, cat: 'food', desc: 'Legendary matcha tea house since 1859' },
        { lat: 35.0050, lng: 135.7660, label: 'Kyoto Gogyo', num: 5, cat: 'food', desc: 'Famous kogashi (burnt) miso ramen' }
      ]
    },

    // ===== DAY 11: Tuesday April 14 — Departure =====
    {
      num: 11,
      date: '2026-04-14',
      neighborhoods: 'Kyoto Station · Central Kyoto',
      title: 'Sayonara Kyoto — Last Morning Moments',
      description: "Your final morning in Japan. Depending on your flight time, squeeze in a last temple visit or simply enjoy a leisurely breakfast and pick up omiyage (souvenirs) at Kyoto Station before heading to the airport.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Final Morning Options',
              description: "If your flight is later, consider a peaceful morning at Nanzenji Temple (free grounds, beautiful aqueduct) or the Philosopher's Path cherry blossom walk nearby. For an early flight, Kyoto Station's underground mall has excellent breakfast options and gift shops.",
              details: [
                '⛩️ Nanzenji — the brick aqueduct is stunning at any time',
                '🌸 Philosopher\'s Path — 2km canal walk under sakura canopy',
                '🛍️ Kyoto Station Porta underground mall — omiyage paradise',
                '🍵 Buy Uji matcha, yatsuhashi sweets, and Kyoto pickles as gifts'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Inoda Coffee (Sanjo)',
              description: "Kyoto's most beloved kissaten (retro coffee house) since 1940. Their 'Kyoto Breakfast' set with thick toast, egg, and ham with their signature arabica blend is a local institution. The perfect calm final meal.",
              meta: '💰 $$ · 📍 Sanjo, central Kyoto · No reservations'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Depart from Kansai',
              description: "Head to Kansai International Airport (KIX) via the Haruka Express from Kyoto Station (75 min, ¥3,640) or Itami Airport for domestic flights. Buy last-minute Kit-Kats and snacks at the airport — Japan's airport gift shops are incredible.",
              details: [
                '🚃 Haruka Express — direct from Kyoto Station to KIX',
                '✈️ Itami Airport for domestic flights — limousine bus from Kyoto Station (55 min)',
                '🍫 Airport gift floors have exclusive flavors and beautifully wrapped omiyage'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'The Haruka Express has reserved seats — book at the JR ticket counter or online. ICOCA + Haruka combo ticket offers a discount if purchased at the airport on arrival.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0116, lng: 135.7681, label: 'Kyoto Station', num: 1, cat: 'attraction', desc: 'Transport hub with excellent shopping and food' },
        { lat: 35.0112, lng: 135.7923, label: 'Nanzenji Temple', num: 2, cat: 'attraction', desc: 'Zen temple with stunning brick aqueduct' },
        { lat: 35.0157, lng: 135.7941, label: "Philosopher's Path", num: 3, cat: 'attraction', desc: '2km cherry blossom walk along a canal' },
        { lat: 35.0082, lng: 135.7669, label: 'Inoda Coffee', num: 4, cat: 'food', desc: 'Kyoto\'s beloved retro coffee house since 1940' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '¥8,000–15,000/night', midrange: '¥15,000–30,000/night', luxury: '¥30,000–80,000/night' },
    { category: 'Meals (per couple)', budget: '¥4,000–7,000/day', midrange: '¥8,000–15,000/day', luxury: '¥15,000–30,000/day' },
    { category: 'Transport', budget: '¥1,500–3,000/day', midrange: '¥3,000–5,000/day', luxury: '¥5,000–10,000/day' },
    { category: 'Activities/Entry', budget: '¥0–2,000/day', midrange: '¥2,000–5,000/day', luxury: '¥5,000–15,000/day' },
    { category: 'USJ (Day Pass + Express)', budget: '¥9,000pp', midrange: '¥15,000pp', luxury: '¥25,000pp (VIP)' },
    { category: '11-Day Total (couple)', budget: '$2,000–3,500', midrange: '$3,500–6,000', luxury: '$6,000–12,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Kansai International Airport (KIX) serves international flights — 50 min to central Osaka by Nankai Rapi:t', 'Itami Airport (ITM) for domestic — 30 min to Osaka by limousine bus', 'Haruka Express connects KIX to Kyoto directly (75 min)'] },
    { title: '🏨 Where to Stay', items: ['Osaka (nights 1-5): Namba or Shinsaibashi area — walkable to Dotonbori, great metro access', 'Kyoto (nights 6-10): Gion or Higashiyama — walk to temples and traditional streets', 'Budget: business hotels or Airbnb machiya | Mid: boutique ryokan | Luxury: traditional ryokan with kaiseki'] },
    { title: '🌡️ April Weather', items: ['Daytime: 15-20°C (59-68°F), nights 8-12°C (46-54°F)', 'Cherry blossoms typically peak April 3-10 in Osaka/Kyoto', 'Rain is possible — pack a compact umbrella', 'Layers recommended: light jacket, scarf for cool mornings'] },
    { title: '💳 Money', items: ['Japan is increasingly cashless, but many small shops/temples still need cash', 'Carry ¥10,000-20,000 in cash as backup', '7-Eleven and Family Mart ATMs accept international cards', 'IC card (ICOCA) for all local transport'] },
    { title: '📱 Connectivity', items: ['Rent a pocket WiFi at KIX or buy an eSIM before departure', 'Google Maps works perfectly for train navigation in Japan', 'Download Google Translate with Japanese offline pack'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
