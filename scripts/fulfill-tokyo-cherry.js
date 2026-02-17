const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771293922895_oea1ps',
  email: 'cynthialandon@gmail.com',
  destination: 'Tokyo, Japan',
};

const itineraryData = {
  destination: 'Tokyo, Japan',
  countryEmoji: '🇯🇵',
  title: 'Tokyo in Bloom: Cherry Blossoms, Culture & Creatures',
  subtitle: 'Four days of hanami magic, ancient temples, neighborhood charm, animal cafés, and authentic Japanese experiences — all on a budget',
  description: 'Late March in Tokyo is pure magic. The cherry blossoms are at peak bloom, transforming the city into a pink-and-white wonderland. This itinerary weaves together the best of sakura season with deep cultural immersion — tea ceremonies, temple visits, old-town neighborhood walks — and plenty of adorable animal encounters. From owl cafés in Akihabara to the cat-filled streets of Yanaka, this trip is designed for curious couples who want to experience the real Tokyo without breaking the bank.',
  duration: '4 nights',
  dates: 'Mar 24 – Mar 28, 2026',
  budget: 'Under $1,000',
  pace: 'Moderate',
  bestFor: 'Couples, Culture lovers, Animal enthusiasts',
  highlights: ['Cherry blossom hanami at Ueno Park & Meguro River', 'Cat cafés, owl cafés & hedgehog cafés', 'Tea ceremony in a traditional tea house', 'Senso-ji Temple & Meiji Shrine', 'Yanaka old town neighborhood walk', 'Shimokitazawa vintage village', 'Budget-friendly izakaya dining', 'Relaxing onsen experience'],

  essentials: [
    { title: '🛬 Getting Around', text: 'Get a 72-hour Tokyo Metro pass (¥1,500/~$10) — it covers most of your travel. Supplement with a Suica/Pasmo IC card for JR lines and buses. Tokyo\'s train system is incredibly efficient and English-friendly.' },
    { title: '💵 Money', text: 'Japanese Yen (¥). Japan is still fairly cash-heavy — many small restaurants and cafés are cash-only. Withdraw yen at 7-Eleven ATMs (international cards accepted). Budget ¥8,000-12,000/day per person for food and activities.' },
    { title: '🗣️ Language', text: 'Japanese. English signage is common on transit but rare in local neighborhoods. Google Translate\'s camera mode is a lifesaver for menus. Learn basic phrases: sumimasen (excuse me), arigatou (thank you), oishii (delicious).' },
    { title: '🌸 Cherry Blossom Season', text: 'Late March is prime sakura season! Peak bloom (mankai) typically hits Tokyo March 25-31. Bring a picnic blanket for hanami. Best spots: Ueno Park, Meguro River, Chidorigafuchi, Shinjuku Gyoen. Evenings have magical yozakura (night-lit blossoms).' },
    { title: '🐾 Animal Cafés', text: 'Tokyo has cafés for every creature — cats, owls, hedgehogs, rabbits, even otters. Most charge ¥1,000-1,500 (~$7-10) for 30-60 minutes including a drink. Book popular ones online. Be gentle and follow staff instructions.' },
    { title: '🔒 Safety', text: 'Tokyo is one of the safest major cities in the world. Trains run until ~midnight. Convenience stores (konbini) are 24/7 lifelines for snacks, cash, and essentials. Tap water is safe to drink.' },
  ],

  days: [
    // DAY 1 — Asakusa, Ueno & Cherry Blossoms
    {
      num: 1,
      title: 'Temples, Cherry Blossoms & Ueno\'s Wonders',
      description: 'Start with Tokyo\'s most iconic temple, then spend the afternoon under a canopy of cherry blossoms in Ueno Park — one of the city\'s best hanami spots.',
      neighborhoods: 'Asakusa · Ueno',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Senso-ji Temple & Nakamise-dori',
              description: 'Tokyo\'s oldest and most visited temple is stunning in cherry blossom season. Walk through the iconic Kaminarimon (Thunder Gate), browse the traditional snack stalls on Nakamise-dori, and explore the temple grounds. Arrive early to beat crowds.',
              details: ['📍 2-3-1 Asakusa, Taito-ku', '🕐 Temple grounds open 24hrs · Main hall 6am-5pm · Free', '💡 Try ningyo-yaki (custard-filled cakes) and age-manju (fried sweet buns) on Nakamise-dori — ¥100-300 each']
            },
            {
              title: 'Asakusa Backstreets Walk',
              description: 'Wander west of Senso-ji into the quieter backstreets. Discover Hoppy Street (Hoppy-dori) lined with tiny izakayas, the charming Denboin-dori shopping street, and views of Tokyo Skytree across the Sumida River.',
              details: ['💡 Hoppy Street comes alive in the evening — earmark it for a future night out or grab a cheap morning coffee here']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Sometaro (染太郎)',
              description: 'A beloved okonomiyaki (savory pancake) restaurant in a charming old wooden house near Senso-ji. You cook your own at the table — a fun, interactive experience for couples.',
              meta: '📍 2-2-2 Nishi-Asakusa, Taito-ku · 💰 ¥800-1,200/person · Cash only'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Senso-ji is beautiful but packed by 10am. Arrive by 7-8am for peaceful photos with cherry blossoms framing the pagoda.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Ueno Park Hanami 🌸',
              description: 'One of Tokyo\'s most famous cherry blossom spots with over 1,000 trees. Grab snacks and drinks from nearby konbini, lay down a picnic blanket, and join thousands of locals celebrating hanami. The main path becomes a tunnel of pink blossoms.',
              details: ['📍 Uenokoen, Taito-ku · Free', '💡 Pick up a blue tarp (¥100 at Daiso), bento boxes and drinks from the Lawson or 7-Eleven near Ueno Station', '🌸 The path between Keisei Ueno Station and the National Museum is the prime sakura corridor']
            },
            {
              title: 'Ueno Zoo',
              description: 'Japan\'s oldest zoo is right inside Ueno Park. Home to giant pandas, red pandas, gorillas, and a wonderful variety of animals. A must for animal lovers and a perfect complement to your hanami afternoon.',
              details: ['📍 9-83 Uenokoen, Taito-ku', '🕐 9:30am-5pm (last entry 4pm) · Closed Mondays', '💰 ¥600/person (~$4) — one of Tokyo\'s best budget attractions', '🐼 Giant pandas Xiao Xiao and Lei Lei are the stars!']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ameyoko Street Food & Izakaya',
              description: 'The bustling Ameyoko market street near Ueno Station transforms in the evening. Grab yakitori skewers, fresh seafood, and cheap beer from the standing bars and tiny izakayas that line the alley.',
              meta: '📍 Ameyoko, Ueno, Taito-ku · 💰 ¥1,500-2,500/person · Mix of cash and card'
            }
          ],
          tips: [
            { type: 'tip', text: '🌸 If blossoms are peaking, return to Ueno Park after dark for yozakura — the trees are illuminated along the main path until 8pm.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7148, lng: 139.7967, label: 'Senso-ji Temple', num: 1, cat: 'attraction', desc: 'Tokyo\'s oldest temple — iconic Thunder Gate and Nakamise-dori' },
        { lat: 35.7131, lng: 139.7923, label: 'Sometaro Okonomiyaki', num: 2, cat: 'restaurant', desc: 'Cook-your-own okonomiyaki in a charming old house' },
        { lat: 35.7146, lng: 139.7732, label: 'Ueno Park', num: 3, cat: 'attraction', desc: 'Prime cherry blossom hanami with 1,000+ trees' },
        { lat: 35.7164, lng: 139.7713, label: 'Ueno Zoo', num: 4, cat: 'attraction', desc: 'Japan\'s oldest zoo — pandas, red pandas & more' },
        { lat: 35.7085, lng: 139.7745, label: 'Ameyoko Market', num: 5, cat: 'restaurant', desc: 'Bustling market street with street food and izakayas' }
      ]
    },

    // DAY 2 — Meiji Shrine, Harajuku, Shimokitazawa & Cat Café
    {
      num: 2,
      title: 'Shrines, Street Style & Feline Friends',
      description: 'From the serene forest of Meiji Shrine to the creative chaos of Harajuku and the vintage charm of Shimokitazawa — plus your first animal café encounter.',
      neighborhoods: 'Harajuku · Shibuya · Shimokitazawa',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Meiji Shrine (Meiji Jingū)',
              description: 'Walk through the towering torii gate into the forested grounds of Tokyo\'s most important Shinto shrine, dedicated to Emperor Meiji. The 170-acre forest feels like another world — a profound contrast to the surrounding city. Write a wish on an ema (wooden prayer tablet).',
              details: ['📍 1-1 Yoyogikamizonocho, Shibuya-ku', '🕐 Sunrise to sunset · Free', '💡 Buy an ema tablet (¥500) and write your wish — a beautiful ritual for couples']
            },
            {
              title: 'Harajuku & Takeshita Street',
              description: 'Step from ancient Japan into Tokyo\'s most colorful youth culture hub. Takeshita Street is a sensory overload of crepe shops, kawaii fashion, and people-watching. Wander into the backstreets of Ura-Harajuku for quieter vintage shops and cafés.',
              details: ['📍 Takeshita-dori, Jingumae, Shibuya-ku', '💡 Try a Harajuku crepe (¥400-600) — the strawberry and cream is iconic']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Afuri Ramen (Harajuku)',
              description: 'Famous for their yuzu shio (citrus salt) ramen — lighter and more refreshing than heavy tonkotsu. A perfect bowl after a morning of walking. Often has a line, but it moves fast.',
              meta: '📍 1-1-7 Ebisu, Shibuya-ku (Harajuku branch) · 💰 ¥1,000-1,300/person'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Shimokitazawa Exploration',
              description: 'Take the Keio-Inokashira line 2 stops from Shibuya to Shimokitazawa — Tokyo\'s beloved bohemian neighborhood. Wander through vintage clothing shops, independent bookstores, record shops, and cozy coffee spots. The recently redeveloped area under the tracks (Shimokita Ekiue) has great shops and cafés.',
              details: ['📍 Shimokitazawa Station, Setagaya-ku', '💡 Check out Shimokita Ekiue and Bonus Track — a curated collection of indie shops and eateries', '🛍️ New York Joe Exchange and Stick Out for vintage finds']
            },
            {
              title: 'Cat Café Cateriam (Shimokitazawa)',
              description: 'One of Shimokitazawa\'s coziest cat cafés with ~15 friendly rescue cats. Curl up on floor cushions, sip your included drink, and let the cats come to you. A calm, intimate experience far from the touristy cat cafés.',
              details: ['📍 Shimokitazawa area, Setagaya-ku', '💰 ¥1,100 for 60 minutes including one drink', '🕐 11am-9pm · No reservation needed on weekdays', '🐱 All cats are rescues — the café supports local TNR programs']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Shirube (しるべ) Izakaya',
              description: 'A cozy Shimokitazawa izakaya with a handwritten menu of daily specials. This is the real izakaya experience — tiny, lively, and packed with locals. Try the yakitori, potato salad, and edamame with a nama biiru (draft beer).',
              meta: '📍 Shimokitazawa, Setagaya-ku · 💰 ¥2,000-3,000/person with drinks'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Shimokitazawa is best explored by just wandering. Get lost in the side streets — that\'s where the magic is.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6764, lng: 139.6993, label: 'Meiji Shrine', num: 1, cat: 'attraction', desc: 'Tokyo\'s most important Shinto shrine in a 170-acre forest' },
        { lat: 35.6702, lng: 139.7026, label: 'Takeshita Street', num: 2, cat: 'attraction', desc: 'Iconic Harajuku youth culture and kawaii fashion street' },
        { lat: 35.6619, lng: 139.7101, label: 'Afuri Ramen', num: 3, cat: 'restaurant', desc: 'Famous yuzu shio ramen — light and refreshing' },
        { lat: 35.6614, lng: 139.6682, label: 'Shimokitazawa', num: 4, cat: 'attraction', desc: 'Bohemian neighborhood with vintage shops and indie cafés' },
        { lat: 35.6608, lng: 139.6690, label: 'Cat Café Cateriam', num: 5, cat: 'attraction', desc: 'Cozy rescue cat café with ~15 friendly cats' },
        { lat: 35.6620, lng: 139.6675, label: 'Shirube Izakaya', num: 6, cat: 'restaurant', desc: 'Authentic local izakaya with handwritten daily specials' }
      ]
    },

    // DAY 3 — Yanaka, Owl Café, Tea Ceremony & Onsen
    {
      num: 3,
      title: 'Old Tokyo, Owls & Onsen Bliss',
      description: 'Discover the nostalgic charm of Yanaka — Tokyo\'s best-preserved old neighborhood — meet owls up close, experience a traditional tea ceremony, and melt your worries away in a soothing onsen.',
      neighborhoods: 'Yanaka · Akihabara · Bunkyo',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Yanaka Old Town Walk',
              description: 'Step back in time in Yanaka — a neighborhood that survived WWII bombing and retains its pre-war atmosphere. Stroll down Yanaka Ginza shopping street, visit the ancient Yanaka Cemetery (a hidden cherry blossom gem!), and discover tiny temples, traditional sweet shops, and friendly stray cats that roam the streets.',
              details: ['📍 Yanaka, Taito-ku (start from Nippori Station)', '💡 Yanaka Cemetery has a stunning cherry blossom tunnel — a locals-only hanami secret', '🐱 Yanaka is known as Tokyo\'s "cat town" — look for cat-themed shops and actual neighborhood cats', '🍡 Try the handmade menchi katsu (fried meat croquette) at a Yanaka Ginza shop — ¥200']
            },
            {
              title: 'SCAI The Bathhouse',
              description: 'A contemporary art gallery inside a 200-year-old public bathhouse. Free admission and a fascinating blend of old and new Japan. Check their website for current exhibitions.',
              details: ['📍 6-1-23 Yanaka, Taito-ku', '🕐 12pm-6pm · Closed Sun-Mon · Free']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Kayaba Coffee (カヤバ珈琲)',
              description: 'A beautifully restored 1916 wooden building that serves as a café and community gathering spot. Famous for their egg sandwich (tamago sando) and thick-cut toast with homemade jam. Pure nostalgic Yanaka vibes.',
              meta: '📍 6-1-29 Yanaka, Taito-ku · 💰 ¥600-900/person · Cash preferred'
            }
          ],
          tips: [
            { type: 'tip', text: '🐱 Count the cats! Yanaka is Tokyo\'s unofficial cat district — see how many real cats (and cat statues) you can spot.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Owl Café Fukurou no Mise (Akihabara)',
              description: 'One of Tokyo\'s most popular owl cafés, home to around 20 owls of different species. Staff guide you through interacting with the owls — you can hold them on your arm and take photos. A surreal, unforgettable experience.',
              details: ['📍 4-5-8 Sotokanda, Chiyoda-ku (Akihabara)', '💰 ¥1,500/person for 60 minutes', '🕐 Book online in advance — this place fills up fast', '🦉 Be calm and gentle. Owls are sensitive to noise and sudden movements.']
            },
            {
              title: 'Tea Ceremony Experience at Shizu-Kokoro',
              description: 'Experience a traditional Japanese tea ceremony (chado) in an intimate tatami room. An English-speaking tea master guides you through the meditative ritual of preparing and drinking matcha. Learn about wabi-sabi philosophy and the centuries-old art of tea.',
              details: ['📍 Various locations in central Tokyo — book online', '💰 ¥2,000-3,000/person for a 60-minute experience', '💡 Wear socks (no bare feet on tatami). Kneel on the cushion — don\'t worry, the teacher will guide you through everything.']
            }
          ],
          meals: [],
          tips: [
            { type: 'tip', text: '💡 Book your owl café and tea ceremony slots at least a few days in advance — especially during cherry blossom season when tourism peaks.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Spa LaQua Onsen',
              description: 'A modern natural hot spring complex in the heart of Tokyo, fed by real underground springs from 1,700m deep. Multiple indoor and outdoor baths, saunas, and relaxation areas. The perfect way to soak away a day of walking. Note: tattoo-friendly onsen — a rarity in Japan.',
              details: ['📍 1-1-1 Kasuga, Bunkyo-ku (Tokyo Dome City)', '💰 ¥2,900/person · Open 11am-9am (next day)', '♨️ Separate bathing areas for men and women (nude bathing). Bring or rent a towel.', '💡 The outdoor rotenburo (open-air bath) is magical at night with Tokyo\'s skyline glowing around you']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Tokyo Dome City Food Court & Izakaya',
              description: 'After your onsen, explore the restaurants around Tokyo Dome City. Plenty of budget-friendly options from ramen to tonkatsu to izakaya sets.',
              meta: '📍 Tokyo Dome City, Bunkyo-ku · 💰 ¥1,000-2,000/person'
            }
          ],
          tips: [
            { type: 'tip', text: '♨️ Japanese onsen etiquette: Wash thoroughly before entering the bath. Don\'t put towels in the water. Be quiet and relaxed. It\'s nude bathing — embrace it!' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.7265, lng: 139.7672, label: 'Yanaka Ginza', num: 1, cat: 'attraction', desc: 'Nostalgic old-town shopping street with cats and traditional shops' },
        { lat: 35.7250, lng: 139.7698, label: 'Yanaka Cemetery', num: 2, cat: 'attraction', desc: 'Hidden cherry blossom tunnel — a locals-only hanami gem' },
        { lat: 35.7258, lng: 139.7680, label: 'Kayaba Coffee', num: 3, cat: 'restaurant', desc: 'Restored 1916 café — famous tamago sando and thick toast' },
        { lat: 35.6983, lng: 139.7713, label: 'Owl Café Fukurou no Mise', num: 4, cat: 'attraction', desc: 'Hold and interact with ~20 owls of different species' },
        { lat: 35.7080, lng: 139.7520, label: 'Tea Ceremony', num: 5, cat: 'attraction', desc: 'Traditional matcha tea ceremony with English-speaking master' },
        { lat: 35.7076, lng: 139.7538, label: 'Spa LaQua', num: 6, cat: 'attraction', desc: 'Natural hot spring onsen with outdoor baths and city views' }
      ]
    },

    // DAY 4 — Shinjuku Gyoen, Hedgehog Café, Meguro River & Farewell
    {
      num: 4,
      title: 'Sakura Finale & Tiny Hedgehogs',
      description: 'Your final day brings Tokyo\'s two most beautiful cherry blossom spots, an impossibly cute hedgehog café, and a magical evening stroll along the Meguro River.',
      neighborhoods: 'Shinjuku · Roppongi · Meguro',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Shinjuku Gyoen National Garden 🌸',
              description: 'Tokyo\'s most beautiful park and arguably the best hanami spot in the city. 1,000+ cherry trees across Japanese, English, and French formal gardens. The spacious lawns mean you can always find a spot to sit. Alcohol is banned here, making it a calmer alternative to Ueno Park.',
              details: ['📍 11 Naitomachi, Shinjuku-ku', '🕐 9am-5:30pm (last entry 5pm) · Closed Mondays', '💰 ¥500/person (~$3.50)', '🌸 The Somei Yoshino cherries along the central lawn are the star attraction. The Japanese Garden section has weeping cherries that bloom slightly later.', '💡 Enter from the Shinjuku Gate (closest to station) — arrive by 9am to enjoy it before crowds build']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Fuunji Tsukemen (風雲児)',
              description: 'One of Tokyo\'s most acclaimed tsukemen (dipping ramen) shops, just a 5-minute walk from Shinjuku Station. Rich, thick fish-and-pork broth with perfectly chewy noodles. Worth the wait in line.',
              meta: '📍 2-14-3 Yoyogi, Shibuya-ku · 💰 ¥900-1,100/person · Cash only · Expect 15-30 min queue'
            }
          ],
          tips: [
            { type: 'tip', text: '📸 Shinjuku Gyoen photography tip: The reflection of cherry blossoms in the Japanese Garden pond is the money shot. Morning light is best.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Harry Hedgehog Café (Roppongi)',
              description: 'Meet adorable tiny hedgehogs! Pick them up gently with gloves, watch them curl into little balls, and fall completely in love. This is Tokyo\'s most popular hedgehog café, with well-cared-for animals and friendly English-speaking staff.',
              details: ['📍 6-7-2 Roppongi, Minato-ku', '💰 ¥1,400/person for 30 minutes', '🕐 12pm-7pm · Book online recommended', '🦔 Hedgehogs are calmest in the afternoon. Be gentle — they\'re sensitive to noise and fast movements.']
            },
            {
              title: 'Chidorigafuchi Cherry Blossoms by Boat 🌸',
              description: 'Rent a rowboat on the moat surrounding the Imperial Palace and drift beneath a tunnel of cherry blossoms. This is one of Tokyo\'s most romantic sakura experiences — the pink petals floating on the water create a dreamlike scene.',
              details: ['📍 2 Kudanminami, Chiyoda-ku', '💰 ¥800 per boat for 30 minutes', '🕐 Boats available 9:30am-8pm during cherry blossom season', '⚠️ Lines can be 1-2 hours at peak times — go on a weekday or arrive early/late']
            }
          ],
          meals: [],
          tips: [
            { type: 'tip', text: '💡 If the Chidorigafuchi boat line is too long, walk the promenade path instead — it\'s equally beautiful and free.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Meguro River Cherry Blossoms 🌸',
              description: 'The most magical cherry blossom experience in Tokyo. Over 800 trees line both sides of the Meguro River, creating a sakura tunnel for nearly 4 kilometers. During peak season, the trees are illuminated at night, and the petals drift into the river like pink snow. Street food vendors line the banks.',
              details: ['📍 Meguro River, Meguro-ku (walk from Naka-Meguro Station)', '💡 The best section is between Naka-Meguro and Ikejiri-Ohashi stations', '🌸 Night illumination is typically 5pm-9pm during peak bloom', '🍺 Grab a beer and yakitori from the street vendors and stroll along the river — this is Tokyo\'s best yozakura']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Naka-Meguro Izakaya Hopping',
              description: 'The streets around Naka-Meguro station are lined with intimate izakayas, wine bars, and casual restaurants. Find a cozy spot, order some sake and yakitori, and toast to an incredible trip under the cherry blossoms.',
              meta: '📍 Naka-Meguro area, Meguro-ku · 💰 ¥2,000-3,500/person with drinks'
            }
          ],
          tips: [
            { type: 'tip', text: '🌸 The Meguro River at night during peak bloom is genuinely one of the most beautiful things you will ever see. Don\'t rush it.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.6852, lng: 139.7100, label: 'Shinjuku Gyoen', num: 1, cat: 'attraction', desc: '1,000+ cherry trees in stunning formal gardens' },
        { lat: 35.6836, lng: 139.7020, label: 'Fuunji Tsukemen', num: 2, cat: 'restaurant', desc: 'Top-rated tsukemen dipping ramen near Shinjuku' },
        { lat: 35.6610, lng: 139.7312, label: 'Harry Hedgehog Café', num: 3, cat: 'attraction', desc: 'Hold adorable hedgehogs — Tokyo\'s cutest animal café' },
        { lat: 35.6938, lng: 139.7500, label: 'Chidorigafuchi', num: 4, cat: 'attraction', desc: 'Rowboat through cherry blossom tunnel on Imperial Palace moat' },
        { lat: 35.6440, lng: 139.6988, label: 'Meguro River', num: 5, cat: 'attraction', desc: '800+ illuminated cherry trees along 4km of river — peak yozakura' },
        { lat: 35.6441, lng: 139.6990, label: 'Naka-Meguro Izakayas', num: 6, cat: 'restaurant', desc: 'Farewell izakaya dinner in Tokyo\'s trendiest neighborhood' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (4 nights)', low: '$200', mid: '$320', high: '$480', notes: 'Hostels/budget hotels for 2' },
    { category: 'Food & Drinks', low: '$160', mid: '$240', high: '$320', notes: 'Mix of street food, ramen, izakaya' },
    { category: 'Transport', low: '$30', mid: '$45', high: '$60', notes: '72hr metro pass + IC card top-ups' },
    { category: 'Activities & Cafés', low: '$60', mid: '$90', high: '$120', notes: 'Animal cafés, tea ceremony, onsen, gardens' },
    { category: 'Souvenirs & Misc', low: '$20', mid: '$40', high: '$60', notes: 'Omiyage, konbini snacks, extras' },
    { category: 'TOTAL (2 people)', low: '$470', mid: '$735', high: '$1,040', notes: 'Easily under $1,000 at moderate pace' }
  ],

  practicalInfo: [
    { title: '🏨 Where to Stay', items: ['Stay in <strong>Asakusa</strong> (close to Senso-ji, great metro access) or <strong>Shinjuku</strong> (central hub)', '<strong>Khaosan Tokyo Origami</strong> (Asakusa) — ~$40/night double room', '<strong>Unplan Shinjuku</strong> — ~$50/night, stylish hostel with private rooms', '<strong>Mustard Hotel Shimokitazawa</strong> — ~$60/night, boutique feel', '⚠️ Book early — cherry blossom season fills up fast!'] },
    { title: '✈️ Getting from the Airport', items: ['<strong>From Narita:</strong> Keisei Skyliner to Ueno (36 min, ¥2,520) or Access Express (55 min, ¥1,270)', '<strong>From Haneda:</strong> Tokyo Monorail or Keikyu Line (20-30 min, ¥500-650)', 'Both airports have luggage delivery services to your hotel (¥2,000-3,000)'] },
    { title: '📱 Connectivity', items: ['Rent a pocket Wi-Fi at the airport (¥500-900/day)', 'Or buy an eSIM before departure — Ubigi or Airalo (~$5-10 for the trip)', 'Free Wi-Fi at most konbini, stations, and cafés but unreliable'] },
    { title: '🎌 Etiquette Basics', items: ['Don\'t tip — it\'s considered rude in Japan', 'Bow slightly when greeting people', 'Don\'t eat while walking (except at festivals/street food areas)', 'Be quiet on trains — no phone calls, low voices', 'Remove shoes when entering homes, temples, and some restaurants', 'Queue politely — the Japanese are masters of orderly lines'] },
    { title: '🌸 Cherry Blossom Tracker', items: ['Check Japan Meteorological Corporation\'s sakura forecast at <strong>sakura.weathermap.jp</strong>', 'Peak bloom shifts year to year — typically late March for Tokyo', 'You may luck into full bloom or catch early/late stages — all are beautiful!'] }
  ]
};

// Run fulfillment
try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfillment complete!');
  console.log('URL:', result.url);
  console.log('Slug:', result.slug);
  console.log('Email sent:', result.emailSent);
} catch (err) {
  console.error('❌ Fulfillment failed:', err.message);
  process.exit(1);
}
