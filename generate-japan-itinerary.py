#!/usr/bin/env python3
# Generate the Japan itinerary fulfillment script

content = r'''const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1776178142375_dvmst2',
  email: 'chan2471998@gmail.com',
  destination: 'Osaka, Kyoto, Tokyo',
};

const itineraryData = {
  destination: 'Osaka, Kyoto & Tokyo, Japan',
  countryEmoji: '🇯🇵',
  title: "Japan's Golden Route: Osaka, Kyoto & Tokyo",
  subtitle: 'Sixteen days through Japan\'s culinary capital, ancient imperial capital, and neon metropolis — autumn foliage, street food, temple mornings, and city nights for two',
  description: 'Japan in late November is a tapestry of burnt oranges, crisp air, and unforgettable flavor. This 16-day journey begins in Osaka — Japan\'s kitchen — where neon-lit Dotonbori streets sizzle with takoyaki and okonomiyaki, and Osaka Castle grounds glow with autumn color. From there, Kyoto\'s ancient temple corridors and bamboo groves unfold over six meditative days, with peak fall foliage illuminating every stone pathway. The trip closes in electric Tokyo, where golden ginkgo avenues, teamLab\'s digital art gardens, and world-class sushi rounds out this most complete Japanese experience.',
  duration: '16 days / 15 nights',
  dates: 'November 14 – November 29, 2026',
  budget: '$5,000 – $9,000 for two',
  pace: 'Moderate — full days with evenings free',
  bestFor: 'Couples, Culture lovers, Foodies, First-time Japan visitors',
  highlights: [
    'Dotonbori neon lights & Osaka street food',
    'Osaka Castle autumn foliage',
    'Fushimi Inari thousand torii gates at dawn',
    'Arashiyama bamboo grove',
    'Kiyomizudera temple with autumn views',
    'Gion evening geisha district walk',
    'Kyoto Nishiki Market',
    'Golden Pavilion (Kinkaku-ji)',
    "Philosopher's Path in autumn",
    "Tokyo's Meiji Jingu & Harajuku",
    'teamLab Planets immersive art',
    'Tsukiji Outer Market breakfast',
    'Shibuya Crossing & Shibuya Sky views',
    'Senso-ji temple in Asakusa',
    'Mount Fuji day trip from Kawaguchiko'
  ],
  essentials: [
    { title: '🛬 Getting Around Japan', text: 'Get a Japan Rail (JR) Pass before arriving — covers Shinkansen between Osaka, Kyoto, and Tokyo, plus all JR local trains. A 14-day JR Pass (¥47,250/person) is ideal.' },
    { title: '💵 Money', text: 'Japanese Yen (JPY). Cards accepted at most hotels and restaurants. Cash still reigns for street food, small restaurants, temples, and local shops — carry ¥10,000-15,000/person/day outside major cities. 7-Eleven and Japan Post Bank ATMs accept foreign cards.' },
    { title: '🗣️ Language', text: 'Japanese. English spoken at major stations, hotels, and tourist restaurants. Learn essentials: Konnichiwa (hello), Arigatou gozaimasu (thanks). Google Translate\'s camera mode is invaluable for menus.' },
    { title: '🌦️ Weather in November', text: 'Cool and dry across all three cities. Osaka/Kyoto: 10-18°C. Tokyo: 7-17°C. Layer with a light down jacket, sweater, and scarf. Comfortable walking shoes essential. An umbrella for light rain.' },
    { title: '🍽️ Dining Culture', text: 'Reservations recommended for kaiseki and Michelin-starred sushi. Counter seating is common — solo dining is normal. Tipping is not practiced. Say "itadakimasu" before eating, "gochisousama" after.' },
    { title: '🗺️ IC Card (Suica/Pasmo)', text: 'Get a Suica or Pasmo IC card at any train station — load with ¥3,000-5,000. Works on every metro, bus, and convenience store in Tokyo, Kyoto, and Osaka.' },
    { title: '📱 Connectivity', text: 'Get a data SIM or eSIM at the airport (Mobal, Docomo tourist SIMs from ¥3,000 for 15 days). Google Maps and Hyperdia are essential train apps.' },
    { title: '🔒 Safety', text: 'Japan is one of the world\'s safest countries. Violent crime is extremely rare. Normal urban awareness applies. Solo travelers feel completely safe walking at night.' },
  ],

  days: [

    // DAY 1 — November 14: Arrival in Osaka
    {
      num: 1,
      date: 'November 14, 2026',
      title: 'Welcome to Osaka: Japan\'s Kitchen',
      description: 'Arrive in Osaka and ease into the city\'s electric energy. After settling in, dive straight into Dotonbori — the neon-drenched food district where Osaka\'s legendary street food culture comes alive.',
      neighborhoods: 'Namba · Dotonbori · Chuo-ku',
      timeBlocks: [
        {
          label: 'Morning / Arrival',
          activities: [
            {
              title: 'Arrive at Kansai International Airport (KIX)',
              description: 'KIX is Osaka\'s main international gateway. Take the Haruka Express to Shin-Osaka Station (75 min, ¥1,910) or Nankai Railway to Namba (45-65 min, ¥930). Collect your JR Pass at the airport. Get a Suica/Pasmo IC card at the station.',
              details: ['📍 Kansai International Airport (KIX)', '🕐 Trains run 5am-midnight', '💡 Buy a Nankai 1-Day Pass (¥840) if arriving early']
            },
            {
              title: 'Check In & Freshen Up',
              description: 'Check into your hotel in the Namba or Dotonbori area — central to everything. Drop bags, adjust to the time change.',
              details: ['📍 Recommended areas: Dotonbori, Namba, or Yotsubashi']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: '7-Eleven / Lawson Convenience Store',
              description: 'In Japan, convenience stores are a gourmet experience. Stop for your first onigiri, tamagoyaki sandwich, or nikuman (steamed pork bun). Essential Japanese food culture.',
              meta: '📍 Any convenience store · 💰 ¥300-600 · 🕐 Open 24 hours'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Osaka\'s metro day pass (¥800) covers unlimited rides — excellent value for a day of sightseeing.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Dotonbori District',
              description: 'Osaka\'s most iconic neighborhood — a canal-side stretch of neon signs, animated billboards including the famous Glico "Running Man," and an unending parade of food stalls. Walk the canal bridge for the classic Dotonbori photo at dusk.',
              details: ['📍 Dotonbori, Chuo-ku', '🕐 Alive day and night — most vibrant 7pm-11pm', '💡 Best viewpoint: Tazaemon-bashi bridge looking south']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Takoyaki at Aizuya',
              description: 'The quintessential Osaka street food — golf-ball-sized batter balls filled with octopus, pickled ginger, and green onion, grilled crispy outside and molten inside, topped with takoyaki sauce, mayonnaise, bonito flakes, and seaweed.',
              meta: '📍 Dotonbori · 💰 ¥600-1,000 for 8-12 pieces'
            },
            {
              type: '🍽️ Dinner',
              name: 'Okonomiyaki at Mizuno',
              description: 'Osaka\'s savory pancake — thick batter with cabbage, eggs, and your choice of protein, grilled on a hot teppan in front of you. Mizuno near Dotonbori is a local institution since 1945.',
              meta: '📍 1-4-13 Dotonbori, Chuo-ku · 💰 ¥1,000-1,500 · ⭐ Osaka institution'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Osaka\'s rule: "Kuidaore" — eat until you drop. Dotonbori is the spiritual home of this philosophy.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6484, lng: 135.4315, label: 'Kansai International Airport', num: 1, cat: 'transport', desc: "Osaka's main international airport" },
        { lat: 34.6687, lng: 135.4997, label: 'Dotonbori Canal', num: 2, cat: 'neighborhood', desc: "Neon-lit food district — Osaka's culinary heart" },
        { lat: 34.6691, lng: 135.5007, label: 'Takoyaki Aizuya', num: 3, cat: 'restaurant', desc: 'Legendary takoyaki spot' },
        { lat: 34.6687, lng: 135.5008, label: 'Okonomiyaki Mizuno', num: 4, cat: 'restaurant', desc: 'Iconic okonomiyaki since 1945' }
      ]
    },

    // DAY 2 — November 15: Osaka Castle & Umeda
    {
      num: 2,
      date: 'November 15, 2026',
      title: 'Osaka Castle & Umeda Sky Building',
      description: "Explore Osaka's history at the magnificent castle surrounded by peak autumn color, then head to the modern Umeda district for aerial city views and an exceptional kushikatsu dinner in the charming Shinsekai neighborhood.",
      neighborhoods: 'Chuo-ku · Kita-ku · Shinsekai',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Osaka Castle (Osaka-jo)',
              description: 'The iconic 1583 Toyotomi Hideyoshi fortress is a museum inside, but the surrounding Osaka Castle Park is the star in November — the maples and ginkgo trees blaze crimson and gold against the castle\'s golden roof tiles.',
              details: ['📍 1-1 Osakajo, Chuo-ku', '🕐 9am-5pm (¥600) · Castle grounds free', '💡 Arrive at opening to enjoy the park in peaceful morning light']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Park Bench Breakfast',
              description: 'Grab grab-and-go breakfast from a nearby 7-Eleven — melon bread, egg sandwich, and oolong tea — and enjoy it on the castle park benches as morning light filters through the autumn leaves.',
              meta: '📍 Near Osaka Castle · 💰 ¥300-500'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kuromon Ichiba Market',
              description: "Osaka's 'Kitchen Market' — a 170-shop covered arcade selling fresh seafood, grilled eel, wagyu skewers, and Osaka street food. Try fresh uni (sea urchin), grilled scallops, or wagyu beef skewers directly from the stalls.",
              details: ['📍 22-83/chome Kuromon-higashi, Chuo-ku', '🕐 9am-6pm', '💡 Come hungry. Sample everything.']
            },
            {
              title: 'Umeda Sky Building — Floating Garden Observatory',
              description: "The Umeda Sky Building's rooftop observatory sits 173 meters above ground in a dramatic open-air ring. On clear November days, the view stretches to Osaka Bay. One of Japan's most photographed architectural feats.",
              details: ['📍 1-1 Oyodonaka, Kita-ku', '🕐 10am-10:30pm (¥1,500)', '💡 Sunset views are spectacular — book evening tickets in advance']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Fresh Seafood at Kuromon Ichiba',
              description: 'Eat uni nigiri, grilled eel, and Hokkaido scallops directly from market stalls. Vendors will arrange a tray for you to eat standing at the counter.',
              meta: '📍 Kuromon Ichiba · 💰 ¥1,000-2,500 · 🕐 Best before 2pm'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Shinsekai District',
              description: "Osaka's retro charm lives in Shinsekai — a neighborhood built around a 1950s vision of the future. Neon lanterns, the Tsutenkaku tower, and the scent of frying oil from kushikatsu shops line every block. Pure Showa-era nostalgia.",
              details: ['📍 Shinsekai, Naniwa-ku (walkable from Namba)']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Kushikatsu at Yaekatsu',
              description: "Osaka's fried perfection: kushikatsu — skewered meat, vegetables, and seafood, breaded and deep-fried golden. Dip in communal tonkatsu sauce (no double-dipping — use the chopstick end of your skewer). Yaekatsu in Shinsekai has been perfecting this since 1949.",
              meta: '📍 1-2-7 Shinsekai, Naniwa-ku · 💰 ¥1,500-2,500 · 🕐 Open until 11pm'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 After dinner, climb the Tsutenkaku tower (¥700) for neon views of Shinsekai below — pure Showa-era nostalgia.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6833, lng: 135.5258, label: 'Osaka Castle', num: 1, cat: 'attraction', desc: '16th-century castle surrounded by peak autumn color' },
        { lat: 34.6831, lng: 135.5260, label: 'Osaka Castle Park', num: 2, cat: 'attraction', desc: 'Beautiful November maples and ginkgo' },
        { lat: 34.6721, lng: 135.4961, label: 'Kuromon Ichiba Market', num: 3, cat: 'attraction', desc: "Osaka's kitchen market — fresh seafood & street food" },
        { lat: 34.7054, lng: 135.4985, label: 'Umeda Sky Building', num: 4, cat: 'attraction', desc: '173m floating rooftop observatory' },
        { lat: 34.6510, lng: 135.5060, label: 'Shinsekai District', num: 5, cat: 'neighborhood', desc: 'Retro Showa-era neighborhood — kushikatsu & neon' },
        { lat: 34.6508, lng: 135.5063, label: 'Yaekatsu', num: 6, cat: 'restaurant', desc: 'Legendary kushikatsu since 1949' }
      ]
    },

    // DAY 3 — November 16: Nara Day Trip
    {
      num: 3,
      date: 'November 16, 2026',
      title: 'Nara Day Trip: Deer, Temples & Todai-ji',
      description: "Take the 45-minute train to Nara — Japan's ancient capital and home to the country's most approachable wild deer, who bow to visitors and guard the temples with surprising gentleness.",
      neighborhoods: 'Nara City · Todai-ji · Nara Park',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Todai-ji Temple',
              description: "One of Japan's most significant Buddhist temples, founded in 728 AD. The Daibutsu (Great Buddha) inside is one of the largest bronze Buddha statues in the world (15 meters tall). The hall is the world's largest wooden building.",
              details: ['📍 406 Zoshicho, Nara', '🕐 8am-5pm (¥600)', '💡 The approach through the cedar forest from the station is part of the magic']
            },
            {
              title: "Nara's Friendly Deer",
              description: "Nara's fallow deer are sacred messengers of the gods. They roam freely through Nara Park and will bow to you if you bow to them. Buy shika senbei (deer crackers) and feed them — they're enthusiastic beggars.",
              details: ['📍 Nara Park, free to enter', '💡 Hold crackers flat, not in fist. They may headbutt if stingy.']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Naramachi District',
              description: "Wander Naramachi — a former merchant district with narrow lanes, traditional machiya townhouses, and small local restaurants. Try handmade soba or a simple teishoku (set meal).",
              meta: '📍 Naramachi, Nara City · 💰 ¥1,000-1,800'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Kasuga Taisha Shrine',
              description: "Nara's most sacred Shinto shrine, founded in 768 AD. The approach is lined with ancient stone lanterns — over 3,000, many moss-covered. Sits in a UNESCO-listed primeval beech forest. Deep vermillion against green cedars.",
              details: ['📍 160 Kasuganocho, Nara', '🕐 Grounds open 24 hours (¥500 to inner hall)']
            },
            {
              title: "Kofuku-ji & Isui-en Garden",
              description: "Kofuku-ji's five-story pagoda is Nara's most photographed landmark. Isui-en is a classic Japanese strolling garden with a teahouse — particularly beautiful in November with full autumn color.",
              details: ['📍 Kofuku-ji (¥500 museum), Isui-en (¥800)']
            }
          ],
          meals: [
            {
              type: '🍽️ Afternoon Tea',
              name: 'Matcha & Wagashi at a Teahouse',
              description: "After temple-walking, rest at a teahouse near Kasuga Taisha for ceremonial matcha and seasonal wagashi sweet.",
              meta: '📍 Near Kasuga Taisha · 💰 ¥600-1,000'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Return to Osaka by Kintetsu-Nara Line (45 min, ¥760) or JR Nara Line.' }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6889, lng: 135.8398, label: 'Todai-ji Temple', num: 1, cat: 'attraction', desc: 'Home of the Great Buddha — one of the world\'s largest bronze statues' },
        { lat: 34.6851, lng: 135.8430, label: 'Nara Park', num: 2, cat: 'attraction', desc: 'Sacred deer roam freely — feed shika senbei, receive bows' },
        { lat: 34.6904, lng: 135.8348, label: 'Kasuga Taisha Shrine', num: 3, cat: 'attraction', desc: 'Ancient shrine with 3,000+ stone lanterns in primeval forest' },
        { lat: 34.6876, lng: 135.8365, label: 'Kofuku-ji Temple', num: 4, cat: 'attraction', desc: "5-story pagoda — Nara's most iconic landmark" },
        { lat: 34.6895, lng: 135.8313, label: 'Isui-en Garden', num: 5, cat: 'attraction', desc: 'Beautiful Japanese garden with autumn color' },
        { lat: 34.6866, lng: 135.8323, label: 'Naramachi District', num: 6, cat: 'neighborhood', desc: 'Old merchant district with traditional machiya restaurants' }
      ]
    },

    // DAY 4 — November 17: Abeno Harukas & teamLab
    {
      num: 4,
      date: 'November 17, 2026',
      title: "Osaka's Heights & teamLab Botanical Garden",
      description: "Soak in panoramic views from Japan's tallest building, then descend into Osaka's world-class aquarium before closing the day with teamLab's luminous botanical garden.",
      neighborhoods: 'Abeno · Umeda · Osaka Bay',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Abeno Harukas',
              description: "Japan's tallest building (300 meters) with 360-degree views from its open-air rooftop observatory on the 58th-60th floors. On clear November days, the view extends to Osaka Bay and beyond.",
              details: ['📍 1-1-43 Abenosuji, Abeno-ku', '🕐 10am-10pm (¥1,500 adults)', '💡 Sunset tickets sell out — book online in advance']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Tenjinbashi-suji Shopping Street',
              description: "Japan's longest shopping arcade (2km, 600 shops) runs through central Osaka. Pick up warm melon bread or freshly grilled mochi from one of the small local bakeries.",
              meta: '📍 Tenjinbashi-suji, Kita-ku · 💰 ¥300-700'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Osaka Aquarium Kaiyukan',
              description: "One of the world's largest aquariums, built around a massive central tank recreating the Pacific Ocean. Stars: scalloped hammerhead sharks and graceful whale sharks (the largest fish in the sea). Each of the 14 tanks represents a different Pacific Rim region.",
              details: ['📍 1-1-10 Kaigandori, Minato-ku', '🕐 10am-8pm (¥2,400 adults)', '💡 Allow 2-3 hours minimum']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Tempura near Kaiyukan',
              description: 'Near Osaka Bay, intimate tempura restaurants serve pristine seasonal vegetables and seafood — gingko nuts, lotus root, shrimps — battered lightly and fried to order.',
              meta: '📍 Near Kaiyukan, Minato-ku · 💰 ¥2,000-3,500'
            }
          ],
          tips: []
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'teamLab Botanical Garden',
              description: "Osaka's teamLab Botanical Garden transforms a real botanical garden into an immersive digital art experience after dark. Wander through luminous installations — flowers that bloom and dissolve around you, rivers of light, and otherworldly gardens.",
              details: ['📍 Takahashi no Mori, Konohana-ku', '🕐 10am-10pm (¥2,800 adults)', '💡 Wear dark clothing — the installations glow best against dark fabric.']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'On-site teamLab Café',
              description: 'The teamLab botanical garden has a café on-site serving light bistro fare — perfect for eating after your garden walk under the stars.',
              meta: '📍 teamLab Botanical Garden · 💰 ¥1,500-2,500'
            }
          ],
          tips: [
            { type: 'tip', text: "💡 Last night in Osaka — if you have energy, return to Dotonbori for a final takoyaki and canal-side stroll. Kuidaore is the rule." }
          ]
        }
      ],
      mapPins: [
        { lat: 34.6455, lng: 135.5137, label: 'Abeno Harukas', num: 1, cat: 'attraction', desc: "Japan's tallest building — 300m panoramic observatory" },
        { lat: 34.6476, lng: 135.5130, label: 'Tenjinbashi-suji Street', num: 2, cat: 'shopping', desc: "Japan's longest shopping arcade — 2km of local Osaka life" },
        { lat: 34.6544, lng: 135.4289, label: 'Osaka Aquarium Kaiyukan', num: 3, cat: 'attraction', desc: 'World-class aquarium with whale sharks & hammerheads' },
        { lat: 34.6530, lng: 135.4250, label: 'teamLab Botanical Garden', num: 4, cat: 'attraction', desc: 'Immersive digital art in a botanical garden after dark' }
      ]
    },

    // DAY 5 — November 18: Transfer to Kyoto, Fushimi Inari
    {
      num: 5,
      date: 'November 18, 2026',
      title: 'Transfer to Kyoto & Evening at Fushimi Inari',
      description: "Take the direct JR Shinkaisoku rapid train to Kyoto (29 minutes). Then catch Fushimi Inari's iconic vermillion torii gates in afternoon light and stay until dusk.",
      neighborhoods: 'Kyoto Station · Fushimi',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Transfer Osaka → Kyoto',
              description: 'Take the JR Shinkaisoku (special rapid) from Osaka to Kyoto Station — no reservation needed, just hop on. The 29-minute journey runs twice hourly. Kyoto Station is an architectural marvel — the modern glass atrium is striking.',
              details: ['📍 JR Osaka Station → Kyoto Station', '🕐 Every 30 min, ¥850/person with IC card', '💡 JR Pass covers this fully']
            },
            {
              title: 'Check In & Explore Kyoto Station',
              description: "Check into your Kyoto hotel (best locations: Gion, Kawaramachi, or near Kyoto Station). Kyoto Station's 10th floor has excellent food courts including Kyoto Ramen Street.",
              details: ['📍 Kyoto Station Building 10F']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Kyoto Ramen Street',
              description: 'Eight ramen shops representing different regional styles from across Japan. Sample Kyoto\'s lighter shio ramen alongside richer styles.',
              meta: '📍 Kyoto Station Building 10F · 💰 ¥800-1,500'
            }
          ],
          tips: [
            { type: 'tip', text: "💡 Kyoto is significantly more expensive than Osaka. Budget ¥1,500-3,000 per person per day for meals." }
          ]
        },
        {
          label: 'Late Afternoon / Evening',
          activities: [
            {
              title: 'Fushimi Inari Taisha',
              description: "The most iconic Shinto shrine in Japan — famous for its seemingly endless tunnel of 10,000 vermillion torii gates climbing Mount Inari. The hike through the gates takes 2-3 hours round trip. In November, maples at the lower slopes are at peak color.",
              details: ['📍 68 Fukakusa Yabunouchicho, Fushimi-ku', '🕐 Open 24 hours · Free', '💡 Go in late afternoon — day-trippers leave at dusk and it empties beautifully']
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Fushimi Sake District',
              description: "After Fushimi Inari, walk 10 minutes to the Fushimi Sake District — one of Japan's most famous sake-brewing areas with 40+ breweries in an Edo-era canal-side setting. Many offer free tastings.",
              meta: '📍 Fushimi, Kyoto · 💰 Free tastings, ¥500-1,000 for a glass'
            }
          ],
          tips: [
            { type: 'tip', text: "💡 The Hitaki-sai Fire Festival at Fushimi Inari is typically held in November — one of Kyoto's most dramatic festivals." }
          ]
        }
      ],
      mapPins: [
        { lat: 34.9307, lng: 135.7557, label: 'Kyoto Station', num: 1, cat: 'transport', desc: 'Architectural landmark and transport hub' },
        { lat: 34.9671, lng: 135.7727, label: 'Fushimi Inari Taisha', num: 2, cat: 'attraction', desc: '10,000 vermillion torii gates climbing Mount Inari' },
        { lat: 34.9645, lng: 135.7680, label: 'Fushimi Sake District', num: 3, cat: 'attraction', desc: "40+ sake breweries in beautiful Edo-era canal setting" }
      ]
    },

    // DAY 6 — November 19: Arashiyama
    {
      num: 6,
      date: 'November 19, 2026',
      title: 'Arashiyama: Bamboo, Monkeys & Autumn Leaves',
      description: "Western Kyoto's Arashiyama district is a natural wonderland — towering bamboo groves, a scenic river gorge, autumn color everywhere, and a historic trolley train.",
      neighborhoods: 'Arashiyama · Sagano',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Arashiyama Bamboo Grove',
              description: "The towering bamboo stalks create one of Japan's most photographed natural corridors. Walk through as morning light filters between the bamboo — genuinely one of the most atmospheric natural experiences in Japan. Arrive at 7am for a near-empty grove.",
              details: ['📍 Arashiyama, Nishikyo-ku', '🕐 Best at 7-8am', '💡 Combine with nearby Okochi Sanso garden']
            },
            {
              title: 'Arashiyama Monkey Park',
              description: "A mountain meadow park home to 120 Japanese macaques who roam freely. Feed them from a platform (food purchased inside) and enjoy panoramic views of Kyoto from the hilltop.",
              details: ['📍 Arashiyama, Saganaka 7-3', '🕐 9am-5pm (¥1,000 adults)', '💡 15-min walk uphill from the bamboo grove — or take the chairlift']
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Arashiyama Riverside Restaurants',
              description: 'The area around Togetsukyo Bridge has excellent riverside restaurants. Try tofu skin (yuba), Yudofu (hot tofu) hot pot, or seasonal kaiseki at one of the traditional riverside establishments.',
              meta: '📍 Near Togetsukyo Bridge · 💰 ¥2,000-4,000 · 🕐 Lunch starts 11:30am'
            }
          ],
          tips: []
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tenryu-ji Temple & Garden',
              description: "One of Kyoto's five great Zen temples, a UNESCO World Heritage site, and widely considered the most beautiful temple in Arashiyama. The garden by master designer Muso Soseki integrates perfectly with the surrounding mountain.",
              details: ['📍 68 Sagatenryuji Susukinobaba-cho, Ukyo-ku', '🕐 8:30am-5:30pm (¥500 garden, ¥800 including main hall)']
            },
            {
              title: 'Togetsukyo Bridge & Sagano',
              description: "Arashiyama's iconic wooden bridge — the 'Bridge of the Moon Crossing' — has been standing since the Heian period. Stroll across for views of the Hozu River and forested mountains. In November, the maples are spectacular.",
              details: ['📍 Arashiyama, free to cross', '💡 Best views from the river banks on either side']
            }
          ],
          meals: [
            {
              type: '🍽️ Afternoon Tea',
              name: 'Arashiyama Tea House',
              description: 'Sit at a traditional tea house near the bridge for matcha and seasonal wagashi. Watch the Hozu River flow beneath the bridge as the afternoon light turns golden.',
              meta: '📍 Near Togetsukyo Bridge · 💰 ¥600-1,000'
            }
          ],
          tips: [
            { type: 'tip', text: '💡 Take the Sagano Scenic Railway (Trickart) from Arashiyama to Kameoka (¥880, 25 min) — the train winds through the Hozu River gorge with stunning autumn views.' }
          ]
        }
      ],
      mapPins: [
        { lat: 35.0118, lng: 135.6722, label: 'Arashiyama Bamboo Grove', num: 1, cat: 'attraction', desc: "Towering bamboo — one of Japan's most iconic natural walks" },
        { lat: 35.0094, lng: 135.6783, label: 'Arashiyama Monkey Park', num: 2, cat: 'attraction', desc: 'Wild Japanese macaques on a mountain meadow with panoramic views' },
        { lat: 35.0157, lng: 135.6727, label: 'Tenryu-ji Temple', num: 3, cat: 'attraction', desc: "UNESCO Zen temple — arguably Kyoto's most beautiful garden" },
        { lat: 35.0139, lng: 135.6747, label: 'Togetsukyo Bridge', num: 4, cat: 'attraction', desc: "Iconic wooden bridge — 'Moon Crossing' — since the Heian period" },
        { lat: 35.0105, lng: 135.6755, label: 'Arashiyama Riverside', num: 5, cat: 'restaurant', desc: 'Riverside restaurants — tofu & kaiseki' }
      ]
    },

    // DAY 7 — November 20: Kiyomizudera, Sannenzaka & Gion
    {
      num: 7,
      date: 'November 20, 2026',
      title: 'Eastern Kyoto: Kiyomizudera, Sannenzaka & Gion',
      description: "Kyoto's most dramatic temple, a preserved traditional street, and an evening geisha district walk — eastern Kyoto is the city's soul.",
      neighborhoods: 'Higashiyama · Gion · Yasaka',
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Kiyomizudera Temple',
              description: "One of Japan's most celebrated Buddhist temples, founded in 778 AD. Built on the edge of a cliff, its massive wooden stage (the 'pure water' stage) extends over a vista of Kyoto and beyond — in November, the maple colors stretch endlessly in every direction.",
              details: ['📍 1-294 Kiyomizu, Higashiyama-ku', '🕐 6am-6pm (¥500)', '💡 Go at opening (6am) to see the temple nearly alone — magical with morning mist']
            }
          ],
          meals: [
            {
              type: '🍽️ Breakfast',
              name: 'Morning Tea at Kiyomizudera',
              description: 'Before entering the temple, stop at one of the small tea stalls on the approach path for a cup of matcha and a wagashi sweet, eaten overlooking the valley below.',
              meta: '📍 Approach to Kiyomizudera · 💰 ¥400-800'
            }
          ],
          tips: []
        },
        {
          label: 'Late Morning / Midday',
          activities: [
            {
              title: 'Sannenzaka & Ninenzaka Streets',
              description: "The cobblestone approach to Kiyomizudera is one of Kyoto's most photographed streets — a perfectly preserved slice of Edo-era Japan, lined with traditional wooden shops, teah