const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771974512526_eu8v45',
  email: 'ritwik.kumar@gmail.com',
  destination: 'Japan',
  startDate: '2026-03-23',
  endDate: '2026-03-31',
  groupSize: 4,
  requests: ''
};

const itineraryData = {
  destination: 'Japan',
  countryEmoji: '🇯🇵',
  title: 'Cherry Blossom Season Across Japan',
  subtitle: '8 nights through Tokyo, Kyoto & Osaka — sakura, street food, temples & nightlife',
  description: "Late March is the most magical time to visit Japan — cherry blossoms are bursting into bloom across the country. This itinerary takes your group from the neon-lit streets of Tokyo to Kyoto's serene temples and Osaka's legendary food scene. You'll catch early sakura in Tokyo, full bloom in Kyoto, feast your way through Dotonbori, explore ancient shrines, and experience Japan's incredible nightlife. Adventure, culture, and unforgettable food — all in one trip.",
  duration: '8 nights',
  dates: 'Mar 23 – Mar 31, 2026',
  budget: '$$–$$$',
  pace: 'Moderate',
  bestFor: 'Groups · Families · Foodies',
  highlights: [
    'Cherry blossoms at Ueno Park & Meguro River in Tokyo',
    'Fushimi Inari\'s 10,000 vermillion torii gates at sunrise',
    'Street food crawl through Osaka\'s Dotonbori',
    'Golden Gai bar-hopping in Shinjuku',
    'Bamboo Grove & geisha district in Kyoto',
    'teamLab Borderless immersive digital art',
    'Day trip to Nara\'s friendly bowing deer'
  ],

  essentials: [
    { title: '🌸 Cherry Blossom Timing', text: 'Late March is peak sakura season. Tokyo blooms around March 20-25, Kyoto around March 25-April 2. You\'re arriving at the perfect time — expect stunning blossoms everywhere.' },
    { title: '🚄 Getting Around', text: 'Get a 7-day Japan Rail Pass (¥50,000/~$330). Covers bullet trains (shinkansen) between cities and most JR lines within cities. Activate it on Day 2 for maximum value. Use IC cards (Suica/Pasmo) for metros and buses.' },
    { title: '💴 Cash is King', text: 'Japan is still cash-heavy. Withdraw yen from 7-Eleven ATMs (international cards work). Budget ¥5,000-10,000/person/day for food and small purchases. Convenience stores (konbini) are incredible — fresh onigiri, bento, and snacks 24/7.' },
    { title: '👨‍👩‍👧‍👦 Family Tips', text: 'Japan is extremely family-friendly. Kids ride trains free under 6. Most restaurants welcome children. Konbini have everything you might need. Temples and shrines are free to enter (some charge ¥300-500).' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-23',
      neighborhoods: 'Shinjuku · Kabukichō · Golden Gai',
      title: 'Arrival in Tokyo — Neon Lights & Nightlife',
      description: 'Land in Tokyo and dive straight into the electric energy of Shinjuku. Check into your hotel, explore the world\'s busiest train station area, and kick off the trip with an unforgettable night in Golden Gai — Tokyo\'s legendary alley of tiny bars.',
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive & Explore Shinjuku',
              description: 'After landing at Narita or Haneda, take the Narita Express or monorail to Shinjuku. Check into your hotel and head out to explore. The area around Shinjuku Station is a sensory overload of department stores, restaurants, and neon signs.',
              details: [
                '✈️ Narita Express to Shinjuku: ~80 min, ¥3,250',
                '✈️ Haneda monorail + transfer: ~45 min',
                '🏨 Stay in Shinjuku for easy access to trains and nightlife',
                '📸 Shinjuku\'s south terrace has a great city view — free'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Pick up a Suica/Pasmo IC card at the airport — tap-and-go on all Tokyo trains and buses. Also works at vending machines and konbini.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Golden Gai Bar Hopping',
              description: 'Golden Gai is a maze of over 200 tiny bars crammed into six narrow alleys. Each bar seats 5-10 people and has its own personality — jazz bars, punk bars, whisky bars, anime bars. It\'s an experience unlike anything else on Earth.',
              details: [
                '🍶 Most bars charge a small cover (¥500-1,000) plus drinks',
                '🎵 Try Albatross for its chandelier-lit three-story interior',
                '🥃 Look for bars with English menus or welcoming signs outside',
                '👨‍👩‍👧‍👦 Golden Gai is best after 8pm; some bars are 20+ only'
              ]
            }
          ],
          meals: [
            {
              type: '🍜 Dinner',
              name: 'Fuunji Tsukemen',
              description: 'One of Tokyo\'s most famous tsukemen (dipping ramen) shops. The rich, thick broth and perfectly chewy noodles are legendary. Always a queue — worth every minute.',
              meta: '💰 $ · 📍 2-14-3 Yoyogi, Shibuya (near Shinjuku south exit) · Cash only'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6896, lng: 139.7006, label: 'Shinjuku Station', num: 1, cat: 'attraction', desc: 'World\'s busiest train station — your Tokyo base' },
        { lat: 35.6938, lng: 139.7036, label: 'Golden Gai', num: 2, cat: 'nightlife', desc: '200+ tiny bars in atmospheric narrow alleys' },
        { lat: 35.6886, lng: 139.7021, label: 'Fuunji Tsukemen', num: 3, cat: 'food', desc: 'Legendary dipping ramen — expect a queue' },
        { lat: 35.6945, lng: 139.7035, label: 'Kabukichō', num: 4, cat: 'attraction', desc: 'Tokyo\'s vibrant entertainment district' }
      ]
    },
    {
      num: 2,
      date: '2026-03-24',
      neighborhoods: 'Asakusa · Akihabara · Ueno · Yanaka',
      title: 'Old Tokyo — Temples, Arcades & Cherry Blossoms',
      description: 'Explore the traditional side of Tokyo. Start at the ancient Sensō-ji temple in Asakusa, hunt for anime treasures in Akihabara, then catch the cherry blossoms at Ueno Park — one of Tokyo\'s best hanami (flower viewing) spots.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Sensō-ji Temple & Nakamise-dōri',
              description: 'Tokyo\'s oldest temple (founded 645 AD) is stunning in the morning light. Walk through the iconic Kaminarimon Thunder Gate, browse the 250m Nakamise shopping street for traditional snacks and souvenirs, then explore the temple grounds.',
              details: [
                '⛩️ Free entry · Open 24/7 (main hall 6am-5pm)',
                '🍡 Try ningyo-yaki (custard-filled cakes) and age-manju (fried sweet buns)',
                '📸 The five-story pagoda with cherry blossoms is incredible',
                '🎋 Draw an omikuji fortune slip (¥100) — shake the metal cylinder!'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Pelican Café',
              description: 'Iconic bakery since 1942. Their thick-cut shokupan toast with butter is a Tokyo institution. Small, cozy, and absolutely delicious.',
              meta: '💰 $ · 📍 1-25-15 Kotobuki, Taito · Opens 8am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Akihabara Electric Town',
              description: 'The world capital of anime, manga, and gaming. Explore multi-story arcades, retro game shops, figure stores, and maid cafés. Even if you\'re not into anime, the sheer spectacle is unforgettable.',
              details: [
                '🎮 Super Potato — retro game paradise across 5 floors',
                '🎯 Try crane games (UFO catchers) — they\'re addictive!',
                '🤖 Yodobashi Camera — 9 floors of every electronic imaginable',
                '👨‍👩‍👧‍👦 Kids will love the arcades and Pokémon Center nearby'
              ]
            },
            {
              title: 'Ueno Park Cherry Blossoms',
              description: 'Ueno Park has over 1,000 cherry trees and is one of Tokyo\'s most popular hanami spots. By late March, the blossoms should be in full bloom. Grab some konbini snacks and drinks and join the locals for a hanami picnic under the sakura.',
              details: [
                '🌸 Over 1,000 cherry trees line the main path',
                '🍱 Grab bento boxes from a nearby konbini for a picnic',
                '🏛️ Tokyo National Museum is here too — Japan\'s oldest and largest'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Yanaka Ginza & Izakaya Dinner',
              description: 'Yanaka is Tokyo\'s best-preserved old neighborhood — narrow lanes, traditional shops, and cats everywhere. Yanaka Ginza shopping street is charming at dusk. End the day at a traditional izakaya (Japanese pub).',
              details: [
                '🐱 Yanaka is famous for its cats — look for cat-themed shops',
                '🌅 The "Sunset Stairway" (Yūyake Dandan) is beautiful at golden hour'
              ]
            }
          ],
          meals: [
            {
              type: '🍺 Dinner',
              name: 'Torikizoku',
              description: 'Beloved chain izakaya where almost everything is ¥350 (~$2.30). Yakitori skewers, edamame, karaage, beer — authentic Japanese pub experience at unbeatable prices. Perfect for groups.',
              meta: '💰 $ · 📍 Multiple locations in Ueno area'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: 'Sensō-ji Temple', num: 1, cat: 'attraction', desc: 'Tokyo\'s oldest temple with iconic Thunder Gate' },
        { lat: 35.7022, lng: 139.7745, label: 'Akihabara', num: 2, cat: 'attraction', desc: 'Electric Town — anime, gaming, and tech paradise' },
        { lat: 35.7146, lng: 139.7732, label: 'Ueno Park', num: 3, cat: 'attraction', desc: '1,000+ cherry trees — top hanami spot' },
        { lat: 35.7262, lng: 139.7677, label: 'Yanaka Ginza', num: 4, cat: 'attraction', desc: 'Old Tokyo charm with cat-themed shops' },
        { lat: 35.7124, lng: 139.7958, label: 'Pelican Café', num: 5, cat: 'food', desc: 'Legendary shokupan toast since 1942' }
      ]
    },
    {
      num: 3,
      date: '2026-03-25',
      neighborhoods: 'Shibuya · Harajuku · Omotesandō · Meguro',
      title: 'Pop Culture, Fashion & Sakura Along the River',
      description: 'Today is all about Tokyo\'s youthful energy. Cross the world\'s most famous intersection, explore Harajuku\'s wild fashion scene, visit teamLab Borderless, and end with a magical evening walk along the Meguro River — arguably Tokyo\'s most beautiful cherry blossom spot.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shibuya Crossing & Shibuya Sky',
              description: 'Start at the world\'s busiest pedestrian crossing. Watch the organized chaos from the Starbucks above, then head up to Shibuya Sky — a rooftop observation deck with 360° views of Tokyo stretching to Mt. Fuji on clear days.',
              details: [
                '📸 Best crossing photo: from the Magnet by Shibuya 109 building Starbucks',
                '🏙️ Shibuya Sky: ¥2,000, book online to skip the queue',
                '🐕 Say hi to the Hachiko statue outside the station'
              ]
            },
            {
              title: 'Harajuku & Takeshita Street',
              description: 'Harajuku is Tokyo\'s fashion and youth culture epicenter. Takeshita-dōri is a narrow, colorful street packed with quirky fashion shops, crêpe stands, and cotton candy bigger than your head.',
              details: [
                '🍦 Try a rainbow cotton candy or Harajuku crêpe',
                '👗 Explore side streets for vintage and designer shops',
                '⛩️ Meiji Shrine is a peaceful forest escape right next door'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Bills Omotesandō',
              description: 'The famous Australian café known as the "birthplace of ricotta hotcakes." Light, fluffy, and topped with honeycomb butter and banana. A Tokyo brunch institution.',
              meta: '💰 $$ · 📍 Omotesandō, Shibuya · Book ahead on weekends'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'teamLab Borderless',
              description: 'An immersive digital art museum where projections flow across walls, floors, and ceilings in an ever-changing dreamscape. Wander through rooms of waterfalls, flowers, and infinite crystal universes. Absolutely mesmerizing for all ages.',
              details: [
                '🎨 Located in Azabudai Hills, Minato (moved from Odaiba)',
                '🎫 ¥3,800 adults, ¥1,500 kids · Book online in advance — sells out!',
                '⏰ Allow 2-3 hours · Wear white to reflect the projections',
                '📸 Every room is insanely photogenic'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Meguro River Cherry Blossoms',
              description: 'The Meguro River is lined with 800+ cherry trees that form a stunning pink tunnel over the water. In late March, the blossoms are at their peak. The lantern-lit evening walk is pure magic — one of the most beautiful urban scenes in the world.',
              details: [
                '🌸 800+ cherry trees line both banks for 3.8km',
                '🏮 Paper lanterns illuminate the blossoms after dark',
                '🍺 Street food and drink stalls set up along the river',
                '📸 Nakameguro Station exit is the best starting point'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Afuri Ramen (Nakameguro)',
              description: 'Famous for their light, refreshing yuzu shio (citrus salt) ramen — a perfect contrast to heavy tonkotsu. The open kitchen and modern vibe make it feel special.',
              meta: '💰 $ · 📍 1-1-7 Ebisu, Shibuya (Nakameguro area)'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6595, lng: 139.7004, label: 'Shibuya Crossing', num: 1, cat: 'attraction', desc: 'World\'s busiest pedestrian crossing' },
        { lat: 35.6702, lng: 139.7026, label: 'Harajuku / Takeshita-dōri', num: 2, cat: 'attraction', desc: 'Wild fashion, crêpes, and youth culture' },
        { lat: 35.6624, lng: 139.7314, label: 'teamLab Borderless', num: 3, cat: 'attraction', desc: 'Immersive digital art at Azabudai Hills' },
        { lat: 35.6440, lng: 139.6988, label: 'Meguro River', num: 4, cat: 'attraction', desc: '800+ cherry trees forming a pink tunnel' },
        { lat: 35.6673, lng: 139.7122, label: 'Bills Omotesandō', num: 5, cat: 'food', desc: 'Famous ricotta hotcakes brunch' },
        { lat: 35.6440, lng: 139.6992, label: 'Afuri Ramen', num: 6, cat: 'food', desc: 'Refreshing yuzu shio ramen' }
      ]
    },
    {
      num: 4,
      date: '2026-03-26',
      neighborhoods: 'Toyosu · Tsukiji Outer Market · Roppongi',
      title: 'Fish Markets, Sushi & Tokyo\'s Wildest Night Out',
      description: 'Experience the world\'s greatest fish market at dawn, master sushi-making, explore the vibrant Tsukiji Outer Market for street food, then gear up for a legendary night out in Roppongi.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Toyosu Fish Market Tuna Auction',
              description: 'Watch the famous tuna auction from the observation deck at 5:30am. Massive frozen bluefin tuna sell for thousands of dollars in rapid-fire bidding. Then explore the market\'s restaurants for the freshest sushi breakfast you\'ll ever have.',
              details: [
                '⏰ Auction viewing 5:30-6:30am — arrive by 5am',
                '🎫 Free viewing from the observation gallery (limited spots)',
                '🍣 Sushi Dai and Daiwa Sushi are legendary (expect 1-2hr queues)',
                '🚇 Toyosu is on the Yurikamome line'
              ]
            }
          ],
          meals: [
            {
              type: '🍣 Breakfast',
              name: 'Sushi Dai (Toyosu)',
              description: 'The most famous sushi counter in the world. Chef\'s omakase of the morning\'s freshest catch — each piece is a revelation. The queue is brutal but life-changing.',
              meta: '💰 $$ · 📍 Toyosu Market Building 6, 3F · Opens 5am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tsukiji Outer Market Food Crawl',
              description: 'While the inner market moved to Toyosu, the Tsukiji Outer Market is still thriving — a maze of street food stalls, knife shops, and specialty stores. Eat your way through tamagoyaki (sweet omelette), fresh uni, grilled scallops, and mochi.',
              details: [
                '🥚 Tsukimura — famous for dashimaki tamago (rolled omelette on a stick)',
                '🦪 Grilled oysters and scallops for ¥500-800 each',
                '🔪 Aritsugu or Masamoto — legendary knife shops (great souvenirs)',
                '🍡 Freshly pounded mochi and dorayaki'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Roppongi Night Out',
              description: 'Roppongi is Tokyo\'s most international nightlife district. Start with rooftop cocktails, then hit the clubs. It\'s lively, loud, and goes until dawn.',
              details: [
                '🍸 The Bar at the Ritz-Carlton (53F) — jaw-dropping Tokyo Tower views',
                '🎵 V2 Tokyo — massive club with international DJs',
                '🍺 Craft beer fans: try BrewDog Roppongi or Two Dogs Taproom',
                '👨‍👩‍👧‍👦 Family alternative: Tokyo Tower night illumination (closes 11pm)'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Gonpachi Nishi-Azabu',
              description: 'The restaurant that inspired the crazy fight scene in Kill Bill. Dramatic traditional interior with robata grill, soba noodles, and yakitori. Great atmosphere for groups.',
              meta: '💰 $$$ · 📍 1-13-11 Nishi-Azabu, Minato · Book ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6455, lng: 139.7814, label: 'Toyosu Fish Market', num: 1, cat: 'attraction', desc: 'World\'s largest fish market — tuna auction at dawn' },
        { lat: 35.6654, lng: 139.7707, label: 'Tsukiji Outer Market', num: 2, cat: 'food', desc: 'Street food paradise — omelettes, uni, grilled scallops' },
        { lat: 35.6627, lng: 139.7312, label: 'Roppongi', num: 3, cat: 'nightlife', desc: 'International nightlife district — clubs and rooftop bars' },
        { lat: 35.6586, lng: 139.7454, label: 'Tokyo Tower', num: 4, cat: 'attraction', desc: 'Iconic tower — beautiful night illumination' },
        { lat: 35.6569, lng: 139.7260, label: 'Gonpachi Nishi-Azabu', num: 5, cat: 'food', desc: 'The "Kill Bill" restaurant — dramatic interior' },
        { lat: 35.6455, lng: 139.7814, label: 'Sushi Dai', num: 6, cat: 'food', desc: 'World-famous sushi counter at Toyosu' }
      ]
    },
    {
      num: 5,
      date: '2026-03-27',
      neighborhoods: 'Fushimi Inari · Higashiyama · Gion',
      title: 'Bullet Train to Kyoto — Gates, Geisha & Tea',
      description: 'Board the shinkansen to Kyoto! Start with the mesmerizing tunnels of Fushimi Inari, wander through Higashiyama\'s preserved streets, and end in the geisha district of Gion — where you might spot a real maiko at dusk.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinkansen to Kyoto',
              description: 'Take the Nozomi bullet train from Tokyo Station to Kyoto — 2 hours 15 minutes of smooth, silent speed at 300km/h. Grab an ekiben (train bento) from the station for the ride.',
              details: [
                '🚄 Nozomi: ~2h15m, ¥13,320 (or use JR Pass on Hikari: ~2h40m)',
                '🍱 Tokyo Station has amazing ekiben — try the Tokyo Bento at Ekibenya Matsuri',
                '🗻 Sit on the right side (seats D/E) for Mt. Fuji views around Shin-Fuji station'
              ]
            },
            {
              title: 'Fushimi Inari Taisha',
              description: 'Thousands of vermillion torii gates snake up the mountainside in an endless tunnel of orange. It\'s Japan\'s most iconic image and even more breathtaking in person. The full hike to the summit takes 2-3 hours, but even 30 minutes in is magical.',
              details: [
                '⛩️ Free entry · Open 24/7',
                '🥾 Full summit hike: ~4km, 2-3 hours round trip',
                '📸 The deep gates area (halfway up) is less crowded for photos',
                '🦊 Kitsune (fox) statues guard the shrine — they\'re messengers of Inari'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Higashiyama District Walking Tour',
              description: 'Kyoto\'s best-preserved historic district. Stone-paved lanes wind between wooden machiya townhouses, tea shops, and temples. Walk from Kiyomizu-dera down through Sannen-zaka and Ninnen-zaka — the most photogenic streets in Japan.',
              details: [
                '🏯 Kiyomizu-dera: ¥400 · Famous wooden stage with city views',
                '🍵 Stop at a tea house on Ninnen-zaka for matcha and wagashi',
                '👘 Kimono rental shops are everywhere — wear one for the full experience!',
                '📸 Yasaka Pagoda is visible from Sannen-zaka — iconic Kyoto photo'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Omen Kodai-ji',
              description: 'Traditional Kyoto udon in a beautiful wooden house near Kodai-ji temple. Their signature cold udon with dipping sauce and seasonal vegetables is simple perfection.',
              meta: '💰 $$ · 📍 Kodai-ji area, Higashiyama · Cash preferred'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Gion — The Geisha District',
              description: 'As lanterns flicker on along Hanami-koji, Gion transforms into a world of quiet elegance. This is where geiko (Kyoto\'s geisha) and maiko (apprentice geisha) still live and work. Walk slowly, observe respectfully, and soak in the atmosphere.',
              details: [
                '🏮 Hanami-koji is the main street — best at dusk',
                '👘 Maiko sightings are most common 5:30-6:30pm heading to engagements',
                '📸 Please don\'t stop or photograph maiko/geiko — they\'re working',
                '🌸 Shirakawa canal area with willows and cherry blossoms is magical at night'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Gion Kappa Restaurant',
              description: 'Affordable kaiseki-inspired dining in the heart of Gion. Multi-course seasonal Japanese cuisine in an intimate machiya townhouse setting. A taste of Kyoto\'s refined culinary tradition without the ¥30,000 price tag.',
              meta: '💰 $$ · 📍 Gion, Higashiyama-ku · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari Taisha', num: 1, cat: 'attraction', desc: '10,000 vermillion torii gates up the mountain' },
        { lat: 34.9949, lng: 135.7850, label: 'Kiyomizu-dera', num: 2, cat: 'attraction', desc: 'Ancient temple with famous wooden stage' },
        { lat: 34.9990, lng: 135.7780, label: 'Sannen-zaka & Ninnen-zaka', num: 3, cat: 'attraction', desc: 'Stone-paved lanes through historic Higashiyama' },
        { lat: 35.0037, lng: 135.7747, label: 'Gion (Hanami-koji)', num: 4, cat: 'attraction', desc: 'Geisha district — lantern-lit elegance' },
        { lat: 34.9982, lng: 135.7816, label: 'Omen Kodai-ji', num: 5, cat: 'food', desc: 'Traditional Kyoto udon in a wooden townhouse' },
        { lat: 35.0035, lng: 135.7754, label: 'Gion Kappa', num: 6, cat: 'food', desc: 'Affordable kaiseki in a machiya' }
      ]
    },
    {
      num: 6,
      date: '2026-03-28',
      neighborhoods: 'Arashiyama · Kinkaku-ji · Nishiki Market',
      title: 'Bamboo, Gold & Kyoto\'s Kitchen',
      description: 'A day of Kyoto\'s greatest hits. Morning in the ethereal bamboo grove of Arashiyama, the dazzling Golden Pavilion at midday, and an afternoon feasting through Nishiki Market — Kyoto\'s 400-year-old food street.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Arashiyama Bamboo Grove',
              description: 'Walk through towering bamboo stalks that creak and sway overhead — it\'s like entering another world. Arrive early (before 8am) to experience it without crowds. The sound of wind through bamboo is one of Japan\'s "100 Soundscapes."',
              details: [
                '🎋 Free · Open 24/7 · Best before 8am for photos',
                '🐒 Iwatayama Monkey Park nearby — wild macaques with city views',
                '🌸 Cherry blossoms along the Katsura River are stunning in late March'
              ]
            },
            {
              title: 'Tenryū-ji Temple & Garden',
              description: 'One of Kyoto\'s most important Zen temples with a garden that\'s been unchanged for 700 years. The borrowed scenery (shakkei) incorporating the Arashiyama mountains into the garden design is masterful.',
              details: [
                '🏯 ¥500 garden, ¥800 with temple buildings',
                '🧘 UNESCO World Heritage Site',
                '🌸 The garden with sakura and the mountain backdrop is breathtaking'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kinkaku-ji (Golden Pavilion)',
              description: 'A Zen temple covered in gold leaf reflecting perfectly in its mirror pond. It\'s one of Japan\'s most iconic sights and genuinely takes your breath away. The garden around it is exquisite in cherry blossom season.',
              details: [
                '✨ ¥500 · 9am-5pm',
                '📸 The reflection shot from across the pond is unmissable',
                '🍵 Matcha and wagashi at the temple tea house'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Nishiki Market Food Crawl',
              description: 'Kyoto\'s 400-year-old "Kitchen" — a covered arcade bursting with food stalls. Graze on samples of pickles, mochi, fresh tofu, grilled seafood, matcha everything, and Kyoto specialties you won\'t find anywhere else.',
              meta: '💰 $–$$ · 📍 Nishiki-koji-dōri · Most stalls 9am-5pm'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Pontocho Alley Dinner',
              description: 'Pontocho is a narrow, atmospheric alley along the Kamo River packed with restaurants — from high-end kaiseki to casual yakitori. In spring, many restaurants open their riverside terraces (kawayuka) overlooking the cherry blossoms.',
              details: [
                '🏮 The alley is magical when lanterns light up at dusk',
                '🍶 Try local sake from Fushimi — Kyoto\'s sake brewing district',
                '🌊 Riverside terrace dining is a quintessential Kyoto experience'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Misoka-an Kawamichi-ya',
              description: 'A 300-year-old soba noodle restaurant in a beautiful traditional building. Their handmade soba with hot or cold dipping sauce is pure Kyoto — understated and extraordinary.',
              meta: '💰 $$ · 📍 Fuyacho-dori, Nakagyo · Since 1718'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0173, lng: 135.6717, label: 'Arashiyama Bamboo Grove', num: 1, cat: 'attraction', desc: 'Towering bamboo forest — otherworldly experience' },
        { lat: 35.0158, lng: 135.6740, label: 'Tenryū-ji Temple', num: 2, cat: 'attraction', desc: '700-year-old Zen garden — UNESCO World Heritage' },
        { lat: 35.0394, lng: 135.7292, label: 'Kinkaku-ji (Golden Pavilion)', num: 3, cat: 'attraction', desc: 'Gold-leaf temple reflected in mirror pond' },
        { lat: 35.0050, lng: 135.7649, label: 'Nishiki Market', num: 4, cat: 'food', desc: '400-year-old food market — Kyoto\'s Kitchen' },
        { lat: 35.0042, lng: 135.7703, label: 'Pontocho Alley', num: 5, cat: 'food', desc: 'Atmospheric riverside dining alley' },
        { lat: 35.0088, lng: 135.7658, label: 'Misoka-an Kawamichi-ya', num: 6, cat: 'food', desc: '300-year-old soba restaurant' }
      ]
    },
    {
      num: 7,
      date: '2026-03-29',
      neighborhoods: 'Osaka · Dōtonbori · Shinsekai · Osaka Castle',
      title: 'Osaka — Street Food Capital & Castle Views',
      description: 'Take the train to Osaka — Japan\'s kitchen. Osaka is louder, funnier, and more food-obsessed than anywhere else in Japan. Gorge on takoyaki and okonomiyaki in Dōtonbori, explore retro Shinsekai, and see Osaka Castle surrounded by cherry blossoms.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Train to Osaka & Osaka Castle',
              description: 'Take the JR Special Rapid from Kyoto to Osaka (30 minutes). Head straight to Osaka Castle — a magnificent fortress surrounded by a moat and 3,000+ cherry trees. The castle grounds in late March are a hanami paradise.',
              details: [
                '🚄 JR Kyoto → Osaka: 30 min, covered by JR Pass',
                '🏯 Castle tower: ¥600 · Museum inside with Toyotomi history',
                '🌸 Nishinomaru Garden: ¥350 — best sakura viewing spot with castle backdrop',
                '📸 The castle + cherry blossoms + moat reflection is *chef\'s kiss*'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Dōtonbori Street Food Marathon',
              description: 'This is it — Japan\'s most famous food street. Neon signs, giant animatronic crabs, and the smell of sizzling batter everywhere. Osaka\'s motto is "kuidaore" — eat until you drop. Challenge accepted.',
              details: [
                '🐙 Takoyaki (octopus balls) — try Creo-Ru or Wanaka for the best',
                '🥞 Okonomiyaki — Mizuno is legendary (expect a queue)',
                '🍢 Kushikatsu (deep-fried skewers) — no double-dipping!',
                '🦀 Kani Dōraku — the place with the giant moving crab sign',
                '🍦 Pablo cheesecake tarts and Rikuro-Ojisan jiggly cheesecake'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Mizuno Okonomiyaki',
              description: 'Osaka\'s most celebrated okonomiyaki restaurant since 1945. Watch the chefs flip the savory pancakes on the teppan right in front of you. The yamaimo-yaki with pork is their signature — crispy outside, fluffy inside.',
              meta: '💰 $$ · 📍 1-4-15 Dōtonbori, Chuo-ku · Expect 30-60min queue'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shinsekai & Tsūtenkaku Tower',
              description: 'Osaka\'s wonderfully retro neighborhood — think 1960s neon signs, kushikatsu joints, and the iconic Tsūtenkaku Tower. It\'s rough around the edges and completely charming. The locals here are the friendliest in Japan.',
              details: [
                '🗼 Tsūtenkaku Tower: ¥900 — retro observation deck with city views',
                '🍢 Kushikatsu Daruma — the most famous deep-fried skewer joint',
                '🎮 Retro game arcades and Janjan Yokocho market street'
              ]
            },
            {
              title: 'Dōtonbori Night Walk',
              description: 'Dōtonbori is even more spectacular at night when the neon explodes. The Glico Running Man sign reflecting in the canal is THE Osaka photo. Grab some late-night takoyaki and soak it all in.',
              details: [
                '📸 Glico Running Man sign — best from Ebisubashi Bridge',
                '🌃 The canal reflections at night are incredible'
              ]
            }
          ],
          meals: [
            {
              type: '🍺 Dinner',
              name: 'Toyo (Shinsekai)',
              description: 'Tiny standing-only seafood stall in Shinsekai famous for its torched tuna and sea urchin. The owner\'s theatrical blowtorch technique is half the experience. Cash only, no seats, unforgettable.',
              meta: '💰 $$ · 📍 2-2-18 Ebisuhigashi, Naniwa-ku · Cash only'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6873, lng: 135.5262, label: 'Osaka Castle', num: 1, cat: 'attraction', desc: 'Magnificent fortress with 3,000+ cherry trees' },
        { lat: 34.6687, lng: 135.5013, label: 'Dōtonbori', num: 2, cat: 'food', desc: 'Japan\'s most famous food street — eat till you drop' },
        { lat: 34.6523, lng: 135.5062, label: 'Shinsekai', num: 3, cat: 'attraction', desc: 'Retro neighborhood with kushikatsu and neon' },
        { lat: 34.6525, lng: 135.5064, label: 'Tsūtenkaku Tower', num: 4, cat: 'attraction', desc: 'Iconic retro tower with city views' },
        { lat: 34.6693, lng: 135.5018, label: 'Mizuno Okonomiyaki', num: 5, cat: 'food', desc: 'Best okonomiyaki in Osaka since 1945' },
        { lat: 34.6525, lng: 135.5058, label: 'Toyo Shinsekai', num: 6, cat: 'food', desc: 'Famous torched tuna and uni street stall' }
      ]
    },
    {
      num: 8,
      date: '2026-03-30',
      neighborhoods: 'Nara · Tōdai-ji · Nara Park · Osaka (Umeda)',
      title: 'Nara Day Trip — Sacred Deer & Giant Buddha',
      description: 'Take a morning trip to Nara — Japan\'s first permanent capital. Friendly wild deer bow for crackers in the park, and Tōdai-ji houses the world\'s largest bronze Buddha inside the world\'s largest wooden building. Return to Osaka for a final farewell feast.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Train to Nara & Nara Park',
              description: 'Nara is just 45 minutes from Osaka by train. Over 1,000 wild sika deer roam freely through the park and temple grounds. Buy shika-senbei (deer crackers, ¥200) and watch them bow politely before taking one. Kids absolutely love this.',
              details: [
                '🚃 JR or Kintetsu from Osaka-Namba: ~45 min',
                '🦌 Over 1,000 deer roam free — they bow for crackers!',
                '🌸 Cherry blossoms in Nara Park are gorgeous in late March',
                '⚠️ Deer can be pushy — hide the crackers until you\'re ready!'
              ]
            },
            {
              title: 'Tōdai-ji Temple & Great Buddha',
              description: 'The Great Buddha Hall is the world\'s largest wooden building, housing a 15-meter bronze Buddha that\'s been here since 752 AD. The scale is almost incomprehensible — you won\'t believe it until you\'re standing in front of it.',
              details: [
                '🏛️ ¥600 · 8am-5pm',
                '🕳️ Try fitting through the pillar hole — said to grant enlightenment!',
                '📸 The Great South Gate (Nandaimon) with its fierce guardian statues is incredible'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Kakinoha Sushi Tanaka',
              description: 'Nara\'s unique specialty — sushi wrapped in persimmon leaves. The leaves naturally preserve and subtly flavor the fish. A 1,300-year-old tradition you can\'t get anywhere else.',
              meta: '💰 $ · 📍 Near Kintetsu Nara Station'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kasuga Taisha Shrine',
              description: 'A Shinto shrine famous for its thousands of stone and bronze lanterns, many covered in moss and dating back centuries. The path through the ancient cryptomeria forest to reach it is hauntingly beautiful.',
              details: [
                '⛩️ ¥500 for inner sanctuary · Main grounds free',
                '🏮 3,000 lanterns — all lit during Mantoro festivals',
                '🌳 The primeval forest surrounding the shrine is a UNESCO site'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to Osaka — Umeda Sky Building',
              description: 'Head back to Osaka and catch sunset from the Umeda Sky Building\'s floating garden observatory. The 360° open-air rooftop gives panoramic views of the city below, and the escalator ride through the glass tube between towers is thrilling.',
              details: [
                '🏙️ ¥1,500 · Open until 9:30pm',
                '🌅 Arrive 1 hour before sunset for the best light',
                '✨ The rooftop floor has luminous stones that glow in the dark'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Ajinoya Okonomiyaki',
              description: 'Another Osaka okonomiyaki institution in Namba. Less touristy than Mizuno but equally legendary among locals. Their modanyaki (okonomiyaki with yakisoba noodles) is the ultimate Osaka farewell meal.',
              meta: '💰 $$ · 📍 1-7-16 Namba, Chuo-ku'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6851, lng: 135.8048, label: 'Nara Park', num: 1, cat: 'attraction', desc: '1,000+ friendly bowing deer' },
        { lat: 34.6890, lng: 135.8399, label: 'Tōdai-ji Temple', num: 2, cat: 'attraction', desc: 'World\'s largest wooden building & giant Buddha' },
        { lat: 34.6812, lng: 135.8498, label: 'Kasuga Taisha', num: 3, cat: 'attraction', desc: '3,000 lanterns in an ancient forest' },
        { lat: 34.7055, lng: 135.4906, label: 'Umeda Sky Building', num: 4, cat: 'attraction', desc: 'Floating garden observatory — sunset views' },
        { lat: 34.6688, lng: 135.5017, label: 'Ajinoya', num: 5, cat: 'food', desc: 'Local-favorite okonomiyaki' },
        { lat: 34.6850, lng: 135.8060, label: 'Kakinoha Sushi Tanaka', num: 6, cat: 'food', desc: 'Nara\'s persimmon leaf sushi' }
      ]
    },
    {
      num: 9,
      date: '2026-03-31',
      neighborhoods: 'Osaka · Kansai International Airport',
      title: 'Departure Day — Last Bites & Sayonara',
      description: 'Your final morning in Japan. Squeeze in one last konbini run, pick up omiyage (souvenirs) at the station, and savor every last moment before heading to Kansai International Airport. Sayonara, Japan — you\'ll be back.',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kuromon Market — Osaka\'s Kitchen',
              description: 'Kuromon Ichiba is Osaka\'s 170-year-old "Kitchen." One final food crawl through stalls selling fresh sashimi, grilled wagyu, strawberries, and uni bowls. The perfect farewell to Japan\'s food capital.',
              details: [
                '🐟 Fresh sashimi and uni bowls from ¥1,000',
                '🥩 Grilled A5 wagyu on a stick — ¥1,500-2,000',
                '🍓 Giant Japanese strawberries — sweet as candy',
                '⏰ Opens 8am — go early for the freshest picks'
              ]
            },
            {
              title: 'Omiyage Shopping',
              description: 'Japanese souvenir culture is an art. Pick up beautifully packaged sweets, matcha Kit-Kats, and local specialties at the station or airport. Tokyo Banana, Yatsuhashi (Kyoto cinnamon mochi), and Osaka\'s Rikuro cheesecake are classic choices.',
              details: [
                '🎁 Department store basement floors (depachika) have the best selection',
                '🍫 Matcha Kit-Kats and regional flavors make great gifts',
                '📦 Everything is beautifully wrapped — Japan takes presentation seriously'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Kuromon Market Stalls',
              description: 'Your farewell breakfast is a greatest hits of everything you\'ve loved — fresh uni, grilled scallops, tamagoyaki, and one last perfect piece of sashimi.',
              meta: '💰 $–$$ · 📍 Kuromon Ichiba Market, Chuo-ku · Opens 8am'
            }
          ],
          tips: [
            { type: 'tip', text: 'Kansai International Airport (KIX) is about 50 minutes from Namba by Nankai Rapi:t express (¥1,450). The train is stylish — shaped like a retro spaceship. Allow 3 hours before international flights.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6690, lng: 135.5087, label: 'Kuromon Market', num: 1, cat: 'food', desc: '170-year-old market — last food crawl' },
        { lat: 34.6647, lng: 135.5014, label: 'Namba Station', num: 2, cat: 'attraction', desc: 'Hub for airport trains and omiyage shopping' },
        { lat: 34.4348, lng: 135.2441, label: 'Kansai International Airport', num: 3, cat: 'attraction', desc: 'KIX — 50 min from Namba by Rapi:t express' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$80–150/night', midrange: '$150–300/night', luxury: '$300–800/night' },
    { category: 'Meals (per person)', budget: '$20–40/day', midrange: '$40–80/day', luxury: '$100–250/day' },
    { category: 'Transport (JR Pass)', budget: '$330/7-day pass', midrange: '$330 + taxis', luxury: '$330 + private cars' },
    { category: 'Activities', budget: '$10–20/day', midrange: '$20–50/day', luxury: '$50–150/day' },
    { category: 'Shinkansen (w/o JR Pass)', budget: 'N/A', midrange: '~$120 each way', luxury: 'Green car: ~$170' },
    { category: '8-Night Total (per person)', budget: '$1,500–2,500', midrange: '$2,500–4,500', luxury: '$5,000–10,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Tokyo Narita (NRT) or Haneda (HND), depart from Osaka Kansai (KIX)', 'Open-jaw flights (arrive Tokyo, depart Osaka) save backtracking — check on Google Flights', 'Narita Express to Shinjuku: ¥3,250, ~80 min', 'Kansai to Namba: Nankai Rapi:t ¥1,450, ~50 min'] },
    { title: '🏨 Where to Stay', items: ['Tokyo: Shinjuku (transit hub, nightlife) or Shibuya (trendy, central)', 'Kyoto: Near Kyoto Station (convenient) or Gion (atmospheric)', 'Osaka: Namba/Dōtonbori (food, nightlife) or Umeda (business, modern)', 'Budget: Business hotels ¥8,000-12,000/night · Mid: ¥15,000-30,000 · Luxury: ¥40,000+'] },
    { title: '🌡️ Late March Weather', items: ['Tokyo: 10-18°C (50-64°F) — layers recommended', 'Kyoto/Osaka: 8-17°C (46-63°F) — slightly cooler', 'Rain is possible — pack a compact umbrella', 'Cherry blossoms are temperature-sensitive — check forecasts for peak bloom'] },
    { title: '💳 Money & Tipping', items: ['Japan is still cash-heavy — carry ¥10,000-20,000 at all times', '7-Eleven and Japan Post ATMs accept international cards', 'NO tipping anywhere — it can actually be considered rude', 'Tax-free shopping at stores displaying "Tax Free" for purchases over ¥5,000'] },
    { title: '📱 Connectivity & Etiquette', items: ['Rent a pocket WiFi or buy an eSIM (Ubigi, Airalo) at the airport', 'Silence phones on trains — talking on the phone is considered very rude', 'Remove shoes when entering temples, traditional restaurants, and ryokan', 'Bow slightly when greeting — it goes a long way'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
